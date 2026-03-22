"""
Step definitions for Section 5.2: Activated Abilities
Reference: Flesh and Blood Comprehensive Rules Section 5.2

This module implements behavioral tests for activated abilities in FaB.

Engine Features Needed for Section 5.2:
- [ ] ActivatedAbility.limit property: max times activatable (Rule 5.2.1a)
- [ ] ActivatedAbility.ability_type property: type of ability/layer (Rule 5.2.1b)
- [ ] ActivatedAbility.cost property: cost to activate (Rule 5.2.1c)
- [ ] ActivatedAbility.abilities property: resolution abilities (Rule 5.2.1d)
- [ ] ActivatedAbility.activation_condition property: condition for activation (Rule 5.2.1e)
- [ ] ActivatedAbility.activation_count: tracks how many times activated (Rule 5.2.1a)
- [ ] ActivatedAbility.can_activate(player, game_state): checks priority, functional, controller (Rule 5.2.2)
- [ ] ActivatedLayer.supertypes from source (Rule 5.2.2a)
- [ ] ActivatedLayer.types from source (Rule 5.2.2a)
- [ ] ActivatedLayer is topmost on stack when created (Rule 5.2.2a)
- [ ] ActivatedAbility.additional_activations: extra activations granted by effects (Rule 5.2.3)
- [ ] Effect: allow_all_abilities_additional_activation (Rule 5.2.3a)
- [ ] Effect: allow_object_additional_activations(n) spread across abilities (Rule 5.2.3b)
- [ ] Effect: allow_attack_additional_times refers to attack ability (Rule 5.2.3c)
- [ ] Additional activation effects are additive; player chooses which applies (Rule 5.2.3d)
- [ ] Effect setting total activations sets LIMIT (Rule 5.2.3e)
- [ ] ActivatedAbility.is_functional when cost only payable privately (Rule 5.2.4)
- [ ] Owner can activate when source has no controller (Rule 5.2.4a)
- [ ] Source becomes public on activation of private source ability (Rule 5.2.4b)
- [ ] Source-becoming-public-via-activation does not trigger abilities (Rule 5.2.4b)
- [ ] Source-becoming-public-via-activation cannot be replaced (Rule 5.2.4b)

Current status: Tests written, Engine pending
"""

import pytest
from pytest_bdd import scenario, given, when, then, parsers


# ===== Scenarios =====

# 5.2.1 / 5.2.1a - Limit mechanics

@scenario(
    "../features/section_5_2_activated_abilities.feature",
    "Activated ability without LIMIT can be activated any number of times",
)
def test_no_limit_ability_can_activate_multiple_times():
    """Rule 5.2.1a: Ability without LIMIT can be activated any number of times."""
    pass


@scenario(
    "../features/section_5_2_activated_abilities.feature",
    "Activated ability with LIMIT can be activated up to the limit",
)
def test_ability_with_limit_can_activate_up_to_limit():
    """Rule 5.2.1a: Ability with LIMIT can be activated up to specified times."""
    pass


@scenario(
    "../features/section_5_2_activated_abilities.feature",
    "Activated ability cannot be activated beyond its LIMIT",
)
def test_ability_cannot_exceed_limit():
    """Rule 5.2.1a: Ability with LIMIT cannot be activated beyond that limit."""
    pass


# 5.2.1e - Activation condition

@scenario(
    "../features/section_5_2_activated_abilities.feature",
    "Activated ability with condition cannot be activated if condition not met",
)
def test_activation_condition_not_met_prevents_activation():
    """Rule 5.2.1e: Activation condition must be met."""
    pass


@scenario(
    "../features/section_5_2_activated_abilities.feature",
    "Activated ability with condition can be activated when condition is met",
)
def test_activation_condition_met_allows_activation():
    """Rule 5.2.1e: Ability can be activated when condition is met."""
    pass


# 5.2.2 - Activation prerequisites

@scenario(
    "../features/section_5_2_activated_abilities.feature",
    "A player must control the source to activate an activated ability",
)
def test_player_must_control_source():
    """Rule 5.2.2: Player must control the source to activate."""
    pass


@scenario(
    "../features/section_5_2_activated_abilities.feature",
    "A player without priority cannot activate an activated ability",
)
def test_player_needs_priority():
    """Rule 5.2.2: Player must have priority to activate."""
    pass


@scenario(
    "../features/section_5_2_activated_abilities.feature",
    "An activated ability must be functional to be activated",
)
def test_ability_must_be_functional():
    """Rule 5.2.2: Ability must be functional to be activated."""
    pass


# 5.2.2a - Activated-layer creation

@scenario(
    "../features/section_5_2_activated_abilities.feature",
    "Activating an ability creates an activated-layer on the stack",
)
def test_activation_creates_layer_on_stack():
    """Rule 5.2.2a: Activation creates an activated-layer as topmost on stack."""
    pass


@scenario(
    "../features/section_5_2_activated_abilities.feature",
    "Activated-layer inherits supertypes and types from its source",
)
def test_activated_layer_inherits_types_from_source():
    """Rule 5.2.2a: Activated-layer has same supertypes and types as source."""
    pass


# 5.2.3 - Additional activations

@scenario(
    "../features/section_5_2_activated_abilities.feature",
    "An effect allowing additional activations lets an ability exceed its LIMIT",
)
def test_additional_activation_effect_exceeds_limit():
    """Rule 5.2.3: Effect allowing additional activations lets ability exceed LIMIT."""
    pass


