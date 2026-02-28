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

### Section 2.3: Defense

**File**: `features/section_2_3_defense.feature`
**Step Definitions**: `step_defs/test_section_2_3_defense.py`

This section tests the defense property of cards in Flesh and Blood:
- **Rule 2.3.1**: Defense is a numeric property representing the value contributed to the total sum of defense in the damage step of combat
- **Rule 2.3.2**: Printed defense defines the base defense; no printed defense = no defense property; 0 is valid
- **Rule 2.3.2a**: (c) defense is defined by an ability; evaluates to 0 when undetermined
- **Rule 2.3.3**: Defense can be modified; "defense" or {d} symbol refers to the modified defense

#### Test Scenarios:

1. **test_defense_is_numeric_property**
   - Tests: Rule 2.3.1/2.3.2 - Defense is a numeric property
   - Verifies: Card has defense property with numeric value

2. **test_defense_value_used_in_damage_step**
   - Tests: Rule 2.3.1 - Defense contributes to combat damage step
   - Verifies: `defense_contribution` equals the printed defense value

3. **test_printed_defense_defines_base_defense**
   - Tests: Rule 2.3.2 - Printed defense defines base defense
   - Verifies: `base_defense` equals printed defense value

4. **test_zero_is_valid_printed_defense**
   - Tests: Rule 2.3.2 - Zero is a valid printed defense
   - Verifies: Card with defense 0 still has the defense property

5. **test_card_without_printed_defense_lacks_property**
   - Tests: Rule 2.3.2 - No printed defense means no defense property
   - Verifies: `has_defense_property = False` for cards without printed defense

6. **test_ability_defined_defense**
   - Tests: Rule 2.3.2a - (c) defense defined by ability
   - Verifies: Ability-defined defense value is correctly returned

7. **test_ability_defined_defense_zero_when_undetermined**
   - Tests: Rule 2.3.2a - Undetermined (c) defense evaluates to 0
   - Verifies: Defense evaluates to 0 when ability value cannot be determined

8. **test_defense_can_be_modified**
   - Tests: Rule 2.3.3 - Defense can be modified by effects
   - Verifies: Effect boosting defense increases effective_defense

9. **test_defense_term_refers_to_modified_defense**
   - Tests: Rule 2.3.3 - "defense" refers to modified defense
   - Verifies: Modified defense differs from base after boost effect

10. **test_d_symbol_refers_to_modified_defense**
    - Tests: Rule 2.3.3 - {d} symbol refers to modified defense
    - Verifies: {d} symbol resolves to modified (effective) defense

11. **test_defense_can_be_decreased**
    - Tests: Rule 2.3.3 - Defense can be decreased by effects
    - Verifies: Reduction effect decreases effective_defense

12. **test_defense_cannot_be_negative**
    - Tests: Rule 2.0.3c cross-ref - Defense capped at zero
    - Verifies: Defense reduced below zero becomes 0

13. **test_multiple_cards_independent_defense**
    - Tests: Rule 2.3.2 - Each card has its own defense
    - Verifies: Two cards maintain their own independent defense values

#### Implementation Notes:
- All 13 tests pass with stub-based implementation (`DefenseCardStub`, `AbilityDefinedDefenseCardStub`, `DefenseCheckResultStub`)
- `DefenseCardStub.effective_defense` caps at zero (cross-ref Rule 2.0.3c)
- `AbilityDefinedDefenseCardStub.base_defense` returns 0 when `ability_defined_value is None` (Rule 2.3.2a)

#### Engine Features Needed:
- `CardInstance.has_defense_property` property: False when no printed defense (Rule 2.3.2)
- `CardInstance.base_defense` property returning the unmodified printed defense (Rule 2.3.2)
- `CardInstance.effective_defense` returning modified defense (Rule 2.3.3)
- `CardInstance.defense_contribution` used in damage step calculations (Rule 2.3.1)
- Defense modification effects (Rule 2.3.3)
- Numeric defense capped at zero (cross-ref Rule 2.0.3c)
- Ability-defined defense for (c) notation cards (Rule 2.3.2a)
- Undefined (c) defense evaluates to 0 (Rule 2.3.2a)

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

### Section 1.11: Priority

**File**: `features/section_1_11_priority.feature`
**Step Definitions**: `step_defs/test_section_1_11_priority.py`

This section tests the priority system in Flesh and Blood:
- **Rule 1.11.1**: Priority describes which player may play a card, activate an ability, or pass priority
- **Rule 1.11.2**: Only one player can have priority at a time; that player is the "active player"
- **Rule 1.11.3**: Priority only exists during the Action Phase (not during the Close Step); turn player gains priority at phase start, during combat steps, and after layer resolution
- **Rule 1.11.4**: Active player may pass priority to the next player ("pass")
- **Rule 1.11.4a**: Priority passes clockwise; all-pass with non-empty stack resolves top layer; all-pass with empty stack ends the phase/step
- **Rule 1.11.5**: Active player regains priority after playing a card or activating an ability; loses priority after passing; no priority during card play, ability activation, layer resolution, game processes, or game state actions

#### Test Scenarios:

1. **test_priority_is_game_state_concept**
   - Tests: Rule 1.11.1 - Priority describes which player may act
   - Verifies: Priority tracking records who may play cards, activate abilities, or pass

2. **test_only_one_player_has_priority**
   - Tests: Rule 1.11.2 - Only one player can have priority at a time
   - Verifies: Exactly one player holds priority in the action phase

3. **test_player_with_priority_is_active_player**
   - Tests: Rule 1.11.2 - Player with priority is the "active player"
   - Verifies: Priority holder is active player; others are inactive players

4. **test_priority_only_in_action_phase**
   - Tests: Rule 1.11.3 - Priority only exists during Action Phase
   - Verifies: No player has priority during the start phase

5. **test_turn_player_gains_priority_at_action_phase_start**
   - Tests: Rule 1.11.3 - Turn player gains priority at start of action phase
   - Verifies: priority_player_id == turn_player_id when action phase begins

6. **test_no_priority_during_close_step**
   - Tests: Rule 1.11.3 - No priority during the Close Step of combat
   - Verifies: priority_player_id is None when Close Step begins

7. **test_turn_player_gains_priority_during_combat_steps**
   - Tests: Rule 1.11.3 - Turn player gains priority during combat steps (except Close Step)
   - Verifies: priority_player_id == turn_player_id at attack step

8. **test_turn_player_gains_priority_after_layer_resolution**
   - Tests: Rule 1.11.3 - Turn player gains priority after layer resolves
   - Verifies: priority_player_id == turn_player_id after top layer resolves

9. **test_active_player_may_pass_priority**
   - Tests: Rule 1.11.4 - Active player may pass priority
   - Verifies: After passing, active player no longer holds priority; next clockwise player does

10. **test_priority_passes_clockwise**
    - Tests: Rule 1.11.4a - Priority passes to next player in clockwise order
    - Verifies: In 3-player game, player 0 passing gives priority to player 1

11. **test_priority_passes_clockwise_wrap**
    - Tests: Rule 1.11.4a - Clockwise order wraps from last to first
    - Verifies: Player 2 passing in 3-player game gives priority to player 0

12. **test_all_pass_non_empty_stack_resolves**
    - Tests: Rule 1.11.4a - All players passing with non-empty stack resolves top layer
    - Verifies: all_players_passed = True and stack was non-empty triggers resolution

13. **test_all_pass_empty_stack_ends_phase**
    - Tests: Rule 1.11.4a - All players passing with empty stack ends phase or step
    - Verifies: all_players_passed = True and stack empty triggers phase/step end

14. **test_active_player_regains_priority_after_card_play**
    - Tests: Rule 1.11.5 - Active player regains priority after playing a card
    - Verifies: priority_player_id == turn_player_id after card is played

15. **test_active_player_regains_priority_after_ability**
    - Tests: Rule 1.11.5 - Active player regains priority after activating an ability
    - Verifies: priority_player_id == turn_player_id after ability is activated

16. **test_active_player_loses_priority_after_passing**
    - Tests: Rule 1.11.5 - Active player loses priority after passing
    - Verifies: priority_player_id != turn_player_id after passing

17. **test_no_priority_during_card_play**
    - Tests: Rule 1.11.5 - No player has priority while a card is being played
    - Verifies: priority_player_id is None during card play process

18. **test_no_priority_during_layer_resolution**
    - Tests: Rule 1.11.5 - No player has priority while a layer is resolving
    - Verifies: priority_player_id is None during layer resolution

19. **test_no_priority_during_game_state_actions**
    - Tests: Rule 1.11.5 - No player has priority during game state actions
    - Verifies: priority_player_id is None during game state actions

#### Engine Features Needed:
- `PriorityState` class tracking which player has priority (Rule 1.11.1)
- `PriorityState.active_player_id` (Rule 1.11.2)
- `GamePhase` enum with `ACTION_PHASE`, `START_PHASE`, `END_PHASE` (Rule 1.11.3)
- `GameEngine.get_priority_player_id()` (Rule 1.11.2)
- `GameEngine.current_phase` property (Rule 1.11.3)
- `GameEngine.grant_priority_to_turn_player()` (Rule 1.11.3)
- `CombatStep` enum including `CLOSE_STEP` (Rule 1.11.3)
- `GameEngine.current_combat_step` property (Rule 1.11.3)
- `GameEngine.pass_priority(player_id)` -> `PriorityPassResult` (Rule 1.11.4)
- `PriorityPassResult.next_priority_holder_id` (Rule 1.11.4a)
- `GameEngine.all_players_passed()` -> bool (Rule 1.11.4a)
- `GameEngine.resolve_top_of_stack()` called when all pass + non-empty stack (Rule 1.11.4a)
- `GameEngine.end_phase_or_step()` called when all pass + empty stack (Rule 1.11.4a)
- `GameEngine.play_card(card, player_id)` with priority regain (Rule 1.11.5)
- `GameEngine.activate_ability(source, player_id)` with priority regain (Rule 1.11.5)
- `GameEngine.is_in_process_of_playing_card` property (Rule 1.11.5)
- `GameEngine.is_in_process_of_resolving_layer` property (Rule 1.11.5)
- `GameEngine.is_performing_game_state_actions` property (Rule 1.11.5)

### Section 2.0: General (Object Properties)

**File**: `features/section_2_0_general.feature`
**Step Definitions**: `step_defs/test_section_2_0_general.py`

This section tests fundamental rules about object properties:
- **Rule 2.0.1**: A property is an attribute of an object; 13 properties defined: abilities, color, cost, defense, intellect, life, name, pitch, power, subtypes, supertypes, text_box, type
- **Rule 2.0.1a**: Abilities are properties (not objects); activated abilities have cost and type properties
- **Rule 2.0.2**: Card/macro properties determined by true text on cards.fabtcg.com
- **Rule 2.0.3**: Numeric properties have numeric values modifiable by effects/counters
- **Rule 2.0.3a**: Effects modify value not base value ("gain"/"get"/"have"/"lose" = non-base modification)
- **Rule 2.0.3b**: Base value modification is NOT gaining/losing; non-base modification IS gaining/losing (Korshem / Big Bully examples)
- **Rule 2.0.3c**: Numeric properties cannot be negative; capped at zero
- **Rule 2.0.3d**: +/-1 counters modify value not base value
- **Rule 2.0.4**: "Gaining" = didn't have property, now does; "Losing" = had property, no longer does; NOT same as increasing/decreasing value
- **Rule 2.0.5**: Source of a property is the object that has it

#### Test Scenarios:

1. **test_card_has_recognized_game_properties**
   - Tests: Rule 2.0.1 - Properties are attributes of objects
   - Verifies: Card has name, power, defense, cost, and type properties

2. **test_there_are_13_possible_object_properties**
   - Tests: Rule 2.0.1 - Exactly 13 properties defined
   - Verifies: Property system contains exactly the 13 defined property names

3. **test_ability_is_property_not_object**
   - Tests: Rule 2.0.1a - Abilities are properties, not objects
   - Verifies: "go again" is a property of the card, not a game object

4. **test_activated_ability_has_cost_and_type_properties**
   - Tests: Rule 2.0.1a - Activated abilities have cost and type properties
   - Verifies: ActivatedAbility has cost=2 and type property

5. **test_card_properties_come_from_card_definition**
   - Tests: Rule 2.0.2 - Properties from card definition
   - Verifies: Card power, cost, defense match defined values

6. **test_numeric_properties_have_numeric_values**
   - Tests: Rule 2.0.3 - Numeric properties return integers
   - Verifies: Power property value is 3 and classified as numeric

7. **test_effect_modifies_power_not_base**
   - Tests: Rule 2.0.3a - "+2 power" effect increases effective power, not base
   - Verifies: effective_power=6, base_power=4

8. **test_gain_effect_modifies_non_base_power**
   - Tests: Rule 2.0.3a - "gain 2 power" effect increases effective power, not base
   - Verifies: effective_power=5, base_power=3

9. **test_doubling_base_power_not_gaining**
   - Tests: Rule 2.0.3b - Doubling base power NOT classified as "gaining power" (Big Bully)
   - Verifies: base_power=8, modification.is_classified_as_gaining()=False

10. **test_non_base_increase_is_gaining**
    - Tests: Rule 2.0.3b - Non-base power increase IS classified as "gaining power" (Korshem)
    - Verifies: modification.is_classified_as_gaining()=True

11. **test_numeric_property_cannot_be_negative**
    - Tests: Rule 2.0.3c - Power capped at zero when reduced below zero
    - Verifies: effective_power=0 when base=2 and reduced by 5

