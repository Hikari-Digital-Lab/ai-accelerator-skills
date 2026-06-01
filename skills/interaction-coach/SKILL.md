---
name: interaction-coach
description: >-
  Analizează istoricul LOCAL al conversațiilor utilizatorului cu Claude Code și oferă coaching personalizat despre cum să-l folosească mai bine: cum își scrie prompturile, unde pierde context și credit, ce ar putea automatiza, când să folosească plan mode sau alt model. Citește fișierele de sesiune `.jsonl` din `~/.claude/projects/`, calculează tipare (lungimea prompturilor, frecvența `/clear`, modelele folosite, sesiuni prea lungi, consum de tokeni) și transformă cifrele în recomandări concrete. Totul rulează LOCAL — nimic nu pleacă de pe calculator. Se activează când utilizatorul cere lucruri de tipul: „analizează cum folosesc Claude Code", „cum pot folosi mai bine Claude", „dă-mi feedback pe stilul meu de prompting", „unde pierd credit / context", „cum economisesc credite". NU se activează pentru analiză de COD (structura unui proiect) sau pentru debugging-ul unei aplicații — acolo e vorba de cod, nu de stilul de interacțiune.
---

# Interaction Coach

Antrenor personal pentru felul în care vorbești cu Claude Code. Se uită la
istoricul TĂU de conversații (salvat local pe calculator), găsește tiparele —
prompturi vagi, context aglomerat, credit irosit, model greșit pe task — și îți
dă sfaturi concrete, personalizate, ca să obții rezultate mai bune cu mai puțin
credit. Coaching pe datele tale reale, nu sfaturi generice.

## Când se folosește

Se activează când utilizatorul vrea feedback despre CUM folosește Claude Code,
nu despre cod. Exemple de fraze:
- „Analizează cum folosesc Claude Code."
- „Cum pot folosi mai bine Claude / Claude Code?"
- „Dă-mi feedback pe stilul meu de prompting."
- „Unde pierd credit / context?"
- „Cum să-mi economisesc creditele?"
- „De ce termin creditele așa repede?"
- „Ce aș putea automatiza din ce fac repetat?"

## Privacy (citește utilizatorului de la început)

Spune clar, înainte de orice: **analiza rulează 100% LOCAL.** Skill-ul DOAR
CITEȘTE fișierele de istoric de pe calculatorul utilizatorului
(`~/.claude/projects/`). NU trimite nimic în afară — fără rețea, fără upload,
fără telemetrie. Nu modifică și nu șterge nimic. Implicit afișează doar
statistici agregate; conținutul prompturilor nu se arată decât dacă utilizatorul
cere explicit fragmente ilustrative.

## Ce face

1. **Citește istoricul sesiunilor** — fișierele `.jsonl` din
   `~/.claude/projects/<cale-proiect-codificată>/`, unde Claude Code salvează
   local fiecare conversație (un obiect JSON per linie).
2. **Calculează tipare** — rulează `scripts/analizeaza_sesiuni.py`: număr de
   sesiuni și mesaje, lungimea medie a prompturilor tastate, prompturi prea
   scurte/vagi vs. prea lungi, frecvența `/clear` și a altor slash-commands,
   modelele folosite (Haiku/Sonnet/Opus) și proporția lor, sesiuni foarte lungi,
   estimare de consum de tokeni (inclusiv cât trece prin cache).
3. **Dă recomandări** — traduce cifrele în 3-5 sfaturi concrete, prioritizate, în
   limbaj de business, fiecare cu un exemplu „înainte → după". Laudă întâi ce
   face bine, apoi corectează.

## Pași (workflow)

Urmează acești pași în ordine. Bifează-i pe măsură ce avansezi.

```
Progres Interaction Coach:
- [ ] Pas 1: Anunță privacy (rulează local) + întreabă scope (tot / proiect curent)
- [ ] Pas 2: Rulează scriptul de analiză pe istoric
- [ ] Pas 3: Citește ghidul de prompting (references/ghid-prompting-bun.md)
- [ ] Pas 4: Tradu observațiile în 3-5 recomandări prioritizate
- [ ] Pas 5: Dă fiecare recomandare cu exemplu „înainte → după"
- [ ] Pas 6: Oferă un singur pas următor concret
```

### Pas 1 — Privacy + scope

Spune utilizatorului că analiza rulează local și nu pleacă nimic. Apoi întreabă
ce vrea analizat:
- **Tot istoricul** (toate proiectele) → rulează scriptul fără argumente.
- **Doar proiectul curent** → rulează cu `--proiect-curent`.

### Pas 2 — Rulează scriptul de analiză

```bash
# Tot istoricul:
python3 scripts/analizeaza_sesiuni.py

# Doar proiectul din directorul curent:
python3 scripts/analizeaza_sesiuni.py --proiect-curent

# Cu fragmente scurte ilustrative (doar dacă utilizatorul vrea exemple concrete):
python3 scripts/analizeaza_sesiuni.py --exemple

# Ieșire JSON (pentru prelucrare programatică):
python3 scripts/analizeaza_sesiuni.py --json
```

Scriptul rulează doar pe biblioteca standard Python 3 (fără pachete externe) și
tratează grațios cazul „nu există istoric" (folder gol sau inexistent). Dacă nu
găsește fișiere, spune-i utilizatorului unde se uită (`~/.claude/projects/`) și
oferă opțiunea `--root <cale>` dacă istoricul e altundeva.

