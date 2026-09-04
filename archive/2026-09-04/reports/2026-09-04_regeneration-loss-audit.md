# Regeneration loss audit (machine-generated)

Generated 2026-09-04 17:33 UTC by `scripts/safeguard/audit_regeneration.py`.

Every exporter was run into a throwaway directory and the result compared
to the live `site/public/data`. Anything listed here is populated in the
committed tree and absent or impoverished in a fresh export — that is,
editorial content with no source in the database.

## Totals

- live JSON files: **2704**
- regenerated JSON files: **2328**
- files a regeneration would not produce at all: **376**
- files that would lose content: **1048**
- distinct orphaned field paths: **426**

## Orphaned editorial fields

| Files affected | Field path | Example |
|---:|---|---|
| 673 | `segments:concise_summary` — value emptied | `segments/SEG_EXEG_1975-11-05_SECTION_013_01.json` |
| 673 | `segments:people_entities` — array replaced by non-array | `segments/SEG_EXEG_1975-11-05_SECTION_013_01.json` |
| 672 | `segments:texts_works` — array replaced by non-array | `segments/SEG_EXEG_1975-11-05_SECTION_013_01.json` |
| 672 | `segments:theological_motifs` — array replaced by non-array | `segments/SEG_EXEG_1975-11-05_SECTION_013_01.json` |
| 672 | `segments:symbols_images` — array replaced by non-array | `segments/SEG_EXEG_1975-11-05_SECTION_013_01.json` |
| 672 | `segments:tensions` — array replaced by non-array | `segments/SEG_EXEG_1975-11-05_SECTION_013_01.json` |
| 672 | `segments:evidence_quotes` — array replaced by non-array | `segments/SEG_EXEG_1975-11-05_SECTION_013_01.json` |
| 672 | `segments:uncertainty_flags` — array replaced by non-array | `segments/SEG_EXEG_1975-11-05_SECTION_013_01.json` |
| 671 | `segments:autobiographical` — array replaced by non-array | `segments/SEG_EXEG_1975-11-05_SECTION_013_01.json` |
| 662 | `segments:literary_self_ref` — array replaced by non-array | `segments/SEG_EXEG_1975-11-05_SECTION_013_01.json` |
| 447 | `segments:key_claims` — array replaced by non-array | `segments/SEG_EXEG_1975-11-05_SECTION_013_01.json` |
| 447 | `segments:recurring_concepts` — array replaced by non-array | `segments/SEG_EXEG_1975-11-05_SECTION_013_01.json` |
| 447 | `segments:reading_excerpt` — value emptied | `segments/SEG_EXEG_1975-11-05_SECTION_013_01.json` |
| 214 | `timeline:[].source_type` — field absent from regenerated output | `timeline/years/1940.json` |
| 191 | `timeline:[].date_display` — field absent from regenerated output | `timeline/years/1940.json` |
| 179 | `names:linked_segments` — array shrinks 1 -> 0 | `names/entities/al-hammond.json` |
| 161 | `timeline:[].location` — field absent from regenerated output | `timeline/years/1940.json` |
| 112 | `timeline:[].date_end` — value emptied | `timeline/years/1958.json` |
| 104 | `segments:key_claims` — array shrinks 6 -> 5 | `segments/SEG_EXEG_1976-09-15_Dorothy_147.json` |
| 103 | `timeline:[].source_name` — value emptied | `timeline/years/1958.json` |
| 62 | `segments:recurring_concepts` — array shrinks 8 -> 3 | `segments/SEG_EXEG_1976-09-15_Dorothy_148.json` |
| 51 | `timeline:[].importance` — field absent from regenerated output | `timeline/years/1940.json` |
| 48 | `segments:works_referenced` — array replaced by non-array | `segments/SEG_EXEG_1975-11-05_SECTION_013_03.json` |
| 41 | `segments:key_claims` — array shrinks 6 -> 4 | `segments/SEG_EXEG_1976-09-15_Dorothy_146.json` |
| 41 | `timeline:[].notes` — field absent from regenerated output | `timeline/years/1940.json` |
| 41 | `timeline:[].entities` — field absent from regenerated output | `timeline/years/1940.json` |
| 40 | `analytics.json:segments_per_year[].theophanies` — field absent from regenerated output | `analytics.json` |
| 36 | `segments:works_referenced` — array shrinks 2 -> 1 | `segments/SEG_EXEG_1975-11-05_SECTION_013_01.json` |
| 34 | `timeline:[].bio_id` — field absent from regenerated output | `timeline/years/1952.json` |
| 34 | `timeline:[].event_type` — field absent from regenerated output | `timeline/years/1952.json` |
| 34 | `timeline:[].source_name` — field absent from regenerated output | `timeline/years/1952.json` |
| 32 | `timeline:[].theophanies` — field absent from regenerated output | `timeline/index.json` |
| 30 | `segments:recurring_concepts` — array shrinks 8 -> 4 | `segments/SEG_EXEG_1976-09-15_Dorothy_154.json` |
| 28 | `studies:definition` — value emptied | `studies/ai/topics/artificial-persons.json` |
| 28 | `studies:pkd_relevance` — value emptied | `studies/ai/topics/artificial-persons.json` |
| 28 | `studies:in_the_fiction` — value emptied | `studies/ai/topics/artificial-persons.json` |
| 28 | `studies:in_the_exegesis` — value emptied | `studies/ai/topics/artificial-persons.json` |
| 28 | `studies:intellectual_background` — value emptied | `studies/ai/topics/artificial-persons.json` |
| 28 | `studies:scholarly_debate` — value emptied | `studies/ai/topics/artificial-persons.json` |
| 24 | `segments:works_referenced` — array shrinks 4 -> 1 | `segments/SEG_EXEG_1976-09-15_Dorothy_172.json` |
| 23 | `segments:works_referenced` — array shrinks 3 -> 1 | `segments/SEG_EXEG_1975-11-05_SECTION_013_12.json` |
| 23 | `segments:recurring_concepts` — array shrinks 10 -> 3 | `segments/SEG_EXEG_1976-09-15_Dorothy_167.json` |
| 20 | `segments:works_referenced` — array shrinks 3 -> 2 | `segments/SEG_EXEG_1976-09-15_Dorothy_189.json` |
| 20 | `timeline:[]._type` — field absent from regenerated output | `timeline/years/1975.json` |
| 20 | `timeline:[].summary` — field absent from regenerated output | `timeline/years/1975.json` |
| 19 | `segments:works_referenced` — array shrinks 4 -> 2 | `segments/SEG_EXEG_1976-09-15_Dorothy_192.json` |
| 19 | `timeline:[].date_end` — field absent from regenerated output | `timeline/years/1952.json` |
| 19 | `timeline:[].date_confidence` — field absent from regenerated output | `timeline/years/1952.json` |
| 16 | `segments:recurring_concepts` — array shrinks 9 -> 3 | `segments/SEG_EXEG_1978-10-10_SECTION_016_08.json` |
| 15 | `segments:works_referenced` — array shrinks 5 -> 2 | `segments/SEG_EXEG_1976-09-15_Dorothy_149.json` |
| 15 | `segments:recurring_concepts` — array shrinks 10 -> 4 | `segments/SEG_EXEG_1976-09-15_Dorothy_150.json` |
| 14 | `segments:works_referenced` — array shrinks 6 -> 2 | `segments/SEG_EXEG_1976-09-15_Dorothy_18.json` |
| 14 | `segments:recurring_concepts` — array shrinks 7 -> 3 | `segments/SEG_EXEG_1976-09-15_Dorothy_237.json` |
| 13 | `segments:recurring_concepts` — array shrinks 9 -> 4 | `segments/SEG_EXEG_1976-09-15_Dorothy_146.json` |
| 11 | `timeline:[].slug` — field absent from regenerated output | `timeline/years/1975.json` |
| 10 | `timeline:[].theophany_id` — field absent from regenerated output | `timeline/years/1975.json` |
| 10 | `timeline:[].name` — field absent from regenerated output | `timeline/years/1975.json` |
| 10 | `timeline:[].experience_type` — field absent from regenerated output | `timeline/years/1975.json` |
| 10 | `timeline:[].contested_status` — field absent from regenerated output | `timeline/years/1975.json` |
| 8 | `dictionary:[].first_appearance` — value emptied | `dictionary/index.json` |
| 8 | `dictionary:[].peak_usage_start` — value emptied | `dictionary/index.json` |
| 8 | `segments:key_claims` — array shrinks 5 -> 4 | `segments/SEG_EXEG_1976-09-15_Dorothy_184.json` |
| 7 | `timeline:[].parent_theophany_id` — field absent from regenerated output | `timeline/years/1975.json` |
| 6 | `segments:works_referenced` — array shrinks 7 -> 2 | `segments/SEG_EXEG_1976-09-15_Dorothy_152.json` |
| 5 | `segments:works_referenced` — array shrinks 5 -> 1 | `segments/SEG_EXEG_1976-09-15_Dorothy_176.json` |
| 4 | `segments:works_referenced` — array shrinks 8 -> 1 | `segments/SEG_EXEG_1976-09-15_Dorothy_154.json` |
| 4 | `segments:works_referenced` — array shrinks 8 -> 2 | `segments/SEG_EXEG_1976-09-15_Dorothy_171.json` |
| 4 | `segments:works_referenced` — array shrinks 4 -> 3 | `segments/SEG_EXEG_1976-09-15_Dorothy_19.json` |
| 4 | `segments:recurring_concepts` — array shrinks 12 -> 3 | `segments/SEG_EXEG_1978-10-10_SECTION_016_16.json` |
| 4 | `timeline:[].work_id` — field absent from regenerated output | `timeline/years/1975.json` |
| 4 | `timeline:[].canonical_title` — field absent from regenerated output | `timeline/years/1975.json` |
| 4 | `timeline:[].work_type` — field absent from regenerated output | `timeline/years/1975.json` |
| 4 | `timeline:[].category` — field absent from regenerated output | `timeline/years/1975.json` |
| 4 | `timeline:[].page_summary` — field absent from regenerated output | `timeline/years/1975.json` |
| 4 | `timeline:[].source_count` — field absent from regenerated output | `timeline/years/1975.json` |
| 4 | `timeline:[].page_count` — field absent from regenerated output | `timeline/years/1975.json` |
| 4 | `timeline:[].recurring_concepts` — array shrinks 2 -> 1 | `timeline/years/1981.json` |
| 3 | `dictionary:definition` — text shrinks 481 -> 85 | `dictionary/terms/godhead.json` |
| 3 | `segments:recurring_concepts` — array shrinks 11 -> 3 | `segments/SEG_EXEG_1976-09-15_Dorothy_147.json` |
| 3 | `segments:works_referenced` — array shrinks 7 -> 1 | `segments/SEG_EXEG_1976-09-15_Dorothy_153.json` |
| 3 | `segments:evidence_excerpts[].name` — field absent from regenerated output | `segments/SEG_EXEG_1976-09-15_Dorothy_20.json` |
| 3 | `segments:recurring_concepts` — array shrinks 6 -> 3 | `segments/SEG_EXEG_1976-09-15_Dorothy_234.json` |
| 3 | `timeline:` — array shrinks 3 -> 1 | `timeline/years/1940.json` |
| 3 | `timeline:` — array shrinks 4 -> 2 | `timeline/years/1944.json` |
| 2 | `dictionary:definition` — text shrinks 241 -> 85 | `dictionary/terms/advent.json` |
| 2 | `dictionary:definition` — text shrinks 461 -> 84 | `dictionary/terms/apollo.json` |
| 2 | `dictionary:definition` — text shrinks 583 -> 84 | `dictionary/terms/augustine.json` |
| 2 | `dictionary:definition` — text shrinks 447 -> 85 | `dictionary/terms/elijah.json` |
| 2 | `dictionary:definition` — text shrinks 434 -> 85 | `dictionary/terms/form.json` |
| 2 | `dictionary:definition` — text shrinks 405 -> 85 | `dictionary/terms/gestalt.json` |
| 2 | `dictionary:definition` — text shrinks 435 -> 85 | `dictionary/terms/kerygma.json` |
| 2 | `segments:key_claims` — array shrinks 7 -> 5 | `segments/SEG_EXEG_1976-09-15_Dorothy_148.json` |
| 2 | `segments:recurring_concepts` — array shrinks 12 -> 4 | `segments/SEG_EXEG_1976-09-15_Dorothy_149.json` |
| 2 | `segments:key_claims` — array shrinks 7 -> 4 | `segments/SEG_EXEG_1976-09-15_Dorothy_169.json` |
| 2 | `segments:recurring_concepts` — array shrinks 7 -> 4 | `segments/SEG_EXEG_1976-09-15_Dorothy_197.json` |
| 2 | `segments:works_referenced_canonical` — field absent from regenerated output | `segments/SEG_EXEG_1978-10-10_SECTION_016_218.json` |
| 2 | `timeline:` — array shrinks 6 -> 4 | `timeline/years/1942.json` |
| 2 | `timeline:` — array shrinks 4 -> 1 | `timeline/years/1956.json` |
| 2 | `timeline:` — array shrinks 6 -> 3 | `timeline/years/1958.json` |
| 2 | `timeline:` — array shrinks 5 -> 2 | `timeline/years/1962.json` |
| 2 | `timeline:` — array shrinks 7 -> 2 | `timeline/years/1963.json` |
| 2 | `timeline:[].seg_id` — field absent from regenerated output | `timeline/years/1976.json` |
| 2 | `timeline:[].doc_id` — field absent from regenerated output | `timeline/years/1976.json` |
| 2 | `timeline:[].title` — field absent from regenerated output | `timeline/years/1976.json` |
| 2 | `timeline:[].concise_summary` — field absent from regenerated output | `timeline/years/1976.json` |
| 2 | `timeline:[].recurring_concepts` — field absent from regenerated output | `timeline/years/1976.json` |
| 2 | `timeline:[].people_entities` — field absent from regenerated output | `timeline/years/1976.json` |
| 2 | `timeline:[].tensions` — field absent from regenerated output | `timeline/years/1976.json` |
| 2 | `timeline:[].word_count` — field absent from regenerated output | `timeline/years/1976.json` |
| 2 | `timeline:[].has_raw_text` — field absent from regenerated output | `timeline/years/1976.json` |
| 1 | `archive:` — array shrinks 241 -> 232 | `archive/index.json` |
| 1 | `dictionary:[].card_description` — text shrinks 300 -> 102 | `dictionary/index.json` |
| 1 | `dictionary:[].card_description` — text shrinks 299 -> 102 | `dictionary/index.json` |
| 1 | `dictionary:[].card_description` — text shrinks 300 -> 109 | `dictionary/index.json` |
| 1 | `dictionary:[].card_description` — text shrinks 300 -> 81 | `dictionary/index.json` |
| 1 | `dictionary:definition` — text shrinks 290 -> 85 | `dictionary/terms/adam.json` |
| 1 | `dictionary:definition` — text shrinks 614 -> 84 | `dictionary/terms/aristotle.json` |
| 1 | `dictionary:card_description` — text shrinks 196 -> 79 | `dictionary/terms/aristotle.json` |
| 1 | `dictionary:card_description` — text shrinks 199 -> 61 | `dictionary/terms/augustine.json` |
| 1 | `dictionary:definition` — text shrinks 527 -> 84 | `dictionary/terms/bacchae.json` |
| 1 | `dictionary:definition` — text shrinks 553 -> 84 | `dictionary/terms/bardo-thodol.json` |
| 1 | `dictionary:definition` — text shrinks 318 -> 84 | `dictionary/terms/beethoven.json` |
| 1 | `dictionary:definition` — text shrinks 412 -> 84 | `dictionary/terms/being.json` |
| 1 | `dictionary:definition` — text shrinks 537 -> 85 | `dictionary/terms/brahman.json` |
| 1 | `dictionary:definition` — text shrinks 486 -> 85 | `dictionary/terms/buckman.json` |
| 1 | `dictionary:definition` — text shrinks 530 -> 85 | `dictionary/terms/buddha.json` |
| 1 | `dictionary:definition` — text shrinks 564 -> 84 | `dictionary/terms/buddhism.json` |
| 1 | `dictionary:definition` — text shrinks 454 -> 84 | `dictionary/terms/cartesian.json` |
| 1 | `dictionary:definition` — text shrinks 236 -> 84 | `dictionary/terms/catholic.json` |
| 1 | `dictionary:definition` — text shrinks 224 -> 86 | `dictionary/terms/christian.json` |
| 1 | `dictionary:definition` — text shrinks 226 -> 85 | `dictionary/terms/christianity.json` |
| 1 | `dictionary:definition` — text shrinks 213 -> 84 | `dictionary/terms/church.json` |
| 1 | `dictionary:definition` — text shrinks 541 -> 85 | `dictionary/terms/cosmic-christ.json` |
| 1 | `dictionary:definition` — text shrinks 446 -> 84 | `dictionary/terms/covenant.json` |
| 1 | `dictionary:definition` — text shrinks 227 -> 84 | `dictionary/terms/creator.json` |
| 1 | `dictionary:definition` — text shrinks 267 -> 84 | `dictionary/terms/daniel.json` |
| 1 | `dictionary:definition` — text shrinks 505 -> 84 | `dictionary/terms/dante.json` |
| 1 | `dictionary:definition` — text shrinks 396 -> 84 | `dictionary/terms/darkness.json` |
| 1 | `dictionary:definition` — text shrinks 402 -> 84 | `dictionary/terms/dasein.json` |
| 1 | `dictionary:definition` — text shrinks 194 -> 84 | `dictionary/terms/diana.json` |
| 1 | `dictionary:definition` — text shrinks 518 -> 84 | `dictionary/terms/dionysus.json` |
| 1 | `dictionary:definition` — text shrinks 200 -> 84 | `dictionary/terms/divine.json` |
| 1 | `dictionary:definition` — text shrinks 413 -> 85 | `dictionary/terms/earth.json` |
| 1 | `dictionary:definition` — text shrinks 531 -> 84 | `dictionary/terms/empedocles.json` |
| 1 | `dictionary:card_description` — text shrinks 200 -> 66 | `dictionary/terms/empedocles.json` |
| 1 | `dictionary:definition` — text shrinks 229 -> 85 | `dictionary/terms/empire.json` |
| 1 | `dictionary:definition` — text shrinks 526 -> 84 | `dictionary/terms/eucharist.json` |
| 1 | `dictionary:definition` — text shrinks 242 -> 85 | `dictionary/terms/faith.json` |
| 1 | `dictionary:definition` — text shrinks 249 -> 85 | `dictionary/terms/fall.json` |
| 1 | `dictionary:definition` — text shrinks 233 -> 84 | `dictionary/terms/fate.json` |
| 1 | `dictionary:definition` — text shrinks 189 -> 85 | `dictionary/terms/father.json` |
| 1 | `dictionary:definition` — text shrinks 457 -> 85 | `dictionary/terms/felix.json` |
| 1 | `dictionary:definition` — text shrinks 522 -> 85 | `dictionary/terms/firebright.json` |
| 1 | `dictionary:definition` — text shrinks 444 -> 85 | `dictionary/terms/fish.json` |
| 1 | `dictionary:definition` — text shrinks 483 -> 84 | `dictionary/terms/frolix.json` |
| 1 | `dictionary:definition` — text shrinks 224 -> 85 | `dictionary/terms/gabriel.json` |
| 1 | `dictionary:definition` — text shrinks 185 -> 85 | `dictionary/terms/garden.json` |
| 1 | `dictionary:definition` — text shrinks 309 -> 85 | `dictionary/terms/gnostic.json` |
| 1 | `dictionary:definition` — text shrinks 583 -> 85 | `dictionary/terms/gnosticism.json` |
| 1 | `dictionary:definition` — text shrinks 244 -> 84 | `dictionary/terms/gods.json` |
| 1 | `dictionary:definition` — text shrinks 439 -> 85 | `dictionary/terms/gospel.json` |
| 1 | `dictionary:definition` — text shrinks 208 -> 84 | `dictionary/terms/grace.json` |
| 1 | `dictionary:definition` — text shrinks 412 -> 85 | `dictionary/terms/greek.json` |
| 1 | `dictionary:definition` — text shrinks 499 -> 84 | `dictionary/terms/hagia-sophia.json` |
| 1 | `dictionary:definition` — text shrinks 210 -> 85 | `dictionary/terms/hebrew.json` |
| 1 | `dictionary:definition` — text shrinks 482 -> 84 | `dictionary/terms/heraclitus.json` |
| 1 | `dictionary:card_description` — text shrinks 199 -> 70 | `dictionary/terms/heraclitus.json` |
| 1 | `dictionary:definition` — text shrinks 513 -> 85 | `dictionary/terms/hermetic.json` |
| 1 | `dictionary:definition` — text shrinks 213 -> 86 | `dictionary/terms/holy.json` |
| 1 | `dictionary:definition` — text shrinks 395 -> 84 | `dictionary/terms/indian.json` |
| 1 | `dictionary:definition` — text shrinks 240 -> 85 | `dictionary/terms/james.json` |
| 1 | `dictionary:definition` — text shrinks 448 -> 84 | `dictionary/terms/jason.json` |
| 1 | `dictionary:definition` — text shrinks 196 -> 84 | `dictionary/terms/jewish.json` |
| 1 | `dictionary:definition` — text shrinks 262 -> 84 | `dictionary/terms/jews.json` |
| 1 | `dictionary:definition` — text shrinks 245 -> 85 | `dictionary/terms/john.json` |
| 1 | `dictionary:definition` — text shrinks 437 -> 85 | `dictionary/terms/joint.json` |
| 1 | `dictionary:definition` — text shrinks 471 -> 85 | `dictionary/terms/judaism.json` |
| 1 | `dictionary:definition` — text shrinks 465 -> 85 | `dictionary/terms/karma.json` |
| 1 | `dictionary:definition` — text shrinks 428 -> 84 | `dictionary/terms/kathy.json` |
| 1 | `dictionary:definition` — text shrinks 438 -> 85 | `dictionary/terms/king-felix.json` |
| 1 | `dictionary:definition` — text shrinks 186 -> 85 | `dictionary/terms/king.json` |
| 1 | `dictionary:definition` — text shrinks 187 -> 85 | `dictionary/terms/kingdom.json` |
| 1 | `dictionary:definition` — text shrinks 488 -> 84 | `dictionary/terms/kosmos.json` |
| 1 | `dictionary:definition` — text shrinks 514 -> 84 | `dictionary/terms/krishna.json` |
| 1 | `dictionary:definition` — text shrinks 418 -> 85 | `dictionary/terms/light.json` |
| 1 | `dictionary:definition` — text shrinks 242 -> 84 | `dictionary/terms/luke.json` |
| 1 | `dictionary:definition` — text shrinks 550 -> 85 | `dictionary/terms/malebranche.json` |
| 1 | `dictionary:definition` — text shrinks 451 -> 84 | `dictionary/terms/maya.json` |
| 1 | `dictionary:definition` — text shrinks 425 -> 85 | `dictionary/terms/maze.json` |
| 1 | `dictionary:definition` — text shrinks 422 -> 84 | `dictionary/terms/messianic.json` |
| 1 | `dictionary:definition` — text shrinks 409 -> 85 | `dictionary/terms/mind.json` |
| 1 | `dictionary:definition` — text shrinks 480 -> 84 | `dictionary/terms/moses.json` |
| 1 | `dictionary:definition` — text shrinks 429 -> 85 | `dictionary/terms/nixon.json` |
| 1 | `dictionary:definition` — text shrinks 496 -> 84 | `dictionary/terms/nous.json` |
| 1 | `dictionary:definition` — text shrinks 512 -> 84 | `dictionary/terms/orphic.json` |
| 1 | `dictionary:definition` — text shrinks 565 -> 84 | `dictionary/terms/palmer-eldritch.json` |
| 1 | `dictionary:definition` — text shrinks 460 -> 84 | `dictionary/terms/pantocrator.json` |
| 1 | `dictionary:definition` — text shrinks 547 -> 84 | `dictionary/terms/paracelsus.json` |
| 1 | `dictionary:definition` — text shrinks 516 -> 85 | `dictionary/terms/parmenides.json` |
| 1 | `dictionary:card_description` — text shrinks 199 -> 77 | `dictionary/terms/parmenides.json` |
| 1 | `dictionary:definition` — text shrinks 265 -> 85 | `dictionary/terms/paul.json` |
| 1 | `dictionary:definition` — text shrinks 369 -> 84 | `dictionary/terms/phil.json` |
| 1 | `dictionary:definition` — text shrinks 389 -> 84 | `dictionary/terms/philip.json` |
| 1 | `dictionary:definition` — text shrinks 508 -> 85 | `dictionary/terms/philo.json` |
| 1 | `dictionary:definition` — text shrinks 524 -> 85 | `dictionary/terms/plato.json` |
| 1 | `dictionary:card_description` — text shrinks 194 -> 81 | `dictionary/terms/plato.json` |
| 1 | `dictionary:definition` — text shrinks 496 -> 85 | `dictionary/terms/plotinus.json` |
| 1 | `dictionary:definition` — text shrinks 207 -> 85 | `dictionary/terms/prison.json` |
| 1 | `dictionary:definition` — text shrinks 521 -> 85 | `dictionary/terms/pythagoras.json` |
| 1 | `dictionary:card_description` — text shrinks 198 -> 67 | `dictionary/terms/pythagoras.json` |
| 1 | `dictionary:definition` — text shrinks 379 -> 84 | `dictionary/terms/reality.json` |
| 1 | `dictionary:definition` — text shrinks 386 -> 85 | `dictionary/terms/roman.json` |
| 1 | `dictionary:definition` — text shrinks 338 -> 85 | `dictionary/terms/rome.json` |
| 1 | `dictionary:definition` — text shrinks 552 -> 84 | `dictionary/terms/runciter.json` |
| 1 | `dictionary:definition` — text shrinks 451 -> 85 | `dictionary/terms/satan.json` |
| 1 | `dictionary:definition` — text shrinks 455 -> 85 | `dictionary/terms/scanner.json` |
| 1 | `dictionary:definition` — text shrinks 356 -> 84 | `dictionary/terms/sein.json` |
| 1 | `dictionary:definition` — text shrinks 403 -> 84 | `dictionary/terms/self.json` |
| 1 | `dictionary:definition` — text shrinks 501 -> 84 | `dictionary/terms/shiva.json` |
| 1 | `dictionary:definition` — text shrinks 522 -> 84 | `dictionary/terms/sibyl.json` |
| 1 | `dictionary:definition` — text shrinks 508 -> 84 | `dictionary/terms/siddhartha.json` |
| 1 | `dictionary:definition` — text shrinks 292 -> 85 | `dictionary/terms/simon.json` |
| 1 | `dictionary:definition` — text shrinks 390 -> 85 | `dictionary/terms/soviet.json` |
| 1 | `dictionary:definition` — text shrinks 216 -> 86 | `dictionary/terms/spirit.json` |
| 1 | `dictionary:definition` — text shrinks 418 -> 84 | `dictionary/terms/star.json` |
| 1 | `dictionary:definition` — text shrinks 477 -> 85 | `dictionary/terms/stigmata.json` |
| 1 | `dictionary:definition` — text shrinks 346 -> 84 | `dictionary/terms/tessa.json` |
| 1 | `dictionary:definition` — text shrinks 395 -> 85 | `dictionary/terms/torah.json` |
| 1 | `dictionary:definition` — text shrinks 426 -> 85 | `dictionary/terms/urgrund.json` |
| 1 | `dictionary:definition` — text shrinks 315 -> 85 | `dictionary/terms/wisdom.json` |
| 1 | `dictionary:definition` — text shrinks 376 -> 85 | `dictionary/terms/world.json` |
| 1 | `dictionary:definition` — text shrinks 506 -> 84 | `dictionary/terms/xerox-missive.json` |
| 1 | `dictionary:definition` — text shrinks 498 -> 85 | `dictionary/terms/yang.json` |
| 1 | `dictionary:definition` — text shrinks 467 -> 84 | `dictionary/terms/zagreus.json` |
| 1 | `dictionary:definition` — text shrinks 493 -> 85 | `dictionary/terms/zebrapedia.json` |
| 1 | `dictionary:definition` — text shrinks 438 -> 84 | `dictionary/terms/zeus.json` |
| 1 | `dictionary:definition` — text shrinks 458 -> 84 | `dictionary/terms/zoroaster.json` |
| 1 | `segments:Analysis` — field absent from regenerated output | `segments/SEG_EXEG_1975-11-05_SECTION_013_07.json` |
| 1 | `segments:Kill the bastards,` — field absent from regenerated output | `segments/SEG_EXEG_1975-11-05_SECTION_013_16.json` |
| 1 | `segments:recurring_concepts[]` — text shrinks 135 -> 59 | `segments/SEG_EXEG_1976-09-15_Dorothy_146.json` |
| 1 | `segments:recurring_concepts[]` — text shrinks 123 -> 50 | `segments/SEG_EXEG_1976-09-15_Dorothy_146.json` |
| 1 | `segments:recurring_concepts[]` — text shrinks 155 -> 66 | `segments/SEG_EXEG_1976-09-15_Dorothy_147.json` |
| 1 | `segments:reading_excerpt` — text shrinks 402 -> 164 | `segments/SEG_EXEG_1976-09-15_Dorothy_147.json` |
| 1 | `segments:recurring_concepts[]` — text shrinks 130 -> 53 | `segments/SEG_EXEG_1976-09-15_Dorothy_148.json` |
| 1 | `segments:recurring_concepts[]` — text shrinks 155 -> 58 | `segments/SEG_EXEG_1976-09-15_Dorothy_149.json` |
| 1 | `segments:key_claims[]` — text shrinks 235 -> 102 | `segments/SEG_EXEG_1976-09-15_Dorothy_150.json` |
| 1 | `segments:recurring_concepts[]` — text shrinks 135 -> 67 | `segments/SEG_EXEG_1976-09-15_Dorothy_150.json` |
| 1 | `segments:recurring_concepts[]` — text shrinks 108 -> 52 | `segments/SEG_EXEG_1976-09-15_Dorothy_151.json` |
| 1 | `segments:reading_excerpt` — text shrinks 365 -> 159 | `segments/SEG_EXEG_1976-09-15_Dorothy_151.json` |
| 1 | `segments:key_claims[]` — text shrinks 289 -> 143 | `segments/SEG_EXEG_1976-09-15_Dorothy_152.json` |
| 1 | `segments:recurring_concepts[]` — text shrinks 124 -> 40 | `segments/SEG_EXEG_1976-09-15_Dorothy_152.json` |
| 1 | `segments:key_claims[]` — text shrinks 293 -> 119 | `segments/SEG_EXEG_1976-09-15_Dorothy_153.json` |
| 1 | `segments:key_claims[]` — text shrinks 281 -> 107 | `segments/SEG_EXEG_1976-09-15_Dorothy_153.json` |
| 1 | `segments:recurring_concepts[]` — text shrinks 146 -> 70 | `segments/SEG_EXEG_1976-09-15_Dorothy_153.json` |
| 1 | `segments:recurring_concepts[]` — text shrinks 146 -> 65 | `segments/SEG_EXEG_1976-09-15_Dorothy_153.json` |
| 1 | `segments:reading_excerpt` — text shrinks 331 -> 130 | `segments/SEG_EXEG_1976-09-15_Dorothy_153.json` |
| 1 | `segments:recurring_concepts[]` — text shrinks 150 -> 68 | `segments/SEG_EXEG_1976-09-15_Dorothy_154.json` |
| 1 | `segments:recurring_concepts[]` — text shrinks 153 -> 71 | `segments/SEG_EXEG_1976-09-15_Dorothy_154.json` |
| 1 | `segments:recurring_concepts[]` — text shrinks 155 -> 77 | `segments/SEG_EXEG_1976-09-15_Dorothy_154.json` |
| 1 | `segments:key_claims[]` — text shrinks 281 -> 139 | `segments/SEG_EXEG_1976-09-15_Dorothy_155.json` |
| 1 | `segments:key_claims[]` — text shrinks 268 -> 132 | `segments/SEG_EXEG_1976-09-15_Dorothy_155.json` |
| 1 | `segments:recurring_concepts[]` — text shrinks 152 -> 73 | `segments/SEG_EXEG_1976-09-15_Dorothy_156.json` |
| 1 | `segments:recurring_concepts[]` — text shrinks 142 -> 65 | `segments/SEG_EXEG_1976-09-15_Dorothy_156.json` |
| 1 | `segments:key_claims[]` — text shrinks 235 -> 116 | `segments/SEG_EXEG_1976-09-15_Dorothy_157.json` |
| 1 | `segments:key_claims[]` — text shrinks 240 -> 119 | `segments/SEG_EXEG_1976-09-15_Dorothy_158.json` |
| 1 | `segments:key_claims[]` — text shrinks 224 -> 109 | `segments/SEG_EXEG_1976-09-15_Dorothy_158.json` |
| 1 | `segments:recurring_concepts[]` — text shrinks 146 -> 67 | `segments/SEG_EXEG_1976-09-15_Dorothy_159.json` |
| 1 | `segments:key_claims[]` — text shrinks 275 -> 132 | `segments/SEG_EXEG_1976-09-15_Dorothy_160.json` |
| 1 | `segments:reading_excerpt` — text shrinks 353 -> 132 | `segments/SEG_EXEG_1976-09-15_Dorothy_160.json` |
| 1 | `segments:recurring_concepts[]` — text shrinks 115 -> 47 | `segments/SEG_EXEG_1976-09-15_Dorothy_161.json` |
| 1 | `segments:recurring_concepts[]` — text shrinks 102 -> 32 | `segments/SEG_EXEG_1976-09-15_Dorothy_161.json` |
| 1 | `segments:recurring_concepts[]` — text shrinks 171 -> 67 | `segments/SEG_EXEG_1976-09-15_Dorothy_162.json` |
| 1 | `segments:recurring_concepts[]` — text shrinks 179 -> 87 | `segments/SEG_EXEG_1976-09-15_Dorothy_162.json` |
| 1 | `segments:key_claims[]` — text shrinks 208 -> 24 | `segments/SEG_EXEG_1976-09-15_Dorothy_163.json` |
| 1 | `segments:key_claims[]` — text shrinks 245 -> 117 | `segments/SEG_EXEG_1976-09-15_Dorothy_164.json` |
| 1 | `segments:key_claims[]` — text shrinks 249 -> 114 | `segments/SEG_EXEG_1976-09-15_Dorothy_165.json` |
| 1 | `segments:reading_excerpt` — text shrinks 415 -> 114 | `segments/SEG_EXEG_1976-09-15_Dorothy_165.json` |
| 1 | `segments:works_referenced` — array shrinks 10 -> 1 | `segments/SEG_EXEG_1976-09-15_Dorothy_168.json` |
| 1 | `segments:recurring_concepts[]` — text shrinks 164 -> 79 | `segments/SEG_EXEG_1976-09-15_Dorothy_169.json` |
| 1 | `segments:key_claims[]` — text shrinks 196 -> 23 | `segments/SEG_EXEG_1976-09-15_Dorothy_172.json` |
| 1 | `segments:key_claims[]` — text shrinks 186 -> 82 | `segments/SEG_EXEG_1976-09-15_Dorothy_172.json` |
| 1 | `segments:key_claims[]` — text shrinks 194 -> 77 | `segments/SEG_EXEG_1976-09-15_Dorothy_172.json` |
| 1 | `segments:linked_names` — array shrinks 11 -> 0 | `segments/SEG_EXEG_1976-09-15_Dorothy_172.json` |
| 1 | `segments:key_claims[]` — text shrinks 206 -> 30 | `segments/SEG_EXEG_1976-09-15_Dorothy_174.json` |
| 1 | `segments:key_claims[]` — text shrinks 198 -> 62 | `segments/SEG_EXEG_1976-09-15_Dorothy_174.json` |
| 1 | `segments:key_claims[]` — text shrinks 229 -> 63 | `segments/SEG_EXEG_1976-09-15_Dorothy_174.json` |
| 1 | `segments:key_claims[]` — text shrinks 206 -> 68 | `segments/SEG_EXEG_1976-09-15_Dorothy_174.json` |
| 1 | `segments:key_claims[]` — text shrinks 169 -> 26 | `segments/SEG_EXEG_1976-09-15_Dorothy_175.json` |
| 1 | `segments:recurring_concepts[]` — text shrinks 188 -> 73 | `segments/SEG_EXEG_1976-09-15_Dorothy_176.json` |
| 1 | `segments:recurring_concepts[]` — text shrinks 145 -> 62 | `segments/SEG_EXEG_1976-09-15_Dorothy_178.json` |
| 1 | `segments:recurring_concepts` — array shrinks 11 -> 4 | `segments/SEG_EXEG_1976-09-15_Dorothy_180.json` |
| 1 | `segments:recurring_concepts` — array shrinks 13 -> 4 | `segments/SEG_EXEG_1976-09-15_Dorothy_193.json` |
| 1 | `segments:recurring_concepts` — array shrinks 6 -> 4 | `segments/SEG_EXEG_1976-09-15_Dorothy_206.json` |
| 1 | `segments:works_referenced` — array shrinks 6 -> 1 | `segments/SEG_EXEG_1976-09-15_Dorothy_218.json` |
| 1 | `segments:recurring_concepts[]` — text shrinks 144 -> 60 | `segments/SEG_EXEG_1976-09-15_Dorothy_223.json` |
| 1 | `segments:recurring_concepts[]` — text shrinks 178 -> 70 | `segments/SEG_EXEG_1976-09-15_Dorothy_224.json` |
| 1 | `segments:recurring_concepts[]` — text shrinks 159 -> 48 | `segments/SEG_EXEG_1976-09-15_Dorothy_229.json` |
| 1 | `segments:recurring_concepts[]` — text shrinks 153 -> 76 | `segments/SEG_EXEG_1976-09-15_Dorothy_229.json` |
| 1 | `segments:recurring_concepts[]` — text shrinks 172 -> 76 | `segments/SEG_EXEG_1976-09-15_Dorothy_229.json` |
| 1 | `segments:recurring_concepts[]` — text shrinks 132 -> 62 | `segments/SEG_EXEG_1976-09-15_Dorothy_232.json` |
| 1 | `segments:reading_excerpt` — text shrinks 363 -> 173 | `segments/SEG_EXEG_1976-09-15_Dorothy_232.json` |
| 1 | `segments:recurring_concepts[]` — text shrinks 138 -> 64 | `segments/SEG_EXEG_1976-09-15_Dorothy_234.json` |
| 1 | `segments:recurring_concepts[]` — text shrinks 163 -> 78 | `segments/SEG_EXEG_1976-09-15_Dorothy_240.json` |
| 1 | `segments:recurring_concepts[]` — text shrinks 156 -> 77 | `segments/SEG_EXEG_1976-09-15_Dorothy_240.json` |
| 1 | `segments:recurring_concepts[]` — text shrinks 125 -> 59 | `segments/SEG_EXEG_1978-10-10_SECTION_016_02.json` |
| 1 | `segments:recurring_concepts[]` — text shrinks 119 -> 59 | `segments/SEG_EXEG_1978-10-10_SECTION_016_02.json` |
| 1 | `segments:recurring_concepts[]` — text shrinks 157 -> 43 | `segments/SEG_EXEG_1978-10-10_SECTION_016_06.json` |
| 1 | `segments:recurring_concepts[]` — text shrinks 130 -> 63 | `segments/SEG_EXEG_1978-10-10_SECTION_016_07.json` |
| 1 | `segments:recurring_concepts[]` — text shrinks 162 -> 58 | `segments/SEG_EXEG_1978-10-10_SECTION_016_07.json` |
| 1 | `segments:recurring_concepts[]` — text shrinks 163 -> 73 | `segments/SEG_EXEG_1978-10-10_SECTION_016_10.json` |
| 1 | `segments:stimulate": (2) He (Aristotle) did hold that change & order needed explanation. God is the transcendent unmoved mover who causes change & also stimulates the world & all its parts to achieve proper goals. This unmoved mover causes change & inspires goal seeking without himself undergoing any changes. "(1)" Aristotle held that the existence of the world did not require any reference to a transcendent or ultimate power." * EB This fits exactly what I experienced. Aristotle held that god, the prime mover, was/is immaterial & did not occupy space. * This is contrasted to the JewishChristian view of God the creator of the universe. I always ^thought that Aristotle's "prime mover" was primary in time before the universe created it. But I see what he experienced as god as prime mover is exactly what I experienced in 3-74. When I saw Valis I saw Aristotle's God (prime mover; v. supra)! No - I saw its effects. This is why Valis has no body except the object & process possesses processes which he structures: as Aristotle says, he occupies no space. Aristotle also believes that certain causes lay within nature. (Immanent.) This was an important part of his physics. Aristotle's view, in contrast to the Jewish-xtian view, does not hold God to any other role in the world except stimulating "the world & all its parts to achieve proper gods… causes change & inspires goal seeking." He is not the author of the world or the basis of the world; his actions & role are limited to this "prime moving" force exerted, this "stimulation" of what to him is a given. It could exist - ie the world could exist - without him. But there would be no stimulation of it & all its parts ` — field absent from regenerated output | `segments/SEG_EXEG_1978-10-10_SECTION_016_101.json` |
| 1 | `segments:activity` — field absent from regenerated output | `segments/SEG_EXEG_1978-10-10_SECTION_016_101.json` |
| 1 | `segments:key_claims[]` — text shrinks 243 -> 117 | `segments/SEG_EXEG_1978-10-10_SECTION_016_104.json` |
| 1 | `segments:recurring_concepts[]` — text shrinks 133 -> 63 | `segments/SEG_EXEG_1978-10-10_SECTION_016_104.json` |
| 1 | `segments:key_claims[]` — text shrinks 256 -> 124 | `segments/SEG_EXEG_1978-10-10_SECTION_016_11.json` |
| 1 | `segments:recurring_concepts[]` — text shrinks 128 -> 59 | `segments/SEG_EXEG_1978-10-10_SECTION_016_110.json` |
| 1 | `segments:recurring_concepts[]` — text shrinks 136 -> 62 | `segments/SEG_EXEG_1978-10-10_SECTION_016_114.json` |
| 1 | `segments:evidence_excerpts[].match_slug` — field absent from regenerated output | `segments/SEG_EXEG_1978-10-10_SECTION_016_114.json` |
| 1 | `segments:key_claims[]` — text shrinks 158 -> 45 | `segments/SEG_EXEG_1978-10-10_SECTION_016_115.json` |
| 1 | `segments:recurring_concepts[]` — text shrinks 213 -> 99 | `segments/SEG_EXEG_1978-10-10_SECTION_016_117.json` |
| 1 | `segments:recurring_concepts[]` — text shrinks 183 -> 85 | `segments/SEG_EXEG_1978-10-10_SECTION_016_117.json` |
| 1 | `segments:recurring_concepts[]` — text shrinks 191 -> 63 | `segments/SEG_EXEG_1978-10-10_SECTION_016_117.json` |
| 1 | `segments:recurring_concepts[]` — text shrinks 151 -> 69 | `segments/SEG_EXEG_1978-10-10_SECTION_016_120.json` |
| 1 | `segments:works_referenced` — array shrinks 12 -> 2 | `segments/SEG_EXEG_1978-10-10_SECTION_016_125.json` |
| 1 | `segments:recurring_concepts[]` — text shrinks 196 -> 89 | `segments/SEG_EXEG_1978-10-10_SECTION_016_127.json` |
| 1 | `segments:works_referenced` — array shrinks 21 -> 4 | `segments/SEG_EXEG_1978-10-10_SECTION_016_13.json` |
| 1 | `segments:recurring_concepts[]` — text shrinks 157 -> 77 | `segments/SEG_EXEG_1978-10-10_SECTION_016_130.json` |
| 1 | `segments:recurring_concepts[]` — text shrinks 123 -> 45 | `segments/SEG_EXEG_1978-10-10_SECTION_016_131.json` |
| 1 | `segments:recurring_concepts[]` — text shrinks 150 -> 64 | `segments/SEG_EXEG_1978-10-10_SECTION_016_133.json` |
| 1 | `segments:recurring_concepts[]` — text shrinks 191 -> 79 | `segments/SEG_EXEG_1978-10-10_SECTION_016_133.json` |
| 1 | `segments:key_claims[]` — text shrinks 263 -> 118 | `segments/SEG_EXEG_1978-10-10_SECTION_016_15.json` |
| 1 | `segments:key_claims[]` — text shrinks 216 -> 102 | `segments/SEG_EXEG_1978-10-10_SECTION_016_15.json` |
| 1 | `segments:works_referenced_analysis` — field absent from regenerated output | `segments/SEG_EXEG_1978-10-10_SECTION_016_159.json` |
| 1 | `segments:reading_excerpt` — text shrinks 326 -> 129 | `segments/SEG_EXEG_1978-10-10_SECTION_016_16.json` |
| 1 | `segments:we need medical attention. {circled:"16"} prayer is information - literally about conditions within the circuits (system). "Tears" contained such info, literally, & tripped (for me, & possibly historically) the intervention, corrective circuit. VALIS is an info entity - I saw this. King Felix shows that victim [bilate?] had reoccured. "King Felix" is an index to the entire Acts [material?] in "Tears," and the Acts [material?] in info connecting our actual historic saturation to the connection circuit. It synthesizes the [?] of deviation from the [?] signal - & indicates a regression [along?] (a major) the form axis, a failure of the progressive dialectic. This is the mechanism of omniscience; this is how it works. The bad king (tyrant) sabotages the monitoring-connective circuit by blocking all distress signals aimed to trigger it. He suppresses any kind of [repetition?] (feedback) of his activities. Not only can I now see the purpose (function) of the Acts [material?] in "Tears" but, in fact, its necessity; it conveyed the info of a form regression to the King Felix [?] state which I then actually saw! (ala form axis regression in "Ubik` — field absent from regenerated output | `segments/SEG_EXEG_1978-10-10_SECTION_016_178.json` |
| 1 | `segments:Tears." I was a cover for him so he could monitor & repeat back, "Tears` — field absent from regenerated output | `segments/SEG_EXEG_1978-10-10_SECTION_016_178.json` |
| 1 | `segments:Unteleported Man" about Newcolonized- land - the garrison state at Whale's Mouth! Which is why I dreamed the key cypher ` — field absent from regenerated output | `segments/SEG_EXEG_1978-10-10_SECTION_016_178.json` |
| 1 | `segments:Tears" constituted a written prayer "Zebra is an invader.` — field absent from regenerated output | `segments/SEG_EXEG_1978-10-10_SECTION_016_178.json` |
| 1 | `segments:Tears.` — field absent from regenerated output | `segments/SEG_EXEG_1978-10-10_SECTION_016_178.json` |
| 1 | `segments:raw_text` — text shrinks 41145 -> 11726 | `segments/SEG_EXEG_1978-10-10_SECTION_016_180.json` |
| 1 | `segments:recurring_concepts[]` — text shrinks 145 -> 67 | `segments/SEG_EXEG_1978-10-10_SECTION_016_21.json` |
| 1 | `segments:linked_terms[].matched_type` — field absent from regenerated output | `segments/SEG_EXEG_1978-10-10_SECTION_016_219.json` |
| 1 | `segments:recurring_concepts[]` — text shrinks 173 -> 85 | `segments/SEG_EXEG_1978-10-10_SECTION_016_25.json` |
| 1 | `segments:Final world" refers to temporal succession, to the succession of Ages. "The time you've waited for has come. The final world is here. The work is completed. He has been transplanted and is alive.` — field absent from regenerated output | `segments/SEG_EXEG_1978-10-10_SECTION_016_252.json` |
| 1 | `segments:says` — field absent from regenerated output | `segments/SEG_EXEG_1978-10-10_SECTION_016_256.json` |
| 1 | `segments:evidence_excerpts[].,
      "matched_alias` — field absent from regenerated output | `segments/SEG_EXEG_1978-10-10_SECTION_016_274.json` |
