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
    def test_terminal_result_survives_stale_active_telemetry(self):
        # A newer successful task result must win over the older robot running snapshot.
        parent={'id':'P1','scene_id':70,'state':'submitted','task_id':'T','references':[]}
        next_part={'id':'P2','scene_id':65,'state':'waiting_for_slot',
                   'depends_on_completed':['P1'],'references':[]}
        self.run_case([parent,next_part],[{'task_id':'T','final_status':'success'}])
        (self.root/'topview-status.json').write_text(json.dumps({
            'active_tasks':[{'task_id':'T','topview_status':'running'}]}))
        rows={row['id']:row for row in qr.derive(self.root)['items']}
        self.assertEqual(rows['P2']['code'],'ready')
        self.assertTrue(rows['P2']['ready'])

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
    def test_linked_without_excerpt_yields_to_independent(self):
        (self.root/'clip-note.txt').write_bytes(b'independent')
        digest=qr.digest(self.root/'clip-note.txt')
        linked={'id':'LINK','scene_id':48,'priority':0.1,'state':'waiting_for_slot',
                'depends_on_submitted':['PREV'],'depends_on_completed':['PREV'],
                'references':[{'slot':'@Video1','required':True,'canonical_role':'previous_part_end',
                               'source_item_id':'PREV','input_status':'required_not_available'}]}
        dependency_only={'id':'DEPONLY','scene_id':48,'priority':0.15,'state':'waiting_for_slot',
                         'depends_on_submitted':['PREV'],'references':[{'slot':'@Image1','path':'clip-note.txt','sha256':digest}]}
        independent={'id':'FREE','scene_id':51,'priority':0.2,'state':'waiting_for_slot',
                     'depends_on_submitted':[],'references':[{'slot':'@Image1','path':'clip-note.txt','sha256':digest}]}
        unknown={'id':'UNK','scene_id':49,'priority':0.01,'state':'submission_unknown','references':[]}
        refused={'id':'REF','scene_id':49,'priority':0.02,'state':'waiting_for_slot','substantive_refusal':True,
                 'provider_error_code':'7000','references':[{'slot':'@Image1','path':'clip-note.txt','sha256':digest}]}
        parent={'id':'PREV','scene_id':48,'state':'submitted','task_id':'T','references':[]}
        self.run_case([linked,dependency_only,independent,unknown,refused,parent],[{'task_id':'T','final_status':'success'}])
        picked=qr.launch_candidates(self.root)
        self.assertEqual(picked['chosen'],['FREE'])
        reasons={row['id']:row['reason'] for row in picked['skipped']}
        self.assertNotEqual(reasons['LINK'],'ready')
        self.assertEqual(reasons['DEPONLY'],'continuity_excerpt_missing')
        self.assertEqual(reasons['UNK'],'preflight_required')
        self.assertEqual(reasons['REF'],'substantive_refusal')
        self.assertTrue(qr.continuity_blocks_launch(linked,self.root))
        self.assertFalse(qr.continuity_blocks_launch(independent,self.root))
    def test_materialized_excerpt_is_eligible_and_declaration_is_not(self):
        (self.root/'end.mp4').write_bytes(b'excerpt-bytes')
        digest=qr.digest(self.root/'end.mp4')
        ready={'id':'P2','scene_id':42,'priority':0.2,'state':'waiting_for_slot','depends_on_completed':['P1'],
               'references':[{'slot':'@Video1','required':True,'canonical_role':'previous_part_end','source_item_id':'P1',
                              'path':'end.mp4','sha256':digest,'input_status':'available','source_kind':'actual_topview_result_trim'}]}
        declared={'id':'P3','scene_id':42,'priority':0.1,'state':'waiting_for_slot','depends_on_submitted':['P1'],
                  'references':[{'slot':'@Video1','required':True,'source_item_id':'P1','sha256':digest,
                                 'input_status':'available','source_task_id':'T'}]}
        parent={'id':'P1','state':'submitted','task_id':'T','references':[]}
        self.run_case([declared,ready,parent],[{'task_id':'T','final_status':'success'}])
        self.assertEqual(qr.launch_candidates(self.root)['chosen'],['P2'])
        self.assertFalse(qr.continuity_blocks_launch(ready,self.root))
        self.assertTrue(qr.continuity_blocks_launch(declared,self.root))
        private=dict(declared,id='P4',references=[{'slot':'@Video1','required':True,'source_item_id':'P1',
                     'library_file_id':'libfile_saved','sha256':'a'*64,'input_status':'available'}])
        self.assertFalse(qr.continuity_blocks_launch(private,self.root))
    def test_music_needs_new_consent_and_intent_stays(self):
        (self.root/'note.txt').write_bytes(b'story-ref')
        digest=qr.digest(self.root/'note.txt')
        ref=[{'slot':'@Image1','path':'note.txt','sha256':digest}]
        music={'id':'S51E','scene_id':51,'priority':0.1,'state':'waiting_for_slot','references':ref}
        story={'id':'S52','scene_id':52,'priority':0.2,'state':'waiting_for_slot','references':ref,
               'depends_on_completed':['PREV'],'references':[{'slot':'@Video1','path':'note.txt','sha256':digest,
               'input_status':'available','canonical_role':'previous_part_end'}]}
        plain={'id':'FREE','scene_id':60,'priority':0.3,'state':'waiting_for_slot','references':ref}
        running={'id':'S51B','scene_id':51,'priority':0.05,'state':'submitted','task_id':'T51B','references':[]}
        inflight={'id':'S51D','scene_id':51,'priority':0.06,'state':'submitting','references':ref,
                  'claim':{'submission_intent_id':'de496b26-2a6c-4d52-befd-c773c0f90871','submission_intent_at':'2026-11-08T17:37:41Z','replay_forbidden':True}}
        parent={'id':'PREV','scene_id':52,'state':'submitted','task_id':'T','references':[]}
        self.run_case([music,story,plain,running,inflight,parent],[{'task_id':'T','final_status':'success'}])
        q=json.loads((self.root/'ops/topview-launch-queue.json').read_text())
        q['owner_policy_20261108_t369u']={'effect':'music_requires_owner_consent','scenes':[28,49,50,51]}
        (self.root/'ops/topview-launch-queue.json').write_text(json.dumps(q))
        picked=qr.launch_candidates(self.root)
        self.assertEqual(picked['chosen'],['FREE','S52'])
        reasons={row['id']:row['reason'] for row in picked['skipped']}
        self.assertEqual(reasons['S51E'],'music_owner_consent_required')
        self.assertEqual(reasons['S51D'],'preflight_required')
        self.assertTrue(qr.music_create_blocked(q, inflight))
        self.assertFalse(qr.music_create_blocked(q, running))
        self.assertEqual(inflight['claim']['submission_intent_id'],'de496b26-2a6c-4d52-befd-c773c0f90871')
        plain['state']='blocked_inputs'
        q['items']=[music,story,plain,running,inflight,parent]
        (self.root/'ops/topview-launch-queue.json').write_text(json.dumps(q))
        self.assertEqual(qr.launch_candidates(self.root)['chosen'],['S52'])
    def test_t422_puts_the_tatooine_chain_ahead_of_a_ready_single(self):
        (self.root/'note.txt').write_bytes(b'story-ref')
        digest=qr.digest(self.root/'note.txt')
        ref=[{'slot':'@Image1','path':'note.txt','sha256':digest}]
        chain={'id':'S52-R2-SEED20-P4','scene_id':52,'priority':0.5,'state':'waiting_for_slot','references':ref}
        single={'id':'S59-SEED20-P3','scene_id':59,'priority':0.1,'state':'waiting_for_slot','references':ref}
        held={'id':'S62-SEED20-P1-R2-20261108','scene_id':62,'priority':-0.5,'state':'waiting_for_slot','references':ref}
        music={'id':'S49B','scene_id':49,'priority':9,'state':'waiting_for_slot','owner_music_consent':True,
               'owner_music_consent_record':{'condition':'after_all_story','scope':'S49B'},'references':ref}
        self.run_case([music,single,held,chain])
        q=json.loads((self.root/'ops/topview-launch-queue.json').read_text())
        q['owner_policy_20261108_t369u']={'effect':'music_requires_owner_consent','scenes':[28,49,50,51]}
        q['owner_policy_20261109_t422u']={'effect':'tatooine_chain_first','tatooine_chain':['S52-R2-SEED20-P4'],'hold_scenes':[62]}
        (self.root/'ops/topview-launch-queue.json').write_text(json.dumps(q))
        picked=qr.launch_candidates(self.root)
        self.assertEqual(picked['chosen'],['S52-R2-SEED20-P4','S59-SEED20-P3'])
        reasons={row['id']:row['reason'] for row in picked['skipped']}
        self.assertEqual(reasons['S62-SEED20-P1-R2-20261108'],'owner_hold')
        self.assertEqual(reasons['S49B'],'music_owner_consent_required')
        q['items']=[music]
        (self.root/'ops/topview-launch-queue.json').write_text(json.dumps(q))
        self.assertEqual(qr.launch_candidates(self.root)['chosen'],['S49B'])

    def test_does_not_mutate_queue_or_repeat_unchanged_write(self):
        self.run_case([self.first]);before=(self.root/'ops/topview-launch-queue.json').read_bytes()
        self.assertTrue(qr.write(self.root));self.assertFalse(qr.write(self.root))
        self.assertEqual(before,(self.root/'ops/topview-launch-queue.json').read_bytes())

if __name__=='__main__':unittest.main()
