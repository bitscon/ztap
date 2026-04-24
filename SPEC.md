# ZTAP Specification Draft

*Zero Trust Agent Protocol — Transaction Lifecycle and Governance Model*

---

## Status

**DRAFT — Pre-Schema. Not for implementation.**

This document is an early specification draft. It defines the transaction lifecycle, governance
model, and core concepts of the Zero Trust Agent Protocol in prose.

Field names, schema structures, hash canonicalization rules, transport bindings, and API
interfaces are NOT finalized here. This document establishes the governing principles and
lifecycle model that all subsequent schema and implementation work must conform to.

This specification will be versioned. The current working version is `0.1-draft`.

Do not build production systems against this draft.

---

## Purpose

ZTAP defines how governed transactions between agents — and between agents, humans, and systems
— must be structured so that every interaction is authorized, verifiable, and auditable.

The core problem ZTAP addresses: in modern multi-agent AI systems, one agent invokes another
with a plain function call or message. No policy is evaluated. No authorization is recorded.
No verifiable receipt is produced. The interaction happens, and nothing proves what was
requested, what was permitted, or what occurred.

This is ambient authority. It is incompatible with organizational governance.

ZTAP solves this by defining a structured transaction model in which:

- every request is captured in a formal envelope before any action is taken,
- every envelope is submitted to a control plane for policy evaluation,
- every authorization decision is recorded as part of the transaction,
- every result is returned as a linked receipt that can be verified against the original request,
- and the complete record is tamper-detectable via cryptographic hashes.

ZTAP is transport-agnostic. A ZTAP envelope may move by API, file, message queue, GitHub PR,
chat message, workflow engine, email, or any other channel. ZTAP governs the transaction
object, not the delivery mechanism.

**Freedom for engineers. Governance for the organization.**

---

## Non-Goals

ZTAP does not define:

- **Transport protocols.** How envelopes move between actors is out of scope. ZTAP defines
  what must be in the envelope, not how it is delivered.
- **Model selection.** ZTAP does not govern which AI models agents use or how they generate
  outputs.
- **Tool implementation.** ZTAP does not define how agent tools work internally. It governs
  transactions between actors, not the internals of any actor.
- **User interfaces.** How operators interact with the control plane, review approvals, or
  browse audit logs is implementation-specific.
- **Vendor-specific APIs.** ZTAP defines a conceptual control plane contract. Specific API
  endpoints, SDKs, and service configurations are outside the protocol scope.
- **Encryption.** ZTAP v1 requires hash-based integrity, not encryption. Encryption may be
  layered on top for specific deployment contexts but is not a protocol requirement.
- **Cross-organizational federation.** Initial scope is single-organization deployment. See
  Section 17 (Next Steps) for future direction.

---

## The Trust Boundary

**ZTAP does not secure the pipe. ZTAP governs the action.**

ZTAP governance is not enforced by transport. An envelope that travels over a secure channel,
an authenticated API, an encrypted tunnel, or a trusted network is not a governed transaction
by virtue of its delivery method. Transport security and transaction governance are orthogonal.

ZTAP governance is enforced at the point of action. A target actor must refuse to perform
work unless it holds a valid, verifiable ZTAP authorization record for that specific action.
The authorization record — issued by the control plane — is what makes a transaction governed.
The transport is irrelevant.

This means:

- An ungoverned message may exist. It cannot become accepted, authorized, governed work inside
  a ZTAP-compliant environment unless it passes through the control plane's evaluation and
  produces a valid authorization record.
- A compliant target actor does not execute instructions delivered without a valid ZTAP
  authorization record, regardless of how those instructions arrived or who sent them.
- A compliant control plane does not issue authorizations without evaluating policy, regardless
  of how well-trusted the source actor appears to be.
- A compliant runtime does not escalate its own authority. The governance layer and the
  execution layer are permanently separate. The entity that governs does not execute. The
  entity that executes does not self-authorize.

The trust boundary is not defined by the network perimeter. It is defined by the authorization
record. This is the foundational principle from which ZTAP's entire governance model derives.

---

## Core Concepts

### ZTAP Transaction

The full governed unit of work. A transaction begins when a source actor creates a request and
ends when a final receipt is produced — whether the outcome is success, failure, rejection, or
cancellation.

A transaction is not a single message. It is a lifecycle. Multiple envelopes and receipts may
be associated with a single transaction as it moves through its states.

### ZTAP Envelope

The serialized JSON object that carries a transaction event. An envelope captures a point-in-time
state of a transaction: the original request, an authorization decision, an evidence submission,
an amendment event, or a final result.

Submitted envelopes are immutable. Once a transaction envelope has been submitted to the control
plane, it cannot be modified. Subsequent events — results, evidence, approvals — are separate
linked envelopes, not modifications to the original.

