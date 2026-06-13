# Template - Canonical Works Catalog

For: canonical work records in the separate works table, including novels, stories, letters, interviews, essays, and other PKD-authored publications.

## Writing standard

Each work entry should read like a concise academic encyclopedia record. State what the work is, where it belongs in PKD's corpus, why it matters, and what the principal evidence and linked documents show. Use specific publication details and source links rather than generic praise.

## card_summary
**Length:** 60-100 words.

**Required structure:**
1. Title and bibliographic identity.
2. Why the work matters in PKD's corpus.
3. The most important relation to other entries: source count, work type, or canonical context.

## page_summary
**Length:** 250-600 words.

**Required sections:**

1. **Bibliographic identity** - title, author, date, edition or publication context, and work type.
2. **Corpus position** - where the work sits in PKD's career or publication history.
3. **Evidence and linkage** - what archive documents, related works, or people connect to this record.
4. **Interpretive note** - one or two sentences on what researchers use the work for.

## Required JSON fields
- `work_id`
- `canonical_title`
- `slug`
- `author`
- `work_type`
- `category`
- `card_summary`
- `page_summary`
- `source_count`
- `related_docs`

## Lint checklist
- [ ] Card and page both present.
- [ ] Title and corpus context are specific.
- [ ] Links back to related archive documents.
- [ ] Tone is restrained and scholarly.
