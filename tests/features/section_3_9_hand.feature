# Feature file for Section 3.9: Hand
# Reference: Flesh and Blood Comprehensive Rules Section 3.9
#
# 3.9.1 A hand zone is a private zone outside the arena, owned by a player.
#
# 3.9.2 A hand zone can only contain its owner's deck-cards. [1.3.2c]
#
# 3.9.3 The term "hand" refers to the hand zone.
#
# Cross-references:
# - 3.0.4b: hand zone is listed as a private zone
# - 3.0.5b: hand zone is NOT part of the arena
# - 3.0.2: each player owns their own hand zone
# - 3.0.1a: empty zone does not cease to exist
# - 1.3.2c: deck-cards are Action, Attack Reaction, Block, Defense Reaction, Instant, Mentor, Resource

Feature: Section 3.9 - Hand Zone
    As a game engine
    I need to correctly model the hand zone rules
    So that card draw, hand management, and play-from-hand mechanics work correctly

    # ===== Rule 3.9.1: Hand zone is a private zone outside the arena =====

    # Test for Rule 3.9.1 - Hand zone is a private zone
    Scenario: A hand zone is a private zone
        Given a player owns a hand zone
        When checking the visibility of the hand zone
        Then the hand zone is a private zone
        And the hand zone is not a public zone

    # Test for Rule 3.9.1 - Hand zone is outside the arena
    Scenario: A hand zone is outside the arena
        Given a player owns a hand zone
        When checking if the hand zone is in the arena
        Then the hand zone is not in the arena

    # Test for Rule 3.9.1 - Hand zone is owned by a specific player
    Scenario: A hand zone is owned by a specific player
        Given player 0 owns a hand zone
        When checking the owner of the hand zone
        Then the hand zone is owned by player 0

    # Test for Rule 3.9.1 - Two players have separate hand zones
    Scenario: Each player has their own separate hand zone
        Given player 0 owns a hand zone
        And player 1 owns a hand zone
        When comparing the two hand zones
        Then the two hand zones are distinct and separate

    # ===== Rule 3.9.2: Hand zone can only contain owner's deck-cards =====

    # Test for Rule 3.9.2 - Hand zone starts empty
    Scenario: A hand zone starts empty
        Given a player has an empty hand zone
        When checking the contents of the hand zone
        Then the hand zone is empty

    # Test for Rule 3.9.2 - Hand zone can contain owner's action card
    Scenario: A hand zone can contain the owner's action card
        Given player 0 has a hand zone and an action card they own
        When the owner's action card is placed in the hand zone
        Then the hand zone contains the owner's card
        And the hand placement succeeds

    # Test for Rule 3.9.2 - Hand zone can contain owner's attack reaction card
    Scenario: A hand zone can contain the owner's attack reaction card
        Given player 0 has a hand zone and an attack reaction card they own
        When the owner's attack reaction card is placed in the hand zone
        Then the attack reaction hand placement succeeds

    # Test for Rule 3.9.2 - Hand zone can contain owner's defense reaction card
    Scenario: A hand zone can contain the owner's defense reaction card
        Given player 0 has a hand zone and a defense reaction card they own
        When the owner's defense reaction card is placed in the hand zone
        Then the defense reaction hand placement succeeds

    # Test for Rule 3.9.2 - Hand zone can contain owner's instant card
    Scenario: A hand zone can contain the owner's instant card
        Given player 0 has a hand zone and an instant card they own
        When the owner's instant card is placed in the hand zone
        Then the instant hand placement succeeds

    # Test for Rule 3.9.2 - Hand zone cannot contain non-deck card
    Scenario: A hand zone cannot contain an equipment card
        Given player 0 has a hand zone
        And player 0 has an equipment card they own for hand testing
        When attempting to place an equipment card in the hand zone
        Then the hand placement is rejected
        And the hand zone remains empty after equipment rejection

    # Test for Rule 3.9.2 - Hand zone cannot contain opponent's card
    Scenario: A hand zone cannot contain an opponent's card
        Given player 0 has a hand zone
        And player 1 has an action card they own for hand testing
        When attempting to place player 1's card in player 0's hand zone
        Then the opponent hand placement is rejected
        And player 0's hand zone remains empty

    # Test for Rule 3.9.2 - Cards in hand belong to owner
    Scenario: Cards in the hand zone belong to the zone owner
        Given player 0 has a hand zone with their own action card in it
        When checking which cards are in the hand zone
        Then all cards in the hand zone are owned by player 0

    # Test for Rule 3.9.2 - Hand zone can hold multiple owner cards
    Scenario: A hand zone can contain multiple cards owned by the same player
        Given a player has an empty hand zone
        And player 0 has three action cards they own for hand testing
        When all three hand cards are placed in the hand zone
        Then the hand zone contains all three cards
        And all three hand cards are owned by player 0

    # ===== Rule 3.9.3: The term "hand" refers to the hand zone =====

    # Test for Rule 3.9.3 - Term "hand" refers to hand zone
    Scenario: The term hand refers to the hand zone
        Given a player has a hand zone registered in the zone registry
        When resolving the term "hand" for that player
        Then the resolved hand zone is the player's hand zone

    # ===== Cross-rule: Empty zone persists (Rule 3.0.1a) =====

    # Test for Rule 3.0.1a cross-ref - Empty hand zone does not cease to exist
    Scenario: An empty hand zone still exists
        Given a player has an empty hand zone
        When checking if the hand zone exists
        Then the hand zone still exists even when empty
