---
name: plan-helper
description: >-
  Transformă o cerere de business într-un plan clar, numerotat, pas cu pas, ÎNAINTE de a executa ceva. Pune întrebări structurate (formula 95%) cu AskUserQuestion ca să înțeleagă cerințele, sparge task-urile complexe (heuristica „cuvântul ȘI = 2 procese"), apoi livrează un plan pe care îl aprobi înainte de execuție. Recomandă modelul Opus pentru planificare. Se activează când utilizatorul scrie lucruri de tipul: „fă-mi un plan pentru...", „planifică...", „cum abordez...", „ajută-mă să planific", „de unde încep cu...", „vreau să fac X ȘI Y". NU se activează la task-uri triviale dintr-un singur pas (redenumește un fișier, corectează o greșeală) sau când utilizatorul cere clar execuție imediată („fă acum", „doar execută", „nu-mi face plan").
---

# Plan Helper

Ajută oamenii de business (fără background tehnic) să transforme o idee vagă într-un plan concret, pe pași, pe care îl aprobă înainte ca asistentul să facă orice. Forțează gândirea ÎNAINTE de execuție — exact ce previne haosul de tip „fă-mi 5 lucruri" sau „am stat 7 ore pe același lucru".

## Când se folosește

Se activează când utilizatorul cere o planificare, nu o execuție imediată. Exemple de fraze:
- „Fă-mi un plan pentru lansarea newsletter-ului."
- „Planifică o campanie de Black Friday pentru magazinul meu."
- „Cum abordez migrarea clienților pe noul CRM?"
- „Ajută-mă să planific procesul de onboarding pentru angajați noi."
- „Vreau un sistem care citește emailurile ȘI răspunde automat ȘI le arhivează." (conține „ȘI" → semnal puternic de planificare + descompunere)

## Ce face

1. Pune întrebări structurate cu AskUserQuestion pentru a elimina ambiguitatea (formula 95%).
2. Detectează complexitatea ascunsă: aplică heuristica „cuvântul ȘI = 2 procese" și propune spargerea în sub-procese.
3. Livrează un plan numerotat, clar, în limbaj de business, cu o singură frază BLUF la început (ce vei obține la final).
4. Recomandă modelul potrivit: Opus pentru planificare, Sonnet pentru execuție.
5. Așteaptă aprobarea utilizatorului, apoi trece la execuție — pas cu pas, nu tot odată.

## Pași (workflow)

Urmează acești pași în ordine. Bifează-i pe măsură ce avansezi.

```
Progres Plan Helper:
- [ ] Pas 1: Intră în „mod planificare" — anunță că NU execuți încă
- [ ] Pas 2: Pune întrebări cu AskUserQuestion (formula 95%)
- [ ] Pas 3: Aplică heuristica „ȘI = 2 procese" și propune spargerea
- [ ] Pas 4: Scrie planul numerotat (BLUF + pași)
- [ ] Pas 5: Recomandă modelul (Opus pentru plan)
- [ ] Pas 6: Cere aprobarea
- [ ] Pas 7: După aprobare → execută pas cu pas
```

### Pas 1 — Anunță modul planificare

Spune clar, de la început: *„Înainte să fac ceva, hai să clarificăm ce vrei, ca să-ți dau un plan bun. Nu modific/execut nimic până nu aprobi planul."* Asta setează așteptarea corectă și calmează utilizatorul non-tech.

### Pas 2 — Întrebări cu AskUserQuestion (formula 95%)

Folosește tool-ul **AskUserQuestion** ca să pui întrebări cu variante de răspuns. Continuă să întrebi *până ești 95% sigur că înțelegi toate cerințele* — nu ghici, nu „decide tu".

- Maximum 4 întrebări per rundă (limita tool-ului). Pentru task-uri mari, fă mai multe runde.
- Task simplu → 1-2 runde a câte 3-4 întrebări. Task complex → 3+ runde.
- La fiecare opțiune recomandată, pune-o prima și adaugă „(Recomandat)" la final.
- Acoperă cele 6 zone obligatorii: **obiectiv, audiență/beneficiar, scope (ce intră / ce NU intră), constrângeri (timp/buget/tooluri), formatul rezultatului, definiția de „gata"**.
- Pentru întrebări deschise unde variantele nu acoperă tot, lasă utilizatorul să aleagă „Altceva" (text liber).
- Dacă utilizatorul e blocat: *„Sunt non-tech, ajută-mă să-ți răspund corect."* — reformulează întrebarea mai simplu.

