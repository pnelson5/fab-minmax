"""
Step definitions for Section 8.3.20: Ward (Ability Keyword)
Reference: Flesh and Blood Comprehensive Rules Section 8.3.20

This module implements behavioral tests for the Ward ability keyword:
- Ward is a static ability (Rule 8.3.20)
- Written as "Ward N" meaning "If you would be dealt damage, destroy this to
  prevent N of that damage." (Rule 8.3.20)
- Unlike Quell, Ward has no resource cost — the card is destroyed immediately
  as the cost of preventing damage (Rule 8.3.20)

Engine Features Needed for Section 8.3.20:
- [ ] WardAbility class as a static ability (Rule 8.3.20)
- [ ] WardAbility.is_static -> True (Rule 8.3.20)
- [ ] WardAbility.n: int — the prevention amount N (Rule 8.3.20)
- [ ] WardAbility.meaning: formatted ability text string (Rule 8.3.20)
- [ ] WardAction.activate(player, incoming_damage) -> WardResult (Rule 8.3.20)
- [ ] WardResult.damage_prevented: int — should equal N when used (Rule 8.3.20)
- [ ] WardResult.success: bool (Rule 8.3.20)
- [ ] WardResult.card_destroyed: bool — True when Ward was used (Rule 8.3.20)
- [ ] WardResult.net_damage: int — incoming_damage minus N (Rule 8.3.20)
- [ ] Immediate destruction of Ward card when activated (not at end phase) (Rule 8.3.20)
- [ ] DamageReplacementEffect: replaces incoming damage using Ward prevention (Rule 8.3.20)

Current status: Tests written, Engine pending
"""

import pytest
from pytest_bdd import scenario, given, when, then, parsers


# ===== Rule 8.3.20: Ward is a static ability =====

@scenario(
    "../features/section_8_3_20_ward.feature",
    "Ward is a static ability",
)
def test_ward_is_static_ability():
    """Rule 8.3.20: Ward must be a static ability."""
    pass


@scenario(
    "../features/section_8_3_20_ward.feature",
    "Ward ability has the correct N value",
)
def test_ward_has_correct_n_value():
    """Rule 8.3.20: Ward ability stores N for the prevention amount."""
    pass


# ===== Rule 8.3.20: Destroying Ward card prevents N damage =====

@scenario(
    "../features/section_8_3_20_ward.feature",
    "Destroying a Ward 1 card prevents 1 damage",
)
def test_ward_1_prevents_1_damage():
    """Rule 8.3.20: Destroying a Ward 1 card prevents exactly 1 damage."""
    pass


@scenario(
    "../features/section_8_3_20_ward.feature",
    "Destroying a Ward 2 card prevents 2 damage",
)
def test_ward_2_prevents_2_damage():
    """Rule 8.3.20: Destroying a Ward 2 card prevents exactly 2 damage."""
    pass


# ===== Rule 8.3.20: Ward prevents exactly N damage =====

@scenario(
    "../features/section_8_3_20_ward.feature",
    "Ward only prevents exactly N damage, not more",
)
def test_ward_prevents_exactly_n_damage():
    """Rule 8.3.20: Ward prevents exactly N damage, not more."""
    pass


# ===== Rule 8.3.20: Ward card is destroyed immediately =====

@scenario(
    "../features/section_8_3_20_ward.feature",
    "Ward card is destroyed immediately when used",
)
def test_ward_card_destroyed_immediately():
    """Rule 8.3.20: Ward card is destroyed immediately upon use (not at end phase)."""
    pass


# ===== Rule 8.3.20: Ward is optional =====

@scenario(
    "../features/section_8_3_20_ward.feature",
    "Player may choose not to use Ward",
)
def test_ward_is_optional():
    """Rule 8.3.20: Ward use is optional — player may choose not to destroy the card."""
    pass


# ===== Rule 8.3.20: Ward requires no resource payment =====

@scenario(
    "../features/section_8_3_20_ward.feature",
    "Ward requires no resource payment, only destruction of the card",
)
def test_ward_requires_no_resources():
    """Rule 8.3.20: Ward has no resource cost, only the card destruction cost."""
    pass


# ===== Rule 8.3.20: Ward meaning text =====

@scenario(
    "../features/section_8_3_20_ward.feature",
    "Ward ability has the correct meaning text",
)
def test_ward_meaning_text():
    """Rule 8.3.20: Ward ability meaning describes destroying the card to prevent N damage."""
    pass


