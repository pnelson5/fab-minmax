"""
Step definitions for Section 2.0: General (Object Properties)
Reference: Flesh and Blood Comprehensive Rules Section 2.0

This module implements behavioral tests for the fundamental rules about
object properties in Flesh and Blood:

Rule 2.0.1: A property is an attribute of an object defining game interactions.
            13 properties: abilities, color strip, cost, defense, intellect,
            life, name, pitch, power, subtypes, supertypes, text box, type.
Rule 2.0.1a: Abilities are properties (not objects). Activated abilities have
             cost and type properties.
Rule 2.0.2: Properties determined by true text on cards.fabtcg.com.
Rule 2.0.3: Numeric properties have numeric values modifiable by effects/counters.
Rule 2.0.3a: Effects modifying numeric properties do not change base value unless
             specified. "gain"/"get"/"have"/"lose" modifies value, not base value.
Rule 2.0.3b: Base value modification is NOT considered gaining/losing.
             Non-base value modification IS considered gaining/losing.
Rule 2.0.3c: Numeric properties cannot be negative; capped at zero.
Rule 2.0.3d: +/-1 property counters modify value, not base value.
Rule 2.0.4: "Gaining" = didn't have property, now does.
            "Losing" = had property, no longer does.
            Gaining/losing property is NOT the same as increasing/decreasing value.
Rule 2.0.5: Source of a property is the object that has it.

Engine Features Needed for Section 2.0:
- [ ] `ObjectProperty` system with enumeration of all 13 property types (Rule 2.0.1)
- [ ] `CardInstance.get_properties()` -> Set[str] (Rule 2.0.1)
- [ ] `CardInstance.has_property(name)` method (Rule 2.0.1)
- [ ] `ActivatedAbility.cost` and `ActivatedAbility.type` properties (Rule 2.0.1a)
- [ ] `CardInstance.base_power` distinct from `effective_power` (Rule 2.0.3a)
- [ ] `CardInstance.base_defense` distinct from `effective_defense` (Rule 2.0.3a)
- [ ] Effect tracking whether modification is "base" or "non-base" (Rules 2.0.3a, 2.0.3b)
- [ ] `PropertyModification.is_base_modification` flag (Rule 2.0.3b)
- [ ] Numeric properties capped at zero (Rule 2.0.3c)
- [ ] `CardInstance.gained_properties` tracking set (Rule 2.0.4)
- [ ] `CardInstance.lost_properties` tracking set (Rule 2.0.4)
- [ ] `PropertySource` system tracking which object a property belongs to (Rule 2.0.5)
"""

import pytest
from pytest_bdd import scenario, given, when, then, parsers
from dataclasses import dataclass, field
from typing import Optional, Set, List


# ---------------------------------------------------------------------------
# Stub classes for testing Section 2.0 rules
# ---------------------------------------------------------------------------


@dataclass
class PropertyCheckResultStub:
    """Result of checking what properties an object has."""

    property_names: Set[str] = field(default_factory=set)

    def has_property(self, name: str) -> bool:
        return name in self.property_names

    def count(self) -> int:
        return len(self.property_names)


@dataclass
class ActivatedAbilityStub:
    """
    Stub for an activated ability.

    Rule 2.0.1a: Activated abilities have cost and type properties.
    """

    resource_cost: int = 0
    ability_type: str = "activated"

    @property
    def cost(self) -> int:
        """Rule 2.0.1a: Activated abilities have cost property."""
        return self.resource_cost

    @property
    def type(self) -> str:
        """Rule 2.0.1a: Activated abilities have type property."""
        return self.ability_type

    def has_property(self, name: str) -> bool:
        """Check if ability has a given property."""
        return name in ("cost", "type")


@dataclass
class NumericPropertyModificationStub:
    """
    Stub representing an effect that modifies a numeric property.

    Rules 2.0.3a, 2.0.3b: Tracks whether modification is to base or non-base.
    """

    amount: int = 0
    is_base_modification: bool = False
    modifier_type: str = "gain"  # "gain", "set", "base_set", "base_double"

    def is_classified_as_gaining(self) -> bool:
        """
        Rule 2.0.3b: Non-base modifications are classified as gaining/losing.
        Base modifications are NOT classified as gaining/losing.
        """
        return not self.is_base_modification

    def is_classified_as_losing(self) -> bool:
        """Rule 2.0.3b: Non-base decreases are classified as losing."""
        return not self.is_base_modification and self.amount < 0


