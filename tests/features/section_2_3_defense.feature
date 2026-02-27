# Feature file for Section 2.3: Defense
# Reference: Flesh and Blood Comprehensive Rules Section 2.3
#
# 2.3.1 Defense is a numeric property of an object, which represents the value
#        contributed to the total sum of defense used in the damage step of combat.
#
# 2.3.2 The printed defense of a card is typically located at the bottom right
#        corner of a card next to the {d} symbol. The printed defense defines the
#        base defense of a card. If a card does not have a printed defense, it does
#        not have the defense property (0 is a valid printed defense).
#
# 2.3.2a If the defense of a card is represented as a (c), then the card has an
#         ability that defines the defense of the card at any point in or out of the
#         game. If the ability requires a number that cannot be determined, the
#         defense of the card is 0.
#
# 2.3.3 The defense of an object can be modified. The term "defense" or the symbol
#        {d} refers to the modified defense of an object.

Feature: Section 2.3 - Defense
    As a game engine
    I need to correctly implement defense rules
    So that card defense is tracked, referenced, and modified correctly

    # Rule 2.3.1 - Defense is a numeric property
    Scenario: Defense is a numeric property of a card
        Given a defense card is created with a printed defense of 3
        When the engine checks the defense property of the defense 3 card
        Then the defense 3 card should have the defense property
        And the defense of the defense 3 card should be 3
        And the defense of the defense 3 card should be numeric

    # Rule 2.3.1 - Defense contributes to total sum of defense in damage step
    Scenario: Defense value is used in the damage step of combat
        Given a defense card is created with a printed defense of 4
        When the engine calculates the defense contribution of the defense 4 card
        Then the defense contribution of the defense 4 card should be 4

    # Rule 2.3.2 - Printed defense defines base defense
    Scenario: Printed defense defines the base defense of a card
        Given a defense card is created with a printed defense of 2
        When the engine checks the base defense of the defense 2 card
        Then the base defense of the defense 2 card should be 2

    # Rule 2.3.2 - Zero is a valid printed defense
    Scenario: Zero is a valid printed defense
        Given a defense card is created with a printed defense of 0
        When the engine checks the defense property of the defense 0 card
        Then the defense 0 card should have the defense property
        And the defense of the defense 0 card should be 0

    # Rule 2.3.2 - Card without printed defense lacks defense property
    Scenario: Card without a printed defense lacks the defense property
        Given a defense card is created with no printed defense
        When the engine checks the defense property of the no-defense card
        Then the no-defense card should not have the defense property

    # Rule 2.3.2a - (c) defense defined by ability
    Scenario: Card with (c) defense has ability that defines defense
        Given a defense card named "Crown of Seeds" has defense defined by an ability with value 5
        When the engine checks the defense property of the ability-defense card
        Then the ability-defense card should have the defense property
        And the defense of the ability-defense card should be 5

    # Rule 2.3.2a - (c) defense is 0 when ability cannot determine value
    Scenario: Card with (c) defense evaluates to 0 when ability cannot determine value
        Given a defense card has defense defined by an ability that cannot be determined
        When the engine checks the defense property of the undetermined-defense card
        Then the undetermined-defense card should have the defense property
        And the defense of the undetermined-defense card should be 0

    # Rule 2.3.3 - Defense can be modified
    Scenario: Defense of an object can be modified by effects
        Given a defense card is created with a printed defense of 3
        And a defense boost effect of plus 2 is applied to the defense 3 card
        When the engine checks the modified defense of the defense 3 card
        Then the modified defense of the defense 3 card should be 5

    # Rule 2.3.3 - "defense" refers to the modified defense
    Scenario: The term defense refers to the modified defense not base defense
        Given a defense card is created with a printed defense of 4
        And a defense boost effect of plus 1 is applied to the defense 4 card
        When the engine resolves the term defense for the defense 4 card
        Then the resolved defense of the defense 4 card should be 5
        And the base defense of the defense 4 card should remain 4

    # Rule 2.3.3 - {d} symbol refers to modified defense
    Scenario: The symbol d refers to the modified defense of an object
        Given a defense card is created with a printed defense of 2
        And a defense boost effect of plus 3 is applied to the defense 2 card
        When the engine resolves the d symbol for the defense 2 card
        Then the d symbol defense of the defense 2 card should be 5

    # Rule 2.3.3 - Defense reduced by effects
    Scenario: Defense of an object can be decreased by effects
        Given a defense card is created with a printed defense of 5
        And a defense reduction effect of minus 2 is applied to the defense 5 card
        When the engine checks the modified defense of the defense 5 card
        Then the modified defense of the defense 5 card should be 3

    # Rule 2.0.3c cross-ref - Defense cannot go below zero
    Scenario: Defense cannot be reduced below zero
        Given a defense card is created with a printed defense of 1
        And a defense reduction effect of minus 3 is applied to the defense 1 card
        When the engine checks the modified defense of the defense 1 card
        Then the modified defense of the defense 1 card should be 0

    # Rule 2.3.2 - Multiple cards each have their own defense
    Scenario: Multiple cards each have independent defense values
        Given a defense card is created with a printed defense of 3
        And another defense card is created with a printed defense of 2
        When the engine checks both defense cards
        Then the first card defense should be 3
        And the second card defense should be 2
