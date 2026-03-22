"""
Step definitions for Section 6.4: Replacement Effects
Reference: Flesh and Blood Comprehensive Rules Section 6.4

This module implements behavioral tests for replacement effects, which replace
an event with a modified event. Includes prevention effects, self-replacement,
identity-replacement, standard-replacement, and outcome-replacement effects.

Engine Features Needed for Section 6.4:
- [ ] ReplacementEffect base class with .is_active(event) -> bool (Rule 6.4.2)
- [ ] ReplacementEffect.apply(event) -> ModifiedEvent (Rule 6.4.1)
- [ ] ReplacementEffect.condition -> Callable (Rule 6.4.2)
- [ ] ReplacementEffect.variable_values recalculated each time effect could apply (Rule 6.4.2a)
- [ ] ReplacementEffect cannot retroactively apply to past events (Rule 6.4.3)
- [ ] ReplacementEffect chaining: effect A can modify event already modified by effect B (Rule 6.4.4)
- [ ] ReplacementEffect.applied_to_original_event: tracked to prevent double-apply (Rule 6.4.5)
- [ ] ModifiedEvent may activate new replacement effects not active for original event (Rule 6.4.6)
- [ ] SelfReplacementEffect: applies to event of preceding effect on same source (Rule 6.4.7)
- [ ] SelfReplacementEffect.condition evaluated at time preceding effect is generated (Rule 6.4.7b)
- [ ] IdentityReplacementEffect: applied when object enters arena (Rule 6.4.8)
- [ ] IdentityReplacementEffect modifications define copyable properties (Rule 6.4.8a)
- [ ] StandardReplacementEffect: continuous effect with condition/modification (Rule 6.4.9)
- [ ] PreventionEffect: replaces damage event with modified event (Rule 6.4.10)
- [ ] PreventionEffect.prevention_amount reduced by 1 per damage prevented (Rule 6.4.10a)
- [ ] PreventionEffect.prevention_amount defaults to damage in event if unspecified (Rule 6.4.10b)
- [ ] PreventionEffect.damage_type: None means all types (Rule 6.4.10c)
- [ ] PreventionEffect.source: None means all sources (Rule 6.4.10d)
- [ ] PreventionEffect.shielded_object: None means all objects from source (Rule 6.4.10e)
- [ ] PreventionEffect controller declares per-point prevention for multi-type/multi-target (Rule 6.4.10f)
- [ ] PreventionEffect.prevention_amount reduced by modifier before application (Rule 6.4.10g)
- [ ] PreventionEffect applies once even if damage cannot be prevented (Rule 6.4.10h)
- [ ] FixedPreventionEffect: applies to one event, remaining prevention discarded (Rule 6.4.10i)
- [ ] ShieldingPreventionEffect: applies across events until prevention_amount reaches 0 (Rule 6.4.10j)
- [ ] OutcomeReplacementEffect: replaces outcome of an event with another event (Rule 6.4.11)

Current status: Tests written, Engine pending
"""

import pytest
from pytest_bdd import scenario, given, when, then, parsers


# ===== Scenarios =====


@scenario(
    "../features/section_6_4_replacement_effects.feature",
    "A replacement effect replaces an event with a modified event",
)
def test_replacement_effect_replaces_event():
    """Rule 6.4.1: A replacement effect replaces an event with a modified event."""
    pass


@scenario(
    "../features/section_6_4_replacement_effects.feature",
    "A sub-event occurs before the original event when a replacement effect is applied",
)
def test_sub_event_occurs_before_original():
    """Rule 6.4.1a: Sub-events occur before the original event when replacement is applied."""
    pass


@scenario(
    "../features/section_6_4_replacement_effects.feature",
    "A replacement effect is only active when its triggering event is about to occur",
)
def test_replacement_effect_not_active_for_wrong_event():
    """Rule 6.4.2: Replacement effect is inactive when its condition is not met."""
    pass


@scenario(
    "../features/section_6_4_replacement_effects.feature",
    "A replacement effect becomes active when its triggering event is about to occur",
)
def test_replacement_effect_active_for_matching_event():
    """Rule 6.4.2: Replacement effect is active when its condition is met."""
    pass


@scenario(
    "../features/section_6_4_replacement_effects.feature",
    "Variable values in a replacement effect are recalculated each time it could apply",
)
def test_variable_values_recalculated_each_time():
    """Rule 6.4.2a: Variable values are recalculated each time the effect could apply."""
    pass


@scenario(
    "../features/section_6_4_replacement_effects.feature",
    "A replacement effect created after an event does not retroactively replace it",
)
def test_replacement_effect_not_retroactive():
    """Rule 6.4.3: Replacement effects do not apply retroactively."""
    pass


@scenario(
    "../features/section_6_4_replacement_effects.feature",
    "A replacement effect can replace an event already modified by another replacement effect",
)
def test_replacement_effect_can_replace_modified_event():
    """Rule 6.4.4: Replacement effects can be chained."""
    pass


@scenario(
    "../features/section_6_4_replacement_effects.feature",
    "A replacement effect cannot replace the same event more than once per original event",
)
def test_replacement_effect_cannot_replace_own_modified_event():
    """Rule 6.4.5: A replacement effect can only replace an event once per original event."""
    pass


@scenario(
    "../features/section_6_4_replacement_effects.feature",
    "A modified event can trigger replacement effects that the original event would not have",
)
def test_modified_event_can_trigger_new_effects():
    """Rule 6.4.6: Modified events may activate replacement effects inactive for the original."""
    pass


@scenario(
    "../features/section_6_4_replacement_effects.feature",
    "A self-replacement effect replaces the event of its preceding effect when condition is met",
)
def test_self_replacement_applies_when_condition_met():
    """Rule 6.4.7: Self-replacement replaces the preceding effect's event when condition is met."""
    pass


