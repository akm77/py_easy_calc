#!/usr/bin/env python3
"""Generate simple release notes from the commit history."""

from __future__ import annotations

import argparse
import datetime
import subprocess
from pathlib import Path
from typing import Iterable, Optional


def run_git_command(args: list[str]) -> str:
    return subprocess.run(
        ["git", *args],
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()


def get_most_recent_tag() -> Optional[str]:
    try:
        return run_git_command(["describe", "--tags", "--abbrev=0"])
    except subprocess.CalledProcessError:
        return None


def collect_commits(base_ref: Optional[str]) -> Iterable[str]:
    if base_ref:
        rev_range = f"{base_ref}..HEAD"
    else:
        rev_range = "HEAD"

    try:
        log = run_git_command(["log", rev_range, "--pretty=format:%h %s"]).splitlines()
    except subprocess.CalledProcessError:
        log = []
    return log


def build_release_notes(version: str, base_ref: Optional[str], commits: Iterable[str]) -> str:
    header = f"# {version} — {datetime.date.today():%Y-%m-%d}\n\n"
    if base_ref:
        header += f"Changes since `{base_ref}`:\n\n"
    else:
        header += "Changes since first commit:\n\n"

    if not commits:
        header += "- No new commits since the previous release.\n"
        return header

    bullet_list = "".join(f"- {commit}\n" for commit in commits)
    return header + bullet_list


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate release notes from git commits.")
    parser.add_argument("--version", required=True, help="Release version (used for the header).")
    parser.add_argument(
        "--since",
        help="Git reference (tag or commit) to compute the range; by default the most recent tag is used.",
    )
    parser.add_argument("--output", help="Path to write the release notes (printed to stdout if omitted).")

    args = parser.parse_args()

    since_ref = args.since or get_most_recent_tag()
    commits = list(collect_commits(since_ref))
    notes = build_release_notes(args.version, since_ref, commits)

    if args.output:
        Path(args.output).write_text(notes, encoding="utf-8")
        print(f"Release notes written to {args.output}")
    else:
        print(notes)


if __name__ == "__main__":
    main()
