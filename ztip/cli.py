"""``ztip`` command-line interface.

    ztip hash <file>     Print the SHA-256 (RFC 8785) hash of each envelope.
    ztip verify <file>   Recompute hashes and check references; fail-closed on any defect.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from .chain import verify_bundle
from .hashing import envelope_hash


def _load(path: str) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _envelopes(doc: Any) -> list:
    if isinstance(doc, dict) and isinstance(doc.get("envelopes"), list):
        return doc["envelopes"]
    if isinstance(doc, list):
        return doc
    return [doc]


def cmd_hash(args: argparse.Namespace) -> int:
    for index, env in enumerate(_envelopes(_load(args.file))):
        print(f"{envelope_hash(env)}  [{index}] {env.get('envelope_type', '?')}")
    return 0


def cmd_verify(args: argparse.Namespace) -> int:
    findings = verify_bundle(_load(args.file))
    if not findings:
        print(f"OK  {args.file}: integrity verified — hashes recomputable, references intact")
        return 0
    print(f"FAIL  {args.file}: {len(findings)} integrity finding(s)")
    for finding in findings:
        print(f"  - [{finding['envelope_index']}] {finding['envelope_type']}: "
              f"{finding['code']} — {finding['detail']}")
    return 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="ztip", description="ZTIP reference runtime")
    sub = parser.add_subparsers(dest="command", required=True)

    p_hash = sub.add_parser("hash", help="print the hash of each envelope in a file")
    p_hash.add_argument("file")
    p_hash.set_defaults(func=cmd_hash)

    p_verify = sub.add_parser("verify", help="verify bundle integrity (fail-closed)")
    p_verify.add_argument("file")
    p_verify.set_defaults(func=cmd_verify)

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
