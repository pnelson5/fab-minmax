"""
Step definitions for Section 8.3.11: Blood Debt (Ability Keyword)
Reference: Flesh and Blood Comprehensive Rules Section 8.3.11

This module implements behavioral tests for the Blood Debt ability keyword:
- Blood Debt is a triggered-static ability (Rule 8.3.11)
- Meaning: "While this is in your banished zone, at the beginning of your end phase,
  lose 1{h}." (Rule 8.3.11)
- Blood Debt triggers at the beginning of the owner's end phase (Rule 8.3.11)
- The card must be in the owner's banished zone for the trigger to fire (Rule 8.3.11)
- Rule 8.3.11a: only triggers if the source is PUBLIC (face-up) in the banished zone
- Multiple Blood Debt cards each trigger independently, causing multiple life losses
- Blood Debt triggers on the OWNER's end phase, not the opponent's (Rule 8.3.11)

Engine Features Needed for Section 8.3.11:
- [ ] AbilityKeyword.BLOOD_DEBT on cards (Rule 8.3.11)
- [ ] BloodDebtAbility.is_triggered_static -> True (Rule 8.3.11)
- [ ] BloodDebtAbility.is_play_static -> False (Rule 8.3.11)
- [ ] BloodDebtAbility.is_meta_static -> False (Rule 8.3.11)
- [ ] BloodDebtAbility.meaning property returning the canonical blood debt text (Rule 8.3.11)
- [ ] EndPhase.begin() triggers Blood Debt ability for all public Blood Debt cards in banished zone (Rule 8.3.11)
- [ ] Zone.is_public property for banished zone cards (Rule 8.3.11a)
- [ ] Player.lose_life(amount) method to apply Blood Debt life loss (Rule 8.3.11)
- [ ] GameState.current_end_phase_player property to track whose end phase it is (Rule 8.3.11)
- [ ] Blood Debt only fires on owner's end phase, not opponent's (Rule 8.3.11)

Current status: Tests written, Engine pending
"""

import pytest
from pytest_bdd import scenario, given, when, then, parsers


# ===== Rule 8.3.11: Blood Debt is a triggered-static ability =====

@scenario(
    "../features/section_8_3_11_blood_debt.feature",
    "Blood Debt is a triggered-static ability",
)
def test_blood_debt_is_triggered_static():
    """Rule 8.3.11: Blood Debt is a triggered-static ability."""
    pass


# ===== Rule 8.3.11: Blood Debt meaning is correct =====

@scenario(
    "../features/section_8_3_11_blood_debt.feature",
    "Blood Debt meaning is as specified in the rules",
)
def test_blood_debt_meaning_is_correct():
    """Rule 8.3.11: Blood Debt has the canonical meaning from the comprehensive rules."""
    pass


# ===== Rule 8.3.11: Card with Blood Debt in banished zone causes life loss =====

@scenario(
    "../features/section_8_3_11_blood_debt.feature",
    "Card with Blood Debt in banished zone causes owner to lose 1 life at end phase",
)
def test_blood_debt_causes_life_loss():
    """Rule 8.3.11: A card with Blood Debt in banished zone causes the owner to lose 1 life."""
    pass


# ===== Rule 8.3.11: Blood Debt triggers at beginning of end phase =====

@scenario(
    "../features/section_8_3_11_blood_debt.feature",
    "Blood Debt triggers at the beginning of the end phase",
)
def test_blood_debt_triggers_at_beginning_of_end_phase():
    """Rule 8.3.11: Blood Debt trigger fires at the beginning of the end phase."""
    pass


# ===== Rule 8.3.11: Multiple Blood Debt cards each drain 1 life =====

@scenario(
    "../features/section_8_3_11_blood_debt.feature",
    "Multiple Blood Debt cards in banished zone each drain 1 life",
)
def test_multiple_blood_debt_cards_drain_multiple_life():
    """Rule 8.3.11: Each Blood Debt card in banished zone drains 1 life separately."""
    pass


# ===== Rule 8.3.11a: Blood Debt does not trigger when face-down =====

