"""
Step definitions for Section 4.5: Ending a Game
Reference: Flesh and Blood Comprehensive Rules Section 4.5

This module implements behavioral tests for game-ending conditions in Flesh and Blood.

Engine Features Needed for Section 4.5:
- [ ] GameState.check_end_conditions() method (Rule 4.5.1)
- [ ] GameEndResult class with fields: is_over, winner_id, is_draw, reason (Rule 4.5.1)
- [ ] GameState.game_ended flag (Rule 4.5.1)
- [ ] GameState.game_result property (Rule 4.5.1)
- [ ] Player.has_lost flag / GameState.eliminate_player(player_id) (Rule 4.5.1a)
- [ ] GameState.clear_player_controlled_objects(player_id) (Rule 4.5.1a)
- [ ] GameState.remove_player_owned_objects(player_id) (Rule 4.5.1a)
- [ ] Player.is_eliminated flag (Rule 4.5.1a)
- [ ] LayerContinuousEffect.persists_after_controller_loss flag (Rule 4.5.1a)
- [ ] GameState.win_condition_player_id / declare_winner(player_id) (Rule 4.5.2a, 4.5.2b)
- [ ] GameState.all_opponents_lost(player_id) check (Rule 4.5.2a)
- [ ] EffectType.WIN_GAME effect (Rule 4.5.2b)
- [ ] Player.hero.life_total property (Rule 4.5.3a)
- [ ] GameState.check_hero_life_loss() (Rule 4.5.3a)
- [ ] Player.controls_hero flag (Rule 4.5.3a)
- [ ] EffectType.LOSE_GAME effect (Rule 4.5.3b)
- [ ] GameState.player_concede(player_id) (Rule 4.5.3c)
- [ ] GameState.check_simultaneous_life_loss() (Rule 4.5.4a)
- [ ] GameEndResult.is_draw = True and reason = "simultaneous_life_loss" (Rule 4.5.4a)
- [ ] EffectType.GAME_DRAW effect (Rule 4.5.4b)
- [ ] GameState.declare_intentional_draw(player_ids) (Rule 4.5.4c)
- [ ] GameState.check_stalemate() (Rule 4.5.4d)
- [ ] GameState.check_deadlock() (Rule 4.5.4e)

Current status: Tests written, Engine pending
"""

import pytest
from pytest_bdd import scenario, given, when, then, parsers


# ===== Scenarios =====


@scenario(
    "../features/section_4_5_ending_a_game.feature",
    "Game ends immediately when a player wins",
)
def test_game_ends_immediately_on_win():
    """Rule 4.5.1: A game ends immediately when a player wins."""
    pass


@scenario(
    "../features/section_4_5_ending_a_game.feature",
    "Game ends immediately when the game is a draw",
)
def test_game_ends_immediately_on_draw():
    """Rule 4.5.1: A game ends immediately when the game is a draw."""
    pass


@scenario(
    "../features/section_4_5_ending_a_game.feature",
    "Losing player's controlled objects are cleared when they lose in multiplayer",
)
def test_losing_player_controlled_objects_cleared():
    """Rule 4.5.1a: Losing player's controlled objects are cleared first."""
    pass


@scenario(
    "../features/section_4_5_ending_a_game.feature",
    "Losing player's owned objects are removed from the game",
)
def test_losing_player_owned_objects_removed():
    """Rule 4.5.1a: All objects owned by the losing player are removed from game."""
    pass


@scenario(
    "../features/section_4_5_ending_a_game.feature",
    "Layer-continuous effects controlled by losing player persist until expiry",
)
def test_layer_continuous_effects_persist_after_player_loss():
    """Rule 4.5.1a: Layer-continuous effects continue to exist until they expire."""
    pass


@scenario(
    "../features/section_4_5_ending_a_game.feature",
    "Player and hero cease to exist after losing in multiplayer",
)
def test_player_and_hero_cease_to_exist_on_loss():
    """Rule 4.5.1a: Player and their hero cease to exist for the rest of the game."""
    pass


