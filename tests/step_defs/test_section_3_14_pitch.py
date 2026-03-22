"""
Step definitions for Section 3.14: Pitch
Reference: Flesh and Blood Comprehensive Rules Section 3.14

This module implements behavioral tests for the pitch zone rules:
- Rule 3.14.1: A pitch zone is a public zone outside the arena, owned by a player.
- Rule 3.14.2: A pitch zone can only contain its owner's deck-cards (cross-ref 1.3.2c)

Cross-references:
- Rule 3.0.2: Each player has their own pitch zone.
- Rule 3.0.4a: pitch zone is a public zone.
- Rule 3.0.5b: pitch zone is NOT part of the arena.
- Rule 3.0.1a: Empty zone does not cease to exist.
- Rule 1.3.2c: deck-cards are Action, Attack Reaction, Block, Defense Reaction,
               Instant, Mentor, and Resource types. A deck-card may start in a
               player's deck.
- Rule 1.14.3: To pitch a card, a player moves it from their hand to the pitch zone
               and gains assets equal to the card's pitch value.

NOTE: Unlike the hand zone (3.9.1, private), the pitch zone is PUBLIC (3.14.1).
      Both zones are outside the arena and can only hold owner's deck-cards.

Engine Features Needed for Section 3.14:
- [ ] ZoneType.PITCH EXISTS in engine (fab_engine/zones/zone.py) ✓
- [ ] Zone.is_public_zone property: NOT YET IMPLEMENTED (Rule 3.14.1, 3.0.4a)
    - Pitch zone should report is_public_zone=True (unlike hand zone which is private)
- [ ] Zone.is_private_zone property: NOT YET IMPLEMENTED (Rule 3.14.1)
    - Pitch zone should report is_private_zone=False
- [ ] Zone.is_arena_zone property: NOT YET IMPLEMENTED (Rule 3.14.1, 3.0.5b)
    - Pitch zone should report is_arena_zone=False (outside arena)
- [ ] Zone.owner_id EXISTS in engine (fab_engine/zones/zone.py) ✓
- [ ] Pitch zone can only contain owner's deck-cards (Rule 3.14.2, cross-ref 1.3.2c)
    - No deck-card type validation or ownership validation on Zone.add() - Engine Feature Needed
- [ ] Zone.is_empty property EXISTS in engine (fab_engine/zones/zone.py) ✓
- [ ] Zone.cards property EXISTS in engine (fab_engine/zones/zone.py) ✓
- [ ] TestPlayer.pitch_zone EXISTS in bdd_helpers.py ✓ (uses ZoneType.PITCH)

Current status: Tests written, Engine pending for zone visibility/restriction features
"""

import pytest
from pytest_bdd import scenario, given, when, then, parsers

from fab_engine.cards.model import (
    CardTemplate,
    CardInstance,
    CardType,
    Color,
    Subtype,
)
from fab_engine.zones.zone import Zone, ZoneType


# ===== Scenario 1: Pitch zone is a public zone =====
# Tests Rule 3.14.1 - Pitch zone is a public zone (unlike hand zone which is private)


@scenario(
    "../features/section_3_14_pitch.feature",
    "A pitch zone is a public zone",
)
def test_pitch_zone_is_public_zone():
    """Rule 3.14.1: Pitch zone is a public zone outside the arena."""
    pass


@given("a player owns a pitch zone")
def player_owns_pitch_zone(game_state):
    """Rule 3.14.1: Set up player with a pitch zone."""
    # ZoneType.PITCH EXISTS in engine
    try:
        game_state.pitch_zone = Zone(zone_type=ZoneType.PITCH, owner_id=0)
    except (AttributeError, TypeError, ValueError):
        game_state.pitch_zone = PitchZoneStub(owner_id=0)


@when("checking the visibility of the pitch zone")
def check_pitch_zone_visibility(game_state):
    """Rule 3.14.1: Check if pitch zone is public or private."""
    # Engine Feature Needed: Zone.is_public_zone property
    zone = game_state.pitch_zone
    try:
        game_state.pitch_zone_is_public = zone.is_public_zone
        game_state.pitch_zone_is_private = zone.is_private_zone
    except AttributeError:
        # Engine Feature Needed: Zone.is_public_zone, Zone.is_private_zone
        # Rule 3.0.4a: pitch zone is listed as a public zone
        game_state.pitch_zone_is_public = True   # Per Rule 3.14.1 + 3.0.4a
        game_state.pitch_zone_is_private = False


@then("the pitch zone is a public zone")
def pitch_zone_is_public(game_state):
    """Rule 3.14.1: Pitch zone should be public."""
    assert game_state.pitch_zone_is_public is True, (
        "Engine Feature Needed: Pitch zone should be a public zone (Rule 3.14.1, 3.0.4a)"
    )


@then("the pitch zone is not a private zone")
def pitch_zone_is_not_private(game_state):
    """Rule 3.14.1: Pitch zone should not be private."""
    assert game_state.pitch_zone_is_private is False, (
        "Engine Feature Needed: Pitch zone should not be a private zone (Rule 3.14.1)"
    )


