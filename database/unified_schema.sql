-- QueryPat Unified Exegesis Knowledge Portal
-- Canonical SQLite Schema v1.0
--
-- ID Policy:
--   DOC_EXEG_*   Exegesis document/section
--   DOC_ARCH_*   Archive PDF document
--   SEG_EXEG_*   Exegesis chunk/segment
--   SEG_ARCH_*   Archive page/passage segment
--   TERM_*       Dictionary term
--   EV_*         Evidence packet
--   TL_*         Timeline event
--   ASSET_*      File reference (PDF, image, etc.)
--
-- Slugs are derived separately for public URLs and never used as primary keys.

PRAGMA journal_mode = WAL;
PRAGMA foreign_keys = ON;

-- ============================================================
-- CORE OBJECTS
-- ============================================================

CREATE TABLE documents (
    doc_id              TEXT PRIMARY KEY,           -- DOC_EXEG_* or DOC_ARCH_*
    doc_type            TEXT NOT NULL CHECK (doc_type IN (
                            'exegesis_section', 'archive_pdf', 'letter', 'interview',
                            'scholarship', 'novel', 'short_story', 'biography',
                            'newspaper', 'fan_publication', 'other'
                        )),
    title               TEXT NOT NULL,
    slug                TEXT,                       -- derived, for URLs
    author              TEXT,
    recipient           TEXT,                       -- for letters

    -- Date model (multi-field, never a single "date" column)
    date_start          TEXT,                       -- ISO partial: 1977, 1977-03, 1977-03-14
    date_end            TEXT,                       -- for ranges
    date_display        TEXT,                       -- human-readable: "circa 1977"
    date_confidence     TEXT CHECK (date_confidence IN (
                            'exact', 'approximate', 'circa', 'inferred', 'unknown'
                        )),
    date_basis          TEXT,                       -- how determined: manuscript header, editorial note, etc.
    timeline_type       TEXT CHECK (timeline_type IN (
                            'composition', 'publication', 'letter', 'event_discussed',
                            'interview', 'unknown'
                        )),

    -- Archive-specific extraction metadata
    ingest_level        TEXT CHECK (ingest_level IN (
                            'metadata_only', 'partial', 'full'
                        )),
    extractability_score INTEGER,                   -- 0-100
    relevance_score     INTEGER,                    -- 0-100
    ocr_required        INTEGER DEFAULT 0,          -- boolean
    extraction_status   TEXT CHECK (extraction_status IN (
                            'pending', 'complete', 'failed', 'skipped'
                        )),
    is_pkd_authored     INTEGER DEFAULT 0,          -- boolean

    -- Metadata
    word_count          INTEGER,
    page_count          INTEGER,
    section_order       INTEGER,                    -- for ordering exegesis sections
    section_type        TEXT,                       -- Letter, Journal
    source_filename     TEXT,
    text_char_count     INTEGER,                    -- total extracted text chars
    card_summary        TEXT,                       -- short summary for grid cards
    page_summary        TEXT,                       -- detailed summary
    category            TEXT,                       -- archive taxonomy category
    notes               TEXT,

    created_at          TEXT DEFAULT (datetime('now')),
    updated_at          TEXT DEFAULT (datetime('now'))
);

CREATE INDEX idx_documents_type ON documents(doc_type);
CREATE INDEX idx_documents_date ON documents(date_start);
CREATE INDEX idx_documents_slug ON documents(slug);
CREATE INDEX idx_documents_category ON documents(category);

-- ============================================================

