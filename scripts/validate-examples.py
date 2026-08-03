#!/usr/bin/env python3
"""Validate examples/*.json against schemas/ztip-bundle.schema.json."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


def format_error_path(error: Any) -> str:
    if not error.absolute_path:
        return "$"
    path = "$"
    for part in error.absolute_path:
        if isinstance(part, int):
            path += f"[{part}]"
        else:
            path += f".{part}"
    return path


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def main() -> int:
    try:
        import jsonschema
        from jsonschema import Draft202012Validator
    except ImportError:
        print(
            "ERROR: Missing dependency 'jsonschema'. Install dev dependencies with:"
            " pip install -r requirements-dev.txt"
        )
        return 1

    repo_root = Path(__file__).resolve().parents[1]
    schemas_dir = repo_root / "schemas"
    examples_dir = repo_root / "examples"
    bundle_schema_path = schemas_dir / "ztip-bundle.schema.json"

    if not bundle_schema_path.exists():
        print(f"ERROR: Schema not found: {bundle_schema_path}")
        return 1

    schema_store: dict[str, Any] = {}
    for schema_path in sorted(schemas_dir.glob("*.schema.json")):
        schema_doc = load_json(schema_path)
        schema_store[schema_path.as_uri()] = schema_doc
        schema_store[schema_path.name] = schema_doc
        schema_id = schema_doc.get("$id")
        if isinstance(schema_id, str) and schema_id:
            schema_store[schema_id] = schema_doc
            if not schema_id.startswith(("http://", "https://", "file://")):
                schema_store[(schemas_dir / schema_id).as_uri()] = schema_doc

    bundle_schema = load_json(bundle_schema_path)
    resolver = jsonschema.RefResolver(
        base_uri=bundle_schema_path.as_uri(),
        referrer=bundle_schema,
        store=schema_store,
    )

    Draft202012Validator.check_schema(bundle_schema)
    validator = Draft202012Validator(bundle_schema, resolver=resolver)

    failures = 0
    example_files = sorted(examples_dir.glob("*.json"))

    if not example_files:
        print(f"ERROR: No example files found in {examples_dir}")
        return 1

    for example_path in example_files:
        try:
            raw_doc = load_json(example_path)
        except json.JSONDecodeError as exc:
            print(f"FAIL {example_path.name}")
            print(f"  - JSON parse error at line {exc.lineno}, column {exc.colno}: {exc.msg}")
            failures += 1
            continue

        instance = raw_doc.get("envelopes", raw_doc) if isinstance(raw_doc, dict) else raw_doc
        errors = sorted(validator.iter_errors(instance), key=lambda e: list(e.absolute_path))

        if errors:
            failures += 1
            print(f"FAIL {example_path.name}")
            for err in errors[:10]:
                print(f"  - {format_error_path(err)}: {err.message}")
            if len(errors) > 10:
                print(f"  - ... {len(errors) - 10} additional validation errors")
        else:
            print(f"PASS {example_path.name}")

    if failures:
        print(f"\nValidation completed with {failures} failing example file(s).")
        return 1

    print(f"\nValidation completed successfully: {len(example_files)} example file(s) passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
