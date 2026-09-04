#!/usr/bin/env python3
"""
Seed the "Intertexts & Influences" study and its first topic:
"Burroughs and the Word Virus".

Everything written here is anchored to text that already exists in
database/unified.sqlite:

  * 22 Exegesis segments across sections 015 (1976-09-15), 016 (1978-10-10)
    and 017 (1981-04-16) that name Burroughs;
  * 9 letters in the Selected Letters volumes that name him.

The scholarship lane is intentionally empty; see EDITORIAL notes below.

Passages are extracted by locating a hand-picked anchor phrase in the stored
source text and taking a window around it, so every excerpt on the site is a
verbatim slice of a row already in the database. Nothing is paraphrased into
the evidence lane; interpretation lives only in the dossier prose and in the
evidence-packet summaries, which carry their own generator provenance.

Idempotent: re-running deletes and rebuilds the topic's derived rows.

Usage:
    python scripts/studies/seed_burroughs_word_virus.py
    python scripts/studies/seed_burroughs_word_virus.py --db database/unified.sqlite
"""

import argparse
import json
import re
import sqlite3
import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent.parent
DEFAULT_DB = PROJECT_DIR / 'database' / 'unified.sqlite'

STUDY_ID = 'intertexts'
STUDY_LABEL = 'Intertexts & Influences'
STUDY_DESCRIPTION = (
    "Writers and thinkers Philip K. Dick read, argued with, and absorbed into "
    "his own vocabulary. Each topic tracks a single interlocutor across the "
    "fiction, the Exegesis, and the correspondence, and holds on to the places "
    "where Dick changed his mind about them."
)

TOPIC_ID = 'TOPIC_INTERTEXT_burroughs_word_virus'
TOPIC_SLUG = 'burroughs-word-virus'
TOPIC_NAME = 'Burroughs and the Word Virus'

GENERATOR = 'claude-curated@2026-09-04'
PROVENANCE = 'editorial_curation_from_corpus_evidence'

# --------------------------------------------------------------------------
# Passage specifications.
#
# (source_kind, source_id, anchor, before, after, claim_type, confidence,
#  citation, matched_terms)
#
# `anchor` is matched case-sensitively against the stored source text; the
# window is (anchor_start - before, anchor_end + after).
# --------------------------------------------------------------------------

EXEGESIS_PASSAGES = [
    # ---- Section 015 — September 15, 1976 ---------------------------------
    ('SEG_EXEG_1976-09-15_Dorothy_155',
     'the ticket that exploded" says of the Nova Mob parasites',
     120, 560, 'comparison', 'high',
     'Exegesis, September 15, 1976 (folder 90) — first recorded reading of The Ticket That Exploded',
     ['Burroughs', 'Nova Mob', 'Nova police', 'Thomas', 'Firebright']),

    ('SEG_EXEG_1976-09-15_Dorothy_155',
     'Burroughs speaks of a virus - a word become a neural',
     260, 480, 'definition', 'high',
     'Exegesis, September 15, 1976 (folder 90) — the word virus defined',
     ['Burroughs', 'word virus', 'Ubik']),

    ('SEG_EXEG_1976-09-15_Dorothy_155',
     'The virus (of Burroughs) is an information (or word) virus',
     60, 620, 'causal_theory', 'high',
     'Exegesis, September 15, 1976 (folder 90) — the virus reread as anti-information',
     ['Burroughs', 'word virus', 'information', 'A Maze of Death']),

    ('SEG_EXEG_1976-09-15_Dorothy_155',
     'as burroughs points out, over 10 seconds of inner silence',
     380, 420, 'comparison', 'medium',
     'Exegesis, September 15, 1976 (folder 90) — subvocal chatter as jamming',
     ['Burroughs', 'Julian Jaynes', 'occlusion']),

    ('SEG_EXEG_1976-09-15_Dorothy_156',
     "the theory (Burroughs' included) that this world contains evil entities",
     300, 420, 'comparison', 'medium',
     'Exegesis, September 15, 1976 (folder 90) — hidden entities and the testing world',
     ['Burroughs', 'Satan']),

    ('SEG_EXEG_1976-09-15_Dorothy_168',
     'Burroughs may have got the real situation down in "The Ticket That Exploded"',
     220, 560, 'self_report', 'high',
     'Exegesis, September 15, 1976 (folder 90) — 3-74 as remission from the word virus',
     ['Burroughs', 'word virus', 'The Ticket That Exploded', '3-74', 'Zebra']),

    ('SEG_EXEG_1976-09-15_Dorothy_168',
     "Equal to Burroughs' nova police",
     300, 420, 'comparison', 'high',
     'Exegesis, September 15, 1976 (folder 90) — the healing power identified with the Nova police',
     ['Burroughs', 'Nova police', 'Firebright', 'cosmic Christ']),

    ('SEG_EXEG_1976-09-15_Dorothy_169',
     "This would explain Burroughs' results in obtaining living, latent messages",
     420, 300, 'causal_theory', 'medium',
     'Exegesis, September 15, 1976 (folder 90) — latent messages and the self-generated world',
     ['Burroughs', 'latent messages', 'Black Iron Prison']),

    ('SEG_EXEG_1976-09-15_Dorothy_174',
     'Burroughs is right about the Nova police',
     260, 460, 'comparison', 'medium',
     'Exegesis, September 15, 1976 (folder 90) — PKD as the quarry of the Nova police',
     ['Burroughs', 'Nova police', 'Stanislaw Lem']),

    ('SEG_EXEG_1976-09-15_Dorothy_183',
     "shades of Burroughs' nova Mob",
     420, 320, 'comparison', 'medium',
     'Exegesis, September 15, 1976 (folder 90) — the cop with amnesia',
     ['Burroughs', 'Nova Mob', 'Nova police', 'Thomas', 'Black Iron Prison']),

    ('SEG_EXEG_1976-09-15_Dorothy_187',
     'This fits the "replicating virus" theory of Burroughs',
     360, 400, 'comparison', 'high',
     'Exegesis, September 15, 1976 (folder 90) — Rome CAD 45 as a replicating organism',
     ['Burroughs', 'replicating virus', 'Rome', 'Zebra']),

    ('SEG_EXEG_1976-09-15_Dorothy_188',
     "This is very much like Burroughs' formulation",
     300, 480, 'comparison', 'high',
     'Exegesis, September 15, 1976 (folder 90) — two transtemporal organisms, Nova Mob and Nova police',
     ['Burroughs', 'Nova Mob', 'Nova police', 'latent messages']),

    ('SEG_EXEG_1976-09-15_Dorothy_192',
     'Burroughs posits an information virus',
     420, 400, 'definition', 'high',
     'Exegesis, September 15, 1976 (folder 90) — living information, Logos, KING FELIX',
     ['Burroughs', 'information virus', 'living information', 'Logos', 'King Felix']),

    # ---- Section 016 — October 10, 1978 -----------------------------------
    ('SEG_EXEG_1978-10-10_SECTION_016_07',
     'William Burroughs is correct.',
     460, 340, 'causal_theory', 'high',
     'Exegesis, October 10, 1978 (folder 20) — impairment, not evolutionary leap',
     ['Burroughs', 'occlusion', 'A Scanner Darkly', 'heavy metals']),

    ('SEG_EXEG_1978-10-10_SECTION_016_75',
     "william Burroughs' latent message stuff",
     380, 420, 'comparison', 'medium',
     'Exegesis, October 10, 1978 (folder 20) — random generation and the second Advent',
     ['Burroughs', 'latent messages', 'Acts', 'The Bacchae']),

    ('SEG_EXEG_1978-10-10_SECTION_016_255',
     'Burroughs is right but he has only a bit of the whole picture',
     420, 400, 'critique', 'high',
     'Exegesis, October 10, 1978 (folder 20) — living latent information and KING FELIX',
     ['Burroughs', 'living information', 'King Felix', 'Flow My Tears']),

    ('SEG_EXEG_1978-10-10_SECTION_016_264',
     'information virus theory',
     460, 300, 'self_report', 'high',
     'Exegesis, October 10, 1978 (folder 20) — the "contamination" reading traced to Burroughs and to fear',
     ['Burroughs', 'information virus', 'plasmate', 'paranoia']),

    ('SEG_EXEG_1978-10-10_SECTION_016_267',
     'This is what William Burroughs discovered (but interprets differently)',
     460, 340, 'critique', 'high',
     'Exegesis, October 10, 1978 (folder 20) — the sacred narrative replicating in new information',
     ['Burroughs', 'Valis', 'Acts', 'living information']),

    ('SEG_EXEG_1978-10-10_SECTION_016_278',
     'Burroughs\' "Junky" will',
     300, 380, 'comparison', 'medium',
     'Exegesis, October 10, 1978 (folder 20) — Junky against ponderous philosophy',
     ['Burroughs', 'Junky', 'enantiodromia', 'Ubik']),

    ('SEG_EXEG_1978-10-10_SECTION_016_347',
     'related to william Burroughs latent messages + info virus',
     460, 260, 'comparison', 'high',
     'Exegesis, October 10, 1978 (folder 20) — message collages, syntax, and Valis',
     ['Burroughs', 'latent messages', 'information virus', 'Valis']),

    # ---- Section 017 — April 16, 1981 -------------------------------------
    ('SEG_EXEG_1981-04-16_Pat_02',
     'Burroughs, too, in his own way is right',
     420, 340, 'comparison', 'high',
     'Exegesis, April 16, 1981 (folder 90) — Good Friday: occlusion, Calvin, and A Scanner Darkly',
     ['Burroughs', 'occlusion', 'A Scanner Darkly', 'Calvin', 'Black Iron Prison']),

    ('SEG_EXEG_1981-04-16_Pat_05',
     'Man is not occluded by an "information virus,"',
     260, 620, 'causal_theory', 'high',
     'Exegesis, April 16, 1981 (folder 90) — the inversion of Burroughs stated outright',
     ['Burroughs', 'information virus', 'living information', 'plasmate', 'King Felix']),

    ('SEG_EXEG_1981-04-16_Pat_154',
     'Someone in reading "Valis" will see the correlation to Burroughs',
     260, 480, 'critique', 'high',
     'Exegesis, April 16, 1981 (folder 90) — VALIS as gnosis, "But W. Burroughs not Valentinus"',
     ['Burroughs', 'Valis', 'Gnosticism', 'Valentinus']),

    ('SEG_EXEG_1981-04-16_Pat_154',
     'Burroughs never guessed this',
     440, 340, 'critique', 'high',
     'Exegesis, April 16, 1981 (folder 90) — the info virus splits VALIS into dual messages',
     ['Burroughs', 'information virus', 'Valis', 'I Ching']),

    ('SEG_EXEG_1981-04-16_Pat_154',
     'he ensnared him as the info virus of Burroughs',
     420, 400, 'allegory', 'high',
     'Exegesis, April 16, 1981 (folder 90) — Manichaean turn: the beautiful virus as Satan\'s temptation',
     ['Burroughs', 'information virus', 'Manichaeism', 'Satan', 'The Divine Invasion']),

    ('SEG_EXEG_1981-04-16_Pat_155',
     'This very slightly resembles Burroughs, but is much more radical',
     460, 300, 'critique', 'high',
     'Exegesis, April 16, 1981 (folder 90) — Jonas on Manichaeism outflanks Burroughs',
     ['Burroughs', 'Hans Jonas', 'Manichaeism', 'anamnesis']),

    ('SEG_EXEG_1981-04-16_Pat_155',
     'it controls us (as Burroughs teaches)',
     420, 400, 'causal_theory', 'high',
     'Exegesis, April 16, 1981 (folder 90) — radical acosmism: living info as world',
     ['Burroughs', 'living information', 'acosmism', 'I Ching']),

    ('SEG_EXEG_1981-04-16_Pat_181',
     'as William Burroughs found- when any written text is cut up',
     380, 400, 'comparison', 'high',
     'Exegesis, April 16, 1981 (folder 53) — the cut-up method and Hagia Sophia reading Torah',
     ['Burroughs', 'cut-up', 'Hagia Sophia', 'Torah', 'coaxial realities']),
]

