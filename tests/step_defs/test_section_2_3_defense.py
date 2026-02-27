"""
Step definitions for Section 2.3: Defense
Reference: Flesh and Blood Comprehensive Rules Section 2.3

This module implements behavioral tests for the defense property of cards
in Flesh and Blood.

Rule 2.3.1: Defense is a numeric property of an object, which represents the
            value contributed to the total sum of defense used in the damage
            step of combat.

Rule 2.3.2: The printed defense of a card is typically located at the bottom
            right corner of a card next to the {d} symbol. The printed defense
            defines the base defense of a card. If a card does not have a
            printed defense, it does not have the defense property
            (0 is a valid printed defense).

Rule 2.3.2a: If the defense of a card is represented as a (c), then the card
             has an ability that defines the defense of the card at any point
             in or out of the game. If the ability requires a number that
             cannot be determined, the defense of the card is 0.

Rule 2.3.3: The defense of an object can be modified. The term "defense" or
            the symbol {d} refers to the modified defense of an object.

Engine Features Needed for Section 2.3:
- [ ] `CardInstance.has_defense_property` property: False when no printed defense (Rule 2.3.2)
- [ ] `CardInstance.base_defense` property returning the unmodified printed defense (Rule 2.3.2)
- [ ] `CardInstance.defense` or `CardInstance.effective_defense` returning modified defense (Rule 2.3.3)
- [ ] `CardInstance.defense_contribution` used in damage step calculations (Rule 2.3.1)
- [ ] Defense modification effects that increase/decrease effective defense (Rule 2.3.3)
- [ ] Numeric defense capped at zero (cross-ref Rule 2.0.3c)
- [ ] Ability-defined defense for (c) notation cards (Rule 2.3.2a)
- [ ] Undefined (c) defense evaluates to 0 (Rule 2.3.2a)
"""

import pytest
from pytest_bdd import scenario, given, when, then, parsers
from dataclasses import dataclass, field
from typing import Optional


# ---------------------------------------------------------------------------
# Stub classes for testing Section 2.3 rules
# ---------------------------------------------------------------------------


@dataclass
class DefenseCheckResultStub:
    """
    Result of checking a card's defense property.

    Rule 2.3.1: Defense is a numeric property contributing to combat damage step.
    Rule 2.3.2: Printed defense defines base defense; no printed defense = no property.
    """

    has_defense_property: bool
    defense_value: Optional[int]  # None if no defense property
    is_numeric: bool = True


@dataclass
class DefenseCardStub:
    """
    Stub representing a card with a defense property.

    Models what the engine must implement for Section 2.3.
    Engine Features Needed:
    - [ ] CardInstance.base_defense: unmodified printed defense (Rule 2.3.2)
    - [ ] CardInstance.has_defense_property: False if no printed defense (Rule 2.3.2)
    - [ ] CardInstance.effective_defense: modified defense for rule/effect references (Rule 2.3.3)
    - [ ] CardInstance.defense_contribution: value contributed in damage step (Rule 2.3.1)
    """

    name: str = "Test Card"
    printed_defense: Optional[int] = None  # None if card has no defense property
    defense_modifier: int = 0  # Applied by effects (Rule 2.3.3)

    @property
    def has_defense_property(self) -> bool:
        """Rule 2.3.2: Card has defense property only if there is a printed defense."""
        return self.printed_defense is not None

    @property
    def base_defense(self) -> Optional[int]:
        """Rule 2.3.2: Base defense is the printed defense."""
        return self.printed_defense

    @property
    def effective_defense(self) -> Optional[int]:
        """
        Rule 2.3.3: The modified defense of the object.

        The term "defense" or the symbol {d} refers to this value.
        Capped at zero (cross-ref Rule 2.0.3c).
        """
        if self.printed_defense is None:
            return None
        return max(0, self.printed_defense + self.defense_modifier)

    @property
    def defense_contribution(self) -> int:
        """
        Rule 2.3.1: Value contributed to the total sum of defense in the damage step.

        If no defense property, contributes 0.
        """
        if self.effective_defense is None:
            return 0
        return self.effective_defense

    def check_defense(self) -> DefenseCheckResultStub:
        """Rule 2.3.1/2.3.2: Get the defense property of this card."""
        return DefenseCheckResultStub(
            has_defense_property=self.has_defense_property,
            defense_value=self.effective_defense,
            is_numeric=True,
        )

    def apply_defense_boost(self, amount: int):
        """
        Rule 2.3.3: Apply a positive defense modification from an effect.

        Engine Feature Needed: Effect system applying defense modifications.
        """
        self.defense_modifier += amount

    def apply_defense_reduction(self, amount: int):
        """
        Rule 2.3.3: Apply a negative defense modification from an effect.

        Engine Feature Needed: Effect system applying defense reductions.
        """
        self.defense_modifier -= amount


