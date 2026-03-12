"""
Validation and audit report generator.

Produces audit_report.md (human-readable) and audit_report.json (machine-readable)
with counts, anomalies, and integrity checks.
"""

import json
import sqlite3
import sys
from datetime import datetime
from pathlib import Path


CHECKS = [
    # (label, query, severity)  severity: 'info', 'warn', 'error'
    ("Total documents", "SELECT COUNT(*) FROM documents", "info"),
    ("  Exegesis sections", "SELECT COUNT(*) FROM documents WHERE doc_type = 'exegesis_section'", "info"),
    ("  Archive PDFs", "SELECT COUNT(*) FROM documents WHERE doc_type != 'exegesis_section'", "info"),
    ("Total segments", "SELECT COUNT(*) FROM segments", "info"),
    ("  With summaries", "SELECT COUNT(*) FROM segments WHERE concise_summary IS NOT NULL", "info"),
    ("  Without summaries", "SELECT COUNT(*) FROM segments WHERE concise_summary IS NULL", "info"),
    ("Total terms", "SELECT COUNT(*) FROM terms", "info"),
    ("  Accepted", "SELECT COUNT(*) FROM terms WHERE status = 'accepted'", "info"),
    ("  Provisional", "SELECT COUNT(*) FROM terms WHERE status = 'provisional'", "info"),
    ("  Background", "SELECT COUNT(*) FROM terms WHERE status = 'background'", "info"),
    ("  Alias", "SELECT COUNT(*) FROM terms WHERE status = 'alias'", "info"),
    ("  Rejected", "SELECT COUNT(*) FROM terms WHERE status = 'rejected'", "info"),
    ("Term aliases", "SELECT COUNT(*) FROM term_aliases", "info"),
    ("Term-segment links", "SELECT COUNT(*) FROM term_segments", "info"),
    ("  Confidence 1-2 (strong)", "SELECT COUNT(*) FROM term_segments WHERE link_confidence <= 2", "info"),
    ("  Confidence 3 (medium)", "SELECT COUNT(*) FROM term_segments WHERE link_confidence = 3", "info"),
    ("  Confidence 4-5 (weak)", "SELECT COUNT(*) FROM term_segments WHERE link_confidence >= 4", "info"),
    ("Term-term relations", "SELECT COUNT(*) FROM term_terms", "info"),
    ("Evidence packets", "SELECT COUNT(*) FROM evidence_packets", "info"),
    ("Evidence excerpts", "SELECT COUNT(*) FROM evidence_excerpts", "info"),
    ("Timeline events", "SELECT COUNT(*) FROM timeline_events", "info"),
    ("Assets", "SELECT COUNT(*) FROM assets", "info"),
    ("Annotations", "SELECT COUNT(*) FROM annotations", "info"),

    # Anomaly checks
    ("Orphan terms (no evidence or links)", """
        SELECT COUNT(*) FROM terms t
        WHERE NOT EXISTS (SELECT 1 FROM evidence_packets ep WHERE ep.term_id = t.term_id)
        AND NOT EXISTS (SELECT 1 FROM term_segments ts WHERE ts.term_id = t.term_id)
    """, "warn"),
    ("Segments without dates", "SELECT COUNT(*) FROM segments WHERE date_start IS NULL", "warn"),
    ("Documents without dates", "SELECT COUNT(*) FROM documents WHERE date_start IS NULL", "warn"),
    ("Segments orphaned from documents", """
        SELECT COUNT(*) FROM segments s
        WHERE NOT EXISTS (SELECT 1 FROM documents d WHERE d.doc_id = s.doc_id)
    """, "error"),
    ("Evidence packets for non-existent terms", """
        SELECT COUNT(*) FROM evidence_packets ep
        WHERE NOT EXISTS (SELECT 1 FROM terms t WHERE t.term_id = ep.term_id)
    """, "error"),
    ("Archive docs missing summaries", """
        SELECT COUNT(*) FROM documents
        WHERE doc_type != 'exegesis_section'
        AND (page_summary IS NULL OR page_summary = '')
    """, "warn"),
    ("Terms with >5000 mentions", """
        SELECT COUNT(*) FROM terms WHERE mention_count > 5000
    """, "info"),
    ("Duplicate term slugs", """
        SELECT COUNT(*) FROM (
            SELECT slug FROM terms GROUP BY slug HAVING COUNT(*) > 1
        )
    """, "error"),
]


