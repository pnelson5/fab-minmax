# Feature file for Section 8.3.28: Ambush (Ability Keyword)
# Reference: Flesh and Blood Comprehensive Rules Section 8.3.28
#
# Rule 8.3.28: Ambush is a while-static ability that means "While this is in
# your arsenal, you may defend with it."
#
# Key aspects of Ambush:
# - It is a WHILE-STATIC ability (applies only while in a specific zone)
# - The condition is: "while this is in your arsenal"
# - The effect is: you may defend with the card from the arsenal
# - Without Ambush, cards in the arsenal cannot normally be used to defend
# - The ability is inactive when the card is in any zone other than the arsenal

Feature: Section 8.3.28 - Ambush Ability Keyword
    As a game engine
    I need to correctly implement the Ambush ability keyword
    So that cards with Ambush can defend while in the arsenal

    # Rule 8.3.28: Ambush is recognized as a keyword
    Scenario: Ambush is recognized as an ability keyword
        Given a card with the Ambush keyword
        When I inspect the card's keywords
        Then the card has the Ambush keyword

    # Rule 8.3.28: Ambush is a while-static ability
    Scenario: Ambush is a while-static ability
        Given a card with the Ambush keyword
        When I check the ability type of Ambush
        Then Ambush is a while-static ability

    # Rule 8.3.28: A card with Ambush in the arsenal can defend
    Scenario: Card with Ambush in the arsenal can be used to defend
        Given a card with the Ambush keyword
        And the card is in the player's arsenal
        And there is an active attack
        When the player attempts to defend with the Ambush card from the arsenal
        Then the defend attempt succeeds

    # Rule 8.3.28: Only while in the arsenal
    Scenario: Card with Ambush in hand cannot use Ambush ability to defend
        Given a card with the Ambush keyword
        And the card is in the player's hand
        And there is an active attack
        When the player attempts to defend with the Ambush card from the hand
        Then the defend from hand succeeds normally

    # Rule 8.3.28: Without Ambush, arsenal cards cannot defend
    Scenario: Card without Ambush in the arsenal cannot be used to defend
        Given a card without the Ambush keyword
        And the card is in the player's arsenal
        And there is an active attack
        When the player attempts to defend with the non-Ambush arsenal card
        Then the defend attempt from arsenal is blocked

    # Rule 8.3.28: Ambush while-static condition requires arsenal zone
    Scenario: Card with Ambush in the banished zone cannot use Ambush ability
        Given a card with the Ambush keyword
        And the card is in the player's banished zone
        And there is an active attack
        When the player attempts to defend with the Ambush card from the banished zone
        Then the defend attempt from banished is blocked

    # Rule 8.3.28: Ambush means while-static applies only in own arsenal
    Scenario: Ambush while-static ability is only active while in the arsenal
        Given a card with the Ambush keyword
        And the card is in the player's arsenal
        When I check whether Ambush is active
        Then Ambush is active because the card is in the arsenal

    # Rule 8.3.28: Ambush ability becomes inactive outside the arsenal
    Scenario: Ambush while-static ability is inactive when card is not in the arsenal
        Given a card with the Ambush keyword
        And the card is in the player's hand
        When I check whether Ambush is active
        Then Ambush is inactive because the card is not in the arsenal

    # Rule 8.3.28: Ambush full rule meaning text
    Scenario: Ambush ability meaning matches comprehensive rules text
        Given a card with the Ambush keyword
        When I check the meaning of the Ambush ability
        Then the Ambush meaning is "While this is in your arsenal, you may defend with it"
