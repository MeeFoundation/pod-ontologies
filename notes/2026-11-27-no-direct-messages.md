# No Direct Messages

*Tellipod pod ontology: concept summary, 2026-11-27*

## The concept

Tellipod has **no direct messages**. A pod's chat (`pod:Chat`) is a single group stream, and every member sees every message in it.

- **Directed messages stay in the stream.** A member can @-mention another. The message and the reply are both in the shared stream, so every member sees them.
- **Telli lives only in the Telli chat.** The user talks with their personal agent in the Telli chat, a secret conversation that belongs to no pod. There is no @Telli thread inside a pod's chat area. The agent works on the **current pod**, the pod the user is interacting with.
- **The chat is ordinary shared content.** Every tool's content now reaches every member. In the pod graph, the one projected content with a narrower reach is a member's meta note, which stays in that member's own copy.

## Consequences

- `pod:Chat` is no longer special among tools: none of its content is held back from any member.
- What never propagates on a share is two things: the member's meta note, and their tags and pod space.
- The open question on the chat's suggested vocabulary (`notes/open-items.md`) covers group-stream messages only.

## What changed

`pod.ttl` (Pod Tools section comment, `pod:Chat` comment; versionIRI 10.9.1), `README.md` (Secret and private, the Chat bullet, sharing, tool classes, The Pod Graph), `app-behavior.md` (storage paragraph, Pod Contents, Chat Area, Pod Interface, Personal Agent and its tables, the prompt/response loop), `pod-databook.md` (Where chat content goes), `notes/open-items.md`, `CLAUDE.md`. No new terms and no constraint changes.
