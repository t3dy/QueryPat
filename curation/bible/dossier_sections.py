"""
Editorial prose for the Bible study, and the mention cards it cites.

This module is the thing to edit. `scripts/studies/build_bible_study.py` reads
it, resolves every card against `raw-findings.json`, refuses to build if a
{{CARD-ID}} marker or a long quotation does not resolve against the corpus, and
writes the site JSON.

Each card names the sweep finding it is cut from by three things, none of
which is a line number:

    source   the corpus record id (a segment, a chapter, a letter, a document)
    field    which field of that record the sweep scanned
    anchor   a verbatim phrase inside the 420-character window around the hit

The builder requires the anchor to match exactly one finding. `pith` is the
sentence the passage turns on, copied verbatim from that window. `context` is
written by hand, and says what the passage does in Dick's argument.

Registers, as in curation/gnosticism and docs/RESEARCH_WORKLOG.md:
    A  what PKD says himself                 (Exegesis, trilogy text, letters)
    B  what primary-source evidence shows    (archive facts about the record)
    C  what scholars argue                   (secondary literature)
    D  what portal editors infer             (summaries, analysis, this prose)
"""

STUDY_ID = 'bible'
STUDY_LABEL = 'The Bible in PKD'
STUDY_DESCRIPTION = (
    "Philip K. Dick's engagement with the Bible across the Exegesis, the letters, the "
    "interviews, the VALIS trilogy and the short fiction: the books he quoted, the "
    "translations and glosses he used, the readings he made of them, and the claim "
    "that developed across 1975–81 that the Bible is not a record of the past but a "
    "living text describing, and in some sense being, the present world."
)

STUDY_SECTIONS = [
    {
        'title': 'What this study claims',
        'body': [
            "Philip K. Dick read the Bible from his schooldays, by his own account in 1981. "
            "In the 1970s he began to read it as a text about his own time, and then, in the "
            "notebooks known as the Exegesis, as a text that was the world he was living in. "
            "This study follows that change through the sources the repository holds, and "
            "keeps each source in its own register.",
            "The main evidence is the Exegesis: Dick's own words in 1,104 transcribed "
            "segments, of which 383 use Bible vocabulary at least once. The archive also holds "
            "the full text of his letters, of five interview transcripts, of the short stories, "
            "and of the VALIS chapters and other novels, so the same argument can be followed "
            "into correspondence, speech and fiction. Everything else is either editorial "
            "summary or secondary scholarship, and is labelled as such.",
        ],
    },
    {
        'title': 'What the archive does not yet show',
        'body': [
            "The 1974 Vertex interview is not held as text, so this study cannot say what Dick "
            "told that interviewer about scripture. The archive PDFs and the scholarship are "
            "searched as well, but only the letters, interviews, stories and novels have been "
            "read for cards.",
            "A sweep matches words. It will miss an allusion to scripture that does not name "
            "the book, and it will find a word that does not mean the Bible. An absence of a "
            "card is therefore not a finding about Dick.",
        ],
    },
]

GROUPS = [
    {'key': 'letters-1964', 'label': 'Letters, 1964',
     'blurb': 'Full text of the Selected Letters, from the volume held in the database.'},
    {'key': 'letters-1972', 'label': 'Letters, 1972',
     'blurb': 'The 1972 letter is quoted from the excerpt file held in the repository; the full '
              'letter text is searched in the database.'},
    {'key': 'letters-1973', 'label': 'Letters, 1973',
     'blurb': 'Full text. The rhymed-couplet project, under way.'},
    {'key': 'letters-1975', 'label': 'Letters, 1975',
     'blurb': 'Full text. Cypher, and the Parousia, in the correspondence of the year of the transcriptions.'},
    {'key': 'letters-1976-78', 'label': 'Letters, 1976–1978',
     'blurb': 'Full text. The months around the 15 September 1976 sitting on Acts in Tears, and a conversion.'},
    {'key': 'letters-1980-81', 'label': 'Letters, 1980–1981',
     'blurb': 'Full text. The Torah as Holy Wisdom, recombinant scripture, and the Bible as information.'},
    {'key': 'exeg-1975', 'label': 'The Exegesis — February and November 1975',
     'blurb': 'Transcriptions dated by batch. Each segment inherits its batch date.'},
    {'key': 'exeg-1976', 'label': 'The Exegesis — 15 September 1976',
     'blurb': 'The longest single sitting on the Bible, and the one in which the claim about Acts '
              'in Tears is first made.'},
    {'key': 'exeg-1978', 'label': 'The Exegesis — 10 October 1978 (folder)',
     'blurb': 'A batch date, not a sitting date. Entries inside it refer to late 1980.'},
    {'key': 'exeg-1981', 'label': 'The Exegesis — 16 April 1981',
     'blurb': 'The last sustained theory of the Bible in the transcriptions.'},
    {'key': 'fiction', 'label': 'The trilogy, as held here as full text',
     'blurb': 'VALIS and The Divine Invasion, chapters held as full text. Lane A: Dick’s own words '
              'in fiction.'},
    {'key': 'interviews', 'label': 'Interviews',
     'blurb': 'Five transcripts held as full text, including compiled and book-length collections. '
              'Lane A: Dick speaking. Most passages are undated in the record.'},
    {'key': 'stories', 'label': 'Short stories, as full text',
     'blurb': 'The collected and selected stories, held as full text. Lane A is fiction here: these '
              'are characters’ words, not Dick’s own claims.'},
    {'key': 'scholarship', 'label': 'Scholarship',
     'blurb': 'What scholars argue, not Dick. Lane C.'},
]

