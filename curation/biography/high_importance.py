"""
The remaining importance 4-5 curated biography events with only a "Generated
curation note", checked on 2026-10-30 against Sutin's Divine Invasions, Anne R.
Dick's The Search for Philip K. Dick, Arnold's The Divine Madness of Philip K.
Dick, the Selected Letters and the Exegesis in database/unified.sqlite.
Applied by scripts/biography/apply_biography_curation.py.

Sutin's chapters, used to correct locators: 1 Dec 1928-Jan 1929; 2 1929-1944;
3 1944-1950; 4 1950-1958; 5 1958-1963; 6 1963-1965; 7 1965-1970; 8 1970-1972;
9 1972-1974; 10 Feb 1974-Feb 1975; 11 1975-1978; 12 1979-1982. Arnold's ch. 7
("The Pink Light") ends with "The Exegesis Begins"; ch. 8 is "The Exegesis".

What was wrong:
- incubator: Philip went into the incubator the day Jane died on the way to the
  hospital, not "weeks after".
- Kleo: the marriage gave way to Anne in 1958 at Point Reyes, not "the mid-1950s".
- first story sale: "Roog", to Boucher at F&SF, October 1951.
- Palmer Eldritch: finished at Point Reyes (mailed March 1964), not Oakland.
- Zebra: named in December 1976 (Sutin; letter to Hurst, Feb 11, 1977), not
  March 1974. "VALIS" is older: in the Exegesis section filed under Sept 1975.
- CSUF talk: no July 1973 recording is attested; the letters show Dick lecturing
  to classes there from 1972.
- Exegesis begins: Arnold's stressors were misreported (no break-in or Jane in
  that passage; amphetamine use is alleged and unobserved by Tessa).
- Blade Runner: a news clip (June 1981) and a private effects-reel screening
  (November), not a set visit.
- death: his ashes, not his body, went to Fort Morgan.
- 1976 onward: Santa Ana, not Fullerton.
- UBC speech: Sutin and the letters say February 1972; the CSUF finding aid
  says March 1972. Recorded as a dispute.

Confirmed as they stand: the birth (Dec 16, 1928), the 1940 discovery of
Stirring Science Stories, the 1948 Marlin marriage, Solar Lottery (1955), High
Castle (Putnam, 1962), Androids (written 1966, published 1968), Ubik (written
1966, published 1969), Christopher (July 25, 1973), the Black Iron Prison as an
early image (letter to Gillespie, Jan 28, 1975), living information (1976
folder onward), The Divine Invasion (Simon & Schuster, 1981), the death on
March 2, 1982.
"""

SUTIN = {'author': 'Sutin', 'work': 'Divine Invasions', 'lane': 'C'}
ANNE = {'author': 'Anne R. Dick', 'work': 'The Search for Philip K. Dick', 'lane': 'C'}
ARNOLD = {'author': 'Arnold', 'work': 'The Divine Madness of Philip K. Dick', 'lane': 'C'}


def letter(to: str, date: str) -> str:
    return f'Letter to {to}, {date}'


def checked(what: str) -> str:
    return (f"Checked 2026-10-30 against the biographies, letters and Exegesis in the archive: "
            f"{what} Earlier note: generated, unverified.")


def sutin_ch(old: str, new: str) -> tuple:
    return ({'author': 'Sutin', 'locator': old}, {'locator': new})


