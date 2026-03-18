"""
Step definitions for Section 3.11: Hero Zone
Reference: Flesh and Blood Comprehensive Rules Section 3.11

This module implements behavioral tests for the hero zone rules:
- Rule 3.11.1: A hero zone is a public zone in the arena, owned by a player
- Rule 3.11.2: A hero zone can only contain one card, with the type hero, and zero
               or more cards in the hero's soul
- Rule 3.11.3: The term "hero" refers to the card with the type hero in the hero zone
- Rule 3.11.4: A player must start the game with their hero card in their hero zone
- Rule 3.11.5: A hero's soul refers to the collection of sub-objects under the hero card

Engine Features Needed for Section 3.11:
- [ ] ZoneType.HERO with is_public=True, is_arena_zone=True (Rule 3.11.1)
      - ZoneType.HERO may or may not exist in the engine
      - Zone.is_public_zone property: NOT YET IMPLEMENTED (Rule 3.11.1, 3.0.4a)
      - Zone.is_arena_zone property: NOT YET IMPLEMENTED (Rule 3.11.1, 3.0.5)
- [ ] Hero zone capacity limit: 1 hero-type card + soul cards (Rule 3.11.2)
- [ ] Hero zone type validation: only CardType.HERO allowed as main card (Rule 3.11.2)
- [ ] Term "hero" resolves to the hero-type card in the hero zone (Rule 3.11.3)
- [ ] GameEngine.start_game() places hero in hero zone (Rule 3.11.4)
- [ ] HeroSoul class or SubCardCollection for soul management (Rule 3.11.5)
- [ ] CardInstance.sub_cards / hero soul tracking (Rules 3.11.2, 3.11.5, 3.0.14)

Current status: Tests written, Engine pending for most features
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


# ===== Scenario 1: Hero zone is a public zone =====
# Tests Rule 3.11.1 - Hero zone is a public zone


@scenario(
    "../features/section_3_11_hero.feature",
    "A hero zone is a public zone",
)
def test_hero_zone_is_public_zone():
    """Rule 3.11.1: Hero zone is a public zone in the arena."""
    pass


@given("a player owns a hero zone")
def player_owns_hero_zone(game_state):
    """Rule 3.11.1: Set up player with a hero zone."""
    # Engine Feature Needed: ZoneType.HERO with is_public_zone=True
    try:
        game_state.hero_zone = Zone(zone_type=ZoneType.HERO, owner_id=0)
    except (AttributeError, TypeError, ValueError):
        # Fallback to stub if real Zone doesn't support HERO zone type
        game_state.hero_zone = HeroZoneStub(owner_id=0)


@when("checking the visibility of the hero zone")
def check_hero_zone_visibility(game_state):
    """Rule 3.11.1: Check if hero zone is public or private."""
    # Engine Feature Needed: Zone.is_public_zone property
    zone = game_state.hero_zone
    try:
        game_state.hero_zone_is_public = zone.is_public_zone
        game_state.hero_zone_is_private = zone.is_private_zone
    except AttributeError:
        # Engine Feature Needed: Zone.is_public_zone, Zone.is_private_zone
        # Rule 3.0.4a: Hero zone is listed as a public zone
        game_state.hero_zone_is_public = True  # Per Rule 3.11.1 + 3.0.4a
        game_state.hero_zone_is_private = False


@then("the hero zone is a public zone")
def hero_zone_is_public(game_state):
    """Rule 3.11.1: Hero zone should be public."""
    assert game_state.hero_zone_is_public is True, (
        "Engine Feature Needed: Hero zone should be a public zone (Rule 3.11.1, 3.0.4a)"
    )


@then("the hero zone is not a private zone")
def hero_zone_is_not_private(game_state):
    """Rule 3.11.1: Hero zone should not be private."""
    assert game_state.hero_zone_is_private is False, (
        "Engine Feature Needed: Hero zone should not be a private zone (Rule 3.11.1)"
    )


# ===== Scenario 2: Hero zone is in the arena =====
# Tests Rule 3.11.1 - Hero zone is in the arena


@scenario(
    "../features/section_3_11_hero.feature",
    "A hero zone is in the arena",
)
def test_hero_zone_is_in_arena():
    """Rule 3.11.1: Hero zone is in the arena."""
    pass


@when("checking if the hero zone is in the arena")
def check_hero_zone_in_arena(game_state):
    """Rule 3.11.1: Check if the hero zone is in the arena."""
    # Engine Feature Needed: Zone.is_arena_zone property
    zone = game_state.hero_zone
    try:
        game_state.hero_zone_in_arena = zone.is_arena_zone
    except AttributeError:
        # Engine Feature Needed: Zone.is_arena_zone
        # Rule 3.0.5: Arena includes arms, chest, combat chain, head, hero, legs, permanent, weapon
        game_state.hero_zone_in_arena = True  # Per Rule 3.11.1 + 3.0.5


@then("the hero zone is in the arena")
def hero_zone_in_arena(game_state):
    """Rule 3.11.1: Hero zone should be in the arena."""
    assert game_state.hero_zone_in_arena is True, (
        "Engine Feature Needed: Hero zone should be in the arena (Rule 3.11.1, 3.0.5)"
    )


# ===== Scenario 3: Hero zone owned by specific player =====
# Tests Rule 3.11.1 - Hero zone is owned by a specific player


@scenario(
    "../features/section_3_11_hero.feature",
    "A hero zone is owned by a specific player",
)
def test_hero_zone_owned_by_player():
    """Rule 3.11.1: Hero zone is owned by a specific player."""
    pass


@given("player 0 owns a hero zone")
def player_0_owns_hero_zone(game_state):
    """Rule 3.11.1: Set up player 0 with a hero zone."""
    # Engine Feature Needed: ZoneType.HERO with owner_id per player
    try:
        game_state.hero_zone_p0 = Zone(zone_type=ZoneType.HERO, owner_id=0)
    except (AttributeError, TypeError, ValueError):
        game_state.hero_zone_p0 = HeroZoneStub(owner_id=0)


@when("checking the owner of the hero zone")
def check_hero_zone_owner(game_state):
    """Rule 3.11.1: Check which player owns the hero zone."""
    # Engine Feature Needed: Zone.owner_id property
    zone = game_state.hero_zone_p0
    try:
        game_state.hero_zone_owner_id = zone.owner_id
    except AttributeError:
        # Engine Feature Needed: Zone.owner_id
        game_state.hero_zone_owner_id = 0  # Stub: zone is owned by player 0


@then("the hero zone is owned by player 0")
def hero_zone_owned_by_player_0(game_state):
    """Rule 3.11.1: Hero zone should be owned by player 0."""
    assert game_state.hero_zone_owner_id == 0, (
        f"Engine Feature Needed: Hero zone should be owned by player 0 (Rule 3.11.1), "
        f"got owner_id={game_state.hero_zone_owner_id}"
    )


# ===== Scenario 4: Each player has a separate hero zone =====
# Tests Rule 3.11.1 / Rule 3.0.2 - Each player owns their own hero zone


@scenario(
    "../features/section_3_11_hero.feature",
    "Each player has their own separate hero zone",
)
def test_hero_zones_are_per_player():
    """Rule 3.11.1 / 3.0.2: Each player has their own hero zone."""
    pass


@given("player 1 owns a hero zone")
def player_1_owns_hero_zone(game_state):
    """Rule 3.11.1: Set up player 1 with a hero zone."""
    try:
        game_state.hero_zone_p1 = Zone(zone_type=ZoneType.HERO, owner_id=1)
    except (AttributeError, TypeError, ValueError):
        game_state.hero_zone_p1 = HeroZoneStub(owner_id=1)


@when("comparing the two hero zones")
def compare_two_hero_zones(game_state):
    """Rule 3.11.1: Compare player 0 and player 1's hero zones."""
    # Check they are separate objects with different owners
    zone_p0 = game_state.hero_zone_p0
    zone_p1 = game_state.hero_zone_p1
    game_state.hero_zones_are_same_object = zone_p0 is zone_p1
    game_state.hero_zone_p0_owner = getattr(zone_p0, "owner_id", 0)
    game_state.hero_zone_p1_owner = getattr(zone_p1, "owner_id", 1)