LETTER_PASSAGES = [
    ('LET_1976-01-12_BILL_SARILL_0198',
     'They want people like William Burroughs, Kurt Vonnegut',
     420, 460, 'self_report', 'high',
     'Letter to Bill Sarill, January 12, 1976 — Selected Letters 1975–1976',
     ['Burroughs', 'A Scanner Darkly', 'Doubleday']),

    ('LET_1976-01-12_SHARON_JARVIS_0197',
     '“In many ways, Phil Dick is to psychedelics and science fiction what William Burroughs',
     240, 420, 'comparison', 'medium',
     'Letter to Sharon Jarvis, January 12, 1976 — Selected Letters 1975–1976',
     ['Burroughs', 'A Scanner Darkly', 'Oui', 'Paul Williams']),

    ('LET_1979-10-02_RUSSELL_GALEN_0181',
     'The material on William Burroughs—the article and then the interview',
     200, 400, 'self_report', 'medium',
     'Letter to Kate Wenner, Rolling Stone College Papers, October 5, 1979 — Selected Letters 1977–1979',
     ['Burroughs', 'the Beats', 'Rolling Stone College Papers']),

    ('LET_1981-01-20_BEN_ADAMS_0039',
     'Faulkner, Hemingway, Hunter S. Thompson, William Burroughs',
     280, 300, 'self_report', 'medium',
     'Letter to Ben Adams, January 20, 1981 — Selected Letters 1980–1982',
     ['Burroughs', 'reading advice', 'Hunter S. Thompson']),

    ('LET_1981-02-20_RICHARD_E_GEIS_0061',
     'associ­ ated with Hunter S. Thompson and William S. Burroughs',
     420, 340, 'self_report', 'high',
     'Letter to Richard E. Geis, February 20, 1981 — Selected Letters 1980–1982',
     ['Burroughs', 'VALIS', 'A Scanner Darkly', 'picaresque', 'Henry Miller']),

    ('LET_1981-02-23_PATRICIA_WARRICK_0063',
     'It is a picaresque novel blended with new elements derived from William Burroughs',
     320, 400, 'self_report', 'high',
     'Letter to Patricia Warrick, February 23, 1981 — Selected Letters 1980–1982',
     ['Burroughs', 'VALIS', 'A Scanner Darkly', 'protest art']),

    ('LET_1981-04-15_BRIG_ELLIOT_0079',
     'I am familiar with his theory of an information virus',
     280, 500, 'self_report', 'high',
     'Letter to Brig Elliot, April 15, 1981 — Selected Letters 1980–1982',
     ['Burroughs', 'The Ticket That Exploded', 'information virus',
      'A Scanner Darkly', 'occlusion']),

    ('LET_1981-04-15_BRIG_ELLIOT_0079',
     'I cannot accept Burroughs’ view that we have been invaded by an alien virus',
     220, 480, 'critique', 'high',
     'Letter to Brig Elliot, April 15, 1981 — Selected Letters 1980–1982',
     ['Burroughs', 'information virus', 'occlusion', 'paranoia']),

    ('LET_1981-04-15_BRIG_ELLIOT_0079',
     'Where Burroughs and I sharply disagree',
     300, 500, 'critique', 'high',
     'Letter to Brig Elliot, April 15, 1981 — Selected Letters 1980–1982',
     ['Burroughs', 'information life form', 'occlusion', '3-74']),

    ('LET_1981-08-18_PATRICIA_WARRICK_0132',
     'This life form has not invaded our universe (as William Burroughs supposes)',
     380, 440, 'critique', 'high',
     'Letter to Patricia Warrick, August 18, 1981 — Selected Letters 1980–1982',
     ['Burroughs', 'VALIS', 'Logos', 'Torah', 'Ditheon']),

    ('LET_1981-08-18_PATRICIA_WARRICK_0132',
     'a far cry from Burroughs’ notion that we have been invaded by an information virus',
     460, 120, 'critique', 'high',
     'Letter to Patricia Warrick, August 18, 1981 — Selected Letters 1980–1982',
     ['Burroughs', 'information virus', 'Logos', '3-74']),
]

