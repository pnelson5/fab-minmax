# Feature file for Section 2.0: General (Object Properties)
# Reference: Flesh and Blood Comprehensive Rules Section 2.0
#
# 2.0.1 A property is an attribute of an object that defines how the object interacts
#        with the rules and effects of the game. There are 13 properties an object may have:
#        abilities, color strip, cost, defense, intellect, life, name, pitch, power,
#        subtypes, supertypes, text box, and type.
#
# 2.0.1a An ability is a property, not an object. However, activated abilities have the
#         object properties cost and type, for the purposes of rules and effects.
#
# 2.0.2 The properties of a card or macro are determined by the true text of the card or
#        macro on https://cards.fabtcg.com.
#
# 2.0.3 A numeric property is a property that has a numeric value. The value of some
#        numeric properties can be modified by effects and/or counters to produce a
#        modified value.
#
# 2.0.3a An effect that modifies the value of a numeric property does not modify the
#         base value of that property unless otherwise specified by the effect.
#         An effect that specifies an object to "gain," "get," "have," or "lose" a
#         property-related value, modifies the value of the property but does not
#         change the base value unless it specifically uses the term "base."
#
# 2.0.3b If the base value of a numeric property would be modified by an effect, it is
#         not considered to increase or decrease the value for the purposes of effects
#         that reference gaining or losing respectively. Otherwise, if the non-base value
#         would be modified, it is considered to increase or decrease the value.
#         Example: Korshem - increasing non-base {p} counts as "gaining {p}".
#         Example: Big Bully - doubling base {p} is NOT "gaining {p}".
#
# 2.0.3c A numeric property cannot have a negative base or modified value. If one or more
#         effects would set or reduce the base or modified value of a numeric property to
#         be less than zero, instead they set or reduce it to zero.
#
# 2.0.3d A +1 or -1 property-related counter on an object, modifies the value of the
#         property but does not change the base value.
#
# 2.0.4 An object is considered to have gained a property, or part of a property, if it
#        did not have that property/part before, but currently does. An object is
#        considered to have lost a property, or part of a property, if it had that
#        property/part but currently does not. Gaining or losing a property is not
#        considered to increase or decrease the value for the purposes of effects that
#        reference gaining or losing respectively.
#
# 2.0.5 The source of a property is the object of which the property is an attribute.

