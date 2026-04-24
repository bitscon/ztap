# ZTAP Vision

*Zero Trust Agent Protocol — Why It Exists and Where It's Going*

---

## The Central Promise

**Freedom for engineers. Governance for the organization.**

Companies want to let their engineers use whatever AI agents and tools make them productive.
Leadership wants governance, accountability, auditability, and control over what those agents
are allowed to do.

Today, they are forced to choose. Lock down the tools, or lose visibility into what the tools do.

ZTAP exists so that organizations do not have to choose.

---

## Why ZTAP Exists

AI agents are increasingly being chained together. One agent plans. Another executes. A third
validates. A fourth triggers a deployment. Orchestrators delegate to specialists. Tools call
other tools.

None of these handoffs, in today's frameworks, carry governance. One agent passes a string to
another. The other runs it. No record is produced. No policy is checked. Nothing proves what
was requested, what was authorized, or what actually happened.

This is **ambient authority** — and it is the core governance failure of current multi-agent
architectures. An agent that can invoke another agent implicitly holds the combined authority of
both, with none of the accountability of either.

The answer is not to restrict which tools engineers use. Forced tool approval lists create
friction, slow delivery, and generate workarounds. Engineers need autonomy to choose tools that
work.

The answer is to govern the **transaction**, not the **tool**.

ZTAP defines how every agent interaction is wrapped in a structured, verifiable artifact — one
that records what was requested, whether it was authorized by policy, and what the outcome was.
The agent framework does not matter. The transport does not matter. The artifact governs the
transaction.

---

## The Problems It Solves

### 1. Ungoverned handoffs

In most agent architectures today, one agent invokes another with a plain function call or
message. There is no authorization envelope. No policy check. No artifact produced. Trust is
implicit and unverifiable.

ZTAP replaces implicit trust with an explicit, policy-evaluated, artifact-backed transaction.

### 2. No accountability chain

When something goes wrong in a multi-agent pipeline, reconstructing what happened is often
impossible. Which agent requested what? Who or what authorized it? When?

ZTAP's hash-linked artifact structure produces an unambiguous, tamper-evident record of every
transaction in the chain. Accountability is not an afterthought — it is built into the protocol.

### 3. Tool sprawl without governance

Engineering teams want to use LangChain, CrewAI, model-native tool use, custom frameworks, or
whatever is most effective. Requiring a single approved framework trades engineering velocity
for a false sense of control.

ZTAP governs the transaction, not the toolchain. Any agent framework can participate in ZTAP by
producing a compliant transaction artifact. Governance does not require uniformity.

### 4. Approvals that leave no machine-readable trace

Many teams add informal approval gates — "ping me before deploying to prod," a Slack check-in,
a verbal sign-off. These are not auditable. They are not verifiable. They cannot be reviewed,
replicated, or proven.

ZTAP formalizes policy-driven authorization as a structured record embedded in the transaction
artifact. The approval — or the policy decision that authorized the action automatically — is
part of the artifact, not a memory.

### 5. The transport problem

Agent interactions happen over APIs, message queues, files on disk, GitHub PRs, chat systems,
and workflow engines. Different transports mean different governance gaps.

ZTAP is transport-agnostic. The artifact travels however it needs to travel. The governance
travels with it.

---

## Core Principles

### Freedom for engineers. Governance for the organization.

ZTAP does not constrain which agents, models, frameworks, or tools engineers use. It constrains
whether a transaction between them is authorized.

Engineers choose their tools. The organization defines its policies. ZTAP is the layer that
connects them without requiring either side to compromise.

### Govern the transaction, not the transport

The transport is irrelevant to governance. An API call and a file-based handoff and a message
queue event all carry the same governance requirement: the transaction must be verifiable.

ZTAP defines the artifact structure that makes any transaction verifiable, regardless of how it
moves.

### Explicit authorization at every step

No agent capability is invoked without a transaction artifact that carries a valid authorization
record. There is no ambient authority. There is no "trusted internal path" where governance is
skipped. Every transaction is either explicitly authorized by policy or explicitly not.

### Policy-conditional authorization

Not all transactions are equal. Authorization is determined by organizational policy, not by
the protocol itself. ZTAP supports the full range of policy outcomes:

- **Auto-authorized** — the control plane confirms the transaction is within policy and proceeds
  without human review.
- **Human approval required** — organizational policy requires a named individual or role to
  approve before the transaction proceeds. ZTAP supports optional human-in-the-loop approval
  when required by policy.
- **Additional evidence required** — the control plane requires supplemental context or
  confirmation before making an authorization decision.
- **Rejected** — the transaction does not meet policy requirements and does not proceed.

The protocol records all of these outcomes. The policy defines which applies.

### Integrity without encryption

ZTAP artifacts are plain JSON. They are human-readable, debuggable, storable in any log system,
and reviewable by any tool.

Integrity is enforced via cryptographic hashes — not encryption. Hash fields in the artifact
answer three questions:

- Is this the original artifact, or has it been altered?
- Does the recorded request match what was actually submitted?
- Does the recorded result match what was actually returned?

Encryption is not a requirement of the initial protocol. It may be layered on top for specific
deployment contexts, but it is not ZTAP's responsibility to require it.

