---
description: Ralph loop - Rapidly implement BDD test specifications for the next unchecked rule
---

# Ralph Loop: Rapid BDD Test Implementation

**This command implements ONE rule section's tests, then exits for you to verify and continue.**

## CRITICAL: THIS IS A TEST SPECIFICATION TASK, NOT AN ENGINE IMPLEMENTATION TASK

**DO NOT IMPLEMENT ENGINE FEATURES TO MAKE TESTS PASS**

Your job:
- Write tests that accurately reflect the comprehensive rules
- Verify tests are syntactically correct
- Document what engine features are needed
- Move on

Your job is **NOT**:
- Implement missing engine features in `fab_engine/`
- Make tests pass by writing engine code
- Fix "failures" that are actually missing engine features

**Tests SHOULD fail** because the engine doesn't implement these rules yet. That's the whole point of BDD - write the spec first, implement later.

## What This Does

1. Reads `tests/BDD_TESTS_README.md` to find the next unchecked rule
2. Researches the rule section in the comprehensive rules document
3. Plans and writes BDD test scenarios (feature file + step definitions)
4. Verifies tests were written correctly
5. Updates the checklist to mark section complete
6. Exits so you can review and start next iteration

## Usage

```bash
/ralph-loop
```

That's it! No arguments needed. The command:
- Finds the next `[ ]` (unchecked) rule in the checklist
- Implements that rule's tests
- Marks it `[x]` (complete)
- Exits

## The Loop

```bash
# Iteration 1
/ralph-loop
# -> Implements 1.0: General
# -> Exits

# You review the tests, verify they look good

# Iteration 2
/ralph-loop
# -> Implements 1.1: Players
# -> Exits

# You review the tests, verify they look good

# Iteration 3
/ralph-loop
# -> Implements 1.2: Objects
# -> Exits

# ... and so on for all 90 sections
```

## Implementation Steps

### Step 1: Find Next Rule

1. Read `tests/BDD_TESTS_README.md`
2. Parse the "Rule Coverage Goals" section
3. Find the FIRST unchecked `[ ]` item at the TOP LEVEL (not indented subsections)
4. Extract section number and name

**Example:**
```markdown
### Section 1: Game Concepts
- [ ] 1.0: General           <- FIRST unchecked, select this
  - [x] 1.0.2: Precedence
- [ ] 1.1: Players
- [ ] 1.2: Objects
```

**Result:** Next rule is `1.0 General`

### Step 2: Research the Rule Section

1. **Read the comprehensive rules** for the section:
   - Use `/fab_search "<section_number>" -n 10` to find relevant rules
   - Read directly from `fab-rules/en-fab-cr.md` (markdown format with clear structure)
   - **The markdown file has clickable links**: Rule references like `[1.0.1a](#101a)` are hyperlinked to their sections
   - Alternative: `en-fab-cr.txt` (plain text format, no links)

2. **Identify all sub-rules** within the section (e.g., 1.0.2, 1.0.2a, 1.0.2b)
   - Look for numbered rules (X.Y.Z) and lettered sub-rules (X.Y.Za, X.Y.Zb, etc.)
   - **Follow cross-references**: Click on rule references to understand dependencies
   - Each rule has an HTML anchor: `<a id="102a"></a>` for easy navigation

3. **Extract examples** from the rulebook for each sub-rule
   - Examples are in blockquotes (>) in the markdown file
   - Use these as the basis for test scenarios
   - Examples often reference other rules with clickable links

4. **Understand dependencies**:
   - **Follow the links**: Click referenced rules to understand full context
   - What engine components are needed? (zones, cards, effects, etc.)
   - What existing helper functions can be reused from `tests/bdd_helpers.py`?
   - What new helper functions might be needed?

5. **Check for already-completed subsections**:
   - If the parent section has completed subsections (e.g., `[x] 1.0.2: Precedence`), skip those rules
   - Focus on rules NOT covered by existing subsections

### Step 3: Plan Test Scenarios

