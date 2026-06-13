"""Generate year-by-recipient correspondence trend events from `letters`.

If PKD wrote at least `min_letters` letters to the same recipient in a given
calendar year, this script synthesizes a biography event summarizing the run of
letters. The result is stored in `biography_events` with a stable
`source_doc_id`, so the Biography page and timeline can show the trend without
duplicating it on repeated runs.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sqlite3
import sys
from collections import Counter, defaultdict
from pathlib import Path


MIN_YEAR = 1928
MAX_YEAR = 1982

THEME_PHRASES = {
    "career": "publishing and career pressures",
    "financial": "money and royalty problems",
    "relationships": "family and relationship strain",
    "religion": "religion and theology",
    "philosophy": "metaphysics and philosophy",
    "visionary": "visions and revelatory experience",
    "sf_community": "the science-fiction community",
    "music": "music",
    "politics": "politics",
    "drugs": "drugs and altered states",
}

KEYWORD_THEME_RULES = {
    "career": ["agent", "agency", "contract", "contracts", "option", "rights", "royalty", "royalties", "screenplay", "publisher", "publishing", "sales", "advance"],
    "financial": ["loan", "borrow", "money", "check", "bank", "bill", "payment", "paid", "cash", "expenses"],
    "relationships": ["wife", "husband", "daughter", "baby", "custody", "divorce", "family", "marriage", "mother", "father"],
    "religion": ["god", "christ", "jesus", "holy spirit", "religion", "theology", "revelation", "valis", "zebra", "theophany", "logos", "parousia", "christian"],
    "philosophy": ["metaphys", "philosoph", "spinoza", "plato", "heraclitus", "monism", "anamnesis", "world order", "hologram", "reality", "universe"],
    "visionary": ["vision", "visionary", "satori", "insight", "experience", "revelation", "theophany"],
    "sf_community": ["writer", "novel", "editor", "thesis", "review", "scholar", "fan", "science fiction", "sf", "lem", "jaynes"],
    "music": ["music", "song", "singing", "opera", "record"],
    "politics": ["politics", "cia", "fbi", "government", "conspiracy"],
    "drugs": ["drug", "drugs", "acid", "lsd", "marijuana", "amphetamine", "speed"],
}

INTELLECTUAL_REFERENCES = [
    ("Stanislaw Lem", ["lem"]),
    ("Julian Jaynes", ["jaynes"]),
    ("Spinoza", ["spinoza"]),
    ("Plato", ["plato"]),
    ("Whitehead", ["whitehead"]),
    ("Heraclitus", ["heraclitus"]),
    ("VALIS", ["valis"]),
    ("Zebra", ["zebra"]),
    ("the Logos", ["logos"]),
    ("the Holy Spirit", ["holy spirit"]),
    ("the Parousia", ["parousia"]),
    ("Christ", ["christ"]),
    ("Jesus", ["jesus"]),
]

WORK_ALLOWLIST = {
    "ubik",
    "valis",
    "the man in the high castle",
    "a scanner darkly",
    "flow my tears, the policeman said",
    "do androids dream of electric sheep",
    "a maze of death",
    "now wait for last year",
    "martian time-slip",
    "the three stigmata of palmer eldritch",
    "the divine invasion",
    "the transmigration of timothy archer",
    "counter-clock world",
    "the crack in space",
    "faith of our fathers",
    "the pre-persons",
}


def normalize_text(text: str | None) -> str:
    return re.sub(r"[^a-z0-9]+", " ", (text or "").lower()).strip()


def compact_spaces(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").strip())


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", (text or "").lower()).strip("-")
    return slug or "unknown"


def fetch_letter_groups(con: sqlite3.Connection, min_letters: int) -> list[dict]:
    cur = con.execute(
        """
        SELECT letter_id, date_start, date_display, recipient_raw, recipient_canonical,
               volume_doc_id, body_md
        FROM letters
        WHERE date_start IS NOT NULL
          AND length(date_start) >= 4
          AND substr(date_start, 1, 4) BETWEEN ? AND ?
          AND recipient_raw IS NOT NULL
          AND trim(recipient_raw) != ''
        ORDER BY date_start, letter_id
        """,
        (str(MIN_YEAR), str(MAX_YEAR)),
    )
    rows = [dict(zip([d[0] for d in cur.description], row)) for row in cur.fetchall()]

    by_year_recipient: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for row in rows:
        year = row["date_start"][:4]
        recipient = compact_spaces(row.get("recipient_canonical") or row.get("recipient_raw") or "")
        if not recipient:
            continue
        by_year_recipient[(year, recipient)].append(row)

    groups = []
    for (year, recipient), letters in sorted(by_year_recipient.items()):
        if len(letters) < min_letters:
            continue
        groups.append({
            "year": year,
            "recipient": recipient,
            "letters": letters,
        })
    return groups


def load_letter_theme_map(con: sqlite3.Connection) -> dict[str, Counter]:
    theme_map: dict[str, Counter] = defaultdict(Counter)
    cur = con.execute(
        """
        SELECT letter_id, themes_json, notable_correspondence
        FROM letter_events_candidate
        """
    )
    for letter_id, themes_json, notable in cur.fetchall():
        try:
            for theme in json.loads(themes_json or "[]"):
                theme_map[letter_id][theme] += 1
        except json.JSONDecodeError:
            pass
        if notable:
            theme_map[letter_id][f"nc:{notable}"] += 1
    return theme_map


def load_work_aliases(con: sqlite3.Connection) -> list[tuple[str, str]]:
    cur = con.execute(
        """
        SELECT canonical_title, slug
        FROM works
        WHERE canonical_title IS NOT NULL
          AND substr(date_start, 1, 4) BETWEEN ? AND ?
        """,
        (str(MIN_YEAR), str(MAX_YEAR)),
    )
    aliases: list[tuple[str, str]] = []
    seen: set[str] = set()
    for title, slug in cur.fetchall():
        for candidate in (
            normalize_text(title),
            normalize_text((slug or "").replace("-", " ")),
        ):
            if not candidate:
                continue
            if candidate in seen:
                continue
            if candidate in WORK_ALLOWLIST or " " in candidate or candidate in {"ubik", "valis"}:
                aliases.append((title, candidate))
                seen.add(candidate)
                break
    aliases.sort(key=lambda item: len(item[1]), reverse=True)
    return aliases


def build_work_clause(letters: list[dict], aliases: list[tuple[str, str]]) -> list[str]:
    counts: Counter[str] = Counter()
    for letter in letters:
        body = normalize_text(letter.get("body_md"))
        for title, alias in aliases:
            if alias and re.search(rf"(?<!\w){re.escape(alias)}(?!\w)", body):
                counts[title] += 1
    hits: list[tuple[int, str]] = [(count, title) for title, count in counts.items() if count >= 2]
    hits.sort(key=lambda item: (-item[0], item[1]))
    out: list[str] = []
    for _, title in hits:
        if title not in out:
            out.append(title)
        if len(out) == 3:
            break
    return out


def build_reference_clause(letters: list[dict]) -> list[str]:
    counts: Counter[str] = Counter()
    for label, aliases in INTELLECTUAL_REFERENCES:
        for letter in letters:
            body = normalize_text(letter.get("body_md"))
            if any(alias and re.search(rf"(?<!\w){re.escape(alias)}(?!\w)", body) for alias in aliases):
                counts[label] += 1
    hits: list[tuple[int, str]] = [(count, label) for label, count in counts.items() if count >= 2]
    hits.sort(key=lambda item: (-item[0], item[1]))
    out: list[str] = []
    for _, label in hits:
        if label not in out:
            out.append(label)
        if len(out) == 3:
            break
    return out


def theme_phrases_for_group(letter_ids: list[str], theme_map: dict[str, Counter]) -> list[str]:
    counts: Counter[str] = Counter()
    for letter_id in letter_ids:
        counts.update(theme_map.get(letter_id, Counter()))
    phrases: list[str] = []
    for theme, _n in counts.most_common():
        if theme.startswith("nc:"):
            continue
        phrase = THEME_PHRASES.get(theme)
        if phrase and phrase not in phrases:
            phrases.append(phrase)
        if len(phrases) == 3:
            break
    return phrases


def keyword_theme_phrases(letters: list[dict]) -> list[str]:
    counts: Counter[str] = Counter()
    for letter in letters:
        body = normalize_text(letter.get("body_md"))
        for theme, aliases in KEYWORD_THEME_RULES.items():
            if any(alias and re.search(rf"(?<!\w){re.escape(alias)}(?!\w)", body) for alias in aliases):
                counts[theme] += 1
    phrases: list[str] = []
    for theme, count in counts.most_common():
        if count < 2:
            continue
        phrase = THEME_PHRASES.get(theme)
        if phrase and phrase not in phrases:
            phrases.append(phrase)
        if len(phrases) == 3:
            break
    return phrases


def format_list(items: list[str]) -> str:
    if not items:
        return ""
    if len(items) == 1:
        return items[0]
    if len(items) == 2:
        return f"{items[0]} and {items[1]}"
    return f"{', '.join(items[:-1])}, and {items[-1]}"


def summarize_group(year: str, recipient: str, letters: list[dict], theme_map: dict[str, Counter], aliases: list[tuple[str, str]]) -> tuple[str, str, list[str]]:
    count = len(letters)
    letter_ids = [letter["letter_id"] for letter in letters]

    work_hits = build_work_clause(letters, aliases)
    ref_hits = build_reference_clause(letters)
    theme_hits = theme_phrases_for_group(letter_ids, theme_map)
    keyword_hits = keyword_theme_phrases(letters)
    combined_theme_hits: list[str] = []
    for phrase in theme_hits + keyword_hits:
        if phrase not in combined_theme_hits:
            combined_theme_hits.append(phrase)

    if combined_theme_hits:
        summary = f"In {year}, PKD wrote {count} letters to {recipient}, turning the correspondence into a sustained discussion of {format_list(combined_theme_hits)}."
    elif ref_hits:
        summary = f"In {year}, PKD wrote {count} letters to {recipient}, turning the correspondence into a sustained discussion of {format_list(ref_hits)}."
    elif work_hits:
        summary = f"In {year}, PKD wrote {count} letters to {recipient}, turning the correspondence into a sustained discussion of {format_list(work_hits)}."
    else:
        summary = f"In {year}, PKD wrote {count} letters to {recipient}, turning the correspondence into a running personal and professional journal."

    first_date = letters[0].get("date_start") or f"{year}-01-01"
    last_date = letters[-1].get("date_start") or f"{year}-12-31"
    representative = [letter_ids[0]]
    if len(letter_ids) > 1:
        representative.append(letter_ids[len(letter_ids) // 2])
    if len(letter_ids) > 2:
        representative.append(letter_ids[-1])
    detail_bits = [f"Synthesized from {count} letters to {recipient} in {year} ({first_date} to {last_date})."]
    if work_hits:
        detail_bits.append(f"Repeated work references: {format_list(work_hits)}.")
    if ref_hits:
        detail_bits.append(f"Repeated intellectual references: {format_list(ref_hits)}.")
    if combined_theme_hits:
        detail_bits.append(f"Dominant themes: {format_list(combined_theme_hits)}.")
    detail_bits.append(f"Representative letters: {', '.join(representative)}.")
    detail = " ".join(detail_bits)
    return summary, detail, letter_ids


def upsert_event(
    con: sqlite3.Connection,
    *,
    source_doc_id: str,
    summary: str,
    detail: str,
    year: str,
    recipient: str,
    letter_ids: list[str],
    letter_count: int,
) -> str:
    now = dt.datetime.now(dt.UTC).isoformat(timespec="seconds")
    source_name = "Selected Letters correspondence trend"
    notes = json.dumps(
        {
            "letter_count": letter_count,
            "year": year,
            "recipient": recipient,
            "letter_ids": letter_ids,
        },
        ensure_ascii=False,
    )
    people = json.dumps([recipient], ensure_ascii=False)
    existing = con.execute(
        "SELECT bio_id FROM biography_events WHERE source_doc_id = ? AND source_type = 'letter'",
        (source_doc_id,),
    ).fetchone()

    update_values = (
        summary,
        detail,
        f"{year}",
        f"{year}",
        f"{year}",
        "approximate",
        "correspondence",
        None,
        "letter",
        source_name,
        "confirmed",
        None,
        None,
        None,
        None,
        None,
        None,
        people,
        notes,
        now,
    )
    insert_values = update_values[:-1] + (source_doc_id, now)

    if existing:
        con.execute(
            """
            UPDATE biography_events SET
                summary = ?,
                detail = ?,
                date_start = ?,
                date_end = ?,
                date_display = ?,
                date_confidence = ?,
                event_type = ?,
                location = ?,
                source_type = ?,
                source_name = ?,
                reliability = ?,
                source_letter_id = ?,
                corroborating_letters = ?,
                evidence_quote = ?,
                interpretation_lane = ?,
                contradicts_event_id = ?,
                themes = ?,
                people_involved = ?,
                notes = ?,
                created_at = ?
            WHERE bio_id = ?
            """,
            update_values + (existing[0],),
        )
        return "updated"

    con.execute(
        """
        INSERT INTO biography_events
            (summary, detail, date_start, date_end, date_display, date_confidence,
             event_type, location, source_type, source_name, reliability,
             source_letter_id, corroborating_letters, evidence_quote,
             interpretation_lane, contradicts_event_id, themes, people_involved,
             notes, source_doc_id, created_at)
        VALUES
            (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        insert_values,
    )
    return "added"


