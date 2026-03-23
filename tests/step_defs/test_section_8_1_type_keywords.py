"""
Step definitions for Section 8.1: Type Keywords
Reference: Flesh and Blood Comprehensive Rules Section 8.1

This module implements behavioral tests for each type keyword's specific rules,
covering Action, Attack Reaction, Defense Reaction, Equipment, Hero, Instant,
Resource, Token, Weapon, Mentor, Demi-Hero, Block, Macro, and Companion types.

Engine Features Needed for Section 8.1:
- [ ] CardType.TOKEN enum value (Rule 8.1.8)
- [ ] CardType.RESOURCE enum value (Rule 8.1.7)
- [ ] CardType.MENTOR enum value (Rule 8.1.10)
- [ ] CardType.BLOCK enum value (Rule 8.1.12)
- [ ] CardType.MACRO enum value (Rule 8.1.13)
- [ ] CardType.COMPANION enum value (Rule 8.1.14)
- [ ] CardType.DEMI_HERO enum value (Rule 8.1.11)
- [ ] Action.can_play_on_empty_stack() — validates Rule 8.1.1a
- [ ] Action.can_play_during_combat() — validates Rule 8.1.1b (only in Resolution Step)
- [ ] Action.action_point_cost — additional asset-cost of 1 AP (Rule 8.1.1c)
- [ ] Action.played_as_instant_flags — still action but no AP cost (Rule 8.1.1d)
- [ ] AttackReaction.can_play_restriction() — only attack controller, Reaction Step (Rule 8.1.2a)
- [ ] AttackReaction.resolves_as_cleared() — card is cleared on resolution (Rule 8.1.2b)
- [ ] DefenseReaction.can_play_restriction() — only hero attack-target controller, Reaction Step (Rule 8.1.3a)
- [ ] DefenseReaction.resolves_as_defending_card() — becomes defending card on resolution (Rule 8.1.3b)
- [ ] Token.ceases_to_exist_outside_arena() — token ceases to exist when leaving arena (Rule 8.1.8a)
- [ ] Mentor.card_pool_eligibility_young_hero() — needs young (subtype) hero (Rule 8.1.10a)
- [ ] DemiHero.becomes_hero_without_hero() — becomes player's hero if no hero controlled (Rule 8.1.11b)
- [ ] DemiHero.cleared_if_hero_exists() — cleared from arena if player controls hero (Rule 8.1.11b)
- [ ] Macro.has_macro_type_only_macros() — only macro objects have the macro type (Rule 8.1.13a)

Current status: Tests written, Engine pending
"""

import pytest
from pytest_bdd import scenario, given, when, then, parsers


# ===== 8.1.1 Action Scenarios =====

@scenario(
    "../features/section_8_1_type_keywords.feature",
    "Action card is a deck-card",
)
def test_action_card_is_deck_card():
    """Rule 8.1.1: An action card is a deck-card."""
    pass


@scenario(
    "../features/section_8_1_type_keywords.feature",
    "Action card can only be played when the stack is empty",
)
def test_action_card_requires_empty_stack():
    """Rule 8.1.1a: An action card can only be played when the stack is empty."""
    pass


@scenario(
    "../features/section_8_1_type_keywords.feature",
    "Action card cannot be played when the stack is not empty",
)
def test_action_card_blocked_when_stack_not_empty():
    """Rule 8.1.1a: An action card cannot be played when the stack is not empty."""
    pass


@scenario(
    "../features/section_8_1_type_keywords.feature",
    "Action card cannot be played during combat outside Resolution Step",
)
def test_action_card_blocked_during_combat():
    """Rule 8.1.1b: Action cannot be played during combat except the Resolution Step."""
    pass


@scenario(
    "../features/section_8_1_type_keywords.feature",
    "Action card can be played during the Resolution Step of combat",
)
def test_action_card_allowed_in_resolution_step():
    """Rule 8.1.1b: Action can be played during the Resolution Step of combat."""
    pass


@scenario(
    "../features/section_8_1_type_keywords.feature",
    "Action card requires one action point as additional asset-cost",
)
def test_action_card_requires_action_point():
    """Rule 8.1.1c: An action card has the additional asset-cost of one action point."""
    pass


@scenario(
    "../features/section_8_1_type_keywords.feature",
    "Action card played as instant is still considered an action",
)
def test_action_played_as_instant_still_action():
    """Rule 8.1.1d: Action played as instant is still an action, no AP cost."""
    pass


# ===== 8.1.2 Attack Reaction Scenarios =====

@scenario(
    "../features/section_8_1_type_keywords.feature",
    "Attack reaction card is a deck-card",
)
def test_attack_reaction_is_deck_card():
    """Rule 8.1.2: An attack reaction card is a deck-card."""
    pass


@scenario(
    "../features/section_8_1_type_keywords.feature",
    "Attack reaction can only be played by attack controller during Reaction Step",
)
def test_attack_reaction_requires_attack_controller():
    """Rule 8.1.2a: Attack reaction can only be played by the attack controller."""
    pass


