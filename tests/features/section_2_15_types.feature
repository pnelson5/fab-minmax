# Feature file for Section 2.15: Types
# Reference: Flesh and Blood Comprehensive Rules Section 2.15
#
# 2.15.1 Types are a collection of type keywords. The types of a card
#         determine whether the card is a hero-, token-, deck-, or arena-card,
#         and how a deck-card may be played.
#
# 2.15.2 An object can have zero or more types.
#
# 2.15.3 The type of a card is determined by its type box. The type is
#         printed after the card's supertypes, and before a long dash and
#         subtypes (if any).
#
# 2.15.4 The types of an activated-layer or triggered-layer are the same as
#         the types of its source.
#
# 2.15.4a The types of an activated ability layer include the types determined
#          by the activated ability. [5.2.1]
#
# 2.15.5 An object can gain or lose types from rules and/or effects.
#
# 2.15.6 Types are functional keywords and add additional rules to an object.
#
# 2.15.6a The type keywords are Action, Attack Reaction, Block, Companion,
#          Defense Reaction, Demi-Hero, Equipment, Hero, Instant, Macro,
#          Mentor, Resource, Token, and Weapon. [8.1]

Feature: Section 2.15 - Types
    As a game engine
    I need to correctly implement the types property rules
    So that card classification, layer type inheritance, and type-based rules
    resolve correctly

    # Test for Rule 2.15.1 - Types determine card classification (deck-card)
    Scenario: Action type makes a card a deck-card
        Given a card with type "Action"
        When the engine determines the card's classification
        Then the card is classified as a deck-card
        And the card may start in a player's deck

    # Test for Rule 2.15.1 - Types determine how deck-cards may be played
    Scenario: Types determine how a deck-card may be played
        Given a card with type "Action"
        And a card with type "Instant"
        When the engine checks how each card may be played
        Then the Action card may only be played during the action phase
        And the Instant card may be played outside the action phase

    # Test for Rule 2.15.1 - Hero type makes a hero-card
    Scenario: Hero type makes a card a hero-card
        Given a card with type "Hero"
        When the engine determines the card's classification
        Then the card is classified as a hero-card
        And the card starts the game as a player's hero

    # Test for Rule 2.15.1 - Token type makes a token-card
    Scenario: Token type makes a card a token-card
        Given a card with type "Token"
        When the engine determines the card's classification
        Then the card is classified as a token-card
        And the card is not considered part of a player's card-pool

    # Test for Rule 2.15.1 - Equipment type makes an arena-card
    Scenario: Equipment type makes a card an arena-card
        Given a card with type "Equipment"
        When the engine determines the card's classification
        Then the card is classified as an arena-card
        And the card cannot start in a player's deck

    # Test for Rule 2.15.1 - Weapon type makes an arena-card
    Scenario: Weapon type makes a card an arena-card via weapon type
        Given a card with type "Weapon"
        When the engine determines the card's classification
        Then the card is classified as an arena-card

    # Test for Rule 2.15.2 - An object can have zero types
    Scenario: Object with zero types
        Given a card with no printed type
        When the engine reads the card's types
        Then the card has zero types
        And the card is still a valid game object

    # Test for Rule 2.15.2 - An object can have exactly one type
    Scenario: Object can have exactly one type
        Given a card with type "Action"
        When the engine counts the card's types
        Then the card has exactly 1 type
        And the type name is "Action"

    # Test for Rule 2.15.2 - An object can have multiple types
    Scenario: Object can have multiple types
        Given a card with types "Action" and "Attack Reaction"
        When the engine reads the card's types
        Then the card has exactly 2 types
        And the card has type "Action"
        And the card has type "Attack Reaction"

    # Test for Rule 2.15.3 - Type determined from type box
    Scenario: Type is determined from the type box
        Given a type box string "Warrior Action - Attack"
        When the engine parses the type box
        Then the parsed type is "Action"
        And the parsed supertype is "Warrior"
        And the parsed subtype is "Attack"

    # Test for Rule 2.15.3 - Type printed after supertypes, before subtypes
    Scenario: Type box components appear in correct order
        Given a type box string "Ninja Action - Attack"
        When the engine parses the type box
        Then the type "Action" appears after supertype "Ninja"
        And the type "Action" appears before subtype "Attack"

    # Test for Rule 2.15.4 - Activated-layer inherits source types
    Scenario: Activated-layer inherits types from its source
        Given a card with type "Action"
        When an activated-layer is created from that card's ability
        Then the activated-layer has type "Action"
        And the layer types match the source card types

    # Test for Rule 2.15.4 - Triggered-layer inherits source types
    Scenario: Triggered-layer inherits types from its source
        Given a card with types "Action" and "Attack Reaction"
        When a triggered-layer is created by that card's triggered effect
        Then the triggered-layer has type "Action"
        And the triggered-layer has type "Attack Reaction"

    # Test for Rule 2.15.4 - Layer from no-type source has no types
    Scenario: Layer from no-type source has zero types
        Given a card with no printed type
        When an activated-layer is created from that card's ability
        Then the activated-layer has zero types

    # Test for Rule 2.15.4a - Activated ability layer includes additional types
    Scenario: Activated ability layer includes types from the activated ability
        Given a card with type "Equipment"
        And the card has an activated ability that creates a layer with type "Action"
        When the activated ability layer is created
        Then the activated ability layer has type "Equipment" from the source
        And the activated ability layer also has type "Action" from the ability itself

    # Test for Rule 2.15.5 - Object can gain a type
    Scenario: Object gains a type from an effect
        Given a card with type "Action"
        When an effect grants the card the type "Attack Reaction"
        Then the card now has type "Action"
        And the card now has type "Attack Reaction"
        And the card went from 1 type to 2 types

    # Test for Rule 2.15.5 - Object can lose a type
    Scenario: Object loses a type from an effect
        Given a card with types "Action" and "Attack Reaction"
        When an effect removes the type "Attack Reaction"
        Then the card still has type "Action"
        And the card no longer has type "Attack Reaction"
        And the card went from 2 types to 1 type

    # Test for Rule 2.15.6 - Types are functional keywords
    Scenario: Types are functional keywords that add additional rules
        Given a card with type "Action"
        When the engine checks whether types are functional
        Then the type "Action" is classified as a functional keyword
        And the type "Action" adds additional rules to the card

    # Test for Rule 2.15.6 - Non-functional keywords comparison
    Scenario: Types are functional unlike traits and non-functional subtypes
        Given a card with type "Action"
        And a card with supertype "Warrior"
        When the engine compares functional status
        Then the type "Action" is functional
        And the supertype "Warrior" is non-functional

    # Test for Rule 2.15.6a - All 14 type keywords recognized
    Scenario: All 14 type keywords are recognized
        Given the type keyword registry
        When the engine lists all recognized type keywords
        Then there are exactly 14 type keywords
        And "Action" is a recognized type keyword
        And "Attack Reaction" is a recognized type keyword
        And "Block" is a recognized type keyword
        And "Companion" is a recognized type keyword
        And "Defense Reaction" is a recognized type keyword
        And "Demi-Hero" is a recognized type keyword
        And "Equipment" is a recognized type keyword
        And "Hero" is a recognized type keyword
        And "Instant" is a recognized type keyword
        And "Macro" is a recognized type keyword
        And "Mentor" is a recognized type keyword
        And "Resource" is a recognized type keyword
        And "Token" is a recognized type keyword
        And "Weapon" is a recognized type keyword

    # Test for Rule 2.15.6a - Deck-card types are those defined in 1.3.2c
    Scenario: Deck-card types are Action, Attack Reaction, Block, Defense Reaction, Instant, Mentor, Resource
        Given the type keyword registry
        When the engine identifies which types make a card a deck-card
        Then "Action" makes a deck-card
        And "Attack Reaction" makes a deck-card
        And "Block" makes a deck-card
        And "Defense Reaction" makes a deck-card
        And "Instant" makes a deck-card
        And "Mentor" makes a deck-card
        And "Resource" makes a deck-card
        And "Equipment" does not make a deck-card
        And "Hero" does not make a deck-card
