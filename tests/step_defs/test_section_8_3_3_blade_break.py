"""
Step definitions for Section 8.3.3: Blade Break (Ability Keyword)
Reference: Flesh and Blood Comprehensive Rules Section 8.3.3

This module implements behavioral tests for the Blade Break ability keyword:
- Blade Break is a triggered-static ability (Rule 8.3.3)
- Trigger fires when combat chain closes, if this defended (Rule 8.3.3)
- Effect: destroy the card with Blade Break (Rule 8.3.3)
- Typically found on equipment; equipment is removed from game after defending

Engine Features Needed for Section 8.3.3:
- [ ] AbilityKeyword.BLADE_BREAK triggered-static ability on cards/equipment (Rule 8.3.3)
- [ ] BladeBreakAbility.is_triggered_static -> True (Rule 8.3.3)
- [ ] BladeBreakAbility.trigger_condition — "combat chain closes AND this defended" (Rule 8.3.3)
- [ ] BladeBreakAbility.effect — "destroy this" (Rule 8.3.3)
- [ ] CardInstance.is_destroyed — whether the card has been destroyed (Rule 8.3.3)
- [ ] CombatChain.close() — fires Blade Break triggers for all cards that defended (Rule 8.3.3)
- [ ] CombatChain.set_defended(card, bool) — record which cards defended in the chain (Rule 8.3.3)
- [ ] Zone.contains(card) — check if a card is still in a zone (Rule 8.3.3)

Current status: Tests written, Engine pending
"""

import pytest
from pytest_bdd import scenario, given, when, then, parsers
from typing import Optional, Any


# ===== Rule 8.3.3: Blade Break is a triggered-static ability =====

@scenario(
    "../features/section_8_3_3_blade_break.feature",
    "Blade Break is a triggered-static ability",
)
def test_blade_break_is_triggered_static_ability():
    """Rule 8.3.3: The Blade Break ability is a triggered-static ability."""
    pass


@scenario(
    "../features/section_8_3_3_blade_break.feature",
    "Blade Break ability has the correct triggered-static meaning",
)
def test_blade_break_ability_meaning():
    """Rule 8.3.3: Blade Break means 'When combat chain closes, if this defended, destroy it'."""
    pass


# ===== Rule 8.3.3: Trigger fires and destroys the card =====

@scenario(
    "../features/section_8_3_3_blade_break.feature",
    "Blade Break destroys the card when it defended and combat chain closes",
)
def test_blade_break_destroys_when_defended_and_chain_closes():
    """Rule 8.3.3: Blade Break trigger fires and destroys the card when it defended."""
    pass


@scenario(
    "../features/section_8_3_3_blade_break.feature",
    "Blade Break does not trigger when card did not defend",
)
def test_blade_break_does_not_trigger_when_not_defending():
    """Rule 8.3.3: Blade Break condition 'if this defended' prevents destruction when not defending."""
    pass


# ===== Rule 8.3.3: Destroyed card is removed from zone =====

@scenario(
    "../features/section_8_3_3_blade_break.feature",
    "A destroyed Blade Break card is removed from the defend zone",
)
def test_blade_break_card_removed_from_zone():
    """Rule 8.3.3: The destroyed Blade Break card leaves its current zone."""
    pass


# ===== Rule 8.3.3: Triggers regardless of combat outcome =====

@scenario(
    "../features/section_8_3_3_blade_break.feature",
    "Blade Break triggers even when the attack is fully blocked",
)
def test_blade_break_triggers_when_attack_fully_blocked():
    """Rule 8.3.3: Blade Break fires regardless of whether the attack was fully blocked."""
    pass


@scenario(
    "../features/section_8_3_3_blade_break.feature",
    "Blade Break triggers when the attack deals damage",
)
def test_blade_break_triggers_when_attack_deals_damage():
    """Rule 8.3.3: Blade Break fires regardless of whether the attack dealt damage."""
    pass


# ===== Step Definitions =====

@given('a card with the "Blade Break" keyword ability')
def blade_break_card(game_state):
    """Set up a card with the Blade Break keyword ability."""
    card = game_state.create_card(
        name="Blade Break Test Equipment",
        card_type="Equipment",
    )
    game_state.blade_break_card = card


@given('a card with the "Blade Break" keyword ability in a defend zone')
def blade_break_card_in_defend_zone(game_state):
    """Set up a Blade Break card positioned in a defend zone (able to defend)."""
    card = game_state.create_card(
        name="Blade Break Test Equipment",
        card_type="Equipment",
    )
    game_state.blade_break_card = card
    game_state.blade_break_card_in_zone = True


@given('the Blade Break card defended an attack during the current combat chain')
def blade_break_card_defended(game_state):
    """Record that the Blade Break card defended in the current combat chain."""
    game_state.blade_break_card_defended = True


@given('the Blade Break card did not defend during the current combat chain')
def blade_break_card_did_not_defend(game_state):
    """Record that the Blade Break card did not defend in the current combat chain."""
    game_state.blade_break_card_defended = False


@given('the attack was fully blocked by the defending card')
def attack_fully_blocked(game_state):
    """Record that the attack was fully blocked (no damage to hero)."""
    game_state.attack_fully_blocked = True


@given('the attack dealt damage despite the defense')
def attack_dealt_damage(game_state):
    """Record that the attack dealt damage even though the card defended."""
    game_state.attack_dealt_damage = True


