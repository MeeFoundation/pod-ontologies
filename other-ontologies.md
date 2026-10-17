# Other Domain Ontologies

This document describes the `other/` ontologies: a growing family of small, independent peer ontologies for domains a person merely *has* — a pet, a vehicle, an identity document, an online account, a residence — rather than *is*. It is a companion to [README.md](README.md), which describes the core model these ontologies plug into: pods and their tools, the pod categories, and the Persona, Organization and Service ontologies.

What sends a term here rather than to `persona.ttl` is its subject. Every property in an `other/*.ttl` file describes a record, document or possession — an independent thing with an existence of its own — never the `p:Person` themselves; a term whose subject is the person belongs in `persona.ttl` or, failing that, in a `persona-ext/` extension such as the [Directory Profile Ontology](README.md#directory-profile-ontology). `persona.ttl` holds only the thin `hasX` link property into each domain that needs one (e.g. `p:hasPet`), referenced by name with no `owl:imports` in either direction. Content from these ontologies reaches a pod only through a tool's own `pod:formTopic`, never through `pod:member` (see [Tools](README.md#tools) in README.md). Each ontology is paired with a SHACL shapes file in `other/shacl/`; the form shapes among them are listed in README.md's [Form Shapes](README.md#form-shapes).

Throughout this document we use these short-hands, in addition to those [README.md](README.md) defines (`pod:`, `p:`, `o:`, `s:` and others):

- `pets:` for the `other/pets.ttl` namespace (`http://mee.foundation/ontologies/pets#`) — see [Pets Ontology](#pets-ontology)
- `v:` for the `other/vehicles.ttl` namespace (`http://mee.foundation/ontologies/vehicles#`) — see [Vehicles Ontology](#vehicles-ontology)
- `idoc:` for the `other/identity-documents.ttl` namespace (`http://mee.foundation/ontologies/identity-documents#`) — see [Identity Documents Ontology](#identity-documents-ontology)
- `ma:` for the `other/medical-appointments.ttl` namespace (`http://mee.foundation/ontologies/medical-appointments#`) — see [Medical Appointments Ontology](#medical-appointments-ontology)
- `sa:` for the `other/service-accounts.ttl` namespace (`http://mee.foundation/ontologies/service-accounts#`) — see [Service Accounts Ontology](#service-accounts-ontology)
- `banking:` for the `other/banking.ttl` namespace (`http://mee.foundation/ontologies/banking#`) — see [Banking Ontology](#banking-ontology)
- `residences:` for the `other/residences.ttl` namespace (`http://mee.foundation/ontologies/residences#`) — see [Residences Ontology](#residences-ontology)
- `itineraries:` for the `other/itineraries.ttl` namespace (`http://mee.foundation/ontologies/itineraries#`) — see [Itineraries Ontology](#itineraries-ontology)
- `education:` for the `other/education.ttl` namespace (`http://mee.foundation/ontologies/education#`) — see [Education Ontology](#education-ontology)
- `sources:` for the `other/sources.ttl` namespace (`http://mee.foundation/ontologies/sources#`) — see [Sources Ontology](#sources-ontology)

For worked examples of these ontologies in use, see [example.md](example.md).

## Pets Ontology

The Pets ontology (`other/pets.ttl`) is the first of this project's `other/` peer ontologies (see also the [Vehicles Ontology](#vehicles-ontology)) — small, mostly-vendored ontologies for domains a person merely *has* (a pet, a vehicle) rather than *is*. Keeping this content out of `persona.ttl` means that file stays scoped strictly to a person's own identity; `persona.ttl` holds only the thin `p:hasPet` link (domain `p:Person`, range `pets:Pet`, referenced by name — see [Possession-Related Classes and Properties](README.md#possession-related-classes-and-properties)) connecting a person to this ontology's own classes.

`pets:Pet` and `pets:PetMedicationRecord` are each independent template type label classes, the same kind every other `other/*.ttl` peer ontology defines (see [Persona Templates](README.md#persona-templates) in README.md) — an individual in a graph body is typed with one of these classes directly via `rdf:type`, regardless of what shape validates it.

Throughout this section, `pets:` is short for the `pets:` namespace (`http://mee.foundation/ontologies/pets#`).

### Pet-Related Classes and Properties

This section describes the classes and properties, defined in `other/pets.ttl`, that identify a pet — its name, what kind of animal it is, and, optionally, its birth date, current body weight, sex, and spay/neuter status.

**Classes:**

- `pets:Pet` — template label for a graph that identifies a pet, and also the actual `rdf:type` of the pet individual itself (a pet has no `p:Person` individual of its own — see `p:hasPet` above).
- `pets:BodyWeight` — a pet's body weight as of a single current measurement (not a weigh-in history); a CCO Ratio Measurement Information Content Entity (`cco:ont00001022`); the decimal value and unit sit on a separate Information Bearing Entity (`cco:ont00000253`) that is carrier of it (`obo:BFO_0000101`), the same two-individual style `pets:DosageAmount` uses.

**Properties:**

- `pets:name` — the pet's own name (`xsd:string`); required, exactly one value. A plain string property, not the CCO designated-by/Designative-Name machinery used for a *person's* name — a pet has no FullName/GivenName/FamilyName structure to model.
- `pets:hasSpecies` — links a `pets:Pet` directly to an [NCBI Taxonomy](https://www.ncbi.nlm.nih.gov/taxonomy) (NCBITaxon) class IRI (e.g. `NCBITaxon:9685` for *Felis catus*, the domestic cat); required, exactly one value.
- `pets:hasBreed` — links a `pets:Pet` directly to a [VBO](https://github.com/monarch-initiative/vertebrate-breed-ontology) (Vertebrate Breed Ontology) class IRI (e.g. `VBO:0100221` "Siamese (Cat)"); optional, at most one value. Assert one of VBO's own per-species "Mixed Breed" classes (e.g. `VBO:0100262` "Mixed Breed (Cat)") when the pet is known or assumed to be a non-purebred mixture; omit the property entirely when breed is simply not recorded at all.
- `pets:birthDate` — the pet's date of birth; optional, at most one value, and — unlike a strict single datatype — accepts either a full `xsd:date` (e.g. `"2020-06-15"`) when known exactly, or a bare `xsd:gYear` (e.g. `"2020"`) when only the approximate year is known (common for adopted/rescue pets), mirroring `p:anniversaryDate`'s own dual-precision (`xsd:date`/`xsd:gMonthDay`) treatment.
- `pets:hasBodyWeight` — links a `pets:Pet` to its `pets:BodyWeight` individual; optional, at most one value. The linked `pets:BodyWeight`'s bearer carries exactly one `cco:ont00001769` ("has decimal value") and exactly one `cco:ont00001863` ("uses measurement unit") pointing at a real CCO Measurement Unit individual (e.g. `cco:ont00001477` "Kilogram Measurement Unit" or `cco:ont00001728` "Pound Measurement Unit") — unlike `pets:DosageAmount`, the unit here is required, since a bare number alone is meaningless for a weight.
- `pets:sex` — the pet's biological sex (`xsd:string`); optional, at most one value, constrained by SHACL to exactly `"Male"` or `"Female"`.
- `pets:isSpayedOrNeutered` — whether the pet has been surgically sterilized (`xsd:boolean`); optional, at most one value. A single boolean rather than two sex-specific properties, since `pets:sex` already records which term (spayed vs. neutered) applies.

### Medication-Related Classes and Properties

This section describes the classes and properties, all defined in `other/pets.ttl`, that model a single medication entry — what drug, how much, and how often — reusing external vocabulary wherever one fits rather than inventing flat strings.

**Classes:**

- `pets:PetMedicationRecord` — template label for a graph that carries a pet's list of medications, and also the class of the record individual itself (a pet has no `p:Person` individual of its own, so `pets:hasMedication` links hang off this record rather than off a person).
- `pets:Medication` — a single medication entry: what drug, how much, and how often.
- `pets:DosageAmount` — how much of a `pets:Medication` is given per dose; a CCO Quality Specification (`cco:ont00000575`, a Directive Information Content Entity — a dose is an instruction, not a measurement of something observed); the value (and unit, when it is a measured quantity) sit on a separate Information Bearing Entity (`cco:ont00000253`) that is carrier of it (`obo:BFO_0000101`).
- `pets:MedicationAdministration` — how often, and over what period, a `pets:Medication` is given; subclass of DrOn's "drug administration" process class (`DRON:00000031`).

**Properties:**

- `pets:hasMedication` — links a `pets:PetMedicationRecord` to one of its `pets:Medication` entries (domain `pets:PetMedicationRecord`, range `pets:Medication`); repeatable.
- `pets:hasActiveIngredient` — links a `pets:Medication` directly to a ChEBI chemical-substance class IRI (e.g. `CHEBI:2676` for amoxicillin); repeatable for combination drugs.
- `pets:hasDoseForm` — links a `pets:Medication` to a DrOn dose-form class IRI (e.g. `DRON:00000022` "drug tablet"); omitted for a true measured quantity (e.g. a teaspoon of liquid) rather than a count of discrete units.
- `pets:hasDosageAmount` — links a `pets:Medication` to its `pets:DosageAmount` (domain `pets:Medication`, range `pets:DosageAmount`).
- `pets:hasAdministration` — links a `pets:Medication` to its `pets:MedicationAdministration` (domain `pets:Medication`, range `pets:MedicationAdministration`).
- `pets:medicationFrequencyPerDay` — free-text frequency, e.g. `"2"` or `"as needed"` (domain `pets:MedicationAdministration`).
- `pets:medicationBrandName` — free-text marketed brand name, e.g. `"Clavamox"` (domain `pets:Medication`) — kept as a plain string since DrOn embeds brand names only inside auto-generated RxNorm product-class labels, not as a reusable property.
- `pets:medicationManufacturer` — free-text manufacturer name, e.g. `"Zoetis"` (domain `pets:Medication`) — kept as a plain string since DrOn has no manufacturer/labeler class.
- `pets:medicationDuration` — free-text alternative to a fixed end date, e.g. `"10 days"` (domain `pets:Medication`), for courses with no fixed calendar end date.

`pets:DosageAmount`'s bearer carries exactly one of CCO's `cco:ont00001769` ("has decimal value") or `cco:ont00001773` ("has integer value"), and optionally `cco:ont00001863` ("uses measurement unit") pointing at a CCO Measurement Unit individual (e.g. "Teaspoon Measurement Unit", `cco:ont00001573`) — omitted for a count of discrete dose-form units. `pets:MedicationAdministration` carries `pets:medicationFrequencyPerDay` plus exactly one `BFO_0000199` ("occupies temporal region") link to a `BFO_0000038` temporal-interval individual carrying `cco:ent00000017`/`cco:ent00000018` ("has start/end date") — the same `AddressDesignation` temporal-interval pattern used for address history (see [Modeling Details](README.md#modeling-details) in README.md); an absent end date means the medication is ongoing.

### Reused External Vocabulary (Pets)

The external ontologies reused above, and one deliberately not used:

- **[NCBI Taxonomy](https://www.ncbi.nlm.nih.gov/taxonomy) (NCBITaxon)** — the standard taxonomic identifier for a species. A hand-curated subset covering 33 common pet species — mammals (cat, dog, rabbit, guinea pig, golden hamster, gerbil, chinchilla, ferret, hedgehog, fancy rat, fancy mouse), birds (budgerigar, cockatiel, canary, lovebird, African grey parrot, zebra finch), reptiles/amphibians (red-eared slider, leopard gecko, bearded dragon, ball python, corn snake, green iguana, White's tree frog, axolotl), and aquarium fish (goldfish, betta, zebrafish, Japanese rice fish, guppy, neon tetra, angelfish, koi) — is vendored at `project_files/ncbitaxon-subset.ttl` and `owl:import`ed from `other/pets.ttl`; NCBITaxon's full distribution (~2.7 million classes, all of life) is not vendored, and never realistically could be. CC0/public domain.
- **[VBO](https://github.com/monarch-initiative/vertebrate-breed-ontology) (the Vertebrate Breed Ontology)** — the only breed vocabulary found published as a real, resolvable OWL ontology (FCI/AKC/DAD-IS breed lists exist only as HTML/CSV, with no ontology IRIs). VBO's real full release turned out to be a genuine middle case — 19,961 classes across 49 species, ~78% of which (cattle, sheep, chicken, horse, pig, goat, and more) is livestock/poultry/game with no place in a *Pets* ontology — so rather than hand-picking a handful of illustrative breeds, `project_files/vbo-subset.ttl` extracts **every real breed** (2,822 classes) under the 9 companion-pet species this project names (dog, cat, rabbit, guinea pig, golden hamster, goldfish, zebrafish, zebra finch, Japanese rice fish), preserving VBO's own `subClassOf` breed tree (species-group → breed → sub-breed/variety, e.g. "Dog breed" → "Chihuahua" → "Chihuahua, Long-Haired") including its per-species "Mixed Breed" classes — comprehensive for every real pet species this app models, without dragging in irrelevant livestock breeds. `owl:import`ed from `other/pets.ttl`. Licensed CC-BY 4.0 — attributed in the vendor file's own header and per-class comments.
- **[DrOn](https://github.com/mcwdsi/dron) (the Drug Ontology)** — the only drug-domain ontology actually built on BFO, the same upper ontology CCO (and therefore this project) already uses. A small, hand-curated subset of its upper module — `pets:hasDoseForm`'s target classes ("drug tablet", "drug capsule") and `pets:MedicationAdministration`'s superclass ("drug administration") — is vendored at `project_files/dron-upper.ttl` and `owl:import`ed from `other/pets.ttl`; DrOn's real per-product classes (auto-generated from RxNorm, hundreds of thousands of them, ~300MB) are not vendored, since nothing here needs them.
- **[ChEBI](https://www.ebi.ac.uk/chebi/)** (Chemical Entities of Biological Interest) — `pets:hasActiveIngredient`'s values are real ChEBI class IRIs (e.g. `CHEBI:2676` for amoxicillin), cited directly, not imported (ChEBI is far larger than DrOn) — the same move DrOn itself makes for chemical-substance identity rather than modeling chemistry on its own.
- **CCO's already-vendored, already-transitively-imported `UnitsOfMeasureOntology.ttl`/`InformationEntityOntology.ttl`** (via `PersonOntology.ttl`'s own `owl:imports` chain) — supplies `pets:DosageAmount`'s value/unit-linking properties and real unit individuals (Teaspoon/Tablespoon/Milliliter/Milligram Measurement Unit); its parent class, Quality Specification (`cco:ont00000575`), comes from the likewise vendored and transitively imported `ArtifactOntology.ttl`.
- **FHIR RDF was deliberately not used** — despite HL7 FHIR's `Quantity`/`Dosage` datatypes being a natural-looking fit on paper, FHIR RDF is not BFO-aligned (HL7's own documentation concedes the mismatch and describes FHIR RDF as record/transaction-oriented, "should not be directly interpreted as stating facts"), is ~6MB/1000+ classes, and validates natively via ShEx rather than SHACL — a poor fit for this project's architecture. Only its general shape (value+unit, frequency+period) served as informal inspiration for `pets:DosageAmount`/`pets:MedicationAdministration`'s design, with no RDF-level dependency.
- `persona:usesDrOnClass`/`persona:usesChEBIClass` (annotation properties, `persona.ttl`, mirroring `persona:usesCCOClass`) document exactly which DrOn/ChEBI classes are actually referenced, asserted on `other/pets.ttl`'s own ontology header.

### Pets Ontology Files

- **`other/pets.ttl`** — Defines `pets:Pet` and `pets:PetMedicationRecord`/`pets:Medication` and their properties (see above), each an independent template type label class in its own right. `owl:imports` `project_files/dron-upper.ttl`, `project_files/ncbitaxon-subset.ttl`, and `project_files/vbo-subset.ttl`.
- **`project_files/ncbitaxon-subset.ttl`** — A hand-curated subset of NCBI Taxonomy covering 33 common pet species, cited by their real upstream IRIs with real upstream labels/definitions, not a full mirror. `owl:import`ed by `other/pets.ttl`.
- **`project_files/vbo-subset.ttl`** — A real, programmatically-filtered *extraction* of VBO — every breed (2,822 classes) under the 9 companion-pet species this project names, preserving VBO's own breed tree — not hand-picked, and not a full mirror of VBO's 19,961-class release either (which is ~78% livestock/poultry/game breeds out of scope for a *Pets* ontology). `owl:import`ed by `other/pets.ttl`.
- **`project_files/dron-upper.ttl`** — A hand-curated subset of [DrOn](https://github.com/mcwdsi/dron) (the Drug Ontology)'s upper module — five classes ("drug product", "active ingredient", "drug tablet", "drug capsule", "drug administration"), cited by their real upstream IRIs with real upstream labels/definitions, not a full mirror (DrOn's full distribution is ~300MB of RxNorm-derived per-product classes not relevant here). `owl:import`ed by `other/pets.ttl`. The first non-CCO/non-`mee.foundation` external ontology this project has ever vendored.
- **`other/shacl/pets-shacl.ttl`** — SHACL shapes for pet identity, pet medication, and care & feeding graphs, each directly linked from the tool its `pod-category-templates.ttl` template pod declares, via that tool's `pod:formShape`:
  - `:PetShape` (`pod:shape petshapes:PetShape`) targets `pets:Pet` individuals directly. Enforces: exactly one `name` (`xsd:string`) required; exactly one `hasSpecies` (IRI) required; at most one `hasBreed` (IRI) optional; at most one `birthDate` optional, and if present must be `xsd:date` or `xsd:gYear`; at most one `hasBodyWeight` (`pets:BodyWeight`) optional; at most one `sex` optional, constrained to `"Male"`/`"Female"`; at most one `isSpayedOrNeutered` optional (`xsd:boolean`). `:BodyWeightShape` targets `pets:BodyWeight`: exactly one "has decimal value" and exactly one "uses measurement unit" (IRI), both required — unlike `:DosageAmountShape`, the unit isn't optional here.
  - `:PetMedicationRecordShape` (`pod:shape petshapes:PetMedicationRecordShape`) targets `pets:PetMedicationRecord` record individuals directly — the medication list is a property of the record, not of the pet (which has no `p:Person` individual). Enforces: at least one `hasMedication` link. `:MedicationShape` targets each linked `pets:Medication` individual: at least one `hasActiveIngredient` (IRI); exactly one `hasDosageAmount` (`pets:DosageAmount`) and `hasAdministration` (`pets:MedicationAdministration`); optionally `hasDoseForm` (IRI), `medicationBrandName`, `medicationManufacturer`, `medicationDuration`. `:DosageAmountShape` targets `pets:DosageAmount`: exactly one of "has decimal value"/"has integer value" (`sh:xone`), optionally "uses measurement unit". `:MedicationAdministrationShape` targets `pets:MedicationAdministration`: optional `medicationFrequencyPerDay`; exactly one "occupies temporal region" link to a `BFO_0000038` interval.
  - `:PetsCareAndFeedingShape` — the `pod:formShape` of the tool `podcat:PetsCareAndFeeding` declares — targets `pets:Pet` individuals directly, mirroring `:PetShape`'s own property list, but with every property optional, including `name`/`hasSpecies` (required by `:PetShape` itself).

### Pets Ontology Validation

`other/shacl/pets-shacl.ttl` runs against individual graphs (the template pass), selected the same `pod:shape`-driven way as the Persona template shapes in README.md — `pets:Pet` (identity) and `pets:PetMedicationRecord` (medications) each have their own shape and target class. See [Validation](example.md#validation) for the mechanism and commands.

## Vehicles Ontology

The Vehicles ontology (`other/vehicles.ttl`) is the second of this project's `other/` peer ontologies (after the [Pets Ontology](#pets-ontology)) — small, mostly-vendored ontologies for domains a person merely *has* rather than *is*. Keeping this content out of `persona.ttl` means that file stays scoped strictly to a person's own identity; `persona.ttl` holds only the thin `p:hasVehicle` link (domain `p:Person`, range `v:Vehicle`, referenced by name — see [Possession-Related Classes and Properties](README.md#possession-related-classes-and-properties)) connecting a person to this ontology's own classes.

`v:Vehicle` is an independent template type label class, the same kind `pets:Pet`/`pets:PetMedicationRecord` already establish.

Unlike the Pets ontology (which never vendors an upstream class for "Pet" itself), `v:Vehicle` and its four vehicle-kind classes are also invented locally — named after [schema.org](https://schema.org/Vehicle)'s own `Vehicle`/`Car`/`BusOrCoach`/`Motorcycle`/`MotorizedBicycle` vocabulary for familiarity, but not formally grounded in it (no `owl:imports` or `subClassOf` of schema.org terms). Only the make/model controlled vocabulary is vendored, from Wikidata.

Throughout this section, `v:` is short for the `vehicles:` namespace (`http://mee.foundation/ontologies/vehicles#`) — `other/vehicles.ttl`'s own real Turtle prefix stays the verbose `vehicles:` internally (matching `service.ttl`'s `s:`/`service:` split), but every doc mention uses the short `v:` alias.

### Vehicle-Related Classes and Properties

This section describes the classes and properties, defined in `other/vehicles.ttl`, that identify a vehicle — its kind, make, model, and model year, and, optionally, its VIN, color, body type, fuel type, drive wheel configuration, odometer reading, and engine specification.

**Classes:**

- `v:Vehicle` — template label for a graph that identifies a vehicle, and also the actual `rdf:type` of the vehicle individual itself (a vehicle has no `p:Person` individual of its own — see `p:hasVehicle` above).
- `v:VehicleType` (abstract) — parent of the four concrete vehicle-kind classes below; never itself instantiated.
- `v:Car`, `v:BusOrCoach`, `v:Motorcycle`, `v:MotorizedBicycle` — the four vehicle kinds, each a concrete subclass of `v:VehicleType` with no properties of its own; used solely as `v:hasVehicleType` values (class-value-punning, the same style `pod:category` and `pets:hasSpecies`/`pets:hasBreed` already use).
- `v:Make` — the type of every individual vendored in `project_files/wikidata-vehicle-makes-subset.ttl`, a real vehicle manufacturer.
- `v:Model` — the type of every individual vendored in `project_files/wikidata-vehicle-models-subset.ttl`, a real vehicle model.
- `v:OdometerReading` — a vehicle's current odometer reading; a CCO Ratio Measurement Information Content Entity (`cco:ont00001022`); the decimal value and unit sit on a separate Information Bearing Entity (`cco:ont00000253`) that is carrier of it (`obo:BFO_0000101`), the same two-individual style `pets:BodyWeight` uses.
- `v:EngineSpecification` — a vehicle's engine details (type and displacement); a lighter-weight class than `v:OdometerReading`, with no CCO measurement-unit reification, since displacement is near-universally expressed in liters with no real unit ambiguity to guard against.

**Properties:**

- `v:hasVehicleType` — links a `v:Vehicle` to one of the four vehicle-kind classes (class-value-punned, not an instance); required, exactly one value.
- `v:hasMake` — links a `v:Vehicle` directly to a [Wikidata](https://www.wikidata.org) manufacturer individual (e.g. `wd:Q53268` for Toyota); required, exactly one value.
- `v:hasModel` — links a `v:Vehicle` directly to a Wikidata model individual (e.g. `wd:Q819982` for the Toyota RAV4); required, exactly one value.
- `v:modelMake` — links a `v:Model` individual back to its `v:Make` individual; asserted once per model in `project_files/wikidata-vehicle-models-subset.ttl` itself.
- `v:modelYear` — the vehicle's model year (`xsd:gYear`); required, exactly one value.
- `v:vehicleIdentificationNumber` — the vehicle's VIN (`xsd:string`); optional, at most one value — kept as a flat string since CCO has no reusable VIN designator class (only an informal mention as a `skos:example`).
- `v:color` — the vehicle's exterior color, free text; optional, at most one value.
- `v:bodyType` — the vehicle's body style (e.g. `"SUV"`, `"Sedan"`), free text — mirroring schema.org's own `bodyType`, which is likewise left as Text; optional, at most one value.
- `v:fuelType` — the vehicle's fuel type; optional, at most one value, constrained by SHACL to a small controlled vocabulary (`Gasoline`, `Diesel`, `Electric`, `Hybrid`, `PlugInHybrid`, `Hydrogen`) rather than a vendored external class list.
- `v:driveWheelConfiguration` — which wheels receive power; optional, at most one value, constrained by SHACL to `FWD`/`RWD`/`AWD`/`4WD`.
- `v:hasOdometerReading` — links a `v:Vehicle` to its `v:OdometerReading` individual; optional, at most one value. The linked `v:OdometerReading`'s bearer carries exactly one `cco:ont00001769` ("has decimal value") and exactly one `cco:ont00001863` ("uses measurement unit") pointing at a real CCO Measurement Unit individual (e.g. `cco:ont00001433` "Mile Measurement Unit" or `cco:ont00001598` "Kilometer Measurement Unit") — the unit is required, since a bare number alone is ambiguous between miles and kilometers.
- `v:hasEngineSpecification` — links a `v:Vehicle` to its `v:EngineSpecification` individual; optional, at most one value. Carries `v:engineType` (free text, e.g. `"Internal Combustion"`) and `v:engineDisplacementLiters` (`xsd:decimal`), both optional.

### Reused External Vocabulary (Vehicles)

- **[Wikidata](https://www.wikidata.org)** — a hand-curated selection of 35 major consumer vehicle manufacturers (car, motorcycle, and bus) and 21 current/recent flagship models, each a real Wikidata individual cited by its real Q-ID (e.g. `wd:Q53268` for Toyota, `wd:Q819982` for the Toyota RAV4) — verified live against Wikidata's own SPARQL endpoint and search API. Not a full extraction (unlike `project_files/vbo-subset.ttl`'s real full extraction of VBO's pet-relevant breed tree) — Wikidata has no bounded "vehicle manufacturer"/"vehicle model" scope the way VBO's pet breeds did, so this stays a hand-picked illustrative set, like `project_files/dron-upper.ttl`/`ncbitaxon-subset.ttl`. Deliberately typed as individuals rather than classes (unlike `pets:hasSpecies`/`pets:hasBreed`'s class-value-punning): Wikidata itself models a manufacturer or model as an instance of a class, not as a class in its own right. CC0/public domain, so no attribution obligation applies.
- **[schema.org](https://schema.org/Vehicle)** — the inspiration for `v:Vehicle`'s vehicle-kind naming (`Car`, `BusOrCoach`, `Motorcycle`, `MotorizedBicycle`) and several property names (`bodyType`, `fuelType`, `driveWheelConfiguration`, `vehicleIdentificationNumber`) — not formally imported or subclassed; `other/vehicles.ttl` defines its own local classes/properties rather than reusing schema.org's real IRIs directly.

### Vehicles Ontology Files

- **`other/vehicles.ttl`** — Defines `v:Vehicle` and its properties (see above), an independent template type label class. `owl:imports` `project_files/wikidata-vehicle-makes-subset.ttl` and `project_files/wikidata-vehicle-models-subset.ttl`.
- **`project_files/wikidata-vehicle-makes-subset.ttl`** — A hand-curated subset of Wikidata covering 35 major consumer vehicle manufacturers, cited by their real upstream Q-IDs with real upstream labels, not a full extraction. `owl:import`ed by `other/vehicles.ttl`.
- **`project_files/wikidata-vehicle-models-subset.ttl`** — A hand-curated subset of Wikidata covering 21 current/recent flagship models across the manufacturers above, cited by their real upstream Q-IDs, each linked back to its manufacturer via `v:modelMake`. `owl:import`ed by `other/vehicles.ttl`.
- **`other/shacl/vehicles-shacl.ttl`** — SHACL shapes for vehicle identity graphs, directly linked from the tool its `pod-category-templates.ttl` template pod declares, via that tool's `pod:formShape`:
  - `:VehicleShape` (`pod:shape vehicleshapes:VehicleShape`) targets `v:Vehicle` individuals directly. Enforces: exactly one `hasVehicleType` (`v:VehicleType`), `hasMake` (IRI), `hasModel` (IRI), and `modelYear` (`xsd:gYear`), all required; at most one each of `vehicleIdentificationNumber`, `color`, `bodyType`, `fuelType` (constrained to a small `sh:in` list), `driveWheelConfiguration` (constrained to a small `sh:in` list), `hasOdometerReading` (`v:OdometerReading`), and `hasEngineSpecification` (`v:EngineSpecification`), all optional. `:OdometerReadingShape` targets `v:OdometerReading`: exactly one "has decimal value" and exactly one "uses measurement unit" (IRI), both required. `:EngineSpecificationShape` targets `v:EngineSpecification`: at most one `engineType` and at most one `engineDisplacementLiters`, both optional.

### Vehicles Ontology Validation

`other/shacl/vehicles-shacl.ttl` runs against individual graphs (the template pass), selected the same `pod:shape`-driven way as `other/shacl/pets-shacl.ttl` — `v:Vehicle` has its own shape and target class. See [Validation](example.md#validation) for the mechanism and commands.

## Identity Documents Ontology

The Identity Documents ontology (`other/identity-documents.ttl`) is the third of this project's `other/` peer ontologies (after the [Pets Ontology](#pets-ontology) and [Vehicles Ontology](#vehicles-ontology)) — government-issued identity document classes for what a person merely *has* rather than *is*. Keeping this content out of `persona.ttl` means that file stays scoped strictly to a person's own identity; `persona.ttl` holds only the thin `p:hasIdentityDocument` link (domain `p:Person`, range `idoc:IdentityDocument`, referenced by name — see [Possession-Related Classes and Properties](README.md#possession-related-classes-and-properties)) connecting a person to this ontology's own classes. Unlike Pets/Vehicles, this ontology vendors no external vocabulary of its own — every class it defines is local, and the identity claims each document shape enforces (names, dates, designator numbers) reuse CCO terms the same way `persona.ttl` already does elsewhere.

Throughout this section, `idoc:` is short for the `identitydocuments:` namespace (`http://mee.foundation/ontologies/identity-documents#`) — `other/identity-documents.ttl`'s own real Turtle prefix stays the verbose `identitydocuments:` internally (the same verbose-internal/short-alias split as `vehicles:`/`v:` and `service:`/`s:`), but every doc mention uses the short `idoc:` alias.

### Identity-Document-Related Classes and Properties

This section describes the classes defined in `other/identity-documents.ttl` that identify a government-issued identity document.

**Classes:**

- `idoc:IdentityDocument` — superclass for every government-issued document that formally identifies a person. Never itself instantiated — only its three concrete subclasses below are.
- `idoc:BirthCertificate` — template label for a graph carrying a person's legal birth certificate name record, and the actual `rdf:type` of the reified document individual (linked from `:Self` via `p:hasIdentityDocument`).
- `idoc:DriversLicense` — template label for a graph carrying the identity claims on a state-issued driver's license. Distinct from `p:PhysicalDriversLicense` (`persona.ttl`), which models the physical card object carried in a wallet, not the identity data itself.
- `idoc:Passport` — template label for a graph carrying the identity claims on a government-issued passport.

**Properties:** none of its own — `p:hasIdentityDocument` (domain `p:Person`, range `idoc:IdentityDocument`) is the sole link into this ontology, and it lives in `persona.ttl` instead, the same "thin `hasX` link stays with the person" pattern `p:hasPet`/`p:hasVehicle` already establish.

One designator class rounds the ontology out: `idoc:GenderMarker` (subclass of CCO Designative Name) — the gender marker as it appears on a document (`'M'`, `'F'`, `'X'`), attached to an `idoc:Passport` via `designated by`. It is the only document designator this project mints itself; a driver's license number, passport number, place of birth, issuing jurisdiction, and issue date all reuse CCO's own `ent00000065`–`ent00000069` directly.

### Identity Documents Ontology Files

- **`other/identity-documents.ttl`** — Defines `idoc:IdentityDocument` and its three subclasses (see above), each an independent template type label class in its own right. Carries no `owl:imports` — no external vocabulary is vendored for this domain.
- **`other/shacl/identity-documents-shacl.ttl`** — SHACL shapes for the three document classes, each directly linked from the tool its `pod-category-templates.ttl` template pod declares, via that tool's `pod:formShape`:
  - `:BirthCertificateShape` (`pod:shape idocshapes:BirthCertificateShape`) targets `idoc:BirthCertificate` document individuals directly — all identity claims (names) are properties of the document individual, not the `p:Person`. Enforces: FullName OR (GivenName + FamilyName) required; optional AdditionalName, AlternateName, Nickname, Legal Name.
  - `:DriversLicenseShape` (`pod:shape idocshapes:DriversLicenseShape`) targets `idoc:DriversLicense` document individuals directly. Enforces: FullName OR (GivenName + FamilyName) required; Birthdate, DriversLicenseNumber, ExpirationDateIdentifier required (1..1 each); IssuingJurisdiction, PostalAddress, and hasPhoto optional.
  - `:PassportShape` (`pod:shape idocshapes:PassportShape`) targets `idoc:Passport` document individuals directly. Enforces: FullName OR (GivenName + FamilyName) required; Birthdate, PassportNumber, ExpirationDateIdentifier required (1..1 each); IssueDate, IssuingCountry, PlaceOfBirth, GenderMarker, and hasPhoto optional.

### Identity Documents Ontology Validation

`other/shacl/identity-documents-shacl.ttl` runs against individual graphs (the template pass), selected the same `pod:shape`-driven way as `other/shacl/pets-shacl.ttl`/`other/shacl/vehicles-shacl.ttl` — each of the three document classes has its own shape and target class. See [Validation](example.md#validation) for the mechanism and commands.

## Medical Appointments Ontology

The Medical Appointments ontology (`other/medical-appointments.ttl`) is a small `other/` peer ontology for a domain a person merely *has* — the claims two people need to share in order to arrange a medical appointment on someone else's behalf — rather than *is*. Unlike Pets/Vehicles/Identity Documents, `persona.ttl` carries no thin `hasX` link into it: a record here is shared between the two members coordinating that care rather than possessed by one `p:Person`, so there is no single holder for a link to name.

Throughout this section, `ma:` is short for the `medicalappointments:` namespace (`http://mee.foundation/ontologies/medical-appointments#`) — `other/medical-appointments.ttl`'s own real Turtle prefix stays the verbose `medicalappointments:` internally (matching `identitydocuments:`/`idoc:`'s identical split), but every doc mention uses the short `ma:` alias.

### Medical-Appointment-Related Classes and Properties

**Classes:**

- `ma:MedicalAppointmentRecord` — template label for a graph carrying the claims needed to arrange a medical appointment on behalf of someone else, and the actual `rdf:type` of the reified record individual. The claims below are properties of the record, not of the patient's `p:Person`. Any referenced third party (patient, physician) must have their own claims copied into the same graph, since every named graph must be self-contained for p2p sync between the coordinating members.

**Properties** (domain `ma:MedicalAppointmentRecord` throughout):

- `ma:forPatient` — the `p:Person` the appointment is for.
- `ma:hasPrimaryCarePhysician` — the patient's primary care physician, a `p:Person`. (The physician's own specialty is `p:specialty`, in `persona.ttl` — it describes the physician themselves, not the appointment.)
- `ma:currentMedication` — a medication the patient currently takes, as free text; repeatable.
- `ma:allergy` — an allergy the patient has, as free text; repeatable.
- `ma:medicalHistoryNote` — free-text summary of relevant history or ongoing conditions.
- `ma:insuranceProvider`, `ma:insurancePolicyNumber`, `ma:insuranceGroupNumber` — the patient's health insurance details.
- `ma:preferredPharmacy` — the patient's preferred pharmacy, as a free-text name and/or address.

### Medical Appointments Ontology Files

- **`other/medical-appointments.ttl`** — Defines the class and properties above. Carries no `owl:imports`.
- **`other/shacl/medical-appointments-shacl.ttl`** — `:MedicalAppointmentRecordShape` (`pod:shape mashapes:MedicalAppointmentRecordShape`), linked from the tool `podcat:MedicalAppointment`'s template pod declares, via its `pod:formShape`. Enforces: exactly one `ma:forPatient`, `ma:insuranceProvider`, and `ma:insurancePolicyNumber`; `ma:hasPrimaryCarePhysician`, `ma:medicalHistoryNote`, `ma:insuranceGroupNumber`, `ma:preferredPharmacy` optional; `ma:currentMedication` and `ma:allergy` repeatable.

### Medical Appointments Ontology Validation

`other/shacl/medical-appointments-shacl.ttl` runs against individual graphs (the template pass), selected the same `pod:shape`-driven way as every other per-template shape. See [Validation](example.md#validation).

## Service Accounts Ontology

The Service Accounts ontology (`other/service-accounts.ttl`) is a small `other/` peer ontology for a domain a person merely *has* — an online service account, e.g. with Google or AT&T — rather than *is*. `persona.ttl` carries no thin `hasX` link into it: CCO's own `holds user account` (`cco:ent00000045`) already plays that role — see [Accounts](README.md#accounts).

Throughout this section, `sa:` is short for the `serviceaccounts:` namespace (`http://mee.foundation/ontologies/service-accounts#`) — the file's own real Turtle prefix stays the verbose `serviceaccounts:` internally, but every doc mention uses the short `sa:` alias.

### Service-Account-Related Classes and Properties

**Classes:**

- `sa:ServiceAccount` — template label for a graph carrying the login credentials for one of a person's online service accounts, and the actual `rdf:type` of the account individual. Always multi-typed `cco:ent00000033` (Online Service Account) as well, so its service name, username, and service URI reuse that class's own existing properties directly (`cco:ent00000034`, `cco:ent00000035`, `cco:ent00000036`) with no domain change.

**Properties:**

- `sa:hasPassword` — the password credential; domain `cco:ent00000033`, the class `sa:ServiceAccount` multi-types alongside. It lives here rather than in `persona.ttl` because neither its domain nor its range is a `p:Person`.

- `sa:loyaltyProgramID` — the membership number identifying the account holder within a provider's loyalty or rewards program (a Hilton Honors number, an airline frequent-flyer number). Optional, at most one value: most online service accounts have no loyalty program attached at all, so it appears only on accounts held with a provider that runs one. Distinct from `has user handle` (`cco:ent00000035`) — a loyalty number identifies the person as a *program member* and is quoted when booking or claiming points, while the user handle is what they log in with, and the two are routinely different values on the same account. Range `xsd:string`, never numeric, since real program IDs are opaque identifiers that may carry leading zeros or non-digit characters. Domain `cco:ent00000033`, the same as `sa:hasPassword`, and here rather than in `persona.ttl` for the same reason.

### Service Accounts Ontology Files

- **`other/service-accounts.ttl`** — Defines the class and two properties above. Carries no `owl:imports`.
- **`other/shacl/service-accounts-shacl.ttl`** — `:ServiceAccountShape` (`pod:shape sashapes:ServiceAccountShape`), linked from the tools `podcat:Companies`'s and `podcat:BankingPayments`'s template pods declare, via their `pod:formShape`. Enforces: exactly one `has user handle` (username) and one `sa:hasPassword`; `has service name`, `has service URI`, and `sa:loyaltyProgramID` each optional, at most one value.

### Service Accounts Ontology Validation

`other/shacl/service-accounts-shacl.ttl` runs against individual graphs (the template pass). See [Validation](example.md#validation).

## Banking Ontology

The Banking ontology (`other/banking.ttl`) is a small `other/` peer ontology for a domain a person merely *has* — a debit card and the checking account it draws on — rather than *is*. `persona.ttl` holds only the thin `p:hasBankAccount` link (domain `p:Person`, range `banking:CheckingAccount`, referenced by name — see [Finance-Related Classes and Properties](README.md#finance-related-classes-and-properties)).

Throughout this section, `banking:` is both the file's real Turtle prefix and its doc alias (`http://mee.foundation/ontologies/banking#`) — short enough to need no separate alias, unlike `identitydocuments:`/`idoc:`.

### Banking-Related Classes and Properties

**Classes:**

- `banking:DebitCard` — template label for a graph carrying one of a person's debit cards, and the actual `rdf:type` of the card individual. Always multi-typed `cco:ent00000051` (Debit Card) as well, so its card number, CVV, and expiration date reuse that class's own designator pattern directly.
- `banking:CheckingAccount` — a bank checking account held by a person, linked to a debit card; also a template label for a graph carrying the account's own details (Checking Account Number `cco:ent00000071`, Routing Number `cco:ent00000072`, both via `designated by`).

**Properties:**

- `banking:accessesBankAccount` — links a `banking:DebitCard` (via `cco:ent00000051`) to the `banking:CheckingAccount` it draws funds from. It lives here rather than in `persona.ttl` because neither of its endpoints is a `p:Person`.

### Banking Ontology Files

- **`other/banking.ttl`** — Defines the classes and property above. Carries no `owl:imports`.
- **`other/shacl/banking-shacl.ttl`** — two shapes, both linked from the tool `podcat:BankingPayments`'s template pod declares, via its `pod:formShape`:
  - `:DebitCardShape` (`pod:shape bankingshapes:DebitCardShape`) targets `cco:ent00000051` directly rather than `banking:DebitCard`, since every `banking:DebitCard` individual is always multi-typed alongside that CCO class. Enforces: exactly one card number (PAN) and one expiration date; CVV and a linked `banking:CheckingAccount` optional (max 1 each).
  - `:CheckingAccountShape` (`pod:shape bankingshapes:CheckingAccountShape`) targets `banking:CheckingAccount` directly. Enforces: exactly one Checking Account Number and one Routing Number.

### Banking Ontology Validation

`other/shacl/banking-shacl.ttl` runs against individual graphs (the template pass). See [Validation](example.md#validation).

## Residences Ontology

The Residences ontology (`other/residences.ttl`) is a small `other/` peer ontology for a domain a person merely *has* — a place they have lived, current or past — rather than *is*. `persona.ttl` carries no thin `hasX` link into it: a residence is always the sole `pod:formTopic` of its own `podcat:Home` pod, and the resident is already recorded by the `has participant`/AddressDesignation machinery it multi-types alongside.

Throughout this section, `residences:` is both the file's real Turtle prefix and its doc alias (`http://mee.foundation/ontologies/residences#`).

### Residence-Related Classes and Properties

**Classes:**

- `residences:Residence` — template label for a graph carrying one of a person's residences, and the actual `rdf:type` of the residence individual. Always multi-typed `cco:ent00000016` (AddressDesignation) as well, so its address (`has address`), resident (`has participant`), and date range (`occupies temporal region` → `TemporalInterval`) reuse that class's own property pattern directly. An open-ended interval (no end date) means the current residence — see [Address history](README.md#modeling-details).

**Properties:** none of its own.

### Residences Ontology Files

- **`other/residences.ttl`** — Defines the class above. Carries no `owl:imports`.
- **`other/shacl/residences-shacl.ttl`** — `:ResidenceShape` (`pod:shape residenceshapes:ResidenceShape`), linked from the tool `podcat:Home`'s template pod declares, via its `pod:formShape`. Enforces: exactly one address and one temporal-region interval; a linked participant (the resident, usually `:Self`) optional.

### Residences Ontology Validation

`other/shacl/residences-shacl.ttl` runs against individual graphs (the template pass). See [Validation](example.md#validation).

## Itineraries Ontology

The Itineraries ontology (`other/itineraries.ttl`) is a small `other/` peer ontology for a domain a person merely *has* — a specific trip being planned or taken — rather than *is*, as distinct from `podcat:Travel`'s broader loyalty-program/airline information. `persona.ttl` carries no thin `hasX` link into it: an itinerary is always the `pod:formTopic` of a tool on its own `podcat:Trips` pod.

Throughout this section, `itineraries:` is both the file's real Turtle prefix and its doc alias (`http://mee.foundation/ontologies/itineraries#`).

### Itinerary-Related Classes and Properties

**Classes:**

- `itineraries:Itinerary` — template label for a graph carrying one of a person's trip itineraries, and the actual `rdf:type` of the itinerary individual. Alone among this project's template label classes, it is not multi-typed alongside any existing CCO/domain class — no domain ontology models trip-planning data yet — and it carries no structured properties of its own beyond a human-readable `rdfs:label` and/or `rdfs:comment` describing the trip (destination, dates, notes, as free text).

**Properties:** none of its own.

### Itineraries Ontology Files

- **`other/itineraries.ttl`** — Defines the class above. Carries no `owl:imports`.
- **`other/shacl/itineraries-shacl.ttl`** — `:ItineraryShape` (`pod:shape itineraryshapes:ItineraryShape`), linked from the tool `podcat:Trips`'s template pod declares, via its `pod:formShape`. Enforces: at least one of `rdfs:label` or `rdfs:comment`.

### Itineraries Ontology Validation

`other/shacl/itineraries-shacl.ttl` runs against individual graphs (the template pass). See [Validation](example.md#validation).

## Education Ontology

The Education ontology (`other/education.ttl`) is a small `other/` peer ontology for a domain a person merely *has* — a record of one stage of their schooling — rather than *is*. It is the exact parallel of `other/medical-appointments.ttl`'s `ma:MedicalAppointmentRecord`: a reified record individual, not a property of the person. `p:hasEducation` (`persona.ttl`) is the thin link into it.

It backs `podcat:Education`, which until now had no vocabulary at all behind it, and supplies the High School and College rows of a membership directory profile.

Throughout this section, `education:` is both the file's real Turtle prefix and its doc alias (`http://mee.foundation/ontologies/education#`).

### Education-Related Classes and Properties

**Classes:**

- `education:EducationRecord` — one stage of a person's schooling: a secondary school, a college or university, or a further qualification. An independent template type label class, asserted via `rdf:type` directly on the record individual and targeted directly by its own SHACL shape. A person may hold any number.

**Properties** (every one with domain `education:EducationRecord`, never `p:Person` — that is what keeps this file in `other/` rather than `persona-ext/`):

- `education:schoolName` — the name of the school, college, or awarding institution. The one required property: a record naming no institution records nothing.
- `education:educationLevel` — which stage this record represents. A controlled vocabulary enumerated in the shapes file rather than the ontology (the same pattern `v:fuelType` and `pets:sex` use): `"high school"`, `"college"`, `"other"`. Carrying the stage as a value rather than as a property per stage is deliberate — it lets a form asking for exactly one high school and one college express that as a cardinality constraint in its own shape instead of as vocabulary.
- `education:schoolCity` — the city the institution is in. A bare string: this locates the institution for a reader, it is not part of anyone's postal address.
- `education:schoolState` — the state, province, or region — or the country, where no smaller subdivision applies.
- `education:yearGraduated` — the year of graduation, an `xsd:gYear`. A year rather than a date, since no form and few memories carry the day.
- `education:degree` — a degree or qualification awarded, e.g. `"BSEE"`. Repeat where one institution awarded more than one. A bare string, not a `p:Credential`: that class is a post-nominal designator attached to a person's name, whereas this is an attribute of the record.

### Education Ontology Files

- **`other/education.ttl`** — Defines the class and properties above. Carries no `owl:imports`.
- **`other/shacl/education-shacl.ttl`** — `:EducationRecordShape`. A structural baseline only: datatypes, single-value caps, `education:schoolName` required, and the `education:educationLevel` value list. It requires nothing else — which stages a person must supply, and how many of each, is the asking organization's business and belongs in that organization's own shape.

### Education Ontology Validation

`other/shacl/education-shacl.ttl` runs against individual graphs (the template pass). See [Validation](example.md#validation).

## Sources Ontology

The Sources ontology (`other/sources.ttl`) is a small `other/` peer ontology for content a person merely *has* in unstructured form — a photo, a scan, a PDF, a pasted block of text, a video — rather than *is*. Every other ontology here models data that is already structured. People rarely bring data that way: they bring a photo of a passport, a PDF of a lease, a pasted confirmation email, and the structured record is something that can in principle be read out of it afterwards, by them or by an agent. This file names that unstructured starting point, a **source item**, and the act of reading structure out of it, an **extraction**, so that a structured record can say what it came from.

The metadata a source item carries is the metadata the app and the PDN already keep for any file: a pod attachment has a file name, a media type, and pre-extracted text that is either present or marked unread, and at the PDN layer it is an opaque, immutable payload addressed by its BLAKE3 content hash. Nothing here models OCR, transcription or document conversion themselves — only their result (`sources:extractedText`) and their record (`sources:Extraction`).

`sources:SourceItem` is the range of `pod:attachment` (see [Pod Properties](README.md#pod-properties)): a pod links to each file every member receives with one `pod:attachment` triple, and a member's private file is never a value of it. `persona.ttl` carries no thin `hasX` link into this file: a source item is reached from the pod it is attached to, or from the content derived from it, never from the person directly.

Throughout this section, `sources:` is both the file's real Turtle prefix and its doc alias (`http://mee.foundation/ontologies/sources#`).

### Source-Related Classes and Properties

**Classes:**

- `sources:SourceItem` — one piece of unstructured content a person brought into the app that could become structured pod data. A subclass of CCO's Information Bearing Artifact (`cco:ont00000798`): the bearer of some information, not the information itself, which is why the structured record read out of it is a separate individual. Abstract in intent — only ever asserted through one of its four subclasses. Immutable, like the attachment it describes: a corrected file is a new source item.
- `sources:Image` — a still image: a photo, a screenshot, a scan of a card or a page. Also under CCO's Image (`cco:ont00000702`). Its media type is always `image/*`.
- `sources:Document` — a document file: a PDF, a word-processor file, a spreadsheet, a Markdown file. Also under CCO's Document (`cco:ont00001298`). A scan saved as a PDF is a `sources:Document`; saved as a picture, a `sources:Image` — the file's format decides, not what the page shows. Not an `idoc:IdentityDocument`, which is the identity record a `sources:Document` may be the source of.
- `sources:TextBlob` — free text pasted or typed into the app as a source rather than a file. Its text is its content, so `sources:extractedText` is required here and optional everywhere else. Not a pod's note and not a chat message, both of which are built-in areas of every pod rather than items a person brings.
- `sources:Video` — a video file. Also under CCO's Video (`cco:ont00000874`). Its media type is always `video/*`.
- `sources:Extraction` — one act of deriving structured content from one or more source items: a person typing a passport's fields in from a photo of it, an OCR pass over a scanned form, an LLM turning pasted text into a contact card. A subclass of CCO's Act of Information Processing (`cco:ont00000366`).

**Source item properties** (domain `sources:SourceItem`):

- `sources:mediaType` — the IANA media type, e.g. `"application/pdf"`. Required, exactly one, lowercase, no parameters.
- `sources:fileName` — the file name as added. Optional, since a `sources:TextBlob` has no file behind it; a display and search hint only.
- `sources:byteSize` — the content's size in bytes, an `xsd:nonNegativeInteger`.
- `sources:contentHash` — the BLAKE3 hash of the content as 64 lowercase hex digits, the address the PDN's blob store keeps it under. Lets two members or two pods tell they hold the very same file.
- `sources:addedAt` — when the item was added to the pod, an `xsd:dateTime`. Required. When the photo was taken or the document written is a different fact, not recorded here.
- `sources:extractedText` — the item's text, as read off it by OCR, a converter or a person. Absent means **unread**; it is never the empty string, so an item nothing could be read from never looks like one whose text is empty.

**Extraction properties** (domain `sources:Extraction`, except `sources:derivedBy`):

- `sources:extractedFrom` — the source item(s) the extraction read, at least one: a license read from photos of its front and back is one extraction from two images.
- `sources:extractedBy` — who or what performed it: a `p:Person` entering data by hand, or an `s:Service` (typically the person's own `s:AgentService`). Exactly one. The union is enforced in the shapes file rather than by `rdfs:range`, as `pod:claimant`'s is. Independent of the claimant of the graph the result sits in.
- `sources:extractionMethod` — how: `"manual"`, `"ocr"`, `"llm"` or `"parser"` (a deterministic reader of a known format, such as a vCard). A controlled vocabulary enumerated in the shapes file, the same pattern `education:educationLevel` uses.
- `sources:extractedAt` — when, an `xsd:dateTime`. Required.
- `sources:confidence` — how sure the extractor was of the result as a whole, an `xsd:decimal` from 0 to 1. Normally present only for `"ocr"` and `"llm"`.
- `sources:derivedBy` — links **any** structured content individual (an `idoc:Passport`, a `pets:Pet`, a `p:Person`'s contact details) to the `sources:Extraction` that produced it, 0..N. No `rdfs:domain`, for the same reason `p:hasPhoto` has none. Pointing from the derived record to the extraction, rather than the reverse, lets an existing record gain a provenance link while the immutable source item never changes.

**Possible addition:** `sources:WebLink` — a URL or a saved web page brought as a source (`podcat:Information` already names web links among its contents). Not defined yet: nothing in the app ingests one, and it would first need reconciling with `p:WebURL`, which is a person's own web address rather than a source.

### Sources Ontology Files

- **`other/sources.ttl`** — Defines the classes and properties above. Carries no `owl:imports`; `p:Person`, `s:Service` and the CCO classes are referenced by name.
- **`other/shacl/sources-shacl.ttl`** — `:SourceItemShape` (the constraints common to every kind, targeting all four concrete classes by name), `:ImageShape`, `:TextBlobShape` and `:VideoShape` (what each kind narrows), `:ExtractionShape`, and `:DerivedByShape` (every `sources:derivedBy` value is a `sources:Extraction`). None is a form shape — a source item describes a file, not a form a person fills in — so none appears in README.md's [Form Shapes](README.md#form-shapes).

### Sources Ontology Validation

`other/shacl/sources-shacl.ttl` is a companion shape set: apply it in addition to a graph's own form shape whenever that graph also carries `sources:` individuals, the way `shacl/persona-shacl.ttl` is applied alongside the identity-document shapes. See [Validation](example.md#validation).
