# Metode de organizare a fișierelor (referință)

Cuprins:
1. Metoda PARA (organizare după acțiune)
2. Sistemul Johnny.Decimal (organizare prin numerotare)
3. GTD — material de referință
4. Convenții de denumire a fișierelor
5. Reguli de arhivare (pe dată / pe tip)
6. Greșeli frecvente de evitat
7. Cum alegi metoda potrivită pentru un client

Acest fișier se citește atunci când trebuie propusă o structură de foldere. Conține
metodele consacrate, regulile concrete și exemplele necesare pentru a face o
propunere bună, fără a reinventa nimic.

---

## 1. Metoda PARA (Tiago Forte)

PARA organizează informația după **cât de acționabilă este**, nu după subiect.
Patru foldere principale (plus un Inbox de intrare):

- **P — Proiecte (Projects):** lucruri active, cu un rezultat și un termen.
  Ex: `Lansare site nou`, `Raport trimestrial Q2`, `Renovare birou`.
- **A — Arii (Areas):** responsabilități continue, fără termen, pe care le menții.
  Ex: `Finanțe`, `Sănătate`, `Echipă`, `Marketing`, `Clienți`.
- **R — Resurse (Resources):** material de referință care te-ar putea interesa.
  Ex: `Articole`, `Template-uri`, `Inspirație design`, `Cercetare piață`.
- **A — Arhivă (Archives):** orice e inactiv din celelalte trei. Proiecte
  terminate, arii abandonate, resurse care nu mai sunt relevante.

Regula de aur PARA: când un proiect se termină, **mută-l în Arhivă**, nu îl șterge.
Potrivit pentru: oameni de business cu multe proiecte și responsabilități care se
schimbă des. E cel mai natural pentru audiența non-tehnică.

Structură exemplu:
```
Documente/
├── 1-Proiecte/
│   ├── Lansare-site-nou/
│   └── Raport-Q2-2026/
├── 2-Arii/
│   ├── Finante/
│   ├── Clienti/
│   └── Marketing/
├── 3-Resurse/
│   ├── Template-uri/
│   └── Cercetare-piata/
└── 4-Arhiva/
    ├── 2024/
    └── 2025/
```

---

## 2. Sistemul Johnny.Decimal

Organizare printr-un sistem de numerotare fix. Ideea centrală: **niciodată mai mult
de 10**. Astfel, când cauți ceva, alegi mereu dintre maximum 10 opțiuni la fiecare pas.

Trei niveluri:
- **Arii (Areas):** grupuri mari, numerotate pe intervale de 10: `10-19`, `20-29`...
  Ex: `10-19 Administrație`, `20-29 Clienți`, `30-39 Marketing`.
- **Categorii (Categories):** foldere în interiorul unei arii: `11`, `12`, `13`...
  Ex: `11 Facturi`, `12 Contracte`, `13 Bancă`.
- **ID-uri (IDs):** adresa exactă, mereu în formatul `XX.YY` (două cifre, punct,
  două cifre). Ex: `11.01 Facturi furnizori`, `11.02 Facturi clienți`.

Avantaj-cheie: pentru că folderele sunt numerotate, **nu se mai mută** când le
redenumești. `30.02 Grădină` rămâne pe loc chiar dacă îi schimbi numele.

Exemplu de adresă completă: `20-29 Clienți / 21 Acme SRL / 21.03 Oferte 2026`.

Potrivit pentru: oameni metodici, arhive mari și stabile, echipe care vor o
„hartă" comună a fișierelor. Mai rigid decât PARA — recomandă-l clienților care
chiar vor disciplină, nu celor copleșiți de haos.

---

## 3. GTD — material de referință (David Allen)

Pentru materialul de referință (lucruri pe care le păstrezi „la îndemână", nu
proiecte), GTD recomandă un **singur sistem de dosare în ordine alfabetică**, simplu.
Principiul: salvarea unui document trebuie să fie cât pică — îl arunci într-un folder
și gata. Nu construi ierarhii adânci pentru referință.

Două foldere de top funcționează surprinzător de bine:
- `Proiecte-active/` — un folder per proiect curent.
- `Dosar/` (filing cabinet) — tot restul, alfabetic.

Regulă de întreținere: cel puțin o dată pe an, treci prin dosare și arunci ce nu
mai e relevant.

---

## 4. Convenții de denumire a fișierelor

Reguli verificate, valabile cross-platform (Windows, Mac, Linux):

