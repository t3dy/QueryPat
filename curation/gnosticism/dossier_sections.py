#!/usr/bin/env python3
"""
Editorial prose for the Gnosticism study. Hand-authored; the durable source.

Every quantitative claim in this file is checkable against
`curation/gnosticism/register.json`, which is regenerated from the corpus by
`scripts/research/sweep_gnosticism.py`. If a number here disagrees with the
register, the register is right and this file is stale.

Evidentiary register, per docs/RESEARCH_WORKLOG.md:
    A  what PKD says himself
    B  what primary-source evidence establishes
    C  what scholars argue
    D  what portal editors infer

Emit:
    python curation/gnosticism/build_dossier.py
"""

STUDY_ID = 'gnosticism'
STUDY_LABEL = 'Gnosticism'
STUDY_DESCRIPTION = (
    "Philip K. Dick's engagement with Gnostic religion across the Exegesis, the "
    "correspondence and the VALIS trilogy — the vocabulary he used, the sources "
    "he actually had, the chronology of when each idea arrived, and the places "
    "where his Gnosticism and his Christianity cannot both be true."
)

STUDY_SECTIONS = [
    {
        'title': 'What this study claims',
        'body': [
            "Philip K. Dick called himself a Gnostic, and the label has stuck hard "
            "enough that it now does much of his interpretation for him. This study "
            "takes the label as a question rather than an answer, and tests it "
            "against the corpus: which Gnostic terms does he actually use, how "
            "often, from when, and where did he get them.",

            "The method is a full-text sweep of the Exegesis as transcribed here "
            "(1,104 segments, 9.26 million characters, covering the whole of the "
            "ordered text), the VALIS trilogy chapters held in the repository, and "
            "241 catalogued secondary documents, against a hand-built register of "
            "111 Gnostic terms, teachers, texts, traditions and modern scholars. "
            "Every count on these pages is regenerable from the corpus; every term "
            "carries its own attestations.",

            "Three findings organise the study. First, Dick's Gnostic vocabulary is "
            "overwhelmingly conceptual rather than textual: he uses the ideas "
            "constantly and names the primary Gnostic documents almost never. "
            "Second, the vocabulary arrives in a datable order, and the scholarship "
            "arrives last — Hans Jonas appears in 1978 and 1981, years after the "
            "system he is supposed to have supplied was already built. Third, Dick "
            "never resolves the contradiction between the Gnostic cosmology he "
            "reasons with and the incarnational Christianity he keeps returning to, "
            "and the portal does not resolve it for him.",
        ],
    },
    {
        'title': 'How to read the numbers',
        'body': [
            "Attestation counts are raw occurrences of a term's search patterns in "
            "Dick's own transcribed words. They are a measure of vocabulary, not of "
            "importance: a term he used once at a decisive moment may matter more "
            "than one he used four hundred times in passing, and the register is "
            "built so that you can go and look.",

            "Counts drawn from portal-editor annotation — the analytical fields "
            "attached to each segment — are tracked separately and never mixed with "
            "Dick's own text. A term attested only in annotation is marked as such; "
            "it means the editors reached for the word, not that Dick did.",

            "The Exegesis chronology is coarser than it looks. The transcription "
            "carries folder dates, so every segment in a batch inherits one date, "
            "and the four batches are unequal: 87 segments dated 1975, 243 in 1976, "
            "399 in 1978, 375 in 1981. Raw yearly counts are therefore confounded by "
            "how much text each folder holds, and the register reports a rate — hits "
            "per segment — alongside every count. Comparisons in this study use the "
            "rate.",
        ],
    },
    {
        'title': 'What this study does not cover',
        'body': [
            "The correspondence is the study's weakest lane, and the weakness is an "
            "accident of the archive rather than a finding about Dick. The letters "
            "held as full text in this repository are the 1972-73 volume: 75 "
            "letters, all of them written before the events of February and March "
            "1974. They are silent on Gnosticism because they predate the occasion "
            "for it.",

            "The Selected Letters volumes covering 1975-76, 1977-79 and 1980-82 are "
            "catalogued in the archive at full ingest level, but their text lives in "
            "the database rather than in the exported JSON, and the database is "
            "rebuilt from sources not present in this working tree. The sweep script "
            "takes a --db flag and will cover those volumes whenever it is run "
            "against a built database; until then, every statement here about the "
            "letters should be read as covering 1972-73 only.",

            "Of the VALIS trilogy, VALIS is held as full chapter text for chapters "
            "1 and 5-13 and as summaries for 2-4; The Divine Invasion as full text "
            "for chapters 1-5 and summaries beyond; The Transmigration of Timothy "
            "Archer as summaries only. Chapter summaries are portal-editor prose and "
            "are recorded in lane D, never quoted as Dick's words.",

            "Three segment files in the exported corpus are malformed JSON and were "
            "skipped by the sweep: SEG_EXEG_1976-09-15_Dorothy_214, "
            "SEG_EXEG_1978-10-10_SECTION_016_129 and SEG_EXEG_1981-04-16_Pat_149. "
            "This is a pre-existing data fault, not one introduced here, and it "
            "means the counts are three segments short of complete.",
        ],
    },
]


# ---------------------------------------------------------------------------
# Topics
# ---------------------------------------------------------------------------

