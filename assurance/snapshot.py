"""Fetch evidence files from the source repositories at their pinned commits, and record their hashes.

    python -m assurance.snapshot           # download every file in evidence/sources.json (needs network)
    python -m assurance.snapshot --check   # verify the committed snapshots against evidence/manifest.json

Evidence is copied into the repository (evidence/snapshots/), so the assurance case can be
checked offline and deterministically in CI. Each file is fetched from the exact commit of
the release that Zenodo archived, never from a moving branch, and its SHA-256 is recorded:
if a snapshot is edited by hand, the check fails.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EVIDENCE = ROOT / "evidence"
SNAPSHOTS = EVIDENCE / "snapshots"
MANIFEST = EVIDENCE / "manifest.json"
RAW = "https://raw.githubusercontent.com/K11-Software-Solutions/{repo}/{commit}/{path}"


def sources() -> dict:
    return json.loads((EVIDENCE / "sources.json").read_text(encoding="utf-8"))


def snapshot_path(repo: str, path: str) -> Path:
    return SNAPSHOTS / repo / path


def sha256(data: bytes) -> str:
    return hashlib.sha256(data.replace(b"\r\n", b"\n")).hexdigest()       # line endings must not matter


def fetch() -> dict:
    manifest = {}
    for lab, s in sources().items():
        for path in s["files"]:
            url = RAW.format(repo=s["repo"], commit=s["commit"], path=path)
            with urllib.request.urlopen(url, timeout=30) as r:
                data = r.read()
            target = snapshot_path(s["repo"], path)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
            manifest[f"{s['repo']}/{path}"] = {"commit": s["commit"], "sha256": sha256(data), "url": url}
            print(f"fetched {s['repo']}@{s['commit'][:7]}/{path}")
    MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest


def check() -> list[str]:
    """Every source file has a snapshot, and every snapshot matches its recorded hash and commit."""
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    problems = []
    for lab, s in sources().items():
        for path in s["files"]:
            key = f"{s['repo']}/{path}"
            entry = manifest.get(key)
            p = snapshot_path(s["repo"], path)
            if entry is None or not p.is_file():
                problems.append(f"snapshot missing: {key}")
            elif entry["commit"] != s["commit"]:
                problems.append(f"snapshot of {key} is from {entry['commit'][:7]}, sources pin {s['commit'][:7]}")
            elif sha256(p.read_bytes()) != entry["sha256"]:
                problems.append(f"snapshot of {key} does not match its recorded hash (edited after fetching?)")
    return problems


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)
    if args.check:
        problems = check()
        print("\n".join(problems) or "all snapshots match their pinned commits and hashes")
        return 1 if problems else 0
    fetch()
    return 0


if __name__ == "__main__":
    sys.exit(main())
