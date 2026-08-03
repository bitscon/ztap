# Changelog

## 1.0-draft — Unreleased

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
- Reference runtime: `ztap/` package (RFC 8785 canonicalization, SHA-256 hashing, hash-chain
  verification) with `ztap hash` and `ztap verify` CLI commands.
- Example integrity hashes are real and recomputable with the reference runtime.
- Status alignment: `SPEC.md` now carries the shared `1.0-draft` version string; stale
  pre-schema / not-for-implementation notices replaced across spec, schema status blocks,
  and example draft notices to match the shipped schemas and runtime.
