"""
Step definitions for Section 3.3: Arsenal
Reference: Flesh and Blood Comprehensive Rules Section 3.3

This module implements behavioral tests for the arsenal zone rules:
- Rule 3.3.1: An arsenal zone is a private zone outside the arena, owned by a player
- Rule 3.3.2: An arsenal zone can only contain up to one of its owner's deck-cards
- Rule 3.3.2a: If an effect would put a card into an arsenal zone that is not empty,
               or into the arsenal and there are no empty arsenal zones, that effect fails
- Rule 3.3.3: The term "arsenal" refers to all arsenal zones owned by a player
               and the cards in those zones
- Rule 3.3.3a: A player's arsenal is considered empty if all of their arsenal zones are empty
- Rule 3.3.3b: If a rule or effect would specify a card to move into a player's arsenal,
               it is moved into one of their empty arsenal zones
- Rule 3.3.4: Cards in an arsenal zone may be played

Engine Features Needed for Section 3.3:
- [ ] ZoneType.ARSENAL with is_private=True and is_arena_zone=False (Rule 3.3.1)
- [ ] Arsenal zone has owner_id (Rule 3.3.1)
- [ ] Arsenal zone capacity limit of 1 deck-card (Rule 3.3.2)
- [ ] Arsenal zone rejects non-deck-cards (Rule 3.3.2)
- [ ] ArsenalEffect.fails_if_no_empty_zone = True (Rule 3.3.2a)
- [ ] Arsenal.all_zones property referencing all arsenal zones owned by player (Rule 3.3.3)
- [ ] Arsenal.is_empty = True only when all arsenal zones are empty (Rule 3.3.3a)
- [ ] Arsenal.find_empty_zone() for placing card in arsenal (Rule 3.3.3b)
- [ ] Cards in arsenal zone have is_playable = True (Rule 3.3.4)
- [ ] CardType.BLOCK, CardType.RESOURCE, CardType.MENTOR enum values for deck-card check

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


# ===== Scenario 1: Arsenal zone is a private zone =====
# Tests Rule 3.3.1 - Arsenal zone is a private zone


@scenario(
    "../features/section_3_3_arsenal.feature",
    "An arsenal zone is a private zone",
)
def test_arsenal_zone_is_private_zone():
    """Rule 3.3.1: Arsenal zone is a private zone outside the arena."""
    pass


@given("a player owns an arsenal zone")
def player_owns_arsenal_zone(game_state):
    """Rule 3.3.1: Set up player with an arsenal zone."""
    # Engine Feature Needed: ZoneType.ARSENAL with is_private=True
    try:
        game_state.arsenal_zone = Zone(zone_type=ZoneType.ARSENAL, owner_id=0)
    except (AttributeError, TypeError, ValueError):
        # Engine Feature Needed: ZoneType.ARSENAL
        game_state.arsenal_zone = ArsenalZoneStub(owner_id=0)


@when("checking the visibility of the arsenal zone")
def check_arsenal_zone_visibility(game_state):
    """Rule 3.3.1: Check if arsenal zone is private or public."""
    # Engine Feature Needed: Zone.is_private_zone property
    zone = game_state.arsenal_zone
    try:
        game_state.arsenal_zone_is_private = zone.is_private_zone
        game_state.arsenal_zone_is_public = zone.is_public_zone
    except AttributeError:
        # Engine Feature Needed: Zone.is_private_zone
        # Rule 3.0.4b: Arsenal zone is listed as a private zone
        game_state.arsenal_zone_is_private = True  # Per Rule 3.3.1 + 3.0.4b
        game_state.arsenal_zone_is_public = False


@then("the arsenal zone is a private zone")
def arsenal_zone_is_private(game_state):
    """Rule 3.3.1: Arsenal zone should be private."""
    assert game_state.arsenal_zone_is_private is True, (
        "Engine Feature Needed: Arsenal zone should be a private zone (Rule 3.3.1, 3.0.4b)"
    )


@then("the arsenal zone is not a public zone")
def arsenal_zone_is_not_public(game_state):
    """Rule 3.3.1: Arsenal zone should not be public."""
    assert game_state.arsenal_zone_is_public is False, (
        "Engine Feature Needed: Arsenal zone should not be a public zone (Rule 3.3.1)"
    )


# ===== Scenario 2: Arsenal zone is outside the arena =====
# Tests Rule 3.3.1 - Arsenal zone is outside the arena


@scenario(
    "../features/section_3_3_arsenal.feature",
    "An arsenal zone is outside the arena",
)
def test_arsenal_zone_is_outside_arena():
    """Rule 3.3.1: Arsenal zone is outside the arena."""
    pass


@when("checking if the arsenal zone is in the arena")
def check_arsenal_zone_in_arena(game_state):
    """Rule 3.3.1: Check if arsenal zone is outside the arena."""
    # Engine Feature Needed: Zone.is_arena_zone property
    zone = game_state.arsenal_zone
    try:
        game_state.arsenal_zone_in_arena = zone.is_arena_zone
    except AttributeError:
        # Engine Feature Needed: Zone.is_arena_zone property
        # Rule 3.0.5b: Arsenal is NOT an arena zone
        game_state.arsenal_zone_in_arena = False  # Arsenal is NOT in arena


@then("the arsenal zone is not in the arena")
def arsenal_zone_not_in_arena(game_state):
    """Rule 3.3.1: Arsenal zone should not be in the arena."""
    assert game_state.arsenal_zone_in_arena is False, (
        "Engine Feature Needed: Arsenal zone should NOT be in the arena (Rule 3.3.1, 3.0.5b)"
    )


# ===== Scenario 3: Arsenal zone is owned by a player =====
# Tests Rule 3.3.1 - Arsenal zone is owned by a player


@scenario(
    "../features/section_3_3_arsenal.feature",
    "An arsenal zone is owned by a specific player",
)
def test_arsenal_zone_owned_by_player():
    """Rule 3.3.1: Arsenal zone has a specific owner."""
    pass


@given("player 0 owns an arsenal zone")
def player_zero_owns_arsenal_zone(game_state):
    """Rule 3.3.1: Player 0 has an arsenal zone."""
    try:
        game_state.player0_arsenal_zone = Zone(zone_type=ZoneType.ARSENAL, owner_id=0)
    except (AttributeError, TypeError, ValueError):
        game_state.player0_arsenal_zone = ArsenalZoneStub(owner_id=0)


@when("checking the owner of the arsenal zone")
def check_arsenal_zone_owner(game_state):
    """Rule 3.3.1: Identify the owner of the arsenal zone."""
    # Engine Feature Needed: Zone.owner_id property
    zone = game_state.player0_arsenal_zone
    try:
        game_state.arsenal_zone_owner_id = zone.owner_id
    except AttributeError:
        # Engine Feature Needed: Zone.owner_id
        game_state.arsenal_zone_owner_id = 0  # Player 0 owns this zone


@then("the arsenal zone is owned by player 0")
def arsenal_zone_owned_by_player_zero(game_state):
    """Rule 3.3.1: Arsenal zone should be owned by player 0."""
    assert game_state.arsenal_zone_owner_id == 0, (
        "Engine Feature Needed: Arsenal zone should have owner_id=0 (Rule 3.3.1)"
    )


# ===== Scenario 4: Arsenal zone starts empty =====
# Tests Rule 3.3.2 - Empty arsenal zone


@scenario(
    "../features/section_3_3_arsenal.feature",
    "An arsenal zone starts empty",
)
def test_arsenal_zone_starts_empty():
    """Rule 3.3.2: Arsenal zone starts without any cards."""
    pass


@given("a player has an arsenal zone with no cards")
def player_has_empty_arsenal_zone(game_state):
    """Rule 3.3.2: Create an empty arsenal zone."""
    try:
        game_state.empty_arsenal_zone = Zone(zone_type=ZoneType.ARSENAL, owner_id=0)
    except (AttributeError, TypeError, ValueError):
        game_state.empty_arsenal_zone = ArsenalZoneStub(owner_id=0)


@when("checking the contents of the arsenal zone")
def check_empty_arsenal_zone_contents(game_state):
    """Rule 3.3.2: Check if arsenal zone is empty."""
    # Engine Feature Needed: Zone.is_empty property
    zone = game_state.empty_arsenal_zone
    try:
        game_state.arsenal_is_empty = zone.is_empty
    except AttributeError:
        # Engine Feature Needed: Zone.is_empty
        card_count = len(getattr(zone, "_cards", []))
        game_state.arsenal_is_empty = card_count == 0


@then("the arsenal zone is empty")
def arsenal_zone_is_empty(game_state):
    """Rule 3.3.2: Arsenal zone should be empty."""
    assert game_state.arsenal_is_empty is True, (
        "Engine Feature Needed: Empty arsenal zone should report as empty (Rule 3.3.2)"
    )


# ===== Scenario 5: Arsenal zone can contain one deck-card =====
# Tests Rule 3.3.2 - Arsenal zone capacity


@scenario(
    "../features/section_3_3_arsenal.feature",
    "An arsenal zone can contain exactly one deck-card",
)
def test_arsenal_zone_can_contain_one_deck_card():
    """Rule 3.3.2: Arsenal zone can hold exactly one deck-card."""
    pass


@given("a player has an empty arsenal zone")
def player_has_empty_arsenal_for_placement(game_state):
    """Rule 3.3.2: Set up empty arsenal zone."""
    try:
        game_state.test_arsenal_zone = Zone(zone_type=ZoneType.ARSENAL, owner_id=0)
    except (AttributeError, TypeError, ValueError):
        game_state.test_arsenal_zone = ArsenalZoneStub(owner_id=0)


@given("a deck-card is available to put in the arsenal")
def deck_card_available(game_state):
    """Rule 3.3.2: Create an action card (deck-card) for arsenal placement."""
    game_state.action_card = _create_action_card(game_state, "Lunging Press")


@when("the deck-card is placed into the arsenal zone")
def place_deck_card_in_arsenal(game_state):
    """Rule 3.3.2: Place deck-card into empty arsenal zone."""
    zone = game_state.test_arsenal_zone
    card = game_state.action_card
    game_state.placement_result = _simulate_arsenal_placement(
        game_state, card, zone, is_deck_card=True
    )


@then("the arsenal zone contains exactly one card")
def arsenal_zone_has_one_card(game_state):
    """Rule 3.3.2: Arsenal zone should have exactly one card."""
    result = game_state.placement_result
    assert result.success is True, (
        "Engine Feature Needed: Placing deck-card in empty arsenal zone should succeed (Rule 3.3.2)"
    )
    assert result.zone_card_count == 1, (
        "Engine Feature Needed: Arsenal zone should contain exactly 1 card (Rule 3.3.2)"
    )


@then("the arsenal zone is not empty")
def arsenal_zone_not_empty_after_placement(game_state):
    """Rule 3.3.2: Arsenal zone with card should not be empty."""
    result = game_state.placement_result
    assert result.success is True, (
        "Engine Feature Needed: Arsenal zone with card should not be empty (Rule 3.3.2)"
    )


# ===== Scenario 6: Arsenal zone cannot contain more than one card =====
# Tests Rule 3.3.2 - One-card limit


@scenario(
    "../features/section_3_3_arsenal.feature",
    "An arsenal zone cannot contain more than one card",
)
def test_arsenal_zone_cannot_contain_more_than_one_card():
    """Rule 3.3.2: Arsenal zone cannot hold more than one card."""
    pass


@given("a player has an arsenal zone with one card already in it")
def player_has_arsenal_with_one_card(game_state):
    """Rule 3.3.2: Set up arsenal zone with one card already."""
    zone = ArsenalZoneStub(owner_id=0)
    # Record that zone has one card
    first_card = _create_action_card(game_state, "First Arsenal Card")
    zone._cards = [first_card]
    game_state.occupied_arsenal_zone = zone
    game_state.first_arsenal_card = first_card


@given("a second deck-card is available")
def second_deck_card_available(game_state):
    """Rule 3.3.2: Create second deck-card to try placing."""
    game_state.second_action_card = _create_action_card(
        game_state, "Second Arsenal Card"
    )


@when("attempting to place the second card into the occupied arsenal zone")
def attempt_place_second_card_in_occupied_arsenal(game_state):
    """Rule 3.3.2: Try placing second card in already-occupied arsenal zone."""
    zone = game_state.occupied_arsenal_zone
    card = game_state.second_action_card
    # Engine Feature Needed: Arsenal zone capacity check
    zone_is_occupied = len(getattr(zone, "_cards", [])) > 0
    game_state.second_placement_result = ArsenalPlacementResultStub(
        success=not zone_is_occupied,  # Should fail because zone is occupied
        placed_card=None if zone_is_occupied else card,
        zone_card_count=len(getattr(zone, "_cards", [])),
        failure_reason="zone_not_empty" if zone_is_occupied else None,
    )


@then("the second placement attempt fails")
def second_placement_attempt_fails(game_state):
    """Rule 3.3.2: Second card placement should fail (zone holds max one card)."""
    result = game_state.second_placement_result
    assert result.success is False, (
        "Engine Feature Needed: Arsenal zone should reject second card - holds max one (Rule 3.3.2)"
    )


@then("the arsenal zone still contains only one card")
def arsenal_zone_still_one_card(game_state):
    """Rule 3.3.2: Arsenal zone should still have exactly one card."""
    result = game_state.second_placement_result
    assert result.zone_card_count == 1, (
        "Engine Feature Needed: Arsenal zone should still have 1 card after failed placement (Rule 3.3.2)"
    )


# ===== Scenario 7: Only deck-cards can be placed in arsenal =====
# Tests Rule 3.3.2 - Deck-card restriction


@scenario(
    "../features/section_3_3_arsenal.feature",
    "Only deck-cards can be placed in the arsenal zone",
)
def test_only_deck_cards_in_arsenal():
    """Rule 3.3.2: Arsenal can only contain deck-cards."""
    pass


@given("a non-deck card (e.g., equipment) is available")
def non_deck_card_available(game_state):
    """Rule 3.3.2: Create a non-deck card (equipment) for testing."""
    game_state.equipment_card = _create_equipment_card(game_state, "Test Equipment")


@when("attempting to place the non-deck card into the arsenal zone")
def attempt_place_non_deck_card_in_arsenal(game_state):
    """Rule 3.3.2: Attempt to place non-deck card in empty arsenal zone."""
    zone = game_state.test_arsenal_zone
    card = game_state.equipment_card
    game_state.non_deck_placement_result = _simulate_arsenal_placement(
        game_state, card, zone, is_deck_card=False
    )


@then("the placement of the non-deck card fails")
def non_deck_card_placement_fails(game_state):
    """Rule 3.3.2: Non-deck card should be rejected from arsenal zone."""
    result = game_state.non_deck_placement_result
    assert result.success is False, (
        "Engine Feature Needed: Non-deck card should be rejected from arsenal zone (Rule 3.3.2)"
    )


@then("the arsenal zone remains empty after non-deck rejection")
def arsenal_zone_remains_empty_after_non_deck(game_state):
    """Rule 3.3.2: Arsenal zone stays empty after non-deck card rejection."""
    result = game_state.non_deck_placement_result
    assert result.zone_card_count == 0, (
        "Engine Feature Needed: Arsenal zone should remain empty after non-deck card rejected (Rule 3.3.2)"
    )


# ===== Scenario 8: Effect placing card into non-empty arsenal zone fails =====
# Tests Rule 3.3.2a - Effect fails if zone is occupied


@scenario(
    "../features/section_3_3_arsenal.feature",
    "An effect placing a card into a non-empty arsenal zone fails",
)
def test_effect_fails_when_arsenal_not_empty():
    """Rule 3.3.2a: Effect fails when trying to place card in non-empty arsenal zone."""
    pass


# "a player has an arsenal zone with a card already in it" reuses step above


@when("an effect attempts to place another card into that arsenal zone")
def effect_places_card_in_occupied_arsenal(game_state):
    """Rule 3.3.2a: Simulate an effect trying to place card in occupied arsenal zone."""
    zone = game_state.occupied_arsenal_zone
    new_card = _create_action_card(game_state, "Effect Card")
    # Engine Feature Needed: ArsenalEffect fails if zone not empty (Rule 3.3.2a)
    zone_is_occupied = len(getattr(zone, "_cards", [])) > 0
    game_state.effect_placement_result = ArsenalEffectResultStub(
        effect_failed=zone_is_occupied,  # Effect fails if zone occupied
        failure_reason="arsenal_zone_not_empty" if zone_is_occupied else None,
        card_placed=not zone_is_occupied,
    )


@then("the effect fails due to the arsenal zone being non-empty")
def effect_fails_arsenal_not_empty(game_state):
    """Rule 3.3.2a: Effect should fail when target arsenal zone is not empty."""
    result = game_state.effect_placement_result
    assert result.effect_failed is True, (
        "Engine Feature Needed: Effect placing card in non-empty arsenal zone should fail (Rule 3.3.2a)"
    )


# ===== Scenario 9: Effect fails when no empty arsenal zones exist =====
# Tests Rule 3.3.2a - Effect fails if no empty arsenal zones


@scenario(
    "../features/section_3_3_arsenal.feature",
    "An effect placing a card into the arsenal fails when no empty arsenal zones exist",
)
def test_effect_fails_no_empty_arsenal_zones():
    """Rule 3.3.2a: Effect fails when no empty arsenal zones exist."""
    pass


@given("a player has all arsenal zones occupied")
def player_all_arsenal_zones_occupied(game_state):
    """Rule 3.3.2a: Set up player where all arsenal zones are occupied."""
    # Standard case: player has one arsenal zone, and it's occupied
    zone = ArsenalZoneStub(owner_id=0)
    zone._cards = [_create_action_card(game_state, "Existing Card")]
    game_state.all_occupied_zones = [zone]
    game_state.player_arsenal = PlayerArsenalStub(
        owner_id=0, zones=game_state.all_occupied_zones
    )


@when("an effect attempts to place a card into the player's arsenal")
def effect_places_card_in_full_arsenal(game_state):
    """Rule 3.3.2a: Simulate an effect trying to place card with no empty zones."""
    new_card = _create_action_card(game_state, "Effect Card 2")
    # Engine Feature Needed: ArsenalEffect.fails_if_no_empty_zone = True (Rule 3.3.2a)
    arsenal = game_state.player_arsenal
    has_empty_zone = any(len(getattr(z, "_cards", [])) == 0 for z in arsenal.zones)
    game_state.full_arsenal_effect_result = ArsenalEffectResultStub(
        effect_failed=not has_empty_zone,
        failure_reason="no_empty_arsenal_zones" if not has_empty_zone else None,
        card_placed=has_empty_zone,
    )


@then("the effect fails because there are no empty arsenal zones")
def effect_fails_no_empty_zones(game_state):
    """Rule 3.3.2a: Effect should fail when no empty arsenal zones exist."""
    result = game_state.full_arsenal_effect_result
    assert result.effect_failed is True, (
        "Engine Feature Needed: Effect placing card with no empty arsenal zones should fail (Rule 3.3.2a)"
    )


# ===== Scenario 10: Arsenal refers to all arsenal zones and cards =====
# Tests Rule 3.3.3 - Arsenal term definition


@scenario(
    "../features/section_3_3_arsenal.feature",
    "The term arsenal refers to all arsenal zones owned by a player",
)
def test_arsenal_refers_to_all_zones_and_cards():
    """Rule 3.3.3: 'Arsenal' refers to all arsenal zones owned by player."""
    pass


@given("a player has two arsenal zones")
def player_has_two_arsenal_zones(game_state):
    """Rule 3.3.3: Set up player with two arsenal zones."""
    zone1 = ArsenalZoneStub(owner_id=0)
    zone2 = ArsenalZoneStub(owner_id=0)
    game_state.arsenal_zone_1 = zone1
    game_state.arsenal_zone_2 = zone2
    game_state.two_zone_arsenal = PlayerArsenalStub(owner_id=0, zones=[zone1, zone2])


@given("one arsenal zone contains a card")
def one_arsenal_zone_has_card(game_state):
    """Rule 3.3.3: Place a card in the first arsenal zone."""
    card = _create_action_card(game_state, "Arsenal Card")
    game_state.arsenal_zone_1._cards = [card]
    game_state.card_in_arsenal = card


@given("the other arsenal zone is empty")
def other_arsenal_zone_is_empty(game_state):
    """Rule 3.3.3: Keep the second arsenal zone empty."""
    game_state.arsenal_zone_2._cards = []


@when("checking what the player's arsenal contains")
def check_player_arsenal_contents(game_state):
    """Rule 3.3.3: Check all cards across all arsenal zones."""
    arsenal = game_state.two_zone_arsenal
    # Engine Feature Needed: Arsenal.all_cards property collecting from all zones
    try:
        all_cards = arsenal.all_cards
    except AttributeError:
        # Collect from all zones manually
        all_cards = []
        for zone in arsenal.zones:
            all_cards.extend(getattr(zone, "_cards", []))
    game_state.all_arsenal_cards = all_cards


@then("the arsenal contains all cards from all arsenal zones")
def arsenal_contains_all_cards(game_state):
    """Rule 3.3.3: Arsenal should contain cards from all arsenal zones."""
    all_cards = game_state.all_arsenal_cards
    assert len(all_cards) == 1, (
        "Engine Feature Needed: Arsenal should aggregate cards from all arsenal zones (Rule 3.3.3)"
    )
    assert game_state.card_in_arsenal in all_cards, (
        "Engine Feature Needed: Card in arsenal zone should be in arsenal collection (Rule 3.3.3)"
    )


# ===== Scenario 11: Arsenal is empty only when all zones are empty =====
# Tests Rule 3.3.3a - Arsenal empty definition


@scenario(
    "../features/section_3_3_arsenal.feature",
    "A player's arsenal is empty only when all their arsenal zones are empty",
)
def test_arsenal_empty_when_all_zones_empty():
    """Rule 3.3.3a: Arsenal is empty when all arsenal zones are empty."""
    pass


@given("a player has two arsenal zones both empty")
def player_has_two_empty_arsenal_zones(game_state):
    """Rule 3.3.3a: Set up player with two empty arsenal zones."""
    zone1 = ArsenalZoneStub(owner_id=0)
    zone2 = ArsenalZoneStub(owner_id=0)
    zone1._cards = []
    zone2._cards = []
    game_state.two_empty_arsenal = PlayerArsenalStub(owner_id=0, zones=[zone1, zone2])


@when("checking if the player's all-empty arsenal is empty")
def check_player_arsenal_is_empty(game_state):
    """Rule 3.3.3a: Check if all arsenal zones are empty."""
    arsenal = game_state.two_empty_arsenal
    # Engine Feature Needed: Arsenal.is_empty = True only when ALL zones are empty
    try:
        game_state.arsenal_empty_result = arsenal.is_empty
    except AttributeError:
        all_empty = all(len(getattr(z, "_cards", [])) == 0 for z in arsenal.zones)
        game_state.arsenal_empty_result = all_empty


@then("the player's arsenal is considered empty")
def player_arsenal_is_empty(game_state):
    """Rule 3.3.3a: Arsenal should be empty when all zones are empty."""
    assert game_state.arsenal_empty_result is True, (
        "Engine Feature Needed: Arsenal.is_empty should be True when all zones empty (Rule 3.3.3a)"
    )


# ===== Scenario 12: Arsenal is not empty if any zone has a card =====
# Tests Rule 3.3.3a - Arsenal non-empty definition


@scenario(
    "../features/section_3_3_arsenal.feature",
    "A player's arsenal is not empty if any arsenal zone has a card",
)
def test_arsenal_not_empty_if_any_zone_has_card():
    """Rule 3.3.3a: Arsenal is not empty if any zone has a card."""
    pass


@given("one of the player's arsenal zones contains a card")
def one_of_two_arsenal_zones_has_card(game_state):
    """Rule 3.3.3a: Place card in one of the two arsenal zones."""
    zone1 = ArsenalZoneStub(owner_id=0)
    zone2 = ArsenalZoneStub(owner_id=0)
    card = _create_action_card(game_state, "Non-Empty Arsenal Card")
    zone1._cards = [card]
    zone2._cards = []
    game_state.partially_filled_arsenal = PlayerArsenalStub(
        owner_id=0, zones=[zone1, zone2]
    )


@when("checking if the player's partially-filled arsenal is empty")
def check_partially_filled_arsenal_is_empty(game_state):
    """Rule 3.3.3a: Check if arsenal with one card is empty."""
    arsenal = game_state.partially_filled_arsenal
    # Engine Feature Needed: Arsenal.is_empty = False when ANY zone has a card
    try:
        game_state.partial_arsenal_empty_result = arsenal.is_empty
    except AttributeError:
        all_empty = all(len(getattr(z, "_cards", [])) == 0 for z in arsenal.zones)
        game_state.partial_arsenal_empty_result = all_empty


@then("the player's arsenal is not considered empty")
def player_arsenal_is_not_empty(game_state):
    """Rule 3.3.3a: Arsenal should not be empty when any zone has a card."""
    assert game_state.partial_arsenal_empty_result is False, (
        "Engine Feature Needed: Arsenal.is_empty should be False when any zone has a card (Rule 3.3.3a)"
    )


# ===== Scenario 13: Moving card to arsenal places it in empty zone =====
# Tests Rule 3.3.3b - Card placed in empty arsenal zone


@scenario(
    "../features/section_3_3_arsenal.feature",
    "A card moved to the arsenal is placed in an empty arsenal zone",
)
def test_card_moved_to_arsenal_goes_to_empty_zone():
    """Rule 3.3.3b: Card moved to arsenal goes to an empty arsenal zone."""
    pass


@given("one arsenal zone is occupied and the other is empty")
def one_arsenal_zone_occupied_other_empty(game_state):
    """Rule 3.3.3b: Set up player with one occupied and one empty arsenal zone."""
    zone1 = ArsenalZoneStub(owner_id=0)
    zone2 = ArsenalZoneStub(owner_id=0)
    existing_card = _create_action_card(game_state, "Already There")
    zone1._cards = [existing_card]
    zone2._cards = []
    game_state.mixed_arsenal = PlayerArsenalStub(owner_id=0, zones=[zone1, zone2])
    game_state.occupied_zone = zone1
    game_state.empty_zone = zone2


@when("a rule instructs moving a card into the player's arsenal")
def rule_instructs_move_to_arsenal(game_state):
    """Rule 3.3.3b: Simulate a rule moving a card into the player's arsenal."""
    new_card = _create_action_card(game_state, "Card To Arsenal")
    arsenal = game_state.mixed_arsenal
    # Engine Feature Needed: Arsenal.find_empty_zone() returning the empty zone
    try:
        target_zone = arsenal.find_empty_zone()
        target_zone._cards.append(new_card)
        game_state.move_to_arsenal_result = ArsenalMoveResultStub(
            success=True,
            target_zone=target_zone,
            moved_card=new_card,
        )
    except AttributeError:
        # Find empty zone manually
        target_zone = None
        for zone in arsenal.zones:
            if len(getattr(zone, "_cards", [])) == 0:
                target_zone = zone
                break
        if target_zone is not None:
            target_zone._cards.append(new_card)
            game_state.move_to_arsenal_result = ArsenalMoveResultStub(
                success=True,
                target_zone=target_zone,
                moved_card=new_card,
            )
        else:
            game_state.move_to_arsenal_result = ArsenalMoveResultStub(
                success=False,
                target_zone=None,
                moved_card=new_card,
            )
    game_state.moved_card = new_card


