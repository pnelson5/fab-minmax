"""
Step definitions for Section 6.3: Continuous Effect Interactions
Reference: Flesh and Blood Comprehensive Rules Section 6.3

This module implements behavioral tests for the staging system that governs how
multiple continuous effects interact and are applied to objects and game rules.

Engine Features Needed for Section 6.3:
- [ ] ContinuousEffectStagingSystem.apply_effects(effects, target) -> StagingResult (Rule 6.3.1)
- [ ] ContinuousEffect.is_rule_modifying() -> bool (Rule 6.3.1)
- [ ] ContinuousEffectStagingSystem.apply_rule_modifying_effects_first() (Rule 6.3.1)
- [ ] StagingSystem.get_stage(effect) -> int (Rule 6.3.2): 1-8 per effect type
- [ ] StagingSystem.get_substage(effect) -> int (Rule 6.3.3): 1-7 per effect operation
- [ ] ContinuousEffect.is_dependent() -> bool (Rule 6.3.2a)
- [ ] ContinuousEffect.dependent_stage() -> int (Rule 6.3.2a)
- [ ] StagingSystem.apply_dependent_effect_at_highest_stage() (Rule 6.3.2b)
- [ ] MultiPartEffect.apply_parts_in_respective_stages() (Rule 6.3.2c)
- [ ] StagingSystem.get_timestamp(effect) -> int (Rule 6.3.4)
- [ ] StagingSystem.apply_in_timestamp_order(same_substage_effects) (Rule 6.3.3a / 6.3.4)
- [ ] LayerContinuousEffect.timestamp: set when source resolves (Rule 6.3.4a)
- [ ] StaticContinuousEffect.timestamp: set when static ability becomes functional (Rule 6.3.4a)
- [ ] TurnPlayer.decide_effect_order(effects) -> list (Rule 6.3.4b)
- [ ] StagingSystem.decided_order_is_final() -> bool (Rule 6.3.4b)
- [ ] StagingSystem.insert_new_effect_after_existing(substage, effect) (Rule 6.3.4c)
- [ ] StagingSystem.recalculate_all_effects() (Rule 6.3.5)
- [ ] StagingSystem.update_eligible_effects_after_modification() (Rule 6.3.5a)
- [ ] StagingSystem.no_retroactive_application_to_previous_stages() (Rule 6.3.5b)
- [ ] ContinuousEffect.does_not_remove_properties_added_by_other_effects() (Rule 6.3.6)
- [ ] PreventionEffect.only_prevents_explicitly_specified() (Rule 6.3.7)

Current status: Tests written, Engine pending
"""

import pytest
from pytest_bdd import scenario, given, when, then, parsers


# ===== Scenarios =====


@scenario(
    "../features/section_6_3_continuous_effect_interactions.feature",
    "A rule-modifying continuous effect is applied before object-modifying effects",
)
def test_rule_modifying_effect_applied_before_object_modifying():
    """Rule 6.3.1: Rule-modifying effects are applied before object-modifying effects."""
    pass


@scenario(
    "../features/section_6_3_continuous_effect_interactions.feature",
    "Two or more object-modifying effects are applied using the staging system",
)
def test_object_modifying_effects_use_staging_system():
    """Rule 6.3.1: Object-modifying effects are applied using the staging system."""
    pass


@scenario(
    "../features/section_6_3_continuous_effect_interactions.feature",
    "Stage 1 copyable property effects are applied before stage 4 type effects",
)
def test_stage_1_applied_before_stage_4():
    """Rule 6.3.2: Stage 1 effects are applied before stage 4 effects."""
    pass


@scenario(
    "../features/section_6_3_continuous_effect_interactions.feature",
    "Stage 7 base numeric effects are applied before stage 8 numeric modifier effects",
)
def test_stage_7_applied_before_stage_8():
    """Rule 6.3.2: Stage 7 effects are applied before stage 8 effects."""
    pass


@scenario(
    "../features/section_6_3_continuous_effect_interactions.feature",
    "A dependent effect is applied at the stage it depends on",
)
def test_dependent_effect_applied_at_dependent_stage():
    """Rule 6.3.2a: A dependent effect is applied at the stage on which it depends."""
    pass


@scenario(
    "../features/section_6_3_continuous_effect_interactions.feature",
    "An independent ability effect is applied in stage 6 substage 1",
)
def test_independent_ability_effect_in_stage_6_substage_1():
    """Rule 6.3.3: Independent effects in stages 1-6 are applied before dependent effects."""
    pass


@scenario(
    "../features/section_6_3_continuous_effect_interactions.feature",
    "An effect dependent on two stages is applied at the highest stage",
)
def test_effect_dependent_on_two_stages_applied_at_highest():
    """Rule 6.3.2b: An effect dependent on two stages is applied at the highest stage."""
    pass


@scenario(
    "../features/section_6_3_continuous_effect_interactions.feature",
    "Separate parts of a multi-part effect are applied in their respective stages",
)
def test_multipart_effect_parts_applied_in_respective_stages():
    """Rule 6.3.2c: Separate parts of an effect are applied in their respective stages."""
    pass


@scenario(
    "../features/section_6_3_continuous_effect_interactions.feature",
    "In stage 8 an independent set effect is applied before an independent add effect",
)
def test_stage_8_set_before_add():
    """Rule 6.3.3: In stage 8 set (substage 2) is applied before add (substage 5)."""
    pass


@scenario(
    "../features/section_6_3_continuous_effect_interactions.feature",
    "In stages 1 to 6 independent effects are applied before dependent effects",
)
def test_stages_1_to_6_independent_before_dependent():
    """Rule 6.3.3: In stages 1-6, independent effects are applied before dependent effects."""
    pass


