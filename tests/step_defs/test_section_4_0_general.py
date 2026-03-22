"""
Step definitions for Section 4.0: General (Game Structure)
Reference: Flesh and Blood Comprehensive Rules Section 4.0

This module implements behavioral tests for the top-level game structure rules:
- Rule 4.0.1: A game is preceded by start-of-game procedure and ends when a player
              wins or the game is a draw
- Rule 4.0.2: A match consists of one or more consecutive games between the same
              players with the same decks
- Rule 4.0.3: A turn is a game state concept with 3 phases (Start, Action, End)
- Rule 4.0.3b: Only one player can have a turn at a time; turn-player vs non-turn-player
- Rule 4.0.3c: Extra turns are taken immediately after the specified turn

Engine Features Needed for Section 4.0:
- [ ] GameState.is_start_of_game_procedure property (Rule 4.0.1)
- [ ] GameState.game_over / game_result tracking (Rule 4.0.1)
- [ ] GameState.winner / draw state (Rule 4.0.1)
- [ ] Match / GameMatch concept with consecutive games (Rule 4.0.2)
- [ ] GameState.turn_player / current_turn_player tracking (Rule 4.0.3b)
- [ ] GameState.current_phase property (Rule 4.0.3)
- [ ] Phase enum with START_PHASE, ACTION_PHASE, END_PHASE in order (Rule 4.0.3a)
- [ ] GameState.turn_number or similar turn tracking (Rule 4.0.3)
- [ ] Extra turn scheduling: GameState.schedule_extra_turn(player, after_turn) (Rule 4.0.3c)
- [ ] Extra turn resolves immediately after specified turn, before others (Rule 4.0.3c)

Current status: Tests written, Engine pending
"""

import pytest
from pytest_bdd import scenario, given, when, then, parsers


# ===== Scenarios =====


@scenario(
    "../features/section_4_0_general.feature",
    "A game begins with the start-of-game procedure",
)
def test_game_begins_with_start_of_game_procedure():
    """Rule 4.0.1: A game is preceded by the start-of-game procedure."""
    pass


@scenario(
    "../features/section_4_0_general.feature",
    "A game ends when a player wins",
)
def test_game_ends_when_player_wins():
    """Rule 4.0.1: A game ends when a player wins."""
    pass


@scenario(
    "../features/section_4_0_general.feature",
    "A game can end in a draw",
)
def test_game_can_end_in_draw():
    """Rule 4.0.1: A game can end in a draw."""
    pass


@scenario(
    "../features/section_4_0_general.feature",
    "A match consists of one or more consecutive games",
)
def test_match_consists_of_consecutive_games():
    """Rule 4.0.2: A match consists of consecutive games between same players."""
    pass


@scenario(
    "../features/section_4_0_general.feature",
    "A turn is a game state concept that tracks whose turn it is",
)
def test_turn_is_game_state_concept():
    """Rule 4.0.3: A turn is a game state concept."""
    pass


@scenario(
    "../features/section_4_0_general.feature",
    "A turn consists of Start Phase, Action Phase, and End Phase in order",
)
def test_turn_has_three_phases_in_order():
    """Rule 4.0.3a: A turn has exactly 3 phases in order."""
    pass


@scenario(
    "../features/section_4_0_general.feature",
    "Turn phases cannot be skipped or reordered",
)
def test_turn_phases_cannot_be_skipped():
    """Rule 4.0.3a: Phases occur in the correct order."""
    pass


@scenario(
    "../features/section_4_0_general.feature",
    "Only one player can have a turn at any point in time",
)
def test_only_one_turn_player_at_a_time():
    """Rule 4.0.3b: Only one player has a turn at any point."""
    pass


@scenario(
    "../features/section_4_0_general.feature",
    "The turn-player designation alternates between players",
)
def test_turn_player_alternates():
    """Rule 4.0.3b: Turn-player changes between turns."""
    pass


@scenario(
    "../features/section_4_0_general.feature",
    "An extra turn is taken immediately after the specified turn",
)
def test_extra_turn_taken_immediately_after_specified_turn():
    """Rule 4.0.3c: Extra turns are taken immediately after the specified turn."""
    pass