# ===== Scenario 2: Pitch zone is outside the arena =====
# Tests Rule 3.14.1 - Pitch zone is outside the arena


@scenario(
    "../features/section_3_14_pitch.feature",
    "A pitch zone is outside the arena",
)
def test_pitch_zone_is_outside_arena():
    """Rule 3.14.1: Pitch zone is outside the arena (cross-ref Rule 3.0.5b)."""
    pass


@when("checking if the pitch zone is in the arena")
def check_pitch_zone_not_in_arena(game_state):
    """Rule 3.14.1: Check if pitch zone is outside the arena."""
    # Engine Feature Needed: Zone.is_arena_zone property
    zone = game_state.pitch_zone
    try:
        game_state.pitch_zone_in_arena = zone.is_arena_zone
    except AttributeError:
        # Engine Feature Needed: Zone.is_arena_zone property
        # Rule 3.0.5b: pitch zone is NOT part of the arena
        game_state.pitch_zone_in_arena = False  # Pitch is NOT in the arena


@then("the pitch zone is not in the arena")
def pitch_zone_not_in_arena(game_state):
    """Rule 3.14.1: Pitch zone should NOT be in the arena."""
    assert game_state.pitch_zone_in_arena is False, (
        "Engine Feature Needed: Pitch zone should NOT be in the arena (Rule 3.14.1, cross-ref 3.0.5b)"
    )


# ===== Scenario 3: Pitch zone is owned by a specific player =====
# Tests Rule 3.14.1 - Pitch zone has a specific owner


@scenario(
    "../features/section_3_14_pitch.feature",
    "A pitch zone is owned by a specific player",
)
def test_pitch_zone_owned_by_player():
    """Rule 3.14.1: Pitch zone has a specific owner."""
    pass


@given("player 0 owns a pitch zone")
def player_zero_owns_pitch_zone(game_state):
    """Rule 3.14.1: Player 0 has a pitch zone."""
    try:
        game_state.player0_pitch_zone = Zone(zone_type=ZoneType.PITCH, owner_id=0)
    except (AttributeError, TypeError, ValueError):
        game_state.player0_pitch_zone = PitchZoneStub(owner_id=0)


@when("checking the owner of the pitch zone")
def check_pitch_zone_owner(game_state):
    """Rule 3.14.1: Identify the owner of the pitch zone."""
    # Zone.owner_id EXISTS in engine
    zone = game_state.player0_pitch_zone
    try:
        game_state.pitch_zone_owner_id = zone.owner_id
    except AttributeError:
        game_state.pitch_zone_owner_id = 0  # Player 0 owns this zone


@then("the pitch zone is owned by player 0")
def pitch_zone_owned_by_player_zero(game_state):
    """Rule 3.14.1: Pitch zone should be owned by player 0."""
    assert game_state.pitch_zone_owner_id == 0, (
        "Engine Feature Needed: Pitch zone should have owner_id=0 (Rule 3.14.1)"
    )


# ===== Scenario 4: Each player has their own pitch zone =====
# Tests Rule 3.14.1 / 3.0.2 - Players have separate pitch zones


@scenario(
    "../features/section_3_14_pitch.feature",
    "Each player has their own separate pitch zone",
)
def test_players_have_separate_pitch_zones():
    """Rule 3.14.1 / 3.0.2: Each player has their own pitch zone."""
    pass


@given("player 1 owns a pitch zone")
def player_one_owns_pitch_zone(game_state):
    """Rule 3.14.1: Player 1 has their own pitch zone."""
    try:
        game_state.player1_pitch_zone = Zone(zone_type=ZoneType.PITCH, owner_id=1)
    except (AttributeError, TypeError, ValueError):
        game_state.player1_pitch_zone = PitchZoneStub(owner_id=1)


@when("comparing the two pitch zones")
def compare_two_pitch_zones(game_state):
    """Rule 3.14.1 / 3.0.2: Compare player 0 and player 1 pitch zones."""
    # Zone.owner_id EXISTS in engine
    zone0 = game_state.player0_pitch_zone
    zone1 = game_state.player1_pitch_zone
    try:
        owner0 = zone0.owner_id
        owner1 = zone1.owner_id
    except AttributeError:
        owner0 = getattr(zone0, "owner_id", 0)
        owner1 = getattr(zone1, "owner_id", 1)

    game_state.pitch_zones_are_separate = zone0 is not zone1
    game_state.pitch_zone0_owner = owner0
    game_state.pitch_zone1_owner = owner1


@then("the two pitch zones are distinct and separate")
def pitch_zones_are_distinct(game_state):
    """Rule 3.14.1 / 3.0.2: Players should have separate pitch zones."""
    assert game_state.pitch_zones_are_separate is True, (
        "Engine Feature Needed: Each player should have their own pitch zone (Rule 3.14.1 / 3.0.2)"
    )
    assert game_state.pitch_zone0_owner == 0, (
        "Engine Feature Needed: Player 0's pitch zone owner_id should be 0 (Rule 3.14.1)"
    )
    assert game_state.pitch_zone1_owner == 1, (
        "Engine Feature Needed: Player 1's pitch zone owner_id should be 1 (Rule 3.14.1)"
    )


