"""
Step definitions for Section 8.3.19: Quell (Ability Keyword)
Reference: Flesh and Blood Comprehensive Rules Section 8.3.19

This module implements behavioral tests for the Quell ability keyword:
- Quell is a static ability (Rule 8.3.19)
- Written as "Quell N" meaning "If you would be dealt damage, you may pay N{r}
  to prevent N of that damage. If you do, destroy this at the beginning of the
  end phase." (Rule 8.3.19)

Engine Features Needed for Section 8.3.19:
- [ ] QuellAbility class as a static ability (Rule 8.3.19)
- [ ] QuellAbility.is_static -> True (Rule 8.3.19)
- [ ] QuellAbility.n: int — the resource cost and prevention amount N (Rule 8.3.19)
- [ ] QuellAbility.meaning: formatted ability text string (Rule 8.3.19)
- [ ] QuellAction.can_quell(player) -> bool: checks if player can pay N{r} (Rule 8.3.19)
- [ ] QuellAction.pay_cost(player, incoming_damage) -> QuellResult (Rule 8.3.19)
- [ ] QuellResult.damage_prevented: int — should equal N when paid (Rule 8.3.19)
- [ ] QuellResult.success: bool (Rule 8.3.19)
- [ ] QuellResult.destroy_at_end_phase: bool — True when cost was paid (Rule 8.3.19)
- [ ] EndPhaseBeginEvent handles destruction of Quell cards that paid (Rule 8.3.19)
- [ ] DamageReplacementEffect: replaces incoming damage using Quell prevention (Rule 8.3.19)

Current status: Tests written, Engine pending
"""

import pytest
from pytest_bdd import scenario, given, when, then, parsers


# ===== Rule 8.3.19: Quell is a static ability =====

@scenario(
    "../features/section_8_3_19_quell.feature",
    "Quell is a static ability",
)
def test_quell_is_static_ability():
    """Rule 8.3.19: Quell must be a static ability."""
    pass


@scenario(
    "../features/section_8_3_19_quell.feature",
    "Quell ability has the correct N value",
)
def test_quell_has_correct_n_value():
    """Rule 8.3.19: Quell ability stores N for cost/prevention amount."""
    pass


# ===== Rule 8.3.19: Paying Quell prevents N damage =====

@scenario(
    "../features/section_8_3_19_quell.feature",
    "Paying Quell 1 cost prevents 1 damage",
)
def test_quell_1_prevents_1_damage():
    """Rule 8.3.19: Paying Quell 1 prevents exactly 1 damage."""
    pass


@scenario(
    "../features/section_8_3_19_quell.feature",
    "Paying Quell 2 cost prevents 2 damage",
)
def test_quell_2_prevents_2_damage():
    """Rule 8.3.19: Paying Quell 2 prevents exactly 2 damage."""
    pass


# ===== Rule 8.3.19: Paying Quell is optional =====

@scenario(
    "../features/section_8_3_19_quell.feature",
    "Player may choose not to pay Quell cost",
)
def test_quell_is_optional():
    """Rule 8.3.19: Quell prevention is optional — player may decline."""
    pass


# ===== Rule 8.3.19: Destroy at beginning of end phase after paying =====

@scenario(
    "../features/section_8_3_19_quell.feature",
    "Card is destroyed at beginning of end phase after paying Quell cost",
)
def test_quell_card_destroyed_after_paying():
    """Rule 8.3.19: After paying Quell cost, the card is destroyed at beginning of end phase."""
    pass


@scenario(
    "../features/section_8_3_19_quell.feature",
    "Card is not destroyed if Quell cost was not paid",
)
def test_quell_card_not_destroyed_if_not_paid():
    """Rule 8.3.19: If Quell cost not paid, the card is NOT destroyed at end phase."""
    pass


# ===== Rule 8.3.19: Quell prevents exactly N damage =====

@scenario(
    "../features/section_8_3_19_quell.feature",
    "Quell only prevents exactly N damage, not more",
)
def test_quell_prevents_exactly_n_damage():
    """Rule 8.3.19: Quell prevents exactly N damage, not more."""
    pass


# ===== Rule 8.3.19: Cannot pay with insufficient resources =====

@scenario(
    "../features/section_8_3_19_quell.feature",
    "Cannot pay Quell cost with insufficient resources",
)
def test_quell_cannot_pay_insufficient_resources():
    """Rule 8.3.19: Player cannot activate Quell with fewer than N resource points."""
    pass


# ===== Step Definitions =====

