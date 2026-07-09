#!/usr/bin/env python3
"""Merge subagent biography-enrichment patch files into curated.json.

Reads every *.bio.json in the given dir (each a JSON array of patch objects,
each with an "id" plus enriched fields). Applies by id. VALIDATES every
cross-link against the filesystem and DROPS dead ones (reporting them). Flags
verbatim quotes attributed to secondary sources (which the method forbids).
Idempotent."""
import json, os, sys, glob, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "site", "public", "data")
CURATED = os.path.join(DATA, "biography", "curated.json")

ENRICH_FIELDS = ["event", "narrative", "sources", "lanes", "quotes", "dispute",
                 "links", "confidence", "notes"]
SECONDARY = {"sutin", "arnold", "anne dick", "anne r. dick", "peake"}


def load_valid_slugs():
    dict_slugs = {os.path.basename(f)[:-5] for f in glob.glob(os.path.join(DATA, "dictionary", "terms", "*.json"))}
    exeg_slugs = {os.path.basename(f)[:-5] for f in glob.glob(os.path.join(DATA, "exegesis", "works", "*.json"))} - {"index"}
    theo_slugs = set()
    for f in glob.glob(os.path.join(DATA, "theophanies", "*.json")):
        if "index" in os.path.basename(f):
            continue
        try:
            theo_slugs.add(json.load(open(f, encoding="utf-8")).get("slug"))
        except Exception:
            pass
    try:
        widx = json.load(open(os.path.join(DATA, "works", "index.json"), encoding="utf-8"))
        work_slugs = {w.get("slug") for w in widx if isinstance(w, dict)}
    except Exception:
        work_slugs = set()
    return dict_slugs, exeg_slugs, theo_slugs, work_slugs


def validate_links(links, valid, report, eid):
    dict_slugs, exeg_slugs, theo_slugs, work_slugs = valid
    out = {}
    # people -> /dictionary/<slug> (only dictionary-backed people resolve)
    people = []
    for p in links.get("people", []) or []:
        slug = p.rstrip("/").split("/")[-1]
        if p.startswith("/dictionary/") and slug in dict_slugs:
            people.append(p)
        else:
            report.append(f"    [drop dead people link] {eid}: {p}")
    if people:
        out["people"] = people
    # works -> /works/<slug>
    works = []
    for w in links.get("works", []) or []:
        slug = w.rstrip("/").split("/")[-1]
        if w.startswith("/works/") and slug in work_slugs:
            works.append(w)
        else:
            report.append(f"    [drop dead works link] {eid}: {w}")
    if works:
        out["works"] = works
    # exegesis_work
    ew = links.get("exegesis_work")
    if ew:
        slug = ew.rstrip("/").split("/")[-1]
        if ew.startswith("/exegesis/works/") and slug in exeg_slugs:
            out["exegesis_work"] = ew
        else:
            report.append(f"    [drop dead exegesis link] {eid}: {ew}")
    # theophany
    th = links.get("theophany")
    if th:
        slug = th.rstrip("/").split("/")[-1]
        if th.startswith("/theophanies/") and slug in theo_slugs:
            out["theophany"] = th
        else:
            report.append(f"    [drop dead theophany link] {eid}: {th}")
    return out


def main():
    src = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.environ.get("SCRATCH", ""), "bio")
    files = sorted(glob.glob(os.path.join(src, "*.bio.json")))
    if not files:
        sys.exit(f"No *.bio.json in {src}")
    valid = load_valid_slugs()

    data = json.load(open(CURATED, encoding="utf-8"))
    by_id = {e["id"]: e for e in data}
    report, applied, quote_warnings = [], 0, 0

    for f in files:
        patches = json.load(open(f, encoding="utf-8"))
        report.append(f"  {os.path.basename(f)}: {len(patches)} patches")
        for p in patches:
            eid = p.get("id")
            if eid not in by_id:
                report.append(f"    [!] id not found: {eid}")
                continue
            e = by_id[eid]
            for k in ENRICH_FIELDS:
                if k in p and p[k] not in (None, "", [], {}):
                    e[k] = p[k]
            if isinstance(e.get("links"), dict):
                e["links"] = validate_links(e["links"], valid, report, eid)
                if not e["links"]:
                    del e["links"]
            # flag forbidden verbatim quotes from secondary sources
            for q in e.get("quotes", []) or []:
                src_l = (q.get("source", "") + " " + q.get("speaker", "")).lower()
                if any(s in src_l for s in SECONDARY):
                    quote_warnings += 1
                    report.append(f"    [!] verbatim quote attributed to secondary source in {eid}: {q.get('source')}")
            applied += 1

    json.dump(data, open(CURATED, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print(f"Applied {applied} enrichments to {CURATED}")
    print("\n".join(report))
    enriched_total = sum(1 for e in data if e.get("narrative"))
    print(f"\nTotal enriched entries now: {enriched_total} / {len(data)}")
    if quote_warnings:
        print(f"REVIEW: {quote_warnings} quote(s) attributed to secondary sources — check these.")


if __name__ == "__main__":
    main()
