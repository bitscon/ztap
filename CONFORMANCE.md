# ZTAP Conformance Draft

*Zero Trust Agent Protocol — What It Means to Be Compliant*

---

## Status

**DRAFT — Conformance target for ZTAP `1.0-draft`.**

This document defines conformance requirements for implementations of the Zero Trust Agent
Protocol. It is derived from `SPEC.md` and `SCHEMA.md`. Where this document conflicts with
those, `SPEC.md` is authoritative on governance model and lifecycle, and `SCHEMA.md` is
authoritative on field definitions.

This is an early draft. Conformance test fixtures, certification procedures, and formal
conformance claim formats have not yet been defined.

Do not build production certification processes against this draft.

---

## Conformance Philosophy

ZTAP conformance is grounded in the following non-negotiable principles:

**Fail-closed is a protocol invariant, not a configuration option.**
A conforming implementation must reject invalid, unknown, expired, tampered, or unauthorized
transactions under all circumstances. There is no permissive fallback mode. Ambiguity resolves
to denial.

**Integrity is mandatory.**
Every ZTAP envelope must carry a valid `integrity` object. Implementations must compute and
verify hashes. An envelope without a verifiable hash is not a ZTAP envelope.

**Encryption is policy-conditional.**
ZTAP v1 does not require encryption. Envelopes are plain JSON by default and must be human-
auditable without decryption. Encryption may be layered on top for specific deployment
contexts, but it is not a core conformance requirement and must not be a prerequisite for
envelope processing.

**Transport is out of scope.**
ZTAP conformance is not concerned with how envelopes are delivered. A conforming
implementation must not assume any transport. Governance is enforced at the envelope level,
not at the network layer.

**ZTAP governs the action, not the pipe.**
A conforming actor, runtime, or control plane must refuse governed work unless a valid,
verified ZTAP authorization record exists for the specific action being requested. The fact
that a message arrived over a secure channel does not make it authorized. The authorization
record governs. The transport does not.

---

## Conformance Levels

ZTAP defines three conformance levels. Higher levels include the requirements of all lower
levels. A conforming implementation must declare which level it targets.

---

### Level 1 — Envelope Validator

An Envelope Validator can parse, validate, and report on the structural correctness of ZTAP
envelopes. It does not need to evaluate policy, manage actor registrations, or process
transactions end-to-end.

**An Envelope Validator MUST:**

- Parse any ZTAP envelope presented to it.
- Validate that all required shared fields are present: `ztap_version`, `envelope_type`,
  `transaction_id`, `integrity`.
- Validate that `envelope_type` is one of the five defined ZTAP types.
- Reject envelopes with an unsupported or unrecognized `ztap_version` major version.
- Validate that actor `role` fields contain only defined ZTAP protocol role values.
- Reject envelopes where `role` contains tool names, model names, vendor names, or any value
  not in the ZTAP protocol role set.
- Validate that `integrity.canonicalization` and `integrity.hash_algorithm` are present.
- Validate that `integrity.hash_value` is present and non-empty.
- Verify the envelope hash: recompute the hash using the declared canonicalization and
  algorithm, and confirm it matches `integrity.hash_value`.
- Validate that all reason codes appearing in envelopes are either core ZTAP codes or
  namespaced extension codes. Reject un-namespaced unknown codes.
- Validate that all evidence types appearing in envelopes are either core ZTAP types or
  namespaced extension types. Reject un-namespaced unknown types.
- Report structural validation failures with a structured reason code from the ZTAP core set.

**An Envelope Validator MAY:**

- Accept or warn on `1.0-draft` envelopes at its discretion.
- Perform profile-specific validation of `requested_action.parameters` if it knows the profile.
- Validate the `requested_action.risk_level` field against expected values.

---

### Level 2 — Control Plane

A Level 2 Control Plane can manage the full transaction lifecycle: receive submissions,
evaluate policy, authorize or reject transactions, issue authorization records, receive
receipts, and maintain an auditable record.

**A Level 2 Control Plane MUST satisfy all Level 1 requirements, plus:**

