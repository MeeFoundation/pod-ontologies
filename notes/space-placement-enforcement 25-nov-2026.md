# Space Placement Enforcement

*Tellipod pod ontology — concept summary, updated 2026-11-25*

## The question

The [space-placement rule](space-placement%2025-nov-2026.md) says a pod sits in the space of the party whose life its category tag describes. Where is that rule enforced?

## The answer: half of it

The rule has two halves.

- **Which kind of life is enforced.** Every category tag of a pod must fall under its space's root. `shacl/pod-shacl.ttl`'s `:SecretPodShape` and integrity.md's TTL-9 check this, and the app keeps it true: moving a pod, or deleting its space, drops any tag that would break it. So an Organization-branch tag such as Employees can never sit in a Person-rooted space, and a Pet-branch tag such as Medical can never sit in the user's default space.
- **Whose life is not enforced, and cannot be.** Among spaces that share a root, nothing in the data says whose life a pod belongs to. A child's height tagged Health & Wellness is equally valid in the parent's default space and in the child's space. Reading "⟨space subject⟩'s ⟨category⟩: ⟨pod⟩" is a judgment about meaning, which only a person or a language model can make.

So the second half is a recommendation. Two mechanisms help the user follow it.

## 1. The app's placement hint (deterministic, no agent)

A pod is probably in the wrong space when both of these are true:

- one of its form topics is the subject of one of the user's **other** spaces; and
- none of its category tags names a party's relation to the space's subject. In the Person branch, those are the concepts under People, Pets, Work and Groups.

The app then offers "Move to ⟨space name⟩?" when the tag is added or the form is created. The hint reads only the pod's own form topics and tags and the user's own spaces. If the user declines, it is not offered again for that pod.

The relation exception is what keeps the hint quiet on the relationship pod. In the example, the *Sophia Walker* pod has Sophia as its form topic and she is the subject of Alice's space for Sophia, but its tag, Immediate Family, sits under People, so no hint appears. The same holds for *Paula Walker* (Immediate Family), *Ginger* (Pets) and *Acme* (Work). *Sophia's Health*, whose form topic is the subject of the space it already sits in, triggers nothing either. Had Alice filed *Sophia's Health* in her default space, the hint would have offered to move it.

## 2. Telli as placement coach (future)

The hint cannot see:

- a pod with no form topic, such as one with only member graphs;
- a pod with no category tag;
- a form topic that is not yet any space's subject, where the right answer may be "create a space for this party" — suggested only when the user already keeps several pods about that party's own life.

These need judgment, so they go to the user's personal agent. As the user creates, tags and moves pods, Telli notices a pod that by the rule belongs elsewhere, and suggests the change in the Telli chat, giving its reason in the rule's own terms. It never moves a pod itself.

This waits on two things the initial implementation does not have:

- **read-only access to the user's list of spaces and their subjects**, since the PACRs currently confine the agent to the current pod. Spaces are not pod content and belong to the user alone, so this may be safe to grant early. It is tracked in [open-items.md](open-items.md#space-placement).
- **a proactive mode**, in which the agent reacts to the user's pod actions rather than only to the user's messages.

## Where it is documented

- app-behavior.md, [Pod Spaces](../app-behavior.md#pod-spaces): "Placement is half enforced", and the placement hint.
- app-behavior.md, [Use Cases](../app-behavior.md#use-cases): the fourth use case, Coaching pod placement.
- notes/open-items.md, Space placement item 2: Telli's access to the user's spaces.