CREATE TABLE segments (
    seg_id              TEXT PRIMARY KEY,           -- SEG_EXEG_* or SEG_ARCH_*
    doc_id              TEXT NOT NULL,
    seg_type            TEXT NOT NULL CHECK (seg_type IN (
                            'chunk', 'page_range', 'passage', 'paragraph'
                        )),
    position            INTEGER,                    -- order within document
    slug                TEXT,

    -- Date model
    date_start          TEXT,
    date_end            TEXT,
    date_display        TEXT,
    date_confidence     TEXT CHECK (date_confidence IN (
                            'exact', 'approximate', 'circa', 'inferred', 'unknown'
                        )),
    date_basis          TEXT,
    timeline_type       TEXT,

    -- Content
    title               TEXT,                       -- chunk filename or passage label
    word_count          INTEGER,
    overlap_previous    INTEGER DEFAULT 0,
    overlap_next        INTEGER DEFAULT 0,

    -- Parsed summary fields (from chunk markdown)
    concise_summary     TEXT,
    key_claims          TEXT,                       -- JSON array
    recurring_concepts  TEXT,                       -- JSON array
    people_entities     TEXT,                       -- JSON array
    texts_works         TEXT,                       -- JSON array
    autobiographical    TEXT,                       -- JSON array
    theological_motifs  TEXT,                       -- JSON array
    literary_self_ref   TEXT,                       -- JSON array
    symbols_images      TEXT,                       -- JSON array
    tensions            TEXT,                       -- JSON array
    evidence_quotes     TEXT,                       -- JSON array
    uncertainty_flags   TEXT,                       -- JSON array
    reading_excerpt     TEXT,

    -- Raw corpus text (from .txt chunk files)
    raw_text            TEXT,
    raw_text_source     TEXT,                   -- file path or extraction method
    raw_text_char_count INTEGER,

    notes               TEXT,
    created_at          TEXT DEFAULT (datetime('now')),
    updated_at          TEXT DEFAULT (datetime('now')),

    FOREIGN KEY (doc_id) REFERENCES documents(doc_id)
);

CREATE INDEX idx_segments_doc ON segments(doc_id);
CREATE INDEX idx_segments_date ON segments(date_start);
CREATE INDEX idx_segments_position ON segments(doc_id, position);
CREATE INDEX idx_segments_slug ON segments(slug);

-- ============================================================

CREATE TABLE terms (
    term_id             TEXT PRIMARY KEY,           -- TERM_*
    canonical_name      TEXT NOT NULL UNIQUE,
    slug                TEXT NOT NULL UNIQUE,        -- for URLs

    -- Triage
    status              TEXT NOT NULL DEFAULT 'unreviewed' CHECK (status IN (
                            'accepted', 'provisional', 'alias', 'background', 'rejected'
                        )),
    review_state        TEXT NOT NULL DEFAULT 'unreviewed' CHECK (review_state IN (
                            'unreviewed', 'machine-drafted', 'human-revised', 'publication-ready'
                        )),

    -- Classification
    primary_category    TEXT,                       -- e.g. "Neoplatonism / Gnosticism"
    thematic_categories TEXT,                       -- JSON array of categories
    mention_count       INTEGER DEFAULT 0,          -- raw frequency in corpus
    score               REAL,                       -- extraction score

    -- Dictionary content
    definition          TEXT,                       -- technical definition
    interpretive_note   TEXT,
    visionary_significance TEXT,
    scholarly_caution   TEXT,
    card_description    TEXT,                       -- short description for grid
    full_description    TEXT,                       -- long scholarly essay

    -- Chronology
    first_appearance    TEXT,                       -- ISO date of earliest mention
    peak_usage_start    TEXT,                       -- when usage peaks
    peak_usage_end      TEXT,

    -- Relationships
    see_also            TEXT,                       -- JSON array of related term_ids

    provenance          TEXT,                       -- who/what generated this entry
    notes               TEXT,
    created_at          TEXT DEFAULT (datetime('now')),
    updated_at          TEXT DEFAULT (datetime('now'))
);

CREATE INDEX idx_terms_status ON terms(status);
CREATE INDEX idx_terms_category ON terms(primary_category);
CREATE INDEX idx_terms_slug ON terms(slug);
CREATE INDEX idx_terms_count ON terms(mention_count DESC);

-- ============================================================

CREATE TABLE assets (
    asset_id            TEXT PRIMARY KEY,           -- ASSET_*
    doc_id              TEXT,
    asset_type          TEXT NOT NULL CHECK (asset_type IN (
                            'pdf', 'epub', 'image', 'audio', 'video', 'text', 'other'
                        )),
    file_path           TEXT NOT NULL,
    file_size_mb        REAL,
    mime_type           TEXT,
    notes               TEXT,
    created_at          TEXT DEFAULT (datetime('now')),

    FOREIGN KEY (doc_id) REFERENCES documents(doc_id)
);