For EACH sub-rule identified:
1. Create 1-3 concrete test scenarios
2. Each scenario should test a specific aspect of the rule
3. Use examples from the rulebook when available
4. Think about edge cases and common misunderstandings

**Create a todo list** with all scenarios you plan to implement.

### Step 4: Write the Gherkin Feature File

Create `tests/features/section_<X>_<Y>_<name>.feature` (or `section_<X>_<Y>_<Z>_<name>.feature` for subsections):

**File Structure:**
```gherkin
# Feature file for Section X.Y: [Rule Title]
# Reference: Flesh and Blood Comprehensive Rules Section X.Y
#
# [Copy the full rule text here as a comment]

Feature: Section X.Y - [Rule Title]
    As a game engine
    I need to correctly implement [rule concept]
    So that [game behavior outcome]

    # Test for Rule X.Y.Z - [Specific aspect]
    Scenario: [Descriptive scenario name]
        Given [initial game state setup]
        And [additional context]
        When [action occurs]
        Then [expected outcome]
        And [additional verification]
```

**DO's:**
- Use clear, descriptive scenario names
- Include the full rule text as comments at the top
- Reference specific sub-rule numbers (e.g., Rule 1.0.2a)
- Use concrete examples from the rulebook
- Write scenarios that test ONE specific aspect of the rule
- Use realistic game situations
- Include both positive tests (thing works) and negative tests (thing is prevented)

**DON'Ts:**
- Don't write vague scenarios like "test basic functionality"
- Don't combine multiple rule aspects in one scenario
- Don't use placeholder text like "TBD" or "TODO"
- Don't assume implementation details - focus on behavior
- Don't skip the rule text comments

### Step 5: Write Step Definitions

Create `tests/step_defs/test_section_<X>_<Y>_<name>.py`:

**File Structure:**
```python
"""
Step definitions for Section X.Y: [Rule Title]
Reference: Flesh and Blood Comprehensive Rules Section X.Y

This module implements behavioral tests for [rule concept].
"""

import pytest
from pytest_bdd import scenario, given, when, then, parsers

# Scenario: [First scenario name]
# Tests Rule X.Y.Z: [What it tests]

@scenario(
    "../features/section_X_Y_name.feature",
    "[Scenario name exactly as in feature file]",
)
def test_[descriptive_test_name]():
    """Rule X.Y.Z: [Brief description]."""
    pass


@given('[step text]')
def step_name(game_state):
    """Rule X.Y.Z: [What this step does]."""
    # Implementation using game_state
    pass


# ... more steps ...


# Fixtures

@pytest.fixture
def game_state():
    """
    Fixture providing game state for testing.

    Uses BDDGameState which integrates with the real engine.
    Reference: Rule X.Y
    """
    from tests.bdd_helpers import BDDGameState

    state = BDDGameState()

    # Initialize any test objects needed
    # state.test_card = state.create_card("Test Card")

    return state
```

**DO's:**
- Use REAL engine components via `BDDGameState` and helpers
- Include detailed docstrings with rule references
- Name functions clearly (`test_restriction_overrides_allowance`)
- Use the `game_state` fixture from `bdd_helpers.py`
- Add assertions that verify the rule is followed
- Reuse existing step definitions when possible
- Use `game_state.create_card()` for test cards
- Access real zones via `game_state.player.hand`, `game_state.player.banished_zone`, etc.

**DON'Ts:**
- Don't create mock objects - use REAL engine components
- Don't implement game logic in tests - tests should verify behavior
- Don't duplicate step definitions unnecessarily
- Don't forget to import required types from `fab_engine`
- Don't write steps that depend on execution order across scenarios
- Don't access private methods (starting with `_`) from the engine

### Step 6: Update bdd_helpers.py (if needed)

If the rule requires NEW helper functionality:

1. **Determine what's needed**:
   - New zone types?
   - New game state tracking?
   - New verification methods?

2. **Extend existing classes**:
   - Add methods to `TestPlayer`, `TestAttack`, or `BDDGameState`
   - Use REAL engine components when possible
   - Follow the pattern of existing helpers

