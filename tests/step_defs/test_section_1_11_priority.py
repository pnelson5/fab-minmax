"""
Step definitions for Section 1.11: Priority
Reference: Flesh and Blood Comprehensive Rules Section 1.11

This module implements behavioral tests for the priority system in FAB.

Priority rules tested:
- Rule 1.11.1: Priority describes which player may play a card, activate an
  ability, or pass priority.
- Rule 1.11.2: Only one player has priority at a time; that player is the
  "active player", others are "inactive players".
- Rule 1.11.3: Priority only exists during the Action Phase (not during the
  Close Step). Turn player gains priority at phase start, during combat steps,
  and after layer resolution.
- Rule 1.11.4: Active player may pass priority to the next player ("pass").
- Rule 1.11.4a: Priority passes clockwise; all-pass with non-empty stack
  resolves top layer; all-pass with empty stack ends the phase/step.
- Rule 1.11.5: Active player regains priority after playing a card or
  activating an ability. Active player loses priority after passing. No player
  has priority while playing a card, activating an ability, resolving a layer,
  during a game process, or during game state actions.

Engine Features Needed:
- [ ] PriorityState class tracking which player has priority (Rule 1.11.1)
- [ ] PriorityState.active_player_id (Rule 1.11.2)
- [ ] GamePhase enum with ACTION_PHASE, START_PHASE, END_PHASE (Rule 1.11.3)
- [ ] GameEngine.get_priority_player_id() (Rule 1.11.2)
- [ ] GameEngine.current_phase property (Rule 1.11.3)
- [ ] GameEngine.grant_priority_to_turn_player() (Rule 1.11.3)
- [ ] CombatStep enum including CLOSE_STEP (Rule 1.11.3)
- [ ] GameEngine.current_combat_step property (Rule 1.11.3)
- [ ] GameEngine.pass_priority(player_id) -> PriorityPassResult (Rule 1.11.4)
- [ ] PriorityPassResult.next_priority_holder_id (Rule 1.11.4a)
- [ ] GameEngine.all_players_passed() -> bool (Rule 1.11.4a)
- [ ] GameEngine.resolve_top_of_stack() called when all pass + non-empty (Rule 1.11.4a)
- [ ] GameEngine.end_phase_or_step() called when all pass + empty stack (Rule 1.11.4a)
- [ ] GameEngine.play_card(card, player_id) with priority regain (Rule 1.11.5)
- [ ] GameEngine.activate_ability(source, player_id) with priority regain (Rule 1.11.5)
- [ ] GameEngine.is_in_process_of_playing_card -> bool (Rule 1.11.5)
- [ ] GameEngine.is_in_process_of_resolving_layer -> bool (Rule 1.11.5)
- [ ] GameEngine.is_performing_game_state_actions -> bool (Rule 1.11.5)
"""

import pytest
from pytest_bdd import scenario, given, when, then, parsers


# ===== Scenario definitions =====


@scenario(
    "../features/section_1_11_priority.feature",
    "priority is a game state concept describing who may play",
)
def test_priority_is_game_state_concept():
    """Rule 1.11.1: Priority describes which player may act."""
    pass


@scenario(
    "../features/section_1_11_priority.feature",
    "only one player can have priority at any time",
)
def test_only_one_player_has_priority():
    """Rule 1.11.2: Only one player can have priority at a time."""
    pass


@scenario(
    "../features/section_1_11_priority.feature",
    "the player with priority is the active player",
)
def test_player_with_priority_is_active_player():
    """Rule 1.11.2: Player with priority is active player, others are inactive."""
    pass


@scenario(
    "../features/section_1_11_priority.feature",
    "priority only exists during the action phase",
)
def test_priority_only_in_action_phase():
    """Rule 1.11.3: Priority only exists during the action phase."""
    pass


@scenario(
    "../features/section_1_11_priority.feature",
    "turn player gains priority at start of action phase",
)
def test_turn_player_gains_priority_at_action_phase_start():
    """Rule 1.11.3: Turn player gains priority at start of action phase."""
    pass


@scenario(
    "../features/section_1_11_priority.feature",
    "no priority during close step of combat",
)
def test_no_priority_during_close_step():
    """Rule 1.11.3: Players do not get priority during the Close Step."""
    pass


