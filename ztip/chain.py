"""Integrity verification for ZTIP bundles.

Recomputes each envelope's hash and confirms cross-envelope hash references
resolve. A bundle with no findings is intact and tamper-free.
"""

from __future__ import annotations

from typing import Any

from .hashing import envelope_hash


def _envelopes(bundle: Any) -> list:
    if isinstance(bundle, dict) and isinstance(bundle.get("envelopes"), list):
        return bundle["envelopes"]
    if isinstance(bundle, list):
        return bundle
    return [bundle]


def verify_bundle(bundle: Any) -> list[dict]:
    """Return a list of integrity findings; an empty list means the bundle is intact.

    Each finding: ``{envelope_index, envelope_type, code, detail}`` where code is
    one of ``HASH_MISSING``, ``HASH_MISMATCH``, ``REQUEST_HASH_BROKEN``.
    """
    findings: list[dict] = []
    envelopes = _envelopes(bundle)
    request_hash_by_txn: dict[Any, str] = {}

    for index, env in enumerate(envelopes):
        etype = env.get("envelope_type", "unknown")
        computed = envelope_hash(env)
        stored = (env.get("integrity") or {}).get("hash_value")
        if stored is None:
            findings.append(_finding(index, etype, "HASH_MISSING", "no integrity.hash_value present"))
        elif stored != computed:
            findings.append(
                _finding(index, etype, "HASH_MISMATCH",
                         f"stored {_short(stored)} != computed {_short(computed)}")
            )
        if etype == "transaction_request":
            request_hash_by_txn[env.get("transaction_id")] = computed

    for index, env in enumerate(envelopes):
        ref = env.get("request_hash")
        if ref is None:
            continue
        expected = request_hash_by_txn.get(env.get("transaction_id"))
        if expected is not None and ref != expected:
            findings.append(
                _finding(index, env.get("envelope_type", "unknown"), "REQUEST_HASH_BROKEN",
                         "request_hash does not match the referenced request envelope")
            )

    return findings


def _finding(index: int, etype: str, code: str, detail: str) -> dict:
    return {"envelope_index": index, "envelope_type": etype, "code": code, "detail": detail}


def _short(value: str) -> str:
    return value[:16] + "..." if len(value) > 19 else value