# The archive holds no secondary scholarship on the Dick-Burroughs connection.
# The only Burroughs strings in the scholarship lane are an OCR-mangled 1969
# SF Commentary line about "self-conscious experimenters" that never mentions
# Dick, and an SF Commentary 31 checklist entry for Edgar Rice Burroughs.
# Neither is evidence about this topic; both are deliberately left out.
SCHOLARSHIP_PASSAGES = []

# --------------------------------------------------------------------------
# Dossier prose
# --------------------------------------------------------------------------

DOSSIER = {
    'definition': (
        "The \"word virus\" is William S. Burroughs's proposition, developed across "
        "the Nova trilogy and stated most compactly in The Ticket That Exploded (1962), "
        "that language is a parasitic organism which entered the human nervous system "
        "from outside, replicates through speech and print, and holds its hosts in a "
        "condition they cannot perceive because the perceiving apparatus is itself "
        "infected. Philip K. Dick encountered the idea in September 1976, two and a "
        "half years after 2-3-74, and spent the next five years using it: first as "
        "confirmation, then as a rival hypothesis, and finally as the exact position "
        "he needed to invert in order to state his own."
    ),
    'pkd_relevance': (
        "Burroughs gave Dick a vocabulary for something he had been circling since the "
        "early 1960s — the sense that the world is a jammed signal rather than a solid "
        "object. The Exegesis records the encounter with unusual precision. In the "
        "September 15, 1976 entries Dick has The Ticket That Exploded open beside him "
        "and reads his own experience straight out of it: the Nova Mob parasites moving "
        "from host to host become Thomas taking him over; the Nova police become the "
        "healing power that intervened in 3-74; the \"criminal virus related to words, "
        "submessages\" becomes the occlusion he believes was briefly lifted from him. "
        "But the same entries already begin the modification that will eventually become "
        "a reversal: Dick decides the virus is not an information virus at all but an "
        "anti-information one, a jamming device that blocks reception and substitutes "
        "counterfeit signal — which he immediately illustrates with the erased "
        "instruction tape in A Maze of Death."
    ),
    'in_the_fiction': (
        "No novel or story names Burroughs, and no evidence in this archive shows Dick "
        "reading him before 1976 — a point Dick makes himself in the April 15, 1981 "
        "letter to Brig Elliot, where he notes that he had observed the occlusion in "
        "drug users \"back in 1971 before I knew of Burroughs\" and had already written "
        "it into A Scanner Darkly. What the Exegesis does instead is retrofit: Dick "
        "rereads his own finished books through Burroughs. Ubik and The Three Stigmata "
        "of Palmer Eldritch become books about a replicating parasite that uses humans "
        "as hosts; A Maze of Death supplies the erased instruction tape as the emblem of "
        "blocked reception; Flow My Tears, the Policeman Said supplies the self-generating "
        "Acts material and the KING FELIX cipher, which he calls \"alive or semi-alive "
        "like a virus\"; A Scanner Darkly supplies the impaired self-monitoring circuit. "
        "The influence runs backward through the corpus, not forward into it. The only "
        "forward-running debt Dick acknowledges is stylistic: in letters to Richard Geis "
        "and Patricia Warrick in February 1981 he describes VALIS as a picaresque blended "
        "with \"modern elements associated with Hunter S. Thompson and William S. "
        "Burroughs, as well as my own 1977 novel A SCANNER DARKLY.\""
    ),
    'in_the_exegesis': (
        "Twenty-two Exegesis segments name Burroughs, clustered in three sittings. "
        "September 15, 1976 is the adoption: the Nova Mob, the Nova police, the latent "
        "message, and the word virus are all imported wholesale and mapped onto Thomas, "
        "Firebright, Zebra and 3-74. October 10, 1978 is the qualified endorsement — "
        "\"William Burroughs is correct\" about impairment rather than evolutionary leap, "
        "but \"Burroughs is right and he has only a bit of the whole picture\" about "
        "living latent information; in the same sitting Dick performs a piece of "
        "self-diagnosis, tracing his years-long reading of the plasmate's messages as a "
        "\"contamination\" back to two sources, \"(1) Burroughs' information virus theory; "
        "and (2) paranoia and paranoiac fear.\" April 16, 1981 is the inversion, stated "
        "flatly: man is not occluded by an information virus; man is already occluded, "
        "and the living information is what is being sent to tell him so. Burroughs, Dick "
        "writes, correctly discerned both living information and an occlusion and then "
        "\"leaped to the pessimistic conclusion that there is a cause-and-effect "
        "relationship.\" The same sitting also holds the darkest version, in which the "
        "beautiful living information is Satan's temptation of Christ and Burroughs's "
        "pessimism turns out to be nearly right after all, and the most technical, in "
        "which the cut-up method becomes evidence that a narrative is latent in any text "
        "because Hagia Sophia is reading Torah aloud."
    ),
    'intellectual_background': (
        "Burroughs assembled the word-virus idea from Korzybski's general semantics, "
        "Wilhelm Reich, and his own cut-up practice with Brion Gysin; the Nova trilogy "
        "(The Soft Machine, The Ticket That Exploded, Nova Express) is its narrative "
        "form. Dick reached it through the mid-1970s countercultural information "
        "current rather than through the Beat scene — although in an October 1979 letter "
        "to Rolling Stone College Papers he notes that a Burroughs interview \"leads "
        "right into my story inasmuch as he discusses the rebellion during the Fifties "
        "and the Beats, of which I was one.\" In the Exegesis, Burroughs sits alongside "
        "Julian Jaynes on the lost voices of the gods, Robert Anton Wilson on Sirius, "
        "and, decisively, Hans Jonas on Manichaeism: it is Jonas who finally gives Dick "
        "a framework he judges \"much more radical (ontologically speaking)\" than "
        "Burroughs's."
    ),
    'scholarly_debate': (
        "Dick's own assessment is the sharpest one on record, and it is unusually "
        "even-handed for him: Burroughs \"states the problem correctly, although perhaps "
        "his analysis of the cause is faulty; still, merely to be aware of the problem is "
        "to achieve a great deal.\" That formula — right about the phenomenon, wrong about "
        "the causal direction — holds across all three Exegesis sittings and both 1981 "
        "letters. Readers who treat Burroughs as a straightforward source for VALIS "
        "should weigh the fact that Dick himself insists on the difference twice in "
        "writing to Patricia Warrick, and once tells the Exegesis \"But W. Burroughs "
        "not Valentinus\" — the gnostic lineage matters more to him than the Beat one. "
        "Readers who treat the influence as negligible should weigh how much of the "
        "1976 machinery survives untranslated: the plasmate is still a living information "
        "organism that enters through the optic nerve and modulates brain function."
    ),
    'chronology_summary': (
        "September 1976: first reading of The Ticket That Exploded; wholesale adoption "
        "of the Nova Mob / Nova police / word virus apparatus, immediately reinterpreted "
        "as anti-information. October 1978: qualified endorsement; the heavy-metal and "
        "detox reading of 3-74, and the self-diagnosis of the \"contamination\" theory as "
        "part Burroughs, part fear. February 1981: Burroughs named as a stylistic source "
        "for VALIS in letters to Geis and Warrick. April 15, 1981: the letter to Brig "
        "Elliot spelling out where the two men agree and where they \"sharply disagree.\" "
        "April 16, 1981 — the very next day — the Exegesis states the inversion for "
        "itself. August 1981: to Warrick again, the final formulation, that the "
        "information life form is not an invader but the source of the universe, \"a far "
        "cry from Burroughs' notion.\""
    ),
    'contradictions_summary': (
        "The central contradiction is Dick against himself across five years: in 1976 he "
        "believes he threw off a word virus that had infected him, and in 1981 he denies "
        "that any information virus occludes anyone. It is not a clean supersession. The "
        "April 1981 sitting that states the inversion also contains a Manichaean passage "
        "in which the living information is Satan's beautiful snare and \"it controls us "
        "(as Burroughs teaches).\" A second, smaller contradiction runs between the "
        "notebooks and the correspondence: to Brig Elliot, Dick says he cannot accept an "
        "alien invasion but also cannot dismiss it as paranoia; in the Exegesis he had "
        "already named his own paranoia as one of the two sources of the theory."
    ),
    'editorial_notes': (
        "Passage text is drawn verbatim from the stored Exegesis segment transcriptions "
        "and letter bodies, which preserve handwriting- and OCR-level irregularities — "
        "\"burrought has writted,\" \"TEIE TICKET THAT EXPLODED,\" the plus sign for "
        "\"and.\" These are left as they stand rather than silently normalised; ellipses "
        "mark where an excerpt was cut. The scholarship lane is empty on purpose: this "
        "archive contains no secondary criticism on the Dick-Burroughs connection. The "
        "only two Burroughs strings in that lane are an OCR-mangled 1969 SF Commentary "
        "line about \"self-conscious experimenters\" that never mentions Dick, and an SF "
        "Commentary 31 checklist entry for Edgar Rice Burroughs. That absence is itself "
        "worth recording — the connection is documented almost entirely in Dick's own "
        "hand."
    ),
}

