"""
Step definitions for Section 8.3.16: Essence (Ability Keyword)
Reference: Flesh and Blood Comprehensive Rules Section 8.3.16

This module implements behavioral tests for the Essence ability keyword:
- Essence is a meta-static ability (Rule 8.3.16)
- Essence is written "Essence of [SUPERTYPES]" meaning "You may have [SUPERTYPES]
  cards in your deck, as though your hero had those supertypes" (Rule 8.3.16)
- SUPERTYPES is one or more supertype keywords (Rule 2.11)
- Essence expands the hero's effective supertypes for deck construction (Rule 1.1.3)
- A card may only be in a deck if its supertypes are a subset of the hero's supertypes
  (possibly expanded by Essence) (Rule 1.1.3)
- If a meta-static ability ceases to exist during a game, it does not affect the
  legality of rules followed outside the game (Rule 5.4.3a)

Engine Features Needed for Section 8.3.16:
- [ ] EssenceAbility class as a meta-static ability (Rule 8.3.16)
- [ ] EssenceAbility.is_meta_static -> True (Rule 8.3.16)
- [ ] EssenceAbility.supertypes property returning the granted supertype list (Rule 8.3.16)
- [ ] EssenceAbility.meaning == "You may have [SUPERTYPES] cards in your deck, as though your hero had those supertypes" (Rule 8.3.16)
- [ ] DeckValidator.validate_essence(deck, hero) uses Essence to expand hero supertypes during validation (Rule 8.3.16)
- [ ] DeckValidationError when non-hero-supertype card is in deck without matching Essence (Rule 1.1.3)
- [ ] Losing an Essence card during a game does not retroactively make the deck illegal (Rule 5.4.3a)

Current status: Tests written, Engine pending
"""

import pytest
from pytest_bdd import scenario, given, when, then, parsers


# ===== Rule 8.3.16: Essence is a meta-static ability =====

@scenario(
    "../features/section_8_3_16_essence.feature",
    "Essence is a meta-static ability",
)
def test_essence_is_meta_static_ability():
    """Rule 8.3.16: Essence is a meta-static ability."""
    pass


# ===== Rule 8.3.16: Essence allows including specified supertype cards =====

@scenario(
    "../features/section_8_3_16_essence.feature",
    "A hero without a supertype can include cards of that supertype via Essence",
)
def test_essence_grants_access_to_specified_supertype():
    """Rule 8.3.16: A card with Essence allows including the specified supertype cards."""
    pass


# ===== Rule 8.3.16: Without Essence, hero cannot include non-matching supertype cards =====

@scenario(
    "../features/section_8_3_16_essence.feature",
    "Without Essence a hero cannot include cards of a non-matching supertype",
)
def test_without_essence_hero_cannot_include_non_matching_supertype():
    """Rule 1.1.3: Without Essence, a hero cannot include cards whose supertypes don't match."""
    pass


# ===== Rule 8.3.16: Essence only covers listed supertypes =====

@scenario(
    "../features/section_8_3_16_essence.feature",
    "Essence of Ninja does not grant access to other supertypes",
)
def test_essence_only_covers_specified_supertypes():
    """Rule 8.3.16: Essence grants access only to the supertypes explicitly listed."""
    pass


# ===== Rule 8.3.16: Essence with multiple supertypes =====

@scenario(
    "../features/section_8_3_16_essence.feature",
    "Essence can grant access to multiple supertypes simultaneously",
)
def test_essence_can_grant_multiple_supertypes():
    """Rule 8.3.16: Essence listing multiple supertypes grants access to all listed supertypes."""
    pass


# ===== Rule 8.3.16: Essence meaning format =====

@scenario(
    "../features/section_8_3_16_essence.feature",
    "Essence ability meaning is correctly formatted with the specified supertypes",
)
def test_essence_ability_meaning_format():
    """Rule 8.3.16: Essence ability meaning is 'You may have [SUPERTYPES] cards in your deck, as though your hero had those supertypes'."""
    pass


# ===== Rule 5.4.3a: Losing Essence during game does not affect deck legality =====

@scenario(
    "../features/section_8_3_16_essence.feature",
    "Losing an Essence card during a game does not make the deck illegal",
)
def test_losing_essence_during_game_does_not_affect_deck_legality():
    """Rule 5.4.3a: Losing a meta-static Essence card during the game doesn't retroactively make the deck illegal."""
    pass


# ===== Step Definitions =====

# ---- Given steps ----