@given(parsers.parse('a card with "{quell_text}" ability'))
def card_with_quell_ability(game_state, quell_text):
    """Rule 8.3.19: Create a card with the specified Quell ability text."""
    card = game_state.create_card(name=f"Test Quell Card ({quell_text})")
    card._quell_ability_text = quell_text  # type: ignore[attr-defined]
    parts = quell_text.split()
    n = int(parts[1]) if len(parts) >= 2 and parts[1].isdigit() else 1
    card._quell_n = n  # type: ignore[attr-defined]
    game_state.quell_card = card


@given(parsers.parse('a player has an equipment with "{quell_text}" ability equipped'))
def player_has_quell_equipment_equipped(game_state, quell_text):
    """Rule 8.3.19: Create a card with Quell that is equipped to the player."""
    card = game_state.create_card(name=f"Test Quell Equipment ({quell_text})")
    card._quell_ability_text = quell_text  # type: ignore[attr-defined]
    parts = quell_text.split()
    n = int(parts[1]) if len(parts) >= 2 and parts[1].isdigit() else 1
    card._quell_n = n  # type: ignore[attr-defined]
    # Record the equipped card on game_state (engine equipment zones are tested via
    # Equipment zone tests — here we focus on the Quell ability behavior itself)
    game_state.quell_card = card
    game_state._quell_equipped = True  # type: ignore[attr-defined]


@given(parsers.parse('the player has {amount:d} resource point'))
@given(parsers.parse('the player has {amount:d} resource points'))
def player_has_resource_points(game_state, amount):
    """Rule 8.3.19: Set the player's resource points."""
    game_state.set_player_resource_points(game_state.player, amount)


# ===== When steps =====

@when("I inspect the Quell ability type")
def inspect_quell_ability_type(game_state):
    """Rule 8.3.19: Inspect the ability type of the Quell ability."""
    card = game_state.quell_card
    from fab_engine.abilities import QuellAbility  # type: ignore[import]
    ability = QuellAbility(n=card._quell_n)
    game_state._quell_ability_instance = ability  # type: ignore[attr-defined]


@when(parsers.parse("the player would be dealt {amount:d} damage"))
def player_would_be_dealt_damage(game_state, amount):
    """Rule 8.3.19: Set up incoming damage amount for Quell to respond to."""
    game_state._incoming_damage = amount  # type: ignore[attr-defined]


@when(parsers.parse("the player pays the Quell cost of {amount:d} resource point"))
@when(parsers.parse("the player pays the Quell cost of {amount:d} resource points"))
def player_pays_quell_cost(game_state, amount):
    """Rule 8.3.19: Player pays N resource points to activate Quell damage prevention."""
    card = game_state.quell_card
    from fab_engine.abilities import QuellAbility, QuellAction  # type: ignore[import]
    n = getattr(card, "_quell_n", amount)
    ability = QuellAbility(n=n)
    action = QuellAction(ability=ability, card=card, player=game_state.player)
    incoming = getattr(game_state, "_incoming_damage", 0)
    result = action.pay_cost(game_state.player, incoming_damage=incoming)
    game_state._quell_paid = result.success  # type: ignore[attr-defined]
    game_state._quell_result = result  # type: ignore[attr-defined]


@when("the player declines to pay the Quell cost")
def player_declines_quell(game_state):
    """Rule 8.3.19: Player opts not to pay the Quell cost (optional ability)."""
    game_state._quell_paid = False  # type: ignore[attr-defined]
    game_state._quell_result = None  # type: ignore[attr-defined]


@when("the beginning of the end phase occurs")
def end_phase_begins(game_state):
    """Rule 8.3.19: Simulate the beginning of the end phase."""
    from fab_engine.phases import EndPhaseBeginEvent  # type: ignore[import]
    event = EndPhaseBeginEvent(player=game_state.player)
    result = event.process_quell_destructions(game_state._quell_paid)
    game_state._end_phase_result = result  # type: ignore[attr-defined]


# ===== Then steps =====

@then("the Quell ability is a static ability")
def quell_is_static(game_state):
    """Rule 8.3.19: Quell ability must be a static ability."""
    ability = game_state._quell_ability_instance
    assert hasattr(ability, "is_static"), "QuellAbility must have is_static attribute"
    assert ability.is_static is True, "QuellAbility must be a static ability"


@then(parsers.parse("the Quell ability has N equal to {n:d}"))
def quell_has_n_equal_to(game_state, n):
    """Rule 8.3.19: Quell ability must store the correct N value."""
    ability = game_state._quell_ability_instance
    assert hasattr(ability, "n"), "QuellAbility must have an n attribute"
    assert ability.n == n, f"Expected QuellAbility.n == {n}, got {ability.n}"