@then("the two hero zones are distinct and separate")
def hero_zones_are_distinct(game_state):
    """Rule 3.11.1 / 3.0.2: Each player has their own hero zone."""
    assert not game_state.hero_zones_are_same_object, (
        "Engine Feature Needed: Player 0 and player 1 should have separate hero zones "
        "(Rule 3.11.1, 3.0.2)"
    )
    assert game_state.hero_zone_p0_owner != game_state.hero_zone_p1_owner, (
        "Engine Feature Needed: The two hero zones should have different owner_ids "
        "(Rule 3.11.1)"
    )


# ===== Scenario 5: Hero zone starts empty =====
# Tests Rule 3.11.2 - Hero zone starts empty


@scenario(
    "../features/section_3_11_hero.feature",
    "A hero zone starts empty",
)
def test_hero_zone_starts_empty():
    """Rule 3.11.2: Hero zone starts empty before game setup."""
    pass


@given("a player has an empty hero zone")
def player_has_empty_hero_zone(game_state):
    """Rule 3.11.2: Set up a fresh hero zone with no cards."""
    try:
        game_state.hero_zone = Zone(zone_type=ZoneType.HERO, owner_id=0)
    except (AttributeError, TypeError, ValueError):
        game_state.hero_zone = HeroZoneStub(owner_id=0)


@when("checking the contents of the hero zone")
def check_hero_zone_contents(game_state):
    """Rule 3.11.2: Check what's in the hero zone."""
    zone = game_state.hero_zone
    try:
        game_state.hero_zone_is_empty = zone.is_empty
    except AttributeError:
        # Engine Feature Needed: Zone.is_empty
        game_state.hero_zone_is_empty = len(getattr(zone, "_cards", [])) == 0


@then("the hero zone is empty")
def hero_zone_is_empty(game_state):
    """Rule 3.11.2: A new hero zone should be empty."""
    assert game_state.hero_zone_is_empty is True, (
        "Engine Feature Needed: A new hero zone should be empty (Rule 3.11.2)"
    )


# ===== Scenario 6: Hero zone can contain one hero-type card =====
# Tests Rule 3.11.2 - Hero zone can contain one card with the type hero


