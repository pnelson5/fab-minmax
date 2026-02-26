# Feature file for Section 1.10: Game State
# Reference: Flesh and Blood Comprehensive Rules Section 1.10
#
# Rule 1.10.1: A game state is a moment in the game. The game transitions between
# states when an event occurs (1.9). A priority state is a game state where a player
# would typically receive priority.
#
# Rule 1.10.2: When the game transitions to a new priority state, the following game
# state actions are performed first:
#   (a) First, if one or more heroes have died, their player loses the game (or draw).
#   (b) Second, if one or more living objects in the arena have 0 life total, they are
#       cleared simultaneously as a single event.
#   (c) Third, if a continuous effect allows a player to look at a card based on
#       location, they may start looking at it.
#   (d) Fourth, if the state-condition of a state-based triggered effect is met, the
#       effect triggers. Triggered-layers are then added to the stack.
#   (e) Fifth, if the combat chain is open and a rule or effect has closed it,
#       the Close Step begins.
#
# Rule 1.10.3: If a player makes an illegal action, or starts an action that becomes
# illegal, the game state is reversed to the legal state before that action.
#   (a) Triggered effects do not trigger as a result of the reversal.
#   (b) Replacement effects cannot replace any event from the reversal.
#   (c) If reversal is impossible, as much as possible is reversed and the game
#       continues as though it were the last legal state before the reversal.

