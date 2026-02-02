# SOP Generator

Niche company template: **Solar Panel Installer**

## What it does
Turns procedures into a clean SOP with steps and QA checks.

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
