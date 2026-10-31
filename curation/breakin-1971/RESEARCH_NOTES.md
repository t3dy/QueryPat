# Research notes: the November 1971 break-in

Starting point for an authored dossier on the break-in at 707 Hacienda Way, Santa
Venetia (Marin County), on or about November 17, 1971, and the theories Dick and
others built on it. Not yet a dossier: nothing here is published. Follow
`docs/STUDY_DOSSIERS.md` and model the work on `curation/drugs-in-pkd/`.

## Sweep

```bash
python scripts/research/sweep_corpus.py --profile breakin --summary --out <file>
```

2026-10-30: 9,345 findings, 4,284 strong. Strong primary and document findings:
1,699. The strong tier is archived at
`archive/2026-10-30/research/2026-10-30_breakin-raw-findings.json.gz`.

Most strong hits are the **Xerox missive** (934) and **Pigspurt** (110): the
Exegesis's later theory of 1974, not the break-in itself. Separate them when
classifying. Exegesis section 016 alone has 591 strong hits; the folder filed
under September 1976 has 278.

## The leads that matter

**A police lead nobody on the portal mentions.** Letter to Inspector Shine,
November 4, 1972 (`LET_1972-11-04_INSPECTOR_SHINE_0038`): in February 1972 the
inspector told Dick he had "broken the case" — a man named Jerry Wade had been
arrested with Dick's Ruger .22 pistol, stolen in the robbery. Dick asks whether
anything more was recovered. This stands against every later theory (FBI, CIA,
KGB, Black Panthers, Minutemen, Christian fundamentalists, himself), and should
be a contradiction, not a resolution.

**Dick's own campaign of January 1975.** Letters to Senators Alan Cranston
(Jan 26), Frank Church (Jan 28, as head of the new Senate Select Committee),
William Proxmire (Jan 23), Howard M. Baker (Jan 23), Representative Ronald V.
Dellums (Jan 24), and the ACLU (Jan 26; and June 4, 1973). To Church he encloses
his August 1973 letter in *The Alien Critic* "in which I declare publically what
happened ... and who, at that time, I theorized had done it", and a London Times
piece on unsolved burglaries of anti-war dissenters.

**Other dated letters with several hits:** Dick Geis (June 7, 1973 — the *Alien
Critic* letter itself?), William B. Wolfson (Oct 6, 1972), Bank of Marin (Apr
21, 1973), Marin County Sheriff's Office (undated), John Brunner (Jan 14, 1975 —
already in the curated biography as `pkd_bio_1975_brunner_cia_breakin`), Carol
and Terry Carr (Mar 9, 1972), Linda (Aug 30, 1972), Göran Bengtson and Bruce
Gillespie (undated in the catalogue; check the dateline in the body).

**Biographies:** Arnold (212 strong hits — the largest), Sutin (42), Anne R. Dick
(witnesses Cindy, Clint, Ray Nelson: "Phil did it" / "Clint could have done it" /
"drug dealers he owed money to"). Arnold already reads the break-in through
amphetamine paranoia — see the drugs dossier, `DRG-BIO-ARNOLD-WRONGDRUG`.

**Interviews:** "Even Paranoids Have Enemies" (Paul Williams, 1974) and the Apel
and Briggs interview in *The Last Interview*; the Aquarian (1978) and the "dope
guru to high school kids" passage in *PKD Magazine Interviews*.

## Already on the portal

- Curated biography: `pkd_bio_1971_burglary` (importance 4, sources Arnold +2),
  `pkd_bio_1971_arnold_amphetamine_paranoia`, `pkd_bio_1975_brunner_cia_breakin`.
- Lexicon topic `psychology/paranoia` (drafted, 78 passages; 42% matched only
  "conspiracy").
- Drugs dossier: Santa Venetia section and `DRG-BIO-SUTIN-PARANOIA`.

## Pitfalls

- "break-in" also appears in the 1972–73 letters about other burglaries; check
  that each passage is about Hacienda Way.
- Dick's date drifts (November 16/17, 1971); keep the date each source gives.
- Do not let the Wade arrest "solve" the case on the page. Dick knew of it and
  kept theorising; that is the finding.
