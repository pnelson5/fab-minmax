# Feature file for Section 7.1: Layer Step
# Reference: Flesh and Blood Comprehensive Rules Section 7.1
#
# Rule 7.1.1: The Layer Step is a game state where an attack is unresolved on the stack.
#
# Rule 7.1.2: First, the turn-player gains priority.
#
# Rule 7.1.3: Second and finally, when the top layer of the stack is the attack and all
# players pass in succession, the Layer Step ends and the Attack Step begins.
#
# Cross-references:
# Rule 7.0.2a: If the combat chain is closed and an attack is added to the stack,
#   the combat chain opens and the Layer Step begins immediately.
# Rule 5.3.1: If the stack is not empty and all players pass in succession, the top
#   layer resolves, EXCEPT the Layer Step of combat (attack on top of stack transitions
#   to Attack Step instead of resolving as a normal layer).

Feature: Section 7.1 - Layer Step
    As a game engine
    I need to correctly implement the Layer Step of combat
    So that attacks correctly transition from the stack to the combat chain

    # Test for Rule 7.1.1 - Layer Step is a game state with unresolved attack on stack
    Scenario: Layer Step is a game state where an attack is unresolved on the stack
        Given the combat chain is closed
        And a player has an attack card in hand
        When the player plays the attack card
        Then the attack is on the stack as an unresolved layer
        And the combat chain is open
        And the Layer Step is active

    # Test for Rule 7.0.2a + 7.1.1 - Combat chain opens and Layer Step begins when attack added
    Scenario: Playing an attack opens the combat chain and begins the Layer Step
        Given the combat chain is closed
        And the stack is empty
        When an attack is added to the stack
        Then the combat chain opens immediately
        And the Layer Step begins immediately

    # Test for Rule 7.1.2 - Turn-player gains priority first in the Layer Step
    Scenario: Turn-player gains priority at the start of the Layer Step
        Given the combat chain is closed
        And an attack is added to the stack
        When the Layer Step begins
        Then the turn-player has priority

    # Test for Rule 7.1.3 - Layer Step ends and Attack Step begins when all players pass
    Scenario: Layer Step ends and Attack Step begins when top of stack is attack and all players pass
        Given the Layer Step is active
        And the top layer of the stack is the attack
        When all players pass priority in succession
        Then the Layer Step ends
        And the Attack Step begins

    # Test for Rule 7.1.3 (negative) - Layer Step does not end if other layers are above attack
    Scenario: Layer Step does not end if the top of the stack is not the attack
        Given the Layer Step is active
        And the attack is on the stack
        And an instant is played on top of the attack
        When all players pass priority in succession
        Then the instant resolves
        And the Layer Step continues because the attack is now the top of the stack

    # Test for Rule 7.1.2 - Players can play instants during Layer Step (since they have priority)
    Scenario: Players can play instants during the Layer Step
        Given the Layer Step is active
        And the attack is unresolved on the stack
        When the turn-player plays an instant card
        Then the instant is placed on the stack above the attack
        And the attack remains unresolved on the stack

    # Test for Rule 7.1.3 edge case - Attack Step does NOT begin if players pass but attack is not on top
    Scenario: Attack Step does not begin if there are layers above the attack when all players pass
        Given the Layer Step is active
        And an instant is on top of the attack on the stack
        When all players pass priority in succession
        Then the instant resolves from the stack
        And the Layer Step continues
        And the Attack Step has not begun

    # Test for Rule 7.1.1 - Layer Step is distinct from normal layer resolution
    Scenario: Layer Step is distinct from normal stack resolution
        Given the Layer Step is active
        And the attack is the only layer on the stack
        When all players pass priority in succession
        Then the attack does not resolve as a normal layer
        And instead the Layer Step ends and the Attack Step begins

    # Test for Rule 7.0.2a - Layer Step starts when combat chain was previously closed
    Scenario: Layer Step begins immediately when attack is played while combat chain was closed
        Given the game is in the action phase
        And the combat chain is closed
        When a player plays an attack card targeting the opponent's hero
        Then the combat chain opens
        And the Layer Step begins
        And the turn-player has priority in the Layer Step
