"""Grok is told about a changed warn/fail set, not about unchanged info notes."""
import json
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import site_alerts  # noqa: E402


NOW = datetime(2026, 11, 10, 1, 50, tzinfo=timezone.utc)


def write(root, rel, data):
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")


class AlertTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / "ops").mkdir()
        (self.root / "ops" / "relay-wake.json").write_text(json.dumps({
            "enabled": True, "api_base": "https://cast.agentrelay.com/v1",
            "address": "chatgpt@example", "site_alert_enabled": True,
            "site_alert_address": "chatgpt@example", "site_alert_routing": {"mode":"dot_then_grok", "backup_address":"GrokBot@example"}}), encoding="utf-8")
        self.sent = []

    def sender(self, text, **kwargs):
        self.sent.append(text)
        return "sent", "message_id=1"

    def base(self, **extra):
        checked = (NOW - timedelta(minutes=10)).strftime("%Y-%m-%dT%H:%M:%SZ")
        write(self.root, "topview-status.json", {"checked_at": checked, "occupied_slots": 6, "free_slots": 0})
        write(self.root, "automation-monitor-status.json", {
            "last_scheduled_cycle": {"completed_at": checked, "health": "ok", "note": "ok"}})
        write(self.root, "project-status.json", {"health": "ok"})
        write(self.root, "instruction-sync-status.json", {"health": "ok"})
        write(self.root, "canon-health.json", extra.get("health") or {"problems": []})

    def test_info_notes_do_not_notify_and_the_same_warn_does_not_repeat(self):
        self.base(health={"problems": [
            {"level": "info", "code": "ops-stale", "file": "ops/X.md", "text": "воскресная чистка"},
            {"level": "warn", "code": "handoff-size", "file": "NEW-CHAT-HANDOFF.md", "text": "Хендоф 35 КБ"},
        ]})
        first = site_alerts.notify(self.root, NOW, self.sender)
        self.assertEqual(first["action"], "sent")
        self.assertEqual(len(self.sent), 1)
        self.assertIn("handoff-size", self.sent[0])
        self.assertNotIn("воскресная чистка", self.sent[0])
        again = site_alerts.notify(self.root, NOW, self.sender)
        self.assertEqual((again["action"], len(self.sent)), ("unchanged", 1))

    def test_stale_topview_is_one_stable_banner_and_a_fresh_file_clears_it(self):
        self.base()
        old = (NOW - timedelta(hours=10)).strftime("%Y-%m-%dT%H:%M:%SZ")
        write(self.root, "topview-status.json", {"checked_at": old})
        self.assertEqual(site_alerts.notify(self.root, NOW, self.sender)["action"], "sent")
        self.assertIn("ДАННЫЕ TOPVIEW УСТАРЕЛИ", self.sent[0])
        later = NOW + timedelta(minutes=30)
        write(self.root, "topview-status.json", {"checked_at": later.strftime("%Y-%m-%dT%H:%M:%SZ")})
        # Same stale condition five minutes later must not be a new set.
        self.sent.clear()
        write(self.root, "topview-status.json", {"checked_at": old})
        self.assertEqual(site_alerts.notify(self.root, later, self.sender)["action"], "unchanged")
        fresh = (later - timedelta(minutes=5)).strftime("%Y-%m-%dT%H:%M:%SZ")
        write(self.root, "topview-status.json", {"checked_at": fresh})
        self.assertEqual(site_alerts.notify(self.root, later, self.sender)["action"], "cleared")
        self.assertEqual(self.sent, [])

    def test_a_failed_delivery_does_not_count_as_sent(self):
        self.base(health={"problems": [{"level": "warn", "code": "handoff-size", "file": "H.md", "text": "большой"}]})
        result = site_alerts.notify(self.root, NOW, lambda text, **kwargs: ("no_token", "secret AGENT_RELAY_TOKEN is not set"))
        self.assertEqual(result["action"], "no_token")
        self.assertNotEqual(site_alerts.load_state(self.root)["primary"]["status"], "sent")


