#!/usr/bin/env python3
"""
validate.py — the project's SHACL validation, run one pod at a time.

Every pod-databook under example/Pods/ is validated in isolation from every
other pod: no two pods' extracted data ever reach the same `shacl validate`
call. (The shared foundation/application ontologies merged in below are
schema, not another pod's instance data, so merging those in doesn't violate
this.) Isolation is the whole point — every graph re-asserts shared
individuals such as `:Self` under the self-containment convention, so a
global merge would union facts that were never meant to co-exist and
manufacture violations that no real query would ever see (README.md's "Named Graph Scoping
and Graph-Specific Membership" makes the same point about queries).

Each pod gets two passes:

1. **Pod pass** — the pod's whole content at once: every one of its
   embedded graphs' Turtle, plus the `pod:` triples synthesized from its own
   `tpod.*` frontmatter (databook_graphs.process_pod_databook). Validated
   against the four general shapes files — pod-shacl (the pod model
   itself), persona-shacl, organization-shacl, service-shacl. The graph Turtle
   has to be in here, not just the frontmatter triples: pod-shacl's
   :InstancePodShape constrains creator/owner with `sh:class p:Person` and
   :CGraphShape constrains claimant with
   `sh:or ( [sh:class p:Person] [sh:class o:Organization] [sh:class service:Service] )`,
   and those individuals are typed only in the graph Turtle.

2. **Template pass** — each graph that carries a `shape:` value, checked
   on its own against the shape that value names. A graph's `shape:` is
   the *sole* indicator of what to validate it against, and since
   `pod:shape`'s range is `sh:NodeShape` (pod.ttl) the value already
   *names the shape itself* (e.g. `idocshapes:PassportShape`), with no
   label-to-shape resolution step. The only work left is locating which
   physical `*-shacl.ttl` file defines a shape of that name — since
   `pshapes:` shapes are split across two files — done via the SHAPE_TO_FILE
   table below. A graph with no `shape:` value is skipped outright.

The two passes use different base merges. pod-category-templates.ttl is in the
template pass's base but deliberately out of the pod pass's, so pod-shacl
can't fire on the 102 ctpl:*TemplatePod individuals, which are generic
class-level content bound to no real person.

Root-cause scoping fix (template pass): a class-wide shape targeting `persona:Person` directly
— in practice only `ContactInfoShape`, since every other template's
shape targets a narrow, specific document/account class that only the one
real individual per graph is ever typed as — would otherwise fire on *every*
`persona:Person` individual present in a graph's merged test data, including
an incidental one such as the bare `:Self rdf:type ... persona:Person` every
graph re-asserts under the self-containment convention, which is not the
graph's own real subject and may legitimately lack a GivenName.

The graph's own YAML `subject:` isn't a safe stand-in for "the individual
to validate" here either — a member graph's `subject` can legitimately name
a non-`persona:Person` party (e.g. a Kyoto trip's agent member has
`subject: ":Alice_Travel_Agent"`, a `service:PodAgent`, while the real
ContactInfo-conformant content is asserted on `:Self` in that same graph). So whenever the resolved
shape's own declared target is exactly `sh:targetClass persona:Person`,
`scope_shape` (below) instead re-targets it at every *substantive*
`persona:Person` individual actually present in the graph's own extracted
data — one that carries at least one property beyond the bare `rdf:type`
triple the self-containment convention re-asserts — via `sh:targetNode`,
excluding any bare, data-free mention. Every *other* template's shape keeps
its own original targeting untouched — a narrow document/account class has no
such incidental-mention risk, so rewriting those would misfire, not fix
anything (e.g. `identitydocuments:Passport` is asserted on a reified
`:Alice_US_Passport` individual, never on the graph's own `subject`, `:Self`).
In every case, every *other* root shape co-located in the same physical
shapes file is also stripped of its own targeting for that one validate
call, so it can't spuriously fire on the same merged data either.

Usage:   python3 helpers/validate.py
Exit:    0 if every checked graph conforms, 1 if any graph reports a
         violation or a template's shape name has no entry in SHAPE_TO_FILE.

Requires: pip install pyyaml rdflib   (plus Apache Jena's `riot`/`shacl` on PATH)
"""
import glob
import os
import subprocess
import sys
import tempfile

