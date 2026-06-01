# Checklist clauze & red-flags pentru contracte (România)

Listă concretă de clauze de urmărit într-un contract / ofertă / termeni și condiții,
plus de ce contează fiecare risc. Folosește-o la Pasul 3-5 din `SKILL.md`.

**Nu este consultanță juridică.** Este o grilă de citire ca să vezi rapid ce e
important și unde sunt capcanele. Deciziile importante se iau cu un avocat.

## Cuprins
1. Cum folosești checklist-ul
2. Clauze esențiale (trebuie să existe)
3. Red-flags — capcane clasice (cu praguri de referință)
4. Clauze abuzive (Legea 193/2000) — relevant când o parte e consumator
5. Grilă rapidă de severitate
6. Pe tipuri de document (furnizor / SaaS-T&C / chirie)

---

## 1. Cum folosești checklist-ul

- Stabilește mai întâi **rolul utilizatorului** (Beneficiar/Client vs.
  Prestator/Furnizor). Aceeași clauză e un risc pentru o parte și un avantaj pentru cealaltă.
- Pentru fiecare clauză din listă verifică: **există?** **e clară?** **e
  echilibrată (simetrică între părți)?** **e executabilă (are remediu/penalitate)?**
- **Absența** unei clauze importante (ex. fără plafon de răspundere) e ea însăși
  un risc — semnaleaz-o ca „lipsește", dar nu inventa text.
- Pragurile numerice de mai jos sunt **repere de piață**, nu reguli legale.
  Servesc la calibrarea severității, nu la a declara ceva „ilegal".

## 2. Clauze esențiale (trebuie să existe)

| Clauză | Ce verifici | Dacă lipsește/e vagă |
|---|---|---|
| **Părțile** | denumire, CUI/CNP, sediu, reprezentant legal, rol | risc de identificare/executare |
| **Obiectul** | concret și măsurabil — ce se livrează/prestează exact | obiect vag → greu de cerut executarea (art. 1.226 C. civ. cere obiect determinat sau determinabil) |
| **Prețul** | sumă, monedă, TVA, ce include/exclude | preț neclar → litigiu |
| **Termene de plată** | scadențe, modalitate, avans | cash-flow + penalități |
| **Durata** | determinată/nedeterminată, dată start/final | leagă-o de reînnoire și reziliere |
| **Reziliere/încetare** | cazuri, preaviz, procedură, pact comisoriu | vezi red-flags |
| **Răspundere** | plafon (cap), excluderi, daune | vezi red-flags |
| **Penalități** | întârziere plată, neexecutare | vezi red-flags |
| **Garanție** (la produse/servicii) | întindere, durată, remediu | garanție vagă = protecție iluzorie |
| **Forța majoră** | definiție, notificare, durată max., efect | prea largă scuză orice; prea îngustă = expunere |
| **Confidențialitate** | ce e confidențial, durată, penalitate | fără durată/scop = obligație nelimitată |
| **Proprietate intelectuală** | cine deține rezultatele, licențe | esențial în servicii/creație |
| **Legea aplicabilă & jurisdicția** | ce lege, ce instanță/arbitraj | vezi red-flags |
| **Notificări** | adrese, mijloc, când se consideră primită | probleme de probă la termene |

## 3. Red-flags — capcane clasice

Praguri orientative din practica de contract review (B2B):

### 3.1 Auto-reînnoire tacită (automatic renewal)
- **Ce e:** contractul se prelungește automat dacă nu trimiți o notificare de
  NON-reînnoire cu X zile înainte de termen.
- **Red-flag:** fereastra de notificare **prea scurtă** (< 30 zile) sau mijlocul
  de notificare nespecificat. Reper „confortabil": **60 zile**. Sub 30 zile → ÎNALT.
- **De ce contează:** ratezi fereastra → ești blocat încă un an. ~80% din contractele
  SaaS au auto-reînnoire; cea mai des întâlnită fereastră de non-reînnoire e 60 de zile.
- **Notă RO:** auto-reînnoirea prin acord tacit poate fi **clauză abuzivă** dacă
  termenul de opțiune lăsat consumatorului e insuficient (vezi §4).

### 3.2 Reziliere unilaterală asimetrică
- **Red-flag:** cealaltă parte poate rezilia „pentru convenință" cu preaviz scurt,
  dar tu trebuie preaviz lung + taxă de reziliere. Sau pact comisoriu (reziliere de
  drept, fără instanță) declanșat de încălcări minore.
- **Severitate:** asimetrie clară → ÎNALT.
- **De ce contează:** lipsă de predictibilitate; te poate lăsa fără serviciu sau te poate ține captiv.

### 3.3 Limitarea / plafonarea răspunderii (liability cap)
- **Red-flag:** răspunderea celeilalte părți e **plafonată foarte jos** (sub
  valoarea a 6 luni / a contractului) SAU răspunderea **ta** e **nelimitată**.
  Atenție și la **excepțiile de la plafon** (ex. confidențialitatea exclusă din cap
  → expunere teoretic nelimitată).
- **Reper:** un cap rezonabil ≈ valoarea a 12 luni de plăți. Cap sub 6 luni sau
  „uncapped" în defavoarea ta → ÎNALT.

### 3.4 Indemnizare / despăgubire (indemnification)
- **Red-flag:** formulări foarte largi — „arising out of, relating to, or in
  connection with" / „în legătură cu" — te obligă să acoperi aproape orice.
  Periculos mai ales dacă indemnizarea e **scoasă din plafonul de răspundere**.
- **Severitate:** largă + în afara cap-ului → ÎNALT.

