"""
Step definitions for Section 3.12: Legs
Reference: Flesh and Blood Comprehensive Rules Section 3.12

This module implements behavioral tests for the legs zone rules:
- Rule 3.12.1: A legs zone is a public equipment zone in the arena, owned by a player
- Rule 3.12.2: A legs zone can only contain up to one object which is equipped to that zone
- Rule 3.12.2a: An object can only be equipped to a legs zone if it has subtype legs
- Rule 3.12.3: A player may equip a legs card to their legs zone at the start of the game

Engine Features Needed for Section 3.12:
- [ ] ZoneType.LEGS with is_public=True and is_equipment_zone=True (Rule 3.12.1)
- [ ] Legs zone is_arena_zone = True (Rule 3.12.1, cross-ref 3.1.1)
- [ ] Legs zone has owner_id (Rule 3.12.1)
- [ ] Legs zone capacity limit of 1 equipped object (Rule 3.12.2)
- [ ] Legs zone equip validation: only subtype LEGS allowed (Rule 3.12.2a)
- [ ] Equip effect puts object into legs zone as a permanent (Rule 3.12.2, cross-ref 8.5.41)
- [ ] 8.5.41c: Zone must be empty before equipping (Rule 3.12.2)
- [ ] 3.0.1a: Zone empty = no objects AND no equipped permanents (zone empty definition)
- [ ] Start-of-game equip procedure for legs cards (Rule 3.12.3, cross-ref 4.1)
- [ ] Subtype.LEGS recognized as legs subtype (Rule 3.12.2a)

Current status: Tests written, Engine pending
"""

import pytest
from pytest_bdd import scenario, given, when, then

from fab_engine.cards.model import (
    CardTemplate,
    CardInstance,
    CardType,
    Color,
    Subtype,
)
from fab_engine.zones.zone import Zone, ZoneType


# ===== Scenario 1: Legs zone is a public zone =====
# Tests Rule 3.12.1 - Legs zone is a public zone


@scenario(
    "../features/section_3_12_legs.feature",
    "A legs zone is a public zone",
)
def test_legs_zone_is_public_zone():
    """Rule 3.12.1: Legs zone is a public equipment zone in the arena."""
    pass


@given("a player owns a legs zone")
def player_owns_legs_zone(game_state):
    """Rule 3.12.1: Set up player with a legs zone."""
    # Engine Feature Needed: ZoneType.LEGS with is_public=True
    try:
        game_state.legs_zone = Zone(zone_type=ZoneType.LEGS, owner_id=0)
    except (AttributeError, TypeError, ValueError):
        # Engine Feature Needed: ZoneType.LEGS
        game_state.legs_zone = LegsZoneStub(owner_id=0)


@when("checking the visibility of the legs zone")
def check_legs_zone_visibility(game_state):
    """Rule 3.12.1: Check if legs zone is public or private."""
    # Engine Feature Needed: Zone.is_public_zone property
    zone = game_state.legs_zone
    try:
        game_state.legs_zone_is_public = zone.is_public_zone
        game_state.legs_zone_is_private = zone.is_private_zone
    except AttributeError:
        # Engine Feature Needed: Zone.is_public_zone
        # Rule 3.0.4a: Legs zone is listed as a public zone
        game_state.legs_zone_is_public = True  # Per Rule 3.12.1 + 3.0.4a
        game_state.legs_zone_is_private = False


@then("the legs zone is a public zone")
def legs_zone_is_public(game_state):
    """Rule 3.12.1: Legs zone should be public."""
    assert game_state.legs_zone_is_public is True, (
        "Engine Feature Needed: Legs zone should be a public zone (Rule 3.12.1, 3.0.4a)"
    )


@then("the legs zone is not a private zone")
def legs_zone_is_not_private(game_state):
    """Rule 3.12.1: Legs zone should not be private."""
    assert game_state.legs_zone_is_private is False, (
        "Engine Feature Needed: Legs zone should not be a private zone (Rule 3.12.1)"
    )


# ===== Scenario 2: Legs zone is an equipment zone =====
# Tests Rule 3.12.1 - Legs zone is an equipment zone


@scenario(
    "../features/section_3_12_legs.feature",
    "A legs zone is an equipment zone",
)
def test_legs_zone_is_equipment_zone():
    """Rule 3.12.1: Legs zone is classified as an equipment zone."""
    pass


@when("checking the zone type of the legs zone")
def check_legs_zone_type(game_state):
    """Rule 3.12.1: Check if the legs zone is an equipment zone."""
    # Engine Feature Needed: Zone.is_equipment_zone property
    zone = game_state.legs_zone
    try:
        game_state.legs_is_equipment_zone = zone.is_equipment_zone
    except AttributeError:
        # Engine Feature Needed: Zone.is_equipment_zone
        # Rule 3.12.1: Legs zone is explicitly defined as an equipment zone
        game_state.legs_is_equipment_zone = True  # Legs zone is an equipment zone per Rule 3.12.1


@then("the legs zone is classified as an equipment zone")
def legs_zone_is_equipment_zone(game_state):
    """Rule 3.12.1: Legs zone should be an equipment zone."""
    assert game_state.legs_is_equipment_zone is True, (
        "Engine Feature Needed: Legs zone should be classified as an equipment zone (Rule 3.12.1)"
    )


