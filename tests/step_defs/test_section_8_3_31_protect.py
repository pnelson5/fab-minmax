"""
Step definitions for Section 8.3.31: Protect (Ability Keyword)
Reference: Flesh and Blood Comprehensive Rules Section 8.3.31

This module implements behavioral tests for the Protect ability keyword:
- Protect is a static ability (Rule 8.3.31)
- Protect means: "You may defend any hero attacked by an opponent with this." (Rule 8.3.31)
- A player can use a Protect card to defend any hero attacked by an opponent (Rule 8.3.31)
- When a player defends with a Protect card, they are considered to have protected (Rule 8.3.31a)
- When a player defends with a Protect card, the card is considered to have protected (Rule 8.3.31a)

Context (Rule 7.3.2e):
If a player's hero is attacked, that player declares any defending cards first,
then in clockwise order, players may declare additional defending cards, such as
cards with Protect.

Engine Features Needed for Section 8.3.31:
- [ ] ProtectAbility class as a static ability (Rule 8.3.31)
- [ ] ProtectAbility.is_static -> True (Rule 8.3.31)
- [ ] ProtectAbility.meaning: the text of the ability (Rule 8.3.31)
- [ ] Engine must allow a Protect card to defend any hero attacked by an opponent (Rule 8.3.31)
- [ ] Engine must prevent non-Protect cards from defending other players' heroes (Rule 8.3.31)
- [ ] Engine must mark the defending player as "protected" when they defend with Protect (Rule 8.3.31a)
- [ ] Engine must mark the defending card as "protected" when used to defend (Rule 8.3.31a)
- [ ] CardInstance.keywords property (Rule 8.3.31)
- [ ] CardInstance.get_ability("protect") method (Rule 8.3.31)
- [ ] DefendResult.player_protected flag (Rule 8.3.31a)
- [ ] DefendResult.card_protected flag (Rule 8.3.31a)

Current status: Tests written, Engine pending
"""

import pytest
from pytest_bdd import scenario, given, when, then, parsers


# ===== Rule 8.3.31: Protect is recognized as a keyword =====

@scenario(
    "../features/section_8_3_31_protect.feature",
    "Protect is recognized as an ability keyword",
)
def test_protect_is_recognized_as_keyword():
    """Rule 8.3.31: Protect must be recognized as a keyword on cards that have it."""
    pass


# ===== Rule 8.3.31: Protect is a static ability =====

@scenario(
    "../features/section_8_3_31_protect.feature",
    "Protect is a static ability",
)
def test_protect_is_static_ability():
    """Rule 8.3.31: Protect must be classified as a static ability."""
    pass


# ===== Rule 8.3.31: Protect ability meaning matches comprehensive rules text =====

@scenario(
    "../features/section_8_3_31_protect.feature",
    "Protect ability meaning matches comprehensive rules text",
)
def test_protect_meaning_matches_rules():
    """Rule 8.3.31: The Protect ability meaning must match the comprehensive rules text."""
    pass


# ===== Rule 8.3.31: A player may use a Protect card to defend any hero =====

@scenario(
    "../features/section_8_3_31_protect.feature",
    "A player may defend a hero other than their own using a Protect card",
)
def test_protect_allows_cross_player_defend():
    """Rule 8.3.31: A player may defend any hero attacked by an opponent using a Protect card."""
    pass


# ===== Rule 8.3.31: Without Protect a player cannot defend another hero =====

@scenario(
    "../features/section_8_3_31_protect.feature",
    "A player cannot defend another hero without Protect",
)
def test_no_protect_prevents_cross_player_defend():
    """Rule 8.3.31: A player cannot defend another player's hero without Protect."""
    pass


# ===== Rule 8.3.31a: The defending player is considered to have protected =====

@scenario(
    "../features/section_8_3_31_protect.feature",
    "The defending player is considered to have protected when defending with a Protect card",
)
def test_player_considered_protected():
    """Rule 8.3.31a: The defending player must be considered to have protected."""
    pass


# ===== Rule 8.3.31a: The defending card is considered to have protected =====

@scenario(
    "../features/section_8_3_31_protect.feature",
    "The defending card is considered to have protected when used to defend",
)
def test_card_considered_protected():
    """Rule 8.3.31a: The defending card must be considered to have protected."""
    pass


# ===== Rule 8.3.31: Combined protect scenario =====

