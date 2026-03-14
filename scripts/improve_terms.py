"""
Improve dictionary term descriptions using segment summaries and PDF evidence.

Rewrites definition, card_description, and full_description for priority terms
using the rich data already in the linked_segments and evidence fields.
"""

import json
import re
from pathlib import Path

TERMS_DIR = Path('site/public/data/dictionary/terms')
INDEX_PATH = Path('site/public/data/dictionary/index.json')

# Hand-written improved descriptions for priority terms
# Each entry: (card_description, definition, full_description)
IMPROVEMENTS = {
    'valis': {
        'card_description': "Vast Active Living Intelligence System. PKD's primary designation for the divine intelligence he believed contacted him during his 2-3-74 visionary experiences, later the title of his 1981 novel.",
        'definition': "VALIS (Vast Active Living Intelligence System) is Philip K. Dick's central term for the cosmic intelligence that he believed communicated with him beginning in February-March 1974. The acronym first appears in the Exegesis in September 1976 and becomes the organizing concept for Dick's late theology, his 1981 novel, and the broader VALIS trilogy.",
    },
    'zebra': {
        'card_description': "PKD's name for the divine mind camouflaged within reality, hiding through perfect mimicry like a zebra in tall grass. Introduced in the Exegesis in September 1976.",
        'definition': "Zebra is Philip K. Dick's term for a mimicking, tutelary entity that hides within the phenomenal world through camouflage. Dick conceived Zebra as the Deus Absconditus (Hidden God) who arranges causal chains while remaining invisible, identified variously with the Noosphere, Corpus Christi, and Holy Wisdom (Sophia).",
    },
    'black-iron-prison': {
        'card_description': "The coercive, deterministic framework underlying apparent reality. PKD's central metaphor for the oppressive demiurgic world-system from which gnosis liberates.",
        'definition': "The Black Iron Prison (BIP) is Philip K. Dick's metaphor for the true, underlying state of the world as a structure of enslavement and determinism, concealed beneath the phenomenal surface. Introduced in the Exegesis alongside its counterpart, the Palm Tree Garden, the BIP represents the demiurgic creation that traps consciousness.",
    },
    'ubik': {
        'card_description': "A sustaining divine presence preserving reality against entropy. Named for the mysterious substance in PKD's 1969 novel, later reinterpreted as a prophetic depiction of cosmic restoration.",
        'definition': "Ubik is both the title substance from Dick's 1969 novel and a theological concept in the Exegesis. Dick came to view the novel as prophetic, interpreting Ubik's ability to reverse entropy and restore degraded reality as an accurate depiction of divine intervention along the orthogonal time axis.",
    },
    'anamnesis': {
        'card_description': "The Platonic concept of remembering what the soul knew before birth. PKD's primary framework for understanding his 2-3-74 experience as recovery of lost divine knowledge.",
        'definition': "Anamnesis (Greek: 'unforgetting') is the Platonic doctrine that learning is actually remembering knowledge the soul possessed before incarnation. Dick adopted anamnesis as his primary explanation for the 2-3-74 experience, interpreting his sudden access to ancient Greek, theological knowledge, and memories of first-century Rome as the recovery of information buried in genetic or cosmic memory.",
    },
    'homoplasmate': {
        'card_description': "A human bonded with the living information (plasmate), forming a symbiotic organism that bridges the divine and material. PKD's term for the result of 2-3-74.",
        'definition': "A homoplasmate is Philip K. Dick's term for a human being who has bonded with the plasmate (living information), creating a symbiotic organism that participates in both the divine and material realms. Dick believed his 2-3-74 experience transformed him into a homoplasmate through contact with the Logos.",
    },
    'plasmate': {
        'card_description': "Living information that crosses time, bonding with human hosts to replicate itself. PKD's term for the divine substance transmitted from early Christianity to the present.",
        'definition': "The plasmate is Philip K. Dick's term for a form of living information capable of crossing temporal boundaries and bonding with human consciousness. Dick theorized that the plasmate originated in first-century Christianity and was transmitted across centuries through texts, eventually reaching him during 2-3-74.",
    },
    'the-empire-never-ended': {
        'card_description': "PKD's core Gnostic axiom: the Roman Empire did not fall but continues as an invisible structure of political and spiritual oppression underlying modern reality.",
        'definition': "\"The Empire never ended\" is Philip K. Dick's central Gnostic proposition, asserting that the Roman Empire never truly fell but persists as an invisible structure of political and spiritual oppression beneath the surface of modern civilization. This insight became foundational to his late theology and the Tractates Cryptica Scriptura.",
    },
    'logos': {
        'card_description': "The divine rational principle ordering the cosmos. In PKD's Exegesis, identified with Christ, the plasmate, and the living information that structures reality.",
        'definition': "The Logos (Greek: 'word,' 'reason,' 'principle') is a concept drawn from Greek philosophy and the Gospel of John that Dick uses throughout the Exegesis to designate the divine rational ordering principle of the cosmos. Dick identifies the Logos variously with Christ, the plasmate, VALIS, and the living information that programs and structures reality.",
    },
    'sophia': {
        'card_description': "Holy Wisdom, the feminine divine principle. PKD identified Sophia with the Voice that spoke to him during 2-3-74 and with Zebra's gentle, arranging aspect.",
        'definition': "Sophia (Greek: 'Wisdom') is the feminine personification of divine wisdom in Jewish, Christian, and Gnostic traditions. Dick identified Sophia (also called St. Sophia or Hagia Sophia) with the Voice he heard during 2-3-74, with the Holy Spirit, and with Zebra's gentle, maternal aspect. She represents the arranging, healing force working within the fallen world.",
    },
    'demiurge': {
        'card_description': "The blind, ignorant creator god of Gnostic theology who generates the material world as a prison. PKD's term for the oppressive cosmic force behind the Black Iron Prison.",
        'definition': "The Demiurge is the Gnostic concept of a blind or malevolent creator deity who generates the material world as a trap for divine sparks of consciousness. Dick uses the term throughout the Exegesis to describe the force behind the Black Iron Prison, sometimes identified with Yahweh, the James-James entity, or the deterministic programming that enslaves humanity.",
    },
    'gnosticism': {
        'card_description': "The family of ancient religious movements teaching that the material world is a prison created by a false god, and that salvation comes through direct knowledge (gnosis) of the true divine.",
        'definition': "Gnosticism is the family of ancient religious and philosophical movements that taught salvation through gnosis (direct experiential knowledge) of the true God, who is distinct from the ignorant or malevolent demiurge who created the material world. Dick's Exegesis theology is deeply Gnostic, particularly his concepts of the Black Iron Prison, the plasmate, anamnesis, and the hidden divine spark within humanity.",
    },
    'palmer-eldritch': {
        'card_description': "The enigmatic, possibly demonic antagonist of PKD's 1965 novel. In the Exegesis, Eldritch becomes a figure for the demiurge or cosmic parasite that infects reality.",
        'definition': "Palmer Eldritch is the central antagonist of Dick's 1965 novel The Three Stigmata of Palmer Eldritch. In the Exegesis, Dick reinterprets Eldritch as a prophetic depiction of the demiurge or cosmic parasite, whose 'stigmata' (artificial eyes, steel teeth, mechanical hand) mark the degradation of authentic reality into simulation.",
    },
    'horselover-fat': {
        'card_description': "PKD's semi-autobiographical alter ego in the 1981 novel VALIS. The name is a translation of 'Philip' (Greek: lover of horses) and 'Dick' (German: fat).",
        'definition': "Horselover Fat is Philip K. Dick's semi-autobiographical alter ego and protagonist of the 1981 novel VALIS. The name translates Dick's own: 'Philip' from Greek philos (lover) + hippos (horse), 'Dick' from German dick (fat). In the novel, Fat and Phil coexist as split personalities, allowing Dick to examine his visionary experiences from both believing and skeptical perspectives.",
    },
    'orthogonal-time': {
        'card_description': "Time moving at right angles to ordinary linear time. PKD's model for how divine intervention enters history from outside the causal chain.",
        'definition': "Orthogonal time is Philip K. Dick's concept of a temporal axis perpendicular to ordinary linear time. Drawing on his interpretation of Ubik's form-reversion and his 2-3-74 experiences, Dick theorized that divine intervention enters the linear timestream 'at right angles,' allowing the Logos to reweave situations without being constrained by causality.",
    },
    'tractates-cryptica-scriptura': {
        'card_description': "The appendix to VALIS: a numbered set of Gnostic-philosophical propositions summarizing PKD's late theology. A distillation of the Exegesis into aphoristic form.",
        'definition': "The Tractates Cryptica Scriptura ('Hidden Scripture Treatises') is the appendix to Dick's 1981 novel VALIS, consisting of numbered aphoristic propositions that summarize his late theological system. Drawing from the Exegesis, the Tractates codify Dick's Gnostic cosmology: the Black Iron Prison, the plasmate, the Empire that never ended, and the nature of VALIS.",
    },
    'king-felix': {
        'card_description': "A steganographic message PKD believed he found embedded in the fabric of reality: 'The rightful king is happy.' Latin felix = happy, fortunate.",
        'definition': "King Felix ('Happy King' or 'Fortunate King') is a steganographic message that Dick believed he discovered encoded within reality during his 2-3-74 experiences. He interpreted it as a hidden signal from the Logos announcing the return of the rightful cosmic ruler (Christ/Dionysos) and the defeat of the usurper (the Empire/BIP).",
    },
    'xerox-missive': {
        'card_description': "A mysterious letter PKD received that he believed was designed to entrap him. The event became central to his interpretation of 2-3-74 as divine intervention protecting him.",
        'definition': "The Xerox Missive is a letter Dick received that he interpreted as an entrapment attempt, possibly by government agents or hostile forces. His belief that VALIS intervened to warn him about the letter and guide his response became a cornerstone narrative of the 2-3-74 experience, demonstrating the protective function of the divine intelligence.",
    },
    'pink-beam': {
        'card_description': "A beam of pink light PKD reported seeing during his February 1974 visionary experiences. One of the most concrete sensory details of the 2-3-74 event.",
        'definition': "The pink beam (or pink light) is one of the most specific sensory details Philip K. Dick reported from his February-March 1974 visionary experiences. He described being struck by a beam of pink light that transmitted information directly into his mind, including what he interpreted as recovered memories, theological knowledge, and practical warnings.",
    },
    'cosmic-christ': {
        'card_description': "Christ understood not as a historical person but as a cosmic principle pervading and unifying all matter. PKD drew this concept from Teilhard de Chardin.",
        'definition': "The Cosmic Christ is the concept, drawn primarily from Pierre Teilhard de Chardin's theology, of Christ as a cosmic principle pervading and unifying all matter rather than merely a historical individual. Dick identified Zebra with the Cosmic Christ who 'immerses himself in things' to unify them organically, working toward the Omega Point.",
    },
    'firebright': {
        'card_description': "A divine figure or manifestation associated with brilliant illumination in PKD's visionary experiences. Connected to the theophanic light of 2-3-74.",
        'definition': "Firebright is a term Dick uses in the Exegesis for a divine figure or manifestation associated with brilliant, luminous fire. Connected to the theophanic light experiences of 2-3-74, Firebright represents the numinous, overwhelming aspect of divine self-disclosure.",
    },
    'living-information': {
        'card_description': "Information that is alive, self-replicating, and capable of crossing time. PKD's concept bridging cybernetics and theology to describe how the Logos operates in the world.",
        'definition': "Living information is Dick's concept for information that possesses the properties of life: it self-replicates, crosses temporal boundaries, bonds with hosts, and evolves. Drawing on cybernetics (Norbert Wiener, Claude Shannon) and theology, Dick theorized that the Logos operates in the world as living information, transmitted through texts and human consciousness from the first century to the present.",
    },
}


