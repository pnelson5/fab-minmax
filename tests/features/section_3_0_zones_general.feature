# Feature file for Section 3.0: Zones - General
# Reference: Flesh and Blood Comprehensive Rules Section 3.0
#
# 3.0.1 A zone is a collection of objects. There are 15 types of zones: arms, arsenal, banished,
#        chest, combat chain, deck, graveyard, hand, head, hero, legs, permanent, pitch, stack,
#        and weapon.
#
# 3.0.1a A zone is considered empty when it does not contain any objects and has no permanents
#         equipped to it. An equipment zone is exposed if it is empty. A zone does not cease to
#         exist if it is empty.
#
# 3.0.2 Each player has their own arms, arsenal, banished, chest, deck, graveyard, hand, head,
#        hero, legs, and pitch zones; and has two weapon zones. The stack zone, permanent zone,
#        and combat chain zone are shared by all players.
#
# 3.0.3 An object can have one of two possible states of visibility: public, or private.
#        A public object is an object where information about the properties of the object is
#        currently available to all players. A private object is an object where the information
#        about the properties of that object is not currently available to all players.
#
# 3.0.3a A player may look at any private object they own, or is in a zone that they own,
#         unless the object is in the deck zone.
#
# 3.0.4 A public zone is a zone in which the default visibility of objects is public.
#        A private zone is a zone in which the default visibility of objects is private.
#
# 3.0.4a The arms, banished, chest, combat chain, graveyard, head, hero, legs, permanent,
#         pitch, stack, and weapon zones are public zones.
#
# 3.0.4b The arsenal, deck, and hand zones are private zones.
#
# 3.0.4c A public zone may contain a private object, if the object is made private while in
#         that zone, or if the object is moved into that zone as a private object.
#
# 3.0.4d A private zone may contain public objects if the object is made public while in that
#         zone, or if the object is moved into that zone as a public object.
#
# 3.0.4e If a rule or effect specifies an object in a public zone, the source must be public
#         for the rule or effect to apply unless otherwise stated.
#
# 3.0.5 The arena is a collection of all the arms, chest, combat chain, head, hero, legs,
#        permanent, and weapon zones.
#
# 3.0.5a The arena is not a zone. If an object would be put into the arena by a rule or effect
#         without specifying a zone, it is placed into the permanent zone as a permanent.
#
# 3.0.5b The arsenal, banished, deck, graveyard, hand, pitch, and stack zones are not part of
#         the arena.
#
# 3.0.7 When an object moves from one zone to another, the object leaving its old zone (origin)
#        and the object entering its new zone (destination) is performed simultaneously. At no
#        point is the object not in a zone.
#
# 3.0.7a The object as it leaves the origin is considered the object moving for rules and effects.
#         If the object is private at its origin and would be private at its destination, it is
#         considered to have no properties for effects.
#
# 3.0.7b If the origin and the destination of a move are the same, then no move occurs.
#
# 3.0.9 If an object enters a zone that is not in the arena and is not the stack zone, or a public
#        object becomes a private object, it resets - its previous existence ceases to exist and
#        it becomes a new object with no relation to its previous existence.
#
# 3.0.9a An ability that triggers when an object moves from one zone to another still references
#         the new object, as long as the object remains a public object.
#
# 3.0.9b An ability with an effect that moves an object from one zone to another still references
#         the new object for the remainder of any effects it generates, as long as the object
#         remains a public object.
#
# 3.0.9c The process of how an object becomes a new object is preserved as the history of that
#         new object.
#
# 3.0.12 To clear an object, move it from its current zone to its owner's graveyard.
#
# 3.0.12a If the object is a token, macro, or a non-card-layer, it leaves its current zone and
#          simply ceases to exist.
#
# 3.0.13 If an effect refers to one or more zones without specifying the owner of those zones
#         (or specifying "any"), it refers to the zones owned by the controller of the effect.

