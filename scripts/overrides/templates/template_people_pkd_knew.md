# Template - People PKD Knew

For: editors, spouses and partners, family, friends, fellow SF authors, correspondents, co-workers, bosses, publishers, agents, doctors, fans, scholars who personally interacted with PKD, people central to the Exegesis or unpublished writings, people who inspired or were transformed into characters, and anyone whose report becomes evidence in biographies, letters, interviews, fan publications, or scholarship.

Lane: usually **E** when based on direct primary report, **D** when synthesized from biographies, **C** when the person appears only as a scholarly actor. A single person entry may cite multiple lanes.

## Writing standard

Write each entry as a compact academic encyclopedia article. The prose should identify the person, explain how they enter the PKD record, and then synthesize the relevant evidence without sounding like a note dump. Prefer names, dates, document titles, and specific actions over general labels like "important" or "close." If a claim comes from a memoir, interview, letter, or biographical reconstruction, say so.

## Short card

Every person must have a compact card for tabs, lists, and relational browsing.

Required fields:
- `person_id` - stable kebab-case slug
- `name` - canonical display name
- `relationship_to_pkd` - short phrase: spouse, editor, correspondent, fellow SF author, friend, fan-scholar, scholar, doctor, employer
- `relationship_categories` - controlled array for sorting and filters
- `card_summary` - 35-80 words explaining the association with PKD
- `first_year` and `last_year` - where known, for chronological browsing
- `evidence_counts` - counts by source type: biography events, letters, archive documents, scholar profiles, names index
- `review_state` - unreviewed, machine-drafted, human-revised, publication-ready

## Full page

Required sections:

1. **Association with PKD** - how they knew him, how they enter the record, or why they matter in the Exegesis / unpublished-writing / character-inspiration trail.
2. **What they reported or did** - opinions about PKD, reports about his behavior, editorial/community work, correspondence, collaborations, disputes, influence, or character inspiration.
3. **PKD's view of them** - only when sourced; distinguish PKD's self-report from independent evidence.
4. **Documents and events** - linked biography events, letters, interviews, archive documents, scholarship, and fictional appearances.
5. **Reliability and contradictions** - disagreements among sources, memory problems, later mythmaking, or disputed claims.
6. **Research use** - what question a reader would consult this person to answer.
7. **Source mix** - if the evidence comes from more than one lane, say which lane supports which part of the entry.

## Relationship categories

Use these values where applicable: `family`, `spouse_or_partner`, `friend`, `correspondent`, `editor`, `publisher`, `agent`, `fellow_sf_author`, `workplace`, `doctor_or_therapist`, `fan`, `fan_scholar`, `scholar`, `interviewer_or_media`, `archivist_or_curator`, `mentioned_in_document`, `named_person`, `exegesis_figure`, `character_inspiration`, `university_connection`, `conference_connection`.

## Lint checklist

- [ ] Has a short card and a full page summary.
- [ ] Names the evidence lanes used.
- [ ] Links to at least one event, document, name entry, scholar profile, or letter when available.
- [ ] Separates direct acquaintance from later scholarly mention.
- [ ] Records opinions about PKD only when attributed to a source.
- [ ] Flags contradictions instead of smoothing them away.
- [ ] Reads like an encyclopedia entry rather than a raw relationship list.
