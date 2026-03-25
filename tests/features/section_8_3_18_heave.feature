# Feature file for Section 8.3.18: Heave (Ability Keyword)
# Reference: Flesh and Blood Comprehensive Rules Section 8.3.18
#
# 8.3.18 Heave
#   Heave is a hidden triggered ability. Heave is written as "Heave N" which
#   means "While this is in your hand, at the beginning of your end phase, you
#   may pay N{r} and put this face-up into your arsenal. If you do, create N
#   Seismic Surge tokens."
#
# 8.3.18a If a player pays the cost to pay the resource point cost and put the
#   card with Heave face-up into their arsenal, the player is considered to have
#   heaved and the card is considered to have been heaved.
#
# 8.3.18b A player cannot heave if they cannot pay the resource point cost or
#   put the card with Heave face-up into their arsenal.
#
# Key aspects:
# - Heave is a HIDDEN TRIGGERED ability (not visible on card face)
# - Heave triggers at the BEGINNING OF THE END PHASE while the card is IN HAND
# - Heave is OPTIONAL — the player may choose to pay the cost or not
# - Paying Heave costs: N resource points + move card face-up to arsenal
# - Effect on payment: create N Seismic Surge tokens
# - Both conditions must be met to have "heaved": pay resource cost AND put card in arsenal
# - Cannot heave if cannot pay resource cost OR cannot put card into arsenal

Feature: Section 8.3.18 - Heave Ability Keyword
    As a game engine
    I need to correctly implement the Heave ability keyword
    So that players can optionally move Heave cards from hand to arsenal at end phase and generate Seismic Surge tokens

    # ===== Rule 8.3.18: Heave is a hidden triggered ability =====

    Scenario: Heave is a hidden triggered ability
        Given a card with "Heave 1" ability
        When I inspect the Heave ability type
        Then the Heave ability is a hidden triggered ability

    # ===== Rule 8.3.18: Heave triggers at the beginning of the end phase =====

    Scenario: Heave triggers at the beginning of the end phase while in hand
        Given a player has a card with "Heave 1" in their hand
        When the beginning of the end phase occurs
        Then the Heave ability triggers for that card

    Scenario: Heave does not trigger if the card is not in hand
        Given a player has a card with "Heave 1" in their banished zone
        When the beginning of the end phase occurs
        Then the Heave ability does not trigger for that card

    # ===== Rule 8.3.18: Heave is optional =====

    Scenario: Heave is optional — player may decline to pay the cost
        Given a player has a card with "Heave 1" in their hand
        And the player has 2 resource points
        And the player's arsenal is empty
        When the Heave ability triggers at the beginning of the end phase
        And the player chooses not to pay the Heave cost
        Then the card remains in the player's hand
        And no Seismic Surge tokens are created

    # ===== Rule 8.3.18: Paying Heave cost puts card face-up in arsenal and creates tokens =====

    Scenario: Paying Heave 1 cost puts card face-up in arsenal and creates 1 Seismic Surge token
        Given a player has a card with "Heave 1" in their hand
        And the player has 1 resource point
        And the player's arsenal is empty
        When the Heave ability triggers at the beginning of the end phase
        And the player pays the Heave cost of 1 resource point
        Then the card is placed face-up in the player's arsenal
        And 1 Seismic Surge token is created
        And the player has 0 resource points remaining

    Scenario: Paying Heave 2 cost puts card face-up in arsenal and creates 2 Seismic Surge tokens
        Given a player has a card with "Heave 2" in their hand
        And the player has 2 resource points
        And the player's arsenal is empty
        When the Heave ability triggers at the beginning of the end phase
        And the player pays the Heave cost of 2 resource points
        Then the card is placed face-up in the player's arsenal
        And 2 Seismic Surge tokens are created
        And the player has 0 resource points remaining

    # ===== Rule 8.3.18a: Player and card are considered to have "heaved" =====

    Scenario: Player is considered to have heaved after paying the cost
        Given a player has a card with "Heave 1" in their hand
        And the player has 1 resource point
        And the player's arsenal is empty
        When the player pays the Heave cost and puts the card face-up into their arsenal
        Then the player is considered to have heaved
        And the card is considered to have been heaved

    Scenario: Player is not considered to have heaved if they decline
        Given a player has a card with "Heave 1" in their hand
        And the player has 1 resource point
        And the player's arsenal is empty
        When the Heave ability triggers at the beginning of the end phase
        And the player chooses not to pay the Heave cost
        Then the player is not considered to have heaved
        And the card is not considered to have been heaved

    # ===== Rule 8.3.18b: Cannot heave if cannot pay resource cost =====

    Scenario: Cannot heave if player cannot pay the resource point cost
        Given a player has a card with "Heave 2" in their hand
        And the player has 1 resource point
        And the player's arsenal is empty
        When the Heave ability triggers at the beginning of the end phase
        Then the player cannot pay the Heave cost
        And no Seismic Surge tokens are created

    # ===== Rule 8.3.18b: Cannot heave if cannot put card into arsenal =====

    Scenario: Cannot heave if the player cannot put the card into their arsenal
        Given a player has a card with "Heave 1" in their hand
        And the player has 1 resource point
        And the player's arsenal is occupied
        When the Heave ability triggers at the beginning of the end phase
        Then the player cannot heave because the arsenal is unavailable
        And no Seismic Surge tokens are created
