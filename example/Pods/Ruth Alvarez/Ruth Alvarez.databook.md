---
id: http://www.example.org/tpod/pods/pod-57
title: "Ruth Alvarez"
type: pod-databook
version: 1.0.0
created: 2026-11-16
description: >
  Pod DataBook for the "Ruth Alvarez" pod (category tag: podcat:PrimaryCarePhysician). It sits in Alice's pod space for Paula, anchored to the Paula Walker pod: Dr. Ruth Alvarez is Paula's primary care physician, whom Alice keeps on record so she can help her mother with appointments. It is a one-member pod with one member entry about :Self and one graph about :Ruth_Alvarez (the pod's subject).
tpod:
  categoryTag:
    - "podcat:PrimaryCarePhysician"
  space:
    id: "http://www.example.org/tpod/spaces/space-2"
    root: "podcat:Person"
    anchorPod: "http://www.example.org/tpod/pods/pod-19"
  creator: ":Self"
  owner: ":Self"
  member:
    id: "http://www.example.org/tpod/graphs/graph-111"
    claimant: ":Self"
    subject: ":Self"
    shape: "pshapes:ContactInfoShape"
  tool:
    - id: "http://www.example.org/tpod/tools/tool-39"
      type: "form"
      formTopic: ":Ruth_Alvarez"
      graph:
        - id: "http://www.example.org/tpod/graphs/graph-112"
          claimant: ":Self"
          shape:
            - "pshapes:PrimaryCarePhysicianShape"
            - "pshapes:ContactInfoShape"
---

## Graphs

<a id="graph-111"></a>
### Graph 111

#### Overview

This graph captures Alice's own bare identity claim (just her given name) — the pod's one required `member` entry, satisfying the single-member baseline. Alice is both the claimant and the subject.

#### Graph

```turtle
<!-- databook:id: ruth-alvarez-alice-member-graph -->
<!-- databook:graph: http://www.example.org/tpod/graphs/graph-111#graph -->
@prefix : <http://www.example.org/tpod#> .
@prefix cco: <https://w3id.org/cco-domains/cco/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix persona: <http://mee.foundation/ontologies/persona#> .

:Self rdf:type owl:NamedIndividual ,
               persona:Person .

:Self <https://w3id.org/cco-domains/cco/ont00001879> [  # designated by → GivenName
    rdf:type cco:ent00000002 ;  # GivenName
    <https://w3id.org/cco-domains/cco/ont00001765> "Alice"  # has text value
] .
```

<a id="graph-112"></a>
### Graph 112

#### Overview

This graph captures Alice's record of Dr. Ruth Alvarez, her mother Paula's primary care physician, including her medical specialty (Geriatrics), via `persona:specialty` — the `pod:formShape` of the tool `podcat:PrimaryCarePhysician` declares (`:PrimaryCarePhysicianShape`). The pod carries the same category tag as Alice's own doctor's pod and Sophia's; it is the pod space it sits in, Alice's space for Paula, that makes Ruth Paula's doctor. Alice is the claimant; Ruth is the pod's derived subject, held by its form tool.

#### Graph

```turtle
<!-- databook:id: ruth-alvarez-alice-graph -->
<!-- databook:graph: http://www.example.org/tpod/graphs/graph-112#graph -->
@prefix : <http://www.example.org/tpod#> .
@prefix persona: <http://mee.foundation/ontologies/persona#> .
@prefix cco: <https://w3id.org/cco-domains/cco/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

:Ruth_Alvarez rdf:type owl:NamedIndividual ,
               persona:Person ;
    rdfs:label "Ruth Alvarez (Primary Care Physician)"@en ;

    <https://w3id.org/cco-domains/cco/ont00001879> [  # designated by → GivenName
        rdf:type cco:ent00000002 ;  # GivenName
        <https://w3id.org/cco-domains/cco/ont00001765> "Ruth"  # has text value
    ] ;

    <https://w3id.org/cco-domains/cco/ont00001879> [  # designated by → FamilyName
        rdf:type cco:ent00000004 ;  # FamilyName
        <https://w3id.org/cco-domains/cco/ont00001765> "Alvarez"  # has text value
    ] ;

    <https://w3id.org/cco-domains/cco/ont00001917> [  # described by → Person Note
        rdf:type cco:ent00000048 ;
        <https://w3id.org/cco-domains/cco/ont00001765> "Paula Walker's primary care physician"
    ] ;

    persona:specialty "Geriatrics" .
```
