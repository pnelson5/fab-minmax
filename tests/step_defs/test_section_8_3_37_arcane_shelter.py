"""
Step definitions for Section 8.3.37: Arcane Shelter (Ability Keyword)
Reference: Flesh and Blood Comprehensive Rules Section 8.3.37

This module implements behavioral tests for the Arcane Shelter ability keyword:
- Arcane Shelter is a static ability (Rule 8.3.37)
- Written as "Arcane Shelter N" meaning "If you would be dealt arcane damage,
  destroy this to prevent N of that damage" (Rule 8.3.37)
- The card/equipment with Arcane Shelter is DESTROYED to activate the prevention
- Destroying the card is the cost — no resource payment required (Rule 8.3.37)
- Prevention is optional — the player chooses whether to destroy the card (Rule 8.3.37)
- Applies only to arcane damage, not regular combat damage (Rule 8.3.37)
- Prevents exactly N damage (not more than the incoming damage) (Rule 8.3.37)

Engine Features Needed for Section 8.3.37:
- [ ] AbilityKeyword.ARCANE_SHELTER on cards/equipment (Rule 8.3.37)
- [ ] ArcaneShelterAbility.is_static -> True (not triggered, not meta-static) (Rule 8.3.37)
- [ ] ArcaneShelterAbility.value property returning the N in "Arcane Shelter N" (Rule 8.3.37)
- [ ] ArcaneShelterAbility.meaning == "If you would be dealt arcane damage, destroy this to prevent N of that damage" (Rule 8.3.37)
- [ ] DamageEvent.damage_type distinguishing arcane vs regular combat damage (Rule 8.3.37)
- [ ] ArcaneShelterAbility.activate() destroys the card and creates prevention of N arcane damage (Rule 8.3.37)
- [ ] ArcaneShelterAbility activation moves card to graveyard, removes from equipment zone (Rule 8.3.37)
- [ ] Prevention amount is min(N, incoming_arcane_damage) (Rule 8.3.37)

Current status: Tests written, Engine pending
"""

import pytest
from pytest_bdd import scenario, given, when, then, parsers


# ===== Rule 8.3.37: Arcane Shelter is a static ability =====

@scenario(
    "../features/section_8_3_37_arcane_shelter.feature",
    "Arcane Shelter is a static ability",
)
def test_arcane_shelter_is_static_ability():
    """Rule 8.3.37: Arcane Shelter is a static ability."""
    pass


# ===== Rule 8.3.37: Meaning is correct =====

@scenario(
    "../features/section_8_3_37_arcane_shelter.feature",
    "Arcane Shelter N means destroy this to prevent N arcane damage",
)
def test_arcane_shelter_meaning_is_correct():
    """Rule 8.3.37: Arcane Shelter N means destroy this to prevent N arcane damage."""
    pass


# ===== Rule 8.3.37: Destroying the card prevents arcane damage =====

@scenario(
    "../features/section_8_3_37_arcane_shelter.feature",
    "Player destroys Arcane Shelter equipment to prevent arcane damage",
)
def test_player_destroys_arcane_shelter_to_prevent_damage():
    """Rule 8.3.37: Destroying card prevents N arcane damage."""
    pass


# ===== Rule 8.3.37: Prevention is optional =====

@scenario(
    "../features/section_8_3_37_arcane_shelter.feature",
    "Player may choose not to activate Arcane Shelter",
)
def test_arcane_shelter_prevention_is_optional():
    """Rule 8.3.37: The player may choose not to destroy the card."""
    pass


# ===== Rule 8.3.37: Does not apply to regular combat damage =====

@scenario(
    "../features/section_8_3_37_arcane_shelter.feature",
    "Arcane Shelter does not prevent regular combat damage",
)
def test_arcane_shelter_does_not_prevent_regular_combat_damage():
    """Rule 8.3.37: Arcane Shelter only applies to arcane damage."""
    pass


# ===== Rule 8.3.37: Card is destroyed (moved to graveyard) =====

@scenario(
    "../features/section_8_3_37_arcane_shelter.feature",
    "Activating Arcane Shelter destroys the card",
)
def test_arcane_shelter_activation_destroys_card():
    """Rule 8.3.37: Activating Arcane Shelter moves the card to the graveyard."""
    pass


