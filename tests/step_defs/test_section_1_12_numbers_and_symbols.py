"""
Step definitions for Section 1.12: Numbers and Symbols
Reference: Flesh and Blood Comprehensive Rules Section 1.12

This module implements behavioral tests for numbers and symbols:
- Rule 1.12.1: Numbers are always integers (fractional rounding)
- Rule 1.12.1a: Fractions rounded toward zero (3.5→3, -3.5→-3)
- Rule 1.12.1b: Player-chosen numbers must be non-negative integers; "up to N" = 0..N
- Rule 1.12.2: X represents an undefined value
- Rule 1.12.2a: Undefined X evaluates to zero
- Rule 1.12.2b: Defined X persists until object ceases to exist
- Rule 1.12.2c: Multiple unknowns use Y and Z
- Rule 1.12.3: Asterisk (*) defined by meta-static ability or continuous effect
- Rule 1.12.3a: Undefined * evaluates to zero
- Rule 1.12.3b: Meta-static takes priority over continuous effect
- Rule 1.12.4: Symbols represent property values ({d}, {i}, {h}, {p}, {r}, {c}, {t}, {u})

Engine Features Needed for Section 1.12:
- [ ] NumberCalculator.calculate(value, round_direction) (Rule 1.12.1a)
- [ ] NumberSelector.validate_choice(value, constraint) (Rule 1.12.1b)
- [ ] NumberSelector.validate_up_to_choice(value, max_value) (Rule 1.12.1b)
- [ ] VariableValue class tracking X, Y, Z with defined/undefined state (Rule 1.12.2)
- [ ] VariableValue.evaluate() returning 0 when undefined (Rule 1.12.2a)
- [ ] VariableValue.define(value) persisting until source ceases (Rule 1.12.2b)
- [ ] AsteriskValue class for * properties defined by meta-static/continuous (Rule 1.12.3)
- [ ] AsteriskValue.evaluate() returning 0 when undefined (Rule 1.12.3a)
- [ ] AsteriskValue.resolve_priority() preferring meta-static over effect (Rule 1.12.3b)
- [ ] SymbolRegistry mapping {d}, {i}, {h}, {p}, {r}, {c}, {t}, {u} (Rule 1.12.4)
- [ ] SymbolRegistry.get_property_name(symbol) (Rule 1.12.4)
- [ ] SymbolRegistry.represents_effect(symbol) for {t} and {u} (Rules 1.12.4g/h)
"""

import pytest
from pytest_bdd import scenario, given, when, then, parsers


# =============================================================================
# Scenario registrations
# =============================================================================


@scenario(
    "../features/section_1_12_numbers_and_symbols.feature",
    "Positive fractional calculation rounded toward zero",
)
def test_positive_fractional_rounded_toward_zero():
    """Rule 1.12.1a: Positive fractions rounded toward zero (3.5 → 3)."""
    pass


@scenario(
    "../features/section_1_12_numbers_and_symbols.feature",
    "Negative fractional calculation rounded toward zero",
)
def test_negative_fractional_rounded_toward_zero():
    """Rule 1.12.1a: Negative fractions rounded toward zero (-3.5 → -3)."""
    pass


@scenario(
    "../features/section_1_12_numbers_and_symbols.feature",
    "Effect specifying round up uses upward rounding",
)
def test_effect_with_round_up_specification():
    """Rule 1.12.1a: When effect specifies 'round up', upward rounding is used."""
    pass


@scenario(
    "../features/section_1_12_numbers_and_symbols.feature",
    "Player choosing a number must choose non-negative integer",
)
def test_player_cannot_choose_negative_number():
    """Rule 1.12.1b: Player-chosen numbers must be non-negative integers."""
    pass


@scenario(
    "../features/section_1_12_numbers_and_symbols.feature",
    "Player can choose zero as their number",
)
def test_player_can_choose_zero():
    """Rule 1.12.1b: Zero is a valid choice for player-chosen numbers."""
    pass


@scenario(
    "../features/section_1_12_numbers_and_symbols.feature",
    "Player can choose any positive integer",
)
def test_player_can_choose_positive_integer():
    """Rule 1.12.1b: Positive integers are valid choices."""
    pass


@scenario(
    "../features/section_1_12_numbers_and_symbols.feature",
    "Up to N allows choosing zero",
)
def test_up_to_n_allows_zero():
    """Rule 1.12.1b: Zero is always valid for 'up to N' choices."""
    pass


@scenario(
    "../features/section_1_12_numbers_and_symbols.feature",
    "Up to N allows choosing the maximum",
)
def test_up_to_n_allows_maximum():
    """Rule 1.12.1b: Choosing exactly N is valid for 'up to N' choices."""
    pass


