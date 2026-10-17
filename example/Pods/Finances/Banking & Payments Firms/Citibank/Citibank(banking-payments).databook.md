---
id: http://www.example.org/tpod/pods/pod-04
title: "Citibank"
type: pod-databook
version: 2.1.0
created: 2026-07-10
description: >
  Pod DataBook for folder "Citibank" (pod:category: podcat:BankingPayments). It is a two-member
  pod (member entries about :Citibank_Service and :Self) with two tool graphs about :Self — one
  Alice's own self-asserted service-account username/password, the other Citibank's own claimed
  record (debit card, checking account, online service account). An o:Organization is not
  member-capable, so the bank participates through :Citibank_Service, the service:ServiceProvider
  it provides; both that member graph and the tool graph are claimed by :Citibank itself, the
  party really making those claims.
tpod:
  category: "podcat:BankingPayments"
  creator: ":Self"
  owner: ":Self"
  member:
    - id: "http://www.example.org/tpod/graphs/graph-27"
      claimant: ":Citibank"
      subject: ":Citibank_Service"
      shape: "pshapes:ContactInfoShape"
    - id: "http://www.example.org/tpod/graphs/graph-77"
      claimant: ":Self"
      subject: ":Self"
      shape: "pshapes:ContactInfoShape"
  tool:
    - id: "http://www.example.org/tpod/tools/tool-10"
      type: "form"
      formTopic: ":Self"
      graph:
        - id: "http://www.example.org/tpod/graphs/graph-75"
          claimant: ":Self"
          shape: "sashapes:ServiceAccountShape"
        - id: "http://www.example.org/tpod/graphs/graph-76"
          claimant: ":Citibank"
          shape:
            - "sashapes:ServiceAccountShape"
            - "bankingshapes:DebitCardShape"
            - "bankingshapes:CheckingAccountShape"
---

## Graphs

<a id="graph-27"></a>
### Graph 27

#### Overview

This graph captures the identity Citibank presents as one of the pod's two members — the bank's side of the relationship. An `o:Organization` is never itself a `pod:member` graph's `pod:subject`, so what joins the pod is `:Citibank_Service`, the `service:ServiceProvider` the bank provides, carrying `service:providedBy :Citibank`. The bank's name, website, and short institutional self-description sit on `:Citibank` itself, where they belong; its own claimed record about Alice (debit card, checking account, online service account) is the pod's tool graph instead, graph 76. Citibank — the organization, not the service — is the claimant, since it is the party really making the claim and the one an eventual cryptographic signature would name. Alice's own notes about banking here are her claim, not the bank's, and live in her own member graph instead (graph 77).

#### Graph

```turtle
<!-- databook:id: citibank-org-graph -->
<!-- databook:graph: http://www.example.org/tpod/graphs/graph-27#graph -->
@prefix : <http://www.example.org/tpod#> .
@prefix o: <http://mee.foundation/ontologies/organization#> .
@prefix service: <http://mee.foundation/ontologies/service#> .
@prefix cco: <https://w3id.org/cco-domains/cco/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

:Citibank_Service rdf:type owl:NamedIndividual ,
                   service:ServiceProvider ;
    rdfs:label "Citibank consumer banking service"@en ;
    service:providedBy :Citibank .

:Citibank rdf:type owl:NamedIndividual ,
                   o:Organization ;
    rdfs:label "Citibank"@en ;
    o:hasWebsite "https://citibank.com"^^xsd:anyURI ;

    <https://w3id.org/cco-domains/cco/ont00001917> [  # described by → Organization Note
        rdf:type cco:ent00000048 ;
        <https://w3id.org/cco-domains/cco/ont00001765> "A national consumer bank offering checking and savings accounts, debit and credit cards, lending, and online banking."
    ] .
```

<a id="graph-77"></a>
### Graph 77

#### Overview

This graph is one of the pod's two required `member` entries, claimed by and about `:Self` — a minimal given-name stub, so `:Self` is a genuine member of this pod (see YAML-6) alongside `:Citibank_Service` (graph 27), matching the diagram's two member shapes. It also carries Alice's own notes about Citibank as an institution, asserted on `:Citibank` where they belong: these are her claims about why she banks there, not the bank's, so they sit in the graph she claims rather than in Citibank's own member graph. Note: this makes the pod's own `member` `subject` values (`:Self`, `:Citibank_Service`) overlap with its tool's `formTopic` value (`:Self`, from graphs 75/76) — a known, deliberately-deferred YAML-4 tension.

#### Graph

```turtle
<!-- databook:id: alice-citibank-member-graph -->
<!-- databook:graph: http://www.example.org/tpod/graphs/graph-77#graph -->
@prefix : <http://www.example.org/tpod#> .
@prefix o: <http://mee.foundation/ontologies/organization#> .
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
    ] .

:Citibank rdf:type owl:NamedIndividual ,
                   o:Organization ;
    rdfs:label "Citibank"@en ;

    <https://w3id.org/cco-domains/cco/ont00001917> [  # described by → Organization Note
        rdf:type cco:ent00000048 ;
        <https://w3id.org/cco-domains/cco/ont00001765> "My primary checking account is here — used for rent and bill-pay autopay. Opened 2019."
    ] .
```

