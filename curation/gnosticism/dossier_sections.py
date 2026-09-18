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
        'lexicon_focus': ['GNOS_nag_hammadi', 'GNOS_jonas', 'GNOS_jung',
                          'GNOS_valentinus', 'GNOS_irenaeus',
                          'GNOS_apocryphon_john', 'GNOS_corpus_hermeticum',
                          'GNOS_pagels', 'GNOS_gospel_thomas'],
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
            "Dick's work, finds it reaching him \"via Encyclopaedia Britannica and "
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
