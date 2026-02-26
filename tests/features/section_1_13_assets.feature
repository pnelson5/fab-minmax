# Feature file for Section 1.13: Assets
# Reference: Flesh and Blood Comprehensive Rules Section 1.13
#
# Rule 1.13.1: An asset is a point of a given type, owned by a player.
#              There are four types of assets: action points, resource points,
#              life points, and chi points.
#
# Rule 1.13.2: An action point is an asset that is typically used to play an
#              action card and/or activate an action ability.
# Rule 1.13.2a: A player can gain action points during their action phase from:
#              at the start of their action phase, the ability go again, and
#              effects that grant the player action points.
# Rule 1.13.2b: A player cannot gain action points if it is not their action
#              phase. If a player would gain an action point but it is not their
#              action phase, instead they do not gain any action points.
#
# Rule 1.13.3: A resource point is an asset that is typically used to play
#              cards and activate abilities.
# Rule 1.13.3a: A player can gain resource points from: pitching cards during
#              the payment of an asset-cost that requires resource points, and
#              effects that grant the player resource points.
#
# Rule 1.13.4: A life point is an asset that is paid from a player's hero's
#              life total and is typically used to activate abilities.
# Rule 1.13.4a: A player can gain life points from effects that increase the
#              player's hero's life total.
#
# Rule 1.13.5: A chi point is an asset that is typically used to play cards
#              and activate abilities.
# Rule 1.13.5a: A player can gain chi points from: pitching cards during the
#              payment of an asset-cost that requires chi or resource points.
# Rule 1.13.5b: A chi point can be used in place of a resource point for
#              paying resource point costs.

Feature: Section 1.13 - Assets
    As a game engine
    I need to correctly implement the four types of assets (action, resource, life, chi)
    So that players can gain and spend assets to play cards and activate abilities

    # ===== Rule 1.13.1: Four Types of Assets =====

    Scenario: There are exactly four types of assets
        Given a player exists in the game
        When I query the available asset types
        Then there are exactly 4 asset types
        And one of the asset types is "action_point"
        And one of the asset types is "resource_point"
        And one of the asset types is "life_point"
        And one of the asset types is "chi_point"

    Scenario: An asset is owned by a player
        Given a player exists in the game
        And the player has been given 2 action points
        When the engine queries player ownership of those action points
        Then the player owns those action points
        And the action points belong to that specific player

    # ===== Rule 1.13.2: Action Points =====

    Scenario: Action points are used to play action cards
        Given a player has 1 action point
        When the player spends 1 action point to play an action card
        Then the player has 0 action points
        And the action card play was permitted

    Scenario: Player gains 1 action point at start of action phase
        Given a player starts their action phase
        When the action phase begins
        Then the player gains 1 action point
        And the player has 1 action point available

    Scenario: Go again grants player 1 additional action point
        Given a player is in their action phase with 1 action point
        And the player's attack has the go again keyword
        When the go again effect triggers
        Then the player gains 1 action point
        And the player has 2 action points total

    Scenario: Effect grants action points during action phase
        Given a player is in their action phase with 1 action point
        When an effect grants the player 1 additional action point
        Then the player has 2 action points total

    # ===== Rule 1.13.2b: Cannot Gain Action Points Outside Action Phase =====

    Scenario: Non-turn player cannot gain action points from go again
        Given player 0 is in their action phase
        And player 1 is NOT in their action phase
        When player 1 plays an instant with the go again ability
        Then player 1 does not gain any action points from go again
        And player 1 has 0 action points

    Scenario: Non-turn player cannot gain action points from effects outside action phase
        Given player 0 is in their action phase
        And player 1 is NOT in their action phase
        When an effect would grant player 1 an action point
        Then player 1 does not gain any action points
        And player 1 has 0 action points

    Scenario: Lead the Charge non-turn player gets no action points
        Given player 0 is in their action phase
        And player 1 is NOT in their action phase
        And player 1 has played Lead the Charge as an instant with delayed trigger
        When player 1 plays a cost 0 action card as an instant
        Then player 1 does not gain an action point from the delayed trigger
        And player 1 has 0 action points

    # ===== Rule 1.13.3: Resource Points =====

    Scenario: Resource points are used to pay card costs
        Given a player has 3 resource points
        When the player spends 3 resource points to pay for a card with cost 3
        Then the player has 0 resource points
        And the card cost was paid successfully

    Scenario: Player gains resource points by pitching a card
        Given a player has 0 resource points in hand with a 2-pitch card
        When the player pitches the 2-pitch card during cost payment
        Then the player gains 2 resource points
        And the pitched card moves to the pitch zone

    Scenario: Effect grants resource points directly
        Given a player has 0 resource points
        When an effect grants the player 2 resource points
        Then the player has 2 resource points

    # ===== Rule 1.13.4: Life Points =====

    Scenario: Life points come from the hero life total
        Given a player's hero has 20 life
        When the engine checks the player's life point assets
        Then the player has life points equal to the hero's life total
        And the life point asset is tracked on the hero

    Scenario: Life points can be used to activate abilities
        Given a player's hero has 20 life
        And there is an ability with cost "pay 2 life"
        When the player activates the ability and pays 2 life points
        Then the hero's life total is reduced to 18
        And the ability activation was permitted

    Scenario: Player gains life points when hero life total increases
        Given a player's hero has 15 life out of a maximum of 20
        When an effect increases the hero's life total by 3
        Then the player has gained 3 life points
        And the hero's life total is 18

    # ===== Rule 1.13.5: Chi Points =====

    Scenario: Chi points are used to play cards and activate abilities
        Given a player has 2 chi points
        When the player spends 2 chi points to pay for a chi cost
        Then the player has 0 chi points
        And the chi cost was paid successfully

    Scenario: Player gains chi points by pitching a chi card
        Given a player has 0 chi points and holds a 1-chi-pitch card
        When the player pitches the chi card during cost payment
        Then the player gains 1 chi point
        And the chi points are available to spend

    # ===== Rule 1.13.5b: Chi Points Can Replace Resource Points =====

    Scenario: Chi point substitutes for resource point in cost payment
        Given a player has 0 resource points and 2 chi points
        When the player pays a resource cost of 2 using chi points
        Then the payment succeeds with chi points replacing resource points
        And the player used 2 chi points to pay the resource cost

    Scenario: Chi points are used before resource points in payment
        Given a player has 1 resource point and 2 chi points
        When the player pays a cost of 2 resource points
        Then the player uses the 2 chi points first
        And the player still has 1 resource point remaining

    Scenario: Chi points cannot substitute for non-resource costs
        Given a player has 2 chi points
        When the player needs to pay a life point cost of 2
        Then the player cannot use chi points to pay the life cost
        And the payment fails unless the player has 2 life points

    # ===== Rule 1.13.3 + 1.13.5a: Gaining Assets from Pitching =====

    Scenario: Pitching a resource card gains resource points
        Given a player holds a card with pitch value 3 of type resource
        When the player pitches the card to pay a resource cost
        Then the player gains 3 resource points from the pitch

    Scenario: Pitching a chi card gains chi points
        Given a player holds a card with pitch value 2 of type chi
        When the player pitches the card to pay a chi or resource cost
        Then the player gains 2 chi points from the pitch

    Scenario: Cannot pitch card during payment if it gains the wrong asset type
        Given a player has 0 chi points and needs to pay 2 chi points
        And the player holds a card that only generates resource points when pitched
        When the player tries to pitch the resource-generating card to pay the chi cost
        Then the pitch is rejected
        And the player gains no assets from the failed pitch attempt
