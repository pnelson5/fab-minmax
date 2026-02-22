"""
Step definitions for Section 1.0.2: Restriction, Requirement, and Allowance Precedence
Reference: Flesh and Blood Comprehensive Rules Section 1.0.2

This module implements behavioral tests for the precedence rules between
restrictions, requirements, and allowances in the game engine.
"""

import pytest
from pytest_bdd import scenario, given, when, then, parsers


# Scenario: Restriction overrides allowance for playing cards from banished zone
# Tests Rule 1.0.2: Restriction takes precedence over Allowance


@scenario(
    "../features/section_1_0_2_precedence.feature",
    "Restriction overrides allowance for playing cards from banished zone",
)
def test_restriction_overrides_allowance_banished():
    """Rule 1.0.2: Restriction takes precedence over allowance."""
    pass


@given(
    'a player has a restriction effect "You can\'t play cards from your banished zone"'
)
def player_has_restriction_cant_play_banished(game_state):
    """Rule 1.0.2: Apply restriction effect to player."""
    game_state.player.add_restriction("cant_play_from_banished")


@given(
    'the player has an allowance effect "You may play cards from your banished zone"'
)
def player_has_allowance_play_banished(game_state):
    """Rule 1.0.2: Apply allowance effect to player."""
    game_state.player.add_allowance("may_play_from_banished")


@given("the player has a card in their banished zone")
def player_has_card_in_banished(game_state):
    """Rule 1.0.2: Setup test state with card in banished zone."""
    game_state.player.banished_zone.add_card(game_state.test_card)


@when("the player attempts to play a card from their banished zone")
def player_attempts_play_from_banished(game_state):
    """Rule 1.0.2: Attempt to play card from banished zone."""
    game_state.play_result = game_state.player.attempt_play_from_zone(
        game_state.test_card, "banished"
    )


@then("the play should be prevented")
def play_should_be_prevented(game_state):
    """Rule 1.0.2: Verify restriction prevented the play."""
    assert not game_state.play_result.success
    assert game_state.play_result.blocked_by == "restriction"


@then("the card should remain in the banished zone")
def card_remains_in_banished(game_state):
    """Rule 1.0.2: Verify card did not move zones."""
    assert game_state.test_card in game_state.player.banished_zone


# Scenario: Restriction overrides requirement for defending with equipment
# Tests Rule 1.0.2: Restriction takes precedence over Requirement


@scenario(
    "../features/section_1_0_2_precedence.feature",
    "Restriction overrides requirement for defending with equipment",
)
def test_restriction_overrides_requirement_equipment():
    """Rule 1.0.2: Restriction takes precedence over requirement."""
    pass


@given('an attack has the restriction "This can\'t be defended by equipment"')
def attack_has_restriction_no_equipment_defense(game_state):
    """Rule 1.0.2: Apply restriction to attack."""
    game_state.attack.add_restriction("cant_be_defended_by_equipment")


@given('a defender has a requirement "You must defend with equipment if able"')
def defender_has_requirement_must_use_equipment(game_state):
    """Rule 1.0.2: Apply requirement to defending player."""
    game_state.defender.add_requirement("must_defend_with_equipment")


@given("the defender controls equipment that could defend")
def defender_has_equipment(game_state):
    """Rule 1.0.2: Setup defender with equipment."""
    game_state.defender.arena.add_equipment(game_state.test_equipment)


@when("the defender attempts to defend with equipment")
def defender_attempts_defend_with_equipment(game_state):
    """Rule 1.0.2: Attempt to defend with equipment."""
    game_state.defend_result = game_state.defender.attempt_defend(
        game_state.attack, [game_state.test_equipment]
    )


@then("the defense should be prevented")
def defense_should_be_prevented(game_state):
    """Rule 1.0.2: Verify restriction prevented the defense."""
    assert not game_state.defend_result.success
    assert game_state.defend_result.blocked_by == "restriction"


@then("the equipment should not be used to defend")
def equipment_not_used_to_defend(game_state):
    """Rule 1.0.2: Verify equipment is not defending."""
    assert game_state.test_equipment not in game_state.attack.defenders


# Scenario: Requirement overrides allowance for card selection
# Tests Rule 1.0.2: Requirement takes precedence over Allowance


@scenario(
    "../features/section_1_0_2_precedence.feature",
    "Requirement overrides allowance for card selection",
)
def test_requirement_overrides_allowance_card_play():
    """Rule 1.0.2: Requirement takes precedence over allowance."""
    pass


@given('a player has a requirement "You must play your next card from hand if able"')
def player_has_requirement_play_from_hand(game_state):
    """Rule 1.0.2: Apply requirement to player."""
    game_state.player.add_requirement("must_play_next_from_hand")


@given('the player has an allowance "You may play your next card from arsenal"')
def player_has_allowance_play_from_arsenal(game_state):
    """Rule 1.0.2: Apply allowance to player."""
    game_state.player.add_allowance("may_play_from_arsenal")


