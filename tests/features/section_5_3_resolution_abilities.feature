# Feature file for Section 5.3: Resolution Abilities & Resolving Layers
# Reference: Flesh and Blood Comprehensive Rules Section 5.3
#
# 5.3.1 A resolution ability is an ability that generates effects when its source
# resolves as a layer on the stack. If the stack is not empty and all players pass
# in succession, the top layer of the stack resolves, except the Layer Step of combat.
# When a layer resolves it does so in the following order:
#   Check resolution, Static effects, Layer effects, Go again, Leave stack, Clear.
#
# 5.3.2 Check resolution: First, whether the layer fails to resolve is evaluated. If
# a layer fails to resolve, the resolution stops, the layer is cleared from the stack,
# and the turn-player gains priority.
#
# 5.3.2a If the layer has a resolution ability with a targeted effect, and one or more
# targets were declared when the layer was put onto the stack, at least one of those
# targets must still be a legal target - otherwise, the layer fails to resolve.
#
# 5.3.2b If the layer is a triggered-layer created by a triggered effect with a
# state-trigger condition, the state-trigger condition must be met by the current
# game state - otherwise, the layer fails to resolve.
#
# 5.3.2c If the layer is a defense reaction card and it cannot become a defending
# card on the current chain link, the layer fails to resolve.
#
# 5.3.3 Static effects: Second, static abilities of the layer become functional.
#
# 5.3.4 Layer effects: Third, each of the resolution abilities of the layer generates
# its effects in the order specified (except go again).
#
# 5.3.4a If the parameters of any effect are undetermined, those parameters are
# determined before the effect is generated.
#
# 5.3.4b If an effect fails, any remaining effects continue to be generated.
#
# 5.3.4c If the layer no longer exists after the generation of an effect, the last
# known information of the layer is used to determine the remainder of the resolution
# abilities and the effects that are generated.
#
# 5.3.4d If the layer is melded and it is its first time being resolved, only the
# right-side resolution abilities generate their effects, then resolution stops and
# the turn-player gains priority; if it is the second time being resolved, only the
# left-side resolution abilities generate their effects, then resolution continues.
#
# 5.3.5 Go again: Fourth, if the layer has go again, the controlling player gains 1
# action point.
#
# 5.3.5a If the layer no longer exists, the last known information of the layer is
# used to determine whether the layer had go again.
#
# 5.3.6 Leave stack: Fifth, if a rule or effect would cause the layer to leave the
# stack, it does so.
#
# 5.3.6a A card-layer that becomes a permanent is moved to the arena.
#
# 5.3.6b A card-layer with the type defense reaction becomes a defending card on the
# active chain link.
#
# 5.3.7 Clear: Sixth and finally, if the layer is still on the stack, it is cleared,
# then the turn-player gains priority.