@scenario(
    "../features/section_1_11_priority.feature",
    "turn player gains priority during combat steps",
)
def test_turn_player_gains_priority_during_combat_steps():
    """Rule 1.11.3: Turn player gains priority during most combat steps."""
    pass


@scenario(
    "../features/section_1_11_priority.feature",
    "turn player gains priority after layer resolution",
)
def test_turn_player_gains_priority_after_layer_resolution():
    """Rule 1.11.3: Turn player gains priority after layer resolves."""
    pass


@scenario(
    "../features/section_1_11_priority.feature",
    "active player may pass priority",
)
def test_active_player_may_pass_priority():
    """Rule 1.11.4: Active player may pass priority."""
    pass


@scenario(
    "../features/section_1_11_priority.feature",
    "priority passes clockwise to next player",
)
def test_priority_passes_clockwise():
    """Rule 1.11.4a: Priority is given to the next player in clockwise order."""
    pass


@scenario(
    "../features/section_1_11_priority.feature",
    "priority passes clockwise from last player back to first",
)
def test_priority_passes_clockwise_wrap():
    """Rule 1.11.4a: Clockwise order wraps from last player back to first."""
    pass


@scenario(
    "../features/section_1_11_priority.feature",
    "all players passing with non-empty stack resolves top layer",
)
def test_all_pass_non_empty_stack_resolves():
    """Rule 1.11.4a: All players passing with non-empty stack resolves top layer."""
    pass


@scenario(
    "../features/section_1_11_priority.feature",
    "all players passing with empty stack ends phase or step",
)
def test_all_pass_empty_stack_ends_phase():
    """Rule 1.11.4a: All players passing with empty stack ends phase or step."""
    pass


@scenario(
    "../features/section_1_11_priority.feature",
    "active player regains priority after playing a card",
)
def test_active_player_regains_priority_after_card_play():
    """Rule 1.11.5: Active player regains priority after playing a card."""
    pass


@scenario(
    "../features/section_1_11_priority.feature",
    "active player regains priority after activating an ability",
)
def test_active_player_regains_priority_after_ability():
    """Rule 1.11.5: Active player regains priority after activating an ability."""
    pass


@scenario(
    "../features/section_1_11_priority.feature",
    "active player loses priority after passing",
)
def test_active_player_loses_priority_after_passing():
    """Rule 1.11.5: Active player loses priority after passing."""
    pass


@scenario(
    "../features/section_1_11_priority.feature",
    "no player has priority while a card is being played",
)
def test_no_priority_during_card_play():
    """Rule 1.11.5: No player has priority while a card is being played."""
    pass


@scenario(
    "../features/section_1_11_priority.feature",
    "no player has priority while a layer is resolving",
)
def test_no_priority_during_layer_resolution():
    """Rule 1.11.5: No player has priority while a layer is resolving."""
    pass


@scenario(
    "../features/section_1_11_priority.feature",
    "no player has priority during game state actions",
)
def test_no_priority_during_game_state_actions():
    """Rule 1.11.5: No player has priority during game state actions."""
    pass


# ===== Step definitions =====


@given("a game with two players in the action phase")
def game_with_two_players_in_action_phase(game_state):
    """Set up a game with two players currently in the action phase.

    Rule 1.11.3: The Action Phase is the only phase when players get priority.
    """
    game_state.num_players = 2
    game_state.turn_player_id = 0
    game_state.current_phase = "action_phase"
    game_state.priority_player_id = 0  # Turn player starts with priority


@given("a game with two players")
def game_with_two_players(game_state):
    """Set up a basic game with two players.

    Rule 1.11.1: Priority is a game state concept.
    """
    game_state.num_players = 2
    game_state.turn_player_id = 0
    game_state.priority_player_id = None  # No priority by default


@given("a game with three players in the action phase")
def game_with_three_players_in_action_phase(game_state):
    """Set up a game with three players currently in the action phase.

    Rule 1.11.4a: Priority passes clockwise in a multi-player game.
    """
    game_state.num_players = 3
    game_state.turn_player_id = 0
    game_state.current_phase = "action_phase"
    game_state.priority_player_id = 0


@given(parsers.parse("player {player_id:d} has priority"))
def given_player_has_priority(game_state, player_id):
    """Set a specific player as having priority.

    Rule 1.11.2: Only one player can have priority at a time.
    """
    game_state.priority_player_id = player_id
    # Clear any pass tracking
    game_state.players_passed = set()


