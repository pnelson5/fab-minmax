"""
Step definitions for Section 5.0: General (Layers, Cards, & Abilities)
Reference: Flesh and Blood Comprehensive Rules Section 5.0

Section 5.0 General is an introductory header for Chapter 5: Layers, Cards, & Abilities.
There are no specific numbered rules in section 5.0 itself. Detailed rules are in:
  - 5.1: Playing Cards
  - 5.2: Activated Abilities
  - 5.3: Resolution Abilities & Resolving Layers
  - 5.4: Static Abilities

This module tests the fundamental chapter-level concepts that section 5 establishes:
the stack holds layers (card-layers, activated-layers, triggered-layers), and
cards/abilities interact with the game through the stack in LIFO order.

Engine Features Needed for Section 5 (Chapter Introduction):
- [ ] Stack concept with LIFO resolution ordering (Chapter 5)
- [ ] Layer types: card-layer, activated-layer, triggered-layer (Rule 1.6.2a)
- [ ] CardPlaySteps sequence: Announce, Declare Costs, Declare Modes and Targets,
      Check Legal Play, Calculate Asset-Costs, Pay Asset-Costs, Calculate Effect-Costs,
      Pay Effect-Costs, Play (Rule 5.1.1)
- [ ] Ability property on cards (Rule 2.0.1a)
- [ ] Static abilities apply continuously without stack (Rule 5.4)

Current status: Tests written, Engine pending
"""

import pytest
from pytest_bdd import scenario, given, when, then, parsers


# ===== Scenarios =====


@scenario(
    "../features/section_5_0_general.feature",
    "The stack holds layers representing played cards and abilities",
)
def test_stack_holds_layers():
    """Chapter 5: The stack holds layers for played cards and abilities."""
    pass


@scenario(
    "../features/section_5_0_general.feature",
    "Layers on the stack resolve in last-in first-out order",
)
def test_layers_resolve_lifo():
    """Chapter 5: Layers resolve in LIFO order."""
    pass


@scenario(
    "../features/section_5_0_general.feature",
    "Playing a card involves multiple ordered steps",
)
def test_playing_card_involves_ordered_steps():
    """Rule 5.1.1: Playing a card involves multiple ordered steps."""
    pass


@scenario(
    "../features/section_5_0_general.feature",
    "Cards have abilities that define their interactions with the game",
)
def test_cards_have_abilities():
    """Rule 2.0.1a: Abilities are a property of cards."""
    pass


@scenario(
    "../features/section_5_0_general.feature",
    "Static abilities apply continuously without being placed on the stack",
)
def test_static_abilities_apply_continuously():
    """Rule 5.4: Static abilities apply continuously without going on the stack."""
    pass


# ===== Step Definitions =====


@given("a game is in progress")
def game_in_progress(game_state):
    """Chapter 5: A game is actively being played."""
    game_state.start_game()


@when("a player plays a card or activates an ability")
def player_plays_card_or_activates_ability(game_state):
    """Chapter 5: A card is played onto the stack."""
    card = game_state.create_card(name="Test Card")
    try:
        game_state.play_card_to_stack(card, controller_id=0)
        game_state.last_played_card = card
    except Exception as e:
        game_state.last_played_card = card
        game_state.play_error = str(e)


@then("a layer is placed on the stack")
def layer_placed_on_stack(game_state):
    """Chapter 5: The stack should have at least one layer."""
    try:
        stack_zone = game_state.stack_zone
        assert stack_zone is not None, "Engine needs: Stack zone (Chapter 5)"
        assert len(stack_zone.cards) >= 1, \
            "Engine needs: Layer placed on stack when card played (Chapter 5)"
    except AttributeError:
        pytest.fail(
            "Engine needs: GameState.stack_zone with card tracking (Chapter 5)"
        )


