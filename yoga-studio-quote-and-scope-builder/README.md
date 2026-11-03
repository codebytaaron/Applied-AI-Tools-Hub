# Quote and Scope Builder

Niche company template: **Yoga Studio**

## What it does
Turns notes into an itemized quote with scope, exclusions, and timeline.

## Run
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python main.py
```

Notes:
- Runs in MOCK_MODE by default.
- Edit `prompt.py` to customize behavior.