@scenario(
    "../features/section_1_12_numbers_and_symbols.feature",
    "Up to N rejects exceeding the maximum",
)
def test_up_to_n_rejects_exceeding_maximum():
    """Rule 1.12.1b: Choosing more than N is invalid for 'up to N' choices."""
    pass


@scenario(
    "../features/section_1_12_numbers_and_symbols.feature",
    "Object with undefined X value still has that property",
)
def test_object_with_undefined_x_still_has_property():
    """Rule 1.12.2a: Card with power X still has the power property even when X is undefined."""
    pass


@scenario(
    "../features/section_1_12_numbers_and_symbols.feature",
    "Undefined X evaluates to zero when checking cost",
)
def test_undefined_x_evaluates_to_zero():
    """Rule 1.12.2a: Undefined X is treated as zero for calculations."""
    pass


@scenario(
    "../features/section_1_12_numbers_and_symbols.feature",
    "Defined X value persists until the object ceases to exist",
)
def test_defined_x_persists_until_object_ceases():
    """Rule 1.12.2b: Once X is defined it stays defined until the object ceases to exist."""
    pass


@scenario(
    "../features/section_1_12_numbers_and_symbols.feature",
    "X value does not change after being defined while object exists",
)
def test_defined_x_does_not_reset():
    """Rule 1.12.2b: Defined X cannot be reset to undefined while the object exists."""
    pass


@scenario(
    "../features/section_1_12_numbers_and_symbols.feature",
    "Two or more undefined values in same context use Y and Z",
)
def test_multiple_undefined_values_use_y_and_z():
    """Rule 1.12.2c: Multiple undefined values use X, Y, Z as distinct labels."""
    pass


@scenario(
    "../features/section_1_12_numbers_and_symbols.feature",
    "Object with asterisk value still has that property",
)
def test_object_with_asterisk_still_has_property():
    """Rule 1.12.3: Card with power * still has the power property."""
    pass


@scenario(
    "../features/section_1_12_numbers_and_symbols.feature",
    "Undefined asterisk value evaluates to zero",
)
def test_undefined_asterisk_evaluates_to_zero():
    """Rule 1.12.3a: When * has no defining ability or effect, it evaluates to zero."""
    pass


@scenario(
    "../features/section_1_12_numbers_and_symbols.feature",
    "Mutated Mass power and defense outside game evaluate to zero",
)
def test_mutated_mass_outside_game_is_zero():
    """Rule 1.12.3a: Mutated Mass ability can't define * outside game, so power/defense = 0."""
    pass


@scenario(
    "../features/section_1_12_numbers_and_symbols.feature",
    "Meta-static ability takes priority over continuous effect for asterisk",
)
def test_meta_static_takes_priority_over_continuous_effect():
    """Rule 1.12.3b: Meta-static ability has higher priority than continuous effect for *."""
    pass


@scenario(
    "../features/section_1_12_numbers_and_symbols.feature",
    "Continuous effect defines asterisk when no meta-static ability applies",
)
def test_continuous_effect_defines_asterisk_without_meta_static():
    """Rule 1.12.3b: Continuous effect defines * when no meta-static ability applies."""
    pass


@scenario(
    "../features/section_1_12_numbers_and_symbols.feature",
    "Become copy effect defines asterisk as printed life of original",
)
def test_become_copy_effect_defines_asterisk_life():
    """Rule 1.12.3b: Arakni example - become/copy effect defines * as printed life."""
    pass


@scenario(
    "../features/section_1_12_numbers_and_symbols.feature",
    "Defense symbol represents defense value",
)
def test_defense_symbol_represents_defense():
    """Rule 1.12.4a: The symbol {d} represents a defense value."""
    pass


@scenario(
    "../features/section_1_12_numbers_and_symbols.feature",
    "Intellect symbol represents intellect value",
)
def test_intellect_symbol_represents_intellect():
    """Rule 1.12.4b: The symbol {i} represents an intellect value."""
    pass


@scenario(
    "../features/section_1_12_numbers_and_symbols.feature",
    "Life symbol represents life value",
)
def test_life_symbol_represents_life():
    """Rule 1.12.4c: The symbol {h} represents a life value."""
    pass


@scenario(
    "../features/section_1_12_numbers_and_symbols.feature",
    "Power symbol represents power value",
)
def test_power_symbol_represents_power():
    """Rule 1.12.4d: The symbol {p} represents a power value and physical damage."""
    pass


@scenario(
    "../features/section_1_12_numbers_and_symbols.feature",
    "Resource symbol represents resource value",
)
def test_resource_symbol_represents_resource():
    """Rule 1.12.4e: The symbol {r} represents a resource value."""
    pass


