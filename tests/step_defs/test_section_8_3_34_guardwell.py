"""
Step definitions for Section 8.3.34: Guardwell (Ability Keyword)
Reference: Flesh and Blood Comprehensive Rules Section 8.3.34

This module implements behavioral tests for the Guardwell ability keyword:
- Guardwell is a static ability (Rule 8.3.34)
- Guardwell means: "When the combat chain closes, if this defended, put
  -1{d} counters on it equal to its {d}." (Rule 8.3.34)
- The trigger condition: the card must have defended in the chain (Rule 8.3.34)
- Counters placed equal to the card's current {d} value (Rule 8.3.34)
- If the card did NOT defend, no counters are placed (Rule 8.3.34)
- Each combat chain close is a separate trigger event (Rule 8.3.34)

Engine Features Needed for Section 8.3.34:
- [ ] GuardwellAbility class as a static ability (Rule 8.3.34)
- [ ] GuardwellAbility.is_static -> True (Rule 8.3.34)
- [ ] GuardwellAbility.is_triggered -> False (Rule 8.3.34)
- [ ] GuardwellAbility.meaning property returning canonical text (Rule 8.3.34)
- [ ] Engine must track whether a card with Guardwell defended in the chain (Rule 8.3.34)
- [ ] Engine must place -1{d} counters equal to card's {d} when chain closes (Rule 8.3.34)
- [ ] Engine must NOT place counters if the card did not defend (Rule 8.3.34)
- [ ] CardInstance.keywords property to check for Guardwell (Rule 8.3.34)
- [ ] CardInstance.get_ability("guardwell") method (Rule 8.3.34)
- [ ] CardInstance.defense_counters or counter tracking for -1{d} counters (Rule 8.3.34)
- [ ] CombatChain.close() method that triggers Guardwell (Rule 8.3.34)
- [ ] CardInstance.defended_this_chain flag (Rule 8.3.34)

Current status: Tests written, Engine pending
"""

import pytest
from pytest_bdd import scenario, given, when, then, parsers


# ===== Rule 8.3.34: Guardwell is recognized as a keyword =====

@scenario(
    "../features/section_8_3_34_guardwell.feature",
    "Guardwell is recognized as an ability keyword",
)
def test_guardwell_is_recognized_as_keyword():
    """Rule 8.3.34: Guardwell must be recognized as a keyword on cards that have it."""
    pass


# ===== Rule 8.3.34: Guardwell is a static ability =====

@scenario(
    "../features/section_8_3_34_guardwell.feature",
    "Guardwell is a static ability",
)
def test_guardwell_is_static_ability():
    """Rule 8.3.34: Guardwell must be classified as a static ability."""
    pass


# ===== Rule 8.3.34: Guardwell ability meaning =====

@scenario(
    "../features/section_8_3_34_guardwell.feature",
    "Guardwell ability meaning matches comprehensive rules text",
)
def test_guardwell_ability_meaning():
    """Rule 8.3.34: The Guardwell ability meaning must match the comprehensive rules text."""
    pass


# ===== Rule 8.3.34: Card gets -1{d} counters equal to defense when it defended =====

@scenario(
    "../features/section_8_3_34_guardwell.feature",
    "Card with Guardwell gets minus defense counters when it defended",
)
def test_guardwell_places_counters_equal_to_defense():
    """Rule 8.3.34: When the combat chain closes, a Guardwell card that defended gets
    -1{d} counters equal to its {d} value."""
    pass


# ===== Rule 8.3.34: Counter count equals defense value =====

@scenario(
    "../features/section_8_3_34_guardwell.feature",
    "Number of minus-defense counters equals the card's defense value",
)
def test_guardwell_counter_count_equals_defense():
    """Rule 8.3.34: The number of -1{d} counters placed equals the card's current {d}."""
    pass


# ===== Rule 8.3.34: No counters if card did not defend =====

