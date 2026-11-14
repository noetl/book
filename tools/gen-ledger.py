#!/usr/bin/env python3
"""AP-E (#47): generate Appendix E's ledger from the pages themselves.

For every page in src/SUMMARY.md, read the badge spans at the top of the page
(`<span class="status status-…">…</span>`). A page whose spans include STUB is
not written yet; its other badge is the planned subject badge. Every written
page must have an entry in tools/ledger.json saying what it was verified
against and when it landed; a written page without one fails the run, so the
ledger cannot silently fall behind the book.

The ledger is written between the markers
  <!-- ledger:start --> and <!-- ledger:end -->
in src/appendix-05-status-ledger.md; everything else on that page is
hand-written. `--check` exits non-zero if the committed page differs.
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src")
PAGE = os.path.join(SRC, "appendix-05-status-ledger.md")
START, END = "<!-- ledger:start -->", "<!-- ledger:end -->"
BADGE = re.compile(r'<span class="status status-(real|partial|target|stub)">')


def pages():
    for line in open(os.path.join(SRC, "SUMMARY.md"), encoding="utf-8"):
        m = re.match(r"^(\s*)(?:- )?\[(.+?)\]\((.+?\.md)\)", line)
        if m:
            yield len(m.group(1)) // 4, m.group(2), m.group(3)


def badges(path):
    with open(os.path.join(SRC, path), encoding="utf-8") as f:
        head = "".join(f.readline() for _ in range(6))
    return [b.upper() for b in BADGE.findall(head)]


def build():
    meta = json.load(open(os.path.join(ROOT, "tools", "ledger.json"), encoding="utf-8"))
    rows, missing = [], []
    written = stub = 0
    for depth, title, path in pages():
        b = badges(path)
        is_stub = "STUB" in b
        subject = next((x for x in b if x != "STUB"), "—")
        indent = "&nbsp;&nbsp;&nbsp;&nbsp;" * depth
        if is_stub:
            stub += 1
            rows.append(f"| {indent}{title} | {subject} | not written | | |")
            continue
        written += 1
        m = meta.get(path)
        if not m:
            missing.append(path)
            m = {"verified": "**MISSING: add to tools/ledger.json**", "landed": ""}
        rows.append(f"| {indent}[{title}]({path}) | **{subject}** | written | {m['verified']} | {m['landed']} |")
    if missing:
        sys.stderr.write("written pages with no tools/ledger.json entry:\n  " + "\n  ".join(missing) + "\n")
    out = [START, "",
           f"**{written} pages written, {stub} not yet written** (of {written + stub} in `SUMMARY.md`).",
           "", "| Page | Badge | Status | Verified against | Landed |", "|---|---|---|---|---|"]
    out += rows + ["", END]
    return "\n".join(out), missing


def main():
    block, missing = build()
    text = open(PAGE, encoding="utf-8").read()
    if START not in text or END not in text:
        sys.exit(f"{PAGE}: missing ledger markers")
    new = text[: text.index(START)] + block + text[text.index(END) + len(END):]
    if "--check" in sys.argv:
        if new != text:
            sys.exit("Appendix E ledger is stale: run python3 tools/gen-ledger.py and commit the result.")
    else:
        open(PAGE, "w", encoding="utf-8").write(new)
    if missing:
        sys.exit(1)


if __name__ == "__main__":
    main()
