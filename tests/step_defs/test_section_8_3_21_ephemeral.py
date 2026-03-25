"""
Step definitions for Section 8.3.21: Ephemeral (Ability Keyword)
Reference: Flesh and Blood Comprehensive Rules Section 8.3.21

This module implements behavioral tests for the Ephemeral ability keyword:
- Ephemeral is a meta-static ability AND a static ability (Rule 8.3.21)
- Meta-static part: "You can't start the game with this in your deck." (Rule 8.3.21)
- Static part: "If this would be put into a graveyard from anywhere, instead it
  ceases to exist." (Rule 8.3.21)
- A player cannot include a card with Ephemeral in their card-pool (Rule 8.3.21a)
- A card that ceases to exist from Ephemeral is removed from the game (Rule 8.3.21b)
- A removed-from-game card has no further interaction with rules and effects (Rule 8.3.21b)

Engine Features Needed for Section 8.3.21:
- [ ] EphemeralAbility class as both meta-static and static ability (Rule 8.3.21)
- [ ] EphemeralAbility.is_meta_static -> True (Rule 8.3.21)
- [ ] EphemeralAbility.is_static -> True (Rule 8.3.21)
- [ ] EphemeralAbility.meta_static_meaning: "You can't start the game with this in your deck."
- [ ] EphemeralAbility.static_meaning: "If this would be put into a graveyard from anywhere, instead it ceases to exist."
- [ ] CardTemplate.has_ephemeral property or keyword check (Rule 8.3.21)
- [ ] Card-pool validation that rejects cards with Ephemeral (Rule 8.3.21a)
- [ ] Replacement effect: when Ephemeral card would go to graveyard, cease to exist (Rule 8.3.21)
- [ ] "Ceases to exist" zone — removal from game tracking (Rule 8.3.21b)
- [ ] Removed-from-game cards have no further game interaction (Rule 8.3.21b)

Current status: Tests written, Engine pending
"""

import pytest
from pytest_bdd import scenario, given, when, then, parsers


# ===== Rule 8.3.21: Ephemeral is both meta-static and static =====

@scenario(
    "../features/section_8_3_21_ephemeral.feature",
    "Ephemeral is a meta-static ability",
)
def test_ephemeral_is_meta_static():
    """Rule 8.3.21: Ephemeral must be a meta-static ability."""
    pass


@scenario(
    "../features/section_8_3_21_ephemeral.feature",
    "Ephemeral is also a static ability",
)
def test_ephemeral_is_static():
    """Rule 8.3.21: Ephemeral must also be a static ability."""
    pass


# ===== Rule 8.3.21: Ephemeral meanings =====

@scenario(
    "../features/section_8_3_21_ephemeral.feature",
    "Ephemeral meta-static meaning is cannot start in deck",
)
def test_ephemeral_meta_static_meaning():
    """Rule 8.3.21: Ephemeral meta-static meaning is the cannot-start-in-deck text."""
    pass


@scenario(
    "../features/section_8_3_21_ephemeral.feature",
    "Ephemeral static meaning is ceases to exist instead of going to graveyard",
)
def test_ephemeral_static_meaning():
    """Rule 8.3.21: Ephemeral static meaning is the ceases-to-exist text."""
    pass


# ===== Rule 8.3.21a: Cannot be included in card-pool =====

@scenario(
    "../features/section_8_3_21_ephemeral.feature",
    "A card with Ephemeral cannot be included in a player's card-pool",
)
def test_ephemeral_card_cannot_be_in_card_pool():
    """Rule 8.3.21a: A player cannot include a card with Ephemeral in their card-pool."""
    pass


@scenario(
    "../features/section_8_3_21_ephemeral.feature",
    "A card without Ephemeral can be included in a player's card-pool",
)
def test_non_ephemeral_card_can_be_in_card_pool():
    """Rule 8.3.21a: A card without Ephemeral can be included in a card-pool."""
    pass


# ===== Rule 8.3.21: Ceases to exist instead of going to graveyard =====

@scenario(
    "../features/section_8_3_21_ephemeral.feature",
    "An Ephemeral card ceases to exist instead of going to graveyard",
)
def test_ephemeral_ceases_to_exist_from_play():
    """Rule 8.3.21: Ephemeral card ceases to exist instead of entering graveyard."""
    pass


@scenario(
    "../features/section_8_3_21_ephemeral.feature",
    "An Ephemeral card ceases to exist when moved from hand to graveyard",
)
def test_ephemeral_ceases_to_exist_from_hand():
    """Rule 8.3.21: Ephemeral ceases-to-exist applies from anywhere, including hand."""
    pass


