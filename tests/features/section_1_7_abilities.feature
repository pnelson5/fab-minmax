# Feature file for Section 1.7: Abilities
# Reference: Flesh and Blood Comprehensive Rules Section 1.7
#
# Rule 1.7.1: An ability is a property of an object that influences the game by
#   generating effects or by creating a layer on the stack that resolves and generates
#   effects. The base abilities of a non-token card are determined by its rules text.
#   The base abilities of a token card, macro, or non-card layer are defined by a rule,
#   or the effect or ability that created it.
#
# Rule 1.7.1a: The source of an ability is the card or token that has that ability.
#   The source of an ability of an activated-layer or triggered-layer is the same as
#   the source of the ability that created that layer. Activated-layers and triggered-layers
#   exist independently of their source - if the source of an activated-layer or
#   triggered-layer ceases to exist, it does not prevent the resolution of that layer.
#
# Rule 1.7.1b: The controller of an activated-layer is the player who activated its source.
#   The controller of a triggered-layer is the player who controlled its source when it
#   triggered - if the source has no controller, the controller of the triggered-layer is
#   the player who owns the source.
#
# Rule 1.7.2: If an object has an ability as a property, it is considered a card with that
#   ability. If the ability is a base ability, it is considered a card with that base ability.
#   Example: Torrent of Tempo has "When this hits, it gets go again." - it is not a card with
#   base go again. Until it hits, it is not considered a card with go again.
#
# Rule 1.7.3: There are three categories of abilities: activated abilities, resolution abilities,
#   and static abilities. An ability is categorized based on how it generates effects.
# Rule 1.7.3a: Activated abilities can be activated by a player to put an activated-layer on the stack.
# Rule 1.7.3b: Resolution abilities generate effects when a layer with the ability resolves on the stack.
# Rule 1.7.3c: Static abilities simply generate effects.
#
# Rule 1.7.4: An activated ability can only be activated when it is functional. A resolution or
#   static ability only generates its effects when it is functional. An ability is functional when
#   its source is public and in the arena; otherwise, it is non-functional, with exceptions.
#
# Rule 1.7.4a: An ability of a non-permanent defending card is non-functional unless the ability
#   is an activated ability that specifies it can be activated when the card is defending, a triggered
#   ability with a trigger condition that includes the card defending, or a static ability stated as exception.
#   Example: Rally the Rearguard "Activate this only while this is defending" - functional when defending.
#
# Rule 1.7.4b: An activated ability is functional if its cost can only be paid, or it explicitly
#   specifies it can be activated, when the source is private or outside the arena.
#   Example: Mighty Windup "Instant -- Discard this: Create a Might token" - functional in hand.
#   Example: Guardian of the Shadowrealm - functional in banished zone.
#
# Rule 1.7.4c: A resolution ability is functional when its source object resolves as a layer on the stack.
#   Example: Sigil of Solace "Gain 3{h}" - functional as the card resolves on the stack.
#
# Rule 1.7.4d: A meta-static ability is functional outside the game.
#   Example: Specialization keyword - functional outside the game for deck building.
#
# Rule 1.7.4e: A play-static ability is functional when its source is public in any zone and when played.
#   Example: Ghostly Visit "You may play this from your banished zone" - functional when playing.
#
# Rule 1.7.4f: A property-static ability is functional when its source is in any zone or outside the game.
#   Example: Mutated Mass - {p} and {d} defined by property-static ability always.
#
# Rule 1.7.4g: A while-static ability is functional when its while-condition is met.
#   Example: Yinti Yanti "While this is defending and you control an aura, this gets +1{d}".
#
# Rule 1.7.4h: A static ability is functional when its source resolves as a layer on the stack
#   and/or as its source enters the arena.
#
# Rule 1.7.4i: A triggered-static ability with triggered condition that source is outside the arena
#   is functional when the source meets that condition.
#   Example: Back Alley Breakline "When an activated ability or action card effect puts this
#   face-up into a zone from your deck, gain 1 action point".
#
# Rule 1.7.4j: A static ability with a replacement effect that modifies zone-movement is functional
#   when the source meets that condition.
#   Example: Drone of Brutality "If this would be put into your graveyard, instead put it on the bottom of your deck".
#
# Rule 1.7.5: A modal ability is a choice of modes, where each mode is a base ability the source could have.
# Rule 1.7.5a: Modes of the source are declared as the source is added as a layer on the stack.
# Rule 1.7.5b: Cannot select the same mode more than once unless ability specifies otherwise.
# Rule 1.7.5c: Same mode selected more than once are separate, same target(s) may be selected each time.
# Rule 1.7.5d: Selected modes determine the base abilities for rules and effects.
# Rule 1.7.5e: Number/availability of modes evaluated at time modes are selected.
#
# Rule 1.7.6: A connected ability pair - leading ability's parameters/events referred to by following ability.
# Rule 1.7.6a: An ability can be part of one or more connected ability pairs.
# Rule 1.7.6b: If a following ability cannot refer to the leading ability's parameters/events, relevant effects fail.
# Rule 1.7.6c: If an effect adds a connected ability pair together they are connected; if only one or added separately, not connected.
#
# Rule 1.7.7: The abilities of an object can be modified.

