# OCR pentru PDF scanat (fără strat de text)

Citește acest fișier când `scripts/extract_pdf.py` raportează **„PDF probabil
scanat / fără strat de text"**. Asta înseamnă că paginile sunt imagini (poze ale
documentului), nu text selectabil — extractorul clasic nu poate scoate nimic util
și ai nevoie de **OCR** (Optical Character Recognition).

## Cuprins
1. Cum recunoști un PDF scanat
2. Ce ai nevoie (binare de sistem + pachete pip)
3. Varianta A — `ocrmypdf` (cel mai simplu)
4. Varianta B — `pdf2image` + `pytesseract` (control fin)
5. Limitări și verificări

## 1. Cum recunoști un PDF scanat

- Textul extras e gol sau aproape gol pe (aproape) toate paginile.
- În vizualizatorul de PDF nu poți selecta textul cu mouse-ul.
- Fișierul provine dintr-un scanner / poză / fax.
Scriptul `extract_pdf.py` calculează câte caractere a găsit per pagină și, dacă
media e foarte mică, afișează avertismentul de PDF scanat.

## 2. Ce ai nevoie

OCR are **două** componente: binare de sistem (NU se instalează cu pip) + pachete Python.

**Binare de sistem:**
- **Tesseract OCR** — motorul de recunoaștere. Instalează și pachetul de limbă
  **română (`ron`)** pe lângă engleză.
- **Poppler** — necesar pentru a converti paginile PDF în imagini (`pdf2image`).

Instalare binare:
```bash
# Ubuntu / Debian (inclusiv WSL)
sudo apt-get update
sudo apt-get install -y tesseract-ocr tesseract-ocr-ron poppler-utils

# macOS (Homebrew)
brew install tesseract tesseract-lang poppler

# Windows: descarcă instalerele Tesseract (UB Mannheim) și Poppler,
# apoi adaugă-le în PATH. (Sau rulează în WSL cu comenzile de mai sus.)
```

**Pachete Python:**
```bash
pip install ocrmypdf            # varianta A (recomandată, cea mai simplă)
# SAU, pentru varianta B:
pip install pdf2image pytesseract pillow
```

## 3. Varianta A — `ocrmypdf` (cel mai simplu)

`ocrmypdf` rulează Tesseract intern și adaugă un **strat de text** peste PDF-ul
scanat, păstrând layout-ul. După rulare, ai un PDF normal din care `extract_pdf.py`
poate scoate textul.

```bash
ocrmypdf -l ron+eng "contract-scanat.pdf" "contract-ocr.pdf"
# apoi rulezi extractorul pe rezultatul cu strat de text:
python scripts/extract_pdf.py "contract-ocr.pdf"
```
- `-l ron+eng` → recunoaște română + engleză (contracte adesea mixte).
- Dacă PDF-ul are deja text pe unele pagini, adaugă `--skip-text` ca să nu dea eroare.

## 4. Varianta B — `pdf2image` + `pytesseract` (control fin)

Convertești fiecare pagină în imagine și rulezi Tesseract pe ea. Folosește când
vrei control (preprocesare imagine) sau când nu poți instala `ocrmypdf`.

```python
# pip install pdf2image pytesseract pillow
# necesită Poppler + Tesseract (cu limba `ron`) instalate în sistem
from pdf2image import convert_from_path
import pytesseract

pagini = convert_from_path("contract-scanat.pdf", dpi=300)  # 300 dpi = bun pentru OCR
text_total = []
for i, img in enumerate(pagini, start=1):
    text = pytesseract.image_to_string(img, lang="ron+eng")
    text_total.append(f"\n--- Pagina {i} ---\n{text}")

print("".join(text_total))
```

**Crește acuratețea** pe scanuri proaste: convertește imaginea în grayscale,
mărește-o și aplică thresholding (binarizare) înainte de OCR (cu `pillow`/`opencv`).

## 5. Limitări și verificări

- OCR-ul **nu e 100% precis**, mai ales pe **diacritice românești** (ă, â, î, ș, ț),
  scanuri înclinate, fonturi mici sau pete. Pachetul de limbă `ron` ajută mult.
- **Cifrele sunt cele mai riscante**: sume, date, procente, termene. După OCR,
  **verifică manual în PDF** orice valoare numerică pe care te bazezi (preț, penalități, scadențe).
- Dacă OCR-ul iese foarte slab, spune-i utilizatorului clar că documentul e greu
  de citit automat și că textul extras poate conține erori — nu prezenta cifre nesigure ca fiind certe.

---

## Surse (verificate)
- Tutoriale OCR PDF cu pytesseract + pdf2image (ploomber.io, nutrient.io, towardsdatascience.com).
- `ocrmypdf` ca soluție de adăugare strat de text peste scanuri (documentație proiect / ghiduri).