@when('I inspect the Blade Break ability on the card')
def inspect_blade_break_ability(game_state):
    """Attempt to retrieve the Blade Break ability from the card."""
    card = game_state.blade_break_card
    try:
        ability = card.get_keyword_ability("Blade Break")
        game_state.blade_break_ability = ability
    except (AttributeError, NotImplementedError):
        game_state.blade_break_ability = None
        game_state.missing_engine_feature = (
            "CardInstance.get_keyword_ability('Blade Break') not implemented"
        )


@when('the combat chain closes')
def combat_chain_closes(game_state):
    """Simulate the combat chain closing and evaluate Blade Break triggers."""
    card = game_state.blade_break_card
    defended = getattr(game_state, 'blade_break_card_defended', False)

    try:
        combat_chain = game_state.engine.combat_chain
        combat_chain.set_defended(card, defended)
        combat_chain.close()
        game_state.chain_closed = True
    except (AttributeError, NotImplementedError):
        game_state.chain_closed = False
        game_state.missing_engine_feature = (
            "CombatChain.set_defended() / CombatChain.close() not implemented"
        )


@then('the Blade Break ability is a triggered-static ability')
def blade_break_ability_is_triggered_static(game_state):
    """Rule 8.3.3: Blade Break is a triggered-static ability."""
    if game_state.blade_break_ability is None:
        pytest.fail(
            "Engine Feature Needed: CardInstance.get_keyword_ability('Blade Break') / "
            "AbilityKeyword.BLADE_BREAK not implemented (Rule 8.3.3)"
        )
    ability = game_state.blade_break_ability
    try:
        assert ability.is_triggered_static, (
            "Blade Break should be a triggered-static ability"
        )
    except (AttributeError, NotImplementedError):
        pytest.fail(
            "Engine Feature Needed: Ability.is_triggered_static not implemented (Rule 8.3.3)"
        )


@then('the Blade Break ability means "When the combat chain closes, if this defended, destroy it"')
def blade_break_ability_meaning(game_state):
    """Rule 8.3.3: Blade Break's meaning is the triggered-static text."""
    if game_state.blade_break_ability is None:
        pytest.fail(
            "Engine Feature Needed: CardInstance.get_keyword_ability('Blade Break') / "
            "AbilityKeyword.BLADE_BREAK not implemented (Rule 8.3.3)"
        )
    ability = game_state.blade_break_ability
    try:
        meaning = ability.meaning
        assert "combat chain closes" in meaning.lower(), (
            f"Blade Break meaning should reference 'combat chain closes', got: {meaning}"
        )
        assert "defended" in meaning.lower(), (
            f"Blade Break meaning should reference 'defended', got: {meaning}"
        )
        assert "destroy" in meaning.lower(), (
            f"Blade Break meaning should reference 'destroy', got: {meaning}"
        )
    except (AttributeError, NotImplementedError):
        pytest.fail(
            "Engine Feature Needed: BladeBreakAbility.meaning not implemented (Rule 8.3.3)"
        )


@then('the Blade Break card is destroyed')
def blade_break_card_is_destroyed(game_state):
    """Rule 8.3.3: The card with Blade Break is destroyed after defending and chain close."""
    card = game_state.blade_break_card
    try:
        assert card.is_destroyed, (
            "Blade Break card should be destroyed after defending and combat chain closing"
        )
    except (AttributeError, NotImplementedError):
        pytest.fail(
            "Engine Feature Needed: CardInstance.is_destroyed / "
            "CombatChain.close() Blade Break trigger not implemented (Rule 8.3.3)"
        )


@then('the Blade Break card is not destroyed')
def blade_break_card_is_not_destroyed(game_state):
    """Rule 8.3.3: The card with Blade Break is NOT destroyed when it did not defend."""
    card = game_state.blade_break_card
    try:
        assert not card.is_destroyed, (
            "Blade Break card should NOT be destroyed when it did not defend"
        )
    except (AttributeError, NotImplementedError):
        pytest.fail(
            "Engine Feature Needed: CardInstance.is_destroyed not implemented (Rule 8.3.3)"
        )


@then('the Blade Break card is no longer in the defend zone')
def blade_break_card_not_in_defend_zone(game_state):
    """Rule 8.3.3: A destroyed Blade Break card is removed from its zone."""
    card = game_state.blade_break_card
    try:
        # Card should have been removed from its zone when destroyed
        zone = card.current_zone
        if zone is not None:
            assert not zone.contains(card), (
                "Destroyed Blade Break card should no longer be in its zone"
            )
        # If zone is None, card is no longer in any zone — that's also acceptable
    except (AttributeError, NotImplementedError):
        pytest.fail(
            "Engine Feature Needed: CardInstance.current_zone / Zone.contains() / "
            "destruction removes card from zone — not implemented (Rule 8.3.3)"
        )


# ===== Fixtures =====

@pytest.fixture
def game_state():
    """
    Fixture providing game state for testing Blade Break.

    Uses BDDGameState which integrates with the real engine.
    Reference: Rule 8.3.3 - Blade Break keyword ability.
    """
    from tests.bdd_helpers import BDDGameState

    state = BDDGameState()
    state.blade_break_card = None
    state.blade_break_ability = None
    state.blade_break_card_defended = False
    state.blade_break_card_in_zone = False
    state.attack_fully_blocked = False
    state.attack_dealt_damage = False
    state.chain_closed = False
    state.missing_engine_feature = None

    return state
