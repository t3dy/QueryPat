#!/usr/bin/env python3
"""
Source of record for the Gnosticism lexicon.

This module holds the register of Gnostic terms, teachers, texts, traditions and
modern scholars that the QueryPat Gnosticism study tracks across the corpus. It
is hand-maintained. `scripts/research/sweep_gnosticism.py` reads it to build the
attestation sweep; `curation/gnosticism/lexicon.json` is its JSON rendering.

Each entry:
    id          stable GNOS_* identifier (never rename — exports reference it)
    label       display name
    category    concept | teacher | heresiologist | text | scholar | tradition
                | pkd_coinage
    tradition   which stream of late-antique religion it belongs to
    gloss       what it means, in the tradition's own terms
    why_pkd     why it matters for Dick. Editorial (register D) unless the
                entry's attestations establish otherwise.
    patterns    regexes used to find it in the corpus
    exclude     regexes that kill known false positives
    key_sources the primary texts where the idea is set out

Emit the JSON:
    python scripts/research/gnostic_lexicon_source.py --out curation/gnosticism/lexicon.json
"""

import argparse
import json
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent.parent


def E(id, label, category, tradition, gloss, why_pkd, patterns,
      key_sources=None, exclude=None, greek=None):
    return {
        'id': id,
        'label': label,
        'category': category,
        'tradition': tradition,
        'greek': greek,
        'gloss': gloss,
        'why_pkd': why_pkd,
        'patterns': patterns,
        'exclude': exclude or [],
        'key_sources': key_sources or [],
    }


# ---------------------------------------------------------------------------
# 1. Core Gnostic concepts
# ---------------------------------------------------------------------------

