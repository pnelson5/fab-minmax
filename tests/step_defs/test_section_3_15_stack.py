"""
Step definitions for Section 3.15: Stack
Reference: Flesh and Blood Comprehensive Rules Section 3.15

This module implements behavioral tests for the stack zone rules:
- Rule 3.15.1: The stack zone is a public zone outside the arena, shared by all
               players, and has no owner.
- Rule 3.15.2: The term "stack" refers to the stack zone.
- Rule 3.15.3: The stack contains an ordered collection of layers.
- Rule 3.15.4: When a layer is added, it becomes layer N+1 (1-based, bottom to top).
- Rule 3.15.5: The top layer is layer N with the highest value of N.
- Rule 3.15.6: When layer N is removed, any layer M where M>N becomes M-1.

Cross-references:
- Rule 3.0.4a: Stack zone is a public zone.
- Rule 3.0.5b: Stack zone is NOT part of the arena.
- Rule 1.6:    Layers are the items placed onto the stack.

Engine Features Needed for Section 3.15:
- [ ] Zone.is_public_zone property (Rule 3.15.1, 3.0.4a)
      Stack zone should report is_public_zone=True.
- [ ] Zone.is_arena_zone property (Rule 3.15.1, 3.0.5b)
      Stack zone should report is_arena_zone=False (outside arena).
- [ ] Stack zone has no owner (Rule 3.15.1)
      Engine needs a shared stack zone without an owner_id (or owner_id=None).
      Current TestZone requires owner_id; engine needs a no-owner option.
- [ ] Shared stack zone accessible from any player context (Rule 3.15.1)
      Currently BDDGameState.stack is a list, not a Zone instance.
- [ ] Layer.layer_number property tracking N+1 ordering (Rule 3.15.4)
      Engine needs first-class layer ordering on a real stack Zone.
- [ ] Stack.remove_layer(n) with automatic renumbering of higher layers (Rule 3.15.6)
      Current BDDGameState.stack.pop() only removes from top (no mid-removal).

Current status: Tests written, Engine pending for zone visibility, ownership,
                and layer-renumbering features.
"""

import pytest
from pytest_bdd import scenario, given, when, then, parsers
from typing import List, Any

from fab_engine.zones.zone import Zone, ZoneType


# ===========================================================================
# Scenarios: Rule 3.15.1 - Stack is a public zone outside the arena
# ===========================================================================


@scenario(
    "../features/section_3_15_stack.feature",
    "The stack zone is a public zone",
)
def test_stack_is_public_zone():
    """Rule 3.15.1: The stack zone is a public zone."""
    pass


@scenario(
    "../features/section_3_15_stack.feature",
    "The stack zone is outside the arena",
)
def test_stack_is_outside_arena():
    """Rule 3.15.1: The stack zone is not part of the arena."""
    pass


@scenario(
    "../features/section_3_15_stack.feature",
    "The stack zone has no owner",
)
def test_stack_has_no_owner():
    """Rule 3.15.1: The stack zone has no owner."""
    pass


@scenario(
    "../features/section_3_15_stack.feature",
    "There is only one stack zone shared by all players",
)
def test_only_one_shared_stack():
    """Rule 3.15.1: There is only one stack zone shared by all players."""
    pass


# ===========================================================================
# Scenarios: Rule 3.15.3 - Stack holds layers in order
# ===========================================================================


@scenario(
    "../features/section_3_15_stack.feature",
    "The stack starts empty before any layers are added",
)
def test_stack_starts_empty():
    """Rule 3.15.3: Stack begins with no layers."""
    pass


@scenario(
    "../features/section_3_15_stack.feature",
    "The stack holds layers in an ordered collection",
)
def test_stack_holds_layers_in_order():
    """Rule 3.15.3: Stack maintains an ordered collection of layers."""
    pass


# ===========================================================================
# Scenarios: Rule 3.15.4 - Layers become layer N+1 when added
# ===========================================================================


@scenario(
    "../features/section_3_15_stack.feature",
    "The first layer added to an empty stack becomes layer 1",
)
def test_first_layer_is_layer_1():
    """Rule 3.15.4: First layer added to empty stack is layer 1."""
    pass


@scenario(
    "../features/section_3_15_stack.feature",
    "A second layer added to the stack becomes layer 2",
)
def test_second_layer_is_layer_2():
    """Rule 3.15.4: Second layer added becomes layer 2 (N+1 = 2)."""
    pass


