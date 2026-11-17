---
id: http://www.example.org/tpod/pods/pod-55
title: "Honda"
type: pod-databook
version: 1.3.0
created: 2026-11-16
description: >
  Pod DataBook for the "Honda" pod (category tag: podcat:Vehicles) in Alice's pod space for Paula, where Alice keeps track of Paula's car. Its podcat:Vehicles tag means Paula's vehicles rather than Alice's own, whose RAV4 pod carries the same tag in her default space; the space is what tells the two apart. It is a one-member pod with one member entry about :Self, plus the Vehicle form tool podcat:Vehicles' template pod declares, about :Paula_Honda, Paula's car.
tpod:
  categoryTag:
    - "podcat:Vehicles"
  space:
    id: "http://www.example.org/tpod/spaces/space-2"
    name: "Paula Walker"
    root: "podcat:Person"
    subject: ":Paula_Walker"
  creator: ":Self"
  owner: ":Self"
  member:
    id: "http://www.example.org/tpod/graphs/graph-107"
    claimant: ":Self"
    subject: ":Self"
    shape: "pshapes:ContactInfoShape"
  tool:
    - id: "http://www.example.org/tpod/tools/tool-37"
      type: "form"
      formTopic: ":Paula_Honda"
      graph:
        - id: "http://www.example.org/tpod/graphs/graph-108"
          claimant: ":Self"
          shape: "vehicleshapes:VehicleShape"
---

## Graphs

<a id="graph-107"></a>
### Graph 107

#### Overview

This graph is the pod's required `member` entry, claimed by and about Alice: her given name, which `ContactInfoShape`, the `podcat:Vehicles` template's member shape, requires. Paula has no instance of the app and is not a member of the pod, so this stub is the only member entry.

#### Graph

```turtle
<!-- databook:id: paula-things-member-graph -->
<!-- databook:graph: http://www.example.org/tpod/graphs/graph-107#graph -->
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

<a id="graph-108"></a>
### Graph 108

#### Overview

This graph captures Alice's record of her mother Paula's car, a 2015 Honda Fit, and backs the pod's form tool, the one `podcat:Vehicles`' template declares, whose topic is `:Paula_Honda`. It follows the RAV4 pod's graph 63, validated by `vehicles:Vehicle`'s SHACL shape (`other/shacl/vehicles-shacl.ttl`'s `:VehicleShape`): vehicle type (`vehicles:Car`), make and model (real Wikidata individuals vendored in `project_files/wikidata-vehicle-makes-subset.ttl`/`project_files/wikidata-vehicle-models-subset.ttl`), model year, color and body type. `:Paula_Walker persona:hasVehicle :Paula_Honda` says whose car it is, which the pod's space already makes plain at the pod level: its `podcat:Vehicles` tag means Paula's vehicles. Alice is the claimant.

#### Graph

```turtle
<!-- databook:id: paula-things-graph -->
<!-- databook:graph: http://www.example.org/tpod/graphs/graph-108#graph -->
@prefix : <http://www.example.org/tpod#> .
@prefix persona: <http://mee.foundation/ontologies/persona#> .
@prefix vehicles: <http://mee.foundation/ontologies/vehicles#> .
@prefix wd: <http://www.wikidata.org/entity/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

:Paula_Walker rdf:type owl:NamedIndividual ,
                       persona:Person .

:Paula_Honda rdf:type owl:NamedIndividual ,
                      vehicles:Vehicle ;
    rdfs:label "Paula Walker's Honda"@en ;

    vehicles:hasVehicleType vehicles:Car ;
    vehicles:hasMake wd:Q9584 ;      # Honda
    vehicles:hasModel wd:Q1135125 ;  # Honda Fit
    vehicles:modelYear "2015"^^xsd:gYear ;
    vehicles:color "Blue" ;
    vehicles:bodyType "Hatchback" .

:Paula_Walker persona:hasVehicle :Paula_Honda .
```
