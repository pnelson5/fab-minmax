"""
Step definitions for Section 2.9: Power
Reference: Flesh and Blood Comprehensive Rules Section 2.9

This module implements behavioral tests for the power property of cards
in Flesh and Blood.

Rule 2.9.1: Power is a numeric property of an object, which represents the
            power value used in the damage step of combat.

Rule 2.9.2: The printed power of a card is typically located at the bottom
            left corner of a card next to the {p} symbol. The printed power
            defines the base power of a card. If a card does not have a
            printed power, it does not have the power property
            (0 is a valid printed power).

Rule 2.9.2a: If the power value of a card is represented as a (c), then the
             card has an ability that defines the base power of the card at any
             point in or out of the game. If the ability requires a number that
             cannot be determined, the power of the card is 0.

Rule 2.9.3: The power of an object can be modified. The term "power" or the
            symbol {p} refers to the modified power of an object.

Engine Features Needed for Section 2.9:
- [ ] `CardInstance.has_power_property` property: False when no printed power (Rule 2.9.2)
- [ ] `CardInstance.base_power` property returning the unmodified printed power (Rule 2.9.2)
- [ ] `CardInstance.power` or `CardInstance.effective_power` returning modified power (Rule 2.9.3)
- [ ] `CardInstance.combat_power` used in damage step calculations (Rule 2.9.1)
- [ ] Power modification effects that increase/decrease effective power (Rule 2.9.3)
- [ ] Numeric power capped at zero (cross-ref Rule 2.0.3c)
- [ ] Ability-defined power for (c) notation cards (Rule 2.9.2a)
- [ ] Undefined (c) power evaluates to 0 (Rule 2.9.2a)
"""

import pytest
from pytest_bdd import scenario, given, when, then, parsers
from dataclasses import dataclass, field
from typing import Optional


# ---------------------------------------------------------------------------
# Stub classes for testing Section 2.9 rules
# ---------------------------------------------------------------------------


@dataclass
class PowerCheckResultStub:
    """
    Result of checking a card's power property.

    Rule 2.9.1: Power is a numeric property used in the combat damage step.
    Rule 2.9.2: Printed power defines base power; no printed power = no property.
    """

    has_power_property: bool
    power_value: Optional[int]  # None if no power property
    is_numeric: bool = True


@dataclass
class PowerCardStub:
    """
    Stub representing a card with a power property.

    Models what the engine must implement for Section 2.9.
    Engine Features Needed:
    - [ ] CardInstance.base_power: unmodified printed power (Rule 2.9.2)
    - [ ] CardInstance.has_power_property: False if no printed power (Rule 2.9.2)
    - [ ] CardInstance.effective_power: modified power for rule/effect references (Rule 2.9.3)
    - [ ] CardInstance.combat_power: value used in the damage step of combat (Rule 2.9.1)
    """

    name: str = "Test Card"
    printed_power: Optional[int] = None  # None if card has no power property
    power_modifier: int = 0  # Applied by effects (Rule 2.9.3)

    @property
    def has_power_property(self) -> bool:
        """Rule 2.9.2: Card has power property only if there is a printed power."""
        return self.printed_power is not None

    @property
    def base_power(self) -> Optional[int]:
        """Rule 2.9.2: Base power is the printed power."""
        return self.printed_power

    @property
    def effective_power(self) -> Optional[int]:
        """
        Rule 2.9.3: The modified power of the object.

        The term "power" or the symbol {p} refers to this value.
        Capped at zero (cross-ref Rule 2.0.3c).
        """
        if self.printed_power is None:
            return None
        return max(0, self.printed_power + self.power_modifier)

    @property
    def combat_power(self) -> int:
        """
        Rule 2.9.1: Value used in the damage step of combat.

        If no power property, contributes 0.
        """
        if self.effective_power is None:
            return 0
        return self.effective_power

    def check_power(self) -> PowerCheckResultStub:
        """Rule 2.9.1/2.9.2: Get the power property of this card."""
        return PowerCheckResultStub(
            has_power_property=self.has_power_property,
            power_value=self.effective_power,
            is_numeric=True,
        )

    def apply_power_boost(self, amount: int):
        """
        Rule 2.9.3: Apply a positive power modification from an effect.

        Engine Feature Needed: Effect system applying power modifications.
        """
        self.power_modifier += amount

    def apply_power_reduction(self, amount: int):
        """
        Rule 2.9.3: Apply a negative power modification from an effect.

        Engine Feature Needed: Effect system applying power reductions.
        """
        self.power_modifier -= amount


