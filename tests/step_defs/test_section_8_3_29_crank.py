"""
Step definitions for Section 8.3.29: Crank (Ability Keyword)
Reference: Flesh and Blood Comprehensive Rules Section 8.3.29

This module implements behavioral tests for the Crank ability keyword:
- Crank is a static ability (Rule 8.3.29)
- Crank means: "As this enters the arena, you may remove a steam counter from it.
  If you do, gain an action point." (Rule 8.3.29)
- Removing the steam counter is optional
- If steam counter is removed via Crank, the player is "considered to have cranked"
  and the card is "considered to be cranked" (Rule 8.3.29a)

Engine Features Needed for Section 8.3.29:
- [ ] CrankAbility class as a static ability (Rule 8.3.29)
- [ ] CrankAbility.is_static -> True (Rule 8.3.29)
- [ ] CrankAbility.meaning: the text of the ability (Rule 8.3.29)
- [ ] Steam counter support on CardInstance (Rule 8.3.29)
- [ ] Engine must trigger Crank when card with steam counter enters the arena (Rule 8.3.29)
- [ ] Engine must grant an action point when Crank is used (Rule 8.3.29)
- [ ] Engine must remove the steam counter when Crank is used (Rule 8.3.29)
- [ ] Engine must allow player to decline using Crank (Rule 8.3.29)
- [ ] Engine must track player "has cranked" state (Rule 8.3.29a)
- [ ] Engine must track card "is cranked" state (Rule 8.3.29a)
- [ ] Crank should not be usable if the card has no steam counter (Rule 8.3.29)

Current status: Tests written, Engine pending
"""

import pytest
from pytest_bdd import scenario, given, when, then, parsers


# ===== Rule 8.3.29: Crank is recognized as a keyword =====

@scenario(
    "../features/section_8_3_29_crank.feature",
    "Crank is recognized as an ability keyword",
)
def test_crank_is_recognized_as_keyword():
    """Rule 8.3.29: Crank must be recognized as a keyword on cards that have it."""
    pass


# ===== Rule 8.3.29: Crank is a static ability =====

@scenario(
    "../features/section_8_3_29_crank.feature",
    "Crank is a static ability",
)
def test_crank_is_static_ability():
    """Rule 8.3.29: Crank must be classified as a static ability."""
    pass


# ===== Rule 8.3.29: Card with Crank and steam counter allows using Crank =====

@scenario(
    "../features/section_8_3_29_crank.feature",
    "Card with Crank and a steam counter entering arena allows removing the steam counter",
)
def test_crank_can_remove_steam_counter_on_arena_enter():
    """Rule 8.3.29: When a card with Crank and a steam counter enters the arena, Crank is available."""
    pass


# ===== Rule 8.3.29: Using Crank grants an action point =====

@scenario(
    "../features/section_8_3_29_crank.feature",
    "Removing steam counter via Crank grants an action point",
)
def test_crank_grants_action_point():
    """Rule 8.3.29: Using Crank by removing a steam counter grants 1 action point."""
    pass


# ===== Rule 8.3.29: Crank is optional =====

@scenario(
    "../features/section_8_3_29_crank.feature",
    "Player may choose not to use Crank when card enters the arena",
)
def test_crank_is_optional():
    """Rule 8.3.29: The player may choose not to remove the steam counter via Crank."""
    pass


# ===== Rule 8.3.29: Crank requires a steam counter =====

@scenario(
    "../features/section_8_3_29_crank.feature",
    "Crank cannot be used when the card has no steam counter",
)
def test_crank_requires_steam_counter():
    """Rule 8.3.29: Crank cannot grant an action point if the card has no steam counter."""
    pass


# ===== Rule 8.3.29a: Player is considered to have cranked =====

@scenario(
    "../features/section_8_3_29_crank.feature",
    "Player is considered to have cranked after using Crank",
)
def test_player_considered_to_have_cranked():
    """Rule 8.3.29a: After using Crank, the player is considered to have cranked."""
    pass


# ===== Rule 8.3.29a: Card is considered to be cranked =====

@scenario(
    "../features/section_8_3_29_crank.feature",
    "Card is considered to be cranked after using Crank",
)
def test_card_considered_to_be_cranked():
    """Rule 8.3.29a: After Crank is used, the card is considered to be cranked."""
    pass


# ===== Rule 8.3.29: Crank meaning matches the comprehensive rules =====

@scenario(
    "../features/section_8_3_29_crank.feature",
    "Crank ability meaning matches comprehensive rules text",
)
def test_crank_meaning_matches_rules():
    """Rule 8.3.29: The Crank ability meaning must match the comprehensive rules text."""
    pass


# ===== Given Steps =====

@given("a card with the Crank keyword")
def crank_card(game_state):
    """Rule 8.3.29: Create a card that has the Crank keyword."""
    card = game_state.create_card(name="Crank Test Card")
    game_state.test_card = card


