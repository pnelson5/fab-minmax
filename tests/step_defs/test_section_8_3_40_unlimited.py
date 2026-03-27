"""
Step definitions for Section 8.3.40: Unlimited (Ability Keyword)
Reference: Flesh and Blood Comprehensive Rules Section 8.3.40

This module implements behavioral tests for the Unlimited ability keyword:
- Unlimited is a meta-static ability (Rule 8.3.40)
- Unlimited means "You may have any number of this card in your deck" (Rule 8.3.40)
- A deck may contain any number of copies of an Unlimited card (Rule 8.3.40)
- Cards without Unlimited are still subject to normal copy limits (Rule 8.3.40)

Engine Features Needed for Section 8.3.40:
- [ ] AbilityKeyword.UNLIMITED meta-static ability on cards (Rule 8.3.40)
- [ ] UnlimitedAbility.is_meta_static -> True (Rule 8.3.40)
- [ ] UnlimitedAbility.meaning == "You may have any number of this card in your deck" (Rule 8.3.40)
- [ ] DeckValidator.validate_unlimited(deck) allows any number of copies per Unlimited card (Rule 8.3.40)
- [ ] DeckValidator enforces normal copy limits on cards without Unlimited (Rule 8.3.40)

Current status: Tests written, Engine pending
"""

import pytest
from pytest_bdd import scenario, given, when, then, parsers


# ===== Rule 8.3.40: Unlimited is a meta-static ability =====

@scenario(
    "../features/section_8_3_40_unlimited.feature",
    "Unlimited is a meta-static ability",
)
def test_unlimited_is_meta_static_ability():
    """Rule 8.3.40: Unlimited is a meta-static ability."""
    pass


# ===== Rule 8.3.40: 4 copies of Unlimited card is valid =====

@scenario(
    "../features/section_8_3_40_unlimited.feature",
    "A deck with 4 copies of an Unlimited card is valid",
)
def test_four_unlimited_copies_is_valid():
    """Rule 8.3.40: A deck with 4 copies of an Unlimited card is valid."""
    pass


# ===== Rule 8.3.40: 10 copies of Unlimited card is valid =====

@scenario(
    "../features/section_8_3_40_unlimited.feature",
    "A deck with 10 copies of an Unlimited card is valid",
)
def test_ten_unlimited_copies_is_valid():
    """Rule 8.3.40: A deck with 10 copies of an Unlimited card is valid."""
    pass


# ===== Rule 8.3.40: 1 copy of Unlimited card is valid =====

@scenario(
    "../features/section_8_3_40_unlimited.feature",
    "A deck with 1 copy of an Unlimited card is valid",
)
def test_one_unlimited_copy_is_valid():
    """Rule 8.3.40: A deck with 1 copy of an Unlimited card is valid."""
    pass


# ===== Rule 8.3.40: Card without Unlimited does not get unrestricted copies =====

@scenario(
    "../features/section_8_3_40_unlimited.feature",
    "A card without Unlimited does not get the unlimited-copy benefit",
)
def test_non_unlimited_card_still_subject_to_copy_limits():
    """Rule 8.3.40: Cards without Unlimited are still subject to normal copy limits."""
    pass


# ===== Rule 8.3.40: Multiple different Unlimited cards can each appear any number of times =====

@scenario(
    "../features/section_8_3_40_unlimited.feature",
    "A deck may contain many copies each of multiple different Unlimited cards",
)
def test_multiple_different_unlimited_cards_many_copies_is_valid():
    """Rule 8.3.40: Multiple distinct Unlimited cards may each appear any number of times."""
    pass


# ===== Step Definitions =====

# ---- Given steps ----

@given('a card has the "Unlimited" keyword')
def card_with_unlimited(game_state):
    """Rule 8.3.40: Create a card that has the Unlimited keyword."""
    card = game_state.create_card(name="Unlimited Test Card")
    card._has_unlimited = True
    game_state.unlimited_card = card


@given("a constructed deck")
def empty_constructed_deck(game_state):
    """Rule 8.3.40: Create an empty constructed deck for validation tests."""
    game_state.test_deck = game_state.create_deck()


@given(parsers.parse('the deck contains {count:d} copies of a card named "{card_name}" with the Unlimited keyword'))
def deck_contains_n_unlimited_copies(game_state, count, card_name):
    """Rule 8.3.40: Add N copies of an Unlimited card to the deck."""
    card = game_state.create_card(name=card_name)
    card._has_unlimited = True
    game_state.test_deck_unlimited_card_name = card_name
    game_state.add_cards_to_deck(game_state.test_deck, card, count=count)


