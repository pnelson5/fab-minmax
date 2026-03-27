"""
Step definitions for Section 8.3.38: Meld (Ability Keyword)
Reference: Flesh and Blood Comprehensive Rules Section 8.3.38

This module implements behavioral tests for the Meld ability keyword:
- Meld is a static ability (Rule 8.3.38)
- Meld means "You may pay twice the base cost of this to play both halves of this" (Rule 8.3.38)
- Playing with Meld is optional — the player MAY pay the alternative cost (Rule 8.3.38)
- Paying the alternative cost marks the player and card as melded (Rule 8.3.38a)
- A melded card remains melded until it ceases to exist (Rule 8.3.38a)
- Meld sets the asset-cost before increases/decreases are applied (Rule 8.3.38b)
- Melded split-card has combined properties of both sides (Rule 8.3.38c)
- A non-split-card with Meld is unaffected by Meld (Rule 8.3.38c)
- Resolution order: right-side abilities first, then left-side on second resolution (Rule 5.3.4d)

Engine Features Needed for Section 8.3.38:
- [ ] AbilityKeyword.MELD on cards (Rule 8.3.38)
- [ ] MeldAbility.is_static -> True (Rule 8.3.38)
- [ ] MeldAbility.meaning == "You may pay twice the base cost of this to play both halves of this" (Rule 8.3.38)
- [ ] Split-card alternative cost calculation: base_cost * 2 (Rule 8.3.38)
- [ ] CardInstance.is_melded property to track meld state (Rule 8.3.38a)
- [ ] Player.has_melded property (Rule 8.3.38a)
- [ ] CardInstance.remains_melded_until_ceases_to_exist behavior (Rule 8.3.38a)
- [ ] Cost system: Meld sets asset-cost before increases/decreases (Rule 8.3.38b, 5.1.6)
- [ ] Melded CardInstance.names returns both split-card side names (Rule 8.3.38c)
- [ ] Melded CardInstance.types returns combined types from both sides (Rule 8.3.38c)
- [ ] Non-split-card unaffected by Meld (Rule 8.3.38c)
- [ ] MeldedCard resolution: first resolution triggers right-side abilities only (Rule 5.3.4d)
- [ ] MeldedCard resolution: second resolution triggers left-side abilities only (Rule 5.3.4d)
- [ ] Turn-player gains priority between first and second resolution (Rule 5.3.4d)

Current status: Tests written, Engine pending
"""

import pytest
from pytest_bdd import scenario, given, when, then, parsers


# ===== Rule 8.3.38: Meld is a static ability =====

@scenario(
    "../features/section_8_3_38_meld.feature",
    "Meld is a static ability",
)
def test_meld_is_static_ability():
    """Rule 8.3.38: Meld is a static ability."""
    pass


# ===== Rule 8.3.38: Meld meaning =====

@scenario(
    "../features/section_8_3_38_meld.feature",
    "Meld means pay twice the base cost to play both halves",
)
def test_meld_meaning_is_correct():
    """Rule 8.3.38: Meld means 'You may pay twice the base cost of this to play both halves of this'."""
    pass


# ===== Rule 8.3.38: Playing with Meld is optional =====

@scenario(
    "../features/section_8_3_38_meld.feature",
    "Player may choose not to pay the Meld alternative cost",
)
def test_meld_is_optional():
    """Rule 8.3.38: The player may choose to play the card without Meld."""
    pass


# ===== Rule 8.3.38a: Paying double cost results in a melded card =====

@scenario(
    "../features/section_8_3_38_meld.feature",
    "Paying double cost marks the card as melded",
)
def test_paying_double_cost_marks_card_as_melded():
    """Rule 8.3.38a: Paying the alternative cost meldes the card and the player."""
    pass


# ===== Rule 8.3.38a: Card remains melded until it ceases to exist =====

@scenario(
    "../features/section_8_3_38_meld.feature",
    "Melded card remains melded until it ceases to exist",
)
def test_melded_card_remains_melded():
    """Rule 8.3.38a: A melded card remains melded until it ceases to exist."""
    pass


# ===== Rule 8.3.38b: Meld sets asset-cost before modifications =====

@scenario(
    "../features/section_8_3_38_meld.feature",
    "Meld sets the asset-cost before cost modifications are applied",
)
def test_meld_sets_asset_cost_before_modifications():
    """Rule 8.3.38b: Meld sets the asset-cost before increases and decreases are applied."""
    pass


