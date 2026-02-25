"""
Step definitions for Section 1.3: Cards
Reference: Flesh and Blood Comprehensive Rules Section 1.3

This module implements behavioral tests for card categories, controllers,
permanents, and card distinctness.

Engine Features Needed for Section 1.3:
- [ ] CardType.TOKEN enum value (Rule 1.3.2b)
- [ ] CardType.BLOCK enum value (Rule 1.3.2c)
- [ ] CardType.RESOURCE enum value (Rule 1.3.2c)
- [ ] CardType.MENTOR enum value (Rule 1.3.2c)
- [ ] Subtype.ALLY, AFFLICTION, ASH, CONSTRUCT, FIGMENT, INVOCATION, LANDMARK (Rule 1.3.3)
- [ ] CardTemplate.is_hero_card property (Rule 1.3.2a) - checks CardType.HERO
- [ ] CardTemplate.is_token_card property (Rule 1.3.2b) - checks CardType.TOKEN
- [ ] CardTemplate.is_deck_card property (Rule 1.3.2c) - checks deck card types
- [ ] CardTemplate.is_arena_card property (Rule 1.3.2d) - not hero/token/deck
- [ ] CardTemplate.can_start_in_deck property (Rule 1.3.2c/d) - deck-cards only
- [ ] CardTemplate.is_part_of_card_pool property (Rule 1.3.2b) - tokens excluded
- [ ] CardInstance.is_permanent(zone, in_combat_chain) property (Rule 1.3.3)
- [ ] CardTemplate.get_category() -> str method returning "hero", "token", "deck", "arena"
- [ ] Zone-aware controller assignment (Rule 1.3.1b) - None outside arena/stack
- [ ] Card distinctness check: card.is_distinct_from(other) (Rule 1.3.4)

These features will be implemented in a separate task.
Current status: Tests written, Engine pending
"""

import pytest
from pytest_bdd import scenario, given, when, then, parsers


# ============================================================
# Rule 1.3.1b: Controller
# ============================================================


@scenario(
    "../features/section_1_3_cards.feature",
    "Card in hand has no controller",
)
def test_card_in_hand_has_no_controller():
    """Rule 1.3.1b: Card outside arena/stack has no controller."""
    pass


@scenario(
    "../features/section_1_3_cards.feature",
    "Card in deck has no controller",
)
def test_card_in_deck_has_no_controller():
    """Rule 1.3.1b: Card in deck has no controller."""
    pass


@scenario(
    "../features/section_1_3_cards.feature",
    "Card in graveyard has no controller",
)
def test_card_in_graveyard_has_no_controller():
    """Rule 1.3.1b: Card in graveyard has no controller."""
    pass


@scenario(
    "../features/section_1_3_cards.feature",
    "Card entering arena has controller set to its owner",
)
def test_card_entering_arena_gets_controller():
    """Rule 1.3.1b: Card entering arena gets controller set to its owner."""
    pass


@scenario(
    "../features/section_1_3_cards.feature",
    "Card played to stack has controller set to the player who played it",
)
def test_card_played_to_stack_has_controller():
    """Rule 1.3.1b: Card played to stack gets controller assigned."""
    pass


# ============================================================
# Rule 1.3.2: Four card categories
# ============================================================


@scenario(
    "../features/section_1_3_cards.feature",
    "Hero card is classified as a hero-card",
)
def test_hero_card_classified_as_hero_card():
    """Rule 1.3.2a: Hero-typed cards are hero-cards."""
    pass


@scenario(
    "../features/section_1_3_cards.feature",
    "Token card is classified as a token-card and not part of card-pool",
)
def test_token_card_classified_and_excluded_from_card_pool():
    """Rule 1.3.2b: Token-typed cards are token-cards and not in card-pool."""
    pass


@scenario(
    "../features/section_1_3_cards.feature",
    "Action card is classified as a deck-card",
)
def test_action_card_classified_as_deck_card():
    """Rule 1.3.2c: Action cards are deck-cards."""
    pass


@scenario(
    "../features/section_1_3_cards.feature",
    "Attack reaction card is classified as a deck-card",
)
def test_attack_reaction_card_classified_as_deck_card():
    """Rule 1.3.2c: Attack Reaction cards are deck-cards."""
    pass


@scenario(
    "../features/section_1_3_cards.feature",
    "Defense reaction card is classified as a deck-card",
)
def test_defense_reaction_card_classified_as_deck_card():
    """Rule 1.3.2c: Defense Reaction cards are deck-cards."""
    pass


