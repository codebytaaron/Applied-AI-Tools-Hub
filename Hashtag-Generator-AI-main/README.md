# Hashtag Gen AI

A working hashtag generator that creates platform-ready hashtags from a caption + context.

- Runs with a local LLM (Ollama) for smarter tags
- Automatically falls back to a rules-based generator if Ollama is not running
- Includes a clean dark UI

## Setup

### 1) Create venv and install deps
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
