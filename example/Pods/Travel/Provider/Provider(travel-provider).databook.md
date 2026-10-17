---
id: http://www.example.org/tpod/pods/pod-51
title: "Provider"
type: pod-databook
version: 1.1.0
created: 2026-09-11
description: >
  Pod DataBook for folder "Provider" (pod:category: podcat:TravelProvider). It is a
  one-member pod with one member entry about :Self — a minimal stub, since
  "Provider" is a purely organizational category node with no content or
  relationship of its own beyond Alice's required membership. It also carries the
  tool graph podcat:TravelProvider's own TemplatePod requires,
  deliberately empty, since its real content lives in its own leaf pod (Hilton)
  instead.
tpod:
  category: "podcat:TravelProvider"
  creator: ":Self"
  owner: ":Self"
  member:
    id: "http://www.example.org/tpod/graphs/graph-98"
    claimant: ":Self"
    subject: ":Self"
    shape: "pshapes:ContactInfoShape"
  tool:
    - id: "http://www.example.org/tpod/tools/tool-32"
      type: "form"
      formTopic: ":Self"
      graph:
        - id: "http://www.example.org/tpod/graphs/graph-56"
          claimant: ":Self"
---

## Graphs

<a id="graph-98"></a>
### Graph 98

#### Overview

This graph is the pod's one required `member` entry — a pod with a single `member` entry in the user's own tree of pods always has `:Self` as that member (see YAML-6), regardless of what the pod's subject is. The "Provider" pod is a purely organizational category node (`pod:category: podcat:TravelProvider`) with no relationship or subject of its own beyond Alice's required membership, so this stub carries no further claims. Alice is both the claimant and the subject. It carries her given name, satisfying the `ContactInfoShape` `ctpl:TravelProviderTemplatePod` sets as `pod:memberShape`.

#### Graph

```turtle
<!-- databook:id: alice-travel-provider-member-graph -->
<!-- databook:graph: http://www.example.org/tpod/graphs/graph-98#graph -->
@prefix : <http://www.example.org/tpod#> .
@prefix persona: <http://mee.foundation/ontologies/persona#> .
@prefix cco: <https://w3id.org/cco-domains/cco/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .

:Self rdf:type owl:NamedIndividual ,
               persona:Person .

:Self <https://w3id.org/cco-domains/cco/ont00001879> [  # designated by → GivenName (ContactInfoShape)
        rdf:type cco:ent00000002 ;
        <https://w3id.org/cco-domains/cco/ont00001765> "Alice"
    ] .
```

<a id="graph-56"></a>
### Graph 56

#### Overview

This graph is the pod's required tool graph — required since `podcat:TravelProvider`'s own `TemplatePod` declares a form tool, even though "Provider" is a purely organizational scaffold pod with no tool content of its own (the real content lives in this category's own leaf pod, Hilton, instead). Deliberately empty — no triples at all — and so carries no `template:` value either, the same as every other scaffold pod's empty tool graph. Alice is both the claimant and the subject.

#### Graph

```turtle
<!-- databook:id: alice-travel-provider-tool-graph -->
<!-- databook:graph: http://www.example.org/tpod/graphs/graph-56#graph -->
```
