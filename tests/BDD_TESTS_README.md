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

### Section 1.5: Macros

**File**: `features/section_1_5_macros.feature`
**Step Definitions**: `step_defs/test_section_1_5_macros.py`

This section tests macro object rules in Flesh and Blood:
- **Rule 1.5.1**: A macro is a non-card object in the arena
- **Rule 1.5.1a**: A macro has no owner
- **Rule 1.5.1b**: The controller of a macro is determined by the tournament rule that created it
- **Rule 1.5.2**: A macro cannot be and is not considered part of a player's card-pool
- **Rule 1.5.3**: If a macro leaves the arena, it is removed from the game
- **Rule 8.1.13a**: Only macro objects have the macro type

#### Test Scenarios:

1. **test_macro_is_non_card_game_object**
   - Tests: Rule 1.5.1 - Macro is a non-card object
   - Verifies: Macro is recognized as a game object but NOT as a card

2. **test_macro_exists_in_arena_zone**
   - Tests: Rule 1.5.1 - Macro is located in the arena
   - Verifies: Macro is in the arena and not in any other zone

3. **test_macro_has_no_owner**
   - Tests: Rule 1.5.1a - Macro has no owner
   - Verifies: `owner_id` is None

4. **test_macro_controller_set_by_tournament_rule**
   - Tests: Rule 1.5.1b - Controller assigned by tournament rule
   - Verifies: `controller_id` set to the player designated by tournament rule

5. **test_macro_controller_can_be_any_player**
   - Tests: Rule 1.5.1b - Any player can be assigned as controller
   - Verifies: `controller_id` can be set to player 1 (not just player 0)

6. **test_macro_not_part_of_card_pool**
   - Tests: Rule 1.5.2 - Macro is not in card-pool
   - Verifies: `is_in_card_pool` returns False

7. **test_macro_represented_by_physical_card_not_in_card_pool**
   - Tests: Rule 1.5.2 - Even physical-card-represented macros are not in card-pool
   - Verifies: Physical card representation doesn't change card-pool exclusion

8. **test_macro_leaving_arena_removed_from_game**
   - Tests: Rule 1.5.3 - Macro removed from game when leaving arena
   - Verifies: `is_removed_from_game` becomes True after leaving arena

9. **test_macro_destroyed_removed_not_graveyard**
   - Tests: Rule 1.5.3 - Macro goes to removed-from-game, not graveyard
   - Verifies: Macro not in graveyard after destruction

10. **test_only_macros_have_macro_type**
    - Tests: Rule 8.1.13a - Only macros have the macro type
    - Verifies: Macro has type_name 'macro'; regular card does not

11. **test_macro_has_abilities_from_creating_rule**
    - Tests: Rule 1.7.1 - Macro abilities come from creating rule/effect
    - Verifies: Macro has abilities defined by the creating tournament rule or effect

#### Engine Features Needed:
- `MacroObject` class (Rule 1.5.1) - non-card arena object
- `MacroObject.owner_id = None` always (Rule 1.5.1a)
- `MacroObject.controller_id` set by tournament rule (Rule 1.5.1b)
- `MacroObject.is_in_card_pool = False` (Rule 1.5.2)
- `Engine.remove_from_game(macro)` when macro leaves arena (Rule 1.5.3)
- `MacroObject.type_name = 'macro'` (Rule 8.1.13a)
- `MacroObject.abilities` list set by creating rule/effect (Rule 1.7.1)

### Section 1.6: Layers

**File**: `features/section_1_6_layers.feature`
**Step Definitions**: `step_defs/test_section_1_6_layers.py`

This section tests layer objects in Flesh and Blood. Layers are objects on the stack awaiting resolution:
- **Rule 1.6.1**: A layer is an object on the stack that is yet to be resolved
- **Rule 1.6.1a**: Owner determination for each layer type (card-layer = card owner; activated-layer = activating player; triggered-layer = source controller at trigger time)
- **Rule 1.6.1b**: Controller of a layer = player who put it on the stack
- **Rule 1.6.2**: Three layer categories: card-, activated-, triggered-layers
- **Rule 1.6.2a**: A card-layer is a layer represented by a card on the stack
- **Rule 1.6.2b**: An activated-layer is created by an activated ability; can only exist on the stack (Energy Potion example)
- **Rule 1.6.2c**: A triggered-layer is created by a triggered effect; created before placement on stack (Snatch example)

#### Test Scenarios:

1. **test_layer_is_object_on_stack_yet_to_be_resolved**
   - Tests: Rule 1.6.1 - Layers are stack objects
   - Verifies: Card played to stack creates a layer that hasn't resolved yet

2. **test_all_three_layer_types_are_layers**
   - Tests: Rule 1.6.1 - All three layer types recognized as layers
   - Verifies: Card-layer, activated-layer, triggered-layer all have `is_layer = True`

3. **test_card_layer_owner_is_card_owner**
   - Tests: Rule 1.6.1a - Card-layer owner = card owner
   - Verifies: `owner_id` of card-layer matches owner of the card

4. **test_activated_layer_owner_is_activating_player**
   - Tests: Rule 1.6.1a - Activated-layer owner = activating player
   - Verifies: `owner_id` of activated-layer is the player who activated the ability

5. **test_triggered_layer_owner_is_controller_at_trigger_time**
   - Tests: Rule 1.6.1a - Triggered-layer owner = source controller when triggered
   - Verifies: `owner_id` of triggered-layer is the controller at trigger time

6. **test_triggered_layer_owner_uses_controller_at_trigger_time**
   - Tests: Rule 1.6.1a - Owner tracks controller at trigger time, not current controller
   - Verifies: When controller changes before triggering, owner reflects new controller

7. **test_card_layer_controller_is_player_who_put_on_stack**
   - Tests: Rule 1.6.1b - Controller = player who put layer on stack
   - Verifies: `controller_id` is player 0 for card played by player 0

8. **test_activated_layer_controller_is_activating_player**
   - Tests: Rule 1.6.1b - Controller of activated-layer = activating player
   - Verifies: `controller_id` is set correctly

9. **test_triggered_layer_controller_is_player_who_put_on_stack**
   - Tests: Rule 1.6.1b - Controller of triggered-layer = player who put it on stack
   - Verifies: `controller_id` set when triggered-layer placed on stack

