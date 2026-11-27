# CHR-STD-02 — Suffix-typed core grammar

Status: candidate clarification of the existing OpenRGD / Chronograf convention.

## 1. Principles

Use lower_snake_case for newly authored core record keys and UPPER_SNAKE_CASE for symbolic enum values unless an existing registry specifies another spelling. Preserve case-sensitive registered values, acronyms, identifiers, historical field names and protocol version semantics. Type/record names in prose may use PascalCase, e.g. TimeAtom, ClockDomainRef and TemporalBarcode. Existing types and names are not renamed.

A field name describes meaning, dimensions and logical/representation type. The conventional composition for new names is:

    semantic_stem [ _ semantic_qualifier ] [ _ unit_or_encoding ] _ type_or_structure

This is a descriptive pattern, not an exhaustive ABNF for existing fields. More than one qualifier may be needed; use established names before inventing variants. A schema remains the exact source of truth for admissible values, dimensions, ranges, lexical forms and encoding. Never derive authorization, trustworthy provenance or a valid clock simply from a suffix.

The semantic stem should be explicit (capture, receipt, consumption, commit, etc.), not just timestamp when multiple roles exist. Names encode neither a hidden implementation choice nor a claim of measurement accuracy.

## 2. Existing suffix families

| Suffix / family | Source-backed convention and proposed usage |
|---|---|
| _str | UTF-8 string; context determines semantics and schema defines actual constraints. |
| _id_str | Identifier within a declared namespace; use the existing identifier profile when compatible. |
| _ref_str | Typed reference to a scoped target; the string is not permission to resolve it. |
| _int | Integer; Master Schema historically indicates a 32-bit-safe range unless specified otherwise. Specify exact bounds for each new field, not an inferred machine width. |
| _uint / _uint64 | Nonnegative integer / explicitly 64-bit unsigned logical value; seen in the TimeAtom and AnchorRef64 lineage. Specify range and representation. |
| _float | IEEE 754 numeric representation in the Master Schema; width, finite values, rounding, range and errors must be explicit for a new wire profile. Not an appropriate default for exact temporal coordinates. |
| _bool | Boolean true/false, not integer/string coercion. |
| _enum / _enum_str | Registered symbolic value. Both exist historically; use _enum_str for new Chronograf symbolic string fields when consistent with TimeAtom/Barcode, _enum where an inherited OpenRGD profile requires it. No alias guessing. |
| _iso8601_str | A text date/time profile; exact accepted syntax, scale, timezone and precision must be specified. Does not establish time-source quality. |
| _uri_str | URI string under a stated scheme and resolution policy. |
| _semver_str | Version identifier under the declared version profile. |
| _hex_str / _sha256_hex_str | Lexical hex string / digest with explicit algorithm, byte preimage, length and casing. Not a signature. |
| _group | Named group of related object fields; not an automatically extensible namespace. |
| _obj | Nested object / typed record; schema declares required and optional members. |
| _map | Object used as a key-to-value mapping; specify key space, value schema and bounds. |
| _list / _arr | JSON arrays in existing material. Preserve both. For new core records prefer _arr for collections of records/references and _list for descriptive configuration lists, where no inherited name exists. This is editorial, not a semantic difference in array ordering, uniqueness or set membership. |
| _struct | Reusable structural definition, e.g. meta_group_struct in the Master Schema. Not automatically a serialized field type. |

The compound forms _enum_str, _list_enum, _id_hex_str and _sha256_hex_str have historical precedents. Do not blanket-lint them out. _group/_obj/_map and _arr/_list do not imply equivalence between distinct fields. All shape, ordering, cardinality, uniqueness and unknown-member behavior must be defined in the exact schema.

## 3. Dimensions and units

Retain unit qualifiers (duration_s_float, latency_ms_int, target_frequency_hz_float, max_drift_ppm_float) rather than remove them. Use a single declared unit and scale for each fixed-unit quantity; no silent conversions. Unit tokens in keys are ASCII spellings, not SI typographical symbols. In normative prose use the correct symbols and dimension (s, ms, ns, Hz, etc.). A unit table belongs to the applicable type/encoding profile, not implicit conversion based on suffix.

Keep historical epoch_seconds_int and tick_resolution_exp10_int. Existing aliases such as seconds vs s are not grounds for renaming. The exponent is dimensionless and defines a power of ten relative to the declared unit. Distinguish resolution, accuracy, uncertainty, delay, jitter, drift, and relative error. A finite default must not represent an unknown measurement uncertainty. Logical counters and opaque references are not elapsed seconds.

## 4. Representation vs schema

The following are existing names, not a new schema:

    epoch_seconds_int
    subsecond_ticks_uint
    tick_resolution_exp10_int
    timescale_enum_str
    uncertainty_group
    sync_class_enum_str
    reference_chain_arr

Their mathematical domain, exact wire ranges, normalization, clock-domain binding, uncertainty and canonical encoding are review topics for CHR-0.3B. Preserve field names and semantics within the declared existing profile. New schema versions may choose an exact decimal-string carrier where necessary; distinguish logical uint64 from JSON string (the already proposed CORE-D anchor_handle_uint64_dec is an example, not a global rename). New carrier names must identify the actual encoding or explicitly document the inherited exception. Do not fix a wire width just because it is common in one language.

For each newly specified field provide:

- exact key, abstract type, unit/dimension and meaning;
- concrete schema and permitted encodings, bounds and normalization;
- presence/null/unknown/not-applicable semantics;
- references, scope, validation and failure behavior;
- compatibility version, requirement ID and test evidence when adopted.

A suffix cannot alone distinguish missing values from null, empty collections, zero or UNKNOWN. Never coerce between these to achieve validation success.

## 5. Scope of enforcement

Apply this authoring profile to new Chronograf core protocol fields and new native schemas after adoption. Existing OpenRGD contracts, external bindings, standards-defined fields, generated mirrors, JSON Schema keywords, code identifiers and mathematical symbols keep their own grammar. Exact versioned field contracts outrank naming conventions. Do not import new runtime dependencies on OpenRGD, create a shared executable linter prematurely, or rewrite another repository.

Future grammar conformance will check new fields against their declared schema and explicit exceptions; it will not mutate received bytes. Linting policy and schema validation are separate. No claim of a complete parser, ABNF, normative type registry or implemented validator is made here.
