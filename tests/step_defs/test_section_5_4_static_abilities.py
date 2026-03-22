"""
Step definitions for Section 5.4: Static Abilities
Reference: Flesh and Blood Comprehensive Rules Section 5.4

This module implements behavioral tests for static abilities in FaB:
- Static abilities generate effects without resolving a layer on the stack
- Meta-static abilities apply to outside-game rules
- Play-static abilities govern playing the source card (additional/alternative costs)
- Property-static abilities define dynamic card properties
- Triggered-static abilities generate single triggered effects
- While-static abilities are conditional on game state

Engine Features Needed for Section 5.4:
- [ ] StaticAbility type / marker (Rule 5.4.1): abilities that are written as statements and
      generate effects without stack resolution
- [ ] StaticContinuousEffect (Rule 5.4.2): created by functional static abilities; ends when
      the static ability becomes non-functional
- [ ] MetaStaticAbility (Rule 5.4.3): sub-type that generates outside-game rule effects
- [ ] MetaStaticAbility.outside_game_rules_modified: tracks what outside-game rules are altered
- [ ] card_pool_legality_locked_in: during-game ceasing of meta-static doesn't re-evaluate legality (Rule 5.4.3a)
- [ ] PlayStaticAbility (Rule 5.4.4): sub-type affecting playing of the source card
- [ ] AdditionalCostAbility (Rule 5.4.4a): adds asset-cost / effect-cost to play source
- [ ] AdditionalCostAbility.is_optional: True if cost uses "may" (Rule 5.4.4a)
- [ ] AdditionalCostAbility.must_be_declared_on_play: True; declared at time of playing (Rule 5.4.4a)
- [ ] AlternativeCostAbility (Rule 5.4.4b): replaces base costs; does not affect additional costs
- [ ] AlternativeCostAbility.must_be_declared_on_play: True (Rule 5.4.4b)
- [ ] PlayStaticTriggeredEffect (Rule 5.4.4c): triggers immediately when "When you do" condition met
- [ ] PlayStaticConditionalContinuousEffect (Rule 5.4.4d): generated at time "If you do" condition met
- [ ] PropertyStaticAbility (Rule 5.4.5): defines a property / property-value on an object
- [ ] PropertyStaticAbility.functions_everywhere: True — in all zones and outside game (Rule 5.4.5a)
- [ ] TriggerStaticAbility (Rule 5.4.6): generates a single triggered effect on trigger event
- [ ] TriggerStaticAbility.trigger_even_if_source_ceases: True if source ceases from trigger event (Rule 5.4.6a)
- [ ] WhileStaticAbility (Rule 5.4.7): conditional static ability with a "While [COND]" structure
- [ ] WhileStaticAbility.is_functional(game_state): checks condition + source public/private (Rule 5.4.7a)
- [ ] WhileStaticAbility.explicitly_private_zone: True if while-condition explicitly names private zone (Rule 5.4.7a)
- [ ] HiddenTriggeredAbility (Rule 5.4.7b): both while-static and triggered-static; source is private
- [ ] HiddenTriggeredAbility.owner_may_trigger: player may decide to trigger when source is private
- [ ] HiddenTriggeredAbility.make_source_public(): reveals source when owner triggers
- [ ] HiddenTriggeredAbility.return_to_private(): restores privacy after triggered-layer resolves

Current status: Tests written, Engine pending
"""

import pytest
from pytest_bdd import scenario, given, when, then, parsers


# ===== Scenario definitions =====

@scenario(
    "../features/section_5_4_static_abilities.feature",
    "Static ability generates effects without resolving a layer",
)
def test_static_ability_no_layer_needed():
    """Rule 5.4.1: Static ability generates effects without stack resolution."""
    pass


@scenario(
    "../features/section_5_4_static_abilities.feature",
    "Functional static ability generates a static continuous effect",
)
def test_functional_static_generates_continuous_effect():
    """Rule 5.4.2: Functional static ability generates static continuous effect."""
    pass


@scenario(
    "../features/section_5_4_static_abilities.feature",
    "Static continuous effect ends when static ability becomes non-functional",
)
def test_static_effect_ends_when_nonfunctional():
    """Rule 5.4.2 / 6.2.3a: Static continuous effect ends when ability non-functional."""
    pass


@scenario(
    "../features/section_5_4_static_abilities.feature",
    "Meta-static ability applies rules outside the game",
)
def test_meta_static_applies_outside_game():
    """Rule 5.4.3: Meta-static ability generates effects for outside-game rules."""
    pass


@scenario(
    "../features/section_5_4_static_abilities.feature",
    "Meta-static ability ceasing during game does not affect card-pool legality",
)
def test_meta_static_ceasing_does_not_affect_legality():
    """Rule 5.4.3a: Ceasing of meta-static during game does not affect prior outside-game rules."""
    pass


@scenario(
    "../features/section_5_4_static_abilities.feature",
    "Additional-cost ability requires extra cost to play card",
)
def test_additional_cost_required():
    """Rule 5.4.4a: Additional cost must be paid to play a card with additional-cost ability."""
    pass


@scenario(
    "../features/section_5_4_static_abilities.feature",
    "Additional-cost ability is mandatory when not using the word may",
)
def test_additional_cost_is_mandatory():
    """Rule 5.4.4a: Mandatory additional cost cannot be skipped."""
    pass


@scenario(
    "../features/section_5_4_static_abilities.feature",
    "Optional additional-cost ability can be skipped when using the word may",
)
def test_optional_additional_cost_can_be_skipped():
    """Rule 5.4.4a: Optional additional cost (using 'may') can be skipped."""
    pass


@scenario(
    "../features/section_5_4_static_abilities.feature",
    "Alternative-cost ability allows paying different cost instead of base cost",
)
def test_alternative_cost_replaces_base_cost():
    """Rule 5.4.4b: Alternative cost replaces base asset-costs/effect-costs."""
    pass


@scenario(
    "../features/section_5_4_static_abilities.feature",
    "Alternative cost does not affect additional costs",
)
def test_alternative_cost_does_not_affect_additional_costs():
    """Rule 5.4.4b: Alternative cost has no effect on any additional costs."""
    pass


@scenario(
    "../features/section_5_4_static_abilities.feature",
    "Alternative-cost ability must be declared when playing the card",
)
def test_alternative_cost_must_be_declared_on_play():
    """Rule 5.4.4b: Alternative cost must be declared at time of playing the card."""
    pass


@scenario(
    "../features/section_5_4_static_abilities.feature",
    "Play-static triggered effect triggers immediately when condition is met",
)
def test_play_static_triggered_effect_triggers_immediately():
    """Rule 5.4.4c: Triggered play-static effect triggers immediately when condition met."""
    pass


@scenario(
    "../features/section_5_4_static_abilities.feature",
    "Conditional continuous effect from play-static ability generated when condition met",
)
def test_play_static_conditional_continuous_effect_generated():
    """Rule 5.4.4d: Conditional continuous effect generated when play condition is met."""
    pass