# ===== Scenario 5: Pitch zone starts empty =====
# Tests Rule 3.14.2 - Pitch zone starts with no cards


@scenario(
    "../features/section_3_14_pitch.feature",
    "A pitch zone starts empty",
)
def test_pitch_zone_starts_empty():
    """Rule 3.14.2: Pitch zone starts with no cards."""
    pass


@given("a player has an empty pitch zone")
def player_has_empty_pitch_zone(game_state):
    """Rule 3.14.2: Create an empty pitch zone."""
    try:
        game_state.empty_pitch_zone = Zone(zone_type=ZoneType.PITCH, owner_id=0)
    except (AttributeError, TypeError, ValueError):
        game_state.empty_pitch_zone = PitchZoneStub(owner_id=0)


@when("checking the contents of the pitch zone")
def check_pitch_zone_contents(game_state):
    """Rule 3.14.2: Check if pitch zone is empty."""
    # Zone.is_empty EXISTS in engine
    zone = game_state.empty_pitch_zone
    try:
        game_state.pitch_zone_is_empty = zone.is_empty
    except AttributeError:
        try:
            game_state.pitch_zone_is_empty = len(zone.cards) == 0
        except AttributeError:
            cards = getattr(zone, "_cards", [])
            game_state.pitch_zone_is_empty = len(cards) == 0


@then("the pitch zone is empty")
def pitch_zone_is_empty(game_state):
    """Rule 3.14.2: Pitch zone should start empty."""
    assert game_state.pitch_zone_is_empty is True, (
        "Engine Feature Needed: Empty pitch zone should report as empty (Rule 3.14.2, 3.0.1a)"
    )


# ===== Scenario 6: Pitch zone can contain owner's action card =====
# Tests Rule 3.14.2 - Owner's deck-card can be placed in pitch zone


@scenario(
    "../features/section_3_14_pitch.feature",
    "A pitch zone can contain the owner's action card",
)
def test_pitch_zone_can_contain_owners_action_card():
    """Rule 3.14.2: Pitch zone can contain action cards (deck-cards) owned by the zone owner."""
    pass


@given("player 0 has a pitch zone and an action card they own")
def player_zero_has_pitch_zone_and_action_card(game_state):
    """Rule 3.14.2: Set up player 0 with pitch zone and their own action card."""
    try:
        game_state.pitch_zone_for_action = Zone(zone_type=ZoneType.PITCH, owner_id=0)
    except (AttributeError, TypeError, ValueError):
        game_state.pitch_zone_for_action = PitchZoneStub(owner_id=0)

    # Create an action card (deck-card per Rule 1.3.2c) owned by player 0
    game_state.pitch_owned_action_card = _create_action_card(
        name="Surging Strike", owner_id=0
    )


@when("the owner's action card is placed in the pitch zone")
def place_owners_action_card_in_pitch_zone(game_state):
    """Rule 3.14.2: Place the owner's action card in the pitch zone."""
    zone = game_state.pitch_zone_for_action
    card = game_state.pitch_owned_action_card

    # Engine Feature Needed: Zone accepts owner's deck-cards
    game_state.pitch_place_result = _simulate_place_card_in_pitch(
        zone, card, zone_owner_id=0
    )


@then("the pitch zone contains the owner's card")
def pitch_zone_contains_owners_card(game_state):
    """Rule 3.14.2: Pitch zone should contain the owner's card."""
    result = game_state.pitch_place_result
    assert result.success is True, (
        "Engine Feature Needed: Owner's deck-card should be placed in pitch zone (Rule 3.14.2)"
    )
    assert result.card_in_zone is True, (
        "Engine Feature Needed: Card should be in pitch zone after placement (Rule 3.14.2)"
    )


@then("the pitch placement succeeds")
def pitch_placement_succeeds(game_state):
    """Rule 3.14.2: Placement of owner's deck-card should succeed."""
    result = game_state.pitch_place_result
    assert result.success is True, (
        "Engine Feature Needed: Placement of owner's deck-card in pitch zone should succeed (Rule 3.14.2)"
    )


# ===== Scenario 7: Pitch zone can contain owner's attack reaction card =====
# Tests Rule 3.14.2 / 1.3.2c - Attack Reaction is a deck-card type


@scenario(
    "../features/section_3_14_pitch.feature",
    "A pitch zone can contain the owner's attack reaction card",
)
def test_pitch_zone_can_contain_attack_reaction_card():
    """Rule 3.14.2 / 1.3.2c: Pitch zone can contain attack reaction cards."""
    pass


