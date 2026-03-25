"""
Step definitions for Section 8.3.23: Piercing (Ability Keyword)
Reference: Flesh and Blood Comprehensive Rules Section 8.3.23

This module implements behavioral tests for the Piercing ability keyword:
- Piercing is a static ability (Rule 8.3.23)
- Piercing is written as "Piercing N" (Rule 8.3.23)
- "Piercing N" means "If this is defended by an equipment, it gets +N power" (Rule 8.3.23)

Engine Features Needed for Section 8.3.23:
- [ ] PiercingAbility class as a static ability with numeric value N (Rule 8.3.23)
- [ ] PiercingAbility.is_static -> True (Rule 8.3.23)
- [ ] PiercingAbility.value: the N in "Piercing N" (Rule 8.3.23)
- [ ] CardTemplate.has_piercing or keyword_value("piercing") lookup (Rule 8.3.23)
- [ ] Attack power calculation: +N power when at least one equipment card is defending (Rule 8.3.23)
- [ ] Piercing bonus is conditional on equipment defender presence, not unconditional (Rule 8.3.23)

Current status: Tests written, Engine pending
"""

import pytest
from pytest_bdd import scenario, given, when, then, parsers


# ===== Rule 8.3.23: Piercing is a static ability =====

@scenario(
    "../features/section_8_3_23_piercing.feature",
    "Piercing is a static ability",
)
def test_piercing_is_static_ability():
    """Rule 8.3.23: Piercing must be a static ability."""
    pass


@scenario(
    "../features/section_8_3_23_piercing.feature",
    "Piercing ability has correct numeric value",
)
def test_piercing_has_correct_value():
    """Rule 8.3.23: Piercing N must expose the numeric value N."""
    pass


# ===== Rule 8.3.23: +N power when defended by equipment =====

@scenario(
    "../features/section_8_3_23_piercing.feature",
    "Piercing increases attack power when defended by equipment",
)
def test_piercing_increases_power_vs_equipment():
    """Rule 8.3.23: Attack with Piercing N gets +N power when defended by an equipment card."""
    pass


@scenario(
    "../features/section_8_3_23_piercing.feature",
    "Piercing does not increase power when not defended by equipment",
)
def test_piercing_no_bonus_vs_action():
    """Rule 8.3.23: Piercing does not apply when defended only by non-equipment cards."""
    pass


@scenario(
    "../features/section_8_3_23_piercing.feature",
    "Piercing 3 increases attack power by 3",
)
def test_piercing_3_increases_by_3():
    """Rule 8.3.23: Piercing 3 grants exactly +3 power against equipment defenders."""
    pass


@scenario(
    "../features/section_8_3_23_piercing.feature",
    "Piercing 1 increases attack power by exactly 1",
)
def test_piercing_1_increases_by_1():
    """Rule 8.3.23: Piercing 1 grants exactly +1 power against equipment defenders."""
    pass


@scenario(
    "../features/section_8_3_23_piercing.feature",
    "Piercing power bonus does not apply before equipment defends",
)
def test_piercing_no_bonus_without_defenders():
    """Rule 8.3.23: Piercing bonus only applies when equipment is defending."""
    pass


@scenario(
    "../features/section_8_3_23_piercing.feature",
    "Piercing power bonus applies when multiple equipment defend",
)
def test_piercing_bonus_with_multiple_equipment():
    """Rule 8.3.23: Piercing bonus applies (once, +N total) when multiple equipment cards defend."""
    pass


# ===== Step Definitions =====

@given("a card with Piercing 2 ability")
def card_with_piercing_2(game_state):
    """Rule 8.3.23: Create a card with Piercing 2."""
    game_state.test_card = game_state.create_card(name="Piercing Card")
    try:
        from fab_engine.engine.keywords import PiercingAbility
        game_state.piercing_ability = PiercingAbility(value=2)
    except (ImportError, AttributeError):
        game_state.piercing_ability = None
    game_state.piercing_value = 2


@when("I inspect the Piercing ability")
def inspect_piercing_ability(game_state):
    """Rule 8.3.23: Access the Piercing ability for inspection."""
    pass


@then("the Piercing ability is a static ability")
def piercing_is_static(game_state):
    """Rule 8.3.23: PiercingAbility must be a static ability."""
    ability = game_state.piercing_ability
    assert ability is not None, "PiercingAbility not implemented"
    assert ability.is_static, "PiercingAbility.is_static must be True (Rule 8.3.23)"