class NavDefaultTests(unittest.TestCase):
    def test_phone_filters_start_open_and_can_still_collapse(self):
        html = Path(__file__).resolve().parents[1].joinpath("index.html").read_text(encoding="utf-8")
        self.assertIn('class="side side-open"', html)
        self.assertIn('aria-expanded="true"', html)
        self.assertIn("✕ Скрыть фильтры и оглавление", html)
        media = html.split("@media(max-width:820px)", 1)[1].split("@media", 1)[0]
        self.assertIn(".side:not(.side-open) #filters", media)
        self.assertIn(".side:not(.side-open) #toc", media)
        self.assertLess(html.find(".side-toggle{display:none}"), html.find("@media(max-width:820px)"))

    def test_unmapped_slot_is_not_rendered_as_scene_zero(self):
        html = Path(__file__).resolve().parents[1].joinpath("index.html").read_text(encoding="utf-8")
        now = html.split("function renderNowView", 1)[1].split("function instructionLabel", 1)[0]
        finished = html.split("function finishedTopviewRows", 1)[1].split("function renderTopview", 1)[0]
        self.assertIn("sceneNum(x)", now)
        self.assertIn("слот без сцены", now)
        self.assertIn("id==null", now)
        self.assertNotIn("Number(x.scene_id)", now)
        self.assertNotIn("#scene-0", now)
        self.assertIn("sceneNum", finished)
        self.assertNotIn("Number(x.scene_id)", finished)



