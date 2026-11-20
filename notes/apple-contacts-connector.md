# Apple Contacts Connector Notes

## Overview

Apple Contacts is reached through a **connector** (`pod:Contacts`), not a service and not a tool. It never joins a pod as a member, and it is not shared content either: it links one member's own copy of a pod to the address book on that member's own device. See app-behavior.md's Connectors section.

Tellipod can hold nearly everything an Apple Contacts card holds, and a great deal more: many graphs about one person, claims made by different people, and links to other people as real individuals rather than free-text names. Importing from Apple Contacts into the app is therefore mostly straightforward, but exporting from the app back to Apple Contacts means flattening, and that requires explicit design decisions. Round-tripping losslessly is achievable but requires an anchor strategy (see below).

There are two levels to address:

---

## Level 1: Contacts ↔ Graphs

Apple Contacts' core design assumption is **one card per person**, with everything known about the person flattened into it. vCard accommodates the different parts of a person's life — work, home, and so on — by allowing optional labels on repeatable fields — a person can have two email addresses, one labeled `work` and one labeled `home`. This is vCard's mechanism for saying which part of a person's life a value belongs to.

The app follows the same design assumption. When exporting a person to Apple Contacts, **all N of that person's graphs are merged into a single vCard**. Each field value carries the label from the graph it came from (e.g. a phone number from a work graph gets the `work` label). If two different work graphs both contribute a phone number, the vCard will have two `work` phone numbers — this is correct and consistent with how vCard works.

**Import (Apple Contacts → the app):** each contact record becomes a graph. Most standard vCard fields have direct counterparts in the persona ontology: names, phone numbers, email addresses, postal addresses, organization, job title, birthday, anniversary and photo. A few map less cleanly and need checking against `persona.ttl` before an implementation relies on them. Notes have no per-person field. Social profiles and URLs may be represented differently. Related names are free-text names in vCard, but in Tellipod they are links to other `p:Person` individuals, so on import each one must either be matched to a person the user already has or be kept as a plain name.

**Export (the app → Apple Contacts):** merge all graphs for the person into a single vCard. Map the part of life each value belongs to (work, personal, family, etc.) to the corresponding vCard label. Multiple values under the same label are permitted and expected.

### vCard label constraints

**Number of values:** the vCard spec (RFC 6350) imposes no maximum on repeatable properties — `TEL`, `EMAIL`, `ADR` etc. can appear as many times as needed. Apple Contacts also imposes no hard cap in its data model. A person with phone numbers across many graphs will export cleanly regardless of count.

**Label string length:** vCard's `TYPE` parameter supports predefined types (`work`, `home`, `cell`, etc.) and custom types, stored with an `X-` prefix in vCard 3.0 (e.g. `TYPE=X-Acme-Corp`) or as free strings in vCard 4.0. The vCard spec sets no maximum length for `TYPE` values. However, Apple Contacts has an undocumented practical limit on how much of a custom label it displays in the UI — long labels (e.g. `"Boston Hub Society"`, `"California DMV"`) may be truncated visually even though the full string is preserved in the underlying vCard data. Round-trip fidelity of the data is unaffected; this is purely a display concern.

This display truncation limit is not publicly documented by Apple and likely varies by OS version. It should be verified empirically once an early implementation exists.

---

## Level 2: Groups ↔ Hidden Service Tags

An Apple Contacts **group** is not one of the user's own category tags or user tags, not a topic, and not a member, so it does not map onto anything the user sees in the app at all. The module records it instead as a [hidden service tag](../README.md#tags) on the contact's own pod — `pod:serviceTag`, namespace `foundation.mee.applecontacts`, key `group`, value the group's name verbatim.

**Import (Apple Contacts → the app):** for each group a contact belongs to, write one tag. A contact in three groups gets three tags sharing one namespace and one key, differing only in value — which is exactly what a namespace/key pair is allowed to repeat for. Which category tag the contact's pod carries is decided independently, by the ordinary Auto File suggestion; no pod is created, tagged, or retagged on account of a group.

**Export (the app → Apple Contacts):** read back every tag in this module's namespace with key `group` and re-create the contact's group membership from the values.

There is no flattening to do in either direction. Because a group never corresponds to a category concept, no hierarchy has to be encoded on the way out or reconstructed on the way back in — the group name round-trips verbatim, and a group name that happens to contain a `/` is just a group name, since the tag's structure lives in its sibling properties rather than inside the value.

**Rename safety:** matching is by name, so a group renamed on the Apple side reads as a new group, leaving the old tag stale. A module that wants to survive renames stores the group's own identifier alongside the name under a second key — `groupID` — which is precisely what having a key rather than one opaque string buys.

These tags are per-member state. A pod's service tags sit on `pod:SecretPod`, the part of a pod that one member holds and no other member ever sees, alongside the pod space and the user's own tags. So they never travel when a pod is shared, and the module's own bookkeeping cannot leak into another member's copy, where a different connector, or none, could neither interpret nor clear it.

The connector is per-member for the same reason. `pod:connector` sits on `pod:SecretPod`, so the `pod:Contacts` connector, its sync action and the group tags it writes all stay in the copy of the member who added it, and none of them is sent when the pod is shared. Each member connects their own address book, or none: a member on an iPhone uses this Apple Contacts connector, a member on an Android phone uses an Android one whose module writes under its own namespace, and a member with no address book to sync adds nothing. Two members of the same pod may therefore hold the contact in different groups, in different address books, or not at all, with nothing to reconcile between them.

---

## Anchor Strategy (Key to Losslessness)

vCard supports custom extension fields (`X-` prefix). Storing app IRIs in these fields lets the app re-identify records on re-import without duplication or drift:

- `X-TPOD-PERSON-IRI` on a contact record — points to the `p:Person` individual IRI

Groups need no anchor field of their own: the hidden service tag already holds the group's name verbatim on the pod, and re-identification is by that value (see the rename-safety note above for when a `groupID` tag is worth writing alongside it).

These fields are ignored by Apple Contacts and other vCard consumers but survive export/import cycles, making true lossless round-tripping achievable.

---

## Summary

| Dimension | Import | Export | Lossless? |
|-----------|--------|--------|-----------|
| Contact fields | Direct field mapping | Merge all graphs into one vCard | Yes, with `X-TPOD-PERSON-IRI` anchor |
| Multiple graphs per person | Each → a separate graph in the contact's pod | Flatten to single vCard; multiple values per label are correct | Yes |
| Group membership | Each group → one hidden service tag on the pod | Tags in this module's namespace with key `group` → group membership | Yes — the group name round-trips verbatim |
| App-specific metadata | Stored in a graph | Store IRI in `X-TPOD-*` vCard field | Yes, with anchor fields |
