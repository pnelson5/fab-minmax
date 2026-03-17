# Feature file for Section 3.1: Arena
# Reference: Flesh and Blood Comprehensive Rules Section 3.1
#
# 3.1.1 The arena is a collection of all the arms, chest, combat chain, head, hero, legs,
#        permanent, and weapon zones.
#
# 3.1.1a The arsenal, banished, deck, graveyard, hand, pitch, and stack zones are not part of
#         the arena.
#
# 3.1.2 The arena is not a zone. If an object would be put into the arena by a rule or effect
#        without specifying a zone, it is placed into the permanent zone as a permanent.
#
# 3.1.2a A card is considered to be in the arena if it is in any of the arena zones, and it is
#         not a sub-card under permanent.

Feature: Section 3.1 - Arena
    As a game engine
    I need to correctly model the arena as a collection of specific zones
    So that all arena-related rules and effects work correctly

    # ===== Rule 3.1.1: Arena zone composition =====

    # Test for Rule 3.1.1 - Arena is a collection of specific zones
    Scenario: The arena is a collection of arms, chest, combat chain, head, hero, legs, permanent, and weapon zones
        Given a player's complete set of game zones
        When checking which zones make up the arena
        Then the arms zone is an arena zone
        And the chest zone is an arena zone
        And the combat chain zone is an arena zone
        And the head zone is an arena zone
        And the hero zone is an arena zone
        And the legs zone is an arena zone
        And the permanent zone is an arena zone
        And the weapon zone is an arena zone

    # Test for Rule 3.1.1 - Arena contains exactly 8 zone types
    Scenario: The arena contains exactly 8 zone types
        Given a player's complete set of game zones
        When I count the number of arena zone types
        Then the arena contains exactly 8 zone types

    # Test for Rule 3.1.1a - Non-arena zones are not part of the arena
    Scenario: Arsenal, banished, deck, graveyard, hand, pitch, and stack are not arena zones
        Given a player's complete set of game zones
        When checking which zones are outside the arena
        Then the arsenal zone is not an arena zone
        And the banished zone is not an arena zone
        And the deck zone is not an arena zone
        And the graveyard zone is not an arena zone
        And the hand zone is not an arena zone
        And the pitch zone is not an arena zone
        And the stack zone is not an arena zone

    # ===== Rule 3.1.2: Arena is not a zone =====

    # Test for Rule 3.1.2 - Arena is not itself a zone
    Scenario: The arena is not itself a zone
        Given the list of all zone types
        When checking if arena is a zone type
        Then arena is not a zone type
        And arena is a collection of zones not itself a zone

    # Test for Rule 3.1.2 - Object placed in arena without specifying zone goes to permanent zone
    Scenario: Object placed into arena without zone specification goes to permanent zone
        Given a card that would be placed in the arena without specifying a zone
        When the card is placed in the arena by a rule without specifying a zone
        Then the card is placed in the permanent zone
        And the card is a permanent in the permanent zone

    # Test for Rule 3.1.2 - Object placed in arena by effect without specifying zone goes to permanent zone
    Scenario: Object placed into arena by effect without zone specification goes to permanent zone
        Given a card that would be placed in the arena by an effect
        When the effect places the card in the arena without specifying a zone
        Then the card is placed in the permanent zone as a permanent
        And the card is not placed in any other arena zone

    # ===== Rule 3.1.2a: Card in arena definition =====

    # Test for Rule 3.1.2a - Card in any arena zone is in the arena
    Scenario: A card in an arena zone is considered to be in the arena
        Given a card placed in the arms zone
        When checking if the card is in the arena
        Then the card is considered to be in the arena

    # Test for Rule 3.1.2a - Card in hero zone is in the arena
    Scenario: A card in the hero zone is considered to be in the arena
        Given a hero card placed in the hero zone
        When checking if the hero card is in the arena
        Then the hero card is considered to be in the arena

    # Test for Rule 3.1.2a - Card in the permanent zone is in the arena
    Scenario: A card in the permanent zone is considered to be in the arena
        Given a card placed in the permanent zone
        When checking if the permanent card is in the arena
        Then the permanent card is considered to be in the arena

    # Test for Rule 3.1.2a - Card that is a sub-card under permanent is NOT in the arena
    Scenario: A card that is a sub-card under permanent is not considered to be in the arena
        Given a card that is stored as a sub-card under a permanent
        When checking if the sub-card is in the arena
        Then the sub-card is not considered to be in the arena

    # Test for Rule 3.1.2a - Card in hand is NOT in the arena
    Scenario: A card in the hand zone is not in the arena
        Given a card placed in the hand zone
        When checking if the hand card is in the arena
        Then the hand card is not considered to be in the arena

    # Test for Rule 3.1.2a - Card in graveyard is NOT in the arena
    Scenario: A card in the graveyard zone is not in the arena
        Given a card placed in the graveyard zone
        When checking if the graveyard card is in the arena
        Then the graveyard card is not considered to be in the arena

    # Test for Rule 3.1.2a - Card in deck is NOT in the arena
    Scenario: A card in the deck zone is not in the arena
        Given a card placed in the deck zone
        When checking if the deck card is in the arena
        Then the deck card is not considered to be in the arena

    # Test for Rule 3.1.2a - Card in banished zone is NOT in the arena
    Scenario: A card in the banished zone is not in the arena
        Given a card placed in the banished zone for arena check
        When checking if the banished card is in the arena
        Then the banished card is not considered to be in the arena

    # Test for Rule 3.1.1 / 3.1.2a - Moving a card out of an arena zone removes it from the arena
    Scenario: Moving a card from an arena zone to a non-arena zone removes it from the arena
        Given a card that was previously in the arms zone
        When the card is moved from the arms zone to the graveyard
        Then the card is no longer in the arena
        And the card is in the graveyard zone instead