**Transaction ingestion:**
- Accept `transaction_request` envelopes from registered source actors.
- Assign a stable `transaction_id` and acknowledge receipt.
- Reject submissions from unregistered actors with `ACTOR_UNREGISTERED`.

**Actor and capability management:**
- Maintain a registry of registered actors with their roles and capability claims.
- Validate that the `source_actor` is registered and active.
- Validate that the `target_actor` is registered and active.
- Validate that all `requested_capabilities` are registered against the `target_actor`.
- Reject capability mismatches with `CAPABILITY_MISSING`.
- Maintain registry consistency as described in SPEC.md Section 9 (Requirement 9).
- Refuse to issue authorization decisions while any registry is in an inconsistent state.
  Emit `REGISTRY_INCONSISTENT` if this occurs.

**Policy evaluation:**
- Evaluate the transaction against organizational policy.
- Produce an `authorization_decision` envelope with one of the defined `authorization_status`
  values: `auto_authorized`, `human_approval_required`, `evidence_required`, `rejected`,
  `expired`.
- Include `policy_refs` referencing the policies evaluated.
- Include `reason_codes` on all outcomes, including authorizations.

**Human approval handling:**
- When `human_approval_required` is issued, track the approval request and its scope.
- When approval is received, issue a new `authorization_decision` with `authorization_status:
  "human_approved"` and a fully populated `human_approval_ref` including `approval_scope`.
- Never reuse or transfer an approval. An approval is transaction-specific, action-bound,
  target-bound, and single-use by default.
- Enforce `approval_scope.expires_at`. An expired approval must not be honored.
- Detect and reject approval replay with `APPROVAL_REPLAYED`.

**Integrity:**
- Verify the `integrity.hash_value` of every submitted envelope.
- Reject envelopes with integrity failures with `INTEGRITY_FAILED`.
- Include a valid `integrity` object on every envelope it produces.
- Record the `request_hash` in every `authorization_decision` envelope.

**Audit trail:**
- Retain every submitted envelope, every decision, every receipt, and every evidence record.
- Store records in an append-only, hash-linked audit log.
- Make the audit trail queryable by `transaction_id`, actor, time range, and outcome.

**Receipt handling:**
- Accept `execution_receipt` envelopes from target actors or validators.
- Verify that `receipt.request_hash` matches the original `transaction_request` hash.
- Reject receipts with mismatched hashes with `INTEGRITY_FAILED`.
- Record the receipt in the audit trail.

**Registry consistency:**
- Detect and report inconsistency in actor, capability, policy, or transaction registries.
- Fail closed when consistency cannot be verified.

---

### Level 3 — Governed Executor / Runtime

A Level 3 Governed Executor is a target actor, runtime, or execution system that performs
work on behalf of governed transactions. It is the entity at the trust boundary where
governance is finally enforced by either accepting or refusing action.

**A Level 3 Governed Executor MUST satisfy all Level 1 requirements, plus:**

**Authorization verification before action:**
- Refuse to perform any governed action unless it holds a valid, verified ZTAP authorization
  record for that specific action. This is non-negotiable. An unverified message — regardless
  of how it arrived — is not sufficient basis for action.
- Verify the following before accepting a transaction:
  - The envelope carries a valid `authorization_decision` with `authorization_status` of
    `auto_authorized` or `human_approved`.
  - The `authorization_decision.request_hash` matches the `transaction_request`'s
    `integrity.hash_value`.
  - The `authorization_decision.expires_at` has not elapsed.
  - The `target_actor.actor_id` in the envelope matches its own registered identity.
  - The `requested_capabilities` are within its registered capability claims.
- Reject transactions that fail any of these checks with the appropriate reason code.
- Never execute based on an unverified message, an ambient instruction, or an informal
  approval that has not been recorded as a ZTAP authorization record.

**Receipt production:**
- Produce an `execution_receipt` for every terminal transaction state.
- Include `request_hash` matching the original transaction request.
- Include `authorization_decision_ref` referencing the decision that authorized execution.
- Include structured `verification_results` checked against the transaction's
  `verification_requirements`.