@dataclass
class PropertyGainLossResultStub:
    """
    Stub tracking gain/loss of properties.

    Rule 2.0.4: Gaining = property newly acquired; Losing = property removed.
    Gaining/Losing a property is distinct from increasing/decreasing value.
    """

    property_name: str = ""
    had_before: bool = False
    has_now: bool = False

    @property
    def was_gained(self) -> bool:
        """Rule 2.0.4: Gained if didn't have before and now has."""
        return not self.had_before and self.has_now

    @property
    def was_lost(self) -> bool:
        """Rule 2.0.4: Lost if had before and no longer has."""
        return self.had_before and not self.has_now

    @property
    def is_value_increase(self) -> bool:
        """
        Rule 2.0.4: Gaining a property is NOT the same as increasing its value.
        Gaining/losing a boolean property (like "dominate") is not about values.
        """
        return False  # Gaining a property is never classified as increasing value


@dataclass
class PropertySourceStub:
    """
    Stub representing a property source.

    Rule 2.0.5: Source of a property is the object that has it.
    """

    source_object_name: str = ""
    property_name: str = ""


class CardPropertyStub:
    """
    Stub wrapping a card's property system.

    Used to test Rules 2.0.1 through 2.0.5 without requiring full engine
    property system implementation.
    """

    # Rule 2.0.1: All 13 possible object properties
    ALL_PROPERTIES = {
        "abilities",
        "color",
        "cost",
        "defense",
        "intellect",
        "life",
        "name",
        "pitch",
        "power",
        "subtypes",
        "supertypes",
        "text_box",
        "type",
    }

    def __init__(
        self,
        name: str,
        power: int = -1,
        defense: int = -1,
        cost: int = -1,
        pitch: int = -1,
        life: int = 0,
        intellect: int = 0,
        keywords: List[str] = None,
        has_power: bool = True,
        has_defense: bool = True,
        has_cost: bool = True,
        has_pitch: bool = False,
    ):
        self.name = name
        self._base_power = power
        self._base_defense = defense
        self._base_cost = cost
        self._base_pitch = pitch
        self._life = life
        self._intellect = intellect
        self._keywords = keywords or []
        self._has_power = has_power
        self._has_defense = has_defense
        self._has_cost = has_cost
        self._has_pitch = has_pitch

        # Effect and counter modifications (non-base)
        self._power_modifier = 0
        self._defense_modifier = 0

        # Property tracking (Rule 2.0.4)
        self._gained_properties: Set[str] = set()
        self._lost_properties: Set[str] = set()
        self._boolean_properties: Set[str] = set()
        for kw in self._keywords:
            self._boolean_properties.add(kw)

    def has_property(self, name: str) -> bool:
        """Rule 2.0.1: Check if object has a specific property."""
        if name == "power":
            return self._has_power
        if name == "defense":
            return self._has_defense
        if name == "cost":
            return self._has_cost
        if name == "pitch":
            return self._has_pitch
        if name == "name":
            return True
        if name == "type":
            return True
        if name == "abilities":
            return len(self._keywords) > 0
        # Check keyword/boolean properties
        if name in self._boolean_properties:
            return True
        return False

    def get_properties(self) -> Set[str]:
        """Rule 2.0.1: Get all property names this card has."""
        props = {"name", "type"}
        if self._has_power:
            props.add("power")
        if self._has_defense:
            props.add("defense")
        if self._has_cost:
            props.add("cost")
        if self._has_pitch:
            props.add("pitch")
        if self._life > 0:
            props.add("life")
        if self._intellect > 0:
            props.add("intellect")
        if self._keywords:
            props.add("abilities")
        return props

    @property
    def base_power(self) -> int:
        """Rule 2.0.3a: Base power is unchanged by non-base effects."""
        return self._base_power

    @property
    def effective_power(self) -> int:
        """Rule 2.0.3c: Effective power capped at zero (cannot be negative)."""
        if self._base_power < 0:
            return -1  # Property not present
        return max(0, self._base_power + self._power_modifier)

    @property
    def base_defense(self) -> int:
        """Rule 2.0.3a: Base defense is unchanged by non-base effects."""
        return self._base_defense

    @property
    def effective_defense(self) -> int:
        """Rule 2.0.3c: Effective defense capped at zero (cannot be negative)."""
        if self._base_defense < 0:
            return -1  # Property not present
        return max(0, self._base_defense + self._defense_modifier)

    def apply_non_base_power_modifier(
        self, amount: int
    ) -> NumericPropertyModificationStub:
        """
        Rule 2.0.3a: Apply a non-base power modifier.
        Modifies effective power without changing base power.
        """
        self._power_modifier += amount
        return NumericPropertyModificationStub(
            amount=amount,
            is_base_modification=False,
            modifier_type="gain" if amount > 0 else "lose",
        )

    def apply_base_power_modifier(self, amount: int) -> NumericPropertyModificationStub:
        """
        Rule 2.0.3a/3b: Apply a base power modifier.
        Explicitly modifies base power value.
        NOT classified as "gaining" or "losing" power.
        """
        self._base_power = max(0, self._base_power + amount)
        return NumericPropertyModificationStub(
            amount=amount,
            is_base_modification=True,
            modifier_type="base_set",
        )

    def double_base_power(self) -> NumericPropertyModificationStub:
        """
        Rule 2.0.3b: Double the base power (Big Bully example).
        This is NOT classified as gaining power.
        """
        self._base_power = self._base_power * 2
        return NumericPropertyModificationStub(
            amount=self._base_power,
            is_base_modification=True,
            modifier_type="base_double",
        )

    def apply_defense_modifier(self, amount: int) -> NumericPropertyModificationStub:
        """Rule 2.0.3c: Apply defense modifier. Result capped at zero."""
        self._defense_modifier += amount
        return NumericPropertyModificationStub(
            amount=amount,
            is_base_modification=False,
        )

    def add_power_counter(self, amount: int) -> NumericPropertyModificationStub:
        """
        Rule 2.0.3d: Add a +/-1 power counter.
        Counters modify effective value, not base value.
        """
        self._power_modifier += amount
        return NumericPropertyModificationStub(
            amount=amount,
            is_base_modification=False,
            modifier_type="counter",
        )

    def grant_boolean_property(self, property_name: str) -> PropertyGainLossResultStub:
        """
        Rule 2.0.4: Grant a boolean property the card didn't have before.
        This is a "gain" of the property.
        """
        had_before = property_name in self._boolean_properties
        self._boolean_properties.add(property_name)
        self._gained_properties.add(property_name)
        return PropertyGainLossResultStub(
            property_name=property_name,
            had_before=had_before,
            has_now=True,
        )

    def remove_boolean_property(self, property_name: str) -> PropertyGainLossResultStub:
        """
        Rule 2.0.4: Remove a boolean property the card previously had.
        This is a "loss" of the property.
        """
        had_before = property_name in self._boolean_properties
        self._boolean_properties.discard(property_name)
        self._lost_properties.add(property_name)
        return PropertyGainLossResultStub(
            property_name=property_name,
            had_before=had_before,
            has_now=False,
        )

    def has_boolean_property(self, name: str) -> bool:
        """Check if card currently has a boolean property (like "go again", "dominate")."""
        return name in self._boolean_properties

    def is_game_object(self) -> bool:
        """Rule 2.0.1a: Properties are not objects; cards are objects."""
        return True

    def get_property_source(self, property_name: str) -> Optional["PropertySourceStub"]:
        """
        Rule 2.0.5: Get the source of a given property.
        The source is the object that has the property.
        """
        if (
            self.has_property(property_name)
            or property_name in self._boolean_properties
        ):
            return PropertySourceStub(
                source_object_name=self.name,
                property_name=property_name,
            )
        return None


