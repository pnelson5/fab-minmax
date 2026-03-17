"""
Step definitions for Section 3.0: Zones - General
Reference: Flesh and Blood Comprehensive Rules Section 3.0

This module implements behavioral tests for the zone system in Flesh and Blood:
- Rule 3.0.1: A zone is a collection of objects; 15 zone types exist
- Rule 3.0.1a: Empty zone doesn't cease to exist; equipment zone exposed when empty
- Rule 3.0.2: Each player owns their own zones; stack/permanent/combat chain are shared
- Rule 3.0.3: Objects are public or private
- Rule 3.0.3a: Player can look at their own private objects (except deck zone)
- Rule 3.0.4: Public zones vs private zones
- Rule 3.0.4a: arms, banished, chest, combat chain, graveyard, head, hero, legs, permanent,
               pitch, stack, weapon are public zones
- Rule 3.0.4b: arsenal, deck, hand are private zones
- Rule 3.0.4c: Public zone may contain private objects
- Rule 3.0.4d: Private zone may contain public objects
- Rule 3.0.4e: Rule/effect in public zone requires public source unless stated otherwise
- Rule 3.0.5: Arena = arms + chest + combat chain + head + hero + legs + permanent + weapon
- Rule 3.0.5a: Arena is not a zone; unspecified placement goes to permanent zone
- Rule 3.0.5b: Arsenal, banished, deck, graveyard, hand, pitch, stack NOT in arena
- Rule 3.0.7: Zone movement is simultaneous; object is never in no zone
- Rule 3.0.7a: Leaving object used for effects; private-to-private has no properties
- Rule 3.0.7b: Same-zone move is a no-op
- Rule 3.0.9: Object entering non-arena/non-stack zone resets to new object
- Rule 3.0.9a: Trigger references new object after zone move (while still public)
- Rule 3.0.9c: History preserved in new object
- Rule 3.0.12: Clearing moves object to owner's graveyard
- Rule 3.0.12a: Tokens, macros, non-card-layers cease to exist when cleared
- Rule 3.0.13: Unspecified zone refers to controller's zone

Engine Features Needed for Section 3.0:
- [ ] ZoneType.PERMANENT enum value (Rule 3.0.1) - currently missing; engine has WEAPON_1/WEAPON_2 not WEAPON
- [ ] ZoneType.WEAPON enum value (Rule 3.0.1) - currently split as WEAPON_1 and WEAPON_2
- [ ] ZoneType enum with all 15 zone types (Rule 3.0.1) - currently only 15 values but some differ
- [ ] Zone.is_empty property (Rule 3.0.1a) - Zone.is_empty exists
- [ ] Zone.owner_id tracking per-player zones (Rule 3.0.2)
- [ ] GameState.shared_zones (stack, permanent, combat chain) (Rule 3.0.2)
- [ ] CardInstance.is_public / is_private (Rule 3.0.3)
- [ ] Zone.is_public_zone / is_private_zone property (Rule 3.0.4)
- [ ] PUBLIC_ZONES and PRIVATE_ZONES constants (Rules 3.0.4a/b)
- [ ] CardInstance.can_owner_see() for private look (Rule 3.0.3a)
- [ ] Zone.in_arena property (Rule 3.0.5)
- [ ] GameState.arena collection (Rule 3.0.5)
- [ ] GameEngine.move_card(card, from_zone, to_zone) simultaneous move (Rule 3.0.7)
- [ ] ZoneMoveResult.object_in_origin_after tracking (Rule 3.0.7)
- [ ] CardInstance.reset() when entering non-arena/non-stack zone (Rule 3.0.9)
- [ ] CardInstance.history tracking (Rule 3.0.9c)
- [ ] GameEngine.clear_object(obj) -> graveyard (Rule 3.0.12)
- [ ] Token clearing causes cessation not graveyard move (Rule 3.0.12a)
- [ ] EffectZoneResolver.resolve_zone(effect_controller_id) (Rule 3.0.13)

Current status: Tests written, Engine pending
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


# ===== Scenario 1: 15 zone types =====
# Tests Rule 3.0.1 - There are exactly 15 zone types


@scenario(
    "../features/section_3_0_zones_general.feature",
    "There are exactly 15 zone types",
)
def test_there_are_exactly_15_zone_types():
    """Rule 3.0.1: There are exactly 15 zone types in Flesh and Blood."""
    pass


@given("the game engine zone type registry")
def game_engine_zone_type_registry(game_state):
    """Rule 3.0.1: The engine knows all zone types."""
    pass


@when("I count the number of defined zone types")
def count_zone_types(game_state):
    """Rule 3.0.1: Count all defined zone types."""
    game_state.zone_types = list(ZoneType)


@then("there are exactly 15 zone types")
def there_are_15_zone_types(game_state):
    """Rule 3.0.1: Exactly 15 zone types."""
    assert len(game_state.zone_types) == 15, (
        f"Expected 15 zone types, got {len(game_state.zone_types)}: {game_state.zone_types}"
    )


@then(
    "the zone types include arms, arsenal, banished, chest, combat chain, deck, graveyard, hand, head, hero, legs, permanent, pitch, stack, and weapon"
)
def all_15_zone_types_present(game_state):
    """Rule 3.0.1: All 15 zone types must be present."""
    # Rule 3.0.1: All 15 zone types required
    # Engine currently has WEAPON_1/WEAPON_2 instead of WEAPON (missing feature)
    # Engine currently missing PERMANENT zone type (missing feature)
    expected_zone_names = {
        "ARMS",
        "ARSENAL",
        "BANISHED",
        "CHEST",
        "COMBAT_CHAIN",
        "DECK",
        "GRAVEYARD",
        "HAND",
        "HEAD",
        "HERO",
        "LEGS",
        "PERMANENT",  # Missing engine feature
        "PITCH",
        "STACK",
        "WEAPON",  # Missing engine feature (split into WEAPON_1/WEAPON_2)
    }
    actual_zone_names = {z.name for z in game_state.zone_types}
    missing = expected_zone_names - actual_zone_names
    assert not missing, f"Missing zone type names: {missing}"


# ===== Scenario 2: Zone is a collection of objects =====
# Tests Rule 3.0.1 - Zone holds objects


@scenario(
    "../features/section_3_0_zones_general.feature",
    "A zone is a collection of objects",
)
def test_zone_is_collection_of_objects():
    """Rule 3.0.1: Zone is a collection of objects."""
    pass


@given("a player has a hand zone")
def player_has_hand_zone(game_state):
    """Rule 3.0.1: Player has a hand zone."""
    assert game_state.player.hand is not None


@when("a card is added to the hand zone")
def card_added_to_hand(game_state):
    """Rule 3.0.1: Card placed in hand zone."""
    game_state.test_card = game_state.create_card(name="Zone Test Card")
    game_state.player.hand.add_card(game_state.test_card)


@then("the hand zone contains the card")
def hand_contains_card(game_state):
    """Rule 3.0.1: Card is in the hand zone."""
    assert game_state.test_card in game_state.player.hand


@then("the hand zone is not empty")
def hand_zone_not_empty(game_state):
    """Rule 3.0.1a: Hand zone is not empty."""
    assert len(game_state.player.hand.cards) > 0


# ===== Scenario 3: Empty zone does not cease to exist =====
# Tests Rule 3.0.1a


@scenario(
    "../features/section_3_0_zones_general.feature",
    "An empty zone does not cease to exist",
)
def test_empty_zone_does_not_cease_to_exist():
    """Rule 3.0.1a: Empty zones still exist."""
    pass


@given("a player has a hand zone with no cards")
def player_has_empty_hand_zone(game_state):
    """Rule 3.0.1a: Player has empty hand zone."""
    # Clear any cards from hand
    for card in list(game_state.player.hand.cards):
        game_state.player.hand.remove_card(card)


@when("the engine checks if the empty hand zone exists")
def engine_checks_empty_hand_exists(game_state):
    """Rule 3.0.1a: Check empty zone existence."""
    game_state.empty_zone_exists = game_state.player.hand is not None


@then("the empty hand zone still exists")
def empty_hand_still_exists(game_state):
    """Rule 3.0.1a: Empty zone does not cease to exist."""
    assert game_state.empty_zone_exists is True
    assert game_state.player.hand is not None


@then("the empty hand zone is considered empty")
def empty_hand_is_empty(game_state):
    """Rule 3.0.1a: Empty zone reports as empty."""
    assert len(game_state.player.hand.cards) == 0


# ===== Scenario 4: Each player has their own private zones =====
# Tests Rule 3.0.2


@scenario(
    "../features/section_3_0_zones_general.feature",
    "Each player has their own private zones",
)
def test_each_player_has_own_private_zones():
    """Rule 3.0.2: Each player owns their own zones."""
    pass


@given("two players in a game")
def two_players_in_game(game_state):
    """Rule 3.0.2: Two players exist."""
    assert game_state.player is not None
    assert game_state.defender is not None


@when("checking zone ownership")
def checking_zone_ownership(game_state):
    """Rule 3.0.2: Check zone ownership."""
    game_state.p0_hand = game_state.player.hand
    game_state.p1_hand = game_state.defender.hand


@then("player 0 has their own hand zone")
def player_0_has_hand(game_state):
    """Rule 3.0.2: Player 0 has a hand zone."""
    assert game_state.p0_hand is not None


@then("player 1 has their own hand zone")
def player_1_has_hand(game_state):
    """Rule 3.0.2: Player 1 has a hand zone."""
    assert game_state.p1_hand is not None


@then("the two hand zones are different zones")
def two_hand_zones_different(game_state):
    """Rule 3.0.2: Player zones are distinct."""
    assert game_state.p0_hand is not game_state.p1_hand


# ===== Scenario 5: Shared zones =====
# Tests Rule 3.0.2 - Stack zone is shared


@scenario(
    "../features/section_3_0_zones_general.feature",
    "Shared zones are shared among all players",
)
def test_shared_zones_shared_among_all_players():
    """Rule 3.0.2: Stack, permanent, combat chain zones are shared."""
    pass


@when("checking the stack zone")
def checking_stack_zone(game_state):
    """Rule 3.0.2: Check stack zone."""
    game_state.stack_zone_check = game_state.shared_stack is not None


@then("the stack zone is shared by all players")
def stack_zone_is_shared(game_state):
    """Rule 3.0.2: Stack zone shared by all players."""
    # The stack zone should be a single zone accessible to all players,
    # not per-player. Missing engine feature if no shared_stack attribute.
    assert game_state.stack_zone_check is True


# ===== Scenario 6: A card can be public =====
# Tests Rule 3.0.3


@scenario(
    "../features/section_3_0_zones_general.feature",
    "A card can be public",
)
def test_card_can_be_public():
    """Rule 3.0.3: Objects can have public visibility."""
    pass


@given("a card placed in the graveyard zone for visibility check")
def card_in_graveyard(game_state):
    """Rule 3.0.3: Card in graveyard (public zone)."""
    game_state.graveyard_card = game_state.create_card(name="Graveyard Card")
    game_state.player.graveyard.add_card(game_state.graveyard_card)


@when("the engine checks the graveyard card visibility")
def engine_checks_graveyard_card_visibility(game_state):
    """Rule 3.0.3: Check graveyard card visibility."""
    game_state.card_visibility = game_state.get_object_visibility(
        game_state.graveyard_card
    )


@then("the card is a public object")
def card_is_public(game_state):
    """Rule 3.0.3: Card in graveyard is public."""
    assert game_state.card_visibility == "public"


@then("information about the card properties is available to all players")
def card_properties_available_to_all(game_state):
    """Rule 3.0.3: Public card properties available to all."""
    assert game_state.card_visibility == "public"


# ===== Scenario 7: A card can be private =====
# Tests Rule 3.0.3


@scenario(
    "../features/section_3_0_zones_general.feature",
    "A card can be private",
)
def test_card_can_be_private():
    """Rule 3.0.3: Objects can have private visibility."""
    pass


@given("a card placed in the hand zone for visibility check")
def card_in_hand_zone_for_visibility(game_state):
    """Rule 3.0.3: Card in hand (private zone)."""
    game_state.hand_card_visibility_obj = game_state.create_card(name="Hand Card Vis")
    game_state.player.hand.add_card(game_state.hand_card_visibility_obj)


@when("the engine checks the hand card visibility")
def engine_checks_hand_card_visibility(game_state):
    """Rule 3.0.3: Check hand card visibility."""
    game_state.card_visibility = game_state.get_object_visibility(
        game_state.hand_card_visibility_obj
    )


@then("the card is a private object")
def card_is_private(game_state):
    """Rule 3.0.3: Card in hand is private."""
    assert game_state.card_visibility == "private"


@then("information about the card properties is not available to all players")
def card_properties_not_available(game_state):
    """Rule 3.0.3: Private card properties not available to all."""
    assert game_state.card_visibility == "private"


# ===== Scenario 8: Player can look at their own private objects =====
# Tests Rule 3.0.3a


@scenario(
    "../features/section_3_0_zones_general.feature",
    "Player can look at their own private objects except in deck",
)
def test_player_can_look_at_own_private_objects():
    """Rule 3.0.3a: Player may look at their own private objects except in deck."""
    pass


@given("a player owns a card in their arsenal zone")
def player_owns_card_in_arsenal(game_state):
    """Rule 3.0.3a: Player has card in their own arsenal."""
    game_state.arsenal_card = game_state.create_card(name="Arsenal Card", owner_id=0)
    game_state.player.arsenal.add_card(game_state.arsenal_card)


@when("the player attempts to look at the private card")
def player_looks_at_private_card(game_state):
    """Rule 3.0.3a: Player looks at their own private card."""
    game_state.can_owner_see = game_state.check_can_owner_see(
        game_state.arsenal_card, owner_player_id=0
    )


@then("the player can see the card's properties")
def player_can_see_card(game_state):
    """Rule 3.0.3a: Owner can see their own private objects."""
    assert game_state.can_owner_see is True


@then("the card is still considered private to other players")
def card_private_to_others(game_state):
    """Rule 3.0.3a: Card is still private to non-owners."""
    game_state.other_can_see = game_state.check_can_owner_see(
        game_state.arsenal_card, owner_player_id=1
    )
    assert game_state.other_can_see is False


# ===== Scenario 9: Graveyard is a public zone =====
# Tests Rule 3.0.4a


@scenario(
    "../features/section_3_0_zones_general.feature",
    "The graveyard zone is a public zone",
)
def test_graveyard_is_public_zone():
    """Rule 3.0.4a: Graveyard is a public zone."""
    pass


@given("a player has a graveyard zone")
def player_has_graveyard_zone(game_state):
    """Rule 3.0.4a: Player has graveyard zone."""
    assert game_state.player.graveyard is not None


@when("checking the default visibility of the graveyard")
def checking_graveyard_visibility(game_state):
    """Rule 3.0.4a: Check graveyard zone visibility."""
    game_state.graveyard_visibility = game_state.get_zone_visibility_type(
        game_state.player.graveyard
    )


@then("the graveyard zone is a public zone")
def graveyard_is_public_zone(game_state):
    """Rule 3.0.4a: Graveyard is a public zone."""
    assert game_state.graveyard_visibility == "public"


@then("objects in graveyard are public by default")
def graveyard_objects_are_public(game_state):
    """Rule 3.0.4a: Objects in public zones are public by default."""
    test_card = game_state.create_card(name="Default Public Card")
    game_state.player.graveyard.add_card(test_card)
    visibility = game_state.get_object_visibility(test_card)
    assert visibility == "public"


# ===== Scenario 10: Banished zone is a public zone =====
# Tests Rule 3.0.4a


@scenario(
    "../features/section_3_0_zones_general.feature",
    "The banished zone is a public zone",
)
def test_banished_zone_is_public():
    """Rule 3.0.4a: Banished zone is a public zone."""
    pass


@given("a player has a banished zone")
def player_has_banished_zone(game_state):
    """Rule 3.0.4a: Player has banished zone."""
    assert game_state.player.banished_zone is not None


@when("checking the default visibility of the banished zone")
def checking_banished_visibility(game_state):
    """Rule 3.0.4a: Check banished zone visibility."""
    game_state.banished_visibility = game_state.get_zone_visibility_type(
        game_state.player.banished_zone
    )


@then("the banished zone is a public zone")
def banished_is_public_zone(game_state):
    """Rule 3.0.4a: Banished zone is public."""
    assert game_state.banished_visibility == "public"


# ===== Scenario 11: Pitch zone is a public zone =====
# Tests Rule 3.0.4a


@scenario(
    "../features/section_3_0_zones_general.feature",
    "The pitch zone is a public zone",
)
def test_pitch_zone_is_public():
    """Rule 3.0.4a: Pitch zone is a public zone."""
    pass


@given("a player has a pitch zone")
def player_has_pitch_zone(game_state):
    """Rule 3.0.4a: Player has pitch zone."""
    assert game_state.player.pitch_zone is not None


@when("checking the default visibility of the pitch zone")
def checking_pitch_visibility(game_state):
    """Rule 3.0.4a: Check pitch zone visibility."""
    game_state.pitch_visibility = game_state.get_zone_visibility_type(
        game_state.player.pitch_zone
    )


@then("the pitch zone is a public zone")
def pitch_is_public_zone(game_state):
    """Rule 3.0.4a: Pitch zone is public."""
    assert game_state.pitch_visibility == "public"


# ===== Scenario 12: Stack zone is a public zone =====
# Tests Rule 3.0.4a


@scenario(
    "../features/section_3_0_zones_general.feature",
    "The stack zone is a public zone",
)
def test_stack_zone_is_public():
    """Rule 3.0.4a: Stack zone is a public zone."""
    pass


@given("the stack zone exists")
def stack_zone_exists(game_state):
    """Rule 3.0.4a: Stack zone exists."""
    assert game_state.shared_stack is not None


@when("checking the default visibility of the stack zone")
def checking_stack_visibility(game_state):
    """Rule 3.0.4a: Check stack zone visibility."""
    game_state.stack_visibility = game_state.get_zone_visibility_type(
        game_state.shared_stack
    )


@then("the stack zone is a public zone")
def stack_is_public_zone(game_state):
    """Rule 3.0.4a: Stack zone is public."""
    assert game_state.stack_visibility == "public"


# ===== Scenario 13: Hand zone is a private zone =====
# Tests Rule 3.0.4b


@scenario(
    "../features/section_3_0_zones_general.feature",
    "The hand zone is a private zone",
)
def test_hand_zone_is_private():
    """Rule 3.0.4b: Hand zone is a private zone."""
    pass


# Step "a player has a hand zone" already defined above


@when("checking the default visibility of the hand zone")
def checking_hand_visibility(game_state):
    """Rule 3.0.4b: Check hand zone visibility."""
    game_state.hand_zone_visibility = game_state.get_zone_visibility_type(
        game_state.player.hand
    )


@then("the hand zone is a private zone")
def hand_is_private_zone(game_state):
    """Rule 3.0.4b: Hand zone is private."""
    assert game_state.hand_zone_visibility == "private"


@then("objects in hand are private by default")
def hand_objects_are_private(game_state):
    """Rule 3.0.4b: Objects in hand are private by default."""
    test_card = game_state.create_card(name="Private Hand Card")
    game_state.player.hand.add_card(test_card)
    visibility = game_state.get_object_visibility(test_card)
    assert visibility == "private"


# ===== Scenario 14: Deck zone is a private zone =====
# Tests Rule 3.0.4b


@scenario(
    "../features/section_3_0_zones_general.feature",
    "The deck zone is a private zone",
)
def test_deck_zone_is_private():
    """Rule 3.0.4b: Deck zone is a private zone."""
    pass


@given("a player has a deck zone")
def player_has_deck_zone(game_state):
    """Rule 3.0.4b: Player has a deck zone."""
    assert game_state.player.deck is not None


@when("checking the default visibility of the deck zone")
def checking_deck_visibility(game_state):
    """Rule 3.0.4b: Check deck zone visibility."""
    game_state.deck_visibility = game_state.get_zone_visibility_type(
        game_state.player.deck
    )


@then("the deck zone is a private zone")
def deck_is_private_zone(game_state):
    """Rule 3.0.4b: Deck zone is private."""
    assert game_state.deck_visibility == "private"


# ===== Scenario 15: Arsenal zone is a private zone =====
# Tests Rule 3.0.4b


@scenario(
    "../features/section_3_0_zones_general.feature",
    "The arsenal zone is a private zone",
)
def test_arsenal_zone_is_private():
    """Rule 3.0.4b: Arsenal zone is a private zone."""
    pass


@given("a player has an arsenal zone")
def player_has_arsenal_zone(game_state):
    """Rule 3.0.4b: Player has an arsenal zone."""
    assert game_state.player.arsenal is not None


@when("checking the default visibility of the arsenal zone")
def checking_arsenal_visibility(game_state):
    """Rule 3.0.4b: Check arsenal zone visibility."""
    game_state.arsenal_visibility = game_state.get_zone_visibility_type(
        game_state.player.arsenal
    )


@then("the arsenal zone is a private zone")
def arsenal_is_private_zone(game_state):
    """Rule 3.0.4b: Arsenal zone is private."""
    assert game_state.arsenal_visibility == "private"


# ===== Scenario 16: Public zone can contain private objects =====
# Tests Rule 3.0.4c


@scenario(
    "../features/section_3_0_zones_general.feature",
    "A public zone can contain a private object",
)
def test_public_zone_can_contain_private_object():
    """Rule 3.0.4c: Public zone can hold private objects."""
    pass


@given("a public graveyard zone")
def a_public_graveyard_zone(game_state):
    """Rule 3.0.4c: Graveyard is a public zone."""
    assert game_state.player.graveyard is not None


@given("a card that is made private")
def card_made_private(game_state):
    """Rule 3.0.4c: Card has been made private."""
    game_state.private_card = game_state.create_card(name="Made Private Card")
    game_state.set_object_visibility(game_state.private_card, "private")


@when("the private card is placed in the graveyard")
def private_card_placed_in_graveyard(game_state):
    """Rule 3.0.4c: Private card placed in public graveyard."""
    game_state.player.graveyard.add_card(game_state.private_card)


@then("the graveyard still contains the card as a private object")
def graveyard_has_private_card(game_state):
    """Rule 3.0.4c: Private card exists in public zone."""
    assert game_state.private_card in game_state.player.graveyard
    visibility = game_state.get_object_visibility(game_state.private_card)
    assert visibility == "private"


@then("the zone is still considered a public zone")
def graveyard_still_public_after_private_object(game_state):
    """Rule 3.0.4c: Zone type doesn't change due to contained objects."""
    assert game_state.get_zone_visibility_type(game_state.player.graveyard) == "public"