### ZTAP Receipt

The result envelope produced after a transaction reaches a terminal or intermediate state.
A receipt references the original transaction and the original request envelope by hash, links
the outcome to the request, and provides the information needed to verify that the result
corresponds to the authorized action.

Receipts are produced for all terminal outcomes: success, failure, rejection, cancellation,
and expiry.

### ZTAP Control Plane

The authority layer responsible for evaluating policy, recording authorization decisions, and
governing whether transactions may proceed. The control plane is the single authoritative
source for whether a given transaction is permitted under organizational policy.

The control plane is not defined by ZTAP as a specific product. ZTAP defines the conceptual
contract the control plane must satisfy. ZTI Core is one compliant implementation of this
contract.

### Actor

Any entity that participates in a ZTAP transaction — source, target, approver, or auditor.
Actors may be AI agents, automated systems, or humans. All actors must be identifiable to the
control plane.

### Role

A protocol-level classification of the function an actor performs within a transaction.
Roles are defined by ZTAP and are not implementation-specific. An actor may hold more than
one role depending on context.

Defined roles are listed in Section 14.

### Capability

A declared ability that an actor can perform and that a transaction may request. Capabilities
are not roles. A role describes what function an actor serves in the governance model; a
capability describes what that actor can do.

Example: an actor with the role `executor` may hold capabilities such as `deploy_service`,
`run_query`, or `send_message`. These are distinct claims. A transaction requesting
`deploy_service` from an actor that does not hold that capability must be rejected.

### Evidence

Supporting material that accompanies a transaction to satisfy policy requirements. Evidence
may include test results, approval records, prior transaction receipts, compliance attestations,
or any other structured data the control plane requires before authorizing a transaction.

Evidence envelopes are linked to the transaction by hash.

---

## Transaction Lifecycle

A ZTAP transaction progresses through a defined set of states. Not all states are reached in
every transaction — a rejected transaction does not enter `executing`, and a cancelled
transaction may be cancelled from multiple earlier states.

### States

**`created`**
The transaction envelope has been constructed by the source actor. It has not yet been
submitted to the control plane. At this point the envelope exists only in the source actor's
context.

**`submitted`**
The envelope has been delivered to the control plane. The control plane has acknowledged
receipt. The transaction is now in the governance layer.

**`evaluated`**
The control plane has completed its evaluation of the transaction. Evaluation includes:
schema validity, actor identity and registration, role validity, capability claims, policy
compliance, and integrity requirements. The control plane has not yet issued a final
authorization decision.

**`authorized`**
The control plane has determined that the transaction is permitted to proceed. An authorization
record has been appended to the transaction. The target actor has not yet been notified or
agreed to act.

*Authorization means governance permitted it. It does not mean the target actor has agreed.*

**`rejected`**
The control plane determined that the transaction does not meet policy requirements. A rejection
receipt is produced with a structured reason code. Rejection occurs before any execution
attempt. No action is taken on the target system.

**`accepted`**
The target actor has received the authorized transaction envelope and agreed to perform the
requested work. This is a distinct state from `authorized`.

*Acceptance means the target actor agreed to act. It does not mean execution has begun.*

**`executing`**
The target actor is actively performing the requested work.

**`verifying`**
The result of execution is being checked against verification requirements defined in the
transaction or by policy. Verification may be performed by the target actor, a separate
validator actor, or the control plane.

**`succeeded`**
The transaction completed, and verification passed. A success receipt is produced and linked
to the original transaction.

**`failed`**
The transaction failed. Failure may occur during evaluation, authorization, execution,
or verification. A failure receipt is produced with a structured reason code. See Section 12
for defined reason categories.

**`cancelled`**
An operator or the control plane cancelled the transaction before it reached a terminal state.
Cancellation may occur from `created`, `submitted`, `evaluated`, `authorized`, or `accepted`.
A cancellation receipt is produced.

**`expired`**
The transaction's validity window elapsed before it reached `accepted` or a terminal state.
An expiry receipt is produced. Expiry is a form of failure and follows fail-closed behavior.

### State Transitions

```
created
  └─► submitted
        └─► evaluated
              ├─► authorized
              │     ├─► accepted
              │     │     └─► executing
              │     │           └─► verifying
              │     │                 ├─► succeeded
              │     │                 └─► failed
              │     └─► expired (before acceptance)
              ├─► rejected
              └─► failed (evaluation failure)

[from created, submitted, evaluated, authorized, accepted]
  └─► cancelled

[from submitted, evaluated, authorized, accepted]
  └─► expired
```

### Transition Rules