@scenario(
    "../features/section_1_3_cards.feature",
    "Instant card is classified as a deck-card",
)
def test_instant_card_classified_as_deck_card():
    """Rule 1.3.2c: Instant cards are deck-cards."""
    pass


@scenario(
    "../features/section_1_3_cards.feature",
    "Resource card is classified as a deck-card",
)
def test_resource_card_classified_as_deck_card():
    """Rule 1.3.2c: Resource cards are deck-cards."""
    pass


@scenario(
    "../features/section_1_3_cards.feature",
    "Mentor card is classified as a deck-card",
)
def test_mentor_card_classified_as_deck_card():
    """Rule 1.3.2c: Mentor cards are deck-cards."""
    pass


@scenario(
    "../features/section_1_3_cards.feature",
    "Equipment card is classified as an arena-card",
)
def test_equipment_card_classified_as_arena_card():
    """Rule 1.3.2d: Equipment cards are arena-cards."""
    pass


@scenario(
    "../features/section_1_3_cards.feature",
    "Weapon card is classified as an arena-card",
)
def test_weapon_card_classified_as_arena_card():
    """Rule 1.3.2d: Weapon cards are arena-cards."""
    pass


# ============================================================
# Rule 1.3.3: Permanents
# ============================================================


@scenario(
    "../features/section_1_3_cards.feature",
    "Hero card in arena is a permanent",
)
def test_hero_card_in_arena_is_permanent():
    """Rule 1.3.3: Hero-cards in arena are permanents."""
    pass


@scenario(
    "../features/section_1_3_cards.feature",
    "Equipment card in arena is a permanent",
)
def test_equipment_card_in_arena_is_permanent():
    """Rule 1.3.3: Arena-cards (equipment) in arena are permanents."""
    pass


@scenario(
    "../features/section_1_3_cards.feature",
    "Token card in arena is a permanent",
)
def test_token_card_in_arena_is_permanent():
    """Rule 1.3.3: Token-cards in arena are permanents."""
    pass


@scenario(
    "../features/section_1_3_cards.feature",
    "Deck card with Ally subtype in arena is a permanent",
)
def test_deck_card_with_ally_subtype_in_arena_is_permanent():
    """Rule 1.3.3: Deck-cards with permanent subtypes in arena are permanents."""
    pass


@scenario(
    "../features/section_1_3_cards.feature",
    "Deck card without permanent subtype in arena is not a permanent",
)
def test_deck_card_without_permanent_subtype_not_permanent():
    """Rule 1.3.3: Deck-cards without permanent subtypes in arena are NOT permanents."""
    pass


@scenario(
    "../features/section_1_3_cards.feature",
    "Deck card on combat chain is not a permanent",
)
def test_deck_card_on_combat_chain_not_permanent():
    """Rule 1.3.3: Cards on combat chain are not permanents (even with permanent subtypes)."""
    pass


@scenario(
    "../features/section_1_3_cards.feature",
    "Permanent that leaves arena is no longer a permanent",
)
def test_permanent_leaving_arena_loses_permanent_status():
    """Rule 1.3.3a: Permanents cease to be permanents when they leave the arena."""
    pass


@scenario(
    "../features/section_1_3_cards.feature",
    "Permanent enters arena in untapped state",
)
def test_permanent_enters_arena_untapped():
    """Rule 1.3.3b: Permanents enter arena in untapped state by default."""
    pass


@scenario(
    "../features/section_1_3_cards.feature",
    "Permanent can be tapped",
)
def test_permanent_can_be_tapped():
    """Rule 1.3.3b: Permanents can transition to tapped state."""
    pass


@scenario(
    "../features/section_1_3_cards.feature",
    "Tapped permanent can be untapped",
)
def test_tapped_permanent_can_be_untapped():
    """Rule 1.3.3b: Tapped permanents can be returned to untapped state."""
    pass


# ============================================================
# Rule 1.3.4: Card distinctness
# ============================================================


@scenario(
    "../features/section_1_3_cards.feature",
    "Cards with different names are distinct",
)
def test_cards_with_different_names_are_distinct():
    """Rule 1.3.4: Cards with different names are distinct."""
    pass


@scenario(
    "../features/section_1_3_cards.feature",
    "Cards with same name but different pitch values are distinct",
)
def test_cards_with_same_name_different_pitch_are_distinct():
    """Rule 1.3.4: Sink Below red (pitch 1) is distinct from Sink Below blue (pitch 2)."""
    pass


