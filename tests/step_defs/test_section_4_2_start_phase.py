"""
Step definitions for Section 4.2: Start Phase
Reference: Flesh and Blood Comprehensive Rules Section 4.2

This module implements behavioral tests for the Start Phase of a player's turn.

- Rule 4.2.1: Players do not get priority during the Start Phase.
- Rule 4.2.2: The turn starts; "until start of turn" effects end; the "start of turn"
              event occurs; triggered effects fire and resolve; stack empties automatically.
- Rule 4.2.3: Start Phase ends and game proceeds to the Action Phase.

Engine Features Needed for Section 4.2:
- [ ] GameState.current_phase property tracking the current game phase (Rule 4.2.1)
- [ ] Phase.START_PHASE constant/enum value (Rule 4.2.1)
- [ ] Phase.ACTION_PHASE constant/enum value (Rule 4.2.3)
- [ ] GameState.has_priority(player) returns False during Start Phase (Rule 4.2.1)
- [ ] GameState.can_take_action(player) returns False during Start Phase (Rule 4.2.1)
- [ ] GameState.begin_start_phase() / TurnManager.begin_start_phase() (Rule 4.2.2)
- [ ] TurnManager.trigger_turn_start_event() fires the "start of turn" event (Rule 4.2.2)
- [ ] EffectDuration.UNTIL_START_OF_TURN duration type (Rule 4.2.2)
- [ ] EffectManager.expire_until_start_of_turn_effects() (Rule 4.2.2)
- [ ] TurnManager.collect_start_of_turn_triggers() adds triggered layers to stack (Rule 4.2.2)
- [ ] Stack.resolve_as_all_pass_priority() auto-resolves without player priority (Rule 4.2.2)
- [ ] TurnManager.end_start_phase() transitions to Action Phase (Rule 4.2.3)
- [ ] GameState.current_phase == Phase.ACTION_PHASE after start phase ends (Rule 4.2.3)

Current status: Tests written, Engine pending
"""

import pytest
from pytest_bdd import scenario, given, when, then, parsers


# ===== Scenarios =====


@scenario(
    "../features/section_4_2_start_phase.feature",
    "Players do not get priority during the Start Phase",
)
def test_no_priority_during_start_phase():
    """Rule 4.2.1: Players have no priority during the Start Phase."""
    pass


@scenario(
    "../features/section_4_2_start_phase.feature",
    "Players cannot take game actions during the Start Phase",
)
def test_no_actions_during_start_phase():
    """Rule 4.2.1: No player can take priority-based actions during Start Phase."""
    pass


@scenario(
    "../features/section_4_2_start_phase.feature",
    "Effects lasting until start of turn expire when the turn starts",
)
def test_until_start_of_turn_effects_expire():
    """Rule 4.2.2: Effects lasting 'until start of turn' end when the turn starts."""
    pass


@scenario(
    "../features/section_4_2_start_phase.feature",
    "Multiple until-start-of-turn effects all expire when the turn starts",
)
def test_multiple_until_start_of_turn_effects_expire():
    """Rule 4.2.2: All 'until start of turn' effects end simultaneously."""
    pass


@scenario(
    "../features/section_4_2_start_phase.feature",
    "The start of turn event occurs during the Start Phase",
)
def test_start_of_turn_event_occurs():
    """Rule 4.2.2: The 'start of turn' event fires during the Start Phase."""
    pass


@scenario(
    "../features/section_4_2_start_phase.feature",
    "Effects that trigger at start of turn fire during the Start Phase",
)
def test_start_of_turn_trigger_fires():
    """Rule 4.2.2: Triggered effects at start of turn are added to the stack."""
    pass


@scenario(
    "../features/section_4_2_start_phase.feature",
    "Multiple start-of-turn triggered effects all fire during Start Phase",
)
def test_multiple_start_of_turn_triggers_fire():
    """Rule 4.2.2: All start-of-turn triggered effects are added to the stack."""
    pass


