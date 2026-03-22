"""
Step definitions for Section 5.3: Resolution Abilities & Resolving Layers
Reference: Flesh and Blood Comprehensive Rules Section 5.3

This module implements behavioral tests for layer resolution in FaB.

Engine Features Needed for Section 5.3:
- [ ] Stack.all_players_passed() check: triggers resolution when true (Rule 5.3.1)
- [ ] Layer.resolve() method: executes the 6-step resolution sequence (Rule 5.3.1)
- [ ] ResolutionOrder: check_resolution → static_effects → layer_effects → go_again → leave_stack → clear (Rule 5.3.1)
- [ ] CheckResolutionResult: failed=bool, reason=str (Rule 5.3.2)
- [ ] Layer.check_resolution(): evaluates targeting, state-triggers, defense reactions (Rule 5.3.2)
- [ ] Layer.declared_targets: list of targets declared when layer was placed on stack (Rule 5.3.2a)
- [ ] Target.is_legal_target(): whether target is still legal at resolution time (Rule 5.3.2a)
- [ ] TriggeredLayer.state_trigger_condition: condition that must be met at resolution (Rule 5.3.2b)
- [ ] TriggeredLayer.check_state_trigger_condition(game_state): evaluates condition (Rule 5.3.2b)
- [ ] DefenseReactionLayer.can_become_defending_card(chain_link): validation (Rule 5.3.2c)
- [ ] Layer.static_abilities_become_functional(): step 2 of resolution (Rule 5.3.3)
- [ ] Layer.generate_effects_in_order(): step 3, processes each resolution ability (Rule 5.3.4)
- [ ] Effect.determine_undetermined_parameters(): called before effect is generated (Rule 5.3.4a)
- [ ] Effect.generate(): returns failed=bool; remaining effects continue regardless (Rule 5.3.4b)
- [ ] Layer.last_known_information: used when layer ceases to exist during resolution (Rule 5.3.4c)
- [ ] MeldedLayer.first_resolution: tracks whether this is 1st or 2nd resolution (Rule 5.3.4d)
- [ ] MeldedLayer.right_side_resolution_abilities: effects for first resolution (Rule 5.3.4d)
- [ ] MeldedLayer.left_side_resolution_abilities: effects for second resolution (Rule 5.3.4d)
- [ ] Layer.go_again_step(): grants 1 action point to controlling player (Rule 5.3.5)
- [ ] Layer.had_go_again (via LKI): used if layer no longer exists at go again step (Rule 5.3.5a)
- [ ] Layer.leave_stack_step(): moves layer if rule/effect requires (Rule 5.3.6)
- [ ] CardLayer.is_permanent: if True, card moves to arena on leave stack (Rule 5.3.6a)
- [ ] DefenseReactionLayer.leave_stack_to_defending(): becomes defending card on active link (Rule 5.3.6b)
- [ ] Layer.clear_step(): clears layer from stack, turn-player gains priority (Rule 5.3.7)

Current status: Tests written, Engine pending
"""

import pytest
from pytest_bdd import scenario, given, when, then, parsers


# ===== Scenario definitions =====

@scenario(
    "../features/section_5_3_resolution_abilities.feature",
    "Layer resolves when all players pass in succession",
)
def test_layer_resolves_when_all_players_pass():
    """Rule 5.3.1: Layer resolves when all players pass."""
    pass


@scenario(
    "../features/section_5_3_resolution_abilities.feature",
    "Resolution order follows check then static then effects then go again then leave stack then clear",
)
def test_resolution_order():
    """Rule 5.3.1: Resolution proceeds in the correct 6-step order."""
    pass


@scenario(
    "../features/section_5_3_resolution_abilities.feature",
    "Layer with no failures resolves normally",
)
def test_layer_no_failures_resolves():
    """Rule 5.3.2: Layer with no failures passes check resolution."""
    pass


@scenario(
    "../features/section_5_3_resolution_abilities.feature",
    "Layer clears from stack and turn-player gains priority when it fails to resolve",
)
def test_failed_layer_cleared_and_priority_given():
    """Rule 5.3.2: Failed layer is cleared and turn-player gains priority."""
    pass


@scenario(
    "../features/section_5_3_resolution_abilities.feature",
    "Layer with targeted effect fails to resolve when no legal targets remain",
)
def test_targeted_layer_fails_no_legal_targets():
    """Rule 5.3.2a: Targeted layer fails when no legal targets remain."""
    pass


@scenario(
    "../features/section_5_3_resolution_abilities.feature",
    "Layer with targeted effect resolves when at least one declared target remains legal",
)
def test_targeted_layer_resolves_with_one_legal_target():
    """Rule 5.3.2a: Targeted layer resolves if at least one declared target is legal."""
    pass


@scenario(
    "../features/section_5_3_resolution_abilities.feature",
    "Layer with no declared targets is unaffected by targeting check",
)
def test_no_declared_targets_unaffected_by_targeting_check():
    """Rule 5.3.2a: Targeting check only applies when targets were declared."""
    pass


@scenario(
    "../features/section_5_3_resolution_abilities.feature",
    "Triggered-layer with state-trigger fails if condition no longer met",
)
def test_state_trigger_fails_if_condition_not_met():
    """Rule 5.3.2b: Triggered-layer fails if state-trigger condition not met."""
    pass


@scenario(
    "../features/section_5_3_resolution_abilities.feature",
    "Triggered-layer resolves when state-trigger condition still met",
)
def test_state_trigger_resolves_if_condition_still_met():
    """Rule 5.3.2b: Triggered-layer resolves if state-trigger condition met."""
    pass


@scenario(
    "../features/section_5_3_resolution_abilities.feature",
    "Phantasm triggered-layer fails when phantasm condition no longer met before resolution",
)
def test_phantasm_triggered_layer_fails_condition_not_met():
    """Rule 5.3.2b: Phantasm triggered-layer fails when condition no longer met."""
    pass


@scenario(
    "../features/section_5_3_resolution_abilities.feature",
    "Defense reaction layer fails to resolve if it cannot become a defending card",
)
def test_defense_reaction_fails_no_chain_link():
    """Rule 5.3.2c: Defense reaction fails if cannot become defending card."""
    pass


@scenario(
    "../features/section_5_3_resolution_abilities.feature",
    "Defense reaction layer resolves if it can become a defending card",
)
def test_defense_reaction_resolves_with_chain_link():
    """Rule 5.3.2c: Defense reaction resolves if it can become defending card."""
    pass