def run(db_path: Path, min_letters: int) -> dict:
    con = sqlite3.connect(db_path)
    theme_map = load_letter_theme_map(con)
    work_aliases = load_work_aliases(con)
    groups = fetch_letter_groups(con, min_letters)

    added = 0
    updated = 0
    skipped = 0
    details: list[dict] = []

    for group in groups:
        year = group["year"]
        recipient = group["recipient"]
        letters = group["letters"]
        summary, detail, letter_ids = summarize_group(year, recipient, letters, theme_map, work_aliases)
        source_doc_id = f"LETTER_TREND_{year}_{slugify(recipient)}"
        action = upsert_event(
            con,
            source_doc_id=source_doc_id,
            summary=summary,
            detail=detail,
            year=year,
            recipient=recipient,
            letter_ids=letter_ids,
            letter_count=len(letters),
        )
        if action == "added":
            added += 1
        elif action == "updated":
            updated += 1
        else:
            skipped += 1
        details.append({
            "year": year,
            "recipient": recipient,
            "count": len(letters),
            "source_doc_id": source_doc_id,
            "action": action,
            "summary": summary,
        })

    con.commit()
    con.close()
    return {
        "groups": len(groups),
        "added": added,
        "updated": updated,
        "skipped": skipped,
        "details": details,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default="C:/QueryPat/database/unified.sqlite")
    ap.add_argument("--min-letters", type=int, default=5)
    args = ap.parse_args()
    result = run(Path(args.db), args.min_letters)
    print(f"[done] {result['added']} added; {result['updated']} updated; {result['skipped']} skipped across {result['groups']} groups")
    for item in result["details"]:
        print(f"  [{item['action']}] {item['year']} / {item['recipient']} ({item['count']} letters) -> {item['source_doc_id']}")
        print(f"    {item['summary']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