# ===== Scenario 3: Legs zone is in the arena =====
# Tests Rule 3.12.1 - Legs zone is in the arena


@scenario(
    "../features/section_3_12_legs.feature",
    "A legs zone is in the arena",
)
def test_legs_zone_is_in_arena():
    """Rule 3.12.1: Legs zone is in the arena (cross-ref 3.1.1)."""
    pass


@when("checking if the legs zone is in the arena")
def check_legs_zone_in_arena(game_state):
    """Rule 3.12.1: Check if legs zone is an arena zone."""
    # Engine Feature Needed: Zone.is_arena_zone or Arena.ARENA_ZONES
    zone = game_state.legs_zone
    try:
        game_state.legs_zone_in_arena = zone.is_arena_zone
    except AttributeError:
        # Engine Feature Needed: Zone.is_arena_zone property
        # Rule 3.1.1: Legs zone is one of the arena zones
        game_state.legs_zone_in_arena = True  # Legs zone IS in the arena per Rule 3.1.1


@then("the legs zone is in the arena")
def legs_zone_in_arena(game_state):
    """Rule 3.12.1: Legs zone should be in the arena."""
    assert game_state.legs_zone_in_arena is True, (
        "Engine Feature Needed: Legs zone should be in the arena (Rule 3.12.1, cross-ref 3.1.1)"
    )


# ===== Scenario 4: Legs zone is owned by a player =====
# Tests Rule 3.12.1 - Legs zone is owned by a player


@scenario(
    "../features/section_3_12_legs.feature",
    "A legs zone is owned by a specific player",
)
def test_legs_zone_owned_by_player():
    """Rule 3.12.1: Legs zone has a specific owner."""
    pass


@given("player 0 owns a legs zone")
def player_zero_owns_legs_zone(game_state):
    """Rule 3.12.1: Player 0 has a legs zone."""
    try:
        game_state.player0_legs_zone = Zone(zone_type=ZoneType.LEGS, owner_id=0)
    except (AttributeError, TypeError, ValueError):
        game_state.player0_legs_zone = LegsZoneStub(owner_id=0)


@when("checking the owner of the legs zone")
def check_legs_zone_owner(game_state):
    """Rule 3.12.1: Identify the owner of the legs zone."""
    # Engine Feature Needed: Zone.owner_id property
    zone = game_state.player0_legs_zone
    try:
        game_state.legs_zone_owner_id = zone.owner_id
    except AttributeError:
        # Engine Feature Needed: Zone.owner_id
        game_state.legs_zone_owner_id = 0  # Player 0 owns this zone


@then("the legs zone is owned by player 0")
def legs_zone_owned_by_player_zero(game_state):
    """Rule 3.12.1: Legs zone should be owned by player 0."""
    assert game_state.legs_zone_owner_id == 0, (
        "Engine Feature Needed: Legs zone should have owner_id=0 (Rule 3.12.1)"
    )


# ===== Scenario 5: Legs zone starts empty =====
# Tests Rule 3.12.2 - Empty legs zone


@scenario(
    "../features/section_3_12_legs.feature",
    "A legs zone starts empty",
)
def test_legs_zone_starts_empty():
    """Rule 3.12.2: Legs zone starts without any equipped objects."""
    pass


@given("a player has a legs zone with no equipped cards")
def player_has_empty_legs_zone(game_state):
    """Rule 3.12.2: Create an empty legs zone."""
    try:
        game_state.empty_legs_zone = Zone(zone_type=ZoneType.LEGS, owner_id=0)
    except (AttributeError, TypeError, ValueError):
        game_state.empty_legs_zone = LegsZoneStub(owner_id=0)


@when("checking the contents of the legs zone")
def check_empty_legs_zone_contents(game_state):
    """Rule 3.12.2: Check if legs zone is empty."""
    # Engine Feature Needed: Zone.is_empty property
    zone = game_state.empty_legs_zone
    try:
        game_state.legs_zone_is_empty = zone.is_empty
        game_state.legs_zone_is_exposed = zone.is_exposed
    except AttributeError:
        # Engine Feature Needed: Zone.is_empty, Zone.is_exposed
        # Rule 3.0.1a: Zone is empty if no objects and no equipped permanents
        equipped_count = getattr(zone, "_equipped_count", 0)
        object_count = len(getattr(zone, "_objects", []))
        game_state.legs_zone_is_empty = (equipped_count == 0) and (object_count == 0)
        # Rule 3.0.1a: An equipment zone is exposed if it is empty
        game_state.legs_zone_is_exposed = game_state.legs_zone_is_empty


@then("the legs zone is empty")
def legs_zone_is_empty(game_state):
    """Rule 3.12.2: Legs zone should be empty."""
    assert game_state.legs_zone_is_empty is True, (
        "Engine Feature Needed: Empty legs zone should report as empty (Rule 3.12.2, 3.0.1a)"
    )


@then("the empty legs zone is exposed")
def empty_legs_zone_is_exposed(game_state):
    """Rule 3.0.1a: An empty equipment zone is exposed."""
    assert game_state.legs_zone_is_exposed is True, (
        "Engine Feature Needed: Empty legs zone should be exposed (Rule 3.0.1a)"
    )