@given(parsers.parse('the deck contains {count:d} copies of a card named "{card_name}" without the Unlimited keyword'))
def deck_contains_n_non_unlimited_copies(game_state, count, card_name):
    """Rule 8.3.40: Add N copies of a non-Unlimited card to the deck."""
    card = game_state.create_card(name=card_name)
    card._has_unlimited = False
    game_state.test_deck_normal_card_name = card_name
    game_state.add_cards_to_deck(game_state.test_deck, card, count=count)


@given(parsers.parse('the deck contains 5 copies of a card named "{card_name}" with the Unlimited keyword'))
def deck_contains_five_named_unlimited(game_state, card_name):
    """Rule 8.3.40: Add 5 copies of a named Unlimited card to the deck."""
    card = game_state.create_card(name=card_name)
    card._has_unlimited = True
    if not hasattr(game_state, "test_deck_unlimited_card_names"):
        game_state.test_deck_unlimited_card_names = []
    game_state.test_deck_unlimited_card_names.append(card_name)
    game_state.add_cards_to_deck(game_state.test_deck, card, count=5)


# ---- When steps ----

@when("I inspect the Unlimited ability on the card")
def inspect_unlimited_ability(game_state):
    """Rule 8.3.40: Inspect the Unlimited ability on the card."""
    game_state.inspected_ability = game_state.get_unlimited_ability(
        game_state.unlimited_card
    )


@when("the deck is validated for constructed play")
def validate_deck_for_constructed(game_state):
    """Rule 8.3.40: Validate the deck for constructed play (checks Unlimited permissions)."""
    game_state.validation_result = game_state.validate_deck_for_constructed(
        game_state.test_deck
    )


# ---- Then steps ----

@then("the Unlimited ability is a meta-static ability")
def unlimited_is_meta_static(game_state):
    """Rule 8.3.40: Unlimited must be a meta-static ability."""
    ability = game_state.inspected_ability
    assert ability is not None, "Card should have an Unlimited ability"
    is_meta_static = getattr(ability, "is_meta_static", None)
    assert is_meta_static is True, (
        f"Unlimited should be a meta-static ability (Rule 8.3.40), got: {is_meta_static}"
    )


@then('the Unlimited ability means "You may have any number of this card in your deck"')
def unlimited_meaning_is_correct(game_state):
    """Rule 8.3.40: Unlimited means 'You may have any number of this card in your deck'."""
    ability = game_state.inspected_ability
    meaning = getattr(ability, "meaning", None)
    assert meaning == "You may have any number of this card in your deck", (
        f"Unlimited meaning should be 'You may have any number of this card in your deck' "
        f"(Rule 8.3.40), got: {meaning}"
    )


@then("the deck is valid with respect to the Unlimited card copy count")
def deck_valid_for_unlimited(game_state):
    """Rule 8.3.40: A deck with any number of copies of an Unlimited card is valid."""
    result = game_state.validation_result
    assert result is not None, "validate_deck_for_constructed should return a result"
    is_valid = getattr(result, "is_valid", None)
    errors = getattr(result, "errors", [])
    # Should not have copy-count violations for the Unlimited card
    unlimited_violation = any(
        "unlimited" in str(e).lower() or "copy" in str(e).lower() or "copies" in str(e).lower()
        for e in errors
    )
    assert not unlimited_violation, (
        "An Unlimited card should never trigger copy-count validation errors (Rule 8.3.40), "
        f"but got errors: {errors}"
    )


@then(parsers.parse('the deck is not valid due to exceeding normal copy limits for "{card_name}"'))
def deck_invalid_for_normal_copy_limit(game_state, card_name):
    """Rule 8.3.40: Cards without Unlimited are subject to normal copy limits."""
    result = game_state.validation_result
    assert result is not None, "validate_deck_for_constructed should return a result"
    is_valid = getattr(result, "is_valid", None)
    assert is_valid is False, (
        f"Deck with 4 copies of a non-Unlimited card '{card_name}' should be invalid "
        f"(normal copy limit applies, Rule 8.3.40), got is_valid={is_valid}"
    )


@then("the deck is valid with respect to both Unlimited card copy counts")
def deck_valid_for_both_unlimited_cards(game_state):
    """Rule 8.3.40: A deck with many copies of multiple distinct Unlimited cards is valid."""
    result = game_state.validation_result
    assert result is not None, "validate_deck_for_constructed should return a result"
    is_valid = getattr(result, "is_valid", None)
    assert is_valid is True, (
        "Deck with many copies of multiple different Unlimited cards should be valid "
        f"(Rule 8.3.40), got is_valid={is_valid}"
    )


# ===== Fixtures =====

@pytest.fixture
def game_state():
    """
    Fixture providing game state for testing Unlimited (Rule 8.3.40).

    Uses BDDGameState which integrates with the real engine.
    Reference: Rule 8.3.40
    """
    from tests.bdd_helpers import BDDGameState

    state = BDDGameState()
    return state
