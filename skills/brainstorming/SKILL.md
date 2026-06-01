---
name: brainstorming
description: "Folosește acest skill ÎNAINTE de orice activitate creativă sau decizie deschisă — când utilizatorul spune „vreau să mă gândesc la...”, „idei pentru...”, „brainstorming pentru...”, „ajută-mă să aleg...” sau descrie un scop fără opțiuni concrete (cadou, postare, nume de brand, funcționalitate, strategie). Explorează intenția, cerințele și opțiunile prin întrebări structurate, înainte de a produce un rezultat."
---

# Brainstorming: De la Idei la Design

Transformă o idee vagă într-un plan/design clar, printr-un dialog colaborativ. Funcționează la fel de bine pentru decizii de business non-tehnice (idei de cadou, postări LinkedIn, nume de produs, oferte) și pentru proiecte tehnice (funcționalități, componente).

## Când se folosește

- Utilizatorul are un SCOP, dar nu are opțiuni concrete: „vreau să mă gândesc la idei pentru...”
- Apare o decizie deschisă cu mai multe direcții posibile
- Înainte de a construi/scrie ceva non-trivial — ca să nu pornești pe presupuneri greșite

## NU se activează când

- Utilizatorul a cerut deja explicit un singur lucru clar, fără ambiguitate
- Este o întrebare factuală cu un singur răspuns corect
- Utilizatorul vrea execuție imediată, nu explorare

## Procesul

**1. Înțelegerea ideii**
- Verifică mai întâi contextul (fișiere, documente, ce există deja)
- Pune întrebări **una câte una**, folosind tool-ul **AskUserQuestion**
- Preferă întrebări cu variante de răspuns (parametrul `options`), dar întrebările deschise sunt și ele ok
- O singură întrebare per mesaj — dacă un subiect e mare, sparge-l în mai multe întrebări
- Concentrează-te pe: scop, constrângeri, criterii de succes
- **Lasă utilizatorul să răspundă** — nu presupune în locul lui

**2. Explorarea abordărilor**
- Propune 2-3 direcții diferite, cu avantaje și dezavantaje
- Prezintă-le cu **AskUserQuestion** (`options`), cu avantajele în `description`
- Începe cu opțiunea recomandată și explică de ce

**3. Prezentarea rezultatului**
- Când ai înțeles ce vrea utilizatorul, prezintă designul/planul/lista de idei
- Pentru proiecte: împarte în secțiuni de 200-300 cuvinte și validează după fiecare
- Pentru ideație de business: dă 8-12 idei concrete cu rationale + recomandare top 3
- Fii pregătit să te întorci și să clarifici dacă ceva nu are sens

## Exemple

**Exemplu 1 — non-tech (cadou):**
- Input: „Vreau să fac brainstorming pentru cadoul soției.”
- Skill: pune 4-5 întrebări cu AskUserQuestion (vârstă, interese, buget, ocazie, ultimul cadou apreciat) → 8-12 idei concrete + top 3.

**Exemplu 2 — business (conținut):**
- Input: „Idei pentru o postare LinkedIn despre lansarea produsului.”
- Skill: clarifică audiența, obiectivul (awareness/lead), tonul → 8-10 unghiuri de postare + recomandare.

**Exemplu 3 — tehnic (funcționalitate):**
- Input: „Vreau să mă gândesc la cum ar arăta un sistem de alertă de preț.”
- Skill: întrebări despre surse, prag, canal de notificare → 2-3 abordări cu trade-offs → design pe secțiuni.

## Principii cheie

- **O întrebare pe rând** — nu copleși cu întrebări multiple
- **Variante de răspuns preferate** — mai ușor de răspuns când e posibil
- **YAGNI fără milă** — elimină ce e inutil din orice plan
- **Explorează alternative** — propune mereu 2-3 direcții înainte de a decide
- **Validare incrementală** — prezintă în secțiuni, validează fiecare
- **Fii flexibil** — întoarce-te și clarifică dacă ceva nu are sens