@scenario(
    "../features/section_5_4_static_abilities.feature",
    "Property-static ability defines a dynamic card property",
)
def test_property_static_defines_dynamic_property():
    """Rule 5.4.5: Property-static ability defines the value of a property dynamically."""
    pass


@scenario(
    "../features/section_5_4_static_abilities.feature",
    "Property-static ability updates when game state changes",
)
def test_property_static_updates_with_game_state():
    """Rule 5.4.5: Property-static ability value reflects current game state."""
    pass


@scenario(
    "../features/section_5_4_static_abilities.feature",
    "Property-static ability is functional anywhere in the game",
)
def test_property_static_functional_in_any_zone():
    """Rule 5.4.5a: Property-static abilities function anywhere in the game."""
    pass


@scenario(
    "../features/section_5_4_static_abilities.feature",
    "Property-static ability is functional outside the game",
)
def test_property_static_functional_outside_game():
    """Rule 5.4.5a: Property-static abilities function outside the game."""
    pass


@scenario(
    "../features/section_5_4_static_abilities.feature",
    "Triggered-static ability generates a single triggered effect",
)
def test_triggered_static_generates_single_triggered_effect():
    """Rule 5.4.6: Triggered-static ability generates exactly one triggered effect."""
    pass


@scenario(
    "../features/section_5_4_static_abilities.feature",
    "Triggered-static ability triggers even when source is destroyed by the triggering event",
)
def test_triggered_static_triggers_when_source_ceases_from_trigger():
    """Rule 5.4.6a: Triggered-static triggers even if source ceases from triggering event."""
    pass


@scenario(
    "../features/section_5_4_static_abilities.feature",
    "Triggered-static ability does not trigger if not functional before the event",
)
def test_triggered_static_does_not_trigger_when_not_functional():
    """Rule 5.4.6a: Triggered-static does NOT trigger if not functional before event."""
    pass


@scenario(
    "../features/section_5_4_static_abilities.feature",
    "While-static ability is functional when its condition is met",
)
def test_while_static_functional_when_condition_met():
    """Rule 5.4.7: While-static ability becomes functional when its condition is satisfied."""
    pass


@scenario(
    "../features/section_5_4_static_abilities.feature",
    "While-static ability is not functional when condition is not met",
)
def test_while_static_not_functional_when_condition_not_met():
    """Rule 5.4.7: While-static ability is not functional when condition is not satisfied."""
    pass


@scenario(
    "../features/section_5_4_static_abilities.feature",
    "While-static ability for public zone is functional when source is public",
)
def test_while_static_public_zone_functional_when_public():
    """Rule 5.4.7a: While-static for public zone is functional when source is public."""
    pass


@scenario(
    "../features/section_5_4_static_abilities.feature",
    "While-static ability explicitly specifying hand is functional when source is private",
)
def test_while_static_explicitly_private_zone_functional():
    """Rule 5.4.7a: While-static explicitly specifying private zone is functional when private."""
    pass


@scenario(
    "../features/section_5_4_static_abilities.feature",
    "While-static ability for public zone is not functional when source is private",
)
def test_while_static_public_zone_not_functional_when_private():
    """Rule 5.4.7a: While-static for public zone is NOT functional when source is private."""
    pass


@scenario(
    "../features/section_5_4_static_abilities.feature",
    "Hidden triggered ability owner may choose to trigger when source is private",
)
def test_hidden_triggered_owner_may_choose_to_trigger():
    """Rule 5.4.7b: Hidden triggered ability - owner may decide to trigger when source is private."""
    pass


@scenario(
    "../features/section_5_4_static_abilities.feature",
    "Hidden triggered ability source becomes public when triggered",
)
def test_hidden_triggered_source_becomes_public_on_trigger():
    """Rule 5.4.7b: Source becomes public when owner triggers hidden triggered ability."""
    pass


@scenario(
    "../features/section_5_4_static_abilities.feature",
    "Hidden triggered ability source returns to private after triggered layer resolves",
)
def test_hidden_triggered_source_returns_to_private_after_resolution():
    """Rule 5.4.7b: Source returns to private after triggered-layer resolves."""
    pass


# ===== Step Definitions =====

# ----- 5.4.1: Static ability generates effects without stack layer -----

@given("a card with a static ability that grants a bonus effect")
def step_card_with_static_ability(game_state):
    """Rule 5.4.1: Static ability is written as a statement."""
    from tests.bdd_helpers import BDDGameState
    card = game_state.create_card(name="Static Test Card", card_type="action")
    game_state.static_ability_card = card
    game_state.static_ability_type = "static"


@when("the card is in play")
def step_card_is_in_play(game_state):
    """Rule 5.4.1: Card with static ability is in play."""
    game_state.static_ability_was_in_play = True


@then("the static ability is functional without any layer on the stack")
def step_static_ability_functional_no_layer(game_state):
    """Rule 5.4.1: Static ability does not require a layer on the stack to be functional."""
    result = game_state.get_static_ability_info(
        game_state.static_ability_card,
        ability_type=game_state.static_ability_type,
    )
    assert result.requires_stack_layer is False, (
        "Static ability should be functional without placing a layer on the stack"
    )


@then("the effect is generated immediately without stack resolution")
def step_effect_generated_without_stack(game_state):
    """Rule 5.4.1: Static effect is generated immediately, no stack resolution required."""
    result = game_state.get_static_ability_info(
        game_state.static_ability_card,
        ability_type=game_state.static_ability_type,
    )
    assert result.generates_without_stack is True, (
        "Static ability should generate effects without resolving a layer on the stack"
    )


# ----- 5.4.2: Static continuous effect -----

@given("a card with a functional static ability in the arena")
def step_card_with_functional_static_in_arena(game_state):
    """Rule 5.4.2: Functional static ability in the arena."""
    card = game_state.create_card(name="Functional Static Card", card_type="permanent")
    game_state.play_card_to_arena(card)
    game_state.functional_static_card = card


@when("I check the type of effect generated by the static ability")
def step_check_effect_type(game_state):
    """Rule 5.4.2: Inspect effect type generated by functional static ability."""
    game_state.effect_type_result = game_state.get_static_ability_effect_type(
        game_state.functional_static_card
    )


@then("the effect is a static continuous effect")
def step_effect_is_static_continuous(game_state):
    """Rule 5.4.2: Functional static abilities generate static continuous effects."""
    assert game_state.effect_type_result.effect_type == "static_continuous", (
        "Functional static ability must generate a static continuous effect"
    )


@then("the effect persists as long as the static ability is functional")
def step_effect_persists_while_functional(game_state):
    """Rule 5.4.2 / 6.2.3a: Static continuous effect persists while ability is functional."""
    assert game_state.effect_type_result.has_no_specified_duration is True, (
        "Static continuous effect should persist without a specified duration (ends only when non-functional)"
    )


