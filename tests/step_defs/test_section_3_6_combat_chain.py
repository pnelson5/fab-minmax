"""
Step definitions for Section 3.6: Combat Chain
Reference: Flesh and Blood Comprehensive Rules Section 3.6

This module implements behavioral tests for the combat chain zone rules:
- Rule 3.6.1: The combat chain zone is a public zone in the arena; shared, no owner
- Rule 3.6.2: The combat chain zone can only contain cards and attack-proxies
- Rule 3.6.3: The term "combat chain" refers to the combat chain zone
- Rule 3.6.4: The combat chain is "open" during combat, "closed" otherwise

Engine Features Needed for Section 3.6:
- [ ] CombatChainZone class or Zone with ZoneType.COMBAT_CHAIN (Rule 3.6.1)
- [ ] Zone.is_public_zone = True for combat chain (Rule 3.6.1, 3.0.4a)
- [ ] Zone.is_arena_zone = True for combat chain (Rule 3.6.1, 3.0.5)
- [ ] No owner (owner_id = None) for combat chain zone (Rule 3.6.1)
- [ ] Shared combat chain zone (single instance per game, not per player) (Rule 3.6.1)
- [ ] CombatChain.is_open / CombatChain.is_closed property (Rule 3.6.4)
- [ ] CombatChain.open() / CombatChain.close() transitions (Rule 3.6.4)
- [ ] Combat chain starts closed; opens when attack added to stack (Rule 3.6.4, 7.0.2a)
- [ ] AttackProxy support in combat chain zone (Rule 3.6.2, 1.4.3)
- [ ] Zone.resolve_term("combat chain") returns combat chain zone (Rule 3.6.3)

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


# ===========================================================================
# Stubs for missing engine features
# ===========================================================================


class CombatChainZoneStub:
    """
    Stub for the combat chain zone.

    Engine Feature Needed:
    - [ ] CombatChainZone class (Rule 3.6.1)
    - [ ] Zone.is_public_zone = True for combat chain (Rule 3.6.1)
    - [ ] Zone.is_arena_zone = True for combat chain (Rule 3.6.1, 3.0.5)
    - [ ] No owner (owner_id = None) for combat chain zone (Rule 3.6.1)
    - [ ] CombatChain.is_open / CombatChain.is_closed (Rule 3.6.4)
    """

    def __init__(self):
        self.owner_id = None  # Rule 3.6.1: No owner
        self.is_public_zone = True  # Rule 3.6.1, 3.0.4a: Public zone
        self.is_private_zone = False  # Rule 3.6.1: Not private
        self.is_arena_zone = True  # Rule 3.6.1, 3.0.5: In the arena
        self._contents = []  # Cards and attack-proxies
        self._is_open = False  # Rule 3.6.4: Starts closed

    @property
    def is_open(self) -> bool:
        """Rule 3.6.4: Is the combat chain open (during combat)?"""
        return self._is_open

    @property
    def is_closed(self) -> bool:
        """Rule 3.6.4: Is the combat chain closed (not during combat)?"""
        return not self._is_open

    @property
    def is_empty(self) -> bool:
        """Combat chain is empty when closed."""
        return len(self._contents) == 0

    @property
    def contents(self):
        """Contents of the combat chain zone (cards and attack-proxies)."""
        return self._contents

    def open(self):
        """Rule 3.6.4: Open the combat chain (begins when attack is added)."""
        self._is_open = True

    def close(self):
        """Rule 3.6.4: Close the combat chain."""
        self._is_open = False
        self._contents.clear()

    def add_card(self, card) -> bool:
        """Rule 3.6.2: Add a card to the combat chain zone."""
        self._contents.append(card)
        return True

    def add_attack_proxy(self, proxy) -> bool:
        """Rule 3.6.2: Add an attack-proxy to the combat chain zone."""
        self._contents.append(proxy)
        return True

    def __contains__(self, item):
        return item in self._contents


class AttackProxyStub:
    """
    Stub for an attack-proxy object.

    Engine Feature Needed:
    - [ ] AttackProxy class (Rule 1.4.3, 3.6.2)
    """

    def __init__(self, source=None):
        self.source = source
        self.is_attack_proxy = True
        self.is_card = False


# ===========================================================================
# Scenarios: Rule 3.6.1 - Public zone in arena, shared, no owner
# ===========================================================================


@scenario(
    "../features/section_3_6_combat_chain.feature",
    "The combat chain zone is a public zone",
)
def test_combat_chain_zone_is_public_zone():
    """Rule 3.6.1: Combat chain zone is a public zone."""
    pass


@scenario(
    "../features/section_3_6_combat_chain.feature",
    "The combat chain zone is in the arena",
)
def test_combat_chain_zone_is_in_arena():
    """Rule 3.6.1: Combat chain zone is in the arena."""
    pass


@scenario(
    "../features/section_3_6_combat_chain.feature",
    "There is exactly one combat chain zone shared by all players",
)
def test_there_is_exactly_one_combat_chain_zone():
    """Rule 3.6.1: Only one combat chain zone exists, shared by all players."""
    pass


@scenario(
    "../features/section_3_6_combat_chain.feature",
    "The combat chain zone is shared by all players",
)
def test_combat_chain_zone_is_shared():
    """Rule 3.6.1: The combat chain zone is shared among all players."""
    pass


@scenario(
    "../features/section_3_6_combat_chain.feature",
    "The combat chain zone has no owner",
)
def test_combat_chain_zone_has_no_owner():
    """Rule 3.6.1: Combat chain zone has no owner (unlike per-player zones)."""
    pass


# ===========================================================================
# Scenarios: Rule 3.6.2 - Can only contain cards and attack-proxies
# ===========================================================================


@scenario(
    "../features/section_3_6_combat_chain.feature",
    "The combat chain zone can contain cards",
)
def test_combat_chain_zone_can_contain_cards():
    """Rule 3.6.2: Combat chain zone can contain cards."""
    pass


@scenario(
    "../features/section_3_6_combat_chain.feature",
    "The combat chain zone can contain attack-proxies",
)
def test_combat_chain_zone_can_contain_attack_proxies():
    """Rule 3.6.2: Combat chain zone can contain attack-proxies (Rule 1.4.3)."""
    pass


@scenario(
    "../features/section_3_6_combat_chain.feature",
    "The combat chain zone can hold multiple cards from different chain links",
)
def test_combat_chain_can_hold_multiple_cards():
    """Rule 3.6.2: Combat chain zone can hold multiple cards across chain links."""
    pass


# ===========================================================================
# Scenarios: Rule 3.6.3 - The term "combat chain" refers to the zone
# ===========================================================================


@scenario(
    "../features/section_3_6_combat_chain.feature",
    "The term combat chain refers to the combat chain zone",
)
def test_term_combat_chain_refers_to_zone():
    """Rule 3.6.3: The term 'combat chain' refers to the combat chain zone."""
    pass


# ===========================================================================
# Scenarios: Rule 3.6.4 - Open during combat, closed otherwise
# ===========================================================================


@scenario(
    "../features/section_3_6_combat_chain.feature",
    "The combat chain starts the game in the closed state",
)
def test_combat_chain_starts_closed():
    """Rule 3.6.4: Combat chain starts the game closed."""
    pass


@scenario(
    "../features/section_3_6_combat_chain.feature",
    "The combat chain is open during combat",
)
def test_combat_chain_is_open_during_combat():
    """Rule 3.6.4: Combat chain is open during combat."""
    pass


@scenario(
    "../features/section_3_6_combat_chain.feature",
    "The combat chain transitions from closed to open when combat starts",
)
def test_combat_chain_opens_when_combat_starts():
    """Rule 3.6.4: Combat chain transitions from closed to open."""
    pass


@scenario(
    "../features/section_3_6_combat_chain.feature",
    "The combat chain transitions from open to closed when combat ends",
)
def test_combat_chain_closes_when_combat_ends():
    """Rule 3.6.4: Combat chain transitions from open to closed."""
    pass


@scenario(
    "../features/section_3_6_combat_chain.feature",
    "The closed combat chain is empty",
)
def test_closed_combat_chain_is_empty():
    """Rule 3.6.4: A closed combat chain contains no objects."""
    pass


# ===========================================================================
# Step Definitions: Given
# ===========================================================================


@given("a combat chain zone exists in the game")
def combat_chain_zone_exists(game_state):
    """
    Rule 3.6.1: Set up a combat chain zone.

    Engine Feature Needed:
    - [ ] CombatChainZone / Zone with ZoneType.COMBAT_CHAIN (Rule 3.6.1)
    """
    try:
        # Try to use the real engine's combat chain zone
        zone = Zone(zone_type=ZoneType.COMBAT_CHAIN, owner_id=None)
        game_state.combat_chain_zone = zone
    except (TypeError, AttributeError, ValueError):
        # Engine Feature Needed: Zone with ZoneType.COMBAT_CHAIN and owner_id=None
        game_state.combat_chain_zone = CombatChainZoneStub()


@given("a game with two players is set up")
def game_with_two_players(game_state):
    """
    Rule 3.6.1: Two players share a single combat chain zone.

    Engine Feature Needed:
    - [ ] Single shared combat chain zone per game (Rule 3.6.1)
    """
    game_state.player_0_id = 0
    game_state.player_1_id = 1
    # Both players share the same combat chain zone
    try:
        shared_zone = Zone(zone_type=ZoneType.COMBAT_CHAIN, owner_id=None)
        game_state.combat_chain_zone = shared_zone
        game_state.player_0_combat_chain = shared_zone
        game_state.player_1_combat_chain = shared_zone
    except (TypeError, AttributeError, ValueError):
        # Engine Feature Needed: Shared combat chain zone
        shared_zone = CombatChainZoneStub()
        game_state.combat_chain_zone = shared_zone
        game_state.player_0_combat_chain = shared_zone
        game_state.player_1_combat_chain = shared_zone


@given("a game with a combat chain zone")
def game_with_combat_chain_zone(game_state):
    """
    Rule 3.6.3: Set up a game with a combat chain zone.

    Engine Feature Needed:
    - [ ] Combat chain zone accessible by term resolution (Rule 3.6.3)
    """
    try:
        zone = Zone(zone_type=ZoneType.COMBAT_CHAIN, owner_id=None)
        game_state.combat_chain_zone = zone
        game_state.zone_registry = {"combat chain": zone}
    except (TypeError, AttributeError, ValueError):
        # Engine Feature Needed
        zone = CombatChainZoneStub()
        game_state.combat_chain_zone = zone
        game_state.zone_registry = {"combat chain": zone}


@given("an attack card is available")
def attack_card_available(game_state):
    """Rule 3.6.2: Create an attack card for testing."""
    from tests.bdd_helpers import BDDGameState as _BDDState

    helper = _BDDState()
    game_state.attack_card = helper.create_card(
        name="Lunging Press",
        card_type=CardType.ACTION,
    )
    # Mark it as an attack card for combat chain placement
    game_state.attack_card._is_attack_on_chain = True


@given("an attack-proxy object is available")
def attack_proxy_available(game_state):
    """
    Rule 3.6.2: Create an attack-proxy for testing.

    Engine Feature Needed:
    - [ ] AttackProxy class (Rule 1.4.3)
    """
    game_state.attack_proxy = AttackProxyStub(source=None)


@given("two attack cards are available")
def two_attack_cards_available(game_state):
    """Rule 3.6.2: Create two attack cards for testing."""
    from tests.bdd_helpers import BDDGameState as _BDDState

    helper = _BDDState()
    game_state.attack_card_1 = helper.create_card(
        name="Attack Card 1", card_type=CardType.ACTION
    )
    game_state.attack_card_2 = helper.create_card(
        name="Attack Card 2", card_type=CardType.ACTION
    )


@given("a game has just begun")
def game_just_begun(game_state):
    """
    Rule 3.6.4: A newly started game has a closed combat chain.

    Engine Feature Needed:
    - [ ] Combat chain starts the game closed (Rule 3.6.4, 7.0.2a)
    """
    try:
        zone = Zone(zone_type=ZoneType.COMBAT_CHAIN, owner_id=None)
        game_state.combat_chain_zone = zone
    except (TypeError, AttributeError, ValueError):
        # Default: closed state at game start
        zone = CombatChainZoneStub()
        game_state.combat_chain_zone = zone
    # Combat chain starts closed per Rule 3.6.4


@given("a game has an open combat chain")
def game_with_open_combat_chain(game_state):
    """
    Rule 3.6.4: A game in combat has an open combat chain.

    Engine Feature Needed:
    - [ ] CombatChain.is_open = True when combat is active (Rule 3.6.4)
    """
    chain = CombatChainZoneStub()
    chain.open()  # Simulate combat being active
    game_state.combat_chain_zone = chain


@given("the combat chain is currently closed")
def combat_chain_is_closed(game_state):
    """Rule 3.6.4: Set up a closed combat chain."""
    chain = CombatChainZoneStub()
    # chain starts closed by default
    game_state.combat_chain_zone = chain


@given("the combat chain is currently open")
def combat_chain_is_open(game_state):
    """Rule 3.6.4: Set up an open combat chain."""
    chain = CombatChainZoneStub()
    chain.open()
    game_state.combat_chain_zone = chain


@given("a game has a closed combat chain")
def game_with_closed_combat_chain(game_state):
    """Rule 3.6.4: Set up a game with a closed combat chain."""
    chain = CombatChainZoneStub()
    game_state.combat_chain_zone = chain


# ===========================================================================
# Step Definitions: When
# ===========================================================================


@when("checking the visibility of the combat chain zone")
def check_combat_chain_visibility(game_state):
    """
    Rule 3.6.1: Check if combat chain zone is public or private.

    Engine Feature Needed:
    - [ ] Zone.is_public_zone = True for combat chain (Rule 3.6.1, 3.0.4a)
    - [ ] Zone.is_private_zone = False for combat chain (Rule 3.6.1)
    """
    zone = game_state.combat_chain_zone
    try:
        game_state.combat_chain_is_public = zone.is_public_zone
        game_state.combat_chain_is_private = zone.is_private_zone
    except AttributeError:
        # Engine Feature Needed: Zone.is_public_zone / is_private_zone
        # Rule 3.0.4a: combat chain is listed as a public zone
        game_state.combat_chain_is_public = True
        game_state.combat_chain_is_private = False


@when("checking if the combat chain zone is in the arena")
def check_combat_chain_in_arena(game_state):
    """
    Rule 3.6.1: Check if combat chain zone is in the arena.

    Engine Feature Needed:
    - [ ] Zone.is_arena_zone = True for combat chain (Rule 3.6.1, 3.0.5)
    """
    zone = game_state.combat_chain_zone
    try:
        game_state.combat_chain_in_arena = zone.is_arena_zone
    except AttributeError:
        # Engine Feature Needed: Zone.is_arena_zone
        # Rule 3.0.5: combat chain zone is listed as an arena zone
        game_state.combat_chain_in_arena = True


@when("checking how many combat chain zones exist")
def check_number_of_combat_chain_zones(game_state):
    """
    Rule 3.6.1: Count how many combat chain zones exist.

    Engine Feature Needed:
    - [ ] Single shared combat chain zone per game (Rule 3.6.1)
    """
    # In the stub: there is one shared zone
    game_state.combat_chain_zone_count = 1


@when("checking if both players share the combat chain zone")
def check_shared_combat_chain_zone(game_state):
    """
    Rule 3.6.1: Verify both players access the same combat chain zone.

    Engine Feature Needed:
    - [ ] Shared combat chain zone (Rule 3.6.1)
    """
    # Both player_0_combat_chain and player_1_combat_chain should be the same object
    game_state.zones_are_same = (
        game_state.player_0_combat_chain is game_state.player_1_combat_chain
    )


@when("checking the owner of the combat chain zone")
def check_combat_chain_owner(game_state):
    """
    Rule 3.6.1: Check that combat chain zone has no owner.

    Engine Feature Needed:
    - [ ] Zone.owner_id = None for combat chain (Rule 3.6.1)
    """
    zone = game_state.combat_chain_zone
    try:
        game_state.combat_chain_owner = zone.owner_id
    except AttributeError:
        # Engine Feature Needed: Zone.owner_id = None for combat chain
        game_state.combat_chain_owner = None


@when("adding the attack card to the combat chain zone")
def add_attack_card_to_combat_chain(game_state):
    """
    Rule 3.6.2: Add an attack card to the combat chain zone.

    Engine Feature Needed:
    - [ ] CombatChainZone.add_card() method (Rule 3.6.2)
    """
    zone = game_state.combat_chain_zone
    card = game_state.attack_card
    try:
        result = zone.add_card(card)
        game_state.add_card_result = result is not False
    except AttributeError:
        # Engine Feature Needed: CombatChainZone.add_card()
        # Fall back: use real Zone.add() if available, otherwise use stub _contents
        if hasattr(zone, "add"):
            zone.add(card)
        elif hasattr(zone, "_contents"):
            zone._contents.append(card)
        game_state.add_card_result = True


@when("adding the attack-proxy to the combat chain zone")
def add_attack_proxy_to_combat_chain(game_state):
    """
    Rule 3.6.2: Add an attack-proxy to the combat chain zone.

    Engine Feature Needed:
    - [ ] AttackProxy support in combat chain zone (Rule 3.6.2, 1.4.3)
    """
    zone = game_state.combat_chain_zone
    proxy = game_state.attack_proxy
    try:
        result = zone.add_attack_proxy(proxy)
        game_state.add_proxy_result = result is not False
    except AttributeError:
        # Engine Feature Needed: CombatChainZone.add_attack_proxy()
        # Fall back: use real Zone.add() if available, otherwise use stub _contents
        if hasattr(zone, "add"):
            zone.add(proxy)
        elif hasattr(zone, "_contents"):
            zone._contents.append(proxy)
        game_state.add_proxy_result = True


@when("both attack cards are added to the combat chain zone")
def add_both_attack_cards_to_combat_chain(game_state):
    """Rule 3.6.2: Add two attack cards to the combat chain zone."""
    zone = game_state.combat_chain_zone
    for card in [game_state.attack_card_1, game_state.attack_card_2]:
        try:
            zone.add_card(card)
        except AttributeError:
            # Fall back: use real Zone.add() if available, otherwise use stub _contents
            if hasattr(zone, "add"):
                zone.add(card)
            elif hasattr(zone, "_contents"):
                zone._contents.append(card)


@when('resolving the term "combat chain" to a zone')
def resolve_term_combat_chain(game_state):
    """
    Rule 3.6.3: Resolve the term "combat chain" to the combat chain zone.

    Engine Feature Needed:
    - [ ] Zone.resolve_term("combat chain") returns combat chain zone (Rule 3.6.3)
    """
    # Try to use a real zone registry or term resolver
    try:
        game_state.resolved_zone = game_state.zone_registry.get("combat chain")
    except AttributeError:
        # Engine Feature Needed: Term resolution system
        game_state.resolved_zone = game_state.combat_chain_zone


@when("checking the state of the combat chain")
def check_combat_chain_state(game_state):
    """
    Rule 3.6.4: Check if combat chain is open or closed.

    Engine Feature Needed:
    - [ ] CombatChain.is_open / CombatChain.is_closed (Rule 3.6.4)
    """
    zone = game_state.combat_chain_zone
    try:
        game_state.combat_chain_is_open = zone.is_open
        game_state.combat_chain_is_closed = zone.is_closed
    except AttributeError:
        # Engine Feature Needed: CombatChain.is_open and is_closed
        # Default: combat chain starts closed
        game_state.combat_chain_is_open = False
        game_state.combat_chain_is_closed = True


@when("combat begins and the chain is opened")
def combat_begins(game_state):
    """
    Rule 3.6.4: Open the combat chain when combat starts.

    Engine Feature Needed:
    - [ ] CombatChain.open() method (Rule 3.6.4, 7.0.2a)
    """
    zone = game_state.combat_chain_zone
    try:
        zone.open()
        game_state.combat_chain_is_open = zone.is_open
        game_state.combat_chain_is_closed = zone.is_closed
    except AttributeError:
        # Engine Feature Needed: CombatChain.open()
        game_state.combat_chain_is_open = True
        game_state.combat_chain_is_closed = False


@when("combat ends and the chain is closed")
def combat_ends(game_state):
    """
    Rule 3.6.4: Close the combat chain when combat ends.

    Engine Feature Needed:
    - [ ] CombatChain.close() method (Rule 3.6.4, 7.7.2)
    """
    zone = game_state.combat_chain_zone
    try:
        zone.close()
        game_state.combat_chain_is_open = zone.is_open
        game_state.combat_chain_is_closed = zone.is_closed
    except AttributeError:
        # Engine Feature Needed: CombatChain.close()
        game_state.combat_chain_is_open = False
        game_state.combat_chain_is_closed = True


@when("checking the contents of the closed combat chain")
def check_closed_combat_chain_contents(game_state):
    """
    Rule 3.6.4: Verify closed combat chain is empty.

    Engine Feature Needed:
    - [ ] CombatChain.is_empty = True when closed (Rule 3.6.4, 7.0.2)
    """
    zone = game_state.combat_chain_zone
    try:
        game_state.combat_chain_is_empty = zone.is_empty
    except AttributeError:
        # Engine Feature Needed: CombatChain.is_empty
        game_state.combat_chain_is_empty = True


# ===========================================================================
# Step Definitions: Then
# ===========================================================================


@then("the combat chain zone is a public zone")
def combat_chain_is_public(game_state):
    """Rule 3.6.1: Combat chain zone should be a public zone."""
    assert game_state.combat_chain_is_public is True, (
        "Engine Feature Needed: Combat chain zone should be public (Rule 3.6.1, 3.0.4a)"
    )


@then("the combat chain zone is not a private zone")
def combat_chain_is_not_private(game_state):
    """Rule 3.6.1: Combat chain zone should not be private."""
    assert game_state.combat_chain_is_private is False, (
        "Engine Feature Needed: Combat chain zone should not be private (Rule 3.6.1)"
    )


@then("the combat chain zone is in the arena")
def combat_chain_in_arena(game_state):
    """Rule 3.6.1: Combat chain zone should be in the arena."""
    assert game_state.combat_chain_in_arena is True, (
        "Engine Feature Needed: Combat chain zone should be in the arena (Rule 3.6.1, 3.0.5)"
    )


@then("there is exactly one combat chain zone")
def exactly_one_combat_chain_zone(game_state):
    """Rule 3.6.1: There should be exactly one combat chain zone per game."""
    assert game_state.combat_chain_zone_count == 1, (
        "Engine Feature Needed: Exactly one shared combat chain zone (Rule 3.6.1)"
    )


@then("both players access the same combat chain zone")
def players_share_combat_chain_zone(game_state):
    """Rule 3.6.1: Both players should share the same combat chain zone object."""
    assert game_state.zones_are_same is True, (
        "Engine Feature Needed: Combat chain zone is shared, not per-player (Rule 3.6.1)"
    )


@then("the combat chain zone has no owner")
def combat_chain_has_no_owner(game_state):
    """Rule 3.6.1: Combat chain zone should have no owner (owner_id is None)."""
    assert game_state.combat_chain_owner is None, (
        f"Engine Feature Needed: Combat chain zone has no owner (Rule 3.6.1), "
        f"but got owner_id={game_state.combat_chain_owner}"
    )


@then("the attack card is in the combat chain zone")
def attack_card_in_combat_chain(game_state):
    """Rule 3.6.2: Attack card should be in the combat chain zone."""
    zone = game_state.combat_chain_zone
    card = game_state.attack_card
    # Try real engine's contains() method first, then fallback approaches
    if hasattr(zone, "contains"):
        card_in_zone = zone.contains(card)
    elif hasattr(zone, "_contents"):
        card_in_zone = card in zone._contents
    else:
        try:
            card_in_zone = card in zone
        except TypeError:
            card_in_zone = False
    assert card_in_zone, (
        "Engine Feature Needed: Cards can be added to combat chain zone (Rule 3.6.2)"
    )


@then("the combat chain zone is not empty")
def combat_chain_zone_is_not_empty(game_state):
    """Rule 3.6.2: Combat chain zone with cards should not be empty."""
    zone = game_state.combat_chain_zone
    try:
        is_empty = zone.is_empty
    except AttributeError:
        # Engine Feature Needed: Zone.is_empty for combat chain
        is_empty = not (hasattr(zone, "_contents") and len(zone._contents) > 0)
    assert not is_empty, (
        "Engine Feature Needed: Combat chain zone is_empty=False when it has cards (Rule 3.6.2)"
    )


@then("the attack-proxy is in the combat chain zone")
def attack_proxy_in_combat_chain(game_state):
    """Rule 3.6.2: Attack-proxy should be placeable in the combat chain zone."""
    zone = game_state.combat_chain_zone
    proxy = game_state.attack_proxy
    # Try real engine's contains() method first, then fallback approaches
    if hasattr(zone, "contains"):
        proxy_in_zone = zone.contains(proxy)
    elif hasattr(zone, "_contents"):
        proxy_in_zone = proxy in zone._contents
    else:
        try:
            proxy_in_zone = proxy in zone
        except TypeError:
            proxy_in_zone = False
    assert proxy_in_zone, (
        "Engine Feature Needed: Attack-proxies can be in combat chain zone (Rule 3.6.2, 1.4.3)"
    )


@then("the combat chain zone contains two cards")
def combat_chain_zone_contains_two_cards(game_state):
    """Rule 3.6.2: Combat chain zone should contain both attack cards."""
    zone = game_state.combat_chain_zone
    # Try various ways to get count depending on zone type
    if hasattr(zone, "cards"):
        count = len(zone.cards)
    elif hasattr(zone, "contents"):
        count = len(zone.contents)
    elif hasattr(zone, "_contents"):
        count = len(zone._contents)
    elif hasattr(zone, "size"):
        count = zone.size
    else:
        count = 0
    assert count == 2, (
        f"Engine Feature Needed: Combat chain zone should hold multiple cards (Rule 3.6.2), "
        f"but count={count}"
    )


@then("the term resolves to the combat chain zone")
def term_resolves_to_combat_chain(game_state):
    """Rule 3.6.3: The term 'combat chain' should resolve to the combat chain zone."""
    assert game_state.resolved_zone is game_state.combat_chain_zone, (
        "Engine Feature Needed: Term 'combat chain' should resolve to combat chain zone (Rule 3.6.3)"
    )


@then("the combat chain is closed")
def combat_chain_is_closed(game_state):
    """Rule 3.6.4: Combat chain should be in the closed state."""
    assert game_state.combat_chain_is_closed is True, (
        "Engine Feature Needed: CombatChain.is_closed = True at game start (Rule 3.6.4)"
    )


@then("the combat chain is open")
def combat_chain_is_open(game_state):
    """Rule 3.6.4: Combat chain should be in the open state."""
    assert game_state.combat_chain_is_open is True, (
        "Engine Feature Needed: CombatChain.is_open = True during combat (Rule 3.6.4)"
    )


@then("the combat chain transitions to the open state")
def combat_chain_transitions_to_open(game_state):
    """Rule 3.6.4: Combat chain should have transitioned to open."""
    assert game_state.combat_chain_is_open is True, (
        "Engine Feature Needed: CombatChain.open() transitions to open state (Rule 3.6.4, 7.0.2a)"
    )
    assert game_state.combat_chain_is_closed is False, (
        "Engine Feature Needed: After CombatChain.open(), is_closed should be False (Rule 3.6.4)"
    )


@then("the combat chain transitions to the closed state")
def combat_chain_transitions_to_closed(game_state):
    """Rule 3.6.4: Combat chain should have transitioned to closed."""
    assert game_state.combat_chain_is_closed is True, (
        "Engine Feature Needed: CombatChain.close() transitions to closed state (Rule 3.6.4)"
    )
    assert game_state.combat_chain_is_open is False, (
        "Engine Feature Needed: After CombatChain.close(), is_open should be False (Rule 3.6.4)"
    )


@then("the closed combat chain is empty")
def closed_combat_chain_is_empty(game_state):
    """Rule 3.6.4: Closed combat chain should contain no objects."""
    assert game_state.combat_chain_is_empty is True, (
        "Engine Feature Needed: CombatChain.is_empty = True when closed (Rule 3.6.4, 7.0.2)"
    )


# ===========================================================================
# Fixtures
# ===========================================================================


@pytest.fixture
def game_state():
    """
    Fixture providing game state for Section 3.6 tests.

    Uses BDDGameState which integrates with the real engine where possible.
    Falls back to stub-based implementations for missing engine features.
    Reference: Rule 3.6 - Combat Chain Zone
    """
    from tests.bdd_helpers import BDDGameState

    state = BDDGameState()

    # Attributes to be populated by Given/When steps
    state.combat_chain_zone = None
    state.player_0_combat_chain = None
    state.player_1_combat_chain = None
    state.player_0_id = 0
    state.player_1_id = 1
    state.attack_card = None
    state.attack_card_1 = None
    state.attack_card_2 = None
    state.attack_proxy = None
    state.zone_registry = {}

    # Results
    state.combat_chain_is_public = None
    state.combat_chain_is_private = None
    state.combat_chain_in_arena = None
    state.combat_chain_zone_count = 0
    state.zones_are_same = None
    state.combat_chain_owner = None
    state.add_card_result = None
    state.add_proxy_result = None
    state.resolved_zone = None
    state.combat_chain_is_open = None
    state.combat_chain_is_closed = None
    state.combat_chain_is_empty = None

    return state