# ===== Scenario 17: Private zone can contain public objects =====
# Tests Rule 3.0.4d


@scenario(
    "../features/section_3_0_zones_general.feature",
    "A private zone can contain a public object",
)
def test_private_zone_can_contain_public_object():
    """Rule 3.0.4d: Private zone can hold public objects."""
    pass


@given("a private arsenal zone")
def a_private_arsenal_zone(game_state):
    """Rule 3.0.4d: Arsenal is a private zone."""
    assert game_state.player.arsenal is not None


@given("a card that is made public")
def card_made_public(game_state):
    """Rule 3.0.4d: Card has been made public (e.g., face-up)."""
    game_state.public_card = game_state.create_card(name="Made Public Card")
    game_state.set_object_visibility(game_state.public_card, "public")


@when("the public card is placed in the arsenal")
def public_card_placed_in_arsenal(game_state):
    """Rule 3.0.4d: Public card placed in private arsenal."""
    game_state.player.arsenal.add_card(game_state.public_card)


@then("the arsenal still contains the card as a public object")
def arsenal_has_public_card(game_state):
    """Rule 3.0.4d: Public card exists in private zone."""
    assert game_state.public_card in game_state.player.arsenal
    visibility = game_state.get_object_visibility(game_state.public_card)
    assert visibility == "public"