import yaml
from rdflib import Graph, URIRef
from rdflib.namespace import OWL, RDF, SH

from databook_graphs import (
    as_list,
    extract_graph_block,
    graph_entries,
    iter_graph_blocks,
    process_pod_databook,
    split_frontmatter,
)

# --- shapes-file namespace bases -------------------------------------------
# Each *-shacl.ttl file's own `@prefix :` base — a shape CURIE resolves to
# SHAPE_NS[shapes_file] + local_name.
SHAPE_NS = {
    "shacl/persona-shacl.ttl":            "http://mee.foundation/ontologies/persona/shapes#",
    "shacl/contactinfo-shacl.ttl": "http://mee.foundation/ontologies/persona/shapes#",
    "other/shacl/pets-shacl.ttl":         "http://mee.foundation/ontologies/pets/shapes#",
    "other/shacl/vehicles-shacl.ttl":     "http://mee.foundation/ontologies/vehicles/shapes#",
    "other/shacl/identity-documents-shacl.ttl": "http://mee.foundation/ontologies/identity-documents/shapes#",
    "other/shacl/medical-appointments-shacl.ttl": "http://mee.foundation/ontologies/medical-appointments/shapes#",
    "other/shacl/service-accounts-shacl.ttl": "http://mee.foundation/ontologies/service-accounts/shapes#",
    "other/shacl/banking-shacl.ttl":      "http://mee.foundation/ontologies/banking/shapes#",
    "other/shacl/residences-shacl.ttl":   "http://mee.foundation/ontologies/residences/shapes#",
    "other/shacl/itineraries-shacl.ttl":  "http://mee.foundation/ontologies/itineraries/shapes#",
    "shacl/organization-shacl.ttl":       "http://mee.foundation/ontologies/organization/shapes#",
    "other/shacl/education-shacl.ttl":    "http://mee.foundation/ontologies/education/shapes#",
    "persona-ext/shacl/directory-profile-shacl.ttl": "http://mee.foundation/ontologies/directory-profile/shapes#",
    "pod-category-ext/shacl/boston-hub-society-shacl.ttl": "http://mee.foundation/ontologies/pod-category-ext/boston-hub-society/shapes#",
}

# --- template CURIE prefix -> candidate shapes files ------------------------
# A pod:shape value's own CURIE prefix narrows which physical files could
# define it — pshapes: alone is split across two files, so the shape's own
# local name (below) picks the exact one; every other prefix maps to exactly
# one file.
PREFIX_TO_FILES = {
    "pshapes": ["shacl/persona-shacl.ttl", "shacl/contactinfo-shacl.ttl"],
    "petshapes": ["other/shacl/pets-shacl.ttl"],
    "vehicleshapes": ["other/shacl/vehicles-shacl.ttl"],
    "idocshapes": ["other/shacl/identity-documents-shacl.ttl"],
    "mashapes": ["other/shacl/medical-appointments-shacl.ttl"],
    "sashapes": ["other/shacl/service-accounts-shacl.ttl"],
    "bankingshapes": ["other/shacl/banking-shacl.ttl"],
    "residenceshapes": ["other/shacl/residences-shacl.ttl"],
    "itineraryshapes": ["other/shacl/itineraries-shacl.ttl"],
    "oshapes": ["shacl/organization-shacl.ttl"],
    "educationshapes": ["other/shacl/education-shacl.ttl"],
    "dpshapes": ["persona-ext/shacl/directory-profile-shacl.ttl"],
    "bhsshapes": ["pod-category-ext/shacl/boston-hub-society-shacl.ttl"],
}

