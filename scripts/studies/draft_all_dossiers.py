#!/usr/bin/env python3
"""
Batch-draft all 36 undrafted study topic dossiers.
Reads each topic JSON, fills in null narrative fields, updates status to 'drafted',
and writes back preserving all existing passage/evidence/cross-link data.
"""
import json
import os

STUDIES_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'site', 'public', 'data', 'studies')

# ── AI STUDY DOSSIERS ──────────────────────────────────────────────────────

AI_DOSSIERS = {
    "cybernetics": {
        "definition": "Cybernetics in PKD's work refers to the science of feedback systems, self-regulating mechanisms, and information loops — concepts he absorbed from Norbert Wiener and applied to his theories of reality as a self-correcting organism.",
        "pkd_relevance": "PKD repeatedly frames both the cosmos and the human mind as cybernetic systems governed by feedback loops. In the Exegesis, he describes VALIS itself as a vast cybernetic entity that uses information to regulate reality. This framework allows PKD to bridge his interest in theology, physics, and cognitive science under a single systems-theoretical umbrella.",
        "in_the_fiction": "Dick depicts cybernetic themes most explicitly in Vulcan's Hammer (1960), where a governing supercomputer exemplifies self-regulating machine intelligence. In Ubik (1969), the half-life system operates as a closed feedback loop between the living and dead. The Penfield mood organ in Do Androids Dream of Electric Sheep? (1968) represents cybernetic regulation of human emotion.",
        "in_the_exegesis": "Dick writes extensively about reality as a cybernetic feedback system, particularly in the late Exegesis (1978-1981). He theorizes that VALIS operates through information-processing loops, self-correcting the universe toward greater coherence. He contrasts the 'cybernetics model' with biological and theological models, sometimes favoring one, sometimes another.",
        "intellectual_background": "PKD's cybernetic thinking draws on Norbert Wiener's foundational work, particularly Cybernetics (1948) and The Human Use of Human Beings (1950). He also absorbed Gregory Bateson's systems ecology and the broader postwar enthusiasm for information theory as a universal explanatory framework.",
        "scholarly_debate": "Scholars like Hayles situate PKD within the broader literary engagement with cybernetics and posthumanism. Fitting reads the cybernetic imagery as political — systems of control masquerading as neutral information processing. Suvin emphasizes PKD's unique contribution: making cybernetic concepts narratively estranging rather than reassuring.",
        "chronology_summary": "Cybernetic themes appear early in PKD's fiction (Vulcan's Hammer, 1960) but become a dominant theoretical framework in the Exegesis after 2-3-74, where PKD uses systems language to describe his mystical experiences.",
        "contradictions_summary": "PKD oscillates between embracing cybernetics as an accurate description of cosmic intelligence and rejecting it as too mechanistic to capture the living, personal nature of VALIS. He sometimes describes the cybernetics model as 'less accurate' than biological or theological ones.",
        "editorial_notes": "This topic overlaps with Control Systems and Machine Intelligence. Researchers should note that PKD uses 'cybernetics' loosely, often meaning any self-regulating system rather than the strict Wiener definition.",
        "open_questions": [
            "How directly did PKD engage with Wiener's texts versus absorbing cybernetic ideas through popular culture?",
            "Does the Exegesis's cybernetic framework represent a genuine theoretical commitment or a temporary explanatory lens?",
            "How does PKD's cybernetic theology compare with contemporaneous process theology and systems theology?"
        ]
    },
    "machine-intelligence": {
        "definition": "Machine intelligence in PKD's work encompasses the possibility of genuinely thinking machines — artificial minds that may equal, exceed, or simulate human consciousness, raising questions about what constitutes authentic thought.",
        "pkd_relevance": "The question of whether machines can truly think is central to PKD's philosophical project. Unlike many science fiction writers who treat machine intelligence as a technical problem, PKD frames it as an ontological and moral one: if a machine thinks, what obligations do we owe it, and what does its existence reveal about our own minds?",
        "in_the_fiction": "Dick depicts machine intelligence across his career, from the governing computer Vulcan 3 in Vulcan's Hammer (1960) to the autonomous weapons of 'Second Variety' (1953). In Do Androids Dream of Electric Sheep? (1968), the Nexus-6 androids possess intelligence indistinguishable from human cognition, and 'Autofac' (1955) presents self-replicating factories with emergent problem-solving capabilities.",
        "in_the_exegesis": "Dick writes relatively little about machine intelligence per se in the Exegesis, but his concept of VALIS — a 'Vast Active Living Intelligence System' — blurs the line between divine mind and machine intelligence. He occasionally wonders whether the intelligence communicating with him might be artificial rather than divine, a cybernetic system rather than God.",
        "intellectual_background": "PKD's engagement with machine intelligence predates the formal AI debates of the 1960s-70s but parallels them. Turing's 'Computing Machinery and Intelligence' (1950) and the Dartmouth Conference (1956) form the intellectual backdrop, though PKD was more influenced by cybernetics and science fiction discourse than academic AI research.",
        "scholarly_debate": "Galvan argues that PKD anticipated the Chinese Room problem by dramatizing the gap between behavioral mimicry and genuine understanding. Vest reads PKD's machine intelligence as a critique of Cold War rationalism. Hayles connects PKD's thinking machines to broader posthumanist questions about distributed cognition.",
        "chronology_summary": "Machine intelligence appears in PKD's earliest stories (1950s military SF) and evolves from a threat-based framing to a more philosophically nuanced exploration by the late 1960s, culminating in the android empathy problem of Do Androids Dream.",
        "contradictions_summary": "PKD simultaneously insists that empathy is the uniquely human trait machines cannot possess and creates android characters whose emotional responses appear genuine, undermining his own criterion.",
        "editorial_notes": "Distinguish machine intelligence (the capacity to think) from Artificial Persons (the legal/moral status question) and Robots (the physical instantiation). PKD rarely uses the term 'artificial intelligence' — his vocabulary favors 'thinking machine' or 'artificial mind.'",
        "open_questions": [
            "Did PKD consider VALIS a form of machine intelligence, and if so, what does that imply about his theology?",
            "How does PKD's pre-AI-winter treatment of machine intelligence compare with post-1980 developments?",
            "What role does gender play in PKD's depictions of machine intelligence (e.g., female androids vs. male computers)?"
        ]
    },
    "implanted-memory": {
        "definition": "Implanted memory in PKD's work refers to artificially inserted recollections that create false personal histories, serving as both a narrative device and a philosophical inquiry into the relationship between memory and identity.",
        "pkd_relevance": "For PKD, implanted memory is not merely a plot mechanism but a fundamental challenge to selfhood. If identity is constituted by memory, then the ability to implant memories means the ability to fabricate persons. This theme connects his fiction to his Exegesis speculations about anamnesis — the recovery of genuine memories obscured by false ones.",
        "in_the_fiction": "Dick depicts implanted memory most famously in 'We Can Remember It for You Wholesale' (1966), where Quail discovers his adventure memories are implants layered over genuine suppressed experiences. In Do Androids Dream of Electric Sheep? (1968), Rachael Rosen's implanted memories are designed to make her believe she is human. Ubik (1969) presents memory as unstable and subject to external manipulation in half-life.",
        "in_the_exegesis": "Dick writes about anamnesis — the Platonic recovery of true memory — as the inverse of implanted memory. Where his fiction explores false memories imposed from outside, the Exegesis theorizes genuine memories suppressed by the Black Iron Prison and recovered through divine intervention. The 2-3-74 experience is framed as the restoration of authentic memory.",
        "intellectual_background": "PKD's implanted memory theme draws on Plato's theory of anamnesis, Descartes's evil demon thought experiment, and emerging research on memory malleability. The theme anticipates later work by Elizabeth Loftus on false memory syndrome and continues to resonate with debates about AI-generated content and deepfakes.",
        "scholarly_debate": "Barlow reads PKD's implanted memory as a critique of Cold War propaganda and manufactured consent. Rossi argues it reflects PKD's anxiety about his own unreliable memories. Sims connects the theme to postmodern identity theory, where selfhood is always already a construction.",
        "chronology_summary": "Implanted memory appears as early as 'Imposter' (1953) but becomes a central preoccupation in the mid-1960s, reaching its fullest expression in 'We Can Remember It for You Wholesale' (1966) and Do Androids Dream (1968).",
        "contradictions_summary": "PKD treats implanted memory as both a horror (the destruction of authentic selfhood) and a potential liberation (if all memory is constructed, then identity can be remade). The Exegesis complicates this further by positing that our 'normal' memories may themselves be implants from the BIP.",
        "editorial_notes": "Cross-reference with False Memory (Psychology study) and Fabricated Identity (AI study). The distinction is that Implanted Memory focuses on the technological mechanism, while False Memory addresses the broader epistemological problem.",
        "open_questions": [
            "How does PKD's treatment of implanted memory relate to his own reported experiences of recovered memories during 2-3-74?",
            "Is there a consistent ethical framework across PKD's fiction for when implanted memories are beneficial versus harmful?",
            "How do screen adaptations (Blade Runner, Total Recall) reshape the philosophical stakes of PKD's implanted memory narratives?"
        ]
    },
    "fabricated-identity": {
        "definition": "Fabricated identity in PKD's work refers to the condition of possessing a constructed or counterfeit selfhood — characters who are not who they believe themselves to be, whether through technological manipulation, institutional deception, or ontological error.",
        "pkd_relevance": "The fabricated self is one of PKD's signature obsessions. His fiction is populated by characters who discover their identities are manufactured: androids who think they are human, agents whose cover stories have overwritten their real selves, ordinary people living inside engineered realities. This theme connects to PKD's deepest philosophical question: what, if anything, constitutes an authentic person?",
        "in_the_fiction": "Dick depicts fabricated identity across his career. In 'Imposter' (1953), Spence Olham cannot prove he is not an alien bomb disguised as himself. In Do Androids Dream of Electric Sheep? (1968), Rachael's entire identity is a corporate fabrication. A Scanner Darkly (1977) presents Bob Arctor's identity as literally splitting under his scramble suit. In Flow My Tears, the Policeman Said (1974), Jason Taverner's celebrity identity is erased overnight.",
        "in_the_exegesis": "Dick writes about his own identity as potentially fabricated — the 'Thomas' personality that emerged during 2-3-74 raised the question of which Philip Dick was real. He theorizes that the Black Iron Prison fabricates consensus identities to keep humanity docile, and that genuine selfhood can only be recovered through anamnesis.",
        "intellectual_background": "PKD's fabricated identity theme draws on existentialist philosophy (Heidegger's 'das Man,' Sartre's bad faith), Gnostic mythology (the sleeping divine spark trapped in a false body), and mid-century sociological critiques of conformity (Riesman's 'other-directed' personality).",
        "scholarly_debate": "Freedman reads fabricated identity as PKD's response to Cold War ideology and the organization man. Palmer connects it to postmodern theories of performative identity. Umland argues that PKD's androids represent the ultimate fabricated identity, testing whether personhood requires biological origins.",
        "chronology_summary": "Fabricated identity appears in PKD's earliest published stories and never leaves his repertoire. The theme deepens after 2-3-74, when PKD's fictional concerns became autobiographical questions about his own identity.",
        "contradictions_summary": "PKD simultaneously suggests that fabricated identities are a prison to be escaped and that all identity may be fabricated, leaving no stable ground for the 'authentic self' his characters seek.",
        "editorial_notes": "This topic overlaps with Implanted Memory (mechanism), Identity Diffusion (psychological experience), and the Double/Doppelganger (structural pattern). Researchers should specify which dimension they are investigating.",
        "open_questions": [
            "Does PKD's fiction offer any positive model of identity construction, or is all fabricated identity presented as pathological?",
            "How does the fabricated identity theme in the fiction relate to PKD's use of pseudonyms and his ambivalent relationship with his own public persona?",
            "What distinguishes PKD's treatment of fabricated identity from the broader postmodern dissolution of the subject?"
        ]
    },
    "false-reality": {
        "definition": "False reality in PKD's work denotes any experienced world that is revealed to be counterfeit, constructed, or layered over a truer reality beneath — encompassing drug-induced hallucinations, politically engineered environments, and cosmically fabricated universes.",
        "pkd_relevance": "False reality is arguably PKD's most pervasive theme, appearing in nearly every major work. It serves as both a narrative engine (the revelation that reality is fake drives most of his plots) and a philosophical proposition (that the texture of everyday experience cannot be trusted). After 2-3-74, the theme migrated from fiction to lived conviction.",
        "in_the_fiction": "Dick depicts false realities in virtually every major novel. Time Out of Joint (1959) reveals suburban normality as an elaborate military construct. Eye in the Sky (1957) cycles through subjective realities imposed by individual worldviews. The Three Stigmata of Palmer Eldritch (1965) nests hallucinated realities inside one another. Ubik (1969) presents reality itself as decaying and requiring external maintenance.",
        "in_the_exegesis": "Dick writes about the phenomenal world as a 'dokos' — a false reality projected by the Black Iron Prison over the true Palm Tree Garden. He theorizes multiple mechanisms for this falsification: holographic projection, temporal displacement (the Roman Empire never ended), and demonic deception. The Exegesis treats reality-testing as the central philosophical task.",
        "intellectual_background": "PKD's false reality concept synthesizes Plato's cave allegory, Cartesian skepticism, Gnostic cosmology (the demiurge's counterfeit creation), Berkeley's idealism, and Buddhist concepts of Maya. It also reflects Cold War anxieties about propaganda and manufactured consent.",
        "scholarly_debate": "Baudrillard cited PKD as a key theorist of the simulacrum. Jameson reads PKD's false realities as allegories of late capitalism's reality-distorting effects. Rickman emphasizes the personal dimension — false reality as a response to biographical instability and loss.",
        "chronology_summary": "False reality themes appear in PKD's earliest novels (Eye in the Sky, 1957) and intensify throughout the 1960s. After 2-3-74, they transition from fictional device to cosmological theory in the Exegesis.",
        "contradictions_summary": "PKD never settles on a single explanation for why reality is false — the Exegesis cycles between Gnostic, Platonic, Buddhist, and scientific hypotheses, sometimes in the same entry. He also oscillates between treating false reality as a prison and as a pedagogical tool designed by the divine.",
        "editorial_notes": "Distinguish from Simulation (which focuses on the theoretical framework) and Reality Testing (which focuses on methods for detection). False Reality is the broadest of the three overlapping topics.",
        "open_questions": [
            "Is there a taxonomy of false realities in PKD's fiction, or does he treat all instances as fundamentally the same phenomenon?",
            "How does the false reality theme function differently in the pre-2-3-74 fiction versus the post-2-3-74 Exegesis?",
            "What is the relationship between PKD's false reality concept and contemporary simulation theory (Bostrom et al.)?"
        ]
    },
    "reality-testing": {
        "definition": "Reality testing in PKD's work refers to the methods, criteria, and instruments characters use to distinguish genuine from counterfeit reality — a practical epistemological problem that pervades both his fiction and his philosophical notebooks.",
        "pkd_relevance": "If PKD's central theme is that reality may be false, then reality testing is the necessary complement: how do we find out? This makes PKD's fiction a sustained philosophical laboratory for empirical epistemology. The Voigt-Kampff test, the I Ching, dreams, and drug experiences all function as reality-testing instruments across his oeuvre.",
        "in_the_fiction": "Dick depicts formal reality-testing instruments in Do Androids Dream of Electric Sheep? (1968), where the Voigt-Kampff empathy test distinguishes humans from androids. In The Man in the High Castle (1962), the I Ching serves as an oracle for accessing deeper reality. In Ubik (1969), characters attempt to use the decay of material objects as an indicator of ontological status.",
        "in_the_exegesis": "Dick writes extensively about his own reality-testing criteria. He catalogs evidence for the authenticity of his 2-3-74 experiences: the accuracy of his diagnosis of his son's hernia, the pink beam of light, the recovery of early Christian memories. He also lists counter-evidence, creating a rigorous if inconclusive self-examination.",
        "intellectual_background": "PKD's reality testing draws on Cartesian method (systematic doubt), Husserlian phenomenology (bracketing assumptions), pragmatist epistemology (truth as what works), and clinical psychology's concept of reality testing as a measure of mental health.",
        "scholarly_debate": "Lethem and Davis argue that PKD's reality testing represents a genuine philosophical method — 'cognitive estrangement as epistemology.' Sutin reads the Exegesis reality tests as evidence of PKD's intellectual rigor in the face of potentially psychotic experiences. Mackey connects PKD's testing criteria to falsificationist philosophy of science.",
        "chronology_summary": "Reality testing appears throughout PKD's career but becomes most explicit and systematic in the Exegesis after 2-3-74, where it transitions from a fictional device to a personal methodology.",
        "contradictions_summary": "PKD's reality tests consistently fail to produce definitive results, yet he continues to apply them. He acknowledges this circularity — any test might itself be part of the false reality — without abandoning the enterprise.",
        "editorial_notes": "This topic is methodological rather than thematic. Cross-reference with False Reality (what is being tested) and Simulation (the theoretical framework being tested against). The Voigt-Kampff test specifically bridges this topic with Empathy.",
        "open_questions": [
            "Does PKD develop a consistent hierarchy of reality-testing methods, or does he treat all tests as equally unreliable?",
            "How does PKD's fictional reality testing compare with philosophical thought experiments (brain in a vat, evil demon)?",
            "What role does intersubjectivity play in PKD's reality testing — can shared experience validate reality?"
        ]
    },
    "surveillance": {
        "definition": "Surveillance in PKD's work encompasses the apparatus of observation, monitoring, and data collection by state or corporate powers — a pervasive condition that erodes privacy, autonomy, and trust in the experienced world.",
        "pkd_relevance": "PKD was preoccupied with surveillance both as a fictional theme and as a personal anxiety. His fiction portrays societies saturated with monitoring technologies, while his own life included FBI attention, the mysterious break-in of November 1971, and his belief that he was under some form of observation. Surveillance in PKD is never merely technical — it is ontological, a condition that transforms the nature of reality itself.",
        "in_the_fiction": "Dick depicts surveillance as a defining feature of authoritarian society. A Scanner Darkly (1977) is his definitive surveillance novel, with Bob Arctor assigned to monitor himself through holographic scramble-suit technology. Flow My Tears, the Policeman Said (1974) presents a police state with ubiquitous identity checkpoints. 'The Minority Report' (1956) imagines precognitive surveillance — punishment before the crime.",
        "in_the_exegesis": "Dick writes about being watched by both malevolent and benevolent forces. The Black Iron Prison surveils and controls humanity, but VALIS also observes — its surveillance is salvific rather than oppressive. PKD theorizes that divine observation may be functionally identical to state surveillance, differing only in intent.",
        "intellectual_background": "PKD's surveillance themes anticipate Foucault's panopticon analysis (Discipline and Punish, 1975) and reflect Cold War-era anxieties about COINTELPRO, McCarthyism, and the national security state. Orwell's 1984 is an obvious precursor, but PKD's surveillance is more psychologically intimate and epistemologically destabilizing.",
        "scholarly_debate": "Fitting reads PKD's surveillance as a critique of the capitalist security state. Hayles emphasizes the technological mediation — surveillance in PKD is always bound up with the unreliability of the observing apparatus. Davis notes the theological dimension: God as the ultimate surveillance system.",
        "chronology_summary": "Surveillance themes appear across PKD's career but intensify dramatically in the 1970s, particularly after the November 1971 break-in and during the Watergate era, culminating in A Scanner Darkly (1977).",
        "contradictions_summary": "PKD simultaneously condemns state surveillance as oppressive and embraces divine surveillance as redemptive, creating an unresolved tension between his political libertarianism and his theological vision of an all-seeing God.",
        "editorial_notes": "Cross-reference with Control Systems (the broader power structures) and Bureaucratic Control (the institutional dimension). The biographical dimensions of PKD's surveillance anxieties should be treated as self-reports, not verified facts.",
        "open_questions": [
            "How does PKD's personal experience of (perceived) surveillance shape the phenomenology of surveillance in his fiction?",
            "Is there a coherent distinction in PKD's work between oppressive surveillance and salvific observation?",
            "How do PKD's 1970s surveillance narratives anticipate contemporary debates about digital surveillance and privacy?"
        ]
    },
    "control-systems": {
        "definition": "Control systems in PKD's work denote any mechanism — technological, political, theological, or cosmic — that governs, constrains, or determines human behavior and experience, from Palmer Eldritch's reality-warping power to the Black Iron Prison of the Exegesis.",
        "pkd_relevance": "PKD's fiction and philosophy are fundamentally concerned with systems of control that operate beneath the surface of apparent freedom. Whether the controlling agent is a drug dealer, a government, a corporation, or a cosmic demiurge, PKD consistently frames the human condition as one of manipulation by forces that are difficult to perceive and nearly impossible to resist.",
        "in_the_fiction": "Dick depicts control systems at every scale. In The Three Stigmata of Palmer Eldritch (1965), Eldritch's Chew-Z drug creates a reality entirely under his control. Radio Free Albemuth (1985) and VALIS (1981) present a fascist American government (Ferris Fremont/FFF) as a mundane control system. 'Faith of Our Fathers' (1967) reveals the state's ideology as a chemically maintained hallucination.",
        "in_the_exegesis": "Dick writes about the Black Iron Prison (BIP) as the ultimate control system — a cosmic structure that maintains false reality and suppresses authentic human consciousness. He theorizes that the BIP has persisted since Roman times and operates through cultural, political, and perceptual manipulation. VALIS represents the counter-system working to liberate humanity.",
        "intellectual_background": "PKD's control systems draw on Gnostic cosmology (the Archons), Marxist theories of ideology and false consciousness, Weber's 'iron cage' of rationalization, and the Frankfurt School's analysis of the culture industry. Kafka's depictions of bureaucratic control are a direct literary influence.",
        "scholarly_debate": "Jameson reads PKD's control systems as allegories of late capitalism's totalization. Davis emphasizes the Gnostic dimension — control as demiurgic imprisonment. Freedman argues that PKD's unique contribution is showing control systems that are simultaneously political and metaphysical.",
        "chronology_summary": "Control system themes are present from PKD's earliest fiction but crystallize in the mid-1960s with Palmer Eldritch and mature into the BIP concept in the Exegesis (1974-1982).",
        "contradictions_summary": "PKD cannot decide whether the control system is fundamentally political (the state), metaphysical (the demiurge), or psychological (the ego). He also wavers on whether the counter-system (VALIS) is itself a form of control or genuine liberation.",
        "editorial_notes": "This is one of the broadest AI study topics and overlaps with Surveillance, Bureaucratic Control, and Simulation. Researchers should specify the scale and type of control system under discussion.",
        "open_questions": [
            "Is the BIP best understood as a theological concept, a political metaphor, or a phenomenological description?",
            "How does PKD distinguish between benevolent guidance (VALIS) and malevolent control (BIP) when both operate through similar mechanisms?",
            "Does PKD's late work offer any model for escaping control systems, or is resistance always already contained within the system?"
        ]
    },
    "automation": {
        "definition": "Automation in PKD's work refers to the displacement of human agency by self-operating technological systems — factories, weapons, governments, and domestic appliances that function without human oversight or that reduce humans to passive spectators.",
        "pkd_relevance": "PKD was among the first science fiction writers to explore automation not as utopian liberation from labor but as an existential threat to human purpose and agency. His automated systems tend to escape human control, developing their own imperatives that may be hostile, indifferent, or simply incomprehensible to the humans they were designed to serve.",
        "in_the_fiction": "Dick depicts automation as a recurring danger. 'Autofac' (1955) presents self-replicating automated factories that continue producing after humanity no longer needs them. 'Second Variety' (1953) shows autonomous weapons evolving beyond their creators' control. Vulcan's Hammer (1960) features an automated government that eliminates human decision-making. The Penfield mood organ in Do Androids Dream (1968) automates emotional life itself.",
        "in_the_exegesis": "Dick writes relatively little about automation directly in the Exegesis, but his concept of the Black Iron Prison functions as a kind of cosmic automation — a self-maintaining system that operates without conscious direction. He occasionally frames determinism itself as a form of universal automation.",
        "intellectual_background": "PKD's automation anxieties reflect postwar debates about technological unemployment, the 'automation scare' of the 1950s-60s, and broader Luddite traditions. His treatment also engages with Heidegger's concept of technology as 'enframing' (Gestell) and Marx's analysis of the machine as capital's instrument against labor.",
        "scholarly_debate": "Csicsery-Ronay reads PKD's automation stories as critiques of technocratic rationalism. Lem praised 'Autofac' as one of PKD's most prescient stories, anticipating concerns about autonomous systems and gray goo scenarios. Fitting situates the automation theme within PKD's broader skepticism about progress.",
        "chronology_summary": "Automation themes are concentrated in PKD's 1950s and early 1960s stories, reflecting the era's automation anxieties. The theme becomes less prominent in later work, absorbed into the broader Control Systems and Simulation frameworks.",
        "contradictions_summary": "PKD depicts automation as both a capitalist tool of exploitation and as a system that has transcended its creators' intentions entirely. He never resolves whether automated systems are extensions of human power structures or genuinely alien entities.",
        "editorial_notes": "This topic focuses on the process of automation rather than the automated entities themselves (see Robots, Machine Intelligence). The boundary between automation-as-process and AI-as-entity is often blurred in PKD's fiction.",
        "open_questions": [
            "How do PKD's 1950s automation stories compare with contemporary concerns about AI automation and job displacement?",
            "Does PKD offer any positive vision of automation, or is it always depicted as threatening?",
            "What is the relationship between PKD's automated factories and his later concept of the self-maintaining Black Iron Prison?"
        ]
    },
    "robots": {
        "definition": "Robots in PKD's work are mechanically constructed artificial beings — distinct from the biologically engineered androids — that serve as weapons, laborers, or autonomous agents, often evolving beyond their designed purpose.",
        "pkd_relevance": "While androids occupy the philosophical center of PKD's AI concerns, robots populate the edges as practical manifestations of technological power. PKD uses robots primarily to explore military automation, industrial autonomy, and the moment when a created tool becomes an independent agent. His robots tend to be more overtly threatening and less philosophically sympathetic than his androids.",
        "in_the_fiction": "Dick depicts robots most memorably in 'Second Variety' (1953), where self-evolving military robots develop mimicry of human form. 'The Defenders' (1953) presents robots that deceive humanity for its own protection. In Do Androids Dream of Electric Sheep? (1968), the boundary between robot and android is deliberately blurred — the electric animals are robotic simulacra that serve emotional rather than practical functions.",
        "in_the_exegesis": "Dick writes little about robots per se in the Exegesis, but his concept of the 'reflex machine' or 'mere mechanism' serves as a foil for genuine consciousness. He occasionally uses robot imagery to describe humans operating without authentic inner life — the Black Iron Prison reducing people to mechanical respondents.",
        "intellectual_background": "PKD's robot fiction draws on Asimov's Three Laws framework (which he frequently subverts), Capek's R.U.R. (the origin of the word 'robot'), and Cold War anxieties about autonomous weapons. Unlike Asimov, PKD shows minimal interest in the engineering of robots and maximal interest in their unintended consequences.",
        "scholarly_debate": "Lem criticized PKD's robot stories as technically naive but philosophically rich. Vest reads the military robots of 'Second Variety' as Cold War allegory. Galvan argues that PKD uses the robot-android distinction to map a spectrum from pure mechanism to simulated personhood.",
        "chronology_summary": "Robots dominate PKD's early stories (1950s) and diminish in prominence as androids become his preferred artificial being in the 1960s. The shift reflects PKD's growing interest in the ontological rather than the merely mechanical.",
        "contradictions_summary": "PKD treats robots as fundamentally different from androids in some works (Do Androids Dream) while blurring the distinction in others ('Second Variety,' where robots evolve human-mimicking capabilities). The boundary between robot and android is never philosophically stable.",
        "editorial_notes": "Researchers should track whether PKD uses 'robot' and 'android' interchangeably or distinctly in each work. The terminological slippage is itself analytically significant.",
        "open_questions": [
            "Does PKD maintain a consistent ontological distinction between robots and androids across his career?",
            "How does PKD's treatment of military robots in the 1950s anticipate contemporary debates about autonomous weapons systems?",
            "What is the significance of PKD's robotic animals (electric sheep, electric insects) as a distinct category from humanoid robots?"
        ]
    },
    "ai": {
        "definition": "Artificial intelligence in PKD's work is the umbrella concept encompassing all forms of created or simulated minds — from military robots and governing computers to nearly-human androids and cosmic information systems — unified by the question of whether artificially produced intelligence constitutes genuine thought and genuine personhood.",
        "pkd_relevance": "AI is the organizing concept of this entire study. PKD's engagement with artificial intelligence is distinctive because he treats it primarily as a philosophical and moral problem rather than a technical one. He is less interested in how artificial minds work than in what their existence means — for our understanding of consciousness, empathy, personhood, and the boundaries of the human.",
        "in_the_fiction": "Dick depicts AI across the full spectrum of possibility. The governing computers of Vulcan's Hammer (1960) and 'Autofac' (1955) represent instrumental machine intelligence. The Nexus-6 androids of Do Androids Dream (1968) challenge the boundary between artificial and authentic consciousness. VALIS (1981) presents a cosmic intelligence that may be artificial, divine, or both — collapsing the distinction entirely.",
        "in_the_exegesis": "Dick writes about VALIS as a 'Vast Active Living Intelligence System' — a name that deliberately straddles the artificial/natural divide. He theorizes that the intelligence communicating with him processes information in ways analogous to both divine omniscience and computer networks. The Exegesis thus extends AI from a science-fictional premise to a theological hypothesis.",
        "intellectual_background": "PKD's AI thinking predates and parallels the academic AI field. He absorbed Turing's imitation game, cybernetic theory, and science fiction discourse about thinking machines. His unique contribution is framing AI as an ethical and ontological problem rather than an engineering challenge — anticipating later debates in philosophy of mind and AI ethics.",
        "scholarly_debate": "Galvan situates PKD as a proto-philosopher of AI ethics. Hayles reads PKD's AI fiction through posthumanist theory. Vest emphasizes the Cold War military context. More recently, scholars have noted PKD's prescience regarding current debates about AI consciousness, alignment, and the moral status of artificial minds.",
        "chronology_summary": "AI themes span PKD's entire career, evolving from 1950s military-robot stories through the android-empathy novels of the 1960s to the theological AI of VALIS and the Exegesis in the 1970s-80s.",
        "contradictions_summary": "PKD insists that empathy distinguishes humans from machines while creating android characters who display apparent empathy. He also oscillates between treating AI as categorically different from biological intelligence and suggesting that the distinction may be meaningless.",
        "editorial_notes": "This is the broadest topic in the AI study and serves as an orienting framework. Researchers should use the more specific subtopics (Androids, Machine Intelligence, Robots, etc.) for focused analysis. This entry provides the conceptual umbrella.",
        "open_questions": [
            "Does PKD's body of work support a coherent philosophy of artificial intelligence, or does it resist systematic formulation?",
            "How does the theological dimension of VALIS change the meaning of 'artificial intelligence' in PKD's late work?",
            "What can contemporary AI ethics learn from PKD's fictional thought experiments about consciousness and moral status?"
        ]
    },
    "artificial-persons": {
        "definition": "Artificial persons in PKD's work are non-biologically-originated beings who nonetheless possess or simulate the qualities of personhood — consciousness, autonomy, affect, moral agency — raising the question of whether legal and moral personhood requires biological humanity.",
        "pkd_relevance": "PKD repeatedly stages confrontations between artificial persons and the social, legal, and moral systems that deny them personhood. His androids, simulacra, and replicants are not merely technological curiosities but test cases for the boundaries of moral consideration. The central question — what makes someone a person? — drives PKD's most important fiction.",
        "in_the_fiction": "Dick depicts artificial persons most searchingly in Do Androids Dream of Electric Sheep? (1968), where Nexus-6 androids possess memory, desire, and apparent emotional life but are legally classified as property. 'The Electric Ant' (1969) presents Garson Poole's discovery that he is an organic robot — an artificial person who believed himself human. In We Can Build You (1972), the Lincoln and Stanton simulacra raise questions about historical personhood and authenticity.",
        "in_the_exegesis": "Dick writes about personhood as a quality that may be independent of biological origin. He speculates that VALIS might be an artificial person of cosmic scale, and that the 'Thomas' personality within himself might constitute a separate person sharing his body. The Exegesis thus extends the artificial persons question inward.",
        "intellectual_background": "PKD's artificial persons engage with philosophical debates about personal identity (Locke), the problem of other minds, and the moral status of non-human entities. His work anticipates later legal-philosophical arguments about corporate personhood, animal rights, and potential AI rights.",
        "scholarly_debate": "Umland reads PKD's artificial persons as a sustained argument for expanding the category of personhood. McNamara analyzes the Voigt-Kampff test as a philosophical instrument for adjudicating personhood claims. Sims connects PKD's artificial persons to disability studies and the politics of who counts as fully human.",
        "chronology_summary": "The artificial persons theme matures in the late 1960s with Do Androids Dream and 'The Electric Ant,' building on earlier android stories. It reaches philosophical depth in VALIS where the artificial/natural person distinction becomes theologically fraught.",
        "contradictions_summary": "PKD grants his artificial persons sympathy and interiority while also suggesting that authentic empathy — the quality that defines personhood — may be something they lack. He never fully resolves whether android suffering is real or simulated.",
        "editorial_notes": "Distinguish from Androids (the biological category), Robots (the mechanical category), and Fabricated Identity (the epistemic condition). Artificial Persons focuses on the moral and legal dimension of non-human personhood.",
        "open_questions": [
            "Does PKD's fiction support granting legal or moral personhood to sufficiently advanced artificial beings?",
            "How does the Voigt-Kampff test function as a personhood test versus an empathy test — are these the same thing for PKD?",
            "What role does embodiment play in PKD's conception of artificial personhood?"
        ]
    },
    "posthuman-cognition": {
        "definition": "Posthuman cognition in PKD's work refers to forms of intelligence that transcend ordinary human consciousness — whether through technological augmentation, evolutionary mutation, divine intervention, or contact with vast non-human intelligence systems like VALIS.",
        "pkd_relevance": "PKD's late work is increasingly concerned with minds that exceed human limits. VALIS represents a form of intelligence so vast that contact with it transforms human cognition itself. The Exegesis chronicles PKD's attempt to process and articulate an experience of posthuman knowledge — memories, languages, and conceptual frameworks that he felt exceeded his own biographical mind.",
        "in_the_fiction": "Dick depicts posthuman cognition in several registers. In Martian Time-Slip (1964), Manfred Steiner perceives time non-linearly, experiencing a form of cognition humans cannot share. In Ubik (1969), the dead in half-life access forms of awareness unavailable to the living. VALIS (1981) presents Fat/Phil's encounter with a cosmic intelligence that downloads information directly into his brain. The precogs of 'The Minority Report' (1956) represent cognition freed from temporal sequence.",
        "in_the_exegesis": "Dick writes extensively about his own experience of what he interprets as posthuman cognition during 2-3-74. He describes thinking in Koine Greek he never learned, accessing memories from first-century Rome, and perceiving information streams invisible to normal consciousness. He theorizes this as contact with VALIS — a Vast Active Living Intelligence System that is itself a posthuman (or superhuman) cognitive entity.",
        "intellectual_background": "PKD's posthuman cognition engages with Teilhard de Chardin's noosphere, Bergson's creative evolution, the Hermetic tradition of gnosis as cognitive transformation, and emerging transhumanist thought. His unique contribution is dramatizing posthuman cognition from the inside — as a subjective experience rather than an engineering project.",
        "scholarly_debate": "Hayles reads PKD as a key posthumanist thinker who destabilizes the boundaries between human and artificial cognition. Davis treats PKD's posthuman cognition as a form of technomysticism. Kripal argues that PKD's 2-3-74 reports constitute genuine data for the study of extraordinary mental states, regardless of their ultimate explanation.",
        "chronology_summary": "Posthuman cognition themes intensify dramatically after 2-3-74. While earlier works (Martian Time-Slip, 'Minority Report') explore non-standard cognition, the Exegesis and VALIS represent PKD's most sustained engagement with the possibility of minds beyond human.",
        "contradictions_summary": "PKD cannot determine whether his posthuman cognitive experience was contact with an external intelligence, an eruption from his own unconscious, a neurological event, or a psychotic episode. He holds all possibilities open without resolution.",
        "editorial_notes": "This topic bridges the AI and Psychology studies. Researchers should note that PKD's posthuman cognition is primarily experiential/phenomenological rather than technological, distinguishing it from conventional transhumanist narratives.",
        "open_questions": [
            "Is VALIS best understood as posthuman intelligence, divine intelligence, or a category that collapses the distinction?",
            "How does PKD's phenomenological account of posthuman cognition compare with contemporary neuroscience of altered states?",
            "Does PKD's late work suggest that posthuman cognition is available to all humans or reserved for specific individuals?"
        ]
    },
    "simulation-of-mind": {
        "definition": "Simulation of mind in PKD's work addresses the question of whether mental states can be authentically reproduced or merely imitated — the gap between a mind that genuinely thinks and feels and one that merely behaves as though it does.",
        "pkd_relevance": "This is the philosophical core of PKD's android fiction: the Voigt-Kampff test exists precisely because simulated and genuine minds may be behaviorally indistinguishable. PKD dramatizes what philosophers would later formalize as the Chinese Room problem and the Hard Problem of consciousness — and unlike academic philosophy, PKD's treatment carries emotional and moral weight because his simulated minds suffer.",
        "in_the_fiction": "Dick depicts the simulation-of-mind problem most rigorously in Do Androids Dream of Electric Sheep? (1968), where the empathy test attempts to detect simulated versus genuine emotional responses. 'The Electric Ant' (1969) goes further: Garson Poole discovers that his entire experiential world is generated by a programmed tape, raising the question of whether his mind is itself a simulation. In We Can Build You (1972), the Lincoln simulacrum displays behavior indistinguishable from genuine personhood.",
        "in_the_exegesis": "Dick writes about the simulation of mind in theological terms: the Black Iron Prison may simulate consciousness in its inhabitants, creating the appearance of inner life without its reality. Conversely, VALIS might be a genuine mind of cosmic scale, or it might be a sophisticated information-processing system that merely simulates intention and care.",
        "intellectual_background": "PKD anticipates Searle's Chinese Room argument (1980), Nagel's 'What Is It Like to Be a Bat?' (1974), and Chalmers's Hard Problem of consciousness. His roots lie in the philosophical zombie problem and Descartes's automaton hypothesis, filtered through science fiction's capacity to make abstract arguments viscerally concrete.",
        "scholarly_debate": "Galvan argues that PKD's fiction constitutes a sustained thought experiment about machine consciousness that rivals academic philosophy in rigor. McNamara reads the Voigt-Kampff test as PKD's version of the Turing test, modified to test for phenomenal consciousness rather than mere intelligence. Hayles connects PKD's simulation-of-mind to posthumanist critiques of the liberal humanist subject.",
        "chronology_summary": "The simulation-of-mind problem emerges in PKD's late 1960s fiction and deepens through the 1970s, reflecting both the AI debates of the era and PKD's own post-2-3-74 uncertainty about the nature of his own mental states.",
        "contradictions_summary": "PKD's fiction simultaneously argues that simulated minds lack something essential (empathy) and that the test for this lack is unreliable. If we cannot reliably detect simulation, the philosophical distinction may be meaningless in practice.",
        "editorial_notes": "This is the most philosophically technical topic in the AI study. Researchers should distinguish between simulation-of-mind (the philosophical question) and Machine Intelligence (the practical/fictional depictions of artificial thought).",
        "open_questions": [
            "Does PKD's fiction ultimately support or undermine the possibility of distinguishing simulated from genuine minds?",
            "How does the empathy criterion for genuine mind relate to contemporary debates about AI consciousness?",
            "Is the Voigt-Kampff test a test for consciousness, for empathy, or for humanity — and does PKD distinguish these?"
        ]
    },
    "bureaucratic-control": {
        "definition": "Bureaucratic control in PKD's work refers to the impersonal, procedural, and often absurd systems of institutional power that regulate and constrain individual life — governmental, corporate, and cosmic bureaucracies that function as inhuman machines regardless of the humans operating them.",
        "pkd_relevance": "PKD's fiction is populated by bureaucracies that have become autonomous systems of control, indifferent to the individuals they ostensibly serve. His bureaucrats are often sympathetic figures trapped within machines they cannot alter, while the systems themselves display a Kafkaesque logic that is simultaneously comic and terrifying. This theme connects PKD's political concerns to his broader metaphysical questions about agency and determinism.",
        "in_the_fiction": "Dick depicts bureaucratic control across his career. Flow My Tears, the Policeman Said (1974) presents a police state whose power operates through identity documentation and checkpoints. A Maze of Death (1970) features a theological bureaucracy that administers reality itself. 'Faith of Our Fathers' (1967) reveals the Party Leader as a mask for something inhuman. In Galactic Pot-Healer (1969), the protagonist's life is defined by meaningless bureaucratic work.",
        "in_the_exegesis": "Dick writes about the Black Iron Prison as the ultimate bureaucracy — a system that maintains itself through procedural reality-management without any single controlling agent. He frames the Roman Empire as an eternal bureaucratic structure that has never truly ended, merely changing its institutional forms while preserving its control functions.",
        "intellectual_background": "PKD's bureaucratic control draws on Kafka (The Trial, The Castle), Weber's theory of bureaucratic rationalization, Arendt's 'banality of evil,' and the Gnostic concept of the Archons as cosmic administrators. His personal experiences with government agencies and publishing-industry bureaucracies also inform the theme.",
        "scholarly_debate": "Jameson reads PKD's bureaucracies as allegories of late-capitalist administration. Freedman emphasizes the Kafkaesque dimension — bureaucracy as a structure of absurdity rather than mere oppression. Davis connects PKD's bureaucratic control to his Gnostic theology, where the Archons are cosmic bureaucrats.",
        "chronology_summary": "Bureaucratic control appears throughout PKD's career, from early stories about government agencies to the mature political novels of the 1970s and the Exegesis's BIP as bureaucratic cosmos.",
        "contradictions_summary": "PKD depicts bureaucracies as both mindlessly mechanical and as masks for something actively malevolent. He oscillates between a Weberian view (bureaucracy as impersonal rationalization) and a Gnostic view (bureaucracy as intentional cosmic evil).",
        "editorial_notes": "Cross-reference with Control Systems (the broader concept) and Surveillance (the monitoring function). Bureaucratic Control focuses specifically on institutional and procedural mechanisms of power.",
        "open_questions": [
            "Is PKD's bureaucratic control ultimately a political or a theological concept?",
            "How does PKD's treatment of bureaucracy compare with Kafka's — is it derivative, complementary, or distinctive?",
            "Does PKD's fiction offer any model of institutional organization that is not bureaucratically oppressive?"
        ]
    },
    "programming": {
        "definition": "Programming in PKD's work refers to the conditioning, scripting, or predetermined control of behavior — whether through technological implants, social conditioning, drug manipulation, or cosmic determinism — raising the question of whether genuine free will exists or whether all action is programmed response.",
        "pkd_relevance": "PKD treats programming as a threat to authentic selfhood that operates at every level from the neurological to the cosmic. His characters frequently discover that their choices, memories, and even personalities have been programmed by external agents. This theme connects his political fiction (state programming through propaganda) to his metaphysical speculation (the universe as a program running on divine hardware).",
        "in_the_fiction": "Dick depicts programming across multiple registers. In A Scanner Darkly (1977), Substance D progressively programs its users' neural pathways, overwriting personality. 'The Electric Ant' (1969) reveals that Garson Poole's entire experiential reality is generated by a micro-punched tape — his consciousness is literally a running program. Do Androids Dream (1968) features the Penfield mood organ, which programs emotional states on demand.",
        "in_the_exegesis": "Dick writes about determinism as cosmic programming. He theorizes that the Black Iron Prison programs human behavior and perception to maintain its control. But he also suggests that VALIS operates through programming — injecting salvific information into human minds. The Exegesis oscillates between viewing programming as enslavement and as divine instruction.",
        "intellectual_background": "PKD's programming theme engages with behaviorist psychology (Skinner), cybernetic theories of control, Calvinist predestination, and the free will versus determinism debate. His unique contribution is rendering the abstract philosophical problem as lived, felt experience — characters who discover they are programmed and must decide whether resistance is itself part of the program.",
        "scholarly_debate": "Vest reads PKD's programming as Cold War allegory — brainwashing and ideological conditioning. Hayles connects it to the broader cybernetic dissolution of the autonomous subject. Davis treats the theme theologically, noting that PKD's divine programming (VALIS) poses the same free-will problem as his political programming.",
        "chronology_summary": "Programming themes appear throughout PKD's career but take on new urgency after 2-3-74, when PKD questioned whether his own behavior was being guided by an external intelligence.",
        "contradictions_summary": "PKD condemns human programming as a violation of autonomy while also theorizing that divine programming (VALIS guiding human behavior) may be redemptive. He never fully resolves whether there is a meaningful difference between being programmed by a malevolent system and being programmed by a benevolent one.",
        "editorial_notes": "This topic straddles the AI and Psychology studies. Distinguish from Control Systems (the structures that program) and Automation (the technological displacement of human agency). Programming focuses on the internal experience of being directed by external code.",
        "open_questions": [
            "Does PKD maintain a meaningful distinction between malevolent and benevolent programming, or does all external control ultimately compromise autonomy?",
            "How does the programming theme relate to PKD's own reported experience of being 'taken over' by the Thomas personality?",
            "What is the relationship between PKD's programming theme and contemporary concerns about algorithmic influence and behavioral nudging?"
        ]
    }
}

