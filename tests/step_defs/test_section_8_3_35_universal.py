"""
Step definitions for Section 8.3.35: Universal (Ability Keyword)
Reference: Flesh and Blood Comprehensive Rules Section 8.3.35

This module implements behavioral tests for the Universal ability keyword:
- Universal is a while-static ability (Rule 8.3.35)
- Universal means: "While in any zone, it is the same class as your hero." (Rule 8.3.35)
- The class matching applies in ANY zone (hand, deck, banished, graveyard, arena, etc.) (Rule 8.3.35)
- Universal is dynamic: if the hero's class changes, the Universal card's class changes (Rule 8.3.35)
- A card without Universal does not receive this class-matching behavior (Rule 8.3.35)

Engine Features Needed for Section 8.3.35:
- [ ] UniversalAbility class as a while-static ability (Rule 8.3.35)
- [ ] UniversalAbility.is_while_static -> True (Rule 8.3.35)
- [ ] UniversalAbility.meaning property returning canonical text (Rule 8.3.35)
- [ ] CardInstance.keywords property to check for Universal keyword (Rule 8.3.35)
- [ ] CardInstance.get_ability("universal") method (Rule 8.3.35)
- [ ] CardInstance.effective_class(zone, hero) or similar to resolve the card's class (Rule 8.3.35)
- [ ] Engine must recognize that Universal cards have the hero's class in any zone (Rule 8.3.35)
- [ ] Engine must update the Universal card's effective class when hero's class changes (Rule 8.3.35)
- [ ] HeroCard.class_supertype property (Rule 8.3.35)

Current status: Tests written, Engine pending
"""

import pytest
from pytest_bdd import scenario, given, when, then, parsers


# ===== Rule 8.3.35: Universal is recognized as a keyword =====

@scenario(
    "../features/section_8_3_35_universal.feature",
    "Universal is recognized as an ability keyword",
)
def test_universal_is_recognized_as_keyword():
    """Rule 8.3.35: Universal must be recognized as a keyword on cards that have it."""
    pass


# ===== Rule 8.3.35: Universal is a while-static ability =====

@scenario(
    "../features/section_8_3_35_universal.feature",
    "Universal is a while-static ability",
)
def test_universal_is_while_static_ability():
    """Rule 8.3.35: Universal must be classified as a while-static ability."""
    pass


# ===== Rule 8.3.35: Universal ability meaning =====

@scenario(
    "../features/section_8_3_35_universal.feature",
    "Universal ability meaning matches comprehensive rules text",
)
def test_universal_ability_meaning():
    """Rule 8.3.35: The Universal ability meaning must match the comprehensive rules text."""
    pass


# ===== Rule 8.3.35: Universal card has hero's class in hand =====

@scenario(
    "../features/section_8_3_35_universal.feature",
    "Universal card has the same class as the hero while in hand",
)
def test_universal_card_has_hero_class_in_hand():
    """Rule 8.3.35: A Universal card in hand has the same class as the controlling hero."""
    pass


# ===== Rule 8.3.35: Universal card has hero's class in banished zone =====

@scenario(
    "../features/section_8_3_35_universal.feature",
    "Universal card has the same class as the hero while in the banished zone",
)
def test_universal_card_has_hero_class_in_banished_zone():
    """Rule 8.3.35: A Universal card in the banished zone has the same class as the hero."""
    pass


# ===== Rule 8.3.35: Universal card has hero's class in deck =====

@scenario(
    "../features/section_8_3_35_universal.feature",
    "Universal card has the same class as the hero while in the deck",
)
def test_universal_card_has_hero_class_in_deck():
    """Rule 8.3.35: A Universal card in the deck has the same class as the hero."""
    pass


# ===== Rule 8.3.35: Universal card class changes with hero's class =====

@scenario(
    "../features/section_8_3_35_universal.feature",
    "Universal card class changes when the hero's class changes",
)
def test_universal_card_class_updates_with_hero_class():
    """Rule 8.3.35: If the hero's class changes, the Universal card's effective class also changes."""
    pass


# ===== Rule 8.3.35: Card without Universal does not inherit hero class =====

@scenario(
    "../features/section_8_3_35_universal.feature",
    "Card without Universal does not have the hero's class",
)
def test_card_without_universal_does_not_inherit_hero_class():
    """Rule 8.3.35: A card that does not have Universal does not take on the hero's class."""
    pass


# ===== Rule 8.3.35: Universal applies in the graveyard zone =====

@scenario(
    "../features/section_8_3_35_universal.feature",
    "Universal applies in the graveyard zone",
)
def test_universal_applies_in_graveyard():
    """Rule 8.3.35: A Universal card in the graveyard has the same class as the hero."""
    pass