# --- shape local name -> shapes file -----------------------------------------
# pod:shape's range is sh:NodeShape (pod.ttl), so the value already
# *names the shape directly* — no more label-to-shape resolution, and no more
# named exceptions (there's no label/target mismatch left to except). This
# table exists purely to locate which physical *-shacl.ttl file defines a
# given shape local name. Add a new row here whenever a new shape is
# introduced.
SHAPE_TO_FILE = {
    "BirthCertificateShape": "other/shacl/identity-documents-shacl.ttl",
    "DriversLicenseShape":   "other/shacl/identity-documents-shacl.ttl",
    "PassportShape":         "other/shacl/identity-documents-shacl.ttl",
    "MedicalAppointmentRecordShape": "other/shacl/medical-appointments-shacl.ttl",
    "ServiceAccountShape":           "other/shacl/service-accounts-shacl.ttl",
    "ResidenceShape":                "other/shacl/residences-shacl.ttl",
    "ItineraryShape":                "other/shacl/itineraries-shacl.ttl",
    "PrimaryCarePhysicianShape":     "shacl/persona-shacl.ttl",
    "CheckingAccountShape":          "other/shacl/banking-shacl.ttl",
    "DebitCardShape":                "other/shacl/banking-shacl.ttl",
    "SSNShape":                      "shacl/persona-shacl.ttl",
    "HealthWellnessShape":           "shacl/persona-shacl.ttl",
    "ContactInfoShape":      "shacl/contactinfo-shacl.ttl",
    "PetShape":                      "other/shacl/pets-shacl.ttl",
    "PetMedicationRecordShape":      "other/shacl/pets-shacl.ttl",
    "PetsCareAndFeedingShape":       "other/shacl/pets-shacl.ttl",
    "VehicleShape":                  "other/shacl/vehicles-shacl.ttl",
    "OrganizationShape":             "shacl/organization-shacl.ttl",
    "EducationRecordShape":          "other/shacl/education-shacl.ttl",
    "DirectoryProfileShape":         "persona-ext/shacl/directory-profile-shacl.ttl",
    "MemberShape":                   "pod-category-ext/shacl/boston-hub-society-shacl.ttl",
}


def resolve_shape_file(template):
    """Resolve a pod:shape value (a shape CURIE, e.g.
    'idocshapes:PassportShape') to (shapes_file, shape_local_name).
    Returns None if the prefix is unrecognized or the local name has no
    SHAPE_TO_FILE entry."""
    if ":" not in template:
        return None
    prefix, local_name = template.split(":", 1)
    candidates = PREFIX_TO_FILES.get(prefix)
    if not candidates:
        return None
    shapes_file = SHAPE_TO_FILE.get(local_name)
    if shapes_file not in candidates:
        return None
    return shapes_file, local_name

BASE_ONTOLOGY_FILES = [
    "project_files/bfo-core.ttl",
    "project_files/PersonOntology.ttl",
    "project_files/AddressOntology.ttl",
    "project_files/StagingOntology.ttl",
    "project_files/UnitsOfMeasureOntology.ttl",
    "project_files/InformationEntityOntology.ttl",
    "project_files/dron-upper.ttl",
    "project_files/ncbitaxon-subset.ttl",
    "project_files/vbo-subset.ttl",
    "project_files/wikidata-vehicle-makes-subset.ttl",
    "project_files/wikidata-vehicle-models-subset.ttl",
    "project_files/prov-upper.ttl",
    "persona.ttl", "pod.ttl", "pod-categories.ttl",
    "other/pets.ttl", "other/vehicles.ttl", "other/identity-documents.ttl",
    "other/medical-appointments.ttl", "other/service-accounts.ttl",
    "other/banking.ttl", "other/residences.ttl", "other/itineraries.ttl",
    "other/education.ttl",
    "persona-ext/directory-profile.ttl",
    "organization.ttl", "service.ttl",
] + sorted(glob.glob("pod-category-ext/*.ttl"))

# The template pass additionally merges pod-category-templates.ttl; the pod pass
# deliberately does not, so pod-shacl's :PodShape can't fire on the 102
# ctpl:*TemplatePod individuals — generic class-level content bound to no
# real person, and not what a pod-databook's own validation is about.
# Category extensions (pod-category-ext/) are bundles: each file carries a
# publisher's own skos:ConceptScheme *and* its pod:TemplatePod individuals.
# The scheme half has to reach the pod pass, so that a pod:category value
# naming an extension concept resolves against pod-shacl's sh:class
# skos:Concept / skos:ConceptScheme checks; the template half is harmless
# there, being a single well-formed pod:TemplatePod rather than
# pod-category-templates.ttl's 107.
TEMPLATE_PASS_ONTOLOGY_FILES = BASE_ONTOLOGY_FILES + ["pod-category-templates.ttl"]