@scenario(
    "../features/section_4_0_general.feature",
    "An extra turn effect specifies which turn it follows",
)
def test_extra_turn_effect_follows_specified_turn():
    """Rule 4.0.3c: Extra turn follows the specified turn."""
    pass


# ===== Step Definitions =====


@given("a new game is being set up")
def new_game_being_set_up(game_state):
    """Rule 4.0.1: Initialize a new game."""
    game_state.setup_new_game()


@when("the game initializes")
def game_initializes(game_state):
    """Rule 4.0.1: Trigger the game initialization."""
    game_state.initialize_game()


@then("the start-of-game procedure precedes normal gameplay")
def start_of_game_procedure_precedes_gameplay(game_state):
    """Rule 4.0.1: Start-of-game procedure should be tracked."""
    assert hasattr(game_state, 'is_start_of_game_procedure') or \
           hasattr(game_state, 'game_phase') or \
           hasattr(game_state, 'start_of_game_complete'), \
        "Engine needs: start-of-game procedure tracking (Rule 4.0.1)"


@then("players do not have a turn during the start-of-game procedure")
def no_turns_during_start_of_game(game_state):
    """Rule 4.0.1: No turns during start-of-game procedure."""
    try:
        is_sog = game_state.is_start_of_game_procedure
        if is_sog:
            assert game_state.current_turn_player is None, \
                "No player should have a turn during start-of-game procedure"
    except AttributeError:
        pytest.fail(
            "Engine needs: GameState.is_start_of_game_procedure and "
            "GameState.current_turn_player (Rule 4.0.1)"
        )


@given("a game is in progress")
def game_in_progress(game_state):
    """Rule 4.0.1: A game is actively being played."""
    game_state.start_game()


@when("a win condition is met for a player")
def win_condition_met(game_state):
    """Rule 4.0.1: Trigger a win condition."""
    game_state.trigger_win_condition(winner_id=0)


@then("the game ends")
def game_ends(game_state):
    """Rule 4.0.1: Game should be marked as over."""
    try:
        assert game_state.game_over is True, \
            "Game should be over after win condition met"
    except AttributeError:
        pytest.fail("Engine needs: GameState.game_over property (Rule 4.0.1)")


@then("the winning player is recorded")
def winning_player_recorded(game_state):
    """Rule 4.0.1: The winner should be stored in game state."""
    try:
        assert game_state.winner is not None, \
            "Winning player should be recorded"
        assert game_state.winner == 0, \
            "Winner should be player 0"
    except AttributeError:
        pytest.fail("Engine needs: GameState.winner property (Rule 4.0.1)")


@when("a draw condition is met")
def draw_condition_met(game_state):
    """Rule 4.0.1: Trigger a draw condition."""
    game_state.trigger_draw_condition()


@then("the game ends as a draw")
def game_ends_as_draw(game_state):
    """Rule 4.0.1: Game should be marked as a draw."""
    try:
        assert game_state.game_over is True, \
            "Game should be over after draw condition met"
        assert game_state.is_draw is True, \
            "Game should be marked as a draw"
    except AttributeError:
        pytest.fail(
            "Engine needs: GameState.game_over and GameState.is_draw (Rule 4.0.1)"
        )


@then("no player is recorded as the winner")
def no_player_recorded_as_winner(game_state):
    """Rule 4.0.1: No winner in a draw."""
    try:
        assert game_state.winner is None, \
            "No player should be the winner in a draw"
    except AttributeError:
        pytest.fail("Engine needs: GameState.winner property (Rule 4.0.1)")


@given("a match between two players is initialized")
def match_initialized(game_state):
    """Rule 4.0.2: Initialize a match between two players."""
    game_state.initialize_match(player_count=2)


@when("the first game of the match concludes")
def first_game_concludes(game_state):
    """Rule 4.0.2: End the first game."""
    game_state.conclude_game(game_number=1)


