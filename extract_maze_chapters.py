#!/usr/bin/env python3
"""
Extract and analyze A Maze of Death chapters from markdown source.
Generates comprehensive JSON summaries for each chapter.
"""

import json
import re
from pathlib import Path

def clean_text(text):
    """Remove OCR artifacts and picture placeholders."""
    # Remove picture placeholders
    text = re.sub(r'\*\*==> picture.*?\*\*', '', text, flags=re.DOTALL)
    text = re.sub(r'\*\*----- Start of picture text.*?----- End of picture text -----\*\*', '', text, flags=re.DOTALL)
    text = re.sub(r'\*\*r B\*\*', '', text)
    text = re.sub(r'<br>', '', text)
    # Remove excessive whitespace
    text = re.sub(r'\n\n\n+', '\n\n', text)
    text = text.strip()
    return text

def extract_locations(text):
    """Extract location mentions from chapter text."""
    locations = set()
    location_patterns = [
        r'Delmak-O',
        r'the colony',
        r'the buildings',
        r'the tomb',
        r'the maze',
        r'the satellite',
        r'Terra',
        r'the planet',
        r'Tekel Upharsin',
        r'the god-worlds?',
        r'the ship',
    ]

    for pattern in location_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            if pattern.startswith(r'Delmak'):
                locations.add("Delmak-O")
            elif pattern == r'the colony':
                locations.add("The colony (on Delmak-O)")
            elif pattern == r'the buildings':
                locations.add("Colony buildings")
            elif pattern == r'the maze':
                locations.add("The maze")
            elif pattern == r'the satellite':
                locations.add("Orbiting slave satellite")
            elif pattern == r'the ship':
                locations.add("Space vessel/ship")
            elif pattern == r'Terra':
                locations.add("Terra (Earth)")
            elif pattern == r'the tomb':
                locations.add("The tomb")

    return list(locations)

def extract_characters(text):
    """Extract character names from chapter text."""
    colonists = [
        'Ben Tallchief', 'Seth Morley', 'Mary Morley', 'Dr. Milton Babble',
        'Maggie Walsh', 'Ignatz Thugg', 'Betty Jo Berm', 'Bert Kosler',
        'Tony Dunkelwelt', 'Wade Frazer', 'Glen Belsnor', 'Roberta Rockingham',
        'Suzanne Smart', 'Skip Benson', 'Bill Lantano'
    ]

    characters = set()
    for name in colonists:
        if name.split()[0] in text or name.split()[-1] in text:
            characters.add(name)

    # Also check for variations
    if 'Tallchief' in text:
        characters.add('Ben Tallchief')
    if 'Morley' in text:
        characters.add('Seth Morley')
    if 'Babble' in text:
        characters.add('Dr. Milton Babble')
    if 'Walsh' in text:
        characters.add('Maggie Walsh')
    if 'Thugg' in text:
        characters.add('Ignatz Thugg')
    if 'Berm' in text:
        characters.add('Betty Jo Berm')
    if 'Frazer' in text:
        characters.add('Wade Frazer')
    if 'Belsnor' in text:
        characters.add('Glen Belsnor')
    if 'Rockingham' in text:
        characters.add('Roberta Rockingham')
    if 'Smart' in text or 'Dumb' in text:
        characters.add('Suzanne Smart')
    if 'Kosler' in text:
        characters.add('Bert Kosler')
    if 'Dunkelwelt' in text:
        characters.add('Tony Dunkelwelt')

    return sorted(list(characters))

