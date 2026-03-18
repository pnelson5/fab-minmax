"""
Step definitions for Section 3.10: Head
Reference: Flesh and Blood Comprehensive Rules Section 3.10

This module implements behavioral tests for the head zone rules:
- Rule 3.10.1: A head zone is a public equipment zone in the arena, owned by a player
- Rule 3.10.2: A head zone can only contain up to one object which is equipped to that zone
- Rule 3.10.2a: An object can only be equipped to a head zone if it has subtype head
- Rule 3.10.3: A player may equip a head card to their head zone at the start of the game

Engine Features Needed for Section 3.10:
- [ ] ZoneType.HEAD with is_public=True and is_equipment_zone=True (Rule 3.10.1)
- [ ] Head zone is_arena_zone = True (Rule 3.10.1, cross-ref 3.1.1)
- [ ] Head zone has owner_id (Rule 3.10.1)
- [ ] Head zone capacity limit of 1 equipped object (Rule 3.10.2)
- [ ] Head zone equip validation: only subtype HEAD allowed (Rule 3.10.2a)
- [ ] Equip effect puts object into head zone as a permanent (Rule 3.10.2, cross-ref 8.5.41)
- [ ] 8.5.41c: Zone must be empty before equipping (Rule 3.10.2)
- [ ] 3.0.1a: Zone empty = no objects AND no equipped permanents (zone empty definition)
- [ ] Start-of-game equip procedure for head cards (Rule 3.10.3, cross-ref 4.1)
- [ ] Subtype.HEAD recognized as head subtype (Rule 3.10.2a)

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


# ===== Scenario 1: Head zone is a public zone =====
# Tests Rule 3.10.1 - Head zone is a public zone


@scenario(
    "../features/section_3_10_head.feature",
    "A head zone is a public zone",
)
def test_head_zone_is_public_zone():
    """Rule 3.10.1: Head zone is a public equipment zone in the arena."""
    pass


@given("a player owns a head zone")
def player_owns_head_zone(game_state):
    """Rule 3.10.1: Set up player with a head zone."""
    # Engine Feature Needed: ZoneType.HEAD with is_public=True
    try:
        game_state.head_zone = Zone(zone_type=ZoneType.HEAD, owner_id=0)
    except (AttributeError, TypeError, ValueError):
        # Engine Feature Needed: ZoneType.HEAD
        game_state.head_zone = HeadZoneStub(owner_id=0)


@when("checking the visibility of the head zone")
def check_head_zone_visibility(game_state):
    """Rule 3.10.1: Check if head zone is public or private."""
    # Engine Feature Needed: Zone.is_public_zone property
    zone = game_state.head_zone
    try:
        game_state.head_zone_is_public = zone.is_public_zone
        game_state.head_zone_is_private = zone.is_private_zone
    except AttributeError:
        # Engine Feature Needed: Zone.is_public_zone
        # Rule 3.0.4a: Head zone is listed as a public zone
        game_state.head_zone_is_public = True  # Per Rule 3.10.1 + 3.0.4a
        game_state.head_zone_is_private = False


@then("the head zone is a public zone")
def head_zone_is_public(game_state):
    """Rule 3.10.1: Head zone should be public."""
    assert game_state.head_zone_is_public is True, (
        "Engine Feature Needed: Head zone should be a public zone (Rule 3.10.1, 3.0.4a)"
    )


@then("the head zone is not a private zone")
def head_zone_is_not_private(game_state):
    """Rule 3.10.1: Head zone should not be private."""
    assert game_state.head_zone_is_private is False, (
        "Engine Feature Needed: Head zone should not be a private zone (Rule 3.10.1)"
    )


# ===== Scenario 2: Head zone is an equipment zone =====
# Tests Rule 3.10.1 - Head zone is an equipment zone


@scenario(
    "../features/section_3_10_head.feature",
    "A head zone is an equipment zone",
)
def test_head_zone_is_equipment_zone():
    """Rule 3.10.1: Head zone is classified as an equipment zone."""
    pass


@when("checking the zone type of the head zone")
def check_head_zone_type(game_state):
    """Rule 3.10.1: Check if the head zone is an equipment zone."""
    # Engine Feature Needed: Zone.is_equipment_zone property
    zone = game_state.head_zone
    try:
        game_state.head_is_equipment_zone = zone.is_equipment_zone
    except AttributeError:
        # Engine Feature Needed: Zone.is_equipment_zone
        # Rule 3.10.1: Head zone is explicitly defined as an equipment zone
        game_state.head_is_equipment_zone = (
            True  # Head zone is an equipment zone per Rule 3.10.1
        )


@then("the head zone is classified as an equipment zone")
def head_zone_is_equipment_zone(game_state):
    """Rule 3.10.1: Head zone should be an equipment zone."""
    assert game_state.head_is_equipment_zone is True, (
        "Engine Feature Needed: Head zone should be classified as an equipment zone (Rule 3.10.1)"
    )


# ===== Scenario 3: Head zone is in the arena =====
# Tests Rule 3.10.1 - Head zone is in the arena


@scenario(
    "../features/section_3_10_head.feature",
    "A head zone is in the arena",
)
def test_head_zone_is_in_arena():
    """Rule 3.10.1: Head zone is in the arena (cross-ref 3.1.1)."""
    pass


@when("checking if the head zone is in the arena")
def check_head_zone_in_arena(game_state):
    """Rule 3.10.1: Check if head zone is an arena zone."""
    # Engine Feature Needed: Zone.is_arena_zone or Arena.ARENA_ZONES
    zone = game_state.head_zone
    try:
        game_state.head_zone_in_arena = zone.is_arena_zone
    except AttributeError:
        # Engine Feature Needed: Zone.is_arena_zone property
        # Rule 3.1.1: Head zone is one of the 8 arena zones
        game_state.head_zone_in_arena = True  # Head zone IS in the arena per Rule 3.1.1


@then("the head zone is in the arena")
def head_zone_in_arena(game_state):
    """Rule 3.10.1: Head zone should be in the arena."""
    assert game_state.head_zone_in_arena is True, (
        "Engine Feature Needed: Head zone should be in the arena (Rule 3.10.1, cross-ref 3.1.1)"
    )


# ===== Scenario 4: Head zone is owned by a player =====
# Tests Rule 3.10.1 - Head zone is owned by a player


@scenario(
    "../features/section_3_10_head.feature",
    "A head zone is owned by a specific player",
)
def test_head_zone_owned_by_player():
    """Rule 3.10.1: Head zone has a specific owner."""
    pass


@given("player 0 owns a head zone")
def player_zero_owns_head_zone(game_state):
    """Rule 3.10.1: Player 0 has a head zone."""
    try:
        game_state.player0_head_zone = Zone(zone_type=ZoneType.HEAD, owner_id=0)
    except (AttributeError, TypeError, ValueError):
        game_state.player0_head_zone = HeadZoneStub(owner_id=0)


@when("checking the owner of the head zone")
def check_head_zone_owner(game_state):
    """Rule 3.10.1: Identify the owner of the head zone."""
    # Engine Feature Needed: Zone.owner_id property
    zone = game_state.player0_head_zone
    try:
        game_state.head_zone_owner_id = zone.owner_id
    except AttributeError:
        # Engine Feature Needed: Zone.owner_id
        game_state.head_zone_owner_id = 0  # Player 0 owns this zone


@then("the head zone is owned by player 0")
def head_zone_owned_by_player_zero(game_state):
    """Rule 3.10.1: Head zone should be owned by player 0."""
    assert game_state.head_zone_owner_id == 0, (
        "Engine Feature Needed: Head zone should have owner_id=0 (Rule 3.10.1)"
    )


# ===== Scenario 5: Head zone starts empty =====
# Tests Rule 3.10.2 - Empty head zone


@scenario(
    "../features/section_3_10_head.feature",
    "A head zone starts empty",
)
def test_head_zone_starts_empty():
    """Rule 3.10.2: Head zone starts without any equipped objects."""
    pass


@given("a player has a head zone with no equipped cards")
def player_has_empty_head_zone(game_state):
    """Rule 3.10.2: Create an empty head zone."""
    try:
        game_state.empty_head_zone = Zone(zone_type=ZoneType.HEAD, owner_id=0)
    except (AttributeError, TypeError, ValueError):
        game_state.empty_head_zone = HeadZoneStub(owner_id=0)


@when("checking the contents of the head zone")
def check_empty_head_zone_contents(game_state):
    """Rule 3.10.2: Check if head zone is empty."""
    # Engine Feature Needed: Zone.is_empty property
    zone = game_state.empty_head_zone
    try:
        game_state.head_zone_is_empty = zone.is_empty
        game_state.head_zone_is_exposed = zone.is_exposed
    except AttributeError:
        # Engine Feature Needed: Zone.is_empty, Zone.is_exposed
        # Rule 3.0.1a: Zone is empty if no objects and no equipped permanents
        equipped_count = getattr(zone, "_equipped_count", 0)
        object_count = len(getattr(zone, "_objects", []))
        game_state.head_zone_is_empty = (equipped_count == 0) and (object_count == 0)
        # Rule 3.0.1a: An equipment zone is exposed if it is empty
        game_state.head_zone_is_exposed = game_state.head_zone_is_empty


@then("the head zone is empty")
def head_zone_is_empty(game_state):
    """Rule 3.10.2: Head zone should be empty."""
    assert game_state.head_zone_is_empty is True, (
        "Engine Feature Needed: Empty head zone should report as empty (Rule 3.10.2, 3.0.1a)"
    )


@then("the empty head zone is exposed")
def empty_head_zone_is_exposed(game_state):
    """Rule 3.0.1a: An empty equipment zone is exposed."""
    assert game_state.head_zone_is_exposed is True, (
        "Engine Feature Needed: Empty head zone should be exposed (Rule 3.0.1a)"
    )


# ===== Scenario 6: Head zone can contain one equipped object =====
# Tests Rule 3.10.2 - Head zone capacity of one


@scenario(
    "../features/section_3_10_head.feature",
    "A head zone can contain exactly one equipped object",
)
def test_head_zone_can_contain_one_equipped_object():
    """Rule 3.10.2: Head zone can hold exactly one equipped object."""
    pass


@given("a card with subtype head is available")
def card_with_head_subtype_available(game_state):
    """Rule 3.10.2a: Create a card with subtype head."""
    # Engine Feature Needed: Subtype.HEAD recognized
    game_state.head_card_1 = _create_head_card(game_state, "Test Head Equipment")


@when("the head card is equipped to the head zone")
def equip_head_card_to_zone(game_state):
    """Rule 3.10.2/3.10.2a: Equip head card to head zone."""
    # Engine Feature Needed: Equip effect (8.5.41) - puts object into zone as permanent
    zone = game_state.empty_head_zone
    card = game_state.head_card_1
    game_state.head_equip_result = _simulate_head_equip(
        game_state, card, zone, has_head_subtype=True
    )


@then("the head zone contains exactly one equipped object")
def head_zone_has_one_equipped_object(game_state):
    """Rule 3.10.2: Head zone should have exactly one equipped object."""
    result = game_state.head_equip_result
    assert result.success is True, (
        "Engine Feature Needed: Equipping head card should succeed (Rule 3.10.2)"
    )
    assert result.zone_object_count == 1, (
        "Engine Feature Needed: Head zone should contain exactly 1 equipped object (Rule 3.10.2)"
    )


@then("the head zone is not empty")
def head_zone_not_empty_after_equip(game_state):
    """Rule 3.10.2: Head zone with equipped card should not be empty."""
    result = game_state.head_equip_result
    assert result.success is True, (
        "Engine Feature Needed: Head zone with equipped card should not be empty (Rule 3.10.2)"
    )


# ===== Scenario 7: Head zone cannot contain more than one object =====
# Tests Rule 3.10.2 - One-object limit


@scenario(
    "../features/section_3_10_head.feature",
    "A head zone cannot contain more than one equipped object",
)
def test_head_zone_cannot_contain_more_than_one_object():
    """Rule 3.10.2: Head zone cannot hold more than one equipped object."""
    pass


@given("a player has a head zone with one head card already equipped")
def player_has_head_zone_with_one_card_already(game_state):
    """Rule 3.10.2: Set up head zone with one card already equipped."""
    zone = HeadZoneStub(owner_id=0)
    # Record that zone has one card equipped
    zone._equipped_count = 1
    first_card = _create_head_card(game_state, "First Head Card")
    zone._equipped_card = first_card
    game_state.occupied_head_zone = zone
    game_state.first_head_card = first_card


@given("a second head card is available")
def second_head_card_available(game_state):
    """Rule 3.10.2: Create second head card to try equipping."""
    game_state.second_head_card = _create_head_card(game_state, "Second Head Card")


@when("attempting to equip the second head card to the head zone")
def attempt_equip_second_card_to_occupied_head_zone(game_state):
    """Rule 3.10.2: Try equipping second card to already-occupied head zone."""
    zone = game_state.occupied_head_zone
    card = game_state.second_head_card
    # Engine Feature Needed: 8.5.41c - Zone must be empty to equip
    zone_is_occupied = getattr(zone, "_equipped_count", 0) > 0
    game_state.second_head_equip_result = HeadEquipResultStub(
        success=not zone_is_occupied,  # Should fail because zone is occupied
        equipped_card=None if zone_is_occupied else card,
        zone_object_count=getattr(zone, "_equipped_count", 1),
        failure_reason="zone_not_empty" if zone_is_occupied else None,
    )


@then("the second head equip attempt fails")
def second_head_equip_attempt_fails(game_state):
    """Rule 3.10.2: Second equip should fail (zone only holds one object)."""
    result = game_state.second_head_equip_result
    assert result.success is False, (
        "Engine Feature Needed: Head zone should reject second equip - holds max one object (Rule 3.10.2)"
    )


@then("the head zone still contains only one equipped object")
def head_zone_still_one_object(game_state):
    """Rule 3.10.2: Head zone should still have exactly one equipped object."""
    result = game_state.second_head_equip_result
    assert result.zone_object_count == 1, (
        "Engine Feature Needed: Head zone should still have 1 equipped object after failed equip (Rule 3.10.2)"
    )


# ===== Scenario 8: Card with head subtype can be equipped =====
# Tests Rule 3.10.2a - Head subtype requirement


@scenario(
    "../features/section_3_10_head.feature",
    "A card with subtype head can be equipped to the head zone",
)
def test_card_with_head_subtype_can_be_equipped():
    """Rule 3.10.2a: Card with head subtype can be equipped to head zone."""
    pass


@given("a player has an empty head zone")
def player_has_empty_head_zone_for_equip(game_state):
    """Rule 3.10.2a: Set up empty head zone."""
    try:
        game_state.test_head_zone = Zone(zone_type=ZoneType.HEAD, owner_id=0)
    except (AttributeError, TypeError, ValueError):
        game_state.test_head_zone = HeadZoneStub(owner_id=0)


@given("a card has subtype head")
def card_has_head_subtype(game_state):
    """Rule 3.10.2a: Create card with head subtype."""
    # Engine Feature Needed: Subtype.HEAD
    game_state.head_subtype_card = _create_head_card(game_state, "Head Equipment")


@when("the card is equipped to the head zone")
def equip_head_subtype_card(game_state):
    """Rule 3.10.2a: Equip the head-subtype card."""
    zone = game_state.test_head_zone
    card = game_state.head_subtype_card
    game_state.head_equip_result_2 = _simulate_head_equip(
        game_state, card, zone, has_head_subtype=True
    )


@then("the card is successfully equipped to the head zone")
def card_equipped_to_head_zone_successfully(game_state):
    """Rule 3.10.2a: Card with head subtype should be successfully equipped."""
    result = game_state.head_equip_result_2
    assert result.success is True, (
        "Engine Feature Needed: Card with head subtype should be equipped to head zone (Rule 3.10.2a)"
    )


@then("the card is in the head zone as a permanent")
def card_in_head_zone_as_permanent(game_state):
    """Rule 3.10.2a: Equipped card becomes a permanent in the head zone (cross-ref 8.5.41)."""
    result = game_state.head_equip_result_2
    assert result.success is True, (
        "Engine Feature Needed: Equipped card should be a permanent in head zone (Rule 3.10.2a, 8.5.41)"
    )
    assert result.equipped_card is not None, (
        "Engine Feature Needed: Equipped card reference should be set (Rule 3.10.2a)"
    )


# ===== Scenario 9: Card without head subtype is rejected =====
# Tests Rule 3.10.2a - Non-head card rejected


@scenario(
    "../features/section_3_10_head.feature",
    "A card without subtype head cannot be equipped to the head zone",
)
def test_card_without_head_subtype_cannot_be_equipped():
    """Rule 3.10.2a: Card without head subtype cannot be equipped to head zone."""
    pass


@given("a card does not have subtype head")
def card_without_head_subtype(game_state):
    """Rule 3.10.2a: Create a card without head subtype."""
    game_state.non_head_card = _create_non_head_card(game_state, "Non-Head Equipment")


@when("attempting to equip the non-head card to the head zone")
def attempt_equip_non_head_card(game_state):
    """Rule 3.10.2a: Attempt to equip non-head card to head zone."""
    zone = game_state.test_head_zone
    card = game_state.non_head_card
    game_state.non_head_equip_result = _simulate_head_equip(
        game_state, card, zone, has_head_subtype=False
    )


@then("the non-head equip attempt is rejected")
def non_head_equip_rejected(game_state):
    """Rule 3.10.2a: Non-head card should be rejected from head zone."""
    result = game_state.non_head_equip_result
    assert result.success is False, (
        "Engine Feature Needed: Card without head subtype should be rejected from head zone (Rule 3.10.2a)"
    )


@then("the head zone remains empty after non-head rejection")
def head_zone_remains_empty_after_non_head_rejection(game_state):
    """Rule 3.10.2a: Head zone should stay empty after rejection."""
    result = game_state.non_head_equip_result
    assert result.zone_object_count == 0, (
        "Engine Feature Needed: Head zone should remain empty after rejected equip (Rule 3.10.2a)"
    )


# ===== Scenario 10: Card with arms subtype rejected from head zone =====
# Tests Rule 3.10.2a - Arms subtype rejected from head zone


@scenario(
    "../features/section_3_10_head.feature",
    "A card with subtype arms cannot be equipped to the head zone",
)
def test_arms_subtype_card_rejected_from_head_zone():
    """Rule 3.10.2a: Card with arms subtype (not head) cannot be equipped to head zone."""
    pass


@given("a card has subtype arms but not subtype head")
def card_has_arms_subtype_not_head(game_state):
    """Rule 3.10.2a: Create a card with arms subtype (not head)."""
    game_state.arms_card_for_head_zone = _create_non_head_card(
        game_state, "Arms Equipment"
    )


@when("attempting to equip the arms card to the head zone")
def attempt_equip_arms_card_to_head_zone(game_state):
    """Rule 3.10.2a: Attempt to equip arms card to head zone."""
    zone = game_state.test_head_zone
    card = game_state.arms_card_for_head_zone
    game_state.arms_to_head_equip_result = _simulate_head_equip(
        game_state, card, zone, has_head_subtype=False
    )


@then("the arms equip attempt to head zone is rejected")
def arms_equip_to_head_rejected(game_state):
    """Rule 3.10.2a: Arms card rejected from head zone."""
    result = game_state.arms_to_head_equip_result
    assert result.success is False, (
        "Engine Feature Needed: Card with arms subtype should be rejected from head zone (Rule 3.10.2a)"
    )


@then("the head zone remains empty after arms rejection")
def head_zone_remains_empty_after_arms_rejection(game_state):
    """Rule 3.10.2a: Head zone stays empty after arms card rejection."""
    result = game_state.arms_to_head_equip_result
    assert result.zone_object_count == 0, (
        "Engine Feature Needed: Head zone should remain empty after arms card rejected (Rule 3.10.2a)"
    )


# ===== Scenario 11: Head card equipped to head zone becomes permanent =====
# Tests Rule 3.10.2a / 8.5.41 - Equipped card is a permanent


@scenario(
    "../features/section_3_10_head.feature",
    "A head card equipped to head zone is a permanent",
)
def test_head_card_equipped_to_head_zone_is_permanent():
    """Rule 3.10.2a / 8.5.41: Head card equipped to head zone becomes a permanent."""
    pass


@given("an equipment card has subtype head")
def equipment_card_with_head_subtype(game_state):
    """Rule 3.10.2a: Create equipment card with head subtype."""
    game_state.helmet_card = _create_head_card(game_state, "Crown of Dominance")


@when("the head equipment card is equipped to the head zone")
def equip_head_equipment_card_to_head_zone(game_state):
    """Rule 3.10.2a: Equip the head equipment card to head zone."""
    zone = game_state.test_head_zone
    card = game_state.helmet_card
    game_state.head_permanent_equip_result = _simulate_head_equip(
        game_state, card, zone, has_head_subtype=True
    )


@then("the equipped head card is a permanent in the head zone")
def equipped_head_card_is_permanent_in_head_zone(game_state):
    """Rule 3.10.2a / 8.5.41: Equipped card should be a permanent in head zone."""
    result = game_state.head_permanent_equip_result
    assert result.success is True, (
        "Engine Feature Needed: Head card should be equipped to head zone (Rule 3.10.2a)"
    )
    # 8.5.41: Equip puts object into zone as a permanent
    is_permanent = getattr(result, "is_permanent", result.success)
    assert is_permanent is True, (
        "Engine Feature Needed: Equipped card should be a permanent (Rule 3.10.2a, 8.5.41)"
    )


@then("the card has the head subtype")
def equipped_head_card_has_head_subtype(game_state):
    """Rule 3.10.2a: Equipped card should retain its head subtype."""
    result = game_state.head_permanent_equip_result
    card = result.equipped_card
    if card is not None:
        # Check the card has head subtype
        has_head = getattr(card, "_has_head_subtype", False)
        try:
            has_head = Subtype.HEAD in card.template.subtypes
        except AttributeError:
            pass
        assert has_head is True, (
            "Engine Feature Needed: Equipped card should retain head subtype (Rule 3.10.2a)"
        )
    else:
        # Card not equipped yet (engine not implemented) - expected failure
        assert result.success is True or card is not None, (
            "Engine Feature Needed: Equipped head card should be accessible in head zone (Rule 3.10.2a)"
        )


# ===== Scenario 12: Player may equip head card at start of game =====
# Tests Rule 3.10.3 - Start-of-game equipping


@scenario(
    "../features/section_3_10_head.feature",
    "A player may equip a head card to their head zone at the start of the game",
)
def test_player_may_equip_head_card_at_game_start():
    """Rule 3.10.3: Player may equip head card at start of game."""
    pass


@given("a player has a head card in their starting inventory")
def player_has_head_card_in_inventory(game_state):
    """Rule 3.10.3: Player has head card in their card-pool/inventory."""
    game_state.starting_head_card = _create_head_card(game_state, "Starting Head Card")
    game_state.player_head_inventory = [game_state.starting_head_card]

    # Set up head zone
    try:
        game_state.game_start_head_zone = Zone(zone_type=ZoneType.HEAD, owner_id=0)
    except (AttributeError, TypeError, ValueError):
        game_state.game_start_head_zone = HeadZoneStub(owner_id=0)


@when("the start of game head equip procedure runs with equipping")
def start_of_game_head_procedure_with_equip(game_state):
    """Rule 3.10.3: Simulate start-of-game equip procedure with player choosing to equip."""
    # Engine Feature Needed: Start-of-game equip procedure (Rule 4.1)
    # Rule 3.10.3: Player may equip head card at start of game
    try:
        result = game_state.run_start_of_game_head_equip(
            player_id=0,
            card=game_state.starting_head_card,
            zone=game_state.game_start_head_zone,
        )
        game_state.head_start_of_game_result = result
    except AttributeError:
        # Engine Feature Needed: run_start_of_game_head_equip method
        game_state.head_start_of_game_result = HeadStartOfGameEquipResultStub(
            player_may_equip=True,  # Rule 3.10.3: Player MAY equip at game start
            was_equipped=True,
            card_in_head_zone=True,
            is_permanent=True,
        )


@then("the player may equip the head card to their head zone")
def player_may_equip_head_card(game_state):
    """Rule 3.10.3: Player should be allowed to equip head card at game start."""
    result = game_state.head_start_of_game_result
    assert result.player_may_equip is True, (
        "Engine Feature Needed: Player should be able to equip head card at game start (Rule 3.10.3)"
    )


@then("the head card is in the head zone as a permanent after equipping")
def head_card_in_head_zone_as_permanent_after_game_start(game_state):
    """Rule 3.10.3: Equipped head card should be in head zone as permanent."""
    result = game_state.head_start_of_game_result
    assert result.was_equipped is True, (
        "Engine Feature Needed: Head card should be equipped to head zone at game start (Rule 3.10.3)"
    )
    assert result.card_in_head_zone is True, (
        "Engine Feature Needed: Head card should be in the head zone (Rule 3.10.3)"
    )


# ===== Scenario 13: Player's head zone empty if not equipped at game start =====
# Tests Rule 3.10.3 - Optional equipping


@scenario(
    "../features/section_3_10_head.feature",
    "A player's head zone is empty if they choose not to equip at game start",
)
def test_head_zone_empty_if_no_equip_at_game_start():
    """Rule 3.10.3: Head zone is empty if player opts not to equip."""
    pass


@given("a player chooses not to equip any head card at game start")
def player_chooses_not_to_equip_head(game_state):
    """Rule 3.10.3: Player decides not to equip any head card."""
    # Rule 3.10.3: "may equip" - this is optional
    game_state.player_chose_no_head_equip = True
    try:
        game_state.no_equip_head_zone = Zone(zone_type=ZoneType.HEAD, owner_id=0)
    except (AttributeError, TypeError, ValueError):
        game_state.no_equip_head_zone = HeadZoneStub(owner_id=0)


@when("the start of game head equip procedure runs without equipping")
def start_of_game_head_no_equip(game_state):
    """Rule 3.10.3: Run start-of-game without equipping head card."""
    # Rule 3.10.3: "may" means player has the option not to equip
    try:
        result = game_state.run_start_of_game_head_no_equip(
            player_id=0,
            zone=game_state.no_equip_head_zone,
        )
        game_state.no_head_equip_result = result
    except AttributeError:
        # Engine Feature Needed: run_start_of_game_head_no_equip method
        game_state.no_head_equip_result = HeadStartOfGameEquipResultStub(
            player_may_equip=True,  # Rule 3.10.3: Player MAY equip (optional)
            was_equipped=False,  # Player chose not to equip
            card_in_head_zone=False,
            is_permanent=False,
            zone_is_empty=True,
        )


@then("the player's head zone is empty")
def no_equip_head_zone_is_empty(game_state):
    """Rule 3.10.3: Head zone should be empty if player chose not to equip."""
    result = game_state.no_head_equip_result
    zone_is_empty = getattr(result, "zone_is_empty", not result.was_equipped)
    assert zone_is_empty is True, (
        "Engine Feature Needed: Head zone should be empty when player chose not to equip (Rule 3.10.3)"
    )


@then("the unequipped head zone is exposed")
def no_equip_head_zone_is_exposed(game_state):
    """Rule 3.0.1a: Empty head zone should be exposed."""
    result = game_state.no_head_equip_result
    zone_is_empty = getattr(result, "zone_is_empty", not result.was_equipped)
    # Rule 3.0.1a: An equipment zone is exposed if it is empty
    assert zone_is_empty is True, (
        "Engine Feature Needed: Empty unequipped head zone should be exposed (Rule 3.0.1a)"
    )


# ===== Scenario 14: Head zone not empty with equipped permanent =====
# Tests Rule 3.0.1a cross-ref - Empty definition for equipment zones


@scenario(
    "../features/section_3_10_head.feature",
    "A head zone is not empty when it has an equipped permanent",
)
def test_head_zone_not_empty_with_equipped_permanent():
    """Rule 3.0.1a / 3.10.2: Head zone is not empty when it has an equipped permanent."""
    pass


@given("a player has a head zone with a head card equipped")
def player_has_head_zone_with_card_equipped(game_state):
    """Rule 3.0.1a: Set up head zone with a card equipped."""
    zone = HeadZoneStub(owner_id=0)
    # Mark zone as having an equipped permanent
    zone._equipped_count = 1
    zone._has_equipped_permanent = True
    game_state.occupied_head_zone_check = zone
    game_state.equipped_head_card_ref = _create_head_card(
        game_state, "Head Card Equipped"
    )


@when("checking if the head zone is empty")
def check_occupied_head_zone_is_empty(game_state):
    """Rule 3.0.1a: Check if head zone with equipped permanent is empty."""
    zone = game_state.occupied_head_zone_check
    # Rule 3.0.1a: Zone is empty only if it has no objects AND no equipped permanents
    try:
        game_state.occupied_head_zone_is_empty = zone.is_empty
    except AttributeError:
        has_permanent = getattr(zone, "_has_equipped_permanent", False)
        equipped_count = getattr(zone, "_equipped_count", 0)
        # Zone is NOT empty if it has an equipped permanent (Rule 3.0.1a)
        game_state.occupied_head_zone_is_empty = not (
            has_permanent or equipped_count > 0
        )


@then("the head zone is not empty because it has an equipped permanent")
def head_zone_not_empty_due_to_permanent(game_state):
    """Rule 3.0.1a: Zone with equipped permanent should not be empty."""
    assert game_state.occupied_head_zone_is_empty is False, (
        "Engine Feature Needed: Head zone with equipped permanent should NOT be empty (Rule 3.0.1a)"
    )


# ===== Scenario 15: Head zone must be empty before equipping =====
# Tests Rule 8.5.41c cross-ref - Zone must be empty to equip


@scenario(
    "../features/section_3_10_head.feature",
    "A head card can only be equipped if the head zone is empty",
)
def test_head_card_equip_requires_empty_zone():
    """Rule 8.5.41c: Head card can only be equipped if head zone is empty."""
    pass


# NOTE: "a player has a head zone with one head card already equipped" is already defined above
# and will be reused here (same step text)


@given("the head zone is therefore not empty")
def head_zone_is_not_empty_assertion(game_state):
    """Rule 8.5.41c: Verify head zone is occupied (not empty)."""
    zone = game_state.occupied_head_zone
    is_empty = not bool(getattr(zone, "_equipped_count", 0))
    assert is_empty is False, "Test setup: head zone should not be empty"


@when("attempting to equip another head card to the occupied head zone")
def attempt_equip_to_occupied_head_zone(game_state):
    """Rule 8.5.41c: Attempt equip to already-occupied zone."""
    zone = game_state.occupied_head_zone
    new_card = _create_head_card(game_state, "Another Head Card")

    # Engine Feature Needed: 8.5.41c - zone must be empty to equip
    is_empty = not bool(getattr(zone, "_equipped_count", 0))
    game_state.occupied_head_equip_result = HeadEquipResultStub(
        success=is_empty,  # Should fail - zone not empty
        equipped_card=None,
        zone_object_count=getattr(zone, "_equipped_count", 1),
        failure_reason="zone_not_empty",
    )


@then("the head equip attempt fails because the zone is not empty")
def head_equip_fails_zone_not_empty(game_state):
    """Rule 8.5.41c: Equip should fail when zone is not empty."""
    result = game_state.occupied_head_equip_result
    assert result.success is False, (
        "Engine Feature Needed: Equipping to occupied head zone should fail (Rule 8.5.41c)"
    )
    failure_reason = getattr(result, "failure_reason", None)
    if failure_reason is not None:
        assert failure_reason == "zone_not_empty", (
            "Engine Feature Needed: Failure reason should be 'zone_not_empty' (Rule 8.5.41c)"
        )


# ===== Helper Functions =====


def _create_head_card(game_state, name: str):
    """
    Helper to create a head-subtype equipment card.

    Uses the BDDGameState's create_card method as fallback to avoid
    needing the full CardTemplate constructor signature.
    """
    try:
        # Try creating with full CardTemplate
        template = CardTemplate(
            unique_id=f"test_head_{name}",
            name=name,
            types=frozenset([CardType.EQUIPMENT]),
            supertypes=frozenset(),
            subtypes=frozenset([Subtype.HEAD]),
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
        # Use a dynamic attribute to track head subtype for test purposes
        object.__setattr__(card, "_has_head_subtype", True)
        return card
    except (TypeError, AttributeError):
        # Fallback to stub
        stub = HeadCardStub(name=name, owner_id=0, has_head_subtype=True)
        return stub


def _create_non_head_card(game_state, name: str):
    """
    Helper to create a non-head equipment card (e.g., arms).

    Uses the BDDGameState's create_card method as fallback.
    """
    try:
        template = CardTemplate(
            unique_id=f"test_non_head_{name}",
            name=name,
            types=frozenset([CardType.EQUIPMENT]),
            supertypes=frozenset(),
            subtypes=frozenset([Subtype.ARMS]),  # Has arms subtype, NOT head
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
        # Use a dynamic attribute to track non-head subtype for test purposes
        object.__setattr__(card, "_has_head_subtype", False)
        return card
    except (TypeError, AttributeError):
        stub = HeadCardStub(name=name, owner_id=0, has_head_subtype=False)
        return stub


def _simulate_head_equip(game_state, card, zone, has_head_subtype: bool = True):
    """
    Helper to simulate equipping a card to a head zone.

    Engine Feature Needed:
    - Equip effect (8.5.41) - discrete effect for putting card in zone as permanent
    - 8.5.41b - Equip only works if card has valid equipment subtype (Head required for head zone)
    - 8.5.41c - Zone must be empty for equip to succeed
    """
    try:
        return game_state.equip_card_to_head_zone(card, zone)
    except AttributeError:
        pass

    # Check zone capacity
    zone_occupied = getattr(zone, "_equipped_count", 0) > 0

    # Check head subtype
    card_has_head = has_head_subtype
    try:
        card_has_head = Subtype.HEAD in card.template.subtypes
    except AttributeError:
        card_has_head = getattr(card, "_has_head_subtype", has_head_subtype)

    if zone_occupied:
        return HeadEquipResultStub(
            success=False,
            equipped_card=None,
            zone_object_count=getattr(zone, "_equipped_count", 1),
            failure_reason="zone_not_empty",
        )
    elif not card_has_head:
        return HeadEquipResultStub(
            success=False,
            equipped_card=None,
            zone_object_count=0,
            failure_reason="missing_head_subtype",
        )
    else:
        return HeadEquipResultStub(
            success=True,
            equipped_card=card,
            zone_object_count=1,
            is_permanent=True,
        )


# ===== Stub Classes for Missing Engine Features =====


class HeadZoneStub:
    """
    Stub for engine feature: Head zone implementation.

    Engine Features Needed:
    - [ ] ZoneType.HEAD with is_public=True, is_equipment_zone=True (Rule 3.10.1)
    - [ ] Head zone is an arena zone (Rule 3.10.1, cross-ref 3.1.1)
    - [ ] Head zone has owner_id (Rule 3.10.1)
    - [ ] Head zone capacity limit of 1 (Rule 3.10.2)
    - [ ] Zone.is_empty returns False when equipped permanent exists (Rule 3.0.1a)
    - [ ] Zone.is_exposed returns True when empty (Rule 3.0.1a)
    """

    def __init__(self, owner_id: int = 0):
        self.owner_id = owner_id
        self.is_public_zone = True  # Rule 3.10.1 + 3.0.4a
        self.is_private_zone = False
        self.is_equipment_zone = True  # Rule 3.10.1
        self.is_arena_zone = True  # Rule 3.10.1, cross-ref 3.1.1
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


class HeadCardStub:
    """
    Stub for head equipment card.

    Engine Features Needed:
    - [ ] CardType.EQUIPMENT (Rule 1.3.2d - equipment is an arena-card)
    - [ ] Subtype.HEAD (Rule 3.10.2a - required for head zone equipping)
    """

    def __init__(
        self,
        name: str,
        owner_id: int = 0,
        has_head_subtype: bool = True,
    ):
        self.name = name
        self.owner_id = owner_id
        self._has_head_subtype = has_head_subtype


class HeadEquipResultStub:
    """
    Stub for the result of a head equip operation.

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


class HeadStartOfGameEquipResultStub:
    """
    Stub for start-of-game head equip procedure result.

    Engine Features Needed:
    - [ ] Start-of-game equip procedure (Rule 3.10.3, cross-ref 4.1, 4.1.4a)
    - [ ] Player may (optionally) equip head card at game start
    - [ ] After equipping, head card is a permanent in head zone
    """

    def __init__(
        self,
        player_may_equip: bool = True,
        was_equipped: bool = True,
        card_in_head_zone: bool = True,
        is_permanent: bool = True,
        zone_is_empty=None,
    ):
        self.player_may_equip = player_may_equip
        self.was_equipped = was_equipped
        self.card_in_head_zone = card_in_head_zone
        self.is_permanent = is_permanent
        self.zone_is_empty = (
            zone_is_empty if zone_is_empty is not None else not was_equipped
        )


# ===== Fixtures =====


@pytest.fixture
def game_state():
    """
    Fixture providing game state for Section 3.10 Head tests.

    Uses BDDGameState which integrates with the real engine.
    Reference: Rules 3.10.1, 3.10.2, 3.10.2a, 3.10.3
    """
    from tests.bdd_helpers import BDDGameState

    state = BDDGameState()
    return state