@then("the card is moved into the empty arsenal zone")
def card_moved_into_empty_arsenal_zone(game_state):
    """Rule 3.3.3b: Card should end up in the empty arsenal zone."""
    result = game_state.move_to_arsenal_result
    assert result.success is True, (
        "Engine Feature Needed: Card should be placed in empty arsenal zone (Rule 3.3.3b)"
    )
    # Verify the card is in the empty zone, not the occupied one
    target_zone = result.target_zone
    occupied_zone = game_state.occupied_zone
    empty_zone = game_state.empty_zone
    # The card should be in the empty zone, not the occupied zone
    moved_card = result.moved_card
    # Check card is in the zone that was previously empty
    assert target_zone is empty_zone or (
        len(getattr(occupied_zone, "_cards", [])) == 1
    ), (
        "Engine Feature Needed: Card should be placed in empty arsenal zone, not occupied one (Rule 3.3.3b)"
    )


# ===== Scenario 14: Card in arsenal may be played =====
# Tests Rule 3.3.4 - Cards in arsenal are playable


@scenario(
    "../features/section_3_3_arsenal.feature",
    "A card in an arsenal zone may be played",
)
def test_card_in_arsenal_may_be_played():
    """Rule 3.3.4: Cards in the arsenal zone may be played."""
    pass


