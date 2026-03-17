# Feature file for Section 2.14: Type Box
# Reference: Flesh and Blood Comprehensive Rules Section 2.14
#
# 2.14.1 The type box of a card determines the card's metatypes, supertypes,
#         types, and subtypes, typically located at the bottom of the card.
#         Type boxes are typically written in the format
#         "[METATYPES] [SUPERTYPES] [TYPE] [--- SUBTYPES]," where METATYPES
#         is zero or more metatypes, SUPERTYPES is zero or more supertypes,
#         TYPE is zero or more types, and SUBTYPES is zero or more subtypes.
#
# 2.14.1a If the SUPERTYPES of a type box is "Generic," the card has no
#          supertypes.
#
# 2.14.1b Hybrid cards are cards with SUPERTYPES written in the format
#          "[SUPERTYPES-1] / [SUPERTYPES-2]." A hybrid card can be included
#          in a player's card-pool as though it only has one of the supertypes
#          sets, SUPERTYPES-1 or SUPERTYPES-2, not both. [1.1.3] Otherwise,
#          hybrid cards have all of the supertypes specified by SUPERTYPES-1
#          and SUPERTYPES-2.

Feature: Section 2.14 - Type Box
    As a game engine
    I need to correctly parse and interpret type boxes
    So that cards' metatypes, supertypes, types, and subtypes are correctly determined

    # Test for Rule 2.14.1 - Type box determines the card's properties
    Scenario: Type box determines all card classification components
        Given a card with type box "Warrior Action - Attack"
        When the engine parses the type box
        Then the card has supertype "Warrior"
        And the card has type "Action"
        And the card has subtype "Attack"
        And the card has no metatypes

    # Test for Rule 2.14.1 - Type box with a metatype
    Scenario: Type box with a metatype component
        Given a card with type box "Dorinthea Warrior Action - Attack"
        When the engine parses the type box
        Then the card has metatype "Dorinthea"
        And the card has supertype "Warrior"
        And the card has type "Action"
        And the card has subtype "Attack"

    # Test for Rule 2.14.1 - Type box with no subtypes
    Scenario: Type box with no subtypes component
        Given a card with type box "Ninja Action"
        When the engine parses the type box
        Then the card has supertype "Ninja"
        And the card has type "Action"
        And the card has no subtypes

    # Test for Rule 2.14.1 - Type box format order: metatypes before supertypes before type
    Scenario: Type box components appear in correct order
        Given a card with type box "Katsu Ninja Action - Attack"
        When the engine parses the type box
        Then the type box ordering has metatype "Katsu" before supertype "Ninja"
        And the type box ordering has supertype "Ninja" before type "Action"
        And the type box ordering has type "Action" before subtype "Attack"

    # Test for Rule 2.14.1 - Card with no supertypes, no metatypes, and no subtypes
    Scenario: Type box with only a type
        Given a card with type box "Instant"
        When the engine parses the type box
        Then the card has type "Instant"
        And the card has no supertypes
        And the card has no metatypes
        And the card has no subtypes

    # Test for Rule 2.14.1 - Multiple supertypes in type box
    Scenario: Type box with multiple supertypes
        Given a card with type box "Warrior Draconic Action - Attack"
        When the engine parses the type box
        Then the card has supertype "Warrior"
        And the card has supertype "Draconic"
        And the card has 2 supertypes

    # Test for Rule 2.14.1 - Multiple subtypes in type box
    Scenario: Type box with multiple subtypes
        Given a card with type box "Ranger Action - Attack Arrow"
        When the engine parses the type box
        Then the card has subtype "Attack"
        And the card has subtype "Arrow"
        And the card has 2 subtypes

    # Test for Rule 2.14.1a - "Generic" means no supertypes
    Scenario: Generic type box means card has no supertypes
        Given a card with type box "Generic Action"
        When the engine parses the type box
        Then the card has no supertypes
        And the card has type "Action"

    # Test for Rule 2.14.1a - "Generic" is not itself a supertype
    Scenario: Generic keyword is not a supertype
        Given a card with type box "Generic Action"
        When the engine parses the type box
        Then the card does not have supertype "Generic"
        And the card has zero supertypes

    # Test for Rule 2.14.1a - Generic vs no supertypes equivalence
    Scenario: Generic type box is equivalent to having zero supertypes
        Given a card with type box "Generic Action"
        And a card with type box "Action"
        When both cards' supertypes are compared
        Then both cards have zero supertypes

    # Test for Rule 2.14.1b - Hybrid card definition
    Scenario: Hybrid card has slash-separated supertype sets
        Given a card with type box "Warrior / Wizard Action - Attack"
        When the engine parses the type box as a hybrid card
        Then the card is identified as a hybrid card
        And supertype set 1 is "Warrior"
        And supertype set 2 is "Wizard"

    # Test for Rule 2.14.1b - Hybrid card in Warrior hero's card-pool
    Scenario: Hybrid card can be included in card-pool matching first supertype set
        Given a hybrid card with supertype sets "Warrior" and "Wizard"
        And a Warrior hero
        When checking if the hybrid card can be included in the Warrior hero's card-pool
        Then the hybrid card is eligible for the card-pool
        And the first supertype set "Warrior" is the matching set

    # Test for Rule 2.14.1b - Hybrid card in Wizard hero's card-pool
    Scenario: Hybrid card can be included in card-pool matching second supertype set
        Given a hybrid card with supertype sets "Warrior" and "Wizard"
        And a Wizard hero
        When checking if the hybrid card can be included in the Wizard hero's card-pool
        Then the hybrid card is eligible for the card-pool
        And the second supertype set "Wizard" is the matching set

    # Test for Rule 2.14.1b - Hybrid card not in unmatching hero's card-pool
    Scenario: Hybrid card cannot be included in card-pool when neither supertype set matches
        Given a hybrid card with supertype sets "Warrior" and "Wizard"
        And a Ninja hero
        When checking if the hybrid card can be included in the Ninja hero's card-pool
        Then the hybrid card is not eligible for the card-pool

    # Test for Rule 2.14.1b - Hybrid card's card-pool eligibility uses one set, not both
    Scenario: Hybrid card card-pool check uses only one supertype set at a time
        Given a hybrid card with supertype sets "Warrior" and "Wizard"
        And a Warrior hero without the Wizard supertype
        When checking if the hybrid card can be included in the Warrior hero's card-pool
        Then the hybrid card is eligible for the card-pool
        And only one supertype set needs to match not both combined

    # Test for Rule 2.14.1b - Outside card-pool, hybrid card has all supertypes
    Scenario: Hybrid card has all supertypes outside of card-pool eligibility check
        Given a hybrid card with supertype sets "Warrior" and "Wizard"
        When the engine evaluates the hybrid card's supertypes normally
        Then the card has supertype "Warrior"
        And the card has supertype "Wizard"
        And the card has 2 supertypes

    # Test for Rule 2.14.1b - Hybrid card with multi-supertype sets
    Scenario: Hybrid card with multi-supertype sets matches if either set is a subset
        Given a hybrid card with supertype set 1 "Warrior Draconic" and supertype set 2 "Ninja Shadow"
        And a hero with supertypes "Warrior" and "Draconic"
        When checking if the hybrid card can be included in that hero's card-pool
        Then the hybrid card is eligible for the card-pool
        And supertype set 1 "Warrior Draconic" was the matching set

    # Test for Rule 2.14.1b - Hybrid card partial set match is not enough
    Scenario: Hybrid card with partial set match is not eligible
        Given a hybrid card with supertype set 1 "Warrior Draconic" and supertype set 2 "Ninja Shadow"
        And a hero with only supertype "Warrior"
        When checking if the hybrid card can be included in that hero's card-pool
        Then the hybrid card is not eligible for the card-pool
        And neither full supertype set matches the hero's supertypes
