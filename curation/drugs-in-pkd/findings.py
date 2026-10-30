#!/usr/bin/env python3
"""
Hand-classified findings for the "Drugs in Philip K. Dick" dossier.

Each finding names a source, a verbatim anchor inside it, an extraction window,
and the editorial card: `context` summarises the whole passage in the portal's
voice, `pith` quotes the sentence it turns on. The seeder extracts the passage
at the anchor, and refuses to build if an anchor does not resolve or a pith is
not verbatim in its source.

`concepts` doubles as the page's facet vocabulary: substances first, then
Dick's works, themes, people and biographers. The facet list in
dossier_sections.py names which are browsable.

Every passage here was read and chosen by hand from a sweep of the whole corpus
(scripts/research/sweep_corpus.py --profile drugs). The lexicon topic
psychology/amphetamine-use matched the bare word "speed" and is not a source:
of its 116 passages, 112 matched only that word, and most are about velocity.

Registers: A = PKD's own words, B = primary-source fact, C = scholarly
argument, D = portal-editor inference. Lanes follow the studies convention:
A fiction, B Exegesis, C scholarship, D biography, E letters, interviews and
Dick's own non-fiction paratext.

Run build_inventory.py to write evidence-inventory.json.
"""

# --------------------------------------------------------------------------
# Evidence packets: the claims the page makes, each backed by the findings
# that carry its id.
# --------------------------------------------------------------------------

PACKETS = [
    ('DRG-PKT-AMPH', 'strong',
     "Dick took amphetamines for roughly twenty years, from the early 1950s to 1972: "
     "first as prescribed Semoxydrine (methamphetamine), then in escalating and "
     "partly street-bought quantities. He gave two reasons, depression and the "
     "volume of writing his low advances demanded.",
     "Letters of 1962–1976, the Platt interview (1979), Exegesis section 016, and "
     "the three biographies. The figures differ: 'about 18 years' (1976), 'twenty "
     "years' (Rickman), 'nearly twenty years' (Sutin)."),
    ('DRG-PKT-PSYCHEDELICS', 'strong',
     "Dick's psychedelic experience was small and mostly bad: LSD on two or three "
     "occasions from 1964, one large dose of mescaline in May 1970 that he credited "
     "with the love in Flow My Tears, the Policeman Said, and a 1968 dose of what "
     "turned out to be PCP. How many times, and when, the sources dispute.",
     "Letters of 1965–1977, the Vertex (1974) and Platt (1979) interviews, Sutin, "
     "Anne R. Dick and Rickman."),
    ('DRG-PKT-ELDRITCH', 'strong',
     "Dick repeatedly said The Three Stigmata of Palmer Eldritch (written 1964) "
     "was written before he had taken LSD, from reading; Harlan Ellison printed in "
     "1967 that it was LSD-inspired, apparently with Dick's encouragement.",
     "Letters of 1967 and 1969, the Vertex and Platt interviews, Sutin and Anne R. "
     "Dick. They disagree on the source of the novel's drugs: an article by Aldous "
     "Huxley, or reading about hallucinogenic mushrooms."),
    ('DRG-PKT-MARIN', 'strong',
     "After Nancy Hackett left in 1970, Dick's Santa Venetia house became a "
     "crash-pad for young users and his amphetamine use peaked: by his own report "
     "to a psychiatrist in 1971, a thousand Methedrine tablets a week.",
     "Letters of 1970, VALIS (fiction), Sutin, Anne R. Dick's interviews with the "
     "house's residents, and Arnold."),
    ('DRG-PKT-XKALAY', 'strong',
     "After a suicide attempt in Vancouver in March 1972 Dick spent some weeks at "
     "X-Kalay, a Synanon-style rehabilitation house for heroin addicts, and came "
     "out an evangelist against drugs. By 1975 he thought its lessons faulty, and "
     "later compared its 'game' to brainwashing.",
     "Letters of 1972–1975, Exegesis 1976–79, the Vertex interview, Sutin."),
    ('DRG-PKT-SCANNER', 'strong',
     "A Scanner Darkly (written 1973, published 1977) is Dick's account of the "
     "1970–72 drug culture: its characters are based on people he knew, its "
     "Author's Note lists the dead and damaged, and it puts Dick himself on the "
     "list. He later read it as being about something other than drugs.",
     "The novel and its Author's Note; letters of 1973–1977; the Rickman "
     "interview (1981); the Exegesis, 1976–80."),
    ('DRG-PKT-FICTION', 'strong',
     "Dick's fictional drugs are almost all traps: Can-D and Chew-Z, JJ-180, "
     "Substance D. Each one is addictive, each one is owned by someone, and in each "
     "the user's reality becomes another's.",
     "Now Wait for Last Year, A Scanner Darkly and VALIS in this archive; The Three "
     "Stigmata of Palmer Eldritch through Dick's comments and criticism (the "
     "novel's text is not in the corpus)."),
    ('DRG-PKT-2374', 'strong',
     "Dick named chemical factors in the experiences of February–March 1974 — "
     "sodium pentothal from oral surgery, a large dose of water-soluble vitamins, "
     "lithium — but held that they disinhibited something rather than produced it.",
     "Letters of 1975–1981, Exegesis 1975–80, Sutin."),
    ('DRG-PKT-SACRAMENT', 'moderate',
     "In the Exegesis Dick turned intoxication into theology: John Allegro's "
     "sacred mushroom, Hofmann on LSD at Eleusis, Dionysos; mankind 'drugged + "
     "intoxicated' in a false world; Substance D as a picture of the human "
     "condition. He also says 2-3-74 was not a drug experience.",
     "Exegesis 1976–80."),
    ('DRG-PKT-BIOGRAPHERS', 'strong',
     "The biographers disagree on how much and when: Anne R. Dick's Point Reyes "
     "years against Arnold's 'massive doses'; Sutin's two LSD trips against Anne R. "
     "Dick's one; Arnold's amphetamine psychosis against Rickman's 'imagination'; "
     "Sutin's sobriety after 1972 against Arnold's 'some assert'.",
     "Sutin (1989), Rickman (1984), Anne R. Dick (1995/2010), Arnold (2016). "
     "Anthony Peake's biography is catalogued but its text is not in this archive."),
]


# --------------------------------------------------------------------------
# Sources
# --------------------------------------------------------------------------

LASTINT = 'DOC_ARCH_OCEANOFPDF_COM_THE_LAST_INTERVIEW_AND_OT'
MAGINT = 'DOC_ARCH_PKD_MAGAZINE_INTERVIEWS'
RICKMAN = 'DOC_ARCH_PHILIP_K_DICK_IN_HIS_OWN_WORDS_GREGG_RIC'
FIVE = 'DOC_ARCH_OCEANOFPDF_COM_FIVE_GREAT_NOVELS_THE_THR'   # A Scanner Darkly
NOWWAIT = 'DOC_ARCH_DICK_PHILIP_K_NOW_WAIT_FOR_LAST_YEAR_LIB'
VALIS3 = 'DOC_ARCH_OCEANOFPDF_COM_THE_VALIS_TRILOGY_PHILIP_'
SUTIN = 'DOC_ARCH_DIVINE_INVASIONS_A_LIFE_OF_PHI_LAWRENCE_'
ANNE = 'DOC_ARCH_OCEANOFPDF_COM_THE_SEARCH_FOR_PHILIP_K_D'
ARNOLD = 'DOC_ARCH_OCEANOFPDF_COM_THE_DIVINE_MADNESS_OF_PHI'
BUTLER = 'DOC_ARCH_ANDREW_M_BUTLER_PHILIP_K_DICK_REVISED_AN'
JAMESON = 'DOC_ARCH_FREDRIC_JAMESON_ARCHAEOLOGIES_OF_THE_FUT'

C_SUTIN = 'Lawrence Sutin, Divine Invasions: A Life of Philip K. Dick (1989)'
C_ANNE = 'Anne R. Dick, The Search for Philip K. Dick (1995; Tachyon edition 2010)'
C_ARNOLD = 'Kyle Arnold, The Divine Madness of Philip K. Dick (2016)'
C_RICKMAN = 'Gregg Rickman, Philip K. Dick: In His Own Words (1984)'
C_SCANNER = 'A Scanner Darkly (1977)'

# Exegesis section citations
S13 = 'Exegesis, section of November 1975'
SDOR = 'Exegesis, folder filed with September 1976 (written 1976–79)'
S16 = 'Exegesis, section 016 (1978–1980)'


# Each finding:
#   (id, kind, source_id, citation, anchor, window, packet, claim_type,
#    concepts, context, pith, dated, dating_basis, dating_confidence,
#    editorial_note) — the speaker comes from SPEAKER / AUTHOR below
# kind: exegesis_segment | letter | interview | paratext | fiction | biography |
#       criticism

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


# Who speaks the pith of a non-Dick passage. Interviews and the Author's Note
# are Dick; biography and criticism default to the author of the book, unless
# the pith quotes a witness; fiction is always a character or the narrator.
AUTHOR = {SUTIN: 'Lawrence Sutin', ANNE: 'Anne R. Dick', ARNOLD: 'Kyle Arnold',
          RICKMAN: 'Gregg Rickman', BUTLER: 'Andrew M. Butler',
          JAMESON: 'Fredric Jameson'}
SPEAKER = {
    'DRG-FIC-SCANNER-BUGS': 'The narrator',
    'DRG-FIC-SCANNER-SLOWDEATH': 'Fred (Bob Arctor)',
    'DRG-FIC-SCANNER-HEMISPHERES': 'A police psychologist',
    'DRG-FIC-SCANNER-FIELD': 'Bruce',
    'DRG-FIC-NOWWAIT-ADDICT': 'Corning',
    'DRG-FIC-NOWWAIT-HASTINGS': 'The narrator',
    'DRG-FIC-VALIS-UPPERS': 'The narrator (Horselover Fat)',
    'DRG-FIC-VALIS-PLAGUE': 'The narrator (Horselover Fat)',
    'DRG-BIO-ANNE-SEVENTY': 'Nancy Hackett, quoted by Anne R. Dick',
    'DRG-BIO-ANNE-POT': 'Cindy, quoted by Anne R. Dick',
    'DRG-BIO-ANNE-DORIS': 'Doris Sauter, quoted by Anne R. Dick',
    'DRG-BIO-SUTIN-ARK': 'Tim Powers, quoted by Lawrence Sutin',
    'DRG-INT-1981-RECORD': 'Philip K. Dick',
}


def doc(fid, kind, doc_id, cite, anchor, win, pkt, ctype, concepts, context,
        pith, dated=None, basis=None, conf=None, note=None):
    speaker = SPEAKER.get(fid) or AUTHOR.get(doc_id) or 'Philip K. Dick'
    if kind == 'fiction' and fid not in SPEAKER:
        raise ValueError(f'{fid}: fiction needs a speaker in SPEAKER')
    F.append(dict(id=fid, kind=kind, source_id=doc_id, citation=cite,
                  anchor=anchor, window=win, packet=pkt, claim_type=ctype,
                  concepts=concepts, context=context, pith=pith, speaker=speaker,
                  dated=dated, dating_basis=basis, dating_confidence=conf,
                  note=note))


# ==========================================================================
# 1. Amphetamines: the letters of the 1960s
# ==========================================================================

let('DRG-LET-1962-SEMOX', 'LET_1962-04-25_ANTHONY_BOUCHER_0060',
    'Letter to Anthony Boucher, April 25, 1962',
    'I stumbled on a stimulant drug called semoxydrene', [500, 420],
    'DRG-PKT-AMPH', 'self_report',
    ['Amphetamines', 'Self-medication', 'Prescription'],
    "A long autobiographical letter about agoraphobia. Dick says that at twenty-"
    "four — around 1952–53 — two things pulled him out of a closing-in world: "
    "teaching himself to drive, and a stimulant he spells semoxydrene. The first "
    "5 mg, he writes, gave back the clarity he had been losing for fifteen years "
    "and let him see the delusion he had been living in. Later in the letter the "
    "\"little green pills\" save him and then deliver him to a disastrous move. "
    "The earliest dated account of his amphetamine use in the archive, and it is "
    "an account of a cure.",
    'the first 5 mg which I took cleared away the cobwebs from my brain',
    '25 April 1962',
    note="Semoxydrine was a brand of methamphetamine hydrochloride (Dick learns "
         "this himself in October 1964: DRG-LET-1964-BROCHURE).")

