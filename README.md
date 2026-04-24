# ZTAP — Zero Trust Agent Protocol

> Every agent handoff is a trust decision. ZTAP makes that decision provable.

**Freedom for engineers. Governance for the organization.**

---

## What Is ZTAP?

ZTAP is an open protocol for governed agent transactions.

When one AI agent invokes another — or when an agent requests an action from a system, a human,
or a workflow — that interaction is a transaction. ZTAP defines how that transaction must be
structured so it is authorized, verifiable, and auditable after the fact.

ZTAP does not dictate transport. It does not restrict which agent framework, model, or tool your
engineers use. It governs the **transaction itself**: what was requested, whether it was authorized
by policy, and what happened.

The transport does not matter:

- API call
- File on disk
- Message queue
- GitHub PR
- Chat message
- Workflow engine trigger

ZTAP governs the **transaction artifact**, not how it moves.

---

## The Problem

AI agents are being chained together at scale. Planners invoke executors. Orchestrators invoke
specialists. Tools invoke tools.

None of these handoffs, in today's frameworks, carry governance. One agent passes a message to
another. The other runs it. Nothing is signed. Nothing is policy-checked. Nothing is auditable.

This is ambient authority — the most dangerous kind. An agent that can call another agent
implicitly holds the combined power of both, with none of the accountability of either.

At the same time, the answer is not to lock down which tools engineers can use. That creates
friction, slows delivery, and drives workarounds. Engineers need freedom to use whatever agent
tools help them move fast.

ZTAP solves both sides of that tension.

**Freedom for engineers. Governance for the organization.**

---

## Key Benefits

- **Tool-agnostic governance.** Engineers use any agent, model, or framework. ZTAP wraps the
  transaction, not the tool. No forced migration. No approved-tools list.
- **Every handoff is auditable.** Requests and their outcomes are captured as structured JSON
  artifacts with cryptographic integrity hashes. Every transaction leaves a record.
- **Policy-based authorization.** Transactions are evaluated against organizational policy.
  Some are auto-authorized. Some require human approval. Some are rejected outright. The policy
  decides — not the transport, not the agent.
- **No implicit trust.** There is no "trusted internal network" where governance is relaxed.
  A transaction without a valid authorization record does not pass.
- **Human-readable artifacts.** ZTAP artifacts are plain JSON. Integrity is enforced via
  cryptographic hashes, not encryption. Any person or system can read, store, and verify them.

---

## Relationship to ZTI and ZTI Core

ZTAP is part of the Zero Trust Intelligence (ZTI) ecosystem. The three components are distinct:

| Component | What It Is |
|-----------|-----------|
| **ZTI** | The verification doctrine: do not trust AI output blindly — verify it before it acts. |
| **ZTAP** | The open protocol: defines how governed agent transactions are structured and recorded. |
| **ZTI Core** | A control-plane implementation: evaluates policy, issues authorization records, and stores ZTAP artifacts. |

```text
ZTI (verification doctrine)
  └── ZTAP (open transaction protocol)
        └── ZTI Core (control plane — evaluates policy, authorizes, audits)
```

ZTAP is the protocol. ZTI Core is one compliant implementation of the control plane that enforces
it. Organizations may use ZTI Core or build their own compliant control plane.

---

## How a Governed Transaction Works

1. **An agent initiates a request.** It packages the request as a ZTAP transaction artifact —
   structured JSON describing what is being requested, by whom, and for what purpose.
2. **The control plane evaluates policy.** The artifact is submitted to the control plane (e.g.,
   ZTI Core). Policy determines the outcome: auto-authorize, require human approval, request
   additional evidence, or reject.
3. **An authorization record is issued.** If approved, the control plane appends an authorization
   record to the artifact. The artifact is now a complete, verifiable transaction.
4. **The target agent or system acts.** Only transactions carrying a valid authorization record
   proceed. The artifact, not a side-channel, is the proof of permission.
5. **The artifact is stored.** The complete transaction — request, policy evaluation, authorization
   outcome, and result — is recorded. The integrity hash chain makes post-hoc modification
   detectable.

---

## Conceptual Example

*The following is illustrative only. Field names and schema are not final — formal specification
is in progress.*

```json
{
  "ztap_version": "0.1-draft",
  "transaction_id": "txn_abc123",
  "requesting_agent": "planner-agent-7f3a",
  "target_capability": "deploy",
  "request_payload": {
    "service": "billing-api",
    "environment": "production"
  },
  "authorization": {
    "policy_evaluated": true,
    "outcome": "approved",
    "approved_by": "policy://deploy/production/auto",
    "recorded_at": "2026-04-24T14:00:00Z"
  },
  "integrity": {
    "payload_hash": "sha256:e3b0c44298fc...",
    "artifact_hash": "sha256:a1b2c3d4e5f6..."
  }
}
```

> **Note:** This example illustrates the concept of a governed transaction artifact. Exact field
> names, structure, and required fields are subject to formal specification. See `VISION.md` for
> the governing principles behind the schema design.

In this example, the transaction was authorized by policy automatically — no human approval was
required. A different policy configuration might have required a human to approve before
`artifact_hash` could be finalized and the transaction allowed to proceed.

---

## Authorization Is Policy-Conditional

ZTAP does not require human approval for every transaction. Authorization is determined by
organizational policy, evaluated by the control plane. Possible outcomes include:

- **Auto-authorized** — policy permits this transaction without human review.
- **Human approval required** — policy requires a named approver or role to sign off.
- **Additional evidence required** — policy requires supplemental context before a decision.
- **Rejected** — policy does not permit this transaction.

ZTAP supports all of these outcomes. The protocol records the outcome and the basis for it.
The organization defines the policy.

---

## What ZTAP Does Not Define (Yet)

ZTAP is in early doctrine and protocol design. The following are not yet specified:

- Canonical schema (field names, required vs. optional fields, versioning)
- Transport bindings (how artifacts move between agents and the control plane)
- SDK or library interfaces
- Identity and signing requirements
- Hash algorithm requirements

These will be defined as the specification matures. See `VISION.md` for the principles that
will guide those decisions.

---

## Current Status

ZTAP is in **pre-specification**. The doctrine, lifecycle, and governance model are being defined
before the schema is formalized. This repository is the canonical home for that work.

Contributions, questions, and alignment discussions are welcome.

---

> ZTAP: the open protocol for governed agent transactions.
> Where ZTI asks "was this decision verified?", ZTAP asks "was this handoff governed?"
