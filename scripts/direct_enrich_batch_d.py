#!/usr/bin/env python3
"""Direct enrichment — importance-4 biography, pre-1963 (16 entries).
Follows BIOGRAPHY_AND_EXEGESIS_WORKS_METHOD.md. Facts are Lane C/D (paraphrase+
cite; no fabricated quotes). Verbatim quotes only where verified in the Exegesis.
Idempotent; applies by id."""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(ROOT, "site", "public", "data", "biography", "curated.json")

S = lambda a, w, lane, loc, sup: {"author": a, "work": w, "lane": lane, "locator": loc, "supports": sup}
SUTIN = lambda loc, sup: S("Sutin", "Divine Invasions", "C", loc, sup)
ARNOLD = lambda loc, sup: S("Arnold", "The Divine Madness of Philip K. Dick", "C", loc, sup)
ANNE = lambda loc, sup: S("Anne R. Dick", "The Search for Philip K. Dick", "C", loc, sup)

E = {
 "pkd_bio_1929_incubator": {
  "event": "The premature Philip is kept alive in an incubator weeks after his twin Jane dies — survival shadowed by loss.",
  "narrative": ("Born six weeks premature in December 1928, Philip and his twin sister Jane were underweight and "
    "undernourished. Jane died in January 1929; Philip was kept alive in an incubator and pulled through. The "
    "asymmetry of that survival — one twin lost, one saved — became, in his own later telling, the wound beneath "
    "everything: the missing sister he spent a life writing toward. (The bare medical facts are Lane C; the meaning "
    "he assigned them is Lane B, and is treated in the [[pkd_bio_1929_jane_death]] entry.)"),
  "sources": [SUTIN("ch. 1", "the premature twin birth, Jane's death, and Philip's incubator survival")],
  "lanes": ["C"], "confidence": "high",
 },
 "pkd_bio_1931_parent_separation": {
  "event": "Edgar and Dorothy Dick's marriage breaks down; Dorothy will become the custodial parent of the young Philip.",
  "narrative": ("Philip's parents, Edgar and Dorothy, separated during his early childhood; the marriage did not "
    "survive, and Dorothy — a strong-willed, ambitious woman working in federal government — became the parent who "
    "raised him. The absent father and the intense, difficult bond with the mother recur across the fiction as the "
    "Terrible Father and the cold, controlling maternal figure. Sources vary on the exact chronology of separation "
    "and divorce, so the portal fixes the fact and not the precise date."),
  "sources": [SUTIN("ch. 1", "the parents' separation and Dorothy as custodial parent"),
              ARNOLD("ch. 1", "the psychodynamic weight of the absent father and difficult mother")],
  "lanes": ["C"], "confidence": "medium",
  "notes": "Exact separation/divorce dating varies across sources; the portal states the fact, not a contested date.",
 },
 "pkd_bio_1935_separation": {
  "event": "The divorce is finalized and Dorothy raises Philip largely alone, moving between Washington and Berkeley.",
  "narrative": ("With the divorce settled, Dorothy raised Philip on her own, the household moving with her "
    "government work between Washington, D.C. and the Bay Area before settling in Berkeley. The instability of these "
    "years — a single, demanding mother, frequent moves, chronic childhood anxiety and early asthma — is the soil "
    "of the suburban unease and fragile domesticity that fills his mainstream novels."),
  "sources": [SUTIN("ch. 1", "the post-divorce childhood, the moves, and the Berkeley settlement")],
  "lanes": ["C"], "confidence": "medium",
 },
 "pkd_bio_1940_sf_discovery": {
  "event": "A twelve-year-old Philip discovers pulp science-fiction magazines — the genre he would enter and remake.",
  "narrative": ("Around 1940 Philip picked up the science-fiction pulps — the era's *Stirring Science Stories* and "
    "*Astounding* among them — and the genre took hold. He read voraciously and began to imagine writing it "
    "himself. What he would eventually do to the form — turn its ray-guns and rockets into instruments for "
    "epistemology and theology — starts here, in a boy's magazine habit."),
  "sources": [SUTIN("ch. 1", "PKD's boyhood discovery of the SF pulps")],
  "lanes": ["C"], "confidence": "high",
 },
 "pkd_bio_1948_marriage_marlin": {
  "event": "At nineteen PKD marries Jeanette Marlin; the first marriage is brief and quickly over.",
  "narrative": ("Philip's first marriage, to Jeanette Marlin in 1948, lasted only months. He was nineteen, still "
    "finding his footing in Berkeley's bohemian-intellectual scene around the record shop and the university. The "
    "marriage's speed and collapse set a pattern — five marriages in all — that his fiction reworks as the "
    "recurring figure of the dangerous, unreachable, or departing woman (the 'dark-haired girl')."),
  "sources": [SUTIN("ch. 2", "the brief 1948 marriage to Jeanette Marlin")],
  "lanes": ["C"], "confidence": "high",
 },
 "pkd_bio_1949_university_music": {
  "event": "PKD works at University Radio / Art Music on Telegraph Avenue — the Berkeley record-store years that fed his lifelong music love.",
  "narrative": ("Through the late 1940s and early 1950s Philip clerked and managed at the Telegraph Avenue record "
    "shops (University Radio, later Art Music), an education in classical music, opera, and German Lieder that "
    "marks the fiction from *Doctor Bloodmoney* to the Linda Fox of *The Divine Invasion*. The store, its "
    "customers, and the surrounding Berkeley radical culture also gave him the milieu of his realist novels."),
  "sources": [SUTIN("ch. 2", "the University Radio / Art Music record-store years"),
              ANNE("", "the depth of PKD's musical knowledge and its Berkeley roots")],
  "lanes": ["C"], "confidence": "high",
  "links": {"exegesis_work": None},
 },
 "pkd_bio_1950_marriage_kleo": {
  "event": "PKD marries Kleo Apostolides; the Berkeley marriage spans his apprenticeship and first sales.",
  "narrative": ("Philip married Kleo Apostolides in 1950. The marriage lasted through the whole of his "
    "apprenticeship — the pulp story sales, the first novels, the FBI's mild attention to the couple's left-wing "
    "Berkeley circle — until it gave way in the mid-1950s to his involvement with Anne Rubenstein. Kleo is the "
    "steadying presence behind the years when he was learning to write for a living."),
  "sources": [SUTIN("ch. 2", "the 1950 marriage to Kleo Apostolides and the apprenticeship years")],
  "lanes": ["C"], "confidence": "high",
 },
 "pkd_bio_1951_first_story_sales": {
  "event": "PKD begins selling short stories to the SF pulps, launching a torrent of early short fiction.",
  "narrative": ("In 1951-52 Philip broke through as a professional, selling story after story to the science-"
    "fiction magazines — dozens within a couple of years. The short form was his laboratory: the androids, "
    "simulacra, paranoid small men, and reality-slippage that would power the novels were all first tested at "
    "story length. He wrote, at the same time, the realist novels no one would buy."),
  "sources": [SUTIN("ch. 3", "the 1951-52 breakthrough into professional short-story sales")],
  "lanes": ["C"], "confidence": "high",
 },
 "pkd_bio_1954_ace_acceptance": {
  "event": "Ace Books accepts PKD's first novel for publication as a paperback original.",
  "narrative": ("Ace Books took *Solar Lottery* for its paperback line — the acceptance that made Philip a "
    "novelist. Ace's Donald Wollheim and the Ace Double format would carry much of his 1950s-60s output, the "
    "cheap paperbacks that were the genre's engine and its ghetto. PKD's ambition to escape into mainstream "
    "fiction ran alongside, and mostly failed, for another decade."),
  "sources": [SUTIN("ch. 3", "Ace's acceptance of the first novel")],
  "lanes": ["C"], "confidence": "high",
 },
 "pkd_bio_1955_solar_lottery": {
  "event": "PKD's debut novel Solar Lottery appears from Ace — his entry into book-length SF.",
  "narrative": ("*Solar Lottery* (1955) launched Philip's novel career: a densely plotted future of "
    "power-by-lottery, twitching with the paranoia about systems and hidden control that never left his work. It "
    "sold well enough to establish him as a working SF novelist. The realist novels he cared about more stayed in "
    "the drawer."),
  "sources": [SUTIN("ch. 3", "the 1955 publication and reception of Solar Lottery")],
  "lanes": ["C"], "confidence": "high",
  "links": {"works": ["/works/solar-lottery"]},
 },
 "pkd_bio_1956_marriage_anne": {
  "event": "PKD marries Anne Williams Rubenstein and moves to rural Point Reyes — the marriage of the mainstream years.",
  "narrative": ("Philip married Anne Rubenstein, a widow with three daughters, and settled with her in Point "
    "Reyes Station in Marin County. The Point Reyes years (roughly 1958-64) were his most domestically settled and, "
    "by Anne's account, among his most productive — the mainstream novels and the run toward *The Man in the High "
    "Castle*. The marriage's later deterioration, and how much amphetamine and paranoia it involved, is contested "
    "between Anne's memoir and Sutin's biography."),
  "sources": [ANNE("", "the Point Reyes marriage from the inside"),
              SUTIN("ch. 4", "the 1958-64 marriage to Anne and the Point Reyes period")],
  "lanes": ["C"], "confidence": "high",
  "dispute": {"summary": "Anne Dick and Sutin differ on the character of the marriage and how drug-dependent the productive years were.",
    "positions": [
      {"who": "Anne R. Dick (The Search)", "claim": "the Point Reyes years were relatively stable and productive, less amphetamine-driven than later accounts imply"},
      {"who": "Sutin (Divine Invasions)", "claim": "narrates a marriage increasingly strained by PKD's instability and drug use"}]},
 },
 "pkd_bio_1958_breakdown": {
  "event": "PKD suffers a psychological crisis at Point Reyes — anxiety, agoraphobia, and marital strain converge.",
  "narrative": ("Settling into the Point Reyes marriage, Philip went through a period of acute anxiety, "
    "agoraphobia, and psychosomatic illness that sent him into therapy. The crisis is an early instance of the "
    "pattern that recurs across his life: episodes of severe distress braided together with intense creativity. "
    "How much was situational and how much a standing condition is read differently by Sutin and by the clinician "
    "Arnold."),
  "sources": [SUTIN("ch. 4", "the late-1950s anxiety crisis and therapy"),
              ARNOLD("ch. 1", "the crisis within a longitudinal clinical reading")],
  "lanes": ["C"], "confidence": "medium",
 },
 "pkd_bio_1960_daughter_laura": {
  "event": "Daughter Laura Archer Dick is born to Philip and Anne in Marin County.",
  "narrative": ("Laura, Philip's first biological child, was born in 1960 during the Point Reyes marriage. "
    "Fatherhood is a quiet undercurrent in the fiction — the endangered or precognitively-sensed child (as with "
    "the later intuition about his son Christopher) — and Laura appears by name in his account of the 1963 'band "
    "of darkness' vision he shared with her."),
  "sources": [SUTIN("ch. 4", "Laura's 1960 birth")],
  "lanes": ["C"], "confidence": "high",
 },
 "pkd_bio_1961_i_ching_study": {
  "event": "PKD takes up the I Ching as a working divination and composition tool — the oracle behind The Man in the High Castle.",
  "narrative": ("From the early 1960s Philip consulted the *I Ching*, the Chinese Book of Changes, as a daily "
    "oracle and, notoriously, as a compositional instrument: he used its hexagrams to determine plot turns in "
    "*The Man in the High Castle*, whose characters consult the same oracle. The book seeded a lifelong interest "
    "in whether an information-system could speak with intent — a question that returns, transformed, in the "
    "Exegesis' living-information theology. His attitude toward the oracle later soured; he came to suspect it of "
    "malice."),
  "sources": [SUTIN("ch. 5", "PKD's use of the I Ching in composing The Man in the High Castle")],
  "lanes": ["C"], "confidence": "high",
  "links": {"works": ["/works/the-man-in-the-high-castle"]},
 },
 "pkd_bio_1962_band_darkness": {
  "event": "On Good Friday PKD and his daughter see a 'band of darkness' cross the sky — an omen he later tied to a death.",
  "narrative": ("Philip reported that he and his daughter Laura watched a band of darkness travel across the sky "
    "one Good Friday. He returned to the image for years, reading it in the Exegesis as an omen bound to a death "
    "and to the sacred-time logic of 2-3-74. It sits with the roughly contemporaneous vision of a vast metallic "
    "face in the sky — the 'Palmer Eldritch' / Terrible Father image — among the pre-1974 experiences he later "
    "treated as rehearsals for the main event."),
  "sources": [S("PKD", "Exegesis", "B", "", "PKD's own recollection and interpretation of the Good Friday band of darkness")],
  "lanes": ["B"], "confidence": "medium",
  "quotes": [{"text": "The band of darkness which I and Laura saw passing across the sky on Good Friday... I knew, when I saw that band of darkness travelling across the sky, that it was related to his death.",
              "speaker": "PKD", "source": "Exegesis", "lane": "B"}],
  "notes": "Lane B self-report; dating and interpretation are PKD's own.",
 },
 "pkd_bio_1963_marriage_hackett": {
  "event": "PKD marries Nancy Hackett — the fourth marriage, spanning the peak productive years and the slide toward crisis.",
  "narrative": ("Philip's marriage to Anne having ended, he married Nancy Hackett in 1963. The Nancy years cover "
    "his most prolific stretch — the mid-1960s burst that produced *Palmer Eldritch*, *Now Wait for Last Year*, and "
    "many others — and their unraveling by 1970, when Nancy left with their daughter Isa, opens directly onto the "
    "San Rafael collapse, the break-in, and Vancouver."),
  "sources": [SUTIN("ch. 5", "the 1963 marriage to Nancy Hackett and the productive mid-1960s")],
  "lanes": ["C"], "confidence": "high",
 },
}

def main():
    data = json.load(open(PATH, encoding="utf-8"))
    by_id = {}
    for e in data: by_id.setdefault(e["id"], e)
    done = []
    for eid, patch in E.items():
        if eid in by_id:
            # drop null-valued link keys
            if "links" in patch:
                patch["links"] = {k: v for k, v in patch["links"].items() if v}
                if not patch["links"]: del patch["links"]
            by_id[eid].update(patch); done.append(eid)
        else: print("  WARN missing", eid)
    json.dump(data, open(PATH, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print(f"batch D: enriched {len(done)} / {len(E)}")
    print("total enriched:", sum(1 for e in data if e.get("narrative")), "/", len(data))

if __name__ == "__main__": main()