- Include `atomicity_result` accurately recording whether execution was atomic, partial, or
  non-atomic, and whether rollback was performed.
- Include `reason_codes` on all non-succeeded receipts.

**Atomicity enforcement:**
- Default to `atomic_required` behavior unless the transaction explicitly declares otherwise.
- Fail closed with `PARTIAL_STATE_BLOCKED` if partial execution occurs under `atomic_required`
  and rollback is not possible.
- Include `partial_state_description` in the `atomicity_result` when `PARTIAL_STATE_BLOCKED`
  occurs.

---

## Required Invariants

The following invariants are mandatory for all conforming implementations at all levels.
Violation of any invariant makes an implementation non-conforming.

| Invariant | Required Action on Violation |
|---|---|
| Unsupported major `ztap_version` | Reject with `SCHEMA_INVALID` |
| Missing required field | Reject with `SCHEMA_INVALID` |
| Invalid `role` value (any non-ZTAP value) | Reject with `ROLE_INVALID` |
| Tool name, model name, or vendor name as `role` | Reject with `ROLE_INVALID` |
| Unregistered actor | Reject with `ACTOR_UNREGISTERED` |
| Missing registered capability | Reject with `CAPABILITY_MISSING` |
| Policy explicitly denied | Reject with `POLICY_DENIED` |
| `integrity.hash_value` mismatch | Reject with `INTEGRITY_FAILED` |
| `expires_at` elapsed | Reject with `EXPIRED` |
| Authorization replay detected | Reject with `APPROVAL_REPLAYED` |
| Non-atomic partial execution under `atomic_required` | Fail with `PARTIAL_STATE_BLOCKED` |
| Registry inconsistency detected at control plane | Refuse authorization with `REGISTRY_INCONSISTENT` |
| Free-text-only `verification_requirements` | Reject with `SCHEMA_INVALID` |
| Un-namespaced unknown reason code | Reject with `SCHEMA_INVALID` |
| Un-namespaced unknown evidence type | Reject with `SCHEMA_INVALID` |
| Un-namespaced unknown capability identifier | Reject with `CAPABILITY_MISSING` or `SCHEMA_INVALID` |
| Unknown action profile (unless policy explicitly allows) | Reject with `SCHEMA_INVALID` |
| Un-namespaced unknown profile identifier | Reject with `SCHEMA_INVALID` |
| Source-declared `risk_level` accepted without evaluation | Non-conformant authorization |
| Envelope hash verified with wrong version's rules | Reject with `INTEGRITY_FAILED` |

These invariants are not configurable. They are not defaults. They are protocol rules.

---

## Role and Capability Conformance

Roles are governance classifications defined by the ZTAP protocol. A conforming implementation
must enforce the following:

- Only the defined ZTAP protocol roles are valid `role` values: `operator`, `control_plane`,
  `source_actor`, `target_actor`, `planner`, `executor`, `validator`, `auditor`, `runtime`.
- Tool names, model names, vendor product names, SaaS platform names, and runtime identifiers
  are not valid roles and must be rejected with `ROLE_INVALID`.
- `implementation_ref` is optional metadata. It has no governance authority. A conforming
  control plane must not use `implementation_ref` as the basis for authorization decisions.
- Capability claims are separate from role assignments. Holding a role does not automatically
  grant capabilities. Each capability must be explicitly registered against the actor.
- A transaction requesting a capability not registered for the target actor must be rejected
  with `CAPABILITY_MISSING`.

### Capability Namespacing Conformance

Capability identifiers follow an open governed registry model. A conforming implementation must:

- Accept ZTAP core capabilities by their reserved simple names (e.g., `file.read`, `git.push`,
  `test.run`). The full core capability set is defined in `SCHEMA.md`.
- Require extension capabilities to use a reverse-domain namespaced format
  (e.g., `org.example/deploy_service`). Extension capabilities without a namespace are
  schema-invalid.
