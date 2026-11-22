---
id: http://www.example.org/tpod/pods/pod-08
title: "Paradise"
type: pod-databook
version: 2.2.0
created: 2026-07-10
description: >
  Pod DataBook for the "Paradise" pod (category tag: podcat:Home). It is a one-member pod with one
  member entry about :Self and two form tools. The first, declared by podcat:Home's template, holds
  one graph about :Self, typed residences:Residence, carrying Alice's current Paradise address. The
  second, added by hand, holds one graph about :Alice_PGE_Account, typed
  serviceaccounts:ServiceAccount, carrying her PG&E utility account. The pod's derived subject is
  both topics together.
tpod:
  categoryTag:
    - "podcat:Home"
  creator: ":Self"
  owner: ":Self"
  member:
    id: "http://www.example.org/tpod/graphs/graph-18"
    claimant: ":Self"
    subject: ":Self"
    shape: "pshapes:ContactInfoShape"
  tool:
    - id: "http://www.example.org/tpod/tools/tool-19"
      type: "form"
      formTopic: ":Self"
      graph:
        - id: "http://www.example.org/tpod/graphs/graph-83"
          claimant: ":Self"
          shape: "residenceshapes:ResidenceShape"
    - id: "http://www.example.org/tpod/tools/tool-40"
      type: "form"
      formTopic: ":Alice_PGE_Account"
      graph:
        - id: "http://www.example.org/tpod/graphs/graph-113"
          claimant: ":Self"
          shape: "sashapes:ServiceAccountShape"
---

## Graphs

<a id="graph-18"></a>
### Graph 18

#### Overview

This graph is the pod's one required `member` entry — a pod with a single `member` entry always has `:Self` as that member (see YAML-6). Alice is both the claimant and the subject. It carries her given name, satisfying the `ContactInfoShape` the pod's category template names as `pod:memberShape`; the address content itself is this pod's tool graph (graph 83).

#### Graph

```turtle
<!-- databook:id: alice-paradise-member-graph -->
<!-- databook:graph: http://www.example.org/tpod/graphs/graph-18#graph -->
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

<a id="graph-83"></a>
### Graph 83

#### Overview

This graph captures Alice Walker's current residential address: 123 Sleepy Hollow, Paradise, CA 95969 — this pod's tool content. The address designation has a start date of September 2025 and no end date, indicating it is her current residence. See graph 82 for her previous address. Validated by the `ResidenceShape` per-template SHACL shape. Alice is the claimant.

#### Graph

```turtle
<!-- databook:id: alice-paradise-graph -->
<!-- databook:graph: http://www.example.org/tpod/graphs/graph-83#graph -->
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

:Paradise_Residence rdf:type owl:NamedIndividual ,
                            residences:Residence ,
                            cco:ent00000016 ;  # AddressDesignation
    rdfs:label "Alice's Paradise Residence (2025-present)"@en ;
    rdfs:comment "Alice has lived at this Paradise address since September 2025. No end date indicates current residence."@en ;
    <http://purl.obolibrary.org/obo/BFO_0000057> :Self ;  # has participant
    <https://w3id.org/cco-domains/domains/AddressOntology#ent00000324> :Address_Paradise ;  # has address
    <http://purl.obolibrary.org/obo/BFO_0000199> :Interval_2025_Present .  # occupies temporal region

:Interval_2025_Present rdf:type owl:NamedIndividual ,
                                <http://purl.obolibrary.org/obo/BFO_0000038> ;  # TemporalInterval
    rdfs:label "September 2025 to present"@en ;
    rdfs:comment "Open-ended interval — absence of end date indicates current/ongoing."@en ;
    cco:ent00000017 "2025-09-01"^^xsd:date .
    # No cco:ent00000018 = still current

:Address_Paradise rdf:type owl:NamedIndividual ,
                          cco:ent00000010 ;  # USPostalAddress
    rdfs:label "Paradise Address"@en ;
    <http://purl.obolibrary.org/obo/BFO_0000178> [  # has continuant part → Street
        rdf:type cco:ent00000011 ;
        <https://w3id.org/cco-domains/cco/ont00001765> "123 Sleepy Hollow"
    ] ;
    <http://purl.obolibrary.org/obo/BFO_0000178> [  # has continuant part → City
        rdf:type cco:ent00000012 ;
        <https://w3id.org/cco-domains/cco/ont00001765> "Paradise"
    ] ;
    <http://purl.obolibrary.org/obo/BFO_0000178> [  # has continuant part → State
        rdf:type cco:ent00000013 ;
        <https://w3id.org/cco-domains/cco/ont00001765> "CA"
    ] ;
    <http://purl.obolibrary.org/obo/BFO_0000178> [  # has continuant part → ZIP
        rdf:type cco:ent00000015 ;
        <https://w3id.org/cco-domains/cco/ont00001765> "95969"
    ] ;
    <http://purl.obolibrary.org/obo/BFO_0000178> [  # has continuant part → Country
        rdf:type cco:ent00000014 ;
        <https://w3id.org/cco-domains/cco/ont00001765> "USA"
    ] .
```

<a id="graph-113"></a>
### Graph 113

#### Overview

This graph captures Alice's account with PG&E, the gas and electric utility serving her Paradise home — this pod's second form tool's content. `podcat:Home`'s template declares only the Residence form (graph 83), so Alice added this one by hand with **Add Tool**, picking the Service Account form type; the app stamped its `pod:shape` as `sashapes:ServiceAccountShape` from her pick. Its tool's `formTopic` is `:Alice_PGE_Account`, so the pod's derived subject is `:Self` and `:Alice_PGE_Account` together (see YAML-4). The account is typed `serviceaccounts:ServiceAccount` and multi-typed `cco:ent00000033` (Online Service Account): service name, username, service URI, and password. `:Self` carries `cco:ent00000045` (holds user account) to it. Alice is the claimant.

#### Graph

```turtle
<!-- databook:id: alice-paradise-utility-graph -->
<!-- databook:graph: http://www.example.org/tpod/graphs/graph-113#graph -->
@prefix : <http://www.example.org/tpod#> .
@prefix persona: <http://mee.foundation/ontologies/persona#> .
@prefix cco: <https://w3id.org/cco-domains/cco/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix serviceaccounts: <http://mee.foundation/ontologies/service-accounts#> .

:Self rdf:type owl:NamedIndividual ,
               persona:Person .

:Alice_PGE_Account rdf:type owl:NamedIndividual ,
                     serviceaccounts:ServiceAccount ,
                     cco:ent00000033 ;
    rdfs:label "Alice Walker's PG&E account"@en ;
    cco:ent00000034 "PG&E" ;                                   # has service name
    cco:ent00000035 "alice.walker.paradise" ;                  # has user handle (username)
    cco:ent00000036 "https://www.pge.com/myaccount/"^^xsd:anyURI ;  # has service URI
    serviceaccounts:hasPassword "Sl33py#Hollow2025" .          # has password

:Self <https://w3id.org/cco-domains/cco/ent00000045> :Alice_PGE_Account .  # holds user account
```
