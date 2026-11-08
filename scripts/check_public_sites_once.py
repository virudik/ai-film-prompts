#!/usr/bin/env python3
"""Read-only TLS/HTTP probes of the owner's exact public sites, then bounded publication."""
import concurrent.futures
import hashlib
import http.client
import json
import re
import socket
import ssl
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
ROOT = Path.cwd()
sys.path.insert(0, str(ROOT/'scripts'))
from resume_state import capture, verify_recovery, select_work
from build_resume_packet import write as packet_write
HOLDER = 'chatgpt:ordinary:50d733e4-1083-4c07-98a3-02631f519bc4'
ACQUIRED = '2026-11-08T06:16:57Z'
REPORT = 'reports/public-sites-check-2026-11-08.json'
CP = 'reports/current-work-checkpoint.md'
REG = 'work-resume-register.json'
PLAN = 'ops/FUTURE-PLANS.md'
WORK = 'TOPVIEW-SLOT-PRIORITY-20261024'
ANCHOR = '# 08.11.2026 — прямая проверка TLS семейных поддоменов'
FILES = ['scripts/check_public_sites_once.py', '.github/workflows/check-public-sites-once.yml']
LABELS = ['алина','маша','виталик','видео','фото','работа','мои-видео','обо-мне']

def now(): return datetime.now(timezone.utc).isoformat(timespec='seconds').replace('+00:00','Z')
def read(p): return json.loads((ROOT/p).read_text(encoding='utf-8-sig'))
def save(p,d): (ROOT/p).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def check(release=False):
    x=read('ops/canon-lock.json')
    own=x.get('holder')==HOLDER and x.get('acquired_at')==ACQUIRED and x.get('state')=='held'
    if release: return own
    if not own or datetime.fromisoformat(x['expires_at'].replace('Z','+00:00'))<=datetime.now(timezone.utc): raise RuntimeError('Exact active lease lost')
    c=read('ops/slot-backup.json'); f=c['foreground_owners']['ordinary']
    if c['route_generation']!=3 or f['epoch']!=4 or f['session_id']!='chatgpt-ordinary-continue-20261107-4aa338af-9488-4a37-a1c3-60993ed108ec': raise RuntimeError('Foreground owner changed')

def free():
    if check(True):
        x=read('ops/canon-lock.json'); x.update(state='free',expires_at=None,released_at=now()); save('ops/canon-lock.json',x)

def probe(label):
    display=(label+'.' if label else '')+'рудик.рф'; host=display.encode('idna').decode('ascii')
    out={'domain':display,'hostname_ascii':host,'checked_at':now(),'tls_verified':False,'https_ok':False}
    try:
        out['dns_addresses']=sorted({x[4][0] for x in socket.getaddrinfo(host,443,type=socket.SOCK_STREAM)})
        with socket.create_connection((host,443),timeout=15) as plain:
            with ssl.create_default_context().wrap_socket(plain,server_hostname=host) as tls:
                cert=tls.getpeercert(); der=tls.getpeercert(binary_form=True)
                out.update(tls_verified=True,tls_version=tls.version(),peer_ip=tls.getpeername()[0],certificate_sha256=hashlib.sha256(der).hexdigest(),certificate=cert)
        conn=http.client.HTTPSConnection(host,timeout=20,context=ssl.create_default_context())
        try:
            conn.request('GET','/',headers={'User-Agent':'AI-Film-owner-read-only-verification/1.0'})
            response=conn.getresponse(); body=response.read(65536).decode('utf-8','replace')
            out['http']={'status':response.status,'server':response.getheader('Server'),'location':response.getheader('Location'),'body_prefix_sha256':hashlib.sha256(body.encode()).hexdigest(),'title':re.findall(r'<title[^>]*>(.*?)</title>',body,re.S|re.I)[:1],'refresh':re.findall(r'<meta[^>]+http-equiv=[^>]+>',body,re.I)[:2]}
            out['https_ok']=200<=response.status<400
        finally: conn.close()
    except Exception as e:
        out['error']={'type':type(e).__name__,'message':str(e)[:1200]}
        if isinstance(e,ssl.SSLCertVerificationError):
            out['error']['verify_code']=e.verify_code
            out['error']['verify_message']=e.verify_message
            try:
                ctx=ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT);ctx.check_hostname=False;ctx.verify_mode=ssl.CERT_NONE
                with socket.create_connection((host,443),timeout=10) as plain:
                    with ctx.wrap_socket(plain,server_hostname=host) as sock:
                        der=sock.getpeercert(binary_form=True)
                        p=subprocess.run(['openssl','x509','-inform','DER','-noout','-subject','-issuer','-dates','-ext','subjectAltName'],input=der,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=10)
                        out['untrusted_leaf_diagnostic']={'verified':False,'description':p.stdout.decode('utf-8','replace'),'sha256':hashlib.sha256(der).hexdigest()}
            except Exception as diagnostic_error: out['untrusted_leaf_diagnostic']={'verified':False,'error':str(diagnostic_error)[:400]}
    return out