- A transaction may not advance to `authorized` without passing `evaluated`.
- A transaction may not advance to `executing` without reaching `accepted`.
- A transaction may not advance to `verifying` without completing `executing`.
- `rejected` and `failed` are terminal states. A new transaction must be created to retry.
- `cancelled` is terminal. The original transaction cannot be resumed.
- `expired` is terminal. Expiry is equivalent to failure for audit purposes.
- All terminal states must produce a receipt.

---

## Authorization Model

Authorization is determined by the control plane based on organizational policy. ZTAP does not
define authorization outcomes based on transaction type, actor identity, or any other attribute
directly. Policy governs.

### Authorization Outcomes

**`auto_authorized`**
The control plane determined that the transaction is within policy and authorized it to proceed
without human review. No human approval was required or requested.

**`human_approval_required`**
Policy requires a named individual or role to approve the transaction before it may proceed.
The transaction enters a waiting state. The control plane records the approval request, the
approver identity, and the approval timestamp when the approval is received. The transaction
does not advance until approval is granted.

**`evidence_required`**
Policy requires additional evidence before a decision can be made. The control plane specifies
what evidence is needed. The source actor or a delegated actor must submit a linked evidence
envelope. The transaction does not advance until sufficient evidence is received and evaluated.

**`rejected`**
Policy denies the transaction. The transaction moves to the `rejected` terminal state. A
structured reason code is recorded.

**`expired`**
The transaction's validity window elapsed before a decision was reached. The transaction moves
to the `expired` terminal state.

### Human-in-the-Loop

ZTAP supports human-in-the-loop approval as a policy-conditional outcome. Human approval is
not required for every transaction. Whether a transaction requires human approval, may be
auto-authorized, or must be rejected is determined entirely by organizational policy.

When human approval is required, ZTAP requires that:
- the approval request be recorded in the transaction,
- the approver identity be recorded,
- the approval timestamp be recorded, and
- the approval record be hash-linked to the transaction envelope.

An approval that is not recorded in the transaction is not a ZTAP-compliant approval.

Approvals are action-specific and single-use. An approval issued for one transaction may not
be applied to a different transaction. An authorization record that was consumed to advance a
prior transaction must not be replayed. An expired authorization record is invalid regardless
of whether the original approval was genuine. See `APPROVAL_REPLAYED` in the reason code
registry.

When an approval is received and recorded, the control plane issues a new authorization
decision envelope with `authorization_status: "human_approved"` — a distinct status that
makes human involvement machine-detectable. It does not reuse the `auto_authorized` status.
See `SCHEMA.md` for the full field definition.

### Break-Glass Access

Emergency or exceptional access pathways — commonly called "break-glass" — are governed
pathways with elevated evidence requirements, not authorization bypasses.

**Break-glass has more required evidence than standard authorization, not less.**

A ZTAP-compliant break-glass transaction must carry — at minimum — structured evidence
establishing:

- **Incident or ticket reference** — a stable identifier for the incident or event requiring
  emergency access.
- **Named approver** — the identity of the operator authorizing the break-glass action.
- **Reason code** — the specific reason emergency access is required.
- **Expiration** — a strict, short expiration timestamp after which the break-glass
  authorization is invalid. There is no indefinite emergency authorization.
- **Compensating controls** — what governance safeguards are in place during the period of
  emergency access.
- **Post-incident review reference** — a commitment to review and audit the break-glass
  action after the incident is resolved.

An expired or incomplete break-glass authorization is invalid and must fail closed. A
break-glass action that bypasses authorization is not a legitimate break-glass — it is an
unauthorized action, and must be treated as such in the audit trail.

ZTAP v1 does not define a dedicated break-glass envelope type. Break-glass transactions use
the existing authorization and evidence model, with policy requirements specifying the
evidence fields described above. This principle is normative; the schema implementation is
in progress.

---

## Identity and Actor Registration

All actors that participate in ZTAP transactions must be identifiable to the control plane.
ZTAP defines the identity *claims* that actors must be able to make; it does not mandate the
authentication mechanism used to verify those claims.

Compliant identity mechanisms may include, but are not limited to:
- API key with control plane registration
- Signed JWT (JSON Web Token)
- Mutual TLS (mTLS)
- Local registry identity
- Enterprise SSO delegation
- Platform-native identity (e.g., GitHub identity, cloud IAM role)

ZTAP requires that an actor's identity record include, at minimum, the conceptual equivalents of:

- **Actor identifier** — a stable, unique reference for this actor within the organization's
  control plane. Not necessarily a human-readable name.
- **Role or roles** — the protocol roles this actor is registered to perform.
- **Capability claims** — the specific capabilities this actor is authorized to exercise.
- **Organization or tenant context** — which organization this actor belongs to.
- **Registration status** — whether this actor is currently active and authorized to participate
  in transactions.