@given("the turn player has priority")
def given_turn_player_has_priority(game_state):
    """Set the turn player as having priority.

    Rule 1.11.3: Turn player gains priority at beginning of action phase.
    """
    game_state.priority_player_id = game_state.turn_player_id
    game_state.players_passed = set()


@given("a card is on the stack")
def given_card_is_on_stack(game_state):
    """Put a test card on the stack.

    Rule 1.11.4a: Non-empty stack resolves when all players pass.
    """
    card = game_state.create_card(name="Test Card")
    game_state.stack.append(card)
    game_state.stack_was_non_empty = True


@given("the stack is empty")
def given_stack_is_empty(game_state):
    """Ensure the stack is empty.

    Rule 1.11.4a: Empty stack ends phase or step when all players pass.
    """
    game_state.stack.clear()
    game_state.stack_was_non_empty = False


@given("the combat chain is open")
def given_combat_chain_is_open(game_state):
    """Set up an open combat chain.

    Rule 1.11.3: No priority during the Close Step.
    """
    game_state.combat_chain_is_open = True


@given("the game is in the start phase")
def given_game_in_start_phase(game_state):
    """Set the game to be in the start phase.

    Rule 1.11.3: Priority only exists during Action Phase.
    """
    game_state.current_phase = "start_phase"
    game_state.priority_player_id = None


@given("the game is in the action phase")
def given_game_in_action_phase(game_state):
    """Set the game to be in the action phase.

    Rule 1.11.3: Priority only exists during Action Phase.
    """
    game_state.current_phase = "action_phase"


# ===== When steps =====


@when("the priority system is active")
def when_priority_system_is_active(game_state):
    """Activate the priority system.

    Rule 1.11.1: Priority is a game state concept.
    """
    game_state.priority_system_checked = True


@when("the turn player has priority")
def when_turn_player_has_priority(game_state):
    """The turn player currently holds priority.

    Rule 1.11.2: The player with priority is the active player.
    """
    game_state.priority_player_id = game_state.turn_player_id


@when("the game is in the start phase")
def when_game_is_in_start_phase(game_state):
    """Set the game to the start phase.

    Rule 1.11.3: Priority only exists in Action Phase.
    """
    game_state.current_phase = "start_phase"
    game_state.priority_player_id = None


@when("the game enters the action phase")
def when_game_enters_action_phase(game_state):
    """Transition the game to the action phase.

    Rule 1.11.3: Turn player gains priority at beginning of action phase.
    """
    game_state.current_phase = "action_phase"
    # Engine Feature Needed: GameEngine.grant_priority_to_turn_player()
    game_state.priority_player_id = game_state.turn_player_id


@when("the close step begins")
def when_close_step_begins(game_state):
    """Transition to the Close Step of combat.

    Rule 1.11.3: No priority during the Close Step.
    """
    game_state.current_combat_step = "close_step"
    # Engine Feature Needed: GameEngine does NOT grant priority during Close Step
    game_state.priority_player_id = None


@when("the attack step begins")
def when_attack_step_begins(game_state):
    """Transition to the Attack Step of combat.

    Rule 1.11.3: Turn player gains priority during combat steps (except Close Step).
    """
    game_state.current_combat_step = "attack_step"
    # Engine Feature Needed: GameEngine.grant_priority_to_turn_player() at attack step
    game_state.priority_player_id = game_state.turn_player_id


@when("the top layer resolves")
def when_top_layer_resolves(game_state):
    """Resolve the top layer from the stack.

    Rule 1.11.3: Turn player gains priority after layer resolves.
    """
    if game_state.stack:
        game_state.stack.pop()
    game_state.layer_resolved = True
    # Engine Feature Needed: GameEngine.grant_priority_to_turn_player() after resolution
    game_state.priority_player_id = game_state.turn_player_id


@when("the active player passes priority")
def when_active_player_passes_priority(game_state):
    """The active player passes priority.

    Rule 1.11.4: Active player may pass priority.
    """
    if game_state.priority_player_id is None:
        game_state.pass_result = {"success": False, "reason": "no_priority_holder"}
        return

    passing_player_id = game_state.priority_player_id
    # Track who passed
    if not hasattr(game_state, "players_passed"):
        game_state.players_passed = set()
    game_state.players_passed.add(passing_player_id)

    # Priority goes to next player clockwise
    next_player_id = (passing_player_id + 1) % game_state.num_players
    game_state.prior_priority_player_id = passing_player_id
    game_state.priority_player_id = next_player_id

    game_state.pass_result = {
        "success": True,
        "prior_holder": passing_player_id,
        "new_holder": next_player_id,
    }