@scenario(
    "../features/section_4_2_start_phase.feature",
    "Start-of-turn triggered layers resolve automatically without player priority",
)
def test_stack_resolves_without_player_priority():
    """Rule 4.2.2: Stack resolves as if all players pass priority (no player input needed)."""
    pass


@scenario(
    "../features/section_4_2_start_phase.feature",
    "Start Phase does not end until the stack is empty",
)
def test_start_phase_waits_for_empty_stack():
    """Rule 4.2.2: All layers must resolve before Start Phase ends."""
    pass


@scenario(
    "../features/section_4_2_start_phase.feature",
    "Start Phase ends and game proceeds to the Action Phase",
)
def test_start_phase_proceeds_to_action_phase():
    """Rule 4.2.3: After Start Phase completes, game transitions to Action Phase."""
    pass


@scenario(
    "../features/section_4_2_start_phase.feature",
    "Start Phase steps occur in the correct order",
)
def test_start_phase_correct_order():
    """Rule 4.2.2-4.2.3: until-start-of-turn expiry, event, triggers, then Action Phase."""
    pass


# ===== Given Steps =====


@given("a game is in progress")
def game_in_progress(game_state):
    """Set up a basic in-progress game with two players."""
    assert game_state is not None
    assert game_state.player is not None


@given("it is the beginning of the Start Phase")
def at_start_of_start_phase(game_state):
    """Record that we are about to enter the Start Phase."""
    game_state.test_phase_context = "start_phase"


@given("an effect is active that lasts until the \"start of turn\"")
def effect_until_start_of_turn_active(game_state):
    """Create an active effect with UNTIL_START_OF_TURN duration."""
    effect = game_state.create_until_start_of_turn_effect("test_effect_1")
    game_state.test_effects = [effect]


@given("multiple effects are active that last until the \"start of turn\"")
def multiple_effects_until_start_of_turn_active(game_state):
    """Create multiple active effects with UNTIL_START_OF_TURN duration."""
    effects = [
        game_state.create_until_start_of_turn_effect("test_effect_1"),
        game_state.create_until_start_of_turn_effect("test_effect_2"),
        game_state.create_until_start_of_turn_effect("test_effect_3"),
    ]
    game_state.test_effects = effects


@given("an effect exists that triggers at the start of turn")
def start_of_turn_trigger_exists(game_state):
    """Register an effect that triggers at the start of turn."""
    trigger = game_state.create_start_of_turn_trigger("sot_trigger_1")
    game_state.test_triggers = [trigger]


@given("multiple effects exist that trigger at the start of turn")
def multiple_start_of_turn_triggers_exist(game_state):
    """Register multiple effects that trigger at the start of turn."""
    triggers = [
        game_state.create_start_of_turn_trigger("sot_trigger_1"),
        game_state.create_start_of_turn_trigger("sot_trigger_2"),
    ]
    game_state.test_triggers = triggers


@given("a triggered effect fires at the start of turn")
def triggered_effect_fires_at_sot(game_state):
    """Set up a triggered effect that fires at the start of turn."""
    trigger = game_state.create_start_of_turn_trigger("sot_trigger_auto")
    game_state.test_triggers = [trigger]


@given("multiple triggered effects fire at the start of turn")
def multiple_triggered_effects_fire_at_sot(game_state):
    """Set up multiple triggered effects at the start of turn."""
    triggers = [
        game_state.create_start_of_turn_trigger("sot_trigger_1"),
        game_state.create_start_of_turn_trigger("sot_trigger_2"),
    ]
    game_state.test_triggers = triggers


@given("the Start Phase has completed its steps")
def start_phase_has_completed_steps(game_state):
    """Mark the Start Phase as having completed all its internal steps."""
    game_state.test_phase_context = "start_phase_complete"


# ===== When Steps =====


@when("the Start Phase is active")
def start_phase_is_active(game_state):
    """Simulate the Start Phase being active."""
    result = game_state.begin_start_phase()
    game_state.test_start_phase_result = result


