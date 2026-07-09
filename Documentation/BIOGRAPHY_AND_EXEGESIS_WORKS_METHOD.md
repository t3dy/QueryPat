# Biographical Timeline & "Works in the Exegesis" — Template, Method, and Spec

*Status: authored 2026-07-08. Governs two related bodies of writing: (A) the curated biographical timeline (`site/public/data/biography/curated.json`, rendered by `site/src/pages/Biography.tsx`), and (B) the new "Works in the Exegesis" pages (`site/public/data/exegesis/works/`, to be rendered under `/exegesis/works`).*

This document defines **what a good entry looks like**, **how to research and source it**, and **the data contracts** so the work is repeatable and reviewable. It inherits the five-lane evidentiary scheme and the contradiction-surfacing discipline from [PKDontology.md](../PKDontology.md); it does not re-derive them.

---

## 0. The five lanes (recap)

Every claim is tagged to the lane of its strongest available evidence. Lanes are surfaced, never collapsed.

| Lane | Source class | Epistemic status |
|---|---|---|
| **A** | The fiction | What the text says; never inferred to biography. |
| **B** | The Exegesis | PKD theorizing about himself — an unreliable narrator's account of his own unreliability. |
| **C** | Scholarship | Sutin, Anne Dick, Arnold, Peake, academic articles. Contested; cite the disputant. |
| **D** | Synthesis biography | The portal's own reconstruction from multiple sources. |
| **E** | Letters & interviews | PKD under his own signature, in real time. Closest to primary, still self-report. |

---

## PART A — The Biographical Timeline

### A.1 What is wrong with the current entry

The current `curated.json` entry is a **single declarative sentence with a single source string**:

```json
{
  "id": "pkd_bio_1974_fish_sign_arnold",
  "date": "1974-02",
  "event": "Arnold reconstructs the doorstep pharmacy delivery in which a dark-haired woman wearing a gold fish pendant triggered the fish-sign anamnesis at the start of 2-3-74.",
  "source": "Arnold, The Divine Madness of Philip K. Dick",
  "importance": 5,
  "notes": "Arnold compares Dick's account with Tessa Dick's account and flags discrepancies..."
}
```

Three problems:
1. **One source, one voice.** The 2-3-74 doorstep scene is attested in Sutin, in Arnold, in PKD's own letters, and in the Exegesis — and they *disagree*. A single `source: "Arnold"` erases the triangulation that is the whole point.
2. **No prose.** A sentence is an index card, not writing. The timeline should *read*, not just list.
3. **Disagreement is demoted to a `notes` aside** instead of being structurally surfaced the way the ontology requires.

### A.2 The improved entry schema (a back-compatible superset)

Keep every existing field (the renderer and filters depend on them). **Add** the following optional fields. An entry that omits them renders exactly as today; an entry that includes them renders richer.

