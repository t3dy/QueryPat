# Digital Humanities Resource Goals

This project should be treated as a relationally browsable digital humanities resource for Philip K. Dick: biography, letters, fiction, Exegesis materials, criticism, documents, places, people, concepts, and works should be cross-linked so a reader can follow evidence-rich scholarly trails without losing the larger map.

Future LLMs working in this repository should read this file together with `SCHOLARLYVALUES.md` before making data, writing, extraction, or interface changes. This file is meant to preserve the project's product vision and scholarly habits inside the repo, since we cannot literally alter the assistant's system prompt from within the project.

## Core Resource Vision

The site should feel like a clever, slick, explorable research instrument, not a static exhibit. A user should be able to start with a letter, a biographical event, a work, a religious experience, a person, a place, a drug episode, a composition period, an editor, or a scholar, then follow linked evidence across the whole archive.

Every important entity should become a doorway:

- People: spouses, partners, family, friends, editors, agents, correspondents, interviewers, scholars, biographers, informants, physicians, religious contacts, fan/community figures, and later estate or reception figures.
- Works: stories, novels, essays, speeches, unpublished notes, Exegesis folders, letters, interviews, and secondary studies.
- Events: dated or date-range biographical events, composition periods, publication events, visionary/religious episodes, drug and mental health episodes, jobs, schools, residences, friendships, marriages, affairs, collaborations, and disputes.
- Documents: letters, published books, unpublished PDFs, archive scans, memoirs, reviews, interviews, finding aids, scholarly articles, and project-generated summaries.
- Concepts: Zebra, VALIS, 2-3-74, anamnesis, Gnosticism, split-brain theory, Julian Jaynes, amphetamine use, psychosis, the Black Iron Prison, I Ching, simulation, androids, and related terms.
- Places: Berkeley, Point Reyes, Santa Venetia, Fullerton, Orange County, Vancouver, Metz, and more granular residences, schools, workplaces, and hospitals where supported.

The user experience should reward scholarly rabbit holes. Hyperlinked text, backlink panels, related-document rails, faceted lists, chronology lanes, relationship graphs, and sortable tables are not extras; they are the shape of the project.

## People Section Goal

Create a dedicated `People` section distinct from the existing broader `Names` system. `Names` may include fictional characters, mythological terms, institutions, concepts, or noisy extracted entities. `People` should be curated and source-backed.

Each person page should include:

- A concise identification line.
- Relationship categories to PKD: family, spouse/partner, friend, correspondent, editor, agent, publisher, collaborator, scholar, biographer, informant, interviewer, religious contact, medical/legal/government contact, fan/community contact, intellectual influence, or reception figure.
- Date ranges for the relationship when known.
- A linked timeline of events involving that person.
- A correspondence table when letters exist.
- A documents tab listing letters, interviews, biographies, archive documents, criticism, and notes connected to the person.
- Works connected to the person: dedicated works, collaborations, edited works, reviewed works, or works whose composition/reception they affected.
- Places connected to the person.
- Evidence notes with source links and uncertainty labels.
- Backlinks showing where the person appears in biography entries, document summaries, studies, terms, theophany entries, and archive records.

People records should support aliases, name variants, married names, misspellings, and role changes over time. A person can have multiple roles, and the interface should let users filter and sort by those roles.

## Seed People List

This seed list is a starting target for a 50-100 person People index based on the biography, letters, timeline entries, Selected Letters correspondents, archive summaries, and known PKD scholarship. It deliberately mixes people who knew PKD personally with later biographers, scholars, editors, and informants who shape the evidentiary record. Each entry still needs source-backed person-page work before being treated as complete.

### Family, Spouses, Partners, and Household Network

