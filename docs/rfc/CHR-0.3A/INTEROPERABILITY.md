# CHR-0.3A — Interoperability and ownership

Status: candidate, no schema promotion or live integration.

## 1. One owner per authoritative object

| Object / claim | Owning authority or component | Chronograf contribution |
|---|---|---|
| Qualified temporal coordinate / domain / mapping / anchor | Chronograf provider within verified scope | Define representation and verification |
| Original observation, payload, source envelope | Source/Reality Ingress and authorized Evidence Vault | Qualified capture/receipt/availability refs, uncertainty; no payload ownership |
| Spatial frame, morphology, calibration, physics validity | OpenRGD, CAL, EVOL, Physics according to their contracts | Temporal validity/context, not spatial validation |
| Life, entity, identity, writer lease/fencing, permissions and effects | OpenRGD Identity/Life and external gates | Time qualification; no enrollment, authorization or role minting |
| Canonical Chronon and writer receipt | RGD-Physics / History per Agent v0.1 and CORE-D candidate | Resolve qualified anchors, temporal evidence and relations |
| Aion payload / packed codec | RGD-Physics lineage | Opaque anchor semantics only |
| HyperAion, world/self model, goals, intentions, learning | Cognition / HyperKernel / relevant application owner | Timing and provenance; no reasoning or action approval |
| Memory, facts, summaries, skills, autobiography | Memory projection owners; L3/L4 derived from L2 | Temporal qualifications for query, not memory management |
| Ethical assessment and DecisionTrace | Policy/Ethos owner and effect gate | Evidence refs; no moral correctness proof |
| Retention, erasure, access control | Vault/History/Memory and governance | Timestamped assessments only, no privacy certification |
| Actual actuation and safety fallback | Somatic / independent authorized safety control | Temporal condition report, never an effect grant |

L0 volatile telemetry, L1 protected evidence, L2 canonical history, L3 memory and L4 autobiography retain CORE-D separation. No second ledger of robot existence in Chronograf. Temporal record storage is not History. TPG is a scoped view/relation contract on event evidence (not a competing event store); app owners keep their source records and causal hypotheses.

## 2. Existing contract preservation and identified deltas

The public Agent v0.1 profile assigns Chronon semantics to RGD-Physics and anchor issuance/resolution to Chronograf. CORE-D #14 preserves that boundary and proposes a corrected legacy import process. Treat both as independent candidates, not released authority services.

| Existing surface | Disposition |
|---|---|
| ClockDomainRef | Keep type/meaning; clarify required scope and epoch/boot binding; physical units vs logical order explicit. |
| TimeAtom v1 | Preserve representation as legacy profile; 0.3B defines compatible qualification and versioned exact encoding/canonicalization. |
| Temporal Barcode v1 | Existing OpenRGD primary_domain remains required for that profile; universal profile removes dependency on OpenRGD enum by explicit versioned binding, never silently weakening v1. |
| ChronografAnchorRef64 | Preserve namespace, handle and TimeAtom hash; resolution record binds domain and issuance proof. No truncation into 64-bit time. |
| HistoricalTimeAssertion / ImportAnchorEvidence | Adopt CORE-D direction for non-retroactivity, subject to owner acceptance. |
| HistoryCommitRequest/Receipt | External writer owns verified Life/lease, gate, idempotency, durable acknowledgement/query. Chronograf does not emit COMMITTED. |
| ObservationRef | Preserve RI scope, source/host/boot/receipt and missing sensor capture; no new competing ObservationRef. |
| MemoryAnnotation / OneiricReview | Preserve separate valid/knowledge times, revision links, explicit synthetic status and non-authority. |
| Historical packed Aions | Preserve documented legacy wire compatibility, explicit codec versions and namespaces; do not reinterpret old anchor-as-timestamp bits as opaque handle. |

The old Physics ChrononProtocol docstring describes anchor as timestamp plus entity. This conflicts with opaque AnchorRef64; any migration needs explicit legacy decoding or rejection and a versioned adapter, not a reinterpretation. Aion128/512/4096 and historical Aion16384 are codec profiles, not Chronograf primitives. Aion16384 payload name is not total wire length. HyperAion512 vector semantics and canonical endian/shape validation belong to Physics/Cognition reconciliation. AION layer, Aion payload, HyperAion representation and temporal alignment infrastructure remain distinct. No duplicate ontology created.

An application-neutral history envelope may eventually allow Chronon-like history outside Physics. Ownership and naming require a separate joint RFC covering the single-ledger invariant, consumer migration, evidence availability and compatibility. Until approved, Chronograf provides sufficient neutral time primitives to non-robotic consumers without requiring them to adopt Chronon. No Chronon extraction in 0.3A.

## 3. Example of temporal truth

A source reports a frame capture at T0, a host receives it at T1, perception uses it at T2 and produces a label at T3, planner consumes that label at T4, an independent gate permits an action and a driver reports actuation at T5, History persists a selected event at T6, and later cognition reinterprets the frame at T7. All are separate typed claims, not a universal total-order formula. Capture may be unknown; the host receipt is not capture. TPG links exact revisions and consumed evidence, not the private reasoning of a model. The underlying frame age at T5 comes from T0, not T3. If T0 is unqualified or cross-domain mapping is unknown, do not invent a freshness guarantee. A label produced later never becomes evidence that the earlier decision knew it. History receipt T6 is not proof that action occurred.

AS_KNOWN_AT(T) is a History/Memory query scoped to verified availability/commit semantics, not a raw timestamp filter or a guarantee of actual consumption. Actual consumption requires the usage relation. CURRENT_ASSESSMENT_OF(T_event) may return newer interpretation, preserving original evidence subject to privacy/access constraints. A historical import preserves the old source claim and obtains a separate actual measurement for import/commit. No fake past anchor. If no clock/writer available, retain evidence and report NOT_CONFIRMED or defer according to owner contract.

## 4. Consumer handoff

- CORE-D #14: Chronograf candidate provides qualified import/commit-time reference and resolver semantics; reject invented anchors. Separate ownership review before versioned delta to Agent profile section 11.
- CORE-RI-01 #17 / RI: host receipt is not sensor capture. Preserve exact integer ns and scoped host/boot IDs, origin/status; source time and anchor may be absent. Authorized resolver remains RI/Vault responsibility; no arbitrary URI fetch.
- COG: local session monotonic time does not become TimeAtom/History merely by schema validation. Oneiric reviews stay synthetic; blocked history remains blocked until actual Life, effect gate and authenticated writer are connected.
- EVOL: migration and reboot continuity are temporal evidence categories; actual Life continuity and as-built changes must be independently verified. No implicit identity from matching channel.
- Physics/History: joint anchor resolution/legacy codec review and writer receipt tests. No assumption that prototype hash-based laws certify physics.
- Console/Chronoscope/Visual Feedback/website: consume released temporal schemas and assurance indicators, no second clock protocol; UI must distinguish local/simulated/unverified/attested. Display is not proof.
- RGD-OS / module registry: use versioned published interface and artifact trust policy; do not register a runtime implementation until release/conformance, no new module installation in this RFC.

Handoffs are requirements for subsequent owner review, not changes to other repositories.
