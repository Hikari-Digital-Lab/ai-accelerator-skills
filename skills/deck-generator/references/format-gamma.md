# Format Gamma.app — Cum scrii Markdown care se importa corect

> Cuprins:
> 1. Cum ajunge Markdown-ul in Gamma (cele 2 metode)
> 2. Regula de aur: `---` separa slide-urile
> 3. Sintaxa Markdown pe care o intelege Gamma
> 4. Densitate: o idee per slide
> 5. Checklist final inainte de import
> 6. Greseli frecvente

Acest ghid e sursa de adevar pentru ce importa gamma.app. Nu inventa sintaxa —
foloseste doar elementele de mai jos, verificate pe documentatia Gamma.

---

## 1. Cum ajunge Markdown-ul in Gamma

Utilizatorul are doua cai (ii spui in raport pe care sa o foloseasca):

1. **Paste in Text (recomandat pentru output-ul nostru):**
   - In Gamma: `New` (sau `Create new`) -> `Paste in text`.
   - Sus, deasupra editorului, alege formatul **Presentation** (nu Webpage/Doc/Social).
   - Lipeste TOT continutul fisierului `.md`.
   - Gamma analizeaza structura si genereaza cardurile. Stilul si imaginile se
     adauga apoi automat (AI) sau manual.

2. **Import fisier:**
   - In Gamma: `New` -> `Import` -> incarci fisierul.
   - Gamma importa textul in carduri (un card per slide).

**Important:** Gamma importa DOAR textul si structura. Culorile, fonturile si
imaginile NU vin din Markdown — le pune Gamma dupa. De aceea output-ul nostru se
concentreaza pe **structura curata si text putin**, nu pe stilizare.

---

## 2. Regula de aur: `---` separa slide-urile

Fiecare slide (card in Gamma) este separat de urmatorul printr-o linie cu exact
trei liniute pe rand propriu:

```markdown
## SLIDE 1 - TITLU
# Titlul prezentarii

---

## SLIDE 2 - PROBLEMA
# Care e durerea?
...
```

- `---` = regula orizontala in Markdown = **card nou** in Gamma.
- Pune o linie goala inainte si dupa `---` (mai sigur la parsare).
- Alternativa in interfata Gamma este comanda `/split`, dar in fisierul nostru
  folosim MEREU `---` (functioneaza la paste si la import).
- Daca doua slide-uri ajung lipite intr-un card, lipseste un `---` intre ele.

**Antet de fisier:** prima linie poate fi titlul documentului (`# Slide-uri: ...`),
urmat de `---`. Gamma il trateaza tot ca pe un inceput de continut — nu e o problema.

---

## 3. Sintaxa Markdown pe care o intelege Gamma

Gamma parseaza Markdown standard. Foloseste DOAR aceste elemente:

| Element | Sintaxa | Devine in Gamma |
|---------|---------|-----------------|
| Titlu mare | `# Titlu` | Heading 1 (titlul cardului) |
| Subtitlu | `## Subtitlu` | Heading 2 |
| Sub-subtitlu | `### Detaliu` | Heading 3 |
| Bullet | `- punct` | Lista cu buline |
| Lista numerotata | `1. pas` | Lista ordonata |
| Bold | `**accent**` | Text ingrosat |
| Italic | `*nuanta*` | Text inclinat |
| Citat | `> citat` | Blockquote (card de citat) |
| Tabel | `\| A \| B \|` | Tabel |
| Cod | triplu backtick + limbaj | Bloc de cod |

**Convertirea marcatorului de slide:** scriem `## SLIDE N - TITLU` la inceputul
fiecarui slide pentru claritate interna si pentru ca scriptul de validare il
recunoaste. In Gamma devine doar un heading — utilizatorul il poate sterge sau
pastra. Daca vrei un deck "curat" pentru client, poti omite linia `## SLIDE N`
si pastra doar `---` + titlul real al slide-ului; ambele variante se importa.

### Tabel — format exact

```markdown
| Coloana A | Coloana B |
|-----------|-----------|
| Rand 1A   | Rand 1B   |
| Rand 2A   | Rand 2B   |
```

Maxim 5 randuri de date per tabel. Daca ai mai multe, imparte pe doua slide-uri.

### Cod — format exact (rar in deck-uri de business)

````markdown
```python
print("salut")
```
````

---

## 4. Densitate: o idee per slide

Gamma recomanda **o idee per card** si "muta continut pe un card nou daca devine
prea inalt". Regulile pe care le aplicam (audienta business, non-tech):

- **O singura idee/mesaj per slide.** Daca pui doua idei, fa doua slide-uri.
- **Regula 6x6:** maxim ~6 bullet-uri, ~6 cuvinte per bullet (ghid, nu lege).
- **Maxim 5 bullet-uri** si **~50 de cuvinte** per slide (prag in validator).
- **Titluri scurte** — fraza, nu paragraf.
- **Bold doar pe takeaway** — un singur accent per slide.
- Daca un slide are mai mult text decat incape lejer, **imparte-l**.

Logica: in Gamma, cardurile cresc in inaltime ca sa cuprinda textul. Daca pui
prea mult, cardul devine un perete de text greu de citit pe proiector.

---

## 5. Checklist final inainte de import

- [ ] Fiecare slide e separat prin `---` (linie goala inainte si dupa).
- [ ] Fiecare slide are un titlu (`#` sau `##`).
- [ ] O idee per slide; niciun slide nu depaseste ~5 bullet-uri / ~50 cuvinte.
- [ ] Tabelele au maxim 5 randuri de date.
- [ ] Diacritice complete (a, a, i, s, t).
- [ ] Ai rulat `scripts/valideaza_slideuri.py check fisier.md` si da OK.

---

## 6. Greseli frecvente

- **Folosesti `***` sau `* * *` ca separator** — foloseste `---` (trei liniute).
- **Pui tot textul pe un slide** — Gamma il ingramadeste; imparte-l.
- **Adaugi sintaxa pe care Gamma n-o reda** (HTML, shortcode-uri exotice) —
  ramai la Markdown de baza din tabelul de mai sus.
- **Astepti ca Markdown sa aduca culori/imagini** — nu aduce; Gamma stilizeaza.
- **Titluri lungi cat un paragraf** — taie-le la o fraza.
