# Feature file for Section 6.5: Replacement Effect Interactions
# Reference: Flesh and Blood Comprehensive Rules Section 6.5
#
# Rule 6.5.1: If there are two or more replacement effects that could replace an event
# with a modified event, then effects are applied based on an order determined by the
# turn-player and then an order determined by each controlling player.
#
# Rule 6.5.2: Select Player: First, the turn-player selects a player. When a type of
# replacement effect is applied, each player in clockwise order applies their active
# replacement effects of that type one-by-one until they do not control any more active
# replacement effects of that type; starting with the selected player and ending when
# there are no more active replacement effects of that type to apply.
#
# Rule 6.5.2a: The turn-player does not determine the order of effects they do not
# control, only the first player to apply replacement effects.
#
# Rule 6.5.2b: The selected player is determined once per event and does not change.
#
# Rule 6.5.3: Self-replacement and Identity-replacement: Second, each player applies any
# self- or identity- replacement effects they control.
#
# Rule 6.5.4: Standard-replacement: Third, each player applies any active
# standard-replacement effects they control.
#
# Rule 6.5.5: Prevention: Fourth, each player applies any active prevention effects
# they control.
#
# Rule 6.5.6: Event: Fifth, the event occurs.
#
# Rule 6.5.7: Outcome-replacement: Sixth, each player applies any active
# outcome-replacement effects they control.
#
# Rule 6.5.8: Event: Seventh, and finally, the event is complete.

Feature: Section 6.5 - Replacement Effect Interactions
    As a game engine
    I need to correctly sequence multiple replacement effects
    So that the game applies them in the correct type-priority order

    # Test for Rule 6.5.1 - Multiple replacement effects applied in turn-player/controller order
    Scenario: Multiple replacement effects applying to the same event are ordered by turn-player selection
        Given two players are in a game
        And player 1 is the turn-player
        And player 1 controls a standard-replacement effect
        And player 2 controls a standard-replacement effect
        When an event occurs that both replacement effects could replace
        Then the turn-player selects a starting player to apply standard-replacement effects
        And effects are applied in clockwise order starting from the selected player

    # Test for Rule 6.5.2 - Turn-player selects first applying player
    Scenario: Turn-player selects the first player to apply replacement effects
        Given two players are in a game
        And player 1 is the turn-player
        And player 1 controls a standard-replacement effect
        And player 2 controls a standard-replacement effect
        When an event occurs that both replacement effects could replace
        Then player 1 as turn-player selects which player begins applying effects
        And the selected player is either player 1 or player 2

    # Test for Rule 6.5.2a - Turn-player only determines starting player, not opponent order
    Scenario: Turn-player does not determine the order of opponent-controlled replacement effects
        Given two players are in a game
        And player 1 is the turn-player
        And player 2 controls multiple standard-replacement effects
        When an event occurs that player 2's replacement effects could replace
        Then player 2 determines the order of their own replacement effects
        And player 1 as turn-player cannot determine which of player 2's effects applies first

    # Test for Rule 6.5.2b - Selected player is fixed for the event
    Scenario: The selected starting player does not change during a single event
        Given two players are in a game
        And player 1 is the turn-player
        And player 1 controls a standard-replacement effect
        And player 2 controls a standard-replacement effect
        When an event occurs that both replacement effects could replace
        Then the turn-player selects a starting player once for the event
        And that selected player remains the starting player throughout the event's replacement

    # Test for Rule 6.5.3 - Self-replacement applied before standard-replacement
    Scenario: Self-replacement effects are applied before standard-replacement effects
        Given a player controls a self-replacement effect
        And a player controls a standard-replacement effect
        When an event occurs that both replacement effects could replace
        Then the self-replacement effect is applied before the standard-replacement effect
        And the application order reflects self-replacement preceding standard-replacement

    # Test for Rule 6.5.3 - Identity-replacement applied before standard-replacement
    Scenario: Identity-replacement effects are applied before standard-replacement effects
        Given a player controls an identity-replacement effect
        And a player controls a standard-replacement effect
        When an event occurs that both replacement effects could replace
        Then the identity-replacement effect is applied before the standard-replacement effect
        And the application order reflects identity-replacement preceding standard-replacement

    # Test for Rule 6.5.4 - Standard-replacement applied before prevention
    Scenario: Standard-replacement effects are applied before prevention effects
        Given a player controls a standard-replacement effect
        And a player controls a prevention effect
        When a damage event occurs that both effects could apply to
        Then the standard-replacement effect is applied before the prevention effect
        And the application order reflects standard-replacement preceding prevention

    # Test for Rule 6.5.5 - Prevention effects applied before event occurs
    Scenario: Prevention effects are applied before the event occurs
        Given a player controls a prevention effect that prevents damage
        When a damage event is about to occur
        Then the prevention effect is applied before the damage event occurs
        And the prevention result modifies or eliminates the damage event

    # Test for Rule 6.5.6 - Event occurs after all pre-event replacements
    Scenario: The event occurs only after all self-replacement, identity-replacement, standard-replacement, and prevention effects are applied
        Given a player controls a self-replacement effect
        And a player controls a standard-replacement effect
        And a player controls a prevention effect
        When an event occurs that all three effects could apply to
        Then all three pre-event replacement effects are applied in type order
        And the event occurs after all pre-event replacements have been applied

    # Test for Rule 6.5.7 - Outcome-replacement applied after event occurs
    Scenario: Outcome-replacement effects are applied after the event occurs
        Given a player controls an outcome-replacement effect
        When an event occurs
        Then the event occurs before the outcome-replacement effect is applied
        And the outcome-replacement effect is applied after the event

    # Test for Rule 6.5.8 - Event complete after outcome-replacement
    Scenario: The event is complete after outcome-replacement effects are applied
        Given a player controls an outcome-replacement effect
        When an event occurs and the outcome-replacement is applied
        Then the event is marked complete after outcome-replacement has been applied
        And no further replacement effects can be applied to that event

    # Test for Rule 6.5.3 and 6.5.4 - Full type ordering
    Scenario: Replacement effects are applied in the correct type priority order
        Given a player controls a self-replacement effect
        And a player controls a standard-replacement effect
        And a player controls a prevention effect
        And a player controls an outcome-replacement effect
        When an event occurs that all four effects could apply to
        Then the replacement effects are applied in this order: self-replacement, standard-replacement, prevention, event, outcome-replacement

    # Test for Rule 6.5.1 and 6.5.2 - Multiple players, same type, clockwise order
    Scenario: Multiple players with same-type replacement effects apply them in clockwise order
        Given three players are in a game in clockwise order: player 1, player 2, player 3
        And player 1 is the turn-player
        And player 2 controls a standard-replacement effect
        And player 3 controls a standard-replacement effect
        When an event occurs that both player 2 and player 3's replacement effects could replace
        And player 1 selects player 2 as the starting player
        Then player 2 applies their standard-replacement effect first
        And player 3 applies their standard-replacement effect second

    # Test for Rule 6.5.2 - Each player applies all their effects of a type before next player
    Scenario: Each player applies all their replacement effects of a type before the next player applies theirs
        Given two players are in a game
        And player 1 is the turn-player
        And player 1 controls two standard-replacement effects
        And player 2 controls one standard-replacement effect
        When an event occurs that all three replacement effects could replace
        And player 1 is selected as the starting player
        Then player 1 applies both of their standard-replacement effects before player 2 applies theirs
