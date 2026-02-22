"""
Step definitions for Section 1.2: Objects
Reference: Flesh and Blood Comprehensive Rules Section 1.2

This module implements behavioral tests for object concepts in Flesh and Blood:
- Rule 1.2.1: An object is an element of the game with properties in a zone
- Rule 1.2.1a: Owner of an object = owner of the card/macro/layer that represents it
- Rule 1.2.1b: Controller of an object; no controller outside arena/stack
- Rule 1.2.2: Object has one or more object identities
- Rule 1.2.2a: All objects have the identity "object"
- Rule 1.2.2b: Named objects have their name as an identity
- Rule 1.2.2c: Card's traits, types, subtypes are identities (except subtype "attack")
- Rule 1.2.2d: Attack-card/proxy/layer has the identity "attack"
- Rule 1.2.2e: All cards have the identity "card"
- Rule 1.2.2f: Permanents have the identity "permanent"
- Rule 1.2.2g: Activated-layers have the identity "activated ability"
- Rule 1.2.2h: Triggered-layers have the identity "triggered effect"
- Rule 1.2.3: Last known information = snapshot before object ceases to exist
- Rule 1.2.3a: LKI used when the specific object no longer exists
- Rule 1.2.3b: LKI includes all parameters, history, and effects at snapshot time
- Rule 1.2.3c: LKI is immutable; effects cannot alter it
- Rule 1.2.3d: LKI is not a legal target for rules/effects
- Rule 1.2.4: Cards and macros are sources of abilities, effects, non-card layers, attack-proxies

Engine Features Needed for Section 1.2:
- [ ] GameObject base class or interface with object_identities property (Rule 1.2.2)
- [ ] CardInstance.get_object_identities() -> Set[str] (Rules 1.2.2a-h)
- [ ] CardInstance.owner attribute checking (Rule 1.2.1a)
- [ ] CardInstance.controller attribute only set in arena/stack (Rule 1.2.1b)
- [ ] LastKnownInformation class with snapshot semantics (Rule 1.2.3)
- [ ] LastKnownInformation.is_immutable property (Rule 1.2.3c)
- [ ] LastKnownInformation.is_legal_target property = False (Rule 1.2.3d)
- [ ] GameEngine or Zone tracking of LKI for objects that ceased to exist (Rule 1.2.3a)
- [ ] AttackProxy class with source card reference (Rule 1.2.4)
- [ ] CardInstance.is_permanent property or method (Rule 1.2.2f)

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


# ===== Scenario 1: A card in a zone is a game object =====
# Tests Rule 1.2.1 - Cards in zones are objects with properties


@scenario(
    "../features/section_1_2_objects.feature",
    "A card in a zone is a game object",
)
def test_card_in_zone_is_object():
    """Rule 1.2.1: Cards in zones are game objects with properties."""
    pass


@given("a player has a hand zone")
def player_has_hand_zone(game_state):
    """Rule 1.2.1: A hand zone exists in the game."""
    # game_state.player already has a hand zone via TestZone(ZoneType.HAND)
    assert game_state.player.hand is not None


@given("the player has a card in hand")
def player_has_card_in_hand(game_state):
    """Rule 1.2.1: Card placed in the hand zone."""
    game_state.test_card = game_state.create_card(name="Test Object Card")
    game_state.player.hand.add_card(game_state.test_card)


@given("a player has a card in hand")
def a_player_has_card_in_hand(game_state):
    """Rule 1.2.2a/e: A card is placed in the player's hand zone."""
    game_state.test_card = game_state.create_card(name="Test Object Card")
    game_state.player.hand.add_card(game_state.test_card)


@when("the engine inspects the card in hand")
def engine_inspects_card(game_state):
    """Rule 1.2.1: The engine checks the card object."""
    game_state.inspected_card = game_state.test_card


@then("the card is recognized as a game object")
def card_is_game_object(game_state):
    """Rule 1.2.1: Card is an instance of a game object class."""
    # A card should be recognized as a game object
    assert isinstance(game_state.inspected_card, CardInstance)
    assert game_state.inspected_card.is_game_object


