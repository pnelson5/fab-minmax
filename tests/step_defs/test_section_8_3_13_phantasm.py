"""
Step definitions for Section 8.3.13: Phantasm (Ability Keyword)
Reference: Flesh and Blood Comprehensive Rules Section 8.3.13

This module implements behavioral tests for the Phantasm ability keyword:
- Phantasm is a triggered-static ability (Rule 8.3.13)
- Meaning: "Whenever this is defended by a non-Illusionist attack action card
  with 6 or more {p}, destroy this." (Rule 8.3.13)
- Rule 8.3.13a: State-condition is met when a non-Illusionist attack action card
  with power >= 6 defends; a triggered-layer is put on the stack; when the
  triggered-layer resolves, if the event-condition is still met, the attack is destroyed.
- Rule 8.3.13b: If the Phantasm attack is destroyed before damage is calculated,
  the combat chain closes. If destroyed after damage is calculated, it does NOT close.

Engine Features Needed for Section 8.3.13:
- [ ] AbilityKeyword.PHANTASM on cards (Rule 8.3.13)
- [ ] PhantasmAbility.is_triggered_static -> True (Rule 8.3.13)
- [ ] PhantasmAbility.check_state_condition(defender) -> bool (Rule 8.3.13a)
    Condition: defender is non-Illusionist AND is an attack action card AND has power >= 6
- [ ] PhantasmAbility.create_triggered_layer() -> TriggeredLayer (Rule 8.3.13a)
- [ ] CombatChain.close() triggered when Phantasm attack destroyed before damage (Rule 8.3.13b)
- [ ] CombatChain.is_damage_calculated property (Rule 8.3.13b)
- [ ] Supertype.ILLUSIONIST check on defending cards (Rule 8.3.13a)

Current status: Tests written, Engine pending
"""

import pytest
from pytest_bdd import scenario, given, when, then, parsers


# ===== Rule 8.3.13: Phantasm is classified as an ability keyword =====

@scenario(
    "../features/section_8_3_13_phantasm.feature",
    "Phantasm is classified as an ability keyword",
)
def test_phantasm_is_ability_keyword():
    """Rule 8.3.13: Phantasm is listed as an ability keyword in Section 8.3."""
    pass


# ===== Rule 8.3.13a: Phantasm triggers for non-Illusionist attack action card with 6+ power =====

@scenario(
    "../features/section_8_3_13_phantasm.feature",
    "Phantasm attack is destroyed when defended by non-Illusionist attack action card with 6 or more power",
)
def test_phantasm_triggers_for_non_illusionist_high_power_defender():
    """Rule 8.3.13a: Phantasm state-condition met when defended by non-Illusionist attack action card with 6+ power."""
    pass


# ===== Rule 8.3.13a: Phantasm does NOT trigger for Illusionist attack action cards =====

@scenario(
    "../features/section_8_3_13_phantasm.feature",
    "Phantasm attack is not destroyed when defended by an Illusionist attack action card",
)
def test_phantasm_does_not_trigger_for_illusionist_defender():
    """Rule 8.3.13a: Phantasm state-condition not met when defender is an Illusionist attack action card."""
    pass


# ===== Rule 8.3.13a: Phantasm does NOT trigger for defenders with less than 6 power =====

@scenario(
    "../features/section_8_3_13_phantasm.feature",
    "Phantasm attack is not destroyed when defended by a non-Illusionist card with less than 6 power",
)
def test_phantasm_does_not_trigger_for_low_power_defender():
    """Rule 8.3.13a: Phantasm state-condition not met when defending card has power less than 6."""
    pass


# ===== Rule 8.3.13b: Combat chain closes if Phantasm attack destroyed before damage =====

@scenario(
    "../features/section_8_3_13_phantasm.feature",
    "Combat chain closes when Phantasm attack is destroyed before damage is calculated",
)
def test_combat_chain_closes_when_phantasm_destroys_before_damage():
    """Rule 8.3.13b: Combat chain closes if Phantasm attack destroyed before damage is calculated."""
    pass


# ===== Rule 8.3.13b: Combat chain does NOT close if Phantasm attack destroyed after damage =====

@scenario(
    "../features/section_8_3_13_phantasm.feature",
    "Combat chain does not close when Phantasm attack is destroyed after damage is calculated",
)
def test_combat_chain_does_not_close_when_phantasm_destroys_after_damage():
    """Rule 8.3.13b: Combat chain does not close if Phantasm attack destroyed after damage is calculated."""
    pass


# ===== Step Definitions =====

@given("the engine's list of ability keywords")
def engine_ability_keywords_list(game_state):
    """Retrieve the engine's list of ability keywords."""
    game_state.ability_keywords = game_state.get_ability_keywords_list()


@when(parsers.parse('I check if "{keyword}" is in the list of ability keywords'))
def check_keyword_in_ability_keywords(game_state, keyword):
    """Check if the given keyword is in the ability keywords list."""
    game_state.keyword_check_name = keyword
    game_state.keyword_found = game_state.is_ability_keyword(keyword)


@then(parsers.parse('"{keyword}" is recognized as an ability keyword'))
def keyword_is_recognized_as_ability_keyword(game_state, keyword):
    """Rule 8.3.13: Phantasm must appear in the engine's ability keyword list."""
    assert game_state.keyword_found, (
        f'"{keyword}" must be recognized as an ability keyword (Rule 8.3.13)'
    )


