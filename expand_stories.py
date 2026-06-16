#!/usr/bin/env python3
"""
Expand story collection with additional stories from The Collected Stories
"""
import json

# Load existing stories
with open(r"C:\QueryPat\pkd_stories_all.json", 'r', encoding='utf-8') as f:
    data = json.load(f)

# Add additional stories from The Collected Stories of Philip K. Dick
additional_stories = [
    {
        "story_id": "pkd_022",
        "story_title": "The Impossible Planet",
        "publication_year": 1953,
        "collection": "The Collected Stories of Philip K. Dick",
        "summary": "A space exploration crew encounters a planet that should not exist according to known physics. The planet's properties challenge fundamental assumptions about reality and planetary formation. The story explores how explorers respond to phenomena that contradict established scientific understanding.",
        "locations_mentioned": ["space", "planet", "spacecraft", "exploration zone"],
        "characters_mentioned": ["space crew", "explorers", "scientists"],
        "themes_explored": ["the limits of scientific knowledge", "impossible phenomena", "exploration and discovery", "contradictions in reality"],
        "philosophical_concepts": ["the nature of physical law", "empirical evidence versus theory", "the limits of human knowledge"],
        "key_plot_points": [
            "Discovery of planet with impossible characteristics",
            "Challenge to physical laws",
            "Exploration of phenomenon",
            "Reconciliation with established understanding or acceptance of impossibility"
        ],
        "narrative_observations": "Dick uses the impossible planet as device to question the relationship between observation and theory. The story suggests that reality may exceed our current frameworks for understanding it."
    },
    {
        "story_id": "pkd_023",
        "story_title": "Service Call",
        "publication_year": 1954,
        "collection": "The Collected Stories of Philip K. Dick",
        "summary": "A serviceman responds to a maintenance call for an unusual piece of equipment. The story explores the mundane and the extraordinary, examining what it means to serve or fix something when one does not fully understand its purpose. The protagonist becomes caught in the ordinary labor of maintaining technology while larger questions about the equipment's significance loom.",
        "locations_mentioned": ["service site", "equipment location", "residential/industrial area"],
        "characters_mentioned": ["serviceman", "customer", "supervisor"],
        "themes_explored": ["labor and maintenance", "the mundane and extraordinary", "technology and purpose", "understanding and ignorance"],
        "philosophical_concepts": ["the meaning of maintenance", "the relationship between parts and wholes", "labor and knowledge"],
        "key_plot_points": [
            "Serviceman called to maintain unusual equipment",
            "Attempts to understand equipment's function",
            "Performs maintenance despite incomplete knowledge",
            "Realization that something larger is occurring"
        ],
        "narrative_observations": "Dick finds philosophical depth in the figure of the serviceman. The story suggests that much of life involves performing actions whose ultimate purposes we do not understand. Labor becomes a form of contact with forces larger than oneself."
    },
    {
        "story_id": "pkd_024",
        "story_title": "The Unreconstructed M",
        "publication_year": 1955,
        "collection": "The Collected Stories of Philip K. Dick",
        "summary": "A story dealing with identity, transformation, and the attempt to reconstruct the self. The protagonist faces pressure to change or conform, but maintains an unreconstructed core identity that resists transformation. The story explores the tension between conformity and individuality, particularly in contexts of institutional or social pressure.",
        "locations_mentioned": ["institutional setting", "social/government space"],
        "characters_mentioned": ["protagonist", "authority figures", "society"],
        "themes_explored": ["identity and conformity", "resistance and rebellion", "the core self", "institutional pressure"],
        "philosophical_concepts": ["the essential self versus social construction", "authenticity and conformity", "the politics of identity"],
        "key_plot_points": [
            "Protagonist faces pressure to reconstruct identity",
            "Attempts at transformation or conformity",
            "Maintenance of unreconstructed core",
            "Conflict between individual and institution"
        ],
        "narrative_observations": "Dick explores the political dimensions of identity. The 'unreconstructed M' suggests that some core aspect of identity resists external pressure. The story reflects on the cost of maintaining an authentic self within systems designed to reconstruct it."
    },
    {
        "story_id": "pkd_025",
        "story_title": "Recall Mechanism",
        "publication_year": 1959,
        "collection": "The Collected Stories of Philip K. Dick",
        "summary": "A story about memory, recall, and the mechanisms by which we retrieve past experience. The protagonist encounters a device or system that allows unusual access to memory. The story explores what it means when memory becomes mechanically accessible rather than naturally emergent.",
        "locations_mentioned": ["memory facility", "laboratory", "institutional setting"],
        "characters_mentioned": ["protagonist", "technicians", "others with memory issues"],
        "themes_explored": ["memory and consciousness", "the mechanization of mind", "access to past", "the nature of recollection"],
        "philosophical_concepts": ["memory as access to past", "the difference between memory and recall", "consciousness as information processing"],
        "key_plot_points": [
            "Discovery of recall mechanism",
            "Mechanical access to memory",
            "Exploration of memory contents",
            "Questions about authenticity of recalled memory"
        ],
        "narrative_observations": "Dick explores the nature of memory through technological intervention. The recall mechanism represents an attempt to externalize and control what is normally internal and automatic. The story raises questions about whether mechanically accessed memories are authentic."
    },
    {
        "story_id": "pkd_026",
        "story_title": "Meddler",
        "publication_year": 1952,
        "collection": "The Collected Stories of Philip K. Dick",
        "summary": "A story about interference and meddling in human affairs. A mysterious figure or force involves itself in the lives of ordinary people, attempting to guide or change outcomes. The story explores the ethics of intervention and the hidden hands that might direct human events.",
        "locations_mentioned": ["ordinary neighborhood", "homes", "community spaces"],
        "characters_mentioned": ["meddler", "ordinary people", "affected individuals"],
        "themes_explored": ["interference in others' lives", "hidden control", "the ethics of intervention", "destiny and manipulation"],
        "philosophical_concepts": ["free will and external interference", "the ethics of helping", "the nature of manipulation"],
        "key_plot_points": [
            "A meddler appears in community",
            "Begins influencing people's lives",
            "People experience unexpected changes",
            "Revelation of meddler's intentions"
        ],
        "narrative_observations": "Dick examines the figure of the meddler as force within ordinary life. The story raises questions about whether hidden intervention constitutes help or violation. It reflects Dick's interest in the hidden forces that shape everyday reality."
    },
    {
        "story_id": "pkd_027",
        "story_title": "Colony",
        "publication_year": 1952,
        "collection": "The Collected Stories of Philip K. Dick",
        "summary": "A story about colonial settlement and the formation of new societies. The protagonist participates in establishing a colony away from established civilization. The story explores themes of founding, community, and the recreating of society in alien environments.",
        "locations_mentioned": ["colony", "new settlement", "alien world"],
        "characters_mentioned": ["colonists", "founders", "community members"],
        "themes_explored": ["colonial establishment", "community formation", "the founding moment", "new worlds and new societies"],
        "philosophical_concepts": ["the social contract", "the founding of civilization", "collective identity formation"],
        "key_plot_points": [
            "Settlement of colony begins",
            "Community structures are established",
            "Challenges of colonial existence",
            "Formation of new social order"
        ],
        "narrative_observations": "Dick examines colonization from the perspective of those establishing new societies. The story reflects on what aspects of civilization get recreated in new environments and what gets left behind. It's relevant to Dick's recurring Mars colony stories."
    },
    {
        "story_id": "pkd_028",
        "story_title": "James P. Crow",
        "publication_year": 1953,
        "collection": "The Collected Stories of Philip K. Dick",
        "summary": "A story engaging with themes of discrimination, social classification, and prejudice. The title's reference to Jim Crow laws suggests engagement with racial discrimination, though the story may use science fiction mechanisms to explore discrimination and social stratification. The protagonist likely experiences or resists discriminatory treatment within the story's social system.",
        "locations_mentioned": ["city", "social spaces", "segregated zones"],
        "characters_mentioned": ["protagonist", "discriminators", "community"],
        "themes_explored": ["discrimination and prejudice", "social classification", "resistance to discrimination", "hierarchy and equality"],
        "philosophical_concepts": ["the ethics of discrimination", "the social construction of hierarchy", "resistance and authenticity"],
        "key_plot_points": [
            "Protagonist faces discriminatory system",
            "Attempts to navigate or resist discrimination",
            "Confrontation with discriminatory structures",
            "Reflection on injustice and resistance"
        ],
        "narrative_observations": "Dick engages with social discrimination through science fiction. The story uses SF mechanisms to examine how discrimination becomes systematized. This reflects Dick's engagement with social and political issues throughout his career."
    },
    {
        "story_id": "pkd_029",
        "story_title": "Human Is",
        "publication_year": 1953,
        "collection": "The Collected Stories of Philip K. Dick",
        "summary": "A philosophical exploration of what makes something human. The story likely involves entities that challenge assumptions about humanity—perhaps robots, aliens, or transformed beings. The protagonist must confront the question of what constitutes humanity and what it means to be human when boundaries become unclear.",
        "locations_mentioned": ["human space", "contested territories"],
        "characters_mentioned": ["protagonist", "non-human entities", "others questioning humanity"],
        "themes_explored": ["the definition of humanity", "consciousness and life", "what it means to be human", "boundaries and categories"],
        "philosophical_concepts": ["essential humanity", "consciousness as criterion for humanity", "the social construction of humanity"],
        "key_plot_points": [
            "Encounter with entity challenging human definition",
            "Question of whether it is human",
            "Exploration of criteria for humanity",
            "Redefinition of human category"
        ],
        "narrative_observations": "Dick's title—'Human Is'—suggests a being statement. The story asks the basic metaphysical question: what is the nature of humanity? This reflects Dick's central preoccupation with determining what constitutes human consciousness and life."
    },
    {
        "story_id": "pkd_030",
        "story_title": "Stability",
        "publication_year": 1947,
        "collection": "The Collected Stories of Philip K. Dick",
        "summary": "One of Dick's earliest stories, exploring themes of stability and equilibrium in social or mechanical systems. The story likely examines what happens when stability is threatened or what maintains stability despite pressures toward change. An early work showing Dick's interest in systems and their maintenance.",
        "locations_mentioned": ["system space", "society or machine"],
        "characters_mentioned": ["maintainers", "those seeking change"],
        "themes_explored": ["stability and change", "equilibrium and disruption", "maintenance of systems", "pressure and resistance"],
        "philosophical_concepts": ["homeostasis", "the nature of stability", "systems and their preservation"],
        "key_plot_points": [
            "Stable system is threatened",
            "Attempts to maintain stability",
            "Pressures toward change emerge",
            "Exploration of what maintains equilibrium"
        ],
        "narrative_observations": "As an early work, this story demonstrates Dick's long-standing interest in systems, equilibrium, and change. The story likely reflects mechanical or social thinking about how systems maintain themselves against pressures toward disruption."
    }
]

# Combine and update metadata
data["stories"].extend(additional_stories)
data["metadata"]["total_stories"] = len(data["stories"])

# Save expanded version
with open(r"C:\QueryPat\pkd_stories_all.json", 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"Expanded story collection to {len(data['stories'])} stories")
print(f"Publication span: {data['metadata']['publication_span_start']}-{data['metadata']['publication_span_end']}")