# The four general shapes files the pod pass runs, all at once. The
# per-template *-shacl.ttl files are deliberately absent: they target
# document/account classes and are the template pass's business.
POD_SHAPES_FILES = [
    "shacl/pod-shacl.ttl",
    "shacl/persona-shacl.ttl",
    "shacl/organization-shacl.ttl",
    "shacl/service-shacl.ttl",
]

TARGET_PROPS = [SH.targetClass, SH.targetNode, SH.targetObjectsOf, SH.targetSubjectsOf]

# The one class broad enough to risk an incidental same-type individual
# inside a single isolated graph (the self-containment convention's bare
# `:Self rdf:type ... persona:Person`) — see module docstring.
BROAD_PERSON_CLASS = URIRef("http://mee.foundation/ontologies/persona#Person")


def frontmatter(path):
    fm_text, _, body = split_frontmatter(open(path, encoding="utf-8").read())
    return yaml.safe_load(fm_text), body


def build_base(out_path, files):
    """Merge the shared foundation + application ontologies once, up front —
    the result is reused for every pod, so riot runs twice per invocation
    rather than once per pod."""
    subprocess.run(
        ["riot", "--output=turtle", *files],
        check=True, stdout=open(out_path, "w"), stderr=subprocess.DEVNULL,
    )


def build_pod_shapes():
    """Merge the four general shapes files into one, dropping owl:imports so
    nothing tries to resolve an ontology IRI over the network (the same
    removal scope_shape already makes for a single per-template file)."""
    g = Graph()
    for path in POD_SHAPES_FILES:
        g.parse(path, format="turtle")
    g.remove((None, OWL.imports, None))
    fd, out_path = tempfile.mkstemp(suffix=".ttl")
    os.close(fd)
    g.serialize(destination=out_path, format="turtle")
    return out_path


def pod_data(pod_path, fm, body, base_path):
    """Merge one pod's whole content — every embedded graph's Turtle plus
    the pod: triples synthesized from its own frontmatter — onto the base
    ontologies, and return the merged file's path."""
    lines = []
    for _, block in iter_graph_blocks(body):
        lines += block
    triples = []
    process_pod_databook(fm, triples)

    fd, raw_path = tempfile.mkstemp(suffix=".ttl")
    with os.fdopen(fd, "w") as f:
        f.write("\n".join(lines) + "\n" + "\n".join(triples) + "\n")
    out_path = tempfile.mktemp(suffix=".ttl")
    subprocess.run(
        ["riot", "--output=turtle", base_path, raw_path],
        check=True, stdout=open(out_path, "w"), stderr=subprocess.DEVNULL,
    )
    return out_path


def substantive_person_nodes(data_path):
    """Every persona:Person individual in data_path that carries at least
    one property beyond the bare rdf:type assertion the self-containment
    convention re-asserts on every referenced individual — i.e. excludes an
    incidental cross-referenced party (e.g. a bare `:Self`) that has no real
    content of its own in this particular graph."""
    dg = Graph()
    dg.parse(data_path, format="turtle")
    persons = set(dg.subjects(RDF.type, BROAD_PERSON_CLASS))
    return [p for p in persons if any(pred != RDF.type for pred, _ in dg.predicate_objects(p))]


def scope_shape(shapes_file, shape_local_name, data_path):
    """Load shapes_file and deactivate every root shape except the one
    named (strip their sh:targetClass/targetNode/etc., leaving their
    property/constraint triples intact in case the chosen shape reaches
    them as a nested value-shape via sh:node) — so nothing else co-located
    in the same physical file can independently fire against the small
    per-graph test data.

    If the chosen shape's own declared target is exactly
    `sh:targetClass persona:Person` (the one class broad enough to risk an
    incidental same-type individual within a single isolated graph — see
    module docstring), also re-target it at every substantive
    `persona:Person` individual actually found in data_path via
    sh:targetNode. Every other template's shape already targets a narrow,
    specific class with no such risk, so it's left with its own original
    targeting unchanged.

    Returns the scoped graph, serialized to a temp .ttl file path."""
    ns = SHAPE_NS[shapes_file]
    shape_uri = URIRef(ns + shape_local_name)

    g = Graph()
    g.parse(shapes_file, format="turtle")

    roots = {s for tp in TARGET_PROPS for s in g.subjects(tp, None)}
    if shape_uri not in roots:
        raise ValueError(f"{shape_local_name!r} has no target declaration in {shapes_file}")

    for s in roots:
        if s != shape_uri:
            for tp in TARGET_PROPS:
                g.remove((s, tp, None))

    if (shape_uri, SH.targetClass, BROAD_PERSON_CLASS) in g:
        g.remove((shape_uri, SH.targetClass, BROAD_PERSON_CLASS))
        for node in substantive_person_nodes(data_path):
            g.add((shape_uri, SH.targetNode, node))
    g.remove((None, OWL.imports, None))

    fd, path = tempfile.mkstemp(suffix=".ttl")
    os.close(fd)
    g.serialize(destination=path, format="turtle")
    return path