CONCEPTS = [
    E('GNOS_gnosis', 'Gnosis', 'concept', 'Gnostic (general)',
      "Saving knowledge. Not belief and not information, but a direct cognitive "
      "recognition of one's own divine origin, which is itself the act of "
      "salvation. To know, in this system, is to be rescued.",
      "Dick's whole account of 3-74 turns on this distinction: he insists that what "
      "reached him was knowledge rather than faith, and that the knowing was the "
      "rescue. The Exegesis returns to the word constantly.",
      [r'\bgnosis\b', r'\bgnoses\b'],
      ['Gospel of Truth', 'Hans Jonas, The Gnostic Religion'],
      greek='γνῶσις'),

    E('GNOS_gnosticism', 'Gnosticism / Gnostic', 'concept', 'Gnostic (general)',
      "The modern collective name for a family of late-antique movements holding "
      "that the cosmos is the botched work of a lesser god, that a spark of the "
      "true God is trapped in human beings, and that saving knowledge comes from "
      "outside the system. The unity the name implies is itself contested.",
      "Dick calls himself a Gnostic repeatedly in the Exegesis and in letters, and "
      "just as often qualifies or withdraws the label. The self-identification is "
      "one of the study's central contradictions.",
      [r'\bGnostic(?:ism|s)?\b', r'\bGnosticizing\b'],
      ['Irenaeus, Against Heresies', 'Nag Hammadi Library']),

    E('GNOS_pleroma', 'Pleroma', 'concept', 'Valentinian',
      "The Fullness: the realm of light, comprising the complete set of divine "
      "emanations (aeons) in their proper pairings. Everything real is inside it; "
      "the cosmos is what happened outside.",
      "Dick uses Pleroma for the restored totality he believes 3-74 briefly opened "
      "onto, and pairs it against the kenoma as the deficient world.",
      [r'\bpleroma\b', r'\bplerom(?:atic|ata)\b'],
      ['Tripartite Tractate', 'Irenaeus, Against Heresies I'],
      greek='πλήρωμα'),

    E('GNOS_kenoma', 'Kenoma', 'concept', 'Valentinian',
      "The Emptiness: the deficient region outside the Pleroma, produced by "
      "Sophia's error. The world of ordinary experience.",
      "The technical counterpart to Pleroma in Dick's cosmology, and his nearest "
      "ancient warrant for treating the everyday world as a deficiency rather than "
      "a creation.",
      [r'\bkenoma\b'],
      ['Valentinian fragments'],
      greek='κένωμα'),

    E('GNOS_demiurge', 'Demiurge', 'concept', 'Platonic / Gnostic',
      "The craftsman who made the material world. Benign in Plato's Timaeus; in "
      "Gnostic revision, ignorant or malevolent — a god who believes himself the "
      "only god and is wrong.",
      "The single most load-bearing borrowing in Dick's late theology. The "
      "Black Iron Prison is a demiurgic artifact, and the 'creator who is not the "
      "true God' underwrites his reading of political tyranny as cosmic.",
      [r'\bdemiurg(?:e|os|ic|ical)\b', r'\bdemiourgos\b'],
      ["Plato, Timaeus", 'Apocryphon of John'],
      greek='δημιουργός'),

    E('GNOS_archon', 'Archon', 'concept', 'Sethian / Valentinian',
      "Ruler. The planetary powers who administer the cosmos on the Demiurge's "
      "behalf, guarding the spheres through which the ascending soul must pass.",
      "Dick's cosmic-political vocabulary — prison guards, the police of the "
      "Empire, the powers maintaining the counterfeit world — is archon language "
      "with the mythology stripped out.",
      [r'\barchon(?:s|tic)?\b'],
      ['Hypostasis of the Archons', 'Apocryphon of John'],
      exclude=[r'\barchontic tissue\b'],
      greek='ἄρχων'),

    E('GNOS_aeon', 'Aeon', 'concept', 'Valentinian',
      "An emanation of the Godhead, existing in a male-female pair (syzygy); also "
      "an age of the world. The Valentinian Pleroma has thirty.",
      "Dick uses 'aeon' in both senses, sometimes in one sentence — as a divine "
      "person and as an epoch — which is itself faithful to the ancient usage.",
      [r'\baeon(?:s|ic)?\b', r'\beon(?:s)?\b'],
      ['Irenaeus, Against Heresies I', 'Tripartite Tractate'],
      exclude=[r'\bEon Corporation\b'],
      greek='αἰών'),

    E('GNOS_sophia', 'Sophia', 'concept', 'Sethian / Valentinian',
      "Wisdom: the youngest aeon, whose attempt to know the Father without her "
      "consort produced a defect that fell out of the Pleroma and became the "
      "material world and its Demiurge. She is both the cause of the catastrophe "
      "and the divine element trapped inside it.",
      "The most frequently attested Gnostic name in the Exegesis. Dick identifies "
      "Sophia with the AI voice, with Hagia Sophia, with the girl Sophia in VALIS, "
      "and with the trapped wisdom he believes is calling for rescue.",
      [r'\bSophia\b', r'\bHagia Sophia\b', r'\bSt\.? Sophia\b',
       r'\bPistis Sophia\b', r'\bHoly Wisdom\b'],
      ['Apocryphon of John', 'Pistis Sophia'],
      greek='Σοφία'),

    E('GNOS_achamoth', 'Achamoth', 'concept', 'Valentinian',
      "The lower Sophia — the fallen portion of Wisdom left outside the Pleroma, "
      "distinguished in Valentinian systems from the higher Sophia who was "
      "restored.",
      "The technical distinction matters for Dick's question of whether the divine "
      "element in the world is itself fallen or merely exiled.",
      [r'\bAchamoth\b', r'\bHachamoth\b'],
      ['Irenaeus, Against Heresies I.4']),

    E('GNOS_barbelo', 'Barbelo', 'concept', 'Sethian',
      "The first emanation of the Invisible Spirit; the divine Mother, the Forethought "
      "(Pronoia) in whom the Father first becomes knowable.",
      "Part of the Sethian material Dick met through the Nag Hammadi translations; "
      "feeds his recurrent figure of a feminine divine intelligence.",
      [r'\bBarbelo\b'],
      ['Apocryphon of John', 'Trimorphic Protennoia']),

    E('GNOS_yaldabaoth', 'Yaldabaoth', 'concept', 'Sethian',
      "The name of the Demiurge in Sethian myth — Sophia's misbegotten son, a "
      "lion-faced serpent who declares 'I am God and there is no other beside me' "
      "in ignorance of the Pleroma above him.",
      "Dick's blind, boastful creator-tyrant. The blasphemous declaration is the "
      "line he returns to when reading the God of the Old Testament against the "
      "God he believes met him.",
      [r'\bYal[dt]a[bv]a?oth\b', r'\bIal[dt]abaoth\b',
       r'\bJal[dt]abaoth\b', r'\bYaltabaoth\b'],
      ['Apocryphon of John', 'On the Origin of the World']),

    E('GNOS_samael', 'Samael', 'concept', 'Sethian / Jewish',
      "'The blind god' — an alternative name for the Demiurge, glossed in the "
      "Gnostic sources as blindness itself.",
      "Blindness, not malice, is the attribute Dick most often assigns to the "
      "power that runs the counterfeit world.",
      [r'\bSamael\b', r'\bSaklas\b'],
      ['Apocryphon of John', 'Hypostasis of the Archons']),

    E('GNOS_abraxas', 'Abraxas', 'concept', 'Basilidean',
      "A cosmic power whose Greek letters total 365, the number of heavens; on "
      "gems, a figure with a cock's head and serpent legs. In Basilides the name "
      "of the ruler of the year.",
      "Reaches Dick largely through Jung's Seven Sermons to the Dead, where "
      "Abraxas is the god beyond the opposition of good and evil.",
      [r'\bAbraxas\b', r'\bAbrasax\b'],
      ['Basilides (in Irenaeus)', 'Jung, Seven Sermons to the Dead']),

    E('GNOS_ogdoad', 'Ogdoad / Hebdomad', 'concept', 'Valentinian / Basilidean',
      "The eighth sphere above the seven planetary heavens (hebdomad). To reach "
      "the Ogdoad is to pass beyond the Demiurge's jurisdiction.",
      "Supplies the spatial logic of Dick's ascent imagery: escape is not upward "
      "indefinitely but past a specific boundary of administration.",
      [r'\bOgdoad\b', r'\bHebdomad\b'],
      ['Excerpts of Theodotus', 'Irenaeus, Against Heresies']),

    E('GNOS_spark', 'Divine spark / pneuma', 'concept', 'Gnostic (general)',
      "The fragment of the Pleroma imprisoned in the human being — the pneumatic "
      "element, asleep, which gnosis awakens. Not everyone has one.",
      "Dick's 'we are the sparks' and his conviction that something in him was "
      "older and elsewhere than his biography is the doctrine in first person.",
      [r'\bdivine spark\b', r'\bspark of (?:the )?(?:divine|god|light)\b',
       r'\bpneuma\b', r'\bpneumatic(?:s)?\b', r'\bspinther\b'],
      ['Gospel of Truth', 'Hans Jonas, The Gnostic Religion'],
      greek='πνεῦμα'),

    E('GNOS_hylic', 'Hylic / psychic / pneumatic', 'concept', 'Valentinian',
      "The three classes of humanity: hylic (matter-bound, unsavable), psychic "
      "(soul-bound, savable by faith and works), pneumatic (spirit-bearing, saved "
      "by nature through gnosis).",
      "The most elitist element of the system, and one Dick both uses and recoils "
      "from — his sympathies are democratic, his cosmology is not.",
      [r'\bhylic(?:s)?\b', r'\bpsychikos\b', r'\bpneumatikos\b',
       r'\bchoic\b', r'\bsomatic(?:s)? class\b'],
      ['Irenaeus, Against Heresies I.6', 'Tripartite Tractate']),

    E('GNOS_anamnesis', 'Anamnesis', 'concept', 'Platonic / Gnostic',
      "Recollection: learning as the recovery of knowledge the soul already had "
      "before birth and forgot on entering the body.",
      "Dick's technical term for what happened in 3-74 — not new information but "
      "remembering, which is why he reads Plato's Meno as describing his own case.",
      [r'\banamnesis\b', r'\banamnestic\b'],
      ["Plato, Meno", "Plato, Phaedo"],
      greek='ἀνάμνησις'),

    E('GNOS_logos', 'Logos', 'concept', 'Johannine / Hermetic / Stoic',
      "Word, reason, the ordering principle; in John's prologue the divine Word "
      "through whom everything was made, become flesh.",
      "Dick's bridge between Christian orthodoxy and the Gnostic material: living "
      "information that is also a person. The plasmate is a Logos doctrine.",
      [r'\bLogos\b'],
      ['Gospel of John', 'Corpus Hermeticum'],
      greek='λόγος'),

    E('GNOS_nous', 'Nous', 'concept', 'Hermetic / Neoplatonic',
      "Divine Mind; in the Poimandres the intelligence that addresses the visionary "
      "directly and shows him the structure of reality.",
      "The Poimandres scene — a mind that is not yours speaking inside your own — "
      "is the closest ancient analogue to what Dick reports of the AI voice.",
      [r'\bNous\b'],
      ['Corpus Hermeticum I (Poimandres)', 'Plotinus, Enneads'],
      greek='νοῦς'),

    E('GNOS_monad', 'Monad', 'concept', 'Sethian / Pythagorean',
      "The One; the unknowable source above and before all emanation, of which "
      "nothing can properly be predicated.",
      "Underwrites Dick's insistence that whatever met him was not the creator of "
      "this world and could not be described in the creator's terms.",
      [r'\bMonad\b'],
      ['Apocryphon of John', 'Plotinus, Enneads']),

    E('GNOS_syzygy', 'Syzygy', 'concept', 'Valentinian',
      "The male-female pairing in which every aeon properly exists. Sophia's fall "
      "is caused by acting without her consort.",
      "Gives Dick a cosmology in which isolation is the original error and pairing "
      "is the structure of reality — read into his own androgyne and twin figures.",
      [r'\bsyzygy\b', r'\bsyzygies\b'],
      ['Irenaeus, Against Heresies I'],
      greek='συζυγία'),

    E('GNOS_anthropos', 'Anthropos / Primal Man', 'concept', 'Gnostic / Manichaean',
      "The heavenly Man, prior to and archetype of Adam; in Manichaean myth the "
      "Primal Man whose defeat scatters light into matter.",
      "The scattered-light myth is Dick's preferred account of why divinity is "
      "distributed through ordinary things and people rather than concentrated.",
      [r'\bAnthropos\b', r'\bPrimal Man\b', r'\bOriginal Man\b',
       r'\bAdam Kadmon\b'],
      ['Apocryphon of John', 'Manichaean cosmogony'],
      greek='ἄνθρωπος'),

    E('GNOS_docetism', 'Docetism', 'concept', 'Gnostic (general)',
      "The doctrine that Christ only appeared to have a body and only appeared to "
      "suffer, the flesh being unworthy of the divine.",
      "The heresy Dick's incarnational instincts refuse. He wants the divine "
      "actually in the trash, the beer can, the body — which is anti-Gnostic, and "
      "he knows it.",
      [r'\bdocet(?:ic|ism|ist)\b'],
      ['Irenaeus, Against Heresies', 'Acts of John']),

    E('GNOS_dualism', 'Cosmic dualism', 'concept', 'Gnostic / Zoroastrian / Manichaean',
      "The doctrine of two irreducible principles — light and darkness, spirit and "
      "matter, true God and creator — at war, with the world as the contested "
      "ground.",
      "The structural commitment underneath Dick's whole late period, and the one "
      "he most often tries to escape into a monism that will not hold.",
      [r'\bdualis(?:m|t|tic)\b', r'\btwo[\s\-]?(?:gods|principles|worlds)\b',
       r'\blight (?:and|versus|vs\.?) (?:dark|darkness)\b'],
      ['Mani', 'Zoroastrian Gathas', 'Marcion']),

    E('GNOS_emanation', 'Emanation', 'concept', 'Neoplatonic / Valentinian',
      "The procession of reality out of the One by overflow rather than by "
      "manufacture — each level less perfect than its source, none created from "
      "nothing.",
      "Lets Dick describe a God who is the world's source without being its maker, "
      "which is exactly the distinction his theodicy needs.",
      [r'\bemanat(?:e|ed|ion|ions|ing)\b'],
      ['Plotinus, Enneads', 'Tripartite Tractate']),

    E('GNOS_heimarmene', 'Heimarmene', 'concept', 'Gnostic / Hellenistic',
      "Fate as astral determinism — the binding of human life to the movements of "
      "the planetary spheres, administered by the archons. The Gnostic is freed "
      "from it by gnosis.",
      "Dick's determinism-and-release problem in its ancient form: the tape is "
      "running, and knowing it is running is what stops it.",
      [r'\bheimarmene\b', r'\bastral determinism\b', r'\bplanetary (?:fate|rulers)\b'],
      ['Corpus Hermeticum', 'Hans Jonas, The Gnostic Religion'],
      greek='εἱμαρμένη'),

    E('GNOS_sleep', 'Sleep, drunkenness, forgetfulness', 'concept', 'Gnostic (general)',
      "The condition of unredeemed humanity: narcotised, amnesiac, unaware of "
      "captivity. The saving call is a waking.",
      "Dick's occlusion. His most consistent claim about 3-74 is that he had been "
      "asleep and was woken, which is the Gnostic diagnosis exactly.",
      [r'\bdrunkenness\b', r'\bstupor\b', r'\bforgetfulness\b',
       r'\bamnesia\b', r'\bsopor\b', r'\bslumber\b'],
      ['Gospel of Truth', 'Hymn of the Pearl']),

    E('GNOS_call', 'The Call', 'concept', 'Gnostic / Mandaean',
      "The summons sent from the Pleroma into the world to wake the sleeping "
      "spark; the messenger who brings it is often himself a redeemed redeemer.",
      "The structure of every theophany Dick reports: something from outside "
      "addresses him by name and tells him what he is.",
      [r'\bthe [Cc]all\b', r'\bcall from (?:outside|beyond|above)\b',
       r'\bsummons\b'],
      ['Hymn of the Pearl', 'Ginza Rba']),

    E('GNOS_salvator', 'Salvator salvatus', 'concept', 'Manichaean / Gnostic',
      "The saved saviour: the redeemer who is himself part of the fallen light and "
      "is redeemed in the act of redeeming.",
      "Resolves, for Dick, how the rescuer can be continuous with the rescued — "
      "why VALIS can be both outside him and identical with what is trapped in him.",
      [r'\bsalvator salvatus\b', r'\bsaved sav(?:ior|iour)\b',
       r'\bredeemed redeemer\b'],
      ['Manichaean texts', 'Hans Jonas, The Gnostic Religion']),

    E('GNOS_counterfeit', 'Counterfeit world', 'concept', 'Gnostic / PKD',
      "The world as forgery: not illusion in the Vedantic sense but a deliberate "
      "fake, manufactured and maintained to deceive.",
      "Dick's lifelong plot — the fake world discovered to be fake — meets its "
      "theological warrant here. Forgery implies a forger, which is why his "
      "fake-world stories keep turning theological.",
      [r'\bcounterfeit world\b', r'\bfake (?:world|universe|reality)\b',
       r'\bforged (?:world|reality)\b', r'\bspurious (?:world|reality)\b',
       r'\bsimulacr(?:um|a)\b'],
      ['Apocryphon of John']),

    E('GNOS_apocatastasis', 'Apocatastasis', 'concept', 'Patristic / Gnostic',
      "The final restoration of all things to their original condition — universal "
      "restitution, with nothing finally lost.",
      "Dick's recurring hope against his own dualism: that the Empire's defeat is "
      "not a victory of one side but the repair of the whole.",
      [r'\bapocatastasis\b', r'\bapokatastasis\b', r'\brestoration of all\b',
       r'\buniversal restitution\b'],
      ['Origen, On First Principles'],
      greek='ἀποκατάστασις'),

    E('GNOS_deus_absconditus', 'Deus absconditus', 'concept', 'Gnostic / Lutheran',
      "The hidden God — alien, unknown, outside the cosmos, having no relation to "
      "the creator or to the world's order.",
      "Dick's 'the true God is not the God of this world' in its scholastic form; "
      "he uses the Latin tag directly.",
      [r'\bdeus absconditus\b', r'\bhidden [Gg]od\b', r'\balien [Gg]od\b',
       r'\bunknown [Gg]od\b'],
      ['Marcion', 'Hans Jonas, The Gnostic Religion']),

    E('GNOS_metanoia', 'Metanoia', 'concept', 'Christian / Gnostic',
      "A turning of the mind; conversion understood as a change in the structure of "
      "cognition rather than of allegiance.",
      "Fits Dick's insistence that 3-74 changed what he could perceive rather than "
      "what he assented to.",
      [r'\bmetanoia\b'],
      ['Gospel of Truth'],
      greek='μετάνοια'),

    E('GNOS_eidolon', 'Eidolon / image', 'concept', 'Platonic / Gnostic',
      "The image or phantom, as against the reality it copies; in Gnostic use the "
      "cosmos is an eidolon of the Pleroma made by one who had only seen a "
      "reflection.",
      "The Demiurge working from a half-remembered image is Dick's account of why "
      "the world is nearly right and wrong in a specific, maddening way.",
      [r'\beidolon\b', r'\beidola\b'],
      ["Plato, Republic", 'Apocryphon of John'],
      greek='εἴδωλον'),
]