@given(parsers.parse('a card has the "{essence_keyword}" keyword'))
def card_with_essence_keyword(game_state, essence_keyword):
    """Rule 8.3.16: Create a card that has the specified Essence keyword."""
    card = game_state.create_card(name=f"Essence Test Card ({essence_keyword})")
    # Parse "Essence of [SUPERTYPES]" to extract supertypes
    if essence_keyword.startswith("Essence of "):
        supertypes_str = essence_keyword[len("Essence of "):]
        card._essence_supertypes = supertypes_str.split()
    else:
        card._essence_supertypes = []
    card._essence_keyword = essence_keyword
    game_state.essence_card = card


@given(parsers.parse('a hero "{hero_name}" with supertypes "{hero_supertypes}"'))
def hero_with_supertypes(game_state, hero_name, hero_supertypes):
    """Rule 2.11: Create a hero with the specified supertypes."""
    hero_card = game_state.create_card(name=hero_name)
    hero_card._is_hero = True
    hero_card._hero_full_name = hero_name
    moniker = hero_name.split(",")[0].strip()
    hero_card._hero_moniker = moniker
    hero_card._hero_supertypes = hero_supertypes.split()
    game_state.test_hero = hero_card
    game_state.test_deck = game_state.create_deck()
    game_state.test_deck._hero = hero_card
    game_state.test_deck._essence_cards = []
    game_state.test_deck._restricted_cards = []


@given('a card with "Essence of Ninja" is in the player\'s card pool')
def essence_of_ninja_in_card_pool(game_state):
    """Rule 8.3.16: Add a card with 'Essence of Ninja' to the player's card pool."""
    card = game_state.create_card(name="Essence of Ninja Card")
    card._essence_supertypes = ["Ninja"]
    card._essence_keyword = "Essence of Ninja"
    game_state.test_deck._essence_cards.append(card)
    game_state.essence_card = card


@given('a card with "Essence of Ninja Wizard" is in the player\'s card pool')
def essence_of_ninja_wizard_in_card_pool(game_state):
    """Rule 8.3.16: Add a card with 'Essence of Ninja Wizard' to the player's card pool."""
    card = game_state.create_card(name="Essence of Ninja Wizard Card")
    card._essence_supertypes = ["Ninja", "Wizard"]
    card._essence_keyword = "Essence of Ninja Wizard"
    game_state.test_deck._essence_cards.append(card)
    game_state.essence_card = card


@given('no Essence card is in the player\'s card pool')
def no_essence_in_card_pool(game_state):
    """Rule 8.3.16: No Essence card in the player's card pool."""
    game_state.test_deck._essence_cards = []


@given('a Ninja card is in the player\'s deck')
def ninja_card_in_deck(game_state):
    """Rule 2.11: Add a Ninja supertype card to the test deck."""
    card = game_state.create_card(name="Test Ninja Card")
    card._card_supertypes = ["Ninja"]
    game_state.test_deck._restricted_cards.append(card)
    game_state.add_cards_to_deck(game_state.test_deck, card, count=1)


@given('a Wizard card is in the player\'s deck')
def wizard_card_in_deck(game_state):
    """Rule 2.11: Add a Wizard supertype card to the test deck."""
    card = game_state.create_card(name="Test Wizard Card")
    card._card_supertypes = ["Wizard"]
    game_state.test_deck._restricted_cards.append(card)
    game_state.add_cards_to_deck(game_state.test_deck, card, count=1)


@given('a Guardian card is in the player\'s deck')
def guardian_card_in_deck(game_state):
    """Rule 2.11: Add a Guardian supertype card to the test deck."""
    card = game_state.create_card(name="Test Guardian Card")
    card._card_supertypes = ["Guardian"]
    game_state.test_deck._restricted_cards.append(card)
    game_state.add_cards_to_deck(game_state.test_deck, card, count=1)


@given('the deck was legally constructed with the Essence card present')
def deck_legally_constructed_with_essence(game_state):
    """Rule 5.4.3a: The deck was constructed legally due to the Essence card being present."""
    game_state.deck_was_legally_constructed = True


@given('the Essence card is removed from the card pool during the game')
def essence_card_removed_during_game(game_state):
    """Rule 5.4.3a: During the game, the Essence card is removed from the card pool."""
    game_state.test_deck._essence_cards = []
    game_state.essence_removed_during_game = True


# ---- When steps ----

@when('I inspect the Essence ability on the card')
def inspect_essence_ability(game_state):
    """Rule 8.3.16: Inspect the Essence ability on the card."""
    game_state.inspected_ability = game_state.get_essence_ability(
        game_state.essence_card
    )


