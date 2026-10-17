---
id: http://www.example.org/tpod/pods/pod-44
title: "RAV4"
type: pod-databook
version: 1.1.0
created: 2026-08-29
description: >
  Pod DataBook for folder "RAV4" (pod:category: podcat:Vehicles). A user-defined instance folder for
  Alice's car, nested under the generic Vehicles category — mirroring how "Ginger" reuses its parent
  "Pets" folder's own origin class rather than being Custom. It is a one-member pod with one member
  entry about :Self and one graph about :Alice_RAV4 (the pod's subject), typed vehicles:Vehicle and
  carrying its vehicle type, make, model, model year, VIN, color, body type, fuel type, drive wheel
  configuration, odometer reading, and engine specification.
tpod:
  category: "podcat:Vehicles"
  creator: ":Self"
  owner: ":Self"
  member:
    id: "http://www.example.org/tpod/graphs/graph-62"
    claimant: ":Self"
    subject: ":Self"
    shape: "pshapes:ContactInfoShape"
  tool:
    - id: "http://www.example.org/tpod/tools/tool-29"
      type: "form"
      formTopic: ":Alice_RAV4"
      graph:
        - id: "http://www.example.org/tpod/graphs/graph-63"
          claimant: ":Self"
          shape: "vehicleshapes:VehicleShape"
---

## Graphs

<a id="graph-62"></a>
### Graph 62

#### Overview

This graph is the pod's one required `member` entry — a pod with a single `member` entry in the user's own category-pod tree always has `:Self` as that member (see YAML-6), regardless of what the pod's `subject` is — here, the RAV4 itself. Alice is both the claimant and the subject. It carries her given name, plus a minimal organization name and email, so `:Self` satisfies the `ContactInfoShape` every templated pod's `member` content is now expected to conform to (`pod:memberShape`) — no longer deliberately empty now that this requirement applies.

#### Graph

```turtle
<!-- databook:id: alice-rav4-member-graph -->
<!-- databook:graph: http://www.example.org/tpod/graphs/graph-62#graph -->
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

<a id="graph-63"></a>
### Graph 63

#### Overview

This graph captures Alice's basic claim about her car itself — just enough to back the pod's `subject: ":Alice_RAV4"` with a real graph (see YAML-4) — and, validated by `vehicles:Vehicle`'s SHACL shape (`other/shacl/vehicles-shacl.ttl`'s `:VehicleShape`), identifies its vehicle type (`vehicles:Car`, class-value-punned), make and model (both real Wikidata individuals vendored in `project_files/wikidata-vehicle-makes-subset.ttl`/`project_files/wikidata-vehicle-models-subset.ttl`), model year, VIN, color, body type, fuel type, drive wheel configuration, current odometer reading (a `vehicles:OdometerReading` measurement whose decimal value and unit sit on a separate CCO Information Bearing Entity that is carrier of it, the same two-individual pattern `pets:BodyWeight`/`pets:DosageAmount` use), and engine specification. `:Self persona:hasVehicle :Alice_RAV4` closes the loop from the Person side.

#### Graph

```turtle
<!-- databook:id: alice-rav4-subject-graph -->
<!-- databook:graph: http://www.example.org/tpod/graphs/graph-63#graph -->
@prefix : <http://www.example.org/tpod#> .
@prefix persona: <http://mee.foundation/ontologies/persona#> .
@prefix vehicles: <http://mee.foundation/ontologies/vehicles#> .
@prefix wd: <http://www.wikidata.org/entity/> .
@prefix cco: <https://w3id.org/cco-domains/cco/> .
@prefix obo: <http://purl.obolibrary.org/obo/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

:Self rdf:type owl:NamedIndividual ,
               persona:Person .

:Alice_RAV4 rdf:type owl:NamedIndividual ,
                     vehicles:Vehicle ;
    rdfs:label "Alice Walker's RAV4"@en ;

    vehicles:hasVehicleType vehicles:Car ;
    vehicles:hasMake wd:Q53268 ;   # Toyota
    vehicles:hasModel wd:Q819982 ;  # Toyota RAV4
    vehicles:modelYear "2022"^^xsd:gYear ;
    vehicles:vehicleIdentificationNumber "JT3RWRFV1NU012345" ;
    vehicles:color "Silver" ;
    vehicles:bodyType "SUV" ;
    vehicles:fuelType "Gasoline" ;
    vehicles:driveWheelConfiguration "AWD" ;
    vehicles:hasOdometerReading :Alice_RAV4_Odometer ;
    vehicles:hasEngineSpecification :Alice_RAV4_Engine .

:Alice_RAV4_Odometer rdf:type owl:NamedIndividual ,
                     vehicles:OdometerReading ;
    rdfs:comment "Alice's RAV4's odometer reading as of its most recent service."@en .

:Alice_RAV4_Odometer_Bearer rdf:type owl:NamedIndividual ,
                     cco:ont00000253 ;           # Information Bearing Entity
    obo:BFO_0000101 :Alice_RAV4_Odometer ;       # is carrier of
    cco:ont00001769 "32150.0"^^xsd:decimal ;     # has decimal value
    cco:ont00001863 cco:ont00001433 .            # uses measurement unit → Mile Measurement Unit

:Alice_RAV4_Engine rdf:type owl:NamedIndividual ,
                     vehicles:EngineSpecification ;
    vehicles:engineType "Internal Combustion" ;
    vehicles:engineDisplacementLiters "2.5"^^xsd:decimal .

:Self persona:hasVehicle :Alice_RAV4 .
```
