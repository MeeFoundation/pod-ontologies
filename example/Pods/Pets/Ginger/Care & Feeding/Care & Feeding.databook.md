---
id: http://www.example.org/tpod/pods/pod-42
title: "Care & Feeding"
type: pod-databook
version: 1.1.0
created: 2026-08-29
description: >
  Pod DataBook for folder "Care & Feeding" (pod:category: podcat:PetsCareAndFeeding). It is a two-member pod, shared by Alice with Paula, with two members (about :Self and :Paula_Walker) and one graph about :Ginger, Alice's cat (the pod's subject) — the day-to-day instructions for looking after Ginger, alongside her Medical pod's sibling record of her medical care.
tpod:
  category: "podcat:PetsCareAndFeeding"
  creator: ":Self"
  owner: ":Self"
  userTag:
    - "Ginger"
  member:
    - id: "http://www.example.org/tpod/graphs/graph-58"
      claimant: ":Self"
      subject: ":Self"
      shape: "pshapes:ContactInfoShape"
    - id: "http://www.example.org/tpod/graphs/graph-59"
      claimant: ":Paula_Walker"
      subject: ":Paula_Walker"
      shape: "pshapes:ContactInfoShape"
  tool:
    - id: "http://www.example.org/tpod/tools/tool-25"
      type: "form"
      formTopic: ":Ginger"
      graph:
        - id: "http://www.example.org/tpod/graphs/graph-60"
          claimant: ":Self"
---

## Graphs

<a id="graph-58"></a>
### Graph 58

#### Overview

This graph is one of the pod's two `member` entries, satisfying the two-member baseline alongside graph 59 (Paula's own claim, below). Alice is both the claimant and the subject — her own bare given-name claim, mirroring graph 59's identical pattern for Paula.

#### Graph

```turtle
<!-- databook:id: alice-ginger-care-feeding-member-graph -->
<!-- databook:graph: http://www.example.org/tpod/graphs/graph-58#graph -->
@prefix : <http://www.example.org/tpod#> .
@prefix persona: <http://mee.foundation/ontologies/persona#> .
@prefix cco: <https://w3id.org/cco-domains/cco/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .

:Self rdf:type owl:NamedIndividual ,
               persona:Person ;
    cco:ont00001879 [  # designated by → GivenName
        rdf:type cco:ent00000002 ;  # GivenName
        cco:ont00001765 "Alice"  # has text value
    ] .
```

<a id="graph-59"></a>
### Graph 59

#### Overview

This pod was created by Alice and later shared with Paula, making the pod a two-member pod. This graph is Paula's own bare identity claim (just her given name) — the pod's second `member` entry, satisfying the two-member baseline alongside graph 58 (Alice's own claim, above). Paula is both the claimant and the subject.

#### Graph

```turtle
<!-- databook:id: paula-ginger-care-feeding-member-graph -->
<!-- databook:graph: http://www.example.org/tpod/graphs/graph-59#graph -->
@prefix : <http://www.example.org/tpod#> .
@prefix persona: <http://mee.foundation/ontologies/persona#> .
@prefix cco: <https://w3id.org/cco-domains/cco/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .

:Paula_Walker rdf:type owl:NamedIndividual ,
               persona:Person ;
    cco:ont00001879 [  # designated by → GivenName
        rdf:type cco:ent00000002 ;  # GivenName
        cco:ont00001765 "Paula"  # has text value
    ] .
```

<a id="graph-60"></a>
### Graph 60

#### Overview

This graph captures Alice's day-to-day care and feeding instructions for her cat Ginger — what to feed her and when, and where she sleeps — so that Paula (or anyone else looking after Ginger) knows how to care for her. Alice is the claimant; Ginger is the pod's `subject` but, since she has no `p:Person` individual of her own, her graph is held by the pod's form tool rather than being one of the required `member` entries (graphs 58 and 59, above, fill those slots instead). No formal template governs this content (unlike her sibling Medical pod's `pets:PetMedicationRecord`, or her own basic identifying claim in graph 37, now governed by `pets:Pet`) — no `pod:TemplatePod` points its `pod:category` at `podcat:PetsCareAndFeeding` — so it is asserted directly as a plain comment.

#### Graph

```turtle
<!-- databook:id: ginger-care-feeding-graph -->
<!-- databook:graph: http://www.example.org/tpod/graphs/graph-60#graph -->
@prefix : <http://www.example.org/tpod#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

:Ginger_CareAndFeeding rdf:type owl:NamedIndividual ;
    rdfs:label "Ginger's Care & Feeding Instructions"@en ;
    rdfs:comment "Fed twice daily, 7am and 6pm: half a cup of dry food (Purina Pro Plan) plus a spoonful of wet food. Fresh water bowl refilled daily. Sleeps in a cat bed in Alice's bedroom. Litter box is in the laundry room and is scooped daily."@en .
```
