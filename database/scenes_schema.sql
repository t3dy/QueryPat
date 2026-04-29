-- ─────────────────────────────────────────────────────────────
-- AI Scene Summaries: schema extension for QueryPat
-- Tables for deterministic candidate detection → Claude validation → curated scenes
-- ─────────────────────────────────────────────────────────────

PRAGMA foreign_keys = ON;

-- Interaction-type ontology (seeded, extensible)
CREATE TABLE IF NOT EXISTS ai_interaction_types (
    type_slug           TEXT PRIMARY KEY,
    type_label          TEXT NOT NULL,
    type_description    TEXT,
    sort_order          INTEGER DEFAULT 0
);

-- Stage 1: Deterministic scanner output (raw candidates)
CREATE TABLE IF NOT EXISTS ai_scene_candidates (
    candidate_id        INTEGER PRIMARY KEY AUTOINCREMENT,
    work_id             TEXT,                       -- FK → documents.doc_id (novel/story)
    work_title          TEXT NOT NULL,
    doc_id              TEXT,                       -- FK → documents.doc_id (source PDF)
    page_start          INTEGER,
    page_end            INTEGER,
    char_offset_start   INTEGER NOT NULL,
    char_offset_end     INTEGER NOT NULL,
    source_window_text  TEXT NOT NULL,              -- raw extracted text window

    -- Scanner metadata
    matched_terms       TEXT,                       -- JSON array of matched lexicon terms
    matched_interaction TEXT,                       -- best-guess interaction type from lexicon
    match_score         INTEGER DEFAULT 1,          -- count of co-occurring markers
    detection_method    TEXT NOT NULL DEFAULT 'lexicon'
        CHECK(detection_method IN ('lexicon', 'manual')),

    -- Promotion tracking
    promotion_status    TEXT NOT NULL DEFAULT 'pending'
        CHECK(promotion_status IN ('pending', 'validated', 'rejected', 'merged')),
    promoted_scene_id   TEXT,                       -- FK → ai_scenes.scene_id after promotion
    rejection_reason    TEXT,                       -- from Claude validation

    created_at          TEXT DEFAULT (datetime('now')),

    FOREIGN KEY (work_id)  REFERENCES documents(doc_id),
    FOREIGN KEY (doc_id)   REFERENCES documents(doc_id)
);

-- Stage 2: Validated, enriched scenes (curated)
CREATE TABLE IF NOT EXISTS ai_scenes (
    scene_id            TEXT PRIMARY KEY,            -- SCENE_001, SCENE_002, ...
    candidate_id        INTEGER REFERENCES ai_scene_candidates(candidate_id),

    -- Identity
    scene_label         TEXT NOT NULL,               -- ≤15 words
    work_id             TEXT,                        -- FK → documents.doc_id
    work_title          TEXT NOT NULL,
    doc_id              TEXT,                        -- FK → documents.doc_id

    -- Text-window provenance
    page_start          INTEGER,
    page_end            INTEGER,
    char_offset_start   INTEGER NOT NULL,
    char_offset_end     INTEGER NOT NULL,
    source_window_text  TEXT NOT NULL,               -- validated/trimmed text window

    -- Interaction classification
    interaction_type         TEXT NOT NULL,
    interaction_type_secondary TEXT,

    -- Claude-drafted content
    short_summary       TEXT NOT NULL,               -- 2-3 sentences
    significance        TEXT,                        -- 1-2 sentences, grounded in passage
    source_excerpt      TEXT,                        -- fair-use snippet <150 words

    -- Editorial tracking
    editorial_status    TEXT NOT NULL DEFAULT 'machine-drafted'
        CHECK(editorial_status IN (
            'machine-drafted', 'human-revised', 'publication-ready'
        )),
    fair_use_status     TEXT NOT NULL DEFAULT 'pending'
        CHECK(fair_use_status IN ('pending', 'approved', 'trimmed', 'rejected')),

    notes               TEXT,
    created_at          TEXT DEFAULT (datetime('now')),
    updated_at          TEXT DEFAULT (datetime('now')),

    FOREIGN KEY (work_id) REFERENCES documents(doc_id),
    FOREIGN KEY (doc_id)  REFERENCES documents(doc_id)
);

-- Scene participants (characters involved in the interaction)
CREATE TABLE IF NOT EXISTS ai_scene_participants (
    scene_id            TEXT NOT NULL REFERENCES ai_scenes(scene_id),
    name_id             TEXT REFERENCES names(name_id),
    participant_label   TEXT NOT NULL,
    participant_role    TEXT NOT NULL DEFAULT 'human'
        CHECK(participant_role IN (
            'human', 'ai', 'android', 'robot', 'simulation', 'ambiguous'
        )),
    PRIMARY KEY (scene_id, participant_label)
);

-- Cross-link scenes to AI study topics
CREATE TABLE IF NOT EXISTS ai_scene_topics (
    scene_id            TEXT NOT NULL REFERENCES ai_scenes(scene_id),
    topic_id            TEXT NOT NULL REFERENCES study_topics(topic_id),
    relevance           TEXT NOT NULL DEFAULT 'related'
        CHECK(relevance IN ('primary', 'related', 'tangential')),
    PRIMARY KEY (scene_id, topic_id)
);
