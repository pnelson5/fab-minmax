"""
Step definitions for Section 2.2: Cost
Reference: Flesh and Blood Comprehensive Rules Section 2.2

This module implements behavioral tests for the cost property of cards and abilities
in Flesh and Blood.

Rule 2.2.1: Cost is a numeric property of a card or ability, which determines the
            starting resource asset-cost to play the card or activate the ability.

Rule 2.2.2: The printed cost of a card is typically expressed within a resource point
            symbol located in the top right corner of the card. The printed cost defines
            the base cost of a card. If a card does not have a printed cost, it does not
            have the cost property (0 is a valid printed cost).

Rule 2.2.2a: If the printed value is expressed as two or more undefined symbols and/or
             numeric values, they are additive for determining the base cost of a card.
             Example: Spark of Genius has the cost "XX," which determines base cost X+X.

Rule 2.2.3: The printed cost of an activated ability is expressed as {r} symbols as part
            of the description. The number of {r} symbols dictates the printed cost.
            If there are no resource symbols, then the printed cost is 0.

Rule 2.2.4: The cost property of an object cannot be modified.

Rule 2.2.4a: An effect that increases or reduces the cost of an object does not modify
             the cost property of that object. Effects that modify cost are only applied
             as part of the process for playing or activating that object.

Rule 2.2.4b: An effect that refers to the cost of an object refers to the unmodified
             cost property. An effect that refers to the payment refers to the modified
             cost when it was paid to play/activate and put the object on the stack.

Rule 2.2.5: The visual expression in {r} symbols and the numerical expression of cost
            are functionally identical.

Engine Features Needed for Section 2.2:
- [ ] `CardInstance.has_cost_property` property: False for no printed cost (Rule 2.2.2)
- [ ] `CardInstance.base_cost` property returning the unmodified printed cost (Rule 2.2.2)
- [ ] `CardInstance.cost` property returning the unmodified cost property (Rule 2.2.4b)
- [ ] `CardInstance.effective_play_cost` with modifications applied during play (Rule 2.2.4a)
- [ ] Support for variable cost formulas (XX, X+1, etc.) (Rule 2.2.2a)
- [ ] `ActivatedAbility.base_cost` counting {r} symbols in the ability description (Rule 2.2.3)
- [ ] `CostProperty.is_immutable = True` - cost property cannot be modified (Rule 2.2.4)
- [ ] Cost-reference effects use unmodified cost property (Rule 2.2.4b)
- [ ] Payment-reference effects use modified play cost (Rule 2.2.4b)
- [ ] {r} symbol and numeric cost treated as functionally identical (Rule 2.2.5)
"""

import pytest
from pytest_bdd import scenario, given, when, then, parsers
from dataclasses import dataclass, field
from typing import Optional, List


# ---------------------------------------------------------------------------
# Stub classes for testing Section 2.2 rules
# ---------------------------------------------------------------------------


@dataclass
class CostCheckResultStub:
    """
    Result of checking a card's cost property.

    Rule 2.2.1: Cost is a numeric property determining starting resource asset-cost.
    Rule 2.2.2: Printed cost defines the base cost; no printed cost = no cost property.
    """

    has_cost_property: bool
    cost_value: Optional[int]  # None if no cost property
    is_numeric: bool = True


@dataclass
class AbilityCostStub:
    """
    Stub for an activated ability with a cost expressed as {r} symbols.

    Rule 2.2.3: Activated ability cost = count of {r} symbols in description.
    """

    resource_symbol_count: int  # Number of {r} symbols

    @property
    def base_cost(self) -> int:
        """Rule 2.2.3: Base cost = number of {r} symbols (0 if none)."""
        return self.resource_symbol_count

    @property
    def printed_cost(self) -> int:
        """Rule 2.2.3: Printed cost = base resource cost for the ability."""
        return self.resource_symbol_count


@dataclass
class VariableCostFormulaStub:
    """
    Stub for a card with a variable cost formula (like XX or X+1).

    Rule 2.2.2a: Multiple undefined symbols/values are additive.
    """

    formula: str  # e.g. "XX" or "X+1"
    undefined_symbol_count: int  # Number of undefined X/Y/Z symbols
    fixed_addition: int = 0  # Fixed numeric value added to formula

    def evaluate_base_cost(self, x_value: int) -> int:
        """Rule 2.2.2a: Evaluate additive cost given a value for X."""
        # For formula "XX": base cost = X + X = 2 * x_value
        # For formula "X+1": base cost = X + 1
        return (self.undefined_symbol_count * x_value) + self.fixed_addition

    @property
    def is_additive_formula(self) -> bool:
        """Rule 2.2.2a: Multiple undefined symbols are additive."""
        return self.undefined_symbol_count > 1 or self.fixed_addition > 0