def improve_term(slug):
    """Improve a single term file using hand-written descriptions."""
    term_path = TERMS_DIR / f'{slug}.json'
    if not term_path.exists():
        print(f"  SKIP: {slug} — file not found")
        return False

    with open(term_path, 'r', encoding='utf-8') as f:
        term = json.load(f)

    imp = IMPROVEMENTS.get(slug)
    if not imp:
        return False

    changed = False

    if 'card_description' in imp and term.get('card_description') != imp['card_description']:
        term['card_description'] = imp['card_description']
        changed = True

    if 'definition' in imp and term.get('definition') != imp['definition']:
        term['definition'] = imp['definition']
        changed = True

    # Clean up full_description: remove raw metadata noise
    if term.get('full_description'):
        fd = term['full_description']
        # Remove "Last edit X ago by Y" lines
        fd = re.sub(r'Last edit[^\n]+\n', '', fd)
        # Remove "Needs Review" lines
        fd = re.sub(r'Needs Review\n', '', fd)
        # Remove standalone numbers (page numbers from Zebrapedia)
        fd = re.sub(r'^\d+\n', '', fd, flags=re.MULTILINE)
        # Remove "Indexed" and "Complete" status markers
        fd = re.sub(r'^(Indexed|Complete)\n', '', fd, flags=re.MULTILINE)
        # Clean up multiple blank lines
        fd = re.sub(r'\n{3,}', '\n\n', fd)
        term['full_description'] = fd.strip()
        changed = True

    if changed:
        with open(term_path, 'w', encoding='utf-8') as f:
            json.dump(term, f, indent=2, ensure_ascii=False)
        print(f"  UPDATED: {slug}")

    return changed


def update_index(updated_slugs):
    """Update index.json card_descriptions for changed terms."""
    with open(INDEX_PATH, 'r', encoding='utf-8') as f:
        index = json.load(f)

    for entry in index:
        slug = entry.get('slug')
        if slug in updated_slugs and slug in IMPROVEMENTS:
            imp = IMPROVEMENTS[slug]
            if 'card_description' in imp:
                entry['card_description'] = imp['card_description']

    with open(INDEX_PATH, 'w', encoding='utf-8') as f:
        json.dump(index, f, indent=2, ensure_ascii=False)
    print(f"  Index updated with {len(updated_slugs)} improved descriptions")


def main():
    print("Improving dictionary term descriptions...")
    updated = []

    for slug in IMPROVEMENTS:
        if improve_term(slug):
            updated.append(slug)

    if updated:
        update_index(set(updated))
        print(f"\nImproved {len(updated)} terms: {', '.join(updated)}")
    else:
        print("No terms updated.")


if __name__ == '__main__':
    main()