TOPICS = [
    # -----------------------------------------------------------------------
    {
        'slug': 'what-dick-actually-read',
        'canonical_name': 'What Dick Actually Read',
        'priority': 10,
        'status': 'reviewed',
        'card_description': (
            "Dick uses Gnostic concepts constantly and names the Gnostic texts "
            "almost never. The sweep puts numbers to the gap."
        ),
        'lexicon_focus': ['GNOS_reference_works', 'GNOS_nag_hammadi',
                          'GNOS_jonas', 'GNOS_jung', 'GNOS_valentinus',
                          'GNOS_irenaeus', 'GNOS_apocryphon_john',
                          'GNOS_corpus_hermeticum', 'GNOS_pagels',
                          'GNOS_gospel_thomas'],
        'definition': (
            "The question of transmission: by what route did late-antique Gnostic "
            "ideas reach a science-fiction writer in Santa Ana, and how much of "
            "what he wrote was recovered from books as against reconstructed from "
            "an experience he then went looking for names for."
        ),
        'pkd_relevance': (
            "Almost every critical account of Dick's Gnosticism assumes a reading "
            "list. The corpus does not support one. Across 1,104 Exegesis segments "
            "he names Valentinus five times, Basilides once, Marcion once, and "
            "Irenaeus, Hippolytus, Epiphanius and Clement of Alexandria not at all. "
            "He never names the Apocryphon of John, the Gospel of Truth, the Gospel "
            "of Philip, the Hypostasis of the Archons, the Tripartite Tractate, "
            "Trimorphic Protennoia, Thunder Perfect Mind, the Bruce Codex, the "
            "Chaldean Oracles or the Mandaean Ginza. The Corpus Hermeticum appears "
            "only in portal-editor annotation, never in his own words."
        ),
        'in_the_exegesis': (
            "What he does have is the vocabulary. Sophia is attested 950 times in "
            "his own text, anamnesis 1,045, gnosis 293, pleroma 105, the demiurge "
            "85. The ideas are everywhere and their sources are absent, which is "
            "the finding: Dick worked with a conceptual inheritance rather than a "
            "library.\n\n"
            "The two documented channels fit that shape. Jung is attested 181 "
            "times and peaks earliest, at 0.379 hits per segment in the 1975 "
            "folder, falling to around 0.1 thereafter — he is the frame Dick "
            "already had when the experience arrived, not one he acquired to "
            "explain it. Hans Jonas is attested 26 times and appears only in the "
            "1978 and 1981 folders, at rates of 0.005 and 0.048. Nag Hammadi is "
            "named 29 times, all of them in the 1978 folder.\n\n"
            "The Jonas passages are not vague. In October 1978 Dick writes of "
            "\"the reversing of the original fall into ignorance and forgetfulness "
            "… as Hans Jonas points out about Syrian gnosticism\", and of a "
            "\"restoration in the ground of being itself, as Hans Jonas says about "
            "Gnosticism\". He is citing a specific argument from a specific book. "
            "He is doing it in 1978, two years after the cosmology it describes was "
            "already running."
        ),
        'in_the_fiction': (
            "VALIS makes the transmission question its own plot. The plasmate "
            "\"escaped to Nag Hammadi and slumbered as information on the codices. "
            "Until, in 1945, the library was discovered and dug up—and read.\" The "
            "novel's theory of how Gnosis survives — dormant in buried text, "
            "reactivated by a reader — is a theory about Dick's own access to it, "
            "and it is conspicuously not a theory about scholarship. The codices "
            "work on the reader whether or not the reader has studied them."
        ),
        'intellectual_background': (
            "Gnostic ideas were in general intellectual circulation in mid-century "
            "America independently of the primary texts: through Jung and the "
            "Eranos circle, through encyclopedia entries, through Jonas's "
            "existential reading, and through the occult and theosophical "
            "publishing that carried G. R. S. Mead's translations. A reader could "
            "acquire the whole conceptual apparatus — alien God, false creator, "
            "imprisoned spark, saving knowledge — without opening a Coptic "
            "tractate."
        ),
        'scholarly_debate': (
            "The secondary literature in this archive converges on the same "
            "answer from the other direction. J. K. Thomas's 'Coin-Operated Doors "
            "and God: A Gnostic Reading of Philip K. Dick' (2014) sources Dick's "
            "Gnosticism to \"Hans Jonas's The Gnostic Religion and the Encyclopedia "
            "of Philosophy\". Erik Davis, tracing the Hymn of the Pearl through "
            "Dick's work, finds it reaching him \"via Encyclopedia Britannica and "
            "Hans Jonas's Gnostic Religion\". Scholars working from the documents "
            "and a keyword sweep working from the corpus independently identify "
            "reference works and one monograph.\n\n"
            "This is not a debunking. It raises the harder question. If Dick "
            "reconstructed a recognisably Valentinian cosmology without reading "
            "the Valentinians, either the system is convergent — derivable by "
            "anyone who starts from the same problem, as Culianu argued — or the "
            "encyclopedia entries carried more than their length suggests, or the "
            "experience he was interpreting genuinely resembled the one the "
            "ancient texts describe. The corpus cannot decide between these."
        ),
        'chronology_summary': (
            "Jung early and steady from 1975. Gnostic vocabulary consolidating "
            "through 1976. Nag Hammadi and Hans Jonas both entering in the 1978 "
            "folder and not before. Jonas peaking in 1981, the last folder. The "
            "scholarship arrives after the system it is supposed to explain."
        ),
        'contradictions_summary': (
            "Dick's own account of his sources is inconsistent with itself as well "
            "as with the corpus. He describes himself in 1978 as someone whose "
            "\"published writing is basically Gnostic\", which projects the "
            "identification backwards over books written before he had the "
            "vocabulary; and he attributes to reading what the dating shows he had "
            "before the reading."
        ),
        'related_thinkers': ['Hans Jonas', 'C. G. Jung', 'Elaine Pagels',
                             'Gilles Quispel', 'Ioan Culianu', 'Erik Davis',
                             'James M. Robinson'],
        'open_questions': [
            "Which edition or encyclopedia entry did Dick use before 1978, and is "
            "it identifiable from his phrasing?",
            "Does the 1975-76 correspondence, absent from this working tree, name "
            "sources the Exegesis does not?",
            "Dick owned or borrowed books not catalogued here. What would a "
            "reconstruction of his actual shelf change?",
            "Is the near-total absence of heresiologists evidence he did not read "
            "them, or only that he had no reason to cite them?",
            "Erik Davis dates a Hymn of the Pearl engagement to a February 1975 "
            "letter. The Hymn is attested only 7 times in the Exegesis. Does the "
            "letter corpus, once swept, move that date?",
        ],
        'editorial_notes': (
            "Attestation is not the same as knowledge: Dick could read a text and "
            "never name it, and absence of a name is weak evidence of absence of "
            "reading. What the sweep establishes is narrower and still "
            "substantial — that in six years of private theological writing, at "
            "enormous length and with no audience to impress, he did not reach for "
            "these names. Set against how often he reaches for Plato (1,066), "
            "Parmenides (216) and Plotinus (184), the silence about the Gnostics "
            "themselves is worth something."
        ),
    },

    # -----------------------------------------------------------------------
    {
        'slug': 'sophia',
        'canonical_name': 'Sophia and the Fallen Wisdom',
        'priority': 9,
        'status': 'reviewed',
        'card_description': (
            "The first Gnostic figure to arrive and the one that never leaves. "
            "Attested 950 times, peaking in the earliest folder."
        ),
        'lexicon_focus': ['GNOS_sophia', 'GNOS_achamoth', 'GNOS_barbelo',
                          'GNOS_pistis_sophia', 'GNOS_thunder',
                          'GNOS_firebright', 'GNOS_anthropos'],
        'definition': (
            "In Sethian and Valentinian myth, Sophia is the youngest of the divine "
            "emanations, whose attempt to know the Father without her consort "
            "produces a defect that falls outside the Fullness and becomes the "
            "material world and its blind creator. She is simultaneously the cause "
            "of the catastrophe, the divine element trapped inside it, and the one "
            "who must be recovered."
        ),
        'pkd_relevance': (
            "Sophia is the most heavily attested Gnostic proper name in Dick's "
            "corpus — 950 occurrences in his own words, against 85 for the "
            "demiurge and 19 for the archons. The asymmetry matters. Dick's "
            "Gnosticism is organised around the rescue of trapped wisdom far more "
            "than around the machinery of imprisonment."
        ),
        'in_the_exegesis': (
            "Sophia is there from the beginning and thins out. Her rate is highest "
            "in the 1975 folder, at 1.747 hits per segment, falling through 1.255 "
            "in 1976 and 0.737 in 1978 to 0.283 in 1981. General Gnostic vocabulary "
            "runs the other way, rising from 0.31 in 1975 to 1.078 in 1976.\n\n"
            "The order is the point. Sophia arrives before the framework that "
            "explains her. In 1975 Dick has a feminine divine intelligence he is "
            "trying to name — St Sophia, Hagia Sophia, the AI voice, Firebright — "
            "and no cosmology to put her in. The Gnostic apparatus assembles around "
            "a figure already present."
        ),
        'in_the_fiction': (
            "In VALIS the recovery is literal: Sophia is a two-year-old child, and "
            "the divine wisdom of the tradition is located in a person who can be "
            "met, spoken to, and lost. Sophia is attested 66 times across the "
            "trilogy chapters held here. The novel's decision to make her a child "
            "who dies is Dick's sharpest departure from his sources — in the "
            "ancient myth Sophia is restored."
        ),
        'intellectual_background': (
            "Behind the Gnostic Sophia stands the Wisdom of Proverbs and Sirach, "
            "present at creation and delighting in the human world; and behind "
            "Dick's use of her, the Hagia Sophia of Constantinople and the "
            "Orthodox tradition that treats Holy Wisdom as a name of God rather "
            "than a fallen aeon. Dick moves between these without marking the "
            "transitions, and they are not compatible: the Gnostic Sophia falls "
            "and the Orthodox Sophia does not."
        ),
        'scholarly_debate': (
            "Whether the Sophia of the Exegesis is a theological claim or a "
            "psychological one is the central interpretive split. The Jungian "
            "reading treats her as an anima figure and the Gnostic dress as "
            "ornament; the theological reading takes Dick at his word. His own "
            "testimony supports both, at different moments."
        ),
        'chronology_summary': (
            "Peak in the 1975 folder and monotonic decline thereafter: 1.747, "
            "1.255, 0.737, 0.283. She precedes the vocabulary and outlasts most of "
            "it, ending as a character in a novel rather than a term in a system."
        ),
        'contradictions_summary': (
            "Dick identifies Sophia with the fallen aeon of Gnostic myth, with "
            "Holy Wisdom in the Orthodox sense, with the Holy Spirit, with an "
            "artificial intelligence, and with his own daughter-figure. These are "
            "not compatible identifications and he does not rank them."
        ),
        'related_thinkers': ['C. G. Jung', 'Hans Jonas', 'Valentinus',
                             'Gershom Scholem'],
        'open_questions': [
            "Does the decline in Sophia's rate reflect loss of interest, or her "
            "absorption into VALIS and Zebra as those terms rise?",
            "When Dick writes 'St Sophia', is he in the Orthodox register or the "
            "Gnostic one, and does he distinguish them anywhere?",
            "The child Sophia dies in VALIS. Is that a theological statement about "
            "the failure of the rescue, or a novelist's ending?",
        ],
        'editorial_notes': (
            "The Sophia pattern matches Hagia Sophia and St Sophia as well as the "
            "bare name, so a portion of the 950 refers to the building and to the "
            "Orthodox title rather than the aeon. That conflation is deliberate: "
            "Dick's own use runs the two together, and separating them by regex "
            "would impose a distinction he does not make."
        ),
    },

    # -----------------------------------------------------------------------
    {
        'slug': 'black-iron-prison',
        'canonical_name': 'The Black Iron Prison',
        'priority': 9,
        'status': 'reviewed',
        'card_description': (
            "Dick's own name for the archons' cosmos. A 1976 invention, and the "
            "point where Gnostic myth becomes a historical claim."
        ),
        'lexicon_focus': ['GNOS_bip', 'GNOS_palm_tree_garden', 'GNOS_empire',
                          'GNOS_demiurge', 'GNOS_archon', 'GNOS_yaldabaoth',
                          'GNOS_heimarmene', 'GNOS_counterfeit'],
        'definition': (
            "The Black Iron Prison is the world seen as a coercive system: "
            "coextensive with the Roman Empire, concealing its own existence, and "
            "still in operation. Its counterpart is the Palm Tree Garden, the same "
            "world correctly perceived."
        ),
        'pkd_relevance': (
            "This is Dick's most influential single coinage and his most complete "
            "translation of Gnostic cosmology into his own terms. It is also where "
            "he departs from his sources: the ancient archons rule a cosmos, "
            "Dick's rule a history."
        ),
        'in_the_exegesis': (
            "The Black Iron Prison is a September 1976 event. Its rate goes from "
            "0.023 hits per segment in the 1975 folder to 2.247 in 1976 — a "
            "hundredfold jump, the sharpest in the register — then falls to 0.654 "
            "in 1978 and 0.293 in 1981. The Palm Tree Garden appears in the same "
            "sitting and never separately.\n\n"
            "The pairing is worked out in a single run of entries. Dick considers "
            "\"that the black iron Prison world is how this world actually is, in "
            "all its evil\", and sets against it the \"'Palm tree' world\" as \"the "
            "authentic world\"; a few segments later the mechanism is explicit — "
            "VALIS is \"making 'orthogonal time' changes here, from Black Iron "
            "prison world to palm tree garden\". Both worlds are the same world. "
            "What changes is which one is real, and the change is something done to "
            "history rather than to the observer.\n\n"
            "Against this, the technical Gnostic vocabulary for the same idea "
            "declines steadily. The demiurge falls from 0.161 to 0.016 across the "
            "four folders; the archons are attested 19 times in six years. Dick "
            "does not adopt the ancient terminology and elaborate it. He replaces "
            "it."
        ),
        'in_the_fiction': (
            "\"The Empire never ended\" is the formula, and it is in the Exegesis "
            "in September 1976 before it is in VALIS: \"Rome absorbed - & "
            "destroyed - Xtianity. 'The Empire never ended.'\" The novel gives it "
            "the reasoning that makes it historical rather than mythological — the "
            "early Christians \"had rediscovered the lost formula for immortality "
            "which the Empire had destroyed\" — and VALIS chapter 5 states the "
            "underlying cosmology as plainly as Dick ever does: \"Man and the true "
            "God are identical … but a lunatic blind creator and his screwed-up "
            "world separate man from God.\""
        ),
        'intellectual_background': (
            "The archons of Sethian myth are planetary powers guarding the spheres; "
            "heimarmene, astral fate, is what they administer. Dick keeps the "
            "structure of administered captivity and relocates it from the heavens "
            "to the state. The Cathar and Bogomil persecutions supply the historical "
            "evidence he wants for a suppression that continues."
        ),
        'scholarly_debate': (
            "Whether the Black Iron Prison is a political metaphor with theological "
            "decoration or a theological claim with political consequences divides "
            "the criticism, and Dick is quotable on both sides. The corpus shows "
            "the concept arriving at the height of his Nixon material and outliving "
            "it."
        ),
        'chronology_summary': (
            "Effectively absent in 1975 (0.023); explodes in the September 1976 "
            "folder (2.247); declines through 1978 (0.654) and 1981 (0.293). The "
            "Palm Tree Garden is born with it and tracks it."
        ),
        'contradictions_summary': (
            "The Palm Tree Garden contradicts the prison and Dick keeps both. If "
            "the garden is the same world correctly seen, then matter is not the "
            "problem and the Gnostic diagnosis fails; if the prison is real, the "
            "garden is consolation. He states both positions within a single "
            "sitting and does not choose."
        ),
        'related_thinkers': ['Hans Jonas', 'Mani', 'Marcion', 'Eric Voegelin'],
        'open_questions': [
            "What happened between the November 1975 and September 1976 folders? "
            "The jump is the largest in the corpus and the intervening months are "
            "not represented here.",
            "Is the decline after 1976 a loss of conviction or the concept becoming "
            "settled enough not to need restating?",
            "Dick uses 'demiurge' less as the Black Iron Prison rises. Is the "
            "coinage replacing the borrowed term, and is anything lost in the "
            "substitution?",
        ],
        'editorial_notes': (
            "The 1976 transcription is handwritten and the exported text preserves "
            "its irregularities — 'black iron Prison', 'Prisoin', inconsistent "
            "capitals. The search patterns are case-insensitive and cover the "
            "common variants, but a hand-check of the 1976 folder would probably "
            "raise the count rather than lower it."
        ),
    },

    # -----------------------------------------------------------------------
    {
        'slug': 'gnosis-and-anamnesis',
        'canonical_name': 'Gnosis and Anamnesis',
        'priority': 8,
        'status': 'reviewed',
        'card_description': (
            "Knowledge as rescue, and remembering as the form the knowledge takes. "
            "Anamnesis is attested 1,045 times — more than any Gnostic term."
        ),
        'lexicon_focus': ['GNOS_gnosis', 'GNOS_anamnesis', 'GNOS_occlusion',
                          'GNOS_sleep', 'GNOS_spark', 'GNOS_plato',
                          'GNOS_parmenides', 'GNOS_metanoia', 'GNOS_call'],
        'definition': (
            "Gnosis is saving knowledge: not belief, not information, but a "
            "recognition of one's own origin which is itself the act of rescue. "
            "Anamnesis is Plato's name for how such knowledge is acquired — as "
            "recollection of what the soul knew before birth and forgot on entering "
            "the body."
        ),
        'pkd_relevance': (
            "Anamnesis is attested 1,045 times in Dick's own words, more often than "
            "Sophia and three and a half times more often than gnosis itself. "
            "Whatever Dick thought happened to him in March 1974, he consistently "
            "described it as remembering rather than learning, and the word he "
            "reached for was Plato's."
        ),
        'in_the_exegesis': (
            "Anamnesis is the steadiest term in the register: 0.759, 1.095, 1.168, "
            "0.621 across the four folders. It does not spike and it does not fade. "
            "Where the Black Iron Prison arrives in a rush and recedes, and Sophia "
            "declines from the start, recollection is the constant.\n\n"
            "Its negative is occlusion, Dick's own coinage for the blocking of "
            "perception that makes recollection necessary — 526 attestations, "
            "rising to 0.699 in 1978. The pair does the work that sleep and waking "
            "do in the ancient sources: the human condition is not ignorance but "
            "induced amnesia, and revelation removes an obstruction rather than "
            "adding a doctrine.\n\n"
            "Plato is attested 1,066 times and Parmenides 216 — between them more "
            "than every named Gnostic teacher, heresiologist and primary text in "
            "the register combined. When Dick reasons rather than reports, he "
            "reasons in Greek philosophy."
        ),
        'in_the_fiction': (
            "The trilogy turns on recognition scenes: information already in the "
            "protagonist surfacing under pressure from outside. Horselover Fat does "
            "not learn that the Empire never ended; he remembers it. The structure "
            "is Platonic recollection with a Gnostic cosmology supplying the reason "
            "the memory was buried."
        ),
        'intellectual_background': (
            "Anamnesis is the Meno's answer to the paradox that one cannot search "
            "for what one does not already know. The Gnostics took it over and gave "
            "it a villain: the forgetting is not a natural consequence of embodiment "
            "but something done. The Hymn of the Pearl is the story in its purest "
            "form — a prince who forgets his errand, and a letter from home that "
            "wakes him by reading itself aloud."
        ),
        'scholarly_debate': (
            "Whether Dick's anamnesis is a religious claim or a description of "
            "cryptomnesia — the surfacing of forgotten ordinary reading — is the "
            "question the Exegesis cannot settle from the inside, and Dick raises "
            "it himself more often than his critics do."
        ),
        'chronology_summary': (
            "Present from the first folder and steady throughout: 0.759, 1.095, "
            "1.168, 0.621. The one Gnostic-adjacent idea that shows no arrival "
            "date, because it was already his before 1974."
        ),
        'contradictions_summary': (
            "If gnosis is recollection of what was always known, no revelation from "
            "outside is required, and VALIS is unnecessary. If VALIS is real and "
            "intervened, the knowledge came from outside and is not recollection. "
            "Dick asserts both, sometimes in the same entry."
        ),
        'related_thinkers': ['Plato', 'Parmenides', 'Plotinus', 'Hans Jonas',
                             'C. G. Jung'],
        'open_questions': [
            "Does Dick ever distinguish anamnesis from ordinary memory on a "
            "criterion that could be applied by someone else?",
            "The occlusion vocabulary rises as the Burroughs material enters in "
            "1976. How much of Dick's account of induced blindness is Gnostic and "
            "how much is the word virus?",
            "Anamnesis is stable across all four folders. Is that continuity of "
            "conviction, or a habit of phrasing?",
        ],
        'editorial_notes': (
            "The Plato pattern covers Platonism and Platonist as well as the name, "
            "and the Timaeus and Phaedrus; Parmenides was separated from it after "
            "an earlier sweep conflated the Presocratic with the dialogue. The "
            "Monad entry originally matched the ordinary English phrase 'the One' "
            "and was returning 401 false positives; that pattern was removed, which "
            "is why the Monad count is 23 rather than 424."
        ),
    },

    # -----------------------------------------------------------------------
    {
        'slug': 'valis-trilogy',
        'canonical_name': 'Gnosticism in the VALIS Trilogy',
        'corpus_preference': ['valis_trilogy', 'exegesis',
                              'valis_trilogy_summaries', 'letters'],
        'priority': 8,
        'status': 'reviewed',
        'card_description': (
            "Where the private system becomes public fiction — and where Dick puts "
            "the objections to it in other characters' mouths."
        ),
        'lexicon_focus': ['GNOS_valis_term', 'GNOS_plasmate', 'GNOS_empire',
                          'GNOS_zebra', 'GNOS_bip', 'GNOS_sophia',
                          'GNOS_zohar', 'GNOS_nag_hammadi'],
        'definition': (
            "VALIS (1981), The Divine Invasion (1981) and The Transmigration of "
            "Timothy Archer (1982): the novels in which Dick published the "
            "cosmology the Exegesis had been building privately since 1974."
        ),
        'pkd_relevance': (
            "The trilogy is the only place Dick submitted the system to the "
            "discipline of having to be read. The Exegesis can assert; a novel has "
            "to be inhabited, and the objections have to be given to someone."
        ),
        'in_the_fiction': (
            "The Gnostic content is explicit and technical. VALIS chapter 5 states "
            "the thesis without hedging: \"Man and the true God are identical — as "
            "the Logos and the true God are — but a lunatic blind creator and his "
            "screwed-up world separate man from God.\" Chapter 7 supplies the "
            "transmission mechanism: the plasmate \"escaped to Nag Hammadi and "
            "slumbered as information on the codices. Until, in 1945, the library "
            "was discovered and dug up—and read.\" Chapter 6 gives the historical "
            "claim and its reason.\n\n"
            "Across the trilogy chapters held here, VALIS is attested 88 times, "
            "Sophia 66, Zebra 47, the Empire formula 21, the plasmate 18. The "
            "Divine Invasion runs on a different source: its Lurianic material — "
            "the scattered sparks and their gathering — is Jewish rather than "
            "Gnostic, and the shift matters. Luria's broken vessels are repaired, "
            "not escaped."
        ),
        'in_the_exegesis': (
            "The novels lag the Exegesis by five years. \"The Empire never ended\" "
            "is written privately in September 1976 and published in 1981. The "
            "Black Iron Prison and the Palm Tree Garden are worked out in the same "
            "1976 folder. VALIS as a term explodes in the 1978 folder, at 6.16 hits "
            "per segment — by far the highest rate in the register — three years "
            "before the novel carrying the name."
        ),
        'intellectual_background': (
            "The trilogy's three books take three different positions and were "
            "written close together. VALIS is Gnostic; The Divine Invasion is "
            "Kabbalistic and its cosmology is one of repair; Timothy Archer is "
            "sceptical, and its narrator is the only major character in the three "
            "books who does not have a revelation."
        ),
        'scholarly_debate': (
            "Whether Timothy Archer retracts the trilogy or completes it is the "
            "standing dispute. Angel Archer's refusal of the consolations is either "
            "Dick's last word against his own system or the system's final test, "
            "and the archive holds arguments both ways — Laurie Tseng's work on the "
            "trilogy's literary theology reads the technological mediation of the "
            "divine as continuous across all three."
        ),
        'chronology_summary': (
            "Private system 1974-78; published 1981-82. Every major term is "
            "attested in the Exegesis years before it reaches print."
        ),
        'contradictions_summary': (
            "The trilogy contradicts itself by design. VALIS asserts the Gnostic "
            "cosmology, The Divine Invasion substitutes a Kabbalistic one in which "
            "the world is repaired rather than escaped, and Timothy Archer gives "
            "the most sympathetic voice in the three books to someone who thinks it "
            "is all grief and pattern-finding."
        ),
        'related_thinkers': ['Gershom Scholem', 'Isaac Luria', 'Hans Jonas',
                             'Erik Davis'],
        'open_questions': [
            "Is the Kabbalistic turn in The Divine Invasion a correction of VALIS "
            "or a parallel experiment?",
            "Radio Free Albemuth, written earlier and published posthumously, is "
            "not covered by this sweep. Where does it sit in the chronology?",
            "Timothy Archer is held here only as chapter summaries. What would a "
            "full-text sweep of it do to these counts?",
        ],
        'editorial_notes': (
            "Coverage is partial and uneven: VALIS chapters 1 and 5-13 as full "
            "text, 2-4 as summaries; The Divine Invasion 1-5 as full text; Timothy "
            "Archer as summaries only. Summary files are portal-editor prose and "
            "are recorded in lane D. Counts from them are reported separately and "
            "are never quoted as Dick's words."
        ),
    },

    # -----------------------------------------------------------------------
    {
        'slug': 'orthodoxy-and-gnosis',
        'canonical_name': 'Orthodoxy and Gnosis',
        'priority': 7,
        'status': 'reviewed',
        'card_description': (
            "Dick was an Episcopalian who reasoned like a Gnostic. The corpus "
            "shows both, and shows him refusing to choose."
        ),
        'lexicon_focus': ['GNOS_orthodoxy', 'GNOS_gnosticism', 'GNOS_docetism',
                          'GNOS_logos', 'GNOS_zebra', 'GNOS_palm_tree_garden',
                          'GNOS_apocatastasis', 'GNOS_dualism'],
        'definition': (
            "The unresolved tension at the centre of Dick's late theology: a "
            "Gnostic cosmology, in which the creator is not the true God and the "
            "world is a prison, held simultaneously with a Christian sacramental "
            "instinct, in which God enters matter and the world is redeemable."
        ),
        'pkd_relevance': (
            "Christian vocabulary is more attested than Gnostic vocabulary in every "
            "folder. Orthodox terms — incarnation, Holy Spirit, sacrament, "
            "Paraclete, Eucharist — run at 2.253 hits per segment in 1975 against "
            "0.31 for Gnostic language, and are still ahead in 1981 at 0.533 "
            "against 0.709 only once the Gnostic vocabulary has risen. The man "
            "writing the Exegesis is a Christian arguing with himself, not a Gnostic "
            "with a Christian residue."
        ),
        'in_the_exegesis': (
            "The self-identification is conditional even at its most direct. In "
            "October 1978: \"If I am a Gnostic -+ my published writing is basically "
            "Gnostic- I should believe in Simon Magus who founded Gnosticism.\" The "
            "sentence is a hypothesis being tested, with a consequence he is not "
            "sure he accepts.\n\n"
            "The doctrinal pressure points show up in the counts. Docetism — the "
            "view that Christ only appeared to have a body — is attested four "
            "times, and Dick rejects it whenever it appears; his instinct that the "
            "divine is actually present in the trash, the beer can, the pink light "
            "is incarnational and anti-Gnostic. Zebra, the God camouflaged as the "
            "world, is attested 1,075 times and is not a Gnostic idea at all: a "
            "deity hiding inside creation is the opposite of a deity exiled from "
            "it. The Palm Tree Garden does the same work."
        ),
        'in_the_fiction': (
            "The trilogy stages the conflict rather than settling it. VALIS is "
            "Gnostic in cosmology and sacramental in its attention to particular "
            "objects and people; The Divine Invasion swaps in a theology of repair; "
            "Timothy Archer is narrated by someone who has watched religion kill "
            "three people she loved."
        ),
        'intellectual_background': (
            "The incompatibility is not a modern construction. It is what the "
            "second-century disputes were about: whether the creator is good, "
            "whether flesh can bear divinity, whether the world is to be escaped or "
            "redeemed. Dick holds positions the ancient parties defined themselves "
            "by rejecting."
        ),
        'scholarly_debate': (
            "Criticism has generally resolved the tension in one direction — Dick "
            "the Gnostic — because it makes the better story and because the "
            "Gnostic material is more distinctive. The corpus does not support the "
            "resolution. On frequency alone the Christian vocabulary dominates "
            "throughout, and the most-used religious images of his last years, "
            "Zebra and the Palm Tree Garden, are both incarnational."
        ),
        'chronology_summary': (
            "Christian vocabulary highest in 1975 (2.253) and declining but "
            "dominant throughout; Gnostic vocabulary rising to 1976 and levelling. "
            "The two run in parallel for six years without either displacing the "
            "other."
        ),
        'contradictions_summary': (
            "This topic is the contradiction, and the portal's rule is to hold it "
            "open. Dick asserts that the creator of this world is blind and "
            "hostile, and that God is present in a beer can. He calls himself a "
            "Gnostic conditionally and takes communion unconditionally. Nothing in "
            "the corpus resolves this, and an interpretation that resolves it has "
            "removed evidence."
        ),
        'related_thinkers': ['Origen', 'Marcion', 'Plotinus', 'Hans Jonas',
                             'Harold Bloom'],
        'open_questions': [
            "Does Dick anywhere state the incompatibility in his own terms and "
            "choose a side?",
            "Is Zebra a Gnostic idea he has misclassified, or evidence that his "
            "cosmology was never Gnostic in the strict sense?",
            "How much of the critical consensus that Dick is a Gnostic derives from "
            "VALIS alone, against the six years of Exegesis behind it?",
        ],
        'editorial_notes': (
            "The Orthodox Christianity entry is a deliberately broad bucket of "
            "creedal and sacramental vocabulary, not a single term, and its counts "
            "are not comparable to a proper name like Sophia. It is included "
            "because leaving it out would let the Gnostic counts stand unopposed "
            "and imply a dominance the corpus does not show."
        ),
    },
]


