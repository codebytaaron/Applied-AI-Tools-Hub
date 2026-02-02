#!/usr/bin/env python3
from __future__ import annotations
import os
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel

console = Console()

def mock(system, user):
    return "MOCK_MODE output\\n\\nVet clinic template output."

def call_llm(system, user):
    load_dotenv()
    if os.getenv("MOCK_MODE","true").lower() == "true":
        return mock(system, user)
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    r = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL","gpt-4.1-mini"),
        messages=[{"role":"system","content":system},{"role":"user","content":user}],
        temperature=0.2,
    )
    return r.choices[0].message.content or ""

def main():
    from prompt import SYSTEM_PROMPT, USER_TEMPLATE
    raw = open("examples/input.txt","r",encoding="utf-8").read().strip()
    if not raw:
        raise SystemExit("No input provided")
    out = call_llm(SYSTEM_PROMPT, USER_TEMPLATE.format(input=raw))
    with open("out.md","w",encoding="utf-8") as f:
        f.write(out)
    console.print(Panel.fit("Wrote out.md", title="Done"))

if __name__ == "__main__":
    main()