12. **test_defense_cannot_be_negative**
    - Tests: Rule 2.0.3c - Defense capped at zero
    - Verifies: effective_defense=0 when base=1 and reduced by 3

13. **test_power_counter_modifies_not_base**
    - Tests: Rule 2.0.3d - +1 power counter increases effective power not base
    - Verifies: effective_power=5, base_power=4

14. **test_minus_power_counter_modifies_not_base**
    - Tests: Rule 2.0.3d - -1 power counter decreases effective power not base
    - Verifies: effective_power=3, base_power=4

15. **test_card_gains_new_property**
    - Tests: Rule 2.0.4 - Gaining a property = didn't have, now does
    - Verifies: was_gained=True after granting "go again"

16. **test_card_loses_existing_property**
    - Tests: Rule 2.0.4 - Losing a property = had it, no longer does
    - Verifies: was_lost=True after removing "go again"

17. **test_gaining_property_not_same_as_increasing_value**
    - Tests: Rule 2.0.4 - Gaining property NOT classified as increasing value
    - Verifies: gain_loss_result.is_value_increase=False

18. **test_source_of_property_is_card**
    - Tests: Rule 2.0.5 - Source of a property is the object that has it
    - Verifies: property_source.source_object_name == "Pummel"

#### Implementation Notes:
- All 18 tests pass with stub-based implementation (`CardPropertyStub`, `ActivatedAbilityStub`, etc.)
- `CardPropertyStub.ALL_PROPERTIES` enumerates the 13 defined property names
- `NumericPropertyModificationStub.is_classified_as_gaining()` implements Rule 2.0.3b logic
- `PropertyGainLossResultStub` tracks gain/loss vs value increase distinction (Rule 2.0.4)
- `PropertySourceStub` models Rule 2.0.5 property source tracking

#### Engine Features Needed:
- `ObjectProperty` system with enumeration of all 13 property types (Rule 2.0.1)
- `CardInstance.get_properties()` -> Set[str] (Rule 2.0.1)
- `CardInstance.has_property(name)` method (Rule 2.0.1)
- `ActivatedAbility.cost` and `ActivatedAbility.type` properties (Rule 2.0.1a)
- `CardInstance.base_power` distinct from `effective_power` (Rule 2.0.3a)
- `CardInstance.base_defense` distinct from `effective_defense` (Rule 2.0.3a)
- Effect tracking whether modification is "base" or "non-base" (Rules 2.0.3a, 2.0.3b)
- `PropertyModification.is_base_modification` flag (Rule 2.0.3b)
- Numeric properties capped at zero (Rule 2.0.3c)
- `CardInstance.gained_properties` tracking set (Rule 2.0.4)
- `CardInstance.lost_properties` tracking set (Rule 2.0.4)
- `PropertySource` system tracking which object a property belongs to (Rule 2.0.5)

### Section 2.1: Color

**File**: `features/section_2_1_color.feature`
**Step Definitions**: `step_defs/test_section_2_1_color.py`

This section tests the color property of cards in Flesh and Blood:
- **Rule 2.1.1**: Color is a visual representation of the color of a card
- **Rule 2.1.2**: The printed color is expressed as a color strip; red/yellow/blue strips give those colors; no strip = no color
- **Rule 2.1.2a**: Pitch and color are typically associated (pitch 1=red, 2=yellow, 3=blue) but are independent properties

#### Test Scenarios:

1. **test_color_is_visual_property**
   - Tests: Rule 2.1.1 - Color is a visual representation
   - Verifies: Card with color strip has `has_color = True` and `is_visual_property = True`

2. **test_card_with_red_color_strip_is_red**
   - Tests: Rule 2.1.2 - Red color strip makes card red
   - Verifies: Card's `color_name` is "red"

3. **test_card_with_yellow_color_strip_is_yellow**
   - Tests: Rule 2.1.2 - Yellow color strip makes card yellow
   - Verifies: Card's `color_name` is "yellow"

4. **test_card_with_blue_color_strip_is_blue**
   - Tests: Rule 2.1.2 - Blue color strip makes card blue
   - Verifies: Card's `color_name` is "blue"

5. **test_card_with_no_color_strip_has_no_color**
   - Tests: Rule 2.1.2 - No color strip = no color
   - Verifies: `has_color = False` and `color_name = None`

6. **test_card_pitch_1_typically_red**
   - Tests: Rule 2.1.2a - Pitch 1 typically associated with red
   - Verifies: Pitch 1 red card has both `color_name = "red"` and `pitch_value = 1`

7. **test_card_pitch_2_typically_yellow**
   - Tests: Rule 2.1.2a - Pitch 2 typically associated with yellow
   - Verifies: Pitch 2 yellow card has both `color_name = "yellow"` and `pitch_value = 2`

8. **test_card_pitch_3_typically_blue**
   - Tests: Rule 2.1.2a - Pitch 3 typically associated with blue
   - Verifies: Pitch 3 blue card has both `color_name = "blue"` and `pitch_value = 3`

9. **test_color_and_pitch_are_independent**
   - Tests: Rule 2.1.2a - Color and pitch are independent properties
   - Verifies: Red card with pitch 3 is valid; `are_independent = True`

10. **test_card_no_pitch_typically_no_color**
    - Tests: Rule 2.1.2a - Cards with no pitch typically have no color
    - Verifies: `has_color = False` and `has_pitch = False` for no-pitch no-color card

11. **test_card_no_pitch_can_have_color**
    - Tests: Rule 2.1.2a - Color and pitch are independent; a card can have a color without pitch
    - Verifies: Blue card with no pitch has `color_name = "blue"` and `has_pitch = False`

#### Implementation Notes:
- All 11 tests pass with stub-based implementation (`ColorCardStub`, `ColorCheckResultStub`, `ColorAndPitchCheckResultStub`)
- Tests document that the engine's `CardInstance` must expose color and pitch as independent, named properties
- `ColorCardStub.has_color` returns False when `color_name is None` (Rule 2.1.2)
- `ColorCardStub.has_pitch` returns False when `pitch_value is None` (Rule 2.1.2a)

#### Engine Features Needed:
- `CardInstance.color` property returning `Color` enum (Rule 2.1.1/2.1.2)
- `CardInstance.has_color` property: `False` when `Color.COLORLESS` (Rule 2.1.2)
- `CardInstance.color_name` property returning "red"/"yellow"/"blue"/None (Rule 2.1.2)
- `CardInstance.has_pitch` property (Rule 2.1.2a)
- `Color.COLORLESS` treated as "no color" not a valid color value (Rule 2.1.2)
- Color and pitch recognized as independent card properties (Rule 2.1.2a)

### Section 2.2: Cost

**File**: `features/section_2_2_cost.feature`
**Step Definitions**: `step_defs/test_section_2_2_cost.py`

This section tests the cost property of cards and abilities:
- **Rule 2.2.1**: Cost is a numeric property determining the starting resource asset-cost
- **Rule 2.2.2**: Printed cost defines base cost; no printed cost = no cost property; 0 is valid
- **Rule 2.2.2a**: Multiple undefined symbols/values (XX, X+1, etc.) are additive
- **Rule 2.2.3**: Activated ability cost = count of {r} symbols; no symbols = 0
- **Rule 2.2.4**: Cost property of an object cannot be modified
- **Rule 2.2.4a**: Effects modify play cost, NOT the cost property; only applied during playing
- **Rule 2.2.4b**: "Cost" effects use unmodified property; "payment" effects use modified cost
- **Rule 2.2.5**: {r} symbols and numeric cost expressions are functionally identical

#### Test Scenarios:

1. **test_cost_is_numeric_property_of_card**
   - Tests: Rule 2.2.1 - Cost is a numeric property
   - Verifies: Card with printed cost 3 has the cost property with value 3

2. **test_cost_determines_starting_resource_asset_cost**
   - Tests: Rule 2.2.1 - Cost determines starting resource asset-cost
   - Verifies: Starting resource asset-cost equals the cost property value

3. **test_printed_cost_defines_base_cost**
   - Tests: Rule 2.2.2 - Printed cost defines base cost
   - Verifies: Base cost equals printed cost value

4. **test_zero_is_valid_printed_cost**
   - Tests: Rule 2.2.2 - Zero is a valid printed cost
   - Verifies: Card with cost 0 still has the cost property

5. **test_card_without_printed_cost_lacks_cost_property**
   - Tests: Rule 2.2.2 - No printed cost = no cost property
   - Verifies: Card without printed cost has has_cost_property = False

6. **test_card_with_xx_has_additive_base_cost**
   - Tests: Rule 2.2.2a - Spark of Genius XX cost is additive
   - Verifies: XX with X=3 evaluates to 6 (additive)

7. **test_card_with_x_plus_1_has_additive_cost**
   - Tests: Rule 2.2.2a - Mixed X+1 cost is additive
   - Verifies: X+1 with X=2 evaluates to 3

8. **test_activated_ability_two_resource_symbols_base_cost_2**
   - Tests: Rule 2.2.3 - Two {r} symbols = base cost 2
   - Verifies: Activated ability base cost equals symbol count

9. **test_activated_ability_no_resource_symbols_base_cost_0**
   - Tests: Rule 2.2.3 - No resource symbols = base cost 0
   - Verifies: Activated ability with no {r} symbols has base cost 0

10. **test_resource_symbol_count_is_printed_cost**
    - Tests: Rule 2.2.3 - Symbol count dictates printed cost
    - Verifies: 3 resource symbols = printed cost 3

11. **test_cost_property_cannot_be_modified**
    - Tests: Rule 2.2.4 - Cost property is immutable
    - Verifies: Attempt to modify cost property fails; value stays unchanged

12. **test_cost_reduction_does_not_change_cost_property**
    - Tests: Rule 2.2.4a - Cost reduction only affects play cost
    - Verifies: Cost property stays 3 while effective play cost is 2

13. **test_cost_reduction_only_applies_during_playing**
    - Tests: Rule 2.2.4a - Modification only during playing process
    - Verifies: Effective play cost differs from cost property when reduction active

14. **test_effect_referring_to_cost_uses_unmodified_cost**
    - Tests: Rule 2.2.4b - "Cost" effects use unmodified property
    - Verifies: Effect sees cost value 3 (not 2 after reduction)

15. **test_effect_referring_to_payment_uses_modified_cost**
    - Tests: Rule 2.2.4b - "Payment" effects use modified cost at play time
    - Verifies: Payment record shows 2 (modified), base cost still 3

16. **test_resource_symbol_identical_to_numeric_cost**
    - Tests: Rule 2.2.5 - {r} and numeric are equivalent
    - Verifies: One {r} symbol equals numeric cost 1

17. **test_search_by_cost_finds_both_numeric_and_symbol_cards**
    - Tests: Rule 2.2.5 - Search by cost value finds both formats
    - Verifies: Cards with numeric cost 1 and {r}-symbol cost 1 both found

#### Implementation Notes:
- All 17 tests pass with stub-based implementation (`CostCardStub`, `AbilityCostStub`, etc.)
- `CostCardStub.cost` returns the unmodified printed cost (Rule 2.2.4b)
- `CostCardStub.effective_play_cost` applies reductions (Rule 2.2.4a)
- `CostCardStub.attempt_modify_cost_property()` always returns False (Rule 2.2.4)
- `VariableCostFormulaStub.evaluate_base_cost(x)` handles additive formulas (Rule 2.2.2a)

#### Engine Features Needed:
- `CardInstance.has_cost_property` property: False for no printed cost (Rule 2.2.2)
- `CardInstance.base_cost` property returning the unmodified printed cost (Rule 2.2.2)
- `CardInstance.cost` property returning the unmodified cost property (Rule 2.2.4b)
- `CardInstance.effective_play_cost` with modifications applied during play (Rule 2.2.4a)
- Variable cost formula support (XX, X+1, etc.) with additive evaluation (Rule 2.2.2a)
- `ActivatedAbility.base_cost` counting {r} symbols in description (Rule 2.2.3)
- `CostProperty.is_immutable = True` - cost property cannot be modified (Rule 2.2.4)
- Cost-reference effects use unmodified cost property (Rule 2.2.4b)
- Payment-reference effects use modified play cost at stack time (Rule 2.2.4b)
- {r} symbol count and numeric cost treated as functionally identical (Rule 2.2.5)

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

### Section 2.11: Supertypes

**File**: `features/section_2_11_supertypes.feature`
**Step Definitions**: `step_defs/test_section_2_11_supertypes.py`

This section tests the supertype property of objects in Flesh and Blood:
- **Rule 2.11.1**: Supertypes determine whether a card can be included in a player's card-pool
- **Rule 2.11.2**: An object can have zero or more supertypes
- **Rule 2.11.3**: Supertypes determined by type box; printed before card type
- **Rule 2.11.4**: Activated/triggered-layers inherit source supertypes
- **Rule 2.11.5**: Objects can gain or lose supertypes from rules/effects
- **Rule 2.11.6**: Supertypes are non-functional keywords; either a class or talent
- **Rule 2.11.6a**: Class supertypes: Adjudicator, Assassin, Bard, Brute, Guardian, Illusionist, Mechanologist, Merchant, Necromancer, Ninja, Pirate, Ranger, Runeblade, Shapeshifter, Thief, Warrior, Wizard (17 total)
- **Rule 2.11.6b**: Talent supertypes: Chaos, Draconic, Earth, Elemental, Ice, Light, Lightning, Mystic, Revered, Reviled, Royal, Shadow (12 total)

