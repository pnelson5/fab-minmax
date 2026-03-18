# Feature file for Section 3.8: Graveyard
# Reference: Flesh and Blood Comprehensive Rules Section 3.8
#
# 3.8.1 A graveyard zone is a public zone outside the arena, owned by a player.
#
# 3.8.2 A graveyard zone can only contain its owner's cards.
#
# 3.8.3 The term "graveyard" refers to the graveyard zone.
#
# Cross-references:
# - 3.0.4a: graveyard zone is listed as a public zone
# - 3.0.5b: graveyard zone is NOT part of the arena
# - 3.0.2: each player owns their own graveyard zone
# - 3.0.1a: empty zone does not cease to exist

Feature: Section 3.8 - Graveyard Zone
    As a game engine
    I need to correctly model the graveyard zone rules
    So that card discard and death mechanics work correctly

    # ===== Rule 3.8.1: Graveyard zone is a public zone outside the arena =====

    # Test for Rule 3.8.1 - Graveyard zone is a public zone
    Scenario: A graveyard zone is a public zone
        Given a player owns a graveyard zone
        When checking the visibility of the graveyard zone
        Then the graveyard zone is a public zone
        And the graveyard zone is not a private zone

    # Test for Rule 3.8.1 - Graveyard zone is outside the arena
    Scenario: A graveyard zone is outside the arena
        Given a player owns a graveyard zone
        When checking if the graveyard zone is in the arena
        Then the graveyard zone is not in the arena

    # Test for Rule 3.8.1 - Graveyard zone is owned by a specific player
    Scenario: A graveyard zone is owned by a specific player
        Given player 0 owns a graveyard zone
        When checking the owner of the graveyard zone
        Then the graveyard zone is owned by player 0

    # Test for Rule 3.8.1 - Two players have separate graveyard zones
    Scenario: Each player has their own separate graveyard zone
        Given player 0 owns a graveyard zone
        And player 1 owns a graveyard zone
        When comparing the two graveyard zones
        Then the two graveyard zones are distinct and separate

    # ===== Rule 3.8.2: Graveyard zone can only contain owner's cards =====

    # Test for Rule 3.8.2 - Graveyard zone starts empty
    Scenario: A graveyard zone starts empty
        Given a player has an empty graveyard zone
        When checking the contents of the graveyard zone
        Then the graveyard zone is empty

    # Test for Rule 3.8.2 - Graveyard zone can contain owner's card
    Scenario: A graveyard zone can contain the owner's card
        Given player 0 has a graveyard zone and a card they own
        When the owner's card is placed in the graveyard zone
        Then the graveyard zone contains the owner's card
        And the graveyard placement succeeds

    # Test for Rule 3.8.2 - Graveyard zone cannot contain opponent's cards
    Scenario: A graveyard zone cannot contain an opponent's card
        Given player 0 has a graveyard zone
        And player 1 has a card they own for graveyard testing
        When attempting to place player 1's card in player 0's graveyard zone
        Then the graveyard placement is rejected
        And player 0's graveyard zone remains empty

    # Test for Rule 3.8.2 - Owner's card in graveyard is retrievable
    Scenario: Cards owned by the player are retrievable from graveyard zone
        Given player 0 has a graveyard zone with their own card in it
        When checking which cards are in the graveyard zone
        Then all cards in the graveyard zone are owned by player 0

    # Test for Rule 3.8.2 - Graveyard zone can hold multiple owner cards
    Scenario: A graveyard zone can contain multiple cards owned by the same player
        Given a player has an empty graveyard zone
        And player 0 has three cards they own for graveyard testing
        When all three cards are placed in the graveyard zone
        Then the graveyard zone contains all three cards
        And all three graveyard cards are owned by player 0

    # ===== Rule 3.8.3: The term "graveyard" refers to the graveyard zone =====

    # Test for Rule 3.8.3 - Term "graveyard" refers to graveyard zone
    Scenario: The term graveyard refers to the graveyard zone
        Given a player has a graveyard zone registered in the zone registry
        When resolving the term "graveyard" for that player
        Then the resolved zone is the player's graveyard zone

    # ===== Cross-rule: Empty zone persists (Rule 3.0.1a) =====

    # Test for Rule 3.0.1a cross-ref - Empty graveyard zone does not cease to exist
    Scenario: An empty graveyard zone still exists
        Given a player has an empty graveyard zone
        When checking if the graveyard zone exists
        Then the graveyard zone still exists even when empty
