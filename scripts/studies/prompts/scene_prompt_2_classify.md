# Scene Classification Prompt — Paste into Claude Desktop App

## Task: Extract Participants and Classify Interaction Type

For each validated scene from Philip K. Dick fiction, identify:
1. All participants in the human-AI interaction
2. The primary interaction type (and optional secondary type)

## Interaction Type Ontology

| Slug | Label | Use when... |
|---|---|---|
| `empathy_testing` | Empathy Testing | Formal or informal test of whether an entity is human or artificial |
| `interrogation` | Interrogation | Questioning an AI/android to extract information or assess nature |
| `deception` | Deception | AI/android passing as human, or human deceiving an AI |
| `empathy_failure` | Empathy Failure | Expected empathic response absent or unconvincingly simulated |
| `bureaucratic_enforcement` | Bureaucratic Enforcement | AI/machine system enforcing rules or social order |
| `labor_replacement` | Labor Replacement | Automation replacing human work, dramatized through character experience |
| `therapeutic_exchange` | Therapeutic/Advisory | AI providing counsel, therapy, or guidance |
| `romantic_ambiguity` | Romantic/Intimate Ambiguity | Romantic or sexual interaction with uncertain humanity |
| `identity_uncertainty` | Identity Uncertainty | Character's human/artificial status genuinely unclear |
| `suspicion` | Suspicion/Testing | Informal suspicion that someone may not be human |
| `surveillance` | Surveillance/Monitoring | AI system observing, recording, or controlling humans |
| `memory_manipulation` | Memory/Reality Manipulation | AI system altering memories, perceptions, or reality |
| `revolt` | Revolt/Resistance | AI entity resisting control, asserting autonomy, rebelling |
| `companionship` | Companionship | Non-romantic bonding, alliance, or dependency |
| `creation` | Creation/Awakening | AI entity created, activated, or becoming self-aware |
| `destruction` | Destruction/Retirement | Killing, deactivating, or dismantling an AI entity |

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
    "participants": [
      {
        "label": "Rick Deckard",
        "role": "human",
        "justification": "human bounty hunter administering the test"
      },
      {
        "label": "Rachael Rosen",
        "role": "android",
        "justification": "revealed as Nexus-6 android during the test"
      }
    ],
    "interaction_type": "empathy_testing",
    "interaction_type_secondary": "deception",
    "type_justification": "Deckard administers the Voigt-Kampff; Rachael's android identity is concealed"
  }
]
```

## Participant roles (use exactly one per participant):
- `human` — confirmed human character
- `android` — artificial humanoid, explicitly identified as such in the text
- `robot` — mechanical/non-humanoid artificial entity
- `ai` — software intelligence, computer system
- `simulation` — simulated entity or virtual being
- `ambiguous` — the text deliberately leaves their nature uncertain

## Rules
- Include only characters actively participating in the interaction, not bystanders
- Use the name as it appears in the passage text
- If a character's nature is revealed later in the novel but not in this passage, use `ambiguous`
- Choose the interaction type that best fits THIS specific scene, not the novel's overall theme

---

## Desktop App Instructions

1. Open the batch file (e.g., `batches/classify_batch_001.json`)
2. Copy this entire prompt
3. Replace `PASTE_BATCH_JSON_HERE` with the batch JSON content
4. Paste into Claude desktop app
5. Copy Claude's JSON response
6. Save to `results/classify_batch_001_result.json`
7. Repeat for each batch file
