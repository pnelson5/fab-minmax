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

### Section 1: Game Concepts
- [ ] 1.0: General
  - [ ] 1.0.1: Rule Hierarchy (rules vs effects vs tournament rules)
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
- [ ] 1.10: Game State
- [ ] 1.11: Priority
- [ ] 1.12: Numbers and Symbols
- [ ] 1.13: Assets
- [ ] 1.14: Costs
- [ ] 1.15: Counters

### Section 2: Object Properties
- [ ] 2.0: General
- [ ] 2.1: Color
- [ ] 2.2: Cost
- [ ] 2.3: Defense
- [ ] 2.4: Intellect
- [ ] 2.5: Life
- [ ] 2.6: Metatype
- [ ] 2.7: Name
- [ ] 2.8: Pitch
- [ ] 2.9: Power
- [ ] 2.10: Subtypes
- [ ] 2.11: Supertypes
- [ ] 2.12: Text Box
- [ ] 2.13: Traits
- [ ] 2.14: Type Box
- [ ] 2.15: Types

### Section 3: Zones
- [ ] 3.0: General
- [ ] 3.1: Arena
- [ ] 3.2: Arms
- [ ] 3.3: Arsenal
- [ ] 3.4: Banished
- [ ] 3.5: Chest
- [ ] 3.6: Combat Chain
- [ ] 3.7: Deck
- [ ] 3.8: Graveyard
- [ ] 3.9: Hand
- [ ] 3.10: Head
- [ ] 3.11: Hero
- [ ] 3.12: Legs
- [ ] 3.13: Permanent
- [ ] 3.14: Pitch
- [ ] 3.15: Stack
- [ ] 3.16: Weapon

### Section 4: Game Structure
- [ ] 4.0: General
- [ ] 4.1: Starting a Game
- [ ] 4.2: Start Phase
- [ ] 4.3: Action Phase
- [ ] 4.4: End Phase
- [ ] 4.5: Ending a Game

### Section 5: Layers, Cards, & Abilities
- [ ] 5.0: General
- [ ] 5.1: Playing Cards
- [ ] 5.2: Activated Abilities
- [ ] 5.3: Resolution Abilities & Resolving Layers
- [ ] 5.4: Static Abilities

### Section 6: Effects
- [ ] 6.0: General
- [ ] 6.1: Discrete Effects
- [ ] 6.2: Continuous Effects
- [ ] 6.3: Continuous Effect Interactions
- [ ] 6.4: Replacement Effects
- [ ] 6.5: Replacement Effect Interactions
- [ ] 6.6: Triggered Effects

### Section 7: Combat
- [ ] 7.0: General
- [ ] 7.1: Layer Step
- [ ] 7.2: Attack Step
- [ ] 7.3: Defend Step
- [ ] 7.4: Reaction Step
- [ ] 7.5: Damage Step
- [ ] 7.6: Resolution Step
- [ ] 7.7: Close Step

### Section 8: Keywords
- [ ] 8.0: General
- [ ] 8.1: Type Keywords
- [ ] 8.2: Subtype Keywords
- [ ] 8.3: Ability Keywords
- [ ] 8.4: Label Keywords
- [ ] 8.5: Effect Keywords
- [ ] 8.6: Token Keywords

### Section 9: Additional Rules
- [ ] 9.0: General
- [ ] 9.1: Double-Faced Cards
- [ ] 9.2: Split-Cards
- [ ] 9.3: Marked

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
