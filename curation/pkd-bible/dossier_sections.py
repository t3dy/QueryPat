#!/usr/bin/env python3
"""
The authored dossier "Philip K. Dick and the Bible": essay, browse facets,
card groups, contradictions, open questions and structured fields.

Kept as Python so the prose stays readable and diffable. build_dossier.py
writes it to dossier.json, which is what the seeder reads.

Citations in {{double braces}} are finding ids from findings.py. The seeder
refuses to build if one does not resolve, and checks every quotation of 40+
characters against the sources the dossier cites.

Registers: A = PKD's own words, B = primary-source fact, C = scholarly
argument, D = portal-editor inference.
"""

import re

TITLE = 'Philip K. Dick and the Bible'

SUBTITLE = ("How a reader who joked about rhyming the Bible came to treat it as a "
            "code, a living organism and a book of the future — and never settled "
            "which of its Gods he had met.")

CARD_DESCRIPTION = (
    "Dick's Bible, book by book: Acts and Flow My Tears, Daniel and the Empire, "
    "Malachi's Elijah, Holy Wisdom, scripture as code and as living information — "
    "76 sourced passages across the Exegesis, letters, novels and scholarship.")

SECTIONS = [

 {"id": "note", "heading": "Philip K. Dick and the Bible", "register": "D", "body": [
  "The Bible is the text Philip K. Dick argued with longest. He knew it before he "
  "believed anything about it: he dates his first reading to a junior-high radio "
  "serial about Elijah {{PKB-INT-ELIJAH}}, took the title of A Scanner Darkly from "
  "Paul in 1973 {{PKB-LET-1973B}}, and was comparing translations of Ecclesiastes and "
  "1 Corinthians five months before the experiences of February and March 1974 "
  "{{PKB-LET-1973C}}. After 2-3-74 it became the main instrument with which he tried "
  "to understand what had happened to him.",

  "What makes his use of it distinctive is not piety but method. He read scripture "
  "as a description of the present (\"The Bible is a book of the future\" "
  "{{PKB-LET-1975-CLAUDIA}}), as a cipher (\"The Bible is code\" "
  "{{PKB-EX-1976-ACTSPRISON}}), as a living organism — the esoteric Torah of Philo, "
  "the plasmate {{PKB-EX-1978-TORAH}} — and as a source his own novels had tapped "
  "without his knowing: Flow My Tears, he came to believe, reproduces the Acts of "
  "the Apostles {{PKB-ESS-RASCH}}. Each of these readings is held alongside the "
  "others, and several contradict each other. This page keeps them apart.",

  "The page is organised in two ways at once. The essay below runs roughly in "
  "order, from before 1974 to 1981. The index of books and themes underneath lets "
  "you go the other way: pick Acts, Daniel, Malachi or 1 Corinthians and see every "
  "passage in the archive that turns on it, whatever its date or source. Every "
  "bracketed reference in the essay opens the card it cites."]},

 {"id": "before", "heading": "Before 1974: a reader, not yet a believer",
  "register": "A", "body": [
  "Dick's own account starts in junior high school, with The Light of the World, a "
  "daytime radio dramatisation of the Bible. He came in during the Elijah episodes, "
  "went and read the story, and wanted above all to hear the voice Elijah hears on "
  "Mount Horeb {{PKB-INT-ELIJAH}}. A schoolfriend remembered the same years "
  "differently — an atheist who could not prove God existed and who also tried to "
  "start a Bible Club {{PKB-SCH-SUTIN-02}}. The two accounts agree on the date.",

  "The letters of the 1960s and early 1970s show a writer for whom the Bible is "
  "common property. In 1962 he describes coming out of years of agoraphobic "
  "misperception in Paul's words: he \"did see face to face\" {{PKB-LET-1962}}. In "
  "1964 the King James Bible is his example of a grand style that cannot make "
  "imitation serious {{PKB-LET-1964}}. In 1972–73 a dream about setting the Bible "
  "into rhymed couplets becomes a running joke with friends {{PKB-LET-1972}} "
  "{{PKB-LET-1973A}}.",

  "Two documents from 1973 show more than familiarity. In March he explains to "
  "Carol Carr that the title of the novel he is writing, A Scanner Darkly, is a pun "
  "on 1 Corinthians 13:12 {{PKB-LET-1973B}}. In September he sets three translations "
  "of 1 Corinthians 15:51 side by side for his agent and prefers the Jehovah's "
  "Witnesses' New World Translation as \"so direct, so—honest\" {{PKB-LET-1973C}}. "
  "Ubik, written years earlier, already ends its chapter epigraphs with a product "
  "that speaks as the Word of John's Gospel {{PKB-FIC-UBIK}}.",

  "This matters because Dick later said the opposite. In 1976 he told his mother "
  "that when he saw the Iron Empire in 1974 \"I was almost totally unfamiliar with "
  "the Bible\" {{PKB-LET-1976-HUDNER}}. The claim makes his visions independent of "
  "his reading; his own letters do not support it, at least for the Bible as a "
  "whole. The contradiction is recorded below rather than resolved."]},

 {"id": "acts", "heading": "1975: Acts and Flow My Tears", "register": "A", "body": [
  "The discovery that organised the rest arrived in 1975. Dick's earliest dated "
  "statement of it in this archive is a July letter to Göran Bengtson: Flow My Tears, "
  "the Policeman Said \"on close inspection, contains a number of passages evidently "
  "derived from or which refer to the\" Book of Acts, which he connects to a theory "
  "that his unconscious is an Attic Greek {{PKB-LET-1975-BENGTSON}}. To Claudia Bush "
  "he reads the novel's closing embrace between Felix Buckman and a black stranger "
  "as the Feast of Agape, and does not know how it got in {{PKB-LET-CLAUDIA-AGAPE}}.",

  "The public telling came in the 1978 speech How to Build a Universe That Doesn't "
  "Fall Apart Two Days Later. His Episcopalian priest, hearing the gas-station scene "
  "described, recognised it as Philip meeting the Ethiopian in Acts 8 "
  "{{PKB-ESS-RASCH}}. Dick then found Felix, the Roman official who interrogates "
  "Paul, and a single Jason sheltering a fugitive — an inversion of his own Jason "
  "Taverner {{PKB-ESS-JASON}}. In the Exegesis the name Felix becomes a key: it "
  "\"points to the Biblical nature of the dream\" {{PKB-EX-1975-FELIX}}.",

  "Over the following years the Acts parallel grows from coincidence into "
  "doctrine. Acts is \"a police state\" and \"how it really is\" "
  "{{PKB-EX-1976-ACTSPRISON}}; the canonical Acts \"leaves out crucial information\" "
  "that survives only in the novel {{PKB-EX-1976-OMITS}}; the recipient of the "
  "revelation lives in reality \"as interpreted through + by the Acts lens/grid\", "
  "a contemporary of Christ {{PKB-EX-1978-CONTEMPORARY}}. Dick himself allows that "
  "he may simply have read Acts and forgotten it {{PKB-EX-1978-UNCONSCIOUS}}."]},

 {"id": "future", "heading": "A book of the future: Daniel, Revelation and the Empire",
  "register": "A", "body": [
  "On 27 February 1975 Dick wrote the sentence that governs his apocalyptic reading: "
  "\"The Bible is a book of the future.\" The New Testament and the Old Testament "
  "oracles are \"about tomorrow\"; the backdrop is familiar, the events new "
  "{{PKB-LET-1975-CLAUDIA}}. Daniel and Revelation, \"the two apocalyptic books\", "
  "become the lens for the tyranny he believed he had seen thrown down in 1974.",

  "The identifications are explicit and they move. Revelation's beast is Rome, and "
  "its fall is the Parousia {{PKB-EX-1975-REVROME}}. With the Jehovah's Witnesses he "
  "reads Daniel's statue with feet of clay as the Anglo-American Empire {{PKB-EX-1975-CLAYFEET}}. "
  "By 1976 the scene is Cyrus's siege of Babylon, with Daniel the prisoner, and the "
  "equation runs Babylon = Rome = Washington DC = Moscow {{PKB-EX-1976-BABYLON}}. "
  "Apocalyptic vision, he argues, is a glimpse of eternal reality behind time, true "
  "\"in Daniel's time, in John's and mine\" {{PKB-EX-1975-APOC}}.",

  "He knew how this looked. In the same 1976 sitting he copies a sociological "
  "observation from the Britannica — only the alienated yearn for divine "
  "intervention — and adds: \"I fit this latter class\" {{PKB-EX-1976-ALIENATED}}. "
  "In VALIS the hunt for Nixon in Daniel is given to the cynic Kevin, to Fat's "
  "amusement {{PKB-FIC-VALIS-DANIEL}}. And in October 1981, during a lightning "
  "storm, he read Revelation and Daniel to his frightened cats {{PKB-LET-1981-CATS}}."]},

 {"id": "elijah", "heading": "Elijah, Malachi and the returning Spirit", "register": "A",
  "body": [
  "Malachi's last chapter promises that Elijah will be sent before the great and "
  "terrible day of the Lord. Dick used it more than any other prophetic text to "
  "name what possessed him. The Lord of Hosts suddenly coming to his temple is how "
  "he describes seeing the world as a living organism {{PKB-EX-1975-MALACHI}}; the "
  "Spirit of Elijah that Malachi promises is, he decides, \"the Old Testament Hebrew "
  "concept for the Christian Holy Spirit\" {{PKB-EX-1975-ELIJAH}}. In 1976 he quotes "
  "the sun of righteousness rising with healing in its wings — and reminds himself "
  "what Elijah did to Ahab {{PKB-EX-1976-SUN}}.",

  "The same verse appears in VALIS, where its promise of healing sharpens Fat's "
  "despair over his dying friend {{PKB-FIC-VALIS-MALACHI}}, and Elijah walks into "
  "The Divine Invasion as Elias Tate. In August 1981 the figure Dick reaches for is "
  "still the one from the radio serial: God as the \"still small voice\" that spoke "
  "to Elijah {{PKB-LET-1981-STILLSMALL}}."]},

 {"id": "wisdom", "heading": "Holy Wisdom from an apocryphal book", "register": "A",
  "body": [
  "Dick's St. Sophia — Holy Wisdom, Hagia Sophia, the figure who becomes Zina in "
  "The Divine Invasion — came to him through a book many Protestants do not "
  "count as scripture. In September 1975 he explains to a friend that his church "
  "now recommends the apocrypha, and that the Wisdom of Solomon, part of the "
  "Septuagint the early Christians used, \"was as sacred as any book of the Hebrew "
  "Scriptures\" {{PKB-EX-1975-SEPTUAGINT}}.",

  "From it he builds a theology of the Incarnation: Sophia, the world-builder of "
  "the wisdom books, entered human form and lost some of her powers while she was "
  "here {{PKB-EX-1975-WISDOM}}. By 1977 he identifies the voice in his head with "
  "\"the Logos, or St. Sophia, Holy Wisdom\" {{PKB-LET-1977-JAYNES}}; in 1981 "
  "Wisdom speaks in the novel as the living Torah, the blueprint of the universe "
  "{{PKB-FIC-DI-TORAH}}."]},

 {"id": "code", "heading": "The Bible is code", "register": "A", "body": [
  "The idea that scripture is a cipher appears first in fiction. In March 1975 Dick "
  "outlines a novel in which a man possessed by a Qumran Essene finds \"the New "
  "Testament is in cypher\" {{PKB-LET-1975-ORNSTEIN}}. By 1976 he states it about "
  "the world: the Bible \"isn't about the past; it's code to describe our world\", "
  "and Acts is now {{PKB-EX-1976-CODE}}. To decode it is to read the New Testament "
  "as \"an encoded instruction manual by which to become part of Valis\" "
  "{{PKB-EX-1976-MANUAL}}.",

  "The cipher has a structure. In one entry the testaments are opposing players: "
  "\"O.T. encodes + N.T. decyphers\", dark against light {{PKB-EX-1978-DECYPHER}}. "
  "And it is incomplete. The same Exegesis that calls the Bible code insists that "
  "Acts as canonised leaves out what Flow My Tears preserves {{PKB-EX-1976-OMITS}}. "
  "By 1981 Dick reads his own novels as two ciphers in opposite directions: Flow My "
  "Tears political on the surface with a hidden stream from Acts and Daniel, VALIS "
  "theological on the surface with a hidden political one {{PKB-LET-1981-REVERSE}}."]},

 {"id": "living", "heading": "Living scripture", "register": "A", "body": [
  "Early in 1975 Dick thought the Bible was dispensable: suppress it entirely and "
  "the experience it records would \"spring to life within given human minds once "
  "more\" {{PKB-LET-1975-WILLIAMS}}. He ended in the opposite place. Copying out "
  "Philo's image of the Torah as a living being, body the literal text and soul the "
  "hidden meaning, he exclaims: \"This is the Acts material, the living information "
  "I saw\" {{PKB-EX-1978-TORAH}}.",

  "The carriers of this living text are manuscripts that came out of the ground. "
  "Thomas, the personality he believed took him over, slumbered \"perhaps in a jar "
  "at Qumran\" {{PKB-EX-1976-QUMRAN}}; the huge open books he saw were the Qumran "
  "scrolls Bishop Pike saw, passed to him as plasmate {{PKB-EX-1978-SCROLLS}}; the "
  "Nag Hammadi codices may be \"the actual Secret Living\" blood of Christ "
  "{{PKB-EX-1978-NAGHAMMADI}}. The Logos of John's prologue is the bridge between "
  "text and organism, and Ubik's \"I am the word\" is the proof he finds in his own "
  "fiction {{PKB-EX-1978-UBIKWORD}}.",

  "The novels build the idea as objects. Elias's holographic Bible in The Divine "
  "Invasion yields different messages at every angle, \"an infinitude of knowledge "
  "that ceaselessly changed\" {{PKB-FIC-DI-HOLOGRAM}}; Zina declares \"I am the "
  "Torah\" {{PKB-FIC-DI-TORAH}}. Tseng reads the open, living scripture against the "
  "novel's Church, which wants to freeze it {{PKB-SCH-TSENG}}."]},

 {"id": "translations", "heading": "Which Bible: translations and editions",
  "register": "B", "body": [
  "Dick did not read one Bible. The archive shows him using at least five, and "
  "paying attention to their differences: the King James, whose cadence he took for "
  "granted {{PKB-LET-1964}} and a copy of which he gave his mother {{PKB-EX-1978-KJV}}; "
  "the Jehovah's Witnesses' New World Translation, which he preferred in 1973 "
  "{{PKB-LET-1973C}} and whose reading of Daniel he borrowed {{PKB-EX-1975-CLAYFEET}} "
  "while rejecting its theology of Christ {{PKB-EX-1978-MATTHEW}}; the New English "
  "Bible, which he quotes for John 10 {{PKB-LET-1975-KORMAN}} and checks for the word "
  "\"secret\" in 1 Corinthians 2 {{PKB-EX-1981-SECRET}}; the Jerusalem Bible, "
  "\"an official Catholic Bible\", whose notes he studies in 1981 "
  "{{PKB-LET-1981-BLOODWATER}} {{PKB-LET-1981-AGAPE}}; and Jerome's Vulgate, the "
  "source of the word he wanted on his gravestone, Dilexi {{PKB-LET-DILEXI}}.",

  "He also read through intermediaries: the Septuagint's apocrypha "
  "{{PKB-EX-1975-SEPTUAGINT}}, The Decoded New Testament's esoteric glosses on the "
  "Crucifixion {{PKB-EX-1975-DECODED}}, and reference books on Exodus when a "
  "television drama got Passover wrong {{PKB-LET-1975-CBS}}. The last novel's "
  "bibliography cites the Jerusalem Bible, and its narrator notices the change of "
  "translation in a bishop's hands {{PKB-FIC-ARCHER-DIM}}."]},

 {"id": "whichgod", "heading": "Which God?", "register": "A", "body": [
  "Dick never decided which God of the Bible he had met, and his answers are "
  "incompatible. In 1977 he tells Julian Jaynes it was \"not so much the creator god "
  "of our Bible\" as Plato's arranger {{PKB-LET-1977-JAYNES}}. Reading the Nag "
  "Hammadi codices, he concludes that Palmer Eldritch, explicitly the Christian God "
  "of that novel, is the Gnostics' blind demiurge {{PKB-EX-1978-YALTABAOTH}}. Late "
  "in 1980 it is the Cosmic Christ of John, distinct from the human Jesus, and its "
  "nature is agape {{PKB-EX-1980-COSMICCHRIST}}.",

  "In April 1981 he reverses that: the king on horseback in the Tears dream is YHWH, "
  "judge and destroyer, \"not the God of the N.T., the Xtian God of agape\" but the "
  "God whom Moses knew, and VALIS is \"a fusion of Exodus & Daniel\" "
  "{{PKB-EX-1981-YHWH}}. Two years earlier the same figure was the young king, "
  "Christ as judge, of Daniel and Revelation {{PKB-EX-1978-YOUNGKING}}. The last "
  "novel gives the question to scholarship: the mysterious word in the Zadokite "
  "scrolls is anokhi, God's \"I\" in Exodus 20 {{PKB-FIC-ARCHER-ANOKHI}}."]},

 {"id": "fiction", "heading": "Scripture in the novels", "register": "A", "body": [
  "The fiction uses the Bible in two ways, and the difference matters. Overtly, "
  "characters quote and argue: Pete in Deus Irae calls the Bible \"a chronicle of "
  "God's search for man\" {{PKB-FIC-DEUSIRAE}}; Fat's journal is an exegesis because "
  "it treats his revelations as scripture {{PKB-FIC-VALIS-EXEGESIS}}; Bob Arctor "
  "understands the \"glass darkly\" verse and cannot be helped by it "
  "{{PKB-FIC-SCANNER}}. These are characters speaking, not Dick.",

  "Covertly, on Dick's own later account, the novels carried scripture he did not "
  "know he had put there — Acts in Flow My Tears, the Logos in Ubik. That is a claim "
  "about the novels made from outside them, and the page keeps it in Dick's lane, "
  "not the fiction's. He could also turn on his own scripture-quoting characters: "
  "rereading The Transmigration of Timothy Archer, he decided its bishop uses the "
  "Bible \"not as a man of God but as a lawyer\" {{PKB-LET-1981-ARCHER}}."]},

 {"id": "scholars", "heading": "What scholars say", "register": "C", "body": [
  "Sutin places the Bible and the Dead Sea Scrolls in a lifelong, \"virtually "
  "limitless\" range of reading {{PKB-SCH-SUTIN-01}}. Butler makes 1 Corinthians a "
  "standing heading in his survey of every novel {{PKB-SCH-BUTLER-02}}, traces "
  "Felix and Jason to Acts 17 {{PKB-SCH-BUTLER-03}}, and states that Dick had not "
  "previously read Acts {{PKB-SCH-BUTLER-01}}. An essay in Theory, Culture & Society "
  "reads the \"glass, darkly\" verse and its sequel, caritas, as the two halves of "
  "Dick's late thought {{PKB-SCH-TCS-01}}, and points to work comparing Paul's "
  "conversion in Acts 9 with February 1974 {{PKB-SCH-TCS-02}}. Tseng and the "
  "Extrapolation essay read The Divine Invasion's open Bible and its Job-like wager "
  "{{PKB-SCH-TSENG}} {{PKB-SCH-EXTRAP}}."]},

 {"id": "cautions", "heading": "What this page does not claim", "register": "D", "body": [
  "It does not claim that Dick's scriptural readings are correct, or that the "
  "coincidences he found in Flow My Tears are more than coincidences. It reports "
  "what he wrote and what others have written, in separate lanes: the fiction is "
  "characters speaking, the Exegesis and letters are Dick, the scholarship is "
  "scholars.",

  "Dates are given per passage with the evidence for them. Exegesis section 016 "
  "carries a container date of October 1978 that its own passages contradict; "
  "passages from it are dated 1978–80 unless a stamp or folder places them more "
  "precisely. The 348 machine-extracted \"claims\" about the Bible in our database "
  "are unreviewed and are not used here; every card on this page was chosen and "
  "summarised by reading the passage, and every quotation is checked verbatim "
  "against its source before the page is built."]},
]


