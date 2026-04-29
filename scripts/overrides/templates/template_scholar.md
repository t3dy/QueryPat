# Template — Scholar Profile

For: entries in `scholars.json`. Each scholar has a profile page surfacing their interpretive contribution to PKD studies.

## Tier criteria

- **Tier 1** — Major biographers and primary editors of PKD's writings (Sutin, Anne Dick, Rickman, Arnold, Peake, Lethem/Jackson, Tessa Dick).
- **Tier 2** — Academic scholars with a substantial single-author monograph or multiple landmark articles, *or* whose interpretive frame later scholarship answers to (Robinson, Butler, Palmer, Freedman, Rossi, Burton, Fitting, Suvin, Jameson, Csicsery-Ronay, Lem, Kripal, McKee, DiTommaso, Lapoujade, Warrick).
- **Tier 3** — Editors of collections, finding-aid curators, archive maintainers, fan-academic critics with sustained venues (Sandner, Sullivan, Gillespie, Hollander, CSUF Special Collections).
- **Tier 4** — Single-article contributors with limited but real contributions; not foundational but cited.
- **Tier 5** — Media sources, peripheral mentions, journalists.

A scholar is in the wrong tier if (a) Tier 4 with a foundational monograph, or (b) Tier 1–2 with no interpretive contribution beyond a single review. Re-tiering is part of the editorial pass.

## Required fields

| Field | Length | Description |
|-------|--------|-------------|
| `scholar_id` | slug | stable kebab-case ID |
| `name` | string | canonical name |
| `role` | ≤6 words | one-phrase role (*Marxist science-fiction critic*; *Editor of the Exegesis*; *Italian Dickian, ontological-uncertainty reading*) |
| `tier` | 1–5 | per criteria above |
| `affiliation` | string | institution + period where known |
| `key_works` | array | titles only; no annotations |
| `interpretive_stance` | 120–250 words | the body of the profile (see below) |
| `relevance` | 60–120 words | why a researcher consults them (see below) |
| `quotable_lines` | array of {quote, source} | 2–5 lines later scholars cite |
| `scholarly_lineage` | 1–3 sentences | who they descend from intellectually, who they trained, who responded |
| `key_arguments` | 3–7 items | named moves; each one sentence |
| `disputes` | array of {opponent, issue} | documented disagreements with named scholars |
| `archive_pdfs` | array | existing field; documents in the archive by this scholar |

## interpretive_stance — required structure
**Length:** 120–250 words.
**Tone:** Critical-reportorial, attribute everything.

1. **The central claim about PKD** (one sentence). What is the one thing this scholar most distinctively argues?
2. **Methodological frame** (one sentence). Marxist, psychoanalytic, postmodern, biographical, theological, formalist, ideological-critique, deconstructive, Bergsonian, Deleuzean, etc.
3. **Specific moves** (2–4 sentences). The concepts they introduced, the readings they originated, the errors they corrected. Name works and prior scholars.
4. **Position against earlier scholarship** (1–2 sentences). Whom they answer to or push back on.

## relevance — required structure
**Length:** 60–120 words.
**Purpose:** Tell the researcher what classes of question this scholar answers.

Examples:
- "Primary source for biographical events 1959–1965; contradicts PKD's self-reports in interviews from the same period."
- "Canonical reading of *Ubik* as the formal apex of Dick's fiction; cited by every subsequent monograph."
- "Marxist/Althusserian frame; consult for ideological-critique readings of the mid-1960s novels."

## key_arguments — guidance
3–7 named moves. Each is one sentence. Examples:
- "*Ubik* is the formal apex of Dick's novelistic achievement."
- "PKD's 2-3-74 visions are read through clinical psychiatric categories without dismissing their intellectual content."
- "The break-in is an unsolvable case but the staging hypothesis cannot be ruled out."

## disputes — guidance
Array of `{opponent: "Sutin", issue: "the chronology of the Vancouver trip"}`. Only documented disagreements; not inferred ones.

## Lint checklist
- [ ] Tier matches criteria above.
- [ ] `interpretive_stance` ≥120 words and contains all four required components.
- [ ] `relevance` names question-classes, not vague praise.
- [ ] `key_arguments` is non-empty for Tier 1–3.
- [ ] `quotable_lines` populated for Tier 1–2 where extant.
- [ ] No empty interpretive fields for Tier 1–3.

## Worked examples
See the rewritten profiles for Kim Stanley Robinson, Peter Fitting, and Umberto Rossi in `scholars.json`. These are the canonical demonstrations of the target shape.
