# Feature file for Section 3.6: Combat Chain
# Reference: Flesh and Blood Comprehensive Rules Section 3.6
#
# 3.6.1 The combat chain zone is a public zone in the arena. There is only one
#        combat chain zone, shared by all players, and it does not have an owner.
#
# 3.6.2 The combat chain zone can only contain cards and attack-proxies. [1.4.3]
#
# 3.6.3 The term "combat chain" refers to the combat chain zone.
#
# 3.6.4 The combat chain is "open" during combat - otherwise it is "closed." [7]
#
# Cross-references:
# - 3.0.4a: combat chain zone is a public zone
# - 3.0.5: combat chain zone is in the arena
# - 3.0.2: combat chain zone is shared (not per-player)
# - 1.4.3: attack-proxies are valid combat chain zone contents
# - 7.0.2: combat chain opens when an attack is added to the stack; closes per 7.7.2
# - 7.0.3: chain links are elements of the combat chain

Feature: Section 3.6 - Combat Chain Zone
    As a game engine
    I need to correctly model the combat chain zone rules
    So that combat resolution works correctly

    # ===== Rule 3.6.1: Combat chain zone is public, in the arena, shared, no owner =====

    # Test for Rule 3.6.1 - Combat chain zone is a public zone
    Scenario: The combat chain zone is a public zone
        Given a combat chain zone exists in the game
        When checking the visibility of the combat chain zone
        Then the combat chain zone is a public zone
        And the combat chain zone is not a private zone

    # Test for Rule 3.6.1 - Combat chain zone is in the arena
    Scenario: The combat chain zone is in the arena
        Given a combat chain zone exists in the game
        When checking if the combat chain zone is in the arena
        Then the combat chain zone is in the arena

    # Test for Rule 3.6.1 - There is only one combat chain zone
    Scenario: There is exactly one combat chain zone shared by all players
        Given a game with two players is set up
        When checking how many combat chain zones exist
        Then there is exactly one combat chain zone

    # Test for Rule 3.6.1 - Combat chain zone is shared among all players
    Scenario: The combat chain zone is shared by all players
        Given a game with two players is set up
        When checking if both players share the combat chain zone
        Then both players access the same combat chain zone

    # Test for Rule 3.6.1 - Combat chain zone has no owner
    Scenario: The combat chain zone has no owner
        Given a combat chain zone exists in the game
        When checking the owner of the combat chain zone
        Then the combat chain zone has no owner

    # ===== Rule 3.6.2: Combat chain zone can only contain cards and attack-proxies =====

    # Test for Rule 3.6.2 - Combat chain zone can contain attack cards
    Scenario: The combat chain zone can contain cards
        Given a combat chain zone exists in the game
        And an attack card is available
        When adding the attack card to the combat chain zone
        Then the attack card is in the combat chain zone
        And the combat chain zone is not empty

    # Test for Rule 3.6.2 - Combat chain zone can contain attack-proxies
    Scenario: The combat chain zone can contain attack-proxies
        Given a combat chain zone exists in the game
        And an attack-proxy object is available
        When adding the attack-proxy to the combat chain zone
        Then the attack-proxy is in the combat chain zone

    # Test for Rule 3.6.2 - Combat chain zone can hold multiple cards and proxies
    Scenario: The combat chain zone can hold multiple cards from different chain links
        Given a combat chain zone exists in the game
        And two attack cards are available
        When both attack cards are added to the combat chain zone
        Then the combat chain zone contains two cards

    # ===== Rule 3.6.3: The term "combat chain" refers to the combat chain zone =====

    # Test for Rule 3.6.3 - "combat chain" is a recognized term for the zone
    Scenario: The term combat chain refers to the combat chain zone
        Given a game with a combat chain zone
        When resolving the term "combat chain" to a zone
        Then the term resolves to the combat chain zone

    # ===== Rule 3.6.4: Combat chain open during combat, closed otherwise =====

    # Test for Rule 3.6.4 - Combat chain starts the game closed
    Scenario: The combat chain starts the game in the closed state
        Given a game has just begun
        When checking the state of the combat chain
        Then the combat chain is closed

    # Test for Rule 3.6.4 - Combat chain is open during combat
    Scenario: The combat chain is open during combat
        Given a game has an open combat chain
        When checking the state of the combat chain
        Then the combat chain is open

    # Test for Rule 3.6.4 - Combat chain transitions from closed to open
    Scenario: The combat chain transitions from closed to open when combat starts
        Given the combat chain is currently closed
        When combat begins and the chain is opened
        Then the combat chain transitions to the open state

    # Test for Rule 3.6.4 - Combat chain transitions from open to closed
    Scenario: The combat chain transitions from open to closed when combat ends
        Given the combat chain is currently open
        When combat ends and the chain is closed
        Then the combat chain transitions to the closed state

    # Test for Rule 3.6.4 - Closed combat chain is empty
    Scenario: The closed combat chain is empty
        Given a game has a closed combat chain
        When checking the contents of the closed combat chain
        Then the closed combat chain is empty
