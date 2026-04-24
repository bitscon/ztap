# Security Policy

## Reporting Security Issues
Please report suspected vulnerabilities privately.

Preferred path:
- Use GitHub private vulnerability reporting (Security Advisory / "Report a vulnerability") for this repository.

If private reporting is unavailable:
- Contact maintainers through a private channel and request secure handling.
- Do not post exploit details in public issues while a vulnerability is active.

When reporting, include:
- affected file(s) and protocol surface,
- impact and threat model,
- reproduction steps or proof of concept,
- suggested mitigation if available.

## Disclosure Expectations
- Do not file public exploit details for active vulnerabilities.
- We will triage reports, coordinate fixes, and communicate disclosure timing once mitigations are available.

## Security Scope
In scope for this repo:
- ZTAP specification and conformance text
- JSON Schemas under `schemas/`
- Example envelopes under `examples/`
- Validation tooling under `scripts/`

Out of scope for this repo:
- ZTI Core SaaS implementation details
- Third-party agents and runtimes
- Third-party transports and infrastructure

## Core Security Principles
- Integrity is mandatory.
- Encryption is policy-conditional, not a core protocol prerequisite.
- Governed work must be verified at the action boundary, not inferred from transport security alone.
