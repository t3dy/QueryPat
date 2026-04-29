# Template — Scholarship Document Summary

For: academic articles, dissertations, scholarly monographs, edited collections.
Lane: **C** (Scholarship).

## card_summary
**Length:** 60–90 words.
**Tone:** Neutral, declarative.

**Required structure (single paragraph):**
1. What it is — author, form (article/dissertation/monograph), publisher or journal, year, length.
2. The argument — what the scholar claims, in one sentence.
3. Position in the field — first major X / contrarian Y / canonical reading of Z.

**Forbidden:** *important, seminal, essential, fascinating, magisterial.* Use what the work *does*, not how it makes you feel.

## page_summary
**Length:** 250–600 words.
**Tone:** Critical-reportorial. Attribute everything to the author or to named other scholars.

**Required sections (as paragraphs, no headers):**

1. **Bibliographic identity** — title, author affiliation, publication venue, date, length, series.
2. **Argument** — the thesis statement and the two or three main moves the scholar makes to defend it. Quote the thesis if recoverable. Distinguish argument from contents.
3. **Contributions to PKD studies** — explicit deliverables. Acceptable as named bullets in prose:
   - new readings of specific works (with the works named)
   - terms or concepts introduced
   - archives mined or primary sources recovered
   - corrections to prior scholarship (with the prior scholar named)
   - a methodological frame that subsequent scholars adopt
4. **Position in the literature** — who it builds on, who has contested it, where it sits in the academic and fan reception. This is where critical lineage registers.
5. **Caveats** — biases, dated assumptions, missing material, contested factual claims.

## Required JSON fields
- `card_summary` ✓
- `page_summary` ✓
- `linked_terms` — non-empty
- `works_discussed` — non-empty
- `people_mentioned` — non-empty (the scholars and figures the document cites or argues with)
- `evidentiary_lane` — `C`
- `source_reliability` — `secondary_scholarship`

## Lint checklist
- [ ] Names the thesis explicitly.
- [ ] Names at least three contributions.
- [ ] Names at least one prior scholar this work builds on or contests.
- [ ] Cross-links populated.
- [ ] No forbidden adjectives.
- [ ] Length within bounds.

## Worked example
See the rewritten Kim Stanley Robinson, *The Novels of Philip K. Dick* entry — the canonical demonstration of the target shape.
