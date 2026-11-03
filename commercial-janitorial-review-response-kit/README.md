# Review Response Kit

Niche company template: **Commercial Janitorial**

## What it does
Creates response templates for reviews (1–5 stars).

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