let('DRG-LET-1964-SUPPLY', 'LET_1964-09-24_CAROL_CARR_0068',
    'Letter to Carol Carr, September 24, 1964',
    'my supply of amphetamines has dried up', [260, 260],
    'DRG-PKT-AMPH', 'self_report', ['Amphetamines', 'Prescription'],
    "A comic letter from Oakland, months after leaving Anne and the Point Reyes "
    "house. In among the cats and the Avon Lady, Dick complains that his "
    "amphetamines have run out despite two open prescriptions, and jokes about "
    "something injectable instead. The tone is play; the fact underneath is that "
    "by 1964 he was managing a supply.",
    "I don’t even know why my supply of amphetamines has dried up, and I had two "
    "open prescriptions.",
    '24 September 1964')

let('DRG-LET-1964-BROCHURE', 'LET_1964-10-22_TERRY_CAROL_CARR_0077',
    'Letter to Terry and Carol Carr, October 22, 1964',
    'I am up to six 7.5 mg of them a day', [520, 420],
    'DRG-PKT-AMPH', 'self_report', ['Amphetamines', 'Prescription'],
    "Dick reports to the Carrs that a druggist forgot to remove the brochure from "
    "his refill, so after seven years (\"or is it nine?\") he has finally read "
    "what his pills are: semoxydrine hydrochloride is methamphetamine. He is up to "
    "the strongest dose, six a day, and quotes the warning that overdose can cause "
    "hallucinations and death with mock horror. Sutin reprints the passage as the "
    "epigraph to his account of these years.",
    'I am up to six 7.5 mg of them a day, and 7.5 is their strongest dose',
    '22 October 1964')

let('DRG-LET-1967-PSYCHOSIS', 'LET_1967-07-18_RICH_BROWN_0126',
    'Letter to Rich Brown, July 18, 1967',
    'how does the LSD experience resemble an actual, authentic psychotic interlude',
    [120, 900],
    'DRG-PKT-PSYCHEDELICS', 'self_report', ['LSD', 'Psychosis'],
    "Written for a fanzine discussion. Dick compares an eight-hour psychotic "
    "episode of a few weeks earlier — triggered, he thinks, by deaths and money "
    "troubles — with the LSD experience: the same amplified senses, the same lost "
    "time sense, a delusion that an outside force was directing him. He then "
    "proposes that the LSD trip resembles the Bardo Thodol, and recalls that his "
    "first trip put him in Rome during the Punic Wars, speaking Latin.",
    'when I took LSD the first time I believed myself back in Rome, during the Punic Wars',
    '18 July 1967')

let('DRG-LET-1967-TRIPBOOK', 'LET_1967-08-21_RICH_BROWN_0129',
    'Letter to Rich Brown, August 21, 1967',
    'The second time (under LSD) I perceived Him', [900, 500],
    'DRG-PKT-ELDRITCH', 'self_report',
    ['LSD', 'The Three Stigmata of Palmer Eldritch', 'Reputation'],
    "Dick describes two encounters with an evil, judging deity. The first, a face "
    "in the sky with empty-slot eyes, he \"subsequently wrote ... up\" in The Three "
    "Stigmata of Palmer Eldritch, \"which is a 'trip' book\". The second came under "
    "LSD, a vengeful presence demanding an audit, which he answered with the Latin "
    "of the Requiem. A 1967 statement that ties the novel to a vision and the vision "
    "to the drug vocabulary, without quite saying the novel came from LSD.",
    'The second time (under LSD) I perceived Him as a pulsing, furious, throbbing '
    'mass of vengeance',
    '21 August 1967')

let('DRG-LET-1969-ELDRITCH', 'LET_UNDATED_BRUCE_GILLESPIE_0163',
    'Letter to Bruce Gillespie, June 8, 1969',
    'My first LSD experience, by the way, confirmed', [1500, 300],
    'DRG-PKT-ELDRITCH', 'self_report',
    ['LSD', 'The Three Stigmata of Palmer Eldritch', 'Palmer Eldritch'],
    "Answering a critic's questions, Dick says the face of Palmer Eldritch, with "
    "its slotted eyes, was something he saw objectively over the landscape — \"a "
    "true trip, before I had seen any LSD, much less taken any\" — and that he "
    "joined the Anglo-Catholic Church to protect himself from it. His first LSD "
    "experience, he adds, confirmed the vision: a hell-world it took two thousand "
    "subjective years to crawl out of.",
    'My first LSD experience, by the way, confirmed my vision of Palmer Eldritch',
    '8 June 1969',
    note="The letter carries no catalogue date; the dateline in its body reads "
         "June 8, 1969.")

let('DRG-LET-1970-MESCALIN', 'LET_1970-09-17_JAMES_0185',
    'Letter to James, September 17, 1970',
    'With acid I never had any genuine insights', [500, 600],
    'DRG-PKT-PSYCHEDELICS', 'self_report',
    ['Mescaline', 'LSD', 'Flow My Tears'],
    "Dick announces that he has finished Flow My Tears, the Policeman Said, \"a "
    "novel which truly satisfies me\", and that it is an affirmation rather than "
    "another question about what is real. It is based in part, he says, on one "
    "large dose of mescaline, which gave him what acid never had: an overpowering "
    "love for other people, which he put into the novel. The same letter mentions "
    "rereading his old novels after \"a great number of amphetamines\".",
    'With acid I never had any genuine insights, but on the mescalin I was '
    'overwhelmed by terribly powerful feelings',
    '17 September 1970')

let('DRG-LET-1970-THOUSAND', 'LET_1970-11-24_MR_AND_MRS_WHITE_0196',
    'Letter to Mr. and Mrs. White, November 24, 1970',
    'I took one thousand methamphetamine tablets in two weeks', [500, 360],
    'DRG-PKT-MARIN', 'self_report', ['Amphetamines', 'Drug culture'],
    "A long letter from the Santa Venetia house, among friends who have talked "
    "each other out of suicide. Dick offers his resilience as proof: he took a "
    "thousand methamphetamine tablets in two weeks, crashed, and forty-eight hours "
    "later was on the phone and driving to buy a new stylus. Earlier in the same "
    "letter he wonders whether his happiness is the speed, and decides it is not.",
    'I took one thousand methamphetamine tablets in two weeks, then crashed',
    '24 November 1970')

# ==========================================================================
# 2. Vancouver and X-Kalay, 1972
# ==========================================================================

let('DRG-LET-1972-XKALAY', 'LET_UNDATED_GORAN_BENGTSON_0011',
    'Letter to Göran Bengtson, April 3, 1972',
    'By and large, X-Kalay works with heroin addicts', [700, 500],
    'DRG-PKT-XKALAY', 'self_report', ['Rehabilitation', 'Heroin', 'Suicide'],
    "Written from inside X-Kalay. Dick tells a Swedish correspondent that after a "
    "collapse in Vancouver he tried to kill himself, that Suicide Prevention sent "
    "him to the X-Kalay Foundation, and that its regime — constant company, hard "
    "physical work, isolation from everything he knew — is rebuilding him. The "
    "house works mainly with heroin addicts out of Canadian prisons, and he is "
    "living among them.",
    'I owe my life to them.',
    '3 April 1972',
    note="Catalogued as undated; the dateline in the body reads April 3, 1972.")

let('DRG-LET-1972-HEROIN', 'LET_UNDATED_BRUCE_GILLESPIE_0032',
    'Letter to Bruce Gillespie, October 31, 1972',
    'X-Kalay turned out to be by-and-large a heroin rehabilitation organization',
    [500, 1300],
    'DRG-PKT-XKALAY', 'self_report', ['Rehabilitation', 'Heroin'],
    "Six months later, from Fullerton, Dick gives Gillespie the story of "
    "Vancouver: the suicide attempt, a month at X-Kalay, the attack therapy that "
    "pulled him out of depression within a week. The centre of the letter is what "
    "he saw there: heroin addicts with insect eyes who calculate what you are "
    "worth, a girl addicted at fourteen, a woman of twenty-four taken for fifty. "
    "His \"murderous hate toward drug dealers\", he says, comes from them.",
    'No reduction of the human into a mere thing, short of removing actual sections '
    'of the brain, can be found outside of the dismal transformation brought on by '
    'heroin addiction.',
    '31 October 1972',
    note="Catalogued as undated; the dateline in the body reads October 31, 1972.")

let('DRG-LET-1972-LINDA', 'LET_1972-08-30_LINDA_0019',
    'Letter to Linda, August 30, 1972',
    'the misuse of drugs, dangerous and illegal drugs', [500, 200],
    'DRG-PKT-XKALAY', 'self_report', ['LSD', 'Marijuana', 'Suicide', 'Nancy Hackett'],
    "Explaining the Vancouver suicide attempt, Dick puts it down to the depression "
    "that followed losing his wife and child — and then names drugs as a cause of "
    "that loss: marijuana, hashish and, worst, LSD had helped put his wife in a "
    "mental hospital twice. He now sees these drugs as a major cause of everything "
    "that brought him to the attempt. His own amphetamines are not on the list.",
    'I saw these drugs as a major cause of the problems that had brought me to '
    'attempt suicide.',
    '30 August 1972')

let('DRG-LET-1973-RADIO', 'LET_1973-01-06_NINA_JIM_0061',
    'Letter to Nina and Jim, January 6, 1973',
    'five friends kill themselves during or as a result of acid trips', [400, 300],
    'DRG-PKT-XKALAY', 'self_report', ['LSD', 'Rehabilitation'],
    "To friends at X-Kalay, Dick describes a live radio interview in Los Angeles "
    "where he said that X-Kalay meant more to him than science fiction, and that "
    "five friends had killed themselves during or after acid trips. The station, "
    "which was pro-drug, asked him to retract on air that good acid was fine. He "
    "refused.",
    'what I then said was that no acid was good.',
    '6 January 1973')

let('DRG-LET-1973-VERTEX', 'LET_1973-07-09_LAURA_DICK_0145',
    'Letter to Laura Dick, July 9, 1973',
    'What influence would you say that LSD has had on your writing', [300, 380],
    'DRG-PKT-PSYCHEDELICS', 'self_report', ['LSD', 'Reputation'],
    "Dick tells his daughter about the interview Vertex has just recorded. The "
    "interviewer's first question was what influence LSD had had on his writing; "
    "Dick answered \"none at all\", and the interviewer said plaintively that the "
    "whole first half of his piece was supposed to be about it. Dick tells it as a "
    "joke at the magazine's expense.",
    'and my answer was, “none at all.”',
    '9 July 1973')

let('DRG-LET-1973-NANCY', 'LET_1973-05-04_GORAN_BENGTSON_0122',
    'Letter to Göran Bengtson, May 4, 1973',
    'it was taking street dope, LSD probably', [500, 260],
    'DRG-PKT-SCANNER', 'self_report',
    ['LSD', 'Nancy Hackett', 'A Scanner Darkly'],
    "Dick has just finished the last page of A Scanner Darkly, after two years in "
    "which he could not write. A letter from his ex-wife arrives the same week: "
    "Nancy writes that street drugs, LSD probably, caused all three of her long "
    "psychotic episodes. He had guessed, he says, and notes the irony given the "
    "subject of the novel.",
    'Nancy says, for the first time, that it was taking street dope, LSD probably, '
    'that caused all three of her long psychotic episodes',
    '4 May 1973')