@then("the card has properties")
def card_has_properties(game_state):
    """Rule 1.2.1: Cards have properties (name, type, etc.)."""
    card = game_state.inspected_card
    # Cards should have name, types, color, etc.
    assert card.name is not None
    assert card.template.types is not None


# ===== Scenario 2: Different game elements are all objects =====
# Tests Rule 1.2.1 - Cards, attacks, macros, and layers are objects


@scenario(
    "../features/section_1_2_objects.feature",
    "Different game elements are all objects",
)
def test_different_game_elements_are_objects():
    """Rule 1.2.1: Cards, attacks, macros, and layers are all game objects."""
    pass


@given("a game is in progress")
def game_in_progress(game_state):
    """Rule 1.2.1: A game is being played."""
    # The game_state fixture provides a running game context
    assert game_state is not None


@when("the engine enumerates game objects")
def engine_enumerates_objects(game_state):
    """Rule 1.2.1: Engine can enumerate game objects."""
    game_state.enumerated_objects = game_state.get_all_game_objects()


@then("cards are recognized as objects")
def cards_are_objects(game_state):
    """Rule 1.2.1: Cards are recognized as game objects."""
    # The game object enumeration should include cards
    card = game_state.create_card(name="Test Card Object")
    assert card.is_game_object


@then("attacks are recognized as objects")
def attacks_are_objects(game_state):
    """Rule 1.2.1: Attacks are recognized as game objects."""
    # Attacks created on the combat chain should also be objects
    assert game_state.attack.is_game_object


# ===== Scenario 3: Object owner matches card owner =====
# Tests Rule 1.2.1a - Owner of an object = owner of the card that represents it


@scenario(
    "../features/section_1_2_objects.feature",
    "The owner of an object matches the card that represents it",
)
def test_object_owner_matches_card_owner():
    """Rule 1.2.1a: Object owner is same as the card that represents it."""
    pass


@given("player 0 creates a card")
def player_0_creates_card(game_state):
    """Rule 1.2.1a: Card created and owned by player 0."""
    game_state.owned_card = game_state.create_card(name="Owned Card", owner_id=0)


@given("the card is placed in a zone")
def card_placed_in_zone(game_state):
    """Rule 1.2.1a: Card is placed in a zone, becoming an object."""
    game_state.player.hand.add_card(game_state.owned_card)


@when("the engine checks the card object's owner")
def engine_checks_object_owner(game_state):
    """Rule 1.2.1a: Engine evaluates the owner of the object."""
    game_state.checked_owner_id = game_state.owned_card.owner_id


@then("the card object's owner is player 0")
def object_owner_is_player_0(game_state):
    """Rule 1.2.1a: Object owner matches the card's owner (player 0)."""
    assert game_state.checked_owner_id == 0


# ===== Scenario 4: Object without representing card has no owner =====
# Tests Rule 1.2.1a - Objects without a card have no owner


@scenario(
    "../features/section_1_2_objects.feature",
    "An object without a representing card has no owner",
)
def test_object_without_card_has_no_owner():
    """Rule 1.2.1a: Objects not represented by a card/macro/layer have no owner."""
    pass


@when("an attack-proxy object is created without an owner")
def attack_proxy_created_without_owner(game_state):
    """Rule 1.2.1a: An attack-proxy is created that has no owner assignment."""
    # Attack-proxies that are not represented by a card have no owner
    game_state.attack_proxy = game_state.create_attack_proxy(source=None)


@then("the attack-proxy has no owner")
def attack_proxy_has_no_owner(game_state):
    """Rule 1.2.1a: Attack-proxy without a representing card has no owner."""
    assert game_state.attack_proxy.owner_id is None


# ===== Scenario 5: Card in hand has no controller =====
# Tests Rule 1.2.1b - No controller outside arena/stack


@scenario(
    "../features/section_1_2_objects.feature",
    "A card in hand has no controller",
)
def test_card_in_hand_has_no_controller():
    """Rule 1.2.1b: Cards in hand have no controller."""
    pass


