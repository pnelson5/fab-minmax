"""
Step definitions for Section 1.1: Players
Reference: Flesh and Blood Comprehensive Rules Section 1.1

This module implements behavioral tests for player concepts in Flesh and Blood:
- Rule 1.1.1: A player is a person participating in the game
- Rule 1.1.1a: Participation requirements (hero, card-pool, zones, life total, etc.)
- Rule 1.1.2: A player's hero is a hero-card
- Rule 1.1.2a: Player vs hero distinction
- Rule 1.1.2b: "you" refers to player's hero, "opponent" refers to opponent's hero
- Rule 1.1.3: Card-pool supertype subset validation
- Rule 1.1.3a: Effect-based exception to supertype validation
- Rule 1.1.3b: Hybrid card inclusion via either supertype set
- Rule 1.1.4: Party concept (players who win together)
- Rule 1.1.4a: Player is always in a party with themselves
- Rule 1.1.5: Opponents are players not in the same party
- Rule 1.1.6: Clockwise order

Engine Features Needed for Section 1.1:
- [ ] Player.has_hero() or Player.hero property (Rule 1.1.2)
- [ ] Player.is_eligible_to_participate() (Rule 1.1.1a)
- [ ] Player.card_pool property (Rule 1.1.3)
- [ ] CardPool.validate_card(card, hero) - supertype subset check (Rule 1.1.3)
- [ ] Player.is_in_party_with(other_player) (Rule 1.1.4/1.1.4a)
- [ ] Player.is_opponent_of(other_player) (Rule 1.1.5)
- [ ] GameState.clockwise_order_from(player) (Rule 1.1.6)
- [ ] GameState.next_player_in_clockwise_order(player) (Rule 1.1.6)
- [ ] CardTemplate.supertype_set - collection of Supertype values (Rule 1.1.3)
- [ ] Supertype subset validation logic (Rule 1.1.3, 1.1.3b)
- [ ] HybridCard detection and dual supertype sets (Rule 1.1.3b)

Current status: Tests written, Engine pending
"""

import pytest
from pytest_bdd import scenario, given, when, then, parsers

from fab_engine.cards.model import (
    CardType,
    Supertype,
    CardTemplate,
    CardInstance,
    Color,
)


# ===== Scenario 1: A player must have a hero to participate =====
# Tests Rule 1.1.1 - A player is a person participating in the game


@scenario(
    "../features/section_1_1_players.feature",
    "A player must have a hero to participate in the game",
)
def test_player_must_have_hero_to_participate():
    """Rule 1.1.1/1.1.1a: Players without a hero cannot participate."""
    pass


@given("a player is being set up to participate")
def player_being_set_up(game_state):
    """Rule 1.1.1: Player setup begins."""
    # A fresh player being set up - no hero yet
    game_state.player_under_test = game_state.player
    game_state.player_under_test.hero = None


@when("the player does not have a hero")
def player_has_no_hero(game_state):
    """Rule 1.1.1a: Player has no hero card assigned."""
    # Ensure player has no hero
    game_state.player_under_test.hero = None


@then("the player is not eligible to participate")
def player_not_eligible(game_state):
    """Rule 1.1.1a: Player without a hero cannot participate."""
    # Engine must reject player participation without a hero
    assert not game_state.player_under_test.is_eligible_to_participate()


# ===== Scenario 2: A player requires all components to participate =====
# Tests Rule 1.1.1a - All participation requirements


@scenario(
    "../features/section_1_1_players.feature",
    "A player requires all components to participate",
)
def test_player_requires_all_components():
    """Rule 1.1.1a: Player needs hero, card-pool, zones, and life tracker."""
    pass


@when("the player has a hero and a card-pool and zones and a life total tracker")
def player_has_all_components(game_state):
    """Rule 1.1.1a: Player has all required components."""
    # Set up the player with all required components
    hero_card = game_state.create_card(
        name="Test Hero",
        card_type=CardType.HERO,
        owner_id=0,
    )
    game_state.player_under_test.hero = hero_card
    # card_pool, zones, and life total should also exist
    game_state.has_all_components = True


@then("the player is eligible to participate")
def player_is_eligible(game_state):
    """Rule 1.1.1a: Player with all components can participate."""
    assert game_state.player_under_test.is_eligible_to_participate()


