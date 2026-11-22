---
description: Move each statement to the doc it belongs in — universal model/design text out of example.md and app-behavior.md into README.md, and example text out of README.md into example.md or app-behavior.md
argument-hint: "(no arguments — always reviews README.md, example.md and app-behavior.md)"
---

Review `README.md`, `example.md` and `app-behavior.md` and move every statement that sits in the wrong one of them. Read all three in full — a keyword grep finds only the obvious cases. For a long file, read it in chunks, but read all of it.

## What belongs where

| Doc | Holds | Test |
|---|---|---|
| `README.md` | **Theory**: the ontologies and their core data structures — classes, properties, cardinalities, ranges, the design and the reasoning behind it, in the general case. | True of *every* pod / graph / user, and still true if the Alice Walker example were deleted. |
| `example.md` | **The worked example**: Alice Walker's pods, spaces, graphs, and the specific people, organizations, documents and services in them. | Names or depends on a specific example individual, pod, space, organization or graph number. |
| `app-behavior.md` | **App behavior** built on top of the data: what a user can do and sees, lifecycle, sharing, permissions, naming, search, views — in the general case. | Describes what the *app* does, not what the *data model* is. |

`pod-databook.md` (the `.databook.md` format, all scaffolding) and `storage.md` (where pod content lives) are the canonical homes for their own subjects; this skill does not edit them, but uses them as move targets' existing homes (see step 3 below).

## The two sweeps

### 1. `example.md` and `app-behavior.md` → `README.md`

Find every sentence or clause in `example.md` or `app-behavior.md` that states a **universal fact about the ontologies, core data structures or design** — a rule that would hold for any pod, not an account of the example or of app behavior. Move it to the `README.md` section that documents that term or mechanism.

- Example (`example.md`, Pod Spaces): *"In the repo, a pod in any space but the default carries a `tpod.space` mapping naming the space's id, name, root and subject (see [The `tpod` Block](pod-databook.md#the-tpod-block))."* — a universal statement about every non-default-space pod, not about Alice's pods. It does not belong in `example.md`.
- In `example.md`, the typical tells are "every pod …", "a pod in any …", "always", "never", "exactly one", a property's range or cardinality, "in the repo …", or a "why the model is this way" aside, inside a section otherwise telling Alice's story.
- In `app-behavior.md`, the tells are a property's domain, range or cardinality, a class hierarchy, or the reasoning for a modeling choice, stated as though the app enforced it. App rules stated in app terms ("a member can …", "the app shows …", "when a pod is shared …") stay.
- `example.md` may keep a statement about *what the example does*: "Alice's Ginger pods carry `tpod.space`" is example text; "a non-default-space pod carries `tpod.space`" is not.

### 2. `README.md` → `example.md` or `app-behavior.md`

Find every place `README.md` uses the example to carry an explanation: a specific example individual, pod, space, organization, or graph number (`:Alice_Walker`, the Citibank pod, `graph-14`, the Boston Hub Society, Ginger, Paula, …), or a walk-through of the scenario. Move it:

- to `example.md` when it is about the example's pods and graphs;
- to `app-behavior.md` when it is really app behavior (what a user does or sees), whether or not it names an example individual — de-exemplify it on the way if `app-behavior.md` states its rules in the general case there.

Then leave `README.md` with the general statement plus, where useful, a one-line pointer: "for a worked X, see [example.md](example.md#anchor)". That pointer is all of the example that belongs in `README.md`.

**Standing exception**: prose captioning a diagram embedded in `README.md` (e.g. the Representative Pods section, which names the boxes in `images/representative-pods.png`) stays, per CLAUDE.md's README Coverage section.

## Method

1. Read all three files in full and list every candidate: file, line number, the sentence, which sweep it falls under, and its proposed destination (file + section heading). Note borderline cases separately, each with a one-line reason to move or keep.
2. For each move, read the destination section first:
   - **Already stated there** (in the target, or in `pod-databook.md` / `storage.md` where `README.md` already links to it): just delete the source copy — don't duplicate. If the source sentence was the only path a reader had to that fact, leave a link to where it now lives.
   - **Not stated there**: add it in the destination's own voice — general and present-tense in `README.md` and `app-behavior.md`, about Alice's pods in `example.md` — merging into an existing paragraph rather than appending a stray sentence. A scaffolding-format fact (YAML keys like `tpod.space`) goes into `README.md` as a short statement linking to `pod-databook.md` for the detail, unless `README.md` already links there for it.
3. Repair the source: delete the clause, and if that leaves a gap, close it so the paragraph still reads naturally — in `example.md`, an example-specific sentence ("Alice's pods for Ginger carry …") may replace a universal one when the paragraph needs it.
4. Keep every link, anchor, backticked term, and the prefix conventions in CLAUDE.md's README Coverage section (`p:`, `pod:`, `podcat:`, `s:`, `v:`, `idoc:`, …) intact. Use US English. Describe only the current design — no history (see `/remove-history`). Use the terminology in CLAUDE.md's "Terminology going forward" (pods, tags, views, spaces — never folders, categories as containers, or nesting) and its "Secret vs. private" definitions.
5. When a moved sentence was the target of a cross-reference (an anchor in README.md ↔ app-behavior.md ↔ example.md ↔ storage.md ↔ pod-databook.md), check the referring sentence still points somewhere that says it, and update the link if the text moved sections.
6. Run integrity.md's FS checks that read these docs (cross-references, anchors, secret/private wording) and report any failures.
7. Report back, grouped by sweep: each move as `source file:line → destination file § section`, the before text, and whether it was moved, merged into existing text, or deleted as a duplicate. Then list the borderline cases you left alone and why. Do not commit unless asked.
