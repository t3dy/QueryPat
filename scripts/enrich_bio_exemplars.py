#!/usr/bin/env python3
"""Apply the enriched biography entry template (see
Documentation/BIOGRAPHY_AND_EXEGESIS_WORKS_METHOD.md §A.2) to exemplar 2-3-74
entries. Updates in place by id; safe JSON round-trip. Idempotent."""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(ROOT, "site", "public", "data", "biography", "curated.json")

ENRICH = {
    "pkd_bio_1974_02_03_pink_light": {
        "event": "A delivery woman's golden fish pendant triggers the recollection PKD would call the onset of 2-3-74.",
        "narrative": (
            "In late February 1974, recovering at his Fullerton apartment from an impacted-wisdom-tooth "
            "extraction and the sodium pentothal and pain medication that followed, PKD answered the door to a "
            "young woman delivering analgesics. She wore a necklace bearing the golden fish sign — the ichthys, "
            "the secret emblem of the early Christians. PKD reports that the pendant's glint set off a sudden "
            "anamnesis: a conviction that he was himself a covert early Christian and that the Fullerton around "
            "him was, at some level, first-century Rome. Over the following weeks came the experiences he "
            "grouped under the shorthand 2-3-74 — the pink light, the flood of what he took to be transmitted "
            "information, the sense of an intelligence he later named Zebra, VALIS, or the Holy Spirit.\n\n"
            "The scene is the hinge of PKD's last eight years and of the Exegesis he began writing to explain it. "
            "It is also where the accounts diverge most sharply. PKD's own framing shifts between revelation and "
            "self-suspicion across the notebooks; Sutin and Arnold reconstruct the episode from his letters and "
            "from Tessa Dick's recollection, which does not match his in every detail; and the whole sequence sits "
            "on the standing question the portal keeps open — mystical disclosure or the onset of a psychological "
            "episode on a compromised neurochemical baseline. He dramatized it, barely fictionalized, as the "
            "opening of VALIS."
        ),
        "sources": [
            {"author": "Sutin", "work": "Divine Invasions", "lane": "C", "locator": "ch. 8",
             "supports": "dates the fish-pendant delivery to Feb 1974 and the pink-light onset that followed"},
            {"author": "Arnold", "work": "The Divine Madness of Philip K. Dick", "lane": "C", "locator": "ch. 1",
             "supports": "reconstructs the recognition scene and flags where Tessa Dick's account differs"},
            {"author": "PKD", "work": "Exegesis", "lane": "B",
             "supports": "PKD's own later theological reading of the golden fish as the trigger of anamnesis"},
            {"author": "PKD", "work": "VALIS", "lane": "A",
             "supports": "the episode is dramatized, barely fictionalized, as the novel's opening"},
        ],
        "lanes": ["A", "B", "C"],
        "quotes": [
            {"text": "The golden fish necklace told me it was time; I began my work, like the worm constructing its cocoon.",
             "speaker": "PKD", "source": "Exegesis", "lane": "B"},
            {"text": "And the fish sign I saw was made of gold. And I saw around me a prison, a magnet-like ring, of iron.",
             "speaker": "PKD", "source": "Exegesis", "lane": "B"},
        ],
        "dispute": {
            "summary": "Both the factual detail of the encounter and its meaning are contested.",
            "positions": [
                {"who": "PKD (Exegesis, letters)", "claim": "the golden fish pendant triggered a genuine anamnesis — recovered knowledge of a hidden reality"},
                {"who": "Tessa Dick (per Arnold)", "claim": "recalls the encounter differently; the recognition was less immediate and dramatic than PKD's retellings make it"},
                {"who": "Clinical frame (Arnold)", "claim": "the onset is legible as a psychological episode against an amphetamine and post-anesthetic baseline, not a disclosure"},
            ],
        },
        "links": {
            "people": ["/dictionary/tessa"],
            "works": ["/works/the-valis-trilogy"],
            "exegesis_work": "/exegesis/works/valis",
        },
        "confidence": "high",
        "notes": "Event well attested; the identity/immediacy of the recognition and its interpretation are on the standing contradiction registry.",
    },
    "pkd_bio_1974_03_son_diagnosis": {
        "event": "PKD insists his infant son has an undiagnosed hernia; the diagnosis is confirmed and surgically corrected.",
        "narrative": (
            "In March 1974, during the flood of 2-3-74, PKD became convinced that his infant son Christopher had a "
            "birth defect that had gone undiagnosed — a right inguinal hernia. He attributed the knowledge to the "
            "same informing intelligence behind the visions. He pressed Tessa to take the boy to the doctor; on "
            "examination the hernia was confirmed and repaired surgically.\n\n"
            "This is the most frequently cited of the 2-3-74 events because, unlike the pink light or the visions of "
            "Rome, it appears to have an external, medical corroboration: a specific claim that turned out to be "
            "true. PKD returned to it for the rest of his life as evidence that the experience delivered real "
            "information. The portal records the medical fact as well attested while leaving the causal reading "
            "open — a father's anxious, close attention to his child is not the same kind of claim as divine "
            "transmission, and the sources read the same corroborated outcome in incompatible ways."
        ),
        "sources": [
            {"author": "Sutin", "work": "Divine Invasions", "lane": "C", "locator": "ch. 8",
             "supports": "reports PKD's insistence on the undiagnosed hernia and its surgical confirmation"},
            {"author": "Arnold", "work": "The Divine Madness of Philip K. Dick", "lane": "C", "locator": "ch. 1",
             "supports": "treats the episode within a clinical multi-causal frame rather than as veridical revelation"},
            {"author": "PKD", "work": "How to Build a Universe That Doesn't Fall Apart", "lane": "E",
             "supports": "PKD recounts the diagnosis as evidence the experience conveyed real information"},
        ],
        "lanes": ["C", "E"],
        "dispute": {
            "summary": "The medical outcome is not in dispute; its cause is.",
            "positions": [
                {"who": "PKD (interviews, Exegesis)", "claim": "the diagnosis proves the 2-3-74 intelligence delivered veridical, otherwise-unavailable information"},
                {"who": "Clinical frame (Arnold)", "claim": "an attentive, anxious parent noticing a real symptom is a sufficient and more parsimonious explanation"},
            ],
        },
        "links": {
            "people": ["/dictionary/tessa"],
            "exegesis_work": "/exegesis/works/valis",
        },
        "confidence": "high",
        "notes": "Medical fact well attested; the veridical-information interpretation is contested and sits on the contradiction registry.",
    },
    "pkd_bio_1974_02_visions_rome": {
        "event": "PKD sees Fullerton overlaid with first-century Rome — the anamnesis he reads as the abolition of time.",
        "narrative": (
            "Through the weeks of 3-74, PKD reports perceiving his Fullerton surroundings as the Rome of Christ's "
            "time — himself a persecuted member of a secret Christian underground, the police and the state its "
            "hostile agents, the fish sign the mark of his covert society. He is emphatic in the Exegesis that this "
            "was neither reincarnation nor time-travel: the intervening centuries had not been crossed but "
            "abolished. Time itself, he decides, had briefly withdrawn, exposing an eternal form the present merely "
            "veils. This is the germ of the formula VALIS would make famous — \"the Empire never ended\" — and of "
            "his conviction that we live in apostolic time without knowing it.\n\n"
            "He kept revising the mechanism. Early on he describes a superimposition of Rome onto Fullerton; later "
            "he prefers the image from Ubik — the accidental surface \"melting away\" to disclose the Platonic form "
            "beneath. The experience carried a political charge he did not hide: he dates the lifting of the felt "
            "oppression to the summer of 1974, tying his private Rome to Watergate and Nixon's fall. Whether this is "
            "revelation, a temporal-lobe event, or amphetamine-era ideation is exactly the question the portal keeps "
            "open."
        ),
        "sources": [
            {"author": "PKD", "work": "Exegesis", "lane": "B",
             "supports": "extended first-person account of Fullerton-as-Rome and the abolition of time"},
            {"author": "PKD", "work": "VALIS / Radio Free Albemuth", "lane": "A",
             "supports": "the anamnesis is fictionalized; source of the refrain 'the Empire never ended'"},
            {"author": "Sutin", "work": "Divine Invasions", "lane": "C", "locator": "ch. 8",
             "supports": "situates the Rome visions within the 3-74 sequence"},
            {"author": "Arnold", "work": "The Divine Madness of Philip K. Dick", "lane": "C", "locator": "ch. 1",
             "supports": "reads the experience through a clinical, temporal-lobe-inflected frame"},
        ],
        "lanes": ["A", "B", "C"],
        "quotes": [
            {"text": "It made Rome Fullerton and Fullerton Rome; it made 45 AD 1974 AD and 1974 AD 45 AD.",
             "speaker": "PKD", "source": "Exegesis", "lane": "B"},
            {"text": "The accidentals melted away, and the Platonic form ROME became visible to me: it was already there, but disguised.",
             "speaker": "PKD", "source": "Exegesis", "lane": "B"},
        ],
        "dispute": {
            "summary": "PKD rejects the obvious readings; the sources disagree on what remains.",
            "positions": [
                {"who": "PKD (Exegesis)", "claim": "not reincarnation or time-travel but the abolition of time — the Parousia, God entering time from eternity"},
                {"who": "Clinical frame (Arnold)", "claim": "a temporal-lobe or psychological episode on an amphetamine-era baseline"},
            ],
        },
        "links": {
            "works": ["/works/the-valis-trilogy"],
            "exegesis_work": "/exegesis/works/valis",
        },
        "confidence": "high",
        "notes": "PKD's own account is extensive; every interpretation of it (his included) is contested and on the standing registry.",
    },
}


def main():
    data = json.load(open(PATH, encoding="utf-8"))
    by_id = {e["id"]: e for e in data}
    updated = []
    for eid, patch in ENRICH.items():
        if eid not in by_id:
            print(f"  WARN: {eid} not found")
            continue
        by_id[eid].update(patch)
        updated.append(eid)
    json.dump(data, open(PATH, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print(f"Enriched {len(updated)} entries: {', '.join(updated)}")


if __name__ == "__main__":
    main()
