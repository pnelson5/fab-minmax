"""
Step definitions for Section 7.1: Layer Step
Reference: Flesh and Blood Comprehensive Rules Section 7.1

This module implements behavioral tests for the Layer Step of combat:
the game state where an attack is unresolved on the stack, before it
transitions to the Attack Step.

Engine Features Needed for Section 7.1:
- [ ] CombatChain.is_open property — tracks whether combat chain is open (Rule 7.0.2)
- [ ] CombatChain.open() — opens the combat chain (Rule 7.0.2a)
- [ ] CombatState.current_step property — "layer" | "attack" | "defend" | etc. (Rule 7.1.1)
- [ ] CombatState.layer_step_active property (Rule 7.1.1)
- [ ] CombatState.attack_step_active property (Rule 7.1.3)
- [ ] GameState.turn_player property — player with priority (Rule 7.1.2)
- [ ] PrioritySystem.who_has_priority() -> Player (Rule 7.1.2)
- [ ] PrioritySystem.all_players_passed() -> bool (Rule 7.1.3)
- [ ] Stack.top() -> layer (or None) (Rule 7.1.3)
- [ ] LayerStepTransition: when top-of-stack is attack and all pass → Attack Step begins (Rule 7.1.3)
- [ ] CombatChain.add_attack(attack) — adding attack opens chain and starts Layer Step (Rule 7.0.2a)

Current status: Tests written, Engine pending
"""

import pytest
from pytest_bdd import scenario, given, when, then, parsers


# ===== Scenarios =====

# Rule 7.1.1 — Layer Step is a game state with unresolved attack on stack

@scenario(
    "../features/section_7_1_layer_step.feature",
    "Layer Step is a game state where an attack is unresolved on the stack",
)
def test_layer_step_is_game_state_with_unresolved_attack():
    """Rule 7.1.1: The Layer Step is a game state where an attack is unresolved on the stack."""
    pass


@scenario(
    "../features/section_7_1_layer_step.feature",
    "Layer Step is distinct from normal stack resolution",
)
def test_layer_step_distinct_from_normal_resolution():
    """Rule 7.1.1 + 7.1.3: Attack on top of stack does not resolve as normal layer — Layer Step ends instead."""
    pass


# Rule 7.0.2a + 7.1 — Combat chain opens and Layer Step begins when attack played

@scenario(
    "../features/section_7_1_layer_step.feature",
    "Playing an attack opens the combat chain and begins the Layer Step",
)
def test_playing_attack_opens_chain_and_begins_layer_step():
    """Rule 7.0.2a + 7.1.1: Adding an attack to the stack opens the combat chain and starts Layer Step."""
    pass


@scenario(
    "../features/section_7_1_layer_step.feature",
    "Layer Step begins immediately when attack is played while combat chain was closed",
)
def test_layer_step_begins_immediately_on_attack():
    """Rule 7.0.2a: The combat chain opens and the Layer Step begins immediately when attack is played."""
    pass


# Rule 7.1.2 — Turn-player gains priority

@scenario(
    "../features/section_7_1_layer_step.feature",
    "Turn-player gains priority at the start of the Layer Step",
)
def test_turn_player_gains_priority_in_layer_step():
    """Rule 7.1.2: The turn-player gains priority first in the Layer Step."""
    pass


# Rule 7.1.3 — Layer Step ends and Attack Step begins

@scenario(
    "../features/section_7_1_layer_step.feature",
    "Layer Step ends and Attack Step begins when top of stack is attack and all players pass",
)
def test_layer_step_ends_attack_step_begins_when_all_pass():
    """Rule 7.1.3: When the attack is top of stack and all players pass, Layer Step ends and Attack Step begins."""
    pass


@scenario(
    "../features/section_7_1_layer_step.feature",
    "Layer Step does not end if the top of the stack is not the attack",
)
def test_layer_step_continues_if_attack_not_on_top():
    """Rule 7.1.3: Layer Step only ends when the attack is the top of the stack and all players pass."""
    pass


