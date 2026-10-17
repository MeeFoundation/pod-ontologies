---
id: http://www.example.org/tpod/pods/pod-01
title: "Boston Hub Society"
type: pod-databook
version: 1.5.0
created: 2026-07-10
description: >
  Pod DataBook for folder "Boston Hub Society" (pod:category: bhscat:BostonHubSociety). It is a
  multi-member pod with three members about :BHS_Service, :Self, and :Bob_Johnson, plus one tool
  graph about :BHS itself — the society's own organizational profile. An o:Organization is not
  member-capable, so the society participates through :BHS_Service, the service:ServiceProvider it
  provides; both of its graphs are still claimed by :BHS itself, the party really making those
  claims. Its category is the first category extension (pod-category-ext/boston-hub-society.ttl): a
  concept in the society's own skos:ConceptScheme, skos:broadMatch'd to podcat:Groups, whose template
  pod names bhsshapes:MemberShape as its pod:memberShape — so each member graph here is validated
  against the society's own two-page directory form rather than against pshapes:ContactInfoShape.
tpod:
  category: "bhscat:BostonHubSociety"
  creator: ":Self"
  owner: ":Self"
  member:
    - id: "http://www.example.org/tpod/graphs/graph-01"
      claimant: ":BHS"
      subject: ":BHS_Service"
      shape: "bhsshapes:MemberShape"
    - id: "http://www.example.org/tpod/graphs/graph-14"
      claimant: ":Self"
      subject: ":Self"
      shape: "bhsshapes:MemberShape"
    - id: "http://www.example.org/tpod/graphs/graph-03"
      claimant: ":Bob_Johnson"
      subject: ":Bob_Johnson"
      shape: "bhsshapes:MemberShape"
  tool:
    - id: "http://www.example.org/tpod/tools/tool-15"
      type: "form"
      formTopic: ":BHS"
      graph:
        - id: "http://www.example.org/tpod/graphs/graph-92"
          claimant: ":BHS"
          shape: "oshapes:OrganizationShape"
---

## Graphs

<a id="graph-01"></a>
### Graph 01

#### Overview

This graph captures the identity the Boston Hub Society presents as one of the pod's three parties. In our example BHS is compatible with PDN and participates directly, alongside Alice and Bob — but an `o:Organization` is never itself a `pod:member` graph's `pod:subject`, so what joins the pod is `:BHS_Service`, the `service:ServiceProvider` the society provides, carrying `service:providedBy :BHS`. The society's name and short self-description sit on `:BHS` itself, where they belong; its own organizational facts (member count, website) are the pod's tool graph instead, graph 92. BHS — the organization, not the service — is the claimant, since it is the party really making the claim and the one an eventual cryptographic signature would name.

#### Graph

```turtle
<!-- databook:id: bhs-org-graph -->
<!-- databook:graph: http://www.example.org/tpod/graphs/graph-01#graph -->
@prefix : <http://www.example.org/tpod#> .
@prefix o: <http://mee.foundation/ontologies/organization#> .
@prefix service: <http://mee.foundation/ontologies/service#> .
@prefix cco: <https://w3id.org/cco-domains/cco/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

:BHS_Service rdf:type owl:NamedIndividual ,
             service:ServiceProvider ;
    rdfs:label "Boston Hub Society membership service"@en ;
    service:providedBy :BHS .

:BHS rdf:type owl:NamedIndividual ,
             o:Organization ;
    rdfs:label "Boston Hub Society"@en ;

    <https://w3id.org/cco-domains/cco/ont00001917> [  # described by → Organization Note
        rdf:type cco:ent00000048 ;
        <https://w3id.org/cco-domains/cco/ont00001765> "An informal Boston-area professional networking society. Current members include Alice Walker and Bob Johnson."
    ] .
```

<a id="graph-03"></a>
### Graph 03

#### Overview

This graph captures Bob Johnson's BHS profile as transmitted from Bob's own instance of the app to Alice's over the PDN. It records the name Bob presents to the Boston Hub Society, along with the handful of directory answers he chose to fill in. Like graph 14 it is validated against `bhsshapes:MemberShape`, and it shows what that shape does *not* demand: every field on the society's form except a first and last name is optional, so a member who answers four questions conforms exactly as well as one who answers all of them. Bob is the claimant.

