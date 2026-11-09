#!/usr/bin/env python3
"""Audit S74-S80 without changing assets or inferring facial likeness from hashes."""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import struct
from datetime import datetime, timezone
from pathlib import Path

WORK_ID = 'SEREGIUS-PARODIES-20261109'
SCENES = tuple(range(74, 81))
EXPECTED_IDENTITIES = {
    74: {'references/full/vitalik.jpg'},
    75: {'references/full/vitalik.jpg'},
    76: {'references/full/vitalik.jpg'},
    77: {'references/full/vitalik.jpg', 'references/full/lesha.jpg', 'references/scenes/scene-67/S67-Masha-R-tatooine-sheet.png'},
    78: {'references/full/vitalik.jpg', 'references/scenes/scene-67/S67-Masha-R-tatooine-sheet.png', 'references/scenes/scene-66/S66-Alina-tatooine-sheet.png'},
    79: {'references/full/vitalik.jpg', 'references/scenes/scene-67/S67-Masha-R-tatooine-sheet.png', 'references/scenes/scene-66/S66-Alina-tatooine-sheet.png'},
    80: {'references/full/vitalik.jpg', 'references/scenes/scene-67/S67-Masha-R-tatooine-sheet.png', 'references/scenes/scene-66/S66-Alina-tatooine-sheet.png'},
}

def safe_path(root: Path, value: str) -> Path:
    path = (root / value).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError(f'Path outside repository: {value}')
    return path

def read_json(root: Path, value: str) -> dict:
    return json.loads(safe_path(root, value).read_text(encoding='utf-8'))

