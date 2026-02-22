# Behavioral Tests for Flesh and Blood Comprehensive Rules

## Overview

This directory contains behavioral acceptance tests written using pytest-bdd that validate the game engine's implementation against the official Flesh and Blood Comprehensive Rules.

## Structure

```
tests/
├── features/                    # Gherkin feature files
│   ├── section_1_0_general.feature
│   ├── section_1_0_2_precedence.feature
│   └── section_1_3_1a_card_ownership.feature
├── step_defs/                   # Step definitions (test implementation)
│   ├── conftest.py
│   ├── test_section_1_0_general.py
│   ├── test_section_1_0_2_precedence.py
│   └── test_section_1_3_1a_ownership.py
├── bdd_helpers.py               # Shared test helpers (BDDGameState, TestZone, etc.)
└── BDD_TESTS_README.md          # This file
```

## Test Organization

Each test is mapped to a specific rule from the Comprehensive Rules document:

### Section 1.0: General (Rule Hierarchy)

**File**: `features/section_1_0_general.feature`
**Step Definitions**: `step_defs/test_section_1_0_general.py`

This section tests the three-tier rule hierarchy in Flesh and Blood:
- **Rule 1.0.1**: Comprehensive rules apply to any game of Flesh and Blood
- **Rule 1.0.1a**: Card effects supersede comprehensive rules when they directly contradict
- **Rule 1.0.1b**: Tournament rules supersede both comprehensive rules and card effects

NOTE: Rule 1.0.2 (Restrictions/Requirements/Allowances) is covered separately below.

#### Test Scenarios:

1. **test_comprehensive_rules_apply_to_all_games**
   - Tests: Rule 1.0.1 - Rules apply to all games
   - Verifies: The game engine has a rule hierarchy governing all gameplay

2. **test_comprehensive_rules_define_default_behavior**
   - Tests: Rule 1.0.1 - Rules define default legality
   - Verifies: When no effects are active, comprehensive rules determine action legality

3. **test_effect_supersedes_rule**
   - Tests: Rule 1.0.1a - Card effect overrides a comprehensive rule
   - Verifies: An allowance effect permits an action normally prohibited by the rules

4. **test_card_effect_overrides_default_rule_restriction**
   - Tests: Rule 1.0.1a - Specific card effect overrides a default rule restriction
   - Verifies: "You may play this from your graveyard" effect overrides the default prohibition

5. **test_full_hierarchy_tournament_beats_effect_beats_rule**
   - Tests: Rule 1.0.1a + 1.0.1b - Full hierarchy: tournament > effect > rule
   - Verifies: Tournament rule overrides both card effect and comprehensive rule

6. **test_tournament_rule_supersedes_comprehensive_rule**
   - Tests: Rule 1.0.1b - Tournament rule overrides comprehensive rule
   - Verifies: A tournament prohibition blocks an action the comprehensive rules permit

7. **test_tournament_rule_supersedes_card_effect**
   - Tests: Rule 1.0.1b - Tournament rule overrides card effects
   - Verifies: Tournament prohibition blocks an action that a card effect permits

8. **test_rule_hierarchy_priority_ordering**
   - Tests: Rule 1.0.1/1.0.1a/1.0.1b - The complete three-tier hierarchy
   - Verifies: tournament_rules > card_effects > comprehensive_rules priority order

#### Engine Features Needed:
- `GameEngine.has_rule_hierarchy()` method
- `GameEngine.evaluate_action(action, player_id)` with `ActionEvaluationResult`
- `GameEngine.apply_card_effect(action, effect_type, source)`
- `GameEngine.apply_tournament_rule(action, effect_type, source)`
- `GameEngine.check_base_rule(action)` returning bool
- `GameEngine.evaluate_default_action(action)` with `governed_by` attribute
- `GameEngine.evaluate_card_play(card, from_zone, player_id)`
- `GameEngine.register_card_effect(card, action, effect_type)`
- `GameEngine.get_rule_hierarchy()` returning `RuleHierarchy`
- `RuleHierarchy` class with `highest_priority`, `second_priority`, `base_priority`
- `ActionEvaluationResult` with `permitted`, `governed_by`, `superseded_by` attributes

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

### Section 1.1: Players

**File**: `features/section_1_1_players.feature`
**Step Definitions**: `step_defs/test_section_1_1_players.py`

This section tests the player participation rules:
- **Rule 1.1.1**: A player is a person participating in the game
- **Rule 1.1.1a**: Participation requirements (hero, card-pool, zones, life total)
- **Rule 1.1.2**: A player's hero is a hero-card
- **Rule 1.1.2a/b**: Player vs hero distinction; "you" refers to hero, "opponent" to opponent's hero
- **Rule 1.1.3**: Card-pool supertype subset validation
- **Rule 1.1.3a**: Effect-based exception to supertype validation
- **Rule 1.1.3b**: Hybrid card inclusion via either supertype set
- **Rule 1.1.4**: Party concept (players who win together)
- **Rule 1.1.4a**: A player is always in a party with themselves
- **Rule 1.1.5**: Opponents are players not in the same party
- **Rule 1.1.6**: Clockwise order

#### Test Scenarios:

1. **test_player_must_have_hero_to_participate**
   - Tests: Rule 1.1.1/1.1.1a - Players without a hero cannot participate
   - Verifies: A player without a hero is not eligible to participate

2. **test_player_requires_all_components**
   - Tests: Rule 1.1.1a - All participation requirements
   - Verifies: A player with hero, card-pool, zones, and life tracker is eligible