@given("player 0 has a card in their hand")
def player_0_has_card_in_hand(game_state):
    """Rule 1.2.1b: Card is in the hand zone (not arena or stack)."""
    game_state.hand_card = game_state.create_card(name="Hand Card", owner_id=0)
    game_state.player.hand.add_card(game_state.hand_card)


@when("the engine checks the controller of that card")
def engine_checks_controller(game_state):
    """Rule 1.2.1b: Engine evaluates the controller of the card.

    Works for hand, arena, and stack cards - uses whichever was set in the Given step.
    """
    # Find the card to check (set in whichever Given step ran)
    card = game_state.hand_card or game_state.arena_card or game_state.stack_card
    game_state.checked_controller = card.controller_id if card else None


@then("the card has no controller")
def card_has_no_controller(game_state):
    """Rule 1.2.1b: Card in hand has no controller (controller_id is None)."""
    assert game_state.checked_controller is None


# ===== Scenario 6: Card in the arena has a controller =====
# Tests Rule 1.2.1b - Controller exists when card is in arena


@scenario(
    "../features/section_1_2_objects.feature",
    "A card in the arena has a controller",
)
def test_card_in_arena_has_controller():
    """Rule 1.2.1b: Cards in the arena have a controller."""
    pass


@given("player 0 plays a card into the arena")
def player_0_plays_card_to_arena(game_state):
    """Rule 1.2.1b: Card is moved to the arena zone."""
    game_state.arena_card = game_state.create_card(
        name="Arena Card",
        owner_id=0,
        card_type=CardType.EQUIPMENT,
    )
    # Simulate playing to arena - sets controller
    game_state.play_card_to_arena(game_state.arena_card, controller_id=0)


@then("the card's controller is player 0")
def card_controller_is_player_0(game_state):
    """Rule 1.2.1b: Card in arena has controller (the player who played it)."""
    assert game_state.arena_card.controller_id == 0


# ===== Scenario 7: Card on stack has a controller =====
# Tests Rule 1.2.1b - Controller exists when card is on stack


@scenario(
    "../features/section_1_2_objects.feature",
    "A card on the stack has a controller",
)
def test_card_on_stack_has_controller():
    """Rule 1.2.1b: Cards on the stack have a controller."""
    pass


@given("player 0 plays a card onto the stack")
def player_0_plays_card_to_stack(game_state):
    """Rule 1.2.1b: Card is played to the stack zone."""
    game_state.stack_card = game_state.create_card(
        name="Stack Card",
        owner_id=0,
    )
    # Simulate playing to stack - sets controller
    game_state.play_card_to_stack(game_state.stack_card, controller_id=0)


@then("the card's controller is player 0")
def stack_card_controller_is_player_0(game_state):
    """Rule 1.2.1b: Card in arena or stack has controller (player who played it)."""
    # Use whichever card was set in the Given step (arena or stack scenario)
    card = game_state.arena_card or game_state.stack_card
    assert card is not None, "Expected arena_card or stack_card to be set"
    assert card.controller_id == 0


# ===== Scenario 8: Every object has the "object" identity =====
# Tests Rule 1.2.2a - All objects have the "object" identity


@scenario(
    "../features/section_1_2_objects.feature",
    'Every game object has the object identity "object"',
)
def test_every_object_has_object_identity():
    """Rule 1.2.2a: All game objects have the identity 'object'."""
    pass


@when("the engine checks the object identities of the card")
def engine_checks_object_identities(game_state):
    """Rule 1.2.2: Engine retrieves the object identities of the card."""
    game_state.object_identities = game_state.test_card.get_object_identities()


@then('the card has the object identity "object"')
def card_has_object_identity(game_state):
    """Rule 1.2.2a: The "object" identity is always present."""
    assert "object" in game_state.object_identities


# ===== Scenario 9: Named objects have name as identity =====
# Tests Rule 1.2.2b - Name is an object identity


@scenario(
    "../features/section_1_2_objects.feature",
    "An object's name is one of its object identities",
)
def test_name_is_object_identity():
    """Rule 1.2.2b: An object's name is one of its object identities."""
    pass


