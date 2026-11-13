#!/usr/bin/env python3
"""
yaml-to-rdf.py  —  Synthesize pod: triples from the `tpod.` YAML
frontmatter of pod-databooks.

Why this exists: Turtle-block extraction only pulls fenced Turtle out of a
DataBook — but pod-databook files carry most of their content as `tpod.`
YAML frontmatter, not Turtle. Without this script, pod:Pod individuals
(and pod:MemberGraph's subject/claimant) never appear in the graph SHACL
validates, so shacl/pod-shacl.ttl's :MemberGraphShape never fires against real
instance data. This script closes that gap by mapping each `tpod.` field to
its corresponding ontology property, matching the mapping tables
documented in pod-databook.md's "The `tpod` Block" section.

There is no category-side synthesis here at all — pod-categories.ttl 1.31.0
deleted podcat:Folder and its subclasses podcat:CategoryDefined/podcat:UserDefined
outright, along with podcat:child/podcat:pod/podcat:category/podcat:catType/podcat:label.
Pods do not nest, so there is no tree position to model. A pod's
classification is its pod:categoryTag values (pod.ttl), zero or more, read
directly from the explicit `tpod.categoryTag` YAML list below — never derived from the filename
or the folder.

Since graph-databooks were merged into their owning pod-databooks (each
graph's Turtle content and Overview now live in that pod file's body; its
`id`/`claimant`/`shape`, plus the `subject` a member entry carries
list calls for, now live directly on that same graph's own
`tpod.member`/`tpod.tool[].graph` entry — see pod-databook.md's "Graph Ids
and Named Graphs" section), there is no separate `example/graphs/*.databook.md`
glob any more: `process_pod_databook` below also emits the same triples per
`member`/`tool[].graph` entry that a standalone graph-databook file's frontmatter
used to supply.

A graph's `claimant` and its about-ness value are typed on its plain
`tpod.member[]`/`tpod.tool[].graph[].id`, not that id + "#graph" — matching pod.ttl's
pod:claimant/pod:subject doc comments, and the IRI
pod:member/pod:formGraph actually reference.

Usage:   python3 helpers/yaml-to-rdf.py [repo-root] > yaml-data.ttl
Output:  Turtle triples on stdout — merge with `riot` alongside data extracted
         via `helpers/extract-all.py` (see example.md's Validation section).

Requires: pip install pyyaml
"""

import os, re, sys, yaml, glob

from databook_graphs import process_pod_databook

def frontmatter(path):
    text = open(path, encoding="utf-8").read()
    m = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    return yaml.safe_load(m.group(1)) if m else None


def main(root):
    triples = []

    for path in sorted(
        glob.glob(os.path.join(root, "example", "Pods", "**", "*.databook.md"), recursive=True)
    ):
        if "under-development" in path.split(os.sep):
            continue
        fm = frontmatter(path)
        if not fm or fm.get("type") != "pod-databook":
            continue
        process_pod_databook(fm, triples)

    print("\n".join(triples))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else ".")
