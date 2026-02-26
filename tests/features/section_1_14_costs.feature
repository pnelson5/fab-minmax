# Feature file for Section 1.14: Costs
# Reference: Flesh and Blood Comprehensive Rules Section 1.14
#
# Rule 1.14.1: A cost is the requirement of payment from a player incurred by
#              playing a card, activating an ability, or resolving/applying an
#              effect. A cost requires the payment of assets (asset-costs) and/or
#              the successful resolution of effects (effect-costs).
#
# Rule 1.14.2: An asset-cost is a cost that requires the payment of one or more
#              assets. To pay an asset-cost as a player, the player must have or
#              gain assets of the appropriate type equal to, or greater than, the
#              cost to be paid; then those asset-cost amounts are subtracted from
#              the player's assets and the cost is considered paid.
#
# Rule 1.14.2a: If an asset-cost involves paying two or more types of assets,
#              they must be paid in the following order: chi points, resource
#              points, life points, action points. Each type of asset must be
#              paid in full before starting to pay for the next type.
#
# Rule 1.14.2b: If a player does not have enough assets and does not gain any
#              additional assets to pay an asset-cost, the cost cannot be paid
#              and the game state is reversed to before the cost is paid. If
#              the asset-cost is mandatory and part of another action, the
#              entire action is reversed.
#
# Rule 1.14.2c: To pay a chi point cost, the player must use chi points. If
#              they have fewer chi points than required, the player may pitch
#              cards one at a time until they have enough chi points to pay.
#
# Rule 1.14.2d: To pay a resource point cost, the player must use resource
#              points and chi points. The player must use all of their chi
#              points before using any of their resource points to pay a
#              resource point cost.
#
# Rule 1.14.2e: To pay a life point cost, the player must use life points.
#
# Rule 1.14.2f: To pay an action point cost, the player must use action points.
#
# Rule 1.14.3: To pitch a card as a player, the player moves the card from their
#              hand to the pitch zone and gains assets. The pitch property of a
#              card determines what type and how many assets a player gains when
#              the card is pitched.
#
# Rule 1.14.3a: A card cannot be pitched if it does not have the pitch property.
#
# Rule 1.14.3b: A player may only pitch a card if that card will gain them
#              assets they need to pay an asset-cost or if they are instructed
#              by an effect.
#
# Rule 1.14.3c: Pitching a card is an event that can trigger and be replaced
#              by effects.
#
# Rule 1.14.4: An effect-cost is a cost that requires payment in the form of
#              generating one or more effects. To pay an effect-cost, the player
#              must be able to successfully generate and resolve the specified
#              costs.
#
# Rule 1.14.4a: If an effect-cost involves generating two or more effects, the
#              player declares the order in which the effects will be generated.
#
# Rule 1.14.4b: Before the effect-cost is paid, if any of the effects cannot be
#              generated due to a rule or effect, or the effects cannot resolve
#              successfully based on the current game state, the cost cannot be
#              paid and the game state is reversed to before the cost is paid.
#              If the effect-cost is mandatory and part of another action, the
#              entire action is reversed.
#
# Rule 1.14.4c: During the payment of an effect-cost, if the events of any
#              effects are replaced and cannot be successfully resolved, the
#              cost is still considered paid.
#
# Rule 1.14.5: A cost that is represented by "0," or a cost in which all
#              asset-costs are reduced to zero and there are no effect-costs,
#              is still considered a cost which is paid by acknowledging the
#              zero cost.

