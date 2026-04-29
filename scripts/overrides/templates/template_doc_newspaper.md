# Template — Newspaper Clippings

For: contemporary newspaper articles, reviews, obituaries, local news mentions.
Lane: **D** or **E** depending on whether PKD or someone else is reporting.

## card_summary
**Length:** 40–70 words. Clippings are short; their summaries should be too.

**Required structure:**
1. Publication, date, page.
2. Subject — what the clipping is about (a review, a local appearance, a marriage notice, a divorce filing, an obituary).
3. Significance to PKD studies — what specifically this clipping documents that scholars cite.

## page_summary
**Length:** 100–250 words. Clippings rarely warrant longer.

**Required sections:**

1. **Bibliographic identity** — publication, date, section, page, byline.
2. **Contents** — what the article reports.
3. **Documentary value** — what this clipping evidences: a publication date, a residence, a personal event, a contemporary review's reception, etc. Anchor to the specific biographical or bibliographic claim it supports.
4. **Cross-references** — biography events corroborated, named people, named works.

## Required JSON fields
- `category` — `newspaper`
- `date_display` — exact date
- `evidentiary_lane` — `E` (contemporary record)

## Editorial principle
Clippings are evidentiary, not interpretive. Their summary should answer: "what biography event or work-publication does this corroborate?"

## Lint checklist
- [ ] Exact date.
- [ ] Documentary anchor named.
- [ ] Cross-links to specific biography events.
- [ ] Length within bounds.
