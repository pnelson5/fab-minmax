# Feature file for Section 5.1: Playing Cards
# Reference: Flesh and Blood Comprehensive Rules Section 5.1
#
# 5.1.1 To play a card is to move it to the stack as a card-layer. Only a card's
# owner can play it unless otherwise specified. Playing a card involves the following
# steps in order: Announce, Declare Costs, Declare Modes and Targets, Check Legal Play,
# Calculate Asset-Costs, Pay Asset-Costs, Calculate Effect-Costs, Pay Effect-Costs, Play.
#
# 5.1.1a A player can only play cards from their hand or arsenal zones unless otherwise
# specified by a rule or effect.
#
# 5.1.2 Announce: The player proposes the card to be played. The card moves to the stack
# zone under that player's control and becomes the topmost layer.
#
# 5.1.2a Effects that apply to the next card played are applied if the card matches the
# effect description. Effects dependent on undetermined parameters apply when declared.
#
# 5.1.2b A card may only be announced to be played if a rule or existing effect allows it.
#
# 5.1.3 Declare Costs: The player declares the parameters for any costs of the proposed card.
#
# 5.1.3a If the card has a variable cost X, the player must declare the value of X.
# If playing without paying the cost that includes X, declare X as 0.
#
# 5.1.3b If the card has optional additional costs, the player must declare all that will be paid.
#
# 5.1.3c If the card has an alternative cost or effect allowing play without paying cost,
# the player must declare if the alternative cost/effect will be used. Only one can be declared.
#
# 5.1.3d If the card has type action and may be played as an instant, the player declares
# whether or not they are playing the card as an instant.
#
# 5.1.3e If there are two or more effect-costs, the player declares the order they'll be paid.
#
# 5.1.4 Declare Modes and Targets: Third, the player declares the parameters of all resolution abilities.
#
# 5.1.4a If the card has modal resolution abilities, the player declares modes, then targets.
#
# 5.1.4b If the card is an attack, the player must declare the target(s) of the attack.
#
# 5.1.5 Check Legal Play: The card is evaluated if it is legal to play. If a rule or effect
# prevents it, or parameters are illegal, the card is illegal and game state is reversed.
#
# 5.1.6 Calculate Asset-Costs: All asset-costs are calculated.
#
# 5.1.6a First rules define starting asset-cost, then effects that set, then increase,
# then reduce (floor zero). Applied in timestamp order within each step.
#
# 5.1.6b Action asset-cost starts at zero. If card has type action and is NOT played as
# an instant, action cost starts at one instead.
#
# 5.1.6c Resource asset-cost starts at the base resource cost. If an alternative cost is
# declared that replaces the resource asset-cost, the resource asset-cost starts at zero.
#
# 5.1.7 Pay Asset-Costs: The player pays all asset-costs.
#
# 5.1.7a If any asset-cost is not paid in full, the card is illegal to play and the game
# state is reversed to before the card was announced.
#
# 5.1.8 Calculate Effect-Costs: All effect-costs are calculated.
#
# 5.1.8a If any effect-cost cannot be paid (in declared order), the card is illegal to play
# and the game state is reversed.
#
# 5.1.9 Pay Effect-Costs: The player pays all effect-costs.
#
# 5.1.9a If a replacement effect modifies an effect-cost, and that cost cannot be paid,
# the card can still be played.
#
# 5.1.10 Play: Finally, the card is now considered played and the player regains priority.