@scenario(
    "../features/section_8_1_type_keywords.feature",
    "Attack reaction cannot be played by non-attack-controller",
)
def test_attack_reaction_blocked_for_non_attack_controller():
    """Rule 8.1.2a: Attack reaction cannot be played by non-attack-controller."""
    pass


@scenario(
    "../features/section_8_1_type_keywords.feature",
    "Attack reaction card is cleared when it resolves as a layer",
)
def test_attack_reaction_cleared_on_resolution():
    """Rule 8.1.2b: Attack reaction is cleared when it resolves as a layer."""
    pass


@scenario(
    "../features/section_8_1_type_keywords.feature",
    "Attack reaction card is considered a reaction card",
)
def test_attack_reaction_is_reaction_card():
    """Rule 8.1.2c: An attack reaction card is considered a reaction card."""
    pass


# ===== 8.1.3 Defense Reaction Scenarios =====

@scenario(
    "../features/section_8_1_type_keywords.feature",
    "Defense reaction card is a deck-card",
)
def test_defense_reaction_is_deck_card():
    """Rule 8.1.3: A defense reaction card is a deck-card."""
    pass


@scenario(
    "../features/section_8_1_type_keywords.feature",
    "Defense reaction can only be played by hero attack-target controller during Reaction Step",
)
def test_defense_reaction_requires_hero_attack_target():
    """Rule 8.1.3a: Defense reaction requires controlling a hero that is an attack-target."""
    pass


@scenario(
    "../features/section_8_1_type_keywords.feature",
    "Defense reaction cannot be played by player who does not control attack-target hero",
)
def test_defense_reaction_blocked_when_no_attack_target_hero():
    """Rule 8.1.3a: Defense reaction is blocked if player's hero is not an attack-target."""
    pass


@scenario(
    "../features/section_8_1_type_keywords.feature",
    "Defense reaction card becomes a defending card when it resolves",
)
def test_defense_reaction_becomes_defending_card():
    """Rule 8.1.3b: Defense reaction becomes a defending card on resolution."""
    pass


@scenario(
    "../features/section_8_1_type_keywords.feature",
    "Defense reaction card is considered a reaction card",
)
def test_defense_reaction_is_reaction_card():
    """Rule 8.1.3c: A defense reaction card is considered a reaction card."""
    pass


# ===== 8.1.4 Equipment Scenarios =====

@scenario(
    "../features/section_8_1_type_keywords.feature",
    "Equipment card is an arena-card",
)
def test_equipment_is_arena_card():
    """Rule 8.1.4: An equipment card (without other types) is an arena-card."""
    pass


@scenario(
    "../features/section_8_1_type_keywords.feature",
    "Equipment card can be equipped from card-pool at game start",
)
def test_equipment_equippable_at_game_start():
    """Rule 8.1.4a: Equipment can be equipped from card-pool during start-of-game."""
    pass


@scenario(
    "../features/section_8_1_type_keywords.feature",
    "Equipment permanent can be declared as a defending card",
)
def test_equipment_can_be_defending_card():
    """Rule 8.1.4b: An equipment permanent may be declared as a defending card."""
    pass


# ===== 8.1.5 Hero Scenarios =====

@scenario(
    "../features/section_8_1_type_keywords.feature",
    "Hero card is a hero-card",
)
def test_hero_is_hero_card():
    """Rule 8.1.5: A hero card is a hero-card."""
    pass


@scenario(
    "../features/section_8_1_type_keywords.feature",
    "Hero card starts as a permanent in the hero zone",
)
def test_hero_starts_in_hero_zone():
    """Rule 8.1.5a: A player starts the game with their hero card in the hero zone."""
    pass


@scenario(
    "../features/section_8_1_type_keywords.feature",
    "Hero card cannot be included in a player's card-pool",
)
def test_hero_not_in_card_pool():
    """Rule 8.1.5b: A hero card cannot be included in a player's card-pool."""
    pass


# ===== 8.1.6 Instant Scenarios =====

@scenario(
    "../features/section_8_1_type_keywords.feature",
    "Instant card is a deck-card",
)
def test_instant_is_deck_card():
    """Rule 8.1.6: An instant card is a deck-card."""
    pass


@scenario(
    "../features/section_8_1_type_keywords.feature",
    "Instant card can be played any time player has priority",
)
def test_instant_playable_any_time():
    """Rule 8.1.6a: An instant can be played any time the player has priority."""
    pass


# ===== 8.1.7 Resource Scenarios =====

@scenario(
    "../features/section_8_1_type_keywords.feature",
    "Resource card is a deck-card",
)
def test_resource_is_deck_card():
    """Rule 8.1.7: A resource card is a deck-card."""
    pass


@scenario(
    "../features/section_8_1_type_keywords.feature",
    "Resource card cannot be played",
)
def test_resource_card_cannot_be_played():
    """Rule 8.1.7a: A resource card cannot be played."""
    pass


