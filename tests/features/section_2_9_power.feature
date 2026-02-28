# Feature file for Section 2.9: Power
# Reference: Flesh and Blood Comprehensive Rules Section 2.9
#
# 2.9.1 Power is a numeric property of an object, which represents the power
#        value used in the damage step of combat.
#
# 2.9.2 The printed power of a card is typically located at the bottom left
#        corner of a card next to the {p} symbol. The printed power defines the
#        base power of a card. If a card does not have a printed power, it does
#        not have the power property (0 is a valid printed power).
#
# 2.9.2a If the power value of a card is represented as a (c) then the card has
#         an ability that defines the base power of the card at any point in or
#         out of the game. If the ability requires a number that cannot be
#         determined, the power of the card is 0.
#
# 2.9.3 The power of an object can be modified. The term "power" or the symbol
#        {p} refers to the modified power of an object.

Feature: Section 2.9 - Power
    As a game engine
    I need to correctly implement power rules
    So that card power is tracked, referenced, and modified correctly

    # Rule 2.9.1 - Power is a numeric property
    Scenario: Power is a numeric property of a card
        Given a power card is created with a printed power of 3
        When the engine checks the power property of the power 3 card
        Then the power 3 card should have the power property
        And the power of the power 3 card should be 3
        And the power of the power 3 card should be numeric

    # Rule 2.9.1 - Power is used in the damage step of combat
    Scenario: Power value is used in the damage step of combat
        Given a power card is created with a printed power of 4
        When the engine calculates the power value of the power 4 card for combat
        Then the combat power of the power 4 card should be 4

    # Rule 2.9.2 - Printed power defines base power
    Scenario: Printed power defines the base power of a card
        Given a power card is created with a printed power of 2
        When the engine checks the base power of the power 2 card
        Then the base power of the power 2 card should be 2

    # Rule 2.9.2 - Zero is a valid printed power
    Scenario: Zero is a valid printed power
        Given a power card is created with a printed power of 0
        When the engine checks the power property of the power 0 card
        Then the power 0 card should have the power property
        And the power of the power 0 card should be 0

    # Rule 2.9.2 - Card without printed power lacks the power property
    Scenario: Card without a printed power lacks the power property
        Given a power card is created with no printed power
        When the engine checks the power property of the no-power card
        Then the no-power card should not have the power property

    # Rule 2.9.2a - (c) power defined by ability
    Scenario: Card with (c) power has ability that defines power
        Given a power card named "Mutated Mass" has power defined by an ability with value 7
        When the engine checks the power property of the ability-power card
        Then the ability-power card should have the power property
        And the power of the ability-power card should be 7

    # Rule 2.9.2a - (c) power is 0 when ability cannot determine value
    Scenario: Card with (c) power evaluates to 0 when ability cannot determine value
        Given a power card has power defined by an ability that cannot be determined
        When the engine checks the power property of the undetermined-power card
        Then the undetermined-power card should have the power property
        And the power of the undetermined-power card should be 0

    # Rule 2.9.3 - Power can be modified
    Scenario: Power of an object can be modified by effects
        Given a power card is created with a printed power of 3
        And a power boost effect of plus 2 is applied to the power 3 card
        When the engine checks the modified power of the power 3 card
        Then the modified power of the power 3 card should be 5

    # Rule 2.9.3 - "power" refers to the modified power
    Scenario: The term power refers to the modified power not base power
        Given a power card is created with a printed power of 4
        And a power boost effect of plus 1 is applied to the power 4 card
        When the engine resolves the term power for the power 4 card
        Then the resolved power of the power 4 card should be 5
        And the base power of the power 4 card should remain 4

    # Rule 2.9.3 - {p} symbol refers to modified power
    Scenario: The symbol p refers to the modified power of an object
        Given a power card is created with a printed power of 2
        And a power boost effect of plus 3 is applied to the power 2 card
        When the engine resolves the p symbol for the power 2 card
        Then the p symbol power of the power 2 card should be 5

    # Rule 2.9.3 - Power can be decreased by effects
    Scenario: Power of an object can be decreased by effects
        Given a power card is created with a printed power of 5
        And a power reduction effect of minus 2 is applied to the power 5 card
        When the engine checks the modified power of the power 5 card
        Then the modified power of the power 5 card should be 3

    # Rule 2.0.3c cross-ref - Power cannot go below zero
    Scenario: Power cannot be reduced below zero
        Given a power card is created with a printed power of 1
        And a power reduction effect of minus 3 is applied to the power 1 card
        When the engine checks the modified power of the power 1 card
        Then the modified power of the power 1 card should be 0

    # Rule 2.9.2 - Multiple cards each have their own power
    Scenario: Multiple cards each have independent power values
        Given a power card is created with a printed power of 3
        And another power card is created with a printed power of 6
        When the engine checks both power cards
        Then the first card power should be 3
        And the second card power should be 6
