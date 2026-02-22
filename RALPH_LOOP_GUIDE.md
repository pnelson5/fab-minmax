# Ralph Loop Guide

## Overview

The Ralph Loop is a rapid BDD test specification system that lets you quickly implement tests for all 90 sections of the Flesh and Blood Comprehensive Rules.

## What You Have

### 1. Slash Command: `/ralph-loop`
**Location:** `.opencode/commands/ralph_loop.md`

**What it does:**
- Finds the next unchecked rule in `tests/BDD_TESTS_README.md`
- Calls `/implement-bdd-rule` to write tests
- Verifies tests are correct
- Marks section complete
- Exits for you to review

### 2. Manual Script: `ralph.sh`
**Usage:** `./ralph.sh [model]`

**Best for:** Careful, step-by-step implementation with manual review

```bash
# Run one iteration (default model)
./ralph.sh

# Run with specific model
./ralph.sh anthropic/claude-sonnet-4-6

# Review the tests created
# When satisfied, run again
./ralph.sh

# Repeat 90 times...
```

### 3. Automated Script: `ralph-auto.sh`
**Usage:** `./ralph-auto.sh [N] [model]`

**Best for:** Implementing multiple rules at once

```bash
# Run 5 iterations automatically (default model)
./ralph-auto.sh 5

# Run 5 iterations with specific model
./ralph-auto.sh 5 anthropic/claude-sonnet-4-6

# Review all 5 test files created
# Continue with more
./ralph-auto.sh 10 anthropic/claude-opus-4-6
```

### Model Selection

**See `MODEL_SELECTION.md` for complete details**

**Quick recommendations:**
- **Opus 4.5**: Best quality, slower, for complex rules
- **Sonnet 4.5**: Balanced, recommended default ⭐
- **Haiku 4.5**: Fastest, for simple rules or large batches

```bash
# List available models
opencode models anthropic

# Use recommended default
./ralph.sh anthropic/claude-sonnet-4-5
```

## Recommended Workflow

### Option 1: Slow and Steady (Recommended for First 10 Rules)
```bash
# Implement one rule at a time
./ralph.sh

# After each run:
# 1. Review tests/features/section_X_Y_Z.feature
# 2. Review tests/step_defs/test_section_X_Y_Z.py
# 3. Run: uv run pytest tests/step_defs/test_section_X_Y_Z.py -v
# 4. Verify tests fail for the right reasons
# 5. When happy, run ./ralph.sh again

# Repeat until comfortable with the process
```

### Option 2: Batch Processing (After You're Comfortable)
```bash
# Run 5 iterations
./ralph-auto.sh 5

# Review all 5 files created
# Run all tests: uv run pytest tests/step_defs/ -v

# Continue in batches
./ralph-auto.sh 10
./ralph-auto.sh 20
# etc.
```

### Option 3: Full Auto (For the Brave)
```bash
# Run all remaining rules at once
# First, count how many are left:
grep -c "^\- \[ \]" tests/BDD_TESTS_README.md

# If 85 rules remaining:
./ralph-auto.sh 85

# Go get coffee ☕
# Come back and review all ~85 test files!
```

## How It Works

### The Flow

```
┌─────────────────────────────────────────────────────────┐
│  ralph.sh / ralph-auto.sh                               │
│  (Bash script)                                          │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│  opencode run "/ralph-loop"                             │
│  (Calls OpenCode CLI)                                   │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│  /ralph-loop command                                    │
│  (Slash command in .opencode/commands/)                 │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ├─── 1. Find next [ ] rule in checklist
                      │
                      ├─── 2. Call /implement-bdd-rule X.Y Name
                      │         │
                      │         ├─── Research rules
                      │         ├─── Plan scenarios
                      │         ├─── Write feature file
                      │         ├─── Write step definitions
                      │         ├─── Update helpers
                      │         ├─── Run tests
                      │         ├─── Update docs
                      │         └─── Complete
                      │
                      ├─── 3. Verify tests
                      │         ├─── Files exist
                      │         ├─── Tests collect
                      │         └─── Fail correctly
                      │
                      ├─── 4. Mark [x] in checklist
                      │
                      └─── 5. Exit with summary
```

### What Gets Created Each Iteration

```
tests/
├── features/
│   └── section_X_Y_Z_name.feature          ← NEW
├── step_defs/
│   └── test_section_X_Y_Z_name.py          ← NEW
└── BDD_TESTS_README.md                     ← UPDATED (marked complete)
```

## Verification After Each Run