# ===== Scenario 3: A player's hero is a hero-card =====
# Tests Rule 1.1.2 - Player's hero is a hero-card


@scenario(
    "../features/section_1_1_players.feature",
    "A player's hero is a hero-card",
)
def test_player_hero_is_hero_card():
    """Rule 1.1.2: Player's hero must be a hero-card type."""
    pass


@given("a player has a hero card of type HERO")
def player_has_hero_card(game_state):
    """Rule 1.1.2: Create a hero-card for the player."""
    game_state.hero_card = game_state.create_card(
        name="Test Hero",
        card_type=CardType.HERO,
        owner_id=0,
    )
    game_state.player.hero = game_state.hero_card


@then("the player's hero should be a hero-card")
def player_hero_is_hero_card(game_state):
    """Rule 1.1.2: Verify the hero is a hero-card."""
    assert game_state.player.hero is not None
    assert game_state.player.hero.template.is_hero


@then("the hero should have the HERO card type")
def hero_has_hero_card_type(game_state):
    """Rule 1.1.2: The hero has CardType.HERO."""
    assert CardType.HERO in game_state.player.hero.template.types


# ===== Scenario 4: "you" in card text refers to the player's hero =====
# Tests Rule 1.1.2b - "you" and "opponent" refer to heroes


@scenario(
    "../features/section_1_1_players.feature",
    "The term you in card text refers to the player's hero",
)
def test_you_refers_to_player_hero():
    """Rule 1.1.2b: 'you' in card text refers to the player's hero."""
    pass


@given(parsers.parse('a player has a hero named "{hero_name}"'))
def player_has_named_hero(hero_name, game_state):
    """Rule 1.1.2b: Player has a hero with the given name."""
    game_state.hero_card = game_state.create_card(
        name=hero_name,
        card_type=CardType.HERO,
        owner_id=0,
    )
    game_state.player.hero = game_state.hero_card
    game_state.player_hero_name = hero_name


@given("an opponent has a different hero")
def opponent_has_different_hero(game_state):
    """Rule 1.1.2b: Opponent has their own hero."""
    game_state.opponent_hero_card = game_state.create_card(
        name="Opponent Hero",
        card_type=CardType.HERO,
        owner_id=1,
    )
    game_state.defender.hero = game_state.opponent_hero_card


@when('card text says "you"')
def card_text_references_you(game_state):
    """Rule 1.1.2b: Card text contains 'you' reference."""
    # In the context of card resolution, 'you' refers to the controller's hero
    game_state.you_reference = game_state.player.hero


@then('"you" refers to the player\'s hero')
def you_refers_to_player_hero(game_state):
    """Rule 1.1.2b: 'you' is the player's hero, not the player themselves."""
    # The engine must resolve 'you' to the player's hero
    hero = game_state.player.resolve_you_reference()
    assert hero is not None
    assert hero.template.is_hero
    assert hero.name == game_state.player_hero_name


@then('"opponent" refers to the opponent\'s hero')
def opponent_refers_to_opponent_hero(game_state):
    """Rule 1.1.2b: 'opponent' resolves to the opponent's hero."""
    opponent_hero = game_state.player.resolve_opponent_reference(game_state.defender)
    assert opponent_hero is not None
    assert opponent_hero.template.is_hero
    assert opponent_hero.owner_id == 1


# ===== Scenario 5: A card with matching supertypes can be in the card-pool =====
# Tests Rule 1.1.3 - Card-pool supertype subset validation


@scenario(
    "../features/section_1_1_players.feature",
    "A card with matching supertypes can be included in a card-pool",
)
def test_card_with_matching_supertypes_in_card_pool():
    """Rule 1.1.3: Cards must have supertypes that are a subset of hero's supertypes."""
    pass


@given(parsers.parse('a hero with supertypes "{st1}" and "{st2}"'))
def hero_with_two_supertypes(st1, st2, game_state):
    """Rule 1.1.3: Create a hero with specified supertypes."""
    game_state.hero_supertypes = {st1, st2}
    game_state.hero_template = _create_hero_template_with_supertypes(
        game_state, [st1, st2]
    )
    game_state.hero_card_instance = CardInstance(
        template=game_state.hero_template, owner_id=0
    )


