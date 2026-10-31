# Research notes: music in Philip K. Dick

Starting point for an authored dossier to replace the evidence base of the essay
`site/public/data/essays/music-in-pkd.md`. Not yet a dossier: nothing here is
published. Follow `docs/STUDY_DOSSIERS.md` and model the work on
`curation/drugs-in-pkd/`. A natural home is the `intertexts` study, beside the
Bible and Burroughs dossiers.

## The essay's problem

The essay rests on Perry Kinman's catalogue of 2,067 music references, which is
**not in the archive**. Nothing can be quoted from it or checked against it. The
dossier should be built from primary sources and say so; the catalogue can be
named as secondary context only.

## Sweep

```bash
python scripts/research/sweep_corpus.py --profile music --summary --out <file>
```

2026-10-30: 7,748 findings, 3,202 strong; 2,119 strong primary and document
findings across 226 letters. The strong tier is archived at
`archive/2026-10-30/research/2026-10-30_music-raw-findings.json.gz`.

Top terms: "flow my tears" 419 (mostly the novel's title — classify!),
Beethoven 347, opera 201, Wagner 161, Linda Fox 148 (the character in *The
Divine Invasion*), Dowland 113, Bach 109, Parsifal 85, Mozart 72, Beatles 67,
Linda Ronstadt 55, Strauss 48, Schubert 41, Mahler 30, Purcell 25, Fidelio 15,
Grateful Dead 13.

## The leads that matter

- **Wagner, from a record-store storeroom.** Letter to Robert and Virginia
  Heinlein, August 5, 1975: "I am an old, old Wagner buff"; as a high-school
  employee he found a rare Victor set of *Parsifal* act III conducted by Karl
  Muck, which "got me started". Ties to the Exegesis's Parsifal/plasmate passage
  already in the Bible dossier and the drugs dossier (`DRG-EX-1978-INGREDIENTS`:
  "I got it from 'Parsifal' back in high school").
- **Beethoven.** 1964 letters to James Blish and the Carrs; *Fidelio* in a 1977
  letter to Martin Roogna in Soviet Estonia; Exegesis section 016 and the 1981
  "Pat" folder. Sutin: Fischer-Dieskau's Schubert recordings, quoted in the 1960s
  novels.
- **Dowland.** Letter to John Brunner, August 27, 1970, on *Flow My Tears* and
  the lute song; the novel's chapter epigraphs (the text is not in the archive).
- **Linda Ronstadt and Linda Fox.** *The Divine Invasion* (in the VALIS Trilogy
  document) and the Rickman interviews ("Muzak and Linda Ronstadt", ch. 29 of
  *In His Own Words*).
- **Work.** University Radio and Art Music, the record stores where Dick worked
  (Sutin; Anne R. Dick).

Letters with the most hits: Heinlein (Aug 5, 1975), Blish (June 7, 1964), Carol
Carr (Sept 25, 1964), Claudia Bush (Mar 21, 1975), Martin Roogna (Aug 15, 1977),
the Carrs (Oct 26, 1964), Brunner (Aug 27, 1970), Patricia Warrick (Jan 10,
1981), Sherie Rush (Dec 26, 1981).

## Pitfalls

- "Flow my tears" is usually the novel; keep only passages about the song.
- "Opera", "quartet" and "symphony" are often figurative in the Exegesis.
- "Linda Fox" is a character speaking, lane A; Ronstadt in the letters is lane E.
- Check the Bible dossier's Parsifal passages before writing about the plasmate.