| 1 | `segments:recurring_concepts[]` — text shrinks 176 -> 48 | `segments/SEG_EXEG_1978-10-10_SECTION_016_28.json` |
| 1 | `segments:recurring_concepts[]` — text shrinks 116 -> 53 | `segments/SEG_EXEG_1978-10-10_SECTION_016_30.json` |
| 1 | `segments:recurring_concepts[]` — text shrinks 157 -> 78 | `segments/SEG_EXEG_1978-10-10_SECTION_016_30.json` |
| 1 | `segments:analysis_fields_populated` — field absent from regenerated output | `segments/SEG_EXEG_1978-10-10_SECTION_016_30.json` |
| 1 | `segments:analysis_date` — field absent from regenerated output | `segments/SEG_EXEG_1978-10-10_SECTION_016_30.json` |
| 1 | `segments:but` — field absent from regenerated output | `segments/SEG_EXEG_1978-10-10_SECTION_016_310.json` |
| 1 | `segments:+ the Logos became flesh" - after his resurrection he still had a body, but before the incarnation he did not. Think of what this statement must have meant to the Greco-Roman world: "The Logos became flesh [in Jesus Christ]"! With what they knew about the Logos. (Which we do not.) The point of this would be to reannex creation back to God or - to spiritualize hyle? Spirit penetrates matter? Then probably unspiritual matter was a fallen creation; this is the great restoration discussed in the captivity letters. Yes: Valis is a penetration of the physical (matter as field) by spirit. This is different from pantheism, so physicists will find that reality behaves more and more like Brahman + in Taoism, but this is a dynamic on-going process, I know {I know it} Suddenly I see it all: "The logos became flesh," + this set off a logos-ization of reality itself, a strategy. No longer was Hagia Sophia outside of creation but at its physical core! It is Christ (if one understands that Christ is the Logos). This can be done because, as we have now realized, what we call "material physical reality" is a field. Again: arrangements of our media information are not due to Valis' thoughts but are Valis' thoughts; Valis is building itself a physical body. +, since Valis is information, physical information occurs; Valis uses our world as a carrier on which to record (perhaps record memories? What I saw + am seeing is a memory system; I think Jeter pointed this out). No, it is not memory + it is not cypher + it is not communication; it is its (Valis') thoughts; it is thinking; this is a process (but it can record + hence remember its own thoughts). Physical matter ("the reality field") has been invaded by mind or spirit + therefore is becoming spiritualized, literally. It has to think through arrangements of our media info because this [physical world] is the only brain it has; apparently as with us mind is the result of brain, the neural connections - literal + physical (but also involving energy - the plasmate). This is why I say, "it doesn't arrange [our] info by its thoughts; the arrangements -inc. linkings and relinkings- are its thoughts.` — field absent from regenerated output | `segments/SEG_EXEG_1978-10-10_SECTION_016_312.json` |
| 1 | `segments:unsuspected` — field absent from regenerated output | `segments/SEG_EXEG_1978-10-10_SECTION_016_313.json` |
| 1 | `segments:Parsifal" deals with the Son, it is penultimate, which I did not suspect. From salvation, blood + the cross to - agapē. From this world (2-3-74, the crucifixion) to the next (the Father + his love, not world). The blood + the cross are the highest point of this world. (2-3-74.) Then tears -"of the repentant sinner"- turn to agapē, as in "Tears"; the tears has to do with sin + atonement + Christ + the cross, but all this [sorrow] is a gate to: love. (V. "Tears"!) + love (agapē) equals ecstasy; so tears + sorrow -the cross- are converted into their opposite: joy. Through agapē; this is the goal + mystery of Xtianity, this conversion: utter sorrow (Mitleid) to bliss (agapē). This is "pity's highest power", it leads to bliss since agapē links pity (compassion) to joy - compassion becomes or even is (!!) agapē, + agapē ushers in joy because it (starting as Mitleid) ends up in God, since agapē is his einai. So compassion (Mitleid) is the road from this world to God; hence the crucifixion + the feelings engendered lead to God the Father because of the common element of agapē: this is the miraculous healing of Amfortas' wound. You cannot feel Mitleid without feeling agapē, + you cannot feel agapē without entering into and sharing God's esse. This is what happens at the ending of "Tears," based on my experience in '70, of sorrow becoming compassion becoming love, +, in 3-74, joy; + in 11-17-80 reaching God + his pure agapē nature. Somehow my action vis-à-vis Covenant House fits into this sorrow-compassion-agapē-joy-God sequence. So it's all based on my earlier sorrows, circa 1970! When I was writing "Tears"! Compassion (Mitleid) is a blend of sorrow + love. Thus it is the nexus between sorrow + joy - joy entering because love leads to God. So I now know what "Mitleids Höchtest Macht" refers to. Sorrow to compassion to agapē to God to bliss. The way of the cross now makes sense to me. I understand why Jesus had to die + in the way he did, if he was to be a gate[way] to the Father. The transfiguration in me occurred when I had the dream: punishment (death) exacted on Honor Jackson as justice for what he had done (the talion law). But, seeing this (the O.T.) I felt compassion (which I experienced as sorrow). This took me from the era of justice to the era of mercy, and out from under the law of justice in my own case; it also led me eventually to God through Christ. The old king in the dream is YHWH of the O.T., exacting justice; but, through compassion (Mitleid) I opted for the N.T. in place of the law, I mean agapē + that God (?) (era, maybe: 3rd Torah). So mercy was later (3-74) applied to my case. But it took the dream to convert my sorrow to Mitleid - upon seeing the sentence of justice imposed: death. Without the dream my sorrow (at the loss of Nancy) would have stayed simply sorrow; + the dream was based on the rat experience, which roused vast compassion in me + was the root moksa/religious experience! + it, in turn, was based on the beetle incident when I was in the 4th grade! + in the '60s the Galapagos turtle compassion. At which point the A.I. voice spoke to me! So my whole development was guided along over the decades since childhood. The first episode was my throwing the cat down the stairs - + feeling sorrow for it. The slayer sees himself in what he slays: tat tvam asi. The moment comes in biological evolution where the slayer looks into the eyes of him who he slays + sees himself as the slain, at which point he can no longer slay + his will (in Schopenhauer's sense) doubles back onto itself, is extinguished; the entire dynamism of individual striving self is annihilated - billions of years of this identity + will perish; + the person is freed from this will, the real Karmic factor/drive. Thus my several moments (i.e. with the cat I was throwing down stairs, then the beetle, then the rat, then with Honor Jackson) are significant moments of enlightenment involving this "tat tvam asi," this Brahmanist slayer-slain identification, the extinction of my biological will which is the dynamism of Spinoza's "each creature seeks to persist in its essence, to be", each instance was a further dying of this individuality, this drive to indivually be, replaced by another kind of einai when I + the slain (the other) were one - Brahman-consciousness. I could no longer be an individual bipolarized against all other individuals asserting my needs, desires, power + will against them to fulfill my own wants (striving, craving). These several evolutionary steps are irreversible. They have a "bad" side in that they involved me in the Buddhist perception of world suffering (which cannot be separated from compassion to which this perception gives rise); but this perception + the compassion it gives rise to is precisely the means to release from the wheel of birth + rebirth, since your ego -regarded by the Buddha as irreal- is extinguished with your will - + what is finally led to is the ecstasy of Nirvana - i.e. 11-17-80. This appears in "VR" in the dying dog in the ditch scene + Emmanuel's series of responses: it leads to sorrow + compassion for him, + a return of his memories - i.e. true identity (his Brahman-atman God nature). So the etiology of 11-17-80 lies in 3-74 which is rooted in the dream + sorrow, compassion + love put into "Tears" in 1970, + then back to the rat, + the beetle + the cat (+ the Galapagos turtles), to my whole "Atlas" empath nature. In Western terms it leads to God because God's nature is love, but Indian thought gives a more penetrating analysis of why Mitleid is the means to salvation. Thus my act vis-à-vis Covenant House is representative + symbolic of my freed (enlightened) Buddha nature. It was a paying off of my Karmic cebt. Paradoxically, this enlightened nature creates severe problems for me in wanting things (i.e. in acquiring), +, too, it was the basis of my anti-war stand, leading to the tax situation. That 2-3-74 + 11-17-80 were genuine I cannot now doubt, having perceived this life-history (of progressive moksa) of stages of loss of striving + self (the two are the same). Both Xtianity + Buddhism-Brahmanism lead to the same goal, because both are based on compassion (for India this means the loss of self; for the Xtian it means experiencing agapē hence God, since agapē is his nature). Hence I can now link Xtianity with pan-Indian thought through the "slayer + the slain" compassion. Identification; this is one road + it does lead to release. It leads specifically to the perception of reality as one total sentient field, i.e. Valis (Brahman or the Cosmic Christ) of which you are a part. So Valis is Brahman, but also yourself + also -hence- Christ, since yourself now has given birth to the Godhead i.e. Christos in you: the you it (or you not-you) dualism has been literally abolished! Compassion led to this [experience]; this is 3-74, my perception of Valis: this is perception of Brahman via the Xtian route. Thus my entire life led up to 3-74 + seeing Valis, + this in turn led logically to 11-17-80 - Xtian Nirvana. To meeting God (the Xtian God of love; viz: 3-74 was Brahman, i.e. Eastern; 11-17-80 was Western + Xtian; both are true, + both are reached by the one route of compassion). So 3-74 represented the final extinction of my individual self + a return to Brahman (God) + it is a culmination of a lifetime of moksa-compassion experiences that finally released me from Karma + Maya; + I saw the God-field. I was led along this route (journey) by God. From moksa to moksa. + it's all in "VR," in the dying dog in the ditch + Emmanuel's anamnesis + recovery of his true identity. Buddha + Schopenhauer: abolishing one's cravings i.e. will; but more profound is the Brahman slayer-slain recognition: "I am that which I slay," which abolishes self on the spot. This is the real insight. Tha "slayer-slain" identification is literally a perception, a realization of a fact, a true real fact; one does not just project one's own feelings onto/into the other (this is empathy); no: one realizes one is [also] the other. This is the crucial epistemological discovery set off by compassion, i.e. compassion leads to knowledge: that one is not oneself truly but - okay. "Tat tvam asi," as Sankara pointed out. + if one is",
  "raw_text_char_count` — field absent from regenerated output | `segments/SEG_EXEG_1978-10-10_SECTION_016_313.json` |
