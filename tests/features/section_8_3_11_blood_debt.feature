# Feature file for Section 8.3.11: Blood Debt (Ability Keyword)
# Reference: Flesh and Blood Comprehensive Rules Section 8.3.11
#
# 8.3.11 Blood Debt
#   Blood Debt is a triggered-static ability. Blood debt means "While this is
#   in your banished zone, at the beginning of your end phase, lose 1{h}."
#
# 8.3.11a Blood debt only triggers if its source is public in the banished zone
#   at the beginning of the owner's end phase.
#
# Key aspects:
# - Blood Debt is a TRIGGERED-STATIC ability
# - The trigger fires at the beginning of the owner's end phase
# - The trigger condition: the card must be in the owner's banished zone
# - The trigger effect: the owner loses 1{h} (1 life)
# - Rule 8.3.11a: only triggers if the source is PUBLIC in the banished zone
# - Multiple Blood Debt cards in banished zone each trigger separately
# - Blood Debt is tied to the OWNER's end phase, not the opponent's

Feature: Section 8.3.11 - Blood Debt Ability Keyword
    As a game engine
    I need to correctly implement the Blood Debt ability keyword
    So that cards in the banished zone with Blood Debt drain the owner's life at the end phase

    # ===== Rule 8.3.11: Blood Debt is a triggered-static ability =====

    Scenario: Blood Debt is a triggered-static ability
        Given a card has the "Blood Debt" keyword
        When I inspect the Blood Debt ability on the card
        Then the Blood Debt ability is a triggered-static ability
        And the Blood Debt ability is not a play-static ability
        And the Blood Debt ability is not a meta-static ability

    # ===== Rule 8.3.11: Blood Debt meaning is correct =====

    Scenario: Blood Debt meaning is as specified in the rules
        Given a card has the "Blood Debt" keyword
        When I inspect the Blood Debt ability on the card
        Then the Blood Debt ability means "While this is in your banished zone, at the beginning of your end phase, lose 1{h}."

    # ===== Rule 8.3.11: Card with Blood Debt in banished zone causes life loss =====

    Scenario: Card with Blood Debt in banished zone causes owner to lose 1 life at end phase
        Given a player has 20 life
        And a card with "Blood Debt" is in the player's banished zone face-up
        When the player's end phase begins
        Then the player loses 1 life
        And the player has 19 life

    # ===== Rule 8.3.11: Blood Debt triggers at beginning of owner's end phase =====

    Scenario: Blood Debt triggers at the beginning of the end phase
        Given a player has 20 life
        And a card with "Blood Debt" is in the player's banished zone face-up
        When the player's end phase begins
        Then the Blood Debt trigger fires
        And the trigger fires at the beginning of the end phase

    # ===== Rule 8.3.11: Multiple Blood Debt cards each drain 1 life =====

    Scenario: Multiple Blood Debt cards in banished zone each drain 1 life
        Given a player has 20 life
        And 3 cards with "Blood Debt" are in the player's banished zone face-up
        When the player's end phase begins
        Then the player loses 3 life
        And the player has 17 life

    # ===== Rule 8.3.11a: Blood Debt does not trigger if card is face-down =====

    Scenario: Blood Debt does not trigger when card is face-down in banished zone
        Given a player has 20 life
        And a card with "Blood Debt" is in the player's banished zone face-down
        When the player's end phase begins
        Then the Blood Debt trigger does not fire
        And the player still has 20 life

    # ===== Rule 8.3.11: Blood Debt triggers on owner's end phase, not opponent's =====

    Scenario: Blood Debt does not trigger on the opponent's end phase
        Given a player has 20 life
        And a card with "Blood Debt" is in the player's banished zone face-up
        When the opponent's end phase begins
        Then the Blood Debt trigger does not fire
        And the player still has 20 life
