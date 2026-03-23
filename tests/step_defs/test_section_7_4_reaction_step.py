"""
Step definitions for Section 7.4: Reaction Step
Reference: Flesh and Blood Comprehensive Rules Section 7.4

This module implements behavioral tests for the Reaction Step of combat:
the game state where players may use reactions related to combat.

Engine Features Needed for Section 7.4:
- [ ] CombatState.reaction_step_active property — tracks Reaction Step (Rule 7.4.1)
- [ ] CombatState.current_step property — "layer"|"attack"|"defend"|"reaction"|"damage"|"resolution"|"close"
- [ ] ReactionStep.begin() — starts Reaction Step after Defend Step ends (Rule 7.4.1)
- [ ] ReactionStep.end() — ends Reaction Step and begins Damage Step (Rule 7.4.3)
- [ ] DamageStep.begin() — begins Damage Step after Reaction Step ends (Rule 7.4.3)
- [ ] PrioritySystem.grant_priority_to_turn_player() — (Rule 7.4.2)
- [ ] PrioritySystem.all_players_passed() -> bool — (Rule 7.4.3)
- [ ] CardInstance.is_attack_reaction property — true for attack reaction cards (Rule 7.4.2a)
- [ ] CardInstance.is_defense_reaction property — true for defense reaction cards (Rule 7.4.2b)
- [ ] AttackReaction.can_be_played(player, combat_state) -> bool — checks attack reaction legality (Rule 7.4.2a)
- [ ] DefenseReaction.can_be_played(player, combat_state) -> bool — checks defense reaction legality (Rule 7.4.2b/c)
- [ ] DefenseReaction.resolve(chain_link) -> ResolveResult — resolves defense reaction as defending card (Rule 7.4.2d)
- [ ] ChainLink.add_defending_card(card) — adds a defending card to the chain link (Rule 7.4.2d)
- [ ] ChainLink.defending_cards list — all defending cards on the chain link (Rule 7.4.2d)
- [ ] AttackKeywords.dominate — prevents defending by more than 1 card from hand (Rule 7.4.2c/d)
- [ ] CombatState.attack_controller property — player that controls the active attack (Rule 7.4.2a)
- [ ] CombatState.attack_targets list — heroes that are attack-targets (Rule 7.4.2b)
- [ ] Stack.is_empty property — whether the stack currently has items (Rule 7.4.3)

Current status: Tests written, Engine pending
"""

import pytest
from pytest_bdd import scenario, given, when, then, parsers


# ===== Scenarios =====

# Rule 7.4.1 — Reaction Step is a distinct game state

@scenario(
    "../features/section_7_4_reaction_step.feature",
    "Reaction Step is a game state where reactions may be used",
)
def test_reaction_step_is_game_state():
    """Rule 7.4.1: The Reaction Step is a distinct game state for combat reactions."""
    pass


@scenario(
    "../features/section_7_4_reaction_step.feature",
    "Reaction Step begins after the Defend Step ends",
)
def test_reaction_step_begins_after_defend_step():
    """Rule 7.3.4 → 7.4.1: Reaction Step begins after the Defend Step ends."""
    pass


# Rule 7.4.2 — Turn-player gains priority first

@scenario(
    "../features/section_7_4_reaction_step.feature",
    "Turn-player gains priority first in the Reaction Step",
)
def test_turn_player_gains_priority_first():
    """Rule 7.4.2: The turn-player gains priority first in the Reaction Step."""
    pass


# Rule 7.4.2a — Attack controller may play attack reactions

@scenario(
    "../features/section_7_4_reaction_step.feature",
    "Attack controller may play attack reaction cards during Reaction Step",
)
def test_attack_controller_may_play_attack_reaction():
    """Rule 7.4.2a: Attack controller may play attack reaction cards."""
    pass


@scenario(
    "../features/section_7_4_reaction_step.feature",
    "Attack controller may activate attack reaction abilities during Reaction Step",
)
def test_attack_controller_may_activate_attack_reaction():
    """Rule 7.4.2a: Attack controller may activate attack reaction abilities."""
    pass


@scenario(
    "../features/section_7_4_reaction_step.feature",
    "Non-attack-controller cannot play attack reaction cards",
)
def test_non_attack_controller_cannot_play_attack_reaction():
    """Rule 7.4.2a: Only the attack controller may play attack reaction cards."""
    pass


@scenario(
    "../features/section_7_4_reaction_step.feature",
    "Attack reaction cards cannot be played outside the Reaction Step",
)
def test_attack_reaction_cannot_be_played_outside_reaction_step():
    """Rule 7.4.2a: Attack reactions can only be played during the Reaction Step."""
    pass


# Rule 7.4.2b — Defense reaction may be played by defending hero controller

