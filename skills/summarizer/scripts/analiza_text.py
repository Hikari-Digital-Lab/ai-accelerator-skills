#!/usr/bin/env python3
"""Analizează un text lung înainte de rezumare.

Ce face, în limbaj de business:
- numără cuvintele și caracterele;
- estimează cât durează citirea (la ~200 cuvinte/minut);
- decide dacă textul e prea scurt pentru a merita un rezumat (anti-trigger);
- decide dacă textul e atât de lung încât trebuie împărțit în bucăți
  ("chunking") și rezumat în pași (strategia map-reduce);
- dacă da, taie textul în bucăți la limite naturale (paragrafe / fraze),
  fără să rupă cuvinte la jumătate, și salvează fiecare bucată într-un
  fișier separat pe care îl rezumi pe rând.

Folosire (din folderul skill-ului):
    python scripts/analiza_text.py "text lipit direct între ghilimele"
    python scripts/analiza_text.py --fisier /cale/catre/document.txt
    python scripts/analiza_text.py --fisier doc.md --cuvinte-bucata 1500

Fără dependențe externe — doar biblioteca standard Python 3.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys

# Viteză medie de citire pentru adulți, în cuvinte pe minut.
CUVINTE_PE_MINUT = 200

# Sub atâtea cuvinte, un text e deja scurt — rezumatul nu aduce valoare
# (vezi anti-trigger-ul din SKILL.md: "text deja foarte scurt").
PRAG_PREA_SCURT = 40

# Peste atâtea cuvinte, textul nu mai încape confortabil într-un singur pas;
# îl împărțim în bucăți și rezumăm map-reduce (rezumat pe bucăți → rezumat final).
PRAG_LUNG = 2500

# Câte cuvinte punem implicit într-o bucată când împărțim un document lung.
CUVINTE_PE_BUCATA = 1500


def numara_cuvinte(text: str) -> int:
    """Numără cuvintele (orice secvență de caractere non-spațiu)."""
    return len(re.findall(r"\S+", text))


def minute_citire(nr_cuvinte: int) -> float:
    """Estimează minutele de citire, rotunjit la o zecimală."""
    return round(nr_cuvinte / CUVINTE_PE_MINUT, 1)


def imparte_in_paragrafe(text: str) -> list[str]:
    """Împarte textul în paragrafe după liniile goale."""
    bucati = re.split(r"\n\s*\n", text.strip())
    return [p.strip() for p in bucati if p.strip()]


def imparte_in_fraze(text: str) -> list[str]:
    """Împarte un bloc de text în fraze, păstrând semnele de punctuație."""
    fraze = re.split(r"(?<=[.!?])\s+", text.strip())
    return [f.strip() for f in fraze if f.strip()]


def chunk_text(text: str, cuvinte_pe_bucata: int = CUVINTE_PE_BUCATA) -> list[str]:
    """Taie textul în bucăți de ~cuvinte_pe_bucata, la limite naturale.

    Strategia: adună paragrafe întregi într-o bucată până se atinge limita.
    Dacă un singur paragraf depășește limita, îl sparge mai departe pe fraze.
    Nu rupe niciodată cuvinte la jumătate.
    """
    bucati: list[str] = []
    curent: list[str] = []
    cuvinte_curent = 0

    def descarca() -> None:
        nonlocal curent, cuvinte_curent
        if curent:
            bucati.append("\n\n".join(curent).strip())
            curent = []
            cuvinte_curent = 0

    for paragraf in imparte_in_paragrafe(text):
        cuvinte_par = numara_cuvinte(paragraf)

        # Paragraf uriaș: îl spargem pe fraze, grupând până la limită.
        if cuvinte_par > cuvinte_pe_bucata:
            descarca()
            grup: list[str] = []
            cuvinte_grup = 0
            for fraza in imparte_in_fraze(paragraf):
                cuvinte_fr = numara_cuvinte(fraza)
                if cuvinte_grup + cuvinte_fr > cuvinte_pe_bucata and grup:
                    bucati.append(" ".join(grup).strip())
                    grup = []
                    cuvinte_grup = 0
                grup.append(fraza)
                cuvinte_grup += cuvinte_fr
            if grup:
                bucati.append(" ".join(grup).strip())
            continue

        # Dacă adăugarea paragrafului depășește limita, închidem bucata curentă.
        if cuvinte_curent + cuvinte_par > cuvinte_pe_bucata and curent:
            descarca()

        curent.append(paragraf)
        cuvinte_curent += cuvinte_par

    descarca()
    return bucati


def salveaza_bucati(bucati: list[str], director: str) -> list[str]:
    """Salvează fiecare bucată într-un fișier .txt și întoarce căile."""
    os.makedirs(director, exist_ok=True)
    cai: list[str] = []
    total = len(bucati)
    for i, bucata in enumerate(bucati, start=1):
        cale = os.path.join(director, f"bucata-{i:02d}-din-{total:02d}.txt")
        with open(cale, "w", encoding="utf-8") as f:
            f.write(bucata)
        cai.append(cale)
    return cai


def analizeaza(text: str, cuvinte_pe_bucata: int = CUVINTE_PE_BUCATA) -> dict:
    """Întoarce un dicționar cu verdictul + metrici despre text."""
    nr_cuvinte = numara_cuvinte(text)
    prea_scurt = nr_cuvinte < PRAG_PREA_SCURT
    necesita_chunking = nr_cuvinte > PRAG_LUNG

    if prea_scurt:
        recomandare = (
            "Text deja scurt — NU activa rezumatul (anti-trigger). "
            "Răspunde direct, fără TL;DR formal."
        )
        strategie = "fara_rezumat"
    elif necesita_chunking:
        recomandare = (
            "Text lung — împarte în bucăți și rezumă map-reduce: "
            "rezumă fiecare bucată, apoi combină rezumatele într-un TL;DR final."
        )
        strategie = "map_reduce"
    else:
        recomandare = "Text de dimensiune normală — rezumă într-un singur pas."
        strategie = "un_singur_pas"

    rezultat = {
        "nr_cuvinte": nr_cuvinte,
        "nr_caractere": len(text),
        "minute_citire": minute_citire(nr_cuvinte),
        "prea_scurt": prea_scurt,
        "necesita_chunking": necesita_chunking,
        "strategie": strategie,
        "recomandare": recomandare,
    }
    if necesita_chunking:
        rezultat["nr_bucati_estimat"] = len(chunk_text(text, cuvinte_pe_bucata))
    return rezultat


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Analizează un text înainte de rezumare (metrici + chunking)."
    )
    parser.add_argument(
        "text", nargs="?", default=None, help="Textul lipit direct (între ghilimele)."
    )
    parser.add_argument(
        "--fisier", "-f", help="Cale către un fișier .txt sau .md de analizat."
    )
    parser.add_argument(
        "--cuvinte-bucata",
        type=int,
        default=CUVINTE_PE_BUCATA,
        help=f"Câte cuvinte într-o bucată la împărțire (implicit {CUVINTE_PE_BUCATA}).",
    )
    parser.add_argument(
        "--salveaza-bucati",
        metavar="DIRECTOR",
        help="Dacă textul e lung, salvează bucățile ca fișiere în acest director.",
    )
    args = parser.parse_args(argv)

    if args.fisier:
        try:
            with open(args.fisier, "r", encoding="utf-8") as f:
                text = f.read()
        except OSError as e:
            print(f"Eroare la citirea fișierului: {e}", file=sys.stderr)
            return 1
    elif args.text:
        text = args.text
    else:
        text = sys.stdin.read()

    if not text.strip():
        print("Niciun text de analizat (input gol).", file=sys.stderr)
        return 1

    rezultat = analizeaza(text, args.cuvinte_bucata)

    if args.salveaza_bucati and rezultat["necesita_chunking"]:
        bucati = chunk_text(text, args.cuvinte_bucata)
        rezultat["fisiere_bucati"] = salveaza_bucati(bucati, args.salveaza_bucati)

    print(json.dumps(rezultat, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
