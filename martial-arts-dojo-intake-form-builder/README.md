# Intake Form Builder

Niche company template: **Martial Arts Dojo**

## What it does
Creates a client intake form with the right questions and follow-ups.

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
