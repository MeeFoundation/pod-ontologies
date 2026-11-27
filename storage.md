# Storage

Tellipod persists **no data in the user's filesystem**. Every pod and everything in it lives in a
protected, app-managed store, encrypted at rest.

This document is the canonical statement of where pod content lives and of what follows from it — in
particular, which parts of this repository are real Tellipod and which are development scaffolding. It is
linked from [README.md](README.md), [app-behavior.md](app-behavior.md),
[pod-databook.md](pod-databook.md) and [CLAUDE.md](CLAUDE.md), which describe the model itself and
point here rather than restating any of this.

## Where pod content lives

A pod's entire content is app-internal: its members, tools, graphs, tags, name and id,
together with its note, each member's own meta note, its attachments and its chat. None of it is
written to the filesystem, in any form, at any point. There is no folder representing a pod, no
file representing its note, and no directory holding its attachments.

The store holds each pod's **pod graph**, into which every tool projects its content, and from
which the app reads that content into its UI (see [The Pod Graph](README.md#the-pod-graph) in
README.md). A tool's own working format, where it keeps one, is held in the same store.

The store sits alongside the pod's membership store, the append-only event log whose first entry
is the pod's founding event (see [Pod Id](pod-databook.md#id) in pod-databook.md). A pod is held on the user's own device(s), or, for an organization's own `s:ServiceProvider`, on
Personal Data Network (PDN) nodes hosted by that organization. Apart from one exception a member
opts into, no pod is ever stored by any cloud provider, or any third party of any kind, including
The Mee Foundation: a member who invites a backup service into a pod as a member has that
service's provider keep a copy of that one pod (see
[Inviting Backup Services](app-behavior.md#inviting-backup-services) in app-behavior.md).

## Why

**Crash consistency.** Getting durability and consistency right on top of ordinary files is far
harder than it looks — the failure modes are numerous, poorly documented, and inconsistent across
filesystems and platforms. Dan Luu's [survey of file-consistency
bugs](https://danluu.com/file-consistency/) collects the evidence. A single store the app controls
end to end is the tractable version of the problem.

**Security, which is the product's whole point.** Tellipod exists so that two people can share information
directly, end-to-end encrypted, with no corporate intermediary in the middle. Data transmission is
built to that standard. Leaving the same content sitting as plaintext files in the user's
filesystem — where any other process, sync client, backup agent or indexer on the machine can read
it — undercuts exactly the guarantee the transport layer provides. The risk is not acceptable for
notes, and it is not acceptable for attachments either. Encryption at rest is therefore a property
of *all* Tellipod data, with no carve-out for the unstructured parts.

## What follows from it

- **What a pod is.** A pod is a unit the app manages, identified by its own stable id. Nothing
  marks it in a filesystem, because it is not in one. The reserved `_pod-attachments` folder that
  marks a pod in this repo is a scaffolding convention only (see below).
- **Per-member state.** What each member keeps for themselves is their tags — category tags, user tags, and the module tags their
  own modules write — and the pod space they place the pod in, all held in that member's own store
  and never shared content. This is what lets two members of a shared pod each classify it however
  they like without touching what the other sees; a sender's category tags and space name cross a
  share only as suggestions the recipient may adopt (see [Tags](README.md#tags) and
  [Pod Spaces](README.md#pod-spaces) in README.md). A pod space is no more a folder than a pod is:
  nothing on disk stands for one.
- **A pod's name.** The app's own record of the name is authoritative. A name need not be unique,
  since a pod is resolved by its stable id; a pod the user left unnamed is given `Untitled-N` by the
  app; and some pods share a name across members while others keep one per member (see
  [Naming, Renaming, and Sharing](app-behavior.md#naming-renaming-and-sharing) in app-behavior.md).
- **Attachments.** Every attachment is content every member receives.
- **The note.** Exactly one per pod. It supports links to other pods, resolved by target pod id,
  and to the pod's own tools, graphs and attachments. It is a rich-text document with Markdown-like
  formatting, kept in a working format of the app's own — one suited to those links and to merging
  concurrent edits by several members — and projected into the pod graph like every tool's content.
  A member can export it as a Markdown file.
- **The meta note.** One per member per pod, the member's own personal note about it, in the same
  format as the note, projected into the member's own copy of the pod graph. It is secret to that member: it stays in their own copy of the pod, syncs
  across their own devices, and never propagates on a share.
- **PKM tools.** Tellipod's store is not a PKM vault, and no Obsidian-style tool reads it directly.
  The note's wikilink-style links and its Markdown export are the bridge to such tools.

## What is real Tellipod, and what is scaffolding

The app does not exist yet. This repository develops the ontologies for it and documents the use
cases they have to serve, and it needs real content to do that against — so it carries a worked
example on disk, in the only form available to a repository. **That on-disk form is development
scaffolding in its entirety**: not merely the `.databook.md` files, but the folder layout around
them too.

| Ships as Tellipod | Development scaffolding |
|---|---|
| Every `*.ttl` ontology — `persona.ttl`, `pod.ttl`, `pod-categories.ttl`, `pod-category-templates.ttl`, `service.ttl`, `organization.ttl`, and every `other/`, `persona-ext/` and `pod-category-ext/` peer file (possibly expressed differently in the app) | Every `*.databook.md` file, and the whole format specified in [pod-databook.md](pod-databook.md) |
| Every `**/shacl/*.ttl` shapes file | The `example/pod-spaces/` directory, and every folder in it |
| The concepts the ontologies model — pods, members, owners, tools, graphs, categories, tags, notes, attachments, chat | Pods as folders, one per pod, grouped in one folder per pod space, no pod folder inside another; the `_pod-attachments` marker; folder notes named after their folder, with no file for an empty note; the filename convention |
| The app-level rules in [app-behavior.md](app-behavior.md) — lifecycle, sharing, permissions, naming, tagging | The `helpers/` scripts, and the [integrity.md](integrity.md) checks that read the files and folders on disk |

The scaffolding is genuinely useful and is not going away before the app arrives: it is how the
ontologies get exercised, validated and diagrammed against real content, and it is a diagnostic
independent of any implementation. But nothing in it is a commitment about how Tellipod stores anything.
Where a document in this repo describes a folder, a filename, or a file on disk, it is describing
this repository — see [Development Scaffolding](pod-databook.md#development-scaffolding) in
pod-databook.md for the detailed account, and
[Scaffolding: This Repo's Filesystem Tree](app-behavior.md#scaffolding-this-repos-filesystem-tree)
in app-behavior.md for the picture of it.
