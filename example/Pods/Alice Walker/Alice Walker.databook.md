---
id: http://www.example.org/tpod/pods/pod-18
title: "Alice Walker"
type: pod-databook
version: 1.3.0
created: 2026-07-10
description: >
  Pod DataBook for the "Alice Walker" pod (category tag: podcat:Employees; user tag: "Acme"). It is a one-member pod with one member entry about :Self.
tpod:
  categoryTag: "podcat:Employees"
  creator: ":Self"
  owner: ":Self"
  userTag:
    - "Acme"
  member:
    id: "http://www.example.org/tpod/graphs/graph-10"
    claimant: ":Self"
    subject: ":Self"
    shape: "pshapes:ContactInfoShape"
---

## Graphs

<a id="graph-10"></a>
### Graph 10

#### Overview

This graph captures Alice Walker's professional contact info in ContactInfo format. It records her full name, work email (alice@acme.com), work phone (+15108149999), employer (Acme), department (Engineering), job title (Software Engineer), and LinkedIn profile URL. Validated by the `ContactInfo` per-template SHACL shapes. Alice is the claimant.

#### Graph

```turtle
<!-- databook:id: alice-contact-info-graph -->
<!-- databook:graph: http://www.example.org/tpod/graphs/graph-10#graph -->
@prefix : <http://www.example.org/tpod#> .
@prefix persona: <http://mee.foundation/ontologies/persona#> .
@prefix cco: <https://w3id.org/cco-domains/cco/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

:Self rdf:type owl:NamedIndividual ,
               persona:Person .

:Self rdfs:comment "Alice Walker's Contact Info persona — professional contact details taking details from her Acme graph."@en ;

    # ── Name components ──────────────────────────────────────────────────────

    <https://w3id.org/cco-domains/cco/ont00001879> [  # designated by → GivenName
        rdf:type cco:ent00000002 ;
        <https://w3id.org/cco-domains/cco/ont00001765> "Alice"
    ] ;

    <https://w3id.org/cco-domains/cco/ont00001879> [  # designated by → FamilyName
        rdf:type cco:ent00000004 ;
        <https://w3id.org/cco-domains/cco/ont00001765> "Walker"
    ] ;

    # ── Contact channels ─────────────────────────────────────────────────────

    <https://w3id.org/cco-domains/cco/ont00001879> [  # designated by → EmailAddress (work)
        rdf:type cco:ent00000024 ;
        <https://w3id.org/cco-domains/cco/ont00001765> "alice@acme.com" ;
        persona:contactContext "work"
    ] ;

    <https://w3id.org/cco-domains/cco/ont00001879> [  # designated by → TelephoneNumber (work, voice)
        rdf:type cco:ent00000023 ;
        <https://w3id.org/cco-domains/cco/ont00001765> "+15108149999" ;
        persona:contactContext "work" ;
        persona:phoneFeature "voice"
    ] ;

    # ── Organisation ─────────────────────────────────────────────────────────

    <https://w3id.org/cco-domains/cco/ont00001879> [  # designated by → OrganizationName
        rdf:type cco:ent00000047 ;
        <https://w3id.org/cco-domains/cco/ont00001765> "Acme"
    ] ;

    <https://w3id.org/cco-domains/cco/ont00001879> [  # designated by → OrganizationUnit (department)
        rdf:type persona:OrganizationUnit ;
        <https://w3id.org/cco-domains/cco/ont00001765> "Engineering"
    ] ;

    <https://w3id.org/cco-domains/cco/ont00001879> [  # designated by → JobTitle
        rdf:type persona:JobTitle ;
        <https://w3id.org/cco-domains/cco/ont00001765> "Software Engineer"
    ] ;

    # ── Online services ──────────────────────────────────────────────────────

    <https://w3id.org/cco-domains/cco/ont00001879> [  # designated by → WebURL (LinkedIn profile)
        rdf:type persona:WebURL ;
        <https://w3id.org/cco-domains/cco/ont00001765> "https://www.linkedin.com/in/alicewalker" ;
        persona:serviceLabel "linkedin"
    ] .
```
