# Feature file for Section 1.3: Cards
# Reference: Flesh and Blood Comprehensive Rules Section 1.3
#
# 1.3.1: A card is an object represented by an official Flesh and Blood card.
# 1.3.1a: The owner of a card is the player who started the game with that card
#   as their hero or as part of their card-pool, or the player instructed to create
#   it or otherwise put it into the game.
#   [COVERED BY section_1_3_1a_card_ownership.feature — skip 1.3.1a here]
# 1.3.1b: A card does not have a controller unless it is in the arena or on the stack.
#   The controller of a card is its owner as it enters the arena or the player who
#   played that card.
#
# 1.3.2: There are 4 categories of cards: hero-, token-, deck-, and arena-cards.
# 1.3.2a: A hero-card is any card with the type hero. A hero-card starts the game as
#   a player's hero.
# 1.3.2b: A token-card is any card with the type token. A token-card is not considered
#   part of a player's card-pool.
# 1.3.2c: A deck-card is any card with one of the following types: Action, Attack
#   Reaction, Block, Defense Reaction, Instant, Mentor, and Resource. A deck-card may
#   start the game in a player's deck.
# 1.3.2d: An arena-card is any non-hero- non-token- non-deck-card. An arena-card
#   cannot start the game in a player's deck.
#
# 1.3.3: A permanent is a card in the arena that remains there indefinitely, or until
#   they are destroyed, banished, or otherwise removed by an effect or game rule.
#   Hero-cards, arena-cards, and token-cards are permanents while they are in the
#   arena. Deck-cards become permanents when they are put into the arena (but not the
#   combat chain) and they have one of the following subtypes: Affliction, Ally, Ash,
#   Aura, Construct, Figment, Invocation, Item, and Landmark.
# 1.3.3a: If a permanent leaves the arena, it is no longer considered a permanent.
# 1.3.3b: A permanent has one of two different states: untapped and tapped. Permanents
#   are untapped unless a rule or effect puts them into the arena tapped, or changes
#   their state.
#
# 1.3.4: A card is distinct from another card if one or more of its faces has a name
#   and/or pitch value the other card does not have.

