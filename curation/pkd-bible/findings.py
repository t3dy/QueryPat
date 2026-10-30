#!/usr/bin/env python3
"""
Hand-classified findings for the "Philip K. Dick and the Bible" dossier.

Each finding names a source, a verbatim anchor inside it, an extraction window,
and the editorial card: `context` summarises the whole passage in the portal's
voice, `pith` quotes the sentence it turns on. The seeder extracts the passage
at the anchor, and refuses to build if an anchor does not resolve or a pith is
not verbatim in its source.

`concepts` doubles as the page's facet vocabulary: biblical books first, then
themes. The facet list in dossier_sections.py names which are browsable.

Registers: A = PKD's own words, B = primary-source fact, C = scholarly
argument, D = portal-editor inference. Lanes follow the studies convention:
A fiction, B Exegesis, C scholarship, D biography, E letters and interviews.

Run build_inventory.py to write evidence-inventory.json.
"""

# --------------------------------------------------------------------------
# Evidence packets: the claims the page makes, each backed by the findings
# that carry its id.
# --------------------------------------------------------------------------

PACKETS = [
    ('PKB-PKT-BEFORE', 'strong',
     "Dick knew and used the Bible well before 2-3-74: as a junior-high listener to a "
     "radio serial about Elijah, as the source of the phrase that titled A Scanner "
     "Darkly, and as a reader comparing translations in 1973.",
     "Letters from 1962 to 1973 quote 1 Corinthians, plan a mock rhyming Bible, and "
     "weigh the Jehovah's Witnesses' New World Translation against the New English "
     "Bible. A 1981 interview dates his first Bible reading to junior high. This "
     "stands against his 1976 statement that in 1974 he was almost totally unfamiliar "
     "with the Bible."),
    ('PKB-PKT-ACTS', 'strong',
     "From 1975 Dick held that Flow My Tears, the Policeman Said (written 1970, "
     "published 1974) reproduces material from the Acts of the Apostles that he had "
     "not consciously put there.",
     "The discovery is reported in letters of 1975, worked over in the Exegesis from "
     "1976, and told publicly in the 1978 speech How to Build a Universe That Doesn't "
     "Fall Apart Two Days Later: Felix, Jason, and the meeting with a black stranger."),
    ('PKB-PKT-FUTURE', 'strong',
     "Dick reads the apocalyptic books — Daniel and Revelation — as descriptions of "
     "the present, and identifies the Empire they denounce with Rome, the United "
     "States, and his own Black Iron Prison.",
     "\"The Bible is a book of the future\" (February 1975); the iron empire with feet "
     "of clay (November 1975); Babylon = Rome = Washington DC = Moscow (1976); VALIS "
     "as \"a fusion of Exodus & Daniel\" (April 1981)."),
    ('PKB-PKT-ELIJAH', 'strong',
     "Malachi's promise that Elijah will return before the Day of the Lord is Dick's "
     "main scriptural frame for what possessed him in 1974.",
     "The Exegesis equates the Spirit of Elijah with the Christian Holy Spirit; the "
     "last interview traces the interest to a junior-high radio serial; The Divine "
     "Invasion makes Elijah a character."),
    ('PKB-PKT-WISDOM', 'strong',
     "The deuterocanonical Wisdom of Solomon, read in 1975 at his church's urging, "
     "supplies Dick's Holy Wisdom (St. Sophia) and her incarnation.",
     "A September 1975 letter explains its Septuagint pedigree; Exegesis entries of "
     "1975 derive Sophia's incarnation and her power to confer immortality from it."),
    ('PKB-PKT-CODE', 'strong',
     "In 1976–78 Dick treats scripture as a cipher: the New Testament is code for the "
     "present, Flow My Tears is in the same code, and Acts is a description of now.",
     "\"The Bible is code\"; the N.T. as \"an encoded instruction manual\"; \"O.T. "
     "encodes + N.T. decyphers\". The same entries say the Bible omits what Tears "
     "preserves, so the cipher is never the whole message."),
    ('PKB-PKT-LIVING', 'strong',
     "Dick's \"living information\" and plasmate are modelled on scripture: the "
     "esoteric Torah as a living being, Acts as alive, the Qumran scrolls and Nag "
     "Hammadi codices as the carriers.",
     "Exegesis entries of 1976–80, and the fiction that dramatises them: Elias's "
     "holographic Bible and Zina's \"I am the Torah\" in The Divine Invasion."),
    ('PKB-PKT-TRANSLATIONS', 'strong',
     "Dick read the Bible in several translations and paid attention to the "
     "differences: King James, the Jehovah's Witnesses' New World Translation, the New "
     "English Bible, the Jerusalem Bible, and the Vulgate.",
     "Letters of 1964 to 1981 and the bibliography of The Transmigration of Timothy "
     "Archer, which cites the Jerusalem Bible."),
    ('PKB-PKT-WHICHGOD', 'moderate',
     "Dick never settled which God of the Bible he had met. In 1977 it is not the "
     "creator god of the Bible; in 1978–80 it is the Cosmic Christ of John; in April "
     "1981 it is YHWH, \"not the God of the N.T.\"",
     "Letter to Julian Jaynes (1977), Exegesis section 016, Exegesis April 1981."),
    ('PKB-PKT-FICTION', 'strong',
     "Scripture is built into the fiction both overtly (VALIS, The Divine Invasion, "
     "The Transmigration of Timothy Archer, Deus Irae) and, by Dick's account, "
     "covertly (Flow My Tears, Ubik, A Scanner Darkly).",
     "Fiction lane passages, each a character speaking, not Dick."),
    ('PKB-PKT-SCHOLARS', 'moderate',
     "Scholars have read Dick's Pauline vocabulary (1 Corinthians 13), his Acts "
     "parallels, and his open, living Bible as structural to the late novels.",
     "Butler, Sutin, the Theory, Culture & Society essay on Dick, Bergson and Saint "
     "Paul, Tseng, and the Extrapolation essay on The Divine Invasion."),
]


# --------------------------------------------------------------------------
# Sources
# --------------------------------------------------------------------------

LV7174 = 'DOC_ARCH_THE_SELECTED_LETTERS_OF_PHILIP_K_DICK_19'
VALIS3 = 'DOC_ARCH_OCEANOFPDF_COM_THE_VALIS_TRILOGY_PHILIP_'
HOWTO = 'DOC_ARCH_45007880_PHILIP_K_DICK_HOW_TO_BUILD_A_UN'
LASTINT = 'DOC_ARCH_OCEANOFPDF_COM_THE_LAST_INTERVIEW_AND_OT'
UBIK = 'DOC_ARCH_BOOK_PKD_UBIK'
FIVE = 'DOC_ARCH_OCEANOFPDF_COM_FIVE_GREAT_NOVELS_THE_THR'
DEUS = 'DOC_ARCH_DICK_PHILIP_KINDRED_ZELAZNY_ROGER_DEUS_I'
SUTIN = 'DOC_ARCH_DIVINE_INVASIONS_A_LIFE_OF_PHI_LAWRENCE_'
BUTLER = 'DOC_ARCH_ANDREW_M_BUTLER_PHILIP_K_DICK_REVISED_AN'
TCS = 'DOC_ARCH_THEORY_CULTURE_AMP_SOCIETY_2008_DEC_VOL_'
TSENG = 'DOC_ARCH_02_LAURIE_JUI_HUA_TSENG'
EXTRAP = 'DOC_ARCH_EXTRAPOLATION_2011_JAN_VOL_52_ISS_2_THE_'

# Exegesis section citations
S10 = 'Exegesis, letters to Claudia Bush (undated, c. 1975–76)'
S11 = 'Exegesis, letter to Doris, September 17, 1975'
S12 = 'Exegesis, section of September 1975'
S13 = 'Exegesis, section of November 1975'
S15 = 'Exegesis, section of September 1976'
S16 = 'Exegesis, section 016 (1978–1980)'
S17 = 'Exegesis, April 1981'


# Each finding:
#   (id, kind, source_id, citation, anchor, window, packet, claim_type,
#    concepts, context, pith, speaker, dated, dating_basis, dating_confidence,
#    editorial_note)
# kind: exegesis_segment | letter | interview | fiction | criticism

F = []


def ex(fid, seg, cite, anchor, win, pkt, ctype, concepts, context, pith,
       dated, basis='record', conf='medium', note=None):
    F.append(dict(id=fid, kind='exegesis_segment', source_id=seg, citation=cite,
                  anchor=anchor, window=win, packet=pkt, claim_type=ctype,
                  concepts=concepts, context=context, pith=pith,
                  speaker='Philip K. Dick', dated=dated, dating_basis=basis,
                  dating_confidence=conf, note=note))


def let(fid, letter_id, cite, anchor, win, pkt, ctype, concepts, context, pith,
        dated, basis='dateline', conf='high', note=None):
    F.append(dict(id=fid, kind='letter', source_id=letter_id, citation=cite,
                  anchor=anchor, window=win, packet=pkt, claim_type=ctype,
                  concepts=concepts, context=context, pith=pith,
                  speaker='Philip K. Dick', dated=dated, dating_basis=basis,
                  dating_confidence=conf, note=note))


def doc(fid, kind, doc_id, cite, anchor, win, pkt, ctype, concepts, context,
        pith, speaker, dated=None, basis=None, conf=None, note=None):
    F.append(dict(id=fid, kind=kind, source_id=doc_id, citation=cite,
                  anchor=anchor, window=win, packet=pkt, claim_type=ctype,
                  concepts=concepts, context=context, pith=pith, speaker=speaker,
                  dated=dated, dating_basis=basis, dating_confidence=conf,
                  note=note))


