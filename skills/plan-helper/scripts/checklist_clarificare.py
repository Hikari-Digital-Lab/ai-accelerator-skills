#!/usr/bin/env python3
"""Generator de checklist de clarificare pentru plan-helper.

Plecând de la obiectivul brut al utilizatorului (o frază), generează:
  1. O listă de întrebări de clarificare grupate pe cele 6 zone ale
     cadrului de elicitare 95% (obiectiv, audiență, scope, constrângeri,
     format, polish).
  2. O analiză de complexitate care detectează cuvântul "ȘI" și verbele
     multiple, semnalând nevoia de spargere în procese separate
     (heuristica "cuvântul ȘI = 2 procese").
  3. Un schelet de plan (BLUF + pași) gata de completat.

Nu are dependențe externe — doar biblioteca standard Python 3.
Sigur de rulat oriunde există python3.

Utilizare:
    python checklist_clarificare.py "obiectivul utilizatorului aici"
    python checklist_clarificare.py "citește emailuri ȘI răspunde" --json
    echo "planifică o campanie" | python checklist_clarificare.py

Exemple:
    python checklist_clarificare.py "Fă-mi un plan pentru newsletter"
    python checklist_clarificare.py "vreau să citesc facturi ȘI să le pun în tabel"
"""

import argparse
import json
import re
import sys

# Cele 6 zone ale cadrului de elicitare 95% + întrebări reutilizabile.
ZONE_INTREBARI = {
    "Obiectiv (CE & DE CE)": [
        "Care e rezultatul concret pe care îl vrei la final?",
        "Ce problemă rezolvă asta pentru tine sau pentru business?",
        "Cum vei ști că a ieșit bine? (definiția de „gata”)",
    ],
    "Audiență / beneficiar (PENTRU CINE)": [
        "Cine folosește sau primește rezultatul? (tu, clienții, echipa?)",
        "Ce ton se potrivește publicului: formal sau prietenos?",
    ],
    "Scope (CE INTRĂ / CE NU)": [
        "Ce trebuie neapărat inclus? (must-have)",
        "Ce ar fi frumos, dar nu e obligatoriu? (nice-to-have)",
        "Ce e clar în AFARA acestui task? (ca să nu existe surprize)",
    ],
    "Constrângeri (CÂND / CU CE / CÂT)": [
        "Există un termen-limită?",
        "Ce unelte sau conturi ai deja disponibile?",
        "Există ceva ce TREBUIE folosit sau, dimpotrivă, evitat?",
    ],
    "Format rezultat (CUM ARATĂ)": [
        "În ce formă vrei rezultatul? (text, tabel/Excel, fișiere, postări?)",
        "Unde ajunge livrabilul? (un fișier local, un email, o platformă?)",
    ],
    "Polish & exemple": [
        "Cât de șlefuit trebuie să fie: ciornă rapidă sau versiune finală?",
        "Ai un exemplu de „așa vreau” sau „așa NU vreau”?",
    ],
}

# Verbe de acțiune frecvente în cereri de business. Fiecare cheie e numele
# verbului; valoarea e lista de rădăcini/forme care indică acel verb. Grupăm
# astfel încât același verb (ex: „citi” via „citesc” sau „cite”) să conteze
# o singură dată. Folosit ca semnal secundar de complexitate (verbe multiple
# diferite => mai multe procese).
VERBE_ACTIUNE = {
    "citi": ["citi", "citesc", "cite", "citești"],
    "scrie": ["scri", "scrie"],
    "trimite": ["trimit", "trimite"],
    "raspunde": ["raspund", "răspund"],
    "arhiva": ["arhiv"],
    "sterge": ["sterg", "șterg"],
    "sorta": ["sorta", "sortez"],
    "extrage": ["extrag", "extrage"],
    "salva": ["salv", "salvez"],
    "genera": ["genera", "generez"],
    "anunta/notifica": ["anunt", "anunț", "notific"],
    "publica/posta": ["publica", "postez", "posta"],
    "analiza": ["analiz"],
    "crea": ["creez", "crea", "cr?ază", "crăza"],
    "actualiza": ["actualiz"],
    "importa/exporta": ["import", "export"],
    "verifica": ["verific"],
    "compara": ["compar"],
    "traduce": ["traduc"],
}

# Conectori care anunță o a doua acțiune / proces. Potrivirea e
# case-insensitive, deci nu dublăm variantele cu majuscule. Pentru „și/si”
# folosim o singură expresie care prinde ambele scrieri (cu/fără diacritice).
CONECTORI_SI = [
    r"\b(?:și|si)\b",
    r"\b(?:și|si) apoi\b",
    r"\bplus c[ăa]\b",
    r"\bdup[ăa] care\b",
    r"\btotodat[ăa]\b",
]


def numara_conectori(text: str) -> int:
    """Numără aparițiile conectorilor de tip „ȘI”, fără dublă numărare.

    Conectorii lungi (ex: „și apoi”) sunt căutați primii și consumați din
    text, ca să nu fie numărați și de tiparul scurt („și”).
    """
    rest = text
    total = 0
    # Tiparele lungi înaintea celor scurte.
    pattern_ordonat = sorted(CONECTORI_SI, key=len, reverse=True)
    for pattern in pattern_ordonat:
        gasite = re.findall(pattern, rest, flags=re.IGNORECASE)
        total += len(gasite)
        # Înlocuiește potrivirile cu spațiu ca să nu fie renumărate.
        rest = re.sub(pattern, " ", rest, flags=re.IGNORECASE)
    return total


