# Ghid de prompting bun pentru Claude Code (RO, business non-tech)

Acest fișier e baza de cunoștințe a skill-ului `interaction-coach`. Conține
formulele, regulile și checklist-urile pe care le folosești când transformi
observațiile din analiza istoricului în recomandări concrete. Citește-l înainte
de a formula recomandările.

## Cuprins
- 1. Formula 95% (AskUserQuestion)
- 2. Plan mode (Shift+Tab)
- 3. Heuristica „ȘI = 2 procese"
- 4. Selecția de model (Haiku / Sonnet / Opus)
- 5. Strategia `/clear` și sesiuni scurte
- 6. Prompt caching (economie automată)
- 7. Comenzi de monitorizare (`/cost`, `/context`, `/usage`)
- 8. CLAUDE.md ca memorie persistentă
- 9. Tipare bune vs. proaste de prompting
- 10. Checklist „igienă de context & cost"
- 11. Cum traduci o observație într-o recomandare

---

## 1. Formula 95% (AskUserQuestion)

Formula universală de pus în prompt:

> „Pune-mi întrebări cu AskUserQuestion până când ești 95% sigur că înțelegi
> toate cerințele."

- Răspunsurile la AskUserQuestion îi dau asistentului contextul fără să
  „ghicească" — economisesc 3-5 cicluri de iterații greșite.
- Maximum 4 întrebări per rundă (limita tool-ului). Task complex → mai multe runde.
- Variantă pentru cei non-tech: adaugă „sunt non-tech, ajută-mă să-ți răspund".
- Acoperă 6 zone: obiectiv, audiență, scope (ce intră / ce NU), constrângeri,
  format rezultat, definiția de „gata".

