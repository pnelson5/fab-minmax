# Feature file for Section 6.3: Continuous Effect Interactions
# Reference: Flesh and Blood Comprehensive Rules Section 6.3
#
# Rule 6.3.1: Continuous effects that modify the rules of the game are applied
# simultaneously before continuous effects that modify objects. If there are two
# or more continuous effects that modify the state and/or properties of objects
# in the game, the effects are applied using the staging system. These effects
# are grouped into stages and are applied in ascending stage order, then if there
# are two or more effects in the same stage, the effects are applied using substage
# order, then timestamp order.
#
# Example (6.3.1): Hypothermia: "Attacks you control can't gain go again," which is a
# continuous effect that modifies the rules of the game and is applied before any
# effects would add the go again ability to an attack you control.
#
# Rule 6.3.2: Stage order is defined by how an effect applies to the object.
# Stage 1: Effects that modify copyable properties.
# Stage 2: Effects that modify or are dependent on the controller.
# Stage 3: Effects that modify or are dependent on name, color strip, or text box.
# Stage 4: Effects that modify or are dependent on types or subtypes.
# Stage 5: Effects that modify or are dependent on supertypes.
# Stage 6: Effects that modify or are dependent on abilities.
# Stage 7: Effects that modify or are dependent on the base values of numeric properties.
# Stage 8: Effects and counters that modify or are dependent on the values of numeric properties.
#
# Rule 6.3.2a: An effect is dependent on a stage if the application of another effect
# in that stage would have changed the first application of this effect, and that stage
# is higher than or equal to the stage for this effect. Dependent effects are applied
# in the stage on which they are dependent.
#
# Example (6.3.2a): Thump: "If this card's {p} is greater than its base, it gets dominate
# and "When this hits a hero, they discard a card."" — dependent on stage 8 value of power,
# so applied in stage 8 (substage 7).
#
# Rule 6.3.2b: If an effect is dependent on two or more stages, it is applied at the
# highest of all those stages.
#
# Rule 6.3.2c: If separate parts of an effect are applied in different stages, the
# separate parts of the effect each apply in their respective stages.
#
# Rule 6.3.3: Substage order for stages 1-6: independent effects before dependent effects.
# For stages 7-8:
# Substage 1: Add/remove a numerical property.
# Substage 2: Independent effects that set the value.
# Substage 3: Independent effects that multiply the value.
# Substage 4: Independent effects that divide the value.
# Substage 5: Independent effects that add to the value.
# Substage 6: Independent effects that subtract from the value.
# Substage 7: Dependent effects.
#
# Rule 6.3.3a: If there are two or more effects in the same substage, the effects are
# applied using timestamp order.
#
# Rule 6.3.4: Timestamp order is defined by when an effect was first generated.
# Effects are applied in chronological timestamp order. Same timestamp: turn-player decides.
#
# Rule 6.3.4a: The timestamp of a layer-continuous effect is when its source resolves as a
# layer on the stack. The timestamp of a static-continuous effect is when the static ability
# becomes functional.
#
# Rule 6.3.4b: If two or more effects start to apply to an object at the same time,
# the turn-player decides the order. This decided order cannot be changed.
#
# Rule 6.3.4c: When a new effect is applied to an object in a given substage of ordered
# effects, that effect is ordered after the existing effects in that substage.
#
# Rule 6.3.5: Continuous effects are applied dynamically. If a new effect would apply,
# an effect no longer applies, or an effect is modified, all effects are recalculated
# automatically in stage order.
#
# Rule 6.3.5a: If an object is modified such that it becomes eligible/ineligible for
# another effect, that effect is added/removed to the set of effects in that stage/substage.
#
# Example (6.3.5a): Minnowism: "The next attack action card with 3 or less base {p} you
# play this turn gets +3{p}." If an attack has 6 base power, reduced to 3 in stage 7,
# it becomes eligible for Minnowism's effect, which will be added and applied in stage 8.
#
# Rule 6.3.5b: If an object is modified by an effect that would make it applicable to
# another effect in a previous stage/substage, that other effect is not retroactively applied.
#
# Rule 6.3.6: Continuous effects that remove a property do not remove properties added
# by another effect.
#
# Example (6.3.6): Erase Face: removes class and talent types, but does not remove class
# and talent supertypes gained from other effects such as Brand with Cinderclaw.
#
# Rule 6.3.7: Continuous effects only prevent properties from being added, removed, or
# otherwise modified if they explicitly specify.
#
# Example (6.3.7): Hypothermia: "Attacks you control can't gain go again," prevents effects
# from adding go again, but does not remove go again if it is a base ability.

