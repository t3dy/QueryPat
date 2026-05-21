"""Build a canonical PKD works table and public JSON export.

This seeds the database table from the documents table when needed and writes
route-ready JSON bundles for the web app.
"""

from __future__ import annotations

import argparse
import json
import re
import sqlite3
from collections import defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "database" / "unified.sqlite"
DATA_DIR = ROOT / "site" / "public" / "data"
WORKS_DIR = DATA_DIR / "works"
THEMES_DIR = DATA_DIR / "themes"
ARCHIVE_DIR = DATA_DIR / "archive" / "docs"

FICTION_CATEGORIES = {"novels", "short_stories"}

THEME_DEFINITIONS: list[dict[str, Any]] = [
    {
        "slug": "androids",
        "label": "Androids",
        "description": "Synthetic or programmed human figures, including androids, replicants, and the human-machine boundary.",
        "patterns": [r"\bandroids?\b", r"\breplicants?\b", r"synthetic human", r"\bartificial person", r"\bhumaniform\b"],
    },
    {
        "slug": "robots",
        "label": "Robots",
        "description": "Robots, automation, machine labor, and the fear that technology can replace human agency.",
        "patterns": [r"\brobots?\b", r"\bautomata\b", r"\bautomaton\b", r"\bautomation\b", r"\bautofac\b", r"\bmachine(?:s|)\b"],
    },
    {
        "slug": "drugs",
        "label": "Drugs",
        "description": "Amphetamines, narcotics, intoxication, addiction, rehab, and chemically altered consciousness.",
        "patterns": [r"\bdrugs?\b", r"\bdope\b", r"\bamphetamine\b", r"\blsd\b", r"\baddict(?:ion|ed)?\b", r"\brehab\b", r"\bnarcotic\b", r"\bstimulant\b"],
    },
    {
        "slug": "authentic-human",
        "label": "Authentic Human",
        "description": "Human authenticity, empathy, caritas, and the resistance to programmed or mechanical existence.",
        "patterns": [r"authentic human", r"\bempathy\b", r"\bcaritas\b", r"\bhumanity\b", r"\bpersonhood\b", r"\bnon-human\b"],
    },
    {
        "slug": "betrayal",
        "label": "Betrayal",
        "description": "Deception, imposture, treachery, and the collapse of trust between people or institutions.",
        "patterns": [r"\bbetray(?:al|s|ed)?\b", r"\bimpostor(?:s|)\b", r"\bdecept(?:ion|ive|ively)\b", r"\btreason\b", r"\bfraud\b", r"\bdouble agent\b", r"\bcounterfeit\b"],
    },
    {
        "slug": "reality-breakdown",
        "label": "Reality Breakdown",
        "description": "Unstable reality, temporal slippage, projected worlds, and the breakdown of ordinary perception.",
        "patterns": [r"\breality\b", r"\breal(?:ity|ities)\b", r"\bunreal\b", r"\bconstructed\b", r"\bregression\b", r"\bhalf-life\b", r"\borthogonal\b", r"\birreal\b", r"\bprojection\b", r"\bbreakdown\b"],
    },
    {
        "slug": "delusions",
        "label": "Delusions",
        "description": "Paranoia, psychosis, hallucination, schizophrenia, and other forms of unstable perception.",
        "patterns": [r"\bdelusion(?:al|s)?\b", r"\bpsychosis\b", r"\bschizophrenia\b", r"\bparanoia\b", r"\bhallucination(?:s|)\b", r"\bpsychotic\b", r"\bmadness\b"],
    },
    {
        "slug": "illusionary-realities",
        "label": "Illusionary Realities",
        "description": "Simulations, false worlds, mimicry, illusions, and counterfeit reality-systems.",
        "patterns": [r"\billusion(?:s|ary)?\b", r"\bsimulacra\b", r"\bsimulation(?:s|)\b", r"\bcounterfeit\b", r"\bmimic(?:ry|)\b", r"\bfake world\b", r"\billusion machine\b", r"\bvirtual\b"],
    },
    {
        "slug": "memory-identity",
        "label": "Memory & Identity",
        "description": "Amnesia, implanted or false memory, identity instability, and the porous self.",
        "patterns": [r"\bmemory\b", r"\bamnesia\b", r"\bidentity\b", r"\bfalse memory\b", r"\bimplanted memory\b", r"\bself\b", r"\brecall\b"],
    },
    {
        "slug": "time",
        "label": "Time",
        "description": "Temporal distortion, regression, precognition, time slips, and altered historical sequence.",
        "patterns": [r"\btime\b", r"\btemporal\b", r"\bprecogn(?:ition|itive)\b", r"\bregression\b", r"\bout of joint\b", r"\bchron", r"\bfuture\b", r"\bpast\b"],
    },
    {
        "slug": "empire-control",
        "label": "Empire & Control",
        "description": "Tyranny, surveillance, fascism, state power, and coercive social systems.",
        "patterns": [r"\bempire\b", r"\btyrann(?:y|ical)\b", r"\bfascis", r"\bsurveillance\b", r"\bcontrol\b", r"\bpolice state\b", r"\bauthoritarian\b", r"\boccupation\b"],
    },
    {
        "slug": "religion-gnosis",
        "label": "Religion & Gnosis",
        "description": "God, Christ, revelation, Gnosticism, theology, salvation, and mystical interpretation.",
        "patterns": [r"\bgod\b", r"\bchrist\b", r"\bgnosis\b", r"\bgnostic\b", r"\brevelation\b", r"\bdivine\b", r"\btheolog", r"\bvalis\b", r"\bwisdom\b", r"\bsalvation\b", r"\bchurch\b"],
    },
    {
        "slug": "alien-contact",
        "label": "Alien Contact",
        "description": "Aliens, extraterrestrial intelligence, off-world contact, and nonhuman ecologies.",
        "patterns": [r"\balien(?:s|)\b", r"\bextraterrestrial\b", r"\bmartian\b", r"\bganymede\b", r"\bcosmic\b", r"\boff-world\b", r"\bplanet(?:ary|)\b"],
    },
    {
        "slug": "suburbia-domesticity",
        "label": "Suburbia & Domesticity",
        "description": "Family life, marriage, houses, domestic tension, and the suburban everyday.",
        "patterns": [r"\bhouse\b", r"\bhome\b", r"\bfamily\b", r"\bmarriage\b", r"\bdomestic\b", r"\bsuburb", r"\bwife\b", r"\bhusband\b", r"\bchild(?:ren)?\b"],
    },
]