def update_row(text,key,value,index=3):
    lines=text.splitlines();matches=[i for i,s in enumerate(lines) if s.startswith('| '+key+' |')]
    if len(matches)!=1:raise RuntimeError('Plan row missing/ambiguous '+key)
    parts=lines[matches[0]].split('|');parts[index]=' '+value.replace('|','/')+' ';lines[matches[0]]='|'.join(parts)
    return '\n'.join(lines)+'\n'

phase=sys.argv[1]
if phase=='release':free();raise SystemExit(0)
check()
if phase=='probe':
    result={'schema_version':1,'project':'seregius','scope':'Direct default-CA-verified TLS socket/SNI and HTTP GET from GitHub runner; no DNS/Pages configuration changes, no login or generation.','started_at':now()}
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool: values=list(pool.map(probe,LABELS+['','ии','промты']))
    result['subdomains']=values[:8];result['controls']=values[8:];result['tls_verified_count']=sum(x['tls_verified'] for x in values[:8]);result['https_ok_count']=sum(x['https_ok'] for x in values[:8]);result['finished_at']=now()
    Path('/tmp/public-sites-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result,ensure_ascii=False,indent=2));raise SystemExit(0)
if phase!='publish':raise RuntimeError('Unknown phase')
result=json.loads(Path('/tmp/public-sites-result.json').read_text())
if (ROOT/REPORT).exists(): raise RuntimeError('Existing report: inspect rather than duplicate')
reg=read(REG);w=select_work(reg,project='seregius')
if w['work_id']!=WORK:raise RuntimeError('Focus changed')
if w['recovery']['checkpoint']['anchor']!='# 08.11.2026 — опубликована актуальная точка продолжения':raise RuntimeError('Newer recovery stage exists; recompute')
result['source_head']=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
result['previous_checkpoint']=w['recovery']['checkpoint']
result['all_8_certificates_and_http_verified']=result['tls_verified_count']==8 and result['https_ok_count']==8
save(REPORT,result)
n=result['tls_verified_count'];m=result['https_ok_count'];summary=f'Прямой TLS с проверкой доверенной цепочки и имени: {n}/8 сертификатов подтверждено, HTTP 2xx/3xx: {m}/8. Результаты и ошибки каждого адреса: {REPORT}. DNS и настройки Pages не менялись.'
next_action=w['next_action']
if n==8 and m==8:next_action=next_action.replace('проверку TLS восьми поддоменов и воспроизведения Rutube','проверку воспроизведения Rutube (TLS восьми поддоменов подтверждён 08.11)')
block=ANCHOR+'\n\nwork_id: '+WORK+'\n\n- '+summary+'\n- Исправление recovery уже опубликовано; пауза Keep сохранена. QR/DOM-проверки не выполнялись заново.\n- Следующий шаг: '+next_action+'\n\nchecked_at: '+result['finished_at']+'\n\n---\n\n'
cp=(ROOT/CP).read_text(encoding='utf-8')
if ANCHOR in cp:raise RuntimeError('Checkpoint already exists')
(ROOT/CP).write_text(block+cp,encoding='utf-8')
plans=(ROOT/PLAN).read_text(encoding='utf-8')
state=('СДЕЛАНО — ' if n==8 and m==8 else 'НЕ ЗАКРЫТО — ')+summary
plans=update_row(plans,'A-20',state)
plans=update_row(plans,'G-05',state,index=4)
(ROOT/PLAN).write_text(plans,encoding='utf-8')
capture(ROOT,WORK,ANCHOR,summary,next_action,[REPORT,'reports/continuation-publication-2026-11-08.json','reports/continuation-qc-2026-11-08.json'],['ops/TOPVIEW-FREE-LAUNCH.md','projects/raznoe/HANDOFF.md'])
reg=read(REG);reg['resume_focus']['next_action']=next_action;reg['resume_focus']['updated_at']=reg['last_updated_at'];save(REG,reg)
assert not verify_recovery(ROOT,reg,project='seregius')['reasons']
p=packet_write(ROOT,project='seregius')
assert p['ready_for_resume'] and not p['reasons']
subprocess.run(['python3','scripts/validate_site.py','.'],check=True)
check();free()
for p in FILES:(ROOT/p).unlink(missing_ok=True)
print(summary)
