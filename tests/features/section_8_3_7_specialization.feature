# Feature file for Section 8.3.7: Specialization (Ability Keyword)
# Reference: Flesh and Blood Comprehensive Rules Section 8.3.7
#
# 8.3.7 Specialization
#   Specialization is a meta-static ability. Specialization is written as
#   "[HERO] Specialization" which means "You may only have this in your deck
#   if your hero is [HERO]," where HERO is the moniker of the player's hero card.
#
# Key aspects:
# - Specialization is a META-STATIC ability (applies at deck construction, outside the game)
# - Specialization is written "[HERO] Specialization" — HERO is the moniker
# - A card with "[HERO] Specialization" may only be in a deck whose hero has that moniker
# - Moniker is the most significant identifier of a hero's name (e.g., "Dorinthea"
#   from "Dorinthea Ironsong")
# - Card effects can override the Specialization restriction (Rule 1.0.1a, Rule 5.4.3a)
#   Example: Shiyana, Diamond Gemini — "You may have specialization cards of any hero in your deck"
# - If a meta-static ability ceases to exist during a game, it does not affect
#   the legality of the rules followed outside the game (Rule 5.4.3a)

Feature: Section 8.3.7 - Specialization Ability Keyword
    As a game engine
    I need to correctly implement the Specialization ability keyword
    So that deck construction enforces hero-specific card restrictions

    # ===== Rule 8.3.7: Specialization is a meta-static ability =====

    Scenario: Specialization is a meta-static ability
        Given a card has the "Dorinthea Specialization" keyword
        When I inspect the Specialization ability on the card
        Then the Specialization ability is a meta-static ability
        And the Specialization ability means "You may only have this in your deck if your hero is Dorinthea"

    # ===== Rule 8.3.7: Deck valid when hero matches specialization =====

    Scenario: A deck is valid when the hero moniker matches the Specialization keyword
        Given a constructed deck with hero "Dorinthea Ironsong"
        And the deck contains a card named "Dorinthea Specialization Card" with "Dorinthea Specialization"
        When the deck is validated for constructed play
        Then the deck is valid with respect to the Specialization restriction

    # ===== Rule 8.3.7: Deck invalid when hero does not match specialization =====

    Scenario: A deck is invalid when the hero moniker does not match the Specialization keyword
        Given a constructed deck with hero "Bravo, Showstopper"
        And the deck contains a card named "Dorinthea Specialization Card" with "Dorinthea Specialization"
        When the deck is validated for constructed play
        Then the deck is invalid
        And the validation error mentions the Specialization restriction

    # ===== Rule 8.3.7: Hero moniker (not full name) is used for matching =====

    Scenario: The hero moniker is used for Specialization matching, not the full name
        Given a constructed deck with hero "Dorinthea Ironsong"
        And the deck contains a card named "Ironsong Specialization Card" with "Dorinthea Specialization"
        When the deck is validated for constructed play
        Then the deck is valid with respect to the Specialization restriction
        And the Specialization match is based on the moniker "Dorinthea"

    # ===== Rule 8.3.7: Non-Specialization card not restricted by hero =====

    Scenario: A card without Specialization is not restricted by hero identity
        Given a constructed deck with hero "Bravo, Showstopper"
        And the deck contains a card named "Generic Card" without the Specialization keyword
        When the deck is validated for constructed play
        Then the deck is valid with respect to the generic card

    # ===== Rule 5.4.3a: Effect can override Specialization restriction =====

    Scenario: A card effect can allow Specialization cards of any hero in the deck
        Given a constructed deck with hero "Shiyana, Diamond Gemini"
        And the hero has an ability "You may have specialization cards of any hero in your deck"
        And the deck contains a card named "Dorinthea Specialization Card" with "Dorinthea Specialization"
        When the deck is validated for constructed play
        Then the deck is valid because the Specialization restriction is overridden

    # ===== Rule 5.4.3a: Losing meta-static ability during game does not affect deck legality =====

    Scenario: Losing a Specialization override effect during a game does not make deck illegal
        Given a constructed deck with hero "Shiyana, Diamond Gemini"
        And the hero has an ability "You may have specialization cards of any hero in your deck"
        And the deck contains a card named "Dorinthea Specialization Card" with "Dorinthea Specialization"
        And the deck was legally constructed under that hero ability
        When the hero loses the specialization override ability during the game
        Then the presence of Dorinthea Specialization Card in the card pool remains legal
