"""
Step definitions for Section 8.3.2: Battleworn (Ability Keyword)
Reference: Flesh and Blood Comprehensive Rules Section 8.3.2

This module implements behavioral tests for the Battleworn ability keyword:
- Battleworn is a triggered-static ability (Rule 8.3.2)
- Trigger fires when combat chain closes, if this defended (Rule 8.3.2)
- Effect: put a -1{d} counter on the card (Rule 8.3.2)
- Counters reduce defense value (Rule 8.3.2)
- Counters accumulate across multiple combat chains (Rule 8.3.2)

Engine Features Needed for Section 8.3.2:
- [ ] AbilityKeyword.BATTLEWORN triggered-static ability on cards/equipment (Rule 8.3.2)
- [ ] BattlewornAbility.is_triggered_static -> True (Rule 8.3.2)
- [ ] BattlewornAbility.trigger_condition — "combat chain closes AND this defended" (Rule 8.3.2)
- [ ] BattlewornAbility.effect — "put a -1{d} counter on this" (Rule 8.3.2)
- [ ] CardInstance.counters — list/count of counters on the card (Rule 8.3.2)
- [ ] CounterType.MINUS_ONE_DEFENSE (-1{d}) counter type (Rule 8.3.2)
- [ ] CardInstance.defense_value — base defense stat (Rule 8.3.2)
- [ ] CardInstance.effective_defense_value — base minus -1{d} counters (Rule 8.3.2)
- [ ] CombatChain.close() — fires Battleworn triggers for all cards that defended (Rule 8.3.2)
- [ ] CombatChain.track_defender(card) — record which cards defended in the chain (Rule 8.3.2)
- [ ] CombatChain.did_defend(card) -> bool — query if card defended in chain (Rule 8.3.2)

Current status: Tests written, Engine pending
"""

import pytest
from pytest_bdd import scenario, given, when, then, parsers
from typing import Optional, Any


# ===== Rule 8.3.2: Battleworn is a triggered-static ability =====

@scenario(
    "../features/section_8_3_2_battleworn.feature",
    "Battleworn is a triggered-static ability",
)
def test_battleworn_is_triggered_static_ability():
    """Rule 8.3.2: The Battleworn ability is a triggered-static ability."""
    pass


@scenario(
    "../features/section_8_3_2_battleworn.feature",
    "Battleworn ability has the correct triggered-static meaning",
)
def test_battleworn_ability_meaning():
    """Rule 8.3.2: Battleworn means 'When combat chain closes, if this defended, put -1{d} counter on it'."""
    pass


# ===== Rule 8.3.2: Trigger fires when combat chain closes after defending =====

@scenario(
    "../features/section_8_3_2_battleworn.feature",
    "Battleworn triggers when card defended and combat chain closes",
)
def test_battleworn_triggers_when_defended_and_chain_closes():
    """Rule 8.3.2: Battleworn trigger fires when card defended and combat chain closes."""
    pass


@scenario(
    "../features/section_8_3_2_battleworn.feature",
    "Battleworn does not trigger when card did not defend",
)
def test_battleworn_does_not_trigger_when_not_defending():
    """Rule 8.3.2: Battleworn trigger condition 'if this defended' prevents counter when not defending."""
    pass


# ===== Rule 8.3.2: -1{d} counter reduces defense value =====

@scenario(
    "../features/section_8_3_2_battleworn.feature",
    "A -1{d} counter reduces the defense value of the card",
)
def test_battleworn_counter_reduces_defense():
    """Rule 8.3.2: -1{d} counters placed by Battleworn reduce the card's defense value."""
    pass


# ===== Rule 8.3.2: Multiple chains accumulate counters =====

@scenario(
    "../features/section_8_3_2_battleworn.feature",
    "Battleworn card accumulates counters across multiple chains",
)
def test_battleworn_accumulates_counters_across_chains():
    """Rule 8.3.2: Battleworn places a counter each chain the card defends, accumulating over time."""
    pass


# ===== Rule 8.3.2: Only one counter per chain close =====

@scenario(
    "../features/section_8_3_2_battleworn.feature",
    "Battleworn places exactly one counter when triggered",
)
def test_battleworn_places_exactly_one_counter_per_chain():
    """Rule 8.3.2: Even if a card defends multiple attacks in a chain, only one trigger fires at close."""
    pass


# ===== Step Definitions =====

@given('a card with the "Battleworn" keyword ability')
def battleworn_card(game_state):
    """Set up a card with the Battleworn keyword ability."""
    card = game_state.create_card(
        name="Battleworn Test Equipment",
        card_type="Equipment",
    )
    game_state.battleworn_card = card
    game_state.battleworn_card_initial_counters = 0


