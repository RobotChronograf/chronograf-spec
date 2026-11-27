# CHR-0.3A — Temporal model

Status: architectural candidate; type names below describe semantic responsibilities, not finalized wire schemas. Reuse existing compatible names and version any semantic delta.

## 1. Primitive register

| Primitive | Meaning and boundary |
|---|---|
| ClockDomainRef | Stable identity of a particular clock or logical coordinate domain, scoped to issuer, epoch/generation/boot as appropriate; not a semantic layer ID. |
| TimeAtom | Exact coordinate in a declared dimensional time domain. Preserve existing v1 fields; require unambiguous domain binding. |
| LogicalOrderRef | Counter/vector or other logical order evidence. No seconds or physical duration inferred without a separately verified mapping. |
| TimeInterval / Duration | Qualified interval or elapsed quantity with explicit domain, unit, boundary and uncertainty; duration is not an instant. |
| ClockMapping | Versioned evidence relating domain coordinates, with validity range, mapping parameters, uncertainty, direction and provenance. |
| Uncertainty | Explicit bounds or probabilistic model, with semantics, units and evidence. Unknown/unbounded are not zero. |
| TemporalAssuranceProfile | Structured claims about source and measurement quality, integrity, continuity and verification; not a single score. |
| TemporalChannelRef | Versioned registry + stable channel ID; channel instance identity is separate. RGC-16 is an address, not a timestamp or checksum. |
| TemporalBarcode | Event-time envelope with qualified coordinate/anchor, role, channel, event kind and typed external context references. Existing OpenRGD v1 barcode requires application domain; the neutral profile must not. |
| ChronografAnchorRef64 / AnchorRecord | Existing scoped opaque reference and immutable resolution record, not event ID or proof of actuation. |
| TemporalRelation | Typed relationship between externally owned events/activities/data; includes evidence and provenance. |
| TemporalTopologyGraph (TTG) | Declared configuration: dependency and timing constraints, scheduling hints, policies and profiles. |
| TemporalProvenanceGraph (TPG, candidate name) | Recorded event/usage/temporal relation view; not a new application ledger or causal oracle. |
| TemporalAttestation | A scoped signed statement or externally verifiable receipt about defined bytes/claims under a trust policy. Separate from measurement and content hash. |
| TemporalManifest | Deterministic derivation of versioned inputs and their commitments; signature and verification profile separate. |

New names are not claims of original inventions. The TAP, ClockMapping, logical order, typed relation and TPG schemas require later review; do not publish an incompatible v1 implementation based on this table.

## 2. Coordinate semantics

For the existing decimal encoding, the coordinate is seconds + ticks * 10^exponent relative to a declared epoch and scale. For a normalized decimal fraction with exponent e <= 0, 0 <= ticks < 10^(-e). Use exact integer arithmetic; negative instants use floor-normalized seconds and nonnegative fractions. This is a candidate semantic rule, with precise field bounds, wire widths, supported exponents and canonical representation deferred to 0.3B. Civil time with leap seconds needs an explicit versioned conversion model; no implicit POSIX/UTC/TAI/GPS equivalence.

Representable tick resolution is not actual acquisition accuracy, uncertainty, jitter or precision. Do not infer microsecond accuracy from a microsecond field, or label a POSIX clock TAI without a verified conversion. Clock-domain identity includes necessary session/boot/epoch context; two raw equal values from distinct domains are not equal instants. UTC wall clocks can step; local monotonic clocks need not survive reboot. No use of floating point or unsafe JSON number coercion for full-width integers; canonical decimal-string transport or an exact integer codec to be decided in 0.3B with compatibility fixtures.

For comparison in a common qualified domain, conservative intervals I_a=[a_min,a_max] and I_b=[b_min,b_max] imply a strictly precedes b only when a_max < b_min. Overlap does not imply equality, simultaneity or causation. For other domains, use applicable mapped intervals and mapping uncertainty; if absent/expired/ambiguous, return UNKNOWN/INCOMPARABLE. A confidence interval is not a deterministic bound; state its coverage and assumptions. Relative uncertainty depends on shared clocks and correlations, not blindly summing absolute UTC errors.

## 3. Semantic ontology

The five historic layers remain. They classify temporal roles and may share clocks; a domain can be used by many channels and a channel can carry references to different domains with explicit roles.

| Layer | Existing RGC-16 prefix | Candidate interpretation |
|---|---|---|
| CHRONOS | 0x1xxx | Measured physical timing and operational elapsed time. Distinguish real host time from simulator coordinates. |
| KAIROS | 0x2xxx | Scheduling, deliberation, prediction, oneiric/replay and internal time windows. Virtual rate changes do not create extra physical computation. |
| AION | 0x3xxx | Relational rhythms, coordination, message order and social time; not the Aion payload type. |
| METACHRONOS | 0x4xxx | Temporal policies, integrity, constraints, observability and continuity. |
| ESCHATON | 0xFxxx | Termination, emergency and graceful-boundary events; not authority to execute a shutdown. |

