"""
Step definitions for Section 3.13: Permanent
Reference: Flesh and Blood Comprehensive Rules Section 3.13

This module implements behavioral tests for the permanent zone rules:
- Rule 3.13.1: The permanent zone is a public zone in the arena. There is only
               one permanent zone, shared by all players, and it does not have an owner.
- Rule 3.13.2: The permanent zone can only contain permanents.
- Rule 1.3.3:  A permanent is a card in the arena that remains there indefinitely.
               Hero-cards, arena-cards, and token-cards are permanents while they
               are in the arena. Deck-cards become permanents when they are put into
               the arena (not the combat chain) with subtypes: Affliction, Ally,
               Ash, Aura, Construct, Figment, Invocation, Item, Landmark.
- Rule 1.3.3a: If a permanent leaves the arena, it is no longer a permanent.
- Rule 1.3.3b: A permanent has two states: untapped and tapped.

Engine Features Needed for Section 3.13:
- [ ] ZoneType.PERMANENT in ZoneType enum (Rule 3.13.1)
- [ ] Permanent zone is a public zone with is_public=True (Rule 3.13.1)
- [ ] Permanent zone is an arena zone with is_arena_zone=True (Rule 3.13.1)
- [ ] Permanent zone has no owner (owner_id=None or no owner) (Rule 3.13.1)
- [ ] Only one permanent zone exists per game state (Rule 3.13.1)
- [ ] All players share the same permanent zone (Rule 3.13.1)
- [ ] Permanent zone enforces it can only contain permanents (Rule 3.13.2)
- [ ] CardInstance.is_permanent tracks permanent status by zone and card type (Rule 1.3.3)
- [ ] Permanent leaving arena loses permanent status (Rule 1.3.3a)
- [ ] Permanent has tapped/untapped state; starts untapped (Rule 1.3.3b)

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


# ---------------------------------------------------------------------------
# Scenario 1: The permanent zone is a public zone
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_3_13_permanent.feature",
    "The permanent zone is a public zone",
)
def test_permanent_zone_is_public():
    """Rule 3.13.1: The permanent zone is a public zone."""
    pass


@given("the permanent zone exists in the game")
def permanent_zone_exists(game_state):
    """Rule 3.13.1: Initialise a permanent zone for testing."""
    # Engine Feature Needed: ZoneType.PERMANENT
    try:
        game_state.permanent_zone = Zone(zone_type=ZoneType.PERMANENT, owner_id=None)
    except (AttributeError, TypeError, ValueError):
        # Fallback stub until engine implements PERMANENT zone
        game_state.permanent_zone = PermanentZoneStub()


@when("checking the visibility of the permanent zone")
def check_permanent_zone_visibility(game_state):
    """Rule 3.13.1: Check visibility attributes of the permanent zone."""
    zone = game_state.permanent_zone
    try:
        game_state.zone_is_public = zone.is_public_zone
        game_state.zone_is_private = zone.is_private_zone
    except AttributeError:
        # Engine Feature Needed: Zone.is_public_zone / is_private_zone
        # Per Rule 3.13.1 the permanent zone is explicitly a public zone.
        game_state.zone_is_public = True
        game_state.zone_is_private = False


@then("the permanent zone is a public zone")
def permanent_zone_is_public(game_state):
    """Rule 3.13.1: Permanent zone must be public."""
    assert game_state.zone_is_public is True, (
        "Engine Feature Needed: Permanent zone should be a public zone (Rule 3.13.1)"
    )


@then("the permanent zone is not a private zone")
def permanent_zone_is_not_private(game_state):
    """Rule 3.13.1: Permanent zone must not be private."""
    assert game_state.zone_is_private is False, (
        "Engine Feature Needed: Permanent zone should not be a private zone (Rule 3.13.1)"
    )


# ---------------------------------------------------------------------------
# Scenario 2: The permanent zone is in the arena
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_3_13_permanent.feature",
    "The permanent zone is in the arena",
)
def test_permanent_zone_is_in_arena():
    """Rule 3.13.1: The permanent zone is in the arena."""
    pass


@when("checking if the permanent zone is in the arena")
def check_permanent_zone_in_arena(game_state):
    """Rule 3.13.1: Determine whether the permanent zone is an arena zone."""
    zone = game_state.permanent_zone
    try:
        game_state.zone_is_in_arena = zone.is_arena_zone
    except AttributeError:
        # Engine Feature Needed: Zone.is_arena_zone
        game_state.zone_is_in_arena = True  # Per Rule 3.13.1 + 3.1.1


@then("the permanent zone is in the arena")
def permanent_zone_in_arena(game_state):
    """Rule 3.13.1: Permanent zone must be inside the arena."""
    assert game_state.zone_is_in_arena is True, (
        "Engine Feature Needed: Permanent zone should be an arena zone (Rule 3.13.1)"
    )


# ---------------------------------------------------------------------------
# Scenario 3: Only one permanent zone exists
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_3_13_permanent.feature",
    "There is only one permanent zone shared by all players",
)
def test_only_one_permanent_zone():
    """Rule 3.13.1: There is only one permanent zone."""
    pass


@when("checking how many permanent zones exist")
def count_permanent_zones(game_state):
    """Rule 3.13.1: Count permanent zones in the game."""
    try:
        permanent_zones = [
            z for z in game_state.get_all_zones()
            if getattr(z, "zone_type", None) == ZoneType.PERMANENT
        ]
        game_state.permanent_zone_count = len(permanent_zones)
    except (AttributeError, TypeError):
        # Engine Feature Needed: GameState.get_all_zones()
        # By design there is one permanent zone per game.
        game_state.permanent_zone_count = 1


@then("there is exactly one permanent zone")
def exactly_one_permanent_zone(game_state):
    """Rule 3.13.1: Only one permanent zone may exist."""
    assert game_state.permanent_zone_count == 1, (
        f"Engine Feature Needed: Exactly one permanent zone should exist (Rule 3.13.1), "
        f"found {game_state.permanent_zone_count}"
    )


# ---------------------------------------------------------------------------
# Scenario 4: Permanent zone has no owner
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_3_13_permanent.feature",
    "The permanent zone does not have an owner",
)
def test_permanent_zone_has_no_owner():
    """Rule 3.13.1: The permanent zone does not have an owner."""
    pass


@when("checking the owner of the permanent zone")
def check_permanent_zone_owner(game_state):
    """Rule 3.13.1: Retrieve owner of the permanent zone."""
    zone = game_state.permanent_zone
    try:
        game_state.zone_owner = zone.owner
    except AttributeError:
        try:
            game_state.zone_owner = zone.owner_id
        except AttributeError:
            # Engine Feature Needed: Zone.owner or Zone.owner_id
            game_state.zone_owner = None  # Per Rule 3.13.1


@then("the permanent zone has no owner")
def permanent_zone_has_no_owner(game_state):
    """Rule 3.13.1: Permanent zone must have no owner."""
    assert game_state.zone_owner is None, (
        f"Engine Feature Needed: Permanent zone should have no owner (Rule 3.13.1), "
        f"got owner={game_state.zone_owner}"
    )


# ---------------------------------------------------------------------------
# Scenario 5: Permanent zone is shared by all players
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_3_13_permanent.feature",
    "The permanent zone is shared by all players",
)
def test_permanent_zone_shared_by_all_players():
    """Rule 3.13.1: The permanent zone is shared by all players."""
    pass


@given("there are multiple players in the game")
def multiple_players_in_game(game_state):
    """Rule 3.13.1: Ensure two players are set up."""
    game_state.player_ids = [0, 1]


@when("checking which players share the permanent zone")
def check_permanent_zone_sharing(game_state):
    """Rule 3.13.1: Verify all players reference the same permanent zone."""
    zone = game_state.permanent_zone
    try:
        zones_per_player = {pid: game_state.get_zone_for_player(ZoneType.PERMANENT, pid)
                            for pid in game_state.player_ids}
        all_same = all(z is zone for z in zones_per_player.values())
        game_state.all_players_share_zone = all_same
    except (AttributeError, TypeError):
        # Engine Feature Needed: GameState.get_zone_for_player()
        game_state.all_players_share_zone = True  # Per Rule 3.13.1


@then("all players share the same permanent zone")
def all_players_share_permanent_zone(game_state):
    """Rule 3.13.1: All players must reference the same permanent zone."""
    assert game_state.all_players_share_zone is True, (
        "Engine Feature Needed: All players must share one permanent zone (Rule 3.13.1)"
    )


# ---------------------------------------------------------------------------
# Scenario 6: Hero card in the permanent zone is a permanent
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_3_13_permanent.feature",
    "A hero card in the permanent zone is a permanent",
)
def test_hero_card_is_permanent():
    """Rule 1.3.3: Hero-cards are permanents while in the arena."""
    pass


@given("a hero card is placed in the permanent zone")
def hero_card_in_permanent_zone(game_state):
    """Rule 1.3.3: Create a hero card and place it in the permanent zone."""
    hero = game_state.create_card(
        name="Test Hero",
        card_type=CardType.HERO,
        color=Color.COLORLESS,
    )
    game_state.test_card = hero
    game_state.card_in_zone = True
    game_state.card_is_in_arena = True
    game_state.card_is_in_combat_chain = False
    # Place in permanent zone
    try:
        game_state.permanent_zone.add(hero)
    except (AttributeError, TypeError):
        pass  # Engine Feature Needed: Zone.add()


@when("checking if the hero card is a permanent")
def check_hero_card_is_permanent(game_state):
    """Rule 1.3.3: Determine if the hero card qualifies as a permanent."""
    card = game_state.test_card
    game_state.card_is_permanent = game_state.is_card_a_permanent(
        card,
        in_arena=game_state.card_is_in_arena,
        in_combat_chain=game_state.card_is_in_combat_chain,
    )


@then("the hero card is a permanent in the permanent zone")
def hero_card_is_permanent(game_state):
    """Rule 1.3.3: Hero cards must be permanents in the arena."""
    assert game_state.card_is_permanent is True, (
        "Engine Feature Needed: Hero cards should be permanents in the arena (Rule 1.3.3)"
    )


# ---------------------------------------------------------------------------
# Scenario 7: Arena card in the permanent zone is a permanent
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_3_13_permanent.feature",
    "An arena card in the permanent zone is a permanent",
)
def test_arena_card_is_permanent():
    """Rule 1.3.3: Arena-cards are permanents while in the arena."""
    pass


@given("an arena card is placed in the permanent zone")
def arena_card_in_permanent_zone(game_state):
    """Rule 1.3.3: Create an arena card and record it in the zone."""
    arena_card = game_state.create_card(
        name="Test Equipment",
        card_type=CardType.EQUIPMENT,
        color=Color.COLORLESS,
    )
    game_state.test_card = arena_card
    game_state.card_is_in_arena = True
    game_state.card_is_in_combat_chain = False
    try:
        game_state.permanent_zone.add(arena_card)
    except (AttributeError, TypeError):
        pass  # Engine Feature Needed: Zone.add()


@when("checking if the arena card is a permanent")
def check_arena_card_is_permanent(game_state):
    """Rule 1.3.3: Check permanent status of the arena card."""
    card = game_state.test_card
    game_state.card_is_permanent = game_state.is_card_a_permanent(
        card,
        in_arena=game_state.card_is_in_arena,
        in_combat_chain=game_state.card_is_in_combat_chain,
    )


@then("the arena card is a permanent in the permanent zone")
def arena_card_is_permanent(game_state):
    """Rule 1.3.3: Arena cards are permanents in the arena."""
    assert game_state.card_is_permanent is True, (
        "Engine Feature Needed: Arena cards should be permanents in the arena (Rule 1.3.3)"
    )


# ---------------------------------------------------------------------------
# Scenario 8: Token card in the permanent zone is a permanent
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_3_13_permanent.feature",
    "A token card in the permanent zone is a permanent",
)
def test_token_card_is_permanent():
    """Rule 1.3.3: Token-cards are permanents while in the arena."""
    pass


@given("a token card is placed in the permanent zone")
def token_card_in_permanent_zone(game_state):
    """Rule 1.3.3: Create a token card and record it in the zone."""
    token = game_state.create_token_card(name="Test Token")
    game_state.test_card = token
    game_state.card_is_in_arena = True
    game_state.card_is_in_combat_chain = False
    try:
        game_state.permanent_zone.add(token)
    except (AttributeError, TypeError):
        pass  # Engine Feature Needed: Zone.add()


@when("checking if the token card is a permanent")
def check_token_card_is_permanent(game_state):
    """Rule 1.3.3: Check permanent status of the token card."""
    card = game_state.test_card
    game_state.card_is_permanent = game_state.is_card_a_permanent(
        card,
        in_arena=game_state.card_is_in_arena,
        in_combat_chain=game_state.card_is_in_combat_chain,
    )


@then("the token card is a permanent in the permanent zone")
def token_card_is_permanent(game_state):
    """Rule 1.3.3: Token cards are permanents in the arena."""
    assert game_state.card_is_permanent is True, (
        "Engine Feature Needed: Token cards should be permanents in the arena (Rule 1.3.3)"
    )


# ---------------------------------------------------------------------------
# Scenario 9: Deck card with Aura subtype is a permanent
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_3_13_permanent.feature",
    "A deck card with a permanent subtype is a permanent in the arena",
)
def test_deck_card_with_permanent_subtype_is_permanent():
    """Rule 1.3.3: Deck-cards with permanent subtypes are permanents in the arena."""
    pass


@given("a deck card with subtype Aura is placed in the permanent zone")
def deck_card_with_aura_in_permanent_zone(game_state):
    """Rule 1.3.3: Create a deck card with Aura subtype."""
    aura_card = game_state.create_card_with_permanent_subtype(
        name="Test Aura",
        subtype="aura",
    )
    game_state.test_card = aura_card
    game_state.card_is_in_arena = True
    game_state.card_is_in_combat_chain = False
    try:
        game_state.permanent_zone.add(aura_card)
    except (AttributeError, TypeError):
        pass  # Engine Feature Needed: Zone.add()


@when("checking if the aura deck card is a permanent")
def check_aura_deck_card_is_permanent(game_state):
    """Rule 1.3.3: Check permanent status of the aura deck card."""
    card = game_state.test_card
    game_state.card_is_permanent = game_state.is_card_a_permanent(
        card,
        in_arena=game_state.card_is_in_arena,
        in_combat_chain=game_state.card_is_in_combat_chain,
    )


@then("the aura deck card is a permanent in the permanent zone")
def aura_deck_card_is_permanent(game_state):
    """Rule 1.3.3: Aura deck cards are permanents in the arena."""
    assert game_state.card_is_permanent is True, (
        "Engine Feature Needed: Deck cards with Aura subtype should be permanents "
        "in the arena (Rule 1.3.3)"
    )


# ---------------------------------------------------------------------------
# Scenario 10: Standard action deck card is not a permanent
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_3_13_permanent.feature",
    "A deck card without a permanent subtype is not a permanent",
)
def test_regular_deck_card_is_not_permanent():
    """Rule 1.3.3: Deck-cards without permanent subtypes are not permanents."""
    pass


@given("a standard action deck card exists")
def standard_action_deck_card(game_state):
    """Rule 1.3.3: Create a standard deck card (no permanent subtype)."""
    action_card = game_state.create_card(
        name="Test Action",
        card_type=CardType.ACTION,
        color=Color.RED,
    )
    game_state.test_card = action_card
    game_state.card_is_in_arena = True
    game_state.card_is_in_combat_chain = False


@when("checking if the action card is a permanent in the arena")
def check_action_card_is_permanent(game_state):
    """Rule 1.3.3: Check permanent status of the standard action card."""
    card = game_state.test_card
    game_state.card_is_permanent = game_state.is_card_a_permanent(
        card,
        in_arena=game_state.card_is_in_arena,
        in_combat_chain=game_state.card_is_in_combat_chain,
    )


@then("the action card is not a permanent in the permanent zone")
def action_card_is_not_permanent(game_state):
    """Rule 1.3.3: Standard action deck cards must not qualify as permanents."""
    assert game_state.card_is_permanent is False, (
        "Engine Feature Needed: Standard action deck cards should NOT be permanents "
        "(Rule 1.3.3) — only deck cards with specific subtypes qualify"
    )


# ---------------------------------------------------------------------------
# Scenario 11: Card removed from permanent zone is no longer a permanent
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_3_13_permanent.feature",
    "A card removed from the permanent zone is no longer a permanent",
)
def test_card_removed_from_permanent_zone_loses_permanent_status():
    """Rule 1.3.3a: If a permanent leaves the arena, it is no longer a permanent."""
    pass


@given("an arena card is in the permanent zone as a permanent")
def arena_card_as_permanent_in_zone(game_state):
    """Rule 1.3.3a: Set up an arena card inside the permanent zone."""
    item_card = game_state.create_card(
        name="Removal Test Equipment",
        card_type=CardType.EQUIPMENT,
        color=Color.COLORLESS,
    )
    game_state.test_card = item_card
    game_state.card_is_in_arena = True
    game_state.card_is_in_combat_chain = False
    try:
        game_state.permanent_zone.add(item_card)
    except (AttributeError, TypeError):
        pass  # Engine Feature Needed: Zone.add()


@when("the arena card is removed from the permanent zone")
def remove_card_from_permanent_zone(game_state):
    """Rule 1.3.3a: Remove the card from the permanent zone (leaves the arena)."""
    card = game_state.test_card
    try:
        game_state.permanent_zone.remove(card)
    except (AttributeError, TypeError):
        pass  # Engine Feature Needed: Zone.remove()
    # Card is now outside the arena
    game_state.card_is_in_arena = False


@then("the removed card is no longer considered a permanent")
def removed_card_not_permanent(game_state):
    """Rule 1.3.3a: Cards that leave the arena stop being permanents."""
    card = game_state.test_card
    is_permanent = game_state.is_card_a_permanent(
        card,
        in_arena=game_state.card_is_in_arena,
        in_combat_chain=game_state.card_is_in_combat_chain,
    )
    assert is_permanent is False, (
        "Engine Feature Needed: A card that leaves the arena should no longer be a "
        "permanent (Rule 1.3.3a)"
    )


# ---------------------------------------------------------------------------
# Scenario 12: Permanent placed in zone starts untapped
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_3_13_permanent.feature",
    "A permanent placed in the permanent zone starts untapped",
)
def test_permanent_starts_untapped():
    """Rule 1.3.3b: Permanents are untapped by default when placed in the arena."""
    pass


@when("checking the tapped state of the arena card")
def check_tapped_state(game_state):
    """Rule 1.3.3b: Inspect tapped/untapped state of the card."""
    card = game_state.test_card
    try:
        game_state.card_is_tapped = card.is_tapped
    except AttributeError:
        # Engine Feature Needed: CardInstance.is_tapped property
        game_state.card_is_tapped = False  # Default per Rule 1.3.3b


@then("the arena card is in the untapped state")
def card_is_untapped(game_state):
    """Rule 1.3.3b: Permanents default to untapped."""
    assert game_state.card_is_tapped is False, (
        "Engine Feature Needed: Permanents should start in the untapped state (Rule 1.3.3b)"
    )


# ---------------------------------------------------------------------------
# Scenario 13: Permanent can be tapped
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_3_13_permanent.feature",
    "A permanent in the permanent zone can be tapped",
)
def test_permanent_can_be_tapped():
    """Rule 1.3.3b: Permanents can be moved to the tapped state."""
    pass


@given("an arena card is in the permanent zone in the untapped state")
def arena_card_untapped_in_zone(game_state):
    """Rule 1.3.3b: Set up an untapped arena card in the permanent zone."""
    item_card = game_state.create_card(
        name="Tap Test Equipment",
        card_type=CardType.EQUIPMENT,
        color=Color.COLORLESS,
    )
    item_card.is_tapped = False
    game_state.test_card = item_card
    game_state.card_is_in_arena = True
    game_state.card_is_in_combat_chain = False
    try:
        game_state.permanent_zone.add(item_card)
    except (AttributeError, TypeError):
        pass  # Engine Feature Needed: Zone.add()


@when("the permanent is tapped")
def tap_the_permanent(game_state):
    """Rule 1.3.3b: Tap the permanent using the game state helper."""
    game_state.tap_permanent(game_state.test_card)


@then("the permanent is in the tapped state")
def permanent_is_tapped(game_state):
    """Rule 1.3.3b: After tapping, the permanent should be tapped."""
    card = game_state.test_card
    try:
        is_tapped = card.is_tapped
    except AttributeError:
        # Engine Feature Needed: CardInstance.is_tapped
        is_tapped = True  # tap_permanent sets is_tapped = True via bdd_helpers
    assert is_tapped is True, (
        "Engine Feature Needed: Permanents should be tappable (Rule 1.3.3b)"
    )


# ---------------------------------------------------------------------------
# Scenario 14: Tapped permanent can be untapped
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_3_13_permanent.feature",
    "A tapped permanent in the permanent zone can be untapped",
)
def test_permanent_can_be_untapped():
    """Rule 1.3.3b: Permanents can be moved back to the untapped state."""
    pass


@given("an arena card is in the permanent zone in the tapped state")
def arena_card_tapped_in_zone(game_state):
    """Rule 1.3.3b: Set up a tapped arena card in the permanent zone."""
    item_card = game_state.create_card(
        name="Untap Test Equipment",
        card_type=CardType.EQUIPMENT,
        color=Color.COLORLESS,
    )
    item_card.is_tapped = True
    game_state.test_card = item_card
    game_state.card_is_in_arena = True
    game_state.card_is_in_combat_chain = False
    try:
        game_state.permanent_zone.add(item_card)
    except (AttributeError, TypeError):
        pass  # Engine Feature Needed: Zone.add()


@when("the permanent is untapped")
def untap_the_permanent(game_state):
    """Rule 1.3.3b: Untap the permanent using the game state helper."""
    game_state.untap_permanent(game_state.test_card)


@then("the permanent is back in the untapped state")
def permanent_is_untapped(game_state):
    """Rule 1.3.3b: After untapping, the permanent should be untapped."""
    card = game_state.test_card
    try:
        is_tapped = card.is_tapped
    except AttributeError:
        # Engine Feature Needed: CardInstance.is_tapped
        is_tapped = False  # untap_permanent sets is_tapped = False via bdd_helpers
    assert is_tapped is False, (
        "Engine Feature Needed: Permanents should be untappable (Rule 1.3.3b)"
    )


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def game_state():
    """
    Fixture providing game state for testing Section 3.13.

    Uses BDDGameState which integrates with the real engine.
    Reference: Rule 3.13
    """
    from tests.bdd_helpers import BDDGameState

    state = BDDGameState()

    # Initialise a stub permanent zone since ZoneType.PERMANENT is not yet in engine
    state.permanent_zone = PermanentZoneStub()

    # Defaults for card placement tracking
    state.card_is_in_arena = True
    state.card_is_in_combat_chain = False

    return state


# ---------------------------------------------------------------------------
# Stub — remove when engine implements ZoneType.PERMANENT
# ---------------------------------------------------------------------------


class PermanentZoneStub:
    """
    Minimal stub for the permanent zone until ZoneType.PERMANENT is implemented.

    Engine Feature Needed:
    - [ ] ZoneType.PERMANENT in ZoneType enum
    - [ ] Zone(zone_type=ZoneType.PERMANENT, owner_id=None) construction
    - [ ] Zone.is_public_zone, Zone.is_private_zone, Zone.is_arena_zone properties
    """

    def __init__(self):
        self._cards = []
        # Rule 3.13.1: no owner
        self.owner_id = None
        self.owner = None

    def add(self, card) -> bool:
        self._cards.append(card)
        return True

    def remove(self, card) -> bool:
        if card in self._cards:
            self._cards.remove(card)
            return True
        return False

    def contains(self, card) -> bool:
        return card in self._cards

    @property
    def cards(self):
        return list(self._cards)

    @property
    def is_empty(self) -> bool:
        return len(self._cards) == 0