Exact field names are to be determined during schema specification.

### Tools Are Not Roles

A tool is a capability an actor can exercise. A role describes the actor's function within
the governance model.

An executor that can run a deployment tool holds the `executor` role and the `deploy_service`
capability. These are distinct claims and must be registered separately. Policy may authorize
a role without authorizing every capability that role may hold, and vice versa.

An actor's `implementation_ref` — the underlying tool, model, or system it is built on —
is metadata for audit readability and debugging. It is not a role. It carries no governance
authority. The control plane evaluates the registered role and capability claims, not the
implementation identity. See the normative rule in Section 14 (Roles and Capabilities).

### Unregistered Actors

A transaction submitted by an unregistered actor, or requesting action from an unregistered
target, must be rejected with reason code `ACTOR_UNREGISTERED`. ZTAP is fail-closed. An
unknown actor is not a trusted actor.

---

## Control Plane Contract

The ZTAP control plane must support the following logical operations. This section defines the
conceptual contract, not HTTP endpoints or API signatures. Those are implementation details.

### 1. Submit Transaction

Accept a transaction envelope from a source actor. Acknowledge receipt and assign the
transaction to the `submitted` state. Return a stable transaction reference.

Pre-conditions: the submitting actor must be identifiable. The envelope must be structurally
well-formed enough to process. Full schema and policy evaluation happens during evaluate.

### 2. Evaluate Transaction

Evaluate the submitted transaction against:
- schema validity
- actor identity and registration
- role authorization
- capability claims
- organizational policy
- evidence requirements
- integrity hash validity

Produce an evaluation record. Advance the transaction to `evaluated` or `failed`.

### 3. Authorize, Reject, or Request Evidence

Based on evaluation, the control plane must produce one of the defined authorization outcomes:
`auto_authorized`, `human_approval_required`, `evidence_required`, or `rejected`.

The decision must be recorded as a linked record on the transaction. The decision record must
include the outcome, the policy basis for the outcome, and a timestamp.

### 4. Record Decision

Every authorization decision — including rejections and evidence requests — must be durably
recorded in the control plane's audit log. Decisions are append-only. A decision record cannot
be modified after it is written.

### 5. Deliver Authorized Transaction

Once authorized, the control plane must deliver or make available the authorized transaction
envelope to the target actor. The delivery mechanism is transport-specific and out of scope.
The envelope delivered must include the authorization record appended by the control plane.

### 6. Receive Receipt

Accept a receipt envelope from the target actor or validator. The receipt must reference the
original transaction by its stable identifier and by the hash of the original request envelope.

### 7. Verify Receipt

Confirm that the receipt corresponds to the authorized transaction:
- the transaction identifier matches,
- the request hash in the receipt matches the original envelope hash,
- the receipt is structurally valid.

Verification may be performed by the control plane, a validator actor, or both, as defined by
policy.

### 8. Retain Audit Trail

Every transaction, every envelope, every decision record, every receipt, and every evidence
envelope must be retained in the audit log. The audit trail is append-only. Entries must be
hash-linked to support tamper detection.

The audit trail is the authoritative record of what happened. It must be queryable by
transaction identifier, actor, time range, and outcome.

The hash chain makes tampering detectable: each stored record's hash references the prior
record. A gap or mismatch in the chain is evidence of inconsistency. A compliant control
plane must provide a mechanism for auditors to walk the hash chain and verify completeness.

### 9. Verify Registry Consistency

A compliant control plane must be able to verify the internal consistency of its own
registries before issuing authorization decisions. The registries in scope include:

- **Actor registry** — registered actors, their roles, and their capability claims.
- **Capability registry** — defined capabilities and their policy associations.
- **Policy registry** — active authorization policies and their scope.
- **Transaction registry** — the audit log of submitted transactions and their states.

A control plane that cannot verify its own registry consistency must not issue authorization
decisions. Registry inconsistency is a fail-closed condition. The reason code for this
failure mode is `REGISTRY_INCONSISTENT`.

**The governing principle:** an authorization decision issued against an inconsistent registry
cannot be verified. If the actor registry and the policy registry disagree about what an
actor is permitted to do, the resulting authorization decision is indeterminate. An
indeterminate authorization is not a governed authorization.

**The practical implication:** a control plane must detect registry inconsistency before it
matters — at startup, after configuration changes, and at any point where inconsistency would
affect the validity of an authorization decision about to be issued.

---

## Integrity and Hashing

ZTAP v1 requires hash-based integrity verification. Encryption is not required by the initial
protocol specification and may be added as an optional layer in future versions or specific
deployment contexts.

### Principles

