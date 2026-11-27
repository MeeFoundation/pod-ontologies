# The Pod Graph

*Tellipod pod ontology: concept summary, 2026-11-26*

## The concept

Every pod tool (note, chat, form, calendar, canvas, map) **projects its content into the pod graph**. The pod graph is the single interface through which the app reads a pod's content into its UI.

- **The tool decides the representation.** A tool may keep a working format of its own. The note's, for example, is suited to links and to merging concurrent edits. How the tool represents its content as triples is its own decision, weighing an efficient data layout against the ontology suggested for it.
- **The agent reads it too.** All of a pod's content is in one graph, so the user's personal agent (Telli) can understand that pod by reading the graph. It can also read across pods, as far as its PACRs allow.
- **Reach is preserved.** Projected content keeps its own propagation rule:
  - a group-stream message reaches every member;
  - a direct message reaches only its two participants;
  - a direct message to @Telli and a member's meta note stay in that member's own copy.
- **Only `pod:Form`'s suggested vocabulary is settled.** For a form, the graphs *are* the format. The vocabulary for the note, the chat and the other tools is an open item (`notes/open-items.md`, The pod graph).

## Scaffolding

The example DataBooks carry no note or chat triples. The note's stand-in is the pod folder's `X.md`, and a chat has no scaffolding at all. These are gaps in the scaffolding only. A real Tellipod pod graph holds every tool's content.

## What was changed

`pod.ttl` (Pod Tools section, `pod:Tool`, `pod:Note`, `pod:Chat`, the Pod Content note paragraph), `shacl/pod-shacl.ttl` (comment only), `README.md` (new The Pod Graph subsection under Tools, the tool classes, `pod:tool`, `pod:metaNote`), `app-behavior.md` (Pod Contents, Note Area, Chat Area, Personal Agent), `storage.md`, `pod-databook.md` (scaffolding bullets, open questions), `CLAUDE.md`. No new terms and no constraint changes.