# ==========================================================================
# 1. Before 2-3-74
# ==========================================================================

doc('PKB-INT-ELIJAH', 'interview', LASTINT,
    'Interview with Gregg Rickman, in Philip K. Dick: The Last Interview and '
    'Other Conversations',
    'there was a soap opera on daytime radio called', [260, 700],
    'PKB-PKT-BEFORE', 'self_report', ['1 Kings', 'Elijah', 'Prior knowledge'],
    "Asked by Gregg Rickman where his religious preoccupations come from, Dick goes "
    "back to junior high school and a daytime radio serial, The Light of the World, "
    "that dramatised the Bible. He tuned in during the Elijah episodes, then read "
    "the story for himself, and wanted above everything to hear the low murmuring "
    "voice Elijah hears on Mount Horeb. He says he heard such a voice two or three "
    "years later, during an eleventh-grade physics exam — and then, half-mocking, "
    "files the whole account as an enormous fantasy. It is the earliest date he "
    "ever gives for reading scripture, and it ties the Bible to the voice, not to "
    "doctrine.",
    'And I started reading the Bible and I read that part about Elijah.',
    'Philip K. Dick', None, None, None,
    note="Dick's own retrospective account, given in the last year of his life. "
         "Sutin independently records a Bible Club he tried to found in junior "
         "high (PKB-SCH-SUTIN-02).")

let('PKB-LET-1962', 'LET_1962-04-25_ANTHONY_BOUCHER_0060',
    'Letter to Anthony Boucher, April 25, 1962',
    'We see as through a glass darkly, now face to face', [700, 300],
    'PKB-PKT-BEFORE', 'self_report', ['1 Corinthians', 'Prior knowledge'],
    "A long autobiographical letter about agoraphobia. Dick describes the world of "
    "the street as one he had experienced as hostile and aimed at him, and a "
    "stimulant that briefly let a stronger, more organised view of the world win "
    "out. He reaches for Paul to say what happened: he saw face to face, and never "
    "fully recovered the delusional view he had lived inside. Twelve years before "
    "2-3-74 the Corinthians verse already names, for him, the moment a false world "
    "gives way.",
    'I did see face to face—and after that, never quite got back the delusional view',
    '25 April 1962')

let('PKB-LET-1964', 'LET_1964-06-07_JAMES_BLISH_0064',
    'Letter to James Blish, June 7, 1964',
    'even if it apes the King James Bible and the Iliad put together', [500, 260],
    'PKB-PKT-TRANSLATIONS', 'critique', ['King James Version', 'Translations'],
    "Part of a long argument with James Blish about what makes a novel serious. "
    "Dick's answer is novelty: a serious book must be new, not formula, and the "
    "King James Bible appears only as the gold standard of borrowed grandeur that "
    "cannot by itself make imitation serious. A literary, not a religious, use — "
    "and a sign of how available the King James cadence was to him.",
    'There is no such thing as a “serious” novel which repeats what has gone before',
    '7 June 1964')

let('PKB-LET-1972', 'LET_1972-11-28_PATRICE_DUVIC_0051',
    'Letter to Patrice Duvic, November 28, 1972',
    'I had set the Bible into rhymed couplets', [420, 320],
    'PKB-PKT-BEFORE', 'self_report', ['Genesis', 'Prior knowledge'],
    "A comic dream reported to his French friend: Dick on stage accepting an award, "
    "Harlan Ellison alone in the audience laughing, and the award turning out to be "
    "for setting the Bible into rhymed couplets. He improvises a Genesis couplet and "
    "sets it against Luther's German, which he says he always liked. Fifteen months "
    "before 2-3-74, scripture is a joke he expects a correspondent to get.",
    'I had set the Bible into rhymed couplets.',
    '28 November 1972')

let('PKB-LET-1973A', 'LET_1973-01-07_ART_SPIEGELMAN_MICHELE_GROSS_0062',
    'Letter to Art Spiegelman and Michele Gross, January 7, 1973',
    'turning the Bible into rhymed cou', [380, 260],
    'PKB-PKT-BEFORE', 'self_report', ['Prior knowledge'],
    "Written from Fullerton during the chaotic early months of 1973. The rhymed "
    "Bible from the Duvic dream has become a running gag: Dick reports the project "
    "coming along fine, one couplet finished after four months' work, undertaken at "
    "the dream's bidding for the glory of God and for profit. The joke matters "
    "because it is a joke: the Bible is there to be played with.",
    'for the Glory of God, as well as for fun and profit in my spare time.',
    '7 January 1973')

let('PKB-LET-1973B', 'LET_1973-03-31_CAROL_CARR_0099',
    'Letter to Carol Carr, March 31, 1973',
    'as a sort of pun on Paul', [520, 420],
    'PKB-PKT-BEFORE', 'self_report',
    ['1 Corinthians', 'A Scanner Darkly', 'Prior knowledge'],
    "Exhausted after writing 110 pages in four days, Dick tells Carol Carr about the "
    "new novel, A Scanner Darkly — a somber, tragic book about drug addiction — and "
    "explains its title as a pun on Paul's phrase from 1 Corinthians 13. This is the "
    "clearest proof that a biblical verse was structural to his fiction before "
    "2-3-74: the title, and with it the novel's governing idea of impaired sight, "
    "comes from Paul a year before the visions.",
    'what it is called as a sort of pun on Paul’s phrase, “... We see as through a glass darkly,”',
    '31 March 1973')

let('PKB-LET-1973C', 'LET_1973-09-11_SCOTT_MEREDITH_0192',
    'Letter to Scott Meredith, September 11, 1973',
    'this Jehovah’s Witnesses version is better', [520, 420],
    'PKB-PKT-TRANSLATIONS', 'comparison',
    ['Ecclesiastes', '1 Corinthians', 'Translations', "Jehovah's Witnesses",
     'Prior knowledge'],
    "To his literary agent, five months before 2-3-74, Dick shares a fragment of "
    "Ecclesiastes in the Jehovah's Witnesses' New World Translation and says he "
    "prefers it to the older version. He then sets three renderings of 1 Corinthians "
    "15:51 side by side — the New World Translation's \"Look! I tell you a sacred "
    "secret\", the King James \"Behold I tell you a mystery\", and the New English "
    "Bible's \"Listen! I shall unfold a mystery\" — and praises the first as direct "
    "and honest. This is close reading of translation, not casual quotation.",
    'The new JW version is so direct, so—honest.',
    '11 September 1973')

# ==========================================================================
# 2. 1975: the discovery and the first frame
# ==========================================================================

let('PKB-LET-1975-WILLIAMS', 'LET_1975-01-27_PAUL_WILLIAMS_0030',
    'Letter to Paul Williams, January 27, 1975',
    'even if the Bible itself were totally suppressed and lost', [520, 300],
    'PKB-PKT-LIVING', 'causal_theory', ['Living scripture', 'Anamnesis'],
    "Within a year of 2-3-74, Dick argues to Paul Williams that Christ made "
    "salvation an a priori, inward event, not dependent on outside knowledge, gurus "
    "or sacred texts. The consequence he draws is striking for a man about to spend "
    "eight years on scripture: the Bible is dispensable. Suppress it entirely and the "
    "experience it records would spring to life again in human minds. Set this "
    "beside the later view that the text itself is alive.",
    'this would all reoccur, spring to life within given human minds once more',
    '27 January 1975')

let('PKB-LET-1975-KORMAN', 'LET_1975-02-22_HENRY_KORMAN_0054',
    'Letter to Henry Korman, February 22, 1975',
    'Is it not written in your own law', [420, 420],
    'PKB-PKT-TRANSLATIONS', 'comparison',
    ['Gospel of John', 'Psalms', 'Anamnesis', 'Translations'],
    "Writing to a correspondent interested in Sufism, Dick quotes John 10:34–36 from "
    "the New English Bible — Jesus answering the charge that he claims to be a god "
    "with Psalm 82's \"You are gods\" — as a verse that never seemed to be there "
    "before when he read it. He connects it at once to anamnesis, the Platonic and "
    "Orphic loss of forgetting, which he thinks Jesus is referring to. Reading "
    "scripture is now reading with new eyes.",
    'Scripture cannot be set aside.',
    '22 February 1975')

let('PKB-LET-1975-CLAUDIA', 'LET_1975-02-27_CLAUDIA_BUSH_0063',
    'Letter to Claudia Bush, February 27, 1975',
    'The Bible is a book of the future.', [520, 520],
    'PKB-PKT-FUTURE', 'definition',
    ['Revelation', 'Ubik', 'Apocalypse', 'Orthogonal time'],
    "The long letter to Claudia Bush in which Dick works out \"orthogonal time\" "
    "from Joe Chip's retrograde world in Ubik. Scientists, he predicts, will find "
    "that axis and it will look like our past without being our past. Then the "
    "sentence that governs the next seven years: the Bible, New Testament and Old "
    "Testament oracles alike, is about tomorrow. He separates ground from set — the "
    "familiar backdrop is old, the events played out against it are new — and names "
    "the event: Final Reckoning Time.",
    'The Bible is a book of the future.',
    '27 February 1975',
    note="The same letter is transcribed in the Exegesis folders (segment "
         "SEG_EXEG_1975-02-27_Claudia_03); the letter's dateline is used here.")