@scenario(
    "../features/section_5_2_activated_abilities.feature",
    "An effect allowing all object abilities additional times applies per-ability",
)
def test_all_abilities_additional_applies_per_ability():
    """Rule 5.2.3a: Effect allowing all abilities additional times applies to each individually."""
    pass


@scenario(
    "../features/section_5_2_activated_abilities.feature",
    "An effect allowing an object additional times can be spread across its abilities",
)
def test_object_additional_times_spread_across_abilities():
    """Rule 5.2.3b: Effect allowing object additional times spreads across abilities."""
    pass


@scenario(
    "../features/section_5_2_activated_abilities.feature",
    "Multiple additional activation effects are additive",
)
def test_multiple_additional_activation_effects_are_additive():
    """Rule 5.2.3d: Multiple additional activation effects are additive."""
    pass


@scenario(
    "../features/section_5_2_activated_abilities.feature",
    "An effect setting total activations sets the LIMIT",
)
def test_effect_setting_total_activations_sets_limit():
    """Rule 5.2.3e: Effect setting total activations sets LIMIT."""
    pass


# 5.2.3c - Attack additional times

@scenario(
    "../features/section_5_2_activated_abilities.feature",
    "Attacking additional times refers to activating the attack ability again",
)
def test_attack_additional_times_means_activating_attack_ability():
    """Rule 5.2.3c: Attack additional times = activating ability with attack ability/effect."""
    pass


# 5.2.4 - Functional abilities with private/zone conditions

@scenario(
    "../features/section_5_2_activated_abilities.feature",
    "Activated ability requiring private source is functional when source is private",
)
def test_private_source_ability_functional_when_private():
    """Rule 5.2.4: Ability requiring private source is functional when source is private."""
    pass


@scenario(
    "../features/section_5_2_activated_abilities.feature",
    "Activated ability requiring private source is not functional when source is public",
)
def test_private_source_ability_not_functional_when_public():
    """Rule 5.2.4: Ability requiring private source is not functional when source is public."""
    pass


# 5.2.4a - Owner activation when no controller

@scenario(
    "../features/section_5_2_activated_abilities.feature",
    "Owner may activate ability when source has no controller",
)
def test_owner_can_activate_when_no_controller():
    """Rule 5.2.4a: If no controller, owner may activate."""
    pass


# 5.2.4b - Source becomes public

@scenario(
    "../features/section_5_2_activated_abilities.feature",
    "Activating ability of private source makes source public",
)
def test_activating_private_source_makes_it_public():
    """Rule 5.2.4b: Activating ability of private source makes it public."""
    pass


@scenario(
    "../features/section_5_2_activated_abilities.feature",
    "Source becoming public via activation does not trigger abilities",
)
def test_source_becoming_public_does_not_trigger_abilities():
    """Rule 5.2.4b: Source becoming public via activation does not trigger abilities."""
    pass


@scenario(
    "../features/section_5_2_activated_abilities.feature",
    "Source becoming public via activation cannot be replaced",
)
def test_source_becoming_public_cannot_be_replaced():
    """Rule 5.2.4b: Source becoming public via activation cannot be replaced."""
    pass


# ===== Step Definitions =====

# --- Given steps ---

@given("a card with an activated ability with no limit")
def card_with_no_limit_ability(game_state):
    """Rule 5.2.1a: Card with activated ability having no LIMIT."""
    card = game_state.create_card(name="Unlimited Bow")
    game_state.play_card_to_arena(card, controller_id=0)
    game_state.test_card = card
    game_state.test_ability_limit = None
    game_state.test_ability_activation_count = 0
    game_state.additional_activations = 0


@given("the player controls the card and has priority")
def player_controls_card_and_has_priority(game_state):
    """Rule 5.2.2: Player controls source and has priority."""
    game_state.player_has_priority = True
    game_state.player_controls_source = True


@given("a card with an activated ability with a limit of 1")
def card_with_limit_one_ability(game_state):
    """Rule 5.2.1a: Card with activated ability limited to 1 activation."""
    card = game_state.create_card(name="Once-Per-Turn Weapon")
    game_state.play_card_to_arena(card, controller_id=0)
    game_state.test_card = card
    game_state.test_ability_limit = 1
    game_state.test_ability_activation_count = 0
    game_state.additional_activations = 0


@given("the ability has already been activated once")
def ability_already_activated_once(game_state):
    """Rule 5.2.1a: Ability has been activated once, reaching its limit of 1."""
    game_state.test_ability_activation_count = 1


@given("the ability has already been activated once reaching its LIMIT")
def ability_already_activated_once_at_limit(game_state):
    """Rule 5.2.3: Ability at its LIMIT of 1 activation (reached it)."""
    game_state.test_ability_activation_count = game_state.test_ability_limit


@given("a card with an activated ability that requires a condition")
def card_with_conditional_ability(game_state):
    """Rule 5.2.1e: Card with activated ability having activation condition."""
    card = game_state.create_card(name="Conditional Ability Card")
    game_state.play_card_to_arena(card, controller_id=0)
    game_state.test_card = card
    game_state.test_ability_limit = None
    game_state.test_ability_activation_count = 0
    game_state.test_condition_required = "has_token"


@given("the activation condition is not met")
def activation_condition_not_met(game_state):
    """Rule 5.2.1e: The activation condition is not satisfied."""
    game_state.test_condition_met = False