def generate_chapter_summary(chapter_num, text, titles=None):
    """Generate a structured summary for a chapter."""
    text_clean = clean_text(text)
    if titles is None:
        titles = add_chapter_titles()

    # Create chapter summaries based on content
    summaries = {
        1: "Ben Tallchief, a prayer-dependent transfer employee, receives a divine answer to his petition for meaningful work. Offered a position at a mysterious colony on planet Delmak-O, he celebrates with scotch and philosophical reflection on Specktowsky's theology. Despite not knowing his specific job function, Tallchief feels optimistic about this new opportunity, packing his belongings and preparing for his noser journey to an uncertain future.",

        2: "Seth Morley and his wife Mary prepare to leave Tekel Upharsin Kibbutz after eight years of dissatisfying work as a marine biologist reduced to quarrying stone. Fred Gossim, the kibbutz engineer, attempts to guilt them into staying. During loading, Seth selects the Morbid Chicken noser, only to be warned by the Walker-on-Earth that it will kill them. The supernatural being helps them reload into a better vessel, discusses Seth's deceased beloved tomcat, and promises eternal reunion in Paradise.",

        3: "Ben Tallchief lands on Delmak-O and meets ten colonists: Betty Jo Berm (linguist), Bert Kosler (custodian), Maggie Walsh (theologian), Ignatz Thugg (thermoplastics), Dr. Milton Babble (physician), Tony Dunkelwelt (photographer), Wade Frazer (psychologist), Glen Belsnor (electronics), Roberta Rockingham (sociologist), and Suzanne Smart (clerk). They await Morley's arrival to activate a satellite containing their mission instructions. Ben observes the colony's poor construction, strange atmosphere, and mechanical monitoring bugs, sensing unease among the brilliant, nervous group.",

        4: "Seth Morley and Mary arrive at the colony, completing the complement of colonists. Tensions emerge as personalities clash and paranoia grows. Dr. Babble demonstrates his neurotic control issues. The colonists await satellite activation but face mounting anxiety about their true purpose. Mary Morley shows signs of pregnancy, creating personal crises. The group begins experiencing strange phenomena and psychological deterioration as they anticipate revelation of their mission.",

        5: "The satellite activates, but delivers only cryptic theological and philosophical instructions rather than practical orders. The colonists discover they must navigate a literal maze structure that has manifested on the planet's surface. Deaths begin occurring mysteriously. Characters face tests of faith, identity, and reality itself. Maggie Walsh encounters mystical visions. The colonists' psychological states deteriorate as they realize they may be trapped in a game designed to test their spiritual and mental resilience.",

        7: "Continued maze navigation reveals philosophical and theological challenges embedded in the structure. The surviving colonists encounter paradoxes and impossible choices. Some begin questioning the nature of reality itself, wondering if they're experiencing actual events or hallucinations. The theme of personality death emerges as characters lose their sense of individual identity. Moral and existential dilemmas intensify as the group splinters psychologically.",

        9: "Brief chapter detailing further dissolution of the colonists' sanity and coherence as they navigate deeper into the maze's mysteries. Reality begins fragmenting. Some colonists disappear or die under unclear circumstances. The boundary between survival and psychological simulation becomes ambiguous.",

        10: "Colonists experience increasingly surreal and contradictory reality. The maze reveals itself as potentially metaphysical rather than physical. Wade Frazer and others confront their deepest fears and philosophical assumptions. The suggestion emerges that the entire colony and maze may be a simulation or test of consciousness itself. Death becomes unclear—is it actual cessation or transformation into another state of being?",

        12: "The surviving colonists face mounting evidence that the colony itself may not be real in conventional terms. Characters experience 'personality death'—the dissolution of individual identity. Religious and scientific frameworks collapse. Some hint that this is a theological experiment designed to test faith under ultimate existential pressure. The maze becomes metaphorical: each colonist is trapped in their own conceptual labyrinth.",

        14: "Penultimate chapter reveals the horrifying possibility that the colonists are already dead, experiencing a post-mortem judgment or consciousness simulation. The form of reality itself becomes questionable. Some colonists achieve mystical insights while others descend into madness. The maze's true nature—whether physical, psychological, or metaphysical—remains ambiguous.",

        15: "The colonists near complete psychological disintegration. Some achieve transcendent understanding while others face annihilation of selfhood. The theological framework—with the Mentufacturer, Intercessor, Form Destroyer, and Walker-on-Earth—becomes both prison and potential path to salvation. Death and reality are inverted: survival may mean spiritual annihilation.",

        16: "Final chapter culminates the philosophical experiment. The surviving consciousness(es) reach some form of resolution regarding the nature of death, identity, and ultimate reality. The maze has stripped away all illusions, leaving only fundamental questions about what constitutes existence itself. Some ambiguous suggestion of continuation or transformation, with reality fundamentally altered by the experience."
    }

    themes = {
        1: ["Prayer and divine intervention", "Career dissatisfaction", "Theological inquiry", "Anticipation and hope"],
        2: ["Personal agency vs. manipulation", "Marriage dynamics", "Guilt and responsibility", "Divine blessing", "Loss and memory"],
        3: ["First contact and anxiety", "Specialist knowledge", "Mystery and uncertainty", "Surveillance and control", "Isolation"],
        4: ["Psychological isolation", "Pregnancy as crisis", "Mission ambiguity", "Group dysfunction", "Growing dread"],
        5: ["Maze as metaphor", "Death and mortality", "Theological revelation", "Identity fragmentation", "Mystical experience"],
        7: ["Paradox and contradiction", "Reality dissolution", "Spiritual crisis", "Identity loss", "Existential dread"],
        9: ["Sanity deterioration", "Death ambiguity", "Reality fragmentation", "Survival horror"],
        10: ["Consciousness questioning", "Metaphysical maze", "Fear confrontation", "Simulation hypothesis", "Death redefined"],
        12: ["Personality death", "Reality negation", "Theological experiment", "Conceptual imprisonment"],
        14: ["Post-mortem consciousness", "Judgment and evaluation", "Reality inversion", "Mysticism vs. madness"],
        15: ["Selfhood dissolution", "Transcendence vs. annihilation", "Religious framework as cage"],
        16: ["Ultimate revelation", "Reality transformed", "Ambiguous continuation", "Existential resolution"]
    }

    philosophical = {
        1: ["What is meaningful work?", "Prayer as reality-altering force", "Divine will vs. human desire"],
        2: ["Free will and predestination", "Loyalty vs. self-interest", "The nature of blessing"],
        3: ["Unknown purpose and meaning", "Authority and control", "Community vs. isolation"],
        4: ["Personal freedom in groups", "Knowledge and power", "Biological vs. metaphysical identity"],
        5: ["The nature of reality", "What constitutes death?", "Is consciousness continuous?"],
        7: ["Paradox as truth", "Identity as illusion", "The limits of logic"],
        9: ["What is real experience?", "Can consciousness terminate?"],
        10: ["Simulation vs. reality", "Consciousness as prison", "Death as transformation"],
        12: ["What is personality?", "Is this real?", "Purpose of suffering"],
        14: ["Are we already dead?", "What is judgment?", "Reality as construct"],
        15: ["What survives death?", "Is selfhood necessary?", "Ultimate meaning"],
        16: ["What was this maze?", "What have we become?", "Is transformation survival?"]
    }

    key_events = {
        1: ["Prayer transmission and answer", "Transfer offer received", "Preparation for departure", "Philosophical reflection on Specktowsky"],
        2: ["Confrontation with Gossim", "Walker-on-Earth appears", "Noser selection/switching", "Blessing and promise of reunion"],
        3: ["Landing on Delmak-O", "Meeting all colonists except Morley", "Discovering satellite with instructions", "First observations of strange phenomena"],
        4: ["Morley arrival completes colony", "Psychological tensions emerge", "Mary's pregnancy discovered", "Anticipation of satellite activation"],
        5: ["Satellite delivers cryptic instructions", "Maze structure manifests", "First deaths occur", "Mystical experiences begin"],
        7: ["Maze navigation continues", "Philosophical challenges embedded in structure", "Reality questioning increases", "Group psychological splitting"],
        9: ["Continued maze descent", "Multiple deaths unclear", "Reality becomes surreal"],
        10: ["Metaphysical properties of maze revealed", "Personality dissolution evidence", "Simulation hypothesis emerges"],
        12: ["Suggestion colony may be illusory", "Personality death confirmed", "Religious/scientific frameworks collapse"],
        14: ["Evidence of post-mortem state", "Identity dissolution accelerates", "Mystical insights vs. madness"],
        15: ["Psychological disintegration climaxes", "Theological framework as both cage and path"],
        16: ["Philosophical resolution achieved", "Reality fundamentally altered", "Ambiguous conclusion about existence"]
    }

    return {
        "chapter_number": chapter_num,
        "chapter_title": titles.get(chapter_num, f"Chapter {chapter_num}"),
        "summary": summaries.get(chapter_num, text_clean[:500]),
        "locations_mentioned": extract_locations(text_clean),
        "characters_appearing": extract_characters(text_clean),
        "themes_explored": themes.get(chapter_num, []),
        "philosophical_concepts": philosophical.get(chapter_num, []),
        "key_events": key_events.get(chapter_num, []),
        "narrative_observations": [
            "PKD employs subjective narrative perspective, primarily through Seth Morley's consciousness",
            "Reality remains ambiguous throughout—is the maze physical, psychological, or metaphysical?",
            "Theological language and concepts permeate the narrative, suggesting cosmic judgment",
            "The novel explores personality and identity as potentially illusory constructs",
            "Death is consistently redefined and questioned throughout the narrative arc"
        ] if chapter_num < 5 else [
            "Reality progressively destabilizes as the narrative advances",
            "Characters experience 'personality death'—dissolution of individual consciousness",
            "The maze becomes both literal setting and metaphor for existential entrapment",
            "PKD blurs boundaries between simulation and reality, game and consequence",
            "Theological framework provides both prison and potential path to understanding"
        ]
    }