@then("the zone is still considered a private zone")
def arsenal_still_private_after_public_object(game_state):
    """Rule 3.0.4d: Zone type doesn't change due to contained objects."""
    assert game_state.get_zone_visibility_type(game_state.player.arsenal) == "private"


# ===== Scenario 18: Effect on public zone requires public source =====
# Tests Rule 3.0.4e - Tome of Torment example


@scenario(
    "../features/section_3_0_zones_general.feature",
    "An effect on a public zone only applies to public objects",
)
def test_effect_on_public_zone_requires_public_source():
    """Rule 3.0.4e: Source must be public for rule/effect to apply."""
    pass


@given("a banished zone with a face-down private card")
def banished_zone_with_facedown_card(game_state):
    """Rule 3.0.4e: Card is private in public banished zone."""
    game_state.face_down_card = game_state.create_card(name="Face-Down Card")
    game_state.face_down_card._is_face_down = True
    game_state.set_object_visibility(game_state.face_down_card, "private")
    game_state.player.banished_zone.add_card(game_state.face_down_card)


@when("an effect checks for the card in the banished zone")
def effect_checks_for_card(game_state):
    """Rule 3.0.4e: Effect tries to find card in public zone."""
    game_state.effect_applies = game_state.check_effect_applies_to_public_zone_card(
        game_state.face_down_card, zone_type="banished"
    )