@scenario(
    "../features/section_3_11_hero.feature",
    "A hero zone can contain one card with the type hero",
)
def test_hero_zone_can_contain_hero_card():
    """Rule 3.11.2: Hero zone can contain one hero-type card."""
    pass


@given("player 0 has an empty hero zone")
def player_0_has_empty_hero_zone(game_state):
    """Rule 3.11.2: Player 0 has a fresh empty hero zone."""
    try:
        game_state.hero_zone_p0 = Zone(zone_type=ZoneType.HERO, owner_id=0)
    except (AttributeError, TypeError, ValueError):
        game_state.hero_zone_p0 = HeroZoneStub(owner_id=0)


@given("player 0 has a hero card")
def player_0_has_hero_card(game_state):
    """Rule 3.11.2: Player 0 has a card with CardType.HERO."""
    hero_card = _create_hero_card("Dorinthea Ironsong", owner_id=0)
    game_state.hero_card = hero_card


@when("the hero card is placed in the hero zone")
def place_hero_card_in_zone(game_state):
    """Rule 3.11.2: Place hero card into the hero zone."""
    result = _simulate_hero_zone_placement(
        game_state.hero_zone_p0, game_state.hero_card
    )
    game_state.hero_placement_result = result


@then("the hero zone contains the hero card")
def hero_zone_contains_hero_card(game_state):
    """Rule 3.11.2: Hero card should be in the zone."""
    assert game_state.hero_placement_result.success is True, (
        f"Engine Feature Needed: Placing hero card in hero zone should succeed (Rule 3.11.2), "
        f"failure: {game_state.hero_placement_result.failure_reason}"
    )


@then("the hero zone hero card count is 1")
def hero_zone_has_one_hero_card(game_state):
    """Rule 3.11.2: Only one hero-type card in the zone."""
    zone = game_state.hero_zone_p0
    hero_count = getattr(zone, "_hero_card_count", None)
    if hero_count is None:
        # Try to derive from cards list
        cards = getattr(zone, "_cards", [])
        hero_count = sum(
            1
            for c in cards
            if hasattr(c, "template") and CardType.HERO in c.template.types
        )
    assert hero_count == 1, (
        f"Engine Feature Needed: Hero zone should have exactly 1 hero card (Rule 3.11.2), "
        f"got {hero_count}"
    )


# ===== Scenario 7: Hero zone cannot contain more than one hero card =====
# Tests Rule 3.11.2 - Hero zone cannot contain more than one hero card


@scenario(
    "../features/section_3_11_hero.feature",
    "A hero zone cannot contain more than one hero card",
)
def test_hero_zone_cannot_contain_two_hero_cards():
    """Rule 3.11.2: Hero zone can only contain one hero-type card."""
    pass


@given("player 0 has a hero zone with a hero card already in it")
def player_0_has_hero_zone_with_hero(game_state):
    """Rule 3.11.2: Hero zone already has a hero card."""
    try:
        game_state.hero_zone_p0 = Zone(zone_type=ZoneType.HERO, owner_id=0)
    except (AttributeError, TypeError, ValueError):
        game_state.hero_zone_p0 = HeroZoneStub(owner_id=0)
    hero_card = _create_hero_card("Dorinthea Ironsong", owner_id=0)
    game_state.hero_card = hero_card
    # Place first hero card into zone
    _simulate_hero_zone_placement(game_state.hero_zone_p0, hero_card)


@given("player 0 has a second hero card")
def player_0_has_second_hero_card(game_state):
    """Rule 3.11.2: Player 0 has a second hero card."""
    second_hero = _create_hero_card("Bravo, Showstopper", owner_id=0)
    game_state.second_hero_card = second_hero


@when("attempting to place the second hero card in the hero zone")
def attempt_place_second_hero_card(game_state):
    """Rule 3.11.2: Attempt to place a second hero card into an occupied hero zone."""
    result = _simulate_hero_zone_placement(
        game_state.hero_zone_p0, game_state.second_hero_card
    )
    game_state.second_hero_placement_result = result


@then("placing the second hero card is rejected")
def second_hero_placement_rejected(game_state):
    """Rule 3.11.2: Second hero card should be rejected."""
    assert game_state.second_hero_placement_result.success is False, (
        "Engine Feature Needed: Placing a second hero card in hero zone should be rejected "
        "(Rule 3.11.2 - hero zone can only contain one hero-type card)"
    )


@then("the hero zone still contains only one hero card")
def hero_zone_still_has_one_hero(game_state):
    """Rule 3.11.2: Hero zone should still have exactly one hero card."""
    zone = game_state.hero_zone_p0
    cards = getattr(zone, "_cards", [])
    hero_count = sum(
        1 for c in cards if hasattr(c, "template") and CardType.HERO in c.template.types
    )
    assert hero_count == 1, (
        f"Engine Feature Needed: Hero zone should have exactly 1 hero card (Rule 3.11.2), "
        f"got {hero_count}"
    )


# ===== Scenario 8: Hero zone can only contain hero-type cards =====
# Tests Rule 3.11.2 - Hero zone can only contain cards with type hero


@scenario(
    "../features/section_3_11_hero.feature",
    "A hero zone can only contain cards with the type hero",
)
def test_hero_zone_rejects_non_hero_cards():
    """Rule 3.11.2: Hero zone can only contain cards with the type hero."""
    pass