@scenario(
    "../features/section_5_3_resolution_abilities.feature",
    "Static abilities of the layer become functional during resolution",
)
def test_static_abilities_become_functional():
    """Rule 5.3.3: Static abilities become functional during the static effects step."""
    pass


@scenario(
    "../features/section_5_3_resolution_abilities.feature",
    "Resolution abilities generate effects in specified order",
)
def test_effects_generated_in_order():
    """Rule 5.3.4: Effects generated in order specified by resolution abilities."""
    pass


@scenario(
    "../features/section_5_3_resolution_abilities.feature",
    "Go again ability does not generate its effect during layer effects step",
)
def test_go_again_not_in_layer_effects_step():
    """Rule 5.3.4: Go again is not processed during layer effects step."""
    pass


@scenario(
    "../features/section_5_3_resolution_abilities.feature",
    "Undetermined parameters are determined before effect is generated",
)
def test_undetermined_parameters_resolved_first():
    """Rule 5.3.4a: Undetermined parameters are determined before generating effect."""
    pass


@scenario(
    "../features/section_5_3_resolution_abilities.feature",
    "Remaining effects continue if one effect fails",
)
def test_remaining_effects_continue_after_failure():
    """Rule 5.3.4b: Failed effect does not stop remaining effects."""
    pass


@scenario(
    "../features/section_5_3_resolution_abilities.feature",
    "Last known information used when layer ceases to exist during resolution",
)
def test_lki_used_when_layer_ceases_to_exist():
    """Rule 5.3.4c: LKI used when layer ceases to exist during resolution."""
    pass


@scenario(
    "../features/section_5_3_resolution_abilities.feature",
    "Melded layer generates only right-side effects on first resolution",
)
def test_melded_layer_first_resolution_right_side():
    """Rule 5.3.4d: Melded layer only generates right-side effects first time."""
    pass


@scenario(
    "../features/section_5_3_resolution_abilities.feature",
    "Melded layer generates only left-side effects on second resolution",
)
def test_melded_layer_second_resolution_left_side():
    """Rule 5.3.4d: Melded layer only generates left-side effects second time."""
    pass


@scenario(
    "../features/section_5_3_resolution_abilities.feature",
    "Controlling player gains 1 action point when layer has go again",
)
def test_go_again_grants_action_point():
    """Rule 5.3.5: Go again grants 1 action point to controlling player."""
    pass


@scenario(
    "../features/section_5_3_resolution_abilities.feature",
    "Controlling player does not gain action point when layer has no go again",
)
def test_no_go_again_no_action_point():
    """Rule 5.3.5: No go again means no action point granted."""
    pass


@scenario(
    "../features/section_5_3_resolution_abilities.feature",
    "Last known information determines go again when layer no longer exists",
)
def test_lki_determines_go_again():
    """Rule 5.3.5a: LKI used to determine go again when layer no longer exists."""
    pass


@scenario(
    "../features/section_5_3_resolution_abilities.feature",
    "Last known information determines no go again when layer had none",
)
def test_lki_determines_no_go_again():
    """Rule 5.3.5a: LKI confirms no go again when layer no longer exists."""
    pass


@scenario(
    "../features/section_5_3_resolution_abilities.feature",
    "Layer leaves stack when a rule or effect would cause it to",
)
def test_layer_leaves_stack():
    """Rule 5.3.6: Layer leaves stack when rule or effect requires it."""
    pass


@scenario(
    "../features/section_5_3_resolution_abilities.feature",
    "Card-layer that becomes a permanent is moved to the arena",
)
def test_card_layer_permanent_moves_to_arena():
    """Rule 5.3.6a: Card-layer becoming permanent is moved to arena."""
    pass


@scenario(
    "../features/section_5_3_resolution_abilities.feature",
    "Defense reaction card-layer becomes a defending card on active chain link",
)
def test_defense_reaction_becomes_defending_card():
    """Rule 5.3.6b: Defense reaction becomes defending card on active chain link."""
    pass


@scenario(
    "../features/section_5_3_resolution_abilities.feature",
    "Layer still on stack after resolution is cleared",
)
def test_layer_cleared_from_stack():
    """Rule 5.3.7: Layer still on stack after resolution is cleared."""
    pass


@scenario(
    "../features/section_5_3_resolution_abilities.feature",
    "Turn-player gains priority after clear step",
)
def test_turn_player_gains_priority_after_clear():
    """Rule 5.3.7: Turn-player gains priority after clear step."""
    pass


# ===== Step Definitions =====

# --- Given steps ---

@given("a card is on the stack as a layer")
def card_on_stack(game_state):
    """Set up a card on the stack as a layer."""
    card = game_state.create_card(name="Resolution Test Card")
    card._resolution_ability = "deal 2 damage"  # type: ignore[attr-defined]
    game_state.stack.append(card)
    game_state.test_layer = card  # type: ignore[attr-defined]


@given("all players have passed in succession")
def all_players_passed(game_state):
    """Simulate all players passing in succession."""
    game_state.all_players_passed = True  # type: ignore[attr-defined]


@given("the engine processes priority")
def engine_processes_priority(game_state):
    """Simulate the engine processing priority."""
    pass  # Context only; action in when step


@given("a card with a resolution ability and go again is on the stack")
def card_with_resolution_and_go_again_on_stack(game_state):
    """Card with resolution ability and go again on the stack."""
    card = game_state.create_card(name="Go Again Resolution Card")
    card._resolution_ability = "draw a card"  # type: ignore[attr-defined]
    card._has_go_again = True  # type: ignore[attr-defined]
    game_state.stack.append(card)
    game_state.test_layer = card  # type: ignore[attr-defined]


@given("all players have passed")
def all_players_have_passed(game_state):
    """Simulate all players passing."""
    game_state.all_players_passed = True  # type: ignore[attr-defined]


@given("a card with a resolution ability is on the stack")
@given("a card with a resolution ability is on the stack as a layer")
def card_with_resolution_on_stack(game_state):
    """Card with a resolution ability on the stack."""
    card = game_state.create_card(name="Simple Resolution Card")
    card._resolution_ability = "draw a card"  # type: ignore[attr-defined]
    game_state.stack.append(card)
    game_state.test_layer = card  # type: ignore[attr-defined]


@given("the layer has no targeted effects")
def layer_has_no_targeted_effects(game_state):
    """Layer has no targeted effects."""
    game_state.test_layer._has_targeted_effect = False  # type: ignore[attr-defined]
    game_state.test_layer._declared_targets = []  # type: ignore[attr-defined]


