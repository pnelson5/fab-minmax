# Feature file for Section 1.15: Counters
# Reference: Flesh and Blood Comprehensive Rules Section 1.15
#
# 1.15.1 A counter is a physical marker placed on any public object. A counter is
#         not an object and does not have properties. The identity of a counter is
#         defined by its name, or its numerical value and symbol. Counters with the
#         same name, or value and symbol, are functionally identical and interchangeable.
#
# 1.15.2 When a counter is on an object, it modifies its properties and/or interacts
#         with effects.
#
# 1.15.2a A counter with a numerical value and symbol that corresponds to an object
#          property modifies that property of the object it is on. This modification
#          is considered a rule, not an effect, but does take place at the same time
#          as continuous effects that modify the object in the same way.
#
# 1.15.3 When an object ceases to exist, the counters on that object cease to exist.
#         When a counter is removed from an object it ceases to exist.
#
# 1.15.4 If a counter would be added to an object that has a diametrically opposing
#         counter on it, both diametrically opposing counters remain on the object.
#         Example: If a -1{p} counter is placed on an object with a +1{p} counter
#         on it, they both remain on the object. The counters do not cancel each other
#         out and they are not removed from the object simply because they are
#         diametrically opposing.

Feature: Section 1.15 - Counters
    As a game engine
    I need to correctly implement the counter system
    So that counters correctly track markers on objects and modify their properties

    # ============================================================
    # Rule 1.15.1 - Counters are physical markers; not objects; identity by name or value+symbol
    # ============================================================

    Scenario: A counter is a physical marker placed on a public object
        Given a card "Iron Citadel Shield" is in the arena
        When a "+1{d}" counter is added to "Iron Citadel Shield"
        Then "Iron Citadel Shield" has 1 counter on it
        And the counter is a physical marker on the card

    Scenario: A counter is not an object and has no properties
        Given a card "Courage of Bladehold" is in the arena
        When a "steam" counter is added to "Courage of Bladehold"
        Then the counter is not a game object
        And the counter does not have properties

    Scenario: Counter identity is defined by its name
        Given a card "Courage of Bladehold" is in the arena
        When a "steam" counter is added to "Courage of Bladehold"
        And another "steam" counter is added to "Courage of Bladehold"
        Then both "steam" counters are functionally identical
        And "Courage of Bladehold" has 2 "steam" counters on it

    Scenario: Counter identity is defined by numerical value and symbol
        Given a card "Iron Citadel Shield" is in the arena
        When a "+1{d}" counter is added to "Iron Citadel Shield"
        And another "+1{d}" counter is added to "Iron Citadel Shield"
        Then both "+1{d}" counters are functionally identical and interchangeable
        And "Iron Citadel Shield" has 2 "+1{d}" counters on it

    Scenario: Counters with same name are interchangeable
        Given two separate counters with name "steam" exist on a card
        Then the two "steam" counters are interchangeable

    Scenario: Counters with different names are not the same
        Given a card "Courage of Bladehold" is in the arena
        When a "steam" counter is added to "Courage of Bladehold"
        And a "rust" counter is added to "Courage of Bladehold"
        Then "Courage of Bladehold" has 1 "steam" counter and 1 "rust" counter
        And "steam" counter and "rust" counter have different identities

    # ============================================================
    # Rule 1.15.2 - Counter modifies properties and/or interacts with effects
    # ============================================================

    Scenario: A counter on an object modifies its properties
        Given a card "Iron Citadel Shield" is in the arena with defense 3
        When a "+1{d}" counter is added to "Iron Citadel Shield"
        Then the effective defense of "Iron Citadel Shield" is 4

    Scenario: A counter on an object can interact with effects
        Given a card "Courage of Bladehold" is in the arena
        And an effect watches for "steam" counters on objects
        When a "steam" counter is added to "Courage of Bladehold"
        Then the effect detects the "steam" counter on "Courage of Bladehold"

    # ============================================================
    # Rule 1.15.2a - Numerical value+symbol counter modifies property; treated as rule not effect
    # ============================================================

    Scenario: A plus power counter increases attack power
        Given a card "Brute Force" is in the arena with power 4
        When a "+1{p}" counter is added to "Brute Force"
        Then the effective power of "Brute Force" is 5

    Scenario: A minus power counter decreases attack power
        Given a card "Brute Force" is in the arena with power 4
        When a "-1{p}" counter is added to "Brute Force"
        Then the effective power of "Brute Force" is 3

    Scenario: A plus defense counter increases defense value
        Given a card "Iron Citadel Shield" is in the arena with defense 3
        When a "+2{d}" counter is added to "Iron Citadel Shield"
        Then the effective defense of "Iron Citadel Shield" is 5

    Scenario: Counter property modification is considered a rule not an effect
        Given a card "Iron Citadel Shield" is in the arena with defense 3
        When a "+1{d}" counter is added to "Iron Citadel Shield"
        Then the "+1{d}" counter modification is classified as a rule modification
        And the modification is not classified as an effect

    Scenario: Counter modification applies at the same time as continuous effects
        Given a card "Brute Force" is in the arena with power 4
        And a continuous effect gives "Brute Force" +2{p}
        When a "+1{p}" counter is added to "Brute Force"
        Then the effective power of "Brute Force" is 7
        And the counter modification applies at the same layer as the continuous effect

    Scenario: Multiple counters of the same type stack their modifications
        Given a card "Iron Citadel Shield" is in the arena with defense 3
        When three "+1{d}" counters are added to "Iron Citadel Shield"
        Then the effective defense of "Iron Citadel Shield" is 6

    # ============================================================
    # Rule 1.15.3 - Counters cease when object ceases; counters cease when removed
    # ============================================================

    Scenario: Counters cease to exist when the object ceases to exist
        Given a card "Iron Citadel Shield" is in the arena
        And a "+1{d}" counter is on "Iron Citadel Shield"
        When "Iron Citadel Shield" is destroyed and leaves the arena
        Then the "+1{d}" counter on "Iron Citadel Shield" ceases to exist

    Scenario: Multiple counters all cease when the object ceases
        Given a card "Iron Citadel Shield" is in the arena
        And three "+1{d}" counters are on "Iron Citadel Shield"
        When "Iron Citadel Shield" ceases to exist
        Then all counters on "Iron Citadel Shield" cease to exist

    Scenario: A removed counter ceases to exist
        Given a card "Courage of Bladehold" is in the arena
        And a "steam" counter is on "Courage of Bladehold"
        When the "steam" counter is removed from "Courage of Bladehold"
        Then the removed "steam" counter ceases to exist
        And "Courage of Bladehold" has 0 counters on it

    Scenario: Removing one counter leaves others intact
        Given a card "Courage of Bladehold" is in the arena
        And three "steam" counters are on "Courage of Bladehold"
        When one "steam" counter is removed from "Courage of Bladehold"
        Then "Courage of Bladehold" still has 2 "steam" counters on it

    # ============================================================
    # Rule 1.15.4 - Diametrically opposing counters both remain
    # ============================================================

    Scenario: Opposing counters both remain on the object
        Given a card "Brute Force" is in the arena
        And a "+1{p}" counter is on "Brute Force"
        When a "-1{p}" counter is added to "Brute Force"
        Then "Brute Force" has both a "+1{p}" counter and a "-1{p}" counter on it
        And neither counter is removed

    Scenario: Opposing counters do not cancel each other out
        Given a card "Brute Force" is in the arena with power 4
        And a "+1{p}" counter is on "Brute Force"
        When a "-1{p}" counter is added to "Brute Force"
        Then the effective power of "Brute Force" is 4
        And "Brute Force" still has both opposing counters

    Scenario: Multiple opposing counter pairs all remain on the object
        Given a card "Brute Force" is in the arena
        And two "+1{p}" counters are on "Brute Force"
        When two "-1{p}" counters are added to "Brute Force"
        Then "Brute Force" has 2 "+1{p}" counters and 2 "-1{p}" counters on it

    Scenario: Adding a second opposing counter after first opposing already present
        Given a card "Brute Force" is in the arena
        And a "+1{p}" counter and a "-1{p}" counter are both on "Brute Force"
        When another "+1{p}" counter is added to "Brute Force"
        Then "Brute Force" has 2 "+1{p}" counters and 1 "-1{p}" counters on it
