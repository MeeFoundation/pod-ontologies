# Integrity Checks

This file holds the project's integrity checks, split out of [CLAUDE.md](CLAUDE.md) to keep that file smaller. Everything else about the project — the ontologies, file layout, naming conventions, and architectural patterns these checks refer to — is documented in `CLAUDE.md`.

Files inside any directory named `under-development/` (at any depth) are works-in-progress and must be **excluded from all integrity checks** below.

After any change to a graph (its `tpod.member` entry or `tpod.tool[].graph` entry, or its `### Graph NN` body section) or a pod DataBook, verify the following.

## The four kinds

Checks are grouped by **what the check reads**, and numbered from 1 within each kind. The kind prefix is part of the identifier — `PNG-9`, `TTL-3`, `YAML-6`, `FS-5` — so no two checks ever share a number and the name alone says what a check looks at.

| Kind | Reads | Count |
|---|---|---|
| **PNG-n** | a diagram image — its pixels, or the drawing compared by eye against the data | 11 (+8 sub-checks, 2 of them retired) |
| **TTL-n** | a `.ttl` file, asking about triples; parses with `rdflib` | 8 |
| **YAML-n** | a pod DataBook's YAML frontmatter and Markdown body, as written | 10 |
| **FS-n** | the filesystem, and the documentation prose that refers to it | 6 |

A check that reads two kinds is filed under its **primary** input — the one that makes it the check it is — and says so in its own text. `TTL-2` also reads DataBook YAML; `YAML-5` also reads folder names.

## Running the checks

Run them **kind by kind**, announcing the kind and then working through its checks in order: PNG-1, PNG-2, … then TTL-1, TTL-2, … and so on. Reporting follows the same shape, so a result reads `TTL-3 PASS` and a failure is located by its kind before its number. Within PNG-1, the sub-checks run in letter order (PNG-1a … PNG-1h).

Not every check is automatable. Every PNG check except PNG-10 and PNG-11 is visual — the script under it prints the correct values for cross-reference rather than comparing the image — as are PNG-2's diagram direction and a few others that say so in their own text. Run the scripts; read the rest.

## Which checks use `rdflib`

A check that asks a question about **triples** parses with `rdflib`: every `TTL-n` check, and no other. Regex over Turtle reads documentation as data — it cannot tell an assertion from the same words inside an `rdfs:comment`, and `pod-category-templates.ttl`'s own `ctpl:UserDefinedTemplatePod` comment cites `?tc pod:category podcat:X` as prose, which the former regexes duly extracted as a category named `X` whose member shape was the sentence fragment `pshapes:ContactInfoShape — a Custom pod has no document type and no`. Harmless only by luck.

Every other kind **must not** use `rdflib`, because it asks about something that is not a graph and that parsing would normalize away. `YAML-9` is the clearest case — it hunts a non-string YAML sub-value, an entry that isn't a mapping, an extra sub-key and a repeated `(namespace, key, value)`, all of which synthesis would coerce, drop, or collapse into a set. `YAML-1` compares an id's zero-padding against its `### Graph NN` heading and `<a id=>` anchor, a serialization fact no graph retains. Converting either would make it strictly weaker.

`rdflib` is already required by `helpers/draw.py` and `helpers/validate.py`, so it adds nothing to install, and parsing every ontology and shapes file in the repo takes about 0.1s.

## Scaffolding checks

Many checks read the filesystem — the folders under `example/Pods/`, the `*.databook.md` files in it, and the PNGs under `example/graphs/images/`. All of that is **development scaffolding**: Tellipod persists no data in the user's filesystem at all (see [storage.md](storage.md)), and the on-disk layout exists only so that real pod content can be carried, validated and diagrammed before there is an app to hold it. Every `FS-n` check is a scaffolding check in that sense, along with `YAML-5` and `PNG-1a`: they keep this repo internally consistent and say nothing about how a running Tellipod stores anything. The rest test content that survives unchanged whatever the app does.

## Renumbering

These checks were previously numbered in one flat sequence, `Check 1` … `Check 39`, with several numbers retired and left unused. That scheme is gone: identifiers are now kind-prefixed and start at 1 within each kind. The old flat numbers map as follows, and no longer appear anywhere:

Check 10 → `PNG-1` · Check 10a → `PNG-1a` · Check 10b → `PNG-1b` · Check 10c → `PNG-1c` · Check 10d → `PNG-1d` · Check 10e → `PNG-1e` · Check 10g → `PNG-1f` · Check 10h → `PNG-1g` · Check 10i → `PNG-1h` · Check 1 → `PNG-2` · Check 12 → `PNG-3` · Check 13 → `PNG-4` · Check 14 → `PNG-5` · Check 37 → `PNG-6` · Check 38 → `PNG-7` · Check 15 → `PNG-8` · Check 20 → `PNG-9` · Check 33 → `PNG-10` · Check 34 → `PNG-11` · Check 4 → `TTL-1` · Check 16 → `TTL-2` · Check 26 → `TTL-3` · Check 27 → `TTL-4` · Check 28 → `TTL-5` · Check 29 → `TTL-6` · Check 30 → `TTL-7` · Check 39 → `TTL-8` · Check 2 → `YAML-1` · Check 3 → `YAML-2` · Check 9 → `YAML-3` · Check 18 → `YAML-4` · Check 19 → `YAML-5` · Check 21 → `YAML-6` · Check 23 → `YAML-7` · Check 25 → `YAML-8` · Check 36 → `YAML-9` · Check 5 → `FS-1` · Check 6 → `FS-2` · Check 7 → `FS-3` · Check 8 → `FS-4` · Check 11 → `FS-5` · Check 35 → `FS-6`

Retired checks `17`, `22`, `24`, `31`, `32` and sub-check `10f` had already been removed under the old scheme and have no counterpart here. Under the kind-prefixed scheme a retired check keeps its identifier, marked **Retired** in place, so that no other check is renumbered: `PNG-1b` and `PNG-1e` are the two.

## PNG — diagram checks

These read a **PNG**: either its pixels, or the drawing itself compared by eye against the data it depicts. They are the largest group because most of this project's conventions are expressed in a diagram first. Most are visual — the script under each one prints the correct values for cross-reference rather than comparing the image automatically.


**PNG-1 — Example pod diagrams**: Each of the 12 pod diagrams in `example/images/` draws one persistent view as the desktop app would display it: a flat list of pod boxes, plus display-only elements the app generates from the pods' tags. None of those elements is a pod, and none is stored anywhere. The diagrams draw no nesting, and none should ever be added: pods are a flat set. Each pod box corresponds to a pod in `example/Pods/`, the folder `example/Pods/<Name>/` holding its one pod-databook, `<Name>.databook.md`. The box's bold black first line is the pod's name, mirrored in its pod-databook's `title:`. A pod box reads, top to bottom:

1. the pod's name, in bold black;
2. its category tags on one green line, each as `#<prefLabel>`, if it has any (PNG-1f);
3. its user tags as grey `#<tag>` text, if it has any (PNG-1f);
4. its `{NN}` pod number (PNG-1g).

The display-only elements are an italic **view header** at the top left (`View tags: #<tag>`) and green **group headers** (PNG-1i). Where a diagram and the DataBooks disagree, the DataBooks are authoritative: fix the diagram, unless the data is actually wrong. After any change to `example/Pods/` DataBooks or to the 12 diagrams, verify all of the following:

- **PNG-1a — Every pod box has a pod DataBook**: Every pod box shown in any of the 12 diagrams must have a corresponding pod in `example/Pods/` whose pod-databook's `title:` equals the box's name line verbatim. A green group header or the view header is not a pod box and has no DataBook. Report any pod box with no DataBook rather than creating a pod to match it. PNG-10's `DIAGRAM` table records which pods each diagram draws, and its script reports any pod drawn in none.

- **PNG-1b — Retired.** It required every pod-databook other than an invisible root pod to appear as a box in some branch diagram. Pods do not nest, so there is no root pod and no branch to place a pod under; whether every pod is drawn somewhere is settled by the redraw itself (PNG-1).