@given("a card with a static ability in the arena")
def step_card_with_static_in_arena(game_state):
    """Rule 5.4.2: Card with static ability placed in arena."""
    card = game_state.create_card(name="Static In Arena", card_type="permanent")
    game_state.play_card_to_arena(card)
    game_state.static_in_arena_card = card


@given("the static ability is currently functional and generating an effect")
def step_static_ability_currently_functional(game_state):
    """Rule 5.4.2: Static ability is functional and effect is active."""
    game_state.static_was_functional = game_state.get_static_ability_info(
        game_state.static_in_arena_card, ability_type="static"
    )
    assert game_state.static_was_functional.is_functional is True, (
        "Static ability should be functional while card is in arena"
    )


@when("the card leaves the arena")
def step_card_leaves_arena(game_state):
    """Rule 5.4.2: Card moves out of arena, making static ability non-functional."""
    result = game_state.move_card_out_of_arena(game_state.static_in_arena_card)
    game_state.card_left_arena_result = result


@then("the static continuous effect ends")
def step_static_effect_ends(game_state):
    """Rule 5.4.2 / 6.2.3a: Static continuous effect ends when ability non-functional."""
    result = game_state.get_static_ability_info(
        game_state.static_in_arena_card, ability_type="static"
    )
    assert result.is_functional is False, (
        "Static ability should become non-functional when card leaves arena"
    )
    assert result.effect_ended is True, (
        "Static continuous effect should end when ability becomes non-functional"
    )


@then("the bonus from the static ability is no longer applied")
def step_static_bonus_no_longer_applied(game_state):
    """Rule 5.4.2: Effect generated by static ability stops when ability non-functional."""
    result = game_state.check_static_effect_applied(game_state.static_in_arena_card)
    assert result.effect_is_applied is False, (
        "Bonus from static ability should no longer apply once ability is non-functional"
    )


# ----- 5.4.3: Meta-static ability -----

@given("a hero with a meta-static ability that modifies deck building rules")
def step_hero_with_meta_static(game_state):
    """Rule 5.4.3: Hero has a meta-static ability modifying outside-game rules."""
    hero = game_state.create_card(name="Meta Static Hero", card_type="hero")
    game_state.meta_static_hero = hero
    game_state.meta_static_ability_type = "meta_static"


@when("evaluating the card-pool for legality outside the game")
def step_evaluate_card_pool_outside_game(game_state):
    """Rule 5.4.3: Evaluate card-pool legality with meta-static ability active."""
    game_state.card_pool_eval_result = game_state.evaluate_card_pool_with_meta_static(
        game_state.meta_static_hero
    )


@then("the meta-static ability modifies the outside-game rules")
def step_meta_static_modifies_outside_rules(game_state):
    """Rule 5.4.3: Meta-static ability applies to rules outside of the game."""
    assert game_state.card_pool_eval_result.outside_game_rules_modified is True, (
        "Meta-static ability should modify outside-game rules (e.g., deck building)"
    )


@then("cards that would normally be illegal become legal due to the meta-static ability")
def step_cards_legal_due_to_meta_static(game_state):
    """Rule 5.4.3: Cards that violate default rules become legal via meta-static ability."""
    assert game_state.card_pool_eval_result.previously_illegal_cards_now_legal is True, (
        "Meta-static ability should allow otherwise-illegal cards in card-pool"
    )


@given("a hero with a meta-static ability allowing specialization cards of any hero")
def step_hero_with_cross_specialization_meta_static(game_state):
    """Rule 5.4.3a: Hero has meta-static allowing any hero's specialization cards."""
    hero = game_state.create_card(name="Shiyana Diamond Gemini", card_type="hero")
    game_state.meta_static_hero = hero


@given("the player has specialization cards in their card-pool based on that ability")
def step_player_has_cross_specialization_cards(game_state):
    """Rule 5.4.3a: Card-pool includes specialization cards only legal due to meta-static."""
    spec_card = game_state.create_card(name="Other Hero Specialization", card_type="action")
    game_state.specialization_card = spec_card
    game_state.card_pool_was_legal_before = True  # legal because of meta-static


@when("the meta-static ability ceases to exist during the game")
def step_meta_static_ceases(game_state):
    """Rule 5.4.3a: Meta-static ability is lost during the game."""
    game_state.meta_static_ceased = True
    game_state.meta_static_ceased_result = game_state.simulate_meta_static_ceasing(
        game_state.meta_static_hero
    )


@then("the specialization cards in the card-pool remain legal")
def step_specialization_cards_remain_legal(game_state):
    """Rule 5.4.3a: Card-pool legality is not re-evaluated when meta-static ceases."""
    assert game_state.meta_static_ceased_result.card_pool_legality_unchanged is True, (
        "Specialization cards should remain legal even after meta-static ceases during game"
    )


@then("the legality of previously followed outside-game rules is not affected")
def step_outside_game_rules_not_retroactively_affected(game_state):
    """Rule 5.4.3a: Outside-game rules followed before meta-static ceased remain valid."""
    assert game_state.meta_static_ceased_result.outside_game_rules_retroactively_applied is False, (
        "Ceasing of meta-static should not retroactively affect outside-game rules already applied"
    )


# ----- 5.4.4a: Additional-cost ability -----

@given("a card with an additional-cost play-static ability requiring discard")
def step_card_with_additional_cost_discard(game_state):
    """Rule 5.4.4a: Card has play-static ability that adds a discard as additional cost."""
    card = game_state.create_card(name="Additional Cost Card", card_type="action")
    additional_cost_ability = game_state.create_additional_cost_ability(
        cost_type="discard", is_optional=False
    )
    game_state.additional_cost_card = card
    game_state.additional_cost_ability = additional_cost_ability


@given("a player with the card in hand")
def step_player_with_card_in_hand(game_state):
    """Rule 5.4.4a: Player has the additional-cost card in hand."""
    game_state.player.hand.add_card(game_state.additional_cost_card)


@when("the player attempts to play the card without paying the additional cost")
def step_player_plays_without_additional_cost(game_state):
    """Rule 5.4.4a: Player tries to play without the required additional cost."""
    game_state.play_result = game_state.attempt_play_with_additional_cost(
        card=game_state.additional_cost_card,
        additional_cost_ability=game_state.additional_cost_ability,
        paid_additional_cost=False,
    )


@then("the play attempt fails")
def step_play_attempt_fails(game_state):
    """Rule 5.4.4a: Play fails when mandatory additional cost is not paid."""
    assert game_state.play_result.success is False, (
        "Playing a card without its mandatory additional cost should fail"
    )


@then("the additional cost must be declared when playing the card")
def step_additional_cost_declared_at_play(game_state):
    """Rule 5.4.4a: Additional cost must be declared at the time of playing."""
    assert game_state.additional_cost_ability.must_be_declared_on_play is True, (
        "Additional-cost ability must be declared when playing the card (Rule 5.4.4a)"
    )


