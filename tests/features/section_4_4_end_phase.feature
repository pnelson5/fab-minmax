# Feature file for Section 4.4: End Phase
# Reference: Flesh and Blood Comprehensive Rules Section 4.4
#
# 4.4.1 Players do not get priority during the End Phase.
#
# 4.4.2 First, the "beginning of the end phase" event occurs and effects that trigger
#        at the beginning of the end phase are triggered. Layers on the stack resolve
#        and game state actions are performed as if all players are passing priority in
#        succession until the stack is empty.
#
# 4.4.3 Second, the end-of-turn procedure occurs. After each step in the end-of-turn
#        procedure, if a triggered effect has triggered, the triggered-layers are added
#        to the stack; then layers on the stack resolve and game state actions are
#        performed as if all players are passing priority in succession until the stack
#        is empty. The end-of-turn procedure happens in the following order:
#
# 4.4.3a All allies' life totals are reset to their base life, modified by any counters
#         on the object.
#
# 4.4.3b The turn-player may put a card from their hand face-down into an empty arsenal
#         zone they own.
#
# 4.4.3c Each player puts all cards in their pitch zone (if any) on the bottom of their
#         deck in any order. The order cards are put on the bottom of the deck this way
#         is hidden information.
#
# 4.4.3d The turn-player uptaps all permanents they control.
#
# 4.4.3e All players lose all action points and resource points.
#
# 4.4.3f The turn-player draws cards until the number of cards in their hand is equal
#         to their hero's intellect. If it is the first turn of the game, all other
#         players draw cards until the number of cards in their hand is equal to their
#         hero's intellect. If a player already has at least that many cards in their
#         hand, they do not draw any cards this way.
#
# 4.4.4 Third and finally, the turn ends. Effects that last "until end of turn" and
#        "this turn" end. The next player in clockwise order becomes the new turn-player.
#        The new turn-player begins their Start Phase.

