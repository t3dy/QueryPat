# Content Plan v3 — Writing, Structure, and Coverage

This plan succeeds [IMPROVEMENT_PLAN.md](IMPROVEMENT_PLAN.md) (v2.0, completed). It is governed by the editorial frame in [PKDontology.md](PKDontology.md). Where v2 was about populating tables and cross-links, v3 is about **writing quality, scholarly density, and the templates that enforce both**.

The four deliverables this plan funds:
1. **Style guides and templates** — one per content type (§3)
2. **Scholar profile expansion** — turn empty Tier 4 entries into real interpretive contributions (§4)
3. **Document summary rewrite** — every summary captures "all key contributions" both academic and fan (§5)
4. **Coverage expansion** — close the gaps the ontology identifies (§6)

---

## 1. Why v3

The v2.0 enrichment populated structure: 302 accepted terms, 246 lane-tagged docs, 790 cross-links. The portal now has the right *shape*. What it lacks is **prose density**:

- 76 of 105 scholars have empty `interpretive_stance` and "1 document(s) in the archive" as their entire `relevance` field. Among them: Kim Stanley Robinson, Peter Fitting, Istvan Csicsery-Ronay Jr., Fredric Jameson — scholars whose contributions to PKD studies are foundational.
- Many `card_summary` and `page_summary` fields tell you what a document *is* (publisher, page count, author affiliation) but not what it **contributes** — the arguments it makes, the terms it coins, the controversies it settles or starts.
- There is no published style guide. Every writer (human or LLM) reinvents the rubric.
- There is no editorial frame distinguishing what to record (the ontology) from what not to record.

v3 fixes these.

---

## 2. Editorial principles (from the ontology)

Every entry written under v3 must:

1. **State its lane.** A scholar profile is C; a biography summary is D; an interview citation is E.
2. **Attribute interpretations.** No claim that PKD "really" meant something — always whose reading.
3. **Surface contradictions.** When the literature disagrees, say so.
4. **Cross-link six ways.** Per ontology §6: terms, events, documents, segments, names, works.
5. **Distinguish fact from self-report.** Lane B (Exegesis) is autobiography by an unreliable narrator; treat it as such.

These are non-negotiable and enforceable by editorial review. The style guides in §3 build them in by structure.

---

## 3. Style guides and templates

Each content type gets a template file in `scripts/overrides/templates/`. The template is both prose ruleset and JSON skeleton.

### 3.1 Document summary template (archive docs)

**Card summary** — 60–90 words, single paragraph. Structure:
- Sentence 1: What it is (form, author, publisher, year, length).
- Sentence 2–3: What it covers — the contribution, not the contents. Use verbs like *argues, introduces, contests, surveys, anthologizes, documents*.
- Sentence 4 (optional): Position relative to the field — "first major academic study," "contrarian rebuttal to Sutin," etc.

**Page summary** — 250–600 words. Required sections (as paragraphs, not headers):
1. **Bibliographic identity** — what, who, when, format, length, publisher, series if any.
2. **Argument or contents** — what the document actually says or claims. For scholarship: thesis statement + main moves. For biography: what it covers and how. For fan publication: editor, contributors, regular features. For primary source: the occasion, the audience, the throughline.
3. **Contributions to PKD studies** — the explicit deliverable. Bullet-acceptable here. New terms introduced? Disputed claims advanced? Archives mined? Interpretive frames offered? Translations or recovery? Naming a scholar's specific moves rather than vague praise.
4. **Position in the literature** — who agrees, who pushes back, what it builds on, what it provokes. This is where "academic and fan" reception both register.
5. **Caveats** — biases, missing material, dated assumptions, contested claims.
6. **Cross-references** — explicit linked terms, named scholars, related documents, key segments.

**The "all key contributions" test:** A reader finishing the page summary should be able to state in one sentence why this document is in the archive at all. If they cannot, the summary failed.

Sub-templates per category:
- `template_doc_scholarship.md` — academic articles, dissertations, monographs
- `template_doc_biography.md` — full biographies and memoirs
- `template_doc_interview.md` — single interviews and interview compilations
- `template_doc_primary.md` — PKD's own works (essays, letters, speeches, novels)
- `template_doc_fan.md` — fanzines, fan-press monographs, convention publications
- `template_doc_newspaper.md` — clippings (handle differently — short, location-anchored)
- `template_doc_finding_aid.md` — archives, special collections
- `template_doc_thesis.md` — graduate theses