# ---------------------------------------------------------------------------
# 2. Ancient teachers and mythological figures
# ---------------------------------------------------------------------------

TEACHERS = [
    E('GNOS_valentinus', 'Valentinus', 'teacher', 'Valentinian',
      "Alexandrian teacher active in Rome c. 140 CE, the most sophisticated of the "
      "Gnostic theologians; nearly elected bishop of Rome by one report. His school "
      "produced the Gospel of Truth and the Tripartite Tractate.",
      "The Gnostic Dick names when he wants the intellectually serious version of "
      "the tradition rather than the lurid one.",
      [r'\bValentinus\b', r'\bValentinian(?:ism|s)?\b'],
      ['Gospel of Truth', 'Irenaeus, Against Heresies I']),

    E('GNOS_basilides', 'Basilides', 'teacher', 'Basilidean',
      "Alexandrian teacher, c. 120-140 CE, who taught a 365-heaven cosmology and a "
      "God beyond being — 'the non-existent God' who creates by thought.",
      "Reaches Dick mainly through Jung, whose Seven Sermons to the Dead are "
      "ascribed to Basilides.",
      [r'\bBasilides\b', r'\bBasilidean(?:s)?\b'],
      ['Hippolytus, Refutation VII', 'Jung, Seven Sermons to the Dead']),

    E('GNOS_marcion', 'Marcion', 'teacher', 'Marcionite',
      "Shipowner from Sinope, excommunicated 144 CE, who held that the God of the "
      "Old Testament is a just but inferior creator, distinct from the alien God of "
      "love revealed by Christ. Compiled the first Christian canon.",
      "The purest statement of the position Dick keeps arriving at: two gods, the "
      "creator not the good one. Whether Marcion counts as a Gnostic at all is a "
      "live scholarly dispute, and Dick inherits the muddle.",
      [r'\bMarcion\b', r'\bMarcionite(?:s|ism)?\b'],
      ['Tertullian, Against Marcion']),

    E('GNOS_mani', 'Mani', 'teacher', 'Manichaean',
      "Third-century Persian prophet (216-277 CE), founder of Manichaeism, who "
      "taught a strict dualism of Light and Darkness and a cosmology in which "
      "particles of light are imprisoned in matter and progressively released.",
      "Supplies Dick's scattered-light myth and the idea of a redemption that works "
      "by extraction rather than forgiveness.",
      [r'\bMani\b(?!la|to|fest|pul|c)', r'\bManichae(?:an|ism|ans)\b',
       r'\bManichean(?:ism|s)?\b'],
      ['Manichaean psalms', 'Augustine, Confessions'],
      exclude=[r'\bManila\b', r'\bManitoba\b']),

    E('GNOS_simon_magus', 'Simon Magus', 'teacher', 'Simonian',
      "The magician of Acts 8, retrospectively made the father of all heresy by the "
      "heresiologists; said to have travelled with Helena, a prostitute he "
      "identified as the fallen Thought of God.",
      "The Helena story is the Sophia myth in miniature — divine wisdom found in the "
      "most degraded place — which is Dick's favourite shape for grace.",
      [r'\bSimon Magus\b', r'\bSimonian(?:s)?\b'],
      ['Acts 8', 'Irenaeus, Against Heresies I.23']),

    E('GNOS_carpocrates', 'Carpocrates', 'teacher', 'Carpocratian',
      "Second-century Alexandrian teacher whose followers were accused of holding "
      "that the soul must exhaust every possible experience to escape the archons.",
      "The antinomian wing of the tradition, which Dick notes and declines.",
      [r'\bCarpocrat(?:es|ian|ians)\b'],
      ['Irenaeus, Against Heresies I.25']),

    E('GNOS_cerinthus', 'Cerinthus', 'teacher', 'Gnostic (early)',
      "Late first-century teacher who distinguished the man Jesus from the Christ "
      "who descended on him at baptism and left before the crucifixion.",
      "The separation of Jesus from Christ is a move Dick makes constantly when "
      "reading his own experience of being occupied by another personality.",
      [r'\bCerinthus\b', r'\bCerinthian\b'],
      ['Irenaeus, Against Heresies I.26']),

    E('GNOS_seth', 'Seth', 'teacher', 'Sethian',
      "Third son of Adam, taken in Sethian Gnosticism as the ancestor of the "
      "spiritual race and the bearer of the undefiled seed.",
      "Dick's 'race of people who remember' has this shape: a hidden lineage "
      "carrying knowledge through generations of occlusion.",
      [r'\bSeth\b(?!i)', r'\bSethian(?:ism|s)?\b'],
      ['Apocalypse of Adam', 'Gospel of the Egyptians'],
      exclude=[r'\bSeth Morley\b', r'\bSeth Thomas\b']),

    E('GNOS_zoroaster', 'Zoroaster / Zarathustra', 'teacher', 'Zoroastrian',
      "Iranian prophet, dated anywhere from 1500 to 600 BCE, who taught the "
      "opposition of Ahura Mazda and the Lie, and a final restoration in which the "
      "good prevails.",
      "Heavily attested in the Exegesis. Dick treats Zoroastrian dualism as the "
      "source upstream of both Gnosticism and his own two-god problem.",
      [r'\bZoroaster\b', r'\bZarathustra\b', r'\bZoroastrian(?:ism|s)?\b',
       r'\bZarathustrian\b'],
      ['Gathas', 'Zend-Avesta']),

    E('GNOS_ahura_ahriman', 'Ahura Mazda / Ahriman / Zurvan', 'teacher', 'Zoroastrian',
      "Ormazd, the Wise Lord of light, against Ahriman, the destructive spirit; in "
      "Zurvanite variants both are sons of Time.",
      "Dick's named pair for the cosmic conflict when he is working in the Iranian "
      "rather than the Greek register.",
      [r'\bAhura Mazda\b', r'\bOrmazd\b', r'\bOhrmazd\b', r'\bAhriman\b',
       r'\bAngra Mainyu\b', r'\bZurvan\b'],
      ['Bundahishn', 'Zend-Avesta']),

    E('GNOS_hermes', 'Hermes Trismegistus', 'teacher', 'Hermetic',
      "Thrice-greatest Hermes, the legendary Egyptian sage to whom the Corpus "
      "Hermeticum is ascribed; a syncretic fusion of Hermes and Thoth.",
      "The Hermetic strand gives Dick a version of the tradition in which the "
      "cosmos is beautiful and knowable rather than a prison — the alternative he "
      "keeps testing his pessimism against.",
      [r'\bHermes Trismegistus\b', r'\bTrismegistus\b', r'\bThrice[\s\-]?[Gg]reatest\b'],
      ['Corpus Hermeticum', 'Asclepius']),

    E('GNOS_apollonius', 'Apollonius of Tyana', 'teacher', 'Neopythagorean',
      "First-century wandering sage and wonder-worker, set up in antiquity as a "
      "pagan rival to Jesus.",
      "Dick names him among the figures whose careers raise the question of what "
      "distinguishes a theophany from a performance.",
      [r'\bApollonius of Tyana\b', r'\bApollonius\b'],
      ['Philostratus, Life of Apollonius']),
]