#### Test Scenarios:

1. **test_supertypes_determine_card_pool_inclusion**
   - Tests: Rule 2.11.1 - Supertypes determine card-pool inclusion
   - Verifies: Card with Warrior supertype is eligible for Warrior hero's card-pool

2. **test_non_matching_supertypes_prevent_card_pool_inclusion**
   - Tests: Rule 2.11.1 - Non-matching supertypes prevent inclusion
   - Verifies: Wizard card is NOT eligible for Warrior hero's card-pool

3. **test_card_with_zero_supertypes**
   - Tests: Rule 2.11.2 - Object can have zero supertypes
   - Verifies: Card with no supertypes has zero supertypes and is still a valid game object

4. **test_card_can_have_exactly_one_supertype**
   - Tests: Rule 2.11.2 - Object can have exactly one supertype
   - Verifies: Card has exactly 1 supertype and the correct supertype name

5. **test_card_can_have_multiple_supertypes**
   - Tests: Rule 2.11.2 - Object can have multiple supertypes
   - Verifies: Card with Warrior and Draconic has exactly 2 supertypes

6. **test_supertypes_determined_from_type_box**
   - Tests: Rule 2.11.3 - Supertypes come from type box
   - Verifies: "Warrior Action - Attack" yields Warrior supertype, Action type, Attack subtype

7. **test_supertypes_printed_before_card_type**
   - Tests: Rule 2.11.3 - Supertypes printed before card type
   - Verifies: Type box ordering shows supertypes before the card type

8. **test_activated_layer_inherits_supertypes**
   - Tests: Rule 2.11.4 - Activated-layer inherits source supertypes
   - Verifies: Activated-layer from Warrior source has Warrior supertype

9. **test_triggered_layer_inherits_supertypes**
   - Tests: Rule 2.11.4 - Triggered-layer inherits source supertypes
   - Verifies: Triggered-layer from Wizard/Shadow source has both supertypes

10. **test_layer_from_no_supertype_source**
    - Tests: Rule 2.11.4 - Layer from no-supertype source has no supertypes
    - Verifies: Zero supertypes inherited when source has none

11. **test_object_can_gain_supertype**
    - Tests: Rule 2.11.5 - Object can gain a supertype from an effect
    - Verifies: Card gains Warrior supertype via effect

12. **test_object_can_lose_supertype**
    - Tests: Rule 2.11.5 - Object can lose a supertype from an effect
    - Verifies: Draconic removed, Warrior retained

13. **test_supertypes_are_non_functional**
    - Tests: Rule 2.11.6 - Supertypes are non-functional keywords
    - Verifies: No additional rules added by supertypes; classified as non-functional

14. **test_warrior_is_class_supertype**
    - Tests: Rule 2.11.6/2.11.6a - Warrior is a class supertype keyword
    - Verifies: Supertype category is "class"

15. **test_draconic_is_talent_supertype**
    - Tests: Rule 2.11.6/2.11.6b - Draconic is a talent supertype keyword
    - Verifies: Supertype category is "talent"

16. **test_all_class_supertypes_recognized**
    - Tests: Rule 2.11.6a - All 17 class supertype keywords recognized
    - Verifies: All class keywords present; exactly 17 total

17. **test_all_talent_supertypes_recognized**
    - Tests: Rule 2.11.6b - All 12 talent supertype keywords recognized
    - Verifies: All talent keywords present; exactly 12 total

18. **test_generic_type_box_means_no_supertypes**
    - Tests: Rule 2.14.1a cross-ref - "Generic" means no supertypes
    - Verifies: "Generic Action" type box yields zero supertypes

19. **test_card_with_no_supertypes_in_any_card_pool**
    - Tests: Rule 2.11.1 - No-supertype card valid for any hero
    - Verifies: Empty supertype set is a subset of any hero's supertypes

20. **test_warrior_draconic_card_valid_for_warrior_draconic_hero**
    - Tests: Rule 2.11.1/2.11.2 - Multi-supertype subset validation
    - Verifies: Warrior/Draconic card is valid for Warrior/Draconic hero

21. **test_wizard_card_invalid_for_warrior_hero**
    - Tests: Rule 2.11.1 - Non-subset supertype card rejected
    - Verifies: Wizard card not eligible for Warrior-only hero

22. **test_multi_supertype_card_needs_all_match**
    - Tests: Rule 2.11.1 - All card supertypes must be subset of hero's
    - Verifies: Warrior/Draconic card NOT valid for Warrior-only hero

#### Implementation Notes:
- All 22 tests pass with stub-based test infrastructure (`TypeBoxParseResultStub211`, `SupertypeCheckResultStub211`, `LayerWithSupertypesStub211`)
- `TypeBoxParseResultStub211.parse()` implements type box parsing for rules tests (Rule 2.11.3)
- `check_card_pool_eligibility_by_supertypes()` implements subset validation (Rule 2.11.1)
- `get_supertype_category()` classifies supertypes as class or talent (Rule 2.11.6)
- `get_all_class_supertypes()` and `get_all_talent_supertypes()` return the definitive lists
- Regex-based step matchers (`parsers.re`) used for steps with multiple quoted parameters

#### Engine Features Needed:
- `CardTemplate.supertypes` returning frozenset of supertype keywords (Rule 2.11.2)
- `SupertypeRegistry.CLASS_SUPERTYPES` frozenset with all 17 class supertypes (Rule 2.11.6a)
- `SupertypeRegistry.TALENT_SUPERTYPES` frozenset with all 12 talent supertypes (Rule 2.11.6b)
- `SupertypeRegistry.get_category(name)` -> "class" | "talent" (Rule 2.11.6)
- `SupertypeRegistry.is_non_functional()` = True always (Rule 2.11.6)
- Type box parser extracting supertypes before card type (Rule 2.11.3)
- `Layer.supertypes` inheriting from source (Rule 2.11.4)
- `CardInstance.gain_supertype(name)` method (Rule 2.11.5)
- `CardInstance.lose_supertype(name)` method (Rule 2.11.5)
- Card-pool supertype subset validation (Rule 2.11.1)
- "Generic" type box means no supertypes (Rule 2.14.1a cross-ref)

### Section 2.6: Metatype

**File**: `features/section_2_6_metatype.feature`
**Step Definitions**: `step_defs/test_section_2_6_metatype.py`

This section tests the metatype property of objects in Flesh and Blood:
- **Rule 2.6.1**: Metatypes are metatype keywords that determine whether an object may be added to a game
- **Rule 2.6.2**: An object can have zero or more metatypes
- **Rule 2.6.3**: Metatype determined by type box; printed before supertypes
- **Rule 2.6.4**: Activated/triggered-layers inherit the metatypes of their source
- **Rule 2.6.5**: Objects cannot gain or lose metatypes (immutable)
- **Rule 2.6.6**: Two categories: hero-metatypes (match hero moniker) and set-metatypes (defined by tournament rules)

#### Test Scenarios:

1. **test_metatypes_determine_game_entry_eligibility**
   - Tests: Rule 2.6.1 - Metatypes determine game-entry eligibility
   - Verifies: Card with matching hero-metatype is eligible for that hero's deck

2. **test_non_matching_hero_metatype_cannot_be_added**
   - Tests: Rule 2.6.1/2.6.6 - Non-matching hero-metatype rejected
   - Verifies: Card with Dorinthea metatype rejected for Katsu hero

3. **test_card_with_no_metatypes_has_zero_metatypes**
   - Tests: Rule 2.6.2 - Objects can have zero metatypes
   - Verifies: Generic action card has empty metatypes list

4. **test_card_can_have_exactly_one_metatype**
   - Tests: Rule 2.6.2 - Objects can have one metatype
   - Verifies: Dorinthea Specialization Spell has exactly one metatype

5. **test_card_can_have_multiple_metatypes**
   - Tests: Rule 2.6.2 - Objects can have multiple metatypes
   - Verifies: Card with Dorinthea and Bravo metatypes has two metatypes

6. **test_metatype_determined_by_type_box**
   - Tests: Rule 2.6.3 - Metatype determined by type box
   - Verifies: Metatype value matches what's in the type box

7. **test_metatype_printed_before_supertypes**
   - Tests: Rule 2.6.3 - Metatype printed before supertypes
   - Verifies: Metatype precedes supertypes in type box ordering

8. **test_activated_layer_inherits_source_metatypes**
   - Tests: Rule 2.6.4 - Activated-layer inherits source metatypes
   - Verifies: Layer has same metatypes as creating card

9. **test_triggered_layer_inherits_source_metatypes**
   - Tests: Rule 2.6.4 - Triggered-layer inherits source metatypes
   - Verifies: Triggered-layer has same metatypes as source

10. **test_layer_from_no_metatype_source_has_no_metatypes**
    - Tests: Rule 2.6.4 - Layer from no-metatype source has no metatypes
    - Verifies: Zero metatypes inherited when source has none

11. **test_object_cannot_gain_metatypes**
    - Tests: Rule 2.6.5 - Objects cannot gain metatypes
    - Verifies: Effect attempting to add metatype fails; count unchanged

12. **test_object_cannot_lose_metatypes**
    - Tests: Rule 2.6.5 - Objects cannot lose metatypes
    - Verifies: Effect attempting to remove metatype fails; original metatype retained

13. **test_hero_metatype_legal_for_matching_moniker**
    - Tests: Rule 2.6.6 - Hero-metatype legal for matching moniker
    - Verifies: Bravo Signature Weapon legal for Bravo, Showstopper hero

14. **test_hero_metatype_illegal_for_non_matching_moniker**
    - Tests: Rule 2.6.6 - Hero-metatype illegal for non-matching moniker
    - Verifies: Bravo Signature Weapon rejected for Dorinthea Ironsong hero

15. **test_set_metatype_requires_matching_tournament_rule**
    - Tests: Rule 2.6.6 - Set-metatype card requires matching tournament rule
    - Verifies: Classic Constructed card allowed when tournament rule permits it

16. **test_set_metatype_rejected_without_matching_tournament_rule**
    - Tests: Rule 2.6.6 - Set-metatype card rejected without matching tournament rule
    - Verifies: Classic Constructed card rejected when no matching tournament rule

17. **test_card_with_no_metatypes_always_eligible**
    - Tests: Rule 2.6.1/2.6.2 - No-metatype card always eligible
    - Verifies: Card with no metatypes is not excluded by metatype restrictions for any hero

#### Implementation Notes:
- All 17 tests pass with stub-based implementation (`MetatypeStub`, `MetatypeCardStub`, `HeroCardStub`, `LayerWithMetatypeStub`, etc.)
- `MetatypeCardStub.gain_metatype()` always returns False (Rule 2.6.5 immutability)
- `MetatypeCardStub.lose_metatype()` always returns False (Rule 2.6.5 immutability)
- `LayerWithMetatypeStub.metatypes` delegates to `source.metatypes` (Rule 2.6.4)
- `check_card_pool_legality()` validates hero-metatypes by moniker and set-metatypes by tournament rule

#### Engine Features Needed:
- `CardTemplate.metatypes` property: frozenset of metatype keywords (Rule 2.6.1)
- `MetatypeKeyword` class variants: `HeroMetatype` and `SetMetatype` (Rule 2.6.6)
- `CardTemplate.has_metatype(keyword)` method (Rules 2.6.2, 2.6.3)
- `Layer.metatypes` property inheriting from source (Rule 2.6.4)
- `CardTemplate.metatypes` is immutable - no gain/lose operations (Rule 2.6.5)
- `HeroCard.moniker` property extracted from name (Rule 2.6.6, cross-ref 2.7.3)
- `card_pool_legality_check(card, hero)` validating metatype matching (Rule 2.6.6)
- `TournamentRule.allowed_sets` for set-metatype validation (Rule 2.6.6)

### Section 2.4: Intellect

**File**: `features/section_2_4_intellect.feature`
**Step Definitions**: `step_defs/test_section_2_4_intellect.py`

This section tests the intellect property of hero cards in Flesh and Blood:
- **Rule 2.4.1**: Intellect is a numeric property of a hero card; represents the number of cards drawn up to at end of turn
- **Rule 2.4.2**: Printed intellect defines the base intellect; no printed intellect = no property (0 is valid)
- **Rule 2.4.3**: Intellect can be modified; "intellect" or {i} refers to the modified intellect

#### Test Scenarios:

1. **test_intellect_is_numeric_property**
   - Tests: Rule 2.4.1/2.4.2 - Intellect is a numeric property
   - Verifies: Hero card has intellect property with numeric value

2. **test_intellect_represents_cards_drawn_at_end_of_turn**
   - Tests: Rule 2.4.1 - Intellect is used for end-of-turn draw
   - Verifies: Player draws up to intellect-value cards at end of turn

3. **test_intellect_is_hero_card_property_only**
   - Tests: Rule 2.4.1 - Intellect is exclusively a hero card property
   - Verifies: Hero card has intellect property; non-hero action card does not

4. **test_printed_intellect_defines_base_intellect**
   - Tests: Rule 2.4.2 - Printed intellect defines base intellect
   - Verifies: `base_intellect` equals printed intellect value

5. **test_zero_is_valid_printed_intellect**
   - Tests: Rule 2.4.2 - Zero is a valid printed intellect
   - Verifies: Hero with 0 printed intellect still has the intellect property

6. **test_card_without_printed_intellect_lacks_property**
   - Tests: Rule 2.4.2 - No printed intellect means no intellect property
   - Verifies: `has_intellect_property = False` for cards without printed intellect

