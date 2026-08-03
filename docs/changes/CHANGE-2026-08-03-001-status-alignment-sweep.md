# Change Record

- **Date:** 2026-08-03
- **Type:** docs
- **What changed:** Repo-wide status/consistency alignment — no normative protocol
  content changed. (1) `SPEC.md` status block and closing banner moved from
  `0.1-draft` / "Pre-Schema. Not for implementation." to the shared `1.0-draft`
  version string with an honest pre-release caveat (resolving the known
  discrepancy deferred in CHANGE-2026-07-31-002). (2) `SCHEMA.md` status block no
  longer forbids generating machine-readable schemas (they ship in `schemas/` and
  must stay in sync); closing banner updated to match. (3) All 10
  `examples/*.json` `draft_notice` annotations rewritten: hashes are real and
  recomputable (true since CHANGE-2026-07-31-001), field names remain draft.
  Annotation-only — underscore-prefixed keys are excluded from hashing, so no
  hash changed. (4) Stale "Next Steps" tails rewritten to delivered/remaining
  state: `SPEC.md` (Create SCHEMA/examples/WHITEPAPER → Delivered; open-question
  paragraph now names Q6/Q8 as the freeze gate), `SCHEMA.md` (create-list →
  delivered list + v1-freeze remainder; Open Questions intro/past-tense fixes),
  `CONFORMANCE.md` (create-list + "Prepare public GitHub launch" → delivered +
  fixtures/open-questions remainder), `VISION.md` "What Comes Next" (four
  delivered items now point at the shipped files; next = v1 freeze),
  `ROADMAP.md` and the whitepaper roadmap (delivered markers on Phase 3/4
  items). (5) Truthfulness fixes: `SECURITY.md` "ZTI Core SaaS" → "separate
  commercial product" and the `ztap/` runtime added to the security scope;
  `WHITEPAPER.md` "managed, commercial" → "supported commercial" and Level 2
  clarified self-hosted; `VISION.md` managed services marked future-optional;
  `CONTRIBUTING.md` scope now includes `ztap/` + `tests/` and the exclusion
  names commercial control-plane code instead of "SaaS/runtime". (6) Naming:
  "Zero-Trust Intelligence (ZTI) protocol family" → "Zero Trust Intelligence
  (ZTI) ecosystem" in `README.md` and `AUTHORS.md` (ZTI is the doctrine; ZTAP is
  the protocol). (7) `README.md` conceptual example version → `1.0-draft` and
  its stale hedge now points at `SCHEMA.md`/`schemas/`. (8) `CITATION.cff`
  `date-released` removed (nothing released; CHANGELOG says Unreleased).
  (9) `pyproject.toml` runtime version `0.1.0` → `1.0.0.dev1` (PEP 440
  pre-release aligned with the protocol draft). (10) Stale docstring in
  `scripts/recompute_example_hashes.py` updated to match the new notice.
  `CHANGELOG.md` entry added under 1.0-draft — Unreleased.
- **Why:** The repository contradicted its own shipped state: the canonical spec
  denied the version and implementability the rest of the repo (and the shipped
  schemas, examples, and runtime) asserted, and multiple tail sections
  instructed readers to create artifacts that already exist. AGENTS.md rule 2
  requires one shared version string across spec, schemas, and examples.
- **Risk:** LOW — documentation and annotations only. No envelope fields,
  hashes, schema files, or runtime code changed (one comment-only docstring
  edit; one package-metadata version bump that nothing imports).
- **Verified:** `scripts/validate-examples.py` → 10/10 pass; `ztap verify` →
  10/10 bundles verified (hashes unchanged); `pytest` → 8/8; `pyproject.toml`
  and `CITATION.cff` parse; repo-wide grep shows zero residue of the stale
  phrases ("0.1-draft", "Not for implementation", "Pre-Schema", "protocol
  family", "Core SaaS", illustrative-hash notices, create-directives) outside
  historical change records; two independent adversarial review passes plus a
  final in-context recheck — all findings resolved.
