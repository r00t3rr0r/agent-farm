#!/usr/bin/env python3
"""
validate.py – Validates generated YAML files against JSON schemas
and checks that required CLI tools are available.
"""
import yaml
import json
import sys
import subprocess
from pathlib import Path
from jsonschema import validate as js_validate, ValidationError

SCHEMAS = {
    "agent": Path("schemas/agent_schema.json"),
    "workflow": Path("schemas/workflow_schema.json"),
}

REQUIRED_TOOLS = ["python3", "git", "sqlite3"]


def check_yaml(path: Path) -> bool:
    try:
        yaml.safe_load(path.read_text())
        return True
    except Exception as e:
        print(f"  ❌ YAML parse error [{path.name}]: {e}")
        return False


def check_schema(yml_path: Path, schema: dict) -> bool:
    data = yaml.safe_load(yml_path.read_text())
    try:
        js_validate(instance=data, schema=schema)
        print(f"  ✅ Schema valid: {yml_path.name}")
        return True
    except ValidationError as e:
        print(f"  ❌ Schema invalid [{yml_path.name}]: {e.message}")
        return False


def check_tools(tools: list) -> bool:
    ok = True
    for t in tools:
        result = subprocess.run(["which", t], capture_output=True)
        if result.returncode == 0:
            print(f"  ✅ Tool found: {t}")
        else:
            print(f"  ⚠️  Tool not found: {t} (optional tools may be skipped)")
            ok = False
    return ok


def main():
    all_ok = True

    for kind, schema_path in SCHEMAS.items():
        if not schema_path.exists():
            print(f"⚠️  Schema file missing: {schema_path} (skipping {kind} validation)")
            continue

        schema = json.loads(schema_path.read_text())
        folder = Path("agents") if kind == "agent" else Path("workflows")

        if not folder.exists():
            print(f"⚠️  Folder missing: {folder} (run generate.py first)")
            continue

        yaml_files = [f for f in folder.glob("*.yaml") if f.name != ".gitkeep"]
        if not yaml_files:
            print(f"⚠️  No {kind} YAML files found in {folder}/")
            continue

        print(f"\n🔍 Validating {kind}s...")
        for yml in yaml_files:
            if not check_yaml(yml):
                all_ok = False
                continue
            if not check_schema(yml, schema):
                all_ok = False

    print("\n🔧 Checking required tools...")
    check_tools(REQUIRED_TOOLS)

    print()
    if all_ok:
        print("✅ All validations passed.")
    else:
        print("❌ Some validations failed. Review errors above.")
    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
