# Feature file for Section 1.3.1a: Card Ownership
# Reference: Flesh and Blood Comprehensive Rules Section 1.3.1a
#
# Rule 1.3.1a: The owner of a card is the player who started the game with that card 
# as their hero or as part of their card-pool, or the player instructed to create it 
# or otherwise put it into the game.

Feature: Section 1.3.1a - Card Ownership
    As a game engine
    I need to track card ownership correctly
    So that cards always know which player owns them regardless of zone or controller

    # Test for Rule 1.3.1a - Cards in starting deck are owned by that player
    Scenario: Cards in starting deck are owned by the player who started with them
        Given player 0 has a card in their starting deck
        When the game begins
        Then the card should be owned by player 0
        And the card owner should not change when moved to hand
        And the card owner should not change when played

    # Test for Rule 1.3.1a - Hero card is owned by the player who started with it
    Scenario: Hero card is owned by the player who started with it
        Given player 1 has a hero card
        When the game begins
        Then the hero card should be owned by player 1
        And the hero card owner should never change

    # Test for Rule 1.3.1a - Created tokens are owned by the player who created them
    Scenario: Token created by a player is owned by that player
        Given player 0 is instructed to create a token
        When the token is created
        Then the token should be owned by player 0
        And the token owner should be player 0 even if it moves zones

    # Test for Rule 1.3.1a - Ownership persists across zones
    Scenario: Card ownership persists when card moves between zones
        Given player 0 owns a card in their hand
        When the card is moved to the graveyard
        Then the card should still be owned by player 0
        When the card is moved to the banished zone
        Then the card should still be owned by player 0
        When the card is moved to the deck
        Then the card should still be owned by player 0

    # Test for Rule 1.3.1a - Ownership is independent of controller
    Scenario: Card ownership is independent of who controls it
        Given player 0 owns a card
        And player 1 controls the card
        Then the card should be owned by player 0
        And the card should be controlled by player 1
        And ownership and control should be independent properties

    # Test for Rule 1.3.1a - Card pool determines initial ownership
    Scenario: Cards included in a player's card-pool are owned by that player
        Given player 1 includes a card in their card-pool
        When the card is added to their deck during setup
        Then the card should be owned by player 1
        And the ownership should be established at game start

    # Test for Rule 1.3.1a - Opponent's cards remain owned by opponent
    Scenario: Cards stolen or copied remain owned by original owner
        Given player 0 owns a card
        When player 1 takes control of the card
        Then the card should still be owned by player 0
        And the card should be controlled by player 1
        And player 1 should not become the owner
