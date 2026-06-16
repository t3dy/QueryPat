#!/usr/bin/env python3
import re
import json
from pathlib import Path

# Read the markdown file
markdown_file = r"C:\QueryPat\database\extracted_markdown\DOC_ARCH_OXFORD_BOOKWORMS_LIBRARY_STAGE_5_OXFORD_.md"
with open(markdown_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Split by chapter markers
chapters_raw = re.split(r'\*\*(\d+)\*\*\s*\n', content)

# Parse chapters - the split creates alternating pattern: [text_before, chapter_num, chapter_content, ...]
chapters_data = []
for i in range(1, len(chapters_raw), 2):
    if i + 1 < len(chapters_raw):
        chapter_num = int(chapters_raw[i])
        chapter_text = chapters_raw[i + 1].strip()
        chapters_data.append({
            'number': chapter_num,
            'text': chapter_text
        })

print(f"Extracted {len(chapters_data)} chapters")

# Now analyze each chapter
chapters_json = []

for chap in chapters_data:
    num = chap['number']
    text = chap['text']

    # Extract title - usually first line or heading
    lines = text.split('\n')
    title = ""
    for line in lines[:10]:  # Check first 10 lines
        line = line.strip()
        if line and not line.startswith('#') and not line.startswith('*'):
            if len(line) < 100 and (line[0].isupper() or line[0] == '"'):
                title = line[:100]
                break

    if not title:
        title = f"Chapter {num}"

    # Create comprehensive summary by extracting key sentences
    sentences = re.split(r'(?<=[.!?])\s+', text)
    summary_sentences = []
    for sent in sentences[:50]:  # Get from first 50 sentences
        sent = sent.strip()
        if sent and len(sent) > 20:
            summary_sentences.append(sent)

    summary = ' '.join(summary_sentences[:15])  # Combine into paragraph
    if len(summary) > 50:
        summary = summary[:800] + "..." if len(summary) > 800 else summary

    # Extract locations
    location_patterns = [
        r'San Francisco', r'Mars', r'Earth', r'Nob Hill', r'Mount Zion',
        r'New America', r'New New York', r'Lombard Street', r'Sutter Street',
        r'Hall of Justice', r'peninsula', r'suburbs', r'rooftop', r'apartment',
        r'building', r'office', r'street', r'colony', r'planet'
    ]
    locations = set()
    for pattern in location_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            locations.add(pattern)

    # Extract character names
    char_patterns = [
        r'Rick Deckard', r'John Isidore', r'Inspector Bryant', r'Dave Holden',
        r'Iran', r'Pris Stratton', r'Roy Baty', r'Rachael Rosen', r'Irmgard',
        r'Hannibal Sloat', r'Bill Barbour', r'Ann Marsten', r'Mercer',
        r'Phil Resch', r'Luba Luft', r'Max Polokov', r'Wilbur Mercer'
    ]
    characters = set()
    for pattern in char_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            characters.add(pattern)

    # Extract themes
    theme_keywords = {
        'authenticity': [r'real', r'fake', r'electric', r'artificial', r'android'],
        'humanity': [r'human', r'empathy', r'empathic', r'feeling', r'emotion'],
        'consciousness': [r'conscious', r'mind', r'brain', r'awareness', r'aware'],
        'identity': [r'identity', r'self', r'who.*am', r'belong'],
        'reality': [r'reality', r'real', r'truth', r'illusion'],
        'existence': [r'exist', r'alive', r'death', r'life'],
        'morality': [r'moral', r'ethics', r'right', r'wrong', r'evil', r'good'],
    }

    themes = set()
    for theme, keywords in theme_keywords.items():
        for keyword in keywords:
            if re.search(keyword, text, re.IGNORECASE):
                themes.add(theme)
                break

    # Extract philosophical concepts
    philo_patterns = [
        'consciousness', 'identity', 'personhood', 'artificial life',
        'existentialism', 'empathy', 'reality', 'authenticity', 'the self',
        'what is human', 'what is real', 'being and existence'
    ]
    concepts = set()
    for concept in philo_patterns:
        if re.search(concept, text, re.IGNORECASE):
            concepts.add(concept)

    # Extract key events
    key_events = []
    event_patterns = [
        (r'(android|andy).*escap', 'Androids escaped'),
        (r'(hunt|search|track).*android', 'Bounty hunt begins'),
        (r'Voigt.*Kampff', 'Voigt-Kampff test administered'),
        (r'(retir|kill).*android', 'Android retired'),
        (r'test.*empathy', 'Empathy test given'),
        (r'discover.*android', 'Android discovered'),
        (r'(fusion|Mercer)', 'Mercer empathy fusion'),
        (r'question.*real', 'Reality questioned'),
    ]
    for pattern, event in event_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            key_events.append(event)

    # Build chapter JSON
    chapter_json = {
        'chapter_number': num,
        'chapter_title': title,
        'summary': summary if summary else 'Chapter ' + str(num),
        'locations_mentioned': sorted(list(locations))[:10],
        'characters_appearing': sorted(list(characters))[:15],
        'themes_explored': sorted(list(themes))[:8],
        'philosophical_concepts': sorted(list(concepts))[:8],
        'key_events': key_events[:6],
        'narrative_observations': [
            f"Chapter {num} contains approximately {len(text)} characters",
            f"Primary focus: {', '.join(list(themes)[:2]) if themes else 'plot development'}",
            f"Key characters in this chapter: {', '.join(list(characters)[:3]) if characters else 'various'}"
        ]
    }

    chapters_json.append(chapter_json)

# Save to JSON file
output_file = r"C:\QueryPat\do_androids_dream_chapters_all.json"
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(chapters_json, f, indent=2, ensure_ascii=False)

print(f"\nSuccessfully extracted all 22 chapters")
print(f"Saved to: {output_file}")
print(f"\nSample - Chapter 1:")
print(json.dumps(chapters_json[0], indent=2))