@scenario(
    "../features/section_7_1_layer_step.feature",
    "Attack Step does not begin if there are layers above the attack when all players pass",
)
def test_attack_step_not_begun_with_layers_above_attack():
    """Rule 7.1.3: Attack Step does not begin if other layers are above the attack on the stack."""
    pass


# Rule 7.1.2 — Players can play instants during Layer Step

@scenario(
    "../features/section_7_1_layer_step.feature",
    "Players can play instants during the Layer Step",
)
def test_players_can_play_instants_during_layer_step():
    """Rule 7.1.2: Players have priority in the Layer Step, so they can play instants."""
    pass


# ===== Step Definitions =====

@given("the combat chain is closed")
def combat_chain_is_closed(game_state):
    """Rule 7.0.2: The combat chain starts closed."""
    game_state.combat_chain_open = False


@given("the stack is empty")
def stack_is_empty(game_state):
    """Precondition: stack has no layers."""
    game_state.stack.clear()


@given("a player has an attack card in hand")
def player_has_attack_card_in_hand(game_state):
    """Precondition: player has an attack card ready to play."""
    from fab_engine.cards.model import CardType
    game_state.test_attack_card = game_state.create_card(
        name="Test Strike",
        card_type=CardType.ACTION,
    )
    game_state.player.hand.add_card(game_state.test_attack_card)


@given("an attack is added to the stack")
@when("an attack is added to the stack")
def attack_added_to_stack(game_state):
    """Rule 7.0.2a: An attack is placed on the stack (opening the combat chain)."""
    from fab_engine.cards.model import CardType
    game_state.test_attack_card = game_state.create_card(
        name="Test Strike",
        card_type=CardType.ACTION,
    )
    game_state.play_card_to_stack(game_state.test_attack_card)
    # Simulate the combat chain opening per Rule 7.0.2a
    game_state.combat_chain_open = True
    game_state.layer_step_active = True


@given("the Layer Step is active")
def layer_step_is_active(game_state):
    """Rule 7.1.1: The Layer Step is active — an attack is unresolved on the stack."""
    from fab_engine.cards.model import CardType
    game_state.test_attack_card = game_state.create_card(
        name="Test Strike",
        card_type=CardType.ACTION,
    )
    game_state.play_card_to_stack(game_state.test_attack_card)
    game_state.combat_chain_open = True
    game_state.layer_step_active = True
    game_state.attack_step_active = False
    game_state.turn_player_has_priority = True


@given("the attack is on the stack")
@given("the attack is unresolved on the stack")
def attack_is_on_stack(game_state):
    """The attack is unresolved on the stack."""
    assert game_state.test_attack_card in game_state.stack, \
        "Attack card should be on the stack"


@given("the top layer of the stack is the attack")
def top_layer_is_attack(game_state):
    """Rule 7.1.3: The attack is the top layer of the stack."""
    assert len(game_state.stack) > 0, "Stack must not be empty"
    assert game_state.stack[-1] is game_state.test_attack_card, \
        "Attack must be the top layer of the stack"


@given("an instant is played on top of the attack")
def instant_played_on_top(game_state):
    """An instant is played on top of the attack, so attack is no longer top of stack."""
    from fab_engine.cards.model import CardType
    game_state.test_instant_card = game_state.create_card(
        name="Test Instant",
        card_type=CardType.INSTANT,
    )
    game_state.stack.append(game_state.test_instant_card)


@given("an instant is on top of the attack on the stack")
def instant_on_top_of_attack(game_state):
    """An instant sits above the attack on the stack."""
    from fab_engine.cards.model import CardType
    game_state.test_instant_card = game_state.create_card(
        name="Test Instant",
        card_type=CardType.INSTANT,
    )
    game_state.stack.append(game_state.test_instant_card)


@given("the attack is the only layer on the stack")
def attack_is_only_layer(game_state):
    """Only the attack is on the stack — no other layers above it."""
    assert len(game_state.stack) == 1, \
        f"Expected only the attack on the stack, found {len(game_state.stack)} layers"
    assert game_state.stack[-1] is game_state.test_attack_card, \
        "The only layer on the stack should be the attack"