@scenario(
    "../features/section_1_3_cards.feature",
    "Cards with identical name and pitch value are not distinct",
)
def test_cards_with_identical_name_and_pitch_not_distinct():
    """Rule 1.3.4: Cards with same name and pitch are NOT distinct from each other."""
    pass


# ============================================================
# Step Definitions: Rule 1.3.1b - Controller
# ============================================================


@given("a card exists in a player's hand")
def card_in_hand(game_state):
    """Rule 1.3.1b: Card in hand has no controller."""
    from fab_engine.cards.model import CardType

    game_state.test_card = game_state.create_card(
        "Hand Card", card_type=CardType.ACTION
    )
    game_state.player.hand.add_card(game_state.test_card)


@given("a card exists in a player's deck")
def card_in_deck(game_state):
    """Rule 1.3.1b: Card in deck has no controller."""
    from fab_engine.cards.model import CardType

    game_state.test_card = game_state.create_card(
        "Deck Card", card_type=CardType.ACTION
    )
    game_state.deck.add_card(game_state.test_card)


@given("a card exists in a player's graveyard")
def card_in_graveyard(game_state):
    """Rule 1.3.1b: Card in graveyard has no controller."""
    from fab_engine.cards.model import CardType

    game_state.test_card = game_state.create_card(
        "Graveyard Card", card_type=CardType.ACTION
    )
    game_state.graveyard.add_card(game_state.test_card)


@given("player 0 owns a card")
def player_0_owns_a_card(game_state):
    """Rule 1.3.1b: Create card owned by player 0."""
    from fab_engine.cards.model import CardType

    game_state.test_card = game_state.create_card(
        "Arena Card", card_type=CardType.EQUIPMENT, owner_id=0
    )


@when("the card enters the arena")
def card_enters_arena(game_state):
    """Rule 1.3.1b: Card entering arena gets controller set to owner."""
    game_state.play_card_to_arena(game_state.test_card, controller_id=0)


@when("player 0 plays the card to the stack")
def player_plays_card_to_stack(game_state):
    """Rule 1.3.1b: Playing a card sets controller."""
    game_state.play_card_to_stack(game_state.test_card, controller_id=0)


@then("the card should have no controller")
def card_has_no_controller(game_state):
    """Rule 1.3.1b: Cards outside arena/stack have controller_id = None."""
    assert game_state.test_card.controller_id is None, (
        f"Expected controller_id to be None but got {game_state.test_card.controller_id}"
    )


@then("the card should have controller set to player 0")
def card_controller_is_player_0(game_state):
    """Rule 1.3.1b: Controller set to player 0."""
    assert game_state.test_card.controller_id == 0, (
        f"Expected controller_id to be 0 but got {game_state.test_card.controller_id}"
    )


# ============================================================
# Step Definitions: Rule 1.3.2 - Card Categories
# ============================================================


@given("a card has the type hero")
def card_has_type_hero(game_state):
    """Rule 1.3.2a: Create a hero-typed card."""
    from fab_engine.cards.model import CardType

    game_state.test_card = game_state.create_card("Test Hero", card_type=CardType.HERO)


@given("a card has the type token")
def card_has_type_token(game_state):
    """Rule 1.3.2b: Create a token-typed card.

    Engine Feature Needed:
    - [ ] CardType.TOKEN enum value (Rule 1.3.2b)
    """
    game_state.test_card = game_state.create_token_card("Test Token")


@given("a card has the type action")
def card_has_type_action(game_state):
    """Rule 1.3.2c: Create an action-typed card."""
    from fab_engine.cards.model import CardType

    game_state.test_card = game_state.create_card(
        "Test Action", card_type=CardType.ACTION
    )


@given("a card has the type attack reaction")
def card_has_type_attack_reaction(game_state):
    """Rule 1.3.2c: Create an attack reaction card."""
    from fab_engine.cards.model import CardType

    game_state.test_card = game_state.create_card(
        "Test Attack Reaction", card_type=CardType.ATTACK_REACTION
    )


@given("a card has the type defense reaction")
def card_has_type_defense_reaction(game_state):
    """Rule 1.3.2c: Create a defense reaction card."""
    from fab_engine.cards.model import CardType

    game_state.test_card = game_state.create_card(
        "Test Defense Reaction", card_type=CardType.DEFENSE_REACTION
    )


@given("a card has the type instant")
def card_has_type_instant(game_state):
    """Rule 1.3.2c: Create an instant card."""
    from fab_engine.cards.model import CardType

    game_state.test_card = game_state.create_card(
        "Test Instant", card_type=CardType.INSTANT
    )


