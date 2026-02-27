"""
Step definitions for Section 1.15: Counters
Reference: Flesh and Blood Comprehensive Rules Section 1.15

This module implements behavioral tests for the counter system in Flesh and Blood.
Counters are physical markers placed on public objects that can modify properties
and/or interact with effects.

Engine Features Needed for Section 1.15:
- [ ] Counter class with name or (value, symbol) identity (Rule 1.15.1)
- [ ] Counter.is_game_object = False (Rule 1.15.1)
- [ ] Counter identity equality by name or value+symbol (Rule 1.15.1)
- [ ] CardInstance.counters list tracking placed counters (Rule 1.15.2)
- [ ] CardInstance.add_counter(counter) method (Rule 1.15.2)
- [ ] CardInstance.remove_counter(counter) method (Rule 1.15.3)
- [ ] CardInstance.get_counters(name_or_symbol) method (Rule 1.15.1)
- [ ] Counter property modification system - rule-based, not effect (Rule 1.15.2a)
- [ ] Counter.value and Counter.symbol for numeric+symbol counters (Rule 1.15.2a)
- [ ] CardInstance.effective_power with counter modification (Rule 1.15.2a)
- [ ] CardInstance.effective_defense with counter modification (Rule 1.15.2a)
- [ ] Counter modification same timing layer as continuous effects (Rule 1.15.2a)
- [ ] Counters cease when object ceases (Rule 1.15.3)
- [ ] Counters cease when removed (Rule 1.15.3)
- [ ] No counter cancellation for diametrically opposing counters (Rule 1.15.4)
- [ ] Both opposing counters remain when opposing counter added (Rule 1.15.4)
"""

import pytest
from pytest_bdd import scenario, given, when, then, parsers
from dataclasses import dataclass, field
from typing import List, Optional, Any


# ============================================================
# Scenario: A counter is a physical marker placed on a public object
# Tests Rule 1.15.1 - Counters are physical markers on objects
# ============================================================


@scenario(
    "../features/section_1_15_counters.feature",
    "A counter is a physical marker placed on a public object",
)
def test_counter_is_physical_marker_on_object():
    """Rule 1.15.1: A counter is a physical marker placed on any public object."""
    pass


# ============================================================
# Scenario: A counter is not an object and has no properties
# Tests Rule 1.15.1 - Counters are not objects
# ============================================================


@scenario(
    "../features/section_1_15_counters.feature",
    "A counter is not an object and has no properties",
)
def test_counter_is_not_object_and_has_no_properties():
    """Rule 1.15.1: A counter is not an object and does not have properties."""
    pass


# ============================================================
# Scenario: Counter identity is defined by its name
# Tests Rule 1.15.1 - Name-based counter identity
# ============================================================


@scenario(
    "../features/section_1_15_counters.feature",
    "Counter identity is defined by its name",
)
def test_counter_identity_defined_by_name():
    """Rule 1.15.1: The identity of a counter is defined by its name."""
    pass


# ============================================================
# Scenario: Counter identity is defined by numerical value and symbol
# Tests Rule 1.15.1 - Value+symbol counter identity
# ============================================================


@scenario(
    "../features/section_1_15_counters.feature",
    "Counter identity is defined by numerical value and symbol",
)
def test_counter_identity_defined_by_value_and_symbol():
    """Rule 1.15.1: The identity of a counter is defined by its numerical value and symbol."""
    pass


# ============================================================
# Scenario: Counters with same name are interchangeable
# Tests Rule 1.15.1 - Same-name counters are interchangeable
# ============================================================


@scenario(
    "../features/section_1_15_counters.feature",
    "Counters with same name are interchangeable",
)
def test_counters_with_same_name_are_interchangeable():
    """Rule 1.15.1: Counters with the same name are functionally identical and interchangeable."""
    pass


# ============================================================
# Scenario: Counters with different names are not the same
# Tests Rule 1.15.1 - Different-named counters have different identities
# ============================================================


@scenario(
    "../features/section_1_15_counters.feature",
    "Counters with different names are not the same",
)
def test_counters_with_different_names_are_not_same():
    """Rule 1.15.1: Counters with different names have different identities."""
    pass


# ============================================================
# Scenario: A counter on an object modifies its properties
# Tests Rule 1.15.2 - Counter modifies object properties
# ============================================================


@scenario(
    "../features/section_1_15_counters.feature",
    "A counter on an object modifies its properties",
)
def test_counter_on_object_modifies_properties():
    """Rule 1.15.2: When a counter is on an object, it modifies its properties."""
    pass


# ============================================================
# Scenario: A counter on an object can interact with effects
# Tests Rule 1.15.2 - Counter can interact with effects
# ============================================================


@scenario(
    "../features/section_1_15_counters.feature",
    "A counter on an object can interact with effects",
)
def test_counter_on_object_can_interact_with_effects():
    """Rule 1.15.2: When a counter is on an object, it can interact with effects."""
    pass


# ============================================================
# Scenario: A plus power counter increases attack power
# Tests Rule 1.15.2a - +{p} counter increases power
# ============================================================


@scenario(
    "../features/section_1_15_counters.feature",
    "A plus power counter increases attack power",
)
def test_plus_power_counter_increases_attack_power():
    """Rule 1.15.2a: A +1{p} counter increases the power of the object by 1."""
    pass


# ============================================================
# Scenario: A minus power counter decreases attack power
# Tests Rule 1.15.2a - -{p} counter decreases power
# ============================================================


@scenario(
    "../features/section_1_15_counters.feature",
    "A minus power counter decreases attack power",
)
def test_minus_power_counter_decreases_attack_power():
    """Rule 1.15.2a: A -1{p} counter decreases the power of the object by 1."""
    pass


# ============================================================
# Scenario: A plus defense counter increases defense value
# Tests Rule 1.15.2a - +{d} counter increases defense
# ============================================================


@scenario(
    "../features/section_1_15_counters.feature",
    "A plus defense counter increases defense value",
)
def test_plus_defense_counter_increases_defense_value():
    """Rule 1.15.2a: A +2{d} counter increases the defense of the object by 2."""
    pass


