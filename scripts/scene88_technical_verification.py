"""Owner-scoped technical verification; no generation, approval or queue mutation.

Called by scene88-technical-verification.yml under an exact editor lease.
The staged patch is SHA-locked and all substantive scene inputs are protected.
"""
import concurrent.futures
import hashlib
import json
import os
import re
import subprocess
import sys
import time
import unittest
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

OUT = Path('/tmp/scene88-verification')
OUT.mkdir(exist_ok=True)
ROOT = Path.cwd()
sys.path.insert(0, str(ROOT / 'scripts'))
from resume_state import capture

WORK = 'SEREGIUS-SASHA-PHOTOGRAPHER-20261110'
REPORT = 'reports/scene88-technical-verification-2026-11-10.json'
PUB = 'reports/sasha-photographer-scene-88-2026-11-10.json'
EXPECTED = {
    'tests/test_prompt_send_qc.py': ('a055950faf56ba82b6254d3ab72b9604f54aa0af3919c5e0927786f77ee10e09', 'fdd40910a5d338584bc3d1d9225305aa3eb7bcf56d185e52423a7e00f26fed9f'),
    'tests/test_raznoe_resource_scene3.py': ('40ac875a81abe1a7f98b4ccb9dd96f5809c04398d787a9fb6339b9480a865444', '10f6eb13d0769ca2cffb0f08bd19a7f590833c672adaf0e2976e70854e9608b1'),
    'tests/test_topview_prompt_match.py': ('45f7e6cf2cbe33c222be8e45318d0fa00a35a2f0738625798c51ae820f4d4988', '17ad60ef5164f2e345746c0c7e70736e9bc58a04ed537e410d986043aeaed61d'),
}


def now():
    return datetime.now(timezone.utc).isoformat(timespec='seconds')


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def write_json(p, obj):
    Path(p).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def lease():
    lock = json.loads(Path('ops/canon-lock.json').read_text())
    assert lock['state'] == 'held' and lock['holder'] == os.environ['EXPECTED_HOLDER'], 'lease holder changed'
    assert lock['acquired_at'] == os.environ['EXPECTED_ACQUIRED_AT'], 'lease acquisition changed'
    assert datetime.fromisoformat(lock['expires_at'].replace('Z', '+00:00')) > datetime.now(timezone.utc), 'lease expired'


lease()
head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
pub = json.loads(Path(PUB).read_text())
protected_paths = ['video-prompts.md', 'ops/topview-launch-queue.json', 'review-ledger.json',
                   'references/scenes/scene-88/manifest.json', 'references/full/sasha.jpg', 'parodies.html',
                   'NEW-CHAT-HANDOFF.md', 'SYNC-RUNBOOK.md', 'AI-PROJECT-GUIDE.md', 'PROMPT-STYLE-GUIDE.md',
                   'USER-GUIDE.md', 'README-AI-SYNC.md', 'BACKUP-AI-RUNBOOK.md']
protected_paths += [str(p) for p in Path('projects').glob('*/video-prompts.md')]
protected_paths += [str(p) for p in Path('projects').glob('*/ops/topview-launch-queue.json')]
protected_paths += [a[key] for a in pub['assets'] for key in ('path', 'preview')]
protected = {p: sha(p) for p in protected_paths}
patch = '.github/patches/scene88-test-guards.patch'
assert sha(patch) == '1d0691b39bc506f5d9a60ca3488cc8289bbc7b8632970e0b402a75e49fefb893', 'patch changed'
if all(sha(p) == pair[0] for p, pair in EXPECTED.items()):
    subprocess.run(['git', 'apply', '--check', patch], check=True)
    subprocess.run(['git', 'apply', patch], check=True)
else:
    assert all(sha(p) == pair[1] for p, pair in EXPECTED.items()), 'test sources changed; inspect before retry'
assert all(sha(p) == pair[1] for p, pair in EXPECTED.items()), 'unexpected patch output'

suite = unittest.defaultTestLoader.discover('tests')
with (OUT / 'full-tests.log').open('w') as log:
    result = unittest.TextTestRunner(stream=log, verbosity=2).run(suite)
tests = {'checked_at': now(), 'tests_run': result.testsRun,
         'failures': [t.id() for t, _ in result.failures], 'errors': [t.id() for t, _ in result.errors],
         'skipped': [(t.id(), reason) for t, reason in result.skipped], 'all_tests_passed': result.wasSuccessful()}
write_json(OUT / 'test-results.json', tests)
print('TESTS', json.dumps(tests))
assert result.wasSuccessful() and result.testsRun >= 534 and not result.skipped, 'full suite not green'

base = 'https://xn--l1adcem8c.xn--d1aigvp.xn--p1ai/'
targets = []
for a in pub['assets']:
    targets.extend([(a['path'], a['sha256'], 'original'), (a['preview'], a['preview_sha256'], 'preview')])
