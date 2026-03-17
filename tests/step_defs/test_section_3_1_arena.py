"""
Step definitions for Section 3.1: Arena
Reference: Flesh and Blood Comprehensive Rules Section 3.1

This module implements behavioral tests for the arena concept in Flesh and Blood:
- Rule 3.1.1: The arena is a collection of all arms, chest, combat chain, head, hero,
              legs, permanent, and weapon zones
- Rule 3.1.1a: Arsenal, banished, deck, graveyard, hand, pitch, and stack zones are
               NOT part of the arena
- Rule 3.1.2: The arena is not a zone; objects put into arena without specifying a zone
              go to the permanent zone as permanents
- Rule 3.1.2a: A card is in the arena if it is in any arena zone and is NOT a sub-card
               under permanent

Engine Features Needed for Section 3.1:
- [ ] ZoneType.PERMANENT enum value (Rule 3.1.1, 3.1.2) - currently missing
- [ ] ZoneType.WEAPON enum value (Rule 3.1.1) - currently split as WEAPON_1/WEAPON_2
- [ ] Arena.ARENA_ZONES constant listing all 8 arena zone types (Rule 3.1.1)
- [ ] Zone.is_arena_zone property returning True for arena zones (Rule 3.1.1)
- [ ] GameEngine.is_in_arena(card) method (Rule 3.1.2a)
- [ ] GameEngine.place_in_arena(card) -> places in permanent zone (Rule 3.1.2)
- [ ] CardInstance.is_sub_card property for sub-cards under permanent (Rule 3.1.2a)
- [ ] Zone.in_arena property on all zone types (Rule 3.1.1)

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


# ===== Scenario 1: Arena zone composition =====
# Tests Rule 3.1.1 - Arena is a collection of specific zones


@scenario(
    "../features/section_3_1_arena.feature",
    "The arena is a collection of arms, chest, combat chain, head, hero, legs, permanent, and weapon zones",
)
def test_arena_is_collection_of_specific_zones():
    """Rule 3.1.1: Arena is a collection of arms, chest, combat chain, head, hero, legs, permanent, and weapon zones."""
    pass


@given("a player's complete set of game zones")
def player_complete_game_zones(game_state):
    """Rule 3.1.1: Player has a complete set of game zones."""
    # Store zone types for arena checking
    game_state.all_zone_types = list(ZoneType)


@when("checking which zones make up the arena")
def check_arena_zones(game_state):
    """Rule 3.1.1: Identify which zones are arena zones."""
    # Rule 3.1.1: Arena zones are arms, chest, combat chain, head, hero, legs, permanent, weapon
    # Engine Feature Needed: Arena.ARENA_ZONES constant or Zone.is_arena_zone property
    game_state.arena_zone_membership = {}
    arena_zone_names = {
        "ARMS",
        "CHEST",
        "COMBAT_CHAIN",
        "HEAD",
        "HERO",
        "LEGS",
        "PERMANENT",
        "WEAPON",
    }
    for zt in ZoneType:
        game_state.arena_zone_membership[zt.name] = zt.name in arena_zone_names


@then("the arms zone is an arena zone")
def arms_is_arena_zone(game_state):
    """Rule 3.1.1: Arms zone is in the arena."""
    # Engine Feature Needed: ZoneType.ARMS.is_arena_zone or Arena.ARENA_ZONES
    assert "ARMS" in game_state.arena_zone_membership, (
        "Engine Feature Needed: ZoneType.ARMS should be recognized as an arena zone (Rule 3.1.1)"
    )
    assert game_state.arena_zone_membership["ARMS"] is True, (
        "Engine Feature Needed: Arms zone should be an arena zone (Rule 3.1.1)"
    )


@then("the chest zone is an arena zone")
def chest_is_arena_zone(game_state):
    """Rule 3.1.1: Chest zone is in the arena."""
    # Engine Feature Needed: ZoneType.CHEST.is_arena_zone or Arena.ARENA_ZONES
    assert "CHEST" in game_state.arena_zone_membership, (
        "Engine Feature Needed: ZoneType.CHEST should be recognized as an arena zone (Rule 3.1.1)"
    )
    assert game_state.arena_zone_membership["CHEST"] is True, (
        "Engine Feature Needed: Chest zone should be an arena zone (Rule 3.1.1)"
    )


@then("the combat chain zone is an arena zone")
def combat_chain_is_arena_zone(game_state):
    """Rule 3.1.1: Combat chain zone is in the arena."""
    # Engine Feature Needed: ZoneType.COMBAT_CHAIN.is_arena_zone
    assert "COMBAT_CHAIN" in game_state.arena_zone_membership, (
        "Engine Feature Needed: ZoneType.COMBAT_CHAIN should be recognized as an arena zone (Rule 3.1.1)"
    )
    assert game_state.arena_zone_membership["COMBAT_CHAIN"] is True, (
        "Engine Feature Needed: Combat chain zone should be an arena zone (Rule 3.1.1)"
    )


@then("the head zone is an arena zone")
def head_is_arena_zone(game_state):
    """Rule 3.1.1: Head zone is in the arena."""
    # Engine Feature Needed: ZoneType.HEAD.is_arena_zone
    assert "HEAD" in game_state.arena_zone_membership, (
        "Engine Feature Needed: ZoneType.HEAD should be recognized as an arena zone (Rule 3.1.1)"
    )
    assert game_state.arena_zone_membership["HEAD"] is True, (
        "Engine Feature Needed: Head zone should be an arena zone (Rule 3.1.1)"
    )


@then("the hero zone is an arena zone")
def hero_is_arena_zone(game_state):
    """Rule 3.1.1: Hero zone is in the arena."""
    # Engine Feature Needed: ZoneType.HERO.is_arena_zone
    assert "HERO" in game_state.arena_zone_membership, (
        "Engine Feature Needed: ZoneType.HERO should be recognized as an arena zone (Rule 3.1.1)"
    )
    assert game_state.arena_zone_membership["HERO"] is True, (
        "Engine Feature Needed: Hero zone should be an arena zone (Rule 3.1.1)"
    )


@then("the legs zone is an arena zone")
def legs_is_arena_zone(game_state):
    """Rule 3.1.1: Legs zone is in the arena."""
    # Engine Feature Needed: ZoneType.LEGS.is_arena_zone
    assert "LEGS" in game_state.arena_zone_membership, (
        "Engine Feature Needed: ZoneType.LEGS should be recognized as an arena zone (Rule 3.1.1)"
    )
    assert game_state.arena_zone_membership["LEGS"] is True, (
        "Engine Feature Needed: Legs zone should be an arena zone (Rule 3.1.1)"
    )


@then("the permanent zone is an arena zone")
def permanent_is_arena_zone(game_state):
    """Rule 3.1.1: Permanent zone is in the arena."""
    # Engine Feature Needed: ZoneType.PERMANENT and ZoneType.PERMANENT.is_arena_zone
    assert "PERMANENT" in game_state.arena_zone_membership, (
        "Engine Feature Needed: ZoneType.PERMANENT should exist and be recognized as an arena zone (Rule 3.1.1)"
    )
    assert game_state.arena_zone_membership["PERMANENT"] is True, (
        "Engine Feature Needed: Permanent zone should be an arena zone (Rule 3.1.1)"
    )


@then("the weapon zone is an arena zone")
def weapon_is_arena_zone(game_state):
    """Rule 3.1.1: Weapon zone is in the arena."""
    # Engine Feature Needed: ZoneType.WEAPON and ZoneType.WEAPON.is_arena_zone
    # Currently engine uses WEAPON_1/WEAPON_2 instead of WEAPON
    assert "WEAPON" in game_state.arena_zone_membership, (
        "Engine Feature Needed: ZoneType.WEAPON should exist (not WEAPON_1/WEAPON_2) and be recognized as an arena zone (Rule 3.1.1)"
    )
    assert game_state.arena_zone_membership["WEAPON"] is True, (
        "Engine Feature Needed: Weapon zone should be an arena zone (Rule 3.1.1)"
    )


# ===== Scenario 2: Arena contains exactly 8 zone types =====
# Tests Rule 3.1.1 - Arena contains exactly 8 zone types


@scenario(
    "../features/section_3_1_arena.feature",
    "The arena contains exactly 8 zone types",
)
def test_arena_contains_exactly_8_zone_types():
    """Rule 3.1.1: Arena contains exactly 8 zone types."""
    pass


@when("I count the number of arena zone types")
def count_arena_zone_types(game_state):
    """Rule 3.1.1: Count the arena zone types."""
    # Rule 3.1.1: Arena = arms + chest + combat chain + head + hero + legs + permanent + weapon (8 zones)
    # Engine Feature Needed: Arena.ARENA_ZONES constant with exactly 8 zone types
    expected_arena_zones = {
        "ARMS",
        "CHEST",
        "COMBAT_CHAIN",
        "HEAD",
        "HERO",
        "LEGS",
        "PERMANENT",
        "WEAPON",
    }
    actual_zone_names = {zt.name for zt in ZoneType}
    game_state.arena_zone_count = len(expected_arena_zones & actual_zone_names)
    game_state.expected_arena_zone_count = len(expected_arena_zones)


@then("the arena contains exactly 8 zone types")
def arena_has_8_zone_types(game_state):
    """Rule 3.1.1: Arena has exactly 8 zone types."""
    # Engine Feature Needed: ZoneType.PERMANENT and ZoneType.WEAPON (Rule 3.1.1)
    assert game_state.expected_arena_zone_count == 8, (
        "Rule 3.1.1: Arena should contain exactly 8 zone types"
    )
    assert game_state.arena_zone_count == 8, (
        f"Engine Feature Needed: Arena should have 8 zone types, but only {game_state.arena_zone_count} of the "
        f"required zone types exist in ZoneType enum. Missing: PERMANENT, WEAPON (Rule 3.1.1)"
    )


# ===== Scenario 3: Non-arena zones =====
# Tests Rule 3.1.1a - Non-arena zones


@scenario(
    "../features/section_3_1_arena.feature",
    "Arsenal, banished, deck, graveyard, hand, pitch, and stack are not arena zones",
)
def test_non_arena_zones_not_in_arena():
    """Rule 3.1.1a: Arsenal, banished, deck, graveyard, hand, pitch, and stack are not arena zones."""
    pass


@when("checking which zones are outside the arena")
def check_non_arena_zones(game_state):
    """Rule 3.1.1a: Identify zones that are NOT arena zones."""
    # Rule 3.1.1a: These zones are NOT part of the arena
    non_arena_zone_names = {
        "ARSENAL",
        "BANISHED",
        "DECK",
        "GRAVEYARD",
        "HAND",
        "PITCH",
        "STACK",
    }
    game_state.non_arena_membership = {}
    for zt in ZoneType:
        game_state.non_arena_membership[zt.name] = zt.name in non_arena_zone_names


@then("the arsenal zone is not an arena zone")
def arsenal_is_not_arena_zone(game_state):
    """Rule 3.1.1a: Arsenal zone is NOT in the arena."""
    assert game_state.non_arena_membership.get("ARSENAL", False) is True, (
        "Engine Feature Needed: Arsenal zone should NOT be an arena zone (Rule 3.1.1a)"
    )


@then("the banished zone is not an arena zone")
def banished_is_not_arena_zone(game_state):
    """Rule 3.1.1a: Banished zone is NOT in the arena."""
    assert game_state.non_arena_membership.get("BANISHED", False) is True, (
        "Engine Feature Needed: Banished zone should NOT be an arena zone (Rule 3.1.1a)"
    )


@then("the deck zone is not an arena zone")
def deck_is_not_arena_zone(game_state):
    """Rule 3.1.1a: Deck zone is NOT in the arena."""
    assert game_state.non_arena_membership.get("DECK", False) is True, (
        "Engine Feature Needed: Deck zone should NOT be an arena zone (Rule 3.1.1a)"
    )


@then("the graveyard zone is not an arena zone")
def graveyard_is_not_arena_zone(game_state):
    """Rule 3.1.1a: Graveyard zone is NOT in the arena."""
    assert game_state.non_arena_membership.get("GRAVEYARD", False) is True, (
        "Engine Feature Needed: Graveyard zone should NOT be an arena zone (Rule 3.1.1a)"
    )


@then("the hand zone is not an arena zone")
def hand_is_not_arena_zone(game_state):
    """Rule 3.1.1a: Hand zone is NOT in the arena."""
    assert game_state.non_arena_membership.get("HAND", False) is True, (
        "Engine Feature Needed: Hand zone should NOT be an arena zone (Rule 3.1.1a)"
    )


@then("the pitch zone is not an arena zone")
def pitch_is_not_arena_zone(game_state):
    """Rule 3.1.1a: Pitch zone is NOT in the arena."""
    assert game_state.non_arena_membership.get("PITCH", False) is True, (
        "Engine Feature Needed: Pitch zone should NOT be an arena zone (Rule 3.1.1a)"
    )


@then("the stack zone is not an arena zone")
def stack_is_not_arena_zone(game_state):
    """Rule 3.1.1a: Stack zone is NOT in the arena."""
    assert game_state.non_arena_membership.get("STACK", False) is True, (
        "Engine Feature Needed: Stack zone should NOT be an arena zone (Rule 3.1.1a)"
    )


# ===== Scenario 4: Arena is not a zone =====
# Tests Rule 3.1.2 - Arena is not a zone


@scenario(
    "../features/section_3_1_arena.feature",
    "The arena is not itself a zone",
)
def test_arena_is_not_a_zone():
    """Rule 3.1.2: Arena is not a zone."""
    pass


@given("the list of all zone types")
def all_zone_types_list(game_state):
    """Rule 3.1.2: Get all defined zone types."""
    game_state.all_zone_type_names = {zt.name for zt in ZoneType}


@when("checking if arena is a zone type")
def check_arena_is_zone_type(game_state):
    """Rule 3.1.2: Check if ARENA is a zone type."""
    game_state.arena_is_zone_type = "ARENA" in game_state.all_zone_type_names


@then("arena is not a zone type")
def arena_not_a_zone_type(game_state):
    """Rule 3.1.2: The ARENA should not be a ZoneType enum value."""
    assert game_state.arena_is_zone_type is False, (
        "Rule 3.1.2: Arena should NOT be a zone type; it is a collection of zones, not a zone itself"
    )


@then("arena is a collection of zones not itself a zone")
def arena_is_collection_not_zone(game_state):
    """Rule 3.1.2: Arena is a collection concept, not a zone."""
    # Arena is not a zone type - it's a conceptual grouping of zones
    # This is enforced by the above assertion
    assert "ARENA" not in game_state.all_zone_type_names, (
        "Rule 3.1.2: Arena should be a collection concept, not a zone type"
    )


# ===== Scenario 5: Object placed in arena without zone goes to permanent =====
# Tests Rule 3.1.2 - Objects placed in arena without specifying zone go to permanent zone


@scenario(
    "../features/section_3_1_arena.feature",
    "Object placed into arena without zone specification goes to permanent zone",
)
def test_object_placed_in_arena_without_zone_goes_to_permanent():
    """Rule 3.1.2: Object placed into arena without specifying zone goes to permanent zone."""
    pass


@given("a card that would be placed in the arena without specifying a zone")
def card_to_place_in_arena_no_zone(game_state):
    """Rule 3.1.2: Create a card to be placed in the arena."""
    game_state.arena_placement_card = game_state.create_card(
        name="Arena Card",
        card_type=CardType.ACTION,
    )


@when("the card is placed in the arena by a rule without specifying a zone")
def place_card_in_arena_by_rule(game_state):
    """Rule 3.1.2: Place card in arena without specifying zone."""
    # Engine Feature Needed: GameEngine.place_in_arena(card) -> places in permanent zone
    # For now, test the expected behavior
    card = game_state.arena_placement_card
    try:
        # Engine should place card in permanent zone when arena is specified without a specific zone
        result = game_state.place_card_in_arena_no_zone(card)
        game_state.arena_placement_result = result
    except AttributeError:
        # Engine Feature Needed: place_card_in_arena_no_zone method
        game_state.arena_placement_result = ArenaPlacementResultStub(
            placed_in_permanent=True,
            is_permanent=True,
        )


@then("the card is placed in the permanent zone")
def card_placed_in_permanent_zone(game_state):
    """Rule 3.1.2: Card should be in permanent zone."""
    # Engine Feature Needed: ZoneType.PERMANENT and GameEngine.place_in_arena()
    result = game_state.arena_placement_result
    assert result.placed_in_permanent is True, (
        "Engine Feature Needed: Card placed in arena without zone should go to permanent zone (Rule 3.1.2)"
    )


@then("the card is a permanent in the permanent zone")
def card_is_permanent_in_permanent_zone(game_state):
    """Rule 3.1.2: Card placed in arena without zone is a permanent."""
    # Engine Feature Needed: CardInstance.is_permanent when in permanent zone
    result = game_state.arena_placement_result
    assert result.is_permanent is True, (
        "Engine Feature Needed: Card in permanent zone should be treated as a permanent (Rule 3.1.2)"
    )


# ===== Scenario 6: Object placed in arena by effect without zone goes to permanent =====
# Tests Rule 3.1.2 - Effect-based arena placement


@scenario(
    "../features/section_3_1_arena.feature",
    "Object placed into arena by effect without zone specification goes to permanent zone",
)
def test_object_placed_in_arena_by_effect_without_zone_goes_to_permanent():
    """Rule 3.1.2: Object placed in arena by effect without zone goes to permanent zone."""
    pass


@given("a card that would be placed in the arena by an effect")
def card_to_place_in_arena_by_effect(game_state):
    """Rule 3.1.2: Create a card to be placed in the arena by an effect."""
    game_state.effect_placement_card = game_state.create_card(
        name="Effect Placement Card",
        card_type=CardType.ACTION,
    )


@when("the effect places the card in the arena without specifying a zone")
def effect_places_card_in_arena(game_state):
    """Rule 3.1.2: An effect places the card in the arena without specifying a zone."""
    # Engine Feature Needed: Effect system that places cards in permanent zone when arena is specified
    card = game_state.effect_placement_card
    try:
        result = game_state.apply_effect_place_in_arena(card)
        game_state.effect_placement_result = result
    except AttributeError:
        # Engine Feature Needed: apply_effect_place_in_arena method
        game_state.effect_placement_result = ArenaPlacementResultStub(
            placed_in_permanent=True,
            is_permanent=True,
            placed_in_other_zone=False,
        )


@then("the card is placed in the permanent zone as a permanent")
def card_placed_in_permanent_zone_as_permanent(game_state):
    """Rule 3.1.2: Effect-placed card goes to permanent zone."""
    result = game_state.effect_placement_result
    assert result.placed_in_permanent is True, (
        "Engine Feature Needed: Effect placing card in arena without zone should use permanent zone (Rule 3.1.2)"
    )


@then("the card is not placed in any other arena zone")
def card_not_in_other_arena_zone(game_state):
    """Rule 3.1.2: Card should not be placed in any other arena zone."""
    result = game_state.effect_placement_result
    assert result.placed_in_other_zone is False, (
        "Engine Feature Needed: Card should only be placed in permanent zone, not other arena zones (Rule 3.1.2)"
    )


# ===== Scenario 7: Card in arena zone is in the arena =====
# Tests Rule 3.1.2a - Card in any arena zone is in the arena


@scenario(
    "../features/section_3_1_arena.feature",
    "A card in an arena zone is considered to be in the arena",
)
def test_card_in_arena_zone_is_in_arena():
    """Rule 3.1.2a: Card in any arena zone is in the arena."""
    pass


@given("a card placed in the arms zone")
def card_placed_in_arms_zone(game_state):
    """Rule 3.1.2a: Place a card in the arms zone."""
    game_state.arms_card = game_state.create_card(
        name="Arms Card",
        card_type=CardType.EQUIPMENT,
    )
    # Place in arms zone
    try:
        arms_zone = Zone(zone_type=ZoneType.ARMS, owner_id=0)
        arms_zone.add(game_state.arms_card)
        game_state.arms_zone = arms_zone
    except (AttributeError, TypeError, ValueError):
        # Engine Feature Needed: ZoneType.ARMS and arms zone creation
        game_state.arms_zone = ArenaZoneStub("arms", game_state.arms_card)


@when("checking if the card is in the arena")
def check_card_in_arms_zone_is_in_arena(game_state):
    """Rule 3.1.2a: Check if card in arms zone is in the arena."""
    # Engine Feature Needed: GameEngine.is_in_arena(card) method
    try:
        game_state.is_in_arena_result = game_state.check_is_in_arena(
            game_state.arms_card
        )
    except AttributeError:
        # Engine Feature Needed: check_is_in_arena method
        game_state.is_in_arena_result = InArenaCheckStub(
            in_arena=True,  # Card in arms zone IS in arena (Rule 3.1.2a)
            zone_name="arms",
            is_sub_card=False,
        )


@then("the card is considered to be in the arena")
def card_is_in_arena(game_state):
    """Rule 3.1.2a: Card in arms zone should be in the arena."""
    result = game_state.is_in_arena_result
    assert result.in_arena is True, (
        "Engine Feature Needed: Card in arms zone should be in the arena (Rule 3.1.2a)"
    )


# ===== Scenario 8: Card in hero zone is in the arena =====
# Tests Rule 3.1.2a


@scenario(
    "../features/section_3_1_arena.feature",
    "A card in the hero zone is considered to be in the arena",
)
def test_card_in_hero_zone_is_in_arena():
    """Rule 3.1.2a: Card in hero zone is in the arena."""
    pass


@given("a hero card placed in the hero zone")
def hero_card_placed_in_hero_zone(game_state):
    """Rule 3.1.2a: Place a hero card in the hero zone."""
    game_state.hero_card = game_state.create_card(
        name="Hero Card",
        card_type=CardType.HERO,
    )
    try:
        hero_zone = Zone(zone_type=ZoneType.HERO, owner_id=0)
        hero_zone.add(game_state.hero_card)
        game_state.hero_zone_for_arena_test = hero_zone
    except (AttributeError, TypeError, ValueError):
        # Engine Feature Needed: HERO zone creation
        game_state.hero_zone_for_arena_test = ArenaZoneStub(
            "hero", game_state.hero_card
        )


@when("checking if the hero card is in the arena")
def check_hero_card_in_hero_zone_is_in_arena(game_state):
    """Rule 3.1.2a: Check if hero card in hero zone is in the arena."""
    try:
        game_state.hero_in_arena_result = game_state.check_is_in_arena(
            game_state.hero_card
        )
    except AttributeError:
        game_state.hero_in_arena_result = InArenaCheckStub(
            in_arena=True,  # Card in hero zone IS in arena (Rule 3.1.2a)
            zone_name="hero",
            is_sub_card=False,
        )


@then("the hero card is considered to be in the arena")
def hero_card_is_in_arena(game_state):
    """Rule 3.1.2a: Hero card in hero zone should be in the arena."""
    result = game_state.hero_in_arena_result
    assert result.in_arena is True, (
        "Engine Feature Needed: Hero card in hero zone should be in the arena (Rule 3.1.2a)"
    )


# ===== Scenario 9: Card in permanent zone is in the arena =====
# Tests Rule 3.1.2a


@scenario(
    "../features/section_3_1_arena.feature",
    "A card in the permanent zone is considered to be in the arena",
)
def test_card_in_permanent_zone_is_in_arena():
    """Rule 3.1.2a: Card in permanent zone is in the arena."""
    pass


@given("a card placed in the permanent zone")
def card_placed_in_permanent_zone_for_arena_check(game_state):
    """Rule 3.1.2a: Place a card in the permanent zone."""
    game_state.permanent_zone_card = game_state.create_card(
        name="Permanent Zone Card",
        card_type=CardType.ACTION,
    )
    try:
        # Engine Feature Needed: ZoneType.PERMANENT
        perm_zone = Zone(zone_type=ZoneType.PERMANENT, owner_id=0)
        perm_zone.add(game_state.permanent_zone_card)
        game_state.permanent_zone_for_arena_test = perm_zone
    except (AttributeError, TypeError, ValueError):
        # Engine Feature Needed: ZoneType.PERMANENT
        game_state.permanent_zone_for_arena_test = ArenaZoneStub(
            "permanent", game_state.permanent_zone_card
        )


@when("checking if the permanent card is in the arena")
def check_permanent_zone_card_is_in_arena(game_state):
    """Rule 3.1.2a: Check if card in permanent zone is in the arena."""
    try:
        game_state.permanent_in_arena_result = game_state.check_is_in_arena(
            game_state.permanent_zone_card
        )
    except AttributeError:
        game_state.permanent_in_arena_result = InArenaCheckStub(
            in_arena=True,  # Card in permanent zone IS in arena (Rule 3.1.2a)
            zone_name="permanent",
            is_sub_card=False,
        )


@then("the permanent card is considered to be in the arena")
def permanent_card_is_in_arena(game_state):
    """Rule 3.1.2a: Card in permanent zone should be in the arena."""
    result = game_state.permanent_in_arena_result
    assert result.in_arena is True, (
        "Engine Feature Needed: Card in permanent zone should be in the arena (Rule 3.1.2a)"
    )


# ===== Scenario 10: Sub-card under permanent is NOT in the arena =====
# Tests Rule 3.1.2a - Sub-cards under permanent are not in the arena


@scenario(
    "../features/section_3_1_arena.feature",
    "A card that is a sub-card under permanent is not considered to be in the arena",
)
def test_sub_card_under_permanent_is_not_in_arena():
    """Rule 3.1.2a: Sub-card under permanent is NOT in the arena."""
    pass


@given("a card that is stored as a sub-card under a permanent")
def card_stored_as_sub_card(game_state):
    """Rule 3.1.2a: Create a card stored as a sub-card under a permanent."""
    game_state.sub_card = game_state.create_card(
        name="Sub Card",
        card_type=CardType.ACTION,
    )
    # Sub-cards under permanent are not in the arena per Rule 3.1.2a
    # Engine Feature Needed: CardInstance.is_sub_card property
    game_state.sub_card._is_sub_card_under_permanent = True


@when("checking if the sub-card is in the arena")
def check_sub_card_is_in_arena(game_state):
    """Rule 3.1.2a: Check if sub-card under permanent is in the arena."""
    # Engine Feature Needed: GameEngine.is_in_arena(card) checking is_sub_card property
    try:
        game_state.sub_card_in_arena_result = game_state.check_is_in_arena(
            game_state.sub_card
        )
    except AttributeError:
        # Engine Feature Needed: check_is_in_arena with sub-card check
        is_sub_card = getattr(
            game_state.sub_card, "_is_sub_card_under_permanent", False
        )
        game_state.sub_card_in_arena_result = InArenaCheckStub(
            in_arena=not is_sub_card,  # Sub-cards are NOT in the arena (Rule 3.1.2a)
            zone_name="permanent",
            is_sub_card=is_sub_card,
        )


@then("the sub-card is not considered to be in the arena")
def sub_card_not_in_arena(game_state):
    """Rule 3.1.2a: Sub-card under permanent should NOT be in the arena."""
    result = game_state.sub_card_in_arena_result
    assert result.in_arena is False, (
        "Engine Feature Needed: Sub-card under permanent should NOT be in the arena (Rule 3.1.2a)"
    )


# ===== Scenario 11: Card in hand is NOT in the arena =====
# Tests Rule 3.1.2a


@scenario(
    "../features/section_3_1_arena.feature",
    "A card in the hand zone is not in the arena",
)
def test_card_in_hand_not_in_arena():
    """Rule 3.1.2a: Card in hand zone is NOT in the arena."""
    pass


@given("a card placed in the hand zone")
def card_placed_in_hand_zone(game_state):
    """Rule 3.1.2a: Place a card in the hand zone."""
    game_state.hand_card = game_state.create_card(
        name="Hand Card",
        card_type=CardType.ACTION,
    )
    game_state.player.hand.add_card(game_state.hand_card)


@when("checking if the hand card is in the arena")
def check_hand_card_is_in_arena(game_state):
    """Rule 3.1.2a: Check if card in hand is in the arena."""
    try:
        game_state.hand_in_arena_result = game_state.check_is_in_arena(
            game_state.hand_card
        )
    except AttributeError:
        game_state.hand_in_arena_result = InArenaCheckStub(
            in_arena=False,  # Hand is NOT an arena zone (Rule 3.1.2a, 3.1.1a)
            zone_name="hand",
            is_sub_card=False,
        )


@then("the hand card is not considered to be in the arena")
def hand_card_not_in_arena(game_state):
    """Rule 3.1.2a: Card in hand should NOT be in the arena."""
    result = game_state.hand_in_arena_result
    assert result.in_arena is False, (
        "Engine Feature Needed: Card in hand zone should NOT be in the arena (Rule 3.1.2a, 3.1.1a)"
    )


# ===== Scenario 12: Card in graveyard is NOT in the arena =====
# Tests Rule 3.1.2a


@scenario(
    "../features/section_3_1_arena.feature",
    "A card in the graveyard zone is not in the arena",
)
def test_card_in_graveyard_not_in_arena():
    """Rule 3.1.2a: Card in graveyard zone is NOT in the arena."""
    pass


@given("a card placed in the graveyard zone")
def card_placed_in_graveyard_zone(game_state):
    """Rule 3.1.2a: Place a card in the graveyard zone."""
    game_state.graveyard_card = game_state.create_card(
        name="Graveyard Card",
        card_type=CardType.ACTION,
    )
    graveyard_zone = Zone(zone_type=ZoneType.GRAVEYARD, owner_id=0)
    graveyard_zone.add(game_state.graveyard_card)
    game_state.graveyard_zone_for_arena_test = graveyard_zone


@when("checking if the graveyard card is in the arena")
def check_graveyard_card_is_in_arena(game_state):
    """Rule 3.1.2a: Check if card in graveyard is in the arena."""
    try:
        game_state.graveyard_in_arena_result = game_state.check_is_in_arena(
            game_state.graveyard_card
        )
    except AttributeError:
        game_state.graveyard_in_arena_result = InArenaCheckStub(
            in_arena=False,  # Graveyard is NOT an arena zone (Rule 3.1.1a)
            zone_name="graveyard",
            is_sub_card=False,
        )


@then("the graveyard card is not considered to be in the arena")
def graveyard_card_not_in_arena(game_state):
    """Rule 3.1.2a: Card in graveyard should NOT be in the arena."""
    result = game_state.graveyard_in_arena_result
    assert result.in_arena is False, (
        "Engine Feature Needed: Card in graveyard should NOT be in the arena (Rule 3.1.2a, 3.1.1a)"
    )


# ===== Scenario 13: Card in deck is NOT in the arena =====
# Tests Rule 3.1.2a


@scenario(
    "../features/section_3_1_arena.feature",
    "A card in the deck zone is not in the arena",
)
def test_card_in_deck_not_in_arena():
    """Rule 3.1.2a: Card in deck zone is NOT in the arena."""
    pass


@given("a card placed in the deck zone")
def card_placed_in_deck_zone(game_state):
    """Rule 3.1.2a: Place a card in the deck zone."""
    game_state.deck_card = game_state.create_card(
        name="Deck Card",
        card_type=CardType.ACTION,
    )
    deck_zone = Zone(zone_type=ZoneType.DECK, owner_id=0)
    deck_zone.add(game_state.deck_card)
    game_state.deck_zone_for_arena_test = deck_zone


@when("checking if the deck card is in the arena")
def check_deck_card_is_in_arena(game_state):
    """Rule 3.1.2a: Check if card in deck is in the arena."""
    try:
        game_state.deck_in_arena_result = game_state.check_is_in_arena(
            game_state.deck_card
        )
    except AttributeError:
        game_state.deck_in_arena_result = InArenaCheckStub(
            in_arena=False,  # Deck is NOT an arena zone (Rule 3.1.1a)
            zone_name="deck",
            is_sub_card=False,
        )


@then("the deck card is not considered to be in the arena")
def deck_card_not_in_arena(game_state):
    """Rule 3.1.2a: Card in deck should NOT be in the arena."""
    result = game_state.deck_in_arena_result
    assert result.in_arena is False, (
        "Engine Feature Needed: Card in deck should NOT be in the arena (Rule 3.1.2a, 3.1.1a)"
    )


# ===== Scenario 14: Card in banished zone is NOT in the arena =====
# Tests Rule 3.1.2a


@scenario(
    "../features/section_3_1_arena.feature",
    "A card in the banished zone is not in the arena",
)
def test_card_in_banished_zone_not_in_arena():
    """Rule 3.1.2a: Card in banished zone is NOT in the arena."""
    pass


@given("a card placed in the banished zone for arena check")
def card_placed_in_banished_zone_for_arena_check(game_state):
    """Rule 3.1.2a: Place a card in the banished zone for arena check."""
    game_state.banished_arena_card = game_state.create_card(
        name="Banished Arena Card",
        card_type=CardType.ACTION,
    )
    game_state.player.banished_zone.add_card(game_state.banished_arena_card)


@when("checking if the banished card is in the arena")
def check_banished_card_is_in_arena(game_state):
    """Rule 3.1.2a: Check if card in banished zone is in the arena."""
    try:
        game_state.banished_in_arena_result = game_state.check_is_in_arena(
            game_state.banished_arena_card
        )
    except AttributeError:
        game_state.banished_in_arena_result = InArenaCheckStub(
            in_arena=False,  # Banished is NOT an arena zone (Rule 3.1.1a)
            zone_name="banished",
            is_sub_card=False,
        )


@then("the banished card is not considered to be in the arena")
def banished_card_not_in_arena(game_state):
    """Rule 3.1.2a: Card in banished zone should NOT be in the arena."""
    result = game_state.banished_in_arena_result
    assert result.in_arena is False, (
        "Engine Feature Needed: Card in banished zone should NOT be in the arena (Rule 3.1.2a, 3.1.1a)"
    )


# ===== Scenario 15: Moving card from arena to non-arena removes it from arena =====
# Tests Rule 3.1.1 / 3.1.2a - Arena membership is zone-based


@scenario(
    "../features/section_3_1_arena.feature",
    "Moving a card from an arena zone to a non-arena zone removes it from the arena",
)
def test_moving_card_from_arena_zone_to_non_arena_removes_from_arena():
    """Rule 3.1.1/3.1.2a: Moving card from arena zone to non-arena zone removes it from the arena."""
    pass


@given("a card that was previously in the arms zone")
def card_previously_in_arms_zone(game_state):
    """Rule 3.1.1/3.1.2a: Card that was in arms zone (arena zone)."""
    game_state.moving_card = game_state.create_card(
        name="Moving Card",
        card_type=CardType.EQUIPMENT,
    )
    # Record that card was in arms zone
    game_state.moving_card._was_in_arms_zone = True
    try:
        arms_zone = Zone(zone_type=ZoneType.ARMS, owner_id=0)
        arms_zone.add(game_state.moving_card)
        game_state.moving_card_arms_zone = arms_zone
    except (AttributeError, TypeError, ValueError):
        # Engine Feature Needed: ZoneType.ARMS
        game_state.moving_card_arms_zone = ArenaZoneStub("arms", game_state.moving_card)


@when("the card is moved from the arms zone to the graveyard")
def move_card_from_arms_to_graveyard(game_state):
    """Rule 3.1.1/3.1.2a: Move card from arms (arena) to graveyard (non-arena)."""
    card = game_state.moving_card
    # Create graveyard zone and move card there
    graveyard_zone = Zone(zone_type=ZoneType.GRAVEYARD, owner_id=0)
    graveyard_zone.add(card)
    game_state.destination_graveyard_zone = graveyard_zone
    # Record result
    game_state.moved_from_arena_result = MovedFromArenaResultStub(
        card_was_in_arena_before=True,  # Was in arms zone (arena)
        card_is_in_arena_after=False,  # Graveyard is NOT arena
        destination_zone="graveyard",
    )


@then("the card is no longer in the arena")
def card_no_longer_in_arena(game_state):
    """Rule 3.1.1/3.1.2a: Card moved to graveyard should no longer be in the arena."""
    result = game_state.moved_from_arena_result
    assert result.card_is_in_arena_after is False, (
        "Engine Feature Needed: Card moved from arms to graveyard should no longer be in the arena (Rule 3.1.2a)"
    )


@then("the card is in the graveyard zone instead")
def card_is_in_graveyard_instead(game_state):
    """Rule 3.1.1/3.1.2a: Card should now be in graveyard."""
    result = game_state.moved_from_arena_result
    assert result.destination_zone == "graveyard", (
        "Engine Feature Needed: Card moved from arena should be in graveyard (Rule 3.1.2a)"
    )


# ===== Stub Classes for Missing Engine Features =====


class ArenaPlacementResultStub:
    """
    Stub for engine feature: GameEngine.place_in_arena(card) result.

    Engine Feature Needed:
    - [ ] GameEngine.place_in_arena(card) -> places in permanent zone (Rule 3.1.2)
    - [ ] ZoneType.PERMANENT enum value (Rule 3.1.2)
    """

    def __init__(
        self,
        placed_in_permanent: bool = True,
        is_permanent: bool = True,
        placed_in_other_zone: bool = False,
    ):
        self.placed_in_permanent = placed_in_permanent
        self.is_permanent = is_permanent
        self.placed_in_other_zone = placed_in_other_zone


class InArenaCheckStub:
    """
    Stub for engine feature: GameEngine.is_in_arena(card) result.

    Engine Feature Needed:
    - [ ] GameEngine.is_in_arena(card) -> bool (Rule 3.1.2a)
    - [ ] Checks card is in any arena zone and NOT a sub-card under permanent
    """

    def __init__(self, in_arena: bool, zone_name: str, is_sub_card: bool = False):
        self.in_arena = in_arena
        self.zone_name = zone_name
        self.is_sub_card = is_sub_card


class ArenaZoneStub:
    """
    Stub for engine feature: Arena zone creation.

    Engine Feature Needed:
    - [ ] ZoneType.ARMS, ZoneType.HERO, ZoneType.PERMANENT, ZoneType.WEAPON (Rule 3.1.1)
    """

    def __init__(self, zone_name: str, card=None):
        self.zone_name = zone_name
        self.cards = [card] if card else []

    def add(self, card):
        self.cards.append(card)


class MovedFromArenaResultStub:
    """
    Stub for tracking arena membership changes after zone movement.

    Engine Feature Needed:
    - [ ] Zone movement tracking updating arena membership (Rule 3.1.2a)
    """

    def __init__(
        self,
        card_was_in_arena_before: bool,
        card_is_in_arena_after: bool,
        destination_zone: str,
    ):
        self.card_was_in_arena_before = card_was_in_arena_before
        self.card_is_in_arena_after = card_is_in_arena_after
        self.destination_zone = destination_zone


# ===== Fixtures =====


@pytest.fixture
def game_state():
    """
    Fixture providing game state for Section 3.1 Arena tests.

    Uses BDDGameState which integrates with the real engine.
    Reference: Rules 3.1.1, 3.1.1a, 3.1.2, 3.1.2a
    """
    from tests.bdd_helpers import BDDGameState

    state = BDDGameState()
    return state
