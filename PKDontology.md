# PKDontology — Data Ontology for the PKD Knowledge Base

What counts as a fact about Philip K. Dick, what kinds of facts matter, and how they relate. This is the editorial spine for everything written into the database — dictionary entries, document summaries, scholar pages, biography events, name entries, segment annotations.

The site already enforces a structural ontology (tables, IDs, evidentiary lanes). This document defines the **content ontology**: the topics worth tracking, the questions a scholar/fan would actually want answered, and the editorial rules for handling contested ground.

---

## 1. The Researcher's Standing Questions

The database exists to answer four kinds of questions a PKD researcher actually asks:

1. **What did PKD do, when, and on whose authority?** — Biographical reality versus self-mythology.
2. **What did PKD mean by X?** — His shifting use of theological, philosophical, and bespoke vocabulary.
3. **What is the textual evidence for a given claim?** — Where in the Exegesis, the fiction, the letters, or the interviews does this appear?
4. **What have others said about it, and where do they disagree?** — Critical reception across academic, fan, biographical, and primary-source channels.

Every entry in the database should make one of these questions easier to answer. If it doesn't, it's filler.

---

## 2. Core Entity Domains

The database tracks ten domains. Each has a definitional test (when is X an instance of this domain?) and a list of facts to capture.

### 2.1 Biography Events
**Test:** A discrete, datable occurrence in PKD's life, or a sustained state (residence, marriage, illness) bracketed by start/end dates.

**Facts to capture:**
- Date (with precision: day / month / year / decade / inferred)
- Event description (one sentence, neutral voice, no interpretation)
- Location (city + venue where possible)
- Participants (other named entities)
- Source(s) reporting it
- Reliability tier (confirmed / likely / disputed / contradicted / self-report-only)
- Contradicting accounts (with source and the nature of disagreement)
- Importance (1–5: trivial → life-defining)

**Sub-categories worth tracking distinctly:**
birth, family, education, marriage, divorce, child, residence, employment, drug use, illness, hospitalization, vision/mystical event, publication, contract, finances, FBI/IRS/break-in, correspondence, friendship, conference/convention, interview, film/TV deal, death.

### 2.2 Works (PKD's bibliography)
**Test:** A text PKD authored — novel, story, essay, speech, screenplay, letter, Exegesis fragment.

**Facts to capture:**
- Title (canonical + variants)
- Date written / date published / publication venue
- Length, form (novel/novella/story/essay/letter/speech)
- Composition history (drafts, working titles, abandoned alternates)
- Publishing situation (advance, contract, agent, editor)
- First-edition cover artist where known
- Adaptations (film, TV, stage, comic, audio)
- Themes touched (linked to Themes domain)
- Vocabulary debuted or featured (linked to Dictionary)
- Self-commentary in the Exegesis or letters (linked to Segments)
- Critical reception (linked to Documents)

### 2.3 Visions and Mystical Events
**Test:** An experience PKD reported as anomalous, mystical, theophanic, or paranormal. Includes both single-incident events (the pink-beam, the AI Voice, the Black Iron Prison) and sustained states (2-3-74 → 1982).

**Facts to capture:**
- PKD's own description (with date written)
- Date of the experience itself (when claimed)
- Witnesses or corroborating events
- Competing PKD interpretations (he proposed many — record them all)
- Scholarly interpretations (clinical, mystical, literary)
- Cross-references to fiction (when does it surface in a novel?)

**Editorial caution:** PKD's own theory of an event changed often. Record the theories as theories — never adopt one as the canonical reading.

### 2.4 People (named entities)
**Test:** A real or fictional person, deity, or quasi-personal entity referenced in PKD's work or life.

**Sub-types and what to capture for each:**
- **Family** — relationship, dates, role in PKD's life
- **Spouses** (Jeanette, Kleo, Anne, Nancy, Tessa) — marriage dates, divorce dates, what they wrote about him, what he wrote about them
- **Friends and correspondents** — Tim Powers, K.W. Jeter, James Blaylock, Norman Spinrad, Ursula K. Le Guin, Stanislaw Lem, Doris Sauter, etc.
- **Editors and agents** — Donald Wollheim, Terry Carr, Russ Galen, Scott Meredith, etc.
- **Historical/philosophical figures PKD invoked** — Plato, Plotinus, Mani, Bruno, Eckhart, Böhme, Pascal, Kant, Heidegger, Jung
- **Theological/mythic figures** — Christ, Sophia, the Demiurge, Yaldabaoth, Hermes Trismegistus, Elijah, Thomas, Asklepios, Dionysus
- **Fictional characters in PKD's works** — already 191 catalogued; capture etymology, allusion domain, novels of appearance, thematic role