The 23 IDs in [the pinned v0.2 channel registry](https://github.com/RobotChronograf/chronograf-spec/blob/423c5d7a5b0ba645de6703c5789646eeb9186002/spec/chronograf/layers/time_channels.rcg) are retained without renumbering. In particular the seven existing METACHRONOS codes (ANANKE, ALETHEIA, SYMPATHEIA, ENARGEIA, PHYSIS, HYPOSTASIS, PALINGENESIA) retain their documented semantics. ANANKE reports hard-constraint context; ALETHEIA integrity/evidence; ENARGEIA observable temporal structure. Identity verification, safe actions and migration authorization belong to application owners, not channel IDs. ESC_PAN_REQUEST 0xF000 is the existing panic request; historical cosmological use of that code is not silently restored.

Clock kind, time scale, role/layer, provenance/origin (observed/source-claimed/synthetic/unknown), and trust profile are orthogonal axes. A simulation may run at a varying rate, pause, branch or traverse a model backwards. Represent branches by distinct domain/generation identities and versioned mapping segments; do not imply reversal of physical history or globally total order. Physical mappings used for chronological assertions must be order-preserving within their declared validity. Logical clocks describe partial order, not UTC. Neither a simulated outcome nor a prediction is proof of a physical occurrence.

## 4. Time roles and provenance

The following are distinct roles, not seven mandatory timestamps on every object:

| Role | Scope |
|---|---|
| EVENT / VALID | When a source claims the event occurred or state held. Can be a claim, interval or unknown. |
| CAPTURE | Actual observation acquisition interval or instant, only qualified when evidence supports it. |
| AVAILABILITY | When data became accessible to a specific consumer/boundary; may differ by receiver and may be revoked. |
| CONSUMPTION | When a particular invocation used a specific data revision; property of the usage edge. |
| INFERENCE | Start/end or output generation of a computation, with actual processing domain. |
| COMMIT | Actual acceptance/persistence event measured at the appropriate boundary; writer receipt separate. |
| REVIEW | Later interpretation or assessment, linked to original evidence; never silently retroactive. |

Additionally distinguish command send, receipt, physical actuation start/end, result observation, anchor issue, and import time where relevant. Not all events have a total order; only enforce constraints that follow from a typed relation and comparable clock evidence. A source time assertion is not an anchor. Time roles describe events/edges, not evidence that a computation actually used data. Preserve unknown and not applicable separately.

TTG describes planned loops, dependencies and constraints. Cyclic feedback at configuration level is legitimate. TPG describes actual recorded usage/generation, observations, revisions and timing of specific instances; a verified happens-before subgraph cannot have cycles, but arbitrary semantic references need not form a DAG. Provenance is not proof of physical causation. Use scoped references, explicit relation type, source and target revisions, typed clock evidence and verification status. Incomplete traces must remain visibly incomplete.

For source observation o consumed by invocation p and used by action a, evaluate source age at the relevant decision or actuation time, not only age of the intermediate output. Where mapped bounds exist, a conservative upper age is a_upper - capture_lower; compare with declared end-to-end budget. Track relevant ancestors independently for multi-source data, propagate uncertainty and missing links; do not assume every causal ancestor must be fresh or sum unrelated ages. A newly generated inference does not reset the underlying observation age. Runtime safety owner derives actual budgets and handles missing or violated critical constraints; temporal monitoring is not a certified safety controller.

## 5. Offline and assurance

A local provider must be able to represent and compare its qualified local time with no network. Distinguish source synchronization state, holdover, discontinuity, loss of reference, and unknown global mapping. Propagate bounds over holdover only when a justified drift model and elapsed-time evidence exist. Unknown global uncertainty remains unknown; neither local clock precision nor clock persistence proves absolute accuracy.

TAP candidate dimensions: representable resolution; source accuracy/uncertainty and model/coverage; clock source and calibration/reference chain; synchronization/holdover validity; continuity/reset/rollback evidence; capture-path binding; artifact integrity/authentication; independent external time attestation; scope/coverage/completeness and verification result. These are separable claims, not statistically independent axes or ordered grades. A signer may attest an incorrect claim. Intentional HRI delay, age, queueing and processing latency are not measurement uncertainty.

AnchorRef64 retains namespace + opaque uint64 handle + TimeAtom SHA-256. Zero is invalid; allocation order only within the same namespace. Do not decode handle as time or order different namespaces numerically. AnchorRecord binds exact TimeAtom, domain, issuance context and integrity; the existing TimeAtom hash must not silently change definition. Domain binding and canonical hash encoding are review gates. Multiple events may intentionally refer to a common coordinate without claiming exact simultaneity. Verified resolution checks reference and record integrity and issuer policy; a hash alone authenticates neither source nor time.

Proof of Instant is a candidate attestation profile, not proof of physical capture by definition. Local commitment/signature proves only what the verified trust assumptions justify; independent witnesses may bound commitment formation/existence within a qualified interval. Acquisition time requires independently trustworthy sensor-clock-commit provenance. Later witnesses append receipts, never modify original anchors or backdate capture. No mandatory server or network for core operation; no claim of equivalent assurance offline.

## 6. Scientific boundary

The Temporal Harmonic Principle remains a research program. Its original scalar metrics are not normative or an intelligence measure. Record vector-valued temporal performance (deadline violations, peak/quantiles, uncertainty coverage, unknown fraction) and test adaptation through independent controlled experiments. Hard constraints and quality are separate; an average cannot compensate for a critical violation. Chronon geometry, CFT, experience assimilation, Kairotic Moment optimization and cognitive effects require their own empirical/mathematical review. This architecture is useful even if those hypotheses are rejected.