# --------------------------------------------------------------------------
# Browse configuration: how the mention cards are grouped and faceted.
# --------------------------------------------------------------------------

GROUPS = [
    {'key': 'before', 'label': 'Before 1974',
     'blurb': 'Letters from before the experiences of February and March 1974.'},
    {'key': 'ex1975', 'label': 'The Exegesis — 1975',
     'blurb': 'The first frame: Malachi, Daniel, Revelation, Holy Wisdom.'},
    {'key': 'ex1976', 'label': 'The Exegesis — 1976–79',
     'blurb': 'The cipher: the Bible as code, Acts as now.'},
    {'key': 'ex1978', 'label': 'The Exegesis — 1978–80',
     'blurb': 'Living scripture: the Torah, Qumran, Nag Hammadi, the Cosmic Christ.'},
    {'key': 'ex1981', 'label': 'The Exegesis — 1981',
     'blurb': 'YHWH, and the secret wisdom of 1 Corinthians 2.'},
    {'key': 'letters', 'label': 'Letters, 1975–1981',
     'blurb': 'Dick explaining his Bible to someone else.'},
    {'key': 'speech', 'label': 'Speech and interview',
     'blurb': 'The public telling of the Acts story, and the radio serial about Elijah.'},
    {'key': 'fiction', 'label': 'In the fiction',
     'blurb': 'Characters speaking — not Dick.'},
    {'key': 'scholarship', 'label': 'Biography and scholarship',
     'blurb': 'What Sutin, Butler and others say — not Dick.'},
]