**Facts to capture (generally):**
- Canonical name + aliases / spellings
- Etymology where meaningful
- Allusion domain (Gnostic, Neoplatonic, Hermetic, biblical, classical, contemporary, bespoke)
- Relation to PKD (personal / cited / parodied / fictionalized)
- First appearance and peak usage in the corpus

### 2.5 Places
**Test:** A geographic location with biographical or fictional significance.

**Facts to capture:**
- Coordinates / address where defensible
- Period(s) of PKD's connection
- What happened there (linked to Biography)
- Fictional analogues (Berkeley → many novels' urban backdrops; Marin County → *A Scanner Darkly*'s San Diego; Point Reyes → *Confessions of a Crap Artist*)

### 2.6 Themes
**Test:** A recurring conceptual concern across multiple works.

**Working list (to be expanded):**
reality vs. illusion, simulacra, the authentic human, empathy as moral test, paranoia and surveillance, fascism and the police state, time and time-disturbance, identity dissolution, the demiurge and false world, gnosis and anamnesis, salvation, drugs and altered states, the tyrannical father, the dead twin, the dark-haired girl, women as savior figures, schizophrenia, capitalism and the kipple-state, AI and android consciousness, the Empire and theocratic resistance.

**Facts to capture:**
- Definition
- Works where it dominates
- Exegesis segments that theorize it
- Key scholarly treatments
- Related themes (theme-to-theme graph)

### 2.7 Theological / Philosophical Vocabulary (the Dictionary)
**Test:** A term PKD uses with technical weight — Gnostic, Neoplatonic, biblical, Jungian, philosophical, or his own bespoke coinage.

**Facts to capture (per the Dictionary template, expanded):**
- Canonical form + aliases / spellings
- Etymology and source tradition
- Technical / historical definition
- PKD's usage — how he transforms or repurposes it
- First appearance in corpus
- Peak usage period
- Key Exegesis segments where he develops it
- Related terms (parent / child / synonym / contrast)
- Scholarly notes — has anyone written authoritatively on this term?
- Editorial caution — common misreadings

**Distinguish:**
- *Inherited* terms (Gnostic, Neoplatonic, Christian) — definition is independent of PKD
- *Transformed* terms (terms PKD bent away from their tradition)
- *Bespoke* terms (VALIS, Zebra, homoplasmate, Tagore, the Empire Never Ended)

### 2.8 Influences (intellectual and literary)
**Test:** A thinker, writer, tradition, or text PKD demonstrably engaged with.

**Already partly captured via terms and people, but track distinctly:**
- Direct citations (PKD names them)
- Indirect engagements (scholars argue for influence)
- Counterpart figures (writers PKD measured himself against — Borges, Lem, Le Guin, Pynchon)
- Anti-influences (figures PKD positioned himself against — Heinlein politically, Asimov tonally)

### 2.9 Adaptations and Reception History
**Test:** Anything that turns PKD's work into a downstream artifact.

**Facts to capture:**
- Adaptation type (film, TV, stage, comic, audio, game)
- Source work
- Year, director / showrunner / publisher
- Fidelity / divergence (one paragraph)
- Critical reception
- PKD's own response where extant (he wrote about *Blade Runner* and the *Total Recall* deal)

### 2.10 Documents (the archive)
**Test:** A bibliographic item — book, article, essay, dissertation, fanzine, letter, newspaper clipping, manuscript, finding aid — that informs the database.

**Facts to capture:** see Document Summary Quality (§4) below.

---

## 3. The Evidentiary Lanes

Already implemented in the schema; here is the editorial reason:

