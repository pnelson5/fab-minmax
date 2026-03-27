# Feature file for Section 8.3.42: Suspense (Ability Keyword)
# Reference: Flesh and Blood Comprehensive Rules Section 8.3.42
#
# 8.3.42 Suspense
#   Suspense is a static ability and two triggered-static abilities that means
#   "This enters the arena with 2 suspense counters,"
#   "At the start of your turn, remove a suspense counter from this," and
#   "When this has no suspense counters, destroy it."
#
# Key aspects:
# - Suspense consists of ONE static ability + TWO triggered-static abilities
# - Static ability: the permanent enters the arena with 2 suspense counters
# - Triggered-static ability 1: at the start of your turn, remove a suspense counter
# - Triggered-static ability 2: when the card has no suspense counters, destroy it
# - The card is destroyed (not returned to hand or deck) when counters run out
# - A card enters with exactly 2 counters (not 1, not 3)
# - After 2 start-of-turn triggers, the card is destroyed

Feature: Section 8.3.42 - Suspense Ability Keyword
    As a game engine
    I need to correctly implement the Suspense ability keyword
    So that Suspense permanents enter with 2 counters, lose one per turn, and are destroyed when counters reach zero

    # ===== Rule 8.3.42: Suspense comprises one static and two triggered-static abilities =====

    Scenario: Suspense is a static ability and two triggered-static abilities
        Given a card has the "Suspense" keyword
        When I inspect the Suspense abilities on the card
        Then the Suspense keyword includes one static ability
        And the Suspense keyword includes two triggered-static abilities

    # ===== Rule 8.3.42: Static ability — card enters arena with 2 suspense counters =====

    Scenario: A card with Suspense enters the arena with 2 suspense counters
        Given a card with the "Suspense" keyword
        When the card enters the arena
        Then the card has 2 suspense counters

    Scenario: A card with Suspense does not enter with fewer than 2 suspense counters
        Given a card with the "Suspense" keyword
        When the card enters the arena
        Then the card does not have 1 suspense counter

    Scenario: A card with Suspense does not enter with more than 2 suspense counters
        Given a card with the "Suspense" keyword
        When the card enters the arena
        Then the card does not have 3 suspense counters

    # ===== Rule 8.3.42: Triggered-static ability 1 — remove a suspense counter at start of turn =====

    Scenario: A suspense counter is removed at the start of the controlling player's turn
        Given a card with the "Suspense" keyword is in the arena with 2 suspense counters
        When the start of the controlling player's turn is processed
        Then the card has 1 suspense counter

    Scenario: A second start-of-turn removes the last suspense counter
        Given a card with the "Suspense" keyword is in the arena with 1 suspense counter
        When the start of the controlling player's turn is processed
        Then the card has 0 suspense counters

    # ===== Rule 8.3.42: Triggered-static ability 2 — destroy card when no suspense counters remain =====

    Scenario: A card with Suspense is destroyed when it has no suspense counters
        Given a card with the "Suspense" keyword is in the arena with 0 suspense counters
        When the no-counters destruction trigger is processed
        Then the card is destroyed

    Scenario: After two start-of-turn triggers a Suspense card is destroyed
        Given a card with the "Suspense" keyword is in the arena with 2 suspense counters
        When the start of the controlling player's turn is processed twice
        Then the card is destroyed

    # ===== Rule 8.3.42: Card with remaining counters is NOT destroyed =====

    Scenario: A card with Suspense is not destroyed while it still has suspense counters
        Given a card with the "Suspense" keyword is in the arena with 2 suspense counters
        When the start of the controlling player's turn is processed
        Then the card is not destroyed
        And the card is still in the arena

    # ===== Rule 8.3.42: Cards without Suspense are not affected =====

    Scenario: A card without Suspense does not enter with suspense counters
        Given a card without the "Suspense" keyword
        When the card enters the arena
        Then the card has no suspense counters
