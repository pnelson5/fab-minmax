# Feature file for Section 2.11: Supertypes
# Reference: Flesh and Blood Comprehensive Rules Section 2.11
#
# 2.11.1 Supertypes are a collection of supertype keywords. The supertypes of a
#         card determine whether a card can be included in a player's card-pool.
#
# 2.11.2 An object can have zero or more supertypes.
#
# 2.11.3 The supertypes of a card are determined by its type box. Supertypes are
#         printed before the card's type (if any).
#
# 2.11.4 The supertypes of an activated-layer or triggered-layer are the same as
#         the supertypes of its source.
#
# 2.11.5 An object can gain or lose supertypes from rules and/or effects.
#
# 2.11.6 Supertypes are non-functional keywords and do not add additional rules to
#         an object. A supertype is either a class or a talent.
#
# 2.11.6a The class supertype keywords are Adjudicator, Assassin, Bard, Brute,
#          Guardian, Illusionist, Mechanologist, Merchant, Necromancer, Ninja,
#          Pirate, Ranger, Runeblade, Shapeshifter, Thief, Warrior, and Wizard.
#
# 2.11.6b The talent supertype keywords are Chaos, Draconic, Earth, Elemental,
#          Ice, Light, Lightning, Mystic, Revered, Reviled, Royal, and Shadow.

