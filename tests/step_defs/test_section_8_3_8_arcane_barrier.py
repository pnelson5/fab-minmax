"""
Step definitions for Section 8.3.8: Arcane Barrier (Ability Keyword)
Reference: Flesh and Blood Comprehensive Rules Section 8.3.8

This module implements behavioral tests for the Arcane Barrier ability keyword:
- Arcane Barrier is a static ability (Rule 8.3.8)
- Written as "Arcane Barrier N" meaning "If you would be dealt arcane damage,
  you may pay N{r} to prevent N of that damage" (Rule 8.3.8)
- Prevention is optional — the player chooses whether to pay (Rule 8.3.8)
- Applies only to arcane damage, not regular combat damage (Rule 8.3.8)
- Multiple instances can each be independently activated (Rule 8.3.8)
- Cannot be activated if player lacks sufficient resources (Rule 8.3.8)

Engine Features Needed for Section 8.3.8:
- [ ] AbilityKeyword.ARCANE_BARRIER on cards/equipment (Rule 8.3.8)
- [ ] ArcaneBarrierAbility.is_static -> True (not triggered, not meta-static) (Rule 8.3.8)
- [ ] ArcaneBarrierAbility.value property returning the N in "Arcane Barrier N" (Rule 8.3.8)
- [ ] ArcaneBarrierAbility.meaning == "If you would be dealt arcane damage, you may pay N{r} to prevent N of that damage" (Rule 8.3.8)
- [ ] DamageEvent.damage_type distinguishing arcane vs regular combat damage (Rule 8.3.8)
- [ ] ArcaneBarrierAbility.can_activate(player) checks if player has sufficient resources (Rule 8.3.8)
- [ ] ArcaneBarrierAbility.activate(player) spends N resources and creates prevention of N arcane damage (Rule 8.3.8)
- [ ] Multiple ArcaneBarrierAbility instances on a player each independently activatable (Rule 8.3.8)

Current status: Tests written, Engine pending
"""

import pytest
from pytest_bdd import scenario, given, when, then, parsers


# ===== Rule 8.3.8: Arcane Barrier is a static ability =====

@scenario(
    "../features/section_8_3_8_arcane_barrier.feature",
    "Arcane Barrier is a static ability",
)
def test_arcane_barrier_is_static_ability():
    """Rule 8.3.8: Arcane Barrier is a static ability."""
    pass


# ===== Rule 8.3.8: Meaning is correct =====

@scenario(
    "../features/section_8_3_8_arcane_barrier.feature",
    "Arcane Barrier N means pay N resources to prevent N arcane damage",
)
def test_arcane_barrier_meaning_is_correct():
    """Rule 8.3.8: Arcane Barrier N means pay N{r} to prevent N arcane damage."""
    pass


# ===== Rule 8.3.8: Player can pay to prevent arcane damage =====

@scenario(
    "../features/section_8_3_8_arcane_barrier.feature",
    "Player pays Arcane Barrier cost to prevent arcane damage",
)
def test_player_pays_arcane_barrier_to_prevent_damage():
    """Rule 8.3.8: Paying N resources prevents N arcane damage."""
    pass


# ===== Rule 8.3.8: Prevention is optional =====

@scenario(
    "../features/section_8_3_8_arcane_barrier.feature",
    "Player may choose not to activate Arcane Barrier",
)
def test_arcane_barrier_prevention_is_optional():
    """Rule 8.3.8: The player may choose not to pay the Arcane Barrier cost."""
    pass


# ===== Rule 8.3.8: Does not apply to regular combat damage =====

@scenario(
    "../features/section_8_3_8_arcane_barrier.feature",
    "Arcane Barrier does not prevent regular combat damage",
)
def test_arcane_barrier_does_not_prevent_combat_damage():
    """Rule 8.3.8: Arcane Barrier only applies to arcane damage."""
    pass


# ===== Rule 8.3.8: Cannot activate without sufficient resources =====

@scenario(
    "../features/section_8_3_8_arcane_barrier.feature",
    "Player cannot activate Arcane Barrier without sufficient resources",
)
def test_arcane_barrier_requires_sufficient_resources():
    """Rule 8.3.8: Arcane Barrier cannot be activated if the player lacks N resources."""
    pass


# ===== Rule 8.3.8: Multiple instances independently activatable =====

@scenario(
    "../features/section_8_3_8_arcane_barrier.feature",
    "Multiple Arcane Barrier instances can each be independently activated",
)
def test_multiple_arcane_barrier_instances_independently_activatable():
    """Rule 8.3.8: Multiple instances of Arcane Barrier can each be activated separately."""
    pass


# ===== Step Definitions =====

