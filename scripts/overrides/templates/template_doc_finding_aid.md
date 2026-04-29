# Template — Finding Aids and Special Collections Inventories

For: institutional finding aids (CSUF, Harvard, etc.), archive inventories, manuscript catalogs.
Lane: **E** (Primary, since they describe primary holdings).

## card_summary
**Length:** 60–90 words.

**Required structure:**
1. Institution, collection name, finding aid date.
2. Holdings summary — what kinds of materials, how many boxes / linear feet.
3. Access conditions and significance — what this collection holds that no other holds.

## page_summary
**Length:** 200–400 words.

**Required sections:**

1. **Institutional identity** — institution, collection title, repository, finding-aid date and version.
2. **Holdings** — what's there: manuscripts, drafts, correspondence, photographs, audio, ephemera. Box count, linear feet, date range covered.
3. **Origin and provenance** — how the collection came to the institution, donor, acquisition history.
4. **Notable items** — drafts of specific novels, particular correspondence, marked-up books, the Exegesis folders themselves. Be specific.
5. **Access and citation** — how researchers access the materials, citation format the institution requests.
6. **What it enables** — what research questions this collection uniquely answers. Cross-link to the scholars who have used it.

## Required JSON fields
- `category` — `finding_aids` or `archives`
- `evidentiary_lane` — `E`
- `source_reliability` — `archival_finding_aid`

## Editorial principle
Finding aids are pointers to physical materials. The summary's job is to tell a researcher *what they will find at the institution* and *what kinds of work that material supports*. Don't paraphrase the finding aid; orient the reader to it.

## Lint checklist
- [ ] Institution and collection title named.
- [ ] Holdings quantified (boxes, linear feet, item count).
- [ ] Notable items named specifically.
- [ ] Access and citation noted.
- [ ] Cross-links to scholars who have published using this collection.