@then("the match may continue with another game between the same players")
def match_continues_with_same_players(game_state):
    """Rule 4.0.2: The match can have consecutive games."""
    try:
        assert game_state.match is not None, \
            "A match object should exist"
        assert game_state.match.games_played >= 1, \
            "Match should track games played"
        assert game_state.match.can_continue, \
            "Match should be able to continue"
    except AttributeError:
        pytest.fail(
            "Engine needs: Match object with games_played and can_continue (Rule 4.0.2)"
        )


@then("the same decks are used in consecutive games of the match")
def same_decks_used(game_state):
    """Rule 4.0.2: Same decks are used throughout a match."""
    try:
        assert game_state.match.player_decks_locked is True, \
            "Decks should be locked for the duration of a match"
    except AttributeError:
        pytest.fail(
            "Engine needs: Match.player_decks_locked property (Rule 4.0.2)"
        )


@when("checking the game state for turn information")
def checking_turn_info(game_state):
    """Rule 4.0.3: Access turn information from game state."""
    game_state.access_turn_info()


@then("the game state tracks which player's turn it is")
def game_state_tracks_turn_player(game_state):
    """Rule 4.0.3b: Game state has turn player tracking."""
    try:
        _ = game_state.current_turn_player
    except AttributeError:
        pytest.fail(
            "Engine needs: GameState.current_turn_player (Rule 4.0.3b)"
        )


@then("the game state tracks the current phase")
def game_state_tracks_current_phase(game_state):
    """Rule 4.0.3: Game state tracks the current phase."""
    try:
        _ = game_state.current_phase
    except AttributeError:
        pytest.fail(
            "Engine needs: GameState.current_phase (Rule 4.0.3)"
        )


@given("a game is in progress with a current turn")
def game_in_progress_with_turn(game_state):
    """Rule 4.0.3: A game is in progress with an active turn."""
    game_state.start_game()
    game_state.begin_turn(player_id=0)


@when("the turn's phases are enumerated")
def enumerate_turn_phases(game_state):
    """Rule 4.0.3a: List all phases of a turn."""
    game_state.enumerate_phases()


@then("the first phase is the Start Phase")
def first_phase_is_start(game_state):
    """Rule 4.0.3a: Start Phase is first."""
    try:
        phases = game_state.turn_phases
        assert len(phases) >= 1, "Turn should have at least one phase"
        assert str(phases[0]).upper() in ("START_PHASE", "START", "STARTPHASE"), \
            f"First phase should be Start Phase, got: {phases[0]}"
    except AttributeError:
        pytest.fail(
            "Engine needs: GameState.turn_phases list (Rule 4.0.3a)"
        )


@then("the second phase is the Action Phase")
def second_phase_is_action(game_state):
    """Rule 4.0.3a: Action Phase is second."""
    try:
        phases = game_state.turn_phases
        assert len(phases) >= 2, "Turn should have at least two phases"
        assert str(phases[1]).upper() in ("ACTION_PHASE", "ACTION", "ACTIONPHASE"), \
            f"Second phase should be Action Phase, got: {phases[1]}"
    except AttributeError:
        pytest.fail(
            "Engine needs: GameState.turn_phases list (Rule 4.0.3a)"
        )


@then("the third phase is the End Phase")
def third_phase_is_end(game_state):
    """Rule 4.0.3a: End Phase is third."""
    try:
        phases = game_state.turn_phases
        assert len(phases) >= 3, "Turn should have at least three phases"
        assert str(phases[2]).upper() in ("END_PHASE", "END", "ENDPHASE"), \
            f"Third phase should be End Phase, got: {phases[2]}"
    except AttributeError:
        pytest.fail(
            "Engine needs: GameState.turn_phases list (Rule 4.0.3a)"
        )


@then("there are exactly 3 phases in a turn")
def exactly_three_phases(game_state):
    """Rule 4.0.3a: A turn has exactly 3 phases."""
    try:
        phases = game_state.turn_phases
        assert len(phases) == 3, \
            f"A turn must have exactly 3 phases, got: {len(phases)}"
    except AttributeError:
        pytest.fail(
            "Engine needs: GameState.turn_phases list (Rule 4.0.3a)"
        )


