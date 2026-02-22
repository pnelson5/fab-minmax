# Feature file for Section 1.2: Objects
# Reference: Flesh and Blood Comprehensive Rules Section 1.2
#
# 1.2.1 An object is an element of the game with properties and located in a zone or
#        a player's inventory. Cards, attacks, macros, and layers are objects.
#
# 1.2.1a The owner of an object is the same as the card, macro, or layer that represents it,
#         otherwise it has no owner.
#
# 1.2.1b The controller of an object is the same as the card, macro, or layer that represents it.
#         An object does not have a controller if it is not in the arena or on the stack.
#
# 1.2.2 An object has one or more object identities that can be referred to.
#        Rules in this document and effects typically describe objects using their object
#        identity as the noun.
#
# 1.2.2a An object has the object identity "object."
# 1.2.2b An object with a name property and/or moniker has the object identity of that name and/or moniker.
# 1.2.2c A card has the object identity of its traits, types, and subtypes, except for the subtype attack.
# 1.2.2d An attack-card, attack-proxy, or attack-layer has the object identity "attack."
# 1.2.2e A card has the object identity "card."
# 1.2.2f A permanent has the object identity "permanent."
# 1.2.2g An activated-layer has the object identity "activated ability."
# 1.2.2h A triggered-layer has the object identity "triggered effect."
#
# 1.2.3 Last known information about an object is a snapshot of the state of an object
#        immediately before it ceased to exist.
#
# 1.2.3a If a rule or effect requires information about a specific object that no longer exists,
#         instead it uses last known information about that object to fulfil that requirement.
#         Otherwise, if a rule or effect does not specifically refer to that object,
#         last known information is not used.
#
# 1.2.3b Last known information about an object includes all parameters, history, and effects
#         applicable to that object at the time it still existed.
#
# 1.2.3c Last known information about an object is immutable - it cannot be altered. Rules and
#         effects that would modify the object that no longer exists do not modify the last known
#         information about an object; this may cause effects to fail.
#
# 1.2.3d Last known information about an object is not an object itself - it is not a legal
#         target for rules and effects.
#
# 1.2.4 Card and macro objects are the source of abilities, effects, non-card layers,
#        and attack-proxies.