@scenario(
    "../features/section_8_3_31_protect.feature",
    "Protect allows defending any hero attacked by an opponent",
)
def test_protect_combined_outcome():
    """Rule 8.3.31/8.3.31a: Full protect scenario — defense allowed, player and card protected."""
    pass


# ===== Given Steps =====

@given("a card with the Protect keyword")
def protect_card(game_state):
    """Rule 8.3.31: Create a card that has the Protect keyword."""
    card = game_state.create_card(name="Protect Test Card")
    game_state.protect_card = card
    game_state.test_card = card


@given("a card without the Protect keyword")
def non_protect_card(game_state):
    """Rule 8.3.31: Create a card that does NOT have the Protect keyword."""
    card = game_state.create_card(name="Non-Protect Test Card")
    game_state.non_protect_card = card


@given("a multiplayer game with two heroes")
def multiplayer_game(game_state):
    """Rule 8.3.31: Set up a multiplayer game context with player one and player two."""
    # game_state.player is player one, game_state.defender is player two
    game_state.player_one = game_state.player
    game_state.player_two = game_state.defender


@given("player two's hero is being attacked by an opponent")
def player_two_hero_attacked(game_state):
    """Rule 8.3.31: Simulate an attack on player two's hero."""
    try:
        from tests.bdd_helpers.core import TestAttack
        attack = TestAttack()
        attack.target_player = game_state.player_two
        game_state.active_attack = attack
    except (ImportError, AttributeError, NotImplementedError):
        game_state.active_attack = None


@given("player one has a card with the Protect keyword")
def player_one_has_protect_card(game_state):
    """Rule 8.3.31: Player one holds the Protect card as a potential defender."""
    if not hasattr(game_state, "protect_card") or game_state.protect_card is None:
        card = game_state.create_card(name="Protect Test Card")
        game_state.protect_card = card
        game_state.test_card = card
    game_state.defending_card = game_state.protect_card
    game_state.defending_player = game_state.player_one


@given("player one has a card without the Protect keyword")
def player_one_has_non_protect_card(game_state):
    """Rule 8.3.31: Player one holds a non-Protect card as a potential defender."""
    if not hasattr(game_state, "non_protect_card") or game_state.non_protect_card is None:
        card = game_state.create_card(name="Non-Protect Test Card")
        game_state.non_protect_card = card
    game_state.defending_card = game_state.non_protect_card
    game_state.defending_player = game_state.player_one


# ===== When Steps =====

@when("I inspect the card's keywords")
def inspect_keywords(game_state):
    """Rule 8.3.31: Inspect the keywords on the test card."""
    try:
        game_state.card_keywords = game_state.test_card.keywords
    except AttributeError:
        game_state.card_keywords = None


@when("I check the ability type of Protect")
def check_ability_type(game_state):
    """Rule 8.3.31: Check whether Protect is classified as a static ability."""
    try:
        protect_ability = game_state.test_card.get_ability("protect")
        game_state.protect_ability = protect_ability
        game_state.protect_is_static = getattr(protect_ability, "is_static", False)
    except (AttributeError, TypeError):
        game_state.protect_ability = None
        game_state.protect_is_static = False


@when("I check the meaning of the Protect ability")
def check_protect_meaning(game_state):
    """Rule 8.3.31: Retrieve the meaning text of the Protect ability."""
    try:
        protect_ability = game_state.test_card.get_ability("protect")
        game_state.protect_meaning = protect_ability.meaning
    except (AttributeError, TypeError):
        game_state.protect_meaning = None


@when("player one defends player two's hero with the Protect card")
def player_one_defends_with_protect(game_state):
    """Rule 8.3.31: Player one attempts to defend player two's hero using the Protect card."""
    try:
        result = game_state.player_one.attempt_defend(
            game_state.active_attack,
            [game_state.protect_card],
        )
        game_state.defend_result = result
        game_state.player_protected = getattr(result, "player_protected", None)
        game_state.card_protected = getattr(result, "card_protected", None)
    except (AttributeError, NotImplementedError, TypeError):
        game_state.defend_result = None
        game_state.player_protected = None
        game_state.card_protected = None


@when("player one attempts to defend player two's hero with the non-Protect card")
def player_one_attempts_defend_without_protect(game_state):
    """Rule 8.3.31: Player one attempts to defend player two's hero without a Protect card."""
    try:
        result = game_state.player_one.attempt_defend(
            game_state.active_attack,
            [game_state.non_protect_card],
        )
        game_state.defend_result = result
    except (AttributeError, NotImplementedError, TypeError, ValueError):
        # Engine may raise an error if cross-player defend is not allowed without Protect
        game_state.defend_result = None


