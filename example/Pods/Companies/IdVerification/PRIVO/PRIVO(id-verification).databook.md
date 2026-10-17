---
id: http://www.example.org/tpod/pods/pod-53
title: "PRIVO"
type: pod-databook
version: 1.1.0
created: 2026-09-26
description: >
  Pod DataBook for folder "PRIVO" (pod:category: podcat:IdVerification), nested under
  "IdVerification". The issuing half of the example tree's Browser Extension flow: Alice visited
  privo.com, which issued her an age-verification credential, and because no pod yet had a member
  whose service:siteDomain was privo.com, her app created this one. A two-member pod: Alice
  (graph-102) and :PRIVO_Site (graph-103). PRIVO supports the Pod Interface natively, so its
  member is not one Alice's app mints on its behalf: :PRIVO_Site is typed service:ServiceProvider
  as well as service:WebsiteService, provided by the organization :PRIVO (PRIVO Inc.), which claims
  the member entry, as every service:ServiceProvider's organization does. The credential itself is
  not in any graph: it is the pod's attachment privo-age-credential.json, kept exactly as PRIVO
  Inc. issued and signed it. The pod:Browser tool comes from the category's template and holds no
  graph of its own.
tpod:
  category: "podcat:IdVerification"
  creator: ":Self"
  owner: ":Self"
  member:
    - id: "http://www.example.org/tpod/graphs/graph-102"
      claimant: ":Self"
      subject: ":Self"
      shape: "pshapes:ContactInfoShape"
    - id: "http://www.example.org/tpod/graphs/graph-103"
      claimant: ":PRIVO"
      subject: ":PRIVO_Site"
      shape: "pshapes:ContactInfoShape"
  tool:
    - id: "http://www.example.org/tpod/tools/tool-08"
      type: "browser"
---

## Graphs

<a id="graph-102"></a>
### Graph 102

#### Overview

This graph is one of the pod's two required `member` entries — Alice's own bare given-name claim (see YAML-6: `:Self` must be a member of every pod in the user's own tree), carrying the given name `ContactInfoShape` requires as this template's `pod:memberShape`. Alice is both the claimant and the subject.

#### Graph

```turtle
<!-- databook:id: alice-privo-member-graph -->
<!-- databook:graph: http://www.example.org/tpod/graphs/graph-102#graph -->
@prefix : <http://www.example.org/tpod#> .
@prefix persona: <http://mee.foundation/ontologies/persona#> .
@prefix cco: <https://w3id.org/cco-domains/cco/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

:Self rdf:type owl:NamedIndividual ,
               persona:Person ;
    <https://w3id.org/cco-domains/cco/ont00001879> [  # designated by → GivenName (ContactInfoShape)
        rdf:type cco:ent00000002 ;
        <https://w3id.org/cco-domains/cco/ont00001765> "Alice"
    ] .
```

<a id="graph-103"></a>
### Graph 103

#### Overview

This graph is the other of the pod's two required `member` entries — PRIVO, the site that issued the credential, as `:PRIVO_Site`. It is typed two ways at once. As a `service:WebsiteService` it carries `service:siteDomain "privo.com"`, the key both credential flows match on: it is how the issuing flow found no existing pod for the site, and how the presenting flow later finds this one when it searches for a credential from a trusted issuer. As a `service:ServiceProvider` it carries `service:providedBy :PRIVO`, since PRIVO supports the Pod Interface natively, joining the pod and writing to it itself rather than having Alice's app mint a member on its behalf. Like every `service:ServiceProvider`, it is this entry's subject but not its claimant: the claims are PRIVO Inc.'s, the organization that also signed the credential this pod holds — the same pattern as `:BHS_Service` (graph 01) and `:Citibank_Service` (graph 27). No class in `service.ttl` is disjoint from any other, so the two types sit together without conflict.

Like graph 96, this `member` graph declares `pshapes:ContactInfoShape` (required of every member graph by TTL-7) while carrying no `persona:Person` individual at all, so it is vacuously conformant; `shacl/service-shacl.ttl`'s `:WebsiteServiceShape` and `:ServiceProviderShape` are what validate its content.

#### Graph

```turtle
<!-- databook:id: privo-site-member-graph -->
<!-- databook:graph: http://www.example.org/tpod/graphs/graph-103#graph -->
@prefix : <http://www.example.org/tpod#> .
@prefix o: <http://mee.foundation/ontologies/organization#> .
@prefix service: <http://mee.foundation/ontologies/service#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

:PRIVO_Site rdf:type owl:NamedIndividual ,
                     service:WebsiteService ,
                     service:ServiceProvider ;
    rdfs:label "PRIVO"@en ;
    service:siteDomain "privo.com" ;
    service:providedBy :PRIVO .

:PRIVO rdf:type owl:NamedIndividual ,
                o:Organization ;
    rdfs:label "PRIVO Inc."@en ;
    o:hasWebsite "https://www.privo.com"^^xsd:anyURI .
```
