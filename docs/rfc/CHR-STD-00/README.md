# CHR-STD-00 — Standardization and grammar continuity

Date: 2026-11-27. Status: **candidate editorial and compatibility policy**, not normative acceptance or a release.

## Decision direction

Retain OpenRGD/Chronograf's suffix-based, semantically typed naming convention, including representation suffixes. This is the owner's explicit design direction for new core contracts. Do not replace it with a suffix-free grammar. No existing field is renamed by this proposal.

The OpenRGD Master Schema is the existing source of shared naming, scalar, enum and struct conventions. Chronograf specializes that convention for time. It does not create a competing OpenRGD master schema or require OpenRGD runtime installation. Existing contracts remain authoritative for their exact version and scope; the grammar is an authoring policy, never a decoder or authority mechanism.

## Scope

- [Grammar profile](GRAMMAR_PROFILE.md) — preserve and clarify suffix usage.
- [Source and compatibility review](COMPATIBILITY.md) — exact source pins, divergences and migration rules.
- [Specification policy](SPECIFICATION_POLICY.md) — documents, normative requirements, registries, encoding and conformance.
- [Research entry](RESEARCH_ENTRY.md) — gate and conventions for the scientific program.
- [Status](STATUS.json) — explicit candidate maturity.

This RFC consolidates rather than replaces previous work. CHR-0.3A #1 is an independent architecture candidate; this proposal can be reviewed separately. Nothing here modifies its proposed ownership boundaries or freezes the future TimeAtom wire format.

No files from the private historical archive are published by this RFC. Historical claims, scientific hypotheses and licensing ambiguities remain subject to review. The scope is additive documentation only.