@scenario(
    "../features/section_6_4_replacement_effects.feature",
    "A self-replacement effect does not apply when its condition is not met",
)
def test_self_replacement_does_not_apply_without_condition():
    """Rule 6.4.7: Self-replacement does not apply when its condition is not met."""
    pass


@scenario(
    "../features/section_6_4_replacement_effects.feature",
    "A self-replacement effect only modifies the event of its own preceding effect",
)
def test_self_replacement_only_applies_to_own_preceding_effect():
    """Rule 6.4.7a: Self-replacement does not modify events from other sources."""
    pass


@scenario(
    "../features/section_6_4_replacement_effects.feature",
    "Self-replacement condition with undetermined parameters is evaluated when parameters are determined",
)
def test_self_replacement_condition_evaluated_when_parameters_determined():
    """Rule 6.4.7b: Self-replacement condition with undetermined parameters is evaluated later."""
    pass


@scenario(
    "../features/section_6_4_replacement_effects.feature",
    "An identity-replacement effect modifies how an object enters the arena",
)
def test_identity_replacement_modifies_arena_entry():
    """Rule 6.4.8: Identity-replacement effects modify how objects enter the arena."""
    pass


@scenario(
    "../features/section_6_4_replacement_effects.feature",
    "An identity-replacement effect that modifies object properties defines copyable properties",
)
def test_identity_replacement_defines_copyable_properties():
    """Rule 6.4.8a: Identity-replacement modifications define copyable properties."""
    pass


@scenario(
    "../features/section_6_4_replacement_effects.feature",
    "A standard-replacement effect applies when its condition is met",
)
def test_standard_replacement_applies_when_condition_met():
    """Rule 6.4.9: Standard-replacement effect applies when condition is met."""
    pass


@scenario(
    "../features/section_6_4_replacement_effects.feature",
    "A prevention effect reduces the damage dealt by its prevention amount",
)
def test_prevention_effect_reduces_damage():
    """Rule 6.4.10 / 6.4.10a: Prevention effect reduces damage by prevention amount."""
    pass


@scenario(
    "../features/section_6_4_replacement_effects.feature",
    "A prevention effect without a specified amount prevents all damage in the event",
)
def test_prevention_amount_defaults_to_event_damage():
    """Rule 6.4.10b: Unspecified prevention amount equals the damage in the event."""
    pass


@scenario(
    "../features/section_6_4_replacement_effects.feature",
    "A prevention effect with no specified type prevents all damage types",
)
def test_prevention_no_type_prevents_all():
    """Rule 6.4.10c: Prevention effect with no type prevents all damage types."""
    pass


@scenario(
    "../features/section_6_4_replacement_effects.feature",
    "A prevention effect with a specified type only prevents that damage type",
)
def test_prevention_specified_type_only():
    """Rule 6.4.10c: Prevention effect with specified type only prevents that type."""
    pass


@scenario(
    "../features/section_6_4_replacement_effects.feature",
    "An effect that decreases a prevention effect's amount is applied before the prevention",
)
def test_prevention_amount_reduced_before_application():
    """Rule 6.4.10g: Effects that decrease prevention are applied before the prevention effect."""
    pass


@scenario(
    "../features/section_6_4_replacement_effects.feature",
    "When damage cannot be prevented the prevention effect still applies once but prevention amount is not reduced",
)
def test_cannot_prevent_still_applies_effect():
    """Rule 6.4.10h: When damage cannot be prevented, the prevention effect applies but amount is not reduced."""
    pass


@scenario(
    "../features/section_6_4_replacement_effects.feature",
    "A fixed-prevention effect prevents damage from one triggering event only",
)
def test_fixed_prevention_only_one_event():
    """Rule 6.4.10i: Fixed-prevention effect applies to one event only."""
    pass


@scenario(
    "../features/section_6_4_replacement_effects.feature",
    "A shielding-prevention effect applies across multiple damage events until exhausted",
)
def test_shielding_prevention_applies_across_multiple_events():
    """Rule 6.4.10j: Shielding-prevention effect applies to multiple events until exhausted."""
    pass


@scenario(
    "../features/section_6_4_replacement_effects.feature",
    "An outcome-replacement effect replaces the outcome of an event with another event",
)
def test_outcome_replacement_replaces_event_outcome():
    """Rule 6.4.11: Outcome-replacement effects replace the outcome of an event."""
    pass


# ===== Step Definitions =====


# ----- Rule 6.4.1: Basic replacement effect -----

@given("a replacement effect exists that replaces drawing 2 cards with drawing 3 cards")
def replacement_effect_draw_2_to_3(game_state):
    """Rule 6.4.1: Set up a replacement effect that modifies a draw event."""
    game_state.replacement_effect = game_state.create_replacement_effect(
        replaces="draw 2 cards",
        with_effect="draw 3 cards",
    )
    game_state.replacement_effect_condition_met = True


@given("the condition for the replacement is met")
def replacement_condition_met(game_state):
    """Rule 6.4.2: The replacement condition is satisfied."""
    game_state.replacement_effect_condition_met = True


@when("the event of drawing 2 cards is about to occur")
def draw_2_cards_event_about_to_occur(game_state):
    """Rule 6.4.1: Trigger the event that would be replaced."""
    game_state.pending_event = {"type": "draw", "amount": 2}
    game_state.apply_result = game_state.apply_replacement_effects(
        game_state.pending_event
    )


@then("the replacement effect replaces the event")
def replacement_effect_replaces_event(game_state):
    """Rule 6.4.1: The replacement effect was applied."""
    assert game_state.apply_result is not None
    assert game_state.apply_result.was_replaced is True