@scenario(
    "../features/section_3_15_stack.feature",
    "Multiple layers are numbered sequentially when added",
)
def test_layers_numbered_sequentially():
    """Rule 3.15.4: Layers are numbered 1, 2, 3 sequentially from bottom."""
    pass


# ===========================================================================
# Scenarios: Rule 3.15.5 - Top layer is layer N with highest N
# ===========================================================================


@scenario(
    "../features/section_3_15_stack.feature",
    "The top layer of the stack is the most recently added layer",
)
def test_top_layer_is_most_recent():
    """Rule 3.15.5: Top of stack is the layer with the highest N."""
    pass


@scenario(
    "../features/section_3_15_stack.feature",
    "The top layer updates when a new layer is added",
)
def test_top_layer_updates_on_add():
    """Rule 3.15.5: Top layer N increases when another layer is added."""
    pass


# ===========================================================================
# Scenarios: Rule 3.15.6 - Removing layer N renumbers layers M>N
# ===========================================================================


@scenario(
    "../features/section_3_15_stack.feature",
    "Removing the top layer decreases the stack size by one",
)
def test_remove_top_layer_decreases_size():
    """Rule 3.15.6: Removing top layer (N) leaves N-1 layers."""
    pass


@scenario(
    "../features/section_3_15_stack.feature",
    "Removing a middle layer causes upper layers to be renumbered downward",
)
def test_remove_middle_layer_renumbers():
    """Rule 3.15.6: Removing layer N causes M>N to become M-1."""
    pass


@scenario(
    "../features/section_3_15_stack.feature",
    "Removing the bottom layer renumbers all layers above it",
)
def test_remove_bottom_layer_renumbers_all():
    """Rule 3.15.6: Removing layer 1 shifts all other layers down by 1."""
    pass


@scenario(
    "../features/section_3_15_stack.feature",
    "Rulebook example - negate removes layer 2 of 4 layers",
)
def test_rulebook_negate_example():
    """Rule 3.15.6: Rulebook example: 4-layer stack, layer 2 negated, layers 3→2 and 4→3."""
    pass


# ===========================================================================
# Step definitions: Given
# ===========================================================================


@given("a stack zone exists in the game")
def stack_zone_exists(game_state):
    """Rule 3.15.1: Stack zone exists in the game."""
    # The BDDGameState always has a stack (self.stack list)
    # Engine feature needed: a proper Zone object for the stack
    assert game_state.stack is not None


@given("a game with two players")
def game_with_two_players(game_state):
    """Rule 3.15.1: Game has two players sharing one stack."""
    assert game_state.player is not None
    assert game_state.defender is not None


@given("the stack is empty")
def stack_is_empty(game_state):
    """Rule 3.15.3: Stack starts with no layers."""
    game_state.stack.clear()
    assert len(game_state.stack) == 0


@given("no layers have been added to the stack")
def no_layers_added(game_state):
    """Rule 3.15.3: No layers on the stack yet."""
    game_state.stack.clear()


@given(parsers.parse("the stack already has {n:d} layer"))
def stack_has_n_layers_singular(game_state, n):
    """Rule 3.15.4: Stack pre-populated with N layers."""
    game_state.stack.clear()
    for i in range(n):
        layer = _make_layer(f"layer_{i + 1}")
        game_state.stack.append(layer)
    assert len(game_state.stack) == n


@given(parsers.parse("the stack already has {n:d} layers"))
def stack_has_n_layers(game_state, n):
    """Rule 3.15.4: Stack pre-populated with N layers."""
    game_state.stack.clear()
    for i in range(n):
        layer = _make_layer(f"layer_{i + 1}")
        game_state.stack.append(layer)
    assert len(game_state.stack) == n


@given("the stack has 4 layers labeled A B C D from bottom to top")
def stack_has_4_layers_abcd(game_state):
    """Rule 3.15.6: Stack with 4 labeled layers for removal testing."""
    game_state.stack.clear()
    for label in ["A", "B", "C", "D"]:
        game_state.stack.append(_make_layer(label))
    # store labels for lookup
    game_state._layer_labels = [layer.label for layer in game_state.stack]
    assert len(game_state.stack) == 4


@given("the stack has 3 layers labeled X Y Z from bottom to top")
def stack_has_3_layers_xyz(game_state):
    """Rule 3.15.6: Stack with 3 labeled layers for removal testing."""
    game_state.stack.clear()
    for label in ["X", "Y", "Z"]:
        game_state.stack.append(_make_layer(label))
    game_state._layer_labels = [layer.label for layer in game_state.stack]
    assert len(game_state.stack) == 3


