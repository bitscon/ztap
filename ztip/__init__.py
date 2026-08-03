"""ZTIP reference runtime — canonicalization, hashing, and integrity verification.

Reference implementation for the ZTIP (Zero Trust Intelligence Protocol) open standard.
Self-contained: depends only on the Python standard library, so the protocol
repository builds and verifies on its own (per AGENTS.md portability rules).
"""

from .canonical import canonicalize, canonical_bytes
from .hashing import (
    CANONICALIZATION,
    HASH_ALGORITHM,
    envelope_hash,
    verify_envelope_hash,
)

__all__ = [
    "canonicalize",
    "canonical_bytes",
    "envelope_hash",
    "verify_envelope_hash",
    "HASH_ALGORITHM",
    "CANONICALIZATION",
]
