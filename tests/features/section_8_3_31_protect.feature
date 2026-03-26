# Feature file for Section 8.3.31: Protect (Ability Keyword)
# Reference: Flesh and Blood Comprehensive Rules Section 8.3.31
#
# Rule 8.3.31: Protect is a static ability that means "You may defend any hero
# attacked by an opponent with this."
#
# Rule 8.3.31a: If a player defends with a card with protect, they and the card
# are considered to have protected.
#
# Key aspects of Protect:
# - It is a STATIC ability
# - Allows defending ANY hero attacked by an opponent (cross-player defending)
# - Normally, players can only defend attacks targeting their own hero
# - When used: the defending player is considered to have "protected"
# - When used: the defending card is considered to have "protected"
#
# Context (Rule 7.3.2e):
# "If a player's hero is attacked, that player declares any defending cards first,
#  then in clockwise order, players may declare additional defending cards, such as
#  cards with Protect."

Feature: Section 8.3.31 - Protect Ability Keyword
    As a game engine
    I need to correctly implement the Protect ability keyword
    So that players can defend any hero attacked by an opponent using Protect cards

    # Rule 8.3.31: Protect is recognized as a keyword
    Scenario: Protect is recognized as an ability keyword
        Given a card with the Protect keyword
        When I inspect the card's keywords
        Then the card has the Protect keyword

    # Rule 8.3.31: Protect is a static ability
    Scenario: Protect is a static ability
        Given a card with the Protect keyword
        When I check the ability type of Protect
        Then Protect is a static ability

    # Rule 8.3.31: Protect ability meaning matches comprehensive rules text
    Scenario: Protect ability meaning matches comprehensive rules text
        Given a card with the Protect keyword
        When I check the meaning of the Protect ability
        Then the Protect meaning is "You may defend any hero attacked by an opponent with this."

    # Rule 8.3.31: A player may use a Protect card to defend any hero attacked by an opponent
    Scenario: A player may defend a hero other than their own using a Protect card
        Given a multiplayer game with two heroes
        And player two's hero is being attacked by an opponent
        And player one has a card with the Protect keyword
        When player one defends player two's hero with the Protect card
        Then the defense is allowed

    # Rule 8.3.31: Without Protect a player cannot defend another hero's attack
    Scenario: A player cannot defend another hero without Protect
        Given a multiplayer game with two heroes
        And player two's hero is being attacked by an opponent
        And player one has a card without the Protect keyword
        When player one attempts to defend player two's hero with the non-Protect card
        Then the defense is not allowed

    # Rule 8.3.31a: The defending player is considered to have protected
    Scenario: The defending player is considered to have protected when defending with a Protect card
        Given a multiplayer game with two heroes
        And player two's hero is being attacked by an opponent
        And player one has a card with the Protect keyword
        When player one defends player two's hero with the Protect card
        Then player one is considered to have protected

    # Rule 8.3.31a: The defending card is considered to have protected
    Scenario: The defending card is considered to have protected when used to defend
        Given a multiplayer game with two heroes
        And player two's hero is being attacked by an opponent
        And player one has a card with the Protect keyword
        When player one defends player two's hero with the Protect card
        Then the Protect card is considered to have protected

    # Rule 8.3.31: Protect only works against attacks on heroes by opponents
    Scenario: Protect allows defending any hero attacked by an opponent
        Given a multiplayer game with two heroes
        And player two's hero is being attacked by an opponent
        And player one has a card with the Protect keyword
        When player one defends player two's hero with the Protect card
        Then the defense is allowed
        And player one is considered to have protected
        And the Protect card is considered to have protected
