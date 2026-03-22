# Feature file for Section 3.12: Legs
# Reference: Flesh and Blood Comprehensive Rules Section 3.12
#
# 3.12.1 A legs zone is a public equipment zone in the arena, owned by a player.
#
# 3.12.2 A legs zone can only contain up to one object which is equipped to that
#         zone. [8.5.41]
#
# 3.12.2a An object can only be equipped to a legs zone if it has subtype legs.
#
# 3.12.3 A player may equip a legs card to their legs zone at the start of the game. [4.1]
#
# Cross-references:
# - 3.0.4a: legs zone is a public zone
# - 3.1.1: legs zone is an arena zone
# - 8.5.41: Equip is a discrete effect; puts object into equipment zone as a permanent
# - 8.5.41b: Object can only be equipped if it has one of: 1H, 2H, Arms, Chest, Head, Legs, Off-Hand, or Quiver
# - 8.5.41c: Object can only be equipped to a zone if the zone is empty and it is not already equipped to a zone of the same type
# - 3.0.1a: A zone is empty when it does not contain any objects and has no permanents equipped to it

Feature: Section 3.12 - Legs Zone
    As a game engine
    I need to correctly model the legs zone rules
    So that equipment management in the legs zone works correctly

    # ===== Rule 3.12.1: Legs zone is a public equipment zone in the arena =====

    # Test for Rule 3.12.1 - Legs zone is a public zone
    Scenario: A legs zone is a public zone
        Given a player owns a legs zone
        When checking the visibility of the legs zone
        Then the legs zone is a public zone
        And the legs zone is not a private zone

    # Test for Rule 3.12.1 - Legs zone is an equipment zone
    Scenario: A legs zone is an equipment zone
        Given a player owns a legs zone
        When checking the zone type of the legs zone
        Then the legs zone is classified as an equipment zone

    # Test for Rule 3.12.1 - Legs zone is in the arena
    Scenario: A legs zone is in the arena
        Given a player owns a legs zone
        When checking if the legs zone is in the arena
        Then the legs zone is in the arena

    # Test for Rule 3.12.1 - Legs zone is owned by a player
    Scenario: A legs zone is owned by a specific player
        Given player 0 owns a legs zone
        When checking the owner of the legs zone
        Then the legs zone is owned by player 0

    # ===== Rule 3.12.2: Legs zone can contain up to one equipped object =====

    # Test for Rule 3.12.2 - Legs zone starts empty
    Scenario: A legs zone starts empty
        Given a player has a legs zone with no equipped cards
        When checking the contents of the legs zone
        Then the legs zone is empty
        And the empty legs zone is exposed

    # Test for Rule 3.12.2 - Legs zone can contain exactly one equipped object
    Scenario: A legs zone can contain exactly one equipped object
        Given a player has a legs zone with no equipped cards
        And a card with subtype legs is available
        When the legs card is equipped to the legs zone
        Then the legs zone contains exactly one equipped object
        And the legs zone is not empty

    # Test for Rule 3.12.2 - Legs zone cannot contain more than one object
    Scenario: A legs zone cannot contain more than one equipped object
        Given a player has a legs zone with one legs card already equipped
        And a second legs card is available
        When attempting to equip the second legs card to the legs zone
        Then the second legs equip attempt fails
        And the legs zone still contains only one equipped object

    # ===== Rule 3.12.2a: Only objects with subtype legs can be equipped to legs zone =====

    # Test for Rule 3.12.2a - Card with subtype legs can be equipped to legs zone
    Scenario: A card with subtype legs can be equipped to the legs zone
        Given a player has an empty legs zone
        And a card has subtype legs
        When the card is equipped to the legs zone
        Then the card is successfully equipped to the legs zone
        And the card is in the legs zone as a permanent

    # Test for Rule 3.12.2a - Card without subtype legs cannot be equipped to legs zone
    Scenario: A card without subtype legs cannot be equipped to the legs zone
        Given a player has an empty legs zone
        And a card does not have subtype legs
        When attempting to equip the non-legs card to the legs zone
        Then the non-legs equip attempt is rejected
        And the legs zone remains empty after non-legs rejection

    # Test for Rule 3.12.2a - Card with subtype arms is rejected from legs zone
    Scenario: A card with subtype arms cannot be equipped to the legs zone
        Given a player has an empty legs zone
        And a card has subtype arms but not subtype legs
        When attempting to equip the arms card to the legs zone
        Then the arms equip attempt to legs zone is rejected
        And the legs zone remains empty after arms rejection

    # Test for Rule 3.12.2a - Legs card equipped to legs zone is a permanent
    Scenario: A legs card equipped to legs zone is a permanent
        Given a player has an empty legs zone
        And an equipment card has subtype legs
        When the legs equipment card is equipped to the legs zone
        Then the equipped legs card is a permanent in the legs zone
        And the card has the legs subtype

    # ===== Rule 3.12.3: Player may equip legs card at start of game =====

    # Test for Rule 3.12.3 - Player may equip legs card at start of game
    Scenario: A player may equip a legs card to their legs zone at the start of the game
        Given a player has a legs card in their starting inventory
        When the start of game legs equip procedure runs with equipping
        Then the player may equip the legs card to their legs zone
        And the legs card is in the legs zone as a permanent after equipping

    # Test for Rule 3.12.3 - Player's legs zone is empty if they choose not to equip
    Scenario: A player's legs zone is empty if they choose not to equip at game start
        Given a player chooses not to equip any legs card at game start
        When the start of game legs equip procedure runs without equipping
        Then the player's legs zone is empty
        And the unequipped legs zone is exposed

    # ===== Cross-rule: Zone empty definition includes equipped permanents =====

    # Test for Rule 3.0.1a cross-ref - Legs zone is empty only if it has no objects and no equipped permanents
    Scenario: A legs zone is not empty when it has an equipped permanent
        Given a player has a legs zone with a legs card equipped
        When checking if the legs zone is empty
        Then the legs zone is not empty because it has an equipped permanent

    # Test for Rule 8.5.41c cross-ref - Legs zone must be empty before equipping
    Scenario: A legs card can only be equipped if the legs zone is empty
        Given a player has a legs zone with one legs card already equipped
        And the legs zone is therefore not empty
        When attempting to equip another legs card to the occupied legs zone
        Then the legs equip attempt fails because the zone is not empty
