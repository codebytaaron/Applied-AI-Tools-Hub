# Supplier Reorder Plan

Industry focus: **Landscaping Company**

## What it does
Builds reorder triggers, par levels, and vendor notes.

## Run
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python main.py --in examples/input.txt --out out.md
```

## Notes
- Runs in MOCK_MODE by default.
- Edit `prompt.py` to customize behavior.