@scenario(
    "../features/section_6_3_continuous_effect_interactions.feature",
    "In stage 8 independent multiply effect is applied before independent add effect",
)
def test_stage_8_multiply_before_add():
    """Rule 6.3.3: In stage 8 multiply (substage 3) is applied before add (substage 5)."""
    pass


@scenario(
    "../features/section_6_3_continuous_effect_interactions.feature",
    "Two effects in the same substage are applied in timestamp order",
)
def test_same_substage_effects_applied_in_timestamp_order():
    """Rule 6.3.3a / 6.3.4: Same substage effects applied in chronological timestamp order."""
    pass


@scenario(
    "../features/section_6_3_continuous_effect_interactions.feature",
    "The timestamp of a layer-continuous effect is when its source resolves",
)
def test_layer_continuous_effect_timestamp_at_resolution():
    """Rule 6.3.4a: Layer-continuous effect timestamp is when its source resolves."""
    pass


@scenario(
    "../features/section_6_3_continuous_effect_interactions.feature",
    "The timestamp of a static-continuous effect is when its source ability becomes functional",
)
def test_static_continuous_effect_timestamp_at_ability_functional():
    """Rule 6.3.4a: Static-continuous effect timestamp is when the static ability becomes functional."""
    pass


@scenario(
    "../features/section_6_3_continuous_effect_interactions.feature",
    "When two effects have the same timestamp the turn-player decides application order",
)
def test_same_timestamp_turn_player_decides_order():
    """Rule 6.3.4b: Turn-player decides application order for same-timestamp effects."""
    pass


@scenario(
    "../features/section_6_3_continuous_effect_interactions.feature",
    "The turn-player cannot change the order after it has been decided",
)
def test_decided_order_cannot_be_changed():
    """Rule 6.3.4b: Once decided, the turn-player cannot change the order of effects."""
    pass


@scenario(
    "../features/section_6_3_continuous_effect_interactions.feature",
    "A new effect applied to an object in a substage is ordered after existing effects",
)
def test_new_effect_ordered_after_existing_in_substage():
    """Rule 6.3.4c: New effects in a substage are ordered after existing effects."""
    pass


@scenario(
    "../features/section_6_3_continuous_effect_interactions.feature",
    "All effects are recalculated when a new effect is applied",
)
def test_effects_recalculated_when_new_effect_applied():
    """Rule 6.3.5: Continuous effects are applied dynamically; all recalculated when any changes."""
    pass


@scenario(
    "../features/section_6_3_continuous_effect_interactions.feature",
    "An object becoming eligible for an effect causes that effect to be added",
)
def test_object_becoming_eligible_causes_effect_to_be_added():
    """Rule 6.3.5a: An object becoming eligible for an effect causes that effect to be added."""
    pass


@scenario(
    "../features/section_6_3_continuous_effect_interactions.feature",
    "An object modified in stage 8 does not retroactively trigger stage 6 effects",
)
def test_stage_8_modification_does_not_retroactively_trigger_stage_6():
    """Rule 6.3.5b: Previous stage effects are not retroactively applied."""
    pass


@scenario(
    "../features/section_6_3_continuous_effect_interactions.feature",
    "A remove-property effect does not remove properties added by another effect",
)
def test_remove_property_effect_does_not_remove_properties_from_other_effects():
    """Rule 6.3.6: An effect removing a property does not remove properties added by other effects."""
    pass


@scenario(
    "../features/section_6_3_continuous_effect_interactions.feature",
    "A prevention effect only blocks modifications it explicitly specifies",
)
def test_prevention_effect_only_blocks_explicitly_specified_modifications():
    """Rule 6.3.7: Effects only prevent modifications they explicitly specify."""
    pass


@scenario(
    "../features/section_6_3_continuous_effect_interactions.feature",
    "A prevention effect does not implicitly prevent other modifications",
)
def test_prevention_effect_does_not_implicitly_prevent_other_modifications():
    """Rule 6.3.7: A prevention effect does not block modifications it does not specify."""
    pass


# ===== Step Definitions =====


@given("a game is in progress with multiple continuous effects active")
def game_in_progress_with_multiple_effects(game_state):
    """Set up a basic game state with support for multiple concurrent continuous effects."""
    assert game_state is not None
    game_state.applied_stages = []
    game_state.applied_substages = []
    game_state.effect_application_order = []


@given("a rule-modifying effect prevents attacks from gaining go again")
def rule_modifying_effect_prevents_go_again(game_state):
    """Rule 6.3.1: A rule-modifying continuous effect (like Hypothermia) prevents go again."""
    game_state.rule_effect = game_state.create_rule_modifying_continuous_effect(
        rule="attacks_cannot_gain_go_again"
    )


@given("an object-modifying effect would grant go again to an attack")
def object_modifying_effect_grants_go_again(game_state):
    """Rule 6.3.1: An object-modifying effect that would add go again to an attack."""
    game_state.attack_card = game_state.create_card(name="Test Attack", card_type="attack action")
    game_state.object_effect = game_state.create_object_modifying_continuous_effect(
        modifier="grant_go_again",
        target=game_state.attack_card
    )


@when("the effects are applied to the attack")
def effects_applied_to_attack(game_state):
    """Rule 6.3.1: Apply all active continuous effects to the attack."""
    game_state.application_result = game_state.apply_all_continuous_effects(
        target=game_state.attack_card,
        effects=[game_state.rule_effect, game_state.object_effect]
    )


