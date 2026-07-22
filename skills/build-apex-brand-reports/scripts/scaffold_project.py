#!/usr/bin/env python3
"""Deterministically scaffold or update an Oracle APEX report-kit consumer."""

from __future__ import annotations

import argparse
import difflib
import html as html_lib
import json
import os
import re
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from _kit import (
    RUNTIME_VERSION,
    SCHEMA_VERSION,
    SKILL_VERSION,
    load_json,
    load_structured,
    render_template,
    safe_relative,
    schema_path,
    sha256_bytes,
    sha256_file,
    skill_root,
    validate_instance,
)
from validate_sensitive_data import scan
from validate_theme import validate_theme

MANIFEST_PATH = Path(".apex-brand-report-kit/installation-manifest.json")


def sql_literal(value: str) -> str:
    return value.replace("'", "''")


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def css_value(value: Any, fallback: str) -> str:
    """Return a bounded single CSS value, rejecting rule/style injection."""
    text = str(value if value is not None else fallback).strip()
    if not text:
        return fallback
    lowered = text.lower()
    if len(text) > 500 or any(char in text for char in "{};\r\n") or "</style" in lowered:
        raise ValueError(f"Unsafe CSS token value: {text[:80]!r}")
    return text


def css_font_stack(profile: dict[str, Any]) -> str:
    typography = profile["typography"]
    names = [typography["families"].get("body", "system-ui"), *typography["fallbacks"]]
    result: list[str] = []
    for name in names:
        name = str(name).strip()
        if not re.fullmatch(r"[A-Za-z0-9 _-]+", name):
            raise ValueError(f"Unsafe font family: {name!r}")
        result.append(f'"{name}"' if " " in name else name)
    return ",".join(dict.fromkeys(result))


def parse_timestamp(value: str | None) -> str:
    if value is None:
        return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    datetime.fromisoformat(value.replace("Z", "+00:00"))
    return value


def load_inputs(config_path: Path) -> tuple[dict[str, Any], dict[str, Any], Path]:
    config = load_structured(config_path)
    validate_instance(config, "report-profile.schema.json")
    profile_path = Path(config["theme"]["profile"])
    if not profile_path.is_absolute():
        profile_path = (config_path.parent / profile_path).resolve()
    profile = load_structured(profile_path)
    validate_instance(profile, "brand-profile.schema.json")
    theme_errors = validate_theme(profile_path)
    if theme_errors:
        raise ValueError("Theme validation failed:\n- " + "\n- ".join(theme_errors))
    if (config["features"]["xlsx"] or config["features"]["csv"]) and not config["packages"].get("export_process"):
        raise ValueError("packages.export_process is required when XLSX or CSV is enabled")
    findings = scan(config_path) + scan(profile_path)
    if findings:
        raise ValueError("Sensitive-data patterns found in input:\n- " + "\n- ".join(findings))
    return config, profile, profile_path


