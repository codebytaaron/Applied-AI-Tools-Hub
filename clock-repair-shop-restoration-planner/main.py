#!/usr/bin/env python3
import os
from dotenv import load_dotenv
from rich.console import Console

console = Console()

def mock():
    return "MOCK_MODE output\n\nNiche business template result."

def call_llm(system, user):
    load_dotenv()
    if os.getenv("MOCK_MODE","true").lower() == "true":
        return mock()
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

    console.print("[green]Wrote out.md[/green]")

if __name__ == "__main__":
    main()
