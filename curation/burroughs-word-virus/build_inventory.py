#!/usr/bin/env python3
"""
Build `evidence-inventory.json` — the curated, classified source of truth for
the Burroughs / word virus dossier.

The inventory is authored here rather than as raw JSON so that the editorial
judgements stay readable and diffable in git history. Run after editing:

    python curation/burroughs-word-virus/build_inventory.py

Classification codes are documented in this directory's README.md.
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from mention_cards import CARDS  # noqa: E402

E = []


def add(**kw):
    kw.setdefault('on_public_page', True)
    kw.setdefault('concepts', [])
    kw.setdefault('editorial_note', None)
    kw.setdefault('confidence', 'high')
    E.append(kw)



# Folio references in the published Exegesis (Jackson & Lethem, 2011), verified
# by exact-phrase search against the edition held in this archive. Only 8 of the
# 34 Burroughs passages in our segment transcriptions appear in the published
# selection; the rest are from folders the editors did not print, which is why
# they carry a folder reference rather than a folio.
PUBLISHED_FOLIO = {
    'BWV-EX-1976-01': '29:9',
    'BWV-EX-1976-02': '29:9',
    'BWV-EX-1976-04': '29:11',
    'BWV-EX-1976-09': '16:29',
    'BWV-EX-1976-13': '38:41',
    'BWV-EX-1978-04': '83:60',
    'BWV-EX-1978-07': '83:138',
    'BWV-EX-1978-08': '1:24',
}


F90 = 'Exegesis, September 15, 1976 (folder 90)'
F20 = 'Exegesis, October 10, 1978 (folder 20)'
F90b = 'Exegesis, April 16, 1981 (folder 90)'
F53 = 'Exegesis, April 16, 1981 (folder 53)'
S15, S16, S17 = 'DOC_EXEG_SECTION_015', 'DOC_EXEG_SECTION_016', 'DOC_EXEG_SECTION_017'
D76, D78, D81 = '1976-09-15', '1978-10-10', '1981-04-16'


def ex(eid, seg, doc, date, anchor, before, after, packet, claim_type, concepts,
       citation, confidence='high', note=None, public=True, relevance=1):
    add(id=eid, relevance=relevance, register='A', confidence=confidence,
        source={'type': 'exegesis_segment', 'corpus': 'segments.raw_text',
                'id': seg, 'doc_id': doc, 'date': date, 'citation': citation},
        anchor=anchor, window=[before, after], lane='B', source_mode='exegesis',
        claim_type=claim_type, evidence_packet=packet, concepts=concepts,
        on_public_page=public, editorial_note=note)


def doc(eid, doc_id, anchor, before, after, packet, claim_type, concepts,
        citation, lane, source_mode, register, relevance=1, confidence='high',
        note=None, public=True, date=None):
    add(id=eid, relevance=relevance, register=register, confidence=confidence,
        source={'type': source_mode, 'corpus': 'document_texts.markdown_content',
                'id': doc_id, 'doc_id': doc_id, 'date': date, 'citation': citation},
        anchor=anchor, window=[before, after], lane=lane, source_mode=source_mode,
        claim_type=claim_type, evidence_packet=packet, concepts=concepts,
        on_public_page=public, editorial_note=note)


def let(eid, letter_id, anchor, before, after, packet, claim_type, concepts,
        citation, confidence='high', note=None, public=True, relevance=1):
    add(id=eid, relevance=relevance, register='A', confidence=confidence,
        source={'type': 'letter', 'corpus': 'letters.body_md', 'id': letter_id,
                'date': None, 'citation': citation},
        anchor=anchor, window=[before, after], lane='E', source_mode='letter',
        claim_type=claim_type, evidence_packet=packet, concepts=concepts,
        on_public_page=public, editorial_note=note)


# =========================================================================
# A — PKD's own words: the Exegesis
# =========================================================================

# 1976 — first reading of The Ticket That Exploded
ex('BWV-EX-1976-01', 'SEG_EXEG_1976-09-15_Dorothy_155', S15, D76,
   'the ticket that exploded" says of the Nova Mob parasites', 120, 560,
   'PKT-1976-ADOPTION', 'comparison',
   ['Nova Mob', 'Nova police', 'Thomas', 'Firebright'],
   F90 + ' — first recorded reading of The Ticket That Exploded')
ex('BWV-EX-1976-02', 'SEG_EXEG_1976-09-15_Dorothy_155', S15, D76,
   'Burroughs speaks of a virus - a word become a neural', 260, 480,
   'PKT-1976-ADOPTION', 'definition', ['word virus', 'Ubik'],
   F90 + ' — the word virus defined')
ex('BWV-EX-1976-03', 'SEG_EXEG_1976-09-15_Dorothy_155', S15, D76,
   'The virus (of Burroughs) is an information (or word) virus', 60, 620,
   'PKT-1976-ANTIINFO', 'causal_theory',
   ['anti-information', 'A Maze of Death', 'jamming'],
   F90 + ' — the virus reread as anti-information',
   note='The pivotal modification. Dick keeps the term and inverts the mechanism: '
        'not information that infects, but a block on reception.')
ex('BWV-EX-1976-04', 'SEG_EXEG_1976-09-15_Dorothy_155', S15, D76,
   'as burroughs points out, over 10 seconds of inner silence', 380, 420,
   'PKT-1976-ANTIINFO', 'comparison',
   ['subvocal speech', 'Julian Jaynes', 'jamming'],
   F90 + ' — subvocal chatter as jamming', confidence='medium')
ex('BWV-EX-1976-05', 'SEG_EXEG_1976-09-15_Dorothy_156', S15, D76,
   "the theory (Burroughs' included) that this world contains evil entities", 300, 420,
   'PKT-1976-ADOPTION', 'comparison', ['concealed entities', 'Satan'],
   F90 + ' — hidden entities and the testing world', confidence='medium')
ex('BWV-EX-1976-06', 'SEG_EXEG_1976-09-15_Dorothy_168', S15, D76,
   'Burroughs may have got the real situation down in "The Ticket That Exploded"', 220, 560,
   'PKT-1976-ADOPTION', 'self_report',
   ['word virus', '3-74', 'Zebra', 'Asklepios'],
   F90 + ' — 3-74 as remission from the word virus')
ex('BWV-EX-1976-07', 'SEG_EXEG_1976-09-15_Dorothy_168', S15, D76,
   "Equal to Burroughs' nova police", 300, 420,
   'PKT-1976-ADOPTION', 'comparison',
   ['Nova police', 'Firebright', 'cosmic Christ'],
   F90 + ' — the healing power identified with the Nova police')
ex('BWV-EX-1976-08', 'SEG_EXEG_1976-09-15_Dorothy_169', S15, D76,
   "This would explain Burroughs' results in obtaining living, latent messages", 420, 300,
   'PKT-1976-ANTIINFO', 'causal_theory', ['latent messages', 'Black Iron Prison'],
   F90 + ' — latent messages and the self-generated world', confidence='medium')
ex('BWV-EX-1976-09', 'SEG_EXEG_1976-09-15_Dorothy_174', S15, D76,
   'Burroughs is right about the Nova police', 260, 460,
   'PKT-1976-ADOPTION', 'comparison', ['Nova police', 'Stanislaw Lem'],
   F90 + ' — PKD as the quarry of the Nova police', confidence='medium')
ex('BWV-EX-1976-10', 'SEG_EXEG_1976-09-15_Dorothy_183', S15, D76,
   "shades of Burroughs' nova Mob", 420, 320,
   'PKT-1976-ADOPTION', 'comparison',
   ['Nova Mob', 'Nova police', 'Thomas', 'Black Iron Prison'],
   F90 + ' — the cop with amnesia', confidence='medium')
ex('BWV-EX-1976-11', 'SEG_EXEG_1976-09-15_Dorothy_187', S15, D76,
   'This fits the "replicating virus" theory of Burroughs', 360, 400,
   'PKT-1976-ADOPTION', 'comparison', ['replicating virus', 'Rome', 'Zebra'],
   F90 + ' — Rome CAD 45 as a replicating organism')
ex('BWV-EX-1976-12', 'SEG_EXEG_1976-09-15_Dorothy_188', S15, D76,
   "This is very much like Burroughs' formulation", 300, 480,
   'PKT-1976-ADOPTION', 'comparison',
   ['Nova Mob', 'Nova police', 'latent messages'],
   F90 + ' — two transtemporal organisms')
ex('BWV-EX-1976-13', 'SEG_EXEG_1976-09-15_Dorothy_192', S15, D76,
   'Burroughs posits an information virus', 420, 400,
   'PKT-1976-ANTIINFO', 'definition',
   ['living information', 'Logos', 'King Felix'],
   F90 + ' — living information, Logos, KING FELIX')

# 1978
ex('BWV-EX-1978-01', 'SEG_EXEG_1978-10-10_SECTION_016_07', S16, D78,
   'William Burroughs is correct.', 460, 340,
   'PKT-1978-QUALIFIED', 'causal_theory',
   ['occlusion', 'A Scanner Darkly', 'heavy metals'],
   F20 + ' — impairment, not evolutionary leap')
ex('BWV-EX-1978-02', 'SEG_EXEG_1978-10-10_SECTION_016_13', S16, D78,
   'But this is not an occluding, toxifying "virus"', 300, 620,
   'PKT-1978-REVALUED', 'causal_theory',
   ['anti-information', 'Zebra', 'A Maze of Death', 'A Scanner Darkly',
    'The Electric Ant', 'Impostor'],
   F20 + ' — the information virus revalued as the cure',
   note='NEW in the 2026-09-04 sweep. Dick keeps the term and reverses its valence '
        'three years before the 1981 entry usually read as the reversal, and maps it '
        'onto four of his own novels.')
ex('BWV-EX-1978-03', 'SEG_EXEG_1978-10-10_SECTION_016_75', S16, D78,
   "william Burroughs' latent message stuff", 380, 420,
   'PKT-CUTUP', 'comparison', ['latent messages', 'Acts', 'The Bacchae'],
   F20 + ' — random generation and the second Advent', confidence='medium')
ex('BWV-EX-1978-04', 'SEG_EXEG_1978-10-10_SECTION_016_255', S16, D78,
   'Burroughs is right but he has only a bit of the whole picture', 420, 400,
   'PKT-1978-QUALIFIED', 'critique',
   ['living information', 'King Felix', 'Flow My Tears'],
   F20 + ' — living latent information and KING FELIX')
ex('BWV-EX-1978-05', 'SEG_EXEG_1978-10-10_SECTION_016_264', S16, D78,
   'I doubt very much if the plasmate is an occluding agent', 280, 560,
   'PKT-1978-QUALIFIED', 'self_report',
   ['plasmate', 'information virus', 'paranoia'],
   F20 + ' — the "contamination" reading traced to Burroughs and to fear',
   note="Dick names his own paranoia as one of the two sources of the reading he is "
        "abandoning.")
ex('BWV-EX-1978-06', 'SEG_EXEG_1978-10-10_SECTION_016_265', S16, D78,
   'roughs is right. Is it the plasmate? maybe so.', 420, 360,
   'PKT-1978-QUALIFIED', 'causal_theory',
   ['occluding life form', 'plasmate', 'enslavement'],
   F20 + ' — "Burroughs is right": the occluding life form',
   note='NEW in the sweep. The pessimistic pole, in the same section as '
        'BWV-EX-1978-02. The two readings coexist; neither supersedes the other. '
        'Anchor begins mid-word because the source hyphenates "Bur¬roughs".')
ex('BWV-EX-1978-07', 'SEG_EXEG_1978-10-10_SECTION_016_267', S16, D78,
   'This is what William Burroughs discovered (but interprets differently)', 460, 340,
   'PKT-1978-QUALIFIED', 'critique', ['Valis', 'Acts', 'living information'],
   F20 + ' — the sacred narrative replicating in new information')
ex('BWV-EX-1978-08', 'SEG_EXEG_1978-10-10_SECTION_016_278', S16, D78,
   'Burroughs\' "Junky" will', 300, 380,
   'PKT-STYLE', 'comparison', ['Junky', 'enantiodromia', 'Ubik'],
   F20 + ' — Junky against ponderous philosophy', confidence='medium')
ex('BWV-EX-1978-09', 'SEG_EXEG_1978-10-10_SECTION_016_284', S16, D78,
   'This is no information virus; this is blindness.', 420, 380,
   'PKT-1978-QUALIFIED', 'critique',
   ['blindness', 'Eye in the Sky', 'idios kosmos', 'Ubik'],
   F20 + ' — a third position: not a virus but blindness',
   note='NEW in the sweep. A third reading, again in the same section. The segment '
        'carries an internal folder marker dated 10-20-80, so section 016 spans more '
        'than one sitting — treat its internal chronology with care.')
ex('BWV-EX-1978-10', 'SEG_EXEG_1978-10-10_SECTION_016_304', S16, D78,
   "Some kind of living information (Burrough's information virus) got away", 420, 400,
   'PKT-1978-QUALIFIED', 'causal_theory',
   ['Ubik', 'Valis', 'psychotronics', 'Soviet'],
   F20 + ' — the virus as escaped Soviet technology',
   note='NEW in the sweep. The most literal-minded version: the information virus as a '
        'laboratory escape rather than a metaphysical condition.')
ex('BWV-EX-1978-11', 'SEG_EXEG_1978-10-10_SECTION_016_347', S16, D78,
   'related to william Burroughs latent messages + info virus', 460, 260,
   'PKT-CUTUP', 'comparison', ['latent messages', 'syntax', 'Valis'],
   F20 + ' — message collages, syntax, and Valis')

# 1981
ex('BWV-EX-1981-01', 'SEG_EXEG_1981-04-16_Pat_02', S17, D81,
   'Burroughs, too, in his own way is right', 420, 340,
   'PKT-1981-REVERSAL', 'comparison',
   ['occlusion', 'A Scanner Darkly', 'Calvin', 'Black Iron Prison'],
   F90b + ' — Good Friday: occlusion, Calvin, A Scanner Darkly')
ex('BWV-EX-1981-02', 'SEG_EXEG_1981-04-16_Pat_05', S17, D81,
   'Man is not occluded by an "information virus,"', 260, 620,
   'PKT-1981-REVERSAL', 'causal_theory',
   ['information virus', 'living information', 'plasmate', 'King Felix'],
   F90b + ' — the reversal stated outright')
ex('BWV-EX-1981-03', 'SEG_EXEG_1981-04-16_Pat_44', S17, D81,
   'So it is like an occluding information virus', 380, 380,
   'PKT-1981-PERSISTENCE', 'allegory',
   ['Torah', 'fate', 'programming', 'control'],
   F90b + ' — Torah as occluding information virus',
   note='NEW in the sweep. Written in the same sitting as the reversal, and it keeps '
        'the occluding reading, transferred from Burroughs’ virus to Torah.')
ex('BWV-EX-1981-04', 'SEG_EXEG_1981-04-16_Pat_46', S17, D81,
   'as the "information virus" controls + occludes + enslaves us', 380, 420,
   'PKT-1981-PERSISTENCE', 'causal_theory',
   ['frozen information', 'living information', 'Torah', 'Christ'],
   F90b + ' — the virus penetrated by living hyper-information',
   note='NEW in the sweep. Resolves the tension not by dropping the occluding virus '
        'but by setting a second, living information against it.')
ex('BWV-EX-1981-05', 'SEG_EXEG_1981-04-16_Pat_154', S17, D81,
   'Someone in reading "Valis" will see the correlation to Burroughs', 260, 480,
   'PKT-1981-REVERSAL', 'critique', ['Valis', 'Gnosticism', 'Valentinus'],
   F90b + ' — VALIS as gnosis: "But W. Burroughs not Valentinus"')
ex('BWV-EX-1981-06', 'SEG_EXEG_1981-04-16_Pat_154', S17, D81,
   'Burroughs never guessed this', 440, 340,
   'PKT-1981-REVERSAL', 'critique',
   ['information virus', 'Valis', 'I Ching', 'dual messages'],
   F90b + ' — the info virus splits VALIS into dual messages')
ex('BWV-EX-1981-07', 'SEG_EXEG_1981-04-16_Pat_154', S17, D81,
   'he ensnared him as the info virus of Burroughs', 420, 400,
   'PKT-1981-PERSISTENCE', 'allegory',
   ['Manichaeism', 'Satan', 'beauty', 'The Divine Invasion'],
   F90b + ' — the beautiful virus as Satan’s temptation')
ex('BWV-EX-1981-08', 'SEG_EXEG_1981-04-16_Pat_155', S17, D81,
   'This very slightly resembles Burroughs, but is much more radical', 460, 300,
   'PKT-1981-REVERSAL', 'critique', ['Hans Jonas', 'Manichaeism', 'anamnesis'],
   F90b + ' — Jonas on Manichaeism outflanks Burroughs')
ex('BWV-EX-1981-09', 'SEG_EXEG_1981-04-16_Pat_155', S17, D81,
   'it controls us (as Burroughs teaches)', 420, 400,
   'PKT-1981-PERSISTENCE', 'causal_theory',
   ['acosmism', 'living information', 'I Ching'],
   F90b + ' — radical acosmism: living info as world')
ex('BWV-EX-1981-10', 'SEG_EXEG_1981-04-16_Pat_181', S17, D81,
   'as William Burroughs found- when any written text is cut up', 380, 400,
   'PKT-CUTUP', 'comparison',
   ['cut-up', 'Hagia Sophia', 'Torah', 'coaxial realities'],
   F53 + ' — the cut-up method and Hagia Sophia reading Torah')


PUB = 'DOC_ARCH_THE_EXEGESIS_OF_PHILIP_K_DICK_DICK_PHILI'


# ---- From the published Exegesis, absent from our segment transcriptions ----
# These were found by sweeping the Jackson & Lethem edition held in the archive,
# not the folder transcriptions. They carry folio references.

def pub(eid, anchor, before, after, packet, claim_type, concepts, folio,
        note=None, confidence='high', relevance=1, register='A'):
    add(id=eid, relevance=relevance, register=register, confidence=confidence,
        source={'type': 'exegesis_published',
                'corpus': 'document_texts.markdown_content',
                'id': PUB, 'doc_id': PUB, 'date': None,
                'published_folio': folio,
                'citation': f'The Exegesis of Philip K. Dick, ed. Jackson & Lethem '
                            f'(2011), folio [{folio}]'},
        anchor=anchor, window=[before, after], lane='B', source_mode='exegesis',
        claim_type=claim_type, evidence_packet=packet, concepts=concepts,
        on_public_page=True, editorial_note=note)


pub('BWV-EXP-15-100',
    "What if the proto-story in _Tears_ is a sort of living DNA?", 60, 900,
    'PKT-CUTUP', 'causal_theory',
    ['cut-up', 'Bateson', 'living DNA', 'entelechy', 'Flow My Tears', 'eucharist'],
    '15:100',
    note='NOT in our segment transcriptions; found only in the published edition. '
         'Dick sets the cut-up method beside Bateson’s immanent mind and the '
         'eucharist, and arrives at the formulation that governs the late work: a '
         'living word-entity taking us over through the messages we receive.')

pub('BWV-EXP-19-35',
    'shades of William Burroughs: a criminal virus!', 900, 620,
    'PKT-1978-QUALIFIED', 'causal_theory',
    ['occlusion', 'A Scanner Darkly', 'immune system', 'heavy metal', 'Black Iron Prison'],
    '19:35',
    note='NOT in our segment transcriptions. The most precise statement Dick makes '
         'of the self-concealing nature of the impairment — a brain damaged in '
         'exactly the circuits that would notice the damage — and he names A Scanner '
         'Darkly as “the Key Book in the sequence” in the same breath.')

pub('BWV-EXP-90-16A',
    'I am a word junky, a word disease', 700, 500,
    'PKT-LANGUAGE-CONTROL', 'allegory',
    ['language', 'Angel Archer', 'The Transmigration of Timothy Archer', 'words'],
    '90:16A', relevance=3, confidence='medium',
    note='Dick on Angel Archer’s failure to leap from words to the non-verbal. The '
         'phrasing is Burroughsian — addiction and disease as metaphors for language '
         '— but Burroughs is not named and the debt cannot be demonstrated. Recorded '
         'as a possible influence (relevance 3), not as a reference.')

pub('BWV-EXP-90-6A',
    "**Burroughs, William S** . (1914–1997): Experimental Beat writer.", 30, 420,
    'PKT-SCHOLARSHIP', 'critique',
    ['cut-up', 'Brion Gysin', 'control system', 'editorial apparatus'],
    '90:6A', register='C',
    note='The published edition’s own glossary. It dates Dick’s cut-up experiment to '
         '1978, which Sutin leaves undated — the only dating of that experiment in the '
         'archive. Note an error in the same sentence: Gysin was British-Canadian, born '
         'in Taplow, not Swiss. Editorial apparatus, so register C, not Dick’s words.')


# =========================================================================
# A — PKD's own words: letters
# =========================================================================

SL7576 = 'Selected Letters 1975–1976'
SL7779 = 'Selected Letters 1977–1979'
SL8082 = 'Selected Letters 1980–1982'

let('BWV-LET-1976-01', 'LET_1976-01-12_BILL_SARILL_0198',
    'They want people like William Burroughs, Kurt Vonnegut', 420, 460,
    'PKT-STYLE', 'self_report', ['A Scanner Darkly', 'Doubleday', 'blurb'],
    'Letter to Bill Sarill, January 12, 1976 — ' + SL7576,
    note='Earliest dated Burroughs reference found in the archive. Note that it is '
         'about publishing, not ideas: eight months before Dick reads him.')
let('BWV-LET-1976-02', 'LET_1976-01-12_SHARON_JARVIS_0197',
    '“In many ways, Phil Dick is to psychedelics and science fiction what William Burroughs',
    240, 420, 'PKT-STYLE', 'comparison',
    ['A Scanner Darkly', 'Oui', 'Paul Williams', 'reception'],
    'Letter to Sharon Jarvis, January 12, 1976 — ' + SL7576,
    note='Dick quoting a review in Oui. The comparison is the magazine’s, not his.')
let('BWV-LET-1979-01', 'LET_1979-10-02_RUSSELL_GALEN_0181',
    'The material on William Burroughs—the article and then the interview', 200, 400,
    'PKT-STYLE', 'self_report',
    ['the Beats', 'Rolling Stone College Papers'],
    'Letter to Kate Wenner, Rolling Stone College Papers, October 5, 1979 — ' + SL7779,
    confidence='medium')
let('BWV-LET-1981-01', 'LET_1981-01-20_BEN_ADAMS_0039',
    'Faulkner, Hemingway, Hunter S. Thompson, William Burroughs', 280, 300,
    'PKT-STYLE', 'self_report', ['reading advice', 'Hunter S. Thompson'],
    'Letter to Ben Adams, January 20, 1981 — ' + SL8082, confidence='medium')
let('BWV-LET-1981-02', 'LET_1981-02-20_RICHARD_E_GEIS_0061',
    'associ­ ated with Hunter S. Thompson and William S. Burroughs', 420, 340,
    'PKT-STYLE', 'self_report',
    ['VALIS', 'A Scanner Darkly', 'picaresque', 'Henry Miller'],
    'Letter to Richard E. Geis, February 20, 1981 — ' + SL8082)
let('BWV-LET-1981-03', 'LET_1981-02-23_PATRICIA_WARRICK_0063',
    'It is a picaresque novel blended with new elements derived from William Burroughs',
    320, 400, 'PKT-STYLE', 'self_report',
    ['VALIS', 'A Scanner Darkly', 'protest art'],
    'Letter to Patricia Warrick, February 23, 1981 — ' + SL8082)
let('BWV-LET-1981-04', 'LET_1981-04-15_BRIG_ELLIOT_0079',
    'I am familiar with his theory of an information virus', 280, 500,
    'PKT-LETTERS-DISAGREE', 'self_report',
    ['The Ticket That Exploded', 'information virus', 'A Scanner Darkly', 'occlusion'],
    'Letter to Brig Elliot, April 15, 1981 — ' + SL8082,
    note='Dated one day before the Exegesis entry that states the reversal. Dick also '
         'dates his own observation of occlusion to 1971, "before I knew of Burroughs".')
let('BWV-LET-1981-05', 'LET_1981-04-15_BRIG_ELLIOT_0079',
    'I cannot accept Burroughs’ view that we have been invaded by an alien virus',
    220, 480, 'PKT-LETTERS-DISAGREE', 'critique',
    ['information virus', 'occlusion', 'paranoia'],
    'Letter to Brig Elliot, April 15, 1981 — ' + SL8082)
let('BWV-LET-1981-06', 'LET_1981-04-15_BRIG_ELLIOT_0079',
    'Where Burroughs and I sharply disagree', 300, 500,
    'PKT-LETTERS-DISAGREE', 'critique',
    ['information life form', 'occlusion', '3-74', 'benign'],
    'Letter to Brig Elliot, April 15, 1981 — ' + SL8082)
let('BWV-LET-1981-06B', 'LET_1981-04-15_BRIG_ELLIOT_0079',
    'if you grant an occluding information virus, are you not then yourself occluded',
    340, 260, 'PKT-LETTERS-DISAGREE', 'critique',
    ['epistemology', 'paradox', 'VALIS', 'occlusion', '3-74'],
    'Letter to Brig Elliot, April 15, 1981 — Selected Letters 1980–1982, p. 146',
    note='The close of the letter, and the sharpest thing in the dossier: if the '
         'occlusion is real then any analysis of it is also occluded, including this '
         'one. Dick names VALIS as where he tries to deal with the trap.')

let('BWV-LET-1981-07', 'LET_1981-08-18_PATRICIA_WARRICK_0132',
    'This life form has not invaded our universe (as William Burroughs supposes)', 380, 440,
    'PKT-LETTERS-DISAGREE', 'critique',
    ['VALIS', 'Logos', 'Torah', 'Ditheon'],
    'Letter to Patricia Warrick, August 18, 1981 — ' + SL8082)
let('BWV-LET-1981-08', 'LET_1981-08-18_PATRICIA_WARRICK_0132',
    'a far cry from Burroughs’ notion that we have been invaded by an information virus',
    460, 120, 'PKT-LETTERS-DISAGREE', 'critique',
    ['information virus', 'Logos', '3-74'],
    'Letter to Patricia Warrick, August 18, 1981 — ' + SL8082,
    note='The last dated Burroughs reference in the archive.')

# =========================================================================
# A — PKD's own words: interview and essay
# =========================================================================

doc('BWV-INT-1981-01', 'DOC_ARCH_PHILIP_K_DICK_IN_HIS_OWN_WORDS_GREGG_RIC',
    'about the parasitic information virus', 420, 520,
    'PKT-LETTERS-DISAGREE', 'critique',
    ['information virus', 'Robert Anton Wilson', 'conspiracy', 'paranoia'],
    'Gregg Rickman, Philip K. Dick: In His Own Words — interview',
    lane='E', source_mode='interview', register='A',
    note='NEW in the sweep. The only interview in the archive where Dick discusses the '
         'word virus. He classes it as a malign-conspiracy belief and contrasts it with '
         'the benign conspiracy he and Robert Anton Wilson prefer — consistent with '
         'the 1981 letters, and a third venue for the same argument.')

doc('BWV-ESS-1978-01', 'DOC_ARCH_HOW_TO_BUILD_A_UNIVERSE_THAT_DOESN_T_FAL',
    'The basic tool for the manipulation of reality is the manipulation of words',
    120, 620, 'PKT-LANGUAGE-CONTROL', 'definition',
    ['language as control', 'Orwell', 'spurious realities', 'media'],
    'PKD, "How to Build a Universe That Doesn’t Fall Apart Two Days Later" (1978)',
    lane='E', source_mode='interview', register='A', relevance=3,
    note='Dick’s clearest statement of language-as-control, written the same year as '
         '"William Burroughs is correct" — but he credits Orwell, not Burroughs. '
         'Lapoujade reads this passage as proximity to Burroughs (register C); Dick’s '
         'own attribution is register A. Do not collapse the two.')

# =========================================================================
# C — what scholars and biographers argue
# =========================================================================

SUTIN = 'DOC_ARCH_DIVINE_INVASIONS_A_LIFE_OF_PHI_LAWRENCE_'
LAPOU = 'DOC_ARCH_DAVID_LAPOUJADE_WORLDS_BUILT_TO_FALL_APA'

doc('BWV-SCH-SUTIN-01', SUTIN,
    'He called attention to the similarities between Phil', 380, 620,
    'PKT-SCHOLARSHIP', 'critique',
    ['K.W. Jeter', 'cut-up', 'Acts', 'Moby Dick', 'The Detective'],
    'Lawrence Sutin, Divine Invasions: A Life of Philip K. Dick (1989)',
    lane='D', source_mode='criticism', register='C',
    note='THE key biographical finding. Sutin identifies the "KW" of the 1976 Exegesis '
         'entries as K.W. Jeter, reports that Jeter drew the Burroughs parallel, and '
         'records that Dick and Jeter performed their own cut-up experiment on Moby Dick, '
         'Roderick Thorp’s The Detective and the Book of Acts — the same Acts '
         'material Dick elsewhere claims generated itself in Flow My Tears.')
doc('BWV-SCH-SUTIN-02', SUTIN,
    'Jung, Kant, William Burroughs, the Bible', 420, 380,
    'PKT-SCHOLARSHIP', 'critique', ['reading', 'influences'],
    'Lawrence Sutin, Divine Invasions (1989)',
    lane='D', source_mode='criticism', register='C', confidence='medium',
    note='Sutin places Burroughs in Dick’s lifelong reading. Note the tension with '
         'Dick’s own statement to Brig Elliot that he did not know Burroughs before '
         '1971–76; Sutin gives no date for the reading.')
doc('BWV-SCH-SUTIN-03', SUTIN,
    'A student once asked William Burroughs if he believed in life after death', 300, 460,
    'PKT-SCHOLARSHIP', 'critique', ['Ubik', 'half-life', 'death'],
    'Lawrence Sutin, Divine Invasions (1989)',
    lane='D', source_mode='criticism', register='C',
    note='Sutin uses a Burroughs anecdote to frame Ubik’s central question. This is '
         'the biographer’s comparison, not Dick’s.')
doc('BWV-SCH-SUTIN-04', SUTIN,
    'William Burroughs employs a junkie patois', 380, 420,
    'PKT-SCHOLARSHIP', 'critique',
    ['A Scanner Darkly', 'The Soft Machine', 'The Wild Boys', 'style'],
    'Lawrence Sutin, Divine Invasions (1989)',
    lane='D', source_mode='criticism', register='C',
    note='Sutin judges Dick’s drug dialogue more accurate than Burroughs’.')
doc('BWV-SCH-SUTIN-05', SUTIN,
    'if, say, William Burroughs and Thomas Pynchon', 420, 360,
    'PKT-SCHOLARSHIP', 'critique', ['genre', 'marketing', 'VALIS'],
    'Lawrence Sutin, Divine Invasions (1989)',
    lane='D', source_mode='criticism', register='C', confidence='medium')

doc('BWV-SCH-LAPO-01', LAPOU,
    'On this point, Dick is rather close to William S. Burroughs', 460, 620,
    'PKT-SCHOLARSHIP', 'critique',
    ['language as control', 'Nova Express', 'word virus', 'How to Build a Universe'],
    'David Lapoujade, Worlds Built to Fall Apart: Versions of Philip K. Dick',
    lane='C', source_mode='criticism', register='C',
    note='The most sustained scholarly treatment of the connection in this archive. '
         'Lapoujade quotes Burroughs’ "Word begets image and image is virus" '
         '(Nova Express) beside Dick’s "How to Build a Universe" passage.')
doc('BWV-SCH-LAPO-02', LAPOU,
    'This proximity between Dick and Burroughs stems in part from their readings of Alfred Korzybski',
    120, 620, 'PKT-SCHOLARSHIP', 'causal_theory',
    ['Korzybski', 'general semantics', 'language'],
    'David Lapoujade, Worlds Built to Fall Apart',
    lane='C', source_mode='criticism', register='C',
    note='Lapoujade’s causal claim: Korzybski is a shared source rather than '
         'Burroughs being a source for Dick. The archive contains no direct evidence '
         'either way for Dick’s Korzybski reading; treat as register C.')
doc('BWV-SCH-LAPO-03', LAPOU,
    'the propagative power of a virus', 420, 420,
    'PKT-SCHOLARSHIP', 'critique', ['simulacra', 'trash', 'kipple', 'virus'],
    'David Lapoujade, Worlds Built to Fall Apart',
    lane='C', source_mode='criticism', register='C', confidence='medium')
doc('BWV-SCH-LAPO-04', LAPOU,
    'There are no soft drugs in Dick', 200, 500,
    'PKT-SCHOLARSHIP', 'critique',
    ['drugs', 'The Three Stigmata of Palmer Eldritch', 'control'],
    'David Lapoujade, Worlds Built to Fall Apart',
    lane='C', source_mode='criticism', register='C', confidence='medium')
doc('BWV-SCH-LAPO-05', LAPOU,
    'cooperatives and bureaucracies that Burroughs established', 400, 420,
    'PKT-SCHOLARSHIP', 'critique', ['Naked Lunch', 'bureaucracy', 'parasite'],
    'David Lapoujade, Worlds Built to Fall Apart',
    lane='C', source_mode='criticism', register='C', confidence='medium')

doc('BWV-SCH-BUTLER-01', 'DOC_ARCH_ANDREW_M_BUTLER_PHILIP_K_DICK_REVISED_AN',
    'Burroughs’ testimony about his own sickness', 460, 300,
    'PKT-SCHOLARSHIP', 'critique',
    ['A Scanner Darkly', 'Junky', 'Author’s Note', 'drugs'],
    'Andrew M. Butler, Philip K. Dick (Pocket Essentials, rev. ed.)',
    lane='C', source_mode='criticism', register='C', confidence='medium',
    note='Butler compares the Author’s Note of A Scanner Darkly to Burroughs’ '
         'prefatory testimony in Junky.')

doc('BWV-REC-DAVIS-01', 'DOC_ARCH_OXFORD_BOOKWORMS_LIBRARY_STAGE_5_OXFORD_',
    'belonged to William Burroughs, the millennium belongs to Philip K. Dick', 60, 90,
    'PKT-SCHOLARSHIP', 'comparison', ['reception', 'Erik Davis', 'canon'],
    'Erik Davis in Details, quoted as a jacket endorsement on Do Androids Dream of '
    'Electric Sheep?',
    lane='C', source_mode='criticism', register='C', relevance=2, confidence='medium',
    note='Reception rather than argument: Burroughs as the writer Dick is measured '
         'against. The same line is reprinted in the fanzine Simulacrum Meltdown 3, '
         'there in the present tense ("belong to William Burroughs").')

# =========================================================================
# Recorded but NOT published: negatives and false positives.
# Recording these is the point — the next researcher should not have to
# re-derive that "junkie" in A Scanner Darkly is ordinary English.
# =========================================================================

def neg(eid, what, why, relevance=5, note=None):
    add(id=eid, relevance=relevance, register='B', confidence='high',
        source={'type': 'negative_finding', 'corpus': 'multiple',
                'id': None, 'date': None, 'citation': what},
        anchor=None, window=None, lane=None, source_mode=None,
        claim_type=None, evidence_packet=None, concepts=[],
        on_public_page=False, editorial_note=(note or why))


neg('BWV-NEG-01',
    'PKD fiction: A Scanner Darkly, VALIS, The Man in the High Castle, '
    'The Unteleported Man, Do Androids Dream, the Scanner screenplay',
    'All matches are ordinary English — "junkie"/"junky" for a drug user, '
    '"cut up" in its literal sense. No work of PKD’s fiction in this archive '
    'names Burroughs, alludes to his titles, or uses his coinages. The absence is '
    'itself a finding: the relationship is entirely a matter of the notebooks, '
    'letters and one interview.')
neg('BWV-NEG-02', 'Norman Spinrad, Science Fiction in the Real World',
    'Twelve Burroughs mentions, none about Dick. Burroughs figures as a New Wave and '
    'mainstream-literary reference point in discussions of Le Guin, Gibson, Ballard '
    'and Morrow.', relevance=4)
neg('BWV-NEG-03', 'SF Commentary 17 and 31',
    '"Nova Mob" in SF Commentary is the Melbourne science-fiction discussion group of '
    'that name, not Burroughs’ Nova Mob. SF Commentary 31’s Burroughs is '
    'Edgar Rice, in a checklist entry for The Chessmen of Mars.')
neg('BWV-NEG-04',
    'Kripal Mutants & Mystics; Erik Davis TechGnosis; Jameson Archaeologies of the '
    'Future; Philip K. Dick: Essays of the Here and Now; the Bergson study; the '
    'psychogeography audit; Anne R. Dick, The Search for Philip K. Dick',
    'All matches are index entries, bibliography lines, Edgar Rice Burroughs, or '
    '"junkie" as ordinary English. None of these works discusses Dick and Burroughs '
    'together. TechGnosis discusses the plasmate at length but never in relation to '
    'Burroughs.')
neg('BWV-NEG-05', 'Philip K. Dick: The Last Interview and Other Conversations',
    'The only Burroughs mention is on a back-matter advertisement for the Lou Reed '
    'volume in the same series.')
neg('BWV-NEG-06', 'PKD Magazine Interviews (Lupoff interview)',
    'Extended Burroughs discussion, but it is Edgar Rice Burroughs — Lupoff '
    'recounting writing a book about him and an anecdote about Howard Browne.')
neg('BWV-NEG-07', 'Pre-1976 Burroughs references',
    'None found. The earliest dated reference in the archive is the January 12, 1976 '
    'Doubleday-blurb correspondence, and that is about publishing, not ideas. The '
    'first engagement with the word virus is September 15, 1976. Sutin places Burroughs '
    'in Dick’s lifelong reading but gives no date, and Dick told Brig Elliot in '
    '1981 that he had noticed the occlusion in 1971 "before I knew of Burroughs". The '
    'archive cannot settle when Dick first read him.', relevance=4)


# =========================================================================

PACKETS = [
    ('PKT-1976-ADOPTION', 'strong',
     'In September 1976, reading The Ticket That Exploded, Dick maps Burroughs’ '
     'Nova Mob, Nova police and word virus directly onto Thomas, Firebright, Zebra and '
     'the 3-74 event.',
     'Nine passages from one sitting. Dick identifies Thomas with a Nova Mob parasite '
     'that deposited an egg in him, calls the power that intervened in 3-74 "Equal to '
     'Burroughs’ nova police", and concludes he was "somehow able to throw off the '
     'word virus". The identifications are asserted, not hedged.'),
    ('PKT-1976-ANTIINFO', 'strong',
     'In the same sitting Dick modifies what he has just borrowed: the virus is an '
     '*anti*-information virus that blocks reception and substitutes false signal.',
     '"The virus (of Burroughs) is an information (or word) virus, but in this sense: it '
     'blocks to reception of information. So it is an anti-information virus." He '
     'illustrates it with the erased instruction tape in A Maze of Death and collates it '
     'with Jaynes on the lost voices of the gods. This is the seed of everything that '
     'follows.'),
    ('PKT-1978-QUALIFIED', 'strong',
     'By October 1978 the endorsement is explicitly partial — and the same section '
     'holds at least three incompatible readings at once.',
     '"William Burroughs is correct" about impairment rather than evolutionary leap; but '
     '"Burroughs is right but he has only a bit of the whole picture", and elsewhere in '
     'the same section "This is no information virus; this is blindness." Dick also '
     'traces his own long-held "contamination" reading of the plasmate to "(1) '
     'Burroughs’ information virus theory; and (2) paranoia and paranoiac fear."'),
    ('PKT-1978-REVALUED', 'strong',
     'Also in 1978, three years before the passage usually read as the reversal, Dick '
     'has already flipped the virus’s valence: the information virus is the cure.',
     '"But this is not an occluding, toxifying ‘virus’ — it is an '
     'antitoxic, de-occlusive." He then maps the benign information virus onto four of '
     'his own novels: it abolishes the counterfeit world (Flow My Tears, A Maze of '
     'Death), lifts the inner occlusion (A Scanner Darkly), breaks astral determinism '
     '(The Electric Ant) and restores memory (Impostor).'),
    ('PKT-1981-REVERSAL', 'strong',
     'In April 1981 Dick states the reversal directly: occlusion comes first, and living '
     'information is the remedy sent to announce it.',
     '"Man is not occluded by an ‘information virus,’ i.e. living information; '
     'on the contrary: man is occluded and the living information is sent to tell him the '
     'true situation." Burroughs, he writes, discerned both living information and an '
     'occlusion, then "leaped to the pessimistic conclusion that there is a '
     'cause-and-effect relationship."'),
    ('PKT-1981-PERSISTENCE', 'strong',
     'The reversal does not hold. The same April 1981 sitting keeps the occluding virus '
     'in three other passages.',
     'Torah "is like an occluding information virus; it keeps us enslaved at the level of '
     'machines"; the living information "controls us (as Burroughs teaches)"; and Satan '
     '"ensnared him as the info virus of Burroughs, ensnared him with beauty". Dick does '
     'not choose between the readings — he lets both stand.'),
    ('PKT-LETTERS-DISAGREE', 'strong',
     'The correspondence and the one interview state the disagreement more calmly and '
     'more completely than the notebooks do.',
     'To Brig Elliot (April 15, 1981): "I cannot accept Burroughs’ view that we have '
     'been invaded by an alien virus... yet I cannot readily dismiss this bizarre theory '
     'as mere paranoia on his part... he states the problem correctly, although perhaps '
     'his analysis of the cause is faulty." And: "Where Burroughs and I sharply disagree '
     'is that my supposition is that if an information life form exists... it is benign." '
     'To Patricia Warrick (August 1981), and to Gregg Rickman on tape, he says the same.'),
    ('PKT-CUTUP', 'moderate',
     'Dick takes the cut-up method as evidence that narrative is latent in any text, and '
     'gives it a theological cause.',
     '"This is why — as William Burroughs found — when any written text is cut '
     'up + rejoined at random, a narrative results." In the April 1981 sitting the cause '
     'is Hagia Sophia reading the Torah aloud: if the ground of the world is a text being '
     'narrated, any fragment of text is already inside the narration. Sutin records that '
     'Dick and K.W. Jeter actually performed such an experiment.'),
    ('PKT-STYLE', 'moderate',
     'Burroughs also figures for Dick as a literary model and as a name in the publishing '
     'trade, independent of the virus theory.',
     'In January 1976 Doubleday wanted Burroughs and Vonnegut to blurb A Scanner Darkly '
     'and left it to Dick to approach them; he had no way in. In February 1981 he twice '
     'described VALIS as a picaresque blended with elements from Hunter S. Thompson and '
     'Burroughs. In 1978 he preferred Junky to "ponderous books of philosophy".'),
    ('PKT-LANGUAGE-CONTROL', 'moderate',
     'Dick’s own account of language as the instrument of control, written in 1978 '
     '— crediting Orwell, not Burroughs.',
     '"The basic tool for the manipulation of reality is the manipulation of words. If '
     'you can control the meaning of words, you can control the people who must use the '
     'words." Lapoujade reads this passage as Dick’s proximity to Burroughs. Dick '
     'himself cites 1984. Both things are true; they are different kinds of claim.'),
    ('PKT-SCHOLARSHIP', 'moderate',
     'What the secondary literature in this archive actually says.',
     'Sutin supplies the biographical spine: K.W. Jeter drew the parallel, and the two '
     'men performed a cut-up experiment on Moby Dick, The Detective and the Book of Acts. '
     'Lapoujade supplies the only sustained argument, reading Dick and Burroughs as '
     'convergent through a shared source in Korzybski. Butler compares the Author’s '
     'Note of A Scanner Darkly to Junky. Beyond those three, the archive’s '
     'scholarship does not treat the connection.'),
]

# Attach the published-edition folio where the passage was printed.
for e in E:
    f = PUBLISHED_FOLIO.get(e['id'])
    if f:
        e['source']['published_folio'] = f
        e['source']['citation'] += f' — published Exegesis [{f}]'
    elif e['source']['type'] == 'exegesis_segment':
        e['source']['published_folio'] = None

# Attach the reader-facing card to each finding.
missing_cards = []
for e in E:
    if not e['on_public_page']:
        continue
    card = CARDS.get(e['id'])
    if not card:
        missing_cards.append(e['id'])
        continue
    e['card'] = {'context': card[0], 'pith': card[1], 'speaker': card[2]}
if missing_cards:
    raise SystemExit(f'No mention card for: {missing_cards}')

payload = {
    'topic': 'burroughs-word-virus',
    'title': 'Burroughs and the Word Virus',
    'generated_utc': datetime.now(timezone.utc).isoformat(timespec='seconds'),
    'source_of_truth': True,
    'note': 'Hand-curated. The seeder reads this file; do not machine-overwrite it. '
            'Raw sweep output lives in raw-findings.json and is regenerable.',
    'evidence_packets': [
        {'id': p[0], 'confidence': p[1], 'claim': p[2], 'summary': p[3]}
        for p in PACKETS
    ],
    'evidence': E,
}

out = HERE / 'evidence-inventory.json'
out.write_text(json.dumps(payload, indent=1, ensure_ascii=False), encoding='utf-8')

pub = [e for e in E if e['on_public_page']]
print(f'evidence entries      {len(E)}')
print(f'  published           {len(pub)}')
print(f'  recorded not published {len(E) - len(pub)}')
by_reg = {}
for e in pub:
    by_reg[e['register']] = by_reg.get(e['register'], 0) + 1
print(f'  by register         {by_reg}')
print(f'evidence packets      {len(PACKETS)}')
print(f'mention cards        {sum(1 for e in E if e.get("card"))}')
print(f'wrote {out}')
