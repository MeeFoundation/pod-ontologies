---
id: http://www.example.org/tpod/pods/pod-27
title: "Chestnut Hill Village Association"
type: pod-databook
version: 1.0.0
created: 2026-09-13
description: >
  Pod DataBook for folder "Chestnut Hill Village Association" (pod:category: podcat:Groups). It is a
  multi-member pod with three members about :Self, :Marcy, and :Henry — three of the homeowners on the
  three streets that make up Chestnut Hill Village — plus one tool graph about :CHVA itself, the
  association's own organizational profile. Unlike the Boston Hub Society, the association runs no PDN
  node of its own, so it joins the pod through no service:ServiceProvider of its own and Alice
  self-enters its profile: every one of this pod's graphs is claimed by one of its three human members.
tpod:
  category: "podcat:Groups"
  creator: ":Self"
  owner: ":Self"
  member:
    - id: "http://www.example.org/tpod/graphs/graph-09"
      claimant: ":Self"
      subject: ":Self"
      shape: "pshapes:ContactInfoShape"
    - id: "http://www.example.org/tpod/graphs/graph-45"
      claimant: ":Marcy"
      subject: ":Marcy"
      shape: "pshapes:ContactInfoShape"
    - id: "http://www.example.org/tpod/graphs/graph-100"
      claimant: ":Henry"
      subject: ":Henry"
      shape: "pshapes:ContactInfoShape"
  tool:
    - id: "http://www.example.org/tpod/tools/tool-16"
      type: "form"
      formTopic: ":CHVA"
      graph:
        - id: "http://www.example.org/tpod/graphs/graph-101"
          claimant: ":Self"
          shape: "oshapes:OrganizationShape"
---

## Graphs

<a id="graph-09"></a>
### Graph 09

#### Overview

This graph captures Alice Walker's Chestnut Hill Village Association profile — the identity data she shares with her neighbors in the association. It carries the name she goes by there, the email address the association's mailing list reaches her at, and her association social network, whose members are her neighbors Marcy and Henry. Alice is both the claimant and the subject.

#### Graph

```turtle
<!-- databook:id: alice-chva-graph -->
<!-- databook:graph: http://www.example.org/tpod/graphs/graph-09#graph -->
@prefix : <http://www.example.org/tpod#> .
@prefix persona: <http://mee.foundation/ontologies/persona#> .
@prefix cco: <https://w3id.org/cco-domains/cco/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

:Self rdf:type owl:NamedIndividual ,
               persona:Person .

:Marcy rdf:type owl:NamedIndividual ,
               persona:Person .

:Henry rdf:type owl:NamedIndividual ,
               persona:Person .

:Self rdfs:comment "Alice Walker's persona for her Chestnut Hill Village Association profile."@en ;

    <https://w3id.org/cco-domains/cco/ont00001879> [  # designated by → GivenName (ContactInfoShape)
        rdf:type cco:ent00000002 ;
        <https://w3id.org/cco-domains/cco/ont00001765> "Alice"
    ] ;

    <https://w3id.org/cco-domains/cco/ont00001879> [  # designated by → AlternateName
        rdf:type cco:ent00000006 ;  # AlternateName
        <https://w3id.org/cco-domains/cco/ont00001765> "Alice Walker"
    ] ;

    <https://w3id.org/cco-domains/cco/ont00001879> [  # designated by → Email
        rdf:type cco:ent00000024 ;
        <https://w3id.org/cco-domains/cco/ont00001765> "awalker@gmail.com"
    ] ;

    persona:hasSocialNetwork :Alice_CHVA_Network .


:Alice_CHVA_Network rdf:type owl:NamedIndividual ,
                             cco:ont00001183 ;  # Social Network
    rdfs:label "Alice Walker's Chestnut Hill Village Association connections"@en ;
    <http://purl.obolibrary.org/obo/BFO_0000115> :Marcy ,  # has member part
                                                 :Henry .
```

<a id="graph-45"></a>
### Graph 45

#### Overview