@scenario(
    "../features/section_1_12_numbers_and_symbols.feature",
    "Chi symbol represents chi value",
)
def test_chi_symbol_represents_chi():
    """Rule 1.12.4f: The symbol {c} represents a chi value."""
    pass


@scenario(
    "../features/section_1_12_numbers_and_symbols.feature",
    "Tap symbol represents the tap effect",
)
def test_tap_symbol_represents_tap_effect():
    """Rule 1.12.4g: The symbol {t} represents the tap effect."""
    pass


@scenario(
    "../features/section_1_12_numbers_and_symbols.feature",
    "Untap symbol represents the untap effect",
)
def test_untap_symbol_represents_untap_effect():
    """Rule 1.12.4h: The symbol {u} represents the untap effect."""
    pass


# =============================================================================
# Step Definitions - Given
# =============================================================================


@given("the game engine is initialized")
def step_game_engine_initialized(game_state):
    """Initialize the game engine for testing numbers and symbols."""
    assert game_state is not None


@given("a player must choose a number for an effect")
def step_player_must_choose_number(game_state):
    """Rule 1.12.1b: Set up a number-selection scenario for an effect."""
    game_state.open_choice_constraint = "any_non_negative_integer"


@given(parsers.parse('a player must choose "up to" {max_val:d} for an effect'))
def step_player_must_choose_up_to_n(game_state, max_val):
    """Rule 1.12.1b: Set up an 'up to N' number-selection scenario."""
    game_state.up_to_max = max_val


@given("a card with variable power X is created")
def step_create_variable_power_x_card(game_state):
    """Rule 1.12.2: Create a card whose power property is the variable X."""
    game_state.x_power_card = game_state.create_variable_card(
        property_name="power", variable="X"
    )


@given("the X variable for that card is undefined")
def step_x_variable_undefined(game_state):
    """Rule 1.12.2a: Ensure X has not been defined yet."""
    assert not game_state.is_var_defined(game_state.x_power_card, "X")


@given("a card with variable cost X is created")
def step_create_variable_cost_x_card(game_state):
    """Rule 1.12.2: Create a card whose cost property is the variable X."""
    game_state.x_cost_card = game_state.create_variable_card(
        property_name="cost", variable="X"
    )


@given(parsers.parse("X is pre-defined as {value:d} for the variable-power card"))
def step_x_predefined_as_value(game_state, value):
    """Rule 1.12.2b: Pre-define X for the variable-power card."""
    game_state.define_var(game_state.x_power_card, "X", value)


@given("a context has two undefined values labeled X and Y")
def step_context_has_x_and_y(game_state):
    """Rule 1.12.2c: Set up a context with two distinct undefined variables."""
    game_state.multi_var_ctx = game_state.create_multi_var_context(["X", "Y"])


@given("a card with asterisk power is created")
def step_create_asterisk_power_card(game_state):
    """Rule 1.12.3: Create a card whose power property is the asterisk (*)."""
    game_state.star_power_card = game_state.create_asterisk_card(property_name="power")


@given("no meta-static ability or continuous effect defines the asterisk power")
def step_no_ability_defines_asterisk(game_state):
    """Rule 1.12.3a: No defining ability or effect for the * value."""
    assert not game_state.is_asterisk_defined(game_state.star_power_card, "power")


@given("a Mutated Mass card with asterisk power and defense is created")
def step_create_mutated_mass(game_state):
    """Rule 1.12.3a: Mutated Mass has power=* and defense=* via meta-static ability."""
    game_state.mutated_mass_card = game_state.create_asterisk_card(
        property_name="power", card_name="Mutated Mass"
    )
    game_state.add_asterisk_to_card(game_state.mutated_mass_card, "defense")


@given("no game context exists to define Mutated Mass's asterisk values")
def step_no_game_context_for_mutated_mass(game_state):
    """Rule 1.12.3a: Outside of game, the meta-static ability cannot be used."""
    game_state.mutated_mass_has_game_context = False


@given(parsers.parse("a meta-static ability defines the asterisk power as {value:d}"))
def step_meta_static_defines_power(game_state, value):
    """Rule 1.12.3b: Add a meta-static ability defining asterisk power."""
    game_state.add_meta_static(game_state.star_power_card, "power", value)


@given(
    parsers.parse("a continuous effect also defines the asterisk power as {value:d}")
)
def step_continuous_effect_also_defines_power(game_state, value):
    """Rule 1.12.3b: Add a continuous effect also defining asterisk power."""
    game_state.add_continuous_effect(game_state.star_power_card, "power", value)


