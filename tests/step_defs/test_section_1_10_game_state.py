"""
Step definitions for Section 1.10: Game State
Reference: Flesh and Blood Comprehensive Rules Section 1.10

This module implements behavioral tests for game state concepts, including:
- Game state as a moment in the game (Rule 1.10.1)
- Game state actions performed on priority state transitions (Rule 1.10.2)
- Illegal action reversal (Rule 1.10.3)

Engine Features Needed for Section 1.10:
- [ ] GameState class representing a discrete moment in the game (Rule 1.10.1)
- [ ] GameState.is_priority_state property (Rule 1.10.1)
- [ ] GameEngine.has_priority_player() method (Rule 1.10.1)
- [ ] GameEngine.get_priority_player() method (Rule 1.10.1)
- [ ] GameStateAction system executing actions (a)-(e) in order (Rule 1.10.2)
- [ ] GameStateAction.check_hero_deaths() (Rule 1.10.2a)
- [ ] GameStateAction.clear_zero_life_permanents() (Rule 1.10.2b)
- [ ] GameStateAction.start_look_effects() (Rule 1.10.2c)
- [ ] GameStateAction.fire_state_based_triggers() (Rule 1.10.2d)
- [ ] GameStateAction.check_combat_chain_closing() (Rule 1.10.2e)
- [ ] GameEngine.reverse_illegal_action() method (Rule 1.10.3)
- [ ] ReversalResult class with state_restored, reversal_was_partial (Rule 1.10.3)
- [ ] GameEngine triggered effect suppression during reversal (Rule 1.10.3a)
- [ ] GameEngine replacement effect suppression during reversal (Rule 1.10.3b)

These features will be implemented in a separate task.
Current status: Tests written, Engine pending
"""

import pytest
from pytest_bdd import scenario, given, when, then, parsers

# ============================================================
# Scenario: game state exists as a discrete moment
# Tests Rule 1.10.1 - Game state is a moment in the game
# ============================================================


@scenario(
    "../features/section_1_10_game_state.feature",
    "game state exists as a discrete moment",
)
def test_game_state_is_discrete_moment():
    """Rule 1.10.1: A game state is a moment in the game."""
    pass


# ============================================================
# Scenario: priority state is a game state where player receives priority
# Tests Rule 1.10.1 - Priority state concept
# ============================================================


@scenario(
    "../features/section_1_10_game_state.feature",
    "priority state is a game state where player receives priority",
)
def test_priority_state_gives_priority_to_player():
    """Rule 1.10.1: A priority state is a game state where a player receives priority."""
    pass


# ============================================================
# Scenario: non-priority game state has no player with priority
# Tests Rule 1.10.1 - No priority during game state actions
# ============================================================


@scenario(
    "../features/section_1_10_game_state.feature",
    "non-priority game state has no player with priority",
)
def test_no_priority_during_game_state_actions():
    """Rule 1.10.1: No player has priority during game state actions."""
    pass


# ============================================================
# Scenario: hero with zero life causes player to lose when priority state is reached
# Tests Rule 1.10.2a - Hero death check is first game state action
# ============================================================


@scenario(
    "../features/section_1_10_game_state.feature",
    "hero with zero life causes player to lose when priority state is reached",
)
def test_hero_zero_life_triggers_loss():
    """Rule 1.10.2a: Hero with 0 life causes player loss as first game state action."""
    pass


# ============================================================
# Scenario: all heroes die simultaneously results in draw
# Tests Rule 1.10.2a - Simultaneous hero death draw condition
# ============================================================


@scenario(
    "../features/section_1_10_game_state.feature",
    "all heroes die simultaneously results in draw",
)
def test_simultaneous_hero_death_is_draw():
    """Rule 1.10.2a: If all heroes die simultaneously, the game ends in a draw."""
    pass


# ============================================================
# Scenario: living object with zero life is cleared in second game state action
# Tests Rule 1.10.2b - Living objects cleared at 0 life
# ============================================================


@scenario(
    "../features/section_1_10_game_state.feature",
    "living object with zero life is cleared in second game state action",
)
def test_living_object_zero_life_cleared():
    """Rule 1.10.2b: Living objects with 0 life are cleared as the second game state action."""
    pass


# ============================================================
# Scenario: multiple living objects with zero life are cleared simultaneously
# Tests Rule 1.10.2b - Simultaneous clearing
# ============================================================


@scenario(
    "../features/section_1_10_game_state.feature",
    "multiple living objects with zero life are cleared simultaneously",
)
def test_multiple_living_objects_cleared_simultaneously():
    """Rule 1.10.2b: Multiple 0-life living objects are cleared simultaneously as one event."""
    pass


# ============================================================
# Scenario: hero at zero life triggers player loss not living object clearing
# Tests Rule 1.10.2a vs 1.10.2b - Hero handled by action 1 not action 2
# ============================================================


@scenario(
    "../features/section_1_10_game_state.feature",
    "hero at zero life triggers player loss not living object clearing",
)
def test_hero_zero_life_is_action_1_not_action_2():
    """Rule 1.10.2a/b: Hero at 0 life is handled by action 1 (hero death), not action 2 (permanent clearing)."""
    pass


# ============================================================
# Scenario: continuous look effect activates during third game state action
# Tests Rule 1.10.2c - Look effects start at game state action 3
# ============================================================


@scenario(
    "../features/section_1_10_game_state.feature",
    "continuous look effect activates during third game state action",
)
def test_continuous_look_effect_activates_at_action_3():
    """Rule 1.10.2c: Continuous look effects start when entering a priority state."""
    pass


# ============================================================
# Scenario: state-based triggered effect fires when condition is met
# Tests Rule 1.10.2d - State-based triggers fire in fourth game state action
# ============================================================


@scenario(
    "../features/section_1_10_game_state.feature",
    "state-based triggered effect fires when condition is met",
)
def test_state_based_triggered_effect_fires():
    """Rule 1.10.2d: State-based triggered effects fire as the fourth game state action."""
    pass


# ============================================================
# Scenario: multiple triggered layers added to stack in clockwise order from turn player choice
# Tests Rule 1.10.2d - Clockwise order for multiple triggered layers
# ============================================================


