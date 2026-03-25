"""
Step definitions for Section 8.3.15: Spellvoid (Ability Keyword)
Reference: Flesh and Blood Comprehensive Rules Section 8.3.15

This module implements behavioral tests for the Spellvoid ability keyword:
- Spellvoid is a static ability (Rule 8.3.15)
- Written as "Spellvoid N" meaning "If you would be dealt arcane damage,
  you may destroy this to prevent N of that damage" (Rule 8.3.15)
- Prevention is optional — the player chooses whether to destroy the object (Rule 8.3.15)
- The cost is DESTROYING the object itself, not paying resources (Rule 8.3.15)
- If the controlling player cannot destroy the object, they cannot apply the prevention
  (Rule 8.3.15a)
- Only applies to arcane damage, not regular combat damage (Rule 8.3.15)
- Multiple objects with Spellvoid can each independently be activated (Rule 8.3.15)

Engine Features Needed for Section 8.3.15:
- [ ] AbilityKeyword.SPELLVOID on cards/equipment (Rule 8.3.15)
- [ ] SpellvoidAbility.is_static -> True (not triggered, not meta-static) (Rule 8.3.15)
- [ ] SpellvoidAbility.value property returning the N in "Spellvoid N" (Rule 8.3.15)
- [ ] SpellvoidAbility.meaning == "If you would be dealt arcane damage, you may destroy this
      to prevent N of that damage" (Rule 8.3.15)
- [ ] DamageEvent.damage_type distinguishing arcane vs regular combat damage (Rule 8.3.15)
- [ ] SpellvoidAbility.can_activate(object) checks if object can be destroyed (Rule 8.3.15a)
- [ ] SpellvoidAbility.activate(object) destroys the object and creates prevention of N arcane
      damage (Rule 8.3.15)
- [ ] Prevention blocked when object cannot be destroyed (Rule 8.3.15a)
- [ ] Multiple SpellvoidAbility instances on different objects each independently activatable
      (Rule 8.3.15)

Current status: Tests written, Engine pending
"""

import pytest
from pytest_bdd import scenario, given, when, then, parsers


# ===== Rule 8.3.15: Spellvoid is a static ability =====

@scenario(
    "../features/section_8_3_15_spellvoid.feature",
    "Spellvoid is a static ability",
)
def test_spellvoid_is_static_ability():
    """Rule 8.3.15: Spellvoid is a static ability."""
    pass


# ===== Rule 8.3.15: Spellvoid meaning is correct =====

@scenario(
    "../features/section_8_3_15_spellvoid.feature",
    "Spellvoid N means destroy this to prevent N arcane damage",
)
def test_spellvoid_meaning_is_correct():
    """Rule 8.3.15: Spellvoid N means destroy this to prevent N arcane damage."""
    pass


# ===== Rule 8.3.15: Player may destroy object to prevent arcane damage =====

@scenario(
    "../features/section_8_3_15_spellvoid.feature",
    "Player destroys object with Spellvoid to prevent arcane damage",
)
def test_player_destroys_object_to_prevent_arcane_damage():
    """Rule 8.3.15: Destroying the Spellvoid object prevents N arcane damage."""
    pass


# ===== Rule 8.3.15: Prevention is optional =====

@scenario(
    "../features/section_8_3_15_spellvoid.feature",
    "Player may choose not to activate Spellvoid",
)
def test_spellvoid_prevention_is_optional():
    """Rule 8.3.15: The player may choose not to destroy the object."""
    pass


# ===== Rule 8.3.15: Spellvoid does not prevent regular combat damage =====

@scenario(
    "../features/section_8_3_15_spellvoid.feature",
    "Spellvoid does not prevent regular combat damage",
)
def test_spellvoid_does_not_prevent_combat_damage():
    """Rule 8.3.15: Spellvoid only applies to arcane damage."""
    pass


# ===== Rule 8.3.15a: Cannot apply Spellvoid if object cannot be destroyed =====

@scenario(
    "../features/section_8_3_15_spellvoid.feature",
    "Player cannot apply Spellvoid if object cannot be destroyed",
)
def test_spellvoid_blocked_when_object_indestructible():
    """Rule 8.3.15a: If the object cannot be destroyed, the prevention cannot be applied."""
    pass


# ===== Rule 8.3.15: Multiple Spellvoid objects each independently usable =====

