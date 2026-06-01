# Șabloane de rezumat pe tip de document

Cuprins:
- [Principiul de bază: BLUF + piramida inversată](#principiul-de-baza-bluf--piramida-inversata)
- [Șablonul universal (folosește-l implicit)](#sablonul-universal)
- [Șablon: email / thread de email-uri](#sablon-email)
- [Șablon: contract / document juridic](#sablon-contract)
- [Șablon: raport / document de business](#sablon-raport)
- [Șablon: notițe de ședință / transcript](#sablon-sedinta)
- [Reguli de stil pentru rezumat](#reguli-de-stil)

Alege șablonul după tipul textului. Dacă nu e clar, folosește **șablonul universal**.

---

## Principiul de bază: BLUF + piramida inversată {#principiul-de-baza-bluf--piramida-inversata}

**BLUF = „Bottom Line Up Front"** (concluzia la început). Pune mesajul cel mai
important în primul rând, apoi detaliile. Tehnică folosită în armata SUA tocmai
pentru a transmite rapid un mesaj focusat — diferă de un „abstract" prin faptul
că e mai scurt și mai direct, ca o teză.

**Piramida inversată** (din jurnalism): informația cea mai importantă sus,
restul în ordine descrescătoare a importanței. Cititorul poate să se oprească
oriunde și tot a înțeles esențialul. Exact ce vrea un om de business ocupat.

Regula practică: **dacă cititorul citește DOAR primul rând (TL;DR), trebuie să
știe deja ce să facă.** Restul rezumatului doar adaugă context.

---

## Șablonul universal (folosește-l implicit) {#sablonul-universal}

```markdown
## TL;DR
[1-3 fraze. Ce spune textul + ce se cere de la cititor. Asta e BLUF-ul.]

## Puncte cheie
- [Punct 1 — cel mai important]
- [Punct 2]
- [Punct 3]
(maximum 5 puncte, în ordinea importanței)

## Ce vrea de la mine (call-to-action)
- [Acțiunea concretă cerută de la TINE — verb + livrabil. Dacă nu se cere nimic, scrie „Nimic — doar informativ".]

## Acțiuni & deadline-uri
| Cine | Ce trebuie făcut | Până când |
|------|------------------|-----------|
| [nume / „eu"] | [acțiune concretă] | [data sau „nespecificat"] |

## De verificat / neclar
- [Lucruri ambigue, lipsă sau de confirmat. Omite secțiunea dacă nu e cazul.]
```

Reguli:
- Maximum **5 puncte cheie** (regula de bază pentru rezumate: bulleted list, max 5).
- Tabelul de acțiuni apare DOAR dacă există acțiuni reale. Nu inventa.
- Fiecare acțiune are **un singur owner** (cadrul SMART: un responsabil clar) și,
  dacă există în text, un **deadline** explicit.

---

## Șablon: email / thread de email-uri {#sablon-email}

Pentru email-uri lungi sau thread-uri cu mulți participanți. Extrage întâi
verbele de acțiune din text („te rog trimite", „confirmă", „aprobă", „până
vineri") — ele marchează de obicei un action item.

```markdown
## TL;DR
[1-2 fraze: cine scrie, despre ce, și ce se cere.]

## Ce vrea de la mine
- [Cererea explicită către tine. Dacă sunt mai multe, listează-le.]

## Acțiuni per persoană
| Cine | Ce trebuie făcut | Până când |
|------|------------------|-----------|
| Eu | [...] | [...] |
| [alt nume] | [...] | [...] |

## Context (pe scurt)
- [2-4 puncte de fundal, doar dacă e nevoie pentru decizie.]

## Deadline-uri menționate
- [Listează toate datele/termenele găsite în text.]

## De clarificat
- [Întrebări deschise sau lucruri ambigue din thread.]
```

Sfaturi:
- Într-un thread, **ultimul mesaj** și **cererea cea mai recentă** au prioritate.
- Ignoră semnăturile, disclaimerele și textul citat repetat („> ...").
- Dacă owner-ul unei acțiuni nu e numit explicit, deduce-l din context
  (cine a cerut, cine a făcut data trecută) — dar marchează că e o presupunere.

---

## Șablon: contract / document juridic {#sablon-contract}

Pentru contracte, oferte, termeni și condiții. **Atenție:** nu e consultanță
juridică — pentru contracte importante, recomandă mereu un avocat.

```markdown
## TL;DR
[1-2 fraze: ce tip de contract, între cine, pe ce durată, valoarea principală.]

## Obligațiile mele (ce trebuie să fac eu)
- [Plăți, livrabile, termene de care RĂSPUND eu.]

## Obligațiile celeilalte părți
- [Ce trebuie să facă ei.]

## Bani & termene
- Valoare / preț: [...]
- Când se plătește / ce declanșează plata: [...]
- Durată + reînnoire: [...]

## Cum se iese din contract (reziliere)
- [Perioadă de preaviz, penalități la ieșire anticipată.]

## ⚠️ Steaguri roșii (de verificat cu un avocat)
- [Clauze de reînnoire automată, răspundere dezechilibrată, formulări vagi
  gen „eforturi rezonabile" / „cât de curând posibil", penalități mari,
  confidențialitate prea largă, lipsă SLA.]

## De clarificat înainte de semnare
- [Termeni ambigui, date lipsă, ce trebuie negociat.]
```

Steaguri roșii frecvente de căutat: reînnoire automată, termene de plată
nerezonabile, clauze de răspundere/indemnizare dezechilibrate, formulări vagi
(„eforturi rezonabile", „ASAP"), lipsa unor deadline-uri măsurabile.

---

## Șablon: raport / document de business {#sablon-raport}

Pentru rapoarte, studii, propuneri, documente strategice.

```markdown
## TL;DR (rezumat executiv)
[2-3 fraze: concluzia principală + recomandarea principală. BLUF.]

## Constatări cheie
- [Constatare 1 + cifra/dovada de sprijin]
- [Constatare 2 + dovadă]
- [Constatare 3 + dovadă]
(max 5, în ordinea importanței)

## Recomandări
1. [Recomandare concretă, acționabilă]
2. [...]

## Cifre importante
- [Statistici, rezultate, sume relevante pentru decizie.]

## Ce vrea de la mine
- [Decizie / aprobare / acțiune cerută cititorului. Sau „doar informativ".]
```

---

## Șablon: notițe de ședință / transcript {#sablon-sedinta}

Pentru transcripturi de meeting, notițe, înregistrări transcrise.

```markdown
## TL;DR
[1-2 fraze: subiectul ședinței + cea mai importantă decizie/rezultat.]

## Decizii luate
- [Ce s-a hotărât — ca să nu se redeschidă discuția săptămâna viitoare.]

## Acțiuni (cine, ce, până când)
| Cine | Ce trebuie făcut | Până când |
|------|------------------|-----------|
| [@nume] | [acțiune] | [data] |

## Subiecte discutate (pe scurt)
- [2-5 puncte, în ordinea discuției.]

## Pași următori / next steps
- [Ce urmează, întâlniri viitoare, ce rămâne deschis.]
```

Reguli: o acțiune bună are 3 componente — **task specific, un singur owner, un
deadline clar**. Scrie „@Maria: trimite oferta revizuită până vineri 20",
NU „urmărire client".

---

## Reguli de stil pentru rezumat {#reguli-de-stil}

- **Rezumat extractiv vs. abstractiv:** pentru cifre, nume, sume, date și clauze
  legale — citează aproape verbatim (extractiv), ca să nu introduci erori.
  Pentru context și idei — reformulează mai natural (abstractiv). Combină-le.
- **Nu inventa.** Dacă o informație (deadline, owner, sumă) nu e în text, scrie
  „nespecificat", nu ghici. Mai bine un gol marcat decât o eroare.
- **Limbaj de business, zero jargon.** Explică termenii tehnici în paranteză.
- **Ordinea importanței**, mereu. Cel mai important sus.
- **Scurt.** Un rezumat de o pagină la un document de o pagină e inutil. Țintește
  ~10-20% din lungimea originalului, mai puțin la documente foarte lungi.
- **Păstrează limba originalului** pentru citate; restul rezumatului în română
  (sau în limba cerută de utilizator).