**The original envelope must be hashable.** A submitted transaction envelope must produce a
stable, deterministic hash. This hash serves as the canonical reference for the original
request throughout the transaction lifecycle.

**Receipts must reference the original request hash.** Any receipt produced in relation to a
transaction must include the hash of the original request envelope. This binds the result to
the request and makes it verifiable.

**Evidence must be hash-linked.** Evidence envelopes must include the hash of the transaction
they support. The transaction record must include the hashes of any evidence envelopes
submitted.

**Tampering must be detectable.** Any modification to a submitted envelope — any field, any
value — must produce a different hash, invalidating the hash reference chain.

### What Hash Verification Answers

- Is this the original envelope, or has it been altered?
- Does this receipt correspond to the request I submitted?
- Does the evidence correspond to the transaction it claims to support?
- Has the audit log been tampered with?

### Algorithm

SHA-256 is assumed as the default hash algorithm for ZTAP v1. The exact canonicalization
rules — how a JSON envelope is serialized before hashing, how whitespace and key ordering
are handled — are a specification detail that must be finalized before the v1 schema is frozen.

Canonicalization must be deterministic: the same logical envelope must always produce the
same hash, regardless of how it was serialized or by whom.

---

## Immutability and Amendments

### The Immutability Rule

**Submitted transaction envelopes are immutable.**

Once a transaction envelope has been submitted to the control plane and assigned a transaction
identifier, the original envelope must not be modified. Its content is the canonical record of
what was requested.

This is not a technical limitation — it is a governance requirement. The integrity of the
audit trail depends on the original request being unalterable.

### Handling Changes

If the original request must change after submission, the correct actions are:

1. **Cancel the original transaction** and create a new one, or
2. **Create a linked amendment event** — a separate envelope that references the original
   transaction and records what changed, why, and under what authority.

Amendment events are themselves ZTAP envelopes. They are subject to the same governance model
as original transactions. An amendment that was not authorized by the control plane is not a
valid amendment.

### Linked Records

All subsequent events in a transaction's lifecycle — authorization decisions, evidence
submissions, approvals, amendment events, and receipts — are separate envelopes that reference
the original by transaction identifier and request hash. They do not modify the original.

The full transaction history is the ordered set of all linked envelopes, not a single mutable
record.

---

## Failure Model and Reason Codes

### Fail-Closed Is a Protocol Invariant

**Fail-closed is not a default setting. It is a protocol invariant.**

When a transaction cannot be completed — for any reason — the outcome is rejection or failure,
not continuation. There is no permissive fallback mode. Ambiguity resolves to denial, not
to permission.

A compliant actor, control plane, or implementation must reject a transaction under any of
the following conditions, without exception:

- **Invalid schema.** The envelope does not conform to the required ZTAP structure.
- **Unknown actor.** The submitting or target actor is not registered with the control plane.
- **Invalid role.** The actor's claimed role is not a recognized ZTAP protocol role.
- **Missing authority.** Required authority or delegation is absent from the envelope.
- **Missing capability.** The target actor does not hold the requested capability in its
  registered capability claims.
- **Integrity mismatch.** A hash check fails on any envelope in the transaction chain.
- **Expired transaction.** The transaction's validity window has elapsed.
- **Inconsistent registry.** The control plane cannot verify the internal consistency of its
  actor, capability, policy, or transaction registry.
- **Unsupported version.** The envelope carries a `ztap_version` the implementation does not
  support and has not been explicitly configured to accept.

In no circumstance may an implementation proceed when one of these conditions is true. There
is no "trusted internal path," no "known good actor" shortcut, and no administrative mode
that bypasses the fail-closed rule. Break-glass access is governed access with elevated
evidence requirements — it is not an authorization bypass. See the Break-Glass section in the
Authorization Model for the governing principle.

### Failure Receipts

Every failure must produce a structured receipt containing:
- the transaction identifier,
- the state at which failure occurred,
- a reason code from the defined set,
- a timestamp, and
- a hash of the original request envelope (where available).

Failure without a receipt is not ZTAP-compliant.

### Draft Reason Code Categories

The following are initial reason code categories. Final codes, descriptions, and subcategories
will be specified before schema freeze.