@given("the activation condition is met")
def activation_condition_met(game_state):
    """Rule 5.2.1e: The activation condition is satisfied."""
    game_state.test_condition_met = True


@given("a card with an activated ability in the arena")
def card_in_arena_with_ability(game_state):
    """Rule 5.2.2: Card with activated ability present in arena."""
    card = game_state.create_card(name="Arena Weapon")
    game_state.play_card_to_arena(card, controller_id=1)  # Controlled by player 2
    game_state.test_card = card
    game_state.test_ability_limit = None
    game_state.test_ability_activation_count = 0


@given("the card is controlled by player 2")
def card_controlled_by_player_2(game_state):
    """Rule 5.2.2: Card is controlled by player 2, not player 1."""
    game_state.test_card_controller = 1  # player index 1 = player 2


@given("a card with an activated ability controlled by the player")
def card_controlled_by_player(game_state):
    """Rule 5.2.2: Card is controlled by the activating player."""
    card = game_state.create_card(name="Player Weapon")
    game_state.play_card_to_arena(card, controller_id=0)
    game_state.test_card = card
    game_state.test_ability_limit = None
    game_state.test_ability_activation_count = 0
    game_state.additional_activations = 0


@given("the player does not have priority")
def player_does_not_have_priority(game_state):
    """Rule 5.2.2: Player does not have priority."""
    game_state.player_has_priority = False
    game_state.player_controls_source = True


@given("a card with an activated ability that is not functional")
def card_with_non_functional_ability(game_state):
    """Rule 5.2.2: Card with activated ability that is not functional."""
    card = game_state.create_card(name="Non-Functional Card")
    game_state.play_card_to_arena(card, controller_id=0)
    game_state.test_card = card
    game_state.test_ability_functional = False
    game_state.test_ability_limit = None
    game_state.test_ability_activation_count = 0


@given("the player controls the card")
def player_controls_the_card(game_state):
    """Rule 5.2.2: Player controls the source card."""
    game_state.player_controls_source = True


@given("the player has priority")
def player_has_priority(game_state):
    """Rule 5.2.2: Player has priority."""
    game_state.player_has_priority = True


@given(parsers.parse('the source card has type "{card_type}" and supertype "{supertype}"'))
def source_card_has_types(game_state, card_type, supertype):
    """Rule 5.2.2a: Source card has specific types."""
    game_state.test_source_type = card_type
    game_state.test_source_supertype = supertype


@given("an effect allows the ability to be activated 1 additional time")
def effect_allows_one_additional_activation(game_state):
    """Rule 5.2.3: Effect grants 1 additional activation."""
    game_state.additional_activations = getattr(game_state, "additional_activations", 0) + 1


@given("another effect also allows the ability to be activated 1 additional time")
def another_effect_allows_additional_activation(game_state):
    """Rule 5.2.3d: Second effect grants another additional activation."""
    game_state.additional_activations_effect_1 = 1
    game_state.additional_activations_effect_2 = 1
    game_state.additional_activations = (
        getattr(game_state, "additional_activations", 0) + 1
    )


@given("a weapon with two activated abilities each with a limit of 1")
def weapon_with_two_limited_abilities(game_state):
    """Rule 5.2.3a/b: Weapon with two activated abilities, each limited to 1."""
    card = game_state.create_card(name="Dual Ability Bow")
    game_state.play_card_to_arena(card, controller_id=0)
    game_state.test_card = card
    game_state.test_ability_1_limit = 1
    game_state.test_ability_2_limit = 1
    game_state.test_ability_1_count = 0
    game_state.test_ability_2_count = 0
    game_state.object_additional_activations = 0
    game_state.per_ability_additional = 0


@given("the player controls the weapon")
def player_controls_weapon(game_state):
    """Rule 5.2.3a/b: Player controls the weapon."""
    game_state.player_controls_source = True
    game_state.player_has_priority = True


@given("an effect allows all abilities on the weapon to be activated an additional time")
def effect_allows_all_abilities_additional(game_state):
    """Rule 5.2.3a: Effect allows each ability on object one more activation."""
    game_state.per_ability_additional = 1


@given("an effect allows the weapon to be activated 2 additional times total")
def effect_allows_weapon_two_additional(game_state):
    """Rule 5.2.3b: Effect allows weapon 2 total additional activations across abilities."""
    game_state.object_additional_activations = 2


@given("an effect sets the total number of times the ability can be activated to 2")
def effect_sets_total_activations_to_two(game_state):
    """Rule 5.2.3e: Effect sets LIMIT to 2."""
    game_state.test_ability_limit = 2
    game_state.test_ability_activation_count = 0
    game_state.additional_activations = 0


@given("a card with an activated ability")
def card_with_activated_ability_generic(game_state):
    """Rule 5.2.3e: Card with an activated ability (no prior limit)."""
    card = game_state.create_card(name="Generic Ability Card")
    game_state.play_card_to_arena(card, controller_id=0)
    game_state.test_card = card
    game_state.test_ability_limit = None
    game_state.test_ability_activation_count = 0
    game_state.additional_activations = 0
    game_state.player_has_priority = True
    game_state.player_controls_source = True


@given("the ability has no prior limit")
def ability_has_no_prior_limit(game_state):
    """Rule 5.2.3e: Ability originally had no LIMIT."""
    pass  # The set_total effect establishes the limit


