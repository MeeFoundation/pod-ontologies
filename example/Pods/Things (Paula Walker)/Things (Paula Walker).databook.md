---
id: http://www.example.org/tpod/pods/pod-55
title: "Things"
type: pod-databook
version: 1.0.0
created: 2026-11-16
description: >
  Pod DataBook for the "Things" pod (category tag: podcat:Things) in Alice's pod space for Paula. Its name and its podcat:Things tag mean Paula's things rather than Alice's own, which are in the other "Things" pod, in her default space; the space is what tells the two apart. Its folder carries the space name as a suffix only because two folders cannot share a name (pod-databook.md's Filename Convention). It is a one-member pod with one member entry about :Self, plus a form tool about :Paula_Walker that Alice added with the Contact Info form, since podcat:Things' own template pod declares no tool.
tpod:
  categoryTag:
    - "podcat:Things"
  space:
    id: "http://www.example.org/tpod/spaces/space-2"
    name: "Paula Walker"
    root: "podcat:Person"
    subject: ":Paula_Walker"
  creator: ":Self"
  owner: ":Self"
  member:
    id: "http://www.example.org/tpod/graphs/graph-107"
    claimant: ":Self"
    subject: ":Self"
    shape: "pshapes:ContactInfoShape"
  tool:
    - id: "http://www.example.org/tpod/tools/tool-37"
      type: "form"
      formTopic: ":Paula_Walker"
      graph:
        - id: "http://www.example.org/tpod/graphs/graph-108"
          claimant: ":Self"
          shape: "pshapes:ContactInfoShape"
---

## Graphs

<a id="graph-107"></a>
### Graph 107

#### Overview

This graph is the pod's required `member` entry, claimed by and about Alice: her given name, which `ContactInfoShape`, the `podcat:Things` template's member shape, requires. Paula has no instance of the app and is not a member of the pod, so this stub is the only member entry.

#### Graph

```turtle
<!-- databook:id: paula-things-member-graph -->
<!-- databook:graph: http://www.example.org/tpod/graphs/graph-107#graph -->
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

<a id="graph-108"></a>
### Graph 108

#### Overview

This graph captures Alice's record of her mother Paula's day-to-day possessions: her wallet, with her driver's license and debit card in it. It mirrors the possessions pattern of the Things pod's graph 22, with `:Paula_Walker` in place of `:Self`, which is what the pod's space makes plain at the pod level: these are Paula's things. The graph also carries Paula's given name, which the Contact Info form Alice chose requires. Alice is the claimant.

#### Graph

```turtle
<!-- databook:id: paula-things-graph -->
<!-- databook:graph: http://www.example.org/tpod/graphs/graph-108#graph -->
@prefix : <http://www.example.org/tpod#> .
@prefix persona: <http://mee.foundation/ontologies/persona#> .
@prefix cco: <https://w3id.org/cco-domains/cco/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

:Paula_Walker rdf:type owl:NamedIndividual ,
                       persona:Person ;

    <https://w3id.org/cco-domains/cco/ont00001879> [  # designated by → GivenName (ContactInfoShape)
        rdf:type cco:ent00000002 ;
        <https://w3id.org/cco-domains/cco/ont00001765> "Paula"
    ] ;

    persona:hasWallet :Paula_Wallet ;
    persona:hasPhysicalCard :Paula_DriversLicense ;   # in wallet
    persona:hasPhysicalCard :Paula_PaymentCard .      # in wallet


:Paula_Wallet rdf:type owl:NamedIndividual ,
                       persona:Wallet ;
    rdfs:label "Paula Walker's Wallet"@en .


:Paula_DriversLicense rdf:type owl:NamedIndividual ,
                               persona:PhysicalDriversLicense ;
    rdfs:label "Paula Walker's Driver's License"@en ;
    <http://purl.obolibrary.org/obo/BFO_0000176> :Paula_Wallet .            # continuant part of → in wallet


:Paula_PaymentCard rdf:type owl:NamedIndividual ,
                            persona:PhysicalPaymentCard ;
    rdfs:label "Paula Walker's Payment Card"@en ;
    rdfs:comment "Paula Walker's physical debit card."@en ;
    <http://purl.obolibrary.org/obo/BFO_0000176> :Paula_Wallet .            # continuant part of → in wallet
```