@given("no meta-static ability defines the asterisk power")
def step_no_meta_static_for_asterisk_power(game_state):
    """Rule 1.12.3b: No meta-static ability defines * in this context."""
    # By default no meta-static is defined — nothing to do
    pass


@given(parsers.parse("a continuous effect defines the asterisk power as {value:d}"))
def step_continuous_effect_defines_power(game_state, value):
    """Rule 1.12.3b: Add a continuous effect defining asterisk power."""
    game_state.add_continuous_effect(game_state.star_power_card, "power", value)


@given("an Agent of Chaos card with asterisk life is created")
def step_create_agent_of_chaos(game_state):
    """Rule 1.12.3b: Agent of Chaos has life=*."""
    game_state.agent_chaos_card = game_state.create_asterisk_card(
        property_name="life", card_name="Agent of Chaos"
    )


@given("a become-copy effect defines the life asterisk as the printed life of Arakni")
def step_become_copy_defines_life(game_state):
    """Rule 1.12.3b: Become/copy effect sets * equal to Arakni's printed life."""
    game_state.arakni_life = 40  # Arakni's life value used in the example
    game_state.apply_become_copy(
        game_state.agent_chaos_card, "life", game_state.arakni_life
    )


@given("the symbol registry is available")
def step_symbol_registry_available(game_state):
    """Rule 1.12.4: The game engine has a symbol registry."""
    assert game_state.get_symbol_registry() is not None


# =============================================================================
# Step Definitions - When
# =============================================================================


@when("an effect calculates the value 3.5")
def step_calculate_3_5(game_state):
    """Rule 1.12.1a: Calculate a positive fractional value."""
    game_state.calc_result = game_state.calc_number(3.5)


@when("an effect calculates the value -3.5")
def step_calculate_neg_3_5(game_state):
    """Rule 1.12.1a: Calculate a negative fractional value."""
    game_state.calc_result = game_state.calc_number(-3.5)


@when("an effect calculates the value 2.5 and specifies to round up")
def step_calculate_2_5_round_up(game_state):
    """Rule 1.12.1a: Calculate with round-up specification."""
    game_state.round_up_result = game_state.calc_number(2.5, round_direction="up")


@when(
    parsers.parse(
        "the player attempts to choose the value {value:d} from an open choice"
    )
)
def step_player_open_choice(game_state, value):
    """Rule 1.12.1b: Player makes an open (any non-negative integer) choice."""
    game_state.open_choice_value = value
    game_state.open_choice_result = game_state.validate_choice(
        value, constraint="any_non_negative_integer"
    )


@when(
    parsers.parse(
        "the player attempts to choose the value {value:d} from an up-to-3 range"
    )
)
def step_player_up_to_choice(game_state, value):
    """Rule 1.12.1b: Player makes an 'up to 3' choice."""
    game_state.up_to_choice_value = value
    game_state.up_to_choice_result = game_state.validate_choice(
        value, constraint="up_to", max_value=game_state.up_to_max
    )


@when("the cost X is evaluated while undefined")
def step_evaluate_cost_x_undefined(game_state):
    """Rule 1.12.2a: Evaluate the cost X while it is undefined."""
    game_state.cost_x_evaluated = game_state.eval_var(game_state.x_cost_card, "X")


@when(parsers.parse("X is defined as {value:d} for the variable-power card"))
def step_define_x_as_value(game_state, value):
    """Rule 1.12.2b: Define X for the variable-power card."""
    game_state.define_var(game_state.x_power_card, "X", value)


@when("another effect would try to reset the X variable to undefined")
def step_try_reset_x(game_state):
    """Rule 1.12.2b: Try to reset X to undefined while the card exists."""
    game_state.reset_result = game_state.try_reset_var(game_state.x_power_card, "X")


@when(parsers.parse('looking up the symbol "{symbol}"'))
def step_lookup_symbol(game_state, symbol):
    """Rule 1.12.4: Look up the meaning of a symbol in the registry."""
    registry = game_state.get_symbol_registry()
    game_state.symbol_result = registry.lookup(symbol)


# =============================================================================
# Step Definitions - Then
# =============================================================================


@then("the result is rounded to 3")
def step_result_is_3(game_state):
    """Rule 1.12.1a: 3.5 rounds toward zero to 3."""
    assert game_state.calc_result == 3, (
        f"Expected 3.5 to round to 3, got {game_state.calc_result}"
    )


@then("the result is rounded to -3")
def step_result_is_neg_3(game_state):
    """Rule 1.12.1a: -3.5 rounds toward zero to -3."""
    assert game_state.calc_result == -3, (
        f"Expected -3.5 to round to -3, got {game_state.calc_result}"
    )


