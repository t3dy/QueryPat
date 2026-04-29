# Template — Biography Event

For: entries in `biography/curated.json` and the `biography_events` table.

## Required JSON fields

| Field | Description |
|-------|-------------|
| `id` | stable kebab-case ID (`pkd_bio_{year}_{slug}`) |
| `date` | ISO date or partial (`1974-02-20`, `1974-02`, `1974`, `c1974`) |
| `date_precision` | `day`, `month`, `year`, `decade`, `inferred` |
| `event` | one declarative sentence (see below) |
| `category` | from controlled vocabulary (see below) |
| `entities` | named people/places involved |
| `location` | `City, State` or specific venue |
| `source` | named scholar/biography/interview |
| `importance` | 1–5 (trivial → life-defining) |
| `reliability` | `confirmed`, `likely`, `self-report-only`, `disputed`, `contradicted`, `legendary` |
| `contradicted_by` | array of `{source, account}` when reliability is `disputed` or `contradicted` |
| `notes` | required when reliability ≠ confirmed |

## event field — writing rules
- One sentence.
- Declarative, neutral voice.
- Past tense.
- No interpretive verbs (*believed, feared, decided, realized, understood*).
- Allowed verbs: *wrote, moved, married, divorced, signed, met, attended, hospitalized, reported, drafted, sold, mailed, telephoned, dated, used (drugs), saw, heard, dreamed, claimed, told, denied*.

Wrong: *PKD realized that his break-in had been staged by the FBI.*
Right: *PKD wrote a letter to the FBI describing the November 1971 break-in and inviting investigation.*

## category controlled vocabulary
`birth`, `family`, `education`, `marriage`, `divorce`, `child`, `residence`, `move`, `employment`, `drug_use`, `illness`, `hospitalization`, `vision`, `mystical_event`, `publication`, `contract`, `finances`, `fbi_irs`, `break_in`, `correspondence`, `friendship`, `convention`, `interview`, `media_deal`, `legal`, `death`, `posthumous`, `other`.

## reliability — when to use which

| Tier | Use when |
|------|----------|
| `confirmed` | ≥2 independent sources across ≥2 evidentiary lanes agree |
| `likely` | One credible source, no contradicting account, plausible on context |
| `self-report-only` | Only PKD says it (Exegesis, letters, interviews) |
| `disputed` | Credible sources disagree substantively |
| `contradicted` | Directly refuted by a more reliable source |
| `legendary` | Circulated but unsourceable |

## contradicted_by — required when reliability ≠ confirmed

Format: array of objects describing the divergent account.
```json
"contradicted_by": [
  {
    "source": "Anne Dick, The Search for PKD",
    "account": "denies the staging hypothesis; reads the break-in as a real burglary",
    "lane": "E"
  }
]
```

## Known dispute zones (per ontology §4)
When the event touches one of these, reliability cannot be `confirmed` and `contradicted_by` is required:

1. The November 1971 break-in
2. 2-3-74 events (psychotic / mystical / TLE)
3. Drug use chronology
4. Vancouver suicide attempt (1972)
5. Anne Dick marriage breakdown
6. Composition order of the Exegesis
7. Bishop Pike sequence
8. High-school agoraphobia onset
9. CIA / Lem / "committee" claims

## Lint checklist
- [ ] `event` is one declarative sentence with no interpretive verbs.
- [ ] `source` non-empty.
- [ ] `reliability` set.
- [ ] `notes` non-empty if reliability ≠ confirmed.
- [ ] `contradicted_by` populated if reliability is `disputed` or `contradicted`.
- [ ] `entities` populated where named people are involved.
