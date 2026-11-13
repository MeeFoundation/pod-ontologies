---
id: http://www.example.org/tpod/pods/pod-11
title: "Things"
type: pod-databook
version: 1.2.0
created: 2026-07-10
description: >
  Pod DataBook for the "Things" pod (category tag: podcat:Things). It is a one-member pod with one member entry about :Self.
tpod:
  categoryTag:
    - "podcat:Things"
  creator: ":Self"
  owner: ":Self"
  member:
    id: "http://www.example.org/tpod/graphs/graph-22"
    claimant: ":Self"
    subject: ":Self"
    shape: "pshapes:ContactInfoShape"
---

## Graphs

<a id="graph-22"></a>
### Graph 22

#### Overview

This graph captures Alice Walker's day-to-day physical possessions. Her wallet holds her driver's license and payment card. Her health insurance card is carried separately (not in the wallet). Her Social Security card is stored at home for safety. Alice is the claimant.

#### Graph

```turtle
<!-- databook:id: alice-possessions-graph -->
<!-- databook:graph: http://www.example.org/tpod/graphs/graph-22#graph -->
@prefix : <http://www.example.org/tpod#> .
@prefix persona: <http://mee.foundation/ontologies/persona#> .
@prefix cco: <https://w3id.org/cco-domains/cco/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

:Self rdf:type owl:NamedIndividual ,
               persona:Person .

:Self <https://w3id.org/cco-domains/cco/ont00001879> [  # designated by → GivenName (ContactInfoShape)
        rdf:type cco:ent00000002 ;
        <https://w3id.org/cco-domains/cco/ont00001765> "Alice"
    ] ;

    persona:hasWallet :Alice_Wallet ;
    persona:hasPhysicalCard :Alice_HealthInsuranceCard ;   # not in wallet — carried separately
    persona:hasPhysicalCard :Alice_SSNCard ;               # not in wallet — stored at home for safety
    persona:hasPhysicalCard :Alice_DriversLicense ;        # in wallet
    persona:hasPhysicalCard :Alice_PaymentCard .           # in wallet


:Alice_Wallet rdf:type owl:NamedIndividual ,
                        persona:Wallet ;
    rdfs:label "Alice Walker's Wallet"@en .


:Alice_DriversLicense rdf:type owl:NamedIndividual ,
                               persona:PhysicalDriversLicense ;
    rdfs:label "Alice Walker's Driver's License"@en ;
    rdfs:comment "Alice Walker's physical Texas driver's license card."@en ;
    <http://purl.obolibrary.org/obo/BFO_0000176> :Alice_Wallet ;            # continuant part of → in wallet
    persona:hasImageScan "file:///scans/alice-drivers-license.png"^^xsd:anyURI .


:Alice_PaymentCard rdf:type owl:NamedIndividual ,
                            persona:PhysicalPaymentCard ;
    rdfs:label "Alice Walker's Payment Card"@en ;
    rdfs:comment "Alice Walker's physical debit card."@en ;
    <http://purl.obolibrary.org/obo/BFO_0000176> :Alice_Wallet .            # continuant part of → in wallet


:Alice_HealthInsuranceCard rdf:type owl:NamedIndividual ,
                                    persona:PhysicalHealthInsuranceCard ;
    rdfs:label "Alice Walker's Health Insurance Card"@en ;
    rdfs:comment "Alice Walker's physical health insurance membership card."@en ;
    persona:hasImageScan "file:///scans/alice-health-insurance-card.png"^^xsd:anyURI .


:Alice_SSNCard rdf:type owl:NamedIndividual ,
                        persona:PhysicalSocialSecurityCard ;
    rdfs:label "Alice Walker's Social Security Card"@en ;
    rdfs:comment "Alice Walker's Social Security card — stored at home, not carried in wallet."@en .
```
