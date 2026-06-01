---
name: deck-generator
description: >-
  Genereaza slide-uri in Markdown gata de importat in gamma.app, plecand de la o
  tema sau un continut. Output: un fisier .md cu slide-uri separate corect prin
  `---`, o idee per slide, structura coerenta (titlu, problema, solutie, beneficii,
  CTA). Pentru audienta business non-tech care vrea prezentari rapide (pitch, raport,
  training) fara sa faca PowerPoint manual. Se activeaza cand utilizatorul scrie:
  "fa-mi slide-uri", "prezentare", "deck pentru", "slide-uri despre", "un pitch
  pentru", "slide-uri pentru gamma". NU se activeaza pentru: a scrie un articol sau
  eseu lung (nu slide-uri), editare de imagini, generare de fisiere binare PDF/PPTX.
---

# deck-generator — Slide-uri Markdown pentru gamma.app

## Cand se foloseste

Cand utilizatorul vrea sa transforme o tema sau un continut intr-o prezentare
rapida, fara sa deschida PowerPoint. Output-ul e un fisier `.md` pe care il
lipeste sau il importa in **gamma.app**, iar Gamma il transforma in slide-uri
stilizate. Trigger-e tipice: "fa-mi slide-uri despre X", "prezentare pentru Y",
"deck pentru pitch-ul Z", "un raport in slide-uri".

## Ce face

Plecand de la tema/continut, generezi un deck Markdown care:
- are slide-urile separate corect prin `---` (un card per slide in Gamma);
- respecta **o idee per slide** si densitate redusa (titluri scurte, putin text);
- urmeaza o structura de prezentare coerenta (deschidere -> miez -> actiune),
  potrivita scopului: **pitch**, **raport** sau **training**;
- e in romana, cu diacritice complete, ton profesionist si cald.

## Resurse (citeste-le la nevoie)

- `references/format-gamma.md` — sursa de adevar pentru ce importa Gamma: regula
  `---`, ce sintaxa Markdown intelege, densitate, checklist. **Citeste-o mereu**
  inainte sa generezi, ca sa nu inventezi sintaxa.
- `references/structuri-deck.md` — structurile pitch/raport/training, principiile
  (Kawasaki 10/20/30, hook, AIDA) si framework-ul de engagement RLC (implicit, bland).
- `scripts/valideaza_slideuri.py` — validator + scaffolder. Comenzi:
  - `python3 scripts/valideaza_slideuri.py check fisier.md` — verifica separatoare,
    slide-uri prea dense, slide-uri fara titlu, tabele prea mari, numara slide-urile.
  - `python3 scripts/valideaza_slideuri.py scaffold N --out fisier.md` — genereaza
    un schelet gol de N slide-uri.

## Pasi

1. **Identifica tema, scopul si audienta.** Din cererea utilizatorului extrage:
   subiectul, tipul de deck (pitch / raport / training — vezi tabelul din
   `references/structuri-deck.md`) si, daca exista, continutul brut (cifre, idei,
   text). Daca scopul e ambiguu, pune o singura intrebare scurta sau alege PITCH.

2. **Citeste cele doua referinte.** `references/format-gamma.md` (format) si
   `references/structuri-deck.md` (structura + engagement). Alege structura.

3. **Construieste firul narativ.** Mapeaza continutul pe structura aleasa:
   deschidere (titlu + hook) -> miez (problema/solutie sau constatari/concepte)
   -> inchidere (CTA / recomandari / exercitiu). Aplica RLC **implicit** si bland:
   prinde -> conecteaza -> convinge -> cere. Fara FOMO, fara durere exagerata.

4. **Scrie slide-urile.** Fiecare slide:
   - incepe cu `## SLIDE N - TITLU DESCRIPTIV` (optional, pentru claritate);
   - are un titlu real (`#` sau `##`);
   - **o singura idee**, max ~5 bullet-uri si ~50 de cuvinte;
   - se termina cu `---` (linie goala inainte si dupa).
   Foloseste DOAR sintaxa Markdown din tabelul din `references/format-gamma.md`.
   Diacritice complete. Nu inventa cifre/exemple care nu sunt in continutul primit.

5. **Lungime.** Tinteste 8-12 slide-uri (Kawasaki 10/20/30). Un deck simplu poate
   avea 6; unul complex 12-15. Daca o sectiune are 2 idei, fa 2 slide-uri.

6. **Valideaza.** Scrie fisierul `.md` si ruleaza
   `python3 scripts/valideaza_slideuri.py check <fisier>.md`. Daca raporteaza
   slide-uri prea dense, fara titlu sau separator lipsa, **corecteaza si reruleaza**
   pana da OK.

7. **Livreaza.** Afiseaza continutul deck-ului in terminal (pentru copy-paste direct
   in Gamma) si spune utilizatorului cum sa il importe: in gamma.app -> `New` ->
   `Paste in text` -> format `Presentation` -> lipeste tot. Mentioneaza calea
   fisierului `.md`.

