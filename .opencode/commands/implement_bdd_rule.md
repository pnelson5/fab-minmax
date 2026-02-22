---
description: Implement a BDD test for a specific Flesh and Blood comprehensive rules section
---

# Implement BDD Rule

You are tasked with implementing a complete BDD (Behavior-Driven Development) test for a specific section of the Flesh and Blood Comprehensive Rules.

## ⚠️ CRITICAL: THIS IS A TEST SPECIFICATION TASK, NOT AN ENGINE IMPLEMENTATION TASK

**DO NOT IMPLEMENT ENGINE FEATURES TO MAKE TESTS PASS**

Your job:
- ✅ Write tests that accurately reflect the comprehensive rules
- ✅ Verify tests are syntactically correct
- ✅ Document what engine features are needed
- ✅ Move on to the next rule

Your job is **NOT**:
- ❌ Implement missing engine features in `fab_engine/`
- ❌ Make tests pass by writing engine code
- ❌ Fix "failures" that are actually missing engine features

**Tests SHOULD fail** because the engine doesn't implement these rules yet. That's the whole point of BDD - write the spec first, implement later.

## Usage

```
/implement-bdd-rule <section_number> [rule_name]
```

### Examples
```
/implement-bdd-rule 1.1 Players
/implement-bdd-rule 2.1 Color
/implement-bdd-rule 7.2 Attack Step
```

If no arguments provided, ask the user which rule section they want to implement.

## Prerequisites

Before starting, ensure you have:
1. Read the Comprehensive Rules section from `en-fab-cr.txt`
2. Understood the existing BDD test structure in `tests/BDD_TESTS_README.md`
3. Reviewed the existing example: `tests/features/section_1_0_2_precedence.feature` and `tests/step_defs/test_section_1_0_2_precedence.py`
4. Understood the real engine integration via `tests/bdd_helpers.py`

## Implementation Steps

### Step 1: Research the Rule Section

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

### Step 2: Plan Test Scenarios

For EACH sub-rule identified:
1. Create 1-3 concrete test scenarios
2. Each scenario should test a specific aspect of the rule
3. Use examples from the rulebook when available
4. Think about edge cases and common misunderstandings

**Create a todo list** with all scenarios you plan to implement.

### Step 3: Write the Gherkin Feature File

Create `tests/features/section_<X>_<Y>_<Z>_<name>.feature`:

**File Structure:**
```gherkin
# Feature file for Section X.Y.Z: [Rule Title]
# Reference: Flesh and Blood Comprehensive Rules Section X.Y.Z
#
# [Copy the full rule text here as a comment]

Feature: Section X.Y.Z - [Rule Title]
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
- ✅ Use clear, descriptive scenario names
- ✅ Include the full rule text as comments at the top
- ✅ Reference specific sub-rule numbers (e.g., Rule 1.0.2a)
- ✅ Use concrete examples from the rulebook
- ✅ Write scenarios that test ONE specific aspect of the rule
- ✅ Use realistic game situations
- ✅ Include both positive tests (thing works) and negative tests (thing is prevented)

**DON'Ts:**
- ❌ Don't write vague scenarios like "test basic functionality"
- ❌ Don't combine multiple rule aspects in one scenario
- ❌ Don't use placeholder text like "TBD" or "TODO"
- ❌ Don't assume implementation details - focus on behavior
- ❌ Don't skip the rule text comments

### Step 4: Write Step Definitions

Create `tests/step_defs/test_section_<X>_<Y>_<Z>_<name>.py`:

**File Structure:**
```python
"""
Step definitions for Section X.Y.Z: [Rule Title]
Reference: Flesh and Blood Comprehensive Rules Section X.Y.Z

This module implements behavioral tests for [rule concept].
"""

import pytest
from pytest_bdd import scenario, given, when, then, parsers

# Scenario: [First scenario name]
# Tests Rule X.Y.Z: [What it tests]

