#!/usr/bin/env python3
"""
Extract biographical events from PKD Selected Letters (1972-1973)
Parses 75 significant letters and identifies structured biographical events
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

print(f"Loaded {len(letters_data)} letters and {len(existing_bio)} existing biography events")
print()

# Parse date utilities
def parse_date(date_str: str) -> Tuple[Optional[str], str]:
    """Parse letter date and return (iso_date, precision)"""
    if not date_str or date_str.strip() == "":
        return None, "unknown"

    date_str = date_str.strip()

    # Remove extra whitespace and artifacts
    date_str = re.sub(r'\s+', ' ', date_str)

    # Try various date formats
    # Full date: "December 1, 1972"
    match = re.search(r'(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{1,2}),\s+(\d{4})', date_str)
    if match:
        month_str, day_str, year_str = match.groups()
        month_map = {m: i+1 for i, m in enumerate(['January', 'February', 'March', 'April', 'May', 'June',
                                                    'July', 'August', 'September', 'October', 'November', 'December'])}
        month = month_map.get(month_str, 1)
        day = int(day_str)
        year = int(year_str)
        iso_date = f"{year:04d}-{month:02d}-{day:02d}"
        return iso_date, "day"

    # Month-Year: "December 1972" or "Dec 1972"
    match = re.search(r'(January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+(\d{4})', date_str)
    if match:
        month_str, year_str = match.groups()
        month_map = {
            'January': 1, 'Feb ruary': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6,
            'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12,
            'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'Jun': 6,
            'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12
        }
        month = month_map.get(month_str, 1)
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

# Extract biographical events
bio_events = []
people_mentioned = set()
locations_mentioned = set()
event_count_by_category = defaultdict(int)

# Define event patterns
def extract_christopher_birth(letter: Dict, date_str: str) -> Optional[Dict]:
    """Extract Christopher's birth event"""
    summary = letter.get("summary", "").lower()

    if "christopher" in summary and ("born" in summary or "baby" in summary or "delivered" in summary):
        # Look for specific date
        full_summary = letter.get("summary", "")
        date_match = re.search(r'(born|birth)\s+(July|June)\s+(\d{1,2})', full_summary, re.IGNORECASE)

        iso_date, precision = parse_date(date_str)

        # Check for July 25, 1973 (most specific reference)
        if "july 25" in summary:
            iso_date = "1973-07-25"
            precision = "day"
        elif "july" in summary and "1973" in date_str:
            iso_date = "1973-07-01"
            precision = "month"
        elif "1973" in date_str:
            iso_date = "1973-01-01"
            precision = "year"

        if iso_date:
            event_id = "pkd_bio_1973_christopher_birth"
            if event_id not in existing_ids:
                return {
                    "id": event_id,
                    "date": iso_date,
                    "date_precision": precision,
                    "event": "Birth of son Christopher to Philip K. Dick and wife Tessa",
                    "category": "birth",
                    "entities": ["Christopher Dick", "Tessa Busby Dick"],
                    "location": "Fullerton, California",
                    "source": "letters",
                    "importance": 4,
                    "notes": "Multiple letters (1973) confirm Christopher's birth in July 1973, likely July 25. Mother Tessa. Letter Sept 5, 1973 mentions 'just a month ago' for August 5 reference point, confirming late July birth. First-person account from PKD."
                }
    return None