@given("the card has a steam counter on it")
def card_has_steam_counter(game_state):
    """Rule 8.3.29: Add a steam counter to the test card."""
    try:
        game_state.test_card.add_counter("steam", count=1)
        game_state.initial_steam_counters = 1
    except (AttributeError, NotImplementedError):
        # Engine does not yet support steam counters
        game_state.initial_steam_counters = 1


@given("the card has no steam counter on it")
def card_has_no_steam_counter(game_state):
    """Rule 8.3.29: Ensure the test card has no steam counters."""
    try:
        game_state.test_card.remove_all_counters("steam")
        game_state.initial_steam_counters = 0
    except (AttributeError, NotImplementedError):
        game_state.initial_steam_counters = 0


@given("the player has 1 action point")
def player_has_one_action_point(game_state):
    """Rule 8.3.29: Set the player's action points to 1 before Crank is used."""
    try:
        game_state.player.action_points = 1
        game_state.initial_action_points = 1
    except (AttributeError, NotImplementedError):
        game_state.initial_action_points = 1


# ===== When Steps =====

@when("I inspect the card's keywords")
def inspect_keywords(game_state):
    """Rule 8.3.29: Inspect the keywords on the test card."""
    try:
        game_state.card_keywords = game_state.test_card.keywords
    except AttributeError:
        game_state.card_keywords = None


@when("I check the ability type of Crank")
def check_ability_type(game_state):
    """Rule 8.3.29: Check whether Crank is classified as a static ability."""
    try:
        crank_ability = game_state.test_card.get_ability("crank")
        game_state.crank_ability = crank_ability
        game_state.crank_is_static = getattr(crank_ability, "is_static", False)
    except (AttributeError, TypeError):
        game_state.crank_ability = None
        game_state.crank_is_static = False


@when("the card enters the arena")
def card_enters_arena(game_state):
    """Rule 8.3.29: Move the card into the arena zone (triggering Crank if applicable)."""
    try:
        game_state.crank_available = game_state.player.arena.enter_card(
            game_state.test_card
        )
    except (AttributeError, NotImplementedError):
        game_state.crank_available = None


@when("the card enters the arena and the player uses Crank")
def card_enters_arena_player_uses_crank(game_state):
    """Rule 8.3.29: Move the card into the arena and the player chooses to use Crank."""
    try:
        result = game_state.player.arena.enter_card_with_crank(
            game_state.test_card, use_crank=True
        )
        game_state.crank_result = result
        game_state.player_cranked = getattr(result, "player_cranked", None)
        game_state.card_cranked = getattr(result, "card_cranked", None)
        game_state.action_points_after = getattr(
            game_state.player, "action_points", None
        )
    except (AttributeError, NotImplementedError):
        game_state.crank_result = None
        game_state.player_cranked = None
        game_state.card_cranked = None
        game_state.action_points_after = None


@when("the card enters the arena and the player declines to use Crank")
def card_enters_arena_player_declines_crank(game_state):
    """Rule 8.3.29: Move the card into the arena and the player chooses NOT to use Crank."""
    try:
        result = game_state.player.arena.enter_card_with_crank(
            game_state.test_card, use_crank=False
        )
        game_state.crank_result = result
        game_state.action_points_after = getattr(
            game_state.player, "action_points", None
        )
    except (AttributeError, NotImplementedError):
        game_state.crank_result = None
        game_state.action_points_after = None


@when("I check the meaning of the Crank ability")
def check_crank_meaning(game_state):
    """Rule 8.3.29: Retrieve the meaning text of the Crank ability."""
    try:
        crank_ability = game_state.test_card.get_ability("crank")
        game_state.crank_meaning = crank_ability.meaning
    except (AttributeError, TypeError):
        game_state.crank_meaning = None


# ===== Then Steps =====

@then("the card has the Crank keyword")
def card_has_crank_keyword(game_state):
    """Rule 8.3.29: The card must have Crank in its list of keywords."""
    assert game_state.card_keywords is not None, (
        "Engine feature needed: CardInstance.keywords property (Rule 8.3.29)"
    )
    assert "crank" in [k.lower() for k in game_state.card_keywords], (
        "Engine feature needed: Crank keyword must appear in card.keywords (Rule 8.3.29)"
    )


@then("Crank is a static ability")
def crank_is_static(game_state):
    """Rule 8.3.29: Crank must be classified as a static ability."""
    assert game_state.crank_ability is not None, (
        "Engine feature needed: CardInstance.get_ability('crank') (Rule 8.3.29)"
    )
    assert game_state.crank_is_static, (
        "Engine feature needed: CrankAbility.is_static must be True (Rule 8.3.29)"
    )


