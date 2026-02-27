# Feature file for Section 2.4: Intellect
# Reference: Flesh and Blood Comprehensive Rules Section 2.4
#
# 2.4.1 Intellect is a numeric property of a hero card, which represents the
#        number of cards the controlling player draws up to at the end of their
#        turn. [4.4]
#
# 2.4.2 The printed intellect of a card is typically located at the bottom left
#        corner of a card next to the {i} symbol. The printed intellect defines
#        the base intellect of a card. If a card does not have a printed
#        intellect, it does not have the intellect property (0 is a valid printed
#        intellect).
#
# 2.4.3 The intellect of an object can be modified. The term "intellect" or the
#        symbol {i} refers to the modified intellect of an object.

Feature: Section 2.4 - Intellect
    As a game engine
    I need to correctly implement intellect rules
    So that hero intellect is tracked, referenced, and modified correctly

    # Rule 2.4.1 - Intellect is a numeric property of a hero card
    Scenario: Intellect is a numeric property of a hero card
        Given a hero card is created with a printed intellect of 4
        When the engine checks the intellect property of the intellect 4 hero
        Then the intellect 4 hero should have the intellect property
        And the intellect of the intellect 4 hero should be 4
        And the intellect of the intellect 4 hero should be numeric

    # Rule 2.4.1 - Intellect represents the number of cards drawn at end of turn
    Scenario: Intellect represents cards drawn at end of turn
        Given a hero card is created with a printed intellect of 3
        When the engine resolves end-of-turn draw for the intellect 3 hero
        Then the player draws up to 3 cards at end of turn

    # Rule 2.4.1 - Intellect is specifically a hero card property
    Scenario: Intellect is a property of hero cards only
        Given a hero card is created with a printed intellect of 4
        And a non-hero action card is created with no intellect
        When the engine checks the intellect property of both cards
        Then the hero card should have the intellect property
        And the non-hero action card should not have the intellect property

    # Rule 2.4.2 - Printed intellect defines base intellect
    Scenario: Printed intellect defines the base intellect of a hero card
        Given a hero card is created with a printed intellect of 5
        When the engine checks the base intellect of the intellect 5 hero
        Then the base intellect of the intellect 5 hero should be 5

    # Rule 2.4.2 - Zero is a valid printed intellect
    Scenario: Zero is a valid printed intellect
        Given a hero card is created with a printed intellect of 0
        When the engine checks the intellect property of the intellect 0 hero
        Then the intellect 0 hero should have the intellect property
        And the intellect of the intellect 0 hero should be 0

    # Rule 2.4.2 - No printed intellect means no intellect property
    Scenario: Card without a printed intellect lacks the intellect property
        Given a non-hero card is created with no printed intellect
        When the engine checks the intellect property of the no-intellect card
        Then the no-intellect card should not have the intellect property

    # Rule 2.4.3 - Intellect of an object can be modified
    Scenario: Intellect of a hero can be modified by effects
        Given a hero card is created with a printed intellect of 4
        And an intellect boost effect of plus 1 is applied to the intellect 4 hero
        When the engine checks the modified intellect of the intellect 4 hero
        Then the modified intellect of the intellect 4 hero should be 5

    # Rule 2.4.3 - "intellect" refers to modified intellect
    Scenario: The term intellect refers to the modified intellect not base intellect
        Given a hero card is created with a printed intellect of 4
        And an intellect boost effect of plus 2 is applied to the intellect 4 hero
        When the engine resolves the term intellect for the intellect 4 hero
        Then the resolved intellect of the intellect 4 hero should be 6
        And the base intellect of the intellect 4 hero should remain 4

    # Rule 2.4.3 - {i} symbol refers to modified intellect
    Scenario: The symbol i refers to the modified intellect of a hero
        Given a hero card is created with a printed intellect of 3
        And an intellect boost effect of plus 2 is applied to the intellect 3 hero
        When the engine resolves the i symbol for the intellect 3 hero
        Then the i symbol intellect of the intellect 3 hero should be 5

    # Rule 2.4.3 - Intellect can be decreased by effects
    Scenario: Intellect of a hero can be decreased by effects
        Given a hero card is created with a printed intellect of 4
        And an intellect reduction effect of minus 1 is applied to the intellect 4 hero
        When the engine checks the modified intellect of the intellect 4 hero
        Then the modified intellect of the intellect 4 hero should be 3

    # Rule 2.0.3c cross-ref - Intellect cannot go below zero
    Scenario: Intellect cannot be reduced below zero
        Given a hero card is created with a printed intellect of 2
        And an intellect reduction effect of minus 5 is applied to the intellect 2 hero
        When the engine checks the modified intellect of the intellect 2 hero
        Then the modified intellect of the intellect 2 hero should be 0

    # Rule 2.4.1 + 2.4.3 - Modified intellect affects end-of-turn draw
    Scenario: Modified intellect affects how many cards are drawn at end of turn
        Given a hero card is created with a printed intellect of 4
        And an intellect boost effect of plus 1 is applied to the intellect 4 hero
        When the engine resolves end-of-turn draw for the boosted intellect 4 hero
        Then the player draws up to 5 cards at end of turn

    # Rule 2.4.2 - Two hero cards have independent intellect values
    Scenario: Multiple hero cards have independent intellect values
        Given a hero card is created with a printed intellect of 4
        And another hero card is created with a printed intellect of 3
        When the engine checks both intellect hero cards
        Then the first hero intellect should be 4
        And the second hero intellect should be 3