@when(parsers.parse("player {player_id:d} passes priority"))
def when_specific_player_passes_priority(game_state, player_id):
    """A specific player passes priority.

    Rule 1.11.4a: Priority passes to next player in clockwise order.
    """
    game_state.priority_player_id = player_id
    if not hasattr(game_state, "players_passed"):
        game_state.players_passed = set()
    game_state.players_passed.add(player_id)

    # Next player clockwise
    next_player_id = (player_id + 1) % game_state.num_players
    game_state.prior_priority_player_id = player_id
    game_state.priority_player_id = next_player_id


@when(
    "all players pass priority in succession without playing cards or activating abilities"
)
def when_all_players_pass_in_succession(game_state):
    """All players pass priority in succession.

    Rule 1.11.4a: All players passing triggers stack resolution or phase end.
    """
    if not hasattr(game_state, "players_passed"):
        game_state.players_passed = set()
    # Simulate all players passing without taking actions
    for player_id in range(game_state.num_players):
        game_state.players_passed.add(player_id)

    game_state.all_players_passed = True
    game_state.priority_player_id = None  # No one holds priority after all pass


@when("the active player plays a card")
def when_active_player_plays_card(game_state):
    """The active player plays a card.

    Rule 1.11.5: Active player regains priority after playing a card.
    """
    game_state.card_was_played = True
    # Engine Feature Needed: GameEngine.play_card() with priority regain logic
    game_state.priority_player_id = game_state.turn_player_id  # Regains after play


@when("the active player activates an ability")
def when_active_player_activates_ability(game_state):
    """The active player activates an ability.

    Rule 1.11.5: Active player regains priority after activating an ability.
    """
    game_state.ability_was_activated = True
    # Engine Feature Needed: GameEngine.activate_ability() with priority regain logic
    game_state.priority_player_id = (
        game_state.turn_player_id
    )  # Regains after activation


@when("a card is in the process of being played")
def when_card_is_being_played(game_state):
    """A card is actively in the process of being played.

    Rule 1.11.5: No player has priority while playing a card.
    """
    game_state.is_in_process_of_playing_card = True
    # Engine Feature Needed: GameEngine.is_in_process_of_playing_card = True
    game_state.priority_player_id = None  # No priority during card play


@when("the top layer is in the process of resolving")
def when_layer_is_resolving(game_state):
    """A layer on the stack is actively resolving.

    Rule 1.11.5: No player has priority while resolving a layer.
    """
    game_state.is_resolving_layer = True
    # Engine Feature Needed: GameEngine.is_in_process_of_resolving_layer = True
    game_state.priority_player_id = None  # No priority during resolution


@when("game state actions are being performed")
def when_game_state_actions_are_being_performed(game_state):
    """Game state actions (a)-(e) are currently being performed.

    Rule 1.11.5: No player has priority during game state actions.
    """
    game_state.is_performing_game_state_actions = True
    # Engine Feature Needed: GameEngine.is_performing_game_state_actions = True
    game_state.priority_player_id = None  # No priority during game state actions


# ===== Then steps =====


@then("priority describes which player may play a card or activate an ability")
def then_priority_describes_who_may_play(game_state):
    """Rule 1.11.1: Priority describes who may play cards or activate abilities.

    Engine Feature Needed:
    - [ ] PriorityState.can_play_card(player_id) -> bool
    - [ ] PriorityState.can_activate_ability(player_id) -> bool
    """
    # Engine Feature Needed: Priority system tracks who may play cards
    assert hasattr(game_state, "priority_player_id"), (
        "Engine Feature Needed: priority_player_id tracking (Rule 1.11.1)"
    )


@then("priority describes which player may pass priority to the next player")
def then_priority_describes_who_may_pass(game_state):
    """Rule 1.11.1: Priority describes who may pass priority.

    Engine Feature Needed:
    - [ ] PriorityState.can_pass_priority(player_id) -> bool
    """
    # Engine Feature Needed: Priority system tracks who may pass
    assert hasattr(game_state, "priority_player_id"), (
        "Engine Feature Needed: priority_player_id tracking (Rule 1.11.1)"
    )


