# Feature file for Section 8.3.6: Legendary (Ability Keyword)
# Reference: Flesh and Blood Comprehensive Rules Section 8.3.6
#
# 8.3.6 Legendary
#   Legendary is a meta-static ability that means
#   "You may only have 1 of this in your constructed deck."
#
# Key aspects:
# - Legendary is a META-STATIC ability (not just a restriction; applies at deck construction)
# - A deck may contain at most 1 copy of any Legendary card
# - A deck may not contain 2 or more copies of a Legendary card
# - Non-Legendary cards follow normal copy limits (not Legendary's limit-of-1)

Feature: Section 8.3.6 - Legendary Ability Keyword
    As a game engine
    I need to correctly implement the Legendary ability keyword
    So that deck construction enforces the 1-copy limit for Legendary cards

    # ===== Rule 8.3.6: Legendary is a meta-static ability =====

    Scenario: Legendary is a meta-static ability
        Given a card has the "Legendary" keyword
        When I inspect the Legendary ability on the card
        Then the Legendary ability is a meta-static ability
        And the Legendary ability means "You may only have 1 of this in your constructed deck"

    # ===== Rule 8.3.6: Deck validation with a single Legendary card =====

    Scenario: A deck with exactly 1 copy of a Legendary card is valid
        Given a constructed deck
        And the deck contains exactly 1 copy of a card named "Legendary Card" with the Legendary keyword
        When the deck is validated for constructed play
        Then the deck is valid with respect to the Legendary card

    # ===== Rule 8.3.6: Deck validation with two Legendary cards =====

    Scenario: A deck with 2 copies of a Legendary card is invalid
        Given a constructed deck
        And the deck contains 2 copies of a card named "Legendary Card" with the Legendary keyword
        When the deck is validated for constructed play
        Then the deck is invalid
        And the validation error mentions the Legendary restriction

    # ===== Rule 8.3.6: Deck validation with three Legendary cards =====

    Scenario: A deck with 3 copies of a Legendary card is invalid
        Given a constructed deck
        And the deck contains 3 copies of a card named "Legendary Card" with the Legendary keyword
        When the deck is validated for constructed play
        Then the deck is invalid
        And the validation error mentions the Legendary restriction

    # ===== Rule 8.3.6: Non-Legendary card is not subject to the Legendary limit =====

    Scenario: A non-Legendary card is not restricted to 1 copy
        Given a constructed deck
        And the deck contains 3 copies of a card named "Normal Card" without the Legendary keyword
        When the deck is validated for constructed play
        Then the deck is valid with respect to "Normal Card" copy count

    # ===== Rule 8.3.6: Multiple different Legendary cards are each allowed once =====

    Scenario: A deck may contain 1 copy each of multiple different Legendary cards
        Given a constructed deck
        And the deck contains 1 copy of a card named "Legendary Card A" with the Legendary keyword
        And the deck contains 1 copy of a card named "Legendary Card B" with the Legendary keyword
        When the deck is validated for constructed play
        Then the deck is valid with respect to both Legendary cards