@given("the player has playable cards in hand")
def player_has_playable_cards_in_hand(game_state):
    """Rule 1.0.2: Setup player hand with playable cards."""
    game_state.player.hand.add_card(game_state.test_card_hand)


@given("the player has a playable card in arsenal")
def player_has_playable_card_in_arsenal(game_state):
    """Rule 1.0.2: Setup player arsenal with playable card."""
    game_state.player.arsenal.add_card(game_state.test_card_arsenal)


@when("the player attempts to play a card")
def player_attempts_to_play_card(game_state):
    """Rule 1.0.2: Attempt to play a card."""
    game_state.legal_plays = game_state.player.get_legal_plays()


@then("the player must play from hand")
def player_must_play_from_hand(game_state):
    """Rule 1.0.2: Verify only hand cards are playable."""
    for play in game_state.legal_plays:
        assert play.source_zone == "hand"


@then("the player cannot choose to play from arsenal")
def player_cannot_play_from_arsenal(game_state):
    """Rule 1.0.2: Verify arsenal cards are not playable."""
    arsenal_plays = [p for p in game_state.legal_plays if p.source_zone == "arsenal"]
    assert len(arsenal_plays) == 0


# Scenario: "Only" restriction functions as restriction on all other options
# Tests Rule 1.0.2a: "Only" restrictions are equivalent to restricting everything else


@scenario(
    "../features/section_1_0_2_precedence.feature",
    '"Only" restriction functions as restriction on all other options',
)
def test_only_restriction_equivalent():
    """Rule 1.0.2a: 'Only' restriction restricts all other options."""
    pass


@given('a player has a restriction "You may only play cards from arsenal"')
def player_has_only_arsenal_restriction(game_state):
    """Rule 1.0.2a: Apply 'only' restriction."""
    game_state.player.add_restriction("only_play_from_arsenal")


@given("the player has a card in hand")
def player_has_card_in_hand(game_state):
    """Rule 1.0.2a: Setup player hand."""
    game_state.player.hand.add_card(game_state.test_card_hand)


@given("the player has a card in arsenal")
def player_has_card_in_arsenal(game_state):
    """Rule 1.0.2a: Setup player arsenal."""
    game_state.player.arsenal.add_card(game_state.test_card_arsenal)


@when("the player attempts to play the card from hand")
def player_attempts_play_from_hand(game_state):
    """Rule 1.0.2a: Attempt to play from hand."""
    game_state.play_result = game_state.player.attempt_play_from_zone(
        game_state.test_card_hand, "hand"
    )


@then("only arsenal cards should be playable")
def only_arsenal_playable(game_state):
    """Rule 1.0.2a: Verify only arsenal is playable."""
    legal_plays = game_state.player.get_legal_plays()
    for play in legal_plays:
        assert play.source_zone == "arsenal"


# Scenario: Overpower gained after defenders declared does not remove existing defenders
# Tests Rule 1.0.2b: Restrictions do not retroactively change game state


@scenario(
    "../features/section_1_0_2_precedence.feature",
    "Overpower gained after defenders declared does not remove existing defenders",
)
def test_restriction_not_retroactive():
    """Rule 1.0.2b: Restrictions do not retroactively change game state."""
    pass


@given("an attack is being defended by 2 action cards")
def attack_defended_by_two_cards(game_state):
    """Rule 1.0.2b: Setup attack with 2 defenders."""
    game_state.attack.add_defender(game_state.defender_card_1)
    game_state.attack.add_defender(game_state.defender_card_2)
    game_state.initial_defender_count = len(game_state.attack.defenders)


@given("the attack gains overpower (can't be defended by more than 1 action card)")
def attack_gains_overpower(game_state):
    """Rule 1.0.2b: Apply overpower restriction after defenders declared."""
    game_state.attack.add_keyword("overpower")


@when("the overpower effect is applied")
def overpower_effect_applied(game_state):
    """Rule 1.0.2b: Process the overpower effect."""
    game_state.attack.process_restrictions()


@then("both defending action cards remain defending")
def both_defenders_remain(game_state):
    """Rule 1.0.2b: Verify defenders were not removed retroactively."""
    assert len(game_state.attack.defenders) == game_state.initial_defender_count
    assert game_state.defender_card_1 in game_state.attack.defenders
    assert game_state.defender_card_2 in game_state.attack.defenders


@then("the game state is not retroactively changed")
def game_state_not_retroactively_changed(game_state):
    """Rule 1.0.2b: Verify game state integrity."""
    # The presence of overpower does not undo already-declared defenders
    assert game_state.attack.has_keyword("overpower")
    assert len(game_state.attack.defenders) == 2


# Scenario: Multiple restrictions all apply simultaneously
# Tests Rule 1.0.2: Multiple restrictions enforcement


@scenario(
    "../features/section_1_0_2_precedence.feature",
    "Multiple restrictions all apply simultaneously",
)
def test_multiple_restrictions():
    """Rule 1.0.2: Multiple restrictions all apply."""
    pass


