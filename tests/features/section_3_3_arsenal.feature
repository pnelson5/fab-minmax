# Feature file for Section 3.3: Arsenal
# Reference: Flesh and Blood Comprehensive Rules Section 3.3
#
# 3.3.1 An arsenal zone is a private zone outside the arena, owned by a player.
#
# 3.3.2 An arsenal zone can only contain up to one of its owner's deck-cards. [1.3.2c]
#
# 3.3.2a If an effect would put a card into an arsenal zone that is not empty,
#         or into the arsenal and there are no empty arsenal zones, that effect fails.
#
# 3.3.3 The term "arsenal" refers to all arsenal zones owned by a player and the
#        cards in those zones.
#
# 3.3.3a A player's arsenal is considered empty if all of their arsenal zones are empty.
#
# 3.3.3b If a rule or effect would specify a card to move into a player's arsenal,
#         it is moved into one of their empty arsenal zones.
#
# 3.3.4 Cards in an arsenal zone may be played. [5.1]
#
# Cross-references:
# - 1.3.2c: Deck-cards (Action, Attack Reaction, Block, Defense Reaction, Instant, Mentor, Resource)
# - 3.0.4b: Arsenal zone is a private zone
# - 5.1: Playing cards from arsenal zone

Feature: Section 3.3 - Arsenal Zone
    As a game engine
    I need to correctly model the arsenal zone rules
    So that cards in the arsenal behave according to the comprehensive rules

    # ===== Rule 3.3.1: Arsenal is a private zone outside the arena =====

    # Test for Rule 3.3.1 - Arsenal zone is a private zone
    Scenario: An arsenal zone is a private zone
        Given a player owns an arsenal zone
        When checking the visibility of the arsenal zone
        Then the arsenal zone is a private zone
        And the arsenal zone is not a public zone

    # Test for Rule 3.3.1 - Arsenal zone is outside the arena
    Scenario: An arsenal zone is outside the arena
        Given a player owns an arsenal zone
        When checking if the arsenal zone is in the arena
        Then the arsenal zone is not in the arena

    # Test for Rule 3.3.1 - Arsenal zone is owned by a player
    Scenario: An arsenal zone is owned by a specific player
        Given player 0 owns an arsenal zone
        When checking the owner of the arsenal zone
        Then the arsenal zone is owned by player 0

    # ===== Rule 3.3.2: Arsenal can only contain up to one deck-card =====

    # Test for Rule 3.3.2 - Arsenal zone starts empty
    Scenario: An arsenal zone starts empty
        Given a player has an arsenal zone with no cards
        When checking the contents of the arsenal zone
        Then the arsenal zone is empty

    # Test for Rule 3.3.2 - Arsenal zone can contain one deck-card
    Scenario: An arsenal zone can contain exactly one deck-card
        Given a player has an empty arsenal zone
        And a deck-card is available to put in the arsenal
        When the deck-card is placed into the arsenal zone
        Then the arsenal zone contains exactly one card
        And the arsenal zone is not empty

    # Test for Rule 3.3.2 - Arsenal zone cannot contain more than one card
    Scenario: An arsenal zone cannot contain more than one card
        Given a player has an arsenal zone with one card already in it
        And a second deck-card is available
        When attempting to place the second card into the occupied arsenal zone
        Then the second placement attempt fails
        And the arsenal zone still contains only one card

    # Test for Rule 3.3.2 - Only deck-cards can go in the arsenal
    Scenario: Only deck-cards can be placed in the arsenal zone
        Given a player has an empty arsenal zone
        And a non-deck card (e.g., equipment) is available
        When attempting to place the non-deck card into the arsenal zone
        Then the placement of the non-deck card fails
        And the arsenal zone remains empty after non-deck rejection

    # ===== Rule 3.3.2a: Effect placing card into non-empty arsenal fails =====

    # Test for Rule 3.3.2a - Effect fails when arsenal zone is not empty
    Scenario: An effect placing a card into a non-empty arsenal zone fails
        Given a player has an arsenal zone with one card already in it
        When an effect attempts to place another card into that arsenal zone
        Then the effect fails due to the arsenal zone being non-empty

    # Test for Rule 3.3.2a - Effect fails when no empty arsenal zones exist
    Scenario: An effect placing a card into the arsenal fails when no empty arsenal zones exist
        Given a player has all arsenal zones occupied
        When an effect attempts to place a card into the player's arsenal
        Then the effect fails because there are no empty arsenal zones

    # ===== Rule 3.3.3: "Arsenal" refers to all arsenal zones and their cards =====

    # Test for Rule 3.3.3 - Arsenal refers to all arsenal zones owned by player
    Scenario: The term arsenal refers to all arsenal zones owned by a player
        Given a player has two arsenal zones
        And one arsenal zone contains a card
        And the other arsenal zone is empty
        When checking what the player's arsenal contains
        Then the arsenal contains all cards from all arsenal zones

    # ===== Rule 3.3.3a: Player's arsenal is empty only if ALL zones are empty =====

    # Test for Rule 3.3.3a - Arsenal is empty only when all zones are empty
    Scenario: A player's arsenal is empty only when all their arsenal zones are empty
        Given a player has two arsenal zones both empty
        When checking if the player's all-empty arsenal is empty
        Then the player's arsenal is considered empty

    # Test for Rule 3.3.3a - Arsenal is not empty if any zone has a card
    Scenario: A player's arsenal is not empty if any arsenal zone has a card
        Given a player has two arsenal zones
        And one of the player's arsenal zones contains a card
        When checking if the player's partially-filled arsenal is empty
        Then the player's arsenal is not considered empty

    # ===== Rule 3.3.3b: Moving card to arsenal goes to an empty zone =====

    # Test for Rule 3.3.3b - Card moved to arsenal goes to an empty zone
    Scenario: A card moved to the arsenal is placed in an empty arsenal zone
        Given a player has two arsenal zones
        And one arsenal zone is occupied and the other is empty
        When a rule instructs moving a card into the player's arsenal
        Then the card is moved into the empty arsenal zone

    # ===== Rule 3.3.4: Cards in arsenal may be played =====

    # Test for Rule 3.3.4 - Card in arsenal zone can be played
    Scenario: A card in an arsenal zone may be played
        Given a player has an arsenal zone with a deck-card in it
        When checking if the card in the arsenal can be played
        Then the card in the arsenal zone is playable

    # Test for Rule 3.3.4 - Only the specific card in arsenal can be played from there
    Scenario: Playing a card from the arsenal zone is permitted
        Given a player has an arsenal zone with an action card
        And the player has priority
        When the player plays the card from the arsenal zone
        Then the play from arsenal is permitted
        And the arsenal zone is empty after the card is played