# ===== 8.1.8 Token Scenarios =====

@scenario(
    "../features/section_8_1_type_keywords.feature",
    "Token card is a token-card",
)
def test_token_is_token_card():
    """Rule 8.1.8: A token card is a token-card."""
    pass


@scenario(
    "../features/section_8_1_type_keywords.feature",
    "Token only exists in the arena or as a sub-card",
)
def test_token_exists_only_in_arena_or_as_subcard():
    """Rule 8.1.8a: Tokens only exist in the arena or as sub-cards."""
    pass


@scenario(
    "../features/section_8_1_type_keywords.feature",
    "Token ceases to exist when it leaves the arena and is not a sub-card",
)
def test_token_ceases_to_exist_outside_arena():
    """Rule 8.1.8a: A token that leaves the arena and is not a sub-card ceases to exist."""
    pass


# ===== 8.1.9 Weapon Scenarios =====

@scenario(
    "../features/section_8_1_type_keywords.feature",
    "Weapon card is an arena-card",
)
def test_weapon_is_arena_card():
    """Rule 8.1.9: A weapon card is an arena-card."""
    pass


@scenario(
    "../features/section_8_1_type_keywords.feature",
    "Weapon card can be equipped from card-pool at game start",
)
def test_weapon_equippable_at_game_start():
    """Rule 8.1.9a: Weapon can be equipped from card-pool during start-of-game."""
    pass


# ===== 8.1.10 Mentor Scenarios =====

@scenario(
    "../features/section_8_1_type_keywords.feature",
    "Mentor card is a deck-card",
)
def test_mentor_is_deck_card():
    """Rule 8.1.10: A mentor card is a deck-card."""
    pass


@scenario(
    "../features/section_8_1_type_keywords.feature",
    "Mentor card can only be in card-pool with a young hero",
)
def test_mentor_allowed_with_young_hero():
    """Rule 8.1.10a: Mentor can be in card-pool if player has a young hero."""
    pass


@scenario(
    "../features/section_8_1_type_keywords.feature",
    "Mentor card cannot be in card-pool without a young hero",
)
def test_mentor_blocked_without_young_hero():
    """Rule 8.1.10a: Mentor cannot be in card-pool without a young hero."""
    pass


# ===== 8.1.11 Demi-Hero Scenarios =====

@scenario(
    "../features/section_8_1_type_keywords.feature",
    "Demi-hero card is an arena-card",
)
def test_demi_hero_is_arena_card():
    """Rule 8.1.11: A demi-hero card is an arena-card."""
    pass


@scenario(
    "../features/section_8_1_type_keywords.feature",
    "Demi-hero card is included in the player's card-pool",
)
def test_demi_hero_in_card_pool():
    """Rule 8.1.11a: Demi-hero is included in card-pool and not used in place of hero."""
    pass


@scenario(
    "../features/section_8_1_type_keywords.feature",
    "Demi-hero becomes player's hero when no hero is controlled",
)
def test_demi_hero_becomes_hero_without_hero():
    """Rule 8.1.11b: Demi-hero becomes player's hero when player controls no hero."""
    pass


@scenario(
    "../features/section_8_1_type_keywords.feature",
    "Demi-hero is cleared when player already controls a hero",
)
def test_demi_hero_cleared_when_hero_controlled():
    """Rule 8.1.11b: Demi-hero is cleared from arena when player controls a hero."""
    pass


# ===== 8.1.12 Block Scenarios =====

@scenario(
    "../features/section_8_1_type_keywords.feature",
    "Block card is a deck-card",
)
def test_block_is_deck_card():
    """Rule 8.1.12: A block card is a deck-card."""
    pass


@scenario(
    "../features/section_8_1_type_keywords.feature",
    "Block card cannot be played",
)
def test_block_card_cannot_be_played():
    """Rule 8.1.12a: A block card cannot be played."""
    pass


# ===== 8.1.13 Macro Scenarios =====

@scenario(
    "../features/section_8_1_type_keywords.feature",
    "Macro objects have the macro type",
)
def test_macro_objects_have_macro_type():
    """Rule 8.1.13a: Only macro objects have the macro type."""
    pass


@scenario(
    "../features/section_8_1_type_keywords.feature",
    "Only macro objects have the macro type",
)
def test_non_macro_does_not_have_macro_type():
    """Rule 8.1.13a: Non-macro objects do not have the macro type."""
    pass


# ===== 8.1.14 Companion Scenarios =====

@scenario(
    "../features/section_8_1_type_keywords.feature",
    "Companion card is an arena-card",
)
def test_companion_is_arena_card():
    """Rule 8.1.14: A companion card is an arena-card."""
    pass


# ===== Step Definitions =====

# --- Given steps ---