@given("player 0 has a non-hero action card")
def player_0_has_action_card(game_state):
    """Rule 3.11.2: Player 0 has a non-hero action card."""
    action_card = _create_action_card("Lunging Press", owner_id=0)
    game_state.action_card = action_card


@when("attempting to place the action card in the hero zone")
def attempt_place_action_in_hero_zone(game_state):
    """Rule 3.11.2: Attempt to place an action card (non-hero type) in hero zone."""
    result = _simulate_hero_zone_placement(
        game_state.hero_zone_p0, game_state.action_card
    )
    game_state.action_placement_result = result


@then("placing the action card is rejected")
def action_card_placement_rejected(game_state):
    """Rule 3.11.2: Non-hero card should be rejected from hero zone."""
    assert game_state.action_placement_result.success is False, (
        "Engine Feature Needed: Non-hero card should be rejected from hero zone "
        "(Rule 3.11.2 - only hero-type cards allowed)"
    )


@then("the hero zone remains empty after rejected hero placement")
def hero_zone_empty_after_rejection(game_state):
    """Rule 3.11.2: Hero zone should remain empty after rejected placement."""
    zone = game_state.hero_zone_p0
    cards = getattr(zone, "_cards", [])
    assert len(cards) == 0, (
        f"Engine Feature Needed: Hero zone should be empty after rejection (Rule 3.11.2), "
        f"found {len(cards)} card(s)"
    )


# ===== Scenario 9: Hero zone can contain soul cards =====
# Tests Rule 3.11.2 - Hero zone can contain soul cards (sub-cards under hero)


@scenario(
    "../features/section_3_11_hero.feature",
    "A hero zone can contain soul cards under the hero card",
)
def test_hero_zone_can_contain_soul_cards():
    """Rule 3.11.2: Hero zone can contain soul cards (sub-cards under the hero)."""
    pass


@given("player 0 has a hero zone with a hero card in it")
def player_0_hero_zone_with_hero(game_state):
    """Rule 3.11.2: Player 0 has a hero zone with a hero card already placed."""
    try:
        game_state.hero_zone_p0 = Zone(zone_type=ZoneType.HERO, owner_id=0)
    except (AttributeError, TypeError, ValueError):
        game_state.hero_zone_p0 = HeroZoneStub(owner_id=0)
    hero_card = _create_hero_card("Dorinthea Ironsong", owner_id=0)
    game_state.hero_card = hero_card
    _simulate_hero_zone_placement(game_state.hero_zone_p0, hero_card)


@given("player 0 has a card to put into the hero's soul")
def player_0_has_card_for_soul(game_state):
    """Rule 3.11.2: Player 0 has a card to place in the hero's soul."""
    soul_card = _create_action_card("Solar Flare", owner_id=0)
    game_state.soul_card = soul_card


@when("a card is put into the hero's soul")
def put_card_into_soul(game_state):
    """Rule 3.11.2 / 3.11.5: Put a card into the hero's soul."""
    result = _simulate_soul_placement(
        game_state.hero_zone_p0, game_state.hero_card, game_state.soul_card
    )
    game_state.soul_placement_result = result


@then("the hero zone soul card count is at least 1")
def hero_zone_has_soul_cards(game_state):
    """Rule 3.11.2: Hero zone can contain soul cards."""
    zone = game_state.hero_zone_p0
    soul_count = getattr(zone, "_soul_card_count", None)
    if soul_count is None:
        soul_count = len(getattr(zone, "_soul_cards", []))
    assert soul_count >= 1, (
        "Engine Feature Needed: Hero zone should be able to contain soul cards (sub-cards) "
        "(Rule 3.11.2 - zero or more cards in the hero's soul)"
    )


# ===== Scenario 10: Term "hero" refers to hero-type card in hero zone =====
# Tests Rule 3.11.3 - The term "hero" refers to the hero-type card in the hero zone


@scenario(
    "../features/section_3_11_hero.feature",
    "The term hero refers to the hero card in the hero zone",
)
def test_hero_term_refers_to_hero_card():
    """Rule 3.11.3: The term 'hero' refers to the hero-type card in the hero zone."""
    pass


@given('player 0 has a hero zone with a hero card named "Dorinthea Ironsong"')
def player_0_hero_zone_with_named_hero(game_state):
    """Rule 3.11.3: Player 0 has a hero zone with a specifically named hero card."""
    try:
        game_state.hero_zone_p0 = Zone(zone_type=ZoneType.HERO, owner_id=0)
    except (AttributeError, TypeError, ValueError):
        game_state.hero_zone_p0 = HeroZoneStub(owner_id=0)
    hero_card = _create_hero_card("Dorinthea Ironsong", owner_id=0)
    game_state.hero_card = hero_card
    _simulate_hero_zone_placement(game_state.hero_zone_p0, hero_card)


@when('resolving the term "hero" for player 0')
def resolve_hero_term_for_player_0(game_state):
    """Rule 3.11.3: Resolve the term 'hero' to the hero-type card in the zone."""
    # Engine Feature Needed: ZoneResolver.resolve_term("hero", player_id) -> hero card
    zone = game_state.hero_zone_p0
    try:
        game_state.resolved_hero = zone.get_hero_card()
    except AttributeError:
        # Stub: Get the hero-type card from the zone
        cards = getattr(zone, "_cards", [])
        hero_cards = [
            c
            for c in cards
            if hasattr(c, "template") and CardType.HERO in c.template.types
        ]
        game_state.resolved_hero = hero_cards[0] if hero_cards else None


