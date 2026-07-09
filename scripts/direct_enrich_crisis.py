#!/usr/bin/env python3
"""Direct (non-subagent) enrichment of the pivotal 1971-72 crisis entries,
following Documentation/BIOGRAPHY_AND_EXEGESIS_WORKS_METHOD.md. No fabricated
Exegesis quotes (none clean for these events); paraphrase+cite + dispute-
surfacing. Applies by id to curated.json. Idempotent."""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(ROOT, "site", "public", "data", "biography", "curated.json")

ENRICH = {
    "pkd_bio_1971_burglary": {
        "date": "1971-11-17",
        "date_precision": "day",
        "event": "PKD's San Rafael house is broken into and his files blown open — the never-resolved event he theorized about for years.",
        "narrative": (
            "On 17 November 1971, PKD returned to his San Rafael house to find it burglarized: the window blown in, "
            "his locked file cabinet forced open (some accounts say blown apart with explosives), and papers and "
            "stereo equipment taken. No one was ever charged. The break-in became the defining unsolved event of "
            "his life — a real intrusion he spent years trying to explain, and a rehearsal for the epistemology of "
            "2-3-74: how do you know what happened when every account, including your own, is unreliable?\n\n"
            "PKD's theories multiplied over time. At various points he blamed the FBI, the CIA, the KGB, the "
            "right-wing Minutemen, the Black Panthers, religious fanatics, local drug dealers, jealous rivals, and — "
            "at his most candid — himself, in a blackout or as a cry for help. Both his own accounts and the "
            "scholarship treat the case as genuinely open; it is one of the portal's standing contradiction zones."
        ),
        "sources": [
            {"author": "Sutin", "work": "Divine Invasions", "lane": "C", "locator": "ch. 7",
             "supports": "dates and describes the Nov 1971 break-in and its unresolved status"},
            {"author": "Arnold", "work": "The Divine Madness of Philip K. Dick", "lane": "C", "locator": "ch. 1",
             "supports": "weighs the possibility that PKD staged or imagined part of it within a clinical frame"},
            {"author": "PKD", "work": "Selected Letters / Exegesis", "lane": "E",
             "supports": "PKD's own shifting attributions of responsibility across letters and notebooks"},
        ],
        "lanes": ["C", "E"],
        "dispute": {
            "summary": "Who broke in, and whether it happened as PKD described, has never been resolved; PKD himself named many culprits.",
            "positions": [
                {"who": "PKD (various letters)", "claim": "an external agency (variously FBI/CIA/KGB/Minutemen/dealers) targeted him"},
                {"who": "PKD (at his most candid)", "claim": "he may have done it himself, in a blackout or as a cry for help"},
                {"who": "Clinical frame (Arnold)", "claim": "the event is entangled with amphetamine-era paranoia; parts may be misremembered or self-inflicted"},
            ],
        },
        "links": {"exegesis_work": "/exegesis/works/flow-my-tears-the-policeman-said"},
        "confidence": "medium",
        "notes": "On the standing contradiction registry. The break-in is corroborated as an event; its agent and exact mechanics are not.",
    },
    "pkd_bio_1972_vancouver_suicide_attempt": {
        "date": "1972-03",
        "date_precision": "month",
        "event": "In Vancouver, PKD attempts suicide and enters the X-Kalay drug-rehabilitation community — the low point that pivoted him to Orange County.",
        "narrative": (
            "PKD had flown to Vancouver in February 1972 as guest of honor at a science-fiction convention, where he "
            "delivered the address \"The Android and the Human,\" and then decided to stay in Canada. The plan "
            "collapsed. In March, isolated and despairing after a relationship ended, he attempted suicide and "
            "afterward checked himself into X-Kalay, a Synanon-style heroin-rehabilitation community — an odd "
            "placement for a man whose problem was amphetamines and depression rather than heroin.\n\n"
            "The Vancouver months were the hinge of his life: from X-Kalay he flew in April to Fullerton, in "
            "Orange County, where he would meet Tessa Busby, resume writing after a long hiatus, and undergo 2-3-74 "
            "two years later. The specific drugs and method of the attempt are described incompatibly by different "
            "participants, so the portal records the sequence and leaves the pharmacological detail open."
        ),
        "sources": [
            {"author": "Sutin", "work": "Divine Invasions", "lane": "C", "locator": "ch. 7",
             "supports": "the Vancouver convention, the suicide attempt, X-Kalay, and the move to Fullerton"},
            {"author": "In Pursuit of VALIS (ed. Sutin)", "work": "chronology", "lane": "C",
             "supports": "dates: Feb 1972 Vancouver; March suicide attempt / X-Kalay; April Fullerton"},
            {"author": "Arnold", "work": "The Divine Madness of Philip K. Dick", "lane": "C", "locator": "ch. 1",
             "supports": "reads the episode within the depression/amphetamine-withdrawal frame"},
        ],
        "lanes": ["C", "D"],
        "dispute": {
            "summary": "The drugs involved and the method of the attempt are reported incompatibly across sources.",
            "positions": [
                {"who": "Various participant accounts", "claim": "differ on the substances and the exact means of the attempt"},
                {"who": "Portal synthesis", "claim": "records the attested sequence (attempt → X-Kalay → Fullerton) and leaves the contested detail open"},
            ],
        },
        "links": {"exegesis_work": "/exegesis/works/a-scanner-darkly"},
        "confidence": "high",
        "notes": "The sequence is well attested; the pharmacological specifics are on the standing registry.",
    },
    "pkd_bio_1971_hospitalization": {
        "date": "1971",
        "date_precision": "year",
        "event": "PKD cycles through hospitalizations and psychiatric contact as amphetamine use, paranoia, and a collapsing household converge.",
        "narrative": (
            "By 1971 PKD's San Rafael house had become a chaotic way-station for street people and drug users, his "
            "marriage to Nancy had ended (she left with their daughter Isa in 1970), and heavy amphetamine use had "
            "fed a deepening paranoia. Across this period he had repeated medical and psychiatric contact — including "
            "hospitalization — as depression, physical collapse, and the fear of surveillance closed in. It was the "
            "year of the break-in and the immediate prelude to Vancouver.\n\n"
            "Scholarship divides on how to weight the causes. Sutin narrates a life coming apart under drugs and "
            "circumstance; Arnold, a clinician, reads a genuine psychiatric crisis with a multi-causal etiology "
            "rather than a simple drug story. The portal keeps both frames rather than resolving them."
        ),
        "sources": [
            {"author": "Sutin", "work": "Divine Invasions", "lane": "C", "locator": "ch. 7",
             "supports": "the 1970-71 disintegration: Nancy's departure, the household, the drug use"},
            {"author": "Arnold", "work": "The Divine Madness of Philip K. Dick", "lane": "C", "locator": "ch. 1",
             "supports": "the clinical, multi-causal reading of the 1971 crisis"},
        ],
        "lanes": ["C", "D"],
        "confidence": "medium",
        "notes": "Dates within 1971 are approximate; the clinical-vs-circumstantial weighting is contested.",
    },
}


def main():
    data = json.load(open(PATH, encoding="utf-8"))
    by_id = {}
    for e in data:
        by_id.setdefault(e["id"], e)
    done = []
    for eid, patch in ENRICH.items():
        if eid in by_id:
            by_id[eid].update(patch)
            done.append(eid)
        else:
            print(f"  WARN: {eid} not found")
    json.dump(data, open(PATH, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    n = sum(1 for e in data if e.get("narrative"))
    print(f"Enriched {len(done)} crisis entries: {', '.join(done)}")
    print(f"Total enriched entries now: {n} / {len(data)}")


if __name__ == "__main__":
    main()
