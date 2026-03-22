"""
Step definitions for Section 4.4: End Phase
Reference: Flesh and Blood Comprehensive Rules Section 4.4

This module implements behavioral tests for the End Phase of a player's turn.

- Rule 4.4.1: Players do not get priority during the End Phase.
- Rule 4.4.2: The "beginning of the end phase" event occurs; effects that trigger
              at the beginning of the end phase are triggered; stack resolves.
- Rule 4.4.3: The end-of-turn procedure occurs in order:
  - 4.4.3a: All allies' life totals are reset to their base life (modified by counters).
  - 4.4.3b: Turn-player may put a card from hand face-down into an empty arsenal zone.
  - 4.4.3c: Each player puts all pitch zone cards on the bottom of their deck (hidden order).
  - 4.4.3d: Turn-player uptaps all permanents they control.
  - 4.4.3e: All players lose all action points and resource points.
  - 4.4.3f: Turn-player draws cards until hand equals hero's intellect; on first turn all
             other players also draw to intellect.
- Rule 4.4.4: "Until end of turn" and "this turn" effects expire; next clockwise player
               becomes turn-player and begins their Start Phase.

Engine Features Needed for Section 4.4:
- [ ] TurnManager.begin_end_phase() / GameState.begin_end_phase() (Rule 4.4.1, 4.4.2)
- [ ] EndPhaseResult.players_have_priority flag (Rule 4.4.1)
- [ ] EndPhaseResult.beginning_of_end_phase_event_occurred flag (Rule 4.4.2)
- [ ] TurnManager.trigger_beginning_of_end_phase() fires triggered effects (Rule 4.4.2)
- [ ] EndPhaseResult.triggered_layers_added list (Rule 4.4.2)
- [ ] EndPhaseResult.stack_resolved_before_eot_procedure flag (Rule 4.4.2)
- [ ] TurnManager.run_end_of_turn_procedure() (Rule 4.4.3)
- [ ] EndPhaseResult.end_of_turn_procedure_started flag (Rule 4.4.3)
- [ ] TurnManager resolves triggered effects between each eot procedure step (Rule 4.4.3)
- [ ] TurnManager.reset_ally_life_totals() (Rule 4.4.3a)
- [ ] CardInstance.base_life property (Rule 4.4.3a)
- [ ] EndPhaseResult.ally_life_reset flag (Rule 4.4.3a)
- [ ] TurnManager.offer_arsenal_storage() (Rule 4.4.3b)
- [ ] EndPhaseResult.card_stored_in_arsenal flag (Rule 4.4.3b)
- [ ] EndPhaseResult.arsenal_card_is_face_down flag (Rule 4.4.3b)
- [ ] TurnManager.cycle_pitch_zones() (Rule 4.4.3c)
- [ ] EndPhaseResult.pitch_zone_cycled flag (Rule 4.4.3c)
- [ ] EndPhaseResult.pitch_cycle_order_hidden flag (Rule 4.4.3c)
- [ ] TurnManager.untap_turn_player_permanents() (Rule 4.4.3d)
- [ ] EndPhaseResult.permanents_untapped list (Rule 4.4.3d)
- [ ] TurnManager.clear_all_player_points() (Rule 4.4.3e)
- [ ] EndPhaseResult.action_points_cleared flag (Rule 4.4.3e)
- [ ] EndPhaseResult.resource_points_cleared flag (Rule 4.4.3e)
- [ ] TurnManager.draw_to_intellect() (Rule 4.4.3f)
- [ ] EndPhaseResult.turn_player_drew_cards count (Rule 4.4.3f)
- [ ] EndPhaseResult.non_turn_player_drew_cards count (Rule 4.4.3f)
- [ ] GameState.is_first_turn flag (Rule 4.4.3f)
- [ ] TurnManager.end_turn() (Rule 4.4.4)
- [ ] EndPhaseResult.until_end_of_turn_effects_expired flag (Rule 4.4.4)
- [ ] EndPhaseResult.this_turn_effects_expired flag (Rule 4.4.4)
- [ ] EndPhaseResult.new_turn_player_id (Rule 4.4.4)
- [ ] TurnManager.next_clockwise_player() (Rule 4.4.4)
- [ ] EndPhaseResult.next_phase property == "start_phase" (Rule 4.4.4)

Current status: Tests written, Engine pending
"""

import pytest
from pytest_bdd import scenario, given, when, then, parsers


# ===== Scenarios =====


