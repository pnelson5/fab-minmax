# Feature file for Section 3.7: Deck
# Reference: Flesh and Blood Comprehensive Rules Section 3.7
#
# 3.7.1 A deck zone is a private zone outside the arena, owned by a player.
#
# 3.7.2 A deck zone can only contain its owner's deck-cards. [1.3.2c]
#       Deck-cards: Action, Attack Reaction, Block, Defense Reaction, Instant, Mentor, Resource
#
# 3.7.3 The term "deck" refers to the deck zone.
#
# 3.7.4 A player cannot look at objects in their own deck zone unless specified by a rule or effect.
#
# 3.7.5 Objects in the deck zone are placed face down in an ordered uniform pile.
#
# 3.7.6 A player's starting deck starts the game in their deck zone. [4.1]
#
# Cross-references:
# - 1.3.2c: Deck-cards are Action, Attack Reaction, Block, Defense Reaction, Instant, Mentor, Resource
# - 3.0.4b: deck zone is listed as a private zone
# - 3.0.5b: deck zone is NOT part of the arena
# - 3.0.2: each player owns their own deck zone
# - 3.0.1a: empty zone does not cease to exist
# - 4.1: starting deck placement rules

Feature: Section 3.7 - Deck Zone
    As a game engine
    I need to correctly model the deck zone rules
    So that card draw, deck searching, and game start mechanics work correctly

    # ===== Rule 3.7.1: Deck zone is a private zone outside the arena =====

    # Test for Rule 3.7.1 - Deck zone is a private zone
    Scenario: A deck zone is a private zone
        Given a player owns a deck zone
        When checking the visibility of the deck zone
        Then the deck zone is a private zone
        And the deck zone is not a public zone

    # Test for Rule 3.7.1 - Deck zone is outside the arena
    Scenario: A deck zone is outside the arena
        Given a player owns a deck zone
        When checking if the deck zone is in the arena
        Then the deck zone is not in the arena

    # Test for Rule 3.7.1 - Deck zone is owned by a specific player
    Scenario: A deck zone is owned by a specific player
        Given player 0 has a deck zone
        When checking the owner of the deck zone
        Then the deck zone is owned by player 0

    # Test for Rule 3.7.1 - Each player has their own deck zone
    Scenario: Each player has their own separate deck zone
        Given player 0 has a deck zone
        And player 1 has a deck zone
        When comparing the two deck zones
        Then the two deck zones are distinct and separate

    # ===== Rule 3.7.2: Deck zone can only contain owner's deck-cards =====

    # Test for Rule 3.7.2 - Deck zone starts empty
    Scenario: A deck zone starts empty
        Given a player has an empty deck zone
        When checking the contents of the deck zone
        Then the deck zone is empty

    # Test for Rule 3.7.2 - Deck zone can contain owner's action card
    Scenario: A deck zone can contain the owner's action card
        Given player 0 has a deck zone and an action card they own
        When the owner's action card is placed in the deck zone
        Then the deck zone contains the owner's action card
        And the deck card placement succeeds

    # Test for Rule 3.7.2 - Deck zone can contain various deck-card types
    Scenario: A deck zone can contain action reaction cards
        Given player 0 has a deck zone and an attack reaction card they own
        When the owner's attack reaction card is placed in the deck zone
        Then the deck zone contains the owner's attack reaction card

    # Test for Rule 3.7.2 - Deck zone can contain defense reaction cards
    Scenario: A deck zone can contain defense reaction cards
        Given player 0 has a deck zone and a defense reaction card they own
        When the owner's defense reaction card is placed in the deck zone
        Then the deck zone contains the owner's defense reaction card

    # Test for Rule 3.7.2 - Deck zone can contain instant cards
    Scenario: A deck zone can contain instant cards
        Given player 0 has a deck zone and an instant card they own
        When the owner's instant card is placed in the deck zone
        Then the deck zone contains the owner's instant card

    # Test for Rule 3.7.2 - Non-deck cards cannot start in the deck zone
    Scenario: A non-deck card cannot be placed in the deck zone
        Given player 0 has a deck zone
        And player 0 has an equipment card they own
        When attempting to place the equipment card in player 0's deck zone
        Then the equipment placement in deck zone is rejected
        And player 0's deck zone remains empty

    # Test for Rule 3.7.2 - Opponent's card cannot be placed in deck zone
    Scenario: An opponent's card cannot be placed in a player's deck zone
        Given player 0 has a deck zone
        And player 1 has an action card they own
        When attempting to place player 1's card in player 0's deck zone
        Then the placement of opponent's card in deck zone is rejected
        And player 0's deck zone remains empty after opponent card rejection

    # Test for Rule 3.7.2 - Deck zone can hold multiple owner deck-cards
    Scenario: A deck zone can contain multiple deck-cards from the same owner
        Given player 0 has an empty deck zone
        And player 0 has several action cards they own
        When all the action cards are placed in the deck zone
        Then the deck zone contains all the owner's action cards

    # ===== Rule 3.7.3: "Deck" refers to the deck zone =====

    # Test for Rule 3.7.3 - "Deck" refers to the deck zone
    Scenario: The term deck refers to the deck zone
        Given a game with a registered deck zone
        When resolving the game term "deck"
        Then the term "deck" refers to the deck zone

    # ===== Rule 3.7.4: Player cannot look at their own deck zone =====

    # Test for Rule 3.7.4 - Player cannot freely look at their deck
    Scenario: A player cannot look at their own deck zone without permission
        Given player 0 has a deck zone with cards in it
        When player 0 attempts to look at their own deck zone without a rule or effect
        Then looking at the deck zone is not permitted by default

    # Test for Rule 3.7.4 - Player CAN look at deck when rule or effect specifies
    Scenario: A player can look at their deck zone when specified by a rule or effect
        Given player 0 has a deck zone with cards in it
        And an effect specifies that the player may look at their deck
        When player 0 attempts to look at their own deck zone with the effect active
        Then looking at the deck zone is permitted by the effect

    # ===== Rule 3.7.5: Objects in deck zone are face down in ordered pile =====

    # Test for Rule 3.7.5 - Cards in deck zone are face down
    Scenario: Cards in the deck zone are placed face down
        Given player 0 has a deck zone with cards in it
        When checking the orientation of cards in the deck zone
        Then the cards in the deck zone are face down

    # Test for Rule 3.7.5 - Deck zone maintains an ordered pile
    Scenario: The deck zone maintains an ordered pile of cards
        Given player 0 has a deck zone with several cards placed in a specific order
        When checking the order of cards in the deck zone
        Then the cards are in an ordered pile
        And the first card placed is at the bottom of the pile

    # ===== Rule 3.7.6: Starting deck starts in the deck zone =====

    # Test for Rule 3.7.6 - Starting deck is placed in deck zone at game start
    Scenario: A player's starting deck starts in their deck zone
        Given player 0 has a starting deck of cards
        When the game is started
        Then all starting deck cards are in player 0's deck zone

    # ===== Cross-rule: Empty zone persists (Rule 3.0.1a) =====

    # Test for Rule 3.0.1a cross-ref - Empty deck zone does not cease to exist
    Scenario: An empty deck zone still exists
        Given a player has an empty deck zone
        When checking if the deck zone exists
        Then the deck zone still exists even when empty