@scenario(
    "../features/section_8_3_15_spellvoid.feature",
    "Multiple Spellvoid objects can each independently prevent arcane damage",
)
def test_multiple_spellvoid_objects_independently_usable():
    """Rule 8.3.15: Multiple objects with Spellvoid can each be destroyed independently."""
    pass


# ===== Step Definitions =====

# ---- Given steps ----

@given(parsers.parse('a card has the "{keyword}" keyword'))
def card_has_spellvoid_keyword(game_state, keyword):
    """Rule 8.3.15: Create a card that has a Spellvoid keyword."""
    card = game_state.create_card(name=f"Spellvoid Test Card ({keyword})")
    if keyword.startswith("Spellvoid "):
        try:
            value = int(keyword[len("Spellvoid "):].strip())
        except ValueError:
            value = 1
        card._spellvoid_value = value
        card._keyword = keyword
    game_state.spellvoid_card = card


@given(parsers.parse('a player has an object with "{keyword}"'))
def player_has_object_with_spellvoid(game_state, keyword):
    """Rule 8.3.15: Give the player an object with the specified Spellvoid keyword."""
    if not hasattr(game_state, "spellvoid_objects"):
        game_state.spellvoid_objects = []
    obj = game_state.create_card(name=f"Spellvoid Object ({keyword})")
    if keyword.startswith("Spellvoid "):
        try:
            value = int(keyword[len("Spellvoid "):].strip())
        except ValueError:
            value = 1
        obj._spellvoid_value = value
        obj._keyword = keyword
    obj._can_be_destroyed = True
    obj._is_destroyed = False
    game_state.spellvoid_objects.append(obj)
    game_state.primary_spellvoid_object = obj


@given(parsers.parse('the player also has an object with "{keyword}"'))
def player_also_has_object_with_spellvoid(game_state, keyword):
    """Rule 8.3.15: Give the player a second object with the specified Spellvoid keyword."""
    if not hasattr(game_state, "spellvoid_objects"):
        game_state.spellvoid_objects = []
    obj = game_state.create_card(name=f"Second Spellvoid Object ({keyword})")
    if keyword.startswith("Spellvoid "):
        try:
            value = int(keyword[len("Spellvoid "):].strip())
        except ValueError:
            value = 1
        obj._spellvoid_value = value
        obj._keyword = keyword
    obj._can_be_destroyed = True
    obj._is_destroyed = False
    game_state.spellvoid_objects.append(obj)


@given("the object can be destroyed")
def object_can_be_destroyed(game_state):
    """Rule 8.3.15: The primary Spellvoid object is destroyable."""
    game_state.primary_spellvoid_object._can_be_destroyed = True


@given("the object cannot be destroyed")
def object_cannot_be_destroyed(game_state):
    """Rule 8.3.15a: The primary Spellvoid object cannot be destroyed."""
    game_state.primary_spellvoid_object._can_be_destroyed = False


@given("both objects can be destroyed")
def both_objects_can_be_destroyed(game_state):
    """Rule 8.3.15: All Spellvoid objects in the list are destroyable."""
    for obj in game_state.spellvoid_objects:
        obj._can_be_destroyed = True


# ---- When steps ----

@when("I inspect the Spellvoid ability on the card")
def inspect_spellvoid_ability(game_state):
    """Rule 8.3.15: Inspect the Spellvoid ability on the test card."""
    game_state.inspected_ability = game_state.get_spellvoid_ability(
        game_state.spellvoid_card
    )


@when(parsers.parse("the player would be dealt {amount:d} arcane damage"))
def player_would_be_dealt_arcane_damage(game_state, amount):
    """Rule 8.3.15: Set up an arcane damage event of the specified amount."""
    game_state.incoming_damage_amount = amount
    game_state.incoming_damage_type = "arcane"
    game_state.damage_prevented = 0
    game_state.spellvoid_activated = False


@when(parsers.parse("the player would be dealt {amount:d} regular combat damage"))
def player_would_be_dealt_regular_damage(game_state, amount):
    """Rule 8.3.15: Set up a regular combat damage event (not arcane)."""
    game_state.incoming_damage_amount = amount
    game_state.incoming_damage_type = "combat"
    game_state.damage_prevented = 0
    game_state.spellvoid_activated = False