@when("the Action Phase is active")
def action_phase_is_active(game_state):
    """Rule 4.0.3a: Set the game to be in Action Phase."""
    game_state.advance_to_phase("ACTION_PHASE")


@then("the Start Phase has already occurred")
def start_phase_has_occurred(game_state):
    """Rule 4.0.3a: Start Phase precedes Action Phase."""
    try:
        completed_phases = game_state.completed_phases_this_turn
        start_phase_names = {"START_PHASE", "START", "STARTPHASE"}
        start_completed = any(
            str(p).upper() in start_phase_names for p in completed_phases
        )
        assert start_completed, \
            "Start Phase should have already occurred when Action Phase is active"
    except AttributeError:
        pytest.fail(
            "Engine needs: GameState.completed_phases_this_turn (Rule 4.0.3a)"
        )


@then("the End Phase has not yet occurred")
def end_phase_has_not_occurred(game_state):
    """Rule 4.0.3a: End Phase follows Action Phase."""
    try:
        completed_phases = game_state.completed_phases_this_turn
        end_phase_names = {"END_PHASE", "END", "ENDPHASE"}
        end_completed = any(
            str(p).upper() in end_phase_names for p in completed_phases
        )
        assert not end_completed, \
            "End Phase should not have occurred yet when Action Phase is active"
    except AttributeError:
        pytest.fail(
            "Engine needs: GameState.completed_phases_this_turn (Rule 4.0.3a)"
        )


@given("a game is in progress with two players")
def game_in_progress_two_players(game_state):
    """Rule 4.0.3b: A game with two players."""
    game_state.start_game_with_players(player_count=2)


@when("it is player one's turn")
def player_one_turn(game_state):
    """Rule 4.0.3b: Set player one as the turn-player."""
    game_state.set_turn_player(player_id=0)


@then("player one is the turn-player")
def player_one_is_turn_player(game_state):
    """Rule 4.0.3b: Player one should be the turn-player."""
    try:
        assert game_state.current_turn_player == 0, \
            "Player one (id=0) should be the turn-player"
    except AttributeError:
        pytest.fail(
            "Engine needs: GameState.current_turn_player (Rule 4.0.3b)"
        )


@then("player two is a non-turn-player")
def player_two_is_non_turn_player(game_state):
    """Rule 4.0.3b: Player two should NOT be the turn-player."""
    try:
        assert game_state.current_turn_player != 1, \
            "Player two (id=1) should not be the turn-player"
        non_turn_players = game_state.non_turn_players
        assert 1 in non_turn_players, \
            "Player two should be in the non-turn-players list"
    except AttributeError:
        pytest.fail(
            "Engine needs: GameState.non_turn_players (Rule 4.0.3b)"
        )


@then("exactly one player is the turn-player")
def exactly_one_turn_player(game_state):
    """Rule 4.0.3b: Only one player is the turn-player."""
    try:
        all_players = game_state.all_players
        turn_players = [p for p in all_players if p == game_state.current_turn_player]
        assert len(turn_players) == 1, \
            f"Exactly one player must be the turn-player, got: {len(turn_players)}"
    except AttributeError:
        pytest.fail(
            "Engine needs: GameState.all_players and GameState.current_turn_player (Rule 4.0.3b)"
        )


@when("player one's turn ends")
def player_one_turn_ends(game_state):
    """Rule 4.0.3b: End player one's turn."""
    game_state.end_turn(player_id=0)


@then("player two becomes the turn-player")
def player_two_becomes_turn_player(game_state):
    """Rule 4.0.3b: After player one's turn, player two becomes turn-player."""
    try:
        assert game_state.current_turn_player == 1, \
            "Player two (id=1) should become the turn-player after player one's turn"
    except AttributeError:
        pytest.fail(
            "Engine needs: GameState.current_turn_player (Rule 4.0.3b)"
        )


@then("player one becomes a non-turn-player")
def player_one_becomes_non_turn_player(game_state):
    """Rule 4.0.3b: After their turn ends, player one is a non-turn-player."""
    try:
        non_turn_players = game_state.non_turn_players
        assert 0 in non_turn_players, \
            "Player one (id=0) should become a non-turn-player after their turn ends"
    except AttributeError:
        pytest.fail(
            "Engine needs: GameState.non_turn_players (Rule 4.0.3b)"
        )


