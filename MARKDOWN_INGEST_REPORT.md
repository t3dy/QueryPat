# Markdown Ingestion Report

Summary of `scripts/markdown/convert_all.py` against `documents` + `assets`.

## Status counts

| Status | Documents |
|---|---:|
| pending | 97 |
| complete | 97 |
| skipped_source_missing | 21 |
| skipped_ocr_required | 9 |
| **TOTAL** | **224** |

## Extraction methods used

| Method | Documents |
|---|---:|
| pymupdf4llm | 97 |

## Coverage by category

| Category | Total | Complete | OCR-needed | Failed |
|---|---:|---:|---:|---:|
| scholarship | 64 | 35 | 0 | 0 |
| newspaper | 45 | 14 | 3 | 0 |
| novels | 35 | 13 | 1 | 0 |
| fan_publications | 19 | 6 | 0 | 0 |
| primary | 16 | 8 | 1 | 0 |
| short_stories | 15 | 8 | 0 | 0 |
| other | 12 | 4 | 2 | 0 |
| letters | 10 | 3 | 1 | 0 |
| biographies | 7 | 5 | 1 | 0 |
| interviews | 5 | 1 | 0 | 0 |

## Total markdown characters

- **37,355,334** characters across 97 complete documents
- Average: 385,106 chars/doc

## Documents skipped (OCR required)

These need a scanned-PDF OCR pass (out of scope for this ingest):

- `DOC_ARCH_1974_ROLLING_STONE`
- `DOC_ARCH_DICK_LETTER_ON_WRITING`
- `DOC_ARCH_LA_WEEKLY_1990_11_22_6`
- `DOC_ARCH_LEVINAS_NAME_OF_DOG`
- `DOC_ARCH_MR34443`
- `DOC_ARCH_OAKLAND_TRIBUNE_1955_01_10_19`
- `DOC_ARCH_OCEANOFPDF_COM_A_LIFE_OF_PHILIP_K_DICK_A`
- `DOC_ARCH_OWL_IN_DAYLIGHT`
- `DOC_ARCH_PHILIPK_DICKREVIEWSHERMANWOUKSTHECAINEMU`

## Documents skipped (source file missing)

Asset paths in the DB pointed to files not present at the source root.

- `DOC_ARCH_ACE_DOUBLE_D_193_DICK_PHILIP_K_THE_MAN_W`
- `DOC_ARCH_DICK_PHILIP_K_CLANS_OF_THE_ALPHANE_MOON_`
- `DOC_ARCH_DICK_PHILIP_K_CONFESSIONS_OF_A_CRAP_ARTI`
- `DOC_ARCH_DICK_PHILIP_K_COUNTER_CLOCK_WORLD_2012_M`
- `DOC_ARCH_DICK_PHILIP_K_DR_BLOODMONEY_OR_HOW_WE_GO`
- `DOC_ARCH_DICK_PHILIP_K_FIVE_NOVELS_OF_THE_1960S_A`
- `DOC_ARCH_DICK_PHILIP_K_GATHER_YOURSELVES_TOGETHER`
- `DOC_ARCH_DICK_PHILIP_K_MARY_AND_THE_GIANT_1987_AC`
- `DOC_ARCH_DICK_PHILIP_K_OUR_FRIENDS_FROM_FROLIX_8_`
- `DOC_ARCH_DICK_PHILIP_K_SOLAR_LOTTERY_2012_HOUGHTO`
- `DOC_ARCH_DICK_PHILIP_K_THE_COSMIC_PUPPETS_HOUGHTO`
- `DOC_ARCH_DICK_PHILIP_K_THE_MAN_IN_THE_HIGH_CASTLE`
- `DOC_ARCH_DICK_PHILIP_K_THE_PRESERVING_MACHINE_196`
- `DOC_ARCH_DICK_PHILIP_K_THE_VALIS_TRILOGY_2011_HOU`
- `DOC_ARCH_DICK_PHILIP_K_UBIK_2012_HOUGHTON_MIFFLIN`