Feature: Section 5.1 - Playing Cards
    As a game engine
    I need to correctly implement the card playing process
    So that cards are played legally with all costs and steps followed in order

    # Rule 5.1.1 / 5.1.1a: Card zones restriction
    Scenario: A player can play a card from their hand
        Given a player has a card in their hand
        When the player announces the card from their hand
        Then the card should be accepted as a legal announce location

    Scenario: A player can play a card from their arsenal
        Given a player has a card in their arsenal
        When the player announces the card from their arsenal
        Then the card should be accepted as a legal announce location

    Scenario: A player cannot play a card from an invalid zone without special permission
        Given a player has a card in their graveyard
        When the player announces the card from their graveyard
        Then the announce should be rejected as an illegal zone

    # Rule 5.1.1: Only owner can play a card
    Scenario: Only the owner of a card can play it
        Given a card is controlled by one player but owned by another
        When the non-owner attempts to announce the card
        Then the announce should be rejected as played by non-owner

    # Rule 5.1.2: Announce moves card to stack as topmost layer
    Scenario: Announcing a card moves it to the stack as topmost layer
        Given a player has a card in their hand
        And the stack has no layers
        When the player announces the card
        Then the card should be on the stack
        And the card should be the topmost layer of the stack

    Scenario: Announcing a second card makes it the new topmost layer
        Given a player has two cards in their hand
        And the first card has been announced and is on the stack
        When the player announces the second card
        Then the second card should be the topmost layer of the stack

    # Rule 5.1.2a: Effects applying to the next card played activate on announce
    Scenario: A continuous effect applying to the next card played activates on announce
        Given a continuous effect is active that applies to the next attack action card played
        When a player announces an attack action card
        Then the continuous effect should be applied to the announced card

    Scenario: A continuous effect does not apply if the card doesn't match the description
        Given a continuous effect is active that applies to the next attack action card played
        When a player announces a non-attack card
        Then the continuous effect should not be applied to the announced card

    # Rule 5.1.2b: Card may only be announced if allowed
    Scenario: A card may not be announced if no rule or effect allows it to be played
        Given a card has a play restriction that prevents it from being played
        When the player attempts to announce that card
        Then the announce should be rejected

    # Rule 5.1.3a: Variable cost X must be declared; if playing without paying cost, declare X as 0
    Scenario: A player declares the value of X for a card with variable cost
        Given a player has a card with a variable cost including X
        When the player announces the card and declares X as 3
        Then X should be recorded as 3 for the card's cost calculation

    Scenario: A player playing a card without paying its cost containing X must declare X as 0
        Given a player has a card with a variable cost including X
        And an effect allows the player to play the card without paying its cost
        When the player announces the card using the effect
        Then X must be declared as 0

    # Rule 5.1.3b: Optional additional costs must be declared
    Scenario: A player declares optional additional costs before paying
        Given a player has a card with an optional additional cost
        When the player announces the card and declares the optional cost will be paid
        Then the optional additional cost should be recorded as declared

    Scenario: A player may choose not to pay an optional additional cost
        Given a player has a card with an optional additional cost
        When the player announces the card and declares the optional cost will not be paid
        Then the optional additional cost should not be required

    # Rule 5.1.3c: Alternative cost - only one may be declared
    Scenario: A player declares an alternative cost if using one
        Given a player has a card with an alternative cost
        When the player announces the card and declares the alternative cost will be used
        Then the resource asset-cost should start at zero

    Scenario: A player cannot declare two alternative costs simultaneously
        Given a player has a card with two alternative costs
        When the player attempts to declare both alternative costs simultaneously
        Then only one alternative cost declaration should be accepted

    # Rule 5.1.3d: Declare whether playing action as instant
    Scenario: A player declares an action card is being played as an instant
        Given a player has an action card that may be played as an instant
        When the player announces the card and declares it is being played as an instant
        Then the action cost should start at zero

    Scenario: An action card not declared as instant incurs action cost
        Given a player has an action card that may be played as an instant
        When the player announces the card without declaring instant play
        Then the action cost should start at one

    # Rule 5.1.3e: Declare order of two or more effect-costs
    Scenario: A player declares the order of multiple effect-costs
        Given a player has a card with two effect-costs
        When the player announces the card and declares the order of effect-costs
        Then the declared order should be recorded for effect-cost payment

    # Rule 5.1.4b: Attack must declare target
    Scenario: An attack card requires a target declaration
        Given a player has an attack action card
        When the player announces the attack card
        Then the player must declare an attack target

    # Rule 5.1.5: Check Legal Play - reverses game state if illegal
    Scenario: The game state is reversed if a card is determined to be illegal after announce
        Given a player has a card in their hand
        And a rule prevents the card from being played
        When the player attempts to announce the card
        Then the card should remain in the player's hand
        And the stack should be empty

    Scenario: An illegal play due to illegal target parameters reverses game state
        Given a player has a card that requires a valid target
        And there are no valid targets available
        When the player announces the card
        Then the game state is reversed to before the announce

    # Rule 5.1.6a: Asset-cost calculation order
    Scenario: Asset-costs are calculated with set effects applied before increase effects
        Given a card has a base resource cost of 3
        And an effect sets the resource cost to 2
        And an effect increases the resource cost by 1
        When asset-costs are calculated
        Then the final resource cost should be 3

    Scenario: Asset-cost reduction cannot reduce below zero
        Given a card has a base resource cost of 1
        And an effect reduces the resource cost by 3
        When asset-costs are calculated
        Then the final resource cost should be 0

    # Rule 5.1.6b: Action asset-cost starts at 0 for instants, 1 for non-instants
    Scenario: Action asset-cost is zero when playing as instant
        Given a player has an action card that may be played as an instant
        And the player declares they are playing it as an instant
        When the action asset-cost is calculated
        Then the action asset-cost should be 0

    Scenario: Action asset-cost is one when playing as a non-instant action
        Given a player has an action card
        And the player declares they are NOT playing it as an instant
        When the action asset-cost is calculated
        Then the action asset-cost should be 1

    # Rule 5.1.6c: Alternative cost sets resource cost to zero
    Scenario: Declaring an alternative cost sets the resource asset-cost to zero
        Given a player has a card with a base resource cost of 3
        And the player declares an alternative cost that replaces the resource asset-cost
        When the resource asset-cost is calculated
        Then the resource asset-cost should start at zero

    # Rule 5.1.7a: Failure to pay asset-cost reverses game state
    Scenario: If an asset-cost is not paid in full the card cannot be played
        Given a player has a card with a resource cost of 3
        And the player only has 1 resource available
        When the player attempts to pay the asset-costs
        Then the card play should fail
        And the game state should be reversed to before the announce

    # Rule 5.1.8a: Effect-cost cannot be paid reverses game state
    Scenario: If an effect-cost cannot be paid in declared order the play is reversed
        Given a player has a card with an effect-cost that cannot be paid
        When the player attempts to calculate effect-costs
        Then the card play should fail
        And the game state should be reversed to before the announce

    # Rule 5.1.9a: Replacement effect on effect-cost - card can still be played
    Scenario: If a replacement effect modifies an effect-cost and it cannot be paid the card can still be played
        Given a player has a card with an effect-cost
        And a replacement effect modifies the effect-cost
        And the modified effect-cost cannot be paid
        When the player pays effect-costs
        Then the card play should still succeed

    # Rule 5.1.10: After Play step, card is considered played and priority regained
    Scenario: After successfully playing a card the player regains priority
        Given a player has a card in their hand
        When the player successfully completes all steps to play the card
        Then the card should be considered played
        And the player should regain priority