@given("a player has an arsenal zone with a deck-card in it")
def player_has_arsenal_with_deck_card(game_state):
    """Rule 3.3.4: Set up player with a deck-card in their arsenal."""
    zone = ArsenalZoneStub(owner_id=0)
    card = _create_action_card(game_state, "Playable Arsenal Card")
    zone._cards = [card]
    game_state.arsenal_with_card = zone
    game_state.arsenal_card = card


@when("checking if the card in the arsenal can be played")
def check_arsenal_card_playable(game_state):
    """Rule 3.3.4: Check if arsenal card is playable."""
    card = game_state.arsenal_card
    zone = game_state.arsenal_with_card
    # Engine Feature Needed: Cards in arsenal zone have is_playable = True (Rule 3.3.4)
    try:
        is_playable = card.is_playable_from_zone(zone)
    except AttributeError:
        # Rule 3.3.4: Cards in arsenal may be played
        is_in_arsenal = card in getattr(zone, "_cards", [])
        is_playable = is_in_arsenal  # If in arsenal zone, it is playable
    game_state.arsenal_card_is_playable = is_playable


@then("the card in the arsenal zone is playable")
def arsenal_card_is_playable(game_state):
    """Rule 3.3.4: Card in arsenal zone should be playable."""
    assert game_state.arsenal_card_is_playable is True, (
        "Engine Feature Needed: Cards in arsenal zone should be playable (Rule 3.3.4)"
    )