@dataclass
class CostCardStub:
    """
    Stub for a card with cost property.

    Models what the engine must implement for Section 2.2.
    Engine Features Needed:
    - [ ] CardInstance.base_cost: unmodified printed cost (Rule 2.2.2)
    - [ ] CardInstance.has_cost_property: False if no printed cost (Rule 2.2.2)
    - [ ] CardInstance.cost: unmodified cost for effect references (Rule 2.2.4b)
    - [ ] CardInstance.effective_play_cost: modified cost during playing (Rule 2.2.4a)
    """

    name: str = "Test Card"
    printed_cost: Optional[int] = None  # None if card has no cost property
    cost_reduction: int = 0  # Applied only during playing (Rule 2.2.4a)
    is_being_played: bool = False  # Track whether in play process (Rule 2.2.4a)

    @property
    def has_cost_property(self) -> bool:
        """Rule 2.2.2: Card has cost property only if there is a printed cost."""
        return self.printed_cost is not None

    @property
    def base_cost(self) -> Optional[int]:
        """Rule 2.2.2: Base cost is the printed cost."""
        return self.printed_cost

    @property
    def cost(self) -> Optional[int]:
        """
        Rule 2.2.4b: Cost property is always the unmodified printed cost.

        Effects referring to 'cost' use this unmodified value.
        """
        return self.printed_cost

    @property
    def effective_play_cost(self) -> Optional[int]:
        """
        Rule 2.2.4a: During playing, effects modify the effective play cost.

        This is NOT the cost property — it's the modified calculation
        only applicable during the play process.
        """
        if self.printed_cost is None:
            return None
        return max(0, self.printed_cost - self.cost_reduction)

    def check_cost(self) -> CostCheckResultStub:
        """Rule 2.2.1/2.2.2: Get the cost property of this card."""
        return CostCheckResultStub(
            has_cost_property=self.has_cost_property,
            cost_value=self.printed_cost,
            is_numeric=True,
        )

    def get_starting_resource_asset_cost(self) -> Optional[int]:
        """Rule 2.2.1: The starting resource asset-cost determined by the cost property."""
        return self.printed_cost

    def attempt_modify_cost_property(self, amount: int) -> bool:
        """
        Rule 2.2.4: Attempt to directly modify the cost property.

        Always returns False because the cost property is immutable.
        Engine Feature Needed: Cost property must be immutable.
        """
        # Cost property cannot be modified (Rule 2.2.4)
        return False  # Modification always fails

    def apply_cost_reduction_during_play(self, reduction: int):
        """
        Rule 2.2.4a: Apply a cost reduction effect (only for the play process).

        This does NOT modify the cost property — it modifies only the
        effective play cost calculation.
        """
        self.cost_reduction = reduction


@dataclass
class CostModificationAttemptResultStub:
    """
    Result of attempting to modify the cost property.

    Rule 2.2.4: The cost property cannot be modified.
    """

    modification_applied: bool  # Always False for cost property
    original_cost: int
    current_cost: int  # Should equal original_cost since modification fails


@dataclass
class CostReferenceResultStub:
    """
    Result of an effect referring to the cost of a card.

    Rule 2.2.4b: Effects referring to 'cost' use unmodified cost property.
                 Effects referring to 'payment' use modified cost at stack time.
    """

    referenced_cost: int  # The value the effect sees
    is_unmodified: bool  # True if effect used unmodified cost (Rule 2.2.4b)


@dataclass
class PaymentRecordStub:
    """
    Record of the payment amount when a card is played.

    Rule 2.2.4b: Payment refers to the modified cost when played.
    """

    payment_amount: int  # The modified cost actually paid
    base_cost: int  # The unmodified cost property


@dataclass
class CostSearchResultStub:
    """
    Result of searching for cards matching a cost value.

    Rule 2.2.5: {r} symbols and numeric cost are functionally identical.
    """

    found_cards: List[str]  # Names of matching cards


@dataclass
class NumericCostEquivalentStub:
    """
    Result of interpreting resource symbols as numeric cost.

    Rule 2.2.5: Visual {r} expression and numeric cost expression are equivalent.
    """

    resource_symbol_count: int
    numeric_equivalent: int  # Same as resource_symbol_count (Rule 2.2.5)


# ---------------------------------------------------------------------------
# Scenario: Cost is a numeric property of a card
# Tests Rule 2.2.1 - Cost is a numeric property
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_2_cost.feature",
    "Cost is a numeric property of a card",
)
def test_cost_is_numeric_property_of_card():
    """Rule 2.2.1: Cost is a numeric property of a card."""
    pass


