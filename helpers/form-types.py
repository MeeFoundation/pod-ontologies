#!/usr/bin/env python3
"""Regenerate README.md's Form Shapes table from the ontology.

A form type *is* a SHACL node shape: the Add Tool dialog offers one entry per
shape a tool's graph can be validated against, and the picked shape's IRI is
stamped onto the new graph as its pod:shape value (app-behavior.md's "Adding a
Tool"); README.md's "Form Shapes" section is where the list itself lives. Which shapes those are, and which categories declare one up front via
pod:formShape, are both facts of the .ttl files — so the table's row set, its
shape column and its "Declared by" column are generated here rather than
maintained by hand.

What this script owns, and what it deliberately does not:

  * Owns the ROW SET. The shapes a graph may name are exactly the keys of
    helpers/validate.py's SHAPE_TO_FILE registry — the same registry the
    validator resolves a pod:shape value against — minus any shape that
    appears only as a template's pod:memberShape and never as a
    pod:formShape (bhsshapes:MemberShape is today's only one: it governs a
    category extension's member graphs, not a form). Component shapes that
    validate a node nested inside a form (:BodyWeightShape, :MedicationShape,
    :OdometerReadingShape and the rest) are already outside that registry and
    so never appear here.
  * Owns the SHAPE column (the CURIE) and the DECLARED BY column (every
    category whose pod:TemplatePod names that shape as a pod:formShape, in
    pod-category-templates.ttl or in a pod-category-ext/ bundle).
  * Does NOT own the display name or the description. Those are the app's own
    UI wording, not derivable from a shape's local name, so a surviving row
    keeps the text already in the file and a newly-added row is emitted with a
    TODO for a human (or Claude, via /sync-form-types) to write. --report
    prints the facts to write it from.

Row order is preserved for surviving rows — the table's grouping is editorial —
with new rows appended at the end, so the generated block diffs cleanly.

Usage (from the repo root):
    python3 helpers/form-types.py            # same as --check
    python3 helpers/form-types.py --check    # diff the file against the ontology; exit 1 on drift
    python3 helpers/form-types.py --write    # splice the regenerated table into README.md
    python3 helpers/form-types.py --report   # per-shape facts for writing a description
"""

import argparse
import difflib
import glob
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "helpers"))

import rdflib  # noqa: E402
from rdflib import Namespace  # noqa: E402

from validate import PREFIX_TO_FILES, SHAPE_NS, SHAPE_TO_FILE  # noqa: E402

SH = Namespace("http://www.w3.org/ns/shacl#")
POD = Namespace("http://mee.foundation/ontologies/pod#")

DOC = os.path.join(REPO, "README.md")

# The two shapes files that hold no form shape at all: they constrain the
# pod/graph/tool scaffolding and the service hierarchy themselves, never the
# content a form carries. Every OTHER shape in the corpus must be accounted
# for — either in the registry (a form type) or as a component shape, i.e. one
# whose sh:targetClass some other shape names as a value class — so that a
# newly-added shape nobody registered is reported rather than silently
# missing from the table.
# other/shacl/sources-shacl.ttl holds no form shape either: its shapes are
# companions applied alongside a graph's own form shape, constraining the
# source items and extractions a structured record was derived from.
INFRA_FILES = {"shacl/pod-shacl.ttl", "shacl/service-shacl.ttl",
               "other/shacl/sources-shacl.ttl"}

# The generated block's fences. Everything between them is this script's; the
# prose above and below it is hand-written and never touched.
BEGIN = "<!-- BEGIN GENERATED: form-types (helpers/form-types.py) -->"
END = "<!-- END GENERATED: form-types -->"

HEADER = [
    "| Form type | `pod:shape` value — file | What the form records | Declared by |",
    "|---|---|---|---|",
]

TODO = "{TODO: describe this form — run `python3 helpers/form-types.py --report` for its fields}"


# --- the ontology side -------------------------------------------------------

def template_files():
    """pod-category-templates.ttl plus every category extension bundle — an extension
    carries its own pod:TemplatePod individuals alongside its concept scheme
    (integrity.md's TTL-8)."""
    return [os.path.join(REPO, "pod-category-templates.ttl")] + sorted(
        glob.glob(os.path.join(REPO, "pod-category-ext", "*.ttl"))
    )


def shape_curie(local_name):
    """Registry local name -> the CURIE the docs and the YAML both write."""
    shapes_file = SHAPE_TO_FILE[local_name]
    for prefix, files in PREFIX_TO_FILES.items():
        if shapes_file in files:
            return "%s:%s" % (prefix, local_name)
    raise KeyError("no CURIE prefix maps to %s" % shapes_file)


def shape_pod(curie):
    """Column two: the CURIE a graph's pod:shape carries, plus a link to the
    shapes file that defines it. Both halves are facts of the registry, so the
    link can never drift from the shape it points at."""
    shapes_file = SHAPE_TO_FILE[curie.split(":", 1)[1]]
    return "`%s` — [`%s`](%s)" % (curie, shapes_file, shapes_file)