@dataclass
class AbilityDefinedDefenseCardStub:
    """
    Stub for a card whose defense is defined by an ability (the (c) notation).

    Rule 2.3.2a: If the defense of a card is represented as a (c), then the card
                 has an ability that defines the defense of the card. If the ability
                 requires a number that cannot be determined, the defense is 0.
    """

    name: str = "Crown of Seeds"
    ability_defined_value: Optional[int] = None  # None if cannot be determined

    @property
    def has_defense_property(self) -> bool:
        """Rule 2.3.2a: Card with (c) still has the defense property."""
        return True

    @property
    def base_defense(self) -> int:
        """
        Rule 2.3.2a: Ability-defined defense; returns 0 when undetermined.

        Engine Feature Needed: Ability-defined defense calculation.
        """
        if self.ability_defined_value is None:
            return 0
        return self.ability_defined_value

    @property
    def effective_defense(self) -> int:
        """Rule 2.3.3: Modified defense (base for ability-defined cards)."""
        return self.base_defense

    def check_defense(self) -> "DefenseCheckResultStub":
        """Rule 2.3.2a: Get the defense property of this ability-defined card."""
        return DefenseCheckResultStub(
            has_defense_property=self.has_defense_property,
            defense_value=self.effective_defense,
            is_numeric=True,
        )


@dataclass
class DefenseModificationResultStub:
    """
    Result of resolving the modified defense of an object.

    Rule 2.3.3: The term "defense" or {d} refers to the modified defense.
    """

    modified_defense: int
    base_defense: int
    is_modified: bool


# ---------------------------------------------------------------------------
# Scenarios
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_3_defense.feature",
    "Defense is a numeric property of a card",
)
def test_defense_is_numeric_property():
    """Rule 2.3.1/2.3.2: Defense is a numeric property of an object."""
    pass


@scenario(
    "../features/section_2_3_defense.feature",
    "Defense value is used in the damage step of combat",
)
def test_defense_value_used_in_damage_step():
    """Rule 2.3.1: Defense contributes to total sum in the damage step."""
    pass


@scenario(
    "../features/section_2_3_defense.feature",
    "Printed defense defines the base defense of a card",
)
def test_printed_defense_defines_base_defense():
    """Rule 2.3.2: Printed defense defines the base defense."""
    pass


@scenario(
    "../features/section_2_3_defense.feature",
    "Zero is a valid printed defense",
)
def test_zero_is_valid_printed_defense():
    """Rule 2.3.2: Zero is a valid printed defense value."""
    pass


@scenario(
    "../features/section_2_3_defense.feature",
    "Card without a printed defense lacks the defense property",
)
def test_card_without_printed_defense_lacks_property():
    """Rule 2.3.2: No printed defense means no defense property."""
    pass


@scenario(
    "../features/section_2_3_defense.feature",
    "Card with (c) defense has ability that defines defense",
)
def test_ability_defined_defense():
    """Rule 2.3.2a: (c) defense defined by an ability."""
    pass


@scenario(
    "../features/section_2_3_defense.feature",
    "Card with (c) defense evaluates to 0 when ability cannot determine value",
)
def test_ability_defined_defense_zero_when_undetermined():
    """Rule 2.3.2a: Ability-defined defense evaluates to 0 when undetermined."""
    pass


@scenario(
    "../features/section_2_3_defense.feature",
    "Defense of an object can be modified by effects",
)
def test_defense_can_be_modified():
    """Rule 2.3.3: Defense can be modified by effects."""
    pass