@given('a player has a restriction "You can\'t play red cards"')
def player_has_restriction_no_red(game_state):
    """Rule 1.0.2: Apply red card restriction."""
    game_state.player.add_restriction("cant_play_red")


@given('the player has a restriction "You can\'t play cards with cost 3 or greater"')
def player_has_restriction_no_high_cost(game_state):
    """Rule 1.0.2: Apply high cost restriction."""
    game_state.player.add_restriction("cant_play_cost_3_or_greater")


@given("the player has a red card with cost 1 in hand")
def player_has_red_low_cost(game_state):
    """Rule 1.0.2: Setup red low cost card."""
    game_state.red_card = game_state.create_card(color="red", cost=1)
    game_state.player.hand.add_card(game_state.red_card)


@given("the player has a blue card with cost 3 in hand")
def player_has_blue_high_cost(game_state):
    """Rule 1.0.2: Setup blue high cost card."""
    game_state.blue_card = game_state.create_card(color="blue", cost=3)
    game_state.player.hand.add_card(game_state.blue_card)


@when("the player attempts to play either card")
def player_attempts_play_either(game_state):
    """Rule 1.0.2: Check playability of both cards."""
    game_state.red_playable = game_state.player.can_play(game_state.red_card)
    game_state.blue_playable = game_state.player.can_play(game_state.blue_card)


@then("both cards should be unplayable")
def both_cards_unplayable(game_state):
    """Rule 1.0.2: Verify both cards are restricted."""
    assert not game_state.red_playable
    assert not game_state.blue_playable


@then("all restrictions should be enforced")
def all_restrictions_enforced(game_state):
    """Rule 1.0.2: Verify each restriction blocks its respective card."""
    # Red card blocked by color restriction
    red_check = game_state.player.check_restrictions(game_state.red_card)
    assert "cant_play_red" in red_check.blocking_restrictions

    # Blue card blocked by cost restriction
    blue_check = game_state.player.check_restrictions(game_state.blue_card)
    assert "cant_play_cost_3_or_greater" in blue_check.blocking_restrictions


# Scenario: Allowance permits action when no restriction or requirement exists
# Tests Rule 1.0.2: Allowance alone permits action


@scenario(
    "../features/section_1_0_2_precedence.feature",
    "Allowance permits action when no restriction or requirement exists",
)
def test_allowance_permits_when_no_conflicts():
    """Rule 1.0.2: Allowance permits action when no higher precedence effects exist."""
    pass


@given('a player has an allowance "You may play this card from your banished zone"')
def player_has_allowance_banished(game_state):
    """Rule 1.0.2: Apply allowance to play from banished."""
    # The allowance applies to the player for this specific card
    game_state.player.add_allowance("may_play_from_banished")


@given("the player has no restriction effects active")
def player_no_restrictions(game_state):
    """Rule 1.0.2: Verify no restrictions are active."""
    game_state.player.clear_restrictions()


@given("the player has no requirement effects active")
def player_no_requirements(game_state):
    """Rule 1.0.2: Verify no requirements are active."""
    game_state.player.clear_requirements()


@given("the player has the card in their banished zone")
def player_has_allowance_card_banished(game_state):
    """Rule 1.0.2: Setup card in banished zone."""
    game_state.player.banished_zone.add_card(game_state.test_card)


@when("the player plays the card from their banished zone")
def player_plays_from_banished(game_state):
    """Rule 1.0.2: Play card from banished zone."""
    game_state.play_result = game_state.player.play_card(
        game_state.test_card, from_zone="banished", game_state=game_state
    )


@then("the play should succeed")
def play_should_succeed(game_state):
    """Rule 1.0.2: Verify allowance permitted the play."""
    assert game_state.play_result.success


@then("the card should move to the appropriate zone")
def card_moves_to_appropriate_zone(game_state):
    """Rule 1.0.2: Verify card moved correctly."""
    assert game_state.test_card not in game_state.player.banished_zone
    # Card should be on stack or in arena depending on card type
    assert (
        game_state.test_card in game_state.stack
        or game_state.test_card in game_state.player.arena
    )


# Fixtures


@pytest.fixture
def game_state():
    """
    Fixture providing game state for testing.

    Uses BDDGameState which integrates with the real precedence system.
    Reference: Rule 1.0.2
    """
    from tests.bdd_helpers import BDDGameState

    state = BDDGameState()

    # Initialize test cards
    from fab_engine.cards.model import CardType

    state.test_card = state.create_card("Test Card")
    state.test_card_hand = state.create_card("Hand Card")
    state.test_card_arsenal = state.create_card("Arsenal Card")
    state.test_equipment = state.create_card(
        "Test Equipment", card_type=CardType.EQUIPMENT
    )
    state.defender_card_1 = state.create_card("Defender 1")
    state.defender_card_2 = state.create_card("Defender 2")

    return state
