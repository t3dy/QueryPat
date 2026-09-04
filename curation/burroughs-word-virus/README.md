# Curation: Burroughs and the Word Virus

Durable source of truth for the `/studies/intertexts/burroughs-word-virus` dossier.

This directory exists so that editorial discoveries do **not** live only in
`site/public/data`. The database and the exported JSON are both derived from
here; a regeneration can rebuild the page from this directory alone.

| File | What it is |
|---|---|
| `evidence-inventory.json` | Curated, classified findings. Hand-maintained. The seeder reads this. |
| `raw-findings.json` | Machine output of the full corpus sweep. Regenerable, not hand-edited. |
| `dossier.json` | The dossier prose, section by section, with its evidentiary register. |

Regenerate the raw sweep:

```bash
python scripts/research/sweep_corpus.py --profile burroughs --summary \
    --out curation/burroughs-word-virus/raw-findings.json
```

Rebuild the page from this directory:

```bash
python scripts/studies/seed_burroughs_word_virus.py
python scripts/safeguard/safe_export.py --exporter studies
```

## Relevance classification

Every finding carries a `relevance` code. These are editorial judgements, made
by reading the passage, not by pattern matching.

| Code | Meaning |
|---|---|
| 1 | **Direct Burroughs reference** — names Burroughs or one of his titles |
| 2 | **Burroughs concept/reference** — uses his terms (word virus, Nova police, cut-up) without naming him, in a context where the debt is established |
| 3 | **Possible Burroughs influence** — plausible but not demonstrable from the text |
| 4 | **Thematic parallel** — the same problem, no evidence of contact |
| 5 | **False positive** — keyword match only |

Findings at 4 and 5 are recorded, not published. Recording them is the point:
the next researcher should not have to re-derive that "junkie" in *A Scanner
Darkly* is ordinary English rather than a nod to Burroughs's *Junky*.

## Evidentiary register

Independently of relevance, each finding is tagged with the register it
belongs to. See `docs/RESEARCH_WORKLOG.md`.

| Register | Meaning |
|---|---|
| A | What PKD says himself |
| B | What primary-source evidence establishes |
| C | What scholars argue |
| D | What portal editors infer |

## Corpus coverage

The sweep searched, and the inventory reflects: Exegesis segments (`raw_text`
plus six curated fields), `document_texts.text_content` **and**
`markdown_content`, per-page OCR, individual letters, claims, biography events,
works, PKD-on-PKD mentions, evidence excerpts, annotations, theophanies,
timeline events, the 183 files of `database/extracted_markdown/`, and the
portal essays.

Patterns covered Burroughs's name and variants (including the OCR corruption
`Eurrough`), his titles, his coinages, and Dick's own concept vocabulary
(anti-information, jamming, occlusion, latent message, contamination,
parasite, living information, playback, cut-up). Full pattern list in
`raw-findings.json`.