1. Dorothy Kindred Dick - mother; central family figure and correspondent.
2. Edgar Dick - father; early biography and family context.
3. Jane Charlotte Dick - twin sister; biographical and symbolic center.
4. Jeanette Marlin - first wife.
5. Kleo Apostolides - second wife; Berkeley years and early writing period.
6. Anne Williams Rubinstein Dick - third wife; Point Reyes period and memoir witness.
7. Nancy Hackett - fourth wife; letters, domestic life, 1960s-1970s transition.
8. Tessa Busby / Tessa Dick - fifth wife; 2-3-74 period, later memoir witness.
9. Laura Archer Dick - daughter; frequent correspondent and late-life family context.
10. Isa Hackett - daughter; family witness and estate/reception context.
11. Christopher Dick - son; 2-3-74 medical/theophany cluster.
12. Dorothy Hudner - family and correspondence network.
13. Maren Hackett - family context.
14. Linda Levy - romantic/domestic context in the letters.
15. Doris Sauter - friend/caretaker and late-life witness.
16. Joan Simpson - correspondent and personal network.
17. Cynthia Goldstone - personal network and letters.
18. Sherry Gottlieb - personal network, bookstore and countercultural context.
19. Sonia White - personal correspondence and late-life context.
20. Kathy Demuelle - relationship and letters lead; verify spellings and dates.

### Agents, Editors, Publishers, and Professional Gatekeepers

21. Scott Meredith - literary agent and major correspondent.
22. Russell Galen - agent and heavy Selected Letters correspondent.
23. Jack Scovil - agent/editorial contact and frequent correspondent.
24. Lawrence Ashmead - editor/publishing contact.
25. Anthony Boucher - editor, critic, early SF mentor/gatekeeper.
26. J. Francis McComas - editor and early SF publication context.
27. Donald A. Wollheim - editor/publisher; Ace and SF paperback context.
28. Terry Carr - editor, anthologist, friend/correspondent.
29. Carol Carr - correspondent and SF community figure.
30. Judy-Lynn del Rey - editor and correspondent.
31. Sharon Jarvis - publishing/editorial correspondent.
32. Lurton Blassingame - literary agency context.
33. Ralph Vicinanza - agent and rights/reception context.
34. Malcolm Edwards - editor/publishing/reception context.
35. Peter Nicholls - editor, critic, encyclopedia/reception context.
36. Edward L. Ferman - editor and magazine publication context.
37. David G. Hartwell - editor, critic, and reception figure.
38. Paul Williams - literary executor/editor, Selected Letters and biography witness.
39. Pamela Jackson - Exegesis editor and later document mediator.
40. Jonathan Lethem - editor/reception figure for Library of America and canonization.

### SF Writers, Peers, Friends, and Collaborators

41. Roger Zelazny - SF author and frequent correspondent.
42. Ursula K. Le Guin - SF author and correspondent.
43. Robert A. Heinlein - SF author; letters and field context.
44. Harlan Ellison - SF author/editor and community figure.
45. John Brunner - SF author, critic, and New Worlds context.
46. Brian Aldiss - SF author and reception context.
47. Thomas M. Disch - SF author/critic and field context.
48. Theodore Sturgeon - SF author and field context.
49. Isaac Asimov - SF author and field/reception context.
50. Fritz Leiber - SF/fantasy author and field context.
51. James Blish - SF author/critic and field context.
52. Ray Nelson - friend and collaborator on `The Ganymede Takeover`.
53. K. W. Jeter - friend, younger writer, and biographical witness.
54. Tim Powers - friend, younger writer, and biographical witness.
55. Norman Spinrad - SF author, peer, and field context.
56. Art Spiegelman - correspondent and comics/literary reception context.
57. Michele Gross - correspondent with Art Spiegelman.
58. Bruce Gillespie - fan/editor/correspondent.
59. Jannick Storm - correspondent and international SF context.
60. Stanislaw Lem - writer/critic; reception, controversy, and intellectual context.
61. Franz Rottensteiner - Lem-related and European SF reception context.
62. A. E. van Vogt - SF predecessor/influence and field context.
63. Philip Jose Farmer - SF peer and field context.
64. Charles Platt - interviewer/critic and late-life SF context.

### Scholars, Critics, Biographers, Interviewers, and Informants

