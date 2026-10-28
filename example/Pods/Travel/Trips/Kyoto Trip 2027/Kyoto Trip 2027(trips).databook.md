---
id: http://www.example.org/tpod/pods/pod-47
title: "Kyoto Trip 2027"
type: pod-databook
version: 1.3.0
created: 2026-08-30
description: >
  Pod DataBook for folder "Kyoto Trip 2027" (pod:category: podcat:Trips, reusing its parent "Trips"
  pod's own origin), nested under "Travel" > "Trips". A user-defined instance folder for a
  specific trip Alice is planning with her spouse Dave. A three-member pod demonstrating
  a service:PodAgent as a real pod member: an AI travel agent Alice sponsors, backed by ChatGPT,
  joins alongside Alice and Dave,
  each with a self-claimed member entry (graph-66, graph-67, graph-68). The trip itself is backed
  by three tool graphs sharing one subject (:Kyoto_Trip_2027), one per member, each with a
  distinct claimant — Alice's own basic claim (graph-69), her agent's own evolving,
  collaboratively-drafted itinerary (graph-70), and Dave's own contribution (graph-91) — reaching
  pod:formGraph's real upper bound (one graph per member, see YAML-8) and mirroring how a
  tool's topic may be claimed from more than one side (see the Medical Appointment pod's two
  "Med. Appt mt." squares in README.md's Representative Pods diagram).
tpod:
  category: "podcat:Trips"
  creator: ":Self"
  owner: ":Self"
  member:
    - id: "http://www.example.org/tpod/graphs/graph-66"
      claimant: ":Self"
      subject: ":Self"
      shape: "pshapes:ContactInfoShape"
    - id: "http://www.example.org/tpod/graphs/graph-67"
      claimant: ":Alice_Travel_Agent"
      subject: ":Alice_Travel_Agent"
      shape: "pshapes:ContactInfoShape"
    - id: "http://www.example.org/tpod/graphs/graph-68"
      claimant: ":Dave"
      subject: ":Dave"
      shape: "pshapes:ContactInfoShape"
  tool:
    - id: "http://www.example.org/tpod/tools/tool-33"
      type: "form"
      formTopic: ":Kyoto_Trip_2027"
      graph:
        - id: "http://www.example.org/tpod/graphs/graph-69"
          claimant: ":Self"
          shape: "itineraryshapes:ItineraryShape"
        - id: "http://www.example.org/tpod/graphs/graph-70"
          claimant: ":Alice_Travel_Agent"
          shape: "itineraryshapes:ItineraryShape"
        - id: "http://www.example.org/tpod/graphs/graph-91"
          claimant: ":Dave"
          shape: "itineraryshapes:ItineraryShape"
---

## Graphs

<a id="graph-66"></a>
### Graph 66

#### Overview

This graph is one of the pod's three required `member` entries — Alice's own bare given-name claim (see YAML-6: `:Self` must be a member of every pod in the user's own tree, regardless of member count), extended with her social network link to Dave (mirroring the pattern used in graph 12's Alice–Bob connection) — this is what makes `:Dave` reachable per TTL-1, since he is otherwise referenced only via this pod's `member`/`tool`, not via a dedicated Immediate Family pod of his own (out of scope for this worked example).

#### Graph

```turtle
<!-- databook:id: alice-kyoto-trip-member-graph -->
<!-- databook:graph: http://www.example.org/tpod/graphs/graph-66#graph -->
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

:Dave rdf:type owl:NamedIndividual ,
               persona:Person ;
    <https://w3id.org/cco-domains/cco/ont00001879> [  # designated by → GivenName
        rdf:type cco:ent00000002 ;
        <https://w3id.org/cco-domains/cco/ont00001765> "Dave"
    ] .

:Self persona:hasSocialNetwork :Alice_Dave_Network .

:Alice_Dave_Network rdf:type owl:NamedIndividual ,
                             cco:ont00001183 ;  # Social Network
    rdfs:label "Alice Walker's Dave connection"@en ;
    <http://purl.obolibrary.org/obo/BFO_0000115> :Dave .  # has member part
```

<a id="graph-67"></a>
### Graph 67

#### Overview

This graph is another of the pod's three required `member` entries — an AI travel agent Alice invited to collaborate on planning this trip, joining as a real pod member (see README.md's Service Ontology section) rather than staying an invisible tool: it gets its own self-claimed member graph, exactly like a human member's, typed `service:PodAgent`. It answers to Dave as readily as to Alice — either can address it as "@ChatGPT", its `rdfs:label` — so it carries no `service:actsFor`; instead `service:sponsoredBy :Self` records that Alice pays for it. Behind it sit two pieces of software that are not pod members: its gateway (`:Alice_Travel_Gateway`, a `service:PodGateway`, whose host is not recorded) and the language model it uses (`:Alice_Travel_LLM`, a `service:ChatGPT`, hosted by OpenAI). A `service:Service` is never a `pod:creator` — Alice alone created this pod — but it is a legitimate `pod:claimant` and `pod:member` participant. Unlike a `service:ServiceProvider`, whose claims are attributed to the organization providing it, a pod agent claims under its own IRI: no organization stands behind it in this pod's relationship, OpenAI merely hosting its model.

#### Graph