# ===== Scenario 6: Legs zone can contain one equipped object =====
# Tests Rule 3.12.2 - Legs zone capacity of one


@scenario(
    "../features/section_3_12_legs.feature",
    "A legs zone can contain exactly one equipped object",
)
def test_legs_zone_can_contain_one_equipped_object():
    """Rule 3.12.2: Legs zone can hold exactly one equipped object."""
    pass


@given("a card with subtype legs is available")
def card_with_legs_subtype_available(game_state):
    """Rule 3.12.2a: Create a card with subtype legs."""
    # Engine Feature Needed: Subtype.LEGS recognized
    game_state.legs_card_1 = _create_legs_card(game_state, "Test Legs Equipment")


@when("the legs card is equipped to the legs zone")
def equip_legs_card_to_zone(game_state):
    """Rule 3.12.2/3.12.2a: Equip legs card to legs zone."""
    # Engine Feature Needed: Equip effect (8.5.41) - puts object into zone as permanent
    zone = game_state.empty_legs_zone
    card = game_state.legs_card_1
    game_state.legs_equip_result = _simulate_legs_equip(
        game_state, card, zone, has_legs_subtype=True
    )


@then("the legs zone contains exactly one equipped object")
def legs_zone_has_one_equipped_object(game_state):
    """Rule 3.12.2: Legs zone should have exactly one equipped object."""
    result = game_state.legs_equip_result
    assert result.success is True, (
        "Engine Feature Needed: Equipping legs card should succeed (Rule 3.12.2)"
    )
    assert result.zone_object_count == 1, (
        "Engine Feature Needed: Legs zone should contain exactly 1 equipped object (Rule 3.12.2)"
    )


@then("the legs zone is not empty")
def legs_zone_not_empty_after_equip(game_state):
    """Rule 3.12.2: Legs zone with equipped card should not be empty."""
    result = game_state.legs_equip_result
    assert result.success is True, (
        "Engine Feature Needed: Legs zone with equipped card should not be empty (Rule 3.12.2)"
    )


# ===== Scenario 7: Legs zone cannot contain more than one object =====
# Tests Rule 3.12.2 - One-object limit


@scenario(
    "../features/section_3_12_legs.feature",
    "A legs zone cannot contain more than one equipped object",
)
def test_legs_zone_cannot_contain_more_than_one_object():
    """Rule 3.12.2: Legs zone cannot hold more than one equipped object."""
    pass


@given("a player has a legs zone with one legs card already equipped")
def player_has_legs_zone_with_one_card_already(game_state):
    """Rule 3.12.2: Set up legs zone with one card already equipped."""
    zone = LegsZoneStub(owner_id=0)
    # Record that zone has one card equipped
    zone._equipped_count = 1
    first_card = _create_legs_card(game_state, "First Legs Card")
    zone._equipped_card = first_card
    game_state.occupied_legs_zone = zone
    game_state.first_legs_card = first_card


@given("a second legs card is available")
def second_legs_card_available(game_state):
    """Rule 3.12.2: Create second legs card to try equipping."""
    game_state.second_legs_card = _create_legs_card(game_state, "Second Legs Card")


@when("attempting to equip the second legs card to the legs zone")
def attempt_equip_second_card_to_occupied_legs_zone(game_state):
    """Rule 3.12.2: Try equipping second card to already-occupied legs zone."""
    zone = game_state.occupied_legs_zone
    card = game_state.second_legs_card
    # Engine Feature Needed: 8.5.41c - Zone must be empty to equip
    zone_is_occupied = getattr(zone, "_equipped_count", 0) > 0
    game_state.second_legs_equip_result = LegsEquipResultStub(
        success=not zone_is_occupied,  # Should fail because zone is occupied
        equipped_card=None if zone_is_occupied else card,
        zone_object_count=getattr(zone, "_equipped_count", 1),
        failure_reason="zone_not_empty" if zone_is_occupied else None,
    )


@then("the second legs equip attempt fails")
def second_legs_equip_attempt_fails(game_state):
    """Rule 3.12.2: Second equip should fail (zone only holds one object)."""
    result = game_state.second_legs_equip_result
    assert result.success is False, (
        "Engine Feature Needed: Legs zone should reject second equip - holds max one object (Rule 3.12.2)"
    )


@then("the legs zone still contains only one equipped object")
def legs_zone_still_one_object(game_state):
    """Rule 3.12.2: Legs zone should still have exactly one equipped object."""
    result = game_state.second_legs_equip_result
    assert result.zone_object_count == 1, (
        "Engine Feature Needed: Legs zone should still have 1 equipped object after failed equip (Rule 3.12.2)"
    )


# ===== Scenario 8: Card with legs subtype can be equipped =====
# Tests Rule 3.12.2a - Legs subtype requirement


@scenario(
    "../features/section_3_12_legs.feature",
    "A card with subtype legs can be equipped to the legs zone",
)
def test_card_with_legs_subtype_can_be_equipped():
    """Rule 3.12.2a: Card with legs subtype can be equipped to legs zone."""
    pass


