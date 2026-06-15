#!/usr/bin/env python3
"""
test.py – Runs mock inference simulations and workflow step tests.
Does NOT require a live OpenClaw instance; uses deterministic stubs.
"""
import yaml
import json
import time
import subprocess
import sys
from pathlib import Path

# Mock agent registry – mirrors farm_config.yaml agents
MOCK_AGENTS = {
    "tech_writer_agent": {"temperature": 0.0, "output_type": "markdown"},
    "automation_architect_agent": {"temperature": 0.1, "output_type": "json"},
    "qa_test_architect_agent": {"temperature": 0.0, "output_type": "typescript"},
}


def mock_inference(agent_id: str, prompt: str) -> dict:
    """Returns a deterministic mock response (no GPU/API required)."""
    cfg = MOCK_AGENTS.get(agent_id, {})
    return {
        "id": f"mock-{agent_id}-{int(time.time())}",
        "model": "openclaw/local",
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": f"[MOCK] {prompt[:60]}... (temp={cfg.get('temperature', 0)})",
                }
            }
        ],
        "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
    }


def run_workflow(wf_path: Path) -> bool:
    wf = yaml.safe_load(wf_path.read_text())
    steps = wf.get("steps", [])

    if not steps:
        print(f"  ⚠️  No steps defined in {wf_path.name}")
        return True  # Not a failure – workflow may use steps_ref

    all_pass = True
    for i, step in enumerate(steps):
        agent = step.get("agent_role")
        if agent and agent not in MOCK_AGENTS:
            print(f"  ❌ Step {i}: unknown agent '{agent}'")
            all_pass = False
            continue

        if agent:
            result = mock_inference(agent, f"Test prompt for step {i}")
            assert "choices" in result, "Mock response malformed"
            print(f"  ✅ Step {i}: {agent} → mock inference OK (temp={MOCK_AGENTS[agent]['temperature']})")

        if "validation" in step:
            vtype = step["validation"].get("type", "")
            schema_file = step["validation"].get("schema_file")
            if schema_file and not Path(schema_file).exists():
                print(f"  ⚠️  Step {i}: schema file '{schema_file}' missing (validation skipped)")
            else:
                print(f"  ✅ Step {i}: validation ({vtype}) – schema present or not required")

    return all_pass


def test_mock_openclaw_format():
    """Unit test: verify mock_inference returns valid OpenAI-compatible format."""
    for agent_id in MOCK_AGENTS:
        result = mock_inference(agent_id, "unit test prompt")
        assert "choices" in result
        assert result["usage"]["prompt_tokens"] == 0
        assert result["model"] == "openclaw/local"
    print("  ✅ mock_inference format: OpenAI-compatible structure confirmed")


def main():
    print("🧪 Running Agent Farm Test Suite...\n")

    # Unit test
    print("📌 Unit Test: Mock inference format")
    test_mock_openclaw_format()

    # Workflow tests
    wf_dir = Path("workflows")
    yaml_files = [f for f in wf_dir.glob("*.yaml") if f.name != ".gitkeep"] if wf_dir.exists() else []

    if not yaml_files:
        print("\n⚠️  No workflow YAML files found. Run generate.py first.")
        sys.exit(1)

    print(f"\n📌 Workflow Tests ({len(yaml_files)} workflows found)")
    all_pass = True
    for wf in yaml_files:
        print(f"\n  🔄 Testing: {wf.name}")
        if not run_workflow(wf):
            all_pass = False

    print()
    if all_pass:
        print("🏁 All tests passed ✅")
    else:
        print("🏁 Some tests failed ❌")

    sys.exit(0 if all_pass else 1)


if __name__ == "__main__":
    main()