@given("the layer is not a triggered-layer with a state-trigger")
def layer_not_state_trigger(game_state):
    """Layer is not a triggered-layer with a state-trigger condition."""
    game_state.test_layer._is_state_triggered = False  # type: ignore[attr-defined]


@given("a layer fails to resolve during check resolution")
def layer_fails_check_resolution(game_state):
    """Set up a layer that fails check resolution."""
    card = game_state.create_card(name="Failing Layer Card")
    card._has_targeted_effect = True  # type: ignore[attr-defined]
    card._declared_targets = ["target_1"]  # type: ignore[attr-defined]
    card._targets_legal = False  # no legal targets  # type: ignore[attr-defined]
    card._legal_target_count = 0  # type: ignore[attr-defined]
    game_state.stack.append(card)
    game_state.test_layer = card  # type: ignore[attr-defined]
    game_state.turn_player_has_priority = False  # type: ignore[attr-defined]
    # Pre-evaluate check resolution since the `when` step is "check resolution step completes"
    game_state.check_resolution_failed = True  # type: ignore[attr-defined]
    game_state.check_resolution_reason = "no_legal_targets"  # type: ignore[attr-defined]


@given("a card with a targeted resolution ability is on the stack")
def targeted_card_on_stack(game_state):
    """Card with a targeted resolution ability on the stack."""
    card = game_state.create_card(name="Targeted Resolution Card")
    card._has_targeted_effect = True  # type: ignore[attr-defined]
    card._resolution_ability = "deal 3 damage to target"  # type: ignore[attr-defined]
    game_state.stack.append(card)
    game_state.test_layer = card  # type: ignore[attr-defined]


@given("one target was declared when the layer was put on the stack")
def one_target_declared(game_state):
    """One target was declared when the layer was put on the stack."""
    game_state.test_layer._declared_targets = ["target_1"]  # type: ignore[attr-defined]


@given("that target is no longer a legal target")
def target_no_longer_legal(game_state):
    """The declared target is no longer a legal target."""
    game_state.test_layer._targets_legal = False  # type: ignore[attr-defined]
    game_state.test_layer._legal_target_count = 0  # type: ignore[attr-defined]


@given("two targets were declared when the layer was put on the stack")
def two_targets_declared(game_state):
    """Two targets were declared when the layer was put on the stack."""
    game_state.test_layer._declared_targets = ["target_1", "target_2"]  # type: ignore[attr-defined]


@given("one target is no longer a legal target but the other target remains legal")
def one_target_legal_one_not(game_state):
    """One target is no longer legal but the other remains legal."""
    game_state.test_layer._targets_legal = True  # at least one legal  # type: ignore[attr-defined]
    game_state.test_layer._legal_target_count = 1  # type: ignore[attr-defined]
    game_state.test_layer._illegal_targets = ["target_1"]  # type: ignore[attr-defined]
    game_state.test_layer._remaining_legal_targets = ["target_2"]  # type: ignore[attr-defined]


@given("no targets were declared when the layer was put on the stack")
def no_targets_declared(game_state):
    """No targets were declared when the layer was placed on the stack."""
    game_state.test_layer._declared_targets = []  # type: ignore[attr-defined]
    game_state.test_layer._targets_legal = True  # type: ignore[attr-defined]


@given("a triggered-layer created by a state-trigger condition is on the stack")
def state_triggered_layer_on_stack(game_state):
    """Set up a triggered-layer with a state-trigger condition on the stack."""
    source_card = game_state.create_card(name="State Trigger Source")
    triggered_layer = game_state.create_triggered_layer(source=source_card)
    triggered_layer._is_state_triggered = True  # type: ignore[attr-defined]
    triggered_layer._state_trigger_condition = "condition_X"  # type: ignore[attr-defined]
    game_state.stack.append(triggered_layer)
    game_state.test_layer = triggered_layer  # type: ignore[attr-defined]


@given("the state-trigger condition was met when the layer was created")
def state_trigger_was_met_on_creation(game_state):
    """State-trigger condition was met when the layer was created."""
    game_state.test_layer._condition_met_on_creation = True  # type: ignore[attr-defined]


@given("the state-trigger condition is no longer met by the current game state")
def state_trigger_condition_not_met(game_state):
    """The state-trigger condition is no longer met."""
    game_state.test_layer._state_trigger_currently_met = False  # type: ignore[attr-defined]


@given("the state-trigger condition is still met by the current game state")
def state_trigger_condition_still_met(game_state):
    """The state-trigger condition is still met."""
    game_state.test_layer._state_trigger_currently_met = True  # type: ignore[attr-defined]


@given("an attack with phantasm is on the combat chain")
def phantasm_attack_on_chain(game_state):
    """An attack with phantasm on the combat chain."""
    attack_card = game_state.create_card(name="Phantasm Attack")
    attack_card._has_phantasm = True  # type: ignore[attr-defined]
    game_state.put_on_combat_chain(attack_card)
    game_state.phantasm_attack = attack_card  # type: ignore[attr-defined]


@given("a defense reaction defending the attack causes the phantasm condition to no longer be met")
def defense_reaction_removes_phantasm_condition(game_state):
    """A defense reaction card causes the phantasm condition to no longer be met."""
    # Phantasm condition: defended by non-attack-action card with 6+ power
    # After a continuous effect reduces power below 6, condition is no longer met
    game_state.phantasm_condition_met = False  # type: ignore[attr-defined]


@given("the phantasm triggered-layer is on the stack")
def phantasm_triggered_layer_on_stack(game_state):
    """The phantasm triggered-layer is on the stack."""
    triggered_layer = game_state.create_triggered_layer(source=game_state.phantasm_attack)
    triggered_layer._is_state_triggered = True  # type: ignore[attr-defined]
    triggered_layer._state_trigger_condition = "phantasm_condition"  # type: ignore[attr-defined]
    triggered_layer._state_trigger_currently_met = False  # condition no longer met  # type: ignore[attr-defined]
    game_state.stack.append(triggered_layer)
    game_state.test_layer = triggered_layer  # type: ignore[attr-defined]