**Când o recomanzi:** când vezi prompturi scurte/vagi („fă-mi un site"), sau
multe cicluri de refacere în aceeași sesiune.

---

## 2. Plan mode (Shift+Tab)

- `Shift+Tab` → asistentul NU execută, îți face un plan; tu aprobi; apoi execută.
- Combină plan mode cu formula 95%: „în plan mode, folosește AskUserQuestion ca
  să faci un plan bun; după ce aprob, începe lucrul".
- Previne anti-pattern-urile „fă-mi 5 lucruri" și „am stat ore pe același nod".
- Regulă de aur: **planul se face cu Opus**. „Plan mode cu Haiku e ca și cum ai
  arunca cu piatra în soare."

**Când o recomanzi:** task-uri non-triviale, multi-pas, sau unde s-au făcut
multe corecturi după ce execuția a pornit fără plan.

---

## 3. Heuristica „ȘI = 2 procese"

> „Dacă apare cuvântul «ȘI» în descriere, de obicei poți sparge în 2 procese.
> Cu cât ții pașii mai condensați, cu atât îi e mai greu asistentului să se încurce."

Exemplu (caz real): „citește emailurile ȘI arhivează ce nu trebuie ȘI răspunde
personalizat" = 5 lucruri = haos. Spargere corectă:
1. Proces «citire»: citește + sortează (urgent / normal / spam)
2. Proces «arhivare»: arhivează vechile (peste 30 zile, citite)
3. Proces «răspuns»: generează drafturi doar pentru cele urgente

Fiecare proces = pas separat, ideal **sesiune separată cu `/clear` între ele**.

**Când o recomanzi:** prompturi foarte lungi care înghesuie mai multe acțiuni;
prezența literală a lui „și / ȘI" care leagă verbe diferite.

---

## 4. Selecția de model (Haiku / Sonnet / Opus)

| Model | Putere | Cost | Pentru ce |
|---|---|---|---|
| **Haiku** | Bună (basic) | Mic | Iterații rapide simple, formatare, parsare cunoscută |
| **Sonnet** (default) | Foarte bună | Mediu | ~80% din task-urile zilnice (execuție de rutină) |
| **Opus** | Excelentă | Mare | Plan mode, debug greu, decizii arhitecturale, setup complex |

Reguli:
1. **Plan mode → Opus.** (Altfel „piatra în soare".)
2. **Execuție de rutină → Sonnet** (default e suficient).
3. **Formatare / lookup rapid → Haiku** (economisești credit).
4. **NU folosi Haiku** pentru: plan mode, setup/instalări complexe (ex. MCP),
   brainstorming complex, debug arhitectural. „Haiku nu știe decât basic."

Comutare în Claude Code: `/model opus` (sau `sonnet` / `haiku`).

**Când o recomanzi:**
- Haiku domină în istoric (>40% răspunsuri) → verifică dacă planificarea se face
  greșit pe Haiku.
- Opus pe aproape tot (>80%) → posibil supra-folosit; execuția de rutină pe Sonnet.

---

## 5. Strategia `/clear` și sesiuni scurte

- `/clear` la **fiecare task nou**. Context poluat = răspunsuri proaste + credit ars.
- Tiparul „kitchen sink": începi un task, sari la altul fără legătură, te întorci.
  Fix: `/clear` între task-uri fără legătură.
- Tipar de aur: „1 folder = 1 lecție/task = 1 sesiune".
- Sesiunile foarte lungi (zeci/sute de mesaje) = context aglomerat. Sparge-le.

**Când o recomanzi:** zero sau foarte puține `/clear`, multe sesiuni lungi,
proporție mică `/clear` pe sesiune.

---

## 6. Prompt caching (economie automată)

- Anthropic aplică prompt caching automat: cache-ul reduce mult costul când
  reciteșt același conținut (CLAUDE.md, fișiere mari, system prompt).
- Cache reads ≈ 10% din prețul input normal — e una dintre cele mai mari pârghii
  de cost. Un procent mare de tokeni prin cache e un semn BUN.
- Ca să profiți: pune fișierele mari **devreme** în prompt (prefix de cache);
  dacă schimbi ordinea, pierzi cache-ul.

**Când o recomanzi:** dacă procentul de tokeni prin cache e mic, sugerează
păstrarea contextului stabil (CLAUDE.md + fișiere mari la început).

---

## 7. Comenzi de monitorizare

- `/cost` — vezi cât ai consumat. Folosește-l periodic.
- `/context` — vezi din ce e compus contextul (cine umple fereastra).
- `/usage` — verifică limita de plan / consumul curent.

**Când le recomanzi:** dacă nu apar deloc în istoric — utilizatorul „zboară orb"
pe cost și context.

---

## 8. CLAUDE.md ca memorie persistentă

- Regulile scrise o dată în `CLAUDE.md` nu mai trebuie repetate în fiecare prompt
  (limba, stilul, „intră în plan mode la task-uri non-triviale", „NU folosi Haiku
  pentru plan mode", formatul de output).
- Reduce prompturile repetitive și lungi → mai puțin credit, mai multă consecvență.

**Când o recomanzi:** dacă vezi instrucțiuni repetate des în prompturi (același
ton, aceleași reguli rescrise) — mută-le în CLAUDE.md.

---

## 9. Tipare bune vs. proaste de prompting

**Tipare proaste (semnal că trebuie coaching):**
- Prompturi vagi de o frază: „fă-mi un site", „repară-l".
- Mega-prompturi (pereți de text) cu 5 acțiuni înghesuite.
- Zero `/clear` → sesiuni umflate, context poluat.
- Plan mode sărit la task-uri complexe → multe corecturi după start.
- Haiku pentru planning/debug → „habar n-are".
- Opus pentru orice fleac → cost inutil.
- Deep Research rulat repetat pe aceeași temă → dublezi creditul.

**Tipare bune (de lăudat și întărit):**
- Plan mode + formula 95% înainte de execuție.
- Spargerea task-urilor pe „ȘI".
- `/clear` între task-uri; sesiuni scurte și focusate.
- Model potrivit pe task (Opus plan / Sonnet execuție / Haiku trivial).
- CLAUDE.md cu reguli stabile; fișiere mari devreme (cache).
- `/cost` și `/context` consultate periodic.

---

## 10. Checklist „igienă de context & cost"

Folosește-l ca grilă rapidă când dai feedback. Bifează ce face deja bine
utilizatorul și transformă ne-bifatele în recomandări.

```
Igienă de CONTEXT:
- [ ] /clear la fiecare task nou (nu „kitchen sink")
- [ ] Sesiuni scurte: 1 task = 1 sesiune
- [ ] Plan mode la task-uri non-triviale
- [ ] Task-urile cu „ȘI" sunt sparte în procese separate
- [ ] CLAUDE.md ține regulile stabile (nu le rescrii în fiecare prompt)

Igienă de COST:
- [ ] Model potrivit: Opus plan / Sonnet execuție / Haiku trivial
- [ ] NU Haiku pentru plan mode, debug arhitectural, setup complex
- [ ] /cost verificat periodic
- [ ] /context verificat când fereastra se umple
- [ ] Fișiere mari puse devreme (profiți de prompt caching)
- [ ] NU rula Deep Research repetat pe aceeași temă

Calitatea PROMPTULUI:
- [ ] Formula 95% (AskUserQuestion) la cereri ambigue
- [ ] Prompt = obiectiv + context + criteriu de „gata"
- [ ] Nici vag de o frază, nici perete de text cu 5 acțiuni
- [ ] Spune cum se verifică rezultatul („arată-mi că merge")
```

---

## 11. Cum traduci o observație într-o recomandare

Scriptul `scripts/analizeaza_sesiuni.py` scoate observații-cifre. Transformă-le
în sfaturi concrete, în limbaj de business, cu un exemplu acționabil. Reguli:

- O recomandare = o observație + ce să facă diferit + de ce câștigă (cost/timp).
- Maxim 3-5 recomandări prioritizate (cele cu impact mare întâi). Nu copleși.
- Dă mereu un exemplu de prompt „înainte → după".
- Laudă întâi ce face bine, apoi corectează. Coaching, nu critică.

Exemplu de traducere:

| Observație (din script) | Recomandare (coaching) |
|---|---|
| „30% prompturi >1500 car." | „Prompturile tale sunt adesea pereți de text cu mai multe cereri. Sparge-le pe «ȘI» și folosește plan mode — vei avea mai puține corecturi. Ex: în loc de un prompt cu 4 acțiuni, fă 4 pași separați." |
| „Niciun `/clear`" | „Nu folosești `/clear` — contextul se aglomerează între task-uri și arzi credit. Dă `/clear` la fiecare task nou; regula «1 task = 1 sesiune»." |
| „Haiku 60% din răspunsuri" | „Folosești mult Haiku. E bun pentru lucruri simple, dar pentru plan mode și debug treci pe Opus — altfel «arunci cu piatra în soare»." |