def run(db: sqlite3.Connection, project_dir: Path):
    """Run all audit checks and produce reports."""
    print("Running audit...")

    results = []
    for label, query, severity in CHECKS:
        try:
            value = db.execute(query).fetchone()[0]
            results.append({
                'label': label.strip(),
                'value': value,
                'severity': severity,
            })
            marker = ''
            if severity == 'warn' and value > 0:
                marker = ' [WARN]'
            elif severity == 'error' and value > 0:
                marker = ' [ERROR]'
            print(f"  {label}: {value}{marker}")
        except Exception as e:
            results.append({'label': label.strip(), 'value': str(e), 'severity': 'error'})
            print(f"  {label}: ERROR - {e}")

    # Detailed anomaly lists
    details = {}

    # Top orphan terms
    orphans = db.execute("""
        SELECT canonical_name, mention_count FROM terms t
        WHERE NOT EXISTS (SELECT 1 FROM evidence_packets ep WHERE ep.term_id = t.term_id)
        AND NOT EXISTS (SELECT 1 FROM term_segments ts WHERE ts.term_id = t.term_id)
        ORDER BY mention_count DESC LIMIT 20
    """).fetchall()
    if orphans:
        details['top_orphan_terms'] = [{'name': n, 'mentions': c} for n, c in orphans]

    # High-frequency terms
    high_freq = db.execute("""
        SELECT canonical_name, mention_count FROM terms
        WHERE mention_count > 1000
        ORDER BY mention_count DESC
    """).fetchall()
    if high_freq:
        details['high_frequency_terms'] = [{'name': n, 'mentions': c} for n, c in high_freq]

    # Malformed dates
    bad_dates = db.execute("""
        SELECT seg_id, date_display, date_confidence FROM segments
        WHERE date_confidence = 'inferred' AND date_start IS NULL
        LIMIT 20
    """).fetchall()
    if bad_dates:
        details['segments_with_inferred_null_dates'] = [
            {'seg_id': s, 'display': d, 'confidence': c} for s, d, c in bad_dates
        ]

    # Write JSON report
    report = {
        'generated_at': datetime.now().isoformat(),
        'summary': results,
        'details': details,
    }

    json_path = project_dir / 'audit_report.json'
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    print(f"\n  Wrote {json_path}")

    # Write markdown report
    md_path = project_dir / 'audit_report.md'
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(f"# QueryPat Audit Report\n\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        f.write("## Summary\n\n")
        f.write("| Check | Count | Status |\n")
        f.write("|-------|-------|--------|\n")
        for r in results:
            status = 'OK'
            if r['severity'] == 'warn' and r['value'] > 0:
                status = 'WARN'
            elif r['severity'] == 'error' and r['value'] > 0:
                status = 'ERROR'
            f.write(f"| {r['label']} | {r['value']} | {status} |\n")

        if details.get('high_frequency_terms'):
            f.write("\n## High Frequency Terms\n\n")
            for t in details['high_frequency_terms']:
                f.write(f"- **{t['name']}**: {t['mentions']} mentions\n")

        if details.get('top_orphan_terms'):
            f.write("\n## Top Orphan Terms (no evidence or links)\n\n")
            for t in details['top_orphan_terms']:
                f.write(f"- {t['name']} ({t['mentions']} mentions)\n")

    print(f"  Wrote {md_path}")


if __name__ == '__main__':
    db_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('C:/QueryPat/database/unified.sqlite')
    project_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else Path('C:/QueryPat')
    db = sqlite3.connect(str(db_path))
    run(db, project_dir)
    db.close()
