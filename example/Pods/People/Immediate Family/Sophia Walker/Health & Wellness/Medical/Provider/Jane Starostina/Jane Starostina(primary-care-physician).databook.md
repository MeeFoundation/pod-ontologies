---
id: http://www.example.org/tpod/pods/pod-14
title: "Jane Starostina"
type: pod-databook
version: 1.4.0
created: 2026-07-10
description: >
  Pod DataBook for folder "Jane Starostina" (pod:category: podcat:PrimaryCarePhysician). It is a one-member pod with one member entry about :Self and one graph about :Jane_Starostina (the pod's subject).
tpod:
  category: "podcat:PrimaryCarePhysician"
  creator: ":Self"
  owner: ":Self"
  member:
    id: "http://www.example.org/tpod/graphs/graph-34"
    claimant: ":Self"
    subject: ":Self"
    shape: "pshapes:ContactInfoShape"
  tool:
    - id: "http://www.example.org/tpod/tools/tool-22"
      type: "form"
      formTopic: ":Jane_Starostina"
      graph:
        - id: "http://www.example.org/tpod/graphs/graph-25"
          claimant: ":Self"
          shape:
            - "pshapes:PrimaryCarePhysicianShape"
            - "pshapes:ContactInfoShape"
---

## Graphs

<a id="graph-34"></a>
### Graph 34

#### Overview

This graph captures Alice's own bare identity claim (just her given name) — the pod's one required `member` entry, satisfying the single-member baseline. Alice is both the claimant and the subject.

#### Graph

```turtle
<!-- databook:id: alice-jane-starostina-member-graph -->
<!-- databook:graph: http://www.example.org/tpod/graphs/graph-34#graph -->
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

<a id="graph-25"></a>
### Graph 25

#### Overview

This graph captures Alice's record of Dr. Jane Starostina, who is the primary care physician for Alice's daughter, Sophia Walker, including her medical specialty (Endocrinology), via `persona:specialty` — the `pod:formShape` of the tool `podcat:PrimaryCarePhysician` declares (`:PrimaryCarePhysicianShape`). Alice keeps this information so she and her husband Dave can coordinate Sophia's medical appointments. Alice is the claimant; Jane is the pod's `subject` but, since this pod now has a real member entry (graph 34, above) about Alice herself, Jane's graph is held by the pod's form tool rather than being one of the required `member` entries.

#### Graph

```turtle
<!-- databook:id: jane-starostina-alice-graph -->
<!-- databook:graph: http://www.example.org/tpod/graphs/graph-25#graph -->
@prefix : <http://www.example.org/tpod#> .
@prefix persona: <http://mee.foundation/ontologies/persona#> .
@prefix cco: <https://w3id.org/cco-domains/cco/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

:Jane_Starostina rdf:type owl:NamedIndividual ,
               persona:Person ;
    rdfs:label "Jane Starostina (Primary Care Physician)"@en ;

    <https://w3id.org/cco-domains/cco/ont00001879> [  # designated by → GivenName
        rdf:type cco:ent00000002 ;  # GivenName
        <https://w3id.org/cco-domains/cco/ont00001765> "Jane"  # has text value
    ] ;

    <https://w3id.org/cco-domains/cco/ont00001879> [  # designated by → FamilyName
        rdf:type cco:ent00000004 ;  # FamilyName
        <https://w3id.org/cco-domains/cco/ont00001765> "Starostina"  # has text value
    ] ;

    <https://w3id.org/cco-domains/cco/ont00001917> [  # described by → Person Note
        rdf:type cco:ent00000048 ;
        <https://w3id.org/cco-domains/cco/ont00001765> "Sophia Walker's primary care physician"
    ] ;

    persona:specialty "Endocrinology" .
```