CORRECTIONS = {
    'pkd_bio_1928_birth': {
        'notes': checked("Sutin: \"born six weeks prematurely, on December 16, 1928\", at home "
                         "in Chicago; Arnold agrees and adds that Edgar delivered the twins himself."),
    },
    'pkd_bio_1929_incubator': {
        'date': '1929-01-26',
        'date_precision': 'day',
        'event': ("Jane dies on the way to the hospital; the premature Philip, about a day from "
                  "death, is put into an incubator and survives."),
        'notes': checked("The event text said he was kept alive \"weeks after\" Jane died. Sutin "
                         "(quoting Dorothy's letter), Arnold and Anne R. Dick agree that both "
                         "babies were taken to the hospital together, Jane died on the way, and "
                         "Philip went into the incubator that day. Sutin dates Jane's death "
                         "January 26, 1929; Arnold names the incubator's inventor, Julian Hess."),
    },
    'pkd_bio_1940_sf_discovery': {
        'notes': checked("Sutin: at twelve (December 1940) he read his first SF magazine, "
                         "Stirring Science Stories, edited by Don Wollheim, who bought his first "
                         "novel in 1954; by 1941 he owned stacks of Astounding, Amazing and "
                         "Unknown. Sutin locator corrected from ch. 1 to ch. 2."),
    },
    'pkd_bio_1948_marriage_marlin': {
        'notes': checked("Sutin and Arnold: 1948, about six months. Sutin locator corrected "
                         "from ch. 2 to ch. 3."),
    },
    'pkd_bio_1950_marriage_kleo': {
        'date': '1950-06',
        'date_precision': 'month',
        'notes': checked("Sutin: June 1950. The narrative said the marriage gave way \"in the "
                         "mid-1950s\" to Anne Rubenstein; Phil and Kleo moved to Point Reyes "
                         "Station in September 1958 and he met Anne there that year. Sutin "
                         "locator corrected from ch. 2 to ch. 4."),
    },
    'pkd_bio_1951_first_story_sales': {
        'date': '1951-10',
        'date_precision': 'month',
        'notes': checked("Sutin quotes Dick: the first sale, in October 1951, was \"Roog\" to "
                         "Anthony Boucher's F&SF (Dick gives his age as twenty-one; he was "
                         "twenty-two). Sutin: stories in seven different pulps in June 1953. "
                         "Sutin locator corrected from ch. 3 to ch. 4."),
    },
    'pkd_bio_1954_ace_acceptance': {
        'notes': checked("Sutin: Wollheim bought it for Ace; the Meredith Agency had the "
                         "manuscript in March 1954; Dick's title was Quizmaster Take All, "
                         "Wollheim's Solar Lottery. Sutin locator corrected from ch. 3 to ch. 4."),
    },
    'pkd_bio_1955_solar_lottery': {
        'notes': checked("Sutin: 1955, well reviewed by Boucher, Analog and Damon Knight. "
                         "Sutin locator corrected from ch. 3 to ch. 4."),
    },
    'pkd_bio_1962_high_castle': {
        'notes': checked("Sutin: Putnam hardcover, 1962; Dick in a 1976 interview: \"I used the "
                         "I Ching to plot the book.\" Sutin adds that Dick tossed the coins "
                         "himself wherever a character consults the oracle."),
    },
    'pkd_bio_1963_hugo_award': {
        'date': '1963-09',
        'date_precision': 'month',
        'notes': checked("Sutin: September 1963, after Putnam sold the book to the Science "
                         "Fiction Book Club in late 1962; a local reporter photographed Dick with "
                         "the trophy. Anne R. Dick: the Baywood Press photographed Laura holding "
                         "it. The archive does not say whether Dick attended the convention; "
                         "the location is the convention's. Sutin locator corrected from ch. 6 "
                         "to ch. 5."),
    },
    'pkd_bio_1964_three_stigmata': {
        'location': 'Point Reyes Station, California',
        'notes': checked("Sutin: written 1964, mailed to the Meredith Agency in March 1964 (so "
                         "at Point Reyes, not Oakland), his first SF sale to Doubleday, published "
                         "1965. The face in the sky is from an unpublished headnote (c. 1976) "
                         "quoted by Sutin. The narrative's \"the book he was later most frightened "
                         "by\" had no source and was removed. Ellison recalls Dick calling the "
                         "novel LSD-inspired (see the Drugs dossier). Sutin locator corrected from "
                         "ch. 5 to ch. 6."),
    },
    'pkd_bio_1968_androids': {
        'notes': checked("Sutin: written in 1966, published 1968."),
    },
    'pkd_bio_1969_ubik': {
        'notes': checked("Sutin: written 1966, published 1969. The claim that Dick returns to "
                         "Ubik most often is a portal count over the transcribed Exegesis "
                         "segments (register D). Sutin locator corrected from ch. 6 to ch. 7."),
    },
    'pkd_bio_1972_vancouver': {
        'date': '1972-02',
        'date_precision': 'month',
        'notes': checked("Dick to June, July 30, 1973: \"I flew to Canada in February of last "
                         "year, made my two speeches\". Sutin locator corrected from ch. 7 to ch. 9."),
    },
    'pkd_bio_1972_ubc_lecture': {
        'dispute': {
            'summary': 'The month of the Vancouver speech.',
            'positions': [
                {'who': 'Sutin; Dick (letters)',
                 'claim': 'February 1972, at the convention and at the University of British Columbia'},
                {'who': 'CSUF finding aid (2016)',
                 'claim': 'delivered at the Vancouver convention and at UBC in March 1972'},
            ],
        },
        'notes': checked("Sutin and Dick's letters give February 1972; the CSUF manuscript "
                         "finding aid's catalogue entry says March 1972. Dick to John Bush, Sept "
                         "11, 1973: it was \"the first speech I ever wrote or gave\". \"The time I "
                         "made my UBC speech\" is from the letter to Hatie Rubenstein, Nov 30, 1975."),
    },
    'pkd_bio_1973_christopher_birth': {
        'notes': checked("Sutin and Anne R. Dick: July 25, 1973 (Christopher Kenneth Dick). A "
                         "duplicated clause in the narrative was removed. Sutin locator corrected "
                         "from ch. 7 to ch. 9."),
    },
    'pkd_bio_1973_csuf_talk': {
        'event': ("PKD lectures to classes at Cal State Fullerton, where Willis McNelly had "
                  "brought him in 1972 — part of his re-emergence into public life."),
        'confidence': 'low',
        'notes': checked("The entry said Dick recorded a talk at CSUF in July 1973. Neither the "
                         "letters, the biographies nor the CSUF finding aid attest it. The letters "
                         "show him lecturing to McNelly's classes from 1972 (Aug 30, 1972) and in "
                         "1973 (May 26; July 30). The id is kept. Sutin locator corrected from ch. "
                         "8 to ch. 9."),
    },
    'pkd_bio_1974_exegesis_begin': {
        'notes': checked("Sutin: the Exegesis was \"begun in 1974\"; the Selected Letters "
                         "chronology agrees. Arnold dates its beginning to after August 1974, when "
                         "the experiences waned. The earliest dated Exegesis material in the "
                         "archive is the folder filed under February 27, 1975. The narrative's "
                         "account of Arnold's stressors was corrected to what his text says. "
                         "Locators corrected: Arnold ch. 1 to ch. 7, Sutin ch. 8 to ch. 10."),
    },
    'pkd_bio_1974_03_zebra': {
        'event': ("The intelligence PKD met in March 1974 is the one he named 'Zebra' in "
                  "December 1976 — a mind that camouflages itself perfectly in the ordinary world."),
        'notes': checked("The entry said Dick named it Zebra in March 1974. Sutin dates the "
                         "\"Zebra Principle\" to December 1976, from Dick's earlier reading of a "
                         "study of insect mimicry; Dick told Mark Hurst on February 11, 1977 that "
                         "it came \"about a month and a half ago, while reworking VALIS\". The "
                         "earliest Exegesis use in the archive is in the folder filed under "
                         "September 1976. The date stays at March 1974, the experience named. "
                         "VALIS (filed under Sept 1975) is the older name, so Zebra is not "
                         "\"the first\"."),
    },
    'pkd_bio_1974_philosophical_speculation': {
        'notes': checked("Consistent with Sutin (Exegesis begun in 1974) and the archive (dated "
                         "Exegesis folders from February 1975)."),
    },
    'pkd_bio_1974_black_iron_prison': {
        'notes': checked("The image is early: Dick to Bruce Gillespie, January 28, 1975, \"I saw "
                         "the iron prison around us\". The name \"Black Iron Prison\" and \"the "
                         "Empire never ended\" first appear in the Exegesis folder filed under "
                         "September 1976, which runs to 1979, and in the letter to Hurst of "
                         "February 11, 1977."),
    },
    'pkd_bio_1974_exegesis_ongoing': {
        'location': 'Fullerton and Santa Ana, California',
        'notes': checked("Sutin: \"some eight thousand pages long\". He moved to Santa Ana in "
                         "1976 (Sutin; Selected Letters chronology). Locators corrected: Sutin "
                         "ch. 8-11 to ch. 10-12, Arnold ch. 1 to ch. 8."),
    },
    'pkd_bio_1976_living_information': {
        'location': 'Santa Ana, California',
        'notes': checked("\"Living information\" and \"plasmate\" first appear in the Exegesis "
                         "folder filed under September 1976 (runs to 1979); the range stands. "
                         "Location corrected: Dick moved to Santa Ana in 1976."),
    },
    'pkd_bio_1977_scanner_darkly': {
        'location': 'Santa Ana, California',
        'notes': checked("Doubleday, 1977. The narrative's \"closing dedication\" is the Author's "
                         "Note (Sutin). Location corrected: Santa Ana from 1976."),
    },
    'pkd_bio_1977_valis_theology': {
        'location': 'Santa Ana, California',
        'notes': checked("The name is older than the range: \"the VALIS A\" is in the Exegesis "
                         "section filed under September 1975, and Dick was writing Valisystem A "
                         "in August 1976 (letter to Tessa, Aug 18, 1976). Sutin: VALIS written "
                         "in a two-week burst in November 1978. Location corrected to Santa Ana."),
    },
    'pkd_bio_1981_blade_runner_visit': {
        'event': ("Hostile to the early Blade Runner script, PKD is won over by the footage — a "
                  "news clip in June 1981, then a private screening of the effects reel in "
                  "November, where he poses with Ridley Scott."),
        'notes': checked("Sutin describes no set visit: Dick read Fancher's screenplay in "
                         "December 1980 and loathed it; in June 1981 he saw a clip on the local "
                         "news; in November the studio invited him to a private showing of a "
                         "special-effects reel. The Selected Letters chronology: \"sees first "
                         "scenes from Blade Runner ... on TV\". The id is kept. Sutin locator "
                         "corrected from ch. 11 to ch. 12."),
    },
    'pkd_bio_1981_divine_invasion': {
        'location': 'Santa Ana, California',
        'notes': checked("Simon & Schuster, 1981; Dick to Ben Adams, January 20, 1981, expected "
                         "it \"this coming April\". Location and Sutin locator (ch. 11 to ch. 12) "
                         "corrected."),
    },
    'pkd_bio_1982_death': {
        'notes': checked("Sutin: March 2, 1982, after further strokes and heart failure. Anne "
                         "R. Dick: Edgar had his ashes flown to Fort Morgan and buried beside "
                         "Jane (the narrative said \"his body\"). Arnold: the parents engraved "
                         "Philip's name beside Jane's on her gravestone, with \"Twins\" under both."),
    },
}