@dataclass
class AbilityDefinedPowerCardStub:
    """
    Stub for a card whose power is defined by an ability (the (c) notation).

    Rule 2.9.2a: If the power value of a card is represented as a (c), then the
                 card has an ability that defines the base power of the card. If
                 the ability requires a number that cannot be determined, the
                 power of the card is 0.

    Example from rules: Mutated Mass has power (c), defined by a static ability.
    """

    name: str = "Mutated Mass"
    ability_defined_value: Optional[int] = None  # None if cannot be determined

    @property
    def has_power_property(self) -> bool:
        """Rule 2.9.2a: Card with (c) still has the power property."""
        return True

    @property
    def base_power(self) -> int:
        """
        Rule 2.9.2a: Ability-defined power; returns 0 when undetermined.

        Engine Feature Needed: Ability-defined power calculation.
        """
        if self.ability_defined_value is None:
            return 0
        return self.ability_defined_value

    @property
    def effective_power(self) -> int:
        """Rule 2.9.3: Modified power (base for ability-defined cards)."""
        return self.base_power

    def check_power(self) -> "PowerCheckResultStub":
        """Rule 2.9.2a: Get the power property of this ability-defined card."""
        return PowerCheckResultStub(
            has_power_property=self.has_power_property,
            power_value=self.effective_power,
            is_numeric=True,
        )


@dataclass
class PowerModificationResultStub:
    """
    Result of resolving the modified power of an object.

    Rule 2.9.3: The term "power" or {p} refers to the modified power.
    """

    modified_power: int
    base_power: int
    is_modified: bool


# ---------------------------------------------------------------------------
# Scenarios
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_9_power.feature",
    "Power is a numeric property of a card",
)
def test_power_is_numeric_property():
    """Rule 2.9.1/2.9.2: Power is a numeric property of an object."""
    pass


@scenario(
    "../features/section_2_9_power.feature",
    "Power value is used in the damage step of combat",
)
def test_power_value_used_in_damage_step():
    """Rule 2.9.1: Power is used in the damage step of combat."""
    pass


@scenario(
    "../features/section_2_9_power.feature",
    "Printed power defines the base power of a card",
)
def test_printed_power_defines_base_power():
    """Rule 2.9.2: Printed power defines the base power."""
    pass


@scenario(
    "../features/section_2_9_power.feature",
    "Zero is a valid printed power",
)
def test_zero_is_valid_printed_power():
    """Rule 2.9.2: Zero is a valid printed power value."""
    pass


@scenario(
    "../features/section_2_9_power.feature",
    "Card without a printed power lacks the power property",
)
def test_card_without_printed_power_lacks_property():
    """Rule 2.9.2: No printed power means no power property."""
    pass


@scenario(
    "../features/section_2_9_power.feature",
    "Card with (c) power has ability that defines power",
)
def test_ability_defined_power():
    """Rule 2.9.2a: (c) power defined by an ability."""
    pass


@scenario(
    "../features/section_2_9_power.feature",
    "Card with (c) power evaluates to 0 when ability cannot determine value",
)
def test_ability_defined_power_zero_when_undetermined():
    """Rule 2.9.2a: Ability-defined power evaluates to 0 when undetermined."""
    pass


@scenario(
    "../features/section_2_9_power.feature",
    "Power of an object can be modified by effects",
)
def test_power_can_be_modified():
    """Rule 2.9.3: Power can be modified by effects."""
    pass