# ---------------------------------------------------------------------------
# Test fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def game_state():
    """
    Fixture providing game state for testing Section 2.0.

    Uses CardPropertyStub for property system tests.
    Reference: Rule 2.0 - Object Properties General Rules
    """
    from tests.bdd_helpers import BDDGameState

    state = BDDGameState()
    state.card = None
    state.ability = None
    state.modification = None
    state.gain_loss_result = None
    state.property_check = None
    state.property_list = None
    return state


# ---------------------------------------------------------------------------
# Scenario: Card has recognized game properties
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_0_general.feature",
    "Card has recognized game properties",
)
def test_card_has_recognized_game_properties():
    """Rule 2.0.1: Properties are attributes of objects interacting with rules/effects."""
    pass


@given(
    parsers.parse(
        'a card named "{name}" with power {power:d} and defense {defense:d} and cost {cost:d}'
    )
)
def step_card_with_power_defense_cost(game_state, name, power, defense, cost):
    """Rule 2.0.1: Set up a card with multiple properties."""
    game_state.card = CardPropertyStub(
        name=name,
        power=power,
        defense=defense,
        cost=cost,
    )


@when("the game checks the card's properties")
def step_check_card_properties(game_state):
    """Rule 2.0.1: Check what properties the card has."""
    game_state.property_check = game_state.card.get_properties()


@then(parsers.parse('the card should have a "{prop}" property'))
def step_card_should_have_property(game_state, prop):
    """Rule 2.0.1: Verify a specific property exists."""
    assert prop in game_state.property_check, (
        f"Expected card to have '{prop}' property but it did not. "
        f"Properties: {game_state.property_check}"
    )