@scenario(
    "../features/section_4_4_end_phase.feature",
    "Players do not get priority during the End Phase",
)
def test_no_priority_during_end_phase():
    """Rule 4.4.1: Players do not get priority during the End Phase."""
    pass


@scenario(
    "../features/section_4_4_end_phase.feature",
    "The beginning of end phase event occurs when End Phase starts",
)
def test_beginning_of_end_phase_event():
    """Rule 4.4.2: The 'beginning of the end phase' event fires when End Phase starts."""
    pass


@scenario(
    "../features/section_4_4_end_phase.feature",
    "Effects that trigger at the beginning of the end phase are triggered",
)
def test_beginning_of_end_phase_triggers():
    """Rule 4.4.2: Effects that trigger at beginning of end phase are triggered."""
    pass


@scenario(
    "../features/section_4_4_end_phase.feature",
    "The stack resolves before the end-of-turn procedure",
)
def test_stack_resolves_before_eot_procedure():
    """Rule 4.4.2: The stack resolves before the end-of-turn procedure begins."""
    pass


@scenario(
    "../features/section_4_4_end_phase.feature",
    "End-of-turn procedure occurs after beginning-of-end-phase triggers resolve",
)
def test_eot_procedure_after_triggers_resolve():
    """Rule 4.4.3: End-of-turn procedure starts after beginning-of-end-phase triggers resolve."""
    pass


@scenario(
    "../features/section_4_4_end_phase.feature",
    "Triggered effects after each end-of-turn step are resolved before next step",
)
def test_triggered_effects_between_eot_steps():
    """Rule 4.4.3: Triggered effects after each step resolve before the next step."""
    pass


@scenario(
    "../features/section_4_4_end_phase.feature",
    "Allies' life totals are reset to their base life at end of turn",
)
def test_ally_life_reset():
    """Rule 4.4.3a: Allies' life totals reset to base life at end of turn."""
    pass


@scenario(
    "../features/section_4_4_end_phase.feature",
    "Allies' life reset is modified by counters on the ally",
)
def test_ally_life_reset_modified_by_counters():
    """Rule 4.4.3a: Ally life reset is modified by counters on the ally."""
    pass


@scenario(
    "../features/section_4_4_end_phase.feature",
    "Non-ally permanents do not have life reset during end of turn",
)
def test_non_ally_permanent_not_reset():
    """Rule 4.4.3a: Non-ally permanents are not affected by ally life reset."""
    pass


@scenario(
    "../features/section_4_4_end_phase.feature",
    "Turn-player may put a card face-down into an empty arsenal zone",
)
def test_arsenal_storage_allowed_when_empty():
    """Rule 4.4.3b: Turn-player may place a card from hand into empty arsenal."""
    pass


@scenario(
    "../features/section_4_4_end_phase.feature",
    "Turn-player cannot put a card into a non-empty arsenal during end of turn",
)
def test_arsenal_storage_blocked_when_not_empty():
    """Rule 4.4.3b: Turn-player cannot place card into non-empty arsenal."""
    pass


@scenario(
    "../features/section_4_4_end_phase.feature",
    "Card placed into arsenal during end of turn is face-down",
)
def test_arsenal_card_placed_face_down():
    """Rule 4.4.3b: Card placed into arsenal during end-of-turn is face-down."""
    pass


@scenario(
    "../features/section_4_4_end_phase.feature",
    "Each player puts pitch zone cards on the bottom of their deck at end of turn",
)
def test_pitch_zone_cycled_to_deck():
    """Rule 4.4.3c: Pitch zone cards move to bottom of deck at end of turn."""
    pass


@scenario(
    "../features/section_4_4_end_phase.feature",
    "Order of pitch zone cards going to bottom of deck is player's choice",
)
def test_pitch_cycle_order_player_choice():
    """Rule 4.4.3c: Player chooses order cards go to bottom of deck."""
    pass


@scenario(
    "../features/section_4_4_end_phase.feature",
    "Order of pitch zone cards placed on bottom of deck is hidden information",
)
def test_pitch_cycle_order_hidden():
    """Rule 4.4.3c: Order of pitch zone cards placed on bottom of deck is hidden."""
    pass


@scenario(
    "../features/section_4_4_end_phase.feature",
    "Non-turn players also move their pitch zone cards to the bottom of their deck",
)
def test_non_turn_player_pitch_cycled():
    """Rule 4.4.3c: Non-turn players also move pitch zone cards to bottom of deck."""
    pass