| Lane | Source class | What it can settle | What it cannot settle |
|------|--------------|---------------------|------------------------|
| **A** | Fiction (novels, stories) | What PKD wrote in the works | His intent or beliefs |
| **B** | Exegesis | What PKD theorized about himself and the world | Whether the theory is true |
| **C** | Scholarship (academic) | What trained readers have argued | Biographical reality directly |
| **D** | Synthesis (biographies, encyclopedias) | Consensus narrative | Disputed details |
| **E** | Primary (letters, interviews, contracts, manuscripts) | What PKD said and signed at a given moment | His later reinterpretation |

**Editorial rule:** A claim's lane must be visible in the entry. A biography event sourced only to the Exegesis (lane B) is a self-report, not a confirmed event. A claim attested by lanes D + E + C is settled.

---

## 4. Source Reliability and Contradiction Policy

The PKD literature is unusually contradictory. The ontology has to make this legible rather than smoothing it over.

### Reliability tiers (per claim, not per source)
- **confirmed** — multiple independent sources across at least two lanes agree
- **likely** — one credible source, no contradicting account, plausible on context
- **self-report-only** — only PKD says it (in Exegesis, letters, or interviews)
- **disputed** — credible sources disagree substantively
- **contradicted** — directly refuted by a more reliable source
- **legendary** — circulated but unsourceable; record as story

### Known contradiction zones (always flag, never resolve silently)
1. **The November 1971 break-in** — staged? FBI? KGB? PKD himself? local burglars?
2. **The 2-3-74 events** — psychotic episode? TLE? mystical experience? literary frame?
3. **Drug use chronology** — PKD revised this many times across interviews
4. **The Vancouver suicide attempt (1972)** — circumstances, motive, sequence
5. **The Anne Dick marriage breakdown** — divergent accounts in *Search for PKD* vs. PKD's own letters
6. **Composition order of the Exegesis** — folder dating versus internal cross-references
7. **The Bishop Pike sequence** — PKD's role and the séance question
8. **The high-school years and the agoraphobia onset**
9. **The CIA / Lem / "committee" claims** — PKD's later paranoia about Lem's identity

When writing any entry that touches one of these zones, the contradiction must surface, not hide.

---

## 5. The "Fact vs. Interpretation" Editorial Line

A non-negotiable rule for all writers (human or LLM) contributing to the database:

- **Fact** = reported event, dated, with at least one source. Written in plain declarative voice.
- **Interpretation** = a reading, hypothesis, or inference. Always attributed to whoever holds it.

Example, wrong: *"PKD's break-in was staged to give him an excuse to leave Marin County."*
Example, right: *"The break-in's cause is disputed. Sutin treats it as ambiguous; Rickman entertains a self-staging hypothesis based on PKD's own later doubts; Anne Dick rejects the staging theory."*

Card summaries in the archive and dictionary should **never** smuggle in an interpretive position as if it were settled.

---

## 6. Cross-Reference Rules

The database's value compounds with cross-linking. Every new entry should ask:

1. **What dictionary terms does this entry attest?** (link to terms)
2. **What biography events does it touch or contradict?** (link to events)
3. **What other documents or scholars discuss the same matter?** (link via document_topics / scholars)
4. **What Exegesis segments are relevant?** (link to segments)
5. **What named entities appear?** (link to names)
6. **Which of PKD's works are referenced?** (link via works_referenced)

A document summary that passes through these six prompts produces the cross-link graph for free.

---

## 7. What the Ontology Refuses to Track

Negative space matters. The database should **not** become:

- A novel-by-novel plot synopsis library (Wikipedia does this)
- A film-adaptation review aggregator (Letterboxd does this)
- A sci-fi history textbook (covers context only when load-bearing)
- A general philosophy or theology reference (defines terms only as PKD used them)
- A biographical hagiography or pathologization

Anything outside these lanes is in scope only when it is load-bearing for one of §1's four standing questions.

---

## 8. Coverage Priorities

Where the ontology is currently thin:

1. **Visions / mystical events** (§2.3) — exists scattered across biography events and segments, no unified entity table
2. **Themes** (§2.6) — partially captured via segment fields, no top-level theme entity
3. **Composition history of the works** (§2.2) — sparse; a major gap
4. **Scholar interpretive positions** (§2.x crossing into §4) — most Tier 4 scholars have empty stance
5. **Adaptations** (§2.9) — not currently tracked
6. **Contradiction registry** (§4) — flagged in places, not surfaced as an entity

These are the expansion targets the content plan should attack first.