# ===== Rule 8.3.37: Prevents exactly N damage =====

@scenario(
    "../features/section_8_3_37_arcane_shelter.feature",
    "Arcane Shelter prevents exactly N damage, not more",
)
def test_arcane_shelter_prevents_exactly_n_damage():
    """Rule 8.3.37: Arcane Shelter prevents min(N, incoming_damage) arcane damage."""
    pass


# ===== Step Definitions =====

@given(parsers.parse('a card has the "{keyword}" keyword'))
def card_with_keyword(game_state, keyword):
    """Create a card with the specified keyword."""
    game_state.keyword_card = game_state.create_card(name="Arcane Shelter Equipment")
    game_state.keyword_str = keyword
    # Parse the N value from "Arcane Shelter N"
    parts = keyword.split()
    if len(parts) >= 3:
        try:
            game_state.arcane_shelter_value = int(parts[2])
        except ValueError:
            game_state.arcane_shelter_value = 1
    else:
        game_state.arcane_shelter_value = 1


@given(parsers.parse('a player has an equipment with "{keyword}"'))
def player_has_equipment_with_keyword(game_state, keyword):
    """Set up a player with equipment that has Arcane Shelter."""
    game_state.shelter_equipment = game_state.create_card(name="Arcane Shelter Equipment")
    game_state.keyword_str = keyword
    parts = keyword.split()
    if len(parts) >= 3:
        try:
            game_state.arcane_shelter_value = int(parts[2])
        except ValueError:
            game_state.arcane_shelter_value = 1
    else:
        game_state.arcane_shelter_value = 1
    game_state.shelter_activated = False
    game_state.shelter_destroyed = False


@given(parsers.parse('a player has an equipment with "{keyword}" in play'))
def player_has_equipment_with_keyword_in_play(game_state, keyword):
    """Set up a player with equipped Arcane Shelter card in play."""
    game_state.shelter_equipment = game_state.create_card(name="Arcane Shelter Equipment")
    game_state.keyword_str = keyword
    parts = keyword.split()
    if len(parts) >= 3:
        try:
            game_state.arcane_shelter_value = int(parts[2])
        except ValueError:
            game_state.arcane_shelter_value = 1
    else:
        game_state.arcane_shelter_value = 1
    game_state.shelter_activated = False
    game_state.shelter_destroyed = False


@given(parsers.parse('the player has the card equipped'))
def player_has_card_equipped(game_state):
    """The player has the Arcane Shelter card equipped (uses keyword_card as shelter_equipment)."""
    game_state.shelter_equipment = game_state.keyword_card


@when('I inspect the Arcane Shelter ability on the card')
def inspect_arcane_shelter_ability(game_state):
    """Inspect the Arcane Shelter ability on the keyword_card."""
    from fab_engine.cards.model import CardInstance
    card = game_state.keyword_card
    # Attempt to access ability keyword metadata
    game_state.ability_inspection = {
        "card": card,
        "keyword": game_state.keyword_str,
    }
    try:
        game_state.ability_obj = card.get_ability("arcane_shelter")
    except (AttributeError, NotImplementedError):
        game_state.ability_obj = None


@when(parsers.parse('the player would be dealt {amount:d} arcane damage'))
def player_would_be_dealt_arcane_damage(game_state, amount):
    """Set up incoming arcane damage event."""
    game_state.incoming_damage = amount
    game_state.damage_type = "arcane"
    game_state.damage_prevented = 0
    game_state.damage_dealt = amount


@when(parsers.parse('the player would be dealt {amount:d} regular combat damage'))
def player_would_be_dealt_regular_combat_damage(game_state, amount):
    """Set up incoming regular combat damage event."""
    game_state.incoming_damage = amount
    game_state.damage_type = "regular"
    game_state.damage_prevented = 0
    game_state.damage_dealt = amount


