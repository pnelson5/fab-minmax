# Feature file for Section 8.3.5: Go again (Ability Keyword)
# Reference: Flesh and Blood Comprehensive Rules Section 8.3.5
#
# 8.3.5 Go again
#   Go again is a special resolution ability that means "Gain 1 action point."
#
# 8.3.5a If go again is an ability of a non-attack layer on the stack, the
#   controlling player gains 1 action point after all other resolution
#   abilities have resolved. [ref: 5.3.5]
#
# 8.3.5b If go again is an ability of an attack on the active chain link, the
#   controlling player gains 1 action point at the beginning of the Resolution
#   Step of combat. [ref: 7.6.2]
#
# 8.3.5c An object cannot have more than one "go again" ability. If an effect
#   would give the "go again" ability to an object that already has the "go
#   again" ability, then that part of the effect fails.
#
# Supporting rules:
# 5.3.5:  Go again is resolved fourth during layer resolution (after other
#           resolution abilities).
# 5.3.5a: If the layer no longer exists, last known information is used to
#           determine whether the layer had go again. [ref: 1.2.3]
# 7.6.2:  If the attack has go again, its controller gains 1 action point
#           when the chain link resolves.
# 7.6.2a: If the attack is no longer on the combat chain, last known
#           information is used to determine whether the attack had go again.
# 1.2.3c: Last known information is immutable — effects cannot alter it.
#
# Key aspects:
# - Go again is a RESOLUTION ability, not activated or static
# - For non-attack layers: fires AFTER other resolution abilities (5.3.5)
# - For attacks: fires at the BEGINNING of the Resolution Step (7.6.2)
# - An object can have at most one go again ability (8.3.5c)
# - LKI of go again is used when the object no longer exists (5.3.5a, 7.6.2a)
# - LKI is immutable; conditional static go again cannot retroactively apply (1.2.3c)

Feature: Section 8.3.5 - Go again Ability Keyword
    As a game engine
    I need to correctly implement the go again ability keyword
    So that players gain action points according to the go again rules

    # ===== Rule 8.3.5: Go again is a resolution ability =====

    Scenario: Go again is a resolution ability
        Given a card with the "go again" keyword ability
        When I inspect the go again ability on the card
        Then the go again ability is a resolution ability
        And the go again ability means "Gain 1 action point"

    # ===== Rule 8.3.5a: Non-attack layer with go again =====

    Scenario: Non-attack layer with go again grants action point after other resolutions
        Given a player is in their action phase with 0 action points
        And the player controls a non-attack action card with go again on the stack
        And the card has resolution abilities that generate other effects
        When the non-attack layer resolves
        Then the other resolution abilities resolve before go again
        And the player gains 1 action point from go again

    Scenario: Non-turn player does not gain action point from go again outside action phase
        Given a player is not in their action phase
        And the player controls a non-attack action card with go again on the stack
        When the non-attack layer resolves
        Then the player does not gain an action point from go again

    # ===== Rule 8.3.5b: Attack with go again grants AP at Resolution Step =====

    Scenario: Attack with go again grants 1 action point at the Resolution Step
        Given a player is in their action phase with 1 action point
        And the player's attack has the go again ability on the active chain link
        When the Resolution Step begins
        Then the player gains 1 action point from go again
        And the player now has 2 action points

    Scenario: Attack without go again does not grant action point at Resolution Step
        Given a player is in their action phase with 1 action point
        And the player's attack does not have the go again ability
        When the Resolution Step begins
        Then the player does not gain an action point from the attack
        And the player still has 1 action point

    # ===== Rule 8.3.5c: Object can have at most one go again ability =====

    Scenario: An object cannot be given go again if it already has go again
        Given a card already has the "go again" ability
        When an effect attempts to give the "go again" ability to the card again
        Then that part of the effect fails
        And the card still has exactly one go again ability

    Scenario: Giving go again to a card without it succeeds
        Given a card does not have the "go again" ability
        When an effect gives the "go again" ability to the card
        Then the card gains the go again ability
        And the card has exactly one go again ability

    # ===== Rule 5.3.5a / 7.6.2a: Last known information for go again =====

    Scenario: Attack moved off combat chain uses last known info for go again
        Given a player is in their action phase with 1 action point
        And the player's attack has the go again ability on the active chain link
        And the attack is moved off the combat chain before the Resolution Step
        When the Resolution Step begins
        Then last known information is used to determine whether the attack had go again
        And the player gains 1 action point because the attack had go again

    Scenario: Non-attack layer moved off stack uses last known info for go again
        Given a player is in their action phase with 0 action points
        And the player controls a non-attack card with go again that was placed on the stack
        And the card is removed from the stack before resolution completes
        When go again is evaluated after resolution
        Then last known information is used to determine whether the card had go again
        And the player gains 1 action point because the card had go again

    # ===== Rule 1.2.3c: LKI is immutable — conditional go again example =====

    Scenario: Conditional go again cannot apply retroactively via last known information
        Given a player controls an Illusionist attack as a chain link
        And an effect gives Illusionist attacks go again when a yellow card is in the pitch zone
        And the attack is removed from the combat chain before the condition is met
        When a yellow card is placed into the pitch zone
        Then the chain link does not gain go again via the conditional effect
        And the player does not gain an action point from the conditional effect

    # ===== Rule 3.0.9: Object reset removes gained go again =====

    Scenario: Go again gained then lost when object moves to non-arena non-stack zone
        Given an attack card has the "go again" ability added to it during the reaction step
        When the attack card moves to a zone that resets the object
        Then the reset card is a new object with no relation to its previous existence
        And the reset card does not have the "go again" ability