@scenario(
    "../features/section_4_4_end_phase.feature",
    "Turn-player untaps all permanents they control at end of turn",
)
def test_turn_player_permanents_untapped():
    """Rule 4.4.3d: Turn-player untaps all their permanents."""
    pass


@scenario(
    "../features/section_4_4_end_phase.feature",
    "Only the turn-player's permanents are untapped, not the opponent's",
)
def test_only_turn_player_permanents_untapped():
    """Rule 4.4.3d: Only turn-player's permanents untap, not the opponent's."""
    pass


@scenario(
    "../features/section_4_4_end_phase.feature",
    "All players lose all action points at end of turn",
)
def test_all_action_points_cleared():
    """Rule 4.4.3e: All players lose all action points at end of turn."""
    pass


@scenario(
    "../features/section_4_4_end_phase.feature",
    "All players lose all resource points at end of turn",
)
def test_all_resource_points_cleared():
    """Rule 4.4.3e: All players lose all resource points at end of turn."""
    pass


@scenario(
    "../features/section_4_4_end_phase.feature",
    "Turn-player draws cards up to their hero's intellect at end of turn",
)
def test_turn_player_draws_to_intellect():
    """Rule 4.4.3f: Turn-player draws cards until hand equals hero's intellect."""
    pass


@scenario(
    "../features/section_4_4_end_phase.feature",
    "Turn-player does not draw if hand already has at least intellect cards",
)
def test_turn_player_no_draw_when_at_intellect():
    """Rule 4.4.3f: Turn-player does not draw if hand already at intellect."""
    pass


@scenario(
    "../features/section_4_4_end_phase.feature",
    "Non-turn players draw to intellect only on the first turn of the game",
)
def test_non_turn_player_draws_on_first_turn():
    """Rule 4.4.3f: Non-turn players draw to intellect only on first turn."""
    pass


@scenario(
    "../features/section_4_4_end_phase.feature",
    "Non-turn players do not draw on turns other than the first turn",
)
def test_non_turn_player_no_draw_after_first_turn():
    """Rule 4.4.3f: Non-turn players do not draw on turns after the first."""
    pass


@scenario(
    "../features/section_4_4_end_phase.feature",
    "Effects that last until end of turn expire when the turn ends",
)
def test_until_end_of_turn_effects_expire():
    """Rule 4.4.4: 'Until end of turn' effects expire when the turn ends."""
    pass


@scenario(
    "../features/section_4_4_end_phase.feature",
    'Effects that apply "this turn" expire when the turn ends',
)
def test_this_turn_effects_expire():
    """Rule 4.4.4: 'This turn' effects expire when the turn ends."""
    pass


@scenario(
    "../features/section_4_4_end_phase.feature",
    "The next player in clockwise order becomes the new turn-player",
)
def test_next_clockwise_player_becomes_turn_player():
    """Rule 4.4.4: The next player in clockwise order becomes the new turn-player."""
    pass


@scenario(
    "../features/section_4_4_end_phase.feature",
    "The new turn-player begins their Start Phase after the turn ends",
)
def test_new_turn_player_begins_start_phase():
    """Rule 4.4.4: The new turn-player begins their Start Phase."""
    pass


# ===== Given Steps =====


@given("a game is in progress")
def game_in_progress(game_state):
    """Set up a basic in-progress game state."""
    pass


@given("a game is in progress with multiple players")
def game_in_progress_multiple_players(game_state):
    """Set up a game with multiple players."""
    pass


@given("an effect exists that triggers at the beginning of the end phase")
def effect_triggers_beginning_of_end_phase(game_state):
    """Rule 4.4.2: Create a triggered effect for beginning of end phase."""
    game_state.beginning_of_end_phase_trigger = game_state.create_triggered_layer(
        source=None
    )
    game_state.beginning_of_end_phase_trigger_count = 0


@given("an effect exists that triggers during the end-of-turn procedure")
def effect_triggers_during_eot_procedure(game_state):
    """Rule 4.4.3: Create an effect that triggers during end-of-turn procedure."""
    game_state.eot_procedure_trigger = game_state.create_triggered_layer(source=None)
    game_state.eot_procedure_trigger_fired = False


@given("the turn-player controls an ally with reduced life")
def turn_player_controls_ally_with_reduced_life(game_state):
    """Rule 4.4.3a: Set up an ally with life below base."""
    from fab_engine.cards.model import CardType, Subtype

    ally = game_state.create_card(name="Test Ally", card_type=CardType.PERMANENT)
    ally.base_life = 3
    ally.current_life = 1
    game_state.test_ally = ally
    game_state.player.arena_zone.add_card(ally)


