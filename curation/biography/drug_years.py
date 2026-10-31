"""
Biography corrections and additions for the drug years, 1952-1977.

Source of truth for these entries in site/public/data/biography/curated.json,
which is hand-curated (no exporter writes it). Applied by
scripts/biography/apply_biography_curation.py, which is idempotent.

Every date and claim here was checked against the corpus while building the
Drugs in Philip K. Dick dossier (curation/drugs-in-pkd/). Quotations are the
dossier's piths, which its seeder verifies verbatim; the finding id is given
in `notes` so each can be traced.

CORRECTIONS replace or add fields on an existing event, by id; APPEND adds
list items (sources, quotes) without dropping earlier ones. Ids are never
renamed, even when the year in an id turns out to be wrong.
NEW_EVENTS are appended if their id is absent.
"""

DOSSIER = {'to': '/studies/psychology/drugs-in-pkd', 'label': 'Drugs in Philip K. Dick'}


def dossier_link(facet=None):
    to = DOSSIER['to'] + (f'?facet={facet.replace(" ", "%20")}#mentions' if facet else '')
    return {'to': to, 'label': DOSSIER['label']}


SUTIN = {'author': 'Sutin', 'work': 'Divine Invasions', 'lane': 'C'}
ANNE = {'author': 'Anne R. Dick', 'work': 'The Search for Philip K. Dick', 'lane': 'C'}
ARNOLD = {'author': 'Arnold', 'work': 'The Divine Madness of Philip K. Dick', 'lane': 'C'}


def src(base, supports, locator=''):
    return {**base, 'locator': locator, 'supports': supports}


def letter(recipient, date, supports):
    return {'author': 'PKD', 'work': f'Letter to {recipient}, {date}', 'lane': 'E',
            'locator': '', 'supports': supports}