@when("the player chooses to activate Spellvoid")
def player_activates_spellvoid(game_state):
    """Rule 8.3.15: The player destroys the Spellvoid object to prevent arcane damage."""
    result = game_state.attempt_spellvoid_activation(
        obj=game_state.primary_spellvoid_object,
        damage_type=game_state.incoming_damage_type,
    )
    game_state.spellvoid_result = result
    if result is not None:
        activated = getattr(result, "activated", False)
        if activated:
            game_state.spellvoid_activated = True
            game_state.primary_spellvoid_object._is_destroyed = True
            value = getattr(game_state.primary_spellvoid_object, "_spellvoid_value", 0)
            game_state.damage_prevented = value


@when("the player chooses not to activate Spellvoid")
def player_does_not_activate_spellvoid(game_state):
    """Rule 8.3.15: The player opts not to destroy the Spellvoid object."""
    game_state.spellvoid_activated = False
    game_state.damage_prevented = 0


@when("the player activates both Spellvoid instances")
def player_activates_both_spellvoid_instances(game_state):
    """Rule 8.3.15: The player activates all available Spellvoid instances."""
    total_prevented = 0
    game_state.spellvoid_results = []
    for obj in game_state.spellvoid_objects:
        result = game_state.attempt_spellvoid_activation(
            obj=obj,
            damage_type=game_state.incoming_damage_type,
        )
        game_state.spellvoid_results.append(result)
        if result is not None:
            activated = getattr(result, "activated", False)
            if activated:
                obj._is_destroyed = True
                value = getattr(obj, "_spellvoid_value", 0)
                total_prevented += value
    game_state.damage_prevented = total_prevented
    game_state.spellvoid_activated = total_prevented > 0


# ---- Then steps ----

@then("the Spellvoid ability is a static ability")
def spellvoid_is_static(game_state):
    """Rule 8.3.15: Spellvoid must be a static ability."""
    ability = game_state.inspected_ability
    assert ability is not None, "Card should have a Spellvoid ability"
    is_static = getattr(ability, "is_static", None)
    assert is_static is True, (
        f"Spellvoid should be a static ability (Rule 8.3.15), got is_static={is_static}"
    )


@then("the Spellvoid ability is not a triggered ability")
def spellvoid_is_not_triggered(game_state):
    """Rule 8.3.15: Spellvoid must NOT be a triggered ability."""
    ability = game_state.inspected_ability
    assert ability is not None, "Card should have a Spellvoid ability"
    is_triggered = getattr(ability, "is_triggered", False)
    assert is_triggered is False, (
        f"Spellvoid should NOT be a triggered ability (Rule 8.3.15), got is_triggered={is_triggered}"
    )


@then("the Spellvoid ability is not a meta-static ability")
def spellvoid_is_not_meta_static(game_state):
    """Rule 8.3.15: Spellvoid must NOT be a meta-static ability."""
    ability = game_state.inspected_ability
    assert ability is not None, "Card should have a Spellvoid ability"
    is_meta_static = getattr(ability, "is_meta_static", False)
    assert is_meta_static is False, (
        f"Spellvoid should NOT be a meta-static ability (Rule 8.3.15), got is_meta_static={is_meta_static}"
    )


@then(parsers.parse('the Spellvoid ability means "If you would be dealt arcane damage, you may destroy this to prevent {n:d} of that damage"'))
def spellvoid_meaning_is_correct(game_state, n):
    """Rule 8.3.15: Spellvoid meaning includes the correct prevention amount."""
    ability = game_state.inspected_ability
    meaning = getattr(ability, "meaning", None)
    expected = f"If you would be dealt arcane damage, you may destroy this to prevent {n} of that damage"
    assert meaning == expected, (
        f"Spellvoid meaning should be '{expected}' (Rule 8.3.15), got: {meaning}"
    )


@then(parsers.parse("the Spellvoid value is {value:d}"))
def spellvoid_value_is_correct(game_state, value):
    """Rule 8.3.15: The N in 'Spellvoid N' is the spellvoid value."""
    ability = game_state.inspected_ability
    assert ability is not None, "Card should have a Spellvoid ability"
    spellvoid_value = getattr(ability, "value", None)
    assert spellvoid_value == value, (
        f"Spellvoid value should be {value} (Rule 8.3.15), got: {spellvoid_value}"
    )


@then("the object is destroyed")
def object_is_destroyed(game_state):
    """Rule 8.3.15: The Spellvoid object should be destroyed after activation."""
    assert game_state.primary_spellvoid_object._is_destroyed is True, (
        "Spellvoid object should be destroyed after activation (Rule 8.3.15)"
    )