@then("the rule-modifying effect is applied before the object-modifying effect")
def rule_modifying_applied_before_object_modifying(game_state):
    """Rule 6.3.1: Rule-modifying effects are applied simultaneously before object-modifying effects."""
    assert game_state.application_result.rule_effects_applied_first


@then("the attack does not gain go again")
def attack_does_not_gain_go_again(game_state):
    """Rule 6.3.1: Because the rule-modifying effect prevents go again, the attack cannot gain it."""
    assert not game_state.application_result.go_again_gained


@given("a stage 6 effect grants an ability to an object")
def stage_6_effect_grants_ability(game_state):
    """Rule 6.3.2: A stage 6 effect that grants an ability."""
    game_state.target_card = game_state.create_card(name="Target Object")
    game_state.stage6_effect = game_state.create_staged_continuous_effect(
        stage=6,
        modifier="grant_dominate",
        target=game_state.target_card
    )


@given("a stage 8 effect adds to the power of the same object")
def stage_8_effect_adds_to_power(game_state):
    """Rule 6.3.2: A stage 8 effect that modifies a numeric property."""
    game_state.stage8_effect = game_state.create_staged_continuous_effect(
        stage=8,
        modifier="+2{p}",
        target=game_state.target_card
    )


@when("the staging system applies both effects")
def staging_system_applies_both_effects(game_state):
    """Rule 6.3.2: The staging system applies effects in ascending stage order."""
    game_state.staging_result = game_state.apply_effects_in_staging_order(
        effects=[game_state.stage6_effect, game_state.stage8_effect],
        target=game_state.target_card
    )


@then("the stage 6 effect is applied before the stage 8 effect")
def stage_6_applied_before_stage_8(game_state):
    """Rule 6.3.2: Stage 6 is lower than stage 8, so it is applied first."""
    assert game_state.staging_result.application_order == [6, 8]


@given("a continuous effect in stage 1 modifies a copyable property")
def stage_1_effect_modifies_copyable_property(game_state):
    """Rule 6.3.2: Stage 1 modifies copyable properties."""
    game_state.target_card = game_state.create_card(name="Target Object")
    game_state.stage1_effect = game_state.create_staged_continuous_effect(
        stage=1,
        modifier="copy_properties",
        target=game_state.target_card
    )


@given("a continuous effect in stage 4 modifies the card's types")
def stage_4_effect_modifies_types(game_state):
    """Rule 6.3.2: Stage 4 modifies types/subtypes."""
    game_state.stage4_effect = game_state.create_staged_continuous_effect(
        stage=4,
        modifier="change_type",
        target=game_state.target_card
    )


@then("the stage 1 effect is applied before the stage 4 effect")
def stage_1_applied_before_stage_4(game_state):
    """Rule 6.3.2: Stage 1 is lower than stage 4, so it is applied first."""
    assert game_state.staging_result.application_order == [1, 4]


@given("a stage 7 effect sets the base power of an attack to 4")
def stage_7_effect_sets_base_power(game_state):
    """Rule 6.3.2: Stage 7 modifies the base value of a numeric property."""
    game_state.target_card = game_state.create_card(name="Test Attack", card_type="attack action", power=3)
    game_state.stage7_effect = game_state.create_staged_continuous_effect(
        stage=7,
        modifier="set_base_power_4",
        target=game_state.target_card
    )


@given("a stage 8 effect adds 2 to the power of the same attack")
def stage_8_effect_adds_2_to_power(game_state):
    """Rule 6.3.2: Stage 8 modifies the value of a numeric property."""
    game_state.stage8_add_effect = game_state.create_staged_continuous_effect(
        stage=8,
        modifier="+2{p}",
        target=game_state.target_card
    )


@when("the staging system applies both effects in ascending stage order")
def staging_system_applies_in_ascending_stage_order(game_state):
    """Rule 6.3.2: Staging system applies effects in ascending order."""
    game_state.staging_result = game_state.apply_effects_in_staging_order(
        effects=[game_state.stage7_effect, game_state.stage8_add_effect],
        target=game_state.target_card
    )


@then("the stage 7 effect is applied first setting base power to 4")
def stage_7_applied_first_setting_base_power(game_state):
    """Rule 6.3.2: Stage 7 is applied first; base power is set to 4."""
    assert game_state.staging_result.application_order[0] == 7
    assert game_state.staging_result.intermediate_power_after_stage7 == 4


@then("the stage 8 effect is applied second resulting in total power of 6")
def stage_8_applied_second_resulting_in_power_6(game_state):
    """Rule 6.3.2: Stage 8 is applied second; +2 to base power 4 = 6."""
    assert game_state.staging_result.application_order[1] == 8
    assert game_state.staging_result.final_power == 6


@given("an effect grants abilities to an attack if its power is greater than its base")
def effect_grants_abilities_if_power_greater_than_base(game_state):
    """Rule 6.3.2a: An effect that is dependent on stage 8 power values (like Thump)."""
    game_state.target_card = game_state.create_card(name="Thump Style Card", card_type="attack action", power=4)
    game_state.dependent_effect = game_state.create_dependent_continuous_effect(
        modifier="grant_dominate_if_power_greater_than_base",
        dependent_stage=8,
        target=game_state.target_card
    )


@given("this effect is dependent on the stage 8 power value")
def effect_dependent_on_stage_8(game_state):
    """Rule 6.3.2a: The effect depends on the final power value (stage 8)."""
    assert game_state.dependent_effect.dependent_stage == 8


@when("the staging system evaluates the effect")
def staging_system_evaluates_effect(game_state):
    """Rule 6.3.2a: The staging system determines where to apply the effect."""
    game_state.evaluation_result = game_state.evaluate_effect_staging(game_state.dependent_effect)