65. Claudia Bush - major Exegesis correspondent; corpus should have document summary.
66. Patricia Warrick - scholar and frequent correspondent.
67. Julian Jaynes - theorist and letter recipient; bicameral mind connection to PKD experience.
68. William Sarill - houseguest/conversation partner linked to `A Maze of Death` theology.
69. Eugene Warren - correspondent; `Star Wars` letter context.
70. Mark Hurst - correspondent and late letters context.
71. Carl Bennett - correspondent and letters network.
72. Sandra Miesel - critic/correspondent.
73. Uwe Anton - international critic/correspondent.
74. Patrice Duvic - critic/editor and French reception context.
75. Angus Taylor - interviewer/scholarship context.
76. Willis E. McNelly - critic/interviewer and SF studies context.
77. Darko Suvin - scholar and SF studies context.
78. Kim Stanley Robinson - scholar/novelist; critical work on PKD.
79. Lawrence Sutin - biographer and Exegesis/Divine Invasions context.
80. Gregg Rickman - interviewer, biographer, and archive/reception figure.
81. Kyle Arnold - biographer/scholar; `The Divine Madness of Philip K. Dick` is central for visionary, religious, and psychiatric interpretation.
82. Erik Davis - scholar/reception figure for PKD and religious/countercultural context.
83. Gabriel McKee - scholar of PKD religion and theology.
84. Andrew M. Butler - scholar and reception context.
85. Christopher Palmer - scholar and criticism context.
86. Umberto Rossi - scholar and criticism context.

### Religious, Medical, Legal, Government, and Intellectual Context Figures

87. Bishop James Pike - religious figure and afterlife/theological context.
88. Benjamin Creme - religious/occult contact context.
89. Ira Einhorn - countercultural contact and letters context.
90. Inspector Shine - police contact in the break-in/1971-1972 cluster.
91. George Scruggs - FBI/government correspondence context.
92. Frank Church - government/intelligence investigation context.
93. William Colby - CIA/intelligence context in PKD's letters and suspicions.
94. Timothy Leary - counterculture/drug/intellectual context.
95. Daniel Berrigan - religious/political context.
96. Robert Ornstein - psychology/intellectual context.
97. Joseph Bogen - split-brain research context.
98. John Archibald Wheeler - physics/multiple-universes lead connected to Sarill/Maze context; mark as intellectual context unless direct contact is found.
99. John Allegro - religious/history-of-Christianity/drug-theory context to verify.
100. Ray Bradbury - SF field and reception context; verify direct contact and document links.

## People Data Model Requirements

People data should not be a loose tag cloud. It should be a structured layer that can power browsing, filtering, and evidence trails.

Minimum fields:

- `id`
- `display_name`
- `sort_name`
- `aliases`
- `birth_year`, `death_year` when known
- `roles`
- `relationship_to_pkd`
- `relationship_start`, `relationship_end`, and uncertainty
- `summary`
- `evidence_status`: seed, partial, source-backed, reviewed
- `source_links`: document ids, letter ids, biography event ids, archive ids, study ids
- `related_people`
- `related_places`
- `related_works`
- `related_terms`
- `notes_on_uncertainty`

Relationship records should be first-class data, not buried in prose. A person-person edge should have:

- Source person and target person.
- Relationship type.
- Date range.
- Evidence links.
- Confidence or uncertainty.
- Note describing what the evidence actually shows.

## Frontend Goals

The People section should include:

- A people index with search, role filters, era filters, correspondence filters, and evidence-status filters.
- Sort options by name, number of letters, number of timeline events, role, and chronology.
- Person detail pages with tabs for Overview, Timeline, Letters, Documents, Works, Places, Relationships, and Backlinks.
- Inline linked names throughout biography, archive, document summaries, studies, and term pages.
- A relationship graph view that can be filtered by role and time period.
- "Start here" scholarly trails, such as PKD and editors, PKD and spouses, PKD and religious interpreters, PKD and the 1970s correspondents, PKD and younger California writers, PKD and SF peers, PKD and psychology/psychiatry.
- Related-item sidebars that explain why each recommendation appears.
- A citation/evidence panel for claims on person pages.