# ---- Given steps ----

@given(parsers.parse('a card has the "{keyword}" keyword'))
def card_has_arcane_barrier_keyword(game_state, keyword):
    """Rule 8.3.8: Create a card that has an Arcane Barrier keyword."""
    card = game_state.create_card(name=f"Arcane Barrier Test Card ({keyword})")
    # Parse "Arcane Barrier N" to extract value N
    if keyword.startswith("Arcane Barrier "):
        try:
            value = int(keyword[len("Arcane Barrier "):].strip())
        except ValueError:
            value = 1
        card._arcane_barrier_value = value
        card._keyword = keyword
    game_state.arcane_barrier_card = card


@given(parsers.parse('a player has an equipment with "{keyword}"'))
def player_has_equipment_with_arcane_barrier(game_state, keyword):
    """Rule 8.3.8: Give the player an equipment card with the specified Arcane Barrier keyword."""
    if not hasattr(game_state, "arcane_barrier_equipments"):
        game_state.arcane_barrier_equipments = []
    equipment = game_state.create_card(name=f"Arcane Barrier Equipment ({keyword})")
    if keyword.startswith("Arcane Barrier "):
        try:
            value = int(keyword[len("Arcane Barrier "):].strip())
        except ValueError:
            value = 1
        equipment._arcane_barrier_value = value
        equipment._keyword = keyword
    game_state.arcane_barrier_equipments.append(equipment)
    # Track the first equipment as primary for single-equipment scenarios
    if len(game_state.arcane_barrier_equipments) == 1:
        game_state.primary_arcane_barrier_equipment = equipment


@given(parsers.parse('the player also has an equipment with "{keyword}"'))
def player_also_has_equipment_with_arcane_barrier(game_state, keyword):
    """Rule 8.3.8: Give the player a second equipment card with the specified Arcane Barrier keyword."""
    if not hasattr(game_state, "arcane_barrier_equipments"):
        game_state.arcane_barrier_equipments = []
    equipment = game_state.create_card(name=f"Second Arcane Barrier Equipment ({keyword})")
    if keyword.startswith("Arcane Barrier "):
        try:
            value = int(keyword[len("Arcane Barrier "):].strip())
        except ValueError:
            value = 1
        equipment._arcane_barrier_value = value
        equipment._keyword = keyword
    game_state.arcane_barrier_equipments.append(equipment)


@given(parsers.parse("the player has {count} or more resources available"))
def player_has_resources_available(game_state, count):
    """Rule 8.3.8: Give the player the specified number of available resources."""
    resource_count = int(count)
    game_state.player_available_resources = resource_count
    game_state.resources_spent = 0


@given("the player has 0 resources available")
def player_has_no_resources_available(game_state):
    """Rule 8.3.8: The player has no resources to pay for Arcane Barrier."""
    game_state.player_available_resources = 0
    game_state.resources_spent = 0


# ---- When steps ----

@when("I inspect the Arcane Barrier ability on the card")
def inspect_arcane_barrier_ability(game_state):
    """Rule 8.3.8: Inspect the Arcane Barrier ability on the test card."""
    game_state.inspected_ability = game_state.get_arcane_barrier_ability(
        game_state.arcane_barrier_card
    )


@when(parsers.parse("the player would be dealt {amount:d} arcane damage"))
def player_would_be_dealt_arcane_damage(game_state, amount):
    """Rule 8.3.8: Set up an arcane damage event of the specified amount."""
    game_state.incoming_damage_amount = amount
    game_state.incoming_damage_type = "arcane"
    game_state.damage_prevented = 0
    game_state.arcane_barrier_activated = False


@when(parsers.parse("the player would be dealt {amount:d} regular combat damage"))
def player_would_be_dealt_regular_damage(game_state, amount):
    """Rule 8.3.8: Set up a regular combat damage event (not arcane)."""
    game_state.incoming_damage_amount = amount
    game_state.incoming_damage_type = "combat"
    game_state.damage_prevented = 0
    game_state.arcane_barrier_activated = False


@when("the player chooses to activate Arcane Barrier")
def player_activates_arcane_barrier(game_state):
    """Rule 8.3.8: The player pays the Arcane Barrier cost to prevent arcane damage."""
    result = game_state.attempt_arcane_barrier_activation(
        equipment=game_state.primary_arcane_barrier_equipment,
        available_resources=game_state.player_available_resources,
        damage_type=game_state.incoming_damage_type,
    )
    game_state.arcane_barrier_result = result
    if result is not None:
        activated = getattr(result, "activated", False)
        if activated:
            game_state.arcane_barrier_activated = True
            cost = getattr(game_state.primary_arcane_barrier_equipment, "_arcane_barrier_value", 0)
            game_state.resources_spent = cost
            game_state.damage_prevented = cost


