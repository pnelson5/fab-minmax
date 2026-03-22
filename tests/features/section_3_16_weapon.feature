# Feature file for Section 3.16: Weapon
# Reference: Flesh and Blood Comprehensive Rules Section 3.16
#
# 3.16.1 A weapon zone is a public zone in the arena, owned by a player.
#
# 3.16.2 A weapon zone can only contain up to one object which is equipped to
#         that zone. [8.5.41]
#
# 3.16.2a An object can only be equipped to a weapon zone if it has the type
#          weapon or the subtype off-hand or quiver. An object with the subtype
#          2H must be equipped to two weapon zones. [8.2.2]
#
# 3.16.3 A player may equip a weapon card or an off-hand card to their weapon
#         zone at the start of the game. [4.1]
#
# Cross-references:
# - 3.0.4a: weapon zone is a public zone
# - 3.1.1: weapon zone is an arena zone
# - 8.5.41: Equip is a discrete effect; puts object into equipment zone as a permanent
# - 8.5.41c: Object can only be equipped to a zone if the zone is empty and it is
#            not already equipped to a zone of the same type
# - 3.0.1a: A zone is empty when it does not contain any objects and has no
#           permanents equipped to it
# - 8.2.2: 2H subtype requires two weapon zones

Feature: Section 3.16 - Weapon Zone
    As a game engine
    I need to correctly model the weapon zone rules
    So that equipment management in the weapon zone works correctly

    # ===== Rule 3.16.1: Weapon zone is a public zone in the arena =====

    # Test for Rule 3.16.1 - Weapon zone is a public zone
    Scenario: A weapon zone is a public zone
        Given a player owns a weapon zone
        When checking the visibility of the weapon zone
        Then the weapon zone is a public zone
        And the weapon zone is not a private zone

    # Test for Rule 3.16.1 - Weapon zone is an equipment zone
    Scenario: A weapon zone is an equipment zone
        Given a player owns a weapon zone
        When checking the zone type of the weapon zone
        Then the weapon zone is classified as an equipment zone

    # Test for Rule 3.16.1 - Weapon zone is in the arena
    Scenario: A weapon zone is in the arena
        Given a player owns a weapon zone
        When checking if the weapon zone is in the arena
        Then the weapon zone is in the arena

    # Test for Rule 3.16.1 - Weapon zone is owned by a player
    Scenario: A weapon zone is owned by a specific player
        Given player 0 owns a weapon zone
        When checking the owner of the weapon zone
        Then the weapon zone is owned by player 0

    # ===== Rule 3.16.2: Weapon zone can contain up to one equipped object =====

    # Test for Rule 3.16.2 - Weapon zone starts empty
    Scenario: A weapon zone starts empty
        Given a player has a weapon zone with no equipped cards
        When checking the contents of the weapon zone
        Then the weapon zone is empty
        And the empty weapon zone is exposed

    # Test for Rule 3.16.2 - Weapon zone can contain exactly one equipped object
    Scenario: A weapon zone can contain exactly one equipped object
        Given a player has a weapon zone with no equipped cards
        And a card with type weapon is available
        When the weapon card is equipped to the weapon zone
        Then the weapon zone contains exactly one equipped object
        And the weapon zone is not empty

    # Test for Rule 3.16.2 - Weapon zone cannot contain more than one object
    Scenario: A weapon zone cannot contain more than one equipped object
        Given a player has a weapon zone with one weapon card already equipped
        And a second weapon card is available
        When attempting to equip the second weapon card to the weapon zone
        Then the second weapon equip attempt fails
        And the weapon zone still contains only one equipped object

    # ===== Rule 3.16.2a: Objects that can be equipped to a weapon zone =====

    # Test for Rule 3.16.2a - Card with type weapon can be equipped
    Scenario: A card with type weapon can be equipped to the weapon zone
        Given a player has an empty weapon zone
        And a card has type weapon
        When the weapon-type card is equipped to the weapon zone
        Then the weapon-type card is successfully equipped to the weapon zone
        And the weapon-type card is in the weapon zone as a permanent

    # Test for Rule 3.16.2a - Card with subtype off-hand can be equipped
    Scenario: A card with subtype off-hand can be equipped to the weapon zone
        Given a player has an empty weapon zone
        And a card has subtype off-hand
        When the off-hand card is equipped to the weapon zone
        Then the off-hand card is successfully equipped to the weapon zone
        And the off-hand card is in the weapon zone as a permanent

    # Test for Rule 3.16.2a - Card with subtype quiver can be equipped
    Scenario: A card with subtype quiver can be equipped to the weapon zone
        Given a player has an empty weapon zone
        And a card has subtype quiver
        When the quiver card is equipped to the weapon zone
        Then the quiver card is successfully equipped to the weapon zone
        And the quiver card is in the weapon zone as a permanent

    # Test for Rule 3.16.2a - Card without weapon type or off-hand/quiver subtype cannot be equipped
    Scenario: A non-weapon card cannot be equipped to the weapon zone
        Given a player has an empty weapon zone
        And a card is neither a weapon type nor has subtype off-hand or quiver
        When attempting to equip the non-weapon card to the weapon zone
        Then the non-weapon equip attempt is rejected
        And the weapon zone remains empty after non-weapon rejection

    # Test for Rule 3.16.2a - 2H weapon requires two weapon zones
    Scenario: A card with subtype 2H must be equipped to two weapon zones
        Given a player has two empty weapon zones
        And a card has subtype 2H
        When the 2H weapon card is equipped
        Then the 2H weapon card occupies both weapon zones

    # Test for Rule 3.16.2a - 2H weapon cannot be equipped with only one zone
    Scenario: A card with subtype 2H cannot be equipped if only one weapon zone is available
        Given a player has only one empty weapon zone
        And a card has subtype 2H
        When attempting to equip the 2H card with only one weapon zone
        Then the 2H equip attempt fails due to insufficient weapon zones

    # ===== Rule 3.16.3: Player may equip weapon or off-hand card at game start =====

    # Test for Rule 3.16.3 - Player may equip a weapon card at start of game
    Scenario: A player may equip a weapon card to their weapon zone at the start of the game
        Given a player has a weapon card in their starting inventory
        When the start of game weapon equip procedure runs with equipping
        Then the player may equip the weapon card to their weapon zone
        And the weapon card is in the weapon zone as a permanent after equipping

    # Test for Rule 3.16.3 - Player may equip an off-hand card at start of game
    Scenario: A player may equip an off-hand card to their weapon zone at the start of the game
        Given a player has an off-hand card in their starting inventory
        When the start of game off-hand equip procedure runs
        Then the player may equip the off-hand card to their weapon zone
        And the off-hand card is in the weapon zone as a permanent after equipping

    # Test for Rule 3.16.3 - Player's weapon zone is empty if they choose not to equip
    Scenario: A player's weapon zone is empty if they choose not to equip at game start
        Given a player chooses not to equip any weapon at game start
        When the start of game weapon equip procedure runs without equipping
        Then the player's weapon zone is empty
        And the unequipped weapon zone is exposed

    # ===== Cross-rule: Zone empty definition includes equipped permanents =====

    # Test for Rule 3.0.1a cross-ref - Weapon zone is empty only if no objects and no permanents
    Scenario: A weapon zone is not empty when it has an equipped permanent
        Given a player has a weapon zone with a weapon card equipped
        When checking if the weapon zone is empty
        Then the weapon zone is not empty because it has an equipped permanent

    # Test for Rule 8.5.41c cross-ref - Weapon zone must be empty before equipping
    Scenario: A weapon card can only be equipped if the weapon zone is empty
        Given a player has a weapon zone with one weapon card already equipped
        And the weapon zone is therefore not empty
        When attempting to equip another weapon card to the occupied weapon zone
        Then the weapon equip attempt fails because the zone is not empty
