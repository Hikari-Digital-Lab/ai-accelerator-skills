---
name: summarizer
description: >-
  Rezumă structurat orice text lung — email, thread, document, contract, raport, notițe de ședință — într-un TL;DR clar (1-3 fraze) + puncte cheie + „ce vrea de la mine" (call-to-action) + acțiuni per persoană + deadline-uri. Funcționează pe text lipit direct, pe fișiere locale (.txt/.md) și se compune cu skill-ul pdf-extractor pentru PDF-uri. Se activează când utilizatorul scrie lucruri de tipul: „rezumă...", „TL;DR", „dă-mi pe scurt", „ce vrea de la mine?", „care e rezumatul", „prea lung, fă-mi un sumar", „extrage acțiunile/deadline-urile din...". NU se activează când textul e deja foarte scurt (1-2 fraze) sau când utilizatorul cere să SCRIE conținut nou (un email, un articol, un raport) în loc să rezume ceva existent.
---

# Summarizer

Transformă orice text lung în răspunsul la întrebarea pe care o are de fapt un om
de business ocupat: *„Ce zice asta și ce trebuie să fac eu?"*. Output structurat,
acționabil, în limbaj clar — nu un al doilea text la fel de lung.

## Când se folosește

Se activează când utilizatorul vrea să înțeleagă rapid un text existent, nu să
creeze unul nou. Exemple de fraze:
- „Rezumă email-ul ăsta." / „Rezumă fișierul ~/Downloads/contract.pdf."
- „TL;DR la thread-ul de mai jos."
- „Dă-mi pe scurt ce zice raportul."
- „Ce vrea de la mine în mesajul ăsta?"
- „Extrage-mi acțiunile și deadline-urile din notițele de la ședință."
- „E prea lung, fă-mi un sumar cu punctele importante."

Tipuri de text acoperite: email-uri lungi și thread-uri, contracte și oferte,
rapoarte și propuneri, notițe/transcripturi de ședință, articole, orice document
.txt/.md, și PDF-uri (prin compunere cu `pdf-extractor`).

## Ce face

1. Detectează tipul de text (email / contract / raport / ședință / generic) și alege șablonul potrivit.
2. Produce un **TL;DR** de 1-3 fraze după principiul BLUF (concluzia la început).
3. Extrage **punctele cheie** (max 5, în ordinea importanței).
4. Izolează **„ce vrea de la mine"** — call-to-action-ul concret pentru cititor.
5. Listează **acțiunile per persoană** (cine, ce, până când) și toate **deadline-urile**.
6. Marchează ce e **neclar / de verificat**, fără să inventeze date lipsă.

## Pași (workflow)

Urmează acești pași în ordine.

```
Progres Summarizer:
- [ ] Pas 1: Obține textul (lipit direct / fișier / PDF prin pdf-extractor)
- [ ] Pas 2: Verifică lungimea (anti-trigger „prea scurt" + nevoie de chunking)
- [ ] Pas 3: Detectează tipul de text și alege șablonul
- [ ] Pas 4: Extrage acțiuni + deadline-uri (checklist)
- [ ] Pas 5: Scrie rezumatul structurat (TL;DR + restul)
- [ ] Pas 6: Marchează ce e neclar; NU inventa
```

### Pas 1 — Obține textul