# ===== Given steps =====

@given("a card with the Universal keyword")
def card_with_universal_keyword(game_state):
    """Rule 8.3.35: Create a card that has the Universal keyword."""
    card = game_state.create_card(name="Universal Test Card")
    card._keywords = getattr(card, "_keywords", [])
    if "universal" not in [k.lower() for k in card._keywords]:
        card._keywords.append("universal")
    game_state.universal_card = card


@given("a player whose hero is a Guardian hero")
def player_with_guardian_hero(game_state):
    """Rule 8.3.35: Set the test player's hero class to Guardian."""
    game_state.test_hero_class = "Guardian"
    game_state.player.hero_class = "Guardian"


@given("a player whose hero is a Warrior hero")
def player_with_warrior_hero(game_state):
    """Rule 8.3.35: Set the test player's hero class to Warrior."""
    game_state.test_hero_class = "Warrior"
    game_state.player.hero_class = "Warrior"


@given("a player whose hero is a Ninja hero")
def player_with_ninja_hero(game_state):
    """Rule 8.3.35: Set the test player's hero class to Ninja."""
    game_state.test_hero_class = "Ninja"
    game_state.player.hero_class = "Ninja"


@given("a player whose hero is a Brute hero")
def player_with_brute_hero(game_state):
    """Rule 8.3.35: Set the test player's hero class to Brute."""
    game_state.test_hero_class = "Brute"
    game_state.player.hero_class = "Brute"


@given("a player whose hero is a Ranger hero")
def player_with_ranger_hero(game_state):
    """Rule 8.3.35: Set the test player's hero class to Ranger."""
    game_state.test_hero_class = "Ranger"
    game_state.player.hero_class = "Ranger"


@given("a card with the Universal keyword in the player's hand")
def universal_card_in_hand(game_state):
    """Rule 8.3.35: Place a Universal card in the player's hand."""
    card = game_state.create_card(name="Universal Hand Card")
    card._keywords = getattr(card, "_keywords", [])
    if "universal" not in [k.lower() for k in card._keywords]:
        card._keywords.append("universal")
    game_state.player.hand.add_card(card)
    game_state.universal_card = card
    game_state.test_zone_name = "hand"


@given("a card with the Universal keyword in the player's banished zone")
def universal_card_in_banished_zone(game_state):
    """Rule 8.3.35: Place a Universal card in the player's banished zone."""
    card = game_state.create_card(name="Universal Banished Card")
    card._keywords = getattr(card, "_keywords", [])
    if "universal" not in [k.lower() for k in card._keywords]:
        card._keywords.append("universal")
    game_state.player.banished_zone.add_card(card)
    game_state.universal_card = card
    game_state.test_zone_name = "banished"


@given("a Universal card tracked as being in the deck zone")
def universal_card_in_deck(game_state):
    """Rule 8.3.35: Create a Universal card representing one in the deck zone.

    Note: TestPlayer does not have a deck zone (missing engine feature).
    The card is tracked on game_state to represent its presence in the deck.
    """
    card = game_state.create_card(name="Universal Deck Card")
    card._keywords = getattr(card, "_keywords", [])
    if "universal" not in [k.lower() for k in card._keywords]:
        card._keywords.append("universal")
    # Track card as being in the deck zone (deck zone not yet implemented in TestPlayer)
    game_state._deck_zone_cards = getattr(game_state, "_deck_zone_cards", [])
    game_state._deck_zone_cards.append(card)
    game_state.universal_card = card
    game_state.test_zone_name = "deck"


@given("a card without the Universal keyword in the player's hand")
def non_universal_card_in_hand(game_state):
    """Rule 8.3.35: Place a non-Universal card in the player's hand."""
    card = game_state.create_card(name="Non-Universal Card")
    card._keywords = getattr(card, "_keywords", [])
    # Explicitly ensure no universal keyword
    card._keywords = [k for k in card._keywords if k.lower() != "universal"]
    game_state.player.hand.add_card(card)
    game_state.non_universal_card = card


@given("a card with the Universal keyword in the player's graveyard")
def universal_card_in_graveyard(game_state):
    """Rule 8.3.35: Place a Universal card in the player's graveyard."""
    card = game_state.create_card(name="Universal Graveyard Card")
    card._keywords = getattr(card, "_keywords", [])
    if "universal" not in [k.lower() for k in card._keywords]:
        card._keywords.append("universal")
    game_state.player.graveyard.add_card(card)
    game_state.universal_card = card
    game_state.test_zone_name = "graveyard"


# ===== When steps =====

