---
id: http://www.example.org/tpod/pods/pod-54
title: "Facenook"
type: pod-databook
version: 1.1.0
created: 2026-09-26
description: >
  Pod DataBook for folder "Facenook" (pod:category: podcat:Companies), nested under "Companies".
  The presenting half of the example tree's Browser Extension flow: facenook.com, a social
  network site, asked Alice for an
  age credential from any of a set of age-verification providers it trusts, PRIVO among them. No
  pod had a member whose service:siteDomain was facenook.com, so her app created this one; its
  classifier was not confident what kind of company the site was, so the pod fell back to
  podcat:Companies. The app then found the credential PRIVO had issued in the PRIVO pod, copied
  it here bit for bit as the attachment privo-age-credential.json, and presented it to
  facenook.com through the browser extension. A two-member pod: Alice (graph-104) and
  :Facenook_Site, the service:WebsiteService her app minted for the site (graph-105), claimed by
  Alice. It carries two tools: the form tool podcat:Companies' template declares, holding Alice's
  Facenook account (graph-106), the same sa:ServiceAccount pattern the Google, ATT and Arca pods
  use; and a pod:Browser tool, which no template declared here and the app added during the
  presenting flow.
tpod:
  category: "podcat:Companies"
  creator: ":Self"
  owner: ":Self"
  member:
    - id: "http://www.example.org/tpod/graphs/graph-104"
      claimant: ":Self"
      subject: ":Self"
      shape: "pshapes:ContactInfoShape"
    - id: "http://www.example.org/tpod/graphs/graph-105"
      claimant: ":Self"
      subject: ":Facenook_Site"
      shape: "pshapes:ContactInfoShape"
  tool:
    - id: "http://www.example.org/tpod/tools/tool-04"
      type: "form"
      formTopic: ":Alice_Facenook_Account"
      graph:
        - id: "http://www.example.org/tpod/graphs/graph-106"
          claimant: ":Self"
          shape: "sashapes:ServiceAccountShape"
    - id: "http://www.example.org/tpod/tools/tool-05"
      type: "browser"
---

## Graphs

<a id="graph-104"></a>
### Graph 104

#### Overview

This graph is one of the pod's two required `member` entries — Alice's own bare given-name claim (see YAML-6: `:Self` must be a member of every pod in the user's own tree), carrying the given name `ContactInfoShape` requires as this template's `pod:memberShape`. Alice is both the claimant and the subject.

#### Graph

```turtle
<!-- databook:id: alice-facenook-member-graph -->
<!-- databook:graph: http://www.example.org/tpod/graphs/graph-104#graph -->
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

<a id="graph-105"></a>
### Graph 105

#### Overview

This graph is the other of the pod's two required `member` entries — Facenook, the social network site the credential was presented to, as `:Facenook_Site`, a `service:WebsiteService` with `service:siteDomain "facenook.com"`. Alice's app minted it during the presenting flow, finding no pod with a member for that domain; the next time facenook.com asks for a credential, this is the pod the app finds. Unlike PRIVO, which supports the Pod Interface natively and whose organization claims its own entry (graph 103), facenook.com takes no part in the pod: it never receives a copy or writes to it, so Alice claims the entry, with the service as its subject, and it carries neither `service:actsFor` nor `service:providedBy`.

Like graph 103, it declares `pshapes:ContactInfoShape` while carrying no `persona:Person` individual, so it is vacuously conformant; `shacl/service-shacl.ttl`'s `:WebsiteServiceShape` validates its content.

#### Graph

```turtle
<!-- databook:id: facenook-site-member-graph -->
<!-- databook:graph: http://www.example.org/tpod/graphs/graph-105#graph -->
@prefix : <http://www.example.org/tpod#> .
@prefix service: <http://mee.foundation/ontologies/service#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

:Facenook_Site rdf:type owl:NamedIndividual ,
                        service:WebsiteService ;
    rdfs:label "Facenook"@en ;
    service:siteDomain "facenook.com" .
```

<a id="graph-106"></a>
### Graph 106

#### Overview

This graph captures Alice's basic claim about her Facenook account itself — the sole graph of the form tool `podcat:Companies`' template declares, whose `formTopic: ":Alice_Facenook_Account"` is what the pod's derived subject resolves to (see integrity.md's YAML-4). Typed `serviceaccounts:ServiceAccount`, also multi-typed `cco:ent00000033` (Online Service Account), and validated by `other/shacl/service-accounts-shacl.ttl`'s `:ServiceAccountShape` — the same pattern the Google, ATT and Arca pods use. It records the service name, her username, the service URI, and her password. `:Self` carries `cco:ent00000045` (holds user account) to `:Alice_Facenook_Account`, closing the loop from the Person side.

#### Graph

```turtle
<!-- databook:id: alice-facenook-subject-graph -->
<!-- databook:graph: http://www.example.org/tpod/graphs/graph-106#graph -->
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

:Alice_Facenook_Account rdf:type owl:NamedIndividual ,
                         serviceaccounts:ServiceAccount ,
                         cco:ent00000033 ;
    rdfs:label "Alice Walker's Facenook account"@en ;
    cco:ent00000034 "Facenook" ;                          # has service name
    cco:ent00000035 "awalker@gmail.com" ;                 # has user handle (username)
    cco:ent00000036 "https://www.facenook.com"^^xsd:anyURI ;  # has service URI
    serviceaccounts:hasPassword "Alice#Facenook2026!" .   # has password

:Self <https://w3id.org/cco-domains/cco/ent00000045> :Alice_Facenook_Account .  # holds user account
```