Feature: Section 5.3 - Resolution Abilities & Resolving Layers
    As a game engine
    I need to correctly implement layer resolution rules
    So that effects are generated in the correct order with correct failure handling

    # Test for Rule 5.3.1 - Resolution triggers when all players pass

    Scenario: Layer resolves when all players pass in succession
        Given a card is on the stack as a layer
        And all players have passed in succession
        When the engine processes priority
        Then the top layer should resolve
        And the resolution ability generates its effects

    Scenario: Resolution order follows check then static then effects then go again then leave stack then clear
        Given a card with a resolution ability and go again is on the stack
        And all players have passed
        When the layer resolves
        Then the resolution proceeds in order: check resolution, static effects, layer effects, go again, leave stack, clear

    # Test for Rule 5.3.2 - Check resolution step

    Scenario: Layer with no failures resolves normally
        Given a card with a resolution ability is on the stack
        And the layer has no targeted effects
        And the layer is not a triggered-layer with a state-trigger
        When check resolution is evaluated
        Then the layer does not fail to resolve
        And resolution continues

    Scenario: Layer clears from stack and turn-player gains priority when it fails to resolve
        Given a layer fails to resolve during check resolution
        When the check resolution step completes
        Then the layer is cleared from the stack
        And the turn-player gains priority

    # Test for Rule 5.3.2a - Targeted effect requires legal target

    Scenario: Layer with targeted effect fails to resolve when no legal targets remain
        Given a card with a targeted resolution ability is on the stack
        And one target was declared when the layer was put on the stack
        And that target is no longer a legal target
        When check resolution is evaluated
        Then the layer fails to resolve
        And the layer is cleared from the stack
        And no effects are generated

    Scenario: Layer with targeted effect resolves when at least one declared target remains legal
        Given a card with a targeted resolution ability is on the stack
        And two targets were declared when the layer was put on the stack
        And one target is no longer a legal target but the other target remains legal
        When check resolution is evaluated
        Then the layer does not fail to resolve
        And the effect is generated targeting only the legal target

    Scenario: Layer with no declared targets is unaffected by targeting check
        Given a card with a targeted resolution ability is on the stack
        And no targets were declared when the layer was put on the stack
        When check resolution is evaluated
        Then the targeted check is not applicable
        And the layer does not fail to resolve due to targeting

    # Test for Rule 5.3.2b - State-trigger condition must be met

    Scenario: Triggered-layer with state-trigger fails if condition no longer met
        Given a triggered-layer created by a state-trigger condition is on the stack
        And the state-trigger condition was met when the layer was created
        But the state-trigger condition is no longer met by the current game state
        When check resolution is evaluated
        Then the triggered-layer fails to resolve
        And the triggered-layer is cleared from the stack
        And no effects are generated

    Scenario: Triggered-layer resolves when state-trigger condition still met
        Given a triggered-layer created by a state-trigger condition is on the stack
        And the state-trigger condition is still met by the current game state
        When check resolution is evaluated
        Then the triggered-layer does not fail to resolve

    Scenario: Phantasm triggered-layer fails when phantasm condition no longer met before resolution
        Given an attack with phantasm is on the combat chain
        And a defense reaction defending the attack causes the phantasm condition to no longer be met
        And the phantasm triggered-layer is on the stack
        When check resolution is evaluated
        Then the phantasm triggered-layer fails to resolve
        And the phantasm triggered-layer is cleared from the stack

    # Test for Rule 5.3.2c - Defense reaction card must be able to become defending card

    Scenario: Defense reaction layer fails to resolve if it cannot become a defending card
        Given a defense reaction card is on the stack as a layer
        And there is no active chain link on which it can become a defending card
        When check resolution is evaluated
        Then the defense reaction layer fails to resolve
        And the layer is cleared from the stack

    Scenario: Defense reaction layer resolves if it can become a defending card
        Given a defense reaction card is on the stack as a layer
        And there is an active chain link on which it can become a defending card
        When check resolution is evaluated
        Then the defense reaction layer does not fail to resolve

    # Test for Rule 5.3.3 - Static effects step

    Scenario: Static abilities of the layer become functional during resolution
        Given a card with a static ability is on the stack as a layer
        And the static ability was not functional before resolution
        When the static effects step of resolution occurs
        Then the static ability becomes functional
        And the static ability generates its continuous effect

    # Test for Rule 5.3.4 - Layer effects step

    Scenario: Resolution abilities generate effects in specified order
        Given a card with multiple resolution abilities is on the stack
        And the abilities are ordered A then B then C
        When the layer effects step of resolution occurs
        Then ability A generates its effect first
        And ability B generates its effect second
        And ability C generates its effect third

    Scenario: Go again ability does not generate its effect during layer effects step
        Given a card with go again and a resolution ability is on the stack
        When the layer effects step of resolution occurs
        Then the resolution ability generates its effect
        And go again does not generate its effect during this step

    # Test for Rule 5.3.4a - Undetermined parameters resolved first

    Scenario: Undetermined parameters are determined before effect is generated
        Given a card with a resolution ability whose parameters are undetermined at resolution time
        When the layer effects step determines parameters for the effect
        Then the parameters are determined before the effect is generated
        And the effect is generated with the determined parameters

    # Test for Rule 5.3.4b - Failed effects do not stop remaining effects

    Scenario: Remaining effects continue if one effect fails
        Given a card with three sequential resolution abilities is on the stack
        And the second ability will fail when generated
        When the layer effects step of resolution occurs
        Then the first ability generates its effect
        And the second ability fails to generate its effect
        And the third ability still generates its effect

    # Test for Rule 5.3.4c - LKI used when layer ceases to exist

    Scenario: Last known information used when layer ceases to exist during resolution
        Given a card with multiple resolution abilities is on the stack
        And the layer ceases to exist after the first effect is generated
        When the remainder of the resolution abilities are evaluated
        Then the last known information of the layer is used
        And the remaining effects are determined from last known information

    # Test for Rule 5.3.4d - Melded card resolution

    Scenario: Melded layer generates only right-side effects on first resolution
        Given a melded card is on the stack as a layer
        And it is the first time this melded layer is being resolved
        When the layer effects step of resolution occurs
        Then only the right-side resolution abilities generate their effects
        And resolution stops after the right-side effects
        And the turn-player gains priority

    Scenario: Melded layer generates only left-side effects on second resolution
        Given a melded card is on the stack as a layer
        And it is the second time this melded layer is being resolved
        When the layer effects step of resolution occurs
        Then only the left-side resolution abilities generate their effects
        And resolution continues after the left-side effects

    # Test for Rule 5.3.5 - Go again grants action point

    Scenario: Controlling player gains 1 action point when layer has go again
        Given a card with go again is on the stack as a layer
        And the controlling player has 0 action points
        When the go again step of resolution occurs
        Then the controlling player gains 1 action point
        And the controlling player now has 1 action point

    Scenario: Controlling player does not gain action point when layer has no go again
        Given a card without go again is on the stack as a layer
        And the controlling player has 0 action points
        When the go again step of resolution occurs
        Then the controlling player does not gain an action point
        And the controlling player still has 0 action points

    # Test for Rule 5.3.5a - LKI used for go again when layer ceases to exist

    Scenario: Last known information determines go again when layer no longer exists
        Given a card with go again is on the stack as a layer
        And the layer ceases to exist before the go again step
        When the go again step of resolution occurs
        Then the last known information of the layer indicates it had go again
        And the controlling player gains 1 action point

    Scenario: Last known information determines no go again when layer had none
        Given a card without go again is on the stack as a layer
        And the layer ceases to exist before the go again step
        When the go again step of resolution occurs
        Then the last known information indicates the layer did not have go again
        And the controlling player does not gain an action point

    # Test for Rule 5.3.6 - Leave stack step

    Scenario: Layer leaves stack when a rule or effect would cause it to
        Given a card is on the stack as a layer
        And an effect causes the layer to leave the stack during resolution
        When the leave stack step of resolution occurs
        Then the layer leaves the stack

    # Test for Rule 5.3.6a - Permanent card-layer moves to arena

    Scenario: Card-layer that becomes a permanent is moved to the arena
        Given a card that becomes a permanent is on the stack as a layer
        When the leave stack step of resolution occurs
        Then the card is moved to the arena
        And the card is now in the arena zone

    # Test for Rule 5.3.6b - Defense reaction becomes defending card

    Scenario: Defense reaction card-layer becomes a defending card on active chain link
        Given a defense reaction card is on the stack as a layer
        And there is an active chain link
        When the leave stack step of resolution occurs
        Then the defense reaction card becomes a defending card
        And the card is now defending on the active chain link

    # Test for Rule 5.3.7 - Clear step

    Scenario: Layer still on stack after resolution is cleared
        Given a card with a resolution ability is on the stack as a layer
        And the layer does not leave the stack during the leave stack step
        When the clear step of resolution occurs
        Then the layer is cleared from the stack
        And the stack no longer contains the layer
        And the turn-player gains priority

    Scenario: Turn-player gains priority after clear step
        Given a layer has been cleared from the stack
        When the clear step completes
        Then the turn-player gains priority