@then("the effect is classified as dependent on stage 8")
def effect_classified_as_dependent_on_stage_8(game_state):
    """Rule 6.3.2a: The staging system classifies this as a dependent effect on stage 8."""
    assert game_state.evaluation_result.is_dependent
    assert game_state.evaluation_result.dependent_stage == 8


@then("the effect is applied in stage 8 substage 7")
def effect_applied_in_stage_8_substage_7(game_state):
    """Rule 6.3.2a / 6.3.3: Dependent effects in stage 8 are applied in substage 7."""
    assert game_state.evaluation_result.applied_stage == 8
    assert game_state.evaluation_result.applied_substage == 7


@given("an effect unconditionally grants an ability to an attack")
def effect_unconditionally_grants_ability(game_state):
    """Rule 6.3.3: An independent stage 6 effect that grants an ability unconditionally."""
    game_state.target_card = game_state.create_card(name="Test Attack", card_type="attack action")
    game_state.independent_effect = game_state.create_staged_continuous_effect(
        stage=6,
        modifier="grant_go_again",
        target=game_state.target_card,
        is_independent=True
    )


@then("the effect is classified as independent")
def effect_classified_as_independent(game_state):
    """Rule 6.3.3: The effect is not dependent on any other stage."""
    assert game_state.evaluation_result.is_independent


@then("the effect is applied in stage 6 substage 1")
def effect_applied_in_stage_6_substage_1(game_state):
    """Rule 6.3.3: Independent effects in stages 1-6 are applied in substage 1."""
    assert game_state.evaluation_result.applied_stage == 6
    assert game_state.evaluation_result.applied_substage == 1


@given("an effect is dependent on both stage 6 abilities and stage 8 power values")
def effect_dependent_on_stage_6_and_stage_8(game_state):
    """Rule 6.3.2b: An effect that depends on both stage 6 and stage 8."""
    game_state.target_card = game_state.create_card(name="Multi-Dependent Card", card_type="attack action")
    game_state.multi_dependent_effect = game_state.create_multi_dependent_continuous_effect(
        modifier="complex_modifier",
        dependent_stages=[6, 8],
        target=game_state.target_card
    )


@then("the effect is applied at stage 8 the highest of the two dependent stages")
def effect_applied_at_stage_8_highest(game_state):
    """Rule 6.3.2b: The effect is applied at the highest dependent stage (8)."""
    assert game_state.evaluation_result.applied_stage == 8


@given("an effect has one part that modifies abilities in stage 6")
def effect_has_part_in_stage_6(game_state):
    """Rule 6.3.2c: Part of an effect applies in stage 6 (abilities)."""
    game_state.target_card = game_state.create_card(name="Multi-Part Effect Card", card_type="attack action")
    game_state.multipart_effect = game_state.create_multi_part_continuous_effect(
        parts=[
            {"stage": 6, "modifier": "grant_dominate"},
            {"stage": 8, "modifier": "+2{p}"},
        ],
        target=game_state.target_card
    )


@given("another part of the same effect modifies power in stage 8")
def effect_has_part_in_stage_8(game_state):
    """Rule 6.3.2c: Another part of the same effect applies in stage 8 (numeric properties)."""
    # Already set up in the previous step via multipart_effect
    assert len(game_state.multipart_effect.parts) == 2


@when("the staging system applies the effect")
def staging_system_applies_multipart_effect(game_state):
    """Rule 6.3.2c: The staging system applies each part of the effect."""
    game_state.staging_result = game_state.apply_multipart_effect_in_staging_order(
        effect=game_state.multipart_effect,
        target=game_state.target_card
    )


@then("the ability-modifying part is applied in stage 6")
def ability_part_applied_in_stage_6(game_state):
    """Rule 6.3.2c: The ability-modifying part of the effect is applied in stage 6."""
    assert game_state.staging_result.part_application_stages[0] == 6


@then("the power-modifying part is applied in stage 8")
def power_part_applied_in_stage_8(game_state):
    """Rule 6.3.2c: The power-modifying part of the effect is applied in stage 8."""
    assert game_state.staging_result.part_application_stages[1] == 8


@given("a stage 8 independent effect sets power to 5")
def stage_8_set_power_to_5(game_state):
    """Rule 6.3.3: Stage 8 substage 2 - independent set effect."""
    game_state.target_card = game_state.create_card(name="Test Object", card_type="attack action", power=2)
    game_state.set_effect = game_state.create_stage8_substage_effect(
        substage=2,
        modifier="set_power_5",
        target=game_state.target_card,
        is_independent=True
    )


@given("a stage 8 independent effect adds 3 to power")
def stage_8_add_3_to_power(game_state):
    """Rule 6.3.3: Stage 8 substage 5 - independent add effect."""
    game_state.add_effect = game_state.create_stage8_substage_effect(
        substage=5,
        modifier="+3{p}",
        target=game_state.target_card,
        is_independent=True
    )


@when("the staging system applies both effects to the same object")
def staging_system_applies_both_to_same_object(game_state):
    """Rule 6.3.3: Staging system applies both effects."""
    game_state.staging_result = game_state.apply_effects_in_staging_order(
        effects=[game_state.set_effect, game_state.add_effect],
        target=game_state.target_card
    )


@then("the set effect is applied first in substage 2")
def set_effect_applied_first_in_substage_2(game_state):
    """Rule 6.3.3: Substage 2 (set) is applied before substage 5 (add)."""
    assert game_state.staging_result.substage_application_order[0] == 2


@then("the add effect is applied second in substage 5")
def add_effect_applied_second_in_substage_5(game_state):
    """Rule 6.3.3: Substage 5 (add) is applied after substage 2 (set)."""
    assert game_state.staging_result.substage_application_order[1] == 5