# ===== Rule 8.3.21b: Removed from the game =====

@scenario(
    "../features/section_8_3_21_ephemeral.feature",
    "An Ephemeral card that ceases to exist is removed from the game",
)
def test_ephemeral_card_is_removed_from_game():
    """Rule 8.3.21b: A card that ceases to exist from Ephemeral is removed from game."""
    pass


@scenario(
    "../features/section_8_3_21_ephemeral.feature",
    "A card removed from game via Ephemeral has no further interaction with game rules",
)
def test_removed_from_game_has_no_interaction():
    """Rule 8.3.21b: A removed-from-game card has no further interaction with rules/effects."""
    pass


# ===== Step Definitions =====

@given("a card with Ephemeral ability")
def ephemeral_card(game_state):
    """Create a card with the Ephemeral ability keyword (Rule 8.3.21)."""
    card = game_state.create_card(name="Ephemeral Test Card")
    game_state.ephemeral_card = card
    game_state.ephemeral_ability = None

    # Attempt to get Ephemeral ability from engine
    try:
        from fab_engine.keywords.ephemeral import EphemeralAbility
        ability = EphemeralAbility()
        game_state.ephemeral_ability = ability
        if hasattr(card, "add_ability"):
            card.add_ability(ability)
        elif hasattr(card.template, "add_keyword"):
            card.template.add_keyword("Ephemeral")
        elif hasattr(card.template, "keywords"):
            card.template.keywords.append("Ephemeral")
    except (ImportError, AttributeError):
        # Engine not yet implemented — EphemeralAbility class missing
        game_state.ephemeral_ability = None

    game_state.test_card_has_ephemeral = True


@given("a card without Ephemeral ability")
def non_ephemeral_card(game_state):
    """Create a card without Ephemeral ability (Rule 8.3.21a)."""
    card = game_state.create_card(name="Normal Test Card")
    game_state.ephemeral_card = card
    game_state.test_card_has_ephemeral = False


@given("a card with Ephemeral ability is in play")
def ephemeral_card_in_play(game_state):
    """Set up an Ephemeral card in the arena (Rule 8.3.21)."""
    card = game_state.create_card(name="Ephemeral In Play")
    game_state.ephemeral_card = card
    game_state.test_card_has_ephemeral = True

    try:
        from fab_engine.keywords.ephemeral import EphemeralAbility
        ability = EphemeralAbility()
        game_state.ephemeral_ability = ability
    except ImportError:
        game_state.ephemeral_ability = None

    # Place card in arena
    game_state.player.arena.add_card(card)


@given("a card with Ephemeral ability is in a player's hand")
def ephemeral_card_in_hand(game_state):
    """Set up an Ephemeral card in hand (Rule 8.3.21 — from anywhere)."""
    card = game_state.create_card(name="Ephemeral In Hand")
    game_state.ephemeral_card = card
    game_state.test_card_has_ephemeral = True

    try:
        from fab_engine.keywords.ephemeral import EphemeralAbility
        ability = EphemeralAbility()
        game_state.ephemeral_ability = ability
    except ImportError:
        game_state.ephemeral_ability = None

    game_state.player.hand.add_card(card)


@given("a card with Ephemeral ability has ceased to exist")
def ephemeral_card_ceased_to_exist(game_state):
    """Set up an Ephemeral card that has already ceased to exist (Rule 8.3.21b)."""
    card = game_state.create_card(name="Ephemeral Ceased Card")
    game_state.ceased_card = card

    # Attempt to trigger cease-to-exist
    try:
        from fab_engine.keywords.ephemeral import EphemeralAbility, EphemeralCeaseResult
        ability = EphemeralAbility()
        result = ability.apply_cease_to_exist(card)
        game_state.ephemeral_result = result
        game_state.cease_succeeded = True
    except (ImportError, AttributeError):
        # Engine not implemented — record that we attempted cessation
        game_state.ephemeral_result = None
        game_state.cease_succeeded = False


@when("I inspect the Ephemeral ability")
def inspect_ephemeral_ability(game_state):
    """Inspect the Ephemeral ability object (Rule 8.3.21)."""
    # Already captured in given step; nothing extra needed
    pass


@when("I check if the card can be included in a card-pool")
def check_card_pool_inclusion(game_state):
    """Check if the card is valid for card-pool inclusion (Rule 8.3.21a)."""
    card = game_state.ephemeral_card

    try:
        from fab_engine.deck.validation import can_include_in_card_pool
        game_state.card_pool_check = can_include_in_card_pool(card)
    except (ImportError, AttributeError):
        # Fallback to game_state helper
        game_state.card_pool_check = game_state.is_valid_for_card_pool(card)


