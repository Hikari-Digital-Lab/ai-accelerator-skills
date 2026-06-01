#!/usr/bin/env python3
"""Validator si schelet (scaffolder) pentru slide-uri Markdown destinate gamma.app.

Acest script face doua lucruri, in functie de comanda:

1. VALIDARE (`check`) — verifica un fisier .md cu slide-uri si raporteaza:
   - numarul total de slide-uri (numarate dupa separatorul `---`);
   - slide-urile prea DENSE (prea mult text / prea multe bullet-uri) — regula
     implicita: maxim 5 bullet-uri si maxim 50 de cuvinte per slide;
   - slide-urile FARA titlu (fara nicio linie care incepe cu `#`);
   - separatoarele lipsa intre slide-uri (doua titluri fara `---` intre ele);
   - tabelele cu prea multe randuri (peste 5 randuri de date).

2. SCHELET (`scaffold`) — genereaza un fisier gol cu N slide-uri, separate corect
   prin `---`, gata de completat si de importat in gamma.app.

FORMAT GAMMA.APP (sursa de adevar din repo + documentatia Gamma):
   - fiecare slide e separat de urmatorul printr-o linie cu exact `---`
     (regula orizontala Markdown = un card nou in gamma.app);
   - un slide are de obicei un titlu Markdown (`#`, `##` sau `###`);
   - gamma.app importa Markdown standard: titluri, bullet-uri (`-`), liste
     numerotate, tabele, citate (`>`), blocuri de cod (```).

EXEMPLE DE UTILIZARE
   # Valideaza un fisier de slide-uri existent
   python3 valideaza_slideuri.py check prezentare.md

   # Valideaza cu praguri personalizate (max 4 bullet-uri, max 40 cuvinte / slide)
   python3 valideaza_slideuri.py check prezentare.md --max-bullets 4 --max-words 40

   # Genereaza un schelet gol de 10 slide-uri
   python3 valideaza_slideuri.py scaffold 10 --out schelet.md

   # Genereaza un schelet de 8 slide-uri si afiseaza-l in terminal (fara fisier)
   python3 valideaza_slideuri.py scaffold 8

Codul de iesire este 0 daca totul e ok si 1 daca validarea gaseste probleme —
util in pipeline-uri automate.
"""

import argparse
import re
import sys
from pathlib import Path

# Praguri implicite pentru densitatea unui slide (audienta business, slide-uri aerisite).
DEFAULT_MAX_BULLETS = 5
DEFAULT_MAX_WORDS = 50
DEFAULT_MAX_TABLE_ROWS = 5

SEPARATOR = "---"


def split_slides(text):
    """Imparte textul in slide-uri folosind separatorul `---` (regula orizontala).

    Ignora un eventual frontmatter YAML de la inceputul fisierului (intre doua `---`),
    pentru ca acela nu este un separator de slide. Returneaza o lista de tuple
    (numar_slide, continut_text).
    """
    lines = text.splitlines()

    # Sari peste frontmatter YAML daca fisierul incepe cu `---`.
    start = 0
    if lines and lines[0].strip() == SEPARATOR:
        for i in range(1, len(lines)):
            if lines[i].strip() == SEPARATOR:
                start = i + 1
                break

    chunks = []
    current = []
    for line in lines[start:]:
        if line.strip() == SEPARATOR:
            chunks.append("\n".join(current))
            current = []
        else:
            current.append(line)
    chunks.append("\n".join(current))

    # Un slide e "real" daca are macar o linie non-goala.
    slides = [c for c in chunks if c.strip()]

    # Daca exista marcatoare `## SLIDE`, primul bloc (titlul fisierului, ex.
    # `# Slide-uri: ...`) NU este un slide -> il ignoram daca nu are marcator.
    has_markers = any(
        re.search(r"^##\s+SLIDE\b", c, re.IGNORECASE | re.MULTILINE) for c in slides
    )
    if has_markers and slides:
        first = slides[0]
        if not re.search(r"^##\s+SLIDE\b", first, re.IGNORECASE | re.MULTILINE):
            slides = slides[1:]

    return list(enumerate(slides, start=1))


def count_bullets(slide_text):
    """Numara liniile de tip bullet sau lista numerotata dintr-un slide."""
    count = 0
    for line in slide_text.splitlines():
        stripped = line.strip()
        if re.match(r"^([-*+]|\d+[.)])\s+", stripped):
            count += 1
    return count