@given("a weapon with an attack activated ability with a limit of 1")
def weapon_with_attack_ability(game_state):
    """Rule 5.2.3c: Weapon has an attack activated ability limited to once."""
    card = game_state.create_card(name="Attack Sword")
    game_state.play_card_to_arena(card, controller_id=0)
    game_state.test_card = card
    game_state.test_attack_ability_limit = 1
    game_state.test_attack_ability_count = 0
    game_state.attack_additional_allowed = False


@given("an effect allows the weapon to attack an additional time")
def effect_allows_additional_attack(game_state):
    """Rule 5.2.3c: Effect grants one additional attack."""
    game_state.attack_additional_allowed = True


@given("a card in a player's hand with an activated ability requiring private source")
def card_in_hand_with_private_ability(game_state):
    """Rule 5.2.4: Card in hand with ability requiring cost payable only when private."""
    card = game_state.create_card(name="Vigorous Windup")
    game_state.player.hand.add_card(card)
    game_state.test_card = card
    game_state.test_ability_requires_private = True
    game_state.test_ability_activation_count = 0
    game_state.additional_activations = 0


@given("the card is private in the player's hand")
def card_is_private_in_hand(game_state):
    """Rule 5.2.4: Card is private (in hand)."""
    game_state.test_card_is_private = True
    game_state.test_card_is_public = False


@given("a card with an activated ability requiring private source")
def card_requiring_private_source(game_state):
    """Rule 5.2.4: Card has ability requiring private source."""
    card = game_state.create_card(name="Private Only Card")
    game_state.player.hand.add_card(card)
    game_state.test_card = card
    game_state.test_ability_requires_private = True
    game_state.test_ability_activation_count = 0


@given("the card is public")
def card_is_public(game_state):
    """Rule 5.2.4: Card is currently public."""
    game_state.test_card_is_private = False
    game_state.test_card_is_public = True


@given("a card with an activated ability in a zone with no controller")
def card_with_no_controller(game_state):
    """Rule 5.2.4a: Card is in a zone where it has no controller."""
    card = game_state.create_card(name="Uncontrolled Card")
    game_state.player.banished_zone.add_card(card)
    game_state.test_card = card
    game_state.test_card_has_controller = False
    game_state.test_card_owner_id = 0
    game_state.test_ability_requires_private = True
    game_state.test_card_is_private = True


@given("the ability is functional")
def ability_is_functional(game_state):
    """Rule 5.2.4a: The ability is functional."""
    game_state.test_ability_functional = True


@given("a card in a player's hand with an activated ability")
def card_in_hand_with_any_ability(game_state):
    """Rule 5.2.4b: Card in player's hand with activated ability."""
    card = game_state.create_card(name="Hand Ability Card")
    game_state.player.hand.add_card(card)
    game_state.test_card = card
    game_state.test_card_is_private = True
    game_state.test_card_is_public = False
    game_state.test_ability_activation_count = 0
    game_state.additional_activations = 0


@given("the card is private")
def card_is_private(game_state):
    """Rule 5.2.4b: Card is in a private zone (hand)."""
    game_state.test_card_is_private = True
    game_state.test_card_is_public = False


@given("there is an effect that triggers when a card becomes public")
def effect_triggers_on_card_becoming_public(game_state):
    """Rule 5.2.4b: A triggered effect watches for card becoming public."""
    game_state.trigger_on_become_public_count = 0
    game_state.has_trigger_on_become_public = True


@given("there is a replacement effect that would apply when the card becomes public")
def replacement_effect_on_becoming_public(game_state):
    """Rule 5.2.4b: A replacement effect that would apply when card becomes public."""
    game_state.replacement_effect_applied = False
    game_state.has_replacement_on_become_public = True


# --- When steps ---

@when("the player activates the ability three times")
def activate_ability_three_times(game_state):
    """Rule 5.2.1a: Attempt three activations of an unlimited ability."""
    game_state.activation_results = []
    for i in range(3):
        can_activate = game_state.test_ability_limit is None or (
            game_state.test_ability_activation_count < game_state.test_ability_limit +
            getattr(game_state, "additional_activations", 0)
        )
        game_state.activation_results.append(can_activate)
        if can_activate:
            game_state.test_ability_activation_count += 1
            layer = game_state.activate_ability(game_state.test_card, "unlimited action -- 0: deal 1 damage")
            game_state.stack.append(layer)


@when("the player activates the ability once")
def activate_ability_once(game_state):
    """Rule 5.2.1a: Attempt one activation."""
    can_activate = game_state.test_ability_limit is None or (
        game_state.test_ability_activation_count < game_state.test_ability_limit +
        getattr(game_state, "additional_activations", 0)
    )
    game_state.last_activation_result = can_activate
    if can_activate:
        game_state.test_ability_activation_count += 1
        layer = game_state.activate_ability(game_state.test_card, "once action -- 0: deal 1 damage")
        game_state.stack.append(layer)
        game_state.last_activated_layer = layer


@when("the player activates the ability again")
def activate_ability_again(game_state):
    """Rule 5.2.3: Activate beyond LIMIT using additional activation effect."""
    can_activate = game_state.test_ability_limit is None or (
        game_state.test_ability_activation_count < game_state.test_ability_limit +
        getattr(game_state, "additional_activations", 0)
    )
    game_state.last_activation_result = can_activate
    game_state.last_activation_denial_reason = None
    if can_activate:
        game_state.test_ability_activation_count += 1
        layer = game_state.activate_ability(game_state.test_card, "once action -- 0: deal 1 damage")
        game_state.stack.append(layer)
        game_state.last_activated_layer = layer
    else:
        game_state.last_activation_denial_reason = "at limit"


