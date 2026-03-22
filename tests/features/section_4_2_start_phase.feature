# Feature file for Section 4.2: Start Phase
# Reference: Flesh and Blood Comprehensive Rules Section 4.2
#
# 4.2.1 Players do not get priority during the Start Phase.
#
# 4.2.2 First, the turn starts. Effects that last until the "start of turn" end.
#       The "start of turn" event occurs and effects that trigger at the start of turn
#       are triggered. Layers on the stack resolve and game state actions are performed
#       as if all players are passing priority in succession until the stack is empty.
#       [1.10.2]
#
# 4.2.3 Second and finally, the Start Phase ends and the game proceeds to the action phase.

Feature: Section 4.2 - Start Phase
    As a game engine
    I need to correctly implement the Start Phase
    So that turn-start events fire, effects expire, and the game proceeds to the Action Phase

    # Rule 4.2.1 - No priority during Start Phase
    Scenario: Players do not get priority during the Start Phase
        Given a game is in progress
        And it is the beginning of the Start Phase
        When the Start Phase is active
        Then no player has priority during the Start Phase

    # Rule 4.2.1 - Players cannot take priority-based actions during Start Phase
    Scenario: Players cannot take game actions during the Start Phase
        Given a game is in progress
        And it is the beginning of the Start Phase
        When the Start Phase is active
        Then the turn player cannot play a card during the Start Phase
        And the non-turn player cannot play a card during the Start Phase

    # Rule 4.2.2 - Effects lasting "until start of turn" end
    Scenario: Effects lasting until start of turn expire when the turn starts
        Given a game is in progress
        And an effect is active that lasts until the "start of turn"
        When the Start Phase begins and the turn starts
        Then the "until start of turn" effect ends

    # Rule 4.2.2 - Effects lasting "until start of turn" end before triggers fire
    Scenario: Multiple until-start-of-turn effects all expire when the turn starts
        Given a game is in progress
        And multiple effects are active that last until the "start of turn"
        When the Start Phase begins and the turn starts
        Then all "until start of turn" effects end

    # Rule 4.2.2 - The "start of turn" event occurs
    Scenario: The start of turn event occurs during the Start Phase
        Given a game is in progress
        When the Start Phase begins
        Then the "start of turn" event occurs

    # Rule 4.2.2 - Effects that trigger at start of turn are triggered
    Scenario: Effects that trigger at start of turn fire during the Start Phase
        Given a game is in progress
        And an effect exists that triggers at the start of turn
        When the Start Phase begins and the turn starts
        Then the start-of-turn triggered effect is added to the stack

    # Rule 4.2.2 - Multiple start-of-turn triggers all fire
    Scenario: Multiple start-of-turn triggered effects all fire during Start Phase
        Given a game is in progress
        And multiple effects exist that trigger at the start of turn
        When the Start Phase begins and the turn starts
        Then all start-of-turn triggered effects are added to the stack

    # Rule 4.2.2 - Stack resolves as if all players pass priority
    Scenario: Start-of-turn triggered layers resolve automatically without player priority
        Given a game is in progress
        And a triggered effect fires at the start of turn
        When the Start Phase processes the stack
        Then the stack resolves as if all players are passing priority in succession
        And the stack is empty after the Start Phase processes it

    # Rule 4.2.2 - Stack must be empty before Start Phase can end
    Scenario: Start Phase does not end until the stack is empty
        Given a game is in progress
        And multiple triggered effects fire at the start of turn
        When the Start Phase processes the stack
        Then all layers resolve before the Start Phase ends
        And the stack is empty when the Start Phase ends

    # Rule 4.2.3 - Start Phase ends and game proceeds to Action Phase
    Scenario: Start Phase ends and game proceeds to the Action Phase
        Given a game is in progress
        And the Start Phase has completed its steps
        When the Start Phase ends
        Then the game proceeds to the Action Phase

    # Rule 4.2.3 - Correct ordering: until-start-of-turn expires, then event, then triggers, then Action Phase
    Scenario: Start Phase steps occur in the correct order
        Given a game is in progress
        And an effect is active that lasts until the "start of turn"
        And an effect exists that triggers at the start of turn
        When the Start Phase runs completely
        Then the "until start of turn" effect ends before the start of turn event
        And the start-of-turn triggered effect fires after the turn starts
        And the game proceeds to the Action Phase after the stack is empty
