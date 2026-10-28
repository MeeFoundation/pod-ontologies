#!/usr/bin/env python3
"""
draw.py  —  Generate a Mermaid (.mmd) and PNG diagram for a single graph's
RDF content, whether that graph is embedded in a pod-databook (post-merge)
or (for legacy/under-development .ttl files) stands alone.

Usage:   python helpers/draw.py <pod_file.databook.md> <graph-id-or-local-name>
         python helpers/draw.py <graph_file.ttl>
Output:  <graph-id-local-name>.mmd and .png, always written to
         example/graphs/images/ regardless of where the source pod file
         lives — graph diagrams keep their pre-merge names/location even
         though the graph's own file no longer exists (must be run from the
         repo root for this relative path to resolve).

Requires: pip install rdflib pyyaml
          mmdc (Mermaid CLI) for PNG generation: npm install -g @mermaid-js/mermaid-cli

Blank-node simplification: a blank node that has a type and a single text value
is collapsed into a direct labeled edge (Subject --"TypeName"--> "value"),
avoiding intermediate nodes for the common designator pattern.
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
import yaml
from hashlib import md5
from pathlib import Path

from rdflib import BNode, Graph, Literal, Namespace, URIRef
from rdflib.namespace import OWL, RDF, RDFS

from databook_graphs import as_list, extract_graph_block, find_graph_entry, graph_entries, split_frontmatter

# ── Namespaces ─────────────────────────────────────────────────────────────────
PERSONA = Namespace("http://mee.foundation/ontologies/persona#")
ORG     = Namespace("http://mee.foundation/ontologies/organization#")
SERVICE = Namespace("http://mee.foundation/ontologies/service#")

DESIGNATED_BY  = URIRef("https://w3id.org/cco-domains/cco/ont00001879")
HAS_TEXT_VALUE = URIRef("https://w3id.org/cco-domains/cco/ont00001765")
PERSON_CLASS   = URIRef("https://w3id.org/cco-domains/cco/ont00001262")

# ── Human-readable labels for well-known IRIs ──────────────────────────────────
LABELS = {
    # persona: classes
    str(PERSONA.Person):                        "Person",
    str(PERSONA.Wallet):                        "Wallet",
    str(PERSONA.CheckingAccount):               "CheckingAccount",
    str(PERSONA.CheckingAccountNumber):         "AccountNumber",
    str(PERSONA.RoutingNumber):                 "RoutingNumber",
    str(PERSONA.PhysicalCard):                  "PhysicalCard",
    str(PERSONA.PhysicalDriversLicense):        "PhysicalDriversLicense",
    str(PERSONA.PhysicalHealthInsuranceCard):   "PhysicalHealthInsuranceCard",
    str(PERSONA.PhysicalPaymentCard):           "PhysicalPaymentCard",
    str(PERSONA.PhysicalSocialSecurityCard):    "PhysicalSocialSecurityCard",
    str(PERSONA.DriversLicenseNumber):          "DriversLicenseNumber",
    str(PERSONA.IssuingJurisdiction):           "IssuingJurisdiction",
    str(PERSONA.PassportNumber):                "PassportNumber",
    str(PERSONA.IssuingCountry):                "IssuingCountry",
    str(PERSONA.PlaceOfBirth):                  "PlaceOfBirth",
    str(PERSONA.GenderMarker):                  "GenderMarker",
    str(PERSONA.IssueDate):                     "IssueDate",
    str(PERSONA.JobTitle):                      "JobTitle",
    str(PERSONA.OrganizationUnit):              "OrganizationUnit",
    str(PERSONA.WebURL):                        "WebURL",
    str(PERSONA.Anniversary):                   "Anniversary",
    str(PERSONA.PersonalInfo):                  "PersonalInfo",
    # persona: properties
    str(DESIGNATED_BY):                         "designated by",
    str(HAS_TEXT_VALUE):                        "has text value",
    str(PERSONA.hasPaymentCard):                "hasPaymentCard",
    str(PERSONA.hasBankAccount):                "hasBankAccount",
    str(PERSONA.accessesBankAccount):           "accessesBankAccount",
    str(PERSONA.hasSocialNetwork):              "hasSocialNetwork",
    str(PERSONA.hasPassword):                   "hasPassword",
    str(PERSONA.hasPhysicalCard):               "hasPhysicalCard",
    str(PERSONA.hasWallet):                     "hasWallet",
    str(PERSONA.hasAnniversary):                "hasAnniversary",
    str(PERSONA.hasPhoto):                      "hasPhoto",
    str(PERSONA.hasImageScan):                  "hasImageScan",
    # cco: entity classes (designators / identifiers)
    "https://w3id.org/cco-domains/cco/ent00000001":         "FullName",
    "https://w3id.org/cco-domains/cco/ent00000002":         "GivenName",
    "https://w3id.org/cco-domains/cco/ent00000003":         "AdditionalName",
    "https://w3id.org/cco-domains/cco/ent00000004":         "FamilyName",
    "https://w3id.org/cco-domains/cco/ent00000006":         "AlternateName",
    "https://w3id.org/cco-domains/cco/ent00000008":         "SSN",
    "https://w3id.org/cco-domains/cco/ent00000010":         "PostalAddress",
    "https://w3id.org/cco-domains/cco/ent00000011":         "StreetAddress",
    "https://w3id.org/cco-domains/cco/ent00000012":         "CityName",
    "https://w3id.org/cco-domains/cco/ent00000013":         "StateName",
    "https://w3id.org/cco-domains/cco/ent00000014":         "CountryName",
    "https://w3id.org/cco-domains/cco/ent00000015":         "PostalCode",
    "https://w3id.org/cco-domains/cco/ent00000016":         "AddressDesignation",
    "https://w3id.org/cco-domains/cco/ent00000023":         "TelephoneNumber",
    "https://w3id.org/cco-domains/cco/ent00000024":         "EmailAddress",
    "https://w3id.org/cco-domains/cco/ent00000033":         "OnlineServiceAccount",
    "https://w3id.org/cco-domains/cco/ent00000047":         "OrganizationName",
    "https://w3id.org/cco-domains/cco/ent00000049":         "PaymentCard",
    "https://w3id.org/cco-domains/cco/ent00000051":         "DebitCard",
    "https://w3id.org/cco-domains/cco/ent00000052":         "CardNumber",
    "https://w3id.org/cco-domains/cco/ent00000053":         "CVV",
    "https://w3id.org/cco-domains/cco/ent00000054":         "ExpirationDate",
    # migrated government-ID + financial designator classes (persona: → cco:)
    "https://w3id.org/cco-domains/cco/ent00000065":         "DriversLicenseNumber",
    "https://w3id.org/cco-domains/cco/ent00000066":         "PassportNumber",
    "https://w3id.org/cco-domains/cco/ent00000067":         "PlaceOfBirth",
    "https://w3id.org/cco-domains/cco/ent00000068":         "IssuingJurisdiction",
    "https://w3id.org/cco-domains/cco/ent00000071":         "AccountNumber",
    "https://w3id.org/cco-domains/cco/ent00000072":         "RoutingNumber",
    # reshaped date predicates + generic date-holder type
    "https://w3id.org/cco-domains/cco/ent00000069":         "IssueDate",
    "https://w3id.org/cco-domains/cco/ent00000070":         "ExpirationDate",
    "https://w3id.org/cco-domains/cco/ent00000073":         "hasPaymentCard",
    "https://w3id.org/cco-domains/cco/ont00001340":         "Date",
    # cco: entity properties
    "https://w3id.org/cco-domains/cco/ent00000034":         "serviceName",
    "https://w3id.org/cco-domains/cco/ent00000035":         "userHandle",
    "https://w3id.org/cco-domains/cco/ent00000036":         "serviceURI",
    "https://w3id.org/cco-domains/cco/ent00000045":         "holdsUserAccount",
    "https://w3id.org/cco-domains/cco/ent00000017":         "hasStartDate",
    "https://w3id.org/cco-domains/cco/ent00000018":         "hasEndDate",
    # cco: ont classes
    "https://w3id.org/cco-domains/cco/ont00001262":         "Person",
    "https://w3id.org/cco-domains/cco/ont00001183":         "SocialNetwork",
    "https://w3id.org/cco-domains/cco/ont00000995":         "MaterialArtifact",
    "https://w3id.org/cco-domains/cco/ont00000020":         "Container",
    "https://w3id.org/cco-domains/cco/ont00000058":         "ScalpHair",
    "https://w3id.org/cco-domains/cco/ont00001022":         "RatioMeasurementICE",
    "https://w3id.org/cco-domains/cco/ont00000253":         "InformationBearingEntity",
    "https://w3id.org/cco-domains/cco/ont00000967":         "Height",
    "https://w3id.org/cco-domains/cco/ont00000026":         "HairColor",
    "https://w3id.org/cco-domains/cco/ont00001677":         "Inch",
    "https://w3id.org/cco-domains/cco/ent00000040":         "BlueEyeColor",
    "https://w3id.org/cco-domains/cco/ont00000984":         "OccupationRole",
    # cco: ont properties
    "https://w3id.org/cco-domains/cco/ont00001780":         "hasMother",
    "https://w3id.org/cco-domains/cco/ont00001786":         "isMotherOf",
    "https://w3id.org/cco-domains/cco/ont00001987":         "hasDaughter",
    "https://w3id.org/cco-domains/cco/ont00001769":         "hasDecimalValue",
    "https://w3id.org/cco-domains/cco/ont00001863":         "usesMeasurementUnit",
    "https://w3id.org/cco-domains/cco/ont00001983":         "isRatioMeasurementOf",
    # BFO
    "http://purl.obolibrary.org/obo/BFO_0000038": "TemporalInterval",
    "http://purl.obolibrary.org/obo/BFO_0000115": "hasMemberPart",
    "http://purl.obolibrary.org/obo/BFO_0000101": "isCarrierOf",
    "http://purl.obolibrary.org/obo/BFO_0000057": "hasParticipant",
    "http://purl.obolibrary.org/obo/BFO_0000153": "occupiesTemporalRegion",
    "http://purl.obolibrary.org/obo/BFO_0000176": "continuantPartOf",
    "http://purl.obolibrary.org/obo/BFO_0000178": "hasContinuantPart",
    "http://purl.obolibrary.org/obo/BFO_0000196": "bearerOf",
    # org
    str(ORG.Organization):                      "Organization",
    # service
    str(SERVICE.Service):                       "Service",
    str(SERVICE.AgentService):                  "AgentService",
    str(SERVICE.ChatGPT):                       "ChatGPT",
    str(SERVICE.PodAgent):                      "PodAgent",
    str(SERVICE.PodGateway):                    "PodGateway",
    str(SERVICE.LLMService):                    "LLMService",
    str(SERVICE.AppleContacts):                 "AppleContacts",
    str(SERVICE.ArcaBackup):                    "ArcaBackup",
    str(SERVICE.ServiceProvider):               "ServiceProvider",
    str(SERVICE.actsFor):                       "actsFor",
    str(SERVICE.providedBy):                    "providedBy",
    str(SERVICE.sponsoredBy):                   "sponsoredBy",
    str(SERVICE.viaGateway):                    "viaGateway",
    str(SERVICE.usesLLM):                       "usesLLM",
    str(SERVICE.hostedBy):                      "hostedBy",
}

# Properties suppressed from edge rendering
SKIP_PROPS = {
    str(RDF.type),
    str(RDFS.label),
    str(RDFS.comment),
    str(OWL.versionInfo),
    str(OWL.imports),
    str(HAS_TEXT_VALUE),  # shown inline via blank-node collapse
}

SKIP_TYPES = {OWL.NamedIndividual, OWL.Thing, OWL.Ontology}
TPOD_NS = "http://www.example.org/tpod#"


def lbl(iri: URIRef) -> str:
    s = str(iri)
    if s in LABELS:
        return LABELS[s]
    return s.split("#")[-1] if "#" in s else s.split("/")[-1]


def nid(key: str) -> str:
    return "n" + md5(key.encode()).hexdigest()[:12]


def esc(s: str) -> str:
    """Escape text for use inside a Mermaid quoted label."""
    return s.replace('"', "#quot;").replace("<", "&lt;").replace(">", "&gt;")


# ── DataBook loading ───────────────────────────────────────────────────────────

def load_databook(path: Path, graph_id: str | None = None):
    """Parse a pod-databook's frontmatter, and (when graph_id is given)
    isolate just that one embedded graph's turtle fence — a merged pod
    file's body may contain several fences, one per tpod.member/tpod.tool graph
    entry, so concatenating all of them (the old, pre-merge behavior) would
    wrongly combine sibling graphs' RDF into one graph."""
    content = path.read_text()
    try:
        fm_text, _, body = split_frontmatter(content)
        frontmatter = yaml.safe_load(fm_text) or {}
    except (ValueError, yaml.YAMLError):
        frontmatter, body = {}, ""

    g = Graph()
    if graph_id is not None:
        turtle_lines = extract_graph_block(body, f"{graph_id}#graph")
        if turtle_lines is None:
            sys.exit(f"No graph found for {graph_id!r} in {path}")
        g.parse(data="\n".join(turtle_lines), format="turtle")

    return g, frontmatter