@scenario(
    "../features/section_2_9_power.feature",
    "The term power refers to the modified power not base power",
)
def test_power_term_refers_to_modified_power():
    """Rule 2.9.3: The term 'power' refers to the modified power."""
    pass


@scenario(
    "../features/section_2_9_power.feature",
    "The symbol p refers to the modified power of an object",
)
def test_p_symbol_refers_to_modified_power():
    """Rule 2.9.3: The {p} symbol refers to the modified power."""
    pass


@scenario(
    "../features/section_2_9_power.feature",
    "Power of an object can be decreased by effects",
)
def test_power_can_be_decreased():
    """Rule 2.9.3: Power can be decreased by effects."""
    pass


@scenario(
    "../features/section_2_9_power.feature",
    "Power cannot be reduced below zero",
)
def test_power_cannot_be_negative():
    """Rule 2.0.3c cross-ref: Power is capped at zero."""
    pass


@scenario(
    "../features/section_2_9_power.feature",
    "Multiple cards each have independent power values",
)
def test_multiple_cards_independent_power():
    """Rule 2.9.2: Each card has its own power property."""
    pass


# ---------------------------------------------------------------------------
# Step definitions
# ---------------------------------------------------------------------------


@given(parsers.parse("a power card is created with a printed power of {value:d}"))
def create_power_card(game_state, value):
    """Rule 2.9.2: Create a card with the specified printed power."""
    game_state.power_card = PowerCardStub(
        name=f"Test Power Card ({value})",
        printed_power=value,
    )


@given("a power card is created with no printed power")
def create_no_power_card(game_state):
    """Rule 2.9.2: Create a card with no printed power (no power property)."""
    game_state.power_card = PowerCardStub(
        name="No Power Card",
        printed_power=None,
    )


@given(
    parsers.parse(
        'a power card named "{name}" has power defined by an ability with value {value:d}'
    )
)
def create_ability_power_card(game_state, name, value):
    """Rule 2.9.2a: Create a card whose power is defined by an ability."""
    game_state.power_card = AbilityDefinedPowerCardStub(
        name=name,
        ability_defined_value=value,
    )


@given("a power card has power defined by an ability that cannot be determined")
def create_undetermined_power_card(game_state):
    """Rule 2.9.2a: Create a card with (c) power where the ability value is undetermined."""
    game_state.power_card = AbilityDefinedPowerCardStub(
        name="Undetermined Power Card",
        ability_defined_value=None,
    )


@given(
    parsers.parse(
        "a power boost effect of plus {amount:d} is applied to the power {base:d} card"
    )
)
def apply_power_boost(game_state, amount, base):
    """Rule 2.9.3: Apply a positive power modification to the card."""
    game_state.power_card.apply_power_boost(amount)


@given(
    parsers.parse(
        "a power reduction effect of minus {amount:d} is applied to the power {base:d} card"
    )
)
def apply_power_reduction(game_state, amount, base):
    """Rule 2.9.3: Apply a negative power modification to the card."""
    game_state.power_card.apply_power_reduction(amount)


@given(parsers.parse("another power card is created with a printed power of {value:d}"))
def create_second_power_card(game_state, value):
    """Rule 2.9.2: Create a second card with the specified printed power."""
    game_state.second_power_card = PowerCardStub(
        name=f"Second Test Power Card ({value})",
        printed_power=value,
    )


@when(parsers.parse("the engine checks the power property of the power {value:d} card"))
def check_power_property_by_value(game_state, value):
    """Rule 2.9.1/2.9.2: Check the power property of the card."""
    game_state.power_check_result = game_state.power_card.check_power()


@when("the engine checks the power property of the no-power card")
def check_no_power_property(game_state):
    """Rule 2.9.2: Check the power property of a card with no printed power."""
    game_state.power_check_result = game_state.power_card.check_power()