7. **test_intellect_can_be_modified**
   - Tests: Rule 2.4.3 - Intellect can be modified by effects
   - Verifies: Effect boosting intellect increases `effective_intellect`

8. **test_intellect_term_refers_to_modified_intellect**
   - Tests: Rule 2.4.3 - "intellect" refers to modified intellect
   - Verifies: Modified intellect differs from base after boost effect

9. **test_i_symbol_refers_to_modified_intellect**
   - Tests: Rule 2.4.3 - {i} symbol refers to modified intellect
   - Verifies: {i} symbol resolves to modified (effective) intellect

10. **test_intellect_can_be_decreased**
    - Tests: Rule 2.4.3 - Intellect can be decreased by effects
    - Verifies: Reduction effect decreases `effective_intellect`

11. **test_intellect_cannot_be_negative**
    - Tests: Rule 2.0.3c cross-ref - Intellect capped at zero
    - Verifies: Intellect reduced below zero becomes 0

12. **test_modified_intellect_affects_end_of_turn_draw**
    - Tests: Rule 2.4.1 + 2.4.3 - Modified intellect affects end-of-turn draw
    - Verifies: Boosted intellect results in drawing more cards at end of turn

13. **test_multiple_hero_cards_independent_intellect**
    - Tests: Rule 2.4.2 - Each hero card has its own intellect
    - Verifies: Two heroes maintain their own independent intellect values

#### Implementation Notes:
- All 13 tests pass with stub-based implementation (`IntellectCardStub`, `IntellectCheckResultStub`, `EndOfTurnDrawResultStub`)
- `IntellectCardStub.effective_intellect` caps at zero (cross-ref Rule 2.0.3c)
- `IntellectCardStub.has_intellect_property` returns False when `printed_intellect is None` (Rule 2.4.2)

#### Engine Features Needed:
- `CardInstance.has_intellect_property` property: False when no printed intellect (Rule 2.4.2)
- `CardInstance.base_intellect` property returning the unmodified printed intellect (Rule 2.4.2)
- `CardInstance.effective_intellect` (or `intellect`) returning modified intellect (Rule 2.4.3)
- Intellect restricted to hero card types (Rule 2.4.1)
- End-of-turn draw-up-to logic using effective intellect (Rule 2.4.1)
- Intellect modification effects (Rule 2.4.3)
- Numeric intellect capped at zero (cross-ref Rule 2.0.3c)

### Section 1.13: Assets

**File**: `features/section_1_13_assets.feature`
**Step Definitions**: `step_defs/test_section_1_13_assets.py`

This section tests the four types of assets in Flesh and Blood:
- **Rule 1.13.1**: Assets are points of a given type owned by a player; four types exist
- **Rule 1.13.2**: Action points are used to play action cards and activate action abilities
- **Rule 1.13.2a**: Action points can be gained from action phase start, go again ability, and effects
- **Rule 1.13.2b**: A player cannot gain action points if it is not their action phase
- **Rule 1.13.3**: Resource points are used to play cards and activate abilities
- **Rule 1.13.3a**: Resource points are gained from pitching cards and effects
- **Rule 1.13.4**: Life points come from the hero's life total and activate abilities
- **Rule 1.13.4a**: Life points are gained from effects that increase hero's life total
- **Rule 1.13.5**: Chi points are used to play cards and activate abilities
- **Rule 1.13.5a**: Chi points are gained from pitching chi cards during cost payment
- **Rule 1.13.5b**: Chi points can be used in place of resource points; chi spent before resource

#### Test Scenarios:

1. **test_there_are_exactly_four_asset_types**
   - Tests: Rule 1.13.1 - Exactly four asset types
   - Verifies: action_point, resource_point, life_point, chi_point are all valid

2. **test_asset_owned_by_player**
   - Tests: Rule 1.13.1 - Assets are owned by a specific player
   - Verifies: Player's action points belong only to that player

3. **test_action_points_used_to_play_action_cards**
   - Tests: Rule 1.13.2 - Action points spent when playing action cards
   - Verifies: Spending 1 action point reduces count from 1 to 0

4. **test_player_gains_action_point_at_action_phase_start**
   - Tests: Rule 1.13.2a - 1 action point granted at start of action phase
   - Verifies: Player starts action phase with 1 action point

5. **test_go_again_grants_action_point**
   - Tests: Rule 1.13.2a - Go again grants 1 additional action point
   - Verifies: Player has 2 action points after go again triggers during action phase

6. **test_effect_grants_action_points**
   - Tests: Rule 1.13.2a - Effects can grant action points
   - Verifies: Action point effect increases count by 1 during action phase

7. **test_non_turn_player_no_action_points_from_go_again**
   - Tests: Rule 1.13.2b - Go again blocked outside action phase
   - Verifies: Non-turn player gets 0 action points from go again (Lead the Charge example)

8. **test_non_turn_player_no_action_points_from_effects**
   - Tests: Rule 1.13.2b - Effect-based action point gain blocked outside action phase
   - Verifies: Effect grants 0 action points when player is not in action phase

9. **test_lead_the_charge_no_action_points_outside_phase**
   - Tests: Rule 1.13.2b - Lead the Charge example from the rules
   - Verifies: Delayed trigger from Lead the Charge doesn't grant action points to non-turn player

10. **test_resource_points_used_to_pay_card_costs**
    - Tests: Rule 1.13.3 - Resource points spent to pay card costs
    - Verifies: Spending 3 resource points reduces count from 3 to 0

11. **test_player_gains_resource_points_from_pitch**
    - Tests: Rule 1.13.3a - Pitching generates resource points
    - Verifies: Pitching a 2-pitch card grants 2 resource points

12. **test_effect_grants_resource_points**
    - Tests: Rule 1.13.3a - Effects directly grant resource points
    - Verifies: Effect grants 2 resource points to player

13. **test_life_points_come_from_hero_life_total**
    - Tests: Rule 1.13.4 - Life points are tied to hero's life total
    - Verifies: Player's life points equal hero's life total

14. **test_life_points_activate_abilities**
    - Tests: Rule 1.13.4 - Life points spent to activate abilities
    - Verifies: Paying 2 life reduces hero's life from 20 to 18

15. **test_player_gains_life_points_from_effect**
    - Tests: Rule 1.13.4a - Effects can increase hero life total (gain life points)
    - Verifies: Effect grants 3 life points, increasing hero from 15 to 18

16. **test_chi_points_used_to_play_cards**
    - Tests: Rule 1.13.5 - Chi points spent to pay costs
    - Verifies: Spending 2 chi points reduces count from 2 to 0

17. **test_player_gains_chi_points_from_chi_pitch**
    - Tests: Rule 1.13.5a - Pitching chi cards generates chi points
    - Verifies: Pitching a 1-chi card grants 1 chi point

18. **test_chi_point_substitutes_for_resource_point**
    - Tests: Rule 1.13.5b - Chi substitutes for resource in payment
    - Verifies: 2 chi points successfully pay a resource cost of 2

19. **test_chi_points_used_before_resource_points**
    - Tests: Rule 1.13.5b + 1.14.2a - Chi spent before resource in payment order
    - Verifies: With 1 resource + 2 chi, paying cost 2 uses 2 chi first; 1 resource remains

20. **test_chi_points_cannot_substitute_for_life_costs**
    - Tests: Rule 1.13.5b (limitation) - Chi cannot substitute for life point costs
    - Verifies: Attempt to use chi for life cost fails with "chi_cannot_substitute_for_life"

21. **test_pitching_resource_card_gains_resource_points**
    - Tests: Rule 1.13.3a - Resource-type pitch cards generate resource points
    - Verifies: Pitching a 3-pitch resource card grants 3 resource points

22. **test_pitching_chi_card_gains_chi_points**
    - Tests: Rule 1.13.5a - Chi-type pitch cards generate chi points
    - Verifies: Pitching a 2-pitch chi card grants 2 chi points

23. **test_cannot_pitch_wrong_asset_type_card**
    - Tests: Rule 1.14.3b - Pitch restricted to cards that gain needed asset type
    - Verifies: Cannot pitch resource card when chi points are needed

#### Implementation Notes:
- All asset tracking uses stub metadata (`_action_points`, `_resource_points`, etc.) on TestPlayer objects
- New stub classes added: `AssetSpendResultStub`, `ChiPaymentResultStub`, `LifeGainResultStub`, `LifeCostAbilityStub`
- New helper methods in `BDDGameState`: `get_asset_types`, `set_player_action_points`, `get_player_action_points`, `spend_player_action_point`, `begin_action_phase_for_player`, `trigger_go_again_for_player`, `grant_action_points_via_effect`, `simulate_instant_play_with_go_again`, `attempt_grant_action_points_outside_phase`, `register_lead_the_charge_trigger_for`, `simulate_cost_zero_action_play`, `set_player_resource_points`, `get_player_resource_points`, `pay_resource_cost`, `grant_resource_points_via_effect`, `create_card_with_pitch`, `pitch_card_for_resources`, `set_player_chi_points`, `get_player_chi_points`, `pay_chi_cost`, `pitch_card_for_chi`, `pay_resource_cost_with_chi`, `pay_resource_cost_with_available_assets`, `attempt_chi_for_life_payment`, `attempt_pitch_for_wrong_type`, `set_hero_life_total`, `get_hero_life_total`, `get_player_life_points`, `player_hero_has_life_tracking`, `create_ability_with_life_cost`, `activate_ability_with_life_cost`, `grant_life_points_via_effect`

#### Engine Features Needed:
- `PlayerAssets` class tracking `action_points`, `resource_points`, `life_points`, `chi_points` (Rule 1.13.1)
- `AssetType` enum with `ACTION_POINT`, `RESOURCE_POINT`, `LIFE_POINT`, `CHI_POINT` (Rule 1.13.1)
- `Player.assets` property returning `PlayerAssets` (Rule 1.13.1)
- `Player.gain_asset(asset_type, amount)` method (Rules 1.13.2a, 1.13.3a, 1.13.4a, 1.13.5a)
- `Player.spend_asset(asset_type, amount)` method (Rule 1.13.2)
- `GameEngine.begin_action_phase(player_id)` granting 1 action point (Rule 1.13.2a)
- `GoAgainEffect` granting 1 action point when trigger fires (Rule 1.13.2a)
- Action phase guard: `Player.can_gain_action_points() = False` outside action phase (Rule 1.13.2b)
- Chi points counted as resource points for resource payment (Rule 1.13.5b)
- Payment order: chi first, then resource, then life, then action (Rule 1.14.2a)
- `PitchEffect` generating assets based on card pitch type and value (Rules 1.13.3a, 1.13.5a)
- Pitch restriction: only pitch if card generates needed asset type (Rule 1.14.3b)

### Section 1.14: Costs

**File**: `features/section_1_14_costs.feature`
**Step Definitions**: `step_defs/test_section_1_14_costs.py`

This section tests the cost system for playing cards and activating abilities:
- **Rule 1.14.1**: Playing a card or activating an ability incurs a cost
- **Rule 1.14.2**: Asset-costs are paid by spending assets
- **Rule 1.14.2a**: Multi-asset costs paid in order: chi → resource → life → action
- **Rule 1.14.2b**: If a mandatory cost cannot be paid, the entire action is reversed
- **Rule 1.14.2c**: Chi point costs are paid using chi points
- **Rule 1.14.2d**: Resource point costs are paid using chi first, then resource points
- **Rule 1.14.2e**: Life point costs are paid using life points only
- **Rule 1.14.2f**: Action point costs are paid using action points
- **Rule 1.14.3**: Pitching a card moves it to the pitch zone and grants assets
- **Rule 1.14.3a**: Only cards with the pitch property can be pitched (unless effect instructs)
- **Rule 1.14.3b**: A card can only be pitched if it generates the needed asset type
- **Rule 1.14.3c**: Pitching is an event that can trigger and be replaced by effects
- **Rule 1.14.4**: Effect-costs require generating and resolving a specific effect
- **Rule 1.14.4a**: Player declares the order when paying multiple effect-costs
- **Rule 1.14.4b**: Unpayable effect-costs reverse game state to before activation
- **Rule 1.14.4c**: A replaced effect-cost still counts as paid
- **Rule 1.14.5**: Zero cost is still a cost that must be acknowledged

#### Test Scenarios:

1. **test_cost_incurred_by_playing_card**
   - Tests: Rule 1.14.1 - Playing a card incurs its cost
   - Verifies: Card play result confirms a cost was incurred

2. **test_cost_incurred_by_activating_ability**
   - Tests: Rule 1.14.1 - Activating an ability incurs its cost
   - Verifies: Ability activation result confirms a cost was incurred

3. **test_cost_can_require_both_asset_and_effect_components**
   - Tests: Rule 1.14.1 - Costs can have asset and effect components
   - Verifies: Full cost exposes both asset-cost and effect-cost components

4. **test_player_pays_asset_cost_with_exact_assets**
   - Tests: Rule 1.14.2 - Asset-cost paid with exact resources
   - Verifies: Cost paid, 0 resource points remaining

5. **test_player_pays_asset_cost_with_surplus_assets**
   - Tests: Rule 1.14.2 - Surplus resources remain after payment
   - Verifies: Cost paid, 2 resource points remaining from 4 with cost 2

6. **test_player_cannot_pay_asset_cost_with_insufficient_assets**
   - Tests: Rule 1.14.2b - Insufficient assets prevent payment
   - Verifies: Payment fails when 1 resource point cannot pay cost 3

