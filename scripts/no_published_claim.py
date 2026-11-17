#!/usr/bin/env python3
"""Read-only historical assessment. Never authorizes a new session or Create."""
import hashlib
import json
import subprocess
from pathlib import Path
SOURCE_SHA = '9eb35e9e0555c91c2d81d28bc9a85b0a4e7dff5e10db8124db8253bd322b4aa0'
QUEUE = 'ops/topview-launch-queue.json'
class EvidenceError(ValueError): pass

def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest()

def check_snapshot(item, expected_sha):
    if digest(item) == expected_sha or item.get('claim') or item.get('task_id') or item.get('task_ids') or item.get('submission_intent_id'):
        raise EvidenceError('published_or_ambiguous_claim')
    if item.get('state') not in ('waiting_for_slot', 'blocked_recovery'):
        raise EvidenceError('item_not_unconsumed')
    if any(item.get(k) for k in ('submission_history', 'create_click_count', 'max_new_submissions_consumed', 'retry_control', 'submission_attempts', 'archived_attempts')):
        raise EvidenceError('prior_attempt_requires_separate_reconciliation')

def assess(repo, session, prepared, end):
    def git(*args):
        return subprocess.check_output(['git','-C',str(repo),*args], stderr=subprocess.PIPE).decode().strip()
    if session.get('schema_version') != 1 or session.get('phase') != 'claim_prepared':
        raise EvidenceError('original_claim_prepared_session_required')
    if prepared.get('phase') != 'claim' or prepared.get('create_allowed') is not False:
        raise EvidenceError('original_prepared_claim_required')
    base = prepared.get('expected_main_sha')
    for ref in (base, end):
        if not isinstance(ref,str) or len(ref)!=40 or any(c not in '0123456789abcdef' for c in ref):
            raise EvidenceError('full_immutable_commit_required')
    git('merge-base','--is-ancestor',base,end)
    source = subprocess.check_output(['git','-C',str(repo),'show',base+':scripts/launcher_entry.py'])
    if hashlib.sha256(source).hexdigest()!=SOURCE_SHA:
        raise EvidenceError('reviewed_source_required')
    items = prepared.get('files',{}).get(QUEUE,{}).get('items',[])
    rows=[i for i in items if i.get('id')==session.get('item_id')]
    if len(rows)!=1 or digest(rows[0])!=session.get('expected_item_sha') or rows[0].get('claim',{}).get('claim_id')!=session.get('claim_id'):
        raise EvidenceError('prepared_payload_binding_required')
    commits=[base]+git('rev-list','--reverse','--ancestry-path',base+'..'+end).splitlines()
    shallow = Path(git('rev-parse','--git-path','shallow'))
    if not shallow.is_absolute(): shallow=Path(repo)/shallow
    if shallow.exists() and set(shallow.read_text().splitlines()).intersection(commits[1:]):
        raise EvidenceError('bounded_history_truncated')
    digests=set()
    for commit in commits:
        queue=json.loads(git('show',commit+':'+QUEUE))
        matches=[i for i in queue.get('items',[])+queue.get('archived_items',[]) if i.get('id')==session['item_id']]
        if len(matches)!=1: raise EvidenceError('unique_continuous_item_required')
        check_snapshot(matches[0],session['expected_item_sha']);digests.add(digest(matches[0]))
    return {'assessment':'no_expected_claim_in_retained_ancestry','base':base,'end':end,'commit_count':len(commits),'item_id':session['item_id'],'expected_claim_sha256':session['expected_item_sha'],'observed_item_sha256':sorted(digests),'reviewed_source_sha256':SOURCE_SHA,'python_exit_code_observed':None,'original_command_id':None,'create_allowed':False,'new_session_allowed_by_this_report':False,'limitations':['Retained Git ancestry only; no proof against rewritten or unobserved refs.','Conditional on the reviewed source being the actual unmodified executor; source binding and cessation require independent review.','No conclusion about manual/out-of-protocol provider actions; fresh live reconciliation remains mandatory.']}
