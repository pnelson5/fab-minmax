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

### Section 1.2: Objects

**File**: `features/section_1_2_objects.feature`
**Step Definitions**: `step_defs/test_section_1_2_objects.py`

This section tests object concepts in Flesh and Blood:
- **Rule 1.2.1**: An object is an element of the game with properties in a zone or player inventory
- **Rule 1.2.1a**: Owner of an object = owner of the card/macro/layer representing it
- **Rule 1.2.1b**: Controller of an object; no controller outside arena/stack
- **Rule 1.2.2**: Objects have one or more object identities
- **Rule 1.2.2a**: All objects have the identity "object"
- **Rule 1.2.2b**: Named objects have their name as an identity
- **Rule 1.2.2c**: Card's traits, types, subtypes are identities (except subtype "attack")
- **Rule 1.2.2d**: Attack-card/proxy/layer has the identity "attack"
- **Rule 1.2.2e**: All cards have the identity "card"
- **Rule 1.2.2f**: Permanents have the identity "permanent"
- **Rule 1.2.2g/h**: Activated/triggered layers have their respective identities
- **Rule 1.2.3**: Last known information = snapshot before object ceases to exist
- **Rule 1.2.3a**: LKI used when specific object no longer exists (Endless Arrow example)
- **Rule 1.2.3b**: LKI includes all parameters, history, and effects at snapshot time
- **Rule 1.2.3c**: LKI is immutable (Luminaris example)
- **Rule 1.2.3d**: LKI is not a legal target for rules/effects
- **Rule 1.2.4**: Cards and macros are sources of abilities, effects, attack-proxies

#### Test Scenarios:

1. **test_card_in_zone_is_object**
   - Tests: Rule 1.2.1 - Cards in zones are game objects
   - Verifies: CardInstance has `is_game_object` property

2. **test_different_game_elements_are_objects**
   - Tests: Rule 1.2.1 - Cards, attacks, macros, and layers are objects
   - Verifies: Both cards and attacks are recognized as game objects

3. **test_object_owner_matches_card_owner**
   - Tests: Rule 1.2.1a - Object owner = card owner
   - Verifies: Card object's `owner_id` matches the player who owns the card

4. **test_object_without_card_has_no_owner**
   - Tests: Rule 1.2.1a - Objects without card/macro/layer have no owner
   - Verifies: Attack-proxy with no source has `owner_id = None`

5. **test_card_in_hand_has_no_controller**
   - Tests: Rule 1.2.1b - Cards outside arena/stack have no controller
   - Verifies: Card in hand has `controller_id = None`

6. **test_card_in_arena_has_controller**
   - Tests: Rule 1.2.1b - Cards in arena have a controller
   - Verifies: Card placed in arena has `controller_id` set to 0

7. **test_card_on_stack_has_controller**
   - Tests: Rule 1.2.1b - Cards on stack have a controller
   - Verifies: Card played to stack has `controller_id` set to 0

8. **test_every_object_has_object_identity**
   - Tests: Rule 1.2.2a - All objects have the "object" identity
   - Verifies: `get_object_identities()` includes "object"

9. **test_name_is_object_identity**
   - Tests: Rule 1.2.2b - Card name is an object identity
   - Verifies: "Lunging Press" card has "Lunging Press" as identity

10. **test_weapon_card_has_weapon_identity**
    - Tests: Rule 1.2.2c - Type is an object identity
    - Verifies: Weapon card has "weapon" as an identity

11. **test_attack_subtype_not_object_identity**
    - Tests: Rule 1.2.2c - Exception: "attack" subtype excluded from identities
    - Verifies: attack subtype does NOT appear via `get_object_identities_from_subtypes()`

12. **test_attack_card_has_attack_identity**
    - Tests: Rule 1.2.2d - Attack-cards have "attack" identity
    - Verifies: Attack action card has "attack" object identity (via Rule 1.2.2d, not subtype)

13. **test_every_card_has_card_identity**
    - Tests: Rule 1.2.2e - All cards have "card" identity
    - Verifies: Every card has "card" in `get_object_identities()`

14. **test_permanent_has_permanent_identity**
    - Tests: Rule 1.2.2f - Permanents in arena have "permanent" identity
    - Verifies: Equipment in arena has "permanent" as an object identity

15. **test_lki_captured_when_object_leaves**
    - Tests: Rule 1.2.3 - LKI is captured as snapshot
    - Verifies: LKI captures power=6 when attack card leaves combat chain

16. **test_lki_used_when_object_gone**
    - Tests: Rule 1.2.3a - LKI used for specific object references (Endless Arrow)
    - Verifies: Chain link uses LKI, go again still granted after card moved to hand