Feature: Section 1.14 - Costs
    As a game engine
    I need to correctly implement costs (asset-costs and effect-costs)
    So that players can pay the proper price for playing cards and activating abilities

    # ===== Rule 1.14.1: Costs are requirements of payment =====

    Scenario: A cost is incurred by playing a card
        Given a player has a card with cost 2
        And the player has 2 resource points
        When the player plays the card
        Then the card play incurs a cost
        And the cost requires payment of 2 resource points

    Scenario: A cost is incurred by activating an ability
        Given a player has a card with an activated ability costing 1 resource point
        And the player has 1 resource point
        When the player activates the ability
        Then activating the ability incurs a cost
        And the cost requires payment of 1 resource point

    Scenario: A cost can require both asset-costs and effect-costs
        Given a player has a card with cost 1 and a discard effect-cost
        And the player has 1 resource point and 1 card in hand
        When checking the full cost of the card
        Then the cost has an asset-cost component
        And the cost has an effect-cost component

    # ===== Rule 1.14.2: Asset-costs require paying assets =====

    Scenario: Player pays asset-cost with exact assets
        Given a player has an action card with cost 3
        And the player has 3 resource points
        When the player pays the asset-cost
        Then the cost is paid successfully
        And the player has 0 resource points remaining

    Scenario: Player pays asset-cost with more than enough assets
        Given a player has an action card with cost 2
        And the player has 4 resource points
        When the player pays the asset-cost
        Then the cost is paid successfully
        And the player has 2 resource points remaining

    Scenario: Player cannot pay asset-cost with insufficient assets
        Given a player has an action card with cost 3
        And the player has 1 resource point
        When the player attempts to pay the asset-cost
        Then the cost cannot be paid
        And the game state is reversed to before payment

    # ===== Rule 1.14.2a: Multi-asset payment order =====

    Scenario: Multi-asset cost paid in correct order chi then resource then life then action
        Given a player has an ability with cost 1 chi and 1 resource and 1 life and 1 action
        And the player has 1 chi point, 1 resource point, 3 life points, and 1 action point
        When the player pays the multi-asset cost
        Then chi points are paid first
        And resource points are paid second
        And life points are paid third
        And action points are paid last

    Scenario: Each asset type must be paid in full before the next
        Given a player has an ability with cost 2 chi and 2 resource points
        And the player has 1 chi point and 3 resource points
        When the player attempts to pay 2 chi then 2 resource
        Then the chi cost payment fails because chi points are insufficient
        And payment of resource points does not begin

    # ===== Rule 1.14.2b: Insufficient assets reverses game state =====

    Scenario: Mandatory asset-cost failure reverses entire action
        Given a player has an action card with mandatory cost 3
        And the player has only 1 resource point
        When the player attempts to play the card
        Then the cost cannot be paid
        And the entire card play action is reversed
        And the card is returned to its starting zone

    Scenario: Pitching during payment can provide needed assets
        Given a player has an action card with cost 3
        And the player has 1 resource point
        And the player has a 2-pitch card in hand
        When the player pitches the 2-pitch card during cost payment
        Then the player gains 2 resource points from pitching
        And the player now has 3 resource points total
        And the cost is paid successfully

    # ===== Rule 1.14.2c: Paying chi point costs =====

    Scenario: Paying chi cost uses chi points
        Given a player has an ability with a cost of 2 chi points
        And the player has 3 chi points
        When the player pays the chi point cost
        Then the chi points are spent
        And the player has 1 chi point remaining

    Scenario: Player pitches chi card to gain chi for chi cost
        Given a player has an ability with a cost of 2 chi points
        And the player has 0 chi points
        And the player has a chi-pitch card in hand with chi pitch value 2
        When the player pitches the chi card to pay the chi cost
        Then the player gains 2 chi points from pitching
        And the chi cost is paid successfully

    # ===== Rule 1.14.2d: Paying resource point costs =====

    Scenario: Paying resource cost uses chi points first then resource points
        Given a player has an action card with cost 2
        And the player has 1 chi point and 2 resource points
        When the player pays the resource cost
        Then chi points are used before resource points
        And 1 chi point is spent
        And 1 resource point is spent

    Scenario: Player pitches resource card to gain resources for resource cost
        Given a player has an action card with cost 3
        And the player has 1 resource point
        And the player has a 2-pitch card in hand
        When the player pitches the 2-pitch card during resource cost payment
        Then the player gains 2 resource points from the pitch
        And the resource cost is paid with available resources

    Scenario: Pitching stops when resource cost is fully paid
        Given a player has an action card with cost 2
        And the player has 1 resource point
        And the player has a 3-pitch resource card in hand
        When the player pitches the 3-pitch card to pay the 2 resource cost
        Then the cost is paid
        And the player has 1 resource point left over from pitching
        And the player cannot pitch more cards to pay this cost

    # ===== Rule 1.14.2e: Paying life point costs =====

    Scenario: Paying life cost uses life points
        Given a player has an ability with a cost of 2 life points
        And the player hero has 20 life points
        When the player pays the life point cost
        Then the life points are spent
        And the player hero has 18 life points remaining

    Scenario: Life cost cannot be paid with chi points
        Given a player has an ability with a cost of 1 life point
        And the player has 3 chi points and 1 life point
        When the player attempts to pay 1 life using chi points
        Then the payment fails because chi cannot pay life costs
        And the game state is not changed

    # ===== Rule 1.14.2f: Paying action point costs =====

    Scenario: Paying action cost uses action points
        Given a player has an ability with a cost of 1 action point
        And the player has 1 action point
        When the player pays the action point cost
        Then the action point is spent
        And the player has 0 action points remaining

    # ===== Rule 1.14.3: Pitching cards =====

    Scenario: Pitching a card moves it from hand to pitch zone and grants assets
        Given a player has a 2-pitch card in hand
        When the player pitches the card during cost payment
        Then the card moves from hand to the pitch zone
        And the player gains 2 resource points from pitching

    Scenario: Pitch property determines type and amount of assets gained
        Given a player has a 3-chi-pitch card in hand
        When the player pitches the card during cost payment
        Then the player gains 3 chi points from pitching
        And the pitch zone contains the card

    # ===== Rule 1.14.3a: Only cards with pitch property can be pitched =====

    Scenario: Card without pitch property cannot be pitched
        Given a player has a card with no pitch property in hand
        When the player attempts to pitch that card
        Then the pitch attempt fails
        And the card remains in hand

    Scenario: Card with pitch property can be pitched
        Given a player has a card with pitch value 1 in hand
        When the player pitches that card during cost payment
        Then the pitch succeeds
        And the card moves to the pitch zone

    # ===== Rule 1.14.3b: Pitch only if card gains needed asset type =====

    Scenario: Player can only pitch card if it gains needed asset type
        Given a player is paying a chi point cost of 2
        And the player has a resource-pitch card in hand
        When the player attempts to pitch the resource card for chi cost
        Then the pitch attempt is rejected
        And the reason is that the card only gains resource points not chi points

    Scenario: Player can pitch card if it gains the needed asset type
        Given a player is paying a chi point cost of 2
        And the player has a chi-pitch card in hand with chi pitch value 2
        When the player pitches the chi card for chi cost
        Then the pitch is accepted
        And the player gains chi points for the chi cost

    Scenario: Player can pitch card if instructed by an effect
        Given a player has a card in hand with no pitch property
        And there is an effect instructing the player to pitch a card
        When the player pitches the card as instructed by the effect
        Then the pitch is accepted despite no normal pitch property
        And the card moves to the pitch zone

    # ===== Rule 1.14.3c: Pitching is an event =====

    Scenario: Pitching a card triggers effects that watch for pitching
        Given a player has a 2-pitch card in hand
        And there is an effect that triggers when a card is pitched
        When the player pitches the card during cost payment
        Then the pitch event occurs
        And the triggered effect fires in response to the pitch

    Scenario: Pitching a card can be replaced by replacement effects
        Given a player has a 2-pitch card in hand
        And there is a replacement effect that modifies the pitch event
        When the player pitches the card during cost payment
        Then the replacement effect modifies the pitch event
        And the modified pitch occurs instead of the normal pitch

    # ===== Rule 1.14.4: Effect-costs require generating effects =====

    Scenario: Effect-cost requires successfully generating and resolving an effect
        Given a player has an ability with the effect-cost of destroying a card
        And the player has a card that can be destroyed
        When the player pays the effect-cost
        Then the destroy effect is generated
        And the target card is destroyed as the cost

    Scenario: Hope Merchants Hood effect-cost example
        Given a player controls Hope Merchants Hood
        And the player has 3 cards in hand
        When the player activates the ability to destroy Hope Merchants Hood
        Then destroying Hope Merchants Hood is an effect-cost
        And the cards are shuffled back into the deck

    # ===== Rule 1.14.4a: Multi-effect-cost ordering =====

    Scenario: Player declares order for multi-effect-cost
        Given a player has an ability with two effect-costs discard and deal damage
        And the player has a card in hand and a valid target
        When the player pays the multi-effect-cost
        Then the player declares the order of the effects
        And the effects are generated in the declared order

    # ===== Rule 1.14.4b: Unpayable effect-costs reverse game state =====

    Scenario: Effect-cost that cannot be generated reverses game state
        Given a player has an ability with an effect-cost of destroying their weapon
        And the player has no weapon in play
        When the player attempts to pay the effect-cost
        Then the effect-cost cannot be paid
        And the game state is reversed to before activation

    Scenario: Mandatory effect-cost failure reverses entire action
        Given a player has a card with a mandatory effect-cost of discarding a card
        And the player has no cards in hand to discard
        When the player attempts to play the card
        Then the effect-cost cannot be resolved
        And the entire card play action is reversed

    # ===== Rule 1.14.4c: Replaced effect-costs still count as paid =====

    Scenario: Effect-cost replaced but considered paid
        Given a player has an ability with an effect-cost of discarding a card
        And there is a replacement effect that replaces the discard with banishment
        When the player pays the effect-cost
        Then the replacement effect replaces the discard event
        And the cost is still considered paid despite the replacement

    # ===== Rule 1.14.5: Zero cost is still a cost =====

    Scenario: Card with cost zero still has a cost to pay
        Given a player has a card with cost 0
        When the player plays the card
        Then the cost of 0 is acknowledged as paid
        And the card play proceeds normally

    Scenario: Asset-costs reduced to zero still require acknowledgment
        Given a player has a card with cost 3
        And an effect reduces the cost by 3
        When the player plays the card with reduced cost
        Then the cost has been reduced to 0
        And the zero cost is acknowledged as paid
        And the card play proceeds normally

    Scenario: Zero cost with no effect-costs is still a cost
        Given a player has a card with cost 0 and no effect-costs
        When the player plays the card
        Then the zero cost is a valid cost
        And the cost is paid by acknowledging it