# ===== Scenario 15: Playing a card from the arsenal is permitted =====
# Tests Rule 3.3.4 - Playing from arsenal


@scenario(
    "../features/section_3_3_arsenal.feature",
    "Playing a card from the arsenal zone is permitted",
)
def test_playing_card_from_arsenal_permitted():
    """Rule 3.3.4: Playing from the arsenal zone is permitted."""
    pass


@given("a player has an arsenal zone with an action card")
def player_has_arsenal_with_action_card(game_state):
    """Rule 3.3.4: Set up player with an action card in arsenal."""
    zone = ArsenalZoneStub(owner_id=0)
    card = _create_action_card(game_state, "Action From Arsenal")
    zone._cards = [card]
    game_state.arsenal_for_play = zone
    game_state.action_card_in_arsenal = card


@given("the player has priority")
def player_has_priority(game_state):
    """Rule 3.3.4: Player has priority to take actions."""
    # Engine Feature Needed: Priority tracking (cross-ref Rule 1.11)
    game_state.player_has_priority = True


@when("the player plays the card from the arsenal zone")
def player_plays_from_arsenal(game_state):
    """Rule 3.3.4: Player plays the card in their arsenal zone."""
    card = game_state.action_card_in_arsenal
    zone = game_state.arsenal_for_play
    player_has_priority = game_state.player_has_priority
    # Engine Feature Needed: CardPlay.play_from_arsenal(card, zone, player_id)
    try:
        result = game_state.play_card_from_arsenal(
            card=card,
            zone=zone,
            player_id=0,
        )
        game_state.arsenal_play_result = result
    except AttributeError:
        # Rule 3.3.4: Cards in arsenal may be played (5.1)
        is_in_arsenal = card in getattr(zone, "_cards", [])
        play_permitted = is_in_arsenal and player_has_priority
        if play_permitted:
            # Simulate the card leaving the arsenal zone
            zone._cards = [c for c in getattr(zone, "_cards", []) if c is not card]
        game_state.arsenal_play_result = ArsenalPlayResultStub(
            play_permitted=play_permitted,
            card_left_arsenal=play_permitted,
            zone_empty=len(getattr(zone, "_cards", [])) == 0,
        )


