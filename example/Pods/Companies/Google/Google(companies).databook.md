---
id: http://www.example.org/tpod/pods/pod-03
title: "Google"
type: pod-databook
version: 2.0.0
created: 2026-07-10
description: >
  Pod DataBook for folder "Google" (pod:category: podcat:Companies). It is a one-member pod with one
  member entry about :Self and one graph about :Alice_Google_Account (the pod's subject), typed
  serviceaccounts:ServiceAccount and cco:ent00000033 (Online Service Account), carrying the service name,
  account username, and password for Alice's Google account.
tpod:
  category: "podcat:Companies"
  creator: ":Self"
  owner: ":Self"
  member:
    id: "http://www.example.org/tpod/graphs/graph-16"
    claimant: ":Self"
    subject: ":Self"
    shape: "pshapes:ContactInfoShape"
  tool:
    - id: "http://www.example.org/tpod/tools/tool-06"
      type: "form"
      formTopic: ":Alice_Google_Account"
      graph:
        - id: "http://www.example.org/tpod/graphs/graph-73"
          claimant: ":Self"
          shape: "sashapes:ServiceAccountShape"
---

## Graphs

<a id="graph-16"></a>
### Graph 16

#### Overview

This graph is the pod's one required `member` entry — a pod with a single `member` entry in the user's own category-pod tree always has `:Self` as that member (see YAML-6), regardless of what the pod's `subject` is — here, Alice's Google account itself. Alice is both the claimant and the subject. It carries her given name, plus a minimal organization name and email, so `:Self` satisfies the `ContactInfoShape` every templated pod's `member` content is now expected to conform to (`pod:memberShape`) — no longer deliberately empty now that this requirement applies.

#### Graph

```turtle
<!-- databook:id: alice-google-member-graph -->
<!-- databook:graph: http://www.example.org/tpod/graphs/graph-16#graph -->
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

<a id="graph-73"></a>
### Graph 73

#### Overview

This graph captures Alice's basic claim about her Google account itself — just enough to back the pod's `subject: ":Alice_Google_Account"` with a real graph (see YAML-4) — and, validated by `serviceaccounts:ServiceAccount`'s SHACL shape (`other/shacl/service-accounts-shacl.ttl`'s `:ServiceAccountShape`), identifies the service (Google), her account username (her Gmail address — the same Email designator this pod's original single graph used to carry on `:Self` directly, moved here since it's really a fact about the account, not about Alice as a person), and her account password. `:Self` is also, separately, still designated by that same Email address directly (the `:Self`-level fact this pod's `member` graph doesn't itself carry) — a person's Gmail address is both her own contact email and her Google account's username, so it's asserted once here on each individual it actually describes. `:Self` carries `cco:ent00000045` (has/holds user account) to `:Alice_Google_Account`, closing the loop from the Person side.

#### Graph

```turtle
<!-- databook:id: alice-google-subject-graph -->
<!-- databook:graph: http://www.example.org/tpod/graphs/graph-73#graph -->
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

:Alice_Google_Account rdf:type owl:NamedIndividual ,
                     serviceaccounts:ServiceAccount ,
                     cco:ent00000033 ;
    rdfs:label "Alice Walker's Google account"@en ;
    cco:ent00000034 "Google" ;                       # has service name
    cco:ent00000035 "awalker@gmail.com" ;            # has user handle (username)
    cco:ent00000036 "https://myaccount.google.com"^^xsd:anyURI ;  # has service URI
    serviceaccounts:hasPassword "Alice#Google2026!" .        # has password

:Self <https://w3id.org/cco-domains/cco/ent00000045> :Alice_Google_Account .  # holds user account
```