@given('a card with the "Battleworn" keyword ability in a defend zone')
def battleworn_card_in_defend_zone(game_state):
    """Set up a Battleworn card that is in a defend zone (able to defend)."""
    card = game_state.create_card(
        name="Battleworn Test Equipment",
        card_type="Equipment",
    )
    game_state.battleworn_card = card
    game_state.battleworn_card_initial_counters = 0


@given('an equipment card with defense value 3 and the "Battleworn" keyword ability')
def battleworn_equipment_with_defense(game_state):
    """Set up an equipment card with a base defense of 3 and Battleworn."""
    card = game_state.create_card(
        name="Battleworn Test Equipment",
        card_type="Equipment",
        defense=3,
    )
    game_state.battleworn_card = card
    game_state.battleworn_card_initial_counters = 0


@given('the card defended an attack during the current combat chain')
def card_defended_in_chain(game_state):
    """Record that the Battleworn card defended in the current combat chain."""
    game_state.battleworn_card_defended = True


@given('the card did not defend during the current combat chain')
def card_did_not_defend(game_state):
    """Record that the Battleworn card did not defend in the current combat chain."""
    game_state.battleworn_card_defended = False


@given('the card has 1 counter from a previous chain')
def card_has_one_prior_counter(game_state):
    """Simulate a card that already has 1 -1{d} counter from a previous chain."""
    game_state.battleworn_card_initial_counters = 1


@given('the card defended multiple attacks in the current combat chain')
def card_defended_multiple_attacks(game_state):
    """Record that the Battleworn card defended multiple attacks in the chain."""
    game_state.battleworn_card_defended = True
    game_state.battleworn_defended_count = 2


@when('I inspect the Battleworn ability on the card')
def inspect_battleworn_ability(game_state):
    """Attempt to retrieve the Battleworn ability from the card."""
    card = game_state.battleworn_card
    try:
        ability = card.get_keyword_ability("Battleworn")
        game_state.battleworn_ability = ability
    except (AttributeError, NotImplementedError):
        game_state.battleworn_ability = None
        game_state.missing_engine_feature = "CardInstance.get_keyword_ability('Battleworn') not implemented"


@when('the combat chain closes')
def combat_chain_closes(game_state):
    """Simulate the combat chain closing and evaluate Battleworn triggers."""
    card = game_state.battleworn_card
    defended = getattr(game_state, 'battleworn_card_defended', False)
    initial_counters = getattr(game_state, 'battleworn_card_initial_counters', 0)

    try:
        # Simulate: close the combat chain with tracking of whether card defended
        combat_chain = game_state.engine.combat_chain
        combat_chain.set_defended(card, defended)
        combat_chain.close()
        game_state.chain_closed = True
    except (AttributeError, NotImplementedError):
        game_state.chain_closed = False
        game_state.missing_engine_feature = (
            "CombatChain.set_defended() / CombatChain.close() not implemented"
        )


@then('the Battleworn ability is a triggered-static ability')
def battleworn_ability_is_triggered_static(game_state):
    """Rule 8.3.2: Battleworn is a triggered-static ability."""
    if game_state.battleworn_ability is None:
        pytest.fail(
            "Engine Feature Needed: CardInstance.get_keyword_ability('Battleworn') / "
            "AbilityKeyword.BATTLEWORN not implemented (Rule 8.3.2)"
        )
    ability = game_state.battleworn_ability
    try:
        assert ability.is_triggered_static, (
            "Battleworn should be a triggered-static ability"
        )
    except (AttributeError, NotImplementedError):
        pytest.fail(
            "Engine Feature Needed: Ability.is_triggered_static not implemented (Rule 8.3.2)"
        )


@then('the Battleworn ability means "When the combat chain closes, if this defended, put a -1{d} counter on it"')
def battleworn_ability_meaning(game_state):
    """Rule 8.3.2: Battleworn's meaning is the triggered-static text."""
    if game_state.battleworn_ability is None:
        pytest.fail(
            "Engine Feature Needed: CardInstance.get_keyword_ability('Battleworn') / "
            "AbilityKeyword.BATTLEWORN not implemented (Rule 8.3.2)"
        )
    ability = game_state.battleworn_ability
    try:
        meaning = ability.meaning
        assert "combat chain closes" in meaning.lower(), (
            f"Battleworn meaning should reference 'combat chain closes', got: {meaning}"
        )
        assert "defended" in meaning.lower(), (
            f"Battleworn meaning should reference 'defended', got: {meaning}"
        )
        assert "-1" in meaning, (
            f"Battleworn meaning should reference '-1{{d}} counter', got: {meaning}"
        )
    except (AttributeError, NotImplementedError):
        pytest.fail(
            "Engine Feature Needed: BattlewornAbility.meaning not implemented (Rule 8.3.2)"
        )


