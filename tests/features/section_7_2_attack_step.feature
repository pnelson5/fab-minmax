# Feature file for Section 7.2: Attack Step
# Reference: Flesh and Blood Comprehensive Rules Section 7.2
#
# Rule 7.2.1: The Attack Step is the game state where an attack resolves and
#   becomes attacking before any defending cards are declared.
#
# Rule 7.2.2: First, check that at least one of the attack's attack-targets is
#   still a legal target; if none are legal, the Attack Step ends and the Close
#   Step begins.
#   Rule 7.2.2a: Only one attack-target needs to be legal at this point.
#     If all targets cease to be legal AFTER this check, combat still continues.
#
# Rule 7.2.3: Second, each resolution ability of the attack generates its
#   effects in order (except go again), then the attack moves onto the combat
#   chain as a chain link. Attacking objects remain attacking until they leave
#   the combat chain.
#   Rule 7.2.3a: Attack-card: moves onto the combat chain as a chain link; the
#     attack-card is the active-attack and becomes attacking.
#   Rule 7.2.3b: Attack-proxy: the attack-proxy and its attack-source both move
#     onto the chain link; the attack-proxy is the active-attack; if the
#     attack-source was on a previous chain link, the prior attack-proxy ceases
#     to exist.
#   Rule 7.2.3c: Attack-layer: the card specified by the attack-layer's effect
#     moves onto the chain link as the active-attack; all parameters and applied
#     effects from the attack-layer transfer to the active-attack, then the
#     attack-layer ceases to exist.
#   Rule 7.2.3d: If the active-attack does not exist or cannot move to the
#     combat chain, the Attack Step ends and the Close Step begins.
#
# Rule 7.2.4: Third, the "attack" event occurs and effects that trigger from
#   attacking are triggered.
#   Rule 7.2.4a: If there is an attack-source and it is a living object, it
#     becomes attacking. Otherwise, the controller and their hero card become
#     the "attacking hero" until the active chain link resolves or the combat
#     chain closes.
#   Rule 7.2.4b: If the attack-target is a hero, that hero and their controller
#     become the "defending hero" until the active chain link resolves or the
#     combat chain closes.
#
# Rule 7.2.5: Fourth, the turn-player gains priority.
#
# Rule 7.2.6: Fifth and finally, when the stack is empty and all players pass
#   in succession, the Attack Step ends and the Defend Step begins.

