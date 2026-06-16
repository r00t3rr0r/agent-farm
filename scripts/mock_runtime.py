#!/usr/bin/env python3
"""
mock_runtime.py – Shared deterministic mock runtime for tests and demos.
"""
from __future__ import annotations

import time

MOCK_AGENTS = {
    "tech_writer_agent": {"temperature": 0.0, "output_type": "markdown"},
    "automation_architect_agent": {"temperature": 0.1, "output_type": "json"},
    "qa_test_architect_agent": {"temperature": 0.0, "output_type": "typescript"},
}


def mock_inference(agent_id: str, prompt: str) -> dict:
    """Return a deterministic OpenAI-compatible mock response."""
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
