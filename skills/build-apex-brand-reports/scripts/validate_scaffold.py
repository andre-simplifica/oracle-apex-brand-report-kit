#!/usr/bin/env python3
"""Validate a generated consumer scaffold and its ownership manifest."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from _kit import load_json, safe_relative, sha256_file, validate_instance
from validate_sensitive_data import scan


def validate_scaffold(root: Path) -> list[str]:
    errors: list[str] = []
    manifest_path = root / ".apex-brand-report-kit" / "installation-manifest.json"
    if not manifest_path.is_file():
        return [f"Missing manifest: {manifest_path}"]
    try:
        manifest = load_json(manifest_path)
        validate_instance(manifest, "installation-manifest.schema.json")
    except (OSError, RuntimeError, ValueError) as exc:
        return [str(exc)]

    for owner in ("engine", "theme"):
        for entry in manifest["managed_files"][owner]:
            path = root / safe_relative(entry["path"])
            if not path.is_file():
                errors.append(f"Missing {owner}-managed file: {entry['path']}")
            elif sha256_file(path) != entry["sha256"]:
                errors.append(f"Checksum mismatch: {entry['path']}")

    for relative in manifest["project_files"]:
        if not (root / safe_relative(relative)).is_file():
            errors.append(f"Missing project-owned file: {relative}")

    placeholder = re.compile(r"\{\{[A-Z0-9_]+\}\}")
    for path in root.rglob("*"):
        if path.is_file() and path.suffix.lower() in {".sql", ".pks", ".pkb", ".md", ".js", ".css", ".json", ".yaml", ".yml"}:
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            if placeholder.search(text):
                errors.append(f"Unresolved placeholder: {path.relative_to(root)}")

    for entry in manifest["managed_files"]["engine"]:
        path = root / safe_relative(entry["path"])
        if path.suffix.lower() in {".pks", ".pkb"} and path.is_file():
            text = path.read_text(encoding="utf-8").lower()
            if re.search(r"\b(select|insert|update|delete|merge)\b", text):
                errors.append(f"Business SQL found in engine-managed file: {entry['path']}")

    errors.extend(scan(root))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", type=Path)
    args = parser.parse_args()
    errors = validate_scaffold(args.target.resolve())
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"OK: valid scaffold: {args.target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