@given(parsers.parse('a card with supertypes "{st1}" and "{st2}"'))
def card_with_two_supertypes(st1, st2, game_state):
    """Rule 1.1.3: Create a card with specified supertypes."""
    game_state.test_card_template = _create_card_template_with_supertypes(
        game_state, [st1, st2]
    )
    game_state.test_card = CardInstance(
        template=game_state.test_card_template, owner_id=0
    )


@then("the card should be eligible for the hero's card-pool")
def card_eligible_for_card_pool(game_state):
    """Rule 1.1.3: Card's supertypes are a subset of hero's supertypes."""
    is_eligible = game_state.validate_card_in_card_pool(
        game_state.test_card, game_state.hero_card_instance
    )
    assert is_eligible


@then("the card supertypes are a subset of the hero's supertypes")
def card_supertypes_are_subset(game_state):
    """Rule 1.1.3: Documenting the reason the card is eligible."""
    # This step documents the reasoning - eligibility already verified
    pass


# ===== Scenario 6: A generic card can be in any hero's card-pool =====
# Tests Rule 1.1.3 - Generic cards (no supertypes) are always valid


@scenario(
    "../features/section_1_1_players.feature",
    "A generic card with no supertypes can be included in any hero's card-pool",
)
def test_generic_card_in_any_card_pool():
    """Rule 1.1.3: Empty supertype set is a subset of any set - generic cards always valid."""
    pass


@given(parsers.parse('a hero with supertypes "{st1}"'))
def hero_with_one_supertype(st1, game_state):
    """Rule 1.1.3: Create a hero with a single supertype."""
    game_state.hero_supertypes = {st1}
    game_state.hero_template = _create_hero_template_with_supertypes(game_state, [st1])
    game_state.hero_card_instance = CardInstance(
        template=game_state.hero_template, owner_id=0
    )


@given("a generic card with no supertypes")
def generic_card_no_supertypes(game_state):
    """Rule 1.1.3: A generic card has empty supertype set."""
    game_state.test_card_template = _create_card_template_with_supertypes(
        game_state,
        [],  # No supertypes - generic
    )
    game_state.test_card = CardInstance(
        template=game_state.test_card_template, owner_id=0
    )


@then("the generic card should be eligible for the hero's card-pool")
def generic_card_eligible(game_state):
    """Rule 1.1.3: Generic card (empty supertypes) is valid for any hero."""
    is_eligible = game_state.validate_card_in_card_pool(
        game_state.test_card, game_state.hero_card_instance
    )
    assert is_eligible


@then("an empty set is a subset of any set")
def empty_set_is_subset(game_state):
    """Rule 1.1.3: Mathematical: empty set ⊆ any set."""
    pass


# ===== Scenario 7: A card with non-matching supertypes cannot be in the card-pool =====
# Tests Rule 1.1.3 - Non-matching supertypes are rejected


@scenario(
    "../features/section_1_1_players.feature",
    "A card with non-matching supertypes cannot be included in a card-pool",
)
def test_non_matching_supertypes_rejected():
    """Rule 1.1.3: Cards with non-subset supertypes are excluded from card-pool."""
    pass


@given(parsers.parse('a card with supertypes "{st1}"'))
def card_with_one_supertype(st1, game_state):
    """Rule 1.1.3: Create a card with one supertype."""
    game_state.test_card_template = _create_card_template_with_supertypes(
        game_state, [st1]
    )
    game_state.test_card = CardInstance(
        template=game_state.test_card_template, owner_id=0
    )


@then("the card should not be eligible for the hero's card-pool")
def card_not_eligible(game_state):
    """Rule 1.1.3: Card's supertypes are NOT a subset of hero's supertypes."""
    is_eligible = game_state.validate_card_in_card_pool(
        game_state.test_card, game_state.hero_card_instance
    )
    assert not is_eligible


@then(parsers.parse('"{st}" is not a subset of the hero\'s supertypes'))
def not_a_subset(st, game_state):
    """Rule 1.1.3: Documenting why card is ineligible."""
    pass


# ===== Scenario 8: A card with one matching supertype is eligible =====
# Tests Rule 1.1.3 - Subset means ANY supertype combination that is contained


@scenario(
    "../features/section_1_1_players.feature",
    "A card with one of the hero's supertypes can be in the card-pool",
)
def test_partial_supertype_match_is_eligible():
    """Rule 1.1.3: A card with fewer supertypes (all matching) is a valid subset."""
    pass


