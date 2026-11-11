#!/usr/bin/env python3
"""Check Python syntax, JSON, template setup, and generated catalog without API calls."""
import ast
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', '.venv', 'venv', 'node_modules', '__pycache__', '.next', 'dist'}
errors = []
python_count = json_count = template_count = 0
for path in sorted(ROOT.rglob('*')):
    if not path.is_file() or SKIP.intersection(path.relative_to(ROOT).parts):
        continue
    try:
        if path.suffix == '.py':
            ast.parse(path.read_text(encoding='utf-8-sig'), filename=str(path.relative_to(ROOT)))
            python_count += 1
        elif path.suffix == '.json':
            json.loads(path.read_text(encoding='utf-8-sig'))
            json_count += 1
        if path.name == 'main.py' and (path.parent / 'prompt.py').exists():
            template_count += 1
            for name in ('README.md', 'requirements.txt', '.env.example', 'examples/input.txt'):
                if not (path.parent / name).is_file():
                    errors.append(f'{path.parent.relative_to(ROOT)}: missing {name}')
    except (SyntaxError, ValueError, UnicodeError) as exc:
        errors.append(f'{path.relative_to(ROOT)}: {exc}')
result = subprocess.run([sys.executable, str(ROOT / 'scripts/catalog.py'), '--check'], cwd=ROOT)
if result.returncode:
    errors.append('Generated catalog is out of date')
if errors:
    print('\n'.join(errors), file=sys.stderr)
    raise SystemExit(1)
print(f'Passed: {python_count} Python files, {json_count} JSON files, {template_count} template setups, catalog freshness.')