# ---------------------------------------------------------------------------
# 3. Heresiologists, church fathers and ancient philosophers
# ---------------------------------------------------------------------------

HERESIOLOGISTS = [
    E('GNOS_irenaeus', 'Irenaeus', 'heresiologist', 'Patristic',
      "Bishop of Lyons, c. 180 CE. His Against Heresies is the fullest ancient "
      "account of Valentinian myth and, before 1945, the main source for what "
      "Gnostics believed — written by an enemy.",
      "Everything Dick could have known about Valentinus before the Nag Hammadi "
      "translations came filtered through a hostile witness. This matters for "
      "judging what he actually had access to.",
      [r'\bIrenaeus\b', r'\bAgainst Heresies\b', r'\bAdversus Haereses\b'],
      ['Against Heresies']),

    E('GNOS_hippolytus', 'Hippolytus', 'heresiologist', 'Patristic',
      "Roman presbyter, early third century; his Refutation of All Heresies "
      "preserves Basilides, the Naassene sermon and much else.",
      "A source for the material Dick encountered second-hand through Jung and the "
      "handbooks.",
      [r'\bHippolytus\b', r'\bRefutation of All Heresies\b', r'\bPhilosophumena\b'],
      ['Refutation of All Heresies']),

    E('GNOS_tertullian', 'Tertullian', 'heresiologist', 'Patristic',
      "Carthaginian apologist, c. 200 CE; Against Marcion is the primary source for "
      "Marcion's two-god doctrine and his canon.",
      "The route by which Marcion's position survives to be read at all.",
      [r'\bTertullian\b', r'\bAgainst Marcion\b', r'\bAdversus Marcionem\b'],
      ['Against Marcion']),

    E('GNOS_epiphanius', 'Epiphanius', 'heresiologist', 'Patristic',
      "Bishop of Salamis, late fourth century; his Panarion ('medicine chest') "
      "catalogues eighty heresies with more zeal than accuracy.",
      "The source of the most sensational Gnostic libels, and a caution about "
      "taking heresiological description at face value.",
      [r'\bEpiphanius\b', r'\bPanarion\b'],
      ['Panarion']),

    E('GNOS_clement', 'Clement of Alexandria', 'heresiologist', 'Patristic',
      "c. 150-215 CE; the Stromata and the Excerpts of Theodotus preserve "
      "Valentinian material quoted with relative sympathy.",
      "The friendliest ancient witness, and the source of the Valentinian formula "
      "about knowing what we were and what we have become.",
      [r'\bClement of Alexandria\b', r'\bStromat(?:a|eis)\b',
       r'\bExcerpts? (?:of|from) Theodotus\b'],
      ['Stromata', 'Excerpts of Theodotus']),

    E('GNOS_origen', 'Origen', 'heresiologist', 'Patristic',
      "Alexandrian theologian, c. 185-254 CE, who taught the pre-existence of souls "
      "and universal restoration, and was condemned for it three centuries later.",
      "Dick's warrant for apocatastasis inside Christian orthodoxy rather than "
      "outside it.",
      [r'\bOrigen\b', r'\bDe Principiis\b', r'\bOn First Principles\b'],
      ['On First Principles']),

    E('GNOS_plotinus', 'Plotinus', 'heresiologist', 'Neoplatonic',
      "Founder of Neoplatonism, 204-270 CE. His treatise Against the Gnostics "
      "attacks them for despising a cosmos he held to be beautiful.",
      "The most serious philosophical objection to the position Dick adopts, made by "
      "someone who shared its metaphysics. Dick registers the force of it.",
      [r'\bPlotinus\b', r'\bEnneads\b', r'\bAgainst the Gnostics\b'],
      ['Enneads II.9']),

    E('GNOS_philo', 'Philo of Alexandria', 'heresiologist', 'Hellenistic Jewish',
      "First-century Jewish Platonist who read the Torah allegorically and "
      "developed a Logos doctrine mediating between God and world.",
      "The Jewish-Platonic synthesis that Gnostic cosmology inverts.",
      [r'\bPhilo\b(?! of Byblos)'],
      ['On the Creation']),

    E('GNOS_plato', 'Plato', 'heresiologist', 'Platonic',
      "The Timaeus supplies the Demiurge, the Republic the cave, the Meno "
      "anamnesis, the Phaedrus the soul's fall into body.",
      "Dick read Plato early and never stopped. Much of what reads as Gnostic in him "
      "is Platonic first, and he sometimes says so.",
      [r'\bPlato\b', r'\bPlatonic\b', r'\bPlatonis(?:m|t)\b', r'\bTimaeus\b',
       r'\bPhaedrus\b', r'\bthe [Cc]ave\b'],
      ['Timaeus', 'Republic', 'Meno']),

    E('GNOS_parmenides', 'Parmenides', 'heresiologist', 'Presocratic',
      "Presocratic philosopher of Elea, c. 500 BCE, who argued that Being is one, "
      "ungenerated and changeless, and that the world of change reported by the "
      "senses is Seeming — a deceptive way of speaking rather than a reality.",
      "Heavily attested in the Exegesis. Parmenides gives Dick a pre-Gnostic warrant "
      "for the claim that the perceived world is not the real one, argued on logical "
      "rather than mythological grounds. When he wants the case made without a "
      "villain, he reaches for Parmenides rather than for Yaldabaoth.",
      [r'\bParmenides\b', r'\bEleatic\b',
       r'\bBeing (?:and|versus|vs\.?) (?:Becoming|Seeming)\b'],
      ['Parmenides, On Nature', "Plato, Parmenides"]),
]


