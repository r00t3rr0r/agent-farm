#!/usr/bin/env python3
"""
demo.py – Generates deterministic demo outputs so users can preview the system.
"""
from __future__ import annotations

import json
from pathlib import Path

from mock_runtime import mock_inference

DEMO_OUT = Path("storage/demo")

DEMO_CASES = [
    {
        "agent_id": "tech_writer_agent",
        "name": "tech_writer",
        "title": "API-Dokumentation Demo",
        "prompt": "Erzeuge eine kurze API-Dokumentation fuer POST /invoices inklusive Beispielrequest.",
        "artifact_name": "tech_writer_demo.md",
        "artifact_content": """# POST /invoices

Erstellt eine neue Rechnung im System.

## Request

```json
{
  "customer_id": "cust_1001",
  "amount": 249.90,
  "currency": "EUR"
}
```

## Response

```json
{
  "invoice_id": "inv_2026_0001",
  "status": "created"
}
```
""",
    },
    {
        "agent_id": "automation_architect_agent",
        "name": "lowcode",
        "title": "Low-Code Workflow Demo",
        "prompt": "Baue einen einfachen Lead-Import-Workflow fuer CSV -> Validierung -> CRM.",
        "artifact_name": "lowcode_demo.json",
        "artifact_content": json.dumps(
            {
                "workflow": "lead-import",
                "steps": [
                    {"type": "csv_trigger"},
                    {"type": "validate_email"},
                    {"type": "upsert_crm_contact"},
                ],
                "status": "demo-preview",
            },
            indent=2,
        ),
    },
    {
        "agent_id": "qa_test_architect_agent",
        "name": "qa",
        "title": "QA-Test Demo",
        "prompt": "Erzeuge einen Playwright-Test fuer Login mit erfolgreichem Redirect zum Dashboard.",
        "artifact_name": "qa_demo.spec.ts",
        "artifact_content": """import { test, expect } from '@playwright/test';

test('login redirects to dashboard', async ({ page }) => {
  await page.goto('/login');
  await page.getByLabel('Email').fill('demo@example.com');
  await page.getByLabel('Password').fill('secret-demo');
  await page.getByRole('button', { name: 'Login' }).click();
  await expect(page).toHaveURL(/dashboard/);
});
""",
    },
]


def write_demo_case(case: dict) -> dict:
    result = mock_inference(case["agent_id"], case["prompt"])
    artifact_path = DEMO_OUT / case["artifact_name"]
    artifact_path.write_text(case["artifact_content"], encoding="utf-8")
    return {
        "title": case["title"],
        "agent_id": case["agent_id"],
        "preview": result["choices"][0]["message"]["content"],
        "artifact": str(artifact_path),
    }


def main() -> None:
    DEMO_OUT.mkdir(parents=True, exist_ok=True)

    print("🎬 Agent Farm Demo")
    print("==================")
    print("Generating deterministic preview outputs...\n")

    summary = {"cases": []}
    for case in DEMO_CASES:
        demo_case = write_demo_case(case)
        summary["cases"].append(demo_case)
        print(f"✅ {demo_case['title']}")
        print(f"   Agent: {demo_case['agent_id']}")
        print(f"   Preview: {demo_case['preview']}")
        print(f"   Artifact: {demo_case['artifact']}\n")

    summary_path = DEMO_OUT / "demo_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print("📦 Demo artifacts written to storage/demo/")
    print(f"🧾 Summary: {summary_path}")


if __name__ == "__main__":
    main()