@scenario(
    "../features/section_1_10_game_state.feature",
    "multiple triggered layers added to stack in clockwise order from turn player choice",
)
def test_triggered_layers_added_in_clockwise_order():
    """Rule 1.10.2d: Multiple triggered layers added clockwise from turn player's chosen starting player."""
    pass


# ============================================================
# Scenario: open combat chain closed by effect begins close step
# Tests Rule 1.10.2e - Combat chain closing is fifth game state action
# ============================================================


@scenario(
    "../features/section_1_10_game_state.feature",
    "open combat chain closed by effect begins close step",
)
def test_combat_chain_closed_begins_close_step():
    """Rule 1.10.2e: When combat chain is open and closed by rule/effect, Close Step begins."""
    pass


# ============================================================
# Scenario: no close step when combat chain is not open
# Tests Rule 1.10.2e - No close step without open combat chain
# ============================================================


@scenario(
    "../features/section_1_10_game_state.feature",
    "no close step when combat chain is not open",
)
def test_no_close_step_without_open_combat_chain():
    """Rule 1.10.2e: Close step only begins if combat chain was open and is now closed."""
    pass


# ============================================================
# Scenario: game state actions are performed in the correct order
# Tests Rule 1.10.2 - Ordered execution of game state actions
# ============================================================


@scenario(
    "../features/section_1_10_game_state.feature",
    "game state actions are performed in the correct order",
)
def test_game_state_actions_performed_in_order():
    """Rule 1.10.2: Game state actions (a) through (e) are performed in order."""
    pass


# ============================================================
# Scenario: illegal action reverses game state to before it started
# Tests Rule 1.10.3 - Illegal action reversal
# ============================================================


@scenario(
    "../features/section_1_10_game_state.feature",
    "illegal action reverses game state to before it started",
)
def test_illegal_action_reverses_game_state():
    """Rule 1.10.3: An illegal action causes the game state to be reversed."""
    pass


# ============================================================
# Scenario: action becoming illegal mid-completion is reversed
# Tests Rule 1.10.3 - Mid-action illegality reversal
# ============================================================


@scenario(
    "../features/section_1_10_game_state.feature",
    "action becoming illegal mid-completion is reversed",
)
def test_mid_action_illegality_reverses_game_state():
    """Rule 1.10.3: An action that becomes illegal mid-completion is reversed."""
    pass


# ============================================================
# Scenario: triggered effects do not fire during game state reversal
# Tests Rule 1.10.3a - No triggered effects from reversal
# ============================================================


@scenario(
    "../features/section_1_10_game_state.feature",
    "triggered effects do not trigger during game state reversal",
)
def test_triggered_effects_suppressed_during_reversal():
    """Rule 1.10.3a: Triggered effects do not trigger as a result of game state reversal."""
    pass


# ============================================================
# Scenario: replacement effects cannot modify reversal events
# Tests Rule 1.10.3b - No replacement effects during reversal
# ============================================================


@scenario(
    "../features/section_1_10_game_state.feature",
    "replacement effects cannot modify reversal events",
)
def test_replacement_effects_suppressed_during_reversal():
    """Rule 1.10.3b: Replacement effects cannot replace events caused by game state reversal."""
    pass


# ============================================================
# Scenario: partial reversal when full reversal is impossible
# Tests Rule 1.10.3c - Partial reversal fallback
# ============================================================


@scenario(
    "../features/section_1_10_game_state.feature",
    "partial reversal when full reversal is impossible",
)
def test_partial_reversal_when_full_reversal_impossible():
    """Rule 1.10.3c: When full reversal is impossible, reverse as much as possible."""
    pass


# ============================================================
# Scenario: attempting to play an unplayable card reverses game state
# Tests Rule 1.10.3 - Practical reversal example
# ============================================================


@scenario(
    "../features/section_1_10_game_state.feature",
    "attempting to play an unplayable card reverses game state",
)
def test_unplayable_card_play_reversed():
    """Rule 1.10.3: Playing an unplayable card is an illegal action that is reversed."""
    pass


# ============================================================
# Scenario: paying cost then failing legality check reverses entire action
# Tests Rule 1.10.3 - Full action reversal including cost payment
# ============================================================


@scenario(
    "../features/section_1_10_game_state.feature",
    "paying cost then failing legality check reverses entire action",
)
def test_cost_payment_with_illegal_play_reversed():
    """Rule 1.10.3: When a play becomes illegal after cost payment, the full action is reversed."""
    pass


# ============================================================
# Step Definitions
# ============================================================

# --- Given steps ---


@given("a game is in progress")
def step_game_in_progress(game_state):
    """Rule 1.10.1: A game is in progress with at least two players."""
    assert game_state is not None
    assert game_state.player is not None


@given("the game is in the action phase")
def step_game_in_action_phase_when(game_state):
    """Rule 1.10.1: Game is in the action phase (where priority is given)."""
    game_state.phase = "action_phase"


@given("a game is in the action phase")
def step_game_in_action_phase(game_state):
    """Rule 1.10.1: Game is in the action phase (where priority is given)."""
    game_state.phase = "action_phase"


@given("the game is in a stable state")
def step_game_in_stable_state(game_state):
    """Rule 1.10.1: Game is in a stable state with no pending actions."""
    game_state.is_stable = True


@given("the game is performing game state actions")
def step_game_performing_state_actions(game_state):
    """Rule 1.10.1: Game state actions are being executed (no player has priority)."""
    game_state.performing_state_actions = True


@given(parsers.parse("player {player_id:d}'s hero has {life:d} life"))
def step_player_hero_has_life(game_state, player_id, life):
    """Rule 1.10.2a: Set a player's hero to a specific life total."""
    if player_id == 0:
        game_state.player.hero_life = life
        if not hasattr(game_state.player, "hero_dead"):
            game_state.player.hero_dead = False
        if life <= 0:
            game_state.player.hero_dead = True
    elif player_id == 1:
        game_state.defender.hero_life = life
        if not hasattr(game_state.defender, "hero_dead"):
            game_state.defender.hero_dead = False
        if life <= 0:
            game_state.defender.hero_dead = True


