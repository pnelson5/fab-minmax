# Feature file for Section 4.1: Starting a Game
# Reference: Flesh and Blood Comprehensive Rules Section 4.1
#
# 4.1.1 The process of starting a game is referred to as the start-of-game procedure.
#        Players do not get priority during the start-of-game procedure.
#
# 4.1.2 First, each player places their hero card face up in their hero zone.
#
# 4.1.2a If the hero has a meta-static ability that modifies the start of game procedure,
#         the number zones, or the ownership of zones, or what cards are placed in zones,
#         that modification is independent of the ability during the game.
#         (e.g., Kayo, Underhanded Cheat has "You start the game with 1 weapon zone,"
#          even if Kayo loses that ability during the game, the player will not gain a weapon zone.)
#
# 4.1.3 Second, a player is selected and chooses the first-turn-player.
#        If first game: selected by random mutually agreeable method.
#        If not first game: player who lost first in previous game is selected player;
#        if previous game was a draw, same player as previous game is selected.
#        The selected player then chooses any player to be the first-turn-player.
#
# 4.1.4 Third, each player selects arena-cards from their card-pool that they will start the game with.
#
# 4.1.4a A player may select up to one arena-card for each of their arms, chest, head, legs,
#         and weapon zones. Each card will start equipped in its respective zone.
#
# 4.1.4b Cards selected this way are placed face-down in their respective zones or in a single
#         face-down pile next to the hero. These cards and their number are private until the game begins.
#
# 4.1.5 Fourth, each player selects the deck-cards from their card-pool that will become their deck.
#
# 4.1.5a Arena-cards cannot be included in a player's deck.
#
# 4.1.5b If a meta-static ability effect allows the player to start with one or more cards in a zone
#         other than their deck, these cards are selected from their deck and placed face-down.
#         The cards selected this way are still considered part of the player's deck.
#         (e.g., Dash: "You may start the game with a Mechanologist item with cost {r}{r} or less in the arena.")
#
# 4.1.6 Fifth, all other cards in a player's card-pool not selected in 4.1.4 or 4.1.5 become inventory.
#
# 4.1.6a An inventory is a defined collection of cards in the game - it is not a zone.
#
# 4.1.6b An inventory is private. Players may look at cards in their own inventory during a game
#         but are not required to show any other player.
#
# 4.1.6c If one or more cards remaining in the player's card-pool fail to meet the specifications
#         of a rule or effect at the start of the game, those cards are removed from the game
#         and are not considered part of the inventory for the game.
#         (e.g., Taylor: "Each equipment in your starting inventory must have a different name,"
#          duplicate-named equipment is removed from the game.)
#
# 4.1.7 Sixth, each player shuffles and presents their starting deck to an opponent to be shuffled/cut.
#
# 4.1.7a After presenting, the deck is placed in deck zone and players may no longer change chosen cards.
#
# 4.1.7b A starting deck is private. The opponent may not look at cards in a presented deck.
#
# 4.1.8 Seventh, each player in clockwise order equips weapons and equipment, starting with first-turn-player.
#        Any other cards starting in a zone other than deck are put in respective zones.
#        The "start of the game" event occurs and effects that trigger at start of game are triggered.
#        Layers on stack resolve and game state actions are performed as if all players pass priority.
#
# 4.1.8a If two or more triggered-layers are created, they are added to the stack in order chosen
#         by the first-turn-player.
#
# 4.1.8b If an effect would only trigger during a player's turn, it does not trigger during the
#         start-of-game procedure.
#
# 4.1.9 Eighth and finally, each player draws cards up to their hero's intellect and the
#        first-turn-player begins their Start Phase.

