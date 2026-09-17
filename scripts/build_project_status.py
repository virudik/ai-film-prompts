#!/usr/bin/env python3
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

SLOW_LABEL = "⏳ В МЕДЛЕННОЙ ГЕНЕРАЦИИ"
INSTRUCTION_FILES = (
    "AI-PROJECT-GUIDE.md",
    "SYNC-RUNBOOK.md",
    "USER-GUIDE.md",
    "README-AI-SYNC.md",
    "CLAUDE-TAKEOVER-RUNBOOK.md",
)
PRODUCTION_STATES = {
    "DRAFT",
    "READY",
    "NEEDS_FIX",
    "RESULT_RECEIVED",
    "NEEDS_RERENDER",
    "APPROVED",
    "IN_EDIT",
    "CLOSED",
}
DEPENDENCY_TYPES = {"depends_on", "continues", "alternative_to", "related_to"}
SCENE_META_FIELDS = {
    "target_engine",
    "production_state",
    "duration_s",
    "dialogue",
    "dependencies",
    "tags",
}


def fail(msg):
    print(f"ERROR: {msg}", file=sys.stderr)
    raise SystemExit(1)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def display_date_to_iso(value: str) -> str:
    day, month, year = value.split(".")
    return f"{year}-{month}-{day}"


def normalize_dialogue(value):
    if value is None:
        return {"enabled": None, "language": None}, True
    if not isinstance(value, dict):
        return {"enabled": None, "language": None}, False
    allowed = {"enabled", "language"}
    if set(value) - allowed:
        return {"enabled": None, "language": None}, False
    enabled = value.get("enabled")
    language = value.get("language")
    valid = isinstance(enabled, bool) and (language is None or isinstance(language, str))
    return {"enabled": enabled, "language": language}, valid


def normalize_dependencies(value, active_scene_ids):
    if value is None:
        return [], True, True
    if not isinstance(value, list):
        return [], False, False

    normalized = []
    types_valid = True
    targets_valid = True

    for item in value:
        if not isinstance(item, dict):
            types_valid = False
            targets_valid = False
            continue

        dep_type = item.get("type")
        if dep_type not in DEPENDENCY_TYPES:
            types_valid = False

        has_scene = "scene" in item
        has_targets = "targets" in item
        if has_scene == has_targets:
            targets_valid = False
            continue

        if has_scene:
            target = item.get("scene")
            if not isinstance(target, int) or isinstance(target, bool):
                targets_valid = False
                continue
            targets = [target]
            normalized_item = {"type": dep_type, "scene": target}
        else:
            raw_targets = item.get("targets")
            if (
                not isinstance(raw_targets, list)
                or not raw_targets
                or any(not isinstance(x, int) or isinstance(x, bool) for x in raw_targets)
            ):
                targets_valid = False
                continue
            targets = raw_targets
            normalized_item = {"type": dep_type, "targets": targets}

        if any(target not in active_scene_ids for target in targets):
            targets_valid = False

        normalized.append(normalized_item)

    return normalized, types_valid, targets_valid


def parse_scene_metadata(text, section_scenes, slow_scenes):
    active_scene_ids = set(section_scenes)
    scene_meta = {}

    checks = {
        "scene_meta_json_valid": True,
        "scene_meta_scene_ids_unique": section_scenes == list(dict.fromkeys(section_scenes)),
        "scene_meta_dependency_targets_exist": True,
        "scene_meta_duration_positive": True,
        "scene_meta_production_state_valid": True,
        "scene_meta_dependency_types_valid": True,
        "scene_meta_allowed_fields_valid": True,
        "scene_meta_dialogue_valid": True,
        "scene_meta_tags_valid": True,
        "scene_meta_target_engine_valid": True,
    }

    for scene_id in section_scenes:
        m = re.search(
            rf"^## Сцена {scene_id}\b(.*?)(?=^## Сцена \d+\b|\Z)",
            text,
            re.M | re.S,
        )
        section = m.group(1) if m else ""
        marker_present = re.search(r"<!--\s*scene-meta:", section) is not None
        raw_blocks = re.findall(r"<!--\s*scene-meta:\s*(.*?)\s*-->", section, re.S)

        if marker_present and not raw_blocks:
            checks["scene_meta_json_valid"] = False
        if len(raw_blocks) > 1:
            checks["scene_meta_json_valid"] = False

        raw_meta = None
        if raw_blocks:
            try:
                candidate = json.loads(raw_blocks[0])
                if not isinstance(candidate, dict):
                    raise ValueError("scene-meta must be a JSON object")
                raw_meta = candidate
            except (json.JSONDecodeError, ValueError):
                checks["scene_meta_json_valid"] = False

        normalized = {
            "target_engine": None,
            "production_state": None,
            "duration_s": None,
            "dialogue": {"enabled": None, "language": None},
            "dependencies": [],
            "tags": [],
            "render_state": "SLOW_PENDING" if scene_id in slow_scenes else "IDLE",
        }

        if raw_meta is not None:
            if set(raw_meta) - SCENE_META_FIELDS:
                checks["scene_meta_allowed_fields_valid"] = False

            target_engine = raw_meta.get("target_engine")
            if target_engine is not None and (
                not isinstance(target_engine, str) or not target_engine.strip()
            ):
                checks["scene_meta_target_engine_valid"] = False
            else:
                normalized["target_engine"] = target_engine

            production_state = raw_meta.get("production_state")
            if production_state is not None and production_state not in PRODUCTION_STATES:
                checks["scene_meta_production_state_valid"] = False
            else:
                normalized["production_state"] = production_state

            duration_s = raw_meta.get("duration_s")
            if duration_s is not None and (
                not isinstance(duration_s, int)
                or isinstance(duration_s, bool)
                or duration_s <= 0
            ):
                checks["scene_meta_duration_positive"] = False
            else:
                normalized["duration_s"] = duration_s

            dialogue, dialogue_valid = normalize_dialogue(raw_meta.get("dialogue"))
            normalized["dialogue"] = dialogue
            checks["scene_meta_dialogue_valid"] &= dialogue_valid

            dependencies, types_valid, targets_valid = normalize_dependencies(
                raw_meta.get("dependencies"), active_scene_ids
            )
            normalized["dependencies"] = dependencies
            checks["scene_meta_dependency_types_valid"] &= types_valid
            checks["scene_meta_dependency_targets_exist"] &= targets_valid

            tags = raw_meta.get("tags")
            if tags is not None:
                if not isinstance(tags, list) or any(
                    not isinstance(tag, str) or not tag.strip() for tag in tags
                ):
                    checks["scene_meta_tags_valid"] = False
                else:
                    normalized["tags"] = tags

        scene_meta[str(scene_id)] = normalized

    return scene_meta, checks


