# CHR-STD-01/03/05 — Specification authoring, registries and conformance

Candidate editorial policy aligned with OpenRGD governance and independent version axes.

Use technical English for authoritative documents, preserving established names and vocabulary. Translations are labelled informative unless explicitly adopted. Use the existing glossary rather than inventing new definitions for other owners. Mathematical notation is conventional (e.g. t, E, intervals and mappings), not forced to carry JSON suffixes; a field binding connects a mathematical quantity to an exact named wire field.

Use BCP 14 (RFC 2119 and 8174) for adopted normative requirements. Uppercase terms carry special meanings only under the stated convention. Candidate requirements may use that language with an explicit non-normative status; prose, examples and research claims do not acquire normative force by capitalization alone.

## Document template

Use the following applicable sections, without unnecessary empty sections:

1. Identifier, title, status, version, date, owners and abstract.
2. Motivation, scope, non-goals and terminology.
3. Source evidence, mathematical/information model, assumptions and dependencies.
4. Field dictionary, encoding and processing rules, error behavior and capability negotiation.
5. Version compatibility, migration, extension and registry considerations.
6. Security, privacy, trust, resource bounds and failure handling.
7. Conformance requirements, implementation status, tests and limitations.
8. Normative and informative references, errata and decision history.

Requirements receive stable IDs (CHR-REQ-*, within a centrally maintained scoped register when allocated). IDs are never reassigned; changes to meaning are versioned and linked. Use CHR-STD-* for internal work items, not official IETF RFC numbers. Source, candidate, accepted, deprecated and historical are distinguished following existing governance; a Git merge or tool release is not automatic normative acceptance. Do not claim external endorsement.

## Model/encoding separation

Abstract semantics are independent of text/binary encodings and SDKs. JSONC remains appropriate for the existing authored .rcg source; strict JSON is a candidate interoperable text exchange profile, not an instruction to replace source files. Follow exact schema version, explicit integer bounds, UTF-8, duplicate-key policy, unknown-field handling and safe parsing. I-JSON (RFC 7493) informs exact large integer handling. JCS (RFC 8785) and CBOR (RFC 8949) are candidate encoding/canonicalization references, not selected TimeAtom profiles yet. Specify complete signed preimage, hash profile, canonical bytes, error and range handling before interoperability or signing claims. The existing OpenRGD source hashing profile remains separate.

## Registry and extensions

The existing Chronograf channel registry remains authoritative for its assigned RGC-16 values; preserve the 23 existing assignments. Future registry changes declare owner, scope, version, allocation procedure, reserved/experimental/private-use policy, status, replacement and compatibility behavior. Do not reassign an allocated value to an incompatible meaning. Avoid global IDs for local scopes. Registry governance is inspired by RFC 8126, without claiming IANA administration. Reject or explicitly report unsupported critical extensions; noncritical extension behavior is specified per profile. No arbitrary liberal acceptance or silent correction of malformed protocol inputs (RFC 9413).

## Conformance

Every adopted requirement needs an appropriate check: schema validation, test vector, theorem, trace or documented review. A successful parse is not evidence of trust, hardware behavior or scientific truth. Test positive, negative, boundaries, version mismatches, unsupported values, cross-language exact round trips, resource limits and failure paths. Require independent implementations to demonstrate interoperability before a mature global standard claim; reference implementation is not normative authority. Distinguish target requirement from verified evidence and publish limitations.

Follow existing governance for compatibility, review and human acceptance. Maintain immutable versioned releases, public errata and traceable provenance. License and IP review is a separate gate; no license change in this RFC.

## Reference practices

- [BCP 14 / RFC 8174](https://www.rfc-editor.org/rfc/rfc8174)
- [RFC 7493](https://www.rfc-editor.org/rfc/rfc7493)
- [RFC 8126](https://www.rfc-editor.org/rfc/rfc8126)
- [RFC 9413](https://www.rfc-editor.org/rfc/rfc9413)
- [RFC 8785](https://www.rfc-editor.org/rfc/rfc8785), [RFC 8949](https://www.rfc-editor.org/rfc/rfc8949) — proposed encoding references only