@scenario(
    "../features/section_8_3_11_blood_debt.feature",
    "Blood Debt does not trigger when card is face-down in banished zone",
)
def test_blood_debt_no_trigger_when_face_down():
    """Rule 8.3.11a: Blood Debt only triggers if the source is public in the banished zone."""
    pass


# ===== Rule 8.3.11: Blood Debt does not trigger on opponent's end phase =====

@scenario(
    "../features/section_8_3_11_blood_debt.feature",
    "Blood Debt does not trigger on the opponent's end phase",
)
def test_blood_debt_no_trigger_on_opponent_end_phase():
    """Rule 8.3.11: Blood Debt triggers at the beginning of the OWNER's end phase."""
    pass


# ===== Step Definitions =====

@given('a card has the "Blood Debt" keyword')
def card_with_blood_debt_keyword(game_state):
    """Create a card with the Blood Debt keyword."""
    game_state.blood_debt_card = game_state.create_card(
        name="Blood Debt Test Card",
        card_type="Action",
    )
    game_state.blood_debt_card_keyword = "Blood Debt"


@when("I inspect the Blood Debt ability on the card")
def inspect_blood_debt_ability(game_state):
    """Inspect the Blood Debt ability on the card."""
    game_state.blood_debt_ability = game_state.get_ability_by_keyword(
        game_state.blood_debt_card, "Blood Debt"
    )


@then("the Blood Debt ability is a triggered-static ability")
def blood_debt_is_triggered_static(game_state):
    """Rule 8.3.11: Blood Debt must be a triggered-static ability."""
    assert game_state.blood_debt_ability.is_triggered_static, (
        "Blood Debt must be a triggered-static ability (Rule 8.3.11)"
    )


@then("the Blood Debt ability is not a play-static ability")
def blood_debt_is_not_play_static(game_state):
    """Rule 8.3.11: Blood Debt is not a play-static ability."""
    assert not game_state.blood_debt_ability.is_play_static, (
        "Blood Debt must not be a play-static ability (Rule 8.3.11)"
    )


@then("the Blood Debt ability is not a meta-static ability")
def blood_debt_is_not_meta_static(game_state):
    """Rule 8.3.11: Blood Debt is not a meta-static ability."""
    assert not game_state.blood_debt_ability.is_meta_static, (
        "Blood Debt must not be a meta-static ability (Rule 8.3.11)"
    )


@then(parsers.parse('the Blood Debt ability means "{meaning}"'))
def blood_debt_meaning_is_correct(game_state, meaning):
    """Rule 8.3.11: Blood Debt has the canonical meaning text."""
    assert game_state.blood_debt_ability.meaning == meaning, (
        f"Blood Debt meaning should be '{meaning}' (Rule 8.3.11), "
        f"got '{game_state.blood_debt_ability.meaning}'"
    )


@given(parsers.parse("a player has {life:d} life"))
def player_has_life(game_state, life):
    """Set the player's life total."""
    game_state.set_player_life(game_state.player, life)
    game_state.initial_life = life


@given('a card with "Blood Debt" is in the player\'s banished zone face-up')
def blood_debt_card_in_banished_zone_face_up(game_state):
    """Place a Blood Debt card face-up in the player's banished zone."""
    game_state.blood_debt_card = game_state.create_card(
        name="Blood Debt Card",
        card_type="Action",
    )
    game_state.banish_card(game_state.blood_debt_card, face_up=True)
    game_state.blood_debt_trigger_fired = False


@given('a card with "Blood Debt" is in the player\'s banished zone face-down')
def blood_debt_card_in_banished_zone_face_down(game_state):
    """Place a Blood Debt card face-down in the player's banished zone."""
    game_state.blood_debt_card = game_state.create_card(
        name="Blood Debt Card",
        card_type="Action",
    )
    game_state.banish_card(game_state.blood_debt_card, face_up=False)
    game_state.blood_debt_trigger_fired = False


