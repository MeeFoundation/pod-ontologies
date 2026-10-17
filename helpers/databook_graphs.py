#!/usr/bin/env python3
"""
databook_graphs.py — shared helpers for reading pod-databook files: locating
one embedded graph's content inside a (possibly multi-graph) file, and turning
a pod's own frontmatter into `pod:` triples. Used by draw.py,
extract-graph.py, extract-all.py, yaml-to-rdf.py and validate.py.

Since graph-databooks were merged into their owning pod-databooks, a pod
file's body may contain several ```turtle fences — one per embedded graph
(each `tpod.member`/`tpod.tool[].graph` entry in that pod's frontmatter is one such
graph's own metadata dict). Each fence still carries its own
`<!-- databook:graph: {graph_id}#graph -->` marker, computed from the
graph's own `id` per the unchanged `{id}#graph` named-graph convention
(pod-databook.md's "Graph Ids and Named Graphs") — so isolating one graph's fence
only requires knowing that graph's `id`, no new marker scheme.

Also carries `resolve()`/`as_list()` — needed wherever a `tpod.*` YAML value
(a CURIE or a bare `:X` local name) must become the same full IRI — and the
`pod:` triple synthesis (`process_pod_databook()`/`process_embedded_graph()`)
that turns one pod-databook's frontmatter into Turtle. Both `yaml-to-rdf.py`
(whole-tree dump) and `validate.py` (one pod at a time) call that synthesis,
so it lives here rather than in either script; `yaml-to-rdf.py`'s hyphenated
filename is not an importable module name in any case.
"""
import re

FRONTMATTER_RE = re.compile(r"^(---\n)(.*?\n)(---\n?)(.*)$", re.DOTALL)

TPOD_NS = "http://www.example.org/tpod#"
POD = "http://mee.foundation/ontologies/pod#"

PREFIXES = {
    "podcat": "http://mee.foundation/ontologies/pod-categories#",
    "pod": "http://mee.foundation/ontologies/pod#",
    "persona": "http://mee.foundation/ontologies/persona#",
    "pets": "http://mee.foundation/ontologies/pets#",
    "vehicles": "http://mee.foundation/ontologies/vehicles#",
    # A category extension's own namespace (pod-category-ext/). A tpod.category
    # value may name a concept in an extension's scheme rather than in
    # podcat:PodCategoryScheme — see pod.ttl's pod:category comment. One entry
    # per published extension.
    "bhscat": "http://mee.foundation/ontologies/pod-category-ext/boston-hub-society#",
    # Shape namespaces — a tpod.member[]/tpod.tool[].graph[].shape value is a
    # sh:NodeShape CURIE (pod:shape's range, pod.ttl), not a type label
    # class name, so these must resolve too. Same base URIs pod-category-templates.ttl
    # and each extension's own @prefix block declare. An unlisted prefix does
    # not raise — resolve() falls through to the tpod example namespace — so a
    # missing row here is silent, and every shape prefix in use needs one.
    "pshapes": "http://mee.foundation/ontologies/persona/shapes#",
    "petshapes": "http://mee.foundation/ontologies/pets/shapes#",
    "vehicleshapes": "http://mee.foundation/ontologies/vehicles/shapes#",
    "idocshapes": "http://mee.foundation/ontologies/identity-documents/shapes#",
    "mashapes": "http://mee.foundation/ontologies/medical-appointments/shapes#",
    "sashapes": "http://mee.foundation/ontologies/service-accounts/shapes#",
    "bankingshapes": "http://mee.foundation/ontologies/banking/shapes#",
    "residenceshapes": "http://mee.foundation/ontologies/residences/shapes#",
    "itineraryshapes": "http://mee.foundation/ontologies/itineraries/shapes#",
    "oshapes": "http://mee.foundation/ontologies/organization/shapes#",
    "educationshapes": "http://mee.foundation/ontologies/education/shapes#",
    "dpshapes": "http://mee.foundation/ontologies/directory-profile/shapes#",
    "bhsshapes": "http://mee.foundation/ontologies/pod-category-ext/boston-hub-society/shapes#",
}

# The three sub-keys of one tpod.serviceTag entry, mapped to the
# pod:ServiceTag datatype property each becomes (pod.ttl's Service
# Tag section). Spelled out rather than derived from the key name, so a grep
# for pod:tagNamespace finds this line.
TAG_SUBKEYS = {
    "namespace": "tagNamespace",
    "key": "tagKey",
    "value": "tagValue",
}

