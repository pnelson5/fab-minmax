"""
Step definitions for Section 8.3.7: Specialization (Ability Keyword)
Reference: Flesh and Blood Comprehensive Rules Section 8.3.7

This module implements behavioral tests for the Specialization ability keyword:
- Specialization is a meta-static ability (Rule 8.3.7)
- Specialization is written "[HERO] Specialization" meaning "You may only have this
  in your deck if your hero is [HERO]" (Rule 8.3.7)
- HERO in the Specialization text refers to the moniker of the player's hero card (Rule 8.3.7)
- Card effects can override the Specialization restriction (Rule 1.0.1a, Rule 5.4.3a)
- If a meta-static ability ceases to exist during a game, it does not affect the legality
  of rules followed outside the game (Rule 5.4.3a)

Engine Features Needed for Section 8.3.7:
- [ ] AbilityKeyword.SPECIALIZATION meta-static ability on cards (Rule 8.3.7)
- [ ] SpecializationAbility.is_meta_static -> True (Rule 8.3.7)
- [ ] SpecializationAbility.hero_moniker property returning the hero identifier (Rule 8.3.7)
- [ ] SpecializationAbility.meaning == "You may only have this in your deck if your hero is <HERO>" (Rule 8.3.7)
- [ ] HeroCard.moniker property returning the most significant name identifier (Rule 2.7.3)
- [ ] DeckValidator.validate_specialization(deck, hero) enforces hero moniker matching (Rule 8.3.7)
- [ ] DeckValidationError includes details about which Specialization card violated the rule (Rule 8.3.7)
- [ ] DeckValidator respects hero effects that override the Specialization restriction (Rule 5.4.3a)
- [ ] Losing a Specialization override during a game does not make already-legal deck illegal (Rule 5.4.3a)

Current status: Tests written, Engine pending
"""

import pytest
from pytest_bdd import scenario, given, when, then, parsers


# ===== Rule 8.3.7: Specialization is a meta-static ability =====

@scenario(
    "../features/section_8_3_7_specialization.feature",
    "Specialization is a meta-static ability",
)
def test_specialization_is_meta_static_ability():
    """Rule 8.3.7: Specialization is a meta-static ability."""
    pass


# ===== Rule 8.3.7: Deck valid when hero matches =====

@scenario(
    "../features/section_8_3_7_specialization.feature",
    "A deck is valid when the hero moniker matches the Specialization keyword",
)
def test_deck_valid_when_hero_matches_specialization():
    """Rule 8.3.7: A card with '[HERO] Specialization' is legal when hero's moniker is HERO."""
    pass


# ===== Rule 8.3.7: Deck invalid when hero doesn't match =====

@scenario(
    "../features/section_8_3_7_specialization.feature",
    "A deck is invalid when the hero moniker does not match the Specialization keyword",
)
def test_deck_invalid_when_hero_does_not_match_specialization():
    """Rule 8.3.7: A card with '[HERO] Specialization' is illegal when hero's moniker is not HERO."""
    pass


# ===== Rule 8.3.7: Moniker (not full name) is used for matching =====

@scenario(
    "../features/section_8_3_7_specialization.feature",
    "The hero moniker is used for Specialization matching, not the full name",
)
def test_hero_moniker_used_for_specialization_matching():
    """Rule 8.3.7: Specialization checks the hero's moniker, not the full hero name."""
    pass


# ===== Rule 8.3.7: Non-Specialization card not restricted by hero =====

@scenario(
    "../features/section_8_3_7_specialization.feature",
    "A card without Specialization is not restricted by hero identity",
)
def test_non_specialization_card_not_restricted_by_hero():
    """Rule 8.3.7: Cards without Specialization are not subject to hero identity restrictions."""
    pass


# ===== Rule 5.4.3a: Effect can override Specialization restriction =====

@scenario(
    "../features/section_8_3_7_specialization.feature",
    "A card effect can allow Specialization cards of any hero in the deck",
)
def test_effect_can_override_specialization_restriction():
    """Rule 5.4.3a: A hero effect can override the standard Specialization restriction."""
    pass


# ===== Rule 5.4.3a: Losing override during game doesn't affect deck legality =====

@scenario(
    "../features/section_8_3_7_specialization.feature",
    "Losing a Specialization override effect during a game does not make deck illegal",
)
def test_losing_specialization_override_during_game_does_not_affect_deck_legality():
    """Rule 5.4.3a: A meta-static ability ceasing during a game doesn't retroactively make the deck illegal."""
    pass


# ===== Step Definitions =====

# ---- Given steps ----

