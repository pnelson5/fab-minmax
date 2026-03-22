# Feature file for Section 4.0: General (Game Structure)
# Reference: Flesh and Blood Comprehensive Rules Section 4.0
#
# 4.0.1 A game of Flesh and Blood is preceded by the start-of-game procedure
#        and ends when a player wins or the game is a draw. [4.1][4.5]
#
# 4.0.2 A match consists of one or more consecutive games between the same
#        players with the same decks.
#
# 4.0.3 A turn is a game state concept that structures the order of play and phases.
#
# 4.0.3a A turn consists of 3 phases in order: Start Phase, Action Phase, and
#         End Phase.
#
# 4.0.3b Only one player can have a turn at any point in time. A player whose
#         turn it is is the "turn-player." A player whose turn it is not is a
#         "non-turn-player."
#
# 4.0.3c If an effect would give a player an extra turn, it is taken immediately
#         after the specified turn.

Feature: Section 4.0 - Game Structure General
    As a game engine
    I need to correctly model the high-level game structure rules
    So that turn sequencing, match structure, and game lifecycle work correctly

    # ===== Rule 4.0.1: Game lifecycle =====

    # Test for Rule 4.0.1 - A game is preceded by the start-of-game procedure
    Scenario: A game begins with the start-of-game procedure
        Given a new game is being set up
        When the game initializes
        Then the start-of-game procedure precedes normal gameplay
        And players do not have a turn during the start-of-game procedure

    # Test for Rule 4.0.1 - A game ends when a player wins
    Scenario: A game ends when a player wins
        Given a game is in progress
        When a win condition is met for a player
        Then the game ends
        And the winning player is recorded

    # Test for Rule 4.0.1 - A game can end in a draw
    Scenario: A game can end in a draw
        Given a game is in progress
        When a draw condition is met
        Then the game ends as a draw
        And no player is recorded as the winner

    # ===== Rule 4.0.2: Match structure =====

    # Test for Rule 4.0.2 - A match has one or more games
    Scenario: A match consists of one or more consecutive games
        Given a match between two players is initialized
        When the first game of the match concludes
        Then the match may continue with another game between the same players
        And the same decks are used in consecutive games of the match

    # ===== Rule 4.0.3: Turn structure =====

    # Test for Rule 4.0.3 - A turn is a game state concept
    Scenario: A turn is a game state concept that tracks whose turn it is
        Given a game is in progress
        When checking the game state for turn information
        Then the game state tracks which player's turn it is
        And the game state tracks the current phase

    # Test for Rule 4.0.3a - A turn has exactly 3 phases in order
    Scenario: A turn consists of Start Phase, Action Phase, and End Phase in order
        Given a game is in progress with a current turn
        When the turn's phases are enumerated
        Then the first phase is the Start Phase
        And the second phase is the Action Phase
        And the third phase is the End Phase
        And there are exactly 3 phases in a turn

    # Test for Rule 4.0.3a - Phases must occur in the correct order
    Scenario: Turn phases cannot be skipped or reordered
        Given a game is in progress with a current turn
        When the Action Phase is active
        Then the Start Phase has already occurred
        And the End Phase has not yet occurred

    # ===== Rule 4.0.3b: Turn-player and non-turn-player =====

    # Test for Rule 4.0.3b - Only one player has a turn at a time
    Scenario: Only one player can have a turn at any point in time
        Given a game is in progress with two players
        When it is player one's turn
        Then player one is the turn-player
        And player two is a non-turn-player
        And exactly one player is the turn-player

    # Test for Rule 4.0.3b - Turn-player designation changes each turn
    Scenario: The turn-player designation alternates between players
        Given a game is in progress with two players
        When player one's turn ends
        Then player two becomes the turn-player
        And player one becomes a non-turn-player

    # ===== Rule 4.0.3c: Extra turns =====

    # Test for Rule 4.0.3c - Extra turns are taken immediately after specified turn
    Scenario: An extra turn is taken immediately after the specified turn
        Given a game is in progress with player one as the turn-player
        When an effect grants player one an extra turn after the current turn
        Then player one will take an extra turn immediately after their current turn
        And the extra turn occurs before any other player's next turn

    # Test for Rule 4.0.3c - Extra turn from effect targets specific turn
    Scenario: An extra turn effect specifies which turn it follows
        Given a game is in progress with two players
        When an effect grants player two an extra turn after player one's current turn
        Then player two's extra turn is taken immediately after player one's current turn
        And the normal turn order resumes after the extra turn
