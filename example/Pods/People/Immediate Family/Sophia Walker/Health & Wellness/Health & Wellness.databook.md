---
id: http://www.example.org/tpod/pods/pod-13
title: "Health & Wellness"
type: pod-databook
version: 1.4.0
created: 2026-07-10
description: >
  Pod DataBook for folder "Health & Wellness" (pod:category: podcat:HealthWellness). It is a one-member pod with one member entry about :Self and one graph about :Sophia_Walker (the pod's subject).
tpod:
  category: "podcat:HealthWellness"
  creator: ":Self"
  owner: ":Self"
  member:
    id: "http://www.example.org/tpod/graphs/graph-35"
    claimant: ":Self"
    subject: ":Self"
    shape: "pshapes:ContactInfoShape"
  tool:
    - type: "form"
      formTopic: ":Sophia_Walker"
      graph:
        - id: "http://www.example.org/tpod/graphs/graph-17"
          claimant: ":Self"
          shape: "pshapes:HealthWellnessShape"
---

## Graphs

<a id="graph-35"></a>
### Graph 35

#### Overview

This graph captures Alice's own bare identity claim (just her given name) — the pod's one required `member` entry. A pod with a single `member` entry in the user's own category-pod tree always has `:Self` as that member (the user either created the pod themselves or received it via sharing — either way `:Self` participates), regardless of what the pod's `subject` is. Alice is both the claimant and the subject.

#### Graph

```turtle
<!-- databook:id: alice-health-wellness-member-graph -->
<!-- databook:graph: http://www.example.org/tpod/graphs/graph-35#graph -->
@prefix : <http://www.example.org/tpod#> .
@prefix cco: <https://w3id.org/cco-domains/cco/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix persona: <http://mee.foundation/ontologies/persona#> .

:Self rdf:type owl:NamedIndividual ,
               persona:Person .

:Self <https://w3id.org/cco-domains/cco/ont00001879> [  # designated by → GivenName
    rdf:type cco:ent00000002 ;  # GivenName
    <https://w3id.org/cco-domains/cco/ont00001765> "Alice"  # has text value
] .
```

<a id="graph-17"></a>
### Graph 17

#### Overview

This graph captures Sophia Walker's physical body characteristics — properties that are intrinsic to her as a person and do not belong to any particular institutional or social graph — as recorded by Alice. Height is recorded as a CCO Height quality, measured by a RatioMeasurementICE ("is a ratio measurement of") whose value and unit (52 inches) sit on a separate Information Bearing Entity that is carrier of it. Eye color is modeled as Sophia bearing a BlueEyeColor quality directly. Hair color is borne by her ScalpHair continuant part. Alice is the claimant; Sophia is the pod's `subject` but, since this pod now has a real member entry (graph 35, above) about Alice herself, Sophia's graph is held by the pod's form tool rather than being one of the required `member` entries.

#### Graph

```turtle
<!-- databook:id: sophia-health-graph -->
<!-- databook:graph: http://www.example.org/tpod/graphs/graph-17#graph -->
@prefix : <http://www.example.org/tpod#> .
@prefix persona: <http://mee.foundation/ontologies/persona#> .
@prefix cco: <https://w3id.org/cco-domains/cco/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

:Sophia_Walker rdf:type owl:NamedIndividual ,
               persona:Person .

:Sophia_Walker rdfs:comment "Sophia Walker's physical body characteristics."@en ;

    # ── Height ───────────────────────────────────────────────────────────────

    <http://purl.obolibrary.org/obo/BFO_0000196> :Sophia_Height ;

    # ── Eye color ────────────────────────────────────────────────────────────

    <http://purl.obolibrary.org/obo/BFO_0000196> [  # bearer of → Eye Color
        rdf:type cco:ent00000040 ;  # Blue Eye Color
        rdfs:comment "Eye color: Blue"@en
    ] ;

    # ── Hair ─────────────────────────────────────────────────────────────────

    <http://purl.obolibrary.org/obo/BFO_0000178> [  # has continuant part → Scalp Hair
        rdf:type cco:ont00000058 ;  # Scalp Hair
        <http://purl.obolibrary.org/obo/BFO_0000196> [  # bearer of → Hair Color
            rdf:type cco:ont00000026 ;  # Hair Color
            <https://w3id.org/cco-domains/cco/ont00001765> "Brown" ;
            rdfs:comment "Hair color: Brown"@en
        ]
    ] .


:Sophia_Height rdf:type owl:NamedIndividual ,
                       <https://w3id.org/cco-domains/cco/ont00000967> ;  # Height (CCO Quality)
    rdfs:label "Sophia Walker's height"@en .

:Sophia_Height_Measurement rdf:type owl:NamedIndividual ,
                                   <https://w3id.org/cco-domains/cco/ont00001022> ;  # Ratio Measurement ICE
    <https://w3id.org/cco-domains/cco/ont00001983> :Sophia_Height .  # is a ratio measurement of

:Sophia_Height_Measurement_Bearer rdf:type owl:NamedIndividual ,
                                   <https://w3id.org/cco-domains/cco/ont00000253> ;  # Information Bearing Entity
    <http://purl.obolibrary.org/obo/BFO_0000101> :Sophia_Height_Measurement ;  # is carrier of
    <https://w3id.org/cco-domains/cco/ont00001863> <https://w3id.org/cco-domains/cco/ont00001677> ;  # uses measurement unit: Inch
    <https://w3id.org/cco-domains/cco/ont00001769> "52"^^xsd:decimal .  # has decimal value
```
