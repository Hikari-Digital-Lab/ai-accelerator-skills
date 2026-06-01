#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Analizor de stil pentru sample-uri de scriere în limba română.

Scop
----
Citește 3-5 sample-uri de text ale unui utilizator (postări, e-mailuri, articole)
și scoate METRICI OBIECTIVE care ajută la construirea unei „fișe de voce de brand":

- lungimea medie a propozițiilor (în cuvinte) + variația (min/max/abatere standard);
- cuvinte de conținut frecvente (excluzând stop-words RO) — vocabularul tipic;
- bigrame frecvente (expresii de 2 cuvinte recurente);
- scor de lizibilitate aproximativ (Flesch adaptat, euristic pentru RO);
- densitate de emoji, semne de exclamare/întrebare, MAJUSCULE, puncte de suspensie;
- formule recurente de ÎNCEPUT și de SFÂRȘIT (primele/ultimele cuvinte ale textelor).

Metricile sunt un PUNCT DE PLECARE, nu verdictul final. Modelul (Claude) combină
aceste cifre cu citirea calitativă a textelor pentru fișa de voce.

Utilizare
---------
Fiecare sample = un fișier .txt sau .md. Dă căile ca argumente:

    python analizor_stil.py sample1.txt sample2.txt sample3.md

Sau un folder care conține sample-urile (.txt/.md):

    python analizor_stil.py /cale/catre/folder_sampleuri/

Opțional, scoate rezultatul ca JSON (pentru a-l pasa altui pas):

    python analizor_stil.py --json sample1.txt sample2.txt