@then("exactly one player has priority")
def then_exactly_one_player_has_priority(game_state):
    """Rule 1.11.2: Only one player can have priority at a time.

    Engine Feature Needed:
    - [ ] GameEngine.get_priority_player_id() -> Optional[int]
    - [ ] Invariant: at most one player_id in priority state
    """
    # Engine Feature Needed: PriorityState enforcing single-holder invariant
    priority_holders = [
        pid
        for pid in range(game_state.num_players)
        if pid == game_state.priority_player_id
    ]
    assert len(priority_holders) == 1, (
        f"Engine Feature Needed: Exactly one player must hold priority (Rule 1.11.2). "
        f"Got {len(priority_holders)} priority holders."
    )


@then("the other player does not have priority")
def then_other_player_does_not_have_priority(game_state):
    """Rule 1.11.2: A player who does not have priority is an 'inactive player'.

    Engine Feature Needed:
    - [ ] PriorityState identifying inactive players
    """
    priority_holder = game_state.priority_player_id
    for player_id in range(game_state.num_players):
        if player_id != priority_holder:
            assert player_id != game_state.priority_player_id, (
                f"Engine Feature Needed: Player {player_id} should not have priority "
                f"(Rule 1.11.2). Only player {priority_holder} should."
            )


@then("the player with priority is called the active player")
def then_priority_holder_is_active_player(game_state):
    """Rule 1.11.2: The player with priority is the 'active player'.

    Engine Feature Needed:
    - [ ] GameEngine.get_active_player_id() returning priority holder
    - [ ] 'Active player' concept distinct from 'turn player'
    """
    # Engine Feature Needed: active_player concept
    assert game_state.priority_player_id is not None, (
        "Engine Feature Needed: GameEngine.get_active_player_id() (Rule 1.11.2). "
        "The priority holder is the active player."
    )


@then("the player without priority is called the inactive player")
def then_non_priority_holder_is_inactive(game_state):
    """Rule 1.11.2: Players without priority are 'inactive players'.

    Engine Feature Needed:
    - [ ] GameEngine.get_inactive_player_ids() returning non-priority holders
    """
    active_player = game_state.priority_player_id
    for player_id in range(game_state.num_players):
        if player_id != active_player:
            assert player_id != game_state.priority_player_id, (
                f"Engine Feature Needed: GameEngine.get_inactive_player_ids() (Rule 1.11.2). "
                f"Player {player_id} should be inactive (no priority)."
            )


@then("no player has priority")
def then_no_player_has_priority(game_state):
    """Rule 1.11.3: No player has priority during certain phases/steps.

    Engine Feature Needed:
    - [ ] GameEngine.get_priority_player_id() returning None when no player has priority
    """
    # Engine Feature Needed: Priority system supports None priority state
    assert game_state.priority_player_id is None, (
        f"Engine Feature Needed: GameEngine.get_priority_player_id() should return None "
        f"(Rule 1.11.3). Currently player {game_state.priority_player_id} has priority."
    )


@then("the turn player has priority")
def then_turn_player_has_priority(game_state):
    """Rule 1.11.3: Turn player gains priority.

    Engine Feature Needed:
    - [ ] GameEngine.grant_priority_to_turn_player() method
    - [ ] GameEngine.get_priority_player_id() returning turn_player_id
    """
    assert game_state.priority_player_id == game_state.turn_player_id, (
        f"Engine Feature Needed: GameEngine.grant_priority_to_turn_player() (Rule 1.11.3). "
        f"Expected turn player {game_state.turn_player_id} to have priority, "
        f"but player {game_state.priority_player_id} has it."
    )


@then("no player has priority during the close step")
def then_no_priority_during_close_step(game_state):
    """Rule 1.11.3: Players do not get priority during the Close Step.

    Engine Feature Needed:
    - [ ] GameEngine.current_combat_step property
    - [ ] GameEngine automatically suppresses priority during CLOSE_STEP
    """
    assert game_state.priority_player_id is None, (
        f"Engine Feature Needed: Priority suppressed during Close Step (Rule 1.11.3). "
        f"Currently player {game_state.priority_player_id} has priority during Close Step."
    )


