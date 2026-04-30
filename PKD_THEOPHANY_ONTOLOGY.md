# Theophany & Visionary-Experience Ontology

**Domain:** every reported instance of Philip K. Dick experiencing what he interpreted as theophany, vision, anomalous cognition, possession, dream-revelation, hypnagogic transmission, or any other non-ordinary state in which he believed he was receiving information from a non-human source.

**Position in the data model:** Theophanies sit beside `biography_events` as a sister table. Each theophany has 0..N corresponding biography_events (a theophany causes events — letters written, novels seeded, scholarly engagements). Each biography event can reference a theophany via `theophany_id`. Each theophany has 1..N evidence sources (letters, interviews, Exegesis segments, scholarship).

**Lane sourcing:** all theophany claims are Lane B (PKD's own self-report) by default. Their *narration* by PKD lives in B; their *occurrence* is unknowable from the outside. Scholarly readings of them are Lane C. Biographical placement of them in chronology is Lane D.

---

## 1. Why this is its own domain

The Exegesis-only viewer treated theophanies as ordinary segment content. The expanded portal needs them as first-class entities because:

1. **They recur** — PKD reinterpreted the same vision multiple times across years, reaching incompatible conclusions. The portal must record the same theophany with multiple interpretations rather than re-asserting one canonical reading.
2. **They have multiple sources** — a single theophany may be described in a letter, retold in an Exegesis segment three years later, recounted in a 1981 Rickman interview, novelized in *VALIS*, and reframed in a 2026 scholar's reading. The current schema couldn't hold this.
3. **They have contested ontological status** — PKD himself oscillated between believing they were genuine, believing they were drug-induced, believing they were temporal-lobe seizures, and believing they were communications from a future Phil Dick or a satellite. The ontology must record his oscillation as data.
4. **The literature converges on a small canonical set** — the ~10-15 events biographers and scholars all return to (2-3-74, the Pink Beam, the Fish Sign, the Birth of Christopher Vision, the AI Voice, etc.) need stable IDs so that Exegesis segments, Rickman interview excerpts, scholar quotations, and biography events can all link to the same vision rather than creating duplicate fuzzy references.

---

## 2. Schema

```sql
CREATE TABLE IF NOT EXISTS theophanies (
    theophany_id TEXT PRIMARY KEY,            -- e.g. THEO_1974_03_PINK_BEAM, THEO_1974_02_FISH_SIGN
    name TEXT NOT NULL,                        -- canonical name: "The Pink Beam", "2-3-74", "Fish Sign Encounter"
    slug TEXT NOT NULL UNIQUE,                 -- url slug

    -- Dating (multi-field, like all PKD entities)
    date_start TEXT,                           -- ISO YYYY-MM-DD when known
    date_end TEXT,                             -- if extended over a period (e.g., post-2-3-74 ran for years)
    date_display TEXT,                         -- "February 20, 1974" or "early March 1974"
    date_confidence TEXT,                      -- exact|month|year|approximate
    date_basis TEXT,                           -- "letter to William Sullivan 5/15/74"|"Sutin biography"|"Rickman interview 1981"

    -- Phenomenological taxonomy
    experience_type TEXT,                      -- vision|audition|possession|hypnagogic|dream|gnosis|anamnesis|theophany|reading_event|kabbalistic_transmission|other
    sensory_modality TEXT,                     -- visual|auditory|kinesthetic|cognitive|multimodal|null
    duration TEXT,                             -- "instant"|"seconds"|"minutes"|"hours"|"days"|"continuous_for_period"

    -- Content (what he experienced, in declarative voice)
    summary TEXT NOT NULL,                     -- one-sentence summary
    description TEXT,                          -- 1-3 paragraph fuller description, no editorial gloss

    -- Self-interpretation (PKD's own changing readings — JSON array)
    pkd_interpretations TEXT,                  -- JSON: [{date, source, interpretation, hypothesis_label}]

    -- Scholar interpretations (third-party readings — JSON array)
    scholar_interpretations TEXT,              -- JSON: [{scholar_slug, interpretation, source_doc_id, lane}]

    -- Evidence
    primary_sources TEXT,                      -- JSON array of {type, doc_id|seg_id|letter_id, excerpt}
    primary_quote TEXT,                        -- the canonical quote (PKD's own words, if available)

    -- Cross-linking
    related_theophany_ids TEXT,                -- JSON array — clusters of related visions
    related_works TEXT,                        -- JSON array of work titles seeded by this theophany (e.g. "VALIS")
    related_dictionary_terms TEXT,             -- JSON array of term_ids
    related_names TEXT,                        -- JSON array of name slugs (Christ, Zebra, Valis, Abulafia...)
    related_segments TEXT,                     -- JSON array of seg_ids in the Exegesis

    -- Ontological status fields
    contested_status TEXT,                     -- "genuine|drug_induced|tle|psychiatric|literary|composite|disputed"
    contradiction_zone TEXT,                   -- if this theophany sits on a known dispute zone (yes/no/details)
    pkd_doubt_evidence TEXT,                   -- text noting where PKD himself doubted this experience

    -- Importance
    importance TEXT,                           -- canonical|major|minor — canonical = the ones every biographer treats
    sequence_in_complex INTEGER,               -- if part of a sequence (e.g., the 2-3-74 cluster has many sub-events)
    parent_theophany_id TEXT,                  -- for sub-events under a complex (e.g., 2-3-74 family)

    -- Metadata
    created_at TEXT,
    updated_at TEXT
);

CREATE INDEX IF NOT EXISTS idx_theo_date ON theophanies(date_start);
CREATE INDEX IF NOT EXISTS idx_theo_parent ON theophanies(parent_theophany_id);
CREATE INDEX IF NOT EXISTS idx_theo_importance ON theophanies(importance);

-- Linking tables ---------------------------------------------------------

CREATE TABLE IF NOT EXISTS theophany_evidence (
    evidence_id TEXT PRIMARY KEY,
    theophany_id TEXT NOT NULL,
    source_type TEXT NOT NULL,         -- letter|exegesis_segment|interview|biography|scholarship|fiction|other
    source_doc_id TEXT,                -- DOC_ARCH_*  or DOC_EXEG_*
    source_seg_id TEXT,                -- SEG_EXEG_* if applicable
    source_letter_id TEXT,             -- LET_* if applicable
    page_or_locator TEXT,              -- p. 412, segment offset, time mark
    excerpt TEXT,                      -- the actual passage
    excerpt_lane TEXT,                 -- A|B|C|D|E
    notes TEXT,
    created_at TEXT,
    FOREIGN KEY (theophany_id) REFERENCES theophanies(theophany_id)
);

CREATE INDEX IF NOT EXISTS idx_theo_ev_theo ON theophany_evidence(theophany_id);
CREATE INDEX IF NOT EXISTS idx_theo_ev_source ON theophany_evidence(source_doc_id);

-- biography_events linking
ALTER TABLE biography_events ADD COLUMN theophany_id TEXT;
```

---

## 3. The canonical theophany set (what we seed)

These are the events the literature converges on. Each gets a row in the seed.

| ID | Name | Date | Importance |
|---|---|---|---|
| THEO_1963_PALMER_ELDRITCH_FACE | The Sky-Face Vision (Palmer Eldritch face in the sky) | early 1963 | canonical |
| THEO_1971_11_BREAK_IN_INTUITION | Pre-break-in intuition of foreknowing | November 1971 | major |
| THEO_1972_03_VANCOUVER_DESPAIR | Vancouver despair / suicide attempt context | February-March 1972 | major |
| THEO_1974_02_FISH_SIGN | The Fish-Sign Encounter (Christian fish necklace, 2-20-74) | 1974-02-20 | canonical |
| THEO_1974_02_PINK_BEAM | The Pink Beam Transmission (information dump) | 1974-02-20 | canonical |
| THEO_1974_03_CHRISTOPHER_BIRTH | Christopher's Salvation / Sodium Pentothal Vision | 1974-03 | canonical |
| THEO_1974_03_AI_VOICE | The AI Voice (continuous voice reception begins) | 1974-03-20 | canonical |
| THEO_1974_03_KOINE_GREEK | Koine Greek possession / Acts of the Apostles vision | March 1974 | canonical |
| THEO_1974_SUMMER_ZEBRA | Zebra reveals itself (mimicry hypothesis) | summer 1974 | canonical |
| THEO_1974_BLACK_IRON_PRISON | The Black Iron Prison vision (Rome 70 AD overlay) | 1974 | canonical |
| THEO_1975_NUMERIC_LETTER_GEMATRIA | Numbers/Letters Transformation (Gematria) | 1975 (reported) | canonical |
| THEO_1976_ABULAFIA_POSSESSION | Possession by Abraham Abulafia | 1976 (reported) | canonical |
| THEO_1977_METZ_2_3_75_AGAIN | Second 2-3-74-style event around the Metz speech | 1977-09 | major |
| THEO_1977_PROOF_OF_DAUGHTER_GLAUCOMA | Identification of son's birth defect | 1974-03 | canonical |
| THEO_1980_HYPNAGOGIC_DOG | Hypnagogic dog vision / dream of black-iron prison reopen | 1980 | minor |
| THEO_1981_SISTER_DREAM | Twin sister Jane appearance | 1980-1981 | minor |

Plus a few placeholder/parent records for clusters (e.g., `THEO_1974_2_3_74_CLUSTER` parent over the February-March 1974 sub-events).

---

## 4. Self-interpretation chain (the central feature)

The most distinctive thing about PKD's theophanies is that **he reinterpreted them, sometimes weekly, across the eight years of the Exegesis**. The schema must hold this oscillation.

`pkd_interpretations` is a JSON array, each item:

```json
{
  "date": "1974-03-20",
  "source": "letter to William Sullivan FBI",
  "hypothesis_label": "soviet_satellite",
  "interpretation": "I am being addressed by a satellite operated by Soviet science fiction critics including Stanislaw Lem; the experience is enemy psychological-warfare action.",
  "lane": "B"
}
```

For 2-3-74 alone PKD records ~30 distinct hypothesis labels in the Exegesis. The portal will not pick a winner; it will surface the whole list, dated.

**Standard hypothesis labels** (controlled vocabulary, suggested):
- `soviet_satellite` — Lem-as-front, KGB satellite
- `cia_op` — CIA disinformation
- `christian_revelation` — Christ revealing himself; second Pentecost
- `gnostic_demiurge` — Black Iron Prison / world is fallen
- `valis_information_satellite` — non-human VALIS satellite, possibly extraterrestrial
- `zebra_mimicry` — VALIS as biological mimicry of inanimate matter
- `time_dysphasia` — overlay of 70 AD Rome onto Orange County
- `phil_from_future` — a future PKD addressing past PKD
- `jung_collective` — Jungian archetypes activated
- `tle` — temporal-lobe epilepsy
- `drug_induced` — flashback or amphetamine residue
- `psychotic_break` — ordinary psychiatric event
- `apostle_thomas_rebirth` — PKD as the apostle Thomas reborn
- `hellenistic_wisdom` — Sophia / Hagia Sophia / Logos
- `kabbalistic_gematria` — Hebrew letter mysticism
- `abulafia_possession` — possession by Abraham Abulafia
- `vedic_brahman` — Vedanta non-dualism
- `taoist_li` — Taoist informational metaphysics
- `process_theology` — Whitehead/Hartshorne process
- `evolutionary_consciousness` — Bergsonian elan vital

Each item also carries the source `lane`. PKD's own narration in letters/Exegesis is B; reports of him having said something (in interviews) are E if attested in the moment, C if filtered by scholarship.

---

## 5. Cross-linking the canonical references

Each theophany row should populate:
- `related_works`: novels/stories seeded — `["VALIS", "The Divine Invasion", "Radio Free Albemuth", "The Transmigration of Timothy Archer"]`
- `related_dictionary_terms`: dictionary entries — `["Zebra", "Valis", "Plasmate", "Black Iron Prison", "Logos", "Tagore"]`
- `related_names`: named entities — `["Abulafia", "Thomas (apostle)", "Sophia", "Christ"]`
- `related_segments`: Exegesis segment IDs where this theophany is described
- `related_theophany_ids`: cluster relationships

---

## 6. Display on the website

A new top-level tab **Theophanies** at `/theophanies`:

- **Index page** (`/theophanies`):
  - Hero: brief framing — "the Greek word *theophania* names what PKD said happened to him from 1963 onward; this catalog records every reported instance the corpus knows about, with PKD's changing interpretations and the contemporary scholarship."
  - Filters by year, importance, contested_status
  - Card list of all canonical theophanies with one-sentence summary

- **Detail page** (`/theophanies/:slug`):
  - Phenomenological summary (declarative)
  - PKD's interpretation chain (timeline of his changing hypotheses)
  - Scholar readings (lane C)
  - Primary sources panel (quotes with provenance)
  - Cross-links: novels seeded, dictionary terms, related theophanies, biography events, Exegesis segments

- **Cross-references in existing pages:**
  - `Biography` events that ref a theophany show a small "vision" badge linking to the theophany detail
  - `Dictionary` entries (Zebra, Plasmate, etc.) link back to the theophany that birthed them
  - `Names` entries (Abulafia, Christ, Sophia) show up under the theophanies that invoke them
  - `Exegesis` segments tagged with the theophany they describe

---

## 7. Editorial discipline (the five rules apply unchanged)

Every theophany entry must:
1. **State its lane** — phenomenological description is Lane B (PKD's claim); scholarship is Lane C; biography contextualization is Lane D.
2. **Attribute interpretations** — each `pkd_interpretations[i]` is dated and sourced; never present a "PKD said X" without saying which letter or segment.
3. **Surface contradictions** — when PKD's interpretations disagree across time (and they always do), the chain shows the disagreement.
4. **Cross-link six ways** — terms, events, documents, segments, names, works.
5. **Distinguish fact from self-report** — every theophany is a self-report. The portal records *that* PKD reported it, with what evidence, and which scholars have found this credible or pathological. The portal does not adjudicate ontology.

A theophany is a maximally Lane-B claim — a self-report from inside an unreliable narrator about a state with no external witness. The schema makes this status visible rather than incidental.
