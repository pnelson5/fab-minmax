# Quick Start: Implementing BDD Rules

## Overview

You now have a complete system for implementing BDD tests for all Flesh and Blood comprehensive rules using a ralph (rapid implementation) loop.

## The Setup

### 1. Comprehensive Rules with Links
- **File**: `fab-rules/en-fab-cr.md`
- **Features**: 
  - All rule references are clickable links: `[1.0.1a](#101a)`
  - HTML anchors for every rule: `<a id="102a"></a>`
  - Searchable via qmd
  - Examples in blockquotes

### 2. Slash Command
- **Command**: `/implement-bdd-rule <section> [name]`
- **Location**: `.opencode/commands/implement_bdd_rule.md`
- **Purpose**: Step-by-step guidance for implementing each rule's tests

### 3. Test Checklist
- **File**: `tests/BDD_TESTS_README.md`
- **Contents**: Exhaustive checklist of all 90+ rule sections
- **Status**: 1 complete (1.0.2 Precedence), 89 to go

## Ralph Loop Workflow

**See `RALPH_LOOP_GUIDE.md` for complete details**

### Three Ways to Run

| Method | Command | Use Case |
|--------|---------|----------|
| **Interactive** | `/ralph-loop` | One-off in OpenCode TUI |
| **Manual** | `./ralph.sh` | Step-by-step with review |
| **Automated** | `./ralph-auto.sh N` | Batch processing |

### Quickstart

```bash
# Option 1: Manual (recommended first)
./ralph.sh
# Review tests, then run again

# Option 2: Batch of 5
./ralph-auto.sh 5
# Review all 5, then continue

# Option 3: In OpenCode TUI
/ralph-loop
# Runs one iteration
```

### What Happens Each Iteration

1. Finds next `[ ]` rule in checklist
2. Calls `/implement-bdd-rule` to write tests
3. Verifies tests are correct
4. Marks `[x]` in checklist
5. Exits for you to review

## Example Session

```bash
# You want to implement rule 1.1 (Players)
/implement-bdd-rule 1.1 Players

# Assistant will:
# 1. Read fab-rules/en-fab-cr.md section 1.1
# 2. Follow links to understand dependencies
# 3. Extract examples from blockquotes
# 4. Create todo list for all scenarios
# 5. Write tests/features/section_1_1_players.feature
# 6. Write tests/step_defs/test_section_1_1_players.py
# 7. Update tests/bdd_helpers.py if needed
# 8. Run: uv run pytest tests/step_defs/test_section_1_1_players.py -v
# 9. Update tests/BDD_TESTS_README.md with documentation
# 10. Mark [x] 1.1: Players in the checklist
```

## Key Files

```
.opencode/commands/implement_bdd_rule.md   # The slash command
tests/BDD_TESTS_README.md                  # The checklist
fab-rules/en-fab-cr.md                     # Rules with links
BDD_TEST_PHILOSOPHY.md                     # ⚠️ READ THIS FIRST
convert_to_md.py                           # Conversion script
tests/bdd_helpers.py                       # Test helpers
tests/features/                            # Gherkin scenarios
tests/step_defs/                           # Step definitions
```

## ⚠️ Critical Philosophy - READ FIRST

**See `BDD_TEST_PHILOSOPHY.md` for complete details**

### You Are Writing Specifications, Not Implementations

When running `/implement-bdd-rule`, you write TESTS that define what the engine MUST do. You do NOT implement engine features.

**Tests SHOULD fail** - that's expected and correct!

### Good vs Bad Failures

```python
# ✅ GOOD - Expected failure (missing engine feature):
AttributeError: 'Player' has no attribute 'card_pool'
→ Document what's needed, move on to next rule

# ❌ BAD - Unexpected failure (broken test):  
SyntaxError: invalid syntax in test file
→ Fix the test code, re-run
```

### The Two Phases

**Phase 1: Write Test Specs** ← `/implement-bdd-rule` does this
- Write tests based on comprehensive rules
- Tests fail (expected!)
- Document engine requirements
- Move to next rule

**Phase 2: Implement Engine** ← Separate task, done later
- Read test specs
- Implement engine features
- Tests pass
- Done!

## Tips for Success

### DO ✅
- Use clickable links to understand rule context
- Extract examples from the rulebook for test scenarios
- Use real engine components (via bdd_helpers.py)
- **Write tests that FAIL due to missing engine features**
- Document what engine features are needed
- Fix broken TEST code (syntax, imports, fixtures)
- Mark sections complete when tests fail for RIGHT reasons
- Move on to next rule

### DON'T ❌
- Skip reading related rules (follow the links!)
- Write mocks instead of using real engine
- Combine multiple rules in one scenario
- **Try to make tests pass by implementing engine code**
- **Modify any files in `fab_engine/` directory**
- Feel bad about red tests (they're supposed to be red!)
- Forget to update the checklist

## Useful Commands

```bash
# Search rules
uv run python fab_search.py "attack step" -n 5
/fab_search "restriction precedence" -n 10

# Run tests
uv run pytest tests/step_defs/test_section_X_Y_Z.py -v
uv run pytest tests/step_defs/ -v  # Run all BDD tests

# Reconvert rules (if needed)
uv run python convert_to_md.py
cd fab-rules && qmd update && qmd embed
```

## Current Status

- **Tests Implemented**: 1 (Section 1.0.2 Precedence)
- **Tests Remaining**: ~89 rule sections
- **Ready to Start**: Yes! Pick any unchecked rule from the list

## First Rule to Implement

Suggested starting points:
- `1.1 Players` - Fundamental game concept
- `1.3 Cards` - Core object type
- `2.1 Color` - Simple property to test
- `3.9 Hand` - Essential zone

Just run:
```bash
/implement-bdd-rule 1.1 Players
```

And let the ralph loop begin! 🚀
