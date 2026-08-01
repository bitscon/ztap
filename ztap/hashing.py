"""ZTAP envelope integrity hashing: SHA-256 over the RFC 8785 canonical form.

The stored ``integrity.hash_value`` is computed over the envelope with:
  * non-normative annotation fields (keys beginning with ``_``) removed, and
  * ``integrity.hash_value`` itself excluded (a value cannot hash itself).

Any implementation that follows these rules recomputes the same hash, which is
what turns the repository's example hashes from placeholders into real,
independently verifiable integrity references.
"""

from __future__ import annotations

import hashlib
from typing import Any

from .canonical import canonical_bytes

CANONICALIZATION = "RFC8785-JCS"
HASH_ALGORITHM = "SHA-256"


def _strip_non_normative(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            key: _strip_non_normative(val)
            for key, val in value.items()
            if not str(key).startswith("_")
        }
    if isinstance(value, (list, tuple)):
        return [_strip_non_normative(item) for item in value]
    return value


def envelope_hash(envelope: dict) -> str:
    """Return the lowercase-hex SHA-256 of the canonicalized envelope.

    Excludes non-normative annotation fields and ``integrity.hash_value``.
    """
    prepared = _strip_non_normative(envelope)
    integrity = prepared.get("integrity")
    if isinstance(integrity, dict):
        prepared["integrity"] = {
            key: val for key, val in integrity.items() if key != "hash_value"
        }
    return hashlib.sha256(canonical_bytes(prepared)).hexdigest()


def verify_envelope_hash(envelope: dict) -> bool:
    """Return True iff the envelope's stored hash matches its recomputed hash."""
    integrity = envelope.get("integrity")
    if not isinstance(integrity, dict):
        return False
    stored = integrity.get("hash_value")
    return isinstance(stored, str) and stored == envelope_hash(envelope)