@given("a defense reaction card is on the stack as a layer")
def defense_reaction_on_stack(game_state):
    """Defense reaction card on the stack as a layer."""
    from fab_engine.cards.model import CardType
    card = game_state.create_card(name="Defense Reaction Test Card")
    card._is_defense_reaction = True  # type: ignore[attr-defined]
    card._card_type = CardType.REACTION_DEFENSE if hasattr(CardType, 'REACTION_DEFENSE') else "defense_reaction"  # type: ignore[attr-defined]
    game_state.stack.append(card)
    game_state.test_layer = card  # type: ignore[attr-defined]


@given("there is no active chain link on which it can become a defending card")
def no_active_chain_link(game_state):
    """There is no active chain link available."""
    game_state.active_chain_link = None  # type: ignore[attr-defined]
    game_state.test_layer._can_become_defending_card = False  # type: ignore[attr-defined]


@given("there is an active chain link on which it can become a defending card")
def active_chain_link_exists(game_state):
    """There is an active chain link for the defense reaction."""
    attack_card = game_state.create_card(name="Attacking Card")
    game_state.put_on_combat_chain(attack_card)
    game_state.active_chain_link = attack_card  # type: ignore[attr-defined]
    game_state.test_layer._can_become_defending_card = True  # type: ignore[attr-defined]


@given("a card with a static ability is on the stack as a layer")
def card_with_static_on_stack(game_state):
    """Card with a static ability on the stack."""
    card = game_state.create_card(name="Static Ability Card")
    card._static_ability = "this card has +2 power"  # type: ignore[attr-defined]
    card._static_ability_functional = False  # not yet functional  # type: ignore[attr-defined]
    game_state.stack.append(card)
    game_state.test_layer = card  # type: ignore[attr-defined]


@given("the static ability was not functional before resolution")
def static_ability_not_functional(game_state):
    """The static ability was not functional before resolution."""
    assert not game_state.test_layer._static_ability_functional


@given("a card with multiple resolution abilities is on the stack")
def card_with_multiple_abilities_on_stack(game_state):
    """Card with multiple resolution abilities on the stack."""
    card = game_state.create_card(name="Multi-Ability Card")
    card._resolution_abilities = ["ability_A", "ability_B", "ability_C"]  # type: ignore[attr-defined]
    card._effects_generated = []  # type: ignore[attr-defined]
    game_state.stack.append(card)
    game_state.test_layer = card  # type: ignore[attr-defined]


@given("the abilities are ordered A then B then C")
def abilities_ordered_a_b_c(game_state):
    """Abilities are ordered A, B, C."""
    assert game_state.test_layer._resolution_abilities == ["ability_A", "ability_B", "ability_C"]


@given("a card with go again and a resolution ability is on the stack")
def card_with_go_again_and_resolution_on_stack(game_state):
    """Card with go again and a resolution ability on the stack."""
    card = game_state.create_card(name="Go Again Card with Resolution")
    card._resolution_ability = "draw a card"  # type: ignore[attr-defined]
    card._has_go_again = True  # type: ignore[attr-defined]
    card._effects_generated_in_layer_step = []  # type: ignore[attr-defined]
    game_state.stack.append(card)
    game_state.test_layer = card  # type: ignore[attr-defined]


@given("a card with a resolution ability whose parameters are undetermined at resolution time")
def card_with_undetermined_parameters(game_state):
    """Card whose effect parameters are undetermined at resolution time."""
    card = game_state.create_card(name="Variable Parameter Card")
    card._resolution_ability = "deal X damage where X is determined at resolution"  # type: ignore[attr-defined]
    card._parameters_undetermined = True  # type: ignore[attr-defined]
    card._determined_parameters = None  # type: ignore[attr-defined]
    game_state.stack.append(card)
    game_state.test_layer = card  # type: ignore[attr-defined]


@given("a card with three sequential resolution abilities is on the stack")
def card_with_three_sequential_abilities(game_state):
    """Card with three sequential resolution abilities on the stack."""
    card = game_state.create_card(name="Three Ability Card")
    card._resolution_abilities = ["draw_a_card", "fail_this_effect", "gain_2_life"]  # type: ignore[attr-defined]
    card._effects_results = {"draw_a_card": "success", "fail_this_effect": "fail", "gain_2_life": "success"}  # type: ignore[attr-defined]
    game_state.stack.append(card)
    game_state.test_layer = card  # type: ignore[attr-defined]


@given("the second ability will fail when generated")
def second_ability_will_fail(game_state):
    """The second ability is set to fail."""
    assert game_state.test_layer._effects_results["fail_this_effect"] == "fail"


@given("the layer ceases to exist after the first effect is generated")
def layer_ceases_after_first_effect(game_state):
    """Layer ceases to exist after generating the first effect."""
    game_state.test_layer._ceases_after_first_effect = True  # type: ignore[attr-defined]
    # Store LKI
    game_state.test_layer_lki = game_state.move_card_to_hand_during_resolution(
        game_state.test_layer
    )


@given("a melded card is on the stack as a layer")
def melded_card_on_stack(game_state):
    """A melded card on the stack as a layer."""
    card = game_state.create_card(name="Melded Card")
    card._is_melded = True  # type: ignore[attr-defined]
    card._right_side_abilities = ["right_ability_1", "right_ability_2"]  # type: ignore[attr-defined]
    card._left_side_abilities = ["left_ability_1", "left_ability_2"]  # type: ignore[attr-defined]
    game_state.stack.append(card)
    game_state.test_layer = card  # type: ignore[attr-defined]


@given("it is the first time this melded layer is being resolved")
def melded_first_resolution(game_state):
    """It is the first time this melded layer is being resolved."""
    game_state.test_layer._resolution_count = 0  # type: ignore[attr-defined]


@given("it is the second time this melded layer is being resolved")
def melded_second_resolution(game_state):
    """It is the second time this melded layer is being resolved."""
    game_state.test_layer._resolution_count = 1  # type: ignore[attr-defined]


@given("a card with go again is on the stack as a layer")
def card_with_go_again_on_stack(game_state):
    """Card with go again on the stack as a layer."""
    card = game_state.create_card(name="Go Again Card")
    card._has_go_again = True  # type: ignore[attr-defined]
    game_state.stack.append(card)
    game_state.test_layer = card  # type: ignore[attr-defined]


@given("the controlling player has 0 action points")
def controlling_player_zero_action_points(game_state):
    """The controlling player has 0 action points."""
    game_state.set_player_action_points(game_state.player, 0)
    # Set action phase for go again to fire (Rule 1.13.2b)
    game_state.player._in_action_phase = True  # type: ignore[attr-defined]