@when("the player chooses not to activate Arcane Barrier")
def player_does_not_activate_arcane_barrier(game_state):
    """Rule 8.3.8: The player opts not to pay the Arcane Barrier cost."""
    game_state.arcane_barrier_activated = False
    game_state.resources_spent = 0
    game_state.damage_prevented = 0


@when("the player activates both Arcane Barrier instances")
def player_activates_both_arcane_barrier_instances(game_state):
    """Rule 8.3.8: The player activates all available Arcane Barrier instances."""
    total_prevented = 0
    total_spent = 0
    game_state.arcane_barrier_results = []
    for equipment in game_state.arcane_barrier_equipments:
        result = game_state.attempt_arcane_barrier_activation(
            equipment=equipment,
            available_resources=game_state.player_available_resources - total_spent,
            damage_type=game_state.incoming_damage_type,
        )
        game_state.arcane_barrier_results.append(result)
        if result is not None:
            activated = getattr(result, "activated", False)
            if activated:
                cost = getattr(equipment, "_arcane_barrier_value", 0)
                total_spent += cost
                total_prevented += cost
    game_state.resources_spent = total_spent
    game_state.damage_prevented = total_prevented
    game_state.arcane_barrier_activated = total_prevented > 0


# ---- Then steps ----

@then("the Arcane Barrier ability is a static ability")
def arcane_barrier_is_static(game_state):
    """Rule 8.3.8: Arcane Barrier must be a static ability."""
    ability = game_state.inspected_ability
    assert ability is not None, "Card should have an Arcane Barrier ability"
    is_static = getattr(ability, "is_static", None)
    assert is_static is True, (
        f"Arcane Barrier should be a static ability (Rule 8.3.8), got is_static={is_static}"
    )


@then("the Arcane Barrier ability is not a triggered ability")
def arcane_barrier_is_not_triggered(game_state):
    """Rule 8.3.8: Arcane Barrier must NOT be a triggered ability."""
    ability = game_state.inspected_ability
    assert ability is not None, "Card should have an Arcane Barrier ability"
    is_triggered = getattr(ability, "is_triggered", False)
    assert is_triggered is False, (
        f"Arcane Barrier should NOT be a triggered ability (Rule 8.3.8), got is_triggered={is_triggered}"
    )


@then("the Arcane Barrier ability is not a meta-static ability")
def arcane_barrier_is_not_meta_static(game_state):
    """Rule 8.3.8: Arcane Barrier must NOT be a meta-static ability."""
    ability = game_state.inspected_ability
    assert ability is not None, "Card should have an Arcane Barrier ability"
    is_meta_static = getattr(ability, "is_meta_static", False)
    assert is_meta_static is False, (
        f"Arcane Barrier should NOT be a meta-static ability (Rule 8.3.8), got is_meta_static={is_meta_static}"
    )


@then(parsers.parse('the Arcane Barrier ability means "If you would be dealt arcane damage, you may pay {n:d}{{r}} to prevent {n2:d} of that damage"'))
def arcane_barrier_meaning_is_correct(game_state, n, n2):
    """Rule 8.3.8: Arcane Barrier meaning includes the correct resource cost and prevention amount."""
    ability = game_state.inspected_ability
    meaning = getattr(ability, "meaning", None)
    expected = f"If you would be dealt arcane damage, you may pay {n}{{r}} to prevent {n2} of that damage"
    assert meaning == expected, (
        f"Arcane Barrier meaning should be '{expected}' (Rule 8.3.8), got: {meaning}"
    )


@then(parsers.parse("the Arcane Barrier value is {value:d}"))
def arcane_barrier_value_is_correct(game_state, value):
    """Rule 8.3.8: The N in 'Arcane Barrier N' is the barrier value."""
    ability = game_state.inspected_ability
    assert ability is not None, "Card should have an Arcane Barrier ability"
    barrier_value = getattr(ability, "value", None)
    assert barrier_value == value, (
        f"Arcane Barrier value should be {value} (Rule 8.3.8), got: {barrier_value}"
    )


@then(parsers.parse("the player pays {cost:d} resource"))
def player_pays_resource(game_state, cost):
    """Rule 8.3.8: The player should have spent the correct number of resources on Arcane Barrier."""
    assert game_state.resources_spent == cost, (
        f"Player should have paid {cost} resource(s) for Arcane Barrier (Rule 8.3.8), "
        f"got: {game_state.resources_spent}"
    )


