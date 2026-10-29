# Pod DataBook File Format

## Development Scaffolding

**This file specifies an artifact that will not exist once the Tellipod app ships, and describes a
filesystem layout that will not exist either.** Tellipod persists no data in the user's filesystem at all:
a pod's entire content — everything this document describes, plus the note, the attachments, the
chat and the member's own private files — lives in a protected, app-managed store, encrypted at
rest. See [storage.md](storage.md) for that decision and the reasoning behind it. A running Tellipod
produces no folders, no `.databook.md` file, and no files of any kind.

The app does not exist yet, and `example/Pods/` is how this project carries, validates and diagrams
real pod content in the meantime. So the DataBook lives on disk here, as **development
scaffolding**: three helpers read those files (`helpers/validate.py`, `helpers/yaml-to-rdf.py` and
`helpers/extract-all.py` discover them by globbing `*.databook.md`; `helpers/extract-graph.py` and
`helpers/draw.py` take one as an argument), and seventeen of integrity.md's checks do too. When the
app ships, all of that has to move to whatever the app exposes instead.

The scaffolding is not only the file. The folder around it is scaffolding too, and so is everything
in that folder:

- **A folder stands for a pod, and the reserved `_pod-attachments` folder directly inside it is
  what marks the folder as one.** This gives the repo a pod/not-a-pod test decidable from a single
  folder's immediate contents, with no tree walk — which is what [integrity.md](integrity.md)'s
  FS-5 relies on. Both markers are present here, the folder's and the file's, and FS-5
  requires them to agree; that is what keeps the scaffolding from drifting away from the tree it
  represents. At runtime nothing marks a pod, because there is no folder to mark.
- **A pod's note is a file named after its folder** (`X.md` inside the folder `X`), the folder-note
  convention PKM tools such as Obsidian use. The file is plain Markdown, a stand-in approximating
  what the app's Markdown export of the note would write. At runtime the note is app-internal, held
  in the app's own format rather than as Markdown, and has no name of its own.
- **A pod's attachments are the plain files inside its `_pod-attachments` folder, and the member's
  own private files are the ones loose beside it.** At runtime the same distinction is a rule about
  what propagates on a share, decided by how the member filed the file in the app, not by which
  directory it sits in.