@given("the turn-player controls an ally with +1 counter and reduced life")
def turn_player_controls_ally_with_counter_and_reduced_life(game_state):
    """Rule 4.4.3a: Set up an ally with a +1 counter and reduced life."""
    from fab_engine.cards.model import CardType

    ally = game_state.create_card(name="Test Ally With Counter", card_type=CardType.PERMANENT)
    ally.base_life = 3
    ally.current_life = 1
    ally.plus_one_counters = 1
    game_state.test_ally_with_counter = ally
    game_state.player.arena_zone.add_card(ally)


@given("the turn-player controls a non-ally permanent")
def turn_player_controls_non_ally_permanent(game_state):
    """Rule 4.4.3a: Set up a non-ally permanent (e.g., equipment, item)."""
    from fab_engine.cards.model import CardType

    item = game_state.create_card(name="Test Item", card_type=CardType.PERMANENT)
    game_state.test_non_ally = item
    game_state.player.arena_zone.add_card(item)


@given("the turn-player has a card in hand")
def turn_player_has_card_in_hand(game_state):
    """Set up a card in the turn-player's hand."""
    card = game_state.create_card(name="Test Hand Card")
    game_state.test_hand_card = card
    game_state.player.hand.add_card(card)


@given("the turn-player's arsenal zone is empty")
def turn_player_arsenal_is_empty(game_state):
    """Ensure the turn-player's arsenal zone is empty."""
    game_state.arsenal_is_empty = True


@given("the turn-player's arsenal zone is not empty")
def turn_player_arsenal_is_not_empty(game_state):
    """Set up a card already in the turn-player's arsenal zone."""
    existing_card = game_state.create_card(name="Existing Arsenal Card")
    game_state.player.arsenal_zone.add_card(existing_card)
    game_state.arsenal_is_empty = False


@given("one or more cards are in the turn-player's pitch zone")
def cards_in_turn_player_pitch_zone(game_state):
    """Set up cards in the turn-player's pitch zone."""
    card1 = game_state.create_card(name="Pitched Card 1")
    game_state.player.pitch_zone.add_card(card1)
    game_state.pitched_cards = [card1]


@given("multiple cards are in the turn-player's pitch zone")
def multiple_cards_in_turn_player_pitch_zone(game_state):
    """Set up multiple cards in the turn-player's pitch zone."""
    card1 = game_state.create_card(name="Pitched Card 1")
    card2 = game_state.create_card(name="Pitched Card 2")
    card3 = game_state.create_card(name="Pitched Card 3")
    game_state.player.pitch_zone.add_card(card1)
    game_state.player.pitch_zone.add_card(card2)
    game_state.player.pitch_zone.add_card(card3)
    game_state.pitched_cards = [card1, card2, card3]


@given("one or more cards are in the non-turn-player's pitch zone")
def cards_in_non_turn_player_pitch_zone(game_state):
    """Set up cards in the non-turn-player's pitch zone."""
    card1 = game_state.create_card(name="Opponent Pitched Card 1")
    game_state.opponent.pitch_zone.add_card(card1)
    game_state.opponent_pitched_cards = [card1]


@given("the turn-player controls one or more tapped permanents")
def turn_player_controls_tapped_permanents(game_state):
    """Rule 4.4.3d: Set up tapped permanents for the turn-player."""
    from fab_engine.cards.model import CardType

    perm1 = game_state.create_card(name="Tapped Permanent 1", card_type=CardType.PERMANENT)
    perm2 = game_state.create_card(name="Tapped Permanent 2", card_type=CardType.PERMANENT)
    game_state.player.arena_zone.add_card(perm1)
    game_state.player.arena_zone.add_card(perm2)
    game_state.tap_permanent(perm1)
    game_state.tap_permanent(perm2)
    game_state.tapped_permanents = [perm1, perm2]


@given("the turn-player controls a tapped permanent")
def turn_player_controls_one_tapped_permanent(game_state):
    """Rule 4.4.3d: Set up one tapped permanent for the turn-player."""
    from fab_engine.cards.model import CardType

    perm = game_state.create_card(name="Turn Player Tapped Permanent", card_type=CardType.PERMANENT)
    game_state.player.arena_zone.add_card(perm)
    game_state.tap_permanent(perm)
    game_state.turn_player_tapped_permanent = perm