@given("a card with a mandatory additional-cost ability requiring resource payment")
def step_card_with_mandatory_additional_cost(game_state):
    """Rule 5.4.4a: Card has a mandatory additional cost (no 'may')."""
    card = game_state.create_card(name="Mandatory Additional Cost", card_type="action")
    ability = game_state.create_additional_cost_ability(
        cost_type="resource", is_optional=False
    )
    game_state.mandatory_cost_card = card
    game_state.mandatory_cost_ability = ability
    game_state.player.hand.add_card(card)


@when("the player attempts to play the card")
def step_player_attempts_to_play(game_state):
    """Rule 5.4.4a: Player attempts to play mandatory-additional-cost card."""
    game_state.mandatory_play_result = game_state.attempt_play_with_additional_cost(
        card=game_state.mandatory_cost_card,
        additional_cost_ability=game_state.mandatory_cost_ability,
        paid_additional_cost=False,
    )


@then("the additional cost is required and cannot be skipped")
def step_additional_cost_cannot_be_skipped(game_state):
    """Rule 5.4.4a: Mandatory additional cost cannot be skipped (no 'may')."""
    assert game_state.mandatory_cost_ability.is_optional is False, (
        "Mandatory additional cost should not be optional"
    )
    assert game_state.mandatory_play_result.success is False, (
        "Play should fail when mandatory additional cost is not paid"
    )


@given("a card with an optional additional-cost ability using \"may\"")
def step_card_with_optional_additional_cost(game_state):
    """Rule 5.4.4a: Card has optional additional-cost ability with 'may'."""
    card = game_state.create_card(name="Optional Additional Cost", card_type="action")
    ability = game_state.create_additional_cost_ability(
        cost_type="discard", is_optional=True
    )
    game_state.optional_cost_card = card
    game_state.optional_cost_ability = ability
    game_state.player.hand.add_card(card)


@when("the player plays the card without paying the optional additional cost")
def step_player_plays_without_optional_cost(game_state):
    """Rule 5.4.4a: Player skips the optional additional cost."""
    game_state.optional_play_result = game_state.attempt_play_with_additional_cost(
        card=game_state.optional_cost_card,
        additional_cost_ability=game_state.optional_cost_ability,
        paid_additional_cost=False,
    )


@then("the play succeeds without the optional cost")
def step_play_succeeds_without_optional_cost(game_state):
    """Rule 5.4.4a: Optional ('may') additional cost can be skipped; play still succeeds."""
    assert game_state.optional_play_result.success is True, (
        "Play should succeed when optional additional cost is not paid (it is optional)"
    )


# ----- 5.4.4b: Alternative-cost ability -----

@given("a card with a base cost of 3 resources")
def step_card_with_base_cost_3(game_state):
    """Rule 5.4.4b: Card has a base resource cost of 3."""
    card = game_state.create_card(name="Alternative Cost Card", card_type="action", cost=3)
    game_state.alt_cost_card = card


@given("the card has an alternative-cost ability to discard a card instead")
def step_card_has_alternative_cost_discard(game_state):
    """Rule 5.4.4b: Card has alternative-cost ability: discard a card instead of paying 3."""
    ability = game_state.create_alternative_cost_ability(
        replaces_base_cost=True,
        alternative_cost_type="discard",
    )
    game_state.alt_cost_ability = ability


@given("a player with the card in hand and insufficient resources")
def step_player_with_card_in_hand_insufficient_resources(game_state):
    """Rule 5.4.4b: Player has card but not enough resources to pay base cost."""
    game_state.player.hand.add_card(game_state.alt_cost_card)
    game_state.set_player_resource_points(game_state.player, 0)


@when("the player chooses to pay the alternative cost")
def step_player_pays_alternative_cost(game_state):
    """Rule 5.4.4b: Player declares the alternative cost when playing."""
    game_state.alt_play_result = game_state.attempt_play_with_alternative_cost(
        card=game_state.alt_cost_card,
        alternative_cost_ability=game_state.alt_cost_ability,
        use_alternative=True,
    )


@then("the card is played without paying the base resource cost")
def step_card_played_without_base_cost(game_state):
    """Rule 5.4.4b: Alternative cost replaces the base cost, no resources required."""
    assert game_state.alt_play_result.success is True, (
        "Card should be playable using the alternative cost even without resources"
    )
    assert game_state.alt_play_result.base_cost_paid is False, (
        "Base cost should not be paid when alternative cost is used"
    )


@given("a card with both an alternative-cost ability and an additional-cost ability")
def step_card_with_both_cost_abilities(game_state):
    """Rule 5.4.4b: Card has both an alternative-cost and an additional-cost ability."""
    card = game_state.create_card(name="Dual Cost Card", card_type="action", cost=2)
    alt_ability = game_state.create_alternative_cost_ability(
        replaces_base_cost=True, alternative_cost_type="discard"
    )
    add_ability = game_state.create_additional_cost_ability(
        cost_type="resource", is_optional=False
    )
    game_state.dual_cost_card = card
    game_state.dual_alt_ability = alt_ability
    game_state.dual_add_ability = add_ability
    game_state.player.hand.add_card(card)


@given("a player who chooses to pay the alternative cost")
def step_player_chooses_alternative_cost(game_state):
    """Rule 5.4.4b: Player declares the alternative cost."""
    game_state.using_alternative_cost = True


@when("the player plays the card using the alternative cost")
def step_player_plays_with_alternative_cost(game_state):
    """Rule 5.4.4b: Play is initiated with alternative cost declared."""
    game_state.dual_play_result = game_state.attempt_play_with_both_costs(
        card=game_state.dual_cost_card,
        alternative_cost_ability=game_state.dual_alt_ability,
        additional_cost_ability=game_state.dual_add_ability,
        use_alternative=True,
        paid_additional_cost=False,
    )


@then("the additional cost still applies")
def step_additional_cost_still_applies(game_state):
    """Rule 5.4.4b: Alternative cost does not affect additional costs."""
    assert game_state.dual_play_result.additional_cost_still_required is True, (
        "Additional cost must still apply even when alternative cost is chosen"
    )


@then("must also be paid alongside the alternative cost")
def step_additional_cost_must_be_paid_with_alternative(game_state):
    """Rule 5.4.4b: Both alternative cost and additional cost must be paid."""
    assert game_state.dual_play_result.success is False, (
        "Play should fail if additional cost is not paid even when alternative cost is used"
    )


@given("a card with an alternative-cost ability")
def step_card_with_alternative_cost_ability(game_state):
    """Rule 5.4.4b: Card has an alternative-cost ability."""
    card = game_state.create_card(name="Alt Cost Card", card_type="action", cost=2)
    ability = game_state.create_alternative_cost_ability(
        replaces_base_cost=True, alternative_cost_type="discard"
    )
    game_state.player.hand.add_card(card)
    game_state.decl_alt_card = card
    game_state.decl_alt_ability = ability


@when("the player begins to play the card")
def step_player_begins_to_play(game_state):
    """Rule 5.4.4b: Player initiates playing the card."""
    game_state.declaration_window_result = game_state.check_alternative_cost_declaration_window(
        game_state.decl_alt_card, game_state.decl_alt_ability
    )