CREATE INDEX idx_assets_doc ON assets(doc_id);
CREATE INDEX idx_assets_type ON assets(asset_type);

-- ============================================================

CREATE TABLE timeline_events (
    event_id            TEXT PRIMARY KEY,           -- TL_*
    event_type          TEXT NOT NULL CHECK (event_type IN (
                            'vision', 'writing', 'letter', 'publication',
                            'biographical', 'philosophical', 'other'
                        )),
    event_summary       TEXT NOT NULL,

    -- Date model
    date_start          TEXT,
    date_end            TEXT,
    date_display        TEXT,
    date_confidence     TEXT CHECK (date_confidence IN (
                            'exact', 'approximate', 'circa', 'inferred', 'unknown'
                        )),
    date_basis          TEXT,
    timeline_type       TEXT,

    -- Links
    seg_id              TEXT,
    doc_id              TEXT,
    confidence          TEXT,
    notes               TEXT,
    created_at          TEXT DEFAULT (datetime('now')),

    FOREIGN KEY (seg_id) REFERENCES segments(seg_id),
    FOREIGN KEY (doc_id) REFERENCES documents(doc_id)
);

CREATE INDEX idx_timeline_date ON timeline_events(date_start);
CREATE INDEX idx_timeline_type ON timeline_events(event_type);

-- ============================================================
-- DEDICATED JOIN TABLES
-- ============================================================

CREATE TABLE term_aliases (
    alias_id            INTEGER PRIMARY KEY AUTOINCREMENT,
    term_id             TEXT NOT NULL,
    alias_text          TEXT NOT NULL,
    alias_type          TEXT DEFAULT 'spelling' CHECK (alias_type IN (
                            'spelling', 'abbreviation', 'alternate_name', 'translation'
                        )),
    FOREIGN KEY (term_id) REFERENCES terms(term_id),
    UNIQUE (term_id, alias_text)
);

CREATE INDEX idx_aliases_term ON term_aliases(term_id);
CREATE INDEX idx_aliases_text ON term_aliases(alias_text);

-- ============================================================

CREATE TABLE term_segments (
    term_id             TEXT NOT NULL,
    seg_id              TEXT NOT NULL,
    match_type          TEXT NOT NULL CHECK (match_type IN (
                            'exact_mention', 'alias_mention', 'conceptual',
                            'inferred', 'external'
                        )),
    link_confidence     INTEGER NOT NULL CHECK (link_confidence BETWEEN 1 AND 5),
    link_method         TEXT NOT NULL,              -- e.g. "manifest_join", "string_match", "line_range", "summary_concept", "cooccurrence"
    matched_text        TEXT,                       -- actual string that matched
    context_snippet     TEXT,                       -- surrounding text
    notes               TEXT,

    PRIMARY KEY (term_id, seg_id, match_type),
    FOREIGN KEY (term_id) REFERENCES terms(term_id),
    FOREIGN KEY (seg_id) REFERENCES segments(seg_id)
);

CREATE INDEX idx_term_seg_term ON term_segments(term_id);
CREATE INDEX idx_term_seg_seg ON term_segments(seg_id);
CREATE INDEX idx_term_seg_confidence ON term_segments(link_confidence);

-- ============================================================

CREATE TABLE term_terms (
    term_id_a           TEXT NOT NULL,
    term_id_b           TEXT NOT NULL,
    relation_type       TEXT NOT NULL CHECK (relation_type IN (
                            'related', 'synonym', 'antonym', 'parent', 'child',
                            'co_occurs', 'influences', 'contrasts', 'evolves_into'
                        )),
    strength            REAL,                       -- 0.0-1.0 weight
    link_confidence     INTEGER CHECK (link_confidence BETWEEN 1 AND 5),
    link_method         TEXT,
    notes               TEXT,

    PRIMARY KEY (term_id_a, term_id_b, relation_type),
    FOREIGN KEY (term_id_a) REFERENCES terms(term_id),
    FOREIGN KEY (term_id_b) REFERENCES terms(term_id)
);