@scenario(
    "../features/section_4_5_ending_a_game.feature",
    "Player wins when all opponents have lost",
)
def test_player_wins_when_all_opponents_lost():
    """Rule 4.5.2a: A player wins when all opponents have lost."""
    pass


@scenario(
    "../features/section_4_5_ending_a_game.feature",
    "Player wins when last opponent loses in multiplayer",
)
def test_player_wins_when_last_opponent_eliminated():
    """Rule 4.5.2a: In multiplayer, player wins when last remaining opponent loses."""
    pass


@scenario(
    "../features/section_4_5_ending_a_game.feature",
    "Player wins when an effect states they win",
)
def test_player_wins_by_effect():
    """Rule 4.5.2b: A player wins when an effect states they win the game."""
    pass


@scenario(
    "../features/section_4_5_ending_a_game.feature",
    "Player loses when hero life total is reduced to zero",
)
def test_player_loses_when_hero_life_reaches_zero():
    """Rule 4.5.3a: A player loses when their hero's life total is reduced to zero."""
    pass


@scenario(
    "../features/section_4_5_ending_a_game.feature",
    "Player loses when they do not control a hero",
)
def test_player_loses_when_no_hero_controlled():
    """Rule 4.5.3a: A player loses when they do not control a hero."""
    pass


@scenario(
    "../features/section_4_5_ending_a_game.feature",
    "Player loses when an effect states they lose",
)
def test_player_loses_by_effect():
    """Rule 4.5.3b: A player loses when an effect states they lose the game."""
    pass


@scenario(
    "../features/section_4_5_ending_a_game.feature",
    "Player loses when they concede",
)
def test_player_loses_by_conceding():
    """Rule 4.5.3c: A player loses when they concede."""
    pass


@scenario(
    "../features/section_4_5_ending_a_game.feature",
    "Player can concede at any time",
)
def test_player_can_concede_at_any_time():
    """Rule 4.5.3c: A player can concede at any time, including on their opponent's turn."""
    pass


@scenario(
    "../features/section_4_5_ending_a_game.feature",
    "Game is a draw when all remaining players' heroes simultaneously reach zero life",
)
def test_draw_by_simultaneous_life_loss():
    """Rule 4.5.4a: Simultaneous life loss to zero results in a draw."""
    pass


@scenario(
    "../features/section_4_5_ending_a_game.feature",
    "Game is not a draw if life totals reach zero at different times",
)
def test_no_draw_when_life_loss_not_simultaneous():
    """Rule 4.5.4a: Sequential life loss does not result in a draw."""
    pass


@scenario(
    "../features/section_4_5_ending_a_game.feature",
    "Game is a draw when an effect states the game is a draw",
)
def test_draw_by_effect():
    """Rule 4.5.4b: The game is a draw when an effect states so."""
    pass


@scenario(
    "../features/section_4_5_ending_a_game.feature",
    "Game is a draw when all remaining players agree to intentional draw",
)
def test_draw_by_intentional_agreement():
    """Rule 4.5.4c: All remaining players can agree to an intentional draw."""
    pass


@scenario(
    "../features/section_4_5_ending_a_game.feature",
    "Players can agree to intentional draw at any time",
)
def test_intentional_draw_can_occur_at_any_time():
    """Rule 4.5.4c: Remaining players can agree to a draw at any time."""
    pass


@scenario(
    "../features/section_4_5_ending_a_game.feature",
    "Game is a draw due to stalemate when no player can advance the game",
)
def test_draw_by_stalemate():
    """Rule 4.5.4d: Stalemate occurs when no remaining player can advance the game state."""
    pass


@scenario(
    "../features/section_4_5_ending_a_game.feature",
    "Game is a draw due to deadlock when all players refuse to advance the game",
)
def test_draw_by_deadlock():
    """Rule 4.5.4e: Deadlock occurs when all remaining players refuse to advance game state."""
    pass


# ===== Step Definitions =====


@given("a game with two players")
def a_game_with_two_players(game_state):
    """Set up a standard two-player game."""
    game_state.player_count = 2
    game_state.active_player_ids = [0, 1]