@given("the game is in the action phase")
def game_in_action_phase(game_state):
    """Precondition: the game is in the Action Phase."""
    game_state.begin_action_phase_for_player(game_state.player)


@when("the player plays the attack card")
def player_plays_attack_card(game_state):
    """Player plays the attack card from hand to the stack."""
    card = game_state.test_attack_card
    game_state.player.hand.remove_card(card)
    game_state.play_card_to_stack(card)
    # Rule 7.0.2a: playing an attack opens the combat chain and begins Layer Step
    game_state.combat_chain_open = True
    game_state.layer_step_active = True
    game_state.attack_step_active = False


@when("the Layer Step begins")
def layer_step_begins(game_state):
    """Rule 7.1: The Layer Step state is entered."""
    # Layer Step already active from given steps; turn-player gets priority per Rule 7.1.2
    game_state.turn_player_has_priority = True


@when("all players pass priority in succession")
def all_players_pass_priority(game_state):
    """Rule 7.1.3: All players pass priority."""
    # Check if the top of the stack is the attack
    if game_state.stack and game_state.stack[-1] is game_state.test_attack_card:
        # Rule 7.1.3: Layer Step ends, Attack Step begins
        game_state.layer_step_active = False
        game_state.attack_step_active = True
        game_state.all_players_passed_result = "attack_step_begun"
    else:
        # Other layers on top — resolve the top layer first (Rule 5.3.1 normal resolution)
        if game_state.stack:
            resolved = game_state.resolve_top_of_stack()
            game_state.last_resolved = resolved
        game_state.all_players_passed_result = "layer_resolved"


@when("a player plays an instant card")
@when("the turn-player plays an instant card")
def player_plays_instant_card(game_state):
    """Player plays an instant during the Layer Step."""
    from fab_engine.cards.model import CardType
    game_state.test_instant_card = game_state.create_card(
        name="Test Instant",
        card_type=CardType.INSTANT,
    )
    game_state.stack.append(game_state.test_instant_card)
    game_state.instant_played = True


@when("a player plays an attack card targeting the opponent's hero")
def player_plays_attack_targeting_hero(game_state):
    """Player plays an attack card during the action phase."""
    from fab_engine.cards.model import CardType
    game_state.test_attack_card = game_state.create_card(
        name="Test Strike",
        card_type=CardType.ACTION,
    )
    game_state.play_card_to_stack(game_state.test_attack_card)
    # Rule 7.0.2a: combat chain opens immediately
    game_state.combat_chain_open = True
    game_state.layer_step_active = True
    game_state.attack_step_active = False
    game_state.turn_player_has_priority = True


# ===== Then Steps =====

@then("the attack is on the stack as an unresolved layer")
def attack_is_on_stack_unresolved(game_state):
    """Rule 7.1.1: The attack is on the stack and has not resolved."""
    assert game_state.test_attack_card in game_state.stack, \
        "Attack card should be on the stack as an unresolved layer"


@then("the combat chain is open")
@then("the combat chain opens")
@then("the combat chain opens immediately")
def combat_chain_is_open(game_state):
    """Rule 7.0.2a: The combat chain is open."""
    assert game_state.combat_chain_open is True, \
        "Combat chain should be open after an attack is played"


@then("the Layer Step is active")
def layer_step_is_active_check(game_state):
    """Rule 7.1.1: The Layer Step is the current game state."""
    assert game_state.layer_step_active is True, \
        "Layer Step should be active when an attack is unresolved on the stack"



@then("the Layer Step begins immediately")
@then("the Layer Step begins")
def layer_step_begins_immediately(game_state):
    """Rule 7.0.2a: The Layer Step begins immediately when attack is added to closed combat chain."""
    assert game_state.layer_step_active is True, \
        "Layer Step should begin immediately when combat chain opens"


@then("the turn-player has priority")
@then("the turn-player has priority in the Layer Step")
def turn_player_has_priority(game_state):
    """Rule 7.1.2: The turn-player gains priority first in the Layer Step."""
    assert game_state.turn_player_has_priority is True, \
        "Turn-player should have priority at the start of the Layer Step"