10. **test_there_are_exactly_3_layer_categories**
    - Tests: Rule 1.6.2 - Exactly 3 layer categories exist
    - Verifies: `LayerCategory` enum has exactly 3 values (FAILS - missing engine feature)

11. **test_card_played_to_stack_becomes_card_layer**
    - Tests: Rule 1.6.2a - Card on stack is a card-layer
    - Verifies: `layer_category == "card-layer"` and card reference preserved

12. **test_card_layer_retains_card_properties**
    - Tests: Rule 1.6.2a - Card-layer retains card properties (name, etc.)
    - Verifies: Layer name matches original card name ("Lunging Press")

13. **test_activating_ability_creates_activated_layer**
    - Tests: Rule 1.6.2b - Activated ability creates activated-layer (Energy Potion)
    - Verifies: `layer_category == "activated-layer"` with correct resolution ability

14. **test_activated_layer_can_only_exist_on_stack**
    - Tests: Rule 1.6.2b - Activated-layer restricted to stack zone
    - Verifies: `can_only_exist_on_stack == True`, no other zones valid

15. **test_triggered_effect_creates_triggered_layer**
    - Tests: Rule 1.6.2c - Triggered effect creates triggered-layer (Snatch)
    - Verifies: `layer_category == "triggered-layer"` with correct resolution ability

16. **test_triggered_layer_created_before_put_on_stack**
    - Tests: Rule 1.6.2c - Triggered-layer creation is two-step process
    - Verifies: Layer created as object first, then placed on stack

17. **test_triggered_layer_can_only_exist_on_stack**
    - Tests: Rule 1.6.2c - Triggered-layer restricted to stack zone
    - Verifies: `can_only_exist_on_stack == True`

18. **test_activated_layer_survives_source_destruction**
    - Tests: Rule 1.7.1a cross-ref - Activated-layers exist independently of source
    - Verifies: Layer persists on stack after source (Energy Potion) is destroyed

19. **test_triggered_layer_survives_source_leaving_play**
    - Tests: Rule 1.7.1a cross-ref - Triggered-layers exist independently of source
    - Verifies: Layer persists on stack after source moves to graveyard

#### Engine Features Needed:
- `fab_engine.engine.layers` module with `LayerCategory` enum (Rule 1.6.2)
- `CardLayer` class wrapping CardInstance on the stack (Rule 1.6.2a)
- `ActivatedLayer` class created by activated ability (Rule 1.6.2b)
- `TriggeredLayer` class created by triggered effect (Rule 1.6.2c)
- `Layer.owner_id` per layer type rules (Rule 1.6.1a)
- `Layer.controller_id = player who put it on stack` (Rule 1.6.1b)
- `Layer.can_only_exist_on_stack` property (Rules 1.6.2b, 1.6.2c)
- `Layer.is_prevented_by_source_absence = False` (Rule 1.7.1a)
- `Stack` zone tracking all layer types

### Section 1.4: Attacks

**File**: `features/section_1_4_attacks.feature`
**Step Definitions**: `step_defs/test_section_1_4_attacks.py`

This section tests attack concepts in Flesh and Blood:
- **Rule 1.4.1**: Attacks as objects (attack-cards, attack-proxies, attack-layers)
- **Rule 1.4.1a**: Attack owner = owner of the card or activated ability
- **Rule 1.4.1b**: Attack controller = controller of the representing object
- **Rule 1.4.2**: Attack-cards: cards with attack subtype on stack or combat chain
- **Rule 1.4.2a**: Context-dependent attack status (only on stack/chain)
- **Rule 1.4.3**: Attack-proxies: non-card objects representing another object's attack
- **Rule 1.4.3a**: Property inheritance (not a copy; excludes resolution abilities)
- **Rule 1.4.3b**: Attack-source is the object an attack-proxy represents
- **Rule 1.4.3c**: Proxy lifetime tied to attack-source on same chain link
- **Rule 1.4.3d**: Modified source properties inherited; direct effects not transitive
- **Rule 1.4.3e**: Proxy-specific effects don't apply to attack-source
- **Rule 1.4.4**: Attack-layers: attacks with no properties on stack
- **Rule 1.4.4a**: Attack-layer is either a typical layer or an attack, not both
- **Rule 1.4.4b**: Attack-layer separate from source for attack-specific effects
- **Rule 1.4.5**: Attack-targets: opponent-controlled attackable objects
- **Rule 1.4.5a**: Attackable = living object or made attackable by effect (Spectra)
- **Rule 1.4.5b**: Target persists until chain closes; new targets don't close chain
- **Rule 1.4.5c**: Multiple targets must be separate and legal
- **Rule 1.4.6**: Attack prevention by rule or effect

#### Test Scenarios:

1. **test_attack_card_on_stack_is_attack**
   - Tests: Rule 1.4.1 - Attack-card on stack recognized as attack
   - Verifies: `is_on_stack` + `is_attack_card` flags identify attack

2. **test_attack_card_on_combat_chain_is_attack**
   - Tests: Rule 1.4.1 - Attack-card on combat chain recognized as attack
   - Verifies: `_is_on_combat_chain` + `_was_put_on_chain_as_attack` flags

3. **test_attack_owner_matches_card_owner**
   - Tests: Rule 1.4.1a - Attack owner = card owner
   - Verifies: `attack.owner_id` matches player who owns the card

4. **test_attack_controller_matches_card_controller**
   - Tests: Rule 1.4.1b - Attack controller = object controller
   - Verifies: `controller_id` is set when card is played to stack (FAILS - missing engine feature)

5. **test_attack_subtype_card_on_stack_is_attack_card**
   - Tests: Rule 1.4.2 - Card with attack subtype on stack is attack-card
   - Verifies: Zone-aware attack recognition

6. **test_attack_subtype_card_in_hand_not_attack**
   - Tests: Rule 1.4.2a - Attack subtype card in hand is NOT an attack
   - Verifies: Non-stack/chain cards not recognized as attacks

7. **test_attack_subtype_card_in_graveyard_not_attack**
   - Tests: Rule 1.4.2a - Attack subtype card in graveyard is NOT an attack
   - Verifies: Zone-aware attack check