# Which pod:Tool subclass a tpod.tool entry's own `type` key names (pod.ttl's
# Pod Tools section). Spelled out rather than title-cased from the key, so a
# grep for pod:Form finds this line, and so an unknown type is a
# KeyError here rather than a triple naming a class that does not exist.
TOOL_TYPES = {
    "form": "Form",
    "calendar": "Calendar",
    "canvas": "Canvas",
    "map": "Map",
    "contacts": "Contacts",
    "browser": "Browser",
}


def resolve(val):
    """Resolve a YAML-string value (curie or bare tpod local name) to a full
    IRI. A `tpod.member`/`tpod.tool[].graph` entry's own `id` is already a full IRI
    (it doubles as the graph's actual named-graph identity), so it's used
    directly rather than passed through here."""
    if val.startswith("http://") or val.startswith("https://"):
        return val
    if val.startswith(":"):
        return TPOD_NS + val[1:]
    if ":" in val:
        prefix, local = val.split(":", 1)
        if prefix in PREFIXES:
            return PREFIXES[prefix] + local
    return TPOD_NS + val


def as_list(v):
    if v is None:
        return []
    return v if isinstance(v, list) else [v]


def split_frontmatter(text):
    """Return (fm_text, closing_dashes_incl_trailing_newline, body)."""
    m = FRONTMATTER_RE.match(text)
    if not m:
        raise ValueError("no frontmatter found")
    return m.group(2), m.group(3), m.group(4)


def iter_graph_blocks(body_text):
    """Yield (graph_marker, turtle_lines) for every ```turtle fence in
    body_text, in document order, with the fence's own `<!-- databook: -->`
    comment lines stripped (they are markers, not Turtle — riot rejects
    them). graph_marker is the fence's `<!-- databook:graph: X -->` value,
    or None if it carries no such marker. A merged pod-databook body may
    contain several fences, one per embedded graph."""
    in_fence = False
    current_graph = None
    current_lines = []
    for line in body_text.split("\n"):
        s = line.strip()
        if s == "```turtle":
            in_fence, current_graph, current_lines = True, None, []
            continue
        if in_fence and s == "```":
            in_fence = False
            yield current_graph, current_lines
            continue
        if in_fence:
            m = re.match(r"<!--\s*databook:graph:\s*(\S+)\s*-->", s)
            if m:
                current_graph = m.group(1)
                continue
            if s.startswith("<!-- databook:"):
                continue
            current_lines.append(line)


def extract_graph_block(body_text, target_graph):
    """Return the turtle lines (databook: comment lines stripped) for the
    single ```turtle fence in body_text whose <!-- databook:graph: X -->
    marker equals target_graph, or None if no fence matches."""
    for graph, lines in iter_graph_blocks(body_text):
        if graph == target_graph:
            return lines
    return None


def graph_entries(tpod):
    """Every graph entry a pod links, flattened into one list: its tpod.member
    entries first, then the graphs nested under each tpod.tool. Tool graphs sit
    one level deeper than member entries because a tool states its own
    formTopic once, above them; so that a caller reading a single graph does
    not have to walk back up to find it, each tool graph is returned with its
    tool's `type` and `formTopic` copied onto it. Those two keys are a
    read-time convenience only and are never written back to a databook —
    storing them per graph is exactly what carrying formTopic on the tool
    avoids."""
    out = list(as_list(tpod.get("member")))
    for tool in as_list(tpod.get("tool")):
        if not isinstance(tool, dict):
            continue
        for g in as_list(tool.get("graph")):
            if isinstance(g, dict):
                g = {**g, "type": tool.get("type", "form"),
                     "formTopic": tool.get("formTopic")}
            out.append(g)
    return out


def find_graph_entry(entries, graph_arg):
    """Match graph_arg (an id or id-local-name) against an iterable of graph
    entry dicts — callers pass in graph_entries(tpod), since a member entry or
    any tool's own graph can hold the graph being looked for."""
    for g in entries or []:
        if not isinstance(g, dict):
            continue
        gid = g.get("id", "")
        if gid == graph_arg or gid.rsplit("/", 1)[-1] == graph_arg:
            return g
    return None


def term(node):
    """Format a node as a Turtle term: a blank-node label (`_:x`) is written
    as-is, anything else is an IRI and gets angle brackets. Blank nodes enter
    the picture only as pod:serviceTag's pod:ServiceTag value nodes
    (pod.ttl's Service Tag section), and as tool_node()'s fallback for a
    malformed tool entry with no `id`."""
    return node if node.startswith("_:") else f"<{node}>"