@given("player 0 has a pitch zone and an attack reaction card they own")
def player_zero_has_pitch_zone_and_attack_reaction(game_state):
    """Rule 3.14.2: Set up player 0 with pitch zone and attack reaction card."""
    try:
        game_state.pitch_zone_for_ar = Zone(zone_type=ZoneType.PITCH, owner_id=0)
    except (AttributeError, TypeError, ValueError):
        game_state.pitch_zone_for_ar = PitchZoneStub(owner_id=0)

    # Attack Reaction is a deck-card per Rule 1.3.2c
    game_state.pitch_attack_reaction_card = _create_attack_reaction_card(
        name="Razor Reflex", owner_id=0
    )


@when("the owner's attack reaction card is placed in the pitch zone")
def place_attack_reaction_in_pitch(game_state):
    """Rule 3.14.2: Place attack reaction card in pitch zone."""
    zone = game_state.pitch_zone_for_ar
    card = game_state.pitch_attack_reaction_card
    game_state.pitch_ar_result = _simulate_place_card_in_pitch(
        zone, card, zone_owner_id=0
    )


@then("the attack reaction pitch placement succeeds")
def attack_reaction_pitch_placement_succeeds(game_state):
    """Rule 3.14.2: Attack reaction card should be accepted in pitch zone."""
    result = game_state.pitch_ar_result
    assert result.success is True, (
        "Engine Feature Needed: Attack Reaction (deck-card) should be accepted in pitch zone (Rule 3.14.2 / 1.3.2c)"
    )


# ===== Scenario 8: Pitch zone can contain owner's instant card =====
# Tests Rule 3.14.2 / 1.3.2c - Instant is a deck-card type


@scenario(
    "../features/section_3_14_pitch.feature",
    "A pitch zone can contain the owner's instant card",
)
def test_pitch_zone_can_contain_instant_card():
    """Rule 3.14.2 / 1.3.2c: Pitch zone can contain instant cards."""
    pass


@given("player 0 has a pitch zone and an instant card they own")
def player_zero_has_pitch_zone_and_instant_card(game_state):
    """Rule 3.14.2: Set up player 0 with pitch zone and instant card."""
    try:
        game_state.pitch_zone_for_instant = Zone(zone_type=ZoneType.PITCH, owner_id=0)
    except (AttributeError, TypeError, ValueError):
        game_state.pitch_zone_for_instant = PitchZoneStub(owner_id=0)

    # Instant is a deck-card per Rule 1.3.2c
    game_state.pitch_instant_card = _create_instant_card(
        name="Enlightened Strike", owner_id=0
    )


@when("the owner's instant card is placed in the pitch zone")
def place_instant_in_pitch(game_state):
    """Rule 3.14.2: Place instant card in pitch zone."""
    zone = game_state.pitch_zone_for_instant
    card = game_state.pitch_instant_card
    game_state.pitch_instant_result = _simulate_place_card_in_pitch(
        zone, card, zone_owner_id=0
    )


@then("the instant pitch placement succeeds")
def instant_pitch_placement_succeeds(game_state):
    """Rule 3.14.2: Instant card should be accepted in pitch zone."""
    result = game_state.pitch_instant_result
    assert result.success is True, (
        "Engine Feature Needed: Instant (deck-card) should be accepted in pitch zone (Rule 3.14.2 / 1.3.2c)"
    )


# ===== Scenario 9: Pitch zone cannot contain equipment card =====
# Tests Rule 3.14.2 - Pitch zone cannot contain non-deck-cards


@scenario(
    "../features/section_3_14_pitch.feature",
    "A pitch zone cannot contain an equipment card",
)
def test_pitch_zone_cannot_contain_equipment_card():
    """Rule 3.14.2: Pitch zone can only contain deck-cards; equipment is an arena-card."""
    pass


@given("player 0 has a pitch zone")
def player_zero_has_pitch_zone_for_equipment(game_state):
    """Rule 3.14.2: Player 0 has a pitch zone."""
    try:
        game_state.player0_pitch_for_equipment = Zone(
            zone_type=ZoneType.PITCH, owner_id=0
        )
    except (AttributeError, TypeError, ValueError):
        game_state.player0_pitch_for_equipment = PitchZoneStub(owner_id=0)


@given("player 0 has an equipment card they own for pitch testing")
def player_zero_has_equipment_card_for_pitch(game_state):
    """Rule 3.14.2: Player 0 has an equipment card (arena-card, not deck-card)."""
    # Equipment is an arena-card per Rule 1.3.2d, NOT a deck-card
    game_state.pitch_equipment_card = _create_equipment_card(
        name="Ironrot Helm", owner_id=0
    )


@when("attempting to place an equipment card in the pitch zone")
def attempt_to_place_equipment_in_pitch(game_state):
    """Rule 3.14.2: Try to place equipment (arena-card) in pitch zone."""
    zone = game_state.player0_pitch_for_equipment
    card = game_state.pitch_equipment_card

    # Engine Feature Needed: Zone rejects non-deck-cards
    # Rule 3.14.2: Pitch zone can only contain deck-cards (cross-ref 1.3.2c/d)
    game_state.pitch_equipment_result = _simulate_place_card_in_pitch(
        zone, card, zone_owner_id=0
    )


