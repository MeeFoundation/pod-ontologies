# Shared and Secret Pods

*Tellipod pod ontology — concept summary, 2026-11-20*

## The problem

Every pod a user holds mixes two kinds of state:

- **Shared content**, which every member of the pod holds alike: who created it, who owns it, its members' graphs, its tools, its attachments, its note and its chat.
- **Secret state**, which each member holds for themselves and which never reaches another member, owner included: the pod space they keep it in, their category tags, their user tags, the service tags their own modules write, and their secret meta note.

The ontology already said, property by property, which side each one fell on. A tag's comment said "per-member state, never shared pod content", and so did the space's. But every one of these properties had the same domain, `pod:InstancePod`, so the class structure carried none of the distinction. You had to read the comments to learn it, and nothing kept a new property from landing on the wrong side.

## The concept

The single instance class splits in two, and the line between shared and secret becomes the line between the two classes.

- **`pod:SharedPod`** (concrete; it replaces `pod:InstancePod`) is an actual pod as every one of its members holds it alike. It carries `pod:creator` 1..1, `pod:owner` 1..N, `pod:member` 1..N and `pod:tool` 0..N. It also inherits `pod:attachment`, `pod:note` and `pod:chat` from `pod:Pod`.
- **`pod:SecretPod`** (concrete, `rdfs:subClassOf pod:SharedPod`) is a pod as one member holds it: the shared pod plus that member's own secret part. It carries `pod:space` 1..1, `pod:categoryTag` 0..N, `pod:userTag` 0..N, `pod:serviceTag` 0..N and the documentation-only `pod:metaNote` 1..1.

So:

- **Every pod a user holds is typed `pod:SecretPod`**, and so also `pod:SharedPod` by subclassing. Each member's copy is one such individual.
- **A `pod:SharedPod` that is not also a `pod:SecretPod` is the shared part alone.** This is what a joining member receives before choosing a space or any tags of their own.
- **`pod:TemplatePod` is `owl:disjointWith pod:SharedPod`**, so a template is never a `pod:SecretPod` either.
- **Nothing on `pod:SecretPod` is ever sent as pod content.** There is one crossing point: when a pod is shared, the sender's category tags go with the invitation as suggestions only.
- **A secret tag can still change shared content.** Adding a category tag gives the pod, by Lazy Instantiation, each tool that tag's template declares. Tools live on `pod:SharedPod`, so a tool gained this way reaches every member, even though the tag that prompted it does not.

```
Pod  (abstract: attachment, note*, chat*)
├── TemplatePod  (abstract: category, memberShape, declaresTool)
└── SharedPod    (creator, owner, member, tool)
    └── SecretPod  (space, categoryTag, userTag, serviceTag, metaNote*)

* documentation-only: drawn in pod.png, never declared or stored as a triple
```

## The meta note

`pod:metaNote` is each member's own secret note about a pod. It has the same format as the note and is shown in the same Note area, but it is visible only to that member. Before this change the meta note existed in the app's behavior, but the ontology said that no property modeled it, not even a documentation-only one. It is now a documentation-only property, like `pod:note` and `pod:chat`, drawn off `SecretPod`. Being secret is exactly why it sits there rather than on `pod:Pod` next to the shared note.

## Placement decisions

The first sketch of the split put `tool` on the secret side and left `space` and `serviceTag` on the shared side. The final diagram corrects all three:

- **`tool` is shared.** Every member gets a pod's tools. A form tool holds one graph per claiming member, all about the tool's single `pod:formTopic`, so a tool secret to one member could not hold the other members' claims.
- **`space` is secret.** Each member keeps a shared pod in a space of their own. Nothing about the sender's space travels with an invitation.
- **`serviceTag` is secret.** It is the most secret of the three tags. It is never shown to the user, it is reachable only by the module that wrote it, within that module's own namespace, and it never leaves the copy of the app that wrote it.

## What changed in the repo

- **`pod.ttl`** (`versionIRI` 10.5.0):
  - The `pod:InstancePod` class becomes `pod:SharedPod`, and `pod:SecretPod` is added as its subclass.
  - Domains move: `creator`, `owner`, `member` and `tool` to `SharedPod`; `space`, `categoryTag`, `userTag` and `serviceTag` to `SecretPod`.
  - The disjointness axiom now pairs `TemplatePod` with `SharedPod`.
  - The meta note passage is rewritten around `pod:metaNote`.
- **`shacl/pod-shacl.ttl`**:
  - `:InstancePodShape` splits into `:SharedPodShape` (creator, owner, member, tool) and `:SecretPodShape` (space, the space-root SPARQL constraint, and the three tags).
  - `:PodShape`'s `sh:xone` test is now `TemplatePod` / `SharedPod`.
- **`helpers/databook_graphs.py`** types every synthesized pod as `pod:SharedPod` and `pod:SecretPod`, both asserted explicitly so that validation never depends on subclass inference.
- **`integrity.md`**:
  - PNG-3 (12a/12b/12c) covers the new boxes, the `SharedPod → SecretPod` subclass arrow and the `metaNote` documentation-only exception.
  - 37c, TTL-9's script and the shape names in YAML-9 and the validation section are updated to match.
- **Docs**:
  - In README.md, the InstancePod section becomes SharedPod and SecretPod sections, and `pod:metaNote` is listed under Documentation-only Properties.
  - CLAUDE.md, core-files.md, app-behavior.md and example.md are updated to match.
- **`images/pod-ontology/pod.png`** was redrawn by hand. It is the authority for the split.

## Verification

- No `InstancePod` remains anywhere outside `project_files/` and dated notes.
- `helpers/validate.py`: 33 pods, 85 graphs checked, 0 violations.
- A negative test, a bare pod typed `SharedPod` + `SecretPod` with an empty user tag, triggers both new shapes: missing creator, owner, member and space, and the empty-tag message.
- All TTL, YAML and FS integrity checks pass, as do the scripted PNG-9, PNG-10 and PNG-11. PNG-3 is visual: the redrawn `pod.png` matches `pod.ttl`'s domains, cardinalities and hierarchy.