# ===== Step Definitions =====

@given(parsers.parse('a card with "{ward_text}" ability'))
def card_with_ward_ability(game_state, ward_text):
    """Rule 8.3.20: Create a card with the specified Ward ability text."""
    card = game_state.create_card(name=f"Test Ward Card ({ward_text})")
    card._ward_ability_text = ward_text  # type: ignore[attr-defined]
    parts = ward_text.split()
    n = int(parts[1]) if len(parts) >= 2 and parts[1].isdigit() else 1
    card._ward_n = n  # type: ignore[attr-defined]
    game_state.ward_card = card


@given(parsers.parse('a player has an equipment with "{ward_text}" ability equipped'))
def player_has_ward_equipment_equipped(game_state, ward_text):
    """Rule 8.3.20: Create a card with Ward that is equipped to the player."""
    card = game_state.create_card(name=f"Test Ward Equipment ({ward_text})")
    card._ward_ability_text = ward_text  # type: ignore[attr-defined]
    parts = ward_text.split()
    n = int(parts[1]) if len(parts) >= 2 and parts[1].isdigit() else 1
    card._ward_n = n  # type: ignore[attr-defined]
    # Record the equipped card on game_state
    game_state.ward_card = card
    game_state._ward_equipped = True  # type: ignore[attr-defined]


@given(parsers.parse('the player has {amount:d} resource points'))
def player_has_resource_points_ward(game_state, amount):
    """Rule 8.3.20: Set the player's resource points (Ward requires none)."""
    game_state.set_player_resource_points(game_state.player, amount)


# ===== When steps =====

@when("I inspect the Ward ability type")
def inspect_ward_ability_type(game_state):
    """Rule 8.3.20: Inspect the ability type of the Ward ability."""
    card = game_state.ward_card
    from fab_engine.abilities import WardAbility  # type: ignore[import]
    ability = WardAbility(n=card._ward_n)
    game_state._ward_ability_instance = ability  # type: ignore[attr-defined]


@when(parsers.parse("the player would be dealt {amount:d} damage"))
def player_would_be_dealt_damage_ward(game_state, amount):
    """Rule 8.3.20: Set up incoming damage amount for Ward to respond to."""
    game_state._incoming_damage = amount  # type: ignore[attr-defined]


@when("the player destroys the Ward card to prevent damage")
def player_destroys_ward_card(game_state):
    """Rule 8.3.20: Player destroys the Ward card to prevent N damage."""
    card = game_state.ward_card
    from fab_engine.abilities import WardAbility, WardAction  # type: ignore[import]
    n = getattr(card, "_ward_n", 1)
    ability = WardAbility(n=n)
    action = WardAction(ability=ability, card=card, player=game_state.player)
    incoming = getattr(game_state, "_incoming_damage", 0)
    result = action.activate(game_state.player, incoming_damage=incoming)
    game_state._ward_used = True  # type: ignore[attr-defined]
    game_state._ward_result = result  # type: ignore[attr-defined]


@when("the player does not use Ward")
def player_does_not_use_ward(game_state):
    """Rule 8.3.20: Player opts not to use Ward (optional ability)."""
    game_state._ward_used = False  # type: ignore[attr-defined]
    game_state._ward_result = None  # type: ignore[attr-defined]


# ===== Then steps =====

@then("the Ward ability is a static ability")
def ward_is_static(game_state):
    """Rule 8.3.20: Ward ability must be a static ability."""
    ability = game_state._ward_ability_instance
    assert hasattr(ability, "is_static"), "WardAbility must have is_static attribute"
    assert ability.is_static is True, "WardAbility must be a static ability"


@then(parsers.parse("the Ward ability has N equal to {n:d}"))
def ward_has_n_equal_to(game_state, n):
    """Rule 8.3.20: Ward ability must store the correct N value."""
    ability = game_state._ward_ability_instance
    assert hasattr(ability, "n"), "WardAbility must have an n attribute"
    assert ability.n == n, f"Expected WardAbility.n == {n}, got {ability.n}"


@then(parsers.parse("{count:d} damage is prevented by Ward"))
def damage_is_prevented_by_ward(game_state, count):
    """Rule 8.3.20: N damage must be prevented when Ward card is destroyed."""
    result = game_state._ward_result
    assert result is not None, "WardAction.activate must return a result"
    assert result.success is True, "Ward activation must succeed"
    prevented = getattr(result, "damage_prevented", None)
    assert prevented is not None, "WardResult must include damage_prevented"
    assert prevented == count, f"Expected {count} damage prevented, got {prevented}"


