"""
Step definitions for Section 8.3.6: Legendary (Ability Keyword)
Reference: Flesh and Blood Comprehensive Rules Section 8.3.6

This module implements behavioral tests for the Legendary ability keyword:
- Legendary is a meta-static ability (Rule 8.3.6)
- Legendary means "You may only have 1 of this in your constructed deck" (Rule 8.3.6)
- A deck may contain at most 1 copy of any Legendary card (Rule 8.3.6)
- Non-Legendary cards are not restricted to 1 copy by this rule (Rule 8.3.6)

Engine Features Needed for Section 8.3.6:
- [ ] AbilityKeyword.LEGENDARY meta-static ability on cards (Rule 8.3.6)
- [ ] LegendaryAbility.is_meta_static -> True (Rule 8.3.6)
- [ ] LegendaryAbility.meaning == "You may only have 1 of this in your constructed deck" (Rule 8.3.6)
- [ ] DeckValidator.validate_legendary(deck) enforces at most 1 copy per Legendary card (Rule 8.3.6)
- [ ] DeckValidationError includes details about which Legendary card violated the rule (Rule 8.3.6)

Current status: Tests written, Engine pending
"""

import pytest
from pytest_bdd import scenario, given, when, then, parsers


# ===== Rule 8.3.6: Legendary is a meta-static ability =====

@scenario(
    "../features/section_8_3_6_legendary.feature",
    "Legendary is a meta-static ability",
)
def test_legendary_is_meta_static_ability():
    """Rule 8.3.6: Legendary is a meta-static ability."""
    pass


# ===== Rule 8.3.6: Deck validation — 1 copy valid =====

@scenario(
    "../features/section_8_3_6_legendary.feature",
    "A deck with exactly 1 copy of a Legendary card is valid",
)
def test_one_legendary_copy_is_valid():
    """Rule 8.3.6: A single copy of a Legendary card satisfies the Legendary restriction."""
    pass


# ===== Rule 8.3.6: Deck validation — 2 copies invalid =====

@scenario(
    "../features/section_8_3_6_legendary.feature",
    "A deck with 2 copies of a Legendary card is invalid",
)
def test_two_legendary_copies_is_invalid():
    """Rule 8.3.6: Two copies of a Legendary card violates the Legendary restriction."""
    pass


# ===== Rule 8.3.6: Deck validation — 3 copies invalid =====

@scenario(
    "../features/section_8_3_6_legendary.feature",
    "A deck with 3 copies of a Legendary card is invalid",
)
def test_three_legendary_copies_is_invalid():
    """Rule 8.3.6: Three copies of a Legendary card violates the Legendary restriction."""
    pass


# ===== Rule 8.3.6: Non-Legendary card is not subject to limit-of-1 =====

@scenario(
    "../features/section_8_3_6_legendary.feature",
    "A non-Legendary card is not restricted to 1 copy",
)
def test_non_legendary_card_not_restricted_to_one_copy():
    """Rule 8.3.6: Non-Legendary cards follow normal copy limits, not Legendary's limit-of-1."""
    pass


# ===== Rule 8.3.6: Multiple distinct Legendary cards each allowed once =====

@scenario(
    "../features/section_8_3_6_legendary.feature",
    "A deck may contain 1 copy each of multiple different Legendary cards",
)
def test_multiple_different_legendary_cards_each_one_copy_is_valid():
    """Rule 8.3.6: Each Legendary card may appear once; different Legendary cards don't conflict."""
    pass


# ===== Step Definitions =====

# ---- Given steps ----

@given('a card has the "Legendary" keyword')
def card_with_legendary(game_state):
    """Rule 8.3.6: Create a card that has the Legendary keyword."""
    card = game_state.create_card(name="Legendary Test Card")
    card._has_legendary = True
    game_state.legendary_card = card


@given("a constructed deck")
def empty_constructed_deck(game_state):
    """Rule 8.3.6: Create an empty constructed deck for validation tests."""
    game_state.test_deck = game_state.create_deck()


@given(parsers.parse('the deck contains exactly 1 copy of a card named "{card_name}" with the Legendary keyword'))
def deck_contains_one_legendary(game_state, card_name):
    """Rule 8.3.6: Add exactly 1 copy of a Legendary card to the deck."""
    card = game_state.create_card(name=card_name)
    card._has_legendary = True
    game_state.test_deck_legendary_card_name = card_name
    game_state.add_cards_to_deck(game_state.test_deck, card, count=1)


@given(parsers.parse('the deck contains {count:d} copies of a card named "{card_name}" with the Legendary keyword'))
def deck_contains_n_legendary_copies(game_state, count, card_name):
    """Rule 8.3.6: Add N copies of a Legendary card to the deck."""
    card = game_state.create_card(name=card_name)
    card._has_legendary = True
    game_state.test_deck_legendary_card_name = card_name
    game_state.add_cards_to_deck(game_state.test_deck, card, count=count)


@given(parsers.parse('the deck contains {count:d} copies of a card named "{card_name}" without the Legendary keyword'))
def deck_contains_n_non_legendary_copies(game_state, count, card_name):
    """Rule 8.3.6: Add N copies of a non-Legendary card to the deck."""
    card = game_state.create_card(name=card_name)
    card._has_legendary = False
    game_state.test_deck_normal_card_name = card_name
    game_state.add_cards_to_deck(game_state.test_deck, card, count=count)