@given(parsers.parse('a card with the type "{card_type}"'))
def given_card_with_type(game_state, card_type):
    """Create a card with the specified type keyword."""
    from fab_engine.cards.model import CardType

    type_map = {
        "Action": CardType.ACTION,
        "Attack Reaction": CardType.ATTACK_REACTION,
        "Defense Reaction": CardType.DEFENSE_REACTION,
        "Instant": CardType.INSTANT,
        "Equipment": CardType.EQUIPMENT,
        "Weapon": CardType.WEAPON,
        "Hero": CardType.HERO,
    }

    if card_type in type_map:
        game_state.test_card = game_state.create_card(
            name=f"Test {card_type}",
            card_type=type_map[card_type],
        )
    else:
        # Types not yet in engine — use metadata flags
        game_state.test_card = game_state.create_card(name=f"Test {card_type}")
        flag_map = {
            "Token": "_is_token",
            "Resource": "_is_resource",
            "Mentor": "_is_mentor",
            "Block": "_is_block",
            "Macro": "_is_macro",
            "Companion": "_is_companion",
            "Demi-Hero": "_is_demi_hero",
        }
        if card_type in flag_map:
            setattr(game_state.test_card, flag_map[card_type], True)

    game_state.current_card_type = card_type


@given("the stack is empty")
def given_stack_is_empty(game_state):
    """Set up game state with an empty stack."""
    game_state.stack_is_empty = True
    game_state.stack_has_layers = False


@given("another layer is on the stack")
def given_stack_has_layer(game_state):
    """Set up game state with a layer on the stack."""
    game_state.stack_is_empty = False
    game_state.stack_has_layers = True


@given("the game is in the Reaction Step of combat")
def given_reaction_step(game_state):
    """Set game state to the Reaction Step of combat."""
    game_state.current_combat_step = "reaction"
    game_state.in_combat = True


@given("the game is in the Resolution Step of combat")
def given_resolution_step(game_state):
    """Set game state to the Resolution Step of combat."""
    game_state.current_combat_step = "resolution"
    game_state.in_combat = True


@given("the player has one action point")
def given_player_has_action_point(game_state):
    """Set player to have one action point."""
    game_state.player_action_points = 1


@given("an effect allows playing the action card as though it were an instant")
def given_play_action_as_instant(game_state):
    """Set up an effect that allows playing the action card as an instant."""
    game_state.action_played_as_instant = True


@given("the player controls the current attack")
def given_player_controls_attack(game_state):
    """Set up game state where the player controls the current attack."""
    game_state.player_controls_attack = True
    game_state.player_controls_attack_target_hero = False


@given("the player does not control the current attack")
def given_player_does_not_control_attack(game_state):
    """Set up game state where the player does not control the current attack."""
    game_state.player_controls_attack = False


@given("the player controls a hero that is an attack-target")
def given_player_controls_attack_target_hero(game_state):
    """Set up game state where the player controls a hero that is an attack-target."""
    game_state.player_controls_attack_target_hero = True
    game_state.player_controls_attack = False


@given("the player does not control a hero that is an attack-target")
def given_player_does_not_control_attack_target_hero(game_state):
    """Set up game state where the player's hero is not an attack-target."""
    game_state.player_controls_attack_target_hero = False


@given("an attack reaction card that has resolved as a layer on the stack")
def given_attack_reaction_resolved(game_state):
    """Set up an attack reaction card that has resolved on the stack."""
    from fab_engine.cards.model import CardType
    game_state.test_card = game_state.create_card(
        name="Test Attack Reaction",
        card_type=CardType.ATTACK_REACTION,
    )
    game_state.card_resolved_as_layer = True
    game_state.layer_resolution_type = "attack_reaction"


@given("a defense reaction card that has resolved as a layer on the stack")
def given_defense_reaction_resolved(game_state):
    """Set up a defense reaction card that has resolved on the stack."""
    from fab_engine.cards.model import CardType
    game_state.test_card = game_state.create_card(
        name="Test Defense Reaction",
        card_type=CardType.DEFENSE_REACTION,
    )
    game_state.card_resolved_as_layer = True
    game_state.layer_resolution_type = "defense_reaction"


@given("an equipment permanent in a player's equipment zone")
def given_equipment_permanent(game_state):
    """Set up an equipment permanent in the player's equipment zone."""
    from fab_engine.cards.model import CardType
    game_state.test_card = game_state.create_card(
        name="Test Equipment",
        card_type=CardType.EQUIPMENT,
    )
    game_state.play_card_to_arena(game_state.test_card)
    game_state.equipment_in_zone = True


@given("the game is in the Defend Step of combat")
def given_defend_step(game_state):
    """Set game state to the Defend Step of combat."""
    game_state.current_combat_step = "defend"
    game_state.in_combat = True


@given("a player has a hero card")
def given_player_has_hero_card(game_state):
    """Set up a player with a hero card."""
    from fab_engine.cards.model import CardType
    game_state.test_card = game_state.create_card(
        name="Test Hero",
        card_type=CardType.HERO,
    )


@given("the player has priority")
def given_player_has_priority(game_state):
    """Set up game state where the player has priority."""
    game_state.player_has_priority = True


