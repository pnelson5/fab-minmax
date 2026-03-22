"""
Step definitions for Section 4.3: Action Phase
Reference: Flesh and Blood Comprehensive Rules Section 4.3

This module implements behavioral tests for the Action Phase of a player's turn.

- Rule 4.3.1: The action phase starts; the "beginning of the action phase" event occurs
              and effects that trigger at the beginning of the action phase are triggered.
- Rule 4.3.2: The turn-player has 1 action point.
- Rule 4.3.2a: Effects that trigger when a player gains an action point do not trigger
               when the turn-player gains an action point from the action phase start.
- Rule 4.3.2b: Replacement effects that modify gaining an action point do not apply
               when the turn-player gains an action point from the action phase start.
- Rule 4.3.3: The turn-player gains priority.
- Rule 4.3.4: The action phase ends when the stack is empty, the combat chain is closed,
              and both players pass priority in succession; game proceeds to End Phase.

Engine Features Needed for Section 4.3:
- [ ] GameState.begin_action_phase() / TurnManager.begin_action_phase() (Rule 4.3.1)
- [ ] ActionPhaseResult.beginning_of_action_phase_event_occurred flag (Rule 4.3.1)
- [ ] TurnManager.trigger_beginning_of_action_phase() fires triggered effects (Rule 4.3.1)
- [ ] ActionPhaseResult.triggered_layers_added list (Rule 4.3.1)
- [ ] TurnManager.grant_action_phase_action_point() grants 1 AP to turn-player (Rule 4.3.2)
- [ ] ActionPhaseResult.turn_player_action_points count (Rule 4.3.2)
- [ ] ActionPhaseResult.non_turn_player_action_points_from_grant count (Rule 4.3.2)
- [ ] TurnManager suppresses gain-action-point triggers for AP phase grant (Rule 4.3.2a)
- [ ] ActionPhaseResult.gain_ap_trigger_fired flag (Rule 4.3.2a)
- [ ] TurnManager suppresses replacement effects for AP phase grant (Rule 4.3.2b)
- [ ] ActionPhaseResult.replacement_effect_applied flag (Rule 4.3.2b)
- [ ] TurnManager.grant_priority_to_turn_player() (Rule 4.3.3)
- [ ] ActionPhaseResult.turn_player_has_priority flag (Rule 4.3.3)
- [ ] ActionPhaseResult.players_can_get_priority flag (Rule 4.3.3)
- [ ] TurnManager.check_action_phase_end_conditions() (Rule 4.3.4)
- [ ] ActionPhaseResult.action_phase_ended flag (Rule 4.3.4)
- [ ] ActionPhaseResult.next_phase property (Rule 4.3.4)
- [ ] GameState.stack.is_empty flag (Rule 4.3.4)
- [ ] GameState.combat_chain.is_closed flag (Rule 4.3.4)
- [ ] ActionPhaseResult.step_order list for ordering checks (Rule 4.3)

Current status: Tests written, Engine pending
"""

import pytest
from pytest_bdd import scenario, given, when, then, parsers


# ===== Scenarios =====


@scenario(
    "../features/section_4_3_action_phase.feature",
    "The beginning of action phase event occurs when action phase starts",
)
def test_beginning_of_action_phase_event():
    """Rule 4.3.1: The 'beginning of the action phase' event fires when action phase starts."""
    pass


@scenario(
    "../features/section_4_3_action_phase.feature",
    "Effects that trigger at the beginning of the action phase are triggered",
)
def test_beginning_of_action_phase_trigger_fires():
    """Rule 4.3.1: Triggered effects at beginning of action phase are added to stack."""
    pass


@scenario(
    "../features/section_4_3_action_phase.feature",
    "Multiple effects that trigger at beginning of action phase all fire",
)
def test_multiple_beginning_of_action_phase_triggers_fire():
    """Rule 4.3.1: All beginning-of-action-phase triggered effects fire."""
    pass


@scenario(
    "../features/section_4_3_action_phase.feature",
    "Turn-player has 1 action point at the start of the action phase",
)
def test_turn_player_gets_one_action_point():
    """Rule 4.3.2: Turn-player starts the action phase with exactly 1 action point."""
    pass


