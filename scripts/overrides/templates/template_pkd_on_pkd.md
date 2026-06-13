# Template — PKD on PKD Novel Mention Catalog

For: one entry per PKD novel, summarizing and linking all detected mentions in PKD-authored primary writings.

## Writing standard

Write each entry as an academic encyclopedia entry. State the novel's place in PKD's oeuvre, then synthesize what PKD says about it across letters, interviews, the Exegesis, and other writings. The prose should name the specific source documents, the recurring concerns or interpretations, and any major shifts over time. Avoid generic catalog language; each entry should read as a concise scholarly digest of PKD's self-commentary on that novel.

## card_summary
**Length:** 60–90 words.

**Required structure:**
1. Novel title and brief identification.
2. Total detected mentions and source-document count.
3. The main source mix: letters, interviews, Exegesis, essays, speeches, or other primary writings.
4. One sentence explaining what kind of page the detail view opens.

## page_summary
**Length:** 200–450 words.

**Required sections:**

1. **Catalog note** — explain that this page gathers PKD's own mentions of the novel across primary writings.
2. **Source breakdown** — name the main document types and the kinds of PKD writing represented.
3. **Keyword pattern** — describe recurring contextual language if the extraction script finds it.
4. **How to browse it** — explain that each source document is listed with excerpts and links back to the archive.
5. **Interpretive pattern** — summarize what PKD's remarks collectively suggest, but attribute that synthesis to the catalog rather than to PKD as fact.

## Required JSON fields
- `work_id`
- `canonical_title`
- `slug`
- `mention_count`
- `source_doc_count`
- `source_doc_types`
- `card_summary`
- `page_summary`
- `top_sources`
- `source_documents` on the detail page export
- `mentions` on the detail page export

## Lint checklist
- [ ] Card states the source mix and total mention count.
- [ ] Page summary explains the catalog's scope.
- [ ] Source documents are grouped and linked.
- [ ] Excerpts are present and readable.
- [ ] Entry reads as a scholarly synthesis of PKD's self-commentary.
