---
id: http://www.example.org/tpod/pods/pod-17
title: "Fred Flintstone"
type: pod-databook
version: 1.4.0
created: 2026-08-03
description: >
  Pod DataBook for the "Fred Flintstone" pod (category tag: podcat:Others). It is a two-member pod with two members about :Fred_Flintstone and :Self.
tpod:
  categoryTag:
    - "podcat:Others"
  creator: ":Self"
  owner: ":Self"
  serviceTag:
    - namespace: "foundation.mee.applecontacts"
      key: "group"
      value: "Christmas List"
  member:
    - id: "http://www.example.org/tpod/graphs/graph-31"
      claimant: ":Fred_Flintstone"
      subject: ":Fred_Flintstone"
      shape: "pshapes:ContactInfoShape"
    - id: "http://www.example.org/tpod/graphs/graph-29"
      claimant: ":Self"
      subject: ":Self"
      shape: "pshapes:ContactInfoShape"
---

## Graphs

<a id="graph-29"></a>
### Graph 29

#### Overview

This graph captures Alice Walker's self-claimed persona in her 1:1 relationship with Fred Flintstone. It records the name Alice presents to Fred and her social network link to him. Alice is the claimant.

#### Graph

```turtle
<!-- databook:id: alice-fred-alice-graph -->
<!-- databook:graph: http://www.example.org/tpod/graphs/graph-29#graph -->
@prefix : <http://www.example.org/tpod#> .
@prefix persona: <http://mee.foundation/ontologies/persona#> .
@prefix cco: <https://w3id.org/cco-domains/cco/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

:Self rdf:type owl:NamedIndividual ,
               persona:Person .

:Self rdfs:comment "Alice Walker's persona for her 1:1 relationship with Fred."@en ;

    <https://w3id.org/cco-domains/cco/ont00001879> [  # designated by → AlternateName
        rdf:type cco:ent00000006 ;  # AlternateName
        <https://w3id.org/cco-domains/cco/ont00001765> "Alice Walker"
    ] ;

    <https://w3id.org/cco-domains/cco/ont00001879> [  # designated by → GivenName
        rdf:type cco:ent00000002 ;  # GivenName
        <https://w3id.org/cco-domains/cco/ont00001765> "Alice"  # has text value
    ] ;

    <https://w3id.org/cco-domains/cco/ont00001879> [  # designated by → FamilyName
        rdf:type cco:ent00000004 ;  # FamilyName
        <https://w3id.org/cco-domains/cco/ont00001765> "Walker"  # has text value
    ] ;

    persona:hasSocialNetwork :Alice_Fred_Network .


:Alice_Fred_Network rdf:type owl:NamedIndividual ,
                             cco:ont00001183 ;  # Social Network
    rdfs:label "Alice Walker's Fred connection"@en ;
    <http://purl.obolibrary.org/obo/BFO_0000115> :Fred_Flintstone .  # has member part
```

<a id="graph-31"></a>
### Graph 31

#### Overview

This graph captures Fred Flintstone's self-claimed persona, transmitted from Fred's own instance of the app to Alice's over the PDN. It records Fred's name and his social network link to Alice. Fred is the claimant.

#### Graph

```turtle
<!-- databook:id: fred-fred-fred-graph -->
<!-- databook:graph: http://www.example.org/tpod/graphs/graph-31#graph -->
@prefix : <http://www.example.org/tpod#> .
@prefix persona: <http://mee.foundation/ontologies/persona#> .
@prefix cco: <https://w3id.org/cco-domains/cco/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

:Fred_Flintstone rdf:type owl:NamedIndividual ,
              persona:Person ;
    rdfs:label "Fred Flintstone"@en ;
    rdfs:comment "Fred Flintstone's self-claimed persona in his 1:1 relationship with Alice."@en ;

    <https://w3id.org/cco-domains/cco/ont00001879> [  # designated by → GivenName
        rdf:type cco:ent00000002 ;  # GivenName
        <https://w3id.org/cco-domains/cco/ont00001765> "Fred"  # has text value
    ] ;

    <https://w3id.org/cco-domains/cco/ont00001879> [  # designated by → FamilyName
        rdf:type cco:ent00000004 ;  # FamilyName
        <https://w3id.org/cco-domains/cco/ont00001765> "Flintstone"  # has text value
    ] ;

    persona:hasSocialNetwork :Fred_Fred_Network .


:Fred_Fred_Network rdf:type owl:NamedIndividual ,
                          cco:ont00001183 ;  # Social Network
    rdfs:label "Fred Flintstone's Alice connection"@en ;
    <http://purl.obolibrary.org/obo/BFO_0000115> :Self .  # has member part → Alice
```