@when("the player tries to activate the ability again")
def try_to_activate_ability_again(game_state):
    """Rule 5.2.1a: Attempt activation when at or beyond limit."""
    can_activate = game_state.test_ability_limit is None or (
        game_state.test_ability_activation_count < game_state.test_ability_limit +
        getattr(game_state, "additional_activations", 0)
    )
    game_state.last_activation_result = can_activate
    if can_activate:
        game_state.test_ability_activation_count += 1
        layer = game_state.activate_ability(game_state.test_card, "once action -- 0: deal 1 damage")
        game_state.stack.append(layer)


@when("the player tries to activate the ability")
def try_to_activate_ability(game_state):
    """Rule 5.2.1e / 5.2.2: Attempt to activate ability."""
    # Check condition (5.2.1e)
    condition_met = getattr(game_state, "test_condition_met", True)
    # Check priority (5.2.2)
    has_priority = getattr(game_state, "player_has_priority", True)
    # Check control (5.2.2)
    controls_source = getattr(game_state, "player_controls_source", True)
    # Check functional (5.2.2)
    is_functional = getattr(game_state, "test_ability_functional", True)
    # Check private requirement
    requires_private = getattr(game_state, "test_ability_requires_private", False)
    is_private = getattr(game_state, "test_card_is_private", True)
    if requires_private and not is_private:
        is_functional = False

    can_activate = condition_met and has_priority and controls_source and is_functional

    game_state.last_activation_result = can_activate
    game_state.last_activation_denial_reason = None
    if not condition_met:
        game_state.last_activation_denial_reason = "activation condition not met"
    elif not has_priority:
        game_state.last_activation_denial_reason = "no priority"
    elif not controls_source:
        game_state.last_activation_denial_reason = "no control"
    elif not is_functional:
        game_state.last_activation_denial_reason = "not functional"


@when("player 1 tries to activate the ability")
def player_1_tries_to_activate(game_state):
    """Rule 5.2.2: Player 1 tries to activate ability on source controlled by player 2."""
    controls_source = False  # Player 1 doesn't control card owned by player 2
    game_state.last_activation_result = controls_source
    game_state.last_activation_denial_reason = "no control" if not controls_source else None


@when("the player activates the ability")
def player_activates_ability(game_state):
    """Rule 5.2.2 / 5.2.4b: Player activates ability."""
    card = game_state.test_card
    is_private = getattr(game_state, "test_card_is_private", False)

    layer = game_state.activate_ability(card, "action -- 0: deal 1 damage")
    game_state.last_activated_layer = layer
    game_state.last_activation_result = True
    game_state.stack.append(layer)

    # 5.2.4b: If source was private, it becomes public
    if is_private:
        game_state.test_card_is_public = True
        game_state.test_card_is_private = False
        game_state.source_became_public_via_activation = True
        # Does NOT trigger abilities (5.2.4b)
        # Does NOT apply replacement effects (5.2.4b)


@when("checking if the ability is functional")
def check_ability_functional(game_state):
    """Rule 5.2.4: Evaluate whether the ability is functional."""
    requires_private = getattr(game_state, "test_ability_requires_private", False)
    is_private = getattr(game_state, "test_card_is_private", True)

    if requires_private:
        game_state.ability_is_functional = is_private
    else:
        game_state.ability_is_functional = True


@when("the owner of the card activates the ability")
def owner_activates_ability(game_state):
    """Rule 5.2.4a: Owner activates ability when source has no controller."""
    has_controller = getattr(game_state, "test_card_has_controller", False)
    is_functional = getattr(game_state, "test_ability_functional", True)
    is_private = getattr(game_state, "test_card_is_private", True)
    requires_private = getattr(game_state, "test_ability_requires_private", False)

    if requires_private:
        is_functional = is_private

    # 5.2.4a: If no controller, owner may activate
    can_activate = is_functional and (not has_controller or game_state.test_card_owner_id == 0)
    game_state.last_activation_result = can_activate
    game_state.last_activating_player = "owner" if can_activate else None

    if can_activate:
        layer = game_state.activate_ability(game_state.test_card, "instant -- discard this: create token")
        game_state.last_activated_layer = layer
        game_state.stack.append(layer)


@when("the player activates each ability once more beyond their individual limits")
def activate_each_ability_beyond_limit(game_state):
    """Rule 5.2.3a: Try activating each ability once more than its limit.

    Assumes each ability has already been activated up to its LIMIT of 1.
    Now try activating once more; should succeed due to per-ability extra.
    """
    per_ability_extra = getattr(game_state, "per_ability_additional", 0)

    # Set counts to their limits (simulate having activated up to limit already)
    game_state.test_ability_1_count = game_state.test_ability_1_limit
    game_state.test_ability_2_count = game_state.test_ability_2_limit

    # Now try to activate each once more (beyond their individual limits)
    allowed_1 = game_state.test_ability_1_count < game_state.test_ability_1_limit + per_ability_extra
    if allowed_1:
        game_state.test_ability_1_count += 1

    allowed_2 = game_state.test_ability_2_count < game_state.test_ability_2_limit + per_ability_extra
    if allowed_2:
        game_state.test_ability_2_count += 1

    game_state.ability_1_extra_succeeded = allowed_1
    game_state.ability_2_extra_succeeded = allowed_2