@given('a card named "Lunging Press" exists')
def card_named_lunging_press(game_state):
    """Rule 1.2.2b: Card with name 'Lunging Press' exists."""
    game_state.test_card = game_state.create_card(name="Lunging Press")


@then('the card has the object identity "Lunging Press"')
def card_has_name_identity(game_state):
    """Rule 1.2.2b: Card name 'Lunging Press' is an object identity."""
    assert "Lunging Press" in game_state.object_identities


# ===== Scenario 10: Weapon card has "weapon" identity =====
# Tests Rule 1.2.2c - Type is an object identity


@scenario(
    "../features/section_1_2_objects.feature",
    'A weapon card has the object identity "weapon"',
)
def test_weapon_card_has_weapon_identity():
    """Rule 1.2.2c: A weapon card has 'weapon' as an object identity."""
    pass


@given('a card with type "weapon" exists')
def weapon_card_exists(game_state):
    """Rule 1.2.2c: A weapon-type card is created."""
    game_state.test_card = game_state.create_card(
        name="Test Weapon",
        card_type=CardType.WEAPON,
    )


@then('the card has the object identity "weapon"')
def card_has_weapon_identity(game_state):
    """Rule 1.2.2c: The card's type 'weapon' is an object identity."""
    assert "weapon" in game_state.object_identities


# ===== Scenario 11: Attack subtype is NOT an object identity for cards =====
# Tests Rule 1.2.2c - Exception: subtype "attack" is excluded from identities


@scenario(
    "../features/section_1_2_objects.feature",
    "The attack subtype is not an object identity for cards",
)
def test_attack_subtype_not_object_identity():
    """Rule 1.2.2c: The attack subtype is NOT an object identity via subtype mechanism."""
    pass


@given("an attack action card exists")
def attack_action_card_exists(game_state):
    """Rule 1.2.2c: An action card with the attack subtype is created."""
    game_state.test_card = game_state.create_card(
        name="Test Attack Action",
        card_type=CardType.ACTION,
    )
    # Ensure it has attack subtype
    assert Subtype.ATTACK in game_state.test_card.template.subtypes


@when("the engine checks if the card has the attack object identity")
def engine_checks_attack_identity(game_state):
    """Rule 1.2.2d: Engine checks if the card has the 'attack' object identity."""
    game_state.object_identities = game_state.test_card.get_object_identities()


@then('the card does not have the object identity "attack" via its subtype')
def card_subtype_attack_not_identity(game_state):
    """Rule 1.2.2c: The attack subtype does NOT grant the 'attack' identity directly.
    Note: 1.2.2d says attack-cards DO get 'attack' identity via a separate rule."""
    # This verifies that the subtype "attack" itself is excluded per Rule 1.2.2c
    # The "attack" identity, if present, must come from Rule 1.2.2d (attack-card), not the subtype
    # So we check that the attack subtype is NOT listed directly as an identity
    assert "attack" not in game_state.test_card.get_object_identities_from_subtypes()


@then('the card does have the object identity "action"')
def card_has_action_identity(game_state):
    """Rule 1.2.2c: Card types (like 'action') are included as identities."""
    assert "action" in game_state.object_identities


# ===== Scenario 12: Attack-cards have "attack" identity =====
# Tests Rule 1.2.2d - Attack-cards, proxies, and layers have "attack" identity


@scenario(
    "../features/section_1_2_objects.feature",
    'An attack-card has the object identity "attack"',
)
def test_attack_card_has_attack_identity():
    """Rule 1.2.2d: An attack-card has the object identity 'attack'."""
    pass


@then('the card has the object identity "attack"')
def card_has_attack_identity(game_state):
    """Rule 1.2.2d: Attack-card, attack-proxy, or attack-layer has 'attack' identity."""
    assert "attack" in game_state.object_identities


# ===== Scenario 13: Every card has "card" identity =====
# Tests Rule 1.2.2e - All cards have the "card" identity


@scenario(
    "../features/section_1_2_objects.feature",
    'Every card has the object identity "card"',
)
def test_every_card_has_card_identity():
    """Rule 1.2.2e: All cards have the identity 'card'."""
    pass