- Reject un-namespaced unknown capability identifiers with `CAPABILITY_MISSING` or
  `SCHEMA_INVALID` as appropriate.
- Allow control planes to restrict which extension namespaces are accepted within their
  deployment.

### Profile Conformance

Action profiles follow the same open governed registry model. A conforming control plane must:

- Recognize ZTAP core profiles (`ztap.core/fileops`, `ztap.core/gitops`, `ztap.core/testops`,
  `ztap.core/approval`, `ztap.core/evidence`, `ztap.core/generic`).
- Accept extension profiles only if they are namespaced (`org.example/deploy`).
- Reject un-namespaced unknown profile values with `SCHEMA_INVALID` unless control-plane
  policy explicitly permits unrecognized profiles.
- Always include `parameters` in the envelope hash regardless of whether the profile is
  known to the control plane.

---

## Integrity Conformance

A conforming implementation must:

- Include a valid `integrity` object on every envelope it produces.
- Use RFC 8785 JSON Canonicalization Scheme (JCS) as the default canonicalization method.
- Use SHA-256 as the default hash algorithm.
- Compute the hash by:
  1. Constructing the full envelope with `integrity.hash_value` set to an empty string.
  2. Applying RFC 8785 JCS canonicalization.
  3. Computing SHA-256 over the canonical byte sequence.
  4. Encoding the result as a lowercase hex string.
  5. Setting `integrity.hash_value` to this value.
- Note: only `integrity.hash_value` is excluded from the hash input. All other `integrity`
  fields — `canonicalization`, `hash_algorithm`, `signed` — are included. This ensures the
  declared algorithm and canonicalization method are themselves tamper-evident.
- Verify the hash on every received envelope before processing. Reject hash mismatches with
  `INTEGRITY_FAILED`.
- Never process, forward, or store an envelope with a failed hash without recording the failure.

A conforming control plane must additionally:
- Maintain a hash-linked audit log. Each stored record must reference the prior record's hash.
- Make the hash chain available for auditor verification.

### Multi-Version Integrity Conformance

A conforming control plane that stores envelopes from multiple ZTAP versions must:

- Verify each stored envelope using the `canonicalization` and `hash_algorithm` declared
  in that envelope's own `integrity` object — not the control plane's current default.
- Retain `ztap_version`, `integrity.canonicalization`, and `integrity.hash_algorithm`
  alongside every stored envelope so each can be independently re-verified at any time.
- Not silently reinterpret older-version envelopes under newer schema rules. Version-specific
  validation applies to each record according to its declared version.
- Reject envelopes with unsupported major versions for active authorization. Historical
  records from prior supported versions remain auditable but are not re-authorized.

---

## Authorization Conformance

A conforming control plane must recognize and correctly handle all six `authorization_status`
values:

| Status | Meaning |
|---|---|
| `auto_authorized` | Policy permits the transaction without human review. |
| `human_approval_required` | Policy requires human approval before proceeding. Transaction blocked. |
| `human_approved` | Human approval was required, granted, and recorded. Distinct from `auto_authorized`. |
| `evidence_required` | Additional evidence must be submitted before a decision can be made. |
| `rejected` | Policy denies the transaction. Terminal. |
| `expired` | The transaction's validity window elapsed. Terminal. |

A conforming implementation must:
- Never collapse `human_approved` into `auto_authorized`. The distinction is required so
  human involvement is machine-detectable in the audit trail.
- Issue a new `authorization_decision` envelope (with a new `decision_id`) when a
  `human_approval_required` decision transitions to `human_approved`. The original envelope
  is immutable and must be retained.
- Bind every human approval to its `approval_scope`: `transaction_id`, `request_hash`,
  `action_ids`, `target_actor_id`, `approved_capabilities`, `expires_at`, and `single_use`.
- Enforce `approval_scope.expires_at` on every approval.
- Treat approvals as single-use by default. Reject replay with `APPROVAL_REPLAYED`.

---

## Receipt Conformance