8. **test_card_put_on_combat_chain_as_attack_is_attack_card**
   - Tests: Rule 1.4.2a - Card put on chain as attack IS an attack-card
   - Verifies: `_was_put_on_chain_as_attack` tracking

9. **test_attack_proxy_represents_attack_source**
   - Tests: Rule 1.4.3 - Attack-proxy represents weapon's attack (Bone Basher)
   - Verifies: `proxy.source` references the weapon

10. **test_attack_proxy_inherits_properties**
    - Tests: Rule 1.4.3a - Proxy inherits power and supertype (Edge of Autumn)
    - Verifies: Power and supertype inherited from attack-source

11. **test_attack_proxy_not_inherit_resolution_abilities**
    - Tests: Rule 1.4.3a - Proxy does NOT inherit resolution abilities
    - Verifies: `_has_go_again_resolution_ability` not inherited by proxy

12. **test_attack_proxy_is_separate_not_copy**
    - Tests: Rule 1.4.3a - Proxy is a separate object, not a copy
    - Verifies: `proxy is not source`

13. **test_attack_source_represented_by_proxy**
    - Tests: Rule 1.4.3b - Attack-source is the object represented (Cintari Sellsword)
    - Verifies: `proxy.source.name == "Cintari Sellsword"`

14. **test_attack_proxy_ceases_when_source_on_different_chain_link**
    - Tests: Rule 1.4.3c - Proxy ceases when source moves to different chain link
    - Verifies: `_has_ceased` flag and LKI captured

15. **test_attack_proxy_persists_when_ability_creator_gone**
    - Tests: Rule 1.4.3c - Proxy persists even if ability-granting card ceases (Iris of Reality)
    - Verifies: Proxy does NOT cease when `_ability_granter_ceased = True`

16. **test_modified_source_properties_inherited_by_proxy**
    - Tests: Rule 1.4.3d - Modified source properties inherited (Ironsong Determination)
    - Verifies: Proxy has modified power value (3+1=4)

17. **test_effect_on_source_not_directly_on_proxy**
    - Tests: Rule 1.4.3d - Direct source effects don't apply to proxy (Fog Down)
    - Verifies: `_fog_down_applies` is False on proxy

18. **test_effect_on_proxy_not_on_source**
    - Tests: Rule 1.4.3e - Proxy effects don't apply to source (Sharpen Steel)
    - Verifies: Power bonus on proxy doesn't carry to weapon

19. **test_attack_layer_is_attack_with_no_properties**
    - Tests: Rule 1.4.4 - Attack-layer has no properties (Emperor example)
    - Verifies: `AttackLayerStub.has_no_properties == True`

20. **test_attack_layer_not_both_layer_and_attack**
    - Tests: Rule 1.4.4a - Attack-layer is layer OR attack, not both
    - Verifies: Draconic attack effect doesn't match attack-layer

21. **test_attack_layer_separate_from_source_for_attack_effects**
    - Tests: Rule 1.4.4b - Attack-layer separate from source for attack effects
    - Verifies: Attack-specific effect applies to layer, source checkable separately

22. **test_player_must_declare_attack_target**
    - Tests: Rule 1.4.5 - Player must declare attack-target on stack
    - Verifies: Attack on stack has null target (engine must enforce declaration)

23. **test_attack_target_must_be_opponent_controlled**
    - Tests: Rule 1.4.5 - Target must be opponent-controlled
    - Verifies: Attacker is player 0; target must be from player 1+

24. **test_living_object_is_valid_attack_target**
    - Tests: Rule 1.4.5a - Living objects are attackable
    - Verifies: Hero `_is_living_object = True` -> valid target

25. **test_non_living_object_not_attackable_by_default**
    - Tests: Rule 1.4.5a - Non-living objects not attackable by default
    - Verifies: Equipment without Spectra -> invalid target

26. **test_effect_can_make_object_attackable**
    - Tests: Rule 1.4.5a - Spectra makes non-living object attackable
    - Verifies: `_made_attackable = True` -> valid target

27. **test_attack_target_persists_until_chain_closes**
    - Tests: Rule 1.4.5b - Target persists until chain closes
    - Verifies: Chain doesn't close with different target on second attack

28. **test_different_target_does_not_close_chain**
    - Tests: Rule 1.4.5b - Different target doesn't close chain
    - Verifies: Chain remains open; second attack has its own target

29. **test_multiple_targets_must_be_separate_and_legal**
    - Tests: Rule 1.4.5c - Multiple targets must be separate and legal
    - Verifies: Two different legal targets are valid

30. **test_cannot_declare_same_object_as_multiple_targets**
    - Tests: Rule 1.4.5c - Same object cannot be two targets
    - Verifies: Duplicate targets rejected (`multi_targets_valid = False`)

31. **test_attack_prevented_by_rule**
    - Tests: Rule 1.4.6 - "cannot_attack" restriction prevents attack play
    - Verifies: `attack_play_result = False` when restriction active

32. **test_weapon_attack_prevented_by_effect**
    - Tests: Rule 1.4.6 - "cannot_attack_with_weapons" prevents weapon activation
    - Verifies: `weapon_attack_result = False` when restriction active

#### Engine Features Needed:
- `CardInstance.controller_id` set when card is played to stack (Rule 1.4.1b)
- `CardInstance.is_attack_in_context(zone)` property (Rules 1.4.1, 1.4.2)
- `Attack.owner_id` and `Attack.controller_id` properties (Rules 1.4.1a/b)
- `AttackProxy` class with `source`, `_power`, `_chain_link` attributes (Rule 1.4.3)
- `AttackProxy.inherits_properties()` from source (Rule 1.4.3a)
- `AttackProxy` excludes resolution abilities from inheritance (Rule 1.4.3a)
- `CombatChain` class with chain link management (Rules 1.4.3c, 1.4.5b)
- `CombatChain.advance_chain_link()` causing proxy cessation (Rule 1.4.3c)
- LKI capture for ceased attack-proxies (Rules 1.4.3c, 1.2.3)
- Effect system scoping to proxy vs source (Rules 1.4.3d, 1.4.3e)
- `AttackLayer` class (Rule 1.4.4) with `has_no_properties = True`
- `AttackLayer` treated as layer OR attack, not both (Rule 1.4.4a)
- `AttackTargetDeclaration.validate_attackable()` (Rule 1.4.5a)
- `AttackTargetDeclaration.validate_opponent_controlled()` (Rule 1.4.5)
- `CombatChain.does_not_close_on_different_target()` (Rule 1.4.5b)
- Multi-target validation rejecting duplicates (Rule 1.4.5c)
- Attack prevention check via `PrecedenceManager` (Rule 1.4.6)

