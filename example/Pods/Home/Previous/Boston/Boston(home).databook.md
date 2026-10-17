---
id: http://www.example.org/tpod/pods/pod-07
title: "Boston"
type: pod-databook
version: 2.0.0
created: 2026-07-10
description: >
  Pod DataBook for folder "Boston" (pod:category: podcat:Home). It is a one-member pod with one
  member entry about :Self and one tool graph about :Self (the pod's subject), typed
  residences:Residence, carrying Alice's previous Boston address.
tpod:
  category: "podcat:Home"
  creator: ":Self"
  owner: ":Self"
  member:
    id: "http://www.example.org/tpod/graphs/graph-13"
    claimant: ":Self"
    subject: ":Self"
    shape: "pshapes:ContactInfoShape"
  tool:
    - id: "http://www.example.org/tpod/tools/tool-20"
      type: "form"
      formTopic: ":Self"
      graph:
        - id: "http://www.example.org/tpod/graphs/graph-82"
          claimant: ":Self"
          shape: "residenceshapes:ResidenceShape"
---

## Graphs

<a id="graph-13"></a>
### Graph 13

#### Overview

This graph is the pod's one required `member` entry — a pod with a single `member` entry in the user's own category-pod tree always has `:Self` as that member (see YAML-6). Alice is both the claimant and the subject. It carries her given name, satisfying the `ContactInfoShape` every templated pod's `member` content is now expected to conform to (`pod:memberShape`) — no longer the address content, which now lives in this pod's tool graph instead (graph 82).

#### Graph

```turtle
<!-- databook:id: alice-boston-member-graph -->
<!-- databook:graph: http://www.example.org/tpod/graphs/graph-13#graph -->
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

<a id="graph-82"></a>
### Graph 82

#### Overview

This graph captures Alice Walker's previous residential address: 456 Commonwealth Ave, Boston, MA 02215 — moved here, as this pod's tool content, from the pod's former `member` graph-13. The address designation spans January 2020 to August 2025. See graph 83 for her current address. Validated by the `ResidenceShape` per-template SHACL shape. Alice is the claimant.

#### Graph

```turtle
<!-- databook:id: alice-boston-graph -->
<!-- databook:graph: http://www.example.org/tpod/graphs/graph-82#graph -->
@prefix : <http://www.example.org/tpod#> .
@prefix persona: <http://mee.foundation/ontologies/persona#> .
@prefix cco: <https://w3id.org/cco-domains/cco/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix residences: <http://mee.foundation/ontologies/residences#> .

:Self rdf:type owl:NamedIndividual ,
               persona:Person .

:Boston_Residence rdf:type owl:NamedIndividual ,
                           residences:Residence ,
                           cco:ent00000016 ;  # AddressDesignation
    rdfs:label "Alice's Boston Residence (2020-2025)"@en ;
    rdfs:comment "Alice lived at this Boston address from 2020 to 2025."@en ;
    <http://purl.obolibrary.org/obo/BFO_0000057> :Self ;  # has participant
    <https://w3id.org/cco-domains/domains/AddressOntology#ent00000324> :Address_Boston ;  # has address
    <http://purl.obolibrary.org/obo/BFO_0000199> :Interval_2020_2025 .   # occupies temporal region

:Interval_2020_2025 rdf:type owl:NamedIndividual ,
                             <http://purl.obolibrary.org/obo/BFO_0000038> ;  # TemporalInterval
    rdfs:label "2020-2025"@en ;
    cco:ent00000017 "2020-01-01"^^xsd:date ;
    cco:ent00000018 "2025-08-31"^^xsd:date .

:Address_Boston rdf:type owl:NamedIndividual ,
                         cco:ent00000010 ;  # USPostalAddress
    rdfs:label "Boston Address"@en ;
    <http://purl.obolibrary.org/obo/BFO_0000178> [  # has continuant part → Street
        rdf:type cco:ent00000011 ;
        <https://w3id.org/cco-domains/cco/ont00001765> "456 Commonwealth Ave"
    ] ;
    <http://purl.obolibrary.org/obo/BFO_0000178> [  # has continuant part → City
        rdf:type cco:ent00000012 ;
        <https://w3id.org/cco-domains/cco/ont00001765> "Boston"
    ] ;
    <http://purl.obolibrary.org/obo/BFO_0000178> [  # has continuant part → State
        rdf:type cco:ent00000013 ;
        <https://w3id.org/cco-domains/cco/ont00001765> "MA"
    ] ;
    <http://purl.obolibrary.org/obo/BFO_0000178> [  # has continuant part → ZIP
        rdf:type cco:ent00000015 ;
        <https://w3id.org/cco-domains/cco/ont00001765> "02215"
    ] .
```
