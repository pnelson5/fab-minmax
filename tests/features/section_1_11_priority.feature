# Feature file for Section 1.11: Priority
# Reference: Flesh and Blood Comprehensive Rules Section 1.11
#
# Rule 1.11.1: Priority is a game state concept that describes which player
#   (if any) may play a card, activate an ability, or pass priority to
#   the next player.
#
# Rule 1.11.2: Only one player can have priority at any point in time.
#   A player who has priority is the "active player."
#   A player who does not have priority is an "inactive player."
#
# Rule 1.11.3: The Action Phase is the only phase when players get priority.
#   Within the action phase, players do not get priority during the Close Step
#   of combat. At the beginning of the action phase, during most steps of
#   combat, and after the resolution of a layer, the turn-player gains priority.
#
# Rule 1.11.4: The active player may pass priority to the next player,
#   referred to as "pass."
#
# Rule 1.11.4a: If a player passes, priority is given to the next player in
#   clockwise order. Typically, if all players pass in succession without
#   playing any cards or activating any abilities, and the stack is not empty,
#   the top layer of the stack resolves - otherwise if the stack is empty,
#   the phase or step ends.
#
# Rule 1.11.5: If the active player plays a card or activates an ability, they
#   regain priority after the card has been played or the ability has been
#   activated. If the active player passes, they lose priority until they
#   receive it again from a rule. No player has priority while playing a card,
#   activating an ability, resolving a layer, during a game process, and/or
#   during game state actions.

Feature: Section 1.11 - Priority
    As a game engine
    I need to correctly implement the priority system
    So that players take turns playing cards and activating abilities in the correct order

    # Test for Rule 1.11.1 - Priority describes which player may act
    Scenario: priority is a game state concept describing who may play
        Given a game with two players in the action phase
        When the priority system is active
        Then priority describes which player may play a card or activate an ability
        And priority describes which player may pass priority to the next player

    # Test for Rule 1.11.2 - Only one player has priority at a time
    Scenario: only one player can have priority at any time
        Given a game with two players in the action phase
        When the turn player has priority
        Then exactly one player has priority
        And the other player does not have priority

    # Test for Rule 1.11.2 - Active vs inactive player distinction
    Scenario: the player with priority is the active player
        Given a game with two players in the action phase
        When the turn player has priority
        Then the player with priority is called the active player
        And the player without priority is called the inactive player

    # Test for Rule 1.11.3 - Priority only in action phase
    Scenario: priority only exists during the action phase
        Given a game with two players
        When the game is in the start phase
        Then no player has priority

    # Test for Rule 1.11.3 - Priority exists during action phase
    Scenario: turn player gains priority at start of action phase
        Given a game with two players
        When the game enters the action phase
        Then the turn player has priority

    # Test for Rule 1.11.3 - No priority during Close Step
    Scenario: no priority during close step of combat
        Given a game with two players in the action phase
        And the combat chain is open
        When the close step begins
        Then no player has priority during the close step

    # Test for Rule 1.11.3 - Turn player gains priority during combat steps
    Scenario: turn player gains priority during combat steps
        Given a game with two players
        And the game is in the action phase
        When the attack step begins
        Then the turn player has priority

    # Test for Rule 1.11.3 - Turn player gains priority after layer resolves
    Scenario: turn player gains priority after layer resolution
        Given a game with two players in the action phase
        And a card is on the stack
        When the top layer resolves
        Then the turn player gains priority

    # Test for Rule 1.11.4 - Active player may pass priority
    Scenario: active player may pass priority
        Given a game with two players in the action phase
        And the turn player has priority
        When the active player passes priority
        Then the active player no longer has priority
        And the next player in clockwise order has priority

    # Test for Rule 1.11.4a - Priority passes clockwise
    Scenario: priority passes clockwise to next player
        Given a game with three players in the action phase
        And player 0 has priority
        When player 0 passes priority
        Then player 1 has priority

    # Test for Rule 1.11.4a - Clockwise wraps from last to first
    Scenario: priority passes clockwise from last player back to first
        Given a game with three players in the action phase
        And player 2 has priority
        When player 2 passes priority
        Then player 0 has priority

    # Test for Rule 1.11.4a - All pass with non-empty stack resolves top layer
    Scenario: all players passing with non-empty stack resolves top layer
        Given a game with two players in the action phase
        And a card is on the stack
        When all players pass priority in succession without playing cards or activating abilities
        Then the top layer of the stack resolves

    # Test for Rule 1.11.4a - All pass with empty stack ends phase or step
    Scenario: all players passing with empty stack ends phase or step
        Given a game with two players in the action phase
        And the stack is empty
        When all players pass priority in succession without playing cards or activating abilities
        Then the current phase or step ends

    # Test for Rule 1.11.5 - Active player regains priority after playing a card
    Scenario: active player regains priority after playing a card
        Given a game with two players in the action phase
        And the turn player has priority
        When the active player plays a card
        Then the active player regains priority after the card is played

    # Test for Rule 1.11.5 - Active player regains priority after activating an ability
    Scenario: active player regains priority after activating an ability
        Given a game with two players in the action phase
        And the turn player has priority
        When the active player activates an ability
        Then the active player regains priority after the ability is activated

    # Test for Rule 1.11.5 - Active player loses priority after passing
    Scenario: active player loses priority after passing
        Given a game with two players in the action phase
        And the turn player has priority
        When the active player passes priority
        Then the active player loses priority

    # Test for Rule 1.11.5 - No priority while playing a card
    Scenario: no player has priority while a card is being played
        Given a game with two players in the action phase
        And the turn player has priority
        When a card is in the process of being played
        Then no player has priority during card play

    # Test for Rule 1.11.5 - No priority while resolving a layer
    Scenario: no player has priority while a layer is resolving
        Given a game with two players in the action phase
        And a card is on the stack
        When the top layer is in the process of resolving
        Then no player has priority during resolution

    # Test for Rule 1.11.5 - No priority during game state actions
    Scenario: no player has priority during game state actions
        Given a game with two players
        When game state actions are being performed
        Then no player has priority during game state actions
