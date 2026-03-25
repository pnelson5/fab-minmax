# Feature file for Section 8.3.10: Temper (Ability Keyword)
# Reference: Flesh and Blood Comprehensive Rules Section 8.3.10
#
# 8.3.10 Temper
#   Temper is a triggered-static ability that means "When the combat chain closes,
#   if this defended, put a -1{d} counter on it, then destroy it if it has zero {d}."
#
# Key aspects:
# - Temper is a TRIGGERED-STATIC ability (not play-static, not meta-static)
# - Temper triggers when the combat chain closes
# - The trigger only fires if the card with Temper actually defended that combat chain
# - When triggered: put a -1{d} counter on the card
# - After placing the counter: if the card now has zero {d}, destroy it
# - If the card still has defense remaining (>0), it is NOT destroyed
# - Temper is typically found on equipment cards (which have defense values)

Feature: Section 8.3.10 - Temper Ability Keyword
    As a game engine
    I need to correctly implement the Temper ability keyword
    So that equipment with Temper loses defense counters when used to defend and is destroyed at zero defense

    # ===== Rule 8.3.10: Temper is a triggered-static ability =====

    Scenario: Temper is a triggered-static ability
        Given a card has the "Temper" keyword
        When I inspect the Temper ability on the card
        Then the Temper ability is a triggered-static ability
        And the Temper ability is not a play-static ability
        And the Temper ability is not a meta-static ability

    # ===== Rule 8.3.10: Temper meaning is correct =====

    Scenario: Temper meaning is as specified in the rules
        Given a card has the "Temper" keyword
        When I inspect the Temper ability on the card
        Then the Temper ability means "When the combat chain closes, if this defended, put a -1{d} counter on it, then destroy it if it has zero {d}."

    # ===== Rule 8.3.10: Defending with a Temper card places a counter on chain close =====

    Scenario: Temper card gains a defense counter when used to defend and the chain closes
        Given an equipment card with "Temper" and 3 defense is in play
        And the equipment card was used to defend during the combat chain
        When the combat chain closes
        Then a -1{d} counter is placed on the equipment card
        And the equipment card has 2 effective defense remaining
        And the equipment card is not destroyed

    # ===== Rule 8.3.10: Temper card with 1 defense is destroyed when chain closes =====

    Scenario: Temper card with 1 defense is destroyed when chain closes after defending
        Given an equipment card with "Temper" and 1 defense is in play
        And the equipment card was used to defend during the combat chain
        When the combat chain closes
        Then a -1{d} counter is placed on the equipment card
        And the equipment card has zero defense remaining
        And the equipment card is destroyed

    # ===== Rule 8.3.10: Temper only triggers if the card defended =====

    Scenario: Temper does not trigger when the card did not defend
        Given an equipment card with "Temper" and 3 defense is in play
        And the equipment card was NOT used to defend during the combat chain
        When the combat chain closes
        Then no -1{d} counter is placed on the equipment card
        And the equipment card is not destroyed

    # ===== Rule 8.3.10: Multiple defenses - each chain close reduces defense =====

    Scenario: Temper card loses a defense counter each time it defends and the chain closes
        Given an equipment card with "Temper" and 2 defense is in play
        And the equipment card was used to defend during the first combat chain
        When the first combat chain closes
        Then a -1{d} counter is placed on the equipment card after the first chain
        And the equipment card has 1 effective defense remaining
        And the equipment card is not destroyed after the first chain

    # ===== Rule 8.3.10: Temper card is destroyed when defense reaches zero =====

    Scenario: Temper card is destroyed when defense counters reduce it to zero
        Given an equipment card with "Temper" and 1 defense remaining is in play
        And the equipment card was used to defend during the combat chain
        When the combat chain closes
        Then the equipment card has zero defense remaining
        And the equipment card is destroyed
