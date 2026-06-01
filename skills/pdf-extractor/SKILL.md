---
name: pdf-extractor
description: >-
  Extrage din PDF-uri lungi (contracte, oferte, termeni și condiții) clauzele
  importante, obligațiile fiecărei părți, termenele/deadline-urile și flag-urile
  de risc (auto-reînnoire tacită, penalități, reziliere unilaterală, jurisdicție,
  limitare de răspundere, exclusivitate, confidențialitate, indexare preț).
  Se activează când utilizatorul spune „extrage din PDF", „ce clauze are",
  „ce obligații am", „analizează contractul", „ce riscuri are documentul",
  „ce semnez", „ce trebuie să fac din acest document" — sau cere un rezumat al
  unui PDF de tip contract/ofertă/T&C. Se compune cu skill-ul `summarizer`
  (rezumat + acțiuni + deadline-uri + flag-uri risc). NU se activează pentru:
  PDF-uri scurte triviale, generarea/crearea unui PDF nou, editarea/semnarea
  unui PDF, completarea de formulare. NU oferă consultanță juridică — semnalează
  clauzele și riscurile ca să le vezi rapid și recomandă verificarea cu un avocat.
---

# pdf-extractor — Clauze, obligații, termene și flag-uri de risc din PDF

Ajută un utilizator de business (non-tech) să vadă rapid, dintr-un PDF lung
(contract, ofertă, termeni și condiții), ce contează: ce semnează, ce trebuie
să facă, până când și unde sunt capcanele. **Nu este consultanță juridică** —
scoate la suprafață clauzele și riscurile, dar pentru decizii importante
utilizatorul trebuie să consulte un avocat.

## Când se folosește

Se activează automat când descrierea (frontmatter) matchează cererea. Tipic:
- „Extrage din PDF-ul ăsta clauzele importante."
- „Ce obligații am din contractul de furnizor?"
- „Analizează contractul SaaS și spune-mi ce riscuri are."
- „Ce trebuie să fac din ~/Downloads/contract-vendor.pdf? Până când?"
- „Rezumă termenii și condițiile" (împreună cu `summarizer`).

## Ce face

Pe scurt, transformă un PDF lung într-o fișă structurată:
1. **Text** — extrage textul real din PDF (vezi `scripts/`).
2. **Clauze** — identifică clauzele importante (obiect, preț, durată, reziliere,
   penalități, garanție, confidențialitate, IP, forță majoră, jurisdicție etc.).
3. **Obligații per parte** — cine ce trebuie să facă (tu vs. cealaltă parte).
4. **Termene/deadline-uri** — date, preavize, ferestre de notificare, scadențe.
5. **Flag-uri de risc** — semnalează capcanele clasice (auto-reînnoire tacită,
   reziliere unilaterală asimetrică, răspundere nelimitată/cap mic, jurisdicție
   străină, exclusivitate, indexare preț fără plafon, penalități disproporționate).

## Pași

Copiază acest checklist și bifează pe măsură ce avansezi:

```
Progres analiză PDF:
- [ ] Pas 1: Extrage textul din PDF (script). Verifică dacă e PDF scanat (OCR).
- [ ] Pas 2: Identifică tipul de document și părțile.
- [ ] Pas 3: Mapează clauzele importante (folosește CHECKLIST-ul de referință).
- [ ] Pas 4: Extrage obligațiile per parte + termenele/deadline-urile.
- [ ] Pas 5: Marchează flag-urile de risc (cu severitate ÎNALT/MEDIU/SCĂZUT).
- [ ] Pas 6: Scrie fișa structurată + disclaimer „nu e consult juridic".
```

**Pas 1 — Extrage textul.** Rulează scriptul de extragere și flagging:
```bash
pip install pdfplumber
python scripts/extract_pdf.py "/cale/catre/contract.pdf"
```
Scriptul scoate textul per pagină și o listă de potriviri pentru cuvinte-cheie
de risc (RO + EN). Dacă scriptul raportează **„PDF probabil scanat / fără strat
de text"**, înseamnă că paginile sunt imagini — vezi secțiunea „PDF scanat" de
mai jos înainte de a continua.

**Pas 2 — Tip document + părți.** Stabilește ce e (contract de prestări servicii /
furnizare / chirie / SaaS / NDA / ofertă / T&C) și cine sunt părțile (denumire,
CUI, rol: tu ești Beneficiar sau Prestator?). Rolul schimbă cine suportă fiecare risc.

**Pas 3 — Clauze importante.** Parcurge documentul clauză cu clauză. Pentru ce
să cauți și de ce contează fiecare, **citește `references/checklist-clauze-risc.md`**
(taxonomie completă de clauze + red-flags pentru contracte din România).