@given("the card is in the player's card-pool")
def given_card_in_card_pool(game_state):
    """Indicate the card is in the player's card-pool."""
    game_state.card_in_card_pool = True


@given("the game is in the start-of-game procedure")
def given_start_of_game(game_state):
    """Set game state to the start-of-game procedure."""
    game_state.start_of_game_procedure = True


@given("a token permanent in the arena")
def given_token_permanent_in_arena(game_state):
    """Set up a token permanent in the arena."""
    game_state.test_card = game_state.create_token_card(name="Test Token")
    game_state.token_in_arena = True
    game_state.token_is_subcard = False


@given("the token is not a sub-card")
def given_token_not_subcard(game_state):
    """Indicate the token is not a sub-card."""
    game_state.token_is_subcard = False


@given("the player's hero has the young subtype")
def given_hero_has_young_subtype(game_state):
    """Set up game state where the player's hero has the young subtype."""
    game_state.hero_has_young_subtype = True


@given("the player's hero does not have the young subtype")
def given_hero_lacks_young_subtype(game_state):
    """Set up game state where the player's hero does not have the young subtype."""
    game_state.hero_has_young_subtype = False


@given("a demi-hero permanent in the arena")
def given_demi_hero_permanent(game_state):
    """Set up a demi-hero permanent in the arena."""
    game_state.test_card = game_state.create_card(name="Test Demi-Hero")
    setattr(game_state.test_card, "_is_demi_hero", True)
    game_state.demi_hero_in_arena = True


@given("the controlling player does not control a hero")
def given_no_hero_controlled(game_state):
    """Set up game state where the player controls no hero."""
    game_state.player_controls_hero = False


@given("the controlling player already controls a hero")
def given_hero_already_controlled(game_state):
    """Set up game state where the player already controls a hero."""
    game_state.player_controls_hero = True


@given("a demi-hero that has just become a permanent in the arena")
def given_demi_hero_just_became_permanent(game_state):
    """Set up a demi-hero that has just become a permanent in the arena."""
    game_state.test_card = game_state.create_card(name="Test Demi-Hero")
    setattr(game_state.test_card, "_is_demi_hero", True)
    game_state.demi_hero_in_arena = True


@given("a macro object exists in the game")
def given_macro_object(game_state):
    """Set up a macro object in the game."""
    game_state.test_macro = game_state.check_macro_type_rules()


@given("a card that is not a macro object")
def given_non_macro_card(game_state):
    """Set up a regular card that is not a macro."""
    from fab_engine.cards.model import CardType
    game_state.test_card = game_state.create_card(
        name="Test Non-Macro",
        card_type=CardType.ACTION,
    )


# --- When steps ---

@when("the game categorizes the card")
def when_game_categorizes(game_state):
    """Let the game categorize the card."""
    game_state.categorization_result = game_state.get_card_category(game_state.test_card)


@when("the player attempts to play the action card")
def when_play_action(game_state):
    """Attempt to play the action card."""
    game_state.play_result = game_state.check_action_play_legality(
        card=game_state.test_card,
        stack_empty=getattr(game_state, "stack_is_empty", True),
        in_combat=getattr(game_state, "in_combat", False),
        combat_step=getattr(game_state, "current_combat_step", None),
    )


@when("the game evaluates the action card's cost")
def when_evaluate_action_cost(game_state):
    """Evaluate the action card's cost requirements."""
    game_state.cost_check = game_state.check_action_point_cost(game_state.test_card)


@when("the player plays the action card as an instant")
def when_play_action_as_instant(game_state):
    """Play the action card as though it were an instant."""
    game_state.play_as_instant_result = game_state.play_action_as_instant(
        card=game_state.test_card
    )


@when("the player attempts to play the attack reaction card")
def when_play_attack_reaction(game_state):
    """Attempt to play the attack reaction card."""
    game_state.play_result = game_state.check_attack_reaction_play_legality(
        card=game_state.test_card,
        combat_step=getattr(game_state, "current_combat_step", None),
        player_controls_attack=getattr(game_state, "player_controls_attack", False),
    )


@when("the resolution step processes the layer")
def when_resolution_step_processes(game_state):
    """Have the resolution step process the resolved layer."""
    game_state.layer_processing_result = game_state.process_resolved_layer(
        card=game_state.test_card,
        layer_type=getattr(game_state, "layer_resolution_type", "unknown"),
    )


@when("the game checks whether the card is a reaction card")
def when_check_is_reaction(game_state):
    """Check whether the card is considered a reaction card."""
    game_state.is_reaction_result = game_state.check_is_reaction_card(game_state.test_card)


@when("the player attempts to play the defense reaction card")
def when_play_defense_reaction(game_state):
    """Attempt to play the defense reaction card."""
    game_state.play_result = game_state.check_defense_reaction_play_legality(
        card=game_state.test_card,
        combat_step=getattr(game_state, "current_combat_step", None),
        player_controls_attack_target_hero=getattr(
            game_state, "player_controls_attack_target_hero", False
        ),
    )


