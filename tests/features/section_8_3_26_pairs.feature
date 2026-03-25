# Feature file for Section 8.3.26: Pairs (Ability Keyword)
# Reference: Flesh and Blood Comprehensive Rules Section 8.3.26
#
# Rule 8.3.26: Pairs is a static ability that means "Equip this only with an
# OBJECT.", where OBJECT is 1 or more object identities.
#
# Rule 8.3.26a: A card with pairs can only be equipped to a zone owned by a
# player if the player already has an OBJECT equipped, or if an OBJECT is
# being equipped as part of the same event.
#
# Key aspects of Pairs:
# - It is a STATIC ability (not triggered, not activated)
# - It restricts when equipment can be equipped (requires a companion OBJECT)
# - The player must ALREADY have the OBJECT equipped, OR
# - The OBJECT must be equipped as part of the SAME EVENT (simultaneous equip)
# - Without the required OBJECT, equipping is not legal

Feature: Section 8.3.26 - Pairs Ability Keyword
    As a game engine
    I need to correctly implement the Pairs ability keyword
    So that equipment with Pairs can only be equipped alongside the required companion object

    # Rule 8.3.26: Pairs is recognized as a keyword
    Scenario: Pairs is recognized as an ability keyword
        Given a card with the Pairs keyword
        When I inspect the card's keywords
        Then the card has the Pairs keyword

    # Rule 8.3.26: Pairs is a static ability
    Scenario: Pairs is a static ability
        Given a card with the Pairs keyword
        When I check the ability type of Pairs
        Then Pairs is a static ability

    # Rule 8.3.26a: Can equip when required OBJECT is already equipped
    Scenario: Card with Pairs can be equipped when required object is already equipped
        Given a card with the Pairs keyword pairing with "Twinblade Left"
        And the player already has "Twinblade Left" equipped
        When the player attempts to equip the Pairs card
        Then the equip attempt succeeds

    # Rule 8.3.26a: Cannot equip when required OBJECT is not present
    Scenario: Card with Pairs cannot be equipped when required object is not equipped
        Given a card with the Pairs keyword pairing with "Twinblade Left"
        And the player does not have "Twinblade Left" equipped
        When the player attempts to equip the Pairs card
        Then the equip attempt fails

    # Rule 8.3.26a: Can equip simultaneously with the required OBJECT (same event)
    Scenario: Card with Pairs can be equipped simultaneously with required object
        Given a card with the Pairs keyword pairing with "Twinblade Left"
        And the player does not have "Twinblade Left" equipped
        When the player equips both the Pairs card and "Twinblade Left" as part of the same event
        Then the equip attempt succeeds

    # Rule 8.3.26a: Card without Pairs is not restricted
    Scenario: A card without Pairs can be equipped freely
        Given a card without the Pairs keyword
        And the player does not have any companion equipped
        When the player attempts to equip the card
        Then the equip attempt succeeds

    # Rule 8.3.26: Pairs restriction is specific to the named OBJECT
    Scenario: Card with Pairs is blocked by missing the specific named object
        Given a card with the Pairs keyword pairing with "Twinblade Left"
        And the player has a different equipment "Other Weapon" equipped
        When the player attempts to equip the Pairs card
        Then the equip attempt fails

    # Rule 8.3.26: Pairs correctly allows equip when exact required object is present
    Scenario: Pairs restriction is satisfied only by the correct named object
        Given a card with the Pairs keyword pairing with "Twinblade Left"
        And the player already has "Twinblade Left" equipped
        And the player also has "Other Weapon" equipped
        When the player attempts to equip the Pairs card
        Then the equip attempt succeeds