# ---------------------------------------------------------------------------
# Scenario: There are 13 possible object properties
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_0_general.feature",
    "There are 13 possible object properties",
)
def test_there_are_13_possible_object_properties():
    """Rule 2.0.1: Exactly 13 properties defined: abilities, color, cost, defense,
    intellect, life, name, pitch, power, subtypes, supertypes, text_box, type."""
    pass


@given("the game engine's property system")
def step_game_engine_property_system(game_state):
    """Rule 2.0.1: Access the property system."""
    game_state.property_system = CardPropertyStub.ALL_PROPERTIES


@when("the engine lists all possible object properties")
def step_engine_lists_all_properties(game_state):
    """Rule 2.0.1: Get the complete list of possible object properties."""
    game_state.property_list = game_state.property_system


@then("the property list should contain exactly 13 property names")
def step_property_list_has_13(game_state):
    """Rule 2.0.1: Exactly 13 properties are defined."""
    count = len(game_state.property_list)
    assert count == 13, (
        f"Expected exactly 13 object properties, but got {count}. "
        f"Properties: {game_state.property_list}"
    )


@then(parsers.parse('the properties should include "{prop_name}"'))
def step_properties_should_include(game_state, prop_name):
    """Rule 2.0.1: Verify a specific property is in the list."""
    assert prop_name in game_state.property_list, (
        f"Expected property '{prop_name}' in property list. "
        f"Properties: {game_state.property_list}"
    )


# ---------------------------------------------------------------------------
# Scenario: An ability is a property not an object
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_0_general.feature",
    "An ability is a property not an object",
)
def test_ability_is_property_not_object():
    """Rule 2.0.1a: Abilities are properties, not objects."""
    pass


@given(parsers.parse('a card with the keyword "{keyword}"'))
def step_card_with_keyword(game_state, keyword):
    """Rule 2.0.1a: Set up a card with a specific keyword ability."""
    game_state.card = CardPropertyStub(
        name="Go Again Card",
        power=3,
        defense=2,
        cost=1,
        keywords=[keyword],
    )
    game_state.keyword = keyword


@when(parsers.parse('the game checks if "{prop}" is a property of the card'))
def step_check_if_property_of_card(game_state, prop):
    """Rule 2.0.1a: Check whether something is a property of the card."""
    game_state.is_property = game_state.card.has_boolean_property(prop)
    game_state.checked_prop = prop


@then(parsers.parse('"{prop}" should be recognized as a property of the card'))
def step_should_be_property(game_state, prop):
    """Rule 2.0.1a: Ability should be recognized as a property."""
    assert game_state.card.has_boolean_property(prop), (
        f"Expected '{prop}' to be a property of the card, but it was not."
    )


@then(parsers.parse('"{prop}" should not be recognized as a game object'))
def step_should_not_be_game_object(game_state, prop):
    """Rule 2.0.1a: Abilities are properties, not game objects."""
    # The keyword/ability itself (like "go again") is a property, not an object.
    # The card itself is a game object; the ability is a property of the card.
    # We verify the card IS a game object, but the ability text is not.
    assert game_state.card.is_game_object(), "The card itself should be a game object"
    # Verify: a keyword/ability is not itself a game object
    # (it has no owner_id, controller_id, etc.)
    # This tests the concept that abilities are attributes, not independent objects.
    assert prop not in {"card", "hero", "token", "weapon", "equipment"}, (
        f"The ability '{prop}' should not be a game object category"
    )


# ---------------------------------------------------------------------------
# Scenario: An activated ability has cost and type properties
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_0_general.feature",
    "An activated ability has cost and type properties",
)
def test_activated_ability_has_cost_and_type_properties():
    """Rule 2.0.1a: Activated abilities have cost and type properties."""
    pass


@given(parsers.parse("an activated ability with a resource cost of {cost:d}"))
def step_activated_ability_with_cost(game_state, cost):
    """Rule 2.0.1a: Create an activated ability with a specific cost."""
    game_state.ability = ActivatedAbilityStub(resource_cost=cost)


@when("the game checks the activated ability's properties")
def step_check_activated_ability_properties(game_state):
    """Rule 2.0.1a: Check the ability's properties."""
    game_state.ability_has_cost = game_state.ability.has_property("cost")
    game_state.ability_has_type = game_state.ability.has_property("type")


@then(
    parsers.parse(
        'the activated ability should have a "cost" property equal to {expected_cost:d}'
    )
)
def step_ability_has_cost_equal(game_state, expected_cost):
    """Rule 2.0.1a: Activated ability has the cost property."""
    assert game_state.ability.has_property("cost"), (
        "Activated ability should have a 'cost' property"
    )
    assert game_state.ability.cost == expected_cost, (
        f"Expected cost {expected_cost}, got {game_state.ability.cost}"
    )


