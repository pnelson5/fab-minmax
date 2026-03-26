# Feature file for Section 8.3.30: Modular (Ability Keyword)
# Reference: Flesh and Blood Comprehensive Rules Section 8.3.30
#
# Rule 8.3.30: Modular is a static ability that means "This may be equipped to any of
# your equipment zones. It has the subtype of the zone it's equipped to."
#
# Rule 8.3.30a: The equipment zones are Arms, Chest, Head, and Legs.
#
# Rule 8.3.30b: A card can only be equipped to its owner's equipment zones with Modular.
#
# Rule 8.3.30c: A card with modular does not have any of the equipment subtypes until
# it is equipped to a zone.
#
# Key aspects of Modular:
# - It is a STATIC ability
# - Allows an equipment to be placed in any equipment zone (Arms, Chest, Head, Legs)
# - The card gains the subtype of the zone it is equipped to
# - Only the owner's equipment zones may be used
# - No equipment subtypes are granted until the card is equipped

Feature: Section 8.3.30 - Modular Ability Keyword
    As a game engine
    I need to correctly implement the Modular ability keyword
    So that equipment with Modular can be equipped to any equipment zone and gains the zone's subtype

    # Rule 8.3.30: Modular is recognized as a keyword
    Scenario: Modular is recognized as an ability keyword
        Given a card with the Modular keyword
        When I inspect the card's keywords
        Then the card has the Modular keyword

    # Rule 8.3.30: Modular is a static ability
    Scenario: Modular is a static ability
        Given a card with the Modular keyword
        When I check the ability type of Modular
        Then Modular is a static ability

    # Rule 8.3.30c: Card with Modular has no equipment subtypes before being equipped
    Scenario: Card with Modular has no equipment subtypes before being equipped
        Given a card with the Modular keyword
        When I check the card's subtypes before equipping
        Then the card has no equipment subtypes

    # Rule 8.3.30 + 8.3.30a: Card with Modular can be equipped to Arms zone
    Scenario: Card with Modular can be equipped to the Arms zone
        Given a card with the Modular keyword
        When the card is equipped to the Arms zone
        Then the card is successfully equipped

    # Rule 8.3.30 + 8.3.30a: Card with Modular can be equipped to Chest zone
    Scenario: Card with Modular can be equipped to the Chest zone
        Given a card with the Modular keyword
        When the card is equipped to the Chest zone
        Then the card is successfully equipped

    # Rule 8.3.30 + 8.3.30a: Card with Modular can be equipped to Head zone
    Scenario: Card with Modular can be equipped to the Head zone
        Given a card with the Modular keyword
        When the card is equipped to the Head zone
        Then the card is successfully equipped

    # Rule 8.3.30 + 8.3.30a: Card with Modular can be equipped to Legs zone
    Scenario: Card with Modular can be equipped to the Legs zone
        Given a card with the Modular keyword
        When the card is equipped to the Legs zone
        Then the card is successfully equipped

    # Rule 8.3.30: Card gains subtype of the zone it is equipped to (Arms)
    Scenario: Card with Modular gains Arms subtype when equipped to Arms zone
        Given a card with the Modular keyword
        When the card is equipped to the Arms zone
        Then the card has the Arms subtype

    # Rule 8.3.30: Card gains subtype of the zone it is equipped to (Chest)
    Scenario: Card with Modular gains Chest subtype when equipped to Chest zone
        Given a card with the Modular keyword
        When the card is equipped to the Chest zone
        Then the card has the Chest subtype

    # Rule 8.3.30b: Card with Modular can only be equipped to owner's equipment zones
    Scenario: Card with Modular can only be equipped to owner's equipment zones
        Given a card with the Modular keyword
        And the card belongs to player one
        When player two attempts to equip the card
        Then the equipment attempt fails

    # Rule 8.3.30: Modular ability meaning matches comprehensive rules text
    Scenario: Modular ability meaning matches comprehensive rules text
        Given a card with the Modular keyword
        When I check the meaning of the Modular ability
        Then the Modular meaning is "This may be equipped to any of your equipment zones. It has the subtype of the zone it's equipped to."
