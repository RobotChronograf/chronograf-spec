# CHR-0.3A — Architectural Foundations

Date: 2026-11-27 · Target: Chronograf 0.3 · Status: **RFC candidate / non-normative / non-actuating**

This is an additive architecture proposal, not an adopted standard or a runtime release. The terms MUST/SHOULD below express proposed acceptance invariants only. Existing .rcg files, channel allocations, manifests, runtime APIs, license files and consumer contracts are unchanged. Merging this RFC does not imply acceptance.

## 1. Purpose

Chronograf is a universal temporal interoperability substrate for physical, virtual, distributed and cognitive systems. It represents qualified time, relationships between temporal coordinates and temporal evidence independently of application-specific state. A software-only agent, a laboratory instrument or a simulator must be able to adopt the neutral core without OpenRGD, RGD-Physics, robotics, cognition, networking or an external time service.

Chronograf does not invent a universal physical clock, establish truth of observations, grant authority, or imply that an agent is conscious. An authority is authoritative only for its explicitly defined domain, evidence and trust scope. Offline operation must remain possible; disconnected operation does not guarantee global accuracy or independent timestamp attestation.

## 2. Architectural decisions proposed for review

| ID | Candidate decision |
|---|---|
| A01 | One neutral temporal specification, with independently versioned application profiles. No core import of application schemas. |
| A02 | Distinguish clock domain, timescale, epoch, semantic layer, event origin and assurance; no implicit equality between them. |
| A03 | Preserve exact TimeAtom semantics, qualify coordinates, and never silently invent resolution, calibration or uncertainty. |
| A04 | Preserve all 23 existing v0.2 channel assignments. Semantic layers are an ontology of temporal roles, not five mandatory clocks. |
| A05 | Distinguish configuration topology (TTG) from actual recorded temporal provenance (TPG candidate). |
| A06 | Keep AnchorRef64 opaque and scoped; distinguish measurement, issuance, resolution, verification and external attestation. |
| A07 | Keep hard temporal constraints separate from quality metrics; application policy and hardware safety own actuation and fallback. |
| A08 | Do not move the Chronon semantic/ledger ownership in this RFC; one canonical history per verified Life scope. |
| A09 | Separate evidence from later interpretation; preserve original assertions and measured import/commit times. |
| A10 | Separate scientific hypotheses from engineering conformance; no THP score as a safety gate or intelligence certificate. |
| A11 | One canonical source of temporal definitions, reproducible manifests and versioned bindings; no copied normative registries. |

All A01–A11 remain proposed until reviewed by the appropriate owners.

## 3. Layers of responsibility

- **Chronograf specification:** coordinates, domains, uncertainty and assurance semantics, channels, mappings, temporal relations, anchor and temporal evidence contracts, topology and conformance profiles.
- **Clock provider / Chronograf implementation:** acquire or receive qualified readings, manage clock mappings and anchor issuance/resolution within a declared scope. Capabilities vary; a reader does not automatically become an issuer.
- **Runtime:** schedule and instrument processes, manage timers, report deadline outcomes and temporal anomalies. Scheduling semantics do not prove real-time execution. Application-owned safety mechanisms remain independent.
- **External source/provider:** attest actual acquisition when capable; preserve original claims and measurement provenance. Chronograf cannot certify a physical event it did not witness.
- **Application profiles:** bind generic channels/events to domain-specific semantics and constraints. OpenRGD owns its domain IDs, identities, morphology, policy, effects and role grants.
- **History/Physics and Cognition:** consume qualified references, own domain records and semantic interpretation as described in INTEROPERABILITY.md.

The dependency direction is consumer -> Chronograf contracts. No dependency on any external application service is required to parse, represent or locally compare valid neutral-core records.

## 4. Repository boundary

| Repository | Proposed role |
|---|---|
| chronograf-spec | Authoritative temporal language, registries, profiles, normative test vectors after acceptance |
| chronograf | Reference SDK/codecs and local provider candidate, subject to license and packaging review |
| chronograf-runtime | Optional execution and instrumentation services; no duplicate specification |
| chronograf-server | Optional network transport, witness and verification services; not required for offline core |
| website | Consumer of released contracts; demos explicitly labelled by assurance and origin |
| OpenRGD/openrgd | OpenRGD-owned temporal profile and producer/consumer bindings |

Historical archives remain evidence, not a second normative registry or runtime dependency. Existing repository names are retained; whether to split SDK and reference engine further is an open decision. No new repository or dependency is created here.

## 5. Reading order

- [Temporal model](TEMPORAL_MODEL.md): primitives, ontology, ordering, topology, assurance and anchor rules.
- [Interoperability](INTEROPERABILITY.md): ownership and compatibility with OpenRGD, History, Physics, Cognition and RI.
- [Review gates](REVIEW_GATES.md): failure cases, migration criteria and staged delivery.
- [Status](STATUS.json): non-normative machine-readable status.

## 6. Baselines reviewed

Public repository pins (independent; not a merged stack):
- [Chronograf spec baseline](https://github.com/RobotChronograf/chronograf-spec/tree/423c5d7a5b0ba645de6703c5789646eeb9186002) (kernel, channels, topology, manifest).
- [OpenRGD Agent temporal profile](https://github.com/OpenRGD/openrgd/blob/afe1a831b950a4e6560f0285a0103fc4eaa343b7/contracts/agent/v0.1.0/contracts/00_TEMPORAL_CHRONON_PROFILE.md).
- [OpenRGD CORE-D #14](https://github.com/OpenRGD/openrgd/tree/7b15fda5c825f9359ce0045377ec38364de19efb/contracts/temporal-memory/v0.1.0), including D-TIME-01 and History boundary.
- [OpenRGD RI review #17](https://github.com/OpenRGD/openrgd/blob/1a0f3f0408df8b6f86ab2bf1dcfe5eccc9e826a7/docs/reconciliation/ri/CORE_RI_01.md).
- [Cognition CORE-D consumer](https://github.com/OpenRGD/rgd-cognition/blob/a2e8690781d9acfa2c134a0ce9722285d0723d57/docs/COG-CORE-D.md).
- [RGD-Physics historical protocol](https://github.com/RGD-Physics/kernel/blob/265d79839fc3f86b4290f65597be38d40e86d97d/src/rgd_physics/chronon/interfaces.py).
- [HyperKernel vector implementation](https://github.com/RGD-Physics/hyperkernel/blob/8a6d6dbf0f533e2ed2cd1eb966e680920d999703/src/rgd_hyper/aions/vector.py).

The Agent and CORE-D contracts are themselves candidates. The public spec README declares Polymorf and references a missing LICENSE_SPEC. Existing license declarations differ across history; no relicensing, patent claim, or public release is authorized by this RFC.