def group_of(source_type: str, dated: str | None) -> str:
    """Which GROUPS key a card belongs to, from its source and its date."""
    dated = dated or ''
    if source_type == 'interview':
        return 'speech'
    if source_type == 'fiction':
        return 'fiction'
    if source_type == 'criticism':
        return 'scholarship'
    if source_type == 'letter':
        years = [int(y) for y in re.findall(r'19\d\d', dated)]
        return 'before' if years and max(years) < 1974 else 'letters'
    if '1981' in dated:
        return 'ex1981'
    if '1978' in dated or '1980' in dated:
        return 'ex1978'
    if '1976' in dated:
        return 'ex1976'
    return 'ex1975'

# Facets are the browsable vocabulary of the card `concepts`. `link` points at
# the portal page for the facet where one exists.
FACETS = [
    # Books of the Bible, in canonical order
    {'label': 'Genesis', 'kind': 'book'},
    {'label': 'Exodus', 'kind': 'book'},
    {'label': '1 Kings', 'kind': 'book'},
    {'label': '2 Kings', 'kind': 'book'},
    {'label': 'Job', 'kind': 'book'},
    {'label': 'Psalms', 'kind': 'book'},
    {'label': 'Proverbs', 'kind': 'book'},
    {'label': 'Ecclesiastes', 'kind': 'book'},
    {'label': 'Wisdom of Solomon', 'kind': 'book', 'link': '/dictionary/wisdom'},
    {'label': 'Daniel', 'kind': 'book', 'link': '/dictionary/daniel'},
    {'label': 'Malachi', 'kind': 'book', 'link': '/dictionary/malachi'},
    {'label': 'Matthew', 'kind': 'book'},
    {'label': 'Gospel of John', 'kind': 'book', 'link': '/dictionary/john'},
    {'label': 'Acts', 'kind': 'book', 'link': '/dictionary/acts'},
    {'label': '1 Corinthians', 'kind': 'book'},
    {'label': 'Ephesians', 'kind': 'book'},
    {'label': '1 John', 'kind': 'book'},
    {'label': 'Revelation', 'kind': 'book', 'link': '/dictionary/revelation'},
    {'label': 'Torah', 'kind': 'book', 'link': '/dictionary/torah'},
    # Themes
    {'label': 'Bible as code', 'kind': 'theme'},
    {'label': 'Living scripture', 'kind': 'theme'},
    {'label': 'Prior knowledge', 'kind': 'theme'},
    {'label': 'Apocalypse', 'kind': 'theme'},
    {'label': 'Empire', 'kind': 'theme', 'link': '/dictionary/empire'},
    {'label': 'Elijah', 'kind': 'theme', 'link': '/dictionary/elijah'},
    {'label': 'Hagia Sophia', 'kind': 'theme', 'link': '/dictionary/hagia-sophia'},
    {'label': 'Which God', 'kind': 'theme'},
    {'label': 'YHWH', 'kind': 'theme', 'link': '/names/yhwh'},
    {'label': 'Logos', 'kind': 'theme', 'link': '/dictionary/logos'},
    {'label': 'Agape', 'kind': 'theme'},
    {'label': 'Plasmate', 'kind': 'theme', 'link': '/dictionary/plasmate'},
    {'label': 'Qumran & Nag Hammadi', 'kind': 'theme', 'link': '/dictionary/qumran'},
    {'label': "Jehovah's Witnesses", 'kind': 'theme'},
    # Translations and editions
    {'label': 'Translations', 'kind': 'edition'},
    {'label': 'King James Version', 'kind': 'edition'},
    {'label': 'Jerusalem Bible', 'kind': 'edition'},
    {'label': 'Septuagint', 'kind': 'edition'},
    {'label': 'Vulgate', 'kind': 'edition'},
    {'label': 'The Decoded New Testament', 'kind': 'edition'},
    # Dick's works
    {'label': 'Flow My Tears', 'kind': 'work',
     'link': '/exegesis/works/flow-my-tears-the-policeman-said'},
    {'label': 'Ubik', 'kind': 'work', 'link': '/exegesis/works/ubik'},
    {'label': 'A Scanner Darkly', 'kind': 'work', 'link': '/exegesis/works/a-scanner-darkly'},
    {'label': 'Palmer Eldritch', 'kind': 'work',
     'link': '/exegesis/works/the-three-stigmata-of-palmer-eldritch'},
    {'label': 'Deus Irae', 'kind': 'work', 'link': '/exegesis/works/deus-irae'},
    {'label': 'VALIS', 'kind': 'work', 'link': '/exegesis/works/valis'},
    {'label': 'The Divine Invasion', 'kind': 'work',
     'link': '/exegesis/works/the-divine-invasion'},
    {'label': 'The Transmigration of Timothy Archer', 'kind': 'work'},
]