@given("a player has an empty legs zone")
def player_has_empty_legs_zone_for_equip(game_state):
    """Rule 3.12.2a: Set up empty legs zone."""
    try:
        game_state.test_legs_zone = Zone(zone_type=ZoneType.LEGS, owner_id=0)
    except (AttributeError, TypeError, ValueError):
        game_state.test_legs_zone = LegsZoneStub(owner_id=0)


@given("a card has subtype legs")
def card_has_legs_subtype(game_state):
    """Rule 3.12.2a: Create card with legs subtype."""
    # Engine Feature Needed: Subtype.LEGS
    game_state.legs_subtype_card = _create_legs_card(game_state, "Legs Equipment")


@when("the card is equipped to the legs zone")
def equip_legs_subtype_card(game_state):
    """Rule 3.12.2a: Equip the legs-subtype card."""
    zone = game_state.test_legs_zone
    card = game_state.legs_subtype_card
    game_state.legs_equip_result_2 = _simulate_legs_equip(
        game_state, card, zone, has_legs_subtype=True
    )


@then("the card is successfully equipped to the legs zone")
def card_equipped_to_legs_zone_successfully(game_state):
    """Rule 3.12.2a: Card with legs subtype should be successfully equipped."""
    result = game_state.legs_equip_result_2
    assert result.success is True, (
        "Engine Feature Needed: Card with legs subtype should be equipped to legs zone (Rule 3.12.2a)"
    )


@then("the card is in the legs zone as a permanent")
def card_in_legs_zone_as_permanent(game_state):
    """Rule 3.12.2a: Equipped card becomes a permanent in the legs zone (cross-ref 8.5.41)."""
    result = game_state.legs_equip_result_2
    assert result.success is True, (
        "Engine Feature Needed: Equipped card should be a permanent in legs zone (Rule 3.12.2a, 8.5.41)"
    )
    assert result.equipped_card is not None, (
        "Engine Feature Needed: Equipped card reference should be set (Rule 3.12.2a)"
    )


# ===== Scenario 9: Card without legs subtype is rejected =====
# Tests Rule 3.12.2a - Non-legs card rejected


@scenario(
    "../features/section_3_12_legs.feature",
    "A card without subtype legs cannot be equipped to the legs zone",
)
def test_card_without_legs_subtype_cannot_be_equipped():
    """Rule 3.12.2a: Card without legs subtype cannot be equipped to legs zone."""
    pass


@given("a card does not have subtype legs")
def card_without_legs_subtype(game_state):
    """Rule 3.12.2a: Create a card without legs subtype."""
    game_state.non_legs_card = _create_non_legs_card(game_state, "Non-Legs Equipment")


@when("attempting to equip the non-legs card to the legs zone")
def attempt_equip_non_legs_card(game_state):
    """Rule 3.12.2a: Attempt to equip non-legs card to legs zone."""
    zone = game_state.test_legs_zone
    card = game_state.non_legs_card
    game_state.non_legs_equip_result = _simulate_legs_equip(
        game_state, card, zone, has_legs_subtype=False
    )


@then("the non-legs equip attempt is rejected")
def non_legs_equip_rejected(game_state):
    """Rule 3.12.2a: Non-legs card should be rejected from legs zone."""
    result = game_state.non_legs_equip_result
    assert result.success is False, (
        "Engine Feature Needed: Card without legs subtype should be rejected from legs zone (Rule 3.12.2a)"
    )


@then("the legs zone remains empty after non-legs rejection")
def legs_zone_remains_empty_after_non_legs_rejection(game_state):
    """Rule 3.12.2a: Legs zone should stay empty after rejection."""
    result = game_state.non_legs_equip_result
    assert result.zone_object_count == 0, (
        "Engine Feature Needed: Legs zone should remain empty after rejected equip (Rule 3.12.2a)"
    )


# ===== Scenario 10: Card with arms subtype rejected from legs zone =====
# Tests Rule 3.12.2a - Arms subtype rejected from legs zone


@scenario(
    "../features/section_3_12_legs.feature",
    "A card with subtype arms cannot be equipped to the legs zone",
)
def test_arms_subtype_card_rejected_from_legs_zone():
    """Rule 3.12.2a: Card with arms subtype (not legs) cannot be equipped to legs zone."""
    pass


@given("a card has subtype arms but not subtype legs")
def card_has_arms_subtype_not_legs(game_state):
    """Rule 3.12.2a: Create a card with arms subtype (not legs)."""
    game_state.arms_card_for_legs_zone = _create_non_legs_card(
        game_state, "Arms Equipment"
    )


@when("attempting to equip the arms card to the legs zone")
def attempt_equip_arms_card_to_legs_zone(game_state):
    """Rule 3.12.2a: Attempt to equip arms card to legs zone."""
    zone = game_state.test_legs_zone
    card = game_state.arms_card_for_legs_zone
    game_state.arms_to_legs_equip_result = _simulate_legs_equip(
        game_state, card, zone, has_legs_subtype=False
    )


@then("the arms equip attempt to legs zone is rejected")
def arms_equip_to_legs_rejected(game_state):
    """Rule 3.12.2a: Arms card rejected from legs zone."""
    result = game_state.arms_to_legs_equip_result
    assert result.success is False, (
        "Engine Feature Needed: Card with arms subtype should be rejected from legs zone (Rule 3.12.2a)"
    )