@given("a card has the type resource")
def card_has_type_resource(game_state):
    """Rule 1.3.2c: Create a resource card.

    Engine Feature Needed:
    - [ ] CardType.RESOURCE enum value (Rule 1.3.2c)
    """
    game_state.test_card = game_state.create_resource_card("Test Resource")


@given("a card has the type mentor")
def card_has_type_mentor(game_state):
    """Rule 1.3.2c: Create a mentor card.

    Engine Feature Needed:
    - [ ] CardType.MENTOR enum value (Rule 1.3.2c)
    """
    game_state.test_card = game_state.create_mentor_card("Test Mentor")


@given("a card has the type equipment")
def card_has_type_equipment(game_state):
    """Rule 1.3.2d: Create an equipment card."""
    from fab_engine.cards.model import CardType

    game_state.test_card = game_state.create_card(
        "Test Equipment", card_type=CardType.EQUIPMENT
    )


@given("a card has the type weapon")
def card_has_type_weapon(game_state):
    """Rule 1.3.2d: Create a weapon card."""
    from fab_engine.cards.model import CardType

    game_state.test_card = game_state.create_card(
        "Test Weapon", card_type=CardType.WEAPON
    )


@then("the card should be classified as a hero-card")
def card_is_hero_card(game_state):
    """Rule 1.3.2a: Card with type HERO is a hero-card.

    Engine Feature Needed:
    - [ ] CardTemplate.is_hero_card property or get_category() == 'hero'
    """
    assert game_state.get_card_category(game_state.test_card) == "hero", (
        "Card with HERO type should be classified as a hero-card"
    )


@then("the card should not be classified as a deck-card")
def card_is_not_deck_card(game_state):
    """Rule 1.3.2: A hero-card is not a deck-card."""
    assert game_state.get_card_category(game_state.test_card) != "deck", (
        "Card should not be classified as a deck-card"
    )


@then("the card should not be classified as a token-card")
def card_is_not_token_card(game_state):
    """Rule 1.3.2: A hero-card is not a token-card."""
    assert game_state.get_card_category(game_state.test_card) != "token", (
        "Card should not be classified as a token-card"
    )


@then("the card should not be classified as an arena-card")
def card_is_not_arena_card(game_state):
    """Rule 1.3.2: A hero-card is not an arena-card."""
    assert game_state.get_card_category(game_state.test_card) != "arena", (
        "Card should not be classified as an arena-card"
    )


@then("the card should be classified as a token-card")
def card_is_token_card(game_state):
    """Rule 1.3.2b: Card with type TOKEN is a token-card.

    Engine Feature Needed:
    - [ ] CardType.TOKEN enum value
    - [ ] CardTemplate.is_token_card or get_category() == 'token'
    """
    assert game_state.get_card_category(game_state.test_card) == "token", (
        "Card with TOKEN type should be classified as a token-card"
    )


@then("the token card should not be considered part of a player's card-pool")
def token_card_not_in_card_pool(game_state):
    """Rule 1.3.2b: Token cards are not part of a player's card-pool.

    Engine Feature Needed:
    - [ ] CardTemplate.is_part_of_card_pool property returning False for tokens
    """
    assert game_state.is_valid_for_card_pool(game_state.test_card) is False, (
        "Token card should not be a valid member of a player's card-pool"
    )


@then("the card should be classified as a deck-card")
def card_is_deck_card(game_state):
    """Rule 1.3.2c: Card is a deck-card.

    Engine Feature Needed:
    - [ ] CardTemplate.is_deck_card or get_category() == 'deck'
    """
    assert game_state.get_card_category(game_state.test_card) == "deck", (
        "Card should be classified as a deck-card"
    )


@then("the card may start the game in a player's deck")
def card_may_start_in_deck(game_state):
    """Rule 1.3.2c: Deck-cards may start the game in a player's deck.

    Engine Feature Needed:
    - [ ] CardTemplate.can_start_in_deck property
    """
    assert game_state.can_start_in_deck(game_state.test_card) is True, (
        "Deck card should be allowed to start the game in a player's deck"
    )


@then("the card should be classified as an arena-card")
def card_is_arena_card(game_state):
    """Rule 1.3.2d: Card is an arena-card.

    Engine Feature Needed:
    - [ ] CardTemplate.is_arena_card or get_category() == 'arena'
    """
    assert game_state.get_card_category(game_state.test_card) == "arena", (
        "Card should be classified as an arena-card"
    )