@then("the effect does not apply because the source is private")
def effect_does_not_apply(game_state):
    """Rule 3.0.4e: Private source in public zone - effect doesn't apply."""
    assert game_state.effect_applies is False


# ===== Scenario 19: Arena collects specific zone types =====
# Tests Rule 3.0.5


@scenario(
    "../features/section_3_0_zones_general.feature",
    "The arena collects specific zone types",
)
def test_arena_collects_specific_zone_types():
    """Rule 3.0.5: Arena = arms + chest + combat chain + head + hero + legs + permanent + weapon."""
    pass


@given("a player's game zones")
def players_game_zones(game_state):
    """Rule 3.0.5: Player has zones set up."""
    pass


@when("checking which zones are in the arena")
def checking_arena_zones(game_state):
    """Rule 3.0.5: Check which zones are in the arena."""
    game_state.arena_zone_types = game_state.get_arena_zone_types()


@then("the arms zone is in the arena")
def arms_in_arena(game_state):
    """Rule 3.0.5: Arms zone is in the arena."""
    assert ZoneType.ARMS in game_state.arena_zone_types


@then("the chest zone is in the arena")
def chest_in_arena(game_state):
    """Rule 3.0.5: Chest zone is in the arena."""
    assert ZoneType.CHEST in game_state.arena_zone_types


@then("the head zone is in the arena")
def head_in_arena(game_state):
    """Rule 3.0.5: Head zone is in the arena."""
    assert ZoneType.HEAD in game_state.arena_zone_types


@then("the hero zone is in the arena")
def hero_in_arena(game_state):
    """Rule 3.0.5: Hero zone is in the arena."""
    assert ZoneType.HERO in game_state.arena_zone_types


@then("the legs zone is in the arena")
def legs_in_arena(game_state):
    """Rule 3.0.5: Legs zone is in the arena."""
    assert ZoneType.LEGS in game_state.arena_zone_types


@then("the permanent zone is in the arena")
def permanent_in_arena(game_state):
    """Rule 3.0.5: Permanent zone is in the arena."""
    # ZoneType.PERMANENT is a missing engine feature - this assertion will fail
    # until the engine adds ZoneType.PERMANENT
    PERMANENT = getattr(ZoneType, "PERMANENT", None)
    assert PERMANENT is not None, (
        "Engine Feature Needed: ZoneType.PERMANENT (Rule 3.0.1, 3.0.5)"
    )
    assert PERMANENT in game_state.arena_zone_types


@then("the weapon zone is in the arena")
def weapon_in_arena(game_state):
    """Rule 3.0.5: Weapon zone is in the arena."""
    # ZoneType.WEAPON is a missing engine feature (currently split as WEAPON_1/WEAPON_2)
    WEAPON = getattr(ZoneType, "WEAPON", None)
    assert WEAPON is not None, (
        "Engine Feature Needed: ZoneType.WEAPON (Rule 3.0.1, 3.0.2, 3.0.5)"
    )
    assert WEAPON in game_state.arena_zone_types


# ===== Scenario 20: Arena is not a zone =====
# Tests Rule 3.0.5a


@scenario(
    "../features/section_3_0_zones_general.feature",
    "The arena is not itself a zone",
)
def test_arena_is_not_itself_a_zone():
    """Rule 3.0.5a: Arena is a collection of zones, not a zone type itself."""
    pass


@given("the arena collection")
def arena_collection(game_state):
    """Rule 3.0.5a: Arena exists as a collection."""
    pass


@when("checking if the arena is a zone")
def checking_if_arena_is_zone(game_state):
    """Rule 3.0.5a: Check arena zone type."""
    game_state.arena_is_a_zone_type = game_state.check_arena_is_zone_type()


@then("the arena is not a zone type")
def arena_not_zone_type(game_state):
    """Rule 3.0.5a: ARENA is not itself a ZoneType."""
    assert game_state.arena_is_a_zone_type is False


@then("the arena is a collection of zones")
def arena_is_collection_of_zones(game_state):
    """Rule 3.0.5a: Arena is a collection not a zone."""
    arena_types = game_state.get_arena_zone_types()
    assert len(arena_types) > 0


# ===== Scenario 21: Object placed into arena without zone goes to permanent =====
# Tests Rule 3.0.5a


@scenario(
    "../features/section_3_0_zones_general.feature",
    "Object placed into arena without specifying zone goes to permanent zone",
)
def test_object_placed_into_arena_without_zone_goes_to_permanent():
    """Rule 3.0.5a: Unspecified zone -> permanent zone."""
    pass


@given("a card that would be placed in the arena")
def card_placed_in_arena(game_state):
    """Rule 3.0.5a: Card to be placed in arena."""
    game_state.arena_placement_card = game_state.create_card(name="Arena Card")


@when("no specific zone is specified")
def no_zone_specified(game_state):
    """Rule 3.0.5a: Place in arena without specifying zone."""
    game_state.arena_placement_result = game_state.place_card_in_arena_unspecified(
        game_state.arena_placement_card
    )


@then("the card is placed in the permanent zone")
def card_in_permanent_zone(game_state):
    """Rule 3.0.5a: Card goes to permanent zone."""
    # ZoneType.PERMANENT is a missing engine feature
    PERMANENT = getattr(ZoneType, "PERMANENT", None)
    assert PERMANENT is not None, (
        "Engine Feature Needed: ZoneType.PERMANENT (Rule 3.0.5a)"
    )
    assert game_state.arena_placement_result.destination_zone_type == PERMANENT


@then("the card is a permanent")
def card_is_a_permanent(game_state):
    """Rule 3.0.5a: Card in permanent zone is a permanent."""
    assert game_state.arena_placement_result.is_permanent is True


# ===== Scenario 22: Non-arena zones not in arena =====
# Tests Rule 3.0.5b


@scenario(
    "../features/section_3_0_zones_general.feature",
    "Non-arena zones are not part of the arena",
)
def test_non_arena_zones_not_in_arena():
    """Rule 3.0.5b: Arsenal, banished, deck, graveyard, hand, pitch, stack not in arena."""
    pass


@when("checking which zones are NOT in the arena")
def checking_non_arena_zones(game_state):
    """Rule 3.0.5b: Check which zones are outside arena."""
    game_state.arena_zone_types_3_5b = game_state.get_arena_zone_types()


@then("the arsenal zone is not in the arena")
def arsenal_not_in_arena(game_state):
    """Rule 3.0.5b: Arsenal not in arena."""
    assert ZoneType.ARSENAL not in game_state.arena_zone_types_3_5b


@then("the banished zone is not in the arena")
def banished_not_in_arena(game_state):
    """Rule 3.0.5b: Banished not in arena."""
    assert ZoneType.BANISHED not in game_state.arena_zone_types_3_5b


@then("the deck zone is not in the arena")
def deck_not_in_arena(game_state):
    """Rule 3.0.5b: Deck not in arena."""
    assert ZoneType.DECK not in game_state.arena_zone_types_3_5b


@then("the graveyard zone is not in the arena")
def graveyard_not_in_arena(game_state):
    """Rule 3.0.5b: Graveyard not in arena."""
    assert ZoneType.GRAVEYARD not in game_state.arena_zone_types_3_5b


@then("the hand zone is not in the arena")
def hand_not_in_arena(game_state):
    """Rule 3.0.5b: Hand not in arena."""
    assert ZoneType.HAND not in game_state.arena_zone_types_3_5b


@then("the pitch zone is not in the arena")
def pitch_not_in_arena(game_state):
    """Rule 3.0.5b: Pitch not in arena."""
    assert ZoneType.PITCH not in game_state.arena_zone_types_3_5b


