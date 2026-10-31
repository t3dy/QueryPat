# Rule: the biography section

The Biography page (`site/src/pages/Biography.tsx`) shows
`site/public/data/biography/curated.json` (curated events with importance,
narrative, sources, quotes, disputes and links). `biography/events.json` is 746
machine-extracted events (many with impossible dates) and feeds only the letter
events; do not regenerate it — `export_json.py` drops its related fields.

## curated.json is hand-curated

No exporter writes it. Change it through curation modules:

```bash
python scripts/biography/apply_biography_curation.py --check          # report
python scripts/biography/apply_biography_curation.py --verify         # apply
python scripts/biography/apply_biography_curation.py --audit          # every quote on the page
```

Each module in `curation/biography/` may define `CORRECTIONS` (set fields by
event id; `links` merges), `REPLACE` (swap one passage of a text field), `APPEND`
(add sources, quotes, `dispute.positions` without dropping the old ones), `AMEND`
(set fields on the one list item matching given fields — e.g. a wrong source
`locator`) and `NEW_EVENTS`. The applier is idempotent and `--verify` refuses to write unless
every quote on a touched event is verbatim in the corpus.

Prefer APPEND and REPLACE: replacing a list drops the earlier curator's sources
and the pre-commit guard refuses it. Replace only an entry whose own text is wrong,
and say so in `notes`.

## Conventions

- Never rename an id, even when its year is wrong (`pkd_bio_1956_marriage_anne`
  is the April 1959 marriage). Say so in `notes`.
- `sources[].lane` follows the file's existing convention: biographies C, letters
  E, Exegesis B.
- `links.studies: [{to, label}]` links an event to a dossier; `to` may carry
  `?facet=…#mentions`.
- Facts checked against the corpus so far: marriage to Anne, Ensenada, April 1,
  1959; to Nancy Hackett, July 1966; X-Kalay stay given as a month (Dick), three
  weeks (Sutin), until March (Arnold); police reported an arrest with Dick's
  stolen pistol in February 1972 (letter to Inspector Shine); Jane died January
  26, 1929; Laura born February 25, 1960; stroke found February 18, 1982; Tessa
  marriage April 1973 (Sutin) vs 1972 (Arnold) — see `curation/biography/key_dates.py`
  for the full list, including events confirmed unchanged.
- `--audit` passes on all 61 quotes as of 2026-10-30. Elisions ("...") are allowed
  when the fragments appear in order in one source; reordered fragments fail.
- Events whose `notes` still begin "Generated curation note" have not been
  checked: 75 of 196 on 2026-10-30, none at importance 4–5 (see
  `curation/biography/high_importance.py`). List them with a one-line filter on
  `notes` and work down by importance.
- Sutin locators in the generated entries were often a chapter off. Sutin's
  chapters: 1 Dec 1928–Jan 1929; 2 1929–44; 3 1944–50; 4 1950–58; 5 1958–63;
  6 1963–65; 7 1965–70; 8 1970–72; 9 1972–74; 10 Feb 1974–Feb 1975; 11 1975–78;
  12 1979–82. Dick lived in Santa Ana from 1976, not Fullerton.
- Names in the Exegesis are later than the experiences they name: "Zebra" is
  December 1976 (Sutin; letter to Hurst, Feb 11, 1977); "VALIS" is in the section
  filed under September 1975; "Black Iron Prison", "plasmate" and "living
  information" first appear in the folder filed under September 1976. Date the
  experience and the name separately.
