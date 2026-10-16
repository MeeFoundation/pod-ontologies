---
id: http://www.example.org/tpod/pods/pod-40
title: "Medical"
type: pod-databook
version: 2.3.0
created: 2026-08-21
description: >
  Pod DataBook for folder "Medical" (pod:category: podcat:PetsMedical). It is a two-member pod, shared by Alice with Paula, with two members (about :Self and :Paula_Walker) and one graph about :Ginger, Alice's cat (the pod's subject).
tpod:
  category: "podcat:PetsMedical"
  creator: ":Self"
  owner: ":Self"
  userTag:
    - "Ginger"
  member:
    - id: "http://www.example.org/tpod/graphs/graph-33"
      claimant: ":Self"
      subject: ":Self"
      shape: "pshapes:ContactInfoShape"
    - id: "http://www.example.org/tpod/graphs/graph-57"
      claimant: ":Paula_Walker"
      subject: ":Paula_Walker"
      shape: "pshapes:ContactInfoShape"
  tool:
    - type: "form"
      formTopic: ":Ginger"
      graph:
        - id: "http://www.example.org/tpod/graphs/graph-32"
          claimant: ":Self"
          shape: "petshapes:PetMedicationRecordShape"
---

## Graphs

<a id="graph-33"></a>
### Graph 33

#### Overview

This graph is one of the pod's two `member` entries, satisfying the two-member baseline alongside graph 57 (Paula's own claim, below). Alice is both the claimant and the subject. It carries her given name, plus a minimal organization name and email, so `:Self` satisfies the `ContactInfoShape` every templated pod's `member` content is now expected to conform to (`pod:memberShape`) — no longer deliberately empty now that this requirement applies.

#### Graph

```turtle
<!-- databook:id: alice-ginger-medications-member-graph -->
<!-- databook:graph: http://www.example.org/tpod/graphs/graph-33#graph -->
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

<a id="graph-57"></a>
### Graph 57

#### Overview

This pod was created by Alice and later shared with Paula, making the pod a two-member pod. This graph is Paula's own identity claim — her given name is what actually satisfies the `ContactInfoShape` every templated pod's `member` content is now expected to conform to (`pod:memberShape`); the organization name and phone below are optional extra detail, not a requirement — the pod's second `member` entry, satisfying the two-member baseline alongside graph 33 (Alice's own claim, above). Paula is both the claimant and the subject.

#### Graph

```turtle
<!-- databook:id: paula-ginger-medications-member-graph -->
<!-- databook:graph: http://www.example.org/tpod/graphs/graph-57#graph -->
@prefix : <http://www.example.org/tpod#> .
@prefix persona: <http://mee.foundation/ontologies/persona#> .
@prefix cco: <https://w3id.org/cco-domains/cco/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .

:Paula_Walker rdf:type owl:NamedIndividual ,
               persona:Person ;
    cco:ont00001879 [  # designated by → GivenName
        rdf:type cco:ent00000002 ;  # GivenName
        cco:ont00001765 "Paula"  # has text value
    ] ;

    cco:ont00001879 [  # designated by → OrganizationName (ContactInfoShape)
        rdf:type cco:ent00000047 ;
        cco:ont00001765 "Retired"
    ] ;

    cco:ont00001879 [  # designated by → Phone (ContactInfoShape)
        rdf:type cco:ent00000023 ;
        cco:ont00001765 "+19165550172"
    ] .
```

<a id="graph-32"></a>
### Graph 32

#### Overview

This graph captures Alice's record of her cat Ginger's medications — an amoxicillin/clavulanate course prescribed after a minor infection, and an ongoing daily joint supplement. Validated by the `PetMedications` per-template SHACL shapes (`other/shacl/pets-shacl.ttl`). Alice is the claimant; Ginger is the pod's `subject` but, since she has no `p:Person` individual of her own, her graph is held by the pod's form tool rather than being one of the required `member` entries (graphs 33 and 57, above, fill those slots instead). Each medication's active ingredient(s) are cited by real ChEBI class IRIs, its tablet/liquid dosage form and amount by DrOn/CCO terms, and its schedule by a DrOn drug-administration individual carrying a BFO temporal interval — see `pets:Medication`'s `rdfs:comment` (`other/pets.ttl`) for the full reuse rationale.

#### Graph

```turtle
<!-- databook:id: ginger-medications-graph -->
<!-- databook:graph: http://www.example.org/tpod/graphs/graph-32#graph -->
@prefix : <http://www.example.org/tpod#> .
@prefix pets: <http://mee.foundation/ontologies/pets#> .
@prefix cco: <https://w3id.org/cco-domains/cco/> .
@prefix obo: <http://purl.obolibrary.org/obo/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