@scenario(
    "../features/section_2_3_defense.feature",
    "The term defense refers to the modified defense not base defense",
)
def test_defense_term_refers_to_modified_defense():
    """Rule 2.3.3: The term 'defense' refers to the modified defense."""
    pass


@scenario(
    "../features/section_2_3_defense.feature",
    "The symbol d refers to the modified defense of an object",
)
def test_d_symbol_refers_to_modified_defense():
    """Rule 2.3.3: The {d} symbol refers to the modified defense."""
    pass


@scenario(
    "../features/section_2_3_defense.feature",
    "Defense of an object can be decreased by effects",
)
def test_defense_can_be_decreased():
    """Rule 2.3.3: Defense can be decreased by effects."""
    pass


@scenario(
    "../features/section_2_3_defense.feature",
    "Defense cannot be reduced below zero",
)
def test_defense_cannot_be_negative():
    """Rule 2.0.3c cross-ref: Defense is capped at zero."""
    pass


@scenario(
    "../features/section_2_3_defense.feature",
    "Multiple cards each have independent defense values",
)
def test_multiple_cards_independent_defense():
    """Rule 2.3.2: Each card has its own defense property."""
    pass


# ---------------------------------------------------------------------------
# Step definitions
# ---------------------------------------------------------------------------


@given(parsers.parse("a defense card is created with a printed defense of {value:d}"))
def create_defense_card(game_state, value):
    """Rule 2.3.2: Create a card with the specified printed defense."""
    game_state.defense_card = DefenseCardStub(
        name=f"Test Defense Card ({value})",
        printed_defense=value,
    )


@given("a defense card is created with no printed defense")
def create_no_defense_card(game_state):
    """Rule 2.3.2: Create a card with no printed defense (no defense property)."""
    game_state.defense_card = DefenseCardStub(
        name="No Defense Card",
        printed_defense=None,
    )


@given(
    parsers.parse(
        'a defense card named "{name}" has defense defined by an ability with value {value:d}'
    )
)
def create_ability_defense_card(game_state, name, value):
    """Rule 2.3.2a: Create a card whose defense is defined by an ability."""
    game_state.defense_card = AbilityDefinedDefenseCardStub(
        name=name,
        ability_defined_value=value,
    )


@given("a defense card has defense defined by an ability that cannot be determined")
def create_undetermined_defense_card(game_state):
    """Rule 2.3.2a: Create a card with (c) defense where the ability value is undetermined."""
    game_state.defense_card = AbilityDefinedDefenseCardStub(
        name="Undetermined Defense Card",
        ability_defined_value=None,
    )


@given(
    parsers.parse(
        "a defense boost effect of plus {amount:d} is applied to the defense {base:d} card"
    )
)
def apply_defense_boost(game_state, amount, base):
    """Rule 2.3.3: Apply a positive defense modification to the card."""
    game_state.defense_card.apply_defense_boost(amount)


@given(
    parsers.parse(
        "a defense reduction effect of minus {amount:d} is applied to the defense {base:d} card"
    )
)
def apply_defense_reduction(game_state, amount, base):
    """Rule 2.3.3: Apply a negative defense modification to the card."""
    game_state.defense_card.apply_defense_reduction(amount)


@given(
    parsers.parse("another defense card is created with a printed defense of {value:d}")
)
def create_second_defense_card(game_state, value):
    """Rule 2.3.2: Create a second card with the specified printed defense."""
    game_state.second_defense_card = DefenseCardStub(
        name=f"Second Test Defense Card ({value})",
        printed_defense=value,
    )


@when(
    parsers.parse(
        "the engine checks the defense property of the defense {value:d} card"
    )
)
def check_defense_property_by_value(game_state, value):
    """Rule 2.3.1/2.3.2: Check the defense property of the card."""
    game_state.defense_check_result = game_state.defense_card.check_defense()


@when("the engine checks the defense property of the no-defense card")
def check_no_defense_property(game_state):
    """Rule 2.3.2: Check the defense property of a card with no printed defense."""
    game_state.defense_check_result = game_state.defense_card.check_defense()