@given(
    parsers.parse("a card is created with a printed cost of {cost_value:d}"),
    target_fixture="cost_card",
)
def step_given_card_with_printed_cost(cost_value):
    """Rule 2.2.1/2.2.2: Create a card with a specific printed cost."""
    return CostCardStub(name=f"Card with Cost {cost_value}", printed_cost=cost_value)


@when(
    parsers.parse(
        "the engine checks the cost property of the cost {cost_value:d} card"
    ),
    target_fixture="cost_check_result",
)
def step_when_check_cost_property(cost_card, cost_value):
    """Rule 2.2.1: Check the cost property of the card."""
    return cost_card.check_cost()


@then(parsers.parse("the cost {cost_value:d} card should have the cost property"))
def step_then_card_has_cost_property(cost_check_result, cost_value):
    """Rule 2.2.2: Card with printed cost has the cost property."""
    assert cost_check_result.has_cost_property, (
        f"Card with printed cost {cost_value} should have the cost property"
    )


@then(
    parsers.parse(
        "the cost of the cost {cost_value:d} card should be {expected_cost:d}"
    )
)
def step_then_cost_value_is(cost_check_result, cost_value, expected_cost):
    """Rule 2.2.1: Cost property value matches the printed cost."""
    assert cost_check_result.cost_value == expected_cost, (
        f"Expected cost {expected_cost}, got {cost_check_result.cost_value}"
    )


# ---------------------------------------------------------------------------
# Scenario: Cost determines starting resource asset-cost to play the card
# Tests Rule 2.2.1 - Cost is the starting resource asset-cost
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_2_cost.feature",
    "Cost determines starting resource asset-cost to play the card",
)
def test_cost_determines_starting_resource_asset_cost():
    """Rule 2.2.1: Cost determines the starting resource asset-cost."""
    pass


@when(
    "the engine determines the starting resource asset-cost for the cost 2 card",
    target_fixture="starting_cost_result",
)
def step_when_determine_starting_cost(cost_card):
    """Rule 2.2.1: Determine the starting resource asset-cost."""
    return cost_card.get_starting_resource_asset_cost()


@then(
    parsers.parse(
        "the starting resource asset-cost for the cost 2 card should be {expected:d}"
    )
)
def step_then_starting_cost_is(starting_cost_result, expected):
    """Rule 2.2.1: Starting resource asset-cost equals the cost property."""
    assert starting_cost_result == expected, (
        f"Expected starting resource asset-cost {expected}, got {starting_cost_result}"
    )


# ---------------------------------------------------------------------------
# Scenario: Printed cost defines the base cost of a card
# Tests Rule 2.2.2 - Printed cost = base cost
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_2_cost.feature",
    "Printed cost defines the base cost of a card",
)
def test_printed_cost_defines_base_cost():
    """Rule 2.2.2: The printed cost defines the base cost of a card."""
    pass


@when(
    "the engine checks the base cost of the cost 4 card",
    target_fixture="base_cost_result",
)
def step_when_check_base_cost_of_cost_4(cost_card):
    """Rule 2.2.2: Check the base cost (= printed cost)."""
    return cost_card.base_cost


@then(parsers.parse("the base cost of the cost 4 card should be {expected:d}"))
def step_then_base_cost_is(base_cost_result, expected):
    """Rule 2.2.2: Base cost equals printed cost."""
    assert base_cost_result == expected, (
        f"Expected base cost {expected}, got {base_cost_result}"
    )


# ---------------------------------------------------------------------------
# Scenario: Zero is a valid printed cost
# Tests Rule 2.2.2 - Zero is a valid printed cost
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_2_cost.feature",
    "Zero is a valid printed cost",
)
def test_zero_is_valid_printed_cost():
    """Rule 2.2.2: Zero is a valid printed cost; card still has the cost property."""
    pass


@given(
    "a card is created with a printed cost of 0",
    target_fixture="cost_0_card",
)
def step_given_card_with_cost_0():
    """Rule 2.2.2: Create a card with printed cost 0."""
    return CostCardStub(name="Free Card", printed_cost=0)


@when(
    "the engine checks the cost property of the cost 0 card",
    target_fixture="cost_0_check_result",
)
def step_when_check_cost_0_card(cost_0_card):
    """Rule 2.2.2: Check cost property of zero-cost card."""
    return cost_0_card.check_cost()


@then("the cost 0 card should have the cost property")
def step_then_cost_0_has_property(cost_0_check_result):
    """Rule 2.2.2: Card with printed cost 0 still has the cost property."""
    assert cost_0_check_result.has_cost_property, (
        "Card with printed cost 0 should still have the cost property (0 is a valid cost)"
    )