| Reason Code | Category | Description |
|---|---|---|
| `SCHEMA_INVALID` | Structural | The envelope does not conform to the required schema. |
| `ROLE_INVALID` | Identity | The requesting actor does not hold a valid ZTAP role. |
| `ACTOR_UNREGISTERED` | Identity | The actor is not registered with the control plane. |
| `AUTHORITY_MISSING` | Authorization | Required authority or delegation is absent. |
| `POLICY_DENIED` | Policy | The control plane policy explicitly denies this transaction. |
| `CAPABILITY_MISSING` | Capability | The target actor does not hold the requested capability. |
| `TARGET_REJECTED` | Acceptance | The target actor declined to accept the authorized transaction. |
| `ACTION_FAILED` | Execution | The target actor attempted the action and it failed. |
| `VERIFY_FAILED` | Verification | The result did not pass verification requirements. |
| `TIMEOUT` | Temporal | A required step was not completed within the allowed time window. |
| `EXPIRED` | Temporal | The transaction's validity window elapsed. |
| `CANCELLED` | Control | The transaction was explicitly cancelled by an authorized actor. |
| `INTEGRITY_FAILED` | Integrity | A hash check failed; the envelope or receipt may have been tampered with. |
| `EVIDENCE_MISSING` | Policy | Required evidence was not submitted within the required window. |
| `PARTIAL_STATE_BLOCKED` | Atomicity | The transaction reached a partial execution state and atomicity requirements prevented continuation. |

---

## Atomicity Model

### The Problem

Not all real-world operations are reversible. A deployment may succeed on three of four
services before failing on the fourth. A message may be sent before a downstream step fails.
ZTAP must handle partial execution states without assuming that rollback is always possible.

### Declared Atomicity Modes

Every ZTAP transaction must declare — or be evaluated against a policy that specifies — one
of the following atomicity modes:

**`atomic_required`** *(default)*
The transaction must either complete fully or not at all. If partial execution occurs and
rollback is not possible, the transaction must be failed with reason code
`PARTIAL_STATE_BLOCKED`. The failure receipt must record what partial state was reached.

**`best_effort_allowed`**
Partial completion is permitted if the source actor explicitly declares this mode and the
control plane policy permits it. The receipt must accurately record which steps succeeded and
which failed.

**`non_atomic_explicitly_allowed`**
Non-atomic execution is permitted. This mode must be explicitly authorized in the transaction
envelope and confirmed by the control plane. The receipt must record the actual execution
outcome in full, including any partial state.

### Default Behavior

The default atomicity mode is `atomic_required`. A transaction that does not declare an
atomicity mode is treated as `atomic_required`.

If an executor cannot guarantee atomicity and the transaction mode is `atomic_required`, the
transaction must fail closed with `PARTIAL_STATE_BLOCKED`. The executor must not proceed.

Non-atomic execution must be:
- explicitly declared in the transaction envelope,
- authorized by the control plane,
- and fully reflected in the receipt.

It is never the default. It is never inferred.

---

## Governance-Class Transactions

### Operational vs. Governance Transactions

Not all transactions carry the same governance risk. ZTAP distinguishes between two classes:

**Operational transactions** request ordinary work against systems, services, data, or
infrastructure. Deploying a service, running a query, sending a notification, archiving a
record. These are the standard transaction type described throughout this specification.

**Governance transactions** request modifications to the governance layer itself. Registering
a new actor, revoking a capability grant, modifying an authorization policy, changing approval
requirements, updating control plane configuration, or altering the audit trail structure.

### Why the Distinction Matters

A governance transaction can change the rules under which future operational transactions
are evaluated. A transaction that modifies who is permitted to do what must be held to a
stricter standard than the operational work it enables.

If an executor can register itself with new capabilities via an auto-authorized transaction,
the governance model has a fundamental gap. The authorization rules for governance-class
transactions must be stricter — not equal to or more permissive than — the authorization
rules for operational transactions.

### ZTAP v1 Guidance

ZTAP v1 does not define a separate envelope type for governance transactions. Governance
transactions use the same envelope structure as operational transactions. They are
distinguished by:

- the capabilities they request (capabilities that modify registry or policy state),
- the elevated evidence requirements the control plane applies to them, and
- the authorization approval level organizational policy assigns to them.

A compliant control plane should define policy that ensures governance-class transactions:

- require explicit operator approval, regardless of other auto-authorization rules,
- carry structured evidence of the change being requested and its policy justification,
- produce receipts that record the specific change made, the prior state, and the new state,
- and are clearly labeled as governance-class actions in the audit trail.

This is policy guidance for v1, not a schema requirement. It is included because
implementations that treat governance transactions identically to operational transactions
have an incomplete governance posture.

---

## Roles and Capabilities

### Normative Rule: Roles Are Governance Classifications, Not Implementation Labels

**This is a binding protocol rule.**

A role answers: *what governance function does this actor perform?*
An `implementation_ref` answers: *what tool, model, or system is this actor built on?*

These are separate claims and must never be conflated. Tool names, model names, vendor
product names, SaaS platform names, and runtime identifiers must not appear as `role` values.

**Valid role declarations:**

```
role: "executor",   implementation_ref: "custom-deploy-agent-v3"
role: "planner",    implementation_ref: "llm-gateway-local"
role: "validator",  implementation_ref: "test-runner-ci"
```

