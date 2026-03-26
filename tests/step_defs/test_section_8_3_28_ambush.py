"""
Step definitions for Section 8.3.28: Ambush (Ability Keyword)
Reference: Flesh and Blood Comprehensive Rules Section 8.3.28

This module implements behavioral tests for the Ambush ability keyword:
- Ambush is a while-static ability (Rule 8.3.28)
- Ambush means: "While this is in your arsenal, you may defend with it." (Rule 8.3.28)
- The ability is only active while the card is in the player's arsenal

Engine Features Needed for Section 8.3.28:
- [ ] AmbushAbility class as a while-static ability (Rule 8.3.28)
- [ ] AmbushAbility.is_while_static -> True (Rule 8.3.28)
- [ ] AmbushAbility.condition: "while this is in your arsenal" (Rule 8.3.28)
- [ ] AmbushAbility.meaning: the text of the ability (Rule 8.3.28)
- [ ] AmbushAbility.is_active(zone) -> bool: True only when card is in arsenal (Rule 8.3.28)
- [ ] Engine must allow defending with an Ambush card from the arsenal (Rule 8.3.28)
- [ ] Engine must deny defending with non-Ambush cards from the arsenal (Rule 8.3.28)
- [ ] Engine must deny defending with an Ambush card from any zone other than arsenal (Rule 8.3.28)

Current status: Tests written, Engine pending
"""

import pytest
from pytest_bdd import scenario, given, when, then, parsers

from fab_engine.zones.zone import ZoneType


# ===== Rule 8.3.28: Ambush is recognized as a keyword =====

@scenario(
    "../features/section_8_3_28_ambush.feature",
    "Ambush is recognized as an ability keyword",
)
def test_ambush_is_recognized_as_keyword():
    """Rule 8.3.28: Ambush must be recognized as a keyword on cards that have it."""
    pass


# ===== Rule 8.3.28: Ambush is a while-static ability =====

@scenario(
    "../features/section_8_3_28_ambush.feature",
    "Ambush is a while-static ability",
)
def test_ambush_is_while_static_ability():
    """Rule 8.3.28: Ambush must be classified as a while-static ability."""
    pass


# ===== Rule 8.3.28: Ambush card in arsenal can defend =====

@scenario(
    "../features/section_8_3_28_ambush.feature",
    "Card with Ambush in the arsenal can be used to defend",
)
def test_ambush_card_in_arsenal_can_defend():
    """Rule 8.3.28: A card with Ambush in the arsenal may be used to defend."""
    pass


# ===== Rule 8.3.28: Ambush card in hand uses normal defend rules =====

@scenario(
    "../features/section_8_3_28_ambush.feature",
    "Card with Ambush in hand cannot use Ambush ability to defend",
)
def test_ambush_card_in_hand_uses_normal_defend():
    """Rule 8.3.28: Card with Ambush in hand defends normally (not via Ambush)."""
    pass


# ===== Rule 8.3.28: Card without Ambush in arsenal cannot defend =====

@scenario(
    "../features/section_8_3_28_ambush.feature",
    "Card without Ambush in the arsenal cannot be used to defend",
)
def test_non_ambush_card_in_arsenal_cannot_defend():
    """Rule 8.3.28: Cards without Ambush in the arsenal cannot be used to defend."""
    pass


# ===== Rule 8.3.28: Ambush card in banished zone cannot defend =====

@scenario(
    "../features/section_8_3_28_ambush.feature",
    "Card with Ambush in the banished zone cannot use Ambush ability",
)
def test_ambush_card_in_banished_cannot_defend():
    """Rule 8.3.28: Ambush is inactive when card is not in the arsenal."""
    pass


# ===== Rule 8.3.28: Ambush is active while card is in the arsenal =====

@scenario(
    "../features/section_8_3_28_ambush.feature",
    "Ambush while-static ability is only active while in the arsenal",
)
def test_ambush_active_in_arsenal():
    """Rule 8.3.28: Ambush while-static is active when card is in the arsenal."""
    pass


# ===== Rule 8.3.28: Ambush is inactive outside the arsenal =====

@scenario(
    "../features/section_8_3_28_ambush.feature",
    "Ambush while-static ability is inactive when card is not in the arsenal",
)
def test_ambush_inactive_outside_arsenal():
    """Rule 8.3.28: Ambush while-static is inactive when card is not in the arsenal."""
    pass


# ===== Rule 8.3.28: Ambush meaning matches the comprehensive rules =====

@scenario(
    "../features/section_8_3_28_ambush.feature",
    "Ambush ability meaning matches comprehensive rules text",
)
def test_ambush_meaning_matches_rules():
    """Rule 8.3.28: The Ambush ability meaning must match the comprehensive rules text."""
    pass


# ===== Given Steps =====

@given("a card with the Ambush keyword")
def ambush_card(game_state):
    """Rule 8.3.28: Create a card that has the Ambush keyword."""
    card = game_state.create_card(name="Ambush Test Card")
    game_state.test_card = card
    game_state.test_card_has_ambush = True