# ============================================================
# Scenario: Counter property modification is considered a rule not an effect
# Tests Rule 1.15.2a - Counter modification is a rule, not an effect
# ============================================================


@scenario(
    "../features/section_1_15_counters.feature",
    "Counter property modification is considered a rule not an effect",
)
def test_counter_modification_is_rule_not_effect():
    """Rule 1.15.2a: Counter property modification is considered a rule, not an effect."""
    pass


# ============================================================
# Scenario: Counter modification applies at the same time as continuous effects
# Tests Rule 1.15.2a - Counter modification timing with continuous effects
# ============================================================


@scenario(
    "../features/section_1_15_counters.feature",
    "Counter modification applies at the same time as continuous effects",
)
def test_counter_modification_applies_at_same_time_as_continuous_effects():
    """Rule 1.15.2a: Counter modification applies at the same time as continuous effects."""
    pass


# ============================================================
# Scenario: Multiple counters of the same type stack their modifications
# Tests Rule 1.15.2a - Multiple counters stack
# ============================================================


@scenario(
    "../features/section_1_15_counters.feature",
    "Multiple counters of the same type stack their modifications",
)
def test_multiple_counters_stack_modifications():
    """Rule 1.15.2a: Multiple counters of the same type stack their modifications."""
    pass


# ============================================================
# Scenario: Counters cease to exist when the object ceases to exist
# Tests Rule 1.15.3 - Counters cease with object
# ============================================================


@scenario(
    "../features/section_1_15_counters.feature",
    "Counters cease to exist when the object ceases to exist",
)
def test_counters_cease_when_object_ceases():
    """Rule 1.15.3: When an object ceases to exist, the counters on that object cease to exist."""
    pass


# ============================================================
# Scenario: Multiple counters all cease when the object ceases
# Tests Rule 1.15.3 - All counters cease with object
# ============================================================


@scenario(
    "../features/section_1_15_counters.feature",
    "Multiple counters all cease when the object ceases",
)
def test_multiple_counters_cease_when_object_ceases():
    """Rule 1.15.3: All counters cease to exist when the object ceases."""
    pass


# ============================================================
# Scenario: A removed counter ceases to exist
# Tests Rule 1.15.3 - Removed counters cease
# ============================================================


@scenario(
    "../features/section_1_15_counters.feature",
    "A removed counter ceases to exist",
)
def test_removed_counter_ceases_to_exist():
    """Rule 1.15.3: When a counter is removed from an object it ceases to exist."""
    pass


# ============================================================
# Scenario: Removing one counter leaves others intact
# Tests Rule 1.15.3 - Removing one counter doesn't affect others
# ============================================================


@scenario(
    "../features/section_1_15_counters.feature",
    "Removing one counter leaves others intact",
)
def test_removing_one_counter_leaves_others_intact():
    """Rule 1.15.3: Removing one counter leaves other counters on the object intact."""
    pass


# ============================================================
# Scenario: Opposing counters both remain on the object
# Tests Rule 1.15.4 - Opposing counters both remain
# ============================================================


@scenario(
    "../features/section_1_15_counters.feature",
    "Opposing counters both remain on the object",
)
def test_opposing_counters_both_remain():
    """Rule 1.15.4: Both diametrically opposing counters remain on the object."""
    pass


# ============================================================
# Scenario: Opposing counters do not cancel each other out
# Tests Rule 1.15.4 - Opposing counters don't cancel
# ============================================================


@scenario(
    "../features/section_1_15_counters.feature",
    "Opposing counters do not cancel each other out",
)
def test_opposing_counters_do_not_cancel():
    """Rule 1.15.4: Opposing counters do not cancel each other out."""
    pass


# ============================================================
# Scenario: Multiple opposing counter pairs all remain on the object
# Tests Rule 1.15.4 - Multiple pairs of opposing counters all remain
# ============================================================


@scenario(
    "../features/section_1_15_counters.feature",
    "Multiple opposing counter pairs all remain on the object",
)
def test_multiple_opposing_counter_pairs_all_remain():
    """Rule 1.15.4: Multiple pairs of opposing counters all remain on the object."""
    pass


# ============================================================
# Scenario: Adding a second opposing counter after first opposing already present
# Tests Rule 1.15.4 - Adding more counters to existing opposing pair
# ============================================================


@scenario(
    "../features/section_1_15_counters.feature",
    "Adding a second opposing counter after first opposing already present",
)
def test_adding_counter_when_opposing_already_present():
    """Rule 1.15.4: More counters can be added even when opposing counters already present."""
    pass


# ============================================================
# Step Definitions
# ============================================================


@given(parsers.parse('a card "{card_name}" is in the arena'))
def card_in_arena_basic(game_state, card_name):
    """Rule 1.15.1: Set up a card in the arena for counter testing."""
    card = game_state.create_arena_card(card_name)
    game_state.arena_card = card


@given(parsers.parse('a card "{card_name}" is in the arena with defense {defense:d}'))
def card_in_arena_with_defense(game_state, card_name, defense):
    """Rule 1.15.2a: Set up a card in the arena with a specific defense value."""
    card = game_state.create_arena_card(card_name, defense=defense)
    game_state.arena_card = card


@given(parsers.parse('a card "{card_name}" is in the arena with power {power:d}'))
def card_in_arena_with_power(game_state, card_name, power):
    """Rule 1.15.2a: Set up a card in the arena with a specific power value."""
    card = game_state.create_arena_card(card_name, power=power)
    game_state.arena_card = card


@given(parsers.parse('a "+1{{d}}" counter is on "{card_name}"'))
def plus_d_counter_on_card(game_state, card_name):
    """Rule 1.15.2a: Place a +1{d} counter on the card."""
    counter = game_state.create_counter(value=1, symbol="d")
    game_state.add_counter_to_card(game_state.arena_card, counter)


@given(parsers.parse('three "+1{{d}}" counters are on "{card_name}"'))
def three_plus_d_counters_on_card(game_state, card_name):
    """Rule 1.15.2a: Place three +1{d} counters on the card."""
    for _ in range(3):
        counter = game_state.create_counter(value=1, symbol="d")
        game_state.add_counter_to_card(game_state.arena_card, counter)