def shape_iri(local_name):
    return rdflib.URIRef(SHAPE_NS[SHAPE_TO_FILE[local_name]] + local_name)


def template_roles():
    """Read every pod:formShape / pod:memberShape value, and report which
    category concept each came from. Returns (form_roles, member_roles), each
    mapping a shape IRI to the sorted category CURIEs naming it."""
    form_roles, member_roles = {}, {}
    for path in template_files():
        g = rdflib.Graph()
        g.parse(path, format="turtle")
        norm = g.namespace_manager.normalizeUri
        for tc in set(g.subjects(rdflib.RDF.type, POD.TemplatePod)):
            cats = sorted(norm(c) for c in g.objects(tc, POD.category))
            label = ", ".join(cats) if cats else norm(tc)
            for tool in g.objects(tc, POD.declaresTool):
                for shape in g.objects(tool, POD.formShape):
                    form_roles.setdefault(shape, set()).add(label)
            for shape in g.objects(tc, POD.memberShape):
                member_roles.setdefault(shape, set()).add(label)
    return (
        {k: sorted(v) for k, v in form_roles.items()},
        {k: sorted(v) for k, v in member_roles.items()},
    )


def form_type_shapes():
    """The registry's shapes, minus the member-shape-only ones. Returns
    (rows, member_only), rows being [(curie, declared_by_pod)] keyed for
    lookup and member_only the CURIEs the closing note accounts for."""
    form_roles, member_roles = template_roles()
    rows, member_only = {}, []
    for local_name in SHAPE_TO_FILE:
        iri = shape_iri(local_name)
        curie = shape_curie(local_name)
        declared = form_roles.get(iri, [])
        if not declared and iri in member_roles:
            member_only.append(curie)
            continue
        rows[curie] = ", ".join("`%s`" % c for c in declared) if declared else "—"
    return rows, sorted(member_only)


def unclassified_shapes():
    """Every sh:NodeShape in the corpus that is neither a registered form type,
    nor a component shape, nor infrastructure. A non-empty result means a shape
    was added without deciding whether the Add Tool dialog should offer it."""
    files = sorted(glob.glob(os.path.join(REPO, "**", "shacl", "*.ttl"), recursive=True))
    referenced, shapes = set(), []
    for path in files:
        rel = os.path.relpath(path, REPO)
        g = rdflib.Graph()
        g.parse(path, format="turtle")
        referenced.update(g.objects(None, SH["class"]))
        for s in g.subjects(rdflib.RDF.type, SH.NodeShape):
            if isinstance(s, rdflib.URIRef):
                shapes.append((rel, str(s).rsplit("#", 1)[-1], set(g.objects(s, SH.targetClass))))
    out = []
    for rel, local_name, targets in sorted(shapes):
        if rel in INFRA_FILES or local_name in SHAPE_TO_FILE:
            continue
        if targets and targets <= referenced:  # a component of some other shape
            continue
        out.append("%s  (%s)" % (local_name, rel))
    return out


# --- the document side -------------------------------------------------------

def read_doc():
    with open(DOC, encoding="utf-8") as fh:
        return fh.read()


def split_doc(text):
    """(before, block, after) around the generated fences."""
    if BEGIN not in text or END not in text:
        sys.exit(
            "README.md has no generated form-types block. Expected the fences:\n"
            "  %s\n  %s" % (BEGIN, END)
        )
    before, rest = text.split(BEGIN, 1)
    block, after = rest.split(END, 1)
    return before, block.strip("\n"), after


def parse_block(block):
    """Existing rows, in file order: curie -> (display name, description)."""
    existing = []
    for line in block.splitlines():
        if not line.startswith("|") or line.startswith("|---"):
            continue
        pods = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(pods) != 4 or pods[0] == "Form type":
            continue
        m = re.match(r"`([^`]+)`", pods[1])
        if not m:
            continue
        existing.append((m.group(1), pods[0], pods[2]))
    return existing


def build_block(existing, rows):
    """Regenerate the table: surviving rows keep their order and their prose,
    new rows land at the end with a TODO, dropped rows disappear."""
    lines = list(HEADER)
    seen = set()
    for curie, display, description in existing:
        if curie not in rows:
            continue  # shape left the registry, or became member-shape-only
        seen.add(curie)
        lines.append("| %s | %s | %s | %s |" % (display, shape_pod(curie), description, rows[curie]))
    for curie in sorted(rows):
        if curie in seen:
            continue
        local = curie.split(":", 1)[1]
        display = re.sub(r"(?<=[a-z])(?=[A-Z])", " ", local[: -len("Shape")])
        lines.append("| **%s** | %s | %s | %s |" % (display, shape_pod(curie), TODO, rows[curie]))
    return "\n".join(lines)


# --- the per-shape facts a description is written from -----------------------