@then(parsers.parse("{count:d} damage are prevented by Ward"))
def damage_are_prevented_by_ward(game_state, count):
    """Rule 8.3.20: N damage must be prevented when Ward card is destroyed."""
    result = game_state._ward_result
    assert result is not None, "WardAction.activate must return a result"
    assert result.success is True, "Ward activation must succeed"
    prevented = getattr(result, "damage_prevented", None)
    assert prevented is not None, "WardResult must include damage_prevented"
    assert prevented == count, f"Expected {count} damage prevented, got {prevented}"


@then(parsers.parse("exactly {count:d} damage is prevented by Ward"))
def exactly_damage_is_prevented_by_ward(game_state, count):
    """Rule 8.3.20: Exactly N damage must be prevented (not more)."""
    result = game_state._ward_result
    assert result is not None, "WardAction.activate must return a result"
    prevented = getattr(result, "damage_prevented", None)
    assert prevented is not None, "WardResult must include damage_prevented"
    assert prevented == count, \
        f"Ward should prevent exactly {count} damage, got {prevented}"


@then(parsers.parse("the player takes {amount:d} damage instead"))
def player_takes_reduced_damage_ward(game_state, amount):
    """Rule 8.3.20: Player takes incoming damage minus prevented damage."""
    result = game_state._ward_result
    assert result is not None, "WardAction.activate must return a result"
    net_damage = getattr(result, "net_damage", None)
    assert net_damage is not None, "WardResult must include net_damage"
    assert net_damage == amount, \
        f"Expected player to take {amount} damage, got {net_damage}"


@then("the Ward card is immediately destroyed")
def ward_card_is_immediately_destroyed(game_state):
    """Rule 8.3.20: Ward card must be destroyed immediately upon use (not at end phase)."""
    result = game_state._ward_result
    assert result is not None, "WardAction.activate must return a result"
    card_destroyed = getattr(result, "card_destroyed", None)
    assert card_destroyed is True, \
        "WardResult must indicate card_destroyed=True immediately when Ward is used (Rule 8.3.20)"


@then("no damage is prevented by Ward")
def no_damage_prevented_by_ward(game_state):
    """Rule 8.3.20: No damage prevented when player chooses not to use Ward."""
    result = getattr(game_state, "_ward_result", None)
    if result is not None:
        prevented = getattr(result, "damage_prevented", 0)
        assert prevented == 0, "No damage should be prevented when Ward is not used"
    # No result means player declined — no prevention occurred


@then("the Ward card is not destroyed")
def ward_card_not_destroyed(game_state):
    """Rule 8.3.20: Ward card must NOT be destroyed if player did not use Ward."""
    result = getattr(game_state, "_ward_result", None)
    if result is not None:
        card_destroyed = getattr(result, "card_destroyed", False)
        assert card_destroyed is False, \
            "Ward card must NOT be destroyed when Ward was not used (Rule 8.3.20)"
    # No result means Ward was not used — card survives


@then(parsers.parse("the Ward ability meaning includes preventing {n:d} damage by destroying the card"))
def ward_meaning_includes_prevention(game_state, n):
    """Rule 8.3.20: Ward ability meaning must reference destroying the card to prevent N damage."""
    ability = game_state._ward_ability_instance
    assert hasattr(ability, "meaning"), "WardAbility must have a meaning attribute"
    meaning = ability.meaning
    assert meaning is not None, "WardAbility.meaning must not be None"
    meaning_lower = meaning.lower()
    assert "destroy" in meaning_lower, \
        "Ward meaning must mention destroying the card (Rule 8.3.20)"
    assert str(n) in meaning, \
        f"Ward meaning must include the N value ({n}) (Rule 8.3.20)"


# ===== Fixtures =====

@pytest.fixture
def game_state():
    """
    Fixture providing game state for testing Ward ability.

    Uses BDDGameState which integrates with the real engine.
    Reference: Rule 8.3.20 — Ward ability keyword
    """
    from tests.bdd_helpers import BDDGameState

    state = BDDGameState()
    state.ward_card = None
    state._ward_ability_instance = None
    state._ward_used = False
    state._ward_result = None
    state._incoming_damage = 0
    state._ward_equipped = False

    return state