@given(parsers.parse('a "steam" counter is on "{card_name}"'))
def steam_counter_on_card(game_state, card_name):
    """Rule 1.15.1: Place a named steam counter on the card."""
    counter = game_state.create_named_counter("steam")
    game_state.add_counter_to_card(game_state.arena_card, counter)


@given(parsers.parse('three "steam" counters are on "{card_name}"'))
def three_steam_counters_on_card(game_state, card_name):
    """Rule 1.15.1: Place three steam counters on the card."""
    for _ in range(3):
        counter = game_state.create_named_counter("steam")
        game_state.add_counter_to_card(game_state.arena_card, counter)


@given(parsers.parse('a "+1{{p}}" counter is on "{card_name}"'))
def plus_p_counter_on_card(game_state, card_name):
    """Rule 1.15.4: Place a +1{p} counter on the card."""
    counter = game_state.create_counter(value=1, symbol="p")
    game_state.add_counter_to_card(game_state.arena_card, counter)


@given(parsers.parse('two "+1{{p}}" counters are on "{card_name}"'))
def two_plus_p_counters_on_card(game_state, card_name):
    """Rule 1.15.4: Place two +1{p} counters on the card."""
    for _ in range(2):
        counter = game_state.create_counter(value=1, symbol="p")
        game_state.add_counter_to_card(game_state.arena_card, counter)


@given(
    parsers.parse(
        'a "+1{{p}}" counter and a "-1{{p}}" counter are both on "{card_name}"'
    )
)
def both_opposing_counters_on_card(game_state, card_name):
    """Rule 1.15.4: Place both a +1{p} and -1{p} counter on the card."""
    plus_counter = game_state.create_counter(value=1, symbol="p")
    minus_counter = game_state.create_counter(value=-1, symbol="p")
    game_state.add_counter_to_card(game_state.arena_card, plus_counter)
    game_state.add_counter_to_card(game_state.arena_card, minus_counter)


@given(parsers.parse('two separate counters with name "{name}" exist on a card'))
def two_named_counters_on_card(game_state, name):
    """Rule 1.15.1: Place two separate counters with the same name on a card."""
    card = game_state.create_arena_card("Test Card")
    game_state.arena_card = card
    for _ in range(2):
        counter = game_state.create_named_counter(name)
        game_state.add_counter_to_card(card, counter)


@given(parsers.parse('an effect watches for "{counter_name}" counters on objects'))
def effect_watches_for_counters(game_state, counter_name):
    """Rule 1.15.2: Set up an effect that watches for a named counter."""
    effect_watcher = CounterWatcherEffectStub(counter_name)
    game_state.counter_watcher_effect = effect_watcher


@given(parsers.parse('a continuous effect gives "{card_name}" +2{{p}}'))
def continuous_effect_plus_power(game_state, card_name):
    """Rule 1.15.2a: Apply a continuous +2{p} effect to the card."""
    game_state.continuous_effect = ContinuousCounterEffectStub(
        target=game_state.arena_card, property_name="power", modifier=2
    )


# ============================================================
# When steps
# ============================================================


@when(parsers.parse('a "+1{{d}}" counter is added to "{card_name}"'))
def add_plus_d_counter(game_state, card_name):
    """Rule 1.15.2a: Add a +1{d} counter to the card."""
    counter = game_state.create_counter(value=1, symbol="d")
    game_state.last_added_counter = counter
    game_state.add_counter_to_card(game_state.arena_card, counter)


@when(parsers.parse('another "+1{{d}}" counter is added to "{card_name}"'))
def add_another_plus_d_counter(game_state, card_name):
    """Rule 1.15.1: Add another +1{d} counter to the card."""
    counter = game_state.create_counter(value=1, symbol="d")
    game_state.add_counter_to_card(game_state.arena_card, counter)


@when(parsers.parse('a "+2{{d}}" counter is added to "{card_name}"'))
def add_plus_2d_counter(game_state, card_name):
    """Rule 1.15.2a: Add a +2{d} counter to the card."""
    counter = game_state.create_counter(value=2, symbol="d")
    game_state.add_counter_to_card(game_state.arena_card, counter)


@when(parsers.parse('three "+1{{d}}" counters are added to "{card_name}"'))
def add_three_plus_d_counters(game_state, card_name):
    """Rule 1.15.2a: Add three +1{d} counters to the card."""
    for _ in range(3):
        counter = game_state.create_counter(value=1, symbol="d")
        game_state.add_counter_to_card(game_state.arena_card, counter)


@when(parsers.parse('a "+1{{p}}" counter is added to "{card_name}"'))
def add_plus_p_counter(game_state, card_name):
    """Rule 1.15.2a: Add a +1{p} counter to the card."""
    counter = game_state.create_counter(value=1, symbol="p")
    game_state.last_added_counter = counter
    game_state.add_counter_to_card(game_state.arena_card, counter)


@when(parsers.parse('another "+1{{p}}" counter is added to "{card_name}"'))
def add_another_plus_p_counter(game_state, card_name):
    """Rule 1.15.4: Add another +1{p} counter to the card."""
    counter = game_state.create_counter(value=1, symbol="p")
    game_state.add_counter_to_card(game_state.arena_card, counter)


@when(parsers.parse('a "-1{{p}}" counter is added to "{card_name}"'))
def add_minus_p_counter(game_state, card_name):
    """Rule 1.15.4: Add a -1{p} counter to the card."""
    counter = game_state.create_counter(value=-1, symbol="p")
    game_state.last_added_counter = counter
    result = game_state.add_counter_to_card_with_opposition_check(
        game_state.arena_card, counter
    )
    game_state.opposition_check_result = result


@when(parsers.parse('two "-1{{p}}" counters are added to "{card_name}"'))
def add_two_minus_p_counters(game_state, card_name):
    """Rule 1.15.4: Add two -1{p} counters to the card."""
    for _ in range(2):
        counter = game_state.create_counter(value=-1, symbol="p")
        game_state.add_counter_to_card_with_opposition_check(
            game_state.arena_card, counter
        )