@given("a game is in progress with player one as the turn-player")
def game_in_progress_player_one_turn(game_state):
    """Rule 4.0.3c: A game is in progress with player one as the turn-player."""
    game_state.start_game_with_players(player_count=2)
    game_state.set_turn_player(player_id=0)


@when("an effect grants player one an extra turn after the current turn")
def effect_grants_extra_turn(game_state):
    """Rule 4.0.3c: An effect grants an extra turn."""
    game_state.schedule_extra_turn(player_id=0, after_current_turn=True)


@then("player one will take an extra turn immediately after their current turn")
def extra_turn_immediately_after_current(game_state):
    """Rule 4.0.3c: Extra turn is scheduled right after the current turn."""
    try:
        scheduled = game_state.scheduled_extra_turns
        assert len(scheduled) >= 1, \
            "At least one extra turn should be scheduled"
        first_extra = scheduled[0]
        assert first_extra['player_id'] == 0, \
            "Player one should have the extra turn"
        assert first_extra['after_turn'] == game_state.current_turn_number, \
            "Extra turn should be after the current turn number"
    except AttributeError:
        pytest.fail(
            "Engine needs: GameState.scheduled_extra_turns and "
            "GameState.current_turn_number (Rule 4.0.3c)"
        )


@then("the extra turn occurs before any other player's next turn")
def extra_turn_before_others(game_state):
    """Rule 4.0.3c: Extra turn precedes the normal turn order."""
    try:
        turn_order = game_state.upcoming_turn_order
        if len(turn_order) >= 2:
            # The next turn should be the extra turn for player 0
            assert turn_order[0]['player_id'] == 0, \
                "Player one's extra turn should come first in upcoming turn order"
    except AttributeError:
        pytest.fail(
            "Engine needs: GameState.upcoming_turn_order (Rule 4.0.3c)"
        )


@when("an effect grants player two an extra turn after player one's current turn")
def effect_grants_player_two_extra_turn(game_state):
    """Rule 4.0.3c: An effect grants player two an extra turn after player one's turn."""
    game_state.schedule_extra_turn(
        player_id=1,
        after_turn=game_state.current_turn_number
    )


@then("player two's extra turn is taken immediately after player one's current turn")
def player_two_extra_turn_after_player_one(game_state):
    """Rule 4.0.3c: Player two's extra turn follows player one's current turn."""
    try:
        scheduled = game_state.scheduled_extra_turns
        assert len(scheduled) >= 1, \
            "At least one extra turn should be scheduled"
        extra = next(
            (t for t in scheduled if t['player_id'] == 1), None
        )
        assert extra is not None, \
            "Player two should have an extra turn scheduled"
        assert extra['after_turn'] == game_state.current_turn_number, \
            "Extra turn should follow the current turn number"
    except AttributeError:
        pytest.fail(
            "Engine needs: GameState.scheduled_extra_turns (Rule 4.0.3c)"
        )


@then("the normal turn order resumes after the extra turn")
def normal_turn_order_resumes(game_state):
    """Rule 4.0.3c: Normal turn order resumes after the extra turn."""
    try:
        turn_order = game_state.upcoming_turn_order
        # After extra turn(s), regular turn order should resume
        assert game_state.normal_turn_order_preserved is True, \
            "Normal turn order should be preserved after extra turns resolve"
    except AttributeError:
        pytest.fail(
            "Engine needs: GameState.upcoming_turn_order and "
            "GameState.normal_turn_order_preserved (Rule 4.0.3c)"
        )


# ===== Fixtures =====


@pytest.fixture
def game_state():
    """
    Fixture providing game state for testing Section 4.0.

    Uses BDDGameState which integrates with the real engine.
    Reference: Rule 4.0 - Game Structure General
    """
    from tests.bdd_helpers import BDDGameState

    state = BDDGameState()

    # Initialize with two players for turn-order tests
    state.player_count = 2
    state.current_turn_player = None
    state.game_over = False
    state.is_draw = False
    state.winner = None

    return state