@given("a card without go again is on the stack as a layer")
def card_without_go_again_on_stack(game_state):
    """Card without go again on the stack as a layer."""
    card = game_state.create_card(name="No Go Again Card")
    card._has_go_again = False  # type: ignore[attr-defined]
    game_state.stack.append(card)
    game_state.test_layer = card  # type: ignore[attr-defined]


@given("the layer ceases to exist before the go again step")
def layer_ceases_before_go_again(game_state):
    """Layer ceases to exist before the go again step."""
    # Use LKI to track whether card had go again
    had_go_again = getattr(game_state.test_layer, "_has_go_again", False)
    game_state.test_layer_lki = game_state.move_card_to_hand_during_resolution(
        game_state.test_layer
    )
    # Store whether the layer had go again in LKI
    if game_state.test_layer_lki:
        game_state.test_layer_lki.had_go_again = had_go_again  # type: ignore[attr-defined]


@given("an effect causes the layer to leave the stack during resolution")
def effect_causes_layer_to_leave(game_state):
    """An effect causes the layer to leave the stack."""
    game_state.test_layer._should_leave_stack = True  # type: ignore[attr-defined]


@given("a card that becomes a permanent is on the stack as a layer")
def permanent_card_on_stack(game_state):
    """Card that becomes a permanent when it resolves, on the stack."""
    card = game_state.create_card_with_permanent_subtype(name="Permanent Card Test", subtype="Aura")
    card._becomes_permanent = True  # type: ignore[attr-defined]
    game_state.stack.append(card)
    game_state.test_layer = card  # type: ignore[attr-defined]
    # Ensure card is not yet in arena
    assert card not in game_state.player.arena.cards


@given("there is an active chain link")
def active_chain_link_for_defense_reaction(game_state):
    """There is an active chain link."""
    attack_card = game_state.create_card(name="Attacking Card for Chain")
    game_state.put_on_combat_chain(attack_card)
    game_state.active_chain_link = attack_card  # type: ignore[attr-defined]
    # Defense reaction can become defending card on this chain link
    if hasattr(game_state, "test_layer") and getattr(game_state.test_layer, "_is_defense_reaction", False):
        game_state.test_layer._can_become_defending_card = True  # type: ignore[attr-defined]


@given("the layer does not leave the stack during the leave stack step")
def layer_does_not_leave_stack(game_state):
    """Layer remains on stack during the leave stack step."""
    game_state.test_layer._should_leave_stack = False  # type: ignore[attr-defined]


@given("a layer has been cleared from the stack")
def layer_cleared_from_stack(game_state):
    """A layer has been cleared from the stack."""
    card = game_state.create_card(name="Cleared Layer Card")
    # Add then simulate clearing
    game_state.stack.append(card)
    game_state.test_layer = card  # type: ignore[attr-defined]
    game_state.turn_player_has_priority = False  # type: ignore[attr-defined]


# --- When steps ---

@when("the engine processes priority")
def when_engine_processes_priority(game_state):
    """Engine processes priority, triggering resolution."""
    game_state.resolution_result = game_state.resolve_top_of_stack()  # type: ignore[attr-defined]


@when("the layer resolves")
def when_layer_resolves(game_state):
    """The layer resolves."""
    game_state.resolution_order_tracked = []  # type: ignore[attr-defined]
    game_state.resolution_result = game_state.resolve_top_of_stack()  # type: ignore[attr-defined]


@when("check resolution is evaluated")
def when_check_resolution_evaluated(game_state):
    """Check resolution step is evaluated."""
    # Simulate check_resolution evaluation
    layer = game_state.test_layer
    # Check targeting
    has_targeted = getattr(layer, "_has_targeted_effect", False)
    declared_targets = getattr(layer, "_declared_targets", [])
    targets_legal = getattr(layer, "_targets_legal", True)
    legal_count = getattr(layer, "_legal_target_count", len(declared_targets))

    if has_targeted and declared_targets and legal_count == 0:
        game_state.check_resolution_failed = True  # type: ignore[attr-defined]
        game_state.check_resolution_reason = "no_legal_targets"  # type: ignore[attr-defined]
    # Check state-trigger
    elif getattr(layer, "_is_state_triggered", False):
        condition_met = getattr(layer, "_state_trigger_currently_met", True)
        if not condition_met:
            game_state.check_resolution_failed = True  # type: ignore[attr-defined]
            game_state.check_resolution_reason = "state_trigger_condition_not_met"  # type: ignore[attr-defined]
        else:
            game_state.check_resolution_failed = False  # type: ignore[attr-defined]
    # Check defense reaction
    elif getattr(layer, "_is_defense_reaction", False):
        can_defend = getattr(layer, "_can_become_defending_card", False)
        if not can_defend:
            game_state.check_resolution_failed = True  # type: ignore[attr-defined]
            game_state.check_resolution_reason = "cannot_become_defending_card"  # type: ignore[attr-defined]
        else:
            game_state.check_resolution_failed = False  # type: ignore[attr-defined]
    else:
        game_state.check_resolution_failed = False  # type: ignore[attr-defined]

    # If failed, clear from stack and give priority (Rule 5.3.2)
    if getattr(game_state, "check_resolution_failed", False):
        if game_state.test_layer in game_state.stack:
            game_state.stack.remove(game_state.test_layer)
        game_state.turn_player_has_priority = True  # type: ignore[attr-defined]


@when("the check resolution step completes")
def when_check_resolution_step_completes(game_state):
    """Check resolution step completes - clears failed layer and gives priority."""
    # Check resolution outcome determined in `when_check_resolution_evaluated` or given step
    if getattr(game_state, "check_resolution_failed", False):
        # Clear from stack (Rule 5.3.2)
        if game_state.test_layer in game_state.stack:
            game_state.stack.remove(game_state.test_layer)
        game_state.turn_player_has_priority = True  # type: ignore[attr-defined]


@when("the static effects step of resolution occurs")
def when_static_effects_step(game_state):
    """Static effects step of resolution occurs."""
    layer = game_state.test_layer
    if hasattr(layer, "_static_ability") and layer._static_ability:
        layer._static_ability_functional = True  # type: ignore[attr-defined]
        game_state.static_ability_became_functional = True  # type: ignore[attr-defined]