def extract_vancouver_episode(letter: Dict, date_str: str) -> List[Dict]:
    """Extract events from Vancouver episode"""
    events = []
    summary = letter.get("summary", "")

    if "vancouver" not in summary.lower():
        return events

    iso_date, precision = parse_date(date_str)

    # Vancouver arrival with knife
    if "arriving" in summary.lower() and "knife" in summary.lower():
        event_id = "pkd_bio_1972_vancouver_arrival"
        if event_id not in existing_ids:
            events.append({
                "id": event_id,
                "date": "1972-02-01",
                "date_precision": "month",
                "event": "PKD arrives in Vancouver carrying a stolen knife",
                "category": "travel",
                "entities": ["PKD"],
                "location": "Vancouver, British Columbia",
                "source": "letters",
                "importance": 3,
                "notes": "Letter to Roger Zelazny (Dec 1, 1972): 'I arrived in Canada carrying a knife... I got the knife by stealing it from the girl I was going with in San Rafael'. Unreliable narrator account."
            })

    # Vancouver romance and suicide attempt
    if "jamis" in summary.lower() and "suicide" in summary.lower():
        event_id = "pkd_bio_1972_vancouver_suicide_attempt"
        if event_id not in existing_ids:
            events.append({
                "id": event_id,
                "date": "1972-03-01",
                "date_precision": "month",
                "event": "Suicide attempt in Vancouver after relationship ending with Jamis",
                "category": "health",
                "entities": ["Jamis"],
                "location": "Vancouver, British Columbia",
                "source": "letters",
                "importance": 4,
                "notes": "Letter to Zelazny: 'I had a really tender relationship with a gentle little hippie chick named Jamis... she was the reason for my suicide attempt.' PKD states he heard she was leaving Vancouver, heard it one day, and attempted suicide the next day."
            })

    # X-Kalay work (mopping bathrooms)
    if "x-kalay" in summary.lower():
        event_id = "pkd_bio_1972_xkalay_work"
        if event_id not in existing_ids:
            events.append({
                "id": event_id,
                "date": "1972-03-01",
                "date_precision": "month",
                "event": "Worked at X-Kalay heroin rehabilitation center mopping bathrooms and scrubbing pans",
                "category": "work",
                "entities": [],
                "location": "Vancouver, British Columbia",
                "source": "letters",
                "importance": 3,
                "notes": "Letter states 'The next day I was mopping bathrooms and scrubbing pans all day at X-Kalay, which is like Sinanon'. PKD later used X-Kalay experience for A Scanner Darkly novel."
            })

    return events

def extract_marriage_events(letter: Dict, date_str: str) -> List[Dict]:
    """Extract marriage-related events"""
    events = []
    summary = letter.get("summary", "")
    recipient = letter.get("recipient", "").lower()

    iso_date, precision = parse_date(date_str)

    # Marriage to Tessa (1973)
    if ("married" in summary.lower() or "wife" in summary.lower()) and "tessa" in summary.lower() and "1973" in date_str:
        event_id = "pkd_bio_1973_marriage_tessa"
        if event_id not in existing_ids and iso_date:
            # Look for April marriage reference
            if "april" in date_str.lower() or "april 19" in summary.lower():
                events.append({
                    "id": event_id,
                    "date": "1973-04-19",
                    "date_precision": "day",
                    "event": "Married Tessa Busby",
                    "category": "family",
                    "entities": ["Tessa Busby"],
                    "location": "California",
                    "source": "letters",
                    "importance": 4,
                    "notes": "Letter to Sherry Gottlieb (April 19, 1973): 'On Tuesday we received Locus and saw that we are supposed to get married this week. So we did.' Marriage date confirmed as April 19, 1973."
                })

    return events

def extract_residence_events(letter: Dict, date_str: str) -> List[Dict]:
    """Extract residence changes"""
    events = []
    summary = letter.get("summary", "")

    iso_date, precision = parse_date(date_str)

    # Fullerton/Orange County residence (initial move 1973)
    if ("fullerton" in summary.lower() or "orange county" in summary.lower()) and iso_date and "1973" in iso_date:
        event_id = "pkd_bio_1973_fullerton_residence"
        if event_id not in existing_ids:
            # Extract phone area code if present
            phone_match = re.search(r'714-\d{3}-\d{4}', summary)
            events.append({
                "id": event_id,
                "date": "1973-04-01",
                "date_precision": "month",
                "event": "Moved to apartment in Fullerton, Orange County, California with Tessa",
                "category": "residence",
                "entities": ["Tessa Busby"],
                "location": "Fullerton, California",
                "source": "letters",
                "importance": 2,
                "notes": "Multiple letters reference 'gunjy Fullerton' and phone number 714-524-7306. Letters indicate move occurred before Christopher's July birth. Described as 'new apartment' in several letters from June-Sept 1973."
            })

    # San Rafael abandonment (early 1973)
    if "san rafael" in summary.lower() and "abandoned" in summary.lower():
        event_id = "pkd_bio_1973_abandoned_san_rafael"
        if event_id not in existing_ids:
            events.append({
                "id": event_id,
                "date": "1973-01-01",
                "date_precision": "year",
                "event": "Abandoned home and possessions in San Rafael while depressed after Francie moved out; left for Canada",
                "category": "residence",
                "entities": ["Francie"],
                "location": "San Rafael, California",
                "source": "letters",
                "importance": 2,
                "notes": "Letter to Dr. Henry Edwin Bryan (July 4, 1973): 'The girl Francie to whom I was engaged... abruptly moved out... I abandoned my home in San Rafael and all my possessions and went to Canada.'"
            })

    return events

