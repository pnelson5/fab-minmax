# Feature file for Section 8.3.40: Unlimited (Ability Keyword)
# Reference: Flesh and Blood Comprehensive Rules Section 8.3.40
#
# 8.3.40 Unlimited
#   Unlimited is a meta-static ability that means
#   "You may have any number of this card in your deck."
#
# Key aspects:
# - Unlimited is a META-STATIC ability (applies at deck construction)
# - A deck may contain any number of copies of an Unlimited card
# - Without Unlimited, cards are subject to normal copy limits
# - Unlimited overrides default copy-count restrictions for that card

Feature: Section 8.3.40 - Unlimited Ability Keyword
    As a game engine
    I need to correctly implement the Unlimited ability keyword
    So that deck construction allows any number of copies of Unlimited cards

    # ===== Rule 8.3.40: Unlimited is a meta-static ability =====

    Scenario: Unlimited is a meta-static ability
        Given a card has the "Unlimited" keyword
        When I inspect the Unlimited ability on the card
        Then the Unlimited ability is a meta-static ability
        And the Unlimited ability means "You may have any number of this card in your deck"

    # ===== Rule 8.3.40: A deck with many copies of an Unlimited card is valid =====

    Scenario: A deck with 4 copies of an Unlimited card is valid
        Given a constructed deck
        And the deck contains 4 copies of a card named "Unlimited Card" with the Unlimited keyword
        When the deck is validated for constructed play
        Then the deck is valid with respect to the Unlimited card copy count

    # ===== Rule 8.3.40: A deck with even more copies of an Unlimited card is valid =====

    Scenario: A deck with 10 copies of an Unlimited card is valid
        Given a constructed deck
        And the deck contains 10 copies of a card named "Unlimited Card" with the Unlimited keyword
        When the deck is validated for constructed play
        Then the deck is valid with respect to the Unlimited card copy count

    # ===== Rule 8.3.40: A deck with 1 copy of an Unlimited card is also valid =====

    Scenario: A deck with 1 copy of an Unlimited card is valid
        Given a constructed deck
        And the deck contains 1 copy of a card named "Unlimited Card" with the Unlimited keyword
        When the deck is validated for constructed play
        Then the deck is valid with respect to the Unlimited card copy count

    # ===== Rule 8.3.40: Non-Unlimited card does not gain the unrestricted-copy benefit =====

    Scenario: A card without Unlimited does not get the unlimited-copy benefit
        Given a constructed deck
        And the deck contains 4 copies of a card named "Normal Card" without the Unlimited keyword
        When the deck is validated for constructed play
        Then the deck is not valid due to exceeding normal copy limits for "Normal Card"

    # ===== Rule 8.3.40: Multiple Unlimited cards can each appear in any number =====

    Scenario: A deck may contain many copies each of multiple different Unlimited cards
        Given a constructed deck
        And the deck contains 5 copies of a card named "Unlimited Card A" with the Unlimited keyword
        And the deck contains 5 copies of a card named "Unlimited Card B" with the Unlimited keyword
        When the deck is validated for constructed play
        Then the deck is valid with respect to both Unlimited card copy counts
