#!/usr/bin/env bash
# run.sh – One-command Agent Farm Pipeline
# Usage: ./run.sh [deploy|test-only|demo]
set -e

MODE=${1:-deploy}
echo "🚀 Agent Farm Pipeline | Mode: $MODE"
echo "================================================"

# Step 1: Generate agents & workflows from config
echo ""
echo "📝 Step 1/4: Generating agents & workflows..."
python3 scripts/generate.py

# Step 2: Validate YAML syntax + JSON schemas + tools
echo ""
echo "🔍 Step 2/4: Validating..."
python3 scripts/validate.py || { echo "❌ Validation failed. Aborting."; exit 1; }

# Step 3: Run mock-inference workflow tests
echo ""
echo "🧪 Step 3/4: Running tests..."
python3 scripts/test.py || { echo "❌ Tests failed. Aborting."; exit 1; }

if [[ "$MODE" == "demo" ]]; then
    echo ""
    echo "🎬 Step 4/4: Running demo preview..."
    python3 scripts/demo.py
elif [[ "$MODE" == "deploy" ]]; then
    echo ""
    echo "📤 Step 4/4: Pushing to Git..."
    python3 scripts/git_push.py
fi

echo ""
echo "================================================"
echo "✅ Pipeline complete."
