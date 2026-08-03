# Change Record

- **Date:** 2026-08-03
- **Type:** feat (protocol rename — operator decision D11)
- **What changed:** The protocol is renamed **ZTAP → ZTIP (Zero Trust Intelligence
  Protocol)**, operator-approved 2026-08-03 after a trademark/naming review (the
  prior working name collides with a live third-party US registration in the same
  class, and its search space was already occupied). Applied across the repo:
  package dir `ztap/` → `ztip/` (imports updated in `tests/`, `scripts/`),
  pyproject name/CLI `ztap` → `ztip` (`ztip hash` / `ztip verify`), schema files
  `ztap-envelope/-bundle.schema.json` → `ztip-*` (refs updated), example
  annotation key `_ztap_example` → `_ztip_example` (underscore-stripped from
  hashing — hash-safe), example IDs (`ztap-txn-*` etc.) → `ztip-*`, long name
  "Zero Trust Agent Protocol" → "Zero Trust Intelligence Protocol", repo URLs →
  `github.com/bitscon/ztip`, and all doc prose. Historical records under
  `docs/changes/` are untouched.
- **Deliberately NOT renamed:** the envelope field **`ztap_version`** — it sits
  inside the RFC 8785 canonicalized content that envelope hashes cover, so
  renaming it would invalidate every existing hash and receipt. It is retained as
  a documented legacy field name (notes added in `SCHEMA.md` Section 5 +
  Versioning, and the `README.md` conceptual example).
- **Hash regeneration:** renaming the example envelope IDs changed hashed
  content, so all example integrity hashes were regenerated **by tooling**
  (AGENTS.md rule 4): `scripts/recompute_example_hashes.py` gained a
  `--refresh` mode (same dependency-order resolution as placeholder mode, keyed
  on stale current hashes; external illustrative digests pass through
  untouched). 69 hash values refreshed across the 10 bundles, including
  cross-references (`request_hash`, child/parent links).
- **Why:** D11. The rename window (zero forks, nothing on PyPI) closes at
  launch; ZTIP's search lanes and registries were verified clean and the name
  binds the protocol to the ZTI brand.
- **Risk:** LOW-MEDIUM — no protocol semantics changed (lifecycle, fields,
  canonicalization, hashing rules all identical; the one field name is
  explicitly preserved). Example hashes changed by necessity and were
  regenerated + verified by the runtime. Downstream: the GitHub repo rename is
  covered by GitHub's automatic redirect (existing
  `pip install git+.../ztap.git` keeps working); sibling repos (zticore,
  zti-adoption, zerotrustintelligence) are updated in their own change records.
- **Verified:** `scripts/validate-examples.py` 10/10; `ztip verify` 10/10
  bundles (integrity + chain clean); `pytest` 8/8; `--refresh` idempotent
  (second run = 0 replacements); repo-wide grep confirms the only remaining
  "ztap" outside historical records is the documented `ztap_version` legacy
  field (64 occurrences); pyproject + CITATION parse clean.
