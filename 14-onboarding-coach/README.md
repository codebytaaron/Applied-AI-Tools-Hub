# Customer Onboarding Playbook Generator

Creates an onboarding sequence, success milestones, and a check-in schedule to reduce churn.

## What it does
Given a product and customer type, produces onboarding steps, milestone definitions, sample emails, and a 30-day success plan.

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
