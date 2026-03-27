# Feature file for Section 8.3.41: Watery Grave (Ability Keyword)
# Reference: Flesh and Blood Comprehensive Rules Section 8.3.41
#
# 8.3.41 Watery Grave
#   Watery Grave is a triggered-static ability that means
#   "When this is put into your graveyard from the arena, turn it face-down."
#
# Key aspects:
# - Watery Grave is a TRIGGERED-STATIC ability
# - It triggers specifically when the card moves from the arena to the graveyard
# - The card is turned face-down upon entering the graveyard
# - Moving from other zones (hand, deck) does NOT trigger Watery Grave
# - Cards without Watery Grave are not turned face-down

Feature: Section 8.3.41 - Watery Grave Ability Keyword
    As a game engine
    I need to correctly implement the Watery Grave ability keyword
    So that cards with Watery Grave are turned face-down when put into the graveyard from the arena

    # ===== Rule 8.3.41: Watery Grave is a triggered-static ability =====

    Scenario: Watery Grave is a triggered-static ability
        Given a card has the "Watery Grave" keyword
        When I inspect the Watery Grave ability on the card
        Then the Watery Grave ability is a triggered-static ability
        And the Watery Grave ability means "When this is put into your graveyard from the arena, turn it face-down"

    # ===== Rule 8.3.41: Card with Watery Grave is turned face-down when moved from arena to graveyard =====

    Scenario: A card with Watery Grave is turned face-down when put into the graveyard from the arena
        Given a card with the "Watery Grave" keyword is in the arena
        When the card is put into the graveyard from the arena
        Then the card is face-down in the graveyard

    # ===== Rule 8.3.41: Watery Grave only triggers from the arena, not from other zones =====

    Scenario: A card with Watery Grave going to graveyard from hand is not turned face-down
        Given a card with the "Watery Grave" keyword is in the hand
        When the card is put into the graveyard from the hand
        Then the card is face-up in the graveyard

    Scenario: A card with Watery Grave going to graveyard from deck is not turned face-down
        Given a card with the "Watery Grave" keyword is in the deck
        When the card is put into the graveyard from the deck
        Then the card is face-up in the graveyard

    # ===== Rule 8.3.41: Cards without Watery Grave are not turned face-down =====

    Scenario: A card without Watery Grave going to graveyard from arena is not turned face-down
        Given a card without the "Watery Grave" keyword is in the arena
        When the card is put into the graveyard from the arena
        Then the card is face-up in the graveyard

    # ===== Rule 8.3.41: Watery Grave triggers on own graveyard =====

    Scenario: Watery Grave triggers when moved to the controlling player's own graveyard
        Given a card with the "Watery Grave" keyword is in the arena
        When the card is put into its owner's graveyard from the arena
        Then the card is face-down in the graveyard
