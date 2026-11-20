---
description: Regenerate README.md's Form Shapes table from the ontology (the .ttl files are authoritative), and write descriptions for any newly-added form shape
---

Reconcile the **Form Shapes** table in `README.md`'s [Form Shapes](../../README.md#form-shapes) section against the ontology. The table lists every SHACL shape the app's **Add Tool** dialog offers as a form's template — the value stamped onto the new graph as its `pod:shape`. README calls these *form shapes*; `app-behavior.md` calls the same set *form types*, from the user's side.

**The `.ttl` files are authoritative.** Where the table and the ontology disagree, the table is wrong. This is a one-directional sync: ontology → `README.md`.

`helpers/form-types.py` does the mechanical half. It owns the table's **row set**, its **shape** column (the CURIE plus a link to the `*-shacl.ttl` file defining it) and its **Declared by** column, reading them from `helpers/validate.py`'s `SHAPE_TO_FILE` registry and from every `pod:formShape`/`pod:memberShape` in `pod-category-templates.ttl` and `pod-category-ext/*.ttl`. It does **not** write the display name or the description — those are the app's own UI wording, and your job here.

## Method

1. Run `python3 helpers/form-types.py --check` from the repo root.
   - **Exit 0, no output but the match line** → nothing to do. Say so and stop; do not edit the file.
   - **"Shapes that are neither a registered form type nor a component of one"** → a shape was added to a `**/shacl/*.ttl` file and never classified. Resolve this *first*, before touching the table: read the shape and decide whether a user could sensibly add it as a form. If yes, register it in `helpers/validate.py`'s `SHAPE_TO_FILE` (and `SHAPE_NS`/`PREFIX_TO_FILES` too, if its shapes file is new — that registry is what the validator resolves a `pod:shape` value against, so the gap is a validation gap as much as a docs one). If no, it belongs under the script's `INFRA_FILES` rule or is a component shape already; say which and leave it out.
   - **A unified diff of the table** → go on to step 2.
2. Run `python3 helpers/form-types.py --write`. Surviving rows keep their order, name and description; the shape and Declared by columns are rewritten; a shape that left the registry loses its row; a new shape gets a row at the end of the table with a `{TODO: ...}` description.
3. For each `{TODO: ...}` row, run `python3 helpers/form-types.py --report` and read that shape's block — its target class, its `sh:message`, and its properties marked `REQ`/`opt`. Write the description from those facts, matching the existing rows' style: what the form records, required fields first, then the optional ones, no trailing period. Give the row a real display name too — the generated one is a naive de-camel-casing of the shape's local name (`PetsCareAndFeedingShape` → "Pets Care And Feeding"), so fix it to the label a user would see. Then move the row from the end of the table into the group it belongs with; the ordering is editorial (person-subject forms, then documents, then accounts, then possessions and places, then records), and the script preserves whatever order it finds.
4. Re-read the prose that names facts the ontology settles, now in two places:
   - **`README.md`, the paragraphs around the generated block** — the scope bullets above it (which shapes are components, structural, or member-shape-only) and the category-extension paragraph below it. They name `bhsshapes:MemberShape` as the one member-shape-only shape and `bhscat:BostonHubSociety` as an extension declaring a core shape; `--check`'s match line prints the current member-shape-only set.
   - **`app-behavior.md`'s [Form Types](../../app-behavior.md#form-types)** — its closing paragraph names the three tool kinds with no content model (`pod:Calendar`, `pod:Canvas`, `pod:Map`) and points connectors (`pod:Contacts`, `pod:Browser`) elsewhere, both of which `pod.ttl` settles. That subsection is not generated and holds no table; check it only when the tool kinds change.
5. Re-run `python3 helpers/form-types.py --check` — it must exit 0.

## Scope

- Only `README.md`'s Form Shapes table and the paragraphs immediately around it. Nothing between the `<!-- BEGIN GENERATED: form-types -->` fences is ever hand-edited — change the ontology or the registry instead, then regenerate.
- Does **not** add, remove or rename a shape, a category, or a template's `pod:formShape`. Those are modeling changes and separate, explicit requests; this command only makes the documentation catch up with them.
- Does **not** regenerate anything in `app-behavior.md`. The table is derived from the SHACL shapes the ontologies define, so it lives in `README.md`, which documents those ontologies; `app-behavior.md`'s Form Types subsection covers only what the **Add Tool** dialog does with the user's pick, and is edited by hand (step 4). A genuinely new class or property still needs its own README mention alongside the table — flag that, don't write it here.

## After editing

- Report a concise summary: rows added, removed or re-pointed, and which descriptions you wrote. Don't reprint unchanged rows.
- No `.ttl` file changed, so no version bump — unless step 1 sent you to `helpers/validate.py`, which carries no version either. If the sync revealed a missing SHACL shape or template, say so rather than inventing one.
