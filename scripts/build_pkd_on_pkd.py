"""Build the PKD on PKD catalog.

This indexes mentions of PKD's novels in PKD-authored primary documents
such as letters, interviews, the Exegesis, speeches, and other writings.
The goal is a browsable catalog of self-commentary with minimal manual work.
"""

from __future__ import annotations

import json
import re
import sqlite3
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "database" / "unified.sqlite"
WORKS_INDEX = ROOT / "site" / "public" / "data" / "works" / "index.json"
OUTPUT_DIR = ROOT / "site" / "public" / "data" / "pkd-on-pkd"

STOPWORDS = {
    "about", "again", "also", "been", "being", "book", "books", "could", "dick",
    "dont", "from", "have", "into", "just", "later", "more", "novel", "novels",
    "other", "page", "pages", "said", "say", "says", "that", "their", "there",
    "these", "this", "those", "through", "title", "titles", "will", "with", "would",
}

SOURCE_LABELS = {
    "exegesis_section": "Exegesis",
    "letter": "Letters",
    "interview": "Interviews",
    "scholarship": "Scholarship",
    "biography": "Biography",
    "fan_publication": "Fan publication",
    "archive_pdf": "Primary text",
    "novel": "Novel",
    "short_story": "Short story",
    "other": "Other writing",
}


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-") or "unknown"


def clean_title(title: str) -> str:
    title = re.sub(r"\s*\([^)]*\)\s*$", "", title).strip()
    title = re.sub(r"\s*\[[^\]]*\]\s*$", "", title).strip()
    return title


def normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def tokenize(text: str) -> list[str]:
    return re.findall(r"[a-z0-9']+", text.lower())


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def source_label(doc_type: str) -> str:
    return SOURCE_LABELS.get(doc_type, doc_type.replace("_", " ").title())


def title_aliases(title: str) -> list[str]:
    cleaned = clean_title(title)
    aliases = {cleaned, title}

    stripped = re.sub(r"[^\w\s]", " ", cleaned)
    stripped = re.sub(r"\s+", " ", stripped).strip()
    if stripped:
        aliases.add(stripped)

    if cleaned.lower().startswith(("the ", "a ", "an ")):
        aliases.add(cleaned.split(" ", 1)[1])
        aliases.add(re.sub(r"^(the|a|an)\s+", "", stripped, flags=re.I))

    manual = {
        "Do Androids Dream of Electric Sheep?": ["Do Androids Dream of Electric Sheep", "Electric Sheep", "Androids", "Sheep"],
        "The Man in the High Castle": ["High Castle", "MITHC"],
        "The Three Stigmata of Palmer Eldritch": ["Palmer Eldritch"],
        "A Scanner Darkly": ["Scanner Darkly"],
        "The Transmigration of Timothy Archer": ["Timothy Archer"],
        "Flow My Tears, the Policeman Said": ["Flow My Tears"],
        "The Divine Invasion": ["Divine Invasion"],
        "Ubik": ["UBIK"],
        "VALIS": ["Valis", "V.A.L.I.S."],
        "Deus Irae": ["DEUS IRAE"],
        "Eye in the Sky": ["Eye in the Sky"],
    }
    for alias in manual.get(cleaned, []):
        aliases.add(alias)

    return sorted({a for a in aliases if a}, key=len, reverse=True)


def make_search_pattern(alias: str) -> re.Pattern[str]:
    return re.compile(rf"(?<![a-z0-9]){re.escape(normalize(alias))}(?![a-z0-9])")


def snippet(text: str, start: int, end: int, window: int = 90) -> str:
    left = max(0, start - window)
    right = min(len(text), end + window)
    return re.sub(r"\s+", " ", text[left:right]).strip()