### 3.2 Scholar profile template

The current schema has `role`, `tier`, `key_works`, `interpretive_stance`, `relevance`. This is enough scaffolding; what it needs is body. Required fields after rewrite:

- **role** (one phrase, ≤6 words) — *Marxist science-fiction critic, 1980s*; *Editor of the Exegesis (2011)*; *Italian Dickian, formal-constraint reading*.
- **tier** (1–5, retain) — but document the criteria (see §4).
- **affiliation** (institution + period, where known)
- **interpretive_stance** (120–250 words) — Required structure:
  1. The scholar's central claim about PKD (one sentence).
  2. Their methodological frame (Marxist, psychoanalytic, postmodern, biographical, theological, formalist, ideological-critique, etc.).
  3. The specific moves they make — concepts they introduced, readings they originated, errors they corrected.
  4. How they position against earlier scholars.
- **relevance** (60–120 words) — Why a researcher consults them: what classes of question this scholar answers.
- **quotable_lines** (2–5 short quotes) — *new field*; the lines later scholars cite. Source-tagged.
- **scholarly_lineage** (free text, optional) — *new field*; who they descend from intellectually (Suvin → Freedman; Jameson → Palmer), who they trained, who responded.
- **disputes** (array of {opponent, issue}) — *new field*; the documented disagreements with other scholars.
- **key_arguments** (3–7 bullets) — *new field*; numbered moves. *e.g., "Argues *Ubik* is the canonical text for reading PKD's ontology"; "Reads 2-3-74 as compositionally generative regardless of veridical status"*.

### 3.3 Dictionary entry template (refinement of current)

Current accepted terms have `card_description` (1–2 sentences) and a partial `full_description`. Standardize:

- **card_description** (≤40 words) — ostensive: what the term denotes, in plain terms. No PKD context.
- **full_description** (500–1500 words) — Required sections:
  1. **Etymology and tradition** — the term's history before PKD.
  2. **PKD's usage** — how he transforms it; first appearance, peak usage, span of years.
  3. **Key passages** — 2–4 segment citations with brief gloss.
  4. **Related terms** — explicit graph (parent/child/synonym/contrast).
  5. **Scholarly engagements** — who has written on this term and what they argued.
  6. **Editorial caution** — common misreadings, contested usages.

For *bespoke* terms (VALIS, Zebra, homoplasmate), section 1 becomes *"Coinage and first appearance"*.

### 3.4 Biography event template

Already implemented in `curated.json` schema; tighten the writing rules:

- **event** field — one sentence, declarative, neutral voice, no interpretive verbs (*"believed", "feared", "decided"* — bad; *"wrote", "moved", "married", "reported"* — fine).
- **notes** — must surface contradictions. Required when reliability ≠ confirmed.
- **source** — never blank; named scholar/work.

### 3.5 Segment summary template

Current parsed-summary fields are good but uneven. Standardize:

- **concise_summary** (2–3 sentences): date context + main topic + key claim.
- **key_claims** — bullet list of theological/philosophical assertions PKD makes here.
- **recurring_concepts** — canonical term names only (must match Dictionary entries; this is what enforces cross-linking).

---

## 4. Scholar profile expansion

### 4.1 Tier criteria (currently undefined; document them)
- **Tier 1** — Major biographers and primary editors of PKD's writings (Sutin, Anne Dick, Rickman, Arnold, Peake, Jackson/Lethem, Tessa Dick).
- **Tier 2** — Academic scholars with substantial single-author monographs or multiple landmark articles (Robinson, Butler, Palmer, Freedman, Rossi, Burton, Fitting, Suvin, Jameson, Csicsery-Ronay, Kucukalic, Vest, Dunst).
- **Tier 3** — Editors of collections, finding-aid curators, archive maintainers (Sandner, Sullivan, CSUF Special Collections).
- **Tier 4** — Single-article contributors, fan critics with limited but real contributions (most current Tier-4 entries; many should move up to 2 or down to 5).
- **Tier 5** — Media sources, peripheral mentions, journalists.

