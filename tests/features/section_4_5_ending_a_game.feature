# Feature file for Section 4.5: Ending a Game
# Reference: Flesh and Blood Comprehensive Rules Section 4.5
#
# 4.5.1 A game ends immediately when a player wins, or the game is a draw.
#
# 4.5.1a If a player loses a game, and the game does not end, all objects the player
#         controls are cleared, and then all objects owned by the player are removed from
#         the game. The player and their hero cease to exist for the remainder of the game.
#         Layer-continuous effects controlled by the player continue to exist until they expire.
#
# 4.5.2 A player can win the game in the following ways:
#
# 4.5.2a A player wins the game if all of their opponents have lost the game.
#
# 4.5.2b A player wins the game if an effect states that they win the game.
#
# 4.5.3 A player can lose the game in the following ways:
#
# 4.5.3a A player loses the game if their hero's life total is reduced to zero or they do
#         not control a hero.
#
# 4.5.3b A player loses the game if an effect states that they lose the game.
#
# 4.5.3c A player loses the game if they concede.
#
# 4.5.4 The game can be a draw for the remaining players in the following ways:
#
# 4.5.4a The game is a draw for the remaining players if all remaining players' hero's life
#         totals are simultaneously reduced to zero.
#
# 4.5.4b The game is a draw for the remaining players if an effect states that the game is
#         a draw.
#
# 4.5.4c The game is a draw for the remaining players if all remaining players agree to an
#         intentional draw. The remaining players can agree to a draw at any time.
#
# 4.5.4d The game is a draw for the remaining players if a stalemate occurs. A stalemate
#         happens when no remaining player can legally advance the game state toward ending
#         the game.
#
# 4.5.4e The game is a draw for the remaining players if a deadlock occurs. A deadlock
#         happens when all remaining players refuse to legally advance the game state toward
#         ending the game.

Feature: Section 4.5 - Ending a Game
    As a game engine
    I need to correctly implement game-ending conditions
    So that wins, losses, and draws are properly detected and applied

    # ===== Rule 4.5.1: Game ends immediately =====

    Scenario: Game ends immediately when a player wins
        Given a game with two players
        And player one's hero has 0 life
        When the game checks end conditions
        Then the game ends immediately
        And the result is not ongoing

    Scenario: Game ends immediately when the game is a draw
        Given a game with two players
        And both heroes are simultaneously reduced to 0 life
        When the game checks end conditions
        Then the game ends immediately
        And the result is a draw

    # ===== Rule 4.5.1a: Player loses but game continues (multiplayer) =====

    Scenario: Losing player's controlled objects are cleared when they lose in multiplayer
        Given a game with three players
        And player one controls an attack action card on the combat chain
        And player one controls a triggered layer on the stack
        When player one loses the game
        And the game has not ended because opponents remain
        Then player one's controlled objects are cleared
        And player one ceases to exist in the game

    Scenario: Losing player's owned objects are removed from the game
        Given a game with three players
        And player two controls a token owned by player one
        And player two controls a deck card owned by player one
        When player one loses the game
        And the game has not ended because opponents remain
        Then all objects owned by player one are removed from the game
        And player one's owned cards controlled by other players are removed

    Scenario: Layer-continuous effects controlled by losing player persist until expiry
        Given a game with three players
        And player one has a layer-continuous effect active on the stack
        When player one loses the game
        And the game has not ended because opponents remain
        Then the layer-continuous effect controlled by player one continues to exist
        And the effect remains until it expires naturally

    Scenario: Player and hero cease to exist after losing in multiplayer
        Given a game with three players
        And player one has a hero in the hero zone
        When player one loses the game
        And the game has not ended because opponents remain
        Then player one ceases to exist for the remainder of the game
        And player one's hero ceases to exist for the remainder of the game

    # ===== Rule 4.5.2a: Win by all opponents losing =====

    Scenario: Player wins when all opponents have lost
        Given a game with two players
        And player two's hero has 0 life
        When player two loses the game
        Then the game ends
        And player one wins the game

    Scenario: Player wins when last opponent loses in multiplayer
        Given a game with three players
        And player two has already lost the game
        And player three's hero has 0 life
        When player three loses the game
        Then player one wins the game
        And the game ends

    # ===== Rule 4.5.2b: Win by effect =====

    Scenario: Player wins when an effect states they win
        Given a game with two players
        And an effect states that player one wins the game
        When the effect resolves
        Then player one wins the game
        And the game ends immediately

    # ===== Rule 4.5.3a: Loss by hero life reaching zero =====

    Scenario: Player loses when hero life total is reduced to zero
        Given a game with two players
        And player one's hero has a life total of 20
        When player one's hero's life total is reduced to 0
        Then player one loses the game

    Scenario: Player loses when they do not control a hero
        Given a game with two players
        And player one does not control a hero
        When the game checks end conditions
        Then player one loses the game

    # ===== Rule 4.5.3b: Loss by effect =====

    Scenario: Player loses when an effect states they lose
        Given a game with two players
        And an effect states that player one loses the game
        When the effect resolves
        Then player one loses the game
        And player two wins the game

    # ===== Rule 4.5.3c: Loss by conceding =====

    Scenario: Player loses when they concede
        Given a game with two players
        When player one concedes the game
        Then player one loses the game
        And player two wins the game

    Scenario: Player can concede at any time
        Given a game with two players
        And it is currently player two's turn
        When player one concedes on player two's turn
        Then player one loses the game
        And player two wins the game

    # ===== Rule 4.5.4a: Draw by simultaneous life loss =====

    Scenario: Game is a draw when all remaining players' heroes simultaneously reach zero life
        Given a game with two players
        And both heroes have 1 life remaining
        When an effect simultaneously reduces both heroes' life totals to 0
        Then the game is a draw
        And neither player wins

    Scenario: Game is not a draw if life totals reach zero at different times
        Given a game with two players
        And player one's hero has 1 life
        And player two's hero has 2 life
        When player one's hero's life is reduced to 0 first
        Then player one loses the game
        And player two wins the game
        And the game is not a draw

    # ===== Rule 4.5.4b: Draw by effect =====

    Scenario: Game is a draw when an effect states the game is a draw
        Given a game with two players
        And an effect states that the game is a draw
        When the effect resolves
        Then the game is a draw
        And neither player wins

    # ===== Rule 4.5.4c: Intentional draw =====

    Scenario: Game is a draw when all remaining players agree to intentional draw
        Given a game with two players
        When both players agree to an intentional draw
        Then the game is a draw
        And neither player wins

    Scenario: Players can agree to intentional draw at any time
        Given a game with two players
        And it is currently the middle of the action phase
        When both players agree to an intentional draw during the action phase
        Then the game is a draw immediately

    # ===== Rule 4.5.4d: Stalemate =====

    Scenario: Game is a draw due to stalemate when no player can advance the game
        Given a game with two players
        And both players only have a Cracked Bauble in their hand
        And both players have no cards in deck, arsenal, or banished zone
        And both players control a weapon without an attack ability
        When the game state is evaluated for stalemate
        Then no player can legally advance the game state toward ending
        And the game is a draw by stalemate

    # ===== Rule 4.5.4e: Deadlock =====

    Scenario: Game is a draw due to deadlock when all players refuse to advance the game
        Given a game with two players on 1 life each
        And both players only have Invert Existence and a Cracked Bauble in their hand
        And both players have no equipment, weapon, or cards in deck, arsenal, or banished zone
        When all remaining players refuse to legally advance the game state
        Then the game is a draw by deadlock