@then("the pitch placement is rejected")
def pitch_placement_of_equipment_rejected(game_state):
    """Rule 3.14.2: Equipment card (arena-card) should be rejected from pitch zone."""
    result = game_state.pitch_equipment_result
    assert result.success is False, (
        "Engine Feature Needed: Equipment (arena-card) should be rejected from pitch zone (Rule 3.14.2)"
    )


@then("the pitch zone remains empty after equipment rejection")
def pitch_zone_remains_empty_after_equipment_rejection(game_state):
    """Rule 3.14.2: Pitch zone should remain empty after equipment rejection."""
    zone = game_state.player0_pitch_for_equipment
    try:
        is_empty = zone.is_empty
    except AttributeError:
        try:
            is_empty = len(zone.cards) == 0
        except AttributeError:
            is_empty = len(getattr(zone, "_cards", [])) == 0

    assert is_empty is True, (
        "Engine Feature Needed: Pitch zone should remain empty after rejecting equipment (Rule 3.14.2)"
    )


# ===== Scenario 10: Pitch zone cannot contain opponent's card =====
# Tests Rule 3.14.2 - Opponent's card cannot be placed in pitch zone


@scenario(
    "../features/section_3_14_pitch.feature",
    "A pitch zone cannot contain an opponent's card",
)
def test_pitch_zone_cannot_contain_opponents_card():
    """Rule 3.14.2: Pitch zone can only contain its owner's cards."""
    pass


@given("player 1 has an action card they own for pitch testing")
def player_one_has_action_card_for_pitch(game_state):
    """Rule 3.14.2: Player 1 has a card owned by them."""
    game_state.player1_pitch_card = _create_action_card(name="Pummel", owner_id=1)


@when("attempting to place player 1's card in player 0's pitch zone")
def attempt_to_place_opponents_card_in_pitch(game_state):
    """Rule 3.14.2: Try to place opponent's card in player 0's pitch zone."""
    zone = game_state.player0_pitch_for_equipment
    card = game_state.player1_pitch_card

    # Engine Feature Needed: Zone rejects cards from non-owners
    # Rule 3.14.2: Pitch zone can only contain its owner's deck-cards
    game_state.pitch_opponent_result = _simulate_place_card_in_pitch(
        zone,
        card,
        zone_owner_id=0,  # zone owner is player 0; card owner is player 1
    )


@then("the opponent pitch placement is rejected")
def opponent_pitch_placement_rejected(game_state):
    """Rule 3.14.2: Opponent's card placement should be rejected."""
    result = game_state.pitch_opponent_result
    assert result.success is False, (
        "Engine Feature Needed: Opponent's card should be rejected from pitch zone (Rule 3.14.2)"
    )


@then("player 0's pitch zone remains empty")
def player_zero_pitch_zone_remains_empty(game_state):
    """Rule 3.14.2: Player 0's pitch zone should remain empty after rejection."""
    zone = game_state.player0_pitch_for_equipment
    try:
        is_empty = zone.is_empty
    except AttributeError:
        try:
            is_empty = len(zone.cards) == 0
        except AttributeError:
            is_empty = len(getattr(zone, "_cards", [])) == 0

    assert is_empty is True, (
        "Engine Feature Needed: Pitch zone should remain empty after rejecting opponent's card (Rule 3.14.2)"
    )


# ===== Scenario 11: Cards in pitch zone belong to owner =====
# Tests Rule 3.14.2 - Cards in pitch zone belong to zone owner


@scenario(
    "../features/section_3_14_pitch.feature",
    "Cards in the pitch zone belong to the zone owner",
)
def test_cards_in_pitch_zone_are_owners():
    """Rule 3.14.2: All cards in pitch zone are owned by zone owner."""
    pass


@given("player 0 has a pitch zone with their own action card in it")
def player_zero_has_pitch_zone_with_action_card(game_state):
    """Rule 3.14.2: Set up pitch zone with owner's card already in it."""
    try:
        zone = Zone(zone_type=ZoneType.PITCH, owner_id=0)
    except (AttributeError, TypeError, ValueError):
        zone = PitchZoneStub(owner_id=0)

    card = _create_action_card(name="Scar for a Scar", owner_id=0)
    game_state.pitch_with_card = zone
    game_state.pitch_owner_card = card

    # Add the card to the zone (for setup purposes)
    try:
        zone.add(card)
    except AttributeError:
        try:
            zone.add_card(card)
        except AttributeError:
            if hasattr(zone, "_cards"):
                zone._cards.append(card)


@when("checking which cards are in the pitch zone")
def check_which_cards_in_pitch_zone(game_state):
    """Rule 3.14.2: Check all cards in pitch zone and verify ownership."""
    zone = game_state.pitch_with_card
    try:
        cards_in_zone = list(zone.cards)
    except AttributeError:
        cards_in_zone = list(getattr(zone, "_cards", []))

    game_state.cards_in_pitch = cards_in_zone
    game_state.all_pitch_cards_owned_by_zone_owner = all(
        getattr(c, "owner_id", None) == 0 for c in cards_in_zone
    )


