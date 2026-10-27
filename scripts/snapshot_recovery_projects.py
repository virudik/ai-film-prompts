#!/usr/bin/env python3
"""Copy all project recovery text sources with paths and hashes; no image/media payload."""
import hashlib
import json
import shutil
import sys
from pathlib import Path
from resume_project import context


def snapshot(root, output):
    root, output = Path(root), Path(output) / 'recovery-projects'
    paths = {'projects/projects.json', 'projects/README.md', 'ops/CONTINUE-PROTOCOL.md'}
    for project in json.loads((root / 'projects/projects.json').read_bytes())['projects']:
        ctx = context(root, project['id'])
        packet = json.loads((root / ctx['packet_dir'] / 'resume-packet.json').read_bytes())
        paths.update(s['file'] for s in packet['sources'])
        paths.update(ctx['packet_dir'] + '/' + name for name in ['resume-packet.json', 'resume-packet.md'])
        paths.add(ctx['receipts'])
    manifest = []
    for name in sorted(paths):
        # Canonical packet sources are verified by the packet builder; copy exact bytes.
        from resume_state import local_file
        source = local_file(root, name)
        data = source.read_bytes()
        included = source.suffix.lower() in {'.json', '.md', '.txt', '.yaml', '.yml', '.py', '.js', '.html'}
        if included:
            data.decode('utf-8-sig')
            dest = output / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, dest)
        manifest.append({'file': name, 'sha256': hashlib.sha256(data).hexdigest(), 'included': included})
    (output / 'SHA256.json').write_text(json.dumps(manifest, indent=2) + '\n')


if __name__ == '__main__':
    snapshot(sys.argv[1], sys.argv[2])