<a id="graph-75"></a>
### Graph 75

#### Overview

This graph is Alice's own self-asserted claim about her Citibank online service account — just its username and password, as she herself knows them — distinct from Citibank's own claimed record of the same account (graph 76). Alice is the claimant.

#### Graph

```turtle
<!-- databook:id: alice-citibank-self-asserted-account-graph -->
<!-- databook:graph: http://www.example.org/tpod/graphs/graph-75#graph -->
@prefix : <http://www.example.org/tpod#> .
@prefix persona: <http://mee.foundation/ontologies/persona#> .
@prefix cco: <https://w3id.org/cco-domains/cco/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix serviceaccounts: <http://mee.foundation/ontologies/service-accounts#> .

:Self rdf:type owl:NamedIndividual ,
               persona:Person .

:Alice_Citibank_Online rdf:type owl:NamedIndividual ,
                     serviceaccounts:ServiceAccount ,
                     cco:ent00000033 ;  # Online Service Account
    cco:ent00000035 "awalker@gmail.com" ;           # has user handle (username), self-known
    serviceaccounts:hasPassword "C1t1b@nk#2024!" .          # has password, self-known

:Self <https://w3id.org/cco-domains/cco/ent00000045> :Alice_Citibank_Online .  # holds user account
```

<a id="graph-76"></a>
### Graph 76

#### Overview

This graph captures Alice Walker's financial relationship with Citibank. Citibank is a PDN Organization node which directly claims the information about Alice in this graph. The information in this graph has been transmitted from the Citibank PDN node to Alice's own instance of the app. It includes a VISA debit card linked to a checking account, plus an online service account for online.citi.com. Citibank is the claimant.

#### Graph

```turtle
<!-- databook:id: citibank-graph -->
<!-- databook:graph: http://www.example.org/tpod/graphs/graph-76#graph -->
@prefix : <http://www.example.org/tpod#> .
@prefix persona: <http://mee.foundation/ontologies/persona#> .
@prefix o: <http://mee.foundation/ontologies/organization#> .
@prefix cco: <https://w3id.org/cco-domains/cco/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix serviceaccounts: <http://mee.foundation/ontologies/service-accounts#> .
@prefix banking: <http://mee.foundation/ontologies/banking#> .

:Self rdf:type owl:NamedIndividual ,
               persona:Person .

:Citibank rdf:type owl:NamedIndividual ,
                   o:Organization ;
    rdfs:label "Citibank"@en .

:Self rdfs:comment "Alice Walker regarding her Citibank relationship."@en ;
    cco:ent00000073 :Alice_Debit_Card ;             # has payment card
    persona:hasBankAccount :Alice_Checking_Account ;
    cco:ent00000045 :Alice_Citibank_Online .  # holds user account

:Alice_Debit_Card rdf:type owl:NamedIndividual ,
                           banking:DebitCard ,
                           cco:ent00000051 ;  # Debit Card
    rdfs:label "Alice Walker's VISA Debit Card"@en ;
    <https://w3id.org/cco-domains/cco/ont00001879> [  # designated by → Card Number (PAN)
        rdf:type cco:ent00000052 ;
        <https://w3id.org/cco-domains/cco/ont00001765> "4111-1111-1111-1111"
    ] ;
    <https://w3id.org/cco-domains/cco/ont00001879> [  # designated by → CVV
        rdf:type cco:ent00000053 ;
        <https://w3id.org/cco-domains/cco/ont00001765> "123"
    ] ;
    cco:ent00000070 [  # has expiration date → Calendar Date Identifier
        rdf:type cco:ont00001340 ;
        <https://w3id.org/cco-domains/cco/ont00001765> "12/28"
    ] ;
    banking:accessesBankAccount :Alice_Checking_Account .

:Alice_Checking_Account rdf:type owl:NamedIndividual ,
                                 banking:CheckingAccount ;
    rdfs:label "Alice Walker's Citibank Checking Account"@en ;
    <https://w3id.org/cco-domains/cco/ont00001879> [  # designated by → Checking Account Number
        rdf:type cco:ent00000071 ;
        <https://w3id.org/cco-domains/cco/ont00001765> "9876543210"
    ] ;
    <https://w3id.org/cco-domains/cco/ont00001879> [  # designated by → Routing Number
        rdf:type cco:ent00000072 ;
        <https://w3id.org/cco-domains/cco/ont00001765> "021000089"
    ] .

:Alice_Citibank_Online rdf:type owl:NamedIndividual ,
                                serviceaccounts:ServiceAccount ,
                                cco:ent00000033 ;  # Online Service Account
    rdfs:label "Alice Walker's Citibank Online Account"@en ;
    cco:ent00000034 "Citibank" ;                   # has service name
    cco:ent00000035 "awalker@gmail.com" ;           # has user handle (username)
    cco:ent00000036 "https://online.citi.com"^^xsd:anyURI ;  # has service URI
    serviceaccounts:hasPassword "C1t1b@nk#2024!" .         # has password
```