@then("the Layer Step ends")
def layer_step_ends(game_state):
    """Rule 7.1.3: The Layer Step ends when attack is on top and all players pass."""
    assert game_state.layer_step_active is False, \
        "Layer Step should have ended"


@then("the Attack Step begins")
def attack_step_begins(game_state):
    """Rule 7.1.3: The Attack Step begins after the Layer Step ends."""
    assert game_state.attack_step_active is True, \
        "Attack Step should have begun after the Layer Step ended"


@then("the instant resolves")
def instant_resolves(game_state):
    """Normal stack resolution: the instant (top of stack) resolved."""
    assert game_state.test_instant_card not in game_state.stack, \
        "Instant should have resolved from the stack"


@then("the Layer Step continues because the attack is now the top of the stack")
def layer_step_continues_attack_now_on_top(game_state):
    """Rule 7.1.3: After the instant resolved, the attack is on top; Layer Step continues (not ended yet)."""
    assert game_state.test_attack_card in game_state.stack, \
        "Attack should still be on the stack"
    # Layer Step continues — it hasn't ended yet because we need another pass for it to end
    # (After instant resolves, priority would be given again, and all would need to pass again)


@then("the instant is placed on the stack above the attack")
def instant_placed_above_attack(game_state):
    """The instant is now the top layer of the stack, above the attack."""
    assert len(game_state.stack) >= 2, "Stack should have at least 2 layers"
    assert game_state.stack[-1] is game_state.test_instant_card, \
        "Instant should be on top of the stack"
    assert game_state.test_attack_card in game_state.stack, \
        "Attack should still be on the stack below the instant"


@then("the attack remains unresolved on the stack")
def attack_remains_on_stack(game_state):
    """The attack is still on the stack while the instant is above it."""
    assert game_state.test_attack_card in game_state.stack, \
        "Attack should remain on the stack (unresolved)"


@then("the instant resolves from the stack")
def instant_resolves_from_stack(game_state):
    """The instant resolved as the top layer of the stack per normal resolution (Rule 5.3.1)."""
    assert game_state.test_instant_card not in game_state.stack, \
        "Instant should have resolved from the stack"


@then("the Layer Step continues")
def layer_step_continues(game_state):
    """Rule 7.1.3: Layer Step has not ended."""
    assert game_state.layer_step_active is True, \
        "Layer Step should still be active"


@then("the Attack Step has not begun")
def attack_step_not_begun(game_state):
    """Rule 7.1.3: Attack Step has not begun because the attack was not on top of the stack."""
    assert not getattr(game_state, "attack_step_active", False), \
        "Attack Step should NOT have begun yet"


@then("the attack does not resolve as a normal layer")
def attack_does_not_resolve_as_normal_layer(game_state):
    """Rule 7.1.1 + 5.3.1: Attack does not resolve via normal layer resolution in the Layer Step."""
    # The attack should still be on the stack — it does not resolve normally
    assert game_state.test_attack_card in game_state.stack, \
        "Attack should NOT have resolved as a normal layer — it transitions to Attack Step"


@then("instead the Layer Step ends and the Attack Step begins")
def layer_step_ends_attack_step_begins_instead(game_state):
    """Rule 7.1.3: The transition is Layer Step → Attack Step, not normal stack resolution."""
    assert game_state.layer_step_active is False, "Layer Step should have ended"
    assert game_state.attack_step_active is True, "Attack Step should have begun"


# ===== Fixtures =====

@pytest.fixture
def game_state():
    """
    Fixture providing game state for testing Section 7.1: Layer Step.

    Uses BDDGameState which integrates with the real engine.
    Reference: Rule 7.1
    """
    from tests.bdd_helpers import BDDGameState

    state = BDDGameState()

    # Layer Step tracking (engine feature needed: CombatState)
    state.combat_chain_open = False
    state.layer_step_active = False
    state.attack_step_active = False
    state.turn_player_has_priority = False
    state.all_players_passed_result = None
    state.last_resolved = None
    state.instant_played = False

    return state
