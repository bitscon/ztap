"""Tests for the ZTAP reference runtime: canonicalization, hashing, integrity."""

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from ztap.canonical import canonicalize  # noqa: E402
from ztap.chain import verify_bundle  # noqa: E402
from ztap.hashing import envelope_hash, verify_envelope_hash  # noqa: E402


def test_object_keys_sorted():
    assert canonicalize({"b": 1, "a": 2}) == '{"a":2,"b":1}'


def test_no_insignificant_whitespace():
    assert canonicalize({"x": [1, 2, 3]}) == '{"x":[1,2,3]}'


def test_string_escaping():
    assert canonicalize('a"b\\c\n') == '"a\\"b\\\\c\\n"'


def test_unicode_emitted_literally():
    assert canonicalize("café") == '"café"'


def test_hash_is_deterministic_regardless_of_key_order():
    a = {"envelope_type": "x", "b": 1, "a": 2}
    b = {"a": 2, "b": 1, "envelope_type": "x"}
    assert envelope_hash(a) == envelope_hash(b)


def test_hash_excludes_own_value_and_annotations():
    base = {"envelope_type": "x", "v": 1, "integrity": {"hash_algorithm": "SHA-256"}}
    annotated = {
        "envelope_type": "x",
        "v": 1,
        "_note": "ignore me",
        "integrity": {"hash_algorithm": "SHA-256", "hash_value": "placeholder"},
    }
    assert envelope_hash(base) == envelope_hash(annotated)


def test_verify_and_tamper_detection():
    env = {"envelope_type": "x", "v": 1, "integrity": {}}
    env["integrity"]["hash_value"] = envelope_hash(env)
    assert verify_envelope_hash(env) is True
    env["v"] = 2
    assert verify_envelope_hash(env) is False


def test_example_bundles_verify_clean():
    for path in sorted((REPO_ROOT / "examples").glob("*.json")):
        bundle = json.loads(path.read_text(encoding="utf-8"))
        findings = verify_bundle(bundle)
        assert findings == [], f"{path.name}: {findings}"


if __name__ == "__main__":  # allow running without pytest
    import traceback

    failures = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn()
                print(f"PASS {name}")
            except Exception:  # noqa: BLE001
                failures += 1
                print(f"FAIL {name}")
                traceback.print_exc()
    raise SystemExit(1 if failures else 0)