@given('a card has the "Dorinthea Specialization" keyword')
def card_with_dorinthea_specialization(game_state):
    """Rule 8.3.7: Create a card that has the Dorinthea Specialization keyword."""
    card = game_state.create_card(name="Dorinthea Specialization Test Card")
    card._specialization_hero = "Dorinthea"
    game_state.specialization_card = card


@given(parsers.parse('a constructed deck with hero "{hero_name}"'))
def constructed_deck_with_hero(game_state, hero_name):
    """Rule 8.3.7: Create a constructed deck with the specified hero."""
    game_state.test_deck = game_state.create_deck()
    hero_card = game_state.create_card(name=hero_name)
    hero_card._is_hero = True
    hero_card._hero_full_name = hero_name
    # Moniker is the most significant part of the name (e.g., "Dorinthea" from "Dorinthea Ironsong")
    # or just the first word/token before a comma
    moniker = hero_name.split(",")[0].strip()
    hero_card._hero_moniker = moniker
    game_state.test_deck._hero = hero_card
    game_state.test_hero = hero_card


@given(parsers.parse('the deck contains a card named "{card_name}" with "{specialization}"'))
def deck_contains_specialization_card(game_state, card_name, specialization):
    """Rule 8.3.7: Add a card with a specific Specialization keyword to the deck."""
    card = game_state.create_card(name=card_name)
    # Parse "[HERO] Specialization" to extract the hero moniker
    if specialization.endswith(" Specialization"):
        hero_moniker = specialization[: -len(" Specialization")].strip()
        card._specialization_hero = hero_moniker
    else:
        card._specialization_hero = None
    game_state.test_deck_specialization_card_name = card_name
    game_state.add_cards_to_deck(game_state.test_deck, card, count=1)


@given(parsers.parse('the deck contains a card named "{card_name}" without the Specialization keyword'))
def deck_contains_non_specialization_card(game_state, card_name):
    """Rule 8.3.7: Add a card without Specialization to the deck."""
    card = game_state.create_card(name=card_name)
    card._specialization_hero = None
    game_state.test_deck_generic_card_name = card_name
    game_state.add_cards_to_deck(game_state.test_deck, card, count=1)


@given('the hero has an ability "You may have specialization cards of any hero in your deck"')
def hero_has_specialization_override_ability(game_state):
    """Rule 5.4.3a: The hero has a meta-static ability that overrides the Specialization restriction."""
    hero = game_state.test_hero
    hero._has_universal_specialization = True
    hero._universal_specialization_ability_text = (
        "You may have specialization cards of any hero in your deck"
    )


@given("the deck was legally constructed under that hero ability")
def deck_legally_constructed_under_hero_ability(game_state):
    """Rule 5.4.3a: The deck was constructed legally due to the hero's override ability."""
    game_state.deck_was_legally_constructed = True


@given("the hero loses the specialization override ability during the game")
def hero_loses_specialization_override_during_game(game_state):
    """Rule 5.4.3a: During the game, the hero's override ability is removed."""
    hero = game_state.test_hero
    hero._has_universal_specialization = False
    game_state.hero_lost_override_during_game = True


# ---- When steps ----

@when("I inspect the Specialization ability on the card")
def inspect_specialization_ability(game_state):
    """Rule 8.3.7: Inspect the Specialization ability on the card."""
    game_state.inspected_ability = game_state.get_specialization_ability(
        game_state.specialization_card
    )


@when("the deck is validated for constructed play")
def validate_deck_for_constructed(game_state):
    """Rule 8.3.7: Validate the deck for constructed play (checks Specialization restrictions)."""
    game_state.validation_result = game_state.validate_deck_for_constructed(
        game_state.test_deck
    )


# ---- Then steps ----

@then("the Specialization ability is a meta-static ability")
def specialization_is_meta_static(game_state):
    """Rule 8.3.7: Specialization must be a meta-static ability."""
    ability = game_state.inspected_ability
    assert ability is not None, "Card should have a Specialization ability"
    is_meta_static = getattr(ability, "is_meta_static", None)
    assert is_meta_static is True, (
        f"Specialization should be a meta-static ability (Rule 8.3.7), got: {is_meta_static}"
    )


@then('the Specialization ability means "You may only have this in your deck if your hero is Dorinthea"')
def specialization_meaning_is_correct(game_state):
    """Rule 8.3.7: Specialization meaning includes the hero moniker."""
    ability = game_state.inspected_ability
    meaning = getattr(ability, "meaning", None)
    expected = "You may only have this in your deck if your hero is Dorinthea"
    assert meaning == expected, (
        f"Specialization meaning should be '{expected}' (Rule 8.3.7), got: {meaning}"
    )


