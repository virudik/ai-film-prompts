"""Production provenance must not be parsed as current Topview reference chips."""
import hashlib
import json
from pathlib import Path
import re
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from topview_prompt_match import master_blocks, normalise


class Scene89ProvenanceTests(unittest.TestCase):
    def test_production_prompts_have_only_current_reference_mentions(self):
        blocks = master_blocks((ROOT / 'video-prompts.md').read_text())
        for part, count in [('89F', 3), ('89G', 5)]:
            selected = [(label, body) for label, body in blocks
                        if label.startswith(part + ' ·') and ('Wan 3.0' in label or 'Seedance 2.0' in label)
                        and 'REFERENCES / AUTHORITY ORDER:' in body]
            self.assertEqual(len(selected), 2, part)
            for label, body in selected:
                with self.subTest(label=label):
                    self.assertNotRegex(body, r'<<<\s*Image\s*\d+\s*>>>')
                    self.assertEqual(set(re.findall(r'@Image(\d+)', body)),
                                     {str(n) for n in range(1, count + 1)})
                    for line in body.splitlines():
                        if 'Historical' in line or 'historical source slot' in line:
                            # Only the left-hand definition may be an active mention.
                            self.assertEqual(len(re.findall(r'@Image\d+', line)), 1)

    def test_manifest_roles_are_passive_and_consistent(self):
        order = json.loads((ROOT / 'references/scenes/scene-89/image-order.json').read_text())
        for part in ['89F', '89G']:
            slots = json.loads((ROOT / f'references/scenes/scene-89/{part}/slots.json').read_text())['slots']
            self.assertEqual(len(slots), len(order['subscenes'][part]))
            for slot, ordered in zip(slots, order['subscenes'][part]):
                self.assertEqual(slot['slot'], ordered['slot'])
                self.assertEqual(slot['path'], ordered['path'])
                self.assertEqual(slot['role'], ordered['role'])
                self.assertNotRegex(slot['role'], r'<<<|@Image\d+')

    def test_queue_hashes_match_exact_production_prompts(self):
        blocks = dict(master_blocks((ROOT / 'video-prompts.md').read_text()))
        queue = json.loads((ROOT / 'ops/topview-launch-queue.json').read_text())
        items = [x for x in queue['items'] if x['id'] in ['S89F-WAN30', 'S89G-WAN30']]
        self.assertEqual(len(items), 2)
        for item in items:
            body = blocks[item['canonical_block_label']]
            self.assertEqual(item['canonical_prompt_sha256'], hashlib.sha256(body.encode()).hexdigest())
            self.assertEqual(item['normalized_prompt_sha256'], hashlib.sha256(normalise(body).encode()).hexdigest())


if __name__ == '__main__':
    unittest.main()