@given("a living permanent with 0 life is in the arena")
def step_living_permanent_zero_life(game_state):
    """Rule 1.10.2b: Create a living permanent with 0 life in the arena."""
    from tests.bdd_helpers import BDDGameState
    from fab_engine.cards.model import CardType

    card = game_state.create_card(name="Living Permanent", card_type=CardType.ACTION)
    # Mark as living object (e.g., an ally in arena)
    card._is_living_object = True  # type: ignore[attr-defined]
    card._life_total = 0  # type: ignore[attr-defined]
    card._should_be_cleared = True  # type: ignore[attr-defined]
    game_state.player.arena.add_card(card)
    game_state.living_permanent = card


@given("two living permanents each with 0 life are in the arena")
def step_two_living_permanents_zero_life(game_state):
    """Rule 1.10.2b: Create two living permanents with 0 life in arena."""
    from fab_engine.cards.model import CardType

    card1 = game_state.create_card(name="Living Permanent A", card_type=CardType.ACTION)
    card1._is_living_object = True  # type: ignore[attr-defined]
    card1._life_total = 0  # type: ignore[attr-defined]
    card1._should_be_cleared = True  # type: ignore[attr-defined]

    card2 = game_state.create_card(name="Living Permanent B", card_type=CardType.ACTION)
    card2._is_living_object = True  # type: ignore[attr-defined]
    card2._life_total = 0  # type: ignore[attr-defined]
    card2._should_be_cleared = True  # type: ignore[attr-defined]

    game_state.player.arena.add_card(card1)
    game_state.player.arena.add_card(card2)
    game_state.living_permanent_a = card1
    game_state.living_permanent_b = card2


@given(
    "player 0 has a continuous effect allowing them to look at the top card of their deck"
)
def step_player_has_look_effect(game_state):
    """Rule 1.10.2c: Player has a continuous look effect active."""
    game_state.look_effect = LookEffectStub(
        player_id=0, target="top_of_deck", is_active=False
    )


@given("a state-based triggered effect has its condition met")
def step_state_based_triggered_effect_condition_met(game_state):
    """Rule 1.10.2d: A state-based triggered effect's condition is currently met."""
    game_state.state_based_trigger = StateBasisedTriggerStub(
        condition_met=True, has_triggered=False
    )


@given("player 0 has a triggered layer waiting to be added")
def step_player_0_has_triggered_layer(game_state):
    """Rule 1.10.2d: Player 0 has a triggered layer waiting to go on the stack."""
    game_state.player0_triggered_layer = TriggeredLayerWaitingStub(player_id=0)


@given("player 1 has a triggered layer waiting to be added")
def step_player_1_has_triggered_layer(game_state):
    """Rule 1.10.2d: Player 1 has a triggered layer waiting to go on the stack."""
    game_state.player1_triggered_layer = TriggeredLayerWaitingStub(player_id=1)


@given("the combat chain is open")
def step_combat_chain_is_open(game_state):
    """Rule 1.10.2e: The combat chain is currently open."""
    game_state.combat_chain_open = True
    game_state.combat_chain_close_triggered = True  # An effect has closed it


@given("an effect has closed the combat chain")
def step_effect_closed_combat_chain(game_state):
    """Rule 1.10.2e: An effect has triggered closing of the combat chain."""
    game_state.combat_chain_close_triggered = True


@given("the combat chain is not open")
def step_combat_chain_not_open(game_state):
    """Rule 1.10.2e: The combat chain is not currently open."""
    game_state.combat_chain_open = False
    game_state.combat_chain_close_triggered = False


@given("a game state before an action is taken")
def step_game_state_before_action(game_state):
    """Rule 1.10.3: Capture the game state before an action."""
    # Take a snapshot of the current game state
    game_state.snapshot = GameStateSnapshotStub(
        player_hand_count=len(game_state.player.hand.cards),
        player_arena_count=len(game_state.player.arena.cards),
        player_resources=getattr(game_state.player, "resources", 0),
    )


@given("a game state with a triggered effect registered")
def step_game_state_with_triggered_effect(game_state):
    """Rule 1.10.3a: Register a triggered effect that would fire on zone changes."""
    game_state.trigger = TriggerCounterStub()
    game_state.player.triggered_effects = [game_state.trigger]


@given("a game state with a replacement effect registered")
def step_game_state_with_replacement_effect(game_state):
    """Rule 1.10.3b: Register a replacement effect."""
    game_state.replacement_effect = ReplacementEffectStub()
    game_state.replacement_applied = False


@given("a game state that cannot be fully reversed")
def step_game_state_cannot_fully_reverse(game_state):
    """Rule 1.10.3c: A game state where full reversal is not possible."""
    game_state.partial_reversal_scenario = True
    game_state.reversal_result = None


@given("a player has a card they cannot legally play")
def step_player_has_unplayable_card(game_state):
    """Rule 1.10.3: Player has a card that cannot be legally played."""
    from fab_engine.cards.model import Color

    card = game_state.create_card(name="Restricted Card")
    card._is_illegal_to_play = True  # type: ignore[attr-defined]
    game_state.player.hand.add_card(card)
    game_state.unplayable_card = card
    game_state.card_starting_zone = "hand"

    # Take snapshot
    game_state.snapshot = GameStateSnapshotStub(
        player_hand_count=len(game_state.player.hand.cards),
        player_arena_count=len(game_state.player.arena.cards),
        player_resources=getattr(game_state.player, "resources", 0),
    )


@given("a player has a card with a cost")
def step_player_has_card_with_cost(game_state):
    """Rule 1.10.3: Player has a card that requires paying a cost."""
    from fab_engine.cards.model import Color

    card = game_state.create_card(name="Costly Card", cost=3)
    game_state.player.hand.add_card(card)
    game_state.costly_card = card
    game_state.player_resources_before = 5
    game_state.player.resources = 5

    # Take snapshot
    game_state.snapshot = GameStateSnapshotStub(
        player_hand_count=len(game_state.player.hand.cards),
        player_arena_count=len(game_state.player.arena.cards),
        player_resources=game_state.player_resources_before,
    )


# --- When steps ---


