# Applied AI Tools Hub

A portfolio of AI tools, business prompt templates, and n8n automation workflows by Teddy Aaron. The repository contains **849 top-level project folders**, including **801 Python prompt templates**, plus applications, workflows, and collections with additional nested projects.

**[Browse the full project catalog →](docs/CATALOG.md)** — search by project name, folder, or industry.

## Start here

- **Business templates:** [Job Quote Generator](001-job-quote-generator/), [Lead Triage](01-lead-triage/), and [Content Repurposer](004-content-repurposer/).
- **Automation workflows:** [Lead Booking](Zero-Touch-Lead-Booking-main/), [AI Agent Workflow](Ai-Agent-Workflow-main/), and [NFT Atlas](NFT-Atlas-main/).
- **Applications:** [Orchestra AI](orchestra-ai/), [Honest Grader](Honest-Grader-AI-main/), and [SEO Content Optimizer](SEO-Content-Optimizer-main/).
- **Maintenance:** [Repository guide](docs/MAINTENANCE.md).

Each project is independent. Read its README for dependencies, inputs, and setup; there is no single installation command for the entire repository. Folder names are preserved to keep existing links working.

## Python template setup

For authorized use under the [license](LICENSE), choose a template and run these commands from its folder:

```bash
cd 001-job-quote-generator
python3 -m venv .venv
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
cp .env.example .env
python main.py --in examples/input.txt --out out.md
```

Templates run in `MOCK_MODE=true` by default and produce placeholder output without calling an API. To generate model output, edit `.env`, set `MOCK_MODE=false`, and supply your own `OPENAI_API_KEY`. Adjust `OPENAI_MODEL` as needed. Customize `prompt.py` and the sample input for your task.

## n8n workflows

Workflow folders contain JSON exports. Import the workflow into your n8n instance, configure your own credentials, and review node settings and integrations before enabling it. Consult the individual project README for details.

Some projects are also used at [Zylos](https://zylos.us/automation.html).

## License

© 2026 Teddy Aaron. All rights reserved. Public to view only. Don't copy, reuse, deploy or redistribute any of it without written permission. See [LICENSE](LICENSE).