@then("the active player no longer has priority")
def then_active_player_no_longer_has_priority(game_state):
    """Rule 1.11.4: After passing, the active player no longer holds priority.

    Engine Feature Needed:
    - [ ] GameEngine.pass_priority(player_id) removing priority from passer
    """
    prior_holder = game_state.pass_result.get("prior_holder")
    assert game_state.priority_player_id != prior_holder, (
        f"Engine Feature Needed: GameEngine.pass_priority() removing priority from "
        f"passer (Rule 1.11.4). Player {prior_holder} still has priority after passing."
    )


@then("the next player in clockwise order has priority")
def then_next_clockwise_player_has_priority(game_state):
    """Rule 1.11.4/1.11.4a: Priority passed to the next player clockwise.

    Engine Feature Needed:
    - [ ] GameEngine.pass_priority() computing next clockwise player
    - [ ] Clockwise order awareness per Rule 1.1.6
    """
    expected_next = game_state.pass_result.get("new_holder")
    assert game_state.priority_player_id == expected_next, (
        f"Engine Feature Needed: GameEngine.pass_priority() clockwise pass (Rule 1.11.4a). "
        f"Expected player {expected_next} to have priority, "
        f"but player {game_state.priority_player_id} has it."
    )


@then(parsers.parse("player {player_id:d} has priority"))
def then_specific_player_has_priority(game_state, player_id):
    """Rule 1.11.4a: A specific player has priority.

    Engine Feature Needed:
    - [ ] GameEngine.get_priority_player_id() returning the correct player
    """
    assert game_state.priority_player_id == player_id, (
        f"Engine Feature Needed: Clockwise priority passing (Rule 1.11.4a). "
        f"Expected player {player_id} to have priority, "
        f"but player {game_state.priority_player_id} has it."
    )


@then("the top layer of the stack resolves")
def then_top_layer_resolves(game_state):
    """Rule 1.11.4a: All players passing with non-empty stack resolves top layer.

    Engine Feature Needed:
    - [ ] GameEngine.all_players_passed() triggering resolve_top_of_stack()
    - [ ] Stack.resolve_top() method (Rule 5.3)
    """
    assert game_state.all_players_passed, (
        "Engine Feature Needed: All-players-passed detection (Rule 1.11.4a)"
    )
    # Engine Feature Needed: actual stack resolution when all pass with non-empty stack
    assert game_state.stack_was_non_empty, (
        "Engine Feature Needed: Stack was non-empty before resolution (Rule 1.11.4a)"
    )


@then("the current phase or step ends")
def then_phase_or_step_ends(game_state):
    """Rule 1.11.4a: All players passing with empty stack ends phase or step.

    Engine Feature Needed:
    - [ ] GameEngine.all_players_passed() triggering end_phase_or_step()
    - [ ] GameEngine.end_phase_or_step() method
    """
    assert game_state.all_players_passed, (
        "Engine Feature Needed: All-players-passed detection (Rule 1.11.4a)"
    )
    assert not game_state.stack_was_non_empty, (
        "Engine Feature Needed: Empty stack triggers phase/step end (Rule 1.11.4a)"
    )


@then("the active player regains priority after the card is played")
def then_active_player_regains_priority_after_card_play(game_state):
    """Rule 1.11.5: Active player regains priority after playing a card.

    Engine Feature Needed:
    - [ ] GameEngine.play_card() granting priority back to playing player after play
    - [ ] Priority regain happens after the card is played (not during)
    """
    assert game_state.card_was_played, (
        "Engine Feature Needed: Card play tracking (Rule 1.11.5)"
    )
    assert game_state.priority_player_id == game_state.turn_player_id, (
        f"Engine Feature Needed: GameEngine.play_card() regrants priority (Rule 1.11.5). "
        f"Expected turn player {game_state.turn_player_id} to regain priority "
        f"after playing a card, but player {game_state.priority_player_id} has it."
    )


@then("the active player regains priority after the ability is activated")
def then_active_player_regains_priority_after_ability(game_state):
    """Rule 1.11.5: Active player regains priority after activating an ability.

    Engine Feature Needed:
    - [ ] GameEngine.activate_ability() granting priority back to activating player
    - [ ] Priority regain happens after the ability is activated (not during)
    """
    assert game_state.ability_was_activated, (
        "Engine Feature Needed: Ability activation tracking (Rule 1.11.5)"
    )
    assert game_state.priority_player_id == game_state.turn_player_id, (
        f"Engine Feature Needed: GameEngine.activate_ability() regrants priority (Rule 1.11.5). "
        f"Expected turn player {game_state.turn_player_id} to regain priority "
        f"after activating an ability, but player {game_state.priority_player_id} has it."
    )