| 1 | `segments:evidence_excerpts[].maybe` — field absent from regenerated output | `segments/SEG_EXEG_1978-10-10_SECTION_016_313.json` |
| 1 | `segments:works_referenced_updated` — field absent from regenerated output | `segments/SEG_EXEG_1978-10-10_SECTION_016_319.json` |
| 1 | `segments:recurring_concepts[]` — text shrinks 190 -> 69 | `segments/SEG_EXEG_1978-10-10_SECTION_016_34.json` |
| 1 | `segments:recurring_concepts[]` — text shrinks 192 -> 95 | `segments/SEG_EXEG_1978-10-10_SECTION_016_34.json` |
| 1 | `segments:Pentheus" by Dionysos (Taverner) is converted (by the dream, which is of Christ) into agapÄ" which is sane - the solution to dromsis + madness + grief + loss is found in Xtian agapÄ` — field absent from regenerated output | `segments/SEG_EXEG_1978-10-10_SECTION_016_344.json` |
| 1 | `segments:Felix" vs "Pentheus"). (joy over Tears.) Hence I may have been let in on a mystery of transformation far greater than a political historical power struggle + all this is dealt the inner meaning with in "Tears" of Xtianity - its true meaning - may be represented by "Felix," + its enemy - that which it overcomes - by Tears, i.e. the BIP. The ultimate struggle, then, is spiritual, not physical or literal. Xtianity converts doom into joy by means of agapÄ" this (agapÄ") being the einai of God (as previously figured out. Doom, I identified with death, hence loss, defeat, grief, transmuted through agapÄ" to the infinite bliss (joy) of ature ods 40 This then, is the real victory of Xtianity. doom, loss, grief, love, joy. A kind of ultimate Catharsis unknown before Xtianity because it was not known that agapÄ" is God's nature. Hence through agapÄ` — field absent from regenerated output | `segments/SEG_EXEG_1978-10-10_SECTION_016_344.json` |
| 1 | `segments:even though I die + die awfully, I tell you that God's love never ends." This is why the crucial utterance on the cross, "Eli, Eli, Lahma Sabachthani? Is correctly seen as the key to Jesus' dual nature As God he believed; as as both God + man. man he doubted. Man believing, trusting that God will not desert him, becomes God himself. This is the man-God, the goal of define t Xtianity, the imitation of Christ. "Christos" as that man who knows despite everything, despite world that as fate degrades) destroys him, that God loves him + will never cease loving him. + if God loves him - God's nature (einai) being love (agape) - God will prove his theodicy: he will not harm man, or allow harm to come to man, needlessly; in some way this evident harm will be offset - in fact more than offset, by God himself, acting out of absolute eternal love for man. It cannot be otherwise to the Xtian. "For a little while," is the belief of the Xtian about world, the world as then ordeal. A finite ordeal infinite bliss in the return to God from whom he originally came the finite bad balanced against the infinite good this is the Xtian's understanding. This is how he correctly views his defeat at the hands of world. +, from this view, he confronts world unflinchingly, the first person ever to do so Thus he becomes Christos. + is saved. +, At the heart of these understanding + per‐ D-162 ceptions, this knowing the truth + facing the inds truth, he, a vast, fierce joy, a joy unfathomed by any man before him I the joy of knowing that God has delivered him out of danger + into safety. Without end. This transformation from acceptance into joy which is the heart of Xtianity is called "the resurrection." Jesus knew it first; we know",
  "linked_terms` — field absent from regenerated output | `segments/SEG_EXEG_1978-10-10_SECTION_016_358.json` |
