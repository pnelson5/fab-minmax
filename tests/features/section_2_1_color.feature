# Feature file for Section 2.1: Color
# Reference: Flesh and Blood Comprehensive Rules Section 2.1
#
# 2.1.1 Color is a visual representation of the color of a card.
#
# 2.1.2 The printed color of a card is typically expressed at the top of a card as a
#        color strip.
#        A card with a red color strip is considered red.
#        A card with a yellow color strip is considered yellow.
#        A card with a blue color strip is considered blue.
#        A card with no color strip has no color.
#
# 2.1.2a The printed pitch of a card is typically associated with the printed color of
#         a card, but they are independent. Cards with a printed pitch of 1, 2, and 3,
#         typically have a color strip of red, yellow, and blue respectively. A card
#         with no printed pitch typically does not have a color strip.

Feature: Section 2.1 - Color
    As a game engine
    I need to correctly implement color rules
    So that card colors are tracked and referenced correctly

    # Rule 2.1.1 - Color is a visual property of a card
    Scenario: Color is a visual property of a card
        Given a card is created with a red color strip for visual property testing
        When the engine checks the visual color property of the card
        Then the card should have the color property
        And the color should represent the visual appearance of the card

    # Rule 2.1.2 - Red color strip makes card red
    Scenario: Card with red color strip is considered red
        Given a card is created with a red color strip
        When the engine checks the color of the red card
        Then the color of the red card should be "red"

    # Rule 2.1.2 - Yellow color strip makes card yellow
    Scenario: Card with yellow color strip is considered yellow
        Given a card is created with a yellow color strip
        When the engine checks the color of the yellow card
        Then the color of the yellow card should be "yellow"

    # Rule 2.1.2 - Blue color strip makes card blue
    Scenario: Card with blue color strip is considered blue
        Given a card is created with a blue color strip
        When the engine checks the color of the blue card
        Then the color of the blue card should be "blue"

    # Rule 2.1.2 - No color strip means no color
    Scenario: Card with no color strip has no color
        Given a card is created with no color strip
        When the engine checks the color of the colorless card
        Then the colorless card should have no color

    # Rule 2.1.2a - Pitch and color are typically associated
    Scenario: Card with pitch 1 typically has red color
        Given a card is created with pitch value 1 and red color strip
        When the engine checks both the color and pitch of the red pitch 1 card
        Then the color of the red pitch 1 card should be "red"
        And the pitch of the red pitch 1 card should be 1

    # Rule 2.1.2a - Pitch 2 typically associated with yellow
    Scenario: Card with pitch 2 typically has yellow color
        Given a card is created with pitch value 2 and yellow color strip
        When the engine checks both the color and pitch of the yellow pitch 2 card
        Then the color of the yellow pitch 2 card should be "yellow"
        And the pitch of the yellow pitch 2 card should be 2

    # Rule 2.1.2a - Pitch 3 typically associated with blue
    Scenario: Card with pitch 3 typically has blue color
        Given a card is created with pitch value 3 and blue color strip
        When the engine checks both the color and pitch of the blue pitch 3 card
        Then the color of the blue pitch 3 card should be "blue"
        And the pitch of the blue pitch 3 card should be 3

    # Rule 2.1.2a - Color and pitch are independent properties
    Scenario: Color and pitch are independent - red card can have pitch 3
        Given a card is created with a red color strip and pitch value 3
        When the engine checks the color and pitch of the red pitch 3 card independently
        Then the color of the red pitch 3 card should be "red"
        And the pitch of the red pitch 3 card should be 3
        And color and pitch of the red pitch 3 card should be recognized as independent properties

    # Rule 2.1.2a - A card with no pitch typically has no color
    Scenario: Card with no printed pitch typically has no color strip
        Given a card is created with no pitch and no color strip
        When the engine checks color and pitch of the no-pitch no-color card
        Then the no-pitch no-color card should have no color
        And the no-pitch no-color card should have no pitch property

    # Rule 2.1.2a - A card without pitch can still have a color (they are independent)
    Scenario: Card without pitch can have a color via independent color property
        Given a card is created with a blue color strip but no pitch property
        When the engine checks the color and pitch of the blue no-pitch card independently
        Then the color of the blue no-pitch card should be "blue"
        And the blue no-pitch card should have no pitch property
        And color and pitch of the blue no-pitch card should be recognized as independent properties
