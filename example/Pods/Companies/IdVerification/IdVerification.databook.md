---
id: http://www.example.org/tpod/pods/pod-55
title: "IdVerification"
type: pod-databook
version: 1.1.0
created: 2026-09-26
description: >
  Pod DataBook for folder "IdVerification" (pod:category: podcat:IdVerification), nested under
  "Companies". It is a one-member pod with one member entry about :Self — a minimal stub, since
  "IdVerification" is a purely organizational category node with no content or relationship of
  its own beyond Alice's required membership; its real content lives in its own leaf pod (PRIVO).
  Also carries the pod:Browser tool podcat:IdVerification's own TemplatePod declares, which, being
  a browser rather than a form, holds no graph at all, so there is no empty tool graph to carry.
tpod:
  category: "podcat:IdVerification"
  creator: ":Self"
  owner: ":Self"
  member:
    - id: "http://www.example.org/tpod/graphs/graph-107"
      claimant: ":Self"
      subject: ":Self"
      shape: "pshapes:ContactInfoShape"
  tool:
    - id: "http://www.example.org/tpod/tools/tool-07"
      type: "browser"
---

## Graphs

<a id="graph-107"></a>
### Graph 107

#### Overview

This graph is the pod's one required `member` entry — a pod with a single `member` entry in the user's own tree always has `:Self` as that member (see YAML-6). The "IdVerification" pod is a purely organizational category node (`pod:category: podcat:IdVerification`) with no relationship or subject of its own beyond Alice's required membership. Alice is both the claimant and the subject. It carries her given name, satisfying the `ContactInfoShape` `ctpl:IdVerificationTemplatePod` sets as `pod:memberShape`.

#### Graph

```turtle
<!-- databook:id: alice-idverification-member-graph -->
<!-- databook:graph: http://www.example.org/tpod/graphs/graph-107#graph -->
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