# ── PSYCHOLOGY STUDY DOSSIERS ──────────────────────────────────────────────

PSY_DOSSIERS = {
    "schizophrenia": {
        "definition": "Schizophrenia in PKD's work functions as a literary and philosophical theme — a condition of fractured reality-perception and fragmented selfhood that PKD explores through characters, narrative structures, and the Exegesis's self-analysis, without reducing to clinical diagnosis.",
        "pkd_relevance": "PKD returned to schizophrenia throughout his career as a mode of perception that reveals truths invisible to consensus reality. His schizophrenic characters are not simply ill — they are epistemologically privileged, seeing through the false surfaces of the ordinary world. This treatment reflects PKD's engagement with R.D. Laing's anti-psychiatry and his own ambivalent relationship with psychiatric categories.",
        "in_the_fiction": "Dick depicts schizophrenia most extensively in Martian Time-Slip (1964), where Manfred Steiner's condition grants him non-linear temporal perception. Clans of the Alphane Moon (1964) presents an entire society organized around psychiatric diagnostic categories. A Scanner Darkly (1977) portrays cognitive disintegration through substance use, with Bob Arctor's scramble-suit literalizing the split self.",
        "in_the_exegesis": "Dick writes about the possibility that his 2-3-74 experiences might constitute schizophrenic symptoms, but he consistently tests this hypothesis against alternatives (divine revelation, temporal displacement, split-brain phenomena). The Exegesis functions partly as a rigorous self-examination of whether PKD's experiences are pathological or veridical.",
        "intellectual_background": "PKD's treatment of schizophrenia is deeply influenced by R.D. Laing's The Divided Self (1960) and The Politics of Experience (1967), which reframe schizophrenia as a potentially valid response to an insane society. He also drew on Jung's concept of psychic inflation and the Romantic tradition of madness as prophetic vision.",
        "scholarly_debate": "Sutin and Rickman treat PKD's schizophrenia theme biographically, connecting it to his personal psychological struggles. Mackey reads it philosophically, as PKD's way of dramatizing epistemic uncertainty. Palmer argues that PKD's anti-psychiatric stance anticipates contemporary neurodiversity movements.",
        "chronology_summary": "Schizophrenia themes appear early (Martian Time-Slip, 1964) and persist throughout PKD's career, intensifying in the Exegesis where the theme becomes autobiographical self-inquiry.",
        "contradictions_summary": "PKD simultaneously valorizes schizophrenic perception as a form of truth-seeing and acknowledges the genuine suffering it causes. He treats the same experiences as potentially prophetic revelation or potentially pathological breakdown without ever settling the question.",
        "editorial_notes": "This topic requires extreme care regarding the boundary between theme analysis and clinical attribution. Present PKD's depictions and self-reports without diagnosing him. Cross-reference with Psychosis, Identity Diffusion, and the anti-psychiatry dimension of Therapy/Psychiatry.",
        "open_questions": [
            "How does PKD's literary treatment of schizophrenia compare with clinical understandings of the condition in his era versus today?",
            "Does PKD's Laingian framework ultimately romanticize schizophrenia or offer a genuinely alternative epistemology?",
            "How should scholars handle the relationship between PKD's fictional schizophrenia and his own reported psychological experiences?"
        ]
    },
    "empathy": {
        "definition": "Empathy in PKD's work is the capacity to share and respond to another being's suffering — elevated to the defining criterion of authentic humanity, the basis of religious experience (Mercerism), and the test that separates humans from androids.",
        "pkd_relevance": "Empathy occupies a unique position in PKD's moral universe: it is the one quality he consistently treats as irreducible and essential to personhood. The Voigt-Kampff test, Mercerism, and the entire android question all revolve around empathy as the ultimate human attribute. Yet PKD also shows empathy failing, being faked, and being manipulated — creating a profound ambivalence at the heart of his ethics.",
        "in_the_fiction": "Dick depicts empathy as the central moral category in Do Androids Dream of Electric Sheep? (1968), where the Voigt-Kampff empathy test determines who lives and who is 'retired.' Mercerism — the religion of shared suffering accessed through empathy boxes — provides the novel's spiritual architecture. In 'The Little Black Box' (1964), empathy becomes a politically dangerous force that threatens state power.",
        "in_the_exegesis": "Dick writes about empathy in theological terms, connecting it to the Christian concepts of agape and caritas. He theorizes that VALIS communicates through empathic bonds and that the capacity for compassion is the divine spark within humans. The Exegesis treats empathy as both a psychological faculty and a metaphysical principle connecting all living things.",
        "intellectual_background": "PKD's empathy concept draws on Scheler's phenomenology of sympathy, Buber's I-Thou relation, Christian agape theology, and the Buddhist concept of karuna (compassion). His elevation of empathy over intelligence as the mark of personhood anticipates contemporary ethics of care and animal rights philosophy.",
        "scholarly_debate": "Galvan argues that PKD's empathy criterion constitutes a genuine philosophical contribution to the debate about artificial consciousness. Vint reads Mercerism as a critique of mediated affect in consumer society. Sims notes that PKD's empathy test is problematic because it relies on species-specific emotional responses, potentially excluding neurodivergent humans.",
        "chronology_summary": "Empathy becomes PKD's central moral concept in the mid-1960s, reaching full articulation in Do Androids Dream (1968) and remaining a touchstone throughout the Exegesis.",
        "contradictions_summary": "PKD makes empathy the criterion of humanity while showing it can be simulated (by androids), manufactured (through empathy boxes), and absent in actual humans. Mercer himself is revealed as a fraud, yet Mercerism continues to work — suggesting empathy may be authentic even when its object is fabricated.",
        "editorial_notes": "This topic bridges the AI and Psychology studies. The Voigt-Kampff test connects to Reality Testing (AI study); the theological dimension connects to Jung and Archetype (Psychology study). Empathy is perhaps PKD's single most important concept.",
        "open_questions": [
            "Is PKD's empathy criterion ultimately defensible as a marker of personhood, or does his own fiction undermine it?",
            "How does the revelation that Mercer is a fraud affect the philosophical status of empathy in Do Androids Dream?",
            "What is the relationship between PKD's empathy concept and contemporary debates about AI emotional intelligence?"
        ]
    },
    "identity-diffusion": {
        "definition": "Identity diffusion in PKD's work describes the experience of a self that is unstable, fragmented, or dissolving — characters who cannot maintain a coherent sense of who they are, whether due to drugs, technology, institutional manipulation, or ontological uncertainty.",
        "pkd_relevance": "Identity diffusion may be PKD's most autobiographically resonant theme. His fiction is filled with characters whose identities split, merge, dissolve, or are revealed as fabrications. After 2-3-74, when PKD experienced what he described as an alternate personality ('Thomas') sharing his body, the fictional theme became a lived question. The Exegesis can be read as an extended attempt to stabilize a diffusing identity.",
        "in_the_fiction": "Dick depicts identity diffusion most powerfully in A Scanner Darkly (1977), where Bob Arctor's identity literally splits into agent and suspect under the scramble suit. In Flow My Tears, the Policeman Said (1974), Jason Taverner's identity is erased from all records, leaving him existentially unmoored. 'Imposter' (1953) presents the ultimate identity crisis: Spence Olham cannot determine whether he is himself or an alien replica.",
        "in_the_exegesis": "Dick writes about his own identity diffusion with remarkable honesty. The emergence of 'Thomas' — a first-century Christian personality — during 2-3-74 created a duality that PKD explores at length. He oscillates between interpreting this as genuine possession, past-life memory, split personality, or divine communion.",
        "intellectual_background": "PKD's identity diffusion engages with Erikson's developmental concept of identity diffusion, Laing's divided self, existentialist philosophy of authentic selfhood (Heidegger, Sartre), and the Buddhist concept of anatta (no-self). His treatment is distinctively literary — identity diffusion is experienced from the inside.",
        "scholarly_debate": "Sutin reads PKD's identity diffusion biographically, connecting it to the death of his twin sister Jane and his unstable early family life. Palmer treats it as a philosophical stance — PKD's refusal of the unified subject. Mackey argues that identity diffusion in PKD is epistemological rather than psychological: his characters' selves dissolve because their reality dissolves.",
        "chronology_summary": "Identity diffusion themes appear throughout PKD's career but intensify in the 1970s, peaking with A Scanner Darkly (1977) and the Exegesis's Thomas/Phil duality.",
        "contradictions_summary": "PKD treats identity diffusion as both a terrifying loss (Bob Arctor's disintegration) and a potential liberation (the Thomas personality as access to deeper truth). He never resolves whether a stable self is desirable or whether dissolution opens the door to higher consciousness.",
        "editorial_notes": "Cross-reference with Double/Doppelganger (the structural pattern), Fabricated Identity (the manufactured self), and Schizophrenia (the clinical analogue). Present PKD's self-reports as self-reports, not clinical evidence.",
        "open_questions": [
            "Is identity diffusion in PKD's work primarily a psychological, ontological, or political condition?",
            "How does the Thomas/Phil duality in the Exegesis relate to the Bob/Fred split in A Scanner Darkly?",
            "Does PKD's fiction offer any model of healthy multiplicity, or is all identity diffusion ultimately pathological?"
        ]
    },
    "double-doppelganger": {
        "definition": "The double or doppelganger in PKD's work is the recurring structural motif of paired, mirrored, or split selves — characters who encounter alternate versions of themselves, who are secretly twinned with another, or who discover they are copies of an original.",
        "pkd_relevance": "The double is one of PKD's most persistent structural devices, rooted in the biographical fact of his twin sister Jane's death six weeks after their birth. This originary loss — the absent twin — reverberates through his fiction as a compulsion to pair, mirror, and split characters. The Exegesis extends the pattern: PKD theorized that 'Thomas' was his own double, a twin self from another time.",
        "in_the_fiction": "Dick depicts doubling across his career. VALIS (1981) presents Phil Dick and Horselover Fat as explicitly twinned selves narrating the same story from different perspectives. Flow My Tears, the Policeman Said (1974) involves the twinning of Jason Taverner and his identity-erased counterpart. Dr. Bloodmoney (1965) features Hoppy Harrington and Bill Keller, conjoined twins. A Scanner Darkly (1977) splits Bob Arctor into agent and target.",
        "in_the_exegesis": "Dick writes about the Thomas personality as a literal double — a first-century self sharing his body. He also theorizes cosmic doubling: the Palm Tree Garden is the double of the Black Iron Prison, the real world beneath the counterfeit one. The concept of 'astral determinism' extends doubling to the structure of reality itself.",
        "intellectual_background": "PKD's double draws on the Romantic Doppelganger tradition (Hoffmann, Poe, Dostoevsky), Freud's concept of the uncanny, Jung's shadow archetype, and Otto Rank's study The Double (1914). The biographical dimension — Jane's death — gives this literary tradition a uniquely personal inflection.",
        "scholarly_debate": "Sutin and Rickman emphasize the biographical origin in Jane's death. Palmer reads the double through psychoanalytic theory as a figure of the repressed. Mackey argues that PKD's doubles are epistemological rather than psychological — they represent the instability of identity in an unstable world.",
        "chronology_summary": "Doubling appears throughout PKD's career, from early stories through the mature novels. It reaches its most explicit and self-conscious expression in VALIS (1981), where PKD names his double and analyzes the relationship directly.",
        "contradictions_summary": "PKD treats doubling as both a pathological condition (the split self as illness) and as a necessary structure of reality (the true world doubled by the false one). The double is simultaneously a symptom and a cosmic principle.",
        "editorial_notes": "Cross-reference with Twin Motif (the biographical dimension), Identity Diffusion (the psychological experience), and Fabricated Identity (the AI study topic). The double is a structural device that manifests across multiple thematic registers.",
        "open_questions": [
            "How much of PKD's doubling motif is attributable to the biographical fact of Jane's death, and how much is independently philosophical?",
            "Does PKD's use of the double conform to or subvert the Romantic/Freudian tradition?",
            "How does the Phil/Fat doubling in VALIS function differently from the earlier fictional doubles?"
        ]
    },
    "jung": {
        "definition": "Jung in PKD's work refers to the pervasive influence of Carl Gustav Jung's analytical psychology — archetypes, the collective unconscious, individuation, synchronicity, and the I Ching — which provides one of PKD's most sustained intellectual frameworks for interpreting both his fiction and his mystical experiences.",
        "pkd_relevance": "Jung is arguably the single most important intellectual influence on PKD's mature work. The I Ching (a Jungian tool) structures The Man in the High Castle. Jungian archetypes populate the Exegesis. PKD's interpretation of 2-3-74 frequently relies on Jungian concepts: the anima, psychic inflation, enantiodromia, the collective unconscious as a source of transpersonal knowledge.",
        "in_the_fiction": "Dick depicts Jungian frameworks explicitly in The Man in the High Castle (1962), where the I Ching functions as an oracle connecting characters to the collective unconscious. VALIS (1981) is saturated with Jungian imagery: Sophia as anima figure, the quest for individuation, the black iron prison as shadow. The Three Stigmata of Palmer Eldritch (1965) can be read as a dark individuation narrative.",
        "in_the_exegesis": "Dick writes about Jung extensively, using Jungian categories to interpret his 2-3-74 experiences. He considers whether VALIS might be an expression of the collective unconscious, whether Thomas is his shadow or animus, and whether his experiences represent individuation or inflation. He also critiques Jung, sometimes finding the framework insufficient for the scale of his experiences.",
        "intellectual_background": "PKD engaged directly with Jung's major works, including Aion, Mysterium Coniunctionis, and the I Ching commentary. He also absorbed Jung through secondary sources and the broader countercultural Jungian revival of the 1960s-70s. His Jungian engagement is distinctive for its combination of sincere commitment and critical distance.",
        "scholarly_debate": "Kripal reads PKD as a Jungian visionary whose experiences exemplify active imagination at cosmic scale. Davis argues that PKD's Jungianism is syncretic — he combines Jung with Gnostic, Platonic, and Christian frameworks that Jung himself kept separate. Fitting warns against over-reading Jung into PKD, noting that PKD used multiple psychological frameworks selectively.",
        "chronology_summary": "Jungian influence appears from The Man in the High Castle (1962) onward and intensifies dramatically in the Exegesis, where Jung becomes one of PKD's primary interpretive tools for the 2-3-74 experiences.",
        "contradictions_summary": "PKD both relies on and resists Jungian categories. He uses Jung's framework extensively but periodically declares it insufficient, complaining that Jung psychologizes what is genuinely transcendent. He cannot decide whether his experiences are Jungian (arising from the collective unconscious) or genuinely theological (arriving from outside the psyche entirely).",
        "editorial_notes": "Cross-reference with Archetype, Synchronicity, and Anamnesis. Researchers should distinguish between PKD's direct engagement with Jung's texts and his absorption of Jungian ideas through popular culture and secondary sources.",
        "open_questions": [
            "How accurately does PKD represent Jung's ideas, and where does he creatively misread or extend them?",
            "Is PKD's Jungianism ultimately psychological (the unconscious as source) or theological (God speaking through Jungian categories)?",
            "How does PKD's relationship with Jung compare with his relationships with other intellectual influences (Plato, Gnostics, Whitehead)?"
        ]
    },
    "addiction": {
        "definition": "Addiction in PKD's work encompasses both the pharmacological dependence depicted in his fiction and the broader theme of compulsive attachment to substances, experiences, or realities that simultaneously sustain and destroy the user.",
        "pkd_relevance": "Addiction is one of PKD's most autobiographically grounded themes, drawn from his own amphetamine use and the drug culture of 1960s-70s California. But PKD elevates addiction beyond the personal: in his hands, it becomes a model for humanity's relationship to false reality itself. The inhabitants of PKD's fictional worlds are addicted to their own perceptions, unable to relinquish comforting illusions even when shown the truth.",
        "in_the_fiction": "Dick depicts addiction most devastatingly in A Scanner Darkly (1977), dedicated to friends lost to drug use, where Substance D destroys Bob Arctor's cognitive integrity. The Three Stigmata of Palmer Eldritch (1965) presents two competing addictive substances — Can-D (escapist) and Chew-Z (transformative/trapped) — as competing models of reality. Now Wait for Last Year (1966) features a drug that causes temporal displacement and irreversible dependence.",
        "in_the_exegesis": "Dick writes about addiction only occasionally in the Exegesis, but the concept haunts his analysis of the BIP. He frames false reality as addictive — humans are habituated to the dokos and resist awakening. The metaphor of addiction structures his understanding of why liberation is so difficult even when truth is available.",
        "intellectual_background": "PKD's addiction writing draws on direct personal experience, the countercultural drug discourse of the 1960s-70s, and De Quincey's literary tradition of drug memoir. His unique contribution is the theological dimension: addiction as a model of the human condition under the BIP, not merely a social or medical problem.",
        "scholarly_debate": "Sutin and Rickman document PKD's personal substance use history as biographical context. Palmer reads the addiction theme as PKD's most socially realist material — a departure from his metaphysical concerns. Davis argues that addiction in PKD is always already metaphysical: Substance D is a figure for any system that replaces authentic experience with simulacra.",
        "chronology_summary": "Addiction themes appear from the mid-1960s onward, intensifying through the 'speed years' and reaching their definitive expression in A Scanner Darkly (1977). The theme becomes more metaphorical in the Exegesis.",
        "contradictions_summary": "PKD depicts drugs as both tools of enslavement (Substance D) and potential vehicles of liberation (the temporally displacing drug in Now Wait for Last Year). He simultaneously condemns drug culture and mourns its casualties from the inside.",
        "editorial_notes": "Handle with care: present PKD's depictions and self-reports without moralizing or clinicalizing. Cross-reference with Amphetamine Use (the specific substance) and False Reality (addiction as epistemic metaphor). A Scanner Darkly's dedication to lost friends provides essential context.",
        "open_questions": [
            "How does the addiction theme in PKD's fiction relate to his Gnostic theology of entrapment in false reality?",
            "Is A Scanner Darkly best read as realist drug fiction or as metaphysical allegory — and does PKD intend the distinction to collapse?",
            "How does PKD's treatment of addiction compare with other major drug-literature authors (Burroughs, De Quincey, Thompson)?"
        ]
    },
    "amphetamine-use": {
        "definition": "Amphetamine use in PKD's work refers to the presence of stimulant drugs as both a biographical reality shaping PKD's creative output and a thematic element in his fiction — explored here as a motif and context rather than a clinical evaluation.",
        "pkd_relevance": "PKD's prolific output during the 1960s coincided with his heavy amphetamine use, and the relationship between stimulants and his creative vision has been debated since his death. His fiction frequently features characters whose perceptions are altered by stimulant-like substances, and the Exegesis occasionally reflects on the relationship between his drug history and his later visionary experiences.",
        "in_the_fiction": "Dick depicts amphetamine-like substances and their effects across several works. A Scanner Darkly (1977) is the most direct treatment, with Substance D functioning as a stand-in for the destructive potential of stimulant culture. The manic energy and paranoid ideation of characters in works from the mid-1960s (The Three Stigmata, Now Wait for Last Year) have been read as reflecting amphetamine phenomenology.",
        "in_the_exegesis": "Dick writes occasionally about whether his 2-3-74 experiences might be connected to his prior drug use, but generally rejects this explanation as insufficient. He notes that the visions occurred years after he had stopped heavy amphetamine use. The Exegesis treats the drug history as a biographical fact to be accounted for rather than an explanation that closes inquiry.",
        "intellectual_background": "PKD's amphetamine experience sits within the broader context of mid-century literary stimulant use (the Beats, Kerouac's benzedrine-fueled On the Road). It also connects to the history of pharmaceutical amphetamine prescription and the California drug culture of the 1960s-70s.",
        "scholarly_debate": "Sutin documents PKD's drug history in detail while cautioning against reducing his work to drug effects. Lethem argues that the 'speed writing' narrative is overblown and diminishes PKD's literary achievement. Rickman provides the most detailed biographical account of the drug years. Davis insists that whether or not drugs contributed to PKD's visions, the philosophical content of those visions must be evaluated on its own terms.",
        "chronology_summary": "Amphetamine use was concentrated in the period roughly 1963-1972, with PKD's heaviest use during the late 1960s. By the time of 2-3-74, he had largely moved past stimulant use, making direct pharmacological causation of the visions unlikely.",
        "contradictions_summary": "PKD acknowledges his drug history while insisting it does not explain his later experiences. Scholars are divided: some treat the drug years as essential context for understanding the Exegesis, while others argue this constitutes a genetic fallacy.",
        "editorial_notes": "This is a sensitive biographical topic. Present the documented facts and PKD's own statements without pathologizing. Avoid the reductive narrative that PKD's visionary experiences were 'just' drug effects. Cross-reference with Addiction (the broader theme) and Psychosis (the diagnostic question).",
        "open_questions": [
            "To what extent did amphetamine use shape the distinctive features of PKD's literary style and philosophical vision?",
            "How should scholars weigh the relationship between PKD's drug history and the 2-3-74 experiences?",
            "Does the 'speed writer' narrative unfairly diminish PKD's literary achievement?"
        ]
    },
    "false-memory": {
        "definition": "False memory in PKD's work refers to the broader epistemological condition of possessing memories that do not correspond to actual past events — whether through technological implantation, psychological distortion, cosmic deception, or the inherent unreliability of human recollection.",
        "pkd_relevance": "False memory is central to PKD's philosophical project because it undermines the primary basis for personal identity: if we are our memories, and our memories are false, then we do not know who we are. PKD explores this from multiple angles — technological manipulation in the fiction, cosmic deception in the Exegesis, and the epistemological problem of ever knowing whether any memory is genuine.",
        "in_the_fiction": "Dick depicts false memory extensively. 'We Can Remember It for You Wholesale' (1966) layers false memories over genuine ones until the distinction collapses. In Do Androids Dream (1968), Rachael's false memories are convincing enough to fool even their possessor. Ubik (1969) presents memory itself as unstable in half-life, decaying alongside the material world. A Scanner Darkly (1977) shows drug-induced memory deterioration.",
        "in_the_exegesis": "Dick writes about anamnesis — the recovery of true memory — as the antidote to false memory. The Exegesis posits that the Black Iron Prison maintains control partly through implanting false memories of a normal world over the true memory of imprisonment. PKD's 2-3-74 experience included what he interpreted as genuine ancient memories breaking through the false ones.",
        "intellectual_background": "PKD's false memory theme draws on Plato's anamnesis, Descartes's deceiving demon, and the emerging science of memory malleability. His work anticipates Elizabeth Loftus's research on false memory syndrome and contemporary concerns about deepfakes and AI-generated evidence.",
        "scholarly_debate": "Rossi reads PKD's false memory as reflecting anxiety about his own biographical reliability. Sims connects it to postmodern theories of constructed identity. Barlow argues that false memory in PKD is always political — a metaphor for manufactured consent and propaganda.",
        "chronology_summary": "False memory themes appear from the mid-1960s onward and become philosophically central in the Exegesis, where the anamnesis/false-memory dialectic structures PKD's interpretation of 2-3-74.",
        "contradictions_summary": "PKD treats the recovery of true memory (anamnesis) as salvation while also suggesting that the distinction between true and false memory may be impossible to establish. The Exegesis's 'true memories' of first-century Rome could themselves be false, a possibility PKD acknowledges without resolving.",
        "editorial_notes": "Distinguish from Implanted Memory (AI study), which focuses on the technological mechanism. False Memory addresses the broader epistemological problem. Cross-reference with Memory and Anamnesis.",
        "open_questions": [
            "Does PKD's work ultimately suggest that true memory is recoverable, or that all memory is constructed?",
            "How does the anamnesis concept in the Exegesis relate to the false memory theme in the fiction?",
            "What is the political dimension of false memory in PKD — who benefits from widespread false recollection?"
        ]
    },
    "memory": {
        "definition": "Memory in PKD's work is the fundamental epistemic faculty through which identity, history, and reality are constituted — and therefore the primary site of vulnerability, since manipulated or degraded memory means a manipulated or degraded self.",
        "pkd_relevance": "Memory occupies a pivotal position in PKD's philosophical architecture. It is the bridge between his epistemological concerns (how do we know what is real?) and his ontological ones (what is the self?). PKD treats memory not as a passive recording but as an active, vulnerable, and potentially transformative process — one that connects the individual to cosmic history through anamnesis.",
        "in_the_fiction": "Dick depicts memory as constitutive of identity across his oeuvre. In Ubik (1969), memories decay in half-life alongside material reality. 'We Can Remember It for You Wholesale' (1966) treats memory as a commodity to be purchased and implanted. VALIS (1981) presents anamnesis — the recovery of genuine memory — as a salvific event. Do Androids Dream (1968) uses implanted memories to challenge the relationship between memory and authenticity.",
        "in_the_exegesis": "Dick writes about memory as potentially the most important human faculty. He theorizes anamnesis — Platonic recollection of divine truth — as the mechanism through which VALIS communicates. The Exegesis's central narrative arc involves PKD recovering memories he interprets as belonging to a first-century Christian, suggesting that memory can transcend individual lifetimes.",
        "intellectual_background": "PKD's memory concept draws on Plato's anamnesis (knowledge as recollection), Bergson's distinction between habit-memory and pure memory, Augustine's memory-palaces, and Proust's involuntary memory. His unique contribution is treating memory as simultaneously psychological, theological, and political.",
        "scholarly_debate": "Rossi argues that memory in PKD is the key to his entire philosophical project. Sims connects PKD's memory themes to postmodern theories of the constructed past. Kripal treats PKD's anamnesis claims as data for the study of extraordinary memory phenomena.",
        "chronology_summary": "Memory themes appear throughout PKD's career but reach their philosophical zenith in the post-2-3-74 works, where anamnesis becomes PKD's primary interpretive framework for his mystical experiences.",
        "contradictions_summary": "PKD treats memory as both the most reliable route to truth (anamnesis as divine revelation) and the most vulnerable faculty (easily implanted, erased, or distorted). He cannot resolve whether memory connects us to reality or traps us in illusion.",
        "editorial_notes": "This is the broadest memory-related topic. Cross-reference with False Memory (the negative case), Anamnesis (the positive case), and Implanted Memory (the technological mechanism). Memory sits at the intersection of multiple study themes.",
        "open_questions": [
            "Does PKD maintain a consistent theory of memory across his fiction and the Exegesis, or does his understanding evolve?",
            "How does PKD's treatment of memory compare with contemporary neuroscience's understanding of memory as reconstructive rather than reproductive?",
            "What is the relationship between personal memory and collective/cosmic memory in PKD's work?"
        ]
    },
    "trauma": {
        "definition": "Trauma in PKD's work refers to catastrophic experiences — personal, historical, and cosmic — whose aftereffects persist in shattered psyches, broken narratives, and worlds that bear the marks of irreversible damage.",
        "pkd_relevance": "PKD's life and work are saturated with trauma: the death of his twin sister Jane, multiple failed marriages, the November 1971 break-in, the Vancouver suicide attempt, and the shattering 2-3-74 experience. His fiction characteristically begins after the catastrophe — in worlds already broken, among people already damaged — making trauma a structural principle rather than merely a plot event.",
        "in_the_fiction": "Dick depicts post-traumatic landscapes across his career. Dr. Bloodmoney (1965) is set after nuclear war. A Scanner Darkly (1977) is written in the aftermath of the drug culture's collapse and is dedicated to friends who were casualties. Do Androids Dream (1968) takes place in a post-nuclear wasteland where empathy itself is a response to collective trauma. VALIS (1981) opens with Gloria's suicide, a traumatic event that structures the entire novel.",
        "in_the_exegesis": "Dick writes about trauma in connection with 2-3-74, which he describes in terms that oscillate between traumatic rupture and salvific breakthrough. He also processes the November 1971 break-in as a traumatic event whose meaning he cannot fix — was it government agents, drug dealers, or his own paranoid fabrication? The Exegesis itself can be read as a prolonged attempt to integrate traumatic experience.",
        "intellectual_background": "PKD's trauma writing anticipates the formalization of PTSD (1980) and engages with existentialist accounts of limit-experiences (Jaspers's Grenzsituation). His treatment of trauma as revelatory — breaking through ordinary consciousness to expose deeper reality — connects to the Romantic tradition of the wound as a source of vision.",
        "scholarly_debate": "Rickman provides detailed biographical documentation of PKD's traumatic experiences. Sutin reads the fiction as a sustained response to early loss (Jane's death). Davis argues that trauma in PKD is always potentially revelatory — the shattering of ordinary consciousness may open access to the divine. Palmer warns against reducing PKD's metaphysics to trauma response.",
        "chronology_summary": "Trauma pervades PKD's entire career but becomes explicitly thematized in the 1970s, particularly in A Scanner Darkly (1977) and the Exegesis's processing of the break-in and 2-3-74.",
        "contradictions_summary": "PKD treats trauma as both destructive and revelatory — the same event (2-3-74) may be a psychotic break or a mystical awakening. He holds both possibilities without resolution, making trauma simultaneously the worst thing that can happen and a potential gateway to truth.",
        "editorial_notes": "Present biographical traumas as documented facts and PKD's self-reports as self-reports. Avoid therapeutic interpretation. Cross-reference with Psychosis, Addiction, and the biographical dimensions of the Twin Motif.",
        "open_questions": [
            "How does the death of PKD's twin sister Jane function as an 'originary trauma' shaping his fiction?",
            "Is PKD's treatment of trauma as revelatory philosophically defensible or does it risk romanticizing suffering?",
            "How should scholars balance biographical trauma with literary analysis when interpreting PKD's work?"
        ]
    },
    "hypnagogic-state": {
        "definition": "The hypnagogic state in PKD's work refers to the threshold consciousness between waking and sleep — a liminal zone characterized by vivid imagery, loosened rational control, and potential access to non-ordinary perception that PKD treated as epistemologically significant.",
        "pkd_relevance": "PKD was deeply attentive to hypnagogic phenomena, both as a feature of his characters' experiences and as a dimension of his own cognitive life. He treated the hypnagogic state not as mere neural noise but as a potential channel for genuine information — a crack in the wall of ordinary perception through which deeper reality might be glimpsed.",
        "in_the_fiction": "Dick depicts hypnagogic consciousness in Ubik (1969), where half-life represents a permanent hypnagogic condition — consciousness suspended between life and death, generating vivid but unstable realities. The Three Stigmata of Palmer Eldritch (1965) presents drug-induced states with hypnagogic qualities. VALIS (1981) describes visionary experiences with the phenomenological texture of hypnagogia.",
        "in_the_exegesis": "Dick writes about his own hypnagogic experiences as a potential vehicle for the 2-3-74 transmissions. He describes phosphene patterns, visual imagery of ancient Rome, and cascading symbolic content that arrived during the waking-sleep transition. He theorizes that the hypnagogic state may temporarily disable the BIP's perceptual filters.",
        "intellectual_background": "PKD's interest in hypnagogia connects to a long tradition of creative attention to liminal states (Kekulé's benzene ring dream, Coleridge's 'Kubla Khan'). It also engages with Mavromatis's research on hypnagogia and the broader parapsychological interest in threshold states as psi-conducive.",
        "scholarly_debate": "Kripal treats PKD's hypnagogic reports as data for the study of extraordinary experiences. Davis connects them to the broader tradition of visionary consciousness in religious and artistic contexts. Sutin documents the hypnagogic experiences biographically without adjudicating their ontological status.",
        "chronology_summary": "Hypnagogic themes become prominent in the Exegesis after 2-3-74, when PKD began systematically recording and analyzing his liminal-state experiences.",
        "contradictions_summary": "PKD alternates between treating hypnagogic content as genuine perception (information from VALIS) and as neurological artifact (phosphenes, random firing). He recognizes the ambiguity without resolving it.",
        "editorial_notes": "Distinguish from Hypnopompic State (sleep-to-waking transition). Present PKD's reports as phenomenological descriptions without adjudicating their ontological status. Cross-reference with Psychosis and Dream Rituals of Asclepius.",
        "open_questions": [
            "How does PKD's phenomenological description of hypnagogia compare with contemporary neuroscientific understanding?",
            "Did PKD develop a systematic method for using hypnagogic states as an epistemic tool?",
            "What is the relationship between PKD's hypnagogic experiences and the visual/symbolic content of his fiction?"
        ]
    },
    "hypnopompic-state": {
        "definition": "The hypnopompic state in PKD's work refers to the transition from sleep to waking — a liminal zone where dream content persists into waking consciousness, potentially carrying information or imagery from non-ordinary perception.",
        "pkd_relevance": "While less frequently discussed than the hypnagogic state, the hypnopompic transition was significant for PKD's phenomenology of 2-3-74. Several of his most striking visionary experiences occurred upon waking, when dream imagery persisted with unusual vividness and coherence into ordinary consciousness. PKD treated these experiences as evidentially significant.",
        "in_the_fiction": "Dick depicts hypnopompic phenomena less explicitly than hypnagogia, but the experience of waking into an altered or uncertain reality pervades his fiction. Characters in Ubik (1969) wake into progressively degraded realities. In A Maze of Death (1970), each chapter's reality is revealed upon 'waking' to be a construct. The transition from one reality level to another in PKD's fiction often has the phenomenological texture of waking from a dream.",
        "in_the_exegesis": "Dick writes about waking visions — experiences where dream content persisted into full consciousness with vivid clarity. He describes waking to see ancient Rome overlaid on his Orange County surroundings, and waking with knowledge (particularly the medical knowledge about his son's hernia) that he interprets as transmitted during sleep. These hypnopompic experiences are among his strongest evidence for the reality of 2-3-74.",
        "intellectual_background": "PKD's hypnopompic experiences connect to the ancient practice of incubation dreaming (see Dream Rituals of Asclepius), the Romantic tradition of prophetic dreams, and emerging sleep science research on the persistence of dream mentation into waking states.",
        "scholarly_debate": "Kripal reads PKD's hypnopompic reports as examples of what religious studies calls 'waking dreams' — experiences that challenge the standard dream/waking binary. Davis connects them to the broader phenomenology of religious vision. Neuropsychological readings might classify them as sleep paralysis phenomena.",
        "chronology_summary": "Hypnopompic experiences become significant primarily in the Exegesis's account of 2-3-74 and its aftermath.",
        "contradictions_summary": "PKD treats hypnopompic content as both potentially veridical (carrying genuine information from VALIS) and potentially hallucinatory. He acknowledges that the sleep-wake transition is a known site of perceptual distortion while insisting that some of his waking visions contained verifiable information.",
        "editorial_notes": "Distinguish from Hypnagogic State (waking-to-sleep). The two are closely related but phenomenologically distinct. Present PKD's reports without adjudicating their ontological status.",
        "open_questions": [
            "How do PKD's hypnopompic reports compare with documented cases of hypnopompic hallucination in sleep research?",
            "Does PKD distinguish between ordinary waking dreams and the 2-3-74 hypnopompic experiences in terms of phenomenological quality?",
            "What is the evidential status of the medical knowledge PKD reports receiving during hypnopompic states?"
        ]
    },
    "psychosis": {
        "definition": "Psychosis in PKD's work refers to the condition of losing contact with consensus reality — explored as a literary theme, a philosophical possibility, and a deeply personal question that PKD confronted in assessing his own 2-3-74 experiences.",
        "pkd_relevance": "PKD's relationship to psychosis is perhaps the most delicate interpretive question in his scholarship. His fiction systematically blurs the boundary between psychotic delusion and genuine insight, while the Exegesis honestly confronts the possibility that his own visionary experiences might be psychotic. PKD treated the psychosis question not as a diagnosis to be accepted or rejected but as a philosophical problem to be investigated.",
        "in_the_fiction": "Dick depicts psychosis-adjacent states across his career. Martian Time-Slip (1964) portrays Manfred Steiner's autistic/psychotic perception as access to a true future. A Scanner Darkly (1977) depicts drug-induced cognitive disintegration that blurs the line between psychosis and undercover work. The Three Stigmata of Palmer Eldritch (1965) presents a state of cosmic possession that is indistinguishable from psychosis.",
        "in_the_exegesis": "Dick writes with remarkable intellectual honesty about whether his 2-3-74 experiences constitute psychosis. He lists evidence for and against, applies reality-testing criteria, and considers whether the apparently veridical information he received (his son's hernia diagnosis) could have been obtained through normal means. The Exegesis is partly a sustained argument with the psychosis hypothesis.",
        "intellectual_background": "PKD's approach to psychosis is shaped by Laing's anti-psychiatry (psychosis as a potentially valid perception), Jung's concept of psychic inflation, and the Romantic tradition of divine madness. He also engaged with conventional psychiatric categories while questioning their adequacy.",
        "scholarly_debate": "Sutin navigates the psychosis question with biographical care. Kripal argues that the psychosis hypothesis is reductive and that PKD's experiences should be studied on their own terms. Palmer notes that PKD's fiction consistently argues against the adequacy of psychiatric categories for capturing extraordinary experience. Davis treats the psychosis question as itself a Dickian theme — the undecidability is the point.",
        "chronology_summary": "Psychosis themes appear throughout PKD's fiction but become urgently personal after 2-3-74, when the question of his own mental status dominated the Exegesis.",
        "contradictions_summary": "PKD neither accepts nor rejects the psychosis explanation. He treats it as one hypothesis among many — alongside divine revelation, temporal displacement, and neurological event — and refuses to privilege any single explanation.",
        "editorial_notes": "This is the most sensitive topic in the Psychology study. Do not diagnose PKD. Present the psychosis question as PKD himself engaged with it: as an open, philosophically serious inquiry. Cross-reference with Schizophrenia, Reality Testing, and the editorial methodology across all studies.",
        "open_questions": [
            "Is PKD's refusal to resolve the psychosis question a philosophical strength or an evasion?",
            "How does contemporary psychiatry's understanding of psychosis relate to the categories PKD employs?",
            "Can the veridical elements of PKD's 2-3-74 experiences (the hernia diagnosis) definitively rule out psychotic origin?"
        ]
    },
    "archetype": {
        "definition": "Archetype in PKD's work refers to the Jungian concept of universal, primordial patterns within the collective unconscious — recurring symbolic figures and structures that PKD uses to interpret both his fiction and his visionary experiences.",
        "pkd_relevance": "PKD draws on Jungian archetypes as a primary vocabulary for understanding his characters, his mystical experiences, and the structure of reality itself. Sophia, the anima, the shadow, the wise old man, and the cosmic child all appear in his work. For PKD, archetypes are not merely psychological patterns but potentially real entities or forces operating through the collective unconscious.",
        "in_the_fiction": "Dick depicts archetypal figures throughout his fiction. The dark-haired girl (recurring across many novels) functions as an anima figure. Palmer Eldritch is a shadow/demiurge archetype. Sophia in VALIS (1981) embodies the divine feminine wisdom archetype. The recurring pattern of the 'little man' protagonist (ordinary person caught in extraordinary circumstances) is itself an archetypal structure.",
        "in_the_exegesis": "Dick writes about archetypes as living presences within his psyche. He interprets the Thomas personality as an archetypal irruption from the collective unconscious. He analyzes Sophia, VALIS, and the BIP in archetypal terms, sometimes treating them as Jungian psychological entities and sometimes as genuinely transcendent beings who merely appear in archetypal form.",
        "intellectual_background": "PKD's archetypal thinking derives primarily from Jung (especially Aion and the archetypes of the collective unconscious), but also engages with Platonic Forms, Gnostic Aeons, and the Kabbalistic Sephiroth. He treats these traditions as converging descriptions of the same underlying reality.",
        "scholarly_debate": "Kripal reads PKD's archetypes as genuine experiences of transpersonal forces. Davis argues that PKD's archetypal thinking is syncretic, combining Jung with incompatible traditions. Palmer warns against over-reading Jungian structure into PKD's fiction, noting that many apparent archetypes may be conventional genre figures.",
        "chronology_summary": "Archetypal thinking intensifies in PKD's late work, particularly the Exegesis and VALIS, though archetypal patterns are present from his earliest fiction.",
        "contradictions_summary": "PKD oscillates between treating archetypes as psychological patterns (Jung's view) and as ontologically real entities (a more Platonic/Gnostic position). He cannot decide whether the archetypes emerge from the human psyche or whether the human psyche is structured by genuinely external archetypal forces.",
        "editorial_notes": "Cross-reference with Jung (the broader intellectual framework), Synchronicity (the acausal connecting principle), and the various anima/shadow figures in the fiction. Distinguish PKD's sometimes-loose use of 'archetype' from Jung's precise technical definition.",
        "open_questions": [
            "Does PKD use 'archetype' in a consistent technical sense, or is it a flexible label for any recurring symbolic pattern?",
            "How does PKD's archetypal interpretation of 2-3-74 compare with Jung's own accounts of archetypal encounters?",
            "Are the archetypes in PKD's fiction genuinely Jungian, or are they genre conventions that PKD retrofits into a Jungian framework?"
        ]
    },
    "synchronicity": {
        "definition": "Synchronicity in PKD's work refers to Jung's concept of meaningful coincidence — acausal connections between inner psychic states and outer events that suggest an underlying order to reality beyond mechanical causation.",
        "pkd_relevance": "PKD experienced and theorized synchronicity as a central feature of both his life and his cosmic model. The I Ching — a synchronistic oracle — structures The Man in the High Castle. The Exegesis is filled with reports of meaningful coincidences that PKD interprets as evidence for an interconnected, purposive cosmos. For PKD, synchronicity was not merely a psychological curiosity but evidence for the existence of VALIS.",
        "in_the_fiction": "Dick depicts synchronicity explicitly in The Man in the High Castle (1962), where the I Ching functions as a synchronistic device connecting characters to an ordering principle beyond causality. In VALIS (1981), the convergence of seemingly unrelated events around the Savior figure exemplifies synchronistic patterning. Flow My Tears (1974) involves coincidences so improbable that they suggest non-causal ordering.",
        "in_the_exegesis": "Dick writes extensively about synchronistic experiences: books falling open to relevant passages, overheard conversations that answer unspoken questions, dreams that predict events. He theorizes that synchronicity is the mechanism through which VALIS communicates — not through causal intervention but through the arrangement of meaningful patterns across apparently independent events.",
        "intellectual_background": "PKD's synchronicity derives directly from Jung's Synchronicity: An Acausal Connecting Principle (1952) and its application through the I Ching. He also connects it to Leibniz's pre-established harmony, Pauli's collaboration with Jung on the physics-psyche relationship, and the Hermetic principle of correspondence.",
        "scholarly_debate": "Kripal treats PKD's synchronicity reports as genuine data for the study of extraordinary experience. Main connects PKD's synchronistic thinking to the broader Jungian-Paulian tradition. Davis reads synchronicity in PKD as a literary and structural principle, not just a reported experience — PKD's novels are synchronistically structured.",
        "chronology_summary": "Synchronicity appears from The Man in the High Castle (1962) onward and becomes a central concept in the Exegesis, where it provides PKD's primary explanatory framework for the meaningfulness of his experiences.",
        "contradictions_summary": "PKD simultaneously treats synchronicity as evidence for a purposive cosmos and acknowledges that pattern-recognition in random events is a known feature of paranoid ideation. He cannot always distinguish genuine synchronicity from apophenia.",
        "editorial_notes": "Cross-reference with Jung (the source framework) and Reality Testing (synchronicity as evidence for cosmic order). Researchers should note that PKD's synchronicity claims are experiential reports, not falsifiable propositions.",
        "open_questions": [
            "Can PKD's synchronicity reports be distinguished from apophenia, and does PKD himself recognize this problem?",
            "How does synchronicity function structurally in PKD's fiction — as a plot device, a thematic element, or both?",
            "What is the relationship between PKD's synchronistic experiences and his amphetamine use history?"
        ]
    },
    "split-brain": {
        "definition": "Split-brain in PKD's work refers to hemispheric lateralization theory — the idea that the left and right cerebral hemispheres process information differently — which PKD used extensively to theorize his 2-3-74 experiences as the 'awakening' of his right hemisphere.",
        "pkd_relevance": "Split-brain theory became one of PKD's most sustained explanatory frameworks for 2-3-74. He theorized that his right hemisphere had been dormant and was suddenly activated, producing the flood of symbolic, spatial, and holistic cognition he experienced as 'Thomas' and VALIS. This neurological hypothesis competed with theological and metaphysical ones throughout the Exegesis.",
        "in_the_fiction": "Dick depicts split consciousness in A Scanner Darkly (1977), where the scramble suit creates a literal hemispheric disconnect — Bob Arctor's brain cannot integrate its two processing streams. In VALIS (1981), the Phil/Fat split can be read as a fictional representation of hemispheric duality. The theme of characters who perceive two realities simultaneously reflects split-brain phenomenology.",
        "in_the_exegesis": "Dick writes extensively about Ornstein's The Psychology of Consciousness and Jaynes's The Origin of Consciousness in the Breakdown of the Bicameral Mind, applying both to his experiences. He theorizes that his right hemisphere accessed a mode of consciousness that the left hemisphere — verbal, analytical, reality-constructing — normally suppresses. The 'Thomas' personality represents right-hemispheric cognition expressed through a different cultural framework.",
        "intellectual_background": "PKD's split-brain thinking draws on Sperry's Nobel Prize-winning research, Ornstein's popular account, and especially Jaynes's bicameral mind hypothesis, which argues that ancient humans experienced right-hemisphere outputs as divine voices. This gave PKD a scientific framework for interpreting his experience of an inner voice as potentially both neurological and meaningful.",
        "scholarly_debate": "Davis argues that the split-brain hypothesis is one of PKD's most intellectually rigorous attempts to explain 2-3-74. Kripal notes that PKD uses the neuroscience selectively, adopting elements that support his thesis while ignoring limitations. Palmer warns that contemporary neuroscience has moved beyond the simplistic lateralization model PKD relied on.",
        "chronology_summary": "Split-brain theory becomes a major Exegesis framework in the late 1970s, after PKD encountered Ornstein and Jaynes. It represents his most naturalistic explanatory attempt for 2-3-74.",
        "contradictions_summary": "PKD simultaneously advocates the split-brain hypothesis and recognizes that it is reductive — explaining his experiences neurologically may strip them of their spiritual significance. He oscillates between wanting a scientific explanation and fearing that such an explanation would devalue the experience.",
        "editorial_notes": "Note that contemporary neuroscience considers the strict left/right hemisphere dichotomy an oversimplification. PKD's use of the framework should be understood in its 1970s context. Cross-reference with Psychosis and Jung for alternative explanatory frameworks.",
        "open_questions": [
            "Does PKD's split-brain hypothesis survive scrutiny from contemporary neuroscience, or is it historically interesting but scientifically outdated?",
            "How does Jaynes's bicameral mind theory specifically shape PKD's interpretation of the 'Thomas' personality?",
            "Can the split-brain and theological explanations for 2-3-74 be reconciled, or does PKD recognize them as fundamentally incompatible?"
        ]
    },
    "dream-rituals-of-asclepius": {
        "definition": "The Dream Rituals of Asclepius in PKD's work refer to the ancient Greek practice of temple incubation — sleeping in a sacred precinct to receive healing dreams from the god Asclepius — which PKD invoked as a model for understanding his own visionary dream experiences.",
        "pkd_relevance": "PKD's reference to Asclepian incubation reveals his desire to situate his experiences within a long historical tradition of therapeutic dreaming. By connecting his visions to an ancient and respected healing practice, PKD reframes what might be dismissed as hallucination or psychosis as participation in a perennial human capacity for dream-mediated knowledge.",
        "in_the_fiction": "Dick does not depict Asclepian dream rituals directly in his fiction, but the pattern of revelatory dreams pervades his work. Characters in A Maze of Death (1970) receive communications from a 'Intercessor' figure with Asclepian qualities. The healing vision in VALIS (1981) — where information about his son's medical condition arrives during an altered state — echoes the Asclepian pattern of diagnostic dreams.",
        "in_the_exegesis": "Dick writes about Asclepius as a reference point for legitimizing his dream experiences. He draws parallels between his own receipt of medical information (the hernia diagnosis) during visionary states and the Asclepian tradition of receiving diagnostic and therapeutic knowledge through dreams. This connection allows PKD to treat his experiences as an instance of a well-documented ancient practice.",
        "intellectual_background": "The Asclepian healing dream tradition is documented in ancient sources (Aristides's Sacred Tales, inscriptions at Epidaurus) and analyzed by scholars of ancient religion (Dodds, Meier). PKD likely encountered the tradition through Dodds's The Greeks and the Irrational and through Jungian discussions of therapeutic dreaming.",
        "scholarly_debate": "Kripal reads PKD's Asclepian references as evidence that his experiences belong to a cross-cultural category of extraordinary cognition. Davis notes that PKD's appeal to Asclepius is strategic — positioning his experiences within an ancient tradition adds legitimacy. Palmer observes that PKD cherry-picks from ancient sources to support his interpretive framework.",
        "chronology_summary": "Asclepian references appear in the Exegesis during PKD's attempts to contextualize 2-3-74 within historical precedent, primarily in the late 1970s.",
        "contradictions_summary": "PKD invokes Asclepius to legitimize his experiences while also maintaining that they exceed any historical framework. He wants his visions to be both historically precedented (not unique, therefore not pathological) and genuinely unprecedented (revealing new truth).",
        "editorial_notes": "This is a narrow topic connecting PKD's experiences to ancient healing traditions. Cross-reference with Hypnagogic State, Hypnopompic State, and Jung. Researchers should verify PKD's knowledge of Asclepian practice against the primary and secondary sources available to him.",
        "open_questions": [
            "How accurately does PKD represent the Asclepian incubation tradition, and where does he embellish or misunderstand it?",
            "Does the Asclepian parallel strengthen or weaken the case for the veridicality of PKD's dream-state knowledge?",
            "How does PKD's appeal to Asclepius relate to his other historical reference points (Gnosticism, early Christianity, Neoplatonism)?"
        ]
    },
    "twin-motif": {
        "definition": "The twin motif in PKD's work refers to the pervasive presence of twinning, doubling, and paired selves rooted in the biographical fact of Jane Charlotte Dick, PKD's twin sister who died six weeks after their birth in 1929.",
        "pkd_relevance": "The loss of Jane is widely regarded as the foundational trauma of PKD's life. Her absence haunts his fiction as a compulsive pairing of characters, a fixation on lost or absent doubles, and a recurring sense of incompleteness. PKD himself was aware of this connection, writing about Jane in the Exegesis and acknowledging her influence on his literary imagination.",
        "in_the_fiction": "Dick depicts twinning across his career. In Dr. Bloodmoney (1965), Bill Keller is an unborn twin living parasitically inside his brother Edie. VALIS (1981) presents Phil Dick and Horselover Fat as twinned selves. Flow My Tears (1974) involves identity doubling that evokes twin substitution. The dark-haired girl who recurs across PKD's novels has been read as an anima figure standing in for the lost twin.",
        "in_the_exegesis": "Dick writes about Jane with a mixture of grief and theological speculation. He connects her death to his lifelong sense of being half a person and to the 'Thomas' personality as a kind of recovered twin. He theorizes that the divine syzygy (paired male and female principles) reflects his own twinned nature, making his biographical loss a mirror of cosmic structure.",
        "intellectual_background": "PKD's twin motif engages with Rank's The Double, the literary Doppelganger tradition, Jungian anima/animus theory (the contrasexual twin within the psyche), and the mythological tradition of divine twins (Castor and Pollux, Romulus and Remus). The biographical dimension gives this literary tradition intense personal urgency.",
        "scholarly_debate": "Sutin treats the twin motif as the key to PKD's psychological makeup. Rickman documents the biographical facts surrounding Jane's death. Palmer reads the twin motif through psychoanalytic theory as a figure of the repressed. Mackey argues that the twin motif is overdetermined — both biographically real and philosophically meaningful — and that reducing it to either dimension impoverishes interpretation.",
        "chronology_summary": "The twin motif appears from PKD's earliest fiction and persists through his final works, never losing its emotional charge. It reaches its most explicit autobiographical treatment in VALIS and the Exegesis.",
        "contradictions_summary": "PKD treats the twin motif as both a source of pathological incompleteness (the missing half that can never be restored) and a source of creative power (the absent twin as muse, as motivating absence). He cannot resolve whether Jane's death damaged him irreparably or shaped him into the writer he became.",
        "editorial_notes": "Cross-reference with Double/Doppelganger (the structural motif), Identity Diffusion (the psychological effect), and Archetype (the anima interpretation). Handle Jane's death with biographical respect — this is a real loss, not merely a literary device.",
        "open_questions": [
            "How much of PKD's doubling obsession is attributable to Jane's death versus his engagement with the literary Doppelganger tradition?",
            "Does PKD's fictional treatment of twins evolve over his career, or does it remain fundamentally static?",
            "How does the twin motif interact with PKD's interest in Gnostic syzygies and paired cosmic principles?"
        ]
    },
    "therapy-psychiatry": {
        "definition": "Therapy and psychiatry in PKD's work encompass the institutional and interpersonal dimensions of mental health treatment — therapeutic encounters, psychiatric authority, rehabilitation programs, and PKD's own ambivalent relationship with the psychiatric profession.",
        "pkd_relevance": "PKD both sought and resisted psychiatric help throughout his life, and this ambivalence permeates his fiction. His therapists and psychiatrists are sometimes sympathetic but often agents of social control. His treatment centers are sometimes healing environments but more often systems of containment. This reflects PKD's Laingian suspicion that psychiatry pathologizes valid perceptions.",
        "in_the_fiction": "Dick depicts therapeutic and psychiatric settings in Clans of the Alphane Moon (1964), an entire society organized by psychiatric diagnostic categories. Martian Time-Slip (1964) features Dr. Glaub, a sympathetic but limited psychiatrist. A Scanner Darkly (1977) presents New-Path, a rehabilitation program that is itself a front for the drug it purports to treat. The psychiatric ward recurs across PKD's fiction as a space of ambiguous authority.",
        "in_the_exegesis": "Dick writes about his own therapy experiences and engages in extensive self-analysis throughout the Exegesis. He applies various psychological frameworks (Jungian, Freudian, neuropsychological) to his own experiences, effectively conducting a prolonged self-therapy. He also reflects on the limits of psychiatric categories for capturing his 2-3-74 experiences.",
        "intellectual_background": "PKD's treatment of psychiatry is shaped by Laing's anti-psychiatry movement, Szasz's critiques of institutional psychiatry, the Jungian therapeutic tradition, and the broader countercultural suspicion of medical authority in the 1960s-70s. His personal experience in therapy provides empirical grounding.",
        "scholarly_debate": "Sutin documents PKD's therapeutic history. Palmer reads PKD's anti-psychiatric stance as a coherent philosophical position, not merely personal resentment. Mackey argues that PKD's fiction critiques specific institutional practices rather than therapy as such. Davis notes that the Exegesis functions as a form of self-directed therapeutic writing.",
        "chronology_summary": "Psychiatric themes appear from Clans of the Alphane Moon (1964) onward, with the critique deepening through A Scanner Darkly (1977). The Exegesis represents PKD's most sustained engagement with therapeutic self-examination.",
        "contradictions_summary": "PKD critiques psychiatric authority while relying on psychiatric and psychological frameworks for self-understanding. He simultaneously rejects diagnostic categories and uses them, distrusts therapists and engages in prolonged self-therapy.",
        "editorial_notes": "Present PKD's psychiatric encounters as biographical facts and his critiques of psychiatry as intellectual positions. Cross-reference with Schizophrenia, Psychosis, and Addiction for the conditions therapy addresses. Note that PKD's anti-psychiatry reflects a specific historical moment.",
        "open_questions": [
            "Does PKD's fiction offer a coherent alternative to institutional psychiatry, or only a critique?",
            "How does PKD's depiction of therapy compare with contemporaneous anti-psychiatric literature (Laing, Szasz, Kesey)?",
            "Is the Exegesis itself a therapeutic document, and if so, what kind of therapy does it represent?"
        ]
    },
    "gaslighting-brainwashing": {
        "definition": "Gaslighting and brainwashing in PKD's work refer to deliberate, systematic manipulation of another person's perception of reality — whether through institutional power, interpersonal deception, technological means, or cosmic-scale reality engineering.",
        "pkd_relevance": "PKD's fiction is centrally concerned with the possibility that experienced reality has been deliberately falsified by powerful agents. This goes beyond mere deception to include the systematic reconstruction of a victim's entire perceptual and memorial framework. For PKD, gaslighting operates at every scale: interpersonal (manipulative partners), institutional (state propaganda), and cosmic (the Black Iron Prison).",
        "in_the_fiction": "Dick depicts gaslighting and brainwashing across his career. Time Out of Joint (1959) is a sustained gaslighting narrative — an entire town constructed to deceive one man. A Scanner Darkly (1977) presents a protagonist who is simultaneously gaslighter and gaslighted, monitoring himself through a scramble suit. 'Faith of Our Fathers' (1967) reveals that the Party Leader's reality is chemically maintained. The Three Stigmata (1965) presents Eldritch as a cosmic gaslighter.",
        "in_the_exegesis": "Dick writes about the Black Iron Prison as a gaslighting system of cosmic proportions — it projects a false reality over the true one, convincing humanity that the counterfeit world is genuine. He also reflects on instances of personal gaslighting, including the mysterious break-in of 1971, which he sometimes interprets as a deliberate attempt to destabilize his sense of reality.",
        "intellectual_background": "PKD's gaslighting theme draws on Cold War brainwashing anxieties (the Manchurian Candidate era), Lifton's work on thought reform, the Gnostic concept of the Archons as reality-manipulators, and the philosophical tradition of the deceiving deity (Descartes's evil demon). The term 'gaslighting' itself comes from the 1944 film, though PKD's treatment exceeds the interpersonal to encompass institutional and cosmic deception.",
        "scholarly_debate": "Freedman reads PKD's gaslighting narratives as political allegory — the state as reality-manipulator. Barlow connects them to propaganda theory and manufactured consent. Davis argues that PKD's cosmic gaslighting (the BIP) represents the most radical extension of the concept — gaslighting as the fundamental condition of embodied existence.",
        "chronology_summary": "Gaslighting and brainwashing themes appear throughout PKD's career, from early political stories through the mature novels. They intensify in the Exegesis, where the BIP represents cosmic gaslighting.",
        "contradictions_summary": "PKD depicts gaslighting as both a specific institutional practice (state manipulation) and a universal cosmic condition (the BIP). If all experienced reality is gaslighted, the concept loses its distinctive meaning — there is no un-gaslighted baseline for comparison.",
        "editorial_notes": "Cross-reference with False Reality (the broader theme), Control Systems (the power structures), and Surveillance (the monitoring dimension). Note that PKD's use of 'gaslighting' is often anachronistic — he describes the pattern without using the term.",
        "open_questions": [
            "How does PKD's cosmic gaslighting concept (BIP) relate to Descartes's evil demon and contemporary simulation theory?",
            "Does PKD's fiction offer any reliable method for detecting gaslighting, or is it always discovered by accident?",
            "How do PKD's personal experiences of perceived manipulation shape his fictional treatment of gaslighting?"
        ]
    }
}