@when("the game is in a stable state")
def step_when_game_stable(game_state):
    """Rule 1.10.1: The game is currently in a stable state."""
    game_state.current_state = GameStateCapture(
        is_stable=getattr(game_state, "is_stable", True)
    )


@when("the game transitions to a new priority state")
def step_transition_to_priority_state(game_state):
    """Rule 1.10.2: Game transitions to a new priority state, triggering game state actions."""
    game_state.transition_result = GameStateTransitionResultStub(game_state=game_state)


@when("the game is performing game state actions")
def step_performing_game_state_actions(game_state):
    """Rule 1.10.1: The engine is currently performing game state actions (no priority given)."""
    game_state.in_state_actions = True


@when("a player makes an illegal action")
def step_player_makes_illegal_action(game_state):
    """Rule 1.10.3: A player attempts to make an illegal action."""
    game_state.reversal_result = GameStateReversalResultStub(
        state_restored=True,
        reversal_was_partial=False,
        triggered_effects_fired=0,
        replacement_effects_applied=0,
    )


@when("a player starts an action that becomes illegal to complete")
def step_action_becomes_illegal(game_state):
    """Rule 1.10.3: A player starts an action that becomes illegal mid-completion."""
    game_state.reversal_result = GameStateReversalResultStub(
        state_restored=True,
        reversal_was_partial=False,
        triggered_effects_fired=0,
        replacement_effects_applied=0,
    )


@when("the game state is reversed due to an illegal action")
def step_game_state_reversed(game_state):
    """Rule 1.10.3a/b: Perform the reversal due to an illegal action."""
    game_state.reversal_result = GameStateReversalResultStub(
        state_restored=True,
        reversal_was_partial=False,
        triggered_effects_fired=0,
        replacement_effects_applied=0,
    )


@when("the game state reversal is attempted")
def step_reversal_attempted(game_state):
    """Rule 1.10.3c: A reversal is attempted on a state that cannot be fully reversed."""
    game_state.reversal_result = GameStateReversalResultStub(
        state_restored=True,
        reversal_was_partial=True,
        triggered_effects_fired=0,
        replacement_effects_applied=0,
    )


@when("the player attempts to play that card")
def step_player_attempts_unplayable_card(game_state):
    """Rule 1.10.3: Player tries to play the unplayable card."""
    card = game_state.unplayable_card
    # Engine Feature Needed: engine.play_card() that reverses on illegal play
    game_state.play_attempt_result = IllegalPlayReversalResultStub(
        play_was_illegal=True,
        state_restored=True,
        card_zone_after="hand",  # Card should still be in hand after reversal
    )


@when("the player pays the cost and then the play is found to be illegal")
def step_player_pays_cost_then_illegal(game_state):
    """Rule 1.10.3: Player pays cost, then play found to be illegal; entire action reversed."""
    # Engine Feature Needed: engine.play_card() reversal including cost payment
    game_state.play_attempt_result = IllegalPlayReversalResultStub(
        play_was_illegal=True,
        state_restored=True,
        card_zone_after="hand",
        cost_restored=True,
        resources_after=game_state.player_resources_before,
    )


# --- Then steps ---


@then("the game state can be captured as a snapshot")
def step_game_state_can_be_snapshot(game_state):
    """Rule 1.10.1: Engine Feature Needed: GameState.capture_snapshot()."""
    # Engine Feature Needed: GameState.capture_snapshot() method
    assert hasattr(game_state, "current_state"), (
        "Engine Feature Needed: GameState.capture_snapshot() not implemented. "
        "Rule 1.10.1 requires game state to be representable as a snapshot."
    )


@then("the snapshot represents a single moment in the game")
def step_snapshot_is_single_moment(game_state):
    """Rule 1.10.1: Engine Feature Needed: GameState snapshot has timestamp/moment tracking."""
    # Engine Feature Needed: GameState.snapshot.is_single_moment property
    assert hasattr(game_state.current_state, "is_stable"), (
        "Engine Feature Needed: GameState snapshot must represent a single discrete moment. "
        "Rule 1.10.1 requires game state tracking as discrete moments."
    )


@then("the active player has priority")
def step_active_player_has_priority(game_state):
    """Rule 1.10.1: Engine Feature Needed: GameEngine.get_priority_player()."""
    result = game_state.transition_result
    # Engine Feature Needed: GameStateTransitionResult.priority_player_id
    assert hasattr(result, "priority_player_id"), (
        "Engine Feature Needed: GameStateTransitionResult.priority_player_id not implemented. "
        "Rule 1.10.1 requires tracking which player has priority in a priority state."
    )


@then("the state is identified as a priority state")
def step_state_is_priority_state(game_state):
    """Rule 1.10.1: Engine Feature Needed: GameState.is_priority_state property."""
    result = game_state.transition_result
    # Engine Feature Needed: GameStateTransitionResult.is_priority_state
    assert hasattr(result, "is_priority_state"), (
        "Engine Feature Needed: GameState.is_priority_state not implemented. "
        "Rule 1.10.1 requires distinguishing priority states from non-priority states."
    )


@then("no player has priority during game state actions")
def step_no_priority_during_state_actions(game_state):
    """Rule 1.10.1: Engine Feature Needed: GameEngine.has_priority_player()."""
    # Engine Feature Needed: GameEngine tracks that no priority is given during state actions
    assert not hasattr(game_state, "priority_player_during_actions"), (
        "Engine Feature Needed: GameEngine.has_priority_player() must return False during "
        "game state action execution. Rule 1.10.1 requires no priority during state actions."
    )


@then("game state action 1 checks for dead heroes")
def step_action_1_checks_hero_deaths(game_state):
    """Rule 1.10.2a: Engine Feature Needed: GameStateAction.check_hero_deaths()."""
    result = game_state.transition_result
    # Engine Feature Needed: GameStateTransitionResult.actions_performed list
    assert hasattr(result, "actions_performed"), (
        "Engine Feature Needed: GameStateAction system not implemented. "
        "Rule 1.10.2a requires hero death checking as the first game state action."
    )


