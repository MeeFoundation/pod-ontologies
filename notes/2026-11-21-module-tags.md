# Module tags — 21 Nov 2026

The hidden, software-written pod tag is `pod:moduleTag`, whose values are `pod:ModuleTag` nodes. Each node carries `pod:tagNamespace`, `pod:tagKey` and `pod:tagValue`. The shape that validates it is `:ModuleTagShape` in `shacl/pod-shacl.ttl`, and its YAML key is `tpod.moduleTag`.

## Why "module"

The tag is written by a **module**: software running in one member's own instance on their behalf. That is either the platform module behind a connector (`pod:Contacts`, e.g. the Apple Contacts module writing namespace `foundation.mee.applecontacts`, key `group`) or an `s:AgentService` acting for that member. A connector is never a service, so a name built on "service" misnamed the tag's main writer. Every definition already called the writer "the writing module", and the namespace is "the module's developer's domain", so the tag now takes the module's name.

## Why not a separate connector tag

A `connectorTag` would have copied the mechanism exactly:

- the same three-part node;
- the same hiding from the user's display and tag search;
- the same Pod Interface scoping to the caller's own namespace;
- the same rule against propagating on a share.

The one thing it would add is a record of what kind of module wrote the tag, and the namespace already says which module that was. Two mechanisms would also have doubled the shapes, the YAML-9 checks and the Pod Interface operations.

## Unchanged

`pod:tagNamespace`, `pod:tagKey` and `pod:tagValue`, the domain `pod:SecretPod`, and every behavior of the tag.