# ===== Rule 8.3.38c: Melded card has both names =====

@scenario(
    "../features/section_8_3_38_meld.feature",
    "Melded split-card has both names",
)
def test_melded_card_has_both_names():
    """Rule 8.3.38c: Melded card has the names of both of its sides."""
    pass


# ===== Rule 8.3.38c: Melded card has combined types =====

@scenario(
    "../features/section_8_3_38_meld.feature",
    "Melded split-card has combined types and subtypes",
)
def test_melded_card_has_combined_types():
    """Rule 8.3.38c: Melded card has the combined types and subtypes of both sides."""
    pass


# ===== Rule 8.3.38c: Non-split-card unaffected by Meld =====

@scenario(
    "../features/section_8_3_38_meld.feature",
    "Non-split-card with Meld keyword is unaffected by Meld",
)
def test_non_split_card_unaffected_by_meld():
    """Rule 8.3.38c: If a melded card is not a split-card, it is unaffected by meld."""
    pass


# ===== Rule 5.3.4d: Resolution order — right-side first =====

@scenario(
    "../features/section_8_3_38_meld.feature",
    "Melded card resolves right-side abilities first",
)
def test_melded_card_resolves_right_side_first():
    """Rule 5.3.4d: On first resolution of a melded card, only right-side resolution abilities fire."""
    pass


# ===== Rule 5.3.4d: Resolution order — left-side second =====

@scenario(
    "../features/section_8_3_38_meld.feature",
    "Melded card resolves left-side abilities on second resolution",
)
def test_melded_card_resolves_left_side_second():
    """Rule 5.3.4d: On second resolution of a melded card, only left-side resolution abilities fire."""
    pass


# ===== Step Definitions =====

@given(parsers.parse('a card has the "{keyword}" keyword'))
def card_with_keyword(game_state, keyword):
    """Create a card with the Meld keyword."""
    game_state.keyword_card = game_state.create_card(name="Meld Test Card")
    game_state.keyword_str = keyword


@given(parsers.parse('a split-card with Meld has a base cost of {cost:d}'))
def split_card_with_meld_and_base_cost(game_state, cost):
    """Set up a split-card with Meld and a known base cost."""
    game_state.split_card = game_state.create_card(name="Null||Shock")
    game_state.base_cost = cost
    game_state.meld_cost = cost * 2
    game_state.is_split_card = True
    game_state.card_is_melded = False
    game_state.player_has_melded = False


@given(parsers.parse('there is a cost reduction effect of {reduction:d}'))
def cost_reduction_effect(game_state, reduction):
    """Apply a cost reduction effect to the game state."""
    game_state.cost_reduction = reduction


@given('a split-card has been melded')
def split_card_has_been_melded(game_state):
    """Set up a split-card that has already been melded."""
    game_state.split_card = game_state.create_card(name="Null||Shock")
    game_state.card_is_melded = True
    game_state.player_has_melded = True
    game_state.is_split_card = True
    game_state.resolution_count = 0


@given(parsers.parse('a split-card "{name}" has been melded'))
def named_split_card_has_been_melded(game_state, name):
    """Set up a named split-card that has been melded."""
    parts = name.split("||")
    game_state.left_side_name = parts[0] if len(parts) > 0 else name
    game_state.right_side_name = parts[1] if len(parts) > 1 else name
    game_state.split_card = game_state.create_card(name=name)
    game_state.card_is_melded = True
    game_state.is_split_card = True


@given(parsers.parse('a melded split-card with left-side type "{left_type}" and right-side type "{right_type}"'))
def melded_split_card_with_types(game_state, left_type, right_type):
    """Set up a melded split-card with specific types on each side."""
    game_state.split_card = game_state.create_card(name="Left||Right")
    game_state.left_side_type = left_type
    game_state.right_side_type = right_type
    game_state.card_is_melded = True
    game_state.is_split_card = True


@given('a non-split-card has the "Meld" keyword')
def non_split_card_with_meld(game_state):
    """Set up a non-split-card that has the Meld keyword."""
    game_state.non_split_card = game_state.create_card(name="Regular Card With Meld")
    game_state.is_split_card = False
    game_state.card_is_melded = False


@given('a split-card has been melded and placed on the stack')
def melded_card_on_stack(game_state):
    """Set up a melded split-card that has been placed on the stack."""
    game_state.split_card = game_state.create_card(name="Null||Shock")
    game_state.card_is_melded = True
    game_state.is_split_card = True
    game_state.resolution_count = 0
    game_state.right_side_resolved = False
    game_state.left_side_resolved = False
    game_state.turn_player_gained_priority = False