@then("the modified event of drawing 3 cards occurs instead")
def modified_event_draw_3_occurs(game_state):
    """Rule 6.4.1: The modified event (draw 3) occurs."""
    assert game_state.apply_result.modified_event is not None
    assert game_state.apply_result.modified_event.get("amount") == 3


@then("the original event of drawing 2 cards does not occur")
def original_event_does_not_occur(game_state):
    """Rule 6.4.1: The original event (draw 2) does not occur."""
    assert game_state.apply_result.original_event_occurred is False


# ----- Rule 6.4.1a: Sub-events -----

@given("a replacement effect with a sub-event exists")
def replacement_effect_with_sub_event(game_state):
    """Rule 6.4.1a: A replacement effect that produces a sub-event (e.g., Ward)."""
    game_state.replacement_effect = game_state.create_replacement_effect_with_sub_event(
        sub_event="destroy_source",
        replaces="damage",
        with_effect="prevent_damage",
    )


@when("the replacement effect is applied to an event")
def replacement_effect_applied_to_event(game_state):
    """Rule 6.4.1a: Apply the replacement effect to an event."""
    game_state.pending_event = {"type": "damage", "amount": 1}
    game_state.apply_result = game_state.apply_replacement_effects_with_sub_events(
        game_state.pending_event
    )


@then("the sub-event occurs first")
def sub_event_occurs_first(game_state):
    """Rule 6.4.1a: The sub-event precedes the modified event."""
    assert game_state.apply_result is not None
    assert game_state.apply_result.sub_event_occurred is True


@then("the sub-event occurs before the modified event")
def sub_event_before_modified_event(game_state):
    """Rule 6.4.1a: Sub-events precede the replacement event."""
    assert game_state.apply_result.sub_event_order_before_modified is True


# ----- Rule 6.4.2: Replacement effect active/inactive -----

@given("a replacement effect that replaces a specific damage event")
def replacement_effect_for_specific_damage(game_state):
    """Rule 6.4.2: A replacement effect that targets a specific damage event."""
    game_state.replacement_effect = game_state.create_replacement_effect(
        replaces="damage_to_hero",
        with_effect="prevent_damage",
    )


@when("an event that does not match the replacement condition occurs")
def non_matching_event_occurs(game_state):
    """Rule 6.4.2: An event that does not match the replacement condition."""
    game_state.pending_event = {"type": "draw", "amount": 1}
    game_state.is_active_result = game_state.check_replacement_effect_active(
        game_state.replacement_effect, game_state.pending_event
    )


@then("the replacement effect is not active")
def replacement_effect_not_active(game_state):
    """Rule 6.4.2: The replacement effect is not active for the non-matching event."""
    assert game_state.is_active_result is False


@then("the replacement effect does not apply to the event")
def replacement_effect_does_not_apply(game_state):
    """Rule 6.4.2: The replacement effect is not applied."""
    assert game_state.is_active_result is False


@given("a replacement effect that replaces the next time a hero would be dealt damage")
def replacement_effect_for_hero_damage(game_state):
    """Rule 6.4.2: A replacement effect active for hero damage events."""
    game_state.replacement_effect = game_state.create_replacement_effect(
        replaces="hero_damage",
        with_effect="prevent_damage",
    )


@when("the hero is about to be dealt damage")
def hero_about_to_be_damaged(game_state):
    """Rule 6.4.2: Trigger a hero damage event."""
    game_state.pending_event = {"type": "hero_damage", "amount": 3}
    game_state.is_active_result = game_state.check_replacement_effect_active(
        game_state.replacement_effect, game_state.pending_event
    )


@then("the replacement effect is active")
def replacement_effect_is_active(game_state):
    """Rule 6.4.2: The replacement effect is active for the matching event."""
    assert game_state.is_active_result is True


@then("the replacement effect can be applied to the event")
def replacement_effect_can_apply(game_state):
    """Rule 6.4.2: The replacement effect can be applied."""
    assert game_state.is_active_result is True


# ----- Rule 6.4.2a: Variable values recalculated -----

@given("a replacement effect with a variable value based on game state")
def replacement_effect_with_variable(game_state):
    """Rule 6.4.2a: A replacement effect whose variable depends on current game state."""
    game_state.equipment_count = 2
    game_state.replacement_effect = game_state.create_variable_replacement_effect(
        variable_fn=lambda gs: gs.equipment_count,
    )


@given("the game state changes before the replacement effect is applied")
def game_state_changes_before_application(game_state):
    """Rule 6.4.2a: Simulate a game state change."""
    game_state.equipment_count = 3  # Changed from 2 to 3


@when("the replacement effect is about to be applied")
def replacement_effect_about_to_be_applied(game_state):
    """Rule 6.4.2a: Apply the replacement effect."""
    game_state.pending_event = {"type": "spell_damage", "amount": 5}
    game_state.apply_result = game_state.apply_variable_replacement_effect(
        game_state.replacement_effect, game_state.pending_event
    )


@then("the variable value is recalculated using the current game state")
def variable_value_recalculated(game_state):
    """Rule 6.4.2a: The variable is recalculated from current game state."""
    assert game_state.apply_result is not None
    assert game_state.apply_result.variable_value_used == 3  # Recalculated to 3


@then("the recalculated value is used for the replacement")
def recalculated_value_used(game_state):
    """Rule 6.4.2a: The replacement uses the recalculated value."""
    assert game_state.apply_result.used_recalculated_value is True


# ----- Rule 6.4.3: Must exist before event -----

@given("an event has already occurred")
def event_already_occurred(game_state):
    """Rule 6.4.3: An event has completed."""
    game_state.completed_event = {"type": "damage", "amount": 3, "resolved": True}