@then("the alternative cost must be declared at that time if they wish to use it")
def step_alternative_cost_declared_at_play_time(game_state):
    """Rule 5.4.4b: Alternative cost must be declared when playing the card."""
    assert game_state.declaration_window_result.declaration_required_at_play is True, (
        "Alternative cost must be declared at the time the card is played"
    )


# ----- 5.4.4c: Triggered play-static effect -----

@given("a card with a play-static ability in the format \"EFFECT. When you do, ABILITIES\"")
def step_card_with_play_static_triggered(game_state):
    """Rule 5.4.4c: Card has a play-static ability with triggered 'When you do' format."""
    card = game_state.create_card(name="Play Static Triggered Card", card_type="action")
    ability = game_state.create_play_static_triggered_ability(
        trigger_format="when_you_do"
    )
    game_state.player.hand.add_card(card)
    game_state.play_static_trig_card = card
    game_state.play_static_trig_ability = ability


@given("a player who has met the condition of that play-static ability")
def step_player_meets_play_static_condition(game_state):
    """Rule 5.4.4c: Player meets the play-static trigger condition."""
    game_state.play_static_condition_met = True


@when("the player plays the card using the effect specified in the ability")
def step_player_plays_with_play_static_effect(game_state):
    """Rule 5.4.4c: Player plays the card using the effect from the play-static ability."""
    game_state.play_static_trig_result = game_state.play_card_with_play_static_ability(
        card=game_state.play_static_trig_card,
        ability=game_state.play_static_trig_ability,
        condition_met=game_state.play_static_condition_met,
    )


@then("the triggered effect triggers immediately")
def step_triggered_effect_triggers_immediately(game_state):
    """Rule 5.4.4c: Triggered effect triggers immediately when condition is met."""
    assert game_state.play_static_trig_result.triggered_immediately is True, (
        "Triggered play-static effect should trigger immediately when condition is met"
    )


@then("a triggered layer is placed on the stack")
def step_triggered_layer_placed_on_stack(game_state):
    """Rule 5.4.4c: A triggered layer appears on the stack from the triggered effect."""
    assert game_state.play_static_trig_result.triggered_layer_on_stack is True, (
        "A triggered layer should be placed on the stack for the triggered play-static effect"
    )


# ----- 5.4.4d: Conditional continuous play-static effect -----

@given("a card with a play-static ability in the format \"EFFECT. If you do, CONTINUOUSEFFECT\"")
def step_card_with_play_static_conditional_continuous(game_state):
    """Rule 5.4.4d: Card has a play-static ability with conditional continuous effect."""
    card = game_state.create_card(name="Conditional Continuous Card", card_type="action")
    ability = game_state.create_play_static_conditional_continuous_ability(
        condition_format="if_you_do"
    )
    game_state.player.hand.add_card(card)
    game_state.cond_cont_card = card
    game_state.cond_cont_ability = ability


@given("a player who has met the replacement condition of the play-static ability")
def step_player_meets_replacement_condition(game_state):
    """Rule 5.4.4d: Player meets the 'If you do' replacement condition."""
    game_state.replacement_condition_met = True


@when("the player plays the card using the specified effect")
def step_player_plays_with_specified_effect(game_state):
    """Rule 5.4.4d: Player plays the card using the conditional continuous effect."""
    game_state.cond_cont_result = game_state.play_card_with_play_static_ability(
        card=game_state.cond_cont_card,
        ability=game_state.cond_cont_ability,
        condition_met=game_state.replacement_condition_met,
    )


@then("the conditional continuous effect is generated at the time the condition is met")
def step_conditional_continuous_effect_generated_at_condition(game_state):
    """Rule 5.4.4d: Conditional continuous effect generated at the moment condition is met."""
    assert game_state.cond_cont_result.continuous_effect_generated is True, (
        "Conditional continuous effect should be generated when 'If you do' condition is met"
    )
    assert game_state.cond_cont_result.effect_generated_at_condition_time is True, (
        "Effect should be generated at the time the condition is met"
    )


# ----- 5.4.5: Property-static ability -----

@given("a card with a property-static ability defining its power based on game state")
def step_card_with_property_static(game_state):
    """Rule 5.4.5: Card has property-static ability defining power dynamically."""
    card = game_state.create_card(name="Mutated Mass", card_type="action")
    game_state.property_static_card = card
    game_state.property_static_formula = "twice_pitch_zone_different_costs"


@given("the game state has 3 cards of different costs in the pitch zone")
def step_game_state_3_pitch_cards(game_state):
    """Rule 5.4.5: Pitch zone has 3 cards with different costs."""
    game_state.pitch_zone_card_count = 3
    for i in range(3):
        pitch_card = game_state.create_card(
            name=f"Pitch Card {i}", card_type="action", cost=i
        )
        game_state.player.pitch_zone.add_card(pitch_card)


@when("I check the card's power value")
def step_check_power_value(game_state):
    """Rule 5.4.5: Check the power value of a property-static card."""
    game_state.power_check_result = game_state.get_property_static_value(
        game_state.property_static_card,
        property_name="power",
        formula=game_state.property_static_formula,
    )


@then("the power is calculated dynamically by the property-static ability")
def step_power_calculated_dynamically(game_state):
    """Rule 5.4.5: Property-static ability defines power dynamically."""
    assert game_state.power_check_result.is_dynamically_calculated is True, (
        "Property-static ability should define power dynamically based on game state"
    )


@then("the value matches what the static ability formula specifies")
def step_value_matches_formula(game_state):
    """Rule 5.4.5: Calculated power matches the property-static formula."""
    # 3 cards with different costs => power = twice 3 = 6
    assert game_state.power_check_result.value == 6, (
        "Power should be twice the number of pitch zone cards with different costs (3*2=6)"
    )


@given("a card with a property-static ability defining power as twice the pitch zone count")
def step_card_with_dynamic_power_property(game_state):
    """Rule 5.4.5: Card has a property-static ability for dynamic power."""
    card = game_state.create_card(name="Dynamic Power Card", card_type="action")
    game_state.dynamic_power_card = card
    game_state.property_static_formula = "twice_pitch_count"


@given("the pitch zone has 2 cards")
def step_pitch_zone_has_2_cards(game_state):
    """Rule 5.4.5: Pitch zone starts with 2 cards."""
    for i in range(2):
        pitch_card = game_state.create_card(name=f"Pitch {i}", card_type="action", cost=i)
        game_state.player.pitch_zone.add_card(pitch_card)
    game_state.initial_pitch_count = 2


@when("a third card is added to the pitch zone")
def step_third_card_added_to_pitch(game_state):
    """Rule 5.4.5: A third card is added to the pitch zone."""
    third_card = game_state.create_card(name="Pitch 3", card_type="action", cost=5)
    game_state.player.pitch_zone.add_card(third_card)
    game_state.new_pitch_count = 3