7. **test_multi_asset_cost_paid_in_correct_order**
   - Tests: Rule 1.14.2a - Multi-asset payment order enforcement
   - Verifies: Chi paid first (order 1), resource second (2), life third (3), action last (4)

8. **test_each_asset_type_paid_in_full_before_next**
   - Tests: Rule 1.14.2a - Each asset type fully paid before next begins
   - Verifies: Chi payment fails first, resource payment does not start

9. **test_mandatory_asset_cost_failure_reverses_entire_action**
   - Tests: Rule 1.14.2b - Mandatory cost failure reverses entire action
   - Verifies: Entire action reversed, card returned to starting zone

10. **test_pitching_during_payment_provides_needed_assets**
    - Tests: Rule 1.14.2d - Pitching during payment supplements resources
    - Verifies: 1 + 2 = 3 resource points after pitching 2-pitch card

11. **test_paying_chi_cost_uses_chi_points**
    - Tests: Rule 1.14.2c - Chi costs paid from chi points
    - Verifies: 2 chi points spent, 1 chi remaining from 3

12. **test_player_pitches_chi_card_to_gain_chi_for_chi_cost**
    - Tests: Rule 1.14.2c - Chi gained by pitching chi cards
    - Verifies: 2 chi gained from pitching, chi cost paid successfully

13. **test_paying_resource_cost_uses_chi_first_then_resource**
    - Tests: Rule 1.14.2d - Chi used before resource for resource costs
    - Verifies: 1 chi spent, then 1 resource spent

14. **test_player_pitches_resource_card_during_resource_cost_payment**
    - Tests: Rule 1.14.2d - Pitching resource card during resource cost
    - Verifies: 2 resource points gained from pitch

15. **test_pitching_stops_when_resource_cost_paid**
    - Tests: Rule 1.14.2d - Pitching stops when cost fully paid
    - Verifies: Cost paid, 1 resource left over, no further pitching needed

16. **test_paying_life_cost_uses_life_points**
    - Tests: Rule 1.14.2e - Life costs use life points
    - Verifies: Life total decreases from 20 to 18 after paying 2 life

17. **test_life_cost_cannot_be_paid_with_chi_points**
    - Tests: Rule 1.14.2e - Chi cannot substitute for life costs
    - Verifies: Payment fails, game state not changed

18. **test_paying_action_cost_uses_action_points**
    - Tests: Rule 1.14.2f - Action costs use action points
    - Verifies: 1 action point spent, 0 remaining

19. **test_pitching_card_moves_to_pitch_zone_and_grants_assets**
    - Tests: Rule 1.14.3 - Pitching moves card and grants resources
    - Verifies: Card in pitch zone, 2 resource points gained

20. **test_pitch_property_determines_type_and_amount_of_assets**
    - Tests: Rule 1.14.3 - Pitch property determines assets granted
    - Verifies: 3-chi-pitch card grants 3 chi points

21. **test_card_without_pitch_property_cannot_be_pitched**
    - Tests: Rule 1.14.3a - No-pitch cards cannot be pitched normally
    - Verifies: Pitch attempt fails, card remains in hand

22. **test_card_with_pitch_property_can_be_pitched**
    - Tests: Rule 1.14.3a - Cards with pitch property can be pitched
    - Verifies: Pitch succeeds, card moves to pitch zone

23. **test_player_can_only_pitch_card_if_gains_needed_asset_type**
    - Tests: Rule 1.14.3b - Wrong asset type pitch rejected
    - Verifies: Resource-pitch card rejected when chi is needed

24. **test_player_can_pitch_card_if_gains_needed_asset_type**
    - Tests: Rule 1.14.3b - Correct asset type pitch accepted
    - Verifies: Chi-pitch card accepted when chi is needed

25. **test_player_can_pitch_card_if_instructed_by_effect**
    - Tests: Rule 1.14.3b - Effect instruction bypasses normal pitch restrictions
    - Verifies: No-pitch card accepted when effect instructs pitch

26. **test_pitching_card_triggers_pitch_watchers**
    - Tests: Rule 1.14.3c - Pitching is an event that triggers effects
    - Verifies: Pitch trigger fires when card is pitched

27. **test_pitching_card_can_be_replaced_by_replacement_effects**
    - Tests: Rule 1.14.3c - Pitch event can be replaced
    - Verifies: Replacement effect modifies the pitch event

28. **test_effect_cost_requires_generating_and_resolving_effect**
    - Tests: Rule 1.14.4 - Effect-cost requires generating the specified effect
    - Verifies: Destroy effect generated and target destroyed as cost

29. **test_hope_merchants_hood_effect_cost_example**
    - Tests: Rule 1.14.4 - Hope Merchant's Hood canonical example
    - Verifies: Destroying Hood is the effect-cost, hand shuffled as the ability

30. **test_player_declares_order_for_multi_effect_cost**
    - Tests: Rule 1.14.4a - Player declares order for multiple effect-costs
    - Verifies: Discard and damage effects generated in declared order

31. **test_effect_cost_that_cannot_be_generated_reverses_game_state**
    - Tests: Rule 1.14.4b - Unpayable effect-cost reverses to before activation
    - Verifies: Effect-cost fails, game state reversed

32. **test_mandatory_effect_cost_failure_reverses_entire_action**
    - Tests: Rule 1.14.4b - Mandatory effect-cost failure reverses entire action
    - Verifies: Entire card play action reversed when discard impossible

33. **test_effect_cost_replaced_but_considered_paid**
    - Tests: Rule 1.14.4c - Replaced effect-cost still counts as paid
    - Verifies: Discard replaced by banishment, cost still considered paid

34. **test_card_with_cost_zero_still_has_cost_to_pay**
    - Tests: Rule 1.14.5 - Zero cost is still a cost
    - Verifies: Zero-cost card has cost acknowledged and play proceeds

35. **test_asset_costs_reduced_to_zero_still_require_acknowledgment**
    - Tests: Rule 1.14.5 - Reduced-to-zero cost still acknowledged
    - Verifies: Cost reduced from 3 to 0, zero cost acknowledged

36. **test_zero_cost_with_no_effect_costs_is_still_a_cost**
    - Tests: Rule 1.14.5 - Zero cost with no effect-costs still valid
    - Verifies: Zero cost acknowledged as paid via acknowledgment

#### Implementation Notes:
- New stub classes: `MultiAssetAbilityStub`, `EffectCostAbilityStub`, `TwoEffectCostAbilityStub`, `PitchInstructionEffectStub`, `PitchTriggerEffectStub`, `PitchReplacementEffectStub`, `GeneralReplacementEffectStub`, `CostReductionEffectStub`, `AssetPaymentResultStub`, `MultiAssetPaymentResultStub`, `CardPlayResultStub`, `AbilityActivationResultStub`, `FullCostStub`, `PitchPaymentResultStub`, `PitchAttemptResultStub`, `ChiCostPaymentResultStub`, `ResourceCostPaymentResultStub`, `LifeCostPaymentResultStub`, `ActionCostPaymentResultStub`, `EffectCostPaymentResultStub`, `HoodActivationResultStub`, `MultiEffectCostResultStub`
- New helper methods: `create_card_with_resource_cost`, `create_chi_pitch_card`, `create_multi_asset_ability`, `create_ability_with_chi_cost`, `create_ability_with_action_cost`, `create_ability_with_effect_cost`, `create_ability_with_two_effect_costs`, `create_pitch_instruction_effect`, `create_pitch_trigger_effect`, `create_pitch_replacement_effect`, `create_replacement_effect`, `create_cost_reduction_effect`, `attempt_card_play_1_14`, `attempt_ability_activation_1_14`, `get_full_cost_1_14`, `pay_asset_cost_1_14`, `attempt_pay_asset_cost_1_14`, `pay_multi_asset_cost_1_14`, `attempt_pay_multi_asset_cost_1_14`, `pitch_card_during_payment_1_14`, `pay_chi_cost_1_14`, `pay_resource_cost_tracked_1_14`, `pay_life_cost_1_14`, `pay_action_cost_1_14`, `attempt_pitch_card_1_14`, `pitch_card_via_effect_instruction_1_14`, `pitch_card_with_trigger_check_1_14`, `count_pitch_triggers_fired_1_14`, `pitch_card_with_replacement_check_1_14`, `pay_effect_cost_1_14`, `activate_ability_with_effect_cost_1_14`, `pay_multi_effect_cost_1_14`, `attempt_pay_effect_cost_1_14`, `play_card_with_cost_reduction_1_14`, `attempt_pitch_another_card_1_14`
- `pitch_card_for_chi` and `pitch_card_for_resources` updated to return `PitchPaymentResultStub` instead of `AssetSpendResultStub`
- `attempt_pitch_for_wrong_type` updated to return `PitchAttemptResultStub` with `_pitch_rejected`/`_pitch_succeeded`

#### Engine Features Needed:
- `Cost` class hierarchy: `AssetCost`, `EffectCost` (Rule 1.14.1)
- `Cost.cost_type` attribute (`"asset_cost"` or `"effect_cost"`) (Rule 1.14.1)
- `AssetCost.pay(player)` subtracting assets and returning success (Rule 1.14.2)
- `AssetCost.can_be_paid(player)` check (Rule 1.14.2b)
- Multi-asset payment order enforcement: chi → resource → life → action (Rule 1.14.2a)
- `GameEngine.reverse_illegal_action()` when mandatory cost cannot be paid (Rules 1.14.2b, 1.10.3)
- `AssetCost.pay_chi_cost(player, amount)` (Rule 1.14.2c)
- `AssetCost.pay_resource_cost(player, amount)` - chi before resource (Rule 1.14.2d)
- `AssetCost.pay_life_cost(player, amount)` (Rule 1.14.2e)
- `AssetCost.pay_action_cost(player, amount)` (Rule 1.14.2f)
- `PitchAction.execute(player, card)` moving hand → pitch zone (Rule 1.14.3)
- `CardTemplate.has_pitch` property (Rule 1.14.3a)
- `PitchAction.validate(player, card, needed_asset_type)` (Rule 1.14.3b)
- `PitchEvent` that can trigger and be replaced by effects (Rule 1.14.3c)
- `EffectCost.pay(player)` generating and resolving the specified effects (Rule 1.14.4)
- `EffectCost.can_be_paid(player)` check before payment (Rule 1.14.4b)
- `EffectCost` with multiple effects: player declares order (Rule 1.14.4a)
- `EffectCost.replaced_event_still_counts_as_paid = True` (Rule 1.14.4c)
- Zero cost acknowledgment system (Rule 1.14.5)

### Section 1.15: Counters

**File**: `features/section_1_15_counters.feature`
**Step Definitions**: `step_defs/test_section_1_15_counters.py`

This section tests the counter system in Flesh and Blood:
- **Rule 1.15.1**: A counter is a physical marker on a public object; not an object; identity by name or value+symbol
- **Rule 1.15.2**: Counters modify properties and/or interact with effects
- **Rule 1.15.2a**: Numeric+symbol counters modify object properties as a rule (not an effect), at the same timing layer as continuous effects
- **Rule 1.15.3**: Counters cease when the object ceases or when removed
- **Rule 1.15.4**: Diametrically opposing counters both remain on the object (no cancellation)

#### Test Scenarios:

1. **test_counter_is_physical_marker_on_object**
   - Tests: Rule 1.15.1 - Counter is a physical marker
   - Verifies: Counter recognized as physical marker on card

2. **test_counter_is_not_object_and_has_no_properties**
   - Tests: Rule 1.15.1 - Counter is not a game object
   - Verifies: `is_game_object = False`, `has_object_properties = False`

3. **test_counter_identity_defined_by_name**
   - Tests: Rule 1.15.1 - Named counter identity
   - Verifies: Two "steam" counters are functionally identical

4. **test_counter_identity_defined_by_value_and_symbol**
   - Tests: Rule 1.15.1 - Value+symbol counter identity
   - Verifies: Two "+1{d}" counters are functionally identical and interchangeable

5. **test_counters_with_same_name_are_interchangeable**
   - Tests: Rule 1.15.1 - Same-name counters are interchangeable
   - Verifies: `counters_are_interchangeable()` returns True for same-name counters

6. **test_counters_with_different_names_are_not_same**
   - Tests: Rule 1.15.1 - Different-named counters have different identities
   - Verifies: "steam" and "rust" counters have different identities

7. **test_counter_on_object_modifies_properties**
   - Tests: Rule 1.15.2 - Counter modifies object properties
   - Verifies: "+1{d}" counter increases effective defense from 3 to 4

8. **test_counter_on_object_can_interact_with_effects**
   - Tests: Rule 1.15.2 - Counter interacts with effects
   - Verifies: Counter watcher effect detects "steam" counter on card

9. **test_plus_power_counter_increases_attack_power**
   - Tests: Rule 1.15.2a - +{p} counter increases power
   - Verifies: "+1{p}" counter increases effective power from 4 to 5

10. **test_minus_power_counter_decreases_attack_power**
    - Tests: Rule 1.15.2a - -{p} counter decreases power
    - Verifies: "-1{p}" counter decreases effective power from 4 to 3

11. **test_plus_defense_counter_increases_defense_value**
    - Tests: Rule 1.15.2a - +{d} counter increases defense
    - Verifies: "+2{d}" counter increases effective defense from 3 to 5

12. **test_counter_modification_is_rule_not_effect**
    - Tests: Rule 1.15.2a - Counter modification classified as rule
    - Verifies: Modification type is "rule", not "effect"