- **PNG-1c — A pod box's graph shapes match its DataBook's `member`/`tool` links exactly, both in count and in type**: Shape, not fill, is what distinguishes a `pod:member` graph from a tool's own graph — a square for a tool graph, and for a `member` graph either a circle, when its subject is a human (`p:Person`), or an octagon, when its subject is an `s:Service`. Fill/outline color is a separate, independent fact showing only who claimed that graph — see PNG-8's legend and PNG-10. For the count and field checks below, circles and octagons both count as member shapes: the circle/octagon split is a further fact about *that member's own identity type*, orthogonal to which list the graph is filed in. For every pod box: (1) the total number of shapes attached to it (circles plus squares together) must equal the total number of that pod-databook's own `tpod.member` entries plus the graphs nested under all its `tpod.tool` entries — no more, no fewer; (2) every circle's own numbered label must correspond to a `tpod.member` entry, and every square's own numbered label must correspond to one of a tool's own graphs — never the reverse. A pod's several tools are not distinguished by shape: every tool graph is a square regardless of which tool holds it. A small document icon for a pod attachment (e.g. `companies.png`'s "VC" credential icons in the PRIVO and Facenook boxes) is not a graph shape and is excluded from both counts; its fill follows PNG-10's signed-attachment rule instead. This is a visual check (no automated image parsing), but the script below prints every pod's own member/tool graph numbers, split by field, for direct cross-reference against whichever diagram box is being checked — e.g. `pets.png`'s "Ginger" box shows one circle (`Self [36]`) and one square (`Ginger [37]`), matching `Ginger.databook.md`'s own one member (graph-36) and one tool graph (graph-37); its "Medical" box (the Ginger Medical pod) shows two circles (`Self [33]`, `Paula [57]`) and one square (`Ginger [32]`), matching `Ginger Medical.databook.md`'s two members (graph-33, graph-57) and one tool graph (graph-32). Run:

```python
import re, glob, yaml

def frontmatter(path):
    text = open(path, encoding='utf-8').read()
    m = re.match(r'^---\n(.*?)\n---', text, re.DOTALL)
    return yaml.safe_load(m.group(1)) if m else None

def local_names(entries):
    entries = entries if isinstance(entries, list) else ([entries] if entries else [])
    return [e['id'].rsplit('/', 1)[-1] for e in entries]

for path in sorted(glob.glob('example/Pods/**/*.databook.md', recursive=True)):
    if 'under-development' in path.split('/'):
        continue
    fm = frontmatter(path)
    if not fm or fm.get('type') != 'pod-databook':
        continue
    tpod = fm.get('tpod', {}) or {}
    members = local_names(tpod.get('member'))
    tools = tpod.get('tool') or []
    tool_graphs = []
    for tool in (tools if isinstance(tools, list) else [tools]):
        tool_graphs += local_names(tool.get('graph'))
    print(f"{fm.get('title')!r:30} member(circle)={members}  tool(square)={tool_graphs}")
```

- **PNG-1d — Numbered graph circles/squares have matching embedded graphs**: Every numbered graph circle or square (e.g. `[10]`, `[17]`) shown in a diagram must correspond to a `tpod.member` entry or a tool's own graph (equivalently, a `### Graph NN` body section) in some pod-databook under `example/Pods/` whose id contains that number (e.g. `(10)`, `(17)`).

- **PNG-1e — Retired.** It matched each diagram's child arrows to folder nesting under `example/Pods/`. Pods do not nest and `example/Pods/` is flat (FS-5), so there are no child links to match. The grey connectors the 12 diagrams draw join a group header to the pods listed under it (PNG-1i); they are display-only and say nothing about nesting.

- **PNG-1f — Green category-tag lines and grey user-tag text match the pod's tags**: Below the name, a pod box shows its own tags, with the hash the UI uses for a tag. The **category tags** share one green line, each written `#<prefLabel>` and separated by a space, in `tpod.categoryTag` order, giving each concept's `skos:prefLabel`, from `pod-categories.ttl` or from a category extension's own file under `pod-category-ext/`. The label must match its concept's `skos:prefLabel` verbatim, no more and no fewer words, and never abbreviated. The line is shown even when the label equals the pod's own name: `things.png`'s "Things" box shows `#Things`, and `gov-federal.png`'s "SSN" box shows `#SSN`. No green line is drawn only for a pod with no category tags. The **user tags** follow in grey, each as `#<tag>`, one per `tpod.userTag` value, and none for a pod with none: `pets.png`'s three boxes each show `#Ginger`, and `work.png`'s three each show `#Acme`. A box shows no implied (broader) tag. The broader concepts appear only as group headers (PNG-1i). This is a visual check. PNG-1i's script prints every pod's green and grey lines for cross-reference: for example, `work.png`'s "Paula Walker" box shows the green line `#Employees #Immediate Family`, `home.png`'s "Paradise" box shows `#Home` and its "Boston" box `#Previous`, matching their tags `podcat:Home` and `podcat:Previous`, and `travel.png`'s "Kyoto Trip 2027" box shows `#Trips`.

- **PNG-1g — Black curly-brace `{NN}` label matches the pod's own `pod-<NN>` id**: Every pod box ends with a small black `{NN}` label in curly braces: the pod's own number. It sits on its own last line, or at the end of the last tag line (`#Ginger {41}`, `#Groups {27}`). It must equal the number in the pod-databook's own `id: http://www.example.org/tpod/pods/pod-<NN>` (see YAML-3), written without its zero padding. Group headers and the view header carry no `{NN}`, since they are not pods. Don't confuse this label with the `[NN]` labels on graph shapes (PNG-1d): those are graph numbers in square brackets on a circle, octagon or square, while this is the pod's own number in curly braces on the box itself. This is a visual check (no automated OCR), but the script below, and PNG-1i's, print every pod's actual `pod-<NN>` for cross-reference. For example, `people.png`'s "Bob Johnson" box shows `{16}` and its "Fred Flintstone" box `{17}`; `people2.png`'s "Sophia Walker" box shows `{12}`, "Sophia Health & Wellness" `{13}`, "Jane Starostina" `{14}` and "Medical Appointment" `{15}`; `pets.png`'s "Ginger" box shows `{41}`, "Ginger Medical" `{40}` and "Ginger Care & Feeding" `{42}`; and `travel.png`'s "Kyoto Trip 2027" box shows `{47}` and "Hilton" `{52}`. Run:

```python
import glob, re

for path in sorted(glob.glob('example/Pods/**/*.databook.md', recursive=True)):
    if 'under-development' in path.split('/'):
        continue
    text = open(path).read()
    m = re.search(r'^id:\s*http://www\.example\.org/tpod/pods/(pod-\d{2})', text, re.MULTILINE)
    if m:
        print(f'{m.group(1)}  {path}')
```

- **PNG-1h — Fill color matches real data**: Every pod box's **fill** is set by its category type, matching the legend's "Category tags" box. The type comes from the top concepts the pod's `pod:categoryTag` values reach, following `skos:broader` upward, and for a category extension's concept its single `skos:broadMatch` into the core taxonomy first. The fill is tan/Person when every tag reaches `podcat:Person`, light blue/Organization when every tag reaches `podcat:Organization`, a light-blue-to-tan gradient (Mixed) when the tags reach both, and purple/None when the pod carries no category tag at all. A pod's **name** is always bold black. These diagrams carry no green-name/black-name distinction, the category tags being shown on their own green line instead (PNG-1f). This is a visual check (no automated pixel/OCR comparison). Use PNG-9's script to compute the correct fill for every pod. For example, `people.png`'s "Bob Johnson" and "Fred Flintstone" are tan (tag `podcat:Others`), `work.png`'s "Acme" and "Alice Walker" are light blue (`podcat:Organization` itself, and `podcat:Employees`, which reaches it), its "Paula Walker" carries the light-blue-to-tan gradient (Mixed: `podcat:Employees` reaches `podcat:Organization`, `podcat:ImmediateFamily` reaches `podcat:Person`), and `groups.png`'s "Boston Hub Society" is tan (`bhscat:BostonHubSociety` reaches `podcat:Person` through its `skos:broadMatch` to `podcat:Groups`). Every example pod carries a category tag, so no example diagram box is expected to show purple fill.

- **PNG-1i — The view header and group headers match the pods' tags**: These elements are display-only, and none of them is a pod. Each diagram carries one view header and zero or more group headers.

  - **The view header** is an italic `View tags: #<tag>` at the top left. It names the persistent view's stored tag query, and every pod box drawn must match it. A pod matches when the tag is one of the pod's user tags (`#Ginger`, `#Sophia`, `#Acme`), when the tag is one of the pod's category tags, or when the tag is a concept one of its category tags reaches upward (`#Travel` matches `#Trips` and `#Provider`; `#Groups` matches `#Boston Hub Society` through its `skos:broadMatch`).
  - **A group header** is a green `#<prefLabel>` with grey connectors to the pods listed under it. A pod's headers are, for each of its category tags, the broader concepts that tag reaches, outermost first, down to the tag's immediate broader concept. A pod with several category tags is listed once under each of its tags' header chains, so it can appear more than once in one view: `work.png`'s "Paula Walker" is drawn twice, once under `#People (org)` for `podcat:Employees` and once under `#People` for `podcat:ImmediateFamily`, both boxes identical. The top concept (`podcat:Person` or `podcat:Organization`) is never drawn as a header. A deeper header is drawn indented beneath the one above it: `people2.png`'s `#Health & Wellness`, then `#Medical`, then `#Provider`, above Jane Starostina and Medical Appointment. A header is never the category tag it is drawn for; that tag is on the box (PNG-1f).
  - **Pods with no header** are those listed for a tag that sits directly under a top concept, or is one, and those which carry no tag. They are listed first, above every header: `things.png`'s "Things" (`#Things`, directly under Person) above `#Things` and RAV4, and `work.png`'s "Acme" (`#Organization`) above `#People (org)`.

  A header that stands for no concept the tag it is drawn for reaches, or a header skipped in the chain, is an error. So is a header that duplicates that tag, or a top concept drawn as a header. The script below prints, for every pod and each of its category tags, the header chain, the green category-tag line, its grey user-tags line, and its `{NN}`. Run:

```python
import glob, re, yaml

# Concept CURIE -> prefLabel, and -> the one concept it links upward to (its
# skos:broader, or an extension concept's skos:broadMatch), as in PNG-9.
NAME = r'([A-Za-z]+(?:\\\(org\\\))?)'
pattern = re.compile(
    r'(\w+):' + NAME + r' rdf:type skos:Concept\s*;\s*'
    r'skos:prefLabel "([^"]+)"@en\s*;\s*'
    r'(?:skos:(?:broader|broadMatch) (\w+):' + NAME + r'\s*;\s*)?'
)
unescape = lambda s: s.replace('\\(', '(').replace('\\)', ')')
labels, up = {}, {}
for path in ['pod-categories.ttl'] + sorted(glob.glob('pod-category-ext/*.ttl')):
    for m in pattern.finditer(open(path, encoding='utf-8').read()):
        curie = f'{m.group(1)}:{unescape(m.group(2))}'
        labels[curie] = m.group(3)
        if m.group(4):
            up[curie] = f'{m.group(4)}:{unescape(m.group(5))}'

TOPS = {'podcat:Person', 'podcat:Organization'}

def headers(tag):
    """The group headers drawn above a pod: its tag's broader concepts, outermost
    first, stopping short of the top concept. None if the chain never reaches one."""
    chain, seen, c = [], set(), tag
    while c not in TOPS:
        if c in seen or c not in up:
            return None
        seen.add(c)
        c = up[c]
        if c not in TOPS:
            chain.append(labels.get(c, '???'))
    return list(reversed(chain))

def as_list(v):
    return v if isinstance(v, list) else ([v] if v else [])

for path in sorted(glob.glob('example/Pods/**/*.databook.md', recursive=True)):
    if 'under-development' in path.split('/'):
        continue
    text = open(path, encoding='utf-8').read()
    m = re.match(r'^---\n(.*?)\n---', text, re.DOTALL)
    fm = yaml.safe_load(m.group(1)) if m else None
    if not fm:
        continue
    tpod = fm.get('tpod', {}) or {}
    num = re.search(r'pod-0*(\d+)$', str(fm.get('id', '')))
    grey = ' '.join('#' + t for t in as_list(tpod.get('userTag'))) or '-'
    tags = as_list(tpod.get('categoryTag'))
    # The box's one green line carries every tag; the box itself is drawn once
    # under each tag's header chain, so a multi-tag pod gets one row per tag.
    green = ' '.join('#' + labels.get(t, '???') for t in tags) or '-'
    for tag in tags or [None]:
        hdr = headers(tag) if tag else []
        if hdr is None:
            print(f'UNRESOLVED: {path} has a category tag that reaches no top concept: {tag}')
            continue
        print(f'{fm.get("title"):35s} headers={" > ".join("#" + h for h in hdr) or "-":40s} '
              f'green={green:26s} grey={grey:10s} {{{num.group(1) if num else "?"}}}')
```

The 12 diagrams are: `example/images/people.png`, `example/images/people2.png`, `example/images/work.png`, `example/images/companies.png`, `example/images/finances.png`, `example/images/gov-state.png`, `example/images/gov-federal.png`, `example/images/home.png`, `example/images/things.png`, `example/images/groups.png`, `example/images/pets.png`, `example/images/travel.png`. There is no `health.png`: Sophia's health pods (Sophia Health & Wellness, Jane Starostina, Medical Appointment) are drawn in `people2.png`, under the view `#Sophia`. Which pods each diagram draws is recorded in PNG-10's `DIAGRAM` table. A few boxes are worth noting for what they show:

- `companies.png`'s "Arca" (pod-50, `{50}`, graphs `[95]`/`[96]`/`[97]`) is Alice's pod backup provider and the first worked example of a `service:ArcaBackup` pod member. Its two circles are Alice (`[95]`) and the backup service itself (`[96]`, green/Other, claimed by `:Arca_Backup`, an agent service carrying `s:actsFor :Self` alongside its `s:providedBy :Arca`).
- `pets.png`'s "Ginger Medical" box (pod-40, graphs `[32]`/`[33]`/`[57]`) holds Ginger's medication content, and its "Ginger Care & Feeding" box (pod-42, graphs `[58]`/`[59]`/`[60]`) holds her day-to-day care instructions (`podcat:PetsCareAndFeeding`).
- `things.png`'s "RAV4" (pod-44, `{44}`, graphs `[62]`/`[63]`) is Alice's car.
- `travel.png`'s "Kyoto Trip 2027" (pod-47, `{47}`, graphs `[66]`/`[68]`/`[69]`/`[91]`) has two member circles ("Self" `[66]`, "Dave" `[68]`) and two tool-graph squares sharing one subject ("Kyoto" `[69]`/`[91]`, claimed by Self and Dave respectively). With one tool graph per member, it is the first worked example to reach `pod:formGraph`'s real upper bound (YAML-8).

**PNG-2 — Diagram ↔ files ↔ example.md coverage**: Every numbered graph circle in any of the 12 pod diagrams (`example/images/`) must have (a) a corresponding embedded graph section — a `tpod.member` or `tpod.tool[].graph` entry plus its `### Graph NN` body section — inside a pod-databook file under `example/Pods/`, and (b) a row in one of the tables in the **Graphs** section of `example.md`. Conversely, every row in those tables must correspond to an embedded graph that actually exists — and to that alone: a row does **not** need a numbered circle in any diagram. The 12 diagrams are not required to draw every graph; every graph is documented — a row in `example.md`'s **Graphs** section and a PNG in `example/graphs/images/` (FS-2 and FS-3) — whether or not any diagram draws it. If a circle exists in a diagram but has no embedded graph or `example.md` row, report it rather than creating a graph to match: the DataBooks are authoritative (PNG-1).

**PNG-3 — `pod.ttl` matches `images/pod-ontology/pod.png`**: `Pod` shows `attachment` (to a `sources:SourceItem` box, drawn **0..N**, matching `pod:attachment`'s range — `other/sources.ttl`, referenced by name with no `owl:imports` — and its unbounded cardinality: the files every member of the pod receives, never a member's own private ones). The two classification properties, `pod:category` and `pod:categoryTag`, both range over the classificatory `skos:Concept` (a concept in `podcat:PodCategoryScheme`, pod-categories.ttl, or in a category extension's own scheme); pods do not nest, so there is no tree-position class for either to be confused with. Both record what kind of thing a pod is, and neither needs `owl:imports pod-categories.ttl` (referenced by name only, mirroring `pod:creator`'s identical pattern). The diagram shows two arrows off `Pod` with no counterpart in `pod.ttl` — `note` (to a placeholder box, `(note data object) 1..1` — the note is held in the app's own internal format, not as a Markdown file) and `chat` (to a placeholder box, `(a chat stream) 1..1` — every pod always has a chat stream, possibly empty, held inside the app rather than in the pod's folder) — this is a deliberate, accepted exception to 12a/12b below: README.md already describes both properties' intended semantics (see the Documentation-only Properties section) as planned, but `pod.ttl` itself has no `pod:note`/`pod:chat` declaration yet — neither is ever reified as a triple in any real graph. `Pod` (abstract, blue) carries `attachment` (plus the still-open `note`/`chat` arrows above). `Pod` splits into two disjoint kinds (`owl:disjointWith` — a pod is always exactly one, never both): `TemplatePod` (abstract, blue, a reusable class-level template) carries `category` (to a `skos:Concept` box, **0..1** — the one concept the template is for, carried by every template except `ctpl:UserDefinedTemplatePod`, which carries none), `memberShape` (to a `sh:NodeShape` box, 0..N) and `declaresTool` (to a `pod:Tool` box, 0..N); `InstancePod` (concrete, black, a pod a user actually has) carries `member` (to a `pod:MemberGraph` box, 1..N, no fixed upper bound), `tool` (to a `pod:Tool` box, 0..N), `creator` (to a `p:Person` box, 1..1), `owner` (to its own `p:Person` box, 1..N, no fixed upper bound — every arrow in this diagram carries its own target label, so `creator` and `owner` are drawn as two separate `p:Person` boxes rather than sharing one), and the three tag properties `categoryTag` (to a `skos:Concept` box, **0..N**), `userTag` (to an `xsd:string` box, 0..N) and `serviceTag` (to a `pod:ServiceTag` box, 0..N) — `pod.ttl`'s Pod Tags section. The three tag arrows hang off `InstancePod`, never off `Pod`: their domain is `pod:InstancePod` deliberately, since a `TemplatePod` seeds no tags. `category` and `categoryTag` hang off different boxes for the same reason: `category` names the one concept a template is for and never appears on an instance pod, while `categoryTag` is a member's own classification of a pod, zero or more concepts. The three tags point at different kinds of target because they are different shapes: a category tag is a concept, a user tag is a bare literal, and a service tag is a value node. `ServiceTag` and the `Tool` hierarchy are **not** drawn in this diagram: each has its own, `images/pod-ontology/tag.png` (PNG-6) and `images/pod-ontology/tool.png` (PNG-7). Here they appear only as arrow targets — a `pod:ServiceTag` box off `serviceTag`, and a `pod:Tool` box off both `tool` and `declaresTool` — never as members of the `Pod` hierarchy, which neither has an `rdfs:subClassOf` relation to. There is no `shape` arrow off `InstancePod` at all — a pod stores no shape of its own; the `shape` property that does exist has domain `pod:Graph` and is drawn in `graph.png` (PNG-4) (each graph's own `pod:shape`, set from the template that supplied the graph, is the validation authority for that graph; there is no single template of a pod to derive a pod-level shape from, a pod carrying zero or more category tags) — and no pod-level `subject` arrow off `InstancePod` either — there is no such property (a pod's own subject is derived from its tools' own `pod:formTopic` values, or failing those from `member`'s own `pod:subject` values, rather than stored on the pod itself; those two are real, surviving properties, scoped to `pod:Tool` and `pod:MemberGraph` rather than to `InstancePod` — see PNG-4). `TemplatePod` has no subclasses of its own, and no individual is ever typed both `TemplatePod` and `InstancePod` — every template individual in `pod-category-templates.ttl` is typed solely `TemplatePod`. No arrow points from `Pod`, `TemplatePod`, or `InstancePod` to any tree-position box at all — pods do not nest, and both classification arrows point to `skos:Concept`. This diagram is the ontology-level (not example-data) picture of `pod:Pod`'s structure — the member-composition hierarchy and its content-linking properties. A single "Key" box in the lower right carries three swatches, in this order — blue "Abstract", black "Concrete and visible", green "Concrete but hidden" — and the class-box colors track them exactly: blue is `pod:abstract true` in `pod.ttl` (`Pod` and `TemplatePod`, and nothing else here) and black is every remaining concrete class. The Key lists exactly the swatches this diagram actually uses — two here, since the one green ("concrete but hidden") class, `ServiceTag`, is drawn in `tag.png` instead. A concrete class may only be green where `pod.ttl` or `README.md` actually says the user never sees it; absent that, it is black. Unlike PNG-1 (example diagrams, where the diagram always wins), this check does not presume which side is authoritative when the two disagree — surface the discrepancy and ask:

- **12a** — every property arrow shown off `Pod` (`attachment`) has a corresponding `pod:` property in `pod.ttl` with `rdfs:domain pod:Pod` (the diagram's `note` and `chat` arrows are the two accepted exceptions — see above: both are planned properties, not yet added to `pod.ttl`). Every arrow off `TemplatePod` (`category`, `memberShape`, `declaresTool`) has `rdfs:domain pod:TemplatePod`, and every arrow off `InstancePod` (`creator`, `owner`, `member`, `tool`, `categoryTag`, `userTag`, `serviceTag`) has `rdfs:domain pod:InstancePod`. No arrow may appear off the `pod:Tool` or `pod:ServiceTag` target boxes here — those belong to PNG-7 and PNG-6. No `shape` arrow should appear off `InstancePod` at all — a pod stores no shape of its own, and `pod:shape`'s domain is `pod:Graph`, so it belongs in `graph.png` (PNG-4) (each graph carries its own; a pod stores none). No pod-level `subject` arrow should appear off `InstancePod` either — that property doesn't exist (see PNG-3's own note above); `pod:subject` is real, but scoped to `pod:MemberGraph`, not to `InstancePod` (see PNG-4). Each arrow's target type in the diagram must match the property's `rdfs:range` — `member`'s is `pod:MemberGraph` and `formGraph`'s is `pod:FormGraph` — deliberately *different* classes, one per list, `tool`'s and `declaresTool`'s are both `pod:Tool`, `creator`'s and `owner`'s are both `p:Person` (two separate arrows, each with its own target box — what must match is the range, not the box count), `categoryTag`'s is `skos:Concept`, `userTag`'s is `xsd:string` and `serviceTag`'s is `pod:ServiceTag` (three separate arrows, each 0..N — not one shared arrow, since a tag's kind is carried entirely by which property holds it, and no two share a target), `tagNamespace`'s, `tagKey`'s and `tagValue`'s are all `xsd:string` (three separate arrows, each 1..1), `attachment`'s is `sources:SourceItem` (0..N — a stale `(file)` placeholder target is a discrepancy), `category`'s is `skos:Concept` itself (value is a named category-concept individual, scoped via `skos:inScheme` to `podcat:PodCategoryScheme` or a category extension's own scheme — no class-value punning, since pod-categories.ttl's hierarchy is SKOS, not OWL classes), `memberShape`'s is `sh:NodeShape` (0..N, not 0..1). `formShape` does **not** appear in this diagram at all — its domain is `pod:Tool`, so it is drawn in `tool.png` (PNG-7).
- **12b** — every `pod:` property defined in `pod.ttl` appears as an arrow in the diagram, under the box matching its domain — `Pod`, `TemplatePod`, `InstancePod`, `Tool` (or one of its `Form`/`Calendar`/`Canvas`/`Contacts`/`Map`/`Browser` subclasses), or `ServiceTag` (catches new properties added to the ttl but never drawn, or drawn under the wrong box).
- **12c** — the class hierarchy `Pod` → `TemplatePod`/`InstancePod` (both `owl:disjointWith` one another) shown in the diagram matches `pod.ttl`'s actual `rdfs:subClassOf` relationships (by class local name, not just position). No class hangs below `InstancePod`: a pod that carries a tool is not a different kind of pod, only one carrying `tool` values. `pod:Tool` takes no part in this hierarchy — it has no `rdfs:subClassOf` relation to `Pod` or to either of its kinds, so no subclass line may connect the two; an `InstancePod` *points at* tools via `pod:tool`, and a `TemplatePod` at declared ones via `pod:declaresTool`, but neither contains them as subclasses. `ServiceTag` likewise takes no part in this hierarchy: it is a value-node class `pod:serviceTag` points at, with no `rdfs:subClassOf` in `pod.ttl`, so no subclass line may connect it to `Pod` or to any of `Pod`'s kinds, and its green fill is a display fact about its instances rather than anything `pod:abstract` records.