def tag_node(pod_id, index):
    """A stable blank-node label for one pod:ServiceTag value node,
    derived from the pod's own id local-name plus the value's position in
    tpod.serviceTag. Turtle scopes a blank-node label to one document and
    yaml-to-rdf.py emits every pod in the tree into a single document, so a
    label unique only within one process_pod_databook() call would silently
    merge two pods' tag nodes into one. A pod id is already globally unique
    (integrity.md's YAML-3), so deriving from it needs no counter carried
    between calls and gives the same label on every run."""
    return f"_:tag_{pod_id.rsplit('/', 1)[-1]}_{index}"


def tool_node(pod_id, entry, index):
    """The node for one pod:Tool value. A live tool is named by its own IRI,
    the entry's `id` — what a note's block links resolve by (pod-databook.md's
    Tool Ids). An entry with no `id` is malformed, and falls back to a blank-node
    label derived the way tag_node() derives a pod:ServiceTag's, from the pod's
    own id local-name plus the tool's position in tpod.tool, so that it still
    synthesizes and then fails :LiveToolShape's sh:nodeKind sh:IRI instead of
    vanishing; integrity.md's YAML-2 and YAML-10 catch the same thing at YAML
    level, where they can name the file."""
    if isinstance(entry, dict) and entry.get("id"):
        return entry["id"]
    return f"_:tool_{pod_id.rsplit('/', 1)[-1]}_{index}"


def emit_type(triples, subj, type_iri):
    triples.append(f"{term(subj)} a <{type_iri}> .")


def emit_obj(triples, subj, prop, obj_iri):
    triples.append(f"{term(subj)} <{prop}> {term(obj_iri)} .")


def emit_lit(triples, subj, prop, lit):
    """Emit an xsd:string-typed literal triple — pod:userTag and the three
    pod:ServiceTag parts are the only `tpod.` values that are literals
    rather than IRIs, so they can't go through emit_obj()/resolve(): a tag is
    a plain string, never a CURIE or a local name."""
    escaped = str(lit).replace("\\", "\\\\").replace('"', '\\"')
    triples.append(
        f'{term(subj)} <{prop}> "{escaped}"^^<http://www.w3.org/2001/XMLSchema#string> .'
    )


