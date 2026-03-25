"""
Step definitions for Section 8.3.10: Temper (Ability Keyword)
Reference: Flesh and Blood Comprehensive Rules Section 8.3.10

This module implements behavioral tests for the Temper ability keyword:
- Temper is a triggered-static ability (Rule 8.3.10)
- Meaning: "When the combat chain closes, if this defended, put a -1{d} counter
  on it, then destroy it if it has zero {d}." (Rule 8.3.10)
- Temper only triggers if the card actually defended that combat chain (Rule 8.3.10)
- When triggered: put a -1{d} counter on the card (Rule 8.3.10)
- After placing the counter: destroy the card if it has zero {d} (Rule 8.3.10)
- Typically found on equipment cards with defense values (Rule 8.3.10)

Engine Features Needed for Section 8.3.10:
- [ ] AbilityKeyword.TEMPER on cards (Rule 8.3.10)
- [ ] TemperAbility.is_triggered_static -> True (Rule 8.3.10)
- [ ] TemperAbility.is_play_static -> False (Rule 8.3.10)
- [ ] TemperAbility.is_meta_static -> False (Rule 8.3.10)
- [ ] TemperAbility.meaning property returning the canonical temper text (Rule 8.3.10)
- [ ] CombatChain.close() triggers Temper ability on defending cards (Rule 8.3.10)
- [ ] CardInstance.defended_this_chain property to track if card was used to defend (Rule 8.3.10)
- [ ] CardInstance.add_defense_counter(amount) method to place -1{d} counters (Rule 8.3.10)
- [ ] CardInstance.effective_defense property accounting for -1{d} counters (Rule 8.3.10)
- [ ] CardInstance.defense_counters property tracking -1{d} counters on the card (Rule 8.3.10)
- [ ] Engine destroys card when effective_defense reaches 0 after Temper trigger (Rule 8.3.10)

Current status: Tests written, Engine pending
"""

import pytest
from pytest_bdd import scenario, given, when, then, parsers


# ===== Rule 8.3.10: Temper is a triggered-static ability =====

@scenario(
    "../features/section_8_3_10_temper.feature",
    "Temper is a triggered-static ability",
)
def test_temper_is_triggered_static():
    """Rule 8.3.10: Temper is a triggered-static ability."""
    pass


# ===== Rule 8.3.10: Temper meaning is correct =====

@scenario(
    "../features/section_8_3_10_temper.feature",
    "Temper meaning is as specified in the rules",
)
def test_temper_meaning_is_correct():
    """Rule 8.3.10: Temper has the canonical meaning from the comprehensive rules."""
    pass


# ===== Rule 8.3.10: Defending places -1{d} counter on chain close =====

@scenario(
    "../features/section_8_3_10_temper.feature",
    "Temper card gains a defense counter when used to defend and the chain closes",
)
def test_temper_counter_placed_after_defending():
    """Rule 8.3.10: A -1{d} counter is placed when the Temper card defended and the chain closes."""
    pass


# ===== Rule 8.3.10: Temper card with 1 defense is destroyed =====

@scenario(
    "../features/section_8_3_10_temper.feature",
    "Temper card with 1 defense is destroyed when chain closes after defending",
)
def test_temper_card_destroyed_at_zero_defense():
    """Rule 8.3.10: A Temper card with 1 defense is destroyed when chain closes after defending."""
    pass


# ===== Rule 8.3.10: Temper does not trigger if card did not defend =====

@scenario(
    "../features/section_8_3_10_temper.feature",
    "Temper does not trigger when the card did not defend",
)
def test_temper_no_trigger_without_defending():
    """Rule 8.3.10: Temper only triggers if the card defended."""
    pass


# ===== Rule 8.3.10: Multiple defenses reduce defense each time =====

@scenario(
    "../features/section_8_3_10_temper.feature",
    "Temper card loses a defense counter each time it defends and the chain closes",
)
def test_temper_counter_per_chain_close():
    """Rule 8.3.10: Each chain close where the Temper card defended puts a -1{d} counter."""
    pass


# ===== Rule 8.3.10: Destroyed when counters reduce defense to zero =====

