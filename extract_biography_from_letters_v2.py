#!/usr/bin/env python3
"""
Extract biographical events from PKD Selected Letters (1972-1973) - Version 2
Enhanced with more detailed pattern matching and full letter text scanning
"""

import json
import re
from datetime import datetime
from collections import defaultdict
from typing import List, Dict, Tuple, Optional

# Load source data
with open(r"C:\QueryPat\selected_letters_analysis.json", "r", encoding="utf-8") as f:
    letters_data = json.load(f)

with open(r"C:\QueryPat\site\public\data\biography\curated.json", "r", encoding="utf-8") as f:
    existing_bio = json.load(f)

# Create set of existing event IDs to avoid duplicates
existing_ids = {event.get("id") for event in existing_bio}

print(f"Loaded {len(letters_data)} letters and {len(existing_bio)} existing biography events\n")

# Parse date utilities
def parse_date(date_str: str, default_year: int = 1973) -> Tuple[Optional[str], str]:
    """Parse letter date and return (iso_date, precision)"""
    if not date_str or date_str.strip() == "":
        return None, "unknown"

    date_str = date_str.strip()
    date_str = re.sub(r'\s+', ' ', date_str)

    # Full date: "December 1, 1972"
    match = re.search(r'(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{1,2}),?\s+(\d{4})', date_str, re.IGNORECASE)
    if match:
        month_str, day_str, year_str = match.groups()
        month_map = {m.lower(): i+1 for i, m in enumerate(['January', 'February', 'March', 'April', 'May', 'June',
                                                    'July', 'August', 'September', 'October', 'November', 'December'])}
        month = month_map.get(month_str.lower(), 1)
        day = int(day_str)
        year = int(year_str)
        iso_date = f"{year:04d}-{month:02d}-{day:02d}"
        return iso_date, "day"

    # Month-Year
    match = re.search(r'(January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+(\d{4})', date_str, re.IGNORECASE)
    if match:
        month_str, year_str = match.groups()
        month_map = {
            'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6,
            'july': 7, 'august': 8, 'september': 9, 'october': 10, 'november': 11, 'december': 12,
            'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'jun': 6,
            'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12
        }
        month = month_map.get(month_str.lower(), 1)
        year = int(year_str)
        iso_date = f"{year:04d}-{month:02d}-01"
        return iso_date, "month"

    # Year only
    match = re.search(r'(\d{4})', date_str)
    if match:
        year = int(match.group(1))
        iso_date = f"{year:04d}-01-01"
        return iso_date, "year"

    return None, "unknown"

# Collect all events
bio_events = []
event_ids_local = set(existing_ids)

def add_event(event_dict: Dict) -> bool:
    """Add event if not duplicate; return True if added"""
    if event_dict.get("id") in event_ids_local:
        return False
    bio_events.append(event_dict)
    event_ids_local.add(event_dict.get("id"))
    return True

