# Customer Follow-Up Pack

Niche company template: **Drone Photography Service**

## What it does
Creates follow-up messages (text/email) for after service.

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
