# Feature file for Section 6.6: Triggered Effects
# Reference: Flesh and Blood Comprehensive Rules Section 6.6
#
# Rule 6.6.1: A triggered effect is an effect that can be triggered to put a triggered-layer
# on the stack. Triggered effects are typically written in the format
# "[LIMIT?] (When / Whenever / At / The [ORDINAL] time / The next time) [EVENT and/or STATE] [ABILITIES]."
# Triggered effects never use the term "instead."
#
# Rule 6.6.1a: The LIMIT (if any) specifies the trigger limit, which is the maximum number of
# times the effect can be triggered. If there is no limit, the effect can be triggered any number of times.
#
# Rule 6.6.1b: The ORDINAL (if any) is one or more ordinal numbers that specify which event(s)
# within the given duration will match the trigger condition.
#
# Rule 6.6.1c: The EVENT and/or STATE specifies the event- and/or state-trigger condition.
# If the triggered condition describes an event, the effect is an event-based triggered effect;
# if it describes a game state, the effect is a state-based triggered effect.
#
# Rule 6.6.1d: The ABILITIES specifies the resolution abilities of the triggered-layer.
# When the triggered-layer resolves, the resolution abilities generate effects.
#
# Rule 6.6.2: An inline-triggered effect is a discrete triggered effect that can only trigger
# when it is generated. Written in the format "When [CONDITION] [EFFECT]."
#
# Rule 6.6.2a: An inline-triggered effect does not trigger retroactively if the condition is
# met after the effect is generated.
#
# Rule 6.6.3: A delayed-triggered effect is a layer-continuous triggered effect. Typically
# contains but does not start with "(when / whenever / at / the next time)."
#
# Rule 6.6.3a: A delayed triggered effect always specifies its duration, unless it is
# conditional on a change in phase (end of turn) or step (combat chain closes).
#
# Rule 6.6.4: A static-triggered effect is a static-continuous triggered effect. Typically
# starts with "[LIMIT?] (When / Whenever / At / The [ORDINAL] time)."
#
# Rule 6.6.5: If a game event or game state meets a triggered effect's trigger condition,
# the effect is considered triggered, creating a triggered-layer.
#
# Rule 6.6.5a: A triggered effect must exist before an event/state change that satisfies
# its trigger condition to trigger. The exception is inline-triggered effects.
#
# Rule 6.6.5b: An event-based triggered effect only triggers if a matching event occurs.
# If the event is modified before it occurs and no longer meets the condition, it does not trigger.
#
# Rule 6.6.5c: A state-based triggered effect triggers if the game state changes from not
# meeting to meeting the trigger condition.
#
# Rule 6.6.5d: If the trigger condition includes an ordinal, the effect only triggers on
# the specified ordinal time(s) the condition is met.
#
# Rule 6.6.5e: If triggered but it would exceed the trigger limit, the triggered-layer is
# not created and will not be added to the stack.
#
# Rule 6.6.5f: If triggered but an effect prevents it from triggering, the triggered-layer
# is not created, but the triggering still counts towards the limit (if any).
#
# Rule 6.6.6: When a triggered-layer is created, it is added to the stack before the next
# player receives priority as a game state process.
#
# Rule 6.6.6a: When a triggered-layer is added to the stack, the controller must declare
# parameters. If no legal targets can be declared, the triggered-layer ceases to exist.
#
# Rule 6.6.6b: If two or more triggered-layers would be created, the turn-player selects
# a player; each player adds their pending triggered-layers in clockwise order.