### Auditability is not optional

A transaction that cannot be audited is a transaction that cannot be governed. ZTAP's artifact
structure is designed from the ground up to answer three questions unambiguously and
verifiably:

1. What was requested?
2. What was the authorization outcome, and what was its basis?
3. What happened?

If a ZTAP artifact cannot answer all three questions, it is not a complete artifact.

### The control plane is authoritative

ZTAP does not self-govern. Authorization records are issued by a compliant control plane —
such as ZTI Core. Policy is managed there. Identity verification happens there. The audit log
lives there.

This means policy can change without touching agent code. An agent that submits a non-compliant
transaction to the control plane receives no authorization. Governance is enforced at the
artifact level, not the framework level.

---

## The Relationship Between ZTI, ZTAP, and ZTI Core

These three things are related but distinct:

**ZTI — the doctrine**
Zero Trust Intelligence is a verification philosophy: AI outputs should not be trusted to act
without verification. ZTI defines the principle that every AI-driven action must pass through a
deterministic verification layer before execution.

**ZTAP — the open protocol**
ZTAP is the agent-level expression of the ZTI doctrine. It defines how governed transactions
between agents — and between agents and humans or systems — must be structured. ZTAP is
transport-agnostic and framework-agnostic. It is an open protocol, not tied to any specific
implementation.

**ZTI Core — the control plane**
ZTI Core is a compliant implementation of the control plane that the ZTAP protocol requires.
It evaluates policy, issues authorization records, stores artifacts, and provides audit access.
Organizations may use ZTI Core or build their own control plane that satisfies ZTAP's
authorization and auditability requirements.

```text
ZTI (verification doctrine)
  └── ZTAP (open transaction protocol — this repo)
        └── ZTI Core (one compliant control-plane implementation)
```

ZTAP defines what must be true of a governed transaction. ZTI Core is one way to make it true.

---

## How ZTAP Ensures Integrity and Auditability

Each ZTAP transaction produces a structured artifact containing:

- **Requesting agent identity** — which agent initiated the transaction.
- **Requested action** — what capability or outcome was requested, and with what parameters.
- **Policy evaluation record** — the control plane's decision and its basis (policy reference,
  outcome, timestamp).
- **Authorization outcome** — auto-approved, human-approved, rejected, or pending. If human
  approval was required, the approver identity and timestamp are recorded.
- **Payload integrity hash** — a cryptographic hash of the request payload, proving it was not
  modified after submission.
- **Artifact integrity hash** — a hash of the complete artifact, including the payload hash,
  providing end-to-end tamper detection.

Artifacts are stored in an append-only log. Each artifact references the prior transaction in
the chain. Modifying any artifact invalidates the hashes of all subsequent artifacts, making
tampering detectable.

This is an integrity and accountability mechanism, not a security perimeter. The goal is not
to prevent a determined attacker from altering a log — it is to ensure that under normal
operating conditions, every transaction is provably what it claims to be.

---

## Initial Scope

The first version of ZTAP is scoped to a single-organization deployment:

- One organization
- Multiple agents, using any approved or unapproved frameworks
- One control plane (e.g., ZTI Core) enforcing organizational policy
- Governed, artifact-backed transactions between agents and systems
- An auditable record of every transaction

This is the problem that matters most first. The majority of organizations running multi-agent
workloads today have zero transaction governance. ZTAP's initial scope delivers governance where
there is currently none.

---

## Future Vision

### Protocol standardization

ZTAP publishes a canonical schema, validation rules, and a reference artifact library. Any agent
framework can produce a valid ZTAP artifact with a thin integration layer. Compliance can be
verified programmatically.

### Ecosystem integration

Agent orchestration platforms, IDE plugins, and CI/CD tools adopt ZTAP artifact production
natively. Governance becomes a byproduct of normal engineering workflows, not a separate gate.
ZTI Core and compatible control planes become available as managed services.

### Cross-organizational federation *(future direction)*

As multi-agent workloads extend beyond single-organization boundaries — where one company's
agents interact with another's — ZTAP provides the trust artifact that makes those interactions
governable across organizational lines. Each organization's control plane validates artifacts
against its own policy. The protocol enables interoperability. The control plane enforces
sovereignty.

This is a future direction. It is not in scope for the initial specification.

---

## What Comes Next

ZTAP's immediate next steps are doctrine and specification work:

1. **Transaction lifecycle model** — define the canonical lifecycle of a ZTAP transaction: from
   initiation through policy evaluation, authorization, execution, and artifact finalization.
2. **Formal schema specification** — define required and optional fields, versioning strategy,
   and hash construction rules.
3. **Control plane interface definition** — define what a compliant control plane must expose
   for ZTAP artifact submission, authorization issuance, and audit retrieval.
4. **Reference implementation** — a minimal library that produces and validates ZTAP artifacts,
   usable independent of any specific agent framework.

Schema files and implementation code will follow specification work, not precede it.

---

> ZTAP is the open protocol for governed agent transactions.
> The doctrine: every agent handoff is a trust decision.
> The protocol: make that decision structured, authorized, and verifiable.
> The promise: **freedom for engineers. Governance for the organization.**
