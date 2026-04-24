# ZTAP Whitepaper

*Zero Trust Agent Protocol — A Governance Envelope for Verifiable Agent Work*

Version: `1.0-draft` · Status: Pre-release · Repository: [github.com/bitscon/ztap](https://github.com/bitscon/ztap)
Author: Chad McCormack
Project: Zero-Trust Intelligence / ZTAP

---

## Executive Summary

AI agents are being deployed into production systems at a pace that has outrun the governance frameworks designed to manage them. Engineers are using the tools that make them productive. Organizations are trying to maintain control over what those tools are allowed to do. Today, those two goals are in conflict.

ZTAP — the Zero Trust Agent Protocol — exists to end that conflict.

ZTAP is an open governance envelope and transaction protocol. It defines how every agent-initiated action — whether a deployment, a query, a code change, a message, or any other governed operation — must be structured so it is authorized by policy, verifiable by hash, and auditable by any person or system that needs to inspect it.

ZTAP does not restrict which agents, models, or tools engineers use. It wraps the transaction, not the toolchain. Any agent framework can participate in ZTAP. Any transport can carry a ZTAP envelope. Any control plane that meets the protocol's conformance requirements can evaluate and authorize ZTAP transactions.

The result: organizations can support the agent and tool freedom their engineers need while maintaining the authorization, accountability, integrity, and auditability their governance requirements demand.

**Code freedom, Verified.**

---

## The Problem: Agent Freedom Without Governance

### What engineers want

Engineers want to use the AI agents and tools that make them productive. They want to use the model that writes the best code, the framework that orchestrates the best pipeline, the tool that integrates most easily with their stack. They do not want to submit a change management ticket to get a new AI tool approved. They do not want to use a slower, weaker tool because it was pre-approved two years ago.

This is a reasonable demand. Tool choice is a genuine productivity multiplier in AI-assisted workflows. Constraining it drives workarounds and slows delivery.

### What organizations need

Organizations need to know what their AI agents are doing to production systems. They need to be able to answer, at any time: who authorized this action, what was the policy basis, what exactly was requested, what was the result, and where is the proof?

They need to be able to enforce policy — some agents can deploy to staging but not production; some actions require human approval; some capabilities require prior evidence. They need these controls to be machine-enforceable, not dependent on instructions in a system prompt.

They need an audit trail that holds up. Not a log of LLM chat messages. A record of what was authorized, what was executed, and whether the result matched the authorized action.

### The current gap

In most multi-agent systems today, one agent passes a message to another. The other agent runs it. Nothing is authorized. Nothing is verified. Nothing is auditable. The requesting agent and the executing agent share no formal contract about what was permitted, what happened, or whether it was correct.

This is ambient authority. An agent that can invoke another agent implicitly holds the combined authority of both, with none of the accountability of either. When something goes wrong — and in complex agent pipelines, things will go wrong — the organization cannot reconstruct what happened, who authorized it, or whether the outcome matched the intent.

The standard response has been to lock down tools: approve a short list of agents, require everything else to go through a change process. This imposes friction, kills velocity, and does not actually solve the governance problem — it just limits the surface area of ungoverned action.

ZTAP offers a different answer: govern the transaction, not the tool.

---

## The ZTI Doctrine

Zero Trust Intelligence (ZTI) is the governance doctrine behind ZTAP.

The core principle: do not trust AI outputs or AI-initiated actions simply because they came from a capable model. Verify the authority behind the action. Verify the integrity of the request. Verify that the outcome matches what was authorized.

ZTI is not a product. It is a philosophy about how AI systems should relate to the deterministic governance structures that organizations depend on.

Three ideas form the ZTI doctrine:

**1. Models draft. Deterministic systems govern.**
An AI agent can propose a deployment, draft a code change, or recommend an action. That proposal is not an authorization. It is a draft. The governance layer — not the model's confidence — determines whether the action is permitted.

**2. Trust must be proven, not assumed.**
An agent that arrives via a trusted API, over an encrypted channel, or from a well-known vendor is not, by that fact, authorized to act. Authorization comes from a verified governance record, not from the properties of the transport or the reputation of the sender.

**3. Every action leaves an auditable record.**
If an action cannot be audited — if there is no record of what was requested, what was authorized, and what occurred — then from a governance perspective it effectively did not happen in a controllable way. Governance requires receipts.

ZTAP is the protocol-level expression of these three principles.

---

## What ZTAP Is

ZTAP defines a set of structured JSON envelope types and a transaction lifecycle that together provide the governance layer for agent work. The key concepts:

### ZTAP Transaction

The full governed unit of work. A transaction begins when a source actor creates a request and ends when a final receipt is produced. A transaction is not a single message — it is a lifecycle, with defined states and transitions, each producing a linked record.

### ZTAP Envelope

The serialized JSON object that carries a transaction event. Five envelope types: `transaction_request`, `authorization_decision`, `execution_receipt`, `evidence_record`, and `amendment_event`. Envelopes are immutable once submitted. Subsequent events produce new, linked envelopes rather than modifying prior ones.

### ZTAP Receipt

The result envelope produced at the end of a transaction. A receipt references the original request by hash, records what was attempted and what was completed, and provides the information needed to verify that the result corresponds to what was authorized. Every terminal state — success, failure, rejection, cancellation, expiry — produces a receipt.

### ZTAP Control Plane

The authority layer that evaluates policy, records authorization decisions, and governs whether transactions may proceed. The control plane is the single source of authorization. It evaluates actor identity and registration, capability claims, organizational policy, and evidence requirements before issuing an authorization record.

ZTAP defines what a control plane must do, not what it must be. Any implementation that meets the ZTAP conformance requirements is a valid control plane.

### Actor

Any entity that participates in a ZTAP transaction: an AI agent, an automated system, or a human. All actors must be identifiable to the control plane.

### Role

A protocol-level governance classification. ZTAP defines nine roles: `operator`, `control_plane`, `source_actor`, `target_actor`, `planner`, `executor`, `validator`, `auditor`, and `runtime`. Roles describe the governance function an actor performs, not the tool or model behind the actor.

**This distinction matters.** An actor's role is `executor`. The tool that implements the executor — whatever AI model, runtime, or framework it uses — is optional metadata, recorded in `implementation_ref`. Tool names, model names, and vendor names are not protocol roles. A system that uses tool names as roles has made the protocol vendor-dependent. ZTAP does not.

### Capability

A declared ability that an actor is registered to exercise. Capabilities are separate from roles. Holding the `executor` role does not automatically grant any specific capability. Each capability — `org.example/deploy_service`, `git.push`, `test.run` — must be explicitly registered against the actor and validated by the control plane at transaction evaluation time.

### Evidence

Supporting material submitted to satisfy a policy requirement. Evidence may include test results, approval records, commit references, deployment status, compliance attestations, or other structured data the control plane requires before authorizing a transaction. Evidence is hash-linked to the transaction it supports.

---

## What ZTAP Is Not

Clarity about what ZTAP does not do is as important as clarity about what it does.

**ZTAP is not a transport protocol.** How envelopes move between actors — API, file, message queue, chat, workflow engine, email — is entirely outside ZTAP's scope. A ZTAP envelope may travel by any mechanism. The governance properties of the envelope do not depend on the transport.

**ZTAP is not an AI model.** ZTAP does not generate, evaluate, or select AI outputs. It governs whether AI-initiated actions are authorized to proceed.

**ZTAP is not a user interface.** How operators interact with the control plane, review approvals, or browse audit records is an implementation decision. ZTAP defines the protocol-level contract, not the interface to it.

**ZTAP is not a replacement for MCP.** The Model Context Protocol connects agents and models to tools, data sources, APIs, and resources. ZTAP and MCP address different layers of the same system.

**ZTAP is not a replacement for A2A.** Agent-to-Agent communication protocols define how agents discover and communicate with each other. ZTAP governs the authorization and accountability layer for what agents do, not how they find each other or what protocol they use to communicate.

**ZTAP is not ZTI Core's private API.** ZTI Core is one possible commercial control-plane implementation. ZTAP is the open protocol. They are distinct. ZTAP must remain implementable by any organization's own control plane infrastructure.

**ZTAP is not an encryption mandate.** ZTAP requires integrity — hash-based tamper detection — but does not require encryption. Envelopes are human-readable JSON by default. Encryption may be layered on by deployment policy, transport requirements, or organizational security controls, but it is not a core protocol requirement.

**ZTAP does not prevent ungoverned messages from existing.** Any system can generate arbitrary messages. ZTAP's guarantee is narrower and more valuable: a compliant executor will not accept an ungoverned message as authorized work. Ungoverned messages cannot be promoted to governed transactions inside a ZTAP-compliant environment without passing through the control plane.

---

## How ZTAP Works

### The Transaction Lifecycle

A ZTAP transaction moves through a defined sequence of states:

```
created → submitted → evaluated → authorized → accepted → executing → verifying → succeeded
                                ↓                                                  ↓
                             rejected                                           failed
                                                                               cancelled
                                                                               expired
```

Each state transition produces or references a linked envelope. The complete history of a transaction is the ordered set of all linked envelopes — an append-only, hash-linked record.

**`created`** — The source actor constructs the transaction request envelope. The request captures the action being requested, the actor identities, the capability being invoked, the risk level, the expected verification outcomes, and the integrity hash of the request payload.

**`submitted`** — The source actor delivers the envelope to the control plane. The control plane assigns a stable transaction identifier and acknowledges receipt.

**`evaluated`** — The control plane checks schema validity, actor registration, role authorization, capability claims, policy compliance, evidence requirements, and the integrity hash. This is deterministic evaluation. The model's confidence is not part of the evaluation.

**`authorized` or `rejected`** — The control plane issues an authorization decision. The decision carries one of five statuses: `auto_authorized`, `human_approval_required`, `human_approved`, `evidence_required`, or `rejected`. Authorization is policy-determined. Some transactions are auto-authorized by policy. Some require human approval. Some require prior evidence. Some are denied.

A critical distinction: **`authorized` and `accepted` are separate states.** Authorization means the governance layer permitted the action. Acceptance means the target actor received the authorization and agreed to proceed. Both must occur before execution begins.

**`executing` and `verifying`** — The target actor performs the work and checks the outcome against the verification requirements declared in the original request.

**`succeeded`, `failed`, `cancelled`, or `expired`** — Every terminal state produces a receipt. The receipt references the original request hash, records what was attempted and completed, and provides structured verification results. A transaction that does not produce a receipt is not ZTAP-compliant.

### Authorization Is Policy-Conditional

ZTAP does not require human approval for every transaction. Authorization is determined by organizational policy. Some transactions are auto-authorized. Some require human sign-off. Some require evidence. Some are rejected outright.

When human approval is required, ZTAP requires that the approval be recorded as a structured, time-bounded record — identifying the approver, the timestamp, and the exact scope of the approval. An informal approval — a Slack message, a verbal sign-off — is not a ZTAP-compliant approval.

Human approvals are transaction-specific and single-use. An approval for one transaction cannot be applied to a different transaction. An expired approval cannot be reused. ZTAP calls this enforcement `APPROVAL_REPLAYED` — a first-class rejection reason.

### Break-Glass Access

Emergency situations require fast action. ZTAP supports break-glass access — but break-glass is a governed path, not an authorization bypass.

A break-glass transaction in ZTAP carries more required evidence than a standard authorization, not less. An incident reference, a named approver, compensating controls, a strict expiration, and a post-incident review commitment are required. A break-glass action that bypasses the control plane is not a legitimate break-glass. It is an unauthorized action.

### Governance-Class Transactions

Not all transactions are equal in their governance implications. An agent deploying a service and an agent modifying its own capability grants are fundamentally different risk classes.

ZTAP distinguishes operational transactions (ordinary work against systems) from governance transactions (modifications to policies, actor registrations, capability grants, or control-plane configuration). Governance transactions require stricter authorization — they change the rules under which future transactions are evaluated, and must therefore be held to the most rigorous policy thresholds.

### The Audit Trail

Every ZTAP transaction leaves a hash-linked audit trail. Each envelope references its predecessors by cryptographic hash. Modifying any stored record changes its hash, invalidating the chain and making tampering detectable.

This is the difference between a log and an audit trail. A log records what happened. An audit trail proves it.

---

## The Trust Boundary

**ZTAP does not secure the pipe. ZTAP governs the action.**

This is the most important principle in the protocol and the one most commonly misunderstood.

Transport security — TLS, authenticated APIs, signed requests, private networks — does not make an agent action governed. An agent that arrives over a secure channel is not authorized by that fact. The authorization record, issued by the control plane, is what makes a transaction governed. The transport is irrelevant to ZTAP's governance properties.

ZTAP governance is enforced at the point of action. A compliant executor refuses to perform governed work unless it holds a valid, unexpired, transaction-bound ZTAP authorization record. The executor does not trust the transport. It does not trust the source actor's claims. It verifies the authorization record.

The practical implications:

- An AI agent that sends instructions to a compliant executor without a valid ZTAP authorization record will have its request refused — regardless of which model generated the instruction, which framework delivered it, or which channel it arrived on.
- A model that generates a highly confident instruction does not thereby authorize that instruction. Confidence is not authorization.
- A "trusted internal tool" that bypasses the control plane is not a ZTAP-compliant executor. ZTAP has no trusted internal path.
- The governance layer and the execution layer are permanently separate. The entity that governs does not execute. The entity that executes does not self-authorize.

This is the zero-trust application of agent governance: trust no actor by default, verify every authorization at the point of action.

---

## Integrity Over Encryption

**ZTAP requires integrity, not secrecy.**

ZTAP envelopes are transparent JSON governance packages. By design. An auditor should be able to read a ZTAP envelope without a decryption key, without a proprietary tool, and without special permissions. The envelope is the record. Secrecy would make audit harder without making governance stronger.

What ZTAP requires is integrity: tamper detection. Every ZTAP envelope carries a cryptographic hash of its contents, computed using RFC 8785 JSON Canonicalization Scheme (JCS) and SHA-256. This makes any modification to a submitted envelope detectable. The hash is what proves an envelope has not been altered since it was created.

The hash chain is the audit trail. Each receipt references the original request envelope by hash. Each evidence record is hash-linked to its transaction. Modifying any record in the chain breaks the hashes that follow it. The chain makes tampering detectable, not just recordable.

Encryption is policy-conditional. Organizations may require envelopes to be transmitted or stored in encrypted form, depending on the sensitivity of the data in the parameters or the requirements of their deployment context. ZTAP does not prohibit encryption. It simply does not mandate it as a protocol requirement, because doing so would make ZTAP harder to adopt, harder to audit, and dependent on key management infrastructure that not every deployment context provides.

The principle: governance comes from verifiable structure and integrity checks, not from keeping the record secret.

---

## Relationship to MCP and A2A

ZTAP is designed to complement the emerging agent communication ecosystem, not compete with it.

**MCP** (Model Context Protocol) defines how AI models and agents connect to tools, data sources, and external resources. MCP is a connectivity and capability layer — it answers the question "what can this agent access?"

**A2A** (Agent-to-Agent communication protocols) define how agents discover each other, communicate, and coordinate. A2A is a communication and interoperability layer — it answers the question "how do agents talk to each other?"

**ZTAP** governs the transaction, authority, integrity, receipts, and evidence layer — it answers the question "was this action authorized, and can it be proven?"

These are distinct layers that can operate together:

```
MCP connects.
A2A communicates.
ZTAP verifies governed action.
```

A ZTAP envelope may travel through an A2A communication channel. A ZTAP-governed action may invoke an MCP-connected tool as the execution step. MCP and A2A are not primarily designed to provide ZTAP's transaction-level authorization, receipt, and evidence model. That is ZTAP's role.

ZTAP does not require MCP or A2A to be present. It does not depend on any specific agent communication layer. And it does not prevent organizations from using MCP or A2A — it adds a governance layer on top of whatever agent communication infrastructure they already have.

---

## ZTI Core and Commercial Control Planes

ZTAP is an open protocol. The control plane that enforces it is not specified by the protocol — only the contract the control plane must fulfill.

ZTI Core is intended to be a separate, commercial implementation of a ZTAP-compliant control plane. It is designed to provide:

- an actor and capability registry with a management interface,
- policy authoring and enforcement,
- real-time transaction evaluation and authorization,
- human approval workflows with bounded, auditable approval records,
- evidence collection and verification,
- an append-only, hash-linked audit log,
- and an administrative interface for operators.

ZTI Core is designed to implement ZTAP. It is not ZTAP. The protocol specification in this repository defines the open standard. ZTI Core is one commercial product that implements that standard.

This distinction matters for adoption. Organizations that want to build their own ZTAP-compliant control plane can do so using the SPEC.md, SCHEMA.md, and CONFORMANCE.md documents in this repository. Organizations that want a managed, commercial implementation can use ZTI Core. The protocol remains open regardless.

ZTAP's openness is not marketing positioning — it is a design requirement. A protocol whose conformance requirements are only satisfiable by one vendor's product is not an open protocol. ZTAP's conformance levels, test matrix, and schema are published precisely so that any organization can implement and verify compliance independently.

---

## Example Scenario: A Governed Deployment

Here is what ZTAP governance looks like in practice, without protocol details getting in the way.

**The setup:** An engineering team uses a planning agent — whatever agent framework and model they prefer — to manage routine deployments. The organization has registered the planning agent and the deployment executor as ZTAP actors in their control plane, with appropriate roles and capability grants.

**The request:** The planning agent determines that `billing-api v2.4.1` should be deployed to production. It constructs a ZTAP transaction envelope declaring the action, the target executor, the expected verification outcomes, and the risk level. It hashes the envelope and submits it to the control plane.

**The evaluation:** The control plane checks: Is this actor registered? Does it have the right role? Does the target executor hold the deployment capability? Does policy permit this actor to request this capability in production? Is the declared risk level consistent with policy expectations for this service and environment? The checks are deterministic. The model's confidence is not consulted.

**The authorization:** Policy permits this transaction. The control plane issues an `auto_authorized` decision with a bounded validity window. The authorization is time-limited — if the executor does not accept within the window, the transaction expires.

**The execution:** The deployment executor receives the authorized transaction envelope. Before acting, it verifies: Does this envelope carry a valid authorization record? Does the request hash match the payload? Has the authorization window expired? Is the target actor identity correct? Only when all checks pass does the executor proceed.

**The receipt:** The executor deploys `billing-api v2.4.1`, runs health checks, and produces a ZTAP receipt referencing the original request hash. The receipt records what was attempted, what was completed, and whether verification passed. It is submitted to the control plane and added to the audit trail.

**The audit:** At any time, an auditor can retrieve the complete transaction record: the original request, the policy evaluation, the authorization decision, the execution receipt, and the verification results. The hash chain proves none of these records have been altered. The record answers the four questions every governance audit requires: What was requested? Was it authorized? What happened? Did it match the request?

**The engineer's experience:** The engineer used their preferred planning agent and executor. They did not need to request pre-approval for their toolchain. They did not experience additional latency in routine auto-authorized transactions. The governance layer was present for every action and visible in the audit trail — but not in their way.

For concrete envelope examples, see the [`examples/`](examples/) directory in this repository.

---

## Conformance and Adoption

ZTAP defines three conformance levels. Organizations can adopt incrementally.

### Level 1 — Envelope Validator

A Level 1 implementation can parse and validate ZTAP envelopes: check required fields, verify role values, validate hash integrity, and confirm that reason codes and evidence types meet the registry requirements. An envelope validator does not need to manage actor registrations or evaluate policy.

**Adoption use case:** Build envelope validation into a CI/CD pipeline or an audit tool before investing in a full control plane.

### Level 2 — Control Plane

A Level 2 implementation manages the full transaction lifecycle: actor and capability registration, policy evaluation, authorization decisions, human approval workflows, receipt ingestion, and hash-linked audit retention.

**Adoption use case:** Deploy or configure a control plane (self-hosted or using ZTI Core) that your agent executors submit transactions to.

### Level 3 — Governed Executor / Runtime

A Level 3 implementation enforces the trust boundary at the point of action: refusing governed work without a valid authorization record, verifying hashes before execution, producing receipts after execution.

**Adoption use case:** Wrap your existing execution agents — deployment tools, database executors, code runners — to participate in ZTAP governance.

### A Practical Adoption Path

Organizations new to ZTAP can adopt in stages without disrupting existing workflows:

1. **Validate envelopes.** Instrument existing agent pipelines to emit ZTAP-compliant transaction envelopes, and validate them against the schema.
2. **Register actors.** Define your actors, roles, and capability grants in a control plane.
3. **Evaluate policy before action.** Route transactions through the control plane for authorization before execution.
4. **Require receipts.** Require executors to produce and submit receipts for every governed action.
5. **Audit evidence.** Use the hash-linked audit trail to verify what happened, when, under what authorization, and with what outcome.

Each stage can be adopted independently and incrementally. The full governance model emerges from composing all five.

---

## Security Model and Limitations

ZTAP provides strong integrity and accountability guarantees within a defined scope. Being clear about those boundaries matters.

**What ZTAP provides:**

- A tamper-detectable, hash-linked record of every governed transaction.
- Deterministic schema validation that rejects malformed, unauthorized, or integrity-failed envelopes.
- A clear, auditable record of what was authorized, by whom, under what policy, and with what result.
- Fail-closed behavior: in the absence of a valid authorization record, execution does not proceed.

**What ZTAP does not provide:**

- ZTAP cannot stop arbitrary ungoverned messages from existing. It can only prevent those messages from being accepted as governed work inside a compliant environment.
- Schema validation does not verify that hash values were computed correctly — that requires runtime implementation. ZTAP specifies the algorithm; implementing it correctly is the adopter's responsibility.
- Policy quality matters. A ZTAP control plane with a permissive policy provides weak governance regardless of protocol compliance.
- Registry consistency matters. A control plane that issues authorization decisions against an inconsistent actor or capability registry cannot be trusted. ZTAP specifies that registries must be consistent before authorization is issued — enforcing this at runtime is the implementation's responsibility.
- ZTAP is not a substitute for secure infrastructure, identity management, transport controls, or organizational security practices. It is a governance layer, not a security perimeter.

**The honest summary:** ZTAP provides a strong, auditable governance envelope for agent actions in organizations that implement it correctly and enforce its requirements consistently. It does not provide those guarantees for systems that implement it incorrectly, selectively, or in name only.

---

## Roadmap

ZTAP is in active development. The current specification is at `1.0-draft`. The roadmap:

**Phase 1 — Protocol Draft Stabilization (current)**
Closing remaining `1.0-draft` ambiguities. Keeping protocol decisions coherent across `SPEC.md`, `SCHEMA.md`, `CONFORMANCE.md`, and `examples/`.

**Phase 2 — Schema and Conformance Hardening**
Tightening machine-readable schema validation. Expanding conformance test coverage and negative-path examples. Hardening the test matrix.

**Phase 3 — Whitepaper and Public Launch (this document)**
Publishing the protocol whitepaper. Finalizing public-facing launch materials and onboarding documentation.

**Phase 4 — Reference Validators and SDKs**
Providing reference validator implementations that other tools can build on or verify against. Publishing minimal SDK utilities for envelope creation and hash verification.

**Phase 5 — Ecosystem Compatibility**
Documenting compatibility patterns for MCP and A2A where appropriate. Preserving ZTAP's transport neutrality while providing practical integration guidance.

Protocol decisions are made in this repository. The roadmap is the community's. No delivery dates are promised.

---

## Conclusion

The agent ecosystem is not slowing down. AI agents are already deployed in production systems at organizations that have not yet determined how to govern them. The gap between agent capability and agent governance is widening.

ZTAP is designed for organizations that want to close that gap without closing off their engineers.

The protocol is open. The specification is public. The schemas are machine-verifiable, and the conformance requirements are testable. No organization is locked into a single vendor or implementation. Any team that can implement the ZTAP envelope structure and connect to a conformant control plane can participate in the governance model.

The goal is not to slow agents down. The goal is to make every agent action provable.

What was requested. What was authorized. What happened. Whether it matched.

**Code freedom, Verified.**

---

*ZTAP Whitepaper · `1.0-draft` · [github.com/bitscon/ztap](https://github.com/bitscon/ztap)*
*For protocol specification details, see [SPEC.md](SPEC.md), [SCHEMA.md](SCHEMA.md), and [CONFORMANCE.md](CONFORMANCE.md).*
*For concrete envelope examples, see [examples/](examples/).*
