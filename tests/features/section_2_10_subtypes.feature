# Feature file for Section 2.10: Subtypes
# Reference: Flesh and Blood Comprehensive Rules Section 2.10
#
# 2.10.1 Subtypes are a collection of subtype keywords. The functional subtypes
#         of a card determine what additional rules apply to the card.
#
# 2.10.2 An object can have zero or more subtypes.
#
# 2.10.3 The subtypes of a card are determined by its type box. Subtypes (if any)
#         are printed after a long dash after the card's type.
#         Example: "Action - Attack" has subtype "Attack" after the long dash.
#
# 2.10.4 The subtypes of an activated-layer or triggered-layer are the same as
#         the subtypes of its source.
#
# 2.10.5 An object can gain or lose subtypes from rules and/or effects.
#
# 2.10.6 Subtypes are either functional or non-functional keywords. Functional
#         subtypes add additional rules to an object. Non-functional subtypes
#         do not add additional rules to an object.
#
# 2.10.6a The functional subtype keywords are (1H), (2H), Affliction, Ally,
#          Arrow, Ash, Attack, Aura, Construct, Figment, Invocation, Item,
#          Landmark, Off-Hand, and Quiver.
#
# 2.10.6b The non-functional subtypes keywords are Angel, Arms, Axe, Base,
#          Book, Bow, Brush, Cannon, Chest, Chi, Claw, Club, Cog, Dagger,
#          Demon, Dragon, Evo, Fiddle, Flail, Gem, Gun, Hammer, Head, Legs,
#          Lute, Mercenary, Orb, Pistol, Pit-Fighter, Polearm, Rock, Scepter,
#          Scroll, Scythe, Shuriken, Song, Staff, Sword, Trap, Wrench, and Young.

