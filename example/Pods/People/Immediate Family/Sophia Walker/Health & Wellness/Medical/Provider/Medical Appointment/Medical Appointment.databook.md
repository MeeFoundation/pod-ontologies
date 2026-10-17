---
id: http://www.example.org/tpod/pods/pod-15
title: "Medical Appointment"
type: pod-databook
version: 2.0.0
created: 2026-07-10
description: >
  Pod DataBook for folder "Medical Appointment" (pod:category: podcat:MedicalAppointment). It is a two-member pod with two members about :Dave and :Self and one tool graph about :Sophia_Walker, Alice and Dave's daughter.
tpod:
  category: "podcat:MedicalAppointment"
  creator: ":Self"
  owner: ":Self"
  member:
    - id: "http://www.example.org/tpod/graphs/graph-28"
      claimant: ":Dave"
      subject: ":Dave"
      shape: "pshapes:ContactInfoShape"
    - id: "http://www.example.org/tpod/graphs/graph-30"
      claimant: ":Self"
      subject: ":Self"
      shape: "pshapes:ContactInfoShape"
  tool:
    - id: "http://www.example.org/tpod/tools/tool-23"
      type: "form"
      formTopic: ":Sophia_Walker"
      graph:
        - id: "http://www.example.org/tpod/graphs/graph-26"
          claimant: ":Self"
          shape: "mashapes:MedicalAppointmentRecordShape"
---

## Graphs

<a id="graph-26"></a>
### Graph 26

#### Overview

This graph captures Alice's shared record of the claims needed to arrange a medical appointment on behalf of their daughter, Sophia Walker. Alice maintains this record on her own instance of the app and syncs it to Dave's over the PDN so both parents can coordinate Sophia's care. Because each graph's named graph must be self-contained for p2p sync to work, the claims about Sophia and about her primary care physician, Dr. Jane Starostina, are copied directly into this graph rather than merely linked — Alice already holds Dr. Jane's information in her own instance, so it is Alice's own app that copies it over. Validated by the `MedicalAppointment` per-template SHACL shapes. Alice is the claimant.

#### Graph

```turtle
<!-- databook:id: alice-sophia-medical-appointment-graph -->
<!-- databook:graph: http://www.example.org/tpod/graphs/graph-26#graph -->
@prefix : <http://www.example.org/tpod#> .
@prefix persona: <http://mee.foundation/ontologies/persona#> .
@prefix cco: <https://w3id.org/cco-domains/cco/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix medicalappointments: <http://mee.foundation/ontologies/medical-appointments#> .

# ── Copied third-party individuals (self-containment for p2p sync) ──────────

:Sophia_Walker rdf:type owl:NamedIndividual ,
               persona:Person ;
    rdfs:label "Sophia Walker"@en ;

    <https://w3id.org/cco-domains/cco/ont00001879> [  # designated by → GivenName
        rdf:type cco:ent00000002 ;  # GivenName
        <https://w3id.org/cco-domains/cco/ont00001765> "Sophia"
    ] ;

    <https://w3id.org/cco-domains/cco/ont00001879> [  # designated by → FamilyName
        rdf:type cco:ent00000004 ;  # FamilyName
        <https://w3id.org/cco-domains/cco/ont00001765> "Walker"
    ] .

:Jane_Starostina rdf:type owl:NamedIndividual ,
               persona:Person ;
    rdfs:label "Jane Starostina (Primary Care Physician)"@en ;

    <https://w3id.org/cco-domains/cco/ont00001879> [  # designated by → GivenName
        rdf:type cco:ent00000002 ;  # GivenName
        <https://w3id.org/cco-domains/cco/ont00001765> "Jane"
    ] ;

    <https://w3id.org/cco-domains/cco/ont00001879> [  # designated by → FamilyName
        rdf:type cco:ent00000004 ;  # FamilyName
        <https://w3id.org/cco-domains/cco/ont00001765> "Starostina"
    ] ;

    <https://w3id.org/cco-domains/cco/ont00001917> [  # described by → Person Note
        rdf:type cco:ent00000048 ;
        <https://w3id.org/cco-domains/cco/ont00001765> "Sophia Walker's primary care physician"
    ] .

# ── The shared Medical Appointment claims record ─────────────────────────────

:Sophia_Medical_Appointment rdf:type owl:NamedIndividual ,
               medicalappointments:MedicalAppointmentRecord ;
    rdfs:label "Sophia Walker's Medical Appointment Claims"@en ;
    rdfs:comment "Claims Alice and Dave share to arrange and manage medical appointments for Sophia."@en ;

    medicalappointments:forPatient :Sophia_Walker ;
    medicalappointments:hasPrimaryCarePhysician :Jane_Starostina ;

    medicalappointments:currentMedication "Albuterol inhaler, 2 puffs as needed" ,
                               "Cetirizine 5mg daily" ;

    medicalappointments:allergy "Penicillin" ;

    medicalappointments:medicalHistoryNote "Mild persistent asthma; seasonal allergies." ;

    medicalappointments:insuranceProvider "Acme Health Plan (BlueShield of California)" ;
    medicalappointments:insurancePolicyNumber "XZC-884210773" ;

    medicalappointments:preferredPharmacy "CVS Pharmacy, 123 Main St, Paradise, CA" .
```

