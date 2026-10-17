---
id: http://www.example.org/tpod/pods/pod-24
title: "Banking & Payments Firms"
type: pod-databook
version: 1.3.0
created: 2026-07-10
description: >
  Pod DataBook for folder "Banking & Payments Firms" (pod:category: podcat:BankingPayments). It is a
  one-member pod with one member entry about :Self — a minimal stub,
  since "Banking & Payments Firms" is a purely organizational category node with no
  content or relationship of its own beyond Alice's required membership.
  Also carries an empty tool graph, since podcat:BankingPayments's own TemplatePod
  declares a form tool — the real content
  lives in this category's own leaf pod (Citibank) instead.
tpod:
  category: "podcat:BankingPayments"
  creator: ":Self"
  owner: ":Self"
  member:
    id: "http://www.example.org/tpod/graphs/graph-42"
    claimant: ":Self"
    subject: ":Self"
    shape: "pshapes:ContactInfoShape"
  tool:
    - id: "http://www.example.org/tpod/tools/tool-09"
      type: "form"
      formTopic: ":Self"
      graph:
        - id: "http://www.example.org/tpod/graphs/graph-86"
          claimant: ":Self"
---

## Graphs

<a id="graph-42"></a>
### Graph 42

#### Overview

This graph is the pod's one required `member` entry — a pod with a single `member` entry in the user's own category-pod tree always has `:Self` as that member (see YAML-6), regardless of what the pod's `subject` is — here, Alice herself. The "Banking & Payments Firms" pod is a purely organizational category node (`pod:category: podcat:BankingPayments`) with no relationship or subject of its own beyond Alice's required membership. Alice is both the claimant and the subject. It carries her given name, satisfying the `ContactInfoShape` `ctpl:BankingPaymentsTemplatePod` sets as `pod:memberShape` — no longer deliberately empty.

#### Graph

```turtle
<!-- databook:id: alice-banking-payments-member-graph -->
<!-- databook:graph: http://www.example.org/tpod/graphs/graph-42#graph -->
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

<a id="graph-86"></a>
### Graph 86

#### Overview

This graph is the pod's required tool graph — required since `podcat:BankingPayments`'s own `TemplatePod` declares a form tool, even though "Banking & Payments Firms" is a purely organizational scaffold pod with no tool content of its own (the real content lives in this category's own leaf pod, Citibank, instead). Deliberately empty — no triples at all. Alice is both the claimant and the subject.

#### Graph

```turtle
<!-- databook:id: alice-banking-payments-tool-graph -->
<!-- databook:graph: http://www.example.org/tpod/graphs/graph-86#graph -->
```
