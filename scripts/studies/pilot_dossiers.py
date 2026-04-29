#!/usr/bin/env python3
"""
Layer 2 Pilot: Draft dossier sections for 4 pilot topics.
Prose is written directly — no API calls.
"""

import json
import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parent.parent.parent / 'database' / 'unified.sqlite'

# ── Dossier content per topic ─────────────────────────────────

DOSSIERS = {
    'TOPIC_AI_androids': {
        'definition': (
            "In PKD's work, the android is an artificial being that mimics human appearance "
            "and behavior with sufficient fidelity to pass as human, raising questions about "
            "what constitutes authentic personhood and whether empathy is the decisive criterion "
            "for distinguishing human from non-human."
        ),
        'pkd_relevance': (
            "The android is arguably PKD's most distinctive philosophical creation. Across novels "
            "such as Do Androids Dream of Electric Sheep? and We Can Build You, and throughout "
            "the Exegesis, the figure of the android serves as a lens for examining empathy, "
            "authenticity, and the nature of the soul. PKD repeatedly returns to the idea that "
            "the real danger is not that machines will become human-like, but that humans will "
            "become machine-like — android in affect, stripped of caritas."
        ),
        'in_the_fiction': (
            "In Do Androids Dream of Electric Sheep?, androids are Nexus-6 models subjected to "
            "the Voigt-Kampff empathy test by bounty hunters. Characters like Rachael Rosen blur "
            "the line between authentic and artificial feeling. In We Can Build You, the simulacra "
            "of Lincoln and Stanton raise questions about whether perfect historical reproduction "
            "constitutes personhood. Across PKD's fiction, the android is less a technological "
            "problem than an ethical one: the test of empathy is also a test of the tester."
        ),
        'in_the_exegesis': (
            "In the Exegesis, PKD extends the android concept beyond fiction into theology and "
            "self-analysis. He theorizes that the 'android' condition — the absence of empathy — "
            "is a spiritual rather than mechanical state. Passages describe the Black Iron Prison "
            "as a system that renders its inhabitants android-like, stripping them of authentic "
            "feeling. The Exegesis frames the recovery of empathy as a form of anamnesis, a "
            "remembering of one's true divine nature."
        ),
        'intellectual_background': (
            "PKD's android concept draws on cybernetics, existentialism, and Gnostic theology. "
            "Norbert Wiener's work on feedback systems informs the mechanical dimension; "
            "Heidegger's distinction between authentic and inauthentic existence provides the "
            "philosophical frame; and Gnostic ideas about the demiurge and the pneumatic spark "
            "shape the theological layer. The Turing test and debates about machine consciousness "
            "provide the science-fiction scaffolding."
        ),
        'scholarly_debate': (
            "Scholars disagree about whether PKD's androids are primarily social allegory "
            "(Fitting, Freedman), existential parable (Warrick), or theological proposition "
            "(Galvan, Davis). Some critics emphasize the political dimension — androids as "
            "exploited labor class — while others focus on the empathy criterion as PKD's "
            "distinctive contribution to the philosophical problem of other minds."
        ),
        'chronology_summary': (
            "PKD's engagement with androids begins in early stories like 'Second Variety' (1953) "
            "and matures through Do Androids Dream (1968) into the theological reflections of "
            "the Exegesis (1974-1982), where the android concept merges with Gnostic cosmology."
        ),
        'contradictions_summary': (
            "A core tension exists between PKD's fictional depiction of androids as objects of "
            "sympathy (Rachael, Luba Luft) and his Exegetical use of 'android' as a term of "
            "spiritual condemnation. Additionally, the Exegesis oscillates between treating "
            "the android condition as imposed (by the Black Iron Prison) and as chosen (through "
            "loss of empathy)."
        ),
        'editorial_notes': (
            "Researchers should distinguish carefully between PKD's use of 'android' in fiction "
            "(specific artificial beings) and in the Exegesis (a spiritual/psychological state). "
            "The term shifts meaning across his career."
        ),
        'open_questions': json.dumps([
            "Does PKD ultimately grant androids the capacity for genuine empathy, or does he preserve an ontological distinction?",
            "How does PKD's android concept relate to his later VALIS theology, where the divine is discovered within the seemingly mechanical?",
            "What is the relationship between the android-affect concept in the Exegesis and PKD's real-world experiences of emotional flatness?"
        ]),
        'card_description': (
            "The android as PKD's central figure for examining empathy, authenticity, and the boundary between human and non-human."
        ),
    },

    'TOPIC_AI_simulation': {
        'definition': (
            "Simulation in PKD's work refers to the possibility that experienced reality is "
            "a constructed, projected, or counterfeit version of a deeper or truer reality — "
            "a theme that bridges his science fiction, his Gnostic theology, and his personal "
            "experiences of ontological uncertainty."
        ),
        'pkd_relevance': (
            "Simulation is one of PKD's most persistent and philosophically significant themes. "
            "From the fake worlds of Time Out of Joint and The Man in the High Castle to the "
            "half-life of Ubik and the Black Iron Prison of the Exegesis, PKD repeatedly "
            "constructs narratives in which characters discover that their perceived reality is "
            "fabricated. After 2-3-74, this fictional theme became a lived conviction: PKD came "
            "to believe that the Roman Empire had never ended and that contemporary reality was "
            "a simulation overlaying the true apostolic world."
        ),
        'in_the_fiction': (
            "PKD's fiction is saturated with simulation scenarios. In Time Out of Joint (1959), "
            "Ragle Gumm discovers his small-town life is an elaborate construct. In The Man in "
            "the High Castle (1962), the I Ching suggests that the Axis-victory world may itself "
            "be a fiction. Ubik (1969) presents nested levels of simulated reality in half-life. "
            "These works establish simulation not as a single plot device but as PKD's fundamental "
            "narrative architecture."
        ),
        'in_the_exegesis': (
            "The Exegesis treats simulation as an ontological proposition rather than a fictional "
            "device. PKD theorizes that the phenomenal world is a 'dokos' (Greek for semblance), "
            "a hologrammatic projection generated by the Black Iron Prison to conceal the true "
            "Palm Tree Garden reality beneath. He draws on Platonic, Gnostic, and Vedantic "
            "frameworks to describe layers of simulation, and connects his 2-3-74 experience to "
            "the moment when the simulated veil was momentarily pierced."
        ),
        'intellectual_background': (
            "PKD's simulation concept draws on Plato's cave allegory, Gnostic cosmology (the "
            "demiurge as reality-fabricator), Buddhist and Hindu concepts of Maya, and "
            "Baudrillard's simulacra theory. The concept anticipates later 'simulation hypothesis' "
            "arguments by Bostrom and others, though PKD's version is theologically rather than "
            "computationally grounded."
        ),
        'scholarly_debate': (
            "Scholars debate whether PKD's simulation theme is primarily epistemological "
            "(how do we know what is real?) or ontological (what is the nature of reality itself?). "
            "Baudrillard cited PKD as a key precursor. Critics like Fitting emphasize the political "
            "dimension — simulation as ideology — while Davis and Kripal read the theme through "
            "religious studies as a modern Gnostic revelation narrative."
        ),
        'chronology_summary': (
            "Simulation themes appear in PKD's earliest work but intensify after 2-3-74, when the "
            "fictional device became a personal conviction. The Exegesis passages on simulation "
            "are concentrated in the 1976-1981 period."
        ),
        'contradictions_summary': (
            "PKD oscillates between treating simulation as a prison to be escaped and as a "
            "necessary structure maintained by the divine for pedagogical purposes. The Exegesis "
            "also wavers between Platonic (reality as shadow of the Forms) and Gnostic (reality as "
            "trap set by the demiurge) frameworks, which carry different ethical implications."
        ),
        'editorial_notes': (
            "The simulation theme overlaps heavily with False Reality and Reality Testing topics. "
            "Researchers should cross-reference these entries and note that PKD's simulation concept "
            "is theological rather than computational."
        ),
        'open_questions': json.dumps([
            "Does PKD's simulation concept ultimately resolve into a Platonic, Gnostic, or uniquely Dickian framework?",
            "How does the simulation theme in the fiction differ structurally from the simulation claims in the Exegesis?",
            "What is the relationship between PKD's simulation ideas and his amphetamine use in the 1960s-70s?"
        ]),
        'card_description': (
            "Simulation as PKD's master theme: the possibility that experienced reality is constructed, projected, or counterfeit."
        ),
    },

    'TOPIC_PSY_paranoia': {
        'definition': (
            "Paranoia in PKD's work refers to the pervasive sense that reality is conspiratorially "
            "organized against the subject — a theme that operates simultaneously as a psychiatric "
            "condition depicted in fiction, a lived experience described in the Exegesis, and a "
            "narrative engine that drives some of PKD's most powerful stories."
        ),
        'pkd_relevance': (
            "Paranoia is inseparable from PKD's biography and art. His fiction is populated with "
            "characters who suspect that their reality is manipulated by hidden forces — and who "
            "are frequently proven right. PKD's own experiences, including the November 1971 "
            "break-in at his San Rafael home and the events of 2-3-74, blurred the line between "
            "paranoid ideation and genuine threat. The Exegesis contains extended reflections on "
            "whether his perceptions were pathological or revelatory."
        ),
        'in_the_fiction': (
            "PKD's fiction deploys paranoia as both theme and structure. In A Scanner Darkly, "
            "Bob Arctor surveys himself without knowing it, embodying paranoia as recursive "
            "self-suspicion. In The Man in the High Castle, characters discover that their entire "
            "historical reality may be false. Stories like 'Adjustment Team' and novels like "
            "Time Out of Joint present ordinary people who discover that powerful agencies have "
            "constructed their perceived reality. In PKD's fiction, the paranoid is often the "
            "one character who perceives reality accurately."
        ),
        'in_the_exegesis': (
            "The Exegesis records PKD's sustained attempt to determine whether his paranoid "
            "perceptions were symptoms of mental illness or accurate perceptions of a hidden "
            "reality. He describes the break-in, the pink light experience, and subsequent "
            "events through multiple competing frameworks: political conspiracy, divine "
            "revelation, psychiatric disorder, and information-theoretic models. Notably, PKD "
            "does not simply endorse or dismiss paranoia but treats it as an epistemological "
            "problem that resists resolution."
        ),
        'intellectual_background': (
            "PKD's treatment of paranoia draws on Cold War culture, psychoanalytic theory, and "
            "existential philosophy. The political climate of the 1950s-70s — McCarthyism, "
            "COINTELPRO, Watergate — provided real-world validation for paranoid narratives. "
            "Laing's anti-psychiatric work suggested that 'madness' could be a sane response to "
            "an insane world, a position PKD explored without fully endorsing."
        ),
        'scholarly_debate': (
            "Critics disagree about whether PKD's paranoia should be read as political allegory, "
            "psychological self-portraiture, or epistemological exploration. Some scholars "
            "(Freedman, Jameson) emphasize the Marxist-political dimension: paranoia as "
            "recognition of systemic domination. Others (Sutin, Rickman) foreground the "
            "biographical dimension. A third camp (Davis, Kripal) reads PKD's paranoia as a "
            "modern shamanic or mystical sensitivity."
        ),
        'chronology_summary': (
            "Paranoia themes appear throughout PKD's career, intensifying after the 1971 break-in "
            "and the 2-3-74 experiences. The Exegesis represents PKD's most sustained engagement "
            "with paranoia as a philosophical problem."
        ),
        'contradictions_summary': (
            "The central tension in PKD's treatment of paranoia is whether it represents a "
            "clinical pathology or a heightened perceptual capacity. The Exegesis does not "
            "resolve this tension but holds both possibilities in suspension. A secondary "
            "contradiction exists between the fiction (where paranoid characters are often "
            "vindicated) and the Exegesis (where PKD is less certain about his own case)."
        ),
        'editorial_notes': (
            "Researchers should avoid diagnosing PKD and instead focus on how paranoia functions "
            "in his intellectual and creative system. The term 'paranoia' carries clinical weight "
            "that PKD himself was aware of and deliberately played with."
        ),
        'open_questions': json.dumps([
            "Is PKD's fiction best understood as a literary exploration of paranoia or as a paranoid literary form?",
            "How does PKD's treatment of paranoia relate to the political surveillance culture of the 1970s?",
            "Does the Exegesis ultimately distinguish between justified and pathological paranoia, or refuse to?"
        ]),
        'card_description': (
            "Paranoia as theme, structure, and lived experience in PKD's fiction and Exegesis."
        ),
    },

    'TOPIC_PSY_anamnesis': {
        'definition': (
            "Anamnesis (Greek: 'un-forgetting') is PKD's adaptation of the Platonic concept of "
            "recollection — the idea that the soul possesses knowledge from a prior existence "
            "that can be recovered. For PKD, anamnesis becomes the central theoretical framework "
            "for understanding his 2-3-74 experience: the sudden recovery of knowledge that he "
            "interpreted as remembering a deeper or prior reality."
        ),
        'pkd_relevance': (
            "Anamnesis is arguably the single most important concept in the Exegesis. PKD uses it "
            "to explain his experience of suddenly 'remembering' that he was Thomas, a first-century "
            "Christian living in Rome, and that the contemporary world was a simulated overlay on "
            "apostolic reality. The concept allows PKD to frame his experience as philosophically "
            "legitimate (Platonic) rather than pathological (psychotic), and it becomes the "
            "mechanism through which VALIS operates on human consciousness."
        ),
        'in_the_fiction': (
            "Anamnesis appears in PKD's fiction primarily through characters who suddenly recover "
            "lost or suppressed memories, discovering that their known identity is false and that "
            "a deeper identity exists beneath. The VALIS trilogy makes anamnesis explicit: "
            "Horselover Fat's pink light experience is described as an anamnetic event. Earlier "
            "novels like Flow My Tears, the Policeman Said contain proto-anamnetic moments where "
            "characters' realities shift suddenly."
        ),
        'in_the_exegesis': (
            "The Exegesis contains hundreds of passages developing anamnesis as PKD's master "
            "concept. He connects it to Plato's Meno, to Gnostic soteriology, to Christian "
            "theology of the Paraclete, and to his own 2-3-74 experience. PKD theorizes that "
            "anamnesis is triggered by specific stimuli — the golden fish necklace, certain music, "
            "the Nag Hammadi texts — and that it represents not ordinary remembering but the "
            "recovery of divine knowledge suppressed by the Black Iron Prison. The concept evolves "
            "throughout the Exegesis, sometimes treated as Platonic recollection, sometimes as "
            "Gnostic awakening, sometimes as information transfer from VALIS."
        ),
        'intellectual_background': (
            "PKD's anamnesis concept draws primarily on Plato's theory of recollection (Meno, "
            "Phaedo), Gnostic soteriology (the call from the divine that awakens the pneumatic "
            "spark), and Christian theology of the Holy Spirit as reminder. He also connects it to "
            "Jungian concepts of the collective unconscious and to Wordsworth's 'Intimations of "
            "Immortality' ode."
        ),
        'scholarly_debate': (
            "Scholars debate whether PKD's anamnesis is best understood through Platonic, Gnostic, "
            "or psychological frameworks. Kripal and Davis read it as genuine religious experience. "
            "Sutin and Rickman situate it within PKD's mental health history without reducing it "
            "to pathology. Philosophical readings (Wittkower, Sims) examine whether PKD's version "
            "of anamnesis is philosophically coherent or a creative misreading of Plato."
        ),
        'chronology_summary': (
            "Anamnesis becomes central to PKD's thought after 2-3-74 (February-March 1974) and "
            "dominates the Exegesis from 1974 through 1982. Proto-anamnetic themes appear in "
            "earlier fiction but are not explicitly theorized until the Exegesis."
        ),
        'contradictions_summary': (
            "PKD's treatment of anamnesis oscillates between Platonic and Gnostic frameworks. "
            "Under the Platonic reading, anamnesis recovers timeless Forms; under the Gnostic "
            "reading, it recovers a specific suppressed historical reality (apostolic Christianity). "
            "The Exegesis does not settle this tension. Additionally, PKD wavers on whether "
            "anamnesis is available to all humans or only to those with the pneumatic spark."
        ),
        'editorial_notes': (
            "Anamnesis overlaps significantly with Memory, False Memory, and the Hypnagogic State "
            "topics. Researchers should note that PKD's usage departs from Plato's in significant "
            "ways — particularly in its Gnostic and Christological dimensions."
        ),
        'open_questions': json.dumps([
            "Is PKD's anamnesis ultimately Platonic, Gnostic, or a novel synthesis that transcends both?",
            "What triggers anamnesis in PKD's system, and is the triggering mechanism consistent across the Exegesis?",
            "How does PKD's anamnesis concept relate to clinical accounts of recovered memory and dissociative states?",
            "Does VALIS function as the agent of anamnesis, or is anamnesis an independent capacity of the human soul?"
        ]),
        'card_description': (
            "Anamnesis as PKD's master concept: Platonic recollection reframed as divine remembering after 2-3-74."
        ),
    },
}