def build_keyword_phrase(snippets: list[str], aliases: list[str]) -> str:
    alias_words = set()
    for alias in aliases:
        alias_words.update(tokenize(alias))
    counts = Counter()
    for text in snippets:
        for token in tokenize(text):
            if len(token) < 4:
                continue
            if token in STOPWORDS or token in alias_words:
                continue
            counts[token] += 1
    words = [word for word, _ in counts.most_common(4)]
    if not words:
        return ""
    if len(words) == 1:
        return words[0]
    if len(words) == 2:
        return f"{words[0]} and {words[1]}"
    return ", ".join(words[:-1]) + f", and {words[-1]}"


def load_novel_works() -> list[dict[str, Any]]:
    data = load_json(WORKS_INDEX)
    novels = [row for row in data if row.get("category") == "novels"]
    novels.sort(key=lambda row: row.get("canonical_title", ""))
    return novels


def load_source_docs(db: sqlite3.Connection) -> list[dict[str, Any]]:
    rows = db.execute(
        """
        SELECT d.doc_id, d.slug, d.title, d.doc_type, d.category, d.date_display,
               COALESCE(d.card_summary, '') AS card_summary,
               COALESCE(d.page_summary, '') AS page_summary,
               COALESCE(dt.text_content, '') AS text_content
        FROM documents d
        LEFT JOIN document_texts dt ON d.doc_id = dt.doc_id
        WHERE d.is_pkd_authored = 1
          AND d.doc_type NOT IN ('novel', 'short_story')
        ORDER BY COALESCE(d.date_start, d.date_display, d.title)
        """
    ).fetchall()

    docs: list[dict[str, Any]] = []
    for row in rows:
        doc_id, slug, title, doc_type, category, date_display, card_summary, page_summary, text_content = row
        body = "\n".join(part for part in [card_summary, page_summary, text_content] if part)
        if not body.strip():
            continue
        docs.append(
            {
                "doc_id": doc_id,
                "slug": slug,
                "title": title,
                "doc_type": doc_type,
                "category": category,
                "date_display": date_display,
                "body": body,
            }
        )
    return docs


def load_source_segments(db: sqlite3.Connection) -> list[dict[str, Any]]:
    rows = db.execute(
        """
        SELECT s.seg_id, s.doc_id, d.slug, d.title, d.doc_type, d.category, d.date_display,
               COALESCE(s.concise_summary, '') AS concise_summary,
               COALESCE(s.reading_excerpt, '') AS reading_excerpt,
               COALESCE(s.raw_text, '') AS raw_text,
               COALESCE(s.works_referenced, '[]') AS works_referenced
        FROM segments s
        JOIN documents d ON d.doc_id = s.doc_id
        WHERE d.is_pkd_authored = 1
          AND d.doc_type NOT IN ('novel', 'short_story')
        ORDER BY COALESCE(s.date_start, d.date_start, d.date_display, d.title), s.position, s.seg_id
        """
    ).fetchall()

    segments: list[dict[str, Any]] = []
    for row in rows:
        seg_id, doc_id, slug, title, doc_type, category, date_display, concise_summary, reading_excerpt, raw_text, works_referenced = row
        body = "\n".join(part for part in [concise_summary, reading_excerpt, raw_text] if part)
        if not body.strip():
            continue
        try:
            refs = json.loads(works_referenced) if works_referenced else []
        except json.JSONDecodeError:
            refs = []
        segments.append(
            {
                "seg_id": seg_id,
                "doc_id": doc_id,
                "slug": slug,
                "title": title,
                "doc_type": doc_type,
                "category": category,
                "date_display": date_display,
                "body": body,
                "works_referenced": refs,
            }
        )
    return segments