WORK_THEME_OVERRIDES: dict[str, list[str]] = {
    "solar-lottery": ["empire-control", "betrayal", "androids"],
    "the-man-who-japed": ["empire-control", "betrayal", "suburbia-domesticity"],
    "the-cosmic-puppets": ["illusionary-realities", "reality-breakdown", "religion-gnosis"],
    "eye-in-the-sky": ["reality-breakdown", "illusionary-realities", "delusions", "suburbia-domesticity"],
    "time-out-of-joint": ["time", "reality-breakdown", "illusionary-realities", "betrayal"],
    "the-man-in-the-high-castle": ["illusionary-realities", "empire-control", "betrayal", "reality-breakdown"],
    "the-game-players-of-titan": ["alien-contact", "betrayal", "illusionary-realities", "empire-control"],
    "clans-of-the-alphane-moon": ["delusions", "memory-identity", "authentic-human", "suburbia-domesticity"],
    "the-penultimate-truth": ["empire-control", "illusionary-realities", "betrayal", "reality-breakdown"],
    "the-simulacra": ["illusionary-realities", "empire-control", "betrayal", "robots"],
    "dr-bloodmoney-or-how-we-got-along-after-the-bomb": ["reality-breakdown", "empire-control", "betrayal", "time"],
    "now-wait-for-last-year": ["drugs", "time", "betrayal", "reality-breakdown"],
    "the-crack-in-space": ["reality-breakdown", "empire-control", "alien-contact", "robots"],
    "counter-clock-world": ["time", "reality-breakdown", "illusionary-realities", "empire-control"],
    "the-zap-gun": ["empire-control", "illusionary-realities", "robots", "authentic-human"],
    "the-ganymede-takeover": ["alien-contact", "betrayal", "illusionary-realities", "empire-control"],
    "the-preserving-machine-and-other-stories": ["reality-breakdown", "robots", "illusionary-realities", "authentic-human"],
    "our-friends-from-frolix-8": ["empire-control", "authentic-human", "betrayal", "reality-breakdown"],
    "a-maze-of-death": ["reality-breakdown", "religion-gnosis", "delusions", "betrayal"],
    "confessions-of-a-crap-artist": ["betrayal", "suburbia-domesticity", "authentic-human", "memory-identity"],
    "deus-irae": ["religion-gnosis", "reality-breakdown", "delusions", "empire-control"],
    "the-unteleported-man": ["empire-control", "illusionary-realities", "betrayal", "reality-breakdown"],
    "lies-inc": ["empire-control", "illusionary-realities", "betrayal", "reality-breakdown"],
    "radio-free-albemuth": ["religion-gnosis", "reality-breakdown", "empire-control", "delusions"],
    "mary-and-the-giant": ["suburbia-domesticity", "betrayal", "authentic-human", "memory-identity"],
    "nick-and-the-glimmung": ["religion-gnosis", "alien-contact", "illusionary-realities", "authentic-human"],
    "gather-yourselves-together": ["betrayal", "empire-control", "suburbia-domesticity", "reality-breakdown"],
    "voices-from-the-street": ["drugs", "betrayal", "suburbia-domesticity", "reality-breakdown"],
    "do-androids-dream-of-electric-sheep": ["androids", "authentic-human", "reality-breakdown", "illusionary-realities"],
    "five-novels-of-the-1960s-and-70s": ["reality-breakdown", "empire-control", "religion-gnosis", "time", "betrayal"],
    "the-book-of-philip-k-dick": ["suburbia-domesticity", "robots", "authentic-human", "reality-breakdown"],
    "the-collected-stories-of-philip-k-dick-volumes-1-5": ["reality-breakdown", "illusionary-realities", "betrayal", "authentic-human"],
    "the-philip-k-dick-reader": ["reality-breakdown", "authentic-human", "betrayal", "illusionary-realities"],
    "selected-stories-of-philip-k-dick": ["reality-breakdown", "illusionary-realities", "authentic-human", "betrayal"],
    "second-variety-and-other-classic-stories": ["robots", "betrayal", "reality-breakdown", "empire-control"],
    "electric-dreams": ["illusionary-realities", "reality-breakdown", "authentic-human", "betrayal"],
    "the-minority-report-and-other-classic-stories": ["empire-control", "time", "betrayal", "reality-breakdown"],
    "the-short-happy-life-of-the-brown-oxford-and-other-classic-stories": ["reality-breakdown", "illusionary-realities", "authentic-human", "betrayal"],
    "the-preserving-machine-and-other-stories": ["reality-breakdown", "robots", "illusionary-realities", "authentic-human"],
}


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-") or "unknown"


