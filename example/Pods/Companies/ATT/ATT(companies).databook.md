---
id: http://www.example.org/tpod/pods/pod-02
title: "ATT"
type: pod-databook
version: 2.0.0
created: 2026-07-10
description: >
  Pod DataBook for folder "ATT" (pod:category: podcat:Companies). It is a one-member pod with one
  member entry about :Self and one graph about :Alice_ATT_Account (the pod's subject), typed
  serviceaccounts:ServiceAccount and cco:ent00000033 (Online Service Account), carrying the service name,
  account username, and password for Alice's AT&T account.
tpod:
  category: "podcat:Companies"
  creator: ":Self"
  owner: ":Self"
  member:
    id: "http://www.example.org/tpod/graphs/graph-11"
    claimant: ":Self"
    subject: ":Self"
    shape: "pshapes:ContactInfoShape"
  tool:
    - id: "http://www.example.org/tpod/tools/tool-01"
      type: "form"
      formTopic: ":Alice_ATT_Account"
      graph:
        - id: "http://www.example.org/tpod/graphs/graph-74"
          claimant: ":Self"
          shape: "sashapes:ServiceAccountShape"
---

## Graphs

<a id="graph-11"></a>
### Graph 11

#### Overview

This graph is the pod's one required `member` entry — a pod with a single `member` entry in the user's own category-pod tree always has `:Self` as that member (see YAML-6), regardless of what the pod's `subject` is — here, Alice's AT&T account itself. Alice is both the claimant and the subject. It carries her given name, plus a minimal organization name and email, so `:Self` satisfies the `ContactInfoShape` every templated pod's `member` content is now expected to conform to (`pod:memberShape`) — no longer deliberately empty now that this requirement applies.

#### Graph

```turtle
<!-- databook:id: alice-att-member-graph -->
<!-- databook:graph: http://www.example.org/tpod/graphs/graph-11#graph -->
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
    ] ,
    [  # designated by → OrganizationName (ContactInfoShape)
        rdf:type cco:ent00000047 ;
        <https://w3id.org/cco-domains/cco/ont00001765> "Acme"
    ] ,
    [  # designated by → EmailAddress (ContactInfoShape)
        rdf:type cco:ent00000024 ;
        <https://w3id.org/cco-domains/cco/ont00001765> "alice@acme.com"
    ] .
```

<a id="graph-74"></a>
### Graph 74

#### Overview

This graph captures Alice's basic claim about her AT&T account itself — just enough to back the pod's `subject: ":Alice_ATT_Account"` with a real graph (see YAML-4) — and, validated by `serviceaccounts:ServiceAccount`'s SHACL shape (`other/shacl/service-accounts-shacl.ttl`'s `:ServiceAccountShape`), identifies the service (AT&T), her account username (her mobile phone number, in E.164 format — the same Phone designator this pod's original single graph used to carry on `:Self` directly, moved here since it's really a fact about the account, not about Alice as a person — AT&T accounts are logged into by phone number rather than a separate handle), her account's service URI, and her account password. `:Self` is also, separately, still designated by that same phone number directly (the `:Self`-level fact this pod's `member` graph doesn't itself carry). `:Self` carries `cco:ent00000045` (has/holds user account) to `:Alice_ATT_Account`, closing the loop from the Person side.

#### Graph

```turtle
<!-- databook:id: alice-att-subject-graph -->
<!-- databook:graph: http://www.example.org/tpod/graphs/graph-74#graph -->
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

:Self <https://w3id.org/cco-domains/cco/ont00001879> [  # designated by → Phone
        rdf:type cco:ent00000023 ;
        <https://w3id.org/cco-domains/cco/ont00001765> "+15108149999" ;
        rdfs:comment "E.164 format (international standard)"@en
    ] .

:Alice_ATT_Account rdf:type owl:NamedIndividual ,
                     serviceaccounts:ServiceAccount ,
                     cco:ent00000033 ;
    rdfs:label "Alice Walker's AT&T account"@en ;
    cco:ent00000034 "AT&T" ;                            # has service name
    cco:ent00000035 "+15108149999" ;                    # has user handle (username — AT&T logs in by phone number)
    cco:ent00000036 "https://www.att.com/my/"^^xsd:anyURI ;  # has service URI
    serviceaccounts:hasPassword "Alice#ATT2026!" .              # has password

:Self <https://w3id.org/cco-domains/cco/ent00000045> :Alice_ATT_Account .  # holds user account
```