@given(parsers.parse('the deck contains 1 copy of a card named "{card_name}" with the Legendary keyword'))
def deck_contains_one_named_legendary(game_state, card_name):
    """Rule 8.3.6: Add exactly 1 copy of a named Legendary card to the deck."""
    card = game_state.create_card(name=card_name)
    card._has_legendary = True
    if not hasattr(game_state, "test_deck_legendary_card_names"):
        game_state.test_deck_legendary_card_names = []
    game_state.test_deck_legendary_card_names.append(card_name)
    game_state.add_cards_to_deck(game_state.test_deck, card, count=1)


# ---- When steps ----

@when("I inspect the Legendary ability on the card")
def inspect_legendary_ability(game_state):
    """Rule 8.3.6: Inspect the Legendary ability on the card."""
    game_state.inspected_ability = game_state.get_legendary_ability(
        game_state.legendary_card
    )


@when("the deck is validated for constructed play")
def validate_deck_for_constructed(game_state):
    """Rule 8.3.6: Validate the deck for constructed play (checks Legendary restrictions)."""
    game_state.validation_result = game_state.validate_deck_for_constructed(
        game_state.test_deck
    )


# ---- Then steps ----

@then("the Legendary ability is a meta-static ability")
def legendary_is_meta_static(game_state):
    """Rule 8.3.6: Legendary must be a meta-static ability."""
    ability = game_state.inspected_ability
    assert ability is not None, "Card should have a Legendary ability"
    is_meta_static = getattr(ability, "is_meta_static", None)
    assert is_meta_static is True, (
        f"Legendary should be a meta-static ability (Rule 8.3.6), got: {is_meta_static}"
    )


@then('the Legendary ability means "You may only have 1 of this in your constructed deck"')
def legendary_meaning_is_correct(game_state):
    """Rule 8.3.6: Legendary means 'You may only have 1 of this in your constructed deck'."""
    ability = game_state.inspected_ability
    meaning = getattr(ability, "meaning", None)
    assert meaning == "You may only have 1 of this in your constructed deck", (
        f"Legendary meaning should be 'You may only have 1 of this in your constructed deck' "
        f"(Rule 8.3.6), got: {meaning}"
    )


@then("the deck is valid with respect to the Legendary card")
def deck_valid_for_legendary(game_state):
    """Rule 8.3.6: A deck with 1 copy of a Legendary card satisfies the Legendary restriction."""
    result = game_state.validation_result
    assert result is not None, "validate_deck_for_constructed should return a result"
    is_valid = getattr(result, "is_valid", None)
    assert is_valid is True, (
        f"Deck with 1 copy of a Legendary card should be valid (Rule 8.3.6), got is_valid={is_valid}"
    )


@then("the deck is invalid")
def deck_is_invalid(game_state):
    """Rule 8.3.6: Deck with 2+ copies of a Legendary card is invalid."""
    result = game_state.validation_result
    assert result is not None, "validate_deck_for_constructed should return a result"
    is_valid = getattr(result, "is_valid", None)
    assert is_valid is False, (
        f"Deck with 2+ copies of a Legendary card should be invalid (Rule 8.3.6), got is_valid={is_valid}"
    )


@then("the validation error mentions the Legendary restriction")
def validation_error_mentions_legendary(game_state):
    """Rule 8.3.6: The validation error should reference the Legendary keyword."""
    result = game_state.validation_result
    errors = getattr(result, "errors", [])
    assert errors, "Validation result should have error messages when deck is invalid"
    # At least one error should mention the Legendary restriction
    legendary_mentioned = any(
        "legendary" in str(e).lower() or "Legendary" in str(e)
        for e in errors
    )
    assert legendary_mentioned, (
        f"Validation errors should mention the Legendary restriction (Rule 8.3.6), got: {errors}"
    )


@then('the deck is valid with respect to "Normal Card" copy count')
def deck_valid_for_normal_card_count(game_state):
    """Rule 8.3.6: Non-Legendary cards are not subject to the Legendary limit-of-1."""
    result = game_state.validation_result
    assert result is not None, "validate_deck_for_constructed should return a result"
    # The deck should not be invalid *because of copy count* for a non-Legendary card
    # (Other errors for too many/few cards overall are acceptable, but not Legendary violation)
    is_valid = getattr(result, "is_valid", None)
    errors = getattr(result, "errors", [])
    legendary_violation = any(
        "legendary" in str(e).lower()
        for e in errors
    )
    assert not legendary_violation, (
        "Non-Legendary card should NOT trigger Legendary restriction error (Rule 8.3.6), "
        f"but got Legendary-related errors: {errors}"
    )


@then("the deck is valid with respect to both Legendary cards")
def deck_valid_for_both_legendary_cards(game_state):
    """Rule 8.3.6: 1 copy each of multiple different Legendary cards is valid."""
    result = game_state.validation_result
    assert result is not None, "validate_deck_for_constructed should return a result"
    is_valid = getattr(result, "is_valid", None)
    assert is_valid is True, (
        "Deck with 1 copy each of multiple different Legendary cards should be valid "
        f"(Rule 8.3.6), got is_valid={is_valid}"
    )


# ===== Fixtures =====

@pytest.fixture
def game_state():
    """
    Fixture providing game state for testing Legendary (Rule 8.3.6).

    Uses BDDGameState which integrates with the real engine.
    Reference: Rule 8.3.6
    """
    from tests.bdd_helpers import BDDGameState

    state = BDDGameState()
    return state
