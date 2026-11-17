import json
import unittest
from datetime import timedelta

from test_site_alerts import AlertTests, NOW, write
import site_alerts
import site_alert_canary
import site_alert_receiver as receiver


class ReceiverTests(AlertTests):
    def setUp(self):
        super().setUp()
        self.base(health={'problems':[{'level':'error','code':'broken-ref','text':'broken'}]})
        cfg=site_alerts.read_json(self.root,'ops/relay-wake.json')
        cfg['sender_agent_id']='robot-test'
        write(self.root,'ops/relay-wake.json',cfg)

    def check(self, text, **kwargs):
        options=dict(actor='dot',authenticated_sender_id='robot-test',now=NOW)
        options.update(kwargs)
        return receiver.validate(self.root,text,**options)

    def test_prepared_canonical_incident_visible_to_real_receiving_boundary(self):
        site_alerts.notify(self.root,NOW,prepare_only=True)
        results=[]
        def send(text, **kw):
            results.append(self.check(text))
            return 'sent','receipt'
        site_alerts.notify(self.root,NOW,send,require_prepared=True)
        self.assertTrue(results[0]['accepted'])
        self.assertFalse(results[0]['write_allowed'])
        self.assertEqual(results[0]['kind'],'production')

    def test_sender_role_incident_occurrence_and_resolution_are_checked(self):
        site_alerts.notify(self.root,NOW,self.sender)
        text=self.sent[-1]
        self.assertTrue(self.check(text)['accepted'])
        self.assertFalse(self.check(text,authenticated_sender_id='fake')['accepted'])
        self.assertFalse(self.check(text,actor='grok')['accepted'])
        self.assertFalse(self.check(text.replace('SITE_ALERT_V2 site:','SITE_ALERT_V2 old:'))['accepted'])
        self.assertFalse(self.check(text.replace('occurrence_set=','occurrence_set=wrong'))['accepted'])
        self.assertFalse(self.check(text+'\nrecipient_actor=dot')['accepted'])
        self.base()
        self.assertFalse(self.check(text)['accepted'])

    def test_general_disable_or_invalid_mode_rejects_inflight_production(self):
        site_alerts.notify(self.root,NOW,self.sender)
        text=self.sent[-1]
        cfg=site_alerts.read_json(self.root,'ops/relay-wake.json')
        cfg['site_alert_enabled']=False
        write(self.root,'ops/relay-wake.json',cfg)
        self.assertFalse(self.check(text)['accepted'])
        cfg['site_alert_enabled']=True
        cfg['site_alert_routing']['mode']='invalid'
        write(self.root,'ops/relay-wake.json',cfg)
        self.assertFalse(self.check(text)['accepted'])

    def test_old_message_after_role_switch_is_rejected(self):
        site_alerts.notify(self.root,NOW,self.sender)
        cfg=site_alerts.read_json(self.root,'ops/relay-wake.json')
        cfg['wake_roles']={'primary_actor':'grok','backup_actor':'dot'}
        write(self.root,'ops/relay-wake.json',cfg)
        self.assertFalse(self.check(self.sent[-1])['accepted'])

    def test_canary_exact_allowlist_and_no_writes(self):
        cfg=site_alerts.read_json(self.root,'ops/relay-wake.json')
        cfg['site_alert_routing']['enabled']=False
        cfg['wake_roles']={'primary_actor':'grok','backup_actor':'dot'}
        write(self.root,'ops/relay-wake.json',cfg)
        calls=[]
        def send(root,text,**kw):
            calls.append(text);return 'sent','receipt'
        site_alert_canary.send(self.root,'site-test-123','dot',True,send)
        text=calls[0]
        before={str(p):p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        self.assertFalse(self.check(text)['accepted'])
        good=self.check(text,allowed_test_ids=['site-test-123'])
        self.assertTrue(good['accepted'])
        self.assertEqual(good['role'],'backup')
        self.assertFalse(good['write_allowed'])
        self.assertEqual(before,{str(p):p.read_bytes() for p in self.root.rglob('*') if p.is_file()})
