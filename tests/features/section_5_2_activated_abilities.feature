# Feature file for Section 5.2: Activated Abilities
# Reference: Flesh and Blood Comprehensive Rules Section 5.2
#
# 5.2.1 An activated ability is an ability that can be activated to put an
# activated-layer on the stack. Activated abilities are always written in the
# format "[LIMIT?] [TYPE] -- [COST]: [ABILITIES] [CONDITION?]."
#
# 5.2.1a The LIMIT (if any) is written at the start of the ability and specifies
# the maximum number of times the ability can be activated. If there is no limit,
# the ability can be activated any number of times.
#
# 5.2.1b The TYPE is written directly before the dash and specifies the type of
# the ability and the type of the activated-layer created by activating the ability.
#
# 5.2.1c The COST is written between the dash and colon. It specifies the cost to
# be paid to activate the ability. A cost of "0" specifies the resource cost to
# activate the ability is zero.
#
# 5.2.1d The ABILITIES are written after the colon and specify the base abilities
# of the activated-layer. When the activated-layer resolves, the resolution
# abilities of the layer generate effects.
#
# 5.2.1e The CONDITION (if any) is written at the end of the ability and specifies
# the activation condition. If the activated ability has an activation condition
# and that condition is not met, the ability cannot be activated.
#
# 5.2.2 To activate an activated ability is to create an activated-layer on the
# stack. A player can only activate an activated ability if they have priority,
# the ability is functional, and the player controls its source (or owns its
# source if there is no controller), unless otherwise specified by a rule or effect.
#
# 5.2.2a Announce the activated ability to be activated. The activated-layer is
# created in the stack zone under that player's control and becomes the topmost
# layer of the stack. The activated-layer is created with the same supertypes
# and types as the source of the activated ability. Continuous effects begin to
# apply to the ability layer.
#
# 5.2.2b The remainder of the process for activating an activated ability is
# identical to the process for playing a card listed in steps 5.1.3-5.1.10
# substituting "play" for "activate", and "card" for "ability."
#
# 5.2.3 If an effect allows an ability to be activated additional times, that
# activated ability may be activated to exceed its LIMIT by the specified amount.
#
# 5.2.3a If an effect allows all abilities on an object to be activated additional
# times and the object has two or more activated abilities, each activated ability
# of that object can be activated additional times.
#
# 5.2.3b If an effect allows an object to be activated additional times and the
# object has two or more activated abilities, the effect applies at the time the
# ability is activated beyond its LIMIT. The total number of additional activations
# may be spread across all activated abilities on the object.
#
# 5.2.3c If an effect allows a source to attack additional times, it refers to
# activating an ability on the source with the attack ability (8.3.1) or attack
# effect (8.5.38).
#
# 5.2.3d Effects that allow the additional activation of an activated ability are
# additive. If two or more effects would allow an activated ability to be activated
# beyond its LIMIT, the player chooses which of those effects apply to the activation.
#
# 5.2.3e Effects that state how many times an ability can be activated in total,
# set the LIMIT of the activated ability (or the total number of times that all
# activated abilities), which can be surpassed by effects that allow the ability
# to be activated additional times.
#
# 5.2.4 If an activated ability's cost can only be paid when the source is private,
# or if its activation condition specifies the privacy status and/or zone of its
# source, the ability is functional when the source meets that requirement.
#
# 5.2.4a If an activated ability is functional, but its source has no controller,
# then the owner may activate the ability instead.
#
# 5.2.4b If a player activates an ability of a private source, the source of the
# ability becomes public until either the activated-layer resolves or ceases to
# exist, or the source ceases to exist. When an object becomes public this way,
# it does not trigger any abilities and cannot be replaced by any replacement effects.