@given('a card with only the supertype "Warrior"')
def card_with_only_warrior_supertype(game_state):
    """Rule 1.1.3: Card has a single supertype that the hero also has."""
    game_state.test_card_template = _create_card_template_with_supertypes(
        game_state, ["Warrior"]
    )
    game_state.test_card = CardInstance(
        template=game_state.test_card_template, owner_id=0
    )


@then("a single matching supertype is still a subset")
def single_is_subset(game_state):
    """Rule 1.1.3: A subset requires all card supertypes to be in hero's supertypes."""
    pass


# ===== Scenario 9: Effect allows non-matching supertypes in card-pool =====
# Tests Rule 1.1.3a - Effects can override the supertype subset requirement


@scenario(
    "../features/section_1_1_players.feature",
    "An effect can allow a card with non-matching supertypes in the card-pool",
)
def test_effect_allows_non_matching_supertypes():
    """Rule 1.1.3a: Effects can grant exceptions to supertype validation."""
    pass


@given("an effect that allows starting with that card in the card-pool")
def effect_allows_card_in_pool(game_state):
    """Rule 1.1.3a: An effect grants an exception for this card."""
    game_state.effect_exception_cards = [game_state.test_card]
    game_state.has_effect_exception = True


@then("the card can be included in the card-pool under the effect")
def card_can_be_included_with_effect(game_state):
    """Rule 1.1.3a: With the effect, the card is eligible despite supertype mismatch."""
    is_eligible = game_state.validate_card_in_card_pool(
        game_state.test_card,
        game_state.hero_card_instance,
        effect_exceptions=game_state.effect_exception_cards,
    )
    assert is_eligible


# ===== Scenario 10: Hybrid card matches either supertype set =====
# Tests Rule 1.1.3b - Hybrid cards with dual supertype sets


@scenario(
    "../features/section_1_1_players.feature",
    "A hybrid card can be included if either supertype set matches",
)
def test_hybrid_card_either_supertype_set():
    """Rule 1.1.3b: Hybrid card eligible if EITHER of its supertype sets matches."""
    pass


@given(parsers.parse('a hybrid card with supertype sets "{st1}" and "{st2}"'))
def hybrid_card_with_two_supertype_sets(st1, st2, game_state):
    """Rule 1.1.3b: Hybrid card has two alternative supertype sets."""
    # A hybrid card has two sets: one is {st1} and the other is {st2}
    game_state.hybrid_supertype_sets = [{st1}, {st2}]
    game_state.test_card_template = _create_hybrid_card_template(
        game_state, [{st1}, {st2}]
    )
    game_state.test_card = CardInstance(
        template=game_state.test_card_template, owner_id=0
    )


@then("the hybrid card should be eligible for the hero's card-pool")
def hybrid_card_eligible(game_state):
    """Rule 1.1.3b: Hybrid card is eligible because one supertype set matches."""
    is_eligible = game_state.validate_card_in_card_pool(
        game_state.test_card,
        game_state.hero_card_instance,
        is_hybrid=True,
        hybrid_supertype_sets=game_state.hybrid_supertype_sets,
    )
    assert is_eligible


@then('the "Warrior" supertype set is a subset of the hero\'s supertypes')
def warrior_set_matches(game_state):
    """Rule 1.1.3b: The 'Warrior' alternative set is a subset of hero's supertypes."""
    pass


# ===== Scenario 11: A player is in a party with themselves =====
# Tests Rule 1.1.4/1.1.4a - Party membership includes self


@scenario(
    "../features/section_1_1_players.feature",
    "A player is in a party with themselves",
)
def test_player_in_party_with_themselves():
    """Rule 1.1.4a: A player is always considered to be in a party with themselves."""
    pass


@given(parsers.parse('a player named "{player_name}" is playing'))
def named_player_is_playing(player_name, game_state):
    """Rule 1.1.4: Set up a named player."""
    game_state.named_player_id = 0
    game_state.player_name = player_name


@then(parsers.parse('"{player_name}" should be in a party with herself'))
def player_in_party_with_self(player_name, game_state):
    """Rule 1.1.4a: Player is always in a party with themselves."""
    # The engine must support self-party membership check
    is_in_party = game_state.player.is_in_party_with(game_state.player)
    assert is_in_party