def run_shacl(shapes_path, data_path):
    result = subprocess.run(
        ["shacl", "validate", "--shapes", shapes_path, "--data", data_path, "--text"],
        capture_output=True, text=True,
    )
    text = result.stdout.strip()
    return text == "Conforms", text


def main():
    pod_base_path = tempfile.mktemp(suffix=".ttl")
    build_base(pod_base_path, BASE_ONTOLOGY_FILES)
    template_base_path = tempfile.mktemp(suffix=".ttl")
    build_base(template_base_path, TEMPLATE_PASS_ONTOLOGY_FILES)
    pod_shapes_path = build_pod_shapes()

    pods = checked = skipped = violations = unresolved = 0

    for pod_path in sorted(glob.glob("example/Pods/**/*.databook.md", recursive=True)):
        if "under-development" in pod_path.split(os.sep):
            continue
        fm, body = frontmatter(pod_path)
        if not fm or fm.get("type") != "pod-databook":
            continue
        tpod = fm.get("tpod", {}) or {}

        # --- Pod pass: the pod's whole content against the general shapes.
        data_path = pod_data(pod_path, fm, body, pod_base_path)
        conforms, text = run_shacl(pod_shapes_path, data_path)
        pods += 1
        if conforms:
            print(f"OK       {pod_path} [pod]")
        else:
            print(f"VIOLATION {pod_path} [pod]\n{text}")
            violations += 1

        # --- Template pass: each templated graph against its own shape.
        for entry in graph_entries(tpod):
            if not isinstance(entry, dict):
                continue
            gid = entry["id"]
            gid_local = gid.rsplit("/", 1)[-1]
            templates = as_list(entry.get("shape"))
            if not templates:
                print(f"SKIP     {pod_path} {gid_local} (no shape)")
                skipped += 1
                continue

            lines = extract_graph_block(body, f"{gid}#graph")
            if lines is None:
                print(f"ERROR    {pod_path} {gid_local}: no turtle block found")
                unresolved += 1
                continue

            fd, raw_path = tempfile.mkstemp(suffix=".ttl")
            with os.fdopen(fd, "w") as f:
                f.write("\n".join(lines))
            data_path = tempfile.mktemp(suffix=".ttl")
            subprocess.run(
                ["riot", "--output=turtle", template_base_path, raw_path],
                check=True, stdout=open(data_path, "w"), stderr=subprocess.DEVNULL,
            )

            for template in templates:
                label = f"{pod_path} {gid_local} [{template}]"
                resolved = resolve_shape_file(template)
                if resolved is None:
                    print(f"UNKNOWN  {label}: no SHAPE_TO_FILE entry for this shape")
                    unresolved += 1
                    continue
                shapes_file, shape_local_name = resolved
                shape_path = scope_shape(shapes_file, shape_local_name, data_path)
                conforms, text = run_shacl(shape_path, data_path)
                checked += 1
                if conforms:
                    print(f"OK       {label}")
                else:
                    print(f"VIOLATION {label}\n{text}")
                    violations += 1

    print()
    print(f"Pods: {pods}   Checked: {checked}   Skipped (no shape): {skipped}   "
          f"Violations: {violations}   Unresolved: {unresolved}")
    sys.exit(1 if (violations or unresolved) else 0)


if __name__ == "__main__":
    main()
