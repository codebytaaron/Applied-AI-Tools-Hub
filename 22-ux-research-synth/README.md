# UX Research Synthesizer

Synthesizes interview notes into themes, user needs, and prioritized improvements.

## What it does
Given research notes, outputs key themes, pain points, opportunity areas, and a prioritized backlog.

## Quick start
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
# set MOCK_MODE=true to run without an API key
python main.py --in examples/input.txt --out out.md
```

## Customize
- Edit `prompt.py` to fit your rules, formatting, and required outputs.
- Add real examples to `examples/`.

## Output
- Writes a structured result to `out.md`.