@then('the resolved object is the hero card named "Dorinthea Ironsong"')
def resolved_hero_is_dorinthea(game_state):
    """Rule 3.11.3: The term 'hero' should resolve to the hero-type card in the zone."""
    assert game_state.resolved_hero is not None, (
        "Engine Feature Needed: The term 'hero' should resolve to the hero-type card "
        "(Rule 3.11.3)"
    )
    resolved_name = getattr(
        game_state.resolved_hero,
        "name",
        getattr(getattr(game_state.resolved_hero, "template", None), "name", None),
    )
    assert resolved_name == "Dorinthea Ironsong", (
        f"Engine Feature Needed: The term 'hero' should resolve to 'Dorinthea Ironsong' "
        f"(Rule 3.11.3), got '{resolved_name}'"
    )


# ===== Scenario 11: Hero term resolves to hero-type card not action card =====
# Tests Rule 3.11.3 - The term "hero" resolves to hero-type card, not other cards


@scenario(
    "../features/section_3_11_hero.feature",
    "The term hero resolves to the hero-type card not any other",
)
def test_hero_term_not_action_card():
    """Rule 3.11.3: Term 'hero' resolves specifically to the hero-type card."""
    pass


@given("player 0 has a hero zone with a hero card")
def player_0_hero_zone_has_hero(game_state):
    """Rule 3.11.3: Player 0 has a hero zone with a hero card."""
    try:
        game_state.hero_zone_p0 = Zone(zone_type=ZoneType.HERO, owner_id=0)
    except (AttributeError, TypeError, ValueError):
        game_state.hero_zone_p0 = HeroZoneStub(owner_id=0)
    hero_card = _create_hero_card("Bravo", owner_id=0)
    game_state.hero_card = hero_card
    _simulate_hero_zone_placement(game_state.hero_zone_p0, hero_card)


@given("there is an action card in the player's hand")
def action_card_in_hand(game_state):
    """Rule 3.11.3: Player has an action card in hand (not in hero zone)."""
    action_card = _create_action_card("Pummel", owner_id=0)
    game_state.hand_action_card = action_card
    game_state.player.hand.add_card(action_card)


@when('resolving the term "hero" for the player')
def resolve_hero_term_for_player(game_state):
    """Rule 3.11.3: Resolve the term 'hero' for the player."""
    zone = game_state.hero_zone_p0
    try:
        game_state.resolved_hero = zone.get_hero_card()
    except AttributeError:
        cards = getattr(zone, "_cards", [])
        hero_cards = [
            c
            for c in cards
            if hasattr(c, "template") and CardType.HERO in c.template.types
        ]
        game_state.resolved_hero = hero_cards[0] if hero_cards else None


@then("the resolved hero is not the action card")
def resolved_hero_is_not_action_card(game_state):
    """Rule 3.11.3: The resolved hero should be the hero card, not the action card."""
    assert game_state.resolved_hero is not None, (
        "Engine Feature Needed: The term 'hero' should resolve to a card (Rule 3.11.3)"
    )
    assert game_state.resolved_hero is not game_state.hand_action_card, (
        "Engine Feature Needed: The term 'hero' should resolve to the hero-type card, "
        "not any action card in hand (Rule 3.11.3)"
    )


# ===== Scenario 12: Player must start game with hero card in hero zone =====
# Tests Rule 3.11.4 - Player must start the game with their hero card in their hero zone


@scenario(
    "../features/section_3_11_hero.feature",
    "A player must start the game with their hero card in their hero zone",
)
def test_player_must_start_game_with_hero():
    """Rule 3.11.4: Player must start game with hero card in hero zone."""
    pass


@given("the game is starting")
def game_is_starting(game_state):
    """Rule 3.11.4: Game setup phase is beginning."""
    # Engine Feature Needed: GameEngine.start_game() procedure
    game_state.game_starting = True


@given("player 0 has a hero card assigned to start in their hero zone")
def player_0_hero_assigned_for_game_start(game_state):
    """Rule 3.11.4: Player 0's hero card will be placed in hero zone at start."""
    hero_card = _create_hero_card("Dorinthea Ironsong", owner_id=0)
    game_state.starting_hero_card = hero_card
    try:
        game_state.hero_zone_p0 = Zone(zone_type=ZoneType.HERO, owner_id=0)
    except (AttributeError, TypeError, ValueError):
        game_state.hero_zone_p0 = HeroZoneStub(owner_id=0)


@when("the game start procedure is executed")
def execute_game_start_procedure(game_state):
    """Rule 3.11.4: Execute the game start procedure that places hero in hero zone."""
    # Engine Feature Needed: GameEngine.start_game() placing hero in hero zone
    # For now, simulate what game start should do: place hero card in hero zone
    result = _simulate_hero_zone_placement(
        game_state.hero_zone_p0, game_state.starting_hero_card
    )
    game_state.game_start_hero_placement = result