# ---------------------------------------------------------------------------
# Mention cards. Each card is one passage. Order here is not used; the builder
# numbers nothing, and the id is what the prose cites.
# ---------------------------------------------------------------------------
CARDS = [
    # ---- 1972 letter ----------------------------------------------------
    {
        'id': 'BIB-LET-72-01', 'source': 'LETTER_064', 'field': 'recipient',
        'anchor': 'I had set the Bible into rhymed couplets',
        'pith': 'I had set the Bible into rhymed couplets',
        'group': 'letters-1972', 'lane': 'A', 'register': 'A', 'relevance': 1,
        'citation': 'Letter to Roger Zelazny, 1 December 1972',
        'dated': '1972-12-01', 'dating_basis': 'Dated in the letter.',
        'concepts': ['Genesis', 'rhymed couplets', 'Luther'],
        'speaker': 'Philip K. Dick',
        'context': 'A dream reported to Roger Zelazny: Dick is given an award for having '
                   'set the Bible into rhymed couplets, and quotes his own version of '
                   'Genesis 1 as a sample. The joke is also a judgment: he prefers '
                   'Luther’s rendering of the line “And God saw that it good was.” The '
                   'letter is the first mention of the project. The 1964 letter to James '
                   'Blish is earlier.',
        'editorial_note': 'Quoted from the excerpt file, where the body sits in the recipient '
                          'field. The database holds the full letters; this card has not been '
                          're-anchored to them.',
    },
    # ---- February and November 1975 ------------------------------------
    {
        'id': 'BIB-EX-75-01', 'source': 'SEG_EXEG_1975-02-27_Claudia_03', 'field': 'raw_text',
        'anchor': 'The Bible is a book of the future',
        'pith': 'The Bible is a book of the future',
        'group': 'exeg-1975', 'lane': 'A', 'register': 'A', 'relevance': 1,
        'citation': 'Exegesis, batch of 27 February 1975 (Claudia)',
        'dated': '1975-02-27', 'dating_basis': 'Batch date; the entry is undated.',
        'concepts': ['prophecy', 'eschatology', 'New Testament', 'Old Testament'],
        'speaker': 'Philip K. Dick',
        'context': 'The first sustained claim about the Bible in the Exegesis. Dick '
                   'treats prophecy as a book of the future rather than a record of the '
                   'past, a claim he will return to with more force in 1976.',
    },
    {
        'id': 'BIB-EX-75-02', 'source': 'SEG_EXEG_U_Claudia_12', 'field': 'raw_text',
        'anchor': 'All the O.T. has in it is monotheism',
        'pith': 'All the O.T. has in it is monotheism, which they got from Iknaton.',
        'group': 'exeg-1975', 'lane': 'A', 'register': 'A', 'relevance': 1,
        'citation': 'Exegesis, batch of 27 February 1975 (Claudia)',
        'dated': '1975-02-27', 'dating_basis': 'Batch date; the entry is undated.',
        'concepts': ['Old Testament', 'Akhenaten', 'monotheism', 'Heraclitus'],
        'speaker': 'Philip K. Dick',
        'context': 'Dick sets the Old Testament against the Greeks and dismisses its '
                   'monotheism as borrowed from Akhenaten’s hymn. The debt to Akhenaten '
                   'returns in VALIS, where a psalm is traced to the same source.',
    },
    {
        'id': 'BIB-EX-75-03', 'source': 'SEG_EXEG_1975-11-05_SECTION_013_19', 'field': 'raw_text',
        'anchor': 'The world of the Bible was suddenly around me',
        'pith': 'The world of the Bible was suddenly around me, and real, replacing our world',
        'group': 'exeg-1975', 'lane': 'A', 'register': 'A', 'relevance': 1,
        'citation': 'Exegesis, batch of 5 November 1975 (section 013)',
        'dated': '1975-11-05', 'dating_basis': 'Batch date.',
        'concepts': ['perception', 'biblical scenes', 'Koine Greek'],
        'speaker': 'Philip K. Dick',
        'context': 'The move from reading the Bible to perceiving it. Dick describes a '
                   'sudden sense that the biblical world is more real than the one '
                   'around him, and that he knows Koine Greek, the lingua franca of the time.',
    },
    {
        'id': 'BIB-EX-75-04', 'source': 'SEG_EXEG_1975-11-05_SECTION_013_20', 'field': 'raw_text',
        'anchor': 'The book the Bible is an analog of reality',
        'pith': 'The book the Bible is an analog of reality',
        'group': 'exeg-1975', 'lane': 'A', 'register': 'A', 'relevance': 1,
        'citation': 'Exegesis, batch of 5 November 1975 (section 013)',
        'dated': '1975-11-05', 'dating_basis': 'Batch date.',
        'concepts': ['stegonography', 'analog', 'reality'],
        'speaker': 'Philip K. Dick',
        'context': 'Dick now makes reality itself stegonographic, concealed in the way the '
                   'Bible is concealed, and calls the Bible an analog of that reality. The '
                   'phrase is the seed of the 1978 and 1981 claims that the Bible is a '
                   'model of the world.',
        'editorial_note': 'The transcription reads “stegenographic”; the card keeps the '
                          'sentence as written.',
    },
    {
        'id': 'BIB-EX-75-05', 'source': 'SEG_EXEG_1975-11-05_SECTION_013_13', 'field': 'raw_text',
        'anchor': 'calls Rome',
        'pith': 'calls Rome "the great and only real enemy of the new chosen people, the Church."',
        'group': 'exeg-1975', 'lane': 'A', 'register': 'A', 'relevance': 1,
        'citation': 'Exegesis, batch of 5 November 1975 (section 013)',
        'dated': '1975-11-05', 'dating_basis': 'Batch date.',
        'concepts': ['Jerusalem Bible', 'Rome', 'Antichrist'],
        'speaker': 'Philip K. Dick',
        'context': 'Dick’s reference works are named in the transcriptions. Here the '
                   'Jerusalem Bible’s notes (“the J Bible”) give him Rome as the real enemy '
                   'of the church, which he fits to his own 1974 vision of Rome.',
        'editorial_note': 'Dick calls it the J. Bible or the Jerusalem Bible; the '
                          'transcription OCR also reads “Jerusolam”.',
    },
    # ---- 15 September 1976 ---------------------------------------------
    {
        'id': 'BIB-EX-76-01', 'source': 'SEG_EXEG_1976-09-15_Dorothy_159', 'field': 'raw_text',
        'anchor': 'Acts is the part of the Bible which describes',
        'pith': 'Acts is the part of the Bible which describes the early apostolic age church',
        'group': 'exeg-1976', 'lane': 'A', 'register': 'A', 'relevance': 1,
        'citation': 'Exegesis, 15 September 1976 — the Acts material in Tears',
        'dated': '1976-09-15', 'dating_basis': 'Sitting date given in the folder.',
        'concepts': ['Acts', 'Tears', 'apostolic church', 'Paraclete'],
        'speaker': 'Philip K. Dick',
        'context': 'The claim the 1976 sitting is built on. Dick says the novel Flow My '
                   'Tears, the Policeman Said, which the Exegesis calls “Tears”, contains '
                   '“unmistakable material from Acts”, the book of the early church.',
        'editorial_note': 'Flow My Tears, the Policeman Said (1974; written 1970) is the '
                          'novel the Exegesis calls “Tears”.',
    },
    {
        'id': 'BIB-EX-76-02', 'source': 'SEG_EXEG_1976-09-15_Dorothy_176', 'field': 'raw_text',
        'anchor': 'I had never read Acts',
        'pith': 'I had never read Acts',
        'group': 'exeg-1976', 'lane': 'A', 'register': 'A', 'relevance': 1,
        'citation': 'Exegesis, 15 September 1976 — how the Acts material was found',
        'dated': '1976-09-15', 'dating_basis': 'Sitting date given in the folder.',
        'concepts': ['Acts', 'Father Rasch', 'Tears', 'the Ethiopian eunuch scene'],
        'speaker': 'Philip K. Dick',
        'context': 'Dick credits Father Rasch with pointing out the “Philip + the '
                   'black man” scene, which is in Acts 8. Dick says he had never read Acts '
                   'when he wrote the novel.',
        'editorial_note': 'The scene Rasch identifies is the baptism of an Ethiopian '
                          'official by Philip, Acts 8.26–40; the folder does not cite the verse.',
    },
    {
        'id': 'BIB-EX-76-03', 'source': 'SEG_EXEG_1976-09-15_Dorothy_177', 'field': 'raw_text',
        'anchor': 'how come I properly identified them',
        'pith': 'how come I properly identified them',
        'group': 'exeg-1976', 'lane': 'A', 'register': 'A', 'relevance': 1,
        'citation': 'Exegesis, 15 September 1976 — the puzzle of recognition',
        'dated': '1976-09-15', 'dating_basis': 'Sitting date given in the folder.',
        'concepts': ['recognition', 'Acts', 'anamnesis'],
        'speaker': 'Philip K. Dick',
        'context': 'Dick’s own puzzle. If he did not recognise the Acts material when he '
                   'wrote the novel, how did he identify it the month the book was released? '
                   'The question is raised, not answered, in the sitting.',
    },
    {
        'id': 'BIB-EX-76-04', 'source': 'SEG_EXEG_1976-09-15_Dorothy_170', 'field': 'raw_text',
        'anchor': 'the true world is that of Acts',
        'pith': 'the true world is that of Acts. Why Acts? The last period of the scriptures, the time of the paraclete',
        'group': 'exeg-1976', 'lane': 'A', 'register': 'A', 'relevance': 1,
        'citation': 'Exegesis, 15 September 1976 — Acts as the true world',
        'dated': '1976-09-15', 'dating_basis': 'Sitting date given in the folder.',
        'concepts': ['Acts', 'alibi world', 'Paraclete', 'simulation'],
        'speaker': 'Philip K. Dick',
        'context': 'Dick sets Acts against the “alibi world” of the novel. Our world is '
                   'the simulated one, and the true world is the apostolic age of Acts. '
                   'The argument turns on the Paraclete, the Spirit that succeeds Christ.',
    },
    {
        'id': 'BIB-EX-76-05', 'source': 'SEG_EXEG_1976-09-15_Dorothy_127', 'field': 'raw_text',
        'anchor': 'which makes the novel a form of scripture',
        'pith': 'Ubik wrote "Ubik," which makes the novel a form of scripture',
        'group': 'exeg-1976', 'lane': 'A', 'register': 'A', 'relevance': 2,
        'citation': 'Exegesis, 15 September 1976 — the novels as automatic writing',
        'dated': '1976-09-15', 'dating_basis': 'Sitting date given in the folder.',
        'concepts': ['Ubik', 'scripture', 'automatic writing'],
        'speaker': 'Philip K. Dick',
        'context': 'Dick treats his own novel as dictated, and so as scripture. The '
                   'category is one he later applies to the Bible itself.',
    },
    {
        'id': 'BIB-EX-76-06', 'source': 'SEG_EXEG_1976-09-15_Dorothy_80', 'field': 'raw_text',
        'anchor': "In the Bible isn't about the past",
        'pith': 'In the Bible isn\'t about the past; it\'s code to describe our world (as is "Tears")',
        'group': 'exeg-1976', 'lane': 'A', 'register': 'A', 'relevance': 1,
        'citation': 'Exegesis, 15 September 1976 — the Bible as code',
        'dated': '1976-09-15', 'dating_basis': 'Sitting date given in the folder.',
        'concepts': ['code', 'the present', 'Tears'],
        'speaker': 'Philip K. Dick',
        'context': 'The central move of the sitting. The Bible is not a chronicle of '
                   'events long past; it is a code describing the reader’s own world, as '
                   'Tears is. Dick draws the comparison himself.',
    },
    {
        'id': 'BIB-EX-76-07', 'source': 'SEG_EXEG_1976-09-15_Dorothy_232', 'field': 'raw_text',
        'anchor': 'The ending of Malachi makes it absolutely clear',
        'pith': 'The ending of Malachi makes it absolutely clear that God (1) foresaw the ABSENCE of Elijah from the world',
        'group': 'exeg-1976', 'lane': 'A', 'register': 'A', 'relevance': 1,
        'citation': 'Exegesis, 15 September 1976 — Malachi and Elijah',
        'dated': '1976-09-15', 'dating_basis': 'Sitting date given in the folder.',
        'concepts': ['Malachi', 'Elijah', 'Second Coming'],
        'speaker': 'Philip K. Dick',
        'context': 'Malachi’s closing prophecy of Elijah’s return gives Dick the chronology '
                   'of the Second Coming: God foresaw the long absence, and the return is '
                   'part of the plan. Elijah recurs in every stage of his Bible reading.',
    },
    # ---- 10 October 1978 folder ----------------------------------------
    {
        'id': 'BIB-EX-78-01', 'source': 'SEG_EXEG_1978-10-10_SECTION_016_207', 'field': 'raw_text',
        'anchor': 'is the Living Torah, the informational basis of reality',
        'pith': 'is the Living Torah, the informational basis of reality',
        'group': 'exeg-1978', 'lane': 'A', 'register': 'A', 'relevance': 1,
        'citation': 'Exegesis, folder of 10 October 1978 (section 016)',
        'dated': '1978-10-10', 'dating_basis': 'Folder date; no internal date in the entry.',
        'concepts': ['Torah', 'plasmate', 'information', 'Kabbalah'],
        'speaker': 'Philip K. Dick',
        'context': 'The Torah replaces Acts as the source of the cypher in Tears. Dick says '
                   'the plasmate, the living information he has been describing, is the '
                   'Torah, and that the 1974 experience was Kabbalistic.',
    },
    {
        'id': 'BIB-EX-78-02', 'source': 'SEG_EXEG_1978-10-10_SECTION_016_226', 'field': 'raw_text',
        'anchor': 'Because he depreciated the Torah',
        'pith': 'Because he depreciated the Torah',
        'group': 'exeg-1978', 'lane': 'A', 'register': 'A', 'relevance': 1,
        'citation': 'Exegesis, folder of 10 October 1978 (section 016)',
        'dated': '1978-10-10', 'dating_basis': 'Folder date. The entry is followed by a note dated 12-29-80.',
        'concepts': ['Torah', 'Jesus', 'Hebrew prophets'],
        'speaker': 'Philip K. Dick',
        'context': 'Dick’s explanation of why Israel rejected Jesus: he “depreciated the '
                   'Torah”. Only a claim to be God, the Son of God, or Hagia Sophia could '
                   'give him authority to do so.',
        'editorial_note': 'The entry sits among entries dated 1980 (one reads 12-29-80), so '
                          'the folder date is a batch date.',
    },
    {
        'id': 'BIB-EX-78-03', 'source': 'SEG_EXEG_1978-10-10_SECTION_016_321', 'field': 'raw_text',
        'anchor': 'herewith I just lost my Trinitarianism',
        'pith': 'herewith I just lost my Trinitarianism',
        'group': 'exeg-1978', 'lane': 'A', 'register': 'A', 'relevance': 1,
        'citation': 'Exegesis, folder of 10 October 1978 (section 016)',
        'dated': '1978-10-10', 'dating_basis': 'Folder date; the entry sits among entries dated 1980.',
        'concepts': ['Trinity', 'scripture', 'Wisdom', 'Proverbs 8'],
        'speaker': 'Philip K. Dick',
        'context': 'The cost of the argument. Dick says he has lost his Trinitarianism on '
                   'the evidence of his two experiences and of scripture, and points to '
                   'scripture itself as the second ground.',
    },
    {
        'id': 'BIB-EX-78-04', 'source': 'SEG_EXEG_1978-10-10_SECTION_016_252', 'field': 'raw_text',
        'anchor': 'New Scriptures are needed',
        'pith': 'New Scriptures are needed, new prophets and perhaps a new savior',
        'group': 'exeg-1978', 'lane': 'A', 'register': 'A', 'relevance': 1,
        'citation': 'Exegesis, folder of 10 October 1978 (section 016)',
        'dated': '1978-10-10', 'dating_basis': 'Folder date.',
        'concepts': ['third age', 'new scripture', 'prophecy'],
        'speaker': 'Philip K. Dick',
        'context': 'Dick’s programme for the third age: each age has its own Torah, and the '
                   'third is as revolutionary against the second as the second was against '
                   'the first. The canon, on this view, is not closed.',
    },
    {
        'id': 'BIB-EX-78-05', 'source': 'SEG_EXEG_1978-10-10_SECTION_016_189', 'field': 'raw_text',
        'anchor': 'that Valis turned that info into our world',
        'pith': 'that Valis turned that info into our world',
        'group': 'exeg-1978', 'lane': 'A', 'register': 'A', 'relevance': 2,
        'citation': 'Exegesis, folder of 10 October 1978 (section 016)',
        'dated': '1978-10-10', 'dating_basis': 'Folder date.',
        'concepts': ['VALIS', 'information', 'world-building'],
        'speaker': 'Philip K. Dick',
        'context': 'The mechanism. Dick proposes that the world of 1970–74 was built on '
                   'information contained in the Bible, and that VALIS converted that '
                   'information into the world. Any book that describes a world, he adds, '
                   'could do the same.',
        'editorial_note': 'The transcription is partly garbled at this point; the phrase '
                          'quoted is clear.',
    },
    {
        'id': 'BIB-EX-78-06', 'source': 'SEG_EXEG_1978-10-10_SECTION_016_307', 'field': 'raw_text',
        'anchor': 'using the Bible as a encoding-decoding grid',
        'pith': 'using the Bible as a encoding-decoding grid',
        'group': 'exeg-1978', 'lane': 'A', 'register': 'A', 'relevance': 2,
        'citation': 'Exegesis, folder of 10 October 1978 (section 016)',
        'dated': '1978-10-10', 'dating_basis': 'Folder date.',
        'concepts': ['code', 'control', 'history'],
        'speaker': 'Philip K. Dick',
        'context': 'The political reading. Dick imagines an agency using the Bible as a '
                   'grid for encoding and decoding messages, because biblical material '
                   'floats around everywhere, all the time.',
    },
    {
        'id': 'BIB-EX-78-07', 'source': 'SEG_EXEG_1978-10-10_SECTION_016_151', 'field': 'raw_text',
        'anchor': 'My visualizing the Bible in 3-D',
        'pith': 'My visualizing the Bible in 3-D: layers according to age (time as spacial axis)',
        'group': 'exeg-1978', 'lane': 'A', 'register': 'A', 'relevance': 2,
        'citation': 'Exegesis, folder of 10 October 1978 (section 016)',
        'dated': '1978-10-10', 'dating_basis': 'Folder date.',
        'concepts': ['three dimensions', 'time', 'layers', 'hologram'],
        'speaker': 'Philip K. Dick',
        'context': 'The image that the trilogy will dramatise. Dick pictures the Bible as a '
                   'three-dimensional object, with its strata ordered by the age of the '
                   'texts, so that time becomes a spatial axis.',
    },
    # ---- 16 April 1981 -------------------------------------------------
    {
        'id': 'BIB-EX-81-01', 'source': 'SEG_EXEG_1981-04-16_Pat_140', 'field': 'raw_text',
        'anchor': 'the Bible is not a verbal description of a world',
        'pith': 'the Bible is not a verbal description of a world; it is a world',
        'group': 'exeg-1981', 'lane': 'A', 'register': 'A', 'relevance': 1,
        'citation': 'Exegesis, 16 April 1981 — the Bible as world',
        'dated': '1981-04-16', 'dating_basis': 'Batch date for the April 1981 transcriptions.',
        'concepts': ['world', 'verbal form', 'Hebrew alphabet'],
        'speaker': 'Philip K. Dick',
        'context': 'The last step in the sequence. The Bible is not a description of a world '
                   'but a world in verbal form. Dick ties the idea to the Hebrew alphabet '
                   'and to the plasmate of 1978.',
    },
    {
        'id': 'BIB-EX-81-02', 'source': 'SEG_EXEG_1981-04-16_Pat_151', 'field': 'raw_text',
        'anchor': 'it was the O.T. that I read',
        'pith': 'it was the O.T. that I read, not the N.T., esp. the part about Elijah',
        'group': 'exeg-1981', 'lane': 'A', 'register': 'A', 'relevance': 1,
        'citation': 'Exegesis, 16 April 1981 — the first Bible he read',
        'dated': '1981-04-16', 'dating_basis': 'Batch date.',
        'concepts': ['Old Testament', 'Elijah', 'childhood'],
        'speaker': 'Philip K. Dick',
        'context': 'Autobiography in the Bible argument. The first Bible he read in junior '
                   'high school was the Old Testament, and above all the Elijah passages, '
                   'which he calls his great dream. The later claims grow from that reading.',
    },
    {
        'id': 'BIB-EX-81-03', 'source': 'SEG_EXEG_1981-04-16_Pat_86', 'field': 'raw_text',
        'anchor': 'the touchstone (oh please do not forget this!) is the Bible',
        'pith': 'the touchstone (oh please do not forget this!) is the Bible',
        'group': 'exeg-1981', 'lane': 'A', 'register': 'A', 'relevance': 1,
        'citation': 'Exegesis, 16 April 1981 — the Bible as touchstone',
        'dated': '1981-04-16', 'dating_basis': 'Batch date.',
        'concepts': ['touchstone', 'actual', 'true', 'alive', 'sentient'],
        'speaker': 'Philip K. Dick',
        'context': 'Dick’s test for any account of reality, set out as four properties. The '
                   'Bible is the touchstone because it is actual, true, alive and a '
                   'sentient organism with the keys to the world.',
    },
    {
        'id': 'BIB-EX-81-04', 'source': 'SEG_EXEG_1981-04-16_Pat_160', 'field': 'raw_text',
        'anchor': 'the world of the Bible, specifically Acts',
        'pith': 'the world of the Bible, specifically Acts - the 2nd half of Luke',
        'group': 'exeg-1981', 'lane': 'A', 'register': 'A', 'relevance': 1,
        'citation': 'Exegesis, 16 April 1981 — Acts and Luke',
        'dated': '1981-04-16', 'dating_basis': 'Batch date.',
        'concepts': ['Acts', 'Luke', 'infinity mode'],
        'speaker': 'Philip K. Dick',
        'context': 'The 1974 experience, identified with a passage. Dick says the enhanced '
                   '“infinity” mode he saw in 1974 was the world of the Bible, specifically '
                   'the second half of Luke, which is Acts.',
    },
    {
        'id': 'BIB-EX-81-05', 'source': 'SEG_EXEG_1981-04-16_Pat_76', 'field': 'raw_text',
        'anchor': 'Augustine called the Bible',
        'pith': 'Augustine called the Bible "Letters from home"',
        'group': 'exeg-1981', 'lane': 'A', 'register': 'A', 'relevance': 2,
        'citation': 'Exegesis, 16 April 1981 — letters from home',
        'dated': '1981-04-16', 'dating_basis': 'Batch date.',
        'concepts': ['Augustine', 'veiled messages', 'Holy Spirit'],
        'speaker': 'Philip K. Dick',
        'context': 'Dick borrows Augustine’s image of the Bible as letters from home, '
                   'and argues that the veiled messages in it were placed there by the '
                   'Holy Spirit, so that only the Spirit can read them fully.',
    },
    {
        'id': 'BIB-EX-81-06', 'source': 'SEG_EXEG_1981-04-16_Pat_67', 'field': 'raw_text',
        'anchor': 'no canon, no precedent',
        'pith': 'no canon, no precedent; each person + situation unique',
        'group': 'exeg-1981', 'lane': 'A', 'register': 'A', 'relevance': 1,
        'citation': 'Exegesis, 16 April 1981 — recombinant scripture',
        'dated': '1981-04-16', 'dating_basis': 'Batch date.',
        'concepts': ['recombinant scripture', 'canon', 'unique situation'],
        'speaker': 'Philip K. Dick',
        'context': 'The term Dick coins for what replaces a closed canon: “recombinant '
                   'scripture”, which has no canon and no precedent, and is unique to each '
                   'person and situation.',
        'editorial_note': 'The transcription has a stray quotation mark after “recombinant '
                          'scripture”; the term is clear.',
    },
    {
        'id': 'BIB-EX-81-07', 'source': 'SEG_EXEG_1981-04-16_Pat_118', 'field': 'raw_text',
        'anchor': 'unprecedented third testament',
        'pith': 'unprecedented third testament emanating out of the O.T. + N.T.',
        'group': 'exeg-1981', 'lane': 'A', 'register': 'A', 'relevance': 1,
        'citation': 'Exegesis, 16 April 1981 — the third testament',
        'dated': '1981-04-16', 'dating_basis': 'Batch date.',
        'concepts': ['third testament', 'Torah', 'Kerygma'],
        'speaker': 'Philip K. Dick',
        'context': 'Dick’s name for what his own writing has produced: a third testament '
                   'coming out of the Old and New Testaments, which sees the Torah in the '
                   'Kerygma of the New Testament, advancing into this new form.',
    },
    {
        'id': 'BIB-EX-81-08', 'source': 'SEG_EXEG_1981-04-16_Pat_44', 'field': 'raw_text',
        'anchor': 'Torah does not know everything',
        'pith': 'Torah does not know everything. Christ does.',
        'group': 'exeg-1981', 'lane': 'A', 'register': 'A', 'relevance': 1,
        'citation': 'Exegesis, 16 April 1981 — Torah and Christ',
        'dated': '1981-04-16', 'dating_basis': 'Batch date.',
        'concepts': ['Torah', 'Christ', 'dialectic', 'knowledge'],
        'speaker': 'Philip K. Dick',
        'context': 'The hierarchy at the end of the Torah passages. The law is the frame, '
                   'and Christ is the one who knows what the frame does not. Dick calls this '
                   'the story the whole Bible tells.',
    },
    # ---- The trilogy, as full text -------------------------------------
    {
        'id': 'BIB-TR-VAL-01', 'source': 'valis_chapter_5_text', 'field': 'chapter_text',
        'anchor': 'corrupt parts of the Bible',
        'pith': 'I’ll ask Larry if that’s one of the corrupt parts of the Bible',
        'group': 'fiction', 'lane': 'A', 'register': 'A', 'relevance': 2,
        'citation': 'VALIS, chapter 5',
        'dated': '1981', 'dating_basis': 'Publication year.',
        'concepts': ['Sherri', 'scripture', 'corruption', 'Britannica'],
        'speaker': 'Sherri (character)',
        'context': 'Sherri, the sceptical member of the group, asks whether a passage Fat '
                   'has quoted is one of “the corrupt parts of the Bible”. Fat has been '
                   'reading the Britannica on the secrecy theme in Mark and Matthew.',
    },
    {
        'id': 'BIB-TR-VAL-02', 'source': 'valis_chapter_10_text', 'field': 'chapter_text',
        'anchor': 'Kevin had become a Bible scholar',
        'pith': 'Now Kevin had become a Bible scholar, to Fat’s amusement',
        'group': 'fiction', 'lane': 'A', 'register': 'A', 'relevance': 2,
        'citation': 'VALIS, chapter 10',
        'dated': '1981', 'dating_basis': 'Publication year.',
        'concepts': ['Kevin', 'Daniel', 'Nixon', 'prophecy'],
        'speaker': 'Narrator (Horselover Fat’s circle)',
        'context': 'Kevin reads the two apocalyptic books of the Bible for clues, and finds in '
                   'Daniel a passage he believes describes Nixon. Fat finds the convert '
                   'amusing, and the scene shows how prophecy is put to use.',
    },
    {
        'id': 'BIB-TR-VAL-03', 'source': 'valis_chapter_11_text', 'field': 'chapter_text',
        'anchor': 'it entered our Bible',
        'pith': 'it entered our Bible—it’s older than our Bible',
        'group': 'fiction', 'lane': 'A', 'register': 'A', 'relevance': 2,
        'citation': 'VALIS, chapter 11',
        'dated': '1981', 'dating_basis': 'Publication year.',
        'concepts': ['Psalm 104', 'Akhenaten', 'older sources'],
        'speaker': 'Horselover Fat (character)',
        'context': 'Fat identifies Psalm 104 with the hymn of Akhenaten, and says the hymn '
                   'is older than the Bible that absorbed it. The Exegesis makes the same '
                   'claim about the Old Testament in 1975.',
    },
    {
        'id': 'BIB-TR-DI-01', 'source': 'divine_invasion_chapter_2_text', 'field': 'chapter_text',
        'anchor': 'layers at different depths within the hologram',
        'pith': 'the Bible expressed as layers at different depths within the hologram, each layer according to age',
        'group': 'fiction', 'lane': 'A', 'register': 'A', 'relevance': 1,
        'citation': 'The Divine Invasion, chapter 2',
        'dated': '1981', 'dating_basis': 'Publication year.',
        'concepts': ['hologram', 'three dimensions', 'Elias', 'Emmanuel'],
        'speaker': 'Narrator (Emmanuel)',
        'context': 'The Exegesis’s three-dimensional Bible made into a scene. Elias’s '
                   'holoscope lays out the Bible in layers by age, and Emmanuel studies it, '
                   'reading the total structure as a three-dimensional cosmos.',
    },
    {
        'id': 'BIB-TR-DI-02', 'source': 'divine_invasion_chapter_2_text', 'field': 'chapter_text',
        'anchor': 'never twice the same',
        'pith': 'It became a sentient organism that was never twice the same',
        'group': 'fiction', 'lane': 'A', 'register': 'A', 'relevance': 1,
        'citation': 'The Divine Invasion, chapter 2',
        'dated': '1981', 'dating_basis': 'Publication year.',
        'concepts': ['sentient scripture', 'Church', 'hologram', 'interpretation'],
        'speaker': 'Narrator (Emmanuel)',
        'context': 'Once the Bible is superimposed on a hologram, it is in dialogue with '
                   'the reader and changes each time. The Church forbids the manufacture of '
                   'such holograms because of this, and the novel names the stakes.',
    },
    {
        'id': 'BIB-TR-DI-03', 'source': 'divine_invasion_chapter_2_text', 'field': 'chapter_text',
        'anchor': 'it is alive; it existed before creation',
        'pith': 'Torah is the totality of divine disclosure by God; it is alive; it existed before creation',
        'group': 'fiction', 'lane': 'A', 'register': 'A', 'relevance': 1,
        'citation': 'The Divine Invasion, chapter 2',
        'dated': '1981', 'dating_basis': 'Publication year.',
        'concepts': ['Torah', 'creation', 'divine disclosure'],
        'speaker': 'Elias (character)',
        'context': 'Elias defines the Torah as the whole of God’s disclosure, living and '
                   'prior to creation, and not merely as law. The definition matches the '
                   'living Torah of the 1978 Exegesis.',
    },
    {
        'id': 'BIB-TR-DI-04', 'source': 'divine_invasion_chapter_4_text', 'field': 'chapter_text',
        'anchor': 'I am the Torah',
        'pith': 'I am the Torah',
        'group': 'fiction', 'lane': 'A', 'register': 'A', 'relevance': 1,
        'citation': 'The Divine Invasion, chapter 4',
        'dated': '1981', 'dating_basis': 'Publication year.',
        'concepts': ['Zina Pallas', 'Torah', 'Malkuth', 'Shekhinah'],
        'speaker': 'Zina Pallas (character)',
        'context': 'Zina announces that she is the Torah, the living blueprint of the '
                   'cosmos, and Emmanuel must consult her before he acts on the universe. '
                   'The Exegesis’s claim that the Torah is a living mind acquires a speaker.',
    },
    {
        'id': 'BIB-TR-DI-05', 'source': 'divine_invasion_chapter_2_text', 'field': 'chapter_text',
        'anchor': 'as an addendum, but he knew that he should not',
        'pith': 'He wanted to feed that into the hologram of the Bible, as an addendum, but he knew that he should not',
        'group': 'fiction', 'lane': 'A', 'register': 'A', 'relevance': 2,
        'citation': 'The Divine Invasion, chapter 2',
        'dated': '1981', 'dating_basis': 'Publication year.',
        'concepts': ['addition to scripture', 'restraint', 'hologram'],
        'speaker': 'Emmanuel (character)',
        'context': 'Emmanuel wants to add a line of his own to the Bible’s hologram, and '
                   'holds back. The restraint is the novel’s inverse of the Exegesis, where '
                   'Dick is sure of his right to add to scripture.',
    },
    # ---- Scholarship ----------------------------------------------------
    {
        'id': 'BIB-SCH-01', 'source': 'DOC_ARCH_DAVIS_HYMN_OF_PHILIP_K_DICK_ASE_TALK',
        'field': 'page_summary',
        'anchor': 'embedded in the third-century Acts of Thomas',
        'pith': 'embedded in the third-century Acts of Thomas',
        'group': 'scholarship', 'lane': 'C', 'register': 'C', 'relevance': 1,
        'citation': 'Davis, “The Hymn of Philip K. Dick” (ASE conference talk)',
        'dated': None, 'dating_basis': 'Catalogue record; the talk is undated here.',
        'concepts': ['Hymn of the Pearl', 'Acts of Thomas', 'Gnostic text'],
        'speaker': None,
        'context': 'Davis traces Dick’s use of the Hymn of the Pearl, which is embedded in '
                   'the third-century Acts of Thomas, from a 1975 letter onward. The Acts '
                   'in question are apocryphal, and not the canonical Acts Dick works with.',
        'editorial_note': 'The record is a summary. The talk itself is not held.',
    },
    {
        'id': 'BIB-SCH-02', 'source': 'DOC_ARCH_THEORY_CULTURE_AMP_SOCIETY_2008_DEC_VOL_',
        'field': 'page_summary',
        'anchor': 'the theology of Saint Paul',
        'pith': 'the theology of Saint Paul',
        'group': 'scholarship', 'lane': 'C', 'register': 'C', 'relevance': 2,
        'citation': 'Burton, Theory, Culture & Society (December 2008)',
        'dated': '2008-12', 'dating_basis': 'Publication date of the issue.',
        'concepts': ['Bergson', 'Paul', 'theology'],
        'speaker': None,
        'context': 'Burton reads Dick’s fiction against Bergson and against the theology of '
                   'Saint Paul, the reading that Burton later develops in his monograph on '
                   'Dick and Bergson.',
        'editorial_note': 'Burton’s essay is summarised here, not held.',
    },
    {
        'id': 'BIB-SCH-03', 'source': 'DOC_ARCH_ROSICRUCIAN_PKD_SOURCES', 'field': 'page_summary',
        'anchor': 'Paul of Tarsus, Simon Magus',
        'pith': 'Paul of Tarsus, Simon Magus',
        'group': 'scholarship', 'lane': 'C', 'register': 'C', 'relevance': 2,
        'citation': 'Rosicrucian PKD Sources (archive record)',
        'dated': None, 'dating_basis': 'Catalogue record.',
        'concepts': ['Tractate Cryptica Scriptura', 'Paul of Tarsus', 'secret knowledge'],
        'speaker': None,
        'context': 'The record describes the VALIS appendix, the Tractates Cryptica '
                   'Scriptura, which lists Paul of Tarsus among those said to have known a '
                   'great secret about moving backward in time.',
        'editorial_note': 'The appendix itself is Dick’s text, but the record summarising it '
                          'is editorial, so the card is registered C.',
    },
    # ---- Letters, full text, 1964-1981 ----------------------------------
    {
        'id': 'BIB-LET-64-01', 'source': 'LET_1964-05-22_JAMES_BLISH_0062', 'field': 'body_md',
        'anchor': 'My priest says the Bible is not the story',
        'pith': "My priest says the Bible is not the story of man's search for God but of God's search for man.",
        'group': 'letters-1964', 'lane': 'A', 'register': 'A', 'relevance': 1,
        'citation': 'Letter to James Blish, 22 May 1964',
        'dated': '1964-05-22', 'dating_basis': 'Dated in the letter.',
        'concepts': ['God’s search for man', 'the Redeemer', 'priest'],
        'speaker': 'Philip K. Dick',
        'context': 'Dick repeats his priest’s line that the Bible is “not the story of man’s search for God but of God’s search for man,” and sets it against his own inability to see the Redeemer. It is the earliest Bible passage in the letters, and it reads the Bible from the side of God’s search.',
    },
    {
        'id': 'BIB-LET-73-01', 'source': 'LET_1973-01-07_ART_SPIEGELMAN_MICHELE_GROSS_0062', 'field': 'body_md',
        'anchor': 'The project nearest and dearest to my heart',
        'pith': 'The project nearest and dearest to my heart',
        'group': 'letters-1973', 'lane': 'A', 'register': 'A', 'relevance': 1,
        'citation': 'Letter to Art Spiegelman and Michele Gross, 7 January 1973',
        'dated': '1973-01-07', 'dating_basis': 'Dated in the letter.',
        'concepts': ['rhymed couplets', 'translation', 'Genesis'],
        'speaker': 'Philip K. Dick',
        'context': 'A progress report on the project begun as a joke in 1972: the Bible turned into rhymed couplets is, Dick says, “coming along fine,” with the first one already firmly jelled and on paper. The joke has become a working method.',
    },
    {
        'id': 'BIB-LET-75-01', 'source': 'LET_1975-03-04_ROBERT_ORNSTEIN_0075', 'field': 'body_md',
        'anchor': 'the New Testament is in cypher',
        'pith': 'Studying the Bible, along with this Qumran personality, Brady finds that the New Testament is in cypher.',
        'group': 'letters-1975', 'lane': 'A', 'register': 'A', 'relevance': 1,
        'citation': 'Letter to Robert Ornstein, 4 March 1975',
        'dated': '1975-03-04', 'dating_basis': 'Dated in the letter.',
        'concepts': ['cypher', 'Qumran', 'New Testament', 'Nicholas Brady'],
        'speaker': 'Philip K. Dick',
        'context': 'Dick’s account of the character Brady, who studies the Bible with a Qumran figure and finds the New Testament written in cypher. The same claim is made to Claudia Bush on 16 February 1975, where Dick says that John Allegro is right and the New Testament is a cypher.',
    },
    {
        'id': 'BIB-LET-75-02', 'source': 'LET_1975-07-10_GORAN_BENGTSON_0114', 'field': 'body_md',
        'anchor': 'the moment foretold in the Bible',
        'pith': 'this is indeed the moment foretold in the Bible when the graves will open and give forth their dead, that in fact the Parousia has arrived',
        'group': 'letters-1975', 'lane': 'A', 'register': 'A', 'relevance': 1,
        'citation': 'Letter to Göran Bengtson, 10 July 1975',
        'dated': '1975-07-10', 'dating_basis': 'Dated in the letter.',
        'concepts': ['Parousia', 'the graves', 'eschatology'],
        'speaker': 'Philip K. Dick',
        'context': 'Dick describes the moment at which the realisation spreads that nothing has misfired. It is the moment foretold in the Bible, when the graves open, and the Parousia has arrived, but not in the form anyone had anticipated.',
    },
    {
        'id': 'BIB-LET-76-01', 'source': 'LET_1976-09-06_DOROTHY_HUDNER_0287', 'field': 'body_md',
        'anchor': 'the prophecies of the Bible are all true',
        'pith': 'It was shown to me that the prophecies of the Bible are all true and are systematically being fulfilled.',
        'group': 'letters-1976-78', 'lane': 'A', 'register': 'A', 'relevance': 1,
        'citation': 'Letter to Dorothy Hudner, 6 September 1976',
        'dated': '1976-09-06', 'dating_basis': 'Dated in the letter.',
        'concepts': ['prophecy', 'Parousia', 'Rome', 'Prince of This World'],
        'speaker': 'Philip K. Dick',
        'context': 'Nine days before the Exegesis sitting on Acts in Tears, Dick tells Dorothy Hudner that the prophecies of the Bible are being fulfilled, and that the Parousia is not far off. Rome is the physical presence of the evil spirit, the Prince of This World.',
    },
    {
        'id': 'BIB-LET-77-01', 'source': 'LET_1977-08-21_EUGENE_WARREN_0036', 'field': 'body_md',
        'anchor': 'after which I have read the Bible',
        'pith': 'after which I have read the Bible (the N.T. particularly) again and again',
        'group': 'letters-1976-78', 'lane': 'A', 'register': 'A', 'relevance': 1,
        'citation': 'Letter to Eugene Warren, 21 August 1977',
        'dated': '1977-08-21', 'dating_basis': 'Dated in the letter.',
        'concepts': ['conversion', 'March 1974', 'New Testament', 'Ephesians'],
        'speaker': 'Philip K. Dick',
        'context': 'Dick dates his conversion experience to March 1974, and says that since then he has read the Bible, the New Testament particularly, again and again. The letter also names two parts of what was revealed to him as the most striking, one of them the Jerusalem Bible’s note on Ephesians 1:10.',
    },
    {
        'id': 'BIB-LET-80-01', 'source': 'LET_1980-02-28_JONATHAN_SILVERMAN_SCOTT_MERED_0009', 'field': 'body_md',
        'anchor': 'the Torah can be equated with Holy Wisdom',
        'pith': 'I have already discovered that the Torah can be equated with Holy Wisdom (Hagia Sophia) of Proverbs 8',
        'group': 'letters-1980-81', 'lane': 'A', 'register': 'A', 'relevance': 1,
        'citation': 'Letter to Jonathan Silverman, 28 February 1980',
        'dated': '1980-02-28', 'dating_basis': 'Dated in the letter.',
        'concepts': ['Torah', 'Hagia Sophia', 'Proverbs 8', 'Hertz'],
        'speaker': 'Philip K. Dick',
        'context': 'Dick reports his reading of the Torah with the notes of J. H. Hertz, late Chief Rabbi of the British Empire, and concludes that the Torah can be equated with Holy Wisdom, the Hagia Sophia of Proverbs 8, who was alive and existed before creation.',
    },
    {
        'id': 'BIB-LET-81-01', 'source': 'LET_1981-07-15_PATRICIA_WARRICK_0103', 'field': 'body_md',
        'anchor': 'recombinant information/scripture',
        'pith': 'We have what I call recombinant information/scripture; a given message applies to one person for one situation only',
        'group': 'letters-1980-81', 'lane': 'A', 'register': 'A', 'relevance': 1,
        'citation': 'Letter to Patricia Warrick, 15 July 1981',
        'dated': '1981-07-15', 'dating_basis': 'Dated in the letter.',
        'concepts': ['recombinant scripture', 'canon', 'information'],
        'speaker': 'Philip K. Dick',
        'context': 'The term the Exegesis uses for scripture after the canon, given to Patricia Warrick in a letter. In the third period there is no canon at all: “we have gone beyond the N.T. just as the N.T. went beyond the O.T.” A message applies to one person in one situation, and is then scrapped.',
    },
    {
        'id': 'BIB-LET-81-02', 'source': 'LET_1981-08-18_PATRICIA_WARRICK_0132', 'field': 'body_md',
        'anchor': 'The Bible is the information that is fed into the space-time universe',
        'pith': 'The Bible is the information that is fed into the space-time universe, as if transduced into substantial reality.',
        'group': 'letters-1980-81', 'lane': 'A', 'register': 'A', 'relevance': 1,
        'citation': 'Letter to Patricia Warrick, 18 August 1981',
        'dated': '1981-08-18', 'dating_basis': 'Dated in the letter.',
        'concepts': ['information', 'space-time', 'Joachim of Fiore', 'transduction'],
        'speaker': 'Philip K. Dick',
        'context': 'The fullest statement in the letters of the 1981 theory. The Bible is not a description of this world but the verbal source of the world. Dick explains it through Joachim of Fiore, and calls the source a single living form.',
    },
    {
        'id': 'BIB-LET-81-03', 'source': 'LET_1981-08-18_PATRICIA_WARRICK_0132', 'field': 'body_md',
        'anchor': 'a single coherent life form underlies the written Bible',
        'pith': 'a single coherent life form underlies the written Bible, and it is the source of our universe, and is itself not fixed into a canon',
        'group': 'letters-1980-81', 'lane': 'A', 'register': 'A', 'relevance': 1,
        'citation': 'Letter to Patricia Warrick, 18 August 1981',
        'dated': '1981-08-18', 'dating_basis': 'Dated in the letter.',
        'concepts': ['life form', 'canon', 'written Bible', 'recombination'],
        'speaker': 'Philip K. Dick',
        'context': 'The same letter says that a single living form underlies the written Bible and is the source of the universe. The form is not fixed into a canon but constantly combines and recombines, so the canon is a snapshot of something still moving.',
    },
    {
        'id': 'BIB-LET-81-04', 'source': 'LET_1981-06-03_RUSSELL_GALEN_0088', 'field': 'body_md',
        'anchor': 'completely misuses the Bible',
        'pith': 'Tim Archer completely misuses the Bible in the scene in which Angel tries to talk him out of his secret affair with Kirsten',
        'group': 'letters-1980-81', 'lane': 'A', 'register': 'A', 'relevance': 1,
        'citation': 'Letter to Russell Galen, 3 June 1981',
        'dated': '1981-06-03', 'dating_basis': 'Dated in the letter.',
        'concepts': ['Transmigration of Timothy Archer', 'scripture', 'lawyer'],
        'speaker': 'Philip K. Dick',
        'context': 'Dick rereads The Transmigration of Timothy Archer and sees that Tim Archer misuses the Bible in the scene with Angel and Kirsten. He uses it not as a man of God but as a lawyer, so that scripture becomes a basis for dishonest and carnal action.',
    },
    {
        'id': 'BIB-LET-81-05', 'source': 'LET_1981-08-20_URSULA_K_LE_GUIN_0133', 'field': 'body_md',
        'anchor': 'The Torah has enchanted me',
        'pith': 'The Torah has enchanted me with its haunting concern for all creatures, especially the weak, the harmless and the disadvantaged.',
        'group': 'letters-1980-81', 'lane': 'A', 'register': 'A', 'relevance': 1,
        'citation': 'Letter to Ursula K. Le Guin, 20 August 1981',
        'dated': '1981-08-20', 'dating_basis': 'Dated in the letter.',
        'concepts': ['Torah', 'Deuteronomy', 'the weak', 'bird’s nest'],
        'speaker': 'Philip K. Dick',
        'context': 'Dick praises Deuteronomy to Ursula Le Guin, and quotes the law about the bird’s nest. The Torah is read here for its ethics and its concern for the weak, where the 1976 and 1978 writing reads it as code and as the informational basis of the world.',
    },
    # ---- Interviews, full text --------------------------------------------
    {
        'id': 'BIB-INT-01', 'source': 'DOC_ARCH_PKD_MAGAZINE_INTERVIEWS', 'field': 'markdown_content',
        'anchor': 'I did a very detailed study of the Torah',
        'pith': 'I did a very detailed study of the Torah and the basic tenets of Judaism for it.',
        'group': 'interviews', 'lane': 'A', 'register': 'A', 'relevance': 1,
        'citation': 'PKD Magazine Interviews (compiled), undated interview headed “Philip K. Dick”',
        'dated': None, 'dating_basis': 'The compilation does not date this passage.',
        'concepts': ['Torah', 'Judaism', 'The Divine Invasion'],
        'speaker': 'Philip K. Dick',
        'context': 'Asked how the resolution of the novel came about, Dick says it is resolved “in terms of Judaism,” and that he made a very detailed study of the Torah for it. He says he is not Jewish, and had not been drawn to the religion before, but that the study gave him “tremendous respect” for it.',
    },
    {
        'id': 'BIB-INT-02', 'source': 'DOC_ARCH_PKD_MAGAZINE_INTERVIEWS', 'field': 'markdown_content',
        'anchor': 'I was reading Deuteronomy last night',
        'pith': 'I was reading Deuteronomy last night, and some of the notes by Rabbi Hertz, who is the late Chief Rabbi of the British Empire.',
        'group': 'interviews', 'lane': 'A', 'register': 'A', 'relevance': 1,
        'citation': 'PKD Magazine Interviews (compiled), undated interview',
        'dated': None, 'dating_basis': 'The compilation does not date this passage.',
        'concepts': ['Deuteronomy', 'Hertz', 'care for the poor'],
        'speaker': 'Philip K. Dick',
        'context': 'Dick says he was reading Deuteronomy the night before, with the notes of Rabbi Hertz, and marvels that the injunctions to care for the needy, the sick and the poor are built into a text some three thousand years old. The passage follows a remark about a story on Haig and Reagan, which Dick treats as a story idea.',
    },
    {
        'id': 'BIB-INT-03', 'source': 'DOC_ARCH_PKD_MAGAZINE_INTERVIEWS', 'field': 'markdown_content',
        'anchor': 'The voice is identified as',
        'pith': 'The voice is identified as Ruah, which is the Old Testament word for the Spirit of God.',
        'group': 'interviews', 'lane': 'A', 'register': 'A', 'relevance': 2,
        'citation': 'PKD Magazine Interviews (compiled), undated interview with questions marked TZ',
        'dated': None, 'dating_basis': 'The compilation does not date this passage.',
        'concepts': ['Ruah', 'Spirit of God', 'tutelary spirit', 'VALIS'],
        'speaker': 'Philip K. Dick',
        'context': 'Asked whether the “tutelary spirit” still guides him, Dick says it has not spoken since he finished The Divine Invasion. He names the voice Ruah, the Old Testament word for the Spirit of God. It speaks in a feminine voice and tends to express statements about the messianic expectation.',
    },
    {
        'id': 'BIB-INT-04', 'source': 'DOC_ARCH_PHILIP_K_DICK_IN_HIS_OWN_WORDS_GREGG_RIC', 'field': 'markdown_content',
        'anchor': 'I studied the Torah until I understood',
        'pith': 'I studied the Torah until I understood',
        'group': 'interviews', 'lane': 'A', 'register': 'A', 'relevance': 1,
        'citation': 'Philip K. Dick: In His Own Words (Gregg Rickman, 1984), undated conversation',
        'dated': None, 'dating_basis': 'Undated in the record; the book was published in 1984.',
        'concepts': ['Torah', 'themes of the Torah', 'Christianity', 'Judaism'],
        'speaker': 'Philip K. Dick',
        'context': 'Dick says that for several years he worked on a book about Judaism, and that he studied the Torah with the notes of the late Chief Rabbi until he understood its underlying themes. He says he snuck some Christianity into the book, and finally got back to Christianity.',
    },
    {
        'id': 'BIB-INT-05', 'source': 'DOC_ARCH_OCEANOFPDF_COM_THE_LAST_INTERVIEW_AND_OT', 'field': 'markdown_content',
        'anchor': 'John the Baptist was Elijah',
        'pith': 'John the Baptist was Elijah. That’s who he was. He was Elijah.',
        'group': 'interviews', 'lane': 'A', 'register': 'A', 'relevance': 1,
        'citation': 'The Last Interview and Other Conversations (2015), conversation with Rickman, undated',
        'dated': None, 'dating_basis': 'The compilation spans 1955–1982; this conversation is not dated in the record.',
        'concepts': ['John the Baptist', 'Elijah', 'Malachi', 'Jesus'],
        'speaker': 'Philip K. Dick',
        'context': 'Pressed on who John the Baptist was, Dick answers from scripture: “Don’t you remember your scripture?” He quotes the prophecy in Malachi that Elijah will be sent back, and says that Jesus identified John the Baptist as Elijah. It is the Elijah of the 1976 Exegesis, whose return Malachi gave Dick his timetable for.',
    },
    {
        'id': 'BIB-INT-06', 'source': 'DOC_ARCH_OCEANOFPDF_COM_THE_LAST_INTERVIEW_AND_OT', 'field': 'markdown_content',
        'anchor': 'I started reading the Bible',
        'pith': 'I started reading the Bible and I read that part about Elijah.',
        'group': 'interviews', 'lane': 'A', 'register': 'A', 'relevance': 1,
        'citation': 'The Last Interview and Other Conversations (2015), conversation with Rickman, undated',
        'dated': None, 'dating_basis': 'The compilation spans 1955–1982; this conversation is not dated in the record.',
        'concepts': ['Elijah', 'boyhood reading', 'radio serial', 'The Light of the World'],
        'speaker': 'Philip K. Dick',
        'context': 'Dick recalls that in junior high school a daytime radio serial, The Light of the World, dramatised part of the Bible. He began listening during the part about Elijah, then read the Bible himself, and the Elijah passage was his greatest wish in the world.',
    },
    {
        'id': 'BIB-INT-07', 'source': 'DOC_ARCH_PHILIP_K_DICK_IN_HIS_OWN_WORDS_GREGG_RIC', 'field': 'markdown_content',
        'anchor': 'switched from Christianity to Judaism',
        'pith': 'I’ve switched from Christianity to Judaism.',
        'group': 'interviews', 'lane': 'A', 'register': 'A', 'relevance': 1,
        'citation': 'Philip K. Dick: In His Own Words (Gregg Rickman, 1984), undated conversation',
        'dated': None, 'dating_basis': 'Undated in the record; the book was published in 1984.',
        'concepts': ['Judaism', 'Yahweh', 'Christianity'],
        'speaker': 'Philip K. Dick',
        'context': 'Dick says he has switched from Christianity to Judaism, and that Christianity is renounced and denounced in the book. God in it is specifically Yahweh, as in the Old Testament, though he began to put in funny stuff, and it got away from him.',
    },
    {
        'id': 'BIB-INT-08', 'source': 'DOC_ARCH_THE_MISSOURI_REVIEW_VOL_7_ISS_2_THE_MAIN', 'field': 'markdown_content',
        'anchor': "A Scanner Darkly is from Paul's",
        'pith': "No, A Scanner Darkly is from Paul's 'through a glass, darkly.'",
        'group': 'interviews', 'lane': 'A', 'register': 'A', 'relevance': 2,
        'citation': 'The Mainstream That Through the Ghetto Flows: An Interview with Philip K. Dick (The Missouri Review, 1984)',
        'dated': None, 'dating_basis': 'The interview is dated 1984 in the record; this passage is not dated separately.',
        'concepts': ['A Scanner Darkly', 'Paul', '1 Corinthians 13:12', 'title'],
        'speaker': 'Philip K. Dick',
        'context': 'Asked about the title of A Scanner Darkly, Dick says it is from Paul’s “through a glass, darkly,” which is the King James wording of 1 Corinthians 13:12. It is an allusion in a title, not an argument about scripture.',
    },
    # ---- Short stories, full text (lane A here is fiction: characters, not Dick) --
    {
        'id': 'BIB-STO-01', 'source': 'DOC_ARCH_OCEANOFPDF_COM_THE_COLLECTED_STORIES_OF_', 'field': 'markdown_content',
        'anchor': 'You know, like in the Bible',
        'pith': "Hoppy, what's the light from? Is it God? You know, like in the Bible.",
        'group': 'stories', 'lane': 'A', 'register': 'A', 'relevance': 2,
        'citation': '“A Terran Odyssey”, in The Collected Stories of Philip K. Dick (Underwood-Miller, 1987)',
        'dated': None, 'dating_basis': 'The story’s first publication is given in the volume’s notes, not in this record.',
        'concepts': ['light', 'God', 'the Bible'],
        'speaker': 'Character (fiction)',
        'context': 'A character asks Hoppy what the light is, and whether it is God, “like in the Bible.” The question is a character’s, in fiction, and is not Dick’s own claim. It is one instance of the stories’ habit of reaching for scripture when something strange happens.',
    },
    {
        'id': 'BIB-STO-02', 'source': 'DOC_ARCH_OCEANOFPDF_COM_THE_COLLECTED_STORIES_OF_', 'field': 'markdown_content',
        'anchor': 'to bind a copy of the Bible in wub-fur',
        'pith': 'to bind a copy of the Bible in wub-fur.',
        'group': 'stories', 'lane': 'A', 'register': 'A', 'relevance': 2,
        'citation': '“Not by Its Cover”, in The Collected Stories of Philip K. Dick (Underwood-Miller, 1987)',
        'dated': None, 'dating_basis': 'The story’s first publication is given in the volume’s notes, not in this record.',
        'concepts': ['Bible as object', 'Corinthians', 'wub-fur'],
        'speaker': 'Character (fiction)',
        'context': 'One character suggests binding a copy of the Bible in wub-fur. Another says he had it done, and read Paul’s letters to the Corinthians in the bound copy, and found a single change, to the passage on the mystery. The joke is about the book as an object in the story’s world of commodities.',
    },
    {
        'id': 'BIB-STO-03', 'source': 'DOC_ARCH_OCEANOFPDF_COM_THE_COLLECTED_STORIES_OF_', 'field': 'markdown_content',
        'anchor': 'Even holy, like the Bible',
        'pith': 'Huge books, very valuable. Even holy, like the Bible.',
        'group': 'stories', 'lane': 'A', 'register': 'A', 'relevance': 2,
        'citation': '“The Eye of the Sibyl”, in The Collected Stories of Philip K. Dick (Underwood-Miller, 1987)',
        'dated': None, 'dating_basis': 'The story’s first publication is given in the volume’s notes, not in this record.',
        'concepts': ['dream', 'books', 'holy books', 'warning'],
        'speaker': 'Character (fiction)',
        'context': 'The narrator dreams of open books held up before him, huge and valuable, “even holy, like the Bible.” Ms. Heims reads the dream as a matter for his career as a writer, and the narrator says the books are old, thousands of years old, and warning them about something.',
    },
    {
        'id': 'BIB-STO-04', 'source': 'DOC_ARCH_OCEANOFPDF_COM_THE_COLLECTED_STORIES_OF_', 'field': 'markdown_content',
        'anchor': 'Look it up in the Bible',
        'pith': "Look it up in the Bible if you don't believe me.",
        'group': 'stories', 'lane': 'A', 'register': 'A', 'relevance': 2,
        'citation': '“Retreat Syndrome”, in The Collected Stories of Philip K. Dick (Underwood-Miller, 1987)',
        'dated': None, 'dating_basis': 'The story’s first publication is given in the volume’s notes, not in this record.',
        'concepts': ['punishment', 'authority', 'scripture'],
        'speaker': 'Character (fiction)',
        'context': 'Hagopian tells a colleague to leave Carol alone, since it is not his job to exact vengeance, and that she is being punished and will be as long as she is in their hands. The scripture is offered as settled authority, and the scene is an argument about who may enforce it.',
    },
    {
        'id': 'BIB-STO-05', 'source': 'DOC_ARCH_OCEANOFPDF_COM_THE_COLLECTED_STORIES_OF_', 'field': 'markdown_content',
        'anchor': 'as the Bible says',
        'pith': 'We all go to one place, he thought, as the Bible says.',
        'group': 'stories', 'lane': 'A', 'register': 'A', 'relevance': 2,
        'citation': '“A Little Something for Us Tempunauts”, in The Collected Stories of Philip K. Dick (Underwood-Miller, 1987)',
        'dated': None, 'dating_basis': 'The story’s first publication is given in the volume’s notes, not in this record.',
        'concepts': ['death', 'Ecclesiastes', 'the three of us'],
        'speaker': 'Character (fiction)',
        'context': 'A character who, with two others, has already been where the rest of the people are going, thinks that they all go to one place, as the Bible says. The line is resignation, put in the mouth of a man who feels himself already among the dead.',
    },

]

