---
id: http://www.example.org/tpod/pods/pod-37
title: "Pets"
type: pod-databook
version: 1.2.0
created: 2026-08-21
description: >
  Pod DataBook for folder "Pets" (pod:category: podcat:Pets). It is a
  one-member pod with one member entry about :Self — a minimal stub,
  since "Pets" is a purely organizational category node with no
  content or relationship of its own beyond Alice's required membership.
  also carries an empty tool graph, since podcat:Pets's own
  TemplatePod declares a form tool — the real content
  lives in this category's own leaf pod (Ginger) instead.
tpod:
  category: "podcat:Pets"
  creator: ":Self"
  owner: ":Self"
  member:
    id: "http://www.example.org/tpod/graphs/graph-55"
    claimant: ":Self"
    subject: ":Self"
    shape: "pshapes:ContactInfoShape"
  tool:
    - id: "http://www.example.org/tpod/tools/tool-28"
      type: "form"
      formTopic: ":Self"
      graph:
        - id: "http://www.example.org/tpod/graphs/graph-88"
          claimant: ":Self"
---

## Graphs

<a id="graph-55"></a>
### Graph 55

#### Overview

This graph is the pod's one required `member` entry — a pod with a single `member` entry in the user's own category-pod tree always has `:Self` as that member (see YAML-6), regardless of what the pod's `subject` is — here, Alice herself. The "Pets" pod is a purely organizational category node (`pod:category: podcat:Pets`) with no relationship or subject of its own beyond Alice's required membership. Alice is both the claimant and the subject. It carries her given name, satisfying the `ContactInfoShape` `ctpl:PetProfileTemplatePod` sets as `pod:memberShape` — no longer deliberately empty.

#### Graph

```turtle
<!-- databook:id: alice-pets-member-graph -->
<!-- databook:graph: http://www.example.org/tpod/graphs/graph-55#graph -->
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

<a id="graph-88"></a>
### Graph 88

#### Overview

This graph is the pod's required tool graph — required since `podcat:Pets`'s own `TemplatePod` declares a form tool, even though "Pets" is a purely organizational scaffold pod with no tool content of its own (the real content lives in this category's own leaf pod, Ginger, instead). Deliberately empty — no triples at all. Alice is both the claimant and the subject.

#### Graph

```turtle
<!-- databook:id: alice-pets-tool-graph -->
<!-- databook:graph: http://www.example.org/tpod/graphs/graph-88#graph -->
```