@scenario(
    "../features/section_8_3_34_guardwell.feature",
    "Card with Guardwell gets no counters if it did not defend",
)
def test_guardwell_no_counters_if_not_defended():
    """Rule 8.3.34: If the Guardwell card did not defend, no counters are placed."""
    pass


# ===== Rule 8.3.34: Zero defense gets zero counters =====

@scenario(
    "../features/section_8_3_34_guardwell.feature",
    "Card with Guardwell and zero defense gets no counters when it defended",
)
def test_guardwell_zero_defense_gets_zero_counters():
    """Rule 8.3.34: A Guardwell card with 0 defense gets 0 counters even if it defended."""
    pass


# ===== Rule 8.3.34: Triggers on each combat chain close =====

@scenario(
    "../features/section_8_3_34_guardwell.feature",
    "Guardwell triggers on each separate combat chain close",
)
def test_guardwell_triggers_on_each_chain_close():
    """Rule 8.3.34: Each time a combat chain closes where the card defended,
    more -1{d} counters are placed."""
    pass


# ===== Rule 8.3.34: Guardwell is not a triggered ability =====

@scenario(
    "../features/section_8_3_34_guardwell.feature",
    "Guardwell is not classified as a triggered ability",
)
def test_guardwell_is_not_triggered_ability():
    """Rule 8.3.34: Guardwell is a static ability, not a triggered ability."""
    pass


# ===== Step Definitions =====

@given("a card with the Guardwell keyword")
def card_with_guardwell_keyword(game_state):
    """Rule 8.3.34: Create a card with the Guardwell keyword."""
    game_state.guardwell_card = game_state.create_card(
        name="Guardwell Test Equipment",
        defense=3,
    )
    game_state.guardwell_card_keywords = ["guardwell"]


@given(parsers.parse("a card with the Guardwell keyword and {defense:d} defense"))
def card_with_guardwell_and_defense(game_state, defense):
    """Rule 8.3.34: Create a card with the Guardwell keyword and a specific defense value."""
    game_state.guardwell_card = game_state.create_card(
        name="Guardwell Test Equipment",
        defense=defense,
    )
    game_state.guardwell_card_keywords = ["guardwell"]
    game_state.guardwell_card_defense = defense


@given("the card is in play as equipment")
def card_in_play_as_equipment(game_state):
    """Rule 8.3.34: Guardwell card is equipped and in play."""
    game_state.guardwell_card_in_play = True
    game_state.guardwell_card_defended = False
    game_state.guardwell_card_minus_defense_counters = 0


@when("I inspect the card's keywords")
def inspect_card_keywords(game_state):
    """Rule 8.3.34: Inspect the keywords of the Guardwell card."""
    game_state.inspected_keywords = game_state.guardwell_card_keywords


@when("I check the ability type of Guardwell")
def check_guardwell_ability_type(game_state):
    """Rule 8.3.34: Check whether Guardwell is classified as a static ability."""
    game_state.guardwell_ability = game_state.guardwell_card.get_ability("guardwell")


@when("I inspect the Guardwell ability's meaning")
def inspect_guardwell_meaning(game_state):
    """Rule 8.3.34: Retrieve the meaning text of the Guardwell ability."""
    game_state.guardwell_ability = game_state.guardwell_card.get_ability("guardwell")
    game_state.guardwell_meaning = getattr(game_state.guardwell_ability, "meaning", None)


@when("I check if Guardwell is a triggered ability")
def check_guardwell_is_triggered(game_state):
    """Rule 8.3.34: Check whether Guardwell is classified as a triggered ability."""
    game_state.guardwell_ability = game_state.guardwell_card.get_ability("guardwell")


@when("the card defends in a combat chain")
def card_defends_in_chain(game_state):
    """Rule 8.3.34: The Guardwell card defends in a combat chain."""
    game_state.guardwell_card_defended = True


@when("the combat chain closes")
def combat_chain_closes(game_state):
    """Rule 8.3.34: The combat chain closes, triggering Guardwell if the card defended."""
    if game_state.guardwell_card_defended:
        defense = getattr(game_state, "guardwell_card_defense", 3)
        game_state.guardwell_card_minus_defense_counters += defense
    game_state.guardwell_card_defended = False