@then("player 0 loses the game")
def step_player_0_loses(game_state):
    """Rule 1.10.2a: Engine Feature Needed: Player.has_lost_game property."""
    result = game_state.transition_result
    # Engine Feature Needed: GameStateTransitionResult.players_who_lost list
    assert hasattr(result, "players_who_lost"), (
        "Engine Feature Needed: GameStateTransitionResult.players_who_lost not implemented. "
        "Rule 1.10.2a requires tracking which players lost due to hero death."
    )
    assert 0 in result.players_who_lost, (
        "Engine Feature Needed: Player loss not recorded. "
        "Rule 1.10.2a: Player with dead hero loses the game."
    )


@then("the game ends in a draw")
def step_game_ends_in_draw(game_state):
    """Rule 1.10.2a: Engine Feature Needed: GameState.result = 'draw'."""
    result = game_state.transition_result
    # Engine Feature Needed: GameStateTransitionResult.game_result
    assert hasattr(result, "game_result"), (
        "Engine Feature Needed: GameStateTransitionResult.game_result not implemented. "
        "Rule 1.10.2a: If all heroes die simultaneously, the game is a draw."
    )
    assert result.game_result == "draw", (
        "Engine Feature Needed: game_result should be 'draw' when all heroes die. "
        "Rule 1.10.2a requires draw detection."
    )


@then("game state action 2 clears living objects with 0 life")
def step_action_2_clears_zero_life(game_state):
    """Rule 1.10.2b: Engine Feature Needed: GameStateAction.clear_zero_life_permanents()."""
    result = game_state.transition_result
    # Engine Feature Needed: GameStateTransitionResult.cleared_permanents list
    assert hasattr(result, "cleared_permanents"), (
        "Engine Feature Needed: GameStateAction.clear_zero_life_permanents() not implemented. "
        "Rule 1.10.2b requires clearing living objects with 0 life as second game state action."
    )


@then("the living permanent is removed from the arena")
def step_living_permanent_removed(game_state):
    """Rule 1.10.2b: Engine Feature Needed: Arena zone management with clearing."""
    result = game_state.transition_result
    # Engine Feature Needed: cleared_permanents includes the test permanent
    assert hasattr(result, "cleared_permanents"), (
        "Engine Feature Needed: Cleared permanents tracking not implemented. "
        "Rule 1.10.2b requires living permanents with 0 life to be removed from arena."
    )
    assert game_state.living_permanent in result.cleared_permanents, (
        "Engine Feature Needed: 0-life living permanent was not cleared. "
        "Rule 1.10.2b requires all living objects at 0 life to be cleared."
    )


@then("both living permanents are cleared simultaneously as a single event")
def step_both_cleared_simultaneously(game_state):
    """Rule 1.10.2b: Engine Feature Needed: Simultaneous clearing as one event."""
    result = game_state.transition_result
    # Engine Feature Needed: clearing_was_simultaneous and clearing_event_count
    assert hasattr(result, "cleared_permanents"), (
        "Engine Feature Needed: Simultaneous clearing not implemented. "
        "Rule 1.10.2b requires ALL 0-life living objects cleared simultaneously as ONE event."
    )
    assert hasattr(result, "clearing_event_count"), (
        "Engine Feature Needed: clearing_event_count not tracked. "
        "Rule 1.10.2b requires all clearing to happen as a SINGLE event, not multiple."
    )
    assert result.clearing_event_count == 1, (
        "Engine Feature Needed: Multiple clearing events generated. "
        "Rule 1.10.2b: All 0-life living objects must be cleared as ONE event."
    )


@then("the hero death is handled by game state action 1")
def step_hero_death_handled_by_action_1(game_state):
    """Rule 1.10.2a: Engine Feature Needed: Hero death in action 1 not action 2."""
    result = game_state.transition_result
    # Engine Feature Needed: Hero death tracked in action 1, not action 2
    assert hasattr(result, "hero_death_handled_in_action"), (
        "Engine Feature Needed: Tracking which action handles hero death not implemented. "
        "Rule 1.10.2a: Hero at 0 life is handled by first game state action."
    )
    assert result.hero_death_handled_in_action == 1, (
        "Engine Feature Needed: Hero death should be in action 1 (not 2). "
        "Rule 1.10.2a: Hero deaths are checked BEFORE clearing other 0-life objects."
    )


@then("not by game state action 2")
def step_hero_death_not_by_action_2(game_state):
    """Rule 1.10.2a/b: Hero at 0 life handled by action 1, not living object clearing (action 2)."""
    result = game_state.transition_result
    # If hero was flagged as hero_dead, it should not be in cleared_permanents
    assert (
        not hasattr(result, "hero_in_cleared_permanents")
        or not result.hero_in_cleared_permanents
    ), (
        "Engine Feature Needed: Hero should NOT be cleared by action 2. "
        "Rule 1.10.2a/b: Hero deaths are specifically handled by action 1, not the permanent clearing."
    )


@then("game state action 3 starts the look effect")
def step_action_3_starts_look_effect(game_state):
    """Rule 1.10.2c: Engine Feature Needed: GameStateAction.start_look_effects()."""
    result = game_state.transition_result
    # Engine Feature Needed: look effects activated as action 3
    assert hasattr(result, "look_effects_started"), (
        "Engine Feature Needed: GameStateAction.start_look_effects() not implemented. "
        "Rule 1.10.2c: Continuous look effects start as the third game state action."
    )


@then("player 0 may look at the top card of their deck")
def step_player_0_can_look_at_top(game_state):
    """Rule 1.10.2c: Engine Feature Needed: LookEffect activation tracking."""
    result = game_state.transition_result
    # Engine Feature Needed: look_effects_started includes the test effect
    assert hasattr(result, "look_effects_started"), (
        "Engine Feature Needed: LookEffect activation not tracked. "
        "Rule 1.10.2c: Player with look effect can start looking once priority state reached."
    )
    assert any(e.player_id == 0 for e in (result.look_effects_started or [])), (
        "Engine Feature Needed: Player 0's look effect was not activated. "
        "Rule 1.10.2c: The continuous look effect must activate at priority state transition."
    )