3. **test_player_hero_is_hero_card**
   - Tests: Rule 1.1.2 - Player's hero must be a hero-card type
   - Verifies: The hero has CardType.HERO and `is_hero` property

4. **test_you_refers_to_player_hero**
   - Tests: Rule 1.1.2b - "you" and "opponent" refer to heroes
   - Verifies: resolve_you_reference() and resolve_opponent_reference() return hero cards

5. **test_card_with_matching_supertypes_in_card_pool**
   - Tests: Rule 1.1.3 - Card supertypes must be a subset of hero's supertypes
   - Verifies: A Warrior/Light card is valid for a Warrior/Light hero

6. **test_generic_card_in_any_card_pool**
   - Tests: Rule 1.1.3 - Generic cards (no supertypes) always valid
   - Verifies: Empty supertype set is a subset of any set

7. **test_non_matching_supertypes_rejected**
   - Tests: Rule 1.1.3 - Non-matching supertypes are rejected
   - Verifies: A Wizard card is invalid for a Warrior-only hero

8. **test_partial_supertype_match_is_eligible**
   - Tests: Rule 1.1.3 - Subset means all card supertypes are in hero's supertypes
   - Verifies: A Warrior-only card is valid for a Warrior/Light hero

9. **test_effect_allows_non_matching_supertypes**
   - Tests: Rule 1.1.3a - Effects can grant supertype exceptions
   - Verifies: An effect can allow a normally-ineligible card in the card-pool

10. **test_hybrid_card_either_supertype_set**
    - Tests: Rule 1.1.3b - Hybrid card eligible if EITHER supertype set matches
    - Verifies: Hybrid card with Warrior/Wizard sets is valid for a Warrior hero

11. **test_player_in_party_with_themselves**
    - Tests: Rule 1.1.4a - A player is always in a party with themselves
    - Verifies: is_in_party_with(self) returns True

12. **test_two_players_not_in_same_party**
    - Tests: Rule 1.1.4a - Each player is in their own party in 1v1
    - Verifies: Player 0 and Player 1 are NOT in the same party

13. **test_opponents_are_not_in_same_party**
    - Tests: Rule 1.1.5 - Opponents are players not in the same party
    - Verifies: is_opponent_of() is symmetric between the two players

14. **test_clockwise_order**
    - Tests: Rule 1.1.6 - Clockwise order in a 3-player game
    - Verifies: Next player clockwise wraps correctly (0→1→2→0)

#### Engine Features Needed:
- `TestPlayer.is_eligible_to_participate()` (Rule 1.1.1a)
- `TestPlayer.hero` property with hero card assignment (Rule 1.1.2)
- `TestPlayer.resolve_you_reference()` (Rule 1.1.2b)
- `TestPlayer.resolve_opponent_reference(opponent)` (Rule 1.1.2b)
- `BDDGameState.validate_card_in_card_pool(card, hero, effect_exceptions, is_hybrid, hybrid_supertype_sets)` (Rule 1.1.3/3a/3b)
- `TestPlayer.is_in_party_with(other)` (Rule 1.1.4/1.1.4a)
- `TestPlayer.get_party()` (Rule 1.1.4)
- `TestPlayer.is_opponent_of(other)` (Rule 1.1.5)
- `BDDGameState.get_clockwise_order(starting_player_id, num_players)` (Rule 1.1.6)
- `BDDGameState.get_next_clockwise_player(current_player_id, num_players)` (Rule 1.1.6)
- `Supertype.LIGHT` enum value (Rule 1.1.3 - Light supertypes exist in the game)
- HybridCard support with dual supertype sets in CardTemplate (Rule 1.1.3b)

### Section 1.3.1a: Card Ownership

**File**: `features/section_1_3_1a_card_ownership.feature`
**Step Definitions**: `step_defs/test_section_1_3_1a_ownership.py`

This section tests card ownership rules:
- **Rule 1.3.1a**: The owner of a card is the player who started the game with that card as their hero or as part of their card-pool, or the player instructed to create it or otherwise put it into the game.

#### Test Scenarios:

1. **test_starting_deck_ownership**
   - Tests: Rule 1.3.1a - Ownership established at game start
   - Verifies: Cards in starting deck are owned by the player who started with them

2. **test_hero_card_ownership**
   - Tests: Rule 1.3.1a - Hero ownership
   - Verifies: Hero card is owned by the player who started with it

3. **test_token_ownership**
   - Tests: Rule 1.3.1a - Token ownership
   - Verifies: Token created by a player is owned by that player

4. **test_ownership_persists_across_zones**
   - Tests: Rule 1.3.1a - Ownership persistence
   - Verifies: Card ownership persists when card moves between zones

5. **test_ownership_vs_control**
   - Tests: Rule 1.3.1a/b - Ownership vs control
   - Verifies: Card ownership is independent of who controls it

6. **test_card_pool_ownership**
   - Tests: Rule 1.3.1a - Card-pool ownership
   - Verifies: Cards included in a player's card-pool are owned by that player

7. **test_ownership_doesnt_transfer**
   - Tests: Rule 1.3.1a - Ownership doesn't transfer
   - Verifies: Cards stolen or copied remain owned by original owner

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
- [x] 1.0: General
  - [x] 1.0.1: Rule Hierarchy (rules vs effects vs tournament rules)
  - [x] 1.0.2: Precedence (Restrictions/Requirements/Allowances)
- [x] 1.1: Players
- [ ] 1.2: Objects
- [ ] 1.3: Cards
  - [x] 1.3.1a: Card Ownership
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