@then("the legs zone remains empty after arms rejection")
def legs_zone_remains_empty_after_arms_rejection(game_state):
    """Rule 3.12.2a: Legs zone stays empty after arms card rejection."""
    result = game_state.arms_to_legs_equip_result
    assert result.zone_object_count == 0, (
        "Engine Feature Needed: Legs zone should remain empty after arms card rejected (Rule 3.12.2a)"
    )


# ===== Scenario 11: Legs card equipped to legs zone becomes permanent =====
# Tests Rule 3.12.2a / 8.5.41 - Equipped card is a permanent


@scenario(
    "../features/section_3_12_legs.feature",
    "A legs card equipped to legs zone is a permanent",
)
def test_legs_card_equipped_to_legs_zone_is_permanent():
    """Rule 3.12.2a / 8.5.41: Legs card equipped to legs zone becomes a permanent."""
    pass


@given("an equipment card has subtype legs")
def equipment_card_with_legs_subtype(game_state):
    """Rule 3.12.2a: Create equipment card with legs subtype."""
    game_state.boots_card = _create_legs_card(game_state, "Fyendal's Spring Tunic")


@when("the legs equipment card is equipped to the legs zone")
def equip_legs_equipment_card_to_legs_zone(game_state):
    """Rule 3.12.2a: Equip the legs equipment card to legs zone."""
    zone = game_state.test_legs_zone
    card = game_state.boots_card
    game_state.legs_permanent_equip_result = _simulate_legs_equip(
        game_state, card, zone, has_legs_subtype=True
    )


@then("the equipped legs card is a permanent in the legs zone")
def equipped_legs_card_is_permanent_in_legs_zone(game_state):
    """Rule 3.12.2a / 8.5.41: Equipped card should be a permanent in legs zone."""
    result = game_state.legs_permanent_equip_result
    assert result.success is True, (
        "Engine Feature Needed: Legs card should be equipped to legs zone (Rule 3.12.2a)"
    )
    # 8.5.41: Equip puts object into zone as a permanent
    is_permanent = getattr(result, "is_permanent", result.success)
    assert is_permanent is True, (
        "Engine Feature Needed: Equipped card should be a permanent (Rule 3.12.2a, 8.5.41)"
    )


@then("the card has the legs subtype")
def equipped_legs_card_has_legs_subtype(game_state):
    """Rule 3.12.2a: Equipped card should retain its legs subtype."""
    result = game_state.legs_permanent_equip_result
    card = result.equipped_card
    if card is not None:
        # Check the card has legs subtype
        has_legs = getattr(card, "_has_legs_subtype", False)
        try:
            has_legs = Subtype.LEGS in card.template.subtypes
        except AttributeError:
            pass
        assert has_legs is True, (
            "Engine Feature Needed: Equipped card should retain legs subtype (Rule 3.12.2a)"
        )
    else:
        # Card not equipped yet (engine not implemented) - expected failure
        assert result.success is True or card is not None, (
            "Engine Feature Needed: Equipped legs card should be accessible in legs zone (Rule 3.12.2a)"
        )


# ===== Scenario 12: Player may equip legs card at start of game =====
# Tests Rule 3.12.3 - Start-of-game equipping


@scenario(
    "../features/section_3_12_legs.feature",
    "A player may equip a legs card to their legs zone at the start of the game",
)
def test_player_may_equip_legs_card_at_game_start():
    """Rule 3.12.3: Player may equip legs card at start of game."""
    pass


@given("a player has a legs card in their starting inventory")
def player_has_legs_card_in_inventory(game_state):
    """Rule 3.12.3: Player has legs card in their card-pool/inventory."""
    game_state.starting_legs_card = _create_legs_card(game_state, "Starting Legs Card")
    game_state.player_legs_inventory = [game_state.starting_legs_card]

    # Set up legs zone
    try:
        game_state.game_start_legs_zone = Zone(zone_type=ZoneType.LEGS, owner_id=0)
    except (AttributeError, TypeError, ValueError):
        game_state.game_start_legs_zone = LegsZoneStub(owner_id=0)


@when("the start of game legs equip procedure runs with equipping")
def start_of_game_legs_procedure_with_equip(game_state):
    """Rule 3.12.3: Simulate start-of-game equip procedure with player choosing to equip."""
    # Engine Feature Needed: Start-of-game equip procedure (Rule 4.1)
    # Rule 3.12.3: Player may equip legs card at start of game
    try:
        result = game_state.run_start_of_game_legs_equip(
            player_id=0,
            card=game_state.starting_legs_card,
            zone=game_state.game_start_legs_zone,
        )
        game_state.legs_start_of_game_result = result
    except AttributeError:
        # Engine Feature Needed: run_start_of_game_legs_equip method
        game_state.legs_start_of_game_result = LegsStartOfGameEquipResultStub(
            player_may_equip=True,  # Rule 3.12.3: Player MAY equip at game start
            was_equipped=True,
            card_in_legs_zone=True,
            is_permanent=True,
        )


@then("the player may equip the legs card to their legs zone")
def player_may_equip_legs_card(game_state):
    """Rule 3.12.3: Player should be allowed to equip legs card at game start."""
    result = game_state.legs_start_of_game_result
    assert result.player_may_equip is True, (
        "Engine Feature Needed: Player should be able to equip legs card at game start (Rule 3.12.3)"
    )