17. **test_lki_not_used_for_generic_references**
    - Tests: Rule 1.2.3a - LKI not used for generic zone references
    - Verifies: Generic "all cards in zone" reference doesn't use LKI

18. **test_lki_includes_all_effects**
    - Tests: Rule 1.2.3b - LKI includes all active effects
    - Verifies: LKI snapshot includes the +3 power buff that was active

19. **test_lki_is_immutable**
    - Tests: Rule 1.2.3c - LKI cannot be altered
    - Verifies: Effect fails to grant go again to LKI of gone card

20. **test_luminaris_lki_immutability**
    - Tests: Rule 1.2.3c - Luminaris example from the rules
    - Verifies: Adding yellow card to pitch AFTER card removed doesn't grant go again via LKI

21. **test_lki_is_not_legal_target**
    - Tests: Rule 1.2.3d - LKI is not a legal target
    - Verifies: Targeting LKI fails with "lki_not_legal_target" reason

22. **test_card_is_source_of_abilities**
    - Tests: Rule 1.2.4 - Cards are sources of abilities/effects
    - Verifies: Only CardInstance or macro can be declared as an effect source

23. **test_attack_proxy_source_is_card**
    - Tests: Rule 1.2.4 - Attack-proxies are sourced from cards/macros
    - Verifies: Attack-proxy's `source` attribute is the creating card

#### Engine Features Needed:
- `CardInstance.is_game_object` property (Rule 1.2.1)
- `TestAttack.is_game_object` property (Rule 1.2.1)
- `CardInstance.get_object_identities()` -> Set[str] (Rules 1.2.2a-h)
- `CardInstance.get_object_identities_from_subtypes()` -> Set[str] (Rule 1.2.2c exception)
- `CardInstance.controller_id` properly set via zone entry (Rule 1.2.1b)
- `LastKnownInformation` class with snapshot semantics (Rule 1.2.3)
- `LastKnownInformation.is_immutable` enforcement (Rule 1.2.3c)
- `LastKnownInformation.is_legal_target = False` (Rule 1.2.3d)
- `CombatChain` with LKI tracking (Rules 1.2.3, 1.2.3a)
- `AttackProxy` class with source card reference (Rule 1.2.4)
- `CardInstance.is_permanent` property (for zone-aware identity, Rule 1.2.2f)

### Section 1.3: Cards

**File**: `features/section_1_3_cards.feature`
**Step Definitions**: `step_defs/test_section_1_3_cards.py`

This section tests card definitions, categories, permanents, and distinctness:
- **Rule 1.3.1**: A card is an object represented by an official Flesh and Blood card
- **Rule 1.3.1b**: Controller assignment (None outside arena/stack; owner as it enters arena or player who played it)
- **Rule 1.3.2**: Four card categories: hero-, token-, deck-, and arena-cards
- **Rule 1.3.2a**: Hero-cards have the type hero and start as a player's hero
- **Rule 1.3.2b**: Token-cards have the type token and are NOT part of a player's card-pool
- **Rule 1.3.2c**: Deck-cards (Action, Attack Reaction, Block, Defense Reaction, Instant, Mentor, Resource) may start in deck
- **Rule 1.3.2d**: Arena-cards (non-hero, non-token, non-deck) cannot start in deck
- **Rule 1.3.3**: Permanents (hero-, arena-, token-cards in arena; deck-cards with permanent subtypes in arena)
- **Rule 1.3.3a**: Permanents lose that status when they leave the arena
- **Rule 1.3.3b**: Permanents have untapped/tapped states; default untapped on entry
- **Rule 1.3.4**: Card distinctness based on face name and/or pitch value

#### Test Scenarios:

1. **test_card_in_hand_has_no_controller**
   - Tests: Rule 1.3.1b - Cards outside arena/stack have no controller
   - Verifies: `controller_id` is None for cards in hand

2. **test_card_in_deck_has_no_controller**
   - Tests: Rule 1.3.1b - Cards in deck have no controller
   - Verifies: `controller_id` is None for cards in deck

3. **test_card_in_graveyard_has_no_controller**
   - Tests: Rule 1.3.1b - Cards in graveyard have no controller
   - Verifies: `controller_id` is None for cards in graveyard

4. **test_card_entering_arena_gets_controller**
   - Tests: Rule 1.3.1b - Card entering arena gets controller set to its owner
   - Verifies: `controller_id` set to 0 when card enters arena

5. **test_card_played_to_stack_has_controller**
   - Tests: Rule 1.3.1b - Card played to stack gets controller assigned
   - Verifies: `controller_id` set to 0 when card played to stack

