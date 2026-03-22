# Feature file for Section 3.13: Permanent
# Reference: Flesh and Blood Comprehensive Rules Section 3.13
#
# 3.13.1 The permanent zone is a public zone in the arena. There is only one
#         permanent zone, shared by all players, and it does not have an owner.
#
# 3.13.2 The permanent zone can only contain permanents.
#
# Cross-references:
# - 1.3.3: A permanent is a card in the arena that remains there indefinitely,
#           or until they are destroyed, banished, or otherwise removed by an
#           effect or game rule. Hero-cards, arena-cards, and token-cards are
#           permanents while they are in the arena. Deck-cards become permanents
#           when they are put into the arena (but not the combat chain) and they
#           have one of the following subtypes: Affliction, Ally, Ash, Aura,
#           Construct, Figment, Invocation, Item, and Landmark.
# - 1.3.3a: If a permanent leaves the arena, it is no longer considered a permanent.
# - 1.3.3b: A permanent has one of two different states: untapped and tapped.
#            Permanents are untapped unless a rule or effect puts them into the
#            arena tapped, or changes their state.
# - 3.0.1: A zone is a collection of objects. There are 15 types of zones including
#           permanent.
# - 3.1.1: The permanent zone is in the arena.

Feature: Section 3.13 - Permanent Zone
    As a game engine
    I need to correctly model the permanent zone rules
    So that permanents are tracked in a shared zone without an owner

    # ===== Rule 3.13.1: The permanent zone is a public zone in the arena =====

    # Test for Rule 3.13.1 - Permanent zone is a public zone
    Scenario: The permanent zone is a public zone
        Given the permanent zone exists in the game
        When checking the visibility of the permanent zone
        Then the permanent zone is a public zone
        And the permanent zone is not a private zone

    # Test for Rule 3.13.1 - Permanent zone is in the arena
    Scenario: The permanent zone is in the arena
        Given the permanent zone exists in the game
        When checking if the permanent zone is in the arena
        Then the permanent zone is in the arena

    # Test for Rule 3.13.1 - Only one permanent zone exists
    Scenario: There is only one permanent zone shared by all players
        Given the permanent zone exists in the game
        When checking how many permanent zones exist
        Then there is exactly one permanent zone

    # Test for Rule 3.13.1 - Permanent zone has no owner
    Scenario: The permanent zone does not have an owner
        Given the permanent zone exists in the game
        When checking the owner of the permanent zone
        Then the permanent zone has no owner

    # Test for Rule 3.13.1 - Permanent zone is shared by all players
    Scenario: The permanent zone is shared by all players
        Given the permanent zone exists in the game
        And there are multiple players in the game
        When checking which players share the permanent zone
        Then all players share the same permanent zone

    # ===== Rule 3.13.2: Permanent zone can only contain permanents =====

    # Test for Rule 3.13.2 - Hero cards are permanents in the arena
    Scenario: A hero card in the permanent zone is a permanent
        Given the permanent zone exists in the game
        And a hero card is placed in the permanent zone
        When checking if the hero card is a permanent
        Then the hero card is a permanent in the permanent zone

    # Test for Rule 3.13.2 - Arena cards are permanents in the arena
    Scenario: An arena card in the permanent zone is a permanent
        Given the permanent zone exists in the game
        And an arena card is placed in the permanent zone
        When checking if the arena card is a permanent
        Then the arena card is a permanent in the permanent zone

    # Test for Rule 3.13.2 - Token cards are permanents in the arena
    Scenario: A token card in the permanent zone is a permanent
        Given the permanent zone exists in the game
        And a token card is placed in the permanent zone
        When checking if the token card is a permanent
        Then the token card is a permanent in the permanent zone

    # Test for Rule 3.13.2 - Deck card with permanent subtype is a permanent
    Scenario: A deck card with a permanent subtype is a permanent in the arena
        Given the permanent zone exists in the game
        And a deck card with subtype Aura is placed in the permanent zone
        When checking if the aura deck card is a permanent
        Then the aura deck card is a permanent in the permanent zone

    # Test for Rule 3.13.2 - Deck card without permanent subtype is not a permanent
    Scenario: A deck card without a permanent subtype is not a permanent
        Given the permanent zone exists in the game
        And a standard action deck card exists
        When checking if the action card is a permanent in the arena
        Then the action card is not a permanent in the permanent zone

    # ===== Cross-reference 1.3.3a: Leaving arena removes permanent status =====

    # Test for Rule 1.3.3a - Permanent leaving the arena is no longer a permanent
    Scenario: A card removed from the permanent zone is no longer a permanent
        Given the permanent zone exists in the game
        And an arena card is in the permanent zone as a permanent
        When the arena card is removed from the permanent zone
        Then the removed card is no longer considered a permanent

    # ===== Cross-reference 1.3.3b: Permanents have tapped/untapped state =====

    # Test for Rule 1.3.3b - Permanents start in untapped state
    Scenario: A permanent placed in the permanent zone starts untapped
        Given the permanent zone exists in the game
        And an arena card is placed in the permanent zone
        When checking the tapped state of the arena card
        Then the arena card is in the untapped state

    # Test for Rule 1.3.3b - Permanents can be tapped
    Scenario: A permanent in the permanent zone can be tapped
        Given the permanent zone exists in the game
        And an arena card is in the permanent zone in the untapped state
        When the permanent is tapped
        Then the permanent is in the tapped state

    # Test for Rule 1.3.3b - Permanents can be untapped
    Scenario: A tapped permanent in the permanent zone can be untapped
        Given the permanent zone exists in the game
        And an arena card is in the permanent zone in the tapped state
        When the permanent is untapped
        Then the permanent is back in the untapped state