@when("the Start Phase begins")
def start_phase_begins(game_state):
    """Begin the Start Phase."""
    result = game_state.begin_start_phase()
    game_state.test_start_phase_result = result


@when("the Start Phase begins and the turn starts")
def start_phase_begins_and_turn_starts(game_state):
    """Begin the Start Phase including the turn-start step."""
    result = game_state.begin_start_phase()
    game_state.test_start_phase_result = result


@when("the Start Phase processes the stack")
def start_phase_processes_stack(game_state):
    """Run the Start Phase stack processing step."""
    result = game_state.begin_start_phase()
    game_state.test_start_phase_result = result


@when("the Start Phase ends")
def start_phase_ends(game_state):
    """End the Start Phase and transition to the next phase."""
    result = game_state.end_start_phase()
    game_state.test_start_phase_result = result


@when("the Start Phase runs completely")
def start_phase_runs_completely(game_state):
    """Run the complete Start Phase from start to finish."""
    result = game_state.run_start_phase()
    game_state.test_start_phase_result = result


# ===== Then Steps =====


@then("no player has priority during the Start Phase")
def no_player_has_priority(game_state):
    """Rule 4.2.1: Verify no player holds priority during Start Phase."""
    result = game_state.test_start_phase_result
    # The start phase result should indicate no player has priority
    assert hasattr(result, 'any_player_has_priority'), (
        "Engine needs: StartPhaseResult.any_player_has_priority property"
    )
    assert not result.any_player_has_priority, (
        "Rule 4.2.1: No player should have priority during the Start Phase"
    )


@then("the turn player cannot play a card during the Start Phase")
def turn_player_cannot_play_card(game_state):
    """Rule 4.2.1: Turn player has no priority to play cards."""
    result = game_state.test_start_phase_result
    assert hasattr(result, 'turn_player_can_take_actions'), (
        "Engine needs: StartPhaseResult.turn_player_can_take_actions property"
    )
    assert not result.turn_player_can_take_actions, (
        "Rule 4.2.1: Turn player cannot play cards during the Start Phase"
    )


@then("the non-turn player cannot play a card during the Start Phase")
def non_turn_player_cannot_play_card(game_state):
    """Rule 4.2.1: Non-turn player has no priority to play cards."""
    result = game_state.test_start_phase_result
    assert hasattr(result, 'non_turn_player_can_take_actions'), (
        "Engine needs: StartPhaseResult.non_turn_player_can_take_actions property"
    )
    assert not result.non_turn_player_can_take_actions, (
        "Rule 4.2.1: Non-turn player cannot play cards during the Start Phase"
    )


@then("the \"until start of turn\" effect ends")
def until_start_of_turn_effect_ends(game_state):
    """Rule 4.2.2: An 'until start of turn' effect must expire when the turn starts."""
    result = game_state.test_start_phase_result
    assert hasattr(result, 'expired_effects'), (
        "Engine needs: StartPhaseResult.expired_effects list"
    )
    assert len(result.expired_effects) >= 1, (
        "Rule 4.2.2: At least one 'until start of turn' effect should have expired"
    )
    assert "test_effect_1" in result.expired_effects, (
        "Rule 4.2.2: The 'until start of turn' effect 'test_effect_1' should have expired"
    )


@then("all \"until start of turn\" effects end")
def all_until_start_of_turn_effects_end(game_state):
    """Rule 4.2.2: All 'until start of turn' effects expire when the turn starts."""
    result = game_state.test_start_phase_result
    assert hasattr(result, 'expired_effects'), (
        "Engine needs: StartPhaseResult.expired_effects list"
    )
    assert "test_effect_1" in result.expired_effects, (
        "Rule 4.2.2: 'test_effect_1' should have expired"
    )
    assert "test_effect_2" in result.expired_effects, (
        "Rule 4.2.2: 'test_effect_2' should have expired"
    )
    assert "test_effect_3" in result.expired_effects, (
        "Rule 4.2.2: 'test_effect_3' should have expired"
    )