13. **test_counter_modification_applies_at_same_time_as_continuous_effects**
    - Tests: Rule 1.15.2a - Counter and continuous effect timing
    - Verifies: Both apply at same timing layer; total power = base + counter + effect

14. **test_multiple_counters_stack_modifications**
    - Tests: Rule 1.15.2a - Multiple counters stack
    - Verifies: Three "+1{d}" counters bring defense from 3 to 6

15. **test_counters_cease_when_object_ceases**
    - Tests: Rule 1.15.3 - Counters cease with object
    - Verifies: Counters cease when card is destroyed/leaves arena

16. **test_multiple_counters_cease_when_object_ceases**
    - Tests: Rule 1.15.3 - All counters cease with object
    - Verifies: All three counters cease when card ceases to exist

17. **test_removed_counter_ceases_to_exist**
    - Tests: Rule 1.15.3 - Removed counter ceases
    - Verifies: Removed counter's `counter_ceased = True`

18. **test_removing_one_counter_leaves_others_intact**
    - Tests: Rule 1.15.3 - Partial removal leaves others
    - Verifies: Card still has 2 steam counters after removing one of three

19. **test_opposing_counters_both_remain**
    - Tests: Rule 1.15.4 - Opposing counters both remain
    - Verifies: Adding "-1{p}" to card with "+1{p}" keeps both

20. **test_opposing_counters_do_not_cancel**
    - Tests: Rule 1.15.4 - No cancellation between opposing counters
    - Verifies: Net power still 4 (4 base + 1 - 1), both counters remain

21. **test_multiple_opposing_counter_pairs_all_remain**
    - Tests: Rule 1.15.4 - Multiple opposing pairs all remain
    - Verifies: 2 "+1{p}" and 2 "-1{p}" counters all stay on object

22. **test_adding_counter_when_opposing_already_present**
    - Tests: Rule 1.15.4 - Adding more counters with existing opposing pair
    - Verifies: Adding another "+1{p}" results in 2 "+1{p}" and 1 "-1{p}"

#### Implementation Notes:
- All counter tracking uses `CounterStub` with `name` or `(value, symbol)` identity
- `CounterOppositionResultStub` confirms no cancellation when opposing counter added
- Counter modification timing (`"continuous_effect_layer"`) matches continuous effects per Rule 1.15.2a
- All 22 tests pass with stub-based implementation (engine Counter class pending)

#### Engine Features Needed:
- `Counter` class with `name` or `(value, symbol)` identity (Rule 1.15.1)
- `Counter.is_game_object = False` (Rule 1.15.1)
- `CardInstance.counters` list tracking placed counters (Rule 1.15.2)
- `CardInstance.add_counter(counter)` method (Rule 1.15.2)
- `CardInstance.remove_counter(counter)` method (Rule 1.15.3)
- `CardInstance.effective_power` with counter modification (Rule 1.15.2a)
- `CardInstance.effective_defense` with counter modification (Rule 1.15.2a)
- Counter modification same timing layer as continuous effects (Rule 1.15.2a)
- Counters cease when object ceases (Rule 1.15.3)
- No counter cancellation for diametrically opposing counters (Rule 1.15.4)

### Section 1.12: Numbers and Symbols

**File**: `features/section_1_12_numbers_and_symbols.feature`
**Step Definitions**: `step_defs/test_section_1_12_numbers_and_symbols.py`

This section tests number handling and symbol definitions:
- **Rule 1.12.1**: Numbers are always integers
- **Rule 1.12.1a**: Fractional results rounded toward zero (3.5→3, -3.5→-3)
- **Rule 1.12.1b**: Player-chosen numbers must be non-negative integers; "up to N" = 0..N inclusive
- **Rule 1.12.2**: X represents an undefined value
- **Rule 1.12.2a**: Undefined X evaluates to zero (object still has the property)
- **Rule 1.12.2b**: Once X is defined, it stays defined until the object ceases to exist
- **Rule 1.12.2c**: Multiple unknowns in the same context use Y and Z
- **Rule 1.12.3**: Asterisk (*) defined by meta-static ability or continuous effect
- **Rule 1.12.3a**: Undefined * evaluates to zero (Mutated Mass example)
- **Rule 1.12.3b**: Meta-static ability takes priority over continuous effect (Arakni example)
- **Rule 1.12.4**: Symbols represent property values: {d}=defense, {i}=intellect, {h}=life, {p}=power/damage, {r}=resource, {c}=chi, {t}=tap, {u}=untap

#### Test Scenarios:

1. **test_positive_fractional_rounded_toward_zero**
   - Tests: Rule 1.12.1a - 3.5 rounds toward zero to 3
   - Verifies: Fractional number calculation uses truncation toward zero

2. **test_negative_fractional_rounded_toward_zero**
   - Tests: Rule 1.12.1a - -3.5 rounds toward zero to -3
   - Verifies: Negative fractions round toward zero (not floor/ceiling)

3. **test_effect_with_round_up_specification**
   - Tests: Rule 1.12.1a - When "round up" is specified, override default
   - Verifies: 2.5 rounds up to 3 when explicitly specified

4. **test_player_cannot_choose_negative_number**
   - Tests: Rule 1.12.1b - Player-chosen numbers must be non-negative
   - Verifies: Choosing -1 is rejected

5. **test_player_can_choose_zero**
   - Tests: Rule 1.12.1b - Zero is a valid choice
   - Verifies: Choosing 0 is accepted

6. **test_player_can_choose_positive_integer**
   - Tests: Rule 1.12.1b - Positive integers are valid
   - Verifies: Choosing 5 is accepted

7. **test_up_to_n_allows_zero**
   - Tests: Rule 1.12.1b - "Up to N" lower bound is zero
   - Verifies: Choosing 0 from "up to 3" is valid

8. **test_up_to_n_allows_maximum**
   - Tests: Rule 1.12.1b - "Up to N" upper bound is N
   - Verifies: Choosing 3 from "up to 3" is valid

9. **test_up_to_n_rejects_exceeding_maximum**
   - Tests: Rule 1.12.1b - Cannot exceed N in "up to N"
   - Verifies: Choosing 4 from "up to 3" is rejected

10. **test_object_with_undefined_x_still_has_property**
    - Tests: Rule 1.12.2/1.12.2a - Card with power X still has power property
    - Verifies: has_property("power") = True, evaluates to 0 when undefined

11. **test_undefined_x_evaluates_to_zero**
    - Tests: Rule 1.12.2a - Undefined X evaluates to zero
    - Verifies: Card with cost X evaluates cost to 0 when undefined

12. **test_defined_x_persists_until_object_ceases**
    - Tests: Rule 1.12.2b - Defined X stays defined while object exists
    - Verifies: Power evaluates to 4 after X is defined as 4

13. **test_defined_x_does_not_reset**
    - Tests: Rule 1.12.2b - Defined X cannot be reset to undefined
    - Verifies: Power still evaluates to 3 after reset attempt

14. **test_multiple_undefined_values_use_y_and_z**
    - Tests: Rule 1.12.2c - Multiple unknowns use Y and Z
    - Verifies: X and Y are distinct, both evaluate to 0 when undefined

15. **test_object_with_asterisk_still_has_property**
    - Tests: Rule 1.12.3 - Card with power * still has power property
    - Verifies: has_property("power") = True

16. **test_undefined_asterisk_evaluates_to_zero**
    - Tests: Rule 1.12.3a - Undefined * evaluates to zero
    - Verifies: * power evaluates to 0 with no defining ability or effect

17. **test_mutated_mass_outside_game_is_zero**
    - Tests: Rule 1.12.3a - Mutated Mass example
    - Verifies: Power and defense both evaluate to 0 outside game context

18. **test_meta_static_takes_priority_over_continuous_effect**
    - Tests: Rule 1.12.3b - Meta-static beats continuous effect
    - Verifies: With meta-static=5 and continuous=3, * evaluates to 5

19. **test_continuous_effect_defines_asterisk_without_meta_static**
    - Tests: Rule 1.12.3b - Continuous effect used when no meta-static
    - Verifies: With only continuous=4, * evaluates to 4

20. **test_become_copy_effect_defines_asterisk_life**
    - Tests: Rule 1.12.3b - Arakni become/copy example
    - Verifies: Agent of Chaos life = Arakni's printed life value

21–28. **test_*_symbol_represents_***: Tests Rules 1.12.4a-h
    - Verifies each symbol ({d}, {i}, {h}, {p}, {r}, {c}, {t}, {u}) maps to the correct property or effect
    - {p} also refers to physical damage (Rule 1.12.4d)
    - {t} and {u} represent effects (not property values) (Rules 1.12.4g/h)

#### Implementation Notes:
- All helpers are implemented as stubs in the fixture (no engine dependencies)
- The SymbolRegistry stub documents what the engine must implement (Rule 1.12.4)
- Rounding uses Python's `math.trunc()` to implement "round toward zero" (Rule 1.12.1a)
- The _VarCard stub models variable (X) and asterisk (*) properties with correct priority rules

#### Engine Features Needed:
- [ ] `NumberCalculator.calculate(value, round_direction)` (Rule 1.12.1a)
- [ ] `NumberSelector.validate_choice(value, constraint)` (Rule 1.12.1b)
- [ ] `VariableValue` class tracking X, Y, Z with defined/undefined state (Rule 1.12.2)
- [ ] `VariableValue.evaluate()` returning 0 when undefined (Rule 1.12.2a)
- [ ] `VariableValue.define(value)` persisting until source ceases (Rule 1.12.2b)
- [ ] `AsteriskValue` class for * properties (Rule 1.12.3)
- [ ] `AsteriskValue.resolve_priority()` preferring meta-static over continuous (Rule 1.12.3b)
- [ ] `SymbolRegistry` with complete symbol table (Rule 1.12.4)

### Section 2.5: Life

**File**: `features/section_2_5_life.feature`
**Step Definitions**: `step_defs/test_section_2_5_life.py`

This section tests the life property of objects in Flesh and Blood:
- **Rule 2.5.1**: Life is a numeric property representing the starting life total
- **Rule 2.5.1a**: A permanent with the life property is a living object
- **Rule 2.5.2**: Printed life defines the base life; no printed life = no life property; 0 is valid
- **Rule 2.5.3**: Life of a permanent can be modified; "life total" or {h} = modified life
- **Rule 2.5.3a**: Life total = base life + life gained - life lost (tracked by players)
- **Rule 2.5.3b**: Life gained and life lost are discrete effects (permanently modify total, NOT continuous)
- **Rule 2.5.3c**: If base life changes, life total is recalculated (Shiyana example)
- **Rule 2.5.3d**: Life total can exceed base life
- **Rule 2.5.3e**: Life total cannot be negative; capped at zero
- **Rule 2.5.3f**: Hero at zero life → player loses or draw; non-hero permanent at zero → cleared
- **Rule 2.5.3g**: Living object ceasing to exist is considered to have died

#### Test Scenarios:

1. **test_life_is_numeric_property**
   - Tests: Rule 2.5.1/2.5.2 - Life is a numeric property
   - Verifies: Card has life property with numeric value

2. **test_life_represents_starting_life_total**
   - Tests: Rule 2.5.1 - Life represents the starting life total
   - Verifies: `base_life` equals printed life value (starting total)

3. **test_permanent_with_life_is_living_object**
   - Tests: Rule 2.5.1a - Permanent with life property is a living object
   - Verifies: `is_living_object = True` for permanent in arena with life property

4. **test_permanent_without_life_not_living**
   - Tests: Rule 2.5.1a - Permanent without life property is NOT a living object
   - Verifies: `is_living_object = False` for permanent without life property

5. **test_non_permanent_not_living_even_with_life**
   - Tests: Rule 2.5.1a - Only permanents in arena can be living objects
   - Verifies: Non-permanent with life property is not a living object

6. **test_printed_life_defines_base_life**
   - Tests: Rule 2.5.2 - Printed life defines base life
   - Verifies: `base_life` equals printed life value

7. **test_zero_is_valid_printed_life**
   - Tests: Rule 2.5.2 - Zero is a valid printed life
   - Verifies: Card with life 0 still has the life property

8. **test_card_without_printed_life_lacks_property**
   - Tests: Rule 2.5.2 - No printed life means no life property
   - Verifies: `has_life_property = False` for cards without printed life

9. **test_life_can_be_modified**
   - Tests: Rule 2.5.3 - Life of a permanent can be modified
   - Verifies: Life loss effect reduces effective life total

10. **test_life_total_refers_to_modified_life**
    - Tests: Rule 2.5.3 - "life total" refers to modified life
    - Verifies: Modified life total differs from base after gain effect

11. **test_h_symbol_refers_to_modified_life**
    - Tests: Rule 2.5.3 - {h} symbol refers to modified life
    - Verifies: {h} resolves to modified (effective) life total

12. **test_life_total_formula**
    - Tests: Rule 2.5.3a - Life total formula: base + gained - lost
    - Verifies: 20 + 5 - 3 = 22

13. **test_multiple_life_events_accumulate**
    - Tests: Rule 2.5.3a - Multiple life events accumulate
    - Verifies: Multiple gains and losses accumulate correctly

14. **test_life_gain_loss_are_discrete**
    - Tests: Rule 2.5.3b - Life gain/loss are discrete effects
    - Verifies: Removing "source" of discrete gain doesn't undo the life gained

15. **test_discrete_life_permanently_modifies**
    - Tests: Rule 2.5.3b - Discrete life effects permanently modify life total
    - Verifies: Life total remains modified after effect applied

