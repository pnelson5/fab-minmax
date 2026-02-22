# Feature file for Section 1.1: Players
# Reference: Flesh and Blood Comprehensive Rules Section 1.1
#
# Rule 1.1.1: A player is a person participating in the game.
# Rule 1.1.1a: To participate, a person must have a hero, a card-pool, a way to
#   represent any tokens and counters that could be created by effects in their
#   card-pool, a way to generate uniform random values for effects in their
#   card-pool, a play-space for zones, and a method to record life totals.
# Rule 1.1.2: A player's hero is a hero-card.
# Rule 1.1.2a: This document distinguishes the player as the person participating
#   in the game and the hero as the hero card of a player.
# Rule 1.1.2b: A player plays the game as their hero. Card text makes no
#   distinction between the player and their hero, identifying both identically;
#   the term "you" refers to the player's hero and the term "opponent" refers to
#   the player's opponent's hero.
# Rule 1.1.3: A player's card-pool is a collection of deck-cards and arena-cards.
#   A card can only be included in a player's card-pool if the card's supertypes
#   are a subset of their hero's supertypes.
# Rule 1.1.3a: If an effect allows a player to start the game with one or more
#   cards with supertypes that are not a subset of their hero's supertypes, those
#   cards may be included in the player's card-pool as long as they start the game
#   as specified by the effect. Card text of meta-static abilities refers to the
#   player's card-pool as the player's "deck."
# Rule 1.1.3b: A hybrid card may be included in a player's card-pool if either of
#   the hybrid card's supertype sets is a subset of their hero's supertypes.
# Rule 1.1.4: In a game, a party comprises players who win the game together.
# Rule 1.1.4a: A player is always considered to be in a party with themselves,
#   including when they are the only player in that party.
# Rule 1.1.5: In a game, a player's opponents include all other players who are
#   not in their party.
# Rule 1.1.6: Clockwise order is the order of players starting from the given
#   player and progressing clockwise among the players when viewed from above.

Feature: Section 1.1 - Players
    As a game engine
    I need to correctly model player participation and hero relationships
    So that player identity, card-pool validation, party membership, and turn order work correctly

    # Test for Rule 1.1.1 - A player must have a hero to participate
    Scenario: A player must have a hero to participate in the game
        Given a player is being set up to participate
        When the player does not have a hero
        Then the player is not eligible to participate

    # Test for Rule 1.1.1a - A player must have all required components
    Scenario: A player requires all components to participate
        Given a player is being set up to participate
        When the player has a hero and a card-pool and zones and a life total tracker
        Then the player is eligible to participate

    # Test for Rule 1.1.2 - A player's hero is their hero-card
    Scenario: A player's hero is a hero-card
        Given a player has a hero card of type HERO
        Then the player's hero should be a hero-card
        And the hero should have the HERO card type

    # Test for Rule 1.1.2b - "You" in card text refers to the player's hero
    Scenario: The term you in card text refers to the player's hero
        Given a player has a hero named "Boltyn"
        And an opponent has a different hero
        When card text says "you"
        Then "you" refers to the player's hero
        And "opponent" refers to the opponent's hero

    # Test for Rule 1.1.3 - Card-pool supertype validation (basic)
    Scenario: A card with matching supertypes can be included in a card-pool
        Given a hero with supertypes "Warrior" and "Light"
        And a card with supertypes "Warrior" and "Light"
        Then the card should be eligible for the hero's card-pool
        And the card supertypes are a subset of the hero's supertypes

    # Test for Rule 1.1.3 - Card-pool supertype validation (generic)
    Scenario: A generic card with no supertypes can be included in any hero's card-pool
        Given a hero with supertypes "Warrior"
        And a generic card with no supertypes
        Then the generic card should be eligible for the hero's card-pool
        And an empty set is a subset of any set

    # Test for Rule 1.1.3 - Card-pool supertype restriction
    Scenario: A card with non-matching supertypes cannot be included in a card-pool
        Given a hero with supertypes "Warrior"
        And a card with supertypes "Wizard"
        Then the card should not be eligible for the hero's card-pool
        And "Wizard" is not a subset of the hero's supertypes

    # Test for Rule 1.1.3 - Single supertype matching
    Scenario: A card with one of the hero's supertypes can be in the card-pool
        Given a hero with supertypes "Warrior" and "Light"
        And a card with only the supertype "Warrior"
        Then the card should be eligible for the hero's card-pool
        And a single matching supertype is still a subset

    # Test for Rule 1.1.3a - Effect can allow non-matching supertypes in card-pool
    Scenario: An effect can allow a card with non-matching supertypes in the card-pool
        Given a hero with supertypes "Warrior"
        And a card with supertypes "Wizard"
        And an effect that allows starting with that card in the card-pool
        Then the card can be included in the card-pool under the effect

    # Test for Rule 1.1.3b - Hybrid card can match either supertype set
    Scenario: A hybrid card can be included if either supertype set matches
        Given a hero with supertypes "Warrior" and "Light"
        And a hybrid card with supertype sets "Warrior" and "Wizard"
        Then the hybrid card should be eligible for the hero's card-pool
        And the "Warrior" supertype set is a subset of the hero's supertypes

    # Test for Rule 1.1.4 - Party concept
    Scenario: A player is in a party with themselves
        Given a player named "Alice" is playing
        Then "Alice" should be in a party with herself
        And a player is always in a party with themselves

    # Test for Rule 1.1.4a - Player always in a party with themselves
    Scenario: In a two-player game players are not in the same party
        Given player 0 is playing
        And player 1 is playing
        Then player 0 should not be in a party with player 1
        And each player's party should contain only themselves

    # Test for Rule 1.1.5 - Opponents are players not in the same party
    Scenario: Opponents are players not in the same party
        Given player 0 is playing
        And player 1 is playing
        Then player 1 should be an opponent of player 0
        And player 0 should be an opponent of player 1

    # Test for Rule 1.1.6 - Clockwise order
    Scenario: Clockwise order starts from a given player and goes left
        Given there are three players in the game in clockwise positions
        When determining clockwise order starting from player 0
        Then the next player after player 0 should be player 1
        And the next player after player 1 should be player 2
        And the next player after player 2 should be player 0