<a id="graph-28"></a>
### Graph 28

#### Overview

This graph captures Dave's own self-claimed persona and contact info, shared directly from his own instance of the app to Alice's over the PDN — his given name already satisfies the `ContactInfoShape` every templated pod's `member` content is now expected to conform to (`pod:memberShape`); the organization name below is optional extra detail, not what the shape actually requires. This pod's two members are Alice and Dave (its derived subject, `:Sophia_Walker` (from its sole tool's `formTopic`), is a third party the pod is *about*, not one of its members) — this graph and its counterpart (graph 30, Alice's own self-claimed contact info) together represent those two members, alongside graph 26 (Alice's claims about Sophia's medical appointment). Dave is the claimant.

#### Graph

```turtle
<!-- databook:id: dave-self-graph -->
<!-- databook:graph: http://www.example.org/tpod/graphs/graph-28#graph -->
@prefix : <http://www.example.org/tpod#> .
@prefix persona: <http://mee.foundation/ontologies/persona#> .
@prefix cco: <https://w3id.org/cco-domains/cco/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

:Dave rdf:type owl:NamedIndividual ,
               persona:Person ;
    rdfs:label "Dave (Alice's spouse)"@en ;

    <https://w3id.org/cco-domains/cco/ont00001879> [  # designated by → GivenName
        rdf:type cco:ent00000002 ;  # GivenName
        <https://w3id.org/cco-domains/cco/ont00001765> "Dave"
    ] ;

    <https://w3id.org/cco-domains/cco/ont00001879> [  # designated by → FamilyName
        rdf:type cco:ent00000004 ;  # FamilyName
        <https://w3id.org/cco-domains/cco/ont00001765> "Walker"
    ] ;

    <https://w3id.org/cco-domains/cco/ont00001879> [  # designated by → Phone
        rdf:type cco:ent00000023 ;
        <https://w3id.org/cco-domains/cco/ont00001765> "+19165550198"
    ] ;

    <https://w3id.org/cco-domains/cco/ont00001879> [  # designated by → OrganizationName (ContactInfoShape)
        rdf:type cco:ent00000047 ;
        <https://w3id.org/cco-domains/cco/ont00001765> "Self-Employed"
    ] ;

    <https://w3id.org/cco-domains/cco/ont00001917> [  # described by → Person Note
        rdf:type cco:ent00000048 ;
        <https://w3id.org/cco-domains/cco/ont00001765> "Usually available weekday evenings and weekends for Sophia's appointments."
    ] .
```

<a id="graph-30"></a>
### Graph 30

#### Overview

This graph captures Alice Walker's own self-claimed contact info, kept in this pod so Dave can reach her while coordinating Sophia's medical appointments, plus her given name, which is what actually satisfies the `ContactInfoShape` every templated pod's `member` content is now expected to conform to (`pod:memberShape`) — the organization name below is optional extra detail, not a requirement. This pod's two members are Alice and Dave (its derived subject, `:Sophia_Walker` (from its sole tool's `formTopic`), is a third party the pod is *about*, not one of its members) — this graph and its counterpart (graph 28, Dave's own self-claimed persona) together represent those two members, alongside graph 26 (Alice's claims about Sophia's medical appointment). Alice is the claimant.

#### Graph

```turtle
<!-- databook:id: alice-self-graph -->
<!-- databook:graph: http://www.example.org/tpod/graphs/graph-30#graph -->
@prefix : <http://www.example.org/tpod#> .
@prefix cco: <https://w3id.org/cco-domains/cco/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix persona: <http://mee.foundation/ontologies/persona#> .

:Self rdf:type owl:NamedIndividual ,
               persona:Person .

:Self <https://w3id.org/cco-domains/cco/ont00001879> [  # designated by → GivenName (ContactInfoShape)
        rdf:type cco:ent00000002 ;
        <https://w3id.org/cco-domains/cco/ont00001765> "Alice"
    ] ;

    <https://w3id.org/cco-domains/cco/ont00001879> [  # designated by → Phone
        rdf:type cco:ent00000023 ;
        <https://w3id.org/cco-domains/cco/ont00001765> "+15108149999"
    ] ;

    <https://w3id.org/cco-domains/cco/ont00001879> [  # designated by → OrganizationName (ContactInfoShape)
        rdf:type cco:ent00000047 ;
        <https://w3id.org/cco-domains/cco/ont00001765> "Acme"
    ] ;

    <https://w3id.org/cco-domains/cco/ont00001917> [  # described by → Person Note
        rdf:type cco:ent00000048 ;
        <https://w3id.org/cco-domains/cco/ont00001765> "Best reached by text for scheduling Sophia's appointments."
    ] .
```