# ── Mermaid generation ─────────────────────────────────────────────────────────

def style_class(g: Graph, iri: URIRef) -> str:
    types = set(g.objects(iri, RDF.type))
    if PERSONA.Person in types or PERSON_CLASS in types:
        return "person"
    if ORG.Organization in types:
        return "org"
    if types & {SERVICE.Service, SERVICE.AgentService, SERVICE.ChatGPT,
                SERVICE.PodAgent, SERVICE.PodGateway, SERVICE.LLMService,
                SERVICE.AppleContacts, SERVICE.ArcaBackup,
                SERVICE.ServiceProvider}:
        return "service"
    return ""


def type_label(g: Graph, iri: URIRef) -> str:
    """Return the most informative non-generic type label for an individual."""
    for t in g.objects(iri, RDF.type):
        if t in SKIP_TYPES:
            continue
        tl = lbl(t)
        if tl and "/" not in tl and "#" not in tl:
            return tl
    return ""


def expand_bnode(g: Graph, bn: BNode):
    """Return (type_label, text_value_or_None) for a blank node."""
    btype = g.value(bn, RDF.type)
    tv = g.value(bn, HAS_TEXT_VALUE)
    return (lbl(btype) if btype else ""), (str(tv) if tv is not None else None)


def _dyad_label(dyad_iri: str, src_dir: Path | None) -> str:
    """Return display label for a dyad IRI: stem, with graph number appended if findable."""
    stem = dyad_iri.rstrip("/").split("/")[-1]
    if src_dir is not None:
        matches = list(src_dir.glob(f"[0-9][0-9]-{stem}.databook.md"))
        if matches:
            prefix = matches[0].name.split("-")[0]
            return f"{stem} ({int(prefix)})"
    return stem