def ensure_tables(db: sqlite3.Connection) -> None:
    db.executescript(
        """
        CREATE TABLE IF NOT EXISTS pkd_on_pkd_works (
            work_id             TEXT PRIMARY KEY,
            canonical_title     TEXT NOT NULL,
            slug                TEXT NOT NULL UNIQUE,
            author              TEXT,
            work_type           TEXT,
            category            TEXT,
            mention_count       INTEGER DEFAULT 0,
            source_doc_count    INTEGER DEFAULT 0,
            source_doc_types    TEXT,
            first_mention_date  TEXT,
            last_mention_date   TEXT,
            card_summary        TEXT,
            page_summary        TEXT,
            provenance          TEXT,
            notes               TEXT,
            created_at          TEXT DEFAULT (datetime('now')),
            updated_at          TEXT DEFAULT (datetime('now')),

            FOREIGN KEY (work_id) REFERENCES works(work_id)
        );

        CREATE TABLE IF NOT EXISTS pkd_on_pkd_mentions (
            mention_id          TEXT PRIMARY KEY,
            work_id             TEXT NOT NULL,
            doc_id              TEXT NOT NULL,
            doc_slug            TEXT,
            doc_title           TEXT NOT NULL,
            doc_type            TEXT,
            date_display        TEXT,
            match_text          TEXT,
            context_snippet     TEXT,
            mention_order       INTEGER,
            created_at          TEXT DEFAULT (datetime('now')),

            FOREIGN KEY (work_id) REFERENCES pkd_on_pkd_works(work_id),
            FOREIGN KEY (doc_id) REFERENCES documents(doc_id)
        );

        CREATE INDEX IF NOT EXISTS idx_pkd_on_pkd_slug ON pkd_on_pkd_works(slug);
        CREATE INDEX IF NOT EXISTS idx_pkd_on_pkd_mentions_count ON pkd_on_pkd_works(mention_count DESC);
        CREATE INDEX IF NOT EXISTS idx_pkd_on_pkd_mentions_work ON pkd_on_pkd_mentions(work_id);
        CREATE INDEX IF NOT EXISTS idx_pkd_on_pkd_mentions_doc ON pkd_on_pkd_mentions(doc_id);
        """
    )