targets.append(('references/full/sasha.jpg', pub['source_identity']['sha256'], 'identity'))
for p in ['video-prompts.md', 'references/scenes/scene-88/manifest.json', 'parodies.html']:
    targets.append((p, sha(p), 'published_text'))


def check(target):
    path, expected, kind = target
    row = {'path': path, 'kind': kind, 'expected_sha256': expected, 'canonical_sha256': sha(path), 'verified': False}
    try:
        request = urllib.request.Request(base + path + '?verify=' + str(time.time_ns()),
            headers={'Cache-Control': 'no-cache', 'User-Agent': 'AI-Film-owner-scene88-verification'})
        with urllib.request.urlopen(request, timeout=45) as response:
            raw = response.read(12000001)
            row.update(http_status=response.status, content_type=response.headers.get('Content-Type'), bytes=len(raw))
        assert len(raw) <= 12000000, 'download size limit'
        digest = hashlib.sha256(raw).hexdigest()
        row.update(actual_sha256=digest, verified=digest == expected == row['canonical_sha256'])
    except Exception as error:
        row['error'] = type(error).__name__ + ': ' + str(error)
    return row


with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    rows = list(pool.map(check, targets))
live = {'checked_at': now(), 'base_url': base, 'all_verified': all(row['verified'] for row in rows),
        'originals_verified': sum(row['verified'] for row in rows if row['kind'] == 'original'),
        'previews_verified': sum(row['verified'] for row in rows if row['kind'] == 'preview'), 'results': rows}
write_json(OUT / 'live-byte-verification.json', live)
assert live['all_verified'], 'published bytes mismatch or download failed'

validations = []
for name, command in [('site', ['scripts/validate_site.py', '.']),
                      ('instructions', ['scripts/check_instruction_consistency.py', '.']),
                      ('projects', ['scripts/projects.py', '.', 'validate'])]:
    run = subprocess.run([sys.executable, *command], capture_output=True, text=True)
    (OUT / (name + '-validation.log')).write_text(run.stdout + '\n' + run.stderr)
    validations.append({'name': name, 'exit_code': run.returncode})
    assert run.returncode == 0, name + ' validation failed'

causes = [
    {'test': 'test_handoff_is_one_pointer_line', 'cause': 'Dated 06.11 pointer was correctly moved to archive/handoff-log.md on 07.11; the test searched only the live handoff.', 'fix': 'Require exactly one intact pointer across live handoff and its linked archive; mutation checks detect loss or duplication.'},
    {'test': 'test_topview_keeps_free_route_and_points_at_receipt', 'cause': 'Test required the old exact free-route sentence and fixed 06.11 date at line 7; current 09.11 instructions retain zero-credit restrictions with an owner-authorized UI clarification.', 'fix': 'Validate the current 720p/16:9/single-output/free-Unlimited/zero-cost/no-paid contract and receipt rules; validate metadata date without pinning its position or old value. Mutation checks reject paid or multiple outputs.'},
    {'test': 'test_native_116_cut_keeps_source_and_names_unaccepted_attempts', 'cause': 'Hard-coded inventory 27 omitted nine active v3 prompts; the directory correctly contains 36.', 'fix': 'Preserve 19 originals plus eight v2 files, add exactly the active-cut files, verify their SHA256, 19 clips/114 seconds, 16:9 and not-approved/no-execution state; reject unregistered extras.'},
    {'test': 'test_scene_is_horizontal_and_not_approved', 'cause': 'Substring for RESOURCE scene 3 ran to end of the project master, so it incorrectly included portrait HONOR scenes.', 'fix': 'Bound scene text at the next top-level scene anchor; retain native subscene anchors; regression covers neighboring portrait scene and missing scene.'},
    {'test': 'test_every_master_block_is_found_and_labelled', 'cause': 'Three prompts of scene 73 use plain fences. Production parser found all 243; text-tag-only test count found 240.', 'fix': 'Independently count both supported fence forms and compare every full prompt body; add mixed-fence fixture. No prompt text or parser behavior changed.'},
]
report = {'schema_version': 1, 'work_id': WORK, 'project': 'seregius', 'scene_id': 88,
          'checked_at': now(), 'source_head': head, 'workflow_run_id': os.environ['GITHUB_RUN_ID'],
          'takeover_mode': 'short; 15/15 anchors and source hashes verified by continue_preflight',
          'baseline_run_id': '42890024464', 'baseline_tests': 534, 'baseline_failures': 5,
          'repairs': causes, 'test_files': {p: {'before_sha256': pair[0], 'after_sha256': sha(p)} for p, pair in EXPECTED.items()},
          'tests': tests, 'live_publication': live, 'validations': validations,
          'protected_files_unchanged': protected, 'technical_task_complete': True,
          'editorial_approval': False, 'video_launches': 0, 'credits_spent': 0,
          'scope': 'Scene 88 exact-byte published delivery and five named regression-test repairs only; not artistic acceptance or completion of unrelated historical tasks.'}