@given("a game with three players")
def a_game_with_three_players(game_state):
    """Set up a three-player game."""
    game_state.player_count = 3
    game_state.active_player_ids = [0, 1, 2]


@given("player one's hero has 0 life")
def player_one_hero_has_zero_life(game_state):
    """Rule 4.5.3a: Player one's hero life is at 0."""
    game_state.player_one_hero_life = 0


@given("both heroes are simultaneously reduced to 0 life")
def both_heroes_simultaneously_at_zero(game_state):
    """Rule 4.5.4a: Both heroes lose their remaining life at the same time."""
    game_state.simultaneous_life_loss = True
    game_state.player_one_hero_life = 0
    game_state.player_two_hero_life = 0


@given("player one controls an attack action card on the combat chain")
def player_one_controls_attack_on_chain(game_state):
    """Rule 4.5.1a: Player one has an attack on the combat chain."""
    card = game_state.create_card(name="Test Attack", card_type="attack_action")
    game_state.player_one_combat_chain_card = card
    game_state.player_one_controlled_on_chain = card


@given("player one controls a triggered layer on the stack")
def player_one_controls_triggered_layer(game_state):
    """Rule 4.5.1a: Player one has a triggered layer on the stack."""
    layer = game_state.create_triggered_layer()
    game_state.player_one_triggered_layer = layer


@given("player two controls a token owned by player one")
def player_two_controls_token_owned_by_player_one(game_state):
    """Rule 4.5.1a: An opponent controls a token owned by the losing player."""
    token = game_state.create_token_card(name="Frostbite")
    game_state.token_owned_by_player_one = token
    game_state.token_controlled_by_player_two = token


@given("player two controls a deck card owned by player one")
def player_two_controls_deck_card_owned_by_player_one(game_state):
    """Rule 4.5.1a: An opponent controls a deck card owned by the losing player."""
    card = game_state.create_card(name="Frost Hex")
    game_state.deck_card_owned_by_player_one = card
    game_state.deck_card_controlled_by_player_two = card


@given("player one has a layer-continuous effect active on the stack")
def player_one_has_layer_continuous_effect(game_state):
    """Rule 4.5.1a: Player one controls a layer-continuous effect."""
    game_state.player_one_layer_continuous_effect = {"controller": 0, "active": True}


@given("player one has a hero in the hero zone")
def player_one_has_hero(game_state):
    """Rule 4.5.1a: Player one's hero exists in the hero zone."""
    game_state.player_one_has_hero = True


@given("player two's hero has 0 life")
def player_two_hero_has_zero_life(game_state):
    """Rule 4.5.3a: Player two's hero life is at 0."""
    game_state.player_two_hero_life = 0


@given("player two has already lost the game")
def player_two_has_already_lost(game_state):
    """Rule 4.5.2a: Player two was previously eliminated."""
    game_state.player_two_eliminated = True
    if 1 in game_state.active_player_ids:
        game_state.active_player_ids.remove(1)


@given("player three's hero has 0 life")
def player_three_hero_has_zero_life(game_state):
    """Rule 4.5.2a: Player three's hero life is at 0."""
    game_state.player_three_hero_life = 0


@given("an effect states that player one wins the game")
def effect_says_player_one_wins(game_state):
    """Rule 4.5.2b: A win-game effect targeting player one is set up."""
    game_state.pending_win_effect = {"player_id": 0, "type": "win_game"}


@given("player one's hero has a life total of 20")
def player_one_hero_has_twenty_life(game_state):
    """Rule 4.5.3a: Player one's hero starts at 20 life."""
    game_state.player_one_hero_life = 20


@given("player one does not control a hero")
def player_one_has_no_hero(game_state):
    """Rule 4.5.3a: Player one has no hero under their control."""
    game_state.player_one_controls_hero = False


@given("an effect states that player one loses the game")
def effect_says_player_one_loses(game_state):
    """Rule 4.5.3b: A lose-game effect targeting player one is set up."""
    game_state.pending_lose_effect = {"player_id": 0, "type": "lose_game"}


