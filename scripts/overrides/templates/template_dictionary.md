# Template — Dictionary Entry

For: terms in the dictionary table — Gnostic, Neoplatonic, biblical, philosophical, Jungian terms PKD used; PKD's own bespoke coinages.

## Term classification

Every term is one of:
- **Inherited** — definition is independent of PKD (e.g., *anamnesis*, *hypostasis*, *Demiurge*, *Plotinus*)
- **Transformed** — PKD bent a tradition's term away from its original meaning (e.g., his use of *gnosis* drifts; *hypostasis* gets a private gloss)
- **Bespoke** — PKD's own coinage or a term he gave a private technical sense (e.g., *VALIS*, *Zebra*, *homoplasmate*, *Tagore*, *the Empire Never Ended*)

The classification governs which sections are required.

## card_description
**Length:** ≤40 words.
**Purpose:** Ostensive definition. What does the term denote, in plain terms?
- For inherited terms: the historical/technical definition.
- For bespoke terms: the coinage's referent in PKD's usage.
- Never PKD-context here. Save that for the full description.

## full_description
**Length:** 500–1500 words. Markdown allowed.

### Required sections (use these as actual headers)

#### 1. Etymology and tradition (or **Coinage and first appearance** for bespoke)
- For inherited/transformed: trace the term through its source tradition (Greek philosophy, Gnostic literature, Christian theology, kabbalah, etc.). Cite primary historical sources where they matter (the *Enneads*, the *Nag Hammadi* texts, etc.).
- For bespoke: when does PKD coin or first use it, and in what context (Exegesis, novel, letter)?

#### 2. PKD's usage
- How does PKD use the term? Where does his usage match the tradition, where does it drift?
- First appearance in the corpus (date and segment).
- Peak usage period (date range).
- Span of years he engages with it.
- For transformed terms: name the drift explicitly.

#### 3. Key passages
- 2–4 segment citations, each with a brief gloss. Link to the specific segment IDs.
- The passages should show the term in active use, not in passing mention.

#### 4. Related terms
- Explicit graph: parent terms, child terms, synonyms, contrasts.
- Cross-link to the related dictionary entries.

#### 5. Scholarly engagements
- Has any scholar written authoritatively on this term?
- For bespoke terms: who decoded it, who debated it (e.g., the secondary literature on *VALIS* the concept).
- For inherited terms: how scholars have noted PKD's variant usage.

#### 6. Editorial caution
- Common misreadings.
- Contested usages within PKD's corpus (he sometimes used a term differently in 1974 than in 1978).
- Confusable terms (e.g., *Zebra* the entity vs. the concept of mimicry).

## Required JSON fields
- `card_description` ✓
- `full_description` ✓ (markdown)
- `term_class` — `inherited`, `transformed`, or `bespoke`
- `aliases` — non-empty if the term has spelling variants
- `first_appearance` — date or segment ID
- `peak_usage` — date range
- `related_terms` — non-empty for accepted-tier
- `status` — `accepted`, `provisional`, `alias`, `background`, `rejected`
- `review_state` — `unreviewed`, `machine-drafted`, `human-revised`, `publication-ready`

## Lint checklist
- [ ] All six required sections present.
- [ ] Etymology cited to primary tradition for inherited/transformed terms.
- [ ] First appearance and peak usage dated.
- [ ] At least 2 segment citations with gloss.
- [ ] Related terms graph populated.
- [ ] Editorial caution non-empty (every term has at least one common misreading worth flagging).
