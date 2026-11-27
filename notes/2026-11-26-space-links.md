# Space Links

*Tellipod pod ontology — concept summary, updated 2026-11-26*

## The need

A relationship pod in the user's default space, such as one about their daughter, mother, cat or employer, often has a space of its own on the other side: the space where the user keeps that party's own life. Tag searches and persistent views list pods, but nothing in a list led from such a pod to its party's space. The user had to know the space existed and switch to it in the picker.

## The concept

A **space link** is a button beside a pod in any list of pods that opens the space of a party the pod is about.

- **Label.** "Open space: ⟨space name⟩", e.g. "Open space: Sophia Walker". In a dense view it shrinks to a chip, "↗ Sophia Walker", with the full label as its tooltip. "View Pod Space" was considered and rejected: every pod already sits in a space, so it reads as "show this pod's own space", the opposite of what the button does. A possessive label ("Sophia Walker's space") reads badly for user-chosen names like "Mom" or "Acme".
- **When a pod gets one.** For each of the user's spaces, other than the one the pod sits in, whose subject is one of the parties the pod is about. That set is the pod's **derived subject** (integrity.md's YAML-4): its form topics if it has a form tool, otherwise its members' subjects. Two exclusions:
  - **The user themselves.** They are a member of every pod and the subject of the default space, so matching on them would link every pod to the default space.
  - **Co-members, when the pod has a form tool.** The derived subject is then the form topics only. So Ginger's *Medical* pod, which Paula is a member of, links to no space for Paula: it is about Ginger, and it already sits in Ginger's space.

  A space with no subject never matches.
- **Where it appears.** Beside the pod in every list: search results by tag, name or property, and persistent views. It also appears in the pod's own header. Several matching spaces give one link each, sorted by name; more than two collapse into a "Spaces ▾" menu.
- **What pressing it does.** The same as choosing that space in the picker with an empty search: the current pod space becomes that space and all its pods are shown. It counts as a switch, so the picker remembers it. **Back** returns to the previous list with its tags and scope. A persistent view's stored query and scope are never changed.
- **The reverse.** A space's header links to each pod in the user's other spaces whose derived subject includes the space's subject, typically the relationship pod: "Open pod: ⟨pod name⟩".

## Nothing stored

Space links are computed each time a list is drawn, by matching a pod's derived subject against the user's spaces' `pod:spaceSubject` values. Nothing is stored on the pod or the space, which keeps README's statement that spaces link to nothing true. Nothing is shared either: spaces are secret, so a space link exists only in the user's own copy.

## In the example

In Alice's People, Sophia, Ginger and Acme views, the *Sophia Walker*, *Paula Walker*, *Ginger* and *Acme* pods carry space links to her spaces for Sophia, Paula, Ginger and Acme. The pods already inside those spaces carry none. The example diagrams do not draw space links yet.

## Where it is documented

- app-behavior.md, [Space Links](../app-behavior.md#space-links), and the "From a pod to its party's space, and back" bullet in [Pod Spaces](../app-behavior.md#pod-spaces).
- README.md, [Pod Spaces](../README.md#pod-spaces): the match is computed, never stored.
- example.md, [Tags and Views](../example.md#tags-and-views).
