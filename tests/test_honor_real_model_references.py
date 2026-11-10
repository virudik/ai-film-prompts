import hashlib,json,re,sys,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1];P=R/'projects/raznoe';S=(P/'video-prompts.md').read_text();C4=S[S.index('<a id="scene-4">'):S.index('<a id="scene-5">')];C5=S[S.index('<a id="scene-5">'):];B={4:re.findall(r'```text\n(.*?)\n```',C4,re.S),5:re.findall(r'```text\n(.*?)\n```',C5,re.S)}
class HonorBindings(unittest.TestCase):
 def test_counts_and_durations(self):
  self.assertEqual([len(B[4]),len(B[5])],[36,3]);self.assertEqual(sum('Duration: 30s' in x for x in B[4]),12);self.assertEqual(sum('Duration: 15s' in x for x in B[4]),24)
 def test_source_identity_in_every_prompt(self):
  for sid,model in [(4,'HONOR Magic9 Pro Max'),(5,'HONOR X9e Pro')]:
   for b in B[sid]:self.assertIn(model,b);self.assertIn('@Image1 =',b);self.assertIn('@Image2 =',b);self.assertIn('drive.google.com/file/d/',b);self.assertIn('FRAME FILL',b)
 def test_all_bodies_match_binding_hash(self):
  sys.path.insert(0,str(R/'scripts'));from topview_prompt_match import master_blocks
  bodies=dict(master_blocks(S))
  for sid in [4,5]:
   m=json.loads((P/f'references/scenes/scene-{sid}/reference-bindings.json').read_text());self.assertEqual(len(m['prompts']),len(B[sid]))
   for x in m['prompts']:
    b=bodies[x['label']];self.assertEqual(hashlib.sha256(b.encode()).hexdigest(),x['prompt_sha256']);self.assertEqual(set(re.findall(r'@(?:Image|Video)\d+',b)),set(x['inputs']))
 def test_six_originals_and_previews_exact(self):
  r=json.loads((P/'reports/honor-reference-integration.json').read_text());self.assertEqual(len(r['assets']),6)
  for a in r['assets']:
   for key,hkey in [('path','sha256'),('preview','preview_sha256')]:self.assertEqual(hashlib.sha256((R/a[key]).read_bytes()).hexdigest(),a[hkey])
 def test_illustrations_never_official(self):
  for sid in [4,5]:
   m=json.loads((P/f'references/scenes/scene-{sid}/manifest.json').read_text())
   for r in m['references']:
    if r.get('source_kind')=='chatgpt_generated_existing':self.assertFalse(r['technical_product_identity']);self.assertEqual(r['editorial_status'],'not_approved')
 def test_bad_background_and_pair_not_prompt_inputs(self):
  for b in B[4]+B[5]:self.assertNotIn('H-GEN-PAIR.png',b);self.assertNotIn('X-GEN-MOSCOW.png',b)
  self.assertIn('X-GEN-MOSCOW.png',C5);self.assertIn('H-GEN-PAIR.png',C4)
 def test_no_blank_device_contradiction(self):
  for b in B[4]+B[5]:
   for t in ['BACKGROUND PLATE','not extra generator image slots','A small blank matte rectangle','Hold the blank proxy','not an HONOR product','No supplied files.','No official device or location image is supplied','for a later product front']:
    self.assertNotIn(t,b)
 def test_no_auto_approval_or_video(self):
  for c in [C4,C5]:self.assertIn('"production_state":"DRAFT"',c)
  r=json.loads((P/'reports/honor-reference-integration.json').read_text());self.assertEqual(r['video_launches'],0);self.assertEqual(r['new_generations'],0);self.assertEqual(r['credits_spent'],0)
 def test_real_contest_plan_retained(self):
  self.assertIn('Дворовая машина Голдберга',C5);self.assertIn('Москва',C5);self.assertIn('90 с',C5);self.assertIn('НЕ отправлен',C5)
  for b in B[5]:self.assertIn('NOT competition test footage',b);self.assertIn('No test action',b)
 def test_real_tails_remain_required(self):
  self.assertIn('@Video1',B[5][2]);self.assertNotIn('@Video1',B[5][0]);self.assertNotIn('@Video1',B[5][1]);self.assertEqual(sum('@Video1' in b for b in B[4]),30)
 def test_original_voice_map_preserved(self):
  for b in B[4]:self.assertIn('filmwide-voiceover-120s.json',b);self.assertNotIn('production-voiceover.json',b)
 def test_compact_spacing(self):
  self.assertIsNone(re.search(r'\n(?:[ \t]*\n){2,}',S))
if __name__=='__main__':unittest.main(verbosity=2)
