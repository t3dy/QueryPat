"""
Biography additions for the November 1971 break-in at 707 Hacienda Way.

Applied by scripts/biography/apply_biography_curation.py. The research behind
it, and the leads for a full dossier, are in curation/breakin-1971/.
"""

SHINE = 'Letter to Inspector Shine, November 4, 1972'

REPLACE = {
    'pkd_bio_1971_burglary': {
        'narrative': (
            'No one was ever charged.',
            'In February 1972 the investigating inspector told Dick he had broken the case: '
            'a man named Jerry Wade had been arrested with Dick\'s Ruger .22 pistol, stolen in '
            'the robbery. Dick\'s letters record no outcome beyond that, and he went on '
            'theorising.'),
    },
}

APPEND = {
    'pkd_bio_1971_burglary': {
        'sources': [
            {'author': 'PKD', 'work': SHINE, 'lane': 'E', 'locator': '',
             'supports': 'the police report of an arrest with his stolen pistol, February 1972'},
        ],
        'quotes': [
            {'text': ('you informed me that you had broken the case; a man named Wade (Jerry Wade '
                      'I believe) had been arrested with the Ruger .22 pistol of mine stolen '
                      'during this robbery'),
             'speaker': 'PKD', 'source': SHINE, 'lane': 'E'},
        ],
        'dispute.positions': [
            {'who': 'Marin County police, as reported by PKD (letter, November 1972)',
             'claim': 'a burglary they considered solved: a suspect arrested with his stolen pistol'},
        ],
    },
}
