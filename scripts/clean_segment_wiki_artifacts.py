#!/usr/bin/env python3
"""Strip ZebraPedia wiki transcription artifacts from the DISPLAYED text of
segment evidence_excerpts (and concise_summary): "Last edit over N years ago by
X", "Needs Review", stray "Indexed" status tokens and their adjacent bare
page-number lines. Only touches parseable files; the 37 with unescaped-quote
JSON errors are handled separately. Idempotent."""
import json, glob, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SEG = os.path.join(ROOT, "site", "public", "data", "segments")

# wiki footer/header block: optional leading blank lines, the edit-metadata /
# review / indexed tokens, and bare page-number lines that surround them.
BLOCK = re.compile(
    r"\s*(?:\n|^)\s*Last edit over .+? ago by \S+.*?(?=\n\n|\Z)", re.S)
TOKENS = re.compile(r"\b(?:Needs Review|Indexed)\b")
PAGENUM = re.compile(r"(?:\n|^)\s*\d{1,4}\s*(?=\n|$)")   # bare number-only lines


def clean(text):
    if not text:
        return text
    text = BLOCK.sub("", text)
    text = TOKENS.sub("", text)
    text = PAGENUM.sub("\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]{2,}", " ", text)
    return text.strip()


def main():
    files = glob.glob(os.path.join(SEG, "*.json"))
    parsed = touched = fields = skipped = 0
    for f in files:
        try:
            d = json.load(open(f, encoding="utf-8"))
        except Exception:
            skipped += 1
            continue
        parsed += 1
        if not isinstance(d, dict):
            continue
        ch = False
        for ev in d.get("evidence_excerpts", []) or []:
            if isinstance(ev, dict) and isinstance(ev.get("text"), str) and \
               re.search(r"Last edit over|Needs Review|Indexed", ev["text"]):
                nv = clean(ev["text"])
                if nv != ev["text"]:
                    ev["text"] = nv; fields += 1; ch = True
        cs = d.get("concise_summary")
        if isinstance(cs, str) and re.search(r"Last edit over|Needs Review|Indexed", cs):
            nv = clean(cs)
            if nv != cs:
                d["concise_summary"] = nv; fields += 1; ch = True
        if ch:
            json.dump(d, open(f, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
            touched += 1
    print(f"parsed {parsed} / {len(files)} (skipped {skipped} malformed); "
          f"cleaned {fields} fields in {touched} files")


if __name__ == "__main__":
    main()
