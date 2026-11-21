# Pod Spaces

*Tellipod pod ontology — concept summary, updated 2026-11-17*

## The problem

A pod's **category tags** (`pod:categoryTag`, drawn from `podcat:PodCategoryScheme`) say *what kind* of thing a pod is about: Things, Travel, Pets, Primary Care Physician. They never say *whose*. A user's own things and their mother's things are both `podcat:Things`, so a search for Things mixes the two. 

Before pods were flattened, nesting carried that missing fact. A pod placed beneath the pod about a person (Alice › People › Immediate Family › Paula › Things) belonged to that person's life, and the whole Person branch of the taxonomy could be reused there. Removing nesting removed this second axis.

Without pod spaces Tellipod is really only convenient for organizing information about one's self. It doesn't scale to more complex situations such as when one has to take care of a child or aging parent. For example Alice, Paula and Sophia may all have different primary care physicians, without pod spaces the user is forced to manually add #Paula or #Sophia tags to pods and search by these tags to distinguish the pods related to these people. The newbie user can indeed use user tags to do this, but when there is a lot of information about, say, Paula or Sophia, creating a separate pod space is much more convenient: no need to add user tags like #Sophia and instead of adding #Sophia to the view filter, just use the pod space switcher control. 

**Pod spaces** restore it without bringing back nesting.

## The concept

A **pod space** is the life a set of a user's pods belongs to: the user's own, or the life of a person, organization or pet the user keeps pods about.

- **Every pod sits in exactly one space.**
- **Each space is rooted at one top concept of the taxonomy.** There are three top concepts: `podcat:Person` for a person's life, `podcat:Organization` for an organization's, and `podcat:Pet` for a pet's. Inside a space, that whole branch is available, so a space for the user's mother has its own Things, Travel, People and the rest, and a space for their cat has its own Health, Care & Feeding and Records.
- **Every category tag of every pod in a space must fall under the space's root**, by `skos:broader` transitively or through an extension concept's `skos:broadMatch`. A pod may still carry several tags (0..N) from different branches beneath that root. It can never carry tags from two different top concepts, so the old "Mixed" category type no longer exists.
- **There is one default space.** It is the user's own life: Person-rooted, named with the user's own name (shown as "(default)"), with the user (`:Self`) as its subject.
- **A space may name its subject**: the person, organization or pet whose life it holds. This is optional. A space can be just a name and a root.
- **Only people, organizations and pets get spaces.** A vehicle or document is the topic of a pod in someone's space, never a space's subject. The taxonomy has a branch only for those three kinds of life.
- **Spaces are flat and independent.** They never nest, and they link to nothing: not to each other, and not to any pod. A relationship between parties, such as Paula being Alice's mother or Paula having a sister, is recorded in graphs, as every relationship is.

## The Pet branch

```
podcat:Pet
├─ Health (PetHealth)
│   ├─ Medical (PetsMedical)
│   │   ├─ Veterinarians · Vet Visits · Medications · Vaccinations · Devices
│   └─ Insurance
├─ Care & Feeding (PetsCareAndFeeding)
│   └─ Diet · Grooming · Exercise
├─ Care Providers
│   └─ Sitters & Walkers · Boarding · Groomers · Trainers
├─ Records
│   └─ Registration · Microchip · Adoption & Pedigree
├─ Things
└─ Travel
```

## Ontology terms (`pod.ttl`)

| Term | Kind | Domain → Range | Cardinality | Meaning |
|---|---|---|---|---|
| `pod:PodSpace` | class | — | — | The life a set of pods belongs to. It is not a pod, holds no content, and takes no part in the `pod:Pod` hierarchy. |
| `pod:space` | object property | `pod:InstancePod` → `pod:PodSpace` | exactly 1 | The space a pod sits in. Per-member state. |
| `pod:spaceRoot` | object property | `pod:PodSpace` → `skos:Concept` | exactly 1 | `podcat:Person`, `podcat:Organization` or `podcat:Pet`. |
| `pod:spaceName` | datatype property | `pod:PodSpace` → `xsd:string` | exactly 1 | The user-chosen name. It need not be unique. |
| `pod:spaceSubject` | annotation property | `pod:PodSpace` → `xsd:anyURI` | 0..1 | The person (Person root), organization (Organization root) or pet (Pet root) whose life the space holds. `:Self` marks the default space. |