let('PKB-LET-1975-ORNSTEIN', 'LET_1975-03-04_ROBERT_ORNSTEIN_0075',
    'Letter to Robert Ornstein, March 4, 1975',
    'Brady finds that the New Testament is in cypher', [620, 360],
    'PKB-PKT-CODE', 'allegory',
    ['Qumran & Nag Hammadi', 'Bible as code', 'To Scare the Dead'],
    "Dick outlines, for the psychologist Robert Ornstein, a novel he calls To Scare "
    "the Dead: Nicholas Brady, a secular man, is taken over by the mind of an Essene "
    "from the Qumran wadi of about 45 A.D. Studying the Bible with this second "
    "personality, Brady finds the New Testament is a cipher that the Qumran mind can "
    "read. The plot is the seed of VALIS and The Divine Invasion — and the earliest "
    "statement of the Bible-as-code idea, made in fiction before it is made in the "
    "Exegesis.",
    'Brady finds that the New Testament is in cypher.',
    '4 March 1975')

let('PKB-LET-1975-CBS', 'LET_1975-07-07_MOSES_THE_LAWGIVER_CBS_TV_0110',
    'Letter to CBS Television about Moses the Lawgiver, July 7, 1975',
    'The Bible states that the reason is that the destroying angel', [520, 260],
    'PKB-PKT-TRANSLATIONS', 'critique', ['Exodus', 'Moses'],
    "A fan letter to the network after its miniseries Moses the Lawgiver, which Dick "
    "praises warmly. His one quibble is exegetical: the script has Moses explain "
    "Passover as passing over from death to life, but the text of Exodus gives the "
    "destroying angel passing over the Israelites' houses. He reports that the "
    "programme sent him to the reference books. A small document, but it shows him "
    "holding a dramatisation to the letter of the text.",
    'they, the Israelites, were lit­ erally passed over.',
    '7 July 1975')

let('PKB-LET-1975-BENGTSON', 'LET_1975-07-11_G_RAN_BENGTSON_0115',
    'Letter to Göran Bengtson, July 11, 1975',
    'contains a number of passages evidently derived from', [600, 300],
    'PKB-PKT-ACTS', 'self_report', ['Acts', 'Flow My Tears', 'Ubik', 'Greek'],
    "To a Swedish correspondent Dick tells an odd story about Ubik's Greek, then "
    "offers what he calls a bizarre theory: that his unconscious is an Attic Greek, "
    "versed in philosophy and theology, which ghost-wrote Ubik and perhaps other "
    "books. The evidence he offers is Flow My Tears, the Policeman Said, which on "
    "close inspection contains passages derived from the Book of Acts — written, he "
    "notes, in Greek. The earliest dated letter in this archive to name the Acts "
    "parallel.",
    'FLOW MY TEARS, on close inspection, contains a number of passages evidently derived from or which refer to the',
    '11 July 1975')

let('PKB-LET-CLAUDIA-AGAPE', 'LET_UNDATED_CLAUDIA_BUSH_0044',
    'Letter to Claudia Bush, undated — Selected Letters 1975–1976',
    'so much else from Paul', [620, 120],
    'PKB-PKT-ACTS', 'self_report', ['Acts', 'Flow My Tears', 'Agape'],
    "The close of a letter to Claudia Bush. Dick reads the ending of Flow My Tears — "
    "Felix Buckman, after his dream, embracing the first stranger he meets, a black "
    "man at a gas station — as the embrace at the heart of the early Christian Feast "
    "of Agape, almost the reconstruction of the Savior out of Everyman at random. He "
    "does not know how it got into the novel, but so much else from Acts did. He "
    "attributes Acts to Paul; it is traditionally Luke's.",
    'How it got into my novel I don’t know',
    'Undated (1975–76)', 'record', 'low')

ex('PKB-EX-1975-DECODED', 'SEG_EXEG_U_Claudia_06', S10,
   'The band of darkness which I and Laura saw', [120, 620],
   'PKB-PKT-TRANSLATIONS', 'comparison',
   ['Matthew', 'The Decoded New Testament', 'Good Friday'],
   "Dick recalls the band of darkness he and his daughter Laura saw cross the sky "
   "one Good Friday, during the three hours in which Christ lies dead, with a "
   "powerful wind. He reads it through The Decoded New Testament, which glosses the "
   "cry from the cross, \"Eli, Eli\", as \"my power, my power\" — gone because the "
   "sun has gone down. The darkness the Gospels describe and the darkness they saw "
   "are, he suggests, the same, and a friend's idea of a time dysfunction on the "
   "day of the Crucifixion is entertained.",
   'This darkness described in the Bible, and referred to in the "Decoded" is what Laura and I saw',
   'c. 1975–76', 'record', 'low',
   note="The Decoded New Testament (Gene Savoy, 1974) is a modern esoteric "
        "reading of the Gospels, not a translation; Dick treats it as an "
        "authority alongside the text.")

ex('PKB-EX-1975-MALACHI', 'SEG_EXEG_U_Claudia_02', S10,
   'may have been what Malachi meant', [500, 420],
   'PKB-PKT-ELIJAH', 'comparison', ['Malachi', 'Elijah', 'Theophany'],
   "Dick concedes that no one else saw what he saw, which by ordinary standards "
   "makes it subjective. Then he reaches for Malachi 3:1: seeing the signals firing "
   "all around him, the world as a living organism, may be what the prophet meant "
   "by the Lord of Hosts suddenly coming to his temple. The prophetic text supplies "
   "the description his experience lacks — and he immediately worries whether the "
   "presence was always there and his eyes were only opened.",
   'suddenly He was within everything, and visible, at least to me.',
   'c. 1975–76', 'record', 'low')

ex('PKB-EX-1975-ELIJAH', 'SEG_EXEG_U_Claudia_09', S10,
   'the relationship between Elijah and the Holy Spirit', [460, 560],
   'PKB-PKT-ELIJAH', 'definition', ['Malachi', '2 Kings', 'Elijah', 'Holy Spirit'],
   "Having concluded that 3-74 was a Second Advent, Dick resolves what he calls a "
   "mystery: how Elijah relates to the Holy Spirit. What Malachi promised would "
   "return was the Spirit of Elijah, not the man — clear, he says, from the story "
   "of Elisha — and the Spirit of Elijah is the strict monotheists' Old Testament "
   "name for the Christian Holy Spirit. Possession by Elijah and possession by God "
   "as Spirit are therefore the same thing.",
   'The Spirit of Elijah is the Old Testament Hebrew concept for the Christian Holy Spirit',
   'c. 1975–76', 'record', 'low')

ex('PKB-EX-1975-REVROME', 'SEG_EXEG_U_Claudia_17', S10,
   'witness the beast in Revelation which equals Rome', [500, 420],
   'PKB-PKT-FUTURE', 'allegory',
   ['Revelation', 'Daniel', 'Empire', 'Parousia'],
   "If the tyranny thrown down in 1974 is Rome, the adversary of Christianity — the "
   "beast of Revelation — then its fall is the long-awaited triumph of "
   "Christianity, and since the cosmic Christ led the assault, Dick asks in what way "
   "this is not the Parousia itself, the battle of Revelation, and Daniel's statue "
   "with feet of clay. He then turns at once to the question of what task, if any, "
   "he has been assigned.",
   'then in what way is this not the Parousia and the battle described therein',
   'c. 1975–76', 'record', 'low')

ex('PKB-EX-1975-WISDOM', 'SEG_EXEG_U_Claudia_31', S10,
   'from reading "The Wisdom of Solomon"', [520, 420],
   'PKB-PKT-WISDOM', 'causal_theory',
   ['Wisdom of Solomon', 'Hagia Sophia', 'Incarnation'],
   "Reading the Wisdom of Solomon gives Dick a theory of the Incarnation: St. "
   "Sophia, the world-builder and maintainer of the Wisdom books, entered human form "
   "and for that time lost some of her powers, which is why the incarnate time had "
   "to be brief and why Jesus speaks to his disciples of short-lived pain. Released "
   "again, she can help without limit. Holy Wisdom, the figure who dominates the "
   "late novels, enters here through a deuterocanonical book.",
   'St. Sophia entered human form and during this time lost the various capacities',
   'c. 1975–76', 'record', 'low')

ex('PKB-EX-1975-SEPTUAGINT', 'SEG_EXEG_1975-09-17_Doris_01', S11,
   'I had been reading the apocryphal book', [80, 520],
   'PKB-PKT-WISDOM', 'self_report',
   ['Wisdom of Solomon', 'Septuagint', 'Translations', 'Episcopal Church'],
   "A letter to his friend Doris, filed with the Exegesis. Dick explains why he has been "
   "reading the Wisdom of Solomon: his church — the Episcopal Church — now recommends "
   "the apocryphal books. He gives its pedigree carefully: written in the first "
   "century B.C., part of the Septuagint that the New Testament cites as the "
   "scriptures of the early Christians, and therefore as sacred to them as any "
   "book of the Hebrew Bible. He then copies out passages for her.",
   'was as sacred as any book of the Hebrew Scriptures.',
   '17 September 1975', 'dateline', 'high',
   note="The same text appears in the Selected Letters as a letter beginning "
        "\"Dear Sherri\" (record LET_UNDATED_SHERRI_SOLVIG_0148). Whether Dick sent "
        "it twice or the two records name the recipient differently is not "
        "resolved here.")

ex('PKB-EX-1975-FELIX', 'SEG_EXEG_1975-09-15_SECTION_012_02', S12,
   'It points to the Biblical nature of the dream', [520, 420],
   'PKB-PKT-FUTURE', 'causal_theory',
   ['Daniel', 'Revelation', 'Flow My Tears', 'King Felix'],
   "The real meaning of the dream in Flow My Tears, Dick decides, is not the dream "
   "but one embedded word: \"Felix\". It points to the dream's biblical source, "
   "Daniel and Revelation. He adds that apocalyptic literature, of which only two "
   "books were kept in the Bible, tells of Christ returning as a king on horseback "
   "with other horsemen — the dream's image — and calls the novel an apocalyptic "
   "piece with a covered-over message.",
   'all apocalyptic literature (of which only 2 books are retained in the Bible, of many)',
   'September 1975', 'record', 'medium')