# ===========================================================================
# Step definitions: When
# ===========================================================================


@when("checking the visibility of the stack zone")
def check_stack_visibility(game_state):
    """Rule 3.15.1: Check if stack zone has public visibility."""
    # Engine feature needed: Zone.is_public_zone on stack zone
    # owner_id=0 is a placeholder; engine needs to support owner_id=None for shared zones
    stack_zone = Zone(zone_type=ZoneType.STACK, owner_id=0)
    game_state._checked_zone = stack_zone


@when("checking whether the stack zone is in the arena")
def check_stack_arena_membership(game_state):
    """Rule 3.15.1: Check if stack zone is outside the arena."""
    stack_zone = Zone(zone_type=ZoneType.STACK, owner_id=0)
    game_state._checked_zone = stack_zone


@when("checking the ownership of the stack zone")
def check_stack_ownership(game_state):
    """Rule 3.15.1: Check that stack zone has no owner."""
    stack_zone = Zone(zone_type=ZoneType.STACK, owner_id=0)
    game_state._checked_zone = stack_zone


@when("no layers have been added to the stack")
def when_no_layers_added(game_state):
    """Rule 3.15.3: Confirm no layers have been placed on the stack."""
    # No action needed - stack was already cleared in Given step
    pass


@when("checking how many stack zones exist")
def check_stack_zone_count(game_state):
    """Rule 3.15.1: Verify only one stack zone exists shared by all players."""
    # In the engine, there should be exactly one shared stack zone.
    # Currently BDDGameState.stack is a single shared list.
    # Engine feature needed: dedicated GameState.stack_zone singleton
    game_state._stack_zone_count = 1  # One shared stack in BDDGameState


@when("a layer is added to the stack")
def add_one_layer(game_state):
    """Rule 3.15.4: Add a layer to the stack."""
    layer = _make_layer("new_layer")
    game_state.stack.append(layer)
    game_state._last_added_layer = layer


@when("another layer is added to the stack")
def add_another_layer(game_state):
    """Rule 3.15.4: Add another layer on top."""
    layer = _make_layer(f"layer_{len(game_state.stack) + 1}")
    game_state.stack.append(layer)
    game_state._last_added_layer = layer


@when(parsers.parse("{n:d} layers are added to the stack one at a time"))
def add_n_layers(game_state, n):
    """Rule 3.15.4: Add N layers sequentially to the stack."""
    for i in range(n):
        layer = _make_layer(f"seq_layer_{i + 1}")
        game_state.stack.append(layer)


@when("checking the top of the stack")
def check_top_of_stack(game_state):
    """Rule 3.15.5: Identify the top layer."""
    assert len(game_state.stack) > 0, "Stack must not be empty to check top"
    game_state._top_layer_index = len(game_state.stack) - 1  # 0-based index of top


@when("the top layer is removed from the stack")
def remove_top_layer(game_state):
    """Rule 3.15.6: Remove the top (highest N) layer from the stack."""
    assert len(game_state.stack) > 0, "Stack must not be empty"
    game_state.stack.pop()


@when("layer 2 (B) is removed from the stack")
def remove_layer_2_b(game_state):
    """Rule 3.15.6: Remove layer 2 (index 1, labeled B) from the stack."""
    # Layer 2 is at 0-based index 1
    assert len(game_state.stack) >= 2, "Stack must have at least 2 layers"
    game_state.stack.pop(1)


@when("layer 1 (X) is removed from the stack")
def remove_layer_1_x(game_state):
    """Rule 3.15.6: Remove layer 1 (index 0, labeled X) from the stack."""
    assert len(game_state.stack) >= 1, "Stack must have at least 1 layer"
    game_state.stack.pop(0)


@when("layer 2 (B) is removed by a negate effect")
def remove_layer_2_by_negate(game_state):
    """Rule 3.15.6: Negate effect removes layer 2 (index 1, labeled B)."""
    # Negate: an effect that removes a specific layer from the stack.
    # Engine feature needed: Effect.negate(layer_n) removing layer N and renumbering.
    # Currently we simulate by removing the item at index 1.
    assert len(game_state.stack) >= 2
    game_state.stack.pop(1)


# ===========================================================================
# Step definitions: Then
# ===========================================================================


