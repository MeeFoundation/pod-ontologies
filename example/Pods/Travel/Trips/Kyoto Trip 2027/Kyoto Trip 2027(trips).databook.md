---
id: http://www.example.org/tpod/pods/pod-47
title: "Kyoto Trip 2027"
type: pod-databook
version: 2.0.0
created: 2026-08-30
description: >
  Pod DataBook for folder "Kyoto Trip 2027" (pod:category: podcat:Trips, reusing its parent "Trips"
  pod's own origin), nested under "Travel" > "Trips". A user-defined instance folder for a
  specific trip Alice is planning with her spouse Dave. A two-member pod, Alice and Dave, each
  with a self-claimed member entry (graph-66, graph-68). The trip itself is backed by two tool
  graphs sharing one subject (:Kyoto_Trip_2027), one per member, each with a distinct claimant —
  Alice's own draft itinerary (graph-69), worked out with her personal agent and claimed by her,
  and Dave's own contribution (graph-91) — reaching pod:formGraph's real upper bound (one graph
  per member, see YAML-8) and mirroring how a tool's topic may be claimed from more than one side
  (see the Medical Appointment pod's two "Med. Appt mt." squares in README.md's Representative
  Pods diagram).
tpod:
  category: "podcat:Trips"
  creator: ":Self"
  owner: ":Self"
  member:
    - id: "http://www.example.org/tpod/graphs/graph-66"
      claimant: ":Self"
      subject: ":Self"
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
        - id: "http://www.example.org/tpod/graphs/graph-91"
          claimant: ":Dave"
          shape: "itineraryshapes:ItineraryShape"
---

## Graphs

<a id="graph-66"></a>
### Graph 66

#### Overview

This graph is one of the pod's two required `member` entries — Alice's own bare given-name claim (see YAML-6: `:Self` must be a member of every pod in the user's own tree, regardless of member count), extended with her social network link to Dave (mirroring the pattern used in graph 12's Alice–Bob connection) — this is what makes `:Dave` reachable per TTL-1, since he is otherwise referenced only via this pod's `member`/`tool`, not via a dedicated Immediate Family pod of his own (out of scope for this worked example).

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

<a id="graph-68"></a>
### Graph 68

#### Overview

This graph is the pod's second required `member` entry — Dave's own self-claimed bare given-name persona, transmitted from Dave's own instance of the app to Alice's over the PDN once she invited him to this pod, the same "self-claimed member" pattern Bob Johnson's own graphs use. This second distinct `member` `subject`, alongside `:Self`, is what makes the pod a two-member pod rather than a single-member one.

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

This graph is one of the pod's two tool graphs — Alice's own claim about the trip itself, backing the pod's derived subject `:Kyoto_Trip_2027` with a real graph claimed by her directly (see YAML-4). It holds her draft itinerary, which she works out turn by turn with her personal agent in her private agent chat (see app-behavior.md's Personal Agent section). The agent appears nowhere in the graph: it writes as Alice, so the claim is hers, revised in place rather than replaced each turn. Typed `itineraries:Itinerary`, validated by the `ItineraryShape` per-template SHACL shape, which requires only a human-readable label or description rather than any structured trip-planning fields. This graph and Dave's ([graph 91](#graph-91)) share the same subject but a different claimant — mirroring the Medical Appointment pod's two "Med. Appt mt." squares (see README.md's Representative Pods diagram), where one tool's topic is claimed from each side.

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
    rdfs:label "Kyoto Trip, Spring 2027"@en ;
    rdfs:comment "Draft itinerary, refined turn by turn with Alice's personal agent: cherry blossom season in Kyoto and Nara, proposed late-March dates, and a shortlist of ryokan lodging near Higashiyama."@en .
```

<a id="graph-91"></a>
### Graph 91

#### Overview

This graph is the pod's second tool graph — Dave's own contribution to the trip, claimed by him directly rather than routed through Alice. With this graph, the pod reaches `pod:formGraph`'s real upper bound: one graph per member, each with a distinct claimant (Self and Dave — see YAML-8), the same subject `:Kyoto_Trip_2027` claimed from both sides at once.

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