# Process letters with detailed scanning
for i, letter in enumerate(letters_data):
    letter_id = letter.get("letter_id", f"LETTER_{i}")
    date_str = letter.get("date", "").strip()
    summary = letter.get("summary", "").strip()
    recipient = letter.get("recipient", "").strip()

    iso_date, precision = parse_date(date_str)

    # Extract year from date
    year_match = re.search(r'\d{4}', date_str)
    letter_year = int(year_match.group(0)) if year_match else 1973

    # 1. Christopher birth event
    if "christopher" in summary.lower() and ("born" in summary.lower() or "baby" in summary.lower()):
        # Check for specific birth date
        birth_date = iso_date
        birth_precision = precision

        # Look for July 25 reference
        if "july 25" in summary.lower():
            birth_date = "1973-07-25"
            birth_precision = "day"
        elif "july" in summary.lower() and letter_year == 1973:
            birth_date = "1973-07-01"
            birth_precision = "month"
        elif "born" in summary.lower() and letter_year == 1973:
            birth_date = "1973-07-01"
            birth_precision = "month"

        if add_event({
            "id": "pkd_bio_1973_christopher_birth",
            "date": birth_date or "1973-07-25",
            "date_precision": birth_precision,
            "event": "Birth of son Christopher to Philip K. Dick and wife Tessa",
            "category": "birth",
            "entities": ["Christopher Dick", "Tessa Busby Dick"],
            "location": "Fullerton, California",
            "source": "letters",
            "importance": 4,
            "notes": f"Source: {letter_id} to {recipient.strip()}. Multiple letters confirm July 1973 birth, likely July 25. Letter Sept 5, 1973 states 'just a month ago' confirming late July date."
        }):
            pass

    # 2. Marriage to Tessa
    if "tessa" in summary.lower() and ("married" in summary.lower() or "wife" in summary.lower()) and "1973" in date_str:
        if "april" in date_str.lower() or ("april" in summary.lower() and "married" in summary.lower()):
            if add_event({
                "id": "pkd_bio_1973_marriage_tessa",
                "date": "1973-04-19",
                "date_precision": "day",
                "event": "Married Tessa Busby",
                "category": "family",
                "entities": ["Tessa Busby"],
                "location": "California",
                "source": "letters",
                "importance": 4,
                "notes": f"Source: Letters April 1973. Letter to Sherry Gottlieb (April 19, 1973) states 'we received Locus and saw that we are supposed to get married this week. So we did.'"
            }):
                pass

    # 3. Vancouver episode events
    if "vancouver" in summary.lower():
        # 3a. Arrival with stolen knife
        if "knife" in summary.lower() and "arriving" in summary.lower():
            if add_event({
                "id": "pkd_bio_1972_vancouver_arrival_knife",
                "date": "1972-02-01",
                "date_precision": "month",
                "event": "Arrived in Vancouver carrying a stolen knife taken from girlfriend in San Rafael",
                "category": "travel",
                "entities": [],
                "location": "Vancouver, British Columbia",
                "source": "letters",
                "importance": 2,
                "notes": f"Source: {letter_id}. Letter to Roger Zelazny (Dec 1, 1972): 'I arrived in Canada carrying a knife. I got the knife by stealing it from the girl I was going with in San Rafael, whom I ditched.'"
            }):
                pass

        # 3b. Speech at convention and UBC
        if "speech" in summary.lower() or "convention" in summary.lower():
            if add_event({
                "id": "pkd_bio_1972_vancouver_convention_speech",
                "date": "1972-02-01",
                "date_precision": "month",
                "event": "Guest of honor at Vancouver science fiction convention; gave speech at convention and University of British Columbia",
                "category": "work",
                "entities": [],
                "location": "Vancouver, British Columbia",
                "source": "letters",
                "importance": 3,
                "notes": "Letter Sept 5, 1973: 'Shortly after giving my speech in Vancouver, both at the convention and at the University of British Columbia, I decided to stay on in Canada'. Speech titled 'The Human and the Android'."
            }):
                pass

        # 3c. Affair with reporter's wife
        if "reporter" in summary.lower() and "affair" in summary.lower():
            if add_event({
                "id": "pkd_bio_1972_vancouver_reporter_wife_affair",
                "date": "1972-02-01",
                "date_precision": "month",
                "event": "Had affair with wife of reporter who covered Vancouver convention; offered to fight reporter",
                "category": "relationship",
                "entities": [],
                "location": "Vancouver, British Columbia",
                "source": "letters",
                "importance": 2,
                "notes": "Letter to Zelazny (Dec 1, 1972): 'In Vancouver I had an affair with the wife of the reporter who covered the Convention for the Province. I also offered to beat him up.'"
            }):
                pass

        # 3d. Computer programmer relationship
        if "computer programmer" in summary.lower():
            if add_event({
                "id": "pkd_bio_1972_vancouver_programmer_relationship",
                "date": "1972-02-01",
                "date_precision": "month",
                "event": "Had romantic relationship with computer programmer in Vancouver",
                "category": "relationship",
                "entities": [],
                "location": "Vancouver, British Columbia",
                "source": "letters",
                "importance": 2,
                "notes": "Letter to Zelazny: 'I had an affair, too, with a computer programmer who, when I first visited her apartment, asked me two questions: (one) Want to smoke dope? and (two) Want to go to bed?'"
            }):
                pass

        # 3e. Jamis relationship (key emotional event)
        if "jamis" in summary.lower():
            if add_event({
                "id": "pkd_bio_1972_vancouver_jamis_relationship",
                "date": "1972-03-01",
                "date_precision": "month",
                "event": "Had tender relationship with hippie woman named Jamis in Vancouver; emotional crisis when she announced she was leaving",
                "category": "relationship",
                "entities": ["Jamis"],
                "location": "Vancouver, British Columbia",
                "source": "letters",
                "importance": 3,
                "notes": "Letter to Zelazny (Dec 1, 1972): 'I had a really tender relationship with a gentle little hippie chick named Jamis, there in Vancouver, who was the reason for my suicide attempt. I still sort of love her.'"
            }):
                pass

        # 3f. X-Kalay work
        if "x-kalay" in summary.lower():
            if add_event({
                "id": "pkd_bio_1972_vancouver_xkalay_work",
                "date": "1972-03-01",
                "date_precision": "month",
                "event": "Worked at X-Kalay heroin rehabilitation center, mopping bathrooms and scrubbing pans",
                "category": "work",
                "entities": [],
                "location": "Vancouver, British Columbia",
                "source": "letters",
                "importance": 3,
                "notes": "Letter: 'The next day I was mopping bathrooms and scrubbing pans all day at X-Kalay, which is like Sinanon'. Later used as material for A Scanner Darkly."
            }):
                pass

    # 4. Suicide attempt
    if "suicide" in summary.lower() and ("attempt" in summary.lower() or "tried" in summary.lower() or "did myself in" in summary.lower()):
        # Vancouver suicide attempt (specific)
        if "vancouver" in summary.lower() or "jamis" in summary.lower():
            if add_event({
                "id": "pkd_bio_1972_vancouver_suicide_attempt",
                "date": "1972-03-01",
                "date_precision": "month",
                "event": "Attempted suicide in Vancouver after Jamis announced she was leaving",
                "category": "health",
                "entities": ["Jamis"],
                "location": "Vancouver, British Columbia",
                "source": "letters",
                "importance": 4,
                "notes": "Letter to Zelazny (Dec 1, 1972): sequence of events - heard Jamis was leaving on radio show one day, heard her say next day she was leaving in a month, attempted suicide the next day."
            }):
                pass
        # Later depression/suicidal ideation (1973)
        elif letter_year == 1973 and ("nearly" in summary.lower() or "partem" in summary.lower()):
            if add_event({
                "id": "pkd_bio_1973_suicidal_ideation",
                "date": iso_date or "1973-08-01",
                "date_precision": precision,
                "event": "Experienced suicidal ideation; contacted Orange County Mental Health for crisis intervention",
                "category": "health",
                "entities": [],
                "location": "Orange County, California",
                "source": "letters",
                "importance": 3,
                "notes": f"Source: {letter_id}. Letter states suicidal thoughts resolved with help from therapist within three weeks."
            }):
                pass

    # 5. Francie relationship and San Rafael abandonment
    if "francie" in summary.lower() and "engaged" in summary.lower():
        if add_event({
            "id": "pkd_bio_1973_francie_breakup",
            "date": "1973-01-01",
            "date_precision": "year",
            "event": "Fiancée Francie abruptly moved out, triggering deep depression; PKD abandoned San Rafael home and possessions",
            "category": "relationship",
            "entities": ["Francie"],
            "location": "San Rafael, California",
            "source": "letters",
            "importance": 3,
            "notes": "Letter to Dr. Bryan (July 4, 1973): 'the girl Francie to whom I was engaged... abruptly moved out, leaving me with little or no reason for either writing or living. I abandoned my home in San Rafael and all my possessions and went to Canada.'"
        }):
            pass

    # 6. Fullerton residence
    if ("fullerton" in summary.lower() or "714" in summary) and letter_year == 1973:
        if add_event({
            "id": "pkd_bio_1973_fullerton_move",
            "date": "1973-04-01",
            "date_precision": "month",
            "event": "Moved to new apartment in Fullerton, Orange County, California with Tessa",
            "category": "residence",
            "entities": ["Tessa Busby"],
            "location": "Fullerton, California",
            "source": "letters",
            "importance": 2,
            "notes": "Multiple spring-summer 1973 letters reference 'Fullerton' and phone 714-524-7306. Move occurred before Christopher's July birth."
        }):
            pass

    # 7. Vehicle purchase
    if ("dodge" in summary.lower() or "car" in summary.lower()) and ("1967" in summary or "67" in summary):
        if add_event({
            "id": "pkd_bio_1973_vehicle_purchase",
            "date": iso_date or "1973-08-01",
            "date_precision": precision or "month",
            "event": "Purchased used 1967 Dodge automobile; car had repeated mechanical failures",
            "category": "residence",
            "entities": [],
            "location": "Fullerton, California",
            "source": "letters",
            "importance": 1,
            "notes": "Letter mentions transmission, front end, starter, tires all failed. Described as always in garage."
        }):
            pass

    # 8. Flow My Tears publication/approval
    if "flow my tears" in summary.lower() and ("approved" in summary.lower() or "okayed" in summary.lower()):
        if add_event({
            "id": "pkd_bio_1973_flow_my_tears_approved",
            "date": iso_date or "1973-04-01",
            "date_precision": precision or "month",
            "event": "Flow My Tears, the Policeman Said approved by Doubleday editor; publication scheduled for February 1974",
            "category": "work",
            "entities": [],
            "location": "California",
            "source": "letters",
            "importance": 2,
            "notes": "Letter to Diane Cleaver (April 9, 1973): 'Scott had just now let me know you'd okayed FLOW MY TEARS. I'm very glad.'"
        }):
            pass

    # 9. Do Androids Dream movie option
    if "do androids dream" in summary.lower() and ("united artists" in summary.lower() or "movie" in summary.lower()):
        if add_event({
            "id": "pkd_bio_1973_androids_dream_movie_option",
            "date": iso_date or "1973-09-01",
            "date_precision": precision or "month",
            "event": "Do Androids Dream of Electric Sheep optioned for film by United Artists for $2,000 option money",
            "category": "work",
            "entities": [],
            "location": "California",
            "source": "letters",
            "importance": 3,
            "notes": "Multiple Sept 1973 letters. Female reader gave enthusiastic 6-page recommendation. Helped alleviate financial crisis."
        }):
            pass

    # 10. Scanner Darkly sale/completion
    if "scanner darkly" in summary.lower() and ("sold" in summary.lower() or "bought" in summary.lower() or "doubleday" in summary.lower()):
        if add_event({
            "id": "pkd_bio_1973_scanner_darkly_sale",
            "date": iso_date or "1973-06-01",
            "date_precision": precision or "month",
            "event": "A Scanner Darkly sold to Doubleday (half-finished); novel based on X-Kalay heroin rehabilitation experiences",
            "category": "work",
            "entities": [],
            "location": "California",
            "source": "letters",
            "importance": 3,
            "notes": "June 1973 letters confirm sale. Novel explicitly about drug addiction and heroin subculture PKD witnessed at X-Kalay."
        }):
            pass

    # 11. Vertex magazine interview
    if "vertex" in summary.lower() and "interview" in summary.lower():
        if add_event({
            "id": "pkd_bio_1973_vertex_magazine_interview",
            "date": iso_date or "1973-09-01",
            "date_precision": precision or "month",
            "event": "Interviewed by Art Cover for Vertex magazine; interview to appear in December 1973 issue with photographs",
            "category": "work",
            "entities": [],
            "location": "California",
            "source": "letters",
            "importance": 2,
            "notes": "Sept 1973 letters. Interview cut from 20,000 to 4,000 words. PKD impressed by quality."
        }):
            pass

    # 12. French TV/Disneyland filming
    if ("french" in summary.lower() or "disneyland" in summary.lower()) and ("filming" in summary.lower() or "film" in summary.lower()):
        if add_event({
            "id": "pkd_bio_1973_french_tv_disneyland",
            "date": iso_date or "1973-09-01",
            "date_precision": precision or "month",
            "event": "Did two days of filming for French television, mostly at Disneyland; exhaustion sent PKD to bed with flu for three weeks",
            "category": "work",
            "entities": [],
            "location": "Disneyland, California",
            "source": "letters",
            "importance": 2,
            "notes": "Oct 1973 letter mentions filming and subsequent illness."
        }):
            pass

    # 13. Jaw surgery (emergency)
    if "jaw" in summary.lower() and ("surgery" in summary.lower() or "surgical" in summary.lower()):
        if add_event({
            "id": "pkd_bio_1973_emergency_jaw_surgery",
            "date": iso_date or "1973-06-01",
            "date_precision": precision or "month",
            "event": "Emergency surgery on lower jaw; created severe financial hardship",
            "category": "health",
            "entities": [],
            "location": "Orange County, California",
            "source": "letters",
            "importance": 2,
            "notes": "Letter to Dr. Bryan (July 4, 1973): 'emergency surgery on my lower jaw suddenly ate up all that we had on hand financially.'"
        }):
            pass

    # 14. Patrice Duvic friendship
    if "patrice duvic" in summary.lower() and ("marriage" in summary.lower() or "saved" in summary.lower()):
        if add_event({
            "id": "pkd_bio_1973_patrice_duvic_friendship",
            "date": iso_date or "1973-09-01",
            "date_precision": precision or "month",
            "event": "Correspondence with Patrice Duvic; Tessa credits Patrice with helping save their marriage through gentle mediation",
            "category": "relationship",
            "entities": ["Patrice Duvic"],
            "location": "California",
            "source": "letters",
            "importance": 2,
            "notes": "Letter Sept 5, 1973: 'My wife thinks Patrice is responsible for saving our marriage by gently quieting my aggressive violence.'"
        }):
            pass

    # 15. Five marriages statement (biographical summary)
    if "five times" in summary.lower() and ("married" in summary.lower() or "marriages" in summary.lower()):
        if add_event({
            "id": "pkd_bio_1973_biographical_five_marriages",
            "date": "1973-09-05",
            "date_precision": "day",
            "event": "PKD states he has been married five times with two daughters and a new son Christopher",
            "category": "family",
            "entities": [],
            "location": "California",
            "source": "letters",
            "importance": 2,
            "notes": "Letter to Marcel Thaon (Sept 5, 1973): 'I have been married five times, have two girls and a new little boy.' Self-reported marital history."
        }):
            pass

