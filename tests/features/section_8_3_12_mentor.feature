# Feature file for Section 8.3.12: Mentor (Ability Keyword)
# Reference: Flesh and Blood Comprehensive Rules Section 8.3.12
#
# 8.3.12 Mentor
#   Note: As of 2022, the mentor ability has been superseded by the Mentor type[8.1.10]
#
# Key aspects:
# - Mentor is classified as an ability keyword (Section 8.3)
# - As of 2022, the Mentor ability keyword was superseded by the Mentor type keyword (8.1.10)
# - The Mentor type keyword (8.1.10) is the current in-use rule:
#   * A mentor card is a deck-card (8.1.10)
#   * A mentor card can only be in a player's card-pool if they have a young hero (8.1.10a)
# - Legacy cards that have the old Mentor ability keyword should be recognized by the engine

Feature: Section 8.3.12 - Mentor Ability Keyword (Superseded)
    As a game engine
    I need to correctly handle the Mentor ability keyword
    So that legacy Mentor ability cards are recognized and the supersession by the Mentor type is enforced

    # ===== Rule 8.3.12: Mentor is listed as an ability keyword =====

    Scenario: Mentor is classified as an ability keyword
        Given the engine's list of ability keywords
        When I check if "Mentor" is in the list of ability keywords
        Then "Mentor" is recognized as an ability keyword

    # ===== Rule 8.3.12: Mentor ability keyword superseded by Mentor type =====

    Scenario: Mentor ability keyword has been superseded by the Mentor type
        Given the engine's keyword registry for ability keywords
        When I look up the "Mentor" ability keyword
        Then the "Mentor" ability keyword is marked as superseded
        And it references the "Mentor" type keyword from section 8.1.10

    # ===== Rule 8.3.12: Legacy Mentor ability cards are recognized =====

    Scenario: A card with the legacy Mentor ability keyword is recognized by the engine
        Given a card has the legacy "Mentor" ability keyword
        When I inspect the ability keywords on the card
        Then the card is recognized as having the "Mentor" ability keyword

    # ===== Rule 8.3.12: Mentor type (8.1.10) supersedes old ability =====

    Scenario: Current Mentor behavior is governed by the Mentor type keyword (8.1.10)
        Given a card with the "Mentor" type
        When the game checks deck construction rules for the card
        Then the Mentor type rules (8.1.10) apply to the card
        And the Mentor ability keyword rules do not apply