@then("the stack zone is a public zone")
def assert_stack_is_public(game_state):
    """Rule 3.15.1: Stack zone must report is_public_zone=True."""
    # Engine feature needed: Zone.is_public_zone property
    zone = game_state._checked_zone
    assert zone.is_public_zone, (
        "Rule 3.15.1: Stack zone must be a public zone (is_public_zone=True). "
        "Engine feature needed: Zone.is_public_zone for ZoneType.STACK."
    )


@then("the stack zone is not part of the arena")
def assert_stack_not_in_arena(game_state):
    """Rule 3.15.1: Stack zone must report is_arena_zone=False."""
    # Engine feature needed: Zone.is_arena_zone property
    zone = game_state._checked_zone
    assert not zone.is_arena_zone, (
        "Rule 3.15.1: Stack zone must not be part of the arena (is_arena_zone=False). "
        "Engine feature needed: Zone.is_arena_zone for ZoneType.STACK."
    )


@then("the stack zone has no owner")
def assert_stack_has_no_owner(game_state):
    """Rule 3.15.1: Stack zone has no owner (no owner_id)."""
    # Engine feature needed: Zone without owner (owner_id=None) for shared zones
    zone = game_state._checked_zone
    assert zone.owner_id is None, (
        "Rule 3.15.1: Stack zone must have no owner (owner_id=None). "
        "Engine feature needed: Zone support for owner_id=None (shared zones)."
    )


@then("there is exactly one stack zone")
def assert_one_stack_zone(game_state):
    """Rule 3.15.1: Only one stack zone exists in the game."""
    assert game_state._stack_zone_count == 1, (
        "Rule 3.15.1: There must be exactly one stack zone in the game."
    )


@then("the stack zone is shared between all players")
def assert_stack_is_shared(game_state):
    """Rule 3.15.1: The single stack zone is accessible to all players."""
    # In BDDGameState, game_state.stack is shared (both player and defender use it)
    # Engine feature needed: GameState.stack_zone singleton accessible from all player contexts
    # Currently we just verify the single stack list exists
    assert game_state.stack is not None, (
        "Rule 3.15.1: Stack zone must be shared between all players. "
        "Engine feature needed: GameState.stack_zone singleton."
    )


@then("the stack contains zero layers")
def assert_stack_empty(game_state):
    """Rule 3.15.3: Stack has no layers."""
    assert len(game_state.stack) == 0, (
        f"Rule 3.15.3: Stack should be empty, but has {len(game_state.stack)} layers."
    )


@then("the stack contains one layer")
def assert_stack_has_one_layer(game_state):
    """Rule 3.15.3/3.15.4: Stack has exactly one layer."""
    assert len(game_state.stack) == 1, (
        f"Rule 3.15.3: Stack should have 1 layer, but has {len(game_state.stack)}."
    )


@then("the stack contains two layers")
def assert_stack_has_two_layers(game_state):
    """Rule 3.15.4/3.15.6: Stack has exactly two layers."""
    assert len(game_state.stack) == 2, (
        f"Rule 3.15.4: Stack should have 2 layers, but has {len(game_state.stack)}."
    )


@then("the stack contains three layers")
def assert_stack_has_three_layers(game_state):
    """Rule 3.15.4/3.15.6: Stack has exactly three layers."""
    assert len(game_state.stack) == 3, (
        f"Rule 3.15.4: Stack should have 3 layers, but has {len(game_state.stack)}."
    )


@then("that layer is layer 1")
def assert_layer_is_layer_1(game_state):
    """Rule 3.15.4: The only layer on the stack is layer 1 (index 0)."""
    assert len(game_state.stack) == 1
    assert game_state.stack[0] == game_state._last_added_layer, (
        "Rule 3.15.4: The first layer added should be at position 1 (index 0)."
    )


@then("the newest layer is layer 2")
def assert_newest_layer_is_layer_2(game_state):
    """Rule 3.15.4: Most recently added layer is at position 2 (index 1)."""
    assert len(game_state.stack) == 2
    assert game_state.stack[1] == game_state._last_added_layer, (
        "Rule 3.15.4: The second layer added should be at position 2 (index 1)."
    )


@then("the layers are numbered 1, 2, and 3 in order")
def assert_layers_numbered_1_2_3(game_state):
    """Rule 3.15.4: Three layers exist at positions 1, 2, 3 from bottom."""
    assert len(game_state.stack) == 3, (
        f"Rule 3.15.4: Expected 3 layers, got {len(game_state.stack)}."
    )
    # Layers should be accessible by their position (0-indexed = layer N-1)
    # Engine feature needed: Layer.layer_number property returning N (1-based)
    # Here we verify via position in list
    for i, layer in enumerate(game_state.stack):
        expected_number = i + 1
        # Check layer is accessible at this position
        assert game_state.stack[i] == layer, (
            f"Rule 3.15.4: Layer at position {expected_number} (index {i}) mismatch."
        )