@then("a player is always in a party with themselves")
def always_in_party_with_self(game_state):
    """Rule 1.1.4a: This is an absolute rule, not contingent on game state."""
    pass


# ===== Scenario 12: Two players are not in the same party =====
# Tests Rule 1.1.4a - In a standard game, each player is their own party


@scenario(
    "../features/section_1_1_players.feature",
    "In a two-player game players are not in the same party",
)
def test_two_players_not_in_same_party():
    """Rule 1.1.4a: Each player is in their own party in a 1v1 game."""
    pass


@given("player 0 is playing")
def player_0_is_playing(game_state):
    """Rule 1.1.4: Player 0 is participating."""
    game_state.player_0 = game_state.player


@given("player 1 is playing")
def player_1_is_playing(game_state):
    """Rule 1.1.4: Player 1 is participating."""
    game_state.player_1 = game_state.defender


@then("player 0 should not be in a party with player 1")
def player_0_not_in_party_with_1(game_state):
    """Rule 1.1.4: In a standard 1v1 game, players are opponents, not party members."""
    is_in_party = game_state.player_0.is_in_party_with(game_state.player_1)
    assert not is_in_party


@then("each player's party should contain only themselves")
def each_player_party_is_solo(game_state):
    """Rule 1.1.4a: Each player's party is {themselves}."""
    player_0_party = game_state.player_0.get_party()
    player_1_party = game_state.player_1.get_party()

    # Each party should contain only that player
    assert game_state.player_0 in player_0_party
    assert game_state.player_1 not in player_0_party
    assert game_state.player_1 in player_1_party
    assert game_state.player_0 not in player_1_party


# ===== Scenario 13: Opponents are players not in the same party =====
# Tests Rule 1.1.5 - Opponent definition


@scenario(
    "../features/section_1_1_players.feature",
    "Opponents are players not in the same party",
)
def test_opponents_are_not_in_same_party():
    """Rule 1.1.5: Players not in the same party are opponents."""
    pass


@then("player 1 should be an opponent of player 0")
def player_1_is_opponent_of_player_0(game_state):
    """Rule 1.1.5: Player 1 is an opponent of player 0."""
    is_opponent = game_state.player_0.is_opponent_of(game_state.player_1)
    assert is_opponent


@then("player 0 should be an opponent of player 1")
def player_0_is_opponent_of_player_1(game_state):
    """Rule 1.1.5: Opponent relationship is symmetric."""
    is_opponent = game_state.player_1.is_opponent_of(game_state.player_0)
    assert is_opponent


# ===== Scenario 14: Clockwise order =====
# Tests Rule 1.1.6 - Clockwise player ordering


@scenario(
    "../features/section_1_1_players.feature",
    "Clockwise order starts from a given player and goes left",
)
def test_clockwise_order():
    """Rule 1.1.6: Clockwise order starts from a player and progresses to their left."""
    pass


@given("there are three players in the game in clockwise positions")
def three_players_clockwise(game_state):
    """Rule 1.1.6: Set up a 3-player game for clockwise order testing."""
    game_state.clockwise_players = [
        {"id": 0, "position": "top"},
        {"id": 1, "position": "right"},
        {"id": 2, "position": "bottom"},
    ]
    game_state.num_players = 3


@when("determining clockwise order starting from player 0")
def determine_clockwise_from_player_0(game_state):
    """Rule 1.1.6: Calculate clockwise order starting from player 0."""
    game_state.clockwise_from_0 = game_state.get_clockwise_order(
        starting_player_id=0, num_players=game_state.num_players
    )


@then("the next player after player 0 should be player 1")
def next_after_0_is_1(game_state):
    """Rule 1.1.6: Player 1 is next clockwise from player 0."""
    next_player = game_state.get_next_clockwise_player(
        current_player_id=0, num_players=game_state.num_players
    )
    assert next_player == 1


@then("the next player after player 1 should be player 2")
def next_after_1_is_2(game_state):
    """Rule 1.1.6: Player 2 is next clockwise from player 1."""
    next_player = game_state.get_next_clockwise_player(
        current_player_id=1, num_players=game_state.num_players
    )
    assert next_player == 2