def build_records(works: list[dict[str, Any]], docs: list[dict[str, Any]], segments: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]]]:
    detail_records: dict[str, dict[str, Any]] = {}
    index_records: list[dict[str, Any]] = []

    for work in works:
        aliases = title_aliases(work["canonical_title"])
        work_norm_aliases = [normalize(alias) for alias in aliases if normalize(alias)]
        mention_rows: list[dict[str, Any]] = []
        grouped: dict[str, dict[str, Any]] = {}
        all_snippets: list[str] = []
        source_type_counts: Counter[str] = Counter()
        mention_count = 0
        seen_mentions: set[tuple[str, str, str]] = set()

        for doc in docs:
            body_norm = normalize(doc["body"])
            if not body_norm:
                continue
            seen_spans: set[tuple[int, int]] = set()
            for alias in work_norm_aliases:
                if not alias:
                    continue
                pattern = re.compile(rf"(?<![a-z0-9]){re.escape(alias)}(?![a-z0-9])")
                for match in pattern.finditer(body_norm):
                    span = (match.start(), match.end())
                    if span in seen_spans:
                        continue
                    seen_spans.add(span)
                    mention_count += 1
                    context = snippet(body_norm, match.start(), match.end())
                    mention_key = (doc["doc_id"], normalize(alias), normalize(context))
                    if mention_key in seen_mentions:
                        continue
                    seen_mentions.add(mention_key)
                    mention_id = f"PKDPKD_{slugify(work['slug'])}_{slugify(doc['slug'] or doc['doc_id'])}_{mention_count}"
                    row = {
                        "mention_id": mention_id,
                        "work_id": work["work_id"],
                        "doc_id": doc["doc_id"],
                        "doc_slug": doc["slug"],
                        "doc_title": doc["title"],
                        "doc_type": doc["doc_type"],
                        "date_display": doc["date_display"],
                        "match_text": alias,
                        "context_snippet": context,
                        "mention_order": mention_count,
                    }
                    mention_rows.append(row)
                    all_snippets.append(context)
                    source_type_counts[doc["doc_type"]] += 1
                    bucket = grouped.setdefault(
                        doc["doc_id"],
                        {
                            "doc_id": doc["doc_id"],
                            "doc_slug": doc["slug"],
                            "doc_title": doc["title"],
                            "doc_type": doc["doc_type"],
                            "date_display": doc["date_display"],
                            "mention_count": 0,
                            "excerpts": [],
                        },
                    )
                    bucket["mention_count"] += 1
                    if len(bucket["excerpts"]) < 3:
                        bucket["excerpts"].append(
                            {
                                "match_text": alias,
                                "context_snippet": context,
                                "mention_order": mention_count,
                            }
                        )

        for seg in segments:
            seg_refs = seg.get("works_referenced") or []
            seg_body = normalize(seg["body"])
            if not seg_body:
                continue
            alias_hits = []
            for alias in work_norm_aliases:
                if not alias:
                    continue
                pattern = re.compile(rf"(?<![a-z0-9]){re.escape(alias)}(?![a-z0-9])")
                if pattern.search(seg_body):
                    alias_hits.append(alias)
            ref_hits = [ref for ref in seg_refs if normalize(ref) in work_norm_aliases]
            if not alias_hits and not ref_hits:
                continue

            match_text = ref_hits[0] if ref_hits else alias_hits[0]
            context = seg.get("reading_excerpt") or seg.get("concise_summary") or seg.get("title") or seg["body"]
            mention_key = (seg["doc_id"], normalize(match_text), normalize(context))
            if mention_key in seen_mentions:
                continue
            seen_mentions.add(mention_key)
            mention_count += 1
            mention_id = f"PKDPKD_{slugify(work['slug'])}_{slugify(seg['slug'] or seg['doc_id'])}_{mention_count}"
            row = {
                "mention_id": mention_id,
                "work_id": work["work_id"],
                "doc_id": seg["doc_id"],
                "doc_slug": seg["slug"],
                "doc_title": seg["title"],
                "doc_type": seg["doc_type"],
                "date_display": seg["date_display"],
                "match_text": match_text,
                "context_snippet": context[:240] if context else seg["body"][:240],
                "mention_order": mention_count,
            }
            mention_rows.append(row)
            all_snippets.append(row["context_snippet"])
            source_type_counts[seg["doc_type"]] += 1
            bucket = grouped.setdefault(
                seg["doc_id"],
                {
                    "doc_id": seg["doc_id"],
                    "doc_slug": seg["slug"],
                    "doc_title": seg["title"],
                    "doc_type": seg["doc_type"],
                    "date_display": seg["date_display"],
                    "mention_count": 0,
                    "excerpts": [],
                },
            )
            bucket["mention_count"] += 1
            if len(bucket["excerpts"]) < 3:
                bucket["excerpts"].append(
                    {
                        "match_text": match_text,
                        "context_snippet": row["context_snippet"],
                        "mention_order": mention_count,
                    }
                )

        source_documents = sorted(
            grouped.values(),
            key=lambda item: (-item["mention_count"], item["date_display"] or "", item["doc_title"]),
        )

        top_sources = [
            {
                "doc_id": item["doc_id"],
                "doc_slug": item["doc_slug"],
                "doc_title": item["doc_title"],
                "doc_type": item["doc_type"],
                "date_display": item["date_display"],
                "mention_count": item["mention_count"],
            }
            for item in source_documents[:6]
        ]

        keywords = build_keyword_phrase(all_snippets, aliases)
        source_labels = sorted(
            ((source_label(doc_type), count) for doc_type, count in source_type_counts.items()),
            key=lambda item: (-item[1], item[0]),
        )
        source_phrase = ", ".join(f"{label.lower()} ({count})" for label, count in source_labels[:4]) if source_labels else "PKD-authored writings"
        source_doc_count = len(source_documents)
        title = work["canonical_title"]
        card_summary = (
            f"PKD-on-PKD catalog for {title}: {mention_count} detected title mentions across "
            f"{source_doc_count} PKD-authored writings. The references cluster in {source_phrase}, "
            f"and the detail page shows each source document with its surrounding context."
        )
        page_summary = (
            f"This section gathers PKD's own mentions of {title} across PKD-authored primary writings in the archive. "
            f"The catalog records {mention_count} detected title mentions in {source_doc_count} PKD-authored documents. "
        )
        if source_labels:
            page_summary += "\n\nThe represented source types here include " + ", ".join(
                f"{label.lower()} ({count})" for label, count in source_labels
            ) + ". "
        if top_sources:
            named_sources = ", ".join(
                f"{item['doc_title']} ({item['mention_count']})" for item in top_sources[:3]
            )
            page_summary += f"The heaviest source documents are {named_sources}. "
        if keywords:
            page_summary += f"\n\nNearby language repeatedly turns on {keywords}. "
        page_summary += (
            "\n\nThe mention list is organized by source document so readers can move directly from each remark "
            "to the underlying text."
        )

        index_record = {
            "work_id": work["work_id"],
            "canonical_title": title,
            "slug": work["slug"],
            "author": work.get("author"),
            "work_type": work.get("work_type"),
            "category": work.get("category"),
            "mention_count": mention_count,
            "source_doc_count": source_doc_count,
            "source_doc_types": dict(source_type_counts),
            "first_mention_date": min((item["date_display"] or "" for item in source_documents), default=""),
            "last_mention_date": max((item["date_display"] or "" for item in source_documents), default=""),
            "card_summary": card_summary,
            "page_summary": page_summary,
            "top_sources": top_sources,
        }

        detail_record = dict(index_record)
        detail_record["mentions"] = mention_rows
        detail_record["source_documents"] = source_documents
        detail_record["aliases"] = aliases

        index_records.append(index_record)
        detail_records[work["slug"]] = detail_record

    index_records.sort(key=lambda row: (-row["mention_count"], row["canonical_title"]))
    return index_records, detail_records