@then("the result of the round-up calculation is 3")
def step_round_up_result_is_3(game_state):
    """Rule 1.12.1a: When 'round up' is specified, 2.5 rounds up to 3."""
    assert game_state.round_up_result == 3, (
        f"Expected 2.5 to round up to 3, got {game_state.round_up_result}"
    )


@then("the open choice is rejected as invalid")
def step_open_choice_rejected(game_state):
    """Rule 1.12.1b: Open choice was invalid."""
    assert not game_state.open_choice_result.is_valid, (
        f"Expected open choice {game_state.open_choice_value} to be rejected"
    )


@then("the open choice is accepted as valid")
def step_open_choice_accepted(game_state):
    """Rule 1.12.1b: Open choice was valid."""
    assert game_state.open_choice_result.is_valid, (
        f"Expected open choice {game_state.open_choice_value} to be accepted"
    )


@then("the up-to-3 choice is accepted as valid")
def step_up_to_choice_accepted(game_state):
    """Rule 1.12.1b: Up-to-3 choice was valid."""
    assert game_state.up_to_choice_result.is_valid, (
        f"Expected up-to-3 choice {game_state.up_to_choice_value} to be accepted"
    )


@then("the up-to-3 choice is rejected as invalid")
def step_up_to_choice_rejected(game_state):
    """Rule 1.12.1b: Up-to-3 choice was invalid."""
    assert not game_state.up_to_choice_result.is_valid, (
        f"Expected up-to-3 choice {game_state.up_to_choice_value} to be rejected"
    )


@then("the variable-power card is considered to have the power property")
def step_variable_power_card_has_power(game_state):
    """Rule 1.12.2a: Card still has the power property even with undefined X."""
    assert game_state.has_property(game_state.x_power_card, "power"), (
        "Card should still have power property even when X is undefined"
    )


@then("the variable-power card's power evaluates to 0")
def step_variable_power_evaluates_to_zero(game_state):
    """Rule 1.12.2a: Undefined X evaluates to 0."""
    val = game_state.eval_property(game_state.x_power_card, "power")
    assert val == 0, f"Expected power X = 0 when undefined, got {val}"


@then("the variable-cost card still has the cost property")
def step_variable_cost_card_has_cost(game_state):
    """Rule 1.12.2a: Object still has the cost property even with undefined X."""
    assert game_state.has_property(game_state.x_cost_card, "cost"), (
        "Card should still have cost property even when X is undefined"
    )


@then("the cost X value evaluates to 0")
def step_cost_x_evaluates_to_zero(game_state):
    """Rule 1.12.2a: Undefined X evaluates to zero."""
    assert game_state.cost_x_evaluated == 0, (
        f"Expected cost X to evaluate to 0, got {game_state.cost_x_evaluated}"
    )


@then(parsers.parse("the variable-power card's power evaluates to {expected:d}"))
def step_variable_power_evaluates_to(game_state, expected):
    """Rule 1.12.2b: Variable-power card's power evaluates to defined X value."""
    val = game_state.eval_property(game_state.x_power_card, "power")
    assert val == expected, f"Expected power to evaluate to {expected}, got {val}"


@then("the X value persists for the lifetime of the variable-power card")
def step_x_persists_for_card_lifetime(game_state):
    """Rule 1.12.2b: Defined X remains defined while object exists."""
    assert game_state.is_var_defined(game_state.x_power_card, "X"), (
        "X should remain defined while the object exists"
    )


@then(parsers.parse("the variable-power card's power still evaluates to {expected:d}"))
def step_variable_power_still_evaluates_to(game_state, expected):
    """Rule 1.12.2b: Power should still reflect original defined X, not a reset."""
    val = game_state.eval_property(game_state.x_power_card, "power")
    assert val == expected, (
        f"Expected power to still evaluate to {expected} after reset attempt, got {val}"
    )


@then("X and Y represent distinct undefined values")
def step_x_and_y_are_distinct(game_state):
    """Rule 1.12.2c: X and Y are separate, distinct variable slots."""
    assert game_state.vars_are_distinct(game_state.multi_var_ctx, "X", "Y"), (
        "X and Y should be distinct undefined values"
    )


@then("X and Y each evaluate to 0 while undefined")
def step_x_and_y_evaluate_zero(game_state):
    """Rule 1.12.2c: Both X and Y evaluate to 0 while undefined."""
    x_val = game_state.eval_ctx_var(game_state.multi_var_ctx, "X")
    y_val = game_state.eval_ctx_var(game_state.multi_var_ctx, "Y")
    assert x_val == 0, f"Expected X to evaluate to 0, got {x_val}"
    assert y_val == 0, f"Expected Y to evaluate to 0, got {y_val}"


