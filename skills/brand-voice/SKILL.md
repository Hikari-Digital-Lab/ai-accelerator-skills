---
name: brand-voice
description: >-
  Extrage „vocea de brand" (fișă personaj reutilizabilă) din 3-5 sample-uri de
  scriere ale utilizatorului (postări, e-mailuri, articole, newslettere): ton pe
  dimensiuni (formal↔casual, serios↔amuzant, respectuos↔iconoclast,
  entuziast↔neutru), vocabular tipic, ritm și lungime de frază, formule de
  salut/închidere, expresii-semnătură, plus ce să FACĂ și ce să EVITE. Fișa
  rezultată poate fi folosită de alte skills (e-mail, postări) ca să scrie „ca
  utilizatorul". Se activează când utilizatorul spune „extrage stilul meu",
  „fă-mi o fișă personaj", „vocea mea de brand", „scrie ca mine", „analizează-mi
  stilul", „învață cum scriu" — și furnizează (sau e dispus să furnizeze) texte
  scrise de el. NU se activează când: se cere scrierea de conținut FĂRĂ
  sample-uri furnizate (nu există text-sursă de analizat); se cere analiza vocii
  ALTcuiva fără a avea texte ale acelei persoane; se cere doar un rezumat sau o
  corectură de text. Produce un singur document — fișa de voce — nu rescrie textele.
---

# brand-voice — Fișă de voce de brand din sample-urile tale

Transformă 3-5 texte scrise de utilizator într-o **fișă de voce de brand**: un
document reutilizabil care descrie cum scrie persoana (ton, vocabular, ritm,
formule, ce face / ce evită), astfel încât alte skills (sau Claude) să poată
scrie ulterior „ca el/ea". Audiență țintă: oameni de business non-tech care vor
să-și păstreze vocea proprie când deleagă scrisul către AI.

## Când se folosește

Se activează automat când descrierea (frontmatter) matchează cererea. Tipic:
- „Extrage-mi stilul din postările astea." (cu texte atașate/lipite)
- „Fă-mi o fișă personaj din e-mailurile mele."
- „Analizează cum scriu și spune-mi vocea mea de brand."
- „Vreau ca Claude să scrie ca mine — uite 4 articole."

**Cere ÎNTOTDEAUNA sample-uri reale.** Fără texte scrise de utilizator nu există
ce analiza — vezi „NU se activează când".

## Ce face

Pe scurt, din sample-uri → fișă de voce:
1. **Adună sample-uri** — 3-5 texte reale (postări, e-mailuri, articole). Acceptă
   2 dacă atât are, dar spune că fișa va fi mai puțin sigură; ideal 3-5.
2. **Măsoară obiectiv** — rulează scriptul de analiză: lungime frază, vocabular
   frecvent, lizibilitate, densitate emoji/exclamări, formule de început/sfârșit.
3. **Citește calitativ** — pe lângă cifre, citește textele pentru ton, atitudine,
   ticuri, ce face și ce EVITĂ autorul.
4. **Poziționează tonul** — pe cele 4 dimensiuni (formal↔casual, serios↔amuzant,
   respectuos↔iconoclast, entuziast↔neutru) + axe suplimentare dacă ies clar.
5. **Produce fișa** — un document structurat (vezi template), cu un „briefing"
   acționabil pe care alte skills îl pot folosi ca să scrie în vocea utilizatorului.

## Pași

Copiază acest checklist și bifează pe măsură ce avansezi:

```
Progres fișă de voce:
- [ ] Pas 1: Strânge 3-5 sample-uri reale. Confirmă registrul (e-mail? postări?).
- [ ] Pas 2: Rulează scriptul de analiză pe sample-uri → metrici obiective.
- [ ] Pas 3: Citește textele calitativ (ton, ticuri, ce face / ce evită).
- [ ] Pas 4: Poziționează pe cele 4 dimensiuni de ton (+ axe suplimentare).
- [ ] Pas 5: Scrie fișa în template, cu EXEMPLE din textul real + secțiunea „CE EVITĂ".
- [ ] Pas 6: Adaugă briefing-ul acționabil pentru alte skills. Marchează încrederea.
```

**Pas 1 — Strânge sample-urile.** Cere utilizatorului 3-5 texte scrise de el,
de același tip (un singur registru per fișă). Salvează fiecare ca fișier `.txt`
sau `.md` (sau lasă-le lipite în conversație). Dacă amestecă registre vizibil
diferite (e-mail oficial + postare glumeață), propune fișe separate.

**Pas 2 — Măsoară obiectiv.** Rulează scriptul de analiză:
```bash
python scripts/analizor_stil.py sample1.txt sample2.txt sample3.md
# sau, dacă sunt într-un folder:
python scripts/analizor_stil.py /cale/catre/folder_sampleuri/
```
Scriptul (doar bibliotecă standard Python, fără instalări) scoate: lungimea medie
și variația frazelor, lizibilitate aproximativă (Flesch adaptat RO), top cuvinte
de conținut (fără cuvinte de legătură) și bigrame, densitatea de emoji/exclamări/
întrebări și formulele de început/sfârșit ale fiecărui text. Folosește `--json`
dacă vrei rezultatul structurat. **Cifrele sunt punct de plecare, nu verdict.**