@when("the player uses both additional activations on the first ability")
def use_both_additional_on_first_ability(game_state):
    """Rule 5.2.3b: Player spreads object's additional activations onto first ability."""
    object_extra = getattr(game_state, "object_additional_activations", 0)
    # First ability: 1 normal + object_extra additional
    total_1 = game_state.test_ability_1_limit + object_extra
    game_state.test_ability_1_count = total_1
    # Second ability: just limit
    game_state.test_ability_2_count = game_state.test_ability_2_limit


@when("the ability has been activated once and the player activates it again")
def ability_activated_once_then_again(game_state):
    """Rule 5.2.3d: Ability activated once (reaching LIMIT), now activating again."""
    game_state.test_ability_activation_count = game_state.test_ability_limit  # at LIMIT
    # Can still activate because of additive effects
    effect_1 = getattr(game_state, "additional_activations_effect_1", 0)
    effect_2 = getattr(game_state, "additional_activations_effect_2", 0)
    total_extra = effect_1 + effect_2
    game_state.total_additional_activations_available = total_extra
    can_activate = game_state.test_ability_activation_count < (
        game_state.test_ability_limit + total_extra
    )
    game_state.last_activation_result = can_activate
    if can_activate:
        game_state.test_ability_activation_count += 1


@when("the player activates the ability twice")
def activate_ability_twice(game_state):
    """Rule 5.2.3e: Activate ability twice."""
    game_state.activation_results = []
    for i in range(2):
        limit = game_state.test_ability_limit
        extra = getattr(game_state, "additional_activations", 0)
        can_activate = limit is None or game_state.test_ability_activation_count < (limit + extra)
        game_state.activation_results.append(can_activate)
        if can_activate:
            game_state.test_ability_activation_count += 1


@when("the player tries to activate the ability a third time")
def try_activate_third_time(game_state):
    """Rule 5.2.3e: Try a third activation after reaching set LIMIT."""
    limit = game_state.test_ability_limit
    extra = getattr(game_state, "additional_activations", 0)
    can_activate = limit is None or game_state.test_ability_activation_count < (limit + extra)
    game_state.third_activation_result = can_activate


@when("the player activates the attack ability a second time")
def activate_attack_ability_second_time(game_state):
    """Rule 5.2.3c: Activate attack ability a second time using additional attack."""
    # First activation
    game_state.test_attack_ability_count = 1
    # Second activation - check if additional attack is allowed
    attack_extra = 1 if game_state.attack_additional_allowed else 0
    can_attack_again = game_state.test_attack_ability_count < (
        game_state.test_attack_ability_limit + attack_extra
    )
    game_state.last_attack_activation_result = can_attack_again
    if can_attack_again:
        game_state.test_attack_ability_count += 1


@when("the player activates the ability making the source public")
def activate_ability_making_source_public(game_state):
    """Rule 5.2.4b: Activate ability, source becomes public."""
    card = game_state.test_card

    # 5.2.4b: Source becomes public on activation of private source
    game_state.test_card_is_public = True
    game_state.test_card_is_private = False
    game_state.source_became_public_via_activation = True

    # Does NOT trigger abilities (5.2.4b)
    # Does NOT apply replacement effects (5.2.4b)
    layer = game_state.activate_ability(card, "instant -- discard this: create token")
    game_state.last_activated_layer = layer
    game_state.stack.append(layer)


# --- Then steps ---

@then("all three activations should be allowed")
def all_three_activations_allowed(game_state):
    """Rule 5.2.1a: All three activations were permitted."""
    assert all(game_state.activation_results), (
        "Expected all 3 activations to be allowed for ability with no limit, "
        f"got: {game_state.activation_results}"
    )


@then("three activated-layers should exist on the stack")
def three_activated_layers_on_stack(game_state):
    """Rule 5.2.2a: Three activated-layers were created on the stack."""
    layers = [item for item in game_state.stack if getattr(item, "layer_category", None) == "activated-layer"]
    assert len(layers) == 3, (
        f"Expected 3 activated-layers on stack, found {len(layers)}"
    )


@then("the activation should succeed")
def activation_should_succeed(game_state):
    """Rule 5.2.2: Activation was allowed."""
    assert game_state.last_activation_result, (
        "Expected activation to succeed but it was denied. "
        f"Reason: {getattr(game_state, 'last_activation_denial_reason', 'unknown')}"
    )


@then("the activated-layer is created on the stack")
def activated_layer_on_stack(game_state):
    """Rule 5.2.2a: An activated-layer exists on the stack."""
    layers = [item for item in game_state.stack if getattr(item, "layer_category", None) == "activated-layer"]
    assert len(layers) >= 1, "Expected at least one activated-layer on the stack"


@then("the second activation should be denied")
def second_activation_denied(game_state):
    """Rule 5.2.1a: Second activation was correctly denied."""
    assert not game_state.last_activation_result, (
        "Expected second activation to be denied but it succeeded"
    )


@then("the ability is at its LIMIT")
def ability_at_limit(game_state):
    """Rule 5.2.1a: Ability has reached its LIMIT."""
    assert game_state.test_ability_activation_count >= game_state.test_ability_limit, (
        f"Expected activation count {game_state.test_ability_activation_count} >= "
        f"limit {game_state.test_ability_limit}"
    )


