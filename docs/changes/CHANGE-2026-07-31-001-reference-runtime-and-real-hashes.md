# Change Record

- **Date:** 2026-07-31
- **Type:** feat
- **What changed:** Added the ZTAP reference runtime: `ztap/` package implementing
  RFC 8785 (JCS) canonicalization (`canonical.py`), SHA-256 envelope hashing with the
  `integrity.hash_value`-removal + underscore-annotation-stripping rules (`hashing.py`),
  bundle integrity/chain verification (`chain.py`), and a `ztap` CLI (`cli.py`: `ztap hash`,
  `ztap verify`, fail-closed). Added `pyproject.toml` (package `ztap` 0.1.0, MIT, console
  script) and `tests/test_runtime.py` (8 tests). Added
  `scripts/recompute_example_hashes.py` and regenerated all `examples/*.json` integrity
  hashes: every `EXAMPLE-HASH-*` placeholder replaced with a real, recomputable SHA-256.
  References to content outside a bundle (external evidence, registry state snapshots,
  child envelopes omitted for brevity) carry a deterministic illustrative digest of their
  descriptor, per the tooling's documented rule.
- **Why:** AGENTS.md rule 3 declares placeholder hashes a defect; the spec deferred
  canonicalization, leaving the protocol unimplementable and its examples unverifiable.
  The runtime converts the standard from paper to something anyone can run, and makes the
  examples' integrity claims literally true.
- **Risk:** LOW-MEDIUM — no protocol semantics changed; example hash VALUES changed
  (placeholders → real). Any external consumer that pinned placeholder strings would break;
  none are known and placeholders were self-evidently non-normative.
- **Verified:** `python3 scripts/validate-examples.py` → 10/10 PASS;
  `python3 tests/test_runtime.py` → 8/8 PASS; `ztap verify` → OK on all 10 example bundles;
  `grep -rl EXAMPLE-HASH- examples/` → empty; tamper test (mutating a sealed envelope)
  flips verification to False.
- **ADR reference:** none (reference implementation of existing spec intent; protocol
  decisions recorded in CHANGE-2026-07-31-002).