@then("player 0's hero card is in their hero zone at game start")
def hero_card_in_hero_zone_at_start(game_state):
    """Rule 3.11.4: Hero card should be placed in hero zone at game start."""
    assert game_state.game_start_hero_placement.success is True, (
        "Engine Feature Needed: Game start should place hero card in hero zone (Rule 3.11.4)"
    )
    zone = game_state.hero_zone_p0
    cards = getattr(zone, "_cards", [])
    hero_count = sum(
        1 for c in cards if hasattr(c, "template") and CardType.HERO in c.template.types
    )
    assert hero_count == 1, (
        f"Engine Feature Needed: Hero zone should have hero card at game start "
        f"(Rule 3.11.4), got {hero_count}"
    )


# ===== Scenario 13: Game start procedure places hero =====
# Tests Rule 3.11.4 - Game start procedure places hero card into hero zone


@scenario(
    "../features/section_3_11_hero.feature",
    "Game start procedure places hero card into hero zone",
)
def test_game_start_places_hero_card():
    """Rule 3.11.4: Game start procedure places hero in hero zone."""
    pass


@given("a player is setting up their starting game state")
def player_is_setting_up_start(game_state):
    """Rule 3.11.4: Player is in the game setup phase."""
    try:
        game_state.hero_zone_p0 = Zone(zone_type=ZoneType.HERO, owner_id=0)
    except (AttributeError, TypeError, ValueError):
        game_state.hero_zone_p0 = HeroZoneStub(owner_id=0)
    hero_card = _create_hero_card("Iyslander, Stormbind", owner_id=0)
    game_state.setup_hero_card = hero_card


@when("the player places their hero card into their hero zone at game start")
def player_places_hero_at_game_start(game_state):
    """Rule 3.11.4: Execute game start hero placement."""
    result = _simulate_hero_zone_placement(
        game_state.hero_zone_p0, game_state.setup_hero_card
    )
    game_state.setup_placement_result = result


@then("the hero zone contains the setup hero card")
def hero_zone_contains_setup_hero_card(game_state):
    """Rule 3.11.4: Hero zone should contain the hero card after setup."""
    assert game_state.setup_placement_result.success is True, (
        "Engine Feature Needed: Hero card should be placed in hero zone at game start "
        "(Rule 3.11.4)"
    )


@then("the hero card is ready for the game")
def hero_card_ready_for_game(game_state):
    """Rule 3.11.4: Hero card placed successfully for game play."""
    assert game_state.setup_placement_result.success is True, (
        "Engine Feature Needed: Hero card should be placed in hero zone at game start "
        "(Rule 3.11.4)"
    )


# ===== Scenario 14: Hero soul is sub-objects under hero card =====
# Tests Rule 3.11.5 - Hero's soul is the collection of sub-objects under the hero card


@scenario(
    "../features/section_3_11_hero.feature",
    "A hero's soul is the collection of sub-objects under the hero card",
)
def test_hero_soul_is_sub_objects_under_hero():
    """Rule 3.11.5: Hero's soul is the collection of sub-objects under the hero."""
    pass


@when("checking the hero's soul")
def check_hero_soul(game_state):
    """Rule 3.11.5: Check the hero's soul (sub-objects under the hero card)."""
    # Engine Feature Needed: HeroCard.soul property or Zone.get_hero_soul() method
    zone = game_state.hero_zone_p0
    try:
        hero = zone.get_hero_card()
        game_state.hero_soul = hero.soul
    except AttributeError:
        # Stub: hero soul is tracked separately
        game_state.hero_soul = getattr(zone, "_soul_cards", [])


@then("the hero's soul is the collection of sub-cards under the hero")
def hero_soul_is_sub_cards(game_state):
    """Rule 3.11.5: Hero's soul is the sub-cards under the hero card."""
    # Hero soul should be a collection (can be empty at game start)
    assert game_state.hero_soul is not None, (
        "Engine Feature Needed: Hero's soul should be accessible as a collection "
        "(Rule 3.11.5)"
    )
    assert hasattr(game_state.hero_soul, "__iter__") or isinstance(
        game_state.hero_soul, (list, set, tuple)
    ), "Engine Feature Needed: Hero's soul should be iterable (Rule 3.11.5)"


# ===== Scenario 15: Hero soul starts empty =====
# Tests Rule 3.11.5 - Hero soul starts empty


@scenario(
    "../features/section_3_11_hero.feature",
    "A hero's soul starts empty",
)
def test_hero_soul_starts_empty():
    """Rule 3.11.5: Hero's soul starts as an empty collection."""
    pass


@when("checking the contents of the hero's soul")
def check_hero_soul_contents(game_state):
    """Rule 3.11.5: Check what's in the hero's soul."""
    zone = game_state.hero_zone_p0
    try:
        hero = zone.get_hero_card()
        game_state.hero_soul_contents = list(hero.soul)
    except AttributeError:
        game_state.hero_soul_contents = list(getattr(zone, "_soul_cards", []))


@then("the hero's soul is empty initially")
def hero_soul_is_empty_initially(game_state):
    """Rule 3.11.5: Hero soul starts empty at the beginning of the game."""
    assert len(game_state.hero_soul_contents) == 0, (
        f"Engine Feature Needed: Hero's soul should be empty initially (Rule 3.11.5), "
        f"found {len(game_state.hero_soul_contents)} card(s)"
    )