def clean_title(title: str) -> str:
    title = re.sub(r"\s*\([^)]*\)\s*$", "", title).strip()
    title = re.sub(r"\s*\[[^\]]*\]\s*$", "", title).strip()
    return title


def describe_work_type(work_type: str, category: str | None) -> str:
    if work_type == "primary":
        if category == "letters":
            return "letter collection"
        return "primary text"
    if work_type == "short_stories":
        return "short-story collection"
    return work_type.replace("_", " ")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_text(path: Path, data: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(data, encoding="utf-8")


def compile_patterns(patterns: list[str]) -> list[re.Pattern[str]]:
    return [re.compile(pattern, re.IGNORECASE) for pattern in patterns]


for theme in THEME_DEFINITIONS:
    theme["_compiled_patterns"] = compile_patterns(theme["patterns"])


def ensure_tables(db: sqlite3.Connection) -> None:
    db.executescript(
        """
        CREATE TABLE IF NOT EXISTS works (
            work_id TEXT PRIMARY KEY,
            canonical_title TEXT NOT NULL,
            slug TEXT NOT NULL UNIQUE,
            author TEXT,
            work_type TEXT NOT NULL,
            category TEXT,
            date_start TEXT,
            date_end TEXT,
            date_display TEXT,
            card_summary TEXT,
            page_summary TEXT,
            source_count INTEGER DEFAULT 0,
            page_count INTEGER,
            provenance TEXT,
            notes TEXT
        );

        CREATE TABLE IF NOT EXISTS work_documents (
            work_id TEXT NOT NULL,
            doc_id TEXT NOT NULL,
            role TEXT DEFAULT 'primary',
            PRIMARY KEY (work_id, doc_id)
        );
        """
    )


def build_work_rows(db: sqlite3.Connection) -> list[dict[str, Any]]:
    rows = db.execute(
        """
        SELECT doc_id, title, slug, author, doc_type, category,
               date_display, date_start, page_count, card_summary, page_summary
        FROM documents
        WHERE is_pkd_authored = 1
        ORDER BY COALESCE(date_start, date_display, title)
        """
    ).fetchall()

    grouped: dict[tuple[str, str], list[sqlite3.Row]] = defaultdict(list)
    for doc in rows:
        doc_id, title, slug, author, doc_type, category, date_display, date_start, page_count, card_summary, page_summary = doc
        key = (clean_title(title).lower(), (author or "").strip().lower())
        grouped[key].append(doc)

    works: list[dict[str, Any]] = []
    for (title_key, author_key), docs in grouped.items():
        related_docs = []
        card_summaries = []
        page_summaries = []
        page_counts = []
        date_starts = []
        date_displays = []
        doc_types = defaultdict(int)
        categories = defaultdict(int)
        for doc in docs:
            doc_id, title, slug, author, doc_type, category, date_display, date_start, page_count, card_summary, page_summary = doc
            related_docs.append({
                "doc_id": doc_id,
                "title": title,
                "slug": slug,
                "date_display": date_display,
                "doc_type": doc_type,
            })
            if card_summary:
                card_summaries.append(card_summary)
            if page_summary:
                page_summaries.append(page_summary)
            if page_count:
                page_counts.append(page_count)
            if date_start:
                date_starts.append(date_start)
            if date_display:
                date_displays.append(date_display)
            doc_types[doc_type] += 1
            if category:
                categories[category] += 1

        primary_doc = min(docs, key=lambda d: (d[7] or d[6] or d[1], d[1]))
        doc_id, title, slug, author, doc_type, category, date_display, date_start, page_count, card_summary, page_summary = primary_doc
        primary_card_summary = card_summary or ""
        primary_page_summary = page_summary or card_summary or ""
        work_type = max(doc_types.items(), key=lambda item: (item[1], item[0]))[0]
        if work_type == "archive_pdf":
            work_type = max(categories.items(), key=lambda item: (item[1], item[0]))[0] if categories else "archive_pdf"
        work_kind = describe_work_type(work_type, max(categories.items(), key=lambda item: (item[1], item[0]))[0] if categories else category)
        work_id = f"WORK_{slugify(clean_title(title) or slug or doc_id)}"
        source_mix = ", ".join(
            f"{doc_types[doc_type]} {doc_type.replace('_', ' ')}" for doc_type in sorted(doc_types)
        )
        top_docs = sorted(
            related_docs,
            key=lambda item: (item["date_display"] or "", item["title"]),
        )[:3]
        top_doc_phrase = ", ".join(
            f"{item['title']} ({item['date_display'] or 'undated'})" for item in top_docs
        )
        canonical_title = clean_title(title) or title
        date_display_value = min(date_displays) if date_displays else date_display
        source_count = len(related_docs)
        page_count_value = max(page_counts) if page_counts else (page_count or 0)
        if source_count > 1:
            card_summary = (
                f"Canonical record for {canonical_title}, PKD's {work_kind}. "
                f"This entry consolidates {source_count} linked archive manifestations and summarizes the best surviving record "
                f"for editorial and research use."
            )
            page_summary = (
                f"{canonical_title} is the canonical works-table record for PKD's {work_kind} corpus item. "
                f"The entry consolidates {source_count} linked archive manifestations and keeps them under one bibliographic heading "
                f"so readers can follow edition history, duplication, adaptation, or later republication as a single work record. "
            )
            if source_mix:
                page_summary += f"\n\nThe linked documents span {source_mix}. "
            if top_doc_phrase:
                page_summary += f"The most visible archive manifestations include {top_doc_phrase}. "
            if primary_page_summary:
                page_summary += f"\n\nThe richest source summary notes: {primary_page_summary}"
            page_summary += (
                "\n\nResearchers use this entry to move between the canonical work, the archive documents that preserve it, and any "
                "later commentary or editorial framing attached to those manifestations."
            )
        else:
            card_summary = (
                f"Canonical record for {canonical_title}, PKD's {work_kind}. "
                f"Linked to a single archive manifestation preserved in the archive."
            )
            page_summary = (
                f"{canonical_title} is the canonical works-table record for PKD's {work_kind} corpus item. "
                f"The record links the archive's preserved manifestation of the work to the broader corpus and gives researchers a "
                f"single place to follow its bibliographic and interpretive context."
            )
            if top_doc_phrase:
                page_summary += f"\n\nThe preserved archive item here is {top_doc_phrase}."
            if primary_page_summary:
                page_summary += f"\n\nThe source record itself summarizes the work as follows: {primary_page_summary}"
            page_summary += "\n\nThe entry is most useful when tracing publication context, later commentary, or relationships to other works."
        works.append({
            "work_id": work_id,
            "canonical_title": canonical_title,
            "slug": slugify(canonical_title),
            "author": author,
            "work_type": work_type,
            "category": max(categories.items(), key=lambda item: (item[1], item[0]))[0] if categories else category,
            "date_display": date_display_value,
            "date_start": min(date_starts) if date_starts else date_start,
            "card_summary": card_summary if source_count >= 1 else (max(card_summaries, key=len) if card_summaries else (card_summary or "")),
            "page_summary": page_summary if source_count >= 1 else (max(page_summaries, key=len) if page_summaries else (page_summary or card_summary or "")),
            "page_count": page_count_value,
            "source_count": source_count,
            "related_docs": related_docs,
            "first_doc": {"doc_id": doc_id, "slug": slug, "title": title},
        })
    return works


def infer_themes(work: dict[str, Any]) -> list[str]:
    if work.get("category") not in FICTION_CATEGORIES:
        return []

    slug = work.get("slug", "")
    if slug in WORK_THEME_OVERRIDES:
        return WORK_THEME_OVERRIDES[slug]

    text = " ".join(
        str(part or "")
        for part in (
            work.get("canonical_title"),
            work.get("card_summary"),
            work.get("page_summary"),
        )
    ).lower()

    scores: dict[str, int] = {}
    for theme in THEME_DEFINITIONS:
        score = 0
        for pattern in theme["_compiled_patterns"]:
            if pattern.search(text):
                score += 1
        if score:
            scores[theme["slug"]] = score

    if not scores:
        return ["reality-breakdown"] if work.get("category") == "novels" else ["illusionary-realities"]

    ranked = sorted(scores.items(), key=lambda item: (-item[1], item[0]))
    selected = [slug for slug, _ in ranked[:4]]

    # Keep the theme layer from becoming too narrow.
    if work.get("category") == "novels" and "reality-breakdown" not in selected:
        selected.insert(0, "reality-breakdown")
    if work.get("category") == "short_stories" and "illusionary-realities" not in selected:
        selected.insert(0, "illusionary-realities")

    return list(dict.fromkeys(selected))


def build_theme_index(works: list[dict[str, Any]]) -> dict[str, Any]:
    fiction_works = [work for work in works if work.get("category") in FICTION_CATEGORIES]
    theme_lookup = {theme["slug"]: theme for theme in THEME_DEFINITIONS}
    buckets: dict[str, list[dict[str, Any]]] = {theme["slug"]: [] for theme in THEME_DEFINITIONS}

    for work in fiction_works:
        for theme_slug in work.get("themes", []):
            if theme_slug in buckets:
                buckets[theme_slug].append({
                    "work_id": work["work_id"],
                    "canonical_title": work["canonical_title"],
                    "slug": work["slug"],
                    "category": work["category"],
                    "work_type": work["work_type"],
                    "date_display": work.get("date_display"),
                    "date_start": work.get("date_start"),
                })

    themes = []
    for theme in THEME_DEFINITIONS:
        items = sorted(
            buckets[theme["slug"]],
            key=lambda item: ((item.get("date_start") or "9999"), item.get("canonical_title") or "")
        )
        themes.append({
            "theme_id": f"THEME_{theme['slug'].replace('-', '_')}",
            "slug": theme["slug"],
            "label": theme["label"],
            "description": theme["description"],
            "work_count": len(items),
            "works": items,
            "essay_path": f"themes/essays/{theme['slug']}.md",
        })
    return {
        "theme_count": len(themes),
        "fiction_work_count": len(fiction_works),
        "themes": themes,
    }


THEME_DEVICE_NOTES: dict[str, str] = {
    "androids": "He uses doubles, tests, and counterfeit behavior to make personhood legible as a dramatic problem.",
    "robots": "The plot often turns on automation, domestic machinery, or mechanical imitation, so the device becomes the theme.",
    "drugs": "Chemical distortion works as both subject matter and narrative method, blurring perception and destabilizing the scene.",
    "authentic-human": "Dick stages contrast pairs, ethical tests, and empathic reversals to ask who deserves to count as human.",
    "betrayal": "Double agents, false allies, and reversals of trust keep the plot moving while exposing social fraud.",
    "reality-breakdown": "The narrative repeatedly collapses frames of reference, so the reader experiences the theme as structural instability.",
    "delusions": "Unreliable perception and paranoid interpretation become the engine of scene construction and point of view.",
    "illusionary-realities": "Dick uses nested worlds, simulations, and counterfeit surfaces to turn illusion into the book's governing principle.",
    "memory-identity": "Recalling, forgetting, and misremembering become plot devices that make the self feel provisional.",
    "time": "Temporal slips, regressions, and loops let the plot itself enact the pressure of time on reality.",
    "empire-control": "The machinery of authority is rendered through satire, bureaucracy, and system language that feels larger than any character.",
    "religion-gnosis": "Apocalyptic imagery, revelation, and scriptural echo give the fiction a theological register without abandoning plot.",
    "alien-contact": "Off-world encounter and nonhuman presence are used as estrangement devices that expose human habit from the outside.",
    "suburbia-domesticity": "Dick repeatedly places strange events inside kitchens, homes, and marriages so the domestic scene becomes uncanny.",
}


THEME_OPENERS: dict[str, str] = {
    "androids": "The android theme in Philip K. Dick is rarely only about robots. It is a way of asking where programming ends and moral life begins.",
    "robots": "When Dick writes about robots, he is usually writing about labor, imitation, and the mechanical habits that creep into ordinary life.",
    "drugs": "Drug experience in Dick is never just incidental background. It alters perception, but it also becomes a formal device for making narration unstable.",
    "authentic-human": "The authentic human is one of Dick's central ethical questions: what survives when the world is full of reflex, programming, and counterfeit feeling?",
    "betrayal": "Betrayal in Dick's fiction often starts at the level of plot but ends at the level of ontology, because the trusted world itself may be false.",
    "reality-breakdown": "Reality breakdown is one of Dick's most important inventions as a novelist, because he turns metaphysical doubt into scene-by-scene suspense.",
    "delusions": "Dick uses delusion the way other novelists use weather: it changes the texture of every room, every motive, and every sentence around it.",
    "illusionary-realities": "Illusionary realities are not decorative in Dick; they are the engine that lets him ask whether lived experience is ever fully reliable.",
    "memory-identity": "Memory and identity are fused in Dick's work, and both can fail, fragment, or be rewritten under pressure.",
    "time": "Time in Dick is rarely a neutral background. It bends, loops, slips, and reappears as a problem the plot must solve or endure.",
    "empire-control": "Empire and control are where Dick's fiction becomes political satire, because coercive systems look most powerful when they seem ordinary.",
    "religion-gnosis": "Religion and gnosis in Dick are not ornamentation; they are the mode by which the fiction turns metaphysics into narrative urgency.",
    "alien-contact": "Alien contact in Dick is less about little green men than about estrangement, projection, and the shock of nonhuman intelligence.",
    "suburbia-domesticity": "Dick often begins with houses, marriages, and errands, then reveals that the ordinary domestic frame is the most vulnerable to collapse.",
}


WORK_PLOT_NOTES: dict[str, str] = {
    "solar-lottery": "Dick imagines a political order in which leadership is assigned by chance and protected by an assassin android, so the premise immediately fuses state power with machine violence.",
    "the-man-who-japed": "The novel stages a regime of public virtue and private rebellion, making propaganda and conformity part of the plot's basic pressure system.",
    "the-cosmic-puppets": "A small-town setting opens into a hidden cosmic dualism, so the novel turns ordinary landscape into the stage for metaphysical revelation.",
    "eye-in-the-sky": "An accident in a guided tour leaves the characters trapped in one another's subjective realities, and the novel uses those shifting worlds as both plot engine and satirical device.",
    "time-out-of-joint": "The protagonist's comfortable suburban world begins to misalign with what he remembers, and the novel makes that mismatch the source of its suspense.",
    "the-man-in-the-high-castle": "Dick uses an alternate-history premise, a book-within-the-book, and a metonymic map of empire to make historical uncertainty feel narrated and material at once.",
    "the-game-players-of-titan": "A game structure organizes social life on an alien colony, so the novel turns competition and ritual into a way of reading political power.",
    "clans-of-the-alphane-moon": "Psychiatric clans living on an off-world colony turn pathology into social structure, and Dick uses that satire to ask what counts as normal.",
    "the-penultimate-truth": "The novel splits the world between a subterranean labor force and a surface war staged as propaganda, so reveal and concealment become the governing devices.",
    "the-simulacra": "When political figures become simulacra, the novel makes imitation itself the mechanism by which state power is exposed.",
    "dr-bloodmoney-or-how-we-got-along-after-the-bomb": "Postwar California becomes a field of mutation, barter, and mediated catastrophe, with the novel's episodic structure mirroring social breakdown.",
    "now-wait-for-last-year": "The novel entangles war, drugs, and temporal instability, using a future-present conflict to make chronology itself feel weaponized.",
    "the-crack-in-space": "A breach to another world becomes a literal and social split in the narrative, allowing Dick to move between domestic comedy, labor struggle, and speculative dislocation.",
    "counter-clock-world": "Time runs backward, and the novel converts that impossible premise into a meditation on labor, prophecy, and social order.",
    "the-zap-gun": "The story turns weapons into fashion objects and world politics into performance, so satire becomes the novel's main literary device.",
    "the-ganymede-takeover": "Alien contact and political confusion combine in a plot about occupation, bargaining, and uncertain authority.",
    "the-preserving-machine-and-other-stories": "The title story and its companions repeatedly give objects or systems a life of their own, letting the collection explore what survives form loss.",
    "our-friends-from-frolix-8": "The novel makes political domination and anti-psi resistance feel like competing systems of classification, then lets a counterfeit hero expose the machinery beneath them.",
    "a-maze-of-death": "A colony on a remote world begins to collapse into theological and perceptual uncertainty, and Dick uses the maze itself as a model of unstable reality.",
    "confessions-of-a-crap-artist": "A domestic melodrama about marriage, property, and resentment is turned into a clear-eyed study of ordinary social cruelty.",
    "deus-irae": "A post-apocalyptic quest narrative follows damaged survivors through a world of religion and ruin, making the landscape itself part of the theology.",
    "the-unteleported-man": "Teleportation, colonization, and concealed political systems drive a plot about control, escape, and manufactured reality.",
    "lies-inc": "The novel uses a corporate colony and a fake social order to show how lies can become infrastructure.",
    "radio-free-albemuth": "A split between ordinary life and secret political-theological messages creates a plot in which revelation and surveillance move together.",
    "mary-and-the-giant": "A social novel of work, gender, and desire keeps shifting between romance and social realism, so the ordinary world carries the pressure of imbalance.",
    "nick-and-the-glimmung": "A younger protagonist's encounter with an alien task and a strange ecology lets the novel move between adventure, myth, and moral allegory.",
    "gather-yourselves-together": "Business arrangements and romantic entanglements are staged against a changing foreign setting, letting the novel test loyalty and self-interest.",
    "voices-from-the-street": "The novel treats domestic life and ambition as unstable coordinates, with urban tension and psychic pressure breaking up the social surface.",
    "do-androids-dream-of-electric-sheep": "The bounty-hunter plot unfolds as a test of empathy, while the novel uses fake animals, religious feeling, and damaged domestic spaces to keep the human question unsettled.",
    "the-book-of-philip-k-dick": "This collection organizes early stories around domestic robots, anxious households, and the eerie permeability between the ordinary and the uncanny.",
    "the-collected-stories-of-philip-k-dick-volumes-1-5": "As an omnibus, the collection turns retrospect into structure, arranging many short forms into a single long meditation on identity, power, and unreality.",
    "the-philip-k-dick-reader": "The anthology frames Dick's short fiction as a set of recurring experiments in social instability and ontological doubt.",
    "selected-stories-of-philip-k-dick": "The collection stitches together stories of domestic unease, technological menace, and false reality, so the anthology itself becomes a map of recurring anxieties.",
    "second-variety-and-other-classic-stories": "The title story's self-replicating war machines give the collection a literal image of machine doubling, while the surrounding stories keep returning to the problem of hidden threat.",
    "electric-dreams": "The anthology reintroduces key short fictions through a television-era frame, making adaptation part of the reading experience.",
    "the-minority-report-and-other-classic-stories": "The collection gathers stories about prediction, surveillance, and social systems that claim to know the future before it happens.",
    "the-short-happy-life-of-the-brown-oxford-and-other-classic-stories": "This early-stories volume shows Dick repeatedly making small domestic or humorous premises carry metaphysical weight.",
    "five-great-novels": "The omnibus reads Dick's mid-career fiction as a sequence of escalating tests in reality, identity, and social collapse.",
}


def normalize_spaces(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def first_sentence(text: str, limit: int = 220) -> str:
    text = normalize_spaces((text or "").replace("Full summary pending.", "").replace("\u00e2\u20ac\u201c", " - "))
    if not text:
        return ""
    match = re.search(r"(.+?[.!?])(?:\s|$)", text)
    sentence = match.group(1) if match else text
    sentence = sentence.strip()
    if len(sentence) > limit:
        sentence = sentence[:limit].rsplit(" ", 1)[0].rstrip(",;:") + "..."
    return sentence


def extract_nonboilerplate(text: str) -> str:
    raw = normalize_spaces((text or "").replace("\u00e2\u20ac\u201c", " - "))
    if "The source record itself summarizes the work as follows:" in raw:
        raw = raw.split("The source record itself summarizes the work as follows:", 1)[1].strip()
    if "The richest source summary notes:" in raw:
        raw = raw.split("The richest source summary notes:", 1)[1].strip()
    raw = raw.replace("Full summary pending.", "").strip()
    return raw


def is_boilerplate(summary: str) -> bool:
    lowered = summary.lower().strip()
    return (
        not lowered
        or lowered.startswith("the entry is most useful")
        or lowered.startswith("canonical record")
        or lowered.startswith("the source record itself summarizes")
        or "canonical works-table record" in lowered
    )


def theme_work_paragraph(theme_slug: str, work: dict[str, Any]) -> str:
    summary_source = extract_nonboilerplate(work.get("page_summary") or "")
    summary = first_sentence(summary_source) or first_sentence(work.get("card_summary") or "")
    if is_boilerplate(summary) or "full summary pending" in summary.lower():
        summary = WORK_PLOT_NOTES.get(work["slug"], f"{work['canonical_title']} is one of the corpus items tagged for this theme.")
    device_note = THEME_DEVICE_NOTES.get(theme_slug, "Dick uses recurring motifs, character contrasts, and structural irony to develop the theme.")
    label = "novel" if work.get("category") == "novels" else "story collection"
    title = work["canonical_title"]
    linked_title = f"[{title}](/works/{work['slug']})"
    return (
        f"### {title}\n\n"
        f"{summary} In a {label} like {linked_title}, that premise becomes a thematic pressure point rather than a background idea. "
        f"{device_note} "
        f"The result is a plot that keeps turning the same question over from different angles, so the theme emerges through reversals, doubling, and the small formal choices that make Dick's fiction feel unstable from inside."
    )


def build_theme_essay(theme: dict[str, Any], works: list[dict[str, Any]]) -> str:
    intro = THEME_OPENERS.get(theme["slug"], f"{theme['label']} is one of the recurring interpretive lenses in Dick's fiction.")
    lines = [
        f"# {theme['label']}",
        "",
        intro,
        "",
        theme["description"],
        "",
        "This page reads the fiction corpus through that lens, with each work linked back to its canonical record.",
        "",
        "## Reading the works",
    ]

    fiction_works = [work for work in works if work.get("category") in FICTION_CATEGORIES and theme["slug"] in (work.get("themes") or [])]
    fiction_works.sort(key=lambda work: ((work.get("date_start") or "9999"), work.get("canonical_title") or ""))
    for work in fiction_works:
        lines.extend(["", theme_work_paragraph(theme["slug"], work)])

    lines.extend([
        "",
        "## Synthesis",
        "",
        f"Across these works, {theme['label'].lower()} is not a static topic but a literary machine: Dick uses it to strain plot logic, expose false surfaces, and test whether a character's inner life can survive contact with the system around them. The fiction does not simply mention the theme; it stages it as a recurring formal event.",
    ])
    return "\n".join(lines).strip() + "\n"


def seed_database(db: sqlite3.Connection, works: list[dict[str, Any]]) -> None:
    ensure_tables(db)
    db.execute("DELETE FROM work_documents")
    db.execute("DELETE FROM works")
    for work in works:
        db.execute(
            """
            INSERT INTO works (
                work_id, canonical_title, slug, author, work_type, category,
                date_start, date_display, card_summary, page_summary,
                source_count, page_count, provenance, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                work["work_id"], work["canonical_title"], work["slug"], work["author"],
                work["work_type"], work["category"], work["date_start"], work["date_display"],
                work["card_summary"], work["page_summary"], work["source_count"], work["page_count"],
                "seeded from documents table", None,
            ),
        )
        for rel in work["related_docs"]:
            db.execute(
                "INSERT INTO work_documents (work_id, doc_id, role) VALUES (?, ?, ?)",
                (work["work_id"], rel["doc_id"], "primary"),
            )
    db.commit()


def export_public_json(works: list[dict[str, Any]]) -> None:
    write_json(WORKS_DIR / "index.json", works)
    for work in works:
        detail = dict(work)
        write_json(WORKS_DIR / f"{work['slug']}.json", detail)
    theme_index = build_theme_index(works)
    write_json(THEMES_DIR / "index.json", theme_index)
    essays_dir = THEMES_DIR / "essays"
    for theme in theme_index["themes"]:
        write_text(essays_dir / f"{theme['slug']}.md", build_theme_essay(theme, works))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", type=Path, default=DB_PATH)
    parser.add_argument("--seed-db", action="store_true")
    args = parser.parse_args()

    db = sqlite3.connect(str(args.db))
    db.row_factory = sqlite3.Row
    works = build_work_rows(db)
    for work in works:
        work["themes"] = infer_themes(work)
    if args.seed_db:
        seed_database(db, works)
    export_public_json(works)
    db.close()
    print(f"Exported {len(works)} canonical works")


if __name__ == "__main__":
    main()