Every terminal transaction state must produce an `execution_receipt`. A conforming
implementation must not allow a transaction to reach a terminal state without a receipt.

A conforming receipt must:
- Include `request_hash` matching the `integrity.hash_value` of the original
  `transaction_request` envelope.
- Include `authorization_decision_ref` referencing the `decision_id` of the authorizing
  decision.
- Include `status` with one of the defined values: `succeeded`, `failed`, `rejected`,
  `cancelled`, `expired`, `timed_out`.
- Include `reason_codes`. An empty array is valid only for `status: "succeeded"`.
- Include `actions_attempted` and `actions_completed`. Empty arrays are valid only when no
  execution was attempted.
- Include structured `verification_results` corresponding to each entry in the transaction's
  `verification_requirements`, identified by `check_id`.
- Include `atomicity_result` with `mode_declared`, `outcome`, and `rollback_performed`.
  Include `partial_state_description` when `outcome` is `partial`.
- Include `evidence_refs` when evidence records were submitted and are relevant to the receipt.
- Include a valid `integrity` object.

---

## Evidence Conformance

A conforming implementation must:
- Recognize and correctly process all ZTAP core evidence types defined in Section 10 of
  `SCHEMA.md`.
- Accept extension evidence types only if they are namespaced (`org.example/type-name`).
- Reject un-namespaced unknown evidence types with `SCHEMA_INVALID`.
- Verify `evidence_hash` against the referenced evidence content when evaluating evidence.
- Include `evidence_refs` in `authorization_decision` envelopes when evidence records were
  accepted and influenced the authorization outcome.

---

## Reason Code Conformance

ZTAP uses an open governed registry for reason codes. A conforming implementation must:

- Recognize and correctly handle all ZTAP core reason codes.
- Accept extension reason codes only if they are namespaced (`org.example/CODE_NAME`).
- Reject un-namespaced unknown reason codes with `SCHEMA_INVALID`.
- Not use free-text in place of reason codes for machine-governed decisions.
- Include reason codes on all `authorization_decision` and `execution_receipt` envelopes.

---

## Trust Boundary Conformance

**ZTAP does not secure the pipe. ZTAP governs the action.**

A conforming actor, runtime, tool, or control plane must refuse governed work unless a
valid, verified ZTAP transaction exists and is verified at the point of action.

Specifically, a conforming Level 3 Governed Executor must:
- Refuse any instruction to perform governed work that does not arrive with a valid,
  unexpired ZTAP authorization record.
- Not treat transport-level authentication (API keys, TLS, session tokens) as a substitute
  for a ZTAP authorization record.
- Not infer authorization from conversational context, AI model confidence, or ambient
  trust in the source system.
- Not execute based on an unsigned, unverified, or informal instruction, even from a system
  it considers "trusted."

The corollary: an ungoverned message can exist in the world. It cannot be promoted to
governed, authorized work inside a ZTAP-compliant environment without passing through the
control plane's evaluation and receiving a valid authorization record.

---

## Non-Conforming Behaviors

The following behaviors make an implementation non-conforming. They are listed explicitly
because they are common failure modes in multi-agent governance systems.

**Envelope and schema violations:**
- Accepting an envelope with a missing required field rather than rejecting with `SCHEMA_INVALID`.
- Attempting to infer or repair a malformed field rather than rejecting it.
- Accepting an unrecognized `envelope_type` rather than rejecting with `SCHEMA_INVALID`.

**Role violations:**
- Using a tool name (e.g., `codex`, `cursor`), model name (e.g., `claude`, `gpt-4`), vendor
  name, or platform name as an actor `role` value.
- Accepting such values from submitted envelopes rather than rejecting with `ROLE_INVALID`.
- Using `implementation_ref` as the basis for authorization decisions.

**Integrity violations:**
- Skipping hash verification on received envelopes.
- Accepting an envelope with a hash mismatch rather than rejecting with `INTEGRITY_FAILED`.
- Mutating a submitted `transaction_request` envelope after it has been assigned a
  `transaction_id`. Submitted envelopes are immutable.

