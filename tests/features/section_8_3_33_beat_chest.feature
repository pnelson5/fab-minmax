# Feature file for Section 8.3.33: Beat Chest (Ability Keyword)
# Reference: Flesh and Blood Comprehensive Rules Section 8.3.33
#
# Rule 8.3.33: Beat Chest is a play-static ability that means "As an additional cost
# to play this, you may discard a card with 6 or more {p}."
#
# Rule 8.3.33a: If a player pays the additional cost to play a card with beat chest,
# the player is considered to have beaten chest.
#
# Rule 8.3.33b: A player cannot beat chest if they cannot pay the additional cost of
# discarding a card with 6 or more {p}.
#
# Key aspects of Beat Chest:
# - It is a PLAY-STATIC ability (affects how the card is played)
# - The additional cost is OPTIONAL ("you may discard")
# - The discarded card must have 6 or more pitch value ({p})
# - When the cost is paid: the player is "considered to have beaten chest"
# - Cannot beat chest if the player has no cards with 6+ pitch in hand

Feature: Section 8.3.33 - Beat Chest Ability Keyword
    As a game engine
    I need to correctly implement the Beat Chest ability keyword
    So that players can discard a high-pitch card as an additional cost

    # Rule 8.3.33: Beat Chest is recognized as a keyword
    Scenario: Beat Chest is recognized as an ability keyword
        Given a card with the Beat Chest keyword
        When I inspect the card's keywords
        Then the card has the Beat Chest keyword

    # Rule 8.3.33: Beat Chest is a play-static ability
    Scenario: Beat Chest is a play-static ability
        Given a card with the Beat Chest keyword
        When I check the ability type of Beat Chest
        Then Beat Chest is a play-static ability

    # Rule 8.3.33: Beat Chest ability meaning matches comprehensive rules text
    Scenario: Beat Chest ability meaning matches comprehensive rules text
        Given a card with the Beat Chest keyword
        When I inspect the Beat Chest ability's meaning
        Then the Beat Chest meaning is "As an additional cost to play this, you may discard a card with 6 or more {p}"

    # Rule 8.3.33: The additional cost is optional (player may choose not to beat chest)
    Scenario: Player can play a Beat Chest card without paying the additional cost
        Given a player has a card with the Beat Chest keyword in hand
        And the player has a card with 6 pitch in hand
        When the player plays the card without paying the Beat Chest cost
        Then the card is played successfully
        And the high-pitch card remains in hand
        And the player is not considered to have beaten chest

    # Rule 8.3.33 + 8.3.33a: Player can beat chest by discarding a card with exactly 6 pitch
    Scenario: Player beats chest by discarding a card with exactly 6 pitch
        Given a player has a card with the Beat Chest keyword in hand
        And the player has a card with 6 pitch in hand
        When the player plays the card and pays the Beat Chest cost by discarding the 6-pitch card
        Then the card is played successfully
        And the 6-pitch card is in the graveyard

    # Rule 8.3.33 + 8.3.33a: Player can beat chest by discarding a card with more than 6 pitch
    Scenario: Player beats chest by discarding a card with more than 6 pitch
        Given a player has a card with the Beat Chest keyword in hand
        And the player has a card with 7 pitch in hand
        When the player plays the card and pays the Beat Chest cost by discarding the 7-pitch card
        Then the card is played successfully
        And the 7-pitch card is in the graveyard

    # Rule 8.3.33a: When beating chest, player is considered to have beaten chest
    Scenario: Player is considered to have beaten chest after paying the cost
        Given a player has a card with the Beat Chest keyword in hand
        And the player has a card with 6 pitch in hand
        When the player plays the card and pays the Beat Chest cost by discarding the 6-pitch card
        Then the player is considered to have beaten chest

    # Rule 8.3.33b: Cannot beat chest without a card with 6+ pitch in hand
    Scenario: Player cannot beat chest without a high-pitch card in hand
        Given a player has a card with the Beat Chest keyword in hand
        And the player has no cards with 6 or more pitch in hand
        When the player attempts to pay the Beat Chest cost
        Then the player cannot beat chest
        And no card is discarded as the Beat Chest cost

    # Rule 8.3.33b: Cannot beat chest with only low-pitch cards (5 pitch is not enough)
    Scenario: Player cannot beat chest with a card that has only 5 pitch
        Given a player has a card with the Beat Chest keyword in hand
        And the player has a card with 5 pitch in hand
        And the player has no other cards with 6 or more pitch in hand
        When the player attempts to pay the Beat Chest cost
        Then the player cannot beat chest
