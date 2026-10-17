---
id: http://www.example.org/tpod/pods/pod-43
title: "Vehicles"
type: pod-databook
version: 1.1.0
created: 2026-08-29
description: >
  Pod DataBook for folder "Vehicles" (pod:category: podcat:Vehicles), nested under "Things". It is a
  one-member pod with one member entry about :Self — a minimal stub, since "Vehicles" is a purely
  organizational category node with no content or relationship of its own beyond Alice's required
  membership. Also carries an empty tool graph, since podcat:Vehicles's own TemplatePod
  declares a form tool — the real content lives in this category's own leaf pod
  (RAV4) instead.
tpod:
  category: "podcat:Vehicles"
  creator: ":Self"
  owner: ":Self"
  member:
    id: "http://www.example.org/tpod/graphs/graph-61"
    claimant: ":Self"
    subject: ":Self"
    shape: "pshapes:ContactInfoShape"
  tool:
    - id: "http://www.example.org/tpod/tools/tool-30"
      type: "form"
      formTopic: ":Self"
      graph:
        - id: "http://www.example.org/tpod/graphs/graph-89"
          claimant: ":Self"
---

## Graphs

<a id="graph-61"></a>
### Graph 61

#### Overview

This graph is the pod's one required `member` entry — a pod with a single `member` entry in the user's own category-pod tree always has `:Self` as that member (see YAML-6), regardless of what the pod's `subject` is — here, Alice herself. The "Vehicles" pod is a purely organizational category node (`pod:category: podcat:Vehicles`) with no relationship or subject of its own beyond Alice's required membership. Alice is both the claimant and the subject. It carries her given name, satisfying the `ContactInfoShape` `ctpl:VehicleProfileTemplatePod` sets as `pod:memberShape` — no longer deliberately empty.

#### Graph

```turtle
<!-- databook:id: alice-vehicles-member-graph -->
<!-- databook:graph: http://www.example.org/tpod/graphs/graph-61#graph -->
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

<a id="graph-89"></a>
### Graph 89

#### Overview

This graph is the pod's required tool graph — required since `podcat:Vehicles`'s own `TemplatePod` declares a form tool, even though "Vehicles" is a purely organizational scaffold pod with no tool content of its own (the real content lives in this category's own leaf pod, RAV4, instead). Deliberately empty — no triples at all. Alice is both the claimant and the subject.

#### Graph

```turtle
<!-- databook:id: alice-vehicles-tool-graph -->
<!-- databook:graph: http://www.example.org/tpod/graphs/graph-89#graph -->
```