@scenario(
    "../features/section_X_Y_Z_name.feature",
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
    Reference: Rule X.Y.Z
    """
    from tests.bdd_helpers import BDDGameState
    
    state = BDDGameState()
    
    # Initialize any test objects needed
    # state.test_card = state.create_card("Test Card")
    
    return state
```

**DO's:**
- ✅ Use REAL engine components via `BDDGameState` and helpers
- ✅ Include detailed docstrings with rule references
- ✅ Name functions clearly (`test_restriction_overrides_allowance`)
- ✅ Use the `game_state` fixture from `bdd_helpers.py`
- ✅ Add assertions that verify the rule is followed
- ✅ Reuse existing step definitions when possible
- ✅ Use `game_state.create_card()` for test cards
- ✅ Access real zones via `game_state.player.hand`, `game_state.player.banished_zone`, etc.

**DON'Ts:**
- ❌ Don't create mock objects - use REAL engine components
- ❌ Don't implement game logic in tests - tests should verify behavior
- ❌ Don't duplicate step definitions unnecessarily
- ❌ Don't forget to import required types from `fab_engine`
- ❌ Don't write steps that depend on execution order across scenarios
- ❌ Don't access private methods (starting with `_`) from the engine

### Step 5: Update bdd_helpers.py (if needed)

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
- ✅ Extend existing classes rather than creating new ones
- ✅ Use real `Zone` objects, `CardInstance`, `CardTemplate`, etc.
- ✅ Add docstrings with rule references
- ✅ Keep helpers generic and reusable

**DON'Ts:**
- ❌ Don't add helpers that duplicate existing functionality
- ❌ Don't create mock implementations - wrap real engine classes
- ❌ Don't add rule-specific logic - keep it generic

### Step 6: Run and Verify Tests

**CRITICAL: DO NOT IMPLEMENT ENGINE CODE DURING THIS STEP**

This is a **test specification task**, not an engine implementation task. Your job is to write correct tests that define the spec. The engine will be implemented separately.

1. **Run the new tests**:
   ```bash
   uv run pytest tests/step_defs/test_section_X_Y_Z_name.py -v
   ```

2. **Understand Expected vs Unexpected Failures**:

   **✅ EXPECTED FAILURES (Good - Test is Correct)**:
   ```
   AttributeError: 'TestPlayer' has no attribute 'card_pool'
   → Missing engine feature: Player.card_pool not implemented
   → ACTION: Document this, mark test complete, move on
   
   AssertionError: assert False (play was allowed but should be restricted)
   → Missing engine feature: Restriction system incomplete
   → ACTION: Document this, mark test complete, move on
   
   NotImplementedError: Zone.move_card() not implemented
   → Missing engine feature: Card movement between zones
   → ACTION: Document this, mark test complete, move on
   ```

   **❌ UNEXPECTED FAILURES (Bad - Test is Broken)**:
   ```
   SyntaxError: invalid syntax in test_section_1_1_players.py
   → Broken test code
   → ACTION: Fix the test file syntax
   
   ImportError: cannot import name 'CardType' from 'fab_engine.cards.model'
   → Broken test code (wrong import)
   → ACTION: Fix the import statement
   
   NameError: name 'game_state' is not defined
   → Broken test code (missing fixture)
   → ACTION: Fix the step definition
   
   TypeError: create_card() takes 2 positional arguments but 3 were given
   → Broken test code (wrong API usage)
   → ACTION: Check bdd_helpers.py and fix the call
   ```

3. **Decision Tree**:
   ```
   Test fails
   │
   ├─ Is it a syntax/import/fixture error?
   │  └─ YES → Fix the TEST code, re-run
   │
   ├─ Is it missing a method/attribute from bdd_helpers.py?
   │  └─ YES → Add helper method (if generic), fix TEST code
   │
   ├─ Is it missing engine functionality?
   │  └─ YES → ✅ PERFECT! Document and move on
   │
   └─ Is it an assertion failure?
      │
      ├─ Does the test logic match the comprehensive rules?
      │  └─ YES → ✅ PERFECT! Engine needs work, move on
      │  └─ NO  → Fix the TEST to match the rules
      │
      └─ Is bdd_helpers.py doing the wrong thing?
         └─ YES → Fix the HELPER code (if it's test infrastructure)
   ```

4. **What You Can Fix**:
   - ✅ Syntax errors in test files
   - ✅ Import errors
   - ✅ Missing fixtures
   - ✅ Incorrect use of bdd_helpers API
   - ✅ Test logic that doesn't match comprehensive rules
   - ✅ Missing helper methods in bdd_helpers.py (test infrastructure)

5. **What You CANNOT Fix**:
   - ❌ Missing engine features (e.g., `PrecedenceManager.add_restriction()`)
   - ❌ Missing zone operations (e.g., `Zone.move_card()`)
   - ❌ Missing card properties (e.g., `CardInstance.card_pool`)
   - ❌ Missing game state tracking (e.g., `GameState.turn_player`)
   - ❌ **Anything in `fab_engine/` directory** (unless it's clearly a bug)

6. **Document Expected Failures**:
   ```python
   # In your test file or in a comment:
   """
   Expected Failures (Engine Features Needed):
   - [ ] Player.card_pool property (Rule 1.1.3)
   - [ ] Player.hero property (Rule 1.1.2)
   - [ ] Supertype subset validation (Rule 1.1.3)
   """
   ```

7. **Check test collection**:
   ```bash
   uv run pytest tests/step_defs/test_section_X_Y_Z_name.py --collect-only
   ```
   This verifies pytest can parse and collect your scenarios (should succeed even if tests fail)

8. **Verify all scenarios were collected**:
   - Each scenario in the feature file should appear in the collection
   - If scenarios are missing, check feature file syntax

9. **Final Check**:
   ```bash
   # All BDD tests should still be collectible
   uv run pytest tests/step_defs/ --collect-only
   
   # Your new tests should fail for the RIGHT reasons
   uv run pytest tests/step_defs/test_section_X_Y_Z_name.py -v
   ```

**Remember**: Tests are the SPEC. If a test fails because the engine doesn't implement the rule, that's SUCCESS! You've documented what the engine must do.

### Step 7: Update Documentation

1. **Update `tests/BDD_TESTS_README.md`**:
   - Mark the rule section as complete: `- [x] X.Y: Rule Name`
   - Add a new section documenting the test under "Test Organization"
   - Include scenario names and what they test
   - Follow the pattern of Section 1.0.2

2. **Example documentation**:
   ```markdown
   ### Section X.Y.Z: [Rule Title]
   
   **File**: `features/section_X_Y_Z_name.feature`
   **Step Definitions**: `step_defs/test_section_X_Y_Z_name.py`
   
   This section tests [rule concept]:
   - **Rule X.Y.Z**: [Main rule]
   - **Rule X.Y.Za**: [Sub-rule a]
   
   #### Test Scenarios:
   
   1. **test_scenario_one**
      - Tests: Rule X.Y.Z - [Aspect]
      - Verifies: [What it verifies]
   ```

### Step 8: Complete the Task

1. **Mark todo items as complete**

2. **Run final verification**:
   ```bash
   uv run pytest tests/step_defs/test_section_X_Y_Z_name.py -vv
   ```
   
3. **Verify Expected Failures**:
   - ✅ Tests should be failing (unless engine already implements this rule)
   - ✅ Failures should be due to missing engine features
   - ✅ No syntax errors, import errors, or broken test code

4. **Document Engine Requirements**:
   Create a comment block in the test file or in BDD_TESTS_README.md:
   ```python
   """
   Engine Features Needed for Section X.Y:
   - [ ] Player.card_pool property (stores deck + arena cards)
   - [ ] Player.hero property (reference to hero card)
   - [ ] Supertype validation (check subset of hero's supertypes)
   - [ ] CardPool class (collection of deck-cards and arena-cards)
   
   These features will be implemented in a separate task.
   Current status: Tests written ✅, Engine pending ⏳
   """
   ```

5. **Summarize what was implemented**:
   ```markdown
   ## Completed: Section X.Y - [Rule Name]
   
   ### Test Scenarios Written
   - [x] test_scenario_one - Tests Rule X.Y.Z aspect A
   - [x] test_scenario_two - Tests Rule X.Y.Za aspect B
   - [x] test_scenario_three - Tests Rule X.Y.Zb aspect C
   
   ### Files Created
   - tests/features/section_X_Y_name.feature (N scenarios)
   - tests/step_defs/test_section_X_Y_name.py (M step definitions)
   
   ### Helpers Added (if any)
   - tests/bdd_helpers.py: Added TestPlayer.method_name()
   
   ### Test Status
   - All tests fail as expected (missing engine features)
   - No broken test code
   - Ready for engine implementation
   
   ### Engine Features Needed
   1. Feature A (Rule X.Y.Z)
   2. Feature B (Rule X.Y.Za)
   3. Feature C (Rule X.Y.Zb)
   
   ### Next Steps
   - Mark [x] X.Y in tests/BDD_TESTS_README.md
   - Move to next rule section
   - Engine implementation will happen separately
   ```

6. **Important Reminder**:
   
   **YOU ARE DONE** when tests are written and failing for the right reasons.
   
   ❌ DO NOT say "Now let me implement the engine features..."
   ❌ DO NOT modify files in `fab_engine/` directory
   ❌ DO NOT try to make tests pass
   
   ✅ DO mark the test section as complete
   ✅ DO move on to the next rule
   ✅ DO let the user know tests are ready for engine work (later)

## When Tests Fail: Decision Flowchart

```
┌─────────────────────────┐
│   Test Fails            │
└───────┬─────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────┐
│ Is it a SyntaxError, ImportError, or NameError? │
└────┬────────────────────────────────────────┬───┘
     │ YES                                    │ NO
     ▼                                        ▼
┌─────────────────────┐         ┌────────────────────────────────┐
│ FIX THE TEST CODE   │         │ Is it an AttributeError like:  │
│ - Fix syntax        │         │ 'Player' has no attribute 'X'? │
│ - Fix imports       │         └────┬───────────────────────┬───┘
│ - Fix fixtures      │              │ YES                   │ NO
│ - Re-run test       │              ▼                       ▼
└─────────────────────┘    ┌──────────────────────┐   ┌────────────────────┐
                           │ Is X in fab_engine/? │   │ Is it an assertion │
                           └────┬─────────────┬───┘   │ failure like:      │
                                │ YES         │ NO    │ "assert False"?    │
                                ▼             ▼       └────┬───────────┬───┘
                     ┌──────────────────┐ ┌─────────────┐ │ YES       │ NO
                     │ MISSING ENGINE   │ │ ADD HELPER  │ ▼           ▼
                     │ FEATURE          │ │ - Update    │ ┌──────────────────────┐
                     │ ✅ EXPECTED!     │ │   helpers   │ │ Does test logic      │
                     │ - Document it    │ │ - Re-run    │ │ match the CR?        │
                     │ - Move on        │ └─────────────┘ └────┬─────────────┬───┘
                     └──────────────────┘                      │ YES         │ NO
                                                               ▼             ▼
                                                    ┌──────────────────┐ ┌─────────────┐
                                                    │ MISSING ENGINE   │ │ FIX TEST    │
                                                    │ FEATURE          │ │ - Update    │
                                                    │ ✅ EXPECTED!     │ │   logic to  │
                                                    │ - Document it    │ │   match CR  │
                                                    │ - Move on        │ │ - Re-run    │
                                                    └──────────────────┘ └─────────────┘

GOLDEN RULE: If the failure is because code in `fab_engine/` doesn't exist or doesn't work,
             that's PERFECT! Document it and move on. DO NOT implement engine features.
```

## Important Notes

### Test-First Philosophy ⚠️ READ THIS CAREFULLY

These are **BDD SPECIFICATION tests** - they define what the engine MUST do, not what it currently does:

**Your Job**: Write tests that accurately reflect the comprehensive rules
**NOT Your Job**: Make tests pass by implementing engine features

#### Tests Should Fail (And That's Good!)

- ✅ **EXPECTED**: Tests fail because engine features don't exist yet
- ✅ **CORRECT**: `AttributeError: 'TestPlayer' has no attribute 'card_pool'`
- ✅ **CORRECT**: `AssertionError: Expected restriction to block play`
- ✅ **SUCCESS**: Tests fail for the RIGHT reasons = job well done!

#### When Tests Fail

```python
# GOOD FAILURE (Engine missing features):
def test_player_has_card_pool():
    assert player.card_pool is not None  # ← Fails: no card_pool
# → Document this, move on. Engine will be implemented later.

# BAD FAILURE (Test is broken):
def test_player_has_card_pool()  # ← Missing colon, syntax error
# → Fix the test code, re-run.
```

#### The Two Types of Failures

| Type | Example | What To Do |
|------|---------|------------|
| **Expected** | `AttributeError: 'Player' has no attribute 'card_pool'` | ✅ Document, move on |
| **Expected** | `AssertionError: assert False (restriction didn't block)` | ✅ Document, move on |
| **Expected** | `NotImplementedError: Zone.move_card() not implemented` | ✅ Document, move on |
| **Unexpected** | `SyntaxError: invalid syntax` | ❌ Fix test code |
| **Unexpected** | `ImportError: cannot import CardType` | ❌ Fix test code |
| **Unexpected** | `NameError: 'game_state' is not defined` | ❌ Fix test code |

#### What This Means

1. **Write the test** based on comprehensive rules
2. **Run the test** to verify it's syntactically correct
3. **Test fails** because engine features don't exist? **PERFECT!** ✅
4. **Document** what engine features are needed
5. **Move on** to the next rule
6. **Later** (separate task): Implement engine features to make tests pass

#### Critical Rule

**DO NOT implement code in `fab_engine/` to make tests pass during this task.**

Engine implementation is a separate task that happens AFTER you've written multiple test specs.

### Real Engine Integration

These tests use REAL engine components, not mocks:
- `PrecedenceManager` from `fab_engine/engine/precedence.py`
- `Zone` from `fab_engine/zones/zone.py`
- `CardTemplate` and `CardInstance` from `fab_engine/cards/model.py`
- All enums: `Color`, `CardType`, `Subtype`, `ZoneType`, `EffectType`

See `tests/REAL_VS_MOCK.md` and `tests/ARCHITECTURE_DIAGRAM.md` for details.

### Rule References

Every test should clearly reference:
- The section number (e.g., Rule 1.0.2)
- Sub-rule letters (e.g., Rule 1.0.2a)
- Related rules when applicable

### File Naming Convention

- **Feature files**: `section_X_Y_Z_description.feature`
- **Step files**: `test_section_X_Y_Z_description.py`
- **Test functions**: `test_<descriptive_name>()`
- Use underscores for multi-word names: `section_1_0_2_precedence`

## Concrete Examples: What to Fix vs What to Document

### ✅ Example 1: Fix This (Broken Test Code)
```python
# Test file has this error:
ImportError: cannot import name 'CardTyp' from 'fab_engine.cards.model'

# DIAGNOSIS: Typo in import
# ACTION: Fix the test code
from fab_engine.cards.model import CardType  # Fixed typo
```

### ✅ Example 2: Fix This (Missing Fixture)
```python
# Test fails with:
NameError: name 'game_state' is not defined

# DIAGNOSIS: Forgot to add fixture parameter
# ACTION: Fix the step definition
@given("a player has a card pool")
def step(game_state):  # Added game_state parameter
    pass
```

### ✅ Example 3: Fix This (Wrong Helper API)
```python
# Test fails with:
TypeError: create_card() takes 2 arguments but 3 were given

# DIAGNOSIS: Check bdd_helpers.py - wrong API usage
# ACTION: Fix the test code to use correct API
card = game_state.create_card(name="Test", color=Color.RED)  # Correct usage
```

### ✅ Example 4: Fix This (Test Logic Wrong)
```python
# Rule 1.0.2: "Restriction takes precedence over allowance"
# Test says: allowance should win
assert play_result.success  # WRONG!

# DIAGNOSIS: Test contradicts comprehensive rules
# ACTION: Fix test to match the rule
assert not play_result.success  # Correct - restriction blocks
```

### ❌ Example 5: DON'T Fix This (Missing Engine Feature)
```python
# Test fails with:
AttributeError: 'TestPlayer' has no attribute 'card_pool'

# DIAGNOSIS: Engine doesn't have Player.card_pool property yet
# ACTION: Document and move on - DO NOT implement Player.card_pool
"""
Engine Feature Needed:
- [ ] Player.card_pool property (Rule 1.1.3)
  - Should return collection of deck-cards and arena-cards
  - Implementation: See fab_engine/engine/game.py PlayerState class
"""
```

### ❌ Example 6: DON'T Fix This (Assertion Failure - Missing Engine Logic)
```python
# Test fails with:
AssertionError: assert False
# Expected restriction to block play, but play succeeded

# DIAGNOSIS: PrecedenceManager.check_action() not fully implemented
# ACTION: Document and move on - DO NOT implement precedence logic
"""
Engine Feature Needed:
- [ ] PrecedenceManager.check_action() needs to properly evaluate restrictions
  - Currently returns permitted=True even when restrictions exist
  - Implementation: See fab_engine/engine/precedence.py
"""
```

### ❌ Example 7: DON'T Fix This (NotImplementedError)
```python
# Test fails with:
NotImplementedError: Zone.move_card() not yet implemented

# DIAGNOSIS: Zone doesn't have card movement yet
# ACTION: Document and move on - DO NOT implement Zone.move_card()
"""
Engine Feature Needed:
- [ ] Zone.move_card() method (Rule 3.0 - Zone transitions)
  - Should move card from one zone to another
  - Should trigger zone change events
  - Implementation: See fab_engine/zones/zone.py
"""
```

## Quality Checklist

Before marking complete, verify:

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

### Expected Failure Verification
- [ ] Failures are AttributeError, NotImplementedError, or AssertionError
- [ ] Failures point to missing code in `fab_engine/`, not test code
- [ ] You have NOT implemented engine features to make tests pass
- [ ] Engine requirements are documented

### Documentation
- [ ] BDD_TESTS_README.md is updated with test scenarios
- [ ] Section is marked [x] in the checklist
- [ ] Engine features needed are documented
- [ ] Test status is clear (written ✅, engine pending ⏳)

### Critical Final Check
- [ ] **You did NOT modify any files in `fab_engine/` directory**
- [ ] **Tests are failing for the RIGHT reasons**
- [ ] **You are ready to move on to the next rule**

## Example Workflow

```
User: /implement-bdd-rule 2.1 Color