| 1 | `segments:recurring_concepts[]` — text shrinks 149 -> 74 | `segments/SEG_EXEG_1978-10-10_SECTION_016_37.json` |
| 1 | `segments:recurring_concepts` — array shrinks 14 -> 3 | `segments/SEG_EXEG_1978-10-10_SECTION_016_40.json` |
| 1 | `segments:words_referenced` — field absent from regenerated output | `segments/SEG_EXEG_1978-10-10_SECTION_016_42.json` |
| 1 | `segments:recurring_concepts[]` — text shrinks 107 -> 40 | `segments/SEG_EXEG_1978-10-10_SECTION_016_52.json` |
| 1 | `segments:recurring_concepts[]` — text shrinks 140 -> 69 | `segments/SEG_EXEG_1978-10-10_SECTION_016_55.json` |
| 1 | `segments:recurring_concepts[]` — text shrinks 147 -> 71 | `segments/SEG_EXEG_1978-10-10_SECTION_016_55.json` |
| 1 | `segments:recurring_concepts[]` — text shrinks 160 -> 78 | `segments/SEG_EXEG_1978-10-10_SECTION_016_59.json` |
| 1 | `segments:recurring_concepts[]` — text shrinks 204 -> 85 | `segments/SEG_EXEG_1978-10-10_SECTION_016_60.json` |
| 1 | `segments:recurring_concepts[]` — text shrinks 185 -> 80 | `segments/SEG_EXEG_1978-10-10_SECTION_016_60.json` |
| 1 | `segments:reading_excerpt` — text shrinks 343 -> 122 | `segments/SEG_EXEG_1978-10-10_SECTION_016_61.json` |
| 1 | `segments:reading_excerpt` — text shrinks 401 -> 161 | `segments/SEG_EXEG_1978-10-10_SECTION_016_62.json` |
| 1 | `segments:key_claims[]` — text shrinks 289 -> 17 | `segments/SEG_EXEG_1978-10-10_SECTION_016_64.json` |
| 1 | `segments:key_claims[]` — text shrinks 215 -> 106 | `segments/SEG_EXEG_1978-10-10_SECTION_016_64.json` |
| 1 | `segments:works_referenced` — array shrinks 10 -> 2 | `segments/SEG_EXEG_1978-10-10_SECTION_016_66.json` |
| 1 | `segments:key_claims[]` — text shrinks 153 -> 70 | `segments/SEG_EXEG_1978-10-10_SECTION_016_69.json` |
| 1 | `segments:key_claims[]` — text shrinks 188 -> 71 | `segments/SEG_EXEG_1978-10-10_SECTION_016_69.json` |
| 1 | `segments:key_claims[]` — text shrinks 171 -> 70 | `segments/SEG_EXEG_1978-10-10_SECTION_016_69.json` |
| 1 | `segments:key_claims` — array shrinks 8 -> 5 | `segments/SEG_EXEG_1978-10-10_SECTION_016_71.json` |
| 1 | `segments:key_claims[]` — text shrinks 163 -> 54 | `segments/SEG_EXEG_1978-10-10_SECTION_016_74.json` |
| 1 | `segments:key_claims[]` — text shrinks 143 -> 48 | `segments/SEG_EXEG_1978-10-10_SECTION_016_74.json` |
| 1 | `segments:key_claims[]` — text shrinks 193 -> 79 | `segments/SEG_EXEG_1978-10-10_SECTION_016_74.json` |
| 1 | `segments:recurring_concepts` — array shrinks 15 -> 3 | `segments/SEG_EXEG_1978-10-10_SECTION_016_77.json` |
| 1 | `segments:recurring_concepts` — array shrinks 13 -> 3 | `segments/SEG_EXEG_1978-10-10_SECTION_016_81.json` |
| 1 | `segments:works_referenced_pdk` — field absent from regenerated output | `segments/SEG_EXEG_1978-10-10_SECTION_016_87.json` |
| 1 | `segments:reading_excerpt` — text shrinks 270 -> 113 | `segments/SEG_EXEG_1978-10-10_SECTION_016_88.json` |
| 1 | `segments:works_referenced` — array shrinks 5 -> 3 | `segments/SEG_EXEG_1978-10-10_SECTION_016_95.json` |
| 1 | `segments:reading_excerpt` — text shrinks 453 -> 154 | `segments/SEG_EXEG_1978-10-10_SECTION_016_97.json` |
| 1 | `segments:Tears") no one 1900 years ago could have written that. The Holy Spirit wrote it. So what I realized light night (via Luke & the "Bishop Archer" novel) is that when the Holy Spirit descends on you, it creates a Christos out of you permanently as the final birth in evolution of what you already potentially are (Bill is a perfect example of this) it is the culmination of what must be a series of Growth-steps. But this final one requires the "Birth in the Spirit" no matter how far along you've advanced in enlightenment, the Spirit Then, in 2-3-74, didn't enter me just to decypher call or even rescue me (pronoia); what we have here is "Birth in the Spirit" & son of God adopting as co-heir (with Christ) & son of God (the spirit being God's spirit ). I guess this is a hierogamy. I discuss this in "Valis": the interspecies symbiosis with the plasmate to form the homoplasmate, the metaphor of Bride & Wedding may not be metaphoric at all. It just seems to me that the N.T. is really clear about all this - this is not a forced",
  "raw_text_char_count` — field absent from regenerated output | `segments/SEG_EXEG_1981-04-16_Pat_33.json` |
