# Feature file for Section 2.2: Cost
# Reference: Flesh and Blood Comprehensive Rules Section 2.2
#
# 2.2.1 Cost is a numeric property of a card or ability, which determines the
#        starting resource asset-cost to play the card or activate the ability.
#
# 2.2.2 The printed cost of a card is typically expressed within a resource point
#        symbol located in the top right corner of the card. The printed cost defines
#        the base cost of a card. If a card does not have a printed cost, it does not
#        have the cost property (0 is a valid printed cost).
#
# 2.2.2a If the printed value is expressed as two or more undefined symbols and/or
#         numeric values, they are additive for determining the base cost of a card.
#         Example: Spark of Genius has the cost property with the printed value of "XX,"
#         which determines the base cost as X+X for any value of X.
#
# 2.2.3 The printed cost of an activated ability is expressed as {r} symbols as part of
#        the description of the ability, where the number of {r} symbols dictates the
#        printed cost. If there are no resource symbols, then the printed cost is 0.
#        The printed cost defines the base resource cost of the ability.
#
# 2.2.4 The cost property of an object cannot be modified.
#
# 2.2.4a An effect that increases or reduces the cost of an object does not modify the
#         cost property of that object. Effects that modify cost are only applied as part
#         of the process for playing or activating that object.
#         Example: An effect that reduces the cost to play a card does not change the cost
#         property of that card in any way - it only changes the calculation of the resource
#         cost when that card is being played.
#
# 2.2.4b An effect that refers to the cost of an object refers to the unmodified cost
#         property of an object. An effect that refers to the payment of an object, refers
#         to the modified cost of an object when it was paid to play/activate and put that
#         object on the stack.
#
# 2.2.5 The visual expression in {r} symbols and the numerical expression of cost are
#        functionally identical.
#        Example: "Search your deck for a card with cost value 1," is considered to be the
#        same as the text "Search your deck for a card with cost value {r}."

Feature: Section 2.2 - Cost
    As a game engine
    I need to correctly implement cost rules
    So that card costs are tracked, referenced, and modified correctly

    # Rule 2.2.1 - Cost is a numeric property determining starting resource cost
    Scenario: Cost is a numeric property of a card
        Given a card is created with a printed cost of 3
        When the engine checks the cost property of the cost 3 card
        Then the cost 3 card should have the cost property
        And the cost of the cost 3 card should be 3

    # Rule 2.2.1 - Cost property determines starting resource asset-cost
    Scenario: Cost determines starting resource asset-cost to play the card
        Given a card is created with a printed cost of 2
        When the engine determines the starting resource asset-cost for the cost 2 card
        Then the starting resource asset-cost for the cost 2 card should be 2

    # Rule 2.2.2 - Printed cost defines the base cost
    Scenario: Printed cost defines the base cost of a card
        Given a card is created with a printed cost of 4
        When the engine checks the base cost of the cost 4 card
        Then the base cost of the cost 4 card should be 4

    # Rule 2.2.2 - Zero is a valid printed cost
    Scenario: Zero is a valid printed cost
        Given a card is created with a printed cost of 0
        When the engine checks the cost property of the cost 0 card
        Then the cost 0 card should have the cost property
        And the cost of the cost 0 card should be 0

    # Rule 2.2.2 - Card without printed cost lacks cost property
    Scenario: Card without a printed cost lacks the cost property
        Given a card is created with no printed cost
        When the engine checks the cost property of the no-cost card
        Then the no-cost card should not have the cost property

    # Rule 2.2.2a - Additive undefined symbols determine base cost
    Scenario: Card with two X symbols has additive base cost
        Given a card named "Spark of Genius" is created with two undefined X cost symbols
        When the engine determines the base cost of the Spark of Genius card
        Then the base cost formula of the Spark of Genius card should be additive
        And the base cost of the Spark of Genius card with X equals 3 should be 6

    # Rule 2.2.2a - Numeric values combined with undefined symbols are additive
    Scenario: Card with mixed numeric and X cost symbols has additive base cost
        Given a card is created with a cost of X plus 1
        When the engine determines the base cost of the mixed cost card
        Then the base cost of the mixed cost card with X equals 2 should be 3

    # Rule 2.2.3 - Activated ability cost expressed as resource symbols
    Scenario: Activated ability with two resource symbols has base cost of 2
        Given an activated ability is created with 2 resource symbols in its cost
        When the engine checks the base cost of the 2-resource-symbol ability
        Then the base cost of the 2-resource-symbol ability should be 2

    # Rule 2.2.3 - Activated ability with no resource symbols has base cost 0
    Scenario: Activated ability with no resource symbols has base cost of 0
        Given an activated ability is created with no resource symbols in its cost
        When the engine checks the base cost of the zero-resource ability
        Then the base cost of the zero-resource ability should be 0

    # Rule 2.2.3 - Numeric count of resource symbols is the printed cost
    Scenario: The number of resource symbols determines the ability printed cost
        Given an activated ability is created with 3 resource symbols in its cost
        When the engine checks the printed cost of the 3-resource-symbol ability
        Then the printed cost of the 3-resource-symbol ability should be 3

    # Rule 2.2.4 - Cost property cannot be modified
    Scenario: The cost property of a card cannot be modified
        Given a card is created with a base cost of 5
        When an effect attempts to modify the cost property of the base-cost-5 card
        Then the cost property of the base-cost-5 card should remain unchanged at 5

    # Rule 2.2.4a - Effects modify play cost not the cost property
    Scenario: Cost reduction effect does not change the cost property
        Given a card is created with a base cost of 3
        And a cost reduction effect of 1 is applied when playing the cost 3 card
        When the engine checks the cost property of the cost 3 card with reduction
        Then the cost property of the cost 3 card with reduction should still be 3
        And the play cost of the cost 3 card with reduction should be 2

    # Rule 2.2.4a - Cost modification only applies during the play process
    Scenario: Cost reduction only applies during the playing process
        Given a card is created with a base cost of 4
        And a cost reduction effect of 2 is registered for the base cost 4 card
        When the engine checks the cost property outside of the playing process
        Then the cost property outside playing should be 4
        And the cost modification should only apply during playing

    # Rule 2.2.4b - Effect referring to "cost" uses unmodified cost property
    Scenario: Effect referring to cost uses the unmodified cost property
        Given a card is created with a base cost of 3 for cost-reference testing
        And a cost reduction effect of 1 is registered for the cost-reference card
        When an effect refers to the cost of the cost-reference card
        Then the cost referred to should be the unmodified value of 3

    # Rule 2.2.4b - Effect referring to "payment" uses modified cost at stack time
    Scenario: Effect referring to payment uses the modified cost when paid
        Given a card is created with a base cost of 3 for payment testing
        And a cost reduction effect of 1 is registered for the payment test card
        When the payment test card is played and the payment amount is recorded
        Then the recorded payment amount should be the modified value of 2

    # Rule 2.2.5 - Visual {r} symbols and numeric cost values are equivalent
    Scenario: One resource symbol is functionally identical to numeric cost 1
        Given a card is created with a cost expressed as one resource symbol
        When the engine interprets the resource symbol cost as numeric
        Then the numeric cost equivalent should be 1

    # Rule 2.2.5 - Search by cost value finds cards matching resource symbol count
    Scenario: Searching by numeric cost value finds cards with matching resource symbols
        Given a card named "Cost 1 Card" is created with a numeric cost of 1
        And another card named "Cost 1 Symbol Card" is created with one resource symbol cost
        When the engine searches for cards with cost value 1
        Then both "Cost 1 Card" and "Cost 1 Symbol Card" should be found
