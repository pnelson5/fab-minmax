# Feature file for Section 5.4: Static Abilities
# Reference: Flesh and Blood Comprehensive Rules Section 5.4
#
# 5.4.1 A static ability is an ability that generates effects without resolving
# a layer on the stack. Static abilities are written as statements.
#
# 5.4.2 Static abilities that are functional generate static continuous effects.
# [6.2.3]
#
# 5.4.3 A meta-static ability is a static ability that generates effects that
# apply to the rules outside of the game.
#
# 5.4.3a If a meta-static ability that modifies rules outside the game ceases
# to exist during a game, it does not affect the legality of the rules followed
# outside the game.
# Example: Shiyana, Diamond Gemini has "You may have specialization cards of
# any hero in your deck." If the player has specialization cards in their
# card-pool and Shiyana lost this ability during a game, having those cards
# remains legal.
#
# 5.4.4 A play-static ability is a static ability that generates effects that
# apply to the playing of its source card.
#
# 5.4.4a An additional-cost ability is a play-static ability that adds one or
# more asset-costs and/or effect-costs to play the source card. Typically:
# "As an additional cost to play this [COST]." Optional if COST uses "may";
# must be declared when playing a card.
#
# 5.4.4b An alternative-cost ability is a play-static ability that replaces
# one or more asset-costs and/or effect-costs to play the source card. Typically:
# "You may [COST] rather than pay this's [BASE]." Optional and must be declared
# when playing a card. An alternative cost has no effect on any additional costs.
#
# 5.4.4c If a play-static ability generates a triggered effect that references
# the playing of its source, the effect triggers immediately if the trigger
# condition is met.
#
# 5.4.4d If a play-static ability generates a conditional continuous effect that
# references the playing of its source, the effect is generated at the time the
# condition is met.
#
# 5.4.5 A property-static ability is a static ability that defines the property,
# or value of a property, on an object that would normally be found elsewhere.
# Example: Mutated Mass has "This card's power and defense are equal to twice
# the number of cards in your pitch zone with different costs."
#
# 5.4.5a Property-static abilities function anywhere in and outside the game.
#
# 5.4.6 A triggered-static ability is a static ability that generates a single
# triggered effect. [5.5]
#
# 5.4.6a If the source of a triggered-static ability ceases to exist from an
# event that would trigger its effect, and the ability was functional immediately
# before the event occurs, then the triggered effect is triggered.
# Example: Merciful Retribution: "Whenever an aura or attack action card you
# control is destroyed, deal 1 arcane damage to target hero." If Merciful
# Retribution itself is destroyed, its triggered effect still triggers.
#
# 5.4.7 A while-static ability is a static ability with a condition that makes
# it functional under specified circumstances. Written in format:
# "While [CONDITION], [ABILITY]"
# Example: Yinti Yanti "While this is defending and you control an aura,
# it gets +1{d}."
#
# 5.4.7a A while-static ability is functional when its while-condition is met
# and when its source is public, when its source is private if the while-condition
# explicitly specifies it, or when the while-condition specifies it functions
# in that private zone. Otherwise, a while-static ability is not functional.
# Example: Heave (while in hand) - functional even when source is private.
# Example: Blood Debt (while in banished zone) - NOT functional when source is
# private in that zone, because it doesn't explicitly specify privacy.
#
# 5.4.7b A hidden triggered ability is both a while-static and triggered-static
# ability, where the while-condition specifies the source is private or in a
# private zone. If the triggered condition is met while functional and the source
# is private, the owner MAY decide to trigger the effect. If they do, the source
# becomes public and a triggered-layer is added to the stack. The source remains
# public until the triggered-layer resolves, then returns to private.
# Example: The Librarian "While face down in arsenal, at the start of your turn,
# you may turn him face up."