@then('the card has the object identity "card"')
def card_has_card_identity(game_state):
    """Rule 1.2.2e: Every card has the 'card' object identity."""
    assert "card" in game_state.object_identities


# ===== Scenario 14: Equipment in arena has "permanent" identity =====
# Tests Rule 1.2.2f - Permanents have the "permanent" identity


@scenario(
    "../features/section_1_2_objects.feature",
    'An equipment card in the arena has the object identity "permanent"',
)
def test_permanent_has_permanent_identity():
    """Rule 1.2.2f: Equipment in the arena (a permanent) has 'permanent' identity."""
    pass


@given("player 0 has an equipment card in the arena")
def player_0_has_equipment_in_arena(game_state):
    """Rule 1.2.2f: Equipment is in the arena zone (making it a permanent)."""
    game_state.equipment_card = game_state.create_card(
        name="Test Equipment",
        card_type=CardType.EQUIPMENT,
        owner_id=0,
    )
    game_state.play_card_to_arena(game_state.equipment_card, controller_id=0)


@when("the engine checks the object identities of the equipment")
def engine_checks_equipment_identities(game_state):
    """Rule 1.2.2f: Engine retrieves object identities for equipment in arena."""
    game_state.object_identities = game_state.equipment_card.get_object_identities()


@then('the equipment has the object identity "permanent"')
def equipment_has_permanent_identity(game_state):
    """Rule 1.2.2f: Equipment in the arena is a permanent and has that identity."""
    assert "permanent" in game_state.object_identities


# ===== Scenario 15: LKI is captured when object leaves =====
# Tests Rule 1.2.3 - LKI is a snapshot before object ceases to exist


@scenario(
    "../features/section_1_2_objects.feature",
    "Last known information is captured when an object leaves the game",
)
def test_lki_captured_when_object_leaves():
    """Rule 1.2.3: LKI is a snapshot of state before the object ceased to exist."""
    pass


@given("an attack card with power 6 is on the combat chain")
def attack_card_with_power_6_on_chain(game_state):
    """Rule 1.2.3: Attack card with specific power on combat chain."""
    game_state.chain_card = game_state.create_card(name="Chain Attack", cost=0)
    game_state.chain_card.temp_power_mod = 0
    # Set up as if it's on the combat chain with power 6
    game_state.put_on_combat_chain(game_state.chain_card, power=6)


@when("the attack card is removed from the combat chain")
def attack_card_removed_from_chain(game_state):
    """Rule 1.2.3: Card is moved out of the combat chain (ceases to exist there)."""
    game_state.last_known_info = game_state.remove_from_combat_chain(
        game_state.chain_card
    )


@then("the last known information of the card has power 6")
def lki_has_power_6(game_state):
    """Rule 1.2.3: LKI snapshot includes the power value at time of removal."""
    assert game_state.last_known_info is not None
    assert game_state.last_known_info.power == 6


# ===== Scenario 16: LKI used when object no longer exists =====
# Tests Rule 1.2.3a - LKI used for specific object references


@scenario(
    "../features/section_1_2_objects.feature",
    "Last known information is used when the specific object no longer exists",
)
def test_lki_used_when_object_gone():
    """Rule 1.2.3a: LKI used when effect references specific object that is gone."""
    pass


@given('an attack card named "Endless Arrow" with go again is on the combat chain')
def endless_arrow_on_chain(game_state):
    """Rule 1.2.3a: Endless Arrow with go again on combat chain."""
    game_state.endless_arrow = game_state.create_card(name="Endless Arrow")
    game_state.put_on_combat_chain(game_state.endless_arrow, has_go_again=True)


@when("the card is moved to its owner's hand during resolution")
def card_moved_to_hand(game_state):
    """Rule 1.2.3a: The card is moved to hand (ceases to exist on chain)."""
    game_state.chain_link_lki = game_state.move_card_to_hand_during_resolution(
        game_state.endless_arrow
    )


@then("the chain link uses last known information about the card")
def chain_link_uses_lki(game_state):
    """Rule 1.2.3a: The chain link references LKI since card no longer exists."""
    assert game_state.chain_link_lki is not None
    assert game_state.chain_link_lki.is_last_known_information