@then("the cost of the cost 0 card should be 0")
def step_then_cost_0_value_is_zero(cost_0_check_result):
    """Rule 2.2.2: Card with printed cost 0 has cost value 0."""
    assert cost_0_check_result.cost_value == 0, (
        f"Expected cost 0, got {cost_0_check_result.cost_value}"
    )


# ---------------------------------------------------------------------------
# Scenario: Card without a printed cost lacks the cost property
# Tests Rule 2.2.2 - Missing printed cost = no cost property
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_2_cost.feature",
    "Card without a printed cost lacks the cost property",
)
def test_card_without_printed_cost_lacks_cost_property():
    """Rule 2.2.2: Card without a printed cost does not have the cost property."""
    pass


@given(
    "a card is created with no printed cost",
    target_fixture="no_cost_card",
)
def step_given_no_cost_card():
    """Rule 2.2.2: Create a card without a printed cost (no cost property)."""
    return CostCardStub(name="No Cost Card", printed_cost=None)


@when(
    "the engine checks the cost property of the no-cost card",
    target_fixture="no_cost_check_result",
)
def step_when_check_no_cost_card(no_cost_card):
    """Rule 2.2.2: Check cost property of card with no printed cost."""
    return no_cost_card.check_cost()


@then("the no-cost card should not have the cost property")
def step_then_no_cost_card_lacks_property(no_cost_check_result):
    """Rule 2.2.2: Card without printed cost does not have cost property."""
    assert not no_cost_check_result.has_cost_property, (
        "Card without a printed cost should not have the cost property"
    )


# ---------------------------------------------------------------------------
# Scenario: Card with two X symbols has additive base cost
# Tests Rule 2.2.2a - XX cost formula is additive
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_2_cost.feature",
    "Card with two X symbols has additive base cost",
)
def test_card_with_xx_has_additive_base_cost():
    """Rule 2.2.2a: Card with two undefined X cost symbols has additive base cost."""
    pass


@given(
    'a card named "Spark of Genius" is created with two undefined X cost symbols',
    target_fixture="spark_of_genius_card",
)
def step_given_spark_of_genius():
    """Rule 2.2.2a: Create a card with XX cost (Spark of Genius example)."""
    return VariableCostFormulaStub(
        formula="XX",
        undefined_symbol_count=2,
        fixed_addition=0,
    )


@when(
    "the engine determines the base cost of the Spark of Genius card",
    target_fixture="spark_of_genius_cost_result",
)
def step_when_determine_spark_base_cost(spark_of_genius_card):
    """Rule 2.2.2a: Determine the additive base cost formula."""
    return spark_of_genius_card


@then("the base cost formula of the Spark of Genius card should be additive")
def step_then_spark_cost_is_additive(spark_of_genius_cost_result):
    """Rule 2.2.2a: Two X symbols make the cost additive."""
    assert spark_of_genius_cost_result.is_additive_formula, (
        "Card with two X symbols should have an additive cost formula (Rule 2.2.2a)"
    )


@then(
    parsers.parse(
        "the base cost of the Spark of Genius card with X equals {x_value:d} should be {expected:d}"
    )
)
def step_then_spark_base_cost_evaluated(spark_of_genius_cost_result, x_value, expected):
    """Rule 2.2.2a: XX with X=3 evaluates to 3+3=6."""
    evaluated = spark_of_genius_cost_result.evaluate_base_cost(x_value)
    assert evaluated == expected, (
        f"With X={x_value}, XX should evaluate to {expected}, got {evaluated}"
    )


# ---------------------------------------------------------------------------
# Scenario: Card with mixed numeric and X cost symbols has additive base cost
# Tests Rule 2.2.2a - Mixed formulas are additive
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_2_cost.feature",
    "Card with mixed numeric and X cost symbols has additive base cost",
)
def test_card_with_x_plus_1_has_additive_cost():
    """Rule 2.2.2a: Card with X+1 cost uses additive formula."""
    pass


@given(
    "a card is created with a cost of X plus 1",
    target_fixture="x_plus_1_card",
)
def step_given_x_plus_1_card():
    """Rule 2.2.2a: Create a card with mixed X+1 cost formula."""
    return VariableCostFormulaStub(
        formula="X+1",
        undefined_symbol_count=1,
        fixed_addition=1,
    )


@when(
    "the engine determines the base cost of the mixed cost card",
    target_fixture="mixed_cost_result",
)
def step_when_determine_mixed_cost(x_plus_1_card):
    """Rule 2.2.2a: Determine the additive base cost formula."""
    return x_plus_1_card


@then(
    parsers.parse(
        "the base cost of the mixed cost card with X equals {x_value:d} should be {expected:d}"
    )
)
def step_then_mixed_cost_evaluated(mixed_cost_result, x_value, expected):
    """Rule 2.2.2a: X+1 with X=2 evaluates to 3."""
    evaluated = mixed_cost_result.evaluate_base_cost(x_value)
    assert evaluated == expected, (
        f"With X={x_value}, X+1 should evaluate to {expected}, got {evaluated}"
    )


