#!/bin/bash
# Ralph Loop: Rapidly implement BDD test specifications
# This script runs one iteration of the ralph loop, then exits for you to verify

set -e  # Exit on error

# Parse optional model argument (defaults to anthropic/claude-sonnet-4-6)
MODEL_ID="${1:-anthropic/claude-sonnet-4-6}"

echo "Starting Ralph Loop Iteration..."
echo ""
echo "Using model: $MODEL_ID"
echo ""
echo "This will:"
echo "  1. Find the next unchecked rule in tests/BDD_TESTS_README.md"
echo "  2. Implement BDD tests for that rule"
echo "  3. Verify tests are correct"
echo "  4. Mark the rule complete"
echo "  5. Exit for you to review"
echo ""
echo "Press Ctrl+C to cancel, or Enter to continue..."
read -r

# Use --command to invoke the ralph_loop slash command directly
opencode run --model "$MODEL_ID" --command ralph_loop

echo ""
echo "Ralph loop iteration complete!"
echo ""
echo "Next steps:"
echo "  1. Review the tests that were just created"
echo "  2. Verify they match the comprehensive rules"
echo "  3. Run this script again to continue: ./ralph.sh"
echo ""