let('DRG-LET-1973-RESEARCH', 'LET_UNDATED_BOB_NESS_0169',
    'Letter to Bob Ness, August 31, 1973',
    'It is a very anti-dope book', [400, 400],
    'DRG-PKT-SCANNER', 'self_report', ['A Scanner Darkly', 'Substance D', 'Drug culture'],
    "To the Vancouver radio interviewer who had covered X-Kalay, Dick describes "
    "the novel he has finished: very anti-drug, about Substance D, which the heads "
    "call Slow Death because it burns out the brain until you cannot mop floors. "
    "He presents his years in the drug subculture, with a straight face that "
    "keeps slipping, as research for it — \"(ask me how well I mop floors)\".",
    'I even had to (ugh) partake of dope to get the true sense of it',
    '31 August 1973',
    note="The dateline in the body reads \"August 31 (if there is one), 1973\". The "
         "research framing is a joke the letter itself undercuts; compare the "
         "Author's Note (DRG-NOTE-SCANNER-NOVEL).")

# ==========================================================================
# 3. 1974 and after: vitamins, pentothal, the novel, the legend
# ==========================================================================

let('DRG-LET-1975-SPLITBRAIN', 'LET_1975-01-29_MALCOLM_EDWARDS_0033',
    'Letter to Malcolm Edwards, January 29, 1975',
    'in which I studied the drug-damaged brain', [900, 500],
    'DRG-PKT-2374', 'self_report',
    ['Vitamins', 'A Scanner Darkly', 'Split brain', '2-3-74'],
    "Dick explains to an English editor how 1974 began. He had been reading Robert "
    "Ornstein on the right hemisphere and the orthomolecular vitamin formula said "
    "to improve neural firing; he had just drafted A Scanner Darkly, where he "
    "concluded that the burned-out members of the drug subculture suffered from "
    "some split-brain impairment. Putting these together, he set out to switch on "
    "his own right hemisphere — and in mid-March got \"abrupt, dazzling results\".",
    'in which I studied the drug-damaged brain',
    '29 January 1975')

let('DRG-LET-1975-ORNSTEIN', 'LET_1975-03-04_ROBERT_ORNSTEIN_0075',
    'Letter to Robert Ornstein, March 4, 1975',
    'I did it mainly by ortho molecular formula vitamins', [400, 300],
    'DRG-PKT-2374', 'self_report', ['Vitamins', '2-3-74', 'Split brain'],
    "Dick writes to the psychologist whose work on hemispheric specialisation he "
    "had been reading, to ask what has become of him. Ten months ago, he says, he "
    "brought on his right hemisphere, mainly with the orthomolecular vitamins and "
    "concentrated meditation, and has been a different person since. The letter "
    "is also filed in the Exegesis.",
    'for ten months I have been a different person',
    '4 March 1975')

let('DRG-LET-1975-HEADTRIP', 'LET_1975-02-27_CLAUDIA_BUSH_0063',
    'Letter to Claudia Bush, February 27, 1975',
    'the acid trip in 1964 was the head trip', [500, 300],
    'DRG-PKT-PSYCHEDELICS', 'self_report', ['LSD', '2-3-74'],
    "In the long letter on the death of his cat Pinky, Dick distinguishes what he "
    "saw in 1974 — a light that told him death had come and was real — from a "
    "drug experience. The 1974 events were not \"a mere head trip\"; the acid trip "
    "of 1964 was. It is one of the few places Dick dates his LSD use himself.",
    'I know the difference; the acid trip in 1964 was the head trip.',
    '27 February 1975',
    note="The same letter is filed in the Exegesis (SEG_EXEG_1975-02-27_Claudia_01).")

let('DRG-LET-1975-LOADED', 'LET_1975-02-27_CLAUDIA_BUSH_0063',
    'Letter to Claudia Bush, February 27, 1975',
    'this is obviously a mescaline type of experience', [700, 700],
    'DRG-PKT-2374', 'self_report', ['Mescaline', '2-3-74'],
    "Later in the same letter Dick describes a recent vision — vines swirling up "
    "the vestment of his saint statue, spring bursting out of winter — and "
    "compares it to a children's book he read long ago. He concedes it is \"a "
    "mescaline type of experience\", and that he was \"loaded\", then turns the "
    "concession: the author of the children's book had no mescaline, and the "
    "reproach that he saw it because he wanted to proves nothing.",
    'Now, this is obviously a mescaline type of experience. We know that. And I '
    'was loaded.',
    '27 February 1975',
    note="\"Loaded\" is ambiguous: the letter does not say on what. The Exegesis "
         "copy is SEG_EXEG_1975-02-27_Claudia_03.")

let('DRG-LET-1975-FAULTY', 'LET_1975-07-07_DAVID_HARTWELL_0112',
    'Letter to David Hartwell, July 7, 1975',
    'the education which I got at X-Kalay', [600, 600],
    'DRG-PKT-XKALAY', 'self_report', ['Rehabilitation'],
    "Left alone for a week while his wife and son were away, Dick found himself "
    "back in the conditions of Marin County after Nancy left — no money, no car, "
    "no friends — and this time liked it. He now thinks X-Kalay's education was "
    "faulty: it taught him that the individual alone is doomed, and left him "
    "dependent on others to survive. The lessons \"burst into fragments\".",
    'the education which I got at X-Kalay (the heroin rehab place in Vancouver) '
    'was faulty',
    '7 July 1975')

let('DRG-LET-1975-ROLLCALL', 'LET_1975-09-08_MARCEL_THAON_0140',
    'Letter to Marcel Thaon, September 8, 1975',
    'it deals with people dying from street drugs', [500, 260],
    'DRG-PKT-SCANNER', 'self_report', ['A Scanner Darkly'],
    "To a French translator, Dick calls A Scanner Darkly the best novel he has "
    "written and compares it to All Quiet on the Western Front: people dying from "
    "street drugs in a kind of war, where the protagonist at last falls alone and "
    "unnoticed. The dedication, he says, is a roll call of his dead and injured "
    "friends.",
    'The dedication to it is a rollcall of my dead and injured friends',
    '8 September 1975')

let('DRG-LET-1976-OUI', 'LET_1976-01-13_SHARON_JARVIS_0199',
    'Letter to Sharon Jarvis, January 13, 1976',
    'wrote the story while on an LSD trip, which was not true', [1600, 500],
    'DRG-PKT-ELDRITCH', 'self_report',
    ['LSD', 'Reputation', 'Faith of Our Fathers'],
    "A letter about marketing. Dick quotes Oui magazine's claim that he \"started "
    "experimenting with LSD in the early fifties\" and is an authority on "
    "pharmacology, and Paul Williams's Rolling Stone profile that \"stressed the "
    "drug angle\", as selling points for an editor. In the same breath he "
    "complains that Harlan Ellison told the world he wrote \"Faith of Our "
    "Fathers\" on an LSD trip.",
    'I not only was on drugs, but wrote the story while on an LSD trip, which was '
    'not true',
    '13 January 1976',
    note="Oui's date for his first LSD — the early fifties — is contradicted by "
         "every other source, Dick's included.")

let('DRG-LET-1976-BOGGS', 'LET_1976-09-09_DWAYNE_BOGGS_0285',
    'Letter to Dwayne Boggs, September 9, 1976',
    'I have taken amphetamines, LSD, mescaline and phenothiazines', [40, 1100],
    'DRG-PKT-AMPH', 'self_report',
    ['Amphetamines', 'LSD', 'Mescaline', 'Productivity', 'A Maze of Death'],
    "A numbered reply to a student's questionnaire, and the most compact account "
    "Dick ever gave. He has taken amphetamines, LSD, mescaline and phenothiazines; "
    "used amphetamines for about eighteen years, prescribed for depression, for "
    "energy because he was paid so little per book; took LSD only twice; no drug "
    "trip inspired anything except a passage in A Maze of Death. He takes no drugs "
    "now, and does not recommend them.",
    'I used amphetamines for about 18 years. They were prescribed for me due to '
    'depression.',
    '9 September 1976')

let('DRG-LET-1976-MAZE', 'LET_1976-09-09_DWAYNE_BOGGS_0285',
    'Letter to Dwayne Boggs, September 9, 1976',
    'No drug trip has ever inspired me', [80, 200],
    'DRG-PKT-PSYCHEDELICS', 'self_report', ['LSD', 'A Maze of Death'],
    "The fourth answer in the same questionnaire. Asked whether drugs inspired his "
    "work, Dick names one exception: a small passage in A Maze of Death based on "
    "his first LSD experience. Sutin identifies it as the frozen landscape of snow "
    "and boulders in the novel's eleventh chapter, which Dick in 1974 called his "
    "LSD vision of 1964 \"depicted with exact accuracy\".",
    'No drug trip has ever inspired me to write anything except a small passage in '
    'my novel A MAZE OF DEATH',
    '9 September 1976')

let('DRG-LET-1976-PENTATHOL', 'LET_1976-09-15_DOROTHY_HUDNER_0289',
    'Letter to Dorothy Hudner, September 15, 1976',
    'still under the influence of sodium pentathol', [700, 500],
    'DRG-PKT-2374', 'self_report',
    ['Sodium pentothal', 'Vitamins', '2-3-74'],
    "Dick explains to his mother how many factors went into what he found in "
    "1974. He had just had several teeth removed and was still under sodium "
    "pentothal; he was experimenting with the orthomolecular vitamin formula and "
    "had accidentally taken seven grams of vitamin C; and a girl came to the door "
    "wearing a gold fish necklace. The list is offered as explanation, not "
    "debunking.",
    'I was experimenting with the orthomolecular vitamin formula, and had '
    'accidentally taken 7 grams of vitamin C, much more than is indicated.',
    '15 September 1976',
    note="Dick spells it \"pentathol\" throughout; the drug is sodium pentothal "
         "(thiopental). The letter is also filed in the Exegesis.")

let('DRG-LET-1977-DOPERS', 'LET_1977-02-18_MATT_WILLIAMS_0010',
    'Letter to Matt Williams, February 18, 1977',
    'All the characters are based on real dopers I knew', [600, 400],
    'DRG-PKT-SCANNER', 'self_report',
    ['A Scanner Darkly', 'Drug culture', 'Donna'],
    "Thanking a fan for a Grateful Dead tape — his own reel-to-reel was stolen by "
    "junkies — Dick sends money for a copy of A Scanner Darkly. The book is set in "
    "Orange County, but the events are actual and happened in Marin; every "
    "character is a real doper he knew, most now dead or burned out, and Donna is "
    "as close as he could make her to a girl he loved.",
    'All the characters are based on real dopers I knew, most of whom are dead or '
    'burned out now',
    '18 February 1977')

let('DRG-LET-1977-JAYNES', 'LET_1977-03-16_JULIAN_JAYNES_0021',
    'Letter to Julian Jaynes, March 16, 1977',
    'studied up on the orthomolecular vitamin formula', [600, 500],
    'DRG-PKT-2374', 'self_report', ['Vitamins', '2-3-74', 'Split brain'],
    "To the author of The Origin of Consciousness in the Breakdown of the "
    "Bicameral Mind, Dick explains that the experience behind his two most recent "
    "novels happened at the vernal equinox of 1974, after he had studied Ornstein "
    "and Bogen and begun the orthomolecular vitamins on purpose, to bring his right "
    "hemisphere into parity with the left.",
    'which is said to improve neural firing both in terms of synchronization and '
    'rate of fire',
    '16 March 1977')

let('DRG-LET-1977-STP', 'LET_1977-03-12_MARK_HURST_0019',
    'Letter to Mark Hurst, March 12, 1977',
    'So Phil takes a hit of STP (DOM)', [700, 9100],
    'DRG-PKT-FICTION', 'self_report', ['Psychedelics', 'VALIS', 'Reputation'],
    "An outline for the novel that became VALIS, sent to his Bantam editor. A "
    "character called Phil, envious of friends who have met the entity Zebra, "
    "takes a hit of STP hoping to see it — and does. The outline then has Phil "
    "reflect that anything he saw would be put down to the drug, as Paige is "
    "called a nut and Nicholas a liar. In the published VALIS no one takes a "
    "psychedelic to meet the god.",
    'if Phil had come up with anything—in his case it would be attributed to '
    'psychedelic drugs',
    '12 March 1977',
    note="A plan for fiction, written in a letter: the \"Phil\" here is a character.")

