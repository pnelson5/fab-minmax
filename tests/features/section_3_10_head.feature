# Feature file for Section 3.10: Head
# Reference: Flesh and Blood Comprehensive Rules Section 3.10
#
# 3.10.1 A head zone is a public equipment zone in the arena, owned by a player.
#
# 3.10.2 A head zone can only contain up to one object which is equipped to that
#         zone. [8.5.41]
#
# 3.10.2a An object can only be equipped to a head zone if it has subtype head.
#
# 3.10.3 A player may equip a head card to their head zone at the start of the game. [4.1]
#
# Cross-references:
# - 3.0.4a: head zone is a public zone
# - 3.1.1: head zone is an arena zone
# - 8.5.41: Equip is a discrete effect; puts object into equipment zone as a permanent
# - 8.5.41b: Object can only be equipped if it has one of: 1H, 2H, Arms, Chest, Head, Legs, Off-Hand, or Quiver
# - 8.5.41c: Object can only be equipped to a zone if the zone is empty and it is not already equipped to a zone of the same type
# - 3.0.1a: A zone is empty when it does not contain any objects and has no permanents equipped to it

Feature: Section 3.10 - Head Zone
    As a game engine
    I need to correctly model the head zone rules
    So that equipment management in the head zone works correctly

    # ===== Rule 3.10.1: Head zone is a public equipment zone in the arena =====

    # Test for Rule 3.10.1 - Head zone is a public zone
    Scenario: A head zone is a public zone
        Given a player owns a head zone
        When checking the visibility of the head zone
        Then the head zone is a public zone
        And the head zone is not a private zone

    # Test for Rule 3.10.1 - Head zone is an equipment zone
    Scenario: A head zone is an equipment zone
        Given a player owns a head zone
        When checking the zone type of the head zone
        Then the head zone is classified as an equipment zone

    # Test for Rule 3.10.1 - Head zone is in the arena
    Scenario: A head zone is in the arena
        Given a player owns a head zone
        When checking if the head zone is in the arena
        Then the head zone is in the arena

    # Test for Rule 3.10.1 - Head zone is owned by a player
    Scenario: A head zone is owned by a specific player
        Given player 0 owns a head zone
        When checking the owner of the head zone
        Then the head zone is owned by player 0

    # ===== Rule 3.10.2: Head zone can contain up to one equipped object =====

    # Test for Rule 3.10.2 - Head zone starts empty
    Scenario: A head zone starts empty
        Given a player has a head zone with no equipped cards
        When checking the contents of the head zone
        Then the head zone is empty
        And the empty head zone is exposed

    # Test for Rule 3.10.2 - Head zone can contain exactly one equipped object
    Scenario: A head zone can contain exactly one equipped object
        Given a player has a head zone with no equipped cards
        And a card with subtype head is available
        When the head card is equipped to the head zone
        Then the head zone contains exactly one equipped object
        And the head zone is not empty

    # Test for Rule 3.10.2 - Head zone cannot contain more than one object
    Scenario: A head zone cannot contain more than one equipped object
        Given a player has a head zone with one head card already equipped
        And a second head card is available
        When attempting to equip the second head card to the head zone
        Then the second head equip attempt fails
        And the head zone still contains only one equipped object

    # ===== Rule 3.10.2a: Only objects with subtype head can be equipped to head zone =====

    # Test for Rule 3.10.2a - Card with subtype head can be equipped to head zone
    Scenario: A card with subtype head can be equipped to the head zone
        Given a player has an empty head zone
        And a card has subtype head
        When the card is equipped to the head zone
        Then the card is successfully equipped to the head zone
        And the card is in the head zone as a permanent

    # Test for Rule 3.10.2a - Card without subtype head cannot be equipped to head zone
    Scenario: A card without subtype head cannot be equipped to the head zone
        Given a player has an empty head zone
        And a card does not have subtype head
        When attempting to equip the non-head card to the head zone
        Then the non-head equip attempt is rejected
        And the head zone remains empty after non-head rejection

    # Test for Rule 3.10.2a - Card with subtype arms is rejected from head zone
    Scenario: A card with subtype arms cannot be equipped to the head zone
        Given a player has an empty head zone
        And a card has subtype arms but not subtype head
        When attempting to equip the arms card to the head zone
        Then the arms equip attempt to head zone is rejected
        And the head zone remains empty after arms rejection

    # Test for Rule 3.10.2a - Head card equipped to head zone is a permanent
    Scenario: A head card equipped to head zone is a permanent
        Given a player has an empty head zone
        And an equipment card has subtype head
        When the head equipment card is equipped to the head zone
        Then the equipped head card is a permanent in the head zone
        And the card has the head subtype

    # ===== Rule 3.10.3: Player may equip head card at start of game =====

    # Test for Rule 3.10.3 - Player may equip head card at start of game
    Scenario: A player may equip a head card to their head zone at the start of the game
        Given a player has a head card in their starting inventory
        When the start of game head equip procedure runs with equipping
        Then the player may equip the head card to their head zone
        And the head card is in the head zone as a permanent after equipping

    # Test for Rule 3.10.3 - Player's head zone is empty if they choose not to equip
    Scenario: A player's head zone is empty if they choose not to equip at game start
        Given a player chooses not to equip any head card at game start
        When the start of game head equip procedure runs without equipping
        Then the player's head zone is empty
        And the unequipped head zone is exposed

    # ===== Cross-rule: Zone empty definition includes equipped permanents =====

    # Test for Rule 3.0.1a cross-ref - Head zone is empty only if it has no objects and no equipped permanents
    Scenario: A head zone is not empty when it has an equipped permanent
        Given a player has a head zone with a head card equipped
        When checking if the head zone is empty
        Then the head zone is not empty because it has an equipped permanent

    # Test for Rule 8.5.41c cross-ref - Head zone must be empty before equipping
    Scenario: A head card can only be equipped if the head zone is empty
        Given a player has a head zone with one head card already equipped
        And the head zone is therefore not empty
        When attempting to equip another head card to the occupied head zone
        Then the head equip attempt fails because the zone is not empty
