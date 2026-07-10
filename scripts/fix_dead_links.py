#!/usr/bin/env python3
"""Fix dead internal links in essay/theme-essay markdown. Repoint where a valid
target exists; otherwise unlink (keep the link text, drop the dead href).
Idempotent."""
import glob, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "site", "public", "data")

REPOINT = {
    "/essays/memory-identity": "/themes/memory-identity",
    "/essays/reality-breakdown": "/themes/reality-breakdown",
    "/essays/time": "/themes/time",
    "/works/valis": "/works/the-valis-trilogy",
    "/dictionary/authentic-human": "/themes/authentic-human",
    "/dictionary/empathy": "/studies/psychology/empathy",
    "/theophanies/2-3-74": "/theophanies/2-3-74-cluster",
}
UNLINK = {
    "/works/divine-invasion", "/works/second-variety", "/works/the-electric-ant",
    "/works/stigmata", "/works/transmigration", "/works/a-scanner-darkly",
    "/works/flow-my-tears-the-policeman-said", "/works/autofac",
    "/dictionary/caritas", "/dictionary/homophily",
}

files = glob.glob(os.path.join(DATA, "essays", "*.md")) + \
        glob.glob(os.path.join(DATA, "themes", "essays", "*.md"))

repoints = unlinks = 0
for f in files:
    t = open(f, encoding="utf-8").read()
    orig = t
    for dead, good in REPOINT.items():
        # only replace the href inside a markdown link ](dead)
        n = t.count(f"]({dead})")
        if n:
            t = t.replace(f"]({dead})", f"]({good})")
            repoints += n
    for dead in UNLINK:
        # [text](dead) -> text
        pat = re.compile(r"\[([^\]]+)\]\(" + re.escape(dead) + r"\)")
        t, n = pat.subn(r"\1", t)
        unlinks += n
    if t != orig:
        open(f, "w", encoding="utf-8").write(t)
print(f"repointed {repoints} links; unlinked {unlinks} links across {len(files)} files")
