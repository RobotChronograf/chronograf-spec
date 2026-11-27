# CHR-0.3A — Review and delivery gates

Status: proposed acceptance plan; not a test report. No code or fixtures are executed by this RFC.

## 1. Required counterexamples / future conformance

| ID | Case | Required outcome |
|---|---|---|
| T01 | POSIX reading relabelled TAI, invalid conversion | Reject or explicitly mark unsupported; never silently relabel. |
| T02 | Negative instant, >2^53 integer, resolution boundary | Exact round trip and normalized encoding; no silent precision loss. |
| T03 | Two boot IDs with equal monotonic readings | Incomparable without verified mapping. |
| T04 | Same clock uncertain vs UTC | Relative age uses justified relative error, not naive sum of absolute uncertainties. |
| T05 | Overlapping bounds or missing/expired mapping | UNKNOWN/INCOMPARABLE, not equality or ordering. |
| T06 | Physical clock jump / holdover after disconnect | Evidence discontinuity and appropriate uncertainty; no fake external accuracy. |
| T07 | Reversible simulation or forked timeline | Preserve branch/domain and origin; no physical history mutation. |
| T08 | Every local hop passes; full source-to-action age exceeds budget | End-to-end constraint violated regardless of local compliance. |
| T09 | Critical stale interval hidden by high average score | Hard constraint remains violated; quality cannot compensate. |
| T10 | New label from old frame, unknown capture or incomplete ancestry | Preserve old source age or explicitly unknown; no reset. |
| T11 | Same datum consumed by two invocations | Distinct usage edges and times; availability does not prove use. |
| T12 | Legacy import with only old timestamp | Preserve source assertion, issue anchor only for actually measured new event. |
| T13 | Anchor 0 / foreign namespace / mutated TimeAtom / swapped domain | Reject invalid or mismatched evidence; no comparison by handle across namespaces. |
| T14 | Hash matches but no trusted signer/clock or truncated chain | Distinguish integrity, authenticity, continuity, completeness and trust; no universal proof. |
| T15 | Later external receipt for offline event | Append link; no mutation or retroactive capture claim. |
| T16 | No network, only local monotonic provider | Local core functions; external absolute-time and attestation claims unavailable. |
| T17 | Channel 0xF000 or existing 23-ID registry used | Preserve historical v0.2 meanings; detect duplicate/reassigned ID. |
| T18 | Manifest with changed source, missing required hash, unknown format | Reject or explicit unsupported; reproducible derived view, no fallback to guessed values. |
| T19 | Valid synthetic review or forged COMMITTED text | No physical milestone, Life, History commit or actuation authority. |
| T20 | Non-robot agent or simulator without OpenRGD installed | Neutral temporal representation and local verification supported independently. |

Fixtures must distinguish parsing, semantic validity, metrology, cryptographic verification, authorization and actual runtime evidence. A mock clock/writer can test contracts but cannot satisfy real authority gates.

## 2. Sequence

| Phase | Scope | Exit evidence |
|---|---|---|
| 0.3A | Architecture / ownership / decision register | Owner reviews, disposition of A01–A11, no competing authoritative source |
| 0.3B | TimeAtom, clock domains, exact encoding, uncertainty | Versioned schemas, golden vectors, independent implementation comparison, unit/epoch/clock failure tests |
| 0.3C | Domain mappings and layers; RGC-16 profiles | Verified map compatibility, branch/pause/reboot fixtures, universal core without OpenRGD |
| 0.3D | TTG, temporal provenance, source age and manifests | Canonical source and build reproducibility, typed relations, cycle rules and end-to-end deadline fixtures |
| 0.3E | Offline anchor provider / TAP / attestation | Scoped issuer/verifier, rollback/holdover/failure tests, trust model, actual measurement evidence; independent witness optional |
| 0.3F | OpenRGD/Physics/History/RI/Cognition integration | Versioned owner-reviewed bindings, real provider/resolver evidence, writer and effect-gate integration by owners |
| 0.3 release | Packaging and publication | License/provenance review, reproducible builds, independent conformance and explicit acceptance |

THP-LAB-01 and other scientific investigations proceed independently. No claim of verified intelligence, physics theory, legal timestamp proof, production hard real-time operation or safety certification at these gates.

## 3. Open decisions

- Exact epoch and conversion tables, leap-second handling, representation of negative and extended time, canonical byte encoding and supported field widths.
- TimeAtom/hash compatibility vs domain-qualified record commitment; no silent hash semantic change.
- Profile registry namespace and versioning policy; explicit universal barcode vs existing OpenRGD v1.
- Mapping validity, interval arithmetic, uncertainty propagation, logical-order representation and branch semantics.
- Meaning and API of anchor issuance vs resolution vs source capture and external attestation; authenticated namespace and offline recovery.
- How to express actual topology instance provenance without duplicating RI/History/OTEL ownership; bounded observation and retention.
- Whether to extract universal Chronon envelope: joint ADR/RFC, not accepted.
- Licensing: published spec README references LICENSE_SPEC but file is absent at inspected main; historical declarations differ. Review authority/rights and decide before a public normative release. No license modification here.
- Independent privacy, retention and erasure semantics owned by Vault/History, not this RFC.

Do not promote any contract until its owner explicitly accepts it. Review public source pins again before integration, because other candidate branches may advance independently. Keep old .rcg files and published code unchanged until a versioned migration with tests exists.