@when("the engine checks the power property of the ability-power card")
def check_ability_power_property(game_state):
    """Rule 2.9.2a: Check the power property of an ability-defined power card."""
    game_state.power_check_result = game_state.power_card.check_power()


@when("the engine checks the power property of the undetermined-power card")
def check_undetermined_power_property(game_state):
    """Rule 2.9.2a: Check the power property of a card with undetermined ability power."""
    game_state.power_check_result = game_state.power_card.check_power()


@when(
    parsers.parse(
        "the engine calculates the power value of the power {value:d} card for combat"
    )
)
def calculate_combat_power(game_state, value):
    """Rule 2.9.1: Calculate the power value this card uses in the combat damage step."""
    game_state.combat_power_result = game_state.power_card.combat_power


@when(parsers.parse("the engine checks the base power of the power {value:d} card"))
def check_base_power(game_state, value):
    """Rule 2.9.2: Check the base (unmodified) power of the card."""
    game_state.base_power_result = game_state.power_card.base_power


@when(parsers.parse("the engine checks the modified power of the power {value:d} card"))
def check_modified_power(game_state, value):
    """Rule 2.9.3: Check the modified (effective) power of the card."""
    game_state.modified_power_result = game_state.power_card.effective_power


@when(parsers.parse("the engine resolves the term power for the power {value:d} card"))
def resolve_power_term(game_state, value):
    """Rule 2.9.3: Resolve the term 'power' for a card (gives modified power)."""
    game_state.resolved_power = game_state.power_card.effective_power
    game_state.base_power_stored = game_state.power_card.base_power


@when(parsers.parse("the engine resolves the p symbol for the power {value:d} card"))
def resolve_p_symbol(game_state, value):
    """Rule 2.9.3: Resolve the {p} symbol (gives modified power)."""
    game_state.p_symbol_power = game_state.power_card.effective_power


@when("the engine checks both power cards")
def check_both_power_cards(game_state):
    """Rule 2.9.2: Check the power of both cards to verify independence."""
    game_state.first_card_power = game_state.power_card.effective_power
    game_state.second_card_power = game_state.second_power_card.effective_power


@then(parsers.parse("the power {value:d} card should have the power property"))
def assert_has_power_property(game_state, value):
    """Rule 2.9.2: Verify that the card has the power property."""
    assert game_state.power_check_result.has_power_property, (
        f"Card with printed power {value} should have power property"
    )


@then("the no-power card should not have the power property")
def assert_no_power_property(game_state):
    """Rule 2.9.2: Verify that a card without printed power lacks the property."""
    assert not game_state.power_check_result.has_power_property, (
        "Card without printed power should not have the power property"
    )


@then("the ability-power card should have the power property")
def assert_ability_power_has_property(game_state):
    """Rule 2.9.2a: Verify that an ability-defined power card has the property."""
    assert game_state.power_check_result.has_power_property, (
        "Card with (c) power should still have the power property"
    )


@then("the undetermined-power card should have the power property")
def assert_undetermined_power_has_property(game_state):
    """Rule 2.9.2a: Card with (c) power always has the power property even if undetermined."""
    assert game_state.power_check_result.has_power_property, (
        "Card with (c) power should have the power property even when undetermined"
    )


@then(parsers.parse("the power of the power {value:d} card should be {expected:d}"))
def assert_power_value(game_state, value, expected):
    """Rule 2.9.1/2.9.2: Verify the power value."""
    assert game_state.power_check_result.power_value == expected, (
        f"Expected power {expected}, got {game_state.power_check_result.power_value}"
    )


@then("the power of the ability-power card should be 7")
def assert_ability_power_value_7(game_state):
    """Rule 2.9.2a: Verify the ability-defined power value."""
    assert game_state.power_check_result.power_value == 7, (
        f"Expected ability-defined power 7, got {game_state.power_check_result.power_value}"
    )