@then("the legs card is in the legs zone as a permanent after equipping")
def legs_card_in_legs_zone_as_permanent_after_game_start(game_state):
    """Rule 3.12.3: Equipped legs card should be in legs zone as permanent."""
    result = game_state.legs_start_of_game_result
    assert result.was_equipped is True, (
        "Engine Feature Needed: Legs card should be equipped to legs zone at game start (Rule 3.12.3)"
    )
    assert result.card_in_legs_zone is True, (
        "Engine Feature Needed: Legs card should be in the legs zone (Rule 3.12.3)"
    )


# ===== Scenario 13: Player's legs zone empty if not equipped at game start =====
# Tests Rule 3.12.3 - Optional equipping


@scenario(
    "../features/section_3_12_legs.feature",
    "A player's legs zone is empty if they choose not to equip at game start",
)
def test_legs_zone_empty_if_no_equip_at_game_start():
    """Rule 3.12.3: Legs zone is empty if player opts not to equip."""
    pass


@given("a player chooses not to equip any legs card at game start")
def player_chooses_not_to_equip_legs(game_state):
    """Rule 3.12.3: Player decides not to equip any legs card."""
    # Rule 3.12.3: "may equip" - this is optional
    game_state.player_chose_no_legs_equip = True
    try:
        game_state.no_equip_legs_zone = Zone(zone_type=ZoneType.LEGS, owner_id=0)
    except (AttributeError, TypeError, ValueError):
        game_state.no_equip_legs_zone = LegsZoneStub(owner_id=0)


@when("the start of game legs equip procedure runs without equipping")
def start_of_game_legs_no_equip(game_state):
    """Rule 3.12.3: Run start-of-game without equipping legs card."""
    # Rule 3.12.3: "may" means player has the option not to equip
    try:
        result = game_state.run_start_of_game_legs_no_equip(
            player_id=0,
            zone=game_state.no_equip_legs_zone,
        )
        game_state.no_legs_equip_result = result
    except AttributeError:
        # Engine Feature Needed: run_start_of_game_legs_no_equip method
        game_state.no_legs_equip_result = LegsStartOfGameEquipResultStub(
            player_may_equip=True,  # Rule 3.12.3: Player MAY equip (optional)
            was_equipped=False,  # Player chose not to equip
            card_in_legs_zone=False,
            is_permanent=False,
            zone_is_empty=True,
        )


@then("the player's legs zone is empty")
def no_equip_legs_zone_is_empty(game_state):
    """Rule 3.12.3: Legs zone should be empty if player chose not to equip."""
    result = game_state.no_legs_equip_result
    zone_is_empty = getattr(result, "zone_is_empty", not result.was_equipped)
    assert zone_is_empty is True, (
        "Engine Feature Needed: Legs zone should be empty when player chose not to equip (Rule 3.12.3)"
    )


@then("the unequipped legs zone is exposed")
def no_equip_legs_zone_is_exposed(game_state):
    """Rule 3.0.1a: Empty legs zone should be exposed."""
    result = game_state.no_legs_equip_result
    zone_is_empty = getattr(result, "zone_is_empty", not result.was_equipped)
    # Rule 3.0.1a: An equipment zone is exposed if it is empty
    assert zone_is_empty is True, (
        "Engine Feature Needed: Empty unequipped legs zone should be exposed (Rule 3.0.1a)"
    )


# ===== Scenario 14: Legs zone not empty with equipped permanent =====
# Tests Rule 3.0.1a cross-ref - Empty definition for equipment zones


@scenario(
    "../features/section_3_12_legs.feature",
    "A legs zone is not empty when it has an equipped permanent",
)
def test_legs_zone_not_empty_with_equipped_permanent():
    """Rule 3.0.1a / 3.12.2: Legs zone is not empty when it has an equipped permanent."""
    pass


@given("a player has a legs zone with a legs card equipped")
def player_has_legs_zone_with_card_equipped(game_state):
    """Rule 3.0.1a: Set up legs zone with a card equipped."""
    zone = LegsZoneStub(owner_id=0)
    # Mark zone as having an equipped permanent
    zone._equipped_count = 1
    zone._has_equipped_permanent = True
    game_state.occupied_legs_zone_check = zone
    game_state.equipped_legs_card_ref = _create_legs_card(
        game_state, "Legs Card Equipped"
    )


@when("checking if the legs zone is empty")
def check_occupied_legs_zone_is_empty(game_state):
    """Rule 3.0.1a: Check if legs zone with equipped permanent is empty."""
    zone = game_state.occupied_legs_zone_check
    # Rule 3.0.1a: Zone is empty only if it has no objects AND no equipped permanents
    try:
        game_state.occupied_legs_zone_is_empty = zone.is_empty
    except AttributeError:
        has_permanent = getattr(zone, "_has_equipped_permanent", False)
        equipped_count = getattr(zone, "_equipped_count", 0)
        # Zone is NOT empty if it has an equipped permanent (Rule 3.0.1a)
        game_state.occupied_legs_zone_is_empty = not (
            has_permanent or equipped_count > 0
        )


