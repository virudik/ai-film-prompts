import sys, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from launcher_receipt_provenance import build

class ProvenanceTest(unittest.TestCase):
    def args(self):
        return dict(execution_instance_id='5840bf90-d916-4ab2-861d-f282bc863d07',
                    actual_trigger='scheduled', automation_id='real-id', run_id=None,
                    run_id_unavailable_reason='Not exposed by runtime',
                    started_at='2026-11-18T10:00:00Z', updated_at='2026-11-18T10:02:00Z',
                    scan_checked_at='2026-11-18T10:01:00Z', lease_acquired_at='2026-11-18T10:01:30Z')
    def test_null_runtime_is_preserved_and_start_precedes_scan(self):
        p=build(**self.args()); self.assertIsNone(p['run_id']); self.assertEqual(p['actual_trigger'],'scheduled')
    def test_lease_time_cannot_masquerade_as_runtime_start(self):
        p=self.args(); p['started_at']=p['lease_acquired_at']
        with self.assertRaisesRegex(ValueError,'receipt_time_order'): build(**p)
    def test_unknown_trigger_is_explicit(self):
        p=self.args(); p['actual_trigger']='not_exposed'; p['automation_id']=None
        self.assertEqual(build(**p)['actual_trigger'],'not_exposed')
    def test_missing_reason_or_future_stage_rejected(self):
        for key,value in [('run_id_unavailable_reason',None),('completed_at','2026-11-18T10:03:00Z')]:
            p=self.args(); p[key]=value
            with self.assertRaises(ValueError): build(**p)

    def test_empty_runtime_id_and_blank_reason_rejected(self):
        for key,value in [('run_id',''),('run_id','  '),('run_id_unavailable_reason','  ')]:
            p=self.args(); p[key]=value
            with self.assertRaises(ValueError): build(**p)
