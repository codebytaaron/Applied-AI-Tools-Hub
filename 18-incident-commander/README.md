# Incident Response Coordinator

Creates a timeline, root-cause hypotheses, comms plan, and postmortem outline for incidents.

## What it does
Given incident notes, outputs a structured incident report, immediate actions, stakeholder messaging, and postmortem agenda.

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