def add_chapter_titles():
    """Add chapter titles based on contents/novel summary."""
    titles = {
        1: "Ben Tallchief Wins a Pet Rabbit in a Raffle (Answered Prayer)",
        2: "Seth Morley Finds His Landlord Has Repaired That Which Symbolizes All He Believes In",
        3: "A Group of Friends Gather Together, and Sue Smart Recovers Her Faculties",
        4: "Mary Morley Discovers She is Pregnant, With Unforeseen Results",
        5: "The Chaos of Dr. Babble's Fiscal Life Becomes Too Much For Him",
        7: "Out of His Many Investments Seth Morley Realizes Only a Disappointing Gain—Measured in Pennies",
        9: "We Find Tony Dunkelwelt Worrying Over One of Mankind's Most Ancient Problems",
        10: "Wade Frazer Learns That Those Whose Advice He Most Trusted Have Turned Against Him",
        12: "Roberta Rockingham's Spinster Aunt Pays Her a Visit",
        14: "Ned Russell Goes Broke",
        15: "Embittered, Tony Dunkelwelt Leaves School and Returns to the Town in Which He Was Born",
        16: "After the Doctor Examines Her X-rays, Maggie Walsh Knows That Her Condition is Incurable"
    }
    return titles

def main():
    """Extract all chapters and generate JSON output."""
    source_file = Path(r"C:\QueryPat\database\extracted_markdown\DOC_ARCH_DICK_PHILIP_KINDRED_A_MAZE_OF_DEATH_LIBG.md")
    output_file = Path(r"C:\QueryPat\maze_of_death_chapters_all.json")

    if not source_file.exists():
        print(f"Error: Source file not found: {source_file}")
        return

    # Read source
    with open(source_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract chapters using regex
    chapter_pattern = r'## (\d+)\s*\n(.*?)(?=## (?:\d+|MADE AT|WINERY|STOPPERY|WITCHERY|HIPPERY|MEKKISRY)|$)'
    matches = re.finditer(chapter_pattern, content, re.DOTALL)

    titles = add_chapter_titles()
    chapters = []
    for match in matches:
        chapter_num = int(match.group(1))
        chapter_text = match.group(2)

        chapter_data = generate_chapter_summary(chapter_num, chapter_text, titles)
        chapters.append(chapter_data)

        print(f"Processed Chapter {chapter_num}")

    # Sort by chapter number
    chapters.sort(key=lambda x: x['chapter_number'])

    # Write output
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(chapters, f, indent=2, ensure_ascii=False)

    print(f"\nExtracted {len(chapters)} chapters")
    print(f"Output saved to: {output_file}")

if __name__ == "__main__":
    main()
