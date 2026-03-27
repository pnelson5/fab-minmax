# Feature file for Section 8.3.37: Arcane Shelter (Ability Keyword)
# Reference: Flesh and Blood Comprehensive Rules Section 8.3.37
#
# 8.3.37 Arcane Shelter
#   Arcane Shelter is a static ability. Arcane Shelter is written as "Arcane Shelter N"
#   which means "If you would be dealt arcane damage, destroy this to prevent N of
#   that damage."
#
# Key aspects:
# - Arcane Shelter is a STATIC ability
# - Written as "Arcane Shelter N" where N is a positive integer
# - Meaning: "If you would be dealt arcane damage, destroy this to prevent N of that damage"
# - The card/equipment with Arcane Shelter is DESTROYED to activate the prevention
# - Destroying the card is the cost — no resource payment required
# - Prevention is optional — the player chooses whether to destroy the card
# - Unlike Arcane Barrier, no resource cost is paid; the card itself is sacrificed
# - Arcane Shelter only applies to arcane damage, not regular combat damage

Feature: Section 8.3.37 - Arcane Shelter Ability Keyword
    As a game engine
    I need to correctly implement the Arcane Shelter ability keyword
    So that arcane damage can be prevented by destroying the card with Arcane Shelter

    # ===== Rule 8.3.37: Arcane Shelter is a static ability =====

    Scenario: Arcane Shelter is a static ability
        Given a card has the "Arcane Shelter 1" keyword
        When I inspect the Arcane Shelter ability on the card
        Then the Arcane Shelter ability is a static ability
        And the Arcane Shelter ability is not a triggered ability
        And the Arcane Shelter ability is not a meta-static ability

    # ===== Rule 8.3.37: Arcane Shelter meaning is correct =====

    Scenario: Arcane Shelter N means destroy this to prevent N arcane damage
        Given a card has the "Arcane Shelter 2" keyword
        When I inspect the Arcane Shelter ability on the card
        Then the Arcane Shelter ability means "If you would be dealt arcane damage, destroy this to prevent 2 of that damage"
        And the Arcane Shelter value is 2

    # ===== Rule 8.3.37: Destroying the card prevents N arcane damage =====

    Scenario: Player destroys Arcane Shelter equipment to prevent arcane damage
        Given a player has an equipment with "Arcane Shelter 2"
        When the player would be dealt 5 arcane damage
        And the player chooses to activate Arcane Shelter
        Then the equipment with Arcane Shelter is destroyed
        And 2 arcane damage is prevented
        And the player is dealt 3 arcane damage

    # ===== Rule 8.3.37: Prevention is optional — player may choose not to destroy =====

    Scenario: Player may choose not to activate Arcane Shelter
        Given a player has an equipment with "Arcane Shelter 2"
        When the player would be dealt 5 arcane damage
        And the player chooses not to activate Arcane Shelter
        Then the equipment with Arcane Shelter is not destroyed
        And the player is dealt 5 arcane damage

    # ===== Rule 8.3.37: Arcane Shelter does not apply to regular combat damage =====

    Scenario: Arcane Shelter does not prevent regular combat damage
        Given a player has an equipment with "Arcane Shelter 2"
        When the player would be dealt 5 regular combat damage
        Then Arcane Shelter cannot be activated against regular combat damage
        And the player is dealt 5 regular combat damage

    # ===== Rule 8.3.37: Card is destroyed (not discarded or exiled) =====

    Scenario: Activating Arcane Shelter destroys the card
        Given a player has an equipment with "Arcane Shelter 1" in play
        When the player activates Arcane Shelter to prevent arcane damage
        Then the equipment is moved to the graveyard
        And the equipment is no longer in the equipment zone

    # ===== Rule 8.3.37: Arcane Shelter only prevents up to N damage =====

    Scenario: Arcane Shelter prevents exactly N damage, not more
        Given a card has the "Arcane Shelter 3" keyword
        And the player has the card equipped
        When the player would be dealt 2 arcane damage
        And the player chooses to activate Arcane Shelter
        Then the equipment with Arcane Shelter is destroyed
        And 2 arcane damage is prevented
        And the player is dealt 0 arcane damage
