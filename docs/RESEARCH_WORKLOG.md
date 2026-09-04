# Research worklog convention

QueryPat is an evidence system. A reader who asks *"why does the portal say
this?"* should be able to trace the answer back through the evidence, the
editorial reasoning, and the research session that produced it — six months or
six years later.

Conclusions are already preserved in the database and the exported JSON. What
was not preserved, until now, is **how we got there**: what was searched, what
was rejected, what remains uncertain, and why one formulation was chosen over
another. That is what this convention captures.

## When to write one

Write a worklog entry for a **substantive research session**: one that changes
what the portal claims, adds or reinterprets evidence, resolves or opens a
scholarly question, or makes an editorial decision someone might later want to
revisit.

Do **not** log routine mechanics — every shell command, every build, every
typo fix. The test is whether a future reader would need it to understand or
challenge a claim on the site.

## Where it goes

```
archive/YYYY-MM-DD/worklog/<NN>-<slug>.md
archive/YYYY-MM-DD/prompts/<NN>-<slug>.md        the instruction that started it
archive/YYYY-MM-DD/research/<date>_<what>.txt    sweeps, inventories, raw results
archive/YYYY-MM-DD/drafts/<artifact>.vN.<ext>    superseded versions, never overwritten
archive/YYYY-MM-DD/reports/<date>_<what>.md      validation and audit output
```

Start one with:

```bash
python scripts/safeguard/worklog.py new "burroughs corpus sweep"
```

## What an entry records

| Section | Purpose |
|---|---|
| Research question | what was actually being asked |
| Instruction | the prompt or brief, verbatim or summarised, linked to `prompts/` |
| Corpus searched | which tables, columns, files and formats — and which were *not* |
| Queries | the actual search terms and patterns |
| Documents examined | what was read, including things that turned out irrelevant |
| Discoveries | findings, each tied to a source |
| Interpretations | our reading, marked clearly as ours |
| Contradictions & alternatives | competing readings, preserved rather than resolved |
| Unresolved questions | what we still do not know |
| Decisions | what we chose and **why**, including what we rejected |
| Files changed | code, data, curation |
| Validation | what was run and what it said |
| Artifacts | what was archived, by path |

## The four evidentiary registers

Editorial prose on the site must not blur these. State which one you are in:

| | Register | Example |
|---|---|---|
| **A** | What PKD says himself | "Burroughs is right but he has only a bit of the whole picture" |
| **B** | What primary-source evidence establishes | the Brig Elliot letter is dated one day before the Exegesis entry |
| **C** | What scholars argue | Sutin reports that K.W. Jeter drew the Burroughs parallel |
| **D** | What portal editors infer | the 1976 modification anticipates the 1981 reversal |

Collapsing D into A is the failure mode this convention exists to prevent.

## Preserving alternatives

When a rewrite replaces existing prose, archive the previous version to
`drafts/` first — the old reading may be better, or may become recoverable
evidence of how our understanding changed. Where two interpretations both fit
the evidence, record both and say why one leads. Do not flatten disagreement
into a single confident sentence; in this project, disagreement is data.

## Provenance in the data

Machine-readable counterparts to the worklog:

- `curation/<topic>/*.json` — the durable evidence inventory a page is built
  from, each finding carrying its source, classification, confidence and
  editorial note.
- `study_topics.*_generator` / `*_claim_ids` — which pass wrote each prose
  field and which claims back it.
- `archive/snapshots/INDEX.md` — every archived state, with its git HEAD.
