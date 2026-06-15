#!/usr/bin/env python3
"""
generate.py – Reads farm_config.yaml and generates agent + workflow YAML files
using Jinja2 templates. Outputs are versioned with a config hash.
"""
import yaml
import json
import hashlib
import os
import sys
from pathlib import Path
from jinja2 import Template, TemplateNotFound

TEMPLATES_DIR = Path("templates/j2")
AGENTS_OUT = Path("agents")
WORKFLOWS_OUT = Path("workflows")


def hash_cfg(data: dict) -> str:
    return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()[:8]


def render(template_path: Path, ctx: dict) -> str:
    if not template_path.exists():
        raise FileNotFoundError(f"Template not found: {template_path}")
    tpl = Template(template_path.read_text())
    return tpl.render(**ctx)


def main():
    cfg_path = Path("farm_config.yaml")
    if not cfg_path.exists():
        print("❌ farm_config.yaml not found.")
        sys.exit(1)

    with open(cfg_path) as f:
        cfg = yaml.safe_load(f)

    os.makedirs(AGENTS_OUT, exist_ok=True)
    os.makedirs(WORKFLOWS_OUT, exist_ok=True)

    agents = cfg.get("agents", [])
    workflows = cfg.get("workflows", [])

    for a in agents:
        out = AGENTS_OUT / f"{a['id']}.yaml"
        ctx = {**a, "version_hash": hash_cfg(a)}
        out.write_text(render(TEMPLATES_DIR / "agent.yaml.j2", ctx), encoding="utf-8")
        print(f"  📝 Agent generated: {out}")

    for w in workflows:
        out = WORKFLOWS_OUT / f"{w['id']}.yaml"
        ctx = {**w, "version_hash": hash_cfg(w)}
        out.write_text(render(TEMPLATES_DIR / "workflow.yaml.j2", ctx), encoding="utf-8")
        print(f"  📝 Workflow generated: {out}")

    print(f"\n✅ Generated {len(agents)} agents & {len(workflows)} workflows.")


if __name__ == "__main__":
    main()