@then("the power of the undetermined-power card should be 0")
def assert_undetermined_power_zero(game_state):
    """Rule 2.9.2a: Verify that undetermined (c) power evaluates to 0."""
    assert game_state.power_check_result.power_value == 0, (
        f"Expected undetermined (c) power to be 0, got {game_state.power_check_result.power_value}"
    )


@then("the power of the power 3 card should be numeric")
def assert_power_is_numeric(game_state):
    """Rule 2.9.1: Verify that the power property is numeric."""
    assert game_state.power_check_result.is_numeric, (
        "Power should be classified as a numeric property"
    )


@then(
    parsers.parse("the combat power of the power {value:d} card should be {expected:d}")
)
def assert_combat_power(game_state, value, expected):
    """Rule 2.9.1: Verify the power value used in the damage step of combat."""
    assert game_state.combat_power_result == expected, (
        f"Expected combat power {expected}, got {game_state.combat_power_result}"
    )


@then(
    parsers.parse("the base power of the power {value:d} card should be {expected:d}")
)
def assert_base_power(game_state, value, expected):
    """Rule 2.9.2: Verify the base (unmodified) power."""
    assert game_state.base_power_result == expected, (
        f"Expected base power {expected}, got {game_state.base_power_result}"
    )


@then(
    parsers.parse(
        "the modified power of the power {value:d} card should be {expected:d}"
    )
)
def assert_modified_power(game_state, value, expected):
    """Rule 2.9.3: Verify the modified (effective) power."""
    assert game_state.modified_power_result == expected, (
        f"Expected modified power {expected}, got {game_state.modified_power_result}"
    )


@then(
    parsers.parse(
        "the resolved power of the power {value:d} card should be {expected:d}"
    )
)
def assert_resolved_power_term(game_state, value, expected):
    """Rule 2.9.3: Verify the resolved 'power' term equals the modified power."""
    assert game_state.resolved_power == expected, (
        f"Expected resolved power {expected}, got {game_state.resolved_power}"
    )


@then(
    parsers.parse(
        "the base power of the power {value:d} card should remain {expected:d}"
    )
)
def assert_base_power_unchanged(game_state, value, expected):
    """Rule 2.9.3: Verify base power is unchanged after modification."""
    assert game_state.base_power_stored == expected, (
        f"Expected base power to remain {expected}, got {game_state.base_power_stored}"
    )


@then(
    parsers.parse(
        "the p symbol power of the power {value:d} card should be {expected:d}"
    )
)
def assert_p_symbol_power(game_state, value, expected):
    """Rule 2.9.3: Verify the {p} symbol resolves to the modified power."""
    assert game_state.p_symbol_power == expected, (
        f"Expected {{p}} symbol power {expected}, got {game_state.p_symbol_power}"
    )


@then(parsers.parse("the first card power should be {expected:d}"))
def assert_first_card_power(game_state, expected):
    """Rule 2.9.2: Verify the first card's power."""
    assert game_state.first_card_power == expected, (
        f"Expected first card power {expected}, got {game_state.first_card_power}"
    )


@then(parsers.parse("the second card power should be {expected:d}"))
def assert_second_card_power(game_state, expected):
    """Rule 2.9.2: Verify the second card's power."""
    assert game_state.second_card_power == expected, (
        f"Expected second card power {expected}, got {game_state.second_card_power}"
    )


# ---------------------------------------------------------------------------
# Fixture
# ---------------------------------------------------------------------------


@pytest.fixture
def game_state():
    """
    Fixture providing game state for testing.

    Uses BDDGameState which integrates with the real engine.
    Reference: Rule 2.9 - Power property of cards.
    """
    from tests.bdd_helpers import BDDGameState

    state = BDDGameState()

    # Placeholders for test objects
    state.power_card = None
    state.second_power_card = None
    state.power_check_result = None
    state.combat_power_result = None
    state.base_power_result = None
    state.modified_power_result = None
    state.resolved_power = None
    state.base_power_stored = None
    state.p_symbol_power = None
    state.first_card_power = None
    state.second_card_power = None

    return state