def seed_database(db: sqlite3.Connection, records: list[dict[str, Any]], detail_records: dict[str, dict[str, Any]]) -> None:
    ensure_tables(db)
    db.execute("DELETE FROM pkd_on_pkd_mentions")
    db.execute("DELETE FROM pkd_on_pkd_works")
    for row in records:
        db.execute(
            """
            INSERT INTO pkd_on_pkd_works (
                work_id, canonical_title, slug, author, work_type, category,
                mention_count, source_doc_count, source_doc_types,
                first_mention_date, last_mention_date, card_summary, page_summary,
                provenance, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                row["work_id"], row["canonical_title"], row["slug"], row["author"], row["work_type"],
                row["category"], row["mention_count"], row["source_doc_count"], json.dumps(row["source_doc_types"], ensure_ascii=False),
                row["first_mention_date"], row["last_mention_date"], row["card_summary"], row["page_summary"],
                "automatically extracted from PKD-authored primary documents", None,
            ),
        )

    for detail in detail_records.values():
        for mention in detail["mentions"]:
            db.execute(
                """
                INSERT INTO pkd_on_pkd_mentions (
                    mention_id, work_id, doc_id, doc_slug, doc_title, doc_type,
                    date_display, match_text, context_snippet, mention_order
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    mention["mention_id"], mention["work_id"], mention["doc_id"], mention["doc_slug"],
                    mention["doc_title"], mention["doc_type"], mention["date_display"], mention["match_text"],
                    mention["context_snippet"], mention["mention_order"],
                ),
            )
    db.commit()


def export_public_json(records: list[dict[str, Any]], detail_records: dict[str, dict[str, Any]]) -> None:
    write_json(OUTPUT_DIR / "index.json", records)
    for slug, detail in detail_records.items():
        write_json(OUTPUT_DIR / f"{slug}.json", detail)


def run(db: sqlite3.Connection, project_dir: Path | None = None, seed_db: bool = True) -> None:
    del project_dir
    works = load_novel_works()
    docs = load_source_docs(db)
    segments = load_source_segments(db)
    records, detail_records = build_records(works, docs, segments)
    if seed_db:
        seed_database(db, records, detail_records)
    export_public_json(records, detail_records)
    print(f"Built PKD on PKD catalog for {len(records)} novels")


def main() -> None:
    db = sqlite3.connect(str(DB_PATH))
    db.row_factory = sqlite3.Row
    run(db)
    db.close()


if __name__ == "__main__":
    main()