**Validation:**
- **`shacl/pod-shacl.ttl`:** `:InstancePodShape` requires exactly one `pod:space`, and a SPARQL constraint requires every tag to reach the space's root. `:PodSpaceShape` constrains the root, name and subject.
- **integrity.md:** TTL-9 checks across all pods that there is exactly one `:Self`-subject default space, Person-rooted, that each subject is typed as its root implies, and that every tag reaches its root. YAML-11 checks the `tpod.space` frontmatter.

## App behavior

- **Viewing and switching.** The app shows either all spaces or one. A new user starts in all spaces (`Pod space: all`). A picker lists "All spaces" first, then every space by name, with the default first. A pod created while viewing all spaces goes into the default space.
- **Creating a space.** The user chooses "New space", names it and picks its root. Optionally, they choose the person, organization or pet whose life it holds, and the app offers that party's name for the space.
- **Moving a pod** between spaces changes only the moving member's copy. Tags that don't fall under the new root are dropped, and the user is told which before confirming. No tool is ever removed.
- **Renaming a space** changes only its name.
- **Deleting a space** moves its pods into the default space, dropping any tags that don't fit. The default space can't be deleted.
- **Search and views.** A tag search or persistent view is scoped either to all spaces, the starting scope, or to one space the user picks. In all spaces, results are grouped under a header for each space.
- **Per-member placement.** Like tags, placement is never shared content: each member puts a shared pod in a space of their own.
- **Sharing.** Nothing about the sender's space travels with an invitation: no name, no root, no subject. The joining member chooses which of their own spaces the pod goes in, with the default preselected. The sender's category tags are suggested only where they fall under that space's root.

## How a view shows spaces

A view's header has two lines: the space it is scoped to, then the tags it searches for.

```
Pod space: Alice Walker (default)        Pod space: all
View tags: #Things                       View tags: #Things
```

- **All-spaces view.** This is where a new user starts. The header reads `Pod space: all`, and each space is drawn as a **space panel**: a large grey rectangle labeled `Pod space: <name>` at its top left, holding that space's pods.
- **Single-space view.** The header names the space, so no panels are drawn.
- **A pod box never names its space.** From the UI's point of view a pod is *in* a space, not labeled with one, so the space is the panel around the box, not a line inside it.
- **Panels are outermost.** Each space's own green tag group headers sit inside its panel.
- **Each pod sits in exactly one panel.** Panels partition the view. A tag group header does not: a pod with several tags can appear under several.
- **Order.** Panels are stacked with the default space first, then the others by name, as in the space picker. A space with no matching pod gets no panel.

```
Pod space: all
View tags: #Vehicles
┌ Pod space: Alice Walker (default) ─────────┐
│ #Things                                    │
│   └─ RAV4     #Vehicles                    │
└────────────────────────────────────────────┘
┌ Pod space: Paula Walker ───────────────────┐
│ #Things                                    │
│   └─ Honda    #Vehicles                    │
└────────────────────────────────────────────┘
```

## Worked example (Alice Walker)

| Space | Root | Subject | Pods in it |
|---|---|---|---|
| Alice Walker (default) | `podcat:Person` | `:Self` | All other pods, including the pods *about* Sophia, Paula and Acme |
| Sophia Walker | `podcat:Person` | `:Sophia_Walker` | About Sophia, Jane Starostina, Appointment |
| Paula Walker | `podcat:Person` | `:Paula_Walker` | Honda, Ruth Alvarez |
| Acme | `podcat:Organization` | `:Acme` | Alice Walker (`podcat:Employees`) |
| Ginger | `podcat:Pet` | `:Ginger` | Medical, Untitled-1 |