**PNG-4 — `pod.ttl`'s graph-DataBook classes match `images/pod-ontology/graph.png`**: `pod:Graph`/`pod:CGraph`/`pod:MemberGraph`/`pod:FormGraph` and their `shape`/`claimant`/`subject` annotation properties — the graph-DataBook classification vocabulary, defined in `pod.ttl` since a graph DataBook only ever exists to be linked from a pod — are diagrammed separately from `pod.ttl`'s member-composition hierarchy (PNG-3's `pod.png`), in this dedicated `graph.png`. The diagram shows four boxes on three levels: `Graph` at the top, `CGraph` beneath it, and `CGraph`'s two leaves `MemberGraph` and `FormGraph` side by side. `Graph` shows only `shape` (targeting `sh:NodeShape` 0..N, matching `pod:shape`'s actual `rdfs:range`); `CGraph` (subClassOf `Graph`) shows only `claimant` (targeting `p:Person`/`o:Organization`/`s:Service` 1..1); `MemberGraph` (subClassOf `CGraph`) shows only `subject` (targeting `xsd:anyURI` 1..1), while `FormGraph` (subClassOf `CGraph`) shows no property arrow at all — its about-ness is the holding tool's own `formTopic`, drawn in `pod.png`. No `subject`, `about-by` or `topic` arrow appears anywhere — the two about-ness properties are spelled `subject` (on `pod:MemberGraph`) and `formTopic` (on `pod:Tool`) in `pod.ttl`, so a diagram edge labeled with the bare short form is stale and should be relabeled. No leaf subtype boxes appear below `MemberGraph` or `FormGraph` — neither has subclasses. A "Key" box in the lower right carries two swatches, in this order — blue "Abstract", black "Concrete and visible" — and the class-label colors track them exactly: blue is `pod:abstract true` in `pod.ttl` (`Graph` and `CGraph`), black is every concrete class (`MemberGraph`, `FormGraph`). This is the same convention `pod.png` uses (PNG-3), minus its green "Concrete but hidden" swatch, which is correctly absent here since no class in this diagram is one the app hides from the user. This diagram is the ontology-level picture of `pod:Graph`'s structure.

The split into two leaves is the diagram's substantive claim, and it is a PDN-layer one: a `claimant` and a `subject` value always name a party holding a PDN node subject identity, whereas the `formTopic` standing above a `FormGraph` need not and routinely does not (a `pets:Pet`, a `vehicles:Vehicle`, an `identitydocuments:Passport`, a recipe, a poem). That is why the two are separate properties on separate `owl:disjointWith` classes rather than one property with a wider range. After any change to `pod.ttl`'s graph-DataBook terms or to this diagram, verify:

- **13a** — every property arrow shown off `Graph` in the diagram (`shape`) has a corresponding `pod:` property in `pod.ttl` with `rdfs:domain pod:Graph`, and its target type matches the property's `rdfs:range`.
- **13b** — the one arrow off `CGraph` (`claimant`) has `rdfs:domain pod:CGraph`, not `pod:MemberGraph`; its target in the diagram must match its actual `rdfs:range` — a union of `p:Person`/`o:Organization`/`service:Service`. No `about-by` arrow should appear — `pod.ttl` defines no such property.
- **13c** — the one arrow off `MemberGraph` (`subject`) has `rdfs:domain pod:MemberGraph`, and its target must match its actual `rdfs:range`, any resource IRI (`xsd:anyURI`), not a Person/Organization union. `FormGraph` carries **no** about-ness arrow of its own: what a tool's graphs are about is the holding tool's single `formTopic`, drawn in `pod.png` (PNG-3) rather than here. Neither leaf may show the other's arrow — the two are `owl:disjointWith`, and `shacl/pod-shacl.ttl`'s `:FormGraphShape` carries an `sh:maxCount 0` on `pod:subject` to enforce it.
- **13d** — every `pod:` property whose domain is one of these four classes, defined in `pod.ttl`, appears in the diagram under the correct box (catches new properties added to the ttl but never drawn, or drawn under the wrong box).
- **13e** — the hierarchy `Graph` → `CGraph` → `MemberGraph`/`FormGraph` shown in the diagram matches `pod.ttl`'s actual `rdfs:subClassOf` relationships by class local name, and the two leaves carry `owl:disjointWith` one another. `Graph` and `CGraph` are both `pod:abstract true`; the two leaves are not.
- **13f** — the class-label colors match `pod.ttl`'s `pod:abstract` annotations: `Graph` and `CGraph` blue (both `pod:abstract true`), `MemberGraph` and `FormGraph` black (neither carries it). The Key box lists exactly the swatches the diagram actually uses — two here, since nothing in this diagram is hidden from the user; do not paste `pod.png`'s third, green swatch in unless a hidden class is ever added.
- **13g** — no subclasses appear below `MemberGraph` or `FormGraph` — `pod.ttl` defines none for either. If any appear here or in `pod.ttl`, reconcile them. Check also that `pod:member`'s `rdfs:range` is `pod:MemberGraph` and `pod:formGraph`'s is `pod:FormGraph` (the ranges are what type a real graph, since nothing in a `tpod.member` entry or a tool's own graph marks its own kind — see YAML-2).

**PNG-5 — `pod-categories.ttl` matches `images/pod-categories/pod-categories.png`**: This diagram is the picture of `pod-categories.ttl`'s SKOS concept scheme, not an OWL class hierarchy: `podcat:PodCategoryScheme` (a `skos:ConceptScheme` box) carries `hasTopConcept` arrows to `podcat:Person`/`podcat:Organization`, each a plain `skos:Concept` box (there is no `podcat:Category` class anywhere in the diagram — every box is an individual, not a class), each with representative narrower-concept examples reachable via `broader` arrows drawn concept → concept (Groups/People/Work → Person; Suppliers/People (org) → Organization). There is no `templatePod` arrow anywhere — `pod-categories.ttl` defines no such property; a templated concept's reusable content is found from `pod-category-templates.ttl`'s side instead (see PNG-3), not drawn on this diagram at all. No `Folder`/`CategoryDefined`/`UserDefined` boxes and no `child`/`pod`/`category`/`catType`/`label` arrows should appear anywhere. This diagram does not presume which side is authoritative when the two disagree — surface the discrepancy and ask. After any change to `pod-categories.ttl` or to this diagram, verify:

- **14a** — the only property arrows in the diagram are `hasTopConcept` (off `PodCategoryScheme`, to `Person`/`Organization`) and `broader` (off every other concept, to its own parent concept) — matching `pod-categories.ttl`'s actual `skos:hasTopConcept`/`skos:broader` triples — **plus the category-extension inset described in 14d**, which is the one part of this diagram not drawn from `pod-categories.ttl`. No `templatePod` arrow should appear anywhere — `pod-categories.ttl` defines no such property. No `catType`, `child`, `pod`, `category`, `label`, or `narrower` arrow should appear anywhere either — `pod-categories.ttl` asserts only `broader` (child → parent), never the inverse `narrower`, and defines none of the `Folder`/`CategoryDefined`/`UserDefined` classes such arrows would live on. No `memberShape`/`formShape` arrow should appear either — those are `pod.ttl` properties (see PNG-3), never `pod-categories.ttl` ones. There must be no `Canonical` box and no `copiedFrom` arrow anywhere — `pod-categories.ttl` defines neither.
- **14b** — every `skos:` property actually asserted in `pod-categories.ttl` (`hasTopConcept`, `broader`, `inScheme`, `topConceptOf`, `prefLabel`) appears as an arrow or label in the diagram, under the box matching its domain (catches a new relationship added to the ttl but never drawn). `pod-categories.ttl` defines no `podcat:` property of its own.
- **14c** — the concept structure shown in the diagram — `PodCategoryScheme` → `hasTopConcept` → `Person`/`Organization` → `broader`-linked narrower concepts — matches `pod-categories.ttl`'s actual `skos:hasTopConcept`/`skos:broader` triples (by concept local name, not just position), the 14d inset excepted. There is no class hierarchy to check — `pod-categories.ttl` defines no `owl:Class` other than the ontology header's implicit `owl:Ontology` typing, and no `Folder` hierarchy at all.

- **14d — the category-extension inset** — the diagram carries exactly one illustration of the [category extension](README.md#category-extensions) mechanism, and it is the only content here that does not come from `pod-categories.ttl`. It is **two boxes and two arrows**: an `ExtensionScheme` box (a `skos:ConceptScheme`, its label drawn italic and in parentheses as *(ExtensionScheme)* to mark it as a scheme published outside `pod-categories.ttl`, not a second core scheme) and an `ExtensionConcept` box (a `skos:Concept`), joined by a green `hasTopConcept` arrow scheme → concept, plus a **dashed purple `broadMatch` arrow** from `ExtensionConcept` to one core concept (`Groups`). The dashed line is load-bearing: solid means hierarchy within one scheme, dashed means a mapping between schemes, which is the whole SKOS distinction the mechanism rests on (see TTL-8). The labels must stay **generic placeholders** — never a real publisher's concept such as `bhscat:BostonHubSociety` — since this diagram is embedded in `README.md`, which carries theory only; the worked extension belongs in `example.md`. The two boxes follow the Key's own color rule exactly as the core tree does: `ExtensionScheme` is **blue** (Abstract — a `skos:ConceptScheme` is never shown to a user, which is why `PodCategoryScheme` is blue too), and `ExtensionConcept` is **black** (Visible to user — it is a category a pod is actually tagged with, the peer of `Groups`, which the `broadMatch` arrow points at). Getting these the same color as each other is the easy mistake: it makes a scheme and a concept read as one kind of thing. The Key carries a matching third arrow row, `broadMatch`, alongside `hasTopConcept` and `broader concept`. No other extension box, arrow, or scheme may appear: one inset is an illustration, several would be a second taxonomy.

**PNG-6 — `pod.ttl`'s `pod:ServiceTag` matches `images/pod-ontology/tag.png`**: The service-tag value node has its own diagram rather than sitting inside `pod.png`, since it takes no part in the `Pod` hierarchy at all. `ServiceTag` (concrete but hidden, green) is drawn as a standalone box carrying three arrows — `tagNamespace`, `tagKey` and `tagValue` — each to an `xsd:string` box at `1..1`:

- **37a** — each of the three arrows has `rdfs:domain pod:ServiceTag` and `rdfs:range xsd:string` in `pod.ttl`, and each is required exactly once (`shacl/pod-shacl.ttl`'s `:ServiceTagShape`, `sh:minCount 1`/`sh:maxCount 1`). No fourth arrow appears — `pod.ttl` defines no other property on this class.
- **37b** — `ServiceTag` is drawn green, the "concrete but hidden" swatch: it is concrete (no `pod:abstract` annotation in `pod.ttl`) and the app never displays its values to the user, nor matches them in the user's own tag search (see `pod:serviceTag`'s own comment). It carries no `rdfs:subClassOf`, so no subclass line may connect it to `Pod` or any of `Pod`'s kinds.
- **37c** — no `serviceTag` arrow is drawn *into* `ServiceTag` here; that arrow belongs to `InstancePod` in `pod.png` (PNG-3), which shows `pod:ServiceTag` only as a target box.

**PNG-7 — `pod.ttl`'s `pod:Tool` hierarchy matches `images/pod-ontology/tool.png`**: The tool hierarchy has its own diagram for the same reason `tag.png` does — `pod:Tool` has no `rdfs:subClassOf` relation to `pod:Pod`, so it is not part of that hierarchy and is only pointed at from it. `Tool` (abstract, blue) sits at the top with its six concrete children `Form`, `Calendar`, `Canvas`, `Map`, `Contacts` and `Browser` (all black) below it:

- **38a** — **no arrow is drawn off `Tool` at all.** `pod.ttl` defines no property with `rdfs:domain pod:Tool`: all three tool-content properties are scoped to `pod:Form`, the one tool class with a content model. An arrow drawn off the abstract class would assert of `Calendar`, `Canvas`, `Map`, `Contacts` and `Browser` something none of the five has a data format for yet.
- **38b** — all three arrows hang off `Form`, each with `rdfs:domain pod:Form`: `formTopic` to an `xsd:anyURI` box at **1..1** (required exactly once on a live form tool — `shacl/pod-shacl.ttl`'s `:LiveToolShape`, conditioned on the class), `formGraph` to a `pod:FormGraph` box at **1..N**, and `formShape` to a `sh:NodeShape` box at 0..N. OWL/SHACL sets no maximum on `formGraph` — the real upper bound, one graph per pod member each with a distinct claimant, is YAML-8, not something this diagram draws.
- **38c** — `Calendar`, `Canvas`, `Map`, `Contacts` and `Browser` carry no arrows: `pod.ttl` defines no property with any of them as its domain, and they inherit none, since `Tool` carries none either. All five are drawn all the same, so the extension point reads as plural rather than as a `Form` that happens to be abstract's only child.
- **38d** — the hierarchy `Tool` → `Form`/`Calendar`/`Canvas`/`Map`/`Contacts`/`Browser` matches `pod.ttl`'s actual `rdfs:subClassOf` relationships by class local name. The six leaves are **not** `owl:disjointWith` one another (unlike `pod:MemberGraph`/`pod:FormGraph`, and unlike `pod:TemplatePod`/`pod:InstancePod`), so no disjointness is drawn between them.
- **38e** — the class-label colors match `pod.ttl`'s `pod:abstract` annotations: `Tool` blue (`pod:abstract true`), the six leaves black (none carries it). The Key lists exactly the swatches this diagram uses — two here, since nothing in it is the green "concrete but hidden" case.
- **38f** — no `tool` or `declaresTool` arrow is drawn *into* `Tool` here; both belong to `pod.png` (PNG-3), which shows `pod:Tool` only as a target box.

**PNG-8 — `images/representative-pods.png` matches example usage**: This diagram illustrates seven representative pods, drawn in the same pod-box style as the 12 example diagrams (PNG-1): a bold black name, the category tags as a green `#<prefLabel>` line (PNG-1f), and any user tags as grey `#<tag>` text. Unlike them, it is not a persistent view, so it carries no view header and no group headers, and its boxes carry no `{NN}` label, six of the seven being generic rather than real example pods.

Its legend is the same six titled boxes the 12 example diagrams carry, stacked in this order: "UI View", "Pod name", "Category tags", "Claimant", "Other", "Members". The identical block appears in 13 diagrams, so a change to it has to be applied thirteen times by hand, the same fan-out PNG-11 warns about. Box by box:

- **UI View** holds a green `#Heading` with a grey connector, standing for a group header (PNG-1i). This diagram draws none; the box is kept so that all 13 legends stay identical.
- **Pod name** holds the three-line pod-box formula: bold black "Pod name", green "#Category tag(s)", grey "#User tag(s)".
- **Category tags** holds four fill-color swatches in a 2×2 grid, labeled inside each swatch: "Person" (tan) and "Mix" (light-blue-to-tan gradient) on top, "Org" (light blue) and "None" (purple/lavender) below, following PNG-1h's rule over the pod's category tags. "Mix" is a pod whose tags reach both top concepts. "None" is a pod carrying no `pod:categoryTag`, a display convention and not a class.
- **Claimant** holds two claim-fill swatches, a green "Other" (claimed by someone other than the self) and a dashed "Self" (claimed by the user). Claim fill is a two-state fact; there is no third "Delegate" fill (see PNG-10 and PNG-11).
- **Other** holds a document icon labeled "Attachment", a pod attachment drawn in a pod box (filled green when it is a credential signed by its issuer, per PNG-10, and never counted as a graph shape, per PNG-1c), and a square labeled "Form", the kind of tool a square stands for.
- **Members** holds a circle labeled "Human" and an octagon labeled "Service".

`images/folder-mapping.png` is the one exception and keeps a single "key" box of its own. It draws folders rather than pods' graphs, so its key holds just the two folder swatches, "Folder that is a pod (category tag under Person)" and "Folder not associated with a pod" (see PNG-9).

**Shape**, not fill, is what distinguishes a `pod:member` graph from a tool's own graph: a square for a tool's graph, a circle for a member whose `pod:subject` is a `p:Person`, and an octagon for a member whose `pod:subject` is an `s:Service` of any kind. Fill is layered on independently and shows only who claimed that graph, so any shape can carry either fill. Every shape carries an explicit name label (e.g. "Bob", "Self", "BHS") baked into it, which is how a viewer learns who is involved; a pod box does not display its subject, which is derivable from its shapes (see README's Representative Pods section). Pod box borders are uniform: a pod's member count is never stored and is not drawn. The seven boxes, top to bottom:

  - `Medical Appointment`: tan/Person fill, green `#Medical Appointment`. Two squares "Med. Appt mt.", one green/Other and one white/Self, both about the same topic, showing that a single topic can be claimed more than once: a tool holds one graph per member, capped at the pod's own member count (YAML-8), reached here at two. Plus two circles, "Self" (white) and "Bob" (green). Two members.
  - `Friends`: purple/None fill, no category tag and no user tag, so no tag line at all. Two circles: a green "Fred" and a white "Self" (the pod's required `member` entry, per YAML-6). No squares. Two members.
  - `Employee`: light-blue/Organization fill, green `#Employees` (`podcat:Employees`, which reaches `podcat:Organization`). One white "Self" circle, no squares. One member.
  - `Bob Johnson`: tan/Person fill, green `#Others`. Four circles, two white/Self and two green/Other, covering all four self/other combinations of `pod:subject` and `pod:claimant`. No squares. Two members.
  - `Boston Hub Society`: tan/Person fill, green `#Boston Hub Society`. The tag is an extension concept (`pod-category-ext/boston-hub-society.ttl`), and the tan fill applies because it reaches `podcat:Person` through its single `skos:broadMatch podcat:Groups`. One green square (BHS's own organization profile, held by a form tool), a white "Self" circle, a green "Bob" circle, and a green **octagon** "BHS" for the member whose `pod:subject` is `:BHS_Service`, an `s:ServiceProvider`, its claim attributed to the organization behind it. Illustrative, not a copy of the real pod-01. Three or more members.
  - `Ginger`: tan/Person fill, green `#Pets`, grey `#Ginger`, the diagram's one user tag. One white/Self square "Ginger" (the form tool's graph about the cat) and one white "Self" circle. One member.
  - `Kyoto Trip 2027`: tan/Person fill, green `#Trips`. The one box drawn from real example data, `pod-47`. Two circles, "Self" (white) and "Dave" (green), and two squares, both labeled "Kyoto" and both about `:Kyoto_Trip_2027`, one per claimant: white/Self (graph-69) and green/Other (graph-91). This is the diagram's worked example of a tool reaching its real upper bound of one graph per member (YAML-8). Two members.

  Each pod box shows no icon of any kind, no folder icon and no separate "note" or "chat" icon (see PNG-3's `pod:note`/`pod:chat` planned-property note, which concerns `pod.png` only), just the filled box itself. Re-verify each box's circles and squares remain a valid illustration of the properties and cardinalities described in the Pod and Graph Ontology sections of `README.md` after any change to those properties.

**PNG-9 — a pod carries no category tag if and only if it is drawn with the Custom fill**: Every pod drawn in `images/folder-mapping.png`, `representative-pods.png` and the 12 example diagrams (PNG-1h) carries a **fill** set by its category type: tan/Person, light blue/Organization, a light-blue-to-tan gradient (Mixed), or purple/None (Custom), from the top concepts its `pod:categoryTag` values reach. The Custom case is the one this check pins down: a pod is drawn purple **exactly when** its pod-databook carries no `tpod.categoryTag` value at all, the Custom category being identified by that absence and nothing else. A pod carrying any category tag is never purple, and a pod carrying none is never anything else. In `folder-mapping.png` the fill sits on the folder icon itself. That diagram pictures the repo's development scaffolding rather than a pod as the app holds it, which is also why it draws a Pod DataBook file, unlike the 12 example diagrams. It draws `example/Pods/` as a white folder holding two sibling pod folders, "Bob Johnson" and "Fred Flintstone" (both tag `podcat:Others`, so both tan). Fred Flintstone is expanded to show its DataBook, note file and `_pod-attachments` folder, with three attachments A, B and C. Only a folder that is a pod carries fill at all: `Pods` and `_pod-attachments` stay white, and the key names that distinction, the tan/white split being exactly the pod/not-a-pod test. Every folder name is black. The diagram carries no Custom or Organization pod, so its key lists only the tan swatch, labeled "Folder that is a pod (category tag under Person)". That is the rule for this diagram's key generally, matching PNG-3's for `pod.png`: the key lists exactly the swatches the drawing actually uses, so a swatch whose case is not drawn comes out rather than standing as an unexercised entry. This is a visual check (no automated pixel/OCR comparison), but the script below computes, for every real pod, its category tags and their labels, its category type, and the fill the rule calls for, for direct cross-reference against whichever diagram box or folder is being checked. It reports `UNRESOLVED` for a tag it cannot follow to `podcat:Person` or `podcat:Organization`. Run:

```python
import glob, re, yaml

# Concept CURIE -> prefLabel, and -> the one concept it links upward to: its
# skos:broader within a scheme, or for a category extension's concept its
# skos:broadMatch into the core taxonomy. Read from pod-categories.ttl and
# every category extension bundle, each concept's block being written
# prefLabel-first.
NAME = r'([A-Za-z]+(?:\\\(org\\\))?)'
pattern = re.compile(
    r'(\w+):' + NAME + r' rdf:type skos:Concept\s*;\s*'
    r'skos:prefLabel "([^"]+)"@en\s*;\s*'
    r'(?:skos:(?:broader|broadMatch) (\w+):' + NAME + r'\s*;\s*)?'
)
unescape = lambda s: s.replace('\\(', '(').replace('\\)', ')')
labels, up = {}, {}
for path in ['pod-categories.ttl'] + sorted(glob.glob('pod-category-ext/*.ttl')):
    for m in pattern.finditer(open(path, encoding='utf-8').read()):
        curie = f'{m.group(1)}:{unescape(m.group(2))}'
        labels[curie] = m.group(3)
        if m.group(4):
            up[curie] = f'{m.group(4)}:{unescape(m.group(5))}'

TOPS = {'podcat:Person': 'Person', 'podcat:Organization': 'Organization'}

def top_of(curie):
    seen = set()
    while curie not in TOPS:
        if curie in seen or curie not in up:
            return None
        seen.add(curie)
        curie = up[curie]
    return TOPS[curie]

FILL = {'Person': 'tan/Person', 'Organization': 'light-blue/Organization',
        'Mixed': 'blue-to-tan gradient/Mixed', 'Custom': 'purple/None'}

def as_list(v):
    return v if isinstance(v, list) else ([v] if v else [])

for path in sorted(glob.glob('example/Pods/**/*.databook.md', recursive=True)):
    if 'under-development' in path.split('/'):
        continue
    text = open(path, encoding='utf-8').read()
    m = re.match(r'^---\n(.*?)\n---', text, re.DOTALL)
    fm = yaml.safe_load(m.group(1)) if m else None
    if not fm:
        continue
    tpod = fm.get('tpod', {}) or {}
    tags = as_list(tpod.get('categoryTag'))   # zero or more per pod
    title = fm.get('title')
    tops = {top_of(t) for t in tags}
    if None in tops:
        bad = [t for t in tags if top_of(t) is None]
        print(f'UNRESOLVED: {path} has a category tag that reaches no top concept: {bad}')
        continue
    if not tags:
        kind = 'Custom'                       # no category tag at all, and only then
    else:
        kind = tops.pop() if len(tops) == 1 else 'Mixed'
    shown = ', '.join(tags) or '(none)'
    label = ' '.join('#' + labels.get(t, '???') for t in tags) or '-'
    print(f'{title:35s} tags={shown:50s} label={label:40s} fill={FILL[kind]}')
```

If a diagram box's fill doesn't match this script's output for the corresponding pod, update `tpod.categoryTag` only if the *data* is actually wrong. Otherwise the box is what needs redrawing. No diagram colors a pod's name: every name is black, the category tags being shown on their own green line (PNG-1f), which the script's `label` column gives.

**PNG-10 — a graph shape's claim-fill color matches its graph's own `claimant`**: PNG-1c settles a pod box's graph *shapes* (a circle per `member` entry, a square per tool graph) and explicitly defers their **fill** to PNG-8's legend, as "a separate, independent fact showing who claimed that graph". PNG-1h then checks only the *pod box*'s own Person/Organization/Custom fill and its name-text color. So the claim-fill of the circles and squares themselves — the one color that encodes `pod:claimant` — was defined but verified nowhere, in any of the 12 diagrams. This check closes that gap. The rule, per PNG-8's legend, is a three-way partition of every drawn graph shape, decided entirely by that graph's own `claimant`:

- **outlined/unfilled (Self)** — `claimant: ":Self"`.
- **green (Other)** — every other claimant: another `p:Person`, an `o:Organization`, or any `service:Service`, whether it is an `s:AgentService` leaf or an `s:ServiceProvider`, and whether the graph is a `member` or a tool graph.

- **Signed credential attachments** — the one non-graph shape the rule covers. A credential kept as a pod attachment (a JSON file in the pod's `_pod-attachments` folder carrying an `issuer`) is drawn as a small document icon, filled green, since its issuer signed it and a signature is a claim. The script counts one expected green shape per such file. A copied credential counts in each pod that holds a copy, since each copy is still the issuer's.

Claim fill is therefore a two-state fact — self or not-self — and nothing more. There is no third "Delegate" fill: a service's claims are green like any other non-self party's, and *who* a member is (human vs. service) is carried by the member shape instead, not by its color. That keeps the two facts orthogonal, so a shape's fill can be read without knowing anything about its claimant's type.

The palette values are exact, so this is mechanically checkable by sampling the PNGs directly rather than by eye. Only the two *filled* states can be counted — an unfilled Self shape is the same white as the page background — but that is enough for any single miscolor, since it always moves a shape between buckets and so changes a filled count. The one blind spot is a pair of offsetting errors inside the same diagram — one shape wrongly unfilled and another wrongly filled the same color — which leaves the totals intact; the counts are small enough that such a pair is worth a glance at the diagram when it is edited. (This is exactly how `companies.png`'s `Arca` `[96]` circle was caught: claimed by `:Arca_Backup`, it was drawn unfilled, leaving `companies.png` with 0 green shapes where the data calls for 1.) Legend swatches are excluded by area — a real circle or square is ~96×96px, a swatch far smaller. Each diagram is matched to its pods by the script's `DIAGRAM` table, which records, by pod name, the pods each of the 12 diagrams draws; `people.png` and `people2.png` together draw one set of pods, so they are summed and compared jointly. The table follows the diagrams as drawn: when a diagram is redrawn, update its row. A pod in no row is reported as undrawn. Requires `pip install pillow`. Run:

```python
import re, glob, os, yaml
from collections import Counter
from PIL import Image

PAL = {(220, 250, 221): 'green', (235, 235, 235): 'gray'}
MIN_AREA = 2000   # a real graph shape is ~96x96px; legend swatches are far smaller

def frontmatter(path):
    text = open(path, encoding='utf-8').read()
    m = re.match(r'^---\n(.*?)\n---', text, re.DOTALL)
    return (yaml.safe_load(m.group(1)) if m else None), text

def filled_shapes(path):
    """Count connected regions of each exact palette fill, ignoring legend swatches."""
    im = Image.open(path).convert('RGB')
    W, H = im.size
    px = im.load()
    seen = [[False] * H for _ in range(W)]
    counts = Counter()
    for x in range(W):
        for y in range(H):
            if seen[x][y] or PAL.get(px[x, y]) is None:
                continue
            colour = PAL[px[x, y]]
            stack, area = [(x, y)], 0
            seen[x][y] = True
            while stack:
                a, b = stack.pop()
                area += 1
                for da, db in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    m, n = a + da, b + db
                    if 0 <= m < W and 0 <= n < H and not seen[m][n] and PAL.get(px[m, n]) == colour:
                        seen[m][n] = True
                        stack.append((m, n))
            if area >= MIN_AREA:
                counts[colour] += 1
    return counts

# The pods each diagram draws, by pod name (its folder under example/Pods/).
# people.png/people2.png draw one set of pods between them.
DIAGRAM = {
    'groups':      ['Boston Hub Society', 'Chestnut Hill Village Association'],
    'companies':   ['ATT', 'Arca', 'Facenook', 'Google', 'PRIVO'],
    'finances':    ['Citibank'],
    'gov-federal': ['Passport', 'SSN'],
    'gov-state':   ['Birth Certificate', 'Drivers License'],
    'home':        ['Boston', 'Paradise'],
    'pets':        ['Ginger', 'Ginger Care & Feeding', 'Ginger Medical'],
    'things':      ['RAV4', 'Things'],
    'travel':      ['Hilton', 'Kyoto Trip 2027'],
    'work':        ['Acme', 'Alice Walker', 'Paula Walker'],
    'people':      ['Bob Johnson', 'Fred Flintstone', 'Jane Starostina',
                    'Medical Appointment', 'Sophia Health & Wellness', 'Sophia Walker'],
}
SPLIT = {'people': ['people', 'people2']}   # pod sets drawn across more than one diagram
DRAWN_IN = {pod: d for d, pods in DIAGRAM.items() for pod in pods}

expected = Counter()
for f in glob.glob('example/Pods/**/*.databook.md', recursive=True):
    if 'under-development' in f.split('/'):
        continue
    fmatter, _ = frontmatter(f)
    if not fmatter:
        continue
    pod = os.path.basename(os.path.dirname(f))
    branch = DRAWN_IN.get(pod)
    if branch is None:
        print(f'UNDRAWN {f}: pod {pod!r} is in no row of DIAGRAM')
        continue
    tpod = fmatter.get('tpod', {}) or {}
    # Every graph the pod links: its tpod.member entries, plus the graphs nested
    # under each tpod.tool. A tool's graphs sit one level deeper than a member
    # entry (the tool states its own formTopic once, above them), so they have
    # to be walked into — they are drawn as squares and carry a claimant of
    # their own exactly as member circles do.
    entries = tpod.get('member') or []
    entries = list(entries) if isinstance(entries, list) else [entries]
    tools = tpod.get('tool') or []
    for t in (tools if isinstance(tools, list) else [tools]):
        if not isinstance(t, dict):
            continue
        gs = t.get('graph') or []
        entries += gs if isinstance(gs, list) else [gs]
    for e in entries:
        if not isinstance(e, dict):
            continue
        if e.get('claimant') == ':Self':
            continue                      # unfilled — indistinguishable from background
        expected[(branch, 'green')] += 1
    # A signed credential attachment is drawn green too: its issuer claimed it.
    att_dir = os.path.join(os.path.dirname(f), '_pod-attachments')
    for a in glob.glob(os.path.join(att_dir, '*.json')):
        try:
            import json
            if json.load(open(a, encoding='utf-8')).get('issuer'):
                expected[(branch, 'green')] += 1
        except (ValueError, AttributeError):
            pass

violations = 0
for branch in sorted(DIAGRAM):
    pngs = SPLIT.get(branch, [branch])
    actual = Counter()
    for name in pngs:
        actual += filled_shapes(f'example/images/{name}.png')
    for colour in ('green', 'gray'):
        if actual[colour] != expected[(branch, colour)]:
            violations += 1
            print(f'VIOLATION {"/".join(n + ".png" for n in pngs)}: '
                  f'{actual[colour]} {colour} shape(s) drawn, data calls for '
                  f'{expected[(branch, colour)]}')
print('Every diagram\'s claim-fill colors match their graphs\' own claimants.'
      if violations == 0 else f'{violations} violation(s) found.')
```

If a violation is found, the diagram is the authoritative side for *which pods and shapes exist* (PNG-1), but the DataBook is authoritative for *who claimed a graph* — a `claimant` is a fact about the data, not a drawing choice. So recolor the shape to match its graph's own `claimant` under the three-way rule above. A count that is short by one green usually means a non-`:Self`-claimed shape was left unfilled; a count long by one usually means a `:Self`-claimed shape was filled. The check reports counts rather than naming the offending shape, since matching a specific circle to a specific graph number would require reading the diagram's own `[NN]` labels; with per-diagram counts the candidates are few enough to spot by eye.

**PNG-11 — no diagram still carries the retired "Delegate" legend swatch**: The 12 example diagrams plus `images/representative-pods.png` each carry their own copy of the legend, so a change to it has to be applied thirteen times by hand. (`images/folder-mapping.png` is also scanned below, but carries a key of its own, two folder swatches, rather than this legend.) That legend is six titled boxes, "UI View", "Pod name", "Category tags", "Claimant", "Other" and "Members" (see PNG-8 for the full box-by-box contents). The ones that matter here are **Claimant**, holding two claim-fill swatches (green "Other", dashed "Self"), **Other**, holding the "Attachment" document icon and the square "Form", and **Members**, holding a circle "Human" and an octagon "Service"; it no longer holds the gray "Delegate" swatch that a third claim-fill state once needed (see PNG-8 and PNG-10 — claim fill is now a two-state self/not-self fact, and a member's identity type is carried by shape instead). A diagram left on the older key is mechanically detectable, because that swatch is the only place a filled `(235, 235, 235)` block of any size appears: the current legend has no gray fill, its grey `#User tag(s)` text and `#Heading` connector being a darker grey and thin, and the incidental `(235, 235, 235)` in these PNGs is antialiasing a few dozen pixels in size, far below the threshold below. This catches the stale-legend case that PNG-10 cannot — PNG-10 compares fills against the DataBooks and so passes happily on a diagram whose *shapes* are all correct but whose *legend* still advertises a retired state. Requires `pip install pillow`. Run:

```python
from PIL import Image
import os

GRAY = (235, 235, 235)      # the retired "Delegate" swatch fill
MIN_AREA = 200              # far above antialiasing, far below a real swatch (~1150px)

KEYED = ['example/images/' + n + '.png' for n in
         ('people', 'people2', 'work', 'companies', 'finances', 'gov-state', 'gov-federal',
          'home', 'things', 'groups', 'pets', 'travel')] + \
        ['images/representative-pods.png', 'images/folder-mapping.png']

def gray_blocks(path):
    im = Image.open(path).convert('RGB')
    W, H = im.size
    px = im.load()
    seen = [[False] * H for _ in range(W)]
    found = []
    for x in range(W):
        for y in range(H):
            if seen[x][y] or px[x, y] != GRAY:
                continue
            stack, area, xs, ys = [(x, y)], 0, [], []
            seen[x][y] = True
            while stack:
                a, b = stack.pop()
                area += 1
                xs.append(a)
                ys.append(b)
                for da, db in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    m, n = a + da, b + db
                    if 0 <= m < W and 0 <= n < H and not seen[m][n] and px[m, n] == GRAY:
                        seen[m][n] = True
                        stack.append((m, n))
            if area >= MIN_AREA:
                found.append((area, min(xs), min(ys), max(xs) - min(xs) + 1, max(ys) - min(ys) + 1))
    return found

violations = 0
for path in KEYED:
    if not os.path.exists(path):
        violations += 1
        print(f'VIOLATION {path}: keyed diagram missing from disk')
        continue
    blocks = gray_blocks(path)
    if blocks:
        violations += 1
        where = ', '.join(f'{a}px {w}x{h} at ({x},{y})' for a, x, y, w, h in blocks)
        print(f'VIOLATION {path}: gray {GRAY} region(s) present — {where}')
print('No diagram carries the retired Delegate swatch.' if violations == 0
      else f'{violations} violation(s) found.')
```

If a violation is found, the diagram is still on an older legend and needs it replaced with the current six-box block (PNG-8): drop the gray "Delegate" swatch, and make sure the square swatch sits in the "Other" box labeled "Form" while the "Members" box's shape swatches read "Human" (circle) and "Service" (octagon) rather than a single "Member" circle. A gray region far from the legend column is the other possibility — a graph shape still filled with the retired Delegate color, which PNG-10 will also flag as a count mismatch. Note the limit: this detects the *absence* of the retired swatch, not the *presence* of the correct new one, since reading swatch labels and telling a circle from an octagon would need text and shape recognition rather than exact-color sampling. The circle/octagon distinction stays a visual check for the same reason (see PNG-1c).

## TTL — triple checks

These read a `.ttl` file and ask a question about **triples**, so every one parses with `rdflib` rather than regex. See [Which checks use `rdflib`](#which-checks-use-rdflib) above for why that matters and why no other kind may follow suit.


**TTL-1 — No orphan Persons**: Every `persona:Person` individual other than `:Self` must be reachable via `BFO_0000115` (has member part) from a Social Network individual linked to another `persona:Person` via `persona:hasSocialNetwork`. `:Self` is always the root and needs no incoming link. Since graphs are embedded graph sections across every pod-databook under `example/Pods/**`, this check's scope is the merged whole-example dump (example.md's "Merged whole-example dump"), which spans every embedded graph. **Exception**: a `persona:Person` referenced only via a professional/service-designation property (`medicalappointments:hasPrimaryCarePhysician` is the only one so far) rather than social-network membership is exempt — it represents a service relationship (e.g. a physician), not a social connection, so it has no social network to be reachable from. Example: `:Jane_Starostina`, Sophia Walker's primary care physician — introduced as a `persona:Person` in graph #25 and reached by that property from graph #26. The exempting properties are listed in `DESIGNATION` in the script below, and that list is the whole of what keeps the exemption honest: a property minted later and left out of it will surface its subject as an orphan, which is the intended failure rather than a false positive. Run:

```python
import subprocess, sys
import rdflib

TPOD = rdflib.Namespace('http://www.example.org/tpod#')
PER  = rdflib.URIRef('http://mee.foundation/ontologies/persona#Person')
SN   = rdflib.URIRef('http://mee.foundation/ontologies/persona#hasSocialNetwork')
PART = rdflib.URIRef('http://purl.obolibrary.org/obo/BFO_0000115')

# Professional/service-designation properties: a Person reached ONLY through one
# of these is exempt (see the Exception above). Add to this list when a new such
# property is minted -- that is the whole of what keeps the exemption honest.
DESIGNATION = [
    rdflib.URIRef('http://mee.foundation/ontologies/medical-appointments#hasPrimaryCarePhysician'),
]

dump = subprocess.run([sys.executable, 'helpers/extract-all.py'],
                      capture_output=True, text=True, check=True).stdout
g = rdflib.Graph(); g.parse(data=dump, format='turtle')

name    = lambda u: str(u).split('#')[-1]
persons = {s for s in g.subjects(rdflib.RDF.type, PER)}
reached = {m for p in persons for n in g.objects(p, SN) for m in g.objects(n, PART)}
exempt  = {o for prop in DESIGNATION for o in g.objects(None, prop)}

orphans = sorted(name(p) for p in persons - reached - exempt - {TPOD.Self})
if orphans:
    print(f"ORPHAN Person(s), in no social network: {', '.join(orphans)}")
    print("  Fix: add each to a Social Network individual via BFO_0000115 in the graph")
    print("  that introduces them, or -- if the reference is a service relationship --")
    print("  add its designation property to DESIGNATION above.")
else:
    print(f"No orphan Persons: {len(persons)} persona:Person individuals, "
          f"{len(exempt)} exempt by designation.")
```

This is the one check script that uses `rdflib` rather than regex/YAML parsing like the rest: the question is genuine graph reachability over a merged dump whose `BFO_0000115` values are written as multi-object lists, which a regex would read wrong. `rdflib` is already a dependency of `helpers/draw.py` and `helpers/validate.py`, so this adds nothing new to install.

**TTL-2 — IRI roots: `mee.foundation/ontologies` for foundational files, `www.example.org` for example data**: Every foundational ontology and SHACL shapes file — `persona.ttl`, `pod.ttl`, `pod-categories.ttl`, `pod-category-templates.ttl`, `organization.ttl`, `service.ttl`, every `*-shacl.ttl` companion (each living in a `shacl/` subfolder directly below the ontology file it validates — the foundational ones under the repo-root `shacl/`, each `other/*.ttl` peer ontology's own under `other/shacl/`, one recursive glob covers all of them), and every `other/*.ttl` peer ontology (`other/pets.ttl`, `other/vehicles.ttl`, `other/identity-documents.ttl`, globbed the same way) — must declare its `owl:Ontology` IRI under `http://mee.foundation/ontologies/`. There is no separate canonical category/pod DataBook tree to check — the canonical tree's IRI roots are covered by `pod-categories.ttl`/`pod-category-templates.ttl` themselves. Every DataBook under `example/Pods/` (excluding `under-development/`) represents Alice's own example instance data, so both its own `id:` and every `tpod.member[]`/`tpod.tool[].graph[].id` value it carries must be grounded under `http://www.example.org/` — `https://` is deliberately rejected here, not just accepted alongside it, since every identifier in the example data (pod ids and graph ids alike) was standardized on the plain `http://` scheme for consistency; a stray `https://` is exactly the kind of drift this check exists to catch. Run:

```python
import os, re, glob, yaml
import rdflib

FOUNDATIONAL_TTL = [
    'persona.ttl', 'pod.ttl', 'pod-categories.ttl', 'pod-category-templates.ttl',
    'organization.ttl', 'service.ttl',
] + sorted(glob.glob('**/shacl/*.ttl', recursive=True)) + sorted(glob.glob('other/*.ttl')) \
  + sorted(glob.glob('persona-ext/*.ttl')) + sorted(glob.glob('pod-category-ext/*.ttl'))
# Every *-shacl.ttl companion lives in a shacl/ subfolder directly below the
# ontology file it validates, so the recursive **/shacl/*.ttl glob covers all of
# them, present and future, with no need to list each by name.

errors = 0
for path in FOUNDATIONAL_TTL:
    if not os.path.exists(path):
        continue
    g = rdflib.Graph(); g.parse(path, format='turtle')
    iris = [s for s in g.subjects(rdflib.RDF.type, rdflib.OWL.Ontology)]
    if not iris:
        print(f'NO owl:Ontology IRI FOUND: {path}')
        errors += 1
        continue
    for iri in iris:
        if not str(iri).startswith('http://mee.foundation/ontologies/'):
            print(f'WRONG ROOT (expected mee.foundation): {path} -> {iri}')
            errors += 1

def frontmatter(path):
    text = open(path, encoding='utf-8').read()
    m = re.match(r'^---\n(.*?)\n---', text, re.DOTALL)
    return yaml.safe_load(m.group(1)) if m else None

def as_list(v):
    return [] if v is None else (v if isinstance(v, list) else [v])

def check_pod_tree_id_roots(pattern, expected_prefixes):
    global errors
    for path in sorted(glob.glob(pattern, recursive=True)):
        if 'under-development' in path.split(os.sep):
            continue
        fm = frontmatter(path)
        if not fm:
            continue
        iri = fm.get('id')
        if iri and not any(str(iri).startswith(p) for p in expected_prefixes):
            print(f'WRONG ID ROOT: {path} -> {iri}')
            errors += 1
        tpod = fm.get('tpod') or {}
        entries = [e for e in as_list(tpod.get('member')) if isinstance(e, dict)]
        for tool in as_list(tpod.get('tool')):          # a tool's own graph ids
            if isinstance(tool, dict):                # live one level down, in
                entries += [g for g in as_list(tool.get('graph'))  # its own
                            if isinstance(g, dict)]   # graph list.
        for graph in entries:
            tid = graph.get('id')
            if tid and not any(str(tid).startswith(p) for p in expected_prefixes):
                print(f'WRONG GRAPH ID ROOT: {path} -> {tid}')
                errors += 1

check_pod_tree_id_roots('example/Pods/**/*.databook.md', ['http://www.example.org/'])

print('OK — no IRI-root violations found.' if errors == 0 else f'{errors} violation(s) found.')
```

If a violation is found, rename the offending file's `owl:Ontology`/`id:` IRI to the correct root, and update every catalog entry and cross-reference that pointed at the old IRI to match (see FS-1's validation commands, which also hardcode these IRIs).

**TTL-3 — `pod:shape`'s declared shape must resolve to an `rdf:type` actually asserted in the graph's own embedded Turtle body**: `pod:shape` (`pod.ttl`) is a real `owl:AnnotationProperty` (domain `pod:Graph`, range `sh:NodeShape`, cardinality 0..N), synthesized into RDF from each `tpod.member[]`/`tpod.tool[].graph[].shape` YAML value by `helpers/yaml-to-rdf.py`. But SHACL validation of a templated graph never actually reads this synthesized triple — each per-template shape (e.g. `:PassportShape`) fires purely via its own `sh:targetClass`, matching whatever `rdf:type` is asserted directly in the graph's body (e.g. `:Alice_US_Passport rdf:type identitydocuments:Passport`), completely independent of `shape:`. So nothing else cross-checks that a graph's declared `shape:` shape's own `sh:targetClass` actually names a class asserted on an individual in its own body — a typo'd or stale `shape:` value would go undetected, silently decoupled from what SHACL is actually validating. This is not itself an OWL/SHACL-expressible constraint (same reasoning as YAML-4/YAML-6/YAML-7/YAML-8 — it requires dereferencing the graph's own embedded Turtle content, not just its YAML frontmatter), so it's checked here instead. For every pod-databook under `example/Pods/` (excluding `under-development/`) with a `tpod.member[]`/`tpod.tool[].graph[].shape` value, resolve that shape CURIE to its own `sh:targetClass` (scanning `shacl/persona-shacl.ttl`/`shacl/contactinfo-shacl.ttl` and every `other/shacl/`, `persona-ext/shacl/`, and `pod-category-ext/shacl/` shapes file for the matching shape — the recursive `**/shacl/*.ttl` glob TTL-2 already describes, and the same scan TTL-4 runs), then verify that same graph's own embedded Turtle body asserts `rdf:type` (directly, on some individual) to that resolved class. **Exempt**: `pshapes:ContactInfoShape` and `bhsshapes:MemberShape` — per `helpers/validate.py`'s own module docstring, these are the broad, class-wide shapes (`sh:targetClass persona:Person`) that `helpers/validate.py` re-targets, at actual validation time, at only the *substantive* `persona:Person` individual(s) present in a graph, precisely because it's legitimate for a `pod:member`-list graph (required to carry this shape unconditionally, per TTL-7) to contain none at all — e.g. graph-01 (`Boston Hub Society.databook.md`, whose member shape is `bhsshapes:MemberShape` rather than `ContactInfoShape` — the exemption covers both for exactly the same reason) is the society's own member stub, typing `:BHS_Service` as `service:ServiceProvider` and `:BHS` as `o:Organization`, never `persona:Person`; graph-27 (`Citibank.databook.md`) is the bank's own member stub, carrying its name, website, and institutional self-description, typing `:Citibank_Service`/`:Citibank` the same way; and graph-96 (`Arca.databook.md`) is a backup service's own member stub, typing `:Arca_Backup` as `service:ArcaBackup` and `:Arca` as `o:Organization` — both correctly, vacuously satisfy `ContactInfoShape` in real SHACL validation with zero `persona:Person` individuals present. Every other shape (e.g. `idocshapes:PassportShape`, `bankingshapes:DebitCardShape`) targets a narrow, specific document/account class that a declaring graph always does instantiate for real (e.g. the real Citibank debit-card graph asserts `rdf:type cco:ent00000051` directly, alongside `banking:DebitCard`), so no other exemption is needed. Run:

```python
import yaml, glob
import rdflib
from databook_graphs import as_list, split_frontmatter, extract_graph_block

SH = rdflib.Namespace('http://www.w3.org/ns/shacl#')

def read(path):
    return open(path, encoding='utf-8').read()

# --- shape CURIE -> sh:targetClass, scanned across every file that can define a
# shape under a given prefix. The prefix is the CURIE the *consumer* uses (the
# one pod-category-templates.ttl and the YAML write); a shapes file names its own shapes
# under a bare ':' base, so it cannot supply that prefix itself.
SHAPES_FILES = {
    'pshapes': ['shacl/persona-shacl.ttl', 'shacl/contactinfo-shacl.ttl'],
    'petshapes': ['other/shacl/pets-shacl.ttl'],
    'vehicleshapes': ['other/shacl/vehicles-shacl.ttl'],
    'idocshapes': ['other/shacl/identity-documents-shacl.ttl'],
    'mashapes': ['other/shacl/medical-appointments-shacl.ttl'],
    'sashapes': ['other/shacl/service-accounts-shacl.ttl'],
    'bankingshapes': ['other/shacl/banking-shacl.ttl'],
    'residenceshapes': ['other/shacl/residences-shacl.ttl'],
    'itineraryshapes': ['other/shacl/itineraries-shacl.ttl'],
    'oshapes': ['shacl/organization-shacl.ttl'],
    'educationshapes': ['other/shacl/education-shacl.ttl'],
    'dpshapes': ['persona-ext/shacl/directory-profile-shacl.ttl'],
    'bhsshapes': ['pod-category-ext/shacl/boston-hub-society-shacl.ttl'],
}
target_class, target_curie = {}, {}
for prefix, paths in SHAPES_FILES.items():
    for path in paths:
        g = rdflib.Graph(); g.parse(path, format='turtle')
        for s, _, o in g.triples((None, SH.targetClass, None)):
            key = f"{prefix}:{str(s).split('#')[-1]}"
            target_class[key] = o                                  # full IRI, for comparison
            target_curie[key] = g.namespace_manager.normalizeUri(o)  # CURIE, for messages

def load(path):
    fm_text, _, body = split_frontmatter(read(path))
    return yaml.safe_load(fm_text), body

violations = 0
for f in sorted(glob.glob('example/Pods/**/*.databook.md', recursive=True)):
    if 'under-development' in f.split('/'):
        continue
    fm, body = load(f)
    if not fm:
        continue
    tpod = fm.get('tpod') or {}
    graphs = as_list(tpod.get('member'))
    for tool in as_list(tpod.get('tool')):
        graphs += as_list(tool.get('graph')) if isinstance(tool, dict) else []
    for g_entry in graphs:
        if not isinstance(g_entry, dict) or not g_entry.get('shape'):
            continue
        gid = g_entry['id']
        types = None   # rdf:type objects asserted in this graph's own block
        for shape in as_list(g_entry['shape']):
            # Broad, vacuously-satisfiable shape exemption — see prose above.
            # Both target persona:Person class-wide, so helpers/validate.py
            # re-targets them at substantive persona:Person individuals only,
            # and a member graph containing none (a society's or bank's own
            # member stub) conforms with nothing to check.
            if shape in ('pshapes:ContactInfoShape', 'bhsshapes:MemberShape'):
                continue
            resolved = target_class.get(shape)
            if resolved is None:
                violations += 1
                print(f"VIOLATION {f}: graph {gid} declares shape {shape!r}, no sh:targetClass found for it")
                continue
            if types is None:
                block = extract_graph_block(body, f"{gid}#graph")
                if block is None:
                    print(f'VIOLATION {f}: no turtle block found for {gid} (declares shape {shape!r})')
                    violations += 1
                    break
                # Each graph is self-contained, so its own block parses alone.
                gg = rdflib.Graph(); gg.parse(data='\n'.join(block), format='turtle')
                types = set(gg.objects(None, rdflib.RDF.type))
            if resolved not in types:
                violations += 1
                print(f"VIOLATION {f}: graph {gid} declares shape {shape!r} (resolves to "
                      f"{target_curie[shape]!r}) but no individual in its own turtle block "
                      f"is asserted rdf:type {target_curie[shape]!r}")
print('All shape-declaring graphs assert a matching rdf:type.'
      if violations == 0 else f'{violations} violation(s) found.')
```

If a violation is found: fix whichever side is wrong — either the `shape:` YAML value (if the graph's own asserted `rdf:type` is correct and `template:` names the wrong shape), or the body's `rdf:type` (if `template:` reflects the intended classification and the body was never updated to match).

**TTL-4 — a `member` graph's `shape:` value, and a declared tool's graph's, must be among the shapes its category tags' templates declare**: TTL-3 only compares a graph's `shape:` value against its own body content — this check goes one level higher, comparing it against what the pod's category tags declare as authoritative. For every pod-databook under `example/Pods/` (excluding `under-development/`), `tpod.categoryTag` is read as a list (zero or more values), and each tag is looked up by the reverse lookup `?tc pod:category X` (README's Lazy Instantiation pattern) among the `pod:TemplatePod` individuals of `pod-category-templates.ttl` and every category extension bundle under `pod-category-ext/`. A pod carrying no category tag is looked up instead against `ctpl:UserDefinedTemplatePod`, the one template carrying no `pod:category`, which is what such a pod takes its member baseline from. The templates reached are pooled: every `tpod.member`-list graph carrying a `shape:` value must have that value among the union of their `pod:memberShape` values; and, **only when at least one of them declares a tool**, every tool graph carrying a `shape:` value must be among the union of their declared tools' `pod:formShape` values — direct CURIE-set membership, since `pod:shape`'s range is `sh:NodeShape` (`pod.ttl`), the same range `pod:memberShape`/`pod:formShape` already carry, so no `sh:targetClass` resolution and no named exemptions are needed. A tool on a pod none of whose templates declares one is **not** checked against any shape at all: any pod may gain a tool no template declared, and the user picks that tool's shape themselves — from the app's full list of shapes — so no template has authority over it. A tag whose concept has no template contributes nothing — a defensive branch, not a live case, since TTL-6 and TTL-8's 39d guarantee every concept has one. This is not itself an OWL/SHACL-expressible constraint (same reasoning as YAML-4/YAML-6/YAML-7/YAML-8/TTL-3 — it requires dereferencing values across the template files, not just pod-databook YAML), so it's checked here instead. Run:

```python
import glob, re, yaml
import rdflib

POD = rdflib.Namespace('http://mee.foundation/ontologies/pod#')

# --- every TemplatePod, core and extension: the member/tool shape CURIEs it
# declares, keyed by its pod:category concept's full IRI (None for
# ctpl:UserDefinedTemplatePod, the one template with no pod:category).
# Each file is parsed on its own, so normalizeUri() renders a shape IRI with
# that file's own @prefix bindings — the CURIEs the YAML carries. rdflib reads
# a declared-tool blank node's pod:formShape directly.
templates, prefixes = {}, {}
for path in ['pod-category-templates.ttl'] + sorted(glob.glob('pod-category-ext/*.ttl')):
    g = rdflib.Graph(); g.parse(path, format='turtle')
    curie = g.namespace_manager.normalizeUri
    prefixes.update({p: str(ns) for p, ns in g.namespaces()})
    for s in g.subjects(rdflib.RDF.type, POD.TemplatePod):
        tools = list(g.objects(s, POD.declaresTool))
        entry = {
            'member': {curie(o) for o in g.objects(s, POD.memberShape)},
            # A declared tool is a blank node carrying pod:formShape; its
            # absence is exactly what says the template declares no tool.
            'tool': {curie(o) for t in tools for o in g.objects(t, POD.formShape)},
            'declares_tool': bool(tools),
        }
        cats = list(g.objects(s, POD.category))
        for cat in cats or [None]:
            templates[str(cat) if cat is not None else None] = entry

def expand(c):
    p, _, local = c.partition(':')
    return prefixes.get(p, p + ':') + local

def frontmatter(path):
    text = open(path, encoding='utf-8').read()
    m = re.match(r'^---\n(.*?)\n---', text, re.DOTALL)
    return yaml.safe_load(m.group(1)) if m else None

def as_list(v):
    return [] if v is None else (v if isinstance(v, list) else [v])

def reached_templates(tpod):
    # tpod.categoryTag is a list, zero or more per pod. Each tag reaches its own
    # template; a pod with no tag at all reaches ctpl:UserDefinedTemplatePod's
    # (keyed None). A tag whose concept has no template contributes nothing.
    tags = as_list(tpod.get('categoryTag'))
    keys = [expand(c) for c in tags] if tags else [None]
    return [templates[k] for k in keys if k in templates]

violations = 0
for path in sorted(glob.glob('example/Pods/**/*.databook.md', recursive=True)):
    if 'under-development' in path.split('/'):
        continue
    fm = frontmatter(path)
    if not fm:
        continue
    tpod = fm.get('tpod') or {}
    reached = reached_templates(tpod)
    if not reached:
        continue  # no TemplatePod for any of this pod's tags — nothing to check
    allowed = {
        'member': set().union(*(r['member'] for r in reached)),
        'tool': set().union(*(r['tool'] for r in reached)),
    }
    declares_tool = any(r['declares_tool'] for r in reached)

    def entries_for(field):
        if field == 'member':
            return [e for e in as_list(tpod.get('member')) if isinstance(e, dict)]
        return [g for t in as_list(tpod.get('tool')) if isinstance(t, dict)
                  for g in as_list(t.get('graph')) if isinstance(g, dict)]

    for field in ('member', 'tool'):
        # A tool on a pod none of whose templates declares one was added by
        # hand — the user picks its shape freely, so no template has a say.
        if field == 'tool' and not declares_tool:
            continue
        prop = 'memberShape' if field == 'member' else 'formShape'
        for entry in entries_for(field):
            gid = entry.get('id')
            for shape in as_list(entry.get('shape')):
                if not allowed[field]:
                    violations += 1
                    print(f"VIOLATION {path}: {field} graph {gid} declares shape {shape!r} "
                          f"but none of its category tags' templates has a pod:{prop} value")
                elif shape not in allowed[field]:
                    violations += 1
                    print(f"VIOLATION {path}: {field} graph {gid} declares shape {shape!r}, "
                          f"not among its category tags' templates' pod:{prop} value(s) "
                          f"{sorted(allowed[field])}")
print("All member/tool shape: values are among their category tags' templates' shapes."
      if violations == 0 else f'{violations} violation(s) found.')
```

If a violation is found: either the graph's `shape:` value is wrong (fix it to a shape one of the pod's category tags' templates declares), or the `pod:memberShape` value or the declared tool's `pod:formShape` value(s) on the corresponding template are wrong/missing (add the correct one), or — if the graph is genuinely a different kind of content than its tag's template expects — reconsider whether it belongs in `member` vs. under a tool, or whether the pod carries the right category tags.

**TTL-5 — a pod carries everything its category tags' templates require**: TTL-4 only checks a `shape:` value once one is already present — it never flags a `tpod.member`-list graph that is missing one outright, nor a declared tool that is missing from the pod altogether. This check closes both gaps, against the same templates TTL-4 reaches from the pod's `tpod.categoryTag` values (or `ctpl:UserDefinedTemplatePod`, for a pod carrying no category tag):

- **Member shapes** — every `tpod.member`-list graph must carry, among its `shape:` value(s), every `pod:memberShape` value of every template reached. The mapping is unconditional, with no exception for which shape it happens to be (see `app-behavior.md`'s Lazy Instantiation section).
- **Declared tools** — every tool any reached template declares must be present on the pod. When a member adds a category tag naming a concept that has a template, Lazy Instantiation gives the pod each tool that template declares and the pod does not already carry; removing a tag never removes a tool, and tools are shared content, so the tool reaches every member even though the tag does not. So for every declared form tool, some `tpod.tool` graph must carry each of its `pod:formShape` values; and for every declared tool of another kind (`ctpl:IdVerificationTemplatePod`'s `pod:Browser`, say), the pod must carry a `tpod.tool` entry of that `type`. A pod may carry more tools than its templates declare — a removed tag's among them; only a missing one is a violation.

Both are direct CURIE-set membership, since `pod:shape`'s range is `sh:NodeShape` (`pod.ttl`), the same range `pod:memberShape`/`pod:formShape` already carry, so no label resolution and no named exceptions are needed. A tag whose concept has no template contributes nothing — the same defensive branch as TTL-4. This is not itself an OWL/SHACL-expressible constraint (same reasoning as YAML-4/YAML-6/YAML-7/YAML-8/TTL-3/TTL-4 — it requires dereferencing values across the template files, not just pod-databook YAML), so it's checked here instead. Run:

```python
import glob, re, yaml
import rdflib

POD = rdflib.Namespace('http://mee.foundation/ontologies/pod#')

# Every TemplatePod, core and extension, keyed by its pod:category concept's
# full IRI (None for ctpl:UserDefinedTemplatePod): the memberShape CURIEs it
# requires, and each tool it declares as (tool type, its formShape CURIEs).
# Each file is parsed on its own, so normalizeUri() renders an IRI with that
# file's own @prefix bindings — the CURIEs the YAML carries.
templates, prefixes = {}, {}
for path in ['pod-category-templates.ttl'] + sorted(glob.glob('pod-category-ext/*.ttl')):
    g = rdflib.Graph(); g.parse(path, format='turtle')
    curie = g.namespace_manager.normalizeUri
    prefixes.update({p: str(ns) for p, ns in g.namespaces()})
    for s in g.subjects(rdflib.RDF.type, POD.TemplatePod):
        entry = {
            'name': curie(s),
            'member': {curie(o) for o in g.objects(s, POD.memberShape)},
            'tools': [
                (next((str(c).split('#')[-1].lower() for c in g.objects(t, rdflib.RDF.type)
                       if str(c).startswith(str(POD))), 'form'),
                 {curie(o) for o in g.objects(t, POD.formShape)})
                for t in g.objects(s, POD.declaresTool)
            ],
        }
        cats = list(g.objects(s, POD.category))
        for cat in cats or [None]:
            templates[str(cat) if cat is not None else None] = entry

def expand(c):
    p, _, local = c.partition(':')
    return prefixes.get(p, p + ':') + local

def frontmatter(path):
    text = open(path, encoding='utf-8').read()
    m = re.match(r'^---\n(.*?)\n---', text, re.DOTALL)
    return yaml.safe_load(m.group(1)) if m else None

def as_list(v):
    return [] if v is None else (v if isinstance(v, list) else [v])

def reached_templates(tpod):
    # tpod.categoryTag is a list, zero or more per pod. Each tag reaches its own
    # template; a pod with no tag at all reaches ctpl:UserDefinedTemplatePod's
    # (keyed None). A tag whose concept has no template contributes nothing.
    tags = as_list(tpod.get('categoryTag'))
    keys = [expand(c) for c in tags] if tags else [None]
    return [templates[k] for k in keys if k in templates]

violations = 0
for path in sorted(glob.glob('example/Pods/**/*.databook.md', recursive=True)):
    if 'under-development' in path.split('/'):
        continue
    fm = frontmatter(path)
    if not fm:
        continue
    tpod = fm.get('tpod') or {}
    reached = reached_templates(tpod)
    if not reached:
        continue  # no TemplatePod for any of this pod's tags

    # Member shapes: the union of every reached template's pod:memberShape.
    required = set().union(*(r['member'] for r in reached))
    for entry in as_list(tpod.get('member')):
        if not isinstance(entry, dict):
            continue
        missing = required - set(as_list(entry.get('shape')))
        if missing:
            violations += 1
            print(f"VIOLATION {path}: member graph {entry.get('id')} is missing "
                  f"required pod:shape value(s) {sorted(missing)}")

    # Declared tools: Lazy Instantiation added each one when its tag was added.
    live = [t for t in as_list(tpod.get('tool')) if isinstance(t, dict)]
    live_types = {t.get('type', 'form') for t in live}
    live_shapes = {s for t in live for g in as_list(t.get('graph')) if isinstance(g, dict)
                     for s in as_list(g.get('shape'))}
    for r in reached:
        for kind, shapes in r['tools']:
            if shapes:
                missing = shapes - live_shapes
                if missing:
                    violations += 1
                    print(f"VIOLATION {path}: {r['name']} declares a {kind} tool with "
                          f"pod:formShape {sorted(missing)}, but no tool graph on the pod carries it")
            elif kind not in live_types:
                violations += 1
                print(f"VIOLATION {path}: {r['name']} declares a {kind} tool, "
                      f"but the pod carries no tool of type {kind!r}")
print("Every pod carries every member shape and declared tool its category tags' templates require."
      if violations == 0 else f'{violations} violation(s) found.')
```

If a violation is found: for a missing member shape, add the missing `shape:` value(s) to the graph's own `tpod.member[]` entry, and verify (per TTL-3) that the graph's own individual — usually its `:Self` claim, per the required minimal `GivenName` stub — actually satisfies the shape's constraints; if it doesn't yet, add the missing content rather than just the shape value. For a missing declared tool, add the tool the template declares — for a form tool, with a graph carrying the declared `pod:formShape` — or, if the pod should not carry that category tag at all, remove the tag. Never remove a tool to satisfy this check.

**TTL-6 — every category concept has a matching `pod:TemplatePod`**: Every `skos:Concept` in `pod-categories.ttl`'s `podcat:PodCategoryScheme` — **including** the two SKOS top concepts `podcat:Person`/`podcat:Organization`, which a real pod may legitimately carry as a category tag (`Acme` is tagged `podcat:Organization`, standing for an employer) — must have a matching `pod:TemplatePod` in `pod-category-templates.ttl` carrying that same `pod:category` value. This is the reverse direction of TTL-4/TTL-5's own reverse lookup (`?tc pod:category podcat:X`): those checks skip a category tag outright when its concept has no `TemplatePod` at all, so nothing else catches a category that should have one but doesn't. This is not itself an OWL/SHACL-expressible constraint (same reasoning as YAML-4/YAML-6/YAML-7/YAML-8/TTL-3/TTL-4/TTL-5 — it requires cross-referencing every concept in `pod-categories.ttl` against every individual in `pod-category-templates.ttl`, not just parsing one file's own YAML or Turtle in isolation), so it's checked here instead. Run:

```python
import rdflib

SKOS  = rdflib.Namespace('http://www.w3.org/2004/02/skos/core#')
POD  = rdflib.Namespace('http://mee.foundation/ontologies/pod#')
curie = lambda u: 'podcat:' + str(u).split('#')[-1]

cats = rdflib.Graph(); cats.parse('pod-categories.ttl', format='turtle')
concepts = {s: str(l) for s in cats.subjects(rdflib.RDF.type, SKOS.Concept)
                      for l in cats.objects(s, SKOS.prefLabel)}

tpl = rdflib.Graph(); tpl.parse('pod-category-templates.ttl', format='turtle')
# Only the object of a real pod:category triple counts. A regex over the file
# text would also match the phrase inside ctpl:UserDefinedTemplatePod's own
# rdfs:comment, which cites "?tc pod:category podcat:X" as prose.
existing = {o for s in tpl.subjects(rdflib.RDF.type, POD.TemplatePod)
              for o in tpl.objects(s, POD.category)}

violations = 0
for c in sorted(set(concepts) - existing, key=curie):
    violations += 1
    print(f"VIOLATION: {curie(c)} ({concepts[c]!r}) has no matching pod:TemplatePod in pod-category-templates.ttl")
print("Every category concept, top concepts included, has a matching TemplatePod."
      if violations == 0 else f'{violations} violation(s) found.')
```

If a violation is found: add a new `ctpl:XTemplatePod` individual to `pod-category-templates.ttl` for the missing category, following the standard pattern for a category with no document type of its own — `pod:memberShape pshapes:ContactInfoShape` and no `pod:declaresTool` at all — unless the category genuinely has its own document/record type, in which case follow the pattern of an existing tool-declaring template instead (see `pod-category-templates.ttl`'s row in core-files.md). Adding a new `TemplatePod` also brings the category into scope for TTL-4/TTL-5 and `helpers/validate.py` — re-run those afterward, since any real pod carrying that category tag then needs its own `tpod.member` graph(s) to carry the matching `pod:shape` value (TTL-5) and may need minimal `GivenName` content added if it doesn't already have any (TTL-3 and the template pass).

**TTL-7 — every `pod:TemplatePod` individual carries a `pod:memberShape`, and every one in `pod-category-templates.ttl` carries `pshapes:ContactInfoShape`**: Every `pod:memberShape` value in `pod-category-templates.ttl` is the identical `pshapes:ContactInfoShape` — a `pod:member` graph is always validated as a basic contact-info profile, regardless of category, while any category-specific content lives in a tool instead (see `app-behavior.md`'s Lazy Instantiation section). This is asserted directly and explicitly on every individual, on purpose — not hoisted onto the `pod:TemplatePod` class itself via an OWL restriction, since nothing in this project's own validation pipeline runs a reasoner to materialize such an entailment (`helpers/validate.py` validates literal asserted triples only, via `riot`/`shacl validate`), and TTL-4/TTL-5/TTL-6 above all rely on literally finding this triple in each individual's own block. This check exists to catch a new `TemplatePod` added without it (e.g. by hand, skipping the standard pattern), which SHACL itself wouldn't catch either (`shacl/pod-shacl.ttl`'s `:TemplatePodShape` allows zero or more `pod:memberShape` values, no minimum). This is not itself an OWL/SHACL-expressible constraint (same reasoning as TTL-6 above), so it's checked here instead.

The uniformity claim is scoped to `pod-category-templates.ttl` deliberately, and that scoping is the whole point: a template pod published by a **category extension** (`pod-category-ext/`, see TTL-8) may name any member shape it likes, which is what `pod:memberShape` exists for. `bhscat:BostonHubSocietyTemplatePod` is the first to exercise this, naming `bhsshapes:MemberShape` — the Boston Hub Society's own two-page directory form — in place of `ContactInfoShape`. So the check runs in two halves: **every** `pod:TemplatePod` anywhere must carry at least one `pod:memberShape` value (a template naming none validates nothing, which is always a mistake), and every one **in `pod-category-templates.ttl`** must carry `pshapes:ContactInfoShape` specifically (the app's own shipped templates stay uniform; variation arrives only with an extension). Run:

```python
import glob, rdflib

POD    = rdflib.Namespace('http://mee.foundation/ontologies/pod#')
CONTACT = rdflib.URIRef('http://mee.foundation/ontologies/persona/shapes#ContactInfoShape')

# pod-category-templates.ttl plus every category extension bundle: an extension file
# carries its own pod:TemplatePod individuals alongside its concept scheme.
violations = 0
for path in ['pod-category-templates.ttl'] + sorted(glob.glob('pod-category-ext/*.ttl')):
    core = (path == 'pod-category-templates.ttl')
    g = rdflib.Graph(); g.parse(path, format='turtle')
    for s in sorted(g.subjects(rdflib.RDF.type, POD.TemplatePod), key=str):
        name = str(s).split('#')[-1]
        shapes = set(g.objects(s, POD.memberShape))
        if not shapes:
            violations += 1
            print(f"VIOLATION: {name} ({path}) carries no pod:memberShape at all")
        elif core and CONTACT not in shapes:
            violations += 1
            print(f"VIOLATION: {name} (pod-category-templates.ttl) does not carry pod:memberShape pshapes:ContactInfoShape")
print("Every TemplatePod carries a memberShape; every pod-category-templates.ttl one carries ContactInfoShape."
      if violations == 0 else f'{violations} violation(s) found.')
```

If a violation is found: add a `pod:memberShape` value to the offending `TemplatePod` individual. In `pod-category-templates.ttl` that value is `pshapes:ContactInfoShape`, with no exception. In a `pod-category-ext/` bundle it is whichever shape that extension publishes — the point of an extension being that it may differ. A `TemplatePod` with no `pod:memberShape` at all is always wrong: TTL-5 would then require nothing of that category's member graphs, and they would go unvalidated.

**TTL-8 — every category extension's concepts map into the core taxonomy, and each has a template pod**: A **category extension** (`pod-category-ext/`) is a bundle an organization publishes so other instances can tag and validate pods with a category `pod-categories.ttl` does not define: one file carrying the publisher's own `skos:ConceptScheme`, the concepts in it, and a `pod:TemplatePod` for each, with its member shape beside it in `pod-category-ext/shacl/`. `pod-categories.ttl` and `pod-category-templates.ttl` never change to accommodate one — which is exactly why TTL-6 and TTL-7 can keep their own scoping, and why `images/pod-categories/pod-categories.png` (PNG-5) stays correct as extensions are added.

The mechanism is SKOS's own. `skos:broader` is defined for hierarchy *within* one concept scheme; the `skos:mappingRelation` family, of which `skos:broadMatch` is one, is defined for links *between* schemes. An extension concept is by definition in another scheme, so it links to the core taxonomy with `skos:broadMatch` and never with `skos:broader`. That link is load-bearing rather than decorative: a recipient whose app does not have the extension installed is offered the `broadMatch` target as a category-tag suggestion in place of the extension concept, and a search for a core category reaches a pod tagged with the extension concept through it.

`shacl/pod-shacl.ttl`'s `:InSchemeConceptShape` carries half of this, applied to `pod:category` by `:TemplatePodShape` and to `pod:categoryTag` by `:InstancePodShape` — a value must be a `skos:Concept` with at least one `skos:inScheme` value that is a `skos:ConceptScheme` — and it deliberately does not pin that scheme to `podcat:PodCategoryScheme`, since an extension concept is never in it. The other half is not SHACL-expressible (it requires dereferencing across `pod-category-ext/` and `pod-categories.ttl` at once, the same reasoning as TTL-4/TTL-5/TTL-6), so it is checked here. For every `pod-category-ext/*.ttl` file, every `skos:Concept` in it must:

- **39a** — carry `skos:inScheme` naming a scheme declared in that same file, and **not** `podcat:PodCategoryScheme`. An extension concept that claimed core-scheme membership would be caught by TTL-6 as a core concept with no `pod-category-templates.ttl` entry.
- **39b** — carry exactly one `skos:broadMatch`, whose value is a `podcat:` concept. One, not zero (no core concept to suggest or search by) and not several (no single answer to which).
- **39c** — carry no `skos:broader` at all, that predicate being reserved for within-scheme hierarchy. An extension with a hierarchy *of its own* may use `skos:broader` between two of its own concepts; what 39c forbids is a `skos:broader` pointing at a `podcat:` concept, which is the misuse `skos:broadMatch` exists to replace.
- **39d** — have a matching `pod:TemplatePod` in that same file, carrying that concept as its `pod:category` value — the extension's own analogue of TTL-6, and what makes the reverse lookup in TTL-4/TTL-5 resolve for a pod carrying this category tag.

Run:

```python
import glob, rdflib

SKOS = rdflib.Namespace('http://www.w3.org/2004/02/skos/core#')
POD = rdflib.Namespace('http://mee.foundation/ontologies/pod#')
CAT  = 'http://mee.foundation/ontologies/pod-categories#'
CORE_SCHEME = rdflib.URIRef(CAT + 'PodCategoryScheme')

def short(g, u):
    return g.namespace_manager.normalizeUri(u)

violations = 0
for path in sorted(glob.glob('pod-category-ext/*.ttl')):
    g = rdflib.Graph(); g.parse(path, format='turtle')
    schemes  = set(g.subjects(rdflib.RDF.type, SKOS.ConceptScheme))
    templated = set(g.objects(None, POD.category))
    for c in sorted(g.subjects(rdflib.RDF.type, SKOS.Concept), key=str):
        name = short(g, c)
        in_scheme   = set(g.objects(c, SKOS.inScheme))
        broad_match = list(g.objects(c, SKOS.broadMatch))
        broader     = list(g.objects(c, SKOS.broader))
        if not in_scheme & schemes:                                        # 39a
            violations += 1
            print(f"VIOLATION 39a: {name} ({path}) is not in a scheme declared in its own file")
        if CORE_SCHEME in in_scheme:                                       # 39a
            violations += 1
            print(f"VIOLATION 39a: {name} ({path}) claims skos:inScheme podcat:PodCategoryScheme")
        if len(broad_match) != 1:                                          # 39b
            violations += 1
            print(f"VIOLATION 39b: {name} ({path}) has {len(broad_match)} skos:broadMatch values, expected exactly 1")
        elif not str(broad_match[0]).startswith(CAT):                      # 39b
            violations += 1
            print(f"VIOLATION 39b: {name} ({path}) skos:broadMatch {short(g, broad_match[0])} is not a podcat: concept")
        for b in broader:                                                  # 39c
            if str(b).startswith(CAT):
                violations += 1
                print(f"VIOLATION 39c: {name} ({path}) uses skos:broader {short(g, b)} across schemes; use skos:broadMatch")
        if c not in templated:                                             # 39d
            violations += 1
            print(f"VIOLATION 39d: {name} ({path}) has no pod:TemplatePod naming it as pod:category")
print("Every category extension concept maps into the core taxonomy and has a template pod."
      if violations == 0 else f'{violations} violation(s) found.')
```

If a violation is found: for **39a**/**39b**/**39c**, fix the concept's own block — it belongs to its publisher's scheme and reaches the core taxonomy only through a single `skos:broadMatch`. For **39d**, add a `pod:TemplatePod` for it to the same file, carrying `pod:category` naming the concept and a `pod:memberShape` naming whichever shape the extension publishes (TTL-7's second half requires the `pod:memberShape`; unlike a `pod-category-templates.ttl` template, it need not be `pshapes:ContactInfoShape` — a bundle differing there is the entire purpose of an extension).

## YAML — pod DataBook checks

These read a pod DataBook's **YAML frontmatter**, and sometimes its Markdown body, exactly as written — before any triple is synthesized from it. That is the point: several of them hunt malformations that synthesis would coerce, drop, or collapse away.


**YAML-1 — Graph id naming convention**: Every `tpod.member[]`/`tpod.tool[].graph[]` entry's own `id` value's local-name (the string after the final `/`) — across all pod-databooks in `example/Pods/` — must follow the flat pattern `graph-<NN>`, where `<NN>` is the graph's own number — zero-padded to two digits up to `graph-99`, three digits from `graph-100` on — matching the graph's own diagram label, `### Graph NN` body heading, and `<a id="graph-NN">` anchor. If an id does not match this pattern, flag it rather than silently renaming — the entry's `id` also doubles as the graph's own named-graph identity (`{id}#graph`), so changing it is a bigger operation than a file rename ever was.

**YAML-2 — `member`/`tool` entry well-formedness** (the format itself is specified in [pod-databook.md](pod-databook.md#the-tpod-block)): Each `tpod.member` entry carries a graph's full metadata directly (`id`, `claimant`, `subject`, and optionally `shape`), and each `tpod.tool` entry carries its own `id`/`type`/`formTopic` plus a nested `graph` list whose entries carry `id`, `claimant` and optionally `shape` — rather than a bare local-name reference into a separate list, so there's no cross-list consistency left to check. A tool graph carries no about-ness field of its own: its topic is the tool's single `formTopic`, which is exactly what makes several members' claims unable to disagree about what they are about. `formTopic` and the nested `graph` list are both scoped to a **form** tool (`pod:Form` is the one tool class with a content model — see `pod.ttl`'s Pod Tools section), so an entry of any other type (`calendar`, `canvas`, `contacts`, `map`, `browser`) carries neither. But a malformed entry (e.g. a stray bare string left over from a hand edit, or a missing required field) would otherwise go unnoticed. Which about-ness field an entry carries depends on which list it sits in, since the two lists hold different classes of graph (`pod.ttl`): a `tpod.member` entry is a `pod:MemberGraph` and carries `subject`, while a `tpod.tool[].graph` entry is a `pod:FormGraph` and carries no about-ness field of its own — its topic is the holding tool's single `formTopic`. Neither kind ever carries the other's field — they are `owl:disjointWith`, enforced by `shacl/pod-shacl.ttl`'s `:FormGraphShape` `sh:maxCount 0` guard. For every pod-databook under `example/Pods/`, verify that every tool entry carries an `id` (its pattern and uniqueness are YAML-10's), that every `tpod.member` entry and every tool graph is a mapping (never a bare string), that its `id` matches the `graph-<NN>` id pattern (see YAML-1), that `claimant` is present (required on both kinds, per `:CGraphShape`), and that the entry carries exactly its own list's about-ness field and not the other's; `template` stays optional (see TTL-5 for when it's actually required). Run:

```python
import glob, re, yaml

GRAPH_ID_RE = re.compile(r'^http://www\.example\.org/tpod/graphs/graph-(?:\d{2}|[1-9]\d{2})$')

def frontmatter(path):
    text = open(path, encoding='utf-8').read()
    m = re.match(r'^---\n(.*?)\n---', text, re.DOTALL)
    return yaml.safe_load(m.group(1)) if m else None

def as_list(v):
    return [] if v is None else (v if isinstance(v, list) else [v])

errors = 0
for path in sorted(glob.glob('example/Pods/**/*.databook.md', recursive=True)):
    if 'under-development' in path.split('/'):
        continue
    fm = frontmatter(path)
    if not fm or fm.get('type') != 'pod-databook':
        continue
    tpod = fm.get('tpod', {}) or {}
    # Every graph the pod links, paired with which list it came from: member
    # entries directly, tool graphs one level down under each tool.
    entries = [('member', e) for e in as_list(tpod.get('member'))]
    for i, tool in enumerate(as_list(tpod.get('tool'))):
        if not isinstance(tool, dict):
            print(f'{path}: tool entry {i} is not a mapping: {tool!r}')
            errors += 1
            continue
        # Every live tool is named by its own IRI, its id (pod-databook.md's
        # Tool Ids); YAML-10 checks the id's pattern and uniqueness.
        if not tool.get('id'):
            print(f'{path}: tool entry {i} missing id')
            errors += 1
        if tool.get('type') not in ('form', 'calendar', 'canvas', 'contacts', 'map', 'browser'):
            print(f"{path}: tool entry {i} has unknown type {tool.get('type')!r}")
            errors += 1
        # pod:formTopic and pod:formGraph are scoped to pod:Form
        # (pod.ttl), so both are required of a form tool and of nothing
        # else; no other kind carries a content property at all.
        if tool.get('type', 'form') == 'form':
            if not tool.get('formTopic'):
                print(f'{path}: form tool entry {i} missing formTopic')
                errors += 1
            if not as_list(tool.get('graph')):
                print(f'{path}: form tool entry {i} carries no graph')
                errors += 1
        else:
            for k in ('formTopic', 'graph'):
                if tool.get(k):
                    print(f"{path}: {tool.get('type')} tool entry {i} carries {k}, which is scoped to a form tool")
                    errors += 1
        entries += [('tool', e) for e in as_list(tool.get('graph'))]

    for field, entry in entries:
        if not isinstance(entry, dict):
            print(f'{path}: {field} entry is not a mapping: {entry!r}')
            errors += 1
            continue
        if not GRAPH_ID_RE.match(entry.get('id') or ''):
            print(f"{path}: {field} entry id {entry.get('id')!r} does not match graph-<NN> id pattern")
            errors += 1
        if not entry.get('claimant'):
            print(f"{path}: {field} entry {entry.get('id')!r} missing claimant")
            errors += 1
        # A member entry is a pod:MemberGraph and carries subject; a tool's
        # graph is a pod:FormGraph and carries no about-ness field at all,
        # its topic being the tool's own single formTopic one level up.
        if field == 'member' and not entry.get('subject'):
            print(f"{path}: member entry {entry.get('id')!r} missing subject")
            errors += 1
        for stale in ('subject',) if field == 'tool' else ():
            if entry.get(stale):
                print(f"{path}: tool graph {entry.get('id')!r} carries {stale}, which belongs to a member entry")
                errors += 1
        if entry.get('graphTopic'):
            print(f"{path}: {field} entry {entry.get('id')!r} carries graphTopic; a tool's topic is its own formTopic")
            errors += 1
if not errors:
    print('All pod-databooks: every member entry and tool graph is a well-formed mapping.')
```

If a malformed entry is found, fix it directly (turn a stray bare string back into a full mapping, correct the id, or add the missing `id`/`claimant`/`subject`/`formTopic`).

**YAML-3 — Pod id naming convention**: This check applies only to `example/Pods/` — the example user's own pods — since there is no separate canonical-instance file tree: the canonical tree is the `podcat:PodCategoryScheme` SKOS concept scheme in `pod-categories.ttl` itself, with class-level templates in `pod-category-templates.ttl`. A pod-databook's `id:` is deliberately independent of its filename — the filename stays the folder's own verbatim name per the [Filename Convention](pod-databook.md#filename-convention), but the `id:` value is a flat, opaque, globally-unique identifier, following the same reasoning and pattern as the [Graph Ids and Named Graphs](pod-databook.md#graph-ids-and-named-graphs)'s `graph-<NN>`: a pod's name need not be unique, so encoding it into the id would risk a collision the moment two pods shared a name, and nothing in the repo actually depends on the id's string *structure* — it's purely a self-contained RDF subject identifier for that one pod, never cross-referenced by another pod, a graph, or a catalog file. Every `id:` value — across all pod-databooks in `example/Pods/` — must follow the flat pattern `http://www.example.org/tpod/pods/pod-<NN>`, where `<NN>` is a zero-padded two-digit number, assigned once at creation and never reused or renumbered. Every `<NN>` must be globally unique across `example/Pods/`. Run:

```python
import glob, re

pattern = re.compile(r'^http://www\.example\.org/tpod/pods/pod-(\d{2})$')
seen = {}
errors = 0
for path in sorted(glob.glob('example/Pods/**/*.databook.md', recursive=True)):
    if 'under-development' in path.split('/'):
        continue
    text = open(path).read()
    m = re.search(r'^id:\s*(\S+)', text, re.MULTILINE)
    fid = m.group(1).strip() if m else ''
    pm = pattern.match(fid)
    if not pm:
        print(f'MALFORMED  {path}  id={fid!r} does not match http://www.example.org/tpod/pods/pod-<NN>')
        errors += 1
        continue
    nn = pm.group(1)
    if nn in seen:
        print(f'DUPLICATE  pod-{nn}  used by both {seen[nn]!r} and {path!r}')
        errors += 1
    else:
        seen[nn] = path
print('YAML-3: OK' if errors == 0 else f'YAML-3: {errors} issue(s) found')
```

If a malformed id is found, fix it to match the pattern. If a duplicate `<NN>` is found, assign the newer pod the next unused number — never renumber an existing pod's id, since (like a graph id) it may already be referenced by an external peer over the PDN. This rule has no exceptions for `example/Pods/`, fictional as its data is — treat every id there exactly as if a real external PDN peer might already hold a reference to it.

Note: this check's `^id:\s*(\S+)` regex is anchored at true line-start with no leading whitespace, so it only ever matches a file's own top-level `id:` line — a nested, indented `tpod.member[]`/`tpod.tool[].graph[].id` value never matches this anchor and is intentionally out of scope here (a graph's `id` is not expected to relate to its owning pod file's name at all; see YAML-1 for that). This imposes a requirement on any script that writes `tpod.member`/`tpod.tool`: never emit an unindented `id:` at column 0.

**YAML-4 — a pod's subject is derived from its tools plus `member`, never stored**: There is no independently-asserted pod-level subject property (nor a pod-level `tpod.subject` field — the `subject:` key sits inside each `tpod.member` entry, naming that member) — who or what a pod's relationship is about is computed, not stored, by a simple two-branch rule. The two branches read properties at *different levels*, since a tool states its topic once for all the graphs beneath it while a member entry carries its own subject directly (`pod.ttl`): a `member` entry is a `pod:MemberGraph` carrying `pod:subject`, while a tool's graphs are `pod:FormGraph`s carrying no about-ness of their own, the tool's single `pod:formTopic` standing for all of them. **If the pod has any form tools**, the full set of distinct `pod:formTopic` values among them is the pod's subject (e.g. `Medical Appointment.databook.md`, a two-member pod: `member` holds Dave's and Self's graphs, and its one form tool is about Sophia — subject is `:Sophia_Walker`); **otherwise** the subject is the full set of distinct `pod:subject` values among `member` — the pod's own active members (e.g. `Bob Johnson.databook.md`, a two-member pod with no tool: subject is `:Self` and `:Bob_Johnson` together; `Fred Flintstone.databook.md`, likewise: `:Self` and `:Fred_Flintstone` together). `Boston Hub Society.databook.md` shows the first branch taking over from the second: as a three-member pod it would derive `:BHS_Service`, `:Bob_Johnson`, and `:Self` together, but its one manually-added form tool — BHS's own organizational profile, claimed by BHS — narrows the derived subject to `:BHS` alone. Every real example pod carries at most one form tool, but the rule and this check both generalize to any number, a pod being free to hold as many tools as it likes. A tool's topic is explicitly **allowed** to duplicate a `member` subject — this is the normal shape for every template-declared form tool whose pod's `pod:member` content is just the generic `ContactInfoShape` contact-info stub (claimed by and about `:Self`) while the pod's real content lives in the tool, also about `:Self` (e.g. `Google.databook.md`, `SSN.databook.md`, `Paradise.databook.md`): the stub `member` isn't a distinct party the derived subject needs to separately surface, so the derivation switching to the tool set alone (ignoring `member`) is intended, not a masking bug. This check therefore only reports each pod's derived subject for reference — it does not flag member/tool subject overlap as a violation. Run:

```python
import re, yaml, glob

def frontmatter(path):
    text = open(path, encoding='utf-8').read()
    m = re.match(r'^---\n(.*?)\n---', text, re.DOTALL)
    return yaml.safe_load(m.group(1)) if m else None

for f in glob.glob('example/Pods/**/*.databook.md', recursive=True):
    fm = frontmatter(f)
    if not fm:
        continue
    tpod = fm.get('tpod', {}) or {}
    if not tpod.get('member'):
        continue
    # A member entry carries its own subject directly; a tool carries one
    # topic for all its graphs at once, so the two branches read different
    # levels (pod:subject on the graph vs pod:formTopic on the tool).
    pt = tpod.get('member') or []
    pt = pt if isinstance(pt, list) else [pt]
    tools = tpod.get('tool') or []
    tools = tools if isinstance(tools, list) else [tools]
    pt_subs = {t.get('subject') for t in pt}
    # pod:formTopic is scoped to pod:Form, so only a form tool
    # contributes; a pod holding only non-form tools (a browser, say) falls
    # to the pod:member branch below.
    form_tools = [t for t in tools if t.get('type', 'form') == 'form']
    tool_subs = {t.get('formTopic') for t in form_tools}
    derived = tool_subs if form_tools else pt_subs
    print(f'derived subject={sorted(s for s in derived if s)} {f}')
print()
print('Derived subjects listed above for every pod — member/tool subject overlap is allowed, not a violation.')
```

**YAML-5 — Pod-databook `title:` is the pod's name and matches its own folder's OS name** (a scaffolding check — at runtime there is no folder at all, and the app's own record of the name is authoritative outright): `title:` is defined as the pod's own name — it is always exactly the name of the filesystem folder that holds the pod-databook, and the two are kept in sync (a folder rename means updating `title:` to match, never the reverse); `title:` is never an independent display-name override of the folder's name. The [Filename Convention](pod-databook.md#filename-convention) already requires a pod-databook's *filename root* to be an exact copy of its folder's own name, but that convention is about the filename — not the separate `title:` YAML field, which several other checks (notably PNG-1a's box-label match) treat as authoritative for what a pod "is called." The invariant: for every pod-databook under `example/Pods/`, `title:` must equal `os.path.basename` of the folder it directly lives in, verbatim (same case/spacing/punctuation rule as the filename convention — no kebab-casing, no paraphrasing). Run:

```python
import os, re, yaml

def frontmatter(path):
    text = open(path, encoding='utf-8').read()
    m = re.match(r'^---\n(.*?)\n---', text, re.DOTALL)
    return yaml.safe_load(m.group(1)) if m else None

errors = 0
for dirpath, _, filenames in os.walk('example/Pods'):
    if 'under-development' in dirpath.split(os.sep):
        continue
    pods = [f for f in filenames if f.endswith('.databook.md')]
    for fname in pods:
        path = os.path.join(dirpath, fname)
        fm = frontmatter(path)
        if not fm:
            continue
        title = fm.get('title')
        folder_name = os.path.basename(dirpath)
        if title != folder_name:
            print(f'MISMATCH  {path}  folder={folder_name!r}  title={title!r}')
            errors += 1
print('OK — title: matches its own folder name for every pod-databook.' if errors == 0 else f'{errors} mismatch(es) found.')
```

If a mismatch is found, the folder name is authoritative within this scaffolding — update `title:` to match it exactly, even when the existing `title:` reads more naturally (e.g. an honorific like `Dr. Jane Starostina` vs. folder `Jane Starostina`, or an expansion like `AT&T` vs. folder `ATT`): `title:` is not an independent display-name override, so it cannot legitimately diverge from the folder's own name — the mismatch is drift, not a deliberate choice, since the folder name is also what PNG-1a's diagram-box match keys off. If the *folder's* name is what's actually wrong (e.g. it should have been named `AT&T` all along), rename the folder itself instead, then update the pod-databook's filename and `title:` together to match the new folder name.

**YAML-6 — `:Self` must be a member of every one of the user's pods**: A pod-databook under `example/Pods/` — the example user's own pods — can only ever have gotten there one of two ways: (1) the user created it themselves, in which case they (`:Self`) are trivially a member, or (2) someone else shared it with the user, in which case the share necessarily made `:Self` a member (a pod can't be "shared with" someone without them becoming a member of it). Either way, `:Self` must be one of the pod's active members — i.e. `:Self` must be the `pod:subject` of at least one of that pod's `member` — for **every** pod in `example/Pods/`, regardless of how many members the pod has or what the pod's derived subject (YAML-4) is. This is strictest for a pod with only one `member` entry: that entry's subject must be `:Self`, full stop — never a tool's own `pod:formTopic` (see YAML-4's placement rule above), even when the pod's derived-from-tool subject is a third party (e.g. `Jane_Starostina`, `Sophia_Walker`, `Ginger`) and no other graph happens to exist yet. Pods with more members have more room, so `:Self` just needs to be one of the members alongside whichever other real members the pod has (already satisfied by every existing example, e.g. Bob Johnson, Fred Flintstone, Medical Appointment, Boston Hub Society). This is not itself an OWL/SHACL-expressible constraint (same reasoning as YAML-4 — it requires dereferencing each `member` value's own `subject`, not just counting or matching cardinalities), so it's checked here instead. Run:

```python
import re, yaml, glob

def frontmatter(path):
    text = open(path, encoding='utf-8').read()
    m = re.match(r'^---\n(.*?)\n---', text, re.DOTALL)
    return yaml.safe_load(m.group(1)) if m else None

violations = 0
for f in glob.glob('example/Pods/**/*.databook.md', recursive=True):
    if 'under-development' in f.split('/'):
        continue
    fm = frontmatter(f)
    if not fm:
        continue
    tpod = fm.get('tpod', {}) or {}
    if not tpod.get('member'):
        continue
    pt = tpod.get('member') or []
    pt = pt if isinstance(pt, list) else [pt]
    subs = [t.get('subject') for t in pt]
    if not any(s == ':Self' for s in subs):
        violations += 1
        print(f'VIOLATION member-subjects={subs} (no :Self) {f}')
print('All pods have :Self as a member.' if violations == 0 else f'{violations} violation(s) found.')
```

If a violation is found, add a new minimal graph claimed by and about `:Self` (following the pattern in `Ginger Medical.databook.md`, `Jane Starostina.databook.md`, or `Sophia Health & Wellness.databook.md` — a single `designated by` → `GivenName` triple is enough), assign it the next free `graph-<NN>`, put it in `member`, and move whatever was in that slot under a `tool` entry instead.

**YAML-7 — `pod:owner`'s two subset invariants: creator ⊆ owner, and owner ⊆ member-subjects**: There is no OWL/SHACL-expressible way to check either invariant, since both require dereferencing values or comparing across fields rather than counting/matching a single path's cardinality — the same reasoning as YAML-4/YAML-6. For every pod-databook under `example/Pods/` (excluding `under-development/`) with a `tpod.owner` value: (a) `tpod.creator`'s own value must appear among `tpod.owner`'s values — the creator is always at least the pod's initial owner, and this repo's example data never demonstrates a promotion, so today `tpod.owner` always equals exactly `[tpod.creator]`, but the check only requires creator ⊆ owner, not equality, so a future example demonstrating promotion (owner as a proper superset of creator) would still pass; (b) every value in `tpod.owner` must equal the `pod:subject` of at least one of that pod's `tpod.member` graphs — an owner must always be one of the pod's actual members, never a non-member. Run:

```python
import re, yaml, glob

def frontmatter(path):
    text = open(path, encoding='utf-8').read()
    m = re.match(r'^---\n(.*?)\n---', text, re.DOTALL)
    return yaml.safe_load(m.group(1)) if m else None

violations = 0
for f in glob.glob('example/Pods/**/*.databook.md', recursive=True):
    if 'under-development' in f.split('/'):
        continue
    fm = frontmatter(f)
    if not fm:
        continue
    tpod = fm.get('tpod', {}) or {}
    owner = tpod.get('owner') or []
    owner = owner if isinstance(owner, list) else [owner]
    if not owner:
        continue
    creator = tpod.get('creator')
    if creator and creator not in owner:
        violations += 1
        print(f'VIOLATION {f}: creator {creator!r} not in owner {owner!r} (creator must be a subset of owner)')

    mt = tpod.get('member') or []
    mt = mt if isinstance(mt, list) else [mt]
    member_subs = {t.get('subject') for t in mt}
    bad_owners = [o for o in owner if o not in member_subs]
    if bad_owners:
        violations += 1
        print(f'VIOLATION {f}: owner value(s) {bad_owners} not among member subjects {sorted(s for s in member_subs if s)}')
print('All pods satisfy the owner subset invariants.' if violations == 0 else f'{violations} violation(s) found.')
```

If a violation is found: for (a), add the missing creator value to `tpod.owner`. For (b), either add a `tpod.member` graph whose subject matches the owner value, or remove that value from `tpod.owner` if it doesn't actually belong.

**YAML-8 — `pod:formGraph`'s real upper bound is the pod's own member count: one graph per member, each with a distinct claimant**: `pod:formGraph` carries no OWL/SHACL-expressible maximum — `shacl/pod-shacl.ttl`'s `:LiveToolShape` asserts only `sh:minCount 1` — but in practice its upper bound is exactly the pod's own member count, since every value represents one of the pod's own members making their own claim about the tool's single `pod:formTopic` (see README.md's Tools section). Concretely, two things must both hold for every tool on every pod-databook under `example/Pods/` (excluding `under-development/`): (a) each tool graph's `pod:claimant` must resolve to one of that same pod's own members — a tool's graph is never claimed by a non-member; and (b) within one tool, no two graphs may share the same claimant — each member gets at most one claim on that tool's topic. Together these two facts are what actually cap the count at the member count, rather than any cardinality restriction. The cap is per tool, not per pod: a pod carrying several tools may hold as many graphs in total as it has tools times members. This is not itself an OWL/SHACL-expressible constraint (same reasoning as YAML-4/YAML-6/YAML-7 — it requires dereferencing each graph's own `claimant`, and each `member` value's own `subject`, not just counting or matching cardinalities), so it's checked here instead.

"Resolves to one of the pod's members" is satisfied two ways, because a claimant is the party *really* making the claim rather than the member that mechanically carries it (see `pod.ttl`'s `pod:claimant` comment). Either the claimant **is** a `tpod.member` subject directly — the ordinary case, covering every `p:Person` and every `service:Service` that claims under its own IRI — or it is the `service:providedBy` organization **of** a member subject, which is how a `service:ServiceProvider` member's content gets attributed to the organization behind it. Both of the example data's organization claimants take the second route: `Boston Hub Society.databook.md`'s graph-92 is claimed by `:BHS` while the member subject is `:BHS_Service`, and `Citibank.databook.md`'s graph-76 is claimed by `:Citibank` while the member subject is `:Citibank_Service`. The `providedBy` link lives in the graph Turtle, not the frontmatter, so the script below reads it out of the pod's own embedded graph bodies. Run:

```python
import re, yaml, glob

def frontmatter(path):
    text = open(path, encoding='utf-8').read()
    m = re.match(r'^---\n(.*?)\n---', text, re.DOTALL)
    return yaml.safe_load(m.group(1)) if m else None

violations = 0
for f in glob.glob('example/Pods/**/*.databook.md', recursive=True):
    if 'under-development' in f.split('/'):
        continue
    fm = frontmatter(f)
    if not fm:
        continue
    tpod = fm.get('tpod', {}) or {}
    tools = tpod.get('tool') or []
    tools = tools if isinstance(tools, list) else [tools]
    if not tools:
        continue
    mt = tpod.get('member') or []
    mt = mt if isinstance(mt, list) else [mt]
    member_subs = {t.get('subject') for t in mt}
    # A pod:claimant may also be the service:providedBy organization of a
    # member subject — how a service:ServiceProvider member's content is
    # attributed to the organization behind it. Collect those too, reading the
    # providedBy links out of this pod's own embedded graph bodies.
    body = open(f, encoding='utf-8').read()
    provided = set()
    for svc, org in re.findall(
            r'(:\w+)\s+rdf:type[^.;]*?;[^.]*?service:providedBy\s+(:\w+)', body, re.DOTALL):
        if svc in member_subs:
            provided.add(org)
    allowed = member_subs | provided
    # The cap is per tool: each tool's own graphs must be claimed by distinct
    # members, but two different tools may each be claimed by the same member.
    for i, tool in enumerate(tools):
        graphs = tool.get('graph') or []
        graphs = graphs if isinstance(graphs, list) else [graphs]
        claimants = [g.get('claimant') for g in graphs]
        non_member = [c for c in claimants if c not in allowed]
        if non_member:
            violations += 1
            print(f"VIOLATION {f}: tool {i} graph claimant(s) {non_member} resolve to none of this pod's own members {sorted(s for s in allowed if s)}")
        seen, dup = set(), set()
        for c in claimants:
            (dup.add(c) if c in seen else seen.add(c))
        if dup:
            violations += 1
            print(f'VIOLATION {f}: tool {i} claimant(s) {sorted(dup)} repeat — each of a tool\'s graphs must be claimed by a distinct member')
print('All pods satisfy the tool-graph claimant invariants (member-only, distinct per tool).' if violations == 0 else f'{violations} violation(s) found.')
```

If a violation is found: for a tool graph claimed by a non-member, either add that claimant as a new `member` entry first, or — if the claimant is the organization behind a `service:ServiceProvider` that is already a member — add the missing `service:providedBy` triple to that service's own member graph, or reconsider whether the claim really belongs in this pod's tool at all. For a repeated claimant within one tool, merge the two graphs' content into one — a single member can only make one claim about a given tool's topic, not two.

**YAML-9 — pod tag well-formedness**: A pod's three tag fields — `tpod.categoryTag`, `tpod.userTag` and `tpod.serviceTag` (`pod:categoryTag`/`pod:userTag`/`pod:serviceTag`, `pod.ttl`'s Pod Tags section) — are each optional and each 0..N, but they are different shapes and SHACL reaches different distances into each, so what is left for this check differs by kind. **`tpod.categoryTag`** is a list of concept CURIEs, and `:InstancePodShape` checks each value is a `skos:Concept` in some scheme, so what is left here is only what synthesis hides: a value that is **not a string**, the field being **present but empty**, and a CURIE **repeated** on one pod, which RDF collapses to a single triple before validation runs. A tag together with one of its own broader concepts is deliberately not flagged: the broader one is redundant, being implied anyway, but harmless. **`tpod.userTag`** is a plain string, and `shacl/pod-shacl.ttl`'s `:InstancePodShape` constrains it only to a non-empty one (`sh:minLength 1`), leaving all three of the original failure modes here. *Whitespace*: `" Ginger"` and `"Ginger"` are distinct strings that `sh:minLength` accepts equally, and a padded tag silently fails to match its own unpadded twin in a tag search. *Type confusion*: a YAML value that isn't a string at all — a bare `2027` parsing as an integer, or a nested mapping left behind by a hand edit — reaches synthesis as a non-string, and `helpers/databook_graphs.py`'s `emit_lit()` stringifies whatever it is rather than rejecting it. *Duplication*: RDF is a set, so a tag repeated twice under this property collapses to a single triple *before* validation ever runs, making the duplicate permanently invisible to SHACL no matter what constraint is written. **`tpod.serviceTag`** is a nested mapping per value, and its three sub-keys become `pod:tagNamespace`/`pod:tagKey`/`pod:tagValue` on a `pod:ServiceTag` node that `:ServiceTagShape` constrains directly — spelling, cardinality and surrounding whitespace included. This check therefore does **not** repeat those regexes; duplicating them here would only let the two drift. What it covers for this kind is what no SHACL constraint can reach: a **sub-value that is not a string**, which `emit_lit()` stringifies into something that may well pass (a YAML float `1.2` becomes `"1.2"` and satisfies the reverse-DNS pattern outright); an **entry that is not a mapping at all**, typically a leftover flat `"AppleContacts/Christmas_List"` string from the retired opaque-string form, which SHACL can only report as three anonymous `sh:minCount` failures with no hint that the YAML shape is the problem; an **unrecognized extra sub-key**, which the emitter drops silently so RDF never learns it existed; the field being **present but empty**, indistinguishable in RDF from the field being absent; and **duplication**, which changes character here rather than disappearing — two identical entries synthesize two *distinct* blank nodes, so unlike a repeated literal the duplicate really is present after synthesis, but comparing sibling nodes needs a SPARQL query rather than any core SHACL constraint, and this repo uses `sh:sparql` nowhere. Deduplication is on the whole `(namespace, key, value)` triple, never on `(namespace, key)` alone: a contact sitting in three Apple Contacts Groups is legitimately three tags sharing one namespace and one key. Duplication *across* kinds is deliberately not flagged — the two properties are separate. This check reads YAML directly, before synthesis, which is the only point at which any of it is still observable. Run:

```python
import glob, re, yaml

TAG_SUBKEYS = ('namespace', 'key', 'value')

def frontmatter(path):
    text = open(path, encoding='utf-8').read()
    m = re.match(r'^---\n(.*?)\n---', text, re.DOTALL)
    return yaml.safe_load(m.group(1)) if m else None

def as_list(v):
    return [] if v is None else (v if isinstance(v, list) else [v])

violations = 0
for path in sorted(glob.glob('example/Pods/**/*.databook.md', recursive=True)):
    if 'under-development' in path.split('/'):
        continue
    fm = frontmatter(path)
    if not fm or fm.get('type') != 'pod-databook':
        continue
    tpod = fm.get('tpod', {}) or {}

    # tpod.categoryTag — a list of concept CURIEs. Their being concepts in a
    # scheme is :InstancePodShape's business; only the YAML shape and exact
    # duplicates, which RDF would collapse silently, are checked here.
    if 'categoryTag' in tpod:
        values = as_list(tpod.get('categoryTag'))
        if not values:
            print(f'VIOLATION {path}: categoryTag is present but empty — omit the field instead')
            violations += 1
        seen = set()
        for v in values:
            if not isinstance(v, str) or not v.strip():
                print(f'VIOLATION {path}: categoryTag value {v!r} is not a non-empty string')
                violations += 1
                continue
            if v in seen:
                print(f'VIOLATION {path}: categoryTag value {v!r} is duplicated')
                violations += 1
            seen.add(v)

    # tpod.userTag — a plain string, so all three original failure modes
    # still apply to it unchanged.
    if 'userTag' in tpod:
        values = as_list(tpod.get('userTag'))
        if not values:
            print(f'VIOLATION {path}: userTag is present but empty — omit the field instead')
            violations += 1
        seen = set()
        for v in values:
            if not isinstance(v, str):
                print(f'VIOLATION {path}: userTag value {v!r} is not a string (quote it)')
                violations += 1
                continue
            if not v.strip():
                print(f'VIOLATION {path}: userTag has an empty/blank value')
                violations += 1
                continue
            if v != v.strip():
                print(f'VIOLATION {path}: userTag value {v!r} has leading/trailing whitespace')
                violations += 1
            if v in seen:
                print(f'VIOLATION {path}: userTag value {v!r} is duplicated')
                violations += 1
            seen.add(v)

    # tpod.serviceTag — a nested namespace/key/value mapping per entry.
    # The namespace and key *spellings* are :ServiceTagShape's business
    # (sh:pattern); what is checked here is only the YAML shape SHACL never
    # sees.
    if 'serviceTag' in tpod:
        entries = as_list(tpod.get('serviceTag'))
        if not entries:
            print(f'VIOLATION {path}: serviceTag is present but empty — omit the field instead')
            violations += 1
        seen = set()
        for entry in entries:
            if not isinstance(entry, dict):
                print(f'VIOLATION {path}: serviceTag entry {entry!r} is not a mapping — '
                      f'it needs namespace/key/value sub-keys; the flat string form is retired')
                violations += 1
                continue
            extra = sorted(set(entry) - set(TAG_SUBKEYS))
            if extra:
                print(f'VIOLATION {path}: serviceTag entry has unrecognized sub-key(s) {extra}')
                violations += 1
            malformed = False
            for sub in TAG_SUBKEYS:
                if sub not in entry:
                    print(f'VIOLATION {path}: serviceTag entry is missing {sub}')
                    violations += 1
                    malformed = True
                    continue
                v = entry[sub]
                if not isinstance(v, str):
                    print(f'VIOLATION {path}: serviceTag {sub} {v!r} is not a string (quote it)')
                    violations += 1
                    malformed = True
                elif not v.strip():
                    print(f'VIOLATION {path}: serviceTag {sub} is empty/blank')
                    violations += 1
                    malformed = True
            if malformed:
                continue
            triple = (entry['namespace'], entry['key'], entry['value'])
            if triple in seen:
                print(f'VIOLATION {path}: serviceTag {triple!r} is duplicated on this pod')
                violations += 1
            seen.add(triple)

print('Every pod tag is well-formed.' if violations == 0 else f'{violations} violation(s) found.')
```

If a violation is found: quote a value that parsed as a number, trim the padding, drop the duplicate, restore a flat-string `serviceTag` entry to the three-sub-key mapping form, or delete a tag field that carries nothing rather than leaving it present and empty. Never "fix" a duplicate by moving one copy to a different tag kind just to silence the check — if the same label genuinely belongs to two kinds that is legal and this check already permits it, but a duplicate *within* one kind is always an editing slip. Nor should a repeated `(namespace, key)` pair be "fixed" by inventing a second key: a contact in two Apple Contacts Groups is two entries differing only in `value`, which is exactly right.

**YAML-10 — Tool id naming convention and uniqueness**: A live tool is named by its own IRI, carried as its `tpod.tool` entry's `id` — the id a block link in the pod's note resolves by (see [Tool Ids](pod-databook.md#tool-ids)). In `example/Pods/` that id follows the flat pattern `http://www.example.org/tpod/tools/tool-<NN>`, padded the way graph ids are — two digits up to `tool-99`, three from `tool-100` — and numbered in a single sequence across `example/Pods/`, so no number is used twice. YAML-2 checks that every tool entry carries an `id` at all; this check checks what it says. The id is not related to the tool's kind, topic, position or pod, so nothing beyond the pattern and uniqueness is checked. Run:

```python
import glob, re, yaml

pattern = re.compile(r'^http://www\.example\.org/tpod/tools/tool-(\d{2}|[1-9]\d{2,})$')

def frontmatter(path):
    text = open(path, encoding='utf-8').read()
    m = re.match(r'^---\n(.*?)\n---', text, re.DOTALL)
    return yaml.safe_load(m.group(1)) if m else None

def as_list(v):
    return [] if v is None else (v if isinstance(v, list) else [v])

seen = {}
errors = 0
for path in sorted(glob.glob('example/Pods/**/*.databook.md', recursive=True)):
    if 'under-development' in path.split('/'):
        continue
    fm = frontmatter(path)
    if not fm or fm.get('type') != 'pod-databook':
        continue
    for i, tool in enumerate(as_list((fm.get('tpod') or {}).get('tool'))):
        if not isinstance(tool, dict) or not tool.get('id'):
            continue  # YAML-2's finding, not this check's
        tid = tool['id']
        m = pattern.match(tid)
        if not m:
            print(f'MALFORMED  {path}  tool entry {i} id={tid!r} does not match http://www.example.org/tpod/tools/tool-<NN>')
            errors += 1
            continue
        nn = int(m.group(1))
        if nn in seen:
            print(f'DUPLICATE  tool-{m.group(1)}  used by both {seen[nn]!r} and {path!r}')
            errors += 1
        else:
            seen[nn] = path
print('YAML-10: OK' if errors == 0 else f'YAML-10: {errors} issue(s) found')
```

If a malformed id is found, fix it to match the pattern. If a duplicate number is found, give the newer tool the next unused number — never renumber an existing tool's id, since a block link in some member's copy of the note may already resolve by it. As with YAML-3, this holds for `example/Pods/` too, fictional as its data is.

## FS — filesystem and documentation checks

These read the **filesystem** — folder structure, filenames, which image files exist — and the documentation prose that refers to them. All of it is development scaffolding (see [storage.md](storage.md)): these keep this repo internally consistent and say nothing about how a running Tellipod stores anything.


**FS-1 — Validation documentation completeness**: The `## Validation` section of `example.md` must document a single validator, `helpers/validate.py`, run from the repo root as `python3 helpers/validate.py`. There are no "tiers" — that two-tier split (a global merged-data run plus a per-graph run) was retired because merging every pod into one default graph unions facts that the self-containment convention deliberately keeps per-graph, manufacturing violations no real query would see (the same reasoning as the [Named graph scoping of `BFO_0000115`](CLAUDE.md#key-architectural-patterns) note). The script walks every pod-databook under `example/Pods/` (skipping `under-development/`), validating **each pod in isolation from every other pod** — no two pods' data ever reach the same `shacl validate` call — and gives each pod two passes:

1. **Pod pass** — data is the pod's whole content at once: every one of its embedded graphs' Turtle (via `databook_graphs.iter_graph_blocks()`) plus the `pod:` triples synthesized from that pod's own `tpod.*` frontmatter (via `databook_graphs.process_pod_databook()`, shared with `helpers/yaml-to-rdf.py`). Shapes are the four general shapes files merged into one graph with `owl:imports` stripped: `shacl/pod-shacl.ttl`, `shacl/persona-shacl.ttl`, `shacl/organization-shacl.ttl`, `shacl/service-shacl.ttl`. The graph Turtle must be in this data, not just the frontmatter triples — `:InstancePodShape` constrains `creator`/`owner` with `sh:class p:Person` and `:CGraphShape` constrains `claimant` with `sh:or ( [sh:class p:Person] [sh:class o:Organization] [sh:class service:Service] )`, and those individuals are typed only in the graph Turtle. This pass is the only thing that validates `pod-shacl` against real instance data.
2. **Template pass** — each graph carrying a `shape:` value, checked on its own against the shape that value names. Since `pod:shape`'s range is `sh:NodeShape` (`pod.ttl`), the value already names the shape directly, with no label-to-shape resolution; the script's `SHAPE_TO_FILE` table only maps that shape's local name to which physical `*-shacl.ttl` file defines it, since `pshapes:` shapes are split across `shacl/persona-shacl.ttl` and `shacl/contactinfo-shacl.ttl`. A graph with no `template:` value is skipped. Each resolved shape is scoped so it can't fire outside the one graph being checked: every other shape co-located in the same physical file is deactivated, and — only for `ContactInfoShape` (`sh:targetClass persona:Person`, the one class broad enough to risk an incidental same-type individual, e.g. a bare `:Self` reasserted by the self-containment convention) — the shape is re-targeted (`sh:targetNode`) at only the *substantive* `persona:Person` individual(s) in that graph.

The two passes use **different base merges**, both built once per run: `pod-category-templates.ttl` is in the template pass's base but deliberately excluded from the pod pass's, so `pod-shacl`'s `:PodShape` can't fire on the 102 `ctpl:*TemplatePod` individuals — generic class-level content bound to no real person. The script exits non-zero on any violation or unresolved shape, so it doubles as a CI-style gate.

`example.md` must also document the **merged whole-example dump** (`helpers/extract-all.py` + `helpers/yaml-to-rdf.py` + `riot`) separately from validation, with the warning that the general shapes must never be run against it. That dump exists for the questions that genuinely need the union — TTL-1's cross-pod reachability, and loading the example into a triplestore — not for SHACL. If the algorithm changes, update `example.md`'s Validation section and `helpers/validate.py` to match.

**FS-2 — PNG file location**: The diagram PNG for every embedded graph (each `tpod.member`/`tpod.tool[].graph` entry across every pod-databook under `example/Pods/`) must be stored directly in `example/graphs/images/` (flat, no subfolders — not `images/example/`). Files in `under-development/` are excluded. There is no exemption: **every** embedded graph gets a PNG, whether or not any of the 12 diagrams draws it (PNG-2) — being undrawn has no bearing on whether a graph is diagrammed individually or documented.

**FS-3 — PNG filename convention**: Every diagram PNG in `example/graphs/images/` must use the same base filename as the graph's own `tpod.member[]`/`tpod.tool[].graph[].id` local-name (the string after the final `/`), with `.png` appended. For example, id local-name `graph-14` → `graph-14.png`. If the PNG does not yet exist, the graph's Diagram cell in `example.md` must be marked `*(todo)*` rather than left blank. This applies uniformly to every graph.

**FS-4 — No broken image links in `README.md`/`example.md`/`app-behavior.md`**: Every PNG path referenced in `README.md`, `example.md`, or `app-behavior.md` (both `<img src="...">` tags and `[view](...)` table links) must resolve to an actual file on disk. Run:

```bash
python3 -c "
import re, os
content = open('README.md').read() + open('example.md').read() + open('app-behavior.md').read()
pngs = [m.group(1) for m in re.finditer(r'src=[\"\\'](.*?\.png)[\"\\']', content)]
pngs += [m.group(1) for m in re.finditer(r'\]\((example/[^\s\"\']+\.png)\)', content)]
missing = [p for p in sorted(set(pngs)) if not os.path.exists(p)]
[print('MISSING:', p) for p in missing] or print('All PNG refs OK')
"
```

If any `MISSING:` lines appear, either add the file or update the link.

**FS-5 — `example/Pods/` is flat: one folder per pod, none nested**: **This whole check is a scaffolding check.** Tellipod persists nothing in the user's filesystem (see [storage.md](storage.md)), so at runtime there are no folders and no marker; every rule below governs `example/Pods/`, the layout this repo carries on disk so that real pod content can be validated and diagrammed before there is an app to hold it (see [Development Scaffolding](pod-databook.md#development-scaffolding) in pod-databook.md). There is no `tpod.child`/`tpod.pod` YAML list to cross-check, so the check reads no frontmatter at all. Pods do not nest, and the scaffolding mirrors that: every pod-databook sits at exactly `example/Pods/<Name>/<Name>.databook.md` — one level below `example/Pods/`, in a folder whose name equals the databook's filename stem verbatim (no disambiguator or suffix of any kind; see the [Filename Convention](pod-databook.md#filename-convention)) — and no pod folder sits inside another. A folder is a **pod** iff it directly contains a `_pod-attachments` folder — that folder is simultaneously the pod's attachments and its marker — and the `*.databook.md` carrying the pod's structured content must agree with it in both directions, which is what keeps the scaffolding from drifting. Like everything else here, these rules are meaningless once the app ships. The rules:

1. **Nothing sits loose in `example/Pods/` itself** — every pod has its own folder, so a (non-hidden) file directly in `example/Pods/` is an error.
2. **Every folder directly in `example/Pods/` is a pod**, holding exactly one pod-databook: never more, since a `pod:Pod` is self-contained and two pods sharing a folder would make a file in it ambiguously part of both; and never none, a folder with nothing in it being an empty/placeholder folder and one holding files but no databook being stray content outside any pod.
3. **The databook's stem equals its folder's name**, verbatim: `<Name>.databook.md` in `<Name>/`.
4. **No pod folder nests inside another**: no subfolder of a pod folder, at any depth, holds a pod-databook or a `_pod-attachments` folder. A pod folder holds, besides its databook, an optional `<Name>.md` note, its `_pod-attachments`, and the member's own private files, which they may arrange in subfolders however they like.
5. **`_pod-attachments` sits directly inside its pod folder and is flat** — plain files only, no subfolder and no pod-databook.
6. **Every pod has a `_pod-attachments` folder**, empty or not; since git cannot track an empty directory, a pod with no attachments carries a `.gitkeep` in it.

Hidden files — any whose name begins with a dot — are neither attachments nor private content, so they never make an otherwise empty folder count as occupied. Run:

```python
import os

ROOT = 'example/Pods'
ATTACH = '_pod-attachments'   # the one reserved subfolder name, and the pod marker
SUFFIX = '.databook.md'

def visible(names):
    return [n for n in names if not n.startswith('.')]

errors = []

# 1. Nothing loose in example/Pods/ itself.
for name in sorted(visible(os.listdir(ROOT))):
    if os.path.isfile(os.path.join(ROOT, name)):
        errors.append(f'LOOSE FILE: {name!r} sits directly in {ROOT} (every pod has its own folder)')

for folder in sorted(visible(os.listdir(ROOT))):
    full = os.path.join(ROOT, folder)
    if not os.path.isdir(full) or folder == 'under-development':
        continue

    # 2. Every top-level folder is a pod: exactly one databook directly in it.
    books = sorted(f for f in os.listdir(full) if f.endswith(SUFFIX))
    if not books:
        has_file = any(visible(fns) for _, _, fns in os.walk(full))
        errors.append(f'NOT A POD: {folder!r} holds no {SUFFIX}'
                      + (' but holds files' if has_file else ' and no files (empty/placeholder)'))
        continue
    if len(books) > 1:
        errors.append(f'TOO MANY PODS: {folder!r} has {len(books)} pod-databooks (expected exactly 1): {books}')

    # 3. The databook's stem is the folder's name, verbatim.
    for b in books:
        if b[:-len(SUFFIX)] != folder:
            errors.append(f'STEM MISMATCH: {folder}/{b} (expected {folder}{SUFFIX})')

    # 6. Every pod has its marker folder.
    if not os.path.isdir(os.path.join(full, ATTACH)):
        errors.append(f'MISSING {ATTACH}: pod {folder!r} has none (every pod has one, empty or not)')

    # 4 and 5. Below the pod folder: no nested pod, and a flat _pod-attachments.
    for dirpath, dirnames, filenames in os.walk(full):
        dirnames[:] = [d for d in dirnames if d != 'under-development']
        if dirpath == full:
            continue
        rel = os.path.relpath(dirpath, ROOT)
        if os.path.basename(dirpath) == ATTACH:
            if os.path.dirname(dirpath) != full:
                errors.append(f'NESTED POD: {rel!r} is a pod marker below pod {folder!r} (pods do not nest)')
            if dirnames:
                errors.append(f'NESTED FOLDER IN {ATTACH}: {rel!r} contains {sorted(dirnames)} (attachments are flat)')
        stray = sorted(f for f in filenames if f.endswith(SUFFIX))
        if stray:
            errors.append(f'NESTED POD: {rel!r} holds {stray} below pod {folder!r} (pods do not nest)')

print(f'{ROOT}: ' + (f'{len(errors)} issue(s) found:' if errors
                     else 'OK — flat, one pod per folder, none nested.'))
for e in errors:
    print(' -', e)
```

If a `TOO MANY PODS` or `NESTED POD` issue is found, move the extra pod out to its own new folder directly in `example/Pods/`, named after the pod. A `STEM MISMATCH` means the databook's filename or its folder is misnamed; rename whichever is wrong, and keep `title:` in step (YAML-5). An empty/placeholder folder is not necessarily an error — flag it to the user rather than deleting it, since it may be a deliberate placeholder for content not yet added. Pod-databook files routinely carry substantial body content (one `### Graph NN` section per embedded graph) — this is expected and not itself a violation of this check, which only validates folder layout, not file size or content.

**FS-6 — every image on disk is referenced by the documentation**: FS-4 verifies the forward direction — that every image a document references actually exists. This is the inverse: that every PNG under `images/` and `example/images/` is referenced by at least one Markdown file. An unreferenced image is normally a misplaced export or a leftover from a renamed diagram, invisible to every other check precisely because nothing points at it; without this check such a file can sit in the tree indefinitely and be committed by accident. Note this deliberately covers only the two diagram directories, not `example/graphs/images/`, whose per-graph PNGs are generated by `helpers/draw.py` and linked from example.md's graph tables rather than embedded. Run:

```python
import re, glob, os

DIRS = ['images/**/*.png', 'example/images/*.png']
docs = [f for f in glob.glob('**/*.md', recursive=True)
        if 'under-development' not in f.split('/')]

referenced = set()
for f in docs:
    text = open(f, encoding='utf-8').read()
    referenced |= set(re.findall(r'(?:example/)?images/[\w./-]+\.png', text))

on_disk = set()
for pattern in DIRS:
    on_disk |= set(glob.glob(pattern, recursive=True))

orphans = sorted(on_disk - referenced)
for o in orphans:
    print(f'VIOLATION {o}: present on disk but referenced by no Markdown file')
print('Every image on disk is referenced by the documentation.' if not orphans
      else f'{len(orphans)} unreferenced image(s) found.')
```

If a violation is found, decide which way the discrepancy should be resolved: either the image is wanted, and whichever document should embed it is missing its reference (add it, and see FS-4 for the forward direction), or it is a stray — a save that went to the wrong folder, or the old name of a renamed diagram — and should be deleted. Do not simply add a reference to make the check pass; an image nothing needed is a file that should not be in the tree.