@then("the player gains an action point because the card had go again")
def player_gains_action_point(game_state):
    """Rule 1.2.3a: Go again in LKI grants action point when chain link resolves."""
    # The chain link should have resolved using LKI which includes go again
    assert game_state.chain_link_lki.had_go_again


# ===== Scenario 17: LKI not used for generic references =====
# Tests Rule 1.2.3a - LKI only used for specific object references


@scenario(
    "../features/section_1_2_objects.feature",
    "Last known information is not used when the rule doesn't reference the specific object",
)
def test_lki_not_used_for_generic_references():
    """Rule 1.2.3a: LKI not used when rule doesn't specifically refer to the object."""
    pass


@given("an attack card is on the combat chain")
def attack_card_on_chain(game_state):
    """Rule 1.2.3a: Attack card is on the combat chain."""
    game_state.chain_card_2 = game_state.create_card(name="Generic Chain Attack")
    game_state.put_on_combat_chain(game_state.chain_card_2)


@when("the card is moved out of its zone")
def card_moved_out_of_zone(game_state):
    """Rule 1.2.3a: Card is moved, generating LKI."""
    game_state.remove_from_combat_chain(game_state.chain_card_2)


@when("a rule references all cards in the zone generically")
def rule_references_zone_generically(game_state):
    """Rule 1.2.3a: A rule applies to 'all cards in the zone' (generic reference)."""
    # This generic reference does NOT trigger LKI usage
    game_state.generic_zone_reference_used = True


@then("last known information about the removed card is not used")
def lki_not_used_for_generic_reference(game_state):
    """Rule 1.2.3a: Generic zone references don't use LKI for gone cards."""
    # LKI should NOT be consulted for generic references
    assert game_state.lki_was_used_for_generic_reference() is False


# ===== Scenario 18: LKI includes all effects at snapshot time =====
# Tests Rule 1.2.3b - LKI includes all parameters, history, and effects


@scenario(
    "../features/section_1_2_objects.feature",
    "Last known information includes all effects active at snapshot time",
)
def test_lki_includes_all_effects():
    """Rule 1.2.3b: LKI includes all parameters, history, and effects at snapshot time."""
    pass


@given("an attack card has a power buff of +3 applied to it")
def attack_card_with_power_buff(game_state):
    """Rule 1.2.3b: Card has an active effect buffing its power."""
    game_state.buffed_card = game_state.create_card(name="Buffed Attack")
    game_state.buffed_card.temp_power_mod = 3


@given("the card is on the combat chain")
def card_is_on_combat_chain(game_state):
    """Rule 1.2.3b: Card with the buff is on the combat chain."""
    game_state.put_on_combat_chain(game_state.buffed_card)


@when("the card ceases to exist")
def card_ceases_to_exist(game_state):
    """Rule 1.2.3b: Card is removed (ceases to exist on chain)."""
    game_state.buffed_lki = game_state.remove_from_combat_chain(game_state.buffed_card)


@then("the last known information of the card includes the +3 power buff")
def lki_includes_power_buff(game_state):
    """Rule 1.2.3b: LKI includes the +3 temp power mod that was active."""
    assert game_state.buffed_lki is not None
    assert game_state.buffed_lki.temp_power_mod == 3


# ===== Scenario 19: LKI is immutable =====
# Tests Rule 1.2.3c - LKI cannot be altered


@scenario(
    "../features/section_1_2_objects.feature",
    "Last known information cannot be altered after capture",
)
def test_lki_is_immutable():
    """Rule 1.2.3c: LKI is immutable and cannot be altered."""
    pass


@given("an attack card with no go again is captured in last known information")
def attack_card_in_lki_no_go_again(game_state):
    """Rule 1.2.3c: Card without go again ceases to exist, LKI captured."""
    game_state.no_go_again_card = game_state.create_card(name="No Go Again Attack")
    game_state.put_on_combat_chain(game_state.no_go_again_card, has_go_again=False)
    game_state.no_go_again_lki = game_state.remove_from_combat_chain(
        game_state.no_go_again_card
    )


