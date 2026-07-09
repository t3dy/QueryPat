#!/usr/bin/env python3
"""Direct enrichment — importance-4 biography, 1964-1973 (10 entries)."""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(ROOT, "site", "public", "data", "biography", "curated.json")
S = lambda a, w, lane, loc, sup: {"author": a, "work": w, "lane": lane, "locator": loc, "supports": sup}
SUTIN = lambda loc, sup: S("Sutin", "Divine Invasions", "C", loc, sup)
ARNOLD = lambda loc, sup: S("Arnold", "The Divine Madness of Philip K. Dick", "C", loc, sup)
PKDL = lambda sup: S("PKD", "Selected Letters", "E", "", sup)
PKDX = lambda sup: S("PKD", "Exegesis", "B", "", sup)

E = {
 "pkd_bio_1964_three_stigmata": {
  "event": "PKD writes The Three Stigmata of Palmer Eldritch, transmuting a metallic-face sky vision into his darkest theology.",
  "narrative": ("In 1964, in the middle of an astonishingly prolific run, Philip wrote *The Three Stigmata of "
    "Palmer Eldritch* — the novel of Can-D and Chew-Z, of a returning entrepreneur who may be God or a devouring "
    "alien god. He traced its central image, the vast metallic face with dead eyes and steel teeth, to a vision he "
    "had had of a cruel face filling the sky. It is the book he was later most frightened by, reading it in the "
    "Exegesis as a glimpse of the *anti*-God, the dark twin of the benign Ubik/Valis."),
  "sources": [SUTIN("ch. 5", "the 1964 composition and the sky-face vision behind the novel"),
              PKDX("PKD's later reading of the novel as a vision of the evil deity")],
  "lanes": ["C", "B"], "confidence": "high",
  "links": {"exegesis_work": "/exegesis/works/the-three-stigmata-of-palmer-eldritch"},
 },
 "pkd_bio_1967_voice_creator": {
  "event": "Under LSD PKD hears a Latin voice — 'I am the breath of my Creator' — a line he mined for years.",
  "narrative": ("Philip's few LSD experiences were mostly terrifying — a plunge into a Latin-inflected, timeless "
    "damnation. From that territory came a phrase he never let go of: *I am the breath of my Creator, and as He "
    "inhales and exhales, I live.* He returned to it in the Exegesis as a statement of the creature's utter "
    "dependence on God — the human as something breathed in and out by the divine. The drug did not, on his own "
    "later account, produce the truth; it only opened a door onto material he spent the Exegesis interpreting."),
  "sources": [PKDX("verbatim Latin-voice line, recalled and interpreted in the Exegesis"),
              SUTIN("ch. 6", "PKD's limited and largely negative LSD experiences")],
  "lanes": ["B", "C"], "confidence": "medium",
  "quotes": [{"text": "I am the breath of my Creator, and as He inhales and exhales, I live.",
              "speaker": "PKD", "source": "Exegesis", "lane": "B"}],
 },
 "pkd_bio_1968_sarill_houseguest_maze": {
  "event": "William Sarill becomes a long-term houseguest; conversations feed the theology that becomes A Maze of Death.",
  "narrative": ("The friend and fan William Sarill first met Philip in 1968 and stayed with him for over a month. "
    "Their long conversations about religion and metaphysics fed into the invented theology of *A Maze of Death* — "
    "the Mentufacturer, the Intercessor, the Walker-on-Earth — which PKD built as a working pantheon and later, in "
    "the Exegesis, half-suspected he had discovered rather than invented."),
  "sources": [SUTIN("ch. 6", "Sarill's 1968 visit and its bearing on the Maze theology")],
  "lanes": ["C"], "confidence": "medium",
  "links": {"exegesis_work": "/exegesis/works/a-maze-of-death"},
 },
 "pkd_bio_1969_ubik": {
  "event": "PKD publishes Ubik — the half-life novel he would later read as accidental scripture.",
  "narrative": ("*Ubik* (1969) is the novel of a decaying half-life world sustained by a mysterious spray-can "
    "force. At publication it read as PKD's finest entropy-and-false-reality machine. After 2-3-74 he re-read it "
    "as unintended scripture — Runciter the Logos, Ubik the immanent Holy Spirit — the single work he returns to "
    "most in the Exegesis after *VALIS* itself."),
  "sources": [SUTIN("ch. 6", "the 1969 publication of Ubik"),
              PKDX("PKD's later theological reading of his own novel")],
  "lanes": ["C", "B"], "confidence": "high",
  "links": {"exegesis_work": "/exegesis/works/ubik", "works": ["/works/ubik"]},
 },
 "pkd_bio_1971_arnold_amphetamine_paranoia": {
  "event": "Arnold reads the peak 1971 paranoia around the break-in as amphetamine-driven, not evidence of real pursuers.",
  "narrative": ("The clinician Kyle Arnold treats the height of Philip's 1971 paranoia — the conviction of being "
    "watched and pursued that surrounded the [[pkd_bio_1971_burglary]] — as substantially a product of heavy "
    "amphetamine use and sleeplessness rather than of actual surveillance. It is the clearest test case for the "
    "portal's clinical-versus-literal tension: the same events read as persecution by PKD and as symptom by "
    "Arnold, with neither reading fully disprovable."),
  "sources": [ARNOLD("ch. 1", "the amphetamine-driven clinical reading of the 1971 paranoia")],
  "lanes": ["C"], "confidence": "medium",
  "dispute": {"summary": "Whether the 1971 paranoia tracked real threats or was chemically produced.",
    "positions": [{"who": "PKD (letters)", "claim": "he was genuinely surveilled and pursued"},
                  {"who": "Arnold (clinical)", "claim": "the fear was amphetamine-driven, without a real external agent"}]},
 },
 "pkd_bio_1972_vancouver": {
  "event": "PKD flies to Vancouver as a convention guest of honor and decides to stay — the break from his old life.",
  "narrative": ("In February 1972 Philip left San Rafael for Vancouver to be guest of honor at a science-fiction "
    "convention, where he delivered \"The Android and the Human,\" and impulsively resolved to stay in Canada. The "
    "move severed him from the wreckage of the previous two years; it also stranded him, and within weeks led to "
    "the [[pkd_bio_1972_vancouver_suicide_attempt]] and X-Kalay. Vancouver is the hinge between the San Rafael "
    "collapse and the Orange County rebirth."),
  "sources": [SUTIN("ch. 7", "the Vancouver convention and the decision to remain in Canada")],
  "lanes": ["C"], "confidence": "high",
 },
 "pkd_bio_1972_vancouver_x_kalay_arnold": {
  "event": "Arnold frames the X-Kalay stay as a misfit refuge — a heroin program housing a suicidal amphetamine user.",
  "narrative": ("After the suicide attempt Philip entered X-Kalay, a Synanon-style heroin-rehabilitation "
    "community. Arnold notes the mismatch — a program for hardcore narcotics addicts taking in a depressed, "
    "amphetamine-using science-fiction writer — and reads the episode as much as a search for structure and "
    "belonging as for detoxification. PKD both mocked and credited the program; it gave him a floor to stand on "
    "before Fullerton (see [[pkd_bio_1972_vancouver_suicide_attempt]])."),
  "sources": [ARNOLD("ch. 1", "the clinical reading of the X-Kalay stay and its mismatch"),
              SUTIN("ch. 7", "the X-Kalay chronology")],
  "lanes": ["C"], "confidence": "medium",
 },
 "pkd_bio_1973_marriage_tessa": {
  "event": "PKD marries Tessa Busby in Fullerton — the fifth and final marriage, the household of the 2-3-74 years.",
  "narrative": ("Philip married Leslie 'Tessa' Busby in April 1973, months after settling in Fullerton. Much "
    "younger than he, Tessa became the wife of his last decade: the mother of his son Christopher, a witness to "
    "2-3-74, and — through her differing recollection of the golden-fish delivery — one of the sources whose "
    "account of that event does not always match his."),
  "sources": [SUTIN("ch. 7", "the 1973 marriage to Tessa Busby"),
              PKDL("PKD's contemporaneous letters from the early Fullerton period")],
  "lanes": ["C", "E"], "confidence": "high",
  "links": {"people": ["/dictionary/tessa"]},
 },
 "pkd_bio_1973_csuf_talk": {
  "event": "PKD records a talk at Cal State Fullerton, an early sign of his re-emergence into public and academic life.",
  "narrative": ("In July 1973, newly settled in Orange County, Philip recorded a talk at California State "
    "University, Fullerton. It marks his re-emergence after the long fiction hiatus of 1970-72 — the beginning of "
    "the academic and fan attention that would culminate in the Metz keynote of 1977 and the eventual donation of "
    "his manuscripts to the CSUF library."),
  "sources": [SUTIN("ch. 8", "PKD's Fullerton-period public appearances"),
              PKDL("PKD's letters on the CSUF connection")],
  "lanes": ["C", "E"], "confidence": "medium",
 },
 "pkd_bio_1973_christopher_birth": {
  "event": "Son Christopher Dick is born to Philip and Tessa in Fullerton — the child of the 2-3-74 years.",
  "narrative": ("Christopher, Philip's third child and only son, was born in July 1973. His birth roots the "
    "Fullerton household that 2-3-74 would erupt into a year later — and it is Christopher whose undiagnosed "
    "hernia PKD believed the March 1974 intelligence revealed to him (see [[pkd_bio_1974_03_son_diagnosis]]), the "
    "most-cited apparently-veridical moment of the whole experience."),
  "sources": [SUTIN("ch. 7", "Christopher's 1973 birth"),
              PKDL("PKD's letters announcing his son's birth")],
  "lanes": ["C", "E"], "confidence": "high",
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
    print(f"batch E: enriched {len(done)} / {len(E)}")
    print("total enriched:", sum(1 for e in data if e.get("narrative")), "/", len(data))

if __name__ == "__main__": main()
