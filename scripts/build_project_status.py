#!/usr/bin/env python3
import argparse, json, re, sys
from pathlib import Path

SLOW_LABEL = "⏳ В МЕДЛЕННОЙ ГЕНЕРАЦИИ"

def fail(msg):
    print(f"ERROR: {msg}", file=sys.stderr)
    raise SystemExit(1)

def display_date_to_iso(value: str) -> str:
    day, month, year = value.split('.')
    return f"{year}-{month}-{day}"

def parse_master(path: Path, synced_at: str | None = None):
    text = path.read_text(encoding='utf-8')

    rev = re.search(r"\*\*(\d{2}\.\d{2}\.\d{4}) · (\d+) сцен[^·\n]* · (\d+) полн", text)
    if not rev:
        fail('revision line not found')
    revision_date, declared_scenes, declared_prompts = rev.group(1), int(rev.group(2)), int(rev.group(3))

    work = re.search(r"\*\*🛠️\s*(\d+)\*\*[^\n]*?(W\d+(?:,\s*W\d+)*)", text)
    if not work:
        fail('work-items status line not found')
    declared_work = int(work.group(1))
    work_ids = re.findall(r"W\d+", work.group(2))

    slow = re.search(r"\*\*⏳\s*(\d+)\*\*[^\n]*?:\s*\*\*([0-9, ]+)\*\*", text)
    if not slow:
        fail('slow-generation status line not found')
    declared_slow = int(slow.group(1))
    slow_scenes = [int(x) for x in re.findall(r"\d+", slow.group(2))]

    master_sync = re.search(
        r"Последняя полная синхронизация:\*\*\s*\*\*(\d{2}\.\d{2}\.\d{4}) · (\d{2}:\d{2}) \(([+-]\d{2}:\d{2})\)",
        text,
    )
    if not master_sync:
        fail('last full synchronization timestamp not found')
    master_declared_sync = f"{master_sync.group(1)} · {master_sync.group(2)} ({master_sync.group(3)})"

    section_scenes = [int(x) for x in re.findall(r"^## Сцена (\d+)\b", text, re.M)]
    toc_scenes = [int(x) for x in re.findall(r"^\|\s*(\d+)\s*\|\s*\[", text, re.M)]
    prompt_texts = sum(1 for line in text.splitlines() if line.strip().startswith('```')) // 2

    dedicated_slow = [int(x) for x in re.findall(rf"^\|\s*(\d+)\s+—[^\n]*\|\s*{re.escape(SLOW_LABEL)}\s*\|", text, re.M)]
    toc_slow = [int(x) for x in re.findall(rf"^\|\s*(\d+)\s*\|[^\n]*<br>\*\*{re.escape(SLOW_LABEL)}\*\*", text, re.M)]
    section_slow = []
    for n in section_scenes:
        m = re.search(rf"^## Сцена {n}\b(.*?)(?=^## Сцена \d+\b|\Z)", text, re.M | re.S)
        if m and f"**{SLOW_LABEL}**" in m.group(1):
            section_slow.append(n)

    checks = {
        'declared_scene_count_matches_sections': declared_scenes == len(section_scenes),
        'declared_scene_count_matches_toc': declared_scenes == len(toc_scenes),
        'scene_numbers_match_toc_and_sections': toc_scenes == section_scenes,
        'declared_prompt_count_matches_fences': declared_prompts == prompt_texts,
        'declared_work_count_matches_ids': declared_work == len(work_ids),
        'declared_slow_count_matches_list': declared_slow == len(slow_scenes),
        'slow_status_matches_dedicated_table': slow_scenes == dedicated_slow,
        'slow_status_matches_toc': slow_scenes == toc_slow,
        'slow_status_matches_sections': slow_scenes == section_slow,
        'all_scene_numbers_are_contiguous': section_scenes == list(range(1, declared_scenes + 1)),
    }
    health = 'ok' if all(checks.values()) else 'error'

    # Deterministic by default: generated status uses the synchronization
    # timestamp declared in the canonical Drive master. Scheduled validation
    # therefore creates no meaningless commits when the master is unchanged.
    if synced_at is None:
        iso_date = display_date_to_iso(master_sync.group(1))
        synced_at = f"{iso_date}T{master_sync.group(2)}:00{master_sync.group(3)}"

    status = {
        'schema_version': 1,
        'source_of_truth': 'Google Drive/AI Film Prompts Master/video-prompts.md',
        'automation': 'Drive -> validation -> GitHub mirror + project-status.json -> GitHub Pages',
        'synced_at': synced_at,
        'revision_date': revision_date,
        'master_declared_last_full_sync': master_declared_sync,
        'scenes': declared_scenes,
        'prompt_texts': declared_prompts,
        'work_items': work_ids,
        'work_items_count': declared_work,
        'slow_scenes': slow_scenes,
        'slow_scenes_count': declared_slow,
        'latest_scene': max(section_scenes) if section_scenes else None,
        'health': health,
        'checks': checks,
    }
    return status

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('master', nargs='?', default='video-prompts.md')
    ap.add_argument('--output', default='project-status.json')
    ap.add_argument('--synced-at')
    ap.add_argument('--check-only', action='store_true')
    args = ap.parse_args()

    status = parse_master(Path(args.master), args.synced_at)
    print(json.dumps(status, ensure_ascii=False, indent=2))
    if status['health'] != 'ok':
        fail('master invariant check failed')
    if not args.check_only:
        Path(args.output).write_text(json.dumps(status, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

if __name__ == '__main__':
    main()