**Authorization violations:**
- Treating `human_approved` and `auto_authorized` as equivalent statuses.
- Reusing a prior authorization record for a different transaction.
- Honoring an approval after its `approval_scope.expires_at` has elapsed.
- Using a `single_use: true` approval for a second transaction.
- Failing to record `approval_scope` on human-approved transactions.

**Execution boundary violations:**
- A target actor executing based on an unverified message, ambient instruction, or informal
  approval that does not carry a valid ZTAP authorization record.
- A control plane issuing authorization while its registries are in an inconsistent state.
- A runtime or adapter escalating its own execution authority without a governance artifact.

**Audit trail violations:**
- Allowing a transaction to reach a terminal state without producing a receipt.
- Producing a receipt that does not reference `request_hash`.
- Omitting `reason_codes` from a non-succeeded receipt.
- Storing audit records in a non-append-only, non-hash-linked log.

---

## Minimal Test Matrix

The following table defines a minimum set of positive and negative conformance tests. Each
test should be implementable as a deterministic, automated check. A conforming implementation
must pass all applicable tests for its declared conformance level.

| # | Test | Type | Level | Expected Result |
|---|---|---|---|---|
| T01 | Submit a structurally valid envelope | Positive | L1 | Accepted, hash verified |
| T02 | Submit envelope with missing `ztap_version` | Negative | L1 | Rejected: `SCHEMA_INVALID` |
| T03 | Submit envelope with missing `integrity.hash_value` | Negative | L1 | Rejected: `SCHEMA_INVALID` |
| T04 | Submit envelope with corrupted `integrity.hash_value` | Negative | L1 | Rejected: `INTEGRITY_FAILED` |
| T05 | Submit envelope with `role: "codex"` | Negative | L1 | Rejected: `ROLE_INVALID` |
| T06 | Submit envelope with `role: "claude"` | Negative | L1 | Rejected: `ROLE_INVALID` |
| T07 | Submit envelope with `role: "executor"` | Positive | L1 | Role accepted |
| T08 | Submit envelope with unsupported major version | Negative | L1 | Rejected: `SCHEMA_INVALID` |
| T09 | Submit envelope with un-namespaced unknown reason code | Negative | L1 | Rejected: `SCHEMA_INVALID` |
| T10 | Submit envelope with un-namespaced unknown evidence type | Negative | L1 | Rejected: `SCHEMA_INVALID` |
| T11 | Submit envelope with namespaced extension reason code | Positive | L1 | Accepted |
| T12 | Submit transaction from registered actor | Positive | L2 | `submitted` state, decision issued |
| T13 | Submit transaction from unregistered actor | Negative | L2 | Rejected: `ACTOR_UNREGISTERED` |
| T14 | Request capability not registered to target actor | Negative | L2 | Rejected: `CAPABILITY_MISSING` |
| T15 | Submit transaction matching `auto_authorized` policy | Positive | L2 | `authorization_status: "auto_authorized"` |
| T16 | Submit transaction matching `rejected` policy | Negative | L2 | `authorization_status: "rejected"`, `POLICY_DENIED` |
| T17 | Submit transaction requiring evidence | Positive | L2 | `authorization_status: "evidence_required"` |
| T18 | Submit transaction requiring human approval | Positive | L2 | `authorization_status: "human_approval_required"` |
| T19 | Issue human approval and verify `human_approved` status | Positive | L2 | New decision with `authorization_status: "human_approved"` |
| T20 | Replay a consumed single-use approval | Negative | L2 | Rejected: `APPROVAL_REPLAYED` |
| T21 | Submit receipt with mismatched `request_hash` | Negative | L2 | Rejected: `INTEGRITY_FAILED` |
| T22 | Submit receipt linked to correct `request_hash` | Positive | L2 | Receipt accepted and recorded |
| T23 | Transaction expires before acceptance | Positive | L2 | Receipt with `status: "expired"` |
| T24 | Executor verifies hash before accepting transaction | Positive | L3 | Transaction accepted |
| T25 | Executor receives transaction with hash mismatch | Negative | L3 | Rejected: `INTEGRITY_FAILED` |
| T26 | Executor receives transaction with elapsed `expires_at` | Negative | L3 | Rejected: `EXPIRED` |
| T27 | Executor receives instruction without authorization record | Negative | L3 | Refused — no action taken |
| T28 | Partial execution under `atomic_required` without rollback | Negative | L3 | `PARTIAL_STATE_BLOCKED` in receipt |
| T29 | Successful execution produces receipt with `request_hash` | Positive | L3 | Receipt references original hash |
| T30 | Control plane refuses authorization when registry inconsistent | Negative | L2 | `REGISTRY_INCONSISTENT` |
| T31 | Extension capability with valid namespace accepted | Positive | L1 | Accepted |
| T32 | Un-namespaced unknown capability rejected | Negative | L1 | Rejected: `SCHEMA_INVALID` |
| T33 | Extension profile with valid namespace accepted | Positive | L2 | Evaluated per policy |
| T34 | Unknown un-namespaced profile rejected | Negative | L2 | Rejected: `SCHEMA_INVALID` |
| T35 | Control plane elevates declared risk level, records `evaluated_risk_level` | Positive | L2 | Decision includes `RISK_LEVEL_ESCALATED` and `evaluated_risk_level` |
| T36 | Hash verification uses envelope's declared algorithm, not current default | Positive | L2 | Historical record verified with its own declared method |