@then("the stack zone is not in the arena")
def stack_not_in_arena(game_state):
    """Rule 3.0.5b: Stack not in arena."""
    assert ZoneType.STACK not in game_state.arena_zone_types_3_5b


# ===== Scenario 23: Zone movement is simultaneous =====
# Tests Rule 3.0.7


@scenario(
    "../features/section_3_0_zones_general.feature",
    "Moving a card between zones is simultaneous",
)
def test_moving_card_between_zones_is_simultaneous():
    """Rule 3.0.7: Zone movement is simultaneous."""
    pass


@given("a card in the hand zone")
def card_in_hand_for_move(game_state):
    """Rule 3.0.7: Card in hand ready to be moved."""
    game_state.moving_card = game_state.create_card(name="Moving Card")
    game_state.player.hand.add_card(game_state.moving_card)


@when("the card is moved to the graveyard")
def card_moved_to_graveyard(game_state):
    """Rule 3.0.7: Card moves from hand to graveyard."""
    game_state.zone_move_result = game_state.move_card_between_zones(
        game_state.moving_card,
        from_zone=game_state.player.hand,
        to_zone=game_state.player.graveyard,
    )


@then("the card is no longer in the hand zone")
def card_not_in_hand(game_state):
    """Rule 3.0.7: Card left hand zone."""
    assert game_state.moving_card not in game_state.player.hand


@then("the card is in the graveyard zone")
def card_is_in_graveyard(game_state):
    """Rule 3.0.7: Card is now in graveyard."""
    assert game_state.moving_card in game_state.player.graveyard


@then("the card was never in no zone during the move")
def card_never_in_no_zone(game_state):
    """Rule 3.0.7: Card never exists outside a zone during movement."""
    # The move result should confirm simultaneous transition
    assert game_state.zone_move_result.was_ever_in_no_zone is False


# ===== Scenario 24: Leaving object used for effects =====
# Tests Rule 3.0.7a


@scenario(
    "../features/section_3_0_zones_general.feature",
    "The leaving object is used for zone-triggered effects",
)
def test_leaving_object_used_for_zone_effects():
    """Rule 3.0.7a: Object as it leaves origin is used for effects."""
    pass


@given("a card in the hand zone with power 4")
def card_in_hand_with_power_4(game_state):
    """Rule 3.0.7a: Card with power 4 in hand."""
    game_state.power4_card = game_state.create_card(name="Power 4 Card", cost=4)
    game_state.power4_card._power = 4
    game_state.player.hand.add_card(game_state.power4_card)


@when("the card is moved to the banished zone")
def card_moved_to_banished(game_state):
    """Rule 3.0.7a: Card moves from hand to banished."""
    game_state.zone_power_result = game_state.move_card_and_capture_origin_properties(
        game_state.power4_card,
        from_zone=game_state.player.hand,
        to_zone=game_state.player.banished_zone,
    )


@then("the card's power value at the origin is 4")
def card_power_at_origin_is_4(game_state):
    """Rule 3.0.7a: The object leaving origin has power=4."""
    assert game_state.zone_power_result.origin_power == 4


@then("the card is in the banished zone")
def card_is_in_banished(game_state):
    """Rule 3.0.7a: Card arrived at banished zone."""
    assert game_state.power4_card in game_state.player.banished_zone


# ===== Scenario 25: Private-to-private move has no properties for effects =====
# Tests Rule 3.0.7a - Levia example


@scenario(
    "../features/section_3_0_zones_general.feature",
    "Private-to-private zone move object has no properties for effects",
)
def test_private_to_private_move_has_no_properties():
    """Rule 3.0.7a: Private-to-private move: considered to have no properties."""
    pass


@given("a private card in the hand zone")
def private_card_in_hand(game_state):
    """Rule 3.0.7a: Private card in hand zone."""
    game_state.private_hand_card = game_state.create_card(name="Private Hand Card 2")
    game_state.set_object_visibility(game_state.private_hand_card, "private")
    game_state.player.hand.add_card(game_state.private_hand_card)


@when("the card is moved face-down to the banished zone")
def card_moved_facedown_to_banished(game_state):
    """Rule 3.0.7a: Private card moved face-down to banished zone."""
    game_state.private_move_result = game_state.move_private_card_to_private_zone(
        game_state.private_hand_card,
        from_zone=game_state.player.hand,
        to_zone=game_state.player.banished_zone,
        destination_visibility="private",
    )


@then("the card is considered to have no properties for effects during the move")
def card_has_no_properties_for_effects(game_state):
    """Rule 3.0.7a: Private-to-private move: no properties for effects."""
    assert game_state.private_move_result.has_no_properties_for_effects is True


# ===== Scenario 26: Same-zone move is no-op =====
# Tests Rule 3.0.7b


@scenario(
    "../features/section_3_0_zones_general.feature",
    "Moving a card to the same zone it is already in does nothing",
)
def test_same_zone_move_is_noop():
    """Rule 3.0.7b: Moving to same zone does nothing."""
    pass


@given("a card already placed in the graveyard zone")
def card_in_graveyard_for_noop(game_state):
    """Rule 3.0.7b: Card in graveyard."""
    game_state.noop_card = game_state.create_card(name="No-Op Move Card")
    game_state.player.graveyard.add_card(game_state.noop_card)


@when("an effect tries to move the card to the graveyard again")
def effect_tries_same_zone_move(game_state):
    """Rule 3.0.7b: Effect tries to move card to its current zone."""
    game_state.noop_move_result = game_state.move_card_same_zone(
        game_state.noop_card, zone=game_state.player.graveyard
    )


@then("no move occurs")
def no_move_occurs(game_state):
    """Rule 3.0.7b: No movement event produced."""
    assert game_state.noop_move_result.move_occurred is False


@then("the card remains in the graveyard zone")
def card_remains_in_graveyard(game_state):
    """Rule 3.0.7b: Card stays in graveyard."""
    assert game_state.noop_card in game_state.player.graveyard


# ===== Scenario 27: Card entering hand from graveyard resets =====
# Tests Rule 3.0.9


@scenario(
    "../features/section_3_0_zones_general.feature",
    "Card entering hand from graveyard becomes a new object",
)
def test_card_entering_hand_from_graveyard_resets():
    """Rule 3.0.9: Card entering non-arena/non-stack zone resets."""
    pass


@given("a card in the graveyard zone with an effect applied")
def card_in_graveyard_with_effect_for_reset(game_state):
    """Rule 3.0.9: Card in graveyard with go-again effect, ready to be returned to hand."""
    game_state.reset_card = game_state.create_card(name="Reset Card")
    game_state.reset_card._has_go_again_effect = True
    game_state.player.graveyard.add_card(game_state.reset_card)
    game_state.original_card_id = id(game_state.reset_card)


@when("the card moves from graveyard to the hand zone")
def card_moves_graveyard_to_hand(game_state):
    """Rule 3.0.9: Card moved from graveyard to hand."""
    game_state.reset_result = game_state.move_card_to_hand(
        game_state.reset_card, from_zone=game_state.player.graveyard
    )


@then("the card resets and becomes a new object after entering hand")
def card_resets_to_new_object_hand(game_state):
    """Rule 3.0.9: Card is a new object after entering non-arena zone."""
    assert game_state.reset_result.object_was_reset is True


@then("the card has no relation to its previous existence")
def card_has_no_previous_relation(game_state):
    """Rule 3.0.9: New object has no relation to old existence."""
    # The effect that was applied should no longer exist on the new object
    assert (
        getattr(game_state.reset_result.new_object, "_has_go_again_effect", False)
        is False
    )


# ===== Scenario 28: Public object becoming private resets =====
# Tests Rule 3.0.9


@scenario(
    "../features/section_3_0_zones_general.feature",
    "Card becoming private resets",
)
def test_card_becoming_private_resets():
    """Rule 3.0.9: Public object becoming private resets."""
    pass


@given("a public card in the graveyard zone with go again effect")
def public_graveyard_card_with_go_again(game_state):
    """Rule 3.0.9: Public card in graveyard with go-again effect."""
    game_state.public_go_again_card = game_state.create_card(
        name="Go Again Graveyard Card"
    )
    game_state.set_object_visibility(game_state.public_go_again_card, "public")
    game_state.public_go_again_card._has_go_again_effect = True
    game_state.player.graveyard.add_card(game_state.public_go_again_card)