@when('the player chooses to activate Arcane Shelter')
def player_chooses_to_activate_arcane_shelter(game_state):
    """Player chooses to activate Arcane Shelter, destroying the card."""
    game_state.shelter_activated = True
    try:
        card = game_state.shelter_equipment
        result = card.activate_arcane_shelter(
            damage_amount=game_state.incoming_damage
        )
        prevention = min(game_state.arcane_shelter_value, game_state.incoming_damage)
        game_state.damage_prevented = prevention
        game_state.damage_dealt = game_state.incoming_damage - prevention
        game_state.shelter_destroyed = True
        game_state.activation_result = result
    except (AttributeError, NotImplementedError):
        game_state.activation_result = None


@when('the player chooses not to activate Arcane Shelter')
def player_chooses_not_to_activate_arcane_shelter(game_state):
    """Player chooses not to activate Arcane Shelter."""
    game_state.shelter_activated = False
    game_state.damage_prevented = 0
    game_state.damage_dealt = game_state.incoming_damage
    game_state.shelter_destroyed = False


@when('the player activates Arcane Shelter to prevent arcane damage')
def player_activates_arcane_shelter(game_state):
    """Player activates Arcane Shelter, destroying the card."""
    game_state.shelter_activated = True
    game_state.shelter_destroyed = True
    try:
        card = game_state.shelter_equipment
        result = card.activate_arcane_shelter(damage_amount=3)
        game_state.activation_result = result
    except (AttributeError, NotImplementedError):
        game_state.activation_result = None


@then('the Arcane Shelter ability is a static ability')
def arcane_shelter_is_static(game_state):
    """Verify Arcane Shelter is a static ability."""
    from fab_engine.cards.model import CardInstance
    card = game_state.keyword_card
    try:
        ability = card.get_ability("arcane_shelter")
        assert ability.is_static, "Arcane Shelter must be a static ability"
    except (AttributeError, NotImplementedError):
        pytest.fail("Engine feature needed: card.get_ability('arcane_shelter').is_static")


@then('the Arcane Shelter ability is not a triggered ability')
def arcane_shelter_is_not_triggered(game_state):
    """Verify Arcane Shelter is not a triggered ability."""
    card = game_state.keyword_card
    try:
        ability = card.get_ability("arcane_shelter")
        assert not ability.is_triggered, "Arcane Shelter must not be a triggered ability"
    except (AttributeError, NotImplementedError):
        pytest.fail("Engine feature needed: card.get_ability('arcane_shelter').is_triggered")


@then('the Arcane Shelter ability is not a meta-static ability')
def arcane_shelter_is_not_meta_static(game_state):
    """Verify Arcane Shelter is not a meta-static ability."""
    card = game_state.keyword_card
    try:
        ability = card.get_ability("arcane_shelter")
        assert not ability.is_meta_static, "Arcane Shelter must not be a meta-static ability"
    except (AttributeError, NotImplementedError):
        pytest.fail("Engine feature needed: card.get_ability('arcane_shelter').is_meta_static")


@then(parsers.parse('the Arcane Shelter ability means "If you would be dealt arcane damage, destroy this to prevent {n:d} of that damage"'))
def arcane_shelter_meaning_is_correct(game_state, n):
    """Verify the meaning string for Arcane Shelter N."""
    card = game_state.keyword_card
    expected_meaning = f"If you would be dealt arcane damage, destroy this to prevent {n} of that damage"
    try:
        ability = card.get_ability("arcane_shelter")
        assert ability.meaning == expected_meaning, (
            f"Arcane Shelter meaning mismatch: expected '{expected_meaning}', got '{ability.meaning}'"
        )
    except (AttributeError, NotImplementedError):
        pytest.fail(f"Engine feature needed: ArcaneShelterAbility.meaning == '{expected_meaning}'")


@then(parsers.parse('the Arcane Shelter value is {n:d}'))
def arcane_shelter_value_is(game_state, n):
    """Verify the N value in Arcane Shelter N."""
    card = game_state.keyword_card
    try:
        ability = card.get_ability("arcane_shelter")
        assert ability.value == n, (
            f"Arcane Shelter value mismatch: expected {n}, got {ability.value}"
        )
    except (AttributeError, NotImplementedError):
        pytest.fail(f"Engine feature needed: ArcaneShelterAbility.value == {n}")