ex('PKB-EX-1975-CLAYFEET', 'SEG_EXEG_1975-11-05_SECTION_013_06', S13,
   'the last of the empires mentioned in the "Book of Daniel,"', [600, 420],
   'PKB-PKT-FUTURE', 'comparison',
   ['Daniel', "Jehovah's Witnesses", 'Empire', 'Cosmic Christ'],
   "Dick describes the power he met as the bodiless cosmic Christ, everywhere at "
   "once, which he saw depose the tyranny. He then borrows the Jehovah's Witnesses' "
   "reading of Daniel 2: the Anglo-American Empire is the last of Daniel's kingdoms, "
   "the iron with feet of clay, and he saw the stone \"not cut by man\" hurled at "
   "it. \"Could they be right?\" — he asks, and answers with what he knows: He is "
   "here with power.",
   'Could they be right? Well, I know what I know',
   'November 1975', 'record', 'medium')

ex('PKB-EX-1975-APOC', 'SEG_EXEG_1975-11-05_SECTION_013_17', S13,
   'What is real is the Apocalypse.', [520, 360],
   'PKB-PKT-FUTURE', 'definition', ['Daniel', 'Revelation', 'Apocalypse'],
   "Dick argues that a real, unchanging world lies above and behind linear time, and "
   "that his experience is inexplicable without it. Certain things are always there "
   "and certain events always happening — true in Daniel's time, in John's, and in "
   "his. Apocalyptic vision is not a picture of the end of history but a glimpse of "
   "eternal reality behind the deceptive world of change.",
   'It was true in Daniel’s time, in John’s and mine.',
   'November 1975', 'record', 'medium')

# ==========================================================================
# 3. 1976: the cipher
# ==========================================================================

let('PKB-LET-1976-HUDNER', 'LET_1976-09-06_DOROTHY_HUDNER_0287',
    'Letter to Dorothy Hudner, September 6, 1976',
    'At the time I saw them I was almost totally unfamiliar with the Bible', [700, 300],
    'PKB-PKT-BEFORE', 'self_report',
    ['Daniel', 'Revelation', 'Empire', 'Prior knowledge'],
    "Writing to his mother, Dick describes two worlds of unchange seen in 1974 beneath "
    "the veil of reality: the Iron Empire, Rome, named in Daniel and Revelation, and "
    "a garden of palm trees he walked in for hours. Then a claim about himself: when "
    "he saw them he was almost totally unfamiliar with the Bible and did not "
    "recognise the Iron Empire as the one the two prophets saw. The claim makes the "
    "visions independent of his reading — and it is contradicted by his own letters "
    "of 1962–73.",
    'At the time I saw them I was almost totally unfamiliar with the Bible',
    '6 September 1976',
    note="See the contradiction with PKB-LET-1973B, PKB-LET-1973C and "
         "PKB-INT-ELIJAH. Dick may mean the apocalyptic books specifically; the "
         "letter does not say so.")

ex('PKB-EX-1976-CODE', 'SEG_EXEG_1976-09-15_Dorothy_81', S15,
   "isn't about the past; it's code to describe our world", [420, 420],
   'PKB-PKT-CODE', 'definition', ['Acts', 'Bible as code', 'Flow My Tears', 'Empire'],
   "A war with two sides, us and them, the republic against the empire, \"like in "
   "Star Wars\". Then the thesis, stated flatly: the Bible is not about the past but "
   "a code describing our world, as Flow My Tears is. \"Christ\" names a class of "
   "people now living, Dick among them; the Bible is how they spread the news of "
   "what this world really is; and Acts is not 45 A.D. but now.",
   "Acts isn't 45 AD; it's now.",
   'Date uncertain (1976–79)', 'record', 'low',
   note="Our record dates this section September 1976, but the same segment "
        "carries later stamps (11/19/77 and 3/25/79) and a folder-32 marker, so "
        "the passage cannot be dated more closely than 1976–79.")

ex('PKB-EX-1976-ACTSPRISON', 'SEG_EXEG_1976-09-15_Dorothy_81', S15,
   "That's the code in", [120, 640],
   'PKB-PKT-ACTS', 'causal_theory', ['Acts', 'Bible as code', 'Flow My Tears', 'Thomas'],
   "The same sitting, a few lines on. The code in Flow My Tears is the time and "
   "place of Acts — but what and where is Acts? \"The Bible is code.\" Acts is how "
   "it really is: a police state, and we are in prison. Dick's fake memory, laid "
   "down from 2-74, did not take; portions of true memory, of Acts, survived, along "
   "with Thomas, his real personality. Anamnesis is to be read literally.",
   'Acts is how it really is. Acts is a police state.',
   'Date uncertain (1976–79)', 'record', 'low')

ex('PKB-EX-1976-OMITS', 'SEG_EXEG_1976-09-15_Dorothy_196', S15,
   'The Bible could not serve this purpose', [620, 420],
   'PKB-PKT-CODE', 'causal_theory',
   ['Acts', 'Flow My Tears', 'Living scripture', 'Zebra'],
   "Dick describes two-way travel along the form axis: he went back to Acts by way "
   "of Flow My Tears, while Thomas, an apostolic Christian, came forward. Only the "
   "brain, as living plasmic information, can make that journey — and the Bible "
   "could not have been the vehicle, because Acts as canonised leaves out crucial "
   "information that survives in the novel as Felix Buckman's dream. The novel, on "
   "this account, is more complete than the scripture.",
   'the book "Acts of the Apostles" in it leaves out crucial information',
   'September 1976', 'record', 'medium')

ex('PKB-EX-1976-MANUAL', 'SEG_EXEG_1976-09-15_Dorothy_80', S15,
   'which required me to decode the N.T.!', [520, 400],
   'PKB-PKT-CODE', 'definition', ['Bible as code', 'Valis', 'Crucifixion'],
   "Outlining what his research has to show, Dick proposes that the cosmos has a "
   "dependable mechanism of justification that someone who understood it could "
   "use, in the paradigm of the crucifixion story, to attain apotheosis. Doing so "
   "required decoding the New Testament — reading it as an encoded instruction "
   "manual for becoming part of Valis. The early Christians who understood this, he "
   "adds, could rejoice in their sufferings.",
   'To view it as an encoded instruction manual by which to become part of Valis.',
   'September 1976', 'record', 'medium')

ex('PKB-EX-1976-BABYLON', 'SEG_EXEG_1976-09-15_Dorothy_50', S15,
   "The apocalyptic scene I glimpsed of the siege lifted", [80, 560],
   'PKB-PKT-FUTURE', 'comparison',
   ['Daniel', 'Black Iron Prison', 'Empire', 'Flow My Tears'],
   "Dick identifies the apocalyptic scene he glimpsed — a siege lifted, prisons "
   "freed, a tyrant destroyed — as Cyrus's siege of Babylon and the fall of "
   "Belshazzar, with Daniel as the prisoner. Tears, he says, describes Babylon, "
   "which is Rome, the paradigm of the Black Iron Prison, and the elements of "
   "apocalyptic scripture emerge in it. The identification runs across history: "
   "Babylon equals Rome equals Washington DC equals Moscow.",
   'Babylon = Rome = Washington DC = Moscow, etc.',
   'September 1976', 'record', 'medium')

ex('PKB-EX-1976-ALIENATED', 'SEG_EXEG_1976-09-15_Dorothy_03', S15,
   'And I had visions in the images used by Daniel and in Rev.', [300, 520],
   'PKB-PKT-FUTURE', 'self_report',
   ['Daniel', 'Revelation', 'Hagia Sophia', 'Flow My Tears'],
   "Dick lists his visions in the images of Daniel and Revelation as corroboration, "
   "says St. Sophia led the attack and so Christ was its captain, and claims that "
   "with the Tears dream added, every major theme of both books is in his "
   "experience. Then, from the Encyclopaedia Britannica, a sociological caution he "
   "applies to himself: only an alienated person judges the system evil and yearns "
   "for divine intervention. \"I fit this latter class.\"",
   'I fit this latter class.',
   'September 1976', 'record', 'medium')

ex('PKB-EX-1976-SUN', 'SEG_EXEG_1976-09-15_Dorothy_48', S15,
   'In Malachi it', [520, 380],
   'PKB-PKT-ELIJAH', 'comparison', ['Malachi', 'Elijah', '1 Kings'],
   "Elijah is the forerunner, not the transformation itself, Dick writes, and to "
   "know what kind of change he brings, look at what he did to King Ahab. He quotes "
   "Malachi 4: on the day God acts the sun of righteousness will rise with healing "
   "in its wings, and the righteous will break loose like calves from the stall and "
   "tread down the wicked. The healing comes with the trampling.",
   'consider what he did vis-a-vis king Ahab.',
   'September 1976', 'record', 'medium')

ex('PKB-EX-1976-QUMRAN', 'SEG_EXEG_1976-09-15_Dorothy_232', S15,
   'He is the Savior, who slumbered 1900 years', [260, 420],
   'PKB-PKT-LIVING', 'causal_theory',
   ['Qumran & Nag Hammadi', 'Thomas', 'Living scripture'],
   "Thomas, the personality Dick believed took him over in 1974, is promoted here "
   "from secret apostolic Christian to the one \"they\" had waited for: the Savior, "
   "asleep for 1,900 years, perhaps in a jar at Qumran. The Dead Sea Scrolls become "
   "a container for a living being. An adjacent entry imagines the information "
   "riding in the Qumran scrolls from John to Bishop Pike to Dick.",
   'perhaps in a jar at Qumran.',
   'September 1976', 'record', 'medium')