@given("it is currently player two's turn")
def it_is_player_two_turn(game_state):
    """Set up the game state so it is player two's turn."""
    game_state.current_turn_player_id = 1


@given("both heroes have 1 life remaining")
def both_heroes_have_one_life(game_state):
    """Rule 4.5.4a: Both heroes are at 1 life."""
    game_state.player_one_hero_life = 1
    game_state.player_two_hero_life = 1


@given("player one's hero has 1 life")
def player_one_hero_has_one_life(game_state):
    """Rule 4.5.4a: Player one's hero is at 1 life."""
    game_state.player_one_hero_life = 1


@given("player two's hero has 2 life")
def player_two_hero_has_two_life(game_state):
    """Rule 4.5.4a: Player two's hero is at 2 life."""
    game_state.player_two_hero_life = 2


@given("an effect states that the game is a draw")
def effect_says_game_is_draw(game_state):
    """Rule 4.5.4b: A draw-game effect is set up."""
    game_state.pending_draw_effect = {"type": "game_draw"}


@given("it is currently the middle of the action phase")
def it_is_middle_of_action_phase(game_state):
    """Set up the game state in the middle of the action phase."""
    game_state.current_phase = "action_phase"


@given("both players only have a Cracked Bauble in their hand")
def both_players_have_only_cracked_bauble(game_state):
    """Rule 4.5.4d: Both players have only a Cracked Bauble (non-damaging card)."""
    game_state.player_one_hand = ["Cracked Bauble"]
    game_state.player_two_hand = ["Cracked Bauble"]


@given("both players have no cards in deck, arsenal, or banished zone")
def both_players_have_no_deck_arsenal_banished(game_state):
    """Rule 4.5.4d: No cards in deck, arsenal, or banished zone."""
    game_state.player_one_deck_empty = True
    game_state.player_two_deck_empty = True
    game_state.player_one_arsenal_empty = True
    game_state.player_two_arsenal_empty = True
    game_state.player_one_banished_empty = True
    game_state.player_two_banished_empty = True


@given("both players control a weapon without an attack ability")
def both_players_control_weapon_without_attack(game_state):
    """Rule 4.5.4d: Both players have weapons that cannot reduce life totals."""
    game_state.player_one_weapon = {"name": "Test Weapon", "has_attack_ability": False}
    game_state.player_two_weapon = {"name": "Test Weapon", "has_attack_ability": False}


@given("a game with two players on 1 life each")
def game_with_two_players_on_one_life(game_state):
    """Rule 4.5.4e: Both players are at 1 life."""
    game_state.player_count = 2
    game_state.active_player_ids = [0, 1]
    game_state.player_one_hero_life = 1
    game_state.player_two_hero_life = 1


@given("both players only have Invert Existence and a Cracked Bauble in their hand")
def both_players_have_invert_existence_and_bauble(game_state):
    """Rule 4.5.4e: Both players hold Invert Existence and a Cracked Bauble."""
    game_state.player_one_hand = ["Invert Existence", "Cracked Bauble"]
    game_state.player_two_hand = ["Invert Existence", "Cracked Bauble"]


@given("both players have no equipment, weapon, or cards in deck, arsenal, or banished zone")
def both_players_have_no_resources(game_state):
    """Rule 4.5.4e: No equipment, weapons, or other resources available."""
    game_state.player_one_has_equipment = False
    game_state.player_two_has_equipment = False
    game_state.player_one_has_weapon = False
    game_state.player_two_has_weapon = False
    game_state.player_one_deck_empty = True
    game_state.player_two_deck_empty = True


# ===== When steps =====


@when("the game checks end conditions")
def game_checks_end_conditions(game_state):
    """Trigger end condition check."""
    game_state.end_condition_result = game_state.check_end_conditions()


@when("player one loses the game")
def player_one_loses(game_state):
    """Rule 4.5.3: Trigger player one losing the game."""
    game_state.elimination_result = game_state.eliminate_player(player_id=0)