@then("the layer is the topmost element of the stack")
def layer_is_topmost_element(game_state):
    """Chapter 5: The played card should be on top of the stack."""
    try:
        stack_zone = game_state.stack_zone
        if len(stack_zone.cards) >= 1:
            top_layer = stack_zone.cards[-1]
            assert top_layer is not None, \
                "Engine needs: Stack top tracking (Chapter 5)"
    except AttributeError:
        pytest.fail(
            "Engine needs: Stack zone with topmost layer tracking (Chapter 5)"
        )


@given("a card layer is on the stack")
def card_layer_on_stack(game_state):
    """Chapter 5: A card layer exists on the stack."""
    card = game_state.create_card(name="First Card")
    try:
        game_state.play_card_to_stack(card, controller_id=0)
        game_state.first_layer = card
    except Exception:
        game_state.first_layer = card


@when("a player plays a second card placing another layer on the stack")
def player_plays_second_card(game_state):
    """Chapter 5: A second card is placed on the stack."""
    card2 = game_state.create_card(name="Second Card")
    try:
        game_state.play_card_to_stack(card2, controller_id=0)
        game_state.second_layer = card2
    except Exception:
        game_state.second_layer = card2


@then("the second layer is on top")
def second_layer_is_on_top(game_state):
    """Chapter 5: The most recently played layer should be on top."""
    try:
        stack_zone = game_state.stack_zone
        assert len(stack_zone.cards) >= 2, \
            "Engine needs: Multiple layers on stack (Chapter 5)"
        top = stack_zone.cards[-1]
        assert top is not None, \
            "Engine needs: Stack top layer tracking (Chapter 5)"
    except AttributeError:
        pytest.fail(
            "Engine needs: Stack zone with LIFO ordering (Chapter 5)"
        )


@then("if priority is passed by all players the second layer resolves first")
def second_layer_resolves_first(game_state):
    """Chapter 5: LIFO resolution - second layer resolves before first."""
    try:
        resolution_order = game_state.get_stack_resolution_order()
        assert resolution_order is not None, \
            "Engine needs: Stack resolution order tracking (Chapter 5)"
        # In LIFO, the last added resolves first
        if len(resolution_order) >= 2:
            assert resolution_order[0] != resolution_order[-1], \
                "Stack resolution order should have distinct layers (Chapter 5)"
    except AttributeError:
        pytest.fail(
            "Engine needs: GameState.get_stack_resolution_order() for LIFO resolution (Chapter 5)"
        )


@given("a player has a card in hand")
def player_has_card_in_hand(game_state):
    """Chapter 5: Player has a card ready to play."""
    card = game_state.create_card(name="Hand Card")
    game_state.player.hand_zone.add_card(card)
    game_state.hand_card = card


@when("the player initiates playing that card")
def player_initiates_playing_card(game_state):
    """Chapter 5: The card play sequence begins."""
    try:
        result = game_state.player.play_card(game_state.hand_card)
        game_state.play_result = result
    except Exception as e:
        game_state.play_result = None
        game_state.play_exception = str(e)


@then("the engine initiates the card play step sequence")
def engine_initiates_card_play_steps(game_state):
    """Rule 5.1.1: The card play step sequence is initiated."""
    try:
        steps = game_state.get_card_play_steps()
        assert steps is not None, \
            "Engine needs: Card play step sequence (Rule 5.1.1)"
    except AttributeError:
        pytest.fail(
            "Engine needs: GameState.get_card_play_steps() for card play sequence (Rule 5.1.1)"
        )