Alice keeps five all-spaces views. Three of them, Sophia, Acme and Ginger, gather a user tag across spaces. The other two show why spaces are needed:

- **Vehicles.** Alice has a pod for her own car (*RAV4*) and one for her mother's car (*Honda*, in her space for Paula). Both are tagged `podcat:Vehicles` and hold the same Vehicle form, and only the space panel each sits in says whose car it is.
- **Primary care physicians.** *Marcus Bell* (Alice's doctor, default space), *Ruth Alvarez* (Paula's doctor) and *Jane Starostina* (Sophia's doctor) carry the same tag and the same form. Only the space says whose doctor each is.

Spaces also remove the need for names that carry a qualifier for the person, and a pod's name is whatever the user likes: Sophia's pods are *About Sophia* and *Appointment*, Ginger's are *Medical* and the unnamed *Untitled-1*. 
Ginger shows the Pet branch at work. The *Ginger* pod, about the cat herself, sits in Alice's default space, tagged `podcat:Pets` from the Person branch, the way the *Paula Walker* pod is tagged `podcat:ImmediateFamily`. Ginger's medical record and care instructions live in the Pet-rooted Ginger space, in a pod named plain *Medical* and one Alice never named, which the app called *Untitled-1*, tagged `podcat:PetsMedical` (under `podcat:PetHealth`) and `podcat:PetsCareAndFeeding`; the space supplies the "Ginger" their names used to carry.

Acme shows the Organization branch at work. The *Acme* pod sits in Alice's Person-rooted default space, tagged `podcat:Work`. Her own employee record lives in the separate Organization-rooted Acme space, the only kind of space where a tag like `podcat:Employees` can be used.

## Scaffolding (this repo only)

- **Frontmatter.** A pod outside the default space carries `tpod.space: {id, name, root, subject?}` in its DataBook frontmatter, restated by every pod in that space. A default-space pod carries no `tpod.space` at all. Its space (`space-0`, named "Alice Walker", subject `:Self`) is generated by `helpers/databook_graphs.py`.
- **Folders.** The example pods sit at `example/pods/<Space>/<Name>/`: one folder per space (`Alice Walker (default)`, `Sophia Walker`, `Paula Walker`, `Acme`, `Ginger`), and in each one folder per pod. Pods in different spaces may share a name. A space folder is not a pod.

## Design decisions

- **One taxonomy scheme with three top concepts, not three schemes.** A space picks a top concept.
- **Category tags stay 0..N.** The constraint is that they all fall under the space's root.
- **Pet spaces, with their own branch.** `podcat:Pet` is a third top concept. Under Person, `podcat:Pets` keeps only the pod *about* a pet in its owner's life. Medical, Care & Feeding and the rest of a pet's life moved under `podcat:Pet`, so each concept sits in exactly one place.
- **Space as a panel, not a label.** An all-spaces view draws each space as a grey panel holding its pods, instead of printing the space inside each pod box. That matches the model: a pod sits in exactly one space.
- **No anchors.** An earlier draft anchored each space to the pod about its party, which gave navigation and a chain of spaces. It was dropped. Its cost (an inverse-functional link, cycle checks, deletion rules) bought only convenience, plus relationship information the graphs already hold. The optional `pod:spaceSubject` keeps the one thing worth keeping: a machine-readable answer to "whose space is this?"

## Diagram redraw status

All diagrams are redrawn (2026-11-17/18). Every example diagram's view header names its pod space, and every legend has four swatches: Person, Org, Pet (pale yellow, `#FFF9BE` as exported, `#FFF9C4` in the OmniGraffle source) and None. Five views are all-spaces, drawing each space as a grey panel: `people2.png` (#Sophia), `work.png` (#Acme), `pets.png` (#Ginger), `vehicles.png` (#Vehicles) and `medical.png` (#PrimaryCarePhysician). `pod.png` shows `PodSpace`, `pod-categories.png` the `Pet` top concept, and `folder-mapping.png` the space-folder level of `example/pods/`.