@then("the card's power updates to reflect the new game state")
def step_power_updates_for_new_state(game_state):
    """Rule 5.4.5: Property-static power value updates when game state changes."""
    result = game_state.get_property_static_value(
        game_state.dynamic_power_card,
        property_name="power",
        formula=game_state.property_static_formula,
    )
    # Static continuous effects with variable values update dynamically (Rule 6.2.3b)
    assert result.value == game_state.new_pitch_count * 2, (
        "Property-static value should update when game state changes"
    )


# ----- 5.4.5a: Property-static functions anywhere -----

@given("a card with a property-static ability")
def step_card_with_property_static_ability(game_state):
    """Rule 5.4.5a: Card has a property-static ability."""
    card = game_state.create_card(name="Property Static Anywhere", card_type="action")
    game_state.prop_static_card = card


@when("the card is in the hand zone")
def step_card_is_in_hand_zone(game_state):
    """Rule 5.4.5a: Card with property-static is in the hand zone."""
    game_state.player.hand.add_card(game_state.prop_static_card)
    game_state.prop_static_location = "hand"


@then("the property-static ability is functional")
def step_property_static_functional_in_hand(game_state):
    """Rule 5.4.5a: Property-static ability is functional in the hand zone."""
    result = game_state.check_property_static_functional(
        game_state.prop_static_card,
        location=game_state.prop_static_location,
    )
    assert result.is_functional is True, (
        "Property-static ability should be functional anywhere, including in hand"
    )


@then("the defined property value is applied")
def step_property_value_applied(game_state):
    """Rule 5.4.5a: Property value defined by static ability is applied."""
    result = game_state.check_property_static_functional(
        game_state.prop_static_card,
        location=game_state.prop_static_location,
    )
    assert result.property_value_applied is True, (
        "Property value should be applied wherever the card is"
    )


@when("evaluating the card outside of a game context")
def step_evaluate_card_outside_game(game_state):
    """Rule 5.4.5a: Evaluate property-static ability outside of a game."""
    game_state.prop_static_location = "outside_game"


@then("the property-static ability is still functional")
def step_property_static_functional_outside_game(game_state):
    """Rule 5.4.5a: Property-static ability is functional outside the game."""
    result = game_state.check_property_static_functional(
        game_state.prop_static_card,
        location=game_state.prop_static_location,
    )
    assert result.is_functional is True, (
        "Property-static ability should be functional outside the game (Rule 5.4.5a)"
    )


@then("the property it defines is recognized")
def step_property_defined_recognized(game_state):
    """Rule 5.4.5a: Property defined by property-static ability is recognized outside game."""
    result = game_state.check_property_static_functional(
        game_state.prop_static_card,
        location=game_state.prop_static_location,
    )
    assert result.property_recognized is True, (
        "Property defined by property-static ability should be recognized outside the game"
    )


# ----- 5.4.6: Triggered-static ability -----

@given("a card in the arena with a triggered-static ability")
def step_card_in_arena_with_triggered_static(game_state):
    """Rule 5.4.6: Card has a triggered-static ability and is in the arena."""
    card = game_state.create_card(name="Triggered Static Card", card_type="permanent")
    game_state.play_card_to_arena(card)
    game_state.trig_static_card = card
    game_state.trig_static_ability = game_state.create_triggered_static_ability(
        source=card, trigger_event="any"
    )


@given("the trigger condition of the triggered-static ability is met")
def step_trigger_condition_met(game_state):
    """Rule 5.4.6: Trigger event for the triggered-static ability occurs."""
    game_state.trigger_event_occurred = True


@when("the triggered effect is generated")
def step_triggered_effect_generated(game_state):
    """Rule 5.4.6: Triggered effect from triggered-static ability is generated."""
    game_state.trig_static_result = game_state.generate_triggered_static_effect(
        card=game_state.trig_static_card,
        ability=game_state.trig_static_ability,
        trigger_event_occurred=game_state.trigger_event_occurred,
    )


@then("exactly one triggered layer is created from the triggered-static ability")
def step_exactly_one_triggered_layer_created(game_state):
    """Rule 5.4.6: Triggered-static ability generates exactly one triggered effect."""
    assert game_state.trig_static_result.triggered_layer_count == 1, (
        "Triggered-static ability should generate exactly one triggered effect/layer"
    )


@then("the triggered layer is placed on the stack")
def step_triggered_layer_placed(game_state):
    """Rule 5.4.6: The triggered layer from triggered-static ability goes onto the stack."""
    assert game_state.trig_static_result.layer_on_stack is True, (
        "Triggered layer from triggered-static ability should be placed on the stack"
    )


# ----- 5.4.6a: Source ceases to exist from triggering event -----

@given("a card with a triggered-static ability whose trigger condition is its own destruction")
def step_card_with_self_destruction_trigger(game_state):
    """Rule 5.4.6a: Card triggers when it itself is destroyed."""
    card = game_state.create_card(name="Merciful Retribution", card_type="permanent")
    ability = game_state.create_triggered_static_ability(
        source=card, trigger_event="self_destroyed"
    )
    game_state.self_destroy_card = card
    game_state.self_destroy_ability = ability


@given("the card is in the arena and its triggered-static ability is functional")
def step_card_in_arena_and_trig_functional(game_state):
    """Rule 5.4.6a: Card is in arena with functional triggered-static ability."""
    game_state.play_card_to_arena(game_state.self_destroy_card)
    result = game_state.get_static_ability_info(
        game_state.self_destroy_card, ability_type="triggered_static"
    )
    assert result.is_functional is True, (
        "Triggered-static ability should be functional while card is in arena"
    )


@when("the card is destroyed")
def step_card_is_destroyed(game_state):
    """Rule 5.4.6a: The card is destroyed, which is also its trigger event."""
    game_state.destroy_result = game_state.destroy_card(game_state.self_destroy_card)


@then("the triggered effect still triggers")
def step_triggered_effect_still_triggers(game_state):
    """Rule 5.4.6a: Triggered effect triggers even though source ceased to exist from the event."""
    assert game_state.destroy_result.triggered_effect_fired is True, (
        "Triggered-static effect should trigger even when source ceases from the triggering event"
    )


@then("a triggered layer is placed on the stack for the effect")
def step_triggered_layer_placed_for_self_destroy(game_state):
    """Rule 5.4.6a: Triggered layer is placed on the stack for the triggered effect."""
    assert game_state.destroy_result.triggered_layer_on_stack is True, (
        "A triggered layer should be placed on the stack even when source was destroyed"
    )


@given("a card with a triggered-static ability that is currently not functional")
def step_card_with_nonfunctional_triggered_static(game_state):
    """Rule 5.4.6a: Card's triggered-static ability is not functional (e.g., card is in hand)."""
    card = game_state.create_card(name="Non-Functional Trigger Card", card_type="action")
    ability = game_state.create_triggered_static_ability(
        source=card, trigger_event="some_event"
    )
    # Card is in hand, not in arena, so triggered-static is not functional
    game_state.player.hand.add_card(card)
    game_state.nonfunctional_trig_card = card
    game_state.nonfunctional_trig_ability = ability