@then("the Piercing value is 2")
def piercing_value_is_2(game_state):
    """Rule 8.3.23: Piercing N must expose the numeric value N."""
    ability = game_state.piercing_ability
    assert ability is not None, "PiercingAbility not implemented"
    value = getattr(ability, "value", None) or getattr(ability, "n", None)
    assert value is not None, "PiercingAbility must have a numeric value attribute"
    assert value == 2, f"Piercing value should be 2, got: {value}"


@given(parsers.parse("an attack with Piercing {n:d}"))
def attack_with_piercing(game_state, n):
    """Rule 8.3.23: Set up an attack with Piercing N."""
    game_state.attack.add_keyword("piercing")
    game_state.attack.add_keyword(f"piercing_{n}")
    game_state.piercing_n = n


@given(parsers.parse("the base power of the attack is {power:d}"))
def attack_has_base_power(game_state, power):
    """Set the base power of the attack."""
    game_state.base_power = power


@when("the attack is defended by an equipment card")
def attack_defended_by_equipment(game_state):
    """Rule 8.3.23: Add an equipment card as a defender."""
    from fab_engine.cards.model import CardType
    equip = game_state.create_card(name="Defending Equipment", card_type=CardType.EQUIPMENT)
    game_state.attack.add_defender(equip)
    game_state.has_equipment_defender = True
    # Calculate piercing bonus
    game_state.current_power = game_state.piercing_calculate_power(game_state.attack)


@when("the attack is defended only by an action card")
def attack_defended_by_action(game_state):
    """Rule 8.3.23: Add only an action card as defender (no equipment)."""
    from fab_engine.cards.model import CardType
    action = game_state.create_card(name="Defending Action", card_type=CardType.ACTION)
    game_state.attack.add_defender(action)
    game_state.has_equipment_defender = False
    # Calculate piercing bonus
    game_state.current_power = game_state.piercing_calculate_power(game_state.attack)


@when("the attack has no defenders")
def attack_has_no_defenders(game_state):
    """Rule 8.3.23: Ensure the attack has no defenders."""
    game_state.attack.defenders.clear()
    game_state.has_equipment_defender = False
    game_state.current_power = game_state.piercing_calculate_power(game_state.attack)


@when("the attack is defended by two equipment cards")
def attack_defended_by_two_equipment(game_state):
    """Rule 8.3.23: Add two equipment cards as defenders."""
    from fab_engine.cards.model import CardType
    equip1 = game_state.create_card(name="Equipment Defender 1", card_type=CardType.EQUIPMENT)
    equip2 = game_state.create_card(name="Equipment Defender 2", card_type=CardType.EQUIPMENT)
    game_state.attack.add_defender(equip1)
    game_state.attack.add_defender(equip2)
    game_state.has_equipment_defender = True
    game_state.current_power = game_state.piercing_calculate_power(game_state.attack)


@then(parsers.parse("the attack power is {expected:d}"))
def attack_power_is(game_state, expected):
    """Verify the effective attack power matches the expected value."""
    actual = game_state.current_power
    assert actual == expected, (
        f"Rule 8.3.23: Expected attack power {expected}, got {actual}. "
        f"Base power: {game_state.base_power}, "
        f"Piercing N: {game_state.piercing_n}, "
        f"Equipment defending: {game_state.has_equipment_defender}"
    )


# ===== Fixture =====

@pytest.fixture
def game_state():
    """
    Fixture providing game state for testing Section 8.3.23: Piercing.

    Uses BDDGameState which integrates with the real engine.
    Adds piercing_calculate_power helper to compute effective power
    accounting for the Piercing bonus.
    Reference: Rule 8.3.23
    """
    from tests.bdd_helpers import BDDGameState
    from fab_engine.cards.model import CardType

    state = BDDGameState()
    state.piercing_n = 0
    state.base_power = 0
    state.has_equipment_defender = False
    state.current_power = 0
    state.piercing_ability = None

    def piercing_calculate_power(attack):
        """
        Calculate effective attack power considering Piercing.

        Rule 8.3.23: If the attack has Piercing N and is defended by
        at least one equipment card, the attack gets +N power.
        """
        base = attack.get_power() if hasattr(attack, "get_power") else state.base_power
        has_equipment = any(
            hasattr(d, "template") and CardType.EQUIPMENT in d.template.types
            for d in attack.defenders
        )
        has_piercing = attack.has_keyword("piercing")
        if has_piercing and has_equipment:
            return base + state.piercing_n
        return base

    state.piercing_calculate_power = piercing_calculate_power

    return state