@then("the \"start of turn\" event occurs")
def start_of_turn_event_occurs(game_state):
    """Rule 4.2.2: The 'start of turn' event must fire during the Start Phase."""
    result = game_state.test_start_phase_result
    assert hasattr(result, 'start_of_turn_event_occurred'), (
        "Engine needs: StartPhaseResult.start_of_turn_event_occurred flag"
    )
    assert result.start_of_turn_event_occurred, (
        "Rule 4.2.2: The 'start of turn' event must occur during the Start Phase"
    )


@then("the start-of-turn triggered effect is added to the stack")
def start_of_turn_trigger_added_to_stack(game_state):
    """Rule 4.2.2: A triggered effect at start of turn is placed on the stack."""
    result = game_state.test_start_phase_result
    assert hasattr(result, 'triggered_layers_added'), (
        "Engine needs: StartPhaseResult.triggered_layers_added list"
    )
    assert len(result.triggered_layers_added) >= 1, (
        "Rule 4.2.2: At least one triggered layer should have been added to the stack"
    )
    assert "sot_trigger_1" in result.triggered_layers_added, (
        "Rule 4.2.2: The start-of-turn trigger 'sot_trigger_1' should be on the stack"
    )


@then("all start-of-turn triggered effects are added to the stack")
def all_start_of_turn_triggers_added_to_stack(game_state):
    """Rule 4.2.2: All start-of-turn triggered effects are added to the stack."""
    result = game_state.test_start_phase_result
    assert hasattr(result, 'triggered_layers_added'), (
        "Engine needs: StartPhaseResult.triggered_layers_added list"
    )
    assert "sot_trigger_1" in result.triggered_layers_added, (
        "Rule 4.2.2: 'sot_trigger_1' should have been added to the stack"
    )
    assert "sot_trigger_2" in result.triggered_layers_added, (
        "Rule 4.2.2: 'sot_trigger_2' should have been added to the stack"
    )


@then("the stack resolves as if all players are passing priority in succession")
def stack_resolves_as_all_pass_priority(game_state):
    """Rule 4.2.2: Stack auto-resolves — no individual player priority granted."""
    result = game_state.test_start_phase_result
    assert hasattr(result, 'stack_resolved_automatically'), (
        "Engine needs: StartPhaseResult.stack_resolved_automatically flag"
    )
    assert result.stack_resolved_automatically, (
        "Rule 4.2.2: Stack must resolve as if all players pass priority (no player input)"
    )


@then("the stack is empty after the Start Phase processes it")
def stack_is_empty_after_processing(game_state):
    """Rule 4.2.2: Stack is empty after Start Phase processes triggered effects."""
    result = game_state.test_start_phase_result
    assert hasattr(result, 'stack_is_empty_after_processing'), (
        "Engine needs: StartPhaseResult.stack_is_empty_after_processing flag"
    )
    assert result.stack_is_empty_after_processing, (
        "Rule 4.2.2: The stack must be empty after the Start Phase processes it"
    )


@then("all layers resolve before the Start Phase ends")
def all_layers_resolve_before_start_phase_ends(game_state):
    """Rule 4.2.2: Every layer on the stack resolves before Start Phase ends."""
    result = game_state.test_start_phase_result
    assert hasattr(result, 'all_layers_resolved'), (
        "Engine needs: StartPhaseResult.all_layers_resolved flag"
    )
    assert result.all_layers_resolved, (
        "Rule 4.2.2: All layers on the stack must resolve before Start Phase can end"
    )


@then("the stack is empty when the Start Phase ends")
def stack_empty_when_start_phase_ends(game_state):
    """Rule 4.2.2: The stack is empty when the Start Phase finishes."""
    result = game_state.test_start_phase_result
    assert hasattr(result, 'stack_is_empty_at_end'), (
        "Engine needs: StartPhaseResult.stack_is_empty_at_end flag"
    )
    assert result.stack_is_empty_at_end, (
        "Rule 4.2.2: The stack must be empty when the Start Phase ends"
    )