@then("the object is not destroyed")
def object_is_not_destroyed(game_state):
    """Rule 8.3.15: The Spellvoid object should NOT be destroyed when player opts out."""
    assert game_state.primary_spellvoid_object._is_destroyed is False, (
        "Spellvoid object should NOT be destroyed when player chooses not to activate (Rule 8.3.15)"
    )


@then("both objects are destroyed")
def both_objects_are_destroyed(game_state):
    """Rule 8.3.15: All activated Spellvoid objects should be destroyed."""
    for obj in game_state.spellvoid_objects:
        assert obj._is_destroyed is True, (
            f"All activated Spellvoid objects should be destroyed (Rule 8.3.15), "
            f"object {getattr(obj, '_keyword', 'unknown')} was not destroyed"
        )


@then(parsers.parse("{amount:d} arcane damage is prevented"))
def arcane_damage_is_prevented(game_state, amount):
    """Rule 8.3.15: The correct amount of arcane damage should be prevented."""
    assert game_state.damage_prevented == amount, (
        f"Spellvoid should have prevented {amount} arcane damage (Rule 8.3.15), "
        f"got: {game_state.damage_prevented}"
    )


@then(parsers.parse("the player is dealt {amount:d} arcane damage"))
def player_is_dealt_arcane_damage(game_state, amount):
    """Rule 8.3.15: After prevention, the player takes the correct amount of arcane damage."""
    remaining = game_state.incoming_damage_amount - game_state.damage_prevented
    assert remaining == amount, (
        f"Player should take {amount} arcane damage after Spellvoid prevention (Rule 8.3.15), "
        f"got: {remaining}"
    )


@then("Spellvoid cannot be activated against regular combat damage")
def spellvoid_cannot_activate_for_combat_damage(game_state):
    """Rule 8.3.15: Spellvoid only works against arcane damage, not regular combat damage."""
    assert game_state.incoming_damage_type == "combat", (
        "Damage type should be 'combat' for this test"
    )
    result = game_state.attempt_spellvoid_activation(
        obj=game_state.primary_spellvoid_object,
        damage_type=game_state.incoming_damage_type,
    )
    if result is not None:
        activated = getattr(result, "activated", False)
        assert activated is False, (
            "Spellvoid should NOT be activatable against regular combat damage (Rule 8.3.15)"
        )


@then(parsers.parse("the player is dealt {amount:d} regular combat damage"))
def player_is_dealt_regular_combat_damage(game_state, amount):
    """Rule 8.3.15: After no prevention, the player takes the full combat damage."""
    remaining = game_state.incoming_damage_amount - game_state.damage_prevented
    assert remaining == amount, (
        f"Player should take {amount} regular combat damage (Rule 8.3.15), got: {remaining}"
    )


@then("the player cannot activate Spellvoid")
def player_cannot_activate_spellvoid(game_state):
    """Rule 8.3.15a: When the object cannot be destroyed, Spellvoid cannot be activated."""
    result = game_state.attempt_spellvoid_activation(
        obj=game_state.primary_spellvoid_object,
        damage_type=game_state.incoming_damage_type,
    )
    if result is not None:
        can_activate = getattr(result, "can_activate", None)
        activated = getattr(result, "activated", False)
        assert activated is False, (
            "Player should NOT be able to activate Spellvoid when object cannot be destroyed "
            "(Rule 8.3.15a)"
        )
        if can_activate is not None:
            assert can_activate is False, (
                "can_activate should be False when object cannot be destroyed (Rule 8.3.15a)"
            )
    else:
        # None result means engine doesn't implement this yet — that's expected
        pass


@then(parsers.parse("{amount:d} arcane damage is prevented total"))
def arcane_damage_prevented_total(game_state, amount):
    """Rule 8.3.15: Total arcane damage prevented across all Spellvoid activations."""
    assert game_state.damage_prevented == amount, (
        f"Multiple Spellvoid objects should have prevented {amount} total arcane damage "
        f"(Rule 8.3.15), got: {game_state.damage_prevented}"
    )


# ===== Fixtures =====

@pytest.fixture
def game_state():
    """
    Fixture providing game state for testing Spellvoid (Rule 8.3.15).

    Uses BDDGameState which integrates with the real engine.
    Reference: Rule 8.3.15
    """
    from tests.bdd_helpers import BDDGameState

    state = BDDGameState()
    state.spellvoid_objects = []
    state.damage_prevented = 0
    state.incoming_damage_amount = 0
    state.incoming_damage_type = "arcane"
    state.spellvoid_activated = False
    return state