Feature: Section 1.7 - Abilities
    As a game engine
    I need to correctly implement the ability system
    So that abilities generate effects and create layers according to the comprehensive rules

    # Test for Rule 1.7.1 - Ability is a property of an object
    Scenario: ability_is_property_of_object
        Given a card with a functional text ability "Gain 3 life"
        When the ability is defined on the card
        Then the card should have that ability as a property
        And the ability should influence the game

    # Test for Rule 1.7.1 - Base abilities of non-token card come from rules text
    Scenario: base_abilities_from_rules_text
        Given a non-token action card with functional text "Gain 3{h}"
        When the card's base abilities are determined
        Then the base abilities should be derived from the rules text

    # Test for Rule 1.7.1 - Base abilities of token defined by creating effect
    Scenario: token_base_abilities_from_creating_effect
        Given a token card created with the ability "Deal 1 damage"
        When the token's base abilities are determined
        Then the base abilities should be those given at creation
        And the base abilities should not come from a rules text

    # Test for Rule 1.7.1a - Source of an ability is the card that has it
    Scenario: ability_source_is_card_that_has_it
        Given a card with an ability "Gain 3 life"
        When the ability's source is queried
        Then the source should be that card

    # Test for Rule 1.7.1a - Activated-layer source is same as creating ability source
    Scenario: activated_layer_source_is_same_as_creating_ability_source
        Given a card with an activated ability "Gain 1 resource"
        And the ability has been activated creating an activated-layer on the stack
        When the activated-layer's ability source is queried
        Then the source should be the original card

    # Test for Rule 1.7.1a - Activated-layer exists independently of its source
    Scenario: activated_layer_survives_source_destruction
        Given a card with an activated ability has been activated
        And an activated-layer is on the stack
        When the source card is destroyed
        Then the activated-layer should still exist on the stack
        And the activated-layer should still be resolvable

    # Test for Rule 1.7.1a - Triggered-layer exists independently of its source
    Scenario: triggered_layer_survives_source_leaving_play
        Given a card with a triggered ability has triggered
        And a triggered-layer is on the stack
        When the source card moves to the graveyard
        Then the triggered-layer should still exist on the stack
        And the triggered-layer should still be resolvable

    # Test for Rule 1.7.1b - Controller of activated-layer is activating player
    Scenario: activated_layer_controller_is_activating_player
        Given player 0 controls a card with an activated ability
        When player 0 activates the ability creating an activated-layer
        Then the activated-layer's controller should be player 0

    # Test for Rule 1.7.1b - Controller of triggered-layer is controller at trigger time
    Scenario: triggered_layer_controller_is_controller_at_trigger_time
        Given player 0 controls a card with a triggered ability
        When the trigger condition is met for the card
        And a triggered-layer is created
        Then the triggered-layer's controller should be player 0

    # Test for Rule 1.7.1b - Triggered-layer with no-controller source uses owner
    Scenario: triggered_layer_controller_is_owner_when_source_has_no_controller
        Given a card owned by player 0 with no controller
        And the card has a triggered ability
        When the trigger condition is met
        And a triggered-layer is created from the ownerless-controller source
        Then the triggered-layer's controller should be the card's owner (player 0)

    # Test for Rule 1.7.2 - Object with ability is considered card with that ability
    Scenario: object_with_ability_considered_card_with_ability
        Given a card that has an ability "go again" as a property
        When the card is checked for having go again
        Then the card is considered a card with go again

    # Test for Rule 1.7.2 - Triggered go again: card is NOT a card with base go again
    Scenario: triggered_go_again_not_base_go_again
        Given a card "Torrent of Tempo" with the triggered ability "When this hits, it gets go again"
        When the card's base abilities are checked before hitting
        Then the card should NOT be considered a card with base go again
        And the card should NOT be considered a card with go again

    # Test for Rule 1.7.2 - After triggering, card gains go again but not base go again
    Scenario: card_with_triggered_go_again_gains_ability_after_trigger
        Given a card "Torrent of Tempo" with the triggered ability "When this hits, it gets go again"
        And the triggered condition is met (the card hits)
        And the triggered-layer resolves
        When the card's abilities are checked
        Then the card should be considered a card with go again
        But the card should NOT be considered a card with base go again

    # Test for Rule 1.7.3 - Three categories of abilities
    Scenario: there_are_three_categories_of_abilities
        Given the ability category system is initialized
        When the ability categories are queried
        Then there should be exactly three ability categories
        And the categories should be "activated", "resolution", and "static"

    # Test for Rule 1.7.3a - Activated ability creates activated-layer on stack
    Scenario: activated_ability_creates_activated_layer_on_stack
        Given a card has an activated ability "Gain 1 resource"
        And the player has priority
        And the source card is in the arena
        When the player activates the ability
        Then an activated-layer should be created on the stack
        And the activated-layer should not be resolved yet

    # Test for Rule 1.7.3b - Resolution ability generates effects when layer resolves
    Scenario: resolution_ability_generates_effects_on_resolution
        Given a card "Sigil of Solace" has a resolution ability "Gain 3 life"
        And the card is on the stack as a layer
        When the layer resolves
        Then the resolution ability should generate the "Gain 3 life" effect

    # Test for Rule 1.7.3c - Static ability simply generates effects
    Scenario: static_ability_generates_effects_continuously
        Given a card has a static ability "This gets +1 power"
        And the card is in the arena
        When the static ability is checked
        Then it should be generating its effect continuously
        And no player action is required to activate it

    # Test for Rule 1.7.4 - Ability is functional when source is public and in arena
    Scenario: ability_functional_when_source_in_arena
        Given a card with an activated ability "Gain 1 resource"
        And the card is in the arena (public zone)
        When the arena ability's functionality is checked
        Then the ability should be functional

    # Test for Rule 1.7.4 - Ability is non-functional when source is not in arena
    Scenario: ability_nonfunctional_when_source_in_hand
        Given a card with a standard activated ability "Gain 1 resource"
        And the card is in the player's hand (private zone)
        When the hand ability's functionality is checked
        Then the ability should be non-functional

    # Test for Rule 1.7.4a - Non-permanent defending card ability is non-functional
    Scenario: defending_card_ability_nonfunctional_by_default
        Given a non-permanent card is defending
        And the card has a standard activated ability "Gain 1 resource"
        When the non-permanent defending ability's functionality is checked
        Then the ability should be non-functional

    # Test for Rule 1.7.4a - Defending card ability functional if specifies "when defending"
    Scenario: defending_card_ability_functional_when_specified_as_defending_only
        Given a non-permanent card "Rally the Rearguard" is defending
        And the card has the ability "Activate this only while this is defending"
        When the rally defending ability's functionality is checked
        Then the ability should be functional

    # Test for Rule 1.7.4b - Activated ability functional when cost only payable outside arena
    Scenario: activated_ability_functional_when_cost_only_payable_outside_arena
        Given a card "Mighty Windup" with the ability "Instant -- Discard this: Create a Might token"
        And the card is in the player's hand
        When Mighty Windup's ability functionality is checked
        Then the ability should be functional
        And the cost (discarding itself) can only be paid from hand

    # Test for Rule 1.7.4b - Activated ability in banished zone when specifying so
    Scenario: activated_ability_functional_when_specifying_activated_in_banished
        Given a card "Guardian of the Shadowrealm" with the ability specifying "only while in banished zone"
        And the card is in the player's banished zone
        When Guardian's banished zone ability functionality is checked
        Then the ability should be functional

    # Test for Rule 1.7.4c - Resolution ability functional when source resolves as layer
    Scenario: resolution_ability_functional_when_layer_resolves
        Given a card "Sigil of Solace" has a resolution ability "Gain 3{h}"
        And the card is currently resolving as a layer on the stack
        When the resolution ability's functionality is checked while resolving
        Then the ability should be functional

    # Test for Rule 1.7.4c - Resolution ability non-functional when source is not resolving
    Scenario: resolution_ability_nonfunctional_when_source_not_resolving
        Given a card has a resolution ability "Gain 3{h}"
        And the card is in the player's hand (not on stack)
        When the resolution ability's functionality is checked from hand
        Then the ability should be non-functional

    # Test for Rule 1.7.4d - Meta-static ability is functional outside the game
    Scenario: meta_static_ability_functional_outside_game
        Given a card with the Specialization keyword (a meta-static ability)
        When the meta-static ability's functionality is checked outside the game
        Then the ability should be functional outside the game

    # Test for Rule 1.7.4e - Play-static ability functional when source is public and being played
    Scenario: play_static_ability_functional_when_source_being_played
        Given a card "Ghostly Visit" with the play-static ability "You may play this from your banished zone"
        And the card is public in the banished zone
        When the player attempts to play the card
        Then the play-static ability should be functional
        And the card should be playable from the banished zone

    # Test for Rule 1.7.4f - Property-static ability functional in any zone
    Scenario: property_static_ability_functional_in_any_zone
        Given a card "Mutated Mass" with a property-static ability defining its power
        When the ability's functionality is checked while the card is in the graveyard
        Then the property-static ability should be functional
        And the power should be defined by the property-static ability

    # Test for Rule 1.7.4g - While-static ability functional when while-condition met
    Scenario: while_static_ability_functional_when_condition_met
        Given a card "Yinti Yanti" with "While this is defending and you control an aura, this gets +1{d}"
        And the card is defending
        And the player controls an aura
        When the while-static ability's functionality is checked with condition met
        Then the while-static ability should be functional
        And the card should get +1 defense

    # Test for Rule 1.7.4g - While-static ability non-functional when condition not met
    Scenario: while_static_ability_nonfunctional_when_condition_not_met
        Given a card with a while-static ability requiring "while defending"
        And the card is NOT defending
        When the while-static ability's functionality is checked with condition not met
        Then the while-static ability should be non-functional

    # Test for Rule 1.7.4j - Static with zone-movement replacement functional when condition met
    Scenario: zone_movement_replacement_static_functional_when_condition_met
        Given a card "Drone of Brutality" with "If this would be put into your graveyard, instead put it on the bottom of your deck"
        When the card would be moved to the graveyard
        Then the replacement static ability should be functional
        And the card should go to the bottom of the deck instead

    # Test for Rule 1.7.5 - Modal ability is a choice of modes
    Scenario: modal_ability_provides_choice_of_modes
        Given a card "Art of War" with a modal ability "Choose 2"
        And the card has four available modes
        When the card is added to the stack
        Then the player must declare exactly 2 modes

    # Test for Rule 1.7.5a - Modes declared when source added to stack
    Scenario: modes_declared_when_added_to_stack
        Given a card with a modal ability "Choose 1"
        And three available modes
        When the card is announced to be played
        And the card is being added to the stack
        Then the player must declare their chosen mode at that time

    # Test for Rule 1.7.5b - Cannot select same mode twice unless specified
    Scenario: cannot_select_same_mode_twice_without_permission
        Given a card with a modal ability "Choose 2"
        And the card does not specify the same mode can be chosen more than once
        When the player attempts to select mode 1 twice
        Then the selection should be rejected
        And the player must select two distinct modes

    # Test for Rule 1.7.5b - Can only choose available modes up to max
    Scenario: can_only_select_available_modes
        Given a card with a modal ability "Choose 3"
        But only 2 modes are available
        When the player selects modes
        Then the player can only select a maximum of 2 modes

    # Test for Rule 1.7.5c - Same mode selected twice creates separate events
    Scenario: same_mode_twice_creates_separate_not_compound_event
        Given a card that explicitly allows selecting the same mode multiple times
        When the player selects mode 1 twice
        Then two separate mode instances should be created
        And they should not be treated as a single compound event

    # Test for Rule 1.7.5d - Selected modes become base abilities of source
    Scenario: selected_modes_become_base_abilities
        Given a card with a modal ability "Choose 1"
        When the player selects mode A "Gain 3 life"
        Then the card's base abilities should include "Gain 3 life"
        And the card should NOT have the unselected modes as base abilities

    # Test for Rule 1.7.5d - No modes selected means no modal base abilities
    Scenario: no_modes_selected_means_no_modal_base_abilities
        Given a card with a modal ability "Choose 1"
        When no modes have been selected yet
        Then the card should not have any of the modal options as base abilities

    # Test for Rule 1.7.5e - Mode count evaluated at time of mode selection
    Scenario: mode_count_evaluated_at_mode_selection_time
        Given a card "Sacred Art: Undercurrent Desires" with "If you've played another blue card this turn, choose 3. Otherwise, choose 1"
        And the player has already played a blue card this turn
        When the card is added to the stack and modes are selected
        Then the player should be able to choose 3 modes

    # Test for Rule 1.7.5e - Mode count uses game state at selection time, not resolution
    Scenario: mode_count_uses_state_at_selection_not_resolution
        Given a card with "If [condition], choose 2. Otherwise, choose 1"
        And the condition is TRUE at the time the card is added to the stack
        When the modes are selected (2 modes are declared)
        And the condition changes to FALSE before the card resolves
        Then the card should still resolve with 2 modes
        And the count was determined at selection time not resolution time

    # Test for Rule 1.7.6 - Connected ability pair: following ability refers to leading ability
    Scenario: connected_ability_pair_following_refers_to_leading
        Given a card "Reckless Swing" with:
            """
            Leading ability: "As an additional cost to play this, discard a random card"
            Following ability: "If the discarded card has 6 or more {p}, deal 2 damage to the attacking hero"
            """
        When the card is played and the discard additional cost is paid
        Then the following ability can reference the discarded card
        And the following ability can determine if the card had 6+ power

    # Test for Rule 1.7.6a - Ability can be in multiple connected pairs
    Scenario: ability_can_be_part_of_multiple_connected_pairs
        Given a card with ability A, ability B, and ability C
        And ability A is a leading ability for both B and C
        When the connected ability pairs are queried
        Then ability A should be in two connected pairs
        And ability B and C should each be in their own connected pair

    # Test for Rule 1.7.6b - Following ability fails when cannot refer to leading events
    Scenario: following_ability_fails_when_leading_events_unavailable
        Given a card with a connected ability pair
        And the leading ability has NOT been triggered (no discard occurred)
        When the following ability attempts to reference the leading ability's events
        Then the relevant effects of the following ability should fail
        And there are no parameters/events to refer to

    # Test for Rule 1.7.6c - Connected pair added together remains connected
    Scenario: connected_pair_added_together_is_connected
        Given a card with neither ability A nor ability B originally
        When an effect adds both ability A (leading) and ability B (following) together as a connected pair
        Then the added following ability B should be connected to the added leading ability A
        And the following ability should only refer to the added leading ability

    # Test for Rule 1.7.6c - Only one ability added is not connected
    Scenario: adding_only_one_ability_of_connected_pair_is_not_connected
        Given a card with ability A (originally defined)
        When an effect adds only ability B (the following ability from another connected pair)
        Then ability B should NOT be connected to ability A on this card
        And the effects of ability B that reference a leading ability should fail

    # Test for Rule 1.7.7 - Abilities of an object can be modified
    Scenario: object_abilities_can_be_modified
        Given a card with the ability "Deal 2 damage"
        When an effect modifies the card to give it the ability "Deal 4 damage instead"
        Then the card should now have the modified ability
        And the card's original ability should no longer be in effect (or modified)
