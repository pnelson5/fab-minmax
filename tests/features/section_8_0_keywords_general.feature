# Feature file for Section 8.0: Keywords - General
# Reference: Flesh and Blood Comprehensive Rules Section 8.0
#
# 8.0.1 A keyword is a reserved term or phrase that serves as a descriptive element
#         for rules and/or effects to reference or has some rules meaning.
#
# 8.0.2 A type keyword is a keyword used by a card's text box to describe the type
#         of an object.
#
# 8.0.3 A subtype keyword is a keyword used by a card's text box to describe the
#         subtype of an object.
#
# 8.0.4 An ability keyword is a keyword that substitutes for the rules text of an
#         ability.
#
# 8.0.5 A label keyword is a keyword that groups abilities with common effects.
#         A label keyword and its ability are typically written in the format
#         "[KEYWORD] - [ABILITY]."
#
# 8.0.6 An effect keyword is a keyword that substitutes for the rules text of an
#         effect.
#
# 8.0.6a When a discrete keyword effect is generated, or when a continuous effect
#          is applied, it produces a corresponding event of that keyword.
#
# 8.0.7 A token keyword is a keyword that refers to a specific token. A token
#         keyword is typically written in the format "[KEYWORD] token."

Feature: Section 8.0 - Keywords General
    As a game engine
    I need to correctly identify and classify keyword types
    So that rules can reference keywords and their meanings are applied correctly

    # Rule 8.0.1 - Keywords are reserved terms with rules meaning

    Scenario: A keyword is a reserved term with rules meaning
        Given the game rules define keywords as reserved terms
        When a keyword appears in a card's text box or game effect
        Then it serves as a descriptive element for rules and effects to reference
        And it has a defined rules meaning

    Scenario: Keywords can be referenced by rules and effects
        Given a keyword exists in the rules system
        When a rule or effect references that keyword by name
        Then the keyword's rules meaning applies

    # Rule 8.0.2 - Type keywords describe object types

    Scenario: A type keyword describes the type of an object
        Given a card has a type keyword in its text box
        When the game evaluates the type of the object
        Then the type keyword identifies the card's type

    Scenario: Type keywords belong to the set of recognized type keywords
        Given the game has a defined set of type keywords
        When a type keyword appears on a card
        Then it is one of the recognized type keywords defined in the rules

    # Rule 8.0.3 - Subtype keywords describe object subtypes

    Scenario: A subtype keyword describes the subtype of an object
        Given a card has a subtype keyword in its text box
        When the game evaluates the subtype of the object
        Then the subtype keyword identifies the card's subtype

    # Rule 8.0.4 - Ability keywords substitute for rules text

    Scenario: An ability keyword substitutes for the rules text of an ability
        Given a card has an ability keyword
        When the game processes that ability
        Then the ability keyword expands to its corresponding rules text
        And the full rules text of the ability is applied

    Scenario: Multiple ability keywords can appear on a single card
        Given a card has multiple ability keywords
        When the game processes the card
        Then each ability keyword independently substitutes for its rules text

    # Rule 8.0.5 - Label keywords group abilities

    Scenario: A label keyword groups abilities with common effects
        Given a card has a label keyword followed by an ability
        When the game identifies the label keyword
        Then the keyword groups the associated ability under that label

    Scenario: Label keyword and ability are written in the standard format
        Given a card has the format "[KEYWORD] - [ABILITY]"
        When the game parses the card text
        Then the text before the dash is recognized as the label keyword
        And the text after the dash is recognized as the grouped ability

    # Rule 8.0.6 - Effect keywords substitute for effect rules text

    Scenario: An effect keyword substitutes for the rules text of an effect
        Given a game effect uses an effect keyword
        When the game resolves the effect
        Then the effect keyword expands to its corresponding rules text
        And the full effect is applied according to that rules text

    # Rule 8.0.6a - Discrete keyword effects produce corresponding events

    Scenario: A discrete keyword effect generates a corresponding event
        Given a discrete keyword effect is generated
        When the effect takes place
        Then a corresponding event of that keyword is produced
        And effects that trigger from that event can respond

    Scenario: Applying a continuous effect keyword produces a corresponding event
        Given a continuous effect keyword is applied
        When the continuous effect is applied to an object
        Then a corresponding continuous keyword event is produced
        And effects that trigger from the continuous keyword event can respond

    # Rule 8.0.7 - Token keywords refer to specific tokens

    Scenario: A token keyword refers to a specific token
        Given a token keyword exists in the rules
        When the token keyword is referenced in a card effect
        Then it refers to the specific token defined for that keyword

    Scenario: Token keywords are written in the standard format
        Given an effect creates a token using a token keyword
        When the game parses the token keyword format
        Then the keyword followed by "token" identifies the token type to create