FACET_KINDS = [
    ('book', 'Books of the Bible'),
    ('theme', 'Themes'),
    ('edition', 'Translations and editions'),
    ('work', "Dick's works"),
]

BROWSE_INTRO = (
    "{n} passages in the archive turn on the Bible. Each card summarises the whole "
    "passage and where it sits, then quotes the sentence it turns on; every "
    "quotation is machine-checked against the underlying text before the page is "
    "published. Pick a book, theme, translation or novel to see only the passages "
    "about it, or a lane to see only one kind of source.")


# --------------------------------------------------------------------------
# Contradictions: (summary, explanation, type, fragment_a, fragment_b).
# The fragments locate the two passages; the seeder refuses to drop one silently.
# --------------------------------------------------------------------------

CONTRADICTIONS = [
    ("In 1976 Dick says he was \"almost totally unfamiliar with the Bible\" when he "
     "saw the Iron Empire in 1974; his letters of 1962–73 quote, translate and "
     "title a novel from it.",
     "The 1976 claim makes the visions of Daniel's and Revelation's Empire "
     "independent of his reading. Against it: a junior-high reading of the Elijah "
     "story, the 1 Corinthians title of A Scanner Darkly (March 1973), and a "
     "comparison of three translations of 1 Corinthians 15 (September 1973). He may "
     "have meant the apocalyptic books specifically; the letter does not say so.",
     'self_vs_critic',
     'almost totally unfamiliar with the Bible',
     'this Jehovah’s Witnesses version is better'),

    ("Had Dick read Acts before writing Flow My Tears? He allows he may have read it "
     "and forgotten; Butler states he had not.",
     "In the Exegesis Dick concedes the Acts parallels could come from a forgotten "
     "reading and rests his case on the Taverner material instead. Butler's survey "
     "states as fact that Acts was something \"he had not previously read\". The "
     "secondary claim is stronger than the primary one.",
     'self_vs_critic',
     'unconsciously I knew the Book of Acts',
     'which he had not previously read'),

    ("In January 1975 the Bible is dispensable — its truth would spring up again if "
     "it were lost. By 1978 the text itself is alive.",
     "To Paul Williams the Christian experience is a priori and independent of sacred "
     "texts. By the time he copies out Philo on the living Torah, the text is an "
     "organism — the Acts material, the plasmate. The two views are never "
     "reconciled; the later one does not retract the earlier.",
     'early_vs_late',
     'even if the Bible itself were totally suppressed',
     'This is the Acts material, the living information I saw'),

    ("The Bible is the code — and the Bible is incomplete without Flow My Tears.",
     "The same section of the Exegesis that calls the Bible a code describing our "
     "world also says that Acts as canonised leaves out crucial information, which "
     "survives in the novel's dream. On the second view the scripture is not the "
     "cipher but one damaged copy of it.",
     'interpretive',
     "it's code to describe our world",
     'leaves out crucial information'),

    ("Which God? Not the Bible's creator (1977); the Cosmic Christ whose nature is "
     "agape (1980); YHWH, \"not the God of the N.T.\" (1981).",
     "Three incompatible identifications of the same experience, each stated with "
     "confidence. The April 1981 entry explicitly sets the God of Moses against the "
     "Christian God of agape that the late-1980 entry had just embraced.",
     'early_vs_late',
     'not so much the creator god of our Bible',
     'this is YHWH whom Moses knew'),

    ("Dick meant Bishop Archer as a Christ figure; rereading the novel, he decided "
     "Archer uses scripture as a lawyer.",
     "In the novel Archer meets Angel's \"dim reflection\" with faith, hope and love, "
     "and leaves. In June 1981 Dick tells his agent he had intended a Christ figure "
     "and now sees a man justifying himself from the Bible. Author against "
     "author, over the same scene.",
     'fiction_vs_exegesis',
     'that all we see is a dim reflection',
     'Tim Archer completely misuses the Bible'),

    ("One Jason in the Bible, or two?",
     "In the 1978 speech Dick says a man named Jason appears once and only once in "
     "the Bible, in Acts. Butler speaks of one of two Jasons. A small factual "
     "disagreement, left as the sources state it.",
     'factual',
     'In Acts, the high Roman official',
     'one of two Jasons in the Bible'),
]