---

## Open Questions

The following conformance questions are unresolved and require operator input before a
finalized conformance specification can be published:

1. **Conformance claim format.** How does an implementation declare its conformance level?
   Is there a machine-readable conformance manifest, a self-attestation document, or a test
   report format? This is needed before third-party conformance testing is possible.

2. **Level boundary between L1 and L2.** Can a tool be conformant at L1 without any control
   plane behavior? The current definition suggests yes — a standalone envelope validator with
   no policy engine is a valid L1 implementation. This should be confirmed.

3. ~~**`requested_action.profile` registry conformance.**~~ Resolved. Unknown un-namespaced
   profiles fail closed with `SCHEMA_INVALID` unless policy explicitly allows. Extension
   profiles must be namespaced. See Profile Conformance section and test T33–T34.

5. ~~**Multi-version audit trail conformance.**~~ Resolved. Each envelope is verified against
   its own declared `ztap_version` rules. See Multi-Version Integrity Conformance section
   and test T36.

**Still open:**

1. **Conformance claim format.** How does an implementation declare its conformance level?
   Machine-readable manifest, self-attestation, or test report format?

2. **Partial Level 2 conformance.** Is there a use case for an "audit-only control plane"
   that stores and verifies but does not manage registrations or issue authorizations?

4. **Break-glass conformance.** Minimum evidence fields for break-glass authorization at a
   Level 2 control plane are described in SPEC.md but not yet formalized as schema-level
   required fields. Pending further specification.

6. **Profile versioning.** When a profile's parameter schema changes, what is the profile
   version expression format? (`ztap.core/gitops@2`? `ztap.core/gitops/v2`?)

---

## Next Steps

**Delivered since this conformance draft was written:** the resolved decisions are applied
in `examples/` (including `authorization_status: "human_approved"` in example 02 and the
`requested_action` / `verification_requirements` structures throughout); the
machine-readable JSON Schemas ship under `schemas/` (implementation targets, not
specification authorities); `WHITEPAPER.md` and the repo governance files
(`CONTRIBUTING.md`, `LICENSE`, `CHANGELOG.md`) exist; and the repository is public.

**Remaining:**

1. **Conformance test fixtures** — a set of valid and intentionally invalid ZTAP envelopes
   for use in automated conformance testing. These support the test matrix above.

2. **Resolve the open questions above** — including the profile/version expression format —
   and freeze the conformance targets for a `1.0` release.

---

> ZTAP Conformance Draft — `1.0-draft`.
> Derived from `SPEC.md` and `SCHEMA.md`.
> **Freedom for engineers. Governance for the organization.**