Interface tone should be dense, elegant, and research-forward. Avoid landing-page fluff. The primary screen should expose the resource itself: browsable lists, rich filters, timelines, graphs, documents, and search.

## Search and Extraction Method

Any future expansion of People, biography, and document summaries should use a reproducible search method:

1. Query structured data first: `letters`, `documents`, `biography`, `archive`, `names`, and exported JSON.
2. Search OCR text and extracted markdown with `rg`, recording query terms and file paths.
3. Use known correspondents and curated biography entities as seed terms, but verify against the document text.
4. For each person, capture direct evidence: letters to/from them, references in letters, timeline events, biography claims, interviews, and archive documents.
5. Mark uncertain leads explicitly rather than omitting them or making them sound settled.
6. Generate an output report for each major extraction pass, including queries used, source coverage, and unresolved leads.

High-priority extraction targets:

- Selected Letters to famous SF authors.
- Letter to Julian Jaynes.
- Letter on `Star Wars`.
- Claudia Bush Letters corpus.
- `The Maze of Death Theology` / `Notes on the Tench Novel`.
- Kyle Arnold, `The Divine Madness of Philip K. Dick`, especially visionary, religious, drug, and psychiatric episodes.
- Composition periods for all stories and novels.
- Romantic, marital, and household chronology.
- Schools, jobs, workplaces, residences, and adolescent context.
- Religious, drug, mental health, and visionary experiences, with separate primary and interpretive evidence lanes.

## Document Summary Library Goals

Important documents should be represented as documents even when they are letters, unpublished notes, PDFs, or corpora rather than conventional books.

Required document-summary targets include:

- Letter to Julian Jaynes.
- Letter on `Star Wars`.
- Claudia Bush Letters corpus.
- `The Maze of Death Theology` / `Notes on the Tench Novel`.
- Selected Letters volumes.
- Kyle Arnold, `The Divine Madness of Philip K. Dick`.
- Major biographies, memoirs, interviews, and archive finding aids.

Document pages should link to people, terms, timeline events, related works, places, and source assets. They should include compact summaries, scholarly significance, extraction status, and source limitations.

## Biography and Timeline Goals

The biography should be more than famous milestones. It should include:

- Working periods for every story and novel when evidence supports them.
- Submission, rejection, acceptance, publication, revision, and adaptation events.
- Letters that illuminate composition, religious interpretation, drug use, money, relationships, publishing, and mental states.
- Dating, marriage, separation, divorce, domestic, and household periods.
- Places PKD lived, studied, worked, visited, or wrote.
- Adolescence: schools, jobs, record-store/radio/music contexts, early publications, health, and family life.
- Religious and visionary episodes with primary-source testimony and later interpretive frames.
- Drug experiences and prescriptions, with careful distinction between PKD's claims, witnesses' claims, biographical interpretations, and medical speculation.
- Contradictions and competing interpretations as part of the record.

Every timeline entry should ideally link to people, documents, works, places, and concepts.

## Future LLM Worker Rules

When working on this project:

- Read `SCHOLARLYVALUES.md` and this file before major extraction, interface, or data-design work.
- Prefer source-backed relational data over isolated prose.
- When adding a biography event, also consider whether it creates or updates people, places, works, terms, and document relationships.
- Do not flatten primary testimony, biography, memoir, criticism, and speculation into the same evidentiary status.
- Quote sparingly and legally; use short quotations only where wording matters, and paraphrase the rest.
- Preserve uncertainty. Add fields or notes for contested dates, ambiguous identities, OCR problems, and unverified leads.
- Build for browsing and re-search: every major claim should help a reader find the next relevant document.
- Leave extraction reports and methods so later work can audit and extend the pass.

The desired end state is a digital humanities instrument that lets readers ask: Who knew PKD? What did they know? What documents say so? What works or experiences were connected? What changed over time? Where are the contradictions? Where should the next archival question go?