# Sort events by date
bio_events.sort(key=lambda x: x.get("date", "9999-12-31"))

print(f"Extracted {len(bio_events)} new biographical events\n")

# Group by category for summary
by_category = defaultdict(list)
for event in bio_events:
    by_category[event.get("category", "unknown")].append(event)

print("Events by category:")
for cat in sorted(by_category.keys()):
    print(f"  {cat}: {len(by_category[cat])}")

# Collect locations and people
locations = set()
people = set()
for event in bio_events:
    if event.get("location"):
        locations.add(event["location"])
    for entity in event.get("entities", []):
        if entity:
            people.add(entity)

print(f"\nNew locations mentioned: {len(locations)}")
for loc in sorted(locations):
    print(f"  - {loc}")

print(f"\nNew people mentioned: {len(people)}")
for person in sorted(people):
    print(f"  - {person}")

# Time period summary
time_periods = {
    "1972 Vancouver (Feb-Mar)": [e for e in bio_events if "1972-02" in e.get("date", "") or "1972-03" in e.get("date", "")],
    "1973 Early (Jan-Mar)": [e for e in bio_events if "1973-01" in e.get("date", "") or "1973-02" in e.get("date", "") or "1973-03" in e.get("date", "")],
    "1973 Spring (Apr-May)": [e for e in bio_events if "1973-04" in e.get("date", "") or "1973-05" in e.get("date", "")],
    "1973 Summer (Jun-Aug)": [e for e in bio_events if "1973-06" in e.get("date", "") or "1973-07" in e.get("date", "") or "1973-08" in e.get("date", "")],
    "1973 Fall/Winter (Sep-Dec)": [e for e in bio_events if "1973-09" in e.get("date", "") or "1973-10" in e.get("date", "") or "1973-11" in e.get("date", "") or "1973-12" in e.get("date", "")],
}

print("\nEvents by time period:")
for period, events in time_periods.items():
    if events:
        print(f"  {period}: {len(events)} events")

# Save to JSON
output_file = r"C:\QueryPat\biography_events_from_letters.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(bio_events, f, indent=2, ensure_ascii=False)

print(f"\nSaved {len(bio_events)} events to {output_file}")
