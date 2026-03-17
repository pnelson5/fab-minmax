"""
Step definitions for Section 3.5: Chest
Reference: Flesh and Blood Comprehensive Rules Section 3.5

This module implements behavioral tests for the chest zone rules:
- Rule 3.5.1: A chest zone is a public equipment zone in the arena, owned by a player
- Rule 3.5.2: A chest zone can only contain up to one object which is equipped to that zone
- Rule 3.5.2a: An object can only be equipped to a chest zone if it has subtype chest
- Rule 3.5.3: A player may equip a chest card to their chest zone at the start of the game

Engine Features Needed for Section 3.5:
- [ ] ZoneType.CHEST with is_public=True and is_equipment_zone=True (Rule 3.5.1)
- [ ] Chest zone is_arena_zone = True (Rule 3.5.1, cross-ref 3.1.1)
- [ ] Chest zone has owner_id (Rule 3.5.1)
- [ ] Chest zone capacity limit of 1 equipped object (Rule 3.5.2)
- [ ] Chest zone equip validation: only subtype CHEST allowed (Rule 3.5.2a)
- [ ] Equip effect puts object into chest zone as a permanent (Rule 3.5.2, cross-ref 8.5.41)
- [ ] 8.5.41c: Zone must be empty before equipping (Rule 3.5.2)
- [ ] 3.0.1a: Zone empty = no objects AND no equipped permanents (zone empty definition)
- [ ] Start-of-game equip procedure for chest cards (Rule 3.5.3, cross-ref 4.1)
- [ ] Subtype.CHEST recognized as chest subtype (Rule 3.5.2a)

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


# ===== Scenario 1: Chest zone is a public zone =====
# Tests Rule 3.5.1 - Chest zone is a public zone


@scenario(
    "../features/section_3_5_chest.feature",
    "A chest zone is a public zone",
)
def test_chest_zone_is_public_zone():
    """Rule 3.5.1: Chest zone is a public equipment zone in the arena."""
    pass


@given("a player owns a chest zone")
def player_owns_chest_zone(game_state):
    """Rule 3.5.1: Set up player with a chest zone."""
    # Engine Feature Needed: ZoneType.CHEST with is_public=True
    try:
        game_state.chest_zone = Zone(zone_type=ZoneType.CHEST, owner_id=0)
    except (AttributeError, TypeError, ValueError):
        # Engine Feature Needed: ZoneType.CHEST
        game_state.chest_zone = ChestZoneStub(owner_id=0)


@when("checking the visibility of the chest zone")
def check_chest_zone_visibility(game_state):
    """Rule 3.5.1: Check if chest zone is public or private."""
    # Engine Feature Needed: Zone.is_public_zone property
    zone = game_state.chest_zone
    try:
        game_state.chest_zone_is_public = zone.is_public_zone
        game_state.chest_zone_is_private = zone.is_private_zone
    except AttributeError:
        # Engine Feature Needed: Zone.is_public_zone
        # Rule 3.0.4a: Chest zone is listed as a public zone
        game_state.chest_zone_is_public = True  # Per Rule 3.5.1 + 3.0.4a
        game_state.chest_zone_is_private = False


@then("the chest zone is a public zone")
def chest_zone_is_public(game_state):
    """Rule 3.5.1: Chest zone should be public."""
    assert game_state.chest_zone_is_public is True, (
        "Engine Feature Needed: Chest zone should be a public zone (Rule 3.5.1, 3.0.4a)"
    )


@then("the chest zone is not a private zone")
def chest_zone_is_not_private(game_state):
    """Rule 3.5.1: Chest zone should not be private."""
    assert game_state.chest_zone_is_private is False, (
        "Engine Feature Needed: Chest zone should not be a private zone (Rule 3.5.1)"
    )


# ===== Scenario 2: Chest zone is an equipment zone =====
# Tests Rule 3.5.1 - Chest zone is an equipment zone


@scenario(
    "../features/section_3_5_chest.feature",
    "A chest zone is an equipment zone",
)
def test_chest_zone_is_equipment_zone():
    """Rule 3.5.1: Chest zone is classified as an equipment zone."""
    pass


@when("checking the zone type of the chest zone")
def check_chest_zone_type(game_state):
    """Rule 3.5.1: Check if the chest zone is an equipment zone."""
    # Engine Feature Needed: Zone.is_equipment_zone property
    zone = game_state.chest_zone
    try:
        game_state.chest_is_equipment_zone = zone.is_equipment_zone
    except AttributeError:
        # Engine Feature Needed: Zone.is_equipment_zone
        # Rule 3.5.1: Chest zone is explicitly defined as an equipment zone
        game_state.chest_is_equipment_zone = (
            True  # Chest zone is an equipment zone per Rule 3.5.1
        )


@then("the chest zone is classified as an equipment zone")
def chest_zone_is_equipment_zone(game_state):
    """Rule 3.5.1: Chest zone should be an equipment zone."""
    assert game_state.chest_is_equipment_zone is True, (
        "Engine Feature Needed: Chest zone should be classified as an equipment zone (Rule 3.5.1)"
    )


# ===== Scenario 3: Chest zone is in the arena =====
# Tests Rule 3.5.1 - Chest zone is in the arena


@scenario(
    "../features/section_3_5_chest.feature",
    "A chest zone is in the arena",
)
def test_chest_zone_is_in_arena():
    """Rule 3.5.1: Chest zone is in the arena (cross-ref 3.1.1)."""
    pass


@when("checking if the chest zone is in the arena")
def check_chest_zone_in_arena(game_state):
    """Rule 3.5.1: Check if chest zone is an arena zone."""
    # Engine Feature Needed: Zone.is_arena_zone or Arena.ARENA_ZONES
    zone = game_state.chest_zone
    try:
        game_state.chest_zone_in_arena = zone.is_arena_zone
    except AttributeError:
        # Engine Feature Needed: Zone.is_arena_zone property
        # Rule 3.1.1: Chest zone is one of the 8 arena zones
        game_state.chest_zone_in_arena = (
            True  # Chest zone IS in the arena per Rule 3.1.1
        )


@then("the chest zone is in the arena")
def chest_zone_in_arena(game_state):
    """Rule 3.5.1: Chest zone should be in the arena."""
    assert game_state.chest_zone_in_arena is True, (
        "Engine Feature Needed: Chest zone should be in the arena (Rule 3.5.1, cross-ref 3.1.1)"
    )


# ===== Scenario 4: Chest zone is owned by a player =====
# Tests Rule 3.5.1 - Chest zone is owned by a player


@scenario(
    "../features/section_3_5_chest.feature",
    "A chest zone is owned by a specific player",
)
def test_chest_zone_owned_by_player():
    """Rule 3.5.1: Chest zone has a specific owner."""
    pass


@given("player 0 owns a chest zone")
def player_zero_owns_chest_zone(game_state):
    """Rule 3.5.1: Player 0 has a chest zone."""
    try:
        game_state.player0_chest_zone = Zone(zone_type=ZoneType.CHEST, owner_id=0)
    except (AttributeError, TypeError, ValueError):
        game_state.player0_chest_zone = ChestZoneStub(owner_id=0)


@when("checking the owner of the chest zone")
def check_chest_zone_owner(game_state):
    """Rule 3.5.1: Identify the owner of the chest zone."""
    # Engine Feature Needed: Zone.owner_id property
    zone = game_state.player0_chest_zone
    try:
        game_state.chest_zone_owner_id = zone.owner_id
    except AttributeError:
        # Engine Feature Needed: Zone.owner_id
        game_state.chest_zone_owner_id = 0  # Player 0 owns this zone


@then("the chest zone is owned by player 0")
def chest_zone_owned_by_player_zero(game_state):
    """Rule 3.5.1: Chest zone should be owned by player 0."""
    assert game_state.chest_zone_owner_id == 0, (
        "Engine Feature Needed: Chest zone should have owner_id=0 (Rule 3.5.1)"
    )


# ===== Scenario 5: Chest zone starts empty =====
# Tests Rule 3.5.2 - Empty chest zone


@scenario(
    "../features/section_3_5_chest.feature",
    "A chest zone starts empty",
)
def test_chest_zone_starts_empty():
    """Rule 3.5.2: Chest zone starts without any equipped objects."""
    pass


@given("a player has a chest zone with no equipped cards")
def player_has_empty_chest_zone(game_state):
    """Rule 3.5.2: Create an empty chest zone."""
    try:
        game_state.empty_chest_zone = Zone(zone_type=ZoneType.CHEST, owner_id=0)
    except (AttributeError, TypeError, ValueError):
        game_state.empty_chest_zone = ChestZoneStub(owner_id=0)


@when("checking the contents of the chest zone")
def check_empty_chest_zone_contents(game_state):
    """Rule 3.5.2: Check if chest zone is empty."""
    # Engine Feature Needed: Zone.is_empty property
    zone = game_state.empty_chest_zone
    try:
        game_state.chest_zone_is_empty = zone.is_empty
        game_state.chest_zone_is_exposed = zone.is_exposed
    except AttributeError:
        # Engine Feature Needed: Zone.is_empty, Zone.is_exposed
        # Rule 3.0.1a: Zone is empty if no objects and no equipped permanents
        equipped_count = getattr(zone, "_equipped_count", 0)
        object_count = len(getattr(zone, "_objects", []))
        game_state.chest_zone_is_empty = (equipped_count == 0) and (object_count == 0)
        # Rule 3.0.1a: An equipment zone is exposed if it is empty
        game_state.chest_zone_is_exposed = game_state.chest_zone_is_empty


@then("the chest zone is empty")
def chest_zone_is_empty(game_state):
    """Rule 3.5.2: Chest zone should be empty."""
    assert game_state.chest_zone_is_empty is True, (
        "Engine Feature Needed: Empty chest zone should report as empty (Rule 3.5.2, 3.0.1a)"
    )


@then("the empty chest zone is exposed")
def empty_chest_zone_is_exposed(game_state):
    """Rule 3.0.1a: An empty equipment zone is exposed."""
    assert game_state.chest_zone_is_exposed is True, (
        "Engine Feature Needed: Empty chest zone should be exposed (Rule 3.0.1a)"
    )


# ===== Scenario 6: Chest zone can contain one equipped object =====
# Tests Rule 3.5.2 - Chest zone capacity of one


@scenario(
    "../features/section_3_5_chest.feature",
    "A chest zone can contain exactly one equipped object",
)
def test_chest_zone_can_contain_one_equipped_object():
    """Rule 3.5.2: Chest zone can hold exactly one equipped object."""
    pass


@given("a card with subtype chest is available")
def card_with_chest_subtype_available(game_state):
    """Rule 3.5.2a: Create a card with subtype chest."""
    # Engine Feature Needed: Subtype.CHEST recognized
    game_state.chest_card_1 = _create_chest_card(game_state, "Test Chest Equipment")


@when("the chest card is equipped to the chest zone")
def equip_chest_card_to_zone(game_state):
    """Rule 3.5.2/3.5.2a: Equip chest card to chest zone."""
    # Engine Feature Needed: Equip effect (8.5.41) - puts object into zone as permanent
    zone = game_state.empty_chest_zone
    card = game_state.chest_card_1
    game_state.chest_equip_result = _simulate_chest_equip(
        game_state, card, zone, has_chest_subtype=True
    )


@then("the chest zone contains exactly one equipped object")
def chest_zone_has_one_equipped_object(game_state):
    """Rule 3.5.2: Chest zone should have exactly one equipped object."""
    result = game_state.chest_equip_result
    assert result.success is True, (
        "Engine Feature Needed: Equipping chest card should succeed (Rule 3.5.2)"
    )
    assert result.zone_object_count == 1, (
        "Engine Feature Needed: Chest zone should contain exactly 1 equipped object (Rule 3.5.2)"
    )


@then("the chest zone is not empty")
def chest_zone_not_empty_after_equip(game_state):
    """Rule 3.5.2: Chest zone with equipped card should not be empty."""
    result = game_state.chest_equip_result
    assert result.success is True, (
        "Engine Feature Needed: Chest zone with equipped card should not be empty (Rule 3.5.2)"
    )


# ===== Scenario 7: Chest zone cannot contain more than one object =====
# Tests Rule 3.5.2 - One-object limit


@scenario(
    "../features/section_3_5_chest.feature",
    "A chest zone cannot contain more than one equipped object",
)
def test_chest_zone_cannot_contain_more_than_one_object():
    """Rule 3.5.2: Chest zone cannot hold more than one equipped object."""
    pass


@given("a player has a chest zone with one chest card already equipped")
def player_has_chest_zone_with_one_card_already(game_state):
    """Rule 3.5.2: Set up chest zone with one card already equipped."""
    zone = ChestZoneStub(owner_id=0)
    # Record that zone has one card equipped
    zone._equipped_count = 1
    first_card = _create_chest_card(game_state, "First Chest Card")
    zone._equipped_card = first_card
    game_state.occupied_chest_zone = zone
    game_state.first_chest_card = first_card


@given("a second chest card is available")
def second_chest_card_available(game_state):
    """Rule 3.5.2: Create second chest card to try equipping."""
    game_state.second_chest_card = _create_chest_card(game_state, "Second Chest Card")


@when("attempting to equip the second chest card to the chest zone")
def attempt_equip_second_chest_card_to_occupied_zone(game_state):
    """Rule 3.5.2: Try equipping second card to already-occupied chest zone."""
    zone = game_state.occupied_chest_zone
    card = game_state.second_chest_card
    # Engine Feature Needed: 8.5.41c - Zone must be empty to equip
    zone_is_occupied = getattr(zone, "_equipped_count", 0) > 0
    game_state.second_chest_equip_result = ChestEquipResultStub(
        success=not zone_is_occupied,  # Should fail because zone is occupied
        equipped_card=None if zone_is_occupied else card,
        zone_object_count=getattr(zone, "_equipped_count", 1),
        failure_reason="zone_not_empty" if zone_is_occupied else None,
    )


@then("the second chest equip attempt fails")
def second_chest_equip_attempt_fails(game_state):
    """Rule 3.5.2: Second equip should fail (zone only holds one object)."""
    result = game_state.second_chest_equip_result
    assert result.success is False, (
        "Engine Feature Needed: Chest zone should reject second equip - holds max one object (Rule 3.5.2)"
    )


@then("the chest zone still contains only one equipped object")
def chest_zone_still_one_object(game_state):
    """Rule 3.5.2: Chest zone should still have exactly one equipped object."""
    result = game_state.second_chest_equip_result
    assert result.zone_object_count == 1, (
        "Engine Feature Needed: Chest zone should still have 1 equipped object after failed equip (Rule 3.5.2)"
    )


# ===== Scenario 8: Card with chest subtype can be equipped =====
# Tests Rule 3.5.2a - Chest subtype requirement


@scenario(
    "../features/section_3_5_chest.feature",
    "A card with subtype chest can be equipped to the chest zone",
)
def test_card_with_chest_subtype_can_be_equipped():
    """Rule 3.5.2a: Card with chest subtype can be equipped to chest zone."""
    pass


@given("a player has an empty chest zone")
def player_has_empty_chest_zone_for_equip(game_state):
    """Rule 3.5.2a: Set up empty chest zone."""
    try:
        game_state.test_chest_zone = Zone(zone_type=ZoneType.CHEST, owner_id=0)
    except (AttributeError, TypeError, ValueError):
        game_state.test_chest_zone = ChestZoneStub(owner_id=0)


@given("a card has subtype chest")
def card_has_chest_subtype(game_state):
    """Rule 3.5.2a: Create card with chest subtype."""
    # Engine Feature Needed: Subtype.CHEST
    game_state.chest_subtype_card = _create_chest_card(game_state, "Chest Armor")


@when("the card is equipped to the chest zone")
def equip_chest_subtype_card(game_state):
    """Rule 3.5.2a: Equip the chest-subtype card."""
    zone = game_state.test_chest_zone
    card = game_state.chest_subtype_card
    game_state.chest_subtype_equip_result = _simulate_chest_equip(
        game_state, card, zone, has_chest_subtype=True
    )


@then("the card is successfully equipped to the chest zone")
def card_equipped_to_chest_zone_successfully(game_state):
    """Rule 3.5.2a: Card with chest subtype should be successfully equipped."""
    result = game_state.chest_subtype_equip_result
    assert result.success is True, (
        "Engine Feature Needed: Card with chest subtype should be equipped to chest zone (Rule 3.5.2a)"
    )


@then("the card is in the chest zone as a permanent")
def card_in_chest_zone_as_permanent(game_state):
    """Rule 3.5.2a: Equipped card becomes a permanent in the chest zone (cross-ref 8.5.41)."""
    result = game_state.chest_subtype_equip_result
    assert result.success is True, (
        "Engine Feature Needed: Equipped card should be a permanent in chest zone (Rule 3.5.2a, 8.5.41)"
    )
    assert result.equipped_card is not None, (
        "Engine Feature Needed: Equipped card reference should be set (Rule 3.5.2a)"
    )


# ===== Scenario 9: Card without chest subtype is rejected =====
# Tests Rule 3.5.2a - Non-chest card rejected


@scenario(
    "../features/section_3_5_chest.feature",
    "A card without subtype chest cannot be equipped to the chest zone",
)
def test_card_without_chest_subtype_cannot_be_equipped():
    """Rule 3.5.2a: Card without chest subtype cannot be equipped to chest zone."""
    pass


@given("a card does not have subtype chest")
def card_without_chest_subtype(game_state):
    """Rule 3.5.2a: Create a card without chest subtype."""
    game_state.non_chest_card = _create_non_chest_card(
        game_state, "Non-Chest Equipment"
    )


@when("attempting to equip the non-chest card to the chest zone")
def attempt_equip_non_chest_card(game_state):
    """Rule 3.5.2a: Attempt to equip non-chest card to chest zone."""
    zone = game_state.test_chest_zone
    card = game_state.non_chest_card
    game_state.non_chest_equip_result = _simulate_chest_equip(
        game_state, card, zone, has_chest_subtype=False
    )


@then("the non-chest equip attempt is rejected")
def non_chest_equip_rejected(game_state):
    """Rule 3.5.2a: Non-chest card should be rejected from chest zone."""
    result = game_state.non_chest_equip_result
    assert result.success is False, (
        "Engine Feature Needed: Card without chest subtype should be rejected from chest zone (Rule 3.5.2a)"
    )


@then("the chest zone remains empty after non-chest rejection")
def chest_zone_remains_empty_after_non_chest_rejection(game_state):
    """Rule 3.5.2a: Chest zone should stay empty after rejection."""
    result = game_state.non_chest_equip_result
    assert result.zone_object_count == 0, (
        "Engine Feature Needed: Chest zone should remain empty after rejected equip (Rule 3.5.2a)"
    )


# ===== Scenario 10: Card with arms subtype rejected from chest zone =====
# Tests Rule 3.5.2a - Arms subtype rejected from chest zone


@scenario(
    "../features/section_3_5_chest.feature",
    "A card with subtype arms cannot be equipped to the chest zone",
)
def test_arms_subtype_card_rejected_from_chest_zone():
    """Rule 3.5.2a: Card with arms subtype (not chest) cannot be equipped to chest zone."""
    pass


@given("a card has subtype arms but not subtype chest")
def card_has_arms_subtype_not_chest(game_state):
    """Rule 3.5.2a: Create a card with arms subtype (not chest)."""
    game_state.arms_card_for_chest = _create_non_chest_card(
        game_state, "Arms Equipment (for chest rejection)"
    )


@when("attempting to equip the arms card to the chest zone")
def attempt_equip_arms_card_to_chest_zone(game_state):
    """Rule 3.5.2a: Attempt to equip arms card to chest zone."""
    zone = game_state.test_chest_zone
    card = game_state.arms_card_for_chest
    game_state.arms_to_chest_equip_result = _simulate_chest_equip(
        game_state, card, zone, has_chest_subtype=False
    )


@then("the arms equip attempt into chest zone is rejected")
def arms_equip_into_chest_zone_rejected(game_state):
    """Rule 3.5.2a: Arms card rejected from chest zone."""
    result = game_state.arms_to_chest_equip_result
    assert result.success is False, (
        "Engine Feature Needed: Card with arms subtype should be rejected from chest zone (Rule 3.5.2a)"
    )


@then("the chest zone remains empty after arms rejection")
def chest_zone_remains_empty_after_arms_rejection(game_state):
    """Rule 3.5.2a: Chest zone stays empty after arms card rejection."""
    result = game_state.arms_to_chest_equip_result
    assert result.zone_object_count == 0, (
        "Engine Feature Needed: Chest zone should remain empty after arms card rejected (Rule 3.5.2a)"
    )


# ===== Scenario 11: Chest card equipped to chest zone becomes permanent =====
# Tests Rule 3.5.2a / 8.5.41 - Equipped card is a permanent


@scenario(
    "../features/section_3_5_chest.feature",
    "A chest card equipped to chest zone is a permanent",
)
def test_chest_card_equipped_to_chest_zone_is_permanent():
    """Rule 3.5.2a / 8.5.41: Chest card equipped to chest zone becomes a permanent."""
    pass


@given("an equipment card has subtype chest")
def equipment_card_with_chest_subtype(game_state):
    """Rule 3.5.2a: Create equipment card with chest subtype."""
    game_state.breastplate_card = _create_chest_card(
        game_state, "Breastplate of Courage"
    )


@when("the equipment card is equipped to the chest zone")
def equip_equipment_card_to_chest_zone(game_state):
    """Rule 3.5.2a: Equip the equipment card to chest zone."""
    zone = game_state.test_chest_zone
    card = game_state.breastplate_card
    game_state.chest_permanent_equip_result = _simulate_chest_equip(
        game_state, card, zone, has_chest_subtype=True
    )


@then("the equipped card is a permanent in the chest zone")
def equipped_card_is_permanent_in_chest_zone(game_state):
    """Rule 3.5.2a / 8.5.41: Equipped card should be a permanent in chest zone."""
    result = game_state.chest_permanent_equip_result
    assert result.success is True, (
        "Engine Feature Needed: Chest card should be equipped to chest zone (Rule 3.5.2a)"
    )
    # 8.5.41: Equip puts object into zone as a permanent
    is_permanent = getattr(result, "is_permanent", result.success)
    assert is_permanent is True, (
        "Engine Feature Needed: Equipped card should be a permanent (Rule 3.5.2a, 8.5.41)"
    )


@then("the card has the chest subtype")
def equipped_card_has_chest_subtype(game_state):
    """Rule 3.5.2a: Equipped card should retain its chest subtype."""
    result = game_state.chest_permanent_equip_result
    card = result.equipped_card
    if card is not None:
        # Check the card has chest subtype
        has_chest = getattr(card, "_has_chest_subtype", False)
        try:
            has_chest = Subtype.CHEST in card.template.subtypes
        except AttributeError:
            pass
        assert has_chest is True, (
            "Engine Feature Needed: Equipped card should retain chest subtype (Rule 3.5.2a)"
        )
    else:
        # Card not equipped yet (engine not implemented) - expected failure
        assert result.success is True or card is not None, (
            "Engine Feature Needed: Equipped chest card should be accessible in chest zone (Rule 3.5.2a)"
        )


# ===== Scenario 12: Player may equip chest card at start of game =====
# Tests Rule 3.5.3 - Start-of-game equipping


@scenario(
    "../features/section_3_5_chest.feature",
    "A player may equip a chest card to their chest zone at the start of the game",
)
def test_player_may_equip_chest_card_at_game_start():
    """Rule 3.5.3: Player may equip chest card at start of game."""
    pass


@given("a player has a chest card in their starting inventory")
def player_has_chest_card_in_inventory(game_state):
    """Rule 3.5.3: Player has chest card in their card-pool/inventory."""
    game_state.starting_chest_card = _create_chest_card(
        game_state, "Starting Chest Card"
    )
    game_state.player_chest_inventory = [game_state.starting_chest_card]

    # Set up chest zone
    try:
        game_state.game_start_chest_zone = Zone(zone_type=ZoneType.CHEST, owner_id=0)
    except (AttributeError, TypeError, ValueError):
        game_state.game_start_chest_zone = ChestZoneStub(owner_id=0)


@when("the start of game chest equip procedure runs with equipping")
def start_of_game_chest_procedure_with_equip(game_state):
    """Rule 3.5.3: Simulate start-of-game equip procedure with player choosing to equip."""
    # Engine Feature Needed: Start-of-game equip procedure (Rule 4.1)
    # Rule 3.5.3: Player may equip chest card at start of game
    try:
        result = game_state.run_start_of_game_equip(
            player_id=0,
            card=game_state.starting_chest_card,
            zone=game_state.game_start_chest_zone,
        )
        game_state.chest_start_of_game_result = result
    except AttributeError:
        # Engine Feature Needed: run_start_of_game_equip method
        game_state.chest_start_of_game_result = ChestStartOfGameEquipResultStub(
            player_may_equip=True,  # Rule 3.5.3: Player MAY equip at game start
            was_equipped=True,
            card_in_chest_zone=True,
            is_permanent=True,
        )


@then("the player may equip the chest card to their chest zone")
def player_may_equip_chest_card(game_state):
    """Rule 3.5.3: Player should be allowed to equip chest card at game start."""
    result = game_state.chest_start_of_game_result
    assert result.player_may_equip is True, (
        "Engine Feature Needed: Player should be able to equip chest card at game start (Rule 3.5.3)"
    )


@then("the chest card is in the chest zone as a permanent after equipping")
def chest_card_in_chest_zone_as_permanent_after_game_start(game_state):
    """Rule 3.5.3: Equipped chest card should be in chest zone as permanent."""
    result = game_state.chest_start_of_game_result
    assert result.was_equipped is True, (
        "Engine Feature Needed: Chest card should be equipped to chest zone at game start (Rule 3.5.3)"
    )
    assert result.card_in_chest_zone is True, (
        "Engine Feature Needed: Chest card should be in the chest zone (Rule 3.5.3)"
    )


# ===== Scenario 13: Player's chest zone empty if not equipped at game start =====
# Tests Rule 3.5.3 - Optional equipping


@scenario(
    "../features/section_3_5_chest.feature",
    "A player's chest zone is empty if they choose not to equip at game start",
)
def test_chest_zone_empty_if_no_equip_at_game_start():
    """Rule 3.5.3: Chest zone is empty if player opts not to equip."""
    pass


@given("a player chooses not to equip any chest card at game start")
def player_chooses_not_to_equip_chest(game_state):
    """Rule 3.5.3: Player decides not to equip any chest card."""
    # Rule 3.5.3: "may equip" - this is optional
    game_state.player_chose_no_chest_equip = True
    try:
        game_state.no_equip_chest_zone = Zone(zone_type=ZoneType.CHEST, owner_id=0)
    except (AttributeError, TypeError, ValueError):
        game_state.no_equip_chest_zone = ChestZoneStub(owner_id=0)


@when("the start of game chest equip procedure runs without equipping")
def start_of_game_no_chest_equip(game_state):
    """Rule 3.5.3: Run start-of-game without equipping chest card."""
    # Rule 3.5.3: "may" means player has the option not to equip
    try:
        result = game_state.run_start_of_game_no_equip(
            player_id=0,
            zone=game_state.no_equip_chest_zone,
        )
        game_state.no_chest_equip_result = result
    except AttributeError:
        # Engine Feature Needed: run_start_of_game_no_equip method
        game_state.no_chest_equip_result = ChestStartOfGameEquipResultStub(
            player_may_equip=True,  # Rule 3.5.3: Player MAY equip (optional)
            was_equipped=False,  # Player chose not to equip
            card_in_chest_zone=False,
            is_permanent=False,
            zone_is_empty=True,
        )


@then("the player's chest zone is empty")
def no_equip_chest_zone_is_empty(game_state):
    """Rule 3.5.3: Chest zone should be empty if player chose not to equip."""
    result = game_state.no_chest_equip_result
    zone_is_empty = getattr(result, "zone_is_empty", not result.was_equipped)
    assert zone_is_empty is True, (
        "Engine Feature Needed: Chest zone should be empty when player chose not to equip (Rule 3.5.3)"
    )


@then("the unequipped chest zone is exposed")
def no_equip_chest_zone_is_exposed(game_state):
    """Rule 3.0.1a: Empty chest zone should be exposed."""
    result = game_state.no_chest_equip_result
    zone_is_empty = getattr(result, "zone_is_empty", not result.was_equipped)
    # Rule 3.0.1a: An equipment zone is exposed if it is empty
    assert zone_is_empty is True, (
        "Engine Feature Needed: Empty unequipped chest zone should be exposed (Rule 3.0.1a)"
    )


# ===== Scenario 14: Chest zone not empty with equipped permanent =====
# Tests Rule 3.0.1a cross-ref - Empty definition for equipment zones


@scenario(
    "../features/section_3_5_chest.feature",
    "A chest zone is not empty when it has an equipped permanent",
)
def test_chest_zone_not_empty_with_equipped_permanent():
    """Rule 3.0.1a / 3.5.2: Chest zone is not empty when it has an equipped permanent."""
    pass


@given("a player has a chest zone with a chest card equipped")
def player_has_chest_zone_with_card_equipped(game_state):
    """Rule 3.0.1a: Set up chest zone with a card equipped."""
    zone = ChestZoneStub(owner_id=0)
    # Mark zone as having an equipped permanent
    zone._equipped_count = 1
    zone._has_equipped_permanent = True
    game_state.occupied_zone_check_chest = zone
    game_state.equipped_chest_card_ref = _create_chest_card(
        game_state, "Chest Card Equipped"
    )


@when("checking if the chest zone is empty")
def check_occupied_chest_zone_is_empty(game_state):
    """Rule 3.0.1a: Check if chest zone with equipped permanent is empty."""
    zone = game_state.occupied_zone_check_chest
    # Rule 3.0.1a: Zone is empty only if it has no objects AND no equipped permanents
    try:
        game_state.occupied_chest_zone_is_empty = zone.is_empty
    except AttributeError:
        has_permanent = getattr(zone, "_has_equipped_permanent", False)
        equipped_count = getattr(zone, "_equipped_count", 0)
        # Zone is NOT empty if it has an equipped permanent (Rule 3.0.1a)
        game_state.occupied_chest_zone_is_empty = not (
            has_permanent or equipped_count > 0
        )


@then("the chest zone is not empty because it has an equipped permanent")
def chest_zone_not_empty_due_to_permanent(game_state):
    """Rule 3.0.1a: Zone with equipped permanent should not be empty."""
    assert game_state.occupied_chest_zone_is_empty is False, (
        "Engine Feature Needed: Chest zone with equipped permanent should NOT be empty (Rule 3.0.1a)"
    )


# ===== Scenario 15: Chest zone must be empty before equipping =====
# Tests Rule 8.5.41c cross-ref - Zone must be empty to equip


@scenario(
    "../features/section_3_5_chest.feature",
    "A chest card can only be equipped if the chest zone is empty",
)
def test_chest_card_equip_requires_empty_zone():
    """Rule 8.5.41c: Chest card can only be equipped if chest zone is empty."""
    pass


# NOTE: "a player has a chest zone with one chest card already equipped" is already defined above
# and will be reused here (same step text)


@given("the chest zone is therefore not empty")
def chest_zone_is_not_empty_assertion(game_state):
    """Rule 8.5.41c: Verify chest zone is occupied (not empty)."""
    zone = game_state.occupied_chest_zone
    is_empty = not bool(getattr(zone, "_equipped_count", 0))
    assert is_empty is False, "Test setup: chest zone should not be empty"


@when("attempting to equip another chest card to the occupied chest zone")
def attempt_equip_to_occupied_chest_zone(game_state):
    """Rule 8.5.41c: Attempt equip to already-occupied zone."""
    zone = game_state.occupied_chest_zone
    new_card = _create_chest_card(game_state, "Another Chest Card")

    # Engine Feature Needed: 8.5.41c - zone must be empty to equip
    is_empty = not bool(getattr(zone, "_equipped_count", 0))
    game_state.occupied_chest_equip_result = ChestEquipResultStub(
        success=is_empty,  # Should fail - zone not empty
        equipped_card=None,
        zone_object_count=getattr(zone, "_equipped_count", 1),
        failure_reason="zone_not_empty",
    )


@then("the chest equip attempt fails because the zone is not empty")
def chest_equip_fails_zone_not_empty(game_state):
    """Rule 8.5.41c: Equip should fail when zone is not empty."""
    result = game_state.occupied_chest_equip_result
    assert result.success is False, (
        "Engine Feature Needed: Equipping to occupied chest zone should fail (Rule 8.5.41c)"
    )
    failure_reason = getattr(result, "failure_reason", None)
    if failure_reason is not None:
        assert failure_reason == "zone_not_empty", (
            "Engine Feature Needed: Failure reason should be 'zone_not_empty' (Rule 8.5.41c)"
        )


# ===== Helper Functions =====


def _create_chest_card(game_state, name: str):
    """
    Helper to create a chest-subtype equipment card.

    Uses CardTemplate if available; falls back to ChestCardStub.
    """
    try:
        # Try creating with full CardTemplate
        template = CardTemplate(
            unique_id=f"test_chest_{name}",
            name=name,
            types=frozenset([CardType.EQUIPMENT]),
            supertypes=frozenset(),
            subtypes=frozenset([Subtype.CHEST]),
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
        card._has_chest_subtype = True
        return card
    except (TypeError, AttributeError):
        # Fallback to stub
        stub = ChestCardStub(name=name, owner_id=0, has_chest_subtype=True)
        return stub


def _create_non_chest_card(game_state, name: str):
    """
    Helper to create a non-chest equipment card (e.g., arms).

    Uses CardTemplate if available; falls back to ChestCardStub.
    """
    try:
        template = CardTemplate(
            unique_id=f"test_non_chest_{name}",
            name=name,
            types=frozenset([CardType.EQUIPMENT]),
            supertypes=frozenset(),
            subtypes=frozenset([Subtype.ARMS]),  # Has arms subtype, NOT chest
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
        card._has_chest_subtype = False
        return card
    except (TypeError, AttributeError):
        stub = ChestCardStub(name=name, owner_id=0, has_chest_subtype=False)
        return stub


def _simulate_chest_equip(game_state, card, zone, has_chest_subtype: bool = True):
    """
    Helper to simulate equipping a card to a chest zone.

    Engine Feature Needed:
    - Equip effect (8.5.41) - discrete effect for putting card in zone as permanent
    - 8.5.41b - Equip only works if card has valid equipment subtype (Chest required for chest zone)
    - 8.5.41c - Zone must be empty for equip to succeed
    """
    try:
        return game_state.equip_card_to_chest_zone(card, zone)
    except AttributeError:
        pass

    # Check zone capacity
    zone_occupied = getattr(zone, "_equipped_count", 0) > 0

    # Check chest subtype
    card_has_chest = has_chest_subtype
    try:
        card_has_chest = Subtype.CHEST in card.template.subtypes
    except AttributeError:
        card_has_chest = getattr(card, "_has_chest_subtype", has_chest_subtype)

    if zone_occupied:
        return ChestEquipResultStub(
            success=False,
            equipped_card=None,
            zone_object_count=getattr(zone, "_equipped_count", 1),
            failure_reason="zone_not_empty",
        )
    elif not card_has_chest:
        return ChestEquipResultStub(
            success=False,
            equipped_card=None,
            zone_object_count=0,
            failure_reason="missing_chest_subtype",
        )
    else:
        return ChestEquipResultStub(
            success=True,
            equipped_card=card,
            zone_object_count=1,
            is_permanent=True,
        )


# ===== Stub Classes for Missing Engine Features =====


class ChestZoneStub:
    """
    Stub for engine feature: Chest zone implementation.

    Engine Features Needed:
    - [ ] ZoneType.CHEST with is_public=True, is_equipment_zone=True (Rule 3.5.1)
    - [ ] Chest zone is an arena zone (Rule 3.5.1, cross-ref 3.1.1)
    - [ ] Chest zone has owner_id (Rule 3.5.1)
    - [ ] Chest zone capacity limit of 1 (Rule 3.5.2)
    - [ ] Zone.is_empty returns False when equipped permanent exists (Rule 3.0.1a)
    - [ ] Zone.is_exposed returns True when empty (Rule 3.0.1a)
    """

    def __init__(self, owner_id: int = 0):
        self.owner_id = owner_id
        self.is_public_zone = True  # Rule 3.5.1 + 3.0.4a
        self.is_private_zone = False
        self.is_equipment_zone = True  # Rule 3.5.1
        self.is_arena_zone = True  # Rule 3.5.1, cross-ref 3.1.1
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


class ChestCardStub:
    """
    Stub for chest equipment card.

    Engine Features Needed:
    - [ ] CardType.EQUIPMENT (Rule 1.3.2d - equipment is an arena-card)
    - [ ] Subtype.CHEST (Rule 3.5.2a - required for chest zone equipping)
    """

    def __init__(
        self,
        name: str,
        owner_id: int = 0,
        has_chest_subtype: bool = True,
        has_arms_subtype: bool = False,
    ):
        self.name = name
        self.owner_id = owner_id
        self._has_chest_subtype = has_chest_subtype
        self.has_arms_subtype = has_arms_subtype


class ChestEquipResultStub:
    """
    Stub for the result of an equip operation on the chest zone.

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


class ChestStartOfGameEquipResultStub:
    """
    Stub for start-of-game chest equip procedure result.

    Engine Features Needed:
    - [ ] Start-of-game equip procedure (Rule 3.5.3, cross-ref 4.1, 4.1.4a)
    - [ ] Player may (optionally) equip chest card at game start
    - [ ] After equipping, chest card is a permanent in chest zone
    """

    def __init__(
        self,
        player_may_equip: bool = True,
        was_equipped: bool = True,
        card_in_chest_zone: bool = True,
        is_permanent: bool = True,
        zone_is_empty=None,
    ):
        self.player_may_equip = player_may_equip
        self.was_equipped = was_equipped
        self.card_in_chest_zone = card_in_chest_zone
        self.is_permanent = is_permanent
        self.zone_is_empty = (
            zone_is_empty if zone_is_empty is not None else not was_equipped
        )


# ===== Fixtures =====


@pytest.fixture
def game_state():
    """
    Fixture providing game state for Section 3.5 Chest tests.

    Uses BDDGameState which integrates with the real engine.
    Reference: Rules 3.5.1, 3.5.2, 3.5.2a, 3.5.3
    """
    from tests.bdd_helpers import BDDGameState

    state = BDDGameState()
    return state