RELATED_THINKERS = [
    'William S. Burroughs', 'Brion Gysin', 'Julian Jaynes',
    'Robert Anton Wilson', 'Hans Jonas', 'Stanislaw Lem',
    'Hunter S. Thompson', 'Henry Miller', 'John Calvin',
]

OPEN_QUESTIONS = [
    "Which Burroughs titles did Dick actually own or read? The Exegesis and letters "
    "name only The Ticket That Exploded and Junky; the Nova Mob material he uses "
    "also appears in Nova Express and The Soft Machine.",
    "Who put The Ticket That Exploded in front of him in September 1976? The entries "
    "credit \"KW\" with several of the surrounding observations.",
    "The letter to Brig Elliot (April 15, 1981) and the Exegesis inversion (April 16, "
    "1981) are one day apart. Did writing the letter produce the reversal, or record "
    "one already reached?",
    "Did Doubleday's 1976 attempt to get a Burroughs blurb for A Scanner Darkly ever "
    "reach Burroughs? No reply appears in this archive.",
]

EVIDENCE_PACKETS = [
    ('SEV_BURROUGHS_adoption_1976',
     "In September 1976 Dick imports Burroughs's Nova Mob, Nova police and word virus "
     "wholesale and maps them onto Thomas, Firebright, Zebra and the 3-74 event.",
     "Nine segments from Exegesis section 015 track a single sitting: Dick has The "
     "Ticket That Exploded in hand, identifies Thomas with a Nova Mob parasite that "
     "deposited an egg in him, identifies the power that intervened in 3-74 as \"Equal "
     "to Burroughs' nova police,\" and concludes he was \"somehow able to throw off the "
     "word virus.\" The identification is asserted, not hedged.",
     'strong'),

    ('SEV_BURROUGHS_antiinformation_1976',
     "Dick modifies the borrowed concept in the same sitting: the virus is an "
     "anti-information virus that blocks reception and substitutes counterfeit signal.",
     "\"The virus (of Burroughs) is an information (or word) virus, but in this sense: "
     "it blocks to reception of information. So it is an anti-information virus.\" He "
     "immediately glosses it with the erased instruction tape in A Maze of Death and "
     "collates it with Jaynes on the lost voices of the gods. The modification is the "
     "seed of the later reversal.",
     'strong'),

    ('SEV_BURROUGHS_qualified_1978',
     "By October 1978 the endorsement is explicitly partial, and Dick names Burroughs "
     "as one source of his own paranoid reading of the plasmate.",
     "\"William Burroughs is correct\" about impairment rather than evolutionary leap; "
     "but on living latent information, \"Burroughs is right but he has only a bit of "
     "the whole picture,\" and \"This is what William Burroughs discovered (but "
     "interprets differently).\" In the same section Dick traces his long-held view "
     "that the plasmate's messages were a \"contamination\" to \"(1) Burroughs' "
     "information virus theory; and (2) paranoia and paranoiac fear.\"",
     'strong'),

    ('SEV_BURROUGHS_inversion_1981',
     "In April 1981 Dick inverts the thesis: occlusion comes first, and the living "
     "information is the remedy sent to announce it, not the cause.",
     "\"Man is not occluded by an 'information virus,' i.e. living information; on the "
     "contrary: man is occluded and the living information is sent to tell him the true "
     "situation.\" Burroughs, Dick writes, correctly discerned both living information "
     "and an occlusion, then \"leaped to the pessimistic conclusion that there is a "
     "cause-and-effect relationship.\" The letter to Brig Elliot of April 15, 1981 makes "
     "the same argument to a correspondent one day earlier.",
     'strong'),

    ('SEV_BURROUGHS_letters_disagreement',
     "The correspondence states the disagreement more calmly and more completely than "
     "the notebooks do.",
     "To Brig Elliot (April 15, 1981): \"I cannot accept Burroughs' view that we have "
     "been invaded by an alien virus, an information virus, yet on the other hand I "
     "cannot readily dismiss this bizarre theory as mere paranoia on his part... he "
     "states the problem correctly, although perhaps his analysis of the cause is "
     "faulty.\" And: \"Where Burroughs and I sharply disagree is that my supposition is "
     "that if an information life form exists... it is benign.\" To Patricia Warrick "
     "(August 18, 1981): \"This life form has not invaded our universe (as William "
     "Burroughs supposes) but is the source of our universe, one level higher.\"",
     'strong'),

    ('SEV_BURROUGHS_style_and_trade',
     "Burroughs also figures for Dick as a literary model and as a name in the "
     "publishing economy, independent of the virus theory.",
     "In January 1976 Doubleday wanted Burroughs and Vonnegut to blurb A Scanner Darkly "
     "and left it to Dick to approach them; he had no way in and said so to both Bill "
     "Sarill and Sharon Jarvis. In February 1981 he twice described VALIS as a picaresque "
     "blended with elements from Hunter S. Thompson and Burroughs. In January 1981 he put "
     "Burroughs on a five-name reading list for a beginning writer.",
     'moderate'),

    ('SEV_BURROUGHS_cutup',
     "Dick takes the cut-up method as empirical evidence that narrative is latent in any "
     "text, and gives it a theological cause.",
     "\"This is why - as William Burroughs found - when any written text is cut up + "
     "rejoined at random, a narrative results.\" In the April 1981 sitting the cause is "
     "Hagia Sophia reading the Torah aloud: if the ground of the world is a text being "
     "narrated, any fragment of text is already inside the narration.",
     'moderate'),
]

EVIDENCE_PACKETS.append((
    'SEV_BURROUGHS_manichaean_1981',
    "The same sitting keeps a pessimistic Burroughs alive in Manichaean dress.",
    "Having just denied that living information occludes anyone, Dick writes that "
    "Satan \"ensnared him as the info virus of Burroughs, ensnared him with beauty,\" "
    "and that the living information \"controls us (as Burroughs teaches)\" while "
    "assuming the guise of a world — a position he calls a radical acosmism. The "
    "Manichaean frame lets him hold both readings by splitting the living information "
    "from the Christ that opposes it.",
    'moderate',
))