# ==========================================================================
# 4. 1977–80: living scripture
# ==========================================================================

let('PKB-LET-1977-JAYNES', 'LET_1977-03-16_JULIAN_JAYNES_0021',
    'Letter to Julian Jaynes, March 16, 1977',
    'is not so much the creator god of our Bible', [520, 420],
    'PKB-PKT-WHICHGOD', 'critique', ['Genesis', 'Logos', 'Hagia Sophia', 'Which God'],
    "To the author of The Origin of Consciousness in the Breakdown of the Bicameral "
    "Mind, Dick concedes the right-hemisphere command voice but insists that three "
    "years of research convince him it is godly in nature, not only in tone. Which "
    "god matters: not the creator god of the Bible but the \"arranger\" god of Plato "
    "and the pre-Socratics, ordering anomie into cosmos — the Logos, St. Sophia, Holy "
    "Wisdom.",
    'not so much the creator god of our Bible but the “arranger” god of Plato',
    '16 March 1977')

ex('PKB-EX-1978-UNCONSCIOUS', 'SEG_EXEG_1978-10-10_SECTION_016_259', S16,
   'unconsciously I knew the Book of Acts', [520, 420],
   'PKB-PKT-ACTS', 'self_report',
   ['Acts', 'Flow My Tears', 'Prior knowledge', 'Urstory'],
   "Dick weighs the coincidences in Flow My Tears: the Acts material and the John "
   "Taverner material. One could say he had read Acts and forgotten it — he allows "
   "that — but not Taverner, a sixteenth-century figure he could not have known. "
   "Two coincidences together cannot be chance, so there is an Ur-story, a sacred "
   "narrative that is the informational basis of reality, or an alternate reality "
   "seeping through.",
   'Clearly, there is an Urstory',
   'Date uncertain (1978–80)', 'record', 'low',
   note="Here Dick allows he may have read Acts earlier and forgotten it; Butler "
        "says he had not previously read it (PKB-SCH-BUTLER-01).")

ex('PKB-EX-1978-CONTEMPORARY', 'SEG_EXEG_1978-10-10_SECTION_016_317', S16,
   'he is a contemporary of Christ', [620, 420],
   'PKB-PKT-ACTS', 'definition', ['Acts', 'Anamnesis', 'Pentecost'],
   "A description, in the third person, of what the revelation gives its "
   "recipient: he knows he has played a role in a dialectical struggle outside "
   "space and time since Pentecost, and lives in reality as interpreted through "
   "the lens of Acts. He is a contemporary of Christ, his own acts part of the Acts "
   "of the Apostles; he does not believe it but knows it, because he sees and "
   "remembers it.",
   'his own acts are part of the Acts of the Apostles.',
   'After November 1980', 'stamp', 'medium',
   note="The same segment refers back to \"11-17-80\", so the passage is no "
        "earlier than late November 1980, whatever the section's container date.")

ex('PKB-EX-1978-TORAH', 'SEG_EXEG_1978-10-10_SECTION_016_73', S16,
   'Philo speaks of the Torah as a living being', [420, 520],
   'PKB-PKT-LIVING', 'causal_theory',
   ['Torah', 'Acts', 'Living scripture', 'Plasmate'],
   "Dick copies out a description of the esoteric Torah as a pre-existent being "
   "made of the one great name of God, and Philo's image of the Torah as a living "
   "being whose body is the Pentateuch's literal text and whose soul is its occult "
   "meaning. His response is an exclamation: this is the Acts material, the living "
   "information he saw, the plasmate. Acts, and probably other parts of the Bible, "
   "are alive.",
   'This is the Acts material, the living information I saw',
   'Date uncertain (1978–80)', 'record', 'low')

ex('PKB-EX-1978-DECYPHER', 'SEG_EXEG_1978-10-10_SECTION_016_65', S16,
   'O.T. encodes + N.T. decyphers', [560, 420],
   'PKB-PKT-CODE', 'allegory', ['Bible as code', 'Which God', 'Dialectic'],
   "Dick imagines the two testaments as players in a game run for a finite time, "
   "which the New Testament God will win: justice against mercy, power against "
   "knowledge. The Old Testament creates and poses puzzles; the New, wisdom, solves "
   "them. The Old encodes and the New deciphers; the Old is closed and dark, the "
   "New open and light — and the New can reverse polarities with a counter-puzzle "
   "and start a new hand.",
   'O.T. encodes + N.T. decyphers',
   'Date uncertain (1978–80)', 'record', 'low')

ex('PKB-EX-1978-KJV', 'SEG_EXEG_1978-10-10_SECTION_016_140', S16,
   'It was like the King James Bible', [520, 360],
   'PKB-PKT-TRANSLATIONS', 'self_report',
   ['King James Version', 'Logos', 'Translations'],
   "Revising his reading of a 5 a.m. vision: he was handing someone not technical "
   "papers but a Bible — a finished, authoritative book of sanctioned scripture, "
   "like the King James Bible he gave his mother years ago. The information in him, "
   "he concludes, is religious: further divine revelation, to be printed publicly, "
   "not in classified documents.",
   'That what we are dealing with is further divine revelation',
   'Date uncertain (1978–80)', 'record', 'low')

ex('PKB-EX-1978-UBIKWORD', 'SEG_EXEG_1978-10-10_SECTION_016_140', S16,
   'Ubik specifically says, "I am the word"', [520, 420],
   'PKB-PKT-LIVING', 'comparison',
   ['Gospel of John', 'Ubik', 'Logos', 'Hagia Sophia'],
   "From the Britannica's article on the Fourth Gospel Dick takes a lineage — truth "
   "against lie, light against darkness, from Zoroastrianism through Qumran to St. "
   "John — and identifies Valis's invasion of the world with John's light "
   "penetrating the darkness. Valis is Ubik, he writes, because Ubik says \"I am the "
   "word\": the Logos, God's wisdom, entering creation and becoming the Paraclete.",
   'Valis is Ubik.',
   'Date uncertain (1978–80)', 'record', 'low')

ex('PKB-EX-1978-NAGHAMMADI', 'SEG_EXEG_1978-10-10_SECTION_016_60', S16,
   'in 1945 at Nag Hammadi the actual Secret Living', [520, 420],
   'PKB-PKT-LIVING', 'causal_theory',
   ['Qumran & Nag Hammadi', 'Plasmate', 'Living scripture', 'Eucharist'],
   "Only when reality is experienced as the body of Christ and its life process as "
   "the sacred blood are we home, Dick writes — and then asks: what if the codices "
   "unearthed at Nag Hammadi in 1945 were the Secret Living Blood of Christ, "
   "information and Logos, which restored him and the world, the plasmate described "
   "in VALIS? Buried scripture becomes eucharistic substance.",
   'What, oh what, if it were true that in 1945 at Nag Hammadi',
   'Date uncertain (1978–80)', 'record', 'low')

ex('PKB-EX-1978-YALTABAOTH', 'SEG_EXEG_1978-10-10_SECTION_016_16', S16,
   'after reading in the Nag Hammadi codices', [360, 420],
   'PKB-PKT-WHICHGOD', 'comparison',
   ['Qumran & Nag Hammadi', 'Palmer Eldritch', 'Gnosticism', 'Which God'],
   "Reading the Nag Hammadi codices settles a question about his own fiction: "
   "Palmer Eldritch is beyond doubt Yaltabaoth, the blind creator god of the "
   "Gnostics — the blindness matching Eldritch's artificial eyes — and the novel "
   "explicitly makes Eldritch the Christian God. The non-canonical scriptures "
   "reframe the canonical God as a demiurge.",
   'Palmer Eldritch is beyond doubt Yaltabaoth',
   'Autumn 1978', 'folder', 'medium',
   note="Folder 21; the Burroughs dossier's dating places folders 20–21 between "
        "7 September and 18 October 1978 on the published edition's evidence.")

ex('PKB-EX-1978-MATTHEW', 'SEG_EXEG_1978-10-10_SECTION_016_226', S16,
   'The Jehovah\'s Witnesses do not understand that', [520, 420],
   'PKB-PKT-TRANSLATIONS', 'critique',
   ['Matthew', 'Torah', "Jehovah's Witnesses", 'Hagia Sophia'],
   "Only as Son of God or Hagia Sophia, Dick argues, could Christ claim authority "
   "to amend the Torah, which no man could void; so the claim to divine kingship "
   "was essential. The Jehovah's Witnesses — who deny Christ's full divinity — do "
   "not understand this. He then quotes the antitheses of the Sermon on the Mount, "
   "Matthew 5:21 and 5:28, in which Jesus revises the Law on his own authority.",
   'God having established the Torah it could not be voided or superceded or amended by any man.',
   'Date uncertain (1978–80)', 'record', 'low')

ex('PKB-EX-1980-COSMICCHRIST', 'SEG_EXEG_1978-10-10_SECTION_016_321', S16,
   'The Jehovah\'s Witnesses make this distinction', [620, 380],
   'PKB-PKT-WHICHGOD', 'definition',
   ['Gospel of John', "Jehovah's Witnesses", 'Valis', 'Agape'],
   "The human side of Jesus is like us, Dick writes, but Jesus and the Cosmic Christ "
   "are not the same — a distinction he credits to the Jehovah's Witnesses. Valis is "
   "not Jesus but the Cosmic Christ, what it was before the incarnation, if he "
   "reads St. John correctly. The discovery that follows is new to him: our nature "
   "is not noein, pure reason, but agape.",
   'Valis is not Jesus; Valis is the Cosmic Christ',
   'After November 1980', 'stamp', 'medium',
   note="The same segment refers back three times to \"11-17-80\".")