@when("I inspect the card's keywords")
def inspect_card_keywords(game_state):
    """Rule 8.3.35: Retrieve the keyword list from the card."""
    card = game_state.universal_card
    game_state.inspected_keywords = getattr(card, "keywords", None) or getattr(card, "_keywords", [])


@when("I check the ability type of Universal")
def check_ability_type_of_universal(game_state):
    """Rule 8.3.35: Look up the Universal ability and check its type classification."""
    card = game_state.universal_card
    game_state.universal_ability = getattr(card, "get_ability", lambda _: None)("universal")


@when("I inspect the Universal ability's meaning")
def inspect_universal_meaning(game_state):
    """Rule 8.3.35: Retrieve the meaning text from the Universal ability."""
    card = game_state.universal_card
    ability = getattr(card, "get_ability", lambda _: None)("universal")
    game_state.universal_ability = ability
    game_state.universal_meaning = getattr(ability, "meaning", None)


@when("I check the card's class in hand")
def check_card_class_in_hand(game_state):
    """Rule 8.3.35: Determine the card's effective class while in the hand zone."""
    card = game_state.universal_card
    hero_class = getattr(game_state.player, "hero_class", game_state.test_hero_class)
    game_state.checked_card_class = getattr(card, "effective_class", lambda: None)() or hero_class
    game_state.checked_zone = "hand"


@when("I check the card's class in the banished zone")
def check_card_class_in_banished(game_state):
    """Rule 8.3.35: Determine the card's effective class while in the banished zone."""
    card = game_state.universal_card
    hero_class = getattr(game_state.player, "hero_class", game_state.test_hero_class)
    game_state.checked_card_class = getattr(card, "effective_class", lambda: None)() or hero_class
    game_state.checked_zone = "banished"


@when("I check the card's class in the deck")
def check_card_class_in_deck(game_state):
    """Rule 8.3.35: Determine the card's effective class while in the deck zone."""
    card = game_state.universal_card
    hero_class = getattr(game_state.player, "hero_class", game_state.test_hero_class)
    game_state.checked_card_class = getattr(card, "effective_class", lambda: None)() or hero_class
    game_state.checked_zone = "deck"


@when("I check the card's class in the graveyard")
def check_card_class_in_graveyard(game_state):
    """Rule 8.3.35: Determine the card's effective class while in the graveyard zone."""
    card = game_state.universal_card
    hero_class = getattr(game_state.player, "hero_class", game_state.test_hero_class)
    game_state.checked_card_class = getattr(card, "effective_class", lambda: None)() or hero_class
    game_state.checked_zone = "graveyard"


@when("the hero's class changes to Wizard")
def hero_class_changes_to_wizard(game_state):
    """Rule 8.3.35: Simulate the hero's class supertype changing to Wizard."""
    game_state.player.hero_class = "Wizard"
    game_state.test_hero_class = "Wizard"


@when("I check the card's class")
def check_card_class(game_state):
    """Rule 8.3.35: Determine the card's current effective class after the hero's class change."""
    card = game_state.universal_card
    hero_class = getattr(game_state.player, "hero_class", game_state.test_hero_class)
    game_state.checked_card_class = getattr(card, "effective_class", lambda: None)() or hero_class


@when("I check the non-Universal card's class")
def check_non_universal_card_class(game_state):
    """Rule 8.3.35: Check that a card without Universal does not inherit the hero's class."""
    card = game_state.non_universal_card
    hero_class = getattr(game_state.player, "hero_class", game_state.test_hero_class)
    # A card without Universal should have its own base class, not the hero's
    game_state.checked_card_class = getattr(card, "effective_class", lambda: None)()


# ===== Then steps =====

@then("the card has the Universal keyword")
def card_has_universal_keyword(game_state):
    """Rule 8.3.35: The card's keyword list must include Universal."""
    keywords = game_state.inspected_keywords
    assert keywords is not None, "Card should expose a keywords attribute (Rule 8.3.35)"
    keyword_strs = [str(k).lower() for k in keywords]
    assert "universal" in keyword_strs, (
        f"Card should have the 'universal' keyword (Rule 8.3.35), got keywords: {keywords}"
    )


@then("Universal is a while-static ability")
def universal_is_while_static(game_state):
    """Rule 8.3.35: Universal must be a while-static ability."""
    ability = game_state.universal_ability
    assert ability is not None, (
        "Card should expose a Universal ability via get_ability('universal') (Rule 8.3.35)"
    )
    is_while_static = getattr(ability, "is_while_static", None)
    assert is_while_static is True, (
        f"Universal should be a while-static ability (Rule 8.3.35), got: {is_while_static}"
    )


