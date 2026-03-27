"""
Step definitions for Section 8.3.41: Watery Grave (Ability Keyword)
Reference: Flesh and Blood Comprehensive Rules Section 8.3.41

This module implements behavioral tests for the Watery Grave ability keyword:
- Watery Grave is a triggered-static ability (Rule 8.3.41)
- Watery Grave means "When this is put into your graveyard from the arena, turn it face-down"
  (Rule 8.3.41)
- The ability only triggers when the card moves specifically from the arena to the graveyard
  (Rule 8.3.41)
- Cards moving from hand or deck to graveyard do NOT trigger Watery Grave (Rule 8.3.41)
- Cards without Watery Grave are not turned face-down (Rule 8.3.41)

Engine Features Needed for Section 8.3.41:
- [ ] AbilityKeyword.WATERY_GRAVE triggered-static ability on cards (Rule 8.3.41)
- [ ] WateryGraveAbility.is_triggered_static -> True (Rule 8.3.41)
- [ ] WateryGraveAbility.meaning == "When this is put into your graveyard from the arena, turn it face-down" (Rule 8.3.41)
- [ ] CardInstance.is_face_down property tracking face orientation (Rule 8.3.41)
- [ ] ZoneTransitionHandler: when card with Watery Grave moves arena->graveyard, set face-down (Rule 8.3.41)
- [ ] ZoneTransitionHandler: when card with Watery Grave moves hand/deck->graveyard, do NOT set face-down (Rule 8.3.41)

Current status: Tests written, Engine pending
"""

import pytest
from pytest_bdd import scenario, given, when, then, parsers


# ===== Rule 8.3.41: Watery Grave is a triggered-static ability =====

@scenario(
    "../features/section_8_3_41_watery_grave.feature",
    "Watery Grave is a triggered-static ability",
)
def test_watery_grave_is_triggered_static_ability():
    """Rule 8.3.41: Watery Grave is a triggered-static ability."""
    pass


# ===== Rule 8.3.41: Card turned face-down when moved from arena to graveyard =====

@scenario(
    "../features/section_8_3_41_watery_grave.feature",
    "A card with Watery Grave is turned face-down when put into the graveyard from the arena",
)
def test_watery_grave_card_turned_face_down_from_arena():
    """Rule 8.3.41: A Watery Grave card is face-down in the graveyard after leaving the arena."""
    pass


# ===== Rule 8.3.41: Watery Grave does not trigger from hand =====

@scenario(
    "../features/section_8_3_41_watery_grave.feature",
    "A card with Watery Grave going to graveyard from hand is not turned face-down",
)
def test_watery_grave_does_not_trigger_from_hand():
    """Rule 8.3.41: Watery Grave only triggers from arena, not from hand."""
    pass


# ===== Rule 8.3.41: Watery Grave does not trigger from deck =====

@scenario(
    "../features/section_8_3_41_watery_grave.feature",
    "A card with Watery Grave going to graveyard from deck is not turned face-down",
)
def test_watery_grave_does_not_trigger_from_deck():
    """Rule 8.3.41: Watery Grave only triggers from arena, not from deck."""
    pass


# ===== Rule 8.3.41: Cards without Watery Grave not turned face-down =====

@scenario(
    "../features/section_8_3_41_watery_grave.feature",
    "A card without Watery Grave going to graveyard from arena is not turned face-down",
)
def test_non_watery_grave_card_not_turned_face_down():
    """Rule 8.3.41: Only cards with Watery Grave are turned face-down."""
    pass


# ===== Rule 8.3.41: Watery Grave triggers on own graveyard =====

@scenario(
    "../features/section_8_3_41_watery_grave.feature",
    "Watery Grave triggers when moved to the controlling player's own graveyard",
)
def test_watery_grave_triggers_on_own_graveyard():
    """Rule 8.3.41: Watery Grave triggers when moved to the controlling player's graveyard."""
    pass


# ===== Step Definitions =====

# ---- Given steps ----

@given('a card has the "Watery Grave" keyword')
def card_with_watery_grave(game_state):
    """Rule 8.3.41: Create a card that has the Watery Grave keyword."""
    card = game_state.create_card(name="Watery Grave Test Card")
    card._has_watery_grave = True
    game_state.test_card = card


@given('a card with the "Watery Grave" keyword is in the arena')
def watery_grave_card_in_arena(game_state):
    """Rule 8.3.41: Place a Watery Grave card in the arena."""
    card = game_state.create_card(name="Watery Grave Card")
    card._has_watery_grave = True
    card._is_face_down = False
    game_state.play_card_to_arena(card)
    game_state.test_card = card


@given('a card with the "Watery Grave" keyword is in the hand')
def watery_grave_card_in_hand(game_state):
    """Rule 8.3.41: Place a Watery Grave card in the hand."""
    card = game_state.create_card(name="Watery Grave Card")
    card._has_watery_grave = True
    card._is_face_down = False
    game_state.player.hand.add_card(card)
    game_state.test_card = card