CREATE INDEX idx_tt_a ON term_terms(term_id_a);
CREATE INDEX idx_tt_b ON term_terms(term_id_b);

-- ============================================================

CREATE TABLE document_assets (
    doc_id              TEXT NOT NULL,
    asset_id            TEXT NOT NULL,
    role                TEXT DEFAULT 'source',      -- source, supplement, illustration
    PRIMARY KEY (doc_id, asset_id),
    FOREIGN KEY (doc_id) REFERENCES documents(doc_id),
    FOREIGN KEY (asset_id) REFERENCES assets(asset_id)
);

-- ============================================================
-- EVIDENCE (structured, not blob)
-- ============================================================

CREATE TABLE evidence_packets (
    ev_id               TEXT PRIMARY KEY,           -- EV_*
    term_id             TEXT NOT NULL,
    claim_text          TEXT,                       -- what is being claimed
    evidence_summary    TEXT,                       -- synthesized summary of evidence
    confidence          TEXT CHECK (confidence IN (
                            'strong', 'moderate', 'weak', 'speculative'
                        )),
    source_method       TEXT CHECK (source_method IN (
                            'deterministic', 'heuristic', 'llm', 'editorial'
                        )),
    editorial_status    TEXT DEFAULT 'unreviewed' CHECK (editorial_status IN (
                            'unreviewed', 'machine-drafted', 'human-revised', 'publication-ready'
                        )),
    notes               TEXT,
    created_at          TEXT DEFAULT (datetime('now')),
    updated_at          TEXT DEFAULT (datetime('now')),

    FOREIGN KEY (term_id) REFERENCES terms(term_id)
);

CREATE INDEX idx_ev_term ON evidence_packets(term_id);
CREATE INDEX idx_ev_confidence ON evidence_packets(confidence);

-- ============================================================

CREATE TABLE evidence_excerpts (
    excerpt_id          INTEGER PRIMARY KEY AUTOINCREMENT,
    ev_id               TEXT NOT NULL,
    seg_id              TEXT,                       -- linked segment (if mappable)
    excerpt_text        TEXT NOT NULL,
    line_start          INTEGER,
    line_end            INTEGER,
    folder_id           TEXT,                       -- source folder reference
    matched_alias       TEXT,                       -- which term/alias matched
    notes               TEXT,

    FOREIGN KEY (ev_id) REFERENCES evidence_packets(ev_id),
    FOREIGN KEY (seg_id) REFERENCES segments(seg_id)
);

CREATE INDEX idx_excerpts_ev ON evidence_excerpts(ev_id);
CREATE INDEX idx_excerpts_seg ON evidence_excerpts(seg_id);

-- ============================================================
-- ANNOTATIONS & OVERRIDES
-- ============================================================

CREATE TABLE annotations (
    ann_id              INTEGER PRIMARY KEY AUTOINCREMENT,
    target_type         TEXT NOT NULL CHECK (target_type IN (
                            'document', 'segment', 'term', 'evidence_packet', 'timeline_event'
                        )),
    target_id           TEXT NOT NULL,
    annotation_type     TEXT NOT NULL CHECK (annotation_type IN (
                            'note', 'correction', 'provenance', 'override',
                            'replace_definition', 'set_status', 'suppress_alias',
                            'pin_related_term'
                        )),
    content             TEXT NOT NULL,
    provenance          TEXT,                       -- who/what made this annotation
    created_at          TEXT DEFAULT (datetime('now'))
);

CREATE INDEX idx_ann_target ON annotations(target_type, target_id);
CREATE INDEX idx_ann_type ON annotations(annotation_type);

-- ============================================================
-- BIOGRAPHY
-- ============================================================