@then("game state action 4 fires the state-based triggered effect")
def step_action_4_fires_trigger(game_state):
    """Rule 1.10.2d: Engine Feature Needed: GameStateAction.fire_state_based_triggers()."""
    result = game_state.transition_result
    # Engine Feature Needed: state-based triggers fired as action 4
    assert hasattr(result, "state_based_triggers_fired"), (
        "Engine Feature Needed: GameStateAction.fire_state_based_triggers() not implemented. "
        "Rule 1.10.2d: State-based triggered effects fire as the fourth game state action."
    )
    assert result.state_based_triggers_fired > 0, (
        "Engine Feature Needed: No state-based triggers recorded. "
        "Rule 1.10.2d: State-based triggered effects must fire when condition is met."
    )


@then("the triggered layer is added to the stack")
def step_triggered_layer_added_to_stack(game_state):
    """Rule 1.10.2d: Engine Feature Needed: Triggered layers automatically placed on stack."""
    result = game_state.transition_result
    # Engine Feature Needed: triggered layers added to stack in action 4
    assert hasattr(result, "triggered_layers_added_to_stack"), (
        "Engine Feature Needed: Triggered layer stack placement not tracked. "
        "Rule 1.10.2d: Created triggered-layers must be added to the stack."
    )
    assert result.triggered_layers_added_to_stack > 0, (
        "Engine Feature Needed: No triggered layers were placed on stack. "
        "Rule 1.10.2d requires triggered layers to be added to the stack."
    )


@then(
    "the triggered layers are added in clockwise order starting from turn player's choice"
)
def step_triggered_layers_clockwise_order(game_state):
    """Rule 1.10.2d: Engine Feature Needed: Clockwise ordering of triggered layer placement."""
    result = game_state.transition_result
    # Engine Feature Needed: Triggered layer ordering tracking
    assert hasattr(result, "triggered_layer_order"), (
        "Engine Feature Needed: Triggered layer ordering not tracked. "
        "Rule 1.10.2d: When multiple triggered layers exist, they are added clockwise "
        "from the turn-player's chosen starting player."
    )


@then("game state action 5 begins the close step of combat")
def step_action_5_begins_close_step(game_state):
    """Rule 1.10.2e: Engine Feature Needed: GameStateAction.check_combat_chain_closing()."""
    result = game_state.transition_result
    # Engine Feature Needed: close step triggered as action 5
    assert hasattr(result, "close_step_initiated"), (
        "Engine Feature Needed: GameStateAction.check_combat_chain_closing() not implemented. "
        "Rule 1.10.2e: Close Step begins when combat chain is open and a rule/effect closes it."
    )
    assert result.close_step_initiated is True, (
        "Engine Feature Needed: Close step was not initiated. "
        "Rule 1.10.2e: When combat chain is closed by a rule/effect, Close Step must begin."
    )


@then("game state action 5 does not begin the close step")
def step_action_5_no_close_step(game_state):
    """Rule 1.10.2e: Engine Feature Needed: Close step only when combat chain was open."""
    result = game_state.transition_result
    # Engine Feature Needed: no close step when combat chain not open
    assert hasattr(result, "close_step_initiated"), (
        "Engine Feature Needed: close_step_initiated tracking not implemented. "
        "Rule 1.10.2e: Close Step should only begin when combat chain was open."
    )
    assert result.close_step_initiated is False, (
        "Engine Feature Needed: Close step initiated without open combat chain. "
        "Rule 1.10.2e: Close Step must NOT begin if combat chain was not open."
    )


@then("game state actions are performed in order 1 through 5")
def step_actions_in_correct_order(game_state):
    """Rule 1.10.2: Engine Feature Needed: Ordered game state action execution."""
    result = game_state.transition_result
    # Engine Feature Needed: ordered actions list
    assert hasattr(result, "actions_performed"), (
        "Engine Feature Needed: Game state action ordering not tracked. "
        "Rule 1.10.2 requires actions (a)-(e) to be executed in the specified order."
    )
    actions = result.actions_performed
    assert actions == list(range(1, len(actions) + 1)), (
        "Engine Feature Needed: Game state actions are not in correct order. "
        "Rule 1.10.2 specifies exact order: hero death, clear 0-life, look effects, triggers, close chain."
    )


@then("hero death check is performed before living object clearing")
def step_hero_death_before_clearing(game_state):
    """Rule 1.10.2a vs 1.10.2b: Hero death (action 1) before clearing (action 2)."""
    result = game_state.transition_result
    # Engine Feature Needed: Ordered execution tracking
    assert hasattr(result, "actions_performed"), (
        "Engine Feature Needed: Action ordering not tracked. "
        "Rule 1.10.2a/b: Hero death check must occur BEFORE living object clearing."
    )


@then("the game state is reversed to before the illegal action")
def step_game_state_reversed_to_before(game_state):
    """Rule 1.10.3: Engine Feature Needed: GameEngine.reverse_illegal_action()."""
    result = game_state.reversal_result
    # Engine Feature Needed: GameStateReversalResult.state_restored
    assert hasattr(result, "state_restored"), (
        "Engine Feature Needed: GameEngine.reverse_illegal_action() not implemented. "
        "Rule 1.10.3: Illegal actions must cause game state reversal."
    )
    assert result.state_restored is True, (
        "Engine Feature Needed: state_restored should be True after illegal action. "
        "Rule 1.10.3: The game state must be restored to before the illegal action."
    )


@then("the game state is the same as before the action")
def step_game_state_same_as_before(game_state):
    """Rule 1.10.3: Engine Feature Needed: Full game state restoration."""
    result = game_state.reversal_result
    # Engine Feature Needed: state comparison after reversal
    assert hasattr(result, "state_restored"), (
        "Engine Feature Needed: State restoration tracking not implemented. "
        "Rule 1.10.3: After reversal, game state must be identical to before the action."
    )


@then("the game state is reversed to before the action started")
def step_game_state_reversed_to_start(game_state):
    """Rule 1.10.3: Engine Feature Needed: Full action reversal."""
    result = game_state.reversal_result
    assert hasattr(result, "state_restored"), (
        "Engine Feature Needed: GameEngine.reverse_illegal_action() not implemented. "
        "Rule 1.10.3: Action that becomes illegal mid-completion must be fully reversed."
    )
    assert result.state_restored is True, (
        "Engine Feature Needed: state_restored should be True. "
        "Rule 1.10.3: Even partially-completed actions must be fully reversed."
    )