@then("the asterisk-power card is considered to have the power property")
def step_asterisk_card_has_power(game_state):
    """Rule 1.12.3: Card still has the power property even with * value."""
    assert game_state.has_property(game_state.star_power_card, "power"), (
        "Card should have power property even when power is *"
    )


@then("the asterisk power evaluates to 0")
def step_asterisk_power_evaluates_to_zero(game_state):
    """Rule 1.12.3a: Undefined * evaluates to zero."""
    val = game_state.eval_property(game_state.star_power_card, "power")
    assert val == 0, f"Expected asterisk power to evaluate to 0, got {val}"


@then("Mutated Mass power evaluates to 0")
def step_mutated_mass_power_zero(game_state):
    """Rule 1.12.3a: Mutated Mass power = 0 when evaluated outside game context."""
    val = game_state.eval_property(
        game_state.mutated_mass_card,
        "power",
        has_game_context=game_state.mutated_mass_has_game_context,
    )
    assert val == 0, f"Expected Mutated Mass power to be 0 outside game, got {val}"


@then("Mutated Mass defense evaluates to 0")
def step_mutated_mass_defense_zero(game_state):
    """Rule 1.12.3a: Mutated Mass defense = 0 when evaluated outside game context."""
    val = game_state.eval_property(
        game_state.mutated_mass_card,
        "defense",
        has_game_context=game_state.mutated_mass_has_game_context,
    )
    assert val == 0, f"Expected Mutated Mass defense to be 0 outside game, got {val}"


@then(parsers.parse("the asterisk-power card's power evaluates to {expected:d}"))
def step_asterisk_power_evaluates_to(game_state, expected):
    """Rule 1.12.3b: Asterisk power evaluates to the winning definition."""
    val = game_state.eval_property(game_state.star_power_card, "power")
    assert val == expected, (
        f"Expected asterisk power to evaluate to {expected}, got {val}"
    )


@then("the Agent of Chaos card's life evaluates to Arakni's printed life")
def step_agent_life_equals_arakni_life(game_state):
    """Rule 1.12.3b: Agent of Chaos life should match Arakni's printed life."""
    val = game_state.eval_property(game_state.agent_chaos_card, "life")
    assert val == game_state.arakni_life, (
        f"Expected Agent of Chaos life to be {game_state.arakni_life}, got {val}"
    )


@then(parsers.parse('the symbol represents the property "{property_name}"'))
def step_symbol_is_property(game_state, property_name):
    """Rule 1.12.4: The symbol should map to the expected property name."""
    result = game_state.symbol_result
    assert result.property_name == property_name, (
        f"Expected symbol to represent '{property_name}', got '{result.property_name}'"
    )


@then("the symbol also refers to physical damage")
def step_symbol_also_physical_damage(game_state):
    """Rule 1.12.4d: {p} also refers to physical damage."""
    assert game_state.symbol_result.also_refers_to_physical_damage, (
        "Power symbol {p} should also refer to physical damage"
    )


