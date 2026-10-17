---
id: http://www.example.org/tpod/pods/pod-35
title: "Acme"
type: pod-databook
version: 1.2.0
created: 2026-07-10
description: >
  Pod DataBook for folder "Acme" (pod:category: podcat:Organization). It is a
  one-member pod with one member entry about :Self, plus one form tool about
  :Acme itself — Alice's employer's own o:Organization profile, since
  podcat:Organization's own TemplatePod declares that tool.
tpod:
  category: "podcat:Organization"
  creator: ":Self"
  owner: ":Self"
  member:
    id: "http://www.example.org/tpod/graphs/graph-53"
    claimant: ":Self"
    subject: ":Self"
    shape: "pshapes:ContactInfoShape"
  tool:
    - id: "http://www.example.org/tpod/tools/tool-35"
      type: "form"
      formTopic: ":Acme"
      graph:
        - id: "http://www.example.org/tpod/graphs/graph-94"
          claimant: ":Self"
          shape: "oshapes:OrganizationShape"
---

## Graphs

<a id="graph-53"></a>
### Graph 53

#### Overview

This graph is the pod's one required `member` entry — a pod with a single `member` entry in the user's own category-pod tree always has `:Self` as that member (see YAML-6), regardless of what the pod's `subject` is — here, Alice herself. The "Acme" pod's own subject is Alice's employer, carried by its tool graph (graph 94) rather than by this member stub. Alice is both the claimant and the subject. It carries her given name, satisfying the `ContactInfoShape` `ctpl:OrganizationTemplatePod` sets as `pod:memberShape` — no longer deliberately empty.

#### Graph

```turtle
<!-- databook:id: alice-acme-member-graph -->
<!-- databook:graph: http://www.example.org/tpod/graphs/graph-53#graph -->
@prefix : <http://www.example.org/tpod#> .
@prefix cco: <https://w3id.org/cco-domains/cco/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix persona: <http://mee.foundation/ontologies/persona#> .

:Self rdf:type owl:NamedIndividual ,
               persona:Person .

:Self <https://w3id.org/cco-domains/cco/ont00001879> [  # designated by → GivenName
        rdf:type cco:ent00000002 ;
        <https://w3id.org/cco-domains/cco/ont00001765> "Alice"
    ] .
```

<a id="graph-94"></a>
### Graph 94

#### Overview

This graph captures Acme, Alice's employer, as an `o:Organization` in its own right — the pod's
tool graph, and what its derived subject resolves to (see integrity.md's YAML-4). Alice self-enters
this record: Acme is not a PDN-interoperable node, so she is the claimant even though the graph is
about Acme.

#### Graph

```turtle
<!-- databook:id: alice-acme-org-profile-graph -->
<!-- databook:graph: http://www.example.org/tpod/graphs/graph-94#graph -->
@prefix : <http://www.example.org/tpod#> .
@prefix o: <http://mee.foundation/ontologies/organization#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

:Acme rdf:type owl:NamedIndividual ,
               o:Organization ;
    rdfs:label "Acme"@en ;

    o:numMembers 2400 ;
    o:hasWebsite "https://acme.example.com"^^xsd:anyURI .
```