def extract_health_events(letter: Dict, date_str: str) -> List[Dict]:
    """Extract health-related events"""
    events = []
    summary = letter.get("summary", "")

    iso_date, precision = parse_date(date_str)

    # Emergency jaw surgery
    if "jaw" in summary.lower() and "surgery" in summary.lower():
        event_id = "pkd_bio_1973_jaw_surgery"
        if event_id not in existing_ids and iso_date:
            events.append({
                "id": event_id,
                "date": iso_date if iso_date and "1973" in iso_date else "1973-06-01",
                "date_precision": "month",
                "event": "Emergency surgery on lower jaw",
                "category": "health",
                "entities": [],
                "location": "Orange County, California",
                "source": "letters",
                "importance": 2,
                "notes": "Letter to Dr. Bryan (July 4, 1973): 'emergency surgery on my lower jaw suddenly ate up all that we had on hand financially'. Created financial hardship."
            })

    # Postpartum depression
    if "post partem" in summary.lower() or ("postpartum" in summary.lower() and "nearly did myself in" in summary.lower()):
        event_id = "pkd_bio_1973_postpartum_depression"
        if event_id not in existing_ids and iso_date:
            events.append({
                "id": event_id,
                "date": iso_date if iso_date and "1973" in iso_date else "1973-08-01",
                "date_precision": "month",
                "event": "Experienced postpartum depression after Christopher's birth, nearly attempted suicide",
                "category": "health",
                "entities": [],
                "location": "Fullerton, California",
                "source": "letters",
                "importance": 3,
                "notes": "Letter to Diane Cleaver (Sept 5, 1973): 'Right after Christopher's birth I had a post partem, and nearly did myself in... I contacted Orange County Mental Health, and their therapist pulled me out in three weeks.'"
            })

    # Mental health treatment
    if "mental health" in summary.lower() and "therapist" in summary.lower():
        event_id = "pkd_bio_1973_mental_health_treatment"
        if event_id not in existing_ids and iso_date:
            events.append({
                "id": event_id,
                "date": iso_date if iso_date and "1973" in iso_date else "1973-08-01",
                "date_precision": "month",
                "event": "Sought treatment from Orange County Mental Health; therapist helped resolve suicidal ideation within three weeks",
                "category": "health",
                "entities": [],
                "location": "Orange County, California",
                "source": "letters",
                "importance": 2,
                "notes": "PKD credits therapist with pulling him out of suicidal state after Christopher's birth."
            })

    return events

def extract_work_events(letter: Dict, date_str: str) -> List[Dict]:
    """Extract work/publication events"""
    events = []
    summary = letter.get("summary", "")

    iso_date, precision = parse_date(date_str)

    # Do Androids Dream movie option
    if "do androids dream" in summary.lower() and ("united artists" in summary.lower() or "movie" in summary.lower()):
        event_id = "pkd_bio_1973_androids_movie_option"
        if event_id not in existing_ids and iso_date:
            # Extract option amount if present
            money_match = re.search(r'\$(\d+(?:,\d+)*)', summary)
            money = money_match.group(1) if money_match else "unknown"

            events.append({
                "id": event_id,
                "date": iso_date if iso_date and "1973" in iso_date else "1973-09-01",
                "date_precision": "month",
                "event": "Do Androids Dream of Electric Sheep optioned for film by United Artists for $2,000 option money",
                "category": "work",
                "entities": [],
                "location": "California",
                "source": "letters",
                "importance": 3,
                "notes": "Multiple letters mention UA option ($2,000). Female reader gave enthusiastic recommendation. Helped alleviate financial crisis."
            })

    # Vertex magazine interview
    if "vertex" in summary.lower() and ("interview" in summary.lower() or "art cover" in summary.lower()):
        event_id = "pkd_bio_1973_vertex_interview"
        if event_id not in existing_ids and iso_date:
            events.append({
                "id": event_id,
                "date": iso_date if iso_date and "1973" in iso_date else "1973-09-01",
                "date_precision": "month",
                "event": "Interviewed by Art Cover for Vertex magazine; interview to appear in December 1973 issue with photographs",
                "category": "work",
                "entities": [],
                "location": "California",
                "source": "letters",
                "importance": 2,
                "notes": "PKD expresses enthusiasm about the interview, which was cut from 20,000 to 4,000 words."
            })

    # Scanner Darkly sold
    if "scanner darkly" in summary.lower() and ("sold" in summary.lower() or "doubleday" in summary.lower()):
        event_id = "pkd_bio_1973_scanner_darkly_sale"
        if event_id not in existing_ids:
            events.append({
                "id": event_id,
                "date": "1973-06-01",
                "date_precision": "month",
                "event": "A Scanner Darkly sold to Doubleday; novel based on X-Kalay heroin rehabilitation center experiences",
                "category": "work",
                "entities": [],
                "location": "California",
                "source": "letters",
                "importance": 3,
                "notes": "PKD notes in June 1973 letter that Scanner Darkly was 'bought... half-finished' and is 'based on my experiences at X-Kalay'. Novel addresses addiction themes."
            })

    return events