@then("the arena-card cannot start the game in a player's deck")
def arena_card_cannot_start_in_deck(game_state):
    """Rule 1.3.2d: Arena-cards cannot start the game in a player's deck.

    Engine Feature Needed:
    - [ ] CardTemplate.can_start_in_deck returns False for arena-cards
    """
    assert game_state.can_start_in_deck(game_state.test_card) is False, (
        "Arena card should not be allowed to start the game in a player's deck"
    )


# ============================================================
# Step Definitions: Rule 1.3.3 - Permanents
# ============================================================


@given("a hero card is in the arena")
def hero_card_in_arena(game_state):
    """Rule 1.3.3: Hero card placed in arena."""
    from fab_engine.cards.model import CardType

    game_state.test_card = game_state.create_card("Test Hero", card_type=CardType.HERO)
    game_state.play_card_to_arena(game_state.test_card, controller_id=0)


@given("an equipment card is in the arena")
def equipment_card_in_arena(game_state):
    """Rule 1.3.3: Equipment (arena-card) placed in arena."""
    from fab_engine.cards.model import CardType

    game_state.test_card = game_state.create_card(
        "Test Equipment", card_type=CardType.EQUIPMENT
    )
    game_state.play_card_to_arena(game_state.test_card, controller_id=0)


@given("a token card is in the arena")
def token_card_in_arena(game_state):
    """Rule 1.3.3: Token card placed in arena."""
    game_state.test_card = game_state.create_token_card("Test Token")
    game_state.play_card_to_arena(game_state.test_card, controller_id=0)


@given("a deck card with subtype ally is in the arena")
def deck_card_with_ally_in_arena(game_state):
    """Rule 1.3.3: Deck card with Ally subtype placed in arena (becomes permanent).

    Engine Feature Needed:
    - [ ] Subtype.ALLY enum value (Rule 1.3.3 - permanent deck-card subtypes)
    """
    game_state.test_card = game_state.create_card_with_permanent_subtype(
        "Test Ally", subtype="ally"
    )
    game_state.play_card_to_arena(game_state.test_card, controller_id=0)


@given("an action card without permanent subtypes is in the arena")
def action_card_without_permanent_subtypes_in_arena(game_state):
    """Rule 1.3.3: Action card in arena without permanent subtypes is NOT a permanent."""
    from fab_engine.cards.model import CardType

    game_state.test_card = game_state.create_card(
        "Test Action", card_type=CardType.ACTION
    )
    # Place in arena (conceptually, e.g. via some game effect)
    game_state.play_card_to_arena(game_state.test_card, controller_id=0)
    game_state.is_in_combat_chain = False


@given("an action card is on the combat chain")
def action_card_on_combat_chain(game_state):
    """Rule 1.3.3: Action card placed on combat chain."""
    from fab_engine.cards.model import CardType

    game_state.test_card = game_state.create_card(
        "Test Attack", card_type=CardType.ACTION
    )
    game_state.put_on_combat_chain(game_state.test_card)
    game_state.is_in_combat_chain = True


@given("the card is considered a permanent")
def card_is_permanent_precondition(game_state):
    """Rule 1.3.3: Verify card is currently a permanent before removing."""
    assert game_state.is_card_a_permanent(
        game_state.test_card, in_arena=True, in_combat_chain=False
    ), "Precondition: card should be a permanent while in arena"


@given("an equipment card is placed into the arena")
def equipment_card_placed_into_arena(game_state):
    """Rule 1.3.3b: Equipment placed into arena (should start untapped)."""
    from fab_engine.cards.model import CardType

    game_state.test_card = game_state.create_card(
        "Test Equipment", card_type=CardType.EQUIPMENT
    )
    game_state.play_card_to_arena(game_state.test_card, controller_id=0)


@given("the permanent is in the untapped state")
def permanent_is_untapped(game_state):
    """Rule 1.3.3b: Verify permanent is untapped."""
    game_state.test_card.is_tapped = False


@given("the permanent is in the tapped state")
def permanent_is_tapped(game_state):
    """Rule 1.3.3b: Put permanent in tapped state."""
    game_state.test_card.is_tapped = True


@when("the card is removed from the arena")
def card_removed_from_arena(game_state):
    """Rule 1.3.3a: Card leaves the arena."""
    game_state.player.arena.remove_card(game_state.test_card)
    game_state.card_in_arena = False


@when("the permanent is tapped")
def permanent_is_tapped_action(game_state):
    """Rule 1.3.3b: Tap the permanent.

    Engine Feature Needed:
    - [ ] CardInstance.tap() method or is_tapped setter
    """
    game_state.tap_permanent(game_state.test_card)