# Which evidence packet each passage belongs to, keyed by its anchor phrase.
# Anchors are unique across the specification lists above.
ANCHOR_TO_EV = {
    # Adoption, September 1976
    'the ticket that exploded" says of the Nova Mob parasites': 'SEV_BURROUGHS_adoption_1976',
    'Burroughs speaks of a virus - a word become a neural': 'SEV_BURROUGHS_adoption_1976',
    "the theory (Burroughs' included) that this world contains evil entities": 'SEV_BURROUGHS_adoption_1976',
    'Burroughs may have got the real situation down in "The Ticket That Exploded"': 'SEV_BURROUGHS_adoption_1976',
    "Equal to Burroughs' nova police": 'SEV_BURROUGHS_adoption_1976',
    'Burroughs is right about the Nova police': 'SEV_BURROUGHS_adoption_1976',
    "shades of Burroughs' nova Mob": 'SEV_BURROUGHS_adoption_1976',
    'This fits the "replicating virus" theory of Burroughs': 'SEV_BURROUGHS_adoption_1976',
    "This is very much like Burroughs' formulation": 'SEV_BURROUGHS_adoption_1976',

    # The anti-information modification, September 1976
    'The virus (of Burroughs) is an information (or word) virus': 'SEV_BURROUGHS_antiinformation_1976',
    'as burroughs points out, over 10 seconds of inner silence': 'SEV_BURROUGHS_antiinformation_1976',
    "This would explain Burroughs' results in obtaining living, latent messages": 'SEV_BURROUGHS_antiinformation_1976',
    'Burroughs posits an information virus': 'SEV_BURROUGHS_antiinformation_1976',

    # Qualified endorsement, October 1978
    'William Burroughs is correct.': 'SEV_BURROUGHS_qualified_1978',
    'Burroughs is right but he has only a bit of the whole picture': 'SEV_BURROUGHS_qualified_1978',
    'information virus theory': 'SEV_BURROUGHS_qualified_1978',
    'This is what William Burroughs discovered (but interprets differently)': 'SEV_BURROUGHS_qualified_1978',
    'related to william Burroughs latent messages + info virus': 'SEV_BURROUGHS_qualified_1978',

    # The inversion, April 1981
    'Burroughs, too, in his own way is right': 'SEV_BURROUGHS_inversion_1981',
    'Man is not occluded by an "information virus,"': 'SEV_BURROUGHS_inversion_1981',
    'Someone in reading "Valis" will see the correlation to Burroughs': 'SEV_BURROUGHS_inversion_1981',
    'Burroughs never guessed this': 'SEV_BURROUGHS_inversion_1981',
    'This very slightly resembles Burroughs, but is much more radical': 'SEV_BURROUGHS_inversion_1981',

    # The Manichaean relapse, April 1981
    'he ensnared him as the info virus of Burroughs': 'SEV_BURROUGHS_manichaean_1981',
    'it controls us (as Burroughs teaches)': 'SEV_BURROUGHS_manichaean_1981',

    # Cut-ups and latent narrative
    'as William Burroughs found- when any written text is cut up': 'SEV_BURROUGHS_cutup',
    "william Burroughs' latent message stuff": 'SEV_BURROUGHS_cutup',

    # The disagreement, stated in the correspondence
    'I am familiar with his theory of an information virus': 'SEV_BURROUGHS_letters_disagreement',
    'I cannot accept Burroughs’ view that we have been invaded by an alien virus': 'SEV_BURROUGHS_letters_disagreement',
    'Where Burroughs and I sharply disagree': 'SEV_BURROUGHS_letters_disagreement',
    'This life form has not invaded our universe (as William Burroughs supposes)': 'SEV_BURROUGHS_letters_disagreement',
    'a far cry from Burroughs’ notion that we have been invaded by an information virus': 'SEV_BURROUGHS_letters_disagreement',

    # Burroughs as model and as a name in the trade
    'They want people like William Burroughs, Kurt Vonnegut': 'SEV_BURROUGHS_style_and_trade',
    '“In many ways, Phil Dick is to psychedelics and science fiction what William Burroughs': 'SEV_BURROUGHS_style_and_trade',
    'The material on William Burroughs—the article and then the interview': 'SEV_BURROUGHS_style_and_trade',
    'Faulkner, Hemingway, Hunter S. Thompson, William Burroughs': 'SEV_BURROUGHS_style_and_trade',
    'associ­ ated with Hunter S. Thompson and William S. Burroughs': 'SEV_BURROUGHS_style_and_trade',
    'It is a picaresque novel blended with new elements derived from William Burroughs': 'SEV_BURROUGHS_style_and_trade',
    'Burroughs\' "Junky" will': 'SEV_BURROUGHS_style_and_trade',
}

# (summary, explanation, type, anchor_a, anchor_b)
CONTRADICTIONS = [
    ("In 1976 Dick reports throwing off a word virus that had infected him; in 1981 he "
     "denies that any information virus occludes anyone.",
     "This is the topic's central reversal, and it is a genuine change of position rather "
     "than a change of emphasis. The 1976 entry treats 3-74 as remission from an infection "
     "Burroughs correctly diagnosed. The 1981 entry keeps the two components — living "
     "information, and occlusion — but severs the causal link between them and reassigns "
     "the living information to the side of the remedy. Both readings remain in the "
     "notebooks; neither is retracted.",
     'early_vs_late',
     'Burroughs may have got the real situation down in "The Ticket That Exploded"',
     'Man is not occluded by an "information virus,"'),

    ("The same April 1981 sitting that rejects Burroughs's causal claim also endorses it "
     "in Manichaean form.",
     "Within days — within pages — of writing that living information is sent to inform "
     "rather than to occlude, Dick writes that Satan \"ensnared him as the info virus of "
     "Burroughs, ensnared him with beauty\" and that the living information \"controls us "
     "(as Burroughs teaches).\" The Manichaean frame lets him keep the pessimistic reading "
     "and the optimistic one at once by splitting the living information from the Christ "
     "that opposes it. The tension is not resolved anywhere in the corpus.",
     'interpretive',
     'Man is not occluded by an "information virus,"',
     'he ensnared him as the info virus of Burroughs'),

    ("To a correspondent Dick refuses to call Burroughs's theory paranoia; to himself he "
     "had already named paranoia as one of its two sources.",
     "The 1978 Exegesis entry attributes his own \"contamination\" reading to Burroughs's "
     "theory plus \"paranoia and paranoiac fear.\" The 1981 letter to Brig Elliot declines "
     "to dismiss the same theory \"as mere paranoia on his part.\" The two statements are "
     "compatible on a strict reading — one is about Dick, one about Burroughs — but they "
     "show the difference between what the notebooks say and what the letters concede.",
     'self_vs_critic',
     'information virus theory',
     'I cannot accept Burroughs’ view that we have been invaded by an alien virus'),
]

# relation_type is an enum: 'primary' | 'related' | 'contrasts' | 'subsumes'
RELATED_TERM_IDS = [
    ('TERM_burroughs', 'primary'),
    ('TERM_living-information', 'related'),
    ('TERM_plasmate', 'related'),
    ('TERM_black-iron-prison', 'related'),
    ('TERM_king-felix', 'related'),
    ('TERM_logos', 'related'),
    ('TERM_valis', 'related'),
    ('TERM_ubik', 'related'),
    ('TERM_scanner', 'related'),
    ('TERM_maze', 'related'),
]

RELATED_NAME_IDS = [
    ('NAME_thomas', 'identified_with_nova_mob_parasite'),
    ('NAME_firebright', 'identified_with_deposited_egg'),
    ('NAME_zebra', 'identified_with_nova_police'),
    ('NAME_valis', 'living_information'),
]

# relevance is an enum: 'primary' | 'substantial' | 'mentions'
RELATED_DOC_IDS = [
    ('DOC_EXEG_SECTION_015', 'primary'),       # September 15, 1976 — adoption
    ('DOC_EXEG_SECTION_016', 'primary'),       # October 10, 1978 — qualified
    ('DOC_EXEG_SECTION_017', 'primary'),       # April 16, 1981 — the inversion
    ('DOC_ARCH_THE_SELECTED_LETTERS_OF_PHILIP_K_DICK_19', 'primary'),   # 1980-1982
    ('DOC_ARCH_OCEANOFPDF_COM_SELECTED_LETTERS_OF_PHILI', 'mentions'),  # 1975-1976
    ('DOC_ARCH_PHILIP_K_DICK_PAUL_WILLIAMS_SELECTED_LET', 'mentions'),  # 1977-1979
]