```jsonc
{
  // ── existing fields (unchanged) ──
  "id": "pkd_bio_1974_02_fish_sign",
  "date": "1974-02",
  "date_precision": "month",        // day | month | season | year | circa
  "event": "…",                     // NOW: a one-line HEADLINE (≤ ~25 words)
  "category": "paranormal_experience",
  "entities": ["Tessa Dick", "Fish Sign", "2-3-74"],
  "location": "Fullerton, California",
  "importance": 5,                  // 1–5
  "notes": "…",                     // optional short curatorial aside
  "theophany_id": null, "theophany_slug": null,

  // ── new fields ──
  "narrative": "One–three short paragraphs of synthesized prose. This is the writing. It tells what happened, whose account we are following, and where the accounts diverge. Verbs over adjectives; no vague praise; distinguish fact from self-report.",
  "sources": [
    { "author": "Sutin",  "work": "Divine Invasions",             "lane": "C", "locator": "ch. 8", "supports": "the delivery occurred; dates it late Feb 1974" },
    { "author": "Arnold", "work": "The Divine Madness of PKD",     "lane": "C", "locator": "ch. 1", "supports": "reconstructs the fish-pendant recognition; flags Tessa discrepancy" },
    { "author": "PKD",    "work": "Selected Letters",              "lane": "E", "locator": "SL 1974", "supports": "PKD's own contemporaneous framing" },
    { "author": "PKD",    "work": "Exegesis",                      "lane": "B", "locator": "[4:x]",   "supports": "later theological reading of the same scene" }
  ],
  "lanes": ["B", "C", "E"],         // union of the lanes present (drives badges)
  "dispute": {                       // OPTIONAL — only when sources genuinely conflict
    "summary": "The identity of the delivery woman and the exactness of the fish-pendant recognition differ across accounts.",
    "positions": [
      { "who": "PKD (Exegesis/letters)", "claim": "the golden fish necklace triggered anamnesis on the spot" },
      { "who": "Tessa Dick (per Arnold)", "claim": "recalls the encounter differently; recognition was less immediate" }
    ]
  },
  "quotes": [                        // OPTIONAL — verbatim ONLY from full-text corpus (Exegesis, Letters)
    { "text": "…", "speaker": "PKD", "source": "Exegesis [4:x]", "lane": "B" }
  ],
  "links": {                         // OPTIONAL — cross-references that resolve on-site
    "people": ["/dictionary/tessa-dick"],
    "works": ["/works/flow-my-tears-the-policeman-said"],
    "exegesis_work": "/exegesis/works/ubik",
    "theophany": "/theophanies/…"
  },
  "confidence": "medium"            // high | medium | low — of the synthesized reconstruction
}
```

**Field rules**
- `event` is now the **headline**, not the whole story. Move the substance into `narrative`.
- `sources[]` replaces the informational role of `source`; keep the old `source` string set to the *primary* source for back-compat until the renderer is updated (then it can be derived from `sources[0]`).
- `lane` on each source is mandatory once `sources[]` is present.
- `dispute` is included **only** when accounts conflict. When present, the renderer must show it prominently (not as a footnote).
- `quotes[].text` may be verbatim **only** if drawn from a full-text corpus source (Exegesis, Letters). Never invent a verbatim quote for Sutin/Anne Dick/Arnold — see A.3.

### A.3 The research method (source by source)

The corpus contains **full text** for two source classes and **summaries only** for the secondary biographies. This asymmetry governs how each may be used.