def extract_vehicle_purchase(letter: Dict, date_str: str) -> List[Dict]:
    """Extract vehicle purchase"""
    events = []
    summary = letter.get("summary", "")

    iso_date, precision = parse_date(date_str)

    # 1967 Dodge purchase
    if "dodge" in summary.lower() and ("1967" in summary or "67" in summary):
        event_id = "pkd_bio_1973_dodge_purchase"
        if event_id not in existing_ids and iso_date:
            events.append({
                "id": event_id,
                "date": iso_date if iso_date and "1973" in iso_date else "1973-08-01",
                "date_precision": "month",
                "event": "Purchased used 1967 Dodge automobile",
                "category": "residence",
                "entities": [],
                "location": "Fullerton, California",
                "source": "letters",
                "importance": 1,
                "notes": "Letter mentions car troubles: transmission, front end, starter, tires all failed. Car ultimately became unreliable."
            })

    return events

def extract_speech_events(letter: Dict, date_str: str) -> List[Dict]:
    """Extract speaking engagements"""
    events = []
    summary = letter.get("summary", "")

    iso_date, precision = parse_date(date_str)

    # Vancouver speech
    if ("vancouver" in summary.lower() or "ubc" in summary.lower()) and ("speech" in summary.lower() or "speaking" in summary.lower()):
        event_id = "pkd_bio_1972_vancouver_speech"
        if event_id not in existing_ids:
            events.append({
                "id": event_id,
                "date": "1972-02-01",
                "date_precision": "month",
                "event": "Gave speeches at Vancouver science fiction convention and University of British Columbia",
                "category": "work",
                "entities": [],
                "location": "Vancouver, British Columbia",
                "source": "letters",
                "importance": 3,
                "notes": "Letter Sept 5, 1973 states: 'Shortly after giving my speech in Vancouver, both at the convention and at the University of British Columbia, I decided to stay on in Canada and become a citizen.' Speech titled 'The Human and the Android' (subtitle: 'The Authentic Human versus the Reflex Machine')."
            })

    return events

def extract_relationship_events(letter: Dict, date_str: str) -> List[Dict]:
    """Extract romantic relationship events"""
    events = []
    summary = letter.get("summary", "")
    recipient = letter.get("recipient", "").lower()

    iso_date, precision = parse_date(date_str)

    # Affair with reporter's wife (Vancouver)
    if "vancouver" in summary.lower() and "affair" in summary.lower() and "reporter" in summary.lower():
        event_id = "pkd_bio_1972_vancouver_reporter_affair"
        if event_id not in existing_ids:
            events.append({
                "id": event_id,
                "date": "1972-02-01",
                "date_precision": "month",
                "event": "Had affair with wife of reporter who covered Vancouver convention; offered to fight reporter",
                "category": "relationship",
                "entities": [],
                "location": "Vancouver, British Columbia",
                "source": "letters",
                "importance": 2,
                "notes": "Letter to Zelazny (Dec 1, 1972): 'In Vancouver I had an affair with the wife of the reporter who covered the Convention for the Province. I also offered to beat him up.'"
            })

    # Relationship with computer programmer (Vancouver)
    if "vancouver" in summary.lower() and "computer programmer" in summary.lower():
        event_id = "pkd_bio_1972_vancouver_programmer"
        if event_id not in existing_ids:
            events.append({
                "id": event_id,
                "date": "1972-02-01",
                "date_precision": "month",
                "event": "Had romantic relationship with computer programmer in Vancouver",
                "category": "relationship",
                "entities": [],
                "location": "Vancouver, British Columbia",
                "source": "letters",
                "importance": 2,
                "notes": "Letter to Zelazny: 'I had an affair, too, with a computer programmer who, when I first visited her apartment, asked me two questions: (one) \"Want to smoke dope?\" and (two) \"Want to go to bed?\" I said yes to both. The dope was terrible.'"
            })

    # Francie relationship end
    if "francie" in summary.lower() and ("moved out" in summary.lower() or "engaged" in summary.lower()):
        event_id = "pkd_bio_1973_francie_breakup"
        if event_id not in existing_ids:
            events.append({
                "id": event_id,
                "date": "1973-01-01",
                "date_precision": "year",
                "event": "Fiancée Francie abruptly moved out, causing severe depression",
                "category": "relationship",
                "entities": ["Francie"],
                "location": "San Rafael, California",
                "source": "letters",
                "importance": 2,
                "notes": "Letter to Dr. Bryan (July 4, 1973): 'the girl Francie to whom I was engaged... abruptly moved out, leaving me with little or no reason for either writing or living.'"
            })

    return events