OPEN_QUESTIONS = [
    "Which Bible did Dick own before 1974? — raised under Before 1974. Letters show "
    "the King James, the New World Translation and the New English Bible by 1973, "
    "but no inventory of his books survives in this archive. Resolvable by: an "
    "inventory of his library.",
    "Did Dick know Acts before 1974? — raised under 1975. He allows a forgotten "
    "reading; Butler denies any reading. Resolvable by: pre-1974 letters outside the "
    "Selected Letters, or annotations in his own Bible.",
    "Was the Wisdom of Solomon letter of September 1975 sent to more than one "
    "person? — the same text is recorded once in the Exegesis (\"Dear Doris\") and "
    "once in the Selected Letters (\"Dear Sherri\"). Resolvable by: the original "
    "manuscripts.",
    "What is Dick's source for Philo's living Torah? — raised under Living "
    "scripture. He copies a passage in quotation marks without naming the book. "
    "Resolvable by: identifying the quotation, likely an encyclopedia article on "
    "Kabbalah or Philo.",
    "Which Exegesis passages in section 016 belong to 1978, and which to 1980? — "
    "raised under the cautions. Resolvable by: matching each segment to the "
    "folders of the published edition.",
    "The Book of Acts is traditionally ascribed to Luke; Dick calls it \"Paul's\". "
    "Slip, or a reading? — raised under 1975. Unresolved.",
]

