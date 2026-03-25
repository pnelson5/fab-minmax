# Feature file for Section 8.3.15: Spellvoid (Ability Keyword)
# Reference: Flesh and Blood Comprehensive Rules Section 8.3.15
#
# 8.3.15 Spellvoid
#   Spellvoid is a static ability. Spellvoid is written as "Spellvoid N" which means
#   "If you would be dealt arcane damage, you may destroy this to prevent N of that damage."
#
# 8.3.15a If the controlling player cannot destroy the object with Spellvoid, they cannot
#   apply the optional prevention effect.
#
# Key aspects:
# - Spellvoid is a STATIC ability (not triggered, not meta-static)
# - Written as "Spellvoid N" where N is a positive integer
# - Meaning: "If you would be dealt arcane damage, you may destroy this to prevent N of that damage"
# - Prevention is OPTIONAL — the player chooses whether to destroy the object
# - The cost is DESTROYING the object itself (not paying resources)
# - If the object cannot be destroyed, the prevention effect cannot be applied (Rule 8.3.15a)
# - Spellvoid only applies to arcane damage, not regular combat damage
# - Multiple objects with Spellvoid can each independently be destroyed for their prevention

Feature: Section 8.3.15 - Spellvoid Ability Keyword
    As a game engine
    I need to correctly implement the Spellvoid ability keyword
    So that arcane damage can be optionally prevented by destroying the object

    # ===== Rule 8.3.15: Spellvoid is a static ability =====

    Scenario: Spellvoid is a static ability
        Given a card has the "Spellvoid 1" keyword
        When I inspect the Spellvoid ability on the card
        Then the Spellvoid ability is a static ability
        And the Spellvoid ability is not a triggered ability
        And the Spellvoid ability is not a meta-static ability

    # ===== Rule 8.3.15: Spellvoid meaning is correct =====

    Scenario: Spellvoid N means destroy this to prevent N arcane damage
        Given a card has the "Spellvoid 2" keyword
        When I inspect the Spellvoid ability on the card
        Then the Spellvoid ability means "If you would be dealt arcane damage, you may destroy this to prevent 2 of that damage"
        And the Spellvoid value is 2

    # ===== Rule 8.3.15: Player may destroy object to prevent arcane damage =====

    Scenario: Player destroys object with Spellvoid to prevent arcane damage
        Given a player has an object with "Spellvoid 2"
        And the object can be destroyed
        When the player would be dealt 5 arcane damage
        And the player chooses to activate Spellvoid
        Then the object is destroyed
        And 2 arcane damage is prevented
        And the player is dealt 3 arcane damage

    # ===== Rule 8.3.15: Prevention is optional =====

    Scenario: Player may choose not to activate Spellvoid
        Given a player has an object with "Spellvoid 2"
        And the object can be destroyed
        When the player would be dealt 5 arcane damage
        And the player chooses not to activate Spellvoid
        Then the object is not destroyed
        And the player is dealt 5 arcane damage

    # ===== Rule 8.3.15: Spellvoid does not prevent regular combat damage =====

    Scenario: Spellvoid does not prevent regular combat damage
        Given a player has an object with "Spellvoid 2"
        And the object can be destroyed
        When the player would be dealt 5 regular combat damage
        Then Spellvoid cannot be activated against regular combat damage
        And the player is dealt 5 regular combat damage

    # ===== Rule 8.3.15a: Cannot apply Spellvoid if object cannot be destroyed =====

    Scenario: Player cannot apply Spellvoid if object cannot be destroyed
        Given a player has an object with "Spellvoid 2"
        And the object cannot be destroyed
        When the player would be dealt 5 arcane damage
        Then the player cannot activate Spellvoid
        And the player is dealt 5 arcane damage

    # ===== Rule 8.3.15: Multiple Spellvoid objects each independently usable =====

    Scenario: Multiple Spellvoid objects can each independently prevent arcane damage
        Given a player has an object with "Spellvoid 1"
        And the player also has an object with "Spellvoid 2"
        And both objects can be destroyed
        When the player would be dealt 6 arcane damage
        And the player activates both Spellvoid instances
        Then both objects are destroyed
        And 3 arcane damage is prevented total
        And the player is dealt 3 arcane damage