@scenario(
    "../features/section_4_3_action_phase.feature",
    "Non-turn player does not gain action points at the start of the action phase",
)
def test_non_turn_player_gets_no_action_points():
    """Rule 4.3.2: Non-turn player receives no action points from the action phase grant."""
    pass


@scenario(
    "../features/section_4_3_action_phase.feature",
    "Gain-action-point triggers do not fire when turn-player gains action point from action phase",
)
def test_gain_ap_triggers_suppressed_for_action_phase_grant():
    """Rule 4.3.2a: Triggered effects for gaining action points don't fire for AP phase grant."""
    pass


@scenario(
    "../features/section_4_3_action_phase.feature",
    "Replacement effects for gaining action points do not apply to action phase grant",
)
def test_replacement_effects_suppressed_for_action_phase_grant():
    """Rule 4.3.2b: Replacement effects for gaining AP don't apply to action phase grant."""
    pass


@scenario(
    "../features/section_4_3_action_phase.feature",
    "Turn-player gains priority at the start of the action phase",
)
def test_turn_player_gains_priority():
    """Rule 4.3.3: Turn-player holds priority at the start of the action phase."""
    pass


@scenario(
    "../features/section_4_3_action_phase.feature",
    "The action phase is the only phase during which players get priority",
)
def test_action_phase_is_priority_phase():
    """Rule 4.3.3: Players can get priority during the Action Phase (unlike other phases)."""
    pass


@scenario(
    "../features/section_4_3_action_phase.feature",
    "Action phase ends when stack is empty, combat chain is closed, and both players pass priority",
)
def test_action_phase_ends_on_conditions_met():
    """Rule 4.3.4: Action phase ends when all three conditions are met."""
    pass


@scenario(
    "../features/section_4_3_action_phase.feature",
    "Action phase proceeds to the End Phase when it ends",
)
def test_action_phase_proceeds_to_end_phase():
    """Rule 4.3.4: When action phase ends, game transitions to the End Phase."""
    pass


@scenario(
    "../features/section_4_3_action_phase.feature",
    "Action phase does not end if the stack is not empty",
)
def test_action_phase_does_not_end_with_nonempty_stack():
    """Rule 4.3.4: Action phase cannot end while the stack has layers on it."""
    pass


@scenario(
    "../features/section_4_3_action_phase.feature",
    "Action phase does not end if the combat chain is not closed",
)
def test_action_phase_does_not_end_with_open_combat_chain():
    """Rule 4.3.4: Action phase cannot end while the combat chain is open."""
    pass


@scenario(
    "../features/section_4_3_action_phase.feature",
    "Action phase steps occur in the correct order",
)
def test_action_phase_correct_step_order():
    """Rule 4.3.1-4.3.3: Beginning event -> action point grant -> priority grant."""
    pass


# ===== Given Steps =====


@given("a game is in progress")
def game_in_progress(game_state):
    """Set up a basic in-progress game with two players."""
    assert game_state is not None
    assert game_state.player is not None


@given("an effect exists that triggers at the beginning of the action phase")
def beginning_of_ap_trigger_exists(game_state):
    """Register an effect that triggers at the beginning of the action phase."""
    trigger = game_state.create_beginning_of_action_phase_trigger("boap_trigger_1")
    game_state.test_triggers = [trigger]


@given("multiple effects exist that trigger at the beginning of the action phase")
def multiple_beginning_of_ap_triggers_exist(game_state):
    """Register multiple effects that trigger at the beginning of the action phase."""
    triggers = [
        game_state.create_beginning_of_action_phase_trigger("boap_trigger_1"),
        game_state.create_beginning_of_action_phase_trigger("boap_trigger_2"),
    ]
    game_state.test_triggers = triggers


@given("an effect exists that triggers when a player gains an action point")
def gain_ap_trigger_exists(game_state):
    """Register a triggered effect that fires on gain-action-point events."""
    trigger = game_state.create_gain_action_point_trigger("gain_ap_trigger")
    game_state.test_gain_ap_trigger = trigger