@when("the game has not ended because opponents remain")
def game_continues_with_remaining_opponents(game_state):
    """Rule 4.5.1a: In multiplayer, other players still exist so game continues."""
    game_state.game_still_ongoing = len(game_state.active_player_ids) > 1


@when("player two loses the game")
def player_two_loses(game_state):
    """Rule 4.5.3: Trigger player two losing the game."""
    game_state.elimination_result = game_state.eliminate_player(player_id=1)


@when("player three loses the game")
def player_three_loses(game_state):
    """Rule 4.5.2a: Trigger player three losing the game."""
    game_state.elimination_result = game_state.eliminate_player(player_id=2)


@when("the effect resolves")
def the_effect_resolves(game_state):
    """Resolve the pending win/lose/draw effect."""
    if hasattr(game_state, "pending_win_effect"):
        game_state.effect_resolution_result = game_state.resolve_win_effect(
            game_state.pending_win_effect
        )
    elif hasattr(game_state, "pending_lose_effect"):
        game_state.effect_resolution_result = game_state.resolve_lose_effect(
            game_state.pending_lose_effect
        )
    elif hasattr(game_state, "pending_draw_effect"):
        game_state.effect_resolution_result = game_state.resolve_draw_effect(
            game_state.pending_draw_effect
        )


@when("player one's hero's life total is reduced to 0")
def player_one_hero_life_reduced_to_zero(game_state):
    """Rule 4.5.3a: Apply damage that reduces player one's hero to 0."""
    game_state.player_one_hero_life = 0
    game_state.life_loss_result = game_state.check_hero_life_loss(player_id=0)


@when("player one concedes the game")
def player_one_concedes(game_state):
    """Rule 4.5.3c: Player one performs a concede action."""
    game_state.concede_result = game_state.player_concede(player_id=0)


@when("player one concedes on player two's turn")
def player_one_concedes_on_opponents_turn(game_state):
    """Rule 4.5.3c: Player one concedes while it is player two's turn."""
    game_state.current_turn_player_id = 1
    game_state.concede_result = game_state.player_concede(player_id=0)


@when("an effect simultaneously reduces both heroes' life totals to 0")
def simultaneous_life_reduction_to_zero(game_state):
    """Rule 4.5.4a: Both heroes lose their remaining life simultaneously."""
    game_state.simultaneous_life_loss = True
    game_state.life_loss_result = game_state.check_simultaneous_life_loss(
        player_ids=[0, 1]
    )


@when("player one's hero's life is reduced to 0 first")
def player_one_life_reduced_to_zero_first(game_state):
    """Rule 4.5.4a: Player one's hero reaches 0 first (sequential, not simultaneous)."""
    game_state.simultaneous_life_loss = False
    game_state.player_one_hero_life = 0
    game_state.life_loss_result = game_state.check_hero_life_loss(player_id=0)


@when("both players agree to an intentional draw")
def both_players_agree_intentional_draw(game_state):
    """Rule 4.5.4c: All remaining players consent to an intentional draw."""
    game_state.draw_result = game_state.declare_intentional_draw(
        player_ids=game_state.active_player_ids
    )


@when("both players agree to an intentional draw during the action phase")
def both_players_agree_draw_during_action_phase(game_state):
    """Rule 4.5.4c: Players can agree to draw at any time including action phase."""
    game_state.draw_result = game_state.declare_intentional_draw(
        player_ids=game_state.active_player_ids
    )


@when("the game state is evaluated for stalemate")
def game_state_evaluated_for_stalemate(game_state):
    """Rule 4.5.4d: The game checks whether a stalemate condition exists."""
    game_state.stalemate_result = game_state.check_stalemate()


@when("all remaining players refuse to legally advance the game state")
def all_players_refuse_to_advance(game_state):
    """Rule 4.5.4e: All players decline to make legal plays, constituting a deadlock."""
    game_state.deadlock_result = game_state.check_deadlock()


# ===== Then steps =====


