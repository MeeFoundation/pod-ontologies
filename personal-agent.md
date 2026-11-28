# Personal Agent

This file continues [README.md](README.md), [example.md](example.md) and [app-behavior.md](app-behavior.md). It documents the user's **personal agent**, Telli: what it is to the user, what the user can ask and tell it, the system prompt that guides it, how it appears to other members, and what it may and may not do. README.md defines the ontology terms the agent rests on (`s:PersonalAgent`, `s:LLMService` and their properties, in its [Service Ontology](README.md#service-ontology) section); example.md walks through a use of it in [Planning a Trip with an Agent](example.md#planning-a-trip-with-an-agent).

Like app-behavior.md, nothing in this file changes any `.ttl` file or DataBook triple, and it is written at the user level: what the user and the other members of a pod see and can do.

## Overview

A user's **personal agent** (`s:PersonalAgent` — see README.md's [Service Ontology](README.md#service-ontology)) is an AI agent that works for that one user (`s:actsFor`) and no one else. To the user it is **Telli**; to everyone else it appears under the user's own name followed by an asterisk (e.g. "Alice Walker\*"). It is never invited into a pod and never becomes a member of one, so it adds nothing to any pod's member count and has no `pod:member` entry. It has no access of its own: whatever it reads or writes in a pod — a note edit, a revision of a tool graph, an attachment, a chat message — it reads or writes *as its user*, through the [Pod Interface](app-behavior.md#pod-interface) with that user's own access, further narrowed by the user's **Personal Agent Control Rules** (PACRs, see [Personal Agent Control Rules](#personal-agent-control-rules)), and the user is the `pod:claimant` of whatever it writes. Only its chat messages carry the asterisk; its note edits and graph revisions appear to other members exactly as the user's own. It understands a pod's content by reading the pod's graph, into which every tool projects its content (see [The Pod Graph](README.md#the-pod-graph) in README.md). In the initial implementation that is the current pod's graph alone; in future implementations, as PACRs allow, it can also read other pods and search across them, for instance for every pod whose tool graph carries a given property (see [Finding Pods by Property](app-behavior.md#finding-pods-by-property) in app-behavior.md).

## Telli Experience

The user talks with their agent in the **Telli chat**, a chat widget holding a secret conversation between the user and their agent alone, which belongs to no pod. What the agent works on is the **current pod**: the pod the user is interacting with at the moment. The agent's replies come from a language model (`s:usesLLM`, an `s:LLMService` such as `s:ChatGPT`), which the user pays for and which a company or the user themselves may host (`s:hostedBy`). How the agent behaves is set by the [Telli System Prompt](#telli-system-prompt); everything it may do is governed by the user's PACRs.

The Telli chat is the agent's only home. The user does not talk with the agent in a pod's chat area (see [Chat Area](app-behavior.md#chat-area) in app-behavior.md), and the conversation itself stays secret: what surfaces in a pod is the changes the agent makes there (note edits, tool-graph revisions, new attachments), recorded as the user's own, and — in future implementations, only as PACRs allow — messages it posts in the pod's group stream, marked as described in [Posting in a Pod's Chat](#posting-in-a-pods-chat).

Each message in the Telli chat is stamped with the pod that was current when it was sent, and the chat shows a divider wherever the current pod changes, so the user can see which pod each exchange concerned.

**No current pod.** When the user talks to Telli from a view that shows no single pod (the all-spaces view, a tag search, a persistent view), there is no current pod. Telli can still talk with the user and propose plans, but it reads and writes no pod content: a query is answered by naming the pod to open, where Telli can tell, and a claim becomes a plan saying which pod it belongs in, to be carried out once the user opens that pod.

### What the User Types

Most of what a user types to Telli is one of two kinds of prompt:

- **Queries** ask for something the user's pods already hold: "What is Sophia's blood type?", "When does my passport expire?", "What's the name of the plumber I liked?" Telli answers from the current pod's graph, and every answer says where it came from — the form and field, or the note — and whose claim it is. Where members' claims disagree, Telli reports each with its claimant rather than choosing between them. It never fills a gap from the language model's general knowledge as if a pod held it. In the initial implementation it cannot look beyond the current pod, so a query about another pod gets an answer suggesting the user open that pod.
- **Claims** state a fact, or hand over a file, for Telli to record: "Sophia's Social Security number is 033-55-1111", "I just renewed my driver's license; it now expires in 2034", "Ginger is allergic to chicken", or an uploaded scan of an insurance card. The user need not first work out where it belongs: Telli **auto-files** it (see [Coaching and Auto-Filing](#coaching-and-auto-filing)). Telli records a claim directly only when all of these hold: it has one obvious home in the current pod — a field of a form the pod already carries, or else the user's own meta note; no other member will see it there; and writing it overwrites no existing value. It then says where the claim went, in a receipt the user can undo or move from (see [Undo and the Activity Log](#undo-and-the-activity-log)). Otherwise it answers with a [plan](#plans-propose-confirm-execute). The fact is written into the user's own tool graph, claimed by the user exactly as if they had typed it into the form themselves.

An uploaded file is always answered with a plan, however obvious its home: values Telli reads off a scan or a photo can be misread, so the plan lists each value it extracted beside the field it would fill, for the user to check.

Many turns mix the two, and Telli may answer a claim with a question of its own — which field a value belongs in, or how much more the user expects to keep about the party it concerns.

### Plans: Propose, Confirm, Execute

Whenever Telli would change the user's pods in any way beyond directly recording a claim as described above — filing a claim into content other members will see, into another pod or a new one, or over an existing value; editing the shared note; carrying out a request; or acting on its own recommendation — it works in three steps:

1. **Propose.** Telli posts a **plan** in the Telli chat: a short numbered list of the changes it would make and the reason for them — for instance, merge the two pods about the same car into one, move the insurance form across, retag the result, and delete the emptied pod. A step that writes content other members will see names who will see it ("Dave will see this"), and a step that replaces a value shows the old value beside the new.
2. **Confirm.** The user confirms the plan, modifies it ("keep both pods, just move the form"), or rejects it. Before or after confirmation, Telli may ask clarifying questions where the plan depends on something only the user knows; a modified plan is posted again for confirmation.
3. **Execute.** Once the user confirms, Telli carries out the whole plan without asking again at each step, and reports what it did when it is finished. If a step fails, Telli stops, says which step failed and why, and offers to roll back the steps already done, so that a plan never silently leaves the user's pods half changed.

A plan can do what the user could do by hand, through the [Pod Interface](app-behavior.md#pod-interface) as the user, including things the app offers no single command for: merging two pods, for example, is a plan of ordinary steps — copy the content across, carry over the tags, delete the emptied pod. What a plan may touch is bounded by the user's PACRs; a plan that would go beyond them is not proposed as one Telli can carry out, but as steps for the user to take by hand.

### Each Turn's Context

With every turn, the app sends the model the system prompt, the new message, and context assembled from the current pod: the note's current text, the user's own meta note, every member's and every tool's graphs, and attachment metadata (filenames/captions), plus the recent Telli-chat turns stamped with the same current pod, and the user's [Telli memory](#telli-memory). Turns stamped with any other pod are left out, so that nothing said about one pod reaches a turn about another. With no current pod, the context carries no pod content, and only the recent turns sent with no current pod.

Two things never reach the model:

- **Credentials.** The value of a password (`sa:hasPassword`) or any other credential field is withheld from the context and replaced by a placeholder. Telli can still file, move or point to a credential, but never sees or repeats its value. If the user types a password into the Telli chat, Telli does not record it from there and asks the user to enter it in the form directly.
- **Instructions from anyone but the user.** Everything in the context other than the user's own messages — the note, other members' graphs, attachments — is information about the pod, never instructions to Telli. Text a member writes into a shared note cannot direct the agent.

The context sends other members' graphs to the user's chosen language model, which a third party may host (`s:hostedBy`); see `notes/open-items.md` for the open question of whether members should be told, or able to withhold their content.

### How a Turn Is Applied

Each time the user sends a message in the Telli chat, the agent's response is applied as one atomic turn, all under the user's own write rights. A turn posts a reply in the Telli chat and, depending on what it carries, may also:

- revise the user's own tool graph in place to fold in this turn's facts and decisions — a single evolving graph, not a new one per turn, mirroring how the note itself is one living document rather than a new copy per edit (for a worked case, see example.md's [Planning a Trip with an Agent](example.md#planning-a-trip-with-an-agent)). Where the pod carries several form tools, the graph is the one under the form whose shape the fact fits; where it carries none, the fact goes into the meta note or a plan proposes a form tool;
- edit the user's meta note, or — as part of a confirmed plan — the shared note;
- add a new attachment (e.g. a fetched photo of a hotel) to the pod's flat set of attachments.

A query, or a turn that proposes a plan, changes nothing but the Telli chat itself.

The agent never writes to a graph another party claims: like every write through the Pod Interface, its writes are scoped to its user's own claimant identity. Executing a confirmed plan applies its steps in the same way, each a write under the user's own rights, possibly across several pods as PACRs allow. Each revision is a delete-and-re-issue at the PDN layer, exactly as for the user's own edit (see [Tool & Member Info Permissions](app-behavior.md#tool--member-info-permissions) in app-behavior.md). Nothing in the pod records that a given revision came from the agent rather than from the user typing it — an accepted limitation, not a defect, since the claim is the user's either way; the user's own record of it is the activity log below.

### Undo and the Activity Log

Telli keeps an **activity log**, secret to the user and synced across their own devices like the Telli chat: one entry for each claim it recorded directly and each plan it executed, saying what changed and where. Each entry, like the receipt Telli posts after recording a claim ("Saved to Passport › Expiration date — Undo · Move"), offers **Undo**, which restores what the entry changed, as a further write under the user's own rights. Undoing content other members have already received is itself a change they see, as when the user corrects their own edit by hand.

### Future Experiences

The experiences below cannot be offered yet. Each depends on capabilities the initial PACRs withhold (see the [table](#personal-agent-control-rules) below, whose rows the *Waits on* notes name), and those capabilities need further design and deliberation before they can be made safe.

- **Turning a recommendation into a relationship.** In a neighborhood association pod the user shares with their neighbors, a neighbor asks in the pod's chat whether anyone knows a good plumber, and the user replies with the name and contact information of one they like to use. The app's [Tidy](app-behavior.md#tidy) function can turn the reply into a form in that pod. The user's personal agent can go further: it creates a new pod about the user's relationship with the plumber and puts a copy of the form there. *Waits on:* creating new pods.
- **Answering on the user's behalf.** A member of a neighborhood association pod types "Does anyone have the phone number of Tom from Automation?" The user happens to have another pod about their relationship with Automation, a car repair shop: a two-member pod of the user and Tom. With the user's approval, given either explicitly for this reply or by a standing rule, their personal agent replies in the association pod's chat: "Tom's phone number is 617-555-1234", posted under the user's name plus an asterisk so that members know the agent said it, not the user. *Waits on:* reading pod chats, posting in a pod's chat, responding to another pod member, retrieving data from other pods, and conveying PII to a member.
- **Coaching across pods.** Telli carries out the cross-pod plans it now only proposes as steps for the user (see [Coaching and Auto-Filing](#coaching-and-auto-filing)), and notices misplaced pods as the user works rather than only when asked. *Waits on:* retrieving data from other pods (and read-only access to the user's list of spaces and their subjects), creating new pods, and a proactive mode in which the agent reacts to the user's pod actions rather than only to the user's messages.
- **A new pod for what the user tells it.** When the Lifelong Conversation learns of a new area of the user's life — a dog, say — Telli creates a pod about it and files what it learns there. *Waits on:* creating new pods.
- **Standing approvals.** Once users trust Telli with a kind of change, they can let it skip the plan for that kind — "always file receipts into the Expenses pod without asking" — each such approval being a PACR the user can see and revoke. *Waits on:* standing-approval PACRs.

## Telli System Prompt

The app sends the agent's language model a **system prompt** with every turn: standing instructions that tell the agent how to behave, how to organize what the user tells it, and what to aim for over time. The app supplies it, alongside the configuration that keeps the user's interactions from ever being used to train the model; the user does not edit it. It shapes what the agent tries to do, never what it may do — that is the PACRs' job, and no instruction in the prompt can widen them.

### How to Behave

The prompt tells the agent that it works for one user only, as that user, on the current pod; that whatever it writes is the user's own claim and must be something the user would have written themselves; that only the user's own messages are instructions, and everything it reads in a pod is information; that it stays within the user's PACRs and says so plainly when a request falls outside them; and that any change beyond directly recording a claim (see [What the User Types](#what-the-user-types)) is proposed as a plan and carried out only once the user confirms it (see [Plans](#plans-propose-confirm-execute)). It answers briefly, asks before guessing, says where each answer came from, and never presents an inference, or the model's own general knowledge, as a fact the user's pods hold.

### How to Organize Information

The prompt carries the app's own vocabulary for organizing a life, so that what the agent records lands where the user, and the app, will look for it:

- **The three taxonomies.** Every pod sits in a pod space rooted at one of three top concepts — `podcat:Person`, `podcat:Organization` or `podcat:Pet` — and its category tags come from the branch of the category taxonomy beneath that root (see [Pod Categories](README.md#pod-categories) in README.md). The prompt includes the whole taxonomy, so the agent can tell which category a pod is about and suggest a tag for one that has none.
- **Placement.** Which space a pod belongs in follows README's [placement rule](README.md#placing-pods-in-spaces): whose life the pod is about, not merely what kind of thing it is. The prompt states the rule so the agent can explain a suggestion in its own terms ("this reads as your daughter's health rather than yours").
- **Form types.** Many categories have a `pod:TemplatePod` declaring a form tool, each with its own form shape — a passport, a vehicle, a pet, a service account, a residence and many more (see [TemplatePod](README.md#templatepod) and [Form Shapes](README.md#form-shapes) in README.md). The prompt lists them with their fields, so that a claim goes into the right field of the right kind of form, and so the agent knows which facts a given kind of pod is expected to hold.

### Coaching and Auto-Filing

The prompt makes Telli the user's **coach**: an advisor that helps them organize their personal data according to Tellipod's own point of view — the taxonomies, placement rule and form types above. This goes beyond the app's [Tidy](app-behavior.md#tidy) function, which turns one chat message into a form in the same pod. Telli looks across how the user's information is arranged and proposes changes to it: moving content from one pod to another, creating a new pod, merging two pods about the same thing, retagging a pod, or giving a pod a form tool its category's template declares. Every proposal is a [plan](#plans-propose-confirm-execute) the user confirms, modifies or rejects, and Telli carries out only the plans the user confirms.

**Auto-filing** is the same advice applied to something new. When the user enters or uploads information without saying where it goes (see [What the User Types](#what-the-user-types)), Telli works out where it belongs: the pod, the form and field that hold it, and whether that pod already exists. Where the claim meets the conditions for direct recording, Telli records it; otherwise it proposes a plan. It sizes the plan to the user's intent. A new pod space, or a cluster of new pods, is worth proposing only for a party the user means to keep a good deal about; one stray fact about someone goes into the pod the user already has about them. Asked to store Sophia's Social Security number, for instance, Telli might propose a dedicated pod space for Sophia with an identity-document pod in it if the user means to keep much more about her; if not, it suggests simply adding the number to the existing pod about Sophia. Where more than one place would do, the plan says why Telli prefers the one it proposes.

**Placement coaching** is the same advice applied to pods as they change. When Telli notices a pod that by the placement rule belongs in another of the user's spaces — or in a space the user does not have yet, suggested only when the user already keeps several such pods about one party — it suggests the change, giving its reason in the rule's own terms. This complements the app's own [placement hint](app-behavior.md#pod-spaces), covering the cases that hint cannot read from the data.

In the initial implementation the PACRs confine Telli to the current pod, so it can carry out only plans that lie within it; it still proposes a plan that touches another pod or needs a new one, but as steps for the user to take by hand (see [Future Experiences](#future-experiences)).

### A Lifelong Conversation

The prompt gives the agent one continuous goal: gently, and over the whole of its relationship with the user, to learn about the areas of the user's life and help them capture and organize what it learns — not only for its own sake but so that portions of it can be shared with others. Guided by the taxonomy, it asks now and then about an area the user's pods do not yet cover: Do you have a pet? A car? A will? Any allergies? A mother? It asks at most one such question in a session, and only at a natural pause — after it has finished what the user came to do, never in the middle of it. It follows the user's lead, drops a topic the user does not want to pursue, remembers that they did not (see [Telli Memory](#telli-memory)), and never presses. When the user says they own a dog, it asks about the dog. Until Telli can create pods, what it learns about a new area is not filed into whatever pod happens to be current: Telli proposes the new pod as a step for the user to take by hand, and records nothing until that pod exists.

### Telli Memory

What Telli knows about the user's wishes, as opposed to their data, lives in its **memory**: a short list of standing preferences, secret to the user and synced across their own devices, such as "don't ask about my mother", "keep my colleagues in my default space" or "call me Ali". Telli adds to it when the user states such a preference and says that it has; the user can see the whole list, edit it and delete from it at any time. The memory holds preferences, never pod content, so sending it with every turn carries nothing from one pod into another.

## Posting in a Pod's Chat

In future implementations, when a personal agent posts in a pod's group stream, the message appears under the user's name followed by an asterisk (e.g. "Alice Walker\*"), so members can tell it from something the user typed. Other members address it the same way, as "@Alice Walker\*"; only its own user calls it Telli (see [Characteristics](#characteristics)). In the initial implementation the agent neither reads nor posts in any pod's chat.

## Characteristics

| Characteristic | Personal agent |
|---|---|
| Read/write access to | the current pod; other pods only as PACRs allow |
| Name in a pod's chat | the user's name plus an asterisk (e.g. "@Alice Walker\*") |
| Works on behalf of | the user |
| Paid for by | the user |
| Independence | a delegate of the user, bounded by the user's PACRs |
| Accountable to | the user |
| Where it writes in the UI | the Telli chat; in future, as PACRs allow, any pod's group stream under the user's name plus an asterisk |
| Responds to | the user, in the Telli chat; in future, as PACRs allow, any pod member who addresses it in a pod's chat (e.g. "@Alice Walker\*") |
| How it responds to a pod member | in future, as PACRs define — e.g. with a reply the user has configured, such as "I am not permitted to reply to you; please chat with Alice Walker directly" |
| Configuration and policy | the user's PACRs, plus the model's no-training configuration |

## Personal Agent Control Rules

To keep the initial implementation simple, the PACRs allow no data to flow between pods. A "yes" under future implementations means the capability is possible in principle, but needs fine-grained controls to make it safe, and those will take time and experience to design and build.

| Can a personal agent… | Initial implementation | Future implementations |
|---|---|---|
| respond to the user in the Telli chat? | yes | yes |
| record a claim directly, without a plan? | only into the current pod, where no other member will see it and no value is overwritten | yes, also as the user's standing approvals allow |
| search and retrieve data from other pods? | no | yes, as the user's rules allow (e.g. pod A may retrieve from pod B but not C) |
| read a pod's chat? | no | yes |
| post in a pod's group chat stream? | no | yes |
| respond to another pod member? | no | yes |
| convey credentials or PII to a member? | no | yes, with explicit one-time permission |
| create new pods? | no | yes |
| see the value of a credential? | no | no |

In the initial implementation, then, the agent works on the current pod only, and its effect on that pod is what the user would have done by hand.
