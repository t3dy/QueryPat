#!/usr/bin/env python3
"""Merge written dictionary definitions into term files.
Reads *.dict.json (arrays of {slug, definition, interpretive_note}); sets those
fields + rebuilds card_description from the definition. Idempotent."""
import json, os, sys, glob, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TERMS = os.path.join(ROOT, "site", "public", "data", "dictionary", "terms")
def preview(defn, limit=200):
    defn=defn.strip()
    if len(defn)<=limit: return defn
    cut=defn[:limit]; m=list(re.finditer(r"[.!?](?:\s|$)",cut))
    if m and m[-1].end()>limit*0.5: return cut[:m[-1].end()].strip()
    sp=cut.rfind(" "); return (cut[:sp] if sp>0 else cut).strip()+"…"
def main():
    src=sys.argv[1] if len(sys.argv)>1 else "."
    files=sorted(glob.glob(os.path.join(src,"*.dict.json")))
    applied=0; miss=[]
    for f in files:
        for p in json.load(open(f,encoding="utf-8")):
            slug=p.get("slug"); t=os.path.join(TERMS,f"{slug}.json")
            if not os.path.exists(t): miss.append(slug); continue
            d=json.load(open(t,encoding="utf-8"))
            if p.get("definition"): d["definition"]=p["definition"].strip(); d["card_description"]=preview(p["definition"])
            if p.get("interpretive_note"): d["interpretive_note"]=p["interpretive_note"].strip()
            json.dump(d,open(t,"w",encoding="utf-8"),indent=2,ensure_ascii=False); applied+=1
    print(f"applied {applied} definitions"+(f"; MISSING {miss}" if miss else ""))
    reindex()
def reindex():
    # ensure written terms are present in dictionary/index.json (in case any were filtered)
    idx_path=os.path.join(ROOT,"site","public","data","dictionary","index.json")
    idx=json.load(open(idx_path,encoding="utf-8")); have={e.get("slug") for e in idx}
    added=0
    for f in glob.glob(os.path.join(TERMS,"*.json")):
        d=json.load(open(f,encoding="utf-8"))
        if d.get("slug") not in have and str(d.get("definition") or "").strip():
            idx.append({"canonical_name":d.get("canonical_name"),"slug":d.get("slug")}); have.add(d.get("slug")); added+=1
    if added: json.dump(idx,open(idx_path,"w",encoding="utf-8"),indent=2,ensure_ascii=False)
    print(f"re-added {added} newly-written terms to index")
if __name__=="__main__": main()
