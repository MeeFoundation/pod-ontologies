# Three Tagging Styles in the Tellipod Example

*Summary of changes made 2026-11-18 to `example.md`, `app-behavior.md` and `README.md` in pod-ontologies.*

## The concern

The example blurred a real distinction between three kinds of user:

1. those who tag only with **category tags** (`pod:categoryTag`, picked from the taxonomy),
2. those who tag only with **user tags** (`pod:userTag`, free text), and
3. those who use **both**.

The worry was that too many example pods carried both kinds, so none of the three styles came through clearly.

## What the analysis found

These are the tags on every example pod's `tpod:` block:

| Tag pattern | Count | Pods |
|---|---|---|
| Category tag only | 25 | Arca, ATT, Birth Certificate, Bob Johnson, Boston Hub Society, Boston, CHVA, Citibank, Drivers License, Facenook, Fred Flintstone, Google, Hilton, Kyoto Trip 2027, Marcus Bell, Paradise, Passport, PRIVO, RAV4, SSN, Things, Honda, Ruth Alvarez |
| Both | 9 | Ginger, Medical, Untitled-1 ("Ginger"); Sophia Walker, About Sophia, Jane Starostina, Appointment ("Sophia"); Acme, Alice Walker, Paula Walker ("Acme") |
| User tag only | 0 | — |

The deeper problem was not the mix itself. **Every tag in the example is Alice's.** The pod DataBooks record Alice's instance only, and one user can only show one tagging style. However Alice's own tags were added or deleted, the example could never show three *kinds of user*.

Alice is a "both" user. Each of her nine user tags does something no category tag can do:

- **"Sophia"** gathers four pods whose category tags (`podcat:ImmediateFamily`, `podcat:HealthWellness`, `podcat:PrimaryCarePhysician`, `podcat:MedicalAppointment`) meet only at the top concept `podcat:Person`.
- **"Ginger"** and **"Acme"** gather pods that sit in more than one pod space.

Deleting any of them would break a persistent view the example relies on, so none was deleted.

## The approach

Tags are per-member: no tag is shared pod content. Two other people already share pods with Alice and run their own instances of the app. That gave the example three users, each with a different style, with no change to the data:

| User | Tags with | Pods (shared with Alice) | Their tags | How they find them |
|---|---|---|---|---|
| **Alice** | both | all of hers | unchanged: a category tag on every pod, a user tag on nine | category views plus her Sophia, Ginger and Acme views |
| **Paula** | category tags only | Medical, Untitled-1 | accepts the suggested `podcat:PetsMedical` and `podcat:PetsCareAndFeeding`; adds no user tag | by category: a Health search in her own space for Ginger finds Medical through `podcat:PetHealth` |
| **Dave** | user tags only | Sophia Walker, Appointment, Kyoto Trip 2027 | declines every suggested category tag, so all three are Custom on his side; adds "Sophia", "Sophia", "Kyoto" | by his own words |

**Why this casting:**

- **Paula as category-only** needed the least change. app-behavior.md's Joining a Pod worked example already had her accepting `podcat:PetsMedical`, and it still teaches the rule that a suggestion is filtered by the root of the space she chooses. The only removal was the sentence in which she adds a "Ginger" user tag.
- **Dave as user-tag-only** shows something the example had never shown before: a joining member declining suggested category tags.
  - His "Sophia" tag is spelled exactly like Alice's, yet the two are separate, because user tags are never sent.
  - Declining `podcat:Trips` also shows that a tool reaches every member even when the tag that brought it does not. The itinerary form tool came from the Trips template and is shared content.
- **Bob, Fred, Marcy and Henry were left out.** Nothing in the example looks at their tags, and three users are enough to show three styles.

**Why no data or diagram changes:** the `tpod:` blocks record Alice's instance only, so Dave's and Paula's tags belong in prose. Storing them in Alice's DataBooks would be wrong. For the same reason, no `.databook.md`, `.ttl` or image file changed, and no integrity checks needed rerunning.

## Documentation changes

### `example.md`

- **Tags and Views:** a new `#### Three Ways to Tag` subsection with the three-user table. It explains:
  - that most of Alice's pods carry only a category tag, since that tag brings the template's tools, and she adds a user tag where a category falls short;
  - that Paula files by category only and Dave never opens the taxonomy;
  - that Paula's and Dave's tags live in their own instances and are not stored in the example's pods.
- **Taking Care of Sophia:**
  - The *Sophia Walker* pod: Dave declined the suggested `podcat:ImmediateFamily` and tagged the pod "Sophia" himself.
  - The *Appointment* pod: Dave declined `podcat:MedicalAppointment` and tagged it "Sophia". His tag and Alice's are spelled the same, but each was typed by its own member and lives only in that member's copy.
- **Planning a Trip with an Agent:** tagging the pod `podcat:Trips` gave it the itinerary form tool its template declares. Dave declined the suggestion and tagged it "Kyoto", but the tool reached him anyway, since a tool is shared content and a tag is not.
- **Caring for Ginger:** Paula tags only by category. She accepts `podcat:PetsMedical`, and later `podcat:PetsCareAndFeeding` on *Untitled-1*, and adds no user tag to either.

### `app-behavior.md`

- **Joining a Pod:**
  - Replaced "Paula can add a user tag 'Ginger' of her own … and a search for her own 'Ginger' tag finds it too" with Paula, who organizes by category alone, adding no user tag.
  - Added one sentence: a joining member may equally decline every suggestion and tag with words of their own only, which leaves the pod Custom on their side. It links to example.md's Three Ways to Tag.

### `README.md`

- **Tags:** a new general paragraph, with no example names, following the README theory-vs-example rule. It says:
  - which kinds of tag a user uses is their own preference, and the model favors none;
  - a user may file only by category tag, only by user tag, or both, and a pod may carry neither;
  - category tags bring template tools and broader-concept search, while user tags gather what the taxonomy does not;
  - members of the same shared pod may each tag it in a different style.

  It ends with a one-line link to example.md's Three Ways to Tag.

## Considered and not done

- **Giving Alice a pod with only a user tag.** That would put the Custom case into the actual data and into a diagram; no example pod currently has zero category tags, so the PNG-1f "no green line" branch is never exercised. It was left out because the three-users story does not need it. It would mean editing a DataBook's `tpod.categoryTag`, redrawing that pod's diagram, and rerunning the PNG and YAML checks.
- **Deleting any of Alice's user tags.** Rejected, because each one supports a view that no category tag can reproduce.

## Status

All edits are made in the working tree and not yet committed.