@when("a replacement effect is generated after the event")
def replacement_effect_generated_after_event(game_state):
    """Rule 6.4.3: Create a replacement effect after the event has already occurred."""
    game_state.late_replacement_effect = game_state.create_replacement_effect(
        replaces="damage",
        with_effect="prevent_damage",
    )
    game_state.retroactive_result = game_state.check_retroactive_application(
        game_state.late_replacement_effect, game_state.completed_event
    )


@then("the replacement effect does not retroactively apply to the past event")
def replacement_not_retroactive(game_state):
    """Rule 6.4.3: Replacement effects cannot be applied retroactively."""
    assert game_state.retroactive_result.was_applied is False


@then("the event stands as it originally occurred")
def event_stands_as_occurred(game_state):
    """Rule 6.4.3: The past event is unchanged."""
    assert game_state.retroactive_result.event_modified is False


# ----- Rule 6.4.4: Chain of replacement effects -----

@given("two replacement effects both active for a damage event")
def two_active_replacement_effects(game_state):
    """Rule 6.4.4: Set up two replacement effects both active for the same event."""
    game_state.replacement_effect_a = game_state.create_replacement_effect(
        replaces="damage_5",
        with_effect="damage_3",
    )
    game_state.replacement_effect_b = game_state.create_replacement_effect(
        replaces="damage_3",
        with_effect="prevent_all_damage",
    )
    game_state.pending_event = {"type": "damage", "amount": 5}


@given("the first replacement effect modifies the damage event")
def first_replacement_effect_applied(game_state):
    """Rule 6.4.4: The first replacement is applied, creating a modified event."""
    game_state.modified_event = {"type": "damage", "amount": 3}


@when("the second replacement effect checks if it is active for the modified event")
def second_checks_modified_event(game_state):
    """Rule 6.4.4: Check if the second effect is active for the modified event."""
    game_state.second_active_result = game_state.check_replacement_effect_active(
        game_state.replacement_effect_b, game_state.modified_event
    )


@then("the second replacement effect can be active for the modified event")
def second_active_for_modified(game_state):
    """Rule 6.4.4: The second replacement effect is active for the modified event."""
    assert game_state.second_active_result is True


@then("the second replacement effect can replace the modified event")
def second_can_replace_modified(game_state):
    """Rule 6.4.4: The second replacement effect can be applied to the modified event."""
    assert game_state.second_active_result is True


# ----- Rule 6.4.5: Cannot replace own modified event -----

@given("a replacement effect that replaces a damage event")
def replacement_effect_for_damage(game_state):
    """Rule 6.4.5: A replacement effect targeting a damage event."""
    game_state.replacement_effect = game_state.create_replacement_effect(
        replaces="damage",
        with_effect="halve_damage",
    )
    game_state.pending_event = {"type": "damage", "amount": 4}


@when("the replacement effect has already been applied to the original event")
def replacement_already_applied(game_state):
    """Rule 6.4.5: Mark the replacement effect as already applied."""
    game_state.replacement_effect_already_applied = True
    game_state.modified_event = {"type": "damage", "amount": 2}


@when("the modified event is about to occur")
def modified_event_about_to_occur(game_state):
    """Rule 6.4.5: The modified event is now about to occur."""
    game_state.double_apply_result = game_state.check_can_replace_own_modified_event(
        game_state.replacement_effect,
        game_state.modified_event,
        already_applied=True,
    )


@then("the replacement effect cannot replace its own modified event")
def replacement_cannot_replace_own_modified(game_state):
    """Rule 6.4.5: The replacement effect cannot be applied again."""
    assert game_state.double_apply_result.can_apply is False


@then("the effect can only be applied once per original event")
def effect_applied_once(game_state):
    """Rule 6.4.5: Each replacement effect can be applied at most once per original event."""
    assert game_state.double_apply_result.reason == "already_applied_to_original_event"


# ----- Rule 6.4.6: Modified event triggers new effects -----

@given("an event is about to occur")
def event_about_to_occur(game_state):
    """Rule 6.4.6: An event is pending."""
    game_state.pending_event = {"type": "damage", "amount": 2}


@given("a replacement effect modifies the event to a different type of event")
def replacement_modifies_to_different_type(game_state):
    """Rule 6.4.6: A replacement effect changes the event type."""
    game_state.replacement_effect = game_state.create_replacement_effect(
        replaces="damage",
        with_effect="healing",
    )


@when("the replacement effect is applied and the modified event occurs")
def replacement_applied_modified_event_occurs(game_state):
    """Rule 6.4.6: Apply the replacement and let the modified event occur."""
    game_state.apply_result = game_state.apply_replacement_with_new_event_type(
        game_state.replacement_effect, game_state.pending_event
    )


@then("replacement effects active for the modified event but not the original may apply")
def new_replacement_effects_may_apply(game_state):
    """Rule 6.4.6: The modified event may activate additional replacement effects."""
    assert game_state.apply_result is not None
    assert game_state.apply_result.new_replacement_effects_evaluated is True


@then("triggered effects sensitive to the modified event may fire")
def triggered_effects_may_fire(game_state):
    """Rule 6.4.6: Triggered effects may fire on the modified event."""
    assert game_state.apply_result.triggered_effects_evaluated is True


# ----- Rule 6.4.7: Self-replacement effect -----

@given("a card with a draw effect and a self-replacement effect")
def card_with_draw_and_self_replacement(game_state):
    """Rule 6.4.7: A card that has both a draw effect and a self-replacement effect."""
    game_state.card_with_self_replace = game_state.create_card(
        name="Tome of Divinity Test",
    )
    game_state.self_replacement_condition_met = False


@given("the condition for the self-replacement is satisfied before the draw effect generates its event")
def self_replacement_condition_satisfied(game_state):
    """Rule 6.4.7: The self-replacement condition is satisfied."""
    game_state.self_replacement_condition_met = True


