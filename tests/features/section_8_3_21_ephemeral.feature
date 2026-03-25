# Feature file for Section 8.3.21: Ephemeral (Ability Keyword)
# Reference: Flesh and Blood Comprehensive Rules Section 8.3.21
#
# Rule 8.3.21: Ephemeral is a meta-static ability and a static ability that
# respectively mean "You can't start the game with this in your deck." and
# "If this would be put into a graveyard from anywhere, instead it ceases to exist."
#
# Rule 8.3.21a: A player cannot include a card with Ephemeral in their card-pool.
#
# Rule 8.3.21b: A card that ceases to exist from Ephemeral is removed from the
# game. A card that is removed from the game has no further interaction with the
# rules and effects in the game.

Feature: Section 8.3.21 - Ephemeral Ability Keyword
    As a game engine
    I need to correctly implement the Ephemeral ability keyword
    So that Ephemeral cards cannot be included in card-pools and cease to exist instead of going to graveyard

    # Rule 8.3.21: Ephemeral is both a meta-static ability and a static ability

    Scenario: Ephemeral is a meta-static ability
        Given a card with Ephemeral ability
        When I inspect the Ephemeral ability
        Then the Ephemeral ability is a meta-static ability

    Scenario: Ephemeral is also a static ability
        Given a card with Ephemeral ability
        When I inspect the Ephemeral ability
        Then the Ephemeral ability is also a static ability

    # Rule 8.3.21: Meta-static part means "You can't start the game with this in your deck"

    Scenario: Ephemeral meta-static meaning is cannot start in deck
        Given a card with Ephemeral ability
        When I inspect the Ephemeral ability
        Then the Ephemeral meta-static meaning is "You can't start the game with this in your deck."

    # Rule 8.3.21: Static part means "If this would be put into a graveyard from anywhere, instead it ceases to exist"

    Scenario: Ephemeral static meaning is ceases to exist instead of going to graveyard
        Given a card with Ephemeral ability
        When I inspect the Ephemeral ability
        Then the Ephemeral static meaning is "If this would be put into a graveyard from anywhere, instead it ceases to exist."

    # Rule 8.3.21a: A player cannot include a card with Ephemeral in their card-pool

    Scenario: A card with Ephemeral cannot be included in a player's card-pool
        Given a card with Ephemeral ability
        When I check if the card can be included in a card-pool
        Then the card cannot be included in the card-pool

    Scenario: A card without Ephemeral can be included in a player's card-pool
        Given a card without Ephemeral ability
        When I check if the card can be included in a card-pool
        Then the card can be included in the card-pool

    # Rule 8.3.21: If an Ephemeral card would be put into a graveyard, it ceases to exist instead

    Scenario: An Ephemeral card ceases to exist instead of going to graveyard
        Given a card with Ephemeral ability is in play
        When the card would be put into the graveyard
        Then the card ceases to exist instead of going to graveyard
        And the graveyard does not contain the Ephemeral card

    Scenario: An Ephemeral card ceases to exist when moved from hand to graveyard
        Given a card with Ephemeral ability is in a player's hand
        When the card would be put into the graveyard from hand
        Then the card ceases to exist instead of going to graveyard

    # Rule 8.3.21b: A card that ceases to exist from Ephemeral is removed from the game

    Scenario: An Ephemeral card that ceases to exist is removed from the game
        Given a card with Ephemeral ability is in play
        When the card would be put into the graveyard
        And the card ceases to exist via Ephemeral
        Then the card is removed from the game

    # Rule 8.3.21b: A card removed from the game has no further interaction with rules and effects

    Scenario: A card removed from game via Ephemeral has no further interaction with game rules
        Given a card with Ephemeral ability has ceased to exist
        When I check if the removed card can interact with game rules
        Then the removed card has no further interaction with rules and effects