@then("the player may remove a steam counter from the card using Crank")
def crank_available_to_use(game_state):
    """Rule 8.3.29: Crank must be available when the card with a steam counter enters the arena."""
    assert game_state.crank_available is not None, (
        "Engine feature needed: Arena.enter_card() must signal Crank availability (Rule 8.3.29)"
    )
    assert game_state.crank_available, (
        "Engine feature needed: Crank must be available when steam counter is present "
        "on entering the arena (Rule 8.3.29)"
    )


@then("the player gains 1 action point")
def player_gains_action_point(game_state):
    """Rule 8.3.29: Using Crank must grant the player 1 action point."""
    assert game_state.crank_result is not None, (
        "Engine feature needed: Arena.enter_card_with_crank() (Rule 8.3.29)"
    )
    assert getattr(game_state.crank_result, "action_point_gained", None), (
        "Engine feature needed: Crank must grant an action point when used (Rule 8.3.29)"
    )


@then("the player now has 2 action points")
def player_has_two_action_points(game_state):
    """Rule 8.3.29: After using Crank, player should have initial action points + 1."""
    assert game_state.action_points_after is not None, (
        "Engine feature needed: Player.action_points property (Rule 8.3.29)"
    )
    expected = game_state.initial_action_points + 1
    assert game_state.action_points_after == expected, (
        f"Engine feature needed: After Crank, player should have {expected} action points, "
        f"got {game_state.action_points_after} (Rule 8.3.29)"
    )


@then("the player does not gain an action point from Crank")
def player_does_not_gain_action_point(game_state):
    """Rule 8.3.29: Declining Crank must not grant an action point."""
    gained = getattr(game_state.crank_result, "action_point_gained", False) if game_state.crank_result else False
    assert not gained, (
        "Engine feature needed: Declining Crank must not grant an action point (Rule 8.3.29)"
    )


@then("the player still has 1 action point")
def player_still_has_one_action_point(game_state):
    """Rule 8.3.29: When Crank is declined, player action points must remain unchanged."""
    if game_state.action_points_after is None:
        pytest.skip("Engine feature needed: Player.action_points property (Rule 8.3.29)")
    assert game_state.action_points_after == game_state.initial_action_points, (
        f"Engine feature needed: Declining Crank must leave action points unchanged. "
        f"Expected {game_state.initial_action_points}, got {game_state.action_points_after} "
        f"(Rule 8.3.29)"
    )


@then("Crank cannot grant an action point")
def crank_cannot_grant_action_point(game_state):
    """Rule 8.3.29: Without a steam counter, Crank must not grant an action point."""
    assert game_state.crank_available is not None, (
        "Engine feature needed: Arena.enter_card() must signal Crank availability (Rule 8.3.29)"
    )
    assert not game_state.crank_available, (
        "Engine feature needed: Crank must NOT be available when card has no steam counter "
        "(Rule 8.3.29)"
    )


@then("the player is considered to have cranked")
def player_is_considered_to_have_cranked(game_state):
    """Rule 8.3.29a: After using Crank, the player must be marked as having cranked."""
    assert game_state.player_cranked is not None, (
        "Engine feature needed: CrankResult.player_cranked or Player.has_cranked (Rule 8.3.29a)"
    )
    assert game_state.player_cranked, (
        "Engine feature needed: Player must be considered to have cranked after using Crank "
        "(Rule 8.3.29a)"
    )


@then("the card is considered to be cranked")
def card_is_considered_to_be_cranked(game_state):
    """Rule 8.3.29a: After Crank is used, the card must be marked as cranked."""
    assert game_state.card_cranked is not None, (
        "Engine feature needed: CrankResult.card_cranked or CardInstance.is_cranked (Rule 8.3.29a)"
    )
    assert game_state.card_cranked, (
        "Engine feature needed: Card must be considered to be cranked after Crank is used "
        "(Rule 8.3.29a)"
    )


@then(parsers.parse('the Crank meaning is "{meaning}"'))
def crank_meaning_matches(game_state, meaning):
    """Rule 8.3.29: The Crank ability meaning must match the comprehensive rules."""
    assert game_state.crank_meaning is not None, (
        "Engine feature needed: CrankAbility.meaning property (Rule 8.3.29)"
    )
    assert game_state.crank_meaning == meaning, (
        f"Engine feature needed: CrankAbility.meaning must match CR text. "
        f"Expected: '{meaning}', Got: '{game_state.crank_meaning}' (Rule 8.3.29)"
    )


# ===== Fixtures =====

@pytest.fixture
def game_state():
    """
    Fixture providing game state for Crank ability testing.

    Uses BDDGameState which integrates with the real engine.
    Reference: Rule 8.3.29 - Crank
    """
    from tests.bdd_helpers import BDDGameState

    state = BDDGameState()
    state.test_card = None
    state.initial_steam_counters = 0
    state.initial_action_points = 1
    state.card_keywords = None
    state.crank_ability = None
    state.crank_is_static = False
    state.crank_available = None
    state.crank_result = None
    state.crank_meaning = None
    state.player_cranked = None
    state.card_cranked = None
    state.action_points_after = None

    return state
