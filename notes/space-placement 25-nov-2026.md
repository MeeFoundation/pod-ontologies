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
| Sophia's Health | Sophia | `podcat:HealthWellness` | Sophia | **Sophia's** health & wellness |
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

- **Sophia's Health, Medical and Untitled-1 have the same form topic as the default-space pod** (Sophia, Ginger). What a pod is about does not decide its space.
- **The Alice Walker pod in Acme's space is about nobody but Alice.** A space for a party holds that party's *life*, not facts about them.

## What follows

- **The default space is the user's own life**, and the user's relationships to other parties are part of that life, kept under the People, Pets and Work branches of `podcat:Person`. A space for another party works the same way: Sophia's relationship with her doctor is a relationship pod in *Sophia's* life.
- **The relationship pod lives in the default space.** A pod tagged with the party's relation to the user is the user's relationship with that party, with the party as its form topic or as one of its members, and holds whatever the user chooses to keep about them (name, contact details, birthday, preferences, notes; species and breed; company profile; anything else). The hypothesis's "identity and wholeness" is right in this sense.
- **What belongs to the party's own life goes in their space, whatever kind of information it is**: their health and providers, possessions, finances and accounts, schooling, travel and identity documents. A child's passport is the child's Government record, not the parent's, and a parent's car is the parent's Things. A pet's medical care and feeding go in the pet's space, and an organization's employees and customers in the organization's.
- **Who a pod is about does not decide; whose life it is part of does.** A pod planning a friend's birthday party is the user's Events, and Alice's *Marcus Bell* pod is about Marcus but is her own Primary Care Physician, so both go in the default space.
- **The rule places pods, not claims.** The same claim about a party may be made in their relationship pod, in a pod in their space, or in both; each is made separately, and nothing links them.
- **A space holds the party's life as the user keeps it**: their possessions, their own relationships to third parties, and even the user, where the user figures in that life.
- **A space is for a life the user helps run, not for everyone the user knows.** See below.
- **Each member applies the test from their own vantage.** Nothing about a space travels with an invitation, so Dave places *Appointment* by the same rule, in a space of his own.

## Spaces are for lives the user helps run

If Alice knows 100 people and has a few facts about each, she does not need 100 spaces. The rule decides where a **pod** goes, not where a **fact** goes. Facts about a person go first into the relationship pod: everything Alice knows of them as a person in her life, such as their name, contact details, birthday, preferences and notes. That pod is tagged with their relation to Alice, so it is Alice's, and it sits in her default space. That makes one pod per person and no spaces. The example already works this way: the *Bob Johnson* pod, in Alice's default space, holds her notes about Bob, his favorite drink included (graph 04).

The placement question arises only when the user splits an aspect of another party's life into a pod of its own, tagged from that party's branch: their health, their doctor, their car, their SSN. Those are pods the user keeps on the party's behalf, for a child, an aging parent, a pet or an employer. That is the threshold for a space. For most of the people Alice knows she runs nothing, so they never need one. Nothing pushes her toward more spaces, either: the app's placement hint fires only when a pod's form topic is already another space's subject, so without a space for Bob it stays silent.

## Where the example bends it

Paula is also Acme's employee, a fact that by the rule belongs in Acme's space. Alice keeps it instead inside her *Paula Walker* pod, which is about Paula as her mother, and gathers it with her #Acme user tag. This is consistent with the rule, since the pod as a whole is Alice's immediate family, and example.md says so.

## Open

Things that belong to two lives at once, such as a joint account or a family trip taken with a child, pass the test in two spaces. The proposed tiebreak is the default space whenever the user is themselves a party (Kyoto Trip, taken with Dave, stays in Alice's default space). It is tracked in [open-items.md](open-items.md#space-placement).

## Where it is documented

- README.md, [Placing Pods in Spaces](../README.md#placing-pods-in-spaces): the rule and its consequences, theory only.
- example.md, [Placing Pods in Spaces](../example.md#placing-pods-in-spaces): the rule applied to every space's pods, and the Paula-at-Acme exception.