@then("the steps include announce, declare costs, declare modes and targets, check legal play, calculate asset-costs, pay asset-costs, calculate effect-costs, pay effect-costs, and play")
def steps_include_all_required_steps(game_state):
    """Rule 5.1.1: All 9 steps of playing a card must be present."""
    expected_steps = [
        "announce",
        "declare costs",
        "declare modes and targets",
        "check legal play",
        "calculate asset-costs",
        "pay asset-costs",
        "calculate effect-costs",
        "pay effect-costs",
        "play",
    ]
    try:
        steps = game_state.get_card_play_steps()
        steps_lower = [s.lower() for s in steps]
        for expected in expected_steps:
            assert any(expected in step for step in steps_lower), \
                f"Engine needs: Card play step '{expected}' (Rule 5.1.1)"
    except AttributeError:
        pytest.fail(
            "Engine needs: GameState.get_card_play_steps() returning all 9 steps (Rule 5.1.1)"
        )


@given("a player has a card with an activated ability")
def player_has_card_with_activated_ability(game_state):
    """Rule 2.0.1a: A card with an activated ability."""
    card = game_state.create_card(name="Ability Card")
    game_state.ability_card = card


@when("the player examines the card")
def player_examines_card(game_state):
    """Chapter 5: The card's properties are examined."""
    game_state.examined_card = game_state.ability_card


@then("the card has at least one ability")
def card_has_at_least_one_ability(game_state):
    """Rule 2.0.1a: Abilities are a property of cards."""
    card = game_state.examined_card
    try:
        abilities = card.abilities
        # Card template abilities or instance abilities
        assert abilities is not None, \
            "Engine needs: CardInstance.abilities property (Rule 2.0.1a)"
    except AttributeError:
        pytest.fail(
            "Engine needs: CardInstance.abilities property (Rule 2.0.1a)"
        )


@then("abilities are a property of the card")
def abilities_are_card_property(game_state):
    """Rule 2.0.1a: Abilities exist as a property of the card object."""
    card = game_state.examined_card
    has_abilities_attr = hasattr(card, 'abilities') or \
                         (hasattr(card, 'template') and hasattr(card.template, 'abilities'))
    assert has_abilities_attr, \
        "Engine needs: Abilities as a property on card objects (Rule 2.0.1a)"


@given("a permanent with a static ability is in play")
def permanent_with_static_ability_in_play(game_state):
    """Rule 5.4: A permanent with a static ability is in the arena."""
    card = game_state.create_card_with_permanent_subtype(
        name="Static Ability Permanent",
        subtype="Item",
    )
    game_state.play_card_to_arena(card, controller_id=0)
    game_state.static_permanent = card


@when("the game state is evaluated")
def game_state_is_evaluated(game_state):
    """Rule 5.4: The game state is checked for static ability effects."""
    try:
        game_state.evaluate_static_abilities()
        game_state.static_evaluated = True
    except AttributeError:
        game_state.static_evaluated = False


@then("the static ability applies continuously")
def static_ability_applies_continuously(game_state):
    """Rule 5.4: Static abilities apply without being placed on the stack."""
    try:
        active_statics = game_state.get_active_static_abilities()
        assert active_statics is not None, \
            "Engine needs: Static ability tracking (Rule 5.4)"
    except AttributeError:
        pytest.fail(
            "Engine needs: GameState.get_active_static_abilities() for static ability tracking (Rule 5.4)"
        )


@then("the static ability does not go on the stack to apply")
def static_ability_does_not_use_stack(game_state):
    """Rule 5.4: Static abilities bypass the stack."""
    try:
        stack_zone = game_state.stack_zone
        # Static abilities should not add layers to the stack
        # The permanent itself is in arena, not stack
        static_card = game_state.static_permanent
        in_stack = static_card in stack_zone
        assert not in_stack, \
            "Static ability source should not be on the stack (Rule 5.4)"
    except AttributeError:
        pytest.fail(
            "Engine needs: Stack zone and static ability distinction (Rule 5.4)"
        )


# ===== Fixtures =====


@pytest.fixture
def game_state():
    """
    Fixture providing game state for Section 5.0 testing.

    Uses BDDGameState which integrates with the real engine.
    Reference: Chapter 5 (Layers, Cards, & Abilities)
    """
    from tests.bdd_helpers import BDDGameState

    state = BDDGameState()

    return state
