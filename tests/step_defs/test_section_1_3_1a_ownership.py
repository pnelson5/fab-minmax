"""
Step definitions for Section 1.3.1a: Card Ownership
Reference: Flesh and Blood Comprehensive Rules Section 1.3.1a

Rule 1.3.1a: The owner of a card is the player who started the game with that card
as their hero or as part of their card-pool, or the player instructed to create it
or otherwise put it into the game.
"""

import pytest
from pytest_bdd import scenario, given, when, then, parsers


# Scenario: Cards in starting deck are owned by the player who started with them
# Tests Rule 1.3.1a: Ownership established at game start


@scenario(
    "../features/section_1_3_1a_card_ownership.feature",
    "Cards in starting deck are owned by the player who started with them",
)
def test_starting_deck_ownership():
    """Rule 1.3.1a: Cards in starting deck are owned by that player."""
    pass


@given("player 0 has a card in their starting deck")
def player_0_has_card_in_deck(game_state):
    """Rule 1.3.1a: Create card owned by player 0."""
    game_state.test_card = game_state.create_card("Test Card", owner_id=0)
    game_state.player_0_deck.add_card(game_state.test_card)


@when("the game begins")
def game_begins(game_state):
    """Rule 1.3.1a: Game setup complete."""
    # Game has begun, ownership is established
    pass


@then("the card should be owned by player 0")
def card_owned_by_player_0(game_state):
    """Rule 1.3.1a: Verify card ownership."""
    assert game_state.test_card.owner_id == 0


@then("the card owner should not change when moved to hand")
def ownership_persists_to_hand(game_state):
    """Rule 1.3.1a: Ownership persists across zones."""
    # Move card to hand
    game_state.player_0_deck.remove_card(game_state.test_card)
    game_state.player_0_hand.add_card(game_state.test_card)

    # Ownership should not change
    assert game_state.test_card.owner_id == 0


@then("the card owner should not change when played")
def ownership_persists_when_played(game_state):
    """Rule 1.3.1a: Ownership persists when card is played."""
    # Move card to stack (simulating play)
    game_state.player_0_hand.remove_card(game_state.test_card)
    game_state.stack.append(game_state.test_card)

    # Ownership should not change
    assert game_state.test_card.owner_id == 0


# Scenario: Hero card is owned by the player who started with it
# Tests Rule 1.3.1a: Hero ownership


@scenario(
    "../features/section_1_3_1a_card_ownership.feature",
    "Hero card is owned by the player who started with it",
)
def test_hero_card_ownership():
    """Rule 1.3.1a: Hero card is owned by the player."""
    pass


@given("player 1 has a hero card")
def player_1_has_hero(game_state):
    """Rule 1.3.1a: Create hero for player 1."""
    from fab_engine.cards.model import CardType

    game_state.hero_card = game_state.create_card(
        "Test Hero", owner_id=1, card_type=CardType.HERO
    )


@then("the hero card should be owned by player 1")
def hero_owned_by_player_1(game_state):
    """Rule 1.3.1a: Verify hero ownership."""
    assert game_state.hero_card.owner_id == 1


@then("the hero card owner should never change")
def hero_ownership_never_changes(game_state):
    """Rule 1.3.1a: Hero ownership is immutable."""
    # Hero ownership established at game start and never changes
    assert game_state.hero_card.owner_id == 1


# Scenario: Token created by a player is owned by that player
# Tests Rule 1.3.1a: Token ownership


@scenario(
    "../features/section_1_3_1a_card_ownership.feature",
    "Token created by a player is owned by that player",
)
def test_token_ownership():
    """Rule 1.3.1a: Tokens are owned by the player who created them."""
    pass


@given("player 0 is instructed to create a token")
def player_instructed_create_token(game_state):
    """Rule 1.3.1a: Player will create a token."""
    # Setup - player will create token
    pass


@when("the token is created")
def token_is_created(game_state):
    """Rule 1.3.1a: Create token owned by player 0."""
    from fab_engine.cards.model import CardType

    game_state.token = game_state.create_card(
        "Test Token",
        owner_id=0,
        card_type=CardType.INSTANT,  # Using INSTANT as proxy for token
    )


@then("the token should be owned by player 0")
def token_owned_by_creator(game_state):
    """Rule 1.3.1a: Token owned by creating player."""
    assert game_state.token.owner_id == 0


@then("the token owner should be player 0 even if it moves zones")
def token_ownership_persists(game_state):
    """Rule 1.3.1a: Token ownership persists across zones."""
    # Move token through zones
    game_state.player_0_hand.add_card(game_state.token)
    assert game_state.token.owner_id == 0

    game_state.player_0_hand.remove_card(game_state.token)
    game_state.player_0_graveyard.add_card(game_state.token)
    assert game_state.token.owner_id == 0


# Scenario: Card ownership persists when card moves between zones
# Tests Rule 1.3.1a: Ownership persistence


@scenario(
    "../features/section_1_3_1a_card_ownership.feature",
    "Card ownership persists when card moves between zones",
)
def test_ownership_persists_across_zones():
    """Rule 1.3.1a: Ownership persists when moving between zones."""
    pass


@given("player 0 owns a card in their hand")
def player_owns_card_in_hand(game_state):
    """Rule 1.3.1a: Setup card in hand owned by player 0."""
    game_state.test_card = game_state.create_card("Zone Test Card", owner_id=0)
    game_state.player_0_hand.add_card(game_state.test_card)


