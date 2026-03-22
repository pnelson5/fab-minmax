# Feature file for Section 3.15: Stack
# Reference: Flesh and Blood Comprehensive Rules Section 3.15
#
# 3.15.1 The stack zone is a public zone outside the arena. There is only one
#         stack zone, shared by all players, and it does not have an owner.
#
# 3.15.2 The term "stack" refers to the stack zone.
#
# 3.15.3 The stack contains an ordered collection of layers. [1.6]
#
# 3.15.4 When a layer is added onto the stack, it becomes layer N+1 where N is
#         the number of existing layers on the stack.
#
# 3.15.5 The top layer of the stack is layer N, with the highest value of N.
#
# 3.15.6 When a layer N is removed from the stack by a rule or effect, any
#         layer M where M>N becomes layer M-1.
#         Example: There are 4 layers on the stack. Layer 2 is an instant card
#         and is removed by a "negate" effect. Layer 3 becomes layer 2, and
#         layer 4 becomes layer 3, while layer 1 remains unchanged.
#
# Cross-references:
# - 3.0.1a: An empty zone does not cease to exist.
# - 3.0.3:  The stack zone is shared by all players (unlike player-owned zones).
# - 3.0.4a: The stack zone is a public zone.
# - 3.0.5b: The stack zone is NOT part of the arena.
# - 1.6:    Layers are objects placed on the stack by playing cards or
#           activating/triggering abilities.

Feature: Section 3.15 - Stack Zone
    As a game engine
    I need to correctly model the stack zone rules
    So that card and ability resolution, layer ordering, and stack management work correctly

    # ===== Rule 3.15.1: Stack is a public zone outside the arena =====

    # Test for Rule 3.15.1 - Stack is a public zone
    Scenario: The stack zone is a public zone
        Given a stack zone exists in the game
        When checking the visibility of the stack zone
        Then the stack zone is a public zone

    # Test for Rule 3.15.1 - Stack is outside the arena
    Scenario: The stack zone is outside the arena
        Given a stack zone exists in the game
        When checking whether the stack zone is in the arena
        Then the stack zone is not part of the arena

    # Test for Rule 3.15.1 - Stack has no owner
    Scenario: The stack zone has no owner
        Given a stack zone exists in the game
        When checking the ownership of the stack zone
        Then the stack zone has no owner

    # Test for Rule 3.15.1 - There is only one stack shared by all players
    Scenario: There is only one stack zone shared by all players
        Given a game with two players
        When checking how many stack zones exist
        Then there is exactly one stack zone
        And the stack zone is shared between all players

    # ===== Rule 3.15.3: Stack contains an ordered collection of layers =====

    # Test for Rule 3.15.3 - Stack starts empty
    Scenario: The stack starts empty before any layers are added
        Given a stack zone exists in the game
        When no layers have been added to the stack
        Then the stack contains zero layers

    # Test for Rule 3.15.3 - Stack holds layers in order
    Scenario: The stack holds layers in an ordered collection
        Given a stack zone exists in the game
        When a layer is added to the stack
        Then the stack contains one layer

    # ===== Rule 3.15.4: Layers added to stack become layer N+1 =====

    # Test for Rule 3.15.4 - First layer becomes layer 1
    Scenario: The first layer added to an empty stack becomes layer 1
        Given a stack zone exists in the game
        And the stack is empty
        When a layer is added to the stack
        Then the stack contains one layer
        And that layer is layer 1

    # Test for Rule 3.15.4 - Second layer becomes layer 2
    Scenario: A second layer added to the stack becomes layer 2
        Given a stack zone exists in the game
        And the stack already has 1 layer
        When another layer is added to the stack
        Then the stack contains two layers
        And the newest layer is layer 2

    # Test for Rule 3.15.4 - Multiple layers stack sequentially
    Scenario: Multiple layers are numbered sequentially when added
        Given a stack zone exists in the game
        And the stack is empty
        When 3 layers are added to the stack one at a time
        Then the stack contains three layers
        And the layers are numbered 1, 2, and 3 in order

    # ===== Rule 3.15.5: Top layer is layer N with highest N =====

    # Test for Rule 3.15.5 - Top layer is the most recently added
    Scenario: The top layer of the stack is the most recently added layer
        Given a stack zone exists in the game
        And the stack already has 2 layers
        When checking the top of the stack
        Then the top layer is layer 2

    # Test for Rule 3.15.5 - Top layer after adding third
    Scenario: The top layer updates when a new layer is added
        Given a stack zone exists in the game
        And the stack already has 2 layers
        When another layer is added to the stack
        Then the top layer is layer 3

    # ===== Rule 3.15.6: Removing layer N renumbers layers M>N =====

    # Test for Rule 3.15.6 - Removing top layer leaves N-1 layers
    Scenario: Removing the top layer decreases the stack size by one
        Given a stack zone exists in the game
        And the stack already has 3 layers
        When the top layer is removed from the stack
        Then the stack contains two layers

    # Test for Rule 3.15.6 - Removing a middle layer renumbers upper layers
    Scenario: Removing a middle layer causes upper layers to be renumbered downward
        Given a stack zone exists in the game
        And the stack has 4 layers labeled A B C D from bottom to top
        When layer 2 (B) is removed from the stack
        Then the stack contains three layers
        And layer 1 is still A
        And the former layer 3 (C) is now layer 2
        And the former layer 4 (D) is now layer 3

    # Test for Rule 3.15.6 - Removing bottom layer renumbers all other layers
    Scenario: Removing the bottom layer renumbers all layers above it
        Given a stack zone exists in the game
        And the stack has 3 layers labeled X Y Z from bottom to top
        When layer 1 (X) is removed from the stack
        Then the stack contains two layers
        And the former layer 2 (Y) is now layer 1
        And the former layer 3 (Z) is now layer 2

    # Test for Rule 3.15.6 - Example from rulebook: negate removes layer 2 of 4
    Scenario: Rulebook example - negate removes layer 2 of 4 layers
        Given a stack zone exists in the game
        And the stack has 4 layers labeled A B C D from bottom to top
        When layer 2 (B) is removed by a negate effect
        Then the stack contains three layers
        And layer 1 is still A
        And the former layer 3 (C) is now layer 2
        And the former layer 4 (D) is now layer 3