This is a re-tiering pass, not just a content pass. Robinson (currently Tier 4) → Tier 2. Fitting → Tier 2. Csicsery-Ronay → Tier 2. Several genuine Tier 5s currently sit in Tier 4.

### 4.2 Priority scholar writeups (initial wave of 25)

The scholars most urgently needing real `interpretive_stance` writeups, with the headline contribution each profile must articulate:

| Scholar | Current tier | Target tier | Headline contribution |
|---------|--------------|-------------|------------------------|
| Kim Stanley Robinson | 4 | 2 | First academic monograph (1984); reads PKD's novels as a unified body of work; argues *Ubik* is the apex |
| Peter Fitting | 4 | 2 | "Reality as Ideological Construct" (1983); marxist/Althusserian reading of five novels |
| Umberto Rossi | 2 | 2 (expand) | *The Twisted Worlds of PKD*; reads PKD through "ontological uncertainty"; major Italian critic |
| Christopher Palmer | (in DB) | 2 | *Exhilaration and Terror of the Postmodern* (2003); postmodernist reading; central to current academic consensus |
| Carl Freedman | (in DB) | 2 | Suvinian critical theorist; reads PKD as central to SF's cognitive estrangement project |
| Andrew M. Butler | (in DB) | 1/2 | Pocket Essentials *PKD* + scholarly articles; entry-point reference for UK academic readers |
| Fredric Jameson | (in DB) | 2 | *Archaeologies of the Future*; PKD as exemplar of postmodern utopia/dystopia collapse |
| Istvan Csicsery-Ronay Jr. | (check) | 2 | *The Seven Beauties of Science Fiction*; theoretical framework deployed across PKD studies |
| Darko Suvin | (in DB) | 2 | Cognitive estrangement; Marxist-formalist reading; foundational SF theorist who critiqued PKD |
| James Burton | (in DB) | 2 | *Philosophy of Science Fiction* (Bergson/Dick); reads PKD via Bergsonian time-philosophy |
| Stanislaw Lem | (in DB) | 2 | "PKD: A Visionary Among the Charlatans" (1972); the most consequential single critical essay |
| Jonathan Lethem & Pamela Jackson | (in DB) | 1 | Editors of *The Exegesis of Philip K. Dick* (2011); the editorial achievement that made post-2011 study possible |
| Lawrence Sutin | 1 | 1 (expand) | *Divine Invasions*; the canonical biography; also editor of *In Pursuit of VALIS* and *Shifting Realities* |
| Kyle Arnold | 1 | 1 (expand) | *The Divine Madness*; psychobiographical reading; clinical frame for 2-3-74 |
| Anne R. Dick | 1 | 1 (expand) | *Search for PKD*; ex-spouse memoir; corroborates and contradicts Sutin |
| Gregg Rickman | 1 | 1 (expand) | *PKD: In His Own Words* + *PKD: The Last Testament*; long-form interview record |
| Anthony Peake | 1 | 1 (expand) | *A Life of Philip K. Dick*; recent comprehensive biography from a paranormal-studies frame |
| Tessa B. Dick | 1 | 1 (expand) | Memoirs and *Conversations with PKD*; primary witness to the late period |
| David Lapoujade | (check) | 2 | *Worlds Built to Fall Apart*; Deleuzean reading |
| Jeffrey J. Kripal | (in DB) | 2 | *Esalen* and related work; situates PKD in American esoteric/visionary tradition |
| Gabriel McKee | (in DB) | 2 | *Pink Beams of Light from the God in the Gutter*; theological reading |
| Lorenzo DiTommaso | (in DB) | 2 | Apocalyptic-studies reading of PKD's late theology |
| Bruce Gillespie | (in DB) | 2/3 | Australian critic; *Philip K. Dick: Electric Shepherd* (1975); foundational fan-academic hybrid |
| Norman Spinrad | (in DB) | 2/3 | "Transmogrification of PKD" essay; novelist-critic perspective; also memoirist |
| Frank Hollander | (in DB) | 3 | PKD Otaku editor; the central long-running fan-press venue post-2002 |

Each profile should be 250–400 words structured per §3.2.

### 4.3 Scholars not currently in the database to consider adding

(These are referenced in the literature but I have not yet confirmed presence in `scholars.json`; an audit pass is part of the work.)