Feature: Section 5.4 - Static Abilities
    As a game engine
    I need to correctly implement static abilities
    So that cards generate continuous effects without placing layers on the stack

    # ===== 5.4.1: Basic static ability definition =====

    Scenario: Static ability generates effects without resolving a layer
        Given a card with a static ability that grants a bonus effect
        When the card is in play
        Then the static ability is functional without any layer on the stack
        And the effect is generated immediately without stack resolution

    # ===== 5.4.2: Functional static abilities generate static continuous effects =====

    Scenario: Functional static ability generates a static continuous effect
        Given a card with a functional static ability in the arena
        When I check the type of effect generated by the static ability
        Then the effect is a static continuous effect
        And the effect persists as long as the static ability is functional

    Scenario: Static continuous effect ends when static ability becomes non-functional
        Given a card with a static ability in the arena
        And the static ability is currently functional and generating an effect
        When the card leaves the arena
        Then the static continuous effect ends
        And the bonus from the static ability is no longer applied

    # ===== 5.4.3: Meta-static ability =====

    Scenario: Meta-static ability applies rules outside the game
        Given a hero with a meta-static ability that modifies deck building rules
        When evaluating the card-pool for legality outside the game
        Then the meta-static ability modifies the outside-game rules
        And cards that would normally be illegal become legal due to the meta-static ability

    Scenario: Meta-static ability ceasing during game does not affect card-pool legality
        Given a hero with a meta-static ability allowing specialization cards of any hero
        And the player has specialization cards in their card-pool based on that ability
        When the meta-static ability ceases to exist during the game
        Then the specialization cards in the card-pool remain legal
        And the legality of previously followed outside-game rules is not affected

    # ===== 5.4.4a: Additional-cost ability =====

    Scenario: Additional-cost ability requires extra cost to play card
        Given a card with an additional-cost play-static ability requiring discard
        And a player with the card in hand
        When the player attempts to play the card without paying the additional cost
        Then the play attempt fails
        And the additional cost must be declared when playing the card

    Scenario: Additional-cost ability is mandatory when not using the word may
        Given a card with a mandatory additional-cost ability requiring resource payment
        And a player with the card in hand
        When the player attempts to play the card
        Then the additional cost is required and cannot be skipped

    Scenario: Optional additional-cost ability can be skipped when using the word may
        Given a card with an optional additional-cost ability using "may"
        And a player with the card in hand
        When the player plays the card without paying the optional additional cost
        Then the play succeeds without the optional cost

    # ===== 5.4.4b: Alternative-cost ability =====

    Scenario: Alternative-cost ability allows paying different cost instead of base cost
        Given a card with a base cost of 3 resources
        And the card has an alternative-cost ability to discard a card instead
        And a player with the card in hand and insufficient resources
        When the player chooses to pay the alternative cost
        Then the card is played without paying the base resource cost

    Scenario: Alternative cost does not affect additional costs
        Given a card with both an alternative-cost ability and an additional-cost ability
        And a player who chooses to pay the alternative cost
        When the player plays the card using the alternative cost
        Then the additional cost still applies
        And must also be paid alongside the alternative cost

    Scenario: Alternative-cost ability must be declared when playing the card
        Given a card with an alternative-cost ability
        And a player with the card in hand
        When the player begins to play the card
        Then the alternative cost must be declared at that time if they wish to use it

    # ===== 5.4.4c: Triggered play-static ability =====

    Scenario: Play-static triggered effect triggers immediately when condition is met
        Given a card with a play-static ability in the format "EFFECT. When you do, ABILITIES"
        And a player who has met the condition of that play-static ability
        When the player plays the card using the effect specified in the ability
        Then the triggered effect triggers immediately
        And a triggered layer is placed on the stack

    # ===== 5.4.4d: Conditional continuous play-static ability =====

    Scenario: Conditional continuous effect from play-static ability generated when condition met
        Given a card with a play-static ability in the format "EFFECT. If you do, CONTINUOUSEFFECT"
        And a player who has met the replacement condition of the play-static ability
        When the player plays the card using the specified effect
        Then the conditional continuous effect is generated at the time the condition is met

    # ===== 5.4.5: Property-static ability =====

    Scenario: Property-static ability defines a dynamic card property
        Given a card with a property-static ability defining its power based on game state
        And the game state has 3 cards of different costs in the pitch zone
        When I check the card's power value
        Then the power is calculated dynamically by the property-static ability
        And the value matches what the static ability formula specifies

    Scenario: Property-static ability updates when game state changes
        Given a card with a property-static ability defining power as twice the pitch zone count
        And the pitch zone has 2 cards
        When a third card is added to the pitch zone
        Then the card's power updates to reflect the new game state

    # ===== 5.4.5a: Property-static abilities function anywhere =====

    Scenario: Property-static ability is functional anywhere in the game
        Given a card with a property-static ability
        When the card is in the hand zone
        Then the property-static ability is functional
        And the defined property value is applied

    Scenario: Property-static ability is functional outside the game
        Given a card with a property-static ability
        When evaluating the card outside of a game context
        Then the property-static ability is still functional
        And the property it defines is recognized

    # ===== 5.4.6: Triggered-static ability =====

    Scenario: Triggered-static ability generates a single triggered effect
        Given a card in the arena with a triggered-static ability
        And the trigger condition of the triggered-static ability is met
        When the triggered effect is generated
        Then exactly one triggered layer is created from the triggered-static ability
        And the triggered layer is placed on the stack

    # ===== 5.4.6a: Source ceases to exist from triggering event =====

    Scenario: Triggered-static ability triggers even when source is destroyed by the triggering event
        Given a card with a triggered-static ability whose trigger condition is its own destruction
        And the card is in the arena and its triggered-static ability is functional
        When the card is destroyed
        Then the triggered effect still triggers
        And a triggered layer is placed on the stack for the effect

    Scenario: Triggered-static ability does not trigger if not functional before the event
        Given a card with a triggered-static ability that is currently not functional
        When the trigger event occurs
        Then the triggered effect does not trigger
        And no triggered layer is placed on the stack

    # ===== 5.4.7: While-static ability =====

    Scenario: While-static ability is functional when its condition is met
        Given a card with a while-static ability requiring it to be defending
        And an aura controlled by the same player
        When the card becomes a defending card
        Then the while-static ability becomes functional
        And the effect from the while-static ability applies

    Scenario: While-static ability is not functional when condition is not met
        Given a card with a while-static ability requiring it to be defending
        When the card is not defending
        Then the while-static ability is not functional
        And the effect from the while-static ability does not apply

    # ===== 5.4.7a: Functional based on public/private status =====

    Scenario: While-static ability for public zone is functional when source is public
        Given a card with a while-static ability for a condition in a public zone
        And the source card is public
        When the while-condition is met
        Then the while-static ability is functional

    Scenario: While-static ability explicitly specifying hand is functional when source is private
        Given a card with a while-static ability that explicitly specifies "while this is in your hand"
        And the card is face-down in the player's hand
        When the while-condition is met
        Then the while-static ability is functional even though the source is private

    Scenario: While-static ability for public zone is not functional when source is private
        Given a card with a while-static ability referencing a normally-public zone like banished
        And the card is private in the banished zone
        When the while-condition would otherwise be met
        Then the while-static ability is not functional because the source is private
        And the ability does not generate its effect

    # ===== 5.4.7b: Hidden triggered ability =====

    Scenario: Hidden triggered ability owner may choose to trigger when source is private
        Given a card with a hidden triggered ability
        And the card is face-down in arsenal
        When the trigger condition of the hidden triggered ability is met
        Then the owner may decide to trigger the effect
        And if the owner triggers it, the source becomes public

    Scenario: Hidden triggered ability source becomes public when triggered
        Given a card with a hidden triggered ability face-down in arsenal
        When the owner decides to trigger the hidden triggered ability
        Then the card becomes public immediately
        And a triggered layer is placed on the stack

    Scenario: Hidden triggered ability source returns to private after triggered layer resolves
        Given a card with a hidden triggered ability
        And the owner triggered the hidden triggered ability making the source public
        When the triggered layer resolves
        Then the source returns to being private
        And the card is no longer public
