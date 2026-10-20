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
    "Philip K. Dick's engagement with the Bible across the Exegesis, the 1972–73 "
    "letters, the VALIS trilogy and the short fiction: the books he quoted, the "
    "translations and glosses he used, the readings he made of them, and the claim "
    "that developed across 1975–81 that the Bible is not a record of the past but a "
    "living text describing, and in some sense being, the present world."
)

STUDY_SECTIONS = [
    {
        'title': 'What this study claims',
        'body': [
            "Philip K. Dick read the Bible from his schooldays, by his own account in 1981. "
            "In the 1970s he began to read it as a text about "
            "his own time, and then, in the notebooks known as the Exegesis, as a text that "
            "was the world he was living in. This study follows that change through the "
            "sources the repository holds, and keeps each source in its own register.",
            "The main evidence is the Exegesis: Dick's own words in 1,104 transcribed "
            "segments, of which 383 use Bible vocabulary at least once. The VALIS chapters "
            "1 and 5–13 and the first five chapters of The Divine Invasion are held as full "
            "text, and carry the same argument into fiction. Everything else is either editorial summary or secondary "
            "scholarship, and is labelled as such.",
        ],
    },
    {
        'title': 'What the archive cannot yet show',
        'body': [
            "The interviews are the largest gap. The repository holds five interview "
            "records as catalogue entries and summaries, and none of them mentions the "
            "Bible. This study therefore says nothing about what Dick told interviewers "
            "about scripture, and the absence should not be read as a finding about him.",
            "The letters are a second limit. Only 75 letters from 1972–73 are held, each "
            "capped at about 1,500 characters, and a few have their body stored in the "
            "wrong field. A letter search is a floor, not a census.",
        ],
    },
]