@scenario(
    "../features/section_7_4_reaction_step.feature",
    "Defending hero controller may play defense reaction cards during Reaction Step",
)
def test_defending_hero_controller_may_play_defense_reaction():
    """Rule 7.4.2b: Player controlling a hero as attack-target may play defense reactions."""
    pass


@scenario(
    "../features/section_7_4_reaction_step.feature",
    "Defending hero controller may activate defense reaction abilities during Reaction Step",
)
def test_defending_hero_controller_may_activate_defense_reaction():
    """Rule 7.4.2b: Player controlling a hero as attack-target may activate defense reaction abilities."""
    pass


@scenario(
    "../features/section_7_4_reaction_step.feature",
    "Player without hero as attack-target cannot play defense reaction cards",
)
def test_player_without_hero_as_target_cannot_play_defense_reaction():
    """Rule 7.4.2b: Only players whose hero is an attack-target may play defense reactions."""
    pass


# Rule 7.4.2c — Defense reaction blocked by defend restriction

@scenario(
    "../features/section_7_4_reaction_step.feature",
    "Defense reaction cannot be played if a rule prevents defending with it",
)
def test_defense_reaction_blocked_by_dominate():
    """Rule 7.4.2c: Defense reaction cannot be played if a rule prevents defending with that card."""
    pass


@scenario(
    "../features/section_7_4_reaction_step.feature",
    "Defense reaction can be played when no defend restriction applies",
)
def test_defense_reaction_allowed_without_restriction():
    """Rule 7.4.2c: Defense reaction can be played when no restriction prevents defending."""
    pass


@scenario(
    "../features/section_7_4_reaction_step.feature",
    "Defense reaction can be played when dominate is present but no card from hand defends yet",
)
def test_defense_reaction_allowed_with_dominate_but_no_hand_defender():
    """Rule 7.4.2c: Dominate only blocks additional hand cards; first defense reaction still legal."""
    pass


# Rule 7.4.2d — Defense reaction resolves as a defending card

@scenario(
    "../features/section_7_4_reaction_step.feature",
    "Defense reaction card becomes a defending card when it resolves",
)
def test_defense_reaction_becomes_defending_card():
    """Rule 7.4.2d: A defense reaction card becomes a defending card on the active chain link when it resolves."""
    pass


@scenario(
    "../features/section_7_4_reaction_step.feature",
    "Defense reaction card fails to resolve if it cannot become a defending card",
)
def test_defense_reaction_fails_to_resolve_when_blocked():
    """Rule 7.4.2d: A defense reaction fails to resolve if it cannot become a defending card."""
    pass


@scenario(
    "../features/section_7_4_reaction_step.feature",
    "Second defense reaction fails when dominate already satisfied by first",
)
def test_second_defense_reaction_fails_with_dominate():
    """Rule 7.4.2d: Second defense reaction fails when dominate limit is already filled by first."""
    pass


# Rule 7.4.3 — Reaction Step ends, Damage Step begins

@scenario(
    "../features/section_7_4_reaction_step.feature",
    "Reaction Step ends and Damage Step begins when stack is empty and all players pass",
)
def test_reaction_step_ends_damage_step_begins():
    """Rule 7.4.3: Reaction Step ends and Damage Step begins when stack empty and all players pass."""
    pass


@scenario(
    "../features/section_7_4_reaction_step.feature",
    "Reaction Step does not end while there are items on the stack",
)
def test_reaction_step_does_not_end_with_stack_items():
    """Rule 7.4.3: Reaction Step does not end while items remain on the stack."""
    pass


@scenario(
    "../features/section_7_4_reaction_step.feature",
    "Reaction Step does not end if not all players have passed",
)
def test_reaction_step_does_not_end_without_all_passing():
    """Rule 7.4.3: Reaction Step does not end if not all players have passed priority."""
    pass


# ===== Step Definitions =====

# --- Given steps ---

@given("the Defend Step has completed")
def defend_step_completed(reaction_step_state):
    """Rule 7.3.4: The Defend Step has ended, setting up for the Reaction Step."""
    reaction_step_state.defend_step_completed = True


@given("the Defend Step has ended")
def defend_step_ended(reaction_step_state):
    """Rule 7.3.4: Defend Step has ended."""
    reaction_step_state.defend_step_completed = True


@given("the Reaction Step begins")
def reaction_step_begins(reaction_step_state):
    """Rule 7.4.1: The Reaction Step begins."""
    reaction_step_state.begin_reaction_step()


@given("the Reaction Step is active")
def reaction_step_is_active(reaction_step_state):
    """Rule 7.4.1: The Reaction Step is the current combat step."""
    reaction_step_state.begin_reaction_step()


