#!/usr/bin/env python3
"""
scaneaza_folder.py - Scanner de folder pentru skill-ul file-organizer.

CE FACE:
    1. Scaneaza un folder (recursiv, optional) si listeaza fisierele.
    2. Detecteaza DUPLICATELE in mod sigur si rapid:
       - intai grupeaza fisierele dupa marime (rapid, fara a citi continutul),
       - apoi calculeaza hash (SHA-256) DOAR pentru fisierele cu aceeasi marime.
       Asa nu pierdem timp hashuind fisiere care evident sunt diferite.
    3. Grupeaza fisierele pe tip (extensie) si pe an-luna (data modificarii).
    4. PROPUNE o structura de foldere mai buna (plan), pe categorii sau pe data.

SIGURANTA (foarte important):
    Scriptul ruleaza implicit in mod DRY-RUN: NU muta, NU redenumeste si NU sterge
    NICIODATA nimic. Doar citeste si afiseaza un plan. Mutarea efectiva se face doar
    daca dai explicit flag-ul --aplica, iar atunci fiecare mutare e logata intr-un
    fisier de jurnal (plan_mutari.csv) ca sa poata fi anulata manual la nevoie.
    Stergerea de fisiere NU este implementata deloc, intentionat - duplicatele doar
    se raporteaza, decizia de stergere ramane mereu la om.

EXEMPLU DE RULARE:
    # 1. Doar analiza si plan (NU schimba nimic) - asa pornesti mereu:
    python3 scaneaza_folder.py ~/Downloads

    # 2. Recursiv, gruparea pe data (an/luna) in loc de tip:
    python3 scaneaza_folder.py ~/Downloads --recursiv --dupa data

    # 3. Salveaza planul intr-un fisier si vezi doar duplicatele:
    python3 scaneaza_folder.py ~/Downloads --json plan.json

    # 4. APLICA efectiv planul (cere confirmare; logheaza in plan_mutari.csv):
    python3 scaneaza_folder.py ~/Downloads --aplica

Functioneaza cu Python 3.8+ din biblioteca standard (fara pachete externe).
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import shutil
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

# --- Taxonomie de tipuri de fisiere (extensie -> categorie in limba romana) ---
CATEGORII = {
    "Documente": {
        ".pdf", ".doc", ".docx", ".odt", ".txt", ".rtf", ".md",
        ".tex", ".pages",
    },
    "Foi_de_calcul": {".xls", ".xlsx", ".csv", ".ods", ".numbers", ".tsv"},
    "Prezentari": {".ppt", ".pptx", ".odp", ".key"},
    "Imagini": {
        ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".tif",
        ".webp", ".heic", ".svg", ".raw",
    },
    "Video": {".mp4", ".mov", ".avi", ".mkv", ".wmv", ".webm", ".flv", ".m4v"},
    "Audio": {".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a", ".wma"},
    "Arhive": {".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".dmg", ".iso"},
    "Instalatoare": {".exe", ".msi", ".pkg", ".deb", ".rpm", ".appimage"},
    "Cod": {
        ".py", ".js", ".ts", ".html", ".css", ".json", ".xml", ".yml",
        ".yaml", ".sh", ".java", ".c", ".cpp", ".go", ".rs", ".sql",
    },
}

# Marime sub care ignoram duplicatele (fisiere goale / minuscule = zgomot).
PRAG_MARIME_DUPLICAT = 1  # bytes


def categorie_pentru(extensie: str) -> str:
    """Returneaza categoria (folderul propus) pentru o extensie de fisier."""
    ext = extensie.lower()
    for nume_categorie, extensii in CATEGORII.items():
        if ext in extensii:
            return nume_categorie
    return "Diverse"


def hash_fisier(cale: Path, algoritm: str = "sha256", bloc: int = 1 << 20) -> str:
    """
    Calculeaza hash-ul unui fisier citindu-l in blocuri (nu incarca tot in memorie).

    Foloseste SHA-256 implicit: rezistent la coliziuni, deci doua fisiere cu acelasi
    hash sunt practic sigur identice. Citirea in blocuri de 1 MB permite hashuirea
    fisierelor mari (video, arhive) fara probleme de memorie.
    """
    h = hashlib.new(algoritm)
    with open(cale, "rb") as f:
        for chunk in iter(lambda: f.read(bloc), b""):
            h.update(chunk)
    return h.hexdigest()


def colecteaza_fisiere(radacina: Path, recursiv: bool) -> list[Path]:
    """Aduna toate fisierele dintr-un folder (recursiv sau doar primul nivel)."""
    if recursiv:
        return [p for p in radacina.rglob("*") if p.is_file()]
    return [p for p in radacina.iterdir() if p.is_file()]


def gaseste_duplicate(fisiere: list[Path]) -> list[list[Path]]:
    """
    Gaseste grupurile de fisiere identice.

    Strategie sigura si eficienta (sursa: practica standard de deduplicare):
        Pasul 1: grupeaza dupa MARIME. Fisierele cu marimi diferite nu pot fi
                 identice, deci le excludem fara sa citim continutul (foarte rapid).
        Pasul 2: doar in grupurile cu aceeasi marime, calculeaza hash SHA-256
                 si compara. Asa hashuim strictul necesar.
    """
    dupa_marime: dict[int, list[Path]] = defaultdict(list)
    for cale in fisiere:
        try:
            marime = cale.stat().st_size
        except OSError:
            continue
        if marime >= PRAG_MARIME_DUPLICAT:
            dupa_marime[marime].append(cale)

    duplicate: list[list[Path]] = []
    for marime, candidati in dupa_marime.items():
        if len(candidati) < 2:
            continue  # marime unica -> nu poate fi duplicat
        dupa_hash: dict[str, list[Path]] = defaultdict(list)
        for cale in candidati:
            try:
                dupa_hash[hash_fisier(cale)].append(cale)
            except OSError:
                continue
        for grup in dupa_hash.values():
            if len(grup) >= 2:
                duplicate.append(sorted(grup, key=lambda p: str(p)))
    return duplicate


def an_luna(cale: Path) -> str:
    """Returneaza folderul de data (ex: '2026/06-Iunie') din data modificarii."""
    luni = [
        "Ianuarie", "Februarie", "Martie", "Aprilie", "Mai", "Iunie",
        "Iulie", "August", "Septembrie", "Octombrie", "Noiembrie", "Decembrie",
    ]
    dt = datetime.fromtimestamp(cale.stat().st_mtime)
    return f"{dt.year}/{dt.month:02d}-{luni[dt.month - 1]}"


def construieste_plan(fisiere: list[Path], radacina: Path, dupa: str) -> list[dict]:
    """
    Construieste planul de organizare: pentru fiecare fisier, folderul propus.

    'dupa' poate fi 'tip' (categorie pe extensie) sau 'data' (an/luna).
    Returneaza o lista de dictionare {sursa, destinatie, categorie}.
    Planul NU se aplica aici - doar se descrie.
    """
    plan = []
    for cale in fisiere:
        if dupa == "data":
            try:
                sub = an_luna(cale)
            except OSError:
                sub = "Necunoscut"
        else:
            sub = categorie_pentru(cale.suffix)
        destinatie = radacina / sub / cale.name
        plan.append({
            "sursa": str(cale),
            "destinatie": str(destinatie),
            "categorie": sub,
        })
    return plan


def destinatie_fara_conflict(dest: Path) -> Path:
    """
    Daca destinatia exista deja, adauga un sufix (-1, -2, ...) ca sa NU suprascrie.
    shutil.move suprascrie tacut fisierul de la destinatie, deci protejam explicit.
    """
    if not dest.exists():
        return dest
    tulpina, sufix = dest.stem, dest.suffix
    i = 1
    while True:
        candidat = dest.with_name(f"{tulpina}-{i}{sufix}")
        if not candidat.exists():
            return candidat
        i += 1


def aplica_plan(plan: list[dict], radacina: Path) -> Path:
    """
    APLICA planul: muta efectiv fisierele si scrie un jurnal CSV pentru anulare.

    Se apeleaza DOAR cand utilizatorul a dat --aplica si a confirmat.
    Jurnalul (plan_mutari.csv) contine sursa si destinatia reala a fiecarui fisier,
    ca mutarile sa poata fi inversate manual la nevoie.
    """
    jurnal = radacina / "plan_mutari.csv"
    mutate = 0
    with open(jurnal, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["sursa", "destinatie", "moment"])
        for item in plan:
            sursa = Path(item["sursa"])
            dest = destinatie_fara_conflict(Path(item["destinatie"]))
            if sursa == dest or not sursa.exists():
                continue
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(sursa), str(dest))
            writer.writerow([str(sursa), str(dest), datetime.now().isoformat()])
            mutate += 1
    print(f"\n  Mutate {mutate} fisiere. Jurnal pentru anulare: {jurnal}")
    return jurnal


def raporteaza(fisiere, duplicate, plan, dupa) -> None:
    """Afiseaza raportul lizibil in terminal (rezumat + duplicate + plan)."""
    print("=" * 64)
    print("  RAPORT ORGANIZARE FOLDER  (mod DRY-RUN - nimic nu s-a schimbat)")
    print("=" * 64)
    print(f"\n  Total fisiere analizate: {len(fisiere)}")

    pe_categorie: dict[str, int] = defaultdict(int)
    for item in plan:
        pe_categorie[item["categorie"]] += 1
    print(f"\n  Structura propusa (grupare dupa: {dupa}):")
    for categorie, n in sorted(pe_categorie.items(), key=lambda x: -x[1]):
        print(f"    {categorie:<24} {n:>4} fisiere")

    print(f"\n  Seturi de duplicate gasite: {len(duplicate)}")
    spatiu_irosit = 0
    for i, grup in enumerate(duplicate, 1):
        marime = grup[0].stat().st_size
        spatiu_irosit += marime * (len(grup) - 1)
        print(f"\n  Duplicat #{i}  ({marime / 1024:.0f} KB fiecare, {len(grup)} copii):")
        for cale in grup:
            print(f"      {cale}")
        print(f"      -> Pastreaza una, restul pot fi sterse (cu confirmarea ta).")
    if duplicate:
        print(f"\n  Spatiu recuperabil prin stergerea copiilor: "
              f"{spatiu_irosit / (1024*1024):.1f} MB")

    print("\n" + "=" * 64)
    print("  Acesta este DOAR un plan. Ca sa aplici: adauga flag-ul --aplica")
    print("  Stergerea duplicatelor NU este automata - ramane decizia ta.")
    print("=" * 64)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Scaneaza un folder, gaseste duplicate si propune o structura "
                    "(DRY-RUN implicit - nu schimba nimic fara --aplica).",
    )
    parser.add_argument("folder", help="Folderul de analizat (ex: ~/Downloads)")
    parser.add_argument("--recursiv", action="store_true",
                        help="Intra si in subfoldere")
    parser.add_argument("--dupa", choices=["tip", "data"], default="tip",
                        help="Grupare dupa tip (extensie) sau data (an/luna)")
    parser.add_argument("--json", metavar="FISIER",
                        help="Salveaza planul si duplicatele intr-un fisier JSON")
    parser.add_argument("--aplica", action="store_true",
                        help="APLICA efectiv planul (muta fisierele; cere confirmare)")
    args = parser.parse_args()

    radacina = Path(os.path.expanduser(args.folder)).resolve()
    if not radacina.is_dir():
        print(f"Eroare: '{radacina}' nu este un folder valid.", file=sys.stderr)
        return 1

    fisiere = colecteaza_fisiere(radacina, args.recursiv)
    if not fisiere:
        print("Folderul nu contine fisiere de organizat.")
        return 0

    duplicate = gaseste_duplicate(fisiere)
    plan = construieste_plan(fisiere, radacina, args.dupa)

    raporteaza(fisiere, duplicate, plan, args.dupa)

    if args.json:
        date = {
            "folder": str(radacina),
            "total_fisiere": len(fisiere),
            "plan": plan,
            "duplicate": [[str(p) for p in grup] for grup in duplicate],
        }
        Path(args.json).write_text(
            json.dumps(date, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"\n  Plan salvat in: {args.json}")

    if args.aplica:
        print("\n  ATENTIE: urmeaza sa MUT efectiv fisierele conform planului de mai sus.")
        raspuns = input("  Continui? Scrie 'da' pentru a aplica: ").strip().lower()
        if raspuns == "da":
            aplica_plan(plan, radacina)
        else:
            print("  Anulat. Nu s-a schimbat nimic.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