@then("the game ends immediately")
def game_ends_immediately(game_state):
    """Rule 4.5.1: The game ends as soon as end condition is detected."""
    result = game_state.end_condition_result
    assert result.is_over, "Game should have ended immediately"


@then("the result is not ongoing")
def result_is_not_ongoing(game_state):
    """Rule 4.5.1: The game result is no longer 'ongoing'."""
    result = game_state.end_condition_result
    assert not result.is_ongoing, "Game should not be ongoing after end condition"


@then("the result is a draw")
def result_is_draw(game_state):
    """Rule 4.5.1/4.5.4: The game result is a draw."""
    result = game_state.end_condition_result
    assert result.is_draw, "Game result should be a draw"


@then("the game ends")
def the_game_ends(game_state):
    """Rule 4.5.1: The game ends."""
    result = getattr(game_state, "elimination_result", None) or getattr(
        game_state, "end_condition_result", None
    )
    assert result is not None, "An elimination or end condition result should exist"
    assert result.game_ended, "Game should have ended"


@then("player one wins the game")
def player_one_wins(game_state):
    """Rule 4.5.2: Player one is declared the winner."""
    result = getattr(game_state, "elimination_result", None) or getattr(
        game_state, "effect_resolution_result", None
    )
    assert result is not None, "A game result should exist"
    assert result.winner_id == 0, f"Player one should win, got winner_id={result.winner_id}"


@then("player two wins the game")
def player_two_wins(game_state):
    """Rule 4.5.2: Player two is declared the winner."""
    result = (
        getattr(game_state, "concede_result", None)
        or getattr(game_state, "life_loss_result", None)
        or getattr(game_state, "effect_resolution_result", None)
    )
    assert result is not None, "A game result should exist"
    assert result.winner_id == 1, f"Player two should win, got winner_id={result.winner_id}"


@then("player one ceases to exist in the game")
def player_one_ceases_to_exist(game_state):
    """Rule 4.5.1a: Player one is eliminated and ceases to exist."""
    result = game_state.elimination_result
    assert result.player_eliminated, "Player one should be eliminated"
    assert result.player_ceased_to_exist, "Player one should cease to exist"


@then("player one's controlled objects are cleared")
def player_one_controlled_objects_cleared(game_state):
    """Rule 4.5.1a: Objects controlled by player one are cleared first."""
    result = game_state.elimination_result
    assert result.controlled_objects_cleared, "Controlled objects should be cleared"


@then("all objects owned by player one are removed from the game")
def player_one_owned_objects_removed(game_state):
    """Rule 4.5.1a: All objects owned by player one are removed, even if controlled by others."""
    result = game_state.elimination_result
    assert result.owned_objects_removed, "Owned objects should be removed from game"


@then("player one's owned cards controlled by other players are removed")
def owned_cards_controlled_by_others_removed(game_state):
    """Rule 4.5.1a: Even cards under opponent control but owned by player one are removed."""
    result = game_state.elimination_result
    assert result.owned_objects_removed, "Owned objects controlled by others should be removed"


@then("the layer-continuous effect controlled by player one continues to exist")
def layer_continuous_effect_persists(game_state):
    """Rule 4.5.1a: Layer-continuous effects of the losing player persist until expiry."""
    result = game_state.elimination_result
    assert result.layer_continuous_effects_persist, (
        "Layer-continuous effects should persist after player loss"
    )


@then("the effect remains until it expires naturally")
def effect_expires_naturally(game_state):
    """Rule 4.5.1a: The persistent effect will only end when it naturally expires."""
    result = game_state.elimination_result
    assert result.layer_continuous_effects_persist, (
        "Layer-continuous effects should persist until natural expiry"
    )


@then("player one ceases to exist for the remainder of the game")
def player_one_ceases_to_exist_for_remainder(game_state):
    """Rule 4.5.1a: Player one no longer participates in the game."""
    result = game_state.elimination_result
    assert result.player_ceased_to_exist, "Player should cease to exist"