# ---------------------------------------------------------------------------
# Scenario: Activated ability with two resource symbols has base cost of 2
# Tests Rule 2.2.3 - {r}{r} = base cost 2
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_2_cost.feature",
    "Activated ability with two resource symbols has base cost of 2",
)
def test_activated_ability_two_resource_symbols_base_cost_2():
    """Rule 2.2.3: Two {r} symbols in ability description = base cost 2."""
    pass


@given(
    "an activated ability is created with 2 resource symbols in its cost",
    target_fixture="two_resource_ability",
)
def step_given_ability_with_2_resource_symbols():
    """Rule 2.2.3: Create an activated ability with 2 {r} symbols."""
    return AbilityCostStub(resource_symbol_count=2)


@when(
    "the engine checks the base cost of the 2-resource-symbol ability",
    target_fixture="two_resource_ability_cost",
)
def step_when_check_two_resource_ability_cost(two_resource_ability):
    """Rule 2.2.3: Get the base cost of the activated ability."""
    return two_resource_ability.base_cost


@then(
    parsers.parse(
        "the base cost of the 2-resource-symbol ability should be {expected:d}"
    )
)
def step_then_two_resource_ability_cost_is(two_resource_ability_cost, expected):
    """Rule 2.2.3: Two resource symbols means base cost equals 2."""
    assert two_resource_ability_cost == expected, (
        f"Expected ability base cost {expected}, got {two_resource_ability_cost}"
    )


# ---------------------------------------------------------------------------
# Scenario: Activated ability with no resource symbols has base cost of 0
# Tests Rule 2.2.3 - No resource symbols = base cost 0
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_2_cost.feature",
    "Activated ability with no resource symbols has base cost of 0",
)
def test_activated_ability_no_resource_symbols_base_cost_0():
    """Rule 2.2.3: No {r} symbols in ability description = base cost 0."""
    pass


@given(
    "an activated ability is created with no resource symbols in its cost",
    target_fixture="zero_resource_ability",
)
def step_given_ability_with_no_resource_symbols():
    """Rule 2.2.3: Create an activated ability with no {r} symbols."""
    return AbilityCostStub(resource_symbol_count=0)


@when(
    "the engine checks the base cost of the zero-resource ability",
    target_fixture="zero_resource_ability_cost",
)
def step_when_check_zero_resource_ability_cost(zero_resource_ability):
    """Rule 2.2.3: Get the base cost of the zero-resource ability."""
    return zero_resource_ability.base_cost


@then(
    parsers.parse("the base cost of the zero-resource ability should be {expected:d}")
)
def step_then_zero_resource_ability_cost_is(zero_resource_ability_cost, expected):
    """Rule 2.2.3: No resource symbols means base cost is 0."""
    assert zero_resource_ability_cost == expected, (
        f"Expected ability base cost {expected}, got {zero_resource_ability_cost}"
    )


# ---------------------------------------------------------------------------
# Scenario: The number of resource symbols determines the ability printed cost
# Tests Rule 2.2.3 - {r} count = printed cost
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_2_cost.feature",
    "The number of resource symbols determines the ability printed cost",
)
def test_resource_symbol_count_is_printed_cost():
    """Rule 2.2.3: The number of {r} symbols dictates the printed cost."""
    pass


@given(
    "an activated ability is created with 3 resource symbols in its cost",
    target_fixture="three_resource_ability",
)
def step_given_ability_with_3_resource_symbols():
    """Rule 2.2.3: Create an activated ability with 3 {r} symbols."""
    return AbilityCostStub(resource_symbol_count=3)


@when(
    "the engine checks the printed cost of the 3-resource-symbol ability",
    target_fixture="three_resource_ability_printed_cost",
)
def step_when_check_printed_cost_of_3_resource(three_resource_ability):
    """Rule 2.2.3: Get the printed cost of the ability."""
    return three_resource_ability.printed_cost


@then(
    parsers.parse(
        "the printed cost of the 3-resource-symbol ability should be {expected:d}"
    )
)
def step_then_three_resource_printed_cost_is(
    three_resource_ability_printed_cost, expected
):
    """Rule 2.2.3: 3 resource symbols = printed cost of 3."""
    assert three_resource_ability_printed_cost == expected, (
        f"Expected printed cost {expected}, got {three_resource_ability_printed_cost}"
    )


