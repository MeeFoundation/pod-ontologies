---
id: http://www.example.org/tpod/pods/pod-05
title: "Passport"
type: pod-databook
version: 2.0.0
created: 2026-07-10
description: >
  Pod DataBook for folder "Passport" (pod:category: podcat:Passport). It is a one-member pod with
  one member entry about :Self and one tool graph about :Self (the pod's subject), typed
  identitydocuments:Passport, carrying Alice's US passport identity data.
tpod:
  category: "podcat:Passport"
  creator: ":Self"
  owner: ":Self"
  member:
    id: "http://www.example.org/tpod/graphs/graph-19"
    claimant: ":Self"
    subject: ":Self"
    shape: "pshapes:ContactInfoShape"
  tool:
    - id: "http://www.example.org/tpod/tools/tool-11"
      type: "form"
      formTopic: ":Self"
      graph:
        - id: "http://www.example.org/tpod/graphs/graph-81"
          claimant: ":Self"
          shape: "idocshapes:PassportShape"
---

## Graphs

<a id="graph-19"></a>
### Graph 19

#### Overview

This graph is the pod's one required `member` entry — a pod with a single `member` entry in the user's own category-pod tree always has `:Self` as that member (see YAML-6). Alice is both the claimant and the subject. It carries her given name, satisfying the `ContactInfoShape` every templated pod's `member` content is now expected to conform to (`pod:memberShape`) — no longer the passport document content, which now lives in this pod's tool graph instead (graph 81).

#### Graph

```turtle
<!-- databook:id: alice-passport-member-graph -->
<!-- databook:graph: http://www.example.org/tpod/graphs/graph-19#graph -->
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

<a id="graph-81"></a>
### Graph 81

#### Overview

This graph captures Alice Walker's US passport identity data — moved here, as this pod's tool content, from the pod's former `member` graph-19. Alice self-enters her legal name (Margery Alice Walker), date of birth (1985-07-04), US passport number (123456789), issue date (2021-07-04), expiration date (2031-07-04), place of birth (Austin, Texas, USA), gender marker (F), and a photo. Validated by the `PassportShape` per-template SHACL shape (`other/shacl/identity-documents-shacl.ttl`). Alice is the claimant.

#### Graph

```turtle
<!-- databook:id: alice-passport-graph -->
<!-- databook:graph: http://www.example.org/tpod/graphs/graph-81#graph -->
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

:Self persona:hasIdentityDocument :Alice_US_Passport ;
    <https://w3id.org/cco-domains/cco/ont00001879> :Alice_Passport_Number .  # Person designated by → Passport Number

:Alice_US_Passport rdf:type owl:NamedIndividual ,
                             identitydocuments:Passport ;
    rdfs:label "Alice Walker's US Passport"@en ;
    rdfs:comment "Alice Walker's US passport identity data."@en ;

    # ── Legal name (matches Texas Birth Certificate and Driver's License) ────

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

    cco:ent00000069 [  # has issue date → Calendar Date Identifier
        rdf:type cco:ont00001340 ;
        <https://w3id.org/cco-domains/cco/ont00001765> "2021-07-04"^^xsd:date
    ] ;

    cco:ent00000070 [  # has expiration date → Calendar Date Identifier
        rdf:type cco:ont00001340 ;
        <https://w3id.org/cco-domains/cco/ont00001765> "2031-07-04"^^xsd:date
    ] ;

    # ── Passport number (two-relation form: Person designated-by, document is-carrier-of) ──

    <http://purl.obolibrary.org/obo/BFO_0000101> :Alice_Passport_Number ;  # document is carrier of → Passport Number

    # ── Issuing country ──────────────────────────────────────────────────────

    <https://w3id.org/cco-domains/cco/ont00001879> [  # designated by → Issuing Jurisdiction
        rdf:type cco:ent00000068 ;
        <https://w3id.org/cco-domains/cco/ont00001765> "USA"
    ] ;

    # ── Place of birth ───────────────────────────────────────────────────────

    <https://w3id.org/cco-domains/cco/ont00001879> [  # designated by → Place of Birth
        rdf:type cco:ent00000067 ;
        <https://w3id.org/cco-domains/cco/ont00001765> "Austin, Texas, USA"
    ] ;

    # ── Gender marker ────────────────────────────────────────────────────────

    <https://w3id.org/cco-domains/cco/ont00001879> [  # designated by → GenderMarker
        rdf:type identitydocuments:GenderMarker ;
        <https://w3id.org/cco-domains/cco/ont00001765> "F"
    ] ;

    # ── Photo ────────────────────────────────────────────────────────────────

    persona:hasPhoto "https://example.org/alice-passport-photo.jpg"^^xsd:anyURI .

:Alice_Passport_Number rdf:type owl:NamedIndividual ,
                                cco:ent00000066 ;  # Passport Number
    rdfs:label "Alice Walker's US Passport Number"@en ;
    <https://w3id.org/cco-domains/cco/ont00001765> "123456789" .  # placeholder US passport number
```