@given("a card without the Ambush keyword")
def non_ambush_card(game_state):
    """Rule 8.3.28: Create a card that does NOT have the Ambush keyword."""
    card = game_state.create_card(name="Non-Ambush Test Card")
    game_state.test_card = card
    game_state.test_card_has_ambush = False


@given("the card is in the player's arsenal")
def card_in_arsenal(game_state):
    """Rule 8.3.28: Place the test card in the player's arsenal zone."""
    game_state.player.arsenal.add_card(game_state.test_card)
    game_state.test_card_zone = ZoneType.ARSENAL


@given("the card is in the player's hand")
def card_in_hand(game_state):
    """Rule 8.3.28: Place the test card in the player's hand zone."""
    game_state.player.hand.add_card(game_state.test_card)
    game_state.test_card_zone = ZoneType.HAND


@given("the card is in the player's banished zone")
def card_in_banished(game_state):
    """Rule 8.3.28: Place the test card in the player's banished zone."""
    game_state.player.banished_zone.add_card(game_state.test_card)
    game_state.test_card_zone = ZoneType.BANISHED


@given("the card is in the player's graveyard")
def card_in_graveyard(game_state):
    """Rule 8.3.28: Place the test card in the player's hand (non-arsenal zone)."""
    game_state.player.hand.add_card(game_state.test_card)
    game_state.test_card_zone = ZoneType.HAND


@given("there is an active attack")
def active_attack(game_state):
    """Rule 8.3.28: Set up an active attack for the defend attempt."""
    from tests.bdd_helpers.core import TestAttack
    game_state.active_attack = TestAttack()


# ===== When Steps =====

@when("I inspect the card's keywords")
def inspect_keywords(game_state):
    """Rule 8.3.28: Inspect the keywords on the test card."""
    try:
        game_state.card_keywords = game_state.test_card.keywords
    except AttributeError:
        game_state.card_keywords = None


@when("I check the ability type of Ambush")
def check_ability_type(game_state):
    """Rule 8.3.28: Check whether Ambush is classified as a while-static ability."""
    try:
        ambush_ability = game_state.test_card.get_ability("ambush")
        game_state.ambush_ability = ambush_ability
        game_state.ambush_is_while_static = getattr(ambush_ability, "is_while_static", False)
    except (AttributeError, TypeError):
        game_state.ambush_ability = None
        game_state.ambush_is_while_static = False


@when("the player attempts to defend with the Ambush card from the arsenal")
def attempt_defend_from_arsenal_with_ambush(game_state):
    """Rule 8.3.28: Attempt to defend using an Ambush card from the arsenal."""
    try:
        game_state.defend_result = game_state.player.attempt_defend_from_arsenal(
            game_state.active_attack,
            game_state.test_card,
        )
    except (AttributeError, NotImplementedError):
        # Engine does not yet support defend from arsenal
        game_state.defend_result = None


@when("the player attempts to defend with the Ambush card from the hand")
def attempt_defend_from_hand_with_ambush(game_state):
    """Rule 8.3.28: Attempt to defend using an Ambush card from the hand (normal)."""
    try:
        game_state.defend_result = game_state.player.attempt_defend(
            game_state.active_attack,
            [game_state.test_card],
        )
    except (AttributeError, NotImplementedError):
        game_state.defend_result = None


@when("the player attempts to defend with the non-Ambush arsenal card")
def attempt_defend_from_arsenal_without_ambush(game_state):
    """Rule 8.3.28: Attempt to defend from arsenal with a card that has no Ambush."""
    try:
        game_state.defend_result = game_state.player.attempt_defend_from_arsenal(
            game_state.active_attack,
            game_state.test_card,
        )
    except (AttributeError, NotImplementedError):
        game_state.defend_result = None


@when("the player attempts to defend with the Ambush card from the banished zone")
def attempt_defend_from_banished_with_ambush(game_state):
    """Rule 8.3.28: Attempt to defend from the banished zone (Ambush inactive)."""
    try:
        game_state.defend_result = game_state.player.attempt_defend_from_zone(
            game_state.active_attack,
            game_state.test_card,
            zone=ZoneType.BANISHED,
        )
    except (AttributeError, NotImplementedError):
        game_state.defend_result = None


@when("I check whether Ambush is active")
def check_ambush_active(game_state):
    """Rule 8.3.28: Check whether the Ambush while-static is currently active."""
    try:
        ambush_ability = game_state.test_card.get_ability("ambush")
        game_state.ambush_is_active = ambush_ability.is_active(game_state.test_card_zone)
    except (AttributeError, NotImplementedError, TypeError):
        game_state.ambush_is_active = None


@when("I check the meaning of the Ambush ability")
def check_ambush_meaning(game_state):
    """Rule 8.3.28: Retrieve the meaning text of the Ambush ability."""
    try:
        ambush_ability = game_state.test_card.get_ability("ambush")
        game_state.ambush_meaning = ambush_ability.meaning
    except (AttributeError, TypeError):
        game_state.ambush_meaning = None


# ===== Then Steps =====