### Section 1.7: Abilities

**File**: `features/section_1_7_abilities.feature`
**Step Definitions**: `step_defs/test_section_1_7_abilities.py`

This section tests ability rules in Flesh and Blood:
- **Rule 1.7.1**: An ability is a property of an object influencing the game
- **Rule 1.7.1a**: Source of an ability; activated/triggered-layers exist independently
- **Rule 1.7.1b**: Controller of activated-layer (activating player) and triggered-layer (source controller)
- **Rule 1.7.2**: Object with ability is considered card with that ability; base vs. derived
- **Rule 1.7.3**: Three ability categories: activated, resolution, static
- **Rule 1.7.4**: Ability functionality conditions (when source is public and in arena)
- **Rule 1.7.4a**: Defending card ability exceptions
- **Rule 1.7.4b**: Activated ability outside arena when cost only payable outside
- **Rule 1.7.4c**: Resolution ability functional when resolving as layer
- **Rule 1.7.4d**: Meta-static ability functional outside the game
- **Rule 1.7.4e**: Play-static ability functional when source public and being played
- **Rule 1.7.4f**: Property-static ability functional in any zone
- **Rule 1.7.4g**: While-static ability functional when while-condition met
- **Rule 1.7.4j**: Zone-movement replacement static ability
- **Rule 1.7.5**: Modal abilities - choice of modes
- **Rule 1.7.5a-e**: Modal ability selection rules
- **Rule 1.7.6**: Connected ability pairs
- **Rule 1.7.6a-c**: Connected pair rules
- **Rule 1.7.7**: Abilities can be modified

#### Test Scenarios:

1. **test_ability_is_property_of_object** - Tests Rule 1.7.1 - Ability is a property of an object
2. **test_base_abilities_from_rules_text** - Tests Rule 1.7.1 - Base abilities from rules text for non-token cards
3. **test_token_base_abilities_from_creating_effect** - Tests Rule 1.7.1 - Token abilities from creating effect
4. **test_ability_source_is_card_that_has_it** - Tests Rule 1.7.1a - Source of ability is the card
5. **test_activated_layer_source_is_same_as_creating_ability_source** - Tests Rule 1.7.1a - Activated-layer source
6. **test_activated_layer_survives_source_destruction** - Tests Rule 1.7.1a - Layer exists independently
7. **test_triggered_layer_survives_source_leaving_play** - Tests Rule 1.7.1a - Triggered-layer exists independently
8. **test_activated_layer_controller_is_activating_player** - Tests Rule 1.7.1b - Activated-layer controller
9. **test_triggered_layer_controller_is_controller_at_trigger_time** - Tests Rule 1.7.1b - Triggered-layer controller
10. **test_triggered_layer_controller_is_owner_when_source_has_no_controller** - Tests Rule 1.7.1b - Uses owner
11. **test_object_with_ability_considered_card_with_ability** - Tests Rule 1.7.2 - Object with ability
12. **test_triggered_go_again_not_base_go_again** - Tests Rule 1.7.2 - Torrent of Tempo example
13. **test_card_with_triggered_go_again_gains_ability_after_trigger** - Tests Rule 1.7.2 - After triggering
14. **test_there_are_three_categories_of_abilities** - Tests Rule 1.7.3 - Exactly 3 categories
15. **test_activated_ability_creates_activated_layer_on_stack** - Tests Rule 1.7.3a - Activated ability
16. **test_resolution_ability_generates_effects_on_resolution** - Tests Rule 1.7.3b - Resolution ability
17. **test_static_ability_generates_effects_continuously** - Tests Rule 1.7.3c - Static ability
18. **test_ability_functional_when_source_in_arena** - Tests Rule 1.7.4 - Functional in arena
19. **test_ability_nonfunctional_when_source_in_hand** - Tests Rule 1.7.4 - Non-functional outside arena
20. **test_defending_card_ability_nonfunctional_by_default** - Tests Rule 1.7.4a - Defending card
21. **test_defending_card_ability_functional_when_specified_as_defending_only** - Tests Rule 1.7.4a - Rally
22. **test_activated_ability_functional_when_cost_only_payable_outside_arena** - Tests Rule 1.7.4b - Mighty Windup
23. **test_resolution_ability_functional_when_layer_resolves** - Tests Rule 1.7.4c - Sigil of Solace
24. **test_resolution_ability_nonfunctional_when_source_not_resolving** - Tests Rule 1.7.4c - Non-resolving
25. **test_meta_static_ability_functional_outside_game** - Tests Rule 1.7.4d - Specialization keyword
26. **test_play_static_ability_functional_when_source_being_played** - Tests Rule 1.7.4e - Ghostly Visit
27. **test_property_static_ability_functional_in_any_zone** - Tests Rule 1.7.4f - Mutated Mass
28. **test_while_static_ability_functional_when_condition_met** - Tests Rule 1.7.4g - Yinti Yanti
29. **test_while_static_ability_nonfunctional_when_condition_not_met** - Tests Rule 1.7.4g - Condition not met
30. **test_zone_movement_replacement_static_functional_when_condition_met** - Tests Rule 1.7.4j - Drone of Brutality
31. **test_modal_ability_provides_choice_of_modes** - Tests Rule 1.7.5 - Art of War
32. **test_cannot_select_same_mode_twice_without_permission** - Tests Rule 1.7.5b - Duplicate modes
33. **test_can_only_select_available_modes** - Tests Rule 1.7.5b - Maximum modes
34. **test_selected_modes_become_base_abilities** - Tests Rule 1.7.5d - Modes become base abilities
35. **test_mode_count_evaluated_at_mode_selection_time** - Tests Rule 1.7.5e - Sacred Art example
36. **test_connected_ability_pair_following_refers_to_leading** - Tests Rule 1.7.6 - Reckless Swing
37. **test_following_ability_fails_when_leading_events_unavailable** - Tests Rule 1.7.6b - Following fails
38. **test_connected_pair_added_together_is_connected** - Tests Rule 1.7.6c - Added pair is connected
39. **test_object_abilities_can_be_modified** - Tests Rule 1.7.7 - Ability modification

