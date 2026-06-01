#!/usr/bin/env python3
"""Extractor de text din PDF + flagger de cuvinte-cheie de risc (RO + EN).

Pentru ce e: scoate textul real dintr-un PDF lung (contract, ofertă, termeni și
condiții) și marchează cuvintele-cheie care semnalează clauze de risc, ca un om de
business (non-tech) să vadă rapid unde sunt capcanele. NU este consultanță juridică
și NU decide nimic — doar extrage text și evidențiază unde să te uiți.

Cum se folosește:
    pip install pdfplumber
    python extract_pdf.py "/cale/catre/contract.pdf"

Opțional:
    python extract_pdf.py contract.pdf --text-out text.txt   # salvează textul extras
    python extract_pdf.py contract.pdf --json                 # raport JSON pe stdout

De ce pdfplumber: este licențiat MIT (sigur de distribuit), stabil și bun pe
documente de tip contract. Pentru viteză brută pe volume mari ar fi PyMuPDF, dar
acela e licențiat AGPL (mai restrictiv la distribuire). pypdf e ok doar pentru
extrageri triviale.

PDF scanat: dacă paginile sunt imagini (poze ale documentului), nu există strat de
text și extragerea iese (aproape) goală. Scriptul detectează asta și recomandă OCR
(vezi references/ocr-pdf-scanat.md). OCR-ul are nevoie de Tesseract (limba `ron`) +
Poppler, care NU se instalează cu pip.
"""

from __future__ import annotations

import argparse
import json
import re
import sys

# Sub câte caractere/pagină (în medie) considerăm că PDF-ul e probabil scanat.
# O pagină de contract are tipic câteva mii de caractere; sub ~50 e (aproape) gol.
SCANNED_AVG_CHARS_THRESHOLD = 50

# Dicționar de cuvinte-cheie de risc, grupate pe categorie. Fiecare intrare e o
# listă de pattern-uri (regex, case-insensitive) RO + EN. Categoriile reflectă
# red-flag-urile din references/checklist-clauze-risc.md.
RISK_KEYWORDS: dict[str, list[str]] = {
    "Auto-reînnoire": [
        r"re[îi]nnoire", r"prelungire automat", r"tacit[ăa] relocat",
        r"re[îi]nnoie?ște automat", r"auto[\s-]?renew", r"automatic(ally)? renew",
        r"evergreen", r"renewal term",
    ],
    "Reziliere / încetare": [
        r"reziliere", r"reziliaz", r"den[uü]n[țt]are", r"[îi]ncetare",
        r"pact comisoriu", r"rezilia.{0,15}de drept",
        r"terminat(e|ion)", r"terminate for convenience", r"early termination",
    ],
    "Penalități": [
        r"penalit", r"penaliz", r"daune", r"daune[\s-]?interese",
        r"dob[âa]nd[ăa] penalizatoare", r"penalty", r"penalties",
        r"late fee", r"liquidated damages",
    ],
    "Limitare răspundere": [
        r"limitare.{0,20}r[ăa]spundere", r"plafon.{0,15}r[ăa]spundere",
        r"r[ăa]spundere.{0,15}(limitat|nelimitat)", r"exonerare de r[ăa]spundere",
        r"limitation of liability", r"liabilit(y|ies)\s+cap", r"unlimited liabilit",
        r"liable", r"indemnif",  # indemnif acoperă RO „a despăgubi" via EN + indemnizare
    ],
    "Indemnizare / despăgubire": [
        r"indemniz", r"desp[ăa]gubir", r"a desp[ăa]gubi",
        r"hold harmless", r"indemnif(y|ication)",
    ],
    "Jurisdicție / lege aplicabilă": [
        r"jurisdic[țt]i", r"competen[țt]a.{0,15}instan", r"lege.{0,10}aplicabil",
        r"legea aplicabil", r"arbitraj", r"tribunal arbitral",
        r"governing law", r"jurisdiction", r"arbitration", r"venue", r"forum",
    ],
    "Exclusivitate / non-concurență": [
        r"exclusivitate", r"clauz[ăa] de exclusivitate", r"non[\s-]?concuren[țt]",
        r"neconcuren[țt]", r"exclusiv(e|ity)", r"non[\s-]?compete", r"exclusive supplier",
    ],
    "Confidențialitate": [
        r"confiden[țt]ialitate", r"informa[țt]ii confiden[țt]iale",
        r"nedivulgare", r"confidential", r"non[\s-]?disclosure", r"\bNDA\b",
    ],
    "Forță majoră": [
        r"for[țt][ăa] major", r"caz fortuit", r"force majeure",
    ],
    "Indexare / majorare preț": [
        r"indexare", r"actualizare.{0,10}pre[țt]", r"majorare.{0,10}pre[țt]",
        r"revizuire.{0,10}pre[țt]", r"price increase", r"price escalation",
        r"fee increase", r"\bCPI\b", r"infla[țt]i",
    ],
    "Modificare unilaterală": [
        r"modific.{0,20}unilateral", r"unilateral.{0,20}modific",
        r"modify.{0,20}unilateral", r"unilateral(ly)?.{0,15}(change|modif|amend)",
    ],
    "Date personale / GDPR": [
        r"date cu caracter personal", r"prelucrarea datelor", r"GDPR", r"RGPD",
        r"operator de date", r"persoan[ăa] vizat", r"data processing",
        r"\bDPA\b", r"personal data", r"data protection",
    ],
    "SLA / nivel serviciu": [
        r"\bSLA\b", r"nivel de serviciu", r"disponibilitate.{0,10}\d", r"uptime",
        r"service level", r"availability\s+\d",
    ],
    "Garanție": [
        r"garan[țt]i", r"viciu ascuns", r"conformitate.{0,10}produs",
        r"warrant(y|ies)", r"guarantee",
    ],
    "Termene / scadențe": [
        r"scaden[țt]", r"termen de plat[ăa]", r"preaviz", r"zile lucr[ăa]toare",
        r"zile calendaristice", r"\bdue date\b", r"notice period", r"deadline",
    ],
}