@then("the card has the Ambush keyword")
def card_has_ambush_keyword(game_state):
    """Rule 8.3.28: The card must have Ambush in its list of keywords."""
    assert game_state.card_keywords is not None, (
        "Engine feature needed: CardInstance.keywords property (Rule 8.3.28)"
    )
    assert "ambush" in [k.lower() for k in game_state.card_keywords], (
        "Engine feature needed: Ambush keyword must appear in card.keywords (Rule 8.3.28)"
    )


@then("Ambush is a while-static ability")
def ambush_is_while_static(game_state):
    """Rule 8.3.28: Ambush must be classified as a while-static ability."""
    assert game_state.ambush_ability is not None, (
        "Engine feature needed: CardInstance.get_ability('ambush') (Rule 8.3.28)"
    )
    assert game_state.ambush_is_while_static, (
        "Engine feature needed: AmbushAbility.is_while_static must be True (Rule 8.3.28)"
    )


@then("the defend attempt succeeds")
def defend_attempt_succeeds(game_state):
    """Rule 8.3.28: Defending with an Ambush card from the arsenal must be allowed."""
    assert game_state.defend_result is not None, (
        "Engine feature needed: Player.attempt_defend_from_arsenal() (Rule 8.3.28)"
    )
    assert game_state.defend_result.success, (
        "Engine feature needed: Ambush must allow defending from arsenal (Rule 8.3.28). "
        f"Got: {game_state.defend_result.message}"
    )


@then("the defend from hand succeeds normally")
def defend_from_hand_succeeds(game_state):
    """Rule 8.3.28: Defending from the hand is a normal action (not Ambush-specific)."""
    assert game_state.defend_result is not None, (
        "Engine feature needed: Player.attempt_defend() (Rule 8.3.28)"
    )
    assert game_state.defend_result.success, (
        "Engine feature needed: Defending from hand must succeed normally (Rule 8.3.28). "
        f"Got: {game_state.defend_result.message}"
    )


@then("the defend attempt from arsenal is blocked")
def defend_from_arsenal_blocked_without_ambush(game_state):
    """Rule 8.3.28: Without Ambush, defending from the arsenal must not be allowed."""
    assert game_state.defend_result is not None, (
        "Engine feature needed: Player.attempt_defend_from_arsenal() (Rule 8.3.28)"
    )
    assert not game_state.defend_result.success, (
        "Engine feature needed: Non-Ambush cards must not be usable to defend from arsenal "
        "(Rule 8.3.28). Got success=True unexpectedly."
    )


@then("the defend attempt from banished is blocked")
def defend_from_banished_blocked(game_state):
    """Rule 8.3.28: Ambush is inactive outside the arsenal; defend from banished must be blocked."""
    assert game_state.defend_result is not None, (
        "Engine feature needed: Player.attempt_defend_from_zone() (Rule 8.3.28)"
    )
    assert not game_state.defend_result.success, (
        "Engine feature needed: Ambush inactive outside arsenal; defending from banished "
        "must be blocked (Rule 8.3.28). Got success=True unexpectedly."
    )


@then("Ambush is active because the card is in the arsenal")
def ambush_is_active_in_arsenal(game_state):
    """Rule 8.3.28: Ambush while-static must be active when the card is in the arsenal."""
    assert game_state.ambush_is_active is not None, (
        "Engine feature needed: AmbushAbility.is_active(zone) method (Rule 8.3.28)"
    )
    assert game_state.ambush_is_active, (
        "Engine feature needed: Ambush must be active while card is in the arsenal "
        "(Rule 8.3.28)"
    )


@then("Ambush is inactive because the card is not in the arsenal")
def ambush_is_inactive_outside_arsenal(game_state):
    """Rule 8.3.28: Ambush while-static must be inactive when the card is not in the arsenal."""
    assert game_state.ambush_is_active is not None, (
        "Engine feature needed: AmbushAbility.is_active(zone) method (Rule 8.3.28)"
    )
    assert not game_state.ambush_is_active, (
        "Engine feature needed: Ambush must be inactive when card is not in arsenal "
        "(Rule 8.3.28)"
    )


@then(parsers.parse('the Ambush meaning is "{meaning}"'))
def ambush_meaning_matches(game_state, meaning):
    """Rule 8.3.28: The Ambush ability meaning must match the comprehensive rules."""
    assert game_state.ambush_meaning is not None, (
        "Engine feature needed: AmbushAbility.meaning property (Rule 8.3.28)"
    )
    assert game_state.ambush_meaning == meaning, (
        f"Engine feature needed: AmbushAbility.meaning must match CR text. "
        f"Expected: '{meaning}', Got: '{game_state.ambush_meaning}' (Rule 8.3.28)"
    )


# ===== Fixtures =====

@pytest.fixture
def game_state():
    """
    Fixture providing game state for Ambush ability testing.

    Uses BDDGameState which integrates with the real engine.
    Reference: Rule 8.3.28 - Ambush
    """
    from tests.bdd_helpers import BDDGameState

    state = BDDGameState()
    state.test_card = None
    state.test_card_has_ambush = False
    state.test_card_zone = None
    state.active_attack = None
    state.card_keywords = None
    state.ambush_ability = None
    state.ambush_is_while_static = False
    state.ambush_is_active = None
    state.ambush_meaning = None
    state.defend_result = None

    return state