#### Engine Features Needed:
- `CardInstance.has_ability(name)` and `has_base_ability(name)` properties (Rule 1.7.2)
- `CardInstance.get_base_abilities()` method (Rule 1.7.1)
- `CardInstance.get_ability_source(name)` method (Rule 1.7.1a)
- `CardInstance.static_ability_is_active(name)` method (Rule 1.7.3c)
- `fab_engine.engine.abilities` module with `AbilityCategory` enum (Rule 1.7.3)
- Ability class hierarchy: `ActivatedAbility`, `ResolutionAbility`, `StaticAbility` (Rule 1.7.3)
- `Ability.is_functional(context)` method with full functionality check (Rule 1.7.4)
- `ActivatedLayer` and `TriggeredLayer` classes with `source`, `controller_id`, and `exists_independently_of_source` (Rules 1.7.1a, 1.7.1b)
- `ModalAbility` with `declare_modes()` validation (Rule 1.7.5)
- `ConnectedAbilityPair` with following/leading tracking (Rule 1.7.6)
- Effect system supporting ability modification (Rule 1.7.7)
- Play-static ability granting allowances in the PrecedenceManager (Rule 1.7.4e)

### Section 1.8: Effects

**File**: `features/section_1_8_effects.feature`
**Step Definitions**: `step_defs/test_section_1_8_effects.py`

This section tests effect rules in Flesh and Blood:
- **Rule 1.8.1**: Effects are generated by resolving layers or abilities; always have a source and a controller
- **Rule 1.8.2**: One-shot effects (do something once) vs. continuous effects (affect game state over time)
- **Rule 1.8.3**: Optional effects use "may" phrasing; mandatory effects must be executed
- **Rule 1.8.3a**: Optional effects that cannot fully resolve may not be generated
- **Rule 1.8.4**: Effects with targets require legal targets when generated; target locks in on stack
- **Rule 1.8.4a**: If target ceases to exist or becomes illegal before resolution, effect fails
- **Rule 1.8.5**: Parameters are determined by the player who controls the effect at resolution time
- **Rule 1.8.5a**: Parameters limited to public game objects in the arena or on the stack
- **Rule 1.8.5b**: Required number of parameters; if insufficient, use all available
- **Rule 1.8.5c**: Effect fails if no legal parameters at generation
- **Rule 1.8.5d**: Multiple players determine parameters in clockwise order
- **Rule 1.8.5e**: Player determines order of compound events
- **Rule 1.8.6**: Effect conditions apply to all events; object must have the property
- **Rule 1.8.6a**: Objects without the specified cost property are not restricted by cost effects
- **Rule 1.8.7**: Effects apply to all game objects matching the description (not a specific subset)
- **Rule 1.8.7a**: Missing numeric properties treated as zero for effect calculation
- **Rule 1.8.8**: "As though" effects apply only for the specific applicable effect
- **Rule 1.8.8a**: "Counts as" effects apply only for the specific applicable effect
- **Rule 1.8.9**: Retargeting effects redirect to new valid target; if no valid new target, original unchanged
- **Rule 1.8.10**: "Your next attack" refers to the next attack that comes under the player's control
- **Rule 1.8.10a**: Object already under player's control that becomes specified type does not get "next attack" effect

#### Test Scenarios:

1. **test_effect_has_source_and_controller** - Tests Rule 1.8.1 - Effects have source and controller
2. **test_effect_generated_by_resolving_layer** - Tests Rule 1.8.1 - Effect generated by resolving layer
3. **test_one_shot_effect_executes_once** - Tests Rule 1.8.2 - One-shot effect fires once
4. **test_continuous_effect_persists_over_time** - Tests Rule 1.8.2 - Continuous effect persists
5. **test_optional_effect_with_may_phrasing** - Tests Rule 1.8.3 - Optional "may" phrasing
6. **test_mandatory_effect_must_execute** - Tests Rule 1.8.3 - Mandatory effect executes
7. **test_optional_effect_cannot_be_generated_if_cannot_fully_resolve** - Tests Rule 1.8.3a - Cannot partially resolve
8. **test_targeted_effect_requires_legal_target_when_generated** - Tests Rule 1.8.4 - Target required at generation
9. **test_effect_fails_if_target_ceases_to_exist** - Tests Rule 1.8.4a - Target leaves before resolution
10. **test_effect_fails_if_target_becomes_illegal** - Tests Rule 1.8.4a - Target becomes illegal
11. **test_no_valid_new_target_leaves_original_unchanged** - Tests Rule 1.8.9 - Retarget with no valid new target
12. **test_player_determines_parameters_at_resolution** - Tests Rule 1.8.5 - Parameters at resolution
13. **test_effect_fails_with_no_legal_parameters** - Tests Rule 1.8.5c - No legal parameters fails
14. **test_multiple_players_determine_params_clockwise** - Tests Rule 1.8.5d - Clockwise order
15. **test_parameter_determination_limited_to_public_arena_stack** - Tests Rule 1.8.5a - Public arena/stack only
16. **test_insufficient_objects_uses_all_available** - Tests Rule 1.8.5b - Insufficient uses all available
17. **test_player_determines_compound_event_order** - Tests Rule 1.8.5e - Compound event ordering
18. **test_effect_condition_fails_for_objects_without_property** - Tests Rule 1.8.6 - Condition requires property
19. **test_cards_without_cost_property_not_restricted_by_cost_effects** - Tests Rule 1.8.6a - No cost property
20. **test_missing_numeric_property_treated_as_zero** - Tests Rule 1.8.7a - Missing numeric = zero
21. **test_as_though_effect_applies_only_for_applicable_effect** - Tests Rule 1.8.8 - "As though" scope
22. **test_counts_as_effect_applies_only_for_applicable_effect** - Tests Rule 1.8.8a - "Counts as" scope
23. **test_effect_fails_when_target_ceases_to_exist** - Tests Rule 1.8.4a - Target ceases to exist
24. **test_effect_does_not_fail_if_one_event_succeeds** - Tests Rule 1.8.4a - Partial success
25. **test_effect_fails_no_legal_params_at_generation** - Tests Rule 1.8.5c - No params at generation
26. **test_next_attack_effect_applies_to_next_attack** - Tests Rule 1.8.10 - Next attack bonus
27. **test_replaced_attack_triggers_next_attack_effect** - Tests Rule 1.8.10 - Stealth replacement attack
28. **test_attack_changing_properties_not_next_attack** - Tests Rule 1.8.10a - Already-controlled attack
29–44. Additional scenarios covering damage effects, targets, retargeting, conditions, and compound effects