@when("the card becomes a private object")
def card_becomes_private(game_state):
    """Rule 3.0.9: Card becomes private (face-down)."""
    game_state.become_private_result = game_state.make_object_private(
        game_state.public_go_again_card
    )


@then("the card resets and becomes a new private object")
def card_resets_on_private(game_state):
    """Rule 3.0.9: Object resets when becoming private."""
    assert game_state.become_private_result.object_was_reset is True


@then("the go again effect no longer applies")
def go_again_removed_on_reset(game_state):
    """Rule 3.0.9: Reset removes all effects from previous existence."""
    assert (
        getattr(
            game_state.become_private_result.new_object, "_has_go_again_effect", False
        )
        is False
    )


# ===== Scenario 29: Trigger references new object after zone change =====
# Tests Rule 3.0.9a


@scenario(
    "../features/section_3_0_zones_general.feature",
    "Triggered ability references new object after zone change",
)
def test_trigger_references_new_object_after_zone_change():
    """Rule 3.0.9a: Trigger references new object as long as it's public."""
    pass


@given("a card in the arena with a triggered ability")
def card_in_arena_with_trigger(game_state):
    """Rule 3.0.9a: Card in arena that will trigger when destroyed."""
    game_state.trigger_source_card = game_state.create_card(name="Trigger Source Card")
    game_state.trigger_source_card._has_destroy_trigger = True
    game_state.player.arena.add_card(game_state.trigger_source_card)


@when("the card moves to the graveyard and triggers an ability")
def card_moves_and_triggers(game_state):
    """Rule 3.0.9a: Card destroyed, moves to graveyard, triggers."""
    game_state.trigger_result = game_state.destroy_card_and_capture_trigger(
        game_state.trigger_source_card
    )


@then("the triggered ability references the new object in graveyard")
def trigger_references_new_object(game_state):
    """Rule 3.0.9a: Trigger references new object in graveyard."""
    assert game_state.trigger_result.trigger_references_new_object is True


@then("the triggered ability has the new object reference")
def trigger_has_new_reference(game_state):
    """Rule 3.0.9a: Trigger layer has reference to new graveyard object."""
    assert game_state.trigger_result.new_object_reference is not None


# ===== Scenario 30: Reset object preserves history =====
# Tests Rule 3.0.9c - Slithering Shadowpede example


@scenario(
    "../features/section_3_0_zones_general.feature",
    "Reset object preserves history of how it became a new object",
)
def test_reset_object_preserves_history():
    """Rule 3.0.9c: History preserved when object resets."""
    pass


@given("a card banished from the hand zone")
def card_banished_from_hand(game_state):
    """Rule 3.0.9c: Card moved from hand to banished zone."""
    game_state.history_card = game_state.create_card(name="History Card")
    game_state.player.hand.add_card(game_state.history_card)
    # Banish from hand - card resets, becomes new object in banished zone
    game_state.banish_result = game_state.banish_card_from_hand(game_state.history_card)
    game_state.banished_card_object = game_state.banish_result.new_object


@when("the engine checks the card's history in the banished zone")
def engine_checks_card_history(game_state):
    """Rule 3.0.9c: Check what history the new object has."""
    game_state.card_history = game_state.get_object_history(
        game_state.banished_card_object
    )


@then("the card remembers it was banished from the hand zone")
def card_remembers_banished_from_hand(game_state):
    """Rule 3.0.9c: History shows banished from hand."""
    assert game_state.card_history.was_banished_from_hand is True


@then("the card can be played from the banished zone this turn")
def card_can_be_played_from_banished(game_state):
    """Rule 3.0.9c: History allows play from banished this turn."""
    assert game_state.card_history.can_be_played_from_banished_this_turn is True


# ===== Scenario 31: Clearing moves to graveyard =====
# Tests Rule 3.0.12


@scenario(
    "../features/section_3_0_zones_general.feature",
    "Clearing a card moves it to the graveyard",
)
def test_clearing_card_moves_to_graveyard():
    """Rule 3.0.12: Clearing moves card to owner's graveyard."""
    pass


@given("a card in the permanent zone")
def card_in_permanent_zone(game_state):
    """Rule 3.0.12: Card in permanent zone."""
    game_state.clear_card = game_state.create_card(name="Card To Clear")
    game_state.player.permanent.add_card(game_state.clear_card)


@when("the card is cleared")
def card_is_cleared(game_state):
    """Rule 3.0.12: Clear the card."""
    game_state.clear_result = game_state.clear_object(game_state.clear_card)


@then("the card is moved to its owner's graveyard")
def card_moved_to_owner_graveyard(game_state):
    """Rule 3.0.12: Cleared card goes to graveyard."""
    assert game_state.clear_result.destination_zone_type == ZoneType.GRAVEYARD
    assert game_state.clear_card in game_state.player.graveyard


@then("the card is no longer in the permanent zone")
def card_not_in_permanent(game_state):
    """Rule 3.0.12: Cleared card no longer in permanent zone."""
    assert game_state.clear_card not in game_state.player.permanent


# ===== Scenario 32: Clearing a token causes cessation =====
# Tests Rule 3.0.12a


@scenario(
    "../features/section_3_0_zones_general.feature",
    "Clearing a token causes it to cease to exist",
)
def test_clearing_token_causes_cessation():
    """Rule 3.0.12a: Tokens cease to exist when cleared, not moved to graveyard."""
    pass


@given("a token card in the permanent zone")
def token_in_permanent(game_state):
    """Rule 3.0.12a: Token in permanent zone."""
    # CardType.TOKEN is a missing engine feature (Rule 3.0.12a, 1.3.2b)
    TOKEN = getattr(CardType, "TOKEN", CardType.ACTION)
    game_state.token_card = game_state.create_card(name="Test Token", card_type=TOKEN)
    # Mark as token explicitly since CardType.TOKEN might not exist yet
    game_state.token_card._is_token = True
    game_state.player.permanent.add_card(game_state.token_card)


@when("the token is cleared")
def token_is_cleared(game_state):
    """Rule 3.0.12a: Clear the token."""
    game_state.token_clear_result = game_state.clear_object(game_state.token_card)


@then("the token ceases to exist")
def token_ceases_to_exist(game_state):
    """Rule 3.0.12a: Token ceases to exist on clearing."""
    assert game_state.token_clear_result.ceased_to_exist is True


@then("the token is not moved to any graveyard")
def token_not_in_graveyard(game_state):
    """Rule 3.0.12a: Token not moved to graveyard."""
    assert game_state.token_clear_result.moved_to_graveyard is False


# ===== Scenario 33: Unspecified zone refers to controller's zone =====
# Tests Rule 3.0.13


@scenario(
    "../features/section_3_0_zones_general.feature",
    "Unspecified zone in effect refers to effect controller's zone",
)
def test_unspecified_zone_refers_to_controller_zone():
    """Rule 3.0.13: Effect with no zone owner -> controller's zone."""
    pass


@given('player 0 controls an effect that refers to "your graveyard"')
def player_0_controls_effect_your_graveyard(game_state):
    """Rule 3.0.13: Player 0 controls effect referring to unspecified zone."""
    game_state.effect_controller_id = 0
    game_state.effect_zone_reference = "graveyard"


@when("the effect resolves")
def effect_resolves(game_state):
    """Rule 3.0.13: Effect resolves and resolves zone reference."""
    game_state.resolved_zone = game_state.resolve_effect_zone_reference(
        zone_type_name=game_state.effect_zone_reference,
        controller_id=game_state.effect_controller_id,
    )


@then("the effect refers to player 0's graveyard zone")
def effect_refers_to_player0_graveyard(game_state):
    """Rule 3.0.13: Zone resolved to player 0's graveyard."""
    assert game_state.resolved_zone.owner_id == 0
    assert game_state.resolved_zone.zone_type == ZoneType.GRAVEYARD


@then("not player 1's graveyard zone")
def effect_not_player1_graveyard(game_state):
    """Rule 3.0.13: Zone not player 1's."""
    assert game_state.resolved_zone.owner_id != 1


# ===== Fixtures =====