3. **Document the additions**:
   ```python
   def new_method(self, param):
       """
       Brief description.

       Implements support for Rule X.Y.Z.
       """
   ```

**DO's:**
- Extend existing classes rather than creating new ones
- Use real `Zone` objects, `CardInstance`, `CardTemplate`, etc.
- Add docstrings with rule references
- Keep helpers generic and reusable

**DON'Ts:**
- Don't add helpers that duplicate existing functionality
- Don't create mock implementations - wrap real engine classes
- Don't add rule-specific logic - keep it generic

### Step 7: Run and Verify Tests

**CRITICAL: DO NOT IMPLEMENT ENGINE CODE DURING THIS STEP**

1. **Run the new tests**:
   ```bash
   uv run pytest tests/step_defs/test_section_X_Y_name.py -v
   ```

2. **Understand Expected vs Unexpected Failures**:

   **EXPECTED FAILURES (Good - Test is Correct)**:
   ```
   AttributeError: 'TestPlayer' has no attribute 'card_pool'
   -> Missing engine feature: Player.card_pool not implemented
   -> ACTION: Document this, mark test complete, move on

   AssertionError: assert False (play was allowed but should be restricted)
   -> Missing engine feature: Restriction system incomplete
   -> ACTION: Document this, mark test complete, move on

   NotImplementedError: Zone.move_card() not implemented
   -> Missing engine feature: Card movement between zones
   -> ACTION: Document this, mark test complete, move on
   ```

   **UNEXPECTED FAILURES (Bad - Test is Broken)**:
   ```
   SyntaxError: invalid syntax in test_section_1_1_players.py
   -> Broken test code
   -> ACTION: Fix the test file syntax

   ImportError: cannot import name 'CardType' from 'fab_engine.cards.model'
   -> Broken test code (wrong import)
   -> ACTION: Fix the import statement

   NameError: name 'game_state' is not defined
   -> Broken test code (missing fixture)
   -> ACTION: Fix the step definition

   TypeError: create_card() takes 2 positional arguments but 3 were given
   -> Broken test code (wrong API usage)
   -> ACTION: Check bdd_helpers.py and fix the call
   ```

3. **Decision Tree**:
   ```
   Test fails
   |
   +- Is it a syntax/import/fixture error?
   |  -> YES: Fix the TEST code, re-run
   |
   +- Is it missing a method/attribute from bdd_helpers.py?
   |  -> YES: Add helper method (if generic), fix TEST code
   |
   +- Is it missing engine functionality?
   |  -> YES: PERFECT! Document and move on
   |
   +- Is it an assertion failure?
      |
      +- Does the test logic match the comprehensive rules?
      |  -> YES: PERFECT! Engine needs work, move on
      |  -> NO:  Fix the TEST to match the rules
      |
      +- Is bdd_helpers.py doing the wrong thing?
         -> YES: Fix the HELPER code (if it's test infrastructure)
   ```

4. **What You Can Fix**:
   - Syntax errors in test files
   - Import errors
   - Missing fixtures
   - Incorrect use of bdd_helpers API
   - Test logic that doesn't match comprehensive rules
   - Missing helper methods in bdd_helpers.py (test infrastructure)