# ---------------------------------------------------------------------------
# Scenario: The cost property of a card cannot be modified
# Tests Rule 2.2.4 - Cost property is immutable
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_2_cost.feature",
    "The cost property of a card cannot be modified",
)
def test_cost_property_cannot_be_modified():
    """Rule 2.2.4: The cost property of a card cannot be modified."""
    pass


@given(
    "a card is created with a base cost of 5",
    target_fixture="base_cost_5_card",
)
def step_given_card_with_base_cost_5():
    """Rule 2.2.4: Create a card with base cost 5."""
    return CostCardStub(name="Base Cost 5 Card", printed_cost=5)


@when(
    "an effect attempts to modify the cost property of the base-cost-5 card",
    target_fixture="modification_attempt_result",
)
def step_when_effect_attempts_to_modify_cost(base_cost_5_card):
    """Rule 2.2.4: Attempt to modify the cost property (should fail)."""
    modification_applied = base_cost_5_card.attempt_modify_cost_property(2)
    return CostModificationAttemptResultStub(
        modification_applied=modification_applied,
        original_cost=5,
        current_cost=base_cost_5_card.cost,
    )


@then(
    parsers.parse(
        "the cost property of the base-cost-5 card should remain unchanged at {expected:d}"
    )
)
def step_then_cost_property_unchanged(modification_attempt_result, expected):
    """Rule 2.2.4: Cost property remains unchanged after modification attempt."""
    assert not modification_attempt_result.modification_applied, (
        "Cost property modification should not be applied (Rule 2.2.4)"
    )
    assert modification_attempt_result.current_cost == expected, (
        f"Cost property should remain {expected}, got {modification_attempt_result.current_cost}"
    )


# ---------------------------------------------------------------------------
# Scenario: Cost reduction effect does not change the cost property
# Tests Rule 2.2.4a - Effects modify play cost not cost property
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_2_cost.feature",
    "Cost reduction effect does not change the cost property",
)
def test_cost_reduction_does_not_change_cost_property():
    """Rule 2.2.4a: Cost reduction affects play cost but not cost property."""
    pass


@given(
    "a card is created with a base cost of 3",
    target_fixture="cost_3_card",
)
def step_given_card_with_cost_3():
    """Rule 2.2.4a: Create a card with base cost 3."""
    return CostCardStub(name="Cost 3 Card", printed_cost=3)


@given(
    "a cost reduction effect of 1 is applied when playing the cost 3 card",
    target_fixture="cost_3_card",
)
def step_given_cost_reduction_applied_to_cost_3(cost_3_card):
    """Rule 2.2.4a: Apply a cost reduction effect of 1 to the card."""
    cost_3_card.apply_cost_reduction_during_play(1)
    return cost_3_card


@when(
    "the engine checks the cost property of the cost 3 card with reduction",
    target_fixture="cost_3_with_reduction_result",
)
def step_when_check_cost_property_of_reduced_card(cost_3_card):
    """Rule 2.2.4a: Check both the cost property and effective play cost."""
    return {
        "cost_property": cost_3_card.cost,
        "effective_play_cost": cost_3_card.effective_play_cost,
    }


@then("the cost property of the cost 3 card with reduction should still be 3")
def step_then_cost_property_still_3(cost_3_with_reduction_result):
    """Rule 2.2.4a: Cost property remains 3 even with reduction effect."""
    assert cost_3_with_reduction_result["cost_property"] == 3, (
        f"Cost property should remain 3, got {cost_3_with_reduction_result['cost_property']}"
    )


@then("the play cost of the cost 3 card with reduction should be 2")
def step_then_play_cost_is_2(cost_3_with_reduction_result):
    """Rule 2.2.4a: Effective play cost is 2 (3 - 1 reduction)."""
    assert cost_3_with_reduction_result["effective_play_cost"] == 2, (
        f"Effective play cost should be 2, got {cost_3_with_reduction_result['effective_play_cost']}"
    )


# ---------------------------------------------------------------------------
# Scenario: Cost reduction only applies during the playing process
# Tests Rule 2.2.4a - Modification only during playing
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_2_cost.feature",
    "Cost reduction only applies during the playing process",
)
def test_cost_reduction_only_applies_during_playing():
    """Rule 2.2.4a: Cost modifications only apply during playing/activating."""
    pass


@given(
    "a card is created with a base cost of 4",
    target_fixture="base_cost_4_card",
)
def step_given_card_with_base_cost_4():
    """Rule 2.2.4a: Create a card with base cost 4."""
    return CostCardStub(name="Base Cost 4 Card", printed_cost=4)


@given(
    "a cost reduction effect of 2 is registered for the base cost 4 card",
    target_fixture="base_cost_4_card",
)
def step_given_cost_reduction_registered_for_cost_4(base_cost_4_card):
    """Rule 2.2.4a: Register a cost reduction effect."""
    base_cost_4_card.apply_cost_reduction_during_play(2)
    return base_cost_4_card