**Pas 3 — Citește calitativ.** Cifrele nu prind tonul. Citește textele și notează:
atitudinea (caldă? sfidătoare? sobră?), ticurile verbale, cum deschide și închide,
cum livrează o veste/critică, și — esențial — **ce EVITĂ** (cuvinte, formule, ton
de care se ferește, plus tipare de AI care NU sună a el: „Este important de
menționat", „În peisajul actual", „De asemenea", liste-clișeu).

**Pas 4 — Poziționează tonul.** Pe fiecare dimensiune, dă un scor 1-5 și
justifică-l cu un citat din textul real. **Citește `references/fisa-voce-template.md`**
— conține framework-ul complet al dimensiunilor (cele 4 axe Nielsen Norman + axe
suplimentare) și cum poziționezi pe fiecare.

**Pas 5 — Scrie fișa.** Folosește TEMPLATE-ul din `references/fisa-voce-template.md`.
Reguli: fiecare afirmație despre stil are un **exemplu din textul utilizatorului**;
specificul învinge generalul („fraze de 8-12 cuvinte" > „stil concis"); secțiunea
**„CE EVITĂ" e obligatorie**. Nu inventa exemple care nu există în sample-uri.

**Pas 6 — Briefing + încredere.** Termină cu un „briefing pentru alte skills":
3-5 instrucțiuni acționabile, suficiente ca un skill de e-mail/postări să scrie
în vocea utilizatorului fără să citească toată fișa. Dacă ai avut puține sample-uri
(1-2) sau scurte, marchează ce e confirmat vs. ipoteză.

## Exemple (input → output)

### Exemplu 1 — Postări scurte, energice
**Input (3 postări, fragment):**
> „Salut! Azi un truc simplu. Nu e magie. E disciplină. Tu cum faci? Spune-mi! 🚀"

**Output (extras din fișă):**
```
Formal↔Casual: 5 (tu, „Salut!", exclamații). Entuziast↔Neutru: 4.
Ritm: fraze foarte scurte (3-7 cuvinte), tip „bombă". Un emoji la final.
Formule: deschide cu „Salut!", închide cu întrebare + apel („Spune-mi!").
CE EVITĂ: jargon corporate, fraze lungi, mai mult de 1 emoji.
Briefing: scrie scurt, la persoana a II-a, cârlig în prima frază, apel direct la final.
```

### Exemplu 2 — E-mailuri de echipă, sobre dar calde
**Input (3 e-mailuri, fragment):**
> „Bună, echipă. Vă scriu să clarific obiectivele. Propunerea mea: sync de 15 min, luni. Ce părere aveți? Mulțumesc."

**Output (extras din fișă):**
```
Formal↔Casual: 3 (echilibrat). Concis↔Detaliat: 2 (la obiect). Cald↔Distant: 2 (cald).
Ritm: fraze medii, propuneri marcate cu „Propunerea mea:". Diacritice complete.
Formule: deschide cu „Bună, echipă", cere feedback cu „Ce părere aveți?", închide cu „Mulțumesc".
CE EVITĂ: PowerPoint-uri, vorbărie, ton autoritar.
Briefing: deschide cu salut cald, formulează 1 propunere clară, cere explicit feedback cu termen.
```

### Exemplu 3 — Lipsesc sample-urile
**Input:** „Scrie ca un copywriter de top, energic și convingător."
**Output:** Skill-ul NU produce o fișă inventată. Răspuns: „Pentru o fișă de
voce am nevoie de 3-5 texte scrise CHIAR DE TINE (postări, e-mailuri, articole).
Trimite-mi câteva și extrag stilul tău real." (vezi „NU se activează când").

## NU se activează când

- **Nu există sample-uri.** Se cere scrierea/„stilul" fără texte furnizate de
  utilizator — nu inventa o voce; cere mai întâi 3-5 texte reale.
- **Vocea altcuiva fără text-sursă.** „Scrie ca [persoană publică]" fără a avea
  texte ale acelei persoane — nu există ce analiza.
- **Doar rezumat / corectură.** Se cere un TL;DR sau o corectare de text
  (folosește `summarizer` sau editare directă), nu o fișă de voce.
- **Generare de conținut direct.** Se cere un e-mail/o postare concretă acum —
  scrie-l direct (eventual aplicând o fișă existentă), nu reface analiza de voce.

## Best practices

- **Sample-uri reale, nu ideale.** Captează cum scrie EFECTIV utilizatorul, nu
  cum ar vrea să scrie. Dacă vrea o voce-țintă diferită, spune-i clar ce vede în
  texte vs. ce aspiră, și întreabă care variantă o documentați.
- **Un registru per fișă.** E-mailul formal și postarea glumeață sunt voci
  diferite — nu face media. Fișe separate sau secțiuni clar marcate.
- **Specific, cu dovadă.** Orice rând din fișă are un exemplu din textul real.
  Descrierile generice („ton prietenos") se aplică oricui — sunt inutile.
- **„CE EVITĂ" e obligatoriu.** Anti-pattern-urile (ce nu face + tipare de AI de
  suprimat) sunt la fel de definitorii ca ce face. Fără ele, fișa e pe jumătate.
- **Nu inventa.** Dacă o trăsătură nu reiese din sample-uri, marcheaz-o ca ipoteză
  sau las-o pe dinafară. Preferă golul în locul inventatului.
- **Diacritice = preferință de stil.** Dacă utilizatorul scrie fără diacritice,
  notează asta și păstreaz-o; nu o „corecta" în fișă.
- **Compune cu alte skills.** Fișa e gândită să alimenteze skills de e-mail /
  postări — fă briefing-ul acționabil, ca să poată scrie „ca el" fără fișa întreagă.
- **Document viu.** Pe măsură ce apar sample-uri noi sau feedback, versionează
  fișa (v1, v2) și rafineaz-o.