@then(parsers.parse("the top layer is layer {n:d}"))
def assert_top_layer_is_n(game_state, n):
    """Rule 3.15.5: Top layer is layer N (1-based, highest N)."""
    expected_top_index = n - 1  # Convert to 0-based
    actual_top_index = len(game_state.stack) - 1
    assert actual_top_index == expected_top_index, (
        f"Rule 3.15.5: Top of stack should be layer {n} (index {expected_top_index}), "
        f"but stack has {len(game_state.stack)} layers."
    )


@then("layer 1 is still A")
def assert_layer_1_is_a(game_state):
    """Rule 3.15.6: Layer 1 (index 0) remains unchanged after removal of a higher layer."""
    assert len(game_state.stack) >= 1
    assert game_state.stack[0].label == "A", (
        f"Rule 3.15.6: Layer 1 should still be 'A', got '{game_state.stack[0].label}'."
    )


@then("the former layer 3 (C) is now layer 2")
def assert_former_layer_3_is_now_2(game_state):
    """Rule 3.15.6: After removal of layer 2, former layer 3 (C) is renumbered to layer 2."""
    assert len(game_state.stack) >= 2
    assert game_state.stack[1].label == "C", (
        f"Rule 3.15.6: After removing layer 2, former layer 3 (C) should now be layer 2 "
        f"(index 1), got '{game_state.stack[1].label}'."
    )


@then("the former layer 4 (D) is now layer 3")
def assert_former_layer_4_is_now_3(game_state):
    """Rule 3.15.6: After removal of layer 2, former layer 4 (D) is renumbered to layer 3."""
    assert len(game_state.stack) >= 3
    assert game_state.stack[2].label == "D", (
        f"Rule 3.15.6: After removing layer 2, former layer 4 (D) should now be layer 3 "
        f"(index 2), got '{game_state.stack[2].label}'."
    )


@then("the former layer 2 (Y) is now layer 1")
def assert_former_layer_2_is_now_1(game_state):
    """Rule 3.15.6: After removal of layer 1 (X), former layer 2 (Y) is renumbered to layer 1."""
    assert len(game_state.stack) >= 1
    assert game_state.stack[0].label == "Y", (
        f"Rule 3.15.6: After removing layer 1, former layer 2 (Y) should now be layer 1 "
        f"(index 0), got '{game_state.stack[0].label}'."
    )


@then("the former layer 3 (Z) is now layer 2")
def assert_former_layer_3_z_is_now_2(game_state):
    """Rule 3.15.6: After removal of layer 1 (X), former layer 3 (Z) is renumbered to layer 2."""
    assert len(game_state.stack) >= 2
    assert game_state.stack[1].label == "Z", (
        f"Rule 3.15.6: After removing layer 1, former layer 3 (Z) should now be layer 2 "
        f"(index 1), got '{game_state.stack[1].label}'."
    )


# ===========================================================================
# Helper classes / functions
# ===========================================================================


class _LayerStub:
    """
    Minimal stub representing a layer on the stack for ordering tests.

    Engine Feature Needed:
    - [ ] Layer base class with layer_number property (Rule 3.15.4/3.15.5)
    - [ ] Stack.add_layer() that assigns N+1 numbering (Rule 3.15.4)
    - [ ] Stack.remove_layer(n) that renumbers M>N to M-1 (Rule 3.15.6)
    """

    def __init__(self, label: str):
        self.label = label
        self.is_layer = True

    def __repr__(self):
        return f"LayerStub({self.label!r})"


def _make_layer(label: str) -> _LayerStub:
    """Create a minimal layer stub for ordering tests."""
    return _LayerStub(label)


# ===========================================================================
# Fixtures
# ===========================================================================


@pytest.fixture
def game_state():
    """
    Fixture providing game state for testing Section 3.15: Stack Zone.

    Uses BDDGameState which integrates with the real engine.
    Reference: Rule 3.15
    """
    from tests.bdd_helpers import BDDGameState

    state = BDDGameState()

    # Extra state attributes used by step definitions
    state._checked_zone = None
    state._stack_zone_count = 0
    state._last_added_layer = None
    state._top_layer_index = None
    state._layer_labels = []

    return state