let('DRG-LET-1977-ICE', 'LET_1977-11-10_JAMES_R_BASS_0054',
    'Letter to James R. Bass, November 10, 1977',
    'The first time I took LSD I saw the whole landscape freeze over', [700, 300],
    'DRG-PKT-PSYCHEDELICS', 'self_report', ['LSD', 'Depression'],
    "A letter of comfort to a depressed reader. Dick describes depression as an "
    "extended now in which time stops, like an LSD trip, and recalls his first "
    "trip as a frozen landscape of snow and rocks that lasted thousands of years. "
    "Hell, he has always believed, is cold.",
    'The first time I took LSD I saw the whole landscape freeze over',
    '10 November 1977')

let('DRG-LET-1979-VALIS', 'LET_1979-03-12_LAURA_DICK_0140',
    'Letter to Laura Dick, March 12, 1979',
    'It starts with the suicide of a lovely gentle intelligent cultured young woman',
    [300, 400],
    'DRG-PKT-FICTION', 'self_report', ['LSD', 'VALIS', 'Suicide'],
    "Dick describes the autobiographical novel he has just sold to Bantam, in which "
    "he is three people. It begins where A Scanner Darkly ends, around 1971, with "
    "the LSD-caused suicide of a young woman, whose pointless death throws "
    "Horselover Fat into what looks like psychosis.",
    'It starts with the suicide of a lovely gentle intelligent cultured young '
    'woman, due to LSD',
    '12 March 1979')

let('DRG-LET-1981-NOLONGER', 'LET_1981-02-14_PATRICIA_WARRICK_0059',
    'Letter to Patricia Warrick, February 14, 1981',
    'Nor was I any longer under the influence of the sodium pentathol', [700, 300],
    'DRG-PKT-2374', 'self_report', ['Sodium pentothal', '2-3-74'],
    "Dick tells the critic Patricia Warrick that when the world of the first "
    "century pushed through into his own in 1974, the causes he had listed "
    "elsewhere were absent: he held no convictions on the matter, the girl with "
    "the fish sign was gone, and he was no longer under the pentothal. The antique "
    "world came, he thinks, from a system of inner memories surfacing.",
    'Nor was I any longer under the influence of the sodium pentathol.',
    '14 February 1981')

let('DRG-LET-1981-UNCONSCIOUS', 'LET_1981-08-16_PATRICIA_WARRICK_0130',
    'Letter to Patricia Warrick, August 16, 1981',
    'what you can learn about yourself under the influence of sodium pentothal',
    [500, 300],
    'DRG-PKT-2374', 'self_report', ['Sodium pentothal', '2-3-74'],
    "Six months later, to the same correspondent, the pentothal is back in the "
    "story. The revelation of the fish sign happened while he was oblivious to his "
    "own nature, and it is amazing, he writes, what you can learn about yourself "
    "under sodium pentothal — he had been given a great deal for a wisdom-tooth "
    "extraction that day. He found he agreed with his unconscious completely.",
    'I guess I got in touch with my unconscious',
    '16 August 1981')

let('DRG-LET-1981-JUNKY', 'LET_1981-07-28_S_JENSEN_0115',
    'Letter to S. Jensen, July 28, 1981',
    'I have known a junky', [400, 500],
    'DRG-PKT-MARIN', 'self_report', ['Heroin', 'Drug culture'],
    "Listing the kinds of people he has known — a bishop, a judge — Dick says the "
    "junky was the most humane of them. The man killed himself when his girlfriend "
    "was arrested; Dick once watched him give away his most treasured possession, "
    "a leather jacket Dick had bought him while he was withdrawing.",
    'the junky was the most humane',
    '28 July 1981')

# ==========================================================================
# 4. The Exegesis
# ==========================================================================

ex('DRG-EX-1975-CAUSAL', 'SEG_EXEG_1975-11-05_SECTION_013_13', S13,
   'I believe that the sodium pentathol and sight of the girl', [700, 400],
   'DRG-PKT-2374', 'causal_theory', ['Sodium pentothal', '2-3-74', 'Anamnesis'],
   "Dick states the sceptical explanation himself — that the pentothal and the "
   "fish necklace threw a suggestible man into a hypnoidal state and he imagined "
   "everything — and asks how he then came to think in correct Greek. His answer "
   "keeps the drug as a cause: the pentothal and the girl were necessary, but "
   "what they did was release him from the contemporary world and make him "
   "remember.",
   'I believe that the sodium pentathol and sight of the girl wearing the fish '
   'necklace were necessary causal agents',
   'November 1975')

ex('DRG-EX-1975-VITAMINC', 'SEG_EXEG_1975-11-05_SECTION_013_19', S13,
   'the orthomolecular vitamins, esp. the overdose', [200, 1000],
   'DRG-PKT-2374', 'causal_theory', ['Vitamins', 'Sodium pentothal', '2-3-74'],
   "\"As to the events which preceded my experience\": the vitamins, and above all "
   "the overdose of vitamin C, were crucial in synchronising neural firing, "
   "perhaps by flushing a built-up toxin. Then the thought that sodium pentothal "
   "is the \"truth drug\" — it de-hypnotised him, and the world of the Bible came "
   "back. The entry moves from pharmacology to the claim that it is still "
   "biblical times.",
   'the overdose (7 grams a day) of C is crucial, in regards to improving and '
   'synchronizing neural firing',
   'November 1975')

ex('DRG-EX-1975-MYSTERIES', 'SEG_EXEG_1975-11-05_SECTION_013_17', S13,
   'There was some ancient equivilent, perhaps even drug induced', [300, 300],
   'DRG-PKT-SACRAMENT', 'causal_theory',
   ['Sodium pentothal', 'Mystery religions', 'Anamnesis'],
   "Dick suggests that the pentothal stood in for the trance of the ancient "
   "mysteries: an altered state known to early Christianity, perhaps itself "
   "drug-induced. What matters to him is that something outside and before the "
   "divine seizure caused his memory to return, if only for a second.",
   'There was some ancient equivilent, perhaps even drug induced.',
   'November 1975')

ex('DRG-EX-1976-ALLEGRO', 'SEG_EXEG_1976-09-15_Dorothy_05', SDOR,
   'John Allegro was partially correct', [600, 400],
   'DRG-PKT-SACRAMENT', 'causal_theory',
   ['Psychedelics', 'Sacred mushroom', 'John Allegro', 'Anamnesis'],
   "Reading the Eucharist's \"do this in remembrance of me\" as anamnesis — the "
   "early Christians finding themselves back at the time of the Saviour, as he "
   "did — Dick concludes that John Allegro, whose The Sacred Mushroom and the "
   "Cross derived Christianity from a mushroom cult, was partly right: the "
   "experience resembles psychedelics, in the good sense of doorways.",
   'This means that John Allegro was partially correct',
   'c. September 1976', basis='internal',
   note="Dated by the entry's own count, \"30 months\" after 2-3-74.")

ex('DRG-EX-1976-PAVED', 'SEG_EXEG_1976-09-15_Dorothy_05', SDOR,
   'perhaps my psychedelic experience paved the way', [500, 300],
   'DRG-PKT-SACRAMENT', 'causal_theory', ['Psychedelics', '2-3-74', 'Split brain'],
   "Later in the same entry: the unused neural circuits Bogen and Ornstein "
   "describe exist, and in him they fired. Something unknown is needed to cause "
   "the anamnesis — and his earlier psychedelic experience may have prepared the "
   "ground, as Castaneda's did. The drugs are allowed a role as preparation, not "
   "as cause.",
   'perhaps my psychedelic experience paved the way for me, a la Castaneda',
   'c. September 1976', basis='internal')

ex('DRG-EX-1977-TOXIN', 'SEG_EXEG_1976-09-15_Dorothy_47', SDOR,
   'a metabolic "toxin," mescalin-like, was secreted in my brain', [600, 300],
   'DRG-PKT-2374', 'causal_theory', ['Mescaline', 'Paranoia', '2-3-74'],
   "Reviewing 1974 in clinical terms, Dick allows that it looks psychotic, but "
   "notes that he has been free of paranoid feelings for three whole years. His "
   "model: a mescaline-like metabolic toxin secreted in his own brain destroyed "
   "the persecutory complex. The psychedelic is now endogenous — a drug his body "
   "made.",
   'a metabolic "toxin," mescalin-like, was secreted in my brain',
   'c. 1977', basis='internal',
   note="\"That's been 3 whole years\" since March 1974.")

ex('DRG-EX-1976-TRANSUB', 'SEG_EXEG_1976-09-15_Dorothy_105', SDOR,
   'it is in fact not a study of hallucination + drugs', [500, 300],
   'DRG-PKT-ELDRITCH', 'self_report',
   ['The Three Stigmata of Palmer Eldritch', 'Eucharist'],
   "Dick proposes that what the entity Zebra is doing can be inferred from The "
   "Three Stigmata of Palmer Eldritch with its values reversed — and reports that "
   "on rereading, the novel turns out not to be about hallucination and drugs at "
   "all but about transubstantiation. Chew-Z is a eucharist.",
   'it is in fact not a study of hallucination + drugs but of the miracle of '
   'transubstantiation',
   '1976–79', conf='low')

ex('DRG-EX-1977-SLAVE', 'SEG_EXEG_1976-09-15_Dorothy_76', SDOR,
   'to assume that substance D was secretly being produced by the government',
   [300, 400],
   'DRG-PKT-SCANNER', 'self_report',
   ['A Scanner Darkly', 'Substance D', 'K. W. Jeter'],
   "Talking with K. W. Jeter about A Scanner Darkly's reception, Dick notes that "
   "readers, reviewers and the publishers all assume Substance D is secretly made "
   "by the government, to turn people into slave labour and for profit. The two "
   "agree that this can properly be inferred from the book — a reading Dick says "
   "he had not consciously put there.",
   'substance D was secretly being produced by the government',
   '1977–79', basis='internal', conf='low',
   note="After the novel's reviews (1977).")

ex('DRG-EX-1977-NOTE', 'SEG_EXEG_1976-09-15_Dorothy_77', SDOR,
   'when I wrote the author\'s note to "Scanner" I meant', [700, 300],
   'DRG-PKT-SCANNER', 'self_report',
   ['A Scanner Darkly', 'Rehabilitation'],
   "Dick reads his own Author's Note against the grain. When he wrote that its "
   "people were \"punished entirely too much\" he meant the drug's effects; read at "
   "the end of the novel, it seems instead to mean the lifetime in the New-Path "
   "work camp. The rehabilitation centre — modelled on X-Kalay — becomes the "
   "punishment.",
   'it more seems to refer to the lifetime incarceration at the new path work camp',
   '1977–79', basis='internal', conf='low')

ex('DRG-EX-1977-SYNANON', 'SEG_EXEG_1976-09-15_Dorothy_91', SDOR,
   'is the exact analog of CP brainwashing', [600, 300],
   'DRG-PKT-XKALAY', 'self_report',
   ['A Scanner Darkly', 'Rehabilitation', 'Substance D'],
   "Working through A Scanner Darkly's last revelation — that the makers of "
   "Substance D want slaves, not money — Dick calls addiction and rehabilitation "
   "an establishment plot to recruit slave labour, and the Synanon game, the "
   "attack therapy he had undergone at X-Kalay, the exact equivalent of Communist "
   "brainwashing.",
   'The "Synanon game" is the exact analog of CP brainwashing',
   '1977–79', basis='internal', conf='low')

ex('DRG-EX-1978-PLAYING', 'SEG_EXEG_1976-09-15_Dorothy_179', SDOR,
   'is a study of the punishment (too great) for playing instead of toiling',
   [400, 300],
   'DRG-PKT-SCANNER', 'self_report',
   ['A Scanner Darkly', 'Flow My Tears'],
   "Dick decides that A Scanner Darkly carries on the hidden theme of Flow My "
   "Tears: it does not deplore playing, only that way of playing. It is a study "
   "of the punishment — too great — for playing instead of toiling. \"Not "
   "drugs.\" He is amazed that he wrote it before he had worked out Tears.",
   'is a study of the punishment (too great) for playing instead of toiling, not drugs',
   'c. 1978', basis='internal',
   note="\"After 4 years of exegesis re 'Tears'\": the Tears exegesis begins in 1974.")