@then("the resulting power is 8")
def resulting_power_is_8(game_state):
    """Rule 6.3.3: Set to 5, then add 3 = 8."""
    assert game_state.staging_result.final_power == 8


@given("an independent stage 6 ability effect unconditionally grants an ability")
def independent_stage_6_effect(game_state):
    """Rule 6.3.3: An independent stage 6 effect."""
    game_state.target_card = game_state.create_card(name="Test Object")
    game_state.independent_stage6_effect = game_state.create_staged_continuous_effect(
        stage=6,
        modifier="grant_dominate",
        target=game_state.target_card,
        is_independent=True
    )


@given("a dependent stage 6 ability effect conditionally grants an ability based on object properties")
def dependent_stage_6_effect(game_state):
    """Rule 6.3.3: A dependent stage 6 effect."""
    game_state.dependent_stage6_effect = game_state.create_staged_continuous_effect(
        stage=6,
        modifier="grant_go_again_if_condition",
        target=game_state.target_card,
        is_independent=False
    )


@then("the independent effect is applied in substage 1")
def independent_effect_in_substage_1(game_state):
    """Rule 6.3.3: Independent effects in stages 1-6 are in substage 1."""
    assert game_state.staging_result.independent_effect_substage == 1


@then("the dependent effect is applied in substage 7")
def dependent_effect_in_substage_7(game_state):
    """Rule 6.3.3: Dependent effects are in substage 7."""
    assert game_state.staging_result.dependent_effect_substage == 7


@given("a stage 8 independent multiply effect doubles the power")
def stage_8_multiply_doubles_power(game_state):
    """Rule 6.3.3: Stage 8 substage 3 - multiply effect."""
    game_state.target_card = game_state.create_card(name="Test Object", card_type="attack action", power=3)
    game_state.multiply_effect = game_state.create_stage8_substage_effect(
        substage=3,
        modifier="multiply_power_2x",
        target=game_state.target_card,
        is_independent=True
    )


@given("a stage 8 independent add effect adds 2 to the power")
def stage_8_add_2_to_power(game_state):
    """Rule 6.3.3: Stage 8 substage 5 - add effect."""
    game_state.add2_effect = game_state.create_stage8_substage_effect(
        substage=5,
        modifier="+2{p}",
        target=game_state.target_card,
        is_independent=True
    )


@when("the staging system applies both effects to an object with base power of 3")
def staging_system_applies_to_object_with_power_3(game_state):
    """Rule 6.3.3: Apply both effects to object with base power 3."""
    game_state.staging_result = game_state.apply_effects_in_staging_order(
        effects=[game_state.multiply_effect, game_state.add2_effect],
        target=game_state.target_card
    )


@then("the multiply effect is applied first in substage 3")
def multiply_effect_in_substage_3(game_state):
    """Rule 6.3.3: Substage 3 (multiply) is applied before substage 5 (add)."""
    assert game_state.staging_result.substage_application_order[0] == 3


@then("the add effect is applied second in substage 5")
def add_effect_in_substage_5_second(game_state):
    """Rule 6.3.3: Substage 5 (add) is applied after substage 3 (multiply)."""
    assert game_state.staging_result.substage_application_order[1] == 5


@then("the resulting power is 8")
def resulting_power_is_8_multiply_then_add(game_state):
    """Rule 6.3.3: 3 * 2 = 6, then 6 + 2 = 8."""
    assert game_state.staging_result.final_power == 8


@given("a stage 8 add effect was generated at timestamp 1")
def stage_8_effect_at_timestamp_1(game_state):
    """Rule 6.3.4: An effect with timestamp 1."""
    game_state.target_card = game_state.create_card(name="Test Object", card_type="attack action", power=3)
    game_state.effect_ts1 = game_state.create_continuous_effect_with_timestamp(
        stage=8,
        substage=5,
        modifier="+1{p}",
        timestamp=1,
        target=game_state.target_card
    )


@given("a stage 8 add effect was generated at timestamp 2")
def stage_8_effect_at_timestamp_2(game_state):
    """Rule 6.3.4: An effect with timestamp 2."""
    game_state.effect_ts2 = game_state.create_continuous_effect_with_timestamp(
        stage=8,
        substage=5,
        modifier="+2{p}",
        timestamp=2,
        target=game_state.target_card
    )


@then("the effect with timestamp 1 is applied before the effect with timestamp 2")
def timestamp_1_applied_before_timestamp_2(game_state):
    """Rule 6.3.4: Effects with earlier timestamps are applied first."""
    assert game_state.staging_result.timestamp_application_order == [1, 2]


@given("a card resolves on the stack at game time 100 generating a layer-continuous effect")
def card_resolves_at_game_time_100(game_state):
    """Rule 6.3.4a: A layer resolves and generates a layer-continuous effect."""
    game_state.source_card = game_state.create_card(name="Source Card")
    game_state.layer = game_state.create_layer_with_continuous_effect(
        game_state.source_card,
        modifier="+2{p}",
        duration="end_of_turn"
    )
    game_state.layer_resolve_time = 100
    game_state.layer_continuous_effect = game_state.resolve_layer_at_time(
        game_state.layer, game_time=game_state.layer_resolve_time
    )


@when("the staging system records the timestamp of the effect")
def staging_records_timestamp(game_state):
    """Rule 6.3.4a: The staging system records the timestamp when the effect is generated."""
    game_state.recorded_timestamp = game_state.get_effect_timestamp(
        game_state.layer_continuous_effect
    )