16. **test_base_life_change_recalculates_preserving_lost**
    - Tests: Rule 2.5.3c - Shiyana example: base life change recalculates total
    - Verifies: Shiyana copies Kano (15 base), had lost 5 → new total = 10

17. **test_base_life_change_preserves_life_gained**
    - Tests: Rule 2.5.3c - Base life change preserves life gained
    - Verifies: Gained life preserved when base changes: 10 + 3 = 13

18. **test_life_total_can_exceed_base**
    - Tests: Rule 2.5.3d - Life total can exceed base life
    - Verifies: Life total 25 > base life 20 after gaining 5

19. **test_life_total_capped_at_zero**
    - Tests: Rule 2.5.3e - Life total cannot be negative
    - Verifies: 5 base - 10 lost = capped at 0 (not -5)

20. **test_life_total_exactly_zero**
    - Tests: Rule 2.5.3e - Exactly zero is zero not negative
    - Verifies: 5 - 5 = 0

21. **test_hero_zero_life_triggers_game_state_action**
    - Tests: Rule 2.5.3f - Hero at 0 life triggers game state action
    - Verifies: `game_state_action_fired = True` and `hero_death_handled = True`

22. **test_non_hero_permanent_zero_life_cleared**
    - Tests: Rule 2.5.3f - Non-hero permanent at 0 life cleared
    - Verifies: `permanent_cleared = True` game state action fires

23. **test_living_object_ceasing_is_dead**
    - Tests: Rule 2.5.3g - Living object ceasing = considered dead
    - Verifies: `is_dead = True` when living object ceases to exist

24. **test_death_distinct_from_life_loss**
    - Tests: Rule 2.5.3g - Death vs life loss distinction
    - Verifies: Object that merely lost life is NOT considered dead

25. **test_multiple_independent_life_totals**
    - Tests: Rule 2.5.2 - Multiple cards have independent life totals
    - Verifies: Life loss to hero A doesn't affect hero B

#### Implementation Notes:
- All 25 tests pass with stub-based implementation (`LifeCardStub`, `LifeCheckResultStub`, `GameStateActionResultStub`, `DeathTrackingResultStub`)
- `LifeCardStub.life_total` caps at zero (cross-ref Rule 2.0.3c / Rule 2.5.3e)
- `LifeCardStub.has_life_property` returns False when `printed_life is None` (Rule 2.5.2)
- `LifeCardStub.is_living_object` requires `is_permanent_card and is_in_arena and has_life_property` (Rule 2.5.1a)
- `LifeCardStub.change_base_life(new_value)` preserves life_gained/life_lost for recalculation (Rule 2.5.3c)

#### Engine Features Needed:
- `CardInstance.has_life_property` property: False when no printed life (Rule 2.5.2)
- `CardInstance.base_life` property returning the unmodified printed life (Rule 2.5.2)
- `CardInstance.life_total` property returning modified life total (Rule 2.5.3)
- `Permanent.is_living_object` property: True only when permanent in arena with life property (Rule 2.5.1a)
- Life tracking: `life_gained` + `life_lost` accumulation (Rule 2.5.3a)
- Life gain/loss as discrete effects that permanently modify life total (Rule 2.5.3b)
- Base life change triggers life_total recalculation preserving gain/loss (Rule 2.5.3c)
- `life_total` capped at 0, cannot be negative (Rule 2.5.3e)
- `GameStateAction.check_hero_deaths()` for hero at 0 life (Rule 2.5.3f / 1.10.2a)
- `GameStateAction.clear_zero_life_permanents()` for non-hero at 0 life (Rule 2.5.3f / 1.10.2b)
- `is_dead` tracking for ceased living objects (Rule 2.5.3g)

### Section 2.7: Name

**File**: `features/section_2_7_name.feature`
**Step Definitions**: `step_defs/test_section_2_7_name.py`

This section tests the name property of objects in Flesh and Blood:
- **Rule 2.7.1**: Name is a property of an object representing object identity and uniqueness (with pitch)
- **Rule 2.7.2**: Printed name defines the name of a card
- **Rule 2.7.3**: Personal names determine a moniker (most significant identifier)
- **Rule 2.7.3a**: Non-personal names have no moniker
- **Rule 2.7.3b**: Different names may share the same moniker; moniker-based effects match all
- **Rule 2.7.3c**: A moniker is NOT a name; name-based effects don't match via moniker
- **Rule 2.7.4**: Printed name always considered the English version regardless of card language
- **Rule 2.7.5**: Name matching is exact case-insensitive whole-word match (not substring)

#### Test Scenarios:

1. **test_name_is_property_of_card**
   - Tests: Rule 2.7.1 - Name is a property and object identity
   - Verifies: Card has `has_name_property`, correct name value, name in object identities

2. **test_name_determines_uniqueness_with_pitch**
   - Tests: Rule 2.7.1 - Name + pitch determine uniqueness
   - Verifies: Two Sink Below cards with different pitch values are distinct

3. **test_same_name_and_pitch_not_distinct**
   - Tests: Rule 2.7.1 - Same name and pitch = not distinct
   - Verifies: Two identical Pummel cards are NOT distinct

4. **test_printed_name_defines_card_name**
   - Tests: Rule 2.7.2 - Printed name defines the card name
   - Verifies: Card name equals its printed name

5. **test_personal_name_determines_moniker**
   - Tests: Rule 2.7.3 - Personal name determines moniker
   - Verifies: "Bravo" personal name yields moniker "Bravo"

6. **test_dorinthea_ironsong_moniker**
   - Tests: Rule 2.7.3 - Last name doesn't become moniker
   - Verifies: "Dorinthea Ironsong" yields moniker "Dorinthea"

7. **test_honorific_and_suffix_moniker**
   - Tests: Rule 2.7.3 - Honorifics and suffixes stripped from moniker
   - Verifies: "Ser Boltyn, Breaker of Dawn" yields moniker "Boltyn"

8. **test_the_librarian_moniker**
   - Tests: Rule 2.7.3 - Multi-word moniker (The Librarian)
   - Verifies: "The Librarian" yields moniker "The Librarian"

9. **test_non_personal_name_has_no_moniker**
   - Tests: Rule 2.7.3a - Non-personal names have no moniker
   - Verifies: "Pummel" non-personal name has `moniker = None`

10. **test_action_card_has_no_moniker**
    - Tests: Rule 2.7.3a - Action cards have no moniker
    - Verifies: "Lunging Press" action card has no moniker

11. **test_bravo_showstopper_same_moniker**
    - Tests: Rule 2.7.3b - Different names may share moniker
    - Verifies: "Bravo" and "Bravo, Showstopper" both have moniker "Bravo"

12. **test_effect_moniker_matches_multiple_cards**
    - Tests: Rule 2.7.3b - Moniker-based effect matches all cards with that moniker
    - Verifies: All three Bravo cards (Bravo, Bravo Showstopper, Bravo SOTS) matched

13. **test_dawnblade_name_vs_moniker**
    - Tests: Rule 2.7.3c - Name-based effect does NOT match by moniker
    - Verifies: Effect naming "Dawnblade" matches only "Dawnblade", not "Dawnblade, Resplendent"

14. **test_moniker_not_considered_name**
    - Tests: Rule 2.7.3c - Moniker is not a name
    - Verifies: Name match "Bravo" finds only the card named "Bravo", not "Bravo, Showstopper"

15. **test_printed_name_always_english**
    - Tests: Rule 2.7.4 - English name used regardless of physical card language
    - Verifies: Japanese-printed card still has English name "Pummel"

16. **test_name_matching_whole_word_case_insensitive**
    - Tests: Rule 2.7.5 - Whole-word match (Censor/Blazing Aether example)
    - Verifies: "Blazing Aether" search finds "Blazing Aether" but NOT "Trailblazing Aether"

17. **test_name_matching_case_insensitive**
    - Tests: Rule 2.7.5 - Case-insensitive match
    - Verifies: Lowercase "blazing aether" finds "Blazing Aether"

18. **test_proto_does_not_match_protos**
    - Tests: Rule 2.7.5 - Whole word match (Fabricate/Proto example)
    - Verifies: "Proto" does NOT match "Breaker Helm Protos" ("Protos" ≠ "Proto")

19. **test_full_word_match_finds_correct_cards**
    - Tests: Rule 2.7.5 - Exact word match works
    - Verifies: "Proto" matches "Proto Helm" (Proto is an exact whole word)

#### Implementation Notes:
- All 19 tests pass with stub-based implementation (`NameCardStub`, `PersonalNameParserStub`)
- `NameCardStub.matches_name()` implements whole-word, case-insensitive matching (Rule 2.7.5)
- `PersonalNameParserStub` uses a lookup table for the rulebook examples (Rule 2.7.3)
- `NameCardStub.is_distinct_from()` checks name + pitch for uniqueness (Rule 2.7.1)
- Engine needs `PersonalNameParser` to properly parse the name grammar for all heroes

#### Engine Features Needed:
- `CardTemplate.name` property: the printed name (Rule 2.7.2)
- `CardInstance.name` property accessible from instances (Rule 2.7.1)
- `CardInstance.get_object_identities()`: includes name as identity (Rule 2.7.1)
- `CardTemplate.moniker` property: derived from personal name, or None (Rule 2.7.3)
- `PersonalNameParser.extract_moniker(name)` -> str | None (Rule 2.7.3)
- `CardTemplate.has_moniker` bool property (Rule 2.7.3/2.7.3a)
- `NameMatcher.matches(candidate, query)` with whole-word, case-insensitive matching (Rule 2.7.5)
- `NameMatcher.matches_by_moniker(objects, moniker)` -> List (Rule 2.7.3b)
- `CardTemplate.is_distinct_from(other)` based on name+pitch (Rule 2.7.1 / cross-ref 1.3.4)
- Engine name handling: English-language canonical name always used (Rule 2.7.4)

### Section 2.9: Power

**File**: `features/section_2_9_power.feature`
**Step Definitions**: `step_defs/test_section_2_9_power.py`

This section tests the power property of cards in Flesh and Blood:
- **Rule 2.9.1**: Power is a numeric property of an object, representing the power value used in the damage step of combat
- **Rule 2.9.2**: Printed power defines the base power; no printed power = no property; 0 is valid
- **Rule 2.9.2a**: (c) power is defined by an ability; evaluates to 0 when undetermined
- **Rule 2.9.3**: Power can be modified; "power" or {p} symbol refers to the modified power

#### Test Scenarios:

1. **test_power_is_numeric_property**
   - Tests: Rule 2.9.1/2.9.2 - Power is a numeric property
   - Verifies: Card has power property with numeric value

2. **test_power_value_used_in_damage_step**
   - Tests: Rule 2.9.1 - Power is used in the damage step of combat
   - Verifies: `combat_power` equals the printed power value

3. **test_printed_power_defines_base_power**
   - Tests: Rule 2.9.2 - Printed power defines base power
   - Verifies: `base_power` equals printed power value

4. **test_zero_is_valid_printed_power**
   - Tests: Rule 2.9.2 - Zero is a valid printed power
   - Verifies: Card with power 0 still has the power property

5. **test_card_without_printed_power_lacks_property**
   - Tests: Rule 2.9.2 - No printed power means no power property
   - Verifies: `has_power_property = False` for cards without printed power

6. **test_ability_defined_power**
   - Tests: Rule 2.9.2a - (c) power defined by ability
   - Verifies: Ability-defined power value is correctly returned (Mutated Mass example)

7. **test_ability_defined_power_zero_when_undetermined**
   - Tests: Rule 2.9.2a - Undetermined (c) power evaluates to 0
   - Verifies: Power evaluates to 0 when ability value cannot be determined

8. **test_power_can_be_modified**
   - Tests: Rule 2.9.3 - Power can be modified by effects
   - Verifies: Effect boosting power increases effective_power

9. **test_power_term_refers_to_modified_power**
   - Tests: Rule 2.9.3 - "power" refers to modified power
   - Verifies: Modified power differs from base after boost effect

10. **test_p_symbol_refers_to_modified_power**
    - Tests: Rule 2.9.3 - {p} symbol refers to modified power
    - Verifies: {p} symbol resolves to modified (effective) power

11. **test_power_can_be_decreased**
    - Tests: Rule 2.9.3 - Power can be decreased by effects
    - Verifies: Reduction effect decreases effective_power

12. **test_power_cannot_be_negative**
    - Tests: Rule 2.0.3c cross-ref - Power capped at zero
    - Verifies: Power reduced below zero becomes 0

13. **test_multiple_cards_independent_power**
    - Tests: Rule 2.9.2 - Each card has its own power
    - Verifies: Two cards maintain their own independent power values

#### Implementation Notes:
- All 13 tests pass with stub-based implementation (`PowerCardStub`, `AbilityDefinedPowerCardStub`, `PowerCheckResultStub`)
- `PowerCardStub.effective_power` caps at zero (cross-ref Rule 2.0.3c)
- `AbilityDefinedPowerCardStub.base_power` returns 0 when `ability_defined_value is None` (Rule 2.9.2a)

#### Engine Features Needed:
- `CardInstance.has_power_property` property: False when no printed power (Rule 2.9.2)
- `CardInstance.base_power` property returning the unmodified printed power (Rule 2.9.2)
- `CardInstance.effective_power` returning modified power (Rule 2.9.3)
- `CardInstance.combat_power` used in the damage step of combat (Rule 2.9.1)
- Power modification effects (Rule 2.9.3)
- Numeric power capped at zero (cross-ref Rule 2.0.3c)
- Ability-defined power for (c) notation cards (Rule 2.9.2a)
- Undefined (c) power evaluates to 0 (Rule 2.9.2a)