@when(
    "the engine checks the cost property outside of the playing process",
    target_fixture="outside_playing_result",
)
def step_when_check_cost_outside_playing(base_cost_4_card):
    """Rule 2.2.4a: Check cost property when card is not being played."""
    return {
        "cost_property": base_cost_4_card.cost,
        "is_being_played": base_cost_4_card.is_being_played,
        "effective_play_cost": base_cost_4_card.effective_play_cost,
    }


@then("the cost property outside playing should be 4")
def step_then_cost_property_is_4_outside_playing(outside_playing_result):
    """Rule 2.2.4a: Cost property is always 4 regardless of play process."""
    assert outside_playing_result["cost_property"] == 4, (
        f"Cost property should be 4, got {outside_playing_result['cost_property']}"
    )


@then("the cost modification should only apply during playing")
def step_then_modification_only_during_playing(outside_playing_result):
    """Rule 2.2.4a: Cost modification applies only during the play process."""
    # The effective_play_cost includes the reduction, but the cost property doesn't
    assert (
        outside_playing_result["cost_property"]
        != outside_playing_result["effective_play_cost"]
    ), (
        "Effective play cost (2) should differ from cost property (4) when reduction is active"
    )


# ---------------------------------------------------------------------------
# Scenario: Effect referring to cost uses the unmodified cost property
# Tests Rule 2.2.4b - "Cost" effects use unmodified property
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_2_cost.feature",
    "Effect referring to cost uses the unmodified cost property",
)
def test_effect_referring_to_cost_uses_unmodified_cost():
    """Rule 2.2.4b: Effects referring to 'cost' use the unmodified cost property."""
    pass


@given(
    "a card is created with a base cost of 3 for cost-reference testing",
    target_fixture="cost_reference_card",
)
def step_given_card_with_cost_3_for_reference():
    """Rule 2.2.4b: Create a card with base cost 3 for cost-reference test."""
    return CostCardStub(name="Cost Reference Card", printed_cost=3)


@given(
    "a cost reduction effect of 1 is registered for the cost-reference card",
    target_fixture="cost_reference_card",
)
def step_given_reduction_on_cost_reference_card(cost_reference_card):
    """Rule 2.2.4b: Apply a reduction that won't affect the cost property."""
    cost_reference_card.apply_cost_reduction_during_play(1)
    return cost_reference_card


@when(
    "an effect refers to the cost of the cost-reference card",
    target_fixture="cost_reference_result",
)
def step_when_effect_refers_to_cost(cost_reference_card):
    """Rule 2.2.4b: Effect reads the cost property (unmodified)."""
    return CostReferenceResultStub(
        referenced_cost=cost_reference_card.cost,  # Unmodified cost
        is_unmodified=True,
    )


@then("the cost referred to should be the unmodified value of 3")
def step_then_referenced_cost_is_unmodified_3(cost_reference_result):
    """Rule 2.2.4b: Effect referring to 'cost' sees value 3 (not 2)."""
    assert cost_reference_result.referenced_cost == 3, (
        f"Effect referring to 'cost' should see unmodified value 3, got {cost_reference_result.referenced_cost}"
    )
    assert cost_reference_result.is_unmodified, (
        "Cost-referring effect should use the unmodified cost property (Rule 2.2.4b)"
    )


# ---------------------------------------------------------------------------
# Scenario: Effect referring to payment uses the modified cost when paid
# Tests Rule 2.2.4b - "Payment" effects use modified cost
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_2_cost.feature",
    "Effect referring to payment uses the modified cost when paid",
)
def test_effect_referring_to_payment_uses_modified_cost():
    """Rule 2.2.4b: Effects referring to 'payment' use the modified play cost."""
    pass


@given(
    "a card is created with a base cost of 3 for payment testing",
    target_fixture="payment_test_card",
)
def step_given_card_with_cost_3_for_payment():
    """Rule 2.2.4b: Create a card with base cost 3 for payment test."""
    return CostCardStub(name="Payment Test Card", printed_cost=3)


@given(
    "a cost reduction effect of 1 is registered for the payment test card",
    target_fixture="payment_test_card",
)
def step_given_reduction_on_payment_test_card(payment_test_card):
    """Rule 2.2.4b: Apply a reduction that affects play cost."""
    payment_test_card.apply_cost_reduction_during_play(1)
    return payment_test_card


@when(
    "the payment test card is played and the payment amount is recorded",
    target_fixture="payment_record",
)
def step_when_card_is_played_and_payment_recorded(payment_test_card):
    """Rule 2.2.4b: Record the payment amount when the card is played."""
    return PaymentRecordStub(
        payment_amount=payment_test_card.effective_play_cost,  # Modified cost = 2
        base_cost=payment_test_card.cost,  # Unmodified cost = 3
    )