@then("player one's hero ceases to exist for the remainder of the game")
def player_one_hero_ceases_to_exist(game_state):
    """Rule 4.5.1a: Player one's hero also ceases to exist."""
    result = game_state.elimination_result
    assert result.hero_ceased_to_exist, "Hero should cease to exist"


@then("the game ends immediately")
def game_ends_immediately_on_win():
    """Already handled by the 'the game ends immediately' step."""
    pass


@then("player one loses the game")
def player_one_loses(game_state):
    """Rule 4.5.3: Player one has lost the game."""
    result = (
        getattr(game_state, "life_loss_result", None)
        or getattr(game_state, "effect_resolution_result", None)
        or getattr(game_state, "concede_result", None)
        or getattr(game_state, "end_condition_result", None)
    )
    assert result is not None, "A game result should exist"
    assert result.loser_id == 0, f"Player one should lose, got loser_id={result.loser_id}"


@then("neither player wins")
def neither_player_wins(game_state):
    """Rule 4.5.4: No winner is declared in a draw."""
    result = (
        getattr(game_state, "end_condition_result", None)
        or getattr(game_state, "life_loss_result", None)
        or getattr(game_state, "draw_result", None)
        or getattr(game_state, "effect_resolution_result", None)
    )
    assert result is not None, "A game result should exist"
    assert result.winner_id is None, "No player should win in a draw"
    assert result.is_draw, "Result should be a draw"


@then("the game is a draw")
def the_game_is_a_draw(game_state):
    """Rule 4.5.4: The game ends in a draw."""
    result = (
        getattr(game_state, "life_loss_result", None)
        or getattr(game_state, "draw_result", None)
        or getattr(game_state, "effect_resolution_result", None)
        or getattr(game_state, "end_condition_result", None)
    )
    assert result is not None, "A game result should exist"
    assert result.is_draw, "Game should be a draw"


@then("the game is not a draw")
def the_game_is_not_a_draw(game_state):
    """Rule 4.5.4a: Sequential life loss does not result in a draw."""
    result = game_state.life_loss_result
    assert not result.is_draw, "Game should not be a draw when life loss is sequential"


@then("the game is a draw immediately")
def game_is_draw_immediately(game_state):
    """Rule 4.5.4c: Intentional draw takes effect immediately."""
    result = game_state.draw_result
    assert result.is_draw, "Game should immediately be a draw on intentional agreement"
    assert result.is_over, "Game should be over"


@then("no player can legally advance the game state toward ending")
def no_player_can_advance_game_state(game_state):
    """Rule 4.5.4d: No legal action exists that could advance toward a game ending."""
    result = game_state.stalemate_result
    assert result.is_stalemate, "Stalemate should be detected"
    assert result.no_player_can_advance, "No player should be able to advance game state"


@then("the game is a draw by stalemate")
def game_is_draw_by_stalemate(game_state):
    """Rule 4.5.4d: The stalemate results in a draw."""
    result = game_state.stalemate_result
    assert result.is_draw, "Stalemate should result in a draw"
    assert result.reason == "stalemate", f"Draw reason should be 'stalemate', got {result.reason}"


@then("the game is a draw by deadlock")
def game_is_draw_by_deadlock(game_state):
    """Rule 4.5.4e: The deadlock results in a draw."""
    result = game_state.deadlock_result
    assert result.is_draw, "Deadlock should result in a draw"
    assert result.reason == "deadlock", f"Draw reason should be 'deadlock', got {result.reason}"


# ===== Fixture =====


@pytest.fixture
def game_state():
    """
    Fixture providing game state for testing Section 4.5: Ending a Game.

    Uses BDDGameState which integrates with the real engine.
    Reference: Rules 4.5.1 through 4.5.4e
    """
    from tests.bdd_helpers import BDDGameState

    state = BDDGameState()

    # Initialize game tracking fields
    state.player_count = 2
    state.active_player_ids = [0, 1]
    state.current_turn_player_id = 0
    state.current_phase = "action_phase"
    state.game_still_ongoing = True
    state.simultaneous_life_loss = False
    state.player_one_controls_hero = True

    return state