write_json(REPORT, report)
write_json(OUT / 'technical-report.json', report)
pub['live_publication_verified'] = True
pub['live_publication_verified_at'] = live['checked_at']
pub['latest_test_verification'] = tests
pub['technical_verification_report'] = REPORT
pub['historical_test_comparison_note'] = 'full_test_comparison preserves the original publication baseline and initial five failures; latest_test_verification records the repaired full-suite result.'
write_json(PUB, pub)

anchor = '# 10.11.2026 — Сцена 88: Саша. Даже слишком красиво'
done = ('Проверка публикации завершена: 4 оригинала, 4 превью, исходный референс Саши, мастер, manifest и галерея скачаны с сайта; все 12 SHA256 совпали. '
        f'Пять устаревших/ошибочных тестовых проверок исправлены, полный набор: {result.testsRun} тестов, 0 сбоев, 0 ошибок, 0 пропусков. '
        'Тексты сцен, изображения, очереди, приёмка и семь инструкций не изменены; видео и расходы 0.')
next_action = ('Техническая публикация сцены88 завершена и проверена; не создавать сцену, фотографии и промпты повторно. '
               'Художественная приёмка владельца отдельно. Видео не запускать без отдельного разрешения; Seedance P2 ждёт настоящий конец P1. Остальные исторические задачи этим этапом не закрыты.')
cp = Path('reports/current-work-checkpoint.md')
parts = re.split(r'(?m)(?=^# )', cp.read_text())
positions = [i for i, part in enumerate(parts) if part.splitlines() and part.splitlines()[0] == anchor]
assert len(positions) == 1, 'checkpoint anchor ambiguous'
parts[positions[0]] = anchor + '\n\nwork_id: ' + WORK + '\n\n- ' + done + '\n- Доказательство: ' + REPORT + '; run ' + os.environ['GITHUB_RUN_ID'] + '.\n- Следующий шаг: ' + next_action + '\n\nchecked_at: ' + now() + '\n\n---\n\n'
cp.write_text(''.join(parts))
capture('.', WORK, anchor, done, next_action, [REPORT, PUB, 'references/scenes/scene-88/manifest.json'], [REPORT, 'video-prompts.md', 'parodies.html'], True)
reg = json.loads(Path('work-resume-register.json').read_text())
work = next(w for w in reg['active_work'] if w['work_id'] == WORK)
work['status'] = 'awaiting_owner_review'
work['technical_publication_complete'] = True
work['last_result'] = done
if done not in work['completed']:
    work['completed'].append(done)
write_json('work-resume-register.json', reg)
plan = Path('ops/FUTURE-PLANS.md')
marker = '<!-- scene88-technical-verification-20261110 -->'
if marker not in plan.read_text():
    plan.write_text(plan.read_text().rstrip() + '\n\n' + marker + '\n- **10.11 — сцена88, техническая проверка: СДЕЛАНО.** ' + done + ' Доказательство `' + REPORT + '`.\n')
subprocess.run([sys.executable, 'scripts/build_resume_packet.py', '.', '--project', 'seregius'], check=True)
pre = subprocess.run([sys.executable, 'scripts/continue_preflight.py', '.', '--work-id', WORK], capture_output=True, text=True, check=True)
(OUT / 'continue-preflight-after.json').write_text(pre.stdout)
assert json.loads(pre.stdout)['ready_for_resume'], 'recovery packet invalid'
# Re-run in a clean process after checkpoint changes; do not publish a partial green result.
with (OUT / 'full-tests-after-checkpoint.log').open('w') as log:
    final = subprocess.run([sys.executable, '-m', 'unittest', 'discover', '-s', 'tests'], stdout=log, stderr=subprocess.STDOUT)
assert final.returncode == 0, 'tests failed after checkpoint update'
assert all(sha(p) == digest for p, digest in protected.items()), 'protected source changed'
lease()
allowed = set(EXPECTED) | {REPORT, PUB, 'reports/current-work-checkpoint.md', 'work-resume-register.json',
                          'ops/FUTURE-PLANS.md', 'shadow/resume-packet.md', 'shadow/resume-packet.json'}
changed = set(subprocess.check_output(['git', 'diff', '--name-only'], text=True).splitlines())
untracked = set(subprocess.check_output(['git', 'ls-files', '--others', '--exclude-standard'], text=True).splitlines())
assert changed | untracked <= allowed, 'unexpected changed paths: ' + repr((changed | untracked) - allowed)
subprocess.run(['git', 'add', '--', *sorted(allowed)], check=True)
print('VERIFIED', json.dumps({'tests': result.testsRun, 'live_files': len(rows), 'failures': 0, 'changed_paths': sorted(changed | untracked)}, ensure_ascii=False))