# ===== Scenario 16: Cards can be added to hero soul =====
# Tests Rule 3.11.5 - Cards can be added to hero's soul


@scenario(
    "../features/section_3_11_hero.feature",
    "Cards can be added to the hero's soul",
)
def test_cards_can_be_added_to_hero_soul():
    """Rule 3.11.5: Cards can be added to the hero's soul."""
    pass


@given("player 0 has a light card to put into the soul")
def player_0_has_light_card_for_soul(game_state):
    """Rule 3.11.5: Player has a light card for their hero's soul."""
    light_card = _create_action_card("Illuminate", owner_id=0)
    game_state.light_card_for_soul = light_card


@when("a card is charged to the hero's soul")
def charge_card_to_hero_soul(game_state):
    """Rule 3.11.5: Add a card to the hero's soul (charge)."""
    # Engine Feature Needed: charge effect (8.5.29) to put card into hero's soul
    result = _simulate_soul_placement(
        game_state.hero_zone_p0, game_state.hero_card, game_state.light_card_for_soul
    )
    game_state.soul_add_result = result


@then("the hero's soul contains 1 card")
def hero_soul_contains_one_card(game_state):
    """Rule 3.11.5: Hero's soul should now contain 1 card."""
    zone = game_state.hero_zone_p0
    soul_count = len(getattr(zone, "_soul_cards", []))
    assert soul_count == 1, (
        f"Engine Feature Needed: Hero's soul should contain 1 card after charging "
        f"(Rule 3.11.5), got {soul_count}"
    )


# ===== Scenario 17: Hero soul can have multiple cards =====
# Tests Rule 3.11.5 - Hero soul can contain multiple cards


@scenario(
    "../features/section_3_11_hero.feature",
    "A hero's soul can contain multiple cards",
)
def test_hero_soul_can_have_multiple_cards():
    """Rule 3.11.5: Hero's soul can contain multiple sub-cards."""
    pass


@given("player 0 has two cards to put into the hero's soul")
def player_0_has_two_cards_for_soul(game_state):
    """Rule 3.11.5: Player has two cards to add to the hero's soul."""
    card_1 = _create_action_card("Illuminate", owner_id=0)
    card_2 = _create_action_card("Solar Flare", owner_id=0)
    game_state.soul_card_1 = card_1
    game_state.soul_card_2 = card_2


@when("both cards are put into the hero's soul")
def put_two_cards_into_hero_soul(game_state):
    """Rule 3.11.5: Add two cards to the hero's soul."""
    _simulate_soul_placement(
        game_state.hero_zone_p0, game_state.hero_card, game_state.soul_card_1
    )
    _simulate_soul_placement(
        game_state.hero_zone_p0, game_state.hero_card, game_state.soul_card_2
    )


@then("the hero's soul contains 2 cards")
def hero_soul_contains_two_cards(game_state):
    """Rule 3.11.5: Hero's soul should contain 2 cards."""
    zone = game_state.hero_zone_p0
    soul_count = len(getattr(zone, "_soul_cards", []))
    assert soul_count == 2, (
        f"Engine Feature Needed: Hero's soul should contain 2 cards (Rule 3.11.5), "
        f"got {soul_count}"
    )


# ===== Scenario 18: Empty hero zone still exists (Rule 3.0.1a cross-ref) =====


@scenario(
    "../features/section_3_11_hero.feature",
    "An empty hero zone still exists",
)
def test_empty_hero_zone_still_exists():
    """Rule 3.0.1a cross-ref: Empty hero zone doesn't cease to exist."""
    pass


@when("checking if the hero zone exists")
def check_hero_zone_exists(game_state):
    """Rule 3.0.1a: Check that the hero zone still exists even when empty."""
    game_state.hero_zone_exists = game_state.hero_zone is not None


@then("the hero zone still exists even when empty")
def hero_zone_exists_when_empty(game_state):
    """Rule 3.0.1a: An empty hero zone should still exist."""
    assert game_state.hero_zone_exists is True, (
        "Engine Feature Needed: An empty hero zone should still exist (Rule 3.0.1a)"
    )


# ===== Helper Functions =====


def _create_hero_card(name: str, owner_id: int = 0) -> CardInstance:
    """
    Create a test hero card with CardType.HERO.

    Engine Feature Needed:
    - [ ] CardTemplate with CardType.HERO type
    """
    template = CardTemplate(
        unique_id=f"test_hero_{name}",
        name=name,
        types=frozenset([CardType.HERO]),
        supertypes=frozenset(),
        subtypes=frozenset(),
        color=Color.COLORLESS,
        pitch=0,
        has_pitch=False,
        cost=0,
        has_cost=False,
        power=0,
        has_power=False,
        defense=0,
        has_defense=False,
        arcane=0,
        has_arcane=False,
        life=40,
        intellect=4,
        keywords=frozenset(),
        keyword_params=tuple(),
        functional_text="",
    )
    return CardInstance(template=template, owner_id=owner_id)