@when("the player equips the equipment card")
def when_equip_equipment(game_state):
    """Equip an equipment card during the start-of-game procedure."""
    game_state.equip_result = game_state.equip_arena_card_at_game_start(
        card=game_state.test_card,
        card_type="equipment",
    )


@when("the player declares the equipment as a defending card")
def when_declare_equipment_defender(game_state):
    """Declare an equipment permanent as a defending card."""
    game_state.defend_result = game_state.check_equipment_can_defend(game_state.test_card)


@when("the game starts")
def when_game_starts(game_state):
    """Simulate the game start procedure."""
    game_state.game_start_result = game_state.check_hero_initial_placement(game_state.test_card)


@when("the game checks if the hero card can be included in a card-pool")
def when_check_hero_in_card_pool(game_state):
    """Check if the hero card can be included in a player's card-pool."""
    game_state.hero_card_pool_result = game_state.is_valid_for_card_pool(game_state.test_card)


@when("the game checks when the instant card can be played")
def when_check_instant_timing(game_state):
    """Check the timing restrictions for the instant card."""
    game_state.instant_timing_result = game_state.check_instant_play_timing(game_state.test_card)


@when("the player attempts to play the resource card")
def when_play_resource(game_state):
    """Attempt to play the resource card."""
    game_state.play_result = game_state.check_resource_can_be_played(game_state.test_card)


@when("the game checks the token's valid locations")
def when_check_token_locations(game_state):
    """Check the valid locations for the token."""
    game_state.token_location_result = game_state.check_token_valid_locations(
        game_state.test_card
    )


@when("the token leaves the arena")
def when_token_leaves_arena(game_state):
    """Simulate the token leaving the arena."""
    game_state.token_leave_result = game_state.process_token_leaving_arena(
        card=game_state.test_card,
        is_subcard=getattr(game_state, "token_is_subcard", False),
    )


@when("the player equips the weapon card")
def when_equip_weapon(game_state):
    """Equip a weapon card during the start-of-game procedure."""
    game_state.equip_result = game_state.equip_arena_card_at_game_start(
        card=game_state.test_card,
        card_type="weapon",
    )


@when("the game checks if the mentor card can be included in the card-pool")
def when_check_mentor_card_pool(game_state):
    """Check if the mentor card can be included in the card-pool."""
    game_state.mentor_eligibility = game_state.check_mentor_card_pool_eligibility(
        card=game_state.test_card,
        hero_has_young_subtype=getattr(game_state, "hero_has_young_subtype", False),
    )


@when("the game checks the demi-hero's card classification")
def when_check_demi_hero_classification(game_state):
    """Check the demi-hero's card classification."""
    game_state.demi_hero_classification = game_state.check_demi_hero_classification(
        game_state.test_card
    )


@when("the demi-hero becomes a permanent in the arena")
def when_demi_hero_becomes_permanent(game_state):
    """Process the demi-hero becoming a permanent in the arena."""
    game_state.demi_hero_permanent_result = game_state.process_demi_hero_arrival(
        card=game_state.test_card,
        player_controls_hero=getattr(game_state, "player_controls_hero", False),
    )


@when("the game resolves the demi-hero's arrival")
def when_resolve_demi_hero_arrival(game_state):
    """Resolve the demi-hero's arrival in the arena."""
    game_state.demi_hero_permanent_result = game_state.process_demi_hero_arrival(
        card=game_state.test_card,
        player_controls_hero=getattr(game_state, "player_controls_hero", True),
    )


@when("the player attempts to play the block card")
def when_play_block(game_state):
    """Attempt to play the block card."""
    game_state.play_result = game_state.check_block_can_be_played(game_state.test_card)


@when("the game checks the macro object's type")
def when_check_macro_type(game_state):
    """Check the macro object's type."""
    game_state.macro_type_result = game_state.check_macro_object_type(game_state.test_macro)


@when("the game checks if the card has the macro type")
def when_check_card_has_macro_type(game_state):
    """Check if a non-macro card has the macro type."""
    game_state.macro_type_result = game_state.check_non_macro_has_macro_type(
        game_state.test_card
    )


# --- Then steps ---

@then("the card is categorized as a deck-card")
def then_card_is_deck_card(game_state):
    """Assert the card is categorized as a deck-card."""
    assert game_state.categorization_result == "deck", (
        f"Expected 'deck', got '{game_state.categorization_result}'"
    )


@then("the card is categorized as an arena-card")
def then_card_is_arena_card(game_state):
    """Assert the card is categorized as an arena-card."""
    assert game_state.categorization_result == "arena", (
        f"Expected 'arena', got '{game_state.categorization_result}'"
    )


@then("the card is categorized as a hero-card")
def then_card_is_hero_card(game_state):
    """Assert the card is categorized as a hero-card."""
    assert game_state.categorization_result == "hero", (
        f"Expected 'hero', got '{game_state.categorization_result}'"
    )