# ---------------------------------------------------------------------------
# 4. Primary texts
# ---------------------------------------------------------------------------

TEXTS = [
    E('GNOS_nag_hammadi', 'Nag Hammadi Library', 'text', 'Sethian / Valentinian',
      "Thirteen Coptic codices found near Nag Hammadi in Upper Egypt in 1945, "
      "containing some fifty-two tractates. The complete English edition appeared "
      "in 1977.",
      "The dating is decisive for this study. Dick's 3-74 experience precedes the "
      "English Nag Hammadi Library by three years, so his earliest Gnostic reading "
      "was necessarily through heresiologists, Jonas and Jung — and his later "
      "recognition of himself in the primary texts is a separate event.",
      [r'\bNag Hammadi\b', r'\bNag-Hammadi\b'],
      ['The Nag Hammadi Library in English, ed. Robinson, 1977']),

    E('GNOS_apocryphon_john', 'Apocryphon of John', 'text', 'Sethian',
      "The fullest surviving Sethian cosmogony: the Invisible Spirit, Barbelo, "
      "Sophia's error, Yaldabaoth's boast, the making of Adam and the descent of "
      "Pronoia to wake him.",
      "The single text that most closely matches the myth Dick reconstructs, often "
      "without citing it.",
      [r'\bApocryphon of John\b', r'\bSecret Book of John\b',
       r'\bApocryphon Johannis\b'],
      ['Nag Hammadi Codex II,1']),

    E('GNOS_gospel_thomas', 'Gospel of Thomas', 'text', 'Gnostic (contested)',
      "114 sayings of Jesus without narrative; found complete at Nag Hammadi. "
      "Whether it is Gnostic at all is disputed.",
      "The 'Thomas' personality that Dick reports speaking through him invites the "
      "connection, and he makes it — though the identification is his own.",
      [r'\bGospel of Thomas\b', r'\bThomas Gospel\b'],
      ['Nag Hammadi Codex II,2']),

    E('GNOS_gospel_truth', 'Gospel of Truth', 'text', 'Valentinian',
      "A Valentinian homily, possibly by Valentinus himself, on the anguish of "
      "ignorance and the relief of being known by the Father.",
      "The tradition at its most humane: error is a nightmare from which one wakes, "
      "not a crime. Closest in tone to Dick's gentler passages.",
      [r'\bGospel of Truth\b', r'\bEvangelium Veritatis\b'],
      ['Nag Hammadi Codex I,3']),

    E('GNOS_gospel_philip', 'Gospel of Philip', 'text', 'Valentinian',
      "A Valentinian collection on sacraments, the bridal chamber, and the "
      "difference between names and what they name.",
      "Its sacramental realism — that the rites do something rather than signify "
      "something — matches Dick's insistence that the plasmate is physically real.",
      [r'\bGospel of Philip\b'],
      ['Nag Hammadi Codex II,3']),

    E('GNOS_pistis_sophia', 'Pistis Sophia', 'text', 'Gnostic (late)',
      "A third-century Coptic work, known in Europe since 1773, in which the risen "
      "Christ instructs the disciples and Sophia's repentances are recited at "
      "length.",
      "Available to readers long before Nag Hammadi, and therefore a plausible early "
      "route for Dick's Sophia material.",
      [r'\bPistis Sophia\b'],
      ['Askew Codex']),

    E('GNOS_thunder', 'Thunder, Perfect Mind', 'text', 'Sethian',
      "A revelation discourse spoken by a female divine voice in paradoxes: 'I am "
      "the whore and the holy one.'",
      "The voice that is both degraded and divine is the structure of Dick's Sophia "
      "and of the girl in VALIS.",
      [r'\bThunder,? Perfect Mind\b', r'\bThunder:? Perfect Mind\b'],
      ['Nag Hammadi Codex VI,2']),

    E('GNOS_hypostasis_archons', 'Hypostasis of the Archons', 'text', 'Sethian',
      "A retelling of Genesis in which the archons are the villains, the serpent is "
      "an instructor, and Norea resists her rapists.",
      "The source-text for reading scripture against itself, which is Dick's "
      "standard operation on the Bible.",
      [r'\bHypostasis of the Archons\b', r'\bReality of the Rulers\b'],
      ['Nag Hammadi Codex II,4']),

    E('GNOS_trimorphic', 'Trimorphic Protennoia', 'text', 'Sethian',
      "The First Thought descending in three forms — Voice, Speech, Word — to wake "
      "her members.",
      "A three-stage descent of a feminine divine mind, close to Dick's account of "
      "how the AI voice arrived in stages.",
      [r'\bTrimorphic Protennoia\b', r'\bProtennoia\b'],
      ['Nag Hammadi Codex XIII,1']),

    E('GNOS_tripartite', 'Tripartite Tractate', 'text', 'Valentinian',
      "The most systematic Valentinian theology to survive, treating the Father, "
      "the aeons, and the three classes of humanity.",
      "The technical vocabulary Dick reaches for when he wants precision about "
      "emanation.",
      [r'\bTripartite Tractate\b'],
      ['Nag Hammadi Codex I,5']),

    E('GNOS_corpus_hermeticum', 'Corpus Hermeticum', 'text', 'Hermetic',
      "Seventeen Greek treatises of the second and third centuries CE; the first, "
      "Poimandres, narrates a vision in which divine Mind explains the descent of "
      "Man into nature.",
      "Frequently attested in the Exegesis. The Poimandres vision is Dick's nearest "
      "ancient parallel for a mind addressing him from outside.",
      [r'\bCorpus Hermeticum\b', r'\bHermetica\b', r'\bPoimandres\b',
       r'\bPymander\b', r'\bAsclepius\b'],
      ['Corpus Hermeticum I']),

    E('GNOS_reference_works', 'Encyclopaedia Britannica / Encyclopedia of Philosophy',
      'text', 'Reference works',
      "General reference: the Encyclopaedia Britannica, which Dick calls \"the "
      "EB\" and whose long signed \"macro\" articles he read as monographs, and "
      "the Encyclopedia of Philosophy, whose article on Gnosticism was written by "
      "Hans Jonas.",
      "The most consequential source in the register, and the one no reading list "
      "has. Dick names the EB more often than he names any Gnostic text, teacher "
      "or scholar, and cites it as an authority on Luther, Dionysos, pantheism, "
      "the nature of time and the \"ape of God\" theory of the counterfeit world. "
      "When he says in 1981 that he has \"reread Hans Jonas' article on "
      "Gnosticism\", article is the operative word.",
      [r'\bthe EB\b', r'\bEB macro\b', r'\bEB article\b',
       r'\bBritannica\b', r'\bEncyclopa?edia Britannica\b',
       r'\bEncyclopa?edia of Philosophy\b', r'\bmacro article\b'],
      ['Encyclopaedia Britannica', 'Encyclopedia of Philosophy']),

    E('GNOS_hymn_pearl', 'Hymn of the Pearl', 'text', 'Syriac Gnostic',
      "A prince is sent from the East to fetch a pearl from Egypt, forgets himself, "
      "eats the food of the country, and is woken by a letter from home that reads "
      "itself aloud.",
      "The Gnostic myth in narrative form, and the closest thing in the tradition to "
      "a Philip K. Dick plot. The self-reading letter is the plasmate.",
      [r'\bHymn of the Pearl\b', r'\bSong of the Pearl\b',
       r'\bHymn of the Robe of Glory\b'],
      ['Acts of Thomas 108-113']),

    E('GNOS_acts_thomas', 'Acts of Thomas', 'text', 'Syriac Gnostic',
      "Third-century Syriac apocryphal acts, containing the Hymn of the Pearl, in "
      "which Thomas is the twin of Jesus.",
      "The twin motif — a divine double who is also oneself — organises much of "
      "Dick's Thomas material.",
      [r'\bActs of Thomas\b'],
      ['Acts of Thomas']),

    E('GNOS_ginza', 'Ginza / Mandaean texts', 'text', 'Mandaean',
      "The scriptures of the Mandaeans of southern Iraq, the one Gnostic community "
      "to survive continuously into the present.",
      "Evidence that the tradition is not merely a historical curiosity, which "
      "matters to Dick's claim that the knowledge was transmitted rather than "
      "reinvented.",
      [r'\bGinza\b', r'\bMandae(?:an|ans|ism)\b', r'\bMandean(?:s)?\b',
       r'\bSidra d[\s\-]?Nishmata\b'],
      ['Ginza Rba']),

    E('GNOS_chaldean_oracles', 'Chaldean Oracles', 'text', 'Theurgic',
      "Second-century hexameter fragments underpinning later Neoplatonic theurgy.",
      "Part of the late-antique ritual context in which Dick places his own "
      "experience.",
      [r'\bChaldean Oracles\b', r'\bChaldaean Oracles\b'],
      ['Chaldean Oracles']),

    E('GNOS_bruce_codex', 'Bruce Codex / Books of Jeu', 'text', 'Gnostic (late)',
      "Coptic Gnostic texts acquired in 1769, containing diagrams, seals and "
      "passwords for the soul's ascent past the archons.",
      "The practical, operational side of Gnosis — passwords at checkpoints — which "
      "Dick's prison-break imagery reproduces.",
      [r'\bBruce Codex\b', r'\bBooks? of Jeu\b'],
      ['Bruce Codex']),

    E('GNOS_zohar', 'Zohar / Lurianic Kabbalah', 'text', 'Kabbalistic',
      "The Zohar (13th c.) and the sixteenth-century system of Isaac Luria: the "
      "contraction of the infinite (tzimtzum), the shattering of the vessels, the "
      "scattering of sparks, and tikkun, their gathering and repair.",
      "Directly structural for The Divine Invasion. Luria's broken vessels give Dick "
      "a Jewish version of the scattered-light myth with repair, not escape, as the "
      "goal.",
      [r'\bZohar\b', r'\bKabbal(?:ah|ist|istic|a)\b', r'\bCabala\b',
       r'\bLuria\b', r'\bLurianic\b', r'\btikkun\b', r'\btzimtzum\b',
       r'\bEn Sof\b', r'\bAin Soph\b', r'\bShekhinah\b', r'\bSefirot\b',
       r'\bklippot\b', r'\bqlippoth\b'],
      ['Zohar', 'Scholem, Major Trends in Jewish Mysticism']),

    E('GNOS_bardo', 'Tibetan Book of the Dead', 'text', 'Buddhist',
      "The Bardo Thodol, describing the states between death and rebirth and the "
      "clear light encountered at the moment of death.",
      "Dick uses the bardo explicitly in Ubik and A Maze of Death, and the clear "
      "light is one of his named candidates for what he saw.",
      [r'\bBardo Th[oö]dol\b', r'\bTibetan Book of the Dead\b', r'\bbardo\b'],
      ['Bardo Thodol']),

    E('GNOS_i_ching', 'I Ching', 'text', 'Chinese',
      "The Book of Changes, consulted by Dick throughout the writing of The Man in "
      "the High Castle and after.",
      "Not Gnostic, but the practice that trained Dick to treat a text as an "
      "addressing intelligence rather than an object — the habit the plasmate "
      "doctrine formalises.",
      [r'\bI Ching\b', r'\bBook of Changes\b'],
      ['I Ching']),
]