def extract_personal_narrative_events(letter: Dict, date_str: str) -> List[Dict]:
    """Extract personal history narratives mentioned in letters"""
    events = []
    summary = letter.get("summary", "")

    iso_date, precision = parse_date(date_str)

    # Five marriages statement (Sept 5, 1973 letter to Marcel Thaon)
    if "married five times" in summary.lower() or "five marriages" in summary.lower():
        event_id = "pkd_bio_summary_five_marriages"
        if event_id not in existing_ids:
            events.append({
                "id": event_id,
                "date": "1973-09-05",
                "date_precision": "day",
                "event": "PKD states in letter to Marcel Thaon that he has been married five times",
                "category": "family",
                "entities": [],
                "location": "California",
                "source": "letters",
                "importance": 2,
                "notes": "Letter Sept 5, 1973 to Marcel Thaon: 'I have been married five times, have two girls and a new little boy.' This is PKD's self-reported account of marital history."
            })

    # Gutter years with drug users
    if ("gutter" in summary.lower() or "stilyagi" in summary.lower()) and ("dope" in summary.lower() or "narcotics" in summary.lower()):
        event_id = "pkd_bio_personal_gutter_years"
        if event_id not in existing_ids:
            events.append({
                "id": event_id,
                "date": "1970-01-01",
                "date_precision": "year",
                "event": "PKD describes extended period living in gutter subculture with drug users, heroin addicts, and young people involved in crime",
                "category": "residence",
                "entities": [],
                "location": "California/Canada",
                "source": "letters",
                "importance": 2,
                "notes": "Sept 5, 1973 letter describes: 'when the marriage failed I dropped (gratefully) into the gutter of near-illegal life: narcotics and guns and knives'. States he lived with 'stilyagi (the teen-age hoodlums)' and provided shelter to young people who would have otherwise been lost."
            })

    return events

# Process all letters
for i, letter in enumerate(letters_data):
    letter_id = letter.get("letter_id", f"LETTER_{i}")
    date_str = letter.get("date", "").strip()
    summary = letter.get("summary", "").strip()
    recipient = letter.get("recipient", "").strip()

    iso_date, precision = parse_date(date_str)

    # Extract events using all extraction functions
    extracted = []

    # Christopher birth
    chris_event = extract_christopher_birth(letter, date_str)
    if chris_event:
        extracted.append(chris_event)

    # Vancouver episodes
    extracted.extend(extract_vancouver_episode(letter, date_str))

    # Marriage events
    extracted.extend(extract_marriage_events(letter, date_str))

    # Residence events
    extracted.extend(extract_residence_events(letter, date_str))

    # Health events
    extracted.extend(extract_health_events(letter, date_str))

    # Work events
    extracted.extend(extract_work_events(letter, date_str))

    # Vehicle purchase
    extracted.extend(extract_vehicle_purchase(letter, date_str))

    # Speech events
    extracted.extend(extract_speech_events(letter, date_str))

    # Relationship events
    extracted.extend(extract_relationship_events(letter, date_str))

    # Personal narrative events
    extracted.extend(extract_personal_narrative_events(letter, date_str))

    # Add extracted events (avoiding duplicates)
    for event in extracted:
        if event["id"] not in existing_ids and event["id"] not in {e["id"] for e in bio_events}:
            bio_events.append(event)
            existing_ids.add(event["id"])
            event_count_by_category[event["category"]] += 1

            # Track entities and locations
            for entity in event.get("entities", []):
                if entity:
                    people_mentioned.add(entity)
            if event.get("location"):
                locations_mentioned.add(event["location"])

# Sort by date
bio_events.sort(key=lambda x: x.get("date", ""))

print(f"\nExtracted {len(bio_events)} new biographical events")
print(f"\nEvents by category:")
for cat, count in sorted(event_count_by_category.items()):
    print(f"  {cat}: {count}")

print(f"\nNew locations mentioned: {len(locations_mentioned)}")
for loc in sorted(locations_mentioned):
    print(f"  - {loc}")

print(f"\nNew people mentioned: {len(people_mentioned)}")
for person in sorted(people_mentioned):
    print(f"  - {person}")

# Save to JSON
output_file = r"C:\QueryPat\biography_events_from_letters.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(bio_events, f, indent=2, ensure_ascii=False)

print(f"\nSaved {len(bio_events)} events to {output_file}")