Feature: Section 1.10 - Game State
    As a game engine
    I need to correctly implement game state transitions and reversal
    So that game state actions and illegal action handling work correctly

    # ============================================================
    # Rule 1.10.1: Game State and Priority State Concepts
    # ============================================================

    # Test for Rule 1.10.1 - Game state is a moment in the game
    Scenario: game state exists as a discrete moment
        Given a game is in progress
        When the game is in a stable state
        Then the game state can be captured as a snapshot
        And the snapshot represents a single moment in the game

    # Test for Rule 1.10.1 - Priority state is where a player receives priority
    Scenario: priority state is a game state where player receives priority
        Given a game is in the action phase
        When the game transitions to a new priority state
        Then the active player has priority
        And the state is identified as a priority state

    # Test for Rule 1.10.1 - Non-priority state does not give priority to any player
    Scenario: non-priority game state has no player with priority
        Given a game is in progress
        When the game is performing game state actions
        Then no player has priority during game state actions

    # ============================================================
    # Rule 1.10.2: Game State Actions on Priority State Transitions
    # ============================================================

    # Test for Rule 1.10.2a - Hero death check is first game state action
    Scenario: hero with zero life causes player to lose when priority state is reached
        Given a game is in progress
        And player 0's hero has 0 life
        When the game transitions to a new priority state
        Then game state action 1 checks for dead heroes
        And player 0 loses the game

    # Test for Rule 1.10.2a - Hero death draw condition
    Scenario: all heroes die simultaneously results in draw
        Given a game is in progress
        And player 0's hero has 0 life
        And player 1's hero has 0 life
        When the game transitions to a new priority state
        Then the game ends in a draw

    # Test for Rule 1.10.2b - Living objects cleared at 0 life
    Scenario: living object with zero life is cleared in second game state action
        Given a game is in progress
        And a living permanent with 0 life is in the arena
        When the game transitions to a new priority state
        Then game state action 2 clears living objects with 0 life
        And the living permanent is removed from the arena

    # Test for Rule 1.10.2b - Multiple living objects cleared simultaneously
    Scenario: multiple living objects with zero life are cleared simultaneously
        Given a game is in progress
        And two living permanents each with 0 life are in the arena
        When the game transitions to a new priority state
        Then both living permanents are cleared simultaneously as a single event

    # Test for Rule 1.10.2b - Hero with 0 life is checked by 1.10.2a, not 1.10.2b
    Scenario: hero at zero life triggers player loss not living object clearing
        Given a game is in progress
        And player 0's hero has 0 life
        When the game transitions to a new priority state
        Then the hero death is handled by game state action 1
        And not by game state action 2

    # Test for Rule 1.10.2c - Continuous look effect starts when entering priority state
    Scenario: continuous look effect activates during third game state action
        Given a game is in progress
        And player 0 has a continuous effect allowing them to look at the top card of their deck
        When the game transitions to a new priority state
        Then game state action 3 starts the look effect
        And player 0 may look at the top card of their deck

    # Test for Rule 1.10.2d - State-based triggered effects fire in fourth game state action
    Scenario: state-based triggered effect fires when condition is met
        Given a game is in progress
        And a state-based triggered effect has its condition met
        When the game transitions to a new priority state
        Then game state action 4 fires the state-based triggered effect
        And the triggered layer is added to the stack

    # Test for Rule 1.10.2d - Multiple triggered layers added in clockwise order
    Scenario: multiple triggered layers added to stack in clockwise order from turn player choice
        Given a game is in progress
        And player 0 has a triggered layer waiting to be added
        And player 1 has a triggered layer waiting to be added
        When the game transitions to a new priority state
        Then the triggered layers are added in clockwise order starting from turn player's choice

    # Test for Rule 1.10.2e - Combat chain closing is fifth game state action
    Scenario: open combat chain closed by effect begins close step
        Given a game is in progress
        And the combat chain is open
        And an effect has closed the combat chain
        When the game transitions to a new priority state
        Then game state action 5 begins the close step of combat

    # Test for Rule 1.10.2e - No close step if combat chain is not open
    Scenario: no close step when combat chain is not open
        Given a game is in progress
        And the combat chain is not open
        When the game transitions to a new priority state
        Then game state action 5 does not begin the close step

    # Test for Rule 1.10.2 - Game state actions performed in order
    Scenario: game state actions are performed in the correct order
        Given a game is in progress
        And player 0's hero has 0 life
        And a living permanent with 0 life is in the arena
        When the game transitions to a new priority state
        Then game state actions are performed in order 1 through 5
        And hero death check is performed before living object clearing

    # ============================================================
    # Rule 1.10.3: Illegal Action Reversal
    # ============================================================

    # Test for Rule 1.10.3 - Illegal action reverses game state
    Scenario: illegal action reverses game state to before it started
        Given a game state before an action is taken
        When a player makes an illegal action
        Then the game state is reversed to before the illegal action
        And the game state is the same as before the action

    # Test for Rule 1.10.3 - Action that becomes illegal mid-completion is reversed
    Scenario: action becoming illegal mid-completion is reversed
        Given a game state before an action is taken
        When a player starts an action that becomes illegal to complete
        Then the game state is reversed to before the action started

    # Test for Rule 1.10.3a - Triggered effects do not fire during reversal
    Scenario: triggered effects do not trigger during game state reversal
        Given a game state with a triggered effect registered
        When the game state is reversed due to an illegal action
        Then the triggered effect does not fire
        And the triggered effect trigger count is still 0

    # Test for Rule 1.10.3b - Replacement effects cannot replace reversal events
    Scenario: replacement effects cannot modify reversal events
        Given a game state with a replacement effect registered
        When the game state is reversed due to an illegal action
        Then the replacement effect does not modify any event during the reversal
        And the reversal proceeds unchanged

    # Test for Rule 1.10.3c - If full reversal impossible, reverse as much as possible
    Scenario: partial reversal when full reversal is impossible
        Given a game state that cannot be fully reversed
        When the game state reversal is attempted
        Then as much as possible about the state is reversed
        And the game continues as though it were the last legal state

    # Test for Rule 1.10.3 - Playing unplayable card is reversed
    Scenario: attempting to play an unplayable card reverses game state
        Given a player has a card they cannot legally play
        When the player attempts to play that card
        Then the play attempt is reversed
        And the card remains where it started

    # Test for Rule 1.10.3 - Paying cost then failing legality check reverses full action
    Scenario: paying cost then failing legality check reverses entire action
        Given a player has a card with a cost
        When the player pays the cost and then the play is found to be illegal
        Then the full action including cost payment is reversed
        And the player's resources are restored
