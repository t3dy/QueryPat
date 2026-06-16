#!/usr/bin/env python3
"""
Refined extraction focusing on real story titles
"""
import re
import json
import pickle
from pathlib import Path

# Known story titles from table of contents
known_stories = {
    # Selected Stories
    "BEYOND LIES THE WUB": 1952,
    "ROOG": 1953,
    "PAYCHECK": 1953,
    "SECOND VARIETY": 1953,
    "IMPOSTER": 1953,
    "THE KING OF THE ELVES": 1953,
    "ADJUSTMENT TEAM": 1952,
    "FOSTER, YOU'RE DEAD": 1955,
    "UPON THE DULL EARTH": 1954,
    "AUTOFAC": 1955,
    "THE MINORITY REPORT": 1956,
    "THE DAYS OF PERKY PAT": 1963,
    "PRECIOUS ARTIFACT": 1956,
    "A GAME OF UNCHANCE": 1956,
    "WE CAN REMEMBER IT FOR YOU WHOLESALE": 1966,
    "FAITH OF OUR FATHERS": 1967,
    "THE ELECTRIC ANT": 1969,
    "A LITTLE SOMETHING FOR US TEMPUNAUTS": 1974,
    "THE EXIT DOOR LEADS IN": 1973,
    "RAUTAVAARA'S CASE": 1980,
    "I HOPE I SHALL ARRIVE SOON": 1980,
}

# Load raw extraction
with open(r'C:\QueryPat\extracted_stories_raw.pkl', 'rb') as f:
    all_stories = pickle.load(f)

# Filter for known stories
filtered_stories = []
for story in all_stories:
    title_upper = story['title'].upper().strip()
    
    # Check if title matches known story
    for known_title in known_stories.keys():
        if known_title in title_upper or title_upper in known_title:
            if len(story['text']) > 500:  # Must have substantial text
                story['publication_year'] = known_stories[known_title]
                filtered_stories.append(story)
                break

print(f"Filtered to {len(filtered_stories)} known stories")
for story in filtered_stories:
    print(f"  - {story['title']} ({story['publication_year']})")

# Save filtered
with open(r'C:\QueryPat\filtered_stories.pkl', 'wb') as f:
    pickle.dump(filtered_stories, f)
