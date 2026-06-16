#!/usr/bin/env python3
"""
Comprehensive extraction of PKD stories from all three collections
"""
import re
import json
from pathlib import Path

def extract_stories(file_path):
    """Extract stories from a markdown file"""
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    stories = []
    
    # Pattern to match story headers: ## **STORY TITLE** or ## Story Title
    # More flexible pattern to catch various header formats
    lines = content.split('\n')
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Match story header patterns
        if re.match(r'^##\s+\*{0,2}([A-Z].*?)\*{0,2}\s*$', line, re.IGNORECASE):
            match = re.match(r'^##\s+\*{0,2}([A-Z].*?)\*{0,2}\s*$', line, re.IGNORECASE)
            if match:
                title = match.group(1).strip()
                # Skip certain patterns that aren't stories
                if any(x in title for x in ['PICTURE', 'IMAGE', 'NOVEL', 'CONTENT', 'INTRODUCTION']):
                    i += 1
                    continue
                
                # Collect story text until next header
                story_text = []
                i += 1
                while i < len(lines) and not re.match(r'^##', lines[i]):
                    story_text.append(lines[i])
                    i += 1
                
                # Only add if we have substantial text
                if len('\n'.join(story_text).strip()) > 200:
                    stories.append({
                        'title': title,
                        'text': '\n'.join(story_text).strip(),
                        'file': Path(file_path).name
                    })
                continue
        
        i += 1
    
    return stories

# Process all three files
files = [
    r"C:\QueryPat\database\extracted_markdown\DOC_ARCH_OCEANOFPDF_COM_SELECTED_STORIES_OF_PHILI.md",
    r"C:\QueryPat\database\extracted_markdown\DOC_ARCH_OCEANOFPDF_COM_THE_COLLECTED_STORIES_OF_.md",
    r"C:\QueryPat\database\extracted_markdown\DOC_ARCH_OCEANOFPDF_COM_THE_SHORT_HAPPY_LIFE_OF_T.md",
]

all_stories = []
for file_path in files:
    try:
        stories = extract_stories(file_path)
        all_stories.extend(stories)
        print(f"Extracted {len(stories)} stories from {Path(file_path).name}")
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

# Print first 50 story titles
print(f"\nTotal stories found: {len(all_stories)}\n")
for i, story in enumerate(all_stories[:50]):
    text_preview = story['text'][:100].replace('\n', ' ')
    print(f"{i+1}. {story['title']} ({story['file']})")

# Save stories for processing
import pickle
with open(r'C:\QueryPat\extracted_stories_raw.pkl', 'wb') as f:
    pickle.dump(all_stories, f)
    
print(f"\nSaved {len(all_stories)} stories to extracted_stories_raw.pkl")