def process_pod_databook(fm, triples):
    subj = fm["id"]
    tpod = fm.get("tpod", {}) or {}

    emit_type(triples, subj, POD + "Pod")

    if tpod.get("category"):
        # pod:category — domain pod:Pod, so asserted on every pod
        # regardless of facet (pod.ttl 3.45.0, renamed from pod:origin).
        emit_obj(triples, subj, POD + "category", resolve(tpod["category"]))

    # Every real pod-databook is always also typed pod:InstancePod — no
    # bare tree-position-only pod with no member content; a category node
    # with nothing substantive to say still carries a minimal stub
    # pod:member entry rather than omitting member content. Member count
    # itself is never stored — it's simply the number of distinct
    # subject values among tpod.member, derivable by counting whenever
    # needed. There is no second pod type to emit: a pod that carries
    # a tool holds pod:tool values, not a subclass.
    emit_type(triples, subj, POD + "InstancePod")

    if tpod.get("creator"):
        emit_obj(triples, subj, POD + "creator", resolve(tpod["creator"]))

    # pod:owner — one or more p:Person IRIs, resolved the same way as
    # pod:creator (never a bare graph-local-name).
    for owner_iri in as_list(tpod.get("owner")):
        emit_obj(triples, subj, POD + "owner", resolve(owner_iri))

    # pod:userTag — 0..N plain xsd:string values, domain pod:InstancePod
    # (pod.ttl's Pod Tags section), so emitted after the pod:InstancePod
    # typing above. as_list() lets a single bare string stand in for a
    # one-element list, the same latitude tpod.owner and a graph entry's own
    # template already get. No resolve() here — a user tag is a literal, not
    # a CURIE.
    for tag in as_list(tpod.get("userTag")):
        emit_lit(triples, subj, POD + "userTag", tag)

    # pod:serviceTag — 0..N, each value a pod:ServiceTag node
    # rather than a literal (an owl:ObjectProperty), carrying exactly one
    # pod:tagNamespace/pod:tagKey/pod:tagValue. as_list() applies to the
    # outer sequence only — a lone mapping may stand in for a one-element
    # list, the same latitude tpod.member gets — and never to the three
    # sub-values, each of which is exactly one scalar; coercing there would
    # turn a YAML error into a confusing sh:maxCount violation. The node and
    # its type are emitted even when the entry is malformed, so a missing
    # sub-key surfaces as an :ServiceTagShape sh:minCount violation
    # rather than the tag vanishing from the synthesized graph unremarked;
    # integrity.md's YAML-9 catches the same thing at YAML level, where it
    # can name the file and the sub-key.
    for i, tag in enumerate(as_list(tpod.get("serviceTag"))):
        node = tag_node(subj, i)
        emit_obj(triples, subj, POD + "serviceTag", node)
        emit_type(triples, node, POD + "ServiceTag")
        if not isinstance(tag, dict):
            continue
        for sub_key, prop in TAG_SUBKEYS.items():
            if sub_key in tag:
                emit_lit(triples, node, POD + prop, tag[sub_key])

    for entry in as_list(tpod.get("member")):
        emit_obj(triples, subj, POD + "member", entry["id"])
        process_embedded_graph(entry, triples, "member")

    # pod:tool — zero or more per pod, each a node named by the entry's own
    # `id` for one object the pod carries: a form, a calendar, a drawing canvas, a map, an
    # address-book sync or a connection to a web browser,
    # each with its own data format. The node's rdf:type comes from the
    # entry's own `type` key (form/calendar/canvas/map/contacts/browser); pod:formTopic, what the tool's
    # content is about, is carried once by the tool rather than repeated on
    # each graph beneath it, which is what makes its graphs unable to
    # disagree about what they are about.
    for i, entry in enumerate(as_list(tpod.get("tool"))):
        node = tool_node(subj, entry, i)
        emit_obj(triples, subj, POD + "tool", node)
        emit_type(triples, node, POD + TOOL_TYPES[entry.get("type", "form")])
        if entry.get("formTopic"):
            emit_obj(triples, node, POD + "formTopic", resolve(entry["formTopic"]))
        for graph in as_list(entry.get("graph")):
            emit_obj(triples, node, POD + "formGraph", graph["id"])
            process_embedded_graph(graph, triples, "tool")

    # No pod-level subject synthesis: who/what a pod is about is
    # derivable directly from tools/members — the distinct
    # pod:formTopic values if any tool is present, else the distinct
    # pod:subject values among members (pod.ttl's pod:tool
    # comment) — rather than an independently-asserted fact, so it is
    # never stored as its own triple.

    # No pod-level shape synthesis either: a pod:InstancePod's validation
    # shape is derivable from its own pod:category value via a reverse
    # lookup on pod-category-templates.ttl rather than stored per-instance.


def process_embedded_graph(graph, triples, kind):
    """Emit the graph typing plus claimant/shape for one tpod.member[] or
    tpod.tool[].graph[] entry. `kind` is "member" or "tool", and is what decides
    the type: pod:MemberGraph for a member entry, pod:FormGraph for a tool's own
    graph (pod.ttl's two disjoint pod:CGraph leaves). Nothing in the entry
    itself marks which kind it is; the list it was read from settles it,
    matching pod:member's and pod:formGraph's own ranges. Only a member
    entry carries an about-ness property of its own (pod:subject); a
    tool graph's is pod:formTopic, held once by the tool above it."""
    is_member = kind == "member"
    claimant = graph.get("claimant")
    about = graph.get("subject") if is_member else None
    if not claimant or (is_member and not about):
        return  # missing claimant or subject — not a well-formed graph, skip
    subj = graph["id"]
    emit_type(triples, subj, POD + ("MemberGraph" if is_member else "FormGraph"))
    emit_obj(triples, subj, POD + "claimant", resolve(claimant))
    if is_member:
        emit_obj(triples, subj, POD + "subject", resolve(about))

    # pod:shape — domain pod:Graph, so it applies to both kinds, 0..N,
    # present only on graphs that contain instance(s) of a shape's own type
    # label class (e.g. identitydocuments:Passport, pod.ttl's graph.png
    # diagram). A graph may satisfy more than one shape at once (e.g. a single
    # graph combining ServiceAccount, DebitCard, and CheckingAccount
    # instances), so this accepts either a bare string or a YAML list.
    for shape in as_list(graph.get("shape")):
        emit_obj(triples, subj, POD + "shape", resolve(shape))