@when("the permanent is untapped")
def permanent_is_untapped_action(game_state):
    """Rule 1.3.3b: Untap the permanent.

    Engine Feature Needed:
    - [ ] CardInstance.untap() method or is_tapped setter
    """
    game_state.untap_permanent(game_state.test_card)


@then("the card should be considered a permanent")
def card_is_permanent(game_state):
    """Rule 1.3.3: Card in arena should be considered a permanent.

    Engine Feature Needed:
    - [ ] CardInstance.is_permanent(zone, in_combat_chain) or BDDGameState.is_card_a_permanent()
    """
    in_combat_chain = getattr(game_state, "is_in_combat_chain", False)
    assert game_state.is_card_a_permanent(
        game_state.test_card, in_arena=True, in_combat_chain=in_combat_chain
    ), "Card should be considered a permanent while in the arena"


@then("the card should not be considered a permanent")
def card_is_not_permanent(game_state):
    """Rule 1.3.3/1.3.3a: Card is not a permanent.

    Engine Feature Needed:
    - [ ] CardInstance.is_permanent property
    """
    in_arena = getattr(game_state, "card_in_arena", False)
    in_combat_chain = getattr(game_state, "is_in_combat_chain", False)
    assert not game_state.is_card_a_permanent(
        game_state.test_card, in_arena=in_arena, in_combat_chain=in_combat_chain
    ), "Card should NOT be considered a permanent in this context"


@then("the permanent should be in the untapped state")
def permanent_is_in_untapped_state(game_state):
    """Rule 1.3.3b: Permanent is untapped."""
    assert game_state.test_card.is_tapped is False, (
        "Permanent should be in the untapped state"
    )


@then("the permanent should be in the tapped state")
def permanent_is_in_tapped_state(game_state):
    """Rule 1.3.3b: Permanent is tapped."""
    assert game_state.test_card.is_tapped is True, (
        "Permanent should be in the tapped state"
    )


# ============================================================
# Step Definitions: Rule 1.3.4 - Card Distinctness
# ============================================================


@given(parsers.parse('one card has the name "{name}" and pitch value {pitch:d}'))
def first_card_with_name_and_pitch(name, pitch, game_state):
    """Rule 1.3.4: Set up first card with specific name and pitch."""
    from fab_engine.cards.model import CardType

    game_state.card_a = game_state.create_card_with_name_and_pitch(name, pitch)


@given(parsers.parse('another card has the name "{name}" and pitch value {pitch:d}'))
def second_card_with_name_and_pitch(name, pitch, game_state):
    """Rule 1.3.4: Set up second card with specific name and pitch."""
    game_state.card_b = game_state.create_card_with_name_and_pitch(name, pitch)


@then("the two cards should be considered distinct")
def two_cards_are_distinct(game_state):
    """Rule 1.3.4: Two cards with different name or pitch are distinct.

    Engine Feature Needed:
    - [ ] card.is_distinct_from(other) or BDDGameState.are_cards_distinct(a, b)
    """
    assert game_state.are_cards_distinct(game_state.card_a, game_state.card_b), (
        "Cards with different name and/or pitch should be considered distinct"
    )


@then("the two cards should not be considered distinct")
def two_cards_are_not_distinct(game_state):
    """Rule 1.3.4: Two cards with identical name and pitch are not distinct.

    Engine Feature Needed:
    - [ ] card.is_distinct_from(other) or BDDGameState.are_cards_distinct(a, b)
    """
    assert not game_state.are_cards_distinct(game_state.card_a, game_state.card_b), (
        "Cards with identical name and pitch should NOT be considered distinct"
    )


# ============================================================
# Fixtures
# ============================================================


@pytest.fixture
def game_state():
    """
    Fixture providing game state for Section 1.3 card tests.

    Uses BDDGameState which integrates with the real engine.
    Reference: Rule 1.3
    """
    from tests.bdd_helpers import BDDGameState, TestZone
    from fab_engine.zones.zone import ZoneType

    state = BDDGameState()

    # Additional zones needed for 1.3.1b controller tests
    state.deck = TestZone(ZoneType.DECK, 0)
    state.graveyard = TestZone(ZoneType.GRAVEYARD, 0)

    # Permanent-tracking state
    state.card_in_arena = True
    state.is_in_combat_chain = False

    # Distinctness test cards
    state.card_a = None
    state.card_b = None

    return state