- **Data la început, format ISO 8601: `AAAA-LL-ZZ`** (ex: `2026-06-01`). Asigură
  sortarea cronologică automată. Ex: `2026-06-01-raport-vanzari.xlsx`.
- **Fără spații și fără caractere speciale.** Folosește doar litere, cifre,
  liniuță `-` și underscore `_`. Spațiile și caracterele speciale strică linkurile
  și compatibilitatea între sisteme.
- **Descriptiv, dar scurt.** `oferta-acme-renovare.pdf`, nu `document final (2).pdf`.
- **Cifre cu zero în față** pentru sortare corectă: `01`, `02`, ..., `10` (altfel
  `10` apare înaintea lui `2`).
- **Fără numere de versiune ad-hoc** gen `final-v2-FINAL`. Dacă chiar e nevoie de
  versiuni, pune data; data e o versiune naturală.
- **Curăță artefactele de descărcare:** `document-final-v2 (1).pdf` → `document.pdf`.

Caractere interzise în Windows (evită-le mereu): `\ / : * ? " < > |`, plus
caractere de control, plus spațiu sau punct la final.

Nume rezervate în Windows (NU le folosi nici cu extensie): `CON`, `PRN`, `AUX`,
`NUL`, `COM1`–`COM9`, `LPT1`–`LPT9`. Chiar și `NUL.txt` e problematic. Dacă un nume
de fișier coincide, adaugă un sufix (ex: `CON` → `CON_1`).

Șablon recomandat pentru documente importante:
```
AAAA-LL-ZZ_categorie_descriere-scurta.ext
2026-06-01_factura_acme-srl-renovare.pdf
```

---

## 5. Reguli de arhivare

### Pe dată (an / lună)
Bun pentru fotografii, facturi, extrase, corespondență — orice e legat de un moment.
```
Facturi/
├── 2025/
│   ├── 01-Ianuarie/
│   └── 02-Februarie/
└── 2026/
    └── 01-Ianuarie/
```
La fotografii, ideal e să folosești data din EXIF (când a fost făcută poza); dacă
lipsește, se folosește data modificării fișierului ca rezervă.

### Pe tip (categorie)
Bun pentru un folder haotic (ex: Downloads) cu multe tipuri amestecate: documente,
imagini, arhive, instalatoare. Vezi taxonomia din `scripts/scaneaza_folder.py`.

### Când arhivezi (regula practică)
- Proiecte neatinse de **6+ luni** → candidate de arhivă.
- Foldere neatinse de **peste un an** → mută-le în Arhivă (NU le ștergi — doar le
  dai la o parte).
- Instalatoare vechi, descărcări duplicate, fișiere deschise o dată și niciodată
  după → de obicei se pot șterge (cu confirmare).
- Regula „6 luni neatins": dacă nu ai deschis un fișier descărcat în 6 luni, aproape
  sigur nu îți trebuie.

---

## 6. Greșeli frecvente de evitat

- **Ierarhie prea adâncă.** Peste 3-4 niveluri = navigare frustrantă și căutare
  nesigură. Dacă ai nevoie de mai multă adâncime, de obicei trebuie regândite
  categoriile de sus, nu adăugate subfoldere. Ține-te de **regula a 3 niveluri**.
- **Structură prea plată.** Sute de fișiere într-un singur folder e la fel de rău.
  Echilibru: categorii largi sus (`Proiecte`, `Clienți`, `Media`, `Referință`) +
  maximum 3-4 niveluri.
- **Denumire inconsistentă** între proiecte / clienți. Alege un șablon și ține-te de el.
- **Lipsa unui loc permanent** pentru documente de lungă durată.
- **Niciun plan de arhivare** la final de an → folderele se umflă la nesfârșit.

---

## 7. Cum alegi metoda pentru un client

| Situație client                                  | Metodă recomandată |
|--------------------------------------------------|--------------------|
| Downloads / Desktop haotic, vrea repede ordine   | Pe **tip** (categorii) |
| Multe proiecte și responsabilități care se schimbă | **PARA**          |
| Arhivă mare, stabilă; vrea disciplină / hartă comună | **Johnny.Decimal** |
| Fotografii, facturi, extrase                     | Pe **dată** (an/lună) |
| Material de referință (articole, template-uri)   | **GTD** (alfabetic, plat) |

Recomandă o singură metodă, explică pe scurt de ce, și arată structura propusă
înainte de a muta orice.