#### Graph

```turtle
<!-- databook:id: bob-bhs-graph -->
<!-- databook:graph: http://www.example.org/tpod/graphs/graph-03#graph -->
@prefix : <http://www.example.org/tpod#> .
@prefix persona: <http://mee.foundation/ontologies/persona#> .
@prefix directoryprofile: <http://mee.foundation/ontologies/directory-profile#> .
@prefix education: <http://mee.foundation/ontologies/education#> .
@prefix cco: <https://w3id.org/cco-domains/cco/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

:Bob_Johnson rdf:type owl:NamedIndividual ,
              persona:Person ;
    rdfs:label "Bob Johnson (BHS)"@en ;

    <https://w3id.org/cco-domains/cco/ont00001879> [  # designated by → GivenName ("First full Name")
        rdf:type cco:ent00000002 ;
        <https://w3id.org/cco-domains/cco/ont00001765> "Bob"
    ] ;

    <https://w3id.org/cco-domains/cco/ont00001879> [  # designated by → FamilyName ("Last Name") — required by MemberShape
        rdf:type cco:ent00000004 ;
        <https://w3id.org/cco-domains/cco/ont00001765> "Johnson"
    ] ;

    <https://w3id.org/cco-domains/cco/ont00001879> [  # designated by → Email
        rdf:type cco:ent00000024 ;
        persona:contactContext "home" ;
        <https://w3id.org/cco-domains/cco/ont00001765> "bob.johnson@example.com"
    ] ;

    # ── The four directory questions Bob answered ──────────────────────
    directoryprofile:memberSince "2019-04-02"^^xsd:date ;
    directoryprofile:industry "Finance" ;
    directoryprofile:hometown "Providence, Rhode Island, USA" ;
    persona:hasEducation :Bob_College .


:Bob_College rdf:type owl:NamedIndividual ,
                      education:EducationRecord ;
    rdfs:label "Bob Johnson's college"@en ;
    education:educationLevel "college" ;
    education:schoolName "Brown University" ;
    education:yearGraduated "1998"^^xsd:gYear .
```

<a id="graph-14"></a>
### Graph 14

#### Overview

This graph captures Alice Walker's BHS profile — the identity data she shares with the Boston Hub Society, entered on the society's two-page "Personal Page for BHS 2026 Directory" form. It is validated against `bhsshapes:MemberShape` rather than `pshapes:ContactInfoShape`, the Boston Hub Society being the first category to name a member shape of its own. Beyond the contact details any member graph carries, it records her directory answers — when she joined and who sponsored her, her industries and job function, her schooling, her family, and the short written answers the directory prints under her name. Alice is the claimant.

The vocabulary is entirely shared: names, birth date, employer, job title, address, phone, and email come from CCO and `persona.ttl`; the directory questions from `persona-ext/directory-profile.ttl`; the schooling rows from `other/education.ttl`. Nothing here is BHS-specific — what belongs to the society is only its shape, which requires a FamilyName (`ContactInfoShape` does not) and restricts `directoryprofile:industry` to its own 19-value list.

Her job function is the one answer whose permitted values the society does not set. `dp:jobFunction` hangs off an Occupation Role (`cco:ont00000984`) that Alice bears via `BFO_0000196`, rather than off `:Self` directly, and its 23 values are the job families of the US Standard Occupational Classification — frozen once in `dpshapes:DirectoryProfileShape`, since a national standard is nobody's to vary. `bhsshapes:MemberShape` caps the answer at one and refuses it on the member directly, but leaves the list alone. Note that "Computer and Mathematical" classifies the same employment her `p:JobTitle` of "Software Engineer" names; the two are independent, and a member may carry either, both, or neither.

#### Graph