@then(parsers.parse('the symbol represents the "{effect_name}" effect'))
def step_symbol_is_effect(game_state, effect_name):
    """Rule 1.12.4g/h: Symbol represents an effect (tap/untap)."""
    result = game_state.symbol_result
    assert result.effect_name == effect_name, (
        f"Expected symbol to represent '{effect_name}' effect, got '{result.effect_name}'"
    )


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture
def game_state():
    """
    Fixture providing game state for testing numbers and symbols.

    Uses BDDGameState extended with number/symbol helpers.
    Reference: Rule 1.12
    """
    from tests.bdd_helpers import BDDGameState

    state = BDDGameState()

    # ── State variables ──────────────────────────────────────────────────────
    state.calc_result = None
    state.round_up_result = None
    state.open_choice_constraint = "any_non_negative_integer"
    state.open_choice_value = None
    state.open_choice_result = None
    state.up_to_max = None
    state.up_to_choice_value = None
    state.up_to_choice_result = None
    state.x_power_card = None
    state.x_cost_card = None
    state.cost_x_evaluated = None
    state.multi_var_ctx = None
    state.star_power_card = None
    state.mutated_mass_card = None
    state.mutated_mass_has_game_context = True
    state.agent_chaos_card = None
    state.arakni_life = 40
    state.symbol_result = None
    state.reset_result = None

    # ── Helper implementations ───────────────────────────────────────────────

    def calc_number(value, round_direction=None):
        """
        Calculate a game number, rounding fractions toward zero unless specified.

        Engine Feature Needed:
        - [ ] NumberCalculator.calculate(value, round_direction) (Rule 1.12.1a)
        """
        import math

        if round_direction == "up":
            return math.ceil(value)
        elif round_direction == "down":
            return math.floor(value)
        else:
            # Rule 1.12.1a: Round toward zero (truncate)
            return math.trunc(value)

    state.calc_number = calc_number

    class _ChoiceResult:
        def __init__(self, is_valid, reason=""):
            self.is_valid = is_valid
            self.reason = reason

    def validate_choice(value, constraint="any_non_negative_integer", max_value=None):
        """
        Validate a player's number choice against a constraint.

        Engine Feature Needed:
        - [ ] NumberSelector.validate_choice(value, constraint) (Rule 1.12.1b)
        """
        if constraint == "any_non_negative_integer":
            if not isinstance(value, int) or value < 0:
                return _ChoiceResult(False, "must_be_non_negative_integer")
            return _ChoiceResult(True)
        elif constraint == "up_to":
            if max_value is None:
                return _ChoiceResult(False, "no_max_value")
            if not isinstance(value, int) or value < 0 or value > max_value:
                return _ChoiceResult(False, f"must_be_0_to_{max_value}")
            return _ChoiceResult(True)
        return _ChoiceResult(False, "unknown_constraint")

    state.validate_choice = validate_choice

    # ── Variable card implementation (Rule 1.12.2) ──────────────────────────

    class _VarCard:
        """Stub for a card with a variable (X/Y/Z) property."""

        def __init__(self, property_name, variable, card_name="Test Variable Card"):
            self.card_name = card_name
            self.property_name = property_name
            self.variable = variable
            self._vars = {}  # var_name -> value or None (undefined)
            self._asterisk_props = {}  # prop_name -> list of (type, value)
            self._asterisk_set = set()

        def has_property(self, prop):
            return (
                self.property_name == prop
                or prop in self._asterisk_set
                or prop in self._asterisk_props
            )

        def eval_prop(self, prop, has_game_context=True):
            # Asterisk property
            if prop in self._asterisk_set or prop in self._asterisk_props:
                defs = self._asterisk_props.get(prop, [])
                if not has_game_context:
                    # Rule 1.12.3a: No game context → meta-static can't activate
                    cont_defs = [(t, v) for t, v in defs if t == "continuous"]
                    return cont_defs[0][1] if cont_defs else 0
                # Rule 1.12.3b: meta-static > continuous
                meta_defs = [(t, v) for t, v in defs if t == "meta_static"]
                if meta_defs:
                    return meta_defs[0][1]
                cont_defs = [(t, v) for t, v in defs if t == "continuous"]
                return cont_defs[0][1] if cont_defs else 0  # Rule 1.12.3a

            # Variable (X) property
            if self.property_name == prop:
                v = self._vars.get(self.variable)
                return v if v is not None else 0  # Rule 1.12.2a

            return 0

        def is_defined(self, var_name):
            return self._vars.get(var_name) is not None

        def define(self, var_name, value):
            self._vars[var_name] = value  # Rule 1.12.2b: stays defined

        def try_reset(self, var_name):
            # Rule 1.12.2b: Once defined, remains defined
            return {"reset_attempted": True, "reset_succeeded": False}

        def is_star_defined(self, prop):
            return bool(self._asterisk_props.get(prop, []))

    def create_variable_card(property_name, variable, card_name="Test Var Card"):
        """
        Engine Feature Needed:
        - [ ] CardTemplate/CardInstance supporting variable properties (Rule 1.12.2)
        """
        return _VarCard(
            property_name=property_name, variable=variable, card_name=card_name
        )

    state.create_variable_card = create_variable_card

    def is_var_defined(card, var_name):
        return card.is_defined(var_name)

    state.is_var_defined = is_var_defined

    def has_property(card, prop):
        return card.has_property(prop)

    state.has_property = has_property

    def eval_property(card, prop, has_game_context=True):
        """
        Engine Feature Needed:
        - [ ] CardInstance.evaluate_property(name) (Rule 1.12.2a/b, 1.12.3a/b)
        """
        return card.eval_prop(prop, has_game_context=has_game_context)

    state.eval_property = eval_property

    def eval_var(card, var_name):
        v = card._vars.get(var_name)
        return v if v is not None else 0

    state.eval_var = eval_var

    def define_var(card, var_name, value):
        card.define(var_name, value)

    state.define_var = define_var

    def try_reset_var(card, var_name):
        return card.try_reset(var_name)

    state.try_reset_var = try_reset_var

    # ── Multi-variable context (Rule 1.12.2c) ───────────────────────────────

    class _MultiVarCtx:
        def __init__(self, var_names):
            self.var_names = list(var_names)
            self._vals = {n: None for n in var_names}

        def are_distinct(self, a, b):
            return a != b and a in self.var_names and b in self.var_names

        def eval(self, var_name):
            v = self._vals.get(var_name)
            return v if v is not None else 0

    def create_multi_var_context(var_names):
        """
        Engine Feature Needed:
        - [ ] Multi-variable context tracking X, Y, Z (Rule 1.12.2c)
        """
        return _MultiVarCtx(var_names)

    state.create_multi_var_context = create_multi_var_context

    def vars_are_distinct(ctx, a, b):
        return ctx.are_distinct(a, b)

    state.vars_are_distinct = vars_are_distinct

    def eval_ctx_var(ctx, var_name):
        return ctx.eval(var_name)

    state.eval_ctx_var = eval_ctx_var

    # ── Asterisk card helpers (Rule 1.12.3) ─────────────────────────────────

    def create_asterisk_card(property_name, card_name="Test Asterisk Card"):
        """
        Engine Feature Needed:
        - [ ] AsteriskProperty class tracking meta-static/continuous definitions (Rule 1.12.3)
        """
        card = _VarCard(property_name=property_name, variable="*", card_name=card_name)
        card._asterisk_set.add(property_name)
        card._asterisk_props[property_name] = []
        return card

    state.create_asterisk_card = create_asterisk_card

    def add_asterisk_to_card(card, prop):
        card._asterisk_set.add(prop)
        if prop not in card._asterisk_props:
            card._asterisk_props[prop] = []

    state.add_asterisk_to_card = add_asterisk_to_card

    def is_asterisk_defined(card, prop):
        return card.is_star_defined(prop)

    state.is_asterisk_defined = is_asterisk_defined

    def add_meta_static(card, prop, value):
        """
        Engine Feature Needed:
        - [ ] MetaStaticAbility defining asterisk value (Rule 1.12.3b)
        """
        if prop not in card._asterisk_props:
            card._asterisk_props[prop] = []
        card._asterisk_props[prop].append(("meta_static", value))

    state.add_meta_static = add_meta_static

    def add_continuous_effect(card, prop, value):
        """
        Engine Feature Needed:
        - [ ] ContinuousEffect defining asterisk value (Rule 1.12.3b)
        """
        if prop not in card._asterisk_props:
            card._asterisk_props[prop] = []
        card._asterisk_props[prop].append(("continuous", value))

    state.add_continuous_effect = add_continuous_effect

    def apply_become_copy(card, prop, source_value):
        """
        Engine Feature Needed:
        - [ ] BecomeCopyEffect.define_asterisk(prop, printed_value) (Rule 1.12.3b)
        """
        if prop not in card._asterisk_props:
            card._asterisk_props[prop] = []
        card._asterisk_props[prop].append(("continuous", source_value))
        card._asterisk_set.add(prop)

    state.apply_become_copy = apply_become_copy

    # ── Symbol registry (Rule 1.12.4) ────────────────────────────────────────

    class _SymbolResult:
        def __init__(
            self,
            symbol,
            property_name=None,
            effect_name=None,
            also_refers_to_physical_damage=False,
        ):
            self.symbol = symbol
            self.property_name = property_name
            self.effect_name = effect_name
            self.also_refers_to_physical_damage = also_refers_to_physical_damage

    class _SymbolRegistry:
        """
        Registry mapping symbols to their meanings.

        Engine Feature Needed:
        - [ ] SymbolRegistry class with complete symbol table (Rule 1.12.4)
        """

        _TABLE = {
            "d": _SymbolResult("d", property_name="defense"),
            "i": _SymbolResult("i", property_name="intellect"),
            "h": _SymbolResult("h", property_name="life"),
            "p": _SymbolResult(
                "p", property_name="power", also_refers_to_physical_damage=True
            ),
            "r": _SymbolResult("r", property_name="resource"),
            "c": _SymbolResult("c", property_name="chi"),
            "t": _SymbolResult("t", effect_name="tap"),
            "u": _SymbolResult("u", effect_name="untap"),
        }

        def lookup(self, symbol):
            """
            Engine Feature Needed:
            - [ ] SymbolRegistry.lookup(symbol) -> SymbolResult (Rule 1.12.4)
            """
            result = self._TABLE.get(symbol)
            if result is None:
                raise KeyError(
                    f"Engine Feature Needed: SymbolRegistry missing symbol '{symbol}'. "
                    "Implement SymbolRegistry with all symbols from Rule 1.12.4."
                )
            return result

    def get_symbol_registry():
        """
        Engine Feature Needed:
        - [ ] GameEngine.get_symbol_registry() returning SymbolRegistry (Rule 1.12.4)
        """
        return _SymbolRegistry()

    state.get_symbol_registry = get_symbol_registry

    return state