5. **What You CANNOT Fix**:
   - Missing engine features (e.g., `PrecedenceManager.add_restriction()`)
   - Missing zone operations (e.g., `Zone.move_card()`)
   - Missing card properties (e.g., `CardInstance.card_pool`)
   - Missing game state tracking (e.g., `GameState.turn_player`)
   - **Anything in `fab_engine/` directory** (unless it's clearly a bug)

6. **Check test collection**:
   ```bash
   uv run pytest tests/step_defs/test_section_X_Y_name.py --collect-only
   ```
   This verifies pytest can parse and collect your scenarios (should succeed even if tests fail)

7. **Final Check**:
   ```bash
   # All BDD tests should still be collectible
   uv run pytest tests/step_defs/ --collect-only

   # Your new tests should fail for the RIGHT reasons
   uv run pytest tests/step_defs/test_section_X_Y_name.py -v
   ```

**Remember**: Tests are the SPEC. If a test fails because the engine doesn't implement the rule, that's SUCCESS! You've documented what the engine must do.

### Step 8: Update Documentation

1. **Update `tests/BDD_TESTS_README.md`**:
   - Add a new section documenting the test under "Test Organization"
   - Include scenario names and what they test
   - Follow the pattern of Section 1.0.2

2. **Example documentation**:
   ```markdown
   ### Section X.Y: [Rule Title]

   **File**: `features/section_X_Y_name.feature`
   **Step Definitions**: `step_defs/test_section_X_Y_name.py`

   This section tests [rule concept]:
   - **Rule X.Y.Z**: [Main rule]
   - **Rule X.Y.Za**: [Sub-rule a]

   #### Test Scenarios:

   1. **test_scenario_one**
      - Tests: Rule X.Y.Z - [Aspect]
      - Verifies: [What it verifies]
   ```

3. **Document Engine Requirements** in the test file or BDD_TESTS_README.md:
   ```python
   """
   Engine Features Needed for Section X.Y:
   - [ ] Player.card_pool property (stores deck + arena cards)
   - [ ] Player.hero property (reference to hero card)
   - [ ] Supertype validation (check subset of hero's supertypes)

   These features will be implemented in a separate task.
   Current status: Tests written, Engine pending
   """
   ```

### Step 9: Mark Section Complete

Update `tests/BDD_TESTS_README.md`:

**Find the section:**
```markdown
- [ ] 1.0: General
```

**Change to:**
```markdown
- [x] 1.0: General
```

Use the Edit tool to make this change.

**Critical:** Only mark the TOP-LEVEL section, not subsections.

**Example:**
```markdown
### Section 1: Game Concepts
- [x] 1.0: General           <- Mark this complete
  - [x] 1.0.2: Precedence    <- This was already done
- [ ] 1.1: Players           <- Leave unchecked
```

### Step 10: Report and Exit

Provide a clear summary, then EXIT:

```markdown
## Ralph Loop Iteration Complete

### Rule Implemented
- **Section:** X.Y Name
- **Tests Written:** N scenarios
- **Status:** All tests failing as expected (missing engine features)

### Files Created/Modified
- tests/features/section_X_Y_name.feature
- tests/step_defs/test_section_X_Y_name.py

### Verification Results
- Tests collect successfully
- Tests fail for correct reasons (missing engine features)
- Documentation updated
- Checklist marked complete

### Engine Features Needed
- [ ] Feature A (Rule X.Y.Z)
- [ ] Feature B (Rule X.Y.Za)

### Progress
- **Completed:** N / 90 sections
- **Remaining:** M sections

### Next Steps
1. Review the tests: `tests/step_defs/test_section_X_Y_name.py`
2. Verify they match comprehensive rules
3. Run `/ralph-loop` again to implement next rule
```

**Then EXIT.** Do not continue to the next rule.

## Important Notes

### One Rule Per Iteration

**DO:**
- Implement ONE rule section
- Verify it completely
- Mark it complete
- Exit

**DON'T:**
- Implement multiple rules in one iteration
- Skip verification steps
- Continue to next rule automatically
- Mark sections complete without verification

### When to Stop

The ralph loop stops automatically when all sections are `[x]`. When that happens, announce:

```
ALL RULE SECTIONS COMPLETE!

All 90 rule sections have BDD test specifications written.
Total tests: ~500+ scenarios
All tests failing as expected (ready for engine implementation)

Next phase: Implement engine features to make tests pass.
```

### Subsection Handling

Some sections have subsections:

```markdown
- [ ] 1.0: General
  - [x] 1.0.2: Precedence (Restrictions/Requirements/Allowances)
```

**Rules:**
1. If parent section is unchecked `[ ] 1.0: General`, implement the PARENT, not subsections
2. The subsection `1.0.2` is already done, so skip it when implementing `1.0`
3. Focus on rules NOT covered by existing subsections
4. Mark only the PARENT complete when done

### If No Rules Left in a Section

Sometimes all subsections are complete but parent isn't marked:

```markdown
- [ ] 1.0: General
  - [x] 1.0.1: Rule Hierarchy
  - [x] 1.0.2: Precedence
  # (all subsections done)
```

In this case:
1. Check if there are rules in section 1.0 NOT covered by subsections
2. If yes, implement tests for those rules
3. If no, just mark `[x] 1.0: General` complete and move on

### Error Handling

**If test collection fails:**
```bash
ERROR: SyntaxError in test_section_1_0_general.py
```
1. Fix the syntax error in the test file
2. Re-run collection
3. Do NOT mark complete until collection succeeds

**If tests fail with wrong error types:**
```bash
ImportError: cannot import name 'CardTyp'
```
1. This is broken test code (typo)
2. Fix the import
3. Re-run tests
4. Do NOT mark complete until failures are correct type

**If verification step fails:**
1. Report what failed
2. Fix the issue
3. Re-run verification
4. Do NOT proceed until verification passes

### Skip Already-Complete Sections

When finding next rule to implement:

```markdown
- [x] 1.0: General           <- Skip (already done)
- [x] 1.1: Players           <- Skip (already done)
- [ ] 1.2: Objects           <- IMPLEMENT THIS
```

Always find the FIRST unchecked `[ ]` section at the top level.

## When Tests Fail: Decision Flowchart

```
+-------------------------+
|   Test Fails            |
+---------+---------------+
          |
          v
+-------------------------------------------------+
| Is it a SyntaxError, ImportError, or NameError? |
+----+----------------------------------------+---+
     | YES                                    | NO
     v                                        v
+---------------------+         +--------------------------------+
| FIX THE TEST CODE   |         | Is it an AttributeError like:  |
| - Fix syntax        |         | 'Player' has no attribute 'X'? |
| - Fix imports       |         +----+-----------------------+---+
| - Fix fixtures      |              | YES                   | NO
| - Re-run test       |              v                       v
+---------------------+    +----------------------+   +--------------------+
                           | Is X in fab_engine/? |   | Is it an assertion |
                           +----+-------------+---+   | failure like:      |
                                | YES         | NO    | "assert False"?    |
                                v             v       +----+-----------+---+
                     +------------------+ +-----------+    | YES       | NO
                     | MISSING ENGINE   | | ADD HELPER|    v           v
                     | FEATURE          | | - Update  | +----------------------+
                     | EXPECTED!        | |   helpers | | Does test logic      |
                     | - Document it    | | - Re-run  | | match the CR?        |
                     | - Move on        | +-----------+ +----+-------------+---+
                     +------------------+                    | YES         | NO
                                                             v             v
                                                  +------------------+ +-----------+
                                                  | MISSING ENGINE   | | FIX TEST  |
                                                  | FEATURE          | | - Update  |
                                                  | EXPECTED!        | |   logic   |
                                                  | - Document it    | |   to match|
                                                  | - Move on        | |   CR      |
                                                  +------------------+ | - Re-run  |
                                                                       +-----------+

GOLDEN RULE: If the failure is because code in `fab_engine/` doesn't exist or doesn't work,
             that's PERFECT! Document it and move on. DO NOT implement engine features.
```

## Concrete Examples: What to Fix vs What to Document

### Fix This (Broken Test Code)
```python
# Test file has this error:
ImportError: cannot import name 'CardTyp' from 'fab_engine.cards.model'

# DIAGNOSIS: Typo in import
# ACTION: Fix the test code
from fab_engine.cards.model import CardType  # Fixed typo
```

### Fix This (Missing Fixture)
```python
# Test fails with:
NameError: name 'game_state' is not defined

# DIAGNOSIS: Forgot to add fixture parameter
# ACTION: Fix the step definition
@given("a player has a card pool")
def step(game_state):  # Added game_state parameter
    pass
```

### Fix This (Wrong Helper API)
```python
# Test fails with:
TypeError: create_card() takes 2 arguments but 3 were given

# DIAGNOSIS: Check bdd_helpers.py - wrong API usage
# ACTION: Fix the test code to use correct API
card = game_state.create_card(name="Test", color=Color.RED)  # Correct usage
```

### Fix This (Test Logic Wrong)
```python
# Rule 1.0.2: "Restriction takes precedence over allowance"
# Test says: allowance should win
assert play_result.success  # WRONG!

# DIAGNOSIS: Test contradicts comprehensive rules
# ACTION: Fix test to match the rule
assert not play_result.success  # Correct - restriction blocks
```

### DON'T Fix This (Missing Engine Feature)
```python
# Test fails with:
AttributeError: 'TestPlayer' has no attribute 'card_pool'

# DIAGNOSIS: Engine doesn't have Player.card_pool property yet
# ACTION: Document and move on - DO NOT implement Player.card_pool
"""
Engine Feature Needed:
- [ ] Player.card_pool property (Rule 1.1.3)
"""
```

### DON'T Fix This (Assertion Failure - Missing Engine Logic)
```python
# Test fails with:
AssertionError: assert False
# Expected restriction to block play, but play succeeded

# DIAGNOSIS: PrecedenceManager.check_action() not fully implemented
# ACTION: Document and move on - DO NOT implement precedence logic
"""
Engine Feature Needed:
- [ ] PrecedenceManager.check_action() needs to properly evaluate restrictions
"""
```

### DON'T Fix This (NotImplementedError)
```python
# Test fails with:
NotImplementedError: Zone.move_card() not yet implemented

# DIAGNOSIS: Zone doesn't have card movement yet
# ACTION: Document and move on - DO NOT implement Zone.move_card()
"""
Engine Feature Needed:
- [ ] Zone.move_card() method (Rule 3.0 - Zone transitions)
"""
```

## Real Engine Integration

These tests use REAL engine components, not mocks:
- `PrecedenceManager` from `fab_engine/engine/precedence.py`
- `Zone` from `fab_engine/zones/zone.py`
- `CardTemplate` and `CardInstance` from `fab_engine/cards/model.py`
- All enums: `Color`, `CardType`, `Subtype`, `ZoneType`, `EffectType`

See `tests/REAL_VS_MOCK.md` and `tests/ARCHITECTURE_DIAGRAM.md` for details.

## Verification Checklist

Before marking complete and exiting, verify:

- [ ] Feature file exists and has scenarios
- [ ] Step definitions exist and have test functions
- [ ] `pytest --collect-only` succeeds
- [ ] Tests fail with AttributeError, NotImplementedError, or AssertionError
- [ ] Tests do NOT fail with SyntaxError, ImportError, NameError
- [ ] `tests/BDD_TESTS_README.md` is updated with test documentation
- [ ] Section is marked `[x]` in checklist
- [ ] Summary report is provided
- [ ] You are about to EXIT (not continue to next rule)

## Quality Checklist

### Test Coverage
- [ ] All sub-rules in the section have test coverage
- [ ] Feature file has complete rule text as comments
- [ ] Each scenario tests ONE specific aspect
- [ ] Test scenarios use examples from the comprehensive rules

### Test Implementation
- [ ] Step definitions use real engine components (via bdd_helpers)
- [ ] All docstrings include rule references (e.g., "Rule 1.1.2")
- [ ] Fixtures reuse `BDDGameState` pattern
- [ ] No mock objects used (unless absolutely necessary)
- [ ] Test file naming follows convention (section_X_Y_Z_name)

### Test Execution
- [ ] Tests collect successfully (`pytest --collect-only`)
- [ ] No syntax errors, import errors, or fixture errors
- [ ] Tests fail with EXPECTED errors (missing engine features)
- [ ] Tests do NOT fail with UNEXPECTED errors (broken test code)

### Critical Final Check
- [ ] **You did NOT modify any files in `fab_engine/` directory**
- [ ] **Tests are failing for the RIGHT reasons**
- [ ] **You are ready to EXIT (not continue to next rule)**