TERM_BURROUGHS = {
    'canonical_name': 'Burroughs',
    'primary_category': 'Intertext',
    'card_description': (
        "William S. Burroughs, whose \"word virus\" Dick adopted in 1976, qualified in "
        "1978, and inverted in 1981."
    ),
    'definition': (
        "William S. Burroughs (1914–1997), read by Dick from September 1976 onward and "
        "named in twenty-two Exegesis segments and nine letters. What Dick takes from him "
        "is a single proposition — that language is a parasitic organism, a \"word virus,\" "
        "which infects its hosts and blinds them to their own condition — together with "
        "its narrative furniture from The Ticket That Exploded: the Nova Mob, the Nova "
        "police, and the latent message riding inside ordinary text."
    ),
    'interpretive_note': (
        "Dick's use of Burroughs moves in one direction over five years. In September 1976 "
        "the word virus is confirmation: Thomas is a Nova Mob parasite, the power that "
        "intervened in 3-74 is \"Equal to Burroughs' nova police,\" and 3-74 itself was a "
        "remission in which he \"threw off the word virus.\" In October 1978 the endorsement "
        "narrows — \"Burroughs is right but he has only a bit of the whole picture\" — and "
        "Dick names Burroughs's theory, together with his own \"paranoia and paranoiac fear,\" "
        "as the source of his long-held suspicion that the plasmate's messages were a "
        "contamination. In April 1981 he inverts it: man is already occluded, and the living "
        "information is what is sent to tell him so. Burroughs, on this reading, saw both "
        "halves correctly and connected them the wrong way round."
    ),
    'scholarly_caution': (
        "Dick had not read Burroughs when he wrote the novels most often compared to him. "
        "He says so himself in the April 15, 1981 letter to Brig Elliot: the occlusion he "
        "put into A Scanner Darkly was observed in 1971, \"before I knew of Burroughs.\" "
        "The Exegesis reads Ubik, The Three Stigmata of Palmer Eldritch and A Maze of Death "
        "through Burroughs retroactively. The one influence Dick claims prospectively is "
        "stylistic, on VALIS, alongside Hunter S. Thompson."
    ),
    'see_also': ['Living Information', 'Plasmate', 'Black Iron Prison', 'King Felix',
                 'Logos', 'Valis'],
}


# --------------------------------------------------------------------------
# Schema migration
#
# study_passages was written when the studies pipeline only produced fiction,
# Exegesis and scholarship passages, so its lane CHECK stops at 'C'. The
# corpus itself has used lanes D (biography) and E (letters/interviews) on
# documents from the start, and this topic's strongest evidence is in lane E.
# Widen the constraint rather than collapsing letters into another lane, and
# take the opportunity to add the ev_id link that lets an evidence packet own
# its own passages instead of borrowing the whole topic's.
# --------------------------------------------------------------------------

STUDY_PASSAGES_DDL = """
CREATE TABLE study_passages_new (
    passage_id          INTEGER PRIMARY KEY AUTOINCREMENT,
    topic_id            TEXT NOT NULL,
    ev_id               TEXT,

    doc_id              TEXT,
    seg_id              TEXT,
    page_num            INTEGER,
    char_offset_start   INTEGER,
    char_offset_end     INTEGER,

    passage_text        TEXT NOT NULL,
    context_before      TEXT,
    context_after       TEXT,

    lane                TEXT CHECK (lane IN ('A', 'B', 'C', 'D', 'E')),

    source_mode         TEXT CHECK (source_mode IN (
                            'fiction', 'exegesis', 'letter', 'interview', 'criticism'
                        )),
    claim_type          TEXT CHECK (claim_type IN (
                            'definition', 'symptom_description', 'causal_theory',
                            'allegory', 'self_report', 'critique', 'comparison',
                            'unresolved'
                        )),
    confidence          TEXT CHECK (confidence IN ('high', 'medium', 'low')),

    psych_mode          TEXT,
    ai_mode             TEXT,

    matched_terms       TEXT,
    match_method        TEXT CHECK (match_method IN (
                            'lexicon_exact', 'lexicon_alias', 'claude_conceptual',
                            'claude_inferred', 'curated_anchor'
                        )),

    fair_use_status     TEXT DEFAULT 'pending' CHECK (fair_use_status IN (
                            'pending', 'approved', 'trimmed', 'rejected'
                        )),
    editorial_status    TEXT DEFAULT 'unreviewed',

    notes               TEXT,
    created_at          TEXT DEFAULT (datetime('now')),

    FOREIGN KEY (topic_id) REFERENCES study_topics(topic_id),
    FOREIGN KEY (doc_id) REFERENCES documents(doc_id),
    FOREIGN KEY (seg_id) REFERENCES segments(seg_id)
);
"""

STUDY_PASSAGES_INDEXES = [
    "CREATE INDEX IF NOT EXISTS idx_study_passages_topic ON study_passages(topic_id)",
    "CREATE INDEX IF NOT EXISTS idx_study_passages_doc ON study_passages(doc_id)",
    "CREATE INDEX IF NOT EXISTS idx_study_passages_seg ON study_passages(seg_id)",
    "CREATE INDEX IF NOT EXISTS idx_study_passages_lane ON study_passages(lane)",
    "CREATE INDEX IF NOT EXISTS idx_study_passages_claim ON study_passages(claim_type)",
    "CREATE INDEX IF NOT EXISTS idx_study_passages_ev ON study_passages(ev_id)",
]

CARRIED_COLUMNS = [
    'passage_id', 'topic_id', 'doc_id', 'seg_id', 'page_num',
    'char_offset_start', 'char_offset_end', 'passage_text', 'context_before',
    'context_after', 'lane', 'source_mode', 'claim_type', 'confidence',
    'psych_mode', 'ai_mode', 'matched_terms', 'match_method',
    'fair_use_status', 'editorial_status', 'notes', 'created_at',
]


def ensure_schema(db: sqlite3.Connection) -> bool:
    """Widen study_passages if it still carries the A/B/C-only definition."""
    ddl = db.execute(
        "SELECT sql FROM sqlite_master WHERE type='table' AND name='study_passages'"
    ).fetchone()
    if not ddl:
        raise SystemExit("study_passages table is missing; run the build first.")
    if "'D', 'E'" in ddl[0] and 'ev_id' in ddl[0]:
        return False

    # Views over study_passages block the rename; drop and restore them.
    views = db.execute(
        "SELECT name, sql FROM sqlite_master "
        "WHERE type='view' AND sql LIKE '%study_passages%'").fetchall()

    cols = ', '.join(CARRIED_COLUMNS)
    db.execute("PRAGMA foreign_keys = OFF")
    db.execute("DROP TABLE IF EXISTS study_passages_new")
    for name, _ in views:
        db.execute(f"DROP VIEW {name}")
    db.execute(STUDY_PASSAGES_DDL)
    db.execute(f"INSERT INTO study_passages_new ({cols}) "
               f"SELECT {cols} FROM study_passages")
    db.execute("DROP TABLE study_passages")
    db.execute("ALTER TABLE study_passages_new RENAME TO study_passages")
    for stmt in STUDY_PASSAGES_INDEXES:
        db.execute(stmt)
    for _, sql in views:
        db.execute(sql)
    db.commit()
    db.execute("PRAGMA foreign_keys = ON")
    n = db.execute("SELECT COUNT(*) FROM study_passages").fetchone()[0]
    print(f"  migrated study_passages: lanes A-E, ev_id added ({n} rows preserved)")
    return True


# --------------------------------------------------------------------------
# Extraction helpers
# --------------------------------------------------------------------------

SENTENCE_BREAK = re.compile(r'(?<=[.?!])\s+')

# The Selected Letters scans carry a running head that OCR renders with the
# letters spaced apart ("T HE S E L E C T E D L E T T E R S OF P H I L I P K.
# D I C K"), sometimes with the page number attached. It lands in the middle of
# excerpts and reads as garbage, so strip it from letter-lane text.
_HEAD_WORDS = ['THE', 'SELECTED', 'LETTERS', 'OF', 'PHILIP', 'K', 'DICK']
RUNNING_HEAD = re.compile(
    r'\s*\d{0,4}\s*' +
    r'\s*'.join(r'\s*'.join(ch for ch in word) + r'\.?' for word in _HEAD_WORDS) +
    r'\.?\s*\d{0,4}\s*',
    re.IGNORECASE)


# A window can also clip the running head in half, leaving a run of spaced
# single capitals at one edge; and body_md keeps "##" section markers.
EDGE_SPACED_CAPS = re.compile(
    r'^(?:\s*\d{1,4}\s+)?(?:[A-Z]{1,2}\.?\s+){3,}[A-Z]{1,2}\.?\s*|'
    r'\s*\d{1,4}\s+(?:[A-Z]{1,2}\.?\s+){2,}[A-Z]{1,2}\.?\s*$')


