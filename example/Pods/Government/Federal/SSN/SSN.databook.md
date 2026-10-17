---
id: http://www.example.org/tpod/pods/pod-06
title: "SSN"
type: pod-databook
version: 2.0.0
created: 2026-07-10
description: >
  Pod DataBook for folder "SSN" (pod:category: podcat:SSN). It is a one-member pod with one
  member entry about :Self and one tool graph about :Self (the pod's subject), carrying
  Alice's Social Security number.
tpod:
  category: "podcat:SSN"
  creator: ":Self"
  owner: ":Self"
  member:
    id: "http://www.example.org/tpod/graphs/graph-23"
    claimant: ":Self"
    subject: ":Self"
    shape: "pshapes:ContactInfoShape"
  tool:
    - id: "http://www.example.org/tpod/tools/tool-12"
      type: "form"
      formTopic: ":Self"
      graph:
        - id: "http://www.example.org/tpod/graphs/graph-80"
          claimant: ":Self"
          shape: "pshapes:SSNShape"
---

## Graphs

<a id="graph-23"></a>
### Graph 23

#### Overview

This graph is the pod's one required `member` entry — a pod with a single `member` entry in the user's own category-pod tree always has `:Self` as that member (see YAML-6). Alice is both the claimant and the subject. It carries her given name, satisfying the `ContactInfoShape` every templated pod's `member` content is now expected to conform to (`pod:memberShape`) — no longer the SSN itself, which now lives in this pod's tool graph instead (graph 80).

#### Graph

```turtle
<!-- databook:id: alice-ssn-member-graph -->
<!-- databook:graph: http://www.example.org/tpod/graphs/graph-23#graph -->
@prefix : <http://www.example.org/tpod#> .
@prefix cco: <https://w3id.org/cco-domains/cco/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix persona: <http://mee.foundation/ontologies/persona#> .

:Self rdf:type owl:NamedIndividual ,
               persona:Person .

:Self <https://w3id.org/cco-domains/cco/ont00001879> [  # designated by → GivenName (ContactInfoShape)
        rdf:type cco:ent00000002 ;
        <https://w3id.org/cco-domains/cco/ont00001765> "Alice"
    ] .
```

<a id="graph-80"></a>
### Graph 80

#### Overview

This graph captures Alice Walker's Social Security Administration record — moved here, as this pod's tool content, from the pod's former `member` graph-23. Alice self-enters her SSN (123-45-6788) from her physical Social Security card. The SSA is not a PDN node, so this data is self-claimed rather than received from the SSA directly. Validated by `shacl/persona-shacl.ttl`'s `:SSNShape` (reused directly as this pod's declared tool's `pod:formShape`, since the SSN designator has no separate document class of its own). Alice is the claimant.

#### Graph

```turtle
<!-- databook:id: alice-ssa-graph -->
<!-- databook:graph: http://www.example.org/tpod/graphs/graph-80#graph -->
@prefix : <http://www.example.org/tpod#> .
@prefix persona: <http://mee.foundation/ontologies/persona#> .
@prefix cco: <https://w3id.org/cco-domains/cco/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

:Self rdf:type owl:NamedIndividual ,
               persona:Person .

:Self rdfs:comment "Alice Walker's persona for her Social Security Administration record."@en ;

    <https://w3id.org/cco-domains/cco/ont00001879> [  # designated by → SSN
        rdf:type cco:ent00000008 ;
        <https://w3id.org/cco-domains/cco/ont00001765> "123-45-6788"
    ] .
```
