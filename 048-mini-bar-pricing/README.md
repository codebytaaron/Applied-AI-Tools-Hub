# Mini-Bar Pricing

Industry focus: **Hotel**

## What it does
Creates mini-bar pricing for hotel management.

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