Feature: Section 2.11 - Supertypes
    As a game engine
    I need to correctly implement the supertype property
    So that card-pool validation and supertype-based effects work correctly

    # Test for Rule 2.11.1 - Supertypes determine card-pool inclusion
    Scenario: Supertypes determine card-pool inclusion
        Given a card with supertypes "Warrior"
        And a hero with supertype "Warrior"
        When the engine checks if the card can be included in the hero's card-pool
        Then the card is eligible for the card-pool

    # Test for Rule 2.11.1 - Non-matching supertypes prevent card-pool inclusion
    Scenario: Non-matching supertypes prevent card-pool inclusion
        Given a card with supertypes "Wizard"
        And a hero with supertype "Warrior"
        When the engine checks if the card can be included in the hero's card-pool
        Then the card is not eligible for the card-pool

    # Test for Rule 2.11.2 - An object can have zero supertypes
    Scenario: Card with zero supertypes has no supertypes property values
        Given a card with no supertypes
        When the engine reads the supertypes of the card
        Then the card has zero supertypes
        And the card is still a valid game object

    # Test for Rule 2.11.2 - An object can have exactly one supertype
    Scenario: Card can have exactly one supertype
        Given a card with supertypes "Warrior"
        When the engine reads the supertypes of the card
        Then the card has exactly 1 supertype
        And the card has supertype "Warrior"

    # Test for Rule 2.11.2 - An object can have multiple supertypes
    Scenario: Card can have multiple supertypes
        Given a card with supertypes "Warrior" and "Draconic"
        When the engine reads the supertypes of the card
        Then the card has exactly 2 supertypes
        And the card has supertype "Warrior"
        And the card has supertype "Draconic"

    # Test for Rule 2.11.3 - Supertypes come from type box
    Scenario: Supertypes are determined from the type box
        Given a card with type box "Warrior Action - Attack"
        When the engine parses the type box
        Then the card has supertype "Warrior"
        And the card type is "Action"
        And the card subtype is "Attack"

    # Test for Rule 2.11.3 - Supertypes printed before card type
    Scenario: Supertypes are printed before the card type in the type box
        Given a type box parse result for "Ninja Action - Attack"
        When the engine parses the type box
        Then the type box order shows supertypes before the type

    # Test for Rule 2.11.4 - Activated-layer inherits source supertypes
    Scenario: Activated-layer inherits supertypes from its source
        Given a card with supertypes "Warrior"
        And an activated-layer is created from that card
        When the engine reads the supertypes of the activated-layer
        Then the activated-layer has supertype "Warrior"

    # Test for Rule 2.11.4 - Triggered-layer inherits source supertypes
    Scenario: Triggered-layer inherits supertypes from its source
        Given a card with supertypes "Wizard" and "Shadow"
        And a triggered-layer is created from that card
        When the engine reads the supertypes of the triggered-layer
        Then the triggered-layer has supertype "Wizard"
        And the triggered-layer has supertype "Shadow"

    # Test for Rule 2.11.4 - Layer from no-supertype source has no supertypes
    Scenario: Layer from no-supertype source inherits no supertypes
        Given a card with no supertypes
        And an activated-layer is created from that card
        When the engine reads the supertypes of the activated-layer
        Then the activated-layer has zero supertypes

    # Test for Rule 2.11.5 - An object can gain a supertype
    Scenario: An object can gain a supertype from an effect
        Given a card with no supertypes
        When an effect grants the card the supertype "Warrior"
        Then the card has supertype "Warrior"
        And the card has exactly 1 supertype

    # Test for Rule 2.11.5 - An object can lose a supertype
    Scenario: An object can lose a supertype from an effect
        Given a card with supertypes "Warrior" and "Draconic"
        When an effect removes the supertype "Draconic" from the card
        Then the card no longer has supertype "Draconic"
        And the card still has supertype "Warrior"

    # Test for Rule 2.11.6 - Supertypes are non-functional (don't add additional rules)
    Scenario: Supertypes are non-functional keywords
        Given a card with supertypes "Guardian"
        When the engine checks the supertypes for additional rules
        Then no additional rules are added by the supertypes
        And the supertype is classified as non-functional

    # Test for Rule 2.11.6 - Supertype is either a class or a talent
    Scenario: Warrior is a class supertype keyword
        Given the supertype "Warrior"
        When the engine classifies the supertype
        Then the supertype category is "class"

    # Test for Rule 2.11.6 - Draconic is a talent supertype keyword
    Scenario: Draconic is a talent supertype keyword
        Given the supertype "Draconic"
        When the engine classifies the supertype
        Then the supertype category is "talent"

    # Test for Rule 2.11.6a - All class supertypes are recognized
    Scenario: All class supertype keywords are recognized
        When the engine lists all class supertypes
        Then the class supertypes include "Adjudicator"
        And the class supertypes include "Assassin"
        And the class supertypes include "Bard"
        And the class supertypes include "Brute"
        And the class supertypes include "Guardian"
        And the class supertypes include "Illusionist"
        And the class supertypes include "Mechanologist"
        And the class supertypes include "Merchant"
        And the class supertypes include "Necromancer"
        And the class supertypes include "Ninja"
        And the class supertypes include "Pirate"
        And the class supertypes include "Ranger"
        And the class supertypes include "Runeblade"
        And the class supertypes include "Shapeshifter"
        And the class supertypes include "Thief"
        And the class supertypes include "Warrior"
        And the class supertypes include "Wizard"
        And there are exactly 17 class supertypes

    # Test for Rule 2.11.6b - All talent supertypes are recognized
    Scenario: All talent supertype keywords are recognized
        When the engine lists all talent supertypes
        Then the talent supertypes include "Chaos"
        And the talent supertypes include "Draconic"
        And the talent supertypes include "Earth"
        And the talent supertypes include "Elemental"
        And the talent supertypes include "Ice"
        And the talent supertypes include "Light"
        And the talent supertypes include "Lightning"
        And the talent supertypes include "Mystic"
        And the talent supertypes include "Revered"
        And the talent supertypes include "Reviled"
        And the talent supertypes include "Royal"
        And the talent supertypes include "Shadow"
        And there are exactly 12 talent supertypes

    # Test for Rule 2.11.1 - Generic means no supertypes (from cross-ref Rule 2.14.1a)
    Scenario: Generic type box means card has no supertypes
        Given a card with type box "Generic Action"
        When the engine parses the type box
        Then the card has zero supertypes

    # Test for Rule 2.11.1 - Generic card can be in any card-pool
    Scenario: Card with no supertypes can be in any card-pool
        Given a card with no supertypes
        And a hero with supertype "Warrior"
        When the engine checks if the card can be included in the hero's card-pool
        Then the card is eligible for the card-pool

    # Test for Rule 2.11.2 - Warrior/Draconic multi-class/talent card pool inclusion
    Scenario: Card with Warrior supertype valid for Warrior hero with Draconic talent
        Given a card with supertypes "Warrior" and "Draconic"
        And a hero with supertypes "Warrior" and "Draconic"
        When the engine checks if the card can be included in the hero's card-pool
        Then the card is eligible for the card-pool

    # Test for Rule 2.11.1 - Supertype subset validation (card supertypes must be subset of hero supertypes)
    Scenario: Card with Wizard supertype is invalid for Warrior hero
        Given a card with supertypes "Wizard"
        And a hero with supertype "Warrior"
        When the engine checks if the card can be included in the hero's card-pool
        Then the card is not eligible for the card-pool

    # Test for Rule 2.11.2 - Multi-supertype card must have ALL supertypes match
    Scenario: Card with multiple supertypes needs all to be subset of hero supertypes
        Given a card with supertypes "Warrior" and "Draconic"
        And a hero with supertype "Warrior"
        When the engine checks if the card can be included in the hero's card-pool
        Then the card is not eligible for the card-pool