Vezi `references/ghid-planificare.md` (secțiunea „Cadrul de elicitare 95%") pentru lista completă de întrebări gata de pus, grupate pe zone.

Pentru a genera rapid o listă de întrebări de clarificare plecând de la obiectivul brut al utilizatorului, rulează:
```bash
python scripts/checklist_clarificare.py "obiectivul utilizatorului aici"
```
Scriptul detectează automat cuvântul „ȘI" și semnalează nevoia de spargere.

### Pas 3 — Heuristica „cuvântul ȘI = 2 procese"

Regula de aur: **dacă în descrierea task-ului apare „ȘI", de obicei poți sparge în 2 (sau mai multe) procese separate.** Pași mai condensați = mai greu să se încurce asistentul.

Exemplu (caz real): *„automatizare care citește rezumatul emailurilor, arhivează ce nu mai trebuie ȘI răspunde personalizat"* = 5 lucruri într-un task = haos. Spargere corectă:
- Proces 1: Citește emailuri + sortează (urgent / normal / spam)
- Proces 2: Arhivează vechile (peste 30 zile, citite)
- Proces 3: Generează drafturi de răspuns doar pentru cele urgente

Fiecare proces = pas separat (ideal, sesiune separată). Propune utilizatorului spargerea: *„Văd că ceri 3 lucruri într-unul. Le sparg în 3 pași separați ca să iasă curat?"*

Vezi `references/ghid-planificare.md` (secțiunea „Descompunerea task-urilor") pentru reguli de spargere (verb + un singur livrabil, task atomic = o sesiune de lucru).

### Pas 4 — Scrie planul

Format obligatoriu:

```markdown
**Rezultat final:** [o singură frază BLUF — ce vei avea concret la final]

**Plan:**
1. [Pas concret, începe cu un verb] — [de ce / ce produce]
2. [Pas concret]
3. ...

**Ce NU intră în acest plan:** [scope-out explicit, ca să nu existe surprize]
**Riscuri / lucruri de confirmat:** [1-3 puncte unde s-ar putea bloca]
```

Reguli: fiecare pas începe cu un verb, e o singură acțiune și se poate „bifa". Dacă planul are peste ~8 pași, propune împărțirea în 2-3 planuri mai mici („3 planuri de 4 pași livrează mai sigur decât 1 plan de 12").

### Pas 5 — Recomandă modelul

Spune-i utilizatorului, scurt: *„Pentru planificare îți recomand modelul **Opus** (cel mai bun la gândire structurată). Pentru execuția propriu-zisă, **Sonnet** e suficient și mai ieftin."* Comutare în Claude Code: `/model opus`.

> Citat memorabil de folosit la nevoie: „Plan mode cu Haiku e ca și cum ai arunca cu piatra în soare. Planul se face cu cel mai inteligent model."

### Pas 6 — Cere aprobarea

Întreabă explicit: *„Îți convine planul? Spune «aprob» și pornesc, sau zi-mi ce modific (ex: «schimbă pasul 3»)."* NU executa până nu primești aprobare. Iterează pe plan de câte ori e nevoie — nimic nu rulează până nu aprobă.

### Pas 7 — Execută

După aprobare, execută pas cu pas, în ordinea din plan. Confirmă finalizarea fiecărui pas major înainte să treci la următorul. Dacă apare ceva neașteptat, oprește-te și întreabă, nu improviza.

## Exemple input → output

**Exemplul 1 — campanie de marketing**

Input: *„Fă-mi un plan pentru o campanie de promovare de Crăciun."*

Output (după runda de întrebări):
```
Rezultat final: Un calendar de campanie pe 4 săptămâni cu mesaje gata de
postat pe Instagram și un email de ofertă, țintit pe clienții existenți.

Plan:
1. Definește oferta de Crăciun (reducere / pachet) și termenul-limită
2. Scrie email-ul de ofertă pentru lista de clienți existenți
3. Creează 8 postări Instagram (2/săptămână) cu texte și idei de vizual
4. Stabilește calendarul exact (ce postezi și când)
5. Pregătește un mesaj de „ultima zi" pentru finalul campaniei

Ce NU intră: design grafic în Photoshop, reclame plătite (buget separat).
Riscuri: ai nevoie de poze cu produsele înainte de pasul 3.
```

**Exemplul 2 — task cu „ȘI" (descompunere)**

Input: *„Vreau ca AI-ul să-mi citească facturile primite pe email ȘI să le treacă într-un tabel ȘI să mă anunțe pe Telegram când vine una mare."*

Output: *„Sunt 3 procese diferite aici — le sparg ca să iasă curat și să nu se încurce:"*
```
Plan (3 procese separate):
1. Proces «citire»: Extrage din emailuri furnizorul, suma și data facturii
2. Proces «registru»: Adaugă fiecare factură ca rând nou într-un fișier CSV local
3. Proces «alertă»: Trimite mesaj pe Telegram dacă suma depășește pragul X lei

Le facem pe rând, în pași separați. Începem cu Procesul 1?
```

**Exemplul 3 — anti-trigger (NU planifică)**

Input: *„Redenumește fișierul raport.txt în raport-final.txt."*

Output: Skill-ul NU se activează. E un singur pas trivial — execută direct, fără întrebări și fără plan.

## NU se activează când (anti-triggers)

- Task trivial, un singur pas evident: redenumire fișier, corectare de greșeală, schimbarea unei valori, o întrebare de tip „ce face asta?".
- Utilizatorul cere clar execuție imediată: „fă acum", „doar execută", „nu-mi mai pune întrebări", „nu vreau plan".
- Utilizatorul a aprobat deja un plan în conversație și acum vrea să continue execuția.
- Cerere pur informativă (răspuns dintr-o frază), nu un proiect cu mai mulți pași.

În aceste cazuri, treci direct la acțiune — planificarea ar fi doar birocrație inutilă.

## Best practices

- **Întrebări înainte de plan, plan înainte de execuție.** Niciodată invers.
- **Nu ghici.** Răspunsurile la AskUserQuestion economisesc 3-5 cicluri de refacere. Mai bine 5 întrebări acum decât 5 reparații mai târziu.
- **BLUF.** Prima frază spune ce obține utilizatorul, nu despre ce e planul.
- **Limbaj de business, zero jargon.** „Fișier CSV = un tabel simplu, ca în Excel." Explică termenii tehnici în paranteză.
- **Pași atomici.** Un pas = un verb = o acțiune care se poate bifa. Dacă un pas nu încape într-o singură sesiune de lucru, sparge-l.
- **Scope-out explicit.** Spune mereu ce NU intră în plan — previne nemulțumirile.
- **Recomandă Opus pentru plan**, Sonnet pentru execuție. Nu Opus pentru tot (cost).
- **Iterează pe plan, nu pe cod prost.** Un plan greșit din temelii se rescrie, nu se peticește.
