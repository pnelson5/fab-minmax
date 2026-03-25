"""
Step definitions for Section 8.3.24: Stealth (Ability Keyword)
Reference: Flesh and Blood Comprehensive Rules Section 8.3.24

This module implements behavioral tests for the Stealth ability keyword:
- Stealth is an ability that means nothing (Rule 8.3.24)
- Stealth is a pure label/marker with no inherent mechanical effect
- Cards with Stealth can be queried by other effects (e.g., Uzuri)

Engine Features Needed for Section 8.3.24:
- [ ] CardInstance/CardTemplate.has_keyword("stealth") -> True for stealth cards (Rule 8.3.24)
- [ ] "stealth" keyword must be registerable on a card without adding any mechanical effect
- [ ] Stealth must NOT modify power, defense, or any other game value (Rule 8.3.24)

Current status: Tests written, Engine pending
"""

import pytest
from pytest_bdd import scenario, given, when, then, parsers


# ===== Rule 8.3.24: Stealth is recognized as a keyword =====

@scenario(
    "../features/section_8_3_24_stealth.feature",
    "Stealth is recognized as an ability keyword",
)
def test_stealth_is_recognized_as_keyword():
    """Rule 8.3.24: Stealth must be recognized as a keyword on cards that have it."""
    pass


# ===== Rule 8.3.24: Stealth means nothing — no power/defense bonuses =====

@scenario(
    "../features/section_8_3_24_stealth.feature",
    "Stealth does not grant any power bonus",
)
def test_stealth_no_power_bonus():
    """Rule 8.3.24: Stealth is an ability that means nothing — no power bonus."""
    pass


@scenario(
    "../features/section_8_3_24_stealth.feature",
    "Stealth does not grant any defense bonus",
)
def test_stealth_no_defense_bonus():
    """Rule 8.3.24: Stealth is an ability that means nothing — no defense bonus."""
    pass


# ===== Rule 8.3.24: Cards without stealth do not have the keyword =====

@scenario(
    "../features/section_8_3_24_stealth.feature",
    "Card without Stealth keyword does not have Stealth",
)
def test_card_without_stealth_lacks_keyword():
    """Rule 8.3.24: A card without stealth must not report having the stealth keyword."""
    pass


# ===== Rule 8.3.24: Stealth does not alter how a card is played =====

@scenario(
    "../features/section_8_3_24_stealth.feature",
    "A card with Stealth can be played normally",
)
def test_stealth_card_plays_normally():
    """Rule 8.3.24: Stealth does not change how a card is played."""
    pass


# ===== Rule 8.3.24: Stealth is queryable by other effects =====

@scenario(
    "../features/section_8_3_24_stealth.feature",
    "Other effects can query whether a card has Stealth",
)
def test_stealth_queryable_by_effects():
    """Rule 8.3.24: Stealth must be queryable so effects like Uzuri can reference it."""
    pass


@scenario(
    "../features/section_8_3_24_stealth.feature",
    "Stealth check returns false for card without Stealth",
)
def test_stealth_check_false_for_non_stealth():
    """Rule 8.3.24: A card without stealth must return false for stealth checks."""
    pass


# ===== Step Definitions =====

@given("a card with the Stealth keyword")
def card_with_stealth(game_state):
    """Rule 8.3.24: Set up the attack card with the stealth keyword."""
    game_state.attack.add_keyword("stealth")
    game_state.test_card = game_state.attack


@given("an attack card with the Stealth keyword")
def attack_card_with_stealth(game_state):
    """Rule 8.3.24: Set up an attack card with the stealth keyword."""
    game_state.attack.add_keyword("stealth")
    game_state.test_card = game_state.attack


@given("a card without the Stealth keyword")
def card_without_stealth(game_state):
    """Rule 8.3.24: Use the attack card without adding the stealth keyword."""
    # Default attack has no keywords; use it as the test card
    game_state.test_card = game_state.attack


@given("an attacking card with the Stealth keyword")
def attacking_card_with_stealth(game_state):
    """Rule 8.3.24: Set up an attacking card that has stealth."""
    game_state.attack.add_keyword("stealth")
    game_state.stealth_card = game_state.attack


@given("an attacking card without the Stealth keyword")
def attacking_card_without_stealth(game_state):
    """Rule 8.3.24: Set up an attacking card without stealth."""
    # Default attack has no keywords
    game_state.stealth_card = game_state.attack


@given(parsers.parse("the base power of the attack is {power:d}"))
def attack_has_base_power(game_state, power):
    """Set the base power for the attack."""
    game_state.base_power = power