def token_values(config: dict[str, Any], profile: dict[str, Any]) -> dict[str, str]:
    packages = config["packages"]
    apex = config["apex"]
    theme = config["theme"]
    document = config["document"]
    features = config["features"]
    semantic = profile["colors"]["semantic"]
    screen = profile["colors"]["screen"]
    layout = profile["layout"]
    components = profile["components"]
    component_token = lambda component, token, fallback: components[component]["tokens"].get(token, fallback)
    required_colors = ("primary", "primary_text", "surface", "text", "muted", "border", "success", "warning", "danger", "danger_text")
    missing = [name for name in required_colors if name not in semantic]
    if missing:
        raise ValueError("Brand profile is missing semantic colors: " + ", ".join(missing))
    export_process = packages.get("export_process")
    enabled_exports = [name.upper() for name in ("xlsx", "csv") if features[name]]
    export_status = ", ".join(enabled_exports) + " enabled" if enabled_exports else "XLSX and CSV disabled"
    export_block = (
        f"begin\n    {export_process.upper()};\nend;"
        if export_process and enabled_exports
        else "-- No export page process is required while XLSX and CSV are disabled."
    )
    theme_name_html = html_lib.escape(profile["theme"]["name"], quote=True)
    return {
        "ENGINE_PACKAGE": packages["engine"].upper(),
        "THEME_PACKAGE": packages["theme"].upper(),
        "OWNER_PACKAGE": packages["owner"].upper(),
        "REPORT_FUNCTION": packages["report_function"].upper(),
        "EXPORT_PROCESS": (export_process or "disabled").upper(),
        "EXPORT_STATUS": export_status,
        "EXPORT_PROCESS_BLOCK": export_block,
        "APPLICATION_ID": str(apex["application_id"]),
        "MODAL_PAGE_ID": str(apex["modal_page_id"]),
        "AUTHORIZATION_SCHEME": apex["authorization_scheme"],
        "ITEMS_TO_SUBMIT": ",".join(apex.get("items_to_submit", [])) or "(none)",
        "THEME_ID": theme["id"],
        "THEME_NAME": sql_literal(theme_name_html),
        "THEME_VERSION": theme["version"],
        "HEADER_VARIANT": theme["header"]["variant"],
        "HEADER_SIZE": theme["header"]["size"],
        "SHOW_LOGO": "Y" if theme["header"]["show_logo"] else "N",
        "FOOTER_VARIANT": theme["footer"]["variant"],
        "DENSITY": theme["density"],
        "ORIENTATION": document["orientation"],
        "TOOLBAR": document["toolbar"],
        "TOOLBAR_POSITION": document["toolbar_position"],
        "CONTENT_WIDTH": document["content_width"],
        "ECONOMY_PRINT": "Y" if document["economy_print"] else "N",
        "ECONOMY_PRINT_BOOL": bool_text(document["economy_print"]),
        "REPEAT_TABLE_HEADER_BOOL": bool_text(document["repeat_table_header"]),
        "SHOW_EMISSION_USER": "Y" if document["show_emission_user"] else "N",
        "SHOW_EMISSION_DATETIME": "Y" if document["show_emission_datetime"] else "N",
        "FEATURE_FULLSCREEN": bool_text(features["fullscreen"]),
        "FEATURE_PRINT": bool_text(features["print"]),
        "FEATURE_PDF": bool_text(features["pdf"]),
        "FEATURE_XLSX": bool_text(features["xlsx"]),
        "FEATURE_CSV": bool_text(features["csv"]),
        "LOCALE": config["locale"]["language"],
        "TIMEZONE": config["locale"]["timezone"],
        "COLOR_PRIMARY": semantic["primary"],
        "COLOR_PRIMARY_TEXT": semantic["primary_text"],
        "COLOR_SURFACE": semantic["surface"],
        "COLOR_TEXT": semantic["text"],
        "COLOR_MUTED": semantic["muted"],
        "COLOR_BORDER": semantic["border"],
        "COLOR_SUCCESS": semantic["success"],
        "COLOR_WARNING": semantic["warning"],
        "COLOR_DANGER": semantic["danger"],
        "COLOR_DANGER_TEXT": semantic["danger_text"],
        "COLOR_PAGE": css_value(screen.get("page"), semantic["surface"]),
        "COLOR_FOCUS": css_value(screen.get("focus"), semantic["primary"]),
        "FONT_FAMILY": css_font_stack(profile),
        "HEADER_BACKGROUND": css_value(component_token("header", "background", screen.get("page", semantic["surface"])), semantic["surface"]),
        "HERO_BACKGROUND": css_value(component_token("hero", "background", layout["gradients"].get("hero", semantic["primary"])), semantic["primary"]),
        "SOFT_BACKGROUND": css_value(layout["backgrounds"].get("soft", screen.get("soft", screen.get("page", semantic["surface"]))), semantic["surface"]),
        "TABLE_HEADER_BACKGROUND": css_value(component_token("tables", "header_background", semantic["surface"]), semantic["surface"]),
        "BRAND_BAND_BACKGROUND": css_value(component_token("brand_band", "background", semantic["primary"]), semantic["primary"]),
        "CARD_RADIUS": css_value(component_token("cards", "radius", layout["radii"].get("card", "14px")), "14px"),
        "CONTROL_RADIUS": css_value(component_token("buttons", "radius", layout["radii"].get("control", "8px")), "8px"),
        "HERO_RADIUS": css_value(layout["radii"].get("hero", "16px"), "16px"),
        "CARD_SHADOW": css_value(layout["shadows"].get("card", "none"), "none"),
    }