| Source | In-repo location | Full text? | How to use |
|---|---|---|---|
| **Exegesis** | `exegesis_ordered.txt` (9 MB), `exegesis_entries_analysis.json` (860 analyzed entries) | **Yes** | Quote verbatim (Lane B). Cite folder:page. This is where PKD reinterprets his own life theologically. |
| **Selected Letters** | `selected_letters_analysis.json`, segmented; concordance in `BIO_SOURCE_SEARCH_REPORT.md` | **Yes (segmented)** | Quote verbatim (Lane E). Use the concordance to *find* where a person/place/topic is discussed, then read the segment. |
| **Sutin — Divine Invasions** | `archive/docs/divine-invasions-…json` | **No — `page_summary` only (~1.4 KB)** | Paraphrase and cite (Lane C). Draw factual chronology from the summary + well-attested scholarship. **Do not fabricate verbatim quotes.** |
| **Anne R. Dick — The Search** | `archive/docs/oceanofpdf-…the-search-…json`, `…utopian-studies-…` | **No — summary only** | Paraphrase and cite (Lane C). Her value is the **Point Reyes marriage (1959–65)** and her disputes with Sutin's chronology. |
| **Arnold — The Divine Madness** | `archive/docs/arnold-…json`, `oceanofpdf-…divine-madness…` | **No — summary only** | Paraphrase and cite (Lane C). His value is the **clinical multi-causal frame** (Jane's death, the break-in, temporal-lobe substrate). |
| **Interviews** | archive docs (e.g. Rolling Stone 1974, "How to Build a Universe") | Varies | Quote where full text exists; else paraphrase and cite. Lane E when PKD speaks in his own voice. |

**Procedure for one entry**
1. **Anchor the fact.** Establish the event and date from the most reliable available lane (usually Sutin/Arnold chronology, Lane C, or a dated letter, Lane E).
2. **Triangulate.** Search the concordance (`BIO_SOURCE_SEARCH_REPORT.md`) and `exegesis_entries_analysis.json` for the same event across sources. Record each in `sources[]` with its lane and what it *supports*.
3. **Detect conflict.** If two sources disagree on date, cause, or identity, populate `dispute` — do not silently pick a winner. The known standing disputes (Anne Dick vs. Sutin drug chronology; the Nov 1971 break-in; the Vancouver episode) must always surface.
4. **Quote with discipline.** Pull verbatim only from Exegesis/Letters. For secondary biographies, paraphrase and cite.
5. **Write the narrative.** 1–3 short paragraphs. Name whose account is being followed. Distinguish what happened (Lane C/E) from what PKD later theorized it *meant* (Lane B).
6. **Cross-link.** Populate `links` to people (`/dictionary`), works (`/works` — only slugs that resolve), the matching `/exegesis/works/…` page, and any theophany.
7. **Set `confidence`** on the synthesis, and the `lanes` union.

### A.4 Writing rules (voice)

Inherited from the essay house style and PKDontology §5.4:
- Verbs over adjectives; no vague praise ("masterful," "brilliant").
- **State the lane.** "PKD wrote in the Exegesis that…" (B) is a different claim from "Sutin dates the delivery to…" (C).
- **Distinguish fact from self-report.** 2-3-74 is *what PKD experienced and theorized*, not *what was true*.
- **Surface contradictions** rather than resolving them.
- Link liberally, but only to routes that resolve.

### A.5 Coverage: where to add entries

Current: 192 curated entries, densest around 2-3-74. Under-covered, in priority order:
1. **Early life & apprenticeship (1928–1954):** Jane's death, the parents' divorce, Berkeley, University Radio / Art Music, the first marriages (Jeanette, Kleo), the mainstream-novel years.
2. **The Point Reyes / Anne Dick marriage (1958–1965):** the richest Anne Dick material; currently thin.
3. **The 1970–72 collapse:** the X-Kalay / Vancouver episode, the break-in, the move to Canada and back.
4. **The Orange County years (1972–1982):** the Fullerton/Santa Ana period, Doris Sauter, Joan Simpson, the last novels, the death.

---

## PART B — "Works in the Exegesis" Pages

### B.1 Goal

A robust page for **every novel or short story PKD discusses in the Exegesis**, each giving a summary and analysis of **every mention**, and the **theological use** he makes of the work. "Ubik in the Exegesis" is the model.

### B.2 What the Exegesis material actually is

`exegesis_entries_analysis.json` — **860 analyzed entries**, each: `entry_id`, `folder_page`, `date_range`, `summary`, `philosophical_claims[]`, `key_quotes[]`, `content_length`. Mention counts by work (from a curated pattern match — see B.4):

| Work | Mentions | Theological use (headline) |
|---|---:|---|
| **VALIS** | ~110 | The Exegesis *is* the theory VALIS dramatizes; hardest to separate life from fiction. |
| **Ubik** | ~65 | Ubik = the Atman / Holy Spirit; Runciter = the Logos addressing the living; half-life = our world; entropy = the withdrawal of time-force. |
| **A Scanner Darkly** | ~38 | The "fucked-up dopers" who "correctly understood the reality situation"; Substance D as the split self. |
| **The Three Stigmata of Palmer Eldritch** | ~33 | Chew-Z / Eldritch as the malign demiurge and false sacrament; the stigmata as anti-Christ. |
| **Flow My Tears** | ~19 | The alternate world as Acts-of-the-Apostles time; the anamnesis of Felix Buckman. |
| Long tail | 1–6 each | Time Out of Joint, A Maze of Death, Radio Free Albemuth, Martian Time-Slip, Galactic Pot-Healer, The Divine Invasion, Deus Irae, The Cosmic Puppets, Do Androids Dream. |

This is the seam: PKD read his own novels back as scripture. The pages make that legible.

### B.3 Data contract

**Index:** `site/public/data/exegesis/works/index.json`
```jsonc
{
  "generated": "2026-07-08",
  "source": "exegesis_entries_analysis.json (860 entries)",
  "works": [
    { "slug": "ubik", "title": "Ubik", "mention_count": 65, "date_range": "1974–1981",
      "theological_headline": "Ubik as the Atman/Holy Spirit; Runciter as the Logos." }
  ]
}
```

**Per work:** `site/public/data/exegesis/works/<slug>.json`
```jsonc
{
  "slug": "ubik",
  "title": "Ubik",
  "work_link": "/works/ubik",          // only if a canonical /works record exists; else null
  "mention_count": 65,
  "date_range": "1974–1981",
  "intro": "WRITTEN: 1–2 paragraphs framing how and why PKD returns to this novel in the Exegesis.",
  "theological_synthesis": "WRITTEN: the argument — what theological work the novel does across all mentions.",
  "mentions": [
    {
      "entry_id": "EXEGESIS_004_001",
      "folder_page": "[4:1]",
      "date_range": "1974–1976",
      "summary": "MACHINE-EXTRACTED verbatim/condensed from the analysis entry.",
      "quotes": ["verbatim key_quote(s) from the analysis entry"],
      "gloss": "WRITTEN: what PKD is doing with the novel in THIS passage, and its theological point."
    }
  ],
  "see_also": {
    "essays": ["/essays/exegesis-theophany"],
    "themes": ["/themes/reality-breakdown"],
    "dictionary": ["/dictionary/valis"]
  }
}
```

Split of labor: **extraction fills `mentions[].{entry_id,folder_page,date_range,summary,quotes}` and the counts; a human/careful pass writes `intro`, `theological_synthesis`, and each `gloss`.** The written fields are the deliverable; the extracted fields are the spine.

### B.4 Extraction discipline

- **Curated patterns, not naive substring.** `\btears\b` over-matches; `scanner` matches unrelated words. Use anchored, work-specific regexes and spot-check. Record the pattern used per work.
- **De-dup and order** mentions by `folder_page` then `entry_id`.
- **Preserve provenance:** every mention keeps its `entry_id`/`folder_page` so it is traceable to the Exegesis.
- **Log what's dropped:** if a work has mentions too glancing to gloss, say so in `intro` rather than silently omitting.

### B.5 Routing & UI

Add to `site/src/App.tsx`:
```
<Route path="exegesis/works" element={<ExegesisWorks />} />
<Route path="exegesis/works/:slug" element={<ExegesisWorkDetail />} />
```
- `ExegesisWorks` — index grid from `exegesis/works/index.json`, one card per work (title, mention count, theological headline).
- `ExegesisWorkDetail` — renders `intro` → `theological_synthesis` → the `mentions` list (each: folder:page chip, summary, quotes as blockquotes, written `gloss`) → `see_also`. Not dependent on a `/works/:slug` record existing (Scanner, Three Stigmata, Flow My Tears have none).
- Link the new index from the existing `/exegesis` page and from `/works` where a work record exists.

### B.6 Writing rules for the gloss/synthesis

- The `gloss` answers one question: **what theological use does PKD make of the novel in this passage?** Not a plot recap.
- Quote the Exegesis (Lane B) and mark it as PKD's self-reading, not doctrine.
- Where PKD's reading of his own novel changed over time, track the change across `mentions` (they're date-ordered).
- Cross-link to the fiction (Lane A) and to the theme/essay pages.

---

## Acceptance checklist (per deliverable)

**Biography entry**
- [ ] `event` is a ≤25-word headline; substance is in `narrative`.
- [ ] ≥2 `sources[]` where the event is multiply attested, each lane-tagged.
- [ ] `dispute` present iff sources genuinely conflict.
- [ ] Verbatim quotes only from Exegesis/Letters.
- [ ] `links` resolve on-site; `lanes` union set; `confidence` set.

**"X in Exegesis" page**
- [ ] Every non-glancing mention has an `entry_id`, `summary`, and written `gloss`.
- [ ] `intro` and `theological_synthesis` written, lane-marked.
- [ ] Extraction pattern recorded; dropped/glancing mentions acknowledged.
- [ ] `see_also` resolves; `work_link` null if no canonical record.
