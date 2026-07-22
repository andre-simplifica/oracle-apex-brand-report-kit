"""Shared, dependency-light helpers for the report-kit scripts."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

SKILL_VERSION = "0.1.0"
RUNTIME_VERSION = "0.1.0"
SCHEMA_VERSION = "1.0"


def skill_root() -> Path:
    return Path(__file__).resolve().parents[1]


def repository_root() -> Path:
    current = skill_root()
    for candidate in (current, *current.parents):
        if (candidate / "schemas" / "report-profile.schema.json").is_file():
            return candidate
    return current


def schema_path(name: str) -> Path:
    bundled = skill_root() / "assets" / "schemas" / name
    if bundled.is_file():
        return bundled
    path = repository_root() / "schemas" / name
    if not path.is_file():
        raise FileNotFoundError(f"Schema not found: {name}")
    return path


def load_structured(path: Path) -> Any:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        return json.loads(text)
    try:
        import yaml
    except ImportError as exc:
        raise RuntimeError("PyYAML 6.0.2 is required for YAML configuration") from exc
    return yaml.safe_load(text)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_instance(instance: Any, schema_name: str) -> None:
    try:
        import jsonschema
    except ImportError as exc:
        raise RuntimeError("jsonschema 4.25.1 is required for schema validation") from exc
    schema = load_json(schema_path(schema_name))
    validator = jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker())
    errors = sorted(validator.iter_errors(instance), key=lambda err: tuple(str(p) for p in err.path))
    if errors:
        details = []
        for error in errors:
            location = ".".join(str(part) for part in error.absolute_path) or "$"
            details.append(f"{location}: {error.message}")
        raise ValueError("Schema validation failed:\n- " + "\n- ".join(details))


def sha256_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def render_template(path: Path, values: dict[str, str]) -> str:
    rendered = path.read_text(encoding="utf-8")
    for key, value in values.items():
        rendered = rendered.replace("{{" + key + "}}", value)
    unresolved = sorted(set(re.findall(r"\{\{([A-Z][A-Z0-9_]*)\}\}", rendered)))
    if unresolved:
        raise ValueError(f"Unresolved template values in {path.name}: {', '.join(unresolved)}")
    return rendered


def safe_relative(path: str) -> Path:
    candidate = Path(path)
    if candidate.is_absolute() or ".." in candidate.parts or not candidate.parts:
        raise ValueError(f"Unsafe relative path: {path}")
    return candidate