@then("the timestamp of the layer-continuous effect is game time 100")
def layer_continuous_timestamp_is_100(game_state):
    """Rule 6.3.4a: Layer-continuous timestamp is when the source resolves."""
    assert game_state.recorded_timestamp == 100


@given("a static ability becomes functional at game time 200")
def static_ability_functional_at_200(game_state):
    """Rule 6.3.4a: A static ability becomes functional."""
    game_state.source_card = game_state.create_card(name="Static Source Card")
    game_state.play_card_to_arena(game_state.source_card)
    game_state.static_ability_functional_time = 200
    game_state.static_continuous_effect = game_state.create_static_effect_becoming_functional_at_time(
        source=game_state.source_card,
        modifier="grant_go_again",
        game_time=game_state.static_ability_functional_time
    )


@when("the staging system records the timestamp of the static-continuous effect")
def staging_records_static_timestamp(game_state):
    """Rule 6.3.4a: The staging system records the timestamp of the static-continuous effect."""
    game_state.recorded_timestamp = game_state.get_effect_timestamp(
        game_state.static_continuous_effect
    )


@then("the timestamp of the static-continuous effect is game time 200")
def static_continuous_timestamp_is_200(game_state):
    """Rule 6.3.4a: Static-continuous timestamp is when the static ability becomes functional."""
    assert game_state.recorded_timestamp == 200


@given("two continuous effects start applying to an object at the same time")
def two_effects_same_timestamp(game_state):
    """Rule 6.3.4b: Two effects with the same timestamp."""
    game_state.target_card = game_state.create_card(name="Test Object")
    game_state.same_ts_effect_a = game_state.create_continuous_effect_with_timestamp(
        stage=8, substage=5, modifier="+1{p}", timestamp=50, target=game_state.target_card
    )
    game_state.same_ts_effect_b = game_state.create_continuous_effect_with_timestamp(
        stage=8, substage=5, modifier="+2{p}", timestamp=50, target=game_state.target_card
    )


@when("the turn-player decides the order of those effects")
def turn_player_decides_order(game_state):
    """Rule 6.3.4b: The turn-player decides the application order for same-timestamp effects."""
    # Turn-player chooses effect_b first, then effect_a
    game_state.decided_order_result = game_state.turn_player_decide_effect_order(
        effects=[game_state.same_ts_effect_a, game_state.same_ts_effect_b],
        chosen_order=[game_state.same_ts_effect_b, game_state.same_ts_effect_a]
    )


@then("that decided order is used for those effects in all substages")
def decided_order_used_in_all_substages(game_state):
    """Rule 6.3.4b: The decided order is used as the ordering for those effects."""
    assert game_state.decided_order_result.order_recorded
    assert game_state.decided_order_result.application_order[0] == game_state.same_ts_effect_b
    assert game_state.decided_order_result.application_order[1] == game_state.same_ts_effect_a


@given("two same-timestamp effects have been ordered by the turn-player")
def two_same_timestamp_effects_ordered(game_state):
    """Rule 6.3.4b: Two effects with the same timestamp whose order has been decided."""
    game_state.target_card = game_state.create_card(name="Test Object")
    game_state.effect_x = game_state.create_continuous_effect_with_timestamp(
        stage=8, substage=5, modifier="+1{p}", timestamp=75, target=game_state.target_card
    )
    game_state.effect_y = game_state.create_continuous_effect_with_timestamp(
        stage=8, substage=5, modifier="+2{p}", timestamp=75, target=game_state.target_card
    )
    game_state.decided_order = game_state.turn_player_decide_effect_order(
        effects=[game_state.effect_x, game_state.effect_y],
        chosen_order=[game_state.effect_x, game_state.effect_y]
    )


@when("the turn-player attempts to change the decided order")
def turn_player_attempts_to_change_order(game_state):
    """Rule 6.3.4b: The turn-player tries to change the order after deciding."""
    game_state.change_order_result = game_state.attempt_change_effect_order(
        decided_order=game_state.decided_order,
        new_order=[game_state.effect_y, game_state.effect_x]
    )


@then("the order change is rejected and the original order is maintained")
def order_change_rejected(game_state):
    """Rule 6.3.4b: The decided order is final and cannot be changed."""
    assert not game_state.change_order_result.order_changed
    assert game_state.change_order_result.maintained_order[0] == game_state.effect_x
    assert game_state.change_order_result.maintained_order[1] == game_state.effect_y


@given("two stage 8 add effects are already ordered in the substage for an object")
def two_effects_already_ordered(game_state):
    """Rule 6.3.4c: Two effects already exist in a substage."""
    game_state.target_card = game_state.create_card(name="Test Object", card_type="attack action", power=3)
    game_state.existing_effect_1 = game_state.create_continuous_effect_with_timestamp(
        stage=8, substage=5, modifier="+1{p}", timestamp=10, target=game_state.target_card
    )
    game_state.existing_effect_2 = game_state.create_continuous_effect_with_timestamp(
        stage=8, substage=5, modifier="+1{p}", timestamp=20, target=game_state.target_card
    )
    game_state.substage_ordered_effects = game_state.register_effects_in_substage(
        substage=5,
        effects=[game_state.existing_effect_1, game_state.existing_effect_2],
        target=game_state.target_card
    )


@given("a new stage 8 add effect is then applied to the same object")
def new_stage_8_effect_applied(game_state):
    """Rule 6.3.4c: A new effect is added to the same substage."""
    game_state.new_effect = game_state.create_continuous_effect_with_timestamp(
        stage=8, substage=5, modifier="+2{p}", timestamp=30, target=game_state.target_card
    )