@when(parsers.parse('a "steam" counter is added to "{card_name}"'))
def add_steam_counter_when(game_state, card_name):
    """Rule 1.15.1: Add a named steam counter to the card."""
    counter = game_state.create_named_counter("steam")
    game_state.last_added_counter = counter
    game_state.add_counter_to_card(game_state.arena_card, counter)


@when(parsers.parse('another "steam" counter is added to "{card_name}"'))
def add_another_steam_counter(game_state, card_name):
    """Rule 1.15.1: Add another steam counter to the card."""
    counter = game_state.create_named_counter("steam")
    game_state.add_counter_to_card(game_state.arena_card, counter)


@when(parsers.parse('a "rust" counter is added to "{card_name}"'))
def add_rust_counter(game_state, card_name):
    """Rule 1.15.1: Add a named rust counter to the card."""
    counter = game_state.create_named_counter("rust")
    game_state.add_counter_to_card(game_state.arena_card, counter)


@when(parsers.parse('"{card_name}" is destroyed and leaves the arena'))
def card_destroyed_and_leaves_arena(game_state, card_name):
    """Rule 1.15.3: Destroy the card and have it leave the arena."""
    result = game_state.destroy_card_in_arena(game_state.arena_card)
    game_state.destruction_result = result


@when(parsers.parse('"{card_name}" ceases to exist'))
def card_ceases_to_exist(game_state, card_name):
    """Rule 1.15.3: Have the card cease to exist."""
    result = game_state.card_ceases_to_exist(game_state.arena_card)
    game_state.cessation_result = result


@when(parsers.parse('the "steam" counter is removed from "{card_name}"'))
def steam_counter_removed(game_state, card_name):
    """Rule 1.15.3: Remove the steam counter from the card."""
    result = game_state.remove_counter_from_card(game_state.arena_card, "steam")
    game_state.removal_result = result


@when(parsers.parse('one "steam" counter is removed from "{card_name}"'))
def one_steam_counter_removed(game_state, card_name):
    """Rule 1.15.3: Remove one steam counter from the card."""
    result = game_state.remove_one_counter_from_card(game_state.arena_card, "steam")
    game_state.removal_result = result


# ============================================================
# Then steps
# ============================================================


@then(parsers.parse('"{card_name}" has {count:d} counter on it'))
def card_has_n_counters(game_state, card_name, count):
    """Rule 1.15.1: Verify the card has exactly N counters."""
    actual_count = game_state.get_counter_count(game_state.arena_card)
    assert actual_count == count, (
        f"Expected {count} counters but found {actual_count}. "
        f"Engine Feature Needed: CardInstance.counters tracking (Rule 1.15.1)"
    )


@then("the counter is a physical marker on the card")
def counter_is_physical_marker(game_state):
    """Rule 1.15.1: Verify the counter is recognized as a physical marker."""
    assert game_state.last_added_counter is not None, (
        "Engine Feature Needed: Counter class with physical marker semantics (Rule 1.15.1)"
    )
    is_physical_marker = game_state.counter_is_physical_marker(
        game_state.last_added_counter
    )
    assert is_physical_marker, (
        "Engine Feature Needed: Counter.is_physical_marker property (Rule 1.15.1)"
    )


@then("the counter is not a game object")
def counter_is_not_game_object(game_state):
    """Rule 1.15.1: Verify the counter is not a game object."""
    counter = game_state.get_counters_on_card(game_state.arena_card)[0]
    is_object = game_state.counter_is_game_object(counter)
    assert not is_object, (
        "Engine Feature Needed: Counter.is_game_object = False (Rule 1.15.1)"
    )


@then("the counter does not have properties")
def counter_does_not_have_properties(game_state):
    """Rule 1.15.1: Verify the counter does not have object properties."""
    counter = game_state.get_counters_on_card(game_state.arena_card)[0]
    has_props = game_state.counter_has_object_properties(counter)
    assert not has_props, (
        "Engine Feature Needed: Counter has no object properties (Rule 1.15.1)"
    )


@then(parsers.parse('both "{counter_name}" counters are functionally identical'))
def counters_functionally_identical(game_state, counter_name):
    """Rule 1.15.1: Verify counters with the same name are functionally identical."""
    counters = game_state.get_named_counters_on_card(
        game_state.arena_card, counter_name
    )
    assert len(counters) >= 2, (
        f"Expected at least 2 '{counter_name}' counters. "
        f"Engine Feature Needed: Counter identity by name (Rule 1.15.1)"
    )
    assert game_state.counters_are_identical(counters[0], counters[1]), (
        f"Engine Feature Needed: Counter identity equality (Rule 1.15.1)"
    )


@then(parsers.parse('"{card_name}" has {count:d} "{counter_name}" counters on it'))
def card_has_n_named_counters(game_state, card_name, count, counter_name):
    """Rule 1.15.1: Verify the card has exactly N named counters.
    Handles both named counters (e.g., 'steam') and value+symbol counters (e.g., '+1{d}').
    """
    # Try to parse as a value+symbol counter (e.g., "+1{d}" or "-1{p}")
    import re

    value_symbol_match = re.match(r"^([+-]?\d+)\{(\w+)\}$", counter_name)
    if value_symbol_match:
        value = int(value_symbol_match.group(1))
        symbol = value_symbol_match.group(2)
        actual_count = game_state.get_symbol_counter_count(
            game_state.arena_card, value=value, symbol=symbol
        )
    else:
        actual_count = game_state.get_named_counter_count(
            game_state.arena_card, counter_name
        )
    assert actual_count == count, (
        f"Expected {count} '{counter_name}' counters but found {actual_count}. "
        f"Engine Feature Needed: CardInstance.get_counters(name) (Rule 1.15.1)"
    )