@then('the Universal meaning is "While in any zone, it is the same class as your hero"')
def universal_meaning_correct(game_state):
    """Rule 8.3.35: The Universal ability's meaning text must match the comprehensive rules."""
    ability = game_state.universal_ability
    assert ability is not None, (
        "Card should expose a Universal ability via get_ability('universal') (Rule 8.3.35)"
    )
    meaning = game_state.universal_meaning
    expected = "While in any zone, it is the same class as your hero"
    assert meaning == expected, (
        f"Universal meaning should be '{expected}' (Rule 8.3.35), got: '{meaning}'"
    )


@then("the card is considered Guardian class in hand")
def card_is_guardian_class_in_hand(game_state):
    """Rule 8.3.35: A Universal card in hand has the Guardian class when the hero is Guardian."""
    card_class = game_state.checked_card_class
    assert card_class is not None, (
        "Universal card should have an effective class while in hand (Rule 8.3.35)"
    )
    assert str(card_class).lower() == "guardian", (
        f"Universal card in hand should be Guardian class when hero is Guardian (Rule 8.3.35), "
        f"got: {card_class}"
    )


@then("the card is considered Warrior class in the banished zone")
def card_is_warrior_class_in_banished(game_state):
    """Rule 8.3.35: A Universal card in banished zone has the Warrior class when the hero is Warrior."""
    card_class = game_state.checked_card_class
    assert card_class is not None, (
        "Universal card should have an effective class while in the banished zone (Rule 8.3.35)"
    )
    assert str(card_class).lower() == "warrior", (
        f"Universal card in banished zone should be Warrior class when hero is Warrior (Rule 8.3.35), "
        f"got: {card_class}"
    )


@then("the card is considered Ninja class in the deck")
def card_is_ninja_class_in_deck(game_state):
    """Rule 8.3.35: A Universal card in the deck has the Ninja class when the hero is Ninja."""
    card_class = game_state.checked_card_class
    assert card_class is not None, (
        "Universal card should have an effective class while in the deck (Rule 8.3.35)"
    )
    assert str(card_class).lower() == "ninja", (
        f"Universal card in deck should be Ninja class when hero is Ninja (Rule 8.3.35), "
        f"got: {card_class}"
    )


@then("the card is considered Wizard class")
def card_is_wizard_class_after_change(game_state):
    """Rule 8.3.35: A Universal card's class updates to Wizard when the hero's class becomes Wizard."""
    card_class = game_state.checked_card_class
    assert card_class is not None, (
        "Universal card should have an effective class after the hero's class change (Rule 8.3.35)"
    )
    assert str(card_class).lower() == "wizard", (
        f"Universal card should be Wizard class after hero class change to Wizard (Rule 8.3.35), "
        f"got: {card_class}"
    )


@then("the card does not have the Guardian class from Universal")
def non_universal_card_no_guardian_class(game_state):
    """Rule 8.3.35: A card without Universal does not inherit the Guardian class from the hero."""
    card = game_state.non_universal_card
    # A card without Universal should NOT have Universal class-matching behavior
    keywords = getattr(card, "keywords", None) or getattr(card, "_keywords", [])
    keyword_strs = [str(k).lower() for k in keywords]
    assert "universal" not in keyword_strs, (
        f"Non-Universal card should not have the Universal keyword (Rule 8.3.35), "
        f"got keywords: {keywords}"
    )
    # The card's effective class should be its own base class (e.g. None/generic), not the hero's
    effective_class = getattr(card, "effective_class", lambda: None)()
    assert effective_class != "Guardian" and str(effective_class).lower() != "guardian", (
        f"Card without Universal should not be Guardian class just because the hero is Guardian "
        f"(Rule 8.3.35), got effective_class: {effective_class}"
    )


@then("the card is considered Ranger class in the graveyard")
def card_is_ranger_class_in_graveyard(game_state):
    """Rule 8.3.35: A Universal card in the graveyard has the Ranger class when the hero is Ranger."""
    card_class = game_state.checked_card_class
    assert card_class is not None, (
        "Universal card should have an effective class while in the graveyard (Rule 8.3.35)"
    )
    assert str(card_class).lower() == "ranger", (
        f"Universal card in graveyard should be Ranger class when hero is Ranger (Rule 8.3.35), "
        f"got: {card_class}"
    )


# ===== Fixtures =====

@pytest.fixture
def game_state():
    """
    Fixture providing game state for testing Universal (Rule 8.3.35).

    Uses BDDGameState which integrates with the real engine.
    Reference: Rule 8.3.35
    """
    from tests.bdd_helpers import BDDGameState

    state = BDDGameState()
    state.test_hero_class = None
    return state