@when("the trigger event occurs")
def step_trigger_event_occurs(game_state):
    """Rule 5.4.6a: Trigger event for the non-functional triggered-static occurs."""
    game_state.nonfunctional_trig_result = game_state.generate_triggered_static_effect(
        card=game_state.nonfunctional_trig_card,
        ability=game_state.nonfunctional_trig_ability,
        trigger_event_occurred=True,
    )


@then("the triggered effect does not trigger")
def step_triggered_effect_does_not_trigger(game_state):
    """Rule 5.4.6a: Triggered effect does NOT trigger when ability was not functional."""
    assert game_state.nonfunctional_trig_result.triggered_layer_count == 0, (
        "Triggered-static should NOT trigger if ability was not functional before the event"
    )


@then("no triggered layer is placed on the stack")
def step_no_triggered_layer_placed(game_state):
    """Rule 5.4.6a: No triggered layer is placed when triggered-static was non-functional."""
    assert game_state.nonfunctional_trig_result.layer_on_stack is False, (
        "No triggered layer should be placed when triggered-static was not functional"
    )


# ----- 5.4.7: While-static ability -----

@given("a card with a while-static ability requiring it to be defending")
def step_card_with_while_static_defending(game_state):
    """Rule 5.4.7: Card has a while-static ability 'While this is defending...'."""
    card = game_state.create_card(name="Yinti Yanti", card_type="action")
    ability = game_state.create_while_static_ability(
        while_condition="is_defending",
        explicitly_private=False,
    )
    game_state.while_static_card = card
    game_state.while_static_ability = ability


@given("an aura controlled by the same player")
def step_aura_controlled_by_player(game_state):
    """Rule 5.4.7: An aura is in the arena under the same player's control."""
    aura = game_state.create_card(name="Test Aura", card_type="permanent")
    game_state.play_card_to_arena(aura)
    game_state.test_aura = aura


@when("the card becomes a defending card")
def step_card_becomes_defending(game_state):
    """Rule 5.4.7: The card is put into a defending position."""
    game_state.while_static_result = game_state.put_card_in_defending_position(
        card=game_state.while_static_card,
        ability=game_state.while_static_ability,
    )


@then("the while-static ability becomes functional")
def step_while_static_becomes_functional(game_state):
    """Rule 5.4.7: While-static becomes functional when while-condition is met."""
    assert game_state.while_static_result.ability_functional is True, (
        "While-static ability should be functional when while-condition is met"
    )


@then("the effect from the while-static ability applies")
def step_while_static_effect_applies(game_state):
    """Rule 5.4.7: Effect from while-static ability is applied when functional."""
    assert game_state.while_static_result.effect_applied is True, (
        "Effect from while-static ability should apply when ability is functional"
    )


@when("the card is not defending")
def step_card_is_not_defending(game_state):
    """Rule 5.4.7: Card is not in a defending position."""
    game_state.while_not_defending_result = game_state.check_while_static_when_not_defending(
        card=game_state.while_static_card,
        ability=game_state.while_static_ability,
    )


@then("the while-static ability is not functional")
def step_while_static_not_functional(game_state):
    """Rule 5.4.7: While-static ability is not functional when condition is not met."""
    assert game_state.while_not_defending_result.ability_functional is False, (
        "While-static ability should NOT be functional when while-condition is not met"
    )


@then("the effect from the while-static ability does not apply")
def step_while_static_effect_does_not_apply(game_state):
    """Rule 5.4.7: Effect from while-static is not applied when not functional."""
    assert game_state.while_not_defending_result.effect_applied is False, (
        "Effect from while-static ability should NOT apply when ability is not functional"
    )


# ----- 5.4.7a: Public/private source functional rules -----

@given("a card with a while-static ability for a condition in a public zone")
def step_card_while_static_public_zone(game_state):
    """Rule 5.4.7a: While-static condition references a normally-public zone."""
    card = game_state.create_card(name="Public Zone While Static", card_type="action")
    ability = game_state.create_while_static_ability(
        while_condition="in_arena",
        explicitly_private=False,
    )
    game_state.public_zone_while_card = card
    game_state.public_zone_while_ability = ability


@given("the source card is public")
def step_source_card_is_public(game_state):
    """Rule 5.4.7a: Source card is in a public state."""
    game_state.source_is_public = True


@when("the while-condition is met")
def step_while_condition_is_met(game_state):
    """Rule 5.4.7a: The while-condition for the ability is met."""
    game_state.public_zone_result = game_state.check_while_static_functionality(
        card=game_state.public_zone_while_card,
        ability=game_state.public_zone_while_ability,
        source_is_public=game_state.source_is_public,
        condition_met=True,
    )


@then("the while-static ability is functional")
def step_while_static_is_functional(game_state):
    """Rule 5.4.7a: While-static is functional when condition met and source is public."""
    assert game_state.public_zone_result.is_functional is True, (
        "While-static ability should be functional when condition is met and source is public"
    )


@given("a card with a while-static ability that explicitly specifies \"while this is in your hand\"")
def step_card_while_static_explicit_private(game_state):
    """Rule 5.4.7a: While-static explicitly specifies a private zone (hand)."""
    card = game_state.create_card(name="Heave Card", card_type="action")
    ability = game_state.create_while_static_ability(
        while_condition="in_hand",
        explicitly_private=True,  # explicitly specifies the source is in hand (private zone)
    )
    game_state.explicit_private_card = card
    game_state.explicit_private_ability = ability


@given("the card is face-down in the player's hand")
def step_card_face_down_in_hand(game_state):
    """Rule 5.4.7a: Card is private in the hand zone."""
    game_state.player.hand.add_card(game_state.explicit_private_card)
    game_state.explicit_private_source_public = False  # face-down = private


@when("the while-condition is met")
def step_while_condition_met_private(game_state):
    """Rule 5.4.7a: While-condition (in hand) is met."""
    game_state.explicit_private_result = game_state.check_while_static_functionality(
        card=game_state.explicit_private_card,
        ability=game_state.explicit_private_ability,
        source_is_public=game_state.explicit_private_source_public,
        condition_met=True,
    )


@then("the while-static ability is functional even though the source is private")
def step_while_static_functional_even_private(game_state):
    """Rule 5.4.7a: Explicitly-private while-static is functional even when source is private."""
    assert game_state.explicit_private_result.is_functional is True, (
        "While-static explicitly referencing a private zone should be functional even when source is private"
    )


@given("a card with a while-static ability referencing a normally-public zone like banished")
def step_card_while_static_banished_zone(game_state):
    """Rule 5.4.7a: While-static references banished zone (public by default)."""
    card = game_state.create_card(name="Blood Debt Card", card_type="action")
    ability = game_state.create_while_static_ability(
        while_condition="in_banished",
        explicitly_private=False,  # banished is public by default
    )
    game_state.banished_while_card = card
    game_state.banished_while_ability = ability