# ---------------------------------------------------------------------------
# The essay. Sections are rendered in order. Citations are {{CARD-ID}}.
# Register letters follow REGISTER_LABELS in TopicDetail.tsx.
# ---------------------------------------------------------------------------
DOSSIER_SECTIONS = [
    {
        'id': 'note', 'heading': 'The Bible in Philip K. Dick', 'register': 'D',
        'body': [
            "For the last years of his life Philip K. Dick argued that the Bible is not a "
            "record of the past but a text about the present, and that he was living inside "
            "it. This study follows that argument through the sources the repository holds, "
            "and keeps each source in its own register.",
            "The strongest evidence is still the Exegesis, Dick’s own notebooks, transcribed "
            "here as 1,104 segments. A sweep of their raw text finds Bible vocabulary in 383 of "
            "them: the Bible, Scripture, the Testaments, the Gospels, the Torah, and named books "
            "and verses. The archive also holds the full text of 1,175 letters from the Selected "
            "Letters volumes, of the short stories, of the VALIS chapters and other novels, and "
            "of five interview transcripts. Dick’s letters, speech and fiction are cited in lane "
            "A, and fiction is marked as fiction. The novel and story summaries, the Exegesis "
            "analysis and the scholarship are editorial or secondary, and are labelled where they "
            "are used.",
            "Two limits remain. The 1974 Vertex interview is not held as text. And the sweep "
            "matches words: a passage that alludes to scripture without naming it will not be "
            "found, so an absence here is an absence of the word.",
        ],
    },
    {
        'id': 'y1964', 'heading': '1964: a priest’s reading', 'register': 'A',
        'body': [
            "The earliest Bible passage in the letters is from May 1964, when Dick wrote to "
            "James Blish about his priest and about God’s absence. “My priest says the Bible is "
            "not the story of man's search for God but of God's search for man.” "
            "{{BIB-LET-64-01}} Dick sets the line against his own inability to see the Redeemer, "
            "and asks where He has gone. It reads the Bible from God’s side.",
        ],
    },
    {
        'id': 'y1972', 'heading': '1972: the Bible in rhymed couplets', 'register': 'A',
        'body': [
            "In 1972 the Bible first becomes a project, and it begins as a joke. On 1 December "
            "Dick wrote to Roger Zelazny about a dream in which he was given an award, and "
            "learned that the award was for this: “I had set the Bible into rhymed couplets.” "
            "{{BIB-LET-72-01}}",
            "He gave a sample: “In the beginning God separated the water from the land, And "
            "exclaimed, ‘My, isn’t that grand.’” He preferred Luther’s rendering of the line "
            "“And God saw that it good was.” The letter treats the Bible first as language, "
            "something to be translated, parodied and preferred.",
        ],
    },
    {
        'id': 'y1973', 'heading': '1973: the project under way', 'register': 'A',
        'body': [
            "By January 1973 the joke has become a method. Dick calls the work the project "
            "“nearest and dearest to my heart”, and reports that it is “coming along fine, with "
            "the first one already firmly jelled and on paper.” {{BIB-LET-73-01}}",
        ],
    },
    {
        'id': 'y1975', 'heading': '1975: the Bible as a book of the future', 'register': 'A',
        'body': [
            "In the February 1975 transcriptions the Bible is a prophetic text, and Dick "
            "states its time plainly: “The Bible is a book of the future.” {{BIB-EX-75-01}} "
            "The Old Testament gets less from him. “All the O.T. has in it is monotheism, "
            "which they got from Iknaton.” {{BIB-EX-75-02}}",
            "By November the Bible has stopped being a source and become a condition of "
            "perception. “The world of the Bible was suddenly around me, and real, replacing "
            "our world.” {{BIB-EX-75-03}} The sentence that follows it gives the principle: "
            "“The book the Bible is an analog of reality.” {{BIB-EX-75-04}}",
            "His working reference is the Jerusalem Bible, which he calls the “J. Bible”, "
            "and whose notes give him Rome as “the great and only real enemy of the new "
            "chosen people, the Church.” {{BIB-EX-75-05}}",
            "The letters of the same year make the cypher claim in plain terms. To Robert "
            "Ornstein, in March, Dick writes that a character who studies the Bible with a "
            "Qumran figure “finds that the New Testament is in cypher.” {{BIB-LET-75-01}} In July, "
            "to Göran Bengtson, he describes the moment at which, in his account, “this is indeed "
            "the moment foretold in the Bible”, and the Parousia has arrived, though not in the "
            "form anyone had expected. {{BIB-LET-75-02}}",
        ],
    },
    {
        'id': 'l1976', 'heading': 'September 1976: the letters on the same ground', 'register': 'A',
        'body': [
            "Nine days before the sitting on Acts in Tears, Dick tells Dorothy Hudner that “the "
            "prophecies of the Bible are all true and are systematically being fulfilled.” "
            "{{BIB-LET-76-01}} The evil spirit is in Rome, which is “the Prince of This World”, "
            "and the Parousia is not far off.",
        ],
    },
    {
        'id': 'y1976', 'heading': 'September 1976: Acts in Tears', 'register': 'A',
        'body': [
            "The sitting of 15 September 1976 is the longest Bible argument in the Exegesis, "
            "and its first claim is that Flow My Tears, the Policeman Said, which the notebooks "
            "call “Tears”, contains “unmistakable material from Acts.” {{BIB-EX-76-01}} Acts, "
            "in his account, is the book of the early church, and it describes the period "
            "just after Christ leaves.",
            "The claim comes with a difficulty that Dick records himself. Father Rasch "
            "pointed out the scene of Philip and the black man to him, “my first clue "
            "to biblical material in the book”, and Dick says he “had never read Acts”. "
            "{{BIB-EX-76-02}} He then asks how he could have identified the Acts elements the "
            "month the novel came out, if he had not recognised them when he wrote it. "
            "{{BIB-EX-76-03}}",
            "The answer he reaches is that the world the novel describes is the world of Acts. "
            "“The true world is that of Acts. Why Acts? The last period of the scriptures, the "
            "time of the paraclete.” {{BIB-EX-76-04}} The same sitting calls Ubik a form of "
            "scripture, because the novel was, in his account, written by its own title. "
            "{{BIB-EX-76-05}}",
        ],
    },
    {
        'id': 'y1976b', 'heading': '15 September 1976: the Bible as code', 'register': 'A',
        'body': [
            "The sitting also makes the claim that organises the rest of his Bible writing. "
            "“In the Bible isn’t about the past; it’s code to describe our world (as is "
            "‘Tears’).” {{BIB-EX-76-06}} The prophecy of Malachi gives him the timetable. "
            "“The ending of Malachi makes it absolutely clear that God (1) foresaw the "
            "ABSENCE of Elijah from the world”, and the return of Elijah is therefore part "
            "of a plan. {{BIB-EX-76-07}}",
        ],
    },
    {
        'id': 'l1977', 'heading': '1977: a conversion, and its reading', 'register': 'A',
        'body': [
            "Dick dates his conversion experience to March 1974. Writing to Eugene Warren in "
            "August 1977, he says that since then he has read the Bible, the New Testament "
            "particularly, “again and again.” {{BIB-LET-77-01}} The letter says that two parts of "
            "what was revealed to him seemed the most striking, and one of them is the Jerusalem "
            "Bible’s note on Ephesians 1:10.",
        ],
    },
    {
        'id': 'y1978', 'heading': '1978: the living Torah', 'register': 'A',
        'body': [
            "The folder dated 10 October 1978 is a batch date. Its entries refer to late 1980, "
            "so the folder is a sitting, not a day, and the argument in it develops across "
            "the years that follow. The Torah takes the place Acts held in 1976. “I am sure "
            "that the plasmate – & hence the cypher in ‘Tears’ – is the Living Torah, the "
            "informational basis of reality.” {{BIB-EX-78-01}}",
            "The Torah is not, in this account, simply the Jewish law. It is the source that "
            "Christ corrects. “Jesus was the greatest of the Hebrew prophets, yet he was "
            "rejected by Israel. Why? Because he depreciated the Torah.” {{BIB-EX-78-02}} The "
            "cost to Dick’s own faith is stated in the same folder: “herewith I just lost my "
            "Trinitarianism!” {{BIB-EX-78-03}}",
            "The programme is also stated. The third age has its own Torah, and “New "
            "Scriptures are needed, new prophets and perhaps a new savior.” {{BIB-EX-78-04}}",
        ],
    },
    {
        'id': 'y1978b', 'heading': '1978: the Bible as code, and in three dimensions', 'register': 'A',
        'body': [
            "What the Torah does for the cypher, VALIS does for the book. Dick proposes that "
            "the world of 1970–74 was built on information contained in the Bible, and "
            "“that Valis turned that info into our world.” {{BIB-EX-78-05}} The Bible then "
            "becomes an instrument as well as a source: “using the Bible as a encoding-decoding "
            "grid.” {{BIB-EX-78-06}}",
            "The image he uses for it is spatial. “My visualizing the Bible in 3-D: layers "
            "according to age (time as spacial axis)” {{BIB-EX-78-07}} is the picture the "
            "trilogy later puts on the screen of Elias’s holoscope. See the Divine Invasion "
            "section below.",
        ],
    },
    {
        'id': 'l1980', 'heading': '1980–1981: the Torah as Wisdom, and the Bible as information', 'register': 'A',
        'body': [
            "In February 1980 Dick tells Jonathan Silverman that he has discovered “that the Torah "
            "can be equated with Holy Wisdom (Hagia Sophia) of Proverbs 8.” {{BIB-LET-80-01}} The "
            "Torah he read with the notes of Hertz has become the Wisdom that existed before creation.",
            "The 1981 letters give the Exegesis’s terms to correspondents. In July, to Patricia "
            "Warrick: “We have what I call recombinant information/scripture.” {{BIB-LET-81-01}} "
            "In August he sends her the fullest account: “The Bible is the information that is fed "
            "into the space-time universe, as if transduced into substantial reality.” "
            "{{BIB-LET-81-02}} A single coherent life form, he says, underlies the written Bible, "
            "and is “not fixed into a canon.” {{BIB-LET-81-03}}",
            "Two letters of 1981 turn the same material on fiction and on ethics. To Russell Galen, "
            "in June, Dick says that Tim Archer “completely misuses the Bible”, and uses it “not as "
            "a man of God but as a lawyer.” {{BIB-LET-81-04}} To Ursula Le Guin, in August, he writes "
            "that the Torah “has enchanted me with its haunting concern for all creatures, especially "
            "the weak, the harmless and the disadvantaged.” {{BIB-LET-81-05}}",
        ],
    },
    {
        'id': 'y1981', 'heading': 'April 1981: the Bible is the real world', 'register': 'A',
        'body': [
            "By April 1981 the claim has reversed. The Bible is no longer a description of "
            "the world, but the world: “the Bible is not a verbal description of a world; it is "
            "a world.” {{BIB-EX-81-01}}",
            "The boy who read it is part of the argument. Dick says that when he was in "
            "junior high school and first read the Bible, “it was the O.T. that I read, not "
            "the N.T., esp. the part about Elijah.” {{BIB-EX-81-02}} The test he sets for any "
            "account of reality is a Bible test: “the touchstone (oh please do not forget "
            "this!) is the Bible.” {{BIB-EX-81-03}}",
            "The working example is Acts again, now read against Luke. The “infinity” mode "
            "of 1974 was “the world of the Bible, specifically Acts – the 2nd half of Luke.” "
            "{{BIB-EX-81-04}} The image that carries the claim is Augustine’s. “Augustine "
            "called the Bible ‘Letters from home’.” {{BIB-EX-81-05}}",
        ],
    },
    {
        'id': 'y1981b', 'heading': 'April 1981: recombinant scripture and a third testament', 'register': 'A',
        'body': [
            "A closed canon is no longer possible on this account. Dick’s term for its "
            "replacement is “recombinant scripture”, which has “no canon, no precedent; each "
            "person + situation unique.” {{BIB-EX-81-06}}",
            "He calls the revelation he is living a third testament: an “unprecedented third "
            "testament emanating out of the O.T. + N.T.” {{BIB-EX-81-07}} The hierarchy is "
            "stated in the same transcription: “Torah does not know everything. Christ does.” "
            "{{BIB-EX-81-08}} The law is the frame of the world, and Christ is the one who acts "
            "within it. That is the argument of the 1978 passages, put in its final form.",
        ],
    },
    {
        'id': 'interviews', 'heading': 'The interviews: what Dick said about scripture', 'register': 'A',
        'body': [
            "Five interview transcripts are now held as text, and they change the record of what "
            "Dick said in public. In one conversation, printed in The Last Interview, he recalls "
            "his boyhood: “I started reading the Bible and I read that part about Elijah.” "
            "{{BIB-INT-06}} The same reading is in the Exegesis of April 1981, which records that it "
            "was “the O.T. that I read, not the N.T., esp. the part about Elijah.” {{BIB-EX-81-02}} In "
            "the same conversation the interviewer asks who John the Baptist was, and Dick answers "
            "from Malachi: “John the Baptist was Elijah.” {{BIB-INT-05}}",
            "In His Own Words, Gregg Rickman’s book of 1984, has the most developed account. Dick says "
            "he studied the Torah until he understood its underlying themes, and that he has "
            "“switched from Christianity to Judaism.” {{BIB-INT-04}} {{BIB-INT-07}} In the compiled "
            "magazine interviews the same study is given to a novel: the resolution, he says, is "
            "“in terms of Judaism”, and he made “a very detailed study of the Torah and the basic "
            "tenets of Judaism for it.” {{BIB-INT-01}}",
            "The compiled magazine interviews also have Dick reading Deuteronomy with the notes of "
            "Rabbi Hertz: “I was reading Deuteronomy last night.” {{BIB-INT-02}} The voice that "
            "guided him he names as Ruah, “the Old Testament word for the Spirit of God.” "
            "{{BIB-INT-03}}",
            "The Missouri Review interview of 1984 is held in full. Its few Bible hits are mostly names, "
            "but Dick says the title A Scanner Darkly comes from Paul’s “through a glass, darkly.” "
            "{{BIB-INT-08}} The 1974 Vertex interview is not held at all, so what Dick said there "
            "about scripture cannot be checked.",
        ],
    },
    {
        'id': 'fiction', 'heading': 'What the trilogy does with the Bible', 'register': 'A',
        'body': [
            "In VALIS the Bible is a problem that characters argue over. Sherri, the sceptic, "
            "asks whether a passage Fat has quoted is “one of the corrupt parts of the Bible”. "
            "{{BIB-TR-VAL-01}} Kevin, who becomes a convert, reads Daniel for Nixon: “Now Kevin "
            "had become a Bible scholar, to Fat’s amusement.” {{BIB-TR-VAL-02}} Fat traces Psalm "
            "104 to Akhenaten’s hymn, and says the hymn “entered our Bible—it’s older than our "
            "Bible.” {{BIB-TR-VAL-03}}",
            "The Divine Invasion takes the Exegesis’s three-dimensional Bible and gives it a "
            "scene. Elias’s holoscope lays out “the Bible expressed as layers at different "
            "depths within the hologram, each layer according to age.” {{BIB-TR-DI-01}} Scripture "
            "in the hologram “became a sentient organism that was never twice the same.” "
            "{{BIB-TR-DI-02}} The Torah is the same living thing the notebooks describe: “Torah "
            "is the totality of divine disclosure by God; it is alive; it existed before "
            "creation.” {{BIB-TR-DI-03}}",
            "The novel gives the Torah a body. Zina Pallas says: “I am the Torah.” "
            "{{BIB-TR-DI-04}} Emmanuel, the boy at the centre of the novel, wants to add a line of "
            "his own to the Bible’s hologram, and does not: “He wanted to feed that into the "
            "hologram of the Bible, as an addendum, but he knew that he should not.” "
            "{{BIB-TR-DI-05}} In the notebooks Dick is sure of his right to add to scripture. "
            "In the novel the right is withheld.",
        ],
    },
    {
        'id': 'stories', 'heading': 'The stories, as full text', 'register': 'A',
        'body': [
            "The short stories are now held as full text, and the Bible is in them, mostly in "
            "passing. The stories give scripture to characters, as a phrase they reach for. In “A "
            "Terran Odyssey” a character asks of a strange light, “Is it God? You know, like in the "
            "Bible.” {{BIB-STO-01}} In “The Eye of the Sibyl” a dream of open books is “even holy, "
            "like the Bible.” {{BIB-STO-03}} In “A Little Something for Us Tempunauts” a character "
            "who has already been where the others are going thinks: “We all go to one place, he "
            "thought, as the Bible says.” {{BIB-STO-05}}",
            "In “Not by Its Cover” a character suggests binding a copy of the Bible in wub-fur, and "
            "another says he had it done and read Paul’s letters to the Corinthians in it. "
            "{{BIB-STO-02}} In “Retreat Syndrome” one man tells another to leave Carol alone: “Look it "
            "up in the Bible if you don't believe me.” {{BIB-STO-04}} These are the characters’ "
            "words, read in lane A as fiction. None of them is Dick’s own argument.",
        ],
    },
    {
        'id': 'summaries', 'heading': 'The other novels, as summarised', 'register': 'D',
        'body': [
            "The novel summaries follow the same pattern. The Bible appears in the summaries of "
            "The Divine Invasion and VALIS, and in The Transmigration of Timothy Archer, where a "
            "character quotes scripture. The summary of Ubik records a biblical tradition of "
            "dreams. The summaries of Do Androids Dream of Electric Sheep?, The Man in the High "
            "Castle and A Maze of Death record no biblical reference. These are summaries of "
            "summaries, useful for orientation and not evidence in their own right.",
            "Some novels are also held as full text, and the sweep finds Bible references in that "
            "text. This study has not yet carded them.",
        ],
    },
    {
        'id': 'scholarship', 'heading': 'What the scholarship says', 'register': 'C',
        'body': [
            "Scholars have reached the Bible in Dick’s work mainly through its Gnostic and "
            "Pauline edges. Davis follows the Hymn of the Pearl, which is “embedded in the "
            "third-century Acts of Thomas”, through Dick’s engagement with it from 1975. "
            "{{BIB-SCH-01}} The Acts there are apocryphal, and the canonical Acts of the 1976 "
            "sitting are a different book.",
            "Burton reads Dick’s fiction against Bergson and against “the theology of Saint "
            "Paul”. {{BIB-SCH-02}} The archive’s record of the VALIS appendix names “Paul of "
            "Tarsus, Simon Magus” among those said to have known a great secret. {{BIB-SCH-03}} "
            "The scholarship is also held as full text, and the sweep finds biblical references "
            "in it. This study has carded only the records that bear on Dick’s own words, so the "
            "scholarship is thin here, and a full reading of it is still to do.",
        ],
    },
    {
        'id': 'synthesis', 'heading': 'What the Bible meant to Dick', 'register': 'D',
        'body': [
            "Three things were true of the Bible for Dick, and the archive supports each of them. "
            "It was a text he read closely, in translation and with commentary, from the "
            "Jerusalem Bible notes to the “Decoded New Testament” he was rereading in 1975. It "
            "was a rival authority: Acts is the true world, Christ corrects the Torah, and in "
            "1981 the Torah “does not know everything”. And it was a model for his own writing: "
            "Tears is read as Acts, Ubik as scripture, and the trilogy as a third testament.",
            "What did not settle is whether the Bible describes the past or the present. In 1976 "
            "it is “not about the past”. In 1978 the Torah is the timeless source of the "
            "informational world. In 1981 the Bible is “the real world”, and Dick’s own novels "
            "belong to a new testament. The contradictions run through the whole sequence, and "
            "this essay does not resolve them.",
            "The lanes differ in voice. The trilogy and the stories give the Bible to characters "
            "who argue about it: Sherri, Kevin, Emmanuel, who holds back, and the men in the "
            "stories who reach for a line. The Exegesis gives it to one reader who is sure of his "
            "reading. The letters give it to correspondents, in the voice of a friend: in 1981 "
            "Dick explains the Bible to Patricia Warrick as information, a life form and a canon "
            "that has gone. That difference of voice is the clearest thing the lanes show side by side.",
        ],
    },
]