@given("a replacement effect exists that modifies events when a player gains an action point")
def gain_ap_replacement_effect_exists(game_state):
    """Register a replacement effect that modifies gain-action-point events."""
    replacement = game_state.create_gain_action_point_replacement_effect("gain_ap_replacement")
    game_state.test_gain_ap_replacement = replacement


@given("the stack is empty")
def stack_is_empty(game_state):
    """Ensure the stack has no layers on it."""
    game_state.test_stack_empty = True


@given("the stack has layers on it")
def stack_has_layers(game_state):
    """Add a layer to the stack so it is non-empty."""
    game_state.test_stack_empty = False
    game_state.test_stack_has_layers = True


@given("the combat chain is closed")
def combat_chain_is_closed(game_state):
    """Mark the combat chain as closed."""
    game_state.test_combat_chain_closed = True


@given("the combat chain is open")
def combat_chain_is_open(game_state):
    """Mark the combat chain as open (attack in progress)."""
    game_state.test_combat_chain_closed = False


@given("the action phase has ended")
def action_phase_has_ended(game_state):
    """Mark that the action phase has completed."""
    game_state.test_action_phase_ended = True


# ===== When Steps =====


@when("the Action Phase begins")
def action_phase_begins(game_state):
    """Begin the Action Phase."""
    result = game_state.begin_action_phase()
    game_state.test_action_phase_result = result


@when("the Action Phase is active")
def action_phase_is_active(game_state):
    """Simulate the Action Phase being active."""
    result = game_state.begin_action_phase()
    game_state.test_action_phase_result = result


@when("the Action Phase begins and the turn-player receives 1 action point")
def action_phase_begins_ap_granted(game_state):
    """Begin the Action Phase, including the action point grant step."""
    result = game_state.begin_action_phase()
    game_state.test_action_phase_result = result


@when("both players pass priority in succession")
def both_players_pass_priority(game_state):
    """Simulate both players passing priority."""
    result = game_state.check_action_phase_end_conditions(
        stack_empty=game_state.test_stack_empty,
        combat_chain_closed=game_state.test_combat_chain_closed,
    )
    game_state.test_action_phase_result = result


@when("both players attempt to pass priority")
def both_players_attempt_to_pass_priority(game_state):
    """Attempt to end the action phase by having both players pass."""
    result = game_state.check_action_phase_end_conditions(
        stack_empty=game_state.test_stack_empty,
        combat_chain_closed=game_state.test_combat_chain_closed,
    )
    game_state.test_action_phase_result = result


@when("the action phase completes")
def action_phase_completes(game_state):
    """Complete the action phase and transition to the next phase."""
    result = game_state.end_action_phase()
    game_state.test_action_phase_result = result


@when("the Action Phase runs through its initial steps")
def action_phase_runs_initial_steps(game_state):
    """Run the action phase through its initial ordering steps."""
    result = game_state.begin_action_phase()
    game_state.test_action_phase_result = result


# ===== Then Steps =====


@then("the \"beginning of the action phase\" event occurs")
def beginning_of_action_phase_event_occurs(game_state):
    """Rule 4.3.1: The 'beginning of the action phase' event must fire."""
    result = game_state.test_action_phase_result
    assert hasattr(result, 'beginning_of_action_phase_event_occurred'), (
        "Engine needs: ActionPhaseResult.beginning_of_action_phase_event_occurred flag"
    )
    assert result.beginning_of_action_phase_event_occurred, (
        "Rule 4.3.1: The 'beginning of the action phase' event must occur"
    )


@then("the beginning-of-action-phase triggered effect fires")
def beginning_of_ap_triggered_effect_fires(game_state):
    """Rule 4.3.1: A triggered effect at the beginning of action phase fires."""
    result = game_state.test_action_phase_result
    assert hasattr(result, 'triggered_layers_added'), (
        "Engine needs: ActionPhaseResult.triggered_layers_added list"
    )
    assert len(result.triggered_layers_added) >= 1, (
        "Rule 4.3.1: At least one triggered layer should be added to the stack"
    )
    assert "boap_trigger_1" in result.triggered_layers_added, (
        "Rule 4.3.1: 'boap_trigger_1' should have been added to the stack"
    )