@when("the card resolves and the draw effect is generated")
def card_resolves_draw_effect_generated(game_state):
    """Rule 6.4.7: The card resolves and generates its draw effect."""
    game_state.resolve_result = game_state.resolve_card_with_self_replacement(
        game_state.card_with_self_replace,
        base_draw=2,
        replacement_draw=3,
        condition_met=game_state.self_replacement_condition_met,
    )


@then("the self-replacement effect replaces the draw event")
def self_replacement_replaces_draw(game_state):
    """Rule 6.4.7: The self-replacement effect is applied."""
    assert game_state.resolve_result is not None
    assert game_state.resolve_result.self_replacement_applied is True


@then("the modified draw event occurs instead")
def modified_draw_occurs(game_state):
    """Rule 6.4.7: The modified draw (3 cards) occurs."""
    assert game_state.resolve_result.cards_drawn == 3


@given("the condition for the self-replacement is NOT satisfied")
def self_replacement_condition_not_satisfied(game_state):
    """Rule 6.4.7: The self-replacement condition is NOT satisfied."""
    game_state.self_replacement_condition_met = False


@then("the self-replacement effect does not apply")
def self_replacement_does_not_apply(game_state):
    """Rule 6.4.7: The self-replacement effect is not applied."""
    assert game_state.resolve_result is not None
    assert game_state.resolve_result.self_replacement_applied is False


@then("the original draw event occurs as normal")
def original_draw_occurs(game_state):
    """Rule 6.4.7: The original draw (2 cards) occurs."""
    assert game_state.resolve_result.cards_drawn == 2


# ----- Rule 6.4.7a: Self-replacement only applies to own preceding effect -----

@given("a card with a self-replacement effect")
def card_with_self_replacement(game_state):
    """Rule 6.4.7a: A card that has a self-replacement effect."""
    game_state.card_with_self_replace = game_state.create_card(
        name="Self-Replace Source Card",
    )
    game_state.other_card = game_state.create_card(
        name="Other Draw Card",
    )


@given("another card also generates a draw effect")
def another_card_generates_draw(game_state):
    """Rule 6.4.7a: Another unrelated card that also generates a draw effect."""
    # The other card's draw effect is distinct from the self-replacement source
    game_state.other_card_draw_event = {"type": "draw", "amount": 2, "source": "other_card"}


@when("the other card's draw effect generates an event")
def other_card_draw_event_generated(game_state):
    """Rule 6.4.7a: The other card generates a draw event."""
    game_state.cross_apply_result = game_state.check_self_replacement_cross_card(
        game_state.card_with_self_replace,
        game_state.other_card_draw_event,
    )


@then("the self-replacement effect does not apply to the other card's draw event")
def self_replacement_does_not_apply_to_other(game_state):
    """Rule 6.4.7a: Self-replacement only applies to its own preceding effect."""
    assert game_state.cross_apply_result.applied is False


# ----- Rule 6.4.7b: Condition evaluated when parameters are determined -----

@given("a card with a self-replacement effect dependent on a future card's properties")
def card_with_self_replacement_on_future_card(game_state):
    """Rule 6.4.7b: A card with a self-replacement condition depending on a future card."""
    game_state.card_with_self_replace = game_state.create_card(
        name="Weave Earth Test",
    )
    game_state.future_card = game_state.create_card(
        name="Future Attack Card",
    )
    game_state.future_card_is_fused = False


@when("a future card is played and its relevant property is determined")
def future_card_property_determined(game_state):
    """Rule 6.4.7b: The future card's property (e.g., fused) is determined."""
    game_state.future_card_is_fused = True
    game_state.deferred_condition_result = game_state.evaluate_deferred_self_replacement_condition(
        game_state.card_with_self_replace,
        game_state.future_card,
        fused=game_state.future_card_is_fused,
    )


@then("the self-replacement condition is evaluated at that time")
def self_replacement_condition_evaluated_at_play_time(game_state):
    """Rule 6.4.7b: The condition was evaluated when the future card's property was determined."""
    assert game_state.deferred_condition_result is not None
    assert game_state.deferred_condition_result.condition_evaluated_at_parameter_determination is True


@then("if the condition is met the self-replacement applies")
def if_condition_met_self_replacement_applies(game_state):
    """Rule 6.4.7b: The self-replacement applies since the condition is met."""
    assert game_state.deferred_condition_result.replacement_applied is True


# ----- Rule 6.4.8: Identity-replacement effect -----

@given("a card with an identity-replacement effect that specifies it enters with counters")
def card_with_identity_replacement(game_state):
    """Rule 6.4.8: A card with an identity-replacement effect (e.g., Hyper Driver)."""
    game_state.card_with_identity_replace = game_state.create_card(
        name="Hyper Driver Test",
    )
    game_state.expected_counters = 3


@when("the card enters the arena")
def card_enters_arena(game_state):
    """Rule 6.4.8: The card enters the arena triggering the identity-replacement."""
    game_state.arena_entry_result = game_state.apply_identity_replacement_effect(
        game_state.card_with_identity_replace,
        counter_count=game_state.expected_counters,
    )


@then("the identity-replacement effect applies")
def identity_replacement_applies(game_state):
    """Rule 6.4.8: The identity-replacement was applied."""
    assert game_state.arena_entry_result is not None
    assert game_state.arena_entry_result.identity_replacement_applied is True


@then("the card enters the arena with the specified counters already on it")
def card_enters_with_counters(game_state):
    """Rule 6.4.8: The card has the specified counters when it enters."""
    assert game_state.arena_entry_result.counters_on_entry == game_state.expected_counters