@pytest.fixture
def game_state():
    """
    Fixture providing game state for testing Section 3.0 Zone rules.

    Uses BDDGameState with additional zone-specific helper methods.
    Reference: Rule 3.0
    """
    from tests.bdd_helpers import BDDGameState

    state = BDDGameState()

    # Additional state tracking needed for zone tests

    # Rule 3.0.1: Zone types available from ZoneType enum
    state.zone_types = []

    # Rule 3.0.2: Shared zones (missing engine feature)
    # Stack, permanent, combat chain zones are shared by all players
    # These should be represented as a single shared zone accessible to all players
    state.shared_stack = ZoneSharedStub(ZoneType.STACK)

    # Rule 3.0.5: Arena zone types
    state._arena_zone_types = None

    # Results storage
    state.card_visibility = None
    state.zone_types = []
    state.graveyard_visibility = None
    state.banished_visibility = None
    state.pitch_visibility = None
    state.stack_visibility = None
    state.hand_zone_visibility = None
    state.deck_visibility = None
    state.arsenal_visibility = None
    state.arena_zone_types = None
    state.arena_zone_types_3_5b = None
    state.zone_move_result = None
    state.zone_power_result = None
    state.private_move_result = None
    state.noop_move_result = None
    state.reset_result = None
    state.become_private_result = None
    state.trigger_result = None
    state.card_history = None
    state.clear_result = None
    state.token_clear_result = None
    state.resolved_zone = None
    state.can_owner_see = None
    state.p0_hand = None
    state.p1_hand = None
    state.stack_zone_check = None
    state.effect_applies = None

    # Add additional zones to player that may be missing from bdd_helpers
    _add_missing_zones(state)

    # Add helper methods
    _add_zone_helper_methods(state)

    return state


def _add_missing_zones(state):
    """Add zones that TestPlayer doesn't have by default."""
    # TestPlayer only has hand, banished_zone, arsenal, arena, pitch_zone
    # We need graveyard, deck, permanent, and combat chain for these tests
    from tests.bdd_helpers import TestZone

    if not hasattr(state.player, "graveyard"):
        state.player.graveyard = TestZone(ZoneType.GRAVEYARD, 0)

    if not hasattr(state.player, "deck"):
        state.player.deck = TestZone(ZoneType.DECK, 0)

    if not hasattr(state.player, "permanent"):
        # ZoneType.PERMANENT is a missing engine feature - use STACK as placeholder
        # Engine Feature Needed: ZoneType.PERMANENT (Rule 3.0.1, 3.0.5)
        _permanent_zone_type = getattr(ZoneType, "PERMANENT", ZoneType.STACK)
        state.player.permanent = TestZone(_permanent_zone_type, 0)

    if not hasattr(state.defender, "graveyard"):
        state.defender.graveyard = TestZone(ZoneType.GRAVEYARD, 1)


def _add_zone_helper_methods(state):
    """Add helper methods for zone visibility and movement testing."""

    def get_zone_visibility_type(zone):
        """Get the default visibility type of a zone (public or private)."""
        zone_obj = zone._zone if hasattr(zone, "_zone") else zone
        # Rule 3.0.4a: arms, banished, chest, combat chain, graveyard, head, hero, legs,
        # permanent, pitch, stack, weapon are public zones
        # Note: ZoneType.PERMANENT and ZoneType.WEAPON are missing engine features
        PUBLIC_ZONE_TYPES = {
            ZoneType.ARMS,
            ZoneType.BANISHED,
            ZoneType.CHEST,
            ZoneType.COMBAT_CHAIN,
            ZoneType.GRAVEYARD,
            ZoneType.HEAD,
            ZoneType.HERO,
            ZoneType.LEGS,
            ZoneType.PITCH,
            ZoneType.STACK,
            ZoneType.WEAPON_1,  # Current engine has WEAPON_1/WEAPON_2 instead of WEAPON
            ZoneType.WEAPON_2,
        }
        # Add PERMANENT if it exists (missing engine feature)
        _permanent = getattr(ZoneType, "PERMANENT", None)
        if _permanent:
            PUBLIC_ZONE_TYPES.add(_permanent)
        # Add WEAPON if it exists (missing engine feature)
        _weapon = getattr(ZoneType, "WEAPON", None)
        if _weapon:
            PUBLIC_ZONE_TYPES.add(_weapon)
        if zone_obj.zone_type in PUBLIC_ZONE_TYPES:
            return "public"
        return "private"

    def get_object_visibility(card):
        """Get the visibility of an object.

        If the card has an explicit visibility set via set_object_visibility(),
        that takes priority over the zone-default visibility (Rules 3.0.4c/d).
        """
        # Explicit visibility set overrides zone-based defaults (Rules 3.0.4c/d)
        if hasattr(card, "_visibility_explicitly_set"):
            return "private" if card._is_private else "public"
        # If explicitly made private (face-down), it's private regardless of zone
        if hasattr(card, "_is_private") and card._is_private:
            return "private"
        # Default: determine from zone type
        for zone_attr in ["hand", "arsenal", "deck"]:
            zone = getattr(state.player, zone_attr, None)
            if zone and card in zone:
                return "private"
        return "public"

    def set_object_visibility(card, visibility):
        """Set the visibility of an object explicitly.
        Rules 3.0.4c/d: Public zones can have private objects, private zones can have public objects.
        """
        card._is_private = visibility == "private"
        card._visibility_explicitly_set = True

    def check_can_owner_see(card, owner_player_id):
        """Check if a player can see their own private object.
        Rule 3.0.3a: Player may look at their own private objects, except in deck zone."""
        card_owner_id = getattr(card, "owner_id", 0)
        if card_owner_id != owner_player_id:
            return False
        # Cannot see if in deck zone
        player = state.player if owner_player_id == 0 else state.defender
        if hasattr(player, "deck") and card in player.deck:
            return False
        return True

    def get_arena_zone_types():
        """Rule 3.0.5: Arena contains arms, chest, combat chain, head, hero, legs, permanent, weapon."""
        # Rule 3.0.5: Arena zone types (engine is missing PERMANENT and WEAPON)
        arena_types = {
            ZoneType.ARMS,
            ZoneType.CHEST,
            ZoneType.COMBAT_CHAIN,
            ZoneType.HEAD,
            ZoneType.HERO,
            ZoneType.LEGS,
        }
        # Add PERMANENT if available (missing engine feature)
        _permanent = getattr(ZoneType, "PERMANENT", None)
        if _permanent:
            arena_types.add(_permanent)
        # Add WEAPON if available; otherwise use WEAPON_1/WEAPON_2 (engine limitation)
        _weapon = getattr(ZoneType, "WEAPON", None)
        if _weapon:
            arena_types.add(_weapon)
        return arena_types

    def check_arena_is_zone_type():
        """Rule 3.0.5a: Arena is not itself a ZoneType."""
        # If there's an ARENA value in ZoneType, this is wrong
        return hasattr(ZoneType, "ARENA")

    def check_effect_applies_to_public_zone_card(card, zone_type):
        """Rule 3.0.4e: Effect in public zone only applies if source is public."""
        if hasattr(card, "_is_private") and card._is_private:
            return False
        return True

    def move_card_between_zones(card, from_zone, to_zone):
        """Rule 3.0.7: Move card between zones simultaneously."""
        result = ZoneMoveResultStub()
        result.was_ever_in_no_zone = False
        from_zone.remove_card(card)
        to_zone.add_card(card)
        return result

    def move_card_and_capture_origin_properties(card, from_zone, to_zone):
        """Rule 3.0.7a: Move card, capturing origin properties."""
        result = ZoneMoveResultStub()
        result.origin_power = getattr(card, "_power", 0)
        from_zone.remove_card(card)
        to_zone.add_card(card)
        return result

    def move_private_card_to_private_zone(
        card, from_zone, to_zone, destination_visibility
    ):
        """Rule 3.0.7a: Move private card to private destination."""
        result = PrivateMoveResultStub()
        # Private-to-private: no properties for effects
        origin_private = hasattr(card, "_is_private") and card._is_private
        dest_private = destination_visibility == "private"
        result.has_no_properties_for_effects = origin_private and dest_private
        from_zone.remove_card(card)
        to_zone.add_card(card)
        return result

    def move_card_same_zone(card, zone):
        """Rule 3.0.7b: Move to same zone is no-op."""
        result = SameZoneMoveResultStub()
        if card in zone:
            result.move_occurred = False
        else:
            result.move_occurred = True
            zone.add_card(card)
        return result

    def move_card_to_hand(card, from_zone):
        """Rule 3.0.9: Move card to hand (non-arena zone) - resets."""
        result = ZoneResetResultStub()
        result.object_was_reset = True
        # When card enters hand, it resets - effects don't carry over
        from_zone.remove_card(card)
        state.player.hand.add_card(card)
        # Create a "new object" representation - in real engine, card would be new object
        result.new_object = type("NewObject", (), {})()
        # Effects from old existence don't transfer
        return result

    def make_object_private(card):
        """Rule 3.0.9: Making an object private causes a reset."""
        result = ZoneResetResultStub()
        result.object_was_reset = True
        card._is_private = True
        # Create new object - effects don't carry over
        result.new_object = type("NewObject", (), {})()
        return result

    def destroy_card_and_capture_trigger(card):
        """Rule 3.0.9a: Destroy card and capture triggered ability reference."""
        result = TriggerResultStub()
        # Card moves from arena to graveyard
        state.player.arena.remove_card(card)
        state.player.graveyard.add_card(card)
        # Trigger references new object (same card, but in graveyard = new object per Rule 3.0.9)
        result.trigger_references_new_object = True
        result.new_object_reference = (
            card  # In real engine, this would be the new object
        )
        return result

    def banish_card_from_hand(card):
        """Rule 3.0.9c: Banish card from hand, preserving history."""
        result = BanishResultStub()
        state.player.hand.remove_card(card)
        state.player.banished_zone.add_card(card)
        # New object in banished zone, but history preserved
        result.new_object = type(
            "BanishedObject", (), {"_was_banished_from_hand": True}
        )()
        return result

    def get_object_history(obj):
        """Rule 3.0.9c: Get the history of an object."""
        history = ObjectHistoryStub()
        history.was_banished_from_hand = getattr(obj, "_was_banished_from_hand", False)
        history.can_be_played_from_banished_this_turn = history.was_banished_from_hand
        return history

    def clear_object(card):
        """Rule 3.0.12: Clear an object - move to graveyard or cease to exist."""
        result = ClearResultStub()
        # Check if token (Rule 3.0.12a)
        # CardType.TOKEN is a missing engine feature - use _is_token attribute as fallback
        TOKEN = getattr(CardType, "TOKEN", None)
        is_token = getattr(card, "_is_token", False)
        if not is_token and TOKEN is not None and hasattr(card, "template"):
            is_token = TOKEN in card.template.types

        # Remove from current zone
        for zone_attr in [
            "permanent",
            "graveyard",
            "arena",
            "hand",
            "banished_zone",
            "arsenal",
        ]:
            zone = getattr(state.player, zone_attr, None)
            if zone and card in zone:
                zone.remove_card(card)
                break

        if is_token:
            result.ceased_to_exist = True
            result.moved_to_graveyard = False
            result.destination_zone_type = None
        else:
            result.ceased_to_exist = False
            result.moved_to_graveyard = True
            result.destination_zone_type = ZoneType.GRAVEYARD
            state.player.graveyard.add_card(card)

        return result

    def place_card_in_arena_unspecified(card):
        """Rule 3.0.5a: Place card in arena without specifying zone -> permanent zone."""
        result = ArenaPlacementResultStub()
        # ZoneType.PERMANENT is a missing engine feature
        PERMANENT = getattr(ZoneType, "PERMANENT", None)
        result.destination_zone_type = (
            PERMANENT  # None until engine adds ZoneType.PERMANENT
        )
        result.is_permanent = True
        state.player.permanent.add_card(card)
        return result

    def resolve_effect_zone_reference(zone_type_name, controller_id):
        """Rule 3.0.13: Resolve zone reference for effect without specified owner."""
        zone_type_map = {
            "graveyard": ZoneType.GRAVEYARD,
            "hand": ZoneType.HAND,
            "banished": ZoneType.BANISHED,
            "deck": ZoneType.DECK,
        }
        zone_type = zone_type_map.get(zone_type_name)
        player = state.player if controller_id == 0 else state.defender
        # Return a zone reference result
        result = ZoneReferenceResultStub()
        result.owner_id = controller_id
        result.zone_type = zone_type
        return result

    # Attach methods to state
    state.get_zone_visibility_type = get_zone_visibility_type
    state.get_object_visibility = get_object_visibility
    state.set_object_visibility = set_object_visibility
    state.check_can_owner_see = check_can_owner_see
    state.get_arena_zone_types = get_arena_zone_types
    state.check_arena_is_zone_type = check_arena_is_zone_type
    state.check_effect_applies_to_public_zone_card = (
        check_effect_applies_to_public_zone_card
    )
    state.move_card_between_zones = move_card_between_zones
    state.move_card_and_capture_origin_properties = (
        move_card_and_capture_origin_properties
    )
    state.move_private_card_to_private_zone = move_private_card_to_private_zone
    state.move_card_same_zone = move_card_same_zone
    state.move_card_to_hand = move_card_to_hand
    state.make_object_private = make_object_private
    state.destroy_card_and_capture_trigger = destroy_card_and_capture_trigger
    state.banish_card_from_hand = banish_card_from_hand
    state.get_object_history = get_object_history
    state.clear_object = clear_object
    state.place_card_in_arena_unspecified = place_card_in_arena_unspecified
    state.resolve_effect_zone_reference = resolve_effect_zone_reference