### 3.5 Jurisdicție & lege aplicabilă
- **Red-flag:** lege/jurisdicție **străină** fără motiv de business clar; arbitraj
  obligatoriu cu costuri/venue dezavantajoase; instanță într-un forum îndepărtat.
- **Notă RO:** pentru consumator, impunerea arbitrajului în locul instanței poate
  fi abuzivă (consumatorul are dreptul la instanță — Legea 193/2000 / Cod proc. civ.).
- **Severitate:** jurisdicție străină fără rost → ÎNALT.

### 3.6 Exclusivitate / non-concurență
- **Red-flag:** te obligă să lucrezi DOAR cu ei sau îți interzice clienți/furnizori
  concurenți, fără compensație sau pe durată/teritoriu disproporționat.
- **Severitate:** exclusivitate strânsă, neremunerată → ÎNALT/MEDIU.

### 3.7 Penalități de întârziere
- **Red-flag:** procent zilnic mare, fără plafon, sau penalități care depășesc cu
  mult prejudiciul. În RO, penalitatea manifest excesivă poate fi redusă de instanță
  (art. 1.541 C. civ.), dar tehnica e plafonarea din contract.
- **Severitate:** disproporționat / fără plafon → MEDIU (ÎNALT dacă e foarte mare).

### 3.8 Indexare / majorare preț
- **Red-flag:** furnizorul poate mări prețul la reînnoire fără preaviz și **fără
  plafon**. Reper: ~55% din contractele enterprise cu auto-reînnoire au plafon de
  escaladare de 3-5%/an. Lipsa plafonului → MEDIU.

### 3.9 Modificare unilaterală a termenilor
- **Red-flag:** o parte poate schimba unilateral termeni/preț/condiții fără motiv
  întemeiat și fără acceptul tău. În RO, în raport cu consumatorul, e tipic abuziv (§4).
- **Severitate:** ÎNALT.

### 3.10 Date personale / GDPR (la SaaS și prelucrare date)
- **Red-flag:** lipsa unui **DPA** (acord de prelucrare a datelor), temei legal
  neclar, fără drepturile persoanei vizate, transferuri în afara UE fără garanții.
- **De ce contează:** fără DPA nu poți, practic, lucra conform cu date UE.
- **Severitate:** ÎNALT.

### 3.11 SLA (la SaaS) — nivel de serviciu
- **Red-flag:** fără uptime garantat sau remediu (credite) pentru nerespectare.
  Reper de piață B2B: **99,5%-99,9%** uptime. Lipsa SLA / remediu → MEDIU.

## 4. Clauze abuzive (Legea 193/2000)

Relevant **doar** când una dintre părți e **consumator** (persoană fizică,
profesionist pe de altă parte). O clauză nenegociată direct este abuzivă dacă
**creează un dezechilibru semnificativ** între drepturi și obligații, în
defavoarea consumatorului, contrar bunei-credințe. Exemple tipice de clauze abuzive:
- dreptul profesionistului de a **modifica unilateral** clauzele fără motiv întemeiat
  prevăzut în contract;
- **auto-reînnoirea** prin acord tacit când termenul de opțiune lăsat consumatorului
  e insuficient;
- reținerea de sume de la consumator pentru neexecutare, fără despăgubire echivalentă
  când profesionistul e cel care nu execută;
- impunerea **arbitrajului** / a unei jurisdicții care îngrădește dreptul de a se adresa instanței.

Dacă identifici așa ceva și utilizatorul e consumator → flag **ÎNALT** + recomandare
de avocat. Sursă oficială: textul Legii 193/2000 pe `legislatie.just.ro` și ANPC.

## 5. Grilă rapidă de severitate

- **ÎNALT** — potențial abuziv (consumator), asimetrie majoră, răspundere nelimitată
  pentru tine / cap foarte mic pentru ei, jurisdicție străină fără rost, exclusivitate
  strânsă, modificare unilaterală, lipsă DPA, auto-reînnoire cu preaviz < 30 zile.
- **MEDIU** — penalități mari, indexare fără plafon, garanție/forță majoră/confidențialitate
  vagi, lipsă SLA/remediu, indemnizare largă (dar în cap).
- **SCĂZUT** — formulări neclare, anexe lipsă, termene de notificare nespecificate,
  numerotare/referințe inconsistente.

## 6. Pe tipuri de document

### Contract de furnizare / prestări servicii
Prioritate: obiect măsurabil, preț + termene de plată, penalități de întârziere
(cu plafon), garanție, reziliere simetrică, forță majoră, confidențialitate, IP, jurisdicție.

### SaaS / Termeni și condiții
Prioritate: auto-reînnoire (fereastra de non-reînnoire), majorare preț (plafon),
SLA/uptime + remediu, DPA/GDPR, plafon de răspundere + excepții, terminare + export/ștergere date.

### Contract de chirie / închiriere
Prioritate: durată + reînnoire (relocațiune tacită), preaviz de denunțare, garanție/depozit,
indexare chirie, cui revin reparațiile, condiții de reziliere, penalități, predare/recepție.

---

## Surse (verificate)
- Legea 193/2000 (clauze abuzive) — `legislatie.just.ro` și ANPC (`anpc.ro`).
- Clauze esențiale în contracte comerciale RO — articole de practică juridică (prunaru.ro, legalzen.ro, qabusiness.ro).
- Praguri red-flag B2B (auto-renewal 60z, cap 12 luni, SLA 99,5-99,9%, escaladare preț 3-5%) — ghiduri de contract review (spellbook.legal, bindlegal.com, SaaS contract guides).
