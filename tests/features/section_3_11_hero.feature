# Feature file for Section 3.11: Hero Zone
# Reference: Flesh and Blood Comprehensive Rules Section 3.11
#
# 3.11.1 A hero zone is a public zone in the arena, owned by a player.
#
# 3.11.2 A hero zone can only contain one card, with the type hero, and zero or
#         more cards in the hero's soul.
#
# 3.11.3 The term "hero" refers to the card with the type hero in the hero zone.
#
# 3.11.4 A player must start the game with their hero card in their hero zone.
#
# 3.11.5 A hero's soul refers to the collection of sub-objects under the hero card.
#         [3.0.14]
#
# Cross-references:
# - 3.0.4a: hero zone is listed as a public zone
# - 3.0.5: arena includes the hero zone
# - 3.0.2: each player owns their own hero zone
# - 3.0.1a: empty zone does not cease to exist
# - 3.0.14: sub-card rules (for hero soul)
# - 4.1: starting the game procedure
# - 1.3.2a: hero-cards have the type hero

Feature: Section 3.11 - Hero Zone
    As a game engine
    I need to correctly model the hero zone rules
    So that hero placement and hero soul mechanics work correctly

    # ===== Rule 3.11.1: Hero zone is a public zone in the arena =====

    # Test for Rule 3.11.1 - Hero zone is a public zone
    Scenario: A hero zone is a public zone
        Given a player owns a hero zone
        When checking the visibility of the hero zone
        Then the hero zone is a public zone
        And the hero zone is not a private zone

    # Test for Rule 3.11.1 - Hero zone is in the arena
    Scenario: A hero zone is in the arena
        Given a player owns a hero zone
        When checking if the hero zone is in the arena
        Then the hero zone is in the arena

    # Test for Rule 3.11.1 - Hero zone is owned by a specific player
    Scenario: A hero zone is owned by a specific player
        Given player 0 owns a hero zone
        When checking the owner of the hero zone
        Then the hero zone is owned by player 0

    # Test for Rule 3.11.1 - Each player has their own hero zone
    Scenario: Each player has their own separate hero zone
        Given player 0 owns a hero zone
        And player 1 owns a hero zone
        When comparing the two hero zones
        Then the two hero zones are distinct and separate

    # ===== Rule 3.11.2: Hero zone can only contain one hero-type card plus soul cards =====

    # Test for Rule 3.11.2 - Hero zone starts empty
    Scenario: A hero zone starts empty
        Given a player has an empty hero zone
        When checking the contents of the hero zone
        Then the hero zone is empty

    # Test for Rule 3.11.2 - Hero zone can contain one hero-type card
    Scenario: A hero zone can contain one card with the type hero
        Given player 0 has an empty hero zone
        And player 0 has a hero card
        When the hero card is placed in the hero zone
        Then the hero zone contains the hero card
        And the hero zone hero card count is 1

    # Test for Rule 3.11.2 - Hero zone cannot contain more than one hero card
    Scenario: A hero zone cannot contain more than one hero card
        Given player 0 has a hero zone with a hero card already in it
        And player 0 has a second hero card
        When attempting to place the second hero card in the hero zone
        Then placing the second hero card is rejected
        And the hero zone still contains only one hero card

    # Test for Rule 3.11.2 - Hero zone can only contain cards with type hero (not action cards)
    Scenario: A hero zone can only contain cards with the type hero
        Given player 0 has an empty hero zone
        And player 0 has a non-hero action card
        When attempting to place the action card in the hero zone
        Then placing the action card is rejected
        And the hero zone remains empty after rejected hero placement

    # Test for Rule 3.11.2 - Hero zone can contain soul cards (sub-cards under the hero)
    Scenario: A hero zone can contain soul cards under the hero card
        Given player 0 has a hero zone with a hero card in it
        And player 0 has a card to put into the hero's soul
        When a card is put into the hero's soul
        Then the hero zone soul card count is at least 1

    # ===== Rule 3.11.3: The term "hero" refers to the card with type hero in the hero zone =====

    # Test for Rule 3.11.3 - The term "hero" refers to the hero-type card in the hero zone
    Scenario: The term hero refers to the hero card in the hero zone
        Given player 0 has a hero zone with a hero card named "Dorinthea Ironsong"
        When resolving the term "hero" for player 0
        Then the resolved object is the hero card named "Dorinthea Ironsong"

    # Test for Rule 3.11.3 - Hero term resolves to the hero-type card not any other card
    Scenario: The term hero resolves to the hero-type card not any other
        Given player 0 has a hero zone with a hero card
        And there is an action card in the player's hand
        When resolving the term "hero" for the player
        Then the resolved hero is not the action card

    # ===== Rule 3.11.4: Player must start the game with hero card in hero zone =====

    # Test for Rule 3.11.4 - Player must have hero card in hero zone at game start
    Scenario: A player must start the game with their hero card in their hero zone
        Given the game is starting
        And player 0 has a hero card assigned to start in their hero zone
        When the game start procedure is executed
        Then player 0's hero card is in their hero zone at game start

    # Test for Rule 3.11.4 - Game start places hero in hero zone
    Scenario: Game start procedure places hero card into hero zone
        Given a player is setting up their starting game state
        When the player places their hero card into their hero zone at game start
        Then the hero zone contains the setup hero card
        And the hero card is ready for the game

    # ===== Rule 3.11.5: Hero soul is the collection of sub-objects under the hero card =====

    # Test for Rule 3.11.5 - Hero soul is the collection of sub-objects under the hero card
    Scenario: A hero's soul is the collection of sub-objects under the hero card
        Given player 0 has a hero zone with a hero card
        When checking the hero's soul
        Then the hero's soul is the collection of sub-cards under the hero

    # Test for Rule 3.11.5 - Hero soul starts empty
    Scenario: A hero's soul starts empty
        Given player 0 has a hero zone with a hero card in it
        When checking the contents of the hero's soul
        Then the hero's soul is empty initially

    # Test for Rule 3.11.5 - Hero soul can have cards added to it
    Scenario: Cards can be added to the hero's soul
        Given player 0 has a hero zone with a hero card
        And player 0 has a light card to put into the soul
        When a card is charged to the hero's soul
        Then the hero's soul contains 1 card

    # Test for Rule 3.11.5 - Hero soul can have multiple cards
    Scenario: A hero's soul can contain multiple cards
        Given player 0 has a hero zone with a hero card
        And player 0 has two cards to put into the hero's soul
        When both cards are put into the hero's soul
        Then the hero's soul contains 2 cards

    # ===== Cross-rule: Empty zone persists (Rule 3.0.1a) =====

    # Test for Rule 3.0.1a cross-ref - Empty hero zone does not cease to exist
    Scenario: An empty hero zone still exists
        Given a player has an empty hero zone
        When checking if the hero zone exists
        Then the hero zone still exists even when empty