#### Implementation Notes:
- `CardTemplate` is a frozen dataclass — set instance metadata on `CardInstance` using `card._has_no_cost_property = True` or `card._has_no_pitch_property = True` instead of modifying the template
- Duplicate step text across scenarios causes pytest-bdd to use the LAST definition; all step texts were made unique per scenario
- Helper stubs added to `bdd_helpers.py`: `DamageEffectStub`, `OptionalEffectStub`, `MultiTargetEffectStub`, `EffectResolutionResultStub`
- New helper methods added to `BDDGameState`: `create_damage_effect`, `check_card_has_effect`, `create_optional_effect`, `resolve_optional_effect`, `create_multi_target_damage_effect`, `resolve_targeted_effect`

#### Engine Features Needed:
- `Effect` base class with `source`, `controller_id`, `effect_type` (Rule 1.8.1)
- `OneShotEffect` and `ContinuousEffect` subclasses (Rule 1.8.2)
- `Effect.is_optional` flag and enforcement (Rule 1.8.3)
- `OptionalEffect.can_fully_resolve()` check (Rule 1.8.3a)
- `TargetedEffect` with `requires_legal_target_at_generation=True` (Rule 1.8.4)
- `Effect.target_is_legal()` and `Effect.fail_if_target_gone=True` (Rule 1.8.4a)
- `Effect.parameters` determined at resolution by controlling player (Rule 1.8.5)
- Parameter source restricted to public arena/stack objects (Rule 1.8.5a)
- `Effect.use_all_available_if_insufficient=True` (Rule 1.8.5b)
- `Effect.fail_if_no_legal_params_at_generation=True` (Rule 1.8.5c)
- Multi-player parameter determination in clockwise turn order (Rule 1.8.5d)
- `CompoundEffect.player_chooses_event_order=True` (Rule 1.8.5e)
- `Effect.condition` requiring objects to have the specified property (Rule 1.8.6)
- `Effect.use_zero_for_missing_numeric_property=True` (Rule 1.8.7a)
- `AsThroughEffect` and `CountsAsEffect` with scoped applicability (Rules 1.8.8, 1.8.8a)
- `RetargetEffect` with fallback to original target (Rule 1.8.9)
- `NextAttackEffect` tracking attacks coming under player control (Rule 1.8.10)
- `NextAttackEffect.does_not_apply_retroactively=True` for property changes (Rule 1.8.10a)

### Section 1.9: Events

**File**: `features/section_1_9_events.feature`
**Step Definitions**: `step_defs/test_section_1_9_events.py`

This section tests event rules in Flesh and Blood:
- **Rule 1.9.1**: An event is a change in game state (layer resolution, effect result, phase transition, or player action)
- **Rule 1.9.1a**: Outside-game events cannot be modified by in-game replacement effects or trigger in-game triggered effects, unless they directly interact with the game
- **Rule 1.9.1b**: Events comprising instructions to do nothing do not occur; cannot be modified or trigger effects
- **Rule 1.9.1c**: Player may choose to fail unverifiable instructions
- **Rule 1.9.2**: Compound events involve performing the same instruction multiple times, expanded into individual events
- **Rule 1.9.2a**: Triggered effects trigger once on compound event, not again for individual events
- **Rule 1.9.2b**: Replacement effects replacing compound events cannot also replace individual events
- **Rule 1.9.2c**: Multi-player events are compound events in clockwise order from turn player (or effect controller)
- **Rule 1.9.3**: Composite events are made up of one or more internal events
- **Rule 1.9.3a**: Triggered effects on composite events trigger only once
- **Rule 1.9.3b**: Prevented triggering applies to entire composite event and its internal events
- **Rule 1.9.3c**: Partially replacing internal events does not prevent composite event from occurring
- **Rule 1.9.3d**: Composite event does not occur if all internal events fail

#### Test Scenarios:

1. **test_layer_resolution_produces_an_event**
   - Tests: Rule 1.9.1 - Layer resolution is a source of events
   - Verifies: event_type = "layer_resolution" when a card on the stack resolves

2. **test_player_action_produces_an_event**
   - Tests: Rule 1.9.1 - Player actions produce events
   - Verifies: event_type = "player_action" when player draws a card

3. **test_turn_phase_transition_produces_an_event**
   - Tests: Rule 1.9.1 - Phase transitions produce events
   - Verifies: event_type = "phase_transition" when game moves to action phase

4. **test_event_can_be_modified_by_replacement_effect**
   - Tests: Rule 1.9.1 - Events can be modified by replacement effects
   - Verifies: Replacement effect doubles draw event

5. **test_event_can_trigger_a_triggered_effect**
   - Tests: Rule 1.9.1 - Events can trigger triggered effects
   - Verifies: Discard event fires triggered effect

6. **test_outside_game_event_cannot_be_modified_by_replacement_effects**
   - Tests: Rule 1.9.1a - Outside-game events not modifiable in-game
   - Verifies: Booster reveal event not modified by in-game replacement

7. **test_outside_game_event_that_interacts_with_game_can_be_modified**
   - Tests: Rule 1.9.1a - Game-interacting events from outside effects can be modified
   - Verifies: Put-into-hand event can be modified by zone-entry replacement

8. **test_zero_damage_event_does_not_occur**
   - Tests: Rule 1.9.1b - Blazing Aether example (0 damage = no event)
   - Verifies: event.occurred = False when X = 0