def _meta_subgraph(tpod: dict, src_dir: Path | None = None) -> list[str]:
    """Build a Mermaid subgraph showing the tpod: YAML properties as a metadata box."""
    props = []
    if name := tpod.get("name"):
        props.append(f"name: {name}")
    if cat := tpod.get("contextCategory"):
        props.append(f"category: {cat.removeprefix('context:')}")
    if claimant := tpod.get("claimant"):
        props.append(f"claimant: {claimant}")
    if graph_subject := tpod.get("subject"):
        props.append(f"subject: {graph_subject}")
    if tool_topic := tpod.get("formTopic"):
        props.append(f"formTopic: {tool_topic}")
    if form_shape := tpod.get("shape"):
        props.append(f"shape: {form_shape}")
    if dyad := tpod.get("dyad"):
        props.append(f"dyad: {_dyad_label(str(dyad), src_dir)}")
    if not props:
        return []
    label = "\\n".join(esc(p) for p in props)
    return [
        '    subgraph ctx["Graph"]',
        "        direction LR",
        f'        ctx_meta["{label}"]:::meta',
        "    end",
    ]


def build_mermaid(g: Graph, frontmatter: dict | None = None, src_dir: Path | None = None) -> str:
    tpod = (frontmatter or {}).get("tpod") or {}
    context_category_label = tpod.get("contextCategory")

    header = []
    if context_category_label:
        header.append(f"%% ContextCategory: {context_category_label}")
    header.append("flowchart TD")
    header.append("    classDef person fill:#fffacd,stroke:#aaa,color:#333")
    header.append("    classDef org    fill:#cce5ff,stroke:#aaa,color:#333")
    header.append("    classDef service fill:#e6e6e6,stroke:#aaa,color:#333")
    header.append("    classDef lit    fill:none,stroke:none,font-style:italic,color:#2a7a2a")
    header.append("    classDef meta   fill:#f5f5ff,stroke:#9999cc,color:#333")

    individuals = {
        s for s in g.subjects(RDF.type, OWL.NamedIndividual)
        if isinstance(s, URIRef)
    }

    declared: set[str] = set()
    node_lines: list[str] = []
    edge_lines: list[str] = []

    def ensure_ind(iri: URIRef) -> str:
        k = nid("ind:" + str(iri))
        if k not in declared:
            local = str(iri).split("#")[-1] if "#" in str(iri) else str(iri).split("/")[-1]
            tl = type_label(g, iri)
            label = esc(f":{local}") + (f"\\n({esc(tl)})" if tl else "")
            cls = style_class(g, iri)
            node_lines.append(f'    {k}["{label}"]' + (f':::{cls}' if cls else ""))
            declared.add(k)
        return k

    def ensure_ext(iri: URIRef) -> str:
        k = nid("ext:" + str(iri))
        if k not in declared:
            local = str(iri).split("#")[-1] if "#" in str(iri) else str(iri).split("/")[-1]
            node_lines.append(f'    {k}[":{esc(local)}"]')
            declared.add(k)
        return k

    def ensure_lit(val: str, key: str) -> str:
        k = nid("lit:" + key)
        if k not in declared:
            node_lines.append(f'    {k}("{esc(val)}"):::lit')
            declared.add(k)
        return k

    for ind in sorted(individuals, key=str):
        src = ensure_ind(ind)

        for pred, obj in g.predicate_objects(ind):
            if str(pred) in SKIP_PROPS:
                continue
            plabel = lbl(pred)

            if isinstance(obj, BNode):
                tl, tv = expand_bnode(g, obj)
                if tv is not None:
                    # Collapse: Subject --"label"--> "value".
                    # designated-by (ont00001879): role is on the bnode TYPE (tl).
                    # A specific designator predicate (e.g. the reshaped date
                    # subproperties has-issue-date / has-expiration-date, whose bnode
                    # is a generic Calendar Date Identifier): role is on the PREDICATE.
                    if pred == DESIGNATED_BY:
                        edge_label = tl if tl else plabel
                    else:
                        edge_label = plabel if plabel else tl
                    tgt = ensure_lit(tv, str(ind) + str(obj))
                    edge_lines.append(f'    {src} -->|"{esc(edge_label)}"| {tgt}')
                else:
                    # Complex blank node: show as a diamond with its type
                    bk = nid("bn:" + str(obj))
                    if bk not in declared:
                        blabel = tl if tl else "_"
                        node_lines.append(f'    {bk}{{"{esc(blabel)}"}}')
                        declared.add(bk)
                    edge_lines.append(f'    {src} -->|"{esc(plabel)}"| {bk}')
                    for bp, bo in g.predicate_objects(obj):
                        if str(bp) in SKIP_PROPS or bp == RDF.type:
                            continue
                        bpl = lbl(bp)
                        if isinstance(bo, Literal):
                            tgt = ensure_lit(str(bo), str(obj) + str(bp) + str(bo))
                            edge_lines.append(f'    {bk} -->|"{esc(bpl)}"| {tgt}')
                        elif isinstance(bo, URIRef) and bo in individuals:
                            edge_lines.append(f'    {bk} -->|"{esc(bpl)}"| {ensure_ind(bo)}')
                        elif isinstance(bo, BNode):
                            ntl, ntv = expand_bnode(g, bo)
                            if ntv is not None:
                                edge_label = ntl if ntl else bpl
                                tgt = ensure_lit(ntv, str(obj) + str(bo))
                                edge_lines.append(f'    {bk} -->|"{esc(edge_label)}"| {tgt}')
                            else:
                                nbk = nid("bn:" + str(bo))
                                if nbk not in declared:
                                    node_lines.append(f'    {nbk}{{"{esc(ntl or "_")}"}}')
                                    declared.add(nbk)
                                edge_lines.append(f'    {bk} -->|"{esc(bpl)}"| {nbk}')

            elif isinstance(obj, URIRef):
                if obj in individuals:
                    edge_lines.append(f'    {src} -->|"{esc(plabel)}"| {ensure_ind(obj)}')
                elif str(obj).startswith(TPOD_NS):
                    edge_lines.append(f'    {src} -->|"{esc(plabel)}"| {ensure_ext(obj)}')
                else:
                    val = lbl(obj)
                    tgt = ensure_lit(val, str(ind) + str(pred) + str(obj))
                    edge_lines.append(f'    {src} -->|"{esc(plabel)}"| {tgt}')

            elif isinstance(obj, Literal):
                tgt = ensure_lit(str(obj), str(ind) + str(pred) + str(obj))
                edge_lines.append(f'    {src} -->|"{esc(plabel)}"| {tgt}')

    meta_lines = _meta_subgraph(tpod, src_dir)

    parts = header + [""]
    if meta_lines:
        parts += meta_lines + [""]
    parts += node_lines
    if edge_lines:
        parts += [""] + edge_lines
    return "\n".join(parts)


