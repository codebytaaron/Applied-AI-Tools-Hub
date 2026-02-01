#!/usr/bin/env python3
from __future__ import annotations
import os, sys
from typing import Optional
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel

console = Console()

def _mock(system: str, user: str) -> str:
    seed = abs(hash(system + "\\n" + user)) % 99991
    return (
        "MOCK_MODE output\\n"
        f"seed={seed}\\n\\n"
        "Placeholder output. Set MOCK_MODE=false and add OPENAI_API_KEY for real outputs."
    )

def call_llm(system: str, user: str) -> str:
    load_dotenv()
    if os.getenv("MOCK_MODE","true").lower() == "true":
        return _mock(system, user)
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    r = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL","gpt-4.1-mini"),
        messages=[{"role":"system","content":system},{"role":"user","content":user}],
        temperature=0.2,
    )
    return r.choices[0].message.content or ""

def read_input(path: Optional[str]) -> str:
    if path:
        return open(path,"r",encoding="utf-8").read()
    if not sys.stdin.isatty():
        return sys.stdin.read()
    return ""

def main():
    import argparse
    p = argparse.ArgumentParser(description="Run this local-business AI template")
    p.add_argument("--in", dest="inp", default="examples/input.txt")
    p.add_argument("--out", dest="out", default="out.md")
    a = p.parse_args()
    from prompt import SYSTEM_PROMPT, USER_TEMPLATE
    raw = read_input(a.inp).strip()
    if not raw:
        raise SystemExit("No input provided")
    out = call_llm(SYSTEM_PROMPT, USER_TEMPLATE.format(input=raw))
    with open(a.out,"w",encoding="utf-8") as f:
        f.write(out)
    console.print(Panel.fit(f"Wrote {a.out}", title="Done", border_style="green"))

if __name__ == "__main__":
    main()
