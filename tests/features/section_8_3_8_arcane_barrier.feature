# Feature file for Section 8.3.8: Arcane Barrier (Ability Keyword)
# Reference: Flesh and Blood Comprehensive Rules Section 8.3.8
#
# 8.3.8 Arcane Barrier
#   Arcane Barrier is a static ability. Arcane Barrier is written as "Arcane Barrier N"
#   which means "If you would be dealt arcane damage, you may pay N{r} to prevent N of
#   that damage."
#
# Key aspects:
# - Arcane Barrier is a STATIC ability (not triggered-static, not meta-static)
# - Written as "Arcane Barrier N" where N is a positive integer
# - Meaning: "If you would be dealt arcane damage, you may pay N{r} to prevent N of that damage"
# - Prevention is OPTIONAL — the player chooses whether to pay the cost
# - Paying N{r} (N resource points) prevents exactly N arcane damage
# - Multiple instances of Arcane Barrier can each independently be activated
# - Arcane Barrier only applies to arcane damage, not regular combat damage
# - If the player cannot pay the cost (insufficient resources), they cannot apply the prevention

Feature: Section 8.3.8 - Arcane Barrier Ability Keyword
    As a game engine
    I need to correctly implement the Arcane Barrier ability keyword
    So that arcane damage can be optionally prevented by paying resources

    # ===== Rule 8.3.8: Arcane Barrier is a static ability =====

    Scenario: Arcane Barrier is a static ability
        Given a card has the "Arcane Barrier 1" keyword
        When I inspect the Arcane Barrier ability on the card
        Then the Arcane Barrier ability is a static ability
        And the Arcane Barrier ability is not a triggered ability
        And the Arcane Barrier ability is not a meta-static ability

    # ===== Rule 8.3.8: Arcane Barrier meaning is correct =====

    Scenario: Arcane Barrier N means pay N resources to prevent N arcane damage
        Given a card has the "Arcane Barrier 2" keyword
        When I inspect the Arcane Barrier ability on the card
        Then the Arcane Barrier ability means "If you would be dealt arcane damage, you may pay 2{r} to prevent 2 of that damage"
        And the Arcane Barrier value is 2

    # ===== Rule 8.3.8: Player may pay to prevent arcane damage =====

    Scenario: Player pays Arcane Barrier cost to prevent arcane damage
        Given a player has an equipment with "Arcane Barrier 1"
        And the player has 1 or more resources available
        When the player would be dealt 3 arcane damage
        And the player chooses to activate Arcane Barrier
        Then the player pays 1 resource
        And 1 arcane damage is prevented
        And the player is dealt 2 arcane damage

    # ===== Rule 8.3.8: Prevention is optional — player may choose not to pay =====

    Scenario: Player may choose not to activate Arcane Barrier
        Given a player has an equipment with "Arcane Barrier 1"
        And the player has 1 or more resources available
        When the player would be dealt 3 arcane damage
        And the player chooses not to activate Arcane Barrier
        Then no resources are spent on Arcane Barrier
        And the player is dealt 3 arcane damage

    # ===== Rule 8.3.8: Arcane Barrier does not apply to regular combat damage =====

    Scenario: Arcane Barrier does not prevent regular combat damage
        Given a player has an equipment with "Arcane Barrier 1"
        And the player has 1 or more resources available
        When the player would be dealt 3 regular combat damage
        Then Arcane Barrier cannot be activated against regular combat damage
        And the player is dealt 3 regular combat damage

    # ===== Rule 8.3.8: Player cannot use Arcane Barrier without sufficient resources =====

    Scenario: Player cannot activate Arcane Barrier without sufficient resources
        Given a player has an equipment with "Arcane Barrier 2"
        And the player has 0 resources available
        When the player would be dealt 3 arcane damage
        Then the player cannot activate Arcane Barrier
        And the player is dealt 3 arcane damage

    # ===== Rule 8.3.8: Multiple instances of Arcane Barrier can each be activated =====

    Scenario: Multiple Arcane Barrier instances can each be independently activated
        Given a player has an equipment with "Arcane Barrier 1"
        And the player also has an equipment with "Arcane Barrier 1"
        And the player has 2 or more resources available
        When the player would be dealt 5 arcane damage
        And the player activates both Arcane Barrier instances
        Then the player pays 2 resources total
        And 2 arcane damage is prevented total
        And the player is dealt 3 arcane damage