@then(
    parsers.parse(
        'both "+1{{d}}" counters are functionally identical and interchangeable'
    )
)
def plus_d_counters_identical_and_interchangeable(game_state):
    """Rule 1.15.1: Verify +1{d} counters are identical and interchangeable."""
    counters = game_state.get_symbol_counters_on_card(
        game_state.arena_card, value=1, symbol="d"
    )
    assert len(counters) >= 2, (
        "Expected at least 2 +1{d} counters. "
        "Engine Feature Needed: Counter identity by value+symbol (Rule 1.15.1)"
    )
    assert game_state.counters_are_interchangeable(counters[0], counters[1]), (
        "Engine Feature Needed: Counter interchangeability check (Rule 1.15.1)"
    )


@then(parsers.parse('"{card_name}" has {count:d} "+1{{d}}" counters on it'))
def card_has_n_plus_d_counters(game_state, card_name, count):
    """Rule 1.15.1: Verify the card has exactly N +1{d} counters."""
    actual_count = game_state.get_symbol_counter_count(
        game_state.arena_card, value=1, symbol="d"
    )
    assert actual_count == count, (
        f"Expected {count} +1{{d}} counters but found {actual_count}. "
        f"Engine Feature Needed: Counter tracking by value+symbol (Rule 1.15.1)"
    )


@then(parsers.parse('the two "{counter_name}" counters are interchangeable'))
def two_named_counters_are_interchangeable(game_state, counter_name):
    """Rule 1.15.1: Verify two counters with the same name are interchangeable."""
    counters = game_state.get_named_counters_on_card(
        game_state.arena_card, counter_name
    )
    assert len(counters) >= 2, (
        f"Expected at least 2 '{counter_name}' counters. "
        f"Engine Feature Needed: Counter identity (Rule 1.15.1)"
    )
    assert game_state.counters_are_interchangeable(counters[0], counters[1]), (
        "Engine Feature Needed: Counter.is_interchangeable_with() (Rule 1.15.1)"
    )


@then(parsers.parse('"{card_name}" has 1 "steam" counter and 1 "rust" counter'))
def card_has_one_steam_and_one_rust(game_state, card_name):
    """Rule 1.15.1: Verify the card has one steam and one rust counter."""
    steam_count = game_state.get_named_counter_count(game_state.arena_card, "steam")
    rust_count = game_state.get_named_counter_count(game_state.arena_card, "rust")
    assert steam_count == 1, (
        f"Expected 1 steam counter but found {steam_count}. "
        f"Engine Feature Needed: Counter tracking by name (Rule 1.15.1)"
    )
    assert rust_count == 1, (
        f"Expected 1 rust counter but found {rust_count}. "
        f"Engine Feature Needed: Counter tracking by name (Rule 1.15.1)"
    )


@then(parsers.parse('"steam" counter and "rust" counter have different identities'))
def steam_and_rust_have_different_identities(game_state):
    """Rule 1.15.1: Verify steam and rust counters have different identities."""
    steam_counters = game_state.get_named_counters_on_card(
        game_state.arena_card, "steam"
    )
    rust_counters = game_state.get_named_counters_on_card(game_state.arena_card, "rust")
    assert len(steam_counters) > 0 and len(rust_counters) > 0, (
        "Engine Feature Needed: Counter named tracking (Rule 1.15.1)"
    )
    assert not game_state.counters_are_identical(steam_counters[0], rust_counters[0]), (
        "Engine Feature Needed: Counter identity inequality (Rule 1.15.1)"
    )


@then(parsers.parse('the effective defense of "{card_name}" is {expected:d}'))
def effective_defense_equals(game_state, card_name, expected):
    """Rule 1.15.2a: Verify the effective defense value including counter modifications."""
    actual = game_state.get_effective_defense(game_state.arena_card)
    assert actual == expected, (
        f"Expected effective defense {expected} but got {actual}. "
        f"Engine Feature Needed: CardInstance.effective_defense with counter mods (Rule 1.15.2a)"
    )


@then(parsers.parse('the effective power of "{card_name}" is {expected:d}'))
def effective_power_equals(game_state, card_name, expected):
    """Rule 1.15.2a: Verify the effective power value including counter modifications."""
    actual = game_state.get_effective_power(game_state.arena_card)
    assert actual == expected, (
        f"Expected effective power {expected} but got {actual}. "
        f"Engine Feature Needed: CardInstance.effective_power with counter mods (Rule 1.15.2a)"
    )


@then(parsers.parse('the effect detects the "{counter_name}" counter on "{card_name}"'))
def effect_detects_counter(game_state, counter_name, card_name):
    """Rule 1.15.2: Verify the effect detected the named counter."""
    detected = game_state.counter_watcher_effect.detected_counter_on_card(
        game_state.arena_card, counter_name
    )
    assert detected, (
        f"Effect did not detect '{counter_name}' counter. "
        f"Engine Feature Needed: Counter interaction with effects (Rule 1.15.2)"
    )


@then(
    parsers.parse(
        'the "+1{{d}}" counter modification is classified as a rule modification'
    )
)
def counter_modification_is_rule(game_state):
    """Rule 1.15.2a: Verify counter modification is classified as a rule, not an effect."""
    mod_type = game_state.get_counter_modification_type(game_state.arena_card)
    assert mod_type == "rule", (
        f"Expected modification type 'rule' but got '{mod_type}'. "
        f"Engine Feature Needed: Counter modification classified as rule (Rule 1.15.2a)"
    )


@then("the modification is not classified as an effect")
def modification_not_effect(game_state):
    """Rule 1.15.2a: Verify counter modification is NOT classified as an effect."""
    mod_type = game_state.get_counter_modification_type(game_state.arena_card)
    assert mod_type != "effect", (
        "Counter modification was incorrectly classified as an effect. "
        "Engine Feature Needed: Counter modification is a rule (Rule 1.15.2a)"
    )


@then("the counter modification applies at the same layer as the continuous effect")
def counter_mod_same_layer_as_effect(game_state):
    """Rule 1.15.2a: Verify counter modification and continuous effects are at same timing layer."""
    timing_layer = game_state.get_counter_modification_timing_layer(
        game_state.arena_card
    )
    effect_timing_layer = game_state.get_effect_timing_layer(
        game_state.continuous_effect
    )
    assert timing_layer == effect_timing_layer, (
        f"Counter timing layer ({timing_layer}) != effect timing layer ({effect_timing_layer}). "
        f"Engine Feature Needed: Counter mod at same timing layer as continuous effects (Rule 1.15.2a)"
    )


