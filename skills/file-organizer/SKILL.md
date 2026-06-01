---
name: file-organizer
description: >-
  Organizează logic foldere și fișiere pe calculator: analizează structura
  curentă, găsește duplicate (prin hash), propune o structură mai bună și
  mută/redenumește fișierele DOAR cu confirmarea utilizatorului — niciodată
  fără aprobare. Reduce haosul digital. De folosit când utilizatorul cere, în
  română sau engleză: „organizează folderul X", „fă ordine în Downloads",
  „curăță folderul", „sortează fișierele", „găsește duplicate", „arhivează
  fișierele vechi", „organize my Downloads", „clean up this folder". NU se
  folosește pentru a deschide sau edita un singur fișier și nici pentru
  operații pe fișiere care nu țin de organizare (ex: editare conținut,
  conversie format, trimitere fișiere).
---

# File Organizer (Organizator de fișiere)

Asistent de organizare a fișierelor pentru oameni de business non-tehnici.
Transformă un folder haotic (Downloads, Desktop, dosare de proiecte) într-o
structură logică — în siguranță, cu confirmare la fiecare pas.

## Când se folosește

Folosește acest skill când utilizatorul cere ordine într-un folder. Exemple de
formulări care îl declanșează:
- „Organizează folderul Downloads / Documente / Desktop"
- „Fă ordine în Downloads, e un haos"
- „Curăță folderul ăsta de fișiere vechi"
- „Sortează fișierele pe tipuri / pe dată"
- „Găsește duplicatele și ajută-mă să decid ce păstrez"
- „Arhivează proiectele pe care nu le-am mai atins de un an"

## Ce face

1. **Analizează** structura curentă a folderului (câte fișiere, ce tipuri, ce
   mărimi, ce date).
2. **Găsește duplicate** în mod sigur și rapid (întâi după mărime, apoi prin hash
   SHA-256 — vezi scriptul).
3. **Propune** o structură mai bună, aleasă în funcție de situație (pe tip, pe dată,
   PARA, Johnny.Decimal).
4. **Mută și redenumește** fișierele — DOAR după ce utilizatorul aprobă planul.
5. **Niciodată nu șterge** fără aprobare explicită. Duplicatele se raportează;
   decizia de ștergere rămâne la utilizator.

## Pași (cum procedezi)

1. **Înțelege scopul.** Întreabă scurt, doar dacă nu e clar:
   - Ce folder? (Downloads, Documente, Desktop, dosar de proiecte?)
   - Care e problema principală? (nu găsesc nimic / duplicate / prea multe fișiere
     vechi / nicio structură?)
   - Există fișiere de evitat? (proiecte active, date sensibile?)

2. **Rulează scannerul în mod DRY-RUN** (nu schimbă nimic). Acesta listează
   fișierele, găsește duplicatele și propune un plan:
   ```bash
   python3 scripts/scaneaza_folder.py "CALEA/CATRE/FOLDER"
   # adaugă --recursiv pentru subfoldere; --dupa data pentru grupare an/lună
   ```

3. **Alege metoda de organizare** potrivită situației. Pentru reguli, taxonomii și
   exemple, citește `references/metode-organizare.md` (PARA, Johnny.Decimal, GTD,
   convenții de denumire, reguli de arhivare, tabelul „ce metodă pentru ce client").

4. **Prezintă planul** clar utilizatorului ÎNAINTE de orice modificare: structura
   propusă (arbore de foldere), ce fișiere se mută unde, ce duplicate s-au găsit,
   ce redenumiri se aplică. Cere aprobare explicită („da/nu/modifică").

5. **Aplică doar după aprobare.** Rulează cu `--aplica` (scriptul mai cere o
   confirmare și scrie un jurnal `plan_mutari.csv` pentru anulare la nevoie):
   ```bash
   python3 scripts/scaneaza_folder.py "CALEA/CATRE/FOLDER" --aplica
   ```

6. **Raportează rezultatul** și dă 2-3 sfaturi de întreținere (ex: sortează
   Downloads săptămânal, arhivează la final de an).

## Exemple (business, RO)

**Exemplu 1 — Downloads haotic (antreprenor).**
Utilizator: „Am 600 de fișiere în Downloads, nu mai găsesc nimic. Fă ordine."
Procesul: rulezi scannerul DRY-RUN → vezi documente, poze, instalatoare, arhive,
3 seturi de duplicate (220 MB recuperabili) → propui grupare pe tip (Documente,
Imagini, Instalatoare, Arhive, Diverse) → arăți planul → după „da", aplici cu
`--aplica` → raportezi: 600 fișiere în 5 foldere, jurnal salvat.

**Exemplu 2 — Dosar de clienți (firmă de servicii).**
Utilizator: „Organizează folderul Clienți, e amestecat și are versiuni duble."
Procesul: rulezi scannerul → identifici fișiere cu același conținut sub nume diferite
(`oferta-final.pdf`, `oferta-final-v2 (1).pdf`) → recomanzi metoda PARA sau
Johnny.Decimal din `references/metode-organizare.md` + convenția de denumire
`AAAA-LL-ZZ_client_descriere` → propui structura → aplici după confirmare.

**Exemplu 3 — Arhivare la final de an (contabilitate).**
Utilizator: „Arhivează facturile vechi pe ani și luni."
Procesul: rulezi `--dupa data` → structura devine `2025/01-Ianuarie/...` → propui
mutarea facturilor neatinse de 6+ luni în arhivă (fără ștergere) → aplici după „da".

## NU se activează când

- Utilizatorul vrea să **deschidă sau să editeze conținutul** unui singur fișier
  (ex: „deschide raportul", „schimbă textul din document").
- Se cere o **operație care nu ține de organizare**: conversie de format, trimitere
  pe email, compresie, redactare conținut.
- Se cere **ștergere în masă, automată** — acest skill nu șterge niciodată automat.

## Best practices (reguli de siguranță)

- **DRY-RUN întâi, mereu.** Rulează scannerul fără `--aplica` și arată planul. Nimic
  nu se mută până când utilizatorul nu confirmă.
- **Confirmare înainte de mutare.** Cere aprobare explicită pentru plan. La aplicare,
  scriptul mai cere o dată confirmarea („da").
- **Niciodată ștergere fără aprobare.** Duplicatele se RAPORTEAZĂ; nu se șterg
  automat. Recomandă ce să păstreze (de obicei copia cu numele/locul cel mai bun),
  dar decizia e a omului.
- **Nu suprascrie.** Dacă la destinație există deja un fișier cu același nume,
  scriptul adaugă un sufix (`-1`, `-2`) în loc să suprascrie.
- **Arhivează, nu șterge.** Fișierele vechi se mută în Arhivă, nu se aruncă.
- **Jurnal pentru anulare.** La `--aplica`, mutările se scriu în `plan_mutari.csv`
  ca să poată fi inversate manual la nevoie.
- **Evită ierarhiile adânci.** Maximum 3-4 niveluri (vezi greșelile din referință).
- **Ocolește fișierele active/sensibile** pe care utilizatorul le-a marcat.

## Resurse incluse

- `scripts/scaneaza_folder.py` — scanner DRY-RUN: listează fișiere, detectează
  duplicate prin hash (mărime → SHA-256), grupează pe tip sau dată, propune o
  structură; mută doar cu `--aplica` și logează în `plan_mutari.csv`.
- `references/metode-organizare.md` — metodele PARA, Johnny.Decimal, GTD; convenții
  de denumire (ISO 8601, caractere interzise, nume rezervate Windows); reguli de
  arhivare pe dată/tip; greșeli de evitat; tabel de alegere a metodei per client.
