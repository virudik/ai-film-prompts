import json
import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))
import queue_readiness as qr

class QueueReadinessTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name);(self.root/'ops').mkdir()
        self.first={'id':'P1','scene_id':62,'canonical_block_label':'62 · Seedance 2.0 часть 1','state':'waiting_for_slot','references':[]}
        self.second={'id':'P2','scene_id':62,'canonical_block_label':'62 · Seedance 2.0 часть 2','state':'blocked_inputs','references':[{'slot':'@Video1','source_item_id':'P1','input_status':'required_not_available'}]}
    def run_case(self,items,tasks=()):
        for path,data in [('ops/topview-launch-queue.json',{'items':items}),('topview-task-map.json',{'processed_tasks':list(tasks)}),('topview-status.json',{})]:
            (self.root/path).write_text(json.dumps(data))
        return {r['id']:r for r in qr.derive(self.root)['items']}
    def test_parts_are_independent(self):
        rows=self.run_case([self.first,self.second]);self.assertTrue(rows['P1']['ready']);self.assertEqual(rows['P2']['code'],'waiting_result')
    def test_success_needs_trim_and_qc(self):
        self.first.update(state='submitted',task_id='T')
        rows=self.run_case([self.first,self.second],[{'task_id':'T','final_status':'success'}])
        self.assertNotIn('P1',rows);self.assertEqual(rows['P2']['code'],'prepare_continuity');self.assertFalse(rows['P2']['ready'])
    def test_missing_image_is_not_previous_result(self):
        self.first['references']=[{'slot':'@Image1','path':'missing.jpg','input_status':'available'}]
        self.assertEqual(self.run_case([self.first])['P1']['code'],'missing_reference')
    def test_hash_mismatch_is_blocked(self):
        (self.root/'image.jpg').write_bytes(b'x');self.first['references']=[{'path':'image.jpg','sha256':'bad'}]
        self.assertFalse(self.run_case([self.first])['P1']['ready'])
    def test_saved_private_clip_is_available_but_not_auto_unblocked(self):
        self.second['references']=[{'slot':'@Video1','library_file_id':'libfile_saved','sha256':'a'*64,'input_status':'available'}]
        self.assertEqual(self.run_case([self.second])['P2']['code'],'preflight_required')
    def test_owner_hold_wins_over_existing_file(self):
        self.first.update(scene_id=44,owner_decision_20261023={'meaning':'wait'})
        self.assertEqual(self.run_case([self.first])['P1']['code'],'owner_hold')
    def test_does_not_mutate_queue_or_repeat_unchanged_write(self):
        self.run_case([self.first]);before=(self.root/'ops/topview-launch-queue.json').read_bytes()
        self.assertTrue(qr.write(self.root));self.assertFalse(qr.write(self.root))
        self.assertEqual(before,(self.root/'ops/topview-launch-queue.json').read_bytes())

if __name__=='__main__':unittest.main()