@when('the deck is validated for constructed play')
def validate_deck_for_constructed(game_state):
    """Rule 8.3.16: Validate the deck for constructed play (checks Essence and supertype restrictions)."""
    game_state.validation_result = game_state.validate_deck_for_constructed(
        game_state.test_deck
    )


# ---- Then steps ----

@then('the Essence ability is a meta-static ability')
def essence_is_meta_static(game_state):
    """Rule 8.3.16: Essence must be a meta-static ability."""
    ability = game_state.inspected_ability
    assert ability is not None, "Card should have an Essence ability"
    is_meta_static = getattr(ability, "is_meta_static", None)
    assert is_meta_static is True, (
        f"Essence should be a meta-static ability (Rule 8.3.16), got: {is_meta_static}"
    )


@then(parsers.parse('the Essence ability means "{expected_meaning}"'))
def essence_meaning_is_correct(game_state, expected_meaning):
    """Rule 8.3.16: Essence meaning is 'You may have [SUPERTYPES] cards in your deck, as though your hero had those supertypes'."""
    ability = game_state.inspected_ability
    meaning = getattr(ability, "meaning", None)
    assert meaning == expected_meaning, (
        f"Essence meaning should be '{expected_meaning}' (Rule 8.3.16), got: {meaning}"
    )


@then('the deck is valid because Essence of Ninja grants access to Ninja cards')
def deck_valid_due_to_essence_of_ninja(game_state):
    """Rule 8.3.16: Deck is valid when Essence of Ninja allows Ninja cards."""
    result = game_state.validation_result
    assert result is not None, "validate_deck_for_constructed should return a result"
    is_valid = getattr(result, "is_valid", None)
    assert is_valid is True, (
        "Deck with Ninja cards should be valid when Essence of Ninja is in card pool "
        f"(Rule 8.3.16), got is_valid={is_valid}"
    )


@then('the deck is invalid because Ninja is not in the hero\'s supertypes')
def deck_invalid_no_ninja_supertype(game_state):
    """Rule 1.1.3: Deck is invalid when Ninja card is included but hero is not Ninja."""
    result = game_state.validation_result
    assert result is not None, "validate_deck_for_constructed should return a result"
    is_valid = getattr(result, "is_valid", None)
    assert is_valid is False, (
        "Deck with Ninja cards should be INVALID when hero has no Ninja supertype and "
        f"no Essence of Ninja is in card pool (Rule 1.1.3), got is_valid={is_valid}"
    )


@then('the deck is invalid because Guardian is not covered by Essence of Ninja')
def deck_invalid_guardian_not_covered_by_essence_of_ninja(game_state):
    """Rule 8.3.16: Essence of Ninja does not grant access to Guardian cards."""
    result = game_state.validation_result
    assert result is not None, "validate_deck_for_constructed should return a result"
    is_valid = getattr(result, "is_valid", None)
    assert is_valid is False, (
        "Deck with Guardian cards should be INVALID even with Essence of Ninja, "
        f"because Guardian is not covered (Rule 8.3.16), got is_valid={is_valid}"
    )


@then('the deck is valid because Essence of Ninja Wizard covers both supertypes')
def deck_valid_due_to_essence_ninja_wizard(game_state):
    """Rule 8.3.16: Essence listing multiple supertypes grants access to all of them."""
    result = game_state.validation_result
    assert result is not None, "validate_deck_for_constructed should return a result"
    is_valid = getattr(result, "is_valid", None)
    assert is_valid is True, (
        "Deck with Ninja and Wizard cards should be valid when Essence of Ninja Wizard "
        f"is in card pool (Rule 8.3.16), got is_valid={is_valid}"
    )


@then('the Ninja cards in the deck remain legal despite the Essence card being gone')
def ninja_cards_remain_legal_after_essence_removed(game_state):
    """Rule 5.4.3a: Losing a meta-static Essence during a game doesn't retroactively make the deck illegal."""
    assert game_state.essence_removed_during_game is True, (
        "The Essence card should have been removed during the game"
    )
    # Deck legality is determined at construction time; losing Essence in-game is irrelevant
    card_pool_still_legal = game_state.check_card_pool_legality_unchanged_after_meta_static_loss(
        game_state.test_hero
    )
    assert card_pool_still_legal is not False, (
        "Removing an Essence card during a game should NOT make the deck illegal "
        "(Rule 5.4.3a): deck legality was determined outside the game"
    )


# ===== Fixtures =====

@pytest.fixture
def game_state():
    """
    Fixture providing game state for testing Essence (Rule 8.3.16).

    Uses BDDGameState which integrates with the real engine.
    Reference: Rule 8.3.16
    """
    from tests.bdd_helpers import BDDGameState

    state = BDDGameState()
    return state