### Pas 3 — Citește ghidul de prompting

Citește `references/ghid-prompting-bun.md`. Acolo sunt formulele și regulile cu
care construiești recomandările: formula 95% (AskUserQuestion), plan mode,
heuristica „ȘI = 2 procese", selecția de model, strategia `/clear`, prompt
caching, checklist-ul de igienă context/cost și tabelul „observație → recomandare".

### Pas 4 — Tradu observațiile în recomandări

Ia secțiunea „OBSERVAȚII" din ieșirea scriptului și transform-o în 3-5
recomandări prioritizate (cele cu impact mare de cost/timp întâi). Nu copleși cu
zece sfaturi. Folosește tabelul „observație → recomandare" din ghid.

### Pas 5 — Recomandări cu exemplu „înainte → după"

Fiecare recomandare = ce ai observat + ce să facă diferit + de ce câștigă, plus
un exemplu de prompt „înainte → după". Coaching, nu critică: laudă întâi ce merge.

### Pas 6 — Un singur pas următor

Încheie cu UN singur lucru de făcut acum (ex. „de azi, `/clear` la fiecare task
nou"). Un obicei adoptat bate zece sfaturi uitate.

## Exemple input → output

**Exemplul 1 — prompturi prea lungi și vagi**

Input: *„Analizează cum folosesc Claude Code."*

Scriptul raportează: lungime medie 2040 car., 30% prompturi peste 1500 car.,
niciun `/clear`, 110 sesiuni lungi.

Output (coaching):
```
Bun de început: scrii prompturi bogate în context — asta ajută.
Dar 30% sunt pereți de text cu mai multe cereri într-unul, și nu folosești /clear.

Recomandări (prioritizate):
1. Sparge prompturile pe „ȘI". Ex.:
   ÎNAINTE: „citește emailurile ȘI fă-mi un rezumat ȘI răspunde la cele urgente"
   DUPĂ:    3 pași separați, fiecare sesiune cu /clear între ele.
2. Folosește plan mode (Shift+Tab) + formula 95% (AskUserQuestion) la task-urile
   mari — vei avea mai puține corecturi.
3. /clear la fiecare task nou: 110 sesiuni lungi = context aglomerat = credit ars.

Pas următor: de azi, /clear când treci la un task fără legătură.
```

**Exemplul 2 — model greșit pe task**

Input: *„Unde pierd credit?"* (după rulare cu `--proiect-curent`)

Scriptul raportează: Haiku 60% din răspunsuri, multe sesiuni lungi, zero `/cost`.

Output (coaching):
```
Folosești mult Haiku (60%) — economic, dar Haiku „nu știe decât basic".

Recomandări:
1. Pentru plan mode și debug greu, treci pe Opus: „Plan mode cu Haiku e ca și
   cum ai arunca cu piatra în soare." Comutare: /model opus.
2. Pentru execuția de rutină, Sonnet (default) e suficient și mai ieftin ca Opus.
3. Verifică /cost periodic — acum „zbori orb" pe consum.

Pas următor: înainte de un task complex, /model opus; după plan, /model sonnet.
```

**Exemplul 3 — anti-trigger (NU se activează)**

Input: *„Analizează structura proiectului meu Next.js și spune-mi unde e bug-ul."*

Output: Skill-ul NU se activează. E analiză de COD / debugging de aplicație, nu
feedback pe stilul de interacțiune cu Claude Code.

## NU se activează când (anti-triggers)

- **Analiză de COD**, nu de interacțiune: „explică-mi codebase-ul", „mapează
  componentele", „ce face fișierul X". (Acolo e potrivit un skill de tip
  analyze-codebase.)
- **Debugging de aplicație**: „de ce crapă build-ul", „găsește bug-ul", „rezolvă
  eroarea". Asta e despre cod, nu despre cum vorbești cu asistentul.
- Cereri generice de prompt engineering fără legătură cu istoricul propriu
  (acolo răspunzi direct, nu rulezi analiza).

## Best practices

- **Privacy întâi.** Spune din prima că totul rulează local și nu pleacă nimic.
  Pentru un public non-tech, asta e esențial pentru încredere.
- **Date reale, nu generic.** Recomandările se sprijină pe cifrele din istoricul
  utilizatorului. Citează observația concretă („30% din prompturi peste 1500 car.").
- **Laudă întâi, corectează apoi.** Coaching, nu critică. Întărește obiceiurile bune.
- **Maxim 3-5 recomandări**, prioritizate după impact (cost/timp). Nu copleși.
- **Mereu un exemplu „înainte → după".** Mai clar decât o explicație abstractă.
- **Limbaj de business, zero jargon.** Explică termenii tehnici în paranteză.
- **Un singur pas următor** la final — un obicei adoptat bate zece sfaturi uitate.
- **Nu inventa.** Dacă nu există istoric, spune-o; nu fabrica statistici.

## Resurse

- `scripts/analizeaza_sesiuni.py` — analizatorul local de istoric (`.jsonl`).
  Rulează-l pentru cifre; tratează grațios lipsa istoricului. Vezi docstring-ul
  pentru toate flag-urile (`--proiect-curent`, `--root`, `--exemple`, `--json`).
- `references/ghid-prompting-bun.md` — formulele și regulile de coaching (95%,
  plan mode, „ȘI = 2 procese", selecție de model, `/clear`, prompt caching,
  checklist igienă context/cost, tabel „observație → recomandare"). Citește-l
  înainte de a formula recomandările.