-- Biographical events and claims about PKD, with source tracking
-- and contradiction flagging for critical exploration
CREATE TABLE biography_events (
    bio_id              INTEGER PRIMARY KEY AUTOINCREMENT,
    event_type          TEXT NOT NULL CHECK (event_type IN (
                            'birth', 'death', 'marriage', 'divorce', 'residence',
                            'employment', 'publication', 'vision', 'health',
                            'relationship', 'legal', 'financial', 'travel',
                            'substance_use', 'correspondence', 'other'
                        )),
    summary             TEXT NOT NULL,
    detail              TEXT,               -- longer description

    -- Date model
    date_start          TEXT,
    date_end            TEXT,
    date_display        TEXT,
    date_confidence     TEXT CHECK (date_confidence IN (
                            'exact', 'approximate', 'circa', 'inferred', 'unknown'
                        )),
    date_basis          TEXT,

    -- Source tracking (who said this?)
    source_type         TEXT CHECK (source_type IN (
                            'pkd_self_report', 'family_account', 'friend_account',
                            'biographer', 'interview', 'legal_record', 'publication_record',
                            'exegesis', 'letter', 'other'
                        )),
    source_name         TEXT,               -- e.g. "Tessa Dick", "Lawrence Sutin"
    source_doc_id       TEXT,               -- FK to documents if applicable
    source_seg_id       TEXT,               -- FK to segments if applicable

    -- Contradiction tracking
    contradicted_by     TEXT,               -- JSON array of bio_ids that contradict this
    contradiction_note  TEXT,               -- explanation of the contradiction
    reliability         TEXT CHECK (reliability IN (
                            'confirmed', 'likely', 'disputed', 'contradicted', 'unverified'
                        )) DEFAULT 'unverified',

    -- People involved
    people_involved     TEXT,               -- JSON array of names

    notes               TEXT,
    created_at          TEXT DEFAULT (datetime('now')),

    FOREIGN KEY (source_doc_id) REFERENCES documents(doc_id),
    FOREIGN KEY (source_seg_id) REFERENCES segments(seg_id)
);

CREATE INDEX idx_bio_type ON biography_events(event_type);
CREATE INDEX idx_bio_date ON biography_events(date_start);
CREATE INDEX idx_bio_reliability ON biography_events(reliability);

-- ============================================================
-- NAMES (proper name analysis for PKD digital humanities)
-- ============================================================

-- Core name entities (analogous to terms but for proper names)
CREATE TABLE names (
    name_id             TEXT PRIMARY KEY,           -- NAME_*
    canonical_form      TEXT NOT NULL UNIQUE,
    slug                TEXT NOT NULL UNIQUE,

    -- Classification
    entity_type         TEXT NOT NULL CHECK (entity_type IN (
                            'character', 'place', 'organization',
                            'deity_figure', 'historical_person', 'other'
                        )),
    source_type         TEXT CHECK (source_type IN (
                            'fiction', 'exegesis', 'both', 'reference'
                        )),

    -- Triage (same two-axis system as terms)
    status              TEXT NOT NULL DEFAULT 'unreviewed' CHECK (status IN (
                            'accepted', 'provisional', 'alias', 'background', 'rejected'
                        )),
    review_state        TEXT NOT NULL DEFAULT 'unreviewed' CHECK (review_state IN (
                            'unreviewed', 'machine-drafted', 'human-revised', 'publication-ready'
                        )),

    -- Name analysis fields
    etymology           TEXT,                       -- etymological meaning
    origin_language     TEXT,                       -- Greek, Hebrew, Latin, English, etc.
    allusion_type       TEXT,                       -- JSON array: ["biblical","classical"]
    allusion_target     TEXT,                       -- what the name alludes to
    wordplay_note       TEXT,                       -- puns, anagrams, phonetic play
    symbolic_note       TEXT,                       -- symbolic charge analysis
    card_description    TEXT,                       -- short description for grid cards
    full_description    TEXT,                       -- long scholarly essay

    -- Corpus presence
    mention_count       INTEGER DEFAULT 0,
    first_work          TEXT,                       -- first PKD work where name appears
    work_list           TEXT,                       -- JSON array of work titles

    -- Cross-reference to mini knowledge base
    reference_id        TEXT,                       -- FK to name_references if matched

    provenance          TEXT,
    notes               TEXT,
    created_at          TEXT DEFAULT (datetime('now')),
    updated_at          TEXT DEFAULT (datetime('now'))
);