@when("an effect would grant go again to the no-longer-existing card")
def effect_tries_to_grant_go_again(game_state):
    """Rule 1.2.3c: An effect attempts to modify the LKI by granting go again."""
    game_state.modification_result = game_state.try_modify_lki(
        game_state.no_go_again_lki, "grant_go_again"
    )


@then("the last known information remains unchanged")
def lki_remains_unchanged(game_state):
    """Rule 1.2.3c: LKI still shows no go again - it is immutable."""
    assert not game_state.no_go_again_lki.had_go_again


@then("the effect fails to modify the last known information")
def effect_fails_to_modify_lki(game_state):
    """Rule 1.2.3c: The modification attempt fails or is a no-op."""
    assert (
        game_state.modification_result.failed or game_state.modification_result.was_noop
    )


# ===== Scenario 20: Go again via LKI after card leaves =====
# Tests Rule 1.2.3c with the Luminaris example from the rules


@scenario(
    "../features/section_1_2_objects.feature",
    "Go again cannot be granted to a card via LKI after it leaves",
)
def test_luminaris_lki_immutability():
    """Rule 1.2.3c: Luminaris example - LKI cannot gain go again retroactively."""
    pass


@given("an Illusionist attack card is on the combat chain as a chain link")
def illusionist_attack_on_chain(game_state):
    """Rule 1.2.3c: Illusionist attack is on the combat chain."""
    game_state.illusionist_attack = game_state.create_card(
        name="Illusionist Attack",
        card_type=CardType.ACTION,
    )
    game_state.put_on_combat_chain(game_state.illusionist_attack, has_go_again=False)


@given("the attack card is removed from the combat chain")
def illusionist_attack_removed(game_state):
    """Rule 1.2.3c: Illusionist attack card is removed (e.g., moved to hand)."""
    game_state.illusionist_lki = game_state.remove_from_combat_chain(
        game_state.illusionist_attack
    )


@when("a yellow card is added to the pitch zone")
def yellow_card_added_to_pitch(game_state):
    """Rule 1.2.3c: Yellow card enters pitch zone (would normally trigger Luminaris)."""
    yellow_card = game_state.create_card(name="Yellow Card", color=Color.YELLOW)
    game_state.player.pitch_zone.add_card(yellow_card)


@then("the chain link does not gain go again from the LKI")
def chain_link_does_not_gain_go_again(game_state):
    """Rule 1.2.3c: LKI cannot be retroactively altered to add go again."""
    # The Luminaris condition was met AFTER the card left; LKI is immutable
    assert not game_state.illusionist_lki.had_go_again


# ===== Scenario 21: LKI is not a legal target =====
# Tests Rule 1.2.3d - LKI is not a legal target


@scenario(
    "../features/section_1_2_objects.feature",
    "Last known information is not a legal target for effects",
)
def test_lki_is_not_legal_target():
    """Rule 1.2.3d: LKI is not an object and cannot be targeted."""
    pass


@given("an attack card has ceased to exist")
def attack_card_ceased_to_exist(game_state):
    """Rule 1.2.3d: A card is gone, leaving behind LKI."""
    game_state.gone_card = game_state.create_card(name="Gone Card")
    game_state.put_on_combat_chain(game_state.gone_card)
    game_state.gone_card_lki = game_state.remove_from_combat_chain(game_state.gone_card)


@given("its last known information has been captured")
def lki_has_been_captured(game_state):
    """Rule 1.2.3d: LKI snapshot exists for the gone card."""
    assert game_state.gone_card_lki is not None


@when("an effect attempts to target the last known information")
def effect_targets_lki(game_state):
    """Rule 1.2.3d: An effect tries to use LKI as a target."""
    game_state.targeting_result = game_state.target_object(game_state.gone_card_lki)


@then("the targeting fails because LKI is not a legal target")
def targeting_lki_fails(game_state):
    """Rule 1.2.3d: LKI is not a legal target; targeting fails."""
    assert not game_state.targeting_result.success
    assert game_state.targeting_result.reason == "lki_not_legal_target"


