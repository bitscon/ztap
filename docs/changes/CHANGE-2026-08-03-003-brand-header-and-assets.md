# Change Record

- **Date:** 2026-08-03
- **Type:** docs (brand surface — no spec/runtime change)
- **What changed:** Branded the repo's public face per the ZTI brand kit
  (`zti-adoption/brand/BRAND.md`): (1) `docs/assets/ztip-banner.svg` — README
  banner (dark/orange system, box mark, wordmark, protocol descriptor,
  request→verify→receipt lifecycle glyph; system-font fallbacks since GitHub
  blocks webfonts in embedded SVGs); (2) `docs/assets/ztip-social-card.png` —
  1280×640 social preview card (rendered with brand fonts; source template
  lives in the brand kit); (3) README header now carries the banner + a badge
  row (PyPI version, MIT, spec 1.0-draft, pre-release status — brand colors);
  existing copy untouched. Repo metadata set via GitHub API: description +
  topics (ai-governance, zero-trust, ai-agents, protocol, security, audit,
  integrity, ai-safety).
- **Why:** Operator-directed branding pass — one brand family across doctrine,
  protocol, and product; the open repo gets the open-standard expression of it.
- **Risk:** NONE — README/assets/metadata only; SPEC/SCHEMA/CONFORMANCE bodies
  deliberately carry no branding (kit rule). Badges are shields.io (external
  service, standard practice; verified rendering correct labels incl. PyPI
  v1.0.0.dev1).
- **Verified:** banner SVG renders correctly (Chromium screenshot reviewed);
  social card reviewed at 2× scale; all four badge URLs return correct labels;
  README image path relative and present; repo description/topics confirmed
  via API read-back.
- **Operator follow-up:** upload `docs/assets/ztip-social-card.png` as the
  social preview in GitHub repo Settings (no API exists for it).