Feature: Section 5.2 - Activated Abilities
    As a game engine
    I need to correctly implement activated ability rules
    So that players can activate abilities within their limits and with correct behavior

    # Test for Rule 5.2.1 - Activated ability format components

    Scenario: Activated ability without LIMIT can be activated any number of times
        Given a card with an activated ability with no limit
        And the player controls the card and has priority
        When the player activates the ability three times
        Then all three activations should be allowed
        And three activated-layers should exist on the stack

    Scenario: Activated ability with LIMIT can be activated up to the limit
        Given a card with an activated ability with a limit of 1
        And the player controls the card and has priority
        When the player activates the ability once
        Then the activation should succeed
        And the activated-layer is created on the stack

    Scenario: Activated ability cannot be activated beyond its LIMIT
        Given a card with an activated ability with a limit of 1
        And the player controls the card and has priority
        And the ability has already been activated once
        When the player tries to activate the ability again
        Then the second activation should be denied
        And the ability is at its LIMIT

    Scenario: Activated ability with condition cannot be activated if condition not met
        Given a card with an activated ability that requires a condition
        And the activation condition is not met
        When the player tries to activate the ability
        Then the activation should be denied
        And the reason is the activation condition is not met

    Scenario: Activated ability with condition can be activated when condition is met
        Given a card with an activated ability that requires a condition
        And the activation condition is met
        When the player activates the ability
        Then the activation should succeed

    # Test for Rule 5.2.2 - Activation prerequisites

    Scenario: A player must control the source to activate an activated ability
        Given a card with an activated ability in the arena
        And the card is controlled by player 2
        When player 1 tries to activate the ability
        Then the activation should be denied
        And the reason is the player does not control the source

    Scenario: A player without priority cannot activate an activated ability
        Given a card with an activated ability controlled by the player
        And the player does not have priority
        When the player tries to activate the ability
        Then the activation should be denied
        And the reason is the player does not have priority

    Scenario: An activated ability must be functional to be activated
        Given a card with an activated ability that is not functional
        And the player controls the card
        When the player tries to activate the ability
        Then the activation should be denied
        And the reason is the ability is not functional

    # Test for Rule 5.2.2a - Activated-layer creation

    Scenario: Activating an ability creates an activated-layer on the stack
        Given a card with an activated ability controlled by the player
        And the player has priority
        When the player activates the ability
        Then an activated-layer is created on the stack
        And the activated-layer is controlled by the activating player
        And the activated-layer is the topmost layer on the stack

    Scenario: Activated-layer inherits supertypes and types from its source
        Given a card with an activated ability controlled by the player
        And the source card has type "action" and supertype "legendary"
        When the player activates the ability
        Then the activated-layer has type "action"
        And the activated-layer has supertype "legendary"

    # Test for Rule 5.2.3 - Additional activations exceeding LIMIT

    Scenario: An effect allowing additional activations lets an ability exceed its LIMIT
        Given a card with an activated ability with a limit of 1
        And the player controls the card and has priority
        And an effect allows the ability to be activated 1 additional time
        And the ability has already been activated once reaching its LIMIT
        When the player activates the ability again
        Then the activation should succeed
        And the ability was activated beyond its normal LIMIT

    Scenario: An effect allowing all object abilities additional times applies per-ability
        Given a weapon with two activated abilities each with a limit of 1
        And the player controls the weapon
        And an effect allows all abilities on the weapon to be activated an additional time
        When the player activates each ability once more beyond their individual limits
        Then each ability was allowed one additional activation
        And each ability was activated twice in total

    Scenario: An effect allowing an object additional times can be spread across its abilities
        Given a weapon with two activated abilities each with a limit of 1
        And the player controls the weapon
        And an effect allows the weapon to be activated 2 additional times total
        When the player uses both additional activations on the first ability
        Then the first ability was activated a total of 3 times
        And the second ability was still limited to 1 activation

    Scenario: Multiple additional activation effects are additive
        Given a card with an activated ability with a limit of 1
        And the player controls the card
        And an effect allows the ability to be activated 1 additional time
        And another effect also allows the ability to be activated 1 additional time
        When the ability has been activated once and the player activates it again
        Then the player can choose which additional activation effect to apply
        And the ability can be activated at least once more after that

    Scenario: An effect setting total activations sets the LIMIT
        Given a card with an activated ability
        And an effect sets the total number of times the ability can be activated to 2
        And the ability has no prior limit
        When the player activates the ability twice
        Then both activations should succeed
        When the player tries to activate the ability a third time
        Then the third activation should be denied

    # Test for Rule 5.2.3c - "Attack additional times" means activating attack ability

    Scenario: Attacking additional times refers to activating the attack ability again
        Given a weapon with an attack activated ability with a limit of 1
        And the player controls the weapon
        And an effect allows the weapon to attack an additional time
        When the player activates the attack ability a second time
        Then the additional attack activation should succeed
        And the weapon's attack ability was activated beyond its normal LIMIT

    # Test for Rule 5.2.4 - Functional abilities with private/zone conditions

    Scenario: Activated ability requiring private source is functional when source is private
        Given a card in a player's hand with an activated ability requiring private source
        And the card is private in the player's hand
        When checking if the ability is functional
        Then the ability should be functional
        And the player may activate the ability

    Scenario: Activated ability requiring private source is not functional when source is public
        Given a card with an activated ability requiring private source
        And the card is public
        When checking if the ability is functional
        Then the ability should not be functional

    # Test for Rule 5.2.4a - Owner may activate when source has no controller

    Scenario: Owner may activate ability when source has no controller
        Given a card with an activated ability in a zone with no controller
        And the ability is functional
        When the owner of the card activates the ability
        Then the activation should succeed
        And the owner is treated as the activating player

    # Test for Rule 5.2.4b - Private source becomes public on activation

    Scenario: Activating ability of private source makes source public
        Given a card in a player's hand with an activated ability
        And the card is private
        When the player activates the ability
        Then the source card becomes public
        And the source remains public until the activated-layer resolves or ceases to exist

    Scenario: Source becoming public via activation does not trigger abilities
        Given a card in a player's hand with an activated ability
        And the card is private
        And there is an effect that triggers when a card becomes public
        When the player activates the ability making the source public
        Then the source card becomes public
        But the triggered effect should not trigger from the source becoming public

    Scenario: Source becoming public via activation cannot be replaced
        Given a card in a player's hand with an activated ability
        And the card is private
        And there is a replacement effect that would apply when the card becomes public
        When the player activates the ability making the source public
        Then the source card becomes public
        But the replacement effect should not apply to the card becoming public