CORRECTIONS = {
    'pkd_bio_1956_marriage_anne': {
        'date': '1959-04-01',
        'date_precision': 'day',
        'location': 'Ensenada, Baja California, Mexico',
        'event': ("PKD and Anne Williams Rubenstein marry before a judge in Ensenada, Mexico, "
                  "on April 1, 1959, and settle in Point Reyes Station — the marriage of the "
                  "mainstream years."),
        'notes': ("Corrected 2026-10-30: previously dated 1956 with Berkeley as the place. Sutin "
                  "and Anne R. Dick both put the wedding in Ensenada at the start of April 1959. "
                  "The id keeps the old year because ids are never renamed."),
    },
    'pkd_bio_1963_marriage_hackett': {
        'date': '1966-07',
        'date_precision': 'month',
        'location': 'Marin County, California',
        'event': ("PKD marries Nancy Hackett in a civil ceremony in July 1966, with Bishop James "
                  "Pike in attendance — his fourth marriage, after more than a year living "
                  "together in Oakland."),
        'narrative': (
            "Philip met Nancy Hackett, the nineteen-year-old stepdaughter of his friend Maren "
            "Hackett, at the end of 1964, after leaving Anne and Point Reyes; she was staying "
            "with him in Oakland by early 1965. They married in July 1966 in a civil ceremony; "
            "Bishop James Pike attended and pronounced a blessing, although Phil's marriage to "
            "Anne had never been annulled. Their daughter Isolde Freya (Isa) was born on March "
            "15, 1967. The marriage spans the pill-heavy years Nancy later described to Anne R. "
            "Dick — several doctors, several pharmacies — and ended when Nancy left with Isa in "
            "September 1970, opening onto the Santa Venetia house, the break-in and Vancouver."),
        'sources': [
            src(SUTIN, 'the July 1966 marriage, Pike\'s presence, and Isa\'s birth in March 1967',
                'ch. 5'),
            src(ANNE, 'Nancy\'s account of the marriage years and the pills'),
        ],
        'links': {'studies': [dossier_link('Nancy Hackett')]},
        'notes': ("Corrected 2026-10-30: previously dated 1963 with a narrative that put the "
                  "marriage before the 1964-65 novels. Sutin: \"In July 1966 Phil and Nancy were "
                  "married.\" The id keeps the old year because ids are never renamed."),
    },
    'pkd_bio_1972_suicide_attempt': {
        'event': ("Alone and collapsing in Vancouver after the February science-fiction "
                  "convention, PKD attempts suicide in March 1972; a crisis line refers him to "
                  "X-Kalay, a residential rehabilitation house for heroin addicts."),
        'links': {'studies': [dossier_link('Rehabilitation')]},
        'notes': ("Corrected 2026-10-30: the event text called the February event \"the X-Kalay "
                  "convention\"; the convention was VCon, and X-Kalay was the rehabilitation "
                  "house he entered after the attempt. Dossier: DRG-LET-1972-XKALAY, "
                  "DRG-LET-1972-HEROIN, DRG-BIO-SUTIN-THREEWEEKS."),
    },
    'pkd_bio_1972_vancouver_x_kalay_arnold': {
        'event': ("Arnold describes X-Kalay as a harsh, Synanon-style program run by David "
                  "Berner, built to break new residents down — the only residential addiction "
                  "program in Vancouver at the time."),
        'narrative': (
            "After the suicide attempt Philip entered X-Kalay. Arnold gives its history: founded "
            "in 1967 by David Berner as a transitional community for Native people released from "
            "prison, it became a therapeutic community for addicts under Berner's dictatorial "
            "leadership, with a philosophy of breaking new residents down by name-calling and "
            "humiliation and assigning them the toilets and floors. Arnold reads A Scanner "
            "Darkly's New-Path, which grows the drug it claims to cure, as Dick's judgment on it, "
            "and notes that his paranoia outlasted the reduction in his drug use.\n\n"
            "Dick's own verdict changed. From inside, in April 1972, he wrote \"I owe my life to "
            "them\"; in 1975 he called its education faulty; in the Exegesis its attack-therapy "
            "\"game\" became the equivalent of brainwashing. Sutin credits it with ending his "
            "regular amphetamine use."),
        'sources': [
            src(ARNOLD, 'X-Kalay\'s history, Berner, and its methods; New-Path as its portrait',
                'ch. 1'),
            {**SUTIN, 'locator': 'ch. 7', 'supports': 'the X-Kalay chronology'},
            src(SUTIN, 'the length of the stay and its effect on his amphetamine use', 'ch. 9'),
            letter('Göran Bengtson', 'April 3, 1972', 'the view from inside X-Kalay'),
        ],
        'quotes': [
            {'text': 'I owe my life to them.', 'speaker': 'PKD',
             'source': 'Letter to Göran Bengtson, April 3, 1972', 'lane': 'E'},
        ],
        'dispute': {
            'summary': "How long he stayed at X-Kalay is given three ways.",
            'positions': [
                {'who': 'PKD (letter to Bruce Gillespie, October 31, 1972)',
                 'claim': 'he spent a month there'},
                {'who': 'Sutin (Divine Invasions)',
                 'claim': 'the stay lasted only three weeks before its demands grated'},
                {'who': 'Arnold (The Divine Madness)',
                 'claim': 'he underwent inpatient treatment there until March'},
            ],
        },
        'links': {'studies': [dossier_link('Rehabilitation')]},
        'notes': ("Corrected 2026-10-30: the previous text said Arnold frames the stay as \"a "
                  "misfit refuge\" and \"a search for structure and belonging\"; Arnold's text in "
                  "the archive does not say this. Dossier: DRG-LET-1972-XKALAY, "
                  "DRG-LET-1975-FAULTY, DRG-EX-1977-SYNANON, DRG-BIO-SUTIN-NEVERAGAIN."),
    },
    'pkd_bio_1973_gutter_years_narrative': {
        'date': '1970-1972',
        'date_precision': 'range',
        'event': ("Looking back in 1973, PKD says that after each failed marriage he dropped "
                  "\"gratefully\" into a life among drugs, guns and people he calls vicious — "
                  "above all in the Santa Venetia house of 1970-72."),
        'sources': [
            letter('Diane Cleaver', 'September 5, 1973',
                   'the account of the "gutter" years and the young people he sheltered'),
        ],
        'quotes': [
            {'text': ('when the marriage failed I dropped (gratefully) into the gutter of '
                      'near-illegal life: narcotics and guns and knives and oh so many crimes'),
             'speaker': 'PKD', 'source': 'Letter to Diane Cleaver, September 5, 1973',
             'lane': 'E'},
        ],
        'lanes': ['E'],
        'confidence': 'high',
        'links': {'studies': [dossier_link('Drug culture')]},
        'notes': ("Corrected 2026-10-30: previously dated 1970-01-01 (a placeholder) and "
                  "paraphrased as one period; the letter describes a pattern after each failed "
                  "marriage. The earlier note quoted \"I embraced truly vicious people\"; the "
                  "letter reads \"I embrace truly vicious people, I suppose as an antidote to the "
                  "middle class safe rational spineless world my wives had forced on me.\" The "
                  "id keeps its old year because ids are never renamed."),
    },
    'pkd_bio_1964_amphetamine': {
        'narrative': (
            "By 1964 the amphetamines Dick had taken since the early 1950s were a managed "
            "supply. In September he complained that it had dried up despite two open "
            "prescriptions; in October a brochure left in a refill told him that the "
            "\"semoxydrine hydrochloride\" he had taken for seven years was methamphetamine, and "
            "that he was on its strongest dose. Sutin places Palmer Eldritch in the middle of an "
            "\"amphetamine-fueled writing streak\"; Anne R. Dick dates recreational use to this "
            "year, after he left her."),
        'sources': [
            letter('Terry and Carol Carr', 'October 22, 1964', 'the dose and the brochure'),
            src(SUTIN, 'the 1963-64 writing streak and amphetamines'),
            src(ANNE, 'recreational amphetamine use beginning after the separation'),
        ],
        'quotes': [
            {'text': 'I am up to six 7.5 mg of them a day, and 7.5 is their strongest dose',
             'speaker': 'PKD', 'source': 'Letter to Terry and Carol Carr, October 22, 1964',
             'lane': 'E'},
        ],
        'lanes': ['C', 'E'],
        'confidence': 'high',
        'links': {'studies': [dossier_link('Amphetamines')]},
        'notes': 'Enriched 2026-10-30. Dossier: DRG-LET-1964-SUPPLY, DRG-LET-1964-BROCHURE.',
    },
    'pkd_bio_1967_paranoia_drugs': {
        'narrative': (
            "Arnold reads the paranoia of the Nancy years as amphetamine-induced, part of a "
            "chronic amphetamine psychosis that he argues explains everything others took for "
            "schizophrenia. Sutin documents the pills of these years — Stelazine, relaxants, "
            "Librium, Valium, Dexamyl and white crosses from a rotating set of doctors. Dick "
            "himself, looking back around 1979, gave three causes for his madness: Nancy "
            "leaving, drugs, and endogenous psychosis."),
        'sources': [
            src(ARNOLD, 'amphetamine paranoia as the explanation'),
            src(SUTIN, 'the pills of the Nancy years'),
        ],
        'dispute': {
            'summary': 'How much of the paranoia was the drug.',
            'positions': [
                {'who': 'Arnold (The Divine Madness)',
                 'claim': 'the paranoid episodes are most parsimoniously explained by speed'},
                {'who': 'PKD (Exegesis, c. 1978-80)',
                 'claim': 'drugs were one cause among three, with Nancy leaving and endogenous psychosis'},
            ],
        },
        'lanes': ['B', 'C'],
        'confidence': 'medium',
        'links': {'studies': [dossier_link('Paranoia')]},
        'notes': ('Enriched 2026-10-30. Dossier: DRG-BIO-ARNOLD-WRONGDRUG, '
                  'DRG-BIO-ARNOLD-PSYCHOSIS, DRG-BIO-SUTIN-PILLS, DRG-EX-1978-DRIVENMAD.'),
    },
}