def property_facts(g, shape):
    """Every sh:property constraint on one shape, as (required, label)."""
    norm = g.namespace_manager.normalizeUri
    facts = []
    for ps in g.objects(shape, SH.property):
        path = next(g.objects(ps, SH.path), None)
        if path is None:
            continue
        bits = []
        cls = next(g.objects(ps, SH["class"]), None)
        qvs = next(g.objects(ps, SH.qualifiedValueShape), None)
        if qvs is not None:
            cls = cls or next(g.objects(qvs, SH["class"]), None)
        if cls is not None:
            bits.append("-> %s" % norm(cls))
        dt = next(g.objects(ps, SH.datatype), None)
        if dt is not None:
            bits.append(norm(dt))
        low = next(g.objects(ps, SH.minCount), None) or next(
            g.objects(ps, SH.qualifiedMinCount), None
        )
        high = next(g.objects(ps, SH.maxCount), None) or next(
            g.objects(ps, SH.qualifiedMaxCount), None
        )
        required = low is not None and int(low) >= 1
        bits.append("%s..%s" % (int(low) if low is not None else 0,
                                int(high) if high is not None else "N"))
        if next(g.objects(ps, SH["in"]), None) is not None:
            bits.append("sh:in list")
        msg = next(g.objects(ps, SH.message), None)
        if msg is not None:
            bits.append('"%s"' % msg)
        facts.append((required, "%s  %s" % (norm(path), "  ".join(bits))))
    return facts


def report(rows, member_only):
    form_roles, member_roles = template_roles()
    by_file = {}
    for local_name, path in SHAPE_TO_FILE.items():
        by_file.setdefault(path, []).append(local_name)
    for path in sorted(by_file):
        g = rdflib.Graph()
        g.parse(os.path.join(REPO, path), format="turtle")
        norm = g.namespace_manager.normalizeUri
        for local_name in sorted(by_file[path]):
            curie = shape_curie(local_name)
            iri = shape_iri(local_name)
            role = "form type" if curie in rows else "member shape only (not offered)"
            print("%s  [%s]  — %s" % (curie, path, role))
            targets = sorted(norm(t) for t in g.objects(iri, SH.targetClass))
            if targets:
                print("    targets: %s" % ", ".join(targets))
            msg = next(g.objects(iri, SH.message), None)
            if msg:
                print("    message: %s" % msg)
            declared = form_roles.get(iri, [])
            member = member_roles.get(iri, [])
            print("    declared as formShape by: %s" % (", ".join(declared) or "—"))
            if member:
                print("    named as memberShape by: %d template(s)" % len(member))
            if next(g.objects(iri, SH.xone), None) or next(g.objects(iri, SH["or"]), None):
                print("    NOTE: carries an sh:xone/sh:or alternative — read the file for it")
            facts = property_facts(g, iri)
            for required, label in sorted(facts, key=lambda f: (not f[0], f[1])):
                print("    %s %s" % ("REQ " if required else "opt ", label))
            print()


# --- entry point -------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true", help="diff the file against the ontology (default)")
    ap.add_argument("--write", action="store_true", help="splice the regenerated table into README.md")
    ap.add_argument("--report", action="store_true", help="print the per-shape facts a description is written from")
    args = ap.parse_args()

    rows, member_only = form_type_shapes()

    if args.report:
        report(rows, member_only)
        print("member-shape-only, excluded from the table: %s" %
              (", ".join(member_only) or "none"))
        return 0

    text = read_doc()
    before, block, after = split_doc(text)
    existing = parse_block(block)
    regenerated = build_block(existing, rows)

    if args.write:
        if regenerated == block:
            print("Form Shapes table already matches the ontology — nothing written.")
            return 0
        with open(DOC, "w", encoding="utf-8") as fh:
            fh.write(before + BEGIN + "\n" + regenerated + "\n" + END + after)
        print("Rewrote README.md's Form Shapes table (%d rows)." % len(rows))
        if TODO in regenerated:
            print("NOTE: a new row carries a TODO description — write it before committing.")
        return 0

    stray = unclassified_shapes()
    if stray:
        print("Shapes that are neither a registered form type nor a component of one:")
        for s in stray:
            print("  %s" % s)
        print("\nDecide what each is. A form a user can add: register it in "
              "helpers/validate.py's SHAPE_TO_FILE (and SHAPE_NS/PREFIX_TO_FILES "
              "if its file is new), then rerun. Something else: say so here, in "
              "INFRA_FILES or by the component rule above.\n")

    if regenerated == block:
        if stray:
            return 1
        print("Form Shapes table matches the ontology (%d form types; member-shape-only: %s)."
              % (len(rows), ", ".join(member_only) or "none"))
        return 0

    print("Form Shapes table has drifted from the ontology:\n")
    for line in difflib.unified_diff(
        block.splitlines(), regenerated.splitlines(),
        fromfile="README.md", tofile="generated", lineterm="",
    ):
        print(line)
    print("\nRun `python3 helpers/form-types.py --write` to regenerate it.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