```turtle
<!-- databook:id: alice-travel-agent-member-graph -->
<!-- databook:graph: http://www.example.org/tpod/graphs/graph-67#graph -->
@prefix : <http://www.example.org/tpod#> .
@prefix service: <http://mee.foundation/ontologies/service#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix persona: <http://mee.foundation/ontologies/persona#> .
@prefix cco: <https://w3id.org/cco-domains/cco/> .
@prefix o: <http://mee.foundation/ontologies/organization#> .

:Self rdf:type owl:NamedIndividual ,
               persona:Person ;
    <https://w3id.org/cco-domains/cco/ont00001879> [  # designated by → GivenName (ContactInfoShape)
        rdf:type cco:ent00000002 ;
        <https://w3id.org/cco-domains/cco/ont00001765> "Alice"
    ] .

:Alice_Travel_Agent rdf:type owl:NamedIndividual ,
                    service:PodAgent ;
    rdfs:label "ChatGPT"@en ;
    service:sponsoredBy :Self ;
    service:viaGateway :Alice_Travel_Gateway ;
    service:usesLLM :Alice_Travel_LLM .

:Alice_Travel_Gateway rdf:type owl:NamedIndividual ,
                      service:PodGateway .

:Alice_Travel_LLM rdf:type owl:NamedIndividual ,
                  service:ChatGPT ;
    service:hostedBy :OpenAI .

:OpenAI rdf:type owl:NamedIndividual ,
                 o:Organization ;
    rdfs:label "OpenAI"@en .
```

<a id="graph-68"></a>
### Graph 68

#### Overview

This graph is the pod's third required `member` entry — Dave's own self-claimed bare given-name persona, transmitted from Dave's own instance of the app to Alice's over the PDN once she invited him to this pod, the same "self-claimed member" pattern Bob Johnson's own graphs use. This third distinct `member` `subject` (alongside `:Self` and `:Alice_Travel_Agent`) is what makes the pod a three-member pod rather than a two-member pod.

#### Graph

```turtle
<!-- databook:id: dave-dave-member-graph -->
<!-- databook:graph: http://www.example.org/tpod/graphs/graph-68#graph -->
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
        <https://w3id.org/cco-domains/cco/ont00001765> "Dave"  # has text value
    ] .
```

<a id="graph-69"></a>
### Graph 69

#### Overview

This graph is one of the pod's three tool graphs — Alice's own basic claim identifying the trip itself, backing the pod's derived subject `:Kyoto_Trip_2027` with a real graph claimed by her directly (see YAML-4), distinct from her agent's own more substantive contribution ([graph 70](#graph-70)). Both tool graphs share the same subject but a different claimant — mirroring the Medical Appointment pod's two "Med. Appt mt." squares (see README.md's Representative Pods diagram), where one tool's topic is claimed from each side.

#### Graph

```turtle
<!-- databook:id: alice-kyoto-trip-tool-graph -->
<!-- databook:graph: http://www.example.org/tpod/graphs/graph-69#graph -->
@prefix : <http://www.example.org/tpod#> .
@prefix persona: <http://mee.foundation/ontologies/persona#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix itineraries: <http://mee.foundation/ontologies/itineraries#> .

:Kyoto_Trip_2027 rdf:type owl:NamedIndividual ,
                          itineraries:Itinerary ;
    rdfs:label "Kyoto Trip, Spring 2027"@en .
```

<a id="graph-70"></a>
### Graph 70

#### Overview

This graph is one of the pod's three tool graphs — Alice's travel agent's own evolving understanding of the trip, claimed by the agent rather than by Alice, Dave, or a third `p:Person`/`o:Organization`. This is the agent's single evolving graph — revised in place turn by turn as Alice and her agent go back and forth (see app-behavior.md's Agent Collaboration section), rather than a new graph per conversation turn. Typed `itineraries:Itinerary` (no existing CCO/domain class to multi-type alongside — there is no dedicated trip-planning domain ontology yet), validated by the `ItineraryShape` per-template SHACL shape, which requires only a human-readable label or description rather than any structured trip-planning fields.

#### Graph

```turtle
<!-- databook:id: alice-travel-agent-kyoto-trip-tool-graph -->
<!-- databook:graph: http://www.example.org/tpod/graphs/graph-70#graph -->
@prefix : <http://www.example.org/tpod#> .
@prefix persona: <http://mee.foundation/ontologies/persona#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix itineraries: <http://mee.foundation/ontologies/itineraries#> .

:Kyoto_Trip_2027 rdf:type owl:NamedIndividual ,
                          itineraries:Itinerary ;
    rdfs:comment "Draft itinerary, collaboratively refined turn by turn with Alice's own travel agent: cherry blossom season in Kyoto and Nara, proposed late-March dates, and a shortlist of ryokan lodging near Higashiyama."@en .
```

<a id="graph-91"></a>
### Graph 91

#### Overview

This graph is the pod's third tool graph — Dave's own contribution to the trip, claimed by him directly rather than routed through Alice or her travel agent. With this graph, the pod reaches `pod:formGraph`'s real upper bound: one graph per member, each with a distinct claimant (Self, the agent, and now Dave — see YAML-8), the same subject `:Kyoto_Trip_2027` claimed from all three sides at once.

#### Graph

```turtle
<!-- databook:id: dave-kyoto-trip-tool-graph -->
<!-- databook:graph: http://www.example.org/tpod/graphs/graph-91#graph -->
@prefix : <http://www.example.org/tpod#> .
@prefix persona: <http://mee.foundation/ontologies/persona#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix itineraries: <http://mee.foundation/ontologies/itineraries#> .

:Kyoto_Trip_2027 rdf:type owl:NamedIndividual ,
                          itineraries:Itinerary ;
    rdfs:comment "Dave's own requests for the trip: a day trip to Fushimi Inari Taisha, and at least one dinner reservation at a kaiseki restaurant in Gion."@en .
```
