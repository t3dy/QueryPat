# Selected Letters → Biography Mining Plan

**Goal:** mine the six volumes of *The Selected Letters of Philip K. Dick* (~2,000 pages) for biographical events, populate the `biography_events` table, and surface the results on the [Biography](/biography) page.

**Why now:** the archive markdown ingestion (running in parallel) gives us clean per-volume markdown for the first time. Plain-text dumps from PyMuPDF lost the structural cues (date lines, salutation breaks) the segmenter needs.

---

## Inventory

| Volume | Title | Years covered | Pages | doc_id |
|---|---|---|---|---|
| 1 | Selected Letters Vol 1 | 1938–1971 | 374 | `DOC_ARCH_OCEANOFPDF_COM_THE_SELECTED_LETTERS_VOLU` |
| 2 | Selected Letters | 1972–1973 | 423 | `DOC_ARCH_PHILIP_K_DICK_THE_SELECTED_LETTERS_OF_PH` |
| 3 | Selected Letters | 1974 | (missing — gap in archive) | — |
| 4 | Selected Letters | 1975–1976 | 382 | `DOC_ARCH_OCEANOFPDF_COM_SELECTED_LETTERS_OF_PHILI` |
| 5 | Selected Letters | 1977–1979 | 300 | `DOC_ARCH_PHILIP_K_DICK_PAUL_WILLIAMS_SELECTED_LET` |
| 6 | Selected Letters | 1980–1982 | 344 | `DOC_ARCH_THE_SELECTED_LETTERS_OF_PHILIP_K_DICK_19` |

Plus *A Dark-Haired Girl* (51pp, 2008) and a few singletons.

**Total: ~1,825 pages of letters across the available volumes.**

The 1974 volume is missing from the archive and represents a documented gap — that is the year of 2-3-74. The dispute registry in [PKDontology §4](PKDontology.md) flags 1974 letters as a known evidence shortfall; this mining run will not close that gap.

---

## Pipeline

### Stage 1 — Segment into individual letters (deterministic)

A volume markdown file looks roughly like this (after conversion):

```
## February 14, 1972
Dear Stanislaw Lem,

Thank you for your letter…
[body text]

—
PKD
```

The segmenter (`scripts/letters/segment.py`) uses a regex stack:

1. **Date heading anchors** (`^## (Month DDDD?, YYYY)$` or variations) split on date lines.
2. **Salutation anchors** (`^Dear [A-Z][a-z]+`) inside a chunk confirm a letter boundary.
3. **Signature footers** (`PKD`, `Phil`, `Philip K. Dick`, `Phil Dick`) close a letter.

Each detected letter gets a `letter_id` (e.g. `LET_1972-02-14_LEM_001`), with fields:

- `letter_id`, `volume_doc_id`, `start_offset`, `end_offset`
- `date_display`, `date_start`, `date_end`, `date_confidence` (per the multi-field convention)
- `recipient_raw` (the salutation), `recipient_canonical` (resolved against `names`)
- `sender_location` (if mentioned in header — Point Reyes, Santa Ana, Vancouver, etc.)
- `body_md`, `word_count`

Output: `database/letters/{volume_doc_id}/letters.jsonl` and a new SQLite table `letters` (additive).

### Stage 2 — Heuristic biographical-event extraction (deterministic)

Letters are dense in dateable, locatable, attributable events. A first pass runs purely-deterministic extractors over each letter body:

- **Location lines** (`I'm now in Vancouver`, `we moved to Santa Ana`) → location fact
- **Money mentions** (`advance check from`, `advance of $X from`) → publication-event fact
- **Title mentions** matched against the works dictionary → "discussed" event
- **Person mentions** matched against `names` → mention-link
- **Health mentions** (`hospitalized`, `psychotic break`, `tachycardia`, `dialysis`, `stroke`) → health event
- **Drug mentions** matched against the drugs lexicon → flagged for the contradiction registry
- **Bishop Pike, Anne, Tessa, Nancy, Linda Levy** mentions → relationship-period markers

These produce candidate `biography_events` rows with `reliability='high'`, `source_type='letter'`, `evidentiary_lane='E'`, `date_basis='letter_postmark'`. Each candidate has a `letter_id` foreign key.

### Stage 3 — LLM-targeted reading (the part the deterministic pass can't do)

The deterministic pass catches dateable factual mentions but misses interpretive, narrative, and reflective passages where PKD describes events without naming them with stock vocabulary. For these, a targeted LLM prompt runs over each letter body.

**Target themes** (per user direction, 2026-04-29) — every extracted event must be tagged with at least one of:

1. **drugs** — amphetamines, vitamin regime, hallucinogens, drug rehab, sodium pentothal, drug-related police interaction, X-Kalay, Synanon, Heroin Reform Society, Substance D parallels in life.
2. **music** — composer/song mentions tied to a circumstance (listening to X while writing Y, attending a concert, buying a record, KOIF/KPFA work, Linda Ronstadt encounters, the Fox/Asher generative period for *The Divine Invasion*).
3. **career** — manuscripts written/sold/rejected, advances received, contracts, agent changes (Meredith → Russ Galen → Scott Meredith), award nominations and wins (Hugo, John W. Campbell), film options (Pre-*Blade Runner* and *Blade Runner* itself), foreign rights, panel appearances, Metz speech.
4. **relationships** — marriages, separations, affairs, the Dark-Haired Girls (Linda Levy, Tessa Busby, Doris Sauter, Joan Simpson), friendships (Lem, Bishop Pike, Tim Powers, KW Jeter, James Tiptree Jr., Ursula Le Guin), the Vancouver suicide attempt context.
5. **politics** — FBI letters, the November 1971 break-in attribution shifts, Vietnam War commentary, Black Panther interactions (Reverend Jim Pike, Danny Berrigan), conservative late turns, the alleged "committee" Lem-as-front theory, anti-Soviet shifts, the Ford / Carter / Reagan administrations as referenced.
6. **religion** — Bishop Pike conversations, theological reading (Lem on PKD's own theology, Tillich, Bonhoeffer, Schopenhauer, Boehme, Eckhart, the Nag Hammadi library, Robert Anton Wilson, gnostic texts, Episcopal church attendance, the 2-3-74 vision and its theological aftermath, conversations with Edward Heyne, James Pike's son's death, the apostle Thomas correspondence theory).

A single event can be tagged with multiple themes (and frequently will be — e.g., "I attended Bishop Pike's funeral" is religion + relationships).

**Prompt schema:**

```
For the letter from {date} to {recipient}, extract any biographical events
the letter mentions in the following six theme areas:
  drugs, music, career, relationships, politics, religion.

An event is a dated, attributable fact or self-report about PKD's life
that touches at least one of these themes. Skip routine pleasantries,
weather, and plot summaries of his fiction (unless the letter explicitly
ties the fiction to a real-life event).

Return JSON only:
[
  {
    "summary": "one sentence stating the event",
    "themes": ["drugs"|"music"|"career"|"relationships"|"politics"|"religion", ...],   // 1+ required
    "date_start": "YYYY-MM-DD" | "YYYY-MM" | "YYYY",
    "date_confidence": "exact" | "month" | "year" | "approximate",
    "event_type": "move|publication|meeting|health|relationship|creative|vision|financial|legal|drug_use|listening|reading|writing|other",
    "location": "city, state" | null,
    "people": ["names mentioned"],
    "evidence_quote": "the exact line or short passage",
    "interpretation_lane": "fact" | "self_report",
    "importance": "high" | "medium" | "low"   // for the contradiction registry; high = events on the standing dispute zones
  }
]

Return [] if the letter contains no events in any of the six themes.
```

The `interpretation_lane` field separates a checkable event ("I moved to Santa Ana on November 4") from a self-report ("I felt the presence of God"). Lane B (self-report) events go into `biography_events` with `reliability='self-report'`; lane E (fact) events with `reliability='high'`.

This call runs once per letter. Caching keys on (letter_id, prompt_version) so re-runs are free.

### Stage 4 — Disambiguation and dedup

The same event will often appear in multiple letters (PKD telling the same story to Lem and to Galen, two days apart). The dedup pass:

1. Groups candidate events by (date_start, event_type).
2. Within each group, picks the earliest letter as primary and merges others as `corroborating_letters`.
3. If two events disagree on facts (date, location), surfaces the disagreement via `notes` and tags `contradicts_event_id`.

Result: each unique biographical event has one row with one or more letter citations.

### Stage 5 — Insert into biography_events + cross-linking

New rows go into `biography_events` with:
- `bio_id`: `BIO_LETTER_{date_start}_{event_type}_{nnn}`
- `source_type`: `letter`
- `source_name`: the volume's archive title
- `source_doc_id`: the volume's `DOC_ARCH_*`
- `source_letter_id`: foreign key to the new `letters` table
- `evidentiary_lane`: `E` (primary)
- `reliability`: `high` or `self_report`
- All the regular fields per the [biography event template](scripts/overrides/templates/template_biography_event.md)

Also inserts `event_letter_links`, `event_name_links`, `event_term_links` per [PKDontology §6](PKDontology.md).

### Stage 6 — Re-export JSON

`scripts/export_json.py --biography-only` regenerates `site/public/data/biography/index.json` and `events.json`. The Biography page picks up the new events automatically.

---

## File layout (new)

```
scripts/letters/
  __init__.py
  segment.py                 # Stage 1
  extract_deterministic.py   # Stage 2
  extract_llm.py             # Stage 3 — calls anthropic SDK
  dedupe.py                  # Stage 4
  ingest.py                  # Stage 5 — writes to biography_events
  prompts/
    extract_events.md        # the LLM prompt
database/
  letters/                   # gitignored, regenerable from markdown
    {volume_doc_id}/
      letters.jsonl
      events_candidate.jsonl
LETTERS_MINING_REPORT.md     # written at end, summarizes counts and notable events
```

---

## Schema additions

```sql
CREATE TABLE IF NOT EXISTS letters (
    letter_id TEXT PRIMARY KEY,
    volume_doc_id TEXT NOT NULL,
    sequence_in_volume INTEGER,
    date_start TEXT,
    date_end TEXT,
    date_display TEXT,
    date_confidence TEXT,
    recipient_raw TEXT,
    recipient_canonical TEXT,
    sender_location TEXT,
    word_count INTEGER,
    body_md TEXT,
    created_at TEXT,
    FOREIGN KEY (volume_doc_id) REFERENCES documents(doc_id)
);

CREATE INDEX IF NOT EXISTS idx_letters_date ON letters(date_start);
CREATE INDEX IF NOT EXISTS idx_letters_recipient ON letters(recipient_canonical);

ALTER TABLE biography_events ADD COLUMN source_letter_id TEXT;
ALTER TABLE biography_events ADD COLUMN corroborating_letters TEXT;  -- JSON array of letter_ids
ALTER TABLE biography_events ADD COLUMN evidence_quote TEXT;
ALTER TABLE biography_events ADD COLUMN interpretation_lane TEXT;     -- 'fact' or 'self_report'
ALTER TABLE biography_events ADD COLUMN contradicts_event_id TEXT;
ALTER TABLE biography_events ADD COLUMN themes TEXT;                  -- JSON array; subset of: drugs, music, career, relationships, politics, religion
```

---

## Cost / runtime estimate

- **Stage 1 (segment):** seconds. Pure regex.
- **Stage 2 (deterministic):** seconds.
- **Stage 3 (LLM):** ~2,000 letters × ~1k tokens × 1 call = ~2M input tokens. With Sonnet at $3/MTok input, ~$6 for the run; output is small.
- **Stage 4 (dedupe):** seconds.
- **Stage 5 (ingest):** seconds.
- **Stage 6 (export):** seconds.

Wall-clock dominated by Stage 3 LLM calls; with parallelism (10 concurrent) ~30–45 min for the full run.

---

## Acceptance criteria

After running:
- `letters` table populated with ≥1,500 rows (some letters are very short or boilerplate)
- `biography_events` grew by ≥800 new events (target: 1,500+ if LLM extraction is generous)
- Letter coverage: ≥1 event per 2 letters on average
- Re-running is a no-op (cache hits via `letter_id + prompt_version`)
- Spot-check: 5 random letters, manually verify their extracted events match the source

---

## Risks

1. **Letter boundary detection is fuzzy** — published volumes use varying date formats and editorial annotations. Manual spot-check after Stage 1 is mandatory.
2. **OCR errors in source PDFs** — some volumes are OceanofPDF rips with character corruption ("the" → "thc"). The dedup stage may treat these as distinct events.
3. **PKD's narrative drift** — he tells the same story differently across letters. The dedupe pass needs to be conservative; a too-aggressive merge loses contradictions worth recording.
4. **Date confidence in heading vs. body** — letterhead date is usually exact, but body events ("last week we…") need lower confidence.
5. **Recipient canonicalization** — "Dear Stan" could be Stan Lem or Stan Robinson. Match against `names` with high-confidence-only initially; flag ambiguous as `recipient_canonical=NULL`.

---

## Out of scope

- **The 1974 volume gap.** This mining run cannot fabricate letters that don't exist in the archive. The 1974 letters published in academic journals (a few are scattered) need separate ingestion.
- **Postcards, telegrams, signed correspondence** outside the Selected Letters edition. The *Dark-Haired Girl* volume is included; the unindexed PKDS Newsletter letter excerpts are not.
- **Letter-to-letter relationship modeling** (replies, threads). Treat each letter as standalone for now.