```turtle
<!-- databook:id: alice-bhs-graph -->
<!-- databook:graph: http://www.example.org/tpod/graphs/graph-14#graph -->
@prefix : <http://www.example.org/tpod#> .
@prefix persona: <http://mee.foundation/ontologies/persona#> .
@prefix directoryprofile: <http://mee.foundation/ontologies/directory-profile#> .
@prefix education: <http://mee.foundation/ontologies/education#> .
@prefix cco: <https://w3id.org/cco-domains/cco/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

:Self rdf:type owl:NamedIndividual ,
               persona:Person .

:Self rdfs:comment "Alice Walker's persona for her BHS directory profile."@en ;

    # ── Name components (BHS form, page 1) ──────────────────────────────────
    <https://w3id.org/cco-domains/cco/ont00001879> [  # designated by → GivenName ("First full Name")
        rdf:type cco:ent00000002 ;
        <https://w3id.org/cco-domains/cco/ont00001765> "Alice"
    ] ;

    <https://w3id.org/cco-domains/cco/ont00001879> [  # designated by → FamilyName ("Last Name") — required by MemberShape
        rdf:type cco:ent00000004 ;
        <https://w3id.org/cco-domains/cco/ont00001765> "Walker"
    ] ;

    <https://w3id.org/cco-domains/cco/ont00001879> [  # designated by → AdditionalName ("Middle Initial")
        rdf:type cco:ent00000003 ;
        <https://w3id.org/cco-domains/cco/ont00001765> "M"
    ] ;

    <https://w3id.org/cco-domains/cco/ont00001879> [  # designated by → AlternateName ("Preferred first name")
        rdf:type cco:ent00000006 ;
        <https://w3id.org/cco-domains/cco/ont00001765> "Ali"
    ] ;

    <https://w3id.org/cco-domains/cco/ont00001879> [  # designated by → Birthdate
        rdf:type cco:ent00000046 ;
        <https://w3id.org/cco-domains/cco/ont00001765> "1985-03-12"
    ] ;

    # ── Employment ("Business Name", "Current Title") ────────────────────────
    <https://w3id.org/cco-domains/cco/ont00001879> [  # designated by → OrganizationName
        rdf:type cco:ent00000047 ;
        <https://w3id.org/cco-domains/cco/ont00001765> "Acme"
    ] ;

    <https://w3id.org/cco-domains/cco/ont00001879> [  # designated by → JobTitle
        rdf:type persona:JobTitle ;
        <https://w3id.org/cco-domains/cco/ont00001765> "Software Engineer"
    ] ;

    # ── Addresses — the form asks for a business and a home one ──────────────
    <https://w3id.org/cco-domains/domains/AddressOntology#ent00000324> :Address_BHS_Work ;
    <https://w3id.org/cco-domains/domains/AddressOntology#ent00000324> :Address_BHS_Home ;

    # ── Phones ("Office Phone", "Cell Phone") ────────────────────────────────
    <https://w3id.org/cco-domains/cco/ont00001879> [  # designated by → Phone
        rdf:type cco:ent00000023 ;
        persona:contactContext "work" ;
        persona:phoneFeature "voice" ;
        <https://w3id.org/cco-domains/cco/ont00001765> "+14085550143"
    ] ;

    <https://w3id.org/cco-domains/cco/ont00001879> [  # designated by → Phone
        rdf:type cco:ent00000023 ;
        persona:contactContext "home" ;
        persona:phoneFeature "mobile" ;
        <https://w3id.org/cco-domains/cco/ont00001765> "+15108149999"
    ] ;

    # ── Emails ("Work Email Address", "Home Email") ──────────────────────────
    <https://w3id.org/cco-domains/cco/ont00001879> [  # designated by → Email
        rdf:type cco:ent00000024 ;
        persona:contactContext "work" ;
        <https://w3id.org/cco-domains/cco/ont00001765> "alice@acme.com"
    ] ;

    <https://w3id.org/cco-domains/cco/ont00001879> [  # designated by → Email
        rdf:type cco:ent00000024 ;
        persona:contactContext "home" ;
        <https://w3id.org/cco-domains/cco/ont00001765> "awalker@gmail.com"
    ] ;

    # ── Membership (BHS form, pages 1 and 2) ─────────────────────────────────
    directoryprofile:memberSince "2021-09-15"^^xsd:date ;
    directoryprofile:sponsoredBy "Marcy Chen" ;

    # ── Industry — constrained by MemberShape to the society's own 19 values ─
    directoryprofile:industry "Technology" ;
    directoryprofile:industry "Non-Profit" ;

    # ── Job function — one of the 23 SOC/O*NET job families ──────────────────
    <http://purl.obolibrary.org/obo/BFO_0000196> [  # bearer of → Occupation Role
        rdf:type cco:ont00000984 ;  # Occupation Role
        directoryprofile:jobFunction "Computer and Mathematical" ;
        rdfs:comment "Job function: Computer and Mathematical (SOC major group 15-0000)"@en
    ] ;

    # ── Schooling ("High School", "College") ─────────────────────────────────
    persona:hasEducation :Alice_HighSchool ;
    persona:hasEducation :Alice_College ;

    # ── Career history ───────────────────────────────────────────────────────
    directoryprofile:previousPositions "Software engineer at Northbridge Systems (2008-2014); staff engineer at Vireo Labs (2014-2019)." ;
    directoryprofile:recognitions "Acme Engineering Excellence Award (2023)." ;
    directoryprofile:directorships "Present: Chestnut Hill Village Association. Past: Vireo Labs technical advisory board." ;
    directoryprofile:nonProfitPositions "Volunteer instructor, Boston Coding Outreach (present)." ;

    # ── Family ───────────────────────────────────────────────────────────────
    directoryprofile:spousePartnerName "Dave Walker" ;
    directoryprofile:spousePartnerBirthDate "1983-06-04"^^xsd:date ;
    directoryprofile:family "Sophia Walker (2012)" ;

    # ── Background and personal ──────────────────────────────────────────────
    directoryprofile:hometown "Austin, Texas, USA" ;
    directoryprofile:dietaryRestrictions "Vegetarian" ;
    directoryprofile:personalGoals "Mentor more early-career engineers. Finish the coast-to-coast ride." ;
    directoryprofile:lifeExperiences "Cycled from Boston to Portland over six weeks in 2019, mostly on gravel." ;

    # ── Interests/Hobbies — reuses persona:PersonalInfo, not a new property ──
    persona:hasPersonalInfo :Alice_Hobby_Cycling ;
    persona:hasPersonalInfo :Alice_Hobby_Piano .


#################################################################
#  Addresses
#################################################################

:Address_BHS_Work rdf:type owl:NamedIndividual ,
                           cco:ent00000010 ;  # USPostalAddress
    rdfs:label "Alice Walker's BHS business address"@en ;
    persona:contactContext "work" ;
    <http://purl.obolibrary.org/obo/BFO_0000178> [  # has continuant part → Street
        rdf:type cco:ent00000011 ;
        <https://w3id.org/cco-domains/cco/ont00001765> "2200 Zanker Road"
    ] ;
    <http://purl.obolibrary.org/obo/BFO_0000178> [  # has continuant part → City
        rdf:type cco:ent00000012 ;
        <https://w3id.org/cco-domains/cco/ont00001765> "San Jose"
    ] ;
    <http://purl.obolibrary.org/obo/BFO_0000178> [  # has continuant part → State
        rdf:type cco:ent00000013 ;
        <https://w3id.org/cco-domains/cco/ont00001765> "CA"
    ] ;
    <http://purl.obolibrary.org/obo/BFO_0000178> [  # has continuant part → ZIP
        rdf:type cco:ent00000015 ;
        <https://w3id.org/cco-domains/cco/ont00001765> "95131"
    ] ;
    <http://purl.obolibrary.org/obo/BFO_0000178> [  # has continuant part → Country
        rdf:type cco:ent00000014 ;
        <https://w3id.org/cco-domains/cco/ont00001765> "USA"
    ] .

:Address_BHS_Home rdf:type owl:NamedIndividual ,
                           cco:ent00000010 ;  # USPostalAddress
    rdfs:label "Alice Walker's BHS home address"@en ;
    persona:contactContext "home" ;
    <http://purl.obolibrary.org/obo/BFO_0000178> [  # has continuant part → Street
        rdf:type cco:ent00000011 ;
        <https://w3id.org/cco-domains/cco/ont00001765> "123 Sleepy Hollow"
    ] ;
    <http://purl.obolibrary.org/obo/BFO_0000178> [  # has continuant part → City
        rdf:type cco:ent00000012 ;
        <https://w3id.org/cco-domains/cco/ont00001765> "Paradise"
    ] ;
    <http://purl.obolibrary.org/obo/BFO_0000178> [  # has continuant part → State
        rdf:type cco:ent00000013 ;
        <https://w3id.org/cco-domains/cco/ont00001765> "CA"
    ] ;
    <http://purl.obolibrary.org/obo/BFO_0000178> [  # has continuant part → ZIP
        rdf:type cco:ent00000015 ;
        <https://w3id.org/cco-domains/cco/ont00001765> "95969"
    ] ;
    <http://purl.obolibrary.org/obo/BFO_0000178> [  # has continuant part → Country
        rdf:type cco:ent00000014 ;
        <https://w3id.org/cco-domains/cco/ont00001765> "USA"
    ] .

:BHS_WorkAddressDesignation rdf:type owl:NamedIndividual ,
                                     cco:ent00000016 ;  # AddressDesignation
    rdfs:label "Alice Walker's BHS business address designation"@en ;
    <http://purl.obolibrary.org/obo/BFO_0000057> :Self ;
    <https://w3id.org/cco-domains/domains/AddressOntology#ent00000324> :Address_BHS_Work .

:BHS_HomeAddressDesignation rdf:type owl:NamedIndividual ,
                                     cco:ent00000016 ;  # AddressDesignation
    rdfs:label "Alice Walker's BHS home address designation"@en ;
    <http://purl.obolibrary.org/obo/BFO_0000057> :Self ;
    <https://w3id.org/cco-domains/domains/AddressOntology#ent00000324> :Address_BHS_Home .


#################################################################
#  Schooling — other/education.ttl
#  Which stage each record is comes from education:educationLevel, so
#  MemberShape can cap the form's one High School row and one College
#  row without the ontology needing a property per stage.
#################################################################

:Alice_HighSchool rdf:type owl:NamedIndividual ,
                           education:EducationRecord ;
    rdfs:label "Alice Walker's high school"@en ;
    education:educationLevel "high school" ;
    education:schoolName "Westlake High School" ;
    education:schoolCity "Austin" ;
    education:schoolState "TX" ;
    education:yearGraduated "2003"^^xsd:gYear .

:Alice_College rdf:type owl:NamedIndividual ,
                        education:EducationRecord ;
    rdfs:label "Alice Walker's college"@en ;
    education:educationLevel "college" ;
    education:schoolName "University of Texas at Austin" ;
    education:schoolCity "Austin" ;
    education:schoolState "TX" ;
    education:yearGraduated "2007"^^xsd:gYear ;
    education:degree "BS Computer Science" .


#################################################################
#  Interests/Hobbies — persona:PersonalInfo (persona.ttl), reused
#  rather than adding a directoryprofile: property for the same thing.
#################################################################

:Alice_Hobby_Cycling rdf:type owl:NamedIndividual ,
                              persona:PersonalInfo ;
    rdfs:label "Alice Walker's cycling"@en ;
    persona:personalInfoKind "hobby" ;
    persona:personalInfoValue "long-distance cycling" .

:Alice_Hobby_Piano rdf:type owl:NamedIndividual ,
                            persona:PersonalInfo ;
    rdfs:label "Alice Walker's piano"@en ;
    persona:personalInfoKind "hobby" ;
    persona:personalInfoValue "piano" .

```

<a id="graph-92"></a>
### Graph 92

#### Overview

This graph captures the Boston Hub Society's own organizational profile — the society as an
`o:Organization` in its own right, with its current member count and public website — as the pod's
tool graph. It is distinct from graph 01, BHS's `pod:member` entry, which carries only the identity
BHS presents as one of the three parties to this pod. BHS is the claimant.

#### Graph

```turtle
<!-- databook:id: bhs-org-profile-graph -->
<!-- databook:graph: http://www.example.org/tpod/graphs/graph-92#graph -->
@prefix : <http://www.example.org/tpod#> .
@prefix o: <http://mee.foundation/ontologies/organization#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

:BHS rdf:type owl:NamedIndividual ,
             o:Organization ;
    rdfs:label "Boston Hub Society"@en ;

    o:numMembers 80 ;
    o:hasWebsite "https://bostonhubsociety.example.org"^^xsd:anyURI .
```