Feature: Section 1.2 - Objects
    As a game engine
    I need to correctly model game objects, their identities, ownership, control, and last known information
    So that rules and effects can correctly reference and interact with objects

    # ===== Rule 1.2.1: Objects in zones =====

    # Test for Rule 1.2.1 - Cards in zones are objects
    Scenario: A card in a zone is a game object
        Given a player has a hand zone
        And the player has a card in hand
        When the engine inspects the card in hand
        Then the card is recognized as a game object
        And the card has properties

    # Test for Rule 1.2.1 - Cards, attacks, macros, and layers are objects
    Scenario: Different game elements are all objects
        Given a game is in progress
        When the engine enumerates game objects
        Then cards are recognized as objects
        And attacks are recognized as objects

    # ===== Rule 1.2.1a: Owner of an object =====

    # Test for Rule 1.2.1a - Object owner matches card owner
    Scenario: The owner of an object matches the card that represents it
        Given player 0 creates a card
        And the card is placed in a zone
        When the engine checks the card object's owner
        Then the card object's owner is player 0

    # Test for Rule 1.2.1a - Object without representing card has no owner
    Scenario: An object without a representing card has no owner
        Given a game is in progress
        When an attack-proxy object is created without an owner
        Then the attack-proxy has no owner

    # ===== Rule 1.2.1b: Controller of an object =====

    # Test for Rule 1.2.1b - Card has no controller outside arena/stack
    Scenario: A card in hand has no controller
        Given player 0 has a card in their hand
        When the engine checks the controller of that card
        Then the card has no controller

    # Test for Rule 1.2.1b - Card in the arena has a controller
    Scenario: A card in the arena has a controller
        Given player 0 plays a card into the arena
        When the engine checks the controller of that card
        Then the card's controller is player 0

    # Test for Rule 1.2.1b - Card on the stack has a controller
    Scenario: A card on the stack has a controller
        Given player 0 plays a card onto the stack
        When the engine checks the controller of that card
        Then the card's controller is player 0

    # ===== Rule 1.2.2: Object identities =====

    # Test for Rule 1.2.2a - All objects have the "object" identity
    Scenario: Every game object has the object identity "object"
        Given a player has a card in hand
        When the engine checks the object identities of the card
        Then the card has the object identity "object"

    # Test for Rule 1.2.2b - Named objects have their name as identity
    Scenario: An object's name is one of its object identities
        Given a card named "Lunging Press" exists
        When the engine checks the object identities of the card
        Then the card has the object identity "Lunging Press"

    # Test for Rule 1.2.2c - Card's types and subtypes are identities (except attack subtype)
    Scenario: A weapon card has the object identity "weapon"
        Given a card with type "weapon" exists
        When the engine checks the object identities of the card
        Then the card has the object identity "weapon"

    # Test for Rule 1.2.2c - The "attack" subtype is NOT an object identity
    Scenario: The attack subtype is not an object identity for cards
        Given an attack action card exists
        When the engine checks the object identities of the card
        Then the card does not have the object identity "attack" via its subtype
        But the card does have the object identity "action"

    # Test for Rule 1.2.2d - Attack-cards have "attack" identity
    Scenario: An attack-card has the object identity "attack"
        Given an attack action card exists
        When the engine checks if the card has the attack object identity
        Then the card has the object identity "attack"

    # Test for Rule 1.2.2e - All cards have "card" identity
    Scenario: Every card has the object identity "card"
        Given a player has a card in hand
        When the engine checks the object identities of the card
        Then the card has the object identity "card"

    # Test for Rule 1.2.2f - Permanents have "permanent" identity
    Scenario: An equipment card in the arena has the object identity "permanent"
        Given player 0 has an equipment card in the arena
        When the engine checks the object identities of the equipment
        Then the equipment has the object identity "permanent"

    # ===== Rule 1.2.3: Last known information =====

    # Test for Rule 1.2.3 - LKI is a snapshot before object ceases to exist
    Scenario: Last known information is captured when an object leaves the game
        Given an attack card with power 6 is on the combat chain
        When the attack card is removed from the combat chain
        Then the last known information of the card has power 6

    # Test for Rule 1.2.3a - LKI used when object no longer exists
    Scenario: Last known information is used when the specific object no longer exists
        Given an attack card named "Endless Arrow" with go again is on the combat chain
        When the card is moved to its owner's hand during resolution
        Then the chain link uses last known information about the card
        And the player gains an action point because the card had go again

    # Test for Rule 1.2.3a - LKI not used when rule doesn't reference that object
    Scenario: Last known information is not used when the rule doesn't reference the specific object
        Given an attack card is on the combat chain
        When the card is moved out of its zone
        And a rule references all cards in the zone generically
        Then last known information about the removed card is not used

    # Test for Rule 1.2.3b - LKI includes all parameters at time of snapshot
    Scenario: Last known information includes all effects active at snapshot time
        Given an attack card has a power buff of +3 applied to it
        And the card is on the combat chain
        When the card ceases to exist
        Then the last known information of the card includes the +3 power buff

    # Test for Rule 1.2.3c - LKI is immutable
    Scenario: Last known information cannot be altered after capture
        Given an attack card with no go again is captured in last known information
        When an effect would grant go again to the no-longer-existing card
        Then the last known information remains unchanged
        And the effect fails to modify the last known information

    # Test for Rule 1.2.3c - Effect cannot add go again to LKI after condition
    Scenario: Go again cannot be granted to a card via LKI after it leaves
        Given an Illusionist attack card is on the combat chain as a chain link
        And the attack card is removed from the combat chain
        When a yellow card is added to the pitch zone
        Then the chain link does not gain go again from the LKI

    # Test for Rule 1.2.3d - LKI is not a legal target
    Scenario: Last known information is not a legal target for effects
        Given an attack card has ceased to exist
        And its last known information has been captured
        When an effect attempts to target the last known information
        Then the targeting fails because LKI is not a legal target

    # ===== Rule 1.2.4: Sources of abilities and effects =====

    # Test for Rule 1.2.4 - Cards are sources of abilities
    Scenario: A card is the source of its abilities and effects
        Given a card named "Oasis Respite" with a prevention effect exists
        When the player declares the source of a prevention effect
        Then only cards or macros can be declared as the source
        And the declared source is valid

    # Test for Rule 1.2.4 - Attack-proxies originate from card sources
    Scenario: An attack-proxy's source is a card or macro object
        Given a card creates an attack-proxy during play
        When the engine checks the source of the attack-proxy
        Then the attack-proxy's source is the card object that created it