@when("the staging system inserts the new effect")
def staging_inserts_new_effect(game_state):
    """Rule 6.3.4c: The staging system inserts the new effect into the substage ordering."""
    game_state.insertion_result = game_state.insert_effect_into_substage(
        substage_state=game_state.substage_ordered_effects,
        new_effect=game_state.new_effect
    )


@then("the new effect is ordered after the two existing effects in that substage")
def new_effect_ordered_after_existing(game_state):
    """Rule 6.3.4c: The new effect is placed at the end of the substage ordering."""
    ordered = game_state.insertion_result.ordered_effects
    assert len(ordered) == 3
    assert ordered[2] == game_state.new_effect


@given("a stage 8 add effect of +2 power is active on an attack")
def stage_8_add_2_active(game_state):
    """Rule 6.3.5: An existing +2 power effect is active."""
    game_state.target_card = game_state.create_card(name="Test Attack", card_type="attack action", power=3)
    game_state.existing_effect = game_state.create_staged_continuous_effect(
        stage=8, modifier="+2{p}", target=game_state.target_card
    )
    game_state.active_effects = [game_state.existing_effect]


@when("a new stage 8 add effect of +3 power is applied to the same attack")
def new_stage_8_add_3_applied(game_state):
    """Rule 6.3.5: A new effect is added, triggering recalculation."""
    game_state.new_power_effect = game_state.create_staged_continuous_effect(
        stage=8, modifier="+3{p}", target=game_state.target_card
    )
    game_state.active_effects.append(game_state.new_power_effect)
    game_state.recalculation_result = game_state.recalculate_all_effects(
        target=game_state.target_card,
        effects=game_state.active_effects
    )


@then("all effects are recalculated in staging order")
def all_effects_recalculated(game_state):
    """Rule 6.3.5: All effects are recalculated when any effect changes."""
    assert game_state.recalculation_result.all_recalculated


@then("the attack's power reflects contributions from both effects")
def power_reflects_both_effects(game_state):
    """Rule 6.3.5: Both +2 and +3 are applied; total = 3 + 2 + 3 = 8."""
    assert game_state.recalculation_result.final_power == 8


@given("a stage 8 effect grants +3 power to attacks with 3 or less base power")
def stage_8_minnowism_effect(game_state):
    """Rule 6.3.5a: A conditional stage 8 effect (like Minnowism)."""
    game_state.minnowism_effect = game_state.create_conditional_stage_effect(
        stage=8,
        modifier="+3{p}",
        condition="base_power_lte_3"
    )


@given("an attack currently has base power of 6 making it ineligible for that effect")
def attack_with_base_power_6(game_state):
    """Rule 6.3.5a: Attack starts with base power 6, ineligible for Minnowism."""
    game_state.target_card = game_state.create_card(
        name="Minnowism Test Attack", card_type="attack action", power=6
    )
    eligible = game_state.check_effect_eligibility(game_state.minnowism_effect, game_state.target_card)
    assert not eligible


@given("a stage 7 effect reduces the attack's base power to 3")
def stage_7_reduces_base_power_to_3(game_state):
    """Rule 6.3.5a: A stage 7 effect that reduces base power to 3."""
    game_state.base_power_reducer = game_state.create_staged_continuous_effect(
        stage=7,
        modifier="set_base_power_3",
        target=game_state.target_card
    )


@when("the staging system processes stage 7 first then stage 8")
def staging_processes_stage7_then_stage8(game_state):
    """Rule 6.3.5a: Process stages 7 then 8 dynamically."""
    game_state.dynamic_result = game_state.apply_effects_dynamically(
        effects=[game_state.base_power_reducer, game_state.minnowism_effect],
        target=game_state.target_card
    )


@then("the attack becomes eligible for the stage 8 effect after stage 7 processing")
def attack_becomes_eligible_after_stage7(game_state):
    """Rule 6.3.5a: After stage 7 reduces base power to 3, the attack is eligible."""
    assert game_state.dynamic_result.became_eligible_after_stage7


@then("the stage 8 effect is added and applied granting +3 power")
def stage_8_effect_added_and_applied(game_state):
    """Rule 6.3.5a: The Minnowism-style effect is added and applied."""
    assert game_state.dynamic_result.conditional_effect_applied
    assert game_state.dynamic_result.power_bonus == 3


@given("a stage 6 effect grants an ability only to objects with power above 5")
def stage_6_effect_for_power_above_5(game_state):
    """Rule 6.3.5b: A stage 6 effect conditional on power (which is evaluated in stage 8)."""
    game_state.stage6_conditional_effect = game_state.create_conditional_stage_effect(
        stage=6,
        modifier="grant_dominate",
        condition="power_above_5"
    )


@given("an attack has base power of 3 making it ineligible for the stage 6 effect")
def attack_with_base_power_3_ineligible(game_state):
    """Rule 6.3.5b: Attack starts with base power 3, ineligible for the stage 6 effect."""
    game_state.target_card = game_state.create_card(
        name="Non-Retroactive Test Attack", card_type="attack action", power=3
    )


@given("a stage 8 effect increases the attack's power to 6")
def stage_8_increases_power_to_6(game_state):
    """Rule 6.3.5b: A stage 8 effect that increases power to 6."""
    game_state.power_boost = game_state.create_staged_continuous_effect(
        stage=8,
        modifier="+3{p}",
        target=game_state.target_card
    )


@when("the staging system applies effects in order")
def staging_applies_effects_in_order(game_state):
    """Rule 6.3.5b: Effects are applied in stage order."""
    game_state.order_result = game_state.apply_effects_in_staging_order(
        effects=[game_state.stage6_conditional_effect, game_state.power_boost],
        target=game_state.target_card
    )