def detecteaza_verbe(text: str) -> list:
    """Întoarce lista verbelor de acțiune distincte găsite în text.

    Întoarce numele verbului (cheia din VERBE_ACTIUNE), nu rădăcina brută,
    astfel încât același verb scris în forme diferite să conteze o dată.
    """
    text_low = text.lower()
    gasite = []
    for nume_verb, forme in VERBE_ACTIUNE.items():
        if any(forma.lower() in text_low for forma in forme):
            gasite.append(nume_verb)
    return gasite


def analizeaza_complexitate(obiectiv: str) -> dict:
    """Estimează dacă task-ul trebuie spart în procese separate."""
    conectori = numara_conectori(obiectiv)
    verbe = detecteaza_verbe(obiectiv)
    # Procese estimate: cel puțin 1; fiecare conector adaugă unul; verbele
    # multiple sunt un semnal suplimentar (luăm maximul dintre cele două).
    procese_din_conectori = conectori + 1
    procese_din_verbe = max(1, len(verbe))
    procese_estimate = max(procese_din_conectori, procese_din_verbe)
    trebuie_spart = procese_estimate >= 2 and (conectori >= 1 or len(verbe) >= 2)
    return {
        "conectori_si": conectori,
        "verbe_actiune": verbe,
        "procese_estimate": procese_estimate,
        "trebuie_spart": trebuie_spart,
    }


def construieste_raport(obiectiv: str) -> dict:
    """Construiește raportul complet (date structurate)."""
    analiza = analizeaza_complexitate(obiectiv)
    return {
        "obiectiv": obiectiv.strip(),
        "analiza_complexitate": analiza,
        "intrebari_pe_zone": ZONE_INTREBARI,
    }


def afiseaza_text(raport: dict) -> None:
    """Afișează raportul lizibil pentru om."""
    obiectiv = raport["obiectiv"]
    analiza = raport["analiza_complexitate"]

    print("=" * 64)
    print("CHECKLIST DE CLARIFICARE — plan-helper")
    print("=" * 64)
    print(f'\nObiectiv primit: "{obiectiv}"\n')

    # --- Analiză de complexitate ---
    print("-" * 64)
    print("ANALIZĂ COMPLEXITATE (heuristica „cuvântul ȘI = 2 procese”)")
    print("-" * 64)
    print(f"  Conectori de tip „ȘI” găsiți : {analiza['conectori_si']}")
    if analiza["verbe_actiune"]:
        print(f"  Verbe de acțiune detectate   : {', '.join(analiza['verbe_actiune'])}")
    else:
        print("  Verbe de acțiune detectate   : (niciunul evident)")
    print(f"  Procese estimate             : {analiza['procese_estimate']}")
    if analiza["trebuie_spart"]:
        print("\n  >> SEMNAL: task-ul pare COMPLEX. Propune utilizatorului")
        print(f"     spargerea în ~{analiza['procese_estimate']} procese separate,")
        print("     fiecare cu un singur verb / livrabil.")
    else:
        print("\n  >> Task-ul pare a fi un singur proces. Probabil nu necesită spargere.")

    # --- Întrebări de clarificare ---
    print("\n" + "-" * 64)
    print("ÎNTREBĂRI DE PUS CU AskUserQuestion (formula 95%)")
    print("-" * 64)
    print("Regulă: max 4 întrebări per rundă. Întreabă doar ce nu știi din cerere.\n")
    nr = 1
    for zona, intrebari in raport["intrebari_pe_zone"].items():
        print(f"[{zona}]")
        for intrebare in intrebari:
            print(f"  {nr:>2}. {intrebare}")
            nr += 1
        print()

    # --- Schelet de plan ---
    print("-" * 64)
    print("SCHELET DE PLAN (de completat DUPĂ răspunsuri)")
    print("-" * 64)
    print("Rezultat final: [o frază BLUF — ce ai concret la final]\n")
    print("Plan:")
    nr_procese = analiza["procese_estimate"] if analiza["trebuie_spart"] else 3
    for i in range(1, nr_procese + 1):
        print(f"  {i}. [Verb] + [acțiune concretă] — [ce produce]")
    print("\nCe NU intră în acest plan: [scope-out explicit]")
    print("Riscuri / de confirmat: [1-3 puncte]")
    print("Model recomandat: Opus pentru planificare, Sonnet pentru execuție.")
    print()


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Generează un checklist de clarificare + analiză de "
                    "complexitate plecând de la obiectivul utilizatorului."
    )
    parser.add_argument(
        "obiectiv",
        nargs="*",
        help="Obiectivul brut al utilizatorului (între ghilimele). "
             "Dacă lipsește, se citește de la stdin.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Afișează rezultatul ca JSON (pentru integrări).",
    )
    args = parser.parse_args(argv)

    if args.obiectiv:
        obiectiv = " ".join(args.obiectiv)
    else:
        obiectiv = sys.stdin.read().strip()

    if not obiectiv:
        parser.error("Niciun obiectiv furnizat (argument sau stdin).")

    raport = construieste_raport(obiectiv)

    if args.json:
        print(json.dumps(raport, ensure_ascii=False, indent=2))
    else:
        afiseaza_text(raport)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
