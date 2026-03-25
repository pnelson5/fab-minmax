# Feature file for Section 8.3.23: Piercing (Ability Keyword)
# Reference: Flesh and Blood Comprehensive Rules Section 8.3.23
#
# Rule 8.3.23: Piercing is a static ability. Piercing is written as
# "Piercing N" which means "If this is defended by an equipment, it gets +N{p}."

Feature: Section 8.3.23 - Piercing Ability Keyword
    As a game engine
    I need to correctly implement the Piercing ability keyword
    So that attacks with Piercing N gain +N power when defended by equipment

    # Rule 8.3.23: Piercing is a static ability
    Scenario: Piercing is a static ability
        Given a card with Piercing 2 ability
        When I inspect the Piercing ability
        Then the Piercing ability is a static ability

    # Rule 8.3.23: Piercing is written as "Piercing N"
    Scenario: Piercing ability has correct numeric value
        Given a card with Piercing 2 ability
        When I inspect the Piercing ability
        Then the Piercing value is 2

    # Rule 8.3.23: +N power when defended by equipment
    Scenario: Piercing increases attack power when defended by equipment
        Given an attack with Piercing 2
        And the base power of the attack is 3
        When the attack is defended by an equipment card
        Then the attack power is 5

    # Rule 8.3.23: No bonus when not defended by equipment
    Scenario: Piercing does not increase power when not defended by equipment
        Given an attack with Piercing 2
        And the base power of the attack is 3
        When the attack is defended only by an action card
        Then the attack power is 3

    # Rule 8.3.23: Power bonus scales with N
    Scenario: Piercing 3 increases attack power by 3
        Given an attack with Piercing 3
        And the base power of the attack is 4
        When the attack is defended by an equipment card
        Then the attack power is 7

    # Rule 8.3.23: Piercing 1 gives only +1
    Scenario: Piercing 1 increases attack power by exactly 1
        Given an attack with Piercing 1
        And the base power of the attack is 5
        When the attack is defended by an equipment card
        Then the attack power is 6

    # Rule 8.3.23: Bonus applies when equipment is added, not retroactively removed
    Scenario: Piercing power bonus does not apply before equipment defends
        Given an attack with Piercing 2
        And the base power of the attack is 3
        When the attack has no defenders
        Then the attack power is 3

    # Rule 8.3.23: Piercing applies with multiple equipment defenders
    Scenario: Piercing power bonus applies when multiple equipment defend
        Given an attack with Piercing 2
        And the base power of the attack is 3
        When the attack is defended by two equipment cards
        Then the attack power is 5