@then("the stage 6 effect is not retroactively applied after the stage 8 modification")
def stage_6_not_retroactively_applied(game_state):
    """Rule 6.3.5b: Stage 6 is not retroactively re-evaluated after stage 8 changes things."""
    assert not game_state.order_result.stage6_retroactively_applied


@then("the attack does not gain the stage-6 ability")
def attack_does_not_gain_stage6_ability(game_state):
    """Rule 6.3.5b: Dominate is not granted because the stage 6 check is not retroactive."""
    assert not game_state.order_result.ability_granted


@given("an object has a class supertype added by a separate continuous effect")
def object_has_class_supertype_from_effect(game_state):
    """Rule 6.3.6: Another continuous effect adds a class supertype to the object."""
    game_state.target_card = game_state.create_card(name="Test Object")
    game_state.class_adding_effect = game_state.create_staged_continuous_effect(
        stage=5,
        modifier="add_class_supertype_warrior",
        target=game_state.target_card
    )
    game_state.class_added_by_effect = "Warrior"


@given("an effect removes all class supertypes from the object")
def effect_removes_all_class_supertypes(game_state):
    """Rule 6.3.6: An Erase Face-style effect that removes class supertypes."""
    game_state.erase_effect = game_state.create_staged_continuous_effect(
        stage=5,
        modifier="remove_all_class_supertypes",
        target=game_state.target_card
    )


@when("both effects are applied")
def both_effects_applied(game_state):
    """Rule 6.3.6: Both effects are applied using the staging system."""
    game_state.remove_result = game_state.apply_effects_in_staging_order(
        effects=[game_state.erase_effect, game_state.class_adding_effect],
        target=game_state.target_card
    )


@then("the class supertype added by the separate effect is not removed")
def class_supertype_not_removed(game_state):
    """Rule 6.3.6: The remove-property effect does not remove properties added by other effects."""
    assert game_state.remove_result.retained_supertypes_from_other_effects


@then("the object retains the class supertype from the other effect")
def object_retains_class_supertype(game_state):
    """Rule 6.3.6: The Warrior supertype from the separate effect is retained."""
    assert game_state.class_added_by_effect in game_state.remove_result.final_supertypes


@given("a prevention effect explicitly prevents attacks from gaining go again")
def prevention_effect_blocks_go_again(game_state):
    """Rule 6.3.7: A Hypothermia-style effect preventing attacks from gaining go again."""
    game_state.attack_card = game_state.create_card(
        name="Hypothermia Test Attack", card_type="attack action"
    )
    game_state.prevention_effect = game_state.create_prevention_modification_effect(
        prevents="attacks_gaining_go_again"
    )


@given("an attack has go again as a base ability")
def attack_has_base_go_again(game_state):
    """Rule 6.3.7: The attack has go again as a base (printed) ability."""
    game_state.attack_card._has_base_go_again = True


@when("the effects are evaluated")
def effects_are_evaluated(game_state):
    """Rule 6.3.7: Evaluate all active effects."""
    game_state.evaluation_result = game_state.evaluate_prevention_effect(
        prevention_effect=game_state.prevention_effect,
        target=game_state.attack_card
    )


@then("the prevention effect blocks effects from adding go again")
def prevention_blocks_adding_go_again(game_state):
    """Rule 6.3.7: The effect explicitly prevents go again from being added."""
    assert game_state.evaluation_result.prevents_adding_go_again


@then("the attack retains its base go again ability unaffected by the prevention")
def attack_retains_base_go_again(game_state):
    """Rule 6.3.7: The prevention does not remove base/existing go again."""
    assert game_state.evaluation_result.base_go_again_preserved


@given("a prevention effect explicitly prevents attacks from gaining go again")
def prevention_effect_blocks_go_again_only(game_state):
    """Rule 6.3.7: Hypothermia-style effect preventing go again only."""
    game_state.attack_card = game_state.create_card(
        name="Another Test Attack", card_type="attack action"
    )
    game_state.prevention_effect = game_state.create_prevention_modification_effect(
        prevents="attacks_gaining_go_again"
    )


@given("an effect would give the attack +2 power")
def effect_gives_attack_plus_2_power(game_state):
    """Rule 6.3.7: A power modification that is not prevented by the prevention effect."""
    game_state.power_effect = game_state.create_staged_continuous_effect(
        stage=8,
        modifier="+2{p}",
        target=game_state.attack_card
    )


@when("both effects are evaluated")
def both_effects_are_evaluated(game_state):
    """Rule 6.3.7: Both effects are evaluated for the attack."""
    game_state.both_eval_result = game_state.evaluate_effects_with_prevention(
        prevention_effect=game_state.prevention_effect,
        other_effects=[game_state.power_effect],
        target=game_state.attack_card
    )


@then("the prevention effect does not block the power modification")
def prevention_does_not_block_power(game_state):
    """Rule 6.3.7: The prevention only blocks what it explicitly specifies."""
    assert not game_state.both_eval_result.power_modification_blocked


@then("the attack gains the +2 power bonus")
def attack_gains_plus_2_power(game_state):
    """Rule 6.3.7: The power modification is applied normally."""
    assert game_state.both_eval_result.power_bonus_applied == 2


# ===== Fixtures =====


@pytest.fixture
def game_state():
    """
    Fixture providing game state for testing Section 6.3: Continuous Effect Interactions.

    Uses BDDGameState which integrates with the real engine.
    Reference: Rules 6.3.1 - 6.3.7
    """
    from tests.bdd_helpers import BDDGameState

    state = BDDGameState()
    state.applied_stages = []
    state.applied_substages = []
    state.effect_application_order = []
    state.active_effects = []

    return state