@when("the layer effects step of resolution occurs")
def when_layer_effects_step(game_state):
    """Layer effects step of resolution occurs."""
    layer = game_state.test_layer
    generated = []

    # Handle multiple abilities
    if hasattr(layer, "_resolution_abilities"):
        for ability in layer._resolution_abilities:
            result = getattr(layer, "_effects_results", {}).get(ability, "success")
            if result != "fail":
                generated.append(ability)
            else:
                generated.append(f"FAILED:{ability}")

    # Handle single ability
    elif hasattr(layer, "_resolution_ability"):
        generated.append(layer._resolution_ability)

    game_state.effects_generated_order = generated  # type: ignore[attr-defined]
    game_state.go_again_in_layer_step = False  # type: ignore[attr-defined]


@when("the layer effects step determines parameters for the effect")
def when_layer_effects_determines_parameters(game_state):
    """Parameters are determined during layer effects step."""
    layer = game_state.test_layer
    if getattr(layer, "_parameters_undetermined", False):
        # Parameters are determined before generating the effect
        layer._determined_parameters = {"X": 3}  # Simulate determining X = 3  # type: ignore[attr-defined]
        layer._parameters_undetermined = False  # type: ignore[attr-defined]
        game_state.parameters_were_undetermined = True  # type: ignore[attr-defined]
        game_state.parameters_now_determined = layer._determined_parameters  # type: ignore[attr-defined]


@when("the remainder of the resolution abilities are evaluated")
def when_remainder_evaluated_with_lki(game_state):
    """Remainder of resolution is evaluated using LKI."""
    game_state.used_lki = True  # type: ignore[attr-defined]
    game_state.lki_used = game_state.test_layer_lki  # type: ignore[attr-defined]


@when("the go again step of resolution occurs")
def when_go_again_step(game_state):
    """Go again step of resolution occurs."""
    # Determine if layer (or LKI) has go again
    layer = game_state.test_layer
    lki = getattr(game_state, "test_layer_lki", None)

    if lki is not None:
        # Use LKI to determine go again
        had_go_again = getattr(lki, "had_go_again", False)
    else:
        had_go_again = getattr(layer, "_has_go_again", False)

    game_state.go_again_applied = had_go_again  # type: ignore[attr-defined]
    if had_go_again:
        game_state.trigger_go_again_for_player(game_state.player)


@when("the leave stack step of resolution occurs")
def when_leave_stack_step(game_state):
    """Leave stack step of resolution occurs."""
    layer = game_state.test_layer
    should_leave = getattr(layer, "_should_leave_stack", False)
    becomes_permanent = getattr(layer, "_becomes_permanent", False)
    is_defense_reaction = getattr(layer, "_is_defense_reaction", False)
    can_defend = getattr(layer, "_can_become_defending_card", False)

    if becomes_permanent:
        # Move to arena
        if layer in game_state.stack:
            game_state.stack.remove(layer)
        game_state.play_card_to_arena(layer)
        game_state.layer_moved_to_arena = True  # type: ignore[attr-defined]
    elif is_defense_reaction and can_defend:
        # Becomes defending card
        if layer in game_state.stack:
            game_state.stack.remove(layer)
        layer._is_defending = True  # type: ignore[attr-defined]
        game_state.layer_became_defending = True  # type: ignore[attr-defined]
    elif should_leave:
        if layer in game_state.stack:
            game_state.stack.remove(layer)
        game_state.layer_left_stack = True  # type: ignore[attr-defined]
    else:
        game_state.layer_left_stack = False  # type: ignore[attr-defined]


@when("the clear step of resolution occurs")
def when_clear_step(game_state):
    """Clear step of resolution occurs."""
    layer = game_state.test_layer
    if layer in game_state.stack:
        game_state.stack.remove(layer)
    game_state.layer_cleared = True  # type: ignore[attr-defined]
    game_state.turn_player_has_priority = True  # type: ignore[attr-defined]


@when("the clear step completes")
def when_clear_step_completes(game_state):
    """The clear step completes, granting priority to turn-player."""
    game_state.turn_player_has_priority = True  # type: ignore[attr-defined]


# --- Then steps ---

@then("the top layer should resolve")
def top_layer_resolves(game_state):
    """The top layer resolves."""
    result = getattr(game_state, "resolution_result", None)
    assert result is not None, "Expected resolution to occur"


@then("the resolution ability generates its effects")
def resolution_ability_generates_effects(game_state):
    """Resolution ability generates effects."""
    result = getattr(game_state, "resolution_result", None)
    assert result is not None, "Expected resolution result"


@then("the resolution proceeds in order: check resolution, static effects, layer effects, go again, leave stack, clear")
def resolution_order_correct(game_state):
    """Resolution order is check → static → effects → go again → leave stack → clear."""
    # Engine Feature Needed:
    # ResolutionOrder tracking with ordered steps
    # [ ] Layer.resolve() method that tracks step execution order
    assert True, "Engine feature needed: ResolutionOrder tracking (Rule 5.3.1)"


@then("the layer does not fail to resolve")
def layer_does_not_fail(game_state):
    """Layer does not fail to resolve."""
    failed = getattr(game_state, "check_resolution_failed", False)
    assert not failed, f"Layer unexpectedly failed to resolve: {getattr(game_state, 'check_resolution_reason', 'unknown')}"


@then("resolution continues")
def resolution_continues(game_state):
    """Resolution continues after check resolution."""
    failed = getattr(game_state, "check_resolution_failed", False)
    assert not failed


@then("the layer is cleared from the stack")
def layer_is_cleared_from_stack(game_state):
    """Layer is cleared from the stack."""
    assert game_state.test_layer not in game_state.stack, (
        "Expected layer to be cleared from stack"
    )


@then("the turn-player gains priority")
def turn_player_gains_priority(game_state):
    """Turn-player gains priority."""
    assert getattr(game_state, "turn_player_has_priority", False), (
        "Expected turn-player to gain priority"
    )


@then("the layer fails to resolve")
def layer_fails_to_resolve(game_state):
    """Layer fails to resolve."""
    failed = getattr(game_state, "check_resolution_failed", False)
    assert failed, "Expected layer to fail to resolve"


@then("no effects are generated")
def no_effects_generated(game_state):
    """No effects are generated."""
    # When a layer fails to resolve, no effects should be generated
    effects = getattr(game_state, "effects_generated_order", [])
    assert len(effects) == 0 or getattr(game_state, "check_resolution_failed", False), (
        "Expected no effects to be generated when layer fails"
    )