@then(parsers.parse('the "+1{{d}}" counter on "{card_name}" ceases to exist'))
def counter_ceases_with_card(game_state, card_name):
    """Rule 1.15.3: Verify the counter ceased when the card was destroyed."""
    counter_ceased = game_state.did_counters_cease_with_object(game_state.arena_card)
    assert counter_ceased, (
        "Engine Feature Needed: Counters cease when object ceases (Rule 1.15.3)"
    )


@then(parsers.parse('all counters on "{card_name}" cease to exist'))
def all_counters_cease_with_card(game_state, card_name):
    """Rule 1.15.3: Verify all counters ceased when the card ceased to exist."""
    counters_ceased = game_state.did_all_counters_cease_with_object(
        game_state.arena_card
    )
    assert counters_ceased, (
        "Engine Feature Needed: All counters cease when object ceases (Rule 1.15.3)"
    )


@then('the removed "steam" counter ceases to exist')
def removed_steam_counter_ceases(game_state):
    """Rule 1.15.3: Verify the removed counter ceased to exist."""
    ceased = game_state.removal_result.counter_ceased
    assert ceased, (
        "Engine Feature Needed: Removed counter ceases to exist (Rule 1.15.3)"
    )


@then(parsers.parse('"{card_name}" has 0 counters on it'))
def card_has_no_counters(game_state, card_name):
    """Rule 1.15.3: Verify the card has no counters remaining."""
    count = game_state.get_counter_count(game_state.arena_card)
    assert count == 0, (
        f"Expected 0 counters but found {count}. "
        f"Engine Feature Needed: Counter removal tracking (Rule 1.15.3)"
    )


@then(parsers.parse('"{card_name}" still has {count:d} "steam" counters on it'))
def card_still_has_n_steam_counters(game_state, card_name, count):
    """Rule 1.15.3: Verify the card still has the correct number of steam counters."""
    actual = game_state.get_named_counter_count(game_state.arena_card, "steam")
    assert actual == count, (
        f"Expected {count} remaining steam counters but found {actual}. "
        f"Engine Feature Needed: Counter removal leaves others intact (Rule 1.15.3)"
    )


@then(
    parsers.parse(
        '"{card_name}" has both a "+1{{p}}" counter and a "-1{{p}}" counter on it'
    )
)
def card_has_both_opposing_counters(game_state, card_name):
    """Rule 1.15.4: Verify the card has both a +1{p} and a -1{p} counter."""
    plus_count = game_state.get_symbol_counter_count(
        game_state.arena_card, value=1, symbol="p"
    )
    minus_count = game_state.get_symbol_counter_count(
        game_state.arena_card, value=-1, symbol="p"
    )
    assert plus_count >= 1, (
        f"Expected at least 1 '+1{{p}}' counter but found {plus_count}. "
        f"Engine Feature Needed: Opposing counter preservation (Rule 1.15.4)"
    )
    assert minus_count >= 1, (
        f"Expected at least 1 '-1{{p}}' counter but found {minus_count}. "
        f"Engine Feature Needed: Opposing counter preservation (Rule 1.15.4)"
    )


@then("neither counter is removed")
def neither_counter_removed(game_state):
    """Rule 1.15.4: Verify neither opposing counter was removed."""
    opposition_result = game_state.opposition_check_result
    assert not opposition_result.counter_was_removed, (
        "Engine Feature Needed: Opposing counters are not removed (Rule 1.15.4)"
    )


@then(parsers.parse('"{card_name}" still has both opposing counters'))
def card_still_has_both_opposing_counters(game_state, card_name):
    """Rule 1.15.4: Verify both opposing counters remain after net-zero."""
    plus_count = game_state.get_symbol_counter_count(
        game_state.arena_card, value=1, symbol="p"
    )
    minus_count = game_state.get_symbol_counter_count(
        game_state.arena_card, value=-1, symbol="p"
    )
    assert plus_count >= 1 and minus_count >= 1, (
        f"Expected both opposing counters to remain. +1{{p}}={plus_count}, -1{{p}}={minus_count}. "
        f"Engine Feature Needed: Opposing counters both remain (Rule 1.15.4)"
    )


@then(
    parsers.parse(
        '"{card_name}" has {plus_count:d} "+1{{p}}" counters and {minus_count:d} "-1{{p}}" counters on it'
    )
)
def card_has_multiple_opposing_counter_counts(
    game_state, card_name, plus_count, minus_count
):
    """Rule 1.15.4: Verify the card has the correct count of each opposing counter."""
    actual_plus = game_state.get_symbol_counter_count(
        game_state.arena_card, value=1, symbol="p"
    )
    actual_minus = game_state.get_symbol_counter_count(
        game_state.arena_card, value=-1, symbol="p"
    )
    assert actual_plus == plus_count, (
        f"Expected {plus_count} '+1{{p}}' counters but found {actual_plus}. "
        f"Engine Feature Needed: Multi-opposing counter tracking (Rule 1.15.4)"
    )
    assert actual_minus == minus_count, (
        f"Expected {minus_count} '-1{{p}}' counters but found {actual_minus}. "
        f"Engine Feature Needed: Multi-opposing counter tracking (Rule 1.15.4)"
    )


# ============================================================
# Stub classes for counter tests
# ============================================================


@dataclass
class CounterStub:
    """
    Stub representing a counter.

    Engine Feature Needed: Counter class (Rule 1.15.1)
    """

    name: Optional[str] = None  # Named counter (e.g., "steam")
    value: Optional[int] = None  # Numeric counter value (e.g., +1, -1)
    symbol: Optional[str] = None  # Symbol (e.g., "p" for power, "d" for defense)

    @property
    def is_game_object(self) -> bool:
        """Rule 1.15.1: A counter is not a game object."""
        return False

    @property
    def is_physical_marker(self) -> bool:
        """Rule 1.15.1: A counter is a physical marker."""
        return True

    @property
    def has_object_properties(self) -> bool:
        """Rule 1.15.1: A counter does not have object properties."""
        return False

    @property
    def identity(self) -> str:
        """Rule 1.15.1: Counter identity defined by name or value+symbol."""
        if self.name is not None:
            return self.name
        return f"{'+' if self.value and self.value > 0 else ''}{self.value}{{{self.symbol}}}"

    def is_opposing_to(self, other: "CounterStub") -> bool:
        """Check if this counter is diametrically opposing to another counter."""
        if self.symbol is None or other.symbol is None:
            return False
        if self.symbol != other.symbol:
            return False
        # Opposing means same symbol but opposite signs
        if self.value is None or other.value is None:
            return False
        return (self.value > 0 and other.value < 0) or (
            self.value < 0 and other.value > 0
        )