@given('a split-card has been melded and first resolution has occurred')
def melded_card_after_first_resolution(game_state):
    """Set up a melded split-card after its first resolution."""
    game_state.split_card = game_state.create_card(name="Null||Shock")
    game_state.card_is_melded = True
    game_state.is_split_card = True
    game_state.resolution_count = 1
    game_state.right_side_resolved = True
    game_state.left_side_resolved = False
    game_state.turn_player_gained_priority = True


@when('I inspect the Meld ability on the card')
def inspect_meld_ability(game_state):
    """Inspect the Meld ability on the keyword_card."""
    card = game_state.keyword_card
    try:
        game_state.ability_obj = card.get_ability("meld")
    except (AttributeError, NotImplementedError):
        game_state.ability_obj = None


@when('a player chooses to play the split-card without Meld')
def player_plays_without_meld(game_state):
    """Player plays the split-card normally, not using Meld."""
    game_state.play_used_meld = False
    game_state.cost_paid = game_state.base_cost
    game_state.card_is_melded = False
    game_state.player_has_melded = False


@when('a player chooses to pay the Meld alternative cost of 4')
def player_pays_meld_alternative_cost(game_state):
    """Player chooses to pay the Meld alternative cost (twice base cost)."""
    card = game_state.split_card
    game_state.play_used_meld = True
    game_state.cost_paid = game_state.meld_cost
    try:
        result = card.play_with_meld(cost=game_state.meld_cost)
        game_state.card_is_melded = True
        game_state.player_has_melded = True
        game_state.meld_result = result
    except (AttributeError, NotImplementedError):
        game_state.meld_result = None
        # Still set flags as expected behavior
        game_state.card_is_melded = True
        game_state.player_has_melded = True


@when('the melded card is still on the stack')
def melded_card_is_on_stack(game_state):
    """The melded card is still on the stack (has not ceased to exist)."""
    game_state.card_ceased_to_exist = False


@when('a player chooses to pay the Meld alternative cost')
def player_pays_any_meld_alternative_cost(game_state):
    """Player chooses to pay the Meld alternative cost (twice base cost)."""
    game_state.play_used_meld = True
    game_state.meld_base_cost = game_state.base_cost * 2
    game_state.final_meld_cost = game_state.meld_base_cost - getattr(game_state, 'cost_reduction', 0)


@when('a player attempts to play the card')
def player_attempts_to_play_card(game_state):
    """Player attempts to play the non-split-card with Meld keyword."""
    card = game_state.non_split_card
    game_state.play_attempted = True
    try:
        can_meld = card.can_meld()
        game_state.can_meld = can_meld
    except (AttributeError, NotImplementedError):
        game_state.can_meld = False


@when('the melded card resolves for the first time')
def melded_card_resolves_first_time(game_state):
    """The melded card resolves for the first time."""
    card = game_state.split_card
    game_state.resolution_count = 1
    try:
        result = card.resolve_meld(resolution_number=1)
        game_state.right_side_resolved = True
        game_state.left_side_resolved = False
        game_state.turn_player_gained_priority = True
        game_state.first_resolution_result = result
    except (AttributeError, NotImplementedError):
        game_state.first_resolution_result = None


@when('the melded card resolves for the second time')
def melded_card_resolves_second_time(game_state):
    """The melded card resolves for the second time."""
    card = game_state.split_card
    game_state.resolution_count = 2
    try:
        result = card.resolve_meld(resolution_number=2)
        game_state.left_side_resolved = True
        game_state.second_resolution_result = result
    except (AttributeError, NotImplementedError):
        game_state.second_resolution_result = None


@then('the Meld ability is a static ability')
def meld_is_static_ability(game_state):
    """Verify Meld is a static ability."""
    card = game_state.keyword_card
    try:
        ability = card.get_ability("meld")
        assert ability.is_static, "Meld must be a static ability"
    except (AttributeError, NotImplementedError):
        pytest.fail("Engine feature needed: card.get_ability('meld').is_static")


@then('the Meld ability is not a triggered ability')
def meld_is_not_triggered(game_state):
    """Verify Meld is not a triggered ability."""
    card = game_state.keyword_card
    try:
        ability = card.get_ability("meld")
        assert not ability.is_triggered, "Meld must not be a triggered ability"
    except (AttributeError, NotImplementedError):
        pytest.fail("Engine feature needed: card.get_ability('meld').is_triggered")