@when("the engine checks the defense property of the ability-defense card")
def check_ability_defense_property(game_state):
    """Rule 2.3.2a: Check the defense property of an ability-defined defense card."""
    game_state.defense_check_result = game_state.defense_card.check_defense()


@when("the engine checks the defense property of the undetermined-defense card")
def check_undetermined_defense_property(game_state):
    """Rule 2.3.2a: Check the defense property of a card with undetermined ability defense."""
    game_state.defense_check_result = game_state.defense_card.check_defense()


@when(
    parsers.parse(
        "the engine calculates the defense contribution of the defense {value:d} card"
    )
)
def calculate_defense_contribution(game_state, value):
    """Rule 2.3.1: Calculate how much defense this card contributes to combat."""
    game_state.defense_contribution = game_state.defense_card.defense_contribution


@when(parsers.parse("the engine checks the base defense of the defense {value:d} card"))
def check_base_defense(game_state, value):
    """Rule 2.3.2: Check the base (unmodified) defense of the card."""
    game_state.base_defense_result = game_state.defense_card.base_defense


@when(
    parsers.parse(
        "the engine checks the modified defense of the defense {value:d} card"
    )
)
def check_modified_defense(game_state, value):
    """Rule 2.3.3: Check the modified (effective) defense of the card."""
    game_state.modified_defense_result = game_state.defense_card.effective_defense


@when(
    parsers.parse("the engine resolves the term defense for the defense {value:d} card")
)
def resolve_defense_term(game_state, value):
    """Rule 2.3.3: Resolve the term 'defense' for a card (gives modified defense)."""
    game_state.resolved_defense = game_state.defense_card.effective_defense
    game_state.base_defense_stored = game_state.defense_card.base_defense


@when(parsers.parse("the engine resolves the d symbol for the defense {value:d} card"))
def resolve_d_symbol(game_state, value):
    """Rule 2.3.3: Resolve the {d} symbol (gives modified defense)."""
    game_state.d_symbol_defense = game_state.defense_card.effective_defense


@when("the engine checks both defense cards")
def check_both_defense_cards(game_state):
    """Rule 2.3.2: Check the defense of both cards to verify independence."""
    game_state.first_card_defense = game_state.defense_card.effective_defense
    game_state.second_card_defense = game_state.second_defense_card.effective_defense


@then(parsers.parse("the defense {value:d} card should have the defense property"))
def assert_has_defense_property(game_state, value):
    """Rule 2.3.2: Verify that the card has the defense property."""
    assert game_state.defense_check_result.has_defense_property, (
        f"Card with printed defense {value} should have defense property"
    )


@then("the no-defense card should not have the defense property")
def assert_no_defense_property(game_state):
    """Rule 2.3.2: Verify that a card without printed defense lacks the property."""
    assert not game_state.defense_check_result.has_defense_property, (
        "Card without printed defense should not have the defense property"
    )


@then("the ability-defense card should have the defense property")
def assert_ability_defense_has_property(game_state):
    """Rule 2.3.2a: Verify that an ability-defined defense card has the property."""
    assert game_state.defense_check_result.has_defense_property, (
        "Card with (c) defense should still have the defense property"
    )


@then("the undetermined-defense card should have the defense property")
def assert_undetermined_defense_has_property(game_state):
    """Rule 2.3.2a: Card with (c) defense always has the defense property even if undetermined."""
    assert game_state.defense_check_result.has_defense_property, (
        "Card with (c) defense should have the defense property even when undetermined"
    )


@then(parsers.parse("the defense of the defense {value:d} card should be {expected:d}"))
def assert_defense_value(game_state, value, expected):
    """Rule 2.3.1/2.3.2: Verify the defense value."""
    assert game_state.defense_check_result.defense_value == expected, (
        f"Expected defense {expected}, got {game_state.defense_check_result.defense_value}"
    )


@then("the defense of the ability-defense card should be 5")
def assert_ability_defense_value_5(game_state):
    """Rule 2.3.2a: Verify the ability-defined defense value."""
    assert game_state.defense_check_result.defense_value == 5, (
        f"Expected ability-defined defense 5, got {game_state.defense_check_result.defense_value}"
    )