@then("the card is categorized as a token-card")
def then_card_is_token_card(game_state):
    """Assert the card is categorized as a token-card."""
    assert game_state.categorization_result == "token", (
        f"Expected 'token', got '{game_state.categorization_result}'"
    )


@then("the play attempt is allowed by the type restriction")
def then_play_allowed(game_state):
    """Assert the play attempt was allowed."""
    assert game_state.play_result.success, (
        f"Expected play to succeed but got: {getattr(game_state.play_result, 'reason', '')}"
    )


@then("the play attempt is denied because the stack is not empty")
def then_play_denied_stack_not_empty(game_state):
    """Assert the play attempt was denied due to non-empty stack."""
    assert not game_state.play_result.success, (
        "Expected play to fail because the stack is not empty"
    )


@then("the play attempt is denied because it is during combat")
def then_play_denied_during_combat(game_state):
    """Assert the play attempt was denied because it is during combat."""
    assert not game_state.play_result.success, (
        "Expected play to fail because it is during combat"
    )


@then("the play attempt is allowed during the Resolution Step")
def then_play_allowed_resolution_step(game_state):
    """Assert the play attempt was allowed during the Resolution Step."""
    assert game_state.play_result.success, (
        "Expected play to succeed during the Resolution Step"
    )


@then("one action point is required as an additional asset-cost")
def then_action_point_required(game_state):
    """Assert that one action point is required as an additional asset-cost."""
    assert game_state.cost_check.requires_action_point, (
        "Expected action card to require one action point as additional asset-cost"
    )
    assert game_state.cost_check.action_point_amount == 1, (
        f"Expected 1 AP, got {game_state.cost_check.action_point_amount}"
    )


@then("the card is still considered an action card")
def then_still_considered_action(game_state):
    """Assert the card is still considered an action card."""
    assert game_state.play_as_instant_result.card_type == "action", (
        "Expected card to still be considered an action card"
    )


@then("the card does not cost an action point to play")
def then_no_action_point_cost(game_state):
    """Assert the card does not cost an action point when played as an instant."""
    assert not game_state.play_as_instant_result.costs_action_point, (
        "Expected no action point cost when played as instant"
    )


@then("the card can be played any time the player has priority")
def then_playable_any_time(game_state):
    """Assert the card can be played any time the player has priority."""
    assert game_state.play_as_instant_result.can_play_any_time, (
        "Expected card to be playable any time player has priority"
    )


@then("the play attempt is denied because the player does not control the attack")
def then_play_denied_not_attack_controller(game_state):
    """Assert the play was denied because the player does not control the attack."""
    assert not game_state.play_result.success, (
        "Expected play to fail because player does not control the attack"
    )


@then("the attack reaction card is cleared from the game")
def then_attack_reaction_cleared(game_state):
    """Assert the attack reaction card was cleared."""
    assert game_state.layer_processing_result.card_cleared, (
        "Expected attack reaction card to be cleared after resolution"
    )


@then("the card is considered a reaction card")
def then_is_reaction_card(game_state):
    """Assert the card is considered a reaction card."""
    assert game_state.is_reaction_result.is_reaction, (
        "Expected card to be considered a reaction card"
    )


@then("the play attempt is denied because the player's hero is not an attack-target")
def then_play_denied_not_attack_target(game_state):
    """Assert the play was denied because the player's hero is not an attack-target."""
    assert not game_state.play_result.success, (
        "Expected play to fail because player's hero is not an attack-target"
    )


@then("the defense reaction card becomes a defending card on the active chain link")
def then_defense_reaction_becomes_defending(game_state):
    """Assert the defense reaction card became a defending card."""
    assert game_state.layer_processing_result.became_defending_card, (
        "Expected defense reaction to become a defending card on the active chain link"
    )


@then("the equipment is placed in its respective equipment zone")
def then_equipment_placed_in_zone(game_state):
    """Assert the equipment was placed in its equipment zone."""
    assert game_state.equip_result.success, (
        "Expected equipment to be placed in its respective zone"
    )


@then("the declaration is allowed for the equipment permanent")
def then_equipment_can_defend(game_state):
    """Assert the equipment can be declared as a defending card."""
    assert game_state.defend_result.can_defend, (
        "Expected equipment permanent to be allowed as a defending card"
    )


@then("the hero card is a permanent in the player's hero zone")
def then_hero_in_hero_zone(game_state):
    """Assert the hero card starts as a permanent in the hero zone."""
    assert game_state.game_start_result.hero_in_hero_zone, (
        "Expected hero card to be a permanent in the hero zone at game start"
    )


@then("the hero card cannot be included in a player's card-pool")
def then_hero_not_in_card_pool(game_state):
    """Assert the hero card cannot be in a player's card-pool."""
    assert not game_state.hero_card_pool_result, (
        "Expected hero card to be excluded from the card-pool"
    )


@then("the instant can be played at any time the player has priority")
def then_instant_timing_unrestricted(game_state):
    """Assert the instant can be played any time the player has priority."""
    assert game_state.instant_timing_result.unrestricted_timing, (
        "Expected instant to be playable any time the player has priority"
    )


