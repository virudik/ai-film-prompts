#!/usr/bin/env python3
"""One owner-authorized publication, exact lease only; no schedule or generation.
Temporary runner helper. Recompute from fresh main after a rejected push.
"""
import copy
import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT / 'scripts'))
from resume_state import capture, verify_recovery, select_work
from build_resume_packet import write as build_packet

HOLDER = 'chatgpt:ordinary:89a9e9de-45a6-4fd0-9ddd-12b9e0f9ab5b'
ACQUIRED = '2026-11-08T06:00:26Z'
SESSION = 'chatgpt-ordinary-continue-20261107-4aa338af-9488-4a37-a1c3-60993ed108ec'
WORK = 'TOPVIEW-SLOT-PRIORITY-20261024'
REGISTER = 'work-resume-register.json'
CHECKPOINT = 'reports/current-work-checkpoint.md'
PLANS = 'ops/FUTURE-PLANS.md'
REPORT = 'reports/continuation-publication-2026-11-08.json'
QC = 'reports/continuation-qc-2026-11-08.json'
ANCHOR = '# 08.11.2026 — опубликована актуальная точка продолжения'
PLAN_ANCHOR = '# 08.11.2026 — план публикации исправления recovery'
SELF_PATHS = ['scripts/publish_continuation_once.py', '.github/workflows/publish-continuation-repair.yml']
NEXT = ('При свободном слоте выполнить новый полный скан всех досок и сверку claims/task ID, затем взять готовый разрешённый item по живому priority; только Unlimited 0 и собственный CAS. Уже отправленное не повторять. Google Keep отложен по P-14 до новой отдельной команды. Продолжить продуктовые PNG HONOR, QC RESOURCE и настоящих стыков S52/S60/S61, проверку TLS восьми поддоменов и воспроизведения Rutube. Существующие инструкции Саше и визитки не создавать заново; цифровой QR проверен, печатная и художественная приёмка открыты.')
LAST = ('Опубликована привязка recovery к актуальному подтверждённому этапу вместо 06.11; пауза Keep сохранена. Сохранены результаты 14/14 локальных DOM-тестов обработчика ИИшницы от 07.11 (не проверка живого MP4 на телефоне) и повторного чтения QR/сверки SHA двух существующих PNG от 08.11. Очередь, рендеры, расписания и телеметрия не изменялись.')

def stamp():
    return datetime.now(timezone.utc).isoformat(timespec='seconds').replace('+00:00', 'Z')