# ===== Scenario 22: Cards are sources of abilities =====
# Tests Rule 1.2.4 - Cards and macros are sources


@scenario(
    "../features/section_1_2_objects.feature",
    "A card is the source of its abilities and effects",
)
def test_card_is_source_of_abilities():
    """Rule 1.2.4: Cards are the source of abilities, effects, and attack-proxies."""
    pass


@given('a card named "Oasis Respite" with a prevention effect exists')
def oasis_respite_exists(game_state):
    """Rule 1.2.4: Oasis Respite card with prevention effect."""
    game_state.oasis_respite = game_state.create_card(name="Oasis Respite")
    game_state.oasis_respite_effect = game_state.create_prevention_effect(
        source=game_state.oasis_respite
    )


@when("the player declares the source of a prevention effect")
def player_declares_source(game_state):
    """Rule 1.2.4: Player declares which card/macro is the source of the effect."""
    game_state.declared_source = game_state.oasis_respite


@then("only cards or macros can be declared as the source")
def only_cards_or_macros_as_source(game_state):
    """Rule 1.2.4: Source must be a card or macro object."""
    # The engine should validate that the declared source is a card or macro
    assert game_state.is_valid_source(game_state.declared_source)
    assert isinstance(game_state.declared_source, CardInstance)


@then("the declared source is valid")
def declared_source_is_valid(game_state):
    """Rule 1.2.4: Oasis Respite card is a valid source."""
    result = game_state.validate_source_declaration(game_state.declared_source)
    assert result.is_valid


# ===== Scenario 23: Attack-proxy source is a card =====
# Tests Rule 1.2.4 - Attack-proxies originate from card sources


@scenario(
    "../features/section_1_2_objects.feature",
    "An attack-proxy's source is a card or macro object",
)
def test_attack_proxy_source_is_card():
    """Rule 1.2.4: Attack-proxies are sourced from card or macro objects."""
    pass


@given("a card creates an attack-proxy during play")
def card_creates_attack_proxy(game_state):
    """Rule 1.2.4: A card (source) creates an attack-proxy."""
    game_state.source_card = game_state.create_card(name="Proxy Source Card")
    game_state.created_proxy = game_state.create_attack_proxy(
        source=game_state.source_card
    )


@when("the engine checks the source of the attack-proxy")
def engine_checks_proxy_source(game_state):
    """Rule 1.2.4: Engine retrieves the source of the attack-proxy."""
    game_state.proxy_source = game_state.created_proxy.source


@then("the attack-proxy's source is the card object that created it")
def proxy_source_is_source_card(game_state):
    """Rule 1.2.4: Attack-proxy's source is the card that created it."""
    assert game_state.proxy_source is game_state.source_card


# ===== Fixtures =====


@pytest.fixture
def game_state():
    """
    Fixture providing game state for testing Section 1.2: Objects.

    Uses BDDGameState which integrates with the real engine.
    Reference: Rule 1.2
    """
    from tests.bdd_helpers import BDDGameState

    state = BDDGameState()

    # Initialize object tracking
    state.inspected_card = None
    state.owned_card = None
    state.hand_card = None
    state.arena_card = None
    state.stack_card = None
    state.object_identities = set()
    state.enumerated_objects = []
    state.equipment_card = None
    state.chain_card = None
    state.last_known_info = None
    state.endless_arrow = None
    state.chain_link_lki = None
    state.chain_card_2 = None
    state.generic_zone_reference_used = False
    state.buffed_card = None
    state.buffed_lki = None
    state.no_go_again_card = None
    state.no_go_again_lki = None
    state.modification_result = None
    state.illusionist_attack = None
    state.illusionist_lki = None
    state.gone_card = None
    state.gone_card_lki = None
    state.targeting_result = None
    state.oasis_respite = None
    state.oasis_respite_effect = None
    state.declared_source = None
    state.source_card = None
    state.created_proxy = None
    state.proxy_source = None
    state.attack_proxy = None
    state.checked_owner_id = None
    state.checked_controller = None

    return state