@then("the game proceeds to the Action Phase")
def game_proceeds_to_action_phase(game_state):
    """Rule 4.2.3: After the Start Phase ends, game transitions to Action Phase."""
    result = game_state.test_start_phase_result
    assert hasattr(result, 'next_phase'), (
        "Engine needs: StartPhaseResult.next_phase property"
    )
    assert result.next_phase == "action_phase", (
        "Rule 4.2.3: The Start Phase must transition the game to the Action Phase"
    )


@then("the \"until start of turn\" effect ends before the start of turn event")
def until_sot_effect_ends_before_event(game_state):
    """Rule 4.2.2: 'until start of turn' effects expire before the start-of-turn event fires."""
    result = game_state.test_start_phase_result
    assert hasattr(result, 'step_order'), (
        "Engine needs: StartPhaseResult.step_order list tracking phase step sequence"
    )
    assert "expire_until_sot_effects" in result.step_order, (
        "Engine needs: 'expire_until_sot_effects' step in step_order"
    )
    assert "start_of_turn_event" in result.step_order, (
        "Engine needs: 'start_of_turn_event' step in step_order"
    )
    expire_idx = result.step_order.index("expire_until_sot_effects")
    event_idx = result.step_order.index("start_of_turn_event")
    assert expire_idx < event_idx, (
        "Rule 4.2.2: 'until start of turn' effects must expire before the start-of-turn event"
    )


@then("the start-of-turn triggered effect fires after the turn starts")
def sot_trigger_fires_after_turn_starts(game_state):
    """Rule 4.2.2: Start-of-turn triggers fire after the 'start of turn' event occurs."""
    result = game_state.test_start_phase_result
    assert hasattr(result, 'step_order'), (
        "Engine needs: StartPhaseResult.step_order list"
    )
    assert "start_of_turn_event" in result.step_order, (
        "Engine needs: 'start_of_turn_event' step in step_order"
    )
    assert "resolve_sot_triggers" in result.step_order, (
        "Engine needs: 'resolve_sot_triggers' step in step_order"
    )
    event_idx = result.step_order.index("start_of_turn_event")
    trigger_idx = result.step_order.index("resolve_sot_triggers")
    assert event_idx < trigger_idx, (
        "Rule 4.2.2: Start-of-turn triggers must fire after the start-of-turn event"
    )


@then("the game proceeds to the Action Phase after the stack is empty")
def game_proceeds_to_action_phase_after_stack_empty(game_state):
    """Rule 4.2.3: Transition to Action Phase happens only after the stack is empty."""
    result = game_state.test_start_phase_result
    assert hasattr(result, 'step_order'), (
        "Engine needs: StartPhaseResult.step_order list"
    )
    assert "resolve_sot_triggers" in result.step_order, (
        "Engine needs: 'resolve_sot_triggers' step in step_order"
    )
    assert "proceed_to_action_phase" in result.step_order, (
        "Engine needs: 'proceed_to_action_phase' step in step_order"
    )
    trigger_idx = result.step_order.index("resolve_sot_triggers")
    proceed_idx = result.step_order.index("proceed_to_action_phase")
    assert trigger_idx < proceed_idx, (
        "Rule 4.2.3: Game must transition to Action Phase only after all stack layers resolve"
    )


# ===== Fixture =====


@pytest.fixture
def game_state():
    """
    Fixture providing game state for Start Phase testing.

    Uses BDDGameState which integrates with the real engine.
    Reference: Rules 4.2.1 - 4.2.3
    """
    from tests.bdd_helpers import BDDGameState

    state = BDDGameState()
    state.test_effects = []
    state.test_triggers = []
    state.test_phase_context = None
    state.test_start_phase_result = None

    return state
