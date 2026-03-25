# Feature file for Section 8.3.20: Ward (Ability Keyword)
# Reference: Flesh and Blood Comprehensive Rules Section 8.3.20
#
# Rule 8.3.20: Ward is a static ability. Ward is written as "Ward N" which
# means "If you would be dealt damage, destroy this to prevent N of that damage."

Feature: Section 8.3.20 - Ward Ability Keyword
    As a game engine
    I need to correctly implement the Ward ability keyword
    So that players can destroy a card bearing Ward to prevent N damage

    # Rule 8.3.20: Ward is a static ability

    Scenario: Ward is a static ability
        Given a card with "Ward 1" ability
        When I inspect the Ward ability type
        Then the Ward ability is a static ability

    # Rule 8.3.20: Ward N stores the correct N value

    Scenario: Ward ability has the correct N value
        Given a card with "Ward 3" ability
        When I inspect the Ward ability type
        Then the Ward ability has N equal to 3

    # Rule 8.3.20: Destroying the Ward card prevents N damage

    Scenario: Destroying a Ward 1 card prevents 1 damage
        Given a player has an equipment with "Ward 1" ability equipped
        When the player would be dealt 4 damage
        And the player destroys the Ward card to prevent damage
        Then 1 damage is prevented by Ward
        And the player takes 3 damage instead

    Scenario: Destroying a Ward 2 card prevents 2 damage
        Given a player has an equipment with "Ward 2" ability equipped
        When the player would be dealt 5 damage
        And the player destroys the Ward card to prevent damage
        Then 2 damage are prevented by Ward
        And the player takes 3 damage instead

    # Rule 8.3.20: Ward prevents exactly N damage, not more

    Scenario: Ward only prevents exactly N damage, not more
        Given a player has an equipment with "Ward 1" ability equipped
        When the player would be dealt 10 damage
        And the player destroys the Ward card to prevent damage
        Then exactly 1 damage is prevented by Ward
        And the player takes 9 damage instead

    # Rule 8.3.20: Destroying is the cost (card is destroyed immediately)

    Scenario: Ward card is destroyed immediately when used
        Given a player has an equipment with "Ward 1" ability equipped
        When the player would be dealt 4 damage
        And the player destroys the Ward card to prevent damage
        Then the Ward card is immediately destroyed

    # Rule 8.3.20: Player may choose not to use Ward (optional)

    Scenario: Player may choose not to use Ward
        Given a player has an equipment with "Ward 1" ability equipped
        When the player would be dealt 4 damage
        And the player does not use Ward
        Then no damage is prevented by Ward
        And the Ward card is not destroyed

    # Rule 8.3.20: Ward does not require paying resources (unlike Quell)

    Scenario: Ward requires no resource payment, only destruction of the card
        Given a player has an equipment with "Ward 2" ability equipped
        And the player has 0 resource points
        When the player would be dealt 3 damage
        And the player destroys the Ward card to prevent damage
        Then 2 damage are prevented by Ward
        And the player takes 1 damage instead

    # Rule 8.3.20: Ward N meaning is correctly formed

    Scenario: Ward ability has the correct meaning text
        Given a card with "Ward 2" ability
        When I inspect the Ward ability type
        Then the Ward ability meaning includes preventing 2 damage by destroying the card