| 1 | `segments:Messenger" vision fit in with my sense that Christ literally replaces the dying creature + dies it (his) death for it (him)? The endangered creature - person - becomes ditheon at the moment of his fate-crisis, + Christ deals with the person's lethal (deadly) fate - thus (as I say) thwarting the retributive machinery now identified with Karma + fate in this life. the messenger dream referred to the Xerox they is this life, not just the nex missive a co (353 dream: there is a group of us. We discover that reality - the universe - is actually info one of us (a girl) recognizes the info as the own prior thought. With a groan I realize that this means the universe is based on our cha prior thoughts. We are forgetful cosmocrators, trapped in a universe of our own making "I wont without our knowing it. + I think, believe this when I wake up because the implica ims are too depressing + radical." It is like "maze." The trail which I relentlessl pursue in my exegesis consists of woozle tracks that lead back to -surprise -myself in discovering the laws of God I am doing nothing more than discovering my own nature dextreporld. The "Grand illusion" is as in in fact the grand tautology. Finally decypher the writing (info, messages as basis of reality) + discover I've written it myself: imprisoned in my own mind, with my recirculated thoughts as in "Frozen Journey" - solipsism. Thus no new knowledge is possible (i.e. synthetic propo t sitions) conly analytical). I thought, "prajapati the "wholly other" is not "other" at all: the mood of the dream upon the discovery was grim The drear implication here has to do with I call "prior thought formations" - but what It never occurred to me even for a moment that the informational basis of reality - that saw in 3-74 - starts out in my own brain I but this would explain why 3-74 resembled given that the phenomenal world, Ubik." i built in terms of time, space + causation is t but formed in + by the percipient's brain when I saw the info + thought I had pene trated to true reality. But (I noted) it did resemble a giant brain + I wondered of I were projecting my own brain onto reality 9354 the dream says this is precisely the case. Maybe there is (somewhere) an objective reality, but I didn't experience it, or was it perhaps the surd? that which perturbed the reality field. Then I've had it backward; I thought the reality field was ob jectively real + I had perturbed it; but maybe the field (reality) is a construct in my own brain but perturbed from without So the "rustle + glitter in the weeds of the alley" is my only genuine contact with the "wholly other + is known only indirectly, only insofar as it perturbs my construct This is certainly something I never would have thought of except for the dream. Then it was not world that Valis invaded but me in the sense of my world as construct: 1D10s not normally kosmos. This means that we are impinged on by objective reality - or not anyhow at a level of which we are conscious. This is so radical an epistemology that even I am startled. Yet, upon inspection, it is - however radical reasonable. My discovery of Gotaroporic is I sensed last night) circular reasoning; it is as C vast tautology - exactly as the dream says a all turns out that philosophically I agree with it self. my Then our karma is self-generated (not by it we are our own accusers. The by us). but set-ground pimate info was my own brain; + yet This is a great discovery! throughts world construct - brain (info in space + time; i.e. (substantial the brain thinks (generates) the thoughts which then in turn become or generate world: they are the info basis of world t n 3549 world "decompose" into - or get rolled back to in 3-74. Hence in "Valis" I not only say that the universe is [actually] info, but this info is thoughts of a brain expressed as the mutual arrangement + rearrangement of objects; hence I posited: world to info to thoughts to brain thinking the thoughts - but now I must add that this brain is my own brain - the part lying somehow outside of consciousness. moreover, [in the dream] the Girl (i.e. I) recog‐ nized this info as her own prior thoughts; she remembered them, + the act of remembering anamnesis) was precisely what 2-74 consisted i must have recognized something (the of. I Golden Fish sign?) as my own prior thought; put another way, I remembere world (or "world") as my own prior thought-formations. World was familiar; I recognized it. This fits "Ubik" via "Frozen Journey" - which was, after all, written on the basis of Lem's analysis of "Ubik." Then a memory-block is in place in our mind + must be. otherwise we would know the truth (about world + hence our condition); but is this not precisely the premise, really, of much of my co-volume meta novel? but the system is intricate memory does not simply recirculate as world. It is not truly memory (of past experiences once lived), thoughts acting as instructions in it is the sense of digital info fed to an LP groove is a "memory" is not the word; former thoughts hat The key term. There is no implication once lived these events before; the implication is, rather, that I am cosmocrator + program (no: did formerly program) this world for myself: I formerly constructed it as its K3548 creator deliberately. No other agency is involved am (therefore) I but my brain + my thoughts. not a human being but a mentational i entity - possibly artificial in nature setting up a program of thought- info qua instructions to be used for the purpose of (1) generating a world + then (2) feeding that world to myself. Why? Well, remember the sensory deprivation dream with the 15 minite taped reminder-voice. Perhaps we (it is a "we" not an "I" as in "Maze"; this is a group effort! A polyencephalic fusion!) had to deal with the threat of sensory deprivation, + our solution was to program a world to + for ourselves. Well, then; this explains what call "coaxiality" or "common essence"! I There is an atemporal aspatial matrix out There; this explains how USA 1974 + Acts could syntonically be unified - this would, then, be a "technological foul-up" such as Lem theorizes would be your only clue as to the true state of affairs. Valis, then, is the true brain-mind of which we humans are - well, epiphenomenal Foct, I guess; it is the vast binary info processing, world-generating system lying (1) in us + (2) behind world (atman-Brahman; it has a dual existence, since it both underlies world as unitary info-processor + is in us as the Kantian structuring mechanism that supplies time, space + causation). A complex system is involved: the true macro-brain - or brains! that generate the thoughts; the construct or transducer that converts these thoughts into is simultaneously) both in us + world - this external to us (exactly as I experienced (3546 Valis: in me + outside me - this is a unified system (observer participant: "a vast deranged brain that both makes + perceives reality!) + then we recipients/percipients who are whittled-down - i.e. occluded + forgetful - micro-foci of quasi-consciousnesss far short of the "anokhi." of the original brain brains that think/thought the pro‐ gramming thoughts for the purpose of gene‐ rating the basis for world but in "Valis" I reasoned (based on what I experienced in 2-3-74) all the way back from world to info to thoughts to brain; I just didn't see the loop effect: we as percipients are subportions of the cosmogenic",
  "raw_text_char_count` — field absent from regenerated output | `segments/SEG_EXEG_1981-04-16_Pat_69.json` |