ex('PKB-EX-1978-SCROLLS', 'SEG_EXEG_1978-10-10_SECTION_016_63', S16,
   'the huge open books I saw were the Qumran scrolls Jim saw', [460, 380],
   'PKB-PKT-LIVING', 'causal_theory',
   ['Qumran & Nag Hammadi', 'Plasmate', 'James Pike', 'Living scripture'],
   "\"Here is the missing piece\": the huge open books Dick saw were the Qumran "
   "scrolls Bishop James Pike saw, and as plasmate they passed from Pike to Dick, "
   "the information being alive. It was no accident but planned by the divine "
   "power, and the lost gnosis of the ancients reconstituted itself in his head — "
   "and is in VALIS.",
   'the info (as I guessed) is alive.',
   'Date uncertain (1978–80)', 'record', 'low')

ex('PKB-EX-1978-YOUNGKING', 'SEG_EXEG_1978-10-10_SECTION_016_119', S16,
   'as seen in Daniel + revelation', [520, 360],
   'PKB-PKT-FUTURE', 'causal_theory',
   ['Daniel', 'Revelation', 'Flow My Tears', 'King Felix'],
   "Dick rereads the dream in Flow My Tears through Frazer as the ritual killing of "
   "the old king by the new — and then corrects himself: the figure on horseback is "
   "the young king, Christ, as judge and Pantocrator in Daniel and Revelation, "
   "killed, returned, and now taking his rightful place. He quotes Revelation 1:18, "
   "\"I was dead but now I am alive again for ever + ever\".",
   'Revelation makes This clear.',
   'Date uncertain (1978–80)', 'record', 'low')

# ==========================================================================
# 5. 1981
# ==========================================================================

let('PKB-LET-1981-BLOODWATER', 'LET_UNDATED_PATRICIA_WARRICK_0025',
    'Letter to Patricia Warrick, January 11, 1981',
    'I was studying the ending of the Fourth Gospel', [40, 620],
    'PKB-PKT-TRANSLATIONS', 'self_report',
    ['Gospel of John', 'Jerusalem Bible', 'Translations', 'Holy Spirit'],
    "Dick tells Patricia Warrick he has been studying the end of John's Gospel, "
    "where Thomas puts his hand into Christ's side, and found strange notes in his "
    "Jerusalem Bible — \"an official Catholic Bible\". The notes read the blood and "
    "water from the pierced side as the sacrificed Lamb and the Spirit. He reads "
    "scripture, by 1981, through the apparatus of a critical Catholic edition.",
    'I came across some strange notes in my Jerusalem Bible',
    '11 January 1981',
    note="The letter's dateline is misprinted \"Januaiy\" in the OCR, which is why "
         "our record has it as undated.")

let('PKB-LET-1981-AGAPE', 'LET_1981-01-12_PATRICIA_WARRICK_0027',
    'Letter to Patricia Warrick, January 12, 1981',
    'There is a very important note in the Jerusalem Bible', [520, 420],
    'PKB-PKT-TRANSLATIONS', 'definition',
    ['1 Corinthians', '1 John', 'Jerusalem Bible', 'Agape'],
    "The next day, still writing to Warrick, Dick quotes 1 John 4 on God's love "
    "sending his Son, then the Jerusalem Bible's note on 1 Corinthians 13:1: agape is "
    "attributed to God the Father, but being identical with God's nature it is in "
    "the Son, who loves the Father and the human race, and is the same love the "
    "Holy Spirit gives. Agape, the theme of 1 Corinthians 13, becomes by 1981 the "
    "centre of his theology.",
    'There is a very important note in the Jerusalem Bible on First Corinthians 13:1',
    '12 January 1981')

let('PKB-LET-1981-REVERSE', 'LET_1981-02-12_PATRICIA_WARRICK_0051',
    'Letter to Patricia Warrick, February 12, 1981',
    'VALIS, then, is the reverse of FLOW MY TEARS', [520, 520],
    'PKB-PKT-FICTION', 'comparison',
    ['Acts', 'Daniel', 'Flow My Tears', 'VALIS', "Jehovah's Witnesses"],
    "Dick contrasts his two novels: Flow My Tears is overtly political with a hidden "
    "religious stream drawn from Acts and Daniel, while VALIS looks theological but "
    "carries a covert message of violent revolution against the regime, preached as "
    "kerygma from God incarnate. Just before, he notes that the Jehovah's Witnesses "
    "share the apocalyptic hope but are passive — they stand and watch Jehovah "
    "destroy \"Rome\".",
    'there is a latent hidden esoteric religious stream',
    '12 February 1981')

ex('PKB-EX-1981-SECRET', 'SEG_EXEG_1981-04-16_Pat_04', S17,
   'The NEB 1 Cor phrases it', [520, 360],
   'PKB-PKT-TRANSLATIONS', 'comparison',
   ['1 Corinthians', 'Translations', 'YHWH', 'The Divine Invasion'],
   "Dick connects his vision of the Tetragrammaton with the words \"He has been "
   "transplanted and is alive\" — the vision behind The Divine Invasion — to Paul in "
   "1 Corinthians 2, and checks the New English Bible's rendering for the word he "
   "wants: \"I speak God's hidden wisdom, his secret purpose\". Secret, he says, is "
   "the word he was looking for; translation is how he finds it.",
   'Here is the word I was looking for.',
   '1981', 'folder', 'medium',
   note="Folder 90, which the Burroughs dossier places in 1981.")

ex('PKB-EX-1981-YHWH', 'SEG_EXEG_1981-04-16_Pat_169', S17,
   'The old King on horseback in "Tears" is YHWH', [360, 520],
   'PKB-PKT-WHICHGOD', 'definition',
   ['Exodus', 'Daniel', 'Revelation', 'YHWH', 'Flow My Tears', 'Which God'],
   "The old king on horseback in the Tears dream is YHWH, Dick now decides — which "
   "is why he saw Hebrew letters in 3-74. YHWH as judge and destroyer at the end of "
   "time is \"not the God of the N.T., the Xtian God of agape\" but the God whom "
   "Moses knew, and he finds The Divine Invasion already says that Valis is YHWH. "
   "In the next lines he calls VALIS a modern-day apocalyptic book, \"a fusion of "
   "Exodus & Daniel\".",
   'this is YHWH whom Moses knew.',
   'April 1981', 'record', 'high')

let('PKB-LET-1981-ARCHER', 'LET_1981-06-03_RUSSELL_GALEN_0088',
    'Letter to Russell Galen, June 3, 1981',
    'Tim Archer completely misuses the Bible', [520, 520],
    'PKB-PKT-FICTION', 'critique',
    ['The Transmigration of Timothy Archer', 'James Pike', 'Agape'],
    "Rereading the just-finished Transmigration of Timothy Archer, Dick tells his "
    "agent his view of it has changed. He had meant Bishop Archer, modelled on James "
    "Pike, as something of a Christ figure. Now he sees Archer misuse the Bible in "
    "the scene where Angel tries to talk him out of his affair: Archer uses scripture "
    "not as a man of God but as a lawyer, to justify his dishonest and carnal acts.",
    'for him Scripture becomes a basis by which he justifies his dishonest and carnal actions.',
    '3 June 1981')

let('PKB-LET-1981-STILLSMALL', 'LET_1981-08-08_KARL_M_RABENOLD_0121',
    'Letter to Karl M. Rabenold, August 8, 1981',
    'as the Bible says of Moses', [520, 340],
    'PKB-PKT-ELIJAH', 'definition', ['Exodus', '1 Kings', 'Elijah', 'Moses'],
    "Dick argues that through God we are unified with the world, so it ceases to be "
    "alien — otherwise man is, as Exodus says of Moses, \"a stranger in a strange "
    "land\". God is found in the small, trivial and discarded: he is the \"still small "
    "voice\" that spoke to Elijah. The voice from the junior-high radio serial is "
    "still his image of God in the last year of his life.",
    'he is the “still small voice” that spoke to Elijah.',
    '8 August 1981')

let('PKB-LET-1981-RETRIEVAL', 'LET_1981-09-30_PATRICIA_WARRICK_0170',
    'Letter to Patricia Warrick, September 30, 1981',
    'what emerges as the true and whole reality is the Judo-Christian apocalypsis', [520, 420],
    'PKB-PKT-FUTURE', 'definition',
    ['Daniel', 'Acts', 'Apocalypse', 'Golden fish'],
    "Late in 1981 Dick restates the theory in its most general form: a total reality "
    "is always theoretically available for retrieval, given an access key — for him, "
    "the Christian golden fish sign in February 1974. Fully retrieved, it is the "
    "Judeo-Christian apocalypse, the End Times world present at the time of Daniel, "
    "of Acts, now, and in the future. Christianity is a model, or a verbal and "
    "sacerdotal description, of that reality.",
    'it is always theoretically available for retrieval.',
    '30 September 1981')

let('PKB-LET-1981-CATS', 'LET_1981-10-01_CATHY_WORKMAN_0171',
    'Letter to Cathy Workman, October 1, 1981',
    'I read to them from the bible, all about the Last Days', [380, 260],
    'PKB-PKT-FUTURE', 'self_report', ['Revelation', 'Daniel', 'Apocalypse'],
    "A light letter. After a visit from friends, a lightning storm unlike any Los "
    "Angeles has seen terrifies his two cats, and Dick reads to them from Revelation "
    "and Daniel — the Last Days. \"They were suitably impressed.\" The apocalyptic "
    "books he spent seven years decoding, used as a joke months before his death.",
    'They were suitably impressed.',
    '1 October 1981')