@then('the activated ability should have a "type" property')
def step_ability_has_type_property(game_state):
    """Rule 2.0.1a: Activated ability has the type property."""
    assert game_state.ability.has_property("type"), (
        "Activated ability should have a 'type' property"
    )


# ---------------------------------------------------------------------------
# Scenario: Card properties come from the card definition
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_0_general.feature",
    "Card properties come from the card definition",
)
def test_card_properties_come_from_card_definition():
    """Rule 2.0.2: Properties determined by true text of the card."""
    pass


@given(
    parsers.parse(
        "a card template defined with power {power:d} cost {cost:d} defense {defense:d}"
    )
)
def step_card_template_defined_with(game_state, power, cost, defense):
    """Rule 2.0.2: Create a card with defined properties."""
    game_state.card = CardPropertyStub(
        name="Test Card",
        power=power,
        defense=defense,
        cost=cost,
    )


@when("the game reads the card's properties")
def step_game_reads_card_properties(game_state):
    """Rule 2.0.2: Read the card's properties as defined."""
    game_state.read_power = game_state.card.base_power
    game_state.read_cost = game_state.card._base_cost
    game_state.read_defense = game_state.card.base_defense


@then(parsers.parse("the card power should be {expected:d}"))
def step_card_power_should_be(game_state, expected):
    """Rule 2.0.2: Card power matches the defined value."""
    assert game_state.read_power == expected, (
        f"Expected power {expected}, got {game_state.read_power}"
    )


@then(parsers.parse("the card cost should be {expected:d}"))
def step_card_cost_should_be(game_state, expected):
    """Rule 2.0.2: Card cost matches the defined value."""
    assert game_state.read_cost == expected, (
        f"Expected cost {expected}, got {game_state.read_cost}"
    )


@then(parsers.parse("the card defense should be {expected:d}"))
def step_card_defense_should_be(game_state, expected):
    """Rule 2.0.2: Card defense matches the defined value."""
    assert game_state.read_defense == expected, (
        f"Expected defense {expected}, got {game_state.read_defense}"
    )


# ---------------------------------------------------------------------------
# Scenario: Numeric properties have numeric values that can be read
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_0_general.feature",
    "Numeric properties have numeric values that can be read",
)
def test_numeric_properties_have_numeric_values():
    """Rule 2.0.3: Numeric properties have numeric values."""
    pass


@given(parsers.parse('a card named "{name}" with power {power:d}'))
def step_card_named_with_power(game_state, name, power):
    """Rule 2.0.3: Create a card with a specific power value."""
    game_state.card = CardPropertyStub(
        name=name,
        power=power,
        defense=3,
        cost=2,
    )


@when("the game reads the card's numeric properties")
def step_game_reads_numeric_properties(game_state):
    """Rule 2.0.3: Read numeric property values."""
    game_state.power_value = game_state.card.base_power
    game_state.power_is_numeric = isinstance(game_state.power_value, int)


@then(parsers.parse("the power property value should be {expected:d}"))
def step_power_property_value(game_state, expected):
    """Rule 2.0.3: Power property returns a numeric value."""
    assert game_state.power_value == expected, (
        f"Expected power {expected}, got {game_state.power_value}"
    )


@then("power should be classified as a numeric property")
def step_power_is_numeric_property(game_state):
    """Rule 2.0.3: Power is a numeric property."""
    assert game_state.power_is_numeric, "Power should be an integer (numeric property)"


# ---------------------------------------------------------------------------
# Scenario: Effect modifies card power without changing base power
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_0_general.feature",
    "Effect modifies card power without changing base power",
)
def test_effect_modifies_power_not_base():
    """Rule 2.0.3a: Effects modifying numeric properties do not change the base value."""
    pass


@given(parsers.parse("a card with base power {power:d}"))
def step_card_with_base_power(game_state, power):
    """Rule 2.0.3a: Create a card with a specific base power."""
    game_state.card = CardPropertyStub(
        name="Test Card",
        power=power,
        defense=3,
        cost=1,
    )


@given(parsers.parse('an effect that gives the card "+{amount:d} power"'))
def step_effect_gives_power(game_state, amount):
    """Rule 2.0.3a: An effect that gives non-base power."""
    game_state.effect_amount = amount


@when("the non-base power effect is applied to the card")
def step_non_base_power_effect_applied(game_state):
    """Rule 2.0.3a: Apply the effect to modify non-base power."""
    game_state.modification = game_state.card.apply_non_base_power_modifier(
        game_state.effect_amount
    )