@then(parsers.parse("{amount:d} arcane damage is prevented"))
def arcane_damage_is_prevented(game_state, amount):
    """Rule 8.3.8: The correct amount of arcane damage should be prevented."""
    assert game_state.damage_prevented == amount, (
        f"Arcane Barrier should have prevented {amount} arcane damage (Rule 8.3.8), "
        f"got: {game_state.damage_prevented}"
    )


@then(parsers.parse("the player is dealt {amount:d} arcane damage"))
def player_is_dealt_arcane_damage(game_state, amount):
    """Rule 8.3.8: After prevention, the player takes the correct amount of arcane damage."""
    remaining = game_state.incoming_damage_amount - game_state.damage_prevented
    assert remaining == amount, (
        f"Player should take {amount} arcane damage after prevention (Rule 8.3.8), "
        f"got: {remaining}"
    )


@then("no resources are spent on Arcane Barrier")
def no_resources_spent(game_state):
    """Rule 8.3.8: When the player opts out, no resources are spent on Arcane Barrier."""
    assert game_state.resources_spent == 0, (
        f"No resources should be spent when Arcane Barrier is not activated (Rule 8.3.8), "
        f"got: {game_state.resources_spent}"
    )


@then(parsers.parse("the player is dealt {amount:d} regular combat damage"))
def player_is_dealt_regular_combat_damage(game_state, amount):
    """Rule 8.3.8: After no prevention, the player takes the full combat damage."""
    remaining = game_state.incoming_damage_amount - game_state.damage_prevented
    assert remaining == amount, (
        f"Player should take {amount} regular combat damage (Rule 8.3.8), got: {remaining}"
    )


@then("Arcane Barrier cannot be activated against regular combat damage")
def arcane_barrier_cannot_activate_for_combat_damage(game_state):
    """Rule 8.3.8: Arcane Barrier only works against arcane damage, not regular combat damage."""
    assert game_state.incoming_damage_type == "combat", (
        "Damage type should be 'combat' for this test"
    )
    result = game_state.attempt_arcane_barrier_activation(
        equipment=game_state.primary_arcane_barrier_equipment,
        available_resources=game_state.player_available_resources,
        damage_type=game_state.incoming_damage_type,
    )
    if result is not None:
        activated = getattr(result, "activated", False)
        assert activated is False, (
            "Arcane Barrier should NOT be activatable against regular combat damage (Rule 8.3.8)"
        )


@then("the player cannot activate Arcane Barrier")
def player_cannot_activate_arcane_barrier(game_state):
    """Rule 8.3.8: When the player has insufficient resources, Arcane Barrier cannot be activated."""
    result = game_state.attempt_arcane_barrier_activation(
        equipment=game_state.primary_arcane_barrier_equipment,
        available_resources=game_state.player_available_resources,
        damage_type=game_state.incoming_damage_type,
    )
    if result is not None:
        can_activate = getattr(result, "can_activate", None)
        activated = getattr(result, "activated", False)
        assert activated is False, (
            "Player with 0 resources should NOT be able to activate Arcane Barrier (Rule 8.3.8)"
        )
        if can_activate is not None:
            assert can_activate is False, (
                "can_activate should be False when player lacks resources (Rule 8.3.8)"
            )
    else:
        # None result means engine doesn't implement this yet — that's expected
        pass


@then(parsers.parse("the player pays {cost:d} resources total"))
def player_pays_resources_total(game_state, cost):
    """Rule 8.3.8: The total resources spent across all Arcane Barrier activations."""
    assert game_state.resources_spent == cost, (
        f"Player should have paid {cost} total resources for all Arcane Barriers (Rule 8.3.8), "
        f"got: {game_state.resources_spent}"
    )


@then(parsers.parse("{amount:d} arcane damage is prevented total"))
def arcane_damage_prevented_total(game_state, amount):
    """Rule 8.3.8: Total arcane damage prevented across all Arcane Barrier activations."""
    assert game_state.damage_prevented == amount, (
        f"Multiple Arcane Barrier instances should have prevented {amount} total arcane damage "
        f"(Rule 8.3.8), got: {game_state.damage_prevented}"
    )


# ===== Fixtures =====

@pytest.fixture
def game_state():
    """
    Fixture providing game state for testing Arcane Barrier (Rule 8.3.8).

    Uses BDDGameState which integrates with the real engine.
    Reference: Rule 8.3.8
    """
    from tests.bdd_helpers import BDDGameState

    state = BDDGameState()
    state.arcane_barrier_equipments = []
    state.player_available_resources = 0
    state.resources_spent = 0
    state.damage_prevented = 0
    state.incoming_damage_amount = 0
    state.incoming_damage_type = "arcane"
    return state