# ── PNG generation ─────────────────────────────────────────────────────────────

_CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/usr/bin/google-chrome",
    "/usr/bin/chromium-browser",
    "/usr/bin/chromium",
]


def _find_chrome() -> str | None:
    for c in _CHROME_CANDIDATES:
        if Path(c).exists():
            return c
    return shutil.which("google-chrome") or shutil.which("chromium")


def generate_png(mmd_path: Path, png_path: Path) -> None:
    mmdc = shutil.which("mmdc")
    if not mmdc:
        print("Warning: mmdc not found; skipping PNG generation")
        return

    cmd = [mmdc, "-i", str(mmd_path), "-o", str(png_path), "-b", "white", "-s", "4"]

    chrome = _find_chrome()
    cfg_path = None
    try:
        if chrome:
            cfg = json.dumps({"executablePath": chrome})
            with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
                f.write(cfg)
                cfg_path = f.name
            cmd += ["--puppeteerConfigFile", cfg_path]

        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Warning: mmdc failed: {result.stderr.strip()}")
        else:
            print(f"Written: {png_path}")
    finally:
        if cfg_path:
            os.unlink(cfg_path)


# ── Entry point ────────────────────────────────────────────────────────────────

def main() -> None:
    if len(sys.argv) < 2:
        sys.exit(
            "Usage: python helpers/draw.py <pod_file.databook.md> <graph-id-or-local-name>\n"
            "       python helpers/draw.py <graph_file.ttl>"
        )
    src = Path(sys.argv[1])
    if not src.exists():
        sys.exit(f"File not found: {src}")

    if src.name.endswith(".databook.md"):
        if len(sys.argv) < 3:
            sys.exit(
                "A pod-databook file requires a 2nd argument: the graph's id "
                "(or just its local name, the string after the final '/')."
            )
        graph_arg = sys.argv[2]
        _, pod_fm = load_databook(src)  # frontmatter only — no graph_id yet
        tpod = pod_fm.get("tpod") or {}
        entries = graph_entries(tpod)
        match = find_graph_entry(entries, graph_arg)
        if not match:
            sys.exit(f"No tpod.member or tpod.tool[].graph entry with id/local-name {graph_arg!r} in {src}")
        graph_id = match["id"]
        stem = graph_id.rsplit("/", 1)[-1]  # unchanged filename-stem convention
        g, _ = load_databook(src, graph_id)
        # :Self's bare rdf:type owl:NamedIndividual/persona:Person declaration
        # is now asserted directly in every graph that references :Self (no
        # more separate example/graphs/self.ttl to merge in) — build_mermaid's
        # `individuals` set (built from an in-graph owl:NamedIndividual typing)
        # picks it up from the graph's own content like any other individual.
        # Use this one graph's own claimant/subject/shape for the "Graph"
        # metadata box — not the owning pod's aggregate tpod.creator
        # (the pod has no aggregate tpod.subject of its own; the subject
        # key sits inside each member entry, and a pod's own subject is
        # derived from its tools/members).
        frontmatter = {"tpod": {
            "claimant": match.get("claimant"),
            "subject": match.get("subject"),
            "formTopic": match.get("formTopic"),
            "shape": match.get("shape"),
        }}
        out_dir = Path("example/graphs/images")  # fixed — graph PNGs never move
    else:
        g = Graph()
        g.parse(str(src), format="turtle")
        frontmatter = {}
        ontology_iri = g.value(predicate=RDF.type, object=OWL.Ontology)
        if ontology_iri:
            ctype = g.value(ontology_iri, PERSONA.contextType)
            if ctype:
                frontmatter = {"tpod": {"contextCategory": lbl(ctype)}}
        stem = src.stem
        # Write to images/ subdirectory if it exists, otherwise alongside the source
        images_dir = src.parent / "images"
        out_dir = images_dir if images_dir.is_dir() else src.parent

    out = out_dir / f"{stem}.mmd"

    out.write_text(build_mermaid(g, frontmatter, src.parent) + "\n")
    print(f"Written: {out}")
    generate_png(out, out.with_suffix(".png"))


if __name__ == "__main__":
    main()
