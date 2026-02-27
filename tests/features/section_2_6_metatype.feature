# Feature file for Section 2.6: Metatype
# Reference: Flesh and Blood Comprehensive Rules Section 2.6
#
# 2.6.1 Metatypes are a collection of metatype keywords. The metatypes of an
#        object determine whether it may be added to a game.
#
# 2.6.2 An object can have zero or more metatypes.
#
# 2.6.3 The metatype of a card is determined by its type box. The metatype is
#        printed before the card's supertypes.
#
# 2.6.4 The metatypes of an activated-layer or triggered-layer are the same as
#        the metatypes of its source.
#
# 2.6.5 An object cannot gain or lose metatypes.
#
# 2.6.6 Metatypes are either hero-metatypes or set-metatypes.
#        Hero-metatypes specify the moniker(s) of a hero, and the card can only
#        be included in a player's card-pool if it matches their hero's
#        moniker(s). Set-metatypes specify the name(s) of the set the object
#        can be used in as defined by tournament rules.

Feature: Section 2.6 - Metatype
    As a game engine
    I need to correctly implement metatype rules
    So that card-pool legality and game entry eligibility are enforced correctly

    # Rule 2.6.1 - Metatypes determine game-entry eligibility
    Scenario: Metatypes determine whether an object may be added to a game
        Given a card named Dorinthea Specialization Spell with hero-metatype "Dorinthea"
        And a hero named Dorinthea with moniker "Dorinthea"
        When the engine checks if the Dorinthea Specialization Spell may be added to a game
        Then the Dorinthea Specialization Spell should be eligible to be added for the Dorinthea hero

    # Rule 2.6.1 - Card with non-matching metatype cannot be added
    Scenario: Card with non-matching hero-metatype cannot be added to a game
        Given a card named Dorinthea Specialization Spell with hero-metatype "Dorinthea"
        And a hero named Katsu with moniker "Katsu"
        When the engine checks if the Dorinthea Specialization Spell may be added to a game for Katsu
        Then the Dorinthea Specialization Spell should not be eligible for the Katsu hero

    # Rule 2.6.2 - An object can have zero metatypes
    Scenario: A card with no metatypes has zero metatypes
        Given a card named Generic Action with no metatypes
        When the engine checks the metatypes of the Generic Action
        Then the Generic Action should have zero metatypes
        And the Generic Action metatypes list should be empty

    # Rule 2.6.2 - An object can have one metatype
    Scenario: A card can have exactly one metatype
        Given a card named Dorinthea Specialization Spell with hero-metatype "Dorinthea"
        When the engine checks the metatypes of the Dorinthea Specialization Spell
        Then the Dorinthea Specialization Spell should have exactly one metatype
        And the Dorinthea Specialization Spell metatype should be "Dorinthea"

    # Rule 2.6.2 - An object can have multiple metatypes
    Scenario: A card can have multiple metatypes
        Given a card named Multi Metatype Card with two hero-metatypes "Dorinthea" and "Bravo"
        When the engine checks the metatypes of the Multi Metatype Card
        Then the Multi Metatype Card should have exactly two metatypes
        And the Multi Metatype Card metatypes should include "Dorinthea"
        And the Multi Metatype Card metatypes should include "Bravo"

    # Rule 2.6.3 - Metatype is read from the type box
    Scenario: The metatype of a card is determined by its type box
        Given a card named Type Box Card with type box showing metatype "Boltyn" before supertypes
        When the engine reads the metatype from the type box of the Type Box Card
        Then the metatype should be "Boltyn"
        And the metatype should appear before the supertypes in the type box

    # Rule 2.6.3 - Metatype appears before supertypes in the type box
    Scenario: Metatype is printed before supertypes in the type box
        Given a card named Warrior Metatype Card with metatype "Bravo" and supertype "Guardian"
        When the engine reads the type box of the Warrior Metatype Card
        Then the metatype position should be before the supertype position in the type box

    # Rule 2.6.4 - Activated-layer inherits source metatypes
    Scenario: Activated-layer has the same metatypes as its source
        Given a card named Dorinthea Source Card with hero-metatype "Dorinthea" and the card creates an activated-layer
        When the engine checks the layer metatypes of the activated-layer
        Then the activated-layer metatypes should match the source metatypes
        And the activated-layer should have metatype "Dorinthea"

    # Rule 2.6.4 - Triggered-layer inherits source metatypes
    Scenario: Triggered-layer has the same metatypes as its source
        Given a card named Boltyn Trigger Source with hero-metatype "Boltyn" and the card creates a triggered-layer
        When the engine checks the layer metatypes of the triggered-layer
        Then the triggered-layer metatypes should match the source metatypes
        And the triggered-layer should have metatype "Boltyn"

    # Rule 2.6.4 - Layer from card with no metatypes has no metatypes
    Scenario: Layer from a source with no metatypes has no metatypes
        Given a card named No Metatype Source with no metatypes and the card creates an activated-layer
        When the engine checks the layer metatypes of the activated-layer from No Metatype Source
        Then the activated-layer from No Metatype Source should have zero metatypes

    # Rule 2.6.5 - Objects cannot gain metatypes
    Scenario: An object cannot gain metatypes via effects
        Given a card named Metatype Gain Target with no metatypes
        When an effect attempts to grant the Metatype Gain Target hero-metatype "Dorinthea"
        Then the metatype gain attempt should fail
        And the Metatype Gain Target should still have zero metatypes

    # Rule 2.6.5 - Objects cannot lose metatypes
    Scenario: An object cannot lose metatypes via effects
        Given a card named Metatype Loss Target with hero-metatype "Bravo"
        When an effect attempts to remove the "Bravo" metatype from the Metatype Loss Target
        Then the metatype removal attempt should fail
        And the Metatype Loss Target should still have metatype "Bravo"

    # Rule 2.6.6 - Hero-metatypes match by hero moniker
    Scenario: Hero-metatype card legal only for matching hero moniker
        Given a card named Bravo Signature Weapon with hero-metatype "Bravo"
        And a hero named Bravo, Showstopper with moniker "Bravo"
        When checking if Bravo Signature Weapon is legal for card-pool
        Then the Bravo Signature Weapon should be legal for the Bravo Showstopper hero

    # Rule 2.6.6 - Hero-metatypes reject non-matching hero moniker
    Scenario: Hero-metatype card illegal for non-matching hero moniker
        Given a card named Bravo Signature Weapon with hero-metatype "Bravo"
        And a hero named Dorinthea Ironsong with moniker "Dorinthea"
        When checking if Bravo Signature Weapon is legal for the Dorinthea Ironsong card-pool
        Then the Bravo Signature Weapon should not be legal for the Dorinthea Ironsong hero

    # Rule 2.6.6 - Set-metatypes controlled by tournament rules
    Scenario: Set-metatype card requires matching tournament set rule
        Given a card named Classic Constructed Card with set-metatype "Classic Constructed"
        And a tournament rule allowing the set "Classic Constructed"
        When checking if Classic Constructed Card may be added to the game
        Then the Classic Constructed Card should be allowed in the game

    # Rule 2.6.6 - Set-metatype card rejected without matching tournament rule
    Scenario: Set-metatype card rejected when tournament rule does not allow that set
        Given a card named Classic Constructed Card with set-metatype "Classic Constructed"
        And a tournament rule that does not allow "Classic Constructed"
        When checking if Classic Constructed Card may be added under the non-matching tournament rule
        Then the Classic Constructed Card should not be allowed for the non-matching rule

    # Rule 2.6.6 combined with 2.6.1 - Card with no metatypes is always eligible
    Scenario: Card with no metatypes is always eligible regardless of hero
        Given a card named Generic Warrior Action with no metatypes
        And a hero named Dorinthea with moniker "Dorinthea"
        When checking if Generic Warrior Action can be added to game for Dorinthea
        Then the Generic Warrior Action should not be excluded by metatype restrictions