def audit(root: Path) -> dict:
    root = root.resolve()
    errors: list[str] = []
    pending: list[dict] = []
    scene_rows: list[dict] = []
    master = safe_path(root, 'video-prompts.md').read_text(encoding='utf-8')
    pattern = re.compile(r'(?ms)(^## Сцена (\d+) — .*?)(?=\n---\n\n<a id="scene-\d+"></a>|\Z)')
    matches = list(pattern.finditer(master))
    blocks = {int(m[2]): m[1] for m in matches}
    primary_count = 0
    report = read_json(root, 'reports/parody-scenes-2026-11-09.json')
    jobs_report = read_json(root, 'reports/parody-supplementary-reference-jobs-2026-11-09.json')
    rejected = set()
    for document in (report, jobs_report):
        for key in ('rejected_outputs', 'rejected_attempt_history', 'attempts_this_turn'):
            for item in document.get(key, []):
                if item.get('sha256') and item.get('status', 'rejected') == 'rejected':
                    rejected.add(item['sha256'])
    for sid in SCENES:
        if sum(int(m[2]) == sid for m in matches) != 1:
            errors.append(f'S{sid}: missing or duplicate scene block')
        block = blocks.get(sid, '')
        prompt_count = block.count('```text')
        if prompt_count != 3:
            errors.append(f'S{sid}: expected 3 prompt blocks, found {prompt_count}')
        manifest = read_json(root, f'references/scenes/scene-{sid}/manifest.json')
        identities = {r.get('path') for r in manifest.get('references', []) if r.get('role') == 'identity'}
        if identities != EXPECTED_IDENTITIES[sid]:
            errors.append(f'S{sid}: identity bindings differ from owner-confirmed cast')
        staging = []
        for reference in manifest.get('references', []):
            name = reference.get('path', '')
            asset = safe_path(root, name)
            if not asset.is_file():
                errors.append(f'S{sid}: missing referenced asset {name}')
                continue
            raw = asset.read_bytes()
            actual = hashlib.sha256(raw).hexdigest()
            if actual != reference.get('sha256'):
                errors.append(f'S{sid}: SHA mismatch {name}')
            if actual in rejected:
                errors.append(f'S{sid}: rejected output is attached {name}')
            if name not in block:
                errors.append(f'S{sid}: asset not referenced by scene text {name}')
            if reference.get('role') == 'scene_staging':
                png_ok = raw.startswith(b'\x89PNG\r\n\x1a\n') and len(raw) >= 24
                dimensions = list(struct.unpack('>II', raw[16:24])) if png_ok else None
                if not png_ok:
                    errors.append(f'S{sid}: staged asset is not a readable PNG header {name}')
                staging.append({'path': name, 'sha256': actual, 'dimensions': dimensions,
                                'owner_approval': reference.get('owner_approval'),
                                'sha_match': actual == reference.get('sha256')})
        if not staging:
            pending.append({'scene_id': sid, 'kind': 'primary_still', 'reason': 'No attached staged PNG'})
        else:
            primary_count += 1
        scene_rows.append({'scene_id': sid, 'prompt_blocks': prompt_count,
                           'identity_paths': sorted(identities), 'staging': staging})
    for sid in SCENES:
        manifest = read_json(root, f'references/scenes/scene-{sid}/manifest.json')
        for item in manifest.get('additional_references_pending', []):
            pending.append({'scene_id': sid, 'kind': 'declared_additional_reference', 'requirement': item, 'reason': 'Manifest declares this requirement unresolved'})
    expected_jobs = {
        'references/scenes/scene-74/S74-torch-curtain.png',
        'references/scenes/scene-74/S74-globe-stage.png',
        'references/scenes/scene-74/S74-potato-mountain.png',
        'references/scenes/scene-74/S74-searchlight-crates.png',
        'references/scenes/scene-74/S74-saucepan-gong.png',
        'references/scenes/scene-76/S76-normalno-ice.png',
        'references/scenes/scene-76/S76-yaz-boat.png',
    }
    declared_jobs = {j.get('target_path') for j in jobs_report.get('jobs', [])}
    for missing in sorted(expected_jobs - declared_jobs):
        pending.append({'kind': 'missing_supplementary_job', 'path': missing, 'reason': 'Missing record is not completion'})
    supplementary_rows = []
    for job in jobs_report.get('jobs', []):
        name = job['target_path']
        exists = safe_path(root, name).is_file()
        manifest = read_json(root, f"references/scenes/scene-{job['scene_id']}/manifest.json")
        attached = any(ref.get('path') == name for ref in manifest.get('references', []))
        row = {'scene_id': job['scene_id'], 'kind': job['kind'], 'path': name,
               'actual_file_exists': exists, 'attached': attached, 'declared_status': job.get('status')}
        supplementary_rows.append(row)
        if not exists or not attached:
            pending.append({'scene_id': job['scene_id'], 'kind': job['kind'], 'path': name,
                            'reason': 'Actual file and manifest attachment are both required'})
    source_report = read_json(root, 'reports/parody-scenes-source-2026-11-09.json')
    source_review = source_report.get('source_review', {})
    original_review_verified = source_review.get('continuous_playback_audio_verified') is True
    if not original_review_verified:
        pending.append({'kind': 'original_meme_audio_visual_review',
                        'reason': 'No explicit evidence of completed original-video playback/audio review'})
    # Bound source images and file hashes do NOT prove that a generated face looks right.
    likeness_review_verified = report.get('visual_likeness_review', {}).get('all_required_frames_reviewed') is True
    if not likeness_review_verified:
        pending.append({'kind': 'visual_likeness_and_composition_review',
                        'reason': 'No complete per-frame likeness/composition review evidence; hashes do not prove identity'})
    return {'schema_version': 1, 'work_id': WORK_ID,
            'checked_at': datetime.now(timezone.utc).isoformat(),
            'scope': 'Existing S74-S80 files, cast bindings and evidence completeness; no generation, approval or video submission',
            'master_sha256': hashlib.sha256(master.encode()).hexdigest(),
            'execution_ok': True, 'integrity_ok': not errors,
            'work_complete': not errors and not pending,
            'primary_scenes_with_stills': primary_count,
            'prompt_blocks': sum(row['prompt_blocks'] for row in scene_rows),
            'scenes': scene_rows, 'supplementary': supplementary_rows,
            'errors': errors, 'pending': pending,
            'owner_approval_claimed': False, 'other_project_tasks_audited': False,
            'important': 'Successful execution of this audit does not mean the work is complete. Read work_complete and pending.'}

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', type=Path, nargs='?', default=Path('.'))
    parser.add_argument('--json-out', type=Path)
    parser.add_argument('--require-complete', action='store_true')
    args = parser.parse_args()
    try:
        result = audit(args.root)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        result = {'work_id': WORK_ID, 'execution_ok': False, 'work_complete': False,
                  'errors': [str(exc)], 'pending': []}
    output = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(output, encoding='utf-8')
    print(output)
    if not result.get('execution_ok') or result.get('errors'):
        return 1
    return 2 if args.require_complete and not result['work_complete'] else 0

if __name__ == '__main__':
    raise SystemExit(main())