def build_instruction_sync(instruction_dir, repo_root, snapshot_at):
    files = {}
    all_match = True
    complete = bool(instruction_dir and repo_root)

    if not complete:
        return {
            "health": "unverified",
            "snapshot_at": snapshot_at,
            "source_of_truth": "Google Drive canonical instruction files",
            "verification_mode": "authenticated_drive_check_not_configured",
            "files": files,
        }, None

    instruction_dir = Path(instruction_dir)
    repo_root = Path(repo_root)

    for name in INSTRUCTION_FILES:
        drive_path = instruction_dir / name
        mirror_path = repo_root / name
        if not drive_path.is_file() or not mirror_path.is_file():
            all_match = False
            files[name] = {
                "drive_sha256": None,
                "mirror_sha256": None,
                "match": False,
            }
            continue

        drive_bytes = drive_path.read_bytes()
        mirror_bytes = mirror_path.read_bytes()
        drive_sha = sha256_bytes(drive_bytes)
        mirror_sha = sha256_bytes(mirror_bytes)
        match = drive_bytes == mirror_bytes
        all_match &= match
        files[name] = {
            "drive_sha256": drive_sha,
            "mirror_sha256": mirror_sha,
            "match": match,
            "bytes": len(drive_bytes),
        }

    return {
        "health": "ok" if all_match else "error",
        "snapshot_at": snapshot_at,
        "source_of_truth": "Google Drive canonical instruction files",
        "files": files,
    }, all_match


