# Feature file for Section 7.6: Resolution Step
# Reference: Flesh and Blood Comprehensive Rules Section 7.6
#
# Rule 7.6.1: The Resolution Step is a game state where the active chain link
# resolves and the attacker may gain an action point from go again and continue
# the combat chain by attacking.
#
# Rule 7.6.2: First, the active chain link becomes a resolved chain link and
# effects that trigger when the chain link resolves are triggered. If the attack
# has go again, its controller gains 1 action point.
#
# Rule 7.6.2a: If the attack is no longer on the combat chain, the last known
# information of the attack is used to determine whether the attack has go again.
#
# Rule 7.6.3: Second, the turn-player gains priority. If an attack is added to
# the stack, the Resolution Step ends and the Layer Step begins.
#
# Rule 7.6.3a: The turn-player may play or activate another attack during the
# Resolution Step, including attack action cards or abilities with attack.
#
# Rule 7.6.4: Third and finally, when the stack is empty and all players pass in
# succession, the Resolution Step ends and the Close Step begins.

Feature: Section 7.6 - Resolution Step
    As a game engine
    I need to correctly implement the Resolution Step of combat
    So that chain links resolve properly, go again grants action points, and combat can continue

    # -------------------------------------------------------------------------
    # Rule 7.6.1 — Resolution Step is a distinct game state
    # -------------------------------------------------------------------------

    # Tests Rule 7.6.1: The Resolution Step is a game state
    Scenario: Resolution Step is the game state where the active chain link resolves
        Given the combat chain is open with an active chain link
        And the Damage Step has just ended
        When the Resolution Step begins
        Then the current combat step is "resolution"
        And the active chain link begins resolving

    # Tests Rule 7.6.1: Resolution Step follows the Damage Step
    Scenario: Resolution Step begins after the Damage Step ends
        Given the combat chain is open with an active chain link
        And the Damage Step is active
        When the stack is empty and all players pass in succession during the Damage Step
        Then the Damage Step ends
        And the Resolution Step begins

    # -------------------------------------------------------------------------
    # Rule 7.6.2 — Chain link becomes resolved; go again grants action point
    # -------------------------------------------------------------------------

    # Tests Rule 7.6.2: Active chain link becomes a resolved chain link
    Scenario: Active chain link becomes a resolved chain link at the start of Resolution Step
        Given the combat chain is open with an active chain link
        And the Resolution Step is active
        When the chain link resolution begins
        Then the active chain link becomes a resolved chain link
        And effects that trigger when the chain link resolves are triggered

    # Tests Rule 7.6.2: Attack with go again grants 1 action point
    Scenario: Attack with go again grants the controller 1 action point
        Given the combat chain is open with an active chain link
        And the active attack has go again
        And the Resolution Step is active
        When the chain link resolution begins
        Then the controller of the attack gains 1 action point

    # Tests Rule 7.6.2: Attack without go again does not grant action point
    Scenario: Attack without go again does not grant an action point
        Given the combat chain is open with an active chain link
        And the active attack does not have go again
        And the Resolution Step is active
        When the chain link resolution begins
        Then the controller of the attack does not gain an action point from resolution

    # Tests Rule 7.6.2a: Last known information used when attack leaves combat chain
    Scenario: Last known information determines go again if attack leaves combat chain before Resolution Step
        Given the combat chain is open with an active chain link
        And the active attack has go again
        And the active attack has left the combat chain before the Resolution Step
        When the chain link resolution begins
        Then last known information indicates the attack had go again
        And the controller of the attack gains 1 action point

    # Tests Rule 7.6.2a: Last known information used — attack without go again left chain
    Scenario: Last known information used when attack without go again leaves combat chain
        Given the combat chain is open with an active chain link
        And the active attack does not have go again
        And the active attack has left the combat chain before the Resolution Step
        When the chain link resolution begins
        Then last known information indicates the attack did not have go again
        And the controller of the attack does not gain an action point from resolution

    # -------------------------------------------------------------------------
    # Rule 7.6.3 — Turn-player gains priority; new attack restarts Layer Step
    # -------------------------------------------------------------------------

    # Tests Rule 7.6.3: Turn-player gains priority during Resolution Step
    Scenario: Turn-player gains priority during the Resolution Step
        Given the combat chain is open with an active chain link
        And the Resolution Step is active
        And the chain link has resolved
        When priority is granted
        Then the turn-player has priority during the Resolution Step

    # Tests Rule 7.6.3: New attack added during Resolution Step ends it and starts Layer Step
    Scenario: Adding an attack to the stack during Resolution Step ends it and begins Layer Step
        Given the combat chain is open with a resolved chain link
        And the Resolution Step is active
        And the turn-player has priority
        When the turn-player plays an attack action card during the Resolution Step
        Then the attack is added to the stack
        And the Resolution Step ends
        And the Layer Step begins

    # Tests Rule 7.6.3a: Turn-player may play attack action cards during Resolution Step
    Scenario: Turn-player may play attack action cards during the Resolution Step
        Given the combat chain is open with a resolved chain link
        And the Resolution Step is active
        And the turn-player has an attack action card in hand
        And the turn-player has an action point
        When the turn-player attempts to play an attack action card during the Resolution Step
        Then the play is allowed

    # Tests Rule 7.6.3a: Turn-player may activate attack abilities during Resolution Step
    Scenario: Turn-player may activate attack abilities during the Resolution Step
        Given the combat chain is open with a resolved chain link
        And the Resolution Step is active
        And the turn-player has a weapon with an attack ability
        And the turn-player has an action point
        When the turn-player attempts to activate the attack ability during the Resolution Step
        Then the activation is allowed

    # Tests Rule 7.0.1a cross-reference: Non-attack actions cannot be played during Resolution Step
    Scenario: Non-attack action cards cannot be played during the Resolution Step
        Given the combat chain is open with a resolved chain link
        And the Resolution Step is active
        And the turn-player has a non-attack action card in hand
        When the turn-player attempts to play the non-attack action card during the Resolution Step
        Then the play is not allowed during the Resolution Step

    # -------------------------------------------------------------------------
    # Rule 7.6.4 — Resolution Step ends when stack empty and all players pass
    # -------------------------------------------------------------------------

    # Tests Rule 7.6.4: Resolution Step ends when stack is empty and all players pass
    Scenario: Resolution Step ends and Close Step begins when all players pass with empty stack
        Given the combat chain is open with a resolved chain link
        And the Resolution Step is active
        And the stack is empty
        When all players pass in succession during the Resolution Step
        Then the Resolution Step ends
        And the Close Step begins

    # Tests Rule 7.6.4: Resolution Step does not end while stack has items
    Scenario: Resolution Step does not end while the stack has items
        Given the combat chain is open with a resolved chain link
        And the Resolution Step is active
        And there is an item on the stack
        When all players attempt to pass in succession during the Resolution Step
        Then the Resolution Step has not ended

    # -------------------------------------------------------------------------
    # Integration: Full Resolution Step flow
    # -------------------------------------------------------------------------

    # Tests full flow: go again allows continued combat chain
    Scenario: Attack with go again allows attacker to continue combat chain
        Given the combat chain is open with an active chain link
        And the active attack has go again
        And the Damage Step has just ended
        When the Resolution Step begins
        And the chain link resolves and the controller gains 1 action point
        And the turn-player plays another attack action card
        Then the combat chain continues with a new chain link

    # Tests full flow: no go again leads to Close Step if no new attack played
    Scenario: Attack without go again leads to Close Step if no new attack is played
        Given the combat chain is open with an active chain link
        And the active attack does not have go again
        And the Resolution Step is active
        And the chain link has resolved
        When all players pass in succession during the Resolution Step
        Then the Resolution Step ends
        And the Close Step begins
