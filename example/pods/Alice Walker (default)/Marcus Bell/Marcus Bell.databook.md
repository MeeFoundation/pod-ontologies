---
id: http://www.example.org/tpod/pods/pod-56
title: "Marcus Bell"
type: pod-databook
version: 1.0.0
created: 2026-11-16
description: >
  Pod DataBook for the "Marcus Bell" pod (category tag: podcat:PrimaryCarePhysician), in Alice's default pod space: Dr. Marcus Bell is Alice's own primary care physician. It is a one-member pod with one member entry about :Self and one graph about :Marcus_Bell (the pod's subject).
tpod:
  categoryTag:
    - "podcat:PrimaryCarePhysician"
  creator: ":Self"
  owner: ":Self"
  member:
    id: "http://www.example.org/tpod/graphs/graph-109"
    claimant: ":Self"
    subject: ":Self"
    shape: "pshapes:ContactInfoShape"
  tool:
    - id: "http://www.example.org/tpod/tools/tool-38"
      type: "form"
      formTopic: ":Marcus_Bell"
      graph:
        - id: "http://www.example.org/tpod/graphs/graph-110"
          claimant: ":Self"
          shape:
            - "pshapes:PrimaryCarePhysicianShape"
            - "pshapes:ContactInfoShape"
---

## Graphs

<a id="graph-109"></a>
### Graph 109

#### Overview

This graph captures Alice's own bare identity claim (just her given name) — the pod's one required `member` entry, satisfying the single-member baseline. Alice is both the claimant and the subject.

#### Graph

```turtle
<!-- databook:id: marcus-bell-alice-member-graph -->
<!-- databook:graph: http://www.example.org/tpod/graphs/graph-109#graph -->
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

<a id="graph-110"></a>
### Graph 110

#### Overview

This graph captures Alice's record of Dr. Marcus Bell, her own primary care physician, including his medical specialty (Internal Medicine), via `persona:specialty` — the `pod:formShape` of the tool `podcat:PrimaryCarePhysician` declares (`:PrimaryCarePhysicianShape`). The pod sits in Alice's default space, which is what makes him her doctor rather than Sophia's or Paula's: the category tag alone, `podcat:PrimaryCarePhysician`, says only that he is someone's. Alice is the claimant; Marcus is the pod's derived subject, held by its form tool.

#### Graph

```turtle
<!-- databook:id: marcus-bell-alice-graph -->
<!-- databook:graph: http://www.example.org/tpod/graphs/graph-110#graph -->
@prefix : <http://www.example.org/tpod#> .
@prefix persona: <http://mee.foundation/ontologies/persona#> .
@prefix cco: <https://w3id.org/cco-domains/cco/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

:Marcus_Bell rdf:type owl:NamedIndividual ,
               persona:Person ;
    rdfs:label "Marcus Bell (Primary Care Physician)"@en ;

    <https://w3id.org/cco-domains/cco/ont00001879> [  # designated by → GivenName
        rdf:type cco:ent00000002 ;  # GivenName
        <https://w3id.org/cco-domains/cco/ont00001765> "Marcus"  # has text value
    ] ;

    <https://w3id.org/cco-domains/cco/ont00001879> [  # designated by → FamilyName
        rdf:type cco:ent00000004 ;  # FamilyName
        <https://w3id.org/cco-domains/cco/ont00001765> "Bell"  # has text value
    ] ;

    <https://w3id.org/cco-domains/cco/ont00001917> [  # described by → Person Note
        rdf:type cco:ent00000048 ;
        <https://w3id.org/cco-domains/cco/ont00001765> "Alice Walker's primary care physician"
    ] ;

    persona:specialty "Internal Medicine" .
```