6. **test_hero_card_classified_as_hero_card**
   - Tests: Rule 1.3.2a - Cards with type HERO are hero-cards
   - Verifies: `get_card_category()` returns "hero" and not deck/token/arena

7. **test_token_card_classified_and_excluded_from_card_pool**
   - Tests: Rule 1.3.2b - Token cards are token-cards and not in card-pool
   - Verifies: `get_card_category()` returns "token", `is_valid_for_card_pool()` returns False

8. **test_action_card_classified_as_deck_card**
   - Tests: Rule 1.3.2c - Action cards are deck-cards
   - Verifies: Category is "deck" and can start in deck

9. **test_attack_reaction_card_classified_as_deck_card**
   - Tests: Rule 1.3.2c - Attack Reaction cards are deck-cards

10. **test_defense_reaction_card_classified_as_deck_card**
    - Tests: Rule 1.3.2c - Defense Reaction cards are deck-cards

11. **test_instant_card_classified_as_deck_card**
    - Tests: Rule 1.3.2c - Instant cards are deck-cards

12. **test_resource_card_classified_as_deck_card**
    - Tests: Rule 1.3.2c - Resource cards are deck-cards

13. **test_mentor_card_classified_as_deck_card**
    - Tests: Rule 1.3.2c - Mentor cards are deck-cards

14. **test_equipment_card_classified_as_arena_card**
    - Tests: Rule 1.3.2d - Equipment cards are arena-cards
    - Verifies: Cannot start the game in a player's deck

15. **test_weapon_card_classified_as_arena_card**
    - Tests: Rule 1.3.2d - Weapon cards are arena-cards

16. **test_hero_card_in_arena_is_permanent**
    - Tests: Rule 1.3.3 - Hero-cards in arena are permanents

17. **test_equipment_card_in_arena_is_permanent**
    - Tests: Rule 1.3.3 - Arena-cards (equipment) in arena are permanents

18. **test_token_card_in_arena_is_permanent**
    - Tests: Rule 1.3.3 - Token-cards in arena are permanents

19. **test_deck_card_with_ally_subtype_in_arena_is_permanent**
    - Tests: Rule 1.3.3 - Deck-cards with permanent subtype (Ally) in arena are permanents

20. **test_deck_card_without_permanent_subtype_not_permanent**
    - Tests: Rule 1.3.3 - Action cards without permanent subtypes in arena are NOT permanents

21. **test_deck_card_on_combat_chain_not_permanent**
    - Tests: Rule 1.3.3 - Cards on combat chain are never permanents

22. **test_permanent_leaving_arena_loses_permanent_status**
    - Tests: Rule 1.3.3a - Permanents lose status when leaving arena

23. **test_permanent_enters_arena_untapped**
    - Tests: Rule 1.3.3b - Permanents enter arena in untapped state

24. **test_permanent_can_be_tapped**
    - Tests: Rule 1.3.3b - Permanents can transition to tapped state

25. **test_tapped_permanent_can_be_untapped**
    - Tests: Rule 1.3.3b - Tapped permanents can be untapped

26. **test_cards_with_different_names_are_distinct**
    - Tests: Rule 1.3.4 - Cards with different names are distinct

27. **test_cards_with_same_name_different_pitch_are_distinct**
    - Tests: Rule 1.3.4 - Sink Below red (pitch 1) is distinct from Sink Below blue (pitch 2)

28. **test_cards_with_identical_name_and_pitch_not_distinct**
    - Tests: Rule 1.3.4 - Cards with same name and pitch are NOT distinct

#### Engine Features Needed:
- `CardType.TOKEN` enum value (Rule 1.3.2b)
- `CardType.BLOCK`, `CardType.RESOURCE`, `CardType.MENTOR` enum values (Rule 1.3.2c)
- `Subtype.ALLY`, `Subtype.AFFLICTION`, `Subtype.ASH`, `Subtype.CONSTRUCT`, `Subtype.FIGMENT`, `Subtype.INVOCATION`, `Subtype.LANDMARK` (Rule 1.3.3)
- `CardTemplate.get_category()` -> str ("hero"/"token"/"deck"/"arena") (Rule 1.3.2)
- `CardTemplate.can_start_in_deck` property (Rule 1.3.2c/d)
- `CardTemplate.is_part_of_card_pool` property returning False for tokens (Rule 1.3.2b)
- `CardInstance.is_permanent` property with zone/subtype logic (Rule 1.3.3)
- `CardTemplate.is_distinct_from(other)` method (Rule 1.3.4)

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
- [x] 1.2: Objects
- [x] 1.3: Cards
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
