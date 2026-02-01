# Maintenance Schedule Builder

Industry focus: **Car Wash**

## What it does
Creates maintenance schedule builder for car wash operations.

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