TOPIC = {
    'topic_id': 'TOPIC_BIBLE_bible_in_pkd',
    'canonical_name': 'The Bible in Philip K. Dick',
    'slug': 'bible-in-pkd',
    'status': 'reviewed',
    'priority': 10,
    'card_description': (
        "Dick’s Bible as text, code and world, from a 1964 letter and a 1972 joke about rhymed "
        "couplets to the April 1981 claim that the Bible is the real world — across the Exegesis, "
        "the letters, the interviews, the stories and the VALIS trilogy, with what the archive "
        "cannot yet show."
    ),
    'definition': (
        "Scripture as Dick read it: the books he quoted, the translations and glosses he used, "
        "and the readings he made. From 1975 he treated the Bible as a book of the future; by "
        "1976 as code for the present; by 1981 as the world itself, and his own novels as a "
        "third testament."
    ),
    'pkd_relevance': (
        "The Bible is the text Dick returned to for his whole life, and in the Exegesis it "
        "becomes the frame for his theory of reality. The shift from text to world is the "
        "main movement in his late thought, and the trilogy shows it as a scene."
    ),
    'in_the_fiction': (
        "VALIS and The Divine Invasion hold the Bible as characters’ argument and as a hologram. "
        "The Divine Invasion gives the Torah a speaker, Zina Pallas. The short stories hold it in "
        "passing: as a question a character asks, as a dream image, and as a phrase a man reaches "
        "for when he has been where others have not come back."
    ),
    'in_the_exegesis': (
        "The sweep finds Bible vocabulary in 383 of the 1,104 transcribed segments. The argument "
        "runs through the 1975 batch, the 15 September 1976 sitting on Acts in Tears, the 1978 "
        "folder on the living Torah and the Bible in three dimensions, and the April 1981 "
        "transcriptions on recombinant scripture and the third testament."
    ),
    'intellectual_background': (
        "Dick’s reference works are named in the transcriptions: the Jerusalem Bible and its "
        "notes, a “Decoded New Testament”, and Augustine’s image of the Bible as letters from "
        "home. In the letters he reads the Torah with the notes of J. H. Hertz. The Hymn of the "
        "Pearl, in the apocryphal Acts of Thomas, is the one Gnostic text the scholarship traces "
        "through him."
    ),
    'scholarly_debate': (
        "Scholars reach the Bible in Dick through its Gnostic and Pauline edges. The debate is "
        "whether his use of scripture is theology or a literary device; the Exegesis argues the "
        "first, and the trilogy often stages the second."
    ),
    'chronology_summary': (
        "1964: a priest’s reading in a letter. 1972: the Bible in rhymed couplets, begun as a joke. "
        "1975: the Bible as a book of the future, and as cypher. September 1976: Acts in Tears, and "
        "the Bible as code for the present. 1978: the living Torah and the Bible in three dimensions. "
        "1980–81: the Torah as Holy Wisdom, recombinant scripture, and the Bible as information. "
        "April 1981: the Bible as the real world, and a third testament."
    ),
    'contradictions_summary': (
        "Dick never settles whether the Bible is a record of the past or a description of the "
        "present. In 1976 it is “not about the past”; in 1978 the Torah is timeless; in 1981 the "
        "Bible is “the real world”."
    ),
    'related_thinkers': ['Paul of Tarsus', 'Elijah', 'Akhenaten', 'Spinoza', 'Philo of '
                         'Alexandria', 'Augustine', 'Martin Luther', 'Joachim of Fiore',
                         'J. H. Hertz'],
    'editorial_notes': (
        "Hand-authored editorial prose. The sweep is the corpus; the cards are the passages chosen "
        "from it; the prose cites cards and quotes only what the corpus contains. The letters are "
        "the full text of the Selected Letters volumes, except the 1972 letter, which is quoted from "
        "the excerpt file. The interviews are transcripts, and their cards quote Dick’s own speech. "
        "The stories are full text, and their cards quote characters, which is lane A as fiction. "
        "The scholarship and the archive PDFs are searched but not yet carded. Folder dates are "
        "batch dates."
    ),
    'open_questions': [
        "What did Dick say about the Bible at the 1974 Vertex interview? Resolvable by: a transcript. "
        "None is held as text.",
        "Which Bible did he use? The transcriptions name the Jerusalem Bible and a “Decoded New "
        "Testament”, but not an edition of the first or the source of the second. Resolvable by: an "
        "inventory of his library, if one survives.",
        "Did Dick know the Acts material in Tears before 1974? He says he recognised it only after the "
        "novel appeared. Resolvable by: the manuscript or typescript of Flow My Tears, the Policeman Said.",
        "What do the letters of 1982 say about scripture? They are held in full, and no card from that "
        "year has been chosen yet.",
        "What do the scholarship and the archive PDFs add? Resolvable by: reading the lane C hits in the "
        "sweep, and deciding the lane of the published Exegesis, which the database records as B.",
    ],
    'related_topics': [
        {'topic_id': 'TOPIC_GNOS_gnosis_and_anamnesis', 'canonical_name': 'Gnosis and Anamnesis',
         'slug': 'gnosis-and-anamnesis', 'study_id': 'gnosticism'},
        {'topic_id': 'TOPIC_GNOS_valis_trilogy', 'canonical_name': 'Gnosticism in the VALIS Trilogy',
         'slug': 'valis-trilogy', 'study_id': 'gnosticism'},
    ],
}