CREATE INDEX idx_names_type ON names(entity_type);
CREATE INDEX idx_names_status ON names(status);
CREATE INDEX idx_names_slug ON names(slug);
CREATE INDEX idx_names_count ON names(mention_count DESC);

-- ============================================================

CREATE TABLE name_aliases (
    alias_id            INTEGER PRIMARY KEY AUTOINCREMENT,
    name_id             TEXT NOT NULL,
    alias_text          TEXT NOT NULL,
    alias_type          TEXT DEFAULT 'spelling' CHECK (alias_type IN (
                            'spelling', 'nickname', 'alternate_form', 'parenthetical'
                        )),
    FOREIGN KEY (name_id) REFERENCES names(name_id),
    UNIQUE (name_id, alias_text)
);

CREATE INDEX idx_name_aliases_name ON name_aliases(name_id);
CREATE INDEX idx_name_aliases_text ON name_aliases(alias_text);

-- ============================================================

CREATE TABLE name_segments (
    name_id             TEXT NOT NULL,
    seg_id              TEXT NOT NULL,
    match_type          TEXT NOT NULL CHECK (match_type IN (
                            'exact_mention', 'alias_mention', 'inferred', 'character_ref'
                        )),
    link_confidence     INTEGER NOT NULL CHECK (link_confidence BETWEEN 1 AND 5),
    link_method         TEXT NOT NULL,
    matched_text        TEXT,
    context_snippet     TEXT,

    PRIMARY KEY (name_id, seg_id, match_type),
    FOREIGN KEY (name_id) REFERENCES names(name_id),
    FOREIGN KEY (seg_id) REFERENCES segments(seg_id)
);

CREATE INDEX idx_name_seg_name ON name_segments(name_id);
CREATE INDEX idx_name_seg_seg ON name_segments(seg_id);
CREATE INDEX idx_name_seg_confidence ON name_segments(link_confidence);

-- ============================================================

CREATE TABLE name_terms (
    name_id             TEXT NOT NULL,
    term_id             TEXT NOT NULL,
    relation_type       TEXT NOT NULL CHECK (relation_type IN (
                            'alludes_to', 'embodies_concept', 'named_after',
                            'discussed_alongside', 'co_occurs'
                        )),
    link_confidence     INTEGER CHECK (link_confidence BETWEEN 1 AND 5),
    link_method         TEXT,

    PRIMARY KEY (name_id, term_id, relation_type),
    FOREIGN KEY (name_id) REFERENCES names(name_id),
    FOREIGN KEY (term_id) REFERENCES terms(term_id)
);

CREATE INDEX idx_name_term_name ON name_terms(name_id);
CREATE INDEX idx_name_term_term ON name_terms(term_id);

-- ============================================================

-- Mini knowledge base for allusion targets (biblical, classical, etc.)
CREATE TABLE name_references (
    ref_id              TEXT PRIMARY KEY,           -- REF_{domain}_{slug}
    canonical_form      TEXT NOT NULL,
    domain              TEXT NOT NULL CHECK (domain IN (
                            'biblical', 'classical', 'philosophical', 'literary',
                            'gnostic', 'historical', 'mythological', 'linguistic'
                        )),
    brief               TEXT NOT NULL,              -- one-line description
    etymology           TEXT,                       -- etymological meaning
    origin_language     TEXT,
    significance        TEXT,                       -- why relevant to PKD studies
    source_text         TEXT,                       -- e.g., "Genesis 3:1", "Republic VII"
    created_at          TEXT DEFAULT (datetime('now'))
);

CREATE INDEX idx_name_ref_domain ON name_references(domain);
CREATE INDEX idx_name_ref_form ON name_references(canonical_form);

-- ============================================================
-- CORPUS SUBSTRATE (document text extraction + raw segment text)
-- ============================================================