@then("the play attempt is denied because resource cards cannot be played")
def then_resource_cannot_be_played(game_state):
    """Assert the resource card cannot be played."""
    assert not game_state.play_result.success, (
        "Expected resource card play to be denied"
    )


@then("the token can exist in the arena")
def then_token_valid_in_arena(game_state):
    """Assert the token can exist in the arena."""
    assert game_state.token_location_result.valid_in_arena, (
        "Expected token to be valid in the arena"
    )


@then("the token can exist as a sub-card")
def then_token_valid_as_subcard(game_state):
    """Assert the token can exist as a sub-card."""
    assert game_state.token_location_result.valid_as_subcard, (
        "Expected token to be valid as a sub-card"
    )


@then("the token ceases to exist")
def then_token_ceases_to_exist(game_state):
    """Assert the token ceases to exist after leaving the arena."""
    assert game_state.token_leave_result.token_ceased_to_exist, (
        "Expected token to cease to exist when it leaves the arena"
    )


@then("the weapon is placed in its respective weapon zone")
def then_weapon_placed_in_zone(game_state):
    """Assert the weapon was placed in its weapon zone."""
    assert game_state.equip_result.success, (
        "Expected weapon to be placed in its respective zone"
    )


@then("the mentor card is allowed in the card-pool")
def then_mentor_allowed(game_state):
    """Assert the mentor card is allowed in the card-pool."""
    assert game_state.mentor_eligibility.eligible, (
        "Expected mentor card to be allowed with a young hero"
    )


@then("the mentor card is not allowed in the card-pool")
def then_mentor_not_allowed(game_state):
    """Assert the mentor card is not allowed in the card-pool."""
    assert not game_state.mentor_eligibility.eligible, (
        "Expected mentor card to be blocked without a young hero"
    )


@then("the demi-hero is included as part of the player's card-pool")
def then_demi_hero_in_card_pool(game_state):
    """Assert the demi-hero is included in the player's card-pool."""
    assert game_state.demi_hero_classification.in_card_pool, (
        "Expected demi-hero to be included in the player's card-pool"
    )


@then("the demi-hero cannot be used in place of a player's hero at game start")
def then_demi_hero_not_hero_at_start(game_state):
    """Assert the demi-hero cannot replace a player's hero at game start."""
    assert not game_state.demi_hero_classification.can_replace_hero_at_start, (
        "Expected demi-hero to not be usable as a hero replacement at game start"
    )


@then("the demi-hero is considered to be that player's hero")
def then_demi_hero_becomes_hero(game_state):
    """Assert the demi-hero is now considered the player's hero."""
    assert game_state.demi_hero_permanent_result.became_hero, (
        "Expected demi-hero to be considered the player's hero"
    )


@then("the demi-hero has the hero type for the rest of the game")
def then_demi_hero_has_hero_type(game_state):
    """Assert the demi-hero has the hero type for the rest of the game."""
    assert game_state.demi_hero_permanent_result.has_hero_type, (
        "Expected demi-hero to have the hero type for the rest of the game"
    )


@then("the demi-hero is cleared from the arena")
def then_demi_hero_cleared(game_state):
    """Assert the demi-hero was cleared from the arena."""
    assert game_state.demi_hero_permanent_result.cleared_from_arena, (
        "Expected demi-hero to be cleared from the arena"
    )


@then("the play attempt is denied because block cards cannot be played")
def then_block_cannot_be_played(game_state):
    """Assert the block card cannot be played."""
    assert not game_state.play_result.success, (
        "Expected block card play to be denied"
    )


@then("the macro object has the macro type")
def then_macro_has_macro_type(game_state):
    """Assert the macro object has the macro type."""
    assert game_state.macro_type_result.has_macro_type, (
        "Expected macro object to have the macro type"
    )


@then("the card does not have the macro type")
def then_non_macro_no_macro_type(game_state):
    """Assert the non-macro card does not have the macro type."""
    assert not game_state.macro_type_result.has_macro_type, (
        "Expected non-macro card to not have the macro type"
    )


# ===== Fixtures =====

@pytest.fixture
def game_state():
    """
    Fixture providing game state for testing type keywords.

    Uses BDDGameState which integrates with the real engine.
    Reference: Rule 8.1
    """
    from tests.bdd_helpers import BDDGameState

    state = BDDGameState()

    # Default game state values
    state.stack_is_empty = True
    state.stack_has_layers = False
    state.in_combat = False
    state.current_combat_step = None
    state.player_has_priority = True
    state.player_controls_attack = False
    state.player_controls_attack_target_hero = False
    state.player_controls_hero = False
    state.card_in_card_pool = False
    state.start_of_game_procedure = False
    state.token_is_subcard = False
    state.hero_has_young_subtype = False
    state.action_played_as_instant = False
    state.demi_hero_in_arena = False
    state.equipment_in_zone = False
    state.current_card_type = None
    state.player_action_points = 1

    return state
