# Telli Actions

*Tellipod pod ontology: concept summary, 2026-11-28*

## The concept

Telli changes nothing by what it writes in the Telli chat. It acts only through a fixed set of **actions** the app offers it on each turn, each returning a result. Every pod-changing action is a write through the Pod Interface under the user's own claimant identity, so Telli gains no operation the user's own UI lacks. The set is defined in personal-agent.md's [Telli Actions](../personal-agent.md#telli-actions).

- **Direct actions** act without a plan: `record_value`, `edit_draft`, `edit_meta_note`, `read_attachment`, `remember`, `forget`, `undo`, `propose_plan`, `execute_plan` and `roll_back_plan`.
- **Plan steps** are what a plan is made of: set, add or remove a value; publish a draft; undo a change other members saw; edit the shared note or the meta note; keep an uploaded file as an attachment; add a form; add or remove a category tag; and a **user step** for anything Telli may not do itself. Creating pods and spaces, moving content or pods, deleting pods and posting in a pod's chat are later-release steps.

## Why it is built this way

- **The app enforces what the instructions ask.** The conditions for recording directly, the PACRs, own-entries-only writes and plan confirmation are all checked again by the app on each call. The instructions guide Telli; they are not the safeguard.
- **What the user sees is what runs.** A plan is structured data. The app draws the plan card from it and executes exactly its steps.
- **Confirmation is the user's act.** The plan card's Confirm, Change and Reject buttons, or a typed clear yes, which the app accepts only for Telli's latest plan and only if the pods it touches have not changed since it was posted.
- **The app keeps the activity log** and says who will see each change, so neither depends on the model getting it right.
- **The PACRs shape the list.** A withheld action is simply absent from the turn; a withheld change can appear in a plan only as a user step.
- **Drafts make iterative work possible.** Where other members can see the user's entry, Telli builds it up turn by turn in a draft only the user sees, and a single plan step publishes it.
- **Steps state what they expect.** A step that changes a value carries the value it expects; if the pod changed meanwhile, the step fails rather than overwriting someone else's edit.
- **Some acts are never Telli's.** Inviting or removing members, sharing a pod, changing owners, deleting a pod for everyone, and changing another member's entry stay the user's own in every release.
