#!/usr/bin/env python3
"""
extract-all.py — print every embedded graph's fenced turtle block, across
every pod-databook under a root directory, as one merged Turtle stream.

Why this exists: validation never merges the whole tree — `helpers/validate.py`
works one pod at a time on purpose — but a few things legitimately need the
union: integrity.md's TTL-1 ("no orphan Persons"), whose reachability question
only makes sense across every pod at once, and loading the example into a
triplestore for ad-hoc SPARQL. See example.md's "Merged whole-example dump".

Do NOT run the general SHACL shapes against this output: merging every pod
unions facts the self-containment convention deliberately keeps per-graph,
which manufactures violations no real query would ever see.

It shares `databook_graphs.iter_graph_blocks()` with extract-graph.py and
validate.py, so every reader of the fence format uses one implementation.

Files under any directory named `under-development/` are skipped, matching
every integrity check's own scope (CLAUDE.md).

Usage:  python3 helpers/extract-all.py [root]     # root defaults to "example"
Output: the concatenated raw Turtle content of every embedded graph.
"""
import glob
import os
import sys

from databook_graphs import iter_graph_blocks, split_frontmatter


def main():
    root = sys.argv[1] if len(sys.argv) > 1 else "example"
    if len(sys.argv) > 2:
        sys.exit("Usage: helpers/extract-all.py [root]")
    for path in sorted(glob.glob(os.path.join(root, "**", "*.databook.md"), recursive=True)):
        if "under-development" in path.split(os.sep):
            continue
        text = open(path, encoding="utf-8").read()
        try:
            _, _, body = split_frontmatter(text)
        except ValueError:
            body = text
        for _, lines in iter_graph_blocks(body):
            print("\n".join(lines))


if __name__ == "__main__":
    main()