Feature: Section 1.3 - Cards
    As a game engine
    I need to correctly classify and manage card categories, controllers, permanents, and distinctness
    So that card rules are correctly implemented in gameplay

    # ---- Rule 1.3.1b: Controller ----

    # Test for Rule 1.3.1b - Cards in hand/deck/graveyard/banished have no controller
    Scenario: Card in hand has no controller
        Given a card exists in a player's hand
        Then the card should have no controller

    # Test for Rule 1.3.1b - Cards in deck have no controller
    Scenario: Card in deck has no controller
        Given a card exists in a player's deck
        Then the card should have no controller

    # Test for Rule 1.3.1b - Cards in graveyard have no controller
    Scenario: Card in graveyard has no controller
        Given a card exists in a player's graveyard
        Then the card should have no controller

    # Test for Rule 1.3.1b - Card entering arena gets controller set to its owner
    Scenario: Card entering arena has controller set to its owner
        Given player 0 owns a card
        When the card enters the arena
        Then the card should have controller set to player 0

    # Test for Rule 1.3.1b - Card played by a player gets controller set to that player
    Scenario: Card played to stack has controller set to the player who played it
        Given player 0 owns a card
        When player 0 plays the card to the stack
        Then the card should have controller set to player 0

    # ---- Rule 1.3.2: Four card categories ----

    # Test for Rule 1.3.2a - Hero cards have the hero type
    Scenario: Hero card is classified as a hero-card
        Given a card has the type hero
        Then the card should be classified as a hero-card
        And the card should not be classified as a deck-card
        And the card should not be classified as a token-card
        And the card should not be classified as an arena-card

    # Test for Rule 1.3.2b - Token cards are not part of a player's card-pool
    Scenario: Token card is classified as a token-card and not part of card-pool
        Given a card has the type token
        Then the card should be classified as a token-card
        And the token card should not be considered part of a player's card-pool

    # Test for Rule 1.3.2c - Action cards are deck-cards
    Scenario: Action card is classified as a deck-card
        Given a card has the type action
        Then the card should be classified as a deck-card
        And the card may start the game in a player's deck

    # Test for Rule 1.3.2c - Attack Reaction cards are deck-cards
    Scenario: Attack reaction card is classified as a deck-card
        Given a card has the type attack reaction
        Then the card should be classified as a deck-card

    # Test for Rule 1.3.2c - Defense Reaction cards are deck-cards
    Scenario: Defense reaction card is classified as a deck-card
        Given a card has the type defense reaction
        Then the card should be classified as a deck-card

    # Test for Rule 1.3.2c - Instant cards are deck-cards
    Scenario: Instant card is classified as a deck-card
        Given a card has the type instant
        Then the card should be classified as a deck-card

    # Test for Rule 1.3.2c - Resource cards are deck-cards
    Scenario: Resource card is classified as a deck-card
        Given a card has the type resource
        Then the card should be classified as a deck-card

    # Test for Rule 1.3.2c - Mentor cards are deck-cards
    Scenario: Mentor card is classified as a deck-card
        Given a card has the type mentor
        Then the card should be classified as a deck-card

    # Test for Rule 1.3.2d - Equipment cards are arena-cards (not hero, token, or deck)
    Scenario: Equipment card is classified as an arena-card
        Given a card has the type equipment
        Then the card should be classified as an arena-card
        And the arena-card cannot start the game in a player's deck

    # Test for Rule 1.3.2d - Weapon cards are arena-cards
    Scenario: Weapon card is classified as an arena-card
        Given a card has the type weapon
        Then the card should be classified as an arena-card

    # ---- Rule 1.3.3: Permanents ----

    # Test for Rule 1.3.3 - Hero-cards in the arena are permanents
    Scenario: Hero card in arena is a permanent
        Given a hero card is in the arena
        Then the card should be considered a permanent

    # Test for Rule 1.3.3 - Arena-cards in arena are permanents
    Scenario: Equipment card in arena is a permanent
        Given an equipment card is in the arena
        Then the card should be considered a permanent

    # Test for Rule 1.3.3 - Token-cards in arena are permanents
    Scenario: Token card in arena is a permanent
        Given a token card is in the arena
        Then the card should be considered a permanent

    # Test for Rule 1.3.3 - Deck-cards in arena with permanent subtype are permanents
    Scenario: Deck card with Ally subtype in arena is a permanent
        Given a deck card with subtype ally is in the arena
        Then the card should be considered a permanent

    # Test for Rule 1.3.3 - Deck-cards in arena without permanent subtype are NOT permanents
    Scenario: Deck card without permanent subtype in arena is not a permanent
        Given an action card without permanent subtypes is in the arena
        Then the card should not be considered a permanent

    # Test for Rule 1.3.3 - Deck-cards on combat chain are NOT permanents
    Scenario: Deck card on combat chain is not a permanent
        Given an action card is on the combat chain
        Then the card should not be considered a permanent

    # Test for Rule 1.3.3a - Permanent leaving arena loses permanent status
    Scenario: Permanent that leaves arena is no longer a permanent
        Given an equipment card is in the arena
        And the card is considered a permanent
        When the card is removed from the arena
        Then the card should not be considered a permanent

    # Test for Rule 1.3.3b - Permanents start in untapped state
    Scenario: Permanent enters arena in untapped state
        Given an equipment card is placed into the arena
        Then the permanent should be in the untapped state

    # Test for Rule 1.3.3b - Permanents can be tapped
    Scenario: Permanent can be tapped
        Given an equipment card is in the arena
        And the permanent is in the untapped state
        When the permanent is tapped
        Then the permanent should be in the tapped state

    # Test for Rule 1.3.3b - Tapped permanent can be untapped
    Scenario: Tapped permanent can be untapped
        Given an equipment card is in the arena
        And the permanent is in the tapped state
        When the permanent is untapped
        Then the permanent should be in the untapped state

    # ---- Rule 1.3.4: Card distinctness ----

    # Test for Rule 1.3.4 - Cards with different names are distinct
    Scenario: Cards with different names are distinct
        Given one card has the name "Sink Below" and pitch value 1
        And another card has the name "Vaporize" and pitch value 1
        Then the two cards should be considered distinct

    # Test for Rule 1.3.4 - Cards with the same name but different pitch values are distinct
    Scenario: Cards with same name but different pitch values are distinct
        Given one card has the name "Sink Below" and pitch value 1
        And another card has the name "Sink Below" and pitch value 2
        Then the two cards should be considered distinct

    # Test for Rule 1.3.4 - Cards with the same name and same pitch are not distinct
    Scenario: Cards with identical name and pitch value are not distinct
        Given one card has the name "Sink Below" and pitch value 1
        And another card has the name "Sink Below" and pitch value 1
        Then the two cards should not be considered distinct