@given("priority is granted at the start of the Reaction Step")
def priority_granted_at_start(reaction_step_state):
    """Rule 7.4.2: Priority is granted to the turn-player."""
    reaction_step_state.grant_priority_to_turn_player()


@given("a combat chain is active with an attack on the chain link")
def combat_chain_active_with_attack(reaction_step_state):
    """Setup: There is an active combat chain with an attack."""
    reaction_step_state.combat_chain_active = True
    reaction_step_state.has_attack_on_chain_link = True


@given("player A controls the attack")
def player_a_controls_attack(reaction_step_state):
    """Rule 7.4.2a: Player A is the attack controller."""
    reaction_step_state.attack_controller = "player_a"


@given("player A has an attack reaction card in hand")
def player_a_has_attack_reaction_card(reaction_step_state):
    """Setup: Player A has an attack reaction card in hand."""
    card = reaction_step_state.create_attack_reaction_card("Test Attack Reaction")
    reaction_step_state.player_a_hand.append(card)
    reaction_step_state.attack_reaction_card = card


@given("player A controls a permanent with an attack reaction activated ability")
def player_a_has_attack_reaction_permanent(reaction_step_state):
    """Rule 7.4.2a: Player A has a permanent with an attack reaction activated ability."""
    permanent = reaction_step_state.create_permanent_with_attack_reaction_ability(
        "Test Attack Reaction Permanent"
    )
    reaction_step_state.player_a_permanents.append(permanent)
    reaction_step_state.attack_reaction_permanent = permanent


@given("player B does not control the attack")
def player_b_does_not_control_attack(reaction_step_state):
    """Rule 7.4.2a: Player B is not the attack controller."""
    reaction_step_state.attack_controller = "player_a"


@given("player B has an attack reaction card in hand")
def player_b_has_attack_reaction_card(reaction_step_state):
    """Setup: Player B has an attack reaction card in hand."""
    card = reaction_step_state.create_attack_reaction_card("Test Attack Reaction B")
    reaction_step_state.player_b_hand.append(card)
    reaction_step_state.attack_reaction_card = card


@given("the Defend Step is active")
def defend_step_is_active(reaction_step_state):
    """Setup: The Defend Step is currently active, not the Reaction Step."""
    reaction_step_state.current_step = "defend"


@given("player B controls a hero that is an attack-target")
def player_b_hero_is_attack_target(reaction_step_state):
    """Rule 7.4.2b: Player B's hero is an attack-target."""
    reaction_step_state.attack_targets.append("player_b_hero")
    reaction_step_state.attack_target_controller = "player_b"


@given("player B has a defense reaction card in hand")
def player_b_has_defense_reaction_card(reaction_step_state):
    """Setup: Player B has a defense reaction card in hand."""
    card = reaction_step_state.create_defense_reaction_card("Test Defense Reaction")
    reaction_step_state.player_b_hand.append(card)
    reaction_step_state.defense_reaction_card = card


@given("player B controls a permanent with a defense reaction activated ability")
def player_b_has_defense_reaction_permanent(reaction_step_state):
    """Rule 7.4.2b: Player B has a permanent with a defense reaction activated ability."""
    permanent = reaction_step_state.create_permanent_with_defense_reaction_ability(
        "Test Defense Reaction Permanent"
    )
    reaction_step_state.player_b_permanents.append(permanent)
    reaction_step_state.defense_reaction_permanent = permanent


@given("player B does not control a hero that is an attack-target")
def player_b_hero_not_attack_target(reaction_step_state):
    """Rule 7.4.2b: Player B's hero is NOT an attack-target."""
    reaction_step_state.attack_targets = [
        t for t in reaction_step_state.attack_targets if t != "player_b_hero"
    ]
    reaction_step_state.attack_target_controller = "player_a"


@given("the active attack has dominate")
def attack_has_dominate(reaction_step_state):
    """Rule 7.4.2c: The active attack has the dominate keyword."""
    reaction_step_state.attack_has_dominate = True


@given("the hero is already defended by a card from hand")
def hero_defended_by_hand_card(reaction_step_state):
    """Rule 7.4.2c: The attacking hero is already defended by a hand card."""
    reaction_step_state.defending_hand_card_count = 1


@given("the active attack does not have dominate")
def attack_no_dominate(reaction_step_state):
    """Rule 7.4.2c: The active attack does not have dominate."""
    reaction_step_state.attack_has_dominate = False


@given("no cards from hand are defending yet")
def no_hand_cards_defending(reaction_step_state):
    """Rule 7.4.2c: No cards from hand are currently defending."""
    reaction_step_state.defending_hand_card_count = 0


@given("a defense reaction card is on the stack")
def defense_reaction_on_stack(reaction_step_state):
    """Rule 7.4.2d: A defense reaction card is on the stack."""
    card = reaction_step_state.create_defense_reaction_card("Defense Reaction On Stack")
    reaction_step_state.stack.append(card)
    reaction_step_state.defense_reaction_card = card


