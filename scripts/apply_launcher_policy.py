#!/usr/bin/env python3
"""Apply the owner's bounded 31-Oct launcher policy; never generate a video.

Used by a request-driven GitHub workflow, with an exact already-owned lease,
fresh checkout and non-force CAS push. No scheduler is installed here.
"""
import argparse
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

DOCS = ['NEW-CHAT-HANDOFF.md','SYNC-RUNBOOK.md','AI-PROJECT-GUIDE.md','PROMPT-STYLE-GUIDE.md',
        'USER-GUIDE.md','README-AI-SYNC.md','BACKUP-AI-RUNBOOK.md']
REPORT='reports/launcher-coordination-2026-10-31.json'
WORK='TOPVIEW-SLOT-PRIORITY-20261024'
LINK='> **31.10.2026 — согласованные исполнители и передача смены:** действующие роли, общий anti-duplicate и передача задачи по «Продолжай» — `ops/LAUNCHER-COORDINATION.md`; живой реестр — `ops/slot-backup.json`.\n'
CONTINUE='''## Передача ответственности за очередь · 31.10.2026

Команда «Продолжай» / «Прими смену» после приёма передаёт сменщику той же среды незавершённую задачу `TOPVIEW-SLOT-PRIORITY-20261024`. Прочитать `ops/slot-backup.json` и `ops/LAUNCHER-COORDINATION.md`, под собственной точной lease/CAS записать новый session_id и увеличить foreground epoch своей среды; прежний интерактивный чат после переключения — только чтение. Чужую действующую lease не отбирать; сначала сверить claims/task IDs. Никаких сбросов unknown, повторных Create или новых расписаний из-за смены разговора. Сохранить checkpoint/register и первый фактический шаг. Отдельные существующие scheduled исполнители остаются независимыми. Обычный ChatGPT основной при сообщённом исчерпании Work; возвращение Work — только по проверенному восстановлению, не по календарной догадке. Полный контракт, автоматическое взаимное подстраховывание и проверяемая замена фонового задания — профильный документ выше.

'''

def jread(root,path): return json.loads((root/path).read_text(encoding='utf-8'))
def jwrite(root,path,data):
    p=root/path; p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def nowz(): return datetime.now(timezone.utc).isoformat(timespec='seconds').replace('+00:00','Z')
