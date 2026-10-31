"""
Key-date checks on high-importance curated biography events.

Each of these events carried only a "Generated curation note" until 2026-10-30.
Their dates and claims were checked against Sutin's Divine Invasions, Anne R.
Dick's The Search for Philip K. Dick, Arnold's The Divine Madness and the
letters. Applied by scripts/biography/apply_biography_curation.py.

Confirmed as they stand, no change needed: the 1948 marriage to Jeanette Marlin
(six months; Sutin, Arnold), the June 1950 marriage to Kleo Apostolides (Sutin),
Christopher's birth on July 25, 1973 (Sutin, Anne R. Dick), the death on March
2, 1982 (Sutin), and "The Android and the Human" at the University of British
Columbia two days before VCon in February 1972 (Sutin, Anne R. Dick).
"""

SUTIN = {'author': 'Sutin', 'work': 'Divine Invasions', 'lane': 'C'}
ANNE = {'author': 'Anne R. Dick', 'work': 'The Search for Philip K. Dick', 'lane': 'C'}
ARNOLD = {'author': 'Arnold', 'work': 'The Divine Madness of Philip K. Dick', 'lane': 'C'}
BOUCHER = 'Letter to Anthony Boucher, April 25, 1962'


def checked(what: str) -> str:
    return (f"Checked 2026-10-30 against the biographies and letters in the archive: "
            f"{what} Earlier note: generated, unverified.")


CORRECTIONS = {
    'pkd_bio_1929_jane_death': {
        'date': '1929-01-26',
        'date_precision': 'day',
        # The first quote previously reversed the sentence's two halves around an
        # ellipsis; the Exegesis (April 1981, SEG_EXEG_1981-04-16_Pat_102) reads as
        # below. The second quote was already verbatim with an in-order elision.
        'quotes': [
            {'text': ('the ultimate problem confronting me all my life has been the senseless '
                      'injury to + neglect of my sister'),
             'speaker': 'PKD', 'source': 'Exegesis, April 1981', 'lane': 'B'},
            {'text': ('Last night, too, I had the eerie insight that "Mrs. Jack Vance," my '
                      'tutelary spirit, is my sister Jane... And I must be wary that she is '
                      'drawing me away from life and toward her.'),
             'speaker': 'PKD', 'source': 'Exegesis', 'lane': 'B'},
        ],
        'notes': checked("Sutin gives January 26, 1929; Anne R. Dick and Arnold agree that "
                         "Jane died on the way to, or soon after reaching, the hospital. The "
                         "first quote was corrected to the Exegesis's word order."),
    },
    'pkd_bio_1960_daughter_laura': {
        'date': '1960-02-25',
        'date_precision': 'day',
        'quotes': [
            {'text': 'Now my sister is made up for.', 'speaker': 'PKD, recalled by Anne R. Dick',
             'source': 'The Search for Philip K. Dick', 'lane': 'C'},
        ],
        'notes': checked("Sutin and Anne R. Dick both give February 25, 1960. Anne R. Dick "
                         "recalls what Phil said on seeing the baby; he chose the name."),
    },
    'pkd_bio_1982_stroke': {
        'date': '1982-02-18',
        'date_precision': 'day',
        'notes': checked("Anne R. Dick dates it Thursday, February 18: he phoned his doctor "
                         "that morning with pre-stroke symptoms, and his neighbours Juan and Su "
                         "Perez found him on the floor late that afternoon (Sutin names the "
                         "Perezes too). Arnold: the day after his last interview with Rickman."),
    },
    'pkd_bio_1973_marriage_tessa': {
        'dispute': {
            'summary': 'The year of the marriage.',
            'positions': [
                {'who': 'Sutin (Divine Invasions)',
                 'claim': 'April 1973, at their apartment, with Tessa pregnant with Christopher'},
                {'who': 'Arnold (The Divine Madness)',
                 'claim': 'in 1972 Dick married the eighteen-year-old Tessa Busby'},
            ],
        },
        'notes': checked("Sutin: \"In April they were married\" (1973), in a ceremony at "
                         "their apartment. The day, April 19, is not in the biographies in the "
                         "archive and is unverified. Arnold puts the marriage in 1972."),
    },
    'pkd_bio_1974_02_03_pink_light': {
        # Second quote had "magnet-like"; the transcription (SEG_EXEG_U_Henry_01)
        # reads "magnet like". Found by --verify run over every curated quote.
        'quotes': [
            {'text': ('The golden fish necklace told me it was time; I began my work, like the '
                      'worm constructing its cocoon.'),
             'speaker': 'PKD', 'source': 'Exegesis', 'lane': 'B'},
            {'text': ('And the fish sign I saw was made of gold. And I saw around me a prison, a '
                      'magnet like ring, of iron.'),
             'speaker': 'PKD', 'source': 'Exegesis', 'lane': 'B'},
        ],
    },
    'pkd_bio_1958_breakdown': {
        'notes': checked("Dick's own account is the 1962 letter to Anthony Boucher: on a "
                         "bridge over Papermill Creek at Point Reyes Station, cut off from the "
                         "people he had left behind in Berkeley, he was overwhelmed; the "
                         "stimulant that had freed him to move had, he says, delivered him to "
                         "the choice."),
    },
}

REPLACE = {
    'pkd_bio_1982_stroke': {
        'narrative': (
            'a neighbor, alarmed at not hearing from him, alerted help',
            'his neighbours Juan and Su Perez found him late in the afternoon of February 18, '
            'after he had phoned his doctor that morning describing pre-stroke symptoms,'),
    },
}

APPEND = {
    'pkd_bio_1960_daughter_laura': {
        'sources': [
            {**ANNE, 'locator': '', 'supports': 'the birth on February 25, 1960, and the naming'},
        ],
    },
    'pkd_bio_1982_stroke': {
        'sources': [
            {**ANNE, 'locator': '', 'supports': 'Thursday, February 18; the call to his doctor; the Perezes'},
        ],
    },
    'pkd_bio_1973_marriage_tessa': {
        'sources': [
            {**ARNOLD, 'locator': '', 'supports': 'dates the marriage to 1972'},
        ],
    },
    'pkd_bio_1958_breakdown': {
        'sources': [
            {'author': 'PKD', 'work': BOUCHER, 'lane': 'E', 'locator': '',
             'supports': "Dick's own account of the Point Reyes crisis"},
        ],
        'quotes': [
            {'text': ('In a way, I accidentally induced a momentary psychosis by such an abrupt '
                      'change of environment'),
             'speaker': 'PKD', 'source': BOUCHER, 'lane': 'E'},
        ],
        'links.studies': [
            {'to': '/studies/psychology/drugs-in-pkd?facet=Amphetamines#mentions',
             'label': 'Drugs in Philip K. Dick'},
        ],
    },
}
