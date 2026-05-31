# Style Guide: PKD on the Paranormal

Editorial guidelines for the index card summaries and full-page essays in the
Paranormal section (`site/public/data/paranormal/index.json`).

---

## Source Material

All content must be grounded in **verbatim citation from `exegesis_ordered.txt`**,
the 48,829-line chronologically sorted text of Philip K. Dick's *Exegesis*.
Line numbers refer to that file. Never paraphrase when Dick's own words are
available; never attribute to Dick a claim he does not make in the text.

---

## Card Summary (`card_summary`)

**Length:** 60–90 words.

**Purpose:** A stand-alone précis that communicates (a) the hypothesis Dick is
entertaining, (b) the specific paranormal mechanism, and (c) where it fits in
his oscillating interpretive framework.

**Rules:**
- Open with the hypothesis in Dick's terms, not the editor's.
- Name the specific technology, entity, or phenomenon (e.g. "Pulkovo
  Observatory", "Kozyrev time-energy", "OCCP micro-psi") rather than
  abstracting.
- If Dick later revises or rejects the hypothesis, note the oscillation in
  one clause ("He does not fully abandon this model").
- No rhetorical questions. No editorial adjectives like "fascinating" or
  "bizarre."
- Write in present tense (historical present) throughout.

**Example (PAR_001):**
> Dick's early reading of the phosphene activity of March 1974: visual noise
> was actually encoded signal from a Soviet psychotronic research arm he calls
> "OCCP." The phosphenes, in this model, were the carrier wave for a control
> command he was meant to receive and act on — but a 2,000-year-old Christian
> entity intercepted the signal before it reached him.

---

## Primary Quote (`primary_quote`)

**Length:** 25–200 words.

**Rules:**
- Transcribe verbatim from `exegesis_ordered.txt`. No ellipsis except where
  the omitted material is entirely parenthetical and does not affect meaning;
  if you use ellipsis, mark the line range explicitly.
- Prefer a passage that (a) names the mechanism explicitly and (b) could not
  be mistaken for theological or fictional writing — quotes that are clearly
  Dick reasoning about paranormal causation.
- One quote per entry. If two passages are equally strong, use the one that
  is more specific or less well-known.
- Record the line number as `primary_quote_line` using the format `"line NNN"`
  or `"lines NNN–MMM"`.

---

## Full Essay (`full_essay`)

**Length:** 350–550 words in three paragraphs.

**Structure:**

1. **Paragraph 1 — The Hypothesis:**
   State the paranormal claim in Dick's own terms, with at least one verbatim
   quotation. Explain what the mechanism is, where Dick encountered it, and
   when in the *Exegesis* chronology it appears.

2. **Paragraph 2 — The Evidence Dick Marshals:**
   Describe the specific experiential or textual evidence Dick offers in
   support (the phosphene activity, the timing of events, the resonance with
   fiction, the witness account, etc.). Include a second verbatim quotation
   where the text supports it.

3. **Paragraph 3 — Trajectory and Oscillation:**
   Describe where the hypothesis goes: does Dick intensify, revise, bracket,
   or ultimately discard it? Place it in the broader oscillation of the
   *Exegesis* (theological vs. paranormal vs. psychological frames). One
   sentence of contextualisation is acceptable; do not editorialize about
   whether the hypothesis is "correct."

**Rules:**
- Every claim about what Dick believes must be traceable to a specific passage.
- Minimum two verbatim quotations per essay (the primary quote may be one
  of them).
- Quotations within the essay are single-spaced inline, not block-indented.
- Use `\n\n` for paragraph breaks in the JSON string value (no HTML).
- Use `*italic*` for title emphasis (rendered by ReactMarkdown).
- Do not conclude with a verdict ("this is the most important…", "ultimately
  this theory fails…").

---

## Category Assignment (`category_slug`)

| `category_slug`         | Use for                                                             |
|-------------------------|---------------------------------------------------------------------|
| `soviet-psychotronic`   | Microwave beaming, OCCP, satellite override, Riga/Tesla apparatus  |
| `kozyrev-time-energy`   | Nikolai Kozyrev, Pulkovo, time as an energy field, dense time      |
| `precognition`          | Retrograde time perception, foreknowledge, Thomas as precog        |
| `esp-telepathy`         | Biological telepathy, Lem, Kozyrev-mechanism ESP, Peter Mann       |
| `valis-satellite`       | VALIS as orbiting intelligence, Pigspurt, ZEBRA, phosphene beaming |
| `anamnesis`             | Platonic recollection, golden fish sign, past-life unlocking       |
| `second-sight`          | Third eye, prophecy, palintropos, gift of sight restored           |
| `spiritual-paranormal`  | Holy Spirit as psi, Satan with psi powers, Elijah transmission     |
| `mind-control`          | Subliminal media, right-hemisphere programming, occult ruling-out  |

An entry belongs to the category whose mechanism Dick most extensively
theorises. Dual-category entries are not supported; pick the more specific.

---

## Related Slugs (`related_slugs`)

List 2–4 slugs of entries that share a mechanism, a source text, or a
conceptual tension with this entry. Mutual linking is preferred (if A
lists B, B should list A). Do not link entries merely because they share
a category.

---

## Tags (`tags`)

3–7 lowercase tags drawn from this controlled vocabulary (extend only if a
term appears at least three times across entries):

`3-74`, `anamnesis`, `astral-programming`, `Cold-War`, `divine-intervention`,
`ESP`, `Exegesis`, `fiction-as-prophecy`, `God`, `Holy-Spirit`,
`Ira-Einhorn`, `Kozyrev`, `Logos`, `Logos-Effect`, `mind-control`,
`OCCP`, `palintropos`, `parapsychology`, `phosphenes`, `precognition`,
`Pulkovo`, `reincarnation`, `Riga`, `satellite`, `second-sight`,
`Soviet`, `synchronicity`, `telepathy`, `Tesla`, `Thomas`,
`time-density`, `UBIK`, `VALIS`, `ZEBRA`

---

## What to Avoid

- **Speculation about the text**: if a mechanism is not explicitly named
  by Dick, do not infer it from context.
- **Theological framing as paranormal**: entries belong in the Theophanies
  section if the primary frame is divine revelation without a specific
  paranormal mechanism. The Paranormal section covers entries where Dick
  explicitly compares or conflates a theological explanation with a
  psychic/technological one.
- **Dismissal**: do not write "of course" or "predictably" or other
  distancing language. Dick took these hypotheses seriously; the entry
  should take them seriously too.
- **Updating the count**: the `total` field in `index.json` must equal
  `len(entries)`. When adding entries, update both.

---

## Generation

Run `python3 scripts/gen_paranormal.py` to regenerate
`site/public/data/paranormal/index.json` from the canonical source. Edit the
Python script, not the JSON file directly.
