"""
The religion taxonomy: topics, subsections, and the patterns that tag a passage
with them.

This is the thing to edit when a tradition, a subsection or a pattern changes.
`scripts/research/sweep_religion.py` reads it, and every later stage (the
database, the site export, the review tool) reads what the sweep wrote.

A subsection tag is applied to a passage when one of its patterns matches the
matched span itself, not the surrounding context. That keeps "Christ" in a
passage about Sophia from tagging the passage as Christology.

    strong   a term that names the subject (Torah, Zoroaster, Kabbalah)
    weak     a term that is also an ordinary word or a first name (Elias, Paul,
             Law, Tao). Findings from weak patterns are kept and flagged, and
             must be read before they are relied on.
    exclude  a regex that, if it matches within 80 characters either side of a
             hit, drops that hit for that subsection only.

Patterns are case-insensitive unless written with an inline (?-i: ...) group.
"""

TOPICS = [
    # ------------------------------------------------------------------
    {
        'id': 'christianity',
        'label': 'Christianity',
        'description': 'Christ, Paul and the early church, the apocalypse, the Church and '
                       'Rome, and the Bible as scripture. Dick’s Christianity is the '
                       'frame for most of his late theology, and the most heavily '
                       'mentioned tradition in the Exegesis.',
        'subsections': [
            {
                'id': 'christology',
                'label': 'Christ and Jesus',
                'description': 'Christ as a person, as a cosmic principle, and as the '
                               'figure whose return is awaited.',
                'strong': [r'\bChrist\b', r'\bJesus\b'],
                'weak': [r'\bKyrios\b', r'Kingdom of (?:God|Heaven)'],
                'exclude': [r'Christmas', r'Christian Science'],
            },
            {
                'id': 'pauline-acts',
                'label': 'Paul, Acts and the early church',
                'description': 'The Pauline letters, the Acts of the Apostles, and the '
                               'Holy Spirit as Paraclete. Dick’s most sustained single '
                               'reading of a biblical book is of Acts.',
                'strong': [r'(?-i:\bActs\b)', r'\bPauline\b', r'\bSt\.? Paul\b',
                           r'\bParaclete\b', r'\bpentecost', r'Holy Spirit'],
                'weak': [r'(?-i:\bPaul\b)'],
                'exclude': [r'Paul (?:Williams|Sarill|Hoffman|Ghent|Lewis|Rasch)'],
            },
            {
                'id': 'apocalypse',
                'label': 'Apocalypse and the Second Advent',
                'description': 'The Parousia, the apocalyptic books and the return of '
                               'Christ, which Dick dates to his own lifetime.',
                'strong': [r'\bParousia\b', r'\bapocalyp\w*', r'\bSecond (?:Coming|Advent)\b',
                           r'\bAntichrist\b'],
                'weak': [r'(?-i:\bRevelations?\b)', r'\beschatolog\w*'],
                'exclude': [r'apocalypse now'],
            },
            {
                'id': 'church-rome',
                'label': 'The Church and Rome',
                'description': 'Rome as the Empire of his 1974 vision, and the Church as '
                               'institution, sacrament and authority.',
                'strong': [r'\bCatholic\w*', r'\bcathedral\b', r'Church of Rome',
                           r'\bpope\b', r'\bsacrament\w*'],
                'weak': [r'\bRome\b', r'\bthe Church\b'],
                'exclude': [r'Rome, (?:Italy|Georgia|New York)'],
            },
            {
                'id': 'scripture',
                'label': 'Scripture and the Bible',
                'description': 'The Bible as text, code and world. The full study is at '
                               '/studies/bible/bible-in-pkd.',
                'strong': [r'\bBible\w*', r'\bScriptures?\b', r'\b(?:Old|New) Testament\b',
                           r'\bGospels?\b', r'\bbiblical\b', r'\bKing James\b',
                           r'\bVulgate\b', r'\bSeptuagint\b'],
                'weak': [r'\bTestaments?\b', r'\bEpistles?\b'],
                'exclude': [r'Bible Belt', r'Bible[- ]?(?:black|belt)'],
            },
        ],
        'related': ['gnosticism', 'judaism', 'logos'],
    },
    # ------------------------------------------------------------------
    {
        'id': 'gnosticism',
        'label': 'Gnosticism',
        'description': 'Dick called himself a Gnostic. The Gnostic study is at '
                       '/studies/gnosticism; this topic indexes every mention by '
                       'subsection, so the Gnostic material is reachable from the '
                       'religion study as well.',
        'subsections': [
            {
                'id': 'sophia',
                'label': 'Sophia, Wisdom and the Holy Wisdom',
                'description': 'Sophia as the fallen or redeeming feminine principle, and '
                               'Hagia Sophia as the Holy Wisdom in his theology.',
                'strong': [r'\bSophia\b', r'Hagia Sophia', r'Holy Wisdom', r'\bWisdom of God\b'],
                'weak': [r'\bWisdom\b'],
                'exclude': [r'Sophia Loren'],
            },
            {
                'id': 'demiurge',
                'label': 'The Demiurge and the blind creator',
                'description': 'The creator-god as ignorant or blind subordinate: '
                               'Yaldabaoth, Ialdabaoth, Samael, the demiurge.',
                'strong': [r'[Dd]emiurg\w*', r'Yald?aboath', r'Ialdabaoth', r'\bSamael\b',
                           r'\bYaldabaoth\b'],
                'weak': [r'\bblind (?:god|creator)\b'],
                'exclude': [],
            },
            {
                'id': 'anamnesis',
                'label': 'Anamnesis and recollection',
                'description': 'Recollection of a true state before the fall, which Dick '
                               'takes from Plato and from Gnostic texts.',
                'strong': [r'\banamnesis\b'],
                'weak': [r'\brecollection\b'],
                'exclude': [],
            },
            {
                'id': 'gnostic-texts',
                'label': 'Gnostic texts',
                'description': 'The Gospel of Thomas, the Hymn of the Pearl, the Pistis '
                               'Sophia and the Nag Hammadi library, as Dick knew them.',
                'strong': [r'Gospel of Thomas', r'Pistis Sophia', r'Nag Hammadi',
                           r'Hymn of the Pearl', r'Acts of Thomas', r'Gnostic (?:Gospel|texts?|Acts)'],
                'weak': [],
                'exclude': [],
            },
            {
                'id': 'gnostic-general',
                'label': 'Gnostic (general)',
                'description': 'Dick’s own uses of the words Gnostic and Gnosticism, '
                               'without a specific doctrine or text.',
                'strong': [r'\bgnos(?:tic|ticism|is)\b'],
                'weak': [],
                'exclude': [],
            },
        ],
        'related': ['christianity', 'platonism', 'logos', 'zoroastrianism'],
    },
    # ------------------------------------------------------------------
    {
        'id': 'zoroastrianism',
        'label': 'Zoroastrianism and Mazdaism',
        'description': 'The Persian religion of light and darkness, and the traditions '
                       'Dick took from it: dualism, Manichaeism and Mithraism.',
        'subsections': [
            {
                'id': 'zoroaster',
                'label': 'Zoroaster and Mazdaism',
                'description': 'Zoroaster (Zarathustra), Ahura Mazda and the Persian '
                               'tradition as Dick reads it.',
                'strong': [r'\bZoroast\w*', r'\bZarathustra\b', r'\bMazd\w*', r'\bAhura\b'],
                'weak': [],
                'exclude': [],
            },
            {
                'id': 'dualism-manichaeism',
                'label': 'Dualism and Manichaeism',
                'description': 'Light against darkness as the structure of the world, '
                               'and Mani’s system built on it.',
                'strong': [r'\bdualis\w*', r'\bManich\w*'],
                'weak': [r'\blight (?:and|against|versus|vs\.?) (?:darkness|dark)\b'],
                'exclude': [],
            },
            {
                'id': 'mithraism',
                'label': 'Mithraism and the mysteries of light',
                'description': 'The Roman Mithras cult and its place in the Gnostic-Persian '
                               'lineage Dick traces.',
                'strong': [r'\bMithra\w*'],
                'weak': [],
                'exclude': [],
            },
        ],
        'related': ['gnosticism', 'christianity', 'mysticism'],
    },
    # ------------------------------------------------------------------
    {
        'id': 'judaism',
        'label': 'Judaism and the Torah',
        'description': 'The Torah as law, as living text, and as the informational basis of '
                       'reality; the Essenes and Qumran; and the Hebrew prophets Dick read '
                       'as his own precursors.',
        'subsections': [
            {
                'id': 'torah',
                'label': 'The Torah',
                'description': 'The Torah as the law Christ corrects, and as the living '
                               'blueprint of reality.',
                'strong': [r'\bTorah\b'],
                'weak': [r'\bMosaic\b', r'\bMoses\b'],
                'exclude': [],
            },
            {
                'id': 'essenes-qumran',
                'label': 'Essenes and Qumran',
                'description': 'The Essene community, the Qumran scrolls and the Dead Sea '
                               'writings, which Dick places beside the Gospels.',
                'strong': [r'(?-i:\bEssenes?\b)', r'\bQumr\w*', r'Dead Sea (?:Scrolls|writings)'],
                'weak': [r'\bEssene\b'],
                'exclude': [],
            },
            {
                'id': 'hebrew-prophets',
                'label': 'Prophets: Elijah, Malachi, Daniel',
                'description': 'The prophets whose books Dick reads for timetables of '
                               'return and judgment.',
                'strong': [r'\bElijah\b', r'\bMalachi\b', r'\bIsaiah\b', r'\bEzekiel\b',
                           r'\bJeremiah\b'],
                'weak': [r'\bElias\b', r'\bDaniel\b', r'\bprophet\w*'],
                'exclude': [r'Daniel (?:Boone|Ellsberg|Harms)', r'Elias (?:Hayes|Cross)'],
            },
        ],
        'related': ['christianity', 'kabbalah'],
    },
    # ------------------------------------------------------------------
    {
        'id': 'kabbalah',
        'label': 'Kabbalah',
        'description': 'The Jewish mystical tradition as Dick knew it: the Kabbalah, the '
                       'sefirot and the Zohar, which he reads beside his own 1974 '
                       'experience.',
        'subsections': [
            {
                'id': 'kabbalah-general',
                'label': 'Kabbalah (general)',
                'description': 'Dick’s uses of Kabbalah, Cabbala and Qabalah.',
                'strong': [r'\b(?:kabbal\w*|cabbal\w*|cabala\b|qabal\w*)'],
                'weak': [],
                'exclude': [],
            },
            {
                'id': 'sefirot',
                'label': 'Sefirot, Malkuth and the Tree of Life',
                'description': 'The ten sefirot, the lowest of them Malkuth, and the Tree of '
                               'Life that carries them.',
                'strong': [r'\bsefir\w*', r'\bsephir\w*', r'\bMalkuth\b', r'Tree of Life',
                           r'\bEin Sof\b', r'\bEn Sof\b'],
                'weak': [],
                'exclude': [],
            },
            {
                'id': 'zohar',
                'label': 'The Zohar',
                'description': 'The Zohar as the book of the Kabbalah, and its figures such '
                               'as the Shekhinah and the maiden Torah.',
                'strong': [r'(?-i:\bZohar\b)', r'\bShekhin\w*', r'\bShekinah\b'],
                'weak': [],
                'exclude': [],
            },
        ],
        'related': ['judaism', 'logos', 'mysticism'],
    },
    # ------------------------------------------------------------------
    {
        'id': 'logos',
        'label': 'Logos',
        'description': 'The Word: the Logos of the Fourth Gospel, Greek philosophy’s '
                       'rational principle, and Dick’s identification of the Logos with '
                       'information and with VALIS.',
        'subsections': [
            {
                'id': 'logos-word',
                'label': 'The Logos as Word and reason',
                'description': 'The Logos as the Word of John 1, the rational structure of '
                               'the cosmos, and the Greek term.',
                'strong': [r'\bLogos\b', r'In the beginning (?:was|is) the Word',
                           r'Im Anfang war das Wort', r'Fourth Gospel'],
                'weak': [r'\bthe Word\b'],
                'exclude': [],
            },
            {
                'id': 'logos-information',
                'label': 'The Logos as information',
                'description': 'Where Dick identifies the Logos with information, the '
                               'living information that VALIS is, and the Torah as the same.',
                'strong': [],
                'weak': [r'Logos.{0,60}(?:information|info\b|cypher)',
                         r'(?:information|info\b).{0,60}Logos'],
                'exclude': [],
            },
        ],
        'related': ['christianity', 'kabbalah', 'gnosticism'],
    },
    # ------------------------------------------------------------------
    {
        'id': 'mercerism',
        'label': 'Mercerism',
        'description': 'Mercer and Mercerism in Do Androids Dream of Electric Sheep?: the '
                       'empathy box, the fusion with Wilbur Mercer, and the religion of '
                       'shared suffering that Dick returned to.',
        'subsections': [
            {
                'id': 'mercer-figure',
                'label': 'Wilbur Mercer',
                'description': 'The figure of Mercer, his hill and his suffering, in the novel '
                               'and in the notebooks.',
                'strong': [r'\bMercer\b', r'\bWilbur Mercer\b'],
                'weak': [],
                'exclude': [r'Mercer (?:Island|County)'],
            },
            {
                'id': 'mercerism-religion',
                'label': 'Mercerism as religion',
                'description': 'The empathy box and the fusion of many people into one '
                               'experience, read as a religion.',
                'strong': [r'\bMercerism\b', r'\bempathy box\b', r'\bMercerian\b'],
                'weak': [r'\bfusion\b'],
                'exclude': [],
            },
        ],
        'related': ['christianity', 'mysticism'],
    },
    # ------------------------------------------------------------------
    {
        'id': 'platonism',
        'label': 'Platonism, Neoplatonism and Hermeticism',
        'description': 'Plato’s recollection and the Timaeus, Pythagoras, the Neoplatonists, '
                       'and the Hermetic writings Dick cites beside his own experience.',
        'subsections': [
            {
                'id': 'plato-pythagoras',
                'label': 'Plato and Pythagoras',
                'description': 'Platonic forms, the Timaeus, and Pythagorean number and '
                               'harmony.',
                'strong': [r'\bPlato\w*', r'\bPythagor\w*', r'\bTimaeus\b'],
                'weak': [],
                'exclude': [r'Platoon'],
            },
            {
                'id': 'neoplatonism',
                'label': 'Plotinus and the Neoplatonists',
                'description': 'Plotinus, Proclus, Porphyry, and Philo of Alexandria as the '
                               'bridge from Plato to Christian and Jewish mysticism.',
                'strong': [r'\bPlotin\w*', r'\bNeoplaton\w*', r'\bProclus\b', r'\bPorphyry\b',
                           r'\bPhilo\b'],
                'weak': [],
                'exclude': [],
            },
            {
                'id': 'hermetic',
                'label': 'Hermetic writings',
                'description': 'Hermes Trismegistus, the Hermetica and Asklepios.',
                'strong': [r'\bHermes\b', r'\bHermetic\w*', r'\bTrismegist\w*', r'\bAsklep\w*'],
                'weak': [],
                'exclude': [],
            },
        ],
        'related': ['gnosticism', 'logos', 'mystery-religions'],
    },
    # ------------------------------------------------------------------
    {
        'id': 'mystery-religions',
        'label': 'Mystery religions',
        'description': 'Dionysus and Zagreus, the Bacchae, and the Greek mysteries Dick '
                       'set beside the Gospels.',
        'subsections': [
            {
                'id': 'dionysus-zagreus',
                'label': 'Dionysus, Zagreus and the Bacchae',
                'description': 'The god who is torn apart and returns, and the identification '
                               'with Christ that Dick proposes in 1975.',
                'strong': [r'\bDionys\w*', r'\bZagreus\b', r'\bBacchae\b', r'\bBacchus\b',
                           r'\bBacchic\b'],
                'weak': [],
                'exclude': [],
            },
            {
                'id': 'eleusis-orphism',
                'label': 'Eleusis and Orphism',
                'description': 'The Eleusinian mysteries and the Orphic tradition.',
                'strong': [r'\bEleusi\w*', r'\bOrphi\w*'],
                'weak': [r'\bmysteries\b'],
                'exclude': [],
            },
        ],
        'related': ['platonism', 'christianity'],
    },
    # ------------------------------------------------------------------
    {
        'id': 'mysticism',
        'label': 'Mysticism and altered states',
        'description': 'The mystical experience Dick describes as the origin of his theology, '
                       'and the traditions he compares it with.',
        'subsections': [
            {
                'id': 'mystical-experience',
                'label': 'Mystical experience',
                'description': 'Mystical, ecstatic and illuminative language used of his '
                               'own 1974 experience and of other traditions.',
                'strong': [r'\bmystic\w*', r'\becstat\w*', r'\bunio mystica\b'],
                'weak': [r'\billumination\b'],
                'exclude': [],
            },
        ],
        'related': ['kabbalah', 'christianity', 'hinduism'],
    },
    # ------------------------------------------------------------------
    {
        'id': 'buddhism',
        'label': 'Buddhism',
        'description': 'Buddhism in Dick’s reading: the Bardo Thodol, Tibetan Buddhism, and '
                       'the Buddhist idealist tradition.',
        'subsections': [
            {
                'id': 'buddhism-general',
                'label': 'Buddhism and the Bardo',
                'description': 'Buddhist terms, the Bardo Thodol and the Tibetan Book of the Dead.',
                'strong': [r'\bBuddh\w*', r'\bBardo\b', r'Tibetan Book of the Dead',
                           r'\bBodhi\w*', r'\bNirvana\b', r'(?-i:\bZen\b)'],
                'weak': [],
                'exclude': [r'Buddha (?:Board|Bar)'],
            },
        ],
        'related': ['hinduism', 'taoism', 'mysticism'],
    },
    # ------------------------------------------------------------------
    {
        'id': 'hinduism',
        'label': 'Hinduism and Vedanta',
        'description': 'Brahman and the Upanishads, the deities Dick names, and the Vedanta '
                       'he read beside Christianity.',
        'subsections': [
            {
                'id': 'vedanta-brahman',
                'label': 'Brahman, Atman and the Upanishads',
                'description': 'The metaphysics of Vedanta as Dick encountered it.',
                'strong': [r'\bHindu\w*', r'\bVedant\w*', r'\bUpanishad\w*', r'\bBrahman\b',
                           r'\bAtman\b'],
                'weak': [],
                'exclude': [],
            },
            {
                'id': 'deities',
                'label': 'Hindu deities',
                'description': 'Shiva, Vishnu, Krishna and the other deities he names as '
                               'figures for the same reality as Christ.',
                'strong': [r'\bVishnu\b', r'\bShiva\b', r'\bSiva\b', r'\bKrishna\b',
                           r'\bGanesh\w*'],
                'weak': [r'\bKali\b'],
                'exclude': [],
            },
        ],
        'related': ['buddhism', 'mysticism'],
    },
    # ------------------------------------------------------------------
    {
        'id': 'taoism',
        'label': 'Taoism',
        'description': 'The Tao and the Taoist writers Dick read beside the Gnostic and '
                       'Christian material.',
        'subsections': [
            {
                'id': 'tao',
                'label': 'The Tao',
                'description': 'The Tao, the Tao Te Ching and Lao Tzu.',
                'strong': [r'(?-i:\bTao\b)', r'\bTaoi\w*', r'Tao Te Ching', r'\bLao[- ]?[Tt]zu\b'],
                'weak': [],
                'exclude': [],
            },
        ],
        'related': ['buddhism', 'hinduism'],
    },
    # ------------------------------------------------------------------
    {
        'id': 'islam',
        'label': 'Islam',
        'description': 'The Quran, Islam and Sufism, mentioned in the Exegesis and in '
                       'The Divine Invasion.',
        'subsections': [
            {
                'id': 'islam-general',
                'label': 'Islam and Sufism',
                'description': 'The Quran, the Koran, Islam and the Sufi tradition.',
                'strong': [r'\bIslam\w*', r'\bKoran\b', r'\bQuran\b', r'\bSufi\w*'],
                'weak': [r'\bMuhammad\b', r'\bMohammed\b'],
                'exclude': [],
            },
        ],
        'related': ['christianity', 'mysticism'],
    },
]

# Topics named in `related` that have no page of their own are kept as plain
# labels in the site, so a broken relation cannot break the build.
TOPIC_IDS = {t['id'] for t in TOPICS}


def all_subsections():
    """Flat list of (topic_id, subsection) in taxonomy order."""
    return [(t['id'], s) for t in TOPICS for s in t['subsections']]
