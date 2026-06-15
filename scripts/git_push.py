#!/usr/bin/env python3
"""
git_push.py – Atomic Git automation: add → commit (conventional) → tag → push.
Run after generate + validate + test to push a verified farm snapshot.
"""
import subprocess
import sys
import datetime


def run(cmd: str) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, shell=True, capture_output=True, text=True)


def main():
    # Check for changes
    status = run("git status --porcelain")
    if not status.stdout.strip():
        print("ℹ️  No changes to commit. Working tree is clean.")
        sys.exit(0)

    # Generate version tag
    tag = f"farm-v{datetime.datetime.now().strftime('%Y%m%d%H%M')}"

    print(f"📦 Preparing commit: {tag}")

    # Stage all relevant files
    run("git add agents/ workflows/ prompts/ schemas/ scripts/ templates/ farm_config.yaml requirements.txt run.sh docs/")

    msg = f"chore(farm): auto-generate & validate [{tag}]\n\nCo-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
    commit = run(f'git commit -m "{msg}"')

    if "nothing to commit" in commit.stdout:
        print("ℹ️  Nothing staged to commit.")
        sys.exit(0)

    if commit.returncode != 0:
        print(f"❌ Commit failed:\n{commit.stderr}")
        sys.exit(1)

    print(f"  ✅ Committed: {commit.stdout.strip()}")

    # Tag the snapshot
    tag_out = run(f'git tag -a {tag} -m "Agent Farm Snapshot {tag}"')
    if tag_out.returncode != 0:
        print(f"⚠️  Tagging failed (non-fatal): {tag_out.stderr.strip()}")

    # Push with tags
    push = run("git push origin main --tags")
    if push.returncode == 0:
        print(f"✅ Pushed & tagged: {tag}")
    else:
        print(f"❌ Git push failed:\n{push.stderr}")
        sys.exit(1)


if __name__ == "__main__":
    main()