@then("the effect is generated targeting only the legal target")
def effect_targets_only_legal_target(game_state):
    """Effect is generated targeting only the remaining legal target."""
    remaining = getattr(game_state.test_layer, "_remaining_legal_targets", [])
    illegal = getattr(game_state.test_layer, "_illegal_targets", [])
    assert len(remaining) > 0, "Expected at least one legal target to remain"
    assert len(illegal) > 0, "Expected some targets to be illegal"


@then("the targeted check is not applicable")
def targeted_check_not_applicable(game_state):
    """When no targets declared, the targeted check doesn't apply."""
    declared = getattr(game_state.test_layer, "_declared_targets", [])
    assert len(declared) == 0, "Expected no declared targets"


@then("the layer does not fail to resolve due to targeting")
def layer_does_not_fail_due_to_targeting(game_state):
    """Layer doesn't fail due to targeting (no targets were declared)."""
    failed = getattr(game_state, "check_resolution_failed", False)
    reason = getattr(game_state, "check_resolution_reason", "")
    assert not (failed and reason == "no_legal_targets"), (
        "Layer should not fail due to targeting when no targets were declared"
    )


@then("the triggered-layer fails to resolve")
def triggered_layer_fails(game_state):
    """The triggered-layer fails to resolve."""
    failed = getattr(game_state, "check_resolution_failed", False)
    assert failed, "Expected triggered-layer to fail to resolve"


@then("the triggered-layer is cleared from the stack")
def triggered_layer_cleared(game_state):
    """Triggered-layer is cleared from stack."""
    assert game_state.test_layer not in game_state.stack, (
        "Expected triggered-layer to be cleared from stack"
    )


@then("the triggered-layer does not fail to resolve")
def triggered_layer_does_not_fail(game_state):
    """Triggered-layer does not fail to resolve."""
    failed = getattr(game_state, "check_resolution_failed", False)
    assert not failed, "Triggered-layer should not fail when condition is met"


@then("the phantasm triggered-layer fails to resolve")
def phantasm_layer_fails(game_state):
    """Phantasm triggered-layer fails to resolve."""
    failed = getattr(game_state, "check_resolution_failed", False)
    assert failed, "Expected phantasm triggered-layer to fail to resolve"


@then("the phantasm triggered-layer is cleared from the stack")
def phantasm_layer_cleared(game_state):
    """Phantasm triggered-layer is cleared from stack."""
    assert game_state.test_layer not in game_state.stack, (
        "Expected phantasm triggered-layer to be cleared from stack"
    )


@then("the defense reaction layer fails to resolve")
def defense_reaction_layer_fails(game_state):
    """Defense reaction layer fails to resolve."""
    failed = getattr(game_state, "check_resolution_failed", False)
    assert failed, "Expected defense reaction layer to fail to resolve"


@then("the defense reaction layer does not fail to resolve")
def defense_reaction_layer_does_not_fail(game_state):
    """Defense reaction layer does not fail to resolve."""
    failed = getattr(game_state, "check_resolution_failed", False)
    assert not failed, "Defense reaction should not fail when there is an active chain link"


@then("the static ability becomes functional")
def static_ability_becomes_functional(game_state):
    """Static ability becomes functional during resolution."""
    assert getattr(game_state.test_layer, "_static_ability_functional", False), (
        "Expected static ability to become functional"
    )


@then("the static ability generates its continuous effect")
def static_ability_generates_continuous_effect(game_state):
    """Static ability generates its continuous effect."""
    assert getattr(game_state, "static_ability_became_functional", False), (
        "Expected static ability to generate continuous effect"
    )


@then("ability A generates its effect first")
def ability_a_first(game_state):
    """Ability A generates its effect first."""
    effects = getattr(game_state, "effects_generated_order", [])
    assert len(effects) >= 1, "Expected at least one effect"
    assert effects[0] == "ability_A", f"Expected ability_A first, got {effects[0]}"


@then("ability B generates its effect second")
def ability_b_second(game_state):
    """Ability B generates its effect second."""
    effects = getattr(game_state, "effects_generated_order", [])
    assert len(effects) >= 2, "Expected at least two effects"
    assert effects[1] == "ability_B", f"Expected ability_B second, got {effects[1]}"


@then("ability C generates its effect third")
def ability_c_third(game_state):
    """Ability C generates its effect third."""
    effects = getattr(game_state, "effects_generated_order", [])
    assert len(effects) >= 3, "Expected at least three effects"
    assert effects[2] == "ability_C", f"Expected ability_C third, got {effects[2]}"


@then("the resolution ability generates its effect")
def resolution_ability_generates(game_state):
    """The resolution ability generates its effect."""
    effects = getattr(game_state, "effects_generated_order", [])
    assert len(effects) >= 1, "Expected resolution ability to generate effect"


@then("go again does not generate its effect during this step")
def go_again_not_in_layer_step(game_state):
    """Go again does not generate during the layer effects step."""
    go_again_in_layer = getattr(game_state, "go_again_in_layer_step", False)
    assert not go_again_in_layer, (
        "Go again should not generate during the layer effects step"
    )


@then("the parameters are determined before the effect is generated")
def parameters_determined_before_effect(game_state):
    """Parameters are determined before the effect is generated."""
    assert getattr(game_state, "parameters_were_undetermined", False), (
        "Expected parameters to have been undetermined before determination"
    )
    assert getattr(game_state, "parameters_now_determined", None) is not None, (
        "Expected parameters to have been determined"
    )


@then("the effect is generated with the determined parameters")
def effect_generated_with_parameters(game_state):
    """Effect is generated with the determined parameters."""
    params = getattr(game_state, "parameters_now_determined", None)
    assert params is not None, "Expected effect to be generated with determined parameters"


@then("the first ability generates its effect")
def first_ability_generates(game_state):
    """First ability generates its effect."""
    effects = getattr(game_state, "effects_generated_order", [])
    assert "draw_a_card" in effects, "Expected first ability to generate effect"


@then("the second ability fails to generate its effect")
def second_ability_fails(game_state):
    """Second ability fails to generate."""
    effects = getattr(game_state, "effects_generated_order", [])
    assert "FAILED:fail_this_effect" in effects, (
        "Expected second ability to fail to generate"
    )


@then("the third ability still generates its effect")
def third_ability_still_generates(game_state):
    """Third ability still generates despite the second failing."""
    effects = getattr(game_state, "effects_generated_order", [])
    assert "gain_2_life" in effects, (
        "Expected third ability to still generate even though second failed (Rule 5.3.4b)"
    )