@given("a Phantasm attack is on the combat chain")
def phantasm_attack_on_combat_chain(game_state):
    """Set up a Phantasm attack on the combat chain."""
    game_state.phantasm_attack = game_state.create_card(
        name="Phantasm Attack",
        card_type="Action",
    )
    game_state.phantasm_attack_keyword = "Phantasm"
    game_state.attack.add_keyword("Phantasm")
    game_state.attack_on_chain = game_state.phantasm_attack


@given("a defending card is a non-Illusionist attack action card with 6 power")
def non_illusionist_attack_action_with_6_power(game_state):
    """Set up a non-Illusionist attack action card with 6 power as defender."""
    game_state.defending_card = game_state.create_phantasm_defending_card(
        is_illusionist=False,
        power=6,
        is_attack_action=True,
    )


@given("a defending card is an Illusionist attack action card with 6 power")
def illusionist_attack_action_with_6_power(game_state):
    """Set up an Illusionist attack action card with 6 power as defender."""
    game_state.defending_card = game_state.create_phantasm_defending_card(
        is_illusionist=True,
        power=6,
        is_attack_action=True,
    )


@given("a defending card is a non-Illusionist attack action card with 5 power")
def non_illusionist_attack_action_with_5_power(game_state):
    """Set up a non-Illusionist attack action card with 5 power as defender."""
    game_state.defending_card = game_state.create_phantasm_defending_card(
        is_illusionist=False,
        power=5,
        is_attack_action=True,
    )


@when("the defending card defends the Phantasm attack")
def defending_card_defends_phantasm_attack(game_state):
    """Simulate the defending card defending the Phantasm attack."""
    game_state.phantasm_check_result = game_state.check_phantasm_state_condition(
        attack=game_state.attack,
        defender=game_state.defending_card,
    )


@then("the Phantasm state-condition is met")
def phantasm_state_condition_is_met(game_state):
    """Rule 8.3.13a: Phantasm state-condition must be met."""
    assert game_state.phantasm_check_result.state_condition_met, (
        "Phantasm state-condition must be met when defended by non-Illusionist "
        "attack action card with 6 or more power (Rule 8.3.13a)"
    )


@then("a triggered-layer is placed on the stack to destroy the attack")
def triggered_layer_placed_on_stack(game_state):
    """Rule 8.3.13a: A triggered-layer must be created to destroy the attack."""
    assert game_state.phantasm_check_result.triggered_layer_created, (
        "A triggered-layer must be placed on the stack to destroy the Phantasm attack (Rule 8.3.13a)"
    )


@then("the Phantasm state-condition is not met")
def phantasm_state_condition_is_not_met(game_state):
    """Rule 8.3.13a: Phantasm state-condition must NOT be met."""
    assert not game_state.phantasm_check_result.state_condition_met, (
        "Phantasm state-condition must not be met when defender is Illusionist "
        "or has less than 6 power (Rule 8.3.13a)"
    )


@then("no triggered-layer is placed on the stack for Phantasm")
def no_triggered_layer_placed_on_stack(game_state):
    """Rule 8.3.13a: No triggered-layer must be created for Phantasm."""
    assert not game_state.phantasm_check_result.triggered_layer_created, (
        "No triggered-layer must be placed on the stack for Phantasm when "
        "state-condition is not met (Rule 8.3.13a)"
    )


@given("damage for the Phantasm attack's chain link has not been calculated yet")
def damage_not_yet_calculated(game_state):
    """Rule 8.3.13b: Set up state where damage has not been calculated."""
    game_state.damage_calculated = False


@given("damage for the Phantasm attack's chain link has already been calculated")
def damage_already_calculated(game_state):
    """Rule 8.3.13b: Set up state where damage has already been calculated."""
    game_state.damage_calculated = True


@when("the Phantasm attack is destroyed by Phantasm")
def phantasm_attack_is_destroyed(game_state):
    """Simulate the Phantasm attack being destroyed."""
    game_state.combat_chain_close_result = game_state.apply_phantasm_destruction(
        attack=game_state.attack,
        damage_already_calculated=game_state.damage_calculated,
    )


@then("the combat chain closes")
def combat_chain_closes(game_state):
    """Rule 8.3.13b: Combat chain must close when Phantasm destroys attack before damage."""
    assert game_state.combat_chain_close_result.combat_chain_closed, (
        "Combat chain must close when Phantasm attack is destroyed before damage "
        "has been calculated (Rule 8.3.13b)"
    )


@then("the combat chain does not close")
def combat_chain_does_not_close(game_state):
    """Rule 8.3.13b: Combat chain must NOT close when Phantasm destroys attack after damage."""
    assert not game_state.combat_chain_close_result.combat_chain_closed, (
        "Combat chain must not close when Phantasm attack is destroyed after damage "
        "has been calculated (Rule 8.3.13b)"
    )


# ===== Fixtures =====

@pytest.fixture
def game_state():
    """
    Fixture providing game state for testing Phantasm ability keyword.

    Uses BDDGameState which integrates with the real engine.
    Reference: Rule 8.3.13
    """
    from tests.bdd_helpers import BDDGameState

    state = BDDGameState()
    return state