@given("a defending card from hand is already on the chain link")
def defending_card_from_hand_on_chain_link(reaction_step_state):
    """Rule 7.4.2d: There is already a defending card from hand on the chain link."""
    reaction_step_state.defending_hand_card_count = 1


@given("two defense reaction cards are on the stack")
def two_defense_reactions_on_stack(reaction_step_state):
    """Rule 7.4.2d: Two defense reaction cards are on the stack."""
    card1 = reaction_step_state.create_defense_reaction_card("Defense Reaction 1")
    card2 = reaction_step_state.create_defense_reaction_card("Defense Reaction 2")
    reaction_step_state.stack.append(card2)  # card2 on bottom
    reaction_step_state.stack.append(card1)  # card1 on top (resolves first)
    reaction_step_state.defense_reaction_card_1 = card1
    reaction_step_state.defense_reaction_card_2 = card2


@given("the stack is empty")
def stack_is_empty(reaction_step_state):
    """Rule 7.4.3: The stack is currently empty."""
    reaction_step_state.stack.clear()


@given("a reaction card is on the stack")
def reaction_card_on_stack(reaction_step_state):
    """Rule 7.4.3: A reaction card is on the stack."""
    card = reaction_step_state.create_attack_reaction_card("Reaction On Stack")
    reaction_step_state.stack.append(card)


# --- When steps ---

@when("the Reaction Step begins")
def when_reaction_step_begins(reaction_step_state):
    """Rule 7.4.1: The Reaction Step begins."""
    reaction_step_state.begin_reaction_step()


@when("the game advances")
def when_game_advances(reaction_step_state):
    """Transition: The game transitions from Defend Step to Reaction Step."""
    reaction_step_state.advance_from_defend_step()


@when("priority is granted at the start of the Reaction Step")
def when_priority_granted(reaction_step_state):
    """Rule 7.4.2: Priority is granted at the start of the Reaction Step."""
    reaction_step_state.grant_priority_to_turn_player()


@when("player A attempts to play the attack reaction card")
def when_player_a_plays_attack_reaction(reaction_step_state):
    """Rule 7.4.2a: Player A attempts to play an attack reaction card."""
    reaction_step_state.play_result = reaction_step_state.attempt_play_reaction(
        player="player_a",
        card=reaction_step_state.attack_reaction_card,
        current_step=reaction_step_state.current_step,
        attack_controller=reaction_step_state.attack_controller,
        attack_targets=reaction_step_state.attack_targets,
    )


@when("player A attempts to activate the attack reaction ability")
def when_player_a_activates_attack_reaction(reaction_step_state):
    """Rule 7.4.2a: Player A attempts to activate an attack reaction ability."""
    reaction_step_state.activation_result = (
        reaction_step_state.attempt_activate_reaction_ability(
            player="player_a",
            permanent=reaction_step_state.attack_reaction_permanent,
            current_step=reaction_step_state.current_step,
            attack_controller=reaction_step_state.attack_controller,
        )
    )


@when("player B attempts to play the attack reaction card")
def when_player_b_plays_attack_reaction(reaction_step_state):
    """Rule 7.4.2a: Player B (non-attack-controller) attempts to play an attack reaction card."""
    reaction_step_state.play_result = reaction_step_state.attempt_play_reaction(
        player="player_b",
        card=reaction_step_state.attack_reaction_card,
        current_step=reaction_step_state.current_step,
        attack_controller=reaction_step_state.attack_controller,
        attack_targets=reaction_step_state.attack_targets,
    )


@when("player B attempts to play the defense reaction card")
def when_player_b_plays_defense_reaction(reaction_step_state):
    """Rule 7.4.2b: Player B attempts to play a defense reaction card."""
    reaction_step_state.play_result = reaction_step_state.attempt_play_reaction(
        player="player_b",
        card=reaction_step_state.defense_reaction_card,
        current_step=reaction_step_state.current_step,
        attack_controller=reaction_step_state.attack_controller,
        attack_targets=reaction_step_state.attack_targets,
    )


@when("player B attempts to play the defense reaction card from hand")
def when_player_b_plays_defense_reaction_from_hand(reaction_step_state):
    """Rule 7.4.2c: Player B attempts to play a defense reaction card from hand."""
    reaction_step_state.play_result = reaction_step_state.attempt_play_defense_reaction_from_hand(
        player="player_b",
        card=reaction_step_state.defense_reaction_card,
        current_step=reaction_step_state.current_step,
        attack_targets=reaction_step_state.attack_targets,
        attack_has_dominate=reaction_step_state.attack_has_dominate,
        defending_hand_card_count=reaction_step_state.defending_hand_card_count,
    )