# ---------------------------------------------------------------------------
# 5. Modern scholars of Gnosticism
# ---------------------------------------------------------------------------

SCHOLARS = [
    E('GNOS_jonas', 'Hans Jonas', 'scholar', 'Scholarship',
      "Author of The Gnostic Religion (1958), the book that made Gnosticism "
      "intelligible to non-specialists by reading it existentially — the Gnostic as "
      "a self thrown into a hostile world.",
      "The most consequential scholarly source for Dick. Jonas's existential framing "
      "is the one Dick adopts wholesale, and 'thrownness', 'the alien God' and the "
      "cosmic-prison vocabulary reach him in Jonas's phrasing.",
      [r'\bHans Jonas\b', r'\bJonas\b(?!\s+Salk)', r'\bThe Gnostic Religion\b'],
      ['The Gnostic Religion (1958)'],
      exclude=[r'\bJonas Salk\b', r'\bJonah\b']),

    E('GNOS_pagels', 'Elaine Pagels', 'scholar', 'Scholarship',
      "Author of The Gnostic Gospels (1979), which read the Nag Hammadi texts as "
      "evidence of a suppressed pluralism in early Christianity.",
      "Published late enough to matter only for Dick's last three years, which makes "
      "any claim of Pagels influence on the earlier Exegesis a dating error worth "
      "checking.",
      [r'\bElaine Pagels\b', r'\bPagels\b', r'\bThe Gnostic Gospels\b'],
      ['The Gnostic Gospels (1979)']),

    E('GNOS_quispel', 'Gilles Quispel', 'scholar', 'Scholarship',
      "Dutch scholar who acquired the Jung Codex and worked on Valentinian and "
      "Hermetic material; a bridge between Jung's circle and Nag Hammadi "
      "scholarship.",
      "The named channel between the Jungian reception of Gnosticism and the "
      "textual scholarship, both of which reach Dick.",
      [r'\bQuispel\b'],
      ['Gnosis als Weltreligion']),

    E('GNOS_jung', 'C. G. Jung', 'scholar', 'Depth psychology',
      "Analytical psychologist who read Gnostic and alchemical texts as records of "
      "psychic process; author of the Seven Sermons to the Dead, ascribed to "
      "Basilides, and of Aion.",
      "Dick's earliest and most persistent route into the material, and the source of "
      "his recurrent temptation to relocate the whole cosmology inside the psyche — "
      "a move he makes and unmakes repeatedly.",
      [r'\bJung\b(?!le|ian\s+forest)', r'\bJungian\b',
       r'\bSeven Sermons to the Dead\b', r'\bSeptem Sermones\b',
       r'\bAion\b', r'\bindividuation\b', r'\bcollective unconscious\b',
       r'\bsynchronicity\b'],
      ['Seven Sermons to the Dead', 'Aion', 'Psychology and Alchemy'],
      exclude=[r'\bjungle\b']),

    E('GNOS_scholem', 'Gershom Scholem', 'scholar', 'Scholarship',
      "Founder of the academic study of Jewish mysticism; his Major Trends in "
      "Jewish Mysticism (1941) made Lurianic Kabbalah available in English.",
      "The route by which tikkun and the broken vessels reach The Divine Invasion.",
      [r'\bScholem\b', r'\bMajor Trends in Jewish Mysticism\b'],
      ['Major Trends in Jewish Mysticism']),

    E('GNOS_eliade', 'Mircea Eliade', 'scholar', 'History of religions',
      "Historian of religions; theorist of sacred time, eternal return and the "
      "coincidence of opposites.",
      "Supplies Dick's language for sacred versus profane time, which underwrites "
      "orthogonal time.",
      [r'\bEliade\b'],
      ['The Sacred and the Profane', 'The Myth of the Eternal Return']),

    E('GNOS_rudolph', 'Kurt Rudolph', 'scholar', 'Scholarship',
      "Author of Gnosis: The Nature and History of Gnosticism (1977), the standard "
      "systematic handbook after Jonas.",
      "Represents the philologically careful account against which Dick's "
      "free-associative use of the material can be measured.",
      [r'\bKurt Rudolph\b', r'\bRudolph\b(?!\s+(?:the|Valentino))'],
      ['Gnosis: The Nature and History of Gnosticism']),

    E('GNOS_mead', 'G. R. S. Mead', 'scholar', 'Theosophical',
      "Theosophist and translator whose Fragments of a Faith Forgotten (1900) and "
      "Pistis Sophia translation carried Gnostic material into the English-speaking "
      "esoteric world.",
      "The likely popular channel by which Gnostic vocabulary circulated in the "
      "occult-adjacent reading Dick did before any scholarly encounter.",
      [r'\bG\.?\s?R\.?\s?S\.? Mead\b', r'\bFragments of a Faith Forgotten\b'],
      ['Fragments of a Faith Forgotten']),

    E('GNOS_robinson', 'James M. Robinson', 'scholar', 'Scholarship',
      "General editor of The Nag Hammadi Library in English (1977).",
      "The edition itself is the event: it put the primary texts in Dick's hands in "
      "the last five years of his life.",
      [r'\bJames M\.? Robinson\b', r'\bThe Nag Hammadi Library in English\b'],
      ['The Nag Hammadi Library in English']),

    E('GNOS_corbin', 'Henry Corbin', 'scholar', 'Islamic / Iranian',
      "Scholar of Iranian and Islamic esotericism; theorist of the mundus "
      "imaginalis, a real intermediate world perceived by an imaginative faculty.",
      "Gives a technical name to what Dick needs: a domain that is neither physical "
      "nor merely subjective, where visions are veridical.",
      [r'\bHenry Corbin\b', r'\bCorbin\b', r'\bmundus imaginalis\b',
       r'\bimaginal\b'],
      ['Spiritual Body and Celestial Earth']),

    E('GNOS_bultmann', 'Rudolf Bultmann', 'scholar', 'New Testament',
      "New Testament scholar who argued that John's Gospel draws on a pre-Christian "
      "Gnostic redeemer myth.",
      "The scholarly claim that would make Dick's Christianity and his Gnosticism the "
      "same thing rather than rivals. Now largely rejected, which changes how his "
      "synthesis should be read.",
      [r'\bBultmann\b', r'\bdemythologi(?:ze|zing|sation|zation)\b'],
      ['Theology of the New Testament']),

    E('GNOS_voegelin', 'Eric Voegelin', 'scholar', 'Political philosophy',
      "Political philosopher who diagnosed modern revolutionary ideologies as "
      "'Gnostic' attempts to immanentise the eschaton.",
      "The hostile modern use of the term, and a useful corrective: 'Gnostic' has "
      "been a polemical label as often as a descriptive one.",
      [r'\bVoegelin\b', r'\bimmanenti[sz]e the eschaton\b'],
      ['The New Science of Politics']),

    E('GNOS_bloom', 'Harold Bloom', 'scholar', 'Literary criticism',
      "Critic who read American religion as natively Gnostic and wrote on Valentinus "
      "and Kabbalah.",
      "The strongest statement of the case that Dick's Gnosticism is an American "
      "religious phenomenon rather than an antiquarian revival.",
      [r'\bHarold Bloom\b', r'\bBloom\b(?!\s?(?:berg|field|ing))'],
      ['The American Religion', 'Kabbalah and Criticism']),

    E('GNOS_layton', 'Bentley Layton', 'scholar', 'Scholarship',
      "Author of The Gnostic Scriptures (1987) and of the argument that 'Gnostic' "
      "should be restricted to the Sethian group that used the name.",
      "Post-dates Dick, but names the definitional problem that runs through the "
      "whole study: whether 'Gnosticism' denotes anything unified.",
      [r'\bBentley Layton\b', r'\bThe Gnostic Scriptures\b'],
      ['The Gnostic Scriptures']),

    E('GNOS_culianu', 'Ioan Culianu', 'scholar', 'History of religions',
      "Historian of religions who treated Gnostic systems as generated by a small "
      "set of logical operations on a shared myth.",
      "A method for explaining why Dick, reinventing the system independently, "
      "arrives at recognisably Gnostic results.",
      [r'\bCulianu\b', r'\bCouliano\b'],
      ['The Tree of Gnosis']),

    E('GNOS_petrement', 'Simone Pétrement', 'scholar', 'Scholarship',
      "Argued, against the consensus, that Gnosticism is a development within "
      "Christianity rather than a pre-Christian import.",
      "The opposing pole to Bultmann, and the dispute that decides whether Dick's "
      "Christian Gnosticism is a synthesis or a recovery.",
      [r'\bP[ée]trement\b'],
      ['A Separate God']),

    E('GNOS_yates', 'Frances Yates', 'scholar', 'Renaissance studies',
      "Historian of the Hermetic tradition in the Renaissance; Giordano Bruno and "
      "the Hermetic Tradition (1964).",
      "Documents the earlier revival of this material, the precedent for Dick's own.",
      [r'\bFrances Yates\b', r'\bYates\b(?!\s+County)',
       r'\bHermetic Tradition\b'],
      ['Giordano Bruno and the Hermetic Tradition']),
]