Feature: Section 4.1 - Starting a Game
    As a game engine
    I need to correctly implement the start-of-game procedure
    So that games begin with the correct initial state for all players

    # ===== Rule 4.1.1: No priority during start-of-game =====

    Scenario: Players do not get priority during the start-of-game procedure
        Given a new game is being initialized
        When the start-of-game procedure is in progress
        Then no player has priority
        And the game is in start-of-game procedure state

    # ===== Rule 4.1.2: Hero placed in hero zone =====

    Scenario: Hero card is placed face up in hero zone at game start
        Given a player has a hero card
        When the start-of-game procedure begins
        Then the hero card is placed face up in the player's hero zone

    # ===== Rule 4.1.2a: Meta-static zone modification is independent =====

    Scenario: Hero meta-static zone modification persists even if ability is lost
        Given a player's hero has a meta-static ability that modifies zone count at start of game
        When the start-of-game procedure applies the hero's meta-static zone modification
        Then the player's zones are modified as specified
        And the modification persists even if the hero card later loses the meta-static ability

    # ===== Rule 4.1.3: First-turn-player selection =====

    Scenario: First game uses random selection for first-turn-player
        Given it is the first game of the match
        When the first-turn-player is being determined
        Then a player is selected using a random method
        And the selected player chooses who goes first

    Scenario: Subsequent game loser selects first-turn-player
        Given it is not the first game of the match
        And a player lost the previous game first
        When the first-turn-player is being determined
        Then the player who lost first in the previous game is the selected player
        And that player chooses who will be the first-turn-player

    Scenario: Draw game uses same selected player as previous game
        Given it is not the first game of the match
        And the previous game ended in a draw
        When the first-turn-player is being determined
        Then the same player as in the previous game is the selected player

    # ===== Rule 4.1.4a: Arena-card limits per zone =====

    Scenario: Player may select at most one arena-card per equipment zone
        Given a player has multiple equipment cards in their card-pool
        When the player selects arena-cards for the start-of-game procedure
        Then the player may select at most one card per arms zone
        And the player may select at most one card per chest zone
        And the player may select at most one card per head zone
        And the player may select at most one card per legs zone
        And the player may select at most one card per weapon zone

    # ===== Rule 4.1.4b: Arena-cards are face-down and private =====

    Scenario: Arena-cards are placed face-down and remain private until game begins
        Given a player has selected arena-cards for the start-of-game procedure
        When the arena-card selection is submitted
        Then the selected cards are placed face-down
        And the number of selected arena-cards is private to the selecting player

    # ===== Rule 4.1.5a: Arena-cards cannot be in deck =====

    Scenario: Arena-cards cannot be included in a player's deck
        Given a player has equipment cards in their card-pool
        When the player selects deck-cards from their card-pool
        Then equipment arena-cards may not be included in the deck selection

    # ===== Rule 4.1.5b: Meta-static allows non-deck starting cards =====

    Scenario: Meta-static ability allows starting with cards outside the deck zone
        Given a player's hero has a meta-static ability allowing a card to start in a non-deck zone
        When the player selects their starting cards
        Then the player may place the specified card in the non-deck zone
        And that card is still considered part of the player's deck

    # ===== Rule 4.1.6 / 4.1.6a / 4.1.6b: Inventory =====

    Scenario: Cards not selected as arena-cards or deck-cards become the player's inventory
        Given a player has a card-pool with more cards than their deck and arena selections
        When the deck and arena-card selections are complete
        Then the remaining cards become the player's inventory
        And the inventory is not a zone

    Scenario: Inventory is private to the owning player
        Given a player has an inventory at the start of a game
        When an opponent attempts to view the player's inventory
        Then the inventory contents are private and not revealed to the opponent
        And the player may view their own inventory

    # ===== Rule 4.1.6c: Cards failing specs removed =====

    Scenario: Cards failing start-of-game specifications are removed from the game
        Given a player's hero has a rule restricting which cards may be in the inventory
        And the player's card-pool contains cards that violate the restriction
        When the start-of-game procedure evaluates the inventory
        Then the violating cards are removed from the game
        And the removed cards are not part of the player's inventory

    # ===== Rule 4.1.7a: Deck lock after presentation =====

    Scenario: Deck selections are locked after presenting to opponent
        Given a player has presented their starting deck to an opponent
        When the deck has been placed in the deck zone
        Then the player may no longer change their arena-card or deck-card selections

    # ===== Rule 4.1.8: Equip weapons and equipment, start-of-game event =====

    Scenario: Equipment is equipped in clockwise order starting with first-turn-player
        Given a game has determined the first-turn-player
        And players have arena-card selections ready
        When equipment is equipped during the start-of-game procedure
        Then the first-turn-player equips their weapons and equipment first
        And then other players equip in clockwise order

    Scenario: Start of game event triggers at-start-of-game effects
        Given a game is completing the start-of-game procedure
        When the start-of-game event occurs
        Then effects that trigger at start of game are triggered
        And triggered layers are resolved with no player having priority

    # ===== Rule 4.1.8a: First-turn-player orders triggered layers =====

    Scenario: First-turn-player orders multiple start-of-game triggered layers
        Given two or more effects trigger at the start of the game
        When the triggered layers are added to the stack
        Then the first-turn-player chooses the order in which they are added

    # ===== Rule 4.1.8b: Turn-dependent triggers do not fire during start-of-game =====

    Scenario: Effects that only trigger during a player's turn do not trigger during start-of-game
        Given a player controls an effect that would trigger "the first time each turn" something happens
        When that something happens during the start-of-game procedure
        Then the effect does not trigger because it is not during a player's turn

    # ===== Rule 4.1.9: Initial hand draw =====

    Scenario: Each player draws cards up to their hero's intellect to start the game
        Given all start-of-game procedure steps are complete
        When the game transitions to the first turn
        Then each player draws cards from their deck equal to their hero's intellect
        And the first-turn-player begins their Start Phase
