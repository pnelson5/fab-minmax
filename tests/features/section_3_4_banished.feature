# Feature file for Section 3.4: Banished
# Reference: Flesh and Blood Comprehensive Rules Section 3.4
#
# 3.4.1 A banished zone is a public zone outside the arena, owned by a player.
#
# 3.4.2 A banished zone can only contain its owner's cards.
#
# Cross-references:
# - 3.0.4a: banished zone is listed as a public zone
# - 3.0.5b: banished zone is NOT part of the arena
# - 3.0.2: each player owns their own banished zone
# - 3.0.1a: empty zone does not cease to exist

Feature: Section 3.4 - Banished Zone
    As a game engine
    I need to correctly model the banished zone rules
    So that card banishment mechanics work correctly

    # ===== Rule 3.4.1: Banished zone is a public zone outside the arena =====

    # Test for Rule 3.4.1 - Banished zone is a public zone
    Scenario: A banished zone is a public zone
        Given a player owns a banished zone
        When checking the visibility of the banished zone
        Then the banished zone is a public zone
        And the banished zone is not a private zone

    # Test for Rule 3.4.1 - Banished zone is outside the arena
    Scenario: A banished zone is outside the arena
        Given a player owns a banished zone
        When checking if the banished zone is in the arena
        Then the banished zone is not in the arena

    # Test for Rule 3.4.1 - Banished zone is owned by a specific player
    Scenario: A banished zone is owned by a specific player
        Given player 0 owns a banished zone
        When checking the owner of the banished zone
        Then the banished zone is owned by player 0

    # Test for Rule 3.4.1 - Two players have separate banished zones
    Scenario: Each player has their own separate banished zone
        Given player 0 owns a banished zone
        And player 1 owns a banished zone
        When comparing the two banished zones
        Then the two banished zones are distinct and separate

    # ===== Rule 3.4.2: Banished zone can only contain owner's cards =====

    # Test for Rule 3.4.2 - Banished zone starts empty
    Scenario: A banished zone starts empty
        Given a player has an empty banished zone
        When checking the contents of the banished zone
        Then the banished zone is empty

    # Test for Rule 3.4.2 - Banished zone can contain owner's card
    Scenario: A banished zone can contain the owner's card
        Given player 0 has a banished zone and a card they own
        When the owner's card is placed in the banished zone
        Then the banished zone contains the owner's card
        And the placement succeeds

    # Test for Rule 3.4.2 - Banished zone cannot contain opponent's cards
    Scenario: A banished zone cannot contain an opponent's card
        Given player 0 has a banished zone
        And player 1 has a card they own
        When attempting to place player 1's card in player 0's banished zone
        Then the placement is rejected
        And player 0's banished zone remains empty

    # Test for Rule 3.4.2 - Owner's card in banished is retrievable
    Scenario: Cards owned by the player are retrievable from banished zone
        Given player 0 has a banished zone with their own card in it
        When checking which cards are in the banished zone
        Then all cards in the banished zone are owned by player 0

    # Test for Rule 3.4.2 - Banished zone can hold multiple owner cards
    Scenario: A banished zone can contain multiple cards owned by the same player
        Given a player has an empty banished zone
        And player 0 has three cards they own
        When all three cards are placed in the banished zone
        Then the banished zone contains all three cards
        And all three cards are owned by player 0

    # ===== Cross-rule: Empty zone persists (Rule 3.0.1a) =====

    # Test for Rule 3.0.1a cross-ref - Empty banished zone does not cease to exist
    Scenario: An empty banished zone still exists
        Given a player has an empty banished zone
        When checking if the banished zone exists
        Then the banished zone still exists even when empty