def load(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8-sig'))

def save(path, obj):
    (ROOT / path).parent.mkdir(parents=True, exist_ok=True)
    (ROOT / path).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def git(*args):
    return subprocess.check_output(['git', *args], text=True).strip()

def lease(release=False):
    lock = load('ops/canon-lock.json')
    same = lock.get('holder') == HOLDER and lock.get('acquired_at') == ACQUIRED and lock.get('state') == 'held'
    if release:
        return same
    if not same or datetime.fromisoformat(lock['expires_at'].replace('Z', '+00:00')) <= datetime.now(timezone.utc):
        raise RuntimeError('Exact active owner lease is required')
    cfg = load('ops/slot-backup.json')
    fg = cfg['foreground_owners']['ordinary']
    if cfg['route_generation'] != 3 or fg['session_id'] != SESSION or fg['epoch'] != 4:
        raise RuntimeError('Interactive owner or route changed')
    if not cfg['peers']['ordinary']['enabled']:
        raise RuntimeError('Peer disabled')
    return True

def row(text, key, status):
    lines = text.splitlines()
    ix = [i for i, line in enumerate(lines) if line.startswith('| ' + key + ' |')]
    if len(ix) != 1:
        raise RuntimeError('Missing/ambiguous plan row ' + key)
    cells = lines[ix[0]].split('|')
    if len(cells) != 6:
        raise RuntimeError('Unexpected plan row shape ' + key)
    cells[3] = ' ' + status + ' '
    lines[ix[0]] = '|'.join(cells)
    return '\n'.join(lines) + '\n'

def verify_binding():
    reg = load(REGISTER)
    result = verify_recovery(ROOT, reg, project='seregius')
    if result['reasons']:
        raise RuntimeError(result['reasons'])
    selected = result['selected_work']
    if selected['next_action'] != NEXT or selected['checkpoint']['anchor'] != ANCHOR:
        raise RuntimeError('Wrong recovery target')
    return result

def capture_now():
    capture(ROOT, WORK, ANCHOR, LAST, NEXT, [REPORT, QC], ['ops/TOPVIEW-FREE-LAUNCH.md', 'projects/raznoe/HANDOFF.md'])
    reg = load(REGISTER)
    reg['resume_focus']['next_action'] = NEXT
    reg['resume_focus']['updated_at'] = reg['last_updated_at']
    save(REGISTER, reg)
    verify_binding()

phase = sys.argv[1]
if phase == 'release':
    if lease(release=True):
        lock = load('ops/canon-lock.json')
        lock.update(state='free', expires_at=None, released_at=stamp())
        save('ops/canon-lock.json', lock)
    raise SystemExit(0)
lease()
reg = load(REGISTER)
w = select_work(reg, project='seregius')
if w['work_id'] != WORK:
    raise RuntimeError('Work focus changed')
if phase == 'plan':
    if (ROOT / REPORT).exists():
        report = load(REPORT)
        if report.get('holder') != HOLDER:
            raise RuntimeError('Report belongs to another execution')
        raise SystemExit(0)
    old = w.get('recovery', {})
    if old.get('checkpoint', {}).get('anchor') != '# 06.11.2026 — общий Images проверен, ссылка руководства Саше исправлена':
        raise RuntimeError('Recovery already changed; do not replay old repair')
    qc = load(QC)
    if qc['handler_tests']['passed'] != 14 or not all(x['sha_match'] for x in qc['assets']['checks']):
        raise RuntimeError('QC evidence failed')
    report = {'schema_version': 1, 'project': 'seregius', 'work_id': WORK, 'holder': HOLDER,
              'owner_request': 'Опкбликовывай, доделывай недоделанное', 'stage': 'planned_not_completed',
              'started_at': stamp(), 'source_head': git('rev-parse', 'HEAD'), 'previous_recovery': old,
              'scope': 'Publish existing QC and use canonical resume_state.capture; no new monitors, scenes or permission changes.'}
    save(REPORT, report)
    block = PLAN_ANCHOR + '\n\nwork_id: ' + WORK + '\n\nПлан, НЕ результат: опубликовать сохранённые QC, привязать recovery штатным capture, сохранить паузу Keep, проверить тесты и пакет; очередь/расписания не менять. Доказательства и прежняя привязка: ' + REPORT + '.\n\nchecked_at: ' + stamp() + '\n\n---\n\n'
    oldcp = (ROOT / CHECKPOINT).read_text(encoding='utf-8')
    if PLAN_ANCHOR in oldcp:
        raise RuntimeError('Duplicate initial checkpoint')
    (ROOT / CHECKPOINT).write_text(block + oldcp, encoding='utf-8')
    w['publication_plan'] = {'report': REPORT, 'checkpoint_anchor': PLAN_ANCHOR, 'status': 'planned_not_completed'}
    save(REGISTER, reg)
    raise SystemExit(0)
if phase != 'apply':
    raise RuntimeError('Unknown phase')
report = load(REPORT)
if report.get('stage') == 'validated_for_publication':
    verify_binding()
    raise SystemExit(0)
if report['holder'] != HOLDER or w['recovery'] != report['previous_recovery']:
    raise RuntimeError('Another writer changed recovery')
base_reg = copy.deepcopy(reg)
protected = ['video-prompts.md', 'ops/topview-launch-queue.json', 'topview-status.json', 'monitor-role.json', 'ops/slot-backup.json', 'automation-monitor-status.json']
protected_hash = {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in protected}
report['stage'] = 'validating_not_yet_published'
report['recomputed_from_head'] = git('rev-parse', 'HEAD')
report['prior_unavailable_write_claim_corrected'] = 'GitHub write permission and update_file operation confirmed in current execution.'
report['preserved_source_sha256'] = protected_hash
save(REPORT, report)
cp = (ROOT / CHECKPOINT).read_text(encoding='utf-8')
if ANCHOR in cp:
    raise RuntimeError('Final checkpoint already exists; inspect it')
block = ANCHOR + '\n\nwork_id: ' + WORK + '\n\n- ' + LAST + '\n- Доказательства и границы проверок: ' + REPORT + '; ' + QC + '.\n- Следующий шаг: ' + NEXT + '\n\nchecked_at: ' + stamp() + '\n\n---\n\n'
(ROOT / CHECKPOINT).write_text(block + cp, encoding='utf-8')
w.pop('publication_plan', None)
save(REGISTER, reg)
plans = (ROOT / PLANS).read_text(encoding='utf-8')
plans = row(plans, 'A-01', 'Протокол действует; 08.11 recovery привязан к актуальному этапу через штатный capture, Keep остаётся отложен; доказательство reports/continuation-publication-2026-11-08.json')
plans = row(plans, 'A-18', 'КОД ОПУБЛИКОВАН; сохранены 14/14 локальных Chromium DOM-тестов обработчика от 07.11; живое воспроизведение на Android/Safari ОТКРЫТО')
plans = row(plans, 'A-24', 'Существующие PNG/PDF/ZIP сохранены. 08.11 RUDIK_06: SHA совпал, QR фактически прочитан в оригинале и цифровом 90×50 мм/300 dpi; физический оттиск и художественная приёмка ОТКРЫТЫ')
plans = row(plans, 'A-25', 'ЧАСТИЧНО: цифровой QR RUDIK_06 проверен 08.11; точное сходство, логотипы и финальная художественная приёмка владельцем ещё не подтверждены')
(ROOT / PLANS).write_text(plans, encoding='utf-8')
capture_now()
commands = [
 ['python3', '-m', 'unittest', '-v', 'tests.test_continue_preflight', 'tests.test_continue_recovery', 'tests.test_project_recovery', 'tests.test_recovery_integration'],
 ['node', 'tests/continue_status_check.js'],
 ['python3', 'scripts/check_instruction_consistency.py', '.'],
 ['python3', 'scripts/validate_site.py', '.'],
]
checks = []
for cmd in commands:
    p = subprocess.run(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print(p.stdout)
    checks.append({'command': cmd, 'exit_code': p.returncode, 'output_tail': p.stdout[-1500:]})
    if p.returncode:
        raise RuntimeError('Validation failed: ' + ' '.join(cmd))
report['validation'] = checks
report['stage'] = 'validated_for_publication'
report['validated_at'] = stamp()
report['no_generation_or_schedule_changes'] = True
save(REPORT, report)
capture_now()
reg_after = load(REGISTER)
work_after = select_work(reg_after, project='seregius')
for name, data in protected_hash.items():
    if hashlib.sha256((ROOT / name).read_bytes()).hexdigest() != data:
        raise RuntimeError('Protected source changed: ' + name)
for a, b in zip(base_reg['active_work'], reg_after['active_work']):
    if a['work_id'] != WORK and a != b:
        raise RuntimeError('Unrelated active work changed')
for key in base_reg:
    if key not in {'active_work', 'resume_focus', 'last_updated_at'} and base_reg[key] != reg_after[key]:
        raise RuntimeError('Unrelated register data changed: ' + key)
packet = build_packet(ROOT, project='seregius')
if packet['reasons'] or not packet['ready_for_resume'] or packet['selected_work']['next_action'] != NEXT:
    raise RuntimeError('Generated packet is not current and ready: ' + str(packet['reasons']))
lease()
lock = load('ops/canon-lock.json')
lock.update(state='free', expires_at=None, released_at=stamp())
save('ops/canon-lock.json', lock)
for path in SELF_PATHS:
    (ROOT / path).unlink(missing_ok=True)
print('Verified recovery binding and packet; ready for one fresh-main CAS commit. Temporary publisher removed.')