def parse_master(
    path: Path,
    synced_at: str | None = None,
    instruction_dir: Path | None = None,
    repo_root: Path | None = None,
    instruction_snapshot_at: str | None = None,
):
    master_bytes = path.read_bytes()
    text = master_bytes.decode("utf-8")

    rev = re.search(r"\*\*(\d{2}\.\d{2}\.\d{4}) · (\d+) сцен[^·\n]* · (\d+) полн", text)
    if not rev:
        fail("revision line not found")
    revision_date, declared_scenes, declared_prompts = (
        rev.group(1),
        int(rev.group(2)),
        int(rev.group(3)),
    )

    work = re.search(r"\*\*🛠️\s*(\d+)\*\*[^\n]*?(W\d+(?:,\s*W\d+)*)", text)
    if not work:
        fail("work-items status line not found")
    declared_work = int(work.group(1))
    work_ids = re.findall(r"W\d+", work.group(2))

    slow = re.search(r"\*\*⏳\s*(\d+)\*\*[^\n]*?:\s*\*\*([0-9, ]+)\*\*", text)
    if not slow:
        fail("slow-generation status line not found")
    declared_slow = int(slow.group(1))
    slow_scenes = [int(x) for x in re.findall(r"\d+", slow.group(2))]

    master_sync = re.search(
        r"Последняя полная синхронизация:\*\*\s*\*\*(\d{2}\.\d{2}\.\d{4}) · (\d{2}:\d{2}) \(([+-]\d{2}:\d{2})\)",
        text,
    )
    if not master_sync:
        fail("last full synchronization timestamp not found")
    master_declared_sync = (
        f"{master_sync.group(1)} · {master_sync.group(2)} ({master_sync.group(3)})"
    )

    section_scenes = [int(x) for x in re.findall(r"^## Сцена (\d+)\b", text, re.M)]
    toc_scenes = [int(x) for x in re.findall(r"^\|\s*(\d+)\s*\|\s*\[", text, re.M)]
    prompt_texts = sum(
        1 for line in text.splitlines() if line.strip().startswith("```")
    ) // 2

    dedicated_slow = [
        int(x)
        for x in re.findall(
            rf"^\|\s*(\d+)\s+—[^\n]*\|\s*{re.escape(SLOW_LABEL)}\s*\|", text, re.M
        )
    ]
    toc_slow = [
        int(x)
        for x in re.findall(
            rf"^\|\s*(\d+)\s*\|[^\n]*<br>\*\*{re.escape(SLOW_LABEL)}\*\*", text, re.M
        )
    ]
    section_slow = []
    for n in section_scenes:
        m = re.search(
            rf"^## Сцена {n}\b(.*?)(?=^## Сцена \d+\b|\Z)", text, re.M | re.S
        )
        if m and f"**{SLOW_LABEL}**" in m.group(1):
            section_slow.append(n)

    unique_increasing = section_scenes == sorted(set(section_scenes))
    scene_meta, scene_meta_checks = parse_scene_metadata(
        text, section_scenes, slow_scenes
    )

    instruction_sync, instruction_match = build_instruction_sync(
        instruction_dir, repo_root, instruction_snapshot_at
    )

    checks = {
        "declared_scene_count_matches_sections": declared_scenes == len(section_scenes),
        "declared_scene_count_matches_toc": declared_scenes == len(toc_scenes),
        "scene_numbers_match_toc_and_sections": toc_scenes == section_scenes,
        "declared_prompt_count_matches_fences": declared_prompts == prompt_texts,
        "declared_work_count_matches_ids": declared_work == len(work_ids),
        "declared_slow_count_matches_list": declared_slow == len(slow_scenes),
        "slow_status_matches_dedicated_table": slow_scenes == dedicated_slow,
        "slow_status_matches_toc": slow_scenes == toc_slow,
        "slow_status_matches_sections": slow_scenes == section_slow,
        "scene_numbers_are_unique_and_increasing": unique_increasing,
        "canonical_master_sha256_present": bool(sha256_bytes(master_bytes)),
        **scene_meta_checks,
    }
    if instruction_match is not None:
        checks["instruction_mirrors_match_drive"] = instruction_match
    health = "ok" if all(checks.values()) else "error"

    if synced_at is None:
        iso_date = display_date_to_iso(master_sync.group(1))
        synced_at = f"{iso_date}T{master_sync.group(2)}:00{master_sync.group(3)}"

    canonical_master_sha256 = sha256_bytes(master_bytes)

    audit_fingerprint = {
        "revision_date": revision_date,
        "synced_at": synced_at,
        "canonical_master_sha256": canonical_master_sha256,
        "scene_count": declared_scenes,
        "prompt_count": declared_prompts,
        "scene_ids": section_scenes,
        "work_items": work_ids,
        "slow_scenes": slow_scenes,
        "health": health,
        "instruction_sync_health": instruction_sync["health"],
    }

    status = {
        "schema_version": 3,
        "source_of_truth": "Google Drive/AI Film Prompts Master/video-prompts.md",
        "instruction_source_of_truth": "Google Drive canonical instruction files",
        "automation": "Drive master -> validation -> GitHub master mirror + project-status.json -> GitHub Pages; instruction freshness requires authenticated check",
        "synced_at": synced_at,
        "revision_date": revision_date,
        "master_declared_last_full_sync": master_declared_sync,
        "canonical_master_sha256": canonical_master_sha256,
        "canonical_master_bytes": len(master_bytes),
        "scenes": declared_scenes,
        "prompt_texts": declared_prompts,
        "work_items": work_ids,
        "work_items_count": declared_work,
        "slow_scenes": slow_scenes,
        "slow_scenes_count": declared_slow,
        "scene_ids": section_scenes,
        "latest_scene": max(section_scenes) if section_scenes else None,
        "instruction_sync": instruction_sync,
        "warnings": (["instruction_sync_unverified"] if instruction_sync["health"] == "unverified" else []),
        "scene_meta": scene_meta,
        "audit_fingerprint": audit_fingerprint,
        "health": health,
        "checks": checks,
    }
    return status


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("master", nargs="?", default="video-prompts.md")
    ap.add_argument("--output", default="project-status.json")
    ap.add_argument("--synced-at")
    ap.add_argument("--instruction-dir")
    ap.add_argument("--repo-root")
    ap.add_argument("--instruction-snapshot-at")
    ap.add_argument("--check-only", action="store_true")
    args = ap.parse_args()

    status = parse_master(
        Path(args.master),
        args.synced_at,
        Path(args.instruction_dir) if args.instruction_dir else None,
        Path(args.repo_root) if args.repo_root else None,
        args.instruction_snapshot_at,
    )
    print(json.dumps(status, ensure_ascii=False, indent=2))
    if status["health"] != "ok":
        fail("master invariant check failed")
    if not args.check_only:
        Path(args.output).write_text(
            json.dumps(status, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )


if __name__ == "__main__":
    main()