# ----- Rule 6.4.8a: Identity-replacement defines copyable properties -----

@given("a card with an identity-replacement effect that sets its properties on entering arena")
def card_with_property_modifying_identity_replacement(game_state):
    """Rule 6.4.8a: An identity-replacement that modifies properties."""
    game_state.card_with_identity_replace = game_state.create_card(
        name="Identity-Replace Property Card",
    )


@when("the card enters the arena with the identity-replacement applied")
def card_enters_arena_with_identity_replacement(game_state):
    """Rule 6.4.8a: The card enters the arena with identity-replacement applied."""
    game_state.copyable_props_result = game_state.check_identity_replacement_copyable_properties(
        game_state.card_with_identity_replace,
    )


@then("the modifications made by the identity-replacement are part of its copyable properties")
def identity_replacement_modifications_are_copyable(game_state):
    """Rule 6.4.8a: Identity-replacement modifications define copyable properties."""
    assert game_state.copyable_props_result is not None
    assert game_state.copyable_props_result.modification_is_copyable is True


# ----- Rule 6.4.9: Standard-replacement effect -----

@given("a continuous standard-replacement effect with a specific condition")
def continuous_standard_replacement_effect(game_state):
    """Rule 6.4.9: A standard-replacement effect (if/next ... instead ...)."""
    game_state.standard_replacement = game_state.create_standard_replacement_effect(
        condition="would_be_dealt_damage",
        modification="prevent_1_damage",
    )


@given("the condition is currently met")
def standard_replacement_condition_met(game_state):
    """Rule 6.4.9: The standard-replacement condition is currently met."""
    game_state.standard_replacement_active = True


@when("the triggering event is about to occur")
def triggering_event_about_to_occur(game_state):
    """Rule 6.4.9: The triggering event occurs."""
    game_state.pending_event = {"type": "damage", "amount": 3}
    game_state.apply_result = game_state.apply_standard_replacement_effect(
        game_state.standard_replacement, game_state.pending_event
    )


@then("the standard-replacement effect applies")
def standard_replacement_applies(game_state):
    """Rule 6.4.9: The standard-replacement effect was applied."""
    assert game_state.apply_result is not None
    assert game_state.apply_result.was_replaced is True


@then("the event is replaced by the modified event specified in the effect")
def event_replaced_by_specified_modification(game_state):
    """Rule 6.4.9: The event is replaced with the specified modification."""
    assert game_state.apply_result.modification == "prevent_1_damage"


# ----- Rule 6.4.10 / 6.4.10a: Prevention effects -----

@given("a prevention effect that prevents 3 damage")
def prevention_effect_3_damage(game_state):
    """Rule 6.4.10: A prevention effect with a prevention amount of 3."""
    game_state.prevention_effect = game_state.create_prevention_effect_with_amount(
        amount=3,
    )


@when("a damage event of 5 damage is about to be dealt")
def damage_event_5(game_state):
    """Rule 6.4.10a: A damage event of 5 occurs."""
    game_state.pending_event = {"type": "damage", "amount": 5}
    game_state.apply_result = game_state.apply_prevention_to_damage_event(
        game_state.prevention_effect, game_state.pending_event
    )


@then("the prevention effect applies to the damage event")
def prevention_applies_to_damage_event(game_state):
    """Rule 6.4.10: The prevention effect was applied."""
    assert game_state.apply_result is not None
    assert game_state.apply_result.was_applied is True


@then("3 damage is prevented")
def three_damage_prevented(game_state):
    """Rule 6.4.10a: 3 damage was prevented."""
    assert game_state.apply_result.damage_prevented == 3


@then("the remaining 2 damage is dealt as normal")
def two_damage_dealt(game_state):
    """Rule 6.4.10a: 2 remaining damage is dealt."""
    assert game_state.apply_result.damage_dealt == 2


@then("the prevention effect's remaining amount is reduced to 0")
def prevention_amount_reduced_to_zero(game_state):
    """Rule 6.4.10a: Prevention amount is now 0."""
    assert game_state.apply_result.remaining_prevention == 0


# ----- Rule 6.4.10b: Unspecified prevention amount -----

@given("a prevention effect that prevents the next damage without specifying an amount")
def prevention_effect_no_amount(game_state):
    """Rule 6.4.10b: A prevention effect with no explicit amount (e.g., Feign Death)."""
    game_state.prevention_effect = game_state.create_prevention_effect_with_amount(
        amount=None,
    )


@when("a damage event of 4 damage is about to occur")
def damage_event_4(game_state):
    """Rule 6.4.10b: A damage event of 4 occurs."""
    game_state.pending_event = {"type": "damage", "amount": 4}
    game_state.apply_result = game_state.apply_prevention_to_damage_event(
        game_state.prevention_effect, game_state.pending_event
    )


@then("the prevention amount is considered to be 4")
def prevention_amount_is_4(game_state):
    """Rule 6.4.10b: Prevention amount defaults to the damage in the event."""
    assert game_state.apply_result.effective_prevention_amount == 4


@then("all 4 damage is prevented")
def all_4_damage_prevented(game_state):
    """Rule 6.4.10b: All damage is prevented."""
    assert game_state.apply_result.damage_prevented == 4
    assert game_state.apply_result.damage_dealt == 0


# ----- Rule 6.4.10c: Prevention damage type -----

@given("a prevention effect that does not specify a damage type")
def prevention_effect_no_type(game_state):
    """Rule 6.4.10c: A prevention effect with no damage type specified."""
    game_state.prevention_effect = game_state.create_prevention_effect_with_amount(
        amount=3,
        damage_type=None,
    )


