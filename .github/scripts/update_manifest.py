#!/usr/bin/env python3
"""Update a session.manifest.yml file with the rendered DOCX path and append a history entry.

Usage:
  python3 update_manifest.py <manifest.yml> <docx_path>

Attempts to use PyYAML; if unavailable falls back to a conservative text-edit.
"""
import sys
import os
import datetime

if len(sys.argv) != 3:
    print("Usage: update_manifest.py <manifest.yml> <docx_path>", file=sys.stderr)
    sys.exit(2)

manifest_path = sys.argv[1]
docx_path = sys.argv[2]
rel_docx = os.path.relpath(docx_path, start=os.getcwd())

try:
    import yaml
    with open(manifest_path, 'r', encoding='utf-8') as f:
        m = yaml.safe_load(f) or {}

    m.setdefault('outputs', {})
    m['outputs']['docx_file'] = rel_docx

    history = m.get('history', [])
    history.append({
        'timestamp_utc': datetime.datetime.utcnow().replace(microsecond=0).isoformat() + 'Z',
        'action': 'render',
        'details': f"Rendered using pandoc with template {m.get('conversion', {}).get('template_file', 'templates/word/template.docx')}"
    })
    m['history'] = history

    with open(manifest_path, 'w', encoding='utf-8') as f:
        yaml.safe_dump(m, f, sort_keys=False)
    print('Manifest updated (PyYAML).')
except Exception:
    # Fallback: conservative text edits
    print('PyYAML not available or failed; using conservative text replacement.', file=sys.stderr)
    with open(manifest_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # Replace a common `docx_file: null` with actual path
    if 'docx_file:' in text:
        text = text.replace('docx_file: null', f'docx_file: "{rel_docx}"')
        text = text.replace('docx_file: null\n', f'docx_file: "{rel_docx}"\n')
    else:
        # Ensure outputs section exists
        if 'outputs:' in text:
            text = text.replace('outputs:\n', f'outputs:\n  docx_file: "{rel_docx}"\n')
        else:
            # Append outputs section before history or at EOF
            if '\nhistory:' in text:
                text = text.replace('\nhistory:', f'\noutputs:\n  docx_file: "{rel_docx}"\n\nhistory:')
            else:
                text = text + f'\noutputs:\n  docx_file: "{rel_docx}"\n'

    # Append a history entry at the end
    timestamp = datetime.datetime.utcnow().replace(microsecond=0).isoformat() + 'Z'
    entry = f"- timestamp_utc: \"{timestamp}\"\n  action: \"render\"\n  details: \"Rendered using pandoc\"\n"
    if '\nhistory:' in text:
        text = text + '\n' + entry
    else:
        text = text + '\nhistory:\n' + entry

    with open(manifest_path, 'w', encoding='utf-8') as f:
        f.write(text)
    print('Manifest updated (text fallback).')

print('Done.')