@then(parsers.parse("the card's effective power should be {expected:d}"))
def step_effective_power_should_be(game_state, expected):
    """Rule 2.0.3a: Check the modified (effective) power value."""
    assert game_state.card.effective_power == expected, (
        f"Expected effective power {expected}, got {game_state.card.effective_power}"
    )


@then(parsers.parse("the card's base power should still be {expected:d}"))
def step_base_power_still_be(game_state, expected):
    """Rule 2.0.3a: Base power should remain unchanged."""
    assert game_state.card.base_power == expected, (
        f"Expected base power {expected}, got {game_state.card.base_power}"
    )


# ---------------------------------------------------------------------------
# Scenario: Effect using gain keyword modifies non-base power value
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_0_general.feature",
    "Effect using gain keyword modifies non-base power value",
)
def test_gain_effect_modifies_non_base_power():
    """Rule 2.0.3a: 'gain' keyword modifies non-base value."""
    pass


@given(parsers.parse('an effect that makes the card "gain {amount:d} power"'))
def step_effect_makes_card_gain_power(game_state, amount):
    """Rule 2.0.3a: Set up a gain effect."""
    game_state.effect_amount = amount


@when("the gain power effect is applied to the card")
def step_gain_power_effect_applied(game_state):
    """Rule 2.0.3a: Apply the gain power effect to modify non-base power."""
    game_state.modification = game_state.card.apply_non_base_power_modifier(
        game_state.effect_amount
    )


# ---------------------------------------------------------------------------
# Scenario: Doubling base power is not considered gaining power
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_0_general.feature",
    "Doubling base power is not considered gaining power",
)
def test_doubling_base_power_not_gaining():
    """Rule 2.0.3b: Base power modification is NOT considered gaining power.
    Example: Big Bully doubles base power; this is not 'gaining power'."""
    pass


@given(parsers.parse("an effect that doubles the card's base power"))
def step_effect_doubles_base_power(game_state):
    """Rule 2.0.3b: An effect that doubles base power."""
    game_state.effect_type = "base_double"


@when("the base-doubling effect is applied")
def step_base_doubling_effect_applied(game_state):
    """Rule 2.0.3b: Apply the base-doubling effect."""
    game_state.modification = game_state.card.double_base_power()


@then(parsers.parse("the card's base power should be {expected:d}"))
def step_card_base_power_should_be(game_state, expected):
    """Rule 2.0.3b: Base power was doubled."""
    assert game_state.card.base_power == expected, (
        f"Expected base power {expected}, got {game_state.card.base_power}"
    )


@then('the modification should not be classified as "gaining power"')
def step_modification_not_classified_as_gaining(game_state):
    """Rule 2.0.3b: Base modification is NOT classified as 'gaining power'."""
    assert not game_state.modification.is_classified_as_gaining(), (
        "Doubling base power should NOT be classified as 'gaining power' "
        "for effects that reference gaining/losing power (Rule 2.0.3b)"
    )


# ---------------------------------------------------------------------------
# Scenario: Non-base power increase is considered gaining power
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_0_general.feature",
    "Non-base power increase is considered gaining power",
)
def test_non_base_increase_is_gaining():
    """Rule 2.0.3b: Non-base modifications ARE considered gaining/losing.
    Example: Korshem checks if a hero's card has 'gained {p}'."""
    pass


@given(
    parsers.parse("an effect that increases the card's non-base power by {amount:d}")
)
def step_effect_increases_non_base_power(game_state, amount):
    """Rule 2.0.3b: An effect that increases non-base power."""
    game_state.effect_amount = amount


@when("the non-base power increase effect is applied")
def step_non_base_power_increase_applied(game_state):
    """Rule 2.0.3b: Apply the non-base power increase effect."""
    game_state.modification = game_state.card.apply_non_base_power_modifier(
        game_state.effect_amount
    )


@then('the modification should be classified as "gaining power"')
def step_modification_classified_as_gaining(game_state):
    """Rule 2.0.3b: Non-base modification IS classified as 'gaining power'."""
    assert game_state.modification.is_classified_as_gaining(), (
        "Non-base power increase should be classified as 'gaining power' "
        "for effects that reference gaining/losing power (Rule 2.0.3b)"
    )


# ---------------------------------------------------------------------------
# Scenario: Numeric property cannot go below zero
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_0_general.feature",
    "Numeric property cannot go below zero",
)
def test_numeric_property_cannot_be_negative():
    """Rule 2.0.3c: Numeric properties capped at zero; cannot be negative."""
    pass


@given(parsers.parse("an effect that reduces the card's power by {amount:d}"))
def step_effect_reduces_power_by(game_state, amount):
    """Rule 2.0.3c: Set up an effect that reduces power."""
    game_state.effect_amount = -amount  # Negative modifier


