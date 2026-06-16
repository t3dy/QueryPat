import re
import json
from collections import defaultdict

# Read the markdown file
with open('C:/QueryPat/database/extracted_markdown/DOC_ARCH_PHILIP_K_DICK_THE_SELECTED_LETTERS_OF_PH.md', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the start of letters
chronology_end = content.find('**1972-1973**')
letters_start = content.find('[TO', chronology_end)
letters_section = content[letters_start:]

# Split letters by [TO pattern
letter_blocks = re.split(r'(?=\[TO)', letters_section)

def extract_body_text(block):
    body = block
    body = re.sub(r'\[TO[^\]]+\]', '', body)
    body = re.sub(r'_([^_]+)_', lambda m: m.group(1) if not any(c.isdigit() for c in m.group(1)) else '', body)
    body = re.sub(r'^#{1,3}\s+Dear[^\n]*\n', '', body, flags=re.MULTILINE)
    body = re.sub(r'^#{1,3}\s+', '', body, flags=re.MULTILINE)
    body = re.sub(r'(THE SELECTED LETTERS OF PHILIP K\. DICK|Love,?\s+Phil|Sincerely,?\s+Phil|Yours,?\s+Phil)', '', body)
    body = re.sub(r'\n\s*\d+\s*\n', '\n', body)
    body = re.sub(r'\s+$', '', body)
    return body.strip()

def extract_date(block):
    date_match = re.search(r'_([^_]+)_', block)
    if not date_match:
        date_match = re.search(r'\]\s*([^#\n]+?)(?:\n|$)', block)
    return date_match.group(1).strip() if date_match else "Unknown"

def extract_recipient(block):
    recipient_match = re.match(r'\[TO\s+([^\]]+)\]', block)
    return recipient_match.group(1).strip() if recipient_match else "Unknown"

def analyze_content(body_text, recipient, date):
    body_lower = body_text.lower()

    works = []
    locations = []
    personal_struggles = []
    intellectual_content = []
    biographical_events = []
    themes = []
    exegesis_connections = []
    key_quotes = []

    # Works detection
    if 'ubik' in body_lower:
        works.append('Ubik')
    if 'valis' in body_lower:
        works.append('VALIS')
    if 'androids dream' in body_lower or 'electric sheep' in body_lower:
        works.append('Do Androids Dream of Electric Sheep')
    if 'flow my tears' in body_lower:
        works.append('Flow My Tears, the Policeman Said')
    if 'confessions of a crap artist' in body_lower or ('confessions' in body_lower and 'crap' in body_lower):
        works.append('Confessions of a Crap Artist')
    if 'high castle' in body_lower or 'man in the high castle' in body_lower:
        works.append('The Man in the High Castle')
    if 'palmer eldritch' in body_lower:
        works.append('The Three Stigmata of Palmer Eldritch')
    if 'scanner darkly' in body_lower:
        works.append('A Scanner Darkly')
    if 'deus irae' in body_lower:
        works.append('Deus Irae')

    # Location detection
    if 'vancouver' in body_lower:
        locations.append('Vancouver')
    if 'california' in body_lower or 'calif' in body_lower:
        locations.append('California')
    if 'san rafael' in body_lower:
        locations.append('San Rafael')
    if 'x-kalay' in body_lower:
        locations.append('X-Kalay (rehab center)')
    if 'canada' in body_lower:
        locations.append('Canada')

    # Biographical events
    if 'marriage' in body_lower or 'married' in body_lower:
        biographical_events.append('Marriage/Relationship milestone')
    if 'divorce' in body_lower:
        biographical_events.append('Divorce proceedings')
    if 'baby' in body_lower or 'child' in body_lower or 'son' in body_lower or 'daughter' in body_lower:
        biographical_events.append('Child birth/family')
    if 'convention' in body_lower or 'worldcon' in body_lower:
        biographical_events.append('Science fiction convention')
    if 'suicide' in body_lower or 'suicid' in body_lower:
        biographical_events.append('Suicide attempt/mental crisis')
    if 'hospitalized' in body_lower:
        biographical_events.append('Hospitalization')
    if 'published' in body_lower:
        biographical_events.append('Publication milestone')
    if 'award' in body_lower or 'hugo' in body_lower:
        biographical_events.append('Award/Recognition')

    # Personal struggles
    if 'lonely' in body_lower or 'loneliness' in body_lower:
        personal_struggles.append('Loneliness')
    if 'depressed' in body_lower or 'depression' in body_lower or 'despair' in body_lower:
        personal_struggles.append('Depression/Despair')
    if 'drug' in body_lower or 'heroin' in body_lower or 'amphetamine' in body_lower:
        personal_struggles.append('Drug use/addiction')
    if 'divorce' in body_lower or 'wife' in body_lower or 'marriage' in body_lower:
        personal_struggles.append('Relationship/marriage issues')
    if 'health' in body_lower or 'hospital' in body_lower or 'sick' in body_lower:
        personal_struggles.append('Health issues')
    if 'money' in body_lower or 'rent' in body_lower or 'financial' in body_lower or 'broke' in body_lower:
        personal_struggles.append('Financial difficulties')

    # Intellectual content
    if 'theology' in body_lower:
        intellectual_content.append('Theology')
    if 'god' in body_lower or 'religious' in body_lower or 'religion' in body_lower:
        intellectual_content.append('Religion/Spirituality')
    if 'consciousness' in body_lower:
        intellectual_content.append('Consciousness')
    if 'reality' in body_lower:
        intellectual_content.append('Nature of reality')
    if 'android' in body_lower or 'simulacra' in body_lower or 'simulacrum' in body_lower:
        intellectual_content.append('Simulacra/Artificial consciousness')
    if 'writing' in body_lower or 'novel' in body_lower or 'fiction' in body_lower:
        intellectual_content.append('Writing/Fiction craft')
    if 'philosophy' in body_lower:
        intellectual_content.append('Philosophy')
    if 'authentic' in body_lower:
        intellectual_content.append('Authenticity/Being')

    # Extract key quotes
    quotes = re.findall(r'["\']([^"\']{30,200})["\']', body_text)
    if quotes:
        key_quotes = quotes[:3]

    # Identify themes
    if len(intellectual_content) > 0:
        themes.append('Philosophical/Intellectual')
    if len(personal_struggles) > 0:
        themes.append('Personal struggle')
    if len(works) > 0:
        themes.append('Work discussion')
    if 'suicide' in body_lower or 'depressed' in body_lower or 'despair' in body_lower:
        themes.append('Mental health crisis')
    if 'hope' in body_lower or 'love' in body_lower:
        themes.append('Hope/Recovery')

    return {
        'works_mentioned': list(set(works)),
        'locations_mentioned': list(set(locations)),
        'biographical_events': list(set(biographical_events)),
        'personal_struggles': list(set(personal_struggles)),
        'intellectual_content': list(set(intellectual_content)),
        'exegesis_connections': exegesis_connections,
        'key_quotes': key_quotes,
        'themes': list(set(themes))
    }

# Parse all letters
all_letters = []

for block_idx, block in enumerate(letter_blocks[1:], start=1):
    if not block.strip():
        continue

    recipient = extract_recipient(block)
    date = extract_date(block)
    body = extract_body_text(block)

    if len(body) < 100:
        continue

    analysis = analyze_content(body, recipient, date)

    summary = body[:1500] + ('...' if len(body) > 1500 else '')

    letter = {
        'letter_id': f'LETTER_{block_idx:03d}',
        'date': date,
        'recipient': recipient,
        'summary': summary,
        'locations_mentioned': analysis['locations_mentioned'],
        'biographical_events': analysis['biographical_events'],
        'works_mentioned': analysis['works_mentioned'],
        'intellectual_content': analysis['intellectual_content'],
        'personal_struggles': analysis['personal_struggles'],
        'exegesis_connections': analysis['exegesis_connections'],
        'key_quotes': analysis['key_quotes'],
        'themes': analysis['themes']
    }

    all_letters.append(letter)

# Filter for significant letters
def calc_significance(letter):
    score = 0
    score += len(letter['works_mentioned']) * 3
    score += len(letter['intellectual_content']) * 3
    score += len(letter['personal_struggles']) * 2
    score += len(letter['biographical_events']) * 2
    score += len(letter['themes'])
    if '1973' in letter['date']:
        score += 1
    return score

scored_letters = [(letter, calc_significance(letter)) for letter in all_letters]
scored_letters.sort(key=lambda x: x[1], reverse=True)

significant_letters = [letter for letter, score in scored_letters[:75]]
significant_letters.sort(key=lambda x: x['date'])

print(f"Total letters extracted: {len(all_letters)}")
print(f"Significant letters selected: {len(significant_letters)}")
print(f"\nFirst 10 significant letters (chronological):")
for letter in significant_letters[:10]:
    print(f"  {letter['letter_id']}: {letter['recipient']} ({letter['date']})")

# Save to JSON
with open('C:/QueryPat/selected_letters_analysis.json', 'w', encoding='utf-8') as f:
    json.dump(significant_letters, f, indent=2, ensure_ascii=False)

print(f"\nJSON successfully saved to C:/QueryPat/selected_letters_analysis.json")
print(f"File size: {len(json.dumps(significant_letters))} bytes")
