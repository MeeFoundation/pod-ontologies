# Personal Agent

This file continues [README.md](README.md), [example.md](example.md) and [app-behavior.md](app-behavior.md). It documents the user's **personal agent**, Telli: what it is to the user, what the user can ask and tell it, the system prompt that guides it, how it appears to other members, and what it may and may not do. README.md defines the ontology terms the agent rests on (`s:PersonalAgent`, `s:LLMService` and their properties, in its [Service Ontology](README.md#service-ontology) section); example.md walks through a use of it in [Planning a Trip with an Agent](example.md#planning-a-trip-with-an-agent).

Like app-behavior.md, nothing in this file changes any `.ttl` file or DataBook triple, and it is written at the user level: what the user and the other members of a pod see and can do.

## Overview

A user's **personal agent** (`s:PersonalAgent` — see README.md's [Service Ontology](README.md#service-ontology)) is an AI agent that works for that one user (`s:actsFor`) and no one else. To the user it is **Telli**; to everyone else it appears under the user's own name followed by an asterisk (e.g. "Alice Walker\*"). It is never invited into a pod and never becomes a member of one, so it adds nothing to any pod's member count and has no `pod:member` entry. Whatever it writes into a pod — a note edit, a revision of a tool graph, an attachment, a chat message — it writes *as its user*, through the [Pod Interface](app-behavior.md#pod-interface) with that user's own access, and the user is that content's `pod:claimant`. The asterisk on its chat messages is how other members tell them from the user's own. It understands a pod's content by reading the pod's graph, into which every tool projects its content (see [The Pod Graph](README.md#the-pod-graph) in README.md), and so can read across pods wherever its PACRs allow.


## Telli Experience

The user talks with their agent in the **Telli chat**, a chat widget holding a secret conversation between the user and their agent alone, which belongs to no pod. What the agent works on is the **current pod**: the pod the user is interacting with at the moment. The agent's replies come from a language model (`s:usesLLM`, an `s:LLMService` such as `s:ChatGPT`), which the user pays for and which a company or the user themselves may host (`s:hostedBy`). How the agent behaves is set by the [Telli System Prompt](#telli-system-prompt); everything it may do is governed by the user's **Personal Agent Control Rules** (PACRs, see [Personal Agent Control Rules](#personal-agent-control-rules) below).

The Telli chat is the agent's only home. The user does not talk with the agent in a pod's chat area (see [Chat Area](app-behavior.md#chat-area) in app-behavior.md), and the conversation itself stays secret: what surfaces in a pod is the changes the agent makes there (note edits, tool-graph revisions, new attachments), recorded as the user's own, and — only as PACRs allow — messages it posts in the pod's group stream, which are marked as described in [Posting in a Pod's Chat](#posting-in-a-pods-chat).

### What the User Types

Most of what a user types to Telli is one of two kinds of prompt:

- **Queries** ask for something the user's pods already hold: "What is Sophia's blood type?", "When does my passport expire?", "What's the name of the plumber I liked?" Telli answers from the current pod's graph, into which every tool projects its content (see [The Pod Graph](README.md#the-pod-graph) in README.md). In the initial implementation it cannot look beyond the current pod, so a query about another pod gets an answer suggesting the user open that pod.
- **Claims** state a fact, or hand over a file, for Telli to record: "Sophia's Social Security number is 033-55-1111", "I just renewed my driver's license; it now expires in 2034", "Ginger is allergic to chicken", or an uploaded scan of an insurance card. The user need not first work out where it belongs: Telli **auto-files** it (see [Coaching and Auto-Filing](#coaching-and-auto-filing)). When the claim has one obvious home in the current pod — a field of a form it already carries, or else its note — and writing it overwrites no existing value, Telli simply records it and says where it went; otherwise it answers with a [plan](#plans-propose-confirm-execute) saying where it would go — which pod, in which form and field, or a new pod if none fits. The fact is written into the user's own tool graph, claimed by the user exactly as if they had typed it into the form themselves; a claim that fits no form the chosen pod carries goes into its note.

Many turns mix the two, and Telli may answer a claim with a question of its own — which field a value belongs in, or how much more the user expects to keep about the party it concerns.

### Plans: Propose, Confirm, Execute

Whenever Telli would change the user's pods in any way beyond recording a claim in its one obvious place in the current pod — filing a claim that has several possible homes, belongs in another pod or a new one, or would overwrite an existing value; carrying out a request; or acting on its own recommendation — it works in three steps:

1. **Propose.** Telli posts a **plan** in the Telli chat: a short numbered list of the changes it would make and the reason for them — for instance, merge the two pods about the same car into one, move the insurance form across, retag the result, and delete the emptied pod.
2. **Confirm.** The user confirms the plan, modifies it ("keep both pods, just move the form"), or rejects it. Before or after confirmation, Telli may ask clarifying questions where the plan depends on something only the user knows; a modified plan is posted again for confirmation.
3. **Execute.** Once the user confirms, Telli carries out the whole plan without asking again at each step, and reports what it did when it is finished, or where it stopped and why if a step fails.

A plan can do what the user could do by hand, through the [Pod Interface](app-behavior.md#pod-interface) as the user, including things the app offers no single command for: merging two pods, for example, is a plan of ordinary steps — copy the content across, carry over the tags, delete the emptied pod. What a plan may touch is bounded by the user's PACRs (see [Personal Agent Control Rules](#personal-agent-control-rules)); a plan that would go beyond them is not proposed as one Telli can carry out, but as steps for the user to take by hand.

### How a Turn Is Applied

Each time the user sends a message in the Telli chat, the agent's response is applied as one atomic turn, all under the user's own write rights:

- a reply posted in the Telli chat;
- the user's own tool graph revised in place to fold in this turn's facts and decisions — a single evolving graph, not a new one per turn, mirroring how the note itself is one living document rather than a new copy per edit (for a worked case, see example.md's [Planning a Trip with an Agent](example.md#planning-a-trip-with-an-agent));
- optionally, a direct edit to the shared note, and/or a new attachment (e.g. a fetched photo of a hotel) added to the pod's flat set of attachments.

The agent never writes to a graph another party claims: like every write through the Pod Interface, its writes are scoped to its user's own claimant identity. Executing a confirmed plan applies its steps in the same way, each a write under the user's own rights, possibly across several pods as PACRs allow. Each revision is a delete-and-re-issue at the PDN layer, exactly as for the user's own edit (see [Tool & Member Info Permissions](app-behavior.md#tool--member-info-permissions) in app-behavior.md). Nothing records that a given revision came from the agent rather than from the user typing it — an accepted limitation, not a defect, since the claim is the user's either way.

### Future Experiences

The two experiences below cannot be offered yet. Each depends on PACR capabilities that the initial implementation withholds, and those capabilities need further design and deliberation before they can be made safe (see [Personal Agent Control Rules](#personal-agent-control-rules)).

- **Turning a recommendation into a relationship.** In a neighborhood association pod the user shares with their neighbors, a neighbor asks in the pod's chat whether anyone knows a good plumber, and the user replies with the name and contact information of one they like to use. The app's [Tidy](app-behavior.md#tidy) function can turn the reply into a form in that pod. The user's personal agent can go further: it creates a new pod about the user's relationship with the plumber and puts a copy of the form there. *Waits on:* creating new pods.
- **Answering on the user's behalf.** A member of a neighborhood association pod types "Does anyone have the phone number of Tom from Automation?" The user happens to have another pod about their relationship with Automation, a car repair shop: a two-member pod of the user and Tom. With the user's approval, given either explicitly for this reply or by a standing rule, their personal agent replies in the association pod's chat: "Tom's phone number is 617-555-1234", posted under the user's name plus an asterisk so that members know the agent said it, not the user. *Waits on:* responding to another pod member, retrieving data from another pod, and conveying PII to a member.

## Telli System Prompt

The app sends the agent's language model a **system prompt** with every turn: standing instructions that tell the agent how to behave, how to organize what the user tells it, and what to aim for over time. The app supplies it, alongside the configuration that keeps the user's interactions from ever being used to train the model; the user does not edit it. It shapes what the agent tries to do, never what it may do — that is the PACRs' job, and no instruction in the prompt can widen them.

### How to Behave

The prompt tells the agent that it works for one user only, as that user, on the current pod; that whatever it writes is the user's own claim and must be something the user would have written themselves; that it stays within the user's PACRs and says so plainly when a request falls outside them; and that any change beyond recording what the user has just told it in the current pod is proposed as a plan and carried out only once the user confirms it (see [Plans](#plans-propose-confirm-execute)). It answers briefly, asks before guessing, and never presents an inference as a fact the user stated.

### How to Organize Information

The prompt carries the app's own vocabulary for organizing a life, so that what the agent records lands where the user, and the app, will look for it:

- **The three taxonomies.** Every pod sits in a pod space rooted at one of three top concepts — `podcat:Person`, `podcat:Organization` or `podcat:Pet` — and its category tags come from the branch of the category taxonomy beneath that root (see [Pod Categories](README.md#pod-categories) in README.md). The prompt includes the whole taxonomy, so the agent can tell which category a pod is about and suggest a tag for one that has none.
- **Placement.** Which space a pod belongs in follows README's [placement rule](README.md#placing-pods-in-spaces): whose life the pod is about, not merely what kind of thing it is. The prompt states the rule so the agent can explain a suggestion in its own terms ("this reads as your daughter's health rather than yours").
- **Form types.** Many categories have a `pod:TemplatePod` declaring a form tool, each with its own form shape — a passport, a vehicle, a pet, a service account, a residence and many more (see [TemplatePod](README.md#templatepod) and [Form Shapes](README.md#form-shapes) in README.md). The prompt lists them with their fields, so that a claim goes into the right field of the right kind of form, and so the agent knows which facts a given kind of pod is expected to hold.

### Coaching and Auto-Filing

The prompt makes Telli the user's **coach**: an advisor that helps them organize their personal data according to Tellipod's own point of view — the taxonomies, placement rule and form types above. This goes beyond the app's [Tidy](app-behavior.md#tidy) function, which turns one chat message into a form in the same pod. Telli looks across how the user's information is arranged and proposes changes to it: moving content from one pod to another, creating a new pod, merging two pods about the same thing, retagging a pod, or giving a pod a form tool its category's template declares. Every proposal is a [plan](#plans-propose-confirm-execute) the user confirms, modifies or rejects, and Telli carries out only the plans the user confirms.

**Auto-filing** is the same advice applied to something new. When the user enters or uploads information without saying where it goes (see [What the User Types](#what-the-user-types)), Telli works out where it belongs: the pod, the form and field that hold it, and whether that pod already exists. Where the answer is one obvious place in the current pod, Telli records it there directly; otherwise it proposes a plan. It sizes the plan to the user's intent. A new pod space, or a cluster of new pods, is worth proposing only for a party the user means to keep a good deal about; one stray fact about someone goes into the pod the user already has about them. Asked to store Sophia's Social Security number, for instance, Telli might propose a dedicated pod space for Sophia with an identity-document pod in it if the user means to keep much more about her; if not, it suggests simply adding the number to the existing pod about Sophia. Where more than one place would do, the plan says why Telli prefers the one it proposes.

**Placement coaching** is the same advice applied to pods as they change. As the user creates, tags and moves pods, Telli notices a pod that by the placement rule belongs in another of the user's spaces — or in a space the user does not have yet, suggested only when the user already keeps several such pods about one party — and suggests the change, giving its reason in the rule's own terms. This complements the app's own [placement hint](app-behavior.md#pod-spaces), covering the cases that hint cannot read from the data.

In the initial implementation the PACRs confine Telli to the current pod, so it can carry out only plans that lie within it; it still proposes a plan that touches another pod or needs a new one, but as steps for the user to take by hand. *Waits on:* read-only access to the user's list of spaces and their subjects, and to the other pods a plan names (retrieving data from other pods); a proactive mode in which the agent reacts to the user's pod actions rather than only to the user's messages; writing to other pods, for Telli to carry out a plan that spans several; and creating new pods, for one that needs a new pod.

### A Lifelong Conversation

The prompt gives the agent one continuous goal: gently, and over the whole of its relationship with the user, to learn about the areas of the user's life and help them capture and organize what it learns — not only for its own sake but so that portions of it can be shared with others. Guided by the taxonomy, it asks now and then about an area the user's pods do not yet cover: Do you have a pet? A car? A will? Any allergies? A mother? It asks one thing at a time, follows the user's lead, drops a topic the user does not want to pursue, and never presses. When the user says they own a dog, it asks about the dog, and in some future release puts everything it learns in a new pod about it. *Waits on:* creating new pods; until then, what the agent learns goes into the current pod.

### Each Turn's Context

With every turn, the app sends the model the system prompt, the new message, and context assembled from the current pod: the note's current text, every member's and every tool's graphs, and attachment metadata (filenames/captions), plus recent turns of the Telli chat. The response is applied as described in [How a Turn Is Applied](#how-a-turn-is-applied).

## Posting in a Pod's Chat

When a personal agent posts in a pod's group stream, the message appears under the user's name followed by an asterisk (e.g. "Alice Walker\*"), so members can tell it from something the user typed. Other members address it the same way, as "@Alice Walker\*"; only its own user calls it @Telli (see [Characteristics](#characteristics)).

## Access

A personal agent is not a member and has no access of its own: it reaches a pod through the [Pod Interface](app-behavior.md#pod-interface) as its user, with that user's access, further narrowed by the user's PACRs. Within those bounds it can do what its user can, such as searching for every pod whose tool graph carries a given property (see [Finding Pods by Property](app-behavior.md#finding-pods-by-property) in app-behavior.md).

## Characteristics

| Characteristic | Personal agent |
|---|---|
| Read/write access to | the current pod; other pods only as PACRs allow |
| Name in a pod's chat | the user's name plus an asterisk (e.g. "@Alice Walker\*") |
| Works on behalf of | the user |
| Paid for by | the user |
| Independence | a delegate of the user, bounded by the user's PACRs |
| Accountable to | the user |
| Where it writes in the UI | the Telli chat; and, as PACRs allow, any pod's group stream under the user's name plus an asterisk |
| Responds to | the user, in the Telli chat; and, as PACRs allow, any pod member who addresses it in a pod's chat (e.g. "@Alice Walker\*") |
| How it responds to a pod member | as PACRs define — e.g. with a reply the user has configured, such as "I am not permitted to reply to you; please chat with Alice Walker directly" |
| Configuration and policy | the user's PACRs, plus the model's no-training configuration |

## Personal Agent Control Rules

To keep the initial implementation simple, the PACRs allow no data to flow between pods. A "yes" under future implementations means the capability is possible in principle, but needs fine-grained controls to make it safe, and those will take time and experience to design and build.

| Can a personal agent… | Initial implementation | Future implementations |
|---|---|---|
| respond to the user in the Telli chat? | yes | yes |
| search and retrieve data from other pods while doing so? | no | yes, as the user's rules allow (e.g. pod A may retrieve from pod B but not C) |
| respond to the user in a pod's group chat stream? | no | yes |
| respond to another pod member? | no — it gives only the user's configured refusal (e.g. "I am not permitted to reply to you; please chat with Alice Walker directly") | yes |
| convey credentials or PII to a member? | no | yes, with explicit one-time permission |
| create new pods? | no | yes |

In the initial implementation, then, the agent works on the current pod only, and its effect on that pod is what the user would have done by hand.