@then('a -1{d} counter is placed on the Battleworn card')
def battleworn_counter_placed(game_state):
    """Rule 8.3.2: A -1{d} counter is placed on the card after defending and chain close."""
    card = game_state.battleworn_card
    initial = getattr(game_state, 'battleworn_card_initial_counters', 0)
    try:
        current_counters = card.count_counters(counter_type="minus_defense")
        assert current_counters > initial, (
            f"Expected counter count to increase from {initial}, got {current_counters}"
        )
    except (AttributeError, NotImplementedError):
        pytest.fail(
            "Engine Feature Needed: CardInstance.count_counters() / CounterType.MINUS_ONE_DEFENSE "
            "not implemented (Rule 8.3.2)"
        )


@then('no -1{d} counter is placed on the Battleworn card')
def battleworn_no_counter_placed(game_state):
    """Rule 8.3.2: No -1{d} counter is placed when the card did not defend."""
    card = game_state.battleworn_card
    initial = getattr(game_state, 'battleworn_card_initial_counters', 0)
    try:
        current_counters = card.count_counters(counter_type="minus_defense")
        assert current_counters == initial, (
            f"Expected counter count to remain {initial}, got {current_counters}"
        )
    except (AttributeError, NotImplementedError):
        pytest.fail(
            "Engine Feature Needed: CardInstance.count_counters() / CounterType.MINUS_ONE_DEFENSE "
            "not implemented (Rule 8.3.2)"
        )


@then(parsers.parse('the Battleworn card has {count:d} counter on it'))
@then(parsers.parse('the Battleworn card has {count:d} counters on it'))
def battleworn_card_has_n_counters(game_state, count):
    """Rule 8.3.2: The Battleworn card has the expected number of -1{d} counters."""
    card = game_state.battleworn_card
    try:
        current_counters = card.count_counters(counter_type="minus_defense")
        assert current_counters == count, (
            f"Expected {count} -1{{d}} counter(s) on card, got {current_counters}"
        )
    except (AttributeError, NotImplementedError):
        pytest.fail(
            "Engine Feature Needed: CardInstance.count_counters() not implemented (Rule 8.3.2)"
        )


@then(parsers.parse('the effective defense value of the Battleworn card is {value:d}'))
def battleworn_card_effective_defense(game_state, value):
    """Rule 8.3.2: -1{d} counters reduce the effective defense value."""
    card = game_state.battleworn_card
    try:
        effective_defense = card.effective_defense_value
        assert effective_defense == value, (
            f"Expected effective defense {value}, got {effective_defense}"
        )
    except (AttributeError, NotImplementedError):
        pytest.fail(
            "Engine Feature Needed: CardInstance.effective_defense_value not implemented (Rule 8.3.2)"
        )


@then('exactly 1 new -1{d} counter is placed on the Battleworn card')
def battleworn_exactly_one_counter(game_state):
    """Rule 8.3.2: Only one trigger fires when the combat chain closes, even with multiple defenses."""
    card = game_state.battleworn_card
    initial = getattr(game_state, 'battleworn_card_initial_counters', 0)
    try:
        current_counters = card.count_counters(counter_type="minus_defense")
        new_counters = current_counters - initial
        assert new_counters == 1, (
            f"Expected exactly 1 new counter, got {new_counters} new counters "
            f"(total: {current_counters}, initial: {initial})"
        )
    except (AttributeError, NotImplementedError):
        pytest.fail(
            "Engine Feature Needed: CardInstance.count_counters() not implemented (Rule 8.3.2)"
        )


# ===== Fixtures =====

@pytest.fixture
def game_state():
    """
    Fixture providing game state for testing Battleworn.

    Uses BDDGameState which integrates with the real engine.
    Reference: Rule 8.3.2 - Battleworn keyword ability.
    """
    from tests.bdd_helpers import BDDGameState

    state = BDDGameState()
    state.battleworn_card = None
    state.battleworn_ability = None
    state.battleworn_card_defended = False
    state.battleworn_card_initial_counters = 0
    state.battleworn_defended_count = 1
    state.chain_closed = False
    state.missing_engine_feature = None

    return state