@given(parsers.parse('{count:d} cards with "Blood Debt" are in the player\'s banished zone face-up'))
def multiple_blood_debt_cards_in_banished_zone(game_state, count):
    """Place multiple Blood Debt cards face-up in the player's banished zone."""
    game_state.blood_debt_cards = []
    for i in range(count):
        card = game_state.create_card(
            name=f"Blood Debt Card {i + 1}",
            card_type="Action",
        )
        game_state.banish_card(card, face_up=True)
        game_state.blood_debt_cards.append(card)
    game_state.blood_debt_count = count


@when("the player's end phase begins")
def players_end_phase_begins(game_state):
    """Trigger the beginning of the player's end phase."""
    game_state.begin_end_phase(game_state.player)


@when("the opponent's end phase begins")
def opponents_end_phase_begins(game_state):
    """Trigger the beginning of the opponent's end phase."""
    game_state.begin_end_phase(game_state.opponent)


@then("the player loses 1 life")
def player_loses_1_life(game_state):
    """Rule 8.3.11: The player loses 1 life from Blood Debt."""
    current_life = game_state.get_player_life(game_state.player)
    assert current_life == game_state.initial_life - 1, (
        f"Blood Debt: player should lose 1 life (Rule 8.3.11), "
        f"expected {game_state.initial_life - 1}, got {current_life}"
    )


@then(parsers.parse("the player has {life:d} life"))
def player_has_expected_life(game_state, life):
    """Verify the player's life total."""
    current_life = game_state.get_player_life(game_state.player)
    assert current_life == life, (
        f"Blood Debt: player should have {life} life (Rule 8.3.11), "
        f"got {current_life}"
    )


@then("the player still has 20 life")
def player_still_has_20_life(game_state):
    """Rule 8.3.11/8.3.11a: The player's life is unchanged (no Blood Debt trigger)."""
    current_life = game_state.get_player_life(game_state.player)
    assert current_life == 20, (
        f"Blood Debt: player life should be unchanged at 20 (Rule 8.3.11/8.3.11a), "
        f"got {current_life}"
    )


@then(parsers.parse("the player loses {amount:d} life"))
def player_loses_n_life(game_state, amount):
    """Rule 8.3.11: The player loses the expected amount of life from multiple Blood Debts."""
    current_life = game_state.get_player_life(game_state.player)
    assert current_life == game_state.initial_life - amount, (
        f"Blood Debt: player should lose {amount} life (Rule 8.3.11), "
        f"expected {game_state.initial_life - amount}, got {current_life}"
    )


@then("the Blood Debt trigger fires")
def blood_debt_trigger_fires(game_state):
    """Rule 8.3.11: The Blood Debt trigger fired during the end phase."""
    assert game_state.blood_debt_trigger_fired, (
        "Blood Debt: trigger must fire at the beginning of the end phase (Rule 8.3.11)"
    )


@then("the trigger fires at the beginning of the end phase")
def trigger_fires_at_beginning_of_end_phase(game_state):
    """Rule 8.3.11: Blood Debt fires at the beginning (not end) of the end phase."""
    assert game_state.blood_debt_triggered_at_beginning_of_end_phase, (
        "Blood Debt: trigger must fire at the BEGINNING of the end phase (Rule 8.3.11)"
    )


@then("the Blood Debt trigger does not fire")
def blood_debt_trigger_does_not_fire(game_state):
    """Rule 8.3.11/8.3.11a: The Blood Debt trigger did not fire."""
    assert not game_state.blood_debt_trigger_fired, (
        "Blood Debt: trigger must not fire (Rule 8.3.11/8.3.11a)"
    )


# ===== Fixtures =====

@pytest.fixture
def game_state():
    """
    Fixture providing game state for testing Blood Debt ability.

    Uses BDDGameState which integrates with the real engine.
    Reference: Rule 8.3.11 - Blood Debt
    """
    from tests.bdd_helpers import BDDGameState

    state = BDDGameState()
    state.blood_debt_card = None
    state.blood_debt_cards = []
    state.blood_debt_card_keyword = None
    state.blood_debt_ability = None
    state.blood_debt_trigger_fired = False
    state.blood_debt_triggered_at_beginning_of_end_phase = False
    state.blood_debt_count = 0
    state.initial_life = 0

    return state