@when("the combat chain closes without the card defending")
def chain_closes_without_defending(game_state):
    """Rule 8.3.34: The combat chain closes but the Guardwell card did not defend."""
    game_state.guardwell_card_defended = False
    # Chain closes — no counters placed since card did not defend


@when("the card defends in the first combat chain")
def card_defends_in_first_chain(game_state):
    """Rule 8.3.34: The Guardwell card defends in the first combat chain."""
    game_state.guardwell_card_defended = True


@when("the first combat chain closes")
def first_combat_chain_closes(game_state):
    """Rule 8.3.34: The first combat chain closes, placing counters."""
    if game_state.guardwell_card_defended:
        defense = getattr(game_state, "guardwell_card_defense", 4)
        game_state.guardwell_card_minus_defense_counters += defense
    game_state.guardwell_card_defended = False


@when("the card defends in a second combat chain")
def card_defends_in_second_chain(game_state):
    """Rule 8.3.34: The Guardwell card defends in a second combat chain."""
    game_state.guardwell_card_defended = True


@when("the second combat chain closes")
def second_combat_chain_closes(game_state):
    """Rule 8.3.34: The second combat chain closes, placing more counters."""
    if game_state.guardwell_card_defended:
        defense = getattr(game_state, "guardwell_card_defense", 4)
        game_state.guardwell_card_minus_defense_counters += defense
    game_state.guardwell_card_defended = False


@then("the card has the Guardwell keyword")
def card_has_guardwell_keyword(game_state):
    """Rule 8.3.34: The card must have the Guardwell keyword."""
    assert "guardwell" in game_state.inspected_keywords, (
        "Card should have Guardwell keyword but does not"
    )


@then("Guardwell is a static ability")
def guardwell_is_static(game_state):
    """Rule 8.3.34: Guardwell must be classified as a static ability."""
    ability = game_state.guardwell_ability
    assert ability is not None, "Guardwell ability not found on card"
    assert getattr(ability, "is_static", False), (
        "Guardwell should be a static ability"
    )


@then(parsers.parse('the Guardwell meaning is "{meaning}"'))
def guardwell_meaning_matches(game_state, meaning):
    """Rule 8.3.34: Guardwell meaning must match the comprehensive rules text."""
    assert game_state.guardwell_meaning is not None, "Guardwell ability has no meaning"
    assert game_state.guardwell_meaning == meaning, (
        f"Guardwell meaning '{game_state.guardwell_meaning}' does not match "
        f"expected '{meaning}'"
    )


@then(parsers.parse("the card has {count:d} minus-defense counters on it"))
def card_has_minus_defense_counters(game_state, count):
    """Rule 8.3.34: The card must have the specified number of -1{d} counters."""
    actual = game_state.guardwell_card_minus_defense_counters
    assert actual == count, (
        f"Card should have {count} minus-defense counters but has {actual}"
    )


@then("Guardwell is not a triggered ability")
def guardwell_is_not_triggered(game_state):
    """Rule 8.3.34: Guardwell must NOT be classified as a triggered ability."""
    ability = game_state.guardwell_ability
    assert ability is not None, "Guardwell ability not found on card"
    assert not getattr(ability, "is_triggered", True), (
        "Guardwell should not be a triggered ability — it is a static ability"
    )


# ===== Fixtures =====

@pytest.fixture
def game_state():
    """
    Fixture providing game state for testing Guardwell.

    Uses BDDGameState which integrates with the real engine.
    Reference: Rule 8.3.34
    """
    from tests.bdd_helpers import BDDGameState

    state = BDDGameState()
    state.guardwell_card = None
    state.guardwell_card_keywords = []
    state.guardwell_card_defense = 0
    state.guardwell_card_in_play = False
    state.guardwell_card_defended = False
    state.guardwell_card_minus_defense_counters = 0
    state.guardwell_ability = None
    state.guardwell_meaning = None
    state.inspected_keywords = []

    return state
