# Study JSON Export Contracts (FROZEN)

All JSON files live under `site/public/data/studies/`.
Consumed via the existing `useData<T>(path)` hook pattern.

---

## 1. Studies Index — `studies/index.json`

```json
[
  {
    "study_id": "ai",
    "study_label": "AI Topics",
    "study_description": "Representations of artificial intelligence...",
    "topic_count": 23,
    "published_count": 8,
    "total_passages": 412,
    "total_evidence_packets": 34,
    "total_contradictions": 12
  },
  {
    "study_id": "psychology",
    "study_label": "Psychology Topics",
    "study_description": "Representations of psychological experience...",
    "topic_count": 23,
    "published_count": 11,
    "total_passages": 587,
    "total_evidence_packets": 45,
    "total_contradictions": 18
  }
]
```

**Route:** `/studies`
**Page:** `StudiesIndex.tsx`

---

## 2. Study Topic Index — `studies/{study_id}/index.json`

Example: `studies/ai/index.json`

```json
{
  "study_id": "ai",
  "study_label": "AI Topics",
  "study_description": "...",
  "topics": [
    {
      "topic_id": "TOPIC_AI_androids",
      "canonical_name": "Androids",
      "slug": "androids",
      "status": "published",
      "priority": 10,
      "card_description": "PKD's androids test the boundary between...",
      "passage_count": 42,
      "evidence_count": 6,
      "contradiction_count": 3,
      "first_appearance": "1955",
      "lane_distribution": { "A": 25, "B": 10, "C": 7 },
      "related_topics": ["empathy-testing", "counterfeit-humanity"]
    }
  ]
}
```

**Route:** `/studies/ai`, `/studies/psychology`
**Page:** `StudyIndex.tsx`

---

## 3. Topic Detail — `studies/{study_id}/topics/{slug}.json`

Example: `studies/psychology/topics/paranoia.json`

```json
{
  "topic_id": "TOPIC_PSY_paranoia",
  "study_id": "psychology",
  "canonical_name": "Paranoia",
  "slug": "paranoia",
  "status": "published",

  "definition": "...",
  "pkd_relevance": "...",
  "in_the_fiction": "...",
  "in_the_exegesis": "...",
  "intellectual_background": "...",
  "scholarly_debate": "...",
  "chronology_summary": "...",
  "contradictions_summary": "...",
  "related_thinkers": ["Laing", "Bateson", "Freud"],
  "editorial_notes": "...",
  "open_questions": ["Did PKD distinguish clinical paranoia from..."],

  "passage_count": 65,
  "evidence_count": 8,
  "contradiction_count": 4,

  "first_appearance": "1953",
  "peak_period_start": "1964",
  "peak_period_end": "1974",

  "evidence_packets": [
    {
      "ev_id": "SEV_PSY_PARANOIA_001",
      "claim_text": "PKD's paranoia intensified after the 1971 break-in...",
      "evidence_summary": "...",
      "confidence": "strong",
      "source_method": "llm",
      "lane_a_count": 3,
      "lane_b_count": 2,
      "lane_c_count": 1,
      "passages": [
        {
          "passage_id": 101,
          "lane": "A",
          "source_mode": "fiction",
          "doc_id": "DOC_ARCH_...",
          "doc_title": "A Scanner Darkly",
          "passage_text": "...",
          "matched_terms": ["paranoia"],
          "claim_type": "allegory",
          "confidence": "high"
        }
      ]
    }
  ],

  "contradictions": [
    {
      "contradiction_id": 7,
      "summary": "PKD describes paranoia as both illness and insight...",
      "explanation": "...",
      "contradiction_type": "fiction_vs_exegesis",
      "passage_a": {
        "passage_id": 101,
        "lane": "A",
        "doc_title": "A Scanner Darkly",
        "passage_text": "...",
        "source_mode": "fiction"
      },
      "passage_b": {
        "passage_id": 203,
        "lane": "B",
        "doc_title": "Exegesis",
        "passage_text": "...",
        "source_mode": "exegesis"
      }
    }
  ],

  "chronology": [
    {
      "year": "1953",
      "event_type": "fiction",
      "summary": "First paranoid protagonist appears in...",
      "doc_id": "DOC_...",
      "doc_title": "..."
    }
  ],

  "related_documents": [
    {
      "doc_id": "DOC_ARCH_...",
      "title": "A Scanner Darkly",
      "doc_type": "novel",
      "relevance": "primary",
      "passage_count": 12,
      "slug": "a-scanner-darkly"
    }
  ],

  "related_terms": [
    {
      "term_id": "TERM_paranoia",
      "canonical_name": "Paranoia",
      "slug": "paranoia",
      "relation_type": "primary"
    }
  ],

  "related_names": [
    {
      "name_id": "NAME_r_d_laing",
      "display_name": "R.D. Laing",
      "slug": "r-d-laing",
      "relation_type": "related"
    }
  ],

  "related_topics": [
    {
      "topic_id": "TOPIC_PSY_schizophrenia",
      "canonical_name": "Schizophrenia",
      "slug": "schizophrenia",
      "study_id": "psychology"
    }
  ]
}
```

**Route:** `/studies/psychology/paranoia`
**Page:** `TopicDetail.tsx`

---

## 4. Passages by Lane — embedded in topic detail

Passages are grouped within evidence packets (see above).
For the lane-filter UI, the frontend filters `evidence_packets[].passages[]` by `lane` field.

Lane values:
- `"A"` = Primary fiction (novels, stories)
- `"B"` = Exegesis, letters, interviews
- `"C"` = Criticism, biography, scholarship

Lane D (synthesis) = the dossier text itself (not a passage lane).

---

## 5. Directory Structure

```
site/public/data/studies/
  index.json                          # studies index
  ai/
    index.json                        # AI topic index
    topics/
      androids.json                   # topic detail
      simulation.json
      ...
  psychology/
    index.json                        # psychology topic index
    topics/
      paranoia.json                   # topic detail
      schizophrenia.json
      ...
```

---

## 6. Search Index Extension

The existing `search_index.json` will gain entries of type `"study_topic"`:

```json
{
  "type": "study_topic",
  "id": "TOPIC_PSY_paranoia",
  "title": "Paranoia",
  "slug": "paranoia",
  "study_id": "psychology",
  "description": "PKD's paranoia...",
  "route": "/studies/psychology/paranoia"
}
```
