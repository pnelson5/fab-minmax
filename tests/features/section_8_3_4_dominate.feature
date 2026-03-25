# Feature file for Section 8.3.4: Dominate (Ability Keyword)
# Reference: Flesh and Blood Comprehensive Rules Section 8.3.4
#
# 8.3.4 Dominate
#   Dominate is a static ability that means "This can't be defended by more
#   than one card from hand."
#
# 8.3.4a If an attack with dominate is currently defended by a card from hand,
#   an additional card cannot be added as a defending card to the attack's chain
#   link if the card comes from a player's hand. [refs: 5.3.2c, 8.5.32]
#
# 8.3.4b If an attack with dominate is currently defended by a card from hand
#   on the activate chain link, defense reaction cards cannot be played from
#   hand. [ref: 7.4.2c]
#
# 8.3.4c If an attack is defended by two or more cards from hand and then the
#   attack gains dominate, no cards are retroactively removed from defending.
#
# Key aspects:
# - Dominate is a static ability (not triggered, not activated)
# - Restriction applies only to cards "from hand" — one such card is the max
# - Defense reactions played from hand are also blocked (rule 8.3.4b)
# - Dominate gained after defending does NOT remove existing hand defenders (8.3.4c)

Feature: Section 8.3.4 - Dominate Ability Keyword
    As a game engine
    I need to correctly implement the Dominate ability keyword
    So that attacks with Dominate can only be defended by at most one card from hand

    # ===== Rule 8.3.4: Dominate is a static ability =====

    Scenario: Dominate is a static ability
        Given a card with the "Dominate" keyword ability
        When I inspect the Dominate ability on the card
        Then the Dominate ability is a static ability

    Scenario: Dominate ability has the correct meaning
        Given a card with the "Dominate" keyword ability
        When I inspect the Dominate ability on the card
        Then the Dominate ability means "This can't be defended by more than one card from hand"

    # ===== Rule 8.3.4a: Second hand card cannot be added as defender =====

    Scenario: A second hand card cannot be added to defend a Dominate attack
        Given an attack with the "Dominate" keyword
        And the attack is already defended by one card from the defending player's hand
        When the defending player attempts to add a second card from hand as a defender
        Then the defend attempt is rejected
        And the attack still has exactly one defending card from hand

    Scenario: A first hand card can defend a Dominate attack normally
        Given an attack with the "Dominate" keyword
        And the attack has no defending cards yet
        When the defending player attempts to defend with one card from hand
        Then the defend attempt succeeds
        And the attack has one defending card from hand

    Scenario: Non-hand defender can be added even when Dominate attack has a hand defender
        Given an attack with the "Dominate" keyword
        And the attack is already defended by one card from the defending player's hand
        When the defending player attempts to add a card that does not come from hand as a defender
        Then the defend attempt succeeds

    # ===== Rule 8.3.4b: Defense reactions from hand are blocked =====

    Scenario: Defense reaction from hand cannot be played when Dominate attack has a hand defender
        Given an attack with the "Dominate" keyword on the activate chain link
        And the attack is already defended by one card from the defending player's hand
        When the defending player attempts to play a defense reaction from hand
        Then the defense reaction play is rejected

    Scenario: Defense reaction can be played when Dominate attack has no hand defender yet
        Given an attack with the "Dominate" keyword on the activate chain link
        And the attack has no defending cards yet
        When the defending player attempts to play a defense reaction from hand
        Then the defense reaction play succeeds

    # ===== Rule 8.3.4c: Gaining Dominate does not retroactively remove defenders =====

    Scenario: Gaining Dominate does not remove existing hand defenders
        Given an attack that does not have the "Dominate" keyword
        And the attack is already defended by two cards from the defending player's hand
        When the attack gains the "Dominate" keyword
        Then both defending cards remain as defenders
        And no cards are retroactively removed from defending

    Scenario: Gaining Dominate prevents additional hand defenders after being gained
        Given an attack that does not have the "Dominate" keyword
        And the attack is already defended by two cards from the defending player's hand
        When the attack gains the "Dominate" keyword
        And the defending player attempts to add another card from hand as a defender
        Then the additional defend attempt is rejected