REPLACE = {
    'pkd_bio_1929_incubator': {
        'narrative': (
            'Jane died in January 1929; Philip was kept alive in an incubator and pulled through.',
            'On January 26, 1929, both were rushed to the hospital; Jane died on the way. Philip, '
            'about a day from death, was put into an incubator and fed a special formula, and '
            'pulled through.'),
    },
    'pkd_bio_1940_sf_discovery': {
        'narrative': (
            "the era's *Stirring Science Stories* and *Astounding* among them",
            "his first was *Stirring Science Stories*, edited by Donald Wollheim, who would buy "
            "his first novel; by 1941 he owned stacks of *Astounding*, *Amazing* and *Unknown*"),
    },
    'pkd_bio_1950_marriage_kleo': {
        'narrative': (
            'until it gave way in the mid-1950s to his involvement with Anne Rubenstein',
            'and the move to Point Reyes Station in September 1958, where it gave way that year '
            'to his involvement with Anne Williams Rubenstein'),
    },
    'pkd_bio_1951_first_story_sales': {
        'narrative': (
            'In 1951-52 Philip broke through as a professional,',
            'In October 1951 Philip sold his first story, "Roog", to Anthony Boucher at *The '
            'Magazine of Fantasy and Science Fiction*; from there he broke through as a '
            'professional,'),
    },
    'pkd_bio_1954_ace_acceptance': {
        'narrative': (
            "Ace Books took *Solar Lottery* for its paperback line",
            "Donald Wollheim at Ace Books bought *Solar Lottery* (Dick's title was *Quizmaster "
            "Take All*; the Meredith Agency had the manuscript by March 1954) for its paperback "
            "line"),
    },
    'pkd_bio_1963_hugo_award': {
        'narrative': (
            'Sutin dates the win to 1963 and treats it',
            'Sutin dates the win to September 1963, credits the Science Fiction Book Club edition '
            'of late 1962 with winning the fans, and treats it'),
    },
    'pkd_bio_1964_three_stigmata': {
        'narrative': (
            'In 1964, in the middle of an astonishingly prolific run, Philip wrote',
            'In the middle of an astonishingly prolific run at Point Reyes, Philip wrote, and in '
            'March 1964 sent off,'),
    },
    'pkd_bio_1969_ubik': {
        'narrative': (
            'the single work he returns to most in the Exegesis after *VALIS* itself.',
            'the earlier novel of his own he returns to most often in the Exegesis (by a portal '
            'count, its title appears in 425 transcribed Exegesis segments, against 60 for '
            '*Palmer Eldritch*).'),
    },
    'pkd_bio_1973_christopher_birth': {
        'narrative': (
            ' — an intuition he credited to the March 1974 intelligence, the most-cited',
            ', the most-cited'),
    },
    'pkd_bio_1973_csuf_talk': {
        'narrative': (
            'In July 1973, newly settled in Orange County, Philip recorded a talk at California '
            'State University, Fullerton. It marks',
            'By mid-1973 Philip was lecturing to college classes at California State University, '
            'Fullerton. The connection began in April 1972, when Willis McNelly brought him down '
            'from Vancouver to archive his manuscripts in the library\'s special collections. (A '
            'recorded talk in July 1973, which this entry once described, is not attested in the '
            'letters, the biographies or the CSUF finding aid.) The lecturing marks'),
    },
    'pkd_bio_1974_exegesis_begin': {
        'narrative': (
            'situates its beginning within a cluster of stressors — the recent oral surgery and '
            'anesthesia, an amphetamine-era baseline, the unresolved 1971 break-in, and the long '
            'grief over his twin Jane — that the writing tries to metabolize into meaning.',
            'sets 2-3-74 within a cluster of stressors — unpaid taxes and fear of the IRS, '
            'poverty, a new baby, a botched extraction of an impacted tooth, Percodan, '
            'blood-pressure medication and psychiatric prescriptions (by some accounts lithium), '
            'and amphetamine use that some allege but Tessa did not observe — and dates the '
            'Exegesis to after August 1974, when the experiences waned and the theorizing took '
            'over.'),
    },
    'pkd_bio_1974_03_zebra': {
        'narrative': (
            'In March 1974 Philip began calling the intelligence he believed was acting on him '
            '*Zebra*:',
            'The intelligence he believed acted on him in March 1974 he named *Zebra* only in '
            'December 1976, when the "Zebra Principle" came to him while he was reworking '
            '*VALIS*:'),
    },
    'pkd_bio_1974_black_iron_prison': {
        'narrative': (
            '*the Empire never ended*.',
            '*the Empire never ended*. The image is early — in January 1975 he wrote that he had '
            'seen "the iron prison around us" while Nixon was still in office — but the name and '
            'the phrase first appear in the Exegesis folder filed under September 1976.'),
    },
    'pkd_bio_1977_valis_theology': {
        'narrative': (
            'toward a system he named for VALIS — Vast Active Living Intelligence System:',
            'toward a system named for VALIS — Vast Active Living Intelligence System, a name '
            'already in the Exegesis by 1975 and in *Valisystem A*, the novel he was writing in '
            'August 1976:'),
    },
    'pkd_bio_1977_scanner_darkly': {
        'narrative': (
            'a closing dedication naming friends dead or damaged by drugs',
            "a closing Author's Note listing friends dead or damaged by drugs"),
    },
    'pkd_bio_1981_blade_runner_visit': {
        'narrative': (
            'In 1981 Philip visited the production of *Blade Runner*, the adaptation of *Do '
            'Androids Dream of Electric Sheep?*, and met director Ridley Scott. Initially wary of '
            'Hollywood and critical of early script drafts, he was reportedly stunned by the '
            'special-effects footage of the future Los Angeles — recognizing his own imagined '
            'world on the screen.',
            'In 1981 Philip moved from hostility to enthusiasm over *Blade Runner*, the adaptation '
            'of *Do Androids Dream of Electric Sheep?*. He loathed Hampton Fancher\'s screenplay, '
            'read in December 1980, and took a swipe at Ridley Scott\'s *Alien* in print early in '
            '1981. In June he saw a short clip from the film on the local news and was pleased; '
            'in November the studio invited him to a private showing of a reel of special '
            'effects, sending a limousine, and he posed with Ridley Scott for publicity stills.'),
    },
    'pkd_bio_1982_death': {
        'narrative': (
            'His body was taken to Fort Morgan, Colorado,',
            'His ashes were flown to Fort Morgan, Colorado,'),
    },
}

