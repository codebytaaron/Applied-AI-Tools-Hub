# Operational Risk Register Builder

Turns messy notes into a risk register with likelihood, impact, mitigations, owners, and review cadence.

## What it does
Given notes about a project or business area, produces a risk register table, top 5 risks, mitigation plan, and monitoring triggers.

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