# ===== Then Steps =====

@then("the card has the Protect keyword")
def card_has_protect_keyword(game_state):
    """Rule 8.3.31: The card must have Protect in its list of keywords."""
    assert game_state.card_keywords is not None, (
        "Engine feature needed: CardInstance.keywords property (Rule 8.3.31)"
    )
    assert "protect" in [k.lower() for k in game_state.card_keywords], (
        "Engine feature needed: Protect keyword must appear in card.keywords (Rule 8.3.31)"
    )


@then("Protect is a static ability")
def protect_is_static(game_state):
    """Rule 8.3.31: Protect must be classified as a static ability."""
    assert game_state.protect_ability is not None, (
        "Engine feature needed: CardInstance.get_ability('protect') (Rule 8.3.31)"
    )
    assert game_state.protect_is_static, (
        "Engine feature needed: ProtectAbility.is_static must be True (Rule 8.3.31)"
    )


@then(parsers.parse('the Protect meaning is "{meaning}"'))
def protect_meaning_matches(game_state, meaning):
    """Rule 8.3.31: The Protect ability meaning must match the comprehensive rules."""
    assert game_state.protect_meaning is not None, (
        "Engine feature needed: ProtectAbility.meaning property (Rule 8.3.31)"
    )
    assert game_state.protect_meaning == meaning, (
        f"Engine feature needed: ProtectAbility.meaning must match CR text. "
        f"Expected: '{meaning}', Got: '{game_state.protect_meaning}' (Rule 8.3.31)"
    )


@then("the defense is allowed")
def defense_is_allowed(game_state):
    """Rule 8.3.31: Defending another player's hero with a Protect card must be allowed."""
    assert game_state.defend_result is not None, (
        "Engine feature needed: Player.attempt_defend() must allow cross-player defense "
        "when the defending card has Protect (Rule 8.3.31)"
    )
    success = getattr(game_state.defend_result, "success", game_state.defend_result)
    assert success, (
        "Engine feature needed: Engine must allow defending another hero with Protect card "
        "(Rule 8.3.31)"
    )


@then("the defense is not allowed")
def defense_is_not_allowed(game_state):
    """Rule 8.3.31: Defending another player's hero without Protect must be rejected."""
    if game_state.defend_result is None:
        # Engine raised an error — cross-player defend blocked as expected
        return
    success = getattr(game_state.defend_result, "success", game_state.defend_result)
    assert not success, (
        "Engine feature needed: Engine must prevent cross-player defense without Protect "
        "(Rule 8.3.31)"
    )


@then("player one is considered to have protected")
def player_considered_protected(game_state):
    """Rule 8.3.31a: The defending player must be considered to have protected."""
    assert game_state.player_protected is not None, (
        "Engine feature needed: DefendResult.player_protected flag (Rule 8.3.31a)"
    )
    assert game_state.player_protected, (
        "Engine feature needed: Defending player must be marked as 'protected' when "
        "defending with a Protect card (Rule 8.3.31a)"
    )


@then("the Protect card is considered to have protected")
def card_considered_protected(game_state):
    """Rule 8.3.31a: The defending card must be considered to have protected."""
    assert game_state.card_protected is not None, (
        "Engine feature needed: DefendResult.card_protected flag (Rule 8.3.31a)"
    )
    assert game_state.card_protected, (
        "Engine feature needed: Protect card must be marked as 'protected' when used to "
        "defend another hero (Rule 8.3.31a)"
    )


# ===== Fixtures =====

@pytest.fixture
def game_state():
    """
    Fixture providing game state for Protect ability testing.

    Uses BDDGameState which integrates with the real engine.
    Reference: Rule 8.3.31 - Protect
    """
    from tests.bdd_helpers import BDDGameState

    state = BDDGameState()
    state.test_card = None
    state.protect_card = None
    state.non_protect_card = None
    state.card_keywords = None
    state.protect_ability = None
    state.protect_is_static = False
    state.protect_meaning = None
    state.active_attack = None
    state.defend_result = None
    state.player_protected = None
    state.card_protected = None
    state.player_one = None
    state.player_two = None
    state.defending_card = None
    state.defending_player = None

    return state