- Patricia Warrick — *Mind in Motion: The Fiction of Philip K. Dick* (1987); first major thematic study
- Hazel Pierce — *Philip K. Dick* (Starmont, 1982); early reference work
- Douglas Mackey — *Philip K. Dick* (Twayne, 1988)
- Samuel J. Umland — editor, *PKD: Contemporary Critical Interpretations* (1995)
- Roger Zelazny — wrote the foreword to *A Maze of Death*; correspondent
- Erik Davis — *TechGnosis*; situates PKD in the "Californian visionary" lineage
- Simon Critchley — *How to Stop Living and Start Worrying*; philosophical engagement with PKD
- Slavoj Žižek — has written and lectured on PKD across many books
- Gilles Deleuze — *Anti-Oedipus* / *Difference and Repetition* — invoked PKD in passing but consequentially for later French readings
- Jean Baudrillard — wrote on simulacra with PKD as exemplar
- Roberto Casati — Italian philosopher on PKD's ontology
- N. Katherine Hayles — *How We Became Posthuman*; PKD as case study
- Scott Bukatman — *Terminal Identity*; cyberpunk frame retroactively reading PKD
- Veronica Hollinger — feminist SF criticism; PKD readings
- Brian Attebery — strategy of fantasy / SF poetics; PKD chapters
- Lance Olsen — *PKD: A Reader's Companion* (1995)

Audit which are present and add stubs for those that are not.

---

## 5. Document summary rewrite

### 5.1 Triage the 228 documents

For each document in the archive, classify by current summary quality:

- **Adequate** — passes the "all key contributions" test (§3.1). Light copy-edit only.
- **Thin** — names the document but doesn't articulate contributions. Rewrite.
- **Hedging** — uses extracted text or LLM filler that doesn't actually say anything. Rewrite from scratch.
- **Wrong** — factual error or misattribution. Rewrite + audit.

Initial estimate from inspection: ~40% adequate, ~40% thin, ~15% hedging, ~5% wrong. Rewrite target: roughly 130 documents.

### 5.2 Priority order