@scenario(
    "../features/section_8_3_10_temper.feature",
    "Temper card is destroyed when defense counters reduce it to zero",
)
def test_temper_destroyed_when_counters_reach_zero():
    """Rule 8.3.10: Temper card is destroyed when defense reaches zero from accumulated counters."""
    pass


# ===== Step Definitions =====

@given('a card has the "Temper" keyword')
def card_with_temper_keyword(game_state):
    """Create a card with the Temper keyword."""
    game_state.temper_card = game_state.create_card(
        name="Temper Test Equipment",
        card_type="Equipment",
        defense=3,
    )
    game_state.temper_card_keyword = "Temper"


@when("I inspect the Temper ability on the card")
def inspect_temper_ability(game_state):
    """Inspect the Temper ability on the card."""
    game_state.temper_ability = game_state.get_ability_by_keyword(
        game_state.temper_card, "Temper"
    )


@then("the Temper ability is a triggered-static ability")
def temper_is_triggered_static(game_state):
    """Rule 8.3.10: Temper must be a triggered-static ability."""
    assert game_state.temper_ability.is_triggered_static, (
        "Temper must be a triggered-static ability (Rule 8.3.10)"
    )


@then("the Temper ability is not a play-static ability")
def temper_is_not_play_static(game_state):
    """Rule 8.3.10: Temper is not a play-static ability."""
    assert not game_state.temper_ability.is_play_static, (
        "Temper must not be a play-static ability (Rule 8.3.10)"
    )


@then("the Temper ability is not a meta-static ability")
def temper_is_not_meta_static(game_state):
    """Rule 8.3.10: Temper is not a meta-static ability."""
    assert not game_state.temper_ability.is_meta_static, (
        "Temper must not be a meta-static ability (Rule 8.3.10)"
    )


@then(parsers.parse('the Temper ability means "{meaning}"'))
def temper_meaning_is_correct(game_state, meaning):
    """Rule 8.3.10: Temper has the canonical meaning text."""
    assert game_state.temper_ability.meaning == meaning, (
        f"Temper meaning should be '{meaning}' (Rule 8.3.10), "
        f"got '{game_state.temper_ability.meaning}'"
    )


@given(parsers.parse("an equipment card with \"Temper\" and {defense:d} defense is in play"))
def equipment_with_temper_in_play(game_state, defense):
    """Create and play an equipment card with Temper and specified defense."""
    game_state.temper_equipment = game_state.create_card(
        name="Temper Equipment",
        card_type="Equipment",
        defense=defense,
    )
    game_state.temper_equipment_initial_defense = defense
    game_state.play_card_to_arena(game_state.temper_equipment)


@given(parsers.parse("an equipment card with \"Temper\" and {defense:d} defense remaining is in play"))
def equipment_with_temper_remaining_defense_in_play(game_state, defense):
    """Create and play an equipment card with Temper that has given defense remaining."""
    game_state.temper_equipment = game_state.create_card(
        name="Temper Equipment",
        card_type="Equipment",
        defense=defense,
    )
    game_state.temper_equipment_initial_defense = defense
    game_state.play_card_to_arena(game_state.temper_equipment)


@given("the equipment card was used to defend during the combat chain")
def equipment_used_to_defend(game_state):
    """Record that the Temper equipment defended during the combat chain."""
    game_state.temper_equipment_defended = True
    game_state.mark_card_as_defended(game_state.temper_equipment)


@given("the equipment card was NOT used to defend during the combat chain")
def equipment_not_used_to_defend(game_state):
    """Record that the Temper equipment did NOT defend during the combat chain."""
    game_state.temper_equipment_defended = False


@given("the equipment card was used to defend during the first combat chain")
def equipment_used_to_defend_first_chain(game_state):
    """Record that the Temper equipment defended during the first combat chain."""
    game_state.temper_equipment_defended = True
    game_state.mark_card_as_defended(game_state.temper_equipment)


@when("the combat chain closes")
def combat_chain_closes(game_state):
    """Close the combat chain, triggering Temper if applicable."""
    game_state.close_combat_chain()