def build_files(config: dict[str, Any], profile: dict[str, Any]) -> dict[str, dict[Path, bytes]]:
    values = token_values(config, profile)
    assets = skill_root() / "assets"
    database = safe_relative(config["directories"]["database"])
    web = safe_relative(config["directories"]["web"])
    docs = safe_relative(config["directories"]["documentation"])
    engine_name = config["packages"]["engine"].lower()
    theme_name = config["packages"]["theme"].lower()
    page_id = config["apex"]["modal_page_id"]

    def rendered(relative: str) -> bytes:
        return render_template(assets / relative, values).encode("utf-8")

    engine = {
        database / f"{engine_name}.pks": rendered("runtime/plsql/report_engine.pks.tpl"),
        database / f"{engine_name}.pkb": rendered("runtime/plsql/report_engine.pkb.tpl"),
        web / "report-kit.css": rendered("runtime/web/report-kit.css.tpl"),
        web / "report-kit.js": rendered("runtime/web/report-kit.js.tpl"),
    }
    theme = {
        database / f"{theme_name}.pks": rendered("theme-template/report_theme.pks.tpl"),
        database / f"{theme_name}.pkb": rendered("theme-template/report_theme.pkb.tpl"),
        web / "report-theme.css": rendered("theme-template/report-theme.css.tpl"),
        web / "brand-profile.json": (json.dumps(profile, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8"),
    }
    project = {
        docs / f"apex-modal-page-{page_id}.md": rendered("apex-modal-blueprint/page-designer.md.tpl"),
        docs / "report-function-example.sql": rendered("report-template/report-function.sql.tpl"),
        docs / "server-side-export.md": rendered("report-template/server-side-export.md.tpl"),
    }
    return {"engine": engine, "theme": theme, "project": project}


def file_entries(files: dict[Path, bytes]) -> list[dict[str, str]]:
    return [{"path": path.as_posix(), "sha256": sha256_bytes(content)} for path, content in sorted(files.items())]


def compatibility() -> dict[str, dict[str, str]]:
    return {
        "oracle_database": {
            "status": "expected-not-tested",
            "version": "Oracle Database 26ai",
            "evidence": "Repository-only PL/SQL templates; compilation is intentionally not performed by the scaffold.",
        },
        "oracle_apex": {
            "status": "expected-not-tested",
            "version": "Oracle APEX 24.2",
            "evidence": "API pattern validated statically; consumer must confirm installed signatures and run DEV compilation.",
        },
    }


def new_manifest(config: dict[str, Any], files: dict[str, dict[Path, bytes]], installed_at: str) -> dict[str, Any]:
    return {
        "manifest_version": "1.0",
        "skill_version": SKILL_VERSION,
        "runtime_version": RUNTIME_VERSION,
        "schema_versions": {"brand": SCHEMA_VERSION, "report": SCHEMA_VERSION, "manifest": SCHEMA_VERSION},
        "theme": {"id": config["theme"]["id"], "version": config["theme"]["version"]},
        "installed_at": installed_at,
        "managed_files": {"engine": file_entries(files["engine"]), "theme": file_entries(files["theme"])},
        "project_files": [path.as_posix() for path in sorted(files["project"])],
        "features": dict(config["features"]),
        "compatibility": compatibility(),
    }


def updated_manifest(existing: dict[str, Any], config: dict[str, Any], engine: dict[Path, bytes]) -> dict[str, Any]:
    result = json.loads(json.dumps(existing))
    result["skill_version"] = SKILL_VERSION
    result["runtime_version"] = RUNTIME_VERSION
    result["managed_files"]["engine"] = file_entries(engine)
    result["features"] = dict(config["features"])
    result["compatibility"] = compatibility()
    return result


def manifest_bytes(manifest: dict[str, Any]) -> bytes:
    validate_instance(manifest, "installation-manifest.schema.json")
    return (json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def manifest_checksums(manifest: dict[str, Any], owner: str) -> dict[Path, str]:
    return {safe_relative(item["path"]): item["sha256"] for item in manifest["managed_files"][owner]}


def display_change(target: Path, relative: Path, content: bytes) -> None:
    path = target / relative
    if not path.exists():
        print(f"CREATE {relative.as_posix()}")
        return
    current = path.read_bytes()
    if current == content:
        print(f"UNCHANGED {relative.as_posix()}")
        return
    print(f"UPDATE {relative.as_posix()}")
    try:
        old_text = current.decode("utf-8").splitlines(keepends=True)
        new_text = content.decode("utf-8").splitlines(keepends=True)
    except UnicodeDecodeError:
        print("  binary content differs")
        return
    diff = difflib.unified_diff(old_text, new_text, fromfile=f"a/{relative}", tofile=f"b/{relative}", n=2)
    for line in list(diff)[:120]:
        print(line, end="")


def atomic_write(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    except BaseException:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass
        raise


def validate_target(target: Path) -> None:
    if target == Path(target.anchor) or target == Path.home().resolve():
        raise ValueError(f"Refusing broad target: {target}")
    if target.exists() and not target.is_dir():
        raise ValueError(f"Target is not a directory: {target}")


def execute(args: argparse.Namespace) -> int:
    config_path = args.config.resolve()
    target = args.target.resolve()
    validate_target(target)
    config, profile, _ = load_inputs(config_path)
    if args.platform != config["platform"]:
        raise ValueError(f"Platform mismatch: CLI={args.platform}, config={config['platform']}")
    files = build_files(config, profile)
    manifest_path = target / MANIFEST_PATH

    if args.update:
        if not manifest_path.is_file():
            raise ValueError("Cannot update: installation manifest does not exist")
        existing = load_json(manifest_path)
        validate_instance(existing, "installation-manifest.schema.json")
        recorded = manifest_checksums(existing, "engine")
        conflicts = []
        for relative, content in files["engine"].items():
            path = target / relative
            if path.exists() and relative in recorded and sha256_file(path) != recorded[relative] and path.read_bytes() != content:
                conflicts.append(relative.as_posix())
            if path.exists() and relative not in recorded and path.read_bytes() != content:
                conflicts.append(relative.as_posix())
        if conflicts and not args.force:
            raise ValueError("Engine conflicts detected; review or rerun with --force:\n- " + "\n- ".join(conflicts))
        manifest = updated_manifest(existing, config, files["engine"])
        planned = dict(files["engine"])
    else:
        if manifest_path.exists():
            raise ValueError("Installation manifest already exists; use --update")
        planned = {**files["engine"], **files["theme"], **files["project"]}
        existing_paths = [relative.as_posix() for relative in planned if (target / relative).exists()]
        if existing_paths and not args.force:
            raise ValueError("Files already exist; use --force only after review:\n- " + "\n- ".join(existing_paths))
        manifest = new_manifest(config, files, parse_timestamp(args.installed_at))

    planned[MANIFEST_PATH] = manifest_bytes(manifest)
    for relative, content in sorted(planned.items()):
        display_change(target, relative, content)
    if args.dry_run:
        print(f"DRY-RUN: {len(planned)} file(s); no files written")
        return 0

    target.mkdir(parents=True, exist_ok=True)
    for relative, content in sorted(planned.items(), key=lambda item: item[0] == MANIFEST_PATH):
        atomic_write(target / relative, content)
    print(f"OK: wrote {len(planned)} file(s) to {target}")
    return 0


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--target", required=True, type=Path)
    result.add_argument("--config", required=True, type=Path)
    result.add_argument("--platform", default="apex", choices=("apex",))
    result.add_argument("--dry-run", action="store_true")
    result.add_argument("--force", action="store_true")
    result.add_argument("--update", action="store_true")
    result.add_argument("--installed-at", help="ISO-8601 timestamp; useful for deterministic tests")
    return result


def main() -> int:
    try:
        return execute(parser().parse_args())
    except (OSError, RuntimeError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