**Invalid role declarations:**

```
role: "codex"           // tool name is not a protocol role
role: "claude"          // model name is not a protocol role
role: "github-actions"  // platform name is not a protocol role
role: "gpt-4o"          // model identifier is not a protocol role
```

A control plane must reject any transaction envelope where an actor's `role` field contains a
value that is not a defined ZTAP protocol role. The reason code is `ROLE_INVALID`. There is
no pass-through mode for unrecognized role values.

Protocol roles must remain product-neutral so that ZTAP remains implementable by any
compliant control plane, regardless of which tools, models, or vendors actors use internally.

### Protocol Roles

The following roles are defined by the ZTAP protocol. They describe an actor's function in
the governance model — not their identity, implementation, or internal structure.

| Role | Description |
|---|---|
| `operator` | A human or human-delegated authority that configures policy, approves transactions when required, and manages the control plane. |
| `control_plane` | The ZTAP control plane instance. Evaluates policy, issues authorization records, records decisions, and retains the audit trail. |
| `source_actor` | The actor that initiates a transaction — creates the request envelope and submits it to the control plane. |
| `target_actor` | The actor that receives an authorized transaction, accepts it, and performs the requested work. |
| `planner` | An actor that produces structured plans or task decompositions, typically as input to executors. A planner does not execute. |
| `executor` | An actor that performs concrete actions against real systems. An executor does not plan independently. |
| `validator` | An actor that verifies results against defined criteria. A validator does not execute. |
| `auditor` | An actor with read-only access to the transaction log and receipts. Auditors do not participate in transaction execution. |
| `runtime` | An actor that provides execution infrastructure or environment. A runtime executes at the direction of executors. |

An actor may hold more than one role depending on registration and context. The control plane
enforces which roles an actor is permitted to perform in a given transaction.

### Role-to-Capability Binding

Roles do not automatically confer capabilities. An actor must be registered with both a role
and the specific capability claims that role permits them to exercise.

A transaction requesting capability `deploy_service` from an actor registered as `executor`
is valid only if that executor's registration includes `deploy_service` in its capability
claims. A capability not registered against an actor may not be invoked, regardless of role.

### Example Role Mapping

The following is an illustrative mapping, not a protocol requirement:

| Concrete Actor | ZTAP Role(s) |
|---|---|
| Human engineer / system owner | `operator` |
| Orchestration layer | `control_plane` |
| Planning agent | `planner`, `source_actor` |
| Execution agent | `executor`, `target_actor` |
| QA / test agent | `validator` |
| Infrastructure runtime | `runtime`, `target_actor` |

---

## Example Lifecycle Walkthrough

The following is a plain-language walkthrough of a ZTAP transaction for a production deployment
request. Field names are illustrative. This example assumes auto-authorization by policy —
no human approval is required.

---

**Step 1: Source actor creates the transaction envelope.**

A planning agent has determined that service `billing-api` should be deployed to the production
environment. It constructs a ZTAP transaction envelope containing:
- its own identity claim,
- the role it is acting in (`planner`, `source_actor`),
- the identity of the target actor (the executor registered for production deployments),
- the capability being requested (`deploy_service`),
- the request parameters (service name, environment, version),
- the declared atomicity mode (`atomic_required`),
- and a validity window (the transaction must be accepted within N minutes).

The planning agent computes a hash of the request payload and includes it in the envelope.

State: `created`

---

**Step 2: Source actor submits the envelope to the control plane.**

The planning agent delivers the envelope to the ZTAP control plane. The transport used (API
call, message queue, etc.) is irrelevant to the protocol.

The control plane acknowledges receipt and assigns a stable transaction identifier.

State: `submitted`

---

**Step 3: Control plane evaluates the transaction.**

The control plane checks:
- Is the planning agent registered? ✓
- Does it hold the `source_actor` role? ✓
- Is the target executor registered? ✓
- Does the executor hold the `deploy_service` capability? ✓
- Does the request hash match the payload? ✓
- Does policy permit this actor to request this capability against this target? ✓
- Is additional evidence required? (No, per policy for this service/environment combination.)

State: `evaluated`

---

**Step 4: Control plane authorizes the transaction.**

Policy determines this transaction may be auto-authorized. No human approval is required.

The control plane appends an authorization record to the transaction:
- outcome: `auto_authorized`
- policy reference that authorized it
- timestamp

State: `authorized`

---

**Step 5: Target actor receives and accepts the transaction.**

The authorized transaction envelope — now including the authorization record — is delivered
to the executor. The executor confirms:
- the envelope carries a valid authorization record from the control plane,
- the request hash matches the payload,
- the capability requested is in its registration,
- it is able to perform the work.