@dataclass
class CounterRemovalResultStub:
    """Result of removing a counter from an object."""

    counter_ceased: bool = True
    success: bool = True


@dataclass
class CounterOppositionResultStub:
    """Result of checking opposition when adding a counter."""

    counter_was_removed: bool = False
    both_counters_remain: bool = True


@dataclass
class ContinuousCounterEffectStub:
    """
    Stub for a continuous effect that modifies an object's properties.

    Engine Feature Needed: ContinuousEffect class (Rule 1.8.2)
    """

    target: Any
    property_name: str
    modifier: int
    timing_layer: str = "continuous_effect_layer"


@dataclass
class CounterWatcherEffectStub:
    """
    Stub for an effect that watches for named counters on objects.

    Engine Feature Needed: Counter interaction with effects (Rule 1.15.2)
    """

    watched_counter_name: str
    detected_counters: List[Any] = field(default_factory=list)

    def detected_counter_on_card(self, card: Any, counter_name: str) -> bool:
        """Rule 1.15.2: Check if effect detected the counter."""
        return any(c.name == counter_name for c in self.detected_counters)


# ============================================================
# Fixture
# ============================================================


@pytest.fixture
def game_state():
    """
    Fixture providing game state for testing Section 1.15: Counters.

    Uses BDDGameState and extends it with counter-specific helpers.
    Reference: Rule 1.15
    """
    from tests.bdd_helpers import BDDGameState

    state = BDDGameState()

    # Track cards for counter tests
    state.arena_card = None
    state.last_added_counter = None
    state.destruction_result = None
    state.cessation_result = None
    state.removal_result = None
    state.opposition_check_result = None
    state.counter_watcher_effect = None
    state.continuous_effect = None

    # Counter storage: card -> list of CounterStub objects
    state._counters_on_cards = {}
    # Track ceased counters (from destroyed objects)
    state._ceased_counters = []

    def create_arena_card(name: str, defense: int = 0, power: int = 0):
        """Create a card with specified stats, placed in arena."""
        card = state.create_card(name)
        card._base_defense = defense
        card._base_power = power
        card._is_in_arena = True
        state._counters_on_cards[id(card)] = []
        return card

    def create_counter(value: int, symbol: str) -> CounterStub:
        """Rule 1.15.1: Create a numeric+symbol counter."""
        return CounterStub(value=value, symbol=symbol)

    def create_named_counter(name: str) -> CounterStub:
        """Rule 1.15.1: Create a named counter."""
        return CounterStub(name=name)

    def add_counter_to_card(card, counter: CounterStub):
        """Rule 1.15.2: Add a counter to a card."""
        if id(card) not in state._counters_on_cards:
            state._counters_on_cards[id(card)] = []
        state._counters_on_cards[id(card)].append(counter)

        # If watcher effect is active and counter name matches, detect it
        if (
            state.counter_watcher_effect
            and counter.name == state.counter_watcher_effect.watched_counter_name
        ):
            state.counter_watcher_effect.detected_counters.append(counter)

    def add_counter_to_card_with_opposition_check(
        card, counter: CounterStub
    ) -> CounterOppositionResultStub:
        """
        Rule 1.15.4: Add a counter to a card, keeping opposing counters.
        Both diametrically opposing counters remain - no cancellation.
        """
        if id(card) not in state._counters_on_cards:
            state._counters_on_cards[id(card)] = []
        # Rule 1.15.4: Just add the counter - no cancellation occurs
        state._counters_on_cards[id(card)].append(counter)
        return CounterOppositionResultStub(
            counter_was_removed=False, both_counters_remain=True
        )

    def get_counter_count(card) -> int:
        """Rule 1.15.1: Get total number of counters on a card."""
        return len(state._counters_on_cards.get(id(card), []))

    def get_named_counter_count(card, name: str) -> int:
        """Rule 1.15.1: Get count of counters with a specific name."""
        return sum(
            1 for c in state._counters_on_cards.get(id(card), []) if c.name == name
        )

    def get_named_counters_on_card(card, name: str) -> List[CounterStub]:
        """Rule 1.15.1: Get all counters with a specific name on a card."""
        return [c for c in state._counters_on_cards.get(id(card), []) if c.name == name]

    def get_counters_on_card(card) -> List[CounterStub]:
        """Rule 1.15.1: Get all counters on a card."""
        return list(state._counters_on_cards.get(id(card), []))

    def get_symbol_counters_on_card(card, value: int, symbol: str) -> List[CounterStub]:
        """Rule 1.15.1: Get all counters with a specific value+symbol on a card."""
        return [
            c
            for c in state._counters_on_cards.get(id(card), [])
            if c.value == value and c.symbol == symbol
        ]

    def get_symbol_counter_count(card, value: int, symbol: str) -> int:
        """Rule 1.15.1: Get count of counters with a specific value+symbol on a card."""
        return len(get_symbol_counters_on_card(card, value, symbol))

    def counters_are_identical(c1: CounterStub, c2: CounterStub) -> bool:
        """Rule 1.15.1: Check if two counters are functionally identical."""
        return c1.identity == c2.identity

    def counters_are_interchangeable(c1: CounterStub, c2: CounterStub) -> bool:
        """Rule 1.15.1: Check if two counters are interchangeable."""
        return counters_are_identical(c1, c2)

    def counter_is_physical_marker(counter: CounterStub) -> bool:
        """Rule 1.15.1: Check if counter is a physical marker."""
        return counter.is_physical_marker

    def counter_is_game_object(counter: CounterStub) -> bool:
        """Rule 1.15.1: Check if counter is a game object (should be False)."""
        return counter.is_game_object

    def counter_has_object_properties(counter: CounterStub) -> bool:
        """Rule 1.15.1: Check if counter has object properties (should be False)."""
        return counter.has_object_properties

    def get_effective_defense(card) -> int:
        """
        Rule 1.15.2a: Get effective defense including counter modifications.

        Engine Feature Needed: CardInstance.effective_defense (Rule 1.15.2a)
        """
        base = getattr(card, "_base_defense", 0)
        counter_mod = sum(
            c.value
            for c in state._counters_on_cards.get(id(card), [])
            if c.symbol == "d" and c.value is not None
        )
        return base + counter_mod

    def get_effective_power(card) -> int:
        """
        Rule 1.15.2a: Get effective power including counter modifications and effects.

        Engine Feature Needed: CardInstance.effective_power (Rule 1.15.2a)
        """
        base = getattr(card, "_base_power", 0)
        counter_mod = sum(
            c.value
            for c in state._counters_on_cards.get(id(card), [])
            if c.symbol == "p" and c.value is not None
        )
        effect_mod = 0
        if state.continuous_effect and state.continuous_effect.target is card:
            if state.continuous_effect.property_name == "power":
                effect_mod = state.continuous_effect.modifier
        return base + counter_mod + effect_mod

    def get_counter_modification_type(card) -> str:
        """
        Rule 1.15.2a: Get the classification of counter modifications.

        Engine Feature Needed: Counter modification classified as 'rule' not 'effect' (Rule 1.15.2a)
        """
        # Rule 1.15.2a: Counter modifications are classified as rules
        counters = state._counters_on_cards.get(id(card), [])
        numeric_counters = [
            c for c in counters if c.value is not None and c.symbol is not None
        ]
        if numeric_counters:
            return "rule"
        return "none"

    def get_counter_modification_timing_layer(card) -> str:
        """
        Rule 1.15.2a: Get the timing layer for counter modifications.

        Engine Feature Needed: Counter modification timing (Rule 1.15.2a)
        """
        # Rule 1.15.2a: Counter modifications are at the same timing layer as continuous effects
        return "continuous_effect_layer"

    def get_effect_timing_layer(effect: ContinuousCounterEffectStub) -> str:
        """Rule 1.15.2a: Get the timing layer for a continuous effect."""
        return effect.timing_layer

    def destroy_card_in_arena(card) -> dict:
        """
        Rule 1.15.3: Destroy the card in arena, causing counters to cease.

        Engine Feature Needed: Counters cease when object ceases (Rule 1.15.3)
        """
        counters_before = list(state._counters_on_cards.get(id(card), []))
        state._ceased_counters.extend(counters_before)
        state._counters_on_cards[id(card)] = []
        card._is_in_arena = False
        card._has_ceased = True
        return {"counters_ceased": True, "card_destroyed": True}

    def card_ceases_to_exist(card) -> dict:
        """
        Rule 1.15.3: Have the card cease to exist, causing all counters to cease.

        Engine Feature Needed: Counters cease when object ceases (Rule 1.15.3)
        """
        return destroy_card_in_arena(card)

    def did_counters_cease_with_object(card) -> bool:
        """Rule 1.15.3: Check if counters ceased when the card was destroyed."""
        return (
            getattr(card, "_has_ceased", False)
            and len(state._counters_on_cards.get(id(card), [])) == 0
        )

    def did_all_counters_cease_with_object(card) -> bool:
        """Rule 1.15.3: Check if all counters ceased when the card ceased."""
        return did_counters_cease_with_object(card)

    def remove_counter_from_card(card, name: str) -> CounterRemovalResultStub:
        """
        Rule 1.15.3: Remove a named counter from a card.

        Engine Feature Needed: Counter removal (Rule 1.15.3)
        """
        counters = state._counters_on_cards.get(id(card), [])
        for i, c in enumerate(counters):
            if c.name == name:
                removed = counters.pop(i)
                state._ceased_counters.append(removed)
                return CounterRemovalResultStub(counter_ceased=True, success=True)
        return CounterRemovalResultStub(counter_ceased=False, success=False)

    def remove_one_counter_from_card(card, name: str) -> CounterRemovalResultStub:
        """Rule 1.15.3: Remove one named counter from a card (alias for remove_counter_from_card)."""
        return remove_counter_from_card(card, name)

    # Attach methods to the game state
    state.create_arena_card = create_arena_card
    state.create_counter = create_counter
    state.create_named_counter = create_named_counter
    state.add_counter_to_card = add_counter_to_card
    state.add_counter_to_card_with_opposition_check = (
        add_counter_to_card_with_opposition_check
    )
    state.get_counter_count = get_counter_count
    state.get_named_counter_count = get_named_counter_count
    state.get_named_counters_on_card = get_named_counters_on_card
    state.get_counters_on_card = get_counters_on_card
    state.get_symbol_counters_on_card = get_symbol_counters_on_card
    state.get_symbol_counter_count = get_symbol_counter_count
    state.counters_are_identical = counters_are_identical
    state.counters_are_interchangeable = counters_are_interchangeable
    state.counter_is_physical_marker = counter_is_physical_marker
    state.counter_is_game_object = counter_is_game_object
    state.counter_has_object_properties = counter_has_object_properties
    state.get_effective_defense = get_effective_defense
    state.get_effective_power = get_effective_power
    state.get_counter_modification_type = get_counter_modification_type
    state.get_counter_modification_timing_layer = get_counter_modification_timing_layer
    state.get_effect_timing_layer = get_effect_timing_layer
    state.destroy_card_in_arena = destroy_card_in_arena
    state.card_ceases_to_exist = card_ceases_to_exist
    state.did_counters_cease_with_object = did_counters_cease_with_object
    state.did_all_counters_cease_with_object = did_all_counters_cease_with_object
    state.remove_counter_from_card = remove_counter_from_card
    state.remove_one_counter_from_card = remove_one_counter_from_card

    return state
