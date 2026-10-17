---
id: http://www.example.org/tpod/pods/pod-09
title: "Drivers License"
type: pod-databook
version: 2.0.0
created: 2026-07-10
description: >
  Pod DataBook for folder "Drivers License" (pod:category: podcat:DriversLicense). It is a
  one-member pod with one member entry about :Self and one tool graph about :Self (the pod's
  subject), typed identitydocuments:DriversLicense, carrying Alice's California driver's license
  identity data.
tpod:
  category: "podcat:DriversLicense"
  creator: ":Self"
  owner: ":Self"
  member:
    id: "http://www.example.org/tpod/graphs/graph-15"
    claimant: ":Self"
    subject: ":Self"
    shape: "pshapes:ContactInfoShape"
  tool:
    - id: "http://www.example.org/tpod/tools/tool-14"
      type: "form"
      formTopic: ":Self"
      graph:
        - id: "http://www.example.org/tpod/graphs/graph-79"
          claimant: ":Self"
          shape: "idocshapes:DriversLicenseShape"
---

## Graphs

<a id="graph-15"></a>
### Graph 15

#### Overview

This graph is the pod's one required `member` entry — a pod with a single `member` entry in the user's own category-pod tree always has `:Self` as that member (see YAML-6). Alice is both the claimant and the subject. It carries her given name, satisfying the `ContactInfoShape` every templated pod's `member` content is now expected to conform to (`pod:memberShape`) — no longer the driver's license document content, which now lives in this pod's tool graph instead (graph 79).

#### Graph

```turtle
<!-- databook:id: alice-drivers-license-member-graph -->
<!-- databook:graph: http://www.example.org/tpod/graphs/graph-15#graph -->
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

<a id="graph-79"></a>
### Graph 79

#### Overview

This graph captures Alice Walker's California driver's license identity data — moved here, as this pod's tool content, from the pod's former `member` graph-15. Alice self-enters her legal name (Margery Alice Walker), date of birth (1985-07-04), California license number (A1234567), expiration date (2031-07-04), issuing jurisdiction (CA), and a photo. Validated by the `DriversLicenseShape` per-template SHACL shape (`other/shacl/identity-documents-shacl.ttl`). Alice is the claimant.

#### Graph

```turtle
<!-- databook:id: alice-driverslicense-graph -->
<!-- databook:graph: http://www.example.org/tpod/graphs/graph-79#graph -->
@prefix : <http://www.example.org/tpod#> .
@prefix persona: <http://mee.foundation/ontologies/persona#> .
@prefix identitydocuments: <http://mee.foundation/ontologies/identity-documents#> .
@prefix cco: <https://w3id.org/cco-domains/cco/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

:Self rdf:type owl:NamedIndividual ,
               persona:Person .

:Self persona:hasIdentityDocument :Alice_CA_DriversLicense ;
    <https://w3id.org/cco-domains/cco/ont00001879> :Alice_DL_Number .  # Person designated by → Drivers License Number

:Alice_CA_DriversLicense rdf:type owl:NamedIndividual ,
                                   identitydocuments:DriversLicense ;
    rdfs:label "Alice Walker's California Driver's License"@en ;
    rdfs:comment "Alice Walker's California state-issued driver's licence identity data."@en ;

    # ── Legal name (matches Texas Birth Certificate) ─────────────────────────

    <https://w3id.org/cco-domains/cco/ont00001879> [  # designated by → GivenName (legal first name)
        rdf:type cco:ent00000002 ;  # GivenName
        <https://w3id.org/cco-domains/cco/ont00001765> "Margery"
    ] ;

    <https://w3id.org/cco-domains/cco/ont00001879> [  # designated by → AdditionalName (middle name)
        rdf:type cco:ent00000003 ;  # AdditionalName
        <https://w3id.org/cco-domains/cco/ont00001765> "Alice"
    ] ;

    <https://w3id.org/cco-domains/cco/ont00001879> [  # designated by → FamilyName
        rdf:type cco:ent00000004 ;  # FamilyName
        <https://w3id.org/cco-domains/cco/ont00001765> "Walker"
    ] ;

    # ── Dates ────────────────────────────────────────────────────────────────

    <https://w3id.org/cco-domains/cco/ont00001879> [  # designated by → Birthdate
        rdf:type cco:ent00000046 ;  # Birthdate
        <https://w3id.org/cco-domains/cco/ont00001765> "1985-07-04"^^xsd:date
    ] ;

    cco:ent00000070 [  # has expiration date → Calendar Date Identifier
        rdf:type cco:ont00001340 ;  # Calendar Date Identifier
        <https://w3id.org/cco-domains/cco/ont00001765> "2031-07-04"^^xsd:date
    ] ;

    # ── License number (two-relation form: Person designated-by, document is-carrier-of) ──

    <http://purl.obolibrary.org/obo/BFO_0000101> :Alice_DL_Number ;  # document is carrier of → Drivers License Number

    # ── Issuing jurisdiction ─────────────────────────────────────────────────

    <https://w3id.org/cco-domains/cco/ont00001879> [  # designated by → Issuing Jurisdiction
        rdf:type cco:ent00000068 ;
        <https://w3id.org/cco-domains/cco/ont00001765> "CA"
    ] ;

    # ── Photo ────────────────────────────────────────────────────────────────

    persona:hasPhoto "https://example.org/alice-dl-photo.jpg"^^xsd:anyURI .

:Alice_DL_Number rdf:type owl:NamedIndividual ,
                          cco:ent00000065 ;  # Drivers License Number
    rdfs:label "Alice Walker's California Driver's License Number"@en ;
    <https://w3id.org/cco-domains/cco/ont00001765> "A1234567" .  # placeholder California DL number
```