@given('a card with the "Watery Grave" keyword is in the deck')
def watery_grave_card_in_deck(game_state):
    """Rule 8.3.41: Place a Watery Grave card in the deck."""
    card = game_state.create_card(name="Watery Grave Card")
    card._has_watery_grave = True
    card._is_face_down = False
    game_state.player.deck_zone.add_card(card)
    game_state.test_card = card


@given('a card without the "Watery Grave" keyword is in the arena')
def non_watery_grave_card_in_arena(game_state):
    """Rule 8.3.41: Place a non-Watery Grave card in the arena."""
    card = game_state.create_card(name="Normal Card")
    card._has_watery_grave = False
    card._is_face_down = False
    game_state.play_card_to_arena(card)
    game_state.test_card = card


# ---- When steps ----

@when("I inspect the Watery Grave ability on the card")
def inspect_watery_grave_ability(game_state):
    """Rule 8.3.41: Inspect the Watery Grave ability on the card."""
    game_state.inspected_ability = game_state.get_watery_grave_ability(
        game_state.test_card
    )


@when("the card is put into the graveyard from the arena")
def card_put_into_graveyard_from_arena(game_state):
    """Rule 8.3.41: Move the card from the arena to the graveyard."""
    game_state.zone_transition_result = game_state.move_card_to_graveyard(
        game_state.test_card,
        source_zone="arena",
    )


@when("the card is put into the graveyard from the hand")
def card_put_into_graveyard_from_hand(game_state):
    """Rule 8.3.41: Move the card from the hand to the graveyard."""
    game_state.zone_transition_result = game_state.move_card_to_graveyard(
        game_state.test_card,
        source_zone="hand",
    )


@when("the card is put into the graveyard from the deck")
def card_put_into_graveyard_from_deck(game_state):
    """Rule 8.3.41: Move the card from the deck to the graveyard."""
    game_state.zone_transition_result = game_state.move_card_to_graveyard(
        game_state.test_card,
        source_zone="deck",
    )


@when("the card is put into its owner's graveyard from the arena")
def card_put_into_owners_graveyard_from_arena(game_state):
    """Rule 8.3.41: Move the card from the arena to the owner's graveyard."""
    game_state.zone_transition_result = game_state.move_card_to_graveyard(
        game_state.test_card,
        source_zone="arena",
        owner_id=0,
    )


# ---- Then steps ----

@then("the Watery Grave ability is a triggered-static ability")
def watery_grave_is_triggered_static(game_state):
    """Rule 8.3.41: Watery Grave must be a triggered-static ability."""
    ability = game_state.inspected_ability
    assert ability is not None, "Card should have a Watery Grave ability"
    is_triggered_static = getattr(ability, "is_triggered_static", None)
    assert is_triggered_static is True, (
        f"Watery Grave should be a triggered-static ability (Rule 8.3.41), "
        f"got: {is_triggered_static}"
    )


@then('the Watery Grave ability means "When this is put into your graveyard from the arena, turn it face-down"')
def watery_grave_meaning_is_correct(game_state):
    """Rule 8.3.41: Watery Grave means 'When this is put into your graveyard from the arena, turn it face-down'."""
    ability = game_state.inspected_ability
    meaning = getattr(ability, "meaning", None)
    assert meaning == "When this is put into your graveyard from the arena, turn it face-down", (
        f"Watery Grave meaning should be 'When this is put into your graveyard from the arena, "
        f"turn it face-down' (Rule 8.3.41), got: {meaning}"
    )


@then("the card is face-down in the graveyard")
def card_is_face_down_in_graveyard(game_state):
    """Rule 8.3.41: The card should be face-down after Watery Grave triggers."""
    card = game_state.test_card
    is_face_down = getattr(card, "is_face_down", None)
    if is_face_down is None:
        is_face_down = getattr(card, "_is_face_down", None)
    assert is_face_down is True, (
        f"Card with Watery Grave should be face-down in the graveyard after moving from arena "
        f"(Rule 8.3.41), got is_face_down={is_face_down}"
    )
    # Also verify the card is actually in the graveyard
    assert card in game_state.player.graveyard, (
        "Card should be in the graveyard after the zone transition (Rule 8.3.41)"
    )


@then("the card is face-up in the graveyard")
def card_is_face_up_in_graveyard(game_state):
    """Rule 8.3.41: The card should remain face-up when Watery Grave does not trigger."""
    card = game_state.test_card
    is_face_down = getattr(card, "is_face_down", None)
    if is_face_down is None:
        is_face_down = getattr(card, "_is_face_down", None)
    assert is_face_down is False or is_face_down is None, (
        f"Card should remain face-up in the graveyard when Watery Grave does not trigger "
        f"(Rule 8.3.41), got is_face_down={is_face_down}"
    )
    # Also verify the card is actually in the graveyard
    assert card in game_state.player.graveyard, (
        "Card should be in the graveyard after the zone transition (Rule 8.3.41)"
    )


# ===== Fixtures =====

@pytest.fixture
def game_state():
    """
    Fixture providing game state for testing Watery Grave (Rule 8.3.41).

    Uses BDDGameState which integrates with the real engine.
    Reference: Rule 8.3.41
    """
    from tests.bdd_helpers import BDDGameState

    state = BDDGameState()
    return state