@then("the next player after player 2 should be player 0")
def next_after_2_is_0(game_state):
    """Rule 1.1.6: Player 0 is next clockwise from player 2 (wraps around)."""
    next_player = game_state.get_next_clockwise_player(
        current_player_id=2, num_players=game_state.num_players
    )
    assert next_player == 0


# ===== Helper Functions =====


def _create_hero_template_with_supertypes(
    game_state, supertype_names: list
) -> CardTemplate:
    """Create a hero CardTemplate with given supertype names."""
    supertypes = frozenset(_names_to_supertypes(supertype_names))
    return CardTemplate(
        unique_id=f"hero_{supertype_names}_{id(game_state)}",
        name="Test Hero",
        types=frozenset([CardType.HERO]),
        supertypes=supertypes,
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
        life=20,
        intellect=4,
        keywords=frozenset(),
        keyword_params=tuple(),
        functional_text="",
    )


def _create_card_template_with_supertypes(
    game_state, supertype_names: list
) -> CardTemplate:
    """Create a non-hero CardTemplate with given supertype names."""
    supertypes = frozenset(_names_to_supertypes(supertype_names))
    return CardTemplate(
        unique_id=f"card_{supertype_names}_{id(game_state)}",
        name="Test Card",
        types=frozenset([CardType.ACTION]),
        supertypes=supertypes,
        subtypes=frozenset(),
        color=Color.COLORLESS,
        pitch=0,
        has_pitch=False,
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


def _create_hybrid_card_template(game_state, supertype_sets: list) -> CardTemplate:
    """
    Create a hybrid CardTemplate with dual supertype sets.

    Hybrid cards have two alternative supertype sets; the card is eligible
    if EITHER set is a subset of the hero's supertypes (Rule 1.1.3b).
    """
    # Hybrid cards use the first supertype set as their template supertypes
    # The actual hybrid validation needs engine support for dual supertype sets
    first_set = list(supertype_sets[0]) if supertype_sets else []
    supertypes = frozenset(_names_to_supertypes(first_set))
    return CardTemplate(
        unique_id=f"hybrid_{supertype_sets}_{id(game_state)}",
        name="Hybrid Test Card",
        types=frozenset([CardType.ACTION]),
        supertypes=supertypes,
        subtypes=frozenset(),
        color=Color.COLORLESS,
        pitch=0,
        has_pitch=False,
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


def _names_to_supertypes(names: list) -> list:
    """Convert supertype name strings to Supertype enum values."""
    mapping = {
        "Warrior": Supertype.WARRIOR,
        "Light": None,  # Light is not yet a Supertype enum value
        "Wizard": Supertype.WIZARD,
        "Guardian": Supertype.GUARDIAN,
        "Ninja": Supertype.NINJA,
        "Brute": Supertype.BRUTE,
        "Ranger": Supertype.RANGER,
        "Mechanologist": Supertype.MECHANOLOGIST,
        "Shadow": Supertype.SHADOW,
        "Illusionist": Supertype.ILLUSIONIST,
        "Generic": Supertype.GENERIC,
    }
    result = []
    for name in names:
        st = mapping.get(name)
        if st is not None:
            result.append(st)
    return result


# ===== Fixtures =====


@pytest.fixture
def game_state():
    """
    Fixture providing game state for player rule testing.

    Uses BDDGameState which integrates with the real engine.
    Extended with additional attributes needed for Section 1.1 tests.
    Reference: Rule 1.1
    """
    from tests.bdd_helpers import BDDGameState

    state = BDDGameState()

    # Additional state for Section 1.1 tests
    state.player_under_test = None
    state.has_all_components = False
    state.hero_card = None
    state.opponent_hero_card = None
    state.hero_card_instance = None
    state.hero_template = None
    state.test_card_template = None
    state.hero_supertypes = set()
    state.hybrid_supertype_sets = []
    state.has_effect_exception = False
    state.effect_exception_cards = []
    state.named_player_id = None
    state.player_name = None
    state.player_0 = None
    state.player_1 = None
    state.clockwise_players = []
    state.num_players = 2
    state.clockwise_from_0 = []

    # Inject methods needed for Section 1.1 tests onto the player objects
    # These methods represent engine features that need to be implemented
    # For now they will raise AttributeError to document missing features

    return state