The executor accepts the transaction.

State: `accepted`

---

**Step 6: Executor performs the work.**

The executor deploys `billing-api` to production.

State: `executing`

---

**Step 7: Result is verified.**

The executor (or a registered validator) confirms the deployment succeeded: the service is
running, health checks pass, the version matches. The result is checked against the
verification requirements specified in the transaction.

State: `verifying`

---

**Step 8: Receipt is produced and returned.**

The executor produces a ZTAP receipt containing:
- the transaction identifier,
- the hash of the original request envelope,
- the execution outcome (success),
- verification result,
- timestamp,
- a hash of the receipt itself.

The receipt is submitted to the control plane, which verifies the request hash matches and
records the receipt in the audit trail.

State: `succeeded`

---

**Audit trail at conclusion:**

The control plane now holds a complete, hash-linked record of:
1. The original request envelope (immutable, hashed)
2. The evaluation record
3. The authorization record
4. The acceptance record
5. The execution receipt (hash-linked to the original request)

Any of these records can be independently verified. The chain of hashes makes tampering
detectable at any link.

---

## Open Questions

> **Traceability note:** The original pre-schema questions listed below have been addressed
> by operator decisions recorded in `SCHEMA.md`. They remain here for historical traceability
> until the schema is finalized and a changelog or decision log replaces them.

The following decisions required operator input before the ZTAP schema could be drafted:

1. **Validity window** — how is a transaction's validity window expressed? Is it a duration,
   an absolute timestamp, or both? Who sets it — the source actor, the control plane policy,
   or the transaction type?

2. **Receipt structure** — what is the minimum required content of a success receipt? A failure
   receipt? Are they the same structure with different fields populated, or separate envelope
   types?

3. **Evidence envelope structure** — what is the required structure for an evidence envelope?
   Is evidence typed (e.g., test results vs. compliance attestations), or is it treated as
   opaque structured data?

4. **Amendment events** — are amendment events a first-class envelope type with their own
   lifecycle, or are they a subtype of a general "linked event" structure?

5. **Cancellation authority** — who may cancel a transaction? Only the operator? The source
   actor? The control plane on behalf of a policy trigger? All of the above under different
   conditions?

6. **Target rejection** — when a target actor rejects an authorized transaction (reason code
   `TARGET_REJECTED`), is the source actor permitted to retry with a new transaction
   automatically, or does it require operator intervention?

7. **Partial state documentation** — when `PARTIAL_STATE_BLOCKED` occurs, what is the required
   structure of the failure receipt? What information must be recorded to support recovery or
   manual remediation?

8. **Multi-target transactions** — does ZTAP v1 support transactions that request actions from
   more than one target actor? Or is a ZTAP transaction strictly one source, one target?

9. **Canonical JSON and hash construction** — what is the exact canonicalization rule? (e.g.,
   alphabetical key ordering, no whitespace, UTF-8 encoding.) This must be specified before
   any schema is finalized.

10. **Control plane minimum conformance** — what is the minimum set of operations and behaviors
    a control plane must implement to be considered ZTAP-compliant? This is required before
    third-party control plane implementations can be evaluated.

---

## Next Steps

This document has established the doctrine, lifecycle, governance model, and core principles
that govern ZTAP. The logical sequence from here:

**Immediate: Resolve open questions.**
The questions in Section 16 are blocking schema work. Answers to questions 1 (validity window),
2 (receipt structure), 8 (multi-target), and 9 (canonicalization) are required before any
schema file can be written with confidence.

**Next: Create `SCHEMA.md` or `schemas/`.**
Once the open questions are resolved, a formal schema document can define field names, required
vs. optional fields, envelope types, versioning, and hash construction rules. This may be a
single `SCHEMA.md` prose document before producing machine-readable schema files.

**Following: Create `examples/`.**
Reference examples — both valid and deliberately invalid — help implementors understand the
protocol and allow validators to test compliance. Examples should cover the happy path, each
failure mode, and each authorization outcome.

**Later: `WHITEPAPER.md`.**
The external-facing argument for ZTAP adoption is more credible once the specification exists.
The whitepaper synthesizes the problem, the solution, and the governance model for an executive
or architect audience. It is not a technical reference — it is the adoption document.

**Future: Cross-organizational federation.**
Multi-organization ZTAP interaction — where one organization's agents transact with another's,
each validated by their respective control planes — is explicitly deferred from v1 scope. It
is the logical extension of the single-organization model and should be addressed in a future
specification revision after v1 is stable.

---

> ZTAP Specification Draft v0.1 — Pre-Schema.
> Zero Trust Agent Protocol: the open protocol for governed agent transactions.
> **Freedom for engineers. Governance for the organization.**
