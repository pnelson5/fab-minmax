# Feature file for Section 8.3.16: Essence (Ability Keyword)
# Reference: Flesh and Blood Comprehensive Rules Section 8.3.16
#
# 8.3.16 Essence
#   Essence is a meta-static ability. Essence is written in the format
#   "Essence of [SUPERTYPES]" which means "You may have [SUPERTYPES] cards
#   in your deck, as though your hero had those supertypes," where SUPERTYPES
#   is a list of one or more supertypes. [2.11]
#
# Key aspects:
# - Essence is a META-STATIC ability (applies at deck construction, outside the game)
# - Written "Essence of [SUPERTYPES]" — SUPERTYPES is one or more supertype keywords
# - Essence expands which supertype cards the player may include in their deck
# - Without Essence, a card may only be in a deck if its supertypes are a subset
#   of the hero's supertypes (Rule 1.1.3)
# - With Essence of [X], the player may include [X] cards as though their hero
#   had the [X] supertypes
# - Essence can grant access to multiple supertypes at once
# - A card with a supertype NOT covered by Essence is still restricted normally
# - Since it is meta-static, losing Essence during a game does not retroactively
#   make the deck illegal (Rule 5.4.3a)

Feature: Section 8.3.16 - Essence Ability Keyword
    As a game engine
    I need to correctly implement the Essence ability keyword
    So that deck construction allows supertype-crossing via the Essence meta-static ability

    # ===== Rule 8.3.16: Essence is a meta-static ability =====

    Scenario: Essence is a meta-static ability
        Given a card has the "Essence of Ninja" keyword
        When I inspect the Essence ability on the card
        Then the Essence ability is a meta-static ability
        And the Essence ability means "You may have Ninja cards in your deck, as though your hero had those supertypes"

    # ===== Rule 8.3.16: Essence allows including specified supertype cards in deck =====

    Scenario: A hero without a supertype can include cards of that supertype via Essence
        Given a hero "Boltyn, Breaker of Dawn" with supertypes "Light Warrior"
        And a card with "Essence of Ninja" is in the player's card pool
        And a Ninja card is in the player's deck
        When the deck is validated for constructed play
        Then the deck is valid because Essence of Ninja grants access to Ninja cards

    # ===== Rule 8.3.16: Without Essence, hero cannot include non-hero-supertype cards =====

    Scenario: Without Essence a hero cannot include cards of a non-matching supertype
        Given a hero "Boltyn, Breaker of Dawn" with supertypes "Light Warrior"
        And no Essence card is in the player's card pool
        And a Ninja card is in the player's deck
        When the deck is validated for constructed play
        Then the deck is invalid because Ninja is not in the hero's supertypes

    # ===== Rule 8.3.16: Essence only covers the listed supertypes =====

    Scenario: Essence of Ninja does not grant access to other supertypes
        Given a hero "Boltyn, Breaker of Dawn" with supertypes "Light Warrior"
        And a card with "Essence of Ninja" is in the player's card pool
        And a Guardian card is in the player's deck
        When the deck is validated for constructed play
        Then the deck is invalid because Guardian is not covered by Essence of Ninja

    # ===== Rule 8.3.16: Essence with multiple supertypes =====

    Scenario: Essence can grant access to multiple supertypes simultaneously
        Given a hero "Boltyn, Breaker of Dawn" with supertypes "Light Warrior"
        And a card with "Essence of Ninja Wizard" is in the player's card pool
        And a Ninja card is in the player's deck
        And a Wizard card is in the player's deck
        When the deck is validated for constructed play
        Then the deck is valid because Essence of Ninja Wizard covers both supertypes

    # ===== Rule 8.3.16: Essence meaning format is correct =====

    Scenario: Essence ability meaning is correctly formatted with the specified supertypes
        Given a card has the "Essence of Guardian" keyword
        When I inspect the Essence ability on the card
        Then the Essence ability is a meta-static ability
        And the Essence ability means "You may have Guardian cards in your deck, as though your hero had those supertypes"

    # ===== Rule 5.4.3a: Losing Essence during game does not affect deck legality =====

    Scenario: Losing an Essence card during a game does not make the deck illegal
        Given a hero "Boltyn, Breaker of Dawn" with supertypes "Light Warrior"
        And a card with "Essence of Ninja" is in the player's card pool
        And a Ninja card is in the player's deck
        And the deck was legally constructed with the Essence card present
        When the Essence card is removed from the card pool during the game
        Then the Ninja cards in the deck remain legal despite the Essence card being gone