Feature: Section 2.10 - Subtypes
    As a game engine
    I need to correctly implement subtype rules
    So that card subtypes determine additional rules and are correctly tracked

    # Rule 2.10.1 - Subtypes are subtype keywords; functional subtypes add rules
    Scenario: Subtypes are subtype keywords that determine additional rules
        Given a card is created with the subtype "Attack"
        When the engine checks the subtypes of the attack-subtype card
        Then the attack-subtype card should have the "Attack" subtype
        And the "Attack" subtype should be recognized as a functional subtype

    # Rule 2.10.1 - Non-functional subtypes exist but don't add additional rules
    Scenario: Non-functional subtypes do not add additional rules to an object
        Given a card is created with the subtype "Sword"
        When the engine checks whether "Sword" is a functional subtype
        Then "Sword" should not be a functional subtype
        And the sword-subtype card should have the "Sword" subtype

    # Rule 2.10.2 - Object can have zero subtypes
    Scenario: Object with zero subtypes is valid
        Given a card is created with no subtypes
        When the engine checks the subtypes of the no-subtype card
        Then the no-subtype card should have zero subtypes
        And the no-subtype card should still be a valid game object

    # Rule 2.10.2 - Object can have exactly one subtype
    Scenario: Object can have exactly one subtype
        Given a card is created with exactly one subtype "Ally"
        When the engine checks the subtypes of the one-subtype card
        Then the one-subtype card should have exactly 1 subtype
        And the one-subtype card should have the "Ally" subtype

    # Rule 2.10.2 - Object can have multiple subtypes
    Scenario: Object can have multiple subtypes
        Given a card is created with subtypes "Attack" and "Arrow"
        When the engine checks the subtypes of the multi-subtype card
        Then the multi-subtype card should have exactly 2 subtypes
        And the multi-subtype card should have the "Attack" subtype
        And the multi-subtype card should have the "Arrow" subtype

    # Rule 2.10.3 - Subtypes determined by type box, printed after long dash
    Scenario: Subtypes are determined by the type box of the card
        Given a card is defined with type box "Action - Attack"
        When the engine parses the type box of the attack-action card
        Then the attack-action card type should be "Action"
        And the attack-action card subtype should be "Attack"

    # Rule 2.10.3 - Card type without subtype has no subtype
    Scenario: Card with no dash in type box has no subtype
        Given a card is defined with type box "Instant"
        When the engine parses the type box of the instant-only card
        Then the instant-only card should have no subtype from its type box

    # Rule 2.10.4 - Activated-layer inherits source subtypes
    Scenario: Activated-layer inherits subtypes from its source
        Given a card is created with the subtype "Ally" as a layer source
        And an activated-layer is created from the ally-source card
        When the engine checks the subtypes of the activated-ally-layer
        Then the activated-ally-layer should have the "Ally" subtype

    # Rule 2.10.4 - Triggered-layer inherits source subtypes
    Scenario: Triggered-layer inherits subtypes from its source
        Given a card is created with the subtype "Aura" as a layer source
        And a triggered-layer is created from the aura-source card
        When the engine checks the subtypes of the triggered-aura-layer
        Then the triggered-aura-layer should have the "Aura" subtype

    # Rule 2.10.4 - Layer from zero-subtype source has zero subtypes
    Scenario: Layer from source with no subtypes has no subtypes
        Given a card is created with no subtypes as a no-subtype-layer-source
        And an activated-layer is created from the no-subtype-layer-source card
        When the engine checks the subtypes of the no-subtype activated-layer
        Then the no-subtype activated-layer should have zero subtypes

    # Rule 2.10.5 - Object can gain subtypes from rules and effects
    Scenario: Object can gain a subtype from an effect
        Given a card is created with no subtypes
        And a gain-subtype effect grants the "Aura" subtype to the no-subtype card
        When the engine checks the subtypes of the card after gaining the subtype
        Then the card should now have the "Aura" subtype
        And the card should have exactly 1 subtype after gaining

    # Rule 2.10.5 - Object can lose subtypes from rules and effects
    Scenario: Object can lose a subtype from an effect
        Given a card is created with the subtype "Attack" and subtype "Arrow"
        And a lose-subtype effect removes the "Arrow" subtype from the two-subtype card
        When the engine checks the subtypes of the card after losing the subtype
        Then the card should no longer have the "Arrow" subtype
        And the card should still have the "Attack" subtype

    # Rule 2.10.6 - Functional subtypes add additional rules; non-functional do not
    Scenario: Functional subtype keywords include Attack
        Given the engine has a list of functional subtype keywords
        When the engine is queried for whether "Attack" is a functional subtype keyword
        Then "Attack" should be in the functional subtype keyword list

    # Rule 2.10.6a - Functional subtype keywords list
    Scenario: All functional subtype keywords are recognized
        Given the engine has the complete list of functional subtype keywords
        When the engine checks each known functional subtype keyword
        Then "(1H)" should be a functional subtype
        And "(2H)" should be a functional subtype
        And "Affliction" should be a functional subtype
        And "Ally" should be a functional subtype
        And "Arrow" should be a functional subtype
        And "Ash" should be a functional subtype
        And "Aura" should be a functional subtype
        And "Construct" should be a functional subtype
        And "Figment" should be a functional subtype
        And "Invocation" should be a functional subtype
        And "Item" should be a functional subtype
        And "Landmark" should be a functional subtype
        And "Off-Hand" should be a functional subtype
        And "Quiver" should be a functional subtype

    # Rule 2.10.6b - Non-functional subtypes include Sword, Bow, Staff, etc.
    Scenario: Non-functional subtype keywords include common weapon subtypes
        Given the engine has the complete list of non-functional subtype keywords
        When the engine checks each known non-functional subtype keyword
        Then "Sword" should be a non-functional subtype
        And "Bow" should be a non-functional subtype
        And "Staff" should be a non-functional subtype
        And "Dagger" should be a non-functional subtype
        And "Axe" should be a non-functional subtype

    # Rule 2.10.6 - Functional subtype count is exactly 15
    Scenario: There are exactly 15 functional subtype keywords
        Given the engine has the complete list of functional subtype keywords
        When the engine counts all functional subtype keywords
        Then there should be exactly 15 functional subtype keywords

    # Rule 2.10.6a - Attack is a functional subtype (not same as attack card)
    Scenario: Attack subtype adds functional rules to a card
        Given a card is created with the subtype "Attack" as the functional-attack card
        When the engine checks whether the functional-attack card's subtype adds rules
        Then the functional-attack-subtype should add additional rules
        And the "Attack" subtype should be functional

    # Rule 2.10.6b - Sword is non-functional (no additional rules)
    Scenario: Sword subtype does not add functional rules to a card
        Given a card is created with the subtype "Sword" as the non-functional-sword card
        When the engine checks whether the non-functional-sword card's subtype adds rules
        Then the non-functional-sword-subtype should not add additional rules

    # Rule 2.10.6a/6b - Functional and non-functional subtypes can coexist
    Scenario: A card can have both functional and non-functional subtypes
        Given a card is created with subtypes "Attack" and "Sword"
        When the engine checks the subtypes of the attack-and-sword card
        Then the attack-and-sword card should have the "Attack" subtype
        And the attack-and-sword card should have the "Sword" subtype
        And the functional subtypes of the attack-and-sword card should include only "Attack"

    # Rule 2.10.4 - Layer inherits multiple subtypes from source
    Scenario: Layer inherits multiple subtypes from source card
        Given a card is created with subtypes "Attack" and "Arrow" as an arrow-attack-source
        And an activated-layer is created from the arrow-attack-source card
        When the engine checks the subtypes of the arrow-attack activated-layer
        Then the arrow-attack activated-layer should have the "Attack" subtype
        And the arrow-attack activated-layer should have the "Arrow" subtype
