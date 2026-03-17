# Feature file for Section 3.2: Arms
# Reference: Flesh and Blood Comprehensive Rules Section 3.2
#
# 3.2.1 An arms zone is a public equipment zone in the arena, owned by a player.
#
# 3.2.2 An arms zone can only contain up to one object which is equipped to that
#        zone. [8.5.41]
#
# 3.2.2a An object can only be equipped to an arms zone if it has subtype arms.
#
# 3.2.3 A player may equip an arms card to their arms zone at the start of the game. [4.1]
#
# Cross-references:
# - 3.0.4a: arms zone is a public zone
# - 3.1.1: arms zone is an arena zone
# - 8.5.41: Equip is a discrete effect; puts object into equipment zone as a permanent
# - 8.5.41b: Object can only be equipped if it has one of: 1H, 2H, Arms, Chest, Heads, Legs, Off-Hand, or Quiver
# - 8.5.41c: Object can only be equipped to a zone if the zone is empty and it is not already equipped to a zone of the same type
# - 3.0.1a: A zone is empty when it does not contain any objects and has no permanents equipped to it

Feature: Section 3.2 - Arms Zone
    As a game engine
    I need to correctly model the arms zone rules
    So that equipment management in the arms zone works correctly

    # ===== Rule 3.2.1: Arms zone is a public equipment zone in the arena =====

    # Test for Rule 3.2.1 - Arms zone is a public zone
    Scenario: An arms zone is a public zone
        Given a player owns an arms zone
        When checking the visibility of the arms zone
        Then the arms zone is a public zone
        And the arms zone is not a private zone

    # Test for Rule 3.2.1 - Arms zone is an equipment zone
    Scenario: An arms zone is an equipment zone
        Given a player owns an arms zone
        When checking the zone type of the arms zone
        Then the arms zone is classified as an equipment zone

    # Test for Rule 3.2.1 - Arms zone is in the arena
    Scenario: An arms zone is in the arena
        Given a player owns an arms zone
        When checking if the arms zone is in the arena
        Then the arms zone is in the arena

    # Test for Rule 3.2.1 - Arms zone is owned by a player
    Scenario: An arms zone is owned by a specific player
        Given player 0 owns an arms zone
        When checking the owner of the arms zone
        Then the arms zone is owned by player 0

    # ===== Rule 3.2.2: Arms zone can contain up to one equipped object =====

    # Test for Rule 3.2.2 - Arms zone starts empty
    Scenario: An arms zone starts empty
        Given a player has an arms zone with no equipped cards
        When checking the contents of the arms zone
        Then the arms zone is empty
        And the empty arms zone is exposed

    # Test for Rule 3.2.2 - Arms zone can contain exactly one equipped object
    Scenario: An arms zone can contain exactly one equipped object
        Given a player has an arms zone with no equipped cards
        And a card with subtype arms is available
        When the arms card is equipped to the arms zone
        Then the arms zone contains exactly one equipped object
        And the arms zone is not empty

    # Test for Rule 3.2.2 - Arms zone cannot contain more than one object
    Scenario: An arms zone cannot contain more than one equipped object
        Given a player has an arms zone with one arms card already equipped
        And a second arms card is available
        When attempting to equip the second arms card to the arms zone
        Then the second equip attempt fails
        And the arms zone still contains only one equipped object

    # ===== Rule 3.2.2a: Only objects with subtype arms can be equipped to arms zone =====

    # Test for Rule 3.2.2a - Card with subtype arms can be equipped to arms zone
    Scenario: A card with subtype arms can be equipped to the arms zone
        Given a player has an empty arms zone
        And a card has subtype arms
        When the card is equipped to the arms zone
        Then the card is successfully equipped to the arms zone
        And the card is in the arms zone as a permanent

    # Test for Rule 3.2.2a - Card without subtype arms cannot be equipped to arms zone
    Scenario: A card without subtype arms cannot be equipped to the arms zone
        Given a player has an empty arms zone
        And a card does not have subtype arms
        When attempting to equip the non-arms card to the arms zone
        Then the non-arms equip attempt is rejected
        And the arms zone remains empty after non-arms rejection

    # Test for Rule 3.2.2a - Card with subtype chest is rejected from arms zone
    Scenario: A card with subtype chest cannot be equipped to the arms zone
        Given a player has an empty arms zone
        And a card has subtype chest but not subtype arms
        When attempting to equip the chest card to the arms zone
        Then the chest equip attempt is rejected
        And the arms zone remains empty after chest rejection

    # Test for Rule 3.2.2a - Modular card gains arms subtype when equipped to arms zone
    Scenario: An arms card equipped to arms zone is a permanent
        Given a player has an empty arms zone
        And an equipment card has subtype arms
        When the equipment card is equipped to the arms zone
        Then the equipped card is a permanent in the arms zone
        And the card has the arms subtype

    # ===== Rule 3.2.3: Player may equip arms card at start of game =====

    # Test for Rule 3.2.3 - Player may equip arms card at start of game
    Scenario: A player may equip an arms card to their arms zone at the start of the game
        Given a player has an arms card in their starting inventory
        When the start of game equip procedure runs with equipping
        Then the player may equip the arms card to their arms zone
        And the arms card is in the arms zone as a permanent after equipping

    # Test for Rule 3.2.3 - Player's arms zone is empty if they choose not to equip
    Scenario: A player's arms zone is empty if they choose not to equip at game start
        Given a player chooses not to equip any arms card at game start
        When the start of game equip procedure runs without equipping
        Then the player's arms zone is empty
        And the unequipped arms zone is exposed

    # ===== Cross-rule: Zone empty definition includes equipped permanents =====

    # Test for Rule 3.0.1a cross-ref - Arms zone is empty only if it has no objects and no equipped permanents
    Scenario: An arms zone is not empty when it has an equipped permanent
        Given a player has an arms zone with an arms card equipped
        When checking if the arms zone is empty
        Then the arms zone is not empty because it has an equipped permanent

    # Test for Rule 8.5.41c cross-ref - Arms zone must be empty before equipping
    Scenario: An arms card can only be equipped if the arms zone is empty
        Given a player has an arms zone with one arms card already equipped
        And the arms zone is therefore not empty
        When attempting to equip another arms card to the occupied zone
        Then the equip attempt fails because the zone is not empty