@when("a damage event of any damage type is about to occur")
def any_damage_type_event(game_state):
    """Rule 6.4.10c: A mixed-type damage event."""
    game_state.pending_event = {"type": "damage", "amount": 3, "damage_type": "physical"}
    game_state.apply_result = game_state.apply_prevention_to_damage_event(
        game_state.prevention_effect, game_state.pending_event
    )


@then("the prevention effect applies to any damage type")
def prevention_applies_to_any_type(game_state):
    """Rule 6.4.10c: Prevention with no type applies to all types."""
    assert game_state.apply_result.was_applied is True


@given("a prevention effect that specifies it prevents physical damage only")
def prevention_effect_physical_only(game_state):
    """Rule 6.4.10c: A prevention effect that only prevents physical damage."""
    game_state.prevention_effect = game_state.create_prevention_effect_with_amount(
        amount=3,
        damage_type="physical",
    )


@when("a damage event containing both physical and arcane damage is about to occur")
def mixed_damage_type_event(game_state):
    """Rule 6.4.10c: A damage event with both physical and arcane damage."""
    game_state.pending_event = {
        "type": "damage",
        "physical": 2,
        "arcane": 2,
    }
    game_state.apply_result = game_state.apply_typed_prevention_to_damage_event(
        game_state.prevention_effect, game_state.pending_event
    )


@then("the prevention effect only prevents the physical damage")
def prevention_only_prevents_physical(game_state):
    """Rule 6.4.10c: Only physical damage is prevented."""
    assert game_state.apply_result.physical_prevented == 2
    assert game_state.apply_result.arcane_prevented == 0


@then("the arcane damage is dealt as normal")
def arcane_damage_dealt_normally(game_state):
    """Rule 6.4.10c: Arcane damage is unaffected by the typed prevention effect."""
    assert game_state.apply_result.arcane_dealt == 2


# ----- Rule 6.4.10g: Decreasing prevention amount -----

@given("a prevention effect that would prevent 3 damage")
def prevention_effect_would_prevent_3(game_state):
    """Rule 6.4.10g: A prevention effect with initial prevention amount of 3."""
    game_state.prevention_effect = game_state.create_prevention_effect_with_amount(
        amount=3,
    )


@given("an effect exists that reduces the next prevention effect's amount by 1")
def reduction_effect_for_prevention(game_state):
    """Rule 6.4.10g: An effect that reduces the next prevention effect's amount."""
    game_state.prevention_reducer = game_state.create_prevention_reduction_effect(
        reduction=1,
    )


@when("the prevention effect is about to apply to a damage event")
def prevention_about_to_apply(game_state):
    """Rule 6.4.10g: The prevention effect is about to apply."""
    game_state.pending_event = {"type": "damage", "amount": 3}
    game_state.apply_result = game_state.apply_prevention_with_reduction(
        game_state.prevention_effect,
        game_state.prevention_reducer,
        game_state.pending_event,
    )


@then("the total prevention is established as 3")
def total_prevention_established_as_3(game_state):
    """Rule 6.4.10g: Total prevention is first established."""
    assert game_state.apply_result.initial_prevention_amount == 3


@then("the reduction effect reduces the prevention amount to 2")
def reduction_reduces_to_2(game_state):
    """Rule 6.4.10g: The reduction effect lowers prevention from 3 to 2."""
    assert game_state.apply_result.reduced_prevention_amount == 2


@then("only 2 damage is prevented")
def only_2_prevented(game_state):
    """Rule 6.4.10g: Only 2 damage is prevented after the reduction."""
    assert game_state.apply_result.damage_prevented == 2


# ----- Rule 6.4.10h: Cannot prevent still applies -----

@given("a prevention effect with a sub-effect that destroys its source")
def prevention_effect_with_destroy_sub_effect(game_state):
    """Rule 6.4.10h: A prevention effect that also destroys its source (e.g., Enchanting Melody)."""
    game_state.prevention_source = game_state.create_card(name="Enchanting Melody Test")
    game_state.prevention_effect = game_state.create_prevention_effect_with_sub_effect(
        amount=4,
        sub_effect="destroy_source",
        source_card=game_state.prevention_source,
    )


@given("an effect states the damage cannot be prevented")
def damage_cannot_be_prevented(game_state):
    """Rule 6.4.10h: An effect prevents prevention from working."""
    game_state.damage_cannot_be_prevented = True


@when("the damage event occurs")
def damage_event_occurs(game_state):
    """Rule 6.4.10h: The damage event occurs with cannot-prevent modifier."""
    game_state.pending_event = {
        "type": "damage",
        "amount": 3,
        "cannot_be_prevented": True,
    }
    game_state.apply_result = game_state.apply_prevention_effect_to_unprevantable_event(
        game_state.prevention_effect, game_state.pending_event
    )


@then("the prevention effect applies once to the event")
def prevention_applies_once(game_state):
    """Rule 6.4.10h: The prevention effect applies (but prevention amount is not reduced)."""
    assert game_state.apply_result.was_applied is True
    assert game_state.apply_result.times_applied == 1


@then("no damage is prevented")
def no_damage_prevented(game_state):
    """Rule 6.4.10h: No damage is prevented because it cannot be prevented."""
    assert game_state.apply_result.damage_prevented == 0


@then("the additional modification of the prevention effect still occurs")
def additional_modification_still_occurs(game_state):
    """Rule 6.4.10h: The sub-effect (destroy source) still occurs."""
    assert game_state.apply_result.sub_effect_occurred is True


@then("the prevention amount is not reduced")
def prevention_amount_not_reduced(game_state):
    """Rule 6.4.10h: Prevention amount remains unchanged."""
    assert game_state.apply_result.prevention_amount_reduced is False


# ----- Rule 6.4.10i: Fixed-prevention effect -----