GROUPS = [
    {'key': 'letters-1972', 'label': 'Letters, 1972',
     'blurb': 'The Selected Letters held here are excerpts. Where the sweep found a '
              'Bible reference, the excerpt is quoted as it stands.'},
    {'key': 'exeg-1975', 'label': 'The Exegesis — February and November 1975',
     'blurb': 'Transcriptions dated by batch. Each segment inherits its batch date.'},
    {'key': 'exeg-1976', 'label': 'The Exegesis — 15 September 1976',
     'blurb': 'The longest single sitting on the Bible, and the one in which the '
              'claim about Acts in Tears is first made.'},
    {'key': 'exeg-1978', 'label': 'The Exegesis — 10 October 1978 (folder)',
     'blurb': 'A batch date, not a sitting date. Entries inside it refer to late 1980.'},
    {'key': 'exeg-1981', 'label': 'The Exegesis — 16 April 1981',
     'blurb': 'The last sustained theory of the Bible in the transcriptions.'},
    {'key': 'fiction', 'label': 'The trilogy, as held here as full text',
     'blurb': 'VALIS and The Divine Invasion, chapters held as full text. Lane A: '
              'Dick’s own words in fiction.'},
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
                   'Luther’s rendering of the line “And God saw that it good was.” This is the earliest Bible '
                   'passage the sweep finds.',
        'editorial_note': 'The letter is held as a 1,500-character excerpt, and its body '
                          'sits in the recipient field. Read the excerpt, not the summary.',
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
            "The strongest evidence is the Exegesis, Dick’s own notebooks, transcribed here "
            "as 1,104 segments. A sweep of their raw text finds Bible vocabulary in 383 of "
            "them: the Bible, Scripture, the Testaments, the Gospels, the Torah, and named "
            "books and verses. The VALIS chapters 1 and 5–13 and the first five chapters of "
            "The Divine Invasion are held as full text, and carry the same argument into fiction. The 1972–73 letters are held as "
            "excerpts. The story and novel summaries, the Exegesis analysis and the "
            "scholarship are editorial or secondary, and are labelled as they are used.",
            "Two limits belong at the top. The interviews hold no Bible content in the "
            "archive, so this essay cannot say what Dick told interviewers about scripture. "
            "And the letter excerpts make a search for Bible references a floor, not a "
            "census of what he wrote.",
        ],
    },
    {
        'id': 'y1972', 'heading': '1972: the Bible in rhymed couplets', 'register': 'A',
        'body': [
            "The earliest Bible passage the sweep finds is a joke. On 1 December 1972 Dick "
            "wrote to Roger Zelazny about a dream in which he was given an award, and "
            "and learned that the award was for this: “I had set the Bible into rhymed couplets.” "
            "{{BIB-LET-72-01}}",
            "He gave a sample: “In the beginning God separated the water from the land, And "
            "exclaimed, ‘My, isn’t that grand.’” He preferred Luther’s rendering of the line "
            "“And God saw that it good was.” The letter treats the Bible first as language, "
            "something to be translated, parodied and preferred.",
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
        'id': 'interviews', 'heading': 'The interviews: nothing to test here', 'register': 'B',
        'body': [
            "The repository holds five interview records, each with a catalogue card and a "
            "summary. None of the summaries mentions the Bible, a biblical book or a verse. The "
            "only religious terms in them are “mystical experiences”, in the summary of a 1974 "
            "interview, and “prophet”, in the summary of a French documentary transcript.",
            "The most public statements Dick made about scripture therefore cannot be checked "
            "here. A transcript of the Missouri Review interview, “In His Own Words” and the "
            "1974 Vertex interview would be the first texts to add to this study. Until then, "
            "the absence in this essay is an absence in the archive, not a finding about "
            "what he said in public.",
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
        'id': 'summaries', 'heading': 'The stories and the other novels, as summarised', 'register': 'D',
        'body': [
            "The thirty short stories are held here as editorial summaries, not as text. Six of "
            "the summaries use religious vocabulary: “Roog”, “Imposter”, “Adjustment Team”, "
            "“The Minority Report”, “The Days of Perky Pat” and “Faith of Our Fathers”. None of "
            "them names the Bible or a book of it. That may be true of the stories, or it may "
            "be a fact about how the summaries were written. The full text would settle it.",
            "The novel summaries follow the same pattern. The Bible appears in the summaries of "
            "The Divine Invasion and VALIS, and in The Transmigration of Timothy Archer, where a "
            "character quotes scripture. The summary of Ubik records a biblical tradition of "
            "dreams. The summaries of Do Androids Dream of Electric Sheep?, The Man in the High "
            "Castle and A Maze of Death record no biblical reference. These are summaries of "
            "summaries, useful for orientation and not evidence in their own right.",
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
            "Of the scholarship records held here, few mention biblical texts, and none "
            "treats the Torah or the Bible-as-code material of the Exegesis. That is the gap "
            "this study is meant to show.",
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
            "The two lanes differ in voice. The trilogy gives the Bible to characters who argue "
            "about it: Sherri, Kevin, Emmanuel, who holds back. The Exegesis gives it to one "
            "reader who is sure of his reading. That difference is the clearest thing the lanes "
            "show side by side.",
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
        "Dick’s Bible as text, code and world, from a 1972 joke about rhymed couplets to "
        "the April 1981 claim that the Bible is the real world — across the Exegesis, the "
        "VALIS trilogy and the letters, with what the archive cannot yet show."
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
        "VALIS and The Divine Invasion hold the Bible as characters’ argument and as a "
        "hologram. The Divine Invasion gives the Torah a speaker, Zina Pallas. Summaries of "
        "the stories and the other novels record little or no biblical reference."
    ),
    'in_the_exegesis': (
        "The sweep finds Bible vocabulary in 383 of the 1,104 transcribed segments. The "
        "argument runs through the 1975 batch, the 15 September 1976 sitting on Acts in Tears, "
        "the 1978 folder on the living Torah and the Bible in three dimensions, and the April "
        "1981 transcriptions on recombinant scripture and the third testament."
    ),
    'intellectual_background': (
        "Dick’s reference works are named in the transcriptions: the Jerusalem Bible and its "
        "notes, a “Decoded New Testament”, and Augustine’s image of the Bible as letters from "
        "home. The Hymn of the Pearl, in the apocryphal Acts of Thomas, is the one Gnostic "
        "text the scholarship traces through him."
    ),
    'scholarly_debate': (
        "Scholars reach the Bible in Dick through its Gnostic and Pauline edges. The debate is "
        "whether his use of scripture is theology or a literary device; the Exegesis argues the "
        "first, and the trilogy often stages the second."
    ),
    'chronology_summary': (
        "1972: the Bible as a joke about verse. 1975: the Bible as a book of the future. "
        "September 1976: Acts in Tears, and the Bible as code for the present. 1978: the living "
        "Torah and the Bible in three dimensions. April 1981: the Bible as the real world, "
        "recombinant scripture and a third testament."
    ),
    'contradictions_summary': (
        "Dick never settles whether the Bible is a record of the past or a description of the "
        "present. In 1976 it is “not about the past”; in 1978 the Torah is timeless; in 1981 the "
        "Bible is “the real world”."
    ),
    'related_thinkers': ['Paul of Tarsus', 'Elijah', 'Akhenaten', 'Spinoza', 'Philo of '
                         'Alexandria', 'Augustine', 'Martin Luther'],
    'editorial_notes': (
        "Hand-authored editorial prose. The sweep is the corpus; the cards are the passages "
        "chosen from it; the prose cites cards and quotes only what the corpus contains. The "
        "letters are excerpts, the interviews are not held as text, and the stories are "
        "summaries. Folder dates are batch dates."
    ),
    'open_questions': [
        "What did Dick say about the Bible in interviews? Resolvable by: transcripts of the "
        "Missouri Review interview, “In His Own Words”, and the 1974 Vertex interview. None is "
        "held as text.",
        "Which Bible did he use? The transcriptions name the Jerusalem Bible and a “Decoded New "
        "Testament”, but not an edition of the first or the source of the second. Resolvable "
        "by: an inventory of his library, if one survives.",
        "Did Dick know the Acts material in Tears before 1974? He says he recognised it only "
        "after the novel appeared. Resolvable by: the manuscript or typescript of Flow My Tears, "
        "the Policeman Said.",
        "What do the letters after 1973 say about scripture? The repository holds only 1972–73 "
        "excerpts, with some bodies stored in the wrong field.",
        "Do the stories contain biblical references the summaries miss? Resolvable by: full text "
        "of the thirty stories.",
    ],
    'related_topics': [
        {'topic_id': 'TOPIC_GNOS_gnosis_and_anamnesis', 'canonical_name': 'Gnosis and Anamnesis',
         'slug': 'gnosis-and-anamnesis', 'study_id': 'gnosticism'},
        {'topic_id': 'TOPIC_GNOS_valis_trilogy', 'canonical_name': 'Gnosticism in the VALIS Trilogy',
         'slug': 'valis-trilogy', 'study_id': 'gnosticism'},
    ],
}