@given("the non-turn-player controls a tapped permanent")
def non_turn_player_controls_tapped_permanent(game_state):
    """Rule 4.4.3d: Set up a tapped permanent for the non-turn-player."""
    from fab_engine.cards.model import CardType

    perm = game_state.create_card(name="Non-Turn Player Tapped Permanent", card_type=CardType.PERMANENT)
    game_state.opponent.arena_zone.add_card(perm)
    game_state.tap_permanent(perm)
    game_state.opponent_tapped_permanent = perm


@given("one or more players have action points")
def players_have_action_points(game_state):
    """Rule 4.4.3e: Give players action points to clear."""
    game_state.set_player_action_points(game_state.player, 3)
    game_state.set_player_action_points(game_state.opponent, 1)


@given("one or more players have resource points")
def players_have_resource_points(game_state):
    """Rule 4.4.3e: Give players resource points to clear."""
    game_state.player.resources = 4
    game_state.opponent.resources = 2


@given("the turn-player has fewer cards in hand than their hero's intellect")
def turn_player_hand_below_intellect(game_state):
    """Rule 4.4.3f: Turn-player has fewer cards than intellect."""
    game_state.player_intellect = 4
    # Ensure hand has fewer than 4 cards
    while len(game_state.player.hand.cards) >= game_state.player_intellect:
        game_state.player.hand.cards.pop()


@given("the turn-player has cards in hand equal to or more than their hero's intellect")
def turn_player_hand_at_or_above_intellect(game_state):
    """Rule 4.4.3f: Turn-player already has enough cards in hand."""
    game_state.player_intellect = 4
    while len(game_state.player.hand.cards) < game_state.player_intellect:
        card = game_state.create_card(name=f"Hand Card {len(game_state.player.hand.cards)}")
        game_state.player.hand.add_card(card)


@given("it is the first turn of the game")
def it_is_first_turn(game_state):
    """Rule 4.4.3f: Mark game state as first turn."""
    game_state.is_first_turn = True


@given("it is not the first turn of the game")
def it_is_not_first_turn(game_state):
    """Rule 4.4.3f: Mark game state as not first turn."""
    game_state.is_first_turn = False


@given("a non-turn player has fewer cards in hand than their hero's intellect")
def non_turn_player_hand_below_intellect(game_state):
    """Rule 4.4.3f: Non-turn player has fewer cards than intellect."""
    game_state.opponent_intellect = 4
    while len(game_state.opponent.hand.cards) >= game_state.opponent_intellect:
        game_state.opponent.hand.cards.pop()


@given("an effect exists that lasts \"until end of turn\"")
def until_end_of_turn_effect_exists(game_state):
    """Rule 4.4.4: Create an 'until end of turn' effect."""
    game_state.until_eot_effect = {"type": "until_end_of_turn", "active": True}


@given("an effect exists that applies \"this turn\"")
def this_turn_effect_exists(game_state):
    """Rule 4.4.4: Create a 'this turn' effect."""
    game_state.this_turn_effect = {"type": "this_turn", "active": True}


# ===== When Steps =====


@when("the End Phase begins")
def end_phase_begins(game_state):
    """Rule 4.4.1, 4.4.2: Trigger the beginning of the End Phase."""
    game_state.end_phase_result = game_state.begin_end_phase()


@when("a step in the end-of-turn procedure completes")
def eot_procedure_step_completes(game_state):
    """Rule 4.4.3: Simulate a step completing in the end-of-turn procedure."""
    game_state.eot_step_result = game_state.run_end_of_turn_step(
        step="3a",
        check_triggers=True
    )


@when("the end-of-turn procedure step 3a executes")
def eot_step_3a_executes(game_state):
    """Rule 4.4.3a: Run the ally life reset step."""
    game_state.eot_step_3a_result = game_state.run_end_of_turn_step_3a()


@when("the end-of-turn procedure step 3b executes")
def eot_step_3b_executes(game_state):
    """Rule 4.4.3b: Run the arsenal storage step."""
    game_state.eot_step_3b_result = game_state.run_end_of_turn_step_3b()


@when("the turn-player places a card into their arsenal during end-of-turn step 3b")
def turn_player_places_card_in_arsenal(game_state):
    """Rule 4.4.3b: Turn-player exercises the option to store a card."""
    game_state.eot_step_3b_result = game_state.run_end_of_turn_step_3b(
        store_card=game_state.test_hand_card
    )


@when("the end-of-turn procedure step 3c executes")
def eot_step_3c_executes(game_state):
    """Rule 4.4.3c: Run the pitch zone cycling step."""
    game_state.eot_step_3c_result = game_state.run_end_of_turn_step_3c()