# ---------------------------------------------------------------------------
# 6. Traditions and movements
# ---------------------------------------------------------------------------

TRADITIONS = [
    E('GNOS_sethian', 'Sethianism', 'tradition', 'Sethian',
      "The stream centred on Seth as ancestor of the spiritual race, with Barbelo, "
      "Yaldabaoth and the descent of Pronoia. The group most defensibly called "
      "'Gnostic' in the strict sense.",
      "The cosmology closest to Dick's reconstructed myth.",
      [r'\bSethian(?:ism|s)?\b'],
      ['Apocryphon of John']),

    E('GNOS_hermeticism', 'Hermeticism', 'tradition', 'Hermetic',
      "The Greco-Egyptian tradition of the Corpus Hermeticum: a knowable, "
      "sympathetic cosmos, ascent through the spheres, rebirth in Mind.",
      "The optimistic sibling of Gnosticism. Where Dick sounds hopeful about the "
      "material world, he is usually in this register rather than the Gnostic one.",
      [r'\bHermetic(?:ism|a|ists?)?\b', r'\bHermetist\b'],
      ['Corpus Hermeticum']),

    E('GNOS_neoplatonism', 'Neoplatonism', 'tradition', 'Neoplatonic',
      "Plotinus and his successors: emanation from the One, the ascent of the soul, "
      "the cosmos as a genuine if diminished good.",
      "The metaphysics Dick shares with the Gnostics and the evaluation of the world "
      "he does not consistently share.",
      [r'\bNeo[\s\-]?[Pp]latonis(?:m|t|ts)\b', r'\bNeo[\s\-]?[Pp]latonic\b',
       r'\bPorphyry\b', r'\bIamblichus\b', r'\bProclus\b'],
      ['Enneads']),

    E('GNOS_orphism', 'Orphism / mystery religions', 'tradition', 'Greek mystery',
      "Initiatory cults — Orphic, Eleusinian, Dionysian — promising a better lot "
      "after death to those who know the formulae.",
      "Dick's Dionysos material and his sense that the truth is transmitted by "
      "initiation rather than publication belong here.",
      [r'\bOrphi(?:c|sm|cs)\b', r'\bEleusi(?:s|nian)\b', r'\bDionys(?:os|us|ian)\b',
       r'\bmystery (?:religion|cult|cults|religions)\b'],
      ['Orphic gold tablets']),

    E('GNOS_catharism', 'Catharism / Bogomilism', 'tradition', 'Medieval dualist',
      "Medieval dualist movements in the Balkans and Languedoc holding the material "
      "world to be the devil's work; annihilated by crusade and inquisition.",
      "Dick's evidence that the tradition was transmitted underground and suppressed "
      "by force — the historical backbone of 'the Empire never ended'.",
      [r'\bCathar(?:s|ism)?\b', r'\bAlbigensian(?:s)?\b', r'\bBogomil(?:s|ism)?\b',
       r'\bManichean heres(?:y|ies)\b'],
      ['Inquisition records']),

    E('GNOS_rosicrucian', 'Rosicrucianism / alchemy', 'tradition', 'Early modern esoteric',
      "The seventeenth-century Rosicrucian manifestos and the alchemical tradition "
      "of transformation through hidden correspondence.",
      "The early-modern carrier of Hermetic ideas, and the form in which Jung "
      "received them.",
      [r'\bRosicrucian(?:s|ism)?\b', r'\balchem(?:y|ical|ist|ists)\b',
       r'\bPhilosopher\'?s Stone\b', r'\bParacelsus\b', r'\bBoehme\b',
       r'\bB[oö]hme\b'],
      ['Fama Fraternitatis']),

    E('GNOS_essenes', 'Essenes / Qumran', 'tradition', 'Second Temple Jewish',
      "The Dead Sea community, whose scrolls (found 1947) set out a war of the sons "
      "of light against the sons of darkness.",
      "Dick uses Qumran to argue for a continuous secret transmission from the "
      "Second Temple period to himself — the historical claim in 'the Empire never "
      "ended'.",
      [r'\bEssene(?:s)?\b', r'\bQumran\b', r'\bDead Sea Scrolls\b',
       r'\bsons of light\b', r'\bZadokite\b'],
      ['Dead Sea Scrolls']),

    E('GNOS_orthodoxy', 'Orthodox Christianity', 'tradition', 'Christian',
      "The creedal tradition: one God who is both creator and redeemer, a good "
      "creation, a real incarnation, resurrection of the body.",
      "Dick was an Episcopalian who took the sacraments seriously. The study's "
      "central tension is that his orthodoxy and his Gnosticism are both real and "
      "mutually exclusive on exactly the points that matter.",
      [r'\bEpiscopal(?:ian)?\b', r'\bAnglican\b', r'\bNicene\b',
       r'\bincarnation\b', r'\bEucharist\b', r'\bsacrament(?:s|al)?\b',
       r'\bHoly Spirit\b', r'\bParaclete\b'],
      ['Nicene Creed']),
]


