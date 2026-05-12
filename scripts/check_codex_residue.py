#!/usr/bin/env python3
"""Lint: Codex fork must not carry legacy provider residue."""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path


TEXT_EXTENSIONS = {
    ".cfg",
    ".css",
    ".csv",
    ".html",
    ".ini",
    ".json",
    ".jsonl",
    ".md",
    ".py",
    ".sh",
    ".toml",
    ".txt",
    ".yaml",
    ".yml",
}

SKIP_DIRS = {
    ".git",
    ".pytest_cache",
    "__pycache__",
    "node_modules",
}


def _legacy_terms() -> dict[str, re.Pattern[str]]:
    provider = "cl" + "aude"
    vendor = "anth" + "ropic"
    model_a = "op" + "us"
    model_b = "son" + "net"
    model_c = "hai" + "ku"
    return {
        "legacy provider name": re.compile(re.escape(provider), re.IGNORECASE),
        "legacy vendor name": re.compile(re.escape(vendor), re.IGNORECASE),
        "legacy provider model": re.compile(
            rf"\b(?:{model_a}|{model_b}|{model_c})\b",
            re.IGNORECASE,
        ),
    }


def _iter_files(root: Path):
    try:
        result = subprocess.run(
            ["git", "-C", str(root), "ls-files"],
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        for path in root.rglob("*"):
            if any(part in SKIP_DIRS for part in path.parts):
                continue
            if path.is_file():
                yield path
        return

    for rel in result.stdout.splitlines():
        path = root / rel
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.is_file():
            yield path


def _is_text_file(path: Path) -> bool:
    return path.suffix.lower() in TEXT_EXTENSIONS or path.name in {
        ".gitignore",
        "LICENSE",
        "NOTICE.md",
    }


def check(root: Path) -> list[str]:
    errors: list[str] = []
    terms = _legacy_terms()

    for path in _iter_files(root):
        rel = path.relative_to(root).as_posix()
        for label, pattern in terms.items():
            if pattern.search(rel):
                errors.append(f"{rel}: path contains {label}")

        if not _is_text_file(path):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue

        for line_no, line in enumerate(text.splitlines(), start=1):
            for label, pattern in terms.items():
                if pattern.search(line):
                    errors.append(f"{rel}:{line_no}: contains {label}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--root",
        default=".",
        help="Repository root to scan",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    errors = check(root)
    if errors:
        print("Codex residue check failed:")
        for error in errors:
            print(f"  {error}")
        return 1
    print("Codex residue check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