Feature: Section 2.0 - General Object Properties
    As a game engine
    I need to correctly implement object property rules
    So that properties of cards and other game objects are tracked and modified correctly

    # Rule 2.0.1 - Properties are attributes of objects
    Scenario: Card has recognized game properties
        Given a card named "Lunging Press" with power 4 and defense 3 and cost 1
        When the game checks the card's properties
        Then the card should have a "name" property
        And the card should have a "power" property
        And the card should have a "defense" property
        And the card should have a "cost" property
        And the card should have a "type" property

    # Rule 2.0.1 - There are exactly 13 properties
    Scenario: There are 13 possible object properties
        Given the game engine's property system
        When the engine lists all possible object properties
        Then the property list should contain exactly 13 property names
        And the properties should include "abilities"
        And the properties should include "color"
        And the properties should include "cost"
        And the properties should include "defense"
        And the properties should include "intellect"
        And the properties should include "life"
        And the properties should include "name"
        And the properties should include "pitch"
        And the properties should include "power"
        And the properties should include "subtypes"
        And the properties should include "supertypes"
        And the properties should include "text_box"
        And the properties should include "type"

    # Rule 2.0.1a - Ability is a property, not an object
    Scenario: An ability is a property not an object
        Given a card with the keyword "go again"
        When the game checks if "go again" is a property of the card
        Then "go again" should be recognized as a property of the card
        And "go again" should not be recognized as a game object

    # Rule 2.0.1a - Activated abilities have cost and type properties
    Scenario: An activated ability has cost and type properties
        Given an activated ability with a resource cost of 2
        When the game checks the activated ability's properties
        Then the activated ability should have a "cost" property equal to 2
        And the activated ability should have a "type" property

    # Rule 2.0.2 - Card properties determined by official card text
    Scenario: Card properties come from the card definition
        Given a card template defined with power 6 cost 3 defense 2
        When the game reads the card's properties
        Then the card power should be 6
        And the card cost should be 3
        And the card defense should be 2

    # Rule 2.0.3 - Numeric properties have numeric values
    Scenario: Numeric properties have numeric values that can be read
        Given a card named "Surging Strike" with power 3
        When the game reads the card's numeric properties
        Then the power property value should be 3
        And power should be classified as a numeric property

    # Rule 2.0.3a - Effects modify value not base value
    Scenario: Effect modifies card power without changing base power
        Given a card with base power 4
        And an effect that gives the card "+2 power"
        When the non-base power effect is applied to the card
        Then the card's effective power should be 6
        And the card's base power should still be 4

    # Rule 2.0.3a - "Gain" keyword modifies value not base
    Scenario: Effect using gain keyword modifies non-base power value
        Given a card with base power 3
        And an effect that makes the card "gain 2 power"
        When the gain power effect is applied to the card
        Then the card's effective power should be 5
        And the card's base power should still be 3

    # Rule 2.0.3b - Modifying base value not considered gaining power
    Scenario: Doubling base power is not considered gaining power
        Given a card with base power 4
        And an effect that doubles the card's base power
        When the base-doubling effect is applied
        Then the card's base power should be 8
        And the modification should not be classified as "gaining power"

    # Rule 2.0.3b - Modifying non-base value is considered gaining power
    Scenario: Non-base power increase is considered gaining power
        Given a card with base power 3
        And an effect that increases the card's non-base power by 2
        When the non-base power increase effect is applied
        Then the modification should be classified as "gaining power"

    # Rule 2.0.3c - Numeric property cannot be negative
    Scenario: Numeric property cannot go below zero
        Given a card with base power 2
        And an effect that reduces the card's power by 5
        When the power reduction effect is applied
        Then the card's effective power should be 0
        And the card's effective power should not be negative

    # Rule 2.0.3c - Effect setting property to negative value capped at zero
    Scenario: Effect reducing defense to negative is capped at zero
        Given a card with base defense 1
        And an effect that reduces the card's defense by 3
        When the defense reduction effect is applied
        Then the card's effective defense should be 0

    # Rule 2.0.3d - Counter modifies value not base
    Scenario: A power counter modifies card power without changing base power
        Given a card with base power 4
        And a "+1 power" counter is placed on the card
        When the game calculates the card's power
        Then the card's effective power should be 5
        And the card's base power should still be 4

    # Rule 2.0.3d - Minus counter modifies value not base
    Scenario: A minus-power counter modifies card power without changing base
        Given a card with base power 4
        And a "-1 power" counter is placed on the card
        When the game calculates the card's power
        Then the card's effective power should be 3
        And the card's base power should still be 4

    # Rule 2.0.4 - Gaining a property means it didn't have it before
    Scenario: Card gains a property it did not previously have
        Given a card that does not have the "go again" property
        When an effect grants the card the "go again" property
        Then the card should be considered to have "gained go again"
        And the card now has the "go again" property

    # Rule 2.0.4 - Losing a property means it had it and no longer does
    Scenario: Card loses a property it previously had
        Given a card that has the "go again" property
        When an effect removes the card's "go again" property
        Then the card should be considered to have "lost go again"
        And the card no longer has the "go again" property

    # Rule 2.0.4 - Gaining a property is not same as increasing its value
    Scenario: Gaining a property is not the same as increasing property value
        Given a card that does not have the "dominate" property
        When an effect grants the card the "dominate" property
        Then the card should have "gained dominate"
        And this should not be classified as "increasing" the dominate value

    # Rule 2.0.5 - Source of a property is the object it belongs to
    Scenario: The source of a property is the card that has it
        Given a card named "Pummel" with power 9
        When the game identifies the source of the power property
        Then the source of the power property should be the "Pummel" card
