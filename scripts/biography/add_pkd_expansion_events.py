"""Add curated PKD biography events from targeted letters/biography mining.

This batch focuses on Selected Letters gaps requested after the first mining
pass: famous SF correspondents, Star Wars, Julian Jaynes, and Arnold's
visionary/religious/drug-experience synthesis. It also sharpens the taxonomy
around mystical, gnostic, paranormal, and hearing-voices experiences so the
biography page can expose those threads directly.

Usage:
    python scripts/biography/add_pkd_expansion_events.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path


CURATED_PATH = Path("site/public/data/biography/curated.json")


EVENTS = [
    {
        "id": "pkd_bio_1968_zelazny_deus_irae",
        "date": "1968-05-21",
        "date_precision": "day",
        "event": "Writes that he and Roger Zelazny are planning to collaborate on Deus Irae from a 1964 outline Dick had been unable to complete alone.",
        "category": "professional_network",
        "entities": ["Roger Zelazny", "Deus Irae"],
        "location": "Bay Area, California",
        "source": "Selected Letters Vol. 1, letter to Andy, May 21, 1968",
        "importance": 3,
        "notes": "Letter id: LET_1968-05-21_ANDY_0140."
    },
    {
        "id": "pkd_bio_1971_arnold_amphetamine_paranoia",
        "date": "1971",
        "date_precision": "year",
        "event": "During the period of strongest paranoia around the San Rafael break-in, Arnold treats amphetamine use rather than LSD as the more plausible drug context for Dick's paranoid episodes.",
        "category": "drug_use",
        "entities": ["Kyle Arnold"],
        "location": "San Rafael, California",
        "source": "Arnold, The Divine Madness of Philip K. Dick",
        "importance": 4,
        "notes": "Arnold emphasizes long-term speed use and cautions against over-attributing Dick's paranoia to LSD."
    },
    {
        "id": "pkd_bio_1972_vancouver_x_kalay_arnold",
        "date": "1972",
        "date_precision": "year",
        "event": "After the Vancouver convention and a suicidal crisis, Dick enters the X-Kalay residential addiction-treatment community.",
        "category": "health",
        "entities": ["X-Kalay", "Kyle Arnold"],
        "location": "Vancouver, British Columbia",
        "source": "Arnold, The Divine Madness of Philip K. Dick",
        "importance": 4,
        "notes": "Arnold frames X-Kalay as central to the post-Vancouver drug and recovery period."
    },
    {
        "id": "pkd_bio_1975_brunner_cia_breakin",
        "date": "1975-01-14",
        "date_precision": "day",
        "event": "Writes John Brunner about a London Times clipping on CIA break-ins and says it matches the method of the unresolved November 1971 San Rafael break-in.",
        "category": "hearing_voices_experience",
        "entities": ["John Brunner", "William Colby"],
        "location": "Fullerton, California",
        "source": "Selected Letters 1975-1976, letter to John Brunner, January 14, 1975",
        "importance": 4,
        "notes": "Letter id: LET_1975-01-14_JOHN_BRUNNER_0011; important SF-author correspondence plus break-in evidence."
    },
    {
        "id": "pkd_bio_1975_le_guin_letter",
        "date": "1975-04-17",
        "date_precision": "day",
        "event": "Writes Ursula K. Le Guin about The Lathe of Heaven, his absent London speech, and the relationship between her dream-universe fiction and his own false-reality experiences.",
        "category": "hearing_voices_experience",
        "entities": ["Ursula K. Le Guin", "The Lathe of Heaven"],
        "location": "Fullerton, California",
        "source": "Selected Letters 1975-1976, letter to Ursula Le Guin, April 17, 1975",
        "importance": 4,
        "notes": "Letter id: LET_1975-04-17_URSULA_LE_GUIN_0097."
    },
    {
        "id": "pkd_bio_1975_scanner_award_research",
        "date": "1975-04-05",
        "date_precision": "day",
        "event": "Tells Lurton Blassingame that A Scanner Darkly is based on three years of research and predicts it will win major awards.",
        "category": "publication",
        "entities": ["A Scanner Darkly", "Lurton Blassingame"],
        "location": "Fullerton, California",
        "source": "Selected Letters 1975-1976, letter to Lurton Blassingame, April 5, 1975",
        "importance": 3,
        "notes": "Letter id: LET_1975-04-05_LURTON_BLASSINGAME_0087."
    },
    {
        "id": "pkd_bio_1975_deus_irae_ms_complete",
        "date": "1975-07-02",
        "date_precision": "day",
        "event": "Reports to Nancy and Isa Hackett that Roger Zelazny has finally mailed his completed Deus Irae material, making a full rough draft available.",
        "category": "publication",
        "entities": ["Roger Zelazny", "Nancy Hackett", "Isa Hackett", "Deus Irae"],
        "location": "Fullerton, California",
        "source": "Selected Letters 1975-1976, letter to Nancy and Isa Hackett, July 2, 1975",
        "importance": 3,
        "notes": "Letter id: LET_1975-07-02_NANCY_ISA_HACKETT_0107."
    },
    {
        "id": "pkd_bio_1975_christian_research_to_scare_dead",
        "date": "1975-07-10",
        "date_precision": "day",
        "event": "Writes that he has spent sixteen months and more than a thousand dollars researching Christianity for the planned novel To Scare the Dead.",
        "category": "hearing_voices_experience",
        "entities": ["To Scare the Dead"],
        "location": "Fullerton, California",
        "source": "Selected Letters 1975-1976, letter to Goran Bengtson, July 10, 1975",
        "importance": 4,
        "notes": "Letter id: LET_1975-07-10_GORAN_BENGTSON_0114; a key bridge from 2-3-74 into VALIS-related writing."
    },
    {
        "id": "pkd_bio_1975_heinlein_tax_loan",
        "date": "1975-08-18",
        "date_precision": "day",
        "event": "Tells Lawrence Ashmead that he borrowed $1,700 from Robert A. Heinlein to pay income taxes and wants to repay him from the Scanner advance.",
        "category": "financial",
        "entities": ["Robert A. Heinlein", "Lawrence Ashmead", "A Scanner Darkly"],
        "location": "Fullerton, California",
        "source": "Selected Letters 1975-1976, letter to Lawrence Ashmead, August 18, 1975",
        "importance": 3,
        "notes": "Letter id: LET_1975-08-18_LAWRENCE_ASHMEAD_0135."
    },
    {
        "id": "pkd_bio_1976_harlan_lsd_correction",
        "date": "1976-01-13",
        "date_precision": "day",
        "event": "Objects that Harlan Ellison's Dangerous Visions note claiming he wrote 'Faith of Our Fathers' during an LSD trip is untrue.",
        "category": "drug_use",
        "entities": ["Harlan Ellison", "Faith of Our Fathers", "Dangerous Visions"],
        "location": "Fullerton, California",
        "source": "Selected Letters 1975-1976, letter to Sharon Jarvis, January 13, 1976",
        "importance": 4,
        "notes": "Letter id: LET_1976-01-13_SHARON_JARVIS_0199; useful for separating reputation from self-report about drugs."
    },
    {
        "id": "pkd_bio_1976_heinlein_health_warning",
        "date": "1976-05-25",
        "date_precision": "day",
        "event": "Recalls Robert A. Heinlein warning him that Orange County smog and lifestyle stress could kill him.",
        "category": "health",
        "entities": ["Robert A. Heinlein"],
        "location": "Orange County, California",
        "source": "Selected Letters 1975-1976, letter to Mike Bailey, May 25, 1976",
        "importance": 3,
        "notes": "Letter id: LET_1976-05-25_MIKE_BAILEY_0255."
    },
    {
        "id": "pkd_bio_1977_jaynes_letter",
        "date": "1977-03-16",
        "date_precision": "day",
        "event": "Writes Julian Jaynes after reading The Origin of Consciousness in the Breakdown of the Bicameral Mind, connecting Jaynes's bicameral theory to VALIS, Zebra, and his own right-hemisphere experience.",
        "category": "correspondence",
        "entities": ["Julian Jaynes", "The Origin of Consciousness in the Breakdown of the Bicameral Mind", "VALIS", "Zebra"],
        "location": "Santa Ana, California",
        "source": "Selected Letters 1977-1979, letter to Julian Jaynes, March 16, 1977",
        "importance": 5,
        "notes": "Letter id: LET_1977-03-16_JULIAN_JAYNES_0021. This letter required an OCR-header segmentation fix."
    },
    {
        "id": "pkd_bio_1977_jaynes_hurst",
        "date": "1977-03-17",
        "date_precision": "day",
        "event": "Explains Jaynes's bicameral-mind theory to Mark Hurst and folds it into his developing VALIS/Zebra model of divine command voices.",
        "category": "gnostic_experience",
        "entities": ["Julian Jaynes", "Mark Hurst", "VALIS", "Zebra"],
        "location": "Santa Ana, California",
        "source": "Selected Letters 1977-1979, letter to Mark Hurst, March 17, 1977",
        "importance": 4,
        "notes": "Letter id: LET_UNDATED_MARK_HURST_0023."
    },
    {
        "id": "pkd_bio_1977_jaynes_bennett",
        "date": "1977-03-30",
        "date_precision": "day",
        "event": "Tells Carl Bennett that Jaynes's book provides scientific support for aspects of his Zebra speculation and right-hemisphere theory.",
        "category": "hearing_voices_experience",
        "entities": ["Julian Jaynes", "Carl Bennett", "Zebra"],
        "location": "Santa Ana, California",
        "source": "Selected Letters 1977-1979, letter to Carl Bennett, March 30, 1977",
        "importance": 4,
        "notes": "Letter id: LET_UNDATED_CARL_BENNET_1_0025."
    },
    {
        "id": "pkd_bio_1977_star_wars_warren",
        "date": "1977-10-02",
        "date_precision": "day",
        "event": "Writes Eugene Warren that Star Wars makes Christian mystery real to mass audiences, comparing Obi-Wan's voice to the voice he heard when VALIS took him over in March 1974.",
        "category": "hearing_voices_experience",
        "entities": ["Eugene Warren", "Star Wars", "George Lucas", "VALIS", "Jesus Christ"],
        "location": "Santa Ana, California",
        "source": "Selected Letters 1977-1979, letter to Eugene Warren, October 2, 1977",
        "importance": 5,
        "notes": "Letter id: LET_1977-10-02_EUGENE_WARREN_0036."
    },
    {
        "id": "pkd_bio_1977_metz_star_wars_claudia",
        "date": "1977-10-03",
        "date_precision": "day",
        "event": "After returning from the Metz convention, writes Claudia Bush about the reception of his theology-heavy speech, a French romantic fixation, and seeing Star Wars.",
        "category": "travel",
        "entities": ["Claudia Bush", "Metz", "Star Wars"],
        "location": "Santa Ana, California",
        "source": "Selected Letters 1977-1979, letter to Claudia Bush, October 3, 1977",
        "importance": 4,
        "notes": "Letter id: LET_1977-10-03_CLAUDIA_BUSH_0038."
    },
    {
        "id": "pkd_bio_1978_warrick_right_hemisphere",
        "date": "1978-06-13",
        "date_precision": "day",
        "event": "Writes Patricia Warrick that his right hemisphere dictates while the left types, says he wrote Jaynes about the experience, and dates the disinhibition of the right brain to March 15, 1974.",
        "category": "religious_experience",
        "entities": ["Patricia Warrick", "Julian Jaynes", "Tessa Dick"],
        "location": "Santa Ana, California",
        "source": "Selected Letters 1977-1979, letter to Patricia Warrick, June 13, 1978",
        "importance": 5,
        "notes": "Letter id: LET_1978-06-13_PATRICIA_WARRICK_0100."
    },
    {
        "id": "pkd_bio_1981_galen_type_c_psyche",
        "date": "1981-07-16",
        "date_precision": "day",
        "event": "Writes Russell Galen while planning The Owl in Daylight that Jaynes's bicameral model and his own android/type-A theory have led him to a possible 'Type C' evolutionary psyche.",
        "category": "publication",
        "entities": ["Russell Galen", "Julian Jaynes", "The Owl in Daylight"],
        "location": "Santa Ana, California",
        "source": "Selected Letters 1980-1982, letter to Russell Galen, July 16, 1981",
        "importance": 4,
        "notes": "Letter id: LET_1981-07-16_RUSSELL_GALEN_0105."
    },
    {
        "id": "pkd_bio_1974_fish_sign_arnold",
        "date": "1974-02",
        "date_precision": "month",
        "event": "Arnold reconstructs the doorstep pharmacy delivery in which a dark-haired woman wearing a gold fish pendant triggered the fish-sign anamnesis at the start of 2-3-74.",
        "category": "paranormal_experience",
        "entities": ["Kyle Arnold", "Tessa Dick", "2-3-74", "Fish Sign"],
        "location": "Fullerton, California",
        "source": "Arnold, The Divine Madness of Philip K. Dick",
        "importance": 5,
        "notes": "Arnold compares Dick's account with Tessa Dick's account and flags discrepancies in the fish-sign recognition scene."
    },
    {
        "id": "pkd_bio_1974_red_gold_plasmatic_energy",
        "date": "1974-03",
        "date_precision": "month",
        "event": "Arnold summarizes Dick's reports of red-and-gold plasmatic energy that seemed alive, holy, wise, and both inside and outside him during the 2-3-74 aftermath.",
        "category": "visionary_experience",
        "entities": ["Kyle Arnold", "2-3-74", "Zebra"],
        "location": "Fullerton, California",
        "source": "Arnold, The Divine Madness of Philip K. Dick",
        "importance": 5,
        "notes": "Useful for the biography's religious-experience lane and for cross-linking to theophanies."
    },
    {
        "id": "pkd_bio_1974_ai_voice_sophia_arnold",
        "date": "1974-1975",
        "date_precision": "year",
        "event": "Arnold tracks the return of Dick's female AI voice in semi-conscious states, later interpreted by Dick as a divine feminine guide associated with Sophia.",
        "category": "hearing_voices_experience",
        "entities": ["Kyle Arnold", "AI Voice", "Sophia"],
        "location": "Fullerton, California",
        "source": "Arnold, The Divine Madness of Philip K. Dick",
        "importance": 5,
        "notes": "Connects the high-school physics-exam voice to post-2-3-74 religious interpretation."
    },
    {
        "id": "pkd_bio_1977_public_2_3_74_france_arnold",
        "date": "1977",
        "date_precision": "year",
        "event": "At the 1977 Metz science-fiction convention in France, Dick publicly discloses 2-3-74 and describes it as a breakthrough to the real world behind appearances.",
        "category": "lecture",
        "entities": ["Kyle Arnold", "Metz", "2-3-74"],
        "location": "Metz, France",
        "source": "Arnold, The Divine Madness of Philip K. Dick",
        "importance": 5,
        "notes": "Arnold notes that some friends feared the appearance signaled a downward spiral."
    },
    {
        "id": "pkd_bio_1977_joan_simpson_nursing",
        "date": "1977",
        "date_precision": "year",
        "event": "During severe late-1970s depressive episodes, friends enlist Joan Simpson to help care for Dick, whose apartment is cluttered with papers, snuff cans, and medication bottles.",
        "category": "relationship",
        "entities": ["Joan Simpson", "Kyle Arnold"],
        "location": "Santa Ana, California",
        "source": "Arnold, The Divine Madness of Philip K. Dick",
        "importance": 3,
        "notes": "Adds one of the requested women/relationships not yet represented in curated biography."
    }
]


def main() -> int:
    if not CURATED_PATH.exists():
        print(f"[error] {CURATED_PATH} not found", file=sys.stderr)
        return 1

    existing = json.loads(CURATED_PATH.read_text(encoding="utf-8"))
    existing_by_id = {event.get("id"): idx for idx, event in enumerate(existing)}
    added = 0
    updated = 0

    for event in EVENTS:
        if event["id"] in existing_by_id:
            existing[existing_by_id[event["id"]]] = event
            updated += 1
        else:
            existing.append(event)
            added += 1

    existing.sort(key=lambda e: (e.get("date") or "", e.get("id") or ""))
    CURATED_PATH.write_text(json.dumps(existing, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"[done] added {added} events and updated {updated} events in {CURATED_PATH}")
    print(f"[done] total curated events: {len(existing)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