@when("the end-of-turn procedure step 3d executes")
def eot_step_3d_executes(game_state):
    """Rule 4.4.3d: Run the untap permanents step."""
    game_state.eot_step_3d_result = game_state.run_end_of_turn_step_3d()


@when("the end-of-turn procedure step 3e executes")
def eot_step_3e_executes(game_state):
    """Rule 4.4.3e: Run the clear points step."""
    game_state.eot_step_3e_result = game_state.run_end_of_turn_step_3e()


@when("the end-of-turn procedure step 3f executes")
def eot_step_3f_executes(game_state):
    """Rule 4.4.3f: Run the draw to intellect step."""
    game_state.eot_step_3f_result = game_state.run_end_of_turn_step_3f()


@when("the turn ends")
def turn_ends(game_state):
    """Rule 4.4.4: Complete the turn and transition to the next player."""
    game_state.end_turn_result = game_state.end_turn()


# ===== Then Steps =====


@then("no player gets priority during the End Phase")
def no_player_gets_priority(game_state):
    """Rule 4.4.1: Verify no player receives priority during End Phase."""
    assert not game_state.end_phase_result.players_have_priority, (
        "Rule 4.4.1: Players should not get priority during the End Phase"
    )


@then("the \"beginning of the end phase\" event occurs")
def beginning_of_end_phase_event_occurred(game_state):
    """Rule 4.4.2: Verify the beginning-of-end-phase event fired."""
    assert game_state.end_phase_result.beginning_of_end_phase_event_occurred, (
        "Rule 4.4.2: The 'beginning of the end phase' event should occur"
    )


@then("the beginning-of-end-phase triggered effect fires")
def beginning_of_end_phase_trigger_fires(game_state):
    """Rule 4.4.2: Verify the triggered effect at beginning of end phase fired."""
    assert len(game_state.end_phase_result.triggered_layers_added) > 0, (
        "Rule 4.4.2: Triggered effects should fire at beginning of end phase"
    )


@then("the triggered effect resolves before the end-of-turn procedure begins")
def triggered_effect_resolves_before_eot_procedure(game_state):
    """Rule 4.4.2: Verify triggered effects resolve before eot procedure."""
    assert game_state.end_phase_result.stack_resolved_before_eot_procedure, (
        "Rule 4.4.2: Stack should resolve before end-of-turn procedure begins"
    )


@then("the end-of-turn procedure occurs after the stack is empty")
def eot_procedure_after_stack_empty(game_state):
    """Rule 4.4.3: Verify end-of-turn procedure starts after stack is empty."""
    assert game_state.end_phase_result.end_of_turn_procedure_started, (
        "Rule 4.4.3: End-of-turn procedure should start after stack is empty"
    )


@then("any triggered layers are added to the stack and resolved before the next step")
def triggered_layers_resolved_between_steps(game_state):
    """Rule 4.4.3: Verify triggered layers resolve between procedure steps."""
    assert game_state.eot_step_result.triggers_resolved_before_next_step, (
        "Rule 4.4.3: Triggered layers should resolve before the next eot step"
    )


@then("the ally's life total is reset to its base life")
def ally_life_reset_to_base(game_state):
    """Rule 4.4.3a: Verify the ally's life total is reset to its base."""
    assert game_state.eot_step_3a_result.ally_life_reset, (
        "Rule 4.4.3a: Ally life total should be reset to base life"
    )
    ally = game_state.test_ally
    assert ally.current_life == ally.base_life, (
        f"Rule 4.4.3a: Ally life should be {ally.base_life}, got {ally.current_life}"
    )


@then("the ally's life total is reset to its base life modified by the counter")
def ally_life_reset_modified_by_counter(game_state):
    """Rule 4.4.3a: Verify ally life reset accounts for counters."""
    ally = game_state.test_ally_with_counter
    expected_life = ally.base_life + ally.plus_one_counters
    assert ally.current_life == expected_life, (
        f"Rule 4.4.3a: Ally life should be {expected_life} (base + counters), got {ally.current_life}"
    )


@then("the non-ally permanent is not affected by the life reset step")
def non_ally_not_affected_by_life_reset(game_state):
    """Rule 4.4.3a: Verify non-ally permanents are unaffected by life reset."""
    assert game_state.eot_step_3a_result.non_ally_affected is False, (
        "Rule 4.4.3a: Non-ally permanents should not be affected by life reset"
    )