APPEND = {
    'pkd_bio_1956_marriage_anne': {
        'sources': [
            src(SUTIN, 'the Ensenada wedding on April Fools\' Day 1959'),
            src(ANNE, 'the drive to Ensenada at the end of March 1959'),
        ],
    },
}


NEW_EVENTS = [
    {
        'id': 'pkd_bio_1953_first_semoxydrine',
        'date': '1952-1953',
        'date_precision': 'range',
        'event': ("At about twenty-four PKD begins taking Semoxydrine, a prescription "
                  "methamphetamine, which he later describes as having lifted years of "
                  "agoraphobic withdrawal."),
        'category': 'drug_use',
        'entities': ['Kleo Apostolides'],
        'location': 'Berkeley, California',
        'source': 'Letter to Anthony Boucher, April 25, 1962',
        'importance': 3,
        'narrative': (
            "In a long letter of 1962 Dick says that at twenty-four two things rescued him from "
            "a world that had been closing in since adolescence: learning to drive, and a "
            "stimulant he spells semoxydrene, whose first dose restored a clarity he had lost "
            "over fifteen years. When it began is disputed. Sutin quotes Dick's first wife Kleo "
            "insisting that he took nothing but a single Semoxydrine sample from her physician "
            "father; Dick's stepfather's notes of 1971 record Dick saying he had been on "
            "Benzedrine \"since 1951, when Kleo's physician father gave him a prescription\"."),
        'sources': [
            letter('Anthony Boucher', 'April 25, 1962', 'the first dose and its effect'),
            src(SUTIN, 'Kleo\'s denial and the stepfather\'s notes'),
        ],
        'quotes': [
            {'text': 'the first 5 mg which I took cleared away the cobwebs from my brain',
             'speaker': 'PKD', 'source': 'Letter to Anthony Boucher, April 25, 1962', 'lane': 'E'},
        ],
        'dispute': {
            'summary': 'Whether he took amphetamines regularly during the Berkeley marriage.',
            'positions': [
                {'who': 'Kleo, quoted by Sutin', 'claim': 'one sample only, no other drugs'},
                {'who': 'Iskandar Guy, quoted by Sutin', 'claim': 'regular low doses'},
                {'who': 'PKD, in his stepfather\'s notes of 1971',
                 'claim': 'Benzedrine since 1951, on a prescription from Kleo\'s father'},
            ],
        },
        'lanes': ['C', 'E'],
        'confidence': 'medium',
        'links': {'studies': [dossier_link('Amphetamines')]},
        'notes': ('Added 2026-10-30. "At twenty-four" puts it between December 1952 and '
                  'December 1953. Dossier: DRG-LET-1962-SEMOX, DRG-BIO-SUTIN-BERKELEY, '
                  'DRG-BIO-SUTIN-STANFORD.'),
    },
    {
        'id': 'pkd_bio_1964_first_lsd',
        'date': '1964',
        'date_precision': 'year',
        'event': ("PKD takes LSD for the first time — by most accounts in 1964 — and finds "
                  "himself in a frozen hell, judged, speaking Latin."),
        'category': 'drug_use',
        'entities': ['Ray Nelson', 'Jack Newkom'],
        'location': 'Oakland, California',
        'source': 'Sutin',
        'importance': 3,
        'narrative': (
            "Dick told Charles Platt in 1979 that he took LSD twice, the second dose perhaps not "
            "acid at all; the first sent him \"straight to hell\": a frozen landscape, a day of "
            "wrath, Latin. \"That was in 1964.\" A month later the galleys of Palmer Eldritch "
            "arrived and he could not read them. Sutin dates the first trip to 1964, from Jack "
            "Newkom, and counts at least two that year, one with Ray Nelson; Anne R. Dick tells "
            "the Nelson trip as the only one; Gregg Rickman put Dick's first LSD at about 1967. "
            "In 1976 Dick named one passage of A Maze of Death as drawn from the first trip."),
        'sources': [
            {'author': 'PKD', 'work': 'Interview by Charles Platt, May 17, 1979', 'lane': 'E',
             'locator': '', 'supports': 'two trips; the first in 1964'},
            src(SUTIN, 'Newkom, Nelson, and "at least two occasions"'),
            src(ANNE, 'the Nelson trip as the only one'),
        ],
        'quotes': [
            {'text': 'the fact of the matter is that I took it two times', 'speaker': 'PKD',
             'source': 'Interview by Charles Platt, May 17, 1979', 'lane': 'E'},
        ],
        'dispute': {
            'summary': 'When, and how many times.',
            'positions': [
                {'who': 'PKD (1975 letter; 1979 interview)', 'claim': 'twice; first in 1964'},
                {'who': 'Sutin', 'claim': 'at least two occasions in 1964'},
                {'who': 'Anne R. Dick', 'claim': 'one trip, after which he never tried it again'},
                {'who': 'Rickman (1984)', 'claim': 'two or three times, not until about 1967'},
            ],
        },
        'lanes': ['C', 'E'],
        'confidence': 'medium',
        'links': {'works': ['/exegesis/works/a-maze-of-death'],
                  'studies': [dossier_link('LSD')]},
        'notes': ('Added 2026-10-30. Dossier: DRG-INT-1979-TWICE, DRG-LET-1975-HEADTRIP, '
                  'DRG-BIO-SUTIN-ACID, DRG-BIO-ANNE-ONCE, DRG-SCH-RICKMAN-FACTS.'),
    },
    {
        'id': 'pkd_bio_1970_05_mescaline',
        'date': '1970-05',
        'date_precision': 'month',
        'event': ("A single large dose of mescaline gives PKD \"an overpowering love for other "
                  "people\", which he writes into Flow My Tears, the Policeman Said."),
        'category': 'drug_use',
        'entities': [],
        'location': 'San Rafael, California',
        'source': 'Letter to James, September 17, 1970',
        'importance': 3,
        'narrative': (
            "Dick credited mescaline, taken once in May 1970, with what acid never gave him: a "
            "flood of love for other people. He wrote Flow My Tears, the Policeman Said between "
            "March and August that year and told correspondents it was built on that dose. In "
            "the Exegesis he later dates to the same dose the moment a \"fugal\", always-high "
            "personality took over."),
        'sources': [
            letter('James', 'September 17, 1970', 'the dose and the novel'),
            src(SUTIN, 'May 1970, and the writing of Flow My Tears'),
        ],
        'quotes': [
            {'text': ('With acid I never had any genuine insights, but on the mescalin I was '
                      'overwhelmed by terribly powerful feelings'),
             'speaker': 'PKD', 'source': 'Letter to James, September 17, 1970', 'lane': 'E'},
        ],
        'lanes': ['C', 'E'],
        'confidence': 'high',
        'links': {'works': ['/exegesis/works/flow-my-tears-the-policeman-said'],
                  'studies': [dossier_link('Mescaline')]},
        'notes': 'Added 2026-10-30. Dossier: DRG-LET-1970-MESCALIN, DRG-EX-1978-DRIVENMAD.',
    },
    {
        'id': 'pkd_bio_1971_05_stanford_ward',
        'date': '1971-05-03',
        'date_precision': 'day',
        'event': ("PKD is admitted to the psychiatric ward of Stanford University Hospital for "
                  "three days, telling the examining psychiatrist he takes a thousand Methedrine "
                  "tablets a week."),
        'category': 'health',
        'entities': ['Dorothy Hudner', 'Joseph Hudner'],
        'location': 'Palo Alto, California',
        'source': 'Sutin',
        'importance': 3,
        'narrative': (
            "In spring 1971 Dick phoned his mother to say he was a drug addict who must quit or "
            "die. A girlfriend in Palo Alto took him to the Hoover Pavilion at Stanford, where he "
            "was admitted on May 3 and released on May 6. The examining psychiatrist recorded a "
            "thousand Methedrine tablets a week at $300 a month, with Stelazine, an \"astute\" "
            "intellect without delusions, and no physical addiction. Later that year his own "
            "psychiatrist in Marin, seeing no withdrawal, took his claims of addiction for "
            "hypochondria."),
        'sources': [
            src(SUTIN, 'the stepfather\'s notes and the Stanford records'),
            src(ANNE, 'the Marin psychiatrist\'s view of his addiction claims'),
        ],
        'quotes': [
            {'text': 'Phil said he was taking one thousand Methedrine tabs per week',
             'speaker': 'Sutin', 'source': 'Divine Invasions', 'lane': 'C'},
        ],
        'lanes': ['C'],
        'confidence': 'high',
        'links': {'studies': [dossier_link('Amphetamines')]},
        'notes': 'Added 2026-10-30. Dossier: DRG-BIO-SUTIN-STANFORD, DRG-BIO-ANNE-DRA.',
    },
    {
        'id': 'pkd_bio_1974_03_orthomolecular_vitamins',
        'date': '1974-03',
        'date_precision': 'month',
        'event': ("PKD takes massive doses of water-soluble \"orthomolecular\" vitamins to switch "
                  "on his right hemisphere; in mid-March, he writes, he got \"abrupt, dazzling "
                  "results\"."),
        'category': 'health',
        'entities': ['Robert Ornstein'],
        'location': 'Fullerton, California',
        'source': 'Letter to Malcolm Edwards, January 29, 1975',
        'importance': 4,
        'narrative': (
            "Having read Robert Ornstein on the right hemisphere and drafted a novel about "
            "drug-damaged brains, Dick took the orthomolecular vitamin formula on purpose in the "
            "weeks after the February pentothal, to improve his neural firing. Sutin traces the "
            "formula to a Psychology Today article of April 1974. Dick listed the vitamins, "
            "the pentothal and later lithium among the conditions of 2-3-74, always as "
            "disinhibitors rather than causes."),
        'sources': [
            letter('Malcolm Edwards', 'January 29, 1975', 'the plan and the result'),
            letter('Dorothy Hudner', 'September 15, 1976', 'the factors listed together'),
            src(SUTIN, 'the Psychology Today formula'),
        ],
        'quotes': [
            {'text': ('I was experimenting with the orthomolecular vitamin formula, and had '
                      'accidentally taken 7 grams of vitamin C, much more than is indicated.'),
             'speaker': 'PKD', 'source': 'Letter to Dorothy Hudner, September 15, 1976',
             'lane': 'E'},
        ],
        'dispute': {
            'summary': 'How much vitamin C.',
            'positions': [
                {'who': 'PKD (Exegesis, November 1975)', 'claim': 'an overdose of seven grams a day'},
                {'who': 'PKD (letter, September 1976)', 'claim': 'seven grams, taken by accident'},
                {'who': 'Sutin', 'claim': 'seven grams more than the formula called for'},
            ],
        },
        'lanes': ['B', 'C', 'E'],
        'confidence': 'high',
        'links': {'studies': [dossier_link('Vitamins')]},
        'notes': ('Added 2026-10-30. Dossier: DRG-LET-1975-SPLITBRAIN, DRG-LET-1976-PENTATHOL, '
                  'DRG-EX-1975-VITAMINC, DRG-BIO-SUTIN-VITAMINS.'),
    },
    {
        'id': 'pkd_bio_1977_09_metz_speed',
        'date': '1977-09',
        'date_precision': 'month',
        'event': ("Nervous about flying to the Metz festival in France, PKD scores a supply of "
                  "speed — by Sutin's account the only time in his last decade."),
        'category': 'drug_use',
        'entities': ['Joan Simpson'],
        'location': 'Metz, France',
        'source': 'Sutin',
        'importance': 2,
        'narrative': (
            "A year earlier Dick had told a student \"I take no drugs now at all\". Sutin records "
            "one lapse: amphetamines bought for the trip to Metz, where he was guest of honour. "
            "Arnold reports unnamed sources who say he was still abusing amphetamines in 1974; "
            "Doris Sauter remembered no amphetamines in his last years, but a little grass and "
            "a little coke."),
        'sources': [
            src(SUTIN, 'the supply for Metz'),
            letter('Dwayne Boggs', 'September 9, 1976', '"I take no drugs now at all"'),
            src(ANNE, 'Doris Sauter\'s account of his last years'),
        ],
        'quotes': [
            {'text': 'the only time he resorted to amphetamines in his final decade',
             'speaker': 'Sutin', 'source': 'Divine Invasions', 'lane': 'C'},
        ],
        'lanes': ['C', 'E'],
        'confidence': 'medium',
        'links': {'studies': [dossier_link('Sobriety')]},
        'notes': ('Added 2026-10-30. Dossier: DRG-BIO-SUTIN-METZ, DRG-LET-1976-BOGGS, '
                  'DRG-BIO-ARNOLD-COVERT, DRG-BIO-ANNE-DORIS.'),
    },
]