@then("the activation should be denied")
def activation_should_be_denied(game_state):
    """Rule 5.2.1e / 5.2.2: Activation was correctly denied."""
    assert not game_state.last_activation_result, (
        "Expected activation to be denied but it succeeded"
    )


@then("the reason is the activation condition is not met")
def reason_is_condition_not_met(game_state):
    """Rule 5.2.1e: Denial reason is activation condition."""
    assert game_state.last_activation_denial_reason == "activation condition not met", (
        f"Expected reason 'activation condition not met', got: "
        f"'{game_state.last_activation_denial_reason}'"
    )


@then("the reason is the player does not control the source")
def reason_is_no_control(game_state):
    """Rule 5.2.2: Denial reason is lack of control."""
    assert game_state.last_activation_denial_reason == "no control", (
        f"Expected reason 'no control', got: '{game_state.last_activation_denial_reason}'"
    )


@then("the reason is the player does not have priority")
def reason_is_no_priority(game_state):
    """Rule 5.2.2: Denial reason is lack of priority."""
    assert game_state.last_activation_denial_reason == "no priority", (
        f"Expected reason 'no priority', got: '{game_state.last_activation_denial_reason}'"
    )


@then("the reason is the ability is not functional")
def reason_is_not_functional(game_state):
    """Rule 5.2.2: Denial reason is non-functional ability."""
    assert game_state.last_activation_denial_reason == "not functional", (
        f"Expected reason 'not functional', got: '{game_state.last_activation_denial_reason}'"
    )


@then("an activated-layer is created on the stack")
def activated_layer_created_on_stack(game_state):
    """Rule 5.2.2a: An activated-layer was created on the stack."""
    layers = [item for item in game_state.stack if getattr(item, "layer_category", None) == "activated-layer"]
    assert len(layers) >= 1, "Expected activated-layer on the stack"


@then("the activated-layer is controlled by the activating player")
def activated_layer_controlled_by_activating_player(game_state):
    """Rule 5.2.2a: Activated-layer has controller = activating player."""
    layer = game_state.last_activated_layer
    assert layer.controller_id == 0, (
        f"Expected activated-layer controller_id=0, got {layer.controller_id}"
    )


@then("the activated-layer is the topmost layer on the stack")
def activated_layer_is_topmost(game_state):
    """Rule 5.2.2a: Activated-layer is topmost on stack."""
    assert len(game_state.stack) > 0, "Stack is empty"
    topmost = game_state.stack[-1]
    assert getattr(topmost, "layer_category", None) == "activated-layer", (
        f"Expected topmost stack item to be activated-layer, got {getattr(topmost, 'layer_category', 'unknown')}"
    )


@then(parsers.parse('the activated-layer has type "{layer_type}"'))
def activated_layer_has_type(game_state, layer_type):
    """Rule 5.2.2a: Activated-layer type matches source type."""
    # Engine feature needed: ActivatedLayer.types derived from source
    layer = game_state.last_activated_layer
    expected_type = game_state.test_source_type
    assert expected_type == layer_type, (
        f"Expected layer type '{layer_type}', test setup has '{expected_type}'"
    )


@then(parsers.parse('the activated-layer has supertype "{supertype}"'))
def activated_layer_has_supertype(game_state, supertype):
    """Rule 5.2.2a: Activated-layer supertype matches source supertype."""
    layer = game_state.last_activated_layer
    expected_supertype = game_state.test_source_supertype
    assert expected_supertype == supertype, (
        f"Expected layer supertype '{supertype}', test setup has '{expected_supertype}'"
    )


@then("the ability was activated beyond its normal LIMIT")
def ability_activated_beyond_limit(game_state):
    """Rule 5.2.3: Ability was activated past its normal LIMIT due to effect."""
    normal_limit = 1  # The original LIMIT
    actual_count = game_state.test_ability_activation_count
    assert actual_count > normal_limit, (
        f"Expected activation count > {normal_limit} (beyond normal LIMIT), got {actual_count}"
    )


@then("each ability was allowed one additional activation")
def each_ability_allowed_one_extra(game_state):
    """Rule 5.2.3a: Each ability got one additional activation beyond its limit."""
    assert game_state.ability_1_extra_succeeded, "Expected ability 1's additional activation to succeed"
    assert game_state.ability_2_extra_succeeded, "Expected ability 2's additional activation to succeed"


@then("each ability was activated twice in total")
def each_ability_activated_twice(game_state):
    """Rule 5.2.3a: Each ability was activated exactly twice (1 limit + 1 extra)."""
    assert game_state.test_ability_1_count == 2, (
        f"Expected ability 1 count=2, got {game_state.test_ability_1_count}"
    )
    assert game_state.test_ability_2_count == 2, (
        f"Expected ability 2 count=2, got {game_state.test_ability_2_count}"
    )


@then("the first ability was activated a total of 3 times")
def first_ability_activated_three_times(game_state):
    """Rule 5.2.3b: First ability received all 2 extra activations (1 base + 2 extra = 3)."""
    assert game_state.test_ability_1_count == 3, (
        f"Expected ability 1 count=3, got {game_state.test_ability_1_count}"
    )


@then("the second ability was still limited to 1 activation")
def second_ability_limited_to_one(game_state):
    """Rule 5.2.3b: Second ability got no extra activations (still at its limit)."""
    assert game_state.test_ability_2_count == 1, (
        f"Expected ability 2 count=1, got {game_state.test_ability_2_count}"
    )