- **Text lipit direct** în conversație → folosește-l ca atare.
- **Fișier .txt / .md** → citește-l de la calea dată.
- **PDF** → activează întâi skill-ul `pdf-extractor` ca să scoți textul, apoi rezumă-l aici. (Aceasta e „compunerea": `summarizer` + `pdf-extractor`.)
- Dacă utilizatorul cere un rezumat dar nu a dat niciun text/fișier, cere-l scurt.

### Pas 2 — Verifică lungimea

Rulează helper-ul ca să decizi strategia (metrici + nevoie de împărțire):
```bash
python scripts/analiza_text.py --fisier /cale/catre/document.txt
# sau pentru text lipit:
python scripts/analiza_text.py "textul lipit aici"
```
Scriptul întoarce: nr. de cuvinte, timp de citire estimat și o `strategie`:
- `fara_rezumat` → textul e deja foarte scurt (anti-trigger). Răspunde direct, fără TL;DR formal.
- `un_singur_pas` → rezumă normal, dintr-o singură citire.
- `map_reduce` → text lung. Împarte-l în bucăți și rezumă în pași (vezi mai jos).

Pentru documente foarte lungi, salvează bucățile pe disc și procesează-le pe rând:
```bash
python scripts/analiza_text.py --fisier doc.md --salveaza-bucati /tmp/bucati
```
Apoi **map-reduce**: rezumă fiecare bucată separat, după aceea combină
rezumatele parțiale într-un singur TL;DR + listă de acțiuni finală. Această
strategie dă acoperire completă și cost predictibil pe documente mari.

### Pas 3 — Detectează tipul și alege șablonul

Identifică tipul de text și folosește șablonul corespunzător din
`references/sabloane-rezumat.md`:
- **Email / thread** → secțiunea „Șablon: email".
- **Contract / ofertă / T&C** → secțiunea „Șablon: contract" (include steaguri roșii).
- **Raport / propunere** → secțiunea „Șablon: raport".
- **Notițe / transcript de ședință** → secțiunea „Șablon: ședință".
- **Nesigur / generic** → „Șablonul universal".

Citește `references/sabloane-rezumat.md` pentru structura exactă a fiecăruia și
pentru regulile de stil (extractiv vs. abstractiv, max 5 puncte, BLUF).

### Pas 4 — Extrage acțiuni + deadline-uri

Parcurge `references/checklist-actiuni.md` ca să nu ratezi nicio cerere. Pe scurt:
caută verbele de acțiune („te rog", „confirmă", „trimite", „aprobă"), apoi pentru
fiecare acțiune completează **cele 3 W: Ce / Cine / Până când**. Fiecare acțiune
are **un singur owner**. Separă explicit „ce vrea de la MINE" de acțiunile altora.

### Pas 5 — Scrie rezumatul

Aplică șablonul ales. Implicit, structura universală e:

```markdown
## TL;DR
[1-3 fraze — ce spune textul + ce se cere. Concluzia la început.]

## Puncte cheie
- [...] (max 5, ordinea importanței)

## Ce vrea de la mine
- [Acțiunea concretă cerută ție. Sau „Nimic — doar informativ".]

## Acțiuni & deadline-uri
| Cine | Ce trebuie făcut | Până când |
|------|------------------|-----------|
| ...  | ...              | ...       |

## De verificat / neclar
- [Doar dacă e cazul.]
```

### Pas 6 — Marchează ce e neclar

Dacă un deadline, un owner sau o sumă nu apare în text, scrie „nespecificat" sau
„(presupus)". **Nu inventa.** Mai bine un gol marcat onest decât o eroare cu aer
de certitudine. Pentru contracte, adaugă mereu nota că nu e consultanță juridică.

## Exemple input → output

**Exemplul 1 — email de business**

Input: *„Rezumă: «Bună Andrei, am revizuit propunerea voastră. În mare e ok, dar
prețul la modulul de raportare e peste buget — putem ajunge la 8.000 EUR? Am
nevoie de oferta finală până miercuri ca s-o duc în board joi. Trimite și 2
referințe de clienți similari. Mulțumesc, Carmen.»"*

Output:
```markdown
## TL;DR
Carmen acceptă propunerea în principiu, dar cere reducerea prețului la modulul
de raportare la 8.000 EUR și are nevoie de oferta finală până miercuri (board joi).

## Ce vrea de la mine
- Oferta finală cu modulul de raportare la 8.000 EUR.
- 2 referințe de clienți similari.

## Acțiuni & deadline-uri
| Cine | Ce trebuie făcut | Până când |
|------|------------------|-----------|
| Eu | Trimit oferta finală (raportare la 8.000 EUR) | Miercuri |
| Eu | Atașez 2 referințe de clienți similari | Miercuri |

## De verificat / neclar
- Putem coborî la 8.000 EUR fără a tăia din scope? De confirmat intern.
```

**Exemplul 2 — extragere acțiuni din notițe de ședință**

Input: *„Rezumă notițele: «Ședință marketing. S-a decis lansarea campaniei de
toamnă pe 15 sept. Maria pregătește vizualurile. Decizie: bugetul rămâne 5.000
lei. Radu trebuie să confirme bugetul cu finanțul până vineri. Discutat și
newsletter-ul, rămâne pe luna viitoare.»"*

Output:
```markdown
## TL;DR
Marketingul lansează campania de toamnă pe 15 septembrie cu buget de 5.000 lei;
mai rămâne confirmarea bugetului cu departamentul financiar.

## Decizii luate
- Lansarea campaniei de toamnă pe 15 septembrie.
- Bugetul campaniei: 5.000 lei.

## Acțiuni (cine, ce, până când)
| Cine | Ce trebuie făcut | Până când |
|------|------------------|-----------|
| Maria | Pregătește vizualurile campaniei | Nespecificat |
| Radu | Confirmă bugetul cu departamentul financiar | Vineri |

## Pași următori
- Newsletter-ul se amână pentru luna viitoare.
```

**Exemplul 3 — anti-trigger (text prea scurt)**

Input: *„Rezumă: «Ne vedem mâine la 10 la birou. Mulțumesc!»"*

Output: Skill-ul NU produce un rezumat formal. Textul e deja de 1-2 fraze —
răspunde direct: *„E deja foarte scurt: întâlnire mâine la 10, la birou. Nimic de
rezumat."*

## NU se activează când (anti-triggers)

- **Text deja foarte scurt** (1-2 fraze, un mesaj simplu). Un rezumat ar fi mai lung decât originalul.
- **Cerere de a SCRIE conținut nou** — „scrie-mi un email", „redactează un raport",
  „compune o postare". Acolo se creează text, nu se rezumă. (Folosește alt skill.)
- **Cerere de traducere, corectare sau reformulare** fără rezumare.
- **Întrebare punctuală** la care răspunzi dintr-o frază, fără structura completă.

În aceste cazuri, treci direct la acțiune — rezumatul formal ar fi birocrație inutilă.

## Best practices

- **BLUF — concluzia la început.** Dacă cititorul citește doar primul rând, trebuie să știe deja ce să facă.
- **Max 5 puncte cheie**, în ordinea importanței (piramida inversată: importantul sus).
- **„Ce vrea de la mine" e vedeta.** Pentru un om ocupat, asta contează cel mai mult — pune-o sus și clar.
- **Un action item = un owner = (ideal) un deadline.** Nu „urmărire client", ci „trimite oferta până vineri".
- **Extractiv pentru cifre, abstractiv pentru idei.** Sume, date, nume și clauze legale — citează aproape verbatim, ca să nu introduci erori. Contextul — reformulează natural.
- **Nu inventa.** Date lipsă → „nespecificat". Owner dedus → „(presupus)". Mai bine un gol marcat decât o eroare.
- **Documente lungi → map-reduce.** Împarte în bucăți (`scripts/analiza_text.py`), rezumă pe rând, apoi combină. Nu încerca să „înghiți" tot dintr-o dată.
- **Contracte ≠ consultanță juridică.** Marchează steagurile roșii, dar recomandă un avocat pentru documente importante.
- **Limbaj de business, zero jargon.** Explică termenii tehnici în paranteză.