@then("the turn-player may put a card from hand face-down into their arsenal")
def turn_player_may_store_in_arsenal(game_state):
    """Rule 4.4.3b: Verify arsenal storage is offered when arsenal is empty."""
    assert game_state.eot_step_3b_result.arsenal_storage_available, (
        "Rule 4.4.3b: Turn-player should be able to store a card in empty arsenal"
    )


@then("the turn-player cannot put a card into their arsenal this way")
def turn_player_cannot_store_in_arsenal(game_state):
    """Rule 4.4.3b: Verify arsenal storage is not available when non-empty."""
    assert not game_state.eot_step_3b_result.arsenal_storage_available, (
        "Rule 4.4.3b: Turn-player should not be able to store a card in non-empty arsenal"
    )


@then("the card in the arsenal is face-down")
def card_in_arsenal_is_face_down(game_state):
    """Rule 4.4.3b: Verify card placed in arsenal is face-down."""
    assert game_state.eot_step_3b_result.arsenal_card_is_face_down, (
        "Rule 4.4.3b: Card placed in arsenal during end of turn should be face-down"
    )


@then("those cards are moved to the bottom of the turn-player's deck")
def pitch_cards_moved_to_deck_bottom(game_state):
    """Rule 4.4.3c: Verify pitch zone cards moved to bottom of deck."""
    assert game_state.eot_step_3c_result.pitch_zone_cycled, (
        "Rule 4.4.3c: Pitch zone cards should move to bottom of deck"
    )
    assert len(game_state.player.pitch_zone.cards) == 0, (
        "Rule 4.4.3c: Pitch zone should be empty after cycling"
    )


@then("the player chooses the order those cards go to the bottom of their deck")
def player_chooses_pitch_cycle_order(game_state):
    """Rule 4.4.3c: Verify player can choose the order pitch cards cycle."""
    assert game_state.eot_step_3c_result.player_chooses_order, (
        "Rule 4.4.3c: Player should choose the order pitch cards go to bottom of deck"
    )


@then("the order in which cards are placed on the bottom of the deck is hidden information")
def pitch_cycle_order_is_hidden(game_state):
    """Rule 4.4.3c: Verify the order is hidden information."""
    assert game_state.eot_step_3c_result.order_is_hidden_information, (
        "Rule 4.4.3c: Order of pitch cycle cards placed on bottom of deck is hidden"
    )


@then("the non-turn player's pitch zone cards move to the bottom of their deck")
def non_turn_player_pitch_cycled(game_state):
    """Rule 4.4.3c: Verify non-turn player's pitch zone also cycles."""
    assert game_state.eot_step_3c_result.non_turn_player_pitch_cycled, (
        "Rule 4.4.3c: Non-turn player's pitch zone should also be cycled"
    )
    assert len(game_state.opponent.pitch_zone.cards) == 0, (
        "Rule 4.4.3c: Non-turn player's pitch zone should be empty after cycling"
    )


@then("all those permanents become untapped")
def all_tapped_permanents_untapped(game_state):
    """Rule 4.4.3d: Verify all turn-player's permanents are now untapped."""
    for perm in game_state.tapped_permanents:
        assert not perm.is_tapped, (
            f"Rule 4.4.3d: Permanent '{perm.name}' should be untapped after end of turn"
        )


@then("the turn-player's permanent becomes untapped")
def turn_player_permanent_untapped(game_state):
    """Rule 4.4.3d: Verify the turn-player's permanent is untapped."""
    assert not game_state.turn_player_tapped_permanent.is_tapped, (
        "Rule 4.4.3d: Turn-player's permanent should be untapped after end of turn"
    )


@then("the non-turn-player's permanent remains tapped")
def non_turn_player_permanent_still_tapped(game_state):
    """Rule 4.4.3d: Verify the opponent's permanent is still tapped."""
    assert game_state.opponent_tapped_permanent.is_tapped, (
        "Rule 4.4.3d: Non-turn-player's permanent should remain tapped"
    )


@then("all players have zero action points")
def all_players_have_zero_action_points(game_state):
    """Rule 4.4.3e: Verify all players have 0 action points."""
    assert game_state.get_player_action_points(game_state.player) == 0, (
        "Rule 4.4.3e: Turn-player should have 0 action points after end of turn"
    )
    assert game_state.get_player_action_points(game_state.opponent) == 0, (
        "Rule 4.4.3e: Non-turn-player should have 0 action points after end of turn"
    )