def extract_pages(pdf_path: str) -> list[str]:
    """Întoarce lista de texte, câte unul pe pagină. Erorile sunt tratate, nu pasate."""
    try:
        import pdfplumber  # import local ca mesajul de eroare să fie clar dacă lipsește
    except ImportError:
        sys.exit(
            "Lipsește pdfplumber. Instalează cu:\n    pip install pdfplumber"
        )

    try:
        pages: list[str] = []
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                pages.append(page.extract_text() or "")
        return pages
    except FileNotFoundError:
        sys.exit(f"Fișier inexistent: {pdf_path}")
    except Exception as exc:  # PDF corupt / criptat / format neașteptat
        sys.exit(
            f"Nu am putut deschide PDF-ul ({type(exc).__name__}: {exc}).\n"
            "Dacă e protejat cu parolă, deblochează-l întâi. Dacă e scanat, vezi "
            "references/ocr-pdf-scanat.md."
        )


def looks_scanned(pages: list[str]) -> bool:
    """True dacă media de caractere/pagină e foarte mică (probabil PDF scanat)."""
    if not pages:
        return True
    total = sum(len(p.strip()) for p in pages)
    return (total / len(pages)) < SCANNED_AVG_CHARS_THRESHOLD


def find_risk_flags(pages: list[str]) -> dict[str, list[dict]]:
    """Caută cuvintele-cheie de risc. Întoarce {categorie: [{pagina, context}, ...]}."""
    compiled = {
        cat: [re.compile(p, re.IGNORECASE) for p in patterns]
        for cat, patterns in RISK_KEYWORDS.items()
    }
    results: dict[str, list[dict]] = {}
    for page_no, text in enumerate(pages, start=1):
        if not text:
            continue
        for cat, regexes in compiled.items():
            for rx in regexes:
                for m in rx.finditer(text):
                    start = max(0, m.start() - 50)
                    end = min(len(text), m.end() + 50)
                    snippet = " ".join(text[start:end].split())
                    results.setdefault(cat, []).append(
                        {"pagina": page_no, "context": snippet}
                    )
    return results


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Extrage text dintr-un PDF și marchează cuvinte-cheie de risc (RO+EN)."
    )
    parser.add_argument("pdf", help="Calea către fișierul PDF")
    parser.add_argument("--text-out", help="Salvează textul extras în acest fișier")
    parser.add_argument("--json", action="store_true", help="Raport JSON pe stdout")
    args = parser.parse_args()

    pages = extract_pages(args.pdf)
    scanned = looks_scanned(pages)
    flags = {} if scanned else find_risk_flags(pages)
    full_text = "\n\n".join(
        f"--- Pagina {i} ---\n{t}" for i, t in enumerate(pages, start=1)
    )

    if args.text_out:
        with open(args.text_out, "w", encoding="utf-8") as f:
            f.write(full_text)

    if args.json:
        print(json.dumps(
            {
                "fisier": args.pdf,
                "pagini": len(pages),
                "probabil_scanat": scanned,
                "flaguri_risc": flags,
            },
            ensure_ascii=False,
            indent=2,
        ))
        return

    # Raport pentru oameni (stdout)
    print(f"Fișier: {args.pdf}")
    print(f"Pagini: {len(pages)}")
    if scanned:
        print(
            "\n[!] PDF probabil SCANAT / fără strat de text (extragere aproape goală).\n"
            "    Ai nevoie de OCR. Vezi references/ocr-pdf-scanat.md.\n"
            "    Pe scurt: ocrmypdf -l ron+eng intrare.pdf iesire.pdf, apoi rulează din nou."
        )
        return

    if not flags:
        print("\nNiciun cuvânt-cheie de risc detectat automat.")
        print("ATENȚIE: asta NU înseamnă că documentul e fără riscuri — un cuvânt-cheie")
        print("poate lipsi chiar dacă riscul există. Parcurge documentul cu checklist-ul.")
    else:
        print(f"\nFlag-uri de risc detectate ({len(flags)} categorii):\n")
        for cat, hits in flags.items():
            pagini = sorted({h["pagina"] for h in hits})
            print(f"  • {cat}  (pag. {', '.join(map(str, pagini))}, {len(hits)} potriviri)")
            print(f"      ex: \"...{hits[0]['context']}...\"")

    print(
        "\n---\nAceasta NU este consultanță juridică. Cuvintele-cheie doar arată UNDE "
        "să te uiți. Confirmă clauzele în PDF și, pentru decizii importante, consultă "
        "un avocat. Detalii per risc: references/checklist-clauze-risc.md."
    )


if __name__ == "__main__":
    main()