9. **test_non_occurring_event_cannot_be_modified_by_replacement_effects**
   - Tests: Rule 1.9.1b - Null events block replacement effects
   - Verifies: Replacement effect not applied to null event

10. **test_non_occurring_event_does_not_trigger_effects**
    - Tests: Rule 1.9.1b - Null events don't trigger triggered effects
    - Verifies: trigger_count = 0 when null event fires

11. **test_player_may_fail_unverifiable_instruction**
    - Tests: Rule 1.9.1c - Moon Wish example (private deck search)
    - Verifies: Player can choose to fail finding Sun Kiss

12. **test_player_cannot_fail_verifiable_instruction**
    - Tests: Rule 1.9.1c (converse) - Verifiable instructions must be completed
    - Verifies: Player cannot fail a draw when deck contents are verifiable

13. **test_draw_three_cards_is_a_compound_event**
    - Tests: Rule 1.9.2 - Tome of Harvests example ("Draw 3 cards")
    - Verifies: Compound event with 3 individual draw events in sequence

14. **test_compound_event_is_expanded_into_individual_events**
    - Tests: Rule 1.9.2 - Compact format expanded to individual events
    - Verifies: "Create 2 Runechant tokens" expands to 2 individual creation events

15. **test_triggered_effect_on_compound_event_fires_only_once**
    - Tests: Rule 1.9.2a - Korshem example
    - Verifies: Korshem triggers once on compound reveal, not 3 more times

16. **test_triggered_effect_does_not_re_trigger_on_individual_events_of_compound**
    - Tests: Rule 1.9.2a - Second compound trigger scenario
    - Verifies: Draw trigger fires once for compound of 3 draws

17. **test_replacement_effect_on_compound_event_cannot_replace_individual_events**
    - Tests: Rule 1.9.2b - Mordred Tide example
    - Verifies: 3+1=4 tokens created, not 8 (no cascade to individual events)

18. **test_replacement_of_compound_event_does_not_cascade_to_individual_events**
    - Tests: Rule 1.9.2b - Second compound replacement scenario
    - Verifies: Replacement of compound draw doesn't cascade

19. **test_multi_player_event_is_compound_event_in_clockwise_order_from_turn_player**
    - Tests: Rule 1.9.2c - This Round's on Me example
    - Verifies: "Each hero draws" starts with turn player (player 0)

20. **test_multi_player_event_from_effect_starts_with_effect_controller**
    - Tests: Rule 1.9.2c - Effect controller overrides turn player order
    - Verifies: "Each hero draws" from player 0's effect starts with player 0

21. **test_discard_is_a_composite_event_with_internal_events**
    - Tests: Rule 1.9.3 - Discard as composite event
    - Verifies: Composite discard has internal move event (hand → graveyard)

22. **test_composite_event_is_made_up_of_one_or_more_internal_events**
    - Tests: Rule 1.9.3 - Generic composite event structure
    - Verifies: Composite event tracks its internal events

23. **test_triggered_effect_only_triggers_once_on_composite_event**
    - Tests: Rule 1.9.3a - Single trigger from composite + internal
    - Verifies: Discard trigger fires once, not also from internal move event

24. **test_triggered_effect_on_composite_event_does_not_double_trigger**
    - Tests: Rule 1.9.3a - Double-matching trigger fires once
    - Verifies: trigger_count = 1 even if both composite and internal match

25. **test_preventing_trigger_on_composite_event_also_prevents_on_internal_events**
    - Tests: Rule 1.9.3b - Prevention applies to entire composite event
    - Verifies: Prevented trigger doesn't fire from internal events either

26. **test_replacing_internal_event_destination_does_not_prevent_composite_event**
    - Tests: Rule 1.9.3c - Discard to banished example
    - Verifies: Composite discard still occurs even with modified destination

27. **test_partial_modification_of_internal_event_leaves_composite_event_intact**
    - Tests: Rule 1.9.3c - General partial replacement
    - Verifies: Composite event persists when internal is partially replaced

28. **test_composite_event_does_not_occur_if_all_internal_events_are_replaced**
    - Tests: Rule 1.9.3d - Full replacement prevents composite
    - Verifies: composite.occurred = False when internal event fully replaced

29. **test_all_internal_events_fail_prevents_composite_event_triggering**
    - Tests: Rule 1.9.3d - No triggers from non-occurring composite
    - Verifies: Discard trigger doesn't fire when composite didn't occur

#### Engine Features Needed:
- `Event` class hierarchy: `Event`, `CompoundEvent`, `CompositeEvent` (Rule 1.9.1)
- `Event.event_type` attribute identifying source type (Rule 1.9.1)
- `Event.occurred` property (Rule 1.9.1b)
- `Event.is_outside_game` and `Event.directly_interacts_with_game` (Rule 1.9.1a)
- `ReplacementEffect.can_modify(event)` checking outside-game status (Rule 1.9.1a)
- `NullEvent` - event with `occurred = False` (Rule 1.9.1b)
- `UnverifiableInstruction` with `player_may_fail = True` (Rule 1.9.1c)
- `CompoundEvent.individual_events` list (Rule 1.9.2)
- `TriggeredEffect.fires_once_per_compound_event` (Rule 1.9.2a)
- `ReplacementEffect.applied_to_compound` tracking (Rule 1.9.2b)
- `MultiPlayerEvent` starting with turn player or effect controller (Rule 1.9.2c)
- `CompositeEvent.internal_events` list (Rule 1.9.3)
- `CompositeEvent.trigger_once_on_composite_event()` (Rule 1.9.3a)
- `TriggerPrevention.applies_to_composite_and_internal = True` (Rule 1.9.3b)
- `CompositeEvent.occurred = False` when all internal events fail (Rule 1.9.3d)

### Section 1.10: Game State

**File**: `features/section_1_10_game_state.feature`
**Step Definitions**: `step_defs/test_section_1_10_game_state.py`

This section tests game state concepts in Flesh and Blood:
- **Rule 1.10.1**: A game state is a moment in the game; priority state is where player receives priority
- **Rule 1.10.2**: When transitioning to a priority state, five game state actions execute in order:
  - **(a)** Hero death check — players with dead heroes lose (or draw)
  - **(b)** Clear living objects with 0 life simultaneously as one event
  - **(c)** Start continuous look effects based on card location
  - **(d)** Fire state-based triggered effects; add triggered layers to stack (clockwise from turn player)
  - **(e)** If combat chain is open and closed by rule/effect, begin Close Step