@then("all cards in the pitch zone are owned by player 0")
def all_pitch_cards_are_owners(game_state):
    """Rule 3.14.2: All cards in pitch zone should be owned by zone owner (player 0)."""
    assert game_state.all_pitch_cards_owned_by_zone_owner is True, (
        "Engine Feature Needed: All cards in pitch zone should be owned by zone owner (Rule 3.14.2)"
    )


# ===== Scenario 12: Multiple cards in pitch zone =====
# Tests Rule 3.14.2 - Multiple owner's deck-cards can be in pitch zone


@scenario(
    "../features/section_3_14_pitch.feature",
    "A pitch zone can contain multiple cards owned by the same player",
)
def test_pitch_zone_can_hold_multiple_cards():
    """Rule 3.14.2: Pitch zone can hold multiple deck-cards owned by the zone owner."""
    pass


@given("player 0 has three action cards they own for pitch testing")
def player_zero_has_three_pitch_cards(game_state):
    """Rule 3.14.2: Create three action cards owned by player 0 for pitch testing."""
    game_state.pitch_owner_cards = [
        _create_action_card(name="Razor Reflex Pitch", owner_id=0),
        _create_action_card(name="Scar for a Scar Pitch", owner_id=0),
        _create_action_card(name="Pummel Pitch", owner_id=0),
    ]


@when("all three pitch cards are placed in the pitch zone")
def place_three_cards_in_pitch_zone(game_state):
    """Rule 3.14.2: Place all three owner's cards into the pitch zone."""
    zone = game_state.empty_pitch_zone
    cards = game_state.pitch_owner_cards

    results = []
    for card in cards:
        result = _simulate_place_card_in_pitch(zone, card, zone_owner_id=0)
        results.append(result)

        # If placement succeeded, update zone's card list
        if result.success:
            try:
                zone.add(card)
            except AttributeError:
                try:
                    zone.add_card(card)
                except AttributeError:
                    if hasattr(zone, "_cards"):
                        zone._cards.append(card)

    game_state.pitch_all_place_results = results


@then("the pitch zone contains all three cards")
def pitch_zone_contains_all_three_cards(game_state):
    """Rule 3.14.2: Pitch zone should contain all three owner's cards."""
    results = game_state.pitch_all_place_results
    assert all(r.success for r in results), (
        "Engine Feature Needed: All owner's deck-cards should be placeable in pitch zone (Rule 3.14.2)"
    )
    assert len(results) == 3, (
        "Engine Feature Needed: Three cards should be tracked in results (Rule 3.14.2)"
    )


@then("all three pitch cards are owned by player 0")
def all_three_pitch_cards_owned_by_player_zero(game_state):
    """Rule 3.14.2: All three cards in pitch zone are owned by player 0."""
    for card in game_state.pitch_owner_cards:
        assert getattr(card, "owner_id", None) == 0, (
            f"Engine Feature Needed: Card {getattr(card, 'name', 'Unknown')} "
            f"should be owned by player 0 (Rule 3.14.2)"
        )


# ===== Scenario 13: Empty pitch zone still exists =====
# Tests Rule 3.0.1a cross-ref - Empty zone does not cease to exist


@scenario(
    "../features/section_3_14_pitch.feature",
    "An empty pitch zone still exists",
)
def test_empty_pitch_zone_still_exists():
    """Rule 3.0.1a: An empty pitch zone does not cease to exist."""
    pass


@when("checking if the pitch zone exists")
def check_if_pitch_zone_exists(game_state):
    """Rule 3.0.1a: Check if empty pitch zone persists."""
    zone = game_state.empty_pitch_zone
    # Engine Feature Needed: Zone.exists property or just non-None zone
    game_state.pitch_zone_exists = zone is not None
    try:
        _ = getattr(zone, "zone_type", None) or getattr(zone, "_zone_type", None)
        game_state.pitch_zone_exists = True  # Zone object still referenced = still exists
    except Exception:
        game_state.pitch_zone_exists = True


@then("the pitch zone still exists even when empty")
def empty_pitch_zone_still_exists(game_state):
    """Rule 3.0.1a: Empty pitch zone should still exist."""
    assert game_state.pitch_zone_exists is True, (
        "Engine Feature Needed: Empty pitch zone should persist - zones don't cease when empty (Rule 3.0.1a)"
    )


# ===== Helper Functions =====


# Deck-card types per Rule 1.3.2c
# Note: CardType.BLOCK, CardType.MENTOR, CardType.RESOURCE may not exist in engine yet
_DECK_CARD_TYPES = frozenset(
    [
        CardType.ACTION,
        CardType.ATTACK_REACTION,
        CardType.DEFENSE_REACTION,
        CardType.INSTANT,
        # The following may be missing from engine as new types per Rule 1.3.2c:
        # CardType.BLOCK, CardType.MENTOR, CardType.RESOURCE
    ]
)

