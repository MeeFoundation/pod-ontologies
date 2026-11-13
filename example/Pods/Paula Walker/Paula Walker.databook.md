---
id: http://www.example.org/tpod/pods/pod-19
title: "Paula Walker"
type: pod-databook
version: 1.5.0
created: 2026-07-10
description: >
  Pod DataBook for the "Paula Walker" pod (category tags: podcat:Employees, podcat:ImmediateFamily; user tag: "Acme"). Paula is both Alice's Acme colleague and her mother, so Alice gives the pod two category tags — the example's multi-tag case. Since podcat:Employees reaches the podcat:Organization top concept and podcat:ImmediateFamily reaches podcat:Person, a search for either podcat:Person or podcat:Organization finds the pod, and its type is Mixed. It is a two-member pod with member entries about :Self and :Paula_Walker.
tpod:
  categoryTag:
    - "podcat:Employees"
    - "podcat:ImmediateFamily"
  creator: ":Self"
  owner: ":Self"
  userTag:
    - "Acme"
  member:
    - id: "http://www.example.org/tpod/graphs/graph-20"
      claimant: ":Self"
      subject: ":Self"
      shape: "pshapes:ContactInfoShape"
    - id: "http://www.example.org/tpod/graphs/graph-06"
      claimant: ":Self"
      subject: ":Paula_Walker"
      shape: "pshapes:ContactInfoShape"
---

## Graphs

<a id="graph-06"></a>
### Graph 06

#### Overview

This graph captures Alice's record of Paula Walker, her Acme colleague and her mother — one of the pod's two required `member` entries, satisfying `ContactInfoShape`'s required GivenName alongside her existing `rdfs:label` (neither of this pod's category tags has a template that declares a tool, so its content belongs in the member graph). Alice is the claimant.

#### Graph

```turtle
<!-- databook:id: paula-acme-graph -->
<!-- databook:graph: http://www.example.org/tpod/graphs/graph-06#graph -->
@prefix : <http://www.example.org/tpod#> .
@prefix persona: <http://mee.foundation/ontologies/persona#> .
@prefix cco: <https://w3id.org/cco-domains/cco/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

:Self rdf:type owl:NamedIndividual ,
               persona:Person .

:Paula_Walker rdf:type owl:NamedIndividual ,
               persona:Person ;
    rdfs:label "Paula Walker (Acme)"@en ;

    <https://w3id.org/cco-domains/cco/ont00001879> [  # designated by → GivenName (ContactInfoShape)
        rdf:type cco:ent00000002 ;
        <https://w3id.org/cco-domains/cco/ont00001765> "Paula"
    ] ;

    cco:ont00001786 :Self .  # is mother of
```

<a id="graph-20"></a>
### Graph 20

#### Overview

This graph captures Alice Walker's employee identity at Acme. It records her work email address (alice@acme.com) and her Acme social network, which includes colleague Paula Walker. Alice is the claimant.

#### Graph

```turtle
<!-- databook:id: alice-acme-graph -->
<!-- databook:graph: http://www.example.org/tpod/graphs/graph-20#graph -->
@prefix : <http://www.example.org/tpod#> .
@prefix persona: <http://mee.foundation/ontologies/persona#> .
@prefix cco: <https://w3id.org/cco-domains/cco/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

:Self rdf:type owl:NamedIndividual ,
               persona:Person .

:Paula_Walker rdf:type owl:NamedIndividual ,
               persona:Person .

:Self rdfs:comment "Alice Walker's persona for her employment at Acme."@en ;

    <https://w3id.org/cco-domains/cco/ont00001879> [  # designated by → GivenName (ContactInfoShape)
        rdf:type cco:ent00000002 ;
        <https://w3id.org/cco-domains/cco/ont00001765> "Alice"
    ] ;

    <https://w3id.org/cco-domains/cco/ont00001879> [  # designated by → AlternateName
        rdf:type cco:ent00000006 ;  # AlternateName
        <https://w3id.org/cco-domains/cco/ont00001765> "Alice Walker"
    ] ;

    <https://w3id.org/cco-domains/cco/ont00001879> [  # designated by → Email
        rdf:type cco:ent00000024 ;  # Email
        <https://w3id.org/cco-domains/cco/ont00001765> "alice@acme.com"  # has text value
    ] ;

    persona:hasSocialNetwork :Alice_Acme_Network .


:Alice_Acme_Network rdf:type owl:NamedIndividual ,
                             cco:ont00001183 ;  # Social Network
    rdfs:label "Alice Walker's Acme connections"@en ;
    <http://purl.obolibrary.org/obo/BFO_0000115> :Paula_Walker .  # has member part
```