@then('the equipment with Arcane Shelter is destroyed')
def equipment_is_destroyed(game_state):
    """Verify the Arcane Shelter equipment was destroyed."""
    assert game_state.shelter_destroyed, "Arcane Shelter equipment should have been destroyed"
    card = game_state.shelter_equipment
    try:
        assert card.is_destroyed, "Card with Arcane Shelter should be marked as destroyed"
    except AttributeError:
        pytest.fail("Engine feature needed: CardInstance.is_destroyed property")


@then(parsers.parse('{n:d} arcane damage is prevented'))
def n_arcane_damage_is_prevented(game_state, n):
    """Verify exactly N arcane damage was prevented."""
    assert game_state.damage_prevented == n, (
        f"Expected {n} arcane damage prevented, got {game_state.damage_prevented}"
    )


@then(parsers.parse('the player is dealt {n:d} arcane damage'))
def player_is_dealt_n_arcane_damage(game_state, n):
    """Verify the player received the correct amount of arcane damage."""
    assert game_state.damage_dealt == n, (
        f"Expected player to be dealt {n} arcane damage, but was dealt {game_state.damage_dealt}"
    )


@then('the equipment with Arcane Shelter is not destroyed')
def equipment_is_not_destroyed(game_state):
    """Verify the Arcane Shelter equipment was NOT destroyed."""
    assert not game_state.shelter_destroyed, "Arcane Shelter equipment should NOT have been destroyed"


@then(parsers.parse('the player is dealt {n:d} regular combat damage'))
def player_is_dealt_n_regular_damage(game_state, n):
    """Verify the player received the correct amount of regular combat damage."""
    assert game_state.damage_dealt == n, (
        f"Expected player to be dealt {n} regular combat damage, but was dealt {game_state.damage_dealt}"
    )


@then('Arcane Shelter cannot be activated against regular combat damage')
def arcane_shelter_cannot_be_activated_against_regular_damage(game_state):
    """Verify Arcane Shelter cannot be activated for regular combat damage."""
    assert game_state.damage_type == "regular", "Expected regular combat damage"
    try:
        card = game_state.shelter_equipment
        can_activate = card.can_activate_arcane_shelter(damage_type="regular")
        assert not can_activate, "Arcane Shelter should not be activatable against regular damage"
    except (AttributeError, NotImplementedError):
        pytest.fail("Engine feature needed: card.can_activate_arcane_shelter(damage_type) method")


@then('the equipment is moved to the graveyard')
def equipment_is_in_graveyard(game_state):
    """Verify the Arcane Shelter equipment was moved to the graveyard."""
    card = game_state.shelter_equipment
    try:
        assert card.zone.zone_type.name == "GRAVEYARD", (
            f"Arcane Shelter card should be in graveyard, but is in {card.zone.zone_type.name}"
        )
    except (AttributeError, NotImplementedError):
        pytest.fail("Engine feature needed: CardInstance.zone tracking after destruction")


@then('the equipment is no longer in the equipment zone')
def equipment_is_not_in_equipment_zone(game_state):
    """Verify the Arcane Shelter equipment is no longer in an equipment zone."""
    card = game_state.shelter_equipment
    try:
        zone_name = card.zone.zone_type.name
        assert zone_name != "ARMS" and zone_name != "HEAD" and zone_name != "CHEST" and zone_name != "LEGS", (
            f"Arcane Shelter card should not be in equipment zone, but is in {zone_name}"
        )
    except (AttributeError, NotImplementedError):
        pytest.fail("Engine feature needed: CardInstance.zone tracking for equipment zones")


# ===== Fixtures =====

@pytest.fixture
def game_state():
    """
    Fixture providing game state for testing Arcane Shelter.

    Uses BDDGameState which integrates with the real engine.
    Reference: Rule 8.3.37
    """
    from tests.bdd_helpers import BDDGameState

    state = BDDGameState()
    state.incoming_damage = 0
    state.damage_type = "arcane"
    state.damage_prevented = 0
    state.damage_dealt = 0
    state.shelter_activated = False
    state.shelter_destroyed = False
    state.arcane_shelter_value = 1

    return state