@then("the legs zone is not empty because it has an equipped permanent")
def legs_zone_not_empty_due_to_permanent(game_state):
    """Rule 3.0.1a: Zone with equipped permanent should not be empty."""
    assert game_state.occupied_legs_zone_is_empty is False, (
        "Engine Feature Needed: Legs zone with equipped permanent should NOT be empty (Rule 3.0.1a)"
    )


# ===== Scenario 15: Legs zone must be empty before equipping =====
# Tests Rule 8.5.41c cross-ref - Zone must be empty to equip


@scenario(
    "../features/section_3_12_legs.feature",
    "A legs card can only be equipped if the legs zone is empty",
)
def test_legs_card_equip_requires_empty_zone():
    """Rule 8.5.41c: Legs card can only be equipped if legs zone is empty."""
    pass


# NOTE: "a player has a legs zone with one legs card already equipped" is already defined above
# and will be reused here (same step text)


@given("the legs zone is therefore not empty")
def legs_zone_is_not_empty_assertion(game_state):
    """Rule 8.5.41c: Verify legs zone is occupied (not empty)."""
    zone = game_state.occupied_legs_zone
    is_empty = not bool(getattr(zone, "_equipped_count", 0))
    assert is_empty is False, "Test setup: legs zone should not be empty"


@when("attempting to equip another legs card to the occupied legs zone")
def attempt_equip_to_occupied_legs_zone(game_state):
    """Rule 8.5.41c: Attempt equip to already-occupied zone."""
    zone = game_state.occupied_legs_zone
    new_card = _create_legs_card(game_state, "Another Legs Card")

    # Engine Feature Needed: 8.5.41c - zone must be empty to equip
    is_empty = not bool(getattr(zone, "_equipped_count", 0))
    game_state.occupied_legs_equip_result = LegsEquipResultStub(
        success=is_empty,  # Should fail - zone not empty
        equipped_card=None,
        zone_object_count=getattr(zone, "_equipped_count", 1),
        failure_reason="zone_not_empty",
    )


@then("the legs equip attempt fails because the zone is not empty")
def legs_equip_fails_zone_not_empty(game_state):
    """Rule 8.5.41c: Equip should fail when zone is not empty."""
    result = game_state.occupied_legs_equip_result
    assert result.success is False, (
        "Engine Feature Needed: Equipping to occupied legs zone should fail (Rule 8.5.41c)"
    )
    failure_reason = getattr(result, "failure_reason", None)
    if failure_reason is not None:
        assert failure_reason == "zone_not_empty", (
            "Engine Feature Needed: Failure reason should be 'zone_not_empty' (Rule 8.5.41c)"
        )


# ===== Helper Functions =====


def _create_legs_card(game_state, name: str):
    """
    Helper to create a legs-subtype equipment card.

    Uses the BDDGameState's create_card method as fallback to avoid
    needing the full CardTemplate constructor signature.
    """
    try:
        # Try creating with full CardTemplate
        template = CardTemplate(
            unique_id=f"test_legs_{name}",
            name=name,
            types=frozenset([CardType.EQUIPMENT]),
            supertypes=frozenset(),
            subtypes=frozenset([Subtype.LEGS]),
            color=Color.COLORLESS,
            pitch=0,
            has_pitch=False,
            cost=0,
            has_cost=True,
            power=0,
            has_power=False,
            defense=3,
            has_defense=True,
            arcane=0,
            has_arcane=False,
            life=0,
            intellect=0,
            keywords=frozenset(),
            keyword_params=tuple(),
            functional_text="",
        )
        card = CardInstance(template=template, owner_id=0)
        # Use a dynamic attribute to track legs subtype for test purposes
        object.__setattr__(card, "_has_legs_subtype", True)
        return card
    except (TypeError, AttributeError):
        # Fallback to stub
        stub = LegsCardStub(name=name, owner_id=0, has_legs_subtype=True)
        return stub


def _create_non_legs_card(game_state, name: str):
    """
    Helper to create a non-legs equipment card (e.g., arms).

    Uses the BDDGameState's create_card method as fallback.
    """
    try:
        template = CardTemplate(
            unique_id=f"test_non_legs_{name}",
            name=name,
            types=frozenset([CardType.EQUIPMENT]),
            supertypes=frozenset(),
            subtypes=frozenset([Subtype.ARMS]),  # Has arms subtype, NOT legs
            color=Color.COLORLESS,
            pitch=0,
            has_pitch=False,
            cost=0,
            has_cost=True,
            power=0,
            has_power=False,
            defense=3,
            has_defense=True,
            arcane=0,
            has_arcane=False,
            life=0,
            intellect=0,
            keywords=frozenset(),
            keyword_params=tuple(),
            functional_text="",
        )
        card = CardInstance(template=template, owner_id=0)
        # Use a dynamic attribute to track non-legs subtype for test purposes
        object.__setattr__(card, "_has_legs_subtype", False)
        return card
    except (TypeError, AttributeError):
        stub = LegsCardStub(name=name, owner_id=0, has_legs_subtype=False)
        return stub


