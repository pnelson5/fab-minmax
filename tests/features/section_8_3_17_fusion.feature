# Feature file for Section 8.3.17: Fusion (Ability Keyword)
# Reference: Flesh and Blood Comprehensive Rules Section 8.3.17
#
# 8.3.17 Fusion
#   Fusion is an optional additional-cost play-static ability. Fusion is written
#   as "[SUPERTYPES] Fusion" which means "As an additional cost to play this,
#   you may reveal (a/an) [SUPERTYPES] card(s) from your hand," where SUPERTYPES
#   is a list of one or more supertypes. [2.11]
#
# 8.3.17a If a player pays the additional cost to play a card with fusion, the
#   player is considered to have fused those supertypes and the played card is
#   considered to have been fused.
#
# 8.3.17b A player cannot fuse if they cannot pay the additional cost of
#   revealing the card(s) with the specified supertypes from their hand.
#
# 8.3.17c A player may only reveal up to one card for each of the supertypes
#   listed. A single card may be revealed for one or more different supertypes.
#
# 8.3.17d If the list specifies "and," the player must reveal cards with all of
#   the supertypes in the list. If the list specifies "and/or," the player must
#   reveal cards with at least one of the supertypes on the list.
#
# Key aspects:
# - Fusion is a PLAY-STATIC ability (applies while playing the card)
# - Fusion is OPTIONAL — the player chooses whether to pay the additional cost
# - Fusion is an ADDITIONAL COST — must be declared and paid when playing the card
# - Paying fusion makes the played card "fused" and the player "fused those supertypes"
# - Cannot fuse if cannot reveal the required supertypes from hand
# - "and" requires ALL listed supertypes; "and/or" requires AT LEAST ONE
# - One card per supertype; but one card can satisfy multiple supertypes

Feature: Section 8.3.17 - Fusion Ability Keyword
    As a game engine
    I need to correctly implement the Fusion ability keyword
    So that players can optionally reveal cards from their hand as an additional cost when playing Fusion cards

    # ===== Rule 8.3.17: Fusion is an optional additional-cost play-static ability =====

    Scenario: Fusion is a play-static ability
        Given a card has the "Draconic Ninja Fusion" keyword
        When I inspect the Fusion ability on the card
        Then the Fusion ability is a play-static ability
        And the Fusion ability is optional

    # ===== Rule 8.3.17: Fusion keyword format =====

    Scenario: Fusion ability meaning is correctly formatted with the specified supertypes
        Given a card has the "Draconic Ninja Fusion" keyword
        When I inspect the Fusion ability on the card
        Then the Fusion ability means "As an additional cost to play this, you may reveal a Draconic Ninja card from your hand"

    # ===== Rule 8.3.17a: Paying fusion cost makes card and player "fused" =====

    Scenario: Paying the fusion cost makes the played card considered fused
        Given a player has a card with "Draconic Fusion" in their hand
        And the player has a Draconic card in their hand
        When the player plays the fusion card and reveals the Draconic card as the fusion cost
        Then the played card is considered to have been fused
        And the player is considered to have fused Draconic

    # ===== Rule 8.3.17a: Playing fusion card without paying cost is not fused =====

    Scenario: Playing a fusion card without paying the fusion cost does not make it fused
        Given a player has a card with "Draconic Fusion" in their hand
        And the player has a Draconic card in their hand
        When the player plays the fusion card without paying the fusion cost
        Then the played card is not considered to have been fused
        And the player is not considered to have fused Draconic

    # ===== Rule 8.3.17b: Cannot fuse without the required supertype cards in hand =====

    Scenario: Player cannot fuse if they have no cards with the required supertype in hand
        Given a player has a card with "Draconic Fusion" in their hand
        And the player has no Draconic cards in their hand
        When the player attempts to pay the fusion cost
        Then the player cannot fuse because no Draconic card is available in hand

    # ===== Rule 8.3.17c: At most one card revealed per listed supertype =====

    Scenario: Player may only reveal one card per supertype listed in fusion
        Given a player has a card with "Draconic Fusion" in their hand
        And the player has two Draconic cards in their hand
        When the player attempts to reveal both Draconic cards for the fusion cost
        Then the player may only reveal one card for the Draconic fusion cost

    # ===== Rule 8.3.17c: A single card can satisfy multiple supertypes =====

    Scenario: A single card with multiple supertypes can satisfy multiple fusion requirements
        Given a player has a card with "Draconic Ninja Fusion" in their hand
        And the player has a card with both Draconic and Ninja supertypes in their hand
        When the player pays the fusion cost by revealing that card for both supertypes
        Then the played card is considered to have been fused
        And the player only needed to reveal one card to satisfy both fusion requirements

    # ===== Rule 8.3.17d: "and" fusion requires ALL listed supertypes =====

    Scenario: Draconic and Ninja fusion requires revealing cards with both supertypes
        Given a player has a card with "Draconic and Ninja Fusion" in their hand
        And the player has a Draconic card in their hand
        And the player has a Ninja card in their hand
        When the player pays the fusion cost by revealing one Draconic and one Ninja card
        Then the played card is considered to have been fused
        And the player is considered to have fused Draconic and Ninja

    Scenario: Draconic and Ninja fusion cannot be paid with only one supertype revealed
        Given a player has a card with "Draconic and Ninja Fusion" in their hand
        And the player has a Draconic card in their hand
        And the player has no Ninja cards in their hand
        When the player attempts to pay the fusion cost
        Then the player cannot fuse because not all required supertypes are available in hand

    # ===== Rule 8.3.17d: "and/or" fusion requires AT LEAST ONE listed supertype =====

    Scenario: Draconic and/or Ninja fusion can be paid with only a Draconic card
        Given a player has a card with "Draconic and/or Ninja Fusion" in their hand
        And the player has a Draconic card in their hand
        And the player has no Ninja cards in their hand
        When the player pays the fusion cost by revealing the Draconic card
        Then the played card is considered to have been fused
        And the player is considered to have fused Draconic

    Scenario: Draconic and/or Ninja fusion can be paid with only a Ninja card
        Given a player has a card with "Draconic and/or Ninja Fusion" in their hand
        And the player has a Ninja card in their hand
        And the player has no Draconic cards in their hand
        When the player pays the fusion cost by revealing the Ninja card
        Then the played card is considered to have been fused
        And the player is considered to have fused Ninja