## Exemple

### Exemplu 1 — input -> output (PITCH)
**Input:** "Fa-mi slide-uri pentru un pitch despre o aplicatie care automatizeaza
facturarea pentru freelanceri."

**Output (extras):**
```markdown
# Slide-uri: FacturaZen

---

## SLIDE 1 - TITLU
### Facturare fara batai de cap
# FacturaZen
## Aplicatia care iti face facturile in 30 de secunde

---

## SLIDE 2 - HOOK
# Cate ore pierzi lunar pe facturi?

Pentru un freelancer, facturarea manuala inseamna 3-5 ore in fiecare luna.

**Timp care ar putea fi munca platita.**

---

## SLIDE 3 - PROBLEMA
# Facturarea manuala te costa

- Greseli la TVA si la calcule
- Facturi trimise cu intarziere
- Plati uitate, urmarite greu

**Rezultatul: stres si bani pe care ii incasezi tarziu.**

---

## SLIDE 4 - SOLUTIA
# FacturaZen face totul automat

Introduci o data clientii si serviciile. Aplicatia genereaza, trimite si
urmareste facturile in locul tau.

**O factura corecta, trimisa la timp, fara efort.**

---
```
(continua cu CUM FUNCTIONEAZA, BENEFICII, DOVADA, OFERTA, CTA)

### Exemplu 2 — input -> output (RAPORT)
**Input:** "Slide-uri despre rezultatele campaniei de marketing din Q1: am cheltuit
10.000 euro, am avut 120 de clienti noi, cel mai bun canal a fost Google Ads."

**Output (extras):**
```markdown
# Slide-uri: Rezultate Campanie Marketing Q1

---

## SLIDE 1 - TITLU
### Raport de campanie
# Rezultate Marketing Q1
## Buget, achizitii si recomandari

---

## SLIDE 2 - SUMAR EXECUTIV
# Q1: 120 de clienti noi, 83 euro/client

Cu un buget de 10.000 euro am adus 120 de clienti noi. Google Ads a fost cel mai
eficient canal.

**Recomandare: realocam bugetul catre Google Ads in Q2.**

---

## SLIDE 3 - CONSTATARE: COST PER CLIENT
# 83 euro per client nou

10.000 euro buget / 120 clienti = 83 euro cost de achizitie.

**Sub media pietei pentru serviciul nostru.**

---
```
(continua cu celelalte constatari, CE INSEAMNA, RECOMANDARI, URMATORII PASI)

### Exemplu 3 — input -> output (TRAINING)
**Input:** "Slide-uri despre cum sa scrii un email de vanzare, pentru un training
intern de 20 de minute."

**Output (extras):**
```markdown
# Slide-uri: Cum scrii un email de vanzare

---

## SLIDE 1 - TITLU
### Training intern
# Cum scrii un email de vanzare
## In 20 de minute

---

## SLIDE 2 - DE CE CONTEAZA
# Un email bun aduce raspunsuri

Majoritatea emailurilor de vanzare sunt ignorate. Diferenta o face structura.

**Astazi invatam structura care aduce raspunsuri.**

---

## SLIDE 3 - CE VEI INVATA
### La final vei putea
1. **Sa scrii un subiect** care e deschis
2. **Sa structurezi mesajul** in 3 parti
3. **Sa termini cu un CTA** clar

---
```
(continua cu CONTINUT per concept, RECAP, EXERCITIU, INCHIDERE)

## NU se activeaza cand

- Utilizatorul vrea un **articol, eseu, postare de blog sau text lung** — acela e
  text continuu, nu slide-uri.
- Cere **editare/generare de imagini** sau grafica.
- Cere un fisier **binar gata facut: PDF, PPTX, .key** — noi generam doar Markdown
  pentru import in Gamma (Gamma exporta apoi in PDF/PPTX, nu noi).
- Cere modificari la o prezentare existenta in alt format (de ex. un .pptx incarcat).

## Best practices

- **O idee per slide.** Daca un slide are doua mesaje, fa doua slide-uri.
- **Densitate redusa.** Max ~5 bullet-uri si ~50 de cuvinte per slide; titluri scurte.
- **Separator `---` mereu**, cu linie goala inainte si dupa.
- **Deschidere puternica:** hook in slide 2 (intrebare / cifra / poveste scurta).
- **Inchidere cu actiune:** orice deck se termina cu un CTA sau urmatorul pas clar.
- **Beneficii, nu features** (pentru pitch): ce castiga audienta, concret.
- **Concluzia in fata** (pentru raport): sumar executiv inainte de date.
- **Nu inventa** cifre, citate sau studii de caz care nu sunt in continutul primit.
- **Ton profesionist, cald, fara FOMO** de funnel. Diacritice complete.
- **Valideaza mereu** cu `scripts/valideaza_slideuri.py check` inainte de a livra.
