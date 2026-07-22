#!/usr/bin/env python3
"""Scan text files for credentials, private endpoints, and production-like markers."""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

SKIP_DIRS = {".git", ".venv", "__pycache__", ".pytest_cache", "dist"}
TEXT_SUFFIXES = {"", ".md", ".txt", ".py", ".json", ".yaml", ".yml", ".sql", ".pks", ".pkb", ".js", ".css", ".html", ".xml", ".toml"}
PATTERNS = {
    "private IPv4 URL": re.compile(r"https?://(?:10(?:\.\d{1,3}){3}|192\.168(?:\.\d{1,3}){2}|172\.(?:1[6-9]|2\d|3[01])(?:\.\d{1,3}){2})", re.I),
    "private hostname": re.compile(r"https?://[^\s/'\"]+\.(?:internal|local|corp)(?:[/:\s'\"]|$)", re.I),
    "GitHub token": re.compile(r"\b(?:ghp|github_pat)_[A-Za-z0-9_]{20,}\b"),
    "AWS access key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "secret assignment": re.compile(r"(?i)\b(?:password|passwd|secret|api[_-]?key|access[_-]?token)\s*[:=]\s*['\"](?!\{\{|<|example|synthetic|not-a-secret)[^'\"]{8,}['\"]"),
    "Oracle wallet": re.compile(r"(?i)\b(?:cwallet\.sso|ewallet\.p12)\b"),
}


def iter_text_files(root: Path):
    if root.is_file():
        yield root
        return
    for current, dirs, files in os.walk(root):
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS)
        for name in sorted(files):
            path = Path(current) / name
            if path.suffix.lower() in TEXT_SUFFIXES and path.stat().st_size <= 2_000_000:
                yield path


def scan(root: Path) -> list[str]:
    findings = []
    for path in iter_text_files(root):
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for line_number, line in enumerate(text.splitlines(), start=1):
            for label, pattern in PATTERNS.items():
                if pattern.search(line):
                    findings.append(f"{path}:{line_number}: {label}")
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", default=".", type=Path)
    args = parser.parse_args()
    findings = scan(args.path.resolve())
    if findings:
        print("Sensitive-data scan failed:", file=sys.stderr)
        print("\n".join(f"- {item}" for item in findings), file=sys.stderr)
        return 1
    print(f"OK: no sensitive-data patterns found under {args.path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