Feature: Section 6.6 - Triggered Effects
    As a game engine
    I need to correctly implement triggered effects
    So that triggered-layers are created and added to the stack at the right times

    # Test for Rule 6.6.1 - Triggered effects create triggered-layers
    Scenario: A triggered effect creates a triggered-layer when its condition is met
        Given a player has a card with a triggered effect "Whenever this deals damage, gain 1 life"
        When the triggering event occurs
        Then a triggered-layer is created and added to the stack

    # Test for Rule 6.6.1 - Triggered effects never use "instead"
    Scenario: A triggered effect does not use the word "instead"
        Given a triggered effect with text "When this enters the arena, draw a card"
        Then the effect is a triggered effect not a replacement effect
        And the effect does not contain the keyword "instead"

    # Test for Rule 6.6.1a - Unlimited triggering when no limit specified
    Scenario: A triggered effect with no trigger limit triggers any number of times
        Given a player has a card with a triggered effect "Whenever you play a card, gain 1 life"
        And there is no trigger limit specified
        When the triggering event occurs 3 times
        Then the effect creates 3 triggered-layers

    # Test for Rule 6.6.1a - Trigger limit restricts the number of triggers
    Scenario: A triggered effect with a trigger limit cannot exceed that limit
        Given a player has a card with a triggered effect "Once per turn - Whenever you play a card, gain 1 life"
        And the trigger limit is 1
        When the triggering event occurs a second time
        Then no additional triggered-layer is created beyond the limit

    # Test for Rule 6.6.1b - Ordinal trigger condition fires on the specified occurrence
    Scenario: A triggered effect with an ordinal only triggers on the specified occurrence
        Given a player has a card with a triggered effect "The first time you attack each turn, gain 1 action point"
        When the player attacks for the first time that turn
        Then a triggered-layer is created
        When the player attacks for the second time that turn
        Then no triggered-layer is created for the second attack

    # Test for Rule 6.6.1c - Event-based triggered effect
    Scenario: An event-based triggered effect triggers when the specified event occurs
        Given a player has a card with a triggered effect "When this enters the arena, draw a card"
        When the card enters the arena
        Then the triggered effect fires and creates a triggered-layer

    # Test for Rule 6.6.1c - State-based triggered effect
    Scenario: A state-based triggered effect triggers when the game state meets its condition
        Given a player has a card with a triggered effect "When this has no counters, destroy it"
        When the game state changes so the card has no counters
        Then the state-based triggered effect fires and creates a triggered-layer

    # Test for Rule 6.6.1d - Resolution abilities execute when triggered-layer resolves
    Scenario: Triggered-layer generates effects when it resolves
        Given a player has a card with a triggered effect "When this enters the arena, draw a card"
        And the triggered-layer has been added to the stack
        When the triggered-layer resolves
        Then the resolution abilities of the triggered-layer generate their effects

    # Test for Rule 6.6.2 - Inline-triggered effects are discrete triggered effects
    Scenario: An inline-triggered effect triggers only when it is generated
        Given a discrete effect contains an inline-triggered effect "When [condition] [effect]"
        When the inline-triggered effect is generated
        And the condition is met at the time of generation
        Then the inline-triggered effect fires immediately

    # Test for Rule 6.6.2a - Inline-triggered effects don't trigger retroactively
    Scenario: An inline-triggered effect does not trigger if condition met after generation
        Given a discrete effect contains an inline-triggered effect "When [condition] [effect]"
        When the inline-triggered effect is generated
        And the condition is not met at the time of generation
        And the condition is met after the effect is generated
        Then the inline-triggered effect does not fire retroactively

    # Test for Rule 6.6.3 - Delayed-triggered effects are layer-continuous
    Scenario: A delayed-triggered effect is a layer-continuous triggered effect
        Given a delayed-triggered effect "Gain 1 action point the next time you play an action card with cost 2 or greater this turn"
        When the delayed-triggered effect is generated as a layer
        Then it is a layer-continuous triggered effect on the stack

    # Test for Rule 6.6.3a - Delayed triggered effects specify their duration
    Scenario: A delayed triggered effect specifies its duration
        Given a delayed-triggered effect "The next time you boost this turn, draw a card"
        Then the effect has an explicit duration of "this turn"

    # Test for Rule 6.6.3a - Delayed triggered effects ending with combat chain close
    Scenario: A delayed triggered effect conditional on combat chain close lasts until triggered
        Given a delayed-triggered effect "The next time the combat chain closes, gain 2 life"
        Then the effect lasts until it is triggered when the combat chain closes

    # Test for Rule 6.6.4 - Static-triggered effects are static-continuous
    Scenario: A static-triggered effect is a static-continuous triggered effect
        Given a player controls a permanent with a static-triggered effect "Whenever you boost, create a Ponder token"
        Then it is a static-continuous triggered effect

    # Test for Rule 6.6.4 - Static-triggered effect with limit
    Scenario: A static-triggered effect with a limit specified
        Given a player controls a permanent with a static-triggered effect "The first time you boost each turn, gain 1 life"
        Then the effect has a trigger limit of once per turn
        And the ordinal "first" specifies when the trigger fires

    # Test for Rule 6.6.5 - Effect is triggered when condition is met
    Scenario: A triggered effect is triggered when the game event meets the trigger condition
        Given a player has a card with a triggered effect "Whenever an attack hits, draw a card"
        When an attack hits
        Then the triggered effect is triggered
        And a triggered-layer is created

    # Test for Rule 6.6.5a - Triggered effect must exist before the event
    Scenario: A triggered effect does not fire if it did not exist before the triggering event
        Given a triggering event occurs before the triggered effect exists
        When the triggered effect is generated after the event
        Then the triggered effect does not retroactively create a triggered-layer

    # Test for Rule 6.6.5a - Inline-triggered effects are the exception to the existence rule
    Scenario: An inline-triggered effect fires even as it is being generated
        Given a discrete effect generates an inline-triggered effect
        And the trigger condition is met at the moment of generation
        Then the inline-triggered effect fires as it is generated

    # Test for Rule 6.6.5b - Event-based effect only triggers if event meets condition
    Scenario: An event-based triggered effect does not trigger if the event is modified and no longer meets the condition
        Given a player has a card with an event-based triggered effect "When this hits, draw a card"
        And a replacement effect modifies the event so the card no longer hits
        When the modified event occurs
        Then the event-based triggered effect does not trigger

    # Test for Rule 6.6.5b - State condition must also be met for combined triggers
    Scenario: A triggered effect with both event and state conditions only triggers when both are met
        Given a player has a card with a triggered effect requiring both an event and a state condition
        When the triggering event occurs but the state condition is not met
        Then the triggered effect does not trigger
        When the triggering event occurs and the state condition is met
        Then the triggered effect triggers

    # Test for Rule 6.6.5c - State-based triggered effect triggers on state change
    Scenario: A state-based triggered effect triggers when the game state changes to meet its condition
        Given a player has a card with a state-based triggered effect "When this has no steam counters, destroy it"
        And the card initially has 1 steam counter
        When the steam counter is removed and the card now has no steam counters
        Then the state-based triggered effect is triggered

    # Test for Rule 6.6.5c - State-based effect generated while condition already met
    Scenario: A state-based triggered effect generated while condition is already met triggers immediately
        Given a card with a state-based triggered effect "When this has no steam counters, destroy it"
        When the card enters the arena with no steam counters
        Then the state-based triggered effect is generated and the condition is already met
        And the effect is triggered immediately

    # Test for Rule 6.6.5d - Ordinal trigger only fires on the specified occurrence
    Scenario: A triggered effect with ordinal does not trigger after the specified ordinal time has passed
        Given a player has a card with a triggered effect "The first time you boost each turn, gain an action point"
        And the card enters the arena after the player has already boosted once this turn
        When the player boosts again
        Then the triggered effect does not trigger because the first boost already happened

    # Test for Rule 6.6.5e - Trigger limit prevents layer creation
    Scenario: A triggered effect at its trigger limit does not create another triggered-layer
        Given a player has a card with a triggered effect limited to triggering once per turn
        And the effect has already triggered once this turn
        When the triggering condition is met again
        Then no triggered-layer is created because the trigger limit is reached

    # Test for Rule 6.6.5f - Prevention counts toward trigger limit
    Scenario: Triggering prevented by an effect still counts toward the trigger limit
        Given a player controls Katsu with "The first time an attack action card you control hits each turn, [effect]"
        And Tripwire Trap is active with "Hit effects don't trigger this chain link"
        When an attack action card controlled by the Katsu player hits
        Then the Katsu triggered effect does not create a triggered-layer due to Tripwire Trap
        And the once-per-turn limit for the Katsu triggered effect has been used up
        When an attack action card controlled by the Katsu player hits again this turn
        Then the Katsu triggered effect does not create a triggered-layer because the limit is reached

    # Test for Rule 6.6.6 - Triggered-layer added to stack before priority
    Scenario: A triggered-layer is added to the stack before the next player receives priority
        Given a triggered effect fires during a game state process
        When the triggered-layer is created
        Then it is added to the stack as a game state process before the next priority is given

    # Test for Rule 6.6.6a - Controller declares parameters when triggered-layer is added
    Scenario: Controller must declare parameters when triggered-layer is added to stack
        Given a player has a card with a triggered effect that has modal resolution abilities
        When the triggered effect triggers and a triggered-layer is created
        Then the controller must declare the mode for the triggered-layer's modal abilities
        And the triggered-layer is added to the stack after modes are declared

    # Test for Rule 6.6.6a - Triggered-layer with required target ceases to exist if no legal targets
    Scenario: A triggered-layer ceases to exist if no legal targets can be declared
        Given a player has a card with a triggered effect that requires a legal target
        And there are no legal targets available in the game state
        When the triggered effect triggers
        Then the triggered-layer ceases to exist and is not added to the stack

    # Test for Rule 6.6.6a - Example: Thaw requires mode and target selection
    Scenario: Triggered-layer from Thaw requires mode and target selection before being added to stack
        Given a player has a card similar to Thaw with a triggered effect with multiple modes requiring targets
        When the triggered effect fires at start of turn
        Then the controller must select a mode and declare a legal target before the layer is added
        And if no legal target exists for the selected mode the triggered-layer is not added

    # Test for Rule 6.6.6b - Multiple simultaneous triggered-layers ordered by turn-player
    Scenario: Multiple simultaneous triggered-layers are ordered by turn-player selection
        Given two or more triggered-layers would be created simultaneously
        And player 1 is the turn-player
        When the triggered effects fire
        Then the turn-player selects a starting player
        And each player adds their pending triggered-layers to the stack in clockwise order

    # Test for Rule 6.6.6b - Example: Celestial Kimono and Diadem ordering
    Scenario: Player can order their own triggered-layers to maximize benefit
        Given a player controls two permanents with triggered effects that fire simultaneously
        And one triggered effect would gain a resource and the other would spend that resource
        When both triggered effects fire simultaneously
        Then the controlling player may order their triggered-layers so the resource gain resolves first
        And this is true even if they are not the turn-player
