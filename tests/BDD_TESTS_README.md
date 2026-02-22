# Behavioral Tests for Flesh and Blood Comprehensive Rules

## Overview

This directory contains behavioral acceptance tests written using pytest-bdd that validate the game engine's implementation against the official Flesh and Blood Comprehensive Rules.

## Structure

```
tests/
├── features/                    # Gherkin feature files
│   └── section_1_0_2_precedence.feature
├── step_defs/                   # Step definitions (test implementation)
│   ├── conftest.py
│   └── test_section_1_0_2_precedence.py
└── BDD_TESTS_README.md         # This file
```

## Test Organization

Each test is mapped to a specific rule from the Comprehensive Rules document:

### Section 1.0.2: Restriction, Requirement, and Allowance Precedence

**File**: `features/section_1_0_2_precedence.feature`
**Step Definitions**: `step_defs/test_section_1_0_2_precedence.py`

This section tests the fundamental precedence system:
- **Rule 1.0.2**: Restrictions > Requirements > Allowances
- **Rule 1.0.2a**: "Only" restrictions are equivalent to restricting everything else
- **Rule 1.0.2b**: Restrictions do not retroactively change game state

#### Test Scenarios:

1. **test_restriction_overrides_allowance_banished**
   - Tests: Rule 1.0.2 - Restriction takes precedence over Allowance
   - Verifies: A restriction preventing play from banished zone overrides an allowance that permits it

2. **test_restriction_overrides_requirement_equipment**
   - Tests: Rule 1.0.2 - Restriction takes precedence over Requirement
   - Verifies: Attack restriction "can't be defended by equipment" overrides requirement to defend with equipment

3. **test_requirement_overrides_allowance_card_play**
   - Tests: Rule 1.0.2 - Requirement takes precedence over Allowance
   - Verifies: Requirement to play from hand overrides allowance to play from arsenal

4. **test_only_restriction_equivalent**
   - Tests: Rule 1.0.2a - "Only" restriction functionality
   - Verifies: "May only play from arsenal" prevents playing from all other zones

5. **test_restriction_not_retroactive**
   - Tests: Rule 1.0.2b - Non-retroactive restrictions
   - Verifies: Overpower gained after defenders declared doesn't remove existing defenders

6. **test_multiple_restrictions**
   - Tests: Rule 1.0.2 - Multiple simultaneous restrictions
   - Verifies: All restrictions apply concurrently (can't play red, can't play cost 3+)

7. **test_allowance_permits_when_no_conflicts**
   - Tests: Rule 1.0.2 - Allowance alone permits action
   - Verifies: Allowance permits action when no higher precedence effects exist

## Running Tests

### Run all BDD tests:
```bash
uv run pytest tests/step_defs/ -v
```

### Run specific section tests:
```bash
uv run pytest tests/step_defs/test_section_1_0_2_precedence.py -v
```

### Collect tests without running:
```bash
uv run pytest tests/step_defs/ --collect-only
```

### Run with detailed output:
```bash
uv run pytest tests/step_defs/ -vv -s
```

## Current Status

These tests are currently **FAILING** by design. They define the expected behavior that the game engine must implement. As engine features are developed to support the Comprehensive Rules, these tests will begin to pass.

## Development Workflow

1. **Write tests first**: Create feature files and step definitions for new rules
2. **Implement engine features**: Build the game engine to satisfy the tests
3. **Verify compliance**: Run tests to ensure rules are correctly implemented
4. **Refactor**: Improve implementation while keeping tests passing

## Adding New Tests

To add tests for a new rule section:

1. **Create a feature file**: `tests/features/section_X_Y_Z.feature`
   - Write scenarios in Gherkin syntax
   - Reference the specific rule number in comments
   - Include concrete examples from the rulebook

2. **Create step definitions**: `tests/step_defs/test_section_X_Y_Z.py`
   - Import pytest-bdd decorators
   - Implement @given, @when, @then steps
   - Add comprehensive docstrings referencing rule numbers
   - Use mock game state until engine is implemented

3. **Document the mapping**:
   - Add the test to this README
   - Include rule references in test docstrings
   - Link test scenarios to specific rule numbers

## Test Naming Convention

- **Feature files**: `section_X_Y_Z_description.feature` (matches CR section number)
- **Step definition files**: `test_section_X_Y_Z_description.py`
- **Test functions**: `test_<descriptive_name>` (describes what is being tested)
- **Step functions**: Clear, readable names matching Gherkin steps

## Rule Coverage Goals

The ultimate goal is to have **complete test coverage** of the Flesh and Blood Comprehensive Rules:

- [ ] Section 1: Game Concepts
  - [x] 1.0.2: Precedence (Restrictions/Requirements/Allowances)
  - [ ] 1.1: Players
  - [ ] 1.2: Objects
  - [ ] 1.3: Cards
  - [ ] 1.4: Attacks
  - [ ] 1.5: Macros
  - [ ] 1.6: Layers
  - [ ] 1.7: Abilities
  - [ ] 1.8: Effects
  - [ ] 1.9: Events
- [ ] Section 2: Card Properties
- [ ] Section 3: Zones
- [ ] Section 4: Game Setup
- [ ] Section 5: Abilities and Effects
- [ ] Section 6: Priority and the Stack
- [ ] Section 7: Combat
- [ ] Section 8: Keywords and Ability Words
- [ ] Section 9: Turn Structure
- [ ] Section 10: Additional Rules

## Real Engine Integration ⭐

**These tests exercise REAL game engine code, not mocks!**

### What's Real:

- ✅ **`PrecedenceManager`** - Complete precedence system from `fab_engine/engine/precedence.py`
- ✅ **`Zone`** - Actual zone implementation from `fab_engine/zones/zone.py`
- ✅ **`CardTemplate` & `CardInstance`** - Real card models from `fab_engine/cards/model.py`
- ✅ All enums: `Color`, `CardType`, `Subtype`, `ZoneType`, `EffectType`

### How It Works:

```python
# When a test runs...
@given('a player has a restriction "cant_play_from_banished"')
def step(game_state):
    game_state.player.add_restriction("cant_play_from_banished")
    # ↓ This calls...
    # PrecedenceManager.add_restriction()  ← REAL ENGINE CODE!

@when('player attempts to play from banished zone')  
def step(game_state):
    result = game_state.player.attempt_play_from_zone(card, "banished")
    # ↓ This calls...
    # PrecedenceManager.check_action()  ← REAL ENGINE CODE!
    # ↓ Which evaluates...
    # Real precedence rules (Restrictions > Requirements > Allowances)

@then('play should be prevented')
def step(game_state):
    assert not result.permitted  # ← Validating REAL engine behavior!
```

See `tests/REAL_VS_MOCK.md` and `tests/ARCHITECTURE_DIAGRAM.md` for detailed explanations.

## Benefits of This Approach

1. **Traceability**: Each test maps directly to a specific rule
2. **Documentation**: Tests serve as executable documentation of rules
3. **Regression Prevention**: Ensures rule compliance is maintained during refactoring
4. **Clarity**: Gherkin syntax makes tests readable by non-programmers
5. **Completeness**: Systematic coverage of all rules in the comprehensive ruleset
6. **Real Validation**: Tests prove the actual engine implements rules correctly (not mocks!)
7. **Bug Detection**: If engine code breaks, tests fail immediately
8. **Refactoring Safety**: Can change implementation while tests ensure behavior stays correct