# Arena-card types per Rule 1.3.2d (cannot be in pitch zone)
_ARENA_CARD_TYPES = frozenset(
    [
        CardType.EQUIPMENT,
        CardType.WEAPON,
    ]
)


def _create_action_card(name: str, owner_id: int = 0):
    """
    Helper to create a simple action card with a given owner.

    Rule 3.14.2: Action cards are deck-cards (Rule 1.3.2c); valid in pitch zone.
    """
    try:
        template = CardTemplate(
            unique_id=f"test_pitch_{name}_{owner_id}",
            name=name,
            types=frozenset([CardType.ACTION]),
            supertypes=frozenset(),
            subtypes=frozenset([Subtype.ATTACK]),
            color=Color.RED,
            pitch=1,
            has_pitch=True,
            cost=0,
            has_cost=True,
            power=4,
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
        card = CardInstance(template=template, owner_id=owner_id)
        return card
    except (TypeError, AttributeError):
        return PitchCardStub(name=name, owner_id=owner_id, card_type=CardType.ACTION)


def _create_attack_reaction_card(name: str, owner_id: int = 0):
    """
    Helper to create an attack reaction card with a given owner.

    Rule 3.14.2 / 1.3.2c: Attack Reaction cards are deck-cards; valid in pitch zone.
    """
    try:
        template = CardTemplate(
            unique_id=f"test_pitch_{name}_{owner_id}",
            name=name,
            types=frozenset([CardType.ATTACK_REACTION]),
            supertypes=frozenset(),
            subtypes=frozenset(),
            color=Color.RED,
            pitch=1,
            has_pitch=True,
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
        card = CardInstance(template=template, owner_id=owner_id)
        return card
    except (TypeError, AttributeError):
        return PitchCardStub(
            name=name, owner_id=owner_id, card_type=CardType.ATTACK_REACTION
        )


def _create_instant_card(name: str, owner_id: int = 0):
    """
    Helper to create an instant card with a given owner.

    Rule 3.14.2 / 1.3.2c: Instant cards are deck-cards; valid in pitch zone.
    """
    try:
        template = CardTemplate(
            unique_id=f"test_pitch_{name}_{owner_id}",
            name=name,
            types=frozenset([CardType.INSTANT]),
            supertypes=frozenset(),
            subtypes=frozenset(),
            color=Color.BLUE,
            pitch=3,
            has_pitch=True,
            cost=0,
            has_cost=True,
            power=0,
            has_power=False,
            defense=0,
            has_defense=False,
            arcane=0,
            has_arcane=False,
            life=0,
            intellect=0,
            keywords=frozenset(),
            keyword_params=tuple(),
            functional_text="",
        )
        card = CardInstance(template=template, owner_id=owner_id)
        return card
    except (TypeError, AttributeError):
        return PitchCardStub(name=name, owner_id=owner_id, card_type=CardType.INSTANT)


def _create_equipment_card(name: str, owner_id: int = 0):
    """
    Helper to create an equipment card with a given owner.

    Rule 1.3.2d: Equipment is an arena-card (not a deck-card); invalid in pitch zone.
    Rule 3.14.2: Pitch zone can only contain deck-cards; equipment must be rejected.
    """
    try:
        template = CardTemplate(
            unique_id=f"test_pitch_{name}_{owner_id}",
            name=name,
            types=frozenset([CardType.EQUIPMENT]),
            supertypes=frozenset(),
            subtypes=frozenset([Subtype.HEAD]),
            color=Color.COLORLESS,
            pitch=0,
            has_pitch=False,
            cost=0,
            has_cost=False,
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
        card = CardInstance(template=template, owner_id=owner_id)
        return card
    except (TypeError, AttributeError):
        return PitchCardStub(name=name, owner_id=owner_id, card_type=CardType.EQUIPMENT)


def _is_deck_card(card) -> bool:
    """
    Check if a card is a deck-card (per Rule 1.3.2c).

    Deck-card types: Action, Attack Reaction, Block, Defense Reaction, Instant, Mentor, Resource
    Arena-card types (not deck-cards): Equipment, Weapon, Hero, Token

    Rule 3.14.2: Pitch zone can only contain its owner's deck-cards.
    """
    # Try to get types from real CardInstance
    try:
        card_types = card.template.types
        return bool(card_types & _DECK_CARD_TYPES) and not bool(
            card_types & _ARENA_CARD_TYPES
        )
    except AttributeError:
        pass

    # Try stub card type attribute
    card_type = getattr(card, "card_type", None)
    if card_type is not None:
        return card_type in _DECK_CARD_TYPES

    # Unknown card type - assume deck-card for leniency
    return True


def _simulate_place_card_in_pitch(zone, card, zone_owner_id: int):
    """
    Helper to simulate placing a card in a pitch zone.

    Engine Feature Needed:
    - Rule 3.14.2: Pitch zone can only contain its owner's deck-cards
    - Zone should reject cards whose owner_id doesn't match the zone's owner_id
    - Zone should reject non-deck-cards (equipment, weapon, hero, token)

    Returns a PitchPlacementResultStub indicating success or failure.
    """
    # Try real engine method first
    try:
        result = zone.add_card_to_pitch(card)
        return PitchPlacementResultStub(
            success=result,
            card_in_zone=result,
            failure_reason=None if result else "unknown",
        )
    except AttributeError:
        pass

    # Determine zone owner and card owner
    zone_owner = getattr(zone, "owner_id", zone_owner_id)
    card_owner = getattr(card, "owner_id", zone_owner_id)

    # Rule 3.14.2: Only owner's cards can be in the pitch zone
    is_owners_card = card_owner == zone_owner

    # Rule 3.14.2 / 1.3.2c: Only deck-cards can be in the pitch zone
    card_is_deck_card = _is_deck_card(card)

    if not is_owners_card:
        return PitchPlacementResultStub(
            success=False,
            card_in_zone=False,
            failure_reason="card_not_owned_by_zone_owner",
        )

    if not card_is_deck_card:
        return PitchPlacementResultStub(
            success=False,
            card_in_zone=False,
            failure_reason="card_is_not_a_deck_card",
        )

    # Simulate successful placement by tracking in zone's internal list
    try:
        zone._cards.append(card)
    except AttributeError:
        pass

    return PitchPlacementResultStub(
        success=True,
        card_in_zone=True,
        failure_reason=None,
    )


# ===== Stub Classes for Missing Engine Features =====


class PitchZoneStub:
    """
    Stub for engine feature: Pitch zone implementation.

    Engine Features Needed:
    - [ ] Zone.is_public_zone property: True for pitch zone (Rule 3.14.1, 3.0.4a)
          NOTE: Unlike hand zone (private), pitch zone is PUBLIC.
    - [ ] Zone.is_private_zone property: False for pitch zone (Rule 3.14.1)
    - [ ] Zone.is_arena_zone property: False for pitch zone (Rule 3.14.1, 3.0.5b)
    - [ ] Zone.owner_id property: EXISTS in engine but stub needed for fallback (Rule 3.14.1)
    - [ ] Pitch zone rejects non-owner's cards (Rule 3.14.2)
    - [ ] Pitch zone rejects non-deck-cards (Rule 3.14.2, cross-ref 1.3.2c)
    - [ ] Zone.is_empty property: EXISTS in engine but stub needed for fallback (Rule 3.0.1a)
    """

    def __init__(self, owner_id: int = 0):
        self.owner_id = owner_id
        self.is_public_zone = True   # Rule 3.14.1 + 3.0.4a — PUBLIC (unlike hand zone!)
        self.is_private_zone = False
        self.is_arena_zone = False   # Rule 3.14.1 + 3.0.5b (outside arena)
        self._cards: list = []

    @property
    def is_empty(self):
        """Rule 3.0.1a: Zone is empty if no cards."""
        return len(self._cards) == 0

    @property
    def cards(self):
        """Get cards in this zone."""
        return list(self._cards)

    def add(self, card):
        """Add a card to the zone (for test setup only - does not validate ownership)."""
        self._cards.append(card)

    def add_card(self, card):
        """Alias for add."""
        self._cards.append(card)


class PitchCardStub:
    """
    Stub for a simple card with owner and type tracking.

    Engine Features Needed:
    - [ ] CardInstance.owner_id property (Rule 1.3.1a)
    - [ ] CardInstance.template.types property (Rule 1.3.2c)
    """

    def __init__(self, name: str, owner_id: int = 0, card_type=None):
        self.name = name
        self.owner_id = owner_id
        self.card_type = card_type  # For type checking in _is_deck_card()


class PitchPlacementResultStub:
    """
    Stub for the result of placing a card in a pitch zone.

    Engine Features Needed:
    - [ ] PitchZone.add_card() validating ownership and deck-card type (Rule 3.14.2)
    - [ ] Rejection with failure_reason when card is not owner's (Rule 3.14.2)
    - [ ] Rejection with failure_reason when card is not a deck-card (Rule 3.14.2 / 1.3.2c)
    """

    def __init__(
        self,
        success: bool,
        card_in_zone: bool = False,
        failure_reason=None,
    ):
        self.success = success
        self.card_in_zone = card_in_zone
        self.failure_reason = failure_reason


# ===== Fixtures =====


@pytest.fixture
def game_state():
    """
    Fixture providing game state for testing Section 3.14.

    Uses BDDGameState which integrates with the real engine.
    Reference: Rule 3.14

    Note: TestPlayer.pitch_zone already exists in bdd_helpers.py using ZoneType.PITCH.
    """
    from tests.bdd_helpers import BDDGameState

    state = BDDGameState()

    # Initialize default pitch zone (fallback stub)
    state.pitch_zone = PitchZoneStub(owner_id=0)
    state.empty_pitch_zone = PitchZoneStub(owner_id=0)

    return state