@then("the recorded payment amount should be the modified value of 2")
def step_then_payment_amount_is_2(payment_record):
    """Rule 2.2.4b: Payment amount is the modified cost (2, not 3)."""
    assert payment_record.payment_amount == 2, (
        f"Payment amount should be 2 (modified cost), got {payment_record.payment_amount}"
    )
    assert payment_record.base_cost == 3, (
        f"Base cost should still be 3, got {payment_record.base_cost}"
    )


# ---------------------------------------------------------------------------
# Scenario: One resource symbol is functionally identical to numeric cost 1
# Tests Rule 2.2.5 - {r} and numeric 1 are equivalent
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_2_cost.feature",
    "One resource symbol is functionally identical to numeric cost 1",
)
def test_resource_symbol_identical_to_numeric_cost():
    """Rule 2.2.5: Visual {r} expression and numeric cost are equivalent."""
    pass


@given(
    "a card is created with a cost expressed as one resource symbol",
    target_fixture="one_resource_symbol_card",
)
def step_given_card_with_one_resource_symbol():
    """Rule 2.2.5: Create a card with cost expressed as one {r} symbol."""
    # Engine Feature Needed: CardInstance must support both {r} and numeric cost equally
    return NumericCostEquivalentStub(
        resource_symbol_count=1,
        numeric_equivalent=1,
    )


@when(
    "the engine interprets the resource symbol cost as numeric",
    target_fixture="symbol_to_numeric_result",
)
def step_when_interpret_resource_symbol_as_numeric(one_resource_symbol_card):
    """Rule 2.2.5: Interpret the resource symbol count as numeric cost."""
    return one_resource_symbol_card


@then("the numeric cost equivalent should be 1")
def step_then_numeric_cost_is_1(symbol_to_numeric_result):
    """Rule 2.2.5: One {r} symbol equals numeric cost 1."""
    assert symbol_to_numeric_result.numeric_equivalent == 1, (
        f"One resource symbol should equal numeric cost 1, got {symbol_to_numeric_result.numeric_equivalent}"
    )
    assert (
        symbol_to_numeric_result.resource_symbol_count
        == symbol_to_numeric_result.numeric_equivalent
    ), "Resource symbol count should equal numeric cost (Rule 2.2.5)"


# ---------------------------------------------------------------------------
# Scenario: Searching by numeric cost value finds cards with matching resource symbols
# Tests Rule 2.2.5 - {r} symbol and numeric 1 both match cost search
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_2_cost.feature",
    "Searching by numeric cost value finds cards with matching resource symbols",
)
def test_search_by_cost_finds_both_numeric_and_symbol_cards():
    """Rule 2.2.5: Searching by cost value 1 finds both numeric and {r}-symbol cards."""
    pass


@given(
    'a card named "Cost 1 Card" is created with a numeric cost of 1',
    target_fixture="cost_1_numeric_card",
)
def step_given_cost_1_numeric_card():
    """Rule 2.2.5: Create a card with numeric cost 1."""
    return CostCardStub(name="Cost 1 Card", printed_cost=1)


@given(
    'another card named "Cost 1 Symbol Card" is created with one resource symbol cost',
    target_fixture="cost_1_symbol_card",
)
def step_given_cost_1_symbol_card():
    """Rule 2.2.5: Create a card with one {r} symbol cost (equivalent to cost 1)."""
    return CostCardStub(name="Cost 1 Symbol Card", printed_cost=1)


@when(
    "the engine searches for cards with cost value 1",
    target_fixture="cost_1_search_result",
)
def step_when_search_for_cost_1_cards(cost_1_numeric_card, cost_1_symbol_card):
    """Rule 2.2.5: Search returns all cards with effective cost 1."""
    # Simulate a search that finds cards with cost 1 (numeric or symbolic)
    all_cards = [cost_1_numeric_card, cost_1_symbol_card]
    matching = [
        card.name for card in all_cards if card.has_cost_property and card.cost == 1
    ]
    return CostSearchResultStub(found_cards=matching)


@then('both "Cost 1 Card" and "Cost 1 Symbol Card" should be found')
def step_then_both_cost_1_cards_found(cost_1_search_result):
    """Rule 2.2.5: Both forms of cost 1 match the search."""
    assert "Cost 1 Card" in cost_1_search_result.found_cards, (
        '"Cost 1 Card" should be found in search for cost value 1'
    )
    assert "Cost 1 Symbol Card" in cost_1_search_result.found_cards, (
        '"Cost 1 Symbol Card" should be found in search for cost value 1 (Rule 2.2.5)'
    )