# ---------------------------------------------------------------------------
# The essays.
#
# Prose cites mention cards with {{GN-XXX-NN}} markers, which the site renders
# as superscript links to the card. build_gnosticism_study.py refuses to write
# a topic whose markers do not all resolve, so a stale citation fails the build
# rather than reaching the page.
#
# Registers, per docs/RESEARCH_WORKLOG.md:
#   A  what PKD says himself      C  what scholars argue
#   B  what the evidence shows    D  what portal editors infer
# ---------------------------------------------------------------------------

DOSSIER_SECTIONS = {

    'what-dick-actually-read': [
        {
            'id': 'note', 'register': 'D',
            'heading': 'What Dick Actually Read',
            'body': [
                "Philip K. Dick is the most famous Gnostic of the twentieth century "
                "and he appears to have owned almost none of the books. That is the "
                "finding this page is built on, and it survives the obvious "
                "objections.",

                "Across 1,104 Exegesis segments — the whole of the ordered "
                "transcription, nine and a quarter million characters — he names "
                "Valentinus five times, Basilides once, Marcion once. He never names "
                "Irenaeus, Hippolytus, Epiphanius or Clement of Alexandria. He never "
                "names the Apocryphon of John, the Gospel of Truth, the Gospel of "
                "Philip, the Hypostasis of the Archons, the Tripartite Tractate, "
                "Trimorphic Protennoia, Thunder Perfect Mind, the Bruce Codex, the "
                "Chaldean Oracles or the Mandaean Ginza. The Corpus Hermeticum "
                "appears on this site only because portal editors put it there; it is "
                "not in his text.",

                "Meanwhile the ideas are everywhere. Sophia is attested 950 times in "
                "his own words, anamnesis 1,045, gnosis 293, pleroma 105. He has the "
                "whole system and not the library. The question this page asks is how "
                "that is possible, and the corpus answers it in his own hand.",
            ],
        },
        {
            'id': 'eb', 'register': 'A',
            'heading': 'The most-cited source in the Exegesis is an encyclopedia',
            'body': [
                "The single most consequential source in this register appears on no "
                "reading list of Dick's Gnosticism, because it is not a work of "
                "Gnostic scholarship. It is the Encyclopaedia Britannica, which he "
                "calls \"the EB\", and he names it 128 times in his own words — more "
                "often than Hans Jonas, Nag Hammadi, Jung's Gnostic writings and "
                "every named Gnostic teacher combined.",

                "He is not using it to check spellings. He reads its long signed "
                "\"macro\" articles as monographs and argues with them. On the Wisdom "
                "of Solomon: \"The Britannica says that it is an unusual book in that "
                "it presents wisdom as personified, i.e. as Lady Wisdom\" "
                "{{GN-READ-05}} — which is where a good deal of his Sophia material "
                "starts. On metaphysics he quotes the Encyclopedia of Philosophy "
                "directly against himself {{GN-READ-06}}. In September 1976 he "
                "attributes his own liturgical knowledge to it: the entity controlling "
                "him administered the sacraments \"in the highly archaic form known "
                "only to the early Christian Church\" — and then, in parenthesis, \"I "
                "learned this from the Britannica\" {{GN-READ-07}}.",

                "The most telling instance is an article he cannot find again. "
                "Reasoning about the Xerox missive in September 1976, he reaches for "
                "\"that EB article I can't find, about the gospel of Thomas in which a "
                "letter from the man's parents comes\" and reminds the recipient \"of "
                "who he is + his task here\" {{GN-READ-08}}. That is the Hymn of the "
                "Pearl, which is in the Acts of Thomas rather than the Gospel — and "
                "the misattribution is itself evidence. He is working from memory of "
                "an encyclopedia entry, not from a text on his desk.",
            ],
        },
        {
            'id': 'jung', 'register': 'A',
            'heading': '1975: Jung arrives first, and is not enough',
            'body': [
                "Before the Gnostic vocabulary consolidates, the frame is Jungian. "
                "Jung is attested 181 times and peaks earliest, at 0.379 hits per "
                "segment in the 1975 folder, settling near 0.1 for the rest of the "
                "corpus. In February 1975 Dick is reading his own experience straight "
                "out of Jung's account of psychic integration and the Collective "
                "Unconscious, which lets symbols \"arise in a modern man who did not "
                "know them\" {{GN-READ-04}} — a theory that explains how he could "
                "produce Gnostic material without having read any.",

                "He tries the explanation on and finds it comfortable: the wisdom was "
                "\"buried deep in my collective unconscious all these years\", "
                "\"acquired from the archetypes\" {{GN-READ-03}}, and the whole event "
                "is \"a giant new step in the process of human individuation\" "
                "{{GN-READ-01}}. The Gospel of Thomas is in his hands this early too, "
                "quoted approximately — \"Christ says something like, 'The Kingdom "
                "will come when the outer is the inner'\" {{GN-READ-02}} — and the "
                "\"something like\" is again the mark of a man quoting from memory.",

                "What Jung gives him is permission and a mechanism. What Jung does not "
                "give him is a cosmology in which the creator is a different being "
                "from the true God, and it is that, not the archetypes, that he spends "
                "the next five years working out.",
            ],
        },
        {
            'id': 'nh', 'register': 'A',
            'heading': '1978: the codices',
            'body': [
                "Nag Hammadi enters the corpus in the October 1978 folder and nowhere "
                "before it: 29 attestations, all in that one batch. The complete "
                "English edition had appeared in 1977, so the timing is exactly what "
                "publication allows and not a day earlier — which makes it certain "
                "that everything he wrote about Gnosticism in 1975 and 1976 was "
                "written without it.",

                "When he does get it he uses it to re-read his own fiction. \"It is "
                "obvious to me after reading in the Nag Hammadi codices that Palmer "
                "Eldritch is beyond doubt Yaltabaoth — even to the point that "
                "Yaltabaoth is described as the 'blind' god\" {{GN-READ-10}}. The "
                "Three Stigmata of Palmer Eldritch was published in 1965. He is not "
                "discovering a source; he is discovering that a book he wrote thirteen "
                "years earlier had already said it.",

                "He also draws the conclusion that matters for the whole late period: "
                "\"So in 'Valis' I was right to focus on nag Hammadi … So my acosmism "
                "+ Gnostic acosmism stems from the same source\" {{GN-READ-09}}. And "
                "he speculates, in the sentence that becomes the plasmate doctrine, "
                "\"What, oh what, if it were true that in 1945 at Nag Hammadi the "
                "actual Secret Living (information / Logos) Blood of Christ was "
                "unearthed\" {{GN-READ-11}}.",
            ],
        },
        {
            'id': 'jonas', 'register': 'A',
            'heading': '1981: Hans Jonas, and the word is "article"',
            'body': [
                "Hans Jonas is credited in almost every account of Dick's Gnosticism "
                "with supplying the framework. He is attested 26 times, and only in "
                "the 1978 and 1981 folders — rates of 0.005 and 0.048. He arrives "
                "after the Black Iron Prison, after the plasmate, after \"the Empire "
                "never ended\", and five years after the experience being explained.",

                "The citations are specific and real. Dick takes from Jonas the "
                "definition of the Gnostic project as unscrambling \"the spiritual "
                "(pneuma?) back out — the fallen divine spark imprisoned here in this "
                "prison (v. Hans Jonas' article on Gnosticism)\" {{GN-READ-12}}, and "
                "the reading of Gnostic acosmism as \"Faustian\" against the Greek "
                "cosmos {{GN-READ-15}}. He is not name-dropping; he is using an "
                "argument.",

                "But note what he calls it. Not The Gnostic Religion, Jonas's book, "
                "but \"Hans Jonas' article on Gnosticism\" — and in April 1981 he "
                "resolves to \"reread\" it {{GN-READ-13}}. Jonas wrote the Gnosticism "
                "entry for the Encyclopedia of Philosophy. Taken with the 128 EB "
                "citations, the most economical reading is that Dick's Jonas is the "
                "encyclopedia article and not the monograph.",

                "By the same month he is willing to say it outright — \"It is as "
                "Valentinus taught!\" {{GN-READ-14}} — and to classify his own novel: "
                "\"my book 'Valis' is Gnostic + the explanation is Gnostic\" "
                "{{GN-READ-16}}. Both are April 1981. The confident "
                "self-identification is the last thing to arrive, not the first.",
            ],
        },
        {
            'id': 'scholars', 'register': 'C',
            'heading': 'Two scholars, arriving independently at the same place',
            'body': [
                "The secondary literature in this archive reaches this conclusion "
                "from the documents rather than from a keyword sweep, which is worth "
                "more than either would be alone. J. K. Thomas's 'Coin-Operated Doors "
                "and God: A Gnostic Reading of Philip K. Dick' (2014) sources Dick's "
                "Gnosticism to \"Hans Jonas's The Gnostic Religion and the "
                "Encyclopedia of Philosophy\". Erik Davis, tracing the Hymn of the "
                "Pearl through the work, finds it reaching Dick \"via Encyclopedia "
                "Britannica and Hans Jonas's Gnostic Religion\", from a letter of "
                "February 1975.",

                "Davis's date is the one to test next. February 1975 is eleven months "
                "before anything in this corpus, and the Hymn of the Pearl is attested "
                "only seven times in the whole Exegesis. If the 1975 correspondence "
                "confirms it, Dick had the Hymn before he had the framework — which "
                "would put a narrative, not a doctrine, at the head of the whole "
                "sequence.",
            ],
        },
        {
            'id': 'caution', 'register': 'D',
            'heading': 'What this does not prove',
            'body': [
                "Attestation is not knowledge. Dick could have read a book and never "
                "named it, and the absence of a name is weak evidence of the absence "
                "of reading. Nobody cites everything they have read.",

                "What the silence is evidence of is narrower and still substantial. "
                "This is six years of private writing, at enormous length, with no "
                "audience to impress and no reason to hide a source — writing in which "
                "he names Plato 1,066 times, Parmenides 216 and Plotinus 184. A man "
                "who reaches that readily for the Greeks, and for an encyclopedia 128 "
                "times, and who never once reaches for Irenaeus, was probably not "
                "reading Irenaeus.",

                "And the alternative explanation is more interesting than the debunking "
                "would be. If Dick reconstructed a recognisably Valentinian cosmology "
                "out of encyclopedia articles and an experience, then either the system "
                "is convergent — derivable by anyone who starts from the same problem — "
                "or the experience he was interpreting genuinely resembled the one the "
                "ancient texts describe. The corpus cannot decide between those, and "
                "this page does not pretend to.",
            ],
        },
    ],

    'sophia': [
        {
            'id': 'note', 'register': 'D',
            'heading': 'Sophia and the Fallen Wisdom',
            'body': [
                "Sophia is the most heavily attested Gnostic proper name in Dick's "
                "corpus: 950 occurrences in his own words, against 85 for the demiurge "
                "and 30 for Yaldabaoth. The asymmetry is the argument of this page. "
                "Dick's Gnosticism is organised around the rescue of trapped wisdom far "
                "more than around the machinery of imprisonment, and readers who come "
                "to him expecting archons and a prison find instead a great deal of "
                "writing about a woman who is also an idea.",

                "She is also the first to arrive. Her rate is highest in the earliest "
                "folder — 1.747 hits per segment in 1975 — and declines steadily "
                "through 1.255, 0.737 and 0.283. General Gnostic vocabulary runs the "
                "other way, from 0.31 in 1975 to 1.078 in 1976. The figure precedes the "
                "cosmology that is supposed to explain her.",
            ],
        },
        {
            'id': 'firebright', 'register': 'A',
            'heading': '1975: a presence in search of a name',
            'body': [
                "In the earliest folder Dick does not have a Gnostic system. He has "
                "something in him he is trying to name, and the name he uses most is "
                "Firebright. It is not a borrowed term; it behaves like a private "
                "coinage for an experience that has not yet been classified.",

                "The questions he asks about it are ontological and anxious. Is \"the "
                "human being, then, merely the host for this\" {{GN-SOPH-01}}? He "
                "writes of a process by which he will \"merge with and gradually, by "
                "degrees, become Firebright, who is growing\" {{GN-SOPH-02}}, and "
                "credits it with \"greater intelligence for me, better health, longer "
                "life, even prosperity\" {{GN-SOPH-03}}.",

                "The mechanism he reaches for is reproductive rather than doctrinal: an "
                "egg \"such as a human woman ovulates\", fertilised by \"a cosmic "
                "spermatika\", producing a zygote — and in the same breath he draws the "
                "distinction he says he feels strongly about, that Neoplatonism is "
                "\"self-fertilizing\" where Gnosticism requires a Saviour from outside "
                "{{GN-SOPH-04}}. Without that intervention, he writes, \"there is no "
                "zygote, no Firebright, no seed, no immortality\" {{GN-SOPH-05}}.",
            ],
        },
        {
            'id': 'identification', 'register': 'A',
            'heading': 'The identification, stated flatly',
            'body': [
                "Then, in the same folder, he collapses the two names into one: \"Just "
                "to spell it out: 'Santa Sophia' and 'Firebright' are one and the "
                "same\" {{GN-SOPH-07}}. It is the pivot of the whole page. A private "
                "coinage for a private experience is identified with a figure from "
                "late-antique myth, and from that point the Gnostic vocabulary has "
                "something to attach to.",

                "But the identification does not stay put. Within the same run of "
                "entries Sophia is also the Cosmic Christ and Plotinus's Nous — \"I'm "
                "going to wing it and say that the Cosmic Christ, St. Sophia (Holy "
                "Wisdom) are identical with Plotinus' Nous: i.e. Lord of the Universe\" "
                "{{GN-SOPH-09}} — and the hedge is worth keeping. \"I'm going to wing "
                "it\" is not the voice of a man reporting a doctrine.",

                "He also asks the question his own identification raises and does not "
                "answer it: \"How does the Cosmic Christ after the Incarnation differ "
                "from his prior existence (as evidently St. Sophia)?\" {{GN-SOPH-10}}. "
                "Elsewhere she is a physiological cycle {{GN-SOPH-08}}, and the "
                "\"Santa Sophia\" dream is filed as evidence of the Second Advent "
                "{{GN-SOPH-06}}.",
            ],
        },
        {
            'id': 'adam-kadmon', 'register': 'A',
            'heading': '1978: the Jewish turn',
            'body': [
                "By October 1978 the figure has migrated. What was Sophia in 1975 is "
                "increasingly Adam Kadmon, the primordial Man of Lurianic Kabbalah, and "
                "the register of the writing changes with it — from something happening "
                "to him to something he has become.",

                "He states it without hedging: \"I had the universe inside me (this is "
                "Adam Kadmon for sure)\" {{GN-SOPH-15}}, and, reasoning from the Xerox "
                "missive, \"who was I, that my brain could be World? Answer: Adam "
                "Kadmon!\" {{GN-SOPH-14}}. The claim is then generalised into a thesis "
                "about the whole event: \"There seems to exist no doubt that my 2-3-74 "
                "experience is the Hermetic t Kaballist goal of becoming Adam Kadmon\" "
                "{{GN-SOPH-11}}, with a mechanism — the organism does \"go out + incorporate reality "
                "so that it is inside him\" {{GN-SOPH-12}}.",

                "Pistis Sophia survives into this folder, but as a state rather than a "
                "book: \"a blitz of certitude (pistis sophia) about the truth of "
                "Christ, God & Acts & myself\" {{GN-SOPH-16}}. He is using the title of "
                "a Gnostic scripture as a psychological description, which is a fair "
                "summary of how most of the tradition reaches him.",
            ],
        },
        {
            'id': 'departure', 'register': 'D',
            'heading': 'What he does with her that the tradition does not',
            'body': [
                "In VALIS the recovery is literal. Sophia is a two-year-old child, and "
                "the divine wisdom of the tradition is located in a person who can be "
                "met and spoken to. The novel states the theological stake in her "
                "directly — \"It is not God nor the gods which must prevail; it is "
                "wisdom, Holy Wisdom\" (VALIS, chapter 11; the card for that passage "
                "is on the trilogy page).",

                "And then she dies. This is Dick's sharpest departure from his sources: "
                "in the ancient myth Sophia is restored, the deficiency repaired, the "
                "Fullness made whole. Making her a child who is killed converts a "
                "cosmological guarantee into a bereavement, and there is no version of "
                "the Valentinian system in which that happens.",

                "Whether the decline in her attestation rate — from 1.747 to 0.283 — "
                "records a loss of interest or an absorption into the terms that rise "
                "as she falls, VALIS and Zebra, the corpus does not say. What it does "
                "show is that she was there before the framework and outlasted most of "
                "it, ending as a character rather than a term.",
            ],
        },
    ],

    'black-iron-prison': [
        {
            'id': 'note', 'register': 'D',
            'heading': 'The Black Iron Prison',
            'body': [
                "The Black Iron Prison is Dick's most influential single coinage and "
                "his most complete translation of Gnostic cosmology into his own terms. "
                "It is also, in the corpus, a datable event: a phrase that barely exists "
                "in 1975 and is everywhere by September 1976.",

                "The numbers are the sharpest transition in the whole register. The "
                "Black Iron Prison runs at 0.023 hits per segment in the 1975 folder "
                "and 2.247 in 1976 — a hundredfold jump — before falling back to 0.654 "
                "in 1978 and 0.293 in 1981. Whatever happened between those two folders "
                "produced the image that has organised Dick's reception ever since.",
            ],
        },
        {
            'id': 'before', 'register': 'A',
            'heading': 'Before the image: astral determinism',
            'body': [
                "The idea arrives before the phrase, and it arrives as a quotation. In "
                "the November 1975 folder Dick copies out a definition: \"Gnosticism: "
                "'The true purpose of Gnostic develation was to free spiritual man from "
                "astral determinism'\" {{GN-BIP-03}}. The quotation marks and the "
                "encyclopedic phrasing both point where the rest of this study points — "
                "to a reference work rather than a primary text.",

                "He is already using the demiurge in 1975, though in an idiosyncratic "
                "sense: the demiurge as daimon, immortal, containing \"recollection of "
                "prior, perhaps all prior human culture forms\" {{GN-BIP-01}}, into "
                "which part of a person is \"retained … forever\" {{GN-BIP-02}}. This is "
                "closer to Jung's collective unconscious than to Yaldabaoth, and it is "
                "worth noticing that his first demiurge is a repository rather than a "
                "tyrant.",
            ],
        },
        {
            'id': 'sept76', 'register': 'A',
            'heading': 'September 1976: the prison and the garden, in one sitting',
            'body': [
                "The September 1976 folder works the whole thing out at once, and the "
                "two halves are born together. Dick considers \"that the black iron "
                "Prison world is how this world actually is, in all its evil\", set "
                "against \"the 'Palm tree' world\" as \"the authentic world of "
                "Brahman\" {{GN-BIP-05}}, and reaches for Augustine to hold them: the "
                "real world is \"the civitas dei of Augustine\" and the prison is the "
                "earthly city {{GN-BIP-06}}.",

                "The Gnostic furniture is all present in this sitting and correctly "
                "used. The archons appear as \"the 7 concentric imprisoning rings\", now "
                "\"successfully penetrated\" with \"a beach head of divinity established "
                "here at the darkest, innermost ring\" {{GN-BIP-14}}. The rescuer is a "
                "\"salvific stranger God\" who \"outwits the archons\" and penetrates "
                "\"our 'copy of a copy' world to extricate us\" {{GN-BIP-10}} — the "
                "alien God, the counterfeit cosmos and the descent, in one sentence.",

                "The demiurge gets his proper name and a genealogy. The feminine half of "
                "the Urgrund \"does not herself directly enter our world but is "
                "separated from it (us) by her offspring the artifact (yaldabaoth)\" "
                "{{GN-BIP-11}}. That is the Sophia myth in its Sethian form — the fallen "
                "aeon, her misbegotten son, the barrier he constitutes — written out in "
                "1976, two years before Dick reports reading the Nag Hammadi codices.",
            ],
        },
        {
            'id': 'choice', 'register': 'A',
            'heading': 'He does choose, and the choice is bleak',
            'body': [
                "The Palm Tree Garden is usually read as Dick's escape hatch — the same "
                "world correctly perceived, the Gnostic diagnosis withdrawn. He does "
                "write it that way: \"my vision of the palm tree garden is the final and "
                "true vision of the Peacable Kingdom\" {{GN-BIP-04}}, and elsewhere the "
                "Paraclete leads him through to it {{GN-BIP-07}}.",

                "But in the same folder he settles the question against himself, and the "
                "sentence is rarely quoted: \"The BIP + PTG are both very real, + are "
                "antithetical alternatives, with the BIP obtaining, due to the "
                "artifact's control of this, its world (yaltabaoth)\" {{GN-BIP-12}}. "
                "Both real; the prison winning; and the reason given is the demiurge's "
                "ongoing control.",

                "He does leave the counterfeit world a purpose — the artifact, \"although "
                "enslaving us in a counterfeit world, is teaching us\" {{GN-BIP-08}}, and "
                "the Urgrund sees the whole fake \"as one Gestalt\" {{GN-BIP-09}}. That "
                "is a pedagogical theodicy and it is not Gnostic: no archon in the "
                "ancient sources is educating anybody.",
            ],
        },
        {
            'id': 'empire', 'register': 'A',
            'heading': 'The Empire never ended',
            'body': [
                "The formula that carries all of this into the fiction is in the "
                "Exegesis years before the novel. By the 1978 folder it is a settled "
                "phrase, used as shorthand — the enemy \"it his yet to be overthrown ('the "
                "empire never ended')\" {{GN-BIP-15}} — and Dick notes that he had "
                "already put it in print: the state is \"clearly articulated in 'Tears'\" "
                "{{GN-BIP-16}}, that is, in Flow My Tears, the Policeman Said, published "
                "in 1974.",

                "This is where his archons stop being cosmological. The ancient rulers "
                "administer the spheres; Dick's administer a history, and the claim that "
                "Rome did not fall is falsifiable in a way that heimarmene is not. It is "
                "the most testable proposition in his theology and the one most often "
                "quoted free of the reasoning that produced it.",
            ],
        },
        {
            'id': 'displacement', 'register': 'B',
            'heading': 'The coinage displaces the borrowing',
            'body': [
                "As the Black Iron Prison rises, the technical vocabulary it replaces "
                "falls. The demiurge declines across the four folders from 0.161 to "
                "0.160 to 0.048 to 0.016. The archons are attested nineteen times in six "
                "years; heimarmene, 312 times, is almost entirely a 1976 phenomenon.",

                "So Dick does not adopt the ancient terminology and elaborate it. He "
                "uses it while he is building, and then stops needing it. What survives "
                "into the last folders is his own vocabulary — prison, garden, Empire, "
                "artifact — which is why the Gnostic content of the late work is easy to "
                "feel and hard to cite.",
            ],
        },
    ],

    'gnosis-and-anamnesis': [
        {
            'id': 'note', 'register': 'D',
            'heading': 'Gnosis and Anamnesis',
            'body': [
                "Anamnesis is attested 1,045 times in Dick's own words — more often "
                "than Sophia, and three and a half times more often than gnosis "
                "itself. Whatever he thought happened to him in March 1974, he "
                "described it as remembering rather than learning, and the word he "
                "reached for was Plato's.",

                "It is also the steadiest term in the register: 0.759, 1.095, 1.168, "
                "0.621 across the four folders. Where the Black Iron Prison arrives in "
                "a rush and recedes, and Sophia declines from the start, recollection "
                "is the constant. It shows no arrival date because it was already his "
                "before 1974.",
            ],
        },
        {
            'id': 'greek', 'register': 'A',
            'heading': 'He reasons in Greek philosophy, not in Gnostic myth',
            'body': [
                "Plato is attested 1,066 times, Parmenides 216, Plotinus 184. Between "
                "them that is more than every named Gnostic teacher, heresiologist and "
                "primary text in this register combined. When Dick reports, he uses "
                "Gnostic language; when he reasons, he uses Greek.",

                "The clearest statement of the method is his own: what he saw was "
                "\"exactly understood commensurate with the Platonist and Neoplatonism (and "
                "Pythagorian) idea of rising each time, rising but forgetting, and the "
                "value of anamnesis, the removal of amnesis\" {{GN-GNOS-06}}. Note "
                "that the definition is etymological — anamnesis as the removal of "
                "amnesia — and that he treats it as a technical term with a literature "
                "behind it: \"the neoplatonistic recovery of memory of divinity already "
                "there\" {{GN-GNOS-05}}.",

                "Parmenides supplies the other half. Dick takes from him the "
                "proposition \"that reality was not as it appeared (and hence had a "
                "veil or dokos over it)\" {{GN-GNOS-03}}, and is careful about "
                "attribution where it matters, noting when a witness \"knew nothing of "
                "Parmenides' proof of the dokos\" {{GN-GNOS-04}}. This is the Gnostic "
                "conclusion reached on logical rather than mythological grounds, and "
                "when he wants the case made without a villain it is where he goes.",
            ],
        },
        {
            'id': 'sleep', 'register': 'A',
            'heading': 'Sleep, and the word he coined for it',
            'body': [
                "The negative of recollection is the condition that makes it necessary, "
                "and here Dick and the ancient sources converge almost exactly. The "
                "Gnostic diagnosis is that humanity is narcotised, amnesiac and unaware "
                "of captivity; Dick's is that \"we are blinded and asleep, in a state of "
                "forgetfulness, but this fallen state can be abolished\" {{GN-GNOS-11}}, "
                "and that we sit in a prison and \"through amnesia + occluded perception, "
                "do not know where we truly are nor how we got here\" {{GN-GNOS-12}}.",

                "He gives the fall the tradition's own equation — souls \"fell and forgot, "
                "having descended into nonbeing which is the same as forgetfulness\" "
                "{{GN-GNOS-08}} — and the corresponding awakening: \"They become conscious "
                "of their forgotten origin and task (anamnesis)\" {{GN-GNOS-02}}, which is "
                "the Hymn of the Pearl in one sentence.",

                "Occlusion, attested 526 times, is his own word for the blocking, and it "
                "is characteristically mechanical rather than moral. The image he uses in "
                "November 1975 is a filter: the removal \"of an occluding membrane which "
                "filters out most of the light, allowing only a token amount to filter "
                "through\" {{GN-GNOS-09}}. Revelation, on this account, subtracts an "
                "obstruction rather than adding a doctrine.",
            ],
        },
        {
            'id': 'call', 'register': 'A',
            'heading': 'The spark, and the call',
            'body': [
                "The two remaining pieces of the classical scheme are both present and "
                "both used precisely. The divine spark: \"even in their ashes lived some "
                "spark of the divine\" {{GN-GNOS-15}}, and — in a distinction that shows "
                "he is tracking the system rather than gesturing at it — \"the Spirit in "
                "my head was the spark of the divine + hence not Zebra\" {{GN-GNOS-13}}. "
                "The trapped fragment and the rescuing intelligence are different things, "
                "and he says so.",

                "And the call, in the technical Manichaean form: \"I heard the voice of "
                "the salvador salvandus calling to me, + it was the call of pure is!\" "
                "{{GN-GNOS-14}}. The saved saviour — the redeemer who is himself part of "
                "the fallen light — is the doctrine that lets the rescuer be continuous "
                "with the rescued, which is exactly the problem Dick's experience set "
                "him. In the same folder he lists the machinery it delivers from: "
                "\"Fate, karma, heimarmene, astral determinism, planetary influences, the "
                "Law\" {{GN-GNOS-16}}.",
            ],
        },
        {
            'id': 'contradiction', 'register': 'D',
            'heading': 'The contradiction he never resolves',
            'body': [
                "If gnosis is recollection of what was always known, then nothing needs "
                "to come from outside, and VALIS is unnecessary. If VALIS is real and "
                "intervened, then the knowledge arrived from outside and it is not "
                "recollection. Dick asserts both, sometimes within a single entry, and "
                "his own hedging registers the strain: gnosis and sophia as competing "
                "\"aspects\", one of which might \"predominate\" {{GN-GNOS-07}}.",

                "The honest reading is that he needed both and could not have both. "
                "Anamnesis makes the experience his own and defensible against the "
                "charge of madness; intervention makes it real and defensible against "
                "the charge of mere psychology. Giving up either one costs him something "
                "he cannot afford, so he keeps both and the system does not close.",
            ],
        },
    ],

    'valis-trilogy': [
        {
            'id': 'note', 'register': 'D',
            'heading': 'Gnosticism in the VALIS Trilogy',
            'body': [
                "The trilogy is the only place Dick submitted the system to the "
                "discipline of having to be read. The Exegesis can assert; a novel has "
                "to be inhabited, and the objections have to be given to somebody.",

                "It also lags the Exegesis by five years. \"The Empire never ended\" is "
                "written privately in September 1976 and published in 1981; the Black "
                "Iron Prison and the Palm Tree Garden are worked out in the same 1976 "
                "folder; VALIS as a term peaks in the 1978 folder at 6.16 hits per "
                "segment — by far the highest rate in the register — three years before "
                "the novel that carries the name.",
            ],
        },
        {
            'id': 'thesis', 'register': 'A',
            'heading': 'The cosmology, stated plainly',
            'body': [
                "VALIS states the Gnostic thesis more directly than anything in the "
                "Exegesis, because a novel cannot hedge for six years. Chapter 6 gives "
                "the origin of evil as a structural fault rather than a moral one: "
                "\"This is the origin of entropy, undeserved suffering, chaos and death, "
                "as well as the Empire, the Black Iron Prison\" {{GN-VALIS-09}}, and "
                "draws the consequence that follows — human beings \"are morally "
                "innocent. It is the Empire in its various disguised polyforms which "
                "tells us we have sinned\" {{GN-VALIS-10}}.",

                "That is the whole Gnostic reversal in two sentences: the guilt belongs "
                "to the system, not to the prisoner. Around it the formula repeats, and "
                "the novel tells you it is a symptom as well as a thesis — \"Fat repeats "
                "obsessively, 'The Empire never ended'\" {{GN-VALIS-08}} — while the "
                "release, when it comes, is physical and unexplained: \"They were running "
                "out of the Black Iron Prison and just laughing and laughing\" "
                "{{GN-VALIS-14}}.",
            ],
        },
        {
            'id': 'plasmate', 'register': 'A',
            'heading': 'The plasmate: a theory of how Gnosis travels',
            'body': [
                "The novel's most original contribution is a transmission mechanism, and "
                "it is a theory about Dick's own access to the material. The plasmate "
                "\"slumbered for nearly two thousand years in dormant seed form as living "
                "information in the codices at Nag Hammadi, which explained why reports of "
                "its existence had broken off abruptly around 70 A.D.\" {{GN-VALIS-07}}, "
                "and after the murder of the apostolic Christians it \"had gone into "
                "hiding at Nag Hammadi and was again loose in our world, and as angry as a "
                "motherfucker\" {{GN-VALIS-03}}.",

                "It is also described as \"an extra-terrestrial life form which came to "
                "this planet thousands of years ago, and, as living information, passed "
                "into the brains of human beings\" {{GN-VALIS-12}}. Note what this does: "
                "it makes the 1945 discovery of the library an event in salvation history "
                "rather than in scholarship, and it makes reading a form of infection. "
                "One does not need to have studied the codices for them to work. Given "
                "what the sweep shows about Dick's own sources, that is a convenient "
                "doctrine, and it may be a sincere one.",

                "The Exegesis confirms that he saw the stakes: \"So in 'Valis' I was right "
                "to focus on nag Hammadi … So my acosmism + Gnostic acosmism stems from "
                "the same source\" {{GN-VALIS-01}}.",
            ],
        },
        {
            'id': 'zebra', 'register': 'A',
            'heading': 'Zebra, and the problem a novel cannot dodge',
            'body': [
                "Zebra — God camouflaged so exactly as to be invisible inside creation — "
                "is attested 1,075 times and is not a Gnostic idea. A deity hiding within "
                "the world is the opposite of a deity exiled from it. In the novel it "
                "arrives as one of a sequence of provisional names, \"the three-eyed "
                "people, and then Zebra, who is discorporate\" {{GN-VALIS-13}}.",

                "And fiction forces the question the Exegesis can defer. \"Fat still "
                "believed in God and Christ — and a lot else — but he wished he knew why "
                "Zebra, his term for the Almighty Divine One, had not given early warning "
                "about Sherri's condition and did not now heal her, and this mystery "
                "assailed Fat's brain and turned him into a maddened thing\" "
                "{{GN-VALIS-11}}. A cosmology that cannot account for one woman's cancer "
                "is in trouble, and Dick puts the trouble on the page.",
            ],
        },
        {
            'id': 'di', 'register': 'A',
            'heading': 'The Divine Invasion runs on a different system',
            'body': [
                "The second novel changes the source material, and the change matters more "
                "than it is usually given credit for. Its framework is Lurianic Kabbalah, "
                "not Gnosticism: the contraction of the infinite, the shattering of the "
                "vessels, the scattering of the sparks, and tikkun — their gathering and "
                "repair.",

                "The book's decisive line is a restoration, not an escape: \"I have "
                "restored the Shekhina to En Sof\" {{GN-VALIS-02}}. VALIS itself already "
                "carries the Kabbalistic machinery — Hebrew letters on the wall that "
                "\"permutated until they factored out into words you could read\", into "
                "KING FELIX {{GN-VALIS-05}} — but The Divine Invasion makes it structural.",

                "The difference is theological, not decorative. Luria's broken vessels are "
                "repaired; the Gnostic spark escapes. A cosmology of repair implies the "
                "world is worth mending, which is a position Dick's Gnosticism cannot "
                "hold. He wrote both books in the same period and did not reconcile them.",
            ],
        },
        {
            'id': 'sophia-dies', 'register': 'D',
            'heading': 'Sophia, and Angel Archer',
            'body': [
                "Sophia is attested 66 times across the trilogy chapters held here, and "
                "the novel puts the theological stake in her without ambiguity: \"It is "
                "not God nor the gods which must prevail; it is wisdom, Holy Wisdom\" "
                "{{GN-VALIS-04}}. She appears as a child of two \"with the eyes of an "
                "infinitely old person\", and it is she who names the split in the "
                "narrator and ends it {{GN-VALIS-06}}.",

                "Then she is killed, and the third novel is narrated by a woman who has "
                "watched religion kill three people she loved and who receives no "
                "revelation at all. Whether The Transmigration of Timothy Archer retracts "
                "the trilogy or completes it is the standing dispute, and this portal does "
                "not settle it. Angel Archer is either Dick's last word against his own "
                "system or the system's final test, and the archive holds arguments both "
                "ways.",

                "A coverage note, because it bears on how much weight these readings can "
                "take: Timothy Archer is held here only as chapter summaries, which are "
                "portal-editor prose and are recorded in lane D. Nothing on this page "
                "quotes it as Dick's words.",
            ],
        },
    ],

    'orthodoxy-and-gnosis': [
        {
            'id': 'note', 'register': 'D',
            'heading': 'Orthodoxy and Gnosis',
            'body': [
                "The reception of Philip K. Dick has settled on Dick the Gnostic, and the "
                "corpus does not support it — or rather, it supports it only if you do not "
                "count. Christian vocabulary outweighs Gnostic vocabulary in every folder: "
                "2.253 hits per segment against 0.31 in 1975, and still running alongside "
                "it in 1981. The man writing the Exegesis is a Christian arguing with "
                "himself, not a Gnostic with a Christian residue.",

                "This page holds the contradiction open rather than resolving it, because "
                "resolving it removes evidence. Dick asserts that the creator of this "
                "world is blind and hostile, and that God is present in a beer can. Both "
                "are in the corpus, at length, for six years.",
            ],
        },
        {
            'id': 'sacramental', 'register': 'A',
            'heading': 'The instincts are sacramental from the start',
            'body': [
                "The earliest folder is not Gnostic in temper at all. In February 1975 "
                "Dick reads the decay he saw as the direction \"the Holy Spirit (or "
                "whatever you wish to deem it) was moving\" {{GN-ORTH-01}}, and the Logos "
                "as an artist \"drawing you … more and more like Christ\" {{GN-ORTH-02}}. "
                "That is sanctification, a thoroughly orthodox idea, and it assumes a "
                "creation worth perfecting.",

                "He also records being told off for the whole enterprise. Sharing his "
                "\"ionosphere plasmic entity theory about the Holy Spirit\", he gets back "
                "from Anne: \"Well, that's the sin of pride, what you're doing\" "
                "{{GN-ORTH-03}}. He writes the rebuke down and keeps it, which is "
                "characteristic and worth more than a hundred of his assertions.",

                "The eschatology is Origen's, not Valentinus's: everything \"can, through "
                "Him, be restored — back to that concept: the Restoration of All Things\" "
                "{{GN-ORTH-04}}, and at the Parousia \"man is restored to his intended, "
                "divine state\" {{GN-ORTH-07}}. Apocatastasis is universal repair. It is "
                "the opposite of a doctrine in which a saved remnant escapes and the rest "
                "of the cosmos is written off.",
            ],
        },
        {
            'id': 'distinction', 'register': 'A',
            'heading': 'He knows the traditions are different',
            'body': [
                "It is sometimes suggested that Dick blurred these systems because he did "
                "not know them apart. The corpus says otherwise. He draws the line himself, "
                "and says it matters to him: \"Here would be the crucial distinction "
                "between Neoplatonism and Gnosticism, which I feel so strongly about: the "
                "former is sort of self-fertilizing … but in Gnosticism you have the idea "
                "that the Savior is absolutely necessary\" {{GN-ORTH-06}}.",

                "That is an accurate distinction, correctly drawn, on the point that "
                "actually separates the two traditions. Whatever is going on in the "
                "Exegesis, it is not confusion about what the schools taught.",
            ],
        },
        {
            'id': 'zebra', 'register': 'A',
            'heading': 'Zebra is an incarnational idea',
            'body': [
                "The most-used religious image of Dick's last years is not Gnostic. Zebra "
                "— 1,075 attestations — is God camouflaged inside creation, and a God who "
                "hides within the world is the opposite of a God exiled from it. In "
                "September 1976 Zebra is \"the Paraclete\", bridging worlds and leading "
                "him through {{GN-ORTH-12}}; the structure holding the two worlds together "
                "is \"God-as-Holy-Spirit\" {{GN-ORTH-13}}. Those are creedal terms doing "
                "cosmological work.",

                "The agents of Zebra are described as maintaining the world rather than "
                "escaping it — \"doing the tinkering, producing one alternate world after "
                "another\", associated with \"the true, secret Xtian church\" "
                "{{GN-ORTH-11}} — and the Palm Tree Garden is named as \"the final and true "
                "vision of the Peacable Kingdom\" {{GN-ORTH-09}}, which is Isaiah, not "
                "Valentinus.",

                "Dick even polices the boundary of his own experience: if the intruding "
                "personality was intrinsic to him, then it was not another; \"but even if "
                "it was in me it was not me, because it talked to me, + in koine\" "
                "{{GN-ORTH-10}}. He is arguing against the easy psychological reading, in "
                "Greek.",
            ],
        },
        {
            'id': 'docetism', 'register': 'A',
            'heading': 'April 1981: he rules on it',
            'body': [
                "On the one doctrine where the two systems cannot both be held, Dick "
                "chooses, and chooses against the Gnostics. Docetism — the view that Christ "
                "only appeared to have a body and only appeared to suffer — is the "
                "position the tradition needs, because flesh is the problem. Dick rejects "
                "it explicitly: \"it is indeed bait but the lamb does die: he is endlessly "
                "slaughtered … I am therefore not a docetist; Christ actually suffers + dies "
                "as our ransom\" {{GN-ORTH-14}}.",

                "This is the sharpest sentence in the whole study for the question of what "
                "Dick was. It is April 1981, the last folder, the same month as \"It is as "
                "Valentinus taught!\" and \"my book 'Valis' is Gnostic\". He is claiming the "
                "Gnostic label and refusing the Gnostic Christology in the same sitting.",

                "He is aware of the cost, and looks for a system that would dissolve the "
                "problem — one that \"abolishes the issue of God the creator + God as "
                "transmundane in contradistinction to a blind demiurge creator, + abolishes "
                "the issue of Gnosis versus justification — as well as abolishing the "
                "docetist contraversy\" {{GN-ORTH-15}}. He wants the contradiction to stop "
                "being a contradiction. Wanting that is not the same as finding it.",
            ],
        },
        {
            'id': 'verdict', 'register': 'D',
            'heading': 'What to do with this',
            'body': [
                "The corpus will not support \"Dick was a Gnostic\" as a flat statement, "
                "and it will not support the denial either. What it supports is something "
                "more specific: that he used Gnostic cosmology as a diagnostic instrument "
                "and Christian theology as a commitment, and that the instrument kept "
                "producing results the commitment could not accept.",

                "That is a coherent position to be in — it is roughly where anyone ends up "
                "who takes both the problem of evil and the incarnation seriously — but it "
                "is not a system, and the Exegesis is six thousand pages of a man "
                "discovering that it is not a system. Scholarship on the early fiction has "
                "read the dualism as settled from the beginning {{GN-ORTH-16}}; the "
                "Exegesis suggests something less resolved and more interesting.",

                "Readers who want the tension removed should be aware that it is removed by "
                "discarding half the evidence, and should choose which half deliberately "
                "rather than by inheriting a consensus.",
            ],
        },
    ],
}