def strip_running_headers(text: str) -> str:
    text = RUNNING_HEAD.sub(' ', text)
    text = EDGE_SPACED_CAPS.sub(' ', text)
    text = re.sub(r'(^\s*##\s*|\s*##\s*$)', ' ', text)
    return text


def window(text: str, anchor: str, before: int, after: int, clean=None):
    """Return (excerpt, start, end, context_before, context_after) or None.

    The raw window is snapped outward-in to whole words, and to a sentence
    boundary at the head where one falls inside the leading context, so the
    excerpt does not begin or end mid-word.
    """
    idx = text.find(anchor)
    if idx < 0:
        return None
    start = max(0, idx - before)
    end = min(len(text), idx + len(anchor) + after)

    # Snap the head forward to a sentence break inside the leading context,
    # else to the next word boundary.
    head = text[start:idx]
    breaks = list(SENTENCE_BREAK.finditer(head))
    if breaks:
        start += breaks[0].end()
    elif start > 0:
        space = text.find(' ', start)
        if 0 <= space < idx:
            start = space + 1

    # Snap the tail back to a word boundary.
    if end < len(text) and not text[end].isspace():
        space = text.rfind(' ', idx + len(anchor), end)
        if space > 0:
            end = space

    excerpt = text[start:end]
    if clean:
        excerpt = clean(excerpt)
    excerpt = re.sub(r'\s+', ' ', excerpt).strip()
    if start > 0:
        excerpt = '… ' + excerpt
    if end < len(text):
        excerpt = excerpt.rstrip() + ' …'

    ctx_b = re.sub(r'\s+', ' ', text[max(0, start - 150):start]).strip()
    ctx_a = re.sub(r'\s+', ' ', text[end:end + 150]).strip()
    return excerpt, start, end, ctx_b, ctx_a


def collect_passages(db):
    """Build the full passage row set from the live corpus."""
    rows, missing = [], []

    seg_text = {
        s: (t or '') for s, t in db.execute(
            "SELECT seg_id, raw_text FROM segments WHERE raw_text IS NOT NULL")
    }
    seg_doc = {s: d for s, d in db.execute("SELECT seg_id, doc_id FROM segments")}

    for seg_id, anchor, before, after, ctype, conf, cite, terms in EXEGESIS_PASSAGES:
        w = window(seg_text.get(seg_id, ''), anchor, before, after)
        if not w:
            missing.append(('segment', seg_id, anchor))
            continue
        excerpt, start, end, cb, ca = w
        rows.append((TOPIC_ID, ANCHOR_TO_EV.get(anchor), seg_doc.get(seg_id), seg_id,
                     None, start, end, excerpt, cb, ca, 'B', 'exegesis', ctype, conf,
                     None, None, json.dumps(terms), 'curated_anchor',
                     'approved', 'curated', cite))

    for letter_id, anchor, before, after, ctype, conf, cite, terms in LETTER_PASSAGES:
        row = db.execute(
            "SELECT volume_doc_id, body_md FROM letters WHERE letter_id = ?",
            (letter_id,)).fetchone()
        if not row:
            missing.append(('letter', letter_id, anchor))
            continue
        w = window(row[1] or '', anchor, before, after,
                   clean=strip_running_headers)
        if not w:
            missing.append(('letter', letter_id, anchor))
            continue
        excerpt, start, end, cb, ca = w
        rows.append((TOPIC_ID, ANCHOR_TO_EV.get(anchor), row[0], None,
                     None, start, end, excerpt, cb, ca, 'E', 'letter', ctype, conf,
                     None, None, json.dumps(terms), 'curated_anchor',
                     'approved', 'curated', cite))

    for doc_id, anchor, before, after, ctype, conf, cite, terms in SCHOLARSHIP_PASSAGES:
        row = db.execute(
            "SELECT text_content FROM document_texts WHERE doc_id = ?",
            (doc_id,)).fetchone()
        if not row:
            missing.append(('document', doc_id, anchor))
            continue
        w = window(row[0] or '', anchor, before, after)
        if not w:
            missing.append(('document', doc_id, anchor))
            continue
        excerpt, start, end, cb, ca = w
        rows.append((TOPIC_ID, ANCHOR_TO_EV.get(anchor), doc_id, None,
                     None, start, end, excerpt, cb, ca, 'C', 'criticism', ctype, conf,
                     None, None, json.dumps(terms), 'curated_anchor',
                     'approved', 'curated', cite))

    return rows, missing


# --------------------------------------------------------------------------
# Seeding
# --------------------------------------------------------------------------