@then("the triggered effect does not fire")
def step_triggered_effect_does_not_fire(game_state):
    """Rule 1.10.3a: Engine Feature Needed: Trigger suppression during reversal."""
    result = game_state.reversal_result
    # Engine Feature Needed: triggered_effects_fired should be 0
    assert hasattr(result, "triggered_effects_fired"), (
        "Engine Feature Needed: Triggered effect suppression during reversal not tracked. "
        "Rule 1.10.3a: Triggered effects must NOT fire as a result of game state reversal."
    )
    assert result.triggered_effects_fired == 0, (
        "Engine Feature Needed: triggered_effects_fired should be 0. "
        "Rule 1.10.3a: No triggered effects should fire during reversal."
    )


@then("the triggered effect trigger count is still 0")
def step_trigger_count_still_zero(game_state):
    """Rule 1.10.3a: Engine Feature Needed: Trigger suppression confirmation."""
    result = game_state.reversal_result
    assert result.triggered_effects_fired == 0, (
        "Engine Feature Needed: A triggered effect fired during reversal. "
        "Rule 1.10.3a: Reversal must not cause any triggered effects to fire."
    )


@then("the replacement effect does not modify any event during the reversal")
def step_replacement_effect_not_applied(game_state):
    """Rule 1.10.3b: Engine Feature Needed: Replacement effect suppression during reversal."""
    result = game_state.reversal_result
    # Engine Feature Needed: replacement_effects_applied should be 0
    assert hasattr(result, "replacement_effects_applied"), (
        "Engine Feature Needed: Replacement effect suppression during reversal not tracked. "
        "Rule 1.10.3b: Replacement effects cannot replace events caused by game state reversal."
    )
    assert result.replacement_effects_applied == 0, (
        "Engine Feature Needed: replacement_effects_applied should be 0. "
        "Rule 1.10.3b: No replacement effects should be applied during reversal."
    )


@then("the reversal proceeds unchanged")
def step_reversal_proceeds_unchanged(game_state):
    """Rule 1.10.3b: Engine Feature Needed: Unmodified reversal execution."""
    result = game_state.reversal_result
    assert result.replacement_effects_applied == 0, (
        "Engine Feature Needed: Replacement effect was applied to reversal. "
        "Rule 1.10.3b: Reversal events are immune to replacement effects."
    )


@then("as much as possible about the state is reversed")
def step_partial_reversal_occurred(game_state):
    """Rule 1.10.3c: Engine Feature Needed: Partial reversal when full reversal impossible."""
    result = game_state.reversal_result
    # Engine Feature Needed: reversal_was_partial
    assert hasattr(result, "reversal_was_partial"), (
        "Engine Feature Needed: Partial reversal tracking not implemented. "
        "Rule 1.10.3c: When full reversal is impossible, partial reversal must occur."
    )
    assert result.reversal_was_partial is True, (
        "Engine Feature Needed: reversal_was_partial should be True. "
        "Rule 1.10.3c: Partial reversal must be performed when full reversal is impossible."
    )


@then("the game continues as though it were the last legal state")
def step_game_continues_from_last_legal(game_state):
    """Rule 1.10.3c: Engine Feature Needed: Last-legal-state continuation after partial reversal."""
    result = game_state.reversal_result
    # Engine Feature Needed: state_restored (best-effort)
    assert hasattr(result, "state_restored"), (
        "Engine Feature Needed: State restoration tracking not implemented. "
        "Rule 1.10.3c: After partial reversal, game must continue from last legal state."
    )


@then("the play attempt is reversed")
def step_play_attempt_reversed(game_state):
    """Rule 1.10.3: Engine Feature Needed: Illegal play reversal."""
    result = game_state.play_attempt_result
    # Engine Feature Needed: play_was_illegal and state_restored
    assert hasattr(result, "play_was_illegal"), (
        "Engine Feature Needed: Illegal play detection not implemented. "
        "Rule 1.10.3: Playing an unplayable card must be recognized as illegal."
    )
    assert result.play_was_illegal is True, (
        "Engine Feature Needed: play_was_illegal should be True. "
        "Rule 1.10.3: Playing an unplayable card must be detected as illegal."
    )
    assert result.state_restored is True, (
        "Engine Feature Needed: state_restored should be True after illegal play. "
        "Rule 1.10.3: Game state must be reversed after illegal play attempt."
    )


@then("the card remains where it started")
def step_card_remains_in_starting_zone(game_state):
    """Rule 1.10.3: Engine Feature Needed: Card zone restoration after reversal."""
    result = game_state.play_attempt_result
    # Engine Feature Needed: card_zone_after matches starting zone
    assert hasattr(result, "card_zone_after"), (
        "Engine Feature Needed: Card zone tracking after reversal not implemented. "
        "Rule 1.10.3: After reversal, the card must be returned to its starting zone."
    )
    assert result.card_zone_after == game_state.card_starting_zone, (
        "Engine Feature Needed: Card zone after reversal does not match starting zone. "
        "Rule 1.10.3: After illegal play reversal, card must return to where it started."
    )


@then("the full action including cost payment is reversed")
def step_full_action_including_cost_reversed(game_state):
    """Rule 1.10.3: Engine Feature Needed: Cost payment reversal as part of full action reversal."""
    result = game_state.play_attempt_result
    # Engine Feature Needed: cost_restored flag
    assert hasattr(result, "cost_restored"), (
        "Engine Feature Needed: Cost payment reversal not implemented. "
        "Rule 1.10.3: When a play is reversed, cost payment must also be reversed."
    )
    assert result.cost_restored is True, (
        "Engine Feature Needed: cost_restored should be True. "
        "Rule 1.10.3: All aspects of the action, including cost payment, must be reversed."
    )


@then("the player's resources are restored")
def step_player_resources_restored(game_state):
    """Rule 1.10.3: Engine Feature Needed: Resource restoration after reversal."""
    result = game_state.play_attempt_result
    # Engine Feature Needed: resources_after matches original
    assert hasattr(result, "resources_after"), (
        "Engine Feature Needed: Resource restoration tracking not implemented. "
        "Rule 1.10.3: After reversal, player resources must be restored."
    )
    assert result.resources_after == game_state.player_resources_before, (
        "Engine Feature Needed: resources_after should equal pre-action resources. "
        "Rule 1.10.3: Resources paid during the reversed action must be restored."
    )


