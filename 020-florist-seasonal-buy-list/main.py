#!/usr/bin/env python3
import os
from dotenv import load_dotenv

def main():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--in", dest="inp", default="examples/input.txt")
    p.add_argument("--out", dest="out", default="out.md")
    a = p.parse_args()

    raw = open(a.inp).read().strip()
    if not raw:
        raise SystemExit("No input provided")

    from prompt import SYSTEM_PROMPT, USER_TEMPLATE
    load_dotenv()

    if os.getenv("MOCK_MODE","true").lower()=="true":
        out = "MOCK_MODE output\n\n" + raw
    else:
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        r = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL","gpt-4.1-mini"),
            messages=[
                {"role":"system","content":SYSTEM_PROMPT},
                {"role":"user","content":USER_TEMPLATE.format(input=raw)}
            ],
            temperature=0.2
        )
        out = r.choices[0].message.content or ""

    open(a.out,"w").write(out)

if __name__=="__main__":
    main()
