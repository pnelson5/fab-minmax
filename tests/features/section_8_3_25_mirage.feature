# Feature file for Section 8.3.25: Mirage (Ability Keyword)
# Reference: Flesh and Blood Comprehensive Rules Section 8.3.25
#
# Rule 8.3.25: Mirage is a triggered-static ability that means
# "When this is defending a non-Illusionist attack with 6 or more {p}, destroy this."
#
# Key aspects of Mirage:
# - It is a triggered-static ability (triggers during defense)
# - It only triggers when defending a NON-Illusionist attack
# - The triggering condition is the attacking card having 6 or more power
# - The effect is the Mirage card being destroyed
# - Illusionist attacks do NOT trigger Mirage (Illusionist exception)

Feature: Section 8.3.25 - Mirage Ability Keyword
    As a game engine
    I need to correctly implement the Mirage ability keyword
    So that cards with Mirage are destroyed when defending powerful non-Illusionist attacks

    # Rule 8.3.25: Mirage is recognized as a keyword
    Scenario: Mirage is recognized as an ability keyword
        Given a card with the Mirage keyword
        When I inspect the card's keywords
        Then the card has the Mirage keyword

    # Rule 8.3.25: Mirage triggers when defending a non-Illusionist attack with 6+ power
    Scenario: Mirage card is destroyed when defending a non-Illusionist attack with exactly 6 power
        Given a card with the Mirage keyword
        And a non-Illusionist attack with power 6
        When the Mirage card defends the attack
        Then the Mirage card is destroyed

    # Rule 8.3.25: Mirage triggers for any non-Illusionist attack with 6 or more power
    Scenario: Mirage card is destroyed when defending a non-Illusionist attack with more than 6 power
        Given a card with the Mirage keyword
        And a non-Illusionist attack with power 10
        When the Mirage card defends the attack
        Then the Mirage card is destroyed

    # Rule 8.3.25: Mirage does NOT trigger for non-Illusionist attacks with less than 6 power
    Scenario: Mirage card is not destroyed when defending a non-Illusionist attack with 5 power
        Given a card with the Mirage keyword
        And a non-Illusionist attack with power 5
        When the Mirage card defends the attack
        Then the Mirage card is not destroyed

    # Rule 8.3.25: Mirage does NOT trigger for attacks with 0 power
    Scenario: Mirage card is not destroyed when defending a non-Illusionist attack with 0 power
        Given a card with the Mirage keyword
        And a non-Illusionist attack with power 0
        When the Mirage card defends the attack
        Then the Mirage card is not destroyed

    # Rule 8.3.25: Mirage does NOT trigger when defending an Illusionist attack
    Scenario: Mirage card is not destroyed when defending an Illusionist attack with 6 power
        Given a card with the Mirage keyword
        And an Illusionist attack with power 6
        When the Mirage card defends the attack
        Then the Mirage card is not destroyed

    # Rule 8.3.25: Illusionist attacks with high power still do not trigger Mirage
    Scenario: Mirage card is not destroyed when defending an Illusionist attack with 10 power
        Given a card with the Mirage keyword
        And an Illusionist attack with power 10
        When the Mirage card defends the attack
        Then the Mirage card is not destroyed

    # Rule 8.3.25: Card without Mirage is not destroyed when defending
    Scenario: A card without Mirage is not destroyed when defending a powerful non-Illusionist attack
        Given a card without the Mirage keyword
        And a non-Illusionist attack with power 8
        When the non-Mirage card defends the attack
        Then the defending card is not destroyed

    # Rule 8.3.25: Mirage is a triggered-static ability type
    Scenario: Mirage is a triggered-static ability
        Given a card with the Mirage keyword
        When I check the ability type of Mirage
        Then Mirage is a triggered-static ability