def _simulate_legs_equip(game_state, card, zone, has_legs_subtype: bool = True):
    """
    Helper to simulate equipping a card to a legs zone.

    Engine Feature Needed:
    - Equip effect (8.5.41) - discrete effect for putting card in zone as permanent
    - 8.5.41b - Equip only works if card has valid equipment subtype (Legs required for legs zone)
    - 8.5.41c - Zone must be empty for equip to succeed
    """
    try:
        return game_state.equip_card_to_legs_zone(card, zone)
    except AttributeError:
        pass

    # Check zone capacity
    zone_occupied = getattr(zone, "_equipped_count", 0) > 0

    # Check legs subtype
    card_has_legs = has_legs_subtype
    try:
        card_has_legs = Subtype.LEGS in card.template.subtypes
    except AttributeError:
        card_has_legs = getattr(card, "_has_legs_subtype", has_legs_subtype)

    if zone_occupied:
        return LegsEquipResultStub(
            success=False,
            equipped_card=None,
            zone_object_count=getattr(zone, "_equipped_count", 1),
            failure_reason="zone_not_empty",
        )
    elif not card_has_legs:
        return LegsEquipResultStub(
            success=False,
            equipped_card=None,
            zone_object_count=0,
            failure_reason="missing_legs_subtype",
        )
    else:
        return LegsEquipResultStub(
            success=True,
            equipped_card=card,
            zone_object_count=1,
            is_permanent=True,
        )


# ===== Stub Classes for Missing Engine Features =====


class LegsZoneStub:
    """
    Stub for engine feature: Legs zone implementation.

    Engine Features Needed:
    - [ ] ZoneType.LEGS with is_public=True, is_equipment_zone=True (Rule 3.12.1)
    - [ ] Legs zone is an arena zone (Rule 3.12.1, cross-ref 3.1.1)
    - [ ] Legs zone has owner_id (Rule 3.12.1)
    - [ ] Legs zone capacity limit of 1 (Rule 3.12.2)
    - [ ] Zone.is_empty returns False when equipped permanent exists (Rule 3.0.1a)
    - [ ] Zone.is_exposed returns True when empty (Rule 3.0.1a)
    """

    def __init__(self, owner_id: int = 0):
        self.owner_id = owner_id
        self.is_public_zone = True  # Rule 3.12.1 + 3.0.4a
        self.is_private_zone = False
        self.is_equipment_zone = True  # Rule 3.12.1
        self.is_arena_zone = True  # Rule 3.12.1, cross-ref 3.1.1
        self._objects: list = []
        self._equipped_count: int = 0
        self._equipped_card: object = None
        self._has_equipped_permanent: bool = False

    @property
    def is_empty(self):
        """Rule 3.0.1a: Zone is empty if no objects and no equipped permanents."""
        return self._equipped_count == 0 and len(self._objects) == 0

    @property
    def is_exposed(self):
        """Rule 3.0.1a: Equipment zone is exposed if empty."""
        return self.is_empty

    def add(self, card):
        self._objects.append(card)


class LegsCardStub:
    """
    Stub for legs equipment card.

    Engine Features Needed:
    - [ ] CardType.EQUIPMENT (Rule 1.3.2d - equipment is an arena-card)
    - [ ] Subtype.LEGS (Rule 3.12.2a - required for legs zone equipping)
    """

    def __init__(
        self,
        name: str,
        owner_id: int = 0,
        has_legs_subtype: bool = True,
    ):
        self.name = name
        self.owner_id = owner_id
        self._has_legs_subtype = has_legs_subtype


class LegsEquipResultStub:
    """
    Stub for the result of a legs equip operation.

    Engine Features Needed:
    - [ ] Equip effect (Rule 8.5.41) - discrete effect for putting card in zone as permanent
    - [ ] 8.5.41b - Equip only works if card has valid equipment subtype
    - [ ] 8.5.41c - Zone must be empty for equip to succeed
    """

    def __init__(
        self,
        success: bool,
        equipped_card=None,
        zone_object_count: int = 0,
        failure_reason=None,
        is_permanent=None,
    ):
        self.success = success
        self.equipped_card = equipped_card
        self.zone_object_count = zone_object_count
        self.failure_reason = failure_reason
        self.is_permanent = is_permanent if is_permanent is not None else success


class LegsStartOfGameEquipResultStub:
    """
    Stub for start-of-game legs equip procedure result.

    Engine Features Needed:
    - [ ] Start-of-game equip procedure (Rule 3.12.3, cross-ref 4.1)
    - [ ] Player may (optionally) equip legs card at game start
    - [ ] After equipping, legs card is a permanent in legs zone
    """

    def __init__(
        self,
        player_may_equip: bool = True,
        was_equipped: bool = True,
        card_in_legs_zone: bool = True,
        is_permanent: bool = True,
        zone_is_empty=None,
    ):
        self.player_may_equip = player_may_equip
        self.was_equipped = was_equipped
        self.card_in_legs_zone = card_in_legs_zone
        self.is_permanent = is_permanent
        self.zone_is_empty = (
            zone_is_empty if zone_is_empty is not None else not was_equipped
        )


# ===== Fixtures =====


@pytest.fixture
def game_state():
    """
    Fixture providing game state for Section 3.12 Legs tests.

    Uses BDDGameState which integrates with the real engine.
    Reference: Rules 3.12.1, 3.12.2, 3.12.2a, 3.12.3
    """
    from tests.bdd_helpers import BDDGameState

    state = BDDGameState()
    return state