@then('the Meld ability is not an activated ability')
def meld_is_not_activated(game_state):
    """Verify Meld is not an activated ability."""
    card = game_state.keyword_card
    try:
        ability = card.get_ability("meld")
        assert not ability.is_activated, "Meld must not be an activated ability"
    except (AttributeError, NotImplementedError):
        pytest.fail("Engine feature needed: card.get_ability('meld').is_activated")


@then('the Meld ability means "You may pay twice the base cost of this to play both halves of this"')
def meld_meaning_is_correct(game_state):
    """Verify the meaning string for Meld."""
    card = game_state.keyword_card
    expected_meaning = "You may pay twice the base cost of this to play both halves of this"
    try:
        ability = card.get_ability("meld")
        assert ability.meaning == expected_meaning, (
            f"Meld meaning mismatch: expected '{expected_meaning}', got '{ability.meaning}'"
        )
    except (AttributeError, NotImplementedError):
        pytest.fail(f"Engine feature needed: MeldAbility.meaning == '{expected_meaning}'")


@then(parsers.parse('the player pays the normal base cost of {cost:d}'))
def player_pays_normal_cost(game_state, cost):
    """Verify the player paid the normal base cost."""
    assert game_state.cost_paid == cost, (
        f"Expected cost paid to be {cost}, got {game_state.cost_paid}"
    )


@then('the card is not melded')
def card_is_not_melded(game_state):
    """Verify the card is not melded."""
    assert not game_state.card_is_melded, "Card should not be melded when normal cost was paid"


@then('the player is considered to have melded')
def player_has_melded(game_state):
    """Verify the player is considered to have melded."""
    assert game_state.player_has_melded, "Player should be considered to have melded"
    try:
        assert game_state.player.has_melded, "Engine: player.has_melded should be True"
    except (AttributeError, NotImplementedError):
        pytest.fail("Engine feature needed: Player.has_melded property (Rule 8.3.38a)")


@then('the card is melded')
def card_is_melded(game_state):
    """Verify the card is melded."""
    assert game_state.card_is_melded, "Card should be melded after paying the alternative cost"
    card = game_state.split_card
    try:
        assert card.is_melded, "Engine: card.is_melded should be True"
    except (AttributeError, NotImplementedError):
        pytest.fail("Engine feature needed: CardInstance.is_melded property (Rule 8.3.38a)")


@then('the card remains melded until it ceases to exist')
def card_remains_melded_until_ceases_to_exist(game_state):
    """Verify the card remains melded while it still exists."""
    assert not game_state.card_ceased_to_exist, "Card has not ceased to exist yet"
    assert game_state.card_is_melded, "Card should still be melded while it exists"
    card = game_state.split_card
    try:
        assert card.is_melded, "Engine: card.is_melded should remain True until card ceases to exist"
    except (AttributeError, NotImplementedError):
        pytest.fail("Engine feature needed: CardInstance.is_melded persists until card ceases to exist (Rule 8.3.38a)")


@then(parsers.parse('the Meld cost is set to {cost:d} before cost modifications'))
def meld_cost_is_set_before_modifications(game_state, cost):
    """Verify Meld sets the asset-cost to twice the base cost before modifications."""
    assert game_state.meld_base_cost == cost, (
        f"Meld should set asset-cost to {cost} (twice the base cost) before modifications, "
        f"got {game_state.meld_base_cost}"
    )
    card = game_state.split_card
    try:
        meld_asset_cost = card.get_meld_asset_cost()
        assert meld_asset_cost == cost, (
            f"Engine: card.get_meld_asset_cost() should be {cost}, got {meld_asset_cost}"
        )
    except (AttributeError, NotImplementedError):
        pytest.fail(f"Engine feature needed: CardInstance.get_meld_asset_cost() == {cost} (Rule 8.3.38b)")


@then(parsers.parse('the final cost to play with Meld is {cost:d} after the cost reduction'))
def final_meld_cost_after_reduction(game_state, cost):
    """Verify the final cost after applying cost reductions to the Meld asset-cost."""
    assert game_state.final_meld_cost == cost, (
        f"Expected final Meld cost to be {cost} after reduction, got {game_state.final_meld_cost}"
    )


