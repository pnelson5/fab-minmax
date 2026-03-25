# Feature file for Section 8.3.9: Boost (Ability Keyword)
# Reference: Flesh and Blood Comprehensive Rules Section 8.3.9
#
# 8.3.9 Boost
#   Boost is an optional additional-cost play-static ability that means
#   "As an additional cost to play this, you may banish the top card of your deck.
#   If you do, if it's a Mechanologist card, this gets go again."
#
# 8.3.9a If a player pays the additional cost to play a card with boost, the player
#   is considered to have boosted and the played card is considered to have been
#   boosted, even if the banished card is not a Mechanologist card.
#
# 8.3.9b A player cannot boost if they cannot pay the additional cost of banishing
#   the top card of their deck.
#
# Key aspects:
# - Boost is an OPTIONAL additional-cost PLAY-STATIC ability (not triggered, not meta-static)
# - Paying the boost cost means banishing the top card of the player's deck
# - If the banished card is a Mechanologist card, the played card gets go again
# - If the banished card is NOT a Mechanologist card, the played card does NOT get go again
# - The player and card are still considered to have "boosted" regardless of the banished card type
# - If the deck is empty, the player cannot boost (cannot banish the top card)
# - Boost is optional — the player may choose not to pay the additional cost

Feature: Section 8.3.9 - Boost Ability Keyword
    As a game engine
    I need to correctly implement the Boost ability keyword
    So that Mechanologist cards can gain go again when boosted with a Mechanologist card

    # ===== Rule 8.3.9: Boost is an optional additional-cost play-static ability =====

    Scenario: Boost is an optional additional-cost play-static ability
        Given a card has the "Boost" keyword
        When I inspect the Boost ability on the card
        Then the Boost ability is a play-static ability
        And the Boost ability is an optional additional-cost ability
        And the Boost ability is not a triggered ability
        And the Boost ability is not a meta-static ability

    # ===== Rule 8.3.9: Boost meaning is correct =====

    Scenario: Boost meaning is as specified in the rules
        Given a card has the "Boost" keyword
        When I inspect the Boost ability on the card
        Then the Boost ability means "As an additional cost to play this, you may banish the top card of your deck. If you do, if it's a Mechanologist card, this gets go again."

    # ===== Rule 8.3.9: Boosting with a Mechanologist card grants go again =====

    Scenario: Boosting with a Mechanologist card grants go again
        Given a player has a card with the "Boost" keyword in hand
        And the top card of the player's deck is a Mechanologist card
        When the player plays the card and chooses to boost
        Then the top card is banished from the player's deck
        And the played card gets go again
        And the player is considered to have boosted
        And the played card is considered to have been boosted

    # ===== Rule 8.3.9: Boosting with a non-Mechanologist card does not grant go again =====

    Scenario: Boosting with a non-Mechanologist card does not grant go again
        Given a player has a card with the "Boost" keyword in hand
        And the top card of the player's deck is not a Mechanologist card
        When the player plays the card and chooses to boost
        Then the top card is banished from the player's deck
        And the played card does not get go again
        And the player is considered to have boosted
        And the played card is considered to have been boosted

    # ===== Rule 8.3.9a: Boost status applies regardless of banished card type =====

    Scenario: Player is still considered to have boosted even if banished card is not Mechanologist
        Given a player has a card with the "Boost" keyword in hand
        And the top card of the player's deck is not a Mechanologist card
        When the player plays the card and chooses to boost
        Then the player is considered to have boosted
        And the played card is considered to have been boosted

    # ===== Rule 8.3.9b: Cannot boost with empty deck =====

    Scenario: Player cannot boost if their deck is empty
        Given a player has a card with the "Boost" keyword in hand
        And the player's deck is empty
        When the player attempts to boost while playing the card
        Then the player cannot boost
        And the boost additional cost cannot be paid

    # ===== Rule 8.3.9: Boost is optional — player may choose not to boost =====

    Scenario: Player may choose not to boost
        Given a player has a card with the "Boost" keyword in hand
        And the top card of the player's deck is a Mechanologist card
        When the player plays the card without choosing to boost
        Then no card is banished from the deck
        And the played card does not get go again from boost
        And the player is not considered to have boosted