def parse(s): return datetime.fromisoformat(s.replace('Z','+00:00'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def exact_lease(root,request):
    lock=jread(root,'ops/canon-lock.json')
    if (lock.get('state')!='held' or lock.get('holder')!=request['lease_holder'] or
        lock.get('acquired_at')!=request['lease_acquired_at'] or not lock.get('expires_at') or
        parse(lock['expires_at'])<=datetime.now(timezone.utc)):
        raise RuntimeError('Expected exact live lease is absent; do not apply stale request')
    return lock

def prepend_after_title(root,path,text):
    p=root/path; raw=p.read_bytes(); nl=b'\r\n' if b'\r\n' in raw else b'\n'
    insert=text.replace('\n',nl.decode()).encode('utf-8')
    if insert in raw: return
    pos=raw.find(nl)
    if pos<0: raise RuntimeError('No title line: '+path)
    p.write_bytes(raw[:pos+len(nl)]+nl+insert+raw[pos+len(nl):])

def checkpoint(root,request,phase):
    at=nowz(); marker='<!-- launcher-policy:'+request['request_id']+' -->'
    p=root/'reports/current-work-checkpoint.md'; old=p.read_text(encoding='utf-8')
    end='<!-- /launcher-policy -->'
    if marker in old:
        start=old.index(marker); finish=old.index(end,start)+len(end)
        tail=old[finish:]
        if tail.startswith('\n\n---\n\n'): tail=tail[len('\n\n---\n\n'):]
        old=old[:start]+tail.lstrip('\n')
    body=(marker+'\n# Обычный ChatGPT — основной; Work — резерв · 31.10.2026\n\n'
          +'work_id: '+WORK+'\n\n'
          +'Прямая команда владельца: Work-лимит исчерпан; обычный исполнитель основной, Work резервный; оба независимы, но отправка только под общим замком/claim. После доказанного восстановления Work вернуть предпочтение ему. «Продолжай» передаёт ответственность сменщику.\n\n'
          +'Стадия: '+phase+'. Время фактической записи: '+at+'. Технический план: общий реестр ролей, уникальная lease, одноразовый submitting intent, foreground epoch, согласованные инструкции/хендоф, cert и тесты. Очередь/мастер/видео не меняются.\n\n'
          +'Подтверждено до смены ролей: реальный обычный runtime 52f01b43-0358-8330-9c19-fb332e6dcb03 проверил 14 досок/18 страниц/624 видео, 6/6 занято; GUI-проба вернула originating_browser_context_required. Это не подтверждение Create или отдельной квоты. S72 от 11:08:48Z сохраняется как исторический подтверждённый запуск.\n\n'
          +'Следующий шаг: проверить реальную настройку трёх существующих задач и новый обычный runtime после сообщения владельца о лимите; при 6/6 только read-only GUI-проба, при свободном слоте полный preflight и первый готовый разрешённый пункт. Не повторять S72/unknown. Не объявлять страховку полностью принятой без browser/task evidence.\n\n'
          +'Источники: ops/slot-backup.json; ops/LAUNCHER-COORDINATION.md; '+REPORT+'.\n'+end+'\n\n---\n\n')
    p.write_text(body+old,encoding='utf-8')
    reg=jread(root,'work-resume-register.json')
    matches=[w for w in reg['active_work'] if w.get('work_id')==WORK]
    if len(matches)!=1: raise RuntimeError('Expected existing work must be unique')
    w=matches[0]
    w['updated_at']=at
    w['launcher_coordination']={'request_id':request['request_id'],'phase':phase,'registry':'ops/slot-backup.json',
                                'report':REPORT,'browser_launch_acceptance':'pending','quota_isolation':'unverified'}
    w['next_action']='Свежие роли/слоты/claims; обычный ChatGPT основной пока Work исчерпан. Проверить текущий реальный runtime и GUI. Запускать только готовое разрешённое при свободной ёмкости; unknown не повторять. Ответственность сменщика — ops/LAUNCHER-COORDINATION.md.'
    for link in ['ops/LAUNCHER-COORDINATION.md','ops/slot-backup.json',REPORT]:
        if link not in w.setdefault('canonical_refs',[]): w['canonical_refs'].append(link)
    recovery=w.get('recovery') or {}
    if recovery and recovery.get('launcher_request_id')!=request['request_id']:
        w.setdefault('recovery_history',[]).append(recovery)
    w['recovery']={'schema_version':1,'verified_at':at,'last_completed':phase,
                   'next_action':w['next_action'],'launcher_request_id':request['request_id'],
                   'checkpoint':{'file':'reports/current-work-checkpoint.md','anchor':'# Обычный ChatGPT — основной; Work — резерв · 31.10.2026','sha256':sha(p)},
                   'evidence':[], 'read_next':['ops/LAUNCHER-COORDINATION.md','ops/slot-backup.json'],
                   'blockers':['GUI отправка и независимость квоты не подтверждены']}
    reg['last_updated_at']=at
    jwrite(root,'work-resume-register.json',reg)

def apply(root,request):
    exact_lease(root,request)
    cfg=jread(root,'ops/slot-backup.json')
    if cfg.get('applied_owner_request_id')==request['request_id']: return
    if cfg.get('route_generation')!=request['expected_route_generation']:
        raise RuntimeError('Role changed since request; fresh review required')
    protected={p:sha(root/p) for p in ['video-prompts.md','ops/topview-launch-queue.json','monitor-role.json']}
    docs_before={p:sha(root/p) for p in DOCS}
    cfg.setdefault('role_history',[]).append({'at':nowz(),'previous_preferred_executor':cfg.get('preferred_executor','work'),
        'previous_route_generation':cfg['route_generation'],'previous_active_automation_id':cfg['active_automation_id'],
        'reason':'direct owner report: Work quota exhausted; ordinary ChatGPT primary'})
    cfg.update(role='coordinated_launchers',preferred_executor='ordinary',route_generation=cfg['route_generation']+1,
        applied_owner_request_id=request['request_id'],updated_at=nowz(),
        primary_automation_ids=[cfg['active_automation_id']],reserve_automation_ids=['6adc585e7ac08191bb93825117dc7213','6acae6ab433481919e88665c520b8ef2'],
        coordination_rules='ops/LAUNCHER-COORDINATION.md',coordination_guard='scripts/launcher_coordination.py',
        independent_wake=True,preferred_role_is_not_exclusive=True,wait_for_other_executor_failure_ack=False,
        work_capacity={'state':'exhausted','source':'direct_owner_report','reported_at':request['owner_reported_at'],
                       'platform_quota_independently_verified':False},
        owner_decision='31.10.2026: обычный ChatGPT основной пока лимит Work исчерпан; Work резерв. Оба независимо проверяют общую очередь/claims и подстраховывают друг друга. После доказанного восстановления вернуть Work предпочтение. Продолжай передаёт интерактивную ответственность сменщику.',
        restore_work_primary={'authorized_by_owner':True,'requires':'fresh direct owner confirmation OR verified Work runtime, GUI controls and available quota; never enabled/no_update/elapsed time','ordinary_schedule_stays_enabled':True},
        peers={'ordinary':{'enabled':True,'automation_ids':[cfg['active_automation_id']],'receipt':'reports/topview-slot-backup-cycle.json','handoff_to_work_allowed':False},
               'work':{'enabled':True,'automation_ids':['6adc585e7ac08191bb93825117dc7213','6acae6ab433481919e88665c520b8ef2'],
                       'receipts':['reports/topview-event-wake.json','reports/topview-launcher-cycle.json']}})
    cfg['ownership']['holder_template']='chatgpt:<ordinary|work>:<execution-instance-uuid>'
    cfg['takeover_condition']='Current authorized ready work and verified free global capacity, no valid competing lease. Both peers act independently; preferred role and prior success never reserve a free slot. Reconcile claims/unknown first.'
    owners=cfg.setdefault('foreground_owners',{})
    previous=owners.get('ordinary') or {}
    if previous: cfg.setdefault('foreground_owner_history',[]).append(dict(previous,surface='ordinary',retired_at=nowz()))
    owners['ordinary']={'session_id':request['interactive_session_id'],'epoch':int(previous.get('epoch',0))+1,
        'conversation_id':None,'conversation_id_unavailable_reason':'not_exposed_in_current_interactive_tools',
        'accepted_at':nowz(),'source':'direct_owner_role_transfer','work_id':WORK}
    cfg['chat_replacement']['ordinary_chat_switch']='After Continue intake, CAS-transfer this surface foreground session/epoch under an exact own lease; retire prior interactive writer only. Keep existing scheduled peers, queue, history and retry budgets.'
    cfg['rules']=list(dict.fromkeys(['ops/LAUNCHER-COORDINATION.md']+cfg.get('rules',[])))
    jwrite(root,'ops/slot-backup.json',cfg)
    for path in DOCS: prepend_after_title(root,path,LINK)
    prepend_after_title(root,'ops/CONTINUE-PROTOCOL.md',CONTINUE)
    for path in ['ops/CANON-LOCK.md','ops/TOPVIEW-EVENT-WAKE.md','ops/TOPVIEW-FREE-LAUNCH.md']:
        prepend_after_title(root,path,LINK)
    # One short dated handoff line; do not replace historical decisions or checkpoints.
    p=root/'NEW-CHAT-HANDOFF.md'; raw=p.read_bytes(); nl=b'\r\n' if b'\r\n' in raw else b'\n'
    text=raw.decode('utf-8')
    heading='### Новое с последней чистки (дописывать сюда, одной строкой с датой)'
    note='- 31.10: обычный ChatGPT основной при сообщённом исчерпании Work; независимые peer-запуски, общий claim и передача ответственности по «Продолжай» — `ops/LAUNCHER-COORDINATION.md`; приёмка GUI/квоты — в checkpoint.'
    if note not in text:
        if heading not in text: raise RuntimeError('Expected handoff insertion point absent')
        text=text.replace(heading,heading+nl.decode()+nl.decode()+note,1)
        text=text.replace('- Нет неразнесённых записей. Строки, очищенные 30.10, дословно сохранены в `archive/handoff-log.md`; действующее состояние — в профильных файлах выше.','- Строки, очищенные 30.10, сохранены в `archive/handoff-log.md`; действующее состояние — в профильных файлах.')
        text=text.replace('## СЕЙЧАС (обновлено 30.10.2026)','## СЕЙЧАС (обновлено 31.10.2026)',1)
        p.write_bytes(text.encode('utf-8'))
    # Add the new pure guard tests to the existing integration workflow, no extra schedule.
    p=root/'.github/workflows/test-recovery-integration.yml'; text=p.read_text()
    if "'scripts/launcher_coordination.py'" not in text:
        text=text.replace("      - 'tests/test_recovery_integration.py'", "      - 'scripts/launcher_coordination.py'\n      - 'tests/test_launcher_coordination.py'\n      - 'tests/test_recovery_integration.py'",1)
    if 'tests/test_launcher_coordination.py tests/test_recovery_integration.py' not in text:
        text=text.replace('python3 -m unittest -v tests/test_recovery_integration.py','python3 -m unittest -v tests/test_launcher_coordination.py tests/test_recovery_integration.py',1)
    p.write_text(text)
    checkpoint(root,request,'policy_written_validation_pending')
    after={p:sha(root/p) for p in protected}
    if protected!=after: raise RuntimeError('Protected master/queue/telemetry role unexpectedly changed')
    report={'schema_version':1,'project':'seregius','work_id':WORK,'record_type':'configuration_and_code_verification_not_runtime_receipt',
        'request_id':request['request_id'],'updated_at':nowz(),'stage':'policy_written_validation_pending',
        'preferred_executor':'ordinary','work_capacity_source':'owner_reported_exhausted',
        'independent_wake':True,'existing_schedules_retained':True,'new_schedules':0,'new_video_submissions':0,
        'route_generation':cfg['route_generation'],'docs_before':docs_before,'docs_after':{p:sha(root/p) for p in DOCS},
        'protected_files_unchanged':protected,'owner_decisions_checked_open_count':0,
        'prior_runtime_evidence':'reports/topview-slot-backup-cycle.json',
        'browser_create_verified':False,'quota_isolation_verified':False,
        'remaining':['verify actual three automation prompts/readback','new ordinary runtime after owner quota report','authorized GUI control/import and necessary zero-credit Create','verified Work recovery before return of preference']}
    jwrite(root,REPORT,report)

def finish(root,request):
    exact_lease(root,request)
    report=jread(root,REPORT)
    if report.get('request_id')!=request['request_id']: raise RuntimeError('Wrong report request')
    report.update(stage='code_and_documents_validated',updated_at=nowz(),
        validation=['cert_github.py','unittest discover -s tests','validate_site.py','check_instruction_consistency.py'],
        github_run_id=request.get('github_run_id'),github_run_url=request.get('github_run_url'))
    jwrite(root,REPORT,report)
    checkpoint(root,request,'code_and_documents_validated; automation_and_GUI_acceptance_separate')

def release(root,request):
    lock=jread(root,'ops/canon-lock.json')
    if lock.get('holder')!=request['lease_holder'] or lock.get('acquired_at')!=request['lease_acquired_at']:
        raise RuntimeError('Foreign replacement lease; not released')
    lock.update(state='free',expires_at=None,released_at=nowz())
    jwrite(root,'ops/canon-lock.json',lock)

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('root',type=Path); ap.add_argument('phase',choices=['checkpoint','apply','finish','release','check-lease'])
    args=ap.parse_args(); request=jread(args.root,'ops/launcher-policy-request.json')
    if request['action']!='ordinary-primary-after-owner-work-limit': raise RuntimeError('Unsupported owner request')
    if args.phase=='release': release(args.root,request); return
    exact_lease(args.root,request)
    if args.phase=='check-lease': return
    if args.phase=='checkpoint': checkpoint(args.root,request,'plan_saved_before_policy_change')
    elif args.phase=='apply': apply(args.root,request)
    else: finish(args.root,request)

if __name__=='__main__': main()
