#!/usr/bin/env python3
"""analizeaza_sesiuni.py — Analizator LOCAL al istoricului de conversații Claude Code.

CE FACE:
    Citește fișierele de sesiune `.jsonl` pe care Claude Code le salvează LOCAL pe
    calculatorul tău, în `~/.claude/projects/<cale-proiect-codificată>/`, și calculează
    tipare despre felul în care folosești asistentul:
      - câte sesiuni și câte mesaje ai;
      - lungimea medie a prompturilor TALE (doar mesaje tastate de tine, nu rezultate
        de tool-uri și nu mesaje generate de sistem);
      - prompturi prea scurte/vagi vs. prea lungi;
      - cât de des folosești `/clear` (igiena de context) și alte slash-commands;
      - ce modele apar (Haiku / Sonnet / Opus) și în ce proporție;
      - sesiuni foarte lungi (mulți pași = context aglomerat = credit irosit);
      - estimare de consum de tokeni (input/output/cache) din câmpul `usage`.
    La final scoate OBSERVAȚII text, gata de transformat în recomandări de coaching.

PRIVACY (foarte important):
    Totul rulează LOCAL. Scriptul DOAR CITEȘTE fișierele tale și NU trimite nimic
    în afară — fără rețea, fără upload, fără telemetrie. Nu modifică și nu șterge
    niciun fișier de sesiune. Implicit afișează DOAR statistici agregate; conținutul
    propriu-zis al prompturilor NU este afișat decât dacă ceri explicit `--exemple`,
    și chiar și atunci doar fragmente scurte, pentru ilustrare.

DE CE E SIGUR PE FORMAT:
    Formatul real al fișierelor (verificat pe instalări curente de Claude Code):
      - un obiect JSON per linie (JSON Lines);
      - liniile au `type`: "user", "assistant", "system", "summary",
        "file-history-snapshot" etc.;
      - mesajele TALE tastate au type="user" cu `message.content` ca STRING;
      - rezultatele de tool au tot type="user", dar `message.content` e o LISTĂ cu
        blocuri `tool_result` (sau există cheia `toolUseResult`) — acestea NU sunt
        prompturi scrise de tine, deci le excludem din statistica de prompting;
      - liniile cu `isMeta: true` sunt injectate de sistem — le excludem;
      - modelul e în `message.model`; consumul de tokeni în `message.usage`;
      - slash-commands apar în text ca `<command-name>/clear</command-name>`.
    Dacă apar câmpuri noi sau lipsesc unele, scriptul le ignoră grațios.

UTILIZARE:
    # Analizează tot istoricul (folderul implicit ~/.claude/projects):
    python3 analizeaza_sesiuni.py

    # Doar proiectul curent (caută folderul codificat după calea curentă):
    python3 analizeaza_sesiuni.py --proiect-curent

    # Un anume folder de proiect deja codificat:
    python3 analizeaza_sesiuni.py --proiect -home-user-myapp

    # Altă rădăcină (ex. test) și ieșire JSON pentru integrări:
    python3 analizeaza_sesiuni.py --root /cale/spre/projects --json

    # Cu fragmente scurte din cele mai scurte/lungi prompturi (ilustrativ):
    python3 analizeaza_sesiuni.py --exemple

Funcționează cu Python 3.8+ din biblioteca standard (fără pachete externe).
Tratează grațios cazul „nu există istoric" (folder gol sau inexistent).
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

# ---------------------------------------------------------------------------
# Constante de interpretare. Pragurile sunt orientative, alese ca să prindă
# tiparele descrise în curs (prompturi vagi vs. mega-prompturi, sesiuni umflate).
# ---------------------------------------------------------------------------

# Sub acest număr de caractere un prompt e probabil prea scurt/vag ("fă-mi un site").
PRAG_PROMPT_SCURT = 40
# Peste acest număr de caractere un prompt e probabil prea lung — semnal că ar fi
# meritat plan mode + AskUserQuestion în loc de un perete de text.
PRAG_PROMPT_LUNG = 1500
# Peste atâtea mesaje, o sesiune e „lungă": context aglomerat, candidat pentru /clear.
PRAG_SESIUNE_LUNGA = 60

# Familii de modele recunoscute din `message.model` (id-uri reale + aliasuri).
FAMILII_MODEL = {
    "haiku": "Haiku",
    "sonnet": "Sonnet",
    "opus": "Opus",
}


def encode_cale_proiect(cale: str) -> str:
    """Codifică o cale absolută în numele de folder folosit de Claude Code.

    Claude Code înlocuiește separatorii de cale cu „-". Ex.: /home/user/myapp ->
    -home-user-myapp. Reproducem aceeași regulă (non-alfanumeric -> „-") ca să
    putem găsi folderul proiectului curent.
    """
    return re.sub(r"[^a-zA-Z0-9]", "-", cale)


def gaseste_root(root_arg: str | None) -> Path:
    """Întoarce rădăcina `projects` (implicit ~/.claude/projects)."""
    if root_arg:
        return Path(os.path.expanduser(root_arg)).resolve()
    return Path(os.path.expanduser("~/.claude/projects")).resolve()


def selecteaza_foldere(root: Path, proiect: str | None,
                       proiect_curent: bool) -> list[Path]:
    """Alege folderele de proiect de analizat."""
    if not root.is_dir():
        return []
    if proiect:
        cand = root / proiect
        return [cand] if cand.is_dir() else []
    if proiect_curent:
        codificat = encode_cale_proiect(os.getcwd())
        cand = root / codificat
        if cand.is_dir():
            return [cand]
        # fallback: potrivire parțială (calea curentă poate fi un sub-folder)
        partiale = [d for d in root.iterdir()
                    if d.is_dir() and codificat in d.name]
        return partiale
    return [d for d in root.iterdir() if d.is_dir()]


def fisiere_sesiune(foldere: list[Path]) -> list[Path]:
    """Adună toate fișierele `.jsonl` de sesiune din folderele date.

    Fișierele de sesiune stau DIRECT în folderul proiectului (verificat pe
    instalări reale). Folosim `glob("*.jsonl")`, nerecursiv, ca să nu prindem
    eventuale loguri din alte locuri.
    """
    fisiere: list[Path] = []
    for folder in foldere:
        fisiere.extend(sorted(folder.glob("*.jsonl")))
    return fisiere


def este_prompt_utilizator(obj: dict) -> bool:
    """True doar dacă linia e un prompt TASTAT de utilizator (nu tool, nu meta)."""
    if obj.get("type") != "user":
        return False
    if obj.get("isMeta"):
        return False
    if "toolUseResult" in obj:  # rezultat de tool re-introdus ca mesaj user
        return False
    msg = obj.get("message")
    if not isinstance(msg, dict):
        return False
    content = msg.get("content")
    # Prompturile reale au content STRING. Listele sunt blocuri tool_result.
    return isinstance(content, str)


def text_prompt(obj: dict) -> str:
    """Întoarce textul prompt-ului user (string)."""
    return obj.get("message", {}).get("content", "") or ""


def familie_model(model: str) -> str | None:
    """Mapează un id de model pe familia Haiku/Sonnet/Opus."""
    low = (model or "").lower()
    for cheie, eticheta in FAMILII_MODEL.items():
        if cheie in low:
            return eticheta
    return None


# Slash-command-urile apar în text ca <command-name>/clear</command-name>.
RE_COMMAND = re.compile(r"<command-name>\s*(/[\w:-]+)\s*</command-name>")


def extrage_comenzi(text: str) -> list[str]:
    """Extrage slash-commands dintr-un prompt (ex. /clear, /model, /cost)."""
    return [c.lower() for c in RE_COMMAND.findall(text)]


def analizeaza_fisier(cale: Path, acc: dict) -> None:
    """Parcurge un fișier de sesiune și acumulează statistici în `acc`."""
    mesaje_sesiune = 0
    prompturi_sesiune = 0
    try:
        with open(cale, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    continue
                tip = obj.get("type")

                if tip in ("user", "assistant"):
                    mesaje_sesiune += 1
                    acc["mesaje_total"] += 1

                # --- Prompturi tastate de utilizator ---
                if este_prompt_utilizator(obj):
                    txt = text_prompt(obj)
                    comenzi = extrage_comenzi(txt)
                    if comenzi:
                        for c in comenzi:
                            acc["comenzi"][c] += 1
                        # Un mesaj care e DOAR o comandă nu se numără la prompting.
                        if RE_COMMAND.sub("", txt).strip() == "":
                            continue
                    lung = len(txt)
                    acc["prompturi_total"] += 1
                    acc["lungime_totala"] += lung
                    acc["lungimi"].append(lung)
                    prompturi_sesiune += 1
                    if lung < PRAG_PROMPT_SCURT:
                        acc["prompturi_scurte"] += 1
                        acc["exemple_scurte"].append((lung, txt))
                    elif lung > PRAG_PROMPT_LUNG:
                        acc["prompturi_lungi"] += 1
                        acc["exemple_lungi"].append((lung, txt))

                # --- Modele + tokeni din mesaje assistant ---
                if tip == "assistant":
                    msg = obj.get("message", {})
                    fam = familie_model(msg.get("model", ""))
                    if fam:
                        acc["modele"][fam] += 1
                    usage = msg.get("usage") or {}
                    acc["tok_input"] += usage.get("input_tokens", 0) or 0
                    acc["tok_output"] += usage.get("output_tokens", 0) or 0
                    acc["tok_cache_read"] += usage.get(
                        "cache_read_input_tokens", 0) or 0
                    acc["tok_cache_create"] += usage.get(
                        "cache_creation_input_tokens", 0) or 0
    except OSError:
        acc["fisiere_ilizibile"] += 1
        return

    acc["sesiuni_total"] += 1
    if mesaje_sesiune > PRAG_SESIUNE_LUNGA:
        acc["sesiuni_lungi"] += 1
        acc["detalii_sesiuni_lungi"].append((cale.name, mesaje_sesiune))


def acumulator_gol() -> dict:
    return {
        "sesiuni_total": 0,
        "mesaje_total": 0,
        "prompturi_total": 0,
        "lungime_totala": 0,
        "lungimi": [],
        "prompturi_scurte": 0,
        "prompturi_lungi": 0,
        "sesiuni_lungi": 0,
        "fisiere_ilizibile": 0,
        "comenzi": Counter(),
        "modele": Counter(),
        "tok_input": 0,
        "tok_output": 0,
        "tok_cache_read": 0,
        "tok_cache_create": 0,
        "exemple_scurte": [],
        "exemple_lungi": [],
        "detalii_sesiuni_lungi": [],
    }


def construieste_observatii(acc: dict) -> list[str]:
    """Transformă cifrele în observații text (semințe de recomandări)."""
    obs: list[str] = []
    prompturi = acc["prompturi_total"]
    if prompturi == 0:
        return ["Nu există prompturi tastate de analizat în acest istoric."]

    medie = acc["lungime_totala"] / prompturi
    obs.append(f"Lungime medie prompt: {medie:.0f} caractere "
               f"(din {prompturi} prompturi tastate).")

    pct_scurte = 100 * acc["prompturi_scurte"] / prompturi
    pct_lungi = 100 * acc["prompturi_lungi"] / prompturi
    if pct_scurte >= 25:
        obs.append(f"{pct_scurte:.0f}% din prompturi sunt foarte scurte "
                   f"(<{PRAG_PROMPT_SCURT} car.) — risc de cereri vagi. "
                   f"Recomandă formula AskUserQuestion 95% + plan mode.")
    if pct_lungi >= 10:
        obs.append(f"{pct_lungi:.0f}% din prompturi sunt foarte lungi "
                   f"(>{PRAG_PROMPT_LUNG} car.) — pereți de text. "
                   f"Recomandă spargerea (heuristica «ȘI = 2 procese») "
                   f"+ plan mode.")

    # /clear vs. sesiuni: igienă de context.
    nr_clear = acc["comenzi"].get("/clear", 0)
    if acc["sesiuni_total"]:
        clear_per_sesiune = nr_clear / acc["sesiuni_total"]
        if nr_clear == 0:
            obs.append("Niciun `/clear` în istoric — context probabil aglomerat "
                       "între task-uri. Recomandă `/clear` la fiecare task nou.")
        else:
            obs.append(f"`/clear` folosit de {nr_clear} ori "
                       f"({clear_per_sesiune:.1f}/sesiune).")

    if acc["sesiuni_lungi"]:
        obs.append(f"{acc['sesiuni_lungi']} sesiuni lungi "
                   f"(>{PRAG_SESIUNE_LUNGA} mesaje) — candidate pentru spargere "
                   f"în sesiuni mai mici cu `/clear` între ele.")

    # Modele.
    total_model = sum(acc["modele"].values())
    if total_model:
        distrib = ", ".join(f"{k} {100*v/total_model:.0f}%"
                            for k, v in acc["modele"].most_common())
        obs.append(f"Distribuție modele (răspunsuri): {distrib}.")
        pct_haiku = 100 * acc["modele"].get("Haiku", 0) / total_model
        pct_opus = 100 * acc["modele"].get("Opus", 0) / total_model
        if pct_haiku >= 40:
            obs.append(f"Haiku domină ({pct_haiku:.0f}%) — bun pentru cost, dar "
                       f"NU pentru plan mode/debug arhitectural. Verifică dacă "
                       f"planificarea se face pe Opus.")
        if pct_opus >= 80:
            obs.append(f"Opus pe {pct_opus:.0f}% din răspunsuri — posibil "
                       f"supra-folosit. Execuția de rutină merge pe Sonnet (mai ieftin).")

    # Tokeni / caching.
    total_tok = (acc["tok_input"] + acc["tok_output"]
                 + acc["tok_cache_read"] + acc["tok_cache_create"])
    if total_tok:
        cache = acc["tok_cache_read"] + acc["tok_cache_create"]
        pct_cache = 100 * cache / total_tok
        obs.append(f"Tokeni (estimare): input {acc['tok_input']:,}, "
                   f"output {acc['tok_output']:,}, cache {cache:,} "
                   f"({pct_cache:.0f}% din total trece prin cache).")

    # Comenzi de economie folosite.
    for cmd, eticheta in (("/cost", "verificarea costului"),
                          ("/context", "vizualizarea contextului"),
                          ("/model", "schimbarea modelului")):
        if acc["comenzi"].get(cmd, 0) == 0:
            obs.append(f"Nu apare `{cmd}` — sugerează {eticheta} periodic.")

    return obs


def afiseaza_text(acc: dict, root: Path, n_foldere: int,
                  exemple: bool) -> None:
    print("=" * 68)
    print("  INTERACTION COACH — analiză LOCALĂ a istoricului Claude Code")
    print("=" * 68)
    print(f"\n  Rădăcină : {root}")
    print(f"  Proiecte : {n_foldere}")
    print(f"  Privacy  : totul rulează local; nimic nu pleacă de pe calculator.\n")

    if acc["sesiuni_total"] == 0:
        print("  Nu am găsit fișiere de sesiune `.jsonl`.")
        print("  Posibile cauze: încă nu ai folosit Claude Code în acest proiect,")
        print("  istoricul e în altă locație, sau folderul e gol.")
        print("\n  Verifică: ~/.claude/projects/  sau rulează cu --root <cale>.")
        return

    print("-" * 68)
    print("  STATISTICI")
    print("-" * 68)
    print(f"  Sesiuni analizate          : {acc['sesiuni_total']}")
    print(f"  Mesaje (user+assistant)    : {acc['mesaje_total']}")
    print(f"  Prompturi tastate de tine  : {acc['prompturi_total']}")
    if acc["prompturi_total"]:
        medie = acc["lungime_totala"] / acc["prompturi_total"]
        lungimi = sorted(acc["lungimi"])
        median = lungimi[len(lungimi) // 2]
        print(f"  Lungime prompt (medie/median): {medie:.0f} / {median} car.")
        print(f"  Prompturi scurte (<{PRAG_PROMPT_SCURT})       : "
              f"{acc['prompturi_scurte']}")
        print(f"  Prompturi lungi (>{PRAG_PROMPT_LUNG})     : "
              f"{acc['prompturi_lungi']}")
    print(f"  Sesiuni lungi (>{PRAG_SESIUNE_LUNGA} mesaje) : {acc['sesiuni_lungi']}")
    if acc["fisiere_ilizibile"]:
        print(f"  Fișiere necitite           : {acc['fisiere_ilizibile']}")

    if acc["comenzi"]:
        print("\n  Slash-commands (top 8):")
        for cmd, n in acc["comenzi"].most_common(8):
            print(f"    {cmd:<22} {n:>5}")

    if acc["modele"]:
        print("\n  Modele (din răspunsuri assistant):")
        total_model = sum(acc["modele"].values())
        for fam, n in acc["modele"].most_common():
            print(f"    {fam:<10} {n:>6}  ({100*n/total_model:.0f}%)")

    print("\n" + "-" * 68)
    print("  OBSERVAȚII (semințe de recomandări)")
    print("-" * 68)
    for i, o in enumerate(construieste_observatii(acc), 1):
        print(f"  {i}. {o}")

    if exemple:
        print("\n" + "-" * 68)
        print("  FRAGMENTE ILUSTRATIVE (doar pentru context, scurtate)")
        print("-" * 68)
        scurte = sorted(acc["exemple_scurte"])[:3]
        lungi = sorted(acc["exemple_lungi"], reverse=True)[:3]
        if scurte:
            print("  Cele mai scurte prompturi:")
            for lung, txt in scurte:
                print(f"    [{lung} car.] {txt[:70]!r}")
        if lungi:
            print("  Cele mai lungi prompturi:")
            for lung, txt in lungi:
                print(f"    [{lung} car.] {txt[:70]!r}...")

    if acc["detalii_sesiuni_lungi"]:
        print("\n  Sesiuni lungi (candidate pentru /clear):")
        for nume, n in sorted(acc["detalii_sesiuni_lungi"],
                              key=lambda x: -x[1])[:5]:
            print(f"    {nume[:36]:<38} {n} mesaje")

    print("\n" + "=" * 68)
    print("  Folosește aceste observații ca să dai recomandări concrete,")
    print("  personalizate, conform skill-ului interaction-coach.")
    print("=" * 68)


def construieste_json(acc: dict) -> dict:
    """Versiune serializabilă (fără textul brut al prompturilor)."""
    out = {k: v for k, v in acc.items()
           if k not in ("lungimi", "exemple_scurte", "exemple_lungi",
                        "detalii_sesiuni_lungi", "comenzi", "modele")}
    out["comenzi"] = dict(acc["comenzi"])
    out["modele"] = dict(acc["modele"])
    out["sesiuni_lungi_detalii"] = [
        {"fisier": n, "mesaje": m} for n, m in acc["detalii_sesiuni_lungi"]]
    if acc["prompturi_total"]:
        out["lungime_medie_prompt"] = round(
            acc["lungime_totala"] / acc["prompturi_total"], 1)
    out["observatii"] = construieste_observatii(acc)
    return out


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Analizează LOCAL istoricul Claude Code (~/.claude/projects) "
                    "și scoate tipare + observații de coaching. Nu trimite nimic "
                    "în afară.")
    parser.add_argument("--root", help="Rădăcina folderului `projects` "
                        "(implicit ~/.claude/projects).")
    parser.add_argument("--proiect", help="Numele codificat al unui folder de "
                        "proiect (ex. -home-user-myapp).")
    parser.add_argument("--proiect-curent", action="store_true",
                        help="Analizează doar proiectul din directorul curent.")
    parser.add_argument("--exemple", action="store_true",
                        help="Afișează fragmente scurte din prompturi (ilustrativ).")
    parser.add_argument("--json", action="store_true",
                        help="Ieșire JSON (fără textul brut al prompturilor).")
    args = parser.parse_args(argv)

    root = gaseste_root(args.root)
    foldere = selecteaza_foldere(root, args.proiect, args.proiect_curent)
    fisiere = fisiere_sesiune(foldere)

    acc = acumulator_gol()
    for f in fisiere:
        analizeaza_fisier(f, acc)

    if args.json:
        date = construieste_json(acc)
        date["root"] = str(root)
        date["proiecte_analizate"] = len(foldere)
        print(json.dumps(date, ensure_ascii=False, indent=2))
    else:
        afiseaza_text(acc, root, len(foldere), args.exemple)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