This graph captures Marcy's Chestnut Hill Village Association profile as transmitted from Marcy's own instance of the app to Alice's over the PDN. It records the name and email she presents to her neighbors in the association. Marcy is the claimant.

#### Graph

```turtle
<!-- databook:id: marcy-chva-graph -->
<!-- databook:graph: http://www.example.org/tpod/graphs/graph-45#graph -->
@prefix : <http://www.example.org/tpod#> .
@prefix persona: <http://mee.foundation/ontologies/persona#> .
@prefix cco: <https://w3id.org/cco-domains/cco/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

:Marcy rdf:type owl:NamedIndividual ,
                persona:Person ;
    rdfs:label "Marcy (CHVA)"@en ;

    <https://w3id.org/cco-domains/cco/ont00001879> [  # designated by → GivenName
        rdf:type cco:ent00000002 ;
        <https://w3id.org/cco-domains/cco/ont00001765> "Marcy"
    ] ;

    <https://w3id.org/cco-domains/cco/ont00001879> [  # designated by → Email
        rdf:type cco:ent00000024 ;
        <https://w3id.org/cco-domains/cco/ont00001765> "marcy@example.com"
    ] .
```

<a id="graph-100"></a>
### Graph 100

#### Overview

This graph captures Henry's Chestnut Hill Village Association profile as transmitted from Henry's own instance of the app to Alice's over the PDN. It records the name and email he presents to his neighbors in the association. Henry is the claimant.

#### Graph

```turtle
<!-- databook:id: henry-chva-graph -->
<!-- databook:graph: http://www.example.org/tpod/graphs/graph-100#graph -->
@prefix : <http://www.example.org/tpod#> .
@prefix persona: <http://mee.foundation/ontologies/persona#> .
@prefix cco: <https://w3id.org/cco-domains/cco/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

:Henry rdf:type owl:NamedIndividual ,
                persona:Person ;
    rdfs:label "Henry (CHVA)"@en ;

    <https://w3id.org/cco-domains/cco/ont00001879> [  # designated by → GivenName
        rdf:type cco:ent00000002 ;
        <https://w3id.org/cco-domains/cco/ont00001765> "Henry"
    ] ;

    <https://w3id.org/cco-domains/cco/ont00001879> [  # designated by → Email
        rdf:type cco:ent00000024 ;
        <https://w3id.org/cco-domains/cco/ont00001765> "henry@example.com"
    ] .
```

<a id="graph-101"></a>
### Graph 101

#### Overview

This graph captures the Chestnut Hill Village Association's own organizational profile — the association as an `o:Organization` in its own right, with the number of households it covers and its public website — as the pod's tool graph. Where the Boston Hub Society claims its own profile (graph 92) from its own PDN node, the association has none, so Alice self-enters this one: she is the claimant, and `:CHVA` is never a `pod:member` subject at all. The association's day-to-day working material — its recommended contractors (plumbers, electricians, lawn care and the like), the dates of its annual in-person meeting and its annual spring cleanup event, the name of the current president, and its annual dues — is free text rather than modeled data, and lives in this pod's folder note — `Chestnut Hill Village Association.md`, shown in the app's Note area rather than its Attachments area — instead of here.

#### Graph

```turtle
<!-- databook:id: chva-org-profile-graph -->
<!-- databook:graph: http://www.example.org/tpod/graphs/graph-101#graph -->
@prefix : <http://www.example.org/tpod#> .
@prefix o: <http://mee.foundation/ontologies/organization#> .
@prefix cco: <https://w3id.org/cco-domains/cco/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

:CHVA rdf:type owl:NamedIndividual ,
               o:Organization ;
    rdfs:label "Chestnut Hill Village Association"@en ;

    o:numMembers 64 ;
    o:hasWebsite "https://chestnuthillvillage.example.org"^^xsd:anyURI ;

    <https://w3id.org/cco-domains/cco/ont00001917> [  # described by → Organization Note
        rdf:type cco:ent00000048 ;
        <https://w3id.org/cco-domains/cco/ont00001765> "A neighborhood association of the homeowners on the three streets that make up Chestnut Hill Village. Members include Alice Walker, Marcy, and Henry."
    ] .
```