let('PKB-LET-DILEXI', 'LET_UNDATED_DANIEL_GILBERT_0008',
    'Letter to Daniel Gilbert, undated — Selected Letters 1980–1982',
    'I have a great fondness for the word diligo', [200, 380],
    'PKB-PKT-TRANSLATIONS', 'self_report',
    ['Ephesians', 'Vulgate', 'Translations', 'Agape'],
    "A postscript answering a correspondent's Latin. Dick says he is fond of the verb "
    "diligo, to love, and especially of the one-word sentence \"Dilexi\" — I have "
    "loved — which he would like to sum up his life and to stand on his gravestone. "
    "He traces it to Jerome's Vulgate, Ephesians 5:1–2, and copies out the verse.",
    'I would like that word to sum up my life; I would like it on my grave­ stone.',
    'Undated (1980–82)', 'record', 'low')

# ==========================================================================
# 6. The essay and the interview
# ==========================================================================

doc('PKB-ESS-RASCH', 'interview', HOWTO,
    "\"How to Build a Universe That Doesn't Fall Apart Two Days Later\" (speech, 1978)",
    'my priest became progressively more agitated', [420, 620],
    'PKB-PKT-ACTS', 'self_report', ['Acts', 'Flow My Tears', 'Episcopal Church'],
    "The public version of the Acts story. Dick, an Episcopalian, describes to his "
    "priest the scene near the end of Flow My Tears in which Felix Buckman meets a "
    "black stranger at an all-night gas station. The priest grows agitated: it is a "
    "scene from Acts, where the man who meets the Ethiopian on the road is named "
    "Philip. He tells Dick to read Acts; Dick does, and agrees the resemblance is "
    "obvious.",
    'That is a scene from the Book of Acts, from the Bible!',
    'Philip K. Dick', '1978', 'dateline', 'high')

doc('PKB-ESS-JASON', 'interview', HOWTO,
    "\"How to Build a Universe That Doesn't Fall Apart Two Days Later\" (speech, 1978)",
    'In Acts, the high Roman official who arrests and interrogates Saint Paul is named Felix', [60, 920],
    'PKB-PKT-ACTS', 'self_report', ['Acts', 'Flow My Tears', 'King Felix'],
    "The puzzle deepens: the Roman official who interrogates Paul in Acts is Felix, "
    "the name of Dick's police general, and holds the same final authority. Dick "
    "then checks a Bible index for his protagonist's name, Jason, and finds a single "
    "Jason in the whole Bible, in Acts — sheltering a fugitive in his house, an exact "
    "inversion of the novel's Jason, a fugitive sheltered in someone else's.",
    'Well, a man named Jason appears once and only once in the Bible.',
    'Philip K. Dick', '1978', 'dateline', 'high')

# ==========================================================================
# 7. Scripture in the fiction (lane A: characters speak, not Dick)
# ==========================================================================

doc('PKB-FIC-UBIK', 'fiction', UBIK,
    'Ubik (1969), epigraph to chapter 17',
    'I am Ubik. Before the universe was, I am.', [40, 360],
    'PKB-PKT-FICTION', 'allegory', ['Gospel of John', 'Exodus', 'Ubik', 'Logos'],
    "The last of Ubik's chapter epigraphs, in which the product speaks as God. It "
    "fuses John 8:58 (\"Before Abraham was, I am\"), the creator's speech, the "
    "unspeakable name of Exodus 3, and John 1's Word. Written years before 2-3-74, "
    "it is the passage Dick later reads as proof that Ubik is the Logos and "
    "that Valis is Ubik.",
    'I am the word and my name is never spoken, the name which no one knows.',
    'Ubik (epigraph)', '1969', 'publication', 'high')

doc('PKB-FIC-SCANNER', 'fiction', FIVE,
    'A Scanner Darkly (1977)',
    'what that passage in the Bible means, Through a glass darkly', [520, 360],
    'PKB-PKT-FICTION', 'allegory', ['1 Corinthians', 'A Scanner Darkly'],
    "Bob Arctor, watching police psychologists sign off on his split brain, thinks of "
    "a contact print made with the negative reversed, and how short a time it takes "
    "to flip it back. He understands now what the Bible passage means — through a "
    "glass darkly — but understanding does not help him: his percept system is as "
    "damaged as ever. The title's verse, spoken inside the novel.",
    'I understand, he thought, what that passage in the Bible means, Through a glass darkly.',
    'Bob Arctor (narration)', '1977', 'publication', 'high')

doc('PKB-FIC-VALIS-EXEGESIS', 'fiction', VALIS3,
    'VALIS (1981), chapter 2',
    'His term was “exegesis,”', [200, 420],
    'PKB-PKT-FICTION', 'definition', ['Bible as code', 'VALIS', 'Living scripture'],
    "The narrator explains Horselover Fat's word for his journal: exegesis, a "
    "theological term for writing that explains a portion of scripture. Fat believed "
    "the information fired into his head had a holy origin and should be regarded "
    "as scripture. The novel names Dick's own eight-year project after the practice "
    "of commenting on the Bible — and makes the commentary itself scripture.",
    'His term was “exegesis,” a theological term meaning a piece of writing that explains or interprets a portion of scripture.',
    'Phil (narrator), on Horselover Fat', '1981', 'publication', 'high')

doc('PKB-FIC-VALIS-MALACHI', 'fiction', VALIS3,
    'VALIS (1981)',
    'There is a wonderful passage at the very end of the Old Testament', [380, 520],
    'PKB-PKT-ELIJAH', 'allegory', ['Malachi', 'VALIS', 'Healing'],
    "The narrator explains Fat's conviction that Jesus identified himself as Savior "
    "through healing miracles, and quotes Malachi 4:2 — the sun of righteousness "
    "rising with healing in his wings — the same verse Dick copies into the Exegesis "
    "in 1976. In the novel the verse sharpens Fat's despair: by his own system his "
    "dying friend Sherri should have been healed, and she is not.",
    'There is a wonderful passage at the very end of the Old Testament where this matter is clarified.',
    'Phil (narrator)', '1981', 'publication', 'high')

doc('PKB-FIC-VALIS-DANIEL', 'fiction', VALIS3,
    'VALIS (1981)',
    'Kevin began to comb through the two apocalyptic books of the Bible', [300, 760],
    'PKB-PKT-FUTURE', 'allegory', ['Daniel', 'VALIS', 'Empire', 'Richard Nixon'],
    "After the film Valis persuades them that the Empire may have ended with the "
    "fall of Ferris F. Fremount — Nixon — the cynic Kevin starts combing Daniel and "
    "Revelation for clues and finds in Daniel 8 a harsh, grim king, a master of "
    "stratagem, who will be broken \"not by human hands\". Fat is amused that the "
    "cynic has become a Bible scholar. The Exegesis' Daniel, given to a sceptic.",
    'Now Kevin had become a Bible scholar, to Fat’s amusement',
    'Phil (narrator)', '1981', 'publication', 'high')

doc('PKB-FIC-DI-HOLOGRAM', 'fiction', VALIS3,
    'The Divine Invasion (1981)',
    'the Bible expressed as layers at different depths within the hologram', [200, 760],
    'PKB-PKT-LIVING', 'allegory',
    ['Living scripture', 'The Divine Invasion', 'Bible as code', 'Elijah'],
    "The boy Emmanuel studies Elias's most precious possession: the Bible as a "
    "hologram, its layers set at depths according to age, a three-dimensional cosmos "
    "readable from any angle. Tilt the axis of observation and different messages "
    "come out, so Scripture yields an infinite, ceaselessly changing knowledge, "
    "colour-coded for the Trinity. The Exegesis' living, multi-layered scripture, "
    "built as an object.",
    'Thus Scripture yielded up an infinitude of knowledge that ceaselessly changed.',
    'Narrator', '1981', 'publication', 'high')

doc('PKB-FIC-DI-TORAH', 'fiction', VALIS3,
    'The Divine Invasion (1981)',
    'Zina said, “I am the Torah.”', [300, 420],
    'PKB-PKT-LIVING', 'allegory',
    ['Torah', 'Proverbs', 'The Divine Invasion', 'Hagia Sophia'],
    "In the primeval forest of Stanley Park, Emmanuel asks Zina who she is. \"I am "
    "the Torah\": the living, thinking plan and blueprint of the universe that God "
    "made in the beginning and cannot act against. Philo's living Torah, which Dick "
    "copied into the Exegesis, becomes a character — and, as the novel reveals, "
    "Holy Wisdom herself.",
    'You made me alive; I am a living being that thinks. I am the plan of the universe, its blueprint.',
    'Zina', '1981', 'publication', 'high')

doc('PKB-FIC-ARCHER-DIM', 'fiction', VALIS3,
    'The Transmigration of Timothy Archer (1982)',
    'This Bible, I saw, was the Jerusalem Bible.', [300, 520],
    'PKB-PKT-TRANSLATIONS', 'allegory',
    ['1 Corinthians', 'Jerusalem Bible', 'The Transmigration of Timothy Archer'],
    "Angel Archer reads past the point in Bishop Archer's open Bible where he "
    "stopped, a passage she knows in the King James but in a translation she has "
    "never seen — the Jerusalem Bible. Pointing to it she says that \"all we see is a "
    "dim reflection\"; Tim answers with faith, hope and love, \"the greatest of these "
    "is love\", as he leaves for a meeting. The Jerusalem Bible's rendering of the "
    "verse that titled A Scanner Darkly, used by a bishop to evade a moral question.",
    '“It says,” I said, putting my finger on the passage in his big Bible, “that all we see is a dim reflection.”',
    'Angel Archer (narrator)', '1982', 'publication', 'high',
    note="The novel's bibliography lists The Jerusalem Bible (Doubleday, 1966) — "
         "the edition Dick's 1981 letters to Warrick quote.")

