# Style Guide Templates

Editorial templates for content written into the QueryPat database. Governed by [PKDontology.md](../../../PKDontology.md) and [CONTENT_PLAN_V3.md](../../../CONTENT_PLAN_V3.md).

Every template encodes a required structure, a target length, a tone rule, and a non-negotiables list. New entries that fail the template's lint check should not ship.

## Templates

| Template | Use for |
|----------|---------|
| [template_doc_scholarship.md](template_doc_scholarship.md) | Academic articles, dissertations, monographs |
| [template_doc_biography.md](template_doc_biography.md) | Full biographies, memoirs, psychobiographies |
| [template_doc_interview.md](template_doc_interview.md) | Interviews and interview compilations |
| [template_doc_primary.md](template_doc_primary.md) | PKD's own works (essays, letters, speeches, novels, stories) |
| [template_doc_fan.md](template_doc_fan.md) | Fanzines, fan-press monographs, convention publications |
| [template_doc_newspaper.md](template_doc_newspaper.md) | Newspaper clippings and short journalism |
| [template_doc_finding_aid.md](template_doc_finding_aid.md) | Archive finding aids and special-collections inventories |
| [template_scholar.md](template_scholar.md) | Scholar profile entries in scholars.json |
| [template_dictionary.md](template_dictionary.md) | Dictionary term entries |
| [template_biography_event.md](template_biography_event.md) | Biography event entries in curated.json |

## Cross-cutting rules

These apply to every entry:

1. **State the lane.** Per ontology §3, every claim is sourced to a lane (A: Fiction, B: Exegesis, C: Scholarship, D: Synthesis, E: Primary).
2. **Attribute interpretations.** Per ontology §5, no claim that PKD "really" meant X — always whose reading.
3. **Surface contradictions.** Per ontology §4, when sources disagree, name the disagreement.
4. **Cross-link six ways.** Per ontology §6: terms, events, documents, segments, names, works.
5. **Distinguish fact from self-report.** Lane B is autobiography by an unreliable narrator.
6. **No filler.** Don't pad with publisher boilerplate, page-count rehearsal, or "this important work."
7. **Verbs not adjectives.** *argues, introduces, contests, surveys, anthologizes, documents* — not *important, fascinating, seminal, essential*.