def count_words(slide_text):
    """Numara cuvintele dintr-un slide, fara liniile de cod si fara markup greu.

    Liniile dintr-un bloc de cod (``` ... ```) nu sunt numarate ca text de citit,
    pentru ca slide-urile cu cod sunt asteptate sa fie mai lungi.
    """
    words = 0
    in_code = False
    for line in slide_text.splitlines():
        if line.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        # Scoate markup-ul de baza inainte de a numara.
        clean = re.sub(r"[#>*_`|>-]", " ", line)
        words += len(clean.split())
    return words


def has_title(slide_text):
    """Verifica daca slide-ul are macar un titlu Markdown (`#`, `##`, `###`...)."""
    for line in slide_text.splitlines():
        if re.match(r"^#{1,6}\s+\S", line.strip()):
            return True
    return False


def max_table_rows(slide_text):
    """Returneaza numarul maxim de randuri de date dintr-un tabel Markdown din slide.

    Nu numara randul de antet si nici linia separatoare `|---|---|`.
    """
    rows = 0
    max_rows = 0
    for line in slide_text.splitlines():
        stripped = line.strip()
        is_table_row = stripped.startswith("|") and stripped.endswith("|")
        is_separator = bool(re.match(r"^\|[\s:|-]+\|$", stripped))
        if is_separator:
            # Linia `|---|---|` face parte din tabel, dar nu e rand de date:
            # nu o numaram si nu intrerupem tabelul.
            continue
        if is_table_row:
            rows += 1
        else:
            # Sfarsit de tabel: scade 1 pentru randul de antet.
            if rows > 1:
                max_rows = max(max_rows, rows - 1)
            rows = 0
    if rows > 1:
        max_rows = max(max_rows, rows - 1)
    return max_rows


def check_file(path, max_bullets, max_words, max_table_rows_allowed):
    """Valideaza un fisier de slide-uri. Returneaza (ok, raport_text)."""
    p = Path(path)
    if not p.exists():
        return False, f"EROARE: fisierul nu exista: {path}"

    text = p.read_text(encoding="utf-8")
    slides = split_slides(text)

    problems = []
    dense = []
    no_title = []
    big_tables = []

    for num, slide in slides:
        bullets = count_bullets(slide)
        words = count_words(slide)
        if bullets > max_bullets or words > max_words:
            dense.append((num, bullets, words))
        if not has_title(slide):
            no_title.append(num)
        t_rows = max_table_rows(slide)
        if t_rows > max_table_rows_allowed:
            big_tables.append((num, t_rows))

    # Avertizare daca par lipsa separatoare: doua marcatoare de slide `## SLIDE`
    # in acelasi bloc inseamna ca lipseste un `---` intre ele.
    missing_sep = []
    for num, slide in slides:
        slide_markers = sum(
            1 for line in slide.splitlines()
            if re.match(r"^##\s+SLIDE\b", line.strip(), re.IGNORECASE)
        )
        if slide_markers > 1:
            missing_sep.append((num, slide_markers))

    lines = []
    lines.append("=" * 50)
    lines.append("VALIDARE SLIDE-URI PENTRU GAMMA.APP")
    lines.append("=" * 50)
    lines.append(f"Fisier: {path}")
    lines.append(f"Total slide-uri: {len(slides)}")
    lines.append("")

    if dense:
        problems.append("dense")
        lines.append(f"SLIDE-URI PREA DENSE ({len(dense)}) "
                      f"— prag: max {max_bullets} bullet-uri / {max_words} cuvinte:")
        for num, b, w in dense:
            lines.append(f"  - Slide {num}: {b} bullet-uri, {w} cuvinte")
        lines.append("")

    if no_title:
        problems.append("fara titlu")
        lines.append(f"SLIDE-URI FARA TITLU ({len(no_title)}) "
                     f"— adauga un titlu cu `#` sau `##`:")
        lines.append("  - Slide-urile: " + ", ".join(str(n) for n in no_title))
        lines.append("")

    if big_tables:
        problems.append("tabele mari")
        lines.append(f"TABELE PREA MARI ({len(big_tables)}) "
                     f"— prag: max {max_table_rows_allowed} randuri de date:")
        for num, r in big_tables:
            lines.append(f"  - Slide {num}: {r} randuri (imparte tabelul pe 2 slide-uri)")
        lines.append("")

    if missing_sep:
        problems.append("separator posibil lipsa")
        lines.append(f"POSIBIL SEPARATOR `---` LIPSA ({len(missing_sep)}):")
        for num, t in missing_sep:
            lines.append(f"  - Slide {num}: are {t} titluri de nivel 1-2 "
                         f"(probabil 2 slide-uri lipite)")
        lines.append("")

    if not problems:
        lines.append("OK: toate slide-urile respecta regulile de densitate si format.")
        lines.append("Gata de import in gamma.app (copiaza continutul sau incarca .md).")
    else:
        lines.append("REZULTAT: probleme gasite -> " + ", ".join(problems))

    return (len(problems) == 0), "\n".join(lines)