@when("the first combat chain closes")
def first_combat_chain_closes(game_state):
    """Close the first combat chain, triggering Temper if the card defended."""
    game_state.close_combat_chain()


@then("a -1{d} counter is placed on the equipment card")
def defense_counter_placed(game_state):
    """Rule 8.3.10: A -1{d} counter is placed on the Temper card after defending."""
    assert game_state.get_defense_counters(game_state.temper_equipment) >= 1, (
        "Temper: a -1{d} counter must be placed when the card defended and chain closed (Rule 8.3.10)"
    )


@then("a -1{d} counter is placed on the equipment card after the first chain")
def defense_counter_placed_after_first_chain(game_state):
    """Rule 8.3.10: A -1{d} counter is placed after the first chain close."""
    assert game_state.get_defense_counters(game_state.temper_equipment) >= 1, (
        "Temper: a -1{d} counter must be placed after the first chain close (Rule 8.3.10)"
    )


@then(parsers.parse("the equipment card has {remaining:d} effective defense remaining"))
def equipment_has_remaining_defense(game_state, remaining):
    """Rule 8.3.10: The effective defense of the Temper card is reduced by counters."""
    effective_defense = game_state.get_effective_defense(game_state.temper_equipment)
    assert effective_defense == remaining, (
        f"Temper: effective defense should be {remaining} after counters (Rule 8.3.10), "
        f"got {effective_defense}"
    )


@then("the equipment card has 1 effective defense remaining")
def equipment_has_1_defense(game_state):
    """Rule 8.3.10: The Temper card has 1 effective defense after first counter."""
    effective_defense = game_state.get_effective_defense(game_state.temper_equipment)
    assert effective_defense == 1, (
        f"Temper: effective defense should be 1 after one counter (Rule 8.3.10), "
        f"got {effective_defense}"
    )


@then("the equipment card has zero defense remaining")
def equipment_has_zero_defense(game_state):
    """Rule 8.3.10: The Temper card has zero effective defense."""
    effective_defense = game_state.get_effective_defense(game_state.temper_equipment)
    assert effective_defense == 0, (
        f"Temper: effective defense should be 0 (Rule 8.3.10), got {effective_defense}"
    )


@then("the equipment card is destroyed")
def equipment_is_destroyed(game_state):
    """Rule 8.3.10: The Temper card is destroyed when defense reaches zero."""
    assert game_state.is_destroyed(game_state.temper_equipment), (
        "Temper: card with zero {d} must be destroyed (Rule 8.3.10)"
    )


@then("the equipment card is not destroyed")
def equipment_is_not_destroyed(game_state):
    """Rule 8.3.10: The Temper card is not destroyed when defense > 0."""
    assert not game_state.is_destroyed(game_state.temper_equipment), (
        "Temper: card with remaining {d} must not be destroyed (Rule 8.3.10)"
    )


@then("no -1{d} counter is placed on the equipment card")
def no_defense_counter_placed(game_state):
    """Rule 8.3.10: No counter is placed if the Temper card did not defend."""
    counters = game_state.get_defense_counters(game_state.temper_equipment)
    assert counters == 0, (
        f"Temper: no counter should be placed if card did not defend (Rule 8.3.10), "
        f"got {counters} counters"
    )


@then("the equipment card is not destroyed after the first chain")
def equipment_not_destroyed_after_first_chain(game_state):
    """Rule 8.3.10: The Temper card is not destroyed after first chain if defense > 0."""
    assert not game_state.is_destroyed(game_state.temper_equipment), (
        "Temper: card with remaining {d} must not be destroyed after first chain (Rule 8.3.10)"
    )


# ===== Fixtures =====

@pytest.fixture
def game_state():
    """
    Fixture providing game state for testing Temper ability.

    Uses BDDGameState which integrates with the real engine.
    Reference: Rule 8.3.10 - Temper
    """
    from tests.bdd_helpers import BDDGameState

    state = BDDGameState()
    state.temper_card = None
    state.temper_equipment = None
    state.temper_equipment_initial_defense = 0
    state.temper_equipment_defended = False
    state.temper_ability = None
    state.temper_card_keyword = None

    return state
