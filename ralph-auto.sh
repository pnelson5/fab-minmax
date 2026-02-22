#!/bin/bash
# Ralph Loop: Automated - Run multiple iterations
# This script runs N iterations of the ralph loop automatically
# Usage: ./ralph-auto.sh [iterations] [model]
#   ./ralph-auto.sh 5                    # 5 iterations, default model (anthropic/claude-sonnet-4-6)
#   ./ralph-auto.sh 5 anthropic/claude-sonnet-4-6  # 5 iterations, specific model

set -e  # Exit on error

# Parse arguments
ITERATIONS=${1:-1}
MODEL_ID="${2:-anthropic/claude-sonnet-4-6}"
MODEL="--model $MODEL_ID"

echo "🚀 Starting Automated Ralph Loop..."
echo ""
echo "Configuration:"
echo "  Iterations: $ITERATIONS"
echo "  Model: $MODEL_ID"
echo "  Pause between iterations: 5 seconds"
echo ""
echo "This will automatically:"
echo "  1. Find the next unchecked rule"
echo "  2. Implement BDD tests"
echo "  3. Verify tests"
echo "  4. Mark complete"
echo "  5. Repeat $ITERATIONS times"
echo ""
echo "⚠️  WARNING: This runs unattended. Review the results carefully after!"
echo ""
echo "Press Ctrl+C to cancel, or Enter to continue..."
read -r

for i in $(seq 1 "$ITERATIONS"); do
    echo ""
    echo "═══════════════════════════════════════════════════════════════"
    echo "  Iteration $i of $ITERATIONS"
    echo "═══════════════════════════════════════════════════════════════"
    echo ""
    
    # Run opencode with the /ralph-loop command
    opencode run $MODEL "/ralph-loop"
    
    echo ""
    echo "✅ Iteration $i complete!"
    
    # Pause between iterations (except on last one)
    if [ "$i" -lt "$ITERATIONS" ]; then
        echo ""
        echo "Pausing 5 seconds before next iteration..."
        sleep 5
    fi
done

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "  🎉 ALL $ITERATIONS ITERATIONS COMPLETE! 🎉"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "Next steps:"
echo "  1. Review all tests created in tests/features/ and tests/step_defs/"
echo "  2. Check tests/BDD_TESTS_README.md for updated checklist"
echo "  3. Run tests: uv run pytest tests/step_defs/ -v"
echo "  4. Continue with: ./ralph-auto.sh <N> for N more iterations"
echo ""