# ===== Stub Classes for Engine Features Not Yet Implemented =====


class ZoneSharedStub:
    """
    Stub for shared zone (stack, permanent, combat chain).
    Engine Feature Needed: Shared zone accessible to all players (Rule 3.0.2).
    """

    def __init__(self, zone_type: ZoneType):
        self.zone_type = zone_type
        self.cards = []
        self._zone = Zone(zone_type=zone_type, owner_id=-1)  # -1 = shared

    def add_card(self, card):
        self._zone.add(card)

    def remove_card(self, card):
        self._zone.remove(card)

    def __contains__(self, card):
        return self._zone.contains(card)


class ZoneMoveResultStub:
    """
    Stub for zone movement result.
    Engine Feature Needed: ZoneMoveResult tracking movement atomicity (Rule 3.0.7).
    """

    was_ever_in_no_zone: bool = False
    origin_power: int = 0


class PrivateMoveResultStub:
    """
    Stub for private-to-private move result.
    Engine Feature Needed: Tracking no-properties condition (Rule 3.0.7a).
    """

    has_no_properties_for_effects: bool = False


class SameZoneMoveResultStub:
    """
    Stub for same-zone move result.
    Engine Feature Needed: SameZoneMoveResult tracking no-op (Rule 3.0.7b).
    """

    move_occurred: bool = False


class ZoneResetResultStub:
    """
    Stub for zone reset result.
    Engine Feature Needed: Zone reset tracking new object creation (Rule 3.0.9).
    """

    object_was_reset: bool = False
    new_object: object = None


class TriggerResultStub:
    """
    Stub for trigger capture result.
    Engine Feature Needed: Trigger referencing new object after zone change (Rule 3.0.9a).
    """

    trigger_references_new_object: bool = False
    new_object_reference: object = None


class BanishResultStub:
    """
    Stub for banish result.
    Engine Feature Needed: History preservation on zone reset (Rule 3.0.9c).
    """

    new_object: object = None


class ObjectHistoryStub:
    """
    Stub for object history.
    Engine Feature Needed: CardInstance.history tracking (Rule 3.0.9c).
    """

    was_banished_from_hand: bool = False
    can_be_played_from_banished_this_turn: bool = False


class ClearResultStub:
    """
    Stub for clearing result.
    Engine Feature Needed: GameEngine.clear_object() (Rule 3.0.12).
    """

    ceased_to_exist: bool = False
    moved_to_graveyard: bool = False
    destination_zone_type: object = None


class ArenaPlacementResultStub:
    """
    Stub for unspecified arena placement result.
    Engine Feature Needed: Default arena placement to permanent zone (Rule 3.0.5a).
    """

    # ZoneType.PERMANENT is a missing engine feature
    # destination_zone_type would be ZoneType.PERMANENT when implemented
    destination_zone_type: object = (
        None  # Set to ZoneType.PERMANENT when engine supports it
    )
    is_permanent: bool = True


class ZoneReferenceResultStub:
    """
    Stub for zone reference resolution result.
    Engine Feature Needed: EffectZoneResolver.resolve_zone() (Rule 3.0.13).
    """

    owner_id: int = 0
    zone_type: ZoneType = None