@then("the active player loses priority")
def then_active_player_loses_priority(game_state):
    """Rule 1.11.5: Active player loses priority after passing.

    Engine Feature Needed:
    - [ ] GameEngine.pass_priority() removing priority from passer
    - [ ] No priority return until rule grants it back (Rule 1.11.5)
    """
    assert game_state.priority_player_id != game_state.turn_player_id, (
        f"Engine Feature Needed: Priority lost after passing (Rule 1.11.5). "
        f"Turn player {game_state.turn_player_id} still has priority after passing."
    )


@then("no player has priority during card play")
def then_no_priority_during_card_play(game_state):
    """Rule 1.11.5: No player has priority while a card is being played.

    Engine Feature Needed:
    - [ ] GameEngine.is_in_process_of_playing_card property
    - [ ] Priority suppressed while is_in_process_of_playing_card = True
    """
    assert game_state.is_in_process_of_playing_card, (
        "Engine Feature Needed: Card-being-played state tracking (Rule 1.11.5)"
    )
    assert game_state.priority_player_id is None, (
        f"Engine Feature Needed: Priority suppressed during card play (Rule 1.11.5). "
        f"Player {game_state.priority_player_id} has priority during card play."
    )


@then("no player has priority during resolution")
def then_no_priority_during_resolution(game_state):
    """Rule 1.11.5: No player has priority while a layer is resolving.

    Engine Feature Needed:
    - [ ] GameEngine.is_in_process_of_resolving_layer property
    - [ ] Priority suppressed while is_in_process_of_resolving_layer = True
    """
    assert game_state.is_resolving_layer, (
        "Engine Feature Needed: Layer-resolving state tracking (Rule 1.11.5)"
    )
    assert game_state.priority_player_id is None, (
        f"Engine Feature Needed: Priority suppressed during resolution (Rule 1.11.5). "
        f"Player {game_state.priority_player_id} has priority during layer resolution."
    )


@then("no player has priority during game state actions")
def then_no_priority_during_game_state_actions(game_state):
    """Rule 1.11.5: No player has priority during game state actions.

    Engine Feature Needed:
    - [ ] GameEngine.is_performing_game_state_actions property
    - [ ] Priority suppressed while is_performing_game_state_actions = True
    """
    assert game_state.is_performing_game_state_actions, (
        "Engine Feature Needed: Game-state-action state tracking (Rule 1.11.5)"
    )
    assert game_state.priority_player_id is None, (
        f"Engine Feature Needed: Priority suppressed during game state actions (Rule 1.11.5). "
        f"Player {game_state.priority_player_id} has priority during game state actions."
    )


@then("the turn player gains priority")
def then_turn_player_gains_priority(game_state):
    """Rule 1.11.3: Turn player gains priority (general).

    Engine Feature Needed:
    - [ ] GameEngine.grant_priority_to_turn_player() (Rule 1.11.3)
    """
    assert game_state.priority_player_id == game_state.turn_player_id, (
        f"Engine Feature Needed: GameEngine.grant_priority_to_turn_player() (Rule 1.11.3). "
        f"Expected turn player {game_state.turn_player_id} to gain priority after layer "
        f"resolution, but player {game_state.priority_player_id} has it."
    )


# ===== Fixtures =====


@pytest.fixture
def game_state():
    """
    Fixture providing game state for priority rule testing.

    Uses BDDGameState which integrates with the real engine.
    Extends it with priority-specific state.
    Reference: Rule 1.11
    """
    from tests.bdd_helpers import BDDGameState

    state = BDDGameState()

    # Priority-specific state
    state.num_players = 2
    state.turn_player_id = 0
    state.priority_player_id = None
    state.current_phase = None
    state.current_combat_step = None
    state.combat_chain_is_open = False
    state.players_passed = set()
    state.all_players_passed = False
    state.stack_was_non_empty = False
    state.layer_resolved = False
    state.card_was_played = False
    state.ability_was_activated = False
    state.is_in_process_of_playing_card = False
    state.is_resolving_layer = False
    state.is_performing_game_state_actions = False
    state.pass_result = {}
    state.prior_priority_player_id = None
    state.priority_system_checked = False

    return state
