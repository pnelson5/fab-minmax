# Feature file for Section 8.3.13: Phantasm (Ability Keyword)
# Reference: Flesh and Blood Comprehensive Rules Section 8.3.13
#
# 8.3.13 Phantasm
#   Phantasm is a triggered-static ability that means "Whenever this is defended
#   by a non-Illusionist attack action card with 6 or more {p}, destroy this."
#
# 8.3.13a
#   If an attack with Phantasm is being defended by a non-Illusionist attack
#   action card that has the power property with a value of 6 or more, then the
#   state-condition is met and a triggered-layer is put on the stack. When the
#   triggered-layer resolves, if the trigger's event-condition is still met, the
#   attack is destroyed.
#
# 8.3.13b
#   If an attack is destroyed by phantasm before damage for its chain link has
#   been calculated, the combat chain closes.[7.7.2] If an attack is destroyed
#   by phantasm after damage for its chain link has been calculated, the combat
#   chain does not close.

Feature: Section 8.3.13 - Phantasm Ability Keyword
    As a game engine
    I need to correctly implement the Phantasm ability keyword
    So that Phantasm attacks are destroyed when defended by qualifying non-Illusionist attack action cards

    # ===== Rule 8.3.13: Phantasm is classified as an ability keyword =====

    Scenario: Phantasm is classified as an ability keyword
        Given the engine's list of ability keywords
        When I check if "Phantasm" is in the list of ability keywords
        Then "Phantasm" is recognized as an ability keyword

    # ===== Rule 8.3.13a: Phantasm triggers when defended by non-Illusionist attack action card with 6+ power =====

    Scenario: Phantasm attack is destroyed when defended by non-Illusionist attack action card with 6 or more power
        Given a Phantasm attack is on the combat chain
        And a defending card is a non-Illusionist attack action card with 6 power
        When the defending card defends the Phantasm attack
        Then the Phantasm state-condition is met
        And a triggered-layer is placed on the stack to destroy the attack

    # ===== Rule 8.3.13a: Phantasm does NOT trigger for Illusionist attack action cards =====

    Scenario: Phantasm attack is not destroyed when defended by an Illusionist attack action card
        Given a Phantasm attack is on the combat chain
        And a defending card is an Illusionist attack action card with 6 power
        When the defending card defends the Phantasm attack
        Then the Phantasm state-condition is not met
        And no triggered-layer is placed on the stack for Phantasm

    # ===== Rule 8.3.13a: Phantasm does NOT trigger for defenders with less than 6 power =====

    Scenario: Phantasm attack is not destroyed when defended by a non-Illusionist card with less than 6 power
        Given a Phantasm attack is on the combat chain
        And a defending card is a non-Illusionist attack action card with 5 power
        When the defending card defends the Phantasm attack
        Then the Phantasm state-condition is not met
        And no triggered-layer is placed on the stack for Phantasm

    # ===== Rule 8.3.13b: Combat chain closes if Phantasm destroys attack before damage is calculated =====

    Scenario: Combat chain closes when Phantasm attack is destroyed before damage is calculated
        Given a Phantasm attack is on the combat chain
        And damage for the Phantasm attack's chain link has not been calculated yet
        When the Phantasm attack is destroyed by Phantasm
        Then the combat chain closes

    # ===== Rule 8.3.13b: Combat chain does not close if Phantasm destroys attack after damage is calculated =====

    Scenario: Combat chain does not close when Phantasm attack is destroyed after damage is calculated
        Given a Phantasm attack is on the combat chain
        And damage for the Phantasm attack's chain link has already been calculated
        When the Phantasm attack is destroyed by Phantasm
        Then the combat chain does not close
