# Feature file for Section 8.3.2: Battleworn (Ability Keyword)
# Reference: Flesh and Blood Comprehensive Rules Section 8.3.2
#
# 8.3.2 Battleworn
#   Battleworn is a triggered-static ability that means "When the combat chain
#   closes, if this defended, put a -1{d} counter on it."
#
# Key aspects:
# - Battleworn is a triggered-static ability (not a resolution ability)
# - The trigger fires when the combat chain closes
# - The trigger condition is: "if this defended" (during that chain)
# - The effect is: put a -1{d} counter on the card with Battleworn
# - -1{d} counters reduce the defense value of the card

Feature: Section 8.3.2 - Battleworn Ability Keyword
    As a game engine
    I need to correctly implement the Battleworn ability keyword
    So that equipment and cards with Battleworn degrade after defending

    # ===== Rule 8.3.2: Battleworn is a triggered-static ability =====

    Scenario: Battleworn is a triggered-static ability
        Given a card with the "Battleworn" keyword ability
        When I inspect the Battleworn ability on the card
        Then the Battleworn ability is a triggered-static ability

    Scenario: Battleworn ability has the correct triggered-static meaning
        Given a card with the "Battleworn" keyword ability
        When I inspect the Battleworn ability on the card
        Then the Battleworn ability means "When the combat chain closes, if this defended, put a -1{d} counter on it"

    # ===== Rule 8.3.2: Trigger fires when combat chain closes after defending =====

    Scenario: Battleworn triggers when card defended and combat chain closes
        Given a card with the "Battleworn" keyword ability in a defend zone
        And the card defended an attack during the current combat chain
        When the combat chain closes
        Then a -1{d} counter is placed on the Battleworn card
        And the Battleworn card has 1 counter on it

    Scenario: Battleworn does not trigger when card did not defend
        Given a card with the "Battleworn" keyword ability in a defend zone
        And the card did not defend during the current combat chain
        When the combat chain closes
        Then no -1{d} counter is placed on the Battleworn card
        And the Battleworn card has 0 counters on it

    # ===== Rule 8.3.2: -1{d} counter reduces defense value =====

    Scenario: A -1{d} counter reduces the defense value of the card
        Given an equipment card with defense value 3 and the "Battleworn" keyword ability
        And the equipment defended an attack during the current combat chain
        When the combat chain closes
        Then a -1{d} counter is placed on the Battleworn card
        And the effective defense value of the Battleworn card is 2

    # ===== Rule 8.3.2: Multiple chains accumulate counters =====

    Scenario: Battleworn card accumulates counters across multiple chains
        Given a card with the "Battleworn" keyword ability in a defend zone
        And the card has 1 counter from a previous chain
        And the card defended an attack during the current combat chain
        When the combat chain closes
        Then a -1{d} counter is placed on the Battleworn card
        And the Battleworn card has 2 counters on it

    # ===== Rule 8.3.2: Only one counter per chain close =====

    Scenario: Battleworn places exactly one counter when triggered
        Given a card with the "Battleworn" keyword ability in a defend zone
        And the card defended multiple attacks in the current combat chain
        When the combat chain closes
        Then exactly 1 new -1{d} counter is placed on the Battleworn card
