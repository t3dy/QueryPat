# Template — PKD's Own Works (Fiction, Essays, Letters, Speeches)

For: novels, novellas, story collections, individual stories, essays, speeches, letter volumes.
Lane: **A** (Fiction) for novels and stories; **E** (Primary) for letters, essays, speeches, the Exegesis.

## card_summary
**Length:** 70–100 words.

**Required structure:**
1. Form, year written / year published, length, publication venue. For novels: first edition publisher.
2. The premise or occasion (for fiction, one-sentence premise; for essay/speech, the occasion).
3. Position in PKD's career — early commercial / mainstream period / SF mature period / late-period theological.

**Forbidden:** plot synopsis beyond the premise sentence. The site is not a synopsis library.

## page_summary
**Length:** 300–700 words.

### For novels and stories (Lane A)

**Required sections:**

1. **Bibliographic identity** — title, year written, year published, publisher, length, cover artist where known, working titles, alternates.
2. **Composition history** — when written, drafts, abandoned alternates, advance and contract details where known. Composition order matters: PKD wrote some novels in clusters; flag clustering.
3. **Premise** — one paragraph, no spoilers beyond what reviews give.
4. **Themes** — link to the Theme entities. State which themes this work most centrally treats.
5. **Vocabulary debuted or featured** — link to Dictionary terms that originate or peak here.
6. **Self-commentary in the Exegesis or letters** — link to relevant segments. PKD often re-read his own books and theorized them; record where he did so.
7. **Reception** — initial reviews (Lem, Spinrad, contemporary SF press), later academic readings (Robinson, Palmer, Freedman, Rossi).
8. **Adaptations** — where applicable, link to the Adaptation entity.

### For essays, speeches, letters, the Exegesis (Lane E)

If the document comments on one of PKD's novels, add an explicit cross-link to that novel's PKD on PKD entry.

**Required sections:**

1. **Bibliographic identity** — what the document is, when written, to whom (for letters), in what venue (for speeches).
2. **Occasion** — what prompted it.
3. **Argument or theme** — what PKD says.
4. **Vocabulary featured** — terms developed here.
5. **Cross-references** — what novels, what events, what other letters this document touches.

## Required JSON fields
- `is_pkd_authored` — `true`
- `evidentiary_lane` — `A` for fiction, `E` for nonfiction primary
- `source_reliability` — `primary`

## Lint checklist
- [ ] Distinguishes year written from year published.
- [ ] Names themes as linked entities.
- [ ] Names dictionary terms debuted or featured.
- [ ] No plot synopsis beyond premise.
- [ ] No interpretive overlay (interpretations attributed to scholars, not asserted).