- **Rule 1.10.3**: Illegal actions reverse the game state to before the action started
- **Rule 1.10.3a**: Triggered effects do not fire from game state reversals
- **Rule 1.10.3b**: Replacement effects cannot modify reversal events
- **Rule 1.10.3c**: If full reversal is impossible, reverse as much as possible and continue from last legal state

#### Test Scenarios:

1. **test_game_state_is_discrete_moment**
   - Tests: Rule 1.10.1 - Game state is a moment in the game
   - Verifies: Game state can be captured as a snapshot representing a single moment

2. **test_priority_state_gives_priority_to_player**
   - Tests: Rule 1.10.1 - Priority state gives priority to a player
   - Verifies: When transitioning to priority state, active player has priority

3. **test_no_priority_during_game_state_actions**
   - Tests: Rule 1.10.1 - No player has priority during game state actions
   - Verifies: No priority given while executing game state actions

4. **test_hero_zero_life_triggers_loss**
   - Tests: Rule 1.10.2a - Hero at 0 life causes player loss
   - Verifies: First game state action checks for dead heroes

5. **test_simultaneous_hero_death_is_draw**
   - Tests: Rule 1.10.2a - All heroes dying simultaneously = draw
   - Verifies: game_result = "draw" when all heroes die

6. **test_living_object_zero_life_cleared**
   - Tests: Rule 1.10.2b - Living object at 0 life is cleared as second action
   - Verifies: Living permanent with 0 life removed from arena

7. **test_multiple_living_objects_cleared_simultaneously**
   - Tests: Rule 1.10.2b - Multiple 0-life living objects cleared as ONE event
   - Verifies: clearing_event_count == 1 for multiple objects

8. **test_hero_zero_life_is_action_1_not_action_2**
   - Tests: Rule 1.10.2a vs 1.10.2b - Hero death is action 1 not action 2
   - Verifies: hero_death_handled_in_action == 1

9. **test_continuous_look_effect_activates_at_action_3**
   - Tests: Rule 1.10.2c - Continuous look effects start at action 3
   - Verifies: look_effects_started includes player 0's effect

10. **test_state_based_triggered_effect_fires**
    - Tests: Rule 1.10.2d - State-based triggered effects fire at action 4
    - Verifies: state_based_triggers_fired > 0, triggered layers added to stack

11. **test_triggered_layers_added_in_clockwise_order**
    - Tests: Rule 1.10.2d - Multiple triggered layers added clockwise from turn player
    - Verifies: triggered_layer_order tracking exists

12. **test_combat_chain_closed_begins_close_step**
    - Tests: Rule 1.10.2e - Closed combat chain starts Close Step
    - Verifies: close_step_initiated = True when chain closed by effect

13. **test_no_close_step_without_open_combat_chain**
    - Tests: Rule 1.10.2e - No Close Step without open combat chain
    - Verifies: close_step_initiated = False when chain not open

14. **test_game_state_actions_performed_in_order**
    - Tests: Rule 1.10.2 - Actions executed in order (a) through (e)
    - Verifies: actions_performed in sequence 1-5; hero death before clearing

15. **test_illegal_action_reverses_game_state**
    - Tests: Rule 1.10.3 - Illegal action reverses game state
    - Verifies: state_restored = True after reversal

16. **test_mid_action_illegality_reverses_game_state**
    - Tests: Rule 1.10.3 - Mid-completion illegality reverses entire action
    - Verifies: state_restored = True even for partially-completed actions

17. **test_triggered_effects_suppressed_during_reversal**
    - Tests: Rule 1.10.3a - No triggered effects fire during reversal
    - Verifies: triggered_effects_fired == 0

18. **test_replacement_effects_suppressed_during_reversal**
    - Tests: Rule 1.10.3b - Replacement effects cannot modify reversal events
    - Verifies: replacement_effects_applied == 0

19. **test_partial_reversal_when_full_reversal_impossible**
    - Tests: Rule 1.10.3c - Partial reversal when full reversal impossible
    - Verifies: reversal_was_partial = True, game continues from last legal state

20. **test_unplayable_card_play_reversed**
    - Tests: Rule 1.10.3 - Playing unplayable card reversed
    - Verifies: play_was_illegal = True, card returns to starting zone

21. **test_cost_payment_with_illegal_play_reversed**
    - Tests: Rule 1.10.3 - Full action reversal including cost payment
    - Verifies: cost_restored = True, player resources restored

#### Engine Features Needed:
- `GameState` class representing a discrete moment (Rule 1.10.1)
- `GameState.is_priority_state` property (Rule 1.10.1)
- `GameEngine.has_priority_player()` method (Rule 1.10.1)
- `GameEngine.get_priority_player()` method (Rule 1.10.1)
- `GameStateAction` system executing actions (a)-(e) in order (Rule 1.10.2)
- `GameStateAction.check_hero_deaths()` → player loss / draw detection (Rule 1.10.2a)
- `GameStateAction.clear_zero_life_permanents()` as simultaneous single event (Rule 1.10.2b)
- `GameStateAction.start_look_effects()` for continuous look effects (Rule 1.10.2c)
- `GameStateAction.fire_state_based_triggers()` with clockwise ordering (Rule 1.10.2d)
- `GameStateAction.check_combat_chain_closing()` → initiate Close Step (Rule 1.10.2e)
- `GameEngine.reverse_illegal_action()` method (Rule 1.10.3)
- `ReversalResult` with `state_restored`, `reversal_was_partial` (Rule 1.10.3)
- Triggered effect suppression during reversal (Rule 1.10.3a)
- Replacement effect suppression during reversal (Rule 1.10.3b)
- `ContinuousLookEffect` class with location-based activation (Rule 1.10.2c)
- Clockwise ordering for multiple triggered layer placement (Rule 1.10.2d)

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
- [x] 1.4: Attacks
- [x] 1.5: Macros
- [x] 1.6: Layers
- [x] 1.7: Abilities
- [x] 1.8: Effects
- [x] 1.9: Events
- [x] 1.10: Game State
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