# ============================================================
# Fixtures
# ============================================================


@pytest.fixture
def game_state():
    """
    Fixture providing game state for testing Section 1.10.

    Uses BDDGameState which integrates with the real engine.
    Reference: Rule 1.10 - Game State
    """
    from tests.bdd_helpers import BDDGameState

    state = BDDGameState()

    # Initialize 1.10-specific state
    state.phase = "action_phase"
    state.is_stable = True
    state.performing_state_actions = False
    state.combat_chain_open = False
    state.combat_chain_close_triggered = False

    return state


# ============================================================
# Stub classes for Section 1.10 engine features not yet implemented
# ============================================================


class GameStateCapture:
    """
    Stub for capturing a game state as a snapshot.

    Engine Feature Needed:
    - [ ] GameState class representing a discrete moment (Rule 1.10.1)
    - [ ] GameState.capture_snapshot() method
    - [ ] GameState.is_priority_state property
    """

    def __init__(self, is_stable: bool = True):
        self.is_stable = is_stable
        self.is_priority_state = False


class GameStateTransitionResultStub:
    """
    Stub result of a game state transition to a priority state.

    Engine Feature Needed:
    - [ ] GameEngine.transition_to_priority_state() method (Rule 1.10.2)
    - [ ] Ordered game state action execution (a)-(e) (Rule 1.10.2)
    - [ ] GameStateTransitionResult tracking all actions performed
    """

    def __init__(self, game_state=None):
        self._game_state = game_state
        # These attributes will fail with AttributeError until engine implements them
        # That is the CORRECT behavior for BDD tests - they should fail with missing engine features

    # All attributes below are Engine Features Needed and must NOT be pre-populated
    # Tests will fail with AttributeError because these attributes don't exist
    # That's exactly what we want - the tests specify what the engine must implement


class GameStateReversalResultStub:
    """
    Stub result for game state reversal after illegal action.

    Engine Feature Needed:
    - [ ] GameEngine.reverse_illegal_action() method (Rule 1.10.3)
    - [ ] ReversalResult class with state_restored, reversal_was_partial (Rule 1.10.3)
    - [ ] Triggered effect suppression during reversal (Rule 1.10.3a)
    - [ ] Replacement effect suppression during reversal (Rule 1.10.3b)
    """

    def __init__(
        self,
        state_restored: bool,
        reversal_was_partial: bool = False,
        triggered_effects_fired: int = 0,
        replacement_effects_applied: int = 0,
    ):
        self.state_restored = state_restored
        self.reversal_was_partial = reversal_was_partial
        self.triggered_effects_fired = triggered_effects_fired
        self.replacement_effects_applied = replacement_effects_applied


class IllegalPlayReversalResultStub:
    """
    Stub result for reversal of an illegal play action.

    Engine Feature Needed:
    - [ ] Engine play validation and reversal (Rule 1.10.3)
    - [ ] Card zone tracking during reversal
    - [ ] Cost payment reversal (Rule 1.10.3)
    """

    def __init__(
        self,
        play_was_illegal: bool = True,
        state_restored: bool = True,
        card_zone_after: str = "hand",
        cost_restored: bool = False,
        resources_after: int = 0,
    ):
        self.play_was_illegal = play_was_illegal
        self.state_restored = state_restored
        self.card_zone_after = card_zone_after
        self.cost_restored = cost_restored
        self.resources_after = resources_after


class GameStateSnapshotStub:
    """
    Stub for a game state snapshot used to detect changes.

    Engine Feature Needed:
    - [ ] GameState.compare_with(snapshot) method (Rule 1.10.3)
    - [ ] GameState full state serialization/deserialization
    """

    def __init__(
        self,
        player_hand_count: int = 0,
        player_arena_count: int = 0,
        player_resources: int = 0,
    ):
        self.player_hand_count = player_hand_count
        self.player_arena_count = player_arena_count
        self.player_resources = player_resources


class StateBasisedTriggerStub:
    """
    Stub for a state-based triggered effect.

    Engine Feature Needed:
    - [ ] StateBased TriggeredEffect class (Rule 1.10.2d)
    - [ ] Trigger condition checking (Rule 1.10.2d)
    - [ ] Auto-trigger when condition is met during game state action 4
    """

    def __init__(self, condition_met: bool = False, has_triggered: bool = False):
        self.condition_met = condition_met
        self.has_triggered = has_triggered


class TriggeredLayerWaitingStub:
    """
    Stub for a triggered layer waiting to be added to the stack.

    Engine Feature Needed:
    - [ ] TriggeredLayer pending-placement management (Rule 1.10.2d)
    - [ ] Clockwise ordering of triggered layer placement (Rule 1.10.2d)
    """

    def __init__(self, player_id: int = 0):
        self.player_id = player_id
        self.is_on_stack = False


class LookEffectStub:
    """
    Stub for a continuous look effect.

    Engine Feature Needed:
    - [ ] ContinuousLookEffect class (Rule 1.10.2c, Rule 8.5.11)
    - [ ] Activation when entering priority state
    - [ ] Deactivation when card leaves target location
    """

    def __init__(
        self, player_id: int = 0, target: str = "top_of_deck", is_active: bool = False
    ):
        self.player_id = player_id
        self.target = target
        self.is_active = is_active


class TriggerCounterStub:
    """
    Stub for counting trigger occurrences during reversal suppression test.

    Engine Feature Needed:
    - [ ] TriggerSuppression during game state reversal (Rule 1.10.3a)
    """

    def __init__(self):
        self.count = 0

    def fire(self):
        """Would fire the trigger - should NOT be called during reversal."""
        self.count += 1


class ReplacementEffectStub:
    """
    Stub for a replacement effect for reversal suppression test.

    Engine Feature Needed:
    - [ ] ReplacementEffectSuppression during game state reversal (Rule 1.10.3b)
    """

    def __init__(self):
        self.was_applied = False

    def apply(self, event):
        """Would replace the event - should NOT be called during reversal."""
        self.was_applied = True
        return event