### Section 2.8: Pitch

**File**: `features/section_2_8_pitch.feature`
**Step Definitions**: `step_defs/test_section_2_8_pitch.py`

This section tests the pitch property of cards in Flesh and Blood:
- **Rule 2.8.1**: Pitch represents assets gained when pitched; value = number of assets; determines uniqueness with name
- **Rule 2.8.2**: Printed pitch expressed as 1-3 {r} or {c} symbols; symbol type = asset type; count = pitch value; no pitch = no property
- **Rule 2.8.3**: Pitch can be modified; "pitch" refers to modified pitch value
- **Rule 2.8.4**: {r}/{c} symbol expression and numerical expression are functionally identical

#### Test Scenarios:

1. **test_pitch_is_property_of_card**
   - Tests: Rule 2.8.1/2.8.2 - Pitch is a property of a card
   - Verifies: Card has pitch property with numeric value

2. **test_pitch_value_represents_assets_gained**
   - Tests: Rule 2.8.1 - Pitch value is the number of assets gained when pitched
   - Verifies: `pitch_to_gain_assets()` returns the pitch value

3. **test_pitch_contributes_to_card_uniqueness**
   - Tests: Rule 2.8.1 - Pitch determines uniqueness along with name
   - Verifies: Sink Below red (pitch 1) and Sink Below blue (pitch 3) are distinct

4. **test_same_name_same_pitch_not_distinct**
   - Tests: Rule 2.8.1 - Cards with same name and pitch are not distinct
   - Verifies: Two identical Pummel cards are NOT distinct

5. **test_one_resource_symbol_is_pitch_1**
   - Tests: Rule 2.8.2 - One resource symbol = pitch value 1
   - Verifies: `printed_pitch == 1` for card with one {r} symbol

6. **test_two_resource_symbols_is_pitch_2**
   - Tests: Rule 2.8.2 - Two resource symbols = pitch value 2
   - Verifies: `printed_pitch == 2` for card with two {r} symbols

7. **test_three_resource_symbols_is_pitch_3**
   - Tests: Rule 2.8.2 - Three resource symbols = pitch value 3
   - Verifies: `printed_pitch == 3` for card with three {r} symbols

8. **test_resource_symbols_generate_resource_points**
   - Tests: Rule 2.8.2 - {r} symbols generate resource points when pitched
   - Verifies: `pitch_asset_type == "resource"` for resource-symbol cards

9. **test_chi_symbols_generate_chi_points**
   - Tests: Rule 2.8.2 - {c} symbols generate chi points when pitched
   - Verifies: `pitch_asset_type == "chi"` for chi-symbol cards

10. **test_printed_pitch_defines_base_pitch**
    - Tests: Rule 2.8.2 - Printed pitch defines base pitch
    - Verifies: `base_pitch` equals printed pitch value

11. **test_card_without_printed_pitch_lacks_property**
    - Tests: Rule 2.8.2 - No printed pitch means no pitch property
    - Verifies: `has_pitch_property == False` for cards without printed pitch

12. **test_pitch_can_be_modified**
    - Tests: Rule 2.8.3 - Pitch can be modified by effects
    - Verifies: Effect boosting pitch increases `effective_pitch`

13. **test_pitch_term_refers_to_modified_pitch**
    - Tests: Rule 2.8.3 - "pitch" refers to modified pitch value
    - Verifies: Modified pitch differs from base after boost effect

14. **test_pitch_can_be_decreased**
    - Tests: Rule 2.8.3 - Pitch can be decreased by effects
    - Verifies: Reduction effect decreases `effective_pitch`

15. **test_pitch_cannot_be_negative**
    - Tests: Rule 2.0.3c cross-ref - Pitch capped at zero
    - Verifies: Pitch reduced below zero becomes 0

16. **test_resource_symbol_identical_to_numeric_pitch_1**
    - Tests: Rule 2.8.4 - {r} and numeric are equivalent
    - Verifies: One {r} symbol equals numeric pitch 1

17. **test_search_by_numeric_pitch_finds_symbol_cards**
    - Tests: Rule 2.8.4 - Search by pitch value finds both numeric and symbol cards
    - Verifies: Cards with numeric pitch 1 and {r}-symbol pitch 1 both found

18. **test_multiple_cards_independent_pitch**
    - Tests: Rule 2.8.2 - Each card has its own pitch
    - Verifies: Two cards maintain their own independent pitch values

#### Implementation Notes:
- All 18 tests pass with stub-based implementation (`PitchCardStub`, `PitchCheckResultStub`, `PitchSearchResultStub`)
- `PitchCardStub.effective_pitch` caps at zero (cross-ref Rule 2.0.3c)
- `PitchCardStub.has_pitch_property` returns False when `printed_pitch is None` (Rule 2.8.2)
- `PitchCardStub.pitch_asset_type` tracks "resource" vs "chi" asset types (Rule 2.8.2)
- `PitchCardStub.is_distinct_from()` checks name + pitch for uniqueness (Rules 2.8.1, 1.3.4)

#### Engine Features Needed:
- `CardInstance.has_pitch_property` property: False when no printed pitch (Rule 2.8.2)
- `CardInstance.base_pitch` property returning the unmodified printed pitch (Rule 2.8.2)
- `CardInstance.effective_pitch` (or `pitch`) returning modified pitch (Rule 2.8.3)
- `CardInstance.pitch_asset_type` returning "resource" or "chi" based on symbol type (Rule 2.8.2)
- `CardInstance.pitch_assets_generated` method returning assets gained when pitched (Rule 2.8.1)
- Pitch modification effects (Rule 2.8.3)
- Numeric pitch capped at zero (cross-ref Rule 2.0.3c)
- `CardTemplate.is_distinct_from(other)` based on name + pitch (Rules 2.8.1, 1.3.4)
- Symbol count ({r} or {c}) and numeric pitch treated as functionally identical (Rule 2.8.4)

### Section 2.10: Subtypes

**File**: `features/section_2_10_subtypes.feature`
**Step Definitions**: `step_defs/test_section_2_10_subtypes.py`

This section tests the subtypes property of objects in Flesh and Blood:
- **Rule 2.10.1**: Subtypes are subtype keywords; functional subtypes determine what additional rules apply
- **Rule 2.10.2**: An object can have zero or more subtypes
- **Rule 2.10.3**: Subtypes determined by type box; printed after long dash after card type
- **Rule 2.10.4**: Activated/triggered-layers inherit source subtypes
- **Rule 2.10.5**: Objects can gain or lose subtypes from rules/effects
- **Rule 2.10.6**: Subtypes are functional or non-functional; functional adds additional rules
- **Rule 2.10.6a**: Functional subtype keywords: (1H), (2H), Affliction, Ally, Arrow, Ash, Attack, Aura, Construct, Figment, Invocation, Item, Landmark, Off-Hand, Quiver (15 total)
- **Rule 2.10.6b**: Non-functional subtypes: Angel, Arms, Axe, Base, Book, Bow, Sword, Staff, etc.

#### Test Scenarios:

1. **test_subtypes_are_subtype_keywords**
   - Tests: Rule 2.10.1/2.10.6a - Subtypes are subtype keywords; Attack is functional
   - Verifies: Card with Attack subtype has it; Attack recognized as functional

2. **test_non_functional_subtypes_add_no_rules**
   - Tests: Rule 2.10.6b - Non-functional subtypes don't add additional rules
   - Verifies: Sword is not a functional subtype

3. **test_object_with_zero_subtypes**
   - Tests: Rule 2.10.2 - Object can have zero subtypes
   - Verifies: No-subtype card has empty subtypes and is still a valid object

4. **test_object_can_have_one_subtype**
   - Tests: Rule 2.10.2 - Object can have exactly one subtype
   - Verifies: Ally-subtype card has exactly 1 subtype

5. **test_object_can_have_multiple_subtypes**
   - Tests: Rule 2.10.2 - Object can have multiple subtypes
   - Verifies: Card with Attack and Arrow has exactly 2 subtypes

6. **test_subtypes_determined_by_type_box**
   - Tests: Rule 2.10.3 - Subtypes from type box after long dash
   - Verifies: "Action - Attack" parses to type "Action" and subtype "Attack"

7. **test_card_with_no_dash_has_no_subtype**
   - Tests: Rule 2.10.3 - No long dash = no subtype
   - Verifies: "Instant" type box yields no subtypes

8. **test_activated_layer_inherits_subtypes**
   - Tests: Rule 2.10.4 - Activated-layer inherits source subtypes
   - Verifies: Activated-layer from Ally-source has Ally subtype

9. **test_triggered_layer_inherits_subtypes**
   - Tests: Rule 2.10.4 - Triggered-layer inherits source subtypes
   - Verifies: Triggered-layer from Aura-source has Aura subtype

10. **test_layer_from_no_subtype_source**
    - Tests: Rule 2.10.4 - Layer with no-subtype source has zero subtypes
    - Verifies: Activated-layer from no-subtype source has empty subtypes

11. **test_object_can_gain_subtype**
    - Tests: Rule 2.10.5 - Object can gain a subtype from an effect
    - Verifies: Card gains Aura subtype via effect; goes from 0 to 1 subtype

12. **test_object_can_lose_subtype**
    - Tests: Rule 2.10.5 - Object can lose a subtype from an effect
    - Verifies: Card loses Arrow; retains Attack

13. **test_functional_subtypes_include_attack**
    - Tests: Rule 2.10.6 - Functional subtypes add rules; Attack is functional
    - Verifies: Attack is in the functional subtype keyword list

14. **test_all_functional_subtypes_recognized**
    - Tests: Rule 2.10.6a - All 15 functional subtype keywords recognized
    - Verifies: (1H), (2H), Affliction, Ally, Arrow, Ash, Aura, Construct, Figment, Invocation, Item, Landmark, Off-Hand, Quiver all functional

15. **test_non_functional_subtypes_recognized**
    - Tests: Rule 2.10.6b - Non-functional subtypes recognized
    - Verifies: Sword, Bow, Staff, Dagger, Axe all non-functional

16. **test_exactly_15_functional_subtypes**
    - Tests: Rule 2.10.6a - Exactly 15 functional subtype keywords
    - Verifies: functional keyword count == 15

17. **test_attack_subtype_is_functional**
    - Tests: Rule 2.10.6/2.10.6a - Attack subtype adds additional rules
    - Verifies: `adds_additional_rules == True` for Attack subtype

18. **test_sword_subtype_is_non_functional**
    - Tests: Rule 2.10.6b - Sword subtype doesn't add additional rules
    - Verifies: `adds_additional_rules == False` for Sword subtype

19. **test_card_can_have_both_functional_and_non_functional_subtypes**
    - Tests: Rule 2.10.6 - Cards can have both functional and non-functional subtypes
    - Verifies: Attack+Sword card; functional_subtypes contains only Attack

20. **test_layer_inherits_multiple_subtypes**
    - Tests: Rule 2.10.4 - Layer inherits all subtypes from multi-subtype source
    - Verifies: Layer from Attack+Arrow source has both subtypes

#### Implementation Notes:
- All 20 tests pass with stub-based implementation (`SubtypeCardStub`, `LayerWithSubtypesStub`, `TypeBoxParseResultStub`, `SubtypeCheckResultStub`)
- `SubtypeCardStub.functional_subtypes` filters by `FUNCTIONAL_SUBTYPES` frozenset (Rule 2.10.6)
- `LayerWithSubtypesStub.subtypes` delegates to `source.subtypes` (Rule 2.10.4)
- `TypeBoxParseResultStub.parse_type_box()` splits on " - " to extract type and subtypes (Rule 2.10.3)
- `SubtypeCheckResultStub.for_subtype(name)` checks against `FUNCTIONAL_SUBTYPES` frozenset (Rule 2.10.6)
- parsers.parse() used for parametrized `"{keyword}" should be a functional/non-functional subtype` steps

#### Engine Features Needed:
- `CardTemplate.subtypes` or `CardInstance.subtypes` returning a collection of subtype strings (Rule 2.10.2)
- `CardInstance.functional_subtypes` returning only functional subtypes (Rule 2.10.6)
- `SubtypeRegistry.is_functional(name)` classifying subtypes as functional or not (Rule 2.10.6)
- `SubtypeRegistry.FUNCTIONAL_SUBTYPES` frozenset containing exactly 15 functional subtypes (Rule 2.10.6a)
- Type box parser: extracts type and subtypes from "Type - Subtype" format (Rule 2.10.3)
- `Layer.subtypes` property inheriting from source (Rule 2.10.4)
- `CardInstance.gain_subtype(name)` method (Rule 2.10.5)
- `CardInstance.lose_subtype(name)` method (Rule 2.10.5)

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
- [x] 1.11: Priority
- [x] 1.12: Numbers and Symbols
- [x] 1.13: Assets
- [x] 1.14: Costs
- [x] 1.15: Counters

### Section 2: Object Properties
- [x] 2.0: General
- [x] 2.1: Color
- [x] 2.2: Cost
- [x] 2.3: Defense
- [x] 2.4: Intellect
- [x] 2.5: Life
- [x] 2.6: Metatype
- [x] 2.7: Name
- [x] 2.8: Pitch
- [x] 2.9: Power
- [x] 2.10: Subtypes
- [x] 2.11: Supertypes
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
