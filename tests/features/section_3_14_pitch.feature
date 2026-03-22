# Feature file for Section 3.14: Pitch
# Reference: Flesh and Blood Comprehensive Rules Section 3.14
#
# 3.14.1 A pitch zone is a public zone outside the arena, owned by a player.
#
# 3.14.2 A pitch zone can only contain its owner's deck-cards. [1.3.2c]
#
# Cross-references:
# - 3.0.2: each player has their own pitch zone (along with arms, arsenal,
#           banished, chest, deck, graveyard, hand, head, hero, legs zones)
# - 3.0.4a: pitch zone is listed as a public zone
# - 3.0.5b: pitch zone is NOT part of the arena
# - 3.0.1a: empty zone does not cease to exist
# - 1.3.2c: deck-cards are Action, Attack Reaction, Block, Defense Reaction,
#           Instant, Mentor, and Resource types
# - 1.14.3: to pitch a card, a player moves it from their hand to the pitch zone
#           and gains assets equal to the card's pitch value

Feature: Section 3.14 - Pitch Zone
    As a game engine
    I need to correctly model the pitch zone rules
    So that pitching resources, card tracking, and end-of-turn deck cycling work correctly

    # ===== Rule 3.14.1: Pitch zone is a public zone outside the arena =====

    # Test for Rule 3.14.1 - Pitch zone is a public zone
    Scenario: A pitch zone is a public zone
        Given a player owns a pitch zone
        When checking the visibility of the pitch zone
        Then the pitch zone is a public zone
        And the pitch zone is not a private zone

    # Test for Rule 3.14.1 - Pitch zone is outside the arena
    Scenario: A pitch zone is outside the arena
        Given a player owns a pitch zone
        When checking if the pitch zone is in the arena
        Then the pitch zone is not in the arena

    # Test for Rule 3.14.1 - Pitch zone is owned by a specific player
    Scenario: A pitch zone is owned by a specific player
        Given player 0 owns a pitch zone
        When checking the owner of the pitch zone
        Then the pitch zone is owned by player 0

    # Test for Rule 3.14.1 - Two players have separate pitch zones
    Scenario: Each player has their own separate pitch zone
        Given player 0 owns a pitch zone
        And player 1 owns a pitch zone
        When comparing the two pitch zones
        Then the two pitch zones are distinct and separate

    # ===== Rule 3.14.2: Pitch zone can only contain owner's deck-cards =====

    # Test for Rule 3.14.2 - Pitch zone starts empty
    Scenario: A pitch zone starts empty
        Given a player has an empty pitch zone
        When checking the contents of the pitch zone
        Then the pitch zone is empty

    # Test for Rule 3.14.2 - Pitch zone can contain owner's action card
    Scenario: A pitch zone can contain the owner's action card
        Given player 0 has a pitch zone and an action card they own
        When the owner's action card is placed in the pitch zone
        Then the pitch zone contains the owner's card
        And the pitch placement succeeds

    # Test for Rule 3.14.2 - Pitch zone can contain owner's attack reaction card
    Scenario: A pitch zone can contain the owner's attack reaction card
        Given player 0 has a pitch zone and an attack reaction card they own
        When the owner's attack reaction card is placed in the pitch zone
        Then the attack reaction pitch placement succeeds

    # Test for Rule 3.14.2 - Pitch zone can contain owner's instant card
    Scenario: A pitch zone can contain the owner's instant card
        Given player 0 has a pitch zone and an instant card they own
        When the owner's instant card is placed in the pitch zone
        Then the instant pitch placement succeeds

    # Test for Rule 3.14.2 - Pitch zone cannot contain non-deck-card
    Scenario: A pitch zone cannot contain an equipment card
        Given player 0 has a pitch zone
        And player 0 has an equipment card they own for pitch testing
        When attempting to place an equipment card in the pitch zone
        Then the pitch placement is rejected
        And the pitch zone remains empty after equipment rejection

    # Test for Rule 3.14.2 - Pitch zone cannot contain opponent's card
    Scenario: A pitch zone cannot contain an opponent's card
        Given player 0 has a pitch zone
        And player 1 has an action card they own for pitch testing
        When attempting to place player 1's card in player 0's pitch zone
        Then the opponent pitch placement is rejected
        And player 0's pitch zone remains empty

    # Test for Rule 3.14.2 - Cards in pitch belong to owner
    Scenario: Cards in the pitch zone belong to the zone owner
        Given player 0 has a pitch zone with their own action card in it
        When checking which cards are in the pitch zone
        Then all cards in the pitch zone are owned by player 0

    # Test for Rule 3.14.2 - Pitch zone can hold multiple owner cards
    Scenario: A pitch zone can contain multiple cards owned by the same player
        Given a player has an empty pitch zone
        And player 0 has three action cards they own for pitch testing
        When all three pitch cards are placed in the pitch zone
        Then the pitch zone contains all three cards
        And all three pitch cards are owned by player 0

    # ===== Cross-rule: Empty zone persists (Rule 3.0.1a) =====

    # Test for Rule 3.0.1a cross-ref - Empty pitch zone does not cease to exist
    Scenario: An empty pitch zone still exists
        Given a player has an empty pitch zone
        When checking if the pitch zone exists
        Then the pitch zone still exists even when empty