### Quick Check (30 seconds)
```bash
# 1. Check files exist
ls tests/features/section_*.feature | tail -1
ls tests/step_defs/test_section_*.py | tail -1

# 2. Run the new tests
uv run pytest tests/step_defs/test_section_*.py -v | tail -20

# 3. Check for expected failures
# Should see: AttributeError, NotImplementedError, AssertionError
# Should NOT see: SyntaxError, ImportError, NameError
```

### Full Review (5 minutes)
```bash
# 1. Read the feature file
cat tests/features/section_X_Y_Z_name.feature

# 2. Check it matches comprehensive rules
# Open fab-rules/en-fab-cr.md and compare

# 3. Read the step definitions
cat tests/step_defs/test_section_X_Y_Z_name.py

# 4. Run tests with verbose output
uv run pytest tests/step_defs/test_section_X_Y_Z_name.py -vv

# 5. Verify checklist updated
grep "X.Y" tests/BDD_TESTS_README.md
```

## Troubleshooting

### "opencode: command not found"
```bash
# Install opencode
brew install opencode
# or
npm install -g @opencode/cli
```

### "Permission denied: ./ralph.sh"
```bash
chmod +x ralph.sh ralph-auto.sh
```

### "Tests have syntax errors"
The `/ralph-loop` command should have caught this. If you see syntax errors:
1. Fix them manually in the test file
2. Re-run tests to verify
3. Continue with next iteration

### "All tests are passing"
This is unusual - tests should fail because engine features don't exist yet.

Check if:
- The engine already implements this rule (rare)
- Tests are too simple and don't actually test anything
- Test assertions are backwards

Review the test logic carefully.

### "Can't find next rule"
If you see "No unchecked rules found":
```bash
# Check the checklist
cat tests/BDD_TESTS_README.md | grep "^\- \[ \]"

# If empty, congratulations! All 90 sections complete! 🎉
```

## Progress Tracking

### Check Overall Progress
```bash
# Count completed sections
grep -c "^\- \[x\]" tests/BDD_TESTS_README.md

# Count remaining sections  
grep -c "^\- \[ \]" tests/BDD_TESTS_README.md

# List remaining sections
grep "^\- \[ \]" tests/BDD_TESTS_README.md
```

### Check Test Coverage
```bash
# Count test files
ls tests/features/*.feature | wc -l
ls tests/step_defs/test_*.py | wc -l

# Run all tests
uv run pytest tests/step_defs/ -v

# Count passing vs failing
uv run pytest tests/step_defs/ -v | grep -E "(PASSED|FAILED)" | wc -l
```

## Expected Timeline

### Conservative (Manual Review Each)
- **Time per rule:** ~10 minutes (AI writes tests + you review)
- **Total time:** 90 rules × 10 min = **15 hours**
- **Spread over:** ~2 weeks at 1-2 hours/day

### Aggressive (Batch Processing)
- **Time per batch:** ~30 minutes (AI writes 5 rules + you review all)
- **Total time:** 18 batches × 30 min = **9 hours**
- **Spread over:** ~1 week at 1-2 hours/day

### Full Auto (Maximum Speed)
- **Time:** 90 rules in one session = **~3-4 hours AI time + 2 hours review**
- **Total time:** ~6 hours
- **Spread over:** 1-2 days

## Tips for Success

### DO ✅
- Start with manual mode (`./ralph.sh`) for first 5-10 rules
- Review tests carefully in the beginning
- Switch to batch mode once you trust the process
- Take breaks - reviewing tests requires focus
- Keep `fab-rules/en-fab-cr.md` open for reference

### DON'T ❌
- Don't run 90 iterations on your first try
- Don't skip reviewing the first 10 tests
- Don't try to fix failing tests (they should fail!)
- Don't modify engine code during this phase
- Don't forget to verify tests fail for the RIGHT reasons

## Next Phase: Engine Implementation

After all 90 rule sections have tests:

```bash
# Check all tests are red (failing)
uv run pytest tests/step_defs/ -v

# Expected: ~500+ failing tests

# Then start engine implementation (separate phase)
/implement-engine-feature "1.1 Players"
/implement-engine-feature "1.2 Objects"
# etc.

# Goal: All tests green ✅
```

## Summary

You have three ways to run the ralph loop:

| Method | Command | Use Case |
|--------|---------|----------|
| **Interactive** | `/ralph-loop` | One-off, in OpenCode TUI |
| **Manual** | `./ralph.sh` | Careful, step-by-step |
| **Automated** | `./ralph-auto.sh N` | Batch processing |

All three do the same thing - pick next rule, write tests, verify, mark complete, exit.

The difference is how many iterations and how automated.

Start with `./ralph.sh` and work your way up! 🚀
