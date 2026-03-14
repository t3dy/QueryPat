# PDF Search Findings

## Coverage
- 181 of 228 archive documents have extracted text (79%)
- 21 failed extraction (scanned PDFs needing OCR)
- 22 pending extraction
- Text is truncated to 6,000 chars per document (~2-3 pages)

## Term Evidence
Priority term search across 181 documents:
- VALIS: 25 docs, 63 mentions
- Ubik: 18 docs, 31 mentions
- Gnosticism: 8 docs, 12 mentions
- Palmer Eldritch: 8 docs, 9 mentions
- Zebra: 5 docs, 14 mentions
- Horselover Fat: 4 docs, 6 mentions
- Logos: 3 docs, 7 mentions
- Demiurge: 2 docs, 3 mentions
- Living Information: 2 docs, 3 mentions
- The Empire Never Ended: 2 docs, 3 mentions
- Many PKD-specific terms (Sophia, Plotinus, Eckhart, Boehme, etc.) have 0 hits — they don't appear in the first ~3 pages of secondary literature

## Candidate Terms Not Yet in Dictionary
117 candidates appearing in 3+ documents, most notable:
- **Scholars**: Paul Williams (14 docs), Erik Davis (6), Norman Spinrad (6), Gregg Rickman (5), Malcolm Edwards (4), Bruce Gillespie (3), Harlan Ellison (3), Le Guin (6)
- **Works**: High Castle (16), Scanner Darkly (12), Do Androids Dream (11), Electric Sheep (11), Blade Runner (7), Solar Lottery (6), Martian Time (6), The Divine Invasion (6), In Milton Lumky Territory (4)
- **Places**: Point Reyes Station (14), San Rafael (8), Bay Area (3), Fort Morgan (4)
- **Organizations**: Science Fiction Studies (10), Dick Society (6), Hugo Award (6), Gnosis Magazine (3)

## Event Discovery
Biography PDFs yielded no usable events — the 6,000-char truncation means only front matter (title pages, copyright, TOC) is captured, not the narrative content where biographical events would appear.

## Recommendations
1. Increase extraction limit to 50,000+ chars for priority biographies
2. Add scholar names from candidate list to the Names database
3. Add PKD work titles as dictionary terms or a separate Works index
4. Re-run event discovery after expanding extraction coverage