@when("player B attempts to activate the defense reaction ability")
def when_player_b_activates_defense_reaction(reaction_step_state):
    """Rule 7.4.2b: Player B attempts to activate a defense reaction ability."""
    reaction_step_state.activation_result = (
        reaction_step_state.attempt_activate_reaction_ability(
            player="player_b",
            permanent=reaction_step_state.defense_reaction_permanent,
            current_step=reaction_step_state.current_step,
            attack_targets=reaction_step_state.attack_targets,
            attack_target_controller=reaction_step_state.attack_target_controller,
        )
    )


@when("the defense reaction card resolves")
def when_defense_reaction_resolves(reaction_step_state):
    """Rule 7.4.2d: The defense reaction card resolves."""
    reaction_step_state.resolve_result = reaction_step_state.resolve_defense_reaction(
        card=reaction_step_state.defense_reaction_card,
        attack_has_dominate=reaction_step_state.attack_has_dominate,
        defending_hand_card_count=reaction_step_state.defending_hand_card_count,
    )


@when("the first defense reaction card resolves")
def when_first_defense_reaction_resolves(reaction_step_state):
    """Rule 7.4.2d: The first defense reaction card resolves."""
    reaction_step_state.first_resolve_result = reaction_step_state.resolve_defense_reaction(
        card=reaction_step_state.defense_reaction_card_1,
        attack_has_dominate=reaction_step_state.attack_has_dominate,
        defending_hand_card_count=reaction_step_state.defending_hand_card_count,
    )
    # After first resolves, it occupies the dominate slot
    if reaction_step_state.first_resolve_result.became_defending:
        reaction_step_state.defending_hand_card_count += 1


@when("the second defense reaction card resolves")
def when_second_defense_reaction_resolves(reaction_step_state):
    """Rule 7.4.2d: The second defense reaction card attempts to resolve."""
    reaction_step_state.second_resolve_result = reaction_step_state.resolve_defense_reaction(
        card=reaction_step_state.defense_reaction_card_2,
        attack_has_dominate=reaction_step_state.attack_has_dominate,
        defending_hand_card_count=reaction_step_state.defending_hand_card_count,
    )


@when("all players pass priority")
def when_all_players_pass_simple(reaction_step_state):
    """Rule 7.4.3: All players pass priority."""
    reaction_step_state.all_players_passed = True
    reaction_step_state.check_step_end_condition()


@when("all players pass priority in succession")
def when_all_players_pass(reaction_step_state):
    """Rule 7.4.3: All players pass priority in succession."""
    reaction_step_state.all_players_passed = True
    reaction_step_state.check_step_end_condition()


@when("only the turn-player passes priority")
def when_only_turn_player_passes(reaction_step_state):
    """Rule 7.4.3: Only the turn-player passes priority."""
    reaction_step_state.turn_player_passed = True
    reaction_step_state.all_players_passed = False
    reaction_step_state.check_step_end_condition()


# --- Then steps ---

@then(parsers.parse('the current combat step is "{step}"'))
def then_current_combat_step_is(reaction_step_state, step):
    """Verify the current combat step."""
    assert reaction_step_state.current_step == step, (
        f"Expected step '{step}' but got '{reaction_step_state.current_step}'"
    )


@then("it is valid for players to use combat reactions")
def then_reactions_valid(reaction_step_state):
    """Rule 7.4.1: Reactions may be used during the Reaction Step."""
    assert reaction_step_state.reactions_are_valid, (
        "Expected reactions to be valid during the Reaction Step"
    )


@then("the Reaction Step begins")
def then_reaction_step_begins(reaction_step_state):
    """Rule 7.4.1: The Reaction Step has begun."""
    assert reaction_step_state.current_step == "reaction", (
        f"Expected Reaction Step but current step is '{reaction_step_state.current_step}'"
    )


@then("the turn-player has priority")
def then_turn_player_has_priority(reaction_step_state):
    """Rule 7.4.2: The turn-player has priority."""
    assert reaction_step_state.priority_holder == "turn_player", (
        f"Expected turn-player to have priority but priority is with '{reaction_step_state.priority_holder}'"
    )


@then("the play is legal")
def then_play_is_legal(reaction_step_state):
    """The play was found to be legal."""
    assert reaction_step_state.play_result is not None, "play_result is None"
    assert reaction_step_state.play_result.success, (
        f"Expected play to be legal but got: {reaction_step_state.play_result.reason}"
    )


@then("the play is illegal")
def then_play_is_illegal(reaction_step_state):
    """The play was found to be illegal."""
    assert reaction_step_state.play_result is not None, "play_result is None"
    assert not reaction_step_state.play_result.success, (
        "Expected play to be illegal but play was allowed"
    )