Feature: Section 6.3 - Continuous Effect Interactions
    As a game engine
    I need to correctly implement the staging system for continuous effect interactions
    So that multiple simultaneous effects are applied in the correct order and produce correct results

    # --- Rule 6.3.1: Rule-modifying effects applied before object-modifying effects ---

    Scenario: A rule-modifying continuous effect is applied before object-modifying effects
        Given a game is in progress with multiple continuous effects active
        And a rule-modifying effect prevents attacks from gaining go again
        And an object-modifying effect would grant go again to an attack
        When the effects are applied to the attack
        Then the rule-modifying effect is applied before the object-modifying effect
        And the attack does not gain go again

    Scenario: Two or more object-modifying effects are applied using the staging system
        Given a game is in progress with multiple continuous effects active
        And a stage 6 effect grants an ability to an object
        And a stage 8 effect adds to the power of the same object
        When the staging system applies both effects
        Then the stage 6 effect is applied before the stage 8 effect

    # --- Rule 6.3.2: Stage order ---

    Scenario: Stage 1 copyable property effects are applied before stage 4 type effects
        Given a game is in progress with multiple continuous effects active
        And a continuous effect in stage 1 modifies a copyable property
        And a continuous effect in stage 4 modifies the card's types
        When the staging system applies both effects
        Then the stage 1 effect is applied before the stage 4 effect

    Scenario: Stage 7 base numeric effects are applied before stage 8 numeric modifier effects
        Given a game is in progress with multiple continuous effects active
        And a stage 7 effect sets the base power of an attack to 4
        And a stage 8 effect adds 2 to the power of the same attack
        When the staging system applies both effects in ascending stage order
        Then the stage 7 effect is applied first setting base power to 4
        And the stage 8 effect is applied second resulting in total power of 6

    # --- Rule 6.3.2a: Dependent effects applied at dependent stage ---

    Scenario: A dependent effect is applied at the stage it depends on
        Given a game is in progress with multiple continuous effects active
        And an effect grants abilities to an attack if its power is greater than its base
        And this effect is dependent on the stage 8 power value
        When the staging system evaluates the effect
        Then the effect is classified as dependent on stage 8
        And the effect is applied in stage 8 substage 7

    Scenario: An independent ability effect is applied in stage 6 substage 1
        Given a game is in progress with multiple continuous effects active
        And an effect unconditionally grants an ability to an attack
        When the staging system evaluates the effect
        Then the effect is classified as independent
        And the effect is applied in stage 6 substage 1

    # --- Rule 6.3.2b: Effect dependent on multiple stages applied at highest ---

    Scenario: An effect dependent on two stages is applied at the highest stage
        Given a game is in progress with multiple continuous effects active
        And an effect is dependent on both stage 6 abilities and stage 8 power values
        When the staging system evaluates the effect
        Then the effect is applied at stage 8 the highest of the two dependent stages

    # --- Rule 6.3.2c: Separate parts of an effect applied in respective stages ---

    Scenario: Separate parts of a multi-part effect are applied in their respective stages
        Given a game is in progress with multiple continuous effects active
        And an effect has one part that modifies abilities in stage 6
        And another part of the same effect modifies power in stage 8
        When the staging system applies the effect
        Then the ability-modifying part is applied in stage 6
        And the power-modifying part is applied in stage 8

    # --- Rule 6.3.3: Substage order within stages 7-8 ---

    Scenario: In stage 8 an independent set effect is applied before an independent add effect
        Given a game is in progress with multiple continuous effects active
        And a stage 8 independent effect sets power to 5
        And a stage 8 independent effect adds 3 to power
        When the staging system applies both effects to the same object
        Then the set effect is applied first in substage 2
        And the add effect is applied second in substage 5
        And the resulting power is 8

    Scenario: In stages 1 to 6 independent effects are applied before dependent effects
        Given a game is in progress with multiple continuous effects active
        And an independent stage 6 ability effect unconditionally grants an ability
        And a dependent stage 6 ability effect conditionally grants an ability based on object properties
        When the staging system applies both effects
        Then the independent effect is applied in substage 1
        And the dependent effect is applied in substage 7

    Scenario: In stage 8 independent multiply effect is applied before independent add effect
        Given a game is in progress with multiple continuous effects active
        And a stage 8 independent multiply effect doubles the power
        And a stage 8 independent add effect adds 2 to the power
        When the staging system applies both effects to an object with base power of 3
        Then the multiply effect is applied first in substage 3
        And the add effect is applied second in substage 5
        And the resulting power is 8

    # --- Rule 6.3.3a / 6.3.4: Timestamp order for same substage ---

    Scenario: Two effects in the same substage are applied in timestamp order
        Given a game is in progress with multiple continuous effects active
        And a stage 8 add effect was generated at timestamp 1
        And a stage 8 add effect was generated at timestamp 2
        When the staging system applies both effects
        Then the effect with timestamp 1 is applied before the effect with timestamp 2

    # --- Rule 6.3.4a: Timestamp definitions ---

    Scenario: The timestamp of a layer-continuous effect is when its source resolves
        Given a game is in progress with multiple continuous effects active
        And a card resolves on the stack at game time 100 generating a layer-continuous effect
        When the staging system records the timestamp of the effect
        Then the timestamp of the layer-continuous effect is game time 100

    Scenario: The timestamp of a static-continuous effect is when its source ability becomes functional
        Given a game is in progress with multiple continuous effects active
        And a static ability becomes functional at game time 200
        When the staging system records the timestamp of the static-continuous effect
        Then the timestamp of the static-continuous effect is game time 200

    # --- Rule 6.3.4b: Same timestamp: turn-player decides order once ---

    Scenario: When two effects have the same timestamp the turn-player decides application order
        Given a game is in progress with multiple continuous effects active
        And two continuous effects start applying to an object at the same time
        When the turn-player decides the order of those effects
        Then that decided order is used for those effects in all substages

    Scenario: The turn-player cannot change the order after it has been decided
        Given a game is in progress with multiple continuous effects active
        And two same-timestamp effects have been ordered by the turn-player
        When the turn-player attempts to change the decided order
        Then the order change is rejected and the original order is maintained

    # --- Rule 6.3.4c: New effect ordered after existing effects in same substage ---

    Scenario: A new effect applied to an object in a substage is ordered after existing effects
        Given a game is in progress with multiple continuous effects active
        And two stage 8 add effects are already ordered in the substage for an object
        And a new stage 8 add effect is then applied to the same object
        When the staging system inserts the new effect
        Then the new effect is ordered after the two existing effects in that substage

    # --- Rule 6.3.5: Dynamic recalculation ---

    Scenario: All effects are recalculated when a new effect is applied
        Given a game is in progress with multiple continuous effects active
        And a stage 8 add effect of +2 power is active on an attack
        When a new stage 8 add effect of +3 power is applied to the same attack
        Then all effects are recalculated in staging order
        And the attack's power reflects contributions from both effects

    # --- Rule 6.3.5a: Eligibility changes trigger addition/removal of effects ---

    Scenario: An object becoming eligible for an effect causes that effect to be added
        Given a game is in progress with multiple continuous effects active
        And a stage 8 effect grants +3 power to attacks with 3 or less base power
        And an attack currently has base power of 6 making it ineligible for that effect
        And a stage 7 effect reduces the attack's base power to 3
        When the staging system processes stage 7 first then stage 8
        Then the attack becomes eligible for the stage 8 effect after stage 7 processing
        And the stage 8 effect is added and applied granting +3 power

    # --- Rule 6.3.5b: Previous stage effects not retroactively applied ---

    Scenario: An object modified in stage 8 does not retroactively trigger stage 6 effects
        Given a game is in progress with multiple continuous effects active
        And a stage 6 effect grants an ability only to objects with power above 5
        And an attack has base power of 3 making it ineligible for the stage 6 effect
        And a stage 8 effect increases the attack's power to 6
        When the staging system applies effects in order
        Then the stage 6 effect is not retroactively applied after the stage 8 modification
        And the attack does not gain the stage-6 ability

    # --- Rule 6.3.6: Removing a property does not affect properties added by other effects ---

    Scenario: A remove-property effect does not remove properties added by another effect
        Given a game is in progress with multiple continuous effects active
        And an object has a class supertype added by a separate continuous effect
        And an effect removes all class supertypes from the object
        When both effects are applied
        Then the class supertype added by the separate effect is not removed
        And the object retains the class supertype from the other effect

    # --- Rule 6.3.7: Effects only prevent modification if they explicitly specify ---

    Scenario: A prevention effect only blocks modifications it explicitly specifies
        Given a game is in progress with multiple continuous effects active
        And a prevention effect explicitly prevents attacks from gaining go again
        And an attack has go again as a base ability
        When the effects are evaluated
        Then the prevention effect blocks effects from adding go again
        And the attack retains its base go again ability unaffected by the prevention

    Scenario: A prevention effect does not implicitly prevent other modifications
        Given a game is in progress with multiple continuous effects active
        And a prevention effect explicitly prevents attacks from gaining go again
        And an effect would give the attack +2 power
        When both effects are evaluated
        Then the prevention effect does not block the power modification
        And the attack gains the +2 power bonus