@given("the card is private in the banished zone")
def step_card_private_in_banished(game_state):
    """Rule 5.4.7a: Card is private (face-down) even in normally-public banished zone."""
    game_state.banished_source_is_public = False  # private/face-down


@when("the while-condition would otherwise be met")
def step_while_condition_would_be_met(game_state):
    """Rule 5.4.7a: The while-condition is met but source is private."""
    game_state.banished_private_result = game_state.check_while_static_functionality(
        card=game_state.banished_while_card,
        ability=game_state.banished_while_ability,
        source_is_public=game_state.banished_source_is_public,
        condition_met=True,
    )


@then("the while-static ability is not functional because the source is private")
def step_while_static_not_functional_private_banished(game_state):
    """Rule 5.4.7a: While-static for public zone is NOT functional when source is private."""
    assert game_state.banished_private_result.is_functional is False, (
        "While-static for public zone should NOT be functional when source is private"
    )


@then("the ability does not generate its effect")
def step_while_static_no_effect_when_private(game_state):
    """Rule 5.4.7a: No effect generated when while-static is non-functional due to privacy."""
    assert game_state.banished_private_result.effect_generated is False, (
        "While-static ability should not generate its effect when non-functional"
    )


# ----- 5.4.7b: Hidden triggered ability -----

@given("a card with a hidden triggered ability")
def step_card_with_hidden_triggered_ability(game_state):
    """Rule 5.4.7b: Card has a hidden triggered ability (while-static + triggered-static, private)."""
    card = game_state.create_card(name="The Librarian", card_type="permanent")
    ability = game_state.create_hidden_triggered_ability(
        while_condition="face_down_in_arsenal",
        trigger_event="start_of_turn",
    )
    game_state.hidden_trig_card = card
    game_state.hidden_trig_ability = ability


@given("the card is face-down in arsenal")
def step_card_face_down_in_arsenal(game_state):
    """Rule 5.4.7b: Card is face-down (private) in arsenal."""
    game_state.player.arsenal_zone.add_card(game_state.hidden_trig_card)
    game_state.hidden_trig_card_is_public = False  # face-down


@when("the trigger condition of the hidden triggered ability is met")
def step_hidden_triggered_condition_met(game_state):
    """Rule 5.4.7b: Start of turn event occurs while card is face-down in arsenal."""
    game_state.hidden_trig_event_result = game_state.trigger_hidden_triggered_ability(
        card=game_state.hidden_trig_card,
        ability=game_state.hidden_trig_ability,
    )


@then("the owner may decide to trigger the effect")
def step_owner_may_decide_to_trigger(game_state):
    """Rule 5.4.7b: Owner has the option to trigger or not trigger the hidden ability."""
    assert game_state.hidden_trig_event_result.owner_may_choose is True, (
        "Owner should be able to decide whether to trigger the hidden triggered ability"
    )


@then("if the owner triggers it, the source becomes public")
def step_if_owner_triggers_source_becomes_public(game_state):
    """Rule 5.4.7b: If owner triggers, source becomes public."""
    result = game_state.owner_triggers_hidden_ability(
        card=game_state.hidden_trig_card,
        ability=game_state.hidden_trig_ability,
    )
    assert result.source_became_public is True, (
        "Source should become public when owner decides to trigger hidden triggered ability"
    )


@given("a card with a hidden triggered ability face-down in arsenal")
def step_hidden_triggered_card_in_arsenal(game_state):
    """Rule 5.4.7b: Card with hidden triggered ability is face-down in arsenal."""
    card = game_state.create_card(name="The Librarian", card_type="permanent")
    ability = game_state.create_hidden_triggered_ability(
        while_condition="face_down_in_arsenal",
        trigger_event="start_of_turn",
    )
    game_state.player.arsenal_zone.add_card(card)
    game_state.hidden_card2 = card
    game_state.hidden_ability2 = ability
    game_state.hidden_card2_is_public = False


@when("the owner decides to trigger the hidden triggered ability")
def step_owner_decides_to_trigger(game_state):
    """Rule 5.4.7b: Owner elects to trigger the hidden ability."""
    game_state.owner_trigger_result = game_state.owner_triggers_hidden_ability(
        card=game_state.hidden_card2,
        ability=game_state.hidden_ability2,
    )


@then("the card becomes public immediately")
def step_card_becomes_public_immediately(game_state):
    """Rule 5.4.7b: Source card becomes public immediately when hidden ability is triggered."""
    assert game_state.owner_trigger_result.source_became_public is True, (
        "Card should become public immediately when owner triggers hidden triggered ability"
    )


@then("a triggered layer is placed on the stack")
def step_triggered_layer_placed_for_hidden(game_state):
    """Rule 5.4.7b: A triggered layer is placed on the stack for the hidden triggered effect."""
    assert game_state.owner_trigger_result.triggered_layer_on_stack is True, (
        "Triggered layer should be placed on the stack when hidden triggered ability is triggered"
    )


@given("the owner triggered the hidden triggered ability making the source public")
def step_owner_triggered_and_source_is_public(game_state):
    """Rule 5.4.7b: Owner has already triggered hidden ability; source is now public."""
    card = game_state.create_card(name="The Librarian", card_type="permanent")
    ability = game_state.create_hidden_triggered_ability(
        while_condition="face_down_in_arsenal",
        trigger_event="start_of_turn",
    )
    game_state.player.arsenal_zone.add_card(card)
    game_state.hidden_card3 = card
    game_state.hidden_ability3 = ability
    # Simulate owner having already triggered, source is now public
    trigger_result = game_state.owner_triggers_hidden_ability(card, ability)
    game_state.hidden_layer3 = trigger_result.triggered_layer


@when("the triggered layer resolves")
def step_triggered_layer_resolves(game_state):
    """Rule 5.4.7b: The triggered layer from the hidden ability resolves."""
    game_state.hidden_resolve_result = game_state.resolve_hidden_triggered_layer(
        card=game_state.hidden_card3,
        triggered_layer=game_state.hidden_layer3,
    )


@then("the source returns to being private")
def step_source_returns_to_private(game_state):
    """Rule 5.4.7b: Source returns to private after triggered-layer resolves."""
    assert game_state.hidden_resolve_result.source_returned_to_private is True, (
        "Source should return to private after hidden triggered-layer resolves"
    )


@then("the card is no longer public")
def step_card_no_longer_public(game_state):
    """Rule 5.4.7b: Card reverts to private (face-down) state after resolution."""
    assert game_state.hidden_resolve_result.card_is_public is False, (
        "Card should no longer be public after hidden triggered-layer has resolved"
    )


# ===== Fixtures =====

@pytest.fixture
def game_state():
    """
    Fixture providing game state for Section 5.4 static ability tests.

    Uses BDDGameState which integrates with the real engine.
    Reference: Rule 5.4 - Static Abilities
    """
    from tests.bdd_helpers import BDDGameState

    state = BDDGameState()
    return state
