# Feature file for Section 8.3.32: Scrap (Ability Keyword)
# Reference: Flesh and Blood Comprehensive Rules Section 8.3.32
#
# Rule 8.3.32: Scrap is a play-static ability that means "As an additional cost
# to play this, you may banish an item or equipment from your graveyard."
#
# Rule 8.3.32a: If a player pays the additional cost to play a card with scrap,
# the player is considered to have scrapped, and the banished card is considered
# to have been scrapped.
#
# Rule 8.3.32b: A player cannot scrap if they cannot pay the additional cost of
# banishing an item or equipment from their graveyard.
#
# Key aspects of Scrap:
# - It is a PLAY-STATIC ability (affects how the card is played)
# - The additional cost is OPTIONAL ("you may banish")
# - Only items or equipment can be banished (not actions, instants, etc.)
# - The card must come from the graveyard (not from other zones)
# - When scrapped: the player is "considered to have scrapped"
# - When scrapped: the banished card is "considered to have been scrapped"
# - Cannot scrap if there are no items or equipment in graveyard

Feature: Section 8.3.32 - Scrap Ability Keyword
    As a game engine
    I need to correctly implement the Scrap ability keyword
    So that players can banish items or equipment from their graveyard as an additional cost

    # Rule 8.3.32: Scrap is recognized as a keyword
    Scenario: Scrap is recognized as an ability keyword
        Given a card with the Scrap keyword
        When I inspect the card's keywords
        Then the card has the Scrap keyword

    # Rule 8.3.32: Scrap is a play-static ability
    Scenario: Scrap is a play-static ability
        Given a card with the Scrap keyword
        When I check the ability type of Scrap
        Then Scrap is a play-static ability

    # Rule 8.3.32: Scrap ability meaning matches comprehensive rules text
    Scenario: Scrap ability meaning matches comprehensive rules text
        Given a card with the Scrap keyword
        When I inspect the Scrap ability's meaning
        Then the Scrap meaning is "As an additional cost to play this, you may banish an item or equipment from your graveyard"

    # Rule 8.3.32: The additional cost is optional (player may choose not to scrap)
    Scenario: Player can play a Scrap card without paying the additional cost
        Given a player has a card with the Scrap keyword in hand
        And the player has an item in their graveyard
        When the player plays the card without paying the Scrap cost
        Then the card is played successfully
        And the item remains in the graveyard
        And the player is not considered to have scrapped

    # Rule 8.3.32 + 8.3.32a: Player can scrap by banishing an item from graveyard
    Scenario: Player scraps by banishing an item from their graveyard
        Given a player has a card with the Scrap keyword in hand
        And the player has an item in their graveyard
        When the player plays the card and pays the Scrap cost by banishing the item
        Then the card is played successfully
        And the item is banished
        And the item is no longer in the graveyard

    # Rule 8.3.32 + 8.3.32a: Player can scrap by banishing equipment from graveyard
    Scenario: Player scraps by banishing equipment from their graveyard
        Given a player has a card with the Scrap keyword in hand
        And the player has an equipment in their graveyard
        When the player plays the card and pays the Scrap cost by banishing the equipment
        Then the card is played successfully
        And the equipment is banished
        And the equipment is no longer in the graveyard

    # Rule 8.3.32a: When scrapping, player is considered to have scrapped
    Scenario: Player is considered to have scrapped after paying the Scrap cost
        Given a player has a card with the Scrap keyword in hand
        And the player has an item in their graveyard
        When the player plays the card and pays the Scrap cost by banishing the item
        Then the player is considered to have scrapped

    # Rule 8.3.32a: The banished card is considered to have been scrapped
    Scenario: The banished card is considered to have been scrapped
        Given a player has a card with the Scrap keyword in hand
        And the player has an item in their graveyard
        When the player plays the card and pays the Scrap cost by banishing the item
        Then the banished card is considered to have been scrapped

    # Rule 8.3.32b: Cannot scrap without items or equipment in graveyard
    Scenario: Player cannot scrap with an empty graveyard
        Given a player has a card with the Scrap keyword in hand
        And the player's graveyard has no items or equipment
        When the player attempts to pay the Scrap cost
        Then the player cannot scrap
        And no card is banished from the graveyard
