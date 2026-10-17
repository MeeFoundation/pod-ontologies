---
id: http://www.example.org/tpod/pods/pod-12
title: "Sophia Walker"
type: pod-databook
version: 2.0.0
created: 2026-07-10
description: >
  Pod DataBook for folder "Sophia Walker" (pod:category: podcat:ImmediateFamily). It is a two-member pod — Alice (:Self) and her husband Dave — that also carries a form tool about :Sophia_Walker, Alice's daughter. Sophia has no instance of the app, so she is the pod's subject rather than one of its members: Alice added the tool manually and chose the Contact Info template (pshapes:ContactInfoShape) for it, even though podcat:ImmediateFamily's own template pod declares no tool.
tpod:
  category: "podcat:ImmediateFamily"
  creator: ":Self"
  owner: ":Self"
  member:
    - id: "http://www.example.org/tpod/graphs/graph-21"
      claimant: ":Self"
      subject: ":Self"
      shape: "pshapes:ContactInfoShape"
    - id: "http://www.example.org/tpod/graphs/graph-05"
      claimant: ":Dave"
      subject: ":Dave"
      shape: "pshapes:ContactInfoShape"
  tool:
    - id: "http://www.example.org/tpod/tools/tool-24"
      type: "form"
      formTopic: ":Sophia_Walker"
      graph:
        - id: "http://www.example.org/tpod/graphs/graph-07"
          claimant: ":Self"
          shape: "pshapes:ContactInfoShape"
---

## Graphs

<a id="graph-05"></a>
### Graph 05

#### Overview

This graph captures Dave's self-claimed family persona as transmitted from Dave's own instance of the app to Alice's over the PDN, plus his given name, required by the `ContactInfoShape` every templated pod's `member` content is now expected to conform to (`pod:memberShape`). Dave is the claimant — this is the pod's second `member` entry, alongside Alice's own (graph 21), making it a two-member pod.

#### Graph

```turtle
<!-- databook:id: dave-family-dave-graph -->
<!-- databook:graph: http://www.example.org/tpod/graphs/graph-05#graph -->
@prefix : <http://www.example.org/tpod#> .
@prefix persona: <http://mee.foundation/ontologies/persona#> .
@prefix cco: <https://w3id.org/cco-domains/cco/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

:Dave rdf:type owl:NamedIndividual ,
               persona:Person ;
    rdfs:label "Dave (Family) self-claimed"@en ;

    <https://w3id.org/cco-domains/cco/ont00001879> [  # designated by → GivenName (ContactInfoShape)
        rdf:type cco:ent00000002 ;
        <https://w3id.org/cco-domains/cco/ont00001765> "Dave"
    ] .
```

<a id="graph-07"></a>
### Graph 07

#### Overview

This graph captures Alice's Contact Info record of her daughter Sophia Walker. Sophia has no instance of the app, so she cannot join this pod as a member: Alice added this graph manually, in a form tool she added herself, and chose the Contact Info template (`pshapes:ContactInfoShape`) for it, which is what gives an otherwise ordinary `podcat:ImmediateFamily` pod a tool of its own. Sophia is therefore the pod's derived subject rather than one of its two members. Alice is the claimant.

#### Graph

```turtle
<!-- databook:id: sophia-family-alice-graph -->
<!-- databook:graph: http://www.example.org/tpod/graphs/graph-07#graph -->
@prefix : <http://www.example.org/tpod#> .
@prefix persona: <http://mee.foundation/ontologies/persona#> .
@prefix cco: <https://w3id.org/cco-domains/cco/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

:Sophia_Walker rdf:type owl:NamedIndividual ,
               persona:Person ;
    rdfs:label "Sophia Walker (Family)"@en ;

    <https://w3id.org/cco-domains/cco/ont00001879> [  # designated by → GivenName
        rdf:type cco:ent00000002 ;  # GivenName
        <https://w3id.org/cco-domains/cco/ont00001765> "Sophia"  # has text value
    ] ;

    <https://w3id.org/cco-domains/cco/ont00001879> [  # designated by → FamilyName
        rdf:type cco:ent00000004 ;  # FamilyName
        <https://w3id.org/cco-domains/cco/ont00001765> "Walker"  # has text value
    ] .
```

<a id="graph-21"></a>
### Graph 21

#### Overview

This graph captures Alice Walker's family relationships. It records that Sophia Walker is her daughter and her family social network, which includes Sophia Walker and Dave (Alice's husband) as members, plus her own given name, required by the `ContactInfoShape` every templated pod's `member` content is now expected to conform to (`pod:memberShape`). Dave's own family graph (`graph-05`) is the peer record in this relationship; his own claimed record about their daughter appears separately in the "Medical Appointment" pod (graph 28). Alice is the claimant.

#### Graph

```turtle
<!-- databook:id: alice-family-graph -->
<!-- databook:graph: http://www.example.org/tpod/graphs/graph-21#graph -->
@prefix : <http://www.example.org/tpod#> .
@prefix persona: <http://mee.foundation/ontologies/persona#> .
@prefix cco: <https://w3id.org/cco-domains/cco/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

:Self rdf:type owl:NamedIndividual ,
               persona:Person .

:Sophia_Walker rdf:type owl:NamedIndividual ,
               persona:Person .

:Dave rdf:type owl:NamedIndividual ,
               persona:Person .

:Self rdfs:comment "Alice Walker's persona for her family relationships."@en ;

    <https://w3id.org/cco-domains/cco/ont00001879> [  # designated by → GivenName (ContactInfoShape)
        rdf:type cco:ent00000002 ;
        <https://w3id.org/cco-domains/cco/ont00001765> "Alice"
    ] ;

    <https://w3id.org/cco-domains/cco/ont00001879> [  # designated by → AlternateName
        rdf:type cco:ent00000006 ;  # AlternateName
        <https://w3id.org/cco-domains/cco/ont00001765> "Alice Walker"
    ] ;

    cco:ont00001987 :Sophia_Walker ;  # has daughter

    persona:hasSocialNetwork :Alice_Family_Network .


:Alice_Family_Network rdf:type owl:NamedIndividual ,
                               cco:ont00001183 ;  # Social Network
    rdfs:label "Alice Walker's family connections"@en ;
    <http://purl.obolibrary.org/obo/BFO_0000115> :Sophia_Walker ,  # has member part
                                                  :Dave .  # has member part (Alice's husband)
```