- **The [Filename Convention](#filename-convention) below is scaffolding-only.** At runtime there is
  no file, so there is no filename, and nothing depends on one.
- **Nothing records a pod's position in the tree.** Here that is because the position is simply
  wherever the folder currently sits; at runtime it is because a pod's parent is per-member state
  in that member's own store. The invariant holds either way, and `pod:Pod` asserts no tree position
  in either case.

Everything below therefore describes the repo's filesystem, not a user's. Where this repo's layout
and the model appear to disagree, this document is the one to read; [storage.md](storage.md) draws
the boundary, and every other file in the project describes the model and points back here for the
layout.

## What a Pod DataBook Is

A **pod DataBook** is the file that carries a pod's structured content. It is a
[DataBook](https://github.com/w3c-cg/holon/tree/main/architectures/databook) — a Markdown file with
YAML frontmatter, extension `.databook.md` — sitting directly inside the folder this repo uses to
stand for the pod whose content it carries. See [Pod Contents](app-behavior.md#pod-contents) in
app-behavior.md for what a pod actually holds, and [Development Scaffolding](#development-scaffolding)
above for why it is a folder here and nothing at all at runtime.

One pod DataBook carries three things:

- **document fields** — six YAML keys describing the file itself, above the `tpod:` block;
- **the `tpod:` block** — the pod's category, its creator and owners, its tags, and its links to the
  graphs below, whose keys map onto properties defined in `pod.ttl`. See
  [Pod Ontology](README.md#pod-ontology) in README.md for what each property *means*; this
  document says how each is *written*;
- **the body** — one `### Graph NN` section per graph the `tpod:` block links, each holding that
  graph's own Turtle.

A graph has no file of its own: it lives inside the pod DataBook that links it, as one
`tpod.member`/`tpod.tool[].graph` entry plus one body section.

**Nothing in the file records where the pod sits.** There is no tree-position field, no parent
link, and no back-pointer from a graph to the pod that links it — a pod asserts `tpod.member` and
`tpod.tool`, and that is the only direction the link runs. In this repo a pod's position is simply
wherever its folder currently sits, and a graph's containing pod is simply wherever its entry
physically lives, so moving or renaming a folder is a pure filesystem operation with nothing in any
file to update. The invariant is the same one the model asserts for its own reason — a pod's parent
is per-member state in that member's own store, never shared content — which is what lets two members
of a shared pod each file it wherever they like without touching content the other sees. It is also
why two pods can never share a folder here: a file sitting in it would be ambiguously part of both,
and the marker being a folder of one fixed reserved name, of which a directory can hold only one,
makes that structurally impossible rather than merely forbidden.

**The rest of a pod's content is not in this file.** The DataBook holds the structured content and
the metadata about the pod itself; a pod's unstructured content sits beside it:

- **the note** — one Markdown file named after the folder (`X.md` inside the folder `X`), shown in
  the app's Note area. Naming it after its folder is the folder-note convention PKM tools such as
  Obsidian use, which is what lets this repo's tree be browsed in one. It is Markdown because that
  is what the app's export of a note writes, not because the note is Markdown: a link to another
  pod is written in the export's `[[id|text]]` form, and a link to a block inside the pod has no
  syntax here at all (see [Where the note's format and block links go](#where-the-notes-format-and-block-links-go));
- **the attachments** — the plain files inside the folder's own `_pod-attachments` subfolder, flat,
  like email attachments. Every pod has that subfolder, empty or not, and its contents are the part
  of a pod's folder that travels when the pod is shared;
- **the member's own private files** — every other plain file loose in the folder, and any subfolder
  with no pod anywhere beneath it. These stay in that member's copy of the pod and never reach
  another member. The remaining two kinds of subfolder are not the pod's content at all: a
  descendant pod, holding its own `_pod-attachments` folder, and a bare pass-through directory on
  the way to one (integrity.md's FS-5);
- **the chat** — a stream shared by the pod's members, not a file in the folder at all; like this
  file's own content, it lives inside the app.

None of these is named or listed anywhere in the DataBook. There is no attachment manifest and
no note-filename field: here the note is found by its name and the attachments by reading one
reserved folder, so adding a file to a pod is just putting a file in that pod's folder — and
attaching it, so that every member gets it, is just putting it in `_pod-attachments` instead. At
runtime the same two acts are ordinary app operations, and the attached/private distinction is a rule
about what propagates rather than about where a file sits. `pod:attachment` is a real `pod.ttl`
property, its values `sources:SourceItem`s, but the example DataBooks carry none of its triples: in
this scaffolding the `_pod-attachments` folder stands for it. `pod:note` and `pod:chat` are
documentation-only properties — described in README.md's
[Documentation-only Properties](README.md#documentation-only-properties), declared in no ontology,
and never written as a triple by anything (integrity.md's PNG-3).

This document specifies the DataBook file and the folder this repo wraps it in; for what a pod
holds in the app, see [Pod Contents](app-behavior.md#pod-contents) in app-behavior.md, and for the
boundary between the two, [storage.md](storage.md). For real files, see `example/Pods/` and
[example.md](example.md).

## Why This Format

This is not how the app persists a pod — nothing is persisted as a file at all (see
[storage.md](storage.md)). It is how *this repo* carries one, and two properties are what make the
format the right shape for that job.

**It is human-readable.** A pod DataBook is Markdown with YAML frontmatter, so a pod's content can
be navigated, inspected, and edited with ordinary tools, which is the only way it can be worked on
before there is an app. Maintaining this repo's own example tree in VS Code and Claude Code is the
demonstration: everything the format carries is legible as text, and anything wrong with it is
visible in a diff. That property belongs to the scaffolding rather than to Tellipod, and it is worth being
clear about what it does not buy: a format made of ordinary files in ordinary folders was once also
an argument that Tellipod's storage could interoperate with a PKM vault such as Obsidian. It cannot, and
that argument is retired — Tellipod writes no files for a vault to see.

**It is machine-verifiable.** The format is constrained from three directions: SHACL shapes
validate a pod's synthesized triples, [integrity.md](integrity.md)'s checks cover what SHACL cannot
express, and [CLAUDE.md](CLAUDE.md) records the conventions behind both. Together they are a
diagnostic independent of the app — a second reading of the same rules, against which whatever
validation Tellipod implements internally can be checked. A single implementation has nothing to disagree
with.

The format will change, though. It has so far been exercised by one worked example and the
validation pipeline around it, not by an implementation, and the Tellipod implementation team will find
requirements it does not yet meet — a field that has to be added, a convention that holds across the
example tree but not across a real user's, a distinction that only matters once pods are syncing
between real instances. The largest known gap is tools: four of the six kinds have no data format
at all yet. See [Open Questions](#open-questions) at the end for that and the rest of what is
still unsettled. This document tracks the format as it stands rather than freezing it; what
keeps a proposed change honest is that [integrity.md](integrity.md)'s checks and the tree under
`example/Pods/` make its blast radius visible before it is made.

## Filename Convention

**Scaffolding only.** At runtime there is no file and so no filename; nothing in a running Tellipod
depends on any of this section. It governs the DataBooks in this repo, and it is what integrity.md's
FS-5, YAML-5 and PNG-9 read.

Pod-databook filenames follow (there is no separate category-databook file — a folder's sole
DataBook is its pod-databook, see [Pod/Category split](CLAUDE.md#key-architectural-patterns)):

```
<local>(<catType>).databook.md  — pod-databook
```

`<local>` is an **exact copy of the folder's own name** — verbatim, no kebab-casing, no lowercasing,
whatever case/spacing/punctuation the folder itself has (e.g. `Acme`, `Paula Walker`, `ATT`). There
is no `-pod` token: pod-databook is the sole DataBook type in a user's instance tree, so nothing
needs to be disambiguated by it. There is also no numeric disambiguator of any kind (no `-2`, `-N`,
etc.): a folder holds **at most one** pod-databook, ever. (What marks a folder as a pod
in this repo is its `_pod-attachments` folder, not this file; FS-5 requires the two markers to
agree, so in practice a pod folder carries exactly one matching pod-databook and a folder with
neither marker is simply a plain filesystem folder.) `<catType>` is the folder's own category classification,
kebab-cased (e.g. `Employees` → `employees`, `ImmediateFamily` → `immediate-family`, `SSN` → `ssn` —
kebab-casing is acronym-aware: a hyphen is inserted only at a lowercase→uppercase boundary or an
uppercase-run→lowercase boundary, so consecutive capitals stay together). If the matched category
concept's own local name carries a literal `(org)` disambiguator (used only to distinguish it from a
same-named Person-side sibling concept, e.g. `podcat:BankingPayments` vs. `podcat:BankingPayments(org)`),
that suffix is dropped before kebab-casing — `<catType>` only ever needs to disambiguate a
*recurring folder name* by role (e.g. were the same person to appear both as a leaf under
`Employees` and as one under `ImmediateFamily`, both Person-side), never the Person/Organization
split itself, which is already carried by the folder's own tree position and by `pod:category`'s
actual asserted value, never by the filename. So a bank pod whose `pod:category` is
`podcat:BankingPayments` (Person-side, since it's the person's own relationship with the bank, not
company business filed under `Work`) is named `<local>(banking-payments).databook.md` with no `-org`
marker, and the same bare `banking-payments` `<catType>` would apply identically if a pod's
`pod:category` were instead the org-side `podcat:BankingPayments(org)`, since nothing in the filename
needs to tell the two apart.

A pod-databook's `<catType>` parenthetical is purely a filename-level disambiguator — `podcat:catType`
does not exist in RDF at all, so nothing in RDF records it, and nothing reverse-matches the filename
to derive it. The one RDF-level echo of a folder's classification is `pod:category`, read directly
from the pod-databook's own explicit `tpod.category` field (see [The `tpod` Block](#the-tpod-block)), not
derived from the filename at all. Unlike the filename, a pod-databook's `id:` is deliberately *not*
derived from the folder name either — see [`id`](#id) below.

**UserDefined folders — `<catType>` is the literal `custom`**: a pod may legally carry no
`pod:category` at all — this is the UserDefined category, for a pod the user created without picking
any existing category concept. What identifies such a pod is simply that it carries no `category`
value; the filename literal below is this repo's way of making that visible on disk, not the test
itself. Since there is no category concept to kebab-case into `<catType>`, the filename uses the
fixed literal string `custom` in its place, e.g. a folder named `Friends` with no category is
`Friends(custom).databook.md`. The two must always agree — no `tpod.category` iff a `(custom)`
filename — which is what integrity.md's PNG-9 enforces in both directions. The compression rule below still applies verbatim on
top of this (a folder literally named "Custom" would compress to `Custom.databook.md`, though no
real example does this) — `custom` is just an ordinary `<catType>` value from the filename's point
of view, it just happens to never come from kebab-casing a `skos:prefLabel`.

**Compression rule**: if `<local>`, normalized the same acronym-aware way `<catType>` already is, is
identical to the kebab-cased `<catType>`, the parenthetical is dropped entirely, since it's pure
redundancy — `<local>.databook.md` — rather than `<local>(<local>).databook.md`. For example
`podcat:Work`'s folder is named `Work`, and its own `catType` (`Work`) also kebab-cases to `work` — the
same string — so its file is `Work.databook.md`, not `Work(work).databook.md`. This applies on a
normalized-equal match, not raw string identity (since `<local>` itself is never kebab-cased):
folder `Health & Wellness`'s catType `HealthWellness` both normalize to `health-wellness`, so it
compresses too, to `Health & Wellness.databook.md`. `Acme(organization).databook.md` keeps its
parenthetical since normalized `Acme` (`acme`) ≠ `organization`. Most of a tree's top-level scaffold
compresses this way, since these folders' own name simply *is* their category.
`Banking & Payments Firms(banking-payments).databook.md` is a further example of the
non-compressing case: normalized `Banking & Payments Firms` (`banking-payments-firms`) ≠
`banking-payments`, since the folder's own name matches `podcat:BankingPayments`'s full
`skos:prefLabel` ("Banking & Payments Firms") rather than a shortened form.

Folder naming is standardized as the category's own display label (the OS folder name is used
verbatim, with no override field anywhere — the pod-databook's own `title:` field mirrors this name
exactly rather than overriding it, see integrity.md's YAML-5), but a folder's own name alone can't
disambiguate a repeated name's *role* — the same person can legitimately appear at two different
tree positions, e.g. as a leaf under `Immediate Family` and again as a leaf under an employer's
`Employees`, both folders literally named after them — so `catType` carries that role encoding in
the filename instead, not derived from folder position. Such a pair never collides: one would be
`<name>(immediate-family).databook.md` and the other `<name>(employees).databook.md` (an employee
pod reuses the "Employees" scaffold's own category directly, the same "child folder reuses its
parent's category" pattern a pet's own pod under `Pets` already uses — there is no separate
narrower "Employee" category).

## Frontmatter

Every pod DataBook opens with the same six YAML fields, above its `tpod:` block and in this order:
`id`, `title`, `type`, `version`, `created`, `description`. They describe the DataBook itself rather
than the pod's content — only `id` reaches RDF at all, and none of the six corresponds to a
property in `pod.ttl`. The pod's content proper is the `tpod:` block below them, documented in
[The `tpod` Block](#the-tpod-block).

<a id="pod-id"></a>

### `id`

The pod's own id, and the RDF subject every triple synthesized from this DataBook hangs off —
`helpers/databook_graphs.py` reads it directly as the subject IRI of the `pod:Pod` individual. It is
the one frontmatter field with ontology weight, and the one field a DataBook cannot omit. It is
deliberately *not* derived from the folder name or the filename (see
[Filename Convention](#filename-convention)): encoding a name into it would risk a collision the
moment two folders elsewhere in the tree shared both a name and a category, and nothing depends on
the id's string structure.

A pod's id is globally unique across every user's independent tree, not merely within one person's
own. It is flat and opaque, never derived from the pod's own name or category, and no registry or
central coordination assigns it — consistent with no pod, and nothing about it, ever being held by
a cloud provider or third party (see [Pod Storage](app-behavior.md#pod-storage)), and with
`:Self`'s purely-local identifier (see
[`:Self` IRI convention](CLAUDE.md#key-architectural-patterns)). Instead, it is derived from its
creator's identity and freshly generated random bytes (`‖` is byte concatenation):

```
nonce     = 16 random bytes
pod_id    = BLAKE3 derive_key("pdn/pod-id/v1", pdn_id ‖ announcement_pubkey ‖ nonce), first 16 bytes
signature = sign(announcement_secret, "pdn/pod-founding/v1" ‖ pdn_id ‖ announcement_pubkey ‖ nonce)
```

`pdn_id` is the creator's PDN ID; the announcement key pair belongs to their identity, shared by all
their devices, not to one device. The id is written as 32 lowercase hex characters. `pdn_id`,
`announcement_pubkey`, `nonce` and `signature` are stored in the pod's founding event — the first
event in the pod's membership store; the id itself is not stored.

A founding event is valid only when the id recomputed from its fields matches and its signature
verifies (see [Deriving and Checking a Pod Id](app-behavior.md#deriving-and-checking-a-pod-id)).
This is what prevents a member from feeding a device that already knows the id (from its identity's
records or a note link) a forged history with a different founder — a random id such as a Tellipod UUID
names no one and cannot. The context strings keep this hash and signature apart from any other made
over the same bytes; without the founding event, which only members hold, the id reveals neither
creator nor creation time.

This repo's own example data uses sequential `http://www.example.org/tpod/pods/pod-<NN>` ids instead
(see integrity.md's YAML-3) — the same flat, opaque shape, deliberately simple for one worked
example living entirely under a single shared example domain, and not unique once real pods belong
to many different users' independent instances.

### `title`

The pod's own name, and always exactly the name of the filesystem folder holding the DataBook —
verbatim, same case, spacing and punctuation. Within this scaffolding the folder is authoritative:
renaming the folder means updating `title:` to match, never the reverse, and `title:` is never an
independent display-name override (integrity.md's YAML-5, which also treats it as authoritative
for what a pod "is called" when matching diagram box labels). At runtime the app's own record of
the name is authoritative outright, there being no folder to mirror. It is shared, synced pod content, kept identical across every
member's copy, and any member may rename the pod — see
[Naming, Renaming, and Sharing](app-behavior.md#naming-renaming-and-sharing) in app-behavior.md for
the one exception, a bare two-member pod, whose name is instead independent per member.

### `type`

Always the literal `pod-databook` — the only DataBook type in this repo's instance tree, so no
`-pod` token is needed to tell one DataBook kind from another. It does not identify a pod: that is
the `_pod-attachments` folder's job (see [Pod Contents](app-behavior.md#pod-contents)
in app-behavior.md). It is also the tooling's file filter: both
`helpers/yaml-to-rdf.py` and `helpers/validate.py` skip any DataBook whose `type` is anything else,
so a wrong value silently drops the pod from RDF synthesis and validation alike rather than
raising. No integrity check asserts the value.

### `version`

A hand-maintained [semantic version](https://semver.org/) for this one DataBook's own content. No
integrity check enforces it and the repo defines no bump rule, so it carries whatever meaning its
author gave it; in the example tree the values run from `1.0.0` to `2.2.0`, always with a zero patch
component. It is not synthesized into RDF. JSContact's `updated` property maps onto this field
rather than onto any ontology property — see the JSContact mapping table under
[Contact-Related Classes and Properties](README.md#contact-related-classes-and-properties) in
README.md.

### `created`

An unquoted ISO 8601 calendar date, `YYYY-MM-DD`, recording when the pod was created. Hand-entered:
no check reads it, nothing derives it from the filesystem or from git, and it is not synthesized
into RDF.

### `description`

A prose summary of the pod, written as a folded block scalar (`description: >`). Not used by any
tooling and not synthesized into RDF. Throughout the example tree it follows one house style: it
opens `Pod DataBook for folder "<title>" (pod:category: podcat:<Concept>)`, optionally noting where
the pod is nested or whose category it reuses, then characterizes the pod's own shape — how many
members it has, and what its tool is about if it carries one.

## The `tpod` Block

Below the six document fields sits a single `tpod:` mapping carrying the pod's own content. Its
scalar-valued keys map one-for-one onto properties defined in `pod.ttl`:

| YAML field | Ontology property | Cardinality | Meaning |
|------------|-------------------|-------------|---------|
| `tpod.category` | `pod:category` | 0..1 | The category concept this pod was originally instantiated as — a `skos:Concept` individual in `podcat:PodCategoryScheme` (e.g. `"podcat:Others"`) or in a [category extension](README.md#category-extensions)'s own scheme (e.g. `"bhscat:BostonHubSociety"`); absent otherwise. Fixed at creation, not re-derived from the folder's current name. A hint for a recipient's app when this pod is shared with another member |
| `tpod.creator` | `pod:creator` | 1 | Who created this pod's content — a `p:Person` |
| `tpod.owner` | `pod:owner` | 1+ (required, no upper bound) | Which of the pod's members hold the owner role — always includes `tpod.creator`'s own value; a `p:Person`, never an `s:Service` |
| `tpod.userTag` | `pod:userTag` | 0..N | A free-text tag the user minted (e.g. a pet's name, to gather every pod about that pet). Shared pod content |
| `tpod.serviceTag` | `pod:serviceTag` | 0..N | A tag written by this member's own service module for its own bookkeeping. Each entry is a mapping of three sub-keys — `namespace`, `key`, `value` (`pod:tagNamespace`/`pod:tagKey`/`pod:tagValue`), e.g. `namespace: "foundation.mee.applecontacts"`, `key: "group"`, `value: "Christmas List"` — not a single string. Never displayed and never findable by the user — reachable only by the writing module, within its own namespace — and **local to this member's copy** — the one piece of pod content that does not propagate on a share |

Values are written as quoted CURIEs (`"podcat:Pets"`) or bare local names (`":Self"`); both are
resolved to full IRIs by `helpers/databook_graphs.py`. **Any key whose cardinality allows more than
one value may be written either as a YAML list or, when it holds a single value, as a bare scalar** —
`owner: ":Self"` and a one-item list are equivalent, and the same latitude applies to `member`
below.

There is no *pod-level* `tpod.subject` field — who or what a pod's content is about is derived from
`tpod.member`/`tpod.tool` rather than asserted independently (see integrity.md's YAML-4); the
`subject:` key that does appear sits inside each `tpod.member` entry, naming that member rather than
the pod's own subject.

The two remaining keys, `tpod.member` and `tpod.tool`, are link-valued: each entry names one graph
embedded in this same file's body. In ontology terms:

| Property | Value | Cardinality | Meaning |
|----------|-------|-------------|---------|
| `pod:member` | `pod:MemberGraph` | 1+ (required, no upper bound) | The required baseline of self-vs-other classified graphs backing this pod's content — one or more per member in the relationship — distinguished by each linked graph's own `pod:subject`/`pod:claimant` combination rather than by separate properties or classes |
| `pod:tool` | `pod:Tool` | 0..N — a pod with none is the ordinary case, and nothing caps how many it may carry (see [Tools](README.md#tools)) | Each tool brings its own data format and its own UI contribution; a form tool states, once, what its content is about (`pod:formTopic`) |
| `pod:formGraph` | `pod:FormGraph` | 1+ (required) on a live `pod:Form`, capped in practice at the pod's own member count, per tool (see integrity.md's YAML-8) | The graphs beneath one tool, one per claiming member; a different range from `pod:member`, since a tool's `pod:formTopic` need not be a PDN-mappable identity |

Nothing in an entry marks its own kind. The list it sits in settles it: a `tpod.member` entry is a
`pod:MemberGraph`, a graph under a `tpod.tool` entry is a `pod:FormGraph`. The two are `owl:disjointWith`,
so neither ever carries the other's fields.

### `tpod.member` Entries

One entry per member graph — at least one required, no upper bound. A single entry may be written as
a bare mapping rather than a one-item list. Sub-keys:

| Sub-key | Required | Value |
|---------|----------|-------|
| `id` | yes | The graph's full IRI — see [Graph Ids and Named Graphs](#graph-ids-and-named-graphs) |
| `claimant` | yes | Who is making the claim — see [`claimant` Vocabulary](#claimant-vocabulary) |
| `subject` | yes | The party whose member entry this graph is — see [`subject` / `formTopic` Vocabulary](#subject--formtopic-vocabulary) |
| `shape` | no | The `sh:NodeShape` CURIE the graph's content conforms to (`pod:shape`), e.g. `"pshapes:ContactInfoShape"`. May itself be a list where one graph's content satisfies several shapes at once. A graph with no `shape:` is skipped by the template validation pass |

### `tpod.tool` Entries

One entry per tool the pod carries; zero is the ordinary case. Always written as a list. Sub-keys:

| Sub-key | Required | Value |
|---------|----------|-------|
| `id` | yes | The tool's full IRI — see [Tool Ids](#tool-ids) |
| `type` | yes | Which tool class this is: `form`, `calendar`, `canvas`, `contacts`, `map` or `browser`, mapping to `pod:Form`/`pod:Calendar`/`pod:Canvas`/`pod:Contacts`/`pod:Map`/`pod:Browser`. Only `form` has a content model today. `form` and `browser` are the two that appear in the example tree, `browser` only in the PRIVO and Facenook pods |
| `formTopic` | yes on a form | What the tool's content is about (`pod:formTopic`) — any resource IRI, stated once by the tool rather than repeated on each graph beneath it |
| `graph` | yes on a form | A list of that tool's own graph entries, at least one |

Each entry in `graph:` carries `id`, `claimant`, and optionally `shape`, exactly as a `tpod.member`
entry does — but **never `subject`**: a tool graph's about-ness lives one level up, on the tool's
single `formTopic`.

<a id="graph-ids"></a>

## Graph Ids and Named Graphs

A graph lives physically inside its owning pod-databook's `tpod.member`/`tpod.tool[].graph` entries and
body (see [Pod/Category split](CLAUDE.md#key-architectural-patterns)) — it has no file or
filename of its own. Each entry's own `id` (which doubles as the graph's
own named-graph identity, `{id}#graph`) does not re-encode `claimant`/what the graph is about/the
containing pod into the id string, since those facts are already carried by that same entry's own
sibling `claimant:` and `subject:` fields, or its tool's `formTopic:`, and the containing pod is
simply wherever the entry physically lives — encoding them a second time would be pure redundancy.
It follows a single flat pattern instead:

```
http://www.example.org/tpod/graphs/graph-<NN>
```

`<NN>` is the same graph number used everywhere else for this graph — the diagram label, the
`### Graph NN` body heading, and its `<a id="graph-NN">` anchor. It is zero-padded to two digits up
to `graph-99`, and runs on into three digits from `graph-100` — the numbers are minted in one flat
sequence with no leading zero beyond that padding, so `graph-09` and `graph-100` are both
well-formed while `graph-009` is not. A `tpod.member`/`tpod.tool[].graph` entry carries this full IRI
directly as its own `id` field — there's no separate list to cross-reference it against.

**DataBook IRI convention**: a document's `id:` and its `graph.named_graph:` always differ by the
`#graph` fragment — `named_graph` is always `{id}#graph`. The `databook:id` on a block is a fragment
identifier making that block independently addressable as `{id}#{block-id}`.

### Tool Ids

A live tool is named by its own IRI, carried as its `tpod.tool` entry's `id`, and that IRI is the
tool's id. It exists so that a block link in the pod's note — a link to one of the pod's own tools
(see [Pod Contents](app-behavior.md#pod-contents) in app-behavior.md) — has something stable to
resolve by. A tool's position among its pod's tools would not do: reordering the tools, or removing
one, would silently retarget every link to the tools after it.

At runtime the app mints a tool's id when the tool is created, whether the person adds it with Add
Tool or Lazy Instantiation clones it from a template's declared tool. Like a pod id and a graph id,
it is flat, opaque and globally unique, generated from fresh random bytes and never derived from the
tool's kind, its `formTopic`, its position, or the pod that holds it. It is fixed for the tool's
lifetime, and when the tool is removed its id is retired, never given to another tool, so a stale
block link shows as unresolved rather than landing on a newcomer.

A tool's id names the tool node itself, not a named graph: a tool holds graphs, each with its own
`id`, but is not one, so there is no `{id}#graph` counterpart. A tool declared by a template
(`pod:declaresTool` in `pod-category-templates.ttl`) has no id at all — it is a class-level
declaration, never a block-link target — and is a blank node; the live tool cloned from it gets a
fresh id of its own.

This repo's example data uses a flat sequence instead, under the same example domain as its graphs
and pods:

```
http://www.example.org/tpod/tools/tool-<NN>
```

padded the way graph ids are — two digits up to `tool-99`, three from `tool-100` — and numbered in
one sequence across the whole tree (integrity.md's YAML-10). As with a pod or graph id, an existing
tool id is never renumbered.

### `:Self` and Locally-Minted IRIs

The three about-ness and attribution fields below all hold individual IRIs, minted by one
convention. The user's own `p:Person` individual always uses the IRI `:Self`, in every graph in
their own instance. Everyone else — other people, organizations, groups, services — gets a
locally-minted named IRI (`:Bob_Johnson`, `:Acme`).

`:Self` is local and is never exposed over the PDN, so two instances of the app never collide on it:
in each instance it names that instance's own user, and nothing has to reconcile the two. A graph
that arrives from a peer, where that peer was `:Self` in their own instance, is rewritten on receipt
so `:Self` still means the receiving user; the peer is assigned a locally-minted identifier of the
receiver's own, which resolves to or is replaced by their PDN ID once a connection is established.

This is why the example tree can be read as one user's instance throughout even though some of its
graphs were authored by other people: `:Self` is Alice's everywhere in it, whoever wrote the claim.

### `claimant` Vocabulary

A `tpod.member`/`tpod.tool[].graph` entry's own `claimant:` field takes the local IRI of a `p:Person`,
`o:Organization`, or `s:Service` individual. Which of the three a graph names turns on who is
*really* making the claim, not on which member mechanically carries it. Specifically: `:Self` (the
user's `p:Person`) for self-claimed graphs; a named `p:Person` individual when another user claims
the data; a named `o:Organization` individual for content contributed by a `s:ServiceProvider` that
organization provides, since the organization is the responsible party and the one an eventual
cryptographic signature would name; and a named `s:Service` individual for a service with no
organization standing behind it in the relationship. Note that an organization claimant need not be
a member subject — it is reached from one via `s:providedBy`, which is what integrity.md's YAML-8
allows for.

**"Other" claimants**: When the claimant is someone other than the current user (`:Self`), the
claimant is a named individual of one of:

- `p:Person` — another user (a different person claiming data about the user)
- `o:Organization` — a company, nonprofit, or government agency that is a PDN node, claiming on
  behalf of the `s:ServiceProvider` it provides
- `s:Service` — a service claiming under its own IRI, with no organization behind it in the
  relationship (e.g. an invited agent service, or a pod backup service)

An organization only ever appears as a claimant when it is PDN-interoperable. Where it is not, the
user self-enters that data and the claimant is `:Self`. (This distinction is currently a
data-modeling convention, not something any property formally enforces.)

### `subject` / `formTopic` Vocabulary

Which of the two about-ness fields applies is settled entirely by the list the entry sits in — a
`tpod.member` entry is a `pod:MemberGraph` and carries `subject:` (the party whose member entry it is,
always a PDN-mappable identity), a graph under a `tpod.tool` entry is a `pod:FormGraph` and carries no
about-ness field of its own — its topic is the holding tool's single `formTopic:` (what the content
is about, which need not be a PDN identity at all). Neither kind ever carries the other's field. See
`pod.ttl`, and [Graphs](README.md#graphs) in README.md, for why the two are separate properties on
separate disjoint classes.

**Examples** (id local-name, which list it sits in, and the corresponding field values found in that
same `tpod.member`/`tpod.tool[].graph` entry), drawn from the worked example in
[example.md](example.md):

| Id local-name | List | About (`subject`/`formTopic`) | Claimed by | Containing pod |
|----------|------|---------|-------------|---------------------|
| `graph-76` | `tool` | Self (Alice) | Citibank | Citibank(banking-payments) |
| `graph-07` | `tool` | Sophia Walker | Self (Alice) | Sophia Walker(immediate-family) |
| `graph-92` | `tool` | BHS | BHS | Boston Hub Society |
| `graph-08` | `member` | Self (Alice) | Bob Johnson | Bob Johnson(others) |
| `graph-03` | `member` | Bob Johnson | Bob Johnson | Boston Hub Society |
| `graph-01` | `member` | BHS's service | BHS | Boston Hub Society |

<a id="body"></a>

## Body Structure

Below the closing `---` of the frontmatter, the body holds one section per graph the `tpod:` block
links — every graph, whether it came from `tpod.member` or from a `tpod.tool`'s own `graph:` list, in
one flat sequence under a single `## Graphs` heading. Nothing in the body says which list a graph
came from; the frontmatter already settled that.

Each graph contributes exactly four things, in this order:

1. **An HTML anchor** — `<a id="graph-NN"></a>`, making the section linkable as
   `<file>.databook.md#graph-NN`. example.md's tables link every graph this way.
2. **A `### Graph NN` heading**, with the same `NN` as the anchor and as the entry's own `id`.
3. **A `#### Overview` subsection** — prose saying what the graph holds and why. By convention these
   open "This graph captures…".
4. **A `#### Graph` subsection** holding a single fenced ```` ```turtle ```` block: the graph's
   content.

The fence opens with two HTML-comment marker lines before any prefix declaration:

```
<!-- databook:id: <human-readable-slug> -->
<!-- databook:graph: http://www.example.org/tpod/graphs/graph-NN#graph -->
```

`databook:graph:` is the `{id}#graph` named-graph IRI, and it is the marker the tooling actually
reads — `helpers/databook_graphs.py` isolates one graph's fence in a multi-graph file by matching
it. `databook:id:` is a human-readable slug making the block independently addressable; no script
reads it. Both marker lines are stripped from the extracted Turtle.

### Self-Containment

Every graph is self-contained: it carries everything needed to read it, and borrows nothing from any
other graph. Concretely, a graph re-asserts the bare `rdf:type` of every named individual it
references — `:Self rdf:type owl:NamedIndividual, p:Person` appears in each of the graphs that
mention `:Self`, not once in some shared file the others merge in, and the same holds for every other
named individual.

The repeated type declarations look redundant and are not. A graph is the unit that gets extracted,
validated, signed, and shared: one graph's Turtle pulled out on its own has to be complete RDF that
validates against its shape without the rest of the tree present. Nothing else in the format
guarantees that, and a single borrowed declaration would break it silently — the graph would validate
in a merged dataset and fail alone.

There is no separate file holding a user's identity data, and no exception for a named individual's
own type declaration. Every substantive fact lives in the graph it belongs to.

## Skeleton

A complete, minimal pod DataBook — one member entry and one form tool with one graph:

````markdown
---
id: http://www.example.org/tpod/pods/pod-NN
title: "Folder Name"
type: pod-databook
version: 1.0.0
created: 2026-01-31
description: >
  Pod DataBook for folder "Folder Name" (pod:category: podcat:Concept). One-member pod with
  one member entry about :Self and one tool graph about :Topic.
tpod:
  category: "podcat:Concept"
  creator: ":Self"
  owner: ":Self"
  userTag:
    - "a tag"
  member:
    - id: "http://www.example.org/tpod/graphs/graph-NN"
      claimant: ":Self"
      subject: ":Self"
      shape: "pshapes:ContactInfoShape"
  tool:
    - id: "http://www.example.org/tpod/tools/tool-NN"
      type: "form"
      formTopic: ":Topic"
      graph:
        - id: "http://www.example.org/tpod/graphs/graph-MM"
          claimant: ":Self"
          shape: "someshapes:SomeShape"
---

## Graphs

<a id="graph-NN"></a>
### Graph NN

#### Overview

This graph captures …

#### Graph

```turtle
<!-- databook:id: some-member-graph -->
<!-- databook:graph: http://www.example.org/tpod/graphs/graph-NN#graph -->
@prefix : <http://www.example.org/tpod#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix persona: <http://mee.foundation/ontologies/persona#> .

:Self rdf:type owl:NamedIndividual ,
               persona:Person .
```

<a id="graph-MM"></a>
### Graph MM

#### Overview

This graph captures …

#### Graph

```turtle
<!-- databook:id: some-tool-graph -->
<!-- databook:graph: http://www.example.org/tpod/graphs/graph-MM#graph -->
…
```
````

## What Validates This

No single tool checks the whole format. It is enforced in three places:

- **[integrity.md](integrity.md)** — PNG-2 (every graph has both an entry and a body section),
  YAML-1 (`graph-<NN>` id pattern), YAML-2 (entry well-formedness: which sub-keys each kind of
  entry carries), YAML-3 (`pod-<NN>` id pattern), FS-5 (folder ↔ pod-databook structure),
  YAML-5 (`title:` matches the folder's OS name), TTL-3/TTL-4 (a `shape:` value against the
  graph's own content, and against the pod's category's own template), YAML-9
  (`tpod.userTag`/`tpod.serviceTag` well-formedness), and YAML-10 (`tool-<NN>` id pattern and
  uniqueness).
- **`helpers/validate.py`** — synthesizes `pod:` triples from the frontmatter and runs SHACL
  (`shacl/pod-shacl.ttl` and friends) against them, plus a per-graph template pass driven by each
  entry's `shape:` value. See [Validation](example.md#validation) in example.md for the commands.
- **`helpers/databook_graphs.py`** — the parser, and the de facto machine-readable spec for which
  keys are actually consumed. It reads exactly: top-level `id` and `type`;
  `tpod.category`, `tpod.creator`, `tpod.owner`, `tpod.userTag`, `tpod.serviceTag[].{namespace,key,value}`;
  `tpod.member[].{id,claimant,subject,shape}`; and
  `tpod.tool[].{id,type,formTopic,graph[].{id,claimant,shape}}`. No other key is consumed anywhere; an
  unrecognized key is silently ignored.

## Open Questions

What this format does not settle. Each is a change to this document when it is settled, and each is
listed because a reader hitting it should be able to tell that it is genuinely open rather than an
omission.

### Where chat content goes

Every pod has one chat stream, always — `pod:chat`, 1..1, present even when empty — and it lives
inside the app, alongside the content this document specifies. That answers the question this section
used to leave open. It was open because chat had no place in the folder, unlike the note and the
attachments, and no place in the DataBook either, leaving it the one piece of a pod's content with
no specified storage at all. Once a pod's structured content is app-internal rather than a file,
chat simply goes where that content goes, and the reasons it never fit the folder stop mattering.

Two constraints shaped that answer and still bound the app's own design. A chat is unlike the other
content: a note is one document that members edit in place, concurrently, while a chat is
append-only, authored per message, potentially far larger, and read at its tail far more often than
in full. And a pod's chat area holds more than its group stream (see
[Chat Area](app-behavior.md#chat-area) in app-behavior.md): a direct message between two members is
seen by those two alone, and a direct message between a user and their own personal agent (@Telli)
by that user alone, so neither can live in shared, synced pod content the way the group stream can —
whatever holds a pod's chat has to hold messages with different propagation rules. A pod already has
two pieces of content that do not propagate on a share, `pod:serviceTag` and a member's own private
files, so the precedent exists; what is particular here is that the split runs *within* one feature
rather than between two properties.

What is genuinely still open is the storage format the app uses for it, which is an app-internal
question this document does not reach. Nothing about it is a filesystem question any more: a
transcript is not a file anywhere, so the only thing left to settle is how the app's own store holds
an append-only, mostly-read-at-the-tail stream with several propagation rules inside it.

### Where the note's format and block links go

A pod's note is a rich-text document held in the app's own internal format, not Markdown (see
[Pod Contents](app-behavior.md#pod-contents) in app-behavior.md). Like chat's storage format, that
format is an app-internal question this document does not reach; what reaches it is the
scaffolding's stand-in. The `X.md` file beside each DataBook is plain Markdown approximating the
app's Markdown export, and that export is lossy in exactly one place that matters here: a **block
link** — a link from the note to one of the pod's own tools, graphs or attachments — has no
Markdown equivalent and exports as its display text. So the scaffolding has no way to write one, and
no example note contains one.

What a block link resolves by is settled: every kind of target has an IRI of its own — a tool its
`id` (see [Tool Ids](#tool-ids)), a graph its `id` (see
[Graph Ids and Named Graphs](#graph-ids-and-named-graphs)), and an attachment the IRI of its
`sources:SourceItem` individual. What is open is only whether the scaffolding should carry a
block-link syntax of its own, so that an example note can exercise one; nothing needs it yet.

### Where a non-form tool's content goes

Only `pod:Form` has a data format today. Its content is graphs, and a graph is Turtle, which is why
every one of the 101 fences across this repo's example tree is a ```` ```turtle ```` one.
`pod:Calendar`, `pod:Canvas`, `pod:Contacts` and `pod:Map` are declared with no content model at all, so this document has
nothing to say about what a calendar's entries or a canvas's drawing surface look like on disk.
`pod:Browser` has none by design: the credentials it handles are pod attachments, not tool content.

Settling any of them lands in two places: a `tpod.tool` entry needs whatever keys that kind's data
calls for alongside `type`, and the body needs somewhere to put the content.
`formTopic`/`formGraph` are scoped to `pod:Form` precisely so a kind with a different shape is not
forced through them. A calendar's entries are plausibly still graphs, and so still Turtle; a canvas's
drawing surface is plausibly not, which runs into the next question.

### Where a tool's binary content goes

A drawing surface, a scanned document, a map's cached tiles — some of what a tool holds will not be
text. At runtime it is a blob in the app's own store like everything else, **referenced from the
graph rather than encoded into it**. The example tree already works this way for the one binary-ish
thing it carries: a passport photo and a driver's license photo, each an `xsd:anyURI` value on
`p:hasPhoto` rather than image data. In this repo's scaffolding such a blob is a file in the pod's
folder, so that git, a diff and the tooling all get to treat a PNG as a PNG.

Encoding it into the DataBook instead spends most of what recommends this format in the first place.
There are two ways to try, and the objection to both is the same:

- **Base64 inside the Turtle**, as an `xsd:base64Binary` literal, is legal RDF and needs no format
  change at all. But a megabyte of drawing becomes a single unbreakable line a third larger than the
  original — no longer readable as text, no longer diffable, and rewritten whole in git on every
  stroke.
- **A separate fenced block** tagged as something other than `turtle` carries the same size cost,
  and adds one of its own: `helpers/databook_graphs.py` matches the literal ```` ```turtle ````
  opener, so a differently tagged fence is passed over rather than rejected. Content put in one
  today is silently invisible to every tool in this repo rather than failing loudly.

Either could still be right for something small and genuinely inseparable from the claim carrying it
— a signature, a thumbnail — but not for a tool's working data, and the threshold at which "small"
stops applying is itself unset.

What stays open is the reference rather than the storage. A graph is claim content that propagates
between members on a share, so whatever it holds has to still resolve in a recipient's own copy of
the pod — after the pod has been renamed, refiled, or received under a collision-suffixed name (see
[Naming, Renaming, and Sharing](app-behavior.md#naming-renaming-and-sharing) in app-behavior.md).
An identifier scoped to the pod itself survives all three; anything anchored outside it does not. In
this repo a path relative to the pod's own folder is the scaffolding form of exactly that.

### How a tool's own files are told apart from the user's

A pod's files are already one of two things — an **attachment**, which every member receives, or one
of the member's own private files, which no one else does — and both are shown to the user in the
Attachments area. That is the whole definition. But a canvas's backing image is not something the
user attached, nor something they chose to keep back, and showing it in either set alongside the
files they did misrepresents both. So a tool's own files need a third disposition: neither the
pod's attachments nor the member's private files, and not shown in that area at all.

Now that a pod's content is app-internal, this is easier than it was — the app can simply hold a
tool's blobs outside both sets, with no reserved name or manifest needed to keep them apart, because
there is no shared directory for them to be found in by accident. What is still unsettled is the
propagation rule: a tool's blob plainly has to travel with the pod the way an attachment does,
without being one, and nothing yet says whether it follows the attachment rules exactly (immutable,
deletable by any member) or rules of its own. In this repo's scaffolding the question stays open in
its original form, since a file here does sit in a folder and would need a reserved prefix or a
second reserved subdirectory beside `_pod-attachments` to be told apart.