| 1 | `segments:evidence_excerpts[].matched_text` — field absent from regenerated output | `segments/SEG_EXEG_1981-04-16_Pat_77.json` |
| 1 | `segments:document_referenced` — field absent from regenerated output | `segments/SEG_EXEG_1981-04-16_Pat_85.json` |
| 1 | `timeline:` — array shrinks 55 -> 32 | `timeline/index.json` |
| 1 | `timeline:` — array shrinks 5 -> 3 | `timeline/years/1954.json` |
| 1 | `timeline:` — array shrinks 11 -> 8 | `timeline/years/1964.json` |
| 1 | `timeline:` — array shrinks 19 -> 17 | `timeline/years/1967.json` |
| 1 | `timeline:` — array shrinks 6 -> 5 | `timeline/years/1969.json` |
| 1 | `timeline:[].page_summary` — text shrinks 2071 -> 578 | `timeline/years/1969.json` |
| 1 | `timeline:` — array shrinks 14 -> 11 | `timeline/years/1970.json` |
| 1 | `timeline:[].summary` — text shrinks 199 -> 72 | `timeline/years/1970.json` |
| 1 | `timeline:` — array shrinks 10 -> 4 | `timeline/years/1971.json` |
| 1 | `timeline:` — array shrinks 12 -> 5 | `timeline/years/1972.json` |
| 1 | `timeline:[].summary` — text shrinks 192 -> 65 | `timeline/years/1972.json` |
| 1 | `timeline:` — array shrinks 18 -> 14 | `timeline/years/1973.json` |
| 1 | `timeline:` — array shrinks 101 -> 82 | `timeline/years/1974.json` |
| 1 | `timeline:` — array shrinks 166 -> 154 | `timeline/years/1975.json` |
| 1 | `timeline:[].summary` — text shrinks 284 -> 64 | `timeline/years/1975.json` |
| 1 | `timeline:[].summary` — text shrinks 150 -> 70 | `timeline/years/1975.json` |
| 1 | `timeline:[].summary` — text shrinks 246 -> 37 | `timeline/years/1975.json` |
| 1 | `timeline:[].summary` — text shrinks 166 -> 53 | `timeline/years/1975.json` |
| 1 | `timeline:[].summary` — text shrinks 216 -> 70 | `timeline/years/1975.json` |
| 1 | `timeline:[].summary` — text shrinks 154 -> 55 | `timeline/years/1975.json` |
| 1 | `timeline:[].summary` — text shrinks 212 -> 60 | `timeline/years/1975.json` |
| 1 | `timeline:[].summary` — text shrinks 181 -> 64 | `timeline/years/1975.json` |
| 1 | `timeline:` — array shrinks 573 -> 565 | `timeline/years/1976.json` |
| 1 | `timeline:[].summary` — text shrinks 198 -> 71 | `timeline/years/1976.json` |
| 1 | `timeline:[].summary` — text shrinks 235 -> 35 | `timeline/years/1976.json` |
| 1 | `timeline:[].summary` — text shrinks 123 -> 52 | `timeline/years/1976.json` |
| 1 | `timeline:` — array shrinks 18 -> 6 | `timeline/years/1977.json` |
| 1 | `timeline:` — array shrinks 415 -> 411 | `timeline/years/1978.json` |
| 1 | `timeline:[].summary` — text shrinks 201 -> 72 | `timeline/years/1978.json` |
| 1 | `timeline:[].recurring_concepts[]` — text shrinks 121 -> 55 | `timeline/years/1978.json` |
| 1 | `timeline:` — array shrinks 8 -> 4 | `timeline/years/1979.json` |
| 1 | `timeline:` — array shrinks 393 -> 381 | `timeline/years/1981.json` |
| 1 | `timeline:[].recurring_concepts` — array shrinks 3 -> 1 | `timeline/years/1981.json` |