@then("all beginning-of-action-phase triggered effects fire")
def all_beginning_of_ap_triggered_effects_fire(game_state):
    """Rule 4.3.1: All beginning-of-action-phase triggered effects fire."""
    result = game_state.test_action_phase_result
    assert hasattr(result, 'triggered_layers_added'), (
        "Engine needs: ActionPhaseResult.triggered_layers_added list"
    )
    assert "boap_trigger_1" in result.triggered_layers_added, (
        "Rule 4.3.1: 'boap_trigger_1' should have fired"
    )
    assert "boap_trigger_2" in result.triggered_layers_added, (
        "Rule 4.3.1: 'boap_trigger_2' should have fired"
    )


@then("the turn-player has 1 action point")
def turn_player_has_one_action_point(game_state):
    """Rule 4.3.2: Turn-player has exactly 1 action point at action phase start."""
    result = game_state.test_action_phase_result
    assert hasattr(result, 'turn_player_action_points'), (
        "Engine needs: ActionPhaseResult.turn_player_action_points count"
    )
    assert result.turn_player_action_points == 1, (
        f"Rule 4.3.2: Turn-player should have 1 action point, got {result.turn_player_action_points}"
    )


@then("the non-turn player has 0 action points from the action phase grant")
def non_turn_player_has_no_action_points(game_state):
    """Rule 4.3.2: Non-turn player receives no action points from the action phase grant."""
    result = game_state.test_action_phase_result
    assert hasattr(result, 'non_turn_player_action_points_from_grant'), (
        "Engine needs: ActionPhaseResult.non_turn_player_action_points_from_grant count"
    )
    assert result.non_turn_player_action_points_from_grant == 0, (
        "Rule 4.3.2: Non-turn player should not receive action points from action phase grant"
    )


@then("the gain-action-point trigger does not fire for the action phase grant")
def gain_ap_trigger_does_not_fire(game_state):
    """Rule 4.3.2a: Gain-AP triggers are suppressed for the action phase AP grant."""
    result = game_state.test_action_phase_result
    assert hasattr(result, 'gain_ap_trigger_fired'), (
        "Engine needs: ActionPhaseResult.gain_ap_trigger_fired flag"
    )
    assert not result.gain_ap_trigger_fired, (
        "Rule 4.3.2a: Gain-action-point triggers must NOT fire for the action phase AP grant"
    )


@then("the replacement effect does not modify the action phase action point grant")
def replacement_effect_does_not_modify_ap_grant(game_state):
    """Rule 4.3.2b: Replacement effects for gaining AP don't apply to action phase grant."""
    result = game_state.test_action_phase_result
    assert hasattr(result, 'replacement_effect_applied'), (
        "Engine needs: ActionPhaseResult.replacement_effect_applied flag"
    )
    assert not result.replacement_effect_applied, (
        "Rule 4.3.2b: Replacement effects must NOT modify the action phase AP grant"
    )


@then("the turn-player has priority")
def turn_player_has_priority(game_state):
    """Rule 4.3.3: Turn-player holds priority at the start of the action phase."""
    result = game_state.test_action_phase_result
    assert hasattr(result, 'turn_player_has_priority'), (
        "Engine needs: ActionPhaseResult.turn_player_has_priority flag"
    )
    assert result.turn_player_has_priority, (
        "Rule 4.3.3: Turn-player must have priority at the start of the action phase"
    )


@then("players can get priority during the Action Phase")
def players_can_get_priority_during_action_phase(game_state):
    """Rule 4.3.3: The Action Phase is the phase where players get priority."""
    result = game_state.test_action_phase_result
    assert hasattr(result, 'players_can_get_priority'), (
        "Engine needs: ActionPhaseResult.players_can_get_priority flag"
    )
    assert result.players_can_get_priority, (
        "Rule 4.3.3: Players must be able to get priority during the Action Phase"
    )