class RoutingTests(AlertTests):
    def warning(self, level='warn'):
        self.base(health={'problems':[{'level':level,'code':'test','file':'x','text':'problem'}]})
    def refresh(self, now):
        write(self.root,'topview-status.json',{'checked_at':now.isoformat()})
        write(self.root,'automation-monitor-status.json',{'last_scheduled_cycle':{'health':'ok','completed_at':now.isoformat()}})
    def call(self, now):
        self.refresh(now)
        return site_alerts.notify(self.root,now,self.sender)
    def test_dot_first_warning_backup_at_two_hours_once(self):
        self.warning();self.assertEqual(self.call(NOW)['target'],'primary')
        self.assertEqual(self.call(NOW+timedelta(minutes=119))['action'],'unchanged')
        self.assertEqual(self.call(NOW+timedelta(minutes=120))['target'],'backup')
        self.assertEqual(self.call(NOW+timedelta(minutes=240))['action'],'unchanged')
    def test_critical_at_thirty_minutes(self):
        self.warning('error');self.call(NOW)
        self.assertEqual(self.call(NOW+timedelta(minutes=29))['action'],'unchanged')
        self.assertEqual(self.call(NOW+timedelta(minutes=30))['target'],'backup')
    def test_real_progress_postpones_but_stale_commit_does_not(self):
        self.warning('fail');first=self.call(NOW)
        write(self.root,site_alerts.RECEIPTS,{'events':[{'incident_id':first['incident_id'],'actor':'dot',
            'state':'in_progress','updated_at':(NOW+timedelta(minutes=20)).isoformat(),'evidence':'checked current file'}]})
        self.assertEqual(self.call(NOW+timedelta(minutes=30))['action'],'unchanged')
        self.assertEqual(self.call(NOW+timedelta(minutes=50))['target'],'backup')
    def test_wrong_future_naive_or_preincident_ack_ignored(self):
        for delta, incident, naive in ((20,'wrong',False),(1000,None,False),(-1,None,False),(20,None,True)):
            with self.subTest(delta=delta,incident=incident,naive=naive):
                (self.root/site_alerts.STATE).unlink(missing_ok=True)
                self.warning('error');first=self.call(NOW)
                t=NOW+timedelta(minutes=delta)
                write(self.root,site_alerts.RECEIPTS,{'events':[{'incident_id':incident or first['incident_id'],
                    'actor':'dot','state':'in_progress','evidence':'observed',
                    'updated_at':(t.replace(tzinfo=None) if naive else t).isoformat()}]})
                self.assertEqual(self.call(NOW+timedelta(minutes=30))['target'],'backup')
    def test_resolved_then_recurrent_gets_new_incident(self):
        self.warning();first=self.call(NOW)['incident_id']
        self.base();self.call(NOW)
        self.warning();second=self.call(NOW)['incident_id']
        self.assertNotEqual(first,second)
    def test_legacy_grok_sent_does_not_suppress_new_dot_route(self):
        self.warning();sig=site_alerts.signature(site_alerts.collect(self.root,NOW))
        write(self.root,site_alerts.STATE,{'schema_version':1,'signature':sig,'relay':{'status':'sent'}})
        self.assertEqual(self.call(NOW)['target'],'primary')
    def test_failed_send_preserves_timer_and_retries(self):
        self.warning('error')
        def failed(*args,**kwargs):return ('error','transport unavailable')
        site_alerts.notify(self.root,NOW,failed)
        first=site_alerts.load_state(self.root)['first_seen_at']
        site_alerts.notify(self.root,NOW+timedelta(minutes=1),failed)
        self.assertEqual(site_alerts.load_state(self.root)['first_seen_at'],first)
        self.assertEqual(self.call(NOW+timedelta(minutes=30))['target'],'backup')
    def test_destinations_and_payload_stable_when_state_not_persisted(self):
        self.warning();calls=[]
        def sender(text,**kwargs):calls.append((text,kwargs));return ('sent','message_id=1')
        site_alerts.notify(self.root,NOW,sender)
        (self.root/site_alerts.STATE).unlink()
        site_alerts.notify(self.root,NOW+timedelta(seconds=2),sender)
        self.assertEqual(calls[0],calls[1]);self.assertEqual(calls[0][1]['address'],'chatgpt@example')

    def test_persistent_critical_not_starved_by_warning_churn(self):
        self.warning('error');self.call(NOW)
        self.base(health={'problems':[{'level':'error','code':'test','file':'x','text':'problem'},
                                     {'level':'warn','code':'new','text':'warning'}]})
        self.call(NOW+timedelta(minutes=20))
        self.assertEqual(self.call(NOW+timedelta(minutes=30))['target'],'backup')
    def test_same_problem_changed_detail_does_not_reset_timer(self):
        self.warning('error');first=self.call(NOW)
        self.base(health={'problems':[{'level':'error','code':'test','file':'x','text':'new details'}]})
        second=self.call(NOW+timedelta(minutes=20))
        self.assertEqual(second['incident_id'],first['incident_id'])
        self.assertEqual(self.call(NOW+timedelta(minutes=30))['target'],'backup')
    def test_ambiguous_project_warn_is_not_critical(self):
        self.base();write(self.root,'project-status.json',{'health':'warn'});self.call(NOW)
        self.assertEqual(self.call(NOW+timedelta(minutes=30))['action'],'unchanged')

    def test_failed_delivery_commit_cannot_self_trigger_retry_loop(self):
        self.warning();calls=[]
        def failed(*args,**kwargs):calls.append(1);return ('error','timeout')
        site_alerts.notify(self.root,NOW,failed)
        before=(self.root/site_alerts.STATE).read_bytes()
        r=site_alerts.notify(self.root,NOW+timedelta(seconds=30),failed)
        self.assertEqual(r['action'],'retry_deferred');self.assertEqual(len(calls),1)
        self.assertEqual((self.root/site_alerts.STATE).read_bytes(),before)
    def test_workflows_serialize_both_site_writers_and_do_not_rebase_stale_state(self):
        root=Path(__file__).resolve().parents[1]
        for name in ('canon-health.yml','topview-robot.yml'):
            text=(root/'.github/workflows'/name).read_text()
            job=text.split('  site-alerts:',1)[1]
            self.assertIn('group: site-alert-routing',job)
            self.assertIn("github.ref == 'refs/heads/main'",job)
            self.assertNotIn('git rebase',job)

    def test_warning_churn_keeps_incident_progress_and_single_backup(self):
        self.warning('error');first=self.call(NOW)
        write(self.root,site_alerts.RECEIPTS,{'events':[{'incident_id':first['incident_id'],'actor':'dot',
            'state':'in_progress','evidence':'working','updated_at':(NOW+timedelta(minutes=25)).isoformat()}]})
        for minute in (30,40,50):
            self.base(health={'problems':[{'level':'error','code':'test','file':'x','text':'problem'},
                {'level':'warn','code':str(minute),'text':'changing warning'}]})
            r=self.call(NOW+timedelta(minutes=minute))
            self.assertEqual(r['incident_id'],first['incident_id']);self.assertEqual(r['target'],'primary')
        self.assertEqual(self.call(NOW+timedelta(minutes=55))['target'],'backup')
        self.base(health={'problems':[{'level':'error','code':'test','file':'x','text':'problem'},
            {'level':'warn','code':'60','text':'changing warning'}]})
        self.assertEqual(self.call(NOW+timedelta(minutes=60))['target'],'primary')
        self.assertEqual(self.call(NOW+timedelta(minutes=65))['action'],'unchanged')


    def test_continuous_new_warning_each_scan_cannot_starve_critical_backup(self):
        backups = []
        incident = None
        for minute in range(0, 91, 10):
            self.base(health={'problems': [
                {'level': 'error', 'code': 'persistent', 'file': 'x', 'text': 'broken'},
                {'level': 'warn', 'code': str(minute), 'text': 'changing warning'}]})
            result = self.call(NOW + timedelta(minutes=minute))
            incident = incident or result['incident_id']
            self.assertEqual(result['incident_id'], incident)
            if result.get('target') == 'backup':
                backups.append(minute)
        self.assertEqual(backups, [30])

    def test_new_critical_after_old_warning_backup_gets_own_backup(self):
        self.warning()
        first = self.call(NOW)
        self.assertEqual(self.call(NOW + timedelta(minutes=120))['target'], 'backup')
        self.base(health={'problems': [
            {'level': 'warn', 'code': 'test', 'file': 'x', 'text': 'problem'},
            {'level': 'error', 'code': 'NEW', 'text': 'new critical'}]})
        newer = self.call(NOW + timedelta(minutes=130))
        self.assertEqual(newer['incident_id'], first['incident_id'])
        self.assertEqual(newer['target'], 'primary')
        self.assertEqual(self.call(NOW + timedelta(minutes=159))['action'], 'unchanged')
        self.assertEqual(self.call(NOW + timedelta(minutes=160))['target'], 'backup')
        self.assertEqual(self.call(NOW + timedelta(minutes=170))['action'], 'unchanged')


    def test_recurrent_problem_in_continuing_incident_has_new_delivery_key(self):
        def problems(include_error):
            values = [{'level': 'warn', 'code': 'sticky', 'text': 'persistent warning'}]
            if include_error:
                values.append({'level': 'error', 'code': 'recurring', 'text': 'same failure'})
            self.base(health={'problems': values})
        problems(True)
        first = self.call(NOW)
        self.assertEqual(self.call(NOW + timedelta(minutes=30))['target'], 'backup')
        first_backup = self.sent[-1]
        problems(False)
        self.call(NOW + timedelta(minutes=40))
        problems(True)
        recurrent = self.call(NOW + timedelta(minutes=50))
        self.assertEqual(first['incident_id'], recurrent['incident_id'])
        self.assertEqual(self.call(NOW + timedelta(minutes=79))['action'], 'unchanged')
        self.assertEqual(self.call(NOW + timedelta(minutes=80))['target'], 'backup')
        self.assertNotEqual(first_backup, self.sent[-1])
        self.assertEqual(self.call(NOW + timedelta(minutes=90))['action'], 'unchanged')


    def test_covered_critical_does_not_hide_new_warning_backup_deadline(self):
        self.warning('error')
        self.call(NOW)
        self.assertEqual(self.call(NOW + timedelta(minutes=30))['target'], 'backup')
        self.base(health={'problems': [
            {'level': 'error', 'code': 'test', 'file': 'x', 'text': 'problem'},
            {'level': 'warn', 'code': 'NEW', 'text': 'new warning'}]})
        self.assertEqual(self.call(NOW + timedelta(minutes=40))['target'], 'primary')
        self.assertEqual(self.call(NOW + timedelta(minutes=159))['action'], 'unchanged')
        self.assertEqual(self.call(NOW + timedelta(minutes=160))['target'], 'backup')
        self.assertEqual(self.call(NOW + timedelta(minutes=170))['action'], 'unchanged')

if __name__ == '__main__':
    unittest.main()