ex('DRG-EX-1978-THREESTATES', 'SEG_EXEG_1978-10-10_SECTION_016_35', S16,
   'In LSD states you experience (1) apart from (2)', [800, 300],
   'DRG-PKT-SACRAMENT', 'causal_theory', ['LSD', 'Psychedelics', '2-3-74'],
   "A model of three kinds of time: (1) inner time, (2) the outer world's time, "
   "(3) eternity. LSD separates (1) from (2), Dick argues, but never reaches (3); "
   "perhaps some psychedelic such as Amanita muscaria could. He himself reached "
   "(3) only in 2-3-74. The drug experience is placed one rung below the "
   "revelation.",
   'But never did I get to (3) except in 2-3-74.',
   '1978–80', conf='low')

ex('DRG-EX-1978-NOTLSD', 'SEG_EXEG_1978-10-10_SECTION_016_287', S16,
   'I was intoxicated, not by LSD', [500, 500],
   'DRG-PKT-SACRAMENT', 'causal_theory', ['LSD', 'Dionysos', 'Mystery religions', '2-3-74'],
   "After citing Hofmann's theory that LSD was used in the Greater Mysteries and "
   "Allegro's mushroom theory of early Christianity, Dick says that in 1974 he "
   "was indeed intoxicated — not by LSD, and not by a flashback, but by Valis. "
   "Then the reversal: ecstasy is sanity, sobriety is madness, and the secret was "
   "stolen for us by Dionysos. Behind Flow My Tears, he adds, lies the Bacchae.",
   "I was intoxicated, not by LSD - it wasn't a flash-back",
   '1978–80', conf='low')

ex('DRG-EX-1978-MUSHROOM', 'SEG_EXEG_1978-10-10_SECTION_016_190', S16,
   'John allegro was getting close to the truth', [400, 500],
   'DRG-PKT-SACRAMENT', 'causal_theory',
   ['Sacred mushroom', 'Psychedelics', 'John Allegro', '2-3-74'],
   "The two things he is \"not supposed to tell\": the female nature of Christ, "
   "and that he is one of the early apostolic Christians. Allegro's The Sacred "
   "Mushroom and the Cross was close to the truth; Christianity is a shamanic "
   "religion in which another order of reality is experienced, and he crossed "
   "into it \"as I had taken a pscyhedelic\".",
   'I did pass over into "the other" world, all right, asd I had taken a '
   'pscyhedelic: (mushroom).',
   '1978–80', conf='low',
   note="\"As\" may mean \"as if\" or \"because\"; the sentence does not settle "
        "whether he is claiming to have taken a mushroom. Spelling as in the "
        "manuscript.")

ex('DRG-EX-1978-INGREDIENTS', 'SEG_EXEG_1978-10-10_SECTION_016_313', S16,
   'the other ingredient is: the sacred mushroom', [700, 400],
   'DRG-PKT-SACRAMENT', 'causal_theory',
   ['Sacred mushroom', 'Plasmate', 'Eucharist', '2-3-74'],
   "The plasmate is Christ's blood: alive, information, drunk at the agape "
   "feasts. But it needs a second ingredient, the sacred mushroom, as a catalyst. "
   "Then, plainly: the drugs he took reacted with the plasmate in him, and it came "
   "alive. Here, unlike elsewhere, his own drug use is part of the mechanism.",
   'Well, the drugs I took reacted to the plasmate in me.',
   '1978–80', conf='low')

ex('DRG-EX-1979-SPEEDSELF', 'SEG_EXEG_1978-10-10_SECTION_016_356', S16,
   'I must have gone mad (to be precise about it)', [500, 400],
   'DRG-PKT-AMPH', 'self_report', ['Amphetamines', 'Psychosis', 'Flow My Tears'],
   "Dick inverts the usual story of 1974: he was not driven mad then but sobered "
   "up. He dates his madness to the 1950s or 1960s, \"perhaps due to the speed\", "
   "then to Nancy's psychosis around 1969; he was psychotic when he wrote Flow My "
   "Tears in 1970, and in 1971 and 1973; in early 1974 his psychotic "
   "\"speed\"-self collapsed and a sane self took over.",
   'I must have gone mad (to be precise about it) sometime back in the 50s or 60s, '
   'perhaps due to the speed',
   '1979–80', basis='internal',
   note="The entry refers to the Platt interview, which took place on 17 May 1979.")

ex('DRG-EX-1978-FASTER', 'SEG_EXEG_1978-10-10_SECTION_016_168', S16,
   'I had been moving faster + faster for decades due to the amphetamines',
   [300, 300],
   'DRG-PKT-AMPH', 'causal_theory', ['Amphetamines', '2-3-74'],
   "In a theory of 2-3-74 as a timing failure, the amphetamines supply the "
   "mechanism: decades on them had speeded him up; without them his body made up "
   "the missing noradrenaline and he went faster still, until only timeless "
   "constants were visible. The withdrawal, not the drug, sets the stage.",
   'I had been moving faster + faster for decades due to the amphetamines.',
   '1978–80', conf='low')

ex('DRG-EX-1978-DRIVENMAD', 'SEG_EXEG_1978-10-10_SECTION_016_174', S16,
   'Driven mad by 1) Nancy leaving', [1000, 200],
   'DRG-PKT-AMPH', 'self_report',
   ['Amphetamines', 'Mescaline', 'Psychosis', 'Nancy Hackett'],
   "Dick describes a fugal personality that \"took over in 1970 when I took the "
   "mescalin\", always high, intoxicated by amphetamines and cycling up and down "
   "with no relation to reality. Then he gives three causes for his madness, in "
   "order: Nancy leaving, drugs, endogenous psychosis. The drugs are one cause "
   "among three.",
   'Driven mad by 1) Nancy leaving; + 2) drugs; + 3) endogenous psychosis.',
   '1978–80', conf='low')

ex('DRG-EX-1978-NOLONGER', 'SEG_EXEG_1978-10-10_SECTION_016_195', S16,
   "I'm no longer abusing drugs, legal or illegal", [600, 300],
   'DRG-PKT-XKALAY', 'self_report', ['Sobriety'],
   "A stocktaking in the middle of the Exegesis: he has written his best book, "
   "his mind is alive, his daughters have visited, he is economically secure, he "
   "has been to France — and he is no longer abusing drugs, legal or illegal. \"I "
   "am very happy.\" The next sentence wonders whether he has been dead since "
   "1974.",
   "I'm no longer abusing drugs, legal or illegal - i.e. drug-dependent.",
   '1978–80', conf='low')

ex('DRG-EX-1978-JETER', 'SEG_EXEG_1978-10-10_SECTION_016_08', S16,
   'Jeter says, "the fucked-up dopers', [1400, 300],
   'DRG-PKT-SACRAMENT', 'self_report',
   ['A Scanner Darkly', 'Substance D', 'K. W. Jeter', 'Dionysos', 'Hal'],
   "A dream of a cereal box printed like medicine directions convinces Dick that "
   "A Scanner Darkly holds the key: we are toxic, and the entity Zebra is a doctor "
   "chasing the poison — perhaps flushed out by his vitamins. Substance "
   "D's effects resemble tertiary syphilis; it was Hal Barris who showed the "
   "impaired brilliance the novel depicts. Then K. W. Jeter's remark, and Dick's "
   "turn to Dionysos, the mad god: are the sane really the insane?",
   'the fucked-up dopers -on Substance D- were the only ones who correctly '
   'understood the reality situation',
   '1978–80', conf='low')

ex('DRG-EX-1978-IMPAIRMENT', 'SEG_EXEG_1978-10-10_SECTION_016_109', S16,
   'no epistemological insight in my writing outweighs the study of brain impairment',
   [400, 400],
   'DRG-PKT-SCANNER', 'self_report',
   ['A Scanner Darkly', 'Substance D', 'Split brain'],
   "If Christ is a physician using an advanced medical technology, Dick reasons, "
   "then nothing in his writing about knowledge and illusion outweighs A Scanner "
   "Darkly's study of brain damage from Substance D — which was based, he adds, "
   "on observation and experience of real impairment. The novel's double self "
   "is secondary to the damage.",
   'no epistemological insight in my writing outweighs the study of brain impairment',
   '1978–80', conf='low')

ex('DRG-EX-1978-OCCLUSION', 'SEG_EXEG_1978-10-10_SECTION_016_09', S16,
   'In SCANNER the cause of our being unable to reality-test', [300, 400],
   'DRG-PKT-FICTION', 'self_report',
   ['A Scanner Darkly', 'The Three Stigmata of Palmer Eldritch', 'A Maze of Death',
    'Substance D', 'Can-D and Chew-Z'],
   "Dick lays his novels side by side as one account. Tears shows the actual "
   "world, Rome around AD 45; Scanner shows why we cannot test reality — a "
   "damage to perception deliberately induced by a drug; and that matches the "
   "magician of Palmer Eldritch who drugs people into a world where no time "
   "passes. The fictional drugs become a diagnosis.",
   'an inner occlusion deliberately induced by a drug or drug-like substance',
   '1978–80', conf='low')

ex('DRG-EX-1978-HAL', 'SEG_EXEG_1978-10-10_SECTION_016_134', S16,
   "Hal was convinced that if sodium pentathol was given to me I'd remember",
   [300, 900],
   'DRG-PKT-2374', 'causal_theory', ['Sodium pentothal', 'Lithium', 'Vitamins', 'Hal'],
   "In the political version of 2-3-74, Hal Barris had predicted that under "
   "sodium pentothal Dick would remember a dissociated self — and he did: "
   "\"Thomas\". The pentothal was unexpected and let him wake up. A few lines "
   "on, the occluding force is thrown off \"partly to the lithium + The "
   "vitamins, + of course the penta thil\".",
   "Hal was convinced that if sodium pentathol was given to me I'd remember",
   '1978–80', conf='low')

ex('DRG-EX-1978-FLUSHING', 'SEG_EXEG_1978-10-10_SECTION_016_108', S16,
   'Flushing (done by me with lithium', [1300, 300],
   'DRG-PKT-2374', 'causal_theory', ['Lithium', 'Vitamins', 'Sodium pentothal', '2-3-74'],
   "A numbered list of the conditions that set off his waking in 1974: sensory "
   "deprivation, intense fear, physical pain, a disinhibiting stimulus, the "
   "sodium pentothal, recognition of memories, closeness to death — and the "
   "flushing of his neural tissue with lithium and water-soluble vitamins in huge "
   "doses. Chemistry is two items in a list of nine.",
   'Flushing (done by me with lithium + ws vitaming in huge doses) of neural tissue.',
   '1978–80', conf='low')

# ==========================================================================
# 5. Interviews
# ==========================================================================

doc('DRG-INT-1974-ACID', 'interview', LASTINT,
    '“The Acid Truth”, interview by Arthur Byron Cover, Vertex, February 1974 '
    '(in The Last Interview and Other Conversations)',
    'All I ever found out about acid was that I was where I wanted to get out of fast',
    [1100, 200],
    'DRG-PKT-PSYCHEDELICS', 'self_report',
    ['LSD', 'Reputation', 'Faith of Our Fathers'],
    "Asked whether \"Faith of Our Fathers\" was written on acid, Dick says you "
    "cannot write on acid — the one page he managed was in Latin. How much did he "
    "take? \"Not that much.\" He is amazed by the blurbs he wrote for himself "
    "about experimenting with hallucinogens to find the reality beneath delusion.",
    'All I ever found out about acid was that I was where I wanted to get out of '
    'fast.',
    'Interview 1973; published February 1974', basis='publication')

doc('DRG-INT-1974-BEFORE', 'interview', MAGINT,
    'Interview by Arthur Byron Cover, Vertex, February 1974 (in PKD Magazine '
    'Interviews)',
    'I wrote that before I had ever seen LSD', [500, 900],
    'DRG-PKT-ELDRITCH', 'self_report',
    ['LSD', 'The Three Stigmata of Palmer Eldritch', 'Can-D and Chew-Z'],
    "The fuller text of the Vertex interview. Dick knows of no effect LSD had on "
    "his work: Palmer Eldritch, \"a tremendous bad acid trip, so to speak\", was "
    "written before he had seen LSD, from a description of its discovery. Its "
    "drugs produced flashbacks before anyone knew LSD would — \"an accidental "
    "prophecy\".",
    'I wrote that before I had ever seen LSD.',
    'Interview 1973; published February 1974', basis='publication')