**Pas 4 — Obligații + termene.** Pentru fiecare parte, listează obligațiile
concrete (ce trebuie făcut). Separat, extrage toate termenele: scadențe de plată,
preavize de reziliere, ferestre de notificare pentru NON-reînnoire, durată,
termene de livrare/garanție. Marchează deadline-urile care vin curând.

**Pas 5 — Flag-uri de risc.** Pentru fiecare capcană găsită, notează severitatea:
- **ÎNALT** — clauze potențial abuzive (Legea 193/2000), reziliere unilaterală
  doar în favoarea celeilalte părți, răspundere nelimitată / fără cap, jurisdicție
  străină fără motiv, exclusivitate strânsă, auto-reînnoire cu preaviz prea scurt.
- **MEDIU** — penalități de întârziere mari, indexare preț fără plafon, garanție
  vagă, confidențialitate fără durată, forță majoră prea largă/îngustă.
- **SCĂZUT** — formulări neclare, anexe menționate dar lipsă, termene de notificare nespecificate.

**Pas 6 — Fișa finală.** Folosește formatul de output de mai jos. Termină
**întotdeauna** cu disclaimer-ul.

## Format output

```markdown
# Analiză document: [tip + părți]

## TL;DR
[2-3 fraze: ce e, ce te obligă esențial, top risc.]

## Obligațiile tale
- [obligație] — termen: [data/preaviz]

## Obligațiile celeilalte părți
- [obligație] — termen: [data/preaviz]

## Termene & deadline-uri
| Ce | Când | Acțiune necesară |
|----|------|------------------|
| Scadență plată | [data] | [ce faci] |
| Preaviz NON-reînnoire | [cu X zile înainte de termen] | trimite notificare |

## Flag-uri de risc
| Risc | Severitate | Clauza | De ce contează |
|------|-----------|--------|----------------|
| Auto-reînnoire tacită | ÎNALT | art. X | preaviz de doar Y zile pentru a opri reînnoirea |

## Ce să clarifici cu cealaltă parte / avocatul
- [punct concret]

---
*Aceasta NU este consultanță juridică. Rolul analizei este să te ajute să vezi
rapid clauzele și riscurile. Pentru decizii importante (semnare, negociere,
litigiu), consultă un avocat autorizat.*
```

## PDF scanat (fără strat de text)

Multe contracte primite prin email sunt **scanate** (pagini-imagine, fără text
selectabil). Scriptul detectează asta automat (text aproape gol pe pagini). În acest caz:
- Este nevoie de **OCR** (recunoaștere optică a caracterelor). Soluția standard:
  `pdf2image` (convertește paginile în imagini) + `pytesseract` (Tesseract OCR),
  sau direct `ocrmypdf` care adaugă un strat de text peste PDF-ul scanat.
- OCR-ul necesită binare de sistem: **Tesseract** (cu pachetul de limbă `ron`
  pentru română) și **Poppler**. Acestea NU se instalează cu `pip`.
- Pentru detalii și comenzile de instalare/rulare, **citește
  `references/ocr-pdf-scanat.md`**.
- OCR-ul nu este 100% precis pe diacritice/scanuri proaste — tratează cifrele
  (sume, date, procente) cu prudență și verifică-le în PDF.

## NU se activează când

- PDF scurt și trivial (1-2 paragrafe fără clauze) — răspunde direct, fără skill.
- Cerere de **a crea/genera** un PDF nou (folosește alt skill/instrument).
- Cerere de **a edita / semna / completa formulare** într-un PDF.
- Fișierul nu e contract/ofertă/T&C și nu se cer clauze/obligații/riscuri.

## Best practices

- **Citează clauza.** Fiecare flag de risc trimite la articolul/secțiunea din PDF,
  ca utilizatorul să verifice rapid în original.
- **Nu inventa.** Dacă nu găsești o clauză (ex. nu există plafon de răspundere),
  spune „lipsește" — absența unei clauze e ea însăși un risc, dar nu inventa text.
- **Atenție la rol.** Același contract are riscuri diferite pentru Beneficiar vs.
  Prestator. Confirmă rolul utilizatorului.
- **Cifre cu grijă.** Verifică sume, date și procente direct în PDF, mai ales pe scanuri OCR.
- **Limbaj clar, non-tech.** Explică pe înțelesul unui om de business, nu în jargon juridic.
- **Compune cu `summarizer`** când utilizatorul cere și un rezumat general.
- **Disclaimer obligatoriu.** Nu omite niciodată mențiunea „nu e consultanță juridică".