Feature: Section 7.2 - Attack Step
    As a game engine
    I need to correctly implement the Attack Step of combat
    So that attacks correctly transition from the stack to the combat chain and
    the attacking/defending hero designations are correctly applied

    # -----------------------------------------------------------------------
    # Rule 7.2.1 — Attack Step is a distinct game state
    # -----------------------------------------------------------------------

    # Test for Rule 7.2.1 - Attack Step is a game state between Layer Step and Defend Step
    Scenario: Attack Step is a game state where the attack becomes attacking before defenders are declared
        Given the Layer Step is active
        And the top layer of the stack is the attack
        When all players pass priority in succession
        Then the Layer Step ends
        And the Attack Step begins
        And no defending cards have been declared yet

    # -----------------------------------------------------------------------
    # Rule 7.2.2 — Target legality check (first action in Attack Step)
    # -----------------------------------------------------------------------

    # Test for Rule 7.2.2 - Attack Step proceeds when attack-target is still legal
    Scenario: Attack Step proceeds when the attack-target is still a legal target
        Given the Attack Step is about to begin
        And the attack has one attack-target
        And the attack-target is a legal target
        When the Attack Step begins
        Then the attack proceeds onto the combat chain

    # Test for Rule 7.2.2 - Attack Step ends and Close Step begins when no targets are legal
    Scenario: Attack Step ends immediately when all attack-targets are illegal
        Given the Attack Step is about to begin
        And the attack has one attack-target
        And the attack-target is no longer a legal target
        When the Attack Step begins
        Then the Attack Step ends immediately
        And the Close Step begins instead of the Defend Step

    # Test for Rule 7.2.2a - Only one target needs to be legal
    Scenario: Attack Step proceeds when at least one of multiple attack-targets is still legal
        Given the Attack Step is about to begin
        And the attack has two attack-targets
        And one attack-target is a legal target
        And the other attack-target is no longer a legal target
        When the Attack Step begins
        Then the attack proceeds onto the combat chain

    # Test for Rule 7.2.2a - Targets becoming illegal after the check does not end combat
    Scenario: Attack continues even if targets become illegal after the legality check
        Given the Attack Step has passed the target legality check
        And all attack-targets cease to be legal after the check
        When the attack is on the combat chain as the active chain link
        Then the attack remains on the combat chain
        And combat continues to the Defend Step

    # -----------------------------------------------------------------------
    # Rule 7.2.3 — Attack moves onto combat chain (second action in Attack Step)
    # -----------------------------------------------------------------------

    # Test for Rule 7.2.3 - Resolution abilities generate effects before chain placement
    Scenario: Resolution abilities of the attack generate effects before the attack moves to the combat chain
        Given the Attack Step has passed the target legality check
        And the attack has a resolution ability
        When the Attack Step processes the resolution abilities
        Then the resolution ability generates its effect
        And then the attack moves onto the combat chain as a chain link

    # Test for Rule 7.2.3a - Attack-card becomes the active-attack and gains attacking status
    Scenario: Attack-card moves onto the combat chain as the active-attack chain link
        Given the Attack Step is processing an attack-card
        When the attack-card moves onto the combat chain
        Then the attack-card is the active-attack
        And the attack-card is on the combat chain as a chain link
        And the attack-card has the attacking status

    # Test for Rule 7.2.3b - Attack-proxy and attack-source both move onto chain link
    Scenario: Attack-proxy and its attack-source both move onto the combat chain link
        Given the Attack Step is processing an attack with an attack-proxy
        And the attack-proxy has an attack-source
        When the attack moves onto the combat chain
        Then the attack-proxy is the active-attack
        And both the attack-proxy and attack-source are on the same chain link

    # Test for Rule 7.2.3d - Close Step begins if active-attack does not exist
    Scenario: Attack Step ends and Close Step begins if active-attack cannot move to combat chain
        Given the Attack Step is processing an attack
        And the active-attack does not exist
        When the Attack Step attempts to place the attack on the combat chain
        Then the Attack Step ends
        And the Close Step begins

    # -----------------------------------------------------------------------
    # Rule 7.2.4 — "attack" event and attacking/defending hero designations
    # -----------------------------------------------------------------------

    # Test for Rule 7.2.4 - "attack" event occurs after attack moves onto chain
    Scenario: The attack event occurs after the attack moves onto the combat chain
        Given the attack has been placed on the combat chain as a chain link
        When the Attack Step triggers the attack event
        Then effects that trigger on attacking are triggered

    # Test for Rule 7.2.4a - Attack-source that is a living object becomes attacking
    Scenario: Attack-source that is a living object becomes attacking during the Attack Step
        Given the Attack Step is processing an attack with a living attack-source
        When the attack event occurs
        Then the attack-source has the attacking status

    # Test for Rule 7.2.4a - Controller and hero become attacking hero when no living attack-source
    Scenario: Controller and hero become attacking hero when there is no living attack-source
        Given the Attack Step is processing an attack without a living attack-source
        When the attack event occurs
        Then the attacking controller becomes the attacking hero
        And the attacking hero's hero card is designated as the attacking hero

    # Test for Rule 7.2.4b - Defending hero is designated when attack-target is a hero
    Scenario: Attack-target hero and their controller become the defending hero
        Given the Attack Step is processing an attack
        And the attack-target is a hero
        When the attack event occurs
        Then the attack-target hero becomes the defending hero
        And the attack-target hero's controller becomes the defending hero's controller

    # Test for Rule 7.2.4a + 7.2.4b - Attacking and defending hero designations last until chain link resolves
    Scenario: Attacking and defending hero designations persist until the active chain link resolves
        Given the attack event has occurred
        And the attacking hero and defending hero have been designated
        When the active chain link resolves
        Then the attacking hero designation is removed
        And the defending hero designation is removed

    # -----------------------------------------------------------------------
    # Rule 7.2.5 — Turn-player gains priority (fourth action in Attack Step)
    # -----------------------------------------------------------------------

    # Test for Rule 7.2.5 - Turn-player gains priority after attack event
    Scenario: Turn-player gains priority in the Attack Step after the attack event
        Given the attack has been placed on the combat chain
        And the attack event has occurred
        When the Attack Step grants priority
        Then the turn-player has priority

    # -----------------------------------------------------------------------
    # Rule 7.2.6 — Attack Step ends and Defend Step begins
    # -----------------------------------------------------------------------

    # Test for Rule 7.2.6 - Defend Step begins when stack is empty and all players pass
    Scenario: Attack Step ends and Defend Step begins when all players pass with empty stack
        Given the Attack Step is active
        And the stack is empty
        When all players pass priority in succession
        Then the Attack Step ends
        And the Defend Step begins
