# Changelog

## 1.0-draft — Unreleased

- **Protocol renamed: ZTAP → ZTIP (Zero Trust Intelligence Protocol)** — repo, package,
  CLI (`ztip hash` / `ztip verify`), schema filenames, and all documentation. The envelope
  field `ztap_version` is deliberately retained as a legacy name for hash stability (it sits
  inside the canonicalized content that envelope hashes cover); see the legacy-field note in
  `SCHEMA.md`. No hashes or envelope semantics changed.

- Initial protocol doctrine.
- `SPEC.md` baseline protocol definition.
- `SCHEMA.md` envelope and field model.
- `CONFORMANCE.md` conformance requirements and invariants.
- JSON Schema Draft 2020-12 files under `schemas/`.
- 10 protocol lifecycle examples under `examples/`.
- Example validation script: `scripts/validate-examples.py`.
- Completion verification: new normative `SPEC.md` section — independent verification of
  executor results; attestation never satisfies a required check; fail-closed via
  `COMPLETION_UNVERIFIED` / `VERIFY_UNAVAILABLE`.
- Canonicalization finalized: RFC 8785 (JSON Canonicalization Scheme) with SHA-256, normative
  in `SPEC.md` and `SCHEMA.md` (hash computed with `integrity.hash_value` removed and
  underscore-prefixed annotation keys stripped).
- Reference runtime: `ztip/` package (RFC 8785 canonicalization, SHA-256 hashing, hash-chain
  verification) with `ztip hash` and `ztip verify` CLI commands.
- Example integrity hashes are real and recomputable with the reference runtime.
- Status alignment: `SPEC.md` now carries the shared `1.0-draft` version string; stale
  pre-schema / not-for-implementation notices replaced across spec, schema status blocks,
  and example draft notices to match the shipped schemas and runtime.
