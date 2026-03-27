# Feature file for Section 8.3.38: Meld (Ability Keyword)
# Reference: Flesh and Blood Comprehensive Rules Section 8.3.38
#
# 8.3.38 Meld
#   Meld is a static ability that means "You may pay twice the base cost of
#   this to play both halves of this."
#
# 8.3.38a If a player chooses to pay the alternative cost to play a card with
#   meld, the player is considered to have melded and the card is melded. The
#   card remains melded until it ceases to exist.
#
# 8.3.38b Meld sets the asset-cost of a card before increases and decreases
#   are applied. (See 5.1.6)
#
# 8.3.38c A melded card has the properties of both of its sides on a
#   split-card [9.2]: both names, and the combination of its abilities,
#   supertypes, types, and subtypes. If a melded card is not a split-card,
#   it is unaffected by meld.
#
# Cross-references:
# 5.1.2c: When playing a split-card with meld, the player may declare both
#   sides. The declared side(s) determines the card's properties on the stack.
# 5.3.4d: Melded card resolution order — right-side abilities first (turn-player
#   gains priority), then left-side abilities on second resolution.
#
# Key aspects:
# - Meld is a STATIC ability
# - Alternative cost is TWICE the base cost
# - Playing both halves is optional (player MAY pay the alternative cost)
# - A card is only "melded" when the player pays the double cost
# - Meld sets the asset-cost before increases/decreases are applied
# - Melded card has combined properties of both split-card sides
# - A non-split-card with meld is unaffected by meld
# - Resolution order: right-side first, left-side second

Feature: Section 8.3.38 - Meld Ability Keyword
    As a game engine
    I need to correctly implement the Meld ability keyword
    So that split-cards can be played with both halves at double the base cost

    # ===== Rule 8.3.38: Meld is a static ability =====

    Scenario: Meld is a static ability
        Given a card has the "Meld" keyword
        When I inspect the Meld ability on the card
        Then the Meld ability is a static ability
        And the Meld ability is not a triggered ability
        And the Meld ability is not an activated ability

    # ===== Rule 8.3.38: Meld meaning is correct =====

    Scenario: Meld means pay twice the base cost to play both halves
        Given a card has the "Meld" keyword
        When I inspect the Meld ability on the card
        Then the Meld ability means "You may pay twice the base cost of this to play both halves of this"

    # ===== Rule 8.3.38: Playing with meld is optional =====

    Scenario: Player may choose not to pay the Meld alternative cost
        Given a split-card with Meld has a base cost of 2
        When a player chooses to play the split-card without Meld
        Then the player pays the normal base cost of 2
        And the card is not melded

    # ===== Rule 8.3.38a: Paying double cost results in a melded card =====

    Scenario: Paying double cost marks the card as melded
        Given a split-card with Meld has a base cost of 2
        When a player chooses to pay the Meld alternative cost of 4
        Then the player is considered to have melded
        And the card is melded

    # ===== Rule 8.3.38a: Card remains melded until it ceases to exist =====

    Scenario: Melded card remains melded until it ceases to exist
        Given a split-card has been melded
        When the melded card is still on the stack
        Then the card is melded
        And the card remains melded until it ceases to exist

    # ===== Rule 8.3.38b: Meld sets asset-cost before increases/decreases =====

    Scenario: Meld sets the asset-cost before cost modifications are applied
        Given a split-card with Meld has a base cost of 3
        And there is a cost reduction effect of 1
        When a player chooses to pay the Meld alternative cost
        Then the Meld cost is set to 6 before cost modifications
        And the final cost to play with Meld is 5 after the cost reduction

    # ===== Rule 8.3.38c: Melded card has combined properties of both sides =====

    Scenario: Melded split-card has both names
        Given a split-card "Null||Shock" has been melded
        When I inspect the melded card's name
        Then the melded card has the name "Null"
        And the melded card has the name "Shock"

    Scenario: Melded split-card has combined types and subtypes
        Given a melded split-card with left-side type "Action" and right-side type "Instant"
        When I inspect the melded card's types
        Then the melded card has type "Action"
        And the melded card has type "Instant"

    # ===== Rule 8.3.38c: Non-split-card is unaffected by Meld =====

    Scenario: Non-split-card with Meld keyword is unaffected by Meld
        Given a non-split-card has the "Meld" keyword
        When a player attempts to play the card
        Then the card is unaffected by Meld
        And the card cannot be melded

    # ===== Rule 5.3.4d: Melded card resolution order =====

    Scenario: Melded card resolves right-side abilities first
        Given a split-card has been melded and placed on the stack
        When the melded card resolves for the first time
        Then only the right-side resolution abilities generate their effects
        And the turn-player gains priority after first resolution

    Scenario: Melded card resolves left-side abilities on second resolution
        Given a split-card has been melded and first resolution has occurred
        When the melded card resolves for the second time
        Then only the left-side resolution abilities generate their effects
