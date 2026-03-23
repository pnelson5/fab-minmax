# Feature file for Section 7.7: Close Step
# Reference: Flesh and Blood Comprehensive Rules Section 7.7
#
# 7.7.1 The Close Step is a game state where the combat chain closes and combat
#         ends. Players do not get priority during the Close Step.
#
# 7.7.2 If a rule or effect causes the combat chain to close, the current step
#         (if any) ends and the Close Step begins. The combat chain closes in the
#         following situations:
#   7.7.2a If all players pass in succession when the stack is empty during the
#            Resolution Step, the Close Step begins.
#   7.7.2b If there are no valid attack-targets at the beginning of the Attack Step,
#            the Close Step begins.
#   7.7.2c If the active-attack of the active chain link does not exist or cannot
#            move to the combat chain as a chain link, or the active-attack ceases
#            to exist before damage is calculated, the Close Step begins as a game
#            state action.
#   7.7.2d If an effect closes the combat chain, the Close Step begins as a game
#            state action.
#
# 7.7.3 First, the "combat chain closes" event occurs and effects that trigger from
#         the combat chain closing are triggered. All attacks and reactions on the
#         stack are put into their owner's graveyard.
#
# 7.7.4 Second, layers on the stack resolve and game state actions are performed as
#         if all players are passing priority in succession.
#
# 7.7.5 Third, when the stack is empty, all permanents remaining on the combat chain
#         return to their respective zones - equipment and weapons return to their
#         respective equipped zones. Any other permanent returns to the permanent zone.
#
# 7.7.6 Fourth, all remaining objects on the combat chain are cleared.
#
# 7.7.7 Fifth and finally, the combat chain closes. Effects that last for "the/this
#         combat chain" end. The Close Step ends and the Action Phase continues.

Feature: Section 7.7 - Close Step
    As a game engine
    I need to correctly implement the Close Step of combat
    So that the combat chain closes properly and the game state is cleaned up

    # ===== Rule 7.7.1 — Close Step is a game state; no priority =====

    Scenario: Close Step is a distinct game state where the combat chain closes
        Given the combat chain is open
        And the game is in the Resolution Step
        When all players pass in succession with an empty stack
        Then the Close Step begins
        And the combat chain is closing

    Scenario: Players do not get priority during the Close Step
        Given the combat chain is open
        And the game is in the Resolution Step
        When all players pass in succession with an empty stack
        Then the Close Step begins
        And no player has priority during the Close Step

    # ===== Rule 7.7.2 — When the combat chain closes =====

    Scenario: Close Step begins when all players pass during the Resolution Step
        Given the combat chain is open
        And the stack is empty
        And the game is in the Resolution Step
        When all players pass in succession
        Then the Close Step begins
        And the current step is the close step

    Scenario: Close Step begins when there are no valid attack-targets at the Attack Step
        Given the combat chain is open
        And the game is about to begin the Attack Step
        When there are no valid attack-targets
        Then the Close Step begins instead of the Attack Step
        And the current step is the close step

    Scenario: Close Step begins if active-attack ceases to exist before damage
        Given the combat chain is open
        And an attack is the active-attack of the current chain link
        When the active-attack is destroyed before damage is calculated
        Then the Close Step begins as a game state action
        And the current step is the close step

    Scenario: Close Step begins if an effect closes the combat chain
        Given the combat chain is open
        And a card effect that closes the combat chain is resolved
        When the effect resolves
        Then the Close Step begins as a game state action
        And the current step is the close step

    # ===== Rule 7.7.3 — Combat chain closes event; attacks and reactions to graveyard =====

    Scenario: The combat chain closes event occurs at the start of the Close Step
        Given the combat chain is open
        When the Close Step begins
        Then the "combat chain closes" event occurs
        And effects that trigger from the combat chain closing are triggered

    Scenario: Attacks on the stack are put into graveyard when Close Step begins
        Given the combat chain is open
        And there is an attack on the stack
        When the Close Step begins
        Then the attack is put into its owner's graveyard
        And the attack is no longer on the stack

    Scenario: Reactions on the stack are put into graveyard when Close Step begins
        Given the combat chain is open
        And there is a reaction on the stack
        When the Close Step begins
        Then the reaction is put into its owner's graveyard
        And the reaction is no longer on the stack

    # ===== Rule 7.7.4 — Layers resolve during Close Step =====

    Scenario: Triggered layers resolve during the Close Step
        Given the combat chain is in the Close Step
        And there are triggered layers on the stack from the combat chain closes event
        When the Close Step processes the stack
        Then the triggered layers resolve
        And game state actions are performed

    # ===== Rule 7.7.5 — Permanents return to their zones =====

    Scenario: Equipment returns to its equipped zone when combat chain closes
        Given an equipment card is on the combat chain
        When the stack is empty during the Close Step
        Then the equipment returns to the player's equipped zone

    Scenario: Weapons return to their equipped zone when combat chain closes
        Given a weapon card is on the combat chain
        When the stack is empty during the Close Step
        Then the weapon returns to the player's weapon zone

    Scenario: Permanents on the combat chain return to the permanent zone
        Given a non-equipment non-weapon permanent is on the combat chain
        When the stack is empty during the Close Step
        Then the permanent returns to the permanent zone

    # ===== Rule 7.7.6 — Remaining objects are cleared =====

    Scenario: All remaining objects on the combat chain are cleared after permanents return
        Given there are objects remaining on the combat chain
        When the Close Step clears the combat chain
        Then all objects are removed from the combat chain
        And the combat chain has no remaining objects

    # ===== Rule 7.7.7 — Combat chain closes; chain-duration effects end =====

    Scenario: Effects that last for the combat chain end when the combat chain closes
        Given there is an effect that lasts for "this combat chain"
        And the combat chain is in the Close Step
        When the combat chain closes
        Then the effect that lasts for this combat chain ends

    Scenario: The combat chain is closed after the Close Step
        Given the combat chain is open
        When the Close Step completes
        Then the combat chain is closed

    Scenario: The Action Phase continues after the Close Step ends
        Given the combat chain is open
        And the game is in the Action Phase
        When the Close Step completes
        Then the Close Step ends
        And the Action Phase continues