Feature: Section 3.0 - Zones General Rules
    As a game engine
    I need to correctly model the zone system including zone types, visibility, ownership, and object movement
    So that all zone-related rules and effects work correctly

    # ===== Rule 3.0.1: Zone types =====

    # Test for Rule 3.0.1 - There are exactly 15 zone types
    Scenario: There are exactly 15 zone types
        Given the game engine zone type registry
        When I count the number of defined zone types
        Then there are exactly 15 zone types
        And the zone types include arms, arsenal, banished, chest, combat chain, deck, graveyard, hand, head, hero, legs, permanent, pitch, stack, and weapon

    # Test for Rule 3.0.1 - Zone is a collection of objects
    Scenario: A zone is a collection of objects
        Given a player has a hand zone
        When a card is added to the hand zone
        Then the hand zone contains the card
        And the hand zone is not empty

    # Test for Rule 3.0.1a - Empty zone does not cease to exist
    Scenario: An empty zone does not cease to exist
        Given a player has a hand zone with no cards
        When the engine checks if the empty hand zone exists
        Then the empty hand zone still exists
        And the empty hand zone is considered empty

    # ===== Rule 3.0.2: Zone ownership =====

    # Test for Rule 3.0.2 - Each player has their own zones
    Scenario: Each player has their own private zones
        Given two players in a game
        When checking zone ownership
        Then player 0 has their own hand zone
        And player 1 has their own hand zone
        And the two hand zones are different zones

    # Test for Rule 3.0.2 - Stack, permanent, and combat chain zones are shared
    Scenario: Shared zones are shared among all players
        Given two players in a game
        When checking the stack zone
        Then the stack zone is shared by all players

    # ===== Rule 3.0.3: Object visibility =====

    # Test for Rule 3.0.3 - Objects can be public or private
    Scenario: A card can be public
        Given a card placed in the graveyard zone for visibility check
        When the engine checks the graveyard card visibility
        Then the card is a public object
        And information about the card properties is available to all players

    Scenario: A card can be private
        Given a card placed in the hand zone for visibility check
        When the engine checks the hand card visibility
        Then the card is a private object
        And information about the card properties is not available to all players

    # Test for Rule 3.0.3a - Player can look at their own private objects
    Scenario: Player can look at their own private objects except in deck
        Given a player owns a card in their arsenal zone
        When the player attempts to look at the private card
        Then the player can see the card's properties
        And the card is still considered private to other players

    # ===== Rule 3.0.4: Public and private zones =====

    # Test for Rule 3.0.4a - Arms, banished, chest etc. are public zones
    Scenario: The graveyard zone is a public zone
        Given a player has a graveyard zone
        When checking the default visibility of the graveyard
        Then the graveyard zone is a public zone
        And objects in graveyard are public by default

    Scenario: The banished zone is a public zone
        Given a player has a banished zone
        When checking the default visibility of the banished zone
        Then the banished zone is a public zone

    Scenario: The pitch zone is a public zone
        Given a player has a pitch zone
        When checking the default visibility of the pitch zone
        Then the pitch zone is a public zone

    Scenario: The stack zone is a public zone
        Given the stack zone exists
        When checking the default visibility of the stack zone
        Then the stack zone is a public zone

    # Test for Rule 3.0.4b - Arsenal, deck, hand are private zones
    Scenario: The hand zone is a private zone
        Given a player has a hand zone
        When checking the default visibility of the hand zone
        Then the hand zone is a private zone
        And objects in hand are private by default

    Scenario: The deck zone is a private zone
        Given a player has a deck zone
        When checking the default visibility of the deck zone
        Then the deck zone is a private zone

    Scenario: The arsenal zone is a private zone
        Given a player has an arsenal zone
        When checking the default visibility of the arsenal zone
        Then the arsenal zone is a private zone

    # Test for Rule 3.0.4c - Public zone can contain private objects
    Scenario: A public zone can contain a private object
        Given a public graveyard zone
        And a card that is made private
        When the private card is placed in the graveyard
        Then the graveyard still contains the card as a private object
        And the zone is still considered a public zone

    # Test for Rule 3.0.4d - Private zone can contain public objects
    Scenario: A private zone can contain a public object
        Given a private arsenal zone
        And a card that is made public
        When the public card is placed in the arsenal
        Then the arsenal still contains the card as a public object
        And the zone is still considered a private zone

    # Test for Rule 3.0.4e - Public zone rule requires public source
    Scenario: An effect on a public zone only applies to public objects
        Given a banished zone with a face-down private card
        When an effect checks for the card in the banished zone
        Then the effect does not apply because the source is private

    # ===== Rule 3.0.5: Arena definition =====

    # Test for Rule 3.0.5 - The arena collects specific zones
    Scenario: The arena collects specific zone types
        Given a player's game zones
        When checking which zones are in the arena
        Then the arms zone is in the arena
        And the chest zone is in the arena
        And the head zone is in the arena
        And the hero zone is in the arena
        And the legs zone is in the arena
        And the permanent zone is in the arena
        And the weapon zone is in the arena

    # Test for Rule 3.0.5a - Arena is not itself a zone
    Scenario: The arena is not itself a zone
        Given the arena collection
        When checking if the arena is a zone
        Then the arena is not a zone type
        And the arena is a collection of zones

    # Test for Rule 3.0.5a - Object put into arena without zone goes to permanent zone
    Scenario: Object placed into arena without specifying zone goes to permanent zone
        Given a card that would be placed in the arena
        When no specific zone is specified
        Then the card is placed in the permanent zone
        And the card is a permanent

    # Test for Rule 3.0.5b - Arsenal, banished, deck, graveyard, hand, pitch, stack not in arena
    Scenario: Non-arena zones are not part of the arena
        Given a player's game zones
        When checking which zones are NOT in the arena
        Then the arsenal zone is not in the arena
        And the banished zone is not in the arena
        And the deck zone is not in the arena
        And the graveyard zone is not in the arena
        And the hand zone is not in the arena
        And the pitch zone is not in the arena
        And the stack zone is not in the arena

    # ===== Rule 3.0.7: Zone movement =====

    # Test for Rule 3.0.7 - Object moves simultaneously leaves old and enters new zone
    Scenario: Moving a card between zones is simultaneous
        Given a card in the hand zone
        When the card is moved to the graveyard
        Then the card is no longer in the hand zone
        And the card is in the graveyard zone
        And the card was never in no zone during the move

    # Test for Rule 3.0.7a - Leaving object is used for effects
    Scenario: The leaving object is used for zone-triggered effects
        Given a card in the hand zone with power 4
        When the card is moved to the banished zone
        Then the card's power value at the origin is 4
        And the card is in the banished zone

    # Test for Rule 3.0.7a - Private-to-private object has no properties for effects
    Scenario: Private-to-private zone move object has no properties for effects
        Given a private card in the hand zone
        When the card is moved face-down to the banished zone
        Then the card is considered to have no properties for effects during the move

    # Test for Rule 3.0.7b - Moving to same zone is no-op
    Scenario: Moving a card to the same zone it is already in does nothing
        Given a card already placed in the graveyard zone
        When an effect tries to move the card to the graveyard again
        Then no move occurs
        And the card remains in the graveyard zone

    # ===== Rule 3.0.9: Zone reset =====

    # Test for Rule 3.0.9 - Object entering non-arena/non-stack zone resets
    Scenario: Card entering hand from graveyard becomes a new object
        Given a card in the graveyard zone with an effect applied
        When the card moves from graveyard to the hand zone
        Then the card resets and becomes a new object after entering hand
        And the card has no relation to its previous existence

    # Test for Rule 3.0.9 - Public object becoming private resets
    Scenario: Card becoming private resets
        Given a public card in the graveyard zone with go again effect
        When the card becomes a private object
        Then the card resets and becomes a new private object
        And the go again effect no longer applies

    # Test for Rule 3.0.9a - Trigger still references new object
    Scenario: Triggered ability references new object after zone change
        Given a card in the arena with a triggered ability
        When the card moves to the graveyard and triggers an ability
        Then the triggered ability references the new object in graveyard
        And the triggered ability has the new object reference

    # Test for Rule 3.0.9c - History preserved when object resets
    Scenario: Reset object preserves history of how it became a new object
        Given a card banished from the hand zone
        When the engine checks the card's history in the banished zone
        Then the card remembers it was banished from the hand zone
        And the card can be played from the banished zone this turn

    # ===== Rule 3.0.12: Clearing objects =====

    # Test for Rule 3.0.12 - Clearing moves object to graveyard
    Scenario: Clearing a card moves it to the graveyard
        Given a card in the permanent zone
        When the card is cleared
        Then the card is moved to its owner's graveyard
        And the card is no longer in the permanent zone

    # Test for Rule 3.0.12a - Clearing a token causes it to cease to exist
    Scenario: Clearing a token causes it to cease to exist
        Given a token card in the permanent zone
        When the token is cleared
        Then the token ceases to exist
        And the token is not moved to any graveyard

    # ===== Rule 3.0.13: Zone references =====

    # Test for Rule 3.0.13 - Unspecified zone refers to controller's zone
    Scenario: Unspecified zone in effect refers to effect controller's zone
        Given player 0 controls an effect that refers to "your graveyard"
        When the effect resolves
        Then the effect refers to player 0's graveyard zone
        And not player 1's graveyard zone
