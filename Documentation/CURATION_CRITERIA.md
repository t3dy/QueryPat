# Curation Criteria

How the `CurationArtifact` (stage F) decides whether and how an item appears in the portal or
the news aggregator. The goal is to separate **serious historical / scholarly esoteric-studies
content** from generic occult lifestyle, vague spirituality, AI spam, and low-relevance pop
content — and, for PKD-portal material, to keep the fact-vs-interpretation line intact.

## The two decisions

**1. `relevance_status`** — what to do with the item:

| status   | meaning                                                                 |
|----------|-------------------------------------------------------------------------|
| `reject` | Out of scope or low value; do not surface.                              |
| `archive`| Keep on record, do not surface in feeds.                                |
| `review` | Promising but blocked (e.g. ungrounded, unresolved contradiction).      |
| `publish`| Surface as a normal item. **Requires `reasons_for_inclusion`.**         |
| `feature`| Promote prominently. **Requires `reasons_for_inclusion`.**              |

**2. `content_class`** — what kind of thing it is (the spam/serious filter):

| content_class                | surface? | example                                            |
|------------------------------|----------|----------------------------------------------------|
| `serious_scholarship`        | yes      | Peer-reviewed / rigorously argued history.         |
| `primary_source_discussion`  | yes      | Direct engagement with primary sources/manuscripts.|
| `scholarly_reliability_review`| yes     | Assessment of how reliable a source/claim is.      |
| `history_of_science`         | yes      | History-of-science framing of esoteric material.   |
| `book_or_manuscript_history` | yes      | Editions, bibliography, manuscript studies.        |
| `pop_occult_low_relevance`   | usually no| Pop-occult / lifestyle content, low scholarly value.|
| `vague_spirituality`         | no       | Generic spirituality, no historical grounding.     |
| `ai_spam`                    | no       | Low-effort AI-generated filler.                    |
| `generic_lifestyle`          | no       | Wellness / lifestyle, unrelated to scholarship.    |
| `uncertain`                  | review   | Not yet classifiable.                              |

A `publish`/`feature` decision should normally pair a "surface: yes" `content_class` with a
concrete `scholarly_value` and `audience_fit`.

## Signals that push toward "serious"

- Cites or engages **primary sources / manuscripts**; gives locators.
- Names scholars, editions, archives; situates a claim in a literature.
- Distinguishes description from interpretation; flags uncertainty.
- Domain fit (`esoteric_domains`): Western esotericism, Renaissance magic, alchemy, Hermetism,
  Neoplatonism, Christian Kabbalah, grimoires, ritual magic, astrology, witchcraft studies,
  history of science, manuscript studies, book history, iconography, historiography, methodology.

## Signals that push toward "low relevance / spam"

- Self-help / lifestyle framing ("manifest your...", "the magic of...") with no sources.
- Unsourced spiritual generalities; no named texts, scholars, or dates.
- Hallmarks of AI filler: generic listicles, no specific claims, no citations.
- Pop-occult product/marketing content.

## Audience fit and scholarly value

- `audience_fit`: `specialist` | `intelligent_non_specialist` | `general` | `poor_fit` | `uncertain`.
  The portal's default target is the **intelligent non-specialist**: prose should be accessible
  without being dumbed down.
- `scholarly_value`: `high` | `medium` | `low` | `none` | `uncertain`.

## Curation for the PKD portal specifically

In addition to the esoteric-studies filters, PKD-portal curation must respect `PKDontology.md`:

- Tag the **evidentiary lane** (A–E). A claim attested only by the Exegesis (lane B) is a
  self-report, not a confirmed event.
- If the item touches a **contradiction zone** (the 1971 break-in, 2-3-74, drug-use chronology,
  the Lem affair, etc.), it cannot be `publish`/`feature` as settled fact — route to `review`
  or ensure the prose surfaces the dispute.
- Reception-history and primary-press items (interviews, profiles) are in scope when they are
  load-bearing for one of the four standing research questions.

## Worked example

`artifacts/fixtures/example_curation.json` holds the 1974 Rolling Stone item at
`relevance_status: review`, `content_class: primary_source_discussion`. It is **not** published —
even though it is a genuinely relevant reception-history object — because the scan has no OCR
text and carries an unresolved 1974/1975 dating discrepancy. The `reasons_for_inclusion` and
`reasons_for_exclusion` fields record both sides of that call, so the decision is auditable.

## News-aggregator link card

When an aggregator item clears curation, the writing agent emits a `PublicProseArtifact` link
card carrying: title, source + URL (`citations_or_source_links`), date, a short `summary`, a
"why it matters" line (`dek_or_short_description`), `tags`, the relevance status (from this
CurationArtifact), and an optional editorial note (`revision_notes`).