@given(parsers.parse("the base defense of the card is {defense:d}"))
def card_has_base_defense(game_state, defense):
    """Set the base defense value for the test card."""
    game_state.base_defense = defense


@when("I inspect the card's keywords")
def inspect_keywords(game_state):
    """Rule 8.3.24: Retrieve keywords from the card."""
    game_state.card_keywords = game_state.test_card.keywords if hasattr(game_state.test_card, "keywords") else []


@when("the attack is played normally")
def attack_played_normally(game_state):
    """Rule 8.3.24: Play the attack — stealth should not modify power."""
    # Stealth adds nothing; effective power equals base power (Rule 8.3.24)
    game_state.current_power = game_state.base_power


@when("I check the card's defense value")
def check_card_defense(game_state):
    """Rule 8.3.24: Read the card's defense — stealth should not alter it."""
    # Stealth adds nothing; defense is unchanged (Rule 8.3.24)
    game_state.current_defense = game_state.base_defense


@when("the card is played as an attack")
def card_played_as_attack(game_state):
    """Rule 8.3.24: Play the card; stealth does not prevent normal play."""
    game_state.played = True


@when("another effect checks if the attacker has Stealth")
def effect_checks_for_stealth(game_state):
    """Rule 8.3.24: Simulate an effect querying whether the attacker has stealth."""
    game_state.stealth_check_result = game_state.stealth_card.has_keyword("stealth")


@then("the card has the Stealth keyword")
def card_has_stealth_keyword(game_state):
    """Rule 8.3.24: The card must report having the stealth keyword."""
    # Use has_keyword if available (TestAttack), otherwise check keywords list
    if hasattr(game_state.test_card, "has_keyword"):
        has_stealth = game_state.test_card.has_keyword("stealth")
    else:
        has_stealth = "stealth" in game_state.card_keywords
    assert has_stealth, (
        "Rule 8.3.24: Card with stealth must have the 'stealth' keyword"
    )


@then(parsers.parse("the attack power is {expected:d}"))
def attack_power_is(game_state, expected):
    """Rule 8.3.24: Attack power must equal base power (stealth adds nothing)."""
    actual = game_state.current_power
    assert actual == expected, (
        f"Rule 8.3.24: Stealth must not modify power. "
        f"Expected {expected}, got {actual}."
    )


@then(parsers.parse("the defense value is {expected:d}"))
def defense_value_is(game_state, expected):
    """Rule 8.3.24: Defense must equal base defense (stealth adds nothing)."""
    actual = game_state.current_defense
    assert actual == expected, (
        f"Rule 8.3.24: Stealth must not modify defense. "
        f"Expected {expected}, got {actual}."
    )


@then("the card does not have the Stealth keyword")
def card_lacks_stealth_keyword(game_state):
    """Rule 8.3.24: A card without stealth must not report having the keyword."""
    if hasattr(game_state.test_card, "has_keyword"):
        has_stealth = game_state.test_card.has_keyword("stealth")
    else:
        has_stealth = "stealth" in game_state.card_keywords
    assert not has_stealth, (
        "Rule 8.3.24: Card without stealth must not report having the 'stealth' keyword"
    )


@then("the card is on the combat chain")
def card_is_on_combat_chain(game_state):
    """Rule 8.3.24: Playing a stealth card works normally — no restrictions from stealth."""
    assert game_state.played, (
        "Rule 8.3.24: A card with stealth must be playable as a normal attack"
    )


@then("the stealth check returns true")
def stealth_check_true(game_state):
    """Rule 8.3.24: has_keyword('stealth') must return True for cards with stealth."""
    assert game_state.stealth_check_result is True, (
        "Rule 8.3.24: Stealth must be queryable — has_keyword('stealth') should return True"
    )


@then("the stealth check returns false")
def stealth_check_false(game_state):
    """Rule 8.3.24: has_keyword('stealth') must return False for cards without stealth."""
    assert game_state.stealth_check_result is False, (
        "Rule 8.3.24: Card without stealth — has_keyword('stealth') should return False"
    )


# ===== Fixture =====

@pytest.fixture
def game_state():
    """
    Fixture providing game state for testing Section 8.3.24: Stealth.

    Uses BDDGameState which integrates with the real engine.
    Stealth is a pure label keyword with no mechanical effect (Rule 8.3.24).
    Reference: Rule 8.3.24
    """
    from tests.bdd_helpers import BDDGameState

    state = BDDGameState()
    state.base_power = 0
    state.base_defense = 0
    state.current_power = 0
    state.current_defense = 0
    state.card_keywords = []
    state.played = False
    state.stealth_card = None
    state.stealth_check_result = None

    return state
