# Feature file for Section 8.3.19: Quell (Ability Keyword)
# Reference: Flesh and Blood Comprehensive Rules Section 8.3.19
#
# Rule 8.3.19: Quell is a static ability. Quell is written as "Quell N" which
# means "If you would be dealt damage, you may pay N{r} to prevent N of that
# damage. If you do, destroy this at the beginning of the end phase."

Feature: Section 8.3.19 - Quell Ability Keyword
    As a game engine
    I need to correctly implement the Quell ability keyword
    So that players can optionally pay resources to prevent damage at the cost of destroying the card

    # Rule 8.3.19: Quell is a static ability

    Scenario: Quell is a static ability
        Given a card with "Quell 1" ability
        When I inspect the Quell ability type
        Then the Quell ability is a static ability

    # Rule 8.3.19: Quell N means prevention of N damage by paying N resources

    Scenario: Quell ability has the correct N value
        Given a card with "Quell 2" ability
        When I inspect the Quell ability type
        Then the Quell ability has N equal to 2

    # Rule 8.3.19: Paying Quell prevents N damage

    Scenario: Paying Quell 1 cost prevents 1 damage
        Given a player has an equipment with "Quell 1" ability equipped
        And the player has 1 resource point
        When the player would be dealt 3 damage
        And the player pays the Quell cost of 1 resource point
        Then 1 damage is prevented
        And the player takes 2 damage instead

    Scenario: Paying Quell 2 cost prevents 2 damage
        Given a player has an equipment with "Quell 2" ability equipped
        And the player has 2 resource points
        When the player would be dealt 5 damage
        And the player pays the Quell cost of 2 resource points
        Then 2 damage is prevented
        And the player takes 3 damage instead

    # Rule 8.3.19: Paying Quell is optional

    Scenario: Player may choose not to pay Quell cost
        Given a player has an equipment with "Quell 1" ability equipped
        And the player has 1 resource point
        When the player would be dealt 3 damage
        And the player declines to pay the Quell cost
        Then no damage is prevented by Quell
        And the player takes the full 3 damage

    # Rule 8.3.19: Destroy this at the beginning of the end phase after paying

    Scenario: Card is destroyed at beginning of end phase after paying Quell cost
        Given a player has an equipment with "Quell 1" ability equipped
        And the player has 1 resource point
        When the player would be dealt 3 damage
        And the player pays the Quell cost of 1 resource point
        And the beginning of the end phase occurs
        Then the Quell card is destroyed

    Scenario: Card is not destroyed if Quell cost was not paid
        Given a player has an equipment with "Quell 1" ability equipped
        And the player has 1 resource point
        When the player would be dealt 3 damage
        And the player declines to pay the Quell cost
        And the beginning of the end phase occurs
        Then the Quell card is not destroyed by Quell

    # Rule 8.3.19: Cannot pay more than N prevention per activation

    Scenario: Quell only prevents exactly N damage, not more
        Given a player has an equipment with "Quell 1" ability equipped
        And the player has 3 resource points
        When the player would be dealt 5 damage
        And the player pays the Quell cost of 1 resource point
        Then exactly 1 damage is prevented
        And the player takes 4 damage instead

    # Rule 8.3.19: Cannot pay Quell if insufficient resources

    Scenario: Cannot pay Quell cost with insufficient resources
        Given a player has an equipment with "Quell 2" ability equipped
        And the player has 1 resource point
        When the player would be dealt 3 damage
        Then the player cannot pay the Quell cost