:Ginger rdf:type owl:NamedIndividual ;
    rdfs:label "Ginger (Alice's cat)"@en .

:Ginger_Medications rdf:type owl:NamedIndividual ,
               pets:PetMedicationRecord ;
    rdfs:label "Ginger's Medications"@en ;
    rdfs:comment "Alice's record of medications for her cat, Ginger."@en ;

    pets:hasMedication :Ginger_Medication_Clavamox ,
                        :Ginger_Medication_Glucosamine .

:Ginger_Medication_Clavamox rdf:type owl:NamedIndividual ,
               pets:Medication ;
    rdfs:label "Amoxicillin/Clavulanate (Clavamox)"@en ;

    pets:hasActiveIngredient <http://purl.obolibrary.org/obo/CHEBI_2676> ,   # amoxicillin
                              <http://purl.obolibrary.org/obo/CHEBI_48947> ; # clavulanic acid

    pets:hasDoseForm <http://purl.obolibrary.org/obo/DRON_00000022> ;  # drug tablet

    pets:medicationBrandName "Clavamox" ;
    pets:medicationManufacturer "Zoetis" ;

    pets:hasDosageAmount :Ginger_Medication_Clavamox_Dosage ;
    pets:hasAdministration :Ginger_Medication_Clavamox_Administration .

:Ginger_Medication_Clavamox_Dosage rdf:type owl:NamedIndividual ,
               pets:DosageAmount ;
    rdfs:comment "1 tablet — a count of discrete dose-form units (see hasDoseForm above), not a measured quantity, so no 'uses measurement unit' link (per UCUM's own stance that 'tablet' is not a real unit)."@en .

:Ginger_Medication_Clavamox_Dosage_Bearer rdf:type owl:NamedIndividual ,
               cco:ont00000253 ;                 # Information Bearing Entity
    obo:BFO_0000101 :Ginger_Medication_Clavamox_Dosage ;  # is carrier of
    cco:ont00001773 1 .                          # has integer value

:Ginger_Medication_Clavamox_Administration rdf:type owl:NamedIndividual ,
               pets:MedicationAdministration ;
    pets:medicationFrequencyPerDay "2" ;
    <http://purl.obolibrary.org/obo/BFO_0000199> :Ginger_Medication_Clavamox_Interval .  # occupies temporal region

:Ginger_Medication_Clavamox_Interval rdf:type owl:NamedIndividual ,
               <http://purl.obolibrary.org/obo/BFO_0000038> ;  # one-dimensional temporal region
    cco:ent00000017 "2026-08-10"^^xsd:date ;   # has start date
    cco:ent00000018 "2026-08-20"^^xsd:date .   # has end date — a completed short course

:Ginger_Medication_Glucosamine rdf:type owl:NamedIndividual ,
               pets:Medication ;
    rdfs:label "Glucosamine/Chondroitin"@en ;

    pets:hasActiveIngredient <http://purl.obolibrary.org/obo/CHEBI_5417> ,   # glucosamine
                              <http://purl.obolibrary.org/obo/CHEBI_37397> ; # chondroitin sulfate

    pets:hasDosageAmount :Ginger_Medication_Glucosamine_Dosage ;
    pets:hasAdministration :Ginger_Medication_Glucosamine_Administration .

:Ginger_Medication_Glucosamine_Dosage rdf:type owl:NamedIndividual ,
               pets:DosageAmount ;
    rdfs:comment "1 teaspoon — a true measured liquid quantity, so it carries a real CCO measurement unit (unlike the tablet count above)."@en .

:Ginger_Medication_Glucosamine_Dosage_Bearer rdf:type owl:NamedIndividual ,
               cco:ont00000253 ;                 # Information Bearing Entity
    obo:BFO_0000101 :Ginger_Medication_Glucosamine_Dosage ;  # is carrier of
    cco:ont00001769 "1.0"^^xsd:decimal ;         # has decimal value
    cco:ont00001863 cco:ont00001573 .            # uses measurement unit → Teaspoon Measurement Unit

:Ginger_Medication_Glucosamine_Administration rdf:type owl:NamedIndividual ,
               pets:MedicationAdministration ;
    pets:medicationFrequencyPerDay "1" ;
    <http://purl.obolibrary.org/obo/BFO_0000199> :Ginger_Medication_Glucosamine_Interval .  # occupies temporal region

:Ginger_Medication_Glucosamine_Interval rdf:type owl:NamedIndividual ,
               <http://purl.obolibrary.org/obo/BFO_0000038> ;  # one-dimensional temporal region
    cco:ent00000017 "2026-01-15"^^xsd:date .   # has start date — no end date: ongoing/current
```