@when("the card is moved to the graveyard")
def move_to_graveyard(game_state):
    """Rule 1.3.1a: Move card to graveyard."""
    game_state.player_0_hand.remove_card(game_state.test_card)
    game_state.player_0_graveyard.add_card(game_state.test_card)


@then("the card should still be owned by player 0")
def card_still_owned_by_player_0(game_state):
    """Rule 1.3.1a: Ownership unchanged."""
    assert game_state.test_card.owner_id == 0


@when("the card is moved to the banished zone")
def move_to_banished(game_state):
    """Rule 1.3.1a: Move card to banished zone."""
    game_state.player_0_graveyard.remove_card(game_state.test_card)
    game_state.player_0_banished.add_card(game_state.test_card)


@when("the card is moved to the deck")
def move_to_deck(game_state):
    """Rule 1.3.1a: Move card to deck."""
    game_state.player_0_banished.remove_card(game_state.test_card)
    game_state.player_0_deck.add_card(game_state.test_card)


# Scenario: Card ownership is independent of who controls it
# Tests Rule 1.3.1a + 1.3.1b: Ownership vs Control


@scenario(
    "../features/section_1_3_1a_card_ownership.feature",
    "Card ownership is independent of who controls it",
)
def test_ownership_vs_control():
    """Rule 1.3.1a/b: Ownership and control are independent."""
    pass


@given("player 0 owns a card")
def player_0_owns_card(game_state):
    """Rule 1.3.1a: Create card owned by player 0."""
    game_state.test_card = game_state.create_card("Control Test Card", owner_id=0)


@given("player 1 controls the card")
def player_1_controls_card(game_state):
    """Rule 1.3.1b: Set controller to player 1."""
    game_state.test_card.controller_id = 1


@then("the card should be controlled by player 1")
def card_controlled_by_player_1(game_state):
    """Rule 1.3.1b: Verify controller."""
    assert game_state.test_card.controller_id == 1


@then("ownership and control should be independent properties")
def ownership_and_control_independent(game_state):
    """Rule 1.3.1a/b: Ownership and control are separate."""
    assert game_state.test_card.owner_id == 0  # Owner
    assert game_state.test_card.controller_id == 1  # Controller
    assert game_state.test_card.owner_id != game_state.test_card.controller_id


# Scenario: Cards included in a player's card-pool are owned by that player
# Tests Rule 1.3.1a: Card-pool ownership


@scenario(
    "../features/section_1_3_1a_card_ownership.feature",
    "Cards included in a player's card-pool are owned by that player",
)
def test_card_pool_ownership():
    """Rule 1.3.1a: Card-pool cards are owned by that player."""
    pass


@given("player 1 includes a card in their card-pool")
def player_includes_in_card_pool(game_state):
    """Rule 1.3.1a: Card is part of player 1's card-pool."""
    game_state.test_card = game_state.create_card("Card Pool Card", owner_id=1)


@when("the card is added to their deck during setup")
def card_added_to_deck(game_state):
    """Rule 1.3.1a: Add card to deck during game setup."""
    game_state.player_1_deck.add_card(game_state.test_card)


@then("the card should be owned by player 1")
def card_owned_by_player_1(game_state):
    """Rule 1.3.1a: Verify ownership."""
    assert game_state.test_card.owner_id == 1


@then("the ownership should be established at game start")
def ownership_established_at_start(game_state):
    """Rule 1.3.1a: Ownership set when game begins."""
    # Ownership is set when card is created/added to card-pool
    assert game_state.test_card.owner_id == 1


# Scenario: Cards stolen or copied remain owned by original owner
# Tests Rule 1.3.1a: Ownership doesn't transfer


@scenario(
    "../features/section_1_3_1a_card_ownership.feature",
    "Cards stolen or copied remain owned by original owner",
)
def test_ownership_doesnt_transfer():
    """Rule 1.3.1a: Ownership doesn't change when control changes."""
    pass


@when("player 1 takes control of the card")
def player_1_takes_control(game_state):
    """Rule 1.3.1b: Change controller to player 1."""
    game_state.test_card.controller_id = 1


@then("the card should still be owned by player 0")
def still_owned_by_player_0(game_state):
    """Rule 1.3.1a: Owner doesn't change."""
    assert game_state.test_card.owner_id == 0


@then("player 1 should not become the owner")
def player_1_not_owner(game_state):
    """Rule 1.3.1a: Control doesn't grant ownership."""
    assert game_state.test_card.owner_id != 1
    assert game_state.test_card.owner_id == 0


# Fixtures


@pytest.fixture
def game_state():
    """
    Fixture providing game state for ownership testing.

    Uses REAL CardInstance objects with owner_id tracking.
    Reference: Rule 1.3.1a
    """
    from tests.bdd_helpers import BDDGameState
    from fab_engine.zones.zone import ZoneType
    from tests.bdd_helpers import TestZone

    state = BDDGameState()

    # Add player-specific zones for ownership tests
    state.player_0_deck = TestZone(ZoneType.DECK, 0)
    state.player_0_hand = TestZone(ZoneType.HAND, 0)
    state.player_0_graveyard = TestZone(ZoneType.GRAVEYARD, 0)
    state.player_0_banished = TestZone(ZoneType.BANISHED, 0)

    state.player_1_deck = TestZone(ZoneType.DECK, 1)
    state.player_1_hand = TestZone(ZoneType.HAND, 1)

    # Additional state for tests
    state.hero_card = None
    state.token = None

    return state