@then("the activation is legal")
def then_activation_is_legal(reaction_step_state):
    """The ability activation was found to be legal."""
    assert reaction_step_state.activation_result is not None, "activation_result is None"
    assert reaction_step_state.activation_result.success, (
        f"Expected activation to be legal but got: {reaction_step_state.activation_result.reason}"
    )


@then(parsers.parse('the reason is "{reason}"'))
def then_reason_is(reaction_step_state, reason):
    """The play/action was blocked for the expected reason."""
    assert reaction_step_state.play_result is not None, "play_result is None"
    assert reason.lower() in reaction_step_state.play_result.reason.lower(), (
        f"Expected reason to contain '{reason}' but got '{reaction_step_state.play_result.reason}'"
    )


@then("the defense reaction card becomes a defending card on the active chain link")
def then_defense_reaction_becomes_defending(reaction_step_state):
    """Rule 7.4.2d: The defense reaction card is now a defending card."""
    assert reaction_step_state.resolve_result is not None, "resolve_result is None"
    assert reaction_step_state.resolve_result.became_defending, (
        "Expected defense reaction to become a defending card but it did not"
    )


@then("the defending card is associated with player B's hero")
def then_defending_card_associated_with_player_b(reaction_step_state):
    """Rule 7.4.2d: The defending card is associated with player B's hero."""
    assert reaction_step_state.resolve_result is not None, "resolve_result is None"
    assert reaction_step_state.resolve_result.controller_hero == "player_b_hero", (
        f"Expected defending card associated with player_b_hero but got "
        f"'{reaction_step_state.resolve_result.controller_hero}'"
    )


@then("the defense reaction card fails to resolve")
def then_defense_reaction_fails_to_resolve(reaction_step_state):
    """Rule 7.4.2d: The defense reaction card failed to resolve."""
    assert reaction_step_state.resolve_result is not None, "resolve_result is None"
    assert reaction_step_state.resolve_result.failed, (
        "Expected defense reaction to fail to resolve but it resolved successfully"
    )


@then("the defense reaction card does not become a defending card")
def then_defense_reaction_not_defending(reaction_step_state):
    """Rule 7.4.2d: The defense reaction card did not become a defending card."""
    assert reaction_step_state.resolve_result is not None, "resolve_result is None"
    assert not reaction_step_state.resolve_result.became_defending, (
        "Expected defense reaction to not become a defending card"
    )


@then("the first defense reaction card becomes a defending card on the active chain link")
def then_first_defense_reaction_becomes_defending(reaction_step_state):
    """Rule 7.4.2d: The first defense reaction card became a defending card."""
    assert reaction_step_state.first_resolve_result is not None, "first_resolve_result is None"
    assert reaction_step_state.first_resolve_result.became_defending, (
        "Expected first defense reaction to become a defending card but it did not"
    )


@then("the second defense reaction card fails to resolve")
def then_second_defense_reaction_fails(reaction_step_state):
    """Rule 7.4.2d: The second defense reaction card failed to resolve."""
    assert reaction_step_state.second_resolve_result is not None, "second_resolve_result is None"
    assert reaction_step_state.second_resolve_result.failed, (
        "Expected second defense reaction to fail to resolve but it resolved successfully"
    )


@then("the second defense reaction card does not become a defending card")
def then_second_defense_reaction_not_defending(reaction_step_state):
    """Rule 7.4.2d: The second defense reaction card did not become a defending card."""
    assert reaction_step_state.second_resolve_result is not None, "second_resolve_result is None"
    assert not reaction_step_state.second_resolve_result.became_defending, (
        "Expected second defense reaction to not become a defending card"
    )


@then("the Reaction Step ends")
def then_reaction_step_ends(reaction_step_state):
    """Rule 7.4.3: The Reaction Step has ended."""
    assert reaction_step_state.reaction_step_ended, (
        "Expected Reaction Step to have ended but it has not"
    )


@then("the Damage Step begins")
def then_damage_step_begins(reaction_step_state):
    """Rule 7.4.3: The Damage Step has begun."""
    assert reaction_step_state.current_step == "damage", (
        f"Expected Damage Step but current step is '{reaction_step_state.current_step}'"
    )


@then("the Reaction Step has not ended")
def then_reaction_step_not_ended(reaction_step_state):
    """Rule 7.4.3: The Reaction Step has not ended yet."""
    assert not reaction_step_state.reaction_step_ended, (
        "Expected Reaction Step to still be active but it ended"
    )


# ===== Fixture =====

@pytest.fixture
def reaction_step_state():
    """
    Fixture providing game state for Reaction Step testing.

    Uses ReactionStepTestState which wraps real engine components
    where available, and documents missing features needed.
    Reference: Rule 7.4
    """
    return ReactionStepTestState()


