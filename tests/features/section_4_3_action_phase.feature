# Feature file for Section 4.3: Action Phase
# Reference: Flesh and Blood Comprehensive Rules Section 4.3
#
# 4.3.1 First, the action phase starts. The "beginning of the action phase" event
#        occurs and effects that trigger at the beginning of the action phase are triggered.
#
# 4.3.2 Second, the turn-player has 1 action point.
#
# 4.3.2a Effects that trigger when a player gains an action point do not trigger when
#         the turn-player gains an action point this way.
#
# 4.3.2b Replacement effects that modify events when a player gains an action point
#         do not modify or replace when the turn-player gains an action point this way.
#
# 4.3.3 Third, the turn-player gains priority.
#
# 4.3.4 Fourth and finally, when the stack is empty, the combat chain is closed, and
#        both players pass priority in succession, the action phase ends and the game
#        proceeds to the End Phase.

Feature: Section 4.3 - Action Phase
    As a game engine
    I need to correctly implement the Action Phase
    So that action points are granted, priority flows, and the phase ends correctly

    # Rule 4.3.1 - Beginning of action phase event occurs
    Scenario: The beginning of action phase event occurs when action phase starts
        Given a game is in progress
        When the Action Phase begins
        Then the "beginning of the action phase" event occurs

    # Rule 4.3.1 - Triggered effects at beginning of action phase fire
    Scenario: Effects that trigger at the beginning of the action phase are triggered
        Given a game is in progress
        And an effect exists that triggers at the beginning of the action phase
        When the Action Phase begins
        Then the beginning-of-action-phase triggered effect fires

    # Rule 4.3.1 - Multiple beginning-of-action-phase triggers all fire
    Scenario: Multiple effects that trigger at beginning of action phase all fire
        Given a game is in progress
        And multiple effects exist that trigger at the beginning of the action phase
        When the Action Phase begins
        Then all beginning-of-action-phase triggered effects fire

    # Rule 4.3.2 - Turn-player has 1 action point at start of action phase
    Scenario: Turn-player has 1 action point at the start of the action phase
        Given a game is in progress
        When the Action Phase begins
        Then the turn-player has 1 action point

    # Rule 4.3.2 - Non-turn player does not gain action points from action phase start
    Scenario: Non-turn player does not gain action points at the start of the action phase
        Given a game is in progress
        When the Action Phase begins
        Then the non-turn player has 0 action points from the action phase grant

    # Rule 4.3.2a - Gain-action-point triggers do not fire for action phase grant
    Scenario: Gain-action-point triggers do not fire when turn-player gains action point from action phase
        Given a game is in progress
        And an effect exists that triggers when a player gains an action point
        When the Action Phase begins and the turn-player receives 1 action point
        Then the gain-action-point trigger does not fire for the action phase grant

    # Rule 4.3.2b - Replacement effects for gaining action points do not apply to action phase grant
    Scenario: Replacement effects for gaining action points do not apply to action phase grant
        Given a game is in progress
        And a replacement effect exists that modifies events when a player gains an action point
        When the Action Phase begins and the turn-player receives 1 action point
        Then the replacement effect does not modify the action phase action point grant

    # Rule 4.3.3 - Turn-player gains priority after receiving action point
    Scenario: Turn-player gains priority at the start of the action phase
        Given a game is in progress
        When the Action Phase begins
        Then the turn-player has priority

    # Rule 4.3.3 - Action Phase is the only phase when players get priority
    Scenario: The action phase is the only phase during which players get priority
        Given a game is in progress
        When the Action Phase is active
        Then players can get priority during the Action Phase

    # Rule 4.3.4 - Action phase ends when stack empty, chain closed, both players pass
    Scenario: Action phase ends when stack is empty, combat chain is closed, and both players pass priority
        Given a game is in progress
        And the stack is empty
        And the combat chain is closed
        When both players pass priority in succession
        Then the action phase ends

    # Rule 4.3.4 - Action phase proceeds to End Phase
    Scenario: Action phase proceeds to the End Phase when it ends
        Given a game is in progress
        And the action phase has ended
        When the action phase completes
        Then the game proceeds to the End Phase

    # Rule 4.3.4 - Action phase does not end if stack is not empty
    Scenario: Action phase does not end if the stack is not empty
        Given a game is in progress
        And the stack has layers on it
        And the combat chain is closed
        When both players attempt to pass priority
        Then the action phase does not end while the stack is not empty

    # Rule 4.3.4 - Action phase does not end if combat chain is not closed
    Scenario: Action phase does not end if the combat chain is not closed
        Given a game is in progress
        And the stack is empty
        And the combat chain is open
        When both players attempt to pass priority
        Then the action phase does not end while the combat chain is open

    # Rule 4.3 - Steps occur in the correct order
    Scenario: Action phase steps occur in the correct order
        Given a game is in progress
        And an effect exists that triggers at the beginning of the action phase
        When the Action Phase runs through its initial steps
        Then the beginning-of-action-phase event occurs before the action point is granted
        And the action point is granted before the turn-player gains priority