Nu necesită librării externe (doar biblioteca standard Python 3.8+).
"""

from __future__ import annotations

import json
import math
import os
import re
import sys
from collections import Counter

# ---------------------------------------------------------------------------
# Stop-words RO (sursă: stopwords-iso/stopwords-ro). Cuvinte de legătură /
# funcționale care NU spun nimic despre vocabularul tipic al autorului, deci
# le excludem din topul de cuvinte de conținut.
# ---------------------------------------------------------------------------
STOP_WORDS_RO = set("""
a abia acea aceasta această aceea aceeasi acei aceia acel acela acelasi acele
acelea acest acesta aceste acestea acestei acestia acestui aceşti aceştia acolo
acord acum adica ai aia aibă aici aiurea al ala alaturi ale alea alt alta
altceva altcineva alte altfel alti altii altul am anume apoi ar are as asa
asemenea asta astazi astea astfel astăzi asupra atare atat atata atatea atatia
ati atit atita atitea atitia atunci au avea avem aveţi avut azi aş aşadar aţi ba
bine bucur bună ca cam cand capat care careia carora caruia cat catre caut ce
cea ceea cei ceilalti cel cele celor ceva chiar ci cinci cind cine cineva cit
cita cite citeva citi citiva conform contra cu cui cum cumva curând curînd când
cât câte câtva câţi cînd cît cîte cîtva cîţi că căci cărei căror cărui către da
daca dacă dar dat datorită dată dau de deasupra deci decit degraba deja deoarece
departe desi despre deşi din dinaintea dintr dintre doar doi doilea două drept
dupa după dă ea ei el ele era eram este eu exact eşti face fara fata fel fi fie
fiecare fii fim fiu fiţi foarte fost frumos fără geaba graţie halbă ia iar ieri
ii il imi in inainte inapoi inca incit insa intr intre isi iti la le li lor lui
lângă lîngă ma mai mare mea mei mele mereu meu mi mie mine mod mult multa multe
multi multă mulţi mulţumesc mâine mîine mă ne nevoie ni nici niciodata nicăieri
nimeni nimeri nimic niste nişte noastre noastră noi noroc nostri nostru nou noua
nouă noştri nu numai o opt or ori oricare orice oricine oricum oricând oricât
oricînd oricît oriunde pai parca patra patru patrulea pe pentru peste pic pina
plus poate pot prea prima primul prin putini puţin puţina puţină până pînă rog sa
sai sale sau se si sint sintem spate spre sub sunt suntem sunteţi sus sută sînt
sîntem sînteţi să săi său ta tale te ti timp tine toata toate toată tocmai tot
toti totul totusi totuşi toţi trei treia treilea tu tuturor tăi tău ul ului un
una unde undeva unei uneia unele uneori unii unor unora unu unui unuia v va vi
voastre voastră voi vom vor vostru vouă voştri vreme vreo vreun vă zece zero zi
zice îi îl îmi împotriva în înainte înaintea încotro încât încît între întrucât
întrucît îţi ăla ălea ăsta ăstea ăştia şapte şase şi ştiu ţi ţie
""".split())

# Vocale RO (inclusiv diacritice) — pentru numărarea aproximativă a silabelor.
VOCALE = set("aeiouăâîAEIOUĂÂÎ")

# Pattern emoji (acoperă majoritatea blocurilor Unicode de emoji uzuale).
EMOJI_RE = re.compile(
    "[" +
    "\U0001F300-\U0001FAFF" +  # simboluri & pictograme, emoji suplimentare
    "\U00002600-\U000027BF" +  # simboluri diverse + dingbats
    "\U0001F1E6-\U0001F1FF" +  # steaguri regionale
    "\U00002190-\U000021FF" +  # săgeți
    "\U0000FE00-\U0000FE0F" +  # selectori de variație
    "]+",
    flags=re.UNICODE,
)

# Cuvânt = secvență de litere RO (inclusiv diacritice), eventual cu cratimă/apostrof.
CUVANT_RE = re.compile(r"[A-Za-zĂÂÎȘŞȚŢăâîșşțţ]+(?:[-'][A-Za-zĂÂÎȘŞȚŢăâîșşțţ]+)*")


def numara_silabe(cuvant: str) -> int:
    """Estimează numărul de silabe = numărul de grupuri de vocale.

    Euristic, suficient pentru un scor de lizibilitate aproximativ în RO.
    Ex.: „casă" -> 2, „extraordinar" -> 5, „și" -> 1.
    """
    grupuri = 0
    in_vocala = False
    for ch in cuvant:
        if ch in VOCALE:
            if not in_vocala:
                grupuri += 1
                in_vocala = True
        else:
            in_vocala = False
    return max(grupuri, 1)


def imparte_propozitii(text: str) -> list[str]:
    """Împarte textul în propoziții pe .?! și pe linie nouă dublă."""
    bucati = re.split(r"(?<=[.!?])\s+|\n{2,}", text.strip())
    return [b.strip() for b in bucati if b.strip()]


def flesch_aproximativ_ro(nr_cuvinte: int, nr_propozitii: int, nr_silabe: int) -> float:
    """Flesch Reading Ease adaptat euristic pentru RO.

    Formula clasică: 206.835 - 1.015*(cuvinte/propoziții) - 84.6*(silabe/cuvint).
    În RO cuvintele au mai multe silabe decât în EN, deci scorurile ies mai mici;
    îl tratăm doar ca indice RELATIV (mai mare = mai ușor de citit), nu absolut.
    """
    if nr_propozitii == 0 or nr_cuvinte == 0:
        return 0.0
    cps = nr_cuvinte / nr_propozitii          # cuvinte per propoziție
    spc = nr_silabe / nr_cuvinte              # silabe per cuvânt
    return round(206.835 - 1.015 * cps - 84.6 * spc, 1)


def eticheta_lizibilitate(scor: float) -> str:
    """Etichetă calitativă pentru scorul Flesch adaptat la RO.

    Pragurile sunt CALIBRATE pentru RO: pentru că în română cuvintele au mai
    multe silabe decât în EN, același text iese cu ~30 de puncte mai jos decât
    pe scala clasică. De aceea „ușor de citit" începe pe la 40, nu pe la 70.
    """
    if scor >= 40:
        return "foarte ușor de citit (fraze scurte, cuvinte simple)"
    if scor >= 20:
        return "ușor-mediu (accesibil unui public larg)"
    if scor >= 0:
        return "mediu-dificil (fraze mai lungi sau cuvinte mai dense)"
    return "dificil (fraze lungi, vocabular pretențios)"


def primele_cuvinte(text: str, n: int = 4) -> str:
    cuvinte = CUVANT_RE.findall(text.strip())
    return " ".join(cuvinte[:n])


def ultimele_cuvinte(text: str, n: int = 4) -> str:
    cuvinte = CUVANT_RE.findall(text.strip())
    return " ".join(cuvinte[-n:])


def analizeaza_sample(text: str) -> dict:
    """Analizează un singur sample și întoarce metricile lui."""
    propozitii = imparte_propozitii(text)
    cuvinte = CUVANT_RE.findall(text)
    cuvinte_lower = [c.lower() for c in cuvinte]
    nr_silabe = sum(numara_silabe(c) for c in cuvinte)

    lungimi = [len(CUVANT_RE.findall(p)) for p in propozitii]
    lungimi = [x for x in lungimi if x > 0]
    if lungimi:
        medie = sum(lungimi) / len(lungimi)
        varianta = sum((x - medie) ** 2 for x in lungimi) / len(lungimi)
        abatere = math.sqrt(varianta)
    else:
        medie = abatere = 0.0

    return {
        "nr_propozitii": len(propozitii),
        "nr_cuvinte": len(cuvinte),
        "lungime_medie_propozitie": round(medie, 1),
        "lungime_min_propozitie": min(lungimi) if lungimi else 0,
        "lungime_max_propozitie": max(lungimi) if lungimi else 0,
        "variatie_lungime": round(abatere, 1),
        "lizibilitate": flesch_aproximativ_ro(len(cuvinte), len(propozitii), nr_silabe),
        "nr_emoji": len(EMOJI_RE.findall(text)),
        "nr_exclamari": text.count("!"),
        "nr_intrebari": text.count("?"),
        "nr_suspensii": len(re.findall(r"\.\.\.|…", text)),
        "cuvinte_lower": cuvinte_lower,
        "inceput": primele_cuvinte(text),
        "sfarsit": ultimele_cuvinte(text),
    }


def colecteaza_fisiere(cai: list[str]) -> list[str]:
    """Transformă argumentele (fișiere sau foldere) într-o listă de fișiere text."""
    fisiere = []
    for cale in cai:
        if os.path.isdir(cale):
            for nume in sorted(os.listdir(cale)):
                if nume.lower().endswith((".txt", ".md")):
                    fisiere.append(os.path.join(cale, nume))
        elif os.path.isfile(cale):
            fisiere.append(cale)
        else:
            print(f"AVERTISMENT: nu gasesc {cale} - il sar.", file=sys.stderr)
    return fisiere


def agreaga(rezultate: list[dict]) -> dict:
    """Combină metricile per-sample într-un rezumat global."""
    total_cuvinte = [c for r in rezultate for c in r["cuvinte_lower"]]
    continut = [c for c in total_cuvinte if c not in STOP_WORDS_RO and len(c) > 2]

    # Bigrame pe cuvintele de conținut consecutive din fiecare sample.
    bigrame = Counter()
    for r in rezultate:
        seq = [w for w in r["cuvinte_lower"] if w not in STOP_WORDS_RO and len(w) > 2]
        for i in range(len(seq) - 1):
            bigrame[f"{seq[i]} {seq[i+1]}"] += 1

    n = len(rezultate)
    medii = {
        "lungime_medie_propozitie": round(
            sum(r["lungime_medie_propozitie"] for r in rezultate) / n, 1) if n else 0,
        "variatie_lungime": round(
            sum(r["variatie_lungime"] for r in rezultate) / n, 1) if n else 0,
        "lizibilitate": round(
            sum(r["lizibilitate"] for r in rezultate) / n, 1) if n else 0,
    }
    total_cuv = sum(r["nr_cuvinte"] for r in rezultate) or 1

    return {
        "nr_sampleuri": n,
        "total_cuvinte": sum(r["nr_cuvinte"] for r in rezultate),
        "total_propozitii": sum(r["nr_propozitii"] for r in rezultate),
        "medii": medii,
        "lizibilitate_eticheta": eticheta_lizibilitate(medii["lizibilitate"]),
        "top_cuvinte_continut": Counter(continut).most_common(25),
        "top_bigrame": [b for b in bigrame.most_common(15) if b[1] > 1],
        "densitate_emoji_la_1000_cuv": round(
            1000 * sum(r["nr_emoji"] for r in rezultate) / total_cuv, 1),
        "densitate_exclamari_la_1000_cuv": round(
            1000 * sum(r["nr_exclamari"] for r in rezultate) / total_cuv, 1),
        "densitate_intrebari_la_1000_cuv": round(
            1000 * sum(r["nr_intrebari"] for r in rezultate) / total_cuv, 1),
        "total_suspensii": sum(r["nr_suspensii"] for r in rezultate),
        "formule_inceput": [r["inceput"] for r in rezultate],
        "formule_sfarsit": [r["sfarsit"] for r in rezultate],
    }


def afiseaza_text(g: dict, rezultate: list[dict], nume_fisiere: list[str]) -> None:
    print("=" * 64)
    print("ANALIZĂ STIL — METRICI OBIECTIVE PENTRU FIȘA DE VOCE")
    print("=" * 64)
    print(f"Sample-uri analizate: {g['nr_sampleuri']}  "
          f"({g['total_cuvinte']} cuvinte, {g['total_propozitii']} propoziții)\n")

    print("— Ritmul propozițiilor —")
    print(f"  Lungime medie propoziție : {g['medii']['lungime_medie_propozitie']} cuvinte")
    print(f"  Variație (abatere std)   : {g['medii']['variatie_lungime']} "
          f"(mare = alternezi fraze scurte cu lungi)")
    print(f"  Lizibilitate (Flesch≈RO) : {g['medii']['lizibilitate']} "
          f"→ {g['lizibilitate_eticheta']}\n")

    print("— Vocabular tipic (cuvinte de conținut, fără cuvinte de legătură) —")
    for cuv, frecv in g["top_cuvinte_continut"]:
        print(f"  {cuv:<20} {frecv}x")
    print()

    if g["top_bigrame"]:
        print("— Expresii recurente (2 cuvinte) —")
        for big, frecv in g["top_bigrame"]:
            print(f"  „{big}” — {frecv}x")
        print()

    print("— Semnale de ton —")
    print(f"  Emoji      : {g['densitate_emoji_la_1000_cuv']} / 1000 cuvinte")
    print(f"  Exclamări  : {g['densitate_exclamari_la_1000_cuv']} / 1000 cuvinte")
    print(f"  Întrebări  : {g['densitate_intrebari_la_1000_cuv']} / 1000 cuvinte")
    print(f"  Suspensii  : {g['total_suspensii']} (...) în total\n")

    print("— Formule de ÎNCEPUT (primele cuvinte din fiecare sample) —")
    for f in g["formule_inceput"]:
        print(f"  ▸ {f} …")
    print("\n— Formule de SFÂRȘIT (ultimele cuvinte din fiecare sample) —")
    for f in g["formule_sfarsit"]:
        print(f"  … {f}")
    print()
    print("NOTĂ: cifrele sunt un punct de plecare. Citește și textele calitativ")
    print("(ce face, ce evită autorul) înainte de a scrie fișa de voce.")


def main(argv: list[str]) -> int:
    args = [a for a in argv[1:] if a != "--json"]
    ca_json = "--json" in argv

    if not args:
        print(__doc__)
        return 1

    fisiere = colecteaza_fisiere(args)
    if not fisiere:
        print("EROARE: niciun fișier valid de analizat.", file=sys.stderr)
        return 1

    rezultate = []
    for f in fisiere:
        try:
            with open(f, "r", encoding="utf-8") as fh:
                text = fh.read()
        except (OSError, UnicodeDecodeError) as e:
            print(f"AVERTISMENT: nu pot citi {f} ({e}) - il sar.", file=sys.stderr)
            continue
        if text.strip():
            rezultate.append(analizeaza_sample(text))

    if not rezultate:
        print("EROARE: sample-urile sunt goale.", file=sys.stderr)
        return 1

    if len(rezultate) < 3:
        print(f"AVERTISMENT: doar {len(rezultate)} sample(uri). Recomandat 3-5 "
              f"pentru o fișă de voce stabilă.\n", file=sys.stderr)

    g = agreaga(rezultate)
    if ca_json:
        # Eliminăm câmpurile voluminoase per-sample din JSON-ul de ieșire.
        print(json.dumps(g, ensure_ascii=False, indent=2))
    else:
        afiseaza_text(g, rezultate, fisiere)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
