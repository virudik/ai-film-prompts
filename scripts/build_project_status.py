#!/usr/bin/env python3
import argparse
import hashlib
import json
import re
import sys
from datetime import datetime
from pathlib import Path

SLOW_LABEL = "⏳ В МЕДЛЕННОЙ ГЕНЕРАЦИИ"
INSTRUCTION_FILES = (
    "NEW-CHAT-HANDOFF.md",
    "SYNC-RUNBOOK.md",
    "AI-PROJECT-GUIDE.md",
    "PROMPT-STYLE-GUIDE.md",
    "USER-GUIDE.md",
    "README-AI-SYNC.md",
    "BACKUP-AI-RUNBOOK.md",
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
TERMINAL_TOPVIEW_STATUSES = {"success", "fail", "failed", "cancelled"}
ACTIVE_TOPVIEW_STATUSES = {"init", "queued", "running", "processing"}

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


def parse_iso_datetime(value):
    if not value:
        return None
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except (ValueError, TypeError):
        return None
    # Health timestamps must be timezone-aware. Naive values make freshness
    # comparisons ambiguous and previously could raise TypeError.
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        return None
    return parsed


def build_instruction_sync(
    instruction_dir,
    repo_root,
    snapshot_at,
    status_file=None,
    synced_at=None,
):
    files = {}
    all_match = True
    complete = bool(instruction_dir and repo_root)

    if not complete:
        status_path = Path(status_file) if status_file else None
        if status_path and status_path.is_file():
            try:
                external = json.loads(status_path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                external = None

            if isinstance(external, dict):
                checked_at = external.get("checked_at")
                max_hours = external.get("freshness_max_hours", 3)
                try:
                    max_hours = float(max_hours)
                except (TypeError, ValueError):
                    max_hours = 3.0

                checked_dt = parse_iso_datetime(checked_at)
                sync_dt = parse_iso_datetime(synced_at)
                age_hours = None
                timestamp_valid = checked_dt is not None and sync_dt is not None
                if timestamp_valid:
                    age_hours = (sync_dt - checked_dt).total_seconds() / 3600.0

                external_files = external.get("files")
                if not isinstance(external_files, dict):
                    external_files = {}

                def external_file_match(name, info):
                    if not isinstance(info, dict) or info.get("match") is not True:
                        return False
                    drive_hash = info.get("drive_sha256")
                    mirror_hash = info.get("mirror_sha256")
                    if drive_hash is not None or mirror_hash is not None:
                        valid = re.compile(r"^[0-9a-f]{64}$")
                        if not (
                            isinstance(drive_hash, str)
                            and isinstance(mirror_hash, str)
                            and bool(valid.fullmatch(drive_hash))
                            and bool(valid.fullmatch(mirror_hash))
                            and drive_hash == mirror_hash
                        ):
                            return False
                    github_blob = info.get("github_blob")
                    if github_blob is not None:
                        if not isinstance(github_blob, str) or not re.fullmatch(r"[0-9a-f]{40}", github_blob):
                            return False
                        candidate = Path.cwd() / name
                        if not candidate.is_file():
                            return False
                        data = candidate.read_bytes()
                        actual_blob = hashlib.sha1(
                            f"blob {len(data)}\0".encode("ascii") + data
                        ).hexdigest()
                        if github_blob != actual_blob:
                            return False
                    return True

                all_match = bool(external.get("all_match")) and all(
                    external_file_match(name, external_files.get(name))
                    for name in INSTRUCTION_FILES
                )

                raw_health = external.get("health")
                # Fail closed on missing/invalid/future certificate timestamps.
                fresh = (
                    timestamp_valid
                    and age_hours is not None
                    and 0.0 <= age_hours <= max_hours
                )

                if raw_health == "ok" and all_match and fresh:
                    health = "ok"
                    instruction_match = True
                elif raw_health == "ok" and all_match and not fresh:
                    health = "stale"
                    instruction_match = None
                else:
                    health = "error"
                    instruction_match = False

                return {
                    "health": health,
                    "snapshot_at": checked_at,
                    "source_of_truth": "Google Drive canonical instruction files",
                    "verification_mode": external.get(
                        "verification_mode",
                        "authorized_external_instruction_check",
                    ),
                    "freshness_max_hours": max_hours,
                    "age_hours_at_status_build": (
                        round(age_hours, 3) if age_hours is not None else None
                    ),
                    "files": external_files,
                }, instruction_match

        return {
            "health": "unverified",
            "snapshot_at": snapshot_at,
            "source_of_truth": "Google Drive canonical instruction files",
            "verification_mode": "authorized_instruction_check_not_available",
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
    instruction_status_file: Path | None = None,
    topview_status_file: Path | None = None,
    topview_task_map_file: Path | None = None,
):
    master_bytes = path.read_bytes()
    has_utf8_bom = master_bytes.startswith(b"\xef\xbb\xbf")
    if has_utf8_bom:
        fail("canonical master contains UTF-8 BOM")
    try:
        text = master_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        fail(f"canonical master is not valid UTF-8: {exc}")

    rev = re.search(r"\*\*(\d{2}\.\d{2}\.\d{4}) · (\d+) сцен[^·\n]* · (\d+) полн", text)
    if not rev:
        fail("revision line not found")
    revision_date, declared_scenes, declared_prompts = (
        rev.group(1),
        int(rev.group(2)),
        int(rev.group(3)),
    )

    work = re.search(r"\*\*🛠️\s*(\d+)\*\*([^\n]*)", text)
    if not work:
        fail("work-items status line not found")
    declared_work = int(work.group(1))
    work_tail = work.group(2)

    # Accept explicit IDs and compact ranges such as W7–W15 / W7-W15.
    # Expand ranges deterministically so status always represents the real IDs.
    work_ids = []
    consumed_spans = []
    for m in re.finditer(r"W(\d+)\s*[–—-]\s*W?(\d+)", work_tail):
        start, end = int(m.group(1)), int(m.group(2))
        if end < start:
            fail(f"invalid descending work-item range W{start}-W{end}")
        work_ids.extend(f"W{i}" for i in range(start, end + 1))
        consumed_spans.append(m.span())
    remainder = work_tail
    for start, end in reversed(consumed_spans):
        remainder = remainder[:start] + (" " * (end - start)) + remainder[end:]
    work_ids.extend(re.findall(r"W\d+", remainder))
    work_ids = list(dict.fromkeys(work_ids))

    slow = re.search(r"\*\*⏳\s*(\d+)\*\*[^\n]*?:\s*\*\*([0-9, ]+)\*\*", text)
    if not slow:
        fail("slow-generation status line not found")
    declared_slow = int(slow.group(1))
    slow_scenes = [int(x) for x in re.findall(r"\d+", slow.group(2))]

    master_sync = re.search(
        r"Последняя полная синхронизация:\*\*\s*\*\*(.*?)\*\*",
        text,
    )
    if not master_sync:
        fail("last full synchronization declaration not found")
    master_declared_sync = master_sync.group(1).strip()

    section_scenes = [int(x) for x in re.findall(r"^## Сцена (\d+)\b", text, re.M)]
    anchor_scenes = [int(x) for x in re.findall(r'<a\s+id=["\']scene-(\d+)["\']\s*></a>', text, re.I)]
    reserved_match = re.search(
        r"Сцены\s+([^\n]+?)\s+удалены из active master[^\n]*?зарезервированы",
        text,
        re.I,
    )
    reserved_scene_ids = (
        [int(x) for x in re.findall(r"\d+", reserved_match.group(1))]
        if reserved_match
        else []
    )
    toc_scenes = [int(x) for x in re.findall(r"^\|\s*(\d+)\s*\|\s*\[", text, re.M)]
    fence_lines = [line for line in text.splitlines() if line.strip().startswith("```")]
    prompt_texts = len(fence_lines) // 2
    fences_balanced = len(fence_lines) % 2 == 0

    dedicated_slow = [
        int(x)
        for x in re.findall(
            rf"^\|\s*(\d+)\s+—[^\n]*\|\s*{re.escape(SLOW_LABEL)}(?:[^|]*)\|", text, re.M
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
        instruction_dir,
        repo_root,
        instruction_snapshot_at,
        instruction_status_file,
        synced_at,
    )

    checks = {
        "declared_scene_count_matches_sections": declared_scenes == len(section_scenes),
        "declared_scene_count_matches_toc": declared_scenes == len(toc_scenes),
        "scene_numbers_match_toc_and_sections": toc_scenes == section_scenes,
        "declared_prompt_count_matches_fences": declared_prompts == prompt_texts,
        "declared_work_count_matches_ids": declared_work == len(work_ids),
        "declared_slow_count_matches_list": declared_slow == len(slow_scenes),
        "slow_status_matches_dedicated_table": set(slow_scenes) == set(dedicated_slow),
        "slow_status_matches_toc": set(slow_scenes) == set(toc_slow),
        "slow_status_matches_sections": set(slow_scenes) == set(section_slow),
        "scene_numbers_are_unique_and_increasing": unique_increasing,
        "scene_anchors_match_sections": anchor_scenes == section_scenes,
        "scene_anchors_unique": len(anchor_scenes) == len(set(anchor_scenes)),
        "reserved_scene_ids_declared": bool(reserved_scene_ids),
        "reserved_scene_ids_not_reused": not (set(reserved_scene_ids) & set(section_scenes)),
        "prompt_fences_balanced": fences_balanced,
        "canonical_master_utf8_without_bom": not has_utf8_bom,
        "slow_scene_ids_unique": len(slow_scenes) == len(set(slow_scenes)),
        "slow_scene_ids_active": all(scene_id in set(section_scenes) for scene_id in slow_scenes),
        "canonical_master_sha256_present": bool(sha256_bytes(master_bytes)),
        **scene_meta_checks,
    }
    if instruction_match is not None:
        checks["instruction_mirrors_match_drive"] = instruction_match
    # Optional cross-layer Topview validation. This is deterministic and blocks a false green
    # when current telemetry files are supplied by the workflow.
    if topview_status_file and topview_task_map_file:
        try:
            topview = json.loads(Path(topview_status_file).read_text(encoding="utf-8"))
            task_map = json.loads(Path(topview_task_map_file).read_text(encoding="utf-8"))
            active_tasks = topview.get("active_tasks", [])
            active_by_scene = task_map.get("active_by_scene", {})
            processed = task_map.get("processed_tasks", [])
            flat_active = [
                task_id
                for task_ids in active_by_scene.values()
                if isinstance(task_ids, list)
                for task_id in task_ids
            ]
            active_scene_ids = sorted(
                int(scene_id)
                for scene_id, task_ids in active_by_scene.items()
                if isinstance(task_ids, list) and task_ids
            )
            telemetry_task_ids = [
                item.get("task_id") for item in active_tasks if isinstance(item, dict)
            ]
            occupied = topview.get("occupied_slots")
            capacity = topview.get("slot_capacity", 6)
            free = topview.get("free_slots")
            processed_terminal_only = {
                int(item["scene_id"])
                for item in processed
                if isinstance(item, dict)
                and isinstance(item.get("scene_id"), int)
                and str(item.get("final_status", "")).lower() in TERMINAL_TOPVIEW_STATUSES
                and str(item["scene_id"]) not in active_by_scene
            }
            checks.update({
                "topview_active_task_ids_unique": len(flat_active) == len(set(flat_active)),
                "topview_telemetry_task_ids_unique": len(telemetry_task_ids) == len(set(telemetry_task_ids)),
                "topview_active_tasks_match_task_map": sorted(telemetry_task_ids) == sorted(flat_active),
                "topview_active_statuses_valid": all(
                    isinstance(item, dict)
                    and str(item.get("topview_status", "")).lower() in ACTIVE_TOPVIEW_STATUSES
                    for item in active_tasks
                ),
                "topview_task_scene_mapping_matches": all(
                    isinstance(item, dict)
                    and isinstance(item.get("scene_id"), int)
                    and item.get("task_id") in active_by_scene.get(str(item.get("scene_id")), [])
                    for item in active_tasks
                ),
                "topview_active_scene_ids_exist": all(
                    isinstance(item, dict) and item.get("scene_id") in set(section_scenes)
                    for item in active_tasks
                ),
                "topview_occupied_matches_active_tasks": occupied == len(active_tasks) == len(flat_active),
                "topview_free_slots_equation": free == max(0, capacity - occupied),
                "topview_capacity_not_exceeded": occupied <= capacity == 6,
                "topview_active_scenes_are_canonical_slow": set(active_scene_ids).issubset(set(slow_scenes)),
                "no_terminal_only_topview_scene_is_slow": not (processed_terminal_only & set(slow_scenes)),
            })
        except (OSError, json.JSONDecodeError, TypeError, ValueError, KeyError) as exc:
            checks["topview_cross_layer_files_valid"] = False

    health = "ok" if all(checks.values()) else "error"

    if synced_at is None:
        timestamp_match = re.search(
            r"(\\d{2}\\.\\d{2}\\.\\d{4}) · (\\d{2}:\\d{2}) \\(([+-]\\d{2}:\\d{2})\\)",
            master_declared_sync,
        )
        if timestamp_match:
            iso_date = display_date_to_iso(timestamp_match.group(1))
            synced_at = f"{iso_date}T{timestamp_match.group(2)}:00{timestamp_match.group(3)}"
        else:
            synced_at = datetime.now().astimezone().isoformat()

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
        "automation": "Drive master -> validation -> GitHub mirror/status -> Pages; authorized connector verifies private instruction mirrors into instruction-sync-status.json",
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
        "reserved_scene_ids": reserved_scene_ids,
        "instruction_sync": instruction_sync,
        "warnings": (
            []
            if instruction_sync["health"] == "ok"
            else [f"instruction_sync_{instruction_sync['health']}"]
        ),
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
    ap.add_argument("--instruction-status-file", default="instruction-sync-status.json")
    ap.add_argument("--topview-status-file")
    ap.add_argument("--topview-task-map-file")
    ap.add_argument("--check-only", action="store_true")
    args = ap.parse_args()

    status = parse_master(
        Path(args.master),
        args.synced_at,
        Path(args.instruction_dir) if args.instruction_dir else None,
        Path(args.repo_root) if args.repo_root else None,
        args.instruction_snapshot_at,
        Path(args.instruction_status_file) if args.instruction_status_file else None,
        Path(args.topview_status_file) if args.topview_status_file else None,
        Path(args.topview_task_map_file) if args.topview_task_map_file else None,
    )
    print(json.dumps(status, ensure_ascii=False, indent=2))
    # Always persist the generated status before returning a failing health code.
    # This lets the Control Center publish an explicit non-green snapshot instead
    # of remaining silently stuck on an older "ok" status.
    if not args.check_only:
        Path(args.output).write_text(
            json.dumps(status, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    if status["health"] != "ok":
        fail("master invariant check failed")


if __name__ == "__main__":
    main()