-- Extracted text from archive PDFs (full document level)
CREATE TABLE document_texts (
    text_id             TEXT PRIMARY KEY,
    doc_id              TEXT NOT NULL,
    extraction_method   TEXT CHECK (extraction_method IN (
                            'pymupdf', 'ocr', 'manual', 'pre_extracted'
                        )),
    extraction_status   TEXT CHECK (extraction_status IN (
                            'pending', 'complete', 'failed', 'partial'
                        )),
    extractability_score REAL,              -- 0.0-1.0 (printable char ratio)
    ocr_required        INTEGER DEFAULT 0,
    text_content        TEXT,
    char_count          INTEGER,
    created_at          TEXT DEFAULT (datetime('now')),

    FOREIGN KEY (doc_id) REFERENCES documents(doc_id)
);

CREATE INDEX idx_doc_texts_doc ON document_texts(doc_id);
CREATE INDEX idx_doc_texts_status ON document_texts(extraction_status);

-- Per-page extracted text for archive PDFs
CREATE TABLE page_texts (
    page_text_id        TEXT PRIMARY KEY,
    doc_id              TEXT NOT NULL,
    page_num            INTEGER NOT NULL,
    extraction_method   TEXT,
    extraction_status   TEXT,
    page_text           TEXT,
    char_count          INTEGER,

    FOREIGN KEY (doc_id) REFERENCES documents(doc_id)
);

CREATE INDEX idx_page_texts_doc ON page_texts(doc_id);

-- Term co-occurrence from evidence passages
CREATE TABLE term_cooccurrences (
    co_id               INTEGER PRIMARY KEY AUTOINCREMENT,
    term_id_a           TEXT NOT NULL,
    term_id_b           TEXT NOT NULL,
    seg_id              TEXT,
    source_excerpt_id   INTEGER,
    weight              REAL DEFAULT 1.0,
    co_method           TEXT,

    FOREIGN KEY (term_id_a) REFERENCES terms(term_id),
    FOREIGN KEY (term_id_b) REFERENCES terms(term_id),
    FOREIGN KEY (seg_id) REFERENCES segments(seg_id),
    FOREIGN KEY (source_excerpt_id) REFERENCES evidence_excerpts(excerpt_id)
);

CREATE INDEX idx_cooccur_a ON term_cooccurrences(term_id_a);
CREATE INDEX idx_cooccur_b ON term_cooccurrences(term_id_b);
CREATE INDEX idx_cooccur_seg ON term_cooccurrences(seg_id);

-- ============================================================
-- VIEWS (convenience queries)
-- ============================================================

-- Public dictionary: accepted + provisional terms only
CREATE VIEW v_public_dictionary AS
SELECT t.*, COUNT(ts.seg_id) AS linked_segment_count
FROM terms t
LEFT JOIN term_segments ts ON t.term_id = ts.term_id AND ts.link_confidence <= 3
WHERE t.status IN ('accepted', 'provisional')
GROUP BY t.term_id
ORDER BY t.mention_count DESC;

-- Term with all aliases
CREATE VIEW v_term_aliases AS
SELECT t.term_id, t.canonical_name, t.status,
       GROUP_CONCAT(ta.alias_text, ', ') AS aliases
FROM terms t
LEFT JOIN term_aliases ta ON t.term_id = ta.term_id
GROUP BY t.term_id;

-- Public names: accepted + provisional only
CREATE VIEW v_public_names AS
SELECT n.*, COUNT(ns.seg_id) AS linked_segment_count
FROM names n
LEFT JOIN name_segments ns ON n.name_id = ns.name_id AND ns.link_confidence <= 3
WHERE n.status IN ('accepted', 'provisional')
GROUP BY n.name_id
ORDER BY n.mention_count DESC;

-- Segment with document context
CREATE VIEW v_segment_detail AS
SELECT s.*, d.title AS doc_title, d.doc_type, d.author, d.recipient AS doc_recipient
FROM segments s
JOIN documents d ON s.doc_id = d.doc_id;

-- Timeline with linked content
CREATE VIEW v_timeline AS
SELECT tl.*,
       s.title AS seg_title, s.concise_summary,
       d.title AS doc_title
FROM timeline_events tl
LEFT JOIN segments s ON tl.seg_id = s.seg_id
LEFT JOIN documents d ON tl.doc_id = d.doc_id
ORDER BY tl.date_start;