doc('DRG-INT-1974-CONTROL', 'interview', MAGINT,
    'Philip Purser, “Even Sheep Can Upset Scientific Detachment”, Daily Telegraph '
    'Magazine, July 19, 1974 (in PKD Magazine Interviews)',
    'experimented with LSD but always under control', [900, 500],
    'DRG-PKT-ELDRITCH', 'self_report', ['LSD', 'Palmer Eldritch', 'A Scanner Darkly'],
    "To an English journalist, Dick describes the vision of an evil, slot-eyed "
    "deity in the sky — the face he elsewhere calls Palmer Eldritch — seen from a "
    "rented shack in empty pastures where isolation worked like sensory "
    "deprivation: \"I wasn't on LSD or any other drug, not at the time\". Here he "
    "says its scanning gave him the title A Scanner Darkly. An evil form-destroyer "
    "strikes people alone, which is why LSD is so deadly. Purser adds that Dick "
    "had had \"a bad time from drugs\" and now does rehabilitation work.",
    'I’ve experimented with LSD but always under control.',
    '19 July 1974', basis='publication')

doc('DRG-INT-1978-AQUARIAN', 'interview', MAGINT,
    'Interview by Joe Vitale, The Aquarian, October 11–18, 1978 (in PKD Magazine '
    'Interviews)',
    'Drugs cause the mind to feed on itself', [500, 700],
    'DRG-PKT-PSYCHEDELICS', 'self_report',
    ['Psychedelics', 'LSD', 'The Three Stigmata of Palmer Eldritch', 'Reputation'],
    "Asked whether drugs helped him see past illusion, Dick says absolutely not: "
    "drugs eat your head. He once thought enough psychedelics might show ultimate "
    "reality; now he thinks they show the patterns on the rug turning hideous, "
    "and lead to the rubber room. His drug experiences have not appeared in his "
    "work; Palmer Eldritch came from a Huxley article.",
    'There was a time in my life when I thought drugs could be useful',
    'October 1978', basis='publication')

doc('DRG-INT-1979-AMPH', 'interview', LASTINT,
    '“Killing the Rat”, interview by Charles Platt, May 17, 1979 (in The Last '
    'Interview and Other Conversations)',
    'The only drugs I took regularly were amphetamines', [100, 400],
    'DRG-PKT-AMPH', 'self_report', ['Amphetamines', 'Productivity', 'Prescription'],
    "Charles Platt asks how far he was into drugs. The only drugs he took "
    "regularly, Dick says, were amphetamines, because he was paid so little per "
    "book: sixteen novels in five years, sixty finished pages a day. They were "
    "prescribed. He stopped, and does not write as much any more.",
    'the only way I could write that much was to take amphetamines, which were '
    'prescribed for me',
    '17 May 1979', basis='record')

doc('DRG-INT-1979-TWICE', 'interview', LASTINT,
    '“Killing the Rat”, interview by Charles Platt, May 17, 1979 (in The Last '
    'Interview and Other Conversations)',
    'I used to talk like I was really into acid', [60, 1500],
    'DRG-PKT-PSYCHEDELICS', 'self_report',
    ['LSD', 'The Three Stigmata of Palmer Eldritch', 'Reputation'],
    "The fullest account of his LSD use. He took it twice; the second dose may not "
    "have been acid at all. The first was Sandoz acid from the university, split "
    "with a friend, and he \"went straight to hell\". A month later the galleys of "
    "Palmer Eldritch arrived and he could not read them. \"That was in 1964.\" He "
    "begged people not to take it.",
    'the fact of the matter is that I took it two times',
    '17 May 1979', basis='record')

doc('DRG-INT-1979-HUXLEY', 'interview', LASTINT,
    '“Killing the Rat”, interview by Charles Platt, May 17, 1979 (in The Last '
    'Interview and Other Conversations)',
    'all I had had to go on when I wrote it was an article by Aldous Huxley',
    [400, 300],
    'DRG-PKT-ELDRITCH', 'self_report',
    ['LSD', 'The Three Stigmata of Palmer Eldritch'],
    "In the same answer: Palmer Eldritch is \"my classic 'LSD novel'\", written "
    "with nothing to go on but an Aldous Huxley article — and then everything "
    "horrible he had written seemed to come true under acid. The novel came "
    "first; the drug confirmed it.",
    'even though all I had had to go on when I wrote it was an article by Aldous '
    'Huxley',
    '17 May 1979', basis='record')

doc('DRG-INT-1981-RECORD', 'interview', RICKMAN,
    'Interview by Gregg Rickman, September 30, 1981, in Philip K. Dick: In His Own '
    'Words (1984)',
    'I wrote that to record them', [700, 400],
    'DRG-PKT-SCANNER', 'self_report', ['A Scanner Darkly', 'Drug culture'],
    "Rickman asks about A Scanner Darkly, his first book to draw on the early "
    "1970s. Dick dates his time in the drug subculture: after Nancy left in 1970, "
    "through 1971, and the first month of 1972. He began writing about those "
    "people a week after he left, to record them before they faded — and as an "
    "attack on drugs.",
    'And also as an attack on drugs because I had seen it kill so many people',
    '30 September 1981', basis='stamp')

doc('DRG-INT-1982-FLUSH', 'interview', LASTINT,
    '“Destruction and Enlightenment”, interview by Gregg Rickman, April '
    '1981–February 1982 (in The Last Interview and Other Conversations)',
    'score some marijuana and flush two hundred dollars', [300, 500],
    'DRG-PKT-XKALAY', 'self_report', ['Marijuana', 'Sobriety'],
    "Talking about moderation in the last months of his life, Dick describes a "
    "habit his neighbour calls cognitive dissonance: he buys drugs and destroys "
    "them, scores marijuana and flushes two hundred dollars of it, because he "
    "enjoys scoring but does not want to. There are two ways not to be alive, he "
    "says — all the dope in the world, or all the hair shirts.",
    'Because I enjoy the feel of scoring but I don’t want to score.',
    '1981–82', basis='record')

# ==========================================================================
# 6. The fiction, and Dick's own Author's Note
# ==========================================================================

doc('DRG-NOTE-SCANNER-DECISION', 'paratext', FIVE,
    "A Scanner Darkly (1977), Author's Note",
    'Drug misuse is not a disease, it is a decision', [900, 600],
    'DRG-PKT-SCANNER', 'self_report', ['A Scanner Darkly', 'Drug culture'],
    "The note that ends the novel, in Dick's own voice. It is about people who were "
    "punished entirely too much for wanting a good time, like children playing in "
    "the street; the man Jerry Fabin is based on killed himself while it was being "
    "written. Drug misuse, he says, is a decision, and when many people make it, a "
    "life-style — only a speeding-up of ordinary life. There is no moral; there is "
    "Nemesis.",
    'Drug misuse is not a disease, it is a decision, like the decision to step out '
    'in front of a moving car.',
    '1977', basis='publication')

doc('DRG-NOTE-SCANNER-NOVEL', 'paratext', FIVE,
    "A Scanner Darkly (1977), Author's Note",
    'I myself, I am not a character in this novel; I am the novel.', [500, 500],
    'DRG-PKT-SCANNER', 'self_report', ['A Scanner Darkly'],
    "The note continues: for a while Dick was himself one of the children playing "
    "in the street, and was punished; he is on the list of the dedicated, with "
    "what became of each. He is not a character, he says, but the novel — and so "
    "was the whole nation at that time.",
    'I myself, I am not a character in this novel; I am the novel.',
    '1977', basis='publication')

doc('DRG-FIC-SCANNER-BUGS', 'fiction', FIVE, C_SCANNER,
    'Once a guy stood all day shaking bugs from his hair', [10, 900],
    'DRG-PKT-SCANNER', 'symptom_description', ['A Scanner Darkly', 'Substance D'],
    "The novel's first sentence. Jerry Fabin, a burned-out user, spends eight "
    "hours in the shower trying to wash away aphids no one else can see, and works "
    "out their life cycle from the Britannica. Dick's Author's Note says the man "
    "Fabin is based on killed himself; Anne R. Dick's informants describe a "
    "housemate who did the same.",
    'Once a guy stood all day shaking bugs from his hair.',
    '1977', basis='publication')

doc('DRG-FIC-SCANNER-SLOWDEATH', 'fiction', FIVE, C_SCANNER,
    'is for Substance D. Which is for Dumbness and Despair and Desertion',
    [600, 400],
    'DRG-PKT-SCANNER', 'allegory', ['A Scanner Darkly', 'Substance D', 'Bob Arctor'],
    "Fred, the undercover agent in his scramble suit, gives a canned anti-drug "
    "talk to a Lions Club and goes off script. D is for dumbness, despair and "
    "desertion — and finally for death: Slow Death, \"we, the dopers\", call it. "
    "He has given himself away; his superior tells him he blew it.",
    'is finally Death. Slow Death',
    '1977', basis='publication')

doc('DRG-FIC-SCANNER-HEMISPHERES', 'fiction', FIVE, C_SCANNER,
    'The two hemispheres of my brain are competing?', [900, 400],
    'DRG-PKT-SCANNER', 'symptom_description', ['A Scanner Darkly', 'Substance D', 'Split brain'],
    "The police psychologists give Fred his results: not simple impairment but "
    "competition between the hemispheres, two signals carrying conflicting "
    "information, because Substance D has damaged the dominant left side. The "
    "novel's split between Fred and Arctor is given a neurology — the same "
    "split-brain research Dick was reading in 1973–74.",
    'Substance D. It often causes that, functionally.',
    '1977', basis='publication')

doc('DRG-FIC-SCANNER-FIELD', 'fiction', FIVE, C_SCANNER,
    'I saw Substance D growing', [900, 600],
    'DRG-PKT-SCANNER', 'allegory', ['A Scanner Darkly', 'Substance D', 'Rehabilitation'],
    "The ending. Bruce, all that is left of Fred and Arctor, works on a New-Path "
    "farm and kneels before a field of small blue flowers hidden among corn: Mors "
    "ontologica, the source of Substance D, grown by the rehabilitation centre "
    "itself. He hides one in his shoe as a present for his friends.",
    'I saw death rising from the earth, from the ground itself, in one blue field, '
    'in stubbled color.',
    '1977', basis='publication')

doc('DRG-FIC-NOWWAIT-ADDICT', 'fiction', NOWWAIT, 'Now Wait for Last Year (1966)',
    'It is addictive. From even one exposure', [600, 1800],
    'DRG-PKT-FICTION', 'allegory', ['JJ-180', 'Now Wait for Last Year', 'Kathy Sweetscent'],
    "Kathy Sweetscent has tried JJ-180 once at a party in Tijuana. Next morning an "
    "agent of Earth's allies, the 'Starmen, tells her she is addicted after a single "
    "dose, that no clinic can cure it, and that they will supply her if she spies "
    "for them. She has taken dozens of drugs and never this. The drug is a weapon "
    "of a war.",
    "Of course it's addictive, Kathy; that's why we put you on it.",
    '1966', basis='publication')

doc('DRG-FIC-NOWWAIT-HASTINGS', 'fiction', NOWWAIT, 'Now Wait for Last Year (1966)',
    'had a reputation for essaying an experience with every hallucinogenic drug',
    [600, 400],
    'DRG-PKT-FICTION', 'allegory', ['JJ-180', 'Now Wait for Last Year', 'Psychedelics'],
    "At the Tijuana party where JJ-180 is passed round, the guests include Marm "
    "Hastings, a wealthy author on oriental mysticism who tries every new "
    "hallucinogen and is examining his host's library on drugs and religion. He "
    "will ask, sharply, whether the drug is really German. Dick's satire of the "
    "religious drug-seeker, written around 1963–64.",
    'To Hastings this was allied with religion.',
    '1966', basis='publication')

