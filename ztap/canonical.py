"""RFC 8785 JSON Canonicalization Scheme (JCS) for ZTAP envelopes.

SPEC.md ("Integrity and Hashing -> Algorithm") mandates SHA-256 but leaves the
canonicalization rules "to be finalized before the v1 schema is frozen". This
module finalizes them as RFC 8785 (JCS) -- the scheme the example envelopes
already declare via ``integrity.canonicalization = "RFC8785-JCS"``.

Deterministic rules:
  * objects: members sorted by the UTF-16 code units of their keys, no whitespace
  * strings: only the RFC 8785 mandatory escapes; every other code point is
    emitted literally as UTF-8
  * integers: shortest decimal form
  * booleans / null: ``true`` / ``false`` / ``null``

ZTAP envelope values are strings, integers, booleans, arrays, and objects.
Non-integer numbers are not part of the envelope vocabulary; they are rejected
rather than silently mis-canonicalized.
"""

from __future__ import annotations

from typing import Any

_SHORT_ESCAPES = {
    0x08: "\\b",
    0x09: "\\t",
    0x0A: "\\n",
    0x0C: "\\f",
    0x0D: "\\r",
}


def _escape_string(value: str) -> str:
    out = ['"']
    for ch in value:
        code = ord(ch)
        if ch == '"':
            out.append('\\"')
        elif ch == "\\":
            out.append("\\\\")
        elif code in _SHORT_ESCAPES:
            out.append(_SHORT_ESCAPES[code])
        elif code < 0x20:
            out.append("\\u%04x" % code)
        else:
            out.append(ch)
    out.append('"')
    return "".join(out)


def _number(value: Any) -> str:
    if isinstance(value, bool):  # bool is a subclass of int
        raise TypeError("bool is not a JSON number")
    if isinstance(value, int):
        return str(value)
    # float
    if value != value or value in (float("inf"), float("-inf")):
        raise ValueError("NaN and Infinity are not valid JSON numbers")
    if value.is_integer():
        return str(int(value))
    raise NotImplementedError(
        "ZTAP envelopes are integer-only; non-integer float canonicalization is "
        "intentionally unimplemented to avoid silent divergence between implementations"
    )


def canonicalize(value: Any) -> str:
    """Return the RFC 8785 canonical JSON string for ``value``."""
    if value is None:
        return "null"
    if value is True:
        return "true"
    if value is False:
        return "false"
    if isinstance(value, str):
        return _escape_string(value)
    if isinstance(value, (int, float)):
        return _number(value)
    if isinstance(value, (list, tuple)):
        return "[" + ",".join(canonicalize(item) for item in value) + "]"
    if isinstance(value, dict):
        members = sorted(value.items(), key=lambda kv: str(kv[0]).encode("utf-16-be"))
        body = ",".join(
            _escape_string(str(key)) + ":" + canonicalize(val) for key, val in members
        )
        return "{" + body + "}"
    raise TypeError(f"Unsupported type for JCS canonicalization: {type(value).__name__}")


def canonical_bytes(value: Any) -> bytes:
    """Return the UTF-8 encoded RFC 8785 canonical form, ready for hashing."""
    return canonicalize(value).encode("utf-8")