@given("a fixed-prevention effect that prevents 3 damage from the next damage event")
def fixed_prevention_effect_3(game_state):
    """Rule 6.4.10i: A fixed-prevention effect with prevention amount of 3."""
    game_state.fixed_prevention = game_state.create_fixed_prevention_effect(amount=3)


@when("a damage event of 2 damage occurs and 2 damage is prevented")
def first_event_2_damage(game_state):
    """Rule 6.4.10i: The first damage event (2 damage) occurs."""
    game_state.first_event = {"type": "damage", "amount": 2}
    game_state.first_result = game_state.apply_fixed_prevention(
        game_state.fixed_prevention, game_state.first_event
    )
    assert game_state.first_result.damage_prevented == 2


@when("a second damage event then occurs")
def second_damage_event(game_state):
    """Rule 6.4.10i: A second damage event occurs."""
    game_state.second_event = {"type": "damage", "amount": 3}
    game_state.second_result = game_state.apply_fixed_prevention_second_time(
        game_state.fixed_prevention, game_state.second_event
    )


@then("the fixed-prevention effect does not apply to the second damage event")
def fixed_prevention_not_applied_second_time(game_state):
    """Rule 6.4.10i: Fixed-prevention only applies to the first event."""
    assert game_state.second_result.was_applied is False


@then("the remaining 1 damage from the original prevention amount is discarded")
def remaining_prevention_discarded(game_state):
    """Rule 6.4.10i: Remaining prevention amount is not carried over."""
    assert game_state.second_result.remaining_prevention_from_fixed == 0


# ----- Rule 6.4.10j: Shielding-prevention effect -----

@given("a shielding-prevention effect that prevents the next 4 damage")
def shielding_prevention_4(game_state):
    """Rule 6.4.10j: A shielding-prevention effect with total prevention amount of 4."""
    game_state.shielding_prevention = game_state.create_shielding_prevention_effect(amount=4)


@when("a first damage event of 2 damage occurs")
def first_shielding_event(game_state):
    """Rule 6.4.10j: The first damage event (2 damage) occurs."""
    game_state.first_shield_event = {"type": "damage", "amount": 2}
    game_state.first_shield_result = game_state.apply_shielding_prevention(
        game_state.shielding_prevention, game_state.first_shield_event
    )


@then("2 damage is prevented and 2 prevention amount remains")
def two_prevented_two_remain(game_state):
    """Rule 6.4.10j: 2 prevented, 2 remaining."""
    assert game_state.first_shield_result.damage_prevented == 2
    assert game_state.first_shield_result.remaining_prevention == 2


@when("a second damage event of 3 damage occurs")
def second_shielding_event(game_state):
    """Rule 6.4.10j: A second damage event (3 damage) occurs."""
    game_state.second_shield_event = {"type": "damage", "amount": 3}
    game_state.second_shield_result = game_state.apply_shielding_prevention(
        game_state.shielding_prevention, game_state.second_shield_event
    )


@then("the remaining 2 prevention amount prevents 2 of the 3 damage")
def remaining_prevents_2_of_3(game_state):
    """Rule 6.4.10j: Remaining 2 prevention blocks 2 of the 3 incoming damage."""
    assert game_state.second_shield_result.damage_prevented == 2


@then("1 damage is dealt from the second event")
def one_damage_dealt_second_event(game_state):
    """Rule 6.4.10j: 1 damage breaks through."""
    assert game_state.second_shield_result.damage_dealt == 1


@then("the shielding-prevention effect's prevention amount is reduced to 0 and ceases to exist")
def shielding_prevention_exhausted(game_state):
    """Rule 6.4.10j: The shielding-prevention effect is exhausted."""
    assert game_state.second_shield_result.remaining_prevention == 0
    assert game_state.second_shield_result.effect_ceased is True


# ----- Rule 6.4.11: Outcome-replacement effect -----

@given("an outcome-replacement effect that replaces a failure outcome with another event")
def outcome_replacement_effect(game_state):
    """Rule 6.4.11: An outcome-replacement effect (e.g., Victor's clash failure)."""
    game_state.outcome_replacement = game_state.create_outcome_replacement_effect(
        replaces_outcome="fail_clash",
        with_outcome="clash_again",
    )


@given("the replacement condition is met")
def outcome_replacement_condition_met(game_state):
    """Rule 6.4.11: The condition for the outcome-replacement is met."""
    game_state.outcome_replacement_condition = True


@when("the event occurs and would result in the failure outcome")
def event_results_in_failure_outcome(game_state):
    """Rule 6.4.11: An event that would normally result in a failure outcome."""
    game_state.pending_event = {"type": "clash", "outcome": "fail"}
    game_state.apply_result = game_state.apply_outcome_replacement_effect(
        game_state.outcome_replacement, game_state.pending_event
    )


@then("the outcome-replacement effect applies")
def outcome_replacement_applies(game_state):
    """Rule 6.4.11: The outcome-replacement effect was applied."""
    assert game_state.apply_result is not None
    assert game_state.apply_result.was_applied is True


@then("the failure outcome is replaced with the specified replacement event")
def failure_replaced_with_new_event(game_state):
    """Rule 6.4.11: The failure outcome is replaced with the replacement event."""
    assert game_state.apply_result.outcome == "clash_again"


@then("the original failure outcome does not occur")
def original_failure_does_not_occur(game_state):
    """Rule 6.4.11: The original failure outcome is suppressed."""
    assert game_state.apply_result.original_outcome_occurred is False


# ===== Fixture =====


@pytest.fixture
def game_state():
    """
    Fixture providing game state for testing Section 6.4: Replacement Effects.

    Uses BDDGameState which integrates with the real engine.
    Reference: Rule 6.4
    """
    from tests.bdd_helpers import BDDGameState

    state = BDDGameState()
    return state