SCAFFOLD_TEMPLATE = """## SLIDE 1 - TITLU

### {subtitlu}
# {titlu}

---

## SLIDE 2 - PROBLEMA

# Care e durerea?

Descrie in 2-3 randuri problema pe care o simte audienta.

**Concluzia care doare, pe scurt.**

---

## SLIDE 3 - SOLUTIA

# Ce propunem

- Ideea principala a solutiei
- Cum rezolva problema de mai sus

**Beneficiul cheie intr-o propozitie.**

---
"""

EXTRA_SLIDE = """## SLIDE {n} - TITLU DESCRIPTIV

# Titlul slide-ului

- Punct 1 (o idee per slide)
- Punct 2
- Punct 3

**Takeaway in bold.**

---
"""

CTA_SLIDE = """## SLIDE {n} - CALL TO ACTION

### Urmatorul pas

Mesajul de incheiere si actiunea concreta pe care o ceri.

**Pasul concret pe care vrei sa-l faca audienta.**

---
"""


def scaffold(n):
    """Genereaza textul unui schelet gol de N slide-uri, separate prin `---`."""
    if n < 1:
        n = 1
    header = "# Slide-uri: <Titlul Prezentarii>\n\n---\n\n"

    # Primele 3 slide-uri sunt template-ul de baza (titlu, problema, solutie).
    if n <= 3:
        # Taie template-ul de baza la numarul cerut.
        base = SCAFFOLD_TEMPLATE.strip().split("\n---\n")
        kept = base[:n]
        body = "\n\n---\n\n".join(s.strip() for s in kept) + "\n\n---\n"
        filled = body.format(
            subtitlu="Subtitlu scurt", titlu="Titlul Prezentarii"
        )
        return header + filled

    body = SCAFFOLD_TEMPLATE.format(
        subtitlu="Subtitlu scurt", titlu="Titlul Prezentarii"
    )
    # Slide-uri de continut intre slide 4 si penultimul.
    for i in range(4, n):
        body += "\n" + EXTRA_SLIDE.format(n=i)
    # Ultimul slide e mereu un CTA.
    body += "\n" + CTA_SLIDE.format(n=n)
    return header + body


def main():
    parser = argparse.ArgumentParser(
        description="Validator si scaffolder de slide-uri Markdown pentru gamma.app."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_check = sub.add_parser("check", help="Valideaza un fisier .md cu slide-uri.")
    p_check.add_argument("file", help="Calea catre fisierul .md de validat.")
    p_check.add_argument("--max-bullets", type=int, default=DEFAULT_MAX_BULLETS,
                         help=f"Maxim bullet-uri per slide (implicit {DEFAULT_MAX_BULLETS}).")
    p_check.add_argument("--max-words", type=int, default=DEFAULT_MAX_WORDS,
                         help=f"Maxim cuvinte per slide (implicit {DEFAULT_MAX_WORDS}).")
    p_check.add_argument("--max-table-rows", type=int, default=DEFAULT_MAX_TABLE_ROWS,
                         help=f"Maxim randuri de date per tabel (implicit {DEFAULT_MAX_TABLE_ROWS}).")

    p_scaf = sub.add_parser("scaffold", help="Genereaza un schelet gol de N slide-uri.")
    p_scaf.add_argument("n", type=int, help="Numarul de slide-uri din schelet.")
    p_scaf.add_argument("--out", help="Fisierul in care se scrie scheletul (optional).")

    args = parser.parse_args()

    if args.command == "check":
        ok, report = check_file(
            args.file, args.max_bullets, args.max_words, args.max_table_rows
        )
        print(report)
        sys.exit(0 if ok else 1)

    if args.command == "scaffold":
        content = scaffold(args.n)
        if args.out:
            Path(args.out).write_text(content, encoding="utf-8")
            print(f"Schelet de {args.n} slide-uri scris in: {args.out}")
        else:
            print(content)
        sys.exit(0)


if __name__ == "__main__":
    main()
