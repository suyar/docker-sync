#!/usr/bin/env python3
"""Sync workflow matrix versions from dependabot compose files."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# dependabot/<dir>/docker-compose.yml -> workflow file and style
MAPPINGS = {
    "drone-runner": {"workflow": ".github/workflows/sync-drone-runner.yml", "style": "major_full"},
    "drone-server": {"workflow": ".github/workflows/sync-drone-server.yml", "style": "major_full"},
    "gitea-gitea": {"workflow": ".github/workflows/sync-gitea-gitea.yml", "style": "major_full"},
    "gitea-runner": {"workflow": ".github/workflows/sync-gitea-runner.yml", "style": "full_only"},
    "mysql-8.0": {"workflow": ".github/workflows/sync-mysql.yml", "style": "track_minor_full", "track": "8.0"},
    "mysql-8.4": {"workflow": ".github/workflows/sync-mysql.yml", "style": "track_minor_full", "track": "8.4"},
    "mysql-9": {"workflow": ".github/workflows/sync-mysql.yml", "style": "track_minor_full", "track": "9.6"},
    "nginx-1.28": {"workflow": ".github/workflows/sync-nginx.yml", "style": "minor_full"},
    "redis-6.2": {"workflow": ".github/workflows/sync-redis.yml", "style": "track_major_minor_full", "track": "6.2"},
    "redis-7.2": {"workflow": ".github/workflows/sync-redis.yml", "style": "track_major_minor_full", "track": "7.2"},
    "redis-7.4": {"workflow": ".github/workflows/sync-redis.yml", "style": "track_major_minor_full", "track": "7.4"},
    "redis-8.0": {"workflow": ".github/workflows/sync-redis.yml", "style": "track_major_minor_full", "track": "8.0"},
    "redis-8.2": {"workflow": ".github/workflows/sync-redis.yml", "style": "track_major_minor_full", "track": "8.2"},
    "redis-8.4": {"workflow": ".github/workflows/sync-redis.yml", "style": "track_major_minor_full", "track": "8.4"},
    "redis-8.6": {"workflow": ".github/workflows/sync-redis.yml", "style": "track_major_minor_full", "track": "8.6"},
    "vaultwarden-backup": {"workflow": ".github/workflows/sync-vaultwarden-backup.yml", "style": "full_only"},
    "vaultwarden-server": {"workflow": ".github/workflows/sync-vaultwarden-server.yml", "style": "full_only"},
    "woodpecker-agent": {"workflow": ".github/workflows/sync-woodpecker-agent.yml", "style": "full_only"},
    "woodpecker-server": {"workflow": ".github/workflows/sync-woodpecker-server.yml", "style": "full_only"},
}

MATRIX_BLOCK_RE = re.compile(
    r'(?ms)^(?P<indent>\s*)version:\n(?P<body>(?:\s*\-\s*"[^"]+"\n)+)'
)


def parse_tag_from_compose(compose_file: Path) -> str:
    text = compose_file.read_text(encoding="utf-8")
    match = re.search(r"^\s*image:\s*[^:]+:(\S+)\s*$", text, re.MULTILINE)
    if not match:
        raise ValueError(f"Could not find image tag in {compose_file}")
    return match.group(1)


def split_version(tag: str) -> tuple[str, str]:
    has_v = tag.startswith("v")
    core = tag[1:] if has_v else tag
    parts = core.split(".")
    if len(parts) < 2:
        raise ValueError(f"Tag {tag} is not in expected x.y[.z] format")
    major = parts[0]
    minor = f"{parts[0]}.{parts[1]}"
    if has_v:
        major = f"v{major}"
        minor = f"v{minor}"
    return major, minor


def parse_matrix_versions(workflow_text: str) -> tuple[list[str], re.Match[str]]:
    match = MATRIX_BLOCK_RE.search(workflow_text)
    if not match:
        raise ValueError("Could not find matrix.version block")
    body = match.group("body")
    versions = re.findall(r'\-\s*"([^"]+)"', body)
    return versions, match


def render_block(indent: str, versions: list[str]) -> str:
    lines = [f"{indent}version:\n"]
    item_indent = indent + "  "
    for version in versions:
        lines.append(f"{item_indent}- \"{version}\"\n")
    return "".join(lines)


def replace_exact_entry(versions: list[str], old_value: str, new_value: str) -> None:
    for idx, value in enumerate(versions):
        if value == old_value:
            versions[idx] = new_value
            return
    raise ValueError(f"Could not find expected entry {old_value}")


def replace_full_entry(versions: list[str], old_prefix: str, new_value: str) -> None:
    for idx, value in enumerate(versions):
        if value.startswith(old_prefix + "."):
            versions[idx] = new_value
            return
    raise ValueError(f"Could not find expected full entry for {old_prefix}")


def update_versions(current: list[str], new_tag: str, style: str, track: str | None = None) -> list[str]:
    major, minor = split_version(new_tag)
    versions = list(current)

    if style == "full_only":
        return [new_tag]

    if style == "major_full":
        return [major, new_tag]

    if style == "minor_full":
        return [minor, new_tag]

    if style == "track_minor_full":
        if not track:
            raise ValueError("track is required for track_minor_full")
        replace_exact_entry(versions, track, minor)
        replace_full_entry(versions, track, new_tag)
        return versions

    if style == "track_major_minor_full":
        if not track:
            raise ValueError("track is required for track_major_minor_full")
        track_major = track.split(".")[0]
        replace_exact_entry(versions, track_major, major)
        replace_exact_entry(versions, track, minor)
        replace_full_entry(versions, track, new_tag)
        return versions

    raise ValueError(f"Unknown style: {style}")


def sync_one(compose_rel: str) -> bool:
    compose_path = ROOT / compose_rel
    compose_dir = compose_path.parent.name
    mapping = MAPPINGS.get(compose_dir)
    if not mapping:
        print(f"[SKIP] no mapping for {compose_rel}")
        return False

    new_tag = parse_tag_from_compose(compose_path)
    workflow_path = ROOT / mapping["workflow"]
    workflow_text = workflow_path.read_text(encoding="utf-8")
    current_versions, block_match = parse_matrix_versions(workflow_text)

    updated_versions = update_versions(
        current=current_versions,
        new_tag=new_tag,
        style=mapping["style"],
        track=mapping.get("track"),
    )

    if updated_versions == current_versions:
        print(f"[NOCHANGE] {compose_rel} -> {mapping['workflow']}")
        return False

    new_block = render_block(block_match.group("indent"), updated_versions)
    updated_text = workflow_text[: block_match.start()] + new_block + workflow_text[block_match.end() :]
    workflow_path.write_text(updated_text, encoding="utf-8")
    print(f"[UPDATED] {compose_rel} -> {mapping['workflow']}: {current_versions} -> {updated_versions}")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync sync-*.yml matrix.version from dependabot compose files")
    parser.add_argument(
        "files",
        nargs="*",
        help="Changed files (expecting dependabot/**/docker-compose.yml). If empty, process all mapped files.",
    )
    args = parser.parse_args()

    if args.files:
        targets = [f for f in args.files if f.startswith("dependabot/") and f.endswith("/docker-compose.yml")]
    else:
        targets = [f"dependabot/{name}/docker-compose.yml" for name in MAPPINGS]

    for file_rel in sorted(set(targets)):
        sync_one(file_rel)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
