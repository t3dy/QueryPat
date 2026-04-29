# Scene Summary Prompt — Paste into Claude Desktop App

## Task: Write Scene Label, Summary, Significance, and Select Excerpt

For each scene, produce four outputs based strictly on the passage text and
the work it comes from.

## Rules

- **Scene label**: A concise title for this episode (max 15 words).
- **Short summary**: 2-3 sentences. Narrate what happens. Name the
  participants. Note the outcome or state reached at the scene's end.
- **Significance**: 1-2 sentences. State what this specific scene reveals
  about the relationship between the human and artificial participants
  IN THIS PASSAGE. Do not make general claims about "PKD's themes" or
  "Dick's oeuvre." Ground every claim in what the passage text actually shows.
  The significance must be falsifiable against the passage.
- **Source excerpt**: Select the most dramatically revealing portion of the
  passage (under 150 words). Prefer dialogue or action over exposition.
  Trim to complete sentences. This must be a direct quote from the passage.

## Input

Paste the contents of the batch JSON file below:

```json
PASTE_BATCH_JSON_HERE
```

## Output format

```json
[
  {
    "candidate_id": 12,
    "scene_label": "Deckard administers the Voigt-Kampff test to Rachael",
    "short_summary": "Rick Deckard tests Rachael Rosen with the Voigt-Kampff empathy scale at the Rosen Association headquarters. Her responses are ambiguous, registering flat on several markers. The test concludes with Deckard unable to make a definitive determination.",
    "significance": "The scene dramatizes the inadequacy of a single empathy metric as a criterion for distinguishing human from android, as Rachael's responses fall into an interpretive gap the instrument cannot resolve.",
    "source_excerpt": "He seated himself at the testing table...",
    "excerpt_word_count": 87
  }
]
```

## Bad significance examples (DO NOT write like these):
- "This scene reflects PKD's lifelong preoccupation with the nature of consciousness."
- "Here Dick explores his recurring theme of empathy as the defining human quality."
- "This passage illustrates the classic Dickian concern with authenticity."

## Good significance examples (DO write like these):
- "The scene dramatizes the inadequacy of a single empathy metric as a criterion for distinguishing human from android, as Rachael's responses fall into an interpretive gap the instrument cannot resolve."
- "Deckard's hesitation to fire reveals that his professional certainty has eroded through direct contact with the android, whose behavior in the preceding exchange was indistinguishable from grief."

---

## Desktop App Instructions

1. Open the batch file (e.g., `batches/summarize_batch_001.json`)
2. Copy this entire prompt
3. Replace `PASTE_BATCH_JSON_HERE` with the batch JSON content
4. Paste into Claude desktop app
5. Copy Claude's JSON response
6. Save to `results/summarize_batch_001_result.json`
7. Repeat for each batch file
