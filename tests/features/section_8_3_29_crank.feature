# Feature file for Section 8.3.29: Crank (Ability Keyword)
# Reference: Flesh and Blood Comprehensive Rules Section 8.3.29
#
# Rule 8.3.29: Crank is a static ability that means "As this enters the arena,
# you may remove a steam counter from it. If you do, gain an action point."
#
# Rule 8.3.29a: If a player removes a steam counter using crank, they are
# considered to have cranked, and the card is considered to be cranked.
#
# Key aspects of Crank:
# - It is a STATIC ability
# - Triggers as the card enters the arena
# - Requires the card to have a steam counter on it
# - Removing the steam counter is optional ("you may")
# - Removing a steam counter grants 1 action point
# - The player is "considered to have cranked" if they do so
# - The card is "considered to be cranked" if its steam counter was removed

Feature: Section 8.3.29 - Crank Ability Keyword
    As a game engine
    I need to correctly implement the Crank ability keyword
    So that cards with Crank grant an action point when entering the arena with a steam counter

    # Rule 8.3.29: Crank is recognized as a keyword
    Scenario: Crank is recognized as an ability keyword
        Given a card with the Crank keyword
        When I inspect the card's keywords
        Then the card has the Crank keyword

    # Rule 8.3.29: Crank is a static ability
    Scenario: Crank is a static ability
        Given a card with the Crank keyword
        When I check the ability type of Crank
        Then Crank is a static ability

    # Rule 8.3.29: When a card with Crank and a steam counter enters the arena, the player may remove the steam counter
    Scenario: Card with Crank and a steam counter entering arena allows removing the steam counter
        Given a card with the Crank keyword
        And the card has a steam counter on it
        When the card enters the arena
        Then the player may remove a steam counter from the card using Crank

    # Rule 8.3.29: Removing the steam counter via Crank grants an action point
    Scenario: Removing steam counter via Crank grants an action point
        Given a card with the Crank keyword
        And the card has a steam counter on it
        And the player has 1 action point
        When the card enters the arena and the player uses Crank
        Then the player gains 1 action point
        And the player now has 2 action points

    # Rule 8.3.29: Crank is optional - the player may choose not to use it
    Scenario: Player may choose not to use Crank when card enters the arena
        Given a card with the Crank keyword
        And the card has a steam counter on it
        And the player has 1 action point
        When the card enters the arena and the player declines to use Crank
        Then the player does not gain an action point from Crank
        And the player still has 1 action point

    # Rule 8.3.29: Crank cannot be used if no steam counter is on the card
    Scenario: Crank cannot be used when the card has no steam counter
        Given a card with the Crank keyword
        And the card has no steam counter on it
        When the card enters the arena
        Then Crank cannot grant an action point

    # Rule 8.3.29a: Player is considered to have cranked after using Crank
    Scenario: Player is considered to have cranked after using Crank
        Given a card with the Crank keyword
        And the card has a steam counter on it
        When the card enters the arena and the player uses Crank
        Then the player is considered to have cranked

    # Rule 8.3.29a: Card is considered to be cranked after Crank is used
    Scenario: Card is considered to be cranked after using Crank
        Given a card with the Crank keyword
        And the card has a steam counter on it
        When the card enters the arena and the player uses Crank
        Then the card is considered to be cranked

    # Rule 8.3.29: Crank ability meaning matches comprehensive rules text
    Scenario: Crank ability meaning matches comprehensive rules text
        Given a card with the Crank keyword
        When I check the meaning of the Crank ability
        Then the Crank meaning is "As this enters the arena, you may remove a steam counter from it. If you do, gain an action point."
