# Change Record

- **Date:** 2026-07-31
- **Type:** feat
- **What changed:** Two protocol upgrades, drafted and adversarially reviewed (2 independent
  reviewer lenses; all blocker/major findings fixed before landing):
  1. **Completion Verification (new normative SPEC.md section).** An executor's claim of
     success is attestation, not verification. Required checks must pass under an authority
     independent of the executing target actor (control plane, designated validator, or
     deterministic re-execution). Fail-closed reason codes, with disjoint scopes:
     `VERIFY_FAILED` (check ran independently and failed), `COMPLETION_UNVERIFIED` (check
     satisfied only by attestation, never independently verified), `VERIFY_UNAVAILABLE`
     (verification could not run). Coherence edits: Verify Receipt step gains the
     independent-satisfaction bullet; the `verifying` lifecycle state and Walkthrough Step 7
     no longer model executor self-verification; SCHEMA.md `verification_actor` default no
     longer permits target-actor verification; new codes added to SPEC's category table,
     SCHEMA.md's Core Reason Code Registry, and the `reason_code` enum in
     `schemas/ztap-envelope.schema.json`.
  2. **Canonicalization finalized.** RFC 8785 (JCS) + SHA-256 is normative for v1
     (SPEC Algorithm section rewritten; Status, Open Question 9, and Next Steps updated).
     SCHEMA.md Hash Construction now states the full exclusion set exactly as the reference
     runtime computes it: `integrity.hash_value` removed (removal, not empty-string — the
     two are not hash-equivalent under JCS; the prior "either" wording was an ambiguity
     defect) and underscore-prefixed annotation keys stripped recursively. Resolved Open
     Question 7 aligned. Numeric section cross-references in SPEC.md converted to named
     references (the new section shifted numbering). README.md updated (draft status,
     runtime + CLI, specified-schema note); CHANGELOG.md updated under 1.0-draft Unreleased.
- **Why:** (1) is the protocol's answer to the documented 2025 failure mode of agents
  falsely reporting success — the axis no competing framework covers; it was already
  half-present in the artifacts (verification_requirements, `verifying` state,
  verification_results) but the spec never forbade self-verification. (2) closes the spec's
  own declared blocker ("must be finalized before the v1 schema is frozen") and makes
  SPEC, SCHEMA, schemas/, and the runtime state one identical hash rule.
- **Risk:** MEDIUM — normative language changed. Mitigations: version strings untouched
  (pre-existing 0.1-draft vs 1.0-draft discrepancy left alone, tracked separately);
  new reason codes added to the closed enum so conforming validators accept them;
  full validator + runtime sweep green. Known follow-ups (deliberately out of scope):
  CONFORMANCE.md L3 executor-duty reframing as attestation; examples/ receipts do not yet
  populate `verification_actor`; ZTI Core product mention still sits in SPEC's Core
  Concepts section (pre-existing).
- **Verified:** `python3 scripts/validate-examples.py` → 10/10 PASS;
  `python3 tests/test_runtime.py` → 8/8 PASS; `ztap verify` OK on all 10 bundles;
  `grep "Section 1[0-9]" SPEC.md` → empty; no `EXAMPLE-HASH-` placeholders.
- **ADR reference:** none (this repo records decisions in SPEC/SCHEMA + change records).