1. **Tier-1 biographies** (7 documents) — these set the factual baseline; their summaries are referenced from many other entries.
2. **Major academic monographs** (Robinson, Palmer, Freedman, Rossi, Butler, Sutin's edited works, the Lethem/Jackson Exegesis) — heavy cross-link receivers.
3. **PKD's own works** (lane A primary) — fiction novels and stories. Each summary must articulate themes, vocabulary debuted, composition history where known.
4. **Lane E primaries** — letters, interviews, speeches.
5. **Science Fiction Studies articles** — the dense academic vein (~30 docs).
6. **Fan publications** — Niekas, SFC, PKD Otaku, Journey Planet. Per-issue table of contents where extractable.
7. **Newspaper clippings** — short, location-anchored summaries.
8. **Finding aids** — describe holdings, link to archive.

### 5.3 Sample rewrite — Robinson's *The Novels of Philip K. Dick* (1984)

The current summary is decent but does not articulate **what Robinson argues**. Target rewrite:

> Kim Stanley Robinson's doctoral dissertation, published in 1984 by UMI Research Press as no. 9 in the *Studies in Speculative Fiction* series. The first sustained academic monograph on Dick's fiction.
>
> Robinson treats the novels as a unified body of work and reads them developmentally. His central argument is that Dick's mature fiction works through a problem of ontological instability — the novels stage a world whose reality status cannot be settled — and that this trajectory culminates in *Ubik*, which Robinson positions as the apex of the achievement and the formal solution to a problem the earlier novels could only pose. The post-1974 fiction (*A Scanner Darkly*, the VALIS trilogy) Robinson reads as a partial retreat from that achievement, a move toward more openly autobiographical material that he treats with respect but at some critical distance.
>
> Contributions to PKD studies: (1) the first sustained novel-by-novel academic reading; (2) the canonical case for *Ubik* as Dick's central novel — a position now common but originated here; (3) a developmental rather than thematic critical method that has shaped subsequent monograph-form criticism (Palmer, Freedman, Rossi all answer to this template); (4) the establishment that Dick deserves the same close-reading attention as a literary novelist.
>
> Position in the literature: written before Sutin's biography (1989) and Anne Dick's memoir (1995), so without the biographical apparatus that subsequent critics had access to. Later scholars have qualified the *Ubik*-apex thesis (Palmer's postmodern frame, Rossi's ontological-uncertainty frame, Freedman's Marxist frame each redistribute weight). The book retains foundational status because of its priority and its critical clarity.
>
> Robinson went on to a distinguished career as a science-fiction novelist (*Mars* trilogy, *The Ministry for the Future*); the dissertation precedes that fiction work and stands on its own as criticism.

This is the target shape. ~330 words, named contributions, lineage articulated, no filler.

### 5.4 Process

- Build a worksheet (one row per document) with: current summary length, triage class, priority, status.
- Rewrite in batches of 10–15, grouped by author/topic to maintain consistency.
- Each rewrite must update `card_summary` and `page_summary` *and* populate `linked_terms`, `works_discussed`, `people_mentioned` per ontology §6.

---

## 6. Coverage expansion

### 6.1 New entity types
Per ontology §8:

- **Visions / mystical events** — extract as discrete entities. Initial set: the Pink Beam, the AI Voice, the dream of the magazine, the Black Iron Prison, the homoplasmate revelation, Tagore, the Christmas 1980 events.
- **Themes** — top-level entity table. Initial set per ontology §2.6.
- **Adaptations** — top-level table. Initial set: *Blade Runner*, *Total Recall*, *Minority Report*, *A Scanner Darkly*, *Paycheck*, *Next*, *The Adjustment Bureau*, *Radio Free Albemuth*, *The Man in the High Castle* (Amazon), *Electric Dreams* (anthology), *Counter-Clock World* (announced).
- **Contradiction registry** — top-level entity per ontology §4.

### 6.2 Dictionary expansion targets
- 50 accepted → 302 already shipped. Next pushes:
  - Promote terms with ≥10 segment links from provisional to accepted, with full descriptions written
  - Sweep 601 background for genuine theological/philosophical terms wrongly demoted
  - Add missing bespoke terms: *Tagore*, *St. Sophia is going to be born again*, *fish* (Christian symbol use), *ditheon*, *plasmate*, *Acts*, *the Bardo Thodol* (PKD's invocation specifically)

### 6.3 Biography event expansion
- Deep-extract from Tier-1 biographies (Sutin, Anne Dick, Rickman) — target 1500+ events from current 646
- Each extracted event must hit the §3.4 template
- Cross-source flag where two biographies report the same event differently

### 6.4 Segment summary gap-fill
- 900 of 1107 segments lack parsed summaries. Closing this is the largest single coverage push and depends on raw chunk text access.

---

## 7. Implementation order

Aligned with effort and dependency:

1. **Templates committed** (§3) — half-day. Unblocks everything downstream.
2. **Re-tier the scholars** (§4.1) and write the 25 priority profiles (§4.2). 1–2 weeks of focused writing.
3. **Document rewrite — Tier-1 biographies + major monographs** (§5.2 priorities 1–2). ~30 documents.
4. **Theme entity table + initial 20 themes** (§6.1).
5. **Vision-event entity table + initial 10 visions** (§6.1).
6. **Document rewrite — primaries + interviews + SFS articles** (§5.2 priorities 3–5).
7. **Dictionary deepening** (§6.2).
8. **Document rewrite — fan publications + newspapers + finding aids** (§5.2 priorities 6–8).
9. **Biography deep extraction** (§6.3).
10. **Segment gap-fill** (§6.4, longest tail).

---

## 8. Quality assurance

Three checks at minimum, all enforceable in CI:

1. **Lint pass** — every new entry validates against its template's required sections. Missing sections fail the build.
2. **Cross-link audit** — every document summary's `linked_terms` and `people_mentioned` arrays must be non-empty for scholarship-class documents. Term names must resolve in the dictionary.
3. **Editorial sample review** — random 5% of new entries get a human read-through against ontology §5 (fact-vs-interpretation) and §4 (contradiction surfacing).

---

## 9. What this plan does not address

Out of scope for v3 (deferred):

- Graph view / visualization (in [DESIGN_STUDY.md](DESIGN_STUDY.md))
- Search ranking improvements
- Multi-language coverage (Italian, French criticism in original language)
- AIPSY blueprint execution (separate document)
- Site UI redesign

These wait until v3's writing-quality baseline is in place.