@then("all players have zero resource points")
def all_players_have_zero_resource_points(game_state):
    """Rule 4.4.3e: Verify all players have 0 resource points."""
    assert game_state.player.resources == 0, (
        "Rule 4.4.3e: Turn-player should have 0 resource points after end of turn"
    )
    assert game_state.opponent.resources == 0, (
        "Rule 4.4.3e: Non-turn-player should have 0 resource points after end of turn"
    )


@then("the turn-player draws cards until their hand size equals their hero's intellect")
def turn_player_drew_to_intellect(game_state):
    """Rule 4.4.3f: Verify turn-player drew cards to reach intellect hand size."""
    assert game_state.eot_step_3f_result.turn_player_drew_cards > 0, (
        "Rule 4.4.3f: Turn-player should draw cards to reach intellect"
    )
    assert len(game_state.player.hand.cards) == game_state.player_intellect, (
        f"Rule 4.4.3f: Turn-player hand should equal intellect ({game_state.player_intellect})"
    )


@then("the turn-player does not draw any cards")
def turn_player_does_not_draw(game_state):
    """Rule 4.4.3f: Verify turn-player draws no cards when hand >= intellect."""
    assert game_state.eot_step_3f_result.turn_player_drew_cards == 0, (
        "Rule 4.4.3f: Turn-player should not draw if hand already at intellect"
    )


@then("the non-turn player draws cards until their hand size equals their hero's intellect")
def non_turn_player_drew_to_intellect(game_state):
    """Rule 4.4.3f: Verify non-turn player drew to intellect on first turn."""
    assert game_state.eot_step_3f_result.non_turn_player_drew_cards > 0, (
        "Rule 4.4.3f: Non-turn player should draw to intellect on first turn"
    )
    assert len(game_state.opponent.hand.cards) == game_state.opponent_intellect, (
        f"Rule 4.4.3f: Non-turn player hand should equal intellect ({game_state.opponent_intellect})"
    )


@then("the non-turn player does not draw any cards")
def non_turn_player_does_not_draw(game_state):
    """Rule 4.4.3f: Verify non-turn player does not draw after first turn."""
    assert game_state.eot_step_3f_result.non_turn_player_drew_cards == 0, (
        "Rule 4.4.3f: Non-turn player should not draw after first turn"
    )


@then("the \"until end of turn\" effect is no longer active")
def until_end_of_turn_effect_expired(game_state):
    """Rule 4.4.4: Verify 'until end of turn' effects are cleared."""
    assert game_state.end_turn_result.until_end_of_turn_effects_expired, (
        "Rule 4.4.4: 'Until end of turn' effects should expire when turn ends"
    )


@then("the \"this turn\" effect is no longer active")
def this_turn_effect_expired(game_state):
    """Rule 4.4.4: Verify 'this turn' effects are cleared."""
    assert game_state.end_turn_result.this_turn_effects_expired, (
        "Rule 4.4.4: 'This turn' effects should expire when turn ends"
    )


@then("the next player in clockwise order becomes the new turn-player")
def next_clockwise_player_becomes_turn_player(game_state):
    """Rule 4.4.4: Verify turn passes to next player in clockwise order."""
    assert game_state.end_turn_result.new_turn_player_id is not None, (
        "Rule 4.4.4: A new turn-player should be designated"
    )
    assert game_state.end_turn_result.turn_passed_clockwise, (
        "Rule 4.4.4: Turn should pass to next player in clockwise order"
    )


@then("the new turn-player begins their Start Phase")
def new_turn_player_begins_start_phase(game_state):
    """Rule 4.4.4: Verify the new turn-player begins their Start Phase."""
    assert game_state.end_turn_result.next_phase == "start_phase", (
        "Rule 4.4.4: New turn-player should begin their Start Phase"
    )


# ===== Fixtures =====


@pytest.fixture
def game_state():
    """
    Fixture providing game state for End Phase testing.

    Uses BDDGameState which integrates with the real engine.
    Reference: Rule 4.4
    """
    from tests.bdd_helpers import BDDGameState

    state = BDDGameState()

    # Set up basic opponent/non-turn player
    from tests.bdd_helpers import TestPlayer
    state.opponent = TestPlayer(player_id=1)
    state.opponent.hand = state.opponent.hand if hasattr(state.opponent, "hand") else type(
        "FakeHand", (), {"cards": [], "add_card": lambda self, c: self.cards.append(c)}
    )()

    # Defaults
    state.is_first_turn = False
    state.player_intellect = 4
    state.opponent_intellect = 4

    return state