@when("the power reduction effect is applied")
def step_power_reduction_effect_applied(game_state):
    """Rule 2.0.3c: Apply the power-reducing effect."""
    game_state.modification = game_state.card.apply_non_base_power_modifier(
        game_state.effect_amount
    )


@then("the card's effective power should not be negative")
def step_effective_power_not_negative(game_state):
    """Rule 2.0.3c: Power cannot be negative; it must be 0 or more."""
    assert game_state.card.effective_power >= 0, (
        f"Card's effective power should not be negative, "
        f"got {game_state.card.effective_power}"
    )


# ---------------------------------------------------------------------------
# Scenario: Effect reducing defense to negative is capped at zero
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_0_general.feature",
    "Effect reducing defense to negative is capped at zero",
)
def test_defense_cannot_be_negative():
    """Rule 2.0.3c: Defense capped at zero."""
    pass


@given(parsers.parse("a card with base defense {defense:d}"))
def step_card_with_base_defense(game_state, defense):
    """Rule 2.0.3c: Set up a card with a specific base defense."""
    game_state.card = CardPropertyStub(
        name="Defense Card",
        power=3,
        defense=defense,
        cost=1,
    )


@given(parsers.parse("an effect that reduces the card's defense by {amount:d}"))
def step_effect_reduces_defense_by(game_state, amount):
    """Rule 2.0.3c: Set up an effect that reduces defense beyond zero."""
    game_state.defense_effect_amount = -amount


@when("the defense reduction effect is applied")
def step_defense_reduction_effect_applied(game_state):
    """Rule 2.0.3c: Apply the defense-reducing effect."""
    game_state.card.apply_defense_modifier(game_state.defense_effect_amount)


@then(parsers.parse("the card's effective defense should be {expected:d}"))
def step_effective_defense_should_be(game_state, expected):
    """Rule 2.0.3c: Effective defense matches the expected value (0 minimum)."""
    assert game_state.card.effective_defense == expected, (
        f"Expected effective defense {expected}, got {game_state.card.effective_defense}"
    )


# ---------------------------------------------------------------------------
# Scenario: A power counter modifies card power without changing base power
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_0_general.feature",
    "A power counter modifies card power without changing base power",
)
def test_power_counter_modifies_not_base():
    """Rule 2.0.3d: +/-1 property counters modify effective value, not base."""
    pass


@given(parsers.parse('a "+1 power" counter is placed on the card'))
def step_plus_one_power_counter_placed(game_state):
    """Rule 2.0.3d: Place a +1 power counter on the card."""
    game_state.modification = game_state.card.add_power_counter(1)


@when("the game calculates the card's power")
def step_game_calculates_power(game_state):
    """Rule 2.0.3d: Calculate the card's effective power including counters."""
    game_state.calculated_power = game_state.card.effective_power


# Reuse 'the card's effective power should be {expected}' step
# Reuse 'the card's base power should still be {expected}' step


# ---------------------------------------------------------------------------
# Scenario: A minus-power counter modifies card power without changing base
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_0_general.feature",
    "A minus-power counter modifies card power without changing base",
)
def test_minus_power_counter_modifies_not_base():
    """Rule 2.0.3d: -1 property counter modifies effective power, not base."""
    pass


@given(parsers.parse('a "-1 power" counter is placed on the card'))
def step_minus_one_power_counter_placed(game_state):
    """Rule 2.0.3d: Place a -1 power counter on the card."""
    game_state.modification = game_state.card.add_power_counter(-1)


# Reuse 'the game calculates the card's power' step from above
# Reuse 'the card's effective power should be {expected}' step
# Reuse 'the card's base power should still be {expected}' step


# ---------------------------------------------------------------------------
# Scenario: Card gains a property it did not previously have
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_0_general.feature",
    "Card gains a property it did not previously have",
)
def test_card_gains_new_property():
    """Rule 2.0.4: An object 'gains' a property if it didn't have it before."""
    pass


@given(parsers.parse('a card that does not have the "{prop}" property'))
def step_card_without_property(game_state, prop):
    """Rule 2.0.4: Set up a card without the specified property."""
    game_state.card = CardPropertyStub(
        name="Test Card",
        power=3,
        defense=2,
        cost=1,
        keywords=[],  # No keywords/boolean properties
    )
    assert not game_state.card.has_boolean_property(prop), (
        f"Card should not have '{prop}' property initially"
    )
    game_state.target_prop = prop


@when(parsers.parse('an effect grants the card the "{prop}" property'))
def step_effect_grants_property(game_state, prop):
    """Rule 2.0.4: Apply an effect that grants a property."""
    game_state.gain_loss_result = game_state.card.grant_boolean_property(prop)