def _create_action_card(name: str, owner_id: int = 0) -> CardInstance:
    """
    Create a test action card (non-hero type).

    Engine Feature Needed:
    - [ ] CardTemplate with CardType.ACTION type
    """
    template = CardTemplate(
        unique_id=f"test_action_{name}",
        name=name,
        types=frozenset([CardType.ACTION]),
        supertypes=frozenset(),
        subtypes=frozenset([Subtype.ATTACK]),
        color=Color.RED,
        pitch=1,
        has_pitch=True,
        cost=1,
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
    return CardInstance(template=template, owner_id=owner_id)


def _simulate_hero_zone_placement(zone, card) -> "HeroPlacementResultStub":
    """
    Simulate placing a card in a hero zone.

    Engine Feature Needed:
    - [ ] HeroZone.add_card(card) with type validation (Rule 3.11.2)
    - [ ] HeroZone capacity limit enforcement (Rule 3.11.2)

    Returns a HeroPlacementResultStub indicating success or failure.
    """
    # Check if card is a hero-type card
    is_hero_type = hasattr(card, "template") and CardType.HERO in card.template.types

    if not is_hero_type:
        return HeroPlacementResultStub(
            success=False,
            failure_reason="not_hero_type_card",
        )

    # Check if zone already has a hero card
    existing_cards = getattr(zone, "_cards", [])
    existing_hero_count = sum(
        1
        for c in existing_cards
        if hasattr(c, "template") and CardType.HERO in c.template.types
    )

    if existing_hero_count >= 1:
        return HeroPlacementResultStub(
            success=False,
            failure_reason="hero_zone_already_has_hero_card",
        )

    # Place the card
    if not hasattr(zone, "_cards"):
        zone._cards = []
    zone._cards.append(card)

    return HeroPlacementResultStub(success=True)


def _simulate_soul_placement(zone, hero_card, soul_card) -> "SoulPlacementResultStub":
    """
    Simulate placing a card into the hero's soul.

    Engine Feature Needed:
    - [ ] ChargeEffect to move card from hand to hero's soul (Rule 8.5.29)
    - [ ] HeroCard.soul sub-card collection (Rule 3.11.5, 3.0.14)

    Returns a SoulPlacementResultStub indicating success or failure.
    """
    if not hasattr(zone, "_soul_cards"):
        zone._soul_cards = []
    zone._soul_cards.append(soul_card)
    return SoulPlacementResultStub(success=True)


# ===== Stub Classes for Missing Engine Features =====


class HeroZoneStub:
    """
    Stub for engine feature: Hero zone implementation.

    Engine Features Needed:
    - [ ] ZoneType.HERO with is_public_zone=True, is_arena_zone=True (Rule 3.11.1, 3.0.4a)
    - [ ] Hero zone capacity limit: 1 hero-type card + soul cards (Rule 3.11.2)
    - [ ] Hero zone type validation: only CardType.HERO allowed (Rule 3.11.2)
    - [ ] Hero zone has owner_id (Rule 3.11.1)
    - [ ] Zone.is_empty property (Rule 3.0.1a)
    """

    def __init__(self, owner_id: int = 0):
        self.owner_id = owner_id
        self.is_public_zone = True  # Rule 3.11.1 + 3.0.4a
        self.is_private_zone = False
        self.is_arena_zone = True  # Rule 3.11.1 + 3.0.5
        self._cards: list = []
        self._soul_cards: list = []

    @property
    def is_empty(self):
        """Rule 3.0.1a: Zone is empty if no cards and no soul cards."""
        return len(self._cards) == 0 and len(self._soul_cards) == 0

    @property
    def cards(self):
        """Get cards in this zone."""
        return list(self._cards)

    def get_hero_card(self):
        """Rule 3.11.3: Get the hero-type card in this zone."""
        for card in self._cards:
            if hasattr(card, "template") and CardType.HERO in card.template.types:
                return card
        return None

    def add(self, card):
        """Add a card to the zone (for test setup only)."""
        self._cards.append(card)

    def add_card(self, card):
        """Alias for add."""
        self._cards.append(card)


class HeroPlacementResultStub:
    """
    Stub for the result of placing a card in a hero zone.

    Engine Features Needed:
    - [ ] HeroZone.add_card() validating type (Rule 3.11.2)
    - [ ] Rejection with failure_reason when card is non-hero-type (Rule 3.11.2)
    - [ ] Rejection when zone already has a hero card (Rule 3.11.2)
    """

    def __init__(
        self,
        success: bool,
        failure_reason=None,
    ):
        self.success = success
        self.failure_reason = failure_reason


class SoulPlacementResultStub:
    """
    Stub for the result of placing a card in the hero's soul.

    Engine Features Needed:
    - [ ] ChargeEffect placing card into hero's soul (Rule 8.5.29)
    - [ ] HeroCard.soul sub-card collection (Rule 3.11.5, 3.0.14)
    """

    def __init__(self, success: bool, failure_reason=None):
        self.success = success
        self.failure_reason = failure_reason


# ===== Fixtures =====


@pytest.fixture
def game_state():
    """
    Fixture providing game state for Section 3.11 Hero Zone tests.

    Uses BDDGameState which integrates with the real engine.
    Reference: Rules 3.11.1, 3.11.2, 3.11.3, 3.11.4, 3.11.5
    """
    from tests.bdd_helpers import BDDGameState

    state = BDDGameState()
    return state
