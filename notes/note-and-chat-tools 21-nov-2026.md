# Note and Chat Tools

*Tellipod pod ontology — concept summary, 2026-11-21*

## The concept

A pod's note and its chat are **tools**, like a form, a calendar, a canvas or a map. Each brings its own data format into the pod and its own contribution to the app's UI: the note's is the Note area, the chat's the Chat area.

- **`pod:Note`** is the one **required** tool. Every pod carries exactly one, created with the pod and never removed. No template declares one, and the Add Tool action never offers one.
- **`pod:Chat`** is **optional**, like every other tool. A pod carries at most one, added by a member through Add Tool or gained from a category template's `pod:declaresTool`. It is the one tool not all of whose content reaches every member: a direct message reaches only its two participants.
- Neither carries a property. The note's and the chat's content is held in the app's own internal formats, and no triple records it.

```
Tool  (abstract, shared via pod:tool on SharedPod)
├── Note       required, exactly one
├── Chat       optional, at most one
├── Form       formTopic, formGraph, formShape
├── Calendar
├── Canvas
└── Map
```

`pod:tool` is therefore 1..N on every `pod:SharedPod`: the note, plus any optional tools. A pod with nothing but its note is the ordinary case, not a lesser kind of pod.

The pod's Attachments area, Tags area and Member Info are not tools: every pod has them, and none is a tool's contribution. The member's meta note (`pod:metaNote`, documentation only, on `pod:SecretPod`) is not a tool either, since it is never shared; it stays where it was, shown in the Note area beside the note.

## Scaffolding

The example DataBooks write no tool node for either. The note's stand-in is the Markdown file named after the pod's folder, and a chat has no scaffolding at all. So `shacl/pod-shacl.ttl`'s `:SharedPodShape` caps each at one (`sh:qualifiedMaxCount 1`) without requiring the note. `:LiveToolShape` accepts both as live tools, and `:DeclaredToolShape` accepts a declared `pod:Chat` but never a `pod:Note`.

## What changed

- **`pod.ttl`**: `pod:Note` and `pod:Chat` declared as subclasses of `pod:Tool`. The ontology comment, the Pod Tools section, `pod:Tool`, `pod:SharedPod`, `pod:tool` and the Pod Content section describe them. `pod:note` and `pod:chat` are no longer documentation-only properties off `pod:Pod`.
- **`shacl/pod-shacl.ttl`**: the two caps on `pod:tool`, and the tool-kind lists in `:LiveToolShape` and `:DeclaredToolShape`.
- **`README.md`**: the Introduction's Note, Chat and Form text, Documentation-only Properties (now only `pod:metaNote` and `pod:toolData`), SharedPod, Tools and its Properties, and Pod Ontology Files.
- **`app-behavior.md`**: Pod Contents (note bullet, new chat bullet), Adding a Tool, Note Area, Chat Area.
- **`pod-databook.md`**, **`integrity.md`** (PNG-1 icon note, PNG-3, PNG-7), **`other/sources.ttl`**, **`other-ontologies.md`**, **`example.md`**, **`CLAUDE.md`**.

## Diagrams

Both hand-drawn, both redrawn:

- `images/pod-ontology/pod.png` — no `note` or `chat` arrow off `Pod`, which carries `attachment` alone; `tool` off `SharedPod` is **1..N**.
- `images/pod-ontology/tool.png` — `Note` and `Chat` under `Tool`, neither with an arrow.

PNG-3 and PNG-7 match both.
