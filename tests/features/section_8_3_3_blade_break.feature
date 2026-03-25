# Feature file for Section 8.3.3: Blade Break (Ability Keyword)
# Reference: Flesh and Blood Comprehensive Rules Section 8.3.3
#
# 8.3.3 Blade Break
#   Blade Break is a triggered-static ability that means "When the combat chain
#   closes, if this defended, destroy it."
#
# Key aspects:
# - Blade Break is a triggered-static ability (not a resolution ability)
# - The trigger fires when the combat chain closes
# - The trigger condition is: "if this defended" (during that chain)
# - The effect is: destroy the card with Blade Break
# - Typically found on equipment cards — the equipment is destroyed after defending
# - Card goes to graveyard when destroyed (unless a replacement effect applies)

Feature: Section 8.3.3 - Blade Break Ability Keyword
    As a game engine
    I need to correctly implement the Blade Break ability keyword
    So that equipment and cards with Blade Break are destroyed after defending

    # ===== Rule 8.3.3: Blade Break is a triggered-static ability =====

    Scenario: Blade Break is a triggered-static ability
        Given a card with the "Blade Break" keyword ability
        When I inspect the Blade Break ability on the card
        Then the Blade Break ability is a triggered-static ability

    Scenario: Blade Break ability has the correct triggered-static meaning
        Given a card with the "Blade Break" keyword ability
        When I inspect the Blade Break ability on the card
        Then the Blade Break ability means "When the combat chain closes, if this defended, destroy it"

    # ===== Rule 8.3.3: Trigger fires when combat chain closes after defending =====

    Scenario: Blade Break destroys the card when it defended and combat chain closes
        Given a card with the "Blade Break" keyword ability in a defend zone
        And the Blade Break card defended an attack during the current combat chain
        When the combat chain closes
        Then the Blade Break card is destroyed

    Scenario: Blade Break does not trigger when card did not defend
        Given a card with the "Blade Break" keyword ability in a defend zone
        And the Blade Break card did not defend during the current combat chain
        When the combat chain closes
        Then the Blade Break card is not destroyed

    # ===== Rule 8.3.3: Destroyed card leaves the zone =====

    Scenario: A destroyed Blade Break card is removed from the defend zone
        Given a card with the "Blade Break" keyword ability in a defend zone
        And the Blade Break card defended an attack during the current combat chain
        When the combat chain closes
        Then the Blade Break card is no longer in the defend zone

    # ===== Rule 8.3.3: Blade Break triggers regardless of combat outcome =====

    Scenario: Blade Break triggers even when the attack is fully blocked
        Given a card with the "Blade Break" keyword ability in a defend zone
        And the Blade Break card defended an attack during the current combat chain
        And the attack was fully blocked by the defending card
        When the combat chain closes
        Then the Blade Break card is destroyed

    Scenario: Blade Break triggers when the attack deals damage
        Given a card with the "Blade Break" keyword ability in a defend zone
        And the Blade Break card defended an attack during the current combat chain
        And the attack dealt damage despite the defense
        When the combat chain closes
        Then the Blade Break card is destroyed
