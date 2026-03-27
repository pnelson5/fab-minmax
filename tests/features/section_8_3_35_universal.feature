# Feature file for Section 8.3.35: Universal (Ability Keyword)
# Reference: Flesh and Blood Comprehensive Rules Section 8.3.35
#
# Rule 8.3.35: Universal is a while-static ability that means
# "While in any zone, it is the same class as your hero."
#
# Key aspects of Universal:
# - It is a WHILE-STATIC ability (applies conditionally while object exists in any zone)
# - A Universal card has the same class supertype as the controlling player's hero
# - The class matching applies in ANY zone (hand, deck, banished, graveyard, arena, etc.)
# - Universal allows cross-class usage: the card always matches the hero's class
# - The class is dynamic: if the hero's class changes, the Universal card's class changes
# - A card without Universal does not receive this class-matching behavior

Feature: Section 8.3.35 - Universal Ability Keyword
    As a game engine
    I need to correctly implement the Universal ability keyword
    So that cards with Universal are treated as the same class as the player's hero in any zone

    # Rule 8.3.35: Universal is recognized as an ability keyword
    Scenario: Universal is recognized as an ability keyword
        Given a card with the Universal keyword
        When I inspect the card's keywords
        Then the card has the Universal keyword

    # Rule 8.3.35: Universal is a while-static ability
    Scenario: Universal is a while-static ability
        Given a card with the Universal keyword
        When I check the ability type of Universal
        Then Universal is a while-static ability

    # Rule 8.3.35: Universal ability meaning matches comprehensive rules text
    Scenario: Universal ability meaning matches comprehensive rules text
        Given a card with the Universal keyword
        When I inspect the Universal ability's meaning
        Then the Universal meaning is "While in any zone, it is the same class as your hero"

    # Rule 8.3.35: Universal card has the same class as the hero while in hand
    Scenario: Universal card has the same class as the hero while in hand
        Given a player whose hero is a Guardian hero
        And a card with the Universal keyword in the player's hand
        When I check the card's class in hand
        Then the card is considered Guardian class in hand

    # Rule 8.3.35: Universal card has the same class as the hero while in any zone
    Scenario: Universal card has the same class as the hero while in the banished zone
        Given a player whose hero is a Warrior hero
        And a card with the Universal keyword in the player's banished zone
        When I check the card's class in the banished zone
        Then the card is considered Warrior class in the banished zone

    # Rule 8.3.35: Universal card has the same class as the hero while in the deck
    Scenario: Universal card has the same class as the hero while in the deck
        Given a player whose hero is a Ninja hero
        And a Universal card tracked as being in the deck zone
        When I check the card's class in the deck
        Then the card is considered Ninja class in the deck

    # Rule 8.3.35: Universal card class changes dynamically with the hero's class
    Scenario: Universal card class changes when the hero's class changes
        Given a player whose hero is a Brute hero
        And a card with the Universal keyword in the player's hand
        When the hero's class changes to Wizard
        And I check the card's class
        Then the card is considered Wizard class

    # Rule 8.3.35: Card without Universal does not inherit hero class
    Scenario: Card without Universal does not have the hero's class
        Given a player whose hero is a Guardian hero
        And a card without the Universal keyword in the player's hand
        When I check the non-Universal card's class
        Then the card does not have the Guardian class from Universal

    # Rule 8.3.35: Universal applies while in any zone - it is not limited to specific zones
    Scenario: Universal applies in the graveyard zone
        Given a player whose hero is a Ranger hero
        And a card with the Universal keyword in the player's graveyard
        When I check the card's class in the graveyard
        Then the card is considered Ranger class in the graveyard
