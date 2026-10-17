---
id: http://www.example.org/tpod/pods/pod-52
title: "Hilton"
type: pod-databook
version: 1.3.0
created: 2026-09-11
description: >
  Pod DataBook for folder "Hilton" (pod:category: podcat:TravelProvider). A leaf pod
  for one travel provider Alice books with, nested under the generic Provider
  category node and reusing its category — the same "child pod reuses its parent's
  category" pattern Ginger/Pets and Citibank/Banking & Payments Firms already use.
  It is a one-member pod with one member entry about :Self and one tool graph about
  her Hilton Honors account. podcat:TravelProvider's own pod:TemplatePod
  declares a form tool carrying pod:formShape sashapes:ServiceAccountShape, so
  that tool is template-driven and the pod carries it from the start.
  The pod carries no tag: what makes it findable is the loyaltyProgramID in its
  own tool graph, which a search for that property returns directly.
tpod:
  category: "podcat:TravelProvider"
  creator: ":Self"
  owner: ":Self"
  member:
    id: "http://www.example.org/tpod/graphs/graph-99"
    claimant: ":Self"
    subject: ":Self"
    shape: "pshapes:ContactInfoShape"
  tool:
    - id: "http://www.example.org/tpod/tools/tool-31"
      type: "form"
      formTopic: ":Alice_Hilton_Account"
      graph:
        - id: "http://www.example.org/tpod/graphs/graph-84"
          claimant: ":Self"
          shape: "sashapes:ServiceAccountShape"
---

## Graphs

<a id="graph-99"></a>
### Graph 99

#### Overview

This graph is the pod's one required `member` entry, claimed by and about `:Self`. It carries Alice's given name, satisfying the `ContactInfoShape` `ctpl:TravelProviderTemplatePod` sets as `pod:memberShape`. Everything specific to the Hilton relationship lives in the pod's tool graph instead (graph 84), since the member baseline is only ever a contact-info view of the pod's members.

#### Graph

```turtle
<!-- databook:id: alice-hilton-member-graph -->
<!-- databook:graph: http://www.example.org/tpod/graphs/graph-99#graph -->
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

<a id="graph-84"></a>
### Graph 84

#### Overview

This graph captures Alice's own claim about her Hilton Honors account — the pod's sole tool graph, so its tool's own `formTopic: ":Alice_Hilton_Account"` is what the pod's derived subject resolves to (see YAML-4). It is typed `serviceaccounts:ServiceAccount` and multi-typed `cco:ent00000033` (Online Service Account), the same pattern her Google, AT&T and Arca account graphs use, and is validated by `other/shacl/service-accounts-shacl.ttl`'s `:ServiceAccountShape`. Alongside the usual service name, username, service URI and password, it carries `serviceaccounts:loyaltyProgramID` — her Hilton Honors membership number, the value she quotes when booking or claiming points, distinct from the username she logs in with. It is the one example graph exercising that property; every other service-account graph here (Google, AT&T, Arca, Citibank) belongs to a provider running no loyalty program, so all of them legitimately omit it. `podcat:TravelProvider`'s own `pod:TemplatePod` declares a form tool carrying `pod:formShape sashapes:ServiceAccountShape`, so this tool is template-driven rather than hand-added: [Lazy Instantiation](../../../../../app-behavior.md#lazy-instantiation) stamps its `template:` value straight from that shape, and TTL-4 checks the two agree. Its real upper bound is the pod's own member count (YAML-8) — one topic per member, each with a distinct claimant — which for this one-member pod means exactly this one. Alice is both the claimant and the account holder.

#### Graph

```turtle
<!-- databook:id: alice-hilton-account-graph -->
<!-- databook:graph: http://www.example.org/tpod/graphs/graph-84#graph -->
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

:Alice_Hilton_Account rdf:type owl:NamedIndividual ,
                     serviceaccounts:ServiceAccount ,
                     cco:ent00000033 ;
    rdfs:label "Alice Walker's Hilton Honors account"@en ;
    cco:ent00000034 "Hilton Honors" ;                     # has service name
    cco:ent00000035 "awalker@gmail.com" ;                 # has user handle (username)
    cco:ent00000036 "https://www.hilton.com/en/hilton-honors"^^xsd:anyURI ;  # has service URI
    serviceaccounts:hasPassword "Alice#Hilton2026!" ;     # has password
    serviceaccounts:loyaltyProgramID "602194837" .        # Hilton Honors membership number

:Self <https://w3id.org/cco-domains/cco/ent00000045> :Alice_Hilton_Account .  # holds user account
```