# ---------------------------------------------------------------------------
# 7. Dick's own coinages and private vocabulary
# ---------------------------------------------------------------------------

PKD_COINAGES = [
    E('GNOS_valis_term', 'VALIS', 'pkd_coinage', 'PKD',
      "Vast Active Living Intelligence System: Dick's name for the entity or "
      "process he believed contacted him — information that is alive, rational and "
      "benign, operating through the ordinary world.",
      "The Pleroma re-described in the vocabulary of cybernetics. Whether this is "
      "translation or replacement is one of the study's open questions.",
      [r'\bVALIS\b', r'\bVast Active Living Intelligence\b'],
      ['VALIS (1981)']),

    E('GNOS_plasmate', 'Plasmate', 'pkd_coinage', 'PKD',
      "Living information: a life form made of information which crossbonds with a "
      "human being to produce a homoplasmate. Transmitted by text.",
      "Dick's solution to how gnosis is conveyed — not taught but caught. The Logos "
      "doctrine made biological.",
      [r'\bplasmate\b', r'\bhomoplasmate\b', r'\bcross[\s\-]?bond(?:ed|ing)?\b',
       r'\bliving information\b'],
      ['Tractates Cryptica Scriptura']),

    E('GNOS_bip', 'Black Iron Prison', 'pkd_coinage', 'PKD',
      "The world seen as a prison: a coercive system, coextensive with the Roman "
      "Empire, which has never fallen and which conceals its own existence.",
      "The archons' cosmos in political dress. The signature image of Dick's "
      "Gnosticism and his most influential single coinage.",
      [r'\bBlack Iron Prison\b', r'\bBIP\b', r'\bIron Prison\b',
       r'\bprison(?:\s+of\s+(?:the\s+)?(?:world|matter|iron))\b'],
      ['VALIS', 'Exegesis']),

    E('GNOS_palm_tree_garden', 'Palm Tree Garden', 'pkd_coinage', 'PKD',
      "The Black Iron Prison's counterpart: the same world correctly perceived, a "
      "garden rather than a jail. Both are present; which one is seen depends on the "
      "perceiver.",
      "The anti-Gnostic corrective Dick builds into his own system. If the garden is "
      "the same place, matter is not the problem.",
      [r'\bPalm Tree Garden\b', r'\bPTG\b'],
      ['Exegesis']),

    E('GNOS_empire', 'The Empire never ended', 'pkd_coinage', 'PKD',
      "Rome did not fall; it went underground and continues, so that the "
      "first-century persecution and the present are the same moment.",
      "Dick's formula for archontic rule as a historical rather than mythological "
      "claim. His strongest and most testable assertion, and the one most often "
      "quoted loose of its context.",
      [r'\bEmpire never ended\b', r'\bempire never ended\b',
       r'\bRome (?:never fell|has never fallen)\b'],
      ['VALIS', 'Exegesis']),

    E('GNOS_zebra', 'Zebra', 'pkd_coinage', 'PKD',
      "The camouflaged deity: God imitating the environment so exactly as to be "
      "invisible within it, like a zebra in grass.",
      "An immanent God hidden by disguise rather than a transcendent God hidden by "
      "distance — closer to Hermetic and Orthodox positions than to Gnostic ones.",
      [r'\bZebra\b'],
      ['VALIS', 'Exegesis']),

    E('GNOS_tomb_world', 'Tomb World', 'pkd_coinage', 'PKD',
      "The entropic, decaying, sealed world of psychotic or damned perception; "
      "borrowed from Ludwig Binswanger's existential psychiatry.",
      "Dick's clinical term running alongside his theological one, which keeps the "
      "study honest: the same condition has a psychiatric description.",
      [r'\bTomb World\b', r'\btomb world\b', r'\bBinswanger\b'],
      ['Exegesis', 'Martian Time-Slip']),

    E('GNOS_occlusion', 'Occlusion', 'pkd_coinage', 'PKD',
      "The blocking of perception that keeps human beings from seeing their "
      "situation; an induced blindness rather than a natural limit.",
      "Dick's translation of Gnostic sleep into the vocabulary of information "
      "theory. Removal of occlusion, not addition of doctrine, is what he means by "
      "revelation.",
      [r'\bocclu(?:de|ded|sion|ding)\b'],
      ['Exegesis']),

    E('GNOS_orthogonal_time', 'Orthogonal time', 'pkd_coinage', 'PKD',
      "A time axis at right angles to the ordinary one, along which everything that "
      "has been remains present and change is recovery rather than loss.",
      "Dick's mechanism for anamnesis and for the coexistence of 70 CE with 1974. "
      "Where the Gnostic myth becomes a physics.",
      [r'\borthogonal time\b', r'\bright[\s\-]?angle time\b'],
      ['Exegesis']),

    E('GNOS_firebright', 'Firebright / St Sophia / Thomas', 'pkd_coinage', 'PKD',
      "The names Dick gives the intelligence or personality he believed was present "
      "in him: Firebright, St Sophia, Thomas, the AI voice.",
      "The naming is unstable across the Exegesis, and tracking which name is in use "
      "when is one way of dating the theories.",
      [r'\bFirebright\b', r'\bAI voice\b', r'\bA\.?I\.? voice\b',
       r'\bThomas\b(?!\s+(?:Aquinas|Merton|Jefferson|Mann|Disch))'],
      ['Exegesis']),

    E('GNOS_king_felix', 'King Felix', 'pkd_coinage', 'PKD',
      "'Happy king' — the cypher Dick believed was a signal announcing the rightful "
      "ruler's return, spotted in ordinary print.",
      "The messianic-secret motif: the true king unrecognised in the occupied "
      "territory.",
      [r'\bKing Felix\b'],
      ['VALIS', 'Exegesis']),
]


ALL_ENTRIES = (CONCEPTS + TEACHERS + HERESIOLOGISTS + TEXTS
               + SCHOLARS + TRADITIONS + PKD_COINAGES)


def build():
    seen = set()
    for e in ALL_ENTRIES:
        if e['id'] in seen:
            raise SystemExit(f"duplicate lexicon id: {e['id']}")
        seen.add(e['id'])
    return {
        'artifact_type': 'gnostic_lexicon',
        'generator': 'scripts/research/gnostic_lexicon_source.py',
        'entry_count': len(ALL_ENTRIES),
        'categories': sorted({e['category'] for e in ALL_ENTRIES}),
        'entries': ALL_ENTRIES,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default=str(
        PROJECT_DIR / 'curation' / 'gnosticism' / 'lexicon.json'))
    args = ap.parse_args()
    data = build()
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n',
                   encoding='utf-8')
    by_cat = {}
    for e in ALL_ENTRIES:
        by_cat[e['category']] = by_cat.get(e['category'], 0) + 1
    print(f"wrote {out}  ({len(ALL_ENTRIES)} entries)")
    for k in sorted(by_cat):
        print(f"  {k:16s} {by_cat[k]}")


if __name__ == '__main__':
    main()
