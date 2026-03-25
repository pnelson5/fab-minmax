#!/bin/bash
# Ralph Loop: Rapidly implement BDD test specifications
# This script runs one iteration of the ralph loop, then exits for you to verify

set -e  # Exit on error

# Parse optional model argument (defaults to sonnet)
MODEL_ID="${1:-sonnet}"

# Path to the ralph loop prompt
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROMPT_FILE="$SCRIPT_DIR/.opencode/commands/ralph_loop.md"

if [ ! -f "$PROMPT_FILE" ]; then
    echo "Error: Ralph loop prompt not found at $PROMPT_FILE"
    exit 1
fi

echo "Starting Ralph Loop Iteration..."
echo ""
echo "Using model: $MODEL_ID"
echo ""
echo "This will:"
echo "  1. Find the next unchecked rule in tests/BDD_CHECKLIST.md"
echo "  2. Implement BDD tests for that rule"
echo "  3. Verify tests are correct"
echo "  4. Mark the rule complete"
echo "  5. Exit for you to review"
echo ""
echo "Press Ctrl+C to cancel, or Enter to continue..."
read -r

# Use claude CLI with the ralph_loop prompt as system instructions
claude -p \
    --model "$MODEL_ID" \
    --dangerously-skip-permissions \
    --append-system-prompt-file "$PROMPT_FILE" \
    "Execute the Ralph Loop. Find the next unchecked rule in tests/BDD_CHECKLIST.md and implement BDD tests for it, following all steps in your system prompt."

echo ""
echo "Ralph loop iteration complete!"
echo ""
echo "Next steps:"
echo "  1. Review the tests that were just created"
echo "  2. Verify they match the comprehensive rules"
echo "  3. Run this script again to continue: ./ralph.sh"
echo ""