doc('PKB-FIC-ARCHER-ANOKHI', 'fiction', VALIS3,
    'The Transmigration of Timothy Archer (1982)',
    'The word shows up in Exodus, chapter twenty, verse two', [360, 420],
    'PKB-PKT-LIVING', 'causal_theory',
    ['Exodus', 'Qumran & Nag Hammadi', 'The Transmigration of Timothy Archer', 'YHWH'],
    "The Zadokite fragments keep returning to a Hebrew noun, anokhi, and Tim Archer "
    "traces it to Exodus 20:2, where God himself speaks: \"I am the Lord thy God\". "
    "The unknown word in the new scrolls turns out to be the first-person pronoun of "
    "God in the Torah — the fictional counterpart of the Exegesis' search for the "
    "God of Moses.",
    'This is a terribly moving and important section of the Torah, for here God Himself speaks',
    'Angel Archer (narrator)', '1982', 'publication', 'high')

doc('PKB-FIC-DEUSIRAE', 'fiction', DEUS,
    'Deus Irae (1976, with Roger Zelazny)',
    'the Bible is a chronicle of God', [300, 520],
    'PKB-PKT-FICTION', 'definition', ['Genesis', 'Deus Irae', 'Which God'],
    "In the post-holocaust world of Deus Irae, Pete explains why he keeps going back "
    "toward danger: the authentic God of the Bible — not the cult's god of wrath, "
    "Carleton Lufteufel — is searching for man. The Bible is the chronicle of God's "
    "search for man, not man's for God. The separation is a quarrel so old the story "
    "is garbled, leaving God and man like Leibniz's windowless monads.",
    'the Bible is a chronicle of God’s search for man. Not man’s search for God.',
    'Pete', '1976', 'publication', 'high',
    note="Co-written with Roger Zelazny; attribution of any given passage to Dick "
         "is not certain.")

# ==========================================================================
# 8. Biography and scholarship (lanes C and D)
# ==========================================================================

doc('PKB-SCH-SUTIN-01', 'criticism', SUTIN,
    'Lawrence Sutin, Divine Invasions: A Life of Philip K. Dick (1989)',
    'Jung, Kant, William Burroughs, the Bible, the Dead Sea Scrolls', [300, 300],
    'PKB-PKT-SCHOLARS', 'definition', ['Prior knowledge', 'Qumran & Nag Hammadi'],
    "Sutin's introduction describes the range of Dick's reading as virtually "
    "limitless, from physics papers to Binswanger and Jung, and names the Bible and "
    "the Dead Sea Scrolls in the same breath as Burroughs and the Bhagavad Gita. The "
    "biographer places scripture in a lifelong reading, not a post-1974 conversion.",
    'Throughout his life the range of his reading was virtually limitless',
    'Lawrence Sutin', '1989', 'publication', 'high')

doc('PKB-SCH-SUTIN-02', 'criticism', SUTIN,
    'Lawrence Sutin, Divine Invasions: A Life of Philip K. Dick (1989)',
    'He also asked Rimov to join a Bible Club', [400, 300],
    'PKB-PKT-BEFORE', 'self_report', ['Prior knowledge'],
    "From a schoolfriend's recollection: in junior high Phil proclaimed himself an "
    "atheist because no one could prove God existed — and asked the same friend to "
    "join a Bible Club he was trying to found. The friend's verdict is that Phil was "
    "not religious but a devil's advocate, \"searching\". It corroborates the "
    "junior-high date Dick himself gives in 1981.",
    'He also asked Rimov to join a Bible Club he was attempting to found.',
    'Lawrence Sutin, reporting a schoolfriend', '1989', 'publication', 'high')

doc('PKB-SCH-BUTLER-01', 'criticism', BUTLER,
    'Andrew M. Butler, Philip K. Dick (Pocket Essentials, revised edition)',
    'which he had not previously read', [420, 260],
    'PKB-PKT-SCHOLARS', 'critique', ['Acts', 'Flow My Tears', 'Prior knowledge'],
    "Butler's biographical sketch of 1974: Dick convinced Orange County was also "
    "first-century Rome, and struck by parallels between the Acts of the Apostles — "
    "\"which he had not previously read\" — and Flow My Tears. Butler states as fact "
    "what Dick himself, in the Exegesis, leaves open.",
    '(which he had not previously read)',
    'Andrew M. Butler', None, None, None,
    note="Contrast PKB-EX-1978-UNCONSCIOUS, where Dick allows he may have read "
         "Acts earlier and forgotten it.")

doc('PKB-SCH-BUTLER-02', 'criticism', BUTLER,
    'Andrew M. Butler, Philip K. Dick (Pocket Essentials, revised edition)',
    'invocations of 1 Corinthians from', [380, 420],
    'PKB-PKT-SCHOLARS', 'definition', ['1 Corinthians', 'Empire'],
    "Introducing the recurring motifs he tracks novel by novel, Butler names one "
    "world underlying another — often first-century Rome under the present — and "
    "says it is explained sometimes by time manipulation and sometimes by invoking "
    "1 Corinthians, above all chapter 13 and \"through a glass, darkly\". He makes 1 "
    "Corinthians one of his standing headings for every book.",
    'especially chapter thirteen',
    'Andrew M. Butler', None, None, None)

doc('PKB-SCH-BUTLER-03', 'criticism', BUTLER,
    'Andrew M. Butler, Philip K. Dick (Pocket Essentials, revised edition)',
    'echoes a scene from Acts 17', [380, 360],
    'PKB-PKT-SCHOLARS', 'comparison', ['Acts', 'Flow My Tears'],
    "In his entry on Flow My Tears, Butler identifies the sources: Felix's dream of "
    "Jason's death echoes Acts 17, one of two Jasons in the Bible, and Felix is the "
    "name of the official who interrogates Paul. He notes that Dick saw this section "
    "as secret knowledge — a message, or part of his unforgetting.",
    'one of two Jasons in the Bible',
    'Andrew M. Butler', None, None, None,
    note="Butler counts two Jasons; Dick, in the 1978 speech, says Jason appears "
         "once and only once. Neither is resolved here.")

doc('PKB-SCH-TCS-01', 'criticism', TCS,
    'Machines Making Gods: Philip K. Dick, Henri Bergson and Saint Paul, Theory, '
    'Culture & Society 25 (2008)',
    'For now we see through a glass, darkly; but then face to face', [420, 360],
    'PKB-PKT-SCHOLARS', 'definition', ['1 Corinthians', 'Agape', 'Caritas'],
    "The essay argues that Dick regularly figures an illusory reality we struggle "
    "to see through by the \"glass, darkly\" passage of 1 Corinthians 13:12, and "
    "reads his habitual word caritas — the Latin of the verse that follows — as his "
    "name for empathy. Paul supplies both halves of the late Dick: impaired sight, "
    "and the love that answers it.",
    'Dick regularly alludes to this notion of the illusory reality',
    'Theory, Culture & Society essay', '2008', 'publication', 'high')

doc('PKB-SCH-TCS-02', 'criticism', TCS,
    'Machines Making Gods: Philip K. Dick, Henri Bergson and Saint Paul, Theory, '
    'Culture & Society 25 (2008), note 11',
    'discusses the parallels between Saint Paul', [80, 200],
    'PKB-PKT-SCHOLARS', 'comparison', ['Acts', 'Theophany'],
    "A footnote pointing to Gabriel McKee's discussion of the parallels between "
    "Paul's conversion on the road to Damascus, Acts 9:3–8 — a light from heaven, "
    "a voice, blindness — and Dick's visions of February 1974.",
    'conversion experience in the Book of Acts',
    'Theory, Culture & Society essay', '2008', 'publication', 'high')

doc('PKB-SCH-TSENG', 'criticism', TSENG,
    'Laurie Jui-hua Tseng, God and Human Beings in the Technologically-Mediated '
    'Living Condition: Philip K. Dick\'s Literary Theology in the VALIS Trilogy',
    'Contrasted with Elias', [520, 420],
    'PKB-PKT-SCHOLARS', 'critique',
    ['Living scripture', 'The Divine Invasion', 'Bible as code'],
    "Tseng reads Elias's holographic Bible in The Divine Invasion as scripture kept "
    "open and living, and sets it against the novel's Church, which wants to freeze "
    "the Bible and the Koran because a scripture that escapes from under the Church "
    "ends its monopoly. The open text is liberation; the frozen text, authority.",
    'the Church’s attempt to freeze the Bible and the Koran is apparently fascist and unjustifiable',
    'Laurie Jui-hua Tseng', None, None, None)

doc('PKB-SCH-EXTRAP', 'criticism', EXTRAP,
    'The Holy Family from Outer Space: Reconsidering Philip K. Dick\'s The Divine '
    'Invasion, Extrapolation 52.2 (2011)',
    'This bet is reminiscent of the Book of Job', [520, 300],
    'PKB-PKT-SCHOLARS', 'comparison', ['Job', 'The Divine Invasion', 'Hagia Sophia'],
    "Reading The Divine Invasion as a holy family transplanted to science fiction, "
    "the essay notes that Zina's wager with Emmanuel over Linda Fox recalls the bet "
    "between God and Satan in Job — except that Zina turns out to be not the "
    "Adversary but the lost part of God, Malkuth. Elsewhere it argues Dick knew the "
    "Bible too well to let the working title Valis Regained stand.",
    'This bet is reminiscent of the Book of Job in the Bible',
    'Extrapolation essay', '2011', 'publication', 'high')