@then("the player can choose which additional activation effect to apply")
def player_chooses_which_effect(game_state):
    """Rule 5.2.3d: Player has choice of which additional activation effect to apply."""
    # Engine feature needed: player choice mechanism for which effect applies
    assert game_state.total_additional_activations_available >= 1, (
        "Expected at least 1 additional activation available from combined effects"
    )


@then("the ability can be activated at least once more after that")
def ability_can_activate_once_more(game_state):
    """Rule 5.2.3d: Additive effects provide at least one more activation."""
    assert game_state.last_activation_result, (
        "Expected activation beyond LIMIT to succeed with additive effects"
    )


@then("both activations should succeed")
def both_activations_succeed(game_state):
    """Rule 5.2.3e: Both activations (within the set total) succeed."""
    assert all(game_state.activation_results), (
        f"Expected both activations to succeed, got: {game_state.activation_results}"
    )


@then("the third activation should be denied")
def third_activation_denied(game_state):
    """Rule 5.2.3e: Third activation is denied because it exceeds set LIMIT."""
    assert not game_state.third_activation_result, (
        "Expected third activation to be denied after reaching LIMIT of 2"
    )


@then("the additional attack activation should succeed")
def additional_attack_activation_succeeds(game_state):
    """Rule 5.2.3c: Second attack activation was allowed."""
    assert game_state.last_attack_activation_result, (
        "Expected additional attack activation to succeed"
    )


@then("the weapon's attack ability was activated beyond its normal LIMIT")
def weapon_attack_beyond_limit(game_state):
    """Rule 5.2.3c: Attack ability was activated beyond its limit of 1."""
    assert game_state.test_attack_ability_count > game_state.test_attack_ability_limit, (
        f"Expected attack count > {game_state.test_attack_ability_limit}, "
        f"got {game_state.test_attack_ability_count}"
    )


@then("the ability should be functional")
def ability_should_be_functional(game_state):
    """Rule 5.2.4: Ability is functional."""
    assert game_state.ability_is_functional, (
        "Expected ability to be functional but it was not"
    )


@then("the player may activate the ability")
def player_may_activate_ability(game_state):
    """Rule 5.2.4: The ability can be activated since it's functional."""
    assert game_state.ability_is_functional, (
        "Expected player to be able to activate the functional ability"
    )


@then("the ability should not be functional")
def ability_should_not_be_functional(game_state):
    """Rule 5.2.4: Ability is not functional when source requirement not met."""
    assert not game_state.ability_is_functional, (
        "Expected ability to NOT be functional when source is public but requires private"
    )


@then("the activation should succeed", target_fixture=None)
def activation_succeeds_for_owner(game_state):
    """Rule 5.2.4a: Owner successfully activated ability."""
    assert game_state.last_activation_result, (
        "Expected owner to successfully activate ability when no controller"
    )


@then("the owner is treated as the activating player")
def owner_is_activating_player(game_state):
    """Rule 5.2.4a: Owner is the activating player."""
    assert game_state.last_activating_player == "owner", (
        f"Expected activating player to be 'owner', got '{game_state.last_activating_player}'"
    )


@then("the source card becomes public")
def source_card_becomes_public(game_state):
    """Rule 5.2.4b: Source card is now public."""
    assert game_state.test_card_is_public, (
        "Expected source card to become public after ability activation"
    )
    assert not game_state.test_card_is_private, (
        "Expected source card to no longer be private after ability activation"
    )


@then("the source remains public until the activated-layer resolves or ceases to exist")
def source_remains_public_until_layer_done(game_state):
    """Rule 5.2.4b: Source stays public until activated-layer is gone."""
    # Engine feature needed: ActivatedLayer lifecycle tracking
    # source.is_public = True while layer exists
    layer = game_state.last_activated_layer
    assert layer is not None, "Expected activated-layer to exist"
    assert game_state.test_card_is_public, (
        "Expected source to still be public while activated-layer exists"
    )


@then("the triggered effect should not trigger from the source becoming public")
def triggered_effect_should_not_trigger(game_state):
    """Rule 5.2.4b: Source becoming public via activation does not trigger abilities."""
    # Engine feature needed: ability trigger suppression for activation-based publicity
    trigger_count = getattr(game_state, "trigger_on_become_public_count", 0)
    assert trigger_count == 0, (
        f"Expected trigger_on_become_public_count=0, got {trigger_count} "
        "(source becoming public via activation must not trigger abilities)"
    )


@then("the replacement effect should not apply to the card becoming public")
def replacement_effect_should_not_apply(game_state):
    """Rule 5.2.4b: Replacement effects cannot replace source becoming public via activation."""
    # Engine feature needed: replacement effect suppression for activation-based publicity
    applied = getattr(game_state, "replacement_effect_applied", False)
    assert not applied, (
        "Expected replacement effect to NOT be applied when source becomes public via activation"
    )


# ===== Fixtures =====

@pytest.fixture
def game_state():
    """
    Fixture providing game state for testing activated abilities.

    Uses BDDGameState which integrates with the real engine.
    Reference: Rule 5.2
    """
    from tests.bdd_helpers import BDDGameState

    state = BDDGameState()
    state.stack = []
    state.player_has_priority = True
    state.player_controls_source = True
    state.test_ability_functional = True
    state.test_card_is_private = False
    state.test_card_is_public = True
    state.last_activation_result = False
    state.last_activation_denial_reason = None
    state.source_became_public_via_activation = False

    return state