Feature: Section 4.4 - End Phase
    As a game engine
    I need to correctly implement the End Phase
    So that end-of-turn procedures execute in order and turn transitions occur properly

    # Rule 4.4.1 - No priority during End Phase
    Scenario: Players do not get priority during the End Phase
        Given a game is in progress
        When the End Phase begins
        Then no player gets priority during the End Phase

    # Rule 4.4.2 - Beginning of end phase event occurs
    Scenario: The beginning of end phase event occurs when End Phase starts
        Given a game is in progress
        When the End Phase begins
        Then the "beginning of the end phase" event occurs

    # Rule 4.4.2 - Triggered effects at beginning of end phase fire
    Scenario: Effects that trigger at the beginning of the end phase are triggered
        Given a game is in progress
        And an effect exists that triggers at the beginning of the end phase
        When the End Phase begins
        Then the beginning-of-end-phase triggered effect fires

    # Rule 4.4.2 - Stack resolves before end-of-turn procedure
    Scenario: The stack resolves before the end-of-turn procedure
        Given a game is in progress
        And an effect exists that triggers at the beginning of the end phase
        When the End Phase begins
        Then the triggered effect resolves before the end-of-turn procedure begins

    # Rule 4.4.3 - End-of-turn procedure occurs after beginning-of-end-phase triggers resolve
    Scenario: End-of-turn procedure occurs after beginning-of-end-phase triggers resolve
        Given a game is in progress
        When the End Phase begins
        Then the end-of-turn procedure occurs after the stack is empty

    # Rule 4.4.3 - Triggered effects after each step are added to the stack and resolved
    Scenario: Triggered effects after each end-of-turn step are resolved before next step
        Given a game is in progress
        And an effect triggers during the end-of-turn procedure
        When a step in the end-of-turn procedure completes
        Then any triggered layers are added to the stack and resolved before the next step

    # Rule 4.4.3a - Allies' life totals reset to base life
    Scenario: Allies' life totals are reset to their base life at end of turn
        Given a game is in progress
        And the turn-player controls an ally with reduced life
        When the end-of-turn procedure step 3a executes
        Then the ally's life total is reset to its base life

    # Rule 4.4.3a - Ally life reset is modified by counters
    Scenario: Allies' life reset is modified by counters on the ally
        Given a game is in progress
        And the turn-player controls an ally with +1 counter and reduced life
        When the end-of-turn procedure step 3a executes
        Then the ally's life total is reset to its base life modified by the counter

    # Rule 4.4.3a - Non-ally permanents are NOT reset
    Scenario: Non-ally permanents do not have life reset during end of turn
        Given a game is in progress
        And the turn-player controls a non-ally permanent
        When the end-of-turn procedure step 3a executes
        Then the non-ally permanent is not affected by the life reset step

    # Rule 4.4.3b - Turn-player may put a card face-down into empty arsenal
    Scenario: Turn-player may put a card face-down into an empty arsenal zone
        Given a game is in progress
        And the turn-player has a card in hand
        And the turn-player's arsenal zone is empty
        When the end-of-turn procedure step 3b executes
        Then the turn-player may put a card from hand face-down into their arsenal

    # Rule 4.4.3b - Arsenal zone must be empty for turn-player to store card
    Scenario: Turn-player cannot put a card into a non-empty arsenal during end of turn
        Given a game is in progress
        And the turn-player has a card in hand
        And the turn-player's arsenal zone is not empty
        When the end-of-turn procedure step 3b executes
        Then the turn-player cannot put a card into their arsenal this way

    # Rule 4.4.3b - Arsenal card is placed face-down
    Scenario: Card placed into arsenal during end of turn is face-down
        Given a game is in progress
        And the turn-player has a card in hand
        And the turn-player's arsenal zone is empty
        When the turn-player places a card into their arsenal during end-of-turn step 3b
        Then the card in the arsenal is face-down

    # Rule 4.4.3c - Pitch zone cards go to bottom of deck
    Scenario: Each player puts pitch zone cards on the bottom of their deck at end of turn
        Given a game is in progress
        And one or more cards are in the turn-player's pitch zone
        When the end-of-turn procedure step 3c executes
        Then those cards are moved to the bottom of the turn-player's deck

    # Rule 4.4.3c - Pitch zone cards go in any order
    Scenario: Order of pitch zone cards going to bottom of deck is player's choice
        Given a game is in progress
        And multiple cards are in the turn-player's pitch zone
        When the end-of-turn procedure step 3c executes
        Then the player chooses the order those cards go to the bottom of their deck

    # Rule 4.4.3c - Order of pitch zone cards is hidden information
    Scenario: Order of pitch zone cards placed on bottom of deck is hidden information
        Given a game is in progress
        And multiple cards are in the turn-player's pitch zone
        When the end-of-turn procedure step 3c executes
        Then the order in which cards are placed on the bottom of the deck is hidden information

    # Rule 4.4.3c - Non-turn players also move pitch cards to deck
    Scenario: Non-turn players also move their pitch zone cards to the bottom of their deck
        Given a game is in progress
        And one or more cards are in the non-turn-player's pitch zone
        When the end-of-turn procedure step 3c executes
        Then the non-turn player's pitch zone cards move to the bottom of their deck

    # Rule 4.4.3d - Turn-player untaps all their permanents
    Scenario: Turn-player untaps all permanents they control at end of turn
        Given a game is in progress
        And the turn-player controls one or more tapped permanents
        When the end-of-turn procedure step 3d executes
        Then all those permanents become untapped

    # Rule 4.4.3d - Only turn-player's permanents are untapped
    Scenario: Only the turn-player's permanents are untapped, not the opponent's
        Given a game is in progress
        And the turn-player controls a tapped permanent
        And the non-turn-player controls a tapped permanent
        When the end-of-turn procedure step 3d executes
        Then the turn-player's permanent becomes untapped
        And the non-turn-player's permanent remains tapped

    # Rule 4.4.3e - All players lose all action points and resource points
    Scenario: All players lose all action points at end of turn
        Given a game is in progress
        And one or more players have action points
        When the end-of-turn procedure step 3e executes
        Then all players have zero action points

    # Rule 4.4.3e - All players lose all resource points
    Scenario: All players lose all resource points at end of turn
        Given a game is in progress
        And one or more players have resource points
        When the end-of-turn procedure step 3e executes
        Then all players have zero resource points

    # Rule 4.4.3f - Turn-player draws to intellect
    Scenario: Turn-player draws cards up to their hero's intellect at end of turn
        Given a game is in progress
        And the turn-player has fewer cards in hand than their hero's intellect
        When the end-of-turn procedure step 3f executes
        Then the turn-player draws cards until their hand size equals their hero's intellect

    # Rule 4.4.3f - Turn-player does not draw if hand already at intellect
    Scenario: Turn-player does not draw if hand already has at least intellect cards
        Given a game is in progress
        And the turn-player has cards in hand equal to or more than their hero's intellect
        When the end-of-turn procedure step 3f executes
        Then the turn-player does not draw any cards

    # Rule 4.4.3f - Non-turn players draw on first turn of game only
    Scenario: Non-turn players draw to intellect only on the first turn of the game
        Given it is the first turn of the game
        And a non-turn player has fewer cards in hand than their hero's intellect
        When the end-of-turn procedure step 3f executes
        Then the non-turn player draws cards until their hand size equals their hero's intellect

    # Rule 4.4.3f - Non-turn players do NOT draw on subsequent turns
    Scenario: Non-turn players do not draw on turns other than the first turn
        Given it is not the first turn of the game
        And a non-turn player has fewer cards in hand than their hero's intellect
        When the end-of-turn procedure step 3f executes
        Then the non-turn player does not draw any cards

    # Rule 4.4.4 - "Until end of turn" effects expire
    Scenario: Effects that last until end of turn expire when the turn ends
        Given a game is in progress
        And an effect exists that lasts "until end of turn"
        When the turn ends
        Then the "until end of turn" effect is no longer active

    # Rule 4.4.4 - "This turn" effects expire
    Scenario: Effects that apply "this turn" expire when the turn ends
        Given a game is in progress
        And an effect exists that applies "this turn"
        When the turn ends
        Then the "this turn" effect is no longer active

    # Rule 4.4.4 - Next player becomes turn-player
    Scenario: The next player in clockwise order becomes the new turn-player
        Given a game is in progress with multiple players
        When the turn ends
        Then the next player in clockwise order becomes the new turn-player

    # Rule 4.4.4 - New turn-player begins Start Phase
    Scenario: The new turn-player begins their Start Phase after the turn ends
        Given a game is in progress
        When the turn ends
        Then the new turn-player begins their Start Phase