## Files no exporter produces

- `archive/docs/davis-hymn-of-philip-k-dick-ase-talk.json`
- `archive/docs/davis-spin-1989-pkd-sonic-youth.json`
- `archive/docs/gill-2006-pkd-paranoia-thesis.json`
- `archive/docs/jackson-1999-the-world-philip-k-dick-made-dissertation.json`
- `archive/docs/music-in-pkd-spreadsheet.json`
- `archive/docs/rouzleweave-issue-2-may-2002.json`
- `archive/docs/simpson-aesthetics-of-garbage-martian-time-slip.json`
- `archive/docs/taylor-1975-pkd-and-the-umbrella-of-light.json`
- `archive/docs/thomas-coin-operated-doors-and-god.json`
- `biography/curated.json`
- `connections.json`
- `essays/index.json`
- `exegesis/entries.json`
- `exegesis/works/a-maze-of-death.json`
- `exegesis/works/a-scanner-darkly.json`
- `exegesis/works/deus-irae.json`
- `exegesis/works/do-androids-dream-of-electric-sheep.json`
- `exegesis/works/flow-my-tears-the-policeman-said.json`
- `exegesis/works/galactic-pot-healer.json`
- `exegesis/works/index.json`
- `exegesis/works/martian-time-slip.json`
- `exegesis/works/radio-free-albemuth.json`
- `exegesis/works/the-cosmic-puppets.json`
- `exegesis/works/the-divine-invasion.json`
- `exegesis/works/the-three-stigmata-of-palmer-eldritch.json`
- `exegesis/works/time-out-of-joint.json`
- `exegesis/works/ubik.json`
- `exegesis/works/valis.json`
- `letters/entries.json`
- `people/pkd-knew.json`
- `pkd-on-pkd/a-maze-of-death.json`
- `pkd-on-pkd/clans-of-the-alphane-moon.json`
- `pkd-on-pkd/confessions-of-a-crap-artist.json`
- `pkd-on-pkd/counter-clock-world.json`
- `pkd-on-pkd/deus-irae.json`
- `pkd-on-pkd/do-androids-dream-of-electric-sheep.json`
- `pkd-on-pkd/dr-bloodmoney-or-how-we-got-along-after-the-bomb.json`
- `pkd-on-pkd/eye-in-the-sky.json`
- `pkd-on-pkd/five-great-novels.json`
- `pkd-on-pkd/five-novels-of-the-1960s-and-70s.json`
- `pkd-on-pkd/gather-yourselves-together.json`
- `pkd-on-pkd/index.json`
- `pkd-on-pkd/lies-inc.json`
- `pkd-on-pkd/mary-and-the-giant.json`
- `pkd-on-pkd/nick-and-the-glimmung.json`
- `pkd-on-pkd/now-wait-for-last-year.json`
- `pkd-on-pkd/our-friends-from-frolix-8.json`
- `pkd-on-pkd/radio-free-albemuth.json`
- `pkd-on-pkd/solar-lottery.json`
- `pkd-on-pkd/the-cosmic-puppets.json`
- `pkd-on-pkd/the-crack-in-space.json`
- `pkd-on-pkd/the-game-players-of-titan.json`
- `pkd-on-pkd/the-ganymede-takeover.json`
- `pkd-on-pkd/the-man-in-the-high-castle.json`
- `pkd-on-pkd/the-man-who-japed.json`
- `pkd-on-pkd/the-penultimate-truth.json`
- `pkd-on-pkd/the-simulacra.json`
- `pkd-on-pkd/the-unteleported-man.json`
- `pkd-on-pkd/the-valis-trilogy.json`
- `pkd-on-pkd/the-zap-gun.json`
- `pkd-on-pkd/time-out-of-joint.json`
- `pkd-on-pkd/ubik.json`
- `pkd-on-pkd/voices-from-the-street.json`
- `scholars.json`
- `studies/religion/index.json`
- `studies/religion/topics/religion-in-pkds-fiction.json`
- `themes/index.json`
- `theophanies/2-3-74-cluster.json`
- `theophanies/abulafia-possession-1976.json`
- `theophanies/ai-voice-1974.json`
- `theophanies/black-iron-prison-1974.json`
- `theophanies/christopher-diagnosis-1974.json`
- `theophanies/fish-sign-2-20-74.json`
- `theophanies/index.json`
- `theophanies/koine-greek-1974.json`
- `theophanies/metz-1977.json`
- `theophanies/numbers-letters-gematria-1975.json`
- `theophanies/pink-beam-1974.json`
- `theophanies/pre-break-in-foreknowledge-1971.json`
- `theophanies/sky-face-vision-1963.json`
- `theophanies/twin-sister-jane-1980.json`
- `theophanies/vancouver-despair-1972.json`
- `theophanies/zebra-mimicry-1974.json`
- `timeline/years/1928.json`
- `timeline/years/1929.json`
- `timeline/years/1930.json`
- `timeline/years/1931.json`
- `timeline/years/1932.json`
- `timeline/years/1933.json`
- `timeline/years/1934.json`
- `timeline/years/1935.json`
- `timeline/years/1936.json`
- `timeline/years/1937.json`
- `timeline/years/1938.json`
- `timeline/years/1939.json`
- `timeline/years/1941.json`
- `timeline/years/1943.json`
- `timeline/years/1945.json`
- `timeline/years/1946.json`
- `timeline/years/1947.json`
- `timeline/years/1948.json`
- `timeline/years/1949.json`
- `timeline/years/1950.json`
- `timeline/years/1951.json`
- `timeline/years/1960.json`
- `timeline/years/1961.json`
- `works/41706725-dick-philip-k-in-pursuit-of-valis.json`
- `works/45007880-philip-k-dick-how-to-build-a-universe.json`
- `works/a-dark-haired-girl-pkd-letters-from-the-heart-the-spleen-and-the-funnybone.json`
- `works/a-game-of-unchance.json`
- `works/a-little-something-for-us-tempunauts.json`
- `works/a-maze-of-death.json`
- `works/a-present-for-pat.json`
- `works/a-surface-raid.json`
- `works/a-terran-odyssey.json`
- `works/a-world-of-talent.json`
- `works/ace-double-d-193-dick-philip-k-the-man-who-japed-1956-ace-libgen-li.json`
- `works/adjustment-team.json`
- `works/adobe-scan-apr-26-2025.json`
- `works/aka-lies-inc-philip-k-dick-the-unteleported-man-1983-berkley-libgen-li.json`
- `works/autofac.json`
- `works/beyond-lies-the-wub.json`
- `works/beyond-the-door.json`
- `works/book-pkd-ubik.json`
- `works/breakfast-at-twilight.json`
- `works/cadbury-the-beaver-who-lacked.json`
- `works/captive-market.json`
- `works/chains-of-air-web-of-aether.json`
- `works/clans-of-the-alphane-moon.json`
- `works/claudia-bush-letters.json`
- `works/colony.json`
- `works/confessions-of-a-crap-artist.json`
- `works/cosmogony-and-cosmology.json`
- `works/counter-clock-world.json`
- `works/deus-irae.json`
- `works/dick-letter-on-writing.json`
- `works/dick-philip-k-clans-of-the-alphane-moon-1964-ace-books-libgen-li.json`
- `works/dick-philip-k-confessions-of-a-crap-artist-1975-ace-books-libgen-li.json`
- `works/dick-philip-k-counter-clock-world-2012-mariner-books-houghton-mifflin-harcourt-l.json`
- `works/dick-philip-k-dr-bloodmoney-or-how-we-got-along-after-the-bomb-1977-ace-books-li.json`
- `works/dick-philip-k-five-novels-of-the-1960s-and-70s-2008-library-of-america-libgen-li.json`
- `works/dick-philip-k-gather-yourselves-together-houghton-mifflin-harcourt-libgen-li.json`
- `works/dick-philip-k-mary-and-the-giant-1987-ace-books-libgen-li.json`
- `works/dick-philip-k-now-wait-for-last-year-libgen-li.json`
- `works/dick-philip-k-our-friends-from-frolix-8-2013-mariner-books-houghton-mifflin-harc.json`
- `works/dick-philip-k-solar-lottery-2012-houghton-mifflin-harcourt-mariner-books-libgen-.json`
- `works/dick-philip-k-the-cosmic-puppets-houghton-mifflin-harcourt-libgen-li.json`
- `works/dick-philip-k-the-game-players-of-titan-1963-2001-vintage-libgen-li.json`
- `works/dick-philip-k-the-man-in-the-high-castle-1962-2016-vintage-books-boston-mariner-.json`
- `works/dick-philip-k-the-preserving-machine-1969-ace-books-libgen-li.json`
- `works/dick-philip-k-the-valis-trilogy-2011-houghton-mifflin-harcourt-libgen-li.json`
- `works/dick-philip-k-ubik-2012-houghton-mifflin-harcourt-libgen-li.json`
- `works/dick-philip-k-ubik-the-screenplay-2012-houghton-mifflin-harcourt-libgen-li.json`
- `works/dick-philip-k-voices-from-the-street-2007-ace-books-libgen-li.json`
- `works/dick-philip-kindred-a-maze-of-death-libgen-li.json`
- `works/dick-philip-kindred-the-penultimate-truth-libgen-li.json`
- `works/dick-philip-kindred-the-simulacra-libgen-li.json`
- `works/dick-philip-kindred-the-zap-gun-libgen-li.json`
- `works/dick-philip-kindred-time-out-of-joint-libgen-li.json`
- `works/dick-philip-kindred-zelazny-roger-deus-irae-libgen-li.json`
- `works/divine-invasion.json`
- `works/do-androids-dream-of-electric-sheep.json`
- `works/do-androids-dream.json`
- `works/dr-bloodmoney-or-how-we-got-along-after-the-bomb.json`
- `works/electric-dreams.json`
- `works/exhibit-piece.json`
- `works/expendable.json`
- `works/explorers-we.json`
- `works/eye-in-the-sky-philip-k-dick-houghton-mifflin-harcourt-114629893-libgen-li.json`
- `works/eye-in-the-sky.json`
- `works/fair-game.json`
- `works/faith-of-our-fathers.json`
- `works/five-great-novels.json`
- `works/five-novels-of-the-1960s-and-70s.json`
- `works/foster-you-re-dead.json`
- `works/gather-yourselves-together.json`
- `works/hmh-philip-k-dick-radio-free-albemuth-2020-hmh-books-houghton-mifflin-harcourt-l.json`
- `works/holy-quarrel.json`
- `works/how-to-build-a-universe-that-doesn-t-fall-apart-two-days-later.json`
- `works/human-is.json`
- `works/i-hope-i-shall-arrive-soon.json`
- `works/if-there-were-no-benny-cemoli.json`
- `works/imposter.json`
- `works/in-pursuit-of-valis-selections-from-the-exegesis.json`
- `works/index.json`
- `works/james-p-crow.json`
- `works/jon-s-world.json`
- `works/letter-on-star-wars-1977-10-02.json`
- `works/letter-on-star-wars.json`
- `works/letter-to-julian-jaynes-1977-03-16.json`
- `works/letter-to-julian-jaynes.json`
- `works/lies-inc.json`
- `works/man-in-high-castle.json`
- `works/martians-come-in-clouds.json`
- `works/mary-and-the-giant.json`
- `works/maze-of-death-theology.json`
- `works/meddler.json`
- `works/misadjustment.json`
- `works/mr-spaceship.json`
- `works/nanny.json`
