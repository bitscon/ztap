# Change Record

- **Date:** 2026-08-03
- **Type:** docs (IETF Internet-Draft — priority stake, NOT yet submitted)
- **What changed:** New `docs/ietf/draft-mccormack-ztip-00.xml` (xml2rfc v3
  source) + generated `.txt` — "The Zero Trust Intelligence Protocol (ZTIP):
  Governed, Independently Verified AI Agent Transactions." Individual
  submission, informational intent, author Chad McCormack / Zero Trust
  Intelligence. Condenses the protocol for the record: terminology and the
  nine roles, the 12-state lifecycle, the five envelope types, the integrity
  model (RFC 8785 JCS + SHA-256, hash-exclusion rule, the ztap_version
  legacy-field note), the completion-verification semantics as the normative
  heart (independence requirement; attestation never satisfies a required
  check; fail-closed VERIFY_FAILED / COMPLETION_UNVERIFIED /
  VERIFY_UNAVAILABLE), conformance levels, transport independence, security
  considerations. Explicitly states it does not represent IETF consensus and
  points to the repo as the authoritative spec.
- **Why:** Operator-approved posture after the standards-lane recon: a dated,
  neutral, citable priority stake for the verified-done semantics — no
  working-group campaign.
- **Risk:** NONE until submitted (a repo doc). Submission to datatracker is a
  separate operator-gated step; I-Ds expire ~6 months after posting and need
  a re-post (10 minutes).
- **Verified:** xml2rfc renders clean with zero warnings (17,979-byte text,
  ~8 pages); content cross-checked against SPEC.md (states, roles, envelope
  types, reason-code semantics, hash rule verbatim-faithful); BCP 14
  boilerplate present; references resolve via bib.ietf.org includes.
