# Connectors

*Tellipod pod ontology — concept summary, 2026-11-20*

## The problem

`pod:Tool` covered two different things:

- **Content tools** — a form, a calendar, a drawing canvas, a map. These hold data inside the pod that every member shares. A form tool holds one graph per claiming member, all about the tool's single `pod:formTopic`.
- **Device links** — an address-book sync (`pod:Contacts`), a connection to a web browser through the Tellipod extension (`pod:Browser`). These hold no pod content. They link one member's copy of the pod to something on that member's own device.

All of them sat on `pod:SharedPod` via `pod:tool`, so a device link was treated as shared content, and it can't be. A member on an Android phone gets nothing from another member's Apple Contacts link, and a member without the browser extension gets nothing from another member's browser connection.

Lazy Instantiation also ran backwards. A category tag is per-member (on `pod:SecretPod`), yet tagging a pod `podcat:IdVerification` added a `pod:Browser` to every member's pod.

## The concept

A **connector** links one member's own copy of a pod to a capability on that member's own device. It is not a tool.

- **`pod:Connector`** (abstract) is `owl:disjointWith pod:Tool`. Its two concrete subclasses are `pod:Contacts` and `pod:Browser`. Neither has a property of its own.
- **`pod:connector`** sits on `pod:SecretPod` (0..N). It is per-member state and never sent when a pod is shared.
- **`pod:Tool`** keeps `pod:Form`, `pod:Calendar`, `pod:Canvas` and `pod:Map`, which are shared content on `pod:SharedPod` via `pod:tool`. Calendar and Map stay content tools. A sync with a member's own device calendar or maps app would be a future connector.

```
Tool  (abstract, shared via pod:tool on SharedPod)
├── Form       formTopic, formGraph, formShape
├── Calendar
├── Canvas
└── Map

Connector  (abstract, per-member via pod:connector on SecretPod)
├── Contacts
└── Browser
```

Consequences:

- **Each member connects what their own device offers.** An iPhone member uses the Apple Contacts connector, and an Android member uses an Android one whose module writes under its own `pod:tagNamespace`. Two members of one pod may hold different connectors, or none.
- **A connector holds no pod content.** What it brings in becomes ordinary pod content: a graph, or an attachment such as a credential. What it must remember for itself it writes as `pod:serviceTag` values, which are per-member too.
- **Templates use one property.** `pod:declaresTool` now ranges over the union of `pod:Tool` and `pod:Connector`, and Lazy Instantiation sorts each declaration by its class:
  - a declared tool goes on the shared pod and reaches every member;
  - a declared connector goes only on the copy of the member who added the tag, which fits the tag being theirs alone.
- **Block links.** A live connector is named by its own IRI, like a live tool, so its owner's note can link to it. That link resolves only in the owner's copy and fails closed elsewhere.

## Decisions

- **Naming: Tool + Connector.** `pod:Tool` keeps its name for the shared content tools, and the local links get a new name. The alternative was to make "tool" mean the local link and rename the content tools, which would have touched every Form mention.
- **No common superclass.** `pod:Tool` and `pod:Connector` are disjoint siblings, outside the `pod:Pod` hierarchy.
- **One declaration property**, sorted by class, rather than a separate `pod:declaresConnector`.

## What changed in the repo

- **`pod.ttl`** (`versionIRI` 10.6.0):
  - new Pod Connectors section with `pod:Connector` and `pod:connector`;
  - `pod:Contacts`/`pod:Browser` moved under `pod:Connector`;
  - `pod:Tool` narrowed to four kinds;
  - `pod:declaresTool` ranges over the union;
  - Lazy Instantiation wording updated throughout.
- **`shacl/pod-shacl.ttl`:**
  - new `:LiveConnectorShape`;
  - `:LiveToolShape` rejects a connector reached by `pod:tool`;
  - `:DeclaredToolShape` accepts either kind and allows `pod:formShape` only on a declared Form;
  - `:SecretPodShape` constrains `pod:connector`;
  - `:TemplatePodShape` no longer requires every declaration to be a `pod:Tool`.
- **DataBooks:**
  - new `tpod.connector` list of `{id, type}` entries, with ids `http://www.example.org/tpod/connectors/connector-NN`;
  - the four example connectors moved out of `tpod.tool`: Facenook and PRIVO (`browser`), Bob Johnson and Fred Flintstone (`contacts`).
- **`helpers/databook_graphs.py`:** separate `CONNECTOR_TYPES` and emits `pod:connector`.
- **`integrity.md`:**
  - PNG-3 and PNG-7 describe the new arrow and the second hierarchy;
  - TTL-5 checks a declared connector against `tpod.connector`;
  - YAML-2 and YAML-10 cover connector entries and ids.
- **Docs:**
  - README.md gains a Connectors section;
  - app-behavior.md's Tools section becomes Connectors, and Lazy Instantiation, Add Tool and the module definition are updated;
  - pod-databook.md, CLAUDE.md, core-files.md, example.md, `service.ttl` and `other/sources.ttl` wording follows.
  - The Apple Contacts note is now `apple-contacts-connector.md`.
- **Diagrams** (both hand-drawn, both redrawn):
  - `images/pod-ontology/pod.png` draws the `connector` arrow off `SecretPod` (to a `pod:Connector` box, 0..N), plus a documentation-only `toolData` placeholder (`TBD 0..1`) beside `metaNote`;
  - `images/pod-ontology/tool.png` draws the `Connector` hierarchy (`Contacts`, `Browser`) beside `Tool`.

## Verification

- `helpers/validate.py`: 33 pods, 85 graphs, 0 violations.
- A negative test confirms the new shapes reject each misuse:
  - a `pod:Browser` reached by `pod:tool`;
  - a `pod:Contacts` carrying `pod:formTopic`;
  - a `pod:Form` reached by `pod:connector`;
  - a declared `pod:Browser` carrying `pod:formShape`.
- TTL-5 flags a PRIVO pod with its connector removed.
- All TTL, YAML and FS integrity checks pass. PNG-3 and PNG-7 match the redrawn `pod.png` and `tool.png`.