@when("the card would be put into the graveyard")
def card_goes_to_graveyard(game_state):
    """Trigger putting the Ephemeral card into the graveyard (Rule 8.3.21)."""
    card = game_state.ephemeral_card

    try:
        from fab_engine.zones.transitions import move_to_graveyard
        result = move_to_graveyard(card, game_state.player)
        game_state.graveyard_move_result = result
    except (ImportError, AttributeError):
        # Engine not implemented — record attempt
        game_state.graveyard_move_result = None


@when("the card would be put into the graveyard from hand")
def card_goes_to_graveyard_from_hand(game_state):
    """Trigger putting the Ephemeral card into the graveyard from hand (Rule 8.3.21)."""
    card = game_state.ephemeral_card

    try:
        from fab_engine.zones.transitions import move_to_graveyard
        result = move_to_graveyard(card, game_state.player, source_zone="hand")
        game_state.graveyard_move_result = result
    except (ImportError, AttributeError):
        game_state.graveyard_move_result = None


@when("the card ceases to exist via Ephemeral")
def card_ceases_to_exist(game_state):
    """The Ephemeral replacement effect triggers cessation (Rule 8.3.21b)."""
    # This step follows the graveyard move; engine should have already applied Ephemeral
    card = game_state.ephemeral_card

    try:
        from fab_engine.keywords.ephemeral import EphemeralAbility
        ability = EphemeralAbility()
        result = ability.apply_cease_to_exist(card)
        game_state.ephemeral_result = result
    except (ImportError, AttributeError):
        game_state.ephemeral_result = None


@when("I check if the removed card can interact with game rules")
def check_removed_card_interaction(game_state):
    """Check that a ceased card has no further game interaction (Rule 8.3.21b)."""
    card = game_state.ceased_card

    try:
        from fab_engine.game.removed_from_game import can_interact_with_game
        game_state.removed_card_interaction = can_interact_with_game(card)
    except (ImportError, AttributeError):
        game_state.removed_card_interaction = None


# ===== THEN steps =====

@then("the Ephemeral ability is a meta-static ability")
def assert_ephemeral_is_meta_static(game_state):
    """Rule 8.3.21: Ephemeral must be a meta-static ability."""
    ability = game_state.ephemeral_ability
    assert ability is not None, (
        "Engine Feature Needed: EphemeralAbility class not yet implemented "
        "(fab_engine.keywords.ephemeral.EphemeralAbility)"
    )
    assert getattr(ability, "is_meta_static", False), (
        "Engine Feature Needed: EphemeralAbility.is_meta_static must be True "
        "(Rule 8.3.21)"
    )


@then("the Ephemeral ability is also a static ability")
def assert_ephemeral_is_static(game_state):
    """Rule 8.3.21: Ephemeral must also be a static ability."""
    ability = game_state.ephemeral_ability
    assert ability is not None, (
        "Engine Feature Needed: EphemeralAbility class not yet implemented"
    )
    assert getattr(ability, "is_static", False), (
        "Engine Feature Needed: EphemeralAbility.is_static must be True "
        "(Rule 8.3.21)"
    )


@then('the Ephemeral meta-static meaning is "You can\'t start the game with this in your deck."')
def assert_ephemeral_meta_static_meaning(game_state):
    """Rule 8.3.21: Ephemeral meta-static meaning text is correct."""
    ability = game_state.ephemeral_ability
    assert ability is not None, (
        "Engine Feature Needed: EphemeralAbility class not yet implemented"
    )
    expected = "You can't start the game with this in your deck."
    actual = getattr(ability, "meta_static_meaning", None)
    assert actual == expected, (
        f"Engine Feature Needed: EphemeralAbility.meta_static_meaning must be "
        f"'{expected}', got '{actual}' (Rule 8.3.21)"
    )


@then('the Ephemeral static meaning is "If this would be put into a graveyard from anywhere, instead it ceases to exist."')
def assert_ephemeral_static_meaning(game_state):
    """Rule 8.3.21: Ephemeral static meaning text is correct."""
    ability = game_state.ephemeral_ability
    assert ability is not None, (
        "Engine Feature Needed: EphemeralAbility class not yet implemented"
    )
    expected = "If this would be put into a graveyard from anywhere, instead it ceases to exist."
    actual = getattr(ability, "static_meaning", None)
    assert actual == expected, (
        f"Engine Feature Needed: EphemeralAbility.static_meaning must be "
        f"'{expected}', got '{actual}' (Rule 8.3.21)"
    )