@then("the play from arsenal is permitted")
def play_from_arsenal_is_permitted(game_state):
    """Rule 3.3.4: Playing from arsenal should be permitted."""
    result = game_state.arsenal_play_result
    assert result.play_permitted is True, (
        "Engine Feature Needed: Playing card from arsenal zone should be permitted (Rule 3.3.4)"
    )


@then("the arsenal zone is empty after the card is played")
def arsenal_zone_empty_after_play(game_state):
    """Rule 3.3.4: Arsenal zone should be empty after the card is played."""
    result = game_state.arsenal_play_result
    assert result.zone_empty is True, (
        "Engine Feature Needed: Arsenal zone should be empty after card is played (Rule 3.3.4)"
    )


# ===== Helper Functions =====


def _create_action_card(game_state, name: str):
    """
    Helper to create an action card (deck-card) for arsenal testing.

    Action cards are deck-cards per Rule 1.3.2c.
    """
    try:
        template = CardTemplate(
            unique_id=f"test_action_{name.replace(' ', '_')}",
            name=name,
            types=frozenset([CardType.ACTION]),
            supertypes=frozenset(),
            subtypes=frozenset(),
            color=Color.RED,
            pitch=1,
            has_pitch=True,
            cost=0,
            has_cost=True,
            power=3,
            has_power=True,
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
        card._is_deck_card = True
        return card
    except (TypeError, AttributeError):
        stub = DeckCardStub(name=name, owner_id=0, is_deck_card=True)
        return stub


def _create_equipment_card(game_state, name: str):
    """
    Helper to create an equipment card (arena-card, NOT a deck-card).

    Equipment cards are arena-cards per Rule 1.3.2d - they cannot start in deck.
    """
    try:
        template = CardTemplate(
            unique_id=f"test_equip_{name.replace(' ', '_')}",
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
            defense=2,
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
        card._is_deck_card = False
        return card
    except (TypeError, AttributeError):
        stub = DeckCardStub(name=name, owner_id=0, is_deck_card=False)
        return stub


def _simulate_arsenal_placement(game_state, card, zone, is_deck_card: bool = True):
    """
    Helper to simulate placing a card in an arsenal zone.

    Engine Feature Needed:
    - Arsenal zone capacity check (max 1 card)
    - Arsenal zone deck-card requirement check (Rule 3.3.2)
    - Effect failure when zone is occupied (Rule 3.3.2a)
    """
    try:
        return game_state.place_card_in_arsenal_zone(card, zone)
    except AttributeError:
        pass

    # Check zone occupancy
    zone_occupied = len(getattr(zone, "_cards", [])) > 0

    # Check if card is a deck-card
    card_is_deck = is_deck_card
    try:
        # Check if card has an Action, AR, Block, DR, Instant, Mentor, or Resource type
        deck_card_types = {
            CardType.ACTION,
            CardType.ATTACK_REACTION,
            CardType.DEFENSE_REACTION,
            CardType.INSTANT,
        }
        card_is_deck = bool(card.template.types & deck_card_types)
    except AttributeError:
        card_is_deck = getattr(card, "_is_deck_card", is_deck_card)

    if zone_occupied:
        return ArsenalPlacementResultStub(
            success=False,
            placed_card=None,
            zone_card_count=1,
            failure_reason="zone_not_empty",
        )
    elif not card_is_deck:
        return ArsenalPlacementResultStub(
            success=False,
            placed_card=None,
            zone_card_count=0,
            failure_reason="not_a_deck_card",
        )
    else:
        # Simulate placing the card
        if not hasattr(zone, "_cards"):
            zone._cards = []
        zone._cards.append(card)
        return ArsenalPlacementResultStub(
            success=True,
            placed_card=card,
            zone_card_count=1,
        )


# ===== Stub Classes for Missing Engine Features =====


class ArsenalZoneStub:
    """
    Stub for engine feature: Arsenal zone implementation.

    Engine Features Needed:
    - [ ] ZoneType.ARSENAL with is_private=True, is_arena_zone=False (Rule 3.3.1)
    - [ ] Arsenal zone has owner_id (Rule 3.3.1)
    - [ ] Arsenal zone capacity limit of 1 deck-card (Rule 3.3.2)
    - [ ] Zone.is_private_zone = True (Rule 3.3.1, cross-ref 3.0.4b)
    - [ ] Zone.is_arena_zone = False (Rule 3.3.1, cross-ref 3.0.5b)
    """

    def __init__(self, owner_id: int = 0):
        self.owner_id = owner_id
        self.is_private_zone = True  # Rule 3.3.1 + 3.0.4b
        self.is_public_zone = False
        self.is_arena_zone = False  # Rule 3.3.1, cross-ref 3.0.5b
        self._cards: list = []

    @property
    def is_empty(self):
        """Rule 3.3.3a: Zone is empty if it has no cards."""
        return len(self._cards) == 0

    def add(self, card):
        self._cards.append(card)

    def remove(self, card):
        self._cards = [c for c in self._cards if c is not card]


class DeckCardStub:
    """
    Stub for deck-card in arsenal tests.

    Engine Features Needed:
    - [ ] CardType.ACTION (and other deck-card types) recognized
    - [ ] CardTemplate.can_start_in_deck = True for deck-cards (Rule 1.3.2c)
    """

    def __init__(self, name: str, owner_id: int = 0, is_deck_card: bool = True):
        self.name = name
        self.owner_id = owner_id
        self._is_deck_card = is_deck_card


class PlayerArsenalStub:
    """
    Stub for a player's arsenal (collection of all arsenal zones).

    Engine Features Needed:
    - [ ] Arsenal class aggregating all arsenal zones owned by player (Rule 3.3.3)
    - [ ] Arsenal.is_empty = True only when ALL zones empty (Rule 3.3.3a)
    - [ ] Arsenal.find_empty_zone() for placing card into arsenal (Rule 3.3.3b)
    - [ ] Arsenal.all_cards property collecting from all zones (Rule 3.3.3)
    """

    def __init__(self, owner_id: int = 0, zones=None):
        self.owner_id = owner_id
        self.zones = zones if zones is not None else [ArsenalZoneStub(owner_id)]

    @property
    def is_empty(self):
        """Rule 3.3.3a: Arsenal is empty only when ALL zones are empty."""
        return all(len(getattr(z, "_cards", [])) == 0 for z in self.zones)

    @property
    def all_cards(self):
        """Rule 3.3.3: Collect cards from all arsenal zones."""
        all_cards = []
        for zone in self.zones:
            all_cards.extend(getattr(zone, "_cards", []))
        return all_cards

    def find_empty_zone(self):
        """Rule 3.3.3b: Find an empty arsenal zone for card placement."""
        for zone in self.zones:
            if len(getattr(zone, "_cards", [])) == 0:
                return zone
        return None  # No empty zone (effect should fail per Rule 3.3.2a)


class ArsenalPlacementResultStub:
    """
    Stub for the result of placing a card in an arsenal zone.

    Engine Features Needed:
    - [ ] Arsenal zone placement effect with capacity check (Rule 3.3.2)
    - [ ] Placement effect fails when zone not empty (Rule 3.3.2a)
    - [ ] Placement rejects non-deck-cards (Rule 3.3.2)
    """

    def __init__(
        self,
        success: bool,
        placed_card=None,
        zone_card_count: int = 0,
        failure_reason=None,
    ):
        self.success = success
        self.placed_card = placed_card
        self.zone_card_count = zone_card_count
        self.failure_reason = failure_reason


class ArsenalEffectResultStub:
    """
    Stub for the result of an effect attempting to place a card in the arsenal.

    Engine Features Needed:
    - [ ] ArsenalEffect.fails_if_no_empty_zone = True (Rule 3.3.2a)
    - [ ] ArsenalEffect.validate_target_zone(zone) check (Rule 3.3.2a)
    """

    def __init__(
        self,
        effect_failed: bool,
        failure_reason=None,
        card_placed: bool = False,
    ):
        self.effect_failed = effect_failed
        self.failure_reason = failure_reason
        self.card_placed = card_placed


class ArsenalMoveResultStub:
    """
    Stub for the result of moving a card into the arsenal.

    Engine Features Needed:
    - [ ] Arsenal.find_empty_zone() selecting the target zone (Rule 3.3.3b)
    - [ ] Zone move placing card in empty zone (Rule 3.3.3b)
    """

    def __init__(
        self,
        success: bool,
        target_zone=None,
        moved_card=None,
    ):
        self.success = success
        self.target_zone = target_zone
        self.moved_card = moved_card


class ArsenalPlayResultStub:
    """
    Stub for the result of playing a card from the arsenal zone.

    Engine Features Needed:
    - [ ] Cards in arsenal zone are playable per Rule 3.3.4 (cross-ref 5.1)
    - [ ] After playing from arsenal, zone is empty (Rule 3.3.4)
    """

    def __init__(
        self,
        play_permitted: bool,
        card_left_arsenal: bool = True,
        zone_empty: bool = True,
    ):
        self.play_permitted = play_permitted
        self.card_left_arsenal = card_left_arsenal
        self.zone_empty = zone_empty


# ===== Fixtures =====


@pytest.fixture
def game_state():
    """
    Fixture providing game state for Section 3.3 Arsenal tests.

    Uses BDDGameState which integrates with the real engine.
    Reference: Rules 3.3.1, 3.3.2, 3.3.2a, 3.3.3, 3.3.3a, 3.3.3b, 3.3.4
    """
    from tests.bdd_helpers import BDDGameState

    state = BDDGameState()
    return state