AMEND = {
    'pkd_bio_1940_sf_discovery': {'sources': [sutin_ch('ch. 1', 'ch. 2')]},
    'pkd_bio_1948_marriage_marlin': {'sources': [sutin_ch('ch. 2', 'ch. 3')]},
    'pkd_bio_1950_marriage_kleo': {'sources': [sutin_ch('ch. 2', 'ch. 4')]},
    'pkd_bio_1951_first_story_sales': {'sources': [sutin_ch('ch. 3', 'ch. 4')]},
    'pkd_bio_1954_ace_acceptance': {'sources': [sutin_ch('ch. 3', 'ch. 4')]},
    'pkd_bio_1955_solar_lottery': {'sources': [sutin_ch('ch. 3', 'ch. 4')]},
    'pkd_bio_1963_hugo_award': {'sources': [sutin_ch('ch. 6', 'ch. 5')]},
    'pkd_bio_1964_three_stigmata': {'sources': [sutin_ch('ch. 5', 'ch. 6')]},
    'pkd_bio_1969_ubik': {'sources': [sutin_ch('ch. 6', 'ch. 7')]},
    'pkd_bio_1972_vancouver': {'sources': [sutin_ch('ch. 7', 'ch. 9')]},
    'pkd_bio_1973_christopher_birth': {'sources': [sutin_ch('ch. 7', 'ch. 9')]},
    'pkd_bio_1973_csuf_talk': {'sources': [sutin_ch('ch. 8', 'ch. 9')]},
    'pkd_bio_1974_exegesis_begin': {'sources': [
        sutin_ch('ch. 8', 'ch. 10'),
        ({'author': 'Arnold', 'locator': 'ch. 1'}, {'locator': 'ch. 7'}),
    ]},
    'pkd_bio_1974_exegesis_ongoing': {'sources': [
        sutin_ch('ch. 8-11', 'ch. 10-12'),
        ({'author': 'Arnold', 'locator': 'ch. 1'}, {'locator': 'ch. 8'}),
    ]},
    'pkd_bio_1981_blade_runner_visit': {'sources': [sutin_ch('ch. 11', 'ch. 12')]},
    'pkd_bio_1981_divine_invasion': {'sources': [sutin_ch('ch. 11', 'ch. 12')]},
}