RELATED_THINKERS = [
    'Paul', 'Philo of Alexandria', 'Jerome', 'Gene Savoy', 'James A. Pike',
    'Julian Jaynes', 'Plato', 'James George Frazer', 'Lawrence Sutin',
    'Andrew M. Butler', 'Laurie Jui-hua Tseng', 'Gabriel McKee',
]

FIELDS = {
    'definition': (
        "Philip K. Dick's engagement with the Bible across his life: a familiar text "
        "before 1974, then, after the experiences of February and March 1974, the "
        "principal framework through which he interpreted them — read as a book of "
        "the future, a cipher, a living organism, and a source his own novels had "
        "unknowingly reproduced."),
    'pkd_relevance': (
        "No text appears more often in the Exegesis or does more work there. Acts, "
        "Daniel, Revelation, Malachi, the Wisdom of Solomon, John and 1 Corinthians "
        "each supply a structural idea: the Empire, Elijah's return, Holy Wisdom, "
        "the Logos, impaired sight and agape."),
    'in_the_fiction': (
        "Overtly in VALIS, The Divine Invasion, The Transmigration of Timothy Archer "
        "and Deus Irae; by Dick's later account covertly in Flow My Tears (Acts), "
        "Ubik (the Logos) and A Scanner Darkly (1 Corinthians 13)."),
    'in_the_exegesis': (
        "From 1975 to 1981: the Bible as a book of the future, as code, as living "
        "information, and as the record of which God he had met."),
    'intellectual_background': (
        "The Septuagint and its apocrypha; Philo's allegorical Torah; the Dead Sea "
        "Scrolls and Nag Hammadi codices; the Jehovah's Witnesses' apocalyptic "
        "reading of Daniel; modern esoteric readings such as The Decoded New "
        "Testament."),
    'scholarly_debate': (
        "Whether Dick knew Acts before 1974; how far 1 Corinthians 13 structures the "
        "fiction; the open versus the frozen scripture of The Divine Invasion."),
    'chronology_summary': (
        "Junior high: the Elijah radio serial. 1962–73: Corinthians, King James, "
        "rhymed couplets, the Scanner Darkly title, comparing translations. 1975: "
        "Acts and Flow My Tears; the Bible as a book of the future; the Wisdom of "
        "Solomon. 1976: the Bible as code. 1978–80: living scripture. 1981: YHWH; "
        "the Jerusalem Bible."),
    'contradictions_summary': (
        "Seven, kept rather than resolved: his prior knowledge of the Bible; whether "
        "he had read Acts; the Bible dispensable or alive; code or incomplete code; "
        "which God; Bishop Archer as Christ figure or lawyer; one Jason or two."),
    'editorial_notes': (
        "Every card was chosen and summarised by reading the passage. Machine-"
        "extracted claims about the Bible in the database are unreviewed and not "
        "used. Fiction passages are characters speaking (lane A); the Exegesis is "
        "lane B; scholarship lane C; biography lane D; letters and interviews lane "
        "E."),
}