doc('DRG-FIC-VALIS-UPPERS', 'fiction', VALIS3, 'VALIS (1981)',
    'He never did sleeping pills. He did uppers.', [700, 300],
    'DRG-PKT-FICTION', 'allegory',
    ['VALIS', 'Amphetamines', 'Horselover Fat', 'Gloria Knudson'],
    "VALIS opens with a phone call: Gloria asks Horselover Fat for Nembutals so she "
    "can kill herself. His psychiatrist had told him to get off dope, which he "
    "hadn't done. He has no sleeping pills; he does uppers. He lies that he has ten, "
    "to keep her on the line. The narrator, who is also Fat, is telling the story "
    "of 1971.",
    'He never did sleeping pills. He did uppers.',
    '1981', basis='publication')

doc('DRG-FIC-VALIS-PLAGUE', 'fiction', VALIS3, 'VALIS (1981)',
    'It was like a plague. No one could discern how much was due to drugs.',
    [900, 400],
    'DRG-PKT-FICTION', 'allegory',
    ['VALIS', 'LSD', 'Drug culture', 'Timothy Leary', 'Horselover Fat'],
    "After Gloria's suicide, Fat cries, watches TV and takes more dope; his own "
    "brain is going. Earlier the narrator has thanked Tim Leary for his promotion "
    "of expanded consciousness, and blamed Gloria's acid for wrecking her mind. "
    "Now the verdict on the whole Bay Area of the 1960s: it was like a plague, and "
    "no one could tell how much was drugs.",
    'It was like a plague. No one could discern how much was due to drugs.',
    '1981', basis='publication')

# ==========================================================================
# 7. Biography and criticism
# ==========================================================================

doc('DRG-BIO-SUTIN-BERKELEY', 'biography', SUTIN, C_SUTIN,
    'The extent to which Phil used amphetamines while in Berkeley', [300, 500],
    'DRG-PKT-BIOGRAPHERS', 'critique',
    ['Amphetamines', 'Prescription', 'Lawrence Sutin', 'Kleo Apostolides'],
    "Sutin on the 1950s. Doctors routinely prescribed amphetamine analogues such as "
    "Semoxydrine for anxiety and depression, and how much Dick used in Berkeley is "
    "\"just isn't clear\". A friend, Iskandar Guy, recalls regular low doses and "
    "a sophisticated knowledge of pharmacy; Dick's wife Kleo insists he took "
    "nothing but one sample from her father, a muscle relaxant and aspirin.",
    'But Kleo insists that, other than the Semoxydrine sample from her father, '
    'Phil took no drugs but Serpasil',
    '1989', basis='publication')

doc('DRG-BIO-SUTIN-FUEL', 'biography', SUTIN, C_SUTIN,
    'By now it was a steady fuel for the writing', [500, 200],
    'DRG-PKT-BIOGRAPHERS', 'critique',
    ['Amphetamines', 'Productivity', 'Lawrence Sutin'],
    "Sutin on the Point Reyes marriage, around 1960: Dick is hospitalised with "
    "chest pain diagnosed as pyloric spasm and told to cut down on coffee. Sutin "
    "asks whether the Semoxydrine came up, and answers that by then it was a "
    "steady fuel for the writing.",
    'By now it was a steady fuel for the writing.',
    '1989', basis='publication')

doc('DRG-BIO-SUTIN-ACID', 'biography', SUTIN, C_SUTIN,
    'Newkom says that he gave Phil his first hit of acid sometime in 1964',
    [100, 600],
    'DRG-PKT-PSYCHEDELICS', 'critique',
    ['LSD', 'A Maze of Death', 'Lawrence Sutin', 'Ray Nelson'],
    "Sutin dates Dick's first LSD to 1964, from Jack Newkom, and counts \"at least "
    "two occasions\" that year, one with Ray Nelson, who watched him relive a Roman "
    "gladiator's death in Latin. Phil never much liked it. Sutin quotes the July "
    "1974 letter in which Dick says A Maze of Death depicts his 1964 LSD vision "
    "\"with exact accuracy\".",
    'He took it only a very few times, despite wild rumors that he often wrote on '
    'acid-rumors Phil resented but himself helped get started.',
    '1989', basis='publication')

doc('DRG-BIO-SUTIN-1963', 'biography', SUTIN, C_SUTIN,
    'What drugs these were is unknown', [600, 400],
    'DRG-PKT-ELDRITCH', 'causal_theory',
    ['Amphetamines', 'Palmer Eldritch', 'Lawrence Sutin'],
    "On the 1963 vision of the face in the sky. Sutin notes that Dick at the time "
    "described taking \"certain chemicals\" and \"psychedelic drugs\", that a 1967 "
    "letter rules out LSD, and that by the 1970s his accounts dropped the drugs "
    "altogether. His own view: amphetamines alone could do it — though anguish, "
    "not chemistry, was at the vision's heart.",
    'amphetamines alone, in sufficiently high doses, could account for such a vision',
    '1989', basis='publication')

doc('DRG-BIO-SUTIN-PILLS', 'biography', SUTIN, C_SUTIN,
    'Acid, pot, and hash held no special fascination. But pills', [400, 700],
    'DRG-PKT-MARIN', 'critique',
    ['Amphetamines', 'Self-medication', 'Lawrence Sutin', 'Nancy Hackett'],
    "Sutin on the marriage to Nancy Hackett, 1966–70. Drugs carried glamour in the "
    "sixties, and Timothy Leary made a fan call in 1969, but Dick's passion was "
    "pills: Stelazine, relaxants, Librium, Valium, Dexamyl and white crosses, "
    "prescription quality preferred. Nancy: \"like he was medicating himself\". "
    "His supply came from doctors to whom he recited the symptoms.",
    'Acid, pot, and hash held no special fascination. But pills … ah, pills.',
    '1989', basis='publication')

doc('DRG-BIO-SUTIN-ELLISON', 'biography', SUTIN, C_SUTIN,
    'Ellison recalls that Phil assured him that both', [700, 600],
    'DRG-PKT-ELDRITCH', 'critique',
    ['LSD', 'Reputation', 'Faith of Our Fathers', 'The Three Stigmata of Palmer Eldritch',
     'Lawrence Sutin'],
    "Sutin weighs the Dangerous Visions dispute. Ellison's 1967 introduction said "
    "\"Faith of Our Fathers\" and Palmer Eldritch came from hallucinogenic journeys; "
    "Ellison recalls that Dick assured him so, and Dick made no changes to the "
    "galleys. From 1975 the anthology carried Dick's rebuttal. Sutin believes the "
    "denial.",
    'It seems likely that Phil’s 1975 denial is truthful and that the 1967 version '
    'sounded fun at the time.',
    '1989', basis='publication')

doc('DRG-BIO-SUTIN-STANFORD', 'biography', SUTIN, C_SUTIN,
    'said he was taking one thousand Methedrine tabs per week', [1400, 400],
    'DRG-PKT-MARIN', 'critique',
    ['Amphetamines', 'Prescription', 'Lawrence Sutin', 'Kleo Apostolides'],
    "From notes kept by Dick's stepfather in spring 1971: Phil phones to say he is a "
    "drug addict, \"on Benzedrine and other drugs since 1951, when Kleo's physician "
    "father gave him a prescription\". A girlfriend takes him to the psychiatric "
    "ward at Stanford, where the examining psychiatrist records a thousand "
    "Methedrine tablets a week at $300 a month, with Stelazine — and finds an "
    "\"astute\" intellect and no physical addiction.",
    'Phil said he was taking one thousand Methedrine tabs per week',
    '1989', basis='publication')

doc('DRG-BIO-SUTIN-PARANOIA', 'biography', SUTIN, C_SUTIN,
    'bouts of intense paranoia are a known common side effect of amphetamine abuse',
    [800, 500],
    'DRG-PKT-MARIN', 'critique',
    ['Amphetamines', 'Paranoia', 'Drug culture', 'Lawrence Sutin'],
    "Santa Venetia, 1970–71: armed, unstable casualties of the drug scene in the "
    "house daily, a reasonable fear of rip-offs and busts — and jars of a thousand "
    "white crosses in the refrigerator next to protein milkshakes. Sutin will not "
    "choose between the real dangers and the drug: both are true.",
    'bouts of intense paranoia are a known common side effect of amphetamine abuse',
    '1989', basis='publication')

doc('DRG-BIO-SUTIN-THREEWEEKS', 'biography', SUTIN, C_SUTIN,
    'X-Kalay stay lasted only three weeks', [400, 600],
    'DRG-PKT-XKALAY', 'critique',
    ['Rehabilitation', 'Heroin', 'Lawrence Sutin'],
    "Sutin on X-Kalay: residents remembered as aged by decades, attack therapy that "
    "probed Dick's attraction to dark-haired girls — and a stay of only three "
    "weeks, after which its demands grated. Dick had told Vertex he pretended to be "
    "a heroin addict to get in; heroin, Sutin says, was one drug Dick never "
    "touched.",
    'X-Kalay stay lasted only three weeks',
    '1989', basis='publication')

doc('DRG-BIO-SUTIN-NEVERAGAIN', 'biography', SUTIN, C_SUTIN,
    'Never again did Phil take speed on a regular basis', [600, 200],
    'DRG-PKT-BIOGRAPHERS', 'critique',
    ['Amphetamines', 'Rehabilitation', 'Sobriety', 'Lawrence Sutin'],
    "Sutin's verdict on X-Kalay, which closed in 1976: whatever its faults, and "
    "Synanon's, it made Dick see the deadly folly of his amphetamine use. He never "
    "again took speed regularly.",
    'Never again did Phil take speed on a regular basis-this after nearly twenty '
    'years of steadily increasing doses.',
    '1989', basis='publication')

doc('DRG-BIO-SUTIN-VITAMINS', 'biography', SUTIN, C_SUTIN,
    'Phil accidentally took seven more grams of vitamin C than called for',
    [1100, 400],
    'DRG-PKT-2374', 'critique', ['Vitamins', '2-3-74', 'Lawrence Sutin'],
    "Sutin traces the vitamin \"recipe\" to an article by the psychiatrist Harvey "
    "Ross, \"Orthomolecular Psychiatry: Vitamin Pills for Schizophrenics\", in "
    "Psychology Today for April 1974, and lists its doses of niacin, C, B6, B2 and "
    "E. Dick, he writes, took seven grams more vitamin C than called for — and "
    "never settled on a single cause.",
    'Phil accidentally took seven more grams of vitamin C than called for.',
    '1989', basis='publication')

doc('DRG-BIO-SUTIN-METZ', 'biography', SUTIN, C_SUTIN,
    'the only time he resorted to amphetamines in his final decade', [500, 300],
    'DRG-PKT-BIOGRAPHERS', 'critique',
    ['Amphetamines', 'Sobriety', 'Lawrence Sutin'],
    "September 1977: nervous about travelling to the Metz science fiction festival "
    "in France, where he was guest of honour, Dick scored a supply of speed. Sutin "
    "calls it the only time in his last decade.",
    'the only time he resorted to amphetamines in his final decade',
    '1989', basis='publication')

doc('DRG-BIO-SUTIN-ARK', 'biography', SUTIN, C_SUTIN,
    'smoking some marijuana that a visitor had left', [400, 500],
    'DRG-PKT-SACRAMENT', 'critique',
    ['Marijuana', 'Vitamins', 'Lawrence Sutin'],
    "Tim Powers's account of March 1979, quoted by Sutin. Dick had smoked marijuana "
    "a visitor left behind, felt the familiar visionary state come on — \"generally "
    "not dope-related — unless you count Vitamin C as dope\" — and demanded to see "
    "God. He was flattened by terror and saw the Ark of the Covenant.",
    'he saw the Ark of the Covenant',
    '1989', basis='publication')

doc('DRG-BIO-ANNE-SEMOX', 'biography', ANNE, C_ANNE,
    'Phil took two Semoxydrine pills a day', [600, 300],
    'DRG-PKT-BIOGRAPHERS', 'critique',
    ['Amphetamines', 'Prescription', 'Anne R. Dick'],
    "Anne R. Dick on Phil moving into her Point Reyes house in 1958: he arrived "
    "with a closet-full of pills and medicines and loved to dose the girls' colds. "
    "She, raised a Christian Scientist, kept nothing in her medicine cabinet. He "
    "took two Semoxydrine a day, \"prescribed for me years ago\"; she did not ask "
    "what for.",
    'He didn’t tell me what for and I wasn’t interested enough to ask.',
    '1995', basis='publication')