@then("the action phase ends")
def action_phase_ends(game_state):
    """Rule 4.3.4: Action phase ends when all conditions are met."""
    result = game_state.test_action_phase_result
    assert hasattr(result, 'action_phase_ended'), (
        "Engine needs: ActionPhaseResult.action_phase_ended flag"
    )
    assert result.action_phase_ended, (
        "Rule 4.3.4: Action phase must end when stack empty, chain closed, both players pass"
    )


@then("the game proceeds to the End Phase")
def game_proceeds_to_end_phase(game_state):
    """Rule 4.3.4: After action phase ends, game transitions to End Phase."""
    result = game_state.test_action_phase_result
    assert hasattr(result, 'next_phase'), (
        "Engine needs: ActionPhaseResult.next_phase property"
    )
    assert result.next_phase == "end_phase", (
        "Rule 4.3.4: Action phase must transition the game to the End Phase"
    )


@then("the action phase does not end while the stack is not empty")
def action_phase_does_not_end_with_nonempty_stack(game_state):
    """Rule 4.3.4: Action phase cannot end while stack has layers."""
    result = game_state.test_action_phase_result
    assert hasattr(result, 'action_phase_ended'), (
        "Engine needs: ActionPhaseResult.action_phase_ended flag"
    )
    assert not result.action_phase_ended, (
        "Rule 4.3.4: Action phase must NOT end while the stack has layers on it"
    )


@then("the action phase does not end while the combat chain is open")
def action_phase_does_not_end_with_open_chain(game_state):
    """Rule 4.3.4: Action phase cannot end while combat chain is open."""
    result = game_state.test_action_phase_result
    assert hasattr(result, 'action_phase_ended'), (
        "Engine needs: ActionPhaseResult.action_phase_ended flag"
    )
    assert not result.action_phase_ended, (
        "Rule 4.3.4: Action phase must NOT end while the combat chain is open"
    )


@then("the beginning-of-action-phase event occurs before the action point is granted")
def boap_event_before_ap_grant(game_state):
    """Rule 4.3.1-4.3.2: Beginning-of-action-phase event fires before AP is granted."""
    result = game_state.test_action_phase_result
    assert hasattr(result, 'step_order'), (
        "Engine needs: ActionPhaseResult.step_order list tracking phase step sequence"
    )
    assert "beginning_of_action_phase_event" in result.step_order, (
        "Engine needs: 'beginning_of_action_phase_event' step in step_order"
    )
    assert "grant_action_point" in result.step_order, (
        "Engine needs: 'grant_action_point' step in step_order"
    )
    event_idx = result.step_order.index("beginning_of_action_phase_event")
    ap_idx = result.step_order.index("grant_action_point")
    assert event_idx < ap_idx, (
        "Rule 4.3.1-4.3.2: Beginning-of-action-phase event must occur before AP is granted"
    )


@then("the action point is granted before the turn-player gains priority")
def ap_grant_before_priority(game_state):
    """Rule 4.3.2-4.3.3: AP is granted before turn-player gains priority."""
    result = game_state.test_action_phase_result
    assert hasattr(result, 'step_order'), (
        "Engine needs: ActionPhaseResult.step_order list"
    )
    assert "grant_action_point" in result.step_order, (
        "Engine needs: 'grant_action_point' step in step_order"
    )
    assert "grant_priority" in result.step_order, (
        "Engine needs: 'grant_priority' step in step_order"
    )
    ap_idx = result.step_order.index("grant_action_point")
    priority_idx = result.step_order.index("grant_priority")
    assert ap_idx < priority_idx, (
        "Rule 4.3.2-4.3.3: Action point must be granted before the turn-player gains priority"
    )


# ===== Fixture =====


@pytest.fixture
def game_state():
    """
    Fixture providing game state for Action Phase testing.

    Uses BDDGameState which integrates with the real engine.
    Reference: Rules 4.3.1 - 4.3.4
    """
    from tests.bdd_helpers import BDDGameState

    state = BDDGameState()
    state.test_triggers = []
    state.test_gain_ap_trigger = None
    state.test_gain_ap_replacement = None
    state.test_action_phase_result = None
    state.test_stack_empty = True
    state.test_combat_chain_closed = True
    state.test_stack_has_layers = False
    state.test_action_phase_ended = False

    return state
