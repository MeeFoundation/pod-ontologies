---
id: http://www.example.org/tpod/pods/pod-50
title: "Arca"
type: pod-databook
version: 1.1.0
created: 2026-09-10
description: >
  Pod DataBook for folder "Arca" (pod:category: podcat:Companies), nested under "Companies". Alice's
  pod backup provider. A two-member pod demonstrating service:ArcaBackup as a real pod member:
  :Arca_Backup, the backup service Arca provides, joins alongside Alice, each with its own member
  entry (graph-95, graph-96). :Arca_Backup is a service:ArcaBackup, an agent service: it carries
  service:actsFor :Self, since Alice invited it and it preserves her own copy of the pod, and
  service:providedBy :Arca, naming the organization that runs it. That is what separates it from
  :Citibank_Service and :BHS_Service, service:ServiceProvider individuals that act for the
  organization behind them rather than for a member. The account Alice holds with Arca is the topic of the pod's tool (graph-97), the same
  sa:ServiceAccount pattern the Google and ATT pods already use.
tpod:
  category: "podcat:Companies"
  creator: ":Self"
  owner: ":Self"
  member:
    - id: "http://www.example.org/tpod/graphs/graph-95"
      claimant: ":Self"
      subject: ":Self"
      shape: "pshapes:ContactInfoShape"
    - id: "http://www.example.org/tpod/graphs/graph-96"
      claimant: ":Arca_Backup"
      subject: ":Arca_Backup"
      shape: "pshapes:ContactInfoShape"
  tool:
    - id: "http://www.example.org/tpod/tools/tool-02"
      type: "form"
      formTopic: ":Alice_Arca_Account"
      graph:
        - id: "http://www.example.org/tpod/graphs/graph-97"
          claimant: ":Self"
          shape: "sashapes:ServiceAccountShape"
---

## Graphs

<a id="graph-95"></a>
### Graph 95

#### Overview

This graph is one of the pod's two required `member` entries — Alice's own bare given-name claim (see YAML-6: `:Self` must be a member of every pod in the user's own tree, regardless of member count), carrying the given name `ContactInfoShape` requires as this template's `pod:memberShape`. Alice is both the claimant and the subject.

#### Graph

```turtle
<!-- databook:id: alice-arca-member-graph -->
<!-- databook:graph: http://www.example.org/tpod/graphs/graph-95#graph -->
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

<a id="graph-96"></a>
### Graph 96

#### Overview

This graph is the other of the pod's two required `member` entries — Arca's backup service, joining as a real pod member with its own self-claimed member graph, exactly like a human member's. It is typed `service:ArcaBackup`, a leaf under `service:AgentService`, and carries both `service:actsFor :Self` — Alice invited it, and it is her copy of the pod it preserves, so she is the one member it answers to — and `service:providedBy :Arca`, naming the organization that runs it. Carrying both is what distinguishes it from the other two agent-service leaves: `service:ChatGPT` (the Kyoto Trip pod's own agent member, graph 67) names no provider, because OpenAI is not a party to that pod's relationship, whereas Arca genuinely is a party to this one. A `service:Service` is never a `pod:creator` and can never be promoted to `pod:owner` — Alice alone created and owns this pod — but it is a legitimate `pod:member` participant and, having no organization claiming on its behalf in this relationship, a `pod:claimant` under its own IRI.

Like graph 01 and graph 27, this `member` graph declares `pshapes:ContactInfoShape` (required of every member graph by TTL-7) while carrying no *substantive* contact-info content — the only `persona:Person` individual here is the bare `:Self` the self-containment convention requires, since `service:actsFor` names her. `helpers/validate.py` re-targets `ContactInfoShape` at substantive individuals only, so that bare declaration is not treated as a contact-info profile, and the graph stays vacuously conformant — the exemption integrity.md's TTL-3 describes.

#### Graph

```turtle
<!-- databook:id: arca-backup-member-graph -->
<!-- databook:graph: http://www.example.org/tpod/graphs/graph-96#graph -->
@prefix : <http://www.example.org/tpod#> .
@prefix o: <http://mee.foundation/ontologies/organization#> .
@prefix persona: <http://mee.foundation/ontologies/persona#> .
@prefix service: <http://mee.foundation/ontologies/service#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

:Self rdf:type owl:NamedIndividual ,
               persona:Person .

:Arca_Backup rdf:type owl:NamedIndividual ,
                      service:ArcaBackup ;
    rdfs:label "Arca pod backup service"@en ;
    service:actsFor :Self ;
    service:providedBy :Arca .

:Arca rdf:type owl:NamedIndividual ,
               o:Organization ;
    rdfs:label "Arca"@en ;
    o:hasWebsite "https://arca.example.com"^^xsd:anyURI .
```

<a id="graph-97"></a>
### Graph 97

#### Overview

This graph captures Alice's basic claim about her Arca account itself — as the Arca pod's sole tool graph, its tool's own `formTopic: ":Alice_Arca_Account"` is what the pod's derived subject resolves to (see integrity.md's YAML-4). Typed `serviceaccounts:ServiceAccount`, also multi-typed `cco:ent00000033` (Online Service Account), and validated by `other/shacl/service-accounts-shacl.ttl`'s `:ServiceAccountShape` — the same pattern the Google and ATT pods use. It records the service name, her account username, the service URI, and her password. `:Self` carries `cco:ent00000045` (holds user account) to `:Alice_Arca_Account`, closing the loop from the Person side.

#### Graph

```turtle
<!-- databook:id: alice-arca-subject-graph -->
<!-- databook:graph: http://www.example.org/tpod/graphs/graph-97#graph -->
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

:Alice_Arca_Account rdf:type owl:NamedIndividual ,
                     serviceaccounts:ServiceAccount ,
                     cco:ent00000033 ;
    rdfs:label "Alice Walker's Arca account"@en ;
    cco:ent00000034 "Arca" ;                              # has service name
    cco:ent00000035 "awalker@gmail.com" ;                 # has user handle (username)
    cco:ent00000036 "https://arca.example.com/account"^^xsd:anyURI ;  # has service URI
    serviceaccounts:hasPassword "Alice#Arca2026!" .       # has password

:Self <https://w3id.org/cco-domains/cco/ent00000045> :Alice_Arca_Account .  # holds user account
```
