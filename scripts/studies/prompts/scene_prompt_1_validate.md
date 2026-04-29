# Scene Validation Prompt — Paste into Claude Desktop App

## Task: Validate AI Scene Candidates

You are reviewing candidate passages from Philip K. Dick fiction that may
contain scenes dramatizing human-AI interaction.

A valid scene is a **bounded narrative episode** in which a human character
interacts with an AI, robot, android, artificial person, simulation system,
or machine intelligence in a way that dramatizes a conceptual issue.

For each candidate, determine:
1. Does this passage contain such a bounded scene?
2. If yes, where does the scene begin and end within the passage?
3. If no, why not?

## Input

Paste the contents of the batch JSON file below:

```json
PASTE_BATCH_JSON_HERE
```

## Output format

Return a JSON array. One object per candidate:

```json
[
  {
    "candidate_id": 12,
    "is_valid": true,
    "rejection_reason": null,
    "scene_start_phrase": "first 8 words where the scene begins",
    "scene_end_phrase": "last 8 words where the scene ends"
  },
  {
    "candidate_id": 13,
    "is_valid": false,
    "rejection_reason": "exposition_only",
    "scene_start_phrase": null,
    "scene_end_phrase": null
  }
]
```

## Rejection reasons (use exactly one if rejecting):
- `no_ai_entity` — no AI/robot/android/artificial entity present in scene action
- `no_interaction` — AI entity present but no human-AI interaction occurs
- `exposition_only` — passage discusses AI abstractly, no dramatized scene
- `too_fragmentary` — interaction present but too brief or incomplete to summarize

## Rules
- A mention of an android in narration is NOT a scene unless characters interact
- Inner monologue about an android counts only if it occurs during an interaction
- If multiple scenes exist in one passage, validate based on the strongest one

---

## Desktop App Instructions

1. Open the batch file (e.g., `batches/validate_batch_001.json`)
2. Copy this entire prompt
3. Replace `PASTE_BATCH_JSON_HERE` with the batch JSON content
4. Paste into Claude desktop app
5. Copy Claude's JSON response
6. Save to `results/validate_batch_001_result.json`
7. Repeat for each batch file