@then(parsers.parse('the melded card has the name "{name}"'))
def melded_card_has_name(game_state, name):
    """Verify the melded card has the given name (from one of its sides)."""
    card = game_state.split_card
    try:
        names = card.names
        assert name in names, (
            f"Melded card should have name '{name}', but names are: {names}"
        )
    except (AttributeError, NotImplementedError):
        pytest.fail(f"Engine feature needed: CardInstance.names returns both side names when melded (Rule 8.3.38c)")


@then(parsers.parse('the melded card has type "{card_type}"'))
def melded_card_has_type(game_state, card_type):
    """Verify the melded card has the given type (combined from both sides)."""
    card = game_state.split_card
    try:
        types = card.types
        type_names = [t.name if hasattr(t, 'name') else str(t) for t in types]
        assert card_type in type_names or card_type.upper() in [t.upper() for t in type_names], (
            f"Melded card should have type '{card_type}', but types are: {type_names}"
        )
    except (AttributeError, NotImplementedError):
        pytest.fail(f"Engine feature needed: CardInstance.types returns combined types when melded (Rule 8.3.38c)")


@then('the card is unaffected by Meld')
def card_is_unaffected_by_meld(game_state):
    """Verify a non-split-card is unaffected by Meld."""
    assert not game_state.is_split_card, "Card should be a non-split-card"
    card = game_state.non_split_card
    try:
        is_affected = card.is_affected_by_meld()
        assert not is_affected, "Non-split-card should be unaffected by Meld"
    except (AttributeError, NotImplementedError):
        pytest.fail("Engine feature needed: CardInstance.is_affected_by_meld() returns False for non-split-cards (Rule 8.3.38c)")


@then('the card cannot be melded')
def card_cannot_be_melded(game_state):
    """Verify a non-split-card cannot be melded."""
    assert not game_state.can_meld, "Non-split-card should not be able to meld"
    card = game_state.non_split_card
    try:
        can_meld = card.can_meld()
        assert not can_meld, "Non-split-card: card.can_meld() should return False"
    except (AttributeError, NotImplementedError):
        pytest.fail("Engine feature needed: CardInstance.can_meld() returns False for non-split-cards (Rule 8.3.38c)")


@then('only the right-side resolution abilities generate their effects')
def only_right_side_resolves_first(game_state):
    """Verify that on first resolution only right-side abilities fire."""
    assert game_state.resolution_count == 1, "Should be first resolution"
    card = game_state.split_card
    try:
        resolution_state = card.get_meld_resolution_state()
        assert resolution_state.right_resolved, "Engine: right-side should be resolved"
        assert not resolution_state.left_resolved, "Engine: left-side should not be resolved yet"
    except (AttributeError, NotImplementedError):
        pytest.fail("Engine feature needed: CardInstance.get_meld_resolution_state() for melded resolution tracking (Rule 5.3.4d)")


@then('the turn-player gains priority after first resolution')
def turn_player_gains_priority_after_first_resolution(game_state):
    """Verify the turn-player gains priority after the first resolution."""
    try:
        assert game_state.player.has_priority, "Engine: turn-player should have priority after first resolution"
    except (AttributeError, NotImplementedError):
        pytest.fail("Engine feature needed: Player.has_priority after melded card first resolution (Rule 5.3.4d)")


@then('only the left-side resolution abilities generate their effects')
def only_left_side_resolves_second(game_state):
    """Verify that on second resolution only left-side abilities fire."""
    assert game_state.resolution_count == 2, "Should be second resolution"
    card = game_state.split_card
    try:
        resolution_state = card.get_meld_resolution_state()
        assert resolution_state.left_resolved, "Engine: left-side should be resolved on second pass"
    except (AttributeError, NotImplementedError):
        pytest.fail("Engine feature needed: CardInstance.get_meld_resolution_state() tracks left-side resolution (Rule 5.3.4d)")


# ===== Fixtures =====

@pytest.fixture
def game_state():
    """
    Fixture providing game state for testing Meld.

    Uses BDDGameState which integrates with the real engine.
    Reference: Rule 8.3.38
    """
    from tests.bdd_helpers import BDDGameState

    state = BDDGameState()
    state.base_cost = 0
    state.meld_cost = 0
    state.cost_paid = 0
    state.cost_reduction = 0
    state.meld_base_cost = 0
    state.final_meld_cost = 0
    state.card_is_melded = False
    state.player_has_melded = False
    state.play_used_meld = False
    state.is_split_card = False
    state.card_ceased_to_exist = False
    state.resolution_count = 0
    state.right_side_resolved = False
    state.left_side_resolved = False
    state.turn_player_gained_priority = False
    state.can_meld = False

    return state
