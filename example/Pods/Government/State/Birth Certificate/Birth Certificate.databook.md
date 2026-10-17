---
id: http://www.example.org/tpod/pods/pod-10
title: "Birth Certificate"
type: pod-databook
version: 2.0.0
created: 2026-07-10
description: >
  Pod DataBook for folder "Birth Certificate" (pod:category: podcat:BirthCertificate). It is a
  one-member pod with one member entry about :Self and one tool graph about :Self (the pod's
  subject), typed identitydocuments:BirthCertificate, carrying Alice's Texas birth certificate
  identity data.
tpod:
  category: "podcat:BirthCertificate"
  creator: ":Self"
  owner: ":Self"
  member:
    id: "http://www.example.org/tpod/graphs/graph-24"
    claimant: ":Self"
    subject: ":Self"
    shape: "pshapes:ContactInfoShape"
  tool:
    - id: "http://www.example.org/tpod/tools/tool-13"
      type: "form"
      formTopic: ":Self"
      graph:
        - id: "http://www.example.org/tpod/graphs/graph-78"
          claimant: ":Self"
          shape: "idocshapes:BirthCertificateShape"
---

## Graphs

<a id="graph-24"></a>
### Graph 24

#### Overview

This graph is the pod's one required `member` entry — a pod with a single `member` entry in the user's own category-pod tree always has `:Self` as that member (see YAML-6). Alice is both the claimant and the subject. It carries her given name, satisfying the `ContactInfoShape` every templated pod's `member` content is now expected to conform to (`pod:memberShape`) — no longer the birth certificate document content, which now lives in this pod's tool graph instead (graph 78).

#### Graph

```turtle
<!-- databook:id: alice-birth-certificate-member-graph -->
<!-- databook:graph: http://www.example.org/tpod/graphs/graph-24#graph -->
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

<a id="graph-78"></a>
### Graph 78

#### Overview

This graph captures Alice Walker's Texas birth certificate identity data — moved here, as this pod's tool content, from the pod's former `member` graph-24. Alice self-enters her legal name (Margery Alice Walker) and maiden name (Margery Alice Arnold) from her physical birth certificate. Validated by the `BirthCertificateShape` per-template SHACL shape (`other/shacl/identity-documents-shacl.ttl`). Alice is the claimant.

#### Graph

```turtle
<!-- databook:id: alice-tx-birth-cert-graph -->
<!-- databook:graph: http://www.example.org/tpod/graphs/graph-78#graph -->
@prefix : <http://www.example.org/tpod#> .
@prefix persona: <http://mee.foundation/ontologies/persona#> .
@prefix identitydocuments: <http://mee.foundation/ontologies/identity-documents#> .
@prefix cco: <https://w3id.org/cco-domains/cco/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

:Self rdf:type owl:NamedIndividual ,
               persona:Person .

:Self persona:hasIdentityDocument :Alice_TX_Birth_Certificate .

:Alice_TX_Birth_Certificate rdf:type owl:NamedIndividual ,
                                      identitydocuments:BirthCertificate ;
    rdfs:label "Alice Walker's Texas Birth Certificate"@en ;

    <https://w3id.org/cco-domains/cco/ont00001879> [  # designated by → GivenName (legal first name)
        rdf:type cco:ent00000002 ;  # GivenName
        <https://w3id.org/cco-domains/cco/ont00001765> "Margery"  # has text value
    ] ;

    <https://w3id.org/cco-domains/cco/ont00001879> [  # designated by → AdditionalName (middle name)
        rdf:type cco:ent00000003 ;  # AdditionalName
        <https://w3id.org/cco-domains/cco/ont00001765> "Alice"  # has text value
    ] ;

    <https://w3id.org/cco-domains/cco/ont00001879> [  # designated by → FamilyName
        rdf:type cco:ent00000004 ;  # FamilyName
        <https://w3id.org/cco-domains/cco/ont00001765> "Walker"  # has text value
    ] ;

    <https://w3id.org/cco-domains/cco/ont00001879> [  # designated by → AlternateName (maiden name)
        rdf:type cco:ent00000006 ;  # AlternateName
        <https://w3id.org/cco-domains/cco/ont00001765> "Margery Alice Arnold" ;  # has text value
        rdfs:comment "Maiden name (former legal name before marriage)"@en
    ] .
```
