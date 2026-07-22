#!/usr/bin/env python3
"""Create a deterministic, installable ZIP for the skill."""

from __future__ import annotations

import argparse
import sys
import zipfile
from pathlib import Path

from _kit import SKILL_VERSION, skill_root

EXCLUDED = {"__pycache__", ".DS_Store"}


def package(destination: Path) -> Path:
    source = skill_root()
    destination.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in sorted(source.rglob("*")):
            if not path.is_file() or any(part in EXCLUDED for part in path.parts) or path.suffix == ".pyc":
                continue
            relative = Path(source.name) / path.relative_to(source)
            info = zipfile.ZipInfo(relative.as_posix(), date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = (0o755 if path.suffix == ".py" else 0o644) << 16
            archive.writestr(info, path.read_bytes())
    return destination


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("dist") / f"build-apex-brand-reports-{SKILL_VERSION}.zip")
    args = parser.parse_args()
    try:
        output = package(args.output.resolve())
    except OSError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(f"OK: packaged skill: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
