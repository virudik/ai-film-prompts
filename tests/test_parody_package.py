import hashlib
import json
import struct
import tempfile
import unittest
from pathlib import Path
from scripts.check_parody_package import audit, EXPECTED_IDENTITIES, safe_path

TARGETS = [(74, 'S74-torch-curtain'), (74, 'S74-globe-stage'), (74, 'S74-potato-mountain'), (74, 'S74-searchlight-crates'), (74, 'S74-saucepan-gong'), (76, 'S76-normalno-ice'), (76, 'S76-yaz-boat')]

class ParodyPackageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.png = b'\x89PNG\r\n\x1a\n' + b'\x00\x00\x00\rIHDR' + struct.pack('>II', 1600, 900)
        blocks = []
        for sid, paths in EXPECTED_IDENTITIES.items():
            refs = []
            for path in paths:
                self.write(path, b'identity bytes ' + path.encode())
                refs.append(self.ref(path, 'identity'))
            name = f'references/scenes/scene-{sid}/primary.png'
            self.write(name, self.png)
            refs.append(self.ref(name, 'scene_staging'))
            self.js(f'references/scenes/scene-{sid}/manifest.json', {'references': refs})
            blocks.append(f'<a id="scene-{sid}"></a>\n## Сцена {sid} — Test\n' + '\n'.join(ref['path'] for ref in refs) + '\n' + '\n'.join('```text\nprompt\n```' for _ in range(3)))
        self.write('video-prompts.md', '\n---\n\n'.join(blocks))
        self.js('reports/parody-scenes-2026-11-09.json', {'rejected_outputs': []})
        self.js('reports/parody-scenes-source-2026-11-09.json', {'source_review': {}})
        self.jobs = [{'scene_id': sid, 'kind': name, 'target_path': f'references/scenes/scene-{sid}/{name}.png', 'status': 'needs_generation'} for sid, name in TARGETS]
        self.js('reports/parody-supplementary-reference-jobs-2026-11-09.json', {'jobs': self.jobs})

    def write(self, name, value):
        p = self.root / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(value.encode() if isinstance(value, str) else value)

    def js(self, name, value):
        self.write(name, json.dumps(value))

    def ref(self, name, role):
        return {'path': name, 'role': role, 'sha256': hashlib.sha256((self.root / name).read_bytes()).hexdigest()}

    def load(self, name):
        return json.loads((self.root / name).read_text())

    def test_seven_primaries_are_not_full_completion(self):
        r = audit(self.root)
        self.assertTrue(r['integrity_ok'], r['errors'])
        self.assertEqual(r['primary_scenes_with_stills'], 7)
        self.assertEqual(r['prompt_blocks'], 21)
        self.assertFalse(r['work_complete'])
        self.assertGreaterEqual(len(r['pending']), 9)

    def test_bad_sha_is_an_integrity_error(self):
        self.write('references/scenes/scene-74/primary.png', b'changed')
        self.assertFalse(audit(self.root)['integrity_ok'])

    def test_rejected_output_cannot_be_attached(self):
        self.js('reports/parody-scenes-2026-11-09.json', {'rejected_outputs': [{'sha256': hashlib.sha256(self.png).hexdigest()}]})
        self.assertTrue(any('rejected output' in x for x in audit(self.root)['errors']))

    def test_child_reference_cannot_replace_adult_cast(self):
        name = 'references/scenes/scene-77/manifest.json'
        m = self.load(name)
        m['references'][0]['path'] = 'references/scenes/scene-66/S66-Alina-tatooine-sheet.png'
        self.js(name, m)
        self.assertFalse(audit(self.root)['integrity_ok'])

    def test_missing_file_not_satisfied_by_manifest(self):
        (self.root / 'references/scenes/scene-75/primary.png').unlink()
        r = audit(self.root)
        self.assertFalse(r['integrity_ok'])
        self.assertEqual(r['primary_scenes_with_stills'], 6)

    def test_source_audio_review_not_inferred_from_links(self):
        self.js('reports/parody-scenes-source-2026-11-09.json', {'source_review': {'sources': ['https://example.org/video']}})
        self.assertTrue(any(x['kind'] == 'original_meme_audio_visual_review' for x in audit(self.root)['pending']))

    def test_sha_is_not_a_likeness_test(self):
        self.assertTrue(any(x['kind'] == 'visual_likeness_and_composition_review' for x in audit(self.root)['pending']))

    def test_missing_jobs_are_not_silently_closed(self):
        self.js('reports/parody-supplementary-reference-jobs-2026-11-09.json', {'jobs': []})
        r = audit(self.root)
        self.assertFalse(r['work_complete'])
        self.assertTrue(any(x['kind'] == 'missing_supplementary_job' for x in r['pending']))

    def test_path_escape_is_rejected(self):
        with self.assertRaises(ValueError):
            safe_path(self.root, '../outside.png')

    def test_declared_png_exists_does_not_replace_actual_file(self):
        for job in self.jobs:
            job.update(png_exists=True, status='done')
        self.js('reports/parody-supplementary-reference-jobs-2026-11-09.json', {'jobs': self.jobs})
        self.assertEqual(sum(not x['actual_file_exists'] for x in audit(self.root)['supplementary']), 7)

if __name__ == '__main__':
    unittest.main()