def main():
    db = sqlite3.connect(str(DB))

    for topic_id, dossier in DOSSIERS.items():
        name = db.execute("SELECT canonical_name FROM study_topics WHERE topic_id = ?",
                          (topic_id,)).fetchone()[0]

        db.execute("""
            UPDATE study_topics SET
                definition = ?,
                pkd_relevance = ?,
                in_the_fiction = ?,
                in_the_exegesis = ?,
                intellectual_background = ?,
                scholarly_debate = ?,
                chronology_summary = ?,
                contradictions_summary = ?,
                editorial_notes = ?,
                open_questions = ?,
                card_description = ?,
                status = 'drafted',
                updated_at = datetime('now')
            WHERE topic_id = ?
        """, (
            dossier['definition'],
            dossier['pkd_relevance'],
            dossier['in_the_fiction'],
            dossier['in_the_exegesis'],
            dossier['intellectual_background'],
            dossier['scholarly_debate'],
            dossier['chronology_summary'],
            dossier['contradictions_summary'],
            dossier['editorial_notes'],
            dossier['open_questions'],
            dossier['card_description'],
            topic_id,
        ))
        db.commit()
        print(f"  Drafted: {name}")
        print(f"    definition: {dossier['definition'][:80]}...")
        print(f"    card: {dossier['card_description'][:80]}...")

    print(f"\n=== {len(DOSSIERS)} DOSSIERS DRAFTED ===")
    db.close()


if __name__ == '__main__':
    main()
