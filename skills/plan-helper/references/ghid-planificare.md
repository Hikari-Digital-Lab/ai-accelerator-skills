# Ghid de planificare — întrebări, descompunere și structura planului

Material de referință pentru skill-ul plan-helper. Folosește-l ca să pui întrebări bune, să spargi corect task-urile complexe și să scrii planuri pe care utilizatorul le poate aproba imediat. Totul în limbaj de business, pentru oameni fără background tehnic.

## Cuprins
- [Cadrul de elicitare 95% (ce întrebări pui)](#cadrul-de-elicitare-95)
- [Cum pui întrebările cu AskUserQuestion](#cum-pui-intrebarile-cu-askuserquestion)
- [Descompunerea task-urilor (heuristica „ȘI = 2 procese")](#descompunerea-task-urilor)
- [Structura planului (BLUF + pași)](#structura-planului)
- [Definiția de „gata" și scope-out](#definitia-de-gata-si-scope-out)
- [Alegerea modelului](#alegerea-modelului)
- [Greșeli frecvente de evitat](#greseli-frecvente-de-evitat)

---

## Cadrul de elicitare 95%

Scopul: aduni suficient context cât să fii **95% sigur** ce vrea utilizatorul, înainte de a propune un plan. Inspirat din tehnicile clasice de „elicitare de cerințe" (interviu cu beneficiarul) și din regula celor 6 întrebări: **Ce? Pentru cine? Când? Unde? De ce? Cum?**

Acoperă cele 6 zone de mai jos. Pune întrebări doar acolo unde chiar nu știi răspunsul din cerere — nu întreba de dragul de a întreba.

### Zona 1 — Obiectivul (CE și DE CE)
- Care e rezultatul concret pe care îl vrei la final? (un fișier, o campanie, un proces, un document?)
- De ce ai nevoie de asta? Ce problemă rezolvă? *(„De ce" te duce de la simptom la nevoia reală — folosește-l cu tact, nu repetat ca un copil de 2 ani.)*
- Cum vei ști că a ieșit bine? (definiția de „gata")

### Zona 2 — Audiența / beneficiarul (PENTRU CINE)
- Cine folosește / citește / primește rezultatul? (tu, clienții, echipa, un partener?)
- Cât de „tehnic" e publicul? Ce ton se potrivește (formal / prietenos)?

### Zona 3 — Scope: ce intră și ce NU intră
- Ce trebuie neapărat să includă? (must-have)
- Ce ar fi frumos, dar nu e obligatoriu? (nice-to-have)
- Ce e clar în AFARA acestui task? (ca să nu existe surprize)

### Zona 4 — Constrângeri (CÂND, cu CE, CÂT)
- Există un termen-limită?
- Buget / unelte disponibile? (ex: ai deja un cont de email marketing? un site?)
- Ceva ce TREBUIE folosit sau, dimpotrivă, evitat?

### Zona 5 — Formatul rezultatului (CUM arată livrabilul)
- În ce formă vrei rezultatul? (text, tabel/Excel, listă de pași, fișiere, postări gata de publicat?)
- Unde ajunge? (un fișier local, un email, o platformă anume?)

### Zona 6 — Nivelul de polish și exemple
- Cât de „șlefuit" trebuie să fie? (ciornă rapidă vs. versiune finală)
- Ai un exemplu de „așa vreau să arate" sau „așa NU vreau"?

> **Regula deschis vs. închis:** preferă întrebări deschise care invită la detaliu, nu întrebări care suggerează răspunsul. Evită întrebările care „împing" utilizatorul spre un anume răspuns.

---

## Cum pui întrebările cu AskUserQuestion

Tool-ul **AskUserQuestion** afișează întrebări cu variante de răspuns (mai ușor pentru non-tech decât o întrebare goală).

- **Maximum 4 întrebări per apel.** Pentru task-uri mari, fă mai multe runde.
- Fiecare întrebare are un titlu scurt (`header`) și 2-4 opțiuni clare.
- Dacă recomanzi o opțiune, pune-o **prima** și adaugă „(Recomandat)" la final.
- Utilizatorul poate alege întotdeauna „Altceva" și să scrie text liber — nu trebuie să acoperi toate variantele.
- Folosește `multiSelect` când mai multe răspunsuri pot fi corecte simultan (ex: „pe ce canale promovezi?").
- Apelează tool-ul **doar când chiar ești blocat** pe o decizie care e a utilizatorului — nu pentru lucruri pe care le poți deduce singur din context.

**Cadență recomandată:**
- Task simplu: 1-2 runde × 3-4 întrebări.
- Task complex: 3+ runde × 4 întrebări — fiecare detaliu contează.
- Utilizator non-tech blocat: spune-i să scrie *„sunt non-tech, ajută-mă să-ți răspund"* și reformulează mai simplu, cu exemple în opțiuni.

---

## Descompunerea task-urilor

### Heuristica-rege: „cuvântul ȘI = 2 procese"
Dacă în descrierea task-ului apare **„ȘI"**, de regulă poți (și ar trebui) să spargi în 2 sau mai multe procese separate. Pași mai condensați = mai puțin context per pas = mai greu să se încurce asistentul și mai puține erori.

**Semnale că trebuie spart:**
- Apare „ȘI" / „și după aceea" / „plus că" / „totodată".
- Verbe multiple, diferite, în aceeași frază (citește **și** sortează **și** trimite **și** arhivează).
- Rezultatul atinge mai multe sisteme/locuri diferite (email + tabel + notificare).

### Reguli de spargere corectă
1. **Un proces = un verb principal = un singur livrabil.** „Citește emailuri" e un proces; „citește emailuri și răspunde" sunt două.
2. **Task atomic = încape într-o singură sesiune de lucru.** Dacă nu, mai sparge o dată.
3. **Fiecare pas începe cu un verb la imperativ** și se poate „bifa" (e clar când e gata).
4. **Procesele se execută pe rând**, ideal cu context proaspăt între ele (în Claude Code: `/clear` între procese mari).

### Exemplu de spargere (caz real)
Cerere brută: *„automatizare care îmi citește rezumatul mailurilor, arhivează ce nu-mi mai trebuie ȘI răspunde personalizat"* → 5 acțiuni într-un task = „death spiral".

Spargere corectă:
1. **Pipeline citire+sortare:** Citește emailuri și etichetează (urgent / normal / spam).
2. **Pipeline arhivare:** Arhivează emailurile vechi (peste 30 zile, citite).
3. **Pipeline curățare:** Șterge spam-ul confirmat.
4. **Pipeline răspuns:** Generează drafturi de răspuns DOAR pentru cele urgente.

Fiecare pipeline = pas separat. Propune-i utilizatorului: *„Le sparg în 4 procese ca să iasă curat și controlabil?"*

---

## Structura planului

Folosește **BLUF** (Bottom Line Up Front — concluzia la început, din comunicarea militară și executivă): prima frază spune rezultatul, nu despre ce e planul.

- **BLUF corect:** „La final vei avea un calendar de 4 săptămâni cu 8 postări gata de publicat."
- **BLUF greșit (e doar un titlu):** „Acest plan se ocupă de campania de Crăciun."

### Șablon de plan
```markdown
**Rezultat final:** [o frază — ce ai concret la final]

**Plan:**
1. [Verb] + [acțiune concretă] — [ce produce / de ce]
2. [Verb] + [acțiune concretă]
3. ...

**Ce NU intră în acest plan:** [scope-out — ce rămâne pe dinafară]
**Riscuri / de confirmat:** [1-3 puncte unde s-ar putea bloca]
**Model recomandat:** Opus pentru planificare, Sonnet pentru execuție.
```

### Reguli pentru pași
- Maxim ~8 pași per plan. Mai mult → împarte în 2-3 planuri mai mici. („3 planuri de 4 pași livrează mai sigur decât 1 plan de 12.")
- Numerotare clară, ordine logică (ce depinde de ce).
- Nicio acțiune „ascunsă" — dacă un pas presupune o decizie a utilizatorului, marcheaz-o.
- Cere riscurile/edge-case-urile explicit, ca să iasă la suprafață înainte, nu în timpul execuției.

---

## Definiția de „gata" și scope-out

Stabilește ÎNAINTE de a începe ce înseamnă „terminat", ca să eviți refacerile și „mai adaugă și asta" la nesfârșit (scope creep).

- **Definiția de „gata":** criteriile clare după care rezultatul e considerat complet și acceptat. Ex: „3 postări + 1 email, salvate într-un fișier, gata de copiat."
- **Scope-out:** scrie negru pe alb ce NU face planul. Ex: „nu include reclame plătite, nu include design grafic."

Dacă nici „gata", nici scope-ul nu sunt clare înainte de start, aproape sigur apar refaceri și frustrare.

---

## Alegerea modelului

| Model | Bun la | Folosește pentru | Cost |
|---|---|---|---|
| **Opus** | Raționament profund, structură, decizii | **Planificare**, descompunere complexă, debug greu | Mare |
| **Sonnet** (default) | Echilibru putere/viteză | **Execuția** planului, 80% din task-urile zilnice | Mediu |
| **Haiku** | Rapid, ieftin, lucruri simple | Formatare, parsare cunoscută, iterații banale | Mic |

Reguli:
1. **Planificare → Opus.** „Plan mode cu Haiku e ca și cum ai arunca cu piatra în soare."
2. **Execuție → Sonnet** (default e suficient).
3. **NU Haiku** pentru planificare, setup complex sau decizii — „Haiku nu știe decât basic".

În Claude Code: `/model opus` pentru a comuta.

---

## Greșeli frecvente de evitat

- **A executa înainte de a întreba.** Niciodată. Întrebări → plan → aprobare → execuție.
- **A ghici cerințele** ca să „economisești timp" — economisești 5 minute acum și pierzi 1 oră în refaceri.
- **Întrebări care suggerează răspunsul** (leading questions) sau care invită doar „da/nu" și nu prind nuanța.
- **Pași prea mari** care nu încap într-o sesiune — sparge-i.
- **Plan fără scope-out** — duce la „dar credeam că faci și X".
- **Jargon tehnic neexplicat** — pentru un public non-tech, fiecare termen tehnic merită o paranteză simplă.
- **A petici un plan greșit din temelii** în loc să-l rescrii — rezultă cod/muncă și mai proastă.
