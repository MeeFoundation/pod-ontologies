---
description: Find and remove historical information — how things used to work, or could work — from the docs, leaving only how they work now
argument-hint: "[file ...] (default: README.md example.md app-behavior.md)"
---

Sweep the documentation for **historical information** and remove it. The project convention is that every document describes only how things work **now**. Git carries the history; the docs never do.

**Files to review**: `$ARGUMENTS` if given, otherwise `README.md`, `example.md` and `app-behavior.md`. Read each file in full — a keyword grep finds only the explicit cases, and the implicit ones are the majority. For a long file, read it in chunks, but read all of it.

## What counts as history

Remove, or rewrite as a present-tense positive statement, any sentence or clause that describes a design other than the current one. Three kinds:

1. **Explicit history** — narrates a change or a past state of the design.
   - "Before spaces, the only way to tell them apart was to fold the patient into the pod's name or a user tag."
   - "formerly", "previously", "used to", "no longer", "originally", "renamed from", "replaced", "was once", "until recently", "is now" / "are now" (where *now* contrasts with a past), "as of version X", dates attached to design decisions.

2. **Implicit history** — contrastive phrasing that only makes sense against a design that once existed: it denies something no reader would otherwise have assumed.
   - "no pod sits inside another", "in place of browsing a hierarchy of pods" (written after pod nesting was removed).
   - Stating the current model positively is the fix: "A user's pods are a flat set", not "Pods no longer nest" or "Pods don't nest the way they used to".

3. **Alternatives that could work but don't** — a sentence whose only job is to say where something is *not*, or how it *isn't* done, when the doc could simply say where it is or how it is done.
   - app-behavior.md's Pod Storage: "**A pod is never persisted in the user's filesystem**" → say where it is: in the app's local database, encrypted at rest.
   - app-behavior.md's Pod Contents: "Nothing marks it in a filesystem, because it is not in one." → delete, or replace with where a pod is stored (a local database).

## What is *not* history — leave it alone

- **Design rationale for the current model.** A sentence explaining *why* the current design is right, by naming the problem it avoids, is theory and belongs in README.md (e.g. why `skos:broader` rather than `rdfs:subClassOf`, why `pod:formTopic` sits on the tool rather than on each graph, why there is no separate boolean beside `pod:declaresTool`). Keep it when the reasoning teaches something about the current model. Cut it only when the alternative is named merely to be denied, with no reasoning that would survive the cut.
- **Normative constraints stated as rules**: "never shared", "never removed", "exactly one", "owner included". These say how the system works now.
- **History inside the worked example's own story.** Alice moving from Boston to Paradise, a pod tagged `podcat:Home` while she lived there, a pod shared with Paula after its creation — that is the scenario's timeline, not the documentation's.
- **Future plans and current limitations** ("cannot be implemented yet", "some future release") describe the present state and stay.
- **Development scaffolding sections**, where "folder" and "filesystem" are the literal subject: app-behavior.md's Scaffolding section, storage.md's scaffolding-boundary section, integrity.md's scaffolding checks, and all of pod-databook.md. A statement that *this repo* carries pods on disk is current fact about the repo.
- **Terms in their ordinary present-tense sense**: "renamed" in "can be renamed, e.g. to 'Clients'" or "freely renamed by the user" is an app behavior, not a change history; "today" in a count of current templates is harmless (drop it if the sentence reads as well without it).

## Method

1. Read each file in full and list every candidate with its line number, the sentence, and which of the three kinds it is. Note borderline cases separately with a one-line reason for keeping or cutting.
2. Edit. Prefer deleting a clause over rewriting a paragraph; when a deletion leaves a gap, fill it with the present-tense positive fact (where it is, what it does), never with a softer denial. Keep every link, anchor, backticked term and the prefix conventions in CLAUDE.md's README Coverage section intact.
3. If a rewritten sentence was the target of a cross-reference from another doc (README.md ↔ app-behavior.md ↔ example.md ↔ storage.md), check that the referring sentence still makes sense.
4. Report back, file by file: each change as before → after (or "deleted"), then the borderline cases you left alone and why. Do not commit unless asked.