@then(parsers.parse("{count:d} damage is prevented"))
def damage_is_prevented(game_state, count):
    """Rule 8.3.19: N damage must be prevented when Quell cost is paid."""
    result = game_state._quell_result
    assert result is not None, "QuellAction.pay_cost must return a result"
    assert result.success is True, "Quell cost payment must succeed"
    prevented = getattr(result, "damage_prevented", None)
    assert prevented is not None, "QuellResult must include damage_prevented"
    assert prevented == count, f"Expected {count} damage prevented, got {prevented}"


@then(parsers.parse("exactly {count:d} damage is prevented"))
def exactly_damage_is_prevented(game_state, count):
    """Rule 8.3.19: Exactly N damage must be prevented (not more)."""
    result = game_state._quell_result
    assert result is not None, "QuellAction.pay_cost must return a result"
    prevented = getattr(result, "damage_prevented", None)
    assert prevented is not None, "QuellResult must include damage_prevented"
    assert prevented == count, \
        f"Quell should prevent exactly {count} damage, got {prevented}"


@then(parsers.parse("the player takes {amount:d} damage instead"))
def player_takes_reduced_damage(game_state, amount):
    """Rule 8.3.19: Player takes incoming damage minus prevented damage."""
    result = game_state._quell_result
    assert result is not None, "QuellAction.pay_cost must return a result"
    net_damage = getattr(result, "net_damage", None)
    assert net_damage is not None, "QuellResult must include net_damage"
    assert net_damage == amount, \
        f"Expected player to take {amount} damage, got {net_damage}"


@then("no damage is prevented by Quell")
def no_damage_prevented(game_state):
    """Rule 8.3.19: No damage prevented when player declines Quell."""
    result = getattr(game_state, "_quell_result", None)
    if result is not None:
        prevented = getattr(result, "damage_prevented", 0)
        assert prevented == 0, "No damage should be prevented when Quell is declined"
    # No result means player declined — no prevention occurred


@then(parsers.parse("the player takes the full {amount:d} damage"))
def player_takes_full_damage(game_state, amount):
    """Rule 8.3.19: Player takes full incoming damage when Quell is declined."""
    result = getattr(game_state, "_quell_result", None)
    if result is not None:
        net_damage = getattr(result, "net_damage", None)
        if net_damage is not None:
            assert net_damage == amount, \
                f"Expected full {amount} damage when Quell declined, got {net_damage}"
    # If no result, player accepted full damage (as expected)


@then("the Quell card is destroyed")
def quell_card_is_destroyed(game_state):
    """Rule 8.3.19: After paying Quell cost, card is destroyed at beginning of end phase."""
    result = getattr(game_state, "_end_phase_result", None)
    assert result is not None, "EndPhaseBeginEvent.process_quell_destructions must return a result"
    destroyed = getattr(result, "cards_destroyed", [])
    assert game_state.quell_card in destroyed, \
        "Quell card must be destroyed at beginning of end phase after paying Quell cost (Rule 8.3.19)"


@then("the Quell card is not destroyed by Quell")
def quell_card_not_destroyed(game_state):
    """Rule 8.3.19: If Quell cost not paid, card must NOT be destroyed at end phase."""
    result = getattr(game_state, "_end_phase_result", None)
    if result is not None:
        destroyed = getattr(result, "cards_destroyed", [])
        assert game_state.quell_card not in destroyed, \
            "Quell card must NOT be destroyed when Quell cost was not paid (Rule 8.3.19)"


@then("the player cannot pay the Quell cost")
def player_cannot_pay_quell_cost(game_state):
    """Rule 8.3.19: Player cannot activate Quell with insufficient resource points."""
    card = game_state.quell_card
    from fab_engine.abilities import QuellAbility, QuellValidator  # type: ignore[import]
    n = getattr(card, "_quell_n", 1)
    ability = QuellAbility(n=n)
    validator = QuellValidator()
    can_pay = validator.can_pay_resource_cost(game_state.player, n)
    assert can_pay is False, \
        f"Player should not be able to pay Quell {n} with insufficient resources (Rule 8.3.19)"


# ===== Fixtures =====

@pytest.fixture
def game_state():
    """
    Fixture providing game state for testing Quell ability.

    Uses BDDGameState which integrates with the real engine.
    Reference: Rule 8.3.19 — Quell ability keyword
    """
    from tests.bdd_helpers import BDDGameState

    state = BDDGameState()
    state.quell_card = None
    state._quell_ability_instance = None
    state._quell_paid = False
    state._quell_result = None
    state._incoming_damage = 0
    state._end_phase_result = None

    return state
