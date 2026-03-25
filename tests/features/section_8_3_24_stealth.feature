# Feature file for Section 8.3.24: Stealth (Ability Keyword)
# Reference: Flesh and Blood Comprehensive Rules Section 8.3.24
#
# Rule 8.3.24: Stealth is an ability that means nothing.
#
# Stealth is a pure label/marker keyword with no inherent mechanical effect.
# It exists solely so that other cards and effects can reference it
# (e.g., "target attacking card with stealth").

Feature: Section 8.3.24 - Stealth Ability Keyword
    As a game engine
    I need to correctly implement the Stealth ability keyword
    So that cards can be labeled with stealth and referenced by other effects

    # Rule 8.3.24: Stealth is an ability
    Scenario: Stealth is recognized as an ability keyword
        Given a card with the Stealth keyword
        When I inspect the card's keywords
        Then the card has the Stealth keyword

    # Rule 8.3.24: Stealth means nothing — it has no inherent mechanical effect
    Scenario: Stealth does not grant any power bonus
        Given an attack card with the Stealth keyword
        And the base power of the attack is 4
        When the attack is played normally
        Then the attack power is 4

    # Rule 8.3.24: Stealth means nothing — no defense modifications
    Scenario: Stealth does not grant any defense bonus
        Given a card with the Stealth keyword
        And the base defense of the card is 3
        When I check the card's defense value
        Then the defense value is 3

    # Rule 8.3.24: A card without stealth is distinguishable from one with stealth
    Scenario: Card without Stealth keyword does not have Stealth
        Given a card without the Stealth keyword
        When I inspect the card's keywords
        Then the card does not have the Stealth keyword

    # Rule 8.3.24: Stealth does not alter how a card is played
    Scenario: A card with Stealth can be played normally
        Given an attack card with the Stealth keyword
        When the card is played as an attack
        Then the card is on the combat chain

    # Rule 8.3.24: Stealth is queryable by other effects
    Scenario: Other effects can query whether a card has Stealth
        Given an attacking card with the Stealth keyword
        When another effect checks if the attacker has Stealth
        Then the stealth check returns true

    # Rule 8.3.24: A card without Stealth fails a stealth check
    Scenario: Stealth check returns false for card without Stealth
        Given an attacking card without the Stealth keyword
        When another effect checks if the attacker has Stealth
        Then the stealth check returns false
