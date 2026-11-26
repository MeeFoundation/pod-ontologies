# Space Placement

*Tellipod pod ontology — concept summary, updated 2026-11-25*

## The question

[Pod spaces](pod-spaces%2017-nov-2026.md) say whose life a pod belongs to, but nothing said how to choose a space. The example already looked like it followed a rule. Alice keeps a *Sophia Walker* pod in her default space *and* a space for Sophia holding three more pods about her. In the same way, she keeps a *Ginger* pod in her default space and two Ginger pods in her space for Ginger. The working hypothesis was that the party's identity and the relationship go in the default space, while specialized information about the party goes in that party's space. Working back from every placement in the example sharpened that hypothesis into a single rule.

## The rule

> **A pod sits in the space of the party whose life its category tag describes.**

Every category concept is implicitly possessive. Things, Health, Employees and Immediate Family are always *someone's*, and the space says whose.

**The test:** read the pod as "⟨space subject⟩'s ⟨category⟩: ⟨pod⟩". The pod belongs in the space where that sentence is true.

## The evidence

| Pod | Space | Category tag | Form topic | Reads as |
|---|---|---|---|---|
| Sophia Walker | default | `podcat:ImmediateFamily` | Sophia | **Alice's** immediate family |
| About Sophia | Sophia | `podcat:HealthWellness` | Sophia | **Sophia's** health & wellness |
| Jane Starostina | Sophia | `podcat:PrimaryCarePhysician` | Jane | **Sophia's** doctor |
| Appointment | Sophia | `podcat:MedicalAppointment` | Sophia's appointment | **Sophia's** appointment |
| Paula Walker | default | `podcat:ImmediateFamily` | Paula | **Alice's** immediate family |
| Honda | Paula | `podcat:Vehicles` | Paula's car | **Paula's** car |
| Ruth Alvarez | Paula | `podcat:PrimaryCarePhysician` | Ruth | **Paula's** doctor |
| Ginger | default | `podcat:Pets` | Ginger | **Alice's** pet |
| Medical | Ginger | `podcat:PetsMedical` | Ginger | **Ginger's** medical care |
| Untitled-1 | Ginger | `podcat:PetsCareAndFeeding` | Ginger | **Ginger's** care & feeding |
| Acme | default | `podcat:Work` | Acme | **Alice's** work |
| Alice Walker | Acme | `podcat:Employees` | none — a member graph about Alice | **Acme's** employee |

Two rows rule out the obvious alternative, "a pod goes in the space of whoever it is about":

- **About Sophia, Medical and Untitled-1 have the same form topic as the default-space pod** (Sophia, Ginger). What a pod is about does not decide its space.
- **The Alice Walker pod in Acme's space is about nobody but Alice.** A space for a party holds that party's *life*, not facts about them.

## What follows

- **The default space is the user's own life**, and the user's relationships to other parties are part of that life, which is why People, Pets and Work sit under `podcat:Person`. A space for another party works the same way: Sophia's relationship with her doctor is a relationship pod in *Sophia's* life.
- **The pod that identifies a party lives in the user's space.** A pod tagged with the party's relation to the user records who the party is *to the user*: enough to designate them (name, relation, species and breed, company profile), with the party as its form topic. The hypothesis's "identity and wholeness" is right only in this narrower sense.
- **A party's own identity documents go in their space.** A child's passport is the child's Government record, not the parent's.
- **A space holds the party's whole life**: their possessions, their own relationships to third parties, and even the user, where the user figures in that life.
- **A space is needed only once the user keeps something in another party's life.** Bob Johnson and Fred Flintstone have relationship pods and no space.
- **Each member applies the test from their own vantage.** Nothing about a space travels with an invitation, so Dave places *Appointment* by the same rule, in a space of his own.

## Where the example bends it

Paula is also Acme's employee, a fact that by the rule belongs in Acme's space. Alice keeps it instead inside her *Paula Walker* pod, which is about Paula as her mother, and gathers it with her #Acme user tag. This is consistent with the rule, since the pod as a whole is Alice's immediate family, and example.md says so.

## Open

Things that belong to two lives at once, such as a joint account or a family trip taken with a child, pass the test in two spaces. The proposed tiebreak is the default space whenever the user is themselves a party (Kyoto Trip, taken with Dave, stays in Alice's default space). It is tracked in [open-items.md](open-items.md#space-placement).

## Where it is documented

- README.md, [Pod Spaces](../README.md#pod-spaces): the rule and its consequences, theory only.
- example.md, [Pod Spaces](../example.md#pod-spaces): the rule applied to the Sophia, Ginger and Acme pairs, and the Paula-at-Acme exception.