@then("the defense of the undetermined-defense card should be 0")
def assert_undetermined_defense_zero(game_state):
    """Rule 2.3.2a: Verify that undetermined (c) defense evaluates to 0."""
    assert game_state.defense_check_result.defense_value == 0, (
        f"Expected undetermined (c) defense to be 0, got {game_state.defense_check_result.defense_value}"
    )


@then("the defense of the defense 3 card should be numeric")
def assert_defense_is_numeric(game_state):
    """Rule 2.3.1: Verify that the defense property is numeric."""
    assert game_state.defense_check_result.is_numeric, (
        "Defense should be classified as a numeric property"
    )


@then(
    parsers.parse(
        "the defense contribution of the defense {value:d} card should be {expected:d}"
    )
)
def assert_defense_contribution(game_state, value, expected):
    """Rule 2.3.1: Verify the defense contribution in the damage step."""
    assert game_state.defense_contribution == expected, (
        f"Expected defense contribution {expected}, got {game_state.defense_contribution}"
    )


@then(
    parsers.parse(
        "the base defense of the defense {value:d} card should be {expected:d}"
    )
)
def assert_base_defense(game_state, value, expected):
    """Rule 2.3.2: Verify the base (unmodified) defense."""
    assert game_state.base_defense_result == expected, (
        f"Expected base defense {expected}, got {game_state.base_defense_result}"
    )


@then(
    parsers.parse(
        "the modified defense of the defense {value:d} card should be {expected:d}"
    )
)
def assert_modified_defense(game_state, value, expected):
    """Rule 2.3.3: Verify the modified (effective) defense."""
    assert game_state.modified_defense_result == expected, (
        f"Expected modified defense {expected}, got {game_state.modified_defense_result}"
    )


@then(
    parsers.parse(
        "the resolved defense of the defense {value:d} card should be {expected:d}"
    )
)
def assert_resolved_defense_term(game_state, value, expected):
    """Rule 2.3.3: Verify the resolved 'defense' term equals the modified defense."""
    assert game_state.resolved_defense == expected, (
        f"Expected resolved defense {expected}, got {game_state.resolved_defense}"
    )


@then(
    parsers.parse(
        "the base defense of the defense {value:d} card should remain {expected:d}"
    )
)
def assert_base_defense_unchanged(game_state, value, expected):
    """Rule 2.3.3: Verify base defense is unchanged after modification."""
    assert game_state.base_defense_stored == expected, (
        f"Expected base defense to remain {expected}, got {game_state.base_defense_stored}"
    )


@then(
    parsers.parse(
        "the d symbol defense of the defense {value:d} card should be {expected:d}"
    )
)
def assert_d_symbol_defense(game_state, value, expected):
    """Rule 2.3.3: Verify the {d} symbol resolves to the modified defense."""
    assert game_state.d_symbol_defense == expected, (
        f"Expected {{d}} symbol defense {expected}, got {game_state.d_symbol_defense}"
    )


@then(parsers.parse("the first card defense should be {expected:d}"))
def assert_first_card_defense(game_state, expected):
    """Rule 2.3.2: Verify the first card's defense."""
    assert game_state.first_card_defense == expected, (
        f"Expected first card defense {expected}, got {game_state.first_card_defense}"
    )


@then(parsers.parse("the second card defense should be {expected:d}"))
def assert_second_card_defense(game_state, expected):
    """Rule 2.3.2: Verify the second card's defense."""
    assert game_state.second_card_defense == expected, (
        f"Expected second card defense {expected}, got {game_state.second_card_defense}"
    )


# ---------------------------------------------------------------------------
# Fixture
# ---------------------------------------------------------------------------


@pytest.fixture
def game_state():
    """
    Fixture providing game state for testing.

    Uses BDDGameState which integrates with the real engine.
    Reference: Rule 2.3 - Defense property of cards.
    """
    from tests.bdd_helpers import BDDGameState

    state = BDDGameState()

    # Placeholders for test objects
    state.defense_card = None
    state.second_defense_card = None
    state.defense_check_result = None
    state.defense_contribution = None
    state.base_defense_result = None
    state.modified_defense_result = None
    state.resolved_defense = None
    state.base_defense_stored = None
    state.d_symbol_defense = None
    state.first_card_defense = None
    state.second_card_defense = None

    return state
