#!/usr/bin/env python3
"""Validate a brand profile and essential accessibility properties."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from _kit import load_structured, validate_instance


def channel(value: str) -> float:
    normalized = int(value, 16) / 255
    return normalized / 12.92 if normalized <= 0.04045 else ((normalized + 0.055) / 1.055) ** 2.4


def luminance(color: str) -> float:
    color = color.lstrip("#")[:6]
    return 0.2126 * channel(color[0:2]) + 0.7152 * channel(color[2:4]) + 0.0722 * channel(color[4:6])


def contrast(a: str, b: str) -> float:
    light, dark = sorted((luminance(a), luminance(b)), reverse=True)
    return (light + 0.05) / (dark + 0.05)


def validate_theme(path: Path) -> list[str]:
    profile = load_structured(path)
    validate_instance(profile, "brand-profile.schema.json")
    minimum = float(profile["accessibility"]["minimum_contrast"])
    semantic = profile["colors"]["semantic"]
    checks = (("text", "surface"), ("primary_text", "primary"), ("danger_text", "danger"))
    errors = []
    for foreground, background in checks:
        if foreground in semantic and background in semantic:
            ratio = contrast(semantic[foreground], semantic[background])
            if ratio + 0.001 < minimum:
                errors.append(f"Contrast {foreground}/{background} is {ratio:.2f}:1; expected at least {minimum:.2f}:1")
    screen = profile["colors"]["screen"]
    if "focus" in screen:
        for background in ("surface", "page"):
            if background in screen:
                ratio = contrast(screen["focus"], screen[background])
                if ratio + 0.001 < 3.0:
                    errors.append(f"Contrast focus/{background} is {ratio:.2f}:1; expected at least 3.00:1")
    if not profile["accessibility"]["focus_visible"]:
        errors.append("focus_visible must be enabled")
    if not profile["accessibility"]["keyboard"]:
        errors.append("keyboard accessibility must be enabled")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("profile", type=Path)
    args = parser.parse_args()
    try:
        errors = validate_theme(args.profile.resolve())
    except (OSError, RuntimeError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"OK: valid brand profile: {args.profile}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