APPEND = {
    'pkd_bio_1929_incubator': {
        'sources': [
            {**ARNOLD, 'locator': 'ch. 1',
             'supports': 'Jane died on the way to the hospital; Julian Hess\'s incubator'},
            {**ANNE, 'locator': '', 'supports': 'Phil in the incubator two weeks; Jane died soon after'},
        ],
        'lanes': ['C'],
    },
    'pkd_bio_1940_sf_discovery': {
        'quotes': [
            {'text': ('I came across the magazine quite by accident; I was actually looking for '
                      'POPULAR SCIENCE. I was most amazed. Stories about science?'),
             'speaker': 'PKD, quoted by Sutin', 'source': 'Divine Invasions', 'lane': 'E'},
        ],
    },
    'pkd_bio_1951_first_story_sales': {
        'entities': ['Anthony Boucher', 'The Magazine of Fantasy and Science Fiction'],
        'quotes': [
            {'text': ('In October, 1951, when I was twenty-one years old, I sold my first story: '
                      'a tiny fantasy to F&SF, the magazine which Tony Boucher edited.'),
             'speaker': 'PKD, quoted by Sutin', 'source': 'Divine Invasions', 'lane': 'E'},
        ],
    },
    'pkd_bio_1955_solar_lottery': {
        'quotes': [
            {'text': "Isn't it a hell of a thing that this is the one they picked up first?",
             'speaker': 'PKD, recalled by Kleo', 'source': 'Divine Invasions', 'lane': 'C'},
        ],
    },
    'pkd_bio_1962_high_castle': {
        'quotes': [
            {'text': 'I used the I Ching to plot the book.',
             'speaker': 'PKD, 1976 interview quoted by Sutin', 'source': 'Divine Invasions',
             'lane': 'E'},
        ],
    },
    'pkd_bio_1963_hugo_award': {
        'sources': [
            {**ANNE, 'locator': '', 'supports': 'the Baywood Press photograph of Laura with the Hugo'},
        ],
    },
    'pkd_bio_1964_three_stigmata': {
        'quotes': [
            {'text': 'it was a vast visage of perfect evil',
             'speaker': 'PKD, unpublished headnote quoted by Sutin', 'source': 'Divine Invasions',
             'lane': 'E'},
            {'text': ('Once, during the years of the Terrible Separation, I saw Palmer Eldritch in '
                      'the Sun -- I saw God backward'),
             'speaker': 'PKD', 'source': 'Exegesis', 'lane': 'B'},
        ],
    },
    'pkd_bio_1972_vancouver': {
        'sources': [
            {'author': 'PKD', 'work': letter('June', 'July 30, 1973'), 'lane': 'E', 'locator': '',
             'supports': 'flew to Canada in February 1972 and gave two speeches'},
        ],
        'quotes': [
            {'text': 'I flew to Canada in February of last year, made my two speeches',
             'speaker': 'PKD', 'source': letter('June', 'July 30, 1973'), 'lane': 'E'},
        ],
        'lanes': ['E'],
    },
    'pkd_bio_1972_ubc_lecture': {
        'sources': [
            {'author': 'CSUF University Archives', 'work': 'Philip K. Dick Manuscript Collection '
             'Finding Aid (2016)', 'lane': 'C', 'locator': 'Box 4, Folder 1',
             'supports': 'catalogues the speech as delivered in March 1972'},
        ],
        'quotes': [
            {'text': 'It is, oddly, the first speech I ever wrote or gave.',
             'speaker': 'PKD', 'source': letter('John Bush', 'September 11, 1973'), 'lane': 'E'},
        ],
    },
    'pkd_bio_1973_christopher_birth': {
        'sources': [
            {**ANNE, 'locator': '', 'supports': 'Christopher Kenneth Dick, born July 25, 1973'},
        ],
    },
    'pkd_bio_1973_csuf_talk': {
        'quotes': [
            {'text': 'I lecture at the nearby University and we see many s-f people.',
             'speaker': 'PKD', 'source': letter('Susan', 'May 26, 1973'), 'lane': 'E'},
            {'text': "I've been so busy with my writing, plus lecturing both to college classes "
                     "and on the radio here",
             'speaker': 'PKD', 'source': letter('June', 'July 30, 1973'), 'lane': 'E'},
        ],
    },
    'pkd_bio_1974_exegesis_begin': {
        'quotes': [
            {'text': ('I suffered total psychosis in 1974. Poverty, family responsibility (a new '
                      'baby) did it. & fear of the IRS.'),
             'speaker': 'PKD, 1978 journal entry quoted by Arnold',
             'source': 'The Divine Madness of Philip K. Dick', 'lane': 'B'},
        ],
    },
    'pkd_bio_1974_03_zebra': {
        'sources': [
            {**SUTIN, 'locator': 'ch. 11', 'supports': 'dates the "Zebra Principle" to December 1976'},
            {'author': 'PKD', 'work': letter('Mark Hurst', 'February 11, 1977'), 'lane': 'E',
             'locator': '', 'supports': 'the Zebra Principle came "about a month and a half ago"'},
        ],
        'quotes': [
            {'text': ('about a month and a half ago, while reworking VALIS, the idea—not an idea '
                      'but THE IDEA—suddenly popped fullblown into my mind'),
             'speaker': 'PKD', 'source': letter('Mark Hurst', 'February 11, 1977'), 'lane': 'E'},
        ],
        'lanes': ['C', 'E'],
    },
    'pkd_bio_1974_black_iron_prison': {
        'sources': [
            {'author': 'PKD', 'work': letter('Bruce Gillespie', 'January 28, 1975'), 'lane': 'E',
             'locator': '', 'supports': 'the iron prison seen in 1974, "while Nixon was still in office"'},
        ],
        'quotes': [
            {'text': 'Also I saw the iron prison around us (this was while Nixon was still in office)',
             'speaker': 'PKD', 'source': letter('Bruce Gillespie', 'January 28, 1975'), 'lane': 'E'},
        ],
        'lanes': ['E'],
    },
    'pkd_bio_1977_valis_theology': {
        'sources': [
            {**SUTIN, 'locator': 'ch. 11', 'supports': 'VALIS written in two weeks, November 1978'},
            {'author': 'PKD', 'work': letter('Tessa Dick', 'August 18, 1976'), 'lane': 'E',
             'locator': '', 'supports': 'writing Valisystem A in August 1976'},
        ],
        'lanes': ['C', 'E'],
    },
    'pkd_bio_1977_scanner_darkly': {
        'quotes': [
            {'text': 'I myself, I am not a character in the novel; I am the novel.',
             'speaker': 'PKD', 'source': "A Scanner Darkly, Author's Note (quoted by Sutin)",
             'lane': 'E'},
        ],
        'lanes': ['E'],
    },
    'pkd_bio_1981_blade_runner_visit': {
        'sources': [
            {'author': 'PKD', 'work': letter('Mark Hurst', 'March 8, 1981'), 'lane': 'E',
             'locator': '', 'supports': 'production about to begin; offices set up in Burbank'},
        ],
        'lanes': ['E'],
    },
    'pkd_bio_1981_divine_invasion': {
        'sources': [
            {'author': 'PKD', 'work': letter('Ben Adams', 'January 20, 1981'), 'lane': 'E',
             'locator': '', 'supports': 'Simon & Schuster publication expected that April'},
        ],
        'lanes': ['E'],
    },
    'pkd_bio_1982_death': {
        'sources': [
            {**ANNE, 'locator': '', 'supports': "Edgar had Phil's ashes flown to Fort Morgan and buried beside Jane"},
        ],
        'quotes': [
            {'text': ("when Dick's parents buried his sister, they engraved Dick's name on the "
                      "tombstone next to Jane's name"),
             'speaker': 'Arnold', 'source': 'The Divine Madness of Philip K. Dick', 'lane': 'C'},
        ],
    },
}
