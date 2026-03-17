# Feature file for Section 3.5: Chest
# Reference: Flesh and Blood Comprehensive Rules Section 3.5
#
# 3.5.1 A chest zone is a public equipment zone in the arena, owned by a player.
#
# 3.5.2 A chest zone can only contain up to one object which is equipped to that
#        zone. [8.5.41]
#
# 3.5.2a An object can only be equipped to a chest zone if it has subtype chest.
#
# 3.5.3 A player may equip a chest card to their chest zone at the start of the game. [4.1]
#
# Cross-references:
# - 3.0.4a: chest zone is a public zone
# - 3.1.1: chest zone is an arena zone
# - 8.5.41: Equip is a discrete effect; puts object into equipment zone as a permanent
# - 8.5.41b: Object can only be equipped if it has one of: 1H, 2H, Arms, Chest, Head, Legs, Off-Hand, or Quiver
# - 8.5.41c: Object can only be equipped to a zone if the zone is empty and it is not already equipped to a zone of the same type
# - 3.0.1a: A zone is empty when it does not contain any objects and has no permanents equipped to it

Feature: Section 3.5 - Chest Zone
    As a game engine
    I need to correctly model the chest zone rules
    So that equipment management in the chest zone works correctly

    # ===== Rule 3.5.1: Chest zone is a public equipment zone in the arena =====

    # Test for Rule 3.5.1 - Chest zone is a public zone
    Scenario: A chest zone is a public zone
        Given a player owns a chest zone
        When checking the visibility of the chest zone
        Then the chest zone is a public zone
        And the chest zone is not a private zone

    # Test for Rule 3.5.1 - Chest zone is an equipment zone
    Scenario: A chest zone is an equipment zone
        Given a player owns a chest zone
        When checking the zone type of the chest zone
        Then the chest zone is classified as an equipment zone

    # Test for Rule 3.5.1 - Chest zone is in the arena
    Scenario: A chest zone is in the arena
        Given a player owns a chest zone
        When checking if the chest zone is in the arena
        Then the chest zone is in the arena

    # Test for Rule 3.5.1 - Chest zone is owned by a player
    Scenario: A chest zone is owned by a specific player
        Given player 0 owns a chest zone
        When checking the owner of the chest zone
        Then the chest zone is owned by player 0

    # ===== Rule 3.5.2: Chest zone can contain up to one equipped object =====

    # Test for Rule 3.5.2 - Chest zone starts empty
    Scenario: A chest zone starts empty
        Given a player has a chest zone with no equipped cards
        When checking the contents of the chest zone
        Then the chest zone is empty
        And the empty chest zone is exposed

    # Test for Rule 3.5.2 - Chest zone can contain exactly one equipped object
    Scenario: A chest zone can contain exactly one equipped object
        Given a player has a chest zone with no equipped cards
        And a card with subtype chest is available
        When the chest card is equipped to the chest zone
        Then the chest zone contains exactly one equipped object
        And the chest zone is not empty

    # Test for Rule 3.5.2 - Chest zone cannot contain more than one object
    Scenario: A chest zone cannot contain more than one equipped object
        Given a player has a chest zone with one chest card already equipped
        And a second chest card is available
        When attempting to equip the second chest card to the chest zone
        Then the second chest equip attempt fails
        And the chest zone still contains only one equipped object

    # ===== Rule 3.5.2a: Only objects with subtype chest can be equipped to chest zone =====

    # Test for Rule 3.5.2a - Card with subtype chest can be equipped to chest zone
    Scenario: A card with subtype chest can be equipped to the chest zone
        Given a player has an empty chest zone
        And a card has subtype chest
        When the card is equipped to the chest zone
        Then the card is successfully equipped to the chest zone
        And the card is in the chest zone as a permanent

    # Test for Rule 3.5.2a - Card without subtype chest cannot be equipped to chest zone
    Scenario: A card without subtype chest cannot be equipped to the chest zone
        Given a player has an empty chest zone
        And a card does not have subtype chest
        When attempting to equip the non-chest card to the chest zone
        Then the non-chest equip attempt is rejected
        And the chest zone remains empty after non-chest rejection

    # Test for Rule 3.5.2a - Card with subtype arms is rejected from chest zone
    Scenario: A card with subtype arms cannot be equipped to the chest zone
        Given a player has an empty chest zone
        And a card has subtype arms but not subtype chest
        When attempting to equip the arms card to the chest zone
        Then the arms equip attempt into chest zone is rejected
        And the chest zone remains empty after arms rejection

    # Test for Rule 3.5.2a - Chest card equipped to chest zone is permanent
    Scenario: A chest card equipped to chest zone is a permanent
        Given a player has an empty chest zone
        And an equipment card has subtype chest
        When the equipment card is equipped to the chest zone
        Then the equipped card is a permanent in the chest zone
        And the card has the chest subtype

    # ===== Rule 3.5.3: Player may equip chest card at start of game =====

    # Test for Rule 3.5.3 - Player may equip chest card at start of game
    Scenario: A player may equip a chest card to their chest zone at the start of the game
        Given a player has a chest card in their starting inventory
        When the start of game chest equip procedure runs with equipping
        Then the player may equip the chest card to their chest zone
        And the chest card is in the chest zone as a permanent after equipping

    # Test for Rule 3.5.3 - Player's chest zone is empty if they choose not to equip
    Scenario: A player's chest zone is empty if they choose not to equip at game start
        Given a player chooses not to equip any chest card at game start
        When the start of game chest equip procedure runs without equipping
        Then the player's chest zone is empty
        And the unequipped chest zone is exposed

    # ===== Cross-rule: Zone empty definition includes equipped permanents =====

    # Test for Rule 3.0.1a cross-ref - Chest zone is empty only if it has no objects and no equipped permanents
    Scenario: A chest zone is not empty when it has an equipped permanent
        Given a player has a chest zone with a chest card equipped
        When checking if the chest zone is empty
        Then the chest zone is not empty because it has an equipped permanent

    # Test for Rule 8.5.41c cross-ref - Chest zone must be empty before equipping
    Scenario: A chest card can only be equipped if the chest zone is empty
        Given a player has a chest zone with one chest card already equipped
        And the chest zone is therefore not empty
        When attempting to equip another chest card to the occupied chest zone
        Then the chest equip attempt fails because the zone is not empty