@then("the card cannot be included in the card-pool")
def assert_cannot_be_in_card_pool(game_state):
    """Rule 8.3.21a: A card with Ephemeral cannot be included in a card-pool."""
    result = game_state.card_pool_check
    assert result is not None, (
        "Engine Feature Needed: Card-pool validation not yet implemented "
        "(fab_engine.deck.validation.can_include_in_card_pool or "
        "BDDGameState.is_valid_for_card_pool must handle Ephemeral keyword) "
        "(Rule 8.3.21a)"
    )
    assert result is False, (
        "Engine Feature Needed: Cards with Ephemeral keyword must be rejected from "
        "card-pool (Rule 8.3.21a)"
    )


@then("the card can be included in the card-pool")
def assert_can_be_in_card_pool(game_state):
    """Rule 8.3.21a: A card without Ephemeral can be included in a card-pool."""
    result = game_state.card_pool_check
    # A normal card should be valid for card-pool; this may pass even before full engine
    assert result is not False, (
        "Engine Bug: A card without Ephemeral should be valid for the card-pool "
        "(Rule 8.3.21a)"
    )


@then("the card ceases to exist instead of going to graveyard")
def assert_card_ceases_to_exist(game_state):
    """Rule 8.3.21: Ephemeral card ceases to exist instead of going to graveyard."""
    result = game_state.graveyard_move_result
    assert result is not None, (
        "Engine Feature Needed: Zone transition system not yet implemented "
        "(fab_engine.zones.transitions.move_to_graveyard) (Rule 8.3.21)"
    )
    # The result should indicate the card ceased to exist, not entered the graveyard
    ceased = getattr(result, "ceased_to_exist", None)
    assert ceased is True, (
        "Engine Feature Needed: When an Ephemeral card would go to graveyard, "
        "it must cease to exist instead. "
        "Expected result.ceased_to_exist == True (Rule 8.3.21)"
    )


@then("the graveyard does not contain the Ephemeral card")
def assert_graveyard_does_not_contain_ephemeral(game_state):
    """Rule 8.3.21: Ephemeral card must not be in graveyard after cessation."""
    result = game_state.graveyard_move_result
    assert result is not None, (
        "Engine Feature Needed: Zone transition system not yet implemented "
        "(fab_engine.zones.transitions.move_to_graveyard) (Rule 8.3.21)"
    )
    # The result should confirm the card did not enter the graveyard
    entered_graveyard = getattr(result, "entered_graveyard", None)
    assert entered_graveyard is False, (
        "Engine Feature Needed: Ephemeral card must not enter graveyard — "
        "it ceases to exist instead. Expected result.entered_graveyard == False (Rule 8.3.21)"
    )


@then("the card is removed from the game")
def assert_card_removed_from_game(game_state):
    """Rule 8.3.21b: A card that ceases to exist via Ephemeral is removed from game."""
    result = game_state.ephemeral_result
    assert result is not None, (
        "Engine Feature Needed: EphemeralAbility.apply_cease_to_exist() not implemented "
        "(Rule 8.3.21b)"
    )
    removed = getattr(result, "removed_from_game", None)
    assert removed is True, (
        "Engine Feature Needed: A card that ceases to exist via Ephemeral must be "
        "removed from the game. Expected result.removed_from_game == True (Rule 8.3.21b)"
    )


@then("the removed card has no further interaction with rules and effects")
def assert_no_further_interaction(game_state):
    """Rule 8.3.21b: A removed-from-game card has no further interaction."""
    interaction = game_state.removed_card_interaction
    assert interaction is not None, (
        "Engine Feature Needed: fab_engine.game.removed_from_game.can_interact_with_game() "
        "not yet implemented (Rule 8.3.21b)"
    )
    assert interaction is False, (
        "Engine Feature Needed: A card removed from game via Ephemeral must have "
        "no further interaction with rules and effects. "
        "Expected can_interact_with_game(card) == False (Rule 8.3.21b)"
    )


# ===== Fixture =====

@pytest.fixture
def game_state():
    """
    Fixture providing game state for testing.

    Uses BDDGameState which integrates with the real engine.
    Reference: Rule 8.3.21 - Ephemeral
    """
    from tests.bdd_helpers import BDDGameState

    state = BDDGameState()

    # Attributes populated by given/when/then steps
    state.ephemeral_card = None
    state.ephemeral_ability = None
    state.test_card_has_ephemeral = False
    state.card_pool_check = None
    state.graveyard_move_result = None
    state.ephemeral_result = None
    state.ceased_card = None
    state.cease_succeeded = False
    state.removed_card_interaction = None

    return state
