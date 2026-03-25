# Feature file for Section 8.3.27: Rune Gate (Ability Keyword)
# Reference: Flesh and Blood Comprehensive Rules Section 8.3.27
#
# Rule 8.3.27: Rune Gate is a play-static ability that means "If you control
# Runechants equal to or greater than this's {r} cost, you may play it from
# your banished zone without paying its {r} cost."
#
# Rule 8.3.27a: If a player plays a card from their banished zone using rune
# gate, they are considered to have rune gated, and the card is considered to
# be rune gated.
#
# Key aspects of Rune Gate:
# - It is a PLAY-STATIC ability (not triggered, not activated)
# - Requires controlling Runechants >= this card's {r} cost
# - Allows playing the card from the banished zone (not hand/deck)
# - The card is played WITHOUT paying its {r} cost when rune gate is used
# - The player and card are both marked as "rune gated" after use (Rule 8.3.27a)

Feature: Section 8.3.27 - Rune Gate Ability Keyword
    As a game engine
    I need to correctly implement the Rune Gate ability keyword
    So that cards with Rune Gate can be played from the banished zone when enough Runechants are controlled

    # Rule 8.3.27: Rune Gate is recognized as a keyword
    Scenario: Rune Gate is recognized as an ability keyword
        Given a card with the Rune Gate keyword
        When I inspect the card's keywords
        Then the card has the Rune Gate keyword

    # Rule 8.3.27: Rune Gate is a play-static ability
    Scenario: Rune Gate is a play-static ability
        Given a card with the Rune Gate keyword
        When I check the ability type of Rune Gate
        Then Rune Gate is a play-static ability

    # Rule 8.3.27: Can play from banished zone when Runechants >= cost
    Scenario: Card with Rune Gate can be played from banished zone when Runechants meet the cost
        Given a card with the Rune Gate keyword with a Runechant cost of 3
        And the card is in the player's banished zone
        And the player controls 3 Runechants
        When the player attempts to play the card using Rune Gate
        Then the Rune Gate play attempt succeeds

    # Rule 8.3.27: Can play when Runechants exceed cost
    Scenario: Card with Rune Gate can be played when Runechants exceed the required cost
        Given a card with the Rune Gate keyword with a Runechant cost of 2
        And the card is in the player's banished zone
        And the player controls 5 Runechants
        When the player attempts to play the card using Rune Gate
        Then the Rune Gate play attempt succeeds

    # Rule 8.3.27: Cannot play via rune gate when Runechants < cost
    Scenario: Card with Rune Gate cannot be played via rune gate when Runechants are insufficient
        Given a card with the Rune Gate keyword with a Runechant cost of 4
        And the card is in the player's banished zone
        And the player controls 2 Runechants
        When the player attempts to play the card using Rune Gate
        Then the Rune Gate play attempt fails

    # Rule 8.3.27: Cannot use rune gate with zero Runechants when cost > 0
    Scenario: Card with Rune Gate cannot be played when player controls no Runechants
        Given a card with the Rune Gate keyword with a Runechant cost of 1
        And the card is in the player's banished zone
        And the player controls 0 Runechants
        When the player attempts to play the card using Rune Gate
        Then the Rune Gate play attempt fails

    # Rule 8.3.27: Rune Gate does not apply to cards in zones other than banished
    Scenario: Rune Gate only enables playing from the banished zone
        Given a card with the Rune Gate keyword with a Runechant cost of 2
        And the card is in the player's hand
        And the player controls 3 Runechants
        When the player attempts to play the card using Rune Gate
        Then the Rune Gate play attempt fails

    # Rule 8.3.27a: Player is considered to have rune gated after using Rune Gate
    Scenario: Player is marked as rune gated when playing via Rune Gate
        Given a card with the Rune Gate keyword with a Runechant cost of 2
        And the card is in the player's banished zone
        And the player controls 3 Runechants
        When the player plays the card from the banished zone using Rune Gate
        Then the player is considered to have rune gated

    # Rule 8.3.27a: Card is considered rune gated after being played via Rune Gate
    Scenario: Card is marked as rune gated when played via Rune Gate
        Given a card with the Rune Gate keyword with a Runechant cost of 2
        And the card is in the player's banished zone
        And the player controls 3 Runechants
        When the player plays the card from the banished zone using Rune Gate
        Then the card is considered to be rune gated