@then(parsers.parse('the card should be considered to have "gained {prop}"'))
def step_card_gained_property(game_state, prop):
    """Rule 2.0.4: Card should have gained the property."""
    assert game_state.gain_loss_result.was_gained, (
        f"Card should have 'gained' the '{prop}' property "
        f"(did not have it before, now does)"
    )


@then(parsers.parse('the card now has the "{prop}" property'))
def step_card_now_has_property(game_state, prop):
    """Rule 2.0.4: Card currently has the property."""
    assert game_state.card.has_boolean_property(prop), (
        f"Card should now have the '{prop}' property"
    )


# ---------------------------------------------------------------------------
# Scenario: Card loses a property it previously had
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_0_general.feature",
    "Card loses a property it previously had",
)
def test_card_loses_existing_property():
    """Rule 2.0.4: An object 'loses' a property if it had it and no longer does."""
    pass


@given(parsers.parse('a card that has the "{prop}" property'))
def step_card_with_property(game_state, prop):
    """Rule 2.0.4: Set up a card that has the specified property."""
    game_state.card = CardPropertyStub(
        name="Test Card",
        power=3,
        defense=2,
        cost=1,
        keywords=[prop],  # Card has the property
    )
    game_state.target_prop = prop


@when(parsers.parse('an effect removes the card\'s "{prop}" property'))
def step_effect_removes_property(game_state, prop):
    """Rule 2.0.4: Apply an effect that removes a property."""
    game_state.gain_loss_result = game_state.card.remove_boolean_property(prop)


@then(parsers.parse('the card should be considered to have "lost {prop}"'))
def step_card_lost_property(game_state, prop):
    """Rule 2.0.4: Card should have lost the property."""
    assert game_state.gain_loss_result.was_lost, (
        f"Card should have 'lost' the '{prop}' property (had it before, no longer does)"
    )


@then(parsers.parse('the card no longer has the "{prop}" property'))
def step_card_no_longer_has_property(game_state, prop):
    """Rule 2.0.4: Card no longer has the property."""
    assert not game_state.card.has_boolean_property(prop), (
        f"Card should no longer have the '{prop}' property"
    )


# ---------------------------------------------------------------------------
# Scenario: Gaining a property is not the same as increasing property value
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_0_general.feature",
    "Gaining a property is not the same as increasing property value",
)
def test_gaining_property_not_same_as_increasing_value():
    """Rule 2.0.4: Gaining/losing a property is NOT increasing/decreasing its value."""
    pass


# Reuse 'a card that does not have the "{prop}" property' step from above


@then(parsers.parse('the card should have "gained {prop}"'))
def step_card_has_gained_property(game_state, prop):
    """Rule 2.0.4: Card gained the property."""
    assert game_state.gain_loss_result.was_gained, (
        f"Card should have 'gained' the '{prop}' property"
    )


@then(parsers.parse('this should not be classified as "increasing" the {prop} value'))
def step_not_classified_as_increasing(game_state, prop):
    """Rule 2.0.4: Gaining a property is not classified as 'increasing' its value."""
    assert not game_state.gain_loss_result.is_value_increase, (
        f"Gaining the '{prop}' property should NOT be classified as "
        f"'increasing' the property value (Rule 2.0.4)"
    )


# ---------------------------------------------------------------------------
# Scenario: The source of a property is the card that has it
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_0_general.feature",
    "The source of a property is the card that has it",
)
def test_source_of_property_is_card():
    """Rule 2.0.5: The source of a property is the object that has it."""
    pass


@given(parsers.parse('a card named "{name}" with power {power:d}'))
def step_card_named_with_power_2_0_5(game_state, name, power):
    """Rule 2.0.5: Set up a named card with power."""
    game_state.card = CardPropertyStub(
        name=name,
        power=power,
        defense=3,
        cost=2,
    )
    game_state.card_name = name


@when("the game identifies the source of the power property")
def step_identify_property_source(game_state):
    """Rule 2.0.5: Identify which object is the source of power."""
    game_state.property_source = game_state.card.get_property_source("power")


@then(
    parsers.parse('the source of the power property should be the "{source_name}" card')
)
def step_property_source_is_card(game_state, source_name):
    """Rule 2.0.5: The source of the property is the named card."""
    assert game_state.property_source is not None, "Property source should not be None"
    assert game_state.property_source.source_object_name == source_name, (
        f"Expected source to be '{source_name}', "
        f"got '{game_state.property_source.source_object_name}'"
    )
    assert game_state.property_source.property_name == "power", (
        f"Expected property name 'power', "
        f"got '{game_state.property_source.property_name}'"
    )