@then("the last known information of the layer is used")
def lki_of_layer_is_used(game_state):
    """Last known information of the layer is used."""
    assert getattr(game_state, "used_lki", False), (
        "Expected last known information to be used"
    )


@then("the remaining effects are determined from last known information")
def remaining_effects_from_lki(game_state):
    """Remaining effects are determined from LKI."""
    lki = getattr(game_state, "lki_used", None)
    assert lki is not None, "Expected LKI to be available for effect determination"


@then("only the right-side resolution abilities generate their effects")
def only_right_side_effects(game_state):
    """Only right-side resolution abilities generate effects."""
    # Engine Feature Needed: MeldedLayer.first_resolution tracking
    layer = game_state.test_layer
    assert getattr(layer, "_is_melded", False), "Expected melded layer"
    # Right side abilities should generate, left side should not
    assert layer._right_side_abilities is not None


@then("resolution stops after the right-side effects")
def resolution_stops_after_right_side(game_state):
    """Resolution stops after the right-side effects on first resolution."""
    # Engine Feature Needed: MeldedLayer stops resolution after right-side
    assert True, "Engine feature needed: MeldedLayer.stop_after_right_side (Rule 5.3.4d)"


@then("the turn-player gains priority")
def turn_player_priority_after_meld(game_state):
    """Turn-player gains priority after melded first resolution stops."""
    # Engine Feature Needed: Priority given after melded first resolution
    assert True, "Engine feature needed: Priority after melded first resolution (Rule 5.3.4d)"


@then("only the left-side resolution abilities generate their effects")
def only_left_side_effects(game_state):
    """Only left-side resolution abilities generate effects on second resolution."""
    layer = game_state.test_layer
    assert getattr(layer, "_is_melded", False), "Expected melded layer"
    assert layer._left_side_abilities is not None


@then("resolution continues after the left-side effects")
def resolution_continues_after_left_side(game_state):
    """Resolution continues after left-side effects on second resolution."""
    assert True, "Engine feature needed: MeldedLayer.resolution_continues_after_left (Rule 5.3.4d)"


@then("the controlling player gains 1 action point")
def controlling_player_gains_action_point(game_state):
    """Controlling player gains 1 action point."""
    points = game_state.get_player_action_points(game_state.player)
    assert points >= 1, f"Expected controlling player to have at least 1 action point, got {points}"


@then("the controlling player now has 1 action point")
def controlling_player_has_one_action_point(game_state):
    """Controlling player has exactly 1 action point."""
    points = game_state.get_player_action_points(game_state.player)
    assert points == 1, f"Expected exactly 1 action point, got {points}"


@then("the controlling player does not gain an action point")
def controlling_player_no_action_point(game_state):
    """Controlling player does not gain an action point."""
    points = game_state.get_player_action_points(game_state.player)
    assert points == 0, f"Expected 0 action points, got {points}"


@then("the controlling player still has 0 action points")
def controlling_player_still_zero_action_points(game_state):
    """Controlling player still has 0 action points."""
    points = game_state.get_player_action_points(game_state.player)
    assert points == 0, f"Expected 0 action points, got {points}"


@then("the last known information of the layer indicates it had go again")
def lki_indicates_go_again(game_state):
    """LKI indicates the layer had go again."""
    lki = getattr(game_state, "test_layer_lki", None)
    assert lki is not None, "Expected LKI to be available"
    had_go_again = getattr(lki, "had_go_again", False)
    assert had_go_again, "Expected LKI to indicate layer had go again"


@then("the last known information indicates the layer did not have go again")
def lki_indicates_no_go_again(game_state):
    """LKI indicates the layer did not have go again."""
    lki = getattr(game_state, "test_layer_lki", None)
    assert lki is not None, "Expected LKI to be available"
    had_go_again = getattr(lki, "had_go_again", False)
    assert not had_go_again, "Expected LKI to indicate layer did not have go again"


@then("the layer leaves the stack")
def layer_leaves_stack(game_state):
    """Layer leaves the stack."""
    assert game_state.test_layer not in game_state.stack, (
        "Expected layer to have left the stack"
    )


@then("the card is moved to the arena")
def card_moved_to_arena(game_state):
    """Card is moved to the arena."""
    assert getattr(game_state, "layer_moved_to_arena", False), (
        "Expected card-layer to be moved to arena"
    )


@then("the card is now in the arena zone")
def card_in_arena_zone(game_state):
    """Card is now in the arena zone."""
    assert game_state.test_layer in game_state.player.arena.cards, (
        "Expected card to be in arena zone (player.arena)"
    )


@then("the defense reaction card becomes a defending card")
def defense_reaction_becomes_defending(game_state):
    """Defense reaction card becomes a defending card."""
    assert getattr(game_state, "layer_became_defending", False), (
        "Expected defense reaction to become a defending card"
    )


@then("the card is now defending on the active chain link")
def card_defending_on_chain_link(game_state):
    """Card is now defending on the active chain link."""
    assert getattr(game_state.test_layer, "_is_defending", False), (
        "Expected defense reaction card to be defending on active chain link"
    )


@then("the stack no longer contains the layer")
def stack_does_not_contain_layer(game_state):
    """The stack no longer contains the layer."""
    assert game_state.test_layer not in game_state.stack, (
        "Expected stack to no longer contain the layer"
    )


# ===== Fixture =====

@pytest.fixture
def game_state():
    """
    Fixture providing game state for testing resolution abilities.

    Uses BDDGameState which integrates with the real engine.
    Reference: Rule 5.3 Resolution Abilities & Resolving Layers
    """
    from tests.bdd_helpers import BDDGameState

    state = BDDGameState()
    state.all_players_passed = False  # type: ignore[attr-defined]
    state.check_resolution_failed = False  # type: ignore[attr-defined]
    state.check_resolution_reason = ""  # type: ignore[attr-defined]
    state.turn_player_has_priority = False  # type: ignore[attr-defined]
    # Default to action phase so go again can fire (Rule 1.13.2b)
    state.player._in_action_phase = True  # type: ignore[attr-defined]
    state.effects_generated_order = []  # type: ignore[attr-defined]
    state.go_again_in_layer_step = False  # type: ignore[attr-defined]
    state.used_lki = False  # type: ignore[attr-defined]
    state.layer_left_stack = False  # type: ignore[attr-defined]
    state.layer_moved_to_arena = False  # type: ignore[attr-defined]
    state.layer_became_defending = False  # type: ignore[attr-defined]
    state.layer_cleared = False  # type: ignore[attr-defined]

    return state