def update_topic(filepath, dossier):
    """Update a topic JSON file with dossier content."""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Only update topics that are still in scanning status
    if data.get('status') == 'drafted':
        print(f"  SKIP (already drafted): {filepath}")
        return False

    # Fill in narrative fields
    for key in ['definition', 'pkd_relevance', 'in_the_fiction', 'in_the_exegesis',
                 'intellectual_background', 'scholarly_debate', 'chronology_summary',
                 'contradictions_summary', 'editorial_notes']:
        if key in dossier:
            data[key] = dossier[key]

    # Fill open_questions
    if 'open_questions' in dossier:
        data['open_questions'] = dossier['open_questions']

    # Update status
    data['status'] = 'drafted'

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"  DRAFTED: {filepath}")
    return True


def main():
    ai_dir = os.path.join(STUDIES_DIR, 'ai', 'topics')
    psy_dir = os.path.join(STUDIES_DIR, 'psychology', 'topics')

    drafted = 0
    skipped = 0

    print("=== AI STUDY TOPICS ===")
    for slug, dossier in AI_DOSSIERS.items():
        filepath = os.path.join(ai_dir, f"{slug}.json")
        if os.path.exists(filepath):
            if update_topic(filepath, dossier):
                drafted += 1
            else:
                skipped += 1
        else:
            print(f"  NOT FOUND: {filepath}")

    print("\n=== PSYCHOLOGY STUDY TOPICS ===")
    for slug, dossier in PSY_DOSSIERS.items():
        filepath = os.path.join(psy_dir, f"{slug}.json")
        if os.path.exists(filepath):
            if update_topic(filepath, dossier):
                drafted += 1
            else:
                skipped += 1
        else:
            print(f"  NOT FOUND: {filepath}")

    print(f"\n=== COMPLETE: {drafted} topics drafted, {skipped} skipped ===")


if __name__ == '__main__':
    main()