class ReactionPlayResult:
    """Result of attempting to play a reaction card/ability."""

    def __init__(self, success: bool, reason: str = ""):
        self.success = success
        self.reason = reason


class ReactionActivationResult:
    """Result of attempting to activate a reaction ability."""

    def __init__(self, success: bool, reason: str = ""):
        self.success = success
        self.reason = reason


class DefenseReactionResolveResult:
    """Result of resolving a defense reaction card."""

    def __init__(self, became_defending: bool, failed: bool, controller_hero: str = ""):
        self.became_defending = became_defending
        self.failed = failed
        self.controller_hero = controller_hero


class ReactionStepCard:
    """Minimal card representation for Reaction Step tests."""

    def __init__(self, name: str, card_type: str):
        self.name = name
        self.card_type = card_type  # "attack_reaction" or "defense_reaction"
        self.is_attack_reaction = card_type == "attack_reaction"
        self.is_defense_reaction = card_type == "defense_reaction"
        self.from_hand = True


class ReactionStepPermanent:
    """Minimal permanent representation for Reaction Step tests."""

    def __init__(self, name: str, ability_type: str):
        self.name = name
        self.ability_type = ability_type  # "attack_reaction" or "defense_reaction"


class ReactionStepTestState:
    """
    Test state for Section 7.4: Reaction Step.

    Tracks combat state needed to verify Reaction Step rules.
    Engine Features Needed (documented per rule):
    - CombatState.current_step (7.4.1)
    - ReactionStep.begin() / end() (7.4.1, 7.4.3)
    - PrioritySystem (7.4.2, 7.4.3)
    - AttackReaction/DefenseReaction play legality (7.4.2a/b/c)
    - DefenseReaction.resolve() → chain link (7.4.2d)
    """

    def __init__(self):
        self.current_step = None
        self.combat_chain_active = False
        self.has_attack_on_chain_link = False
        self.defend_step_completed = False
        self.reaction_step_ended = False
        self.attack_controller = None
        self.attack_targets = []
        self.attack_target_controller = None
        self.attack_has_dominate = False
        self.defending_hand_card_count = 0
        self.priority_holder = None
        self.stack = []
        self.all_players_passed = False
        self.turn_player_passed = False
        self.player_a_hand = []
        self.player_b_hand = []
        self.player_a_permanents = []
        self.player_b_permanents = []
        self.attack_reaction_card = None
        self.defense_reaction_card = None
        self.attack_reaction_permanent = None
        self.defense_reaction_permanent = None
        self.defense_reaction_card_1 = None
        self.defense_reaction_card_2 = None
        self.play_result = None
        self.activation_result = None
        self.resolve_result = None
        self.first_resolve_result = None
        self.second_resolve_result = None
        self.chain_link_defending_cards = []
        self.reactions_are_valid = False

    def begin_reaction_step(self):
        """Rule 7.4.1: Transition to the Reaction Step."""
        self.current_step = "reaction"
        self.reactions_are_valid = True
        self.grant_priority_to_turn_player()

    def grant_priority_to_turn_player(self):
        """Rule 7.4.2: Grant priority to the turn-player."""
        self.priority_holder = "turn_player"

    def advance_from_defend_step(self):
        """Rule 7.3.4 → 7.4.1: Advance from Defend Step to Reaction Step."""
        if self.defend_step_completed:
            self.begin_reaction_step()

    def check_step_end_condition(self):
        """Rule 7.4.3: Check if Reaction Step should end."""
        if self.all_players_passed and len(self.stack) == 0:
            self.reaction_step_ended = True
            self.current_step = "damage"

    def create_attack_reaction_card(self, name: str) -> ReactionStepCard:
        """Create an attack reaction card for testing."""
        return ReactionStepCard(name=name, card_type="attack_reaction")

    def create_defense_reaction_card(self, name: str) -> ReactionStepCard:
        """Create a defense reaction card for testing."""
        return ReactionStepCard(name=name, card_type="defense_reaction")

    def create_permanent_with_attack_reaction_ability(self, name: str) -> ReactionStepPermanent:
        """Create a permanent with an attack reaction activated ability."""
        return ReactionStepPermanent(name=name, ability_type="attack_reaction")

    def create_permanent_with_defense_reaction_ability(self, name: str) -> ReactionStepPermanent:
        """Create a permanent with a defense reaction activated ability."""
        return ReactionStepPermanent(name=name, ability_type="defense_reaction")

    def attempt_play_reaction(
        self,
        player: str,
        card: ReactionStepCard,
        current_step: str,
        attack_controller: str,
        attack_targets: list,
        attack_target_controller: str = None,
    ) -> ReactionPlayResult:
        """
        Rule 7.4.2a/b: Attempt to play a reaction card.

        Engine Feature Needed:
        - AttackReaction.can_be_played(player, combat_state)
        - DefenseReaction.can_be_played(player, combat_state)
        """
        # Rule 7.4.2a/b: Reactions can only be played during the Reaction Step
        if current_step != "reaction":
            return ReactionPlayResult(
                success=False,
                reason=f"reactions can only be played during the Reaction Step, not '{current_step}'",
            )

        if card.is_attack_reaction:
            # Rule 7.4.2a: Only the attack controller may play attack reactions
            if player != attack_controller:
                return ReactionPlayResult(
                    success=False,
                    reason="only the attack controller may play attack reaction cards",
                )
            return ReactionPlayResult(success=True)

        if card.is_defense_reaction:
            # Rule 7.4.2b: Only a player whose hero is an attack-target may play defense reactions
            target_hero = f"{player}_hero"
            if target_hero not in attack_targets:
                return ReactionPlayResult(
                    success=False,
                    reason="only a player whose hero is an attack-target may play defense reactions",
                )
            return ReactionPlayResult(success=True)

        return ReactionPlayResult(success=False, reason="unknown card type")

    def attempt_play_defense_reaction_from_hand(
        self,
        player: str,
        card: ReactionStepCard,
        current_step: str,
        attack_targets: list,
        attack_has_dominate: bool,
        defending_hand_card_count: int,
        attack_target_controller: str = None,
    ) -> ReactionPlayResult:
        """
        Rule 7.4.2c: Attempt to play a defense reaction from hand, checking dominate restriction.

        Engine Feature Needed:
        - DefenseReaction.can_be_played(player, combat_state) with dominate check
        """
        if current_step != "reaction":
            return ReactionPlayResult(
                success=False,
                reason=f"reactions can only be played during the Reaction Step",
            )

        # Rule 7.4.2b: Player's hero must be an attack-target
        target_hero = f"{player}_hero"
        if target_hero not in attack_targets:
            return ReactionPlayResult(
                success=False,
                reason="only a player whose hero is an attack-target may play defense reactions",
            )

        # Rule 7.4.2c: Defense reaction from hand blocked by dominate if hand card already defends
        if attack_has_dominate and defending_hand_card_count >= 1:
            return ReactionPlayResult(
                success=False,
                reason="dominate prevents defending with an additional card from hand",
            )

        return ReactionPlayResult(success=True)

    def attempt_activate_reaction_ability(
        self,
        player: str,
        permanent: ReactionStepPermanent,
        current_step: str,
        attack_controller: str = None,
        attack_targets: list = None,
        attack_target_controller: str = None,
    ) -> ReactionActivationResult:
        """
        Rule 7.4.2a/b: Attempt to activate a reaction ability.

        Engine Feature Needed:
        - AttackReaction.can_be_activated(player, combat_state)
        - DefenseReaction.can_be_activated(player, combat_state)
        """
        if attack_targets is None:
            attack_targets = []

        if current_step != "reaction":
            return ReactionActivationResult(
                success=False,
                reason=f"reaction abilities can only be activated during the Reaction Step",
            )

        if permanent.ability_type == "attack_reaction":
            if player != attack_controller:
                return ReactionActivationResult(
                    success=False,
                    reason="only the attack controller may activate attack reaction abilities",
                )
            return ReactionActivationResult(success=True)

        if permanent.ability_type == "defense_reaction":
            target_hero = f"{player}_hero"
            if target_hero not in attack_targets:
                return ReactionActivationResult(
                    success=False,
                    reason="only a player whose hero is an attack-target may activate defense reaction abilities",
                )
            return ReactionActivationResult(success=True)

        return ReactionActivationResult(success=False, reason="unknown ability type")

    def resolve_defense_reaction(
        self,
        card: ReactionStepCard,
        attack_has_dominate: bool,
        defending_hand_card_count: int,
    ) -> DefenseReactionResolveResult:
        """
        Rule 7.4.2d: Resolve a defense reaction card.

        Engine Feature Needed:
        - DefenseReaction.resolve(chain_link) -> ResolveResult
        - ChainLink.add_defending_card(card)
        """
        # Rule 7.4.2d: Defense reaction fails if it cannot become a defending card
        # Dominate prevents more than 1 card from hand defending
        if attack_has_dominate and defending_hand_card_count >= 1 and card.from_hand:
            return DefenseReactionResolveResult(
                became_defending=False,
                failed=True,
                controller_hero="",
            )

        # Successfully becomes a defending card
        self.chain_link_defending_cards.append(card)
        return DefenseReactionResolveResult(
            became_defending=True,
            failed=False,
            controller_hero="player_b_hero",
        )
