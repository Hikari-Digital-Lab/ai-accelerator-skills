# skills-basic — Pachetul Foundation de Skills (AI Accelerator)

Biblioteca de **9 skills foundation** pentru Claude Code, în limba română, pentru utilizatori de business non-tehnici. Este pachetul predat la începutul **Modulului 2 — Power User** din cursul AI Accelerator.

Fiecare skill se **auto-activează** când descrierea lui se potrivește cu ce scrii (nu trebuie să-l „chemi" explicit — `description` = trigger-ul).

---

## Cele 9 skills

| Skill | Ce face | Se activează când scrii (exemple) |
|---|---|---|
| **brainstorming** | Ideație structurată înainte de execuție — întrebări → 8-12 idei + recomandare. Pentru decizii deschise (cadou, postare, nume brand, funcționalitate). | „vreau să mă gândesc la...", „idei pentru...", „brainstorming pentru..." |
| **plan-helper** | Forțează „plan mode" — întrebări cu AskUserQuestion (formula 95%), sparge task-uri (heuristica „ȘI = 2 procese"), livrează un plan numerotat de aprobat. | „fă-mi un plan pentru...", „planifică...", „cum abordez...", „de unde încep cu..." |
| **summarizer** | Rezumat structurat al oricărui text/email/document: TL;DR + puncte cheie + „ce vrea de la mine" + acțiuni per persoană + deadline-uri. | „rezumă", „TL;DR", „dă-mi pe scurt", „ce vrea de la mine?" |
| **file-organizer** | Organizează logic foldere: analiză → duplicate (hash) → propunere structură → mută/redenumește **doar cu confirmare**. | „organizează folderul X", „fă ordine în Downloads", „găsește duplicate" |
| **pdf-extractor** | Din PDF-uri lungi (contracte, oferte, T&C): clauze importante, obligații per parte, deadline-uri și **flag-uri de risc**. *(Nu e consultanță juridică.)* | „extrage din PDF", „ce clauze are", „ce obligații am", „analizează contractul" |
| **brand-voice** | Extrage „vocea ta de brand" (fișă personaj reutilizabilă) din 3-5 sample-uri de scriere: ton, vocabular, ritm, formule, do/don't. | „extrage stilul meu", „fișă personaj", „scrie ca mine", „analizează-mi stilul" |
| **deck-generator** | Generează slide-uri în Markdown gata de importat în **gamma.app** (o idee per slide, structură pitch/raport/training). | „fă-mi slide-uri", „prezentare", „deck pentru", „un pitch pentru" |
| **skill-creator** | Meta-skill — te ghidează să creezi (sau să actualizezi) alte skills. *(Versiunea oficială Anthropic, în engleză.)* | „vreau să fac un skill", „transformă în skill" |
| **interaction-coach** | Analizează **local** istoricul tău de conversații cu Claude Code și dă sfaturi: prompturi mai bune, unde pierzi context/credit, ce să automatizezi. | „analizează cum folosesc Claude Code", „unde pierd credit/context" |

---

## Instalare (via `/plugin`)

Acest folder este un **marketplace + plugin** Claude Code (`skills-basic`). Din Claude Code:

```
/plugin marketplace add /mnt/c/Users/psilv/coding/skills-basic
/plugin install skills-basic@ai-accelerator-skills
```

> După instalare în sesiunea curentă, rulează `/reload-plugins` ca skills-urile să se activeze imediat (altfel repornește Claude Code).

Verificare:
```
/plugin
```
Tab **Installed** → vezi `skills-basic`. Sau întreabă direct:
```
Ce skills am din plugin-ul skills-basic? Spune-mi pe scurt ce face fiecare.
```

---

## Structura pachetului

```
skills-basic/
├── .claude-plugin/
│   ├── marketplace.json
│   └── plugin.json
├── README.md
└── skills/
    ├── brainstorming/        SKILL.md
    ├── plan-helper/          SKILL.md + references/ + scripts/
    ├── summarizer/           SKILL.md + references/ + scripts/
    ├── file-organizer/       SKILL.md + references/ + scripts/
    ├── pdf-extractor/        SKILL.md + references/ + scripts/
    ├── brand-voice/          SKILL.md + references/ + scripts/
    ├── deck-generator/       SKILL.md + references/ + scripts/
    ├── skill-creator/        SKILL.md + references/ + scripts/
    └── interaction-coach/    SKILL.md + references/ + scripts/
```

Cele 7 skills generate respectă convenția **skill-creator** (progressive disclosure): `SKILL.md` cu pași clari + exemple, `references/` pentru ghiduri aprofundate, `scripts/` pentru utilitare Python (doar bibliotecă standard, acolo unde e cazul cu instrucțiuni de instalare).

---

## Note

- Skills-urile sunt în **română** (cu excepția `skill-creator`, versiunea oficială Anthropic în engleză). Trigger-ele funcționează și pe formulări în engleză.
- Unele skills se **compun** între ele: `summarizer` + `pdf-extractor` (rezumat de contract), `brand-voice` → alte skills de scriere.
- `interaction-coach` rulează 100% **local** — nu trimite nimic în afara calculatorului.
