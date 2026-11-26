# Open Items

*Tellipod pod ontology — design questions raised but not yet decided. Remove an item once it is settled; the dated concept notes record the decisions.*

## Apple Contacts connector

Raised 2026-11-20 while reviewing [apple-contacts-connector.md](apple-contacts-connector.md). Items 1 and 2 affect `app-behavior.md`'s Apple Contacts section as well as the note; item 3 affects the note alone.

### 1. Where an exported value's vCard label comes from

On export, the note and app-behavior.md both say that each vCard field value "carries the label of the graph it came from" (`work`, `home`, …). But no graph carries such a label: a graph has a `pod:shape`, a `pod:claimant` and (for a member graph) a `pod:subject`, and nothing else. The label has to come from something the model actually holds. Candidates:

- a category tag of the pod the graph sits in (`podcat:Work` → `work`), keeping in mind that category tags are per-member and a pod may carry several or none;
- the pod's own name, written as a custom `X-` label;
- a mix: the predefined vCard type where a tag maps to one, the pod name otherwise.

The same section should also say how "all of a person's graphs" are found. Those are the `pod:MemberGraph`s whose `pod:subject` is the person, plus the `pod:FormGraph`s under any tool whose `pod:formTopic` is the person, across every pod the user holds. It should also say whether graphs claimed by someone other than the user are merged in or left out.

### 2. What kind of graph an imported contact becomes, and in which pod

On import, the note says only that "each contact record becomes a graph". Under the current model, an imported contact is the user's own claim about someone who is usually not a pod member, which suggests:

- a pod of its own for the contact, carrying the user's `:Self` member entry, and, in the user's own copy, a `pod:Contacts` connector and the group module tags;
- the contact's data as a `pod:FormGraph` (claimant `:Self`) under a form tool whose `pod:formTopic` is the contact, rather than as a `pod:MemberGraph`, since the contact is not a member.

Still to decide:

- whether the connector should create a shared form tool for that graph at all, or the graph should sit directly in the pod's member content;
- what happens when the contact later becomes a real member of the pod, as Bob and Fred are in the example.

### 3. The `X-TPOD-PERSON-IRI` anchor

The anchor stores a person's IRI, which means something only in the user's own copy of the app. `:Self` is never exposed, and other people's IRIs are minted locally. So:

- the note should say that re-identification works only when re-importing into that same copy;
- a card exported for the user themselves needs separate handling;
- `TPOD` in the field name should be confirmed or replaced.

## Connectors

Raised 2026-11-20 with the connector split ([connectors 20-nov-2026.md](<connectors 20-nov-2026.md>)).

### 4. How a member adds a connector by hand

A member gains a connector by Lazy Instantiation when a category tag they add declares one (`podcat:IdVerification` declares a `pod:Browser`), and the app adds a `pod:Browser` itself during the credential flows. Nothing settles how a member adds one deliberately, say to start syncing a pod with their address book. The Add Tool dialog offers tools only, and connectors are explicitly excluded from it. `app-behavior.md`'s Connectors section currently says a member adds one "from the pod's own menu", which was written without a decision. Options:

- a separate **Add Connector** action beside Add Tool;
- connectors offered in the Add Tool dialog, marked as the member's own;
- no per-pod action at all: a connector is switched on once per device (in settings, say), and the app attaches it to whichever pods it applies to.

Once decided, fix the wording in `app-behavior.md`.

### 5. What `pod:toolData` holds

`pod.png` draws a `toolData → TBD 0..1` arrow off `SecretPod`, documented for now as a documentation-only placeholder, like `pod:metaNote`. To decide:

- what it holds: a member's own data about the pod's shared tools (such as their own settings, or a draft not yet claimed), connector state, or both;
- its target type, and whether 0..1 means one node for all of the pod's tools or should be one per tool;
- whether it then becomes a real property in `pod.ttl`.

## Space placement

Raised 2026-11-25 when the space-placement rule was written into README.md's [Pod Spaces](../README.md#pod-spaces): a pod sits in the space of the party whose life its category tag describes.

### 1. Things belonging to two lives at once

A joint bank account, or a family trip taken with a child, passes the "⟨space subject⟩'s ⟨category⟩" test in two spaces. Proposed tiebreak: the default space whenever the user is themselves a party to it (the example's Kyoto Trip, taken with Dave, stays in Alice's default space). Not yet decided, and not yet stated in README.md.

### 2. Telli's access to the user's spaces

The placement-coach use case (app-behavior.md's [Use Cases](../app-behavior.md#use-cases)) needs the personal agent to read the user's list of spaces and their subjects. In the initial implementation the PACRs confine the agent to the current pod. Spaces are not pod content and belong to the user alone, so read-only access to them may be safe enough to grant from the start. Undecided: whether to grant it in the initial implementation, and whether the proactive mode (reacting to pod actions, not only to messages) needs a PACR of its own.