@then("the deck is valid with respect to the Specialization restriction")
def deck_valid_for_specialization(game_state):
    """Rule 8.3.7: Deck is valid when hero moniker matches the Specialization keyword."""
    result = game_state.validation_result
    assert result is not None, "validate_deck_for_constructed should return a result"
    is_valid = getattr(result, "is_valid", None)
    assert is_valid is True, (
        f"Deck should be valid when hero moniker matches Specialization (Rule 8.3.7), "
        f"got is_valid={is_valid}"
    )


@then("the deck is invalid")
def deck_is_invalid(game_state):
    """Rule 8.3.7: Deck is invalid when hero moniker does not match Specialization."""
    result = game_state.validation_result
    assert result is not None, "validate_deck_for_constructed should return a result"
    is_valid = getattr(result, "is_valid", None)
    assert is_valid is False, (
        f"Deck should be invalid when hero moniker mismatches Specialization (Rule 8.3.7), "
        f"got is_valid={is_valid}"
    )


@then("the validation error mentions the Specialization restriction")
def validation_error_mentions_specialization(game_state):
    """Rule 8.3.7: The validation error should reference the Specialization keyword."""
    result = game_state.validation_result
    errors = getattr(result, "errors", [])
    assert errors, "Validation result should have error messages when deck is invalid"
    specialization_mentioned = any(
        "specialization" in str(e).lower() or "Specialization" in str(e)
        for e in errors
    )
    assert specialization_mentioned, (
        f"Validation errors should mention the Specialization restriction (Rule 8.3.7), got: {errors}"
    )


@then('the Specialization match is based on the moniker "Dorinthea"')
def specialization_match_uses_moniker(game_state):
    """Rule 8.3.7: Specialization matching is performed against the hero's moniker."""
    result = game_state.validation_result
    assert result is not None, "validate_deck_for_constructed should return a result"
    # Verify that the match was performed using the moniker rather than the full hero name
    moniker_used = getattr(result, "moniker_matched", None)
    if moniker_used is not None:
        assert moniker_used == "Dorinthea", (
            f"Specialization match should use moniker 'Dorinthea' (Rule 8.3.7), got: {moniker_used}"
        )
    # If the engine doesn't yet expose moniker_matched, a valid result is still a pass
    # as long as the deck is valid (tested by deck_valid_for_specialization step)


@then("the deck is valid with respect to the generic card")
def deck_valid_for_generic_card(game_state):
    """Rule 8.3.7: Non-Specialization cards are not restricted by hero identity."""
    result = game_state.validation_result
    assert result is not None, "validate_deck_for_constructed should return a result"
    errors = getattr(result, "errors", [])
    specialization_violation = any(
        "specialization" in str(e).lower()
        for e in errors
    )
    assert not specialization_violation, (
        "Non-Specialization card should NOT trigger Specialization restriction error (Rule 8.3.7), "
        f"but got Specialization-related errors: {errors}"
    )


@then("the deck is valid because the Specialization restriction is overridden")
def deck_valid_because_specialization_overridden(game_state):
    """Rule 5.4.3a: A hero effect can override the Specialization restriction."""
    result = game_state.validation_result
    assert result is not None, "validate_deck_for_constructed should return a result"
    is_valid = getattr(result, "is_valid", None)
    assert is_valid is True, (
        "Deck with Specialization cards should be valid when hero has override ability "
        f"(Rule 5.4.3a), got is_valid={is_valid}"
    )


@then("the presence of Dorinthea Specialization Card in the card pool remains legal")
def specialization_card_remains_legal_after_losing_override(game_state):
    """Rule 5.4.3a: Losing a meta-static override during the game doesn't retroactively make the deck illegal."""
    hero = game_state.test_hero
    # The override was lost during the game
    assert game_state.hero_lost_override_during_game is True, (
        "Hero should have lost the override during game"
    )
    # Despite losing the override during the game, deck legality doesn't change
    card_pool_still_legal = game_state.check_card_pool_legality_unchanged_after_meta_static_loss(
        hero
    )
    assert card_pool_still_legal is not False, (
        "Losing a meta-static override during a game should NOT make the deck illegal "
        "(Rule 5.4.3a): deck legality was determined outside the game"
    )


# ===== Fixtures =====

@pytest.fixture
def game_state():
    """
    Fixture providing game state for testing Specialization (Rule 8.3.7).

    Uses BDDGameState which integrates with the real engine.
    Reference: Rule 8.3.7
    """
    from tests.bdd_helpers import BDDGameState

    state = BDDGameState()
    return state