def seed(db: sqlite3.Connection):
    ensure_schema(db)
    passages, missing = collect_passages(db)

    unassigned = [p for p in passages if p[1] is None]
    if unassigned:
        print("  ERROR: passages with no evidence packet:")
        for p in unassigned:
            print(f"    {p[3] or p[2]}: {p[7][:70]}")
        raise SystemExit(1)
    if missing:
        print("  ERROR: anchors not found in the corpus:")
        for kind, sid, anchor in missing:
            print(f"    {kind} {sid}: {anchor!r}")
        raise SystemExit(1)

    # ---- study ------------------------------------------------------------
    db.execute("""
        INSERT INTO studies (study_id, study_label, study_description, topic_count)
        VALUES (?, ?, ?, 1)
        ON CONFLICT(study_id) DO UPDATE SET
            study_label = excluded.study_label,
            study_description = excluded.study_description,
            updated_at = CURRENT_TIMESTAMP
    """, (STUDY_ID, STUDY_LABEL, STUDY_DESCRIPTION))

    # ---- clear derived rows for idempotency --------------------------------
    db.execute("DELETE FROM study_contradictions WHERE topic_id = ?", (TOPIC_ID,))
    db.execute("DELETE FROM study_passages WHERE topic_id = ?", (TOPIC_ID,))
    db.execute("DELETE FROM study_evidence_packets WHERE topic_id = ?", (TOPIC_ID,))
    db.execute("DELETE FROM study_topic_docs WHERE topic_id = ?", (TOPIC_ID,))
    db.execute("DELETE FROM study_topic_terms WHERE topic_id = ?", (TOPIC_ID,))
    db.execute("DELETE FROM study_topic_names WHERE topic_id = ?", (TOPIC_ID,))

    # ---- topic stub, so the passage/evidence foreign keys resolve ----------
    db.execute("""
        INSERT OR IGNORE INTO study_topics (topic_id, study_id, canonical_name, slug)
        VALUES (?, ?, ?, ?)
    """, (TOPIC_ID, STUDY_ID, TOPIC_NAME, TOPIC_SLUG))

    # ---- passages ---------------------------------------------------------
    db.executemany("""
        INSERT INTO study_passages
            (topic_id, ev_id, doc_id, seg_id, page_num, char_offset_start,
             char_offset_end, passage_text, context_before, context_after, lane,
             source_mode, claim_type, confidence, psych_mode, ai_mode,
             matched_terms, match_method, fair_use_status, editorial_status, notes)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, passages)

    lane_counts = {}
    per_packet = {}
    for p in passages:
        lane_counts[p[10]] = lane_counts.get(p[10], 0) + 1
        per_packet.setdefault(p[1], {})
        per_packet[p[1]][p[10]] = per_packet[p[1]].get(p[10], 0) + 1

    # ---- evidence packets --------------------------------------------------
    for ev_id, claim_text, summary, conf in EVIDENCE_PACKETS:
        db.execute("""
            INSERT INTO study_evidence_packets
                (ev_id, topic_id, claim_text, evidence_summary, confidence,
                 source_method, editorial_status, lane_a_count, lane_b_count,
                 lane_c_count, notes)
            VALUES (?,?,?,?,?,?,?,?,?,?,?)
        """, (ev_id, TOPIC_ID, claim_text, summary, conf, 'editorial',
              'reviewed', per_packet.get(ev_id, {}).get('A', 0),
              per_packet.get(ev_id, {}).get('B', 0),
              per_packet.get(ev_id, {}).get('C', 0), GENERATOR))

    # ---- contradictions ----------------------------------------------------
    def passage_id_for(anchor):
        row = db.execute("""
            SELECT passage_id FROM study_passages
            WHERE topic_id = ? AND passage_text LIKE ?
            ORDER BY passage_id LIMIT 1
        """, (TOPIC_ID, f'%{anchor}%')).fetchone()
        return row[0] if row else None

    n_contra = 0
    for summary, explanation, ctype, anchor_a, anchor_b in CONTRADICTIONS:
        pa, pb = passage_id_for(anchor_a), passage_id_for(anchor_b)
        if pa is None or pb is None:
            print(f"  WARNING: contradiction skipped, passage not found: {summary[:60]}")
            continue
        db.execute("""
            INSERT INTO study_contradictions
                (topic_id, passage_id_a, passage_id_b, summary, explanation,
                 contradiction_type, notes)
            VALUES (?,?,?,?,?,?,?)
        """, (TOPIC_ID, pa, pb, summary, explanation, ctype, GENERATOR))
        n_contra += 1

    # ---- topic -------------------------------------------------------------
    db.execute("""
        INSERT INTO study_topics
            (topic_id, study_id, canonical_name, slug, status, priority,
             definition, pkd_relevance, in_the_fiction, in_the_exegesis,
             intellectual_background, scholarly_debate, chronology_summary,
             contradictions_summary, related_thinkers, editorial_notes,
             open_questions, card_description, passage_count, evidence_count,
             contradiction_count, first_appearance, peak_period_start,
             peak_period_end, related_topics, provenance, notes)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        ON CONFLICT(topic_id) DO UPDATE SET
            study_id = excluded.study_id,
            canonical_name = excluded.canonical_name,
            slug = excluded.slug,
            status = excluded.status,
            priority = excluded.priority,
            definition = excluded.definition,
            pkd_relevance = excluded.pkd_relevance,
            in_the_fiction = excluded.in_the_fiction,
            in_the_exegesis = excluded.in_the_exegesis,
            intellectual_background = excluded.intellectual_background,
            scholarly_debate = excluded.scholarly_debate,
            chronology_summary = excluded.chronology_summary,
            contradictions_summary = excluded.contradictions_summary,
            related_thinkers = excluded.related_thinkers,
            editorial_notes = excluded.editorial_notes,
            open_questions = excluded.open_questions,
            card_description = excluded.card_description,
            passage_count = excluded.passage_count,
            evidence_count = excluded.evidence_count,
            contradiction_count = excluded.contradiction_count,
            first_appearance = excluded.first_appearance,
            peak_period_start = excluded.peak_period_start,
            peak_period_end = excluded.peak_period_end,
            related_topics = excluded.related_topics,
            provenance = excluded.provenance,
            updated_at = CURRENT_TIMESTAMP
    """, (
        TOPIC_ID, STUDY_ID, TOPIC_NAME, TOPIC_SLUG, 'reviewed', 10,
        DOSSIER['definition'], DOSSIER['pkd_relevance'], DOSSIER['in_the_fiction'],
        DOSSIER['in_the_exegesis'], DOSSIER['intellectual_background'],
        DOSSIER['scholarly_debate'], DOSSIER['chronology_summary'],
        DOSSIER['contradictions_summary'], json.dumps(RELATED_THINKERS),
        DOSSIER['editorial_notes'], json.dumps(OPEN_QUESTIONS),
        "Burroughs's word virus, adopted by Dick in 1976, qualified in 1978, and "
        "inverted in 1981 — tracked across 22 Exegesis segments and 9 letters.",
        len(passages), len(EVIDENCE_PACKETS), n_contra,
        '1976', '1976', '1981', json.dumps([]),
        PROVENANCE, GENERATOR,
    ))

    for field in DOSSIER:
        db.execute(
            f"UPDATE study_topics SET {field}_generator = ?, {field}_claim_ids = ? "
            f"WHERE topic_id = ?", (GENERATOR, json.dumps([]), TOPIC_ID))

    # ---- links -------------------------------------------------------------
    for doc_id, relevance in RELATED_DOC_IDS:
        n = db.execute(
            "SELECT COUNT(*) FROM study_passages WHERE topic_id = ? AND doc_id = ?",
            (TOPIC_ID, doc_id)).fetchone()[0]
        db.execute("""
            INSERT OR REPLACE INTO study_topic_docs
                (topic_id, doc_id, relevance, passage_count)
            VALUES (?,?,?,?)
        """, (TOPIC_ID, doc_id, relevance, n))

    for term_id, rel in RELATED_TERM_IDS:
        if db.execute("SELECT 1 FROM terms WHERE term_id = ?", (term_id,)).fetchone():
            db.execute("INSERT OR REPLACE INTO study_topic_terms "
                       "(topic_id, term_id, relation_type) VALUES (?,?,?)",
                       (TOPIC_ID, term_id, rel))

    for name_id, rel in RELATED_NAME_IDS:
        if db.execute("SELECT 1 FROM names WHERE name_id = ?", (name_id,)).fetchone():
            db.execute("INSERT OR REPLACE INTO study_topic_names "
                       "(topic_id, name_id, relation_type) VALUES (?,?,?)",
                       (TOPIC_ID, name_id, rel))

    db.execute("UPDATE studies SET topic_count = "
               "(SELECT COUNT(*) FROM study_topics WHERE study_id = ?) "
               "WHERE study_id = ?", (STUDY_ID, STUDY_ID))

    # ---- dictionary term ---------------------------------------------------
    t = TERM_BURROUGHS
    db.execute("""
        UPDATE terms SET
            canonical_name = ?, status = 'accepted', review_state = 'human-revised',
            primary_category = ?, card_description = ?, definition = ?,
            interpretive_note = ?, visionary_significance = NULL,
            scholarly_caution = ?, full_description = ?, see_also = ?,
            first_appearance = '1976', peak_usage_start = '1976',
            peak_usage_end = '1981', provenance = ?, noise_score = 0.0,
            mention_count = (SELECT COUNT(*) FROM term_segments
                             WHERE term_id = 'TERM_burroughs'),
            definition_generator = ?, interpretive_note_generator = ?,
            scholarly_caution_generator = ?, card_description_generator = ?,
            full_description_generator = ?,
            definition_claim_ids = '[]', interpretive_note_claim_ids = '[]',
            scholarly_caution_claim_ids = '[]', card_description_claim_ids = '[]',
            full_description_claim_ids = '[]',
            visionary_significance_claim_ids = '[]',
            updated_at = CURRENT_TIMESTAMP
        WHERE term_id = 'TERM_burroughs'
    """, (t['canonical_name'], t['primary_category'], t['card_description'],
          t['definition'], t['interpretive_note'], t['scholarly_caution'],
          t['definition'], json.dumps(t['see_also']), PROVENANCE,
          GENERATOR, GENERATOR, GENERATOR, GENERATOR, GENERATOR))

    # "Word virus" and "information virus" are Dick's names for the concept this
    # entry is about, so searches for them should land here rather than nowhere.
    for alias in ('William S. Burroughs', 'William Burroughs',
                  'word virus', 'information virus'):
        db.execute("INSERT OR IGNORE INTO term_aliases (term_id, alias_text, alias_type) "
                   "VALUES ('TERM_burroughs', ?, 'alternate_name')", (alias,))

    db.commit()

    print(f"  study            {STUDY_ID}")
    print(f"  topic            {TOPIC_ID} ({TOPIC_SLUG})")
    print(f"  passages         {len(passages)}  lanes={lane_counts}")
    print(f"  evidence packets {len(EVIDENCE_PACKETS)}")
    print(f"  contradictions   {n_contra}")
    print(f"  related docs     {len(RELATED_DOC_IDS)}")
    print("  TERM_burroughs   promoted to accepted / human-revised")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--db', type=Path, default=DEFAULT_DB)
    args = ap.parse_args()

    if not args.db.exists():
        print(f"Database not found: {args.db}", file=sys.stderr)
        raise SystemExit(1)

    db = sqlite3.connect(str(args.db))
    db.execute("PRAGMA foreign_keys = ON")
    print("Seeding Burroughs / word virus topic...")
    seed(db)
    db.close()
    print("Done. Now run: python scripts/studies/export_studies.py")


if __name__ == '__main__':
    main()