doc('DRG-BIO-ANNE-RECREATIONAL', 'biography', ANNE, C_ANNE,
    'Ray told me that there were a lot of illicit amphetamines around', [500, 400],
    'DRG-PKT-BIOGRAPHERS', 'critique',
    ['Amphetamines', 'Anne R. Dick', 'Ray Nelson'],
    "Anne R. Dick on 1964, after Phil left Point Reyes for Oakland: Ray Nelson told "
    "her there were illicit amphetamines and rumours of dealing around the cottage "
    "Phil shared with Jack Newkom, and that Phil knew more about drugs than a "
    "pharmacist they knew. On her account, recreational use begins here — after "
    "the marriage.",
    'Phil started taking amphetamines “recreationally” at this time.',
    '1995', basis='publication')

doc('DRG-BIO-ANNE-MUSHROOMS', 'biography', ANNE, C_ANNE,
    'He based his ideas on his reading about hallucinogenic mushrooms', [800, 400],
    'DRG-PKT-ELDRITCH', 'critique',
    ['The Three Stigmata of Palmer Eldritch', 'Can-D and Chew-Z', 'Sacred mushroom',
     'Anne R. Dick'],
    "Anne R. Dick reads Palmer Eldritch against Phil's churchgoing in 1963–64: the "
    "novel sets the wafer of worldly pleasure, Can-D, against a spiritual wafer, "
    "Chew-Z, brought from the skies and made from a fungus. Phil did not know about "
    "LSD then, she says; his ideas came from reading about hallucinogenic "
    "mushrooms.",
    'Phil didn’t know about LSD at this time. He based his ideas on his reading '
    'about hallucinogenic mushrooms.',
    '1995', basis='publication')

doc('DRG-BIO-ANNE-ONCE', 'biography', ANNE, C_ANNE,
    'He had such a bad trip that he never tried LSD again', [700, 100],
    'DRG-PKT-PSYCHEDELICS', 'critique', ['LSD', 'Anne R. Dick', 'Ray Nelson'],
    "Anne R. Dick's version of the LSD trip with Ray Nelson: eight hours of "
    "sweating, isolation, a spear thrust through the body, Latin, a Roman "
    "gladiator's life. On her account it was the only one.",
    'He had such a bad trip that he never tried LSD again.',
    '1995', basis='publication')

doc('DRG-BIO-ANNE-SEVENTY', 'biography', ANNE, C_ANNE,
    'He took seventy pills a day', [800, 400],
    'DRG-PKT-MARIN', 'critique',
    ['Amphetamines', 'Prescription', 'Anne R. Dick', 'Nancy Hackett'],
    "Anne R. Dick's informants on the late 1960s: Alys Graveson remembers "
    "Dexedrine, Benzedrine and antidepressants from three doctors, one later "
    "convicted for supplying addicts; Nancy Hackett gives the list — Stelazine, "
    "relaxants, Valium, tranquilisers, stimulants — and a number. Contaminated "
    "street speed then gave Phil acute pancreatitis.",
    'He took seventy pills a day.',
    '1995', basis='publication')

doc('DRG-BIO-ANNE-POT', 'biography', ANNE, C_ANNE,
    'He liked how he felt on speed', [800, 400],
    'DRG-PKT-MARIN', 'critique',
    ['Amphetamines', 'Marijuana', 'Drug culture', 'Anne R. Dick'],
    "Cindy, a seventeen-year-old who came to the Santa Venetia house in 1970 with "
    "her boyfriend, Phil's methedrine supplier, told Anne R. Dick that Phil took a "
    "thousand \"beans\" a week, wrote, crashed for a week, and once flushed a "
    "thousand when a police car passed. He liked feeling powerful on speed. He "
    "would not touch pot.",
    'Phil wouldn’t touch pot, he hated it.',
    '1995', basis='publication')

doc('DRG-BIO-ANNE-DRA', 'biography', ANNE, C_ANNE,
    'Although Phil kept telling Dr. A he was a drug addict', [500, 300],
    'DRG-PKT-MARIN', 'critique', ['Amphetamines', 'Anne R. Dick'],
    "Late 1971: Dick asks his psychiatrist to hospitalise him for protection, and "
    "is admitted to the Marin mental health clinic. He keeps telling the doctor he "
    "is an addict; the doctor, seeing no withdrawal symptoms, thinks him a "
    "hypochondriac. Cindy, told this later: \"Phil carried his 'beans' with him "
    "wherever he went.\"",
    'Dr. A believed Phil was just being hypochondriacal.',
    '1995', basis='publication')

doc('DRG-BIO-ANNE-DORIS', 'biography', ANNE, C_ANNE,
    'Doris believed he was off all drugs', [500, 300],
    'DRG-PKT-BIOGRAPHERS', 'critique',
    ['Marijuana', 'Sobriety', 'Anne R. Dick'],
    "Dick's last years in Santa Ana, as his friend Doris Sauter described them to "
    "Anne R. Dick: a quiet life, Thursday drinks at Tim Powers's, and no "
    "amphetamines at all. \"He did a little grass, a little coke; that was all.\"",
    'He did a little grass, a little coke; that was all.',
    '1995', basis='publication')

doc('DRG-BIO-ARNOLD-WRONGDRUG', 'biography', ARNOLD, C_ARNOLD,
    'many have focused on the wrong drug: LSD', [800, 400],
    'DRG-PKT-BIOGRAPHERS', 'causal_theory',
    ['Amphetamines', 'LSD', 'Paranoia', 'Kyle Arnold'],
    "Arnold, a clinical psychologist, states his thesis in the introduction: Dick's "
    "paranoid episodes — the government agents, the 1971 hospitalisation — are "
    "\"most parsimoniously explained\" as byproducts of speed, which he had taken "
    "since childhood asthma. Commentators who blamed drugs picked the wrong one. "
    "Dick took LSD only occasionally.",
    'many have focused on the wrong drug: LSD',
    '2016', basis='publication')

doc('DRG-BIO-ARNOLD-EPHEDRINE', 'biography', ARNOLD, C_ARNOLD,
    'By age six, Dick was taking an amphetamine medication for asthma', [400, 300],
    'DRG-PKT-AMPH', 'critique',
    ['Amphetamines', 'Prescription', 'Kyle Arnold'],
    "Arnold on Dick's childhood: separations, anxiety, difficulty swallowing, "
    "asthma — and ephedrine for the asthma by age six, \"the first of many "
    "prescription drugs Dick was to use and abuse\", starting the trajectory that "
    "ended in paranoid delusions. Sutin also mentions the asthma pill and calls it "
    "an amphetamine.",
    'By age six, Dick was taking an amphetamine medication for asthma called ephedrine.',
    '2016', basis='publication',
    note="Ephedrine is a related sympathomimetic stimulant, not an amphetamine in "
         "the strict pharmacological sense; both biographers call it one.")

doc('DRG-BIO-ARNOLD-ANNE', 'biography', ARNOLD, C_ARNOLD,
    'he secretly wolfed down increasingly massive doses', [500, 600],
    'DRG-PKT-BIOGRAPHERS', 'causal_theory',
    ['Amphetamines', 'Paranoia', 'Productivity', 'Kyle Arnold', 'Anne R. Dick'],
    "Arnold reads the Point Reyes marriage clinically. Anne's memoir says the fights "
    "came from \"no identifiable source\"; Arnold adds Dick's past, and his "
    "amphetamines, taken in secret and in growing doses, with the paranoia that "
    "follows — the gate scene where Dick fled, believing Anne meant to run him "
    "over.",
    'During his marriage to Anne, he secretly wolfed down increasingly massive '
    'doses to fuel the frenetic pace of his writing.',
    '2016', basis='publication')

doc('DRG-BIO-ARNOLD-PSYCHOSIS', 'biography', ARNOLD, C_ARNOLD,
    'All the symptoms some Dick scholars cite as evidence of schizophrenia',
    [600, 500],
    'DRG-PKT-BIOGRAPHERS', 'causal_theory',
    ['Amphetamines', 'Psychosis', 'Paranoia', 'Kyle Arnold'],
    "Against the diagnosis of schizophrenia, Arnold argues that Dick's paranoia "
    "around 1974 was not an onset but a chronic baseline built over years of "
    "amphetamine dependence, and that a writer of forty-four novels does not fit "
    "the typical picture of schizophrenia.",
    'All the symptoms some Dick scholars cite as evidence of schizophrenia can be '
    'explained by the amphetamine psychosis we know, beyond a shadow of a doubt, '
    'Dick had.',
    '2016', basis='publication')

doc('DRG-BIO-ARNOLD-COVERT', 'biography', ARNOLD, C_ARNOLD,
    'Some assert that he was still abusing amphetamines', [600, 300],
    'DRG-PKT-BIOGRAPHERS', 'critique',
    ['Amphetamines', 'Sobriety', 'Kyle Arnold', 'Tessa'],
    "Arnold on the medicines around February 1974: Percodan after the dental "
    "surgery, a diuretic for blood pressure, psychiatric drugs that may have "
    "included lithium. Some sources, he says, assert Dick was still abusing "
    "amphetamines; his wife Tessa did not see it, but he had hidden it from Anne "
    "too.",
    'Some assert that he was still abusing amphetamines.',
    '2016', basis='publication')

doc('DRG-SCH-RICKMAN-FACTS', 'criticism', RICKMAN, C_RICKMAN,
    'The facts appear to be that he was a heavy user of amphetamines for twenty years',
    [300, 700],
    'DRG-PKT-BIOGRAPHERS', 'critique',
    ['Amphetamines', 'LSD', 'Reputation', 'Gregg Rickman'],
    "Rickman's introduction, written two years after Dick's death, sets out to "
    "correct \"more nonsense\" than on any other subject: twenty years of heavy "
    "amphetamine use, from the early fifties to about 1973, legally over-"
    "prescribed; LSD only two or three times, and late. The collapsing realities "
    "of the novels, he concludes, come from imagination, not drugs.",
    'he took LSD only two or three times, and not ’til about 1967',
    '1984', basis='publication')

doc('DRG-SCH-BUTLER-ELDRITCH', 'criticism', BUTLER,
    'Andrew M. Butler, Philip K. Dick (Pocket Essentials, revised edition)',
    'with whom female colonists empathise on taking the illegal drug Can-D',
    [300, 500],
    'DRG-PKT-FICTION', 'definition',
    ['Can-D and Chew-Z', 'The Three Stigmata of Palmer Eldritch'],
    "Butler's synopsis of Palmer Eldritch, whose text is not in this archive. "
    "Martian colonists take the illegal Can-D to inhabit the miniature world of "
    "Perky Pat; Eldritch returns from the Prox system with Chew-Z, which will make "
    "it obsolete. Butler lists the novel's ideas as bitheism, God as a real "
    "presence, transubstantiation.",
    'Explorer Palmer Eldritch has returned from the Prox System with a new drug, '
    'Chew-Z, which will make CanD obsolete.',
    'Revised edition', basis='publication', conf='low')

doc('DRG-SCH-JAMESON-CHEWZ', 'criticism', JAMESON,
    'Fredric Jameson, Archaeologies of the Future (2005)',
    'And this is precisely the case with Chew-Z', [600, 300],
    'DRG-PKT-FICTION', 'critique',
    ['Can-D and Chew-Z', 'The Three Stigmata of Palmer Eldritch'],
    "Jameson on Dick's reversals. Where a reader assumes reality is being degraded, "
    "it turns out to be the dream-world that is degraded, infected by reality — "
    "and this is the case with Chew-Z, Palmer Eldritch's campaign to drive out the "
    "Perky Pat and Can-D monopoly.",
    'it turns out on the contrary that it is the dreamworld or hallucinatory state '
    'which is degraded, and progressively infected by reality itself',
    '2005', basis='publication')
