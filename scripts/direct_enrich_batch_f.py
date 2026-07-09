#!/usr/bin/env python3
"""Direct enrichment — importance-4 biography, 1974-1981 (21 entries).
Lane-B/E heavy (2-3-74 concepts and the late letters). Verbatim quotes only
where verified; letter contents paraphrased-and-cited (Lane E)."""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(ROOT, "site", "public", "data", "biography", "curated.json")
S = lambda a, w, lane, loc, sup: {"author": a, "work": w, "lane": lane, "locator": loc, "supports": sup}
SUTIN = lambda loc, sup: S("Sutin", "Divine Invasions", "C", loc, sup)
ARNOLD = lambda loc, sup: S("Arnold", "The Divine Madness of Philip K. Dick", "C", loc, sup)
PKDL = lambda sup: S("PKD", "Selected Letters", "E", "", sup)
PKDX = lambda sup: S("PKD", "Exegesis", "B", "", sup)
CLIN = {"summary": "Read as revelation by PKD and as symptom by the clinical literature; the portal keeps both.",
        "positions": [{"who": "PKD (Exegesis/letters)", "claim": "a genuine disclosure of the real"},
                      {"who": "Clinical frame (Arnold)", "claim": "an episode legible in psychiatric terms"}]}

E = {
 "pkd_bio_1974_03_zebra": {
  "event": "PKD names the intelligence behind 2-3-74 'Zebra' — a mind that camouflages itself perfectly in the ordinary world.",
  "narrative": ("In March 1974 Philip began calling the intelligence he believed was acting on him *Zebra*: a "
    "living information-field that hides in plain sight the way a zebra's stripes dissolve into the grass, "
    "mimicking ordinary reality so exactly that it is invisible. Zebra is the first of the many names — VALIS, the "
    "plasmate, the Holy Spirit — he gave the same suspected agency, and the one that best captures his intuition "
    "that God is not elsewhere but camouflaged in the trash of the everyday."),
  "sources": [PKDX("PKD's development of the Zebra concept in the Exegesis")],
  "lanes": ["B"], "confidence": "medium", "dispute": CLIN,
  "links": {"exegesis_work": "/exegesis/works/valis", "theophany": "/theophanies/zebra-mimicry-1974"},
 },
 "pkd_bio_1974_philosophical_speculation": {
  "event": "PKD begins the systematic Exegesis speculation on time, reality, and God that will occupy his last eight years.",
  "narrative": ("From 1974 the private theorizing PKD had always done became a sustained, obsessive project: the "
    "Exegesis, a nightly attempt to explain 2-3-74 by every philosophical and religious system he could reach. "
    "The speculation is genuinely systematic — hypothesis, revision, self-refutation — even as its object keeps "
    "slipping. It is the intellectual engine of everything he wrote after 1974."),
  "sources": [PKDX("the beginning of sustained Exegesis speculation")],
  "lanes": ["B"], "confidence": "high",
 },
 "pkd_bio_1974_black_iron_prison": {
  "event": "PKD develops the Black Iron Prison — our world as a concealed carceral Rome, 'the Empire never ended.'",
  "narrative": ("Among the earliest and most durable Exegesis structures is the Black Iron Prison: the idea that "
    "the ordinary world is a concealed prison, that beneath 1974 Fullerton lies the Rome of the first century, and "
    "that history since has been an illusion masking an unbroken carceral order — *the Empire never ended*. It is "
    "the political and Gnostic face of his theology, set against the liberating Palm Tree Garden, and the seed of "
    "*VALIS* and *Radio Free Albemuth*."),
  "sources": [PKDX("PKD's development of the Black Iron Prison / hidden-Rome concept")],
  "lanes": ["B"], "confidence": "high",
  "links": {"exegesis_work": "/exegesis/works/valis", "theophany": "/theophanies/black-iron-prison-1974"},
 },
 "pkd_bio_1975_brunner_cia_breakin": {
  "event": "PKD writes John Brunner about a news clipping on CIA break-ins, reopening the mystery of his own 1971 burglary.",
  "narrative": ("In January 1975 Philip wrote the British SF novelist John Brunner about a London *Times* clipping "
    "reporting CIA-linked break-ins, seizing on it as possible corroboration that his own [[pkd_bio_1971_burglary]] "
    "had been a government operation. The letter shows how he kept the break-in alive as an open case, folding each "
    "new scrap of news into a theory that never settled."),
  "sources": [PKDL("PKD's Jan 1975 letter to John Brunner on the CIA-break-in clipping")],
  "lanes": ["E"], "confidence": "medium",
 },
 "pkd_bio_1975_le_guin_letter": {
  "event": "PKD writes Ursula K. Le Guin about The Lathe of Heaven and their uneasy literary kinship.",
  "narrative": ("Philip's April 1975 letter to Ursula K. Le Guin engages *The Lathe of Heaven* — a novel widely "
    "read as Dickian in its reality-remaking premise — and their complicated mutual regard. Le Guin was among the "
    "few major writers who took him seriously as an artist; the correspondence is a record of PKD reaching toward "
    "the literary respectability the SF ghetto denied him, even as 2-3-74 pulled him toward the Exegesis."),
  "sources": [PKDL("PKD's April 1975 letter to Le Guin on The Lathe of Heaven")],
  "lanes": ["E"], "confidence": "medium",
 },
 "pkd_bio_1975_blissful_linking_it_all_up": {
  "event": "PKD reports a blissful altered-state experience of 'linking it all up' — a moment of total systematic clarity.",
  "narrative": ("In June 1975 Philip described an altered-state experience of *linking it all up*: a flood of "
    "blissful coherence in which the whole tangle of 2-3-74 briefly resolved into a single system. Such episodes "
    "of ecstatic integration alternate, across the Exegesis, with dread and self-suspicion — the manic pole of a "
    "process the clinical literature reads as mood-driven and PKD read as graded revelation."),
  "sources": [PKDL("PKD's June 1975 account of the 'linking it all up' experience"), ARNOLD("ch. 1", "the ecstatic-integration episodes within a mood-disorder frame")],
  "lanes": ["E", "C"], "confidence": "medium", "dispute": CLIN,
 },
 "pkd_bio_1975_christian_research_to_scare_dead": {
  "event": "PKD reports sixteen months and over a thousand dollars spent on intensive early-Christian and Gnostic research.",
  "narrative": ("By mid-1975 Philip had poured sixteen months and, by his own accounting, more than a thousand "
    "dollars into research on early Christianity, Gnosticism, and church history — hunting confirmation that his "
    "3-74 experience matched the apostolic era he believed he had briefly re-entered. The scale of the effort "
    "shows how far the Exegesis had become a genuine, if idiosyncratic, scholarly obsession rather than mere "
    "reverie."),
  "sources": [PKDL("PKD's July 1975 letter reporting the cost and duration of his Christian research")],
  "lanes": ["E"], "confidence": "medium",
 },
 "pkd_bio_1976_harlan_lsd_correction": {
  "event": "PKD publicly corrects the claim that he wrote his fiction on LSD — insisting the drug had almost nothing to do with the work.",
  "narrative": ("In January 1976 Philip objected to the note in Harlan Ellison's *Dangerous Visions* implying he "
    "wrote under the influence of LSD. He was emphatic: his few acid trips were terrifying and unproductive, and "
    "the novels were written on amphetamines-for-stamina and hard work, not psychedelic inspiration. The "
    "correction matters to the record — it is PKD, in his own voice, refusing the hippie-casualty legend and "
    "distinguishing his fiction from his drug use."),
  "sources": [PKDL("PKD's Jan 1976 letter correcting the LSD claim")],
  "lanes": ["E"], "confidence": "high",
 },
 "pkd_bio_1976_ho_on_voice": {
  "event": "PKD hears a voice naming itself 'Ho On' — Greek for 'I AM,' a title of God.",
  "narrative": ("In September 1976 Philip's hypnagogic AI-voice identified itself as *Ho On* — Koine Greek for "
    "\"the one who is,\" the *I AM* by which God names himself to Moses. For PKD the Greek was itself evidence: the "
    "voice spoke the language of the apostolic Levant he believed he had seen, tying the phenomenon to the early "
    "Christian world rather than to his own English-speaking mind."),
  "sources": [PKDX("the Ho On identification, recorded and glossed in the Exegesis")],
  "lanes": ["B"], "confidence": "medium", "dispute": CLIN,
  "quotes": [{"text": "Ho on: Greek for I AM, a title of God.", "speaker": "PKD", "source": "Exegesis", "lane": "B"}],
  "links": {"theophany": "/theophanies/ai-voice-1974"},
 },
 "pkd_bio_1976_living_information": {
  "event": "PKD develops the theory of 'living information' — the cosmos as a self-aware mind made of meaning.",
  "narrative": ("Across 1976-78 Philip worked out one of his central late ideas: that information itself can be "
    "alive, that the universe is a vast mind processing meaning, and that 2-3-74 was that mind reaching into him "
    "and, briefly, thinking through him. Living information is where his theology meets a proto-cybernetic "
    "metaphysics — God as a self-organizing field of meaning rather than a person — and it underwrites the plasmate "
    "of *VALIS*."),
  "sources": [PKDX("the living-information / cosmic-mind theory in the Exegesis")],
  "lanes": ["B"], "confidence": "high",
  "links": {"exegesis_work": "/exegesis/works/valis"},
 },
 "pkd_bio_1977_scanner_darkly": {
  "event": "PKD publishes A Scanner Darkly — his unsentimental elegy for the drug casualties of his own circle.",
  "narrative": ("*A Scanner Darkly* (1977) turns the San Rafael drug years into fiction: Substance D, the split "
    "narcotics-agent/addict Bob Arctor, and a closing dedication naming friends dead or damaged by drugs. It is "
    "PKD's most personal novel and his clearest ethical statement — drug misuse as a decision with a terrible "
    "price, grieved rather than moralized. He read even this book, in the Exegesis, for what its 'dopers' "
    "understood about reality."),
  "sources": [SUTIN("ch. 9", "the 1977 publication and autobiographical roots of A Scanner Darkly")],
  "lanes": ["C"], "confidence": "high",
  "links": {"exegesis_work": "/exegesis/works/a-scanner-darkly"},
 },
 "pkd_bio_1977_jaynes_hurst": {
  "event": "PKD explains Julian Jaynes's bicameral-mind theory to Mark Hurst, adopting it as a frame for his AI voice.",
  "narrative": ("In March 1977 Philip wrote Mark Hurst laying out Julian Jaynes's *The Origin of Consciousness in "
    "the Breakdown of the Bicameral Mind* — the theory that ancient humans experienced the brain's two hemispheres "
    "as a commanding god-voice. PKD seized on it as a naturalistic frame for his own AI voice: perhaps 2-3-74 was "
    "the bicameral mind reasserting itself, the right hemisphere speaking as 'God' to the left."),
  "sources": [PKDL("PKD's March 1977 letter to Mark Hurst on Jaynes")],
  "lanes": ["E"], "confidence": "medium",
 },
 "pkd_bio_1977_jaynes_bennett": {
  "event": "PKD tells Carl Bennett that Jaynes's bicameral theory gives scientific support to his own experience.",
  "narrative": ("Two weeks later Philip wrote Carl Bennett that Jaynes had, in effect, provided scientific "
    "cover for the AI voice — evidence that a person could really hear an internal speaker experienced as divine. "
    "The two 1977 Jaynes letters show him doing what the Exegesis does everywhere: reaching for an external "
    "framework that would make the experience defensible without dissolving its meaning."),
  "sources": [PKDL("PKD's March 1977 letter to Carl Bennett on Jaynes")],
  "lanes": ["E"], "confidence": "medium",
 },
 "pkd_bio_1977_sarill_reencounter_maze": {
  "event": "PKD re-encounters William Sarill after years apart, reconnecting the friendship behind the Maze theology.",
  "narrative": ("In July 1977 Philip re-encountered his old friend William Sarill after a long silence — the "
    "houseguest of 1968 whose conversations had helped shape the invented gods of *A Maze of Death*. The reunion "
    "belongs to the pattern of the Fullerton years: old ties re-forming as PKD, stabilized and newly famous after "
    "Metz, took stock of the life the crisis years had scattered."),
  "sources": [SUTIN("ch. 9", "PKD's Fullerton-period friendships and the Sarill reconnection")],
  "lanes": ["C"], "confidence": "low",
  "links": {"exegesis_work": "/exegesis/works/a-maze-of-death"},
 },
 "pkd_bio_1977_metz_star_wars_claudia": {
  "event": "Back from the Metz keynote, PKD writes Claudia Bush — reading Star Wars and the age's myths against his own theology.",
  "narrative": ("After delivering his notorious Metz address \"If You Find This World Bad, You Should See Some of "
    "the Others\" — in which he told a French audience that reality might be a computer-generated simulation being "
    "revised — Philip wrote his 2-3-74 confidante Claudia Bush in October 1977. The letter measures the era's "
    "popular myths, *Star Wars* among them, against his own conviction that Christian mystery had become literally "
    "operative in the world."),
  "sources": [PKDL("PKD's Oct 1977 letter to Claudia Bush after Metz")],
  "lanes": ["E"], "confidence": "medium",
  "links": {"theophany": "/theophanies/metz-1977"},
 },
 "pkd_bio_1977_valis_theology": {
  "event": "PKD consolidates the scattered Exegesis into a systematic 'VALIS' theology — the framework the novel dramatizes.",
  "narrative": ("Across 1977-79 Philip pulled the sprawling Exegesis toward a system he named for VALIS — Vast "
    "Active Living Intelligence System: the rational information-deity, the plasmate, the two-source cosmology, the "
    "Black Iron Prison and the coming Kingdom. It is less a settled doctrine than a repeatedly-rebuilt scaffold, "
    "and it becomes the explicit subject of the 1981 novel, where PKD splits himself into narrator and the "
    "mad seeker Horselover Fat."),
  "sources": [PKDX("the consolidation of the VALIS theology across the Exegesis")],
  "lanes": ["B"], "confidence": "high",
  "links": {"exegesis_work": "/exegesis/works/valis"},
 },
 "pkd_bio_1981_blade_runner_visit": {
  "event": "PKD visits the Blade Runner production and, after early hostility, is won over by Ridley Scott's realized world.",
  "narrative": ("In 1981 Philip visited the production of *Blade Runner*, the adaptation of *Do Androids Dream of "
    "Electric Sheep?*, and met director Ridley Scott. Initially wary of Hollywood and critical of early script "
    "drafts, he was reportedly stunned by the special-effects footage of the future Los Angeles — recognizing his "
    "own imagined world on the screen. He died in March 1982, months before the film's release."),
  "sources": [SUTIN("ch. 11", "the 1981 Blade Runner set visit and PKD's shift from hostility to enthusiasm")],
  "lanes": ["C"], "confidence": "high",
  "links": {"exegesis_work": "/exegesis/works/do-androids-dream-of-electric-sheep"},
 },
 "pkd_bio_1981_divine_invasion": {
  "event": "PKD publishes The Divine Invasion — the second VALIS-trilogy novel, God re-entering an occluded world.",
  "narrative": ("*The Divine Invasion* (1981) fictionalizes the Exegesis theology directly: a God long exiled "
    "from a world fallen under the demiurge's rule engineers his own return, incarnate as the boy Emmanuel, "
    "companioned by the wise-child Zina (Sophia). Where *VALIS* is a case history of PKD's own doubt, *The Divine "
    "Invasion* is his attempt to write the cosmology straight, as myth."),
  "sources": [SUTIN("ch. 11", "the 1981 publication of The Divine Invasion")],
  "lanes": ["C"], "confidence": "high",
  "links": {"exegesis_work": "/exegesis/works/the-divine-invasion", "works": ["/works/the-valis-trilogy"]},
 },
 "pkd_bio_1981_01_26_perturbation_reality_field": {
  "event": "PKD writes Patricia Warrick that 3-74 was a miracle — a 'perturbation in the reality field.'",
  "narrative": ("In a January 1981 letter to the scholar Patricia Warrick, Philip called 2-3-74 a miracle and a "
    "*perturbation in the reality field* — his most compressed formulation of the event as an objective "
    "disturbance in reality itself rather than a private mental state. The phrasing, poised between physics and "
    "theology, is characteristic of the late letters, where he tried to state the experience for a serious reader "
    "without surrendering its strangeness."),
  "sources": [PKDL("PKD's Jan 26 1981 letter to Patricia Warrick")],
  "lanes": ["E"], "confidence": "medium", "dispute": CLIN,
 },
 "pkd_bio_1981_02_14_lords_supper_hologram": {
  "event": "PKD tells Patricia Warrick the Eucharist kept him in touch with Christ, experienced as a hologram.",
  "narrative": ("In February 1981 Philip wrote Warrick that the Lord's Supper had kept him in living contact with "
    "Christ — whom he described, in his late idiom, as a *hologram*: a projected but real presence, everywhere and "
    "nowhere. The image fuses his information-metaphysics with orthodox sacrament, and shows the devout, almost "
    "conventionally Christian strain that ran alongside the Gnostic speculation to the end."),
  "sources": [PKDL("PKD's Feb 14 1981 letter to Patricia Warrick on the Eucharist")],
  "lanes": ["E"], "confidence": "medium",
 },
 "pkd_bio_1981_galen_type_c_psyche": {
  "event": "Planning The Owl in Daylight, PKD writes his agent Russell Galen about Jaynes and a 'Type C' psyche.",
  "narrative": ("In July 1981, sketching the novel *The Owl in Daylight* he would not live to write, Philip wrote "
    "his agent Russell Galen about Jaynes and a typology of psyches — the mind that hears the god-voice versus the "
    "modern, self-enclosed consciousness. The letter catches him still building theory into fiction at the very "
    "end, the Exegesis feeding the last unfinished book."),
  "sources": [PKDL("PKD's July 1981 letter to Russell Galen on The Owl in Daylight")],
  "lanes": ["E"], "confidence": "low",
 },
}

def main():
    data = json.load(open(PATH, encoding="utf-8"))
    by_id = {}
    for e in data: by_id.setdefault(e["id"], e)
    done = []
    for eid, patch in E.items():
        if eid in by_id:
            if "links" in patch:
                patch["links"] = {k: v for k, v in patch["links"].items() if v}
                if not patch["links"]: del patch["links"]
            by_id[eid].update(patch); done.append(eid)
        else: print("  WARN missing", eid)
    json.dump(data, open(PATH, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print(f"batch F: enriched {len(done)} / {len(E)}")
    print("total enriched:", sum(1 for e in data if e.get("narrative")), "/", len(data))

if __name__ == "__main__": main()
