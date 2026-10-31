# Rule: lexicon-scanned study topics

Topics in `ai/` and `psychology/` with status scanning, drafted or mapped come from
`scripts/studies/scan_corpus.py` matching word lists in
`scripts/studies/lexicons/{ai_topics,psychology_topics}.json`.

## How the scanner behaves

- Primary and alias terms compile to `\b(term|…)\b`, case-insensitive.
- `exclusions` are tested only within ±50 characters of each match. They cannot
  express "not about X" for a whole passage, and a window that also holds a valid
  match survives.
- It reads `document_texts.text_content` only. Books with only `markdown_content`
  (several biographies) are invisible to it.
- `scan_corpus.py --topic <slug>` rescans one topic and updates its
  `passage_count`. A full run deletes **every** study passage; `build_all.py`
  reseeds the authored dossiers afterwards.

## The recurring failure: one ambiguous word

Check what share of a topic each matched term accounts for before trusting it
(query `study_passages.matched_terms`).

**But read the topic's prose before calling a dominant term a false positive.**
Several `reviewed` topics were deliberately re-defined around Dick's own usage:
`ai/ai` is about the "AI voice" (about 600 of its 717 passages), `ai/surveillance`
about God "monitoring" the world, `ai/automation` about "automatic" unreflective
operation; `psychology/empathy`'s prose embraces agape. Narrowing those lexicons
would leave a definition that contradicts its own passages. (An "AI voice"
exclusion was tried and reverted on 2026-10-30 for exactly this reason.)

| Topic | Term | Status |
|---|---|---|
| `psychology/amphetamine-use` | `speed` (velocity) | 109 of 116 false; aliases replaced by drug phrases, 2026-10-30 |
| `psychology/addiction` | "habit" (52%), "compulsion" | prose is about drugs; likely false positives, not yet fixed |
| `psychology/double-doppelganger` | "copy" (26%), "double" | prose does not use "copy"; check before fixing |
| `psychology/psychosis` | "mad", "madness" | prose uses "mad"; check before fixing |

## Fixing one

Fix the lexicon, not the output: rescan the topic, then hand-place only
`evidence_packets`, `passage_count`, `chronology`, `related_documents`, and an
`editorial_notes` line into the committed topic JSON and the study `index.json`
row. A raw export nulls the topic's machine-drafted prose. Removing false
positives needs a scoped `.allow-data-loss` (see `generated-files.md`).
