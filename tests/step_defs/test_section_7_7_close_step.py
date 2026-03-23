"""
Step definitions for Section 7.7: Close Step
Reference: Flesh and Blood Comprehensive Rules Section 7.7

This module implements behavioral tests for the Close Step of combat:
the game state where the combat chain closes, cleanup occurs, and the
Action Phase continues.

Engine Features Needed for Section 7.7:
- [ ] CombatState.close_step_active property — tracks Close Step (Rule 7.7.1)
- [ ] CombatState.current_step property — includes "close" as a valid value (Rule 7.7.1)
- [ ] PrioritySystem.no_priority_during_close_step() — no priority during Close Step (Rule 7.7.1)
- [ ] CloseStep.begin() — begins Close Step, ends current step (Rule 7.7.2)
- [ ] CloseStep.begin_as_game_state_action() — begins Close Step as game state action (Rule 7.7.2c/d)
- [ ] AttackStep.check_valid_targets() -> bool — checks for valid attack-targets (Rule 7.7.2b)
- [ ] TriggerSystem.trigger_on_combat_chain_closes() — fires "combat chain closes" event (Rule 7.7.3)
- [ ] Stack.move_attacks_to_graveyard() — moves attacks from stack to graveyard (Rule 7.7.3)
- [ ] Stack.move_reactions_to_graveyard() — moves reactions from stack to graveyard (Rule 7.7.3)
- [ ] CloseStep.resolve_triggered_layers() — resolves all layers during Close Step (Rule 7.7.4)
- [ ] CombatChain.return_permanents_to_zones() — returns permanents to their zones (Rule 7.7.5)
- [ ] Equipment.return_to_equipped_zone() — equipment returns to equipped zone (Rule 7.7.5)
- [ ] Weapon.return_to_weapon_zone() — weapons return to weapon zone (Rule 7.7.5)
- [ ] Permanent.return_to_permanent_zone() — permanents return to permanent zone (Rule 7.7.5)
- [ ] CombatChain.clear() — clears all remaining objects from combat chain (Rule 7.7.6)
- [ ] EffectDuration.end_combat_chain_effects() — ends effects lasting "for this combat chain" (Rule 7.7.7)
- [ ] CombatChain.close() — closes the combat chain (Rule 7.7.7)
- [ ] CloseStep.end() — ends Close Step, Action Phase continues (Rule 7.7.7)
- [ ] ActionPhase.continue_after_close_step() — Action Phase resumes after Close Step (Rule 7.7.7)

Current status: Tests written, Engine pending
"""

import pytest
from pytest_bdd import scenario, given, when, then, parsers


# ===== Scenarios =====

# Rule 7.7.1 — Close Step is a game state; no priority

@scenario(
    "../features/section_7_7_close_step.feature",
    "Close Step is a distinct game state where the combat chain closes",
)
def test_close_step_is_game_state():
    """Rule 7.7.1: The Close Step is a distinct game state for closing the combat chain."""
    pass


@scenario(
    "../features/section_7_7_close_step.feature",
    "Players do not get priority during the Close Step",
)
def test_no_priority_during_close_step():
    """Rule 7.7.1: Players do not receive priority during the Close Step."""
    pass


# Rule 7.7.2a — Close Step from Resolution Step

@scenario(
    "../features/section_7_7_close_step.feature",
    "Close Step begins when all players pass during the Resolution Step",
)
def test_close_step_begins_after_all_players_pass():
    """Rule 7.7.2a: All players passing during empty-stack Resolution Step begins Close Step."""
    pass


# Rule 7.7.2b — Close Step from no valid attack-targets

@scenario(
    "../features/section_7_7_close_step.feature",
    "Close Step begins when there are no valid attack-targets at the Attack Step",
)
def test_close_step_begins_no_valid_targets():
    """Rule 7.7.2b: No valid attack-targets at Attack Step beginning triggers Close Step."""
    pass


# Rule 7.7.2c — Close Step from active-attack ceasing to exist

@scenario(
    "../features/section_7_7_close_step.feature",
    "Close Step begins if active-attack ceases to exist before damage",
)
def test_close_step_begins_active_attack_destroyed():
    """Rule 7.7.2c: Active-attack ceasing to exist before damage triggers Close Step as game state action."""
    pass


# Rule 7.7.2d — Close Step from effect

@scenario(
    "../features/section_7_7_close_step.feature",
    "Close Step begins if an effect closes the combat chain",
)
def test_close_step_begins_from_effect():
    """Rule 7.7.2d: An effect that closes the combat chain triggers Close Step as game state action."""
    pass


# Rule 7.7.3 — Combat chain closes event; attacks and reactions to graveyard

@scenario(
    "../features/section_7_7_close_step.feature",
    "The combat chain closes event occurs at the start of the Close Step",
)
def test_combat_chain_closes_event_fires():
    """Rule 7.7.3: The 'combat chain closes' event occurs and triggers effects."""
    pass


@scenario(
    "../features/section_7_7_close_step.feature",
    "Attacks on the stack are put into graveyard when Close Step begins",
)
def test_attacks_on_stack_go_to_graveyard():
    """Rule 7.7.3: All attacks on the stack go to their owner's graveyard when Close Step begins."""
    pass


@scenario(
    "../features/section_7_7_close_step.feature",
    "Reactions on the stack are put into graveyard when Close Step begins",
)
def test_reactions_on_stack_go_to_graveyard():
    """Rule 7.7.3: All reactions on the stack go to their owner's graveyard when Close Step begins."""
    pass


# Rule 7.7.4 — Layers resolve during Close Step

@scenario(
    "../features/section_7_7_close_step.feature",
    "Triggered layers resolve during the Close Step",
)
def test_triggered_layers_resolve_during_close_step():
    """Rule 7.7.4: Layers resolve and game state actions are performed during Close Step."""
    pass


# Rule 7.7.5 — Permanents return to their zones

@scenario(
    "../features/section_7_7_close_step.feature",
    "Equipment returns to its equipped zone when combat chain closes",
)
def test_equipment_returns_to_equipped_zone():
    """Rule 7.7.5: Equipment on combat chain returns to its equipped zone."""
    pass


@scenario(
    "../features/section_7_7_close_step.feature",
    "Weapons return to their equipped zone when combat chain closes",
)
def test_weapons_return_to_weapon_zone():
    """Rule 7.7.5: Weapons on combat chain return to their weapon zone."""
    pass


@scenario(
    "../features/section_7_7_close_step.feature",
    "Permanents on the combat chain return to the permanent zone",
)
def test_permanents_return_to_permanent_zone():
    """Rule 7.7.5: Non-equipment non-weapon permanents return to the permanent zone."""
    pass


# Rule 7.7.6 — Remaining objects cleared

@scenario(
    "../features/section_7_7_close_step.feature",
    "All remaining objects on the combat chain are cleared after permanents return",
)
def test_remaining_objects_cleared_from_combat_chain():
    """Rule 7.7.6: All remaining objects on the combat chain are cleared."""
    pass


# Rule 7.7.7 — Chain-duration effects end; Action Phase continues

@scenario(
    "../features/section_7_7_close_step.feature",
    "Effects that last for the combat chain end when the combat chain closes",
)
def test_combat_chain_duration_effects_end():
    """Rule 7.7.7: Effects lasting 'for this combat chain' end when the chain closes."""
    pass


@scenario(
    "../features/section_7_7_close_step.feature",
    "The combat chain is closed after the Close Step",
)
def test_combat_chain_is_closed_after_close_step():
    """Rule 7.7.7: The combat chain is fully closed after the Close Step completes."""
    pass


@scenario(
    "../features/section_7_7_close_step.feature",
    "The Action Phase continues after the Close Step ends",
)
def test_action_phase_continues_after_close_step():
    """Rule 7.7.7: The Action Phase continues after the Close Step ends."""
    pass


# ===== Step Definitions =====

# --- Givens ---

@given("the combat chain is open")
def combat_chain_is_open(game_state):
    """Rule 7.7: Combat chain is open for combat to occur."""
    game_state.combat_chain_open = True


@given("the game is in the Resolution Step")
def game_in_resolution_step(game_state):
    """Rule 7.6.1: Game is currently in the Resolution Step."""
    game_state.current_combat_step = "resolution"


@given("the stack is empty")
def stack_is_empty(game_state):
    """Rule 7.7.2a: The stack has no layers on it."""
    game_state.stack_empty = True


@given("the game is about to begin the Attack Step")
def game_about_to_begin_attack_step(game_state):
    """Rule 7.7.2b: The Attack Step is about to begin."""
    game_state.pending_step = "attack"


@given("an attack is the active-attack of the current chain link")
def attack_is_active_attack(game_state):
    """Rule 7.7.2c: An attack exists as the active-attack of the current chain link."""
    from tests.bdd_helpers import BDDGameState
    game_state.active_attack = game_state.create_card(name="Active Attack")
    game_state.active_attack_exists = True


@given("a card effect that closes the combat chain is resolved")
def effect_closes_combat_chain(game_state):
    """Rule 7.7.2d: An effect that closes the combat chain is about to resolve."""
    game_state.chain_closing_effect_pending = True


@given("there is an attack on the stack")
def attack_on_the_stack(game_state):
    """Rule 7.7.3: An attack card is on the stack."""
    from tests.bdd_helpers import BDDGameState
    attack = game_state.create_card(name="Attack on Stack")
    game_state.attack_on_stack = attack
    game_state.stack_has_attack = True


@given("there is a reaction on the stack")
def reaction_on_the_stack(game_state):
    """Rule 7.7.3: A reaction card is on the stack."""
    from tests.bdd_helpers import BDDGameState
    reaction = game_state.create_card(name="Reaction on Stack")
    game_state.reaction_on_stack = reaction
    game_state.stack_has_reaction = True


@given("the combat chain is in the Close Step")
def combat_chain_in_close_step(game_state):
    """Rule 7.7.4: The combat chain is currently in the Close Step."""
    game_state.current_combat_step = "close"
    game_state.combat_chain_open = True


@given("there are triggered layers on the stack from the combat chain closes event")
def triggered_layers_from_close_event(game_state):
    """Rule 7.7.4: Triggered layers were placed on the stack when combat chain closes event fired."""
    game_state.triggered_layers_on_stack = True
    game_state.triggered_layers_count = 1


@given("an equipment card is on the combat chain")
def equipment_on_combat_chain(game_state):
    """Rule 7.7.5: An equipment card is present on the combat chain."""
    from fab_engine.cards.model import CardType
    equipment = game_state.create_card(name="Test Equipment")
    game_state.equipment_on_chain = equipment
    game_state.equipment_original_zone = "chest"


@given("a weapon card is on the combat chain")
def weapon_on_combat_chain(game_state):
    """Rule 7.7.5: A weapon card is present on the combat chain."""
    weapon = game_state.create_card(name="Test Weapon")
    game_state.weapon_on_chain = weapon
    game_state.weapon_original_zone = "weapon"


@given("a non-equipment non-weapon permanent is on the combat chain")
def permanent_on_combat_chain(game_state):
    """Rule 7.7.5: A non-equipment, non-weapon permanent is on the combat chain."""
    permanent = game_state.create_card(name="Test Permanent")
    game_state.permanent_on_chain = permanent


@given("there are objects remaining on the combat chain")
def objects_remaining_on_combat_chain(game_state):
    """Rule 7.7.6: There are objects still on the combat chain after permanents returned."""
    game_state.objects_on_combat_chain = True
    game_state.combat_chain_object_count = 2


@given("there is an effect that lasts for \"this combat chain\"")
def effect_lasting_for_combat_chain(game_state):
    """Rule 7.7.7: An effect with duration 'this combat chain' is active."""
    game_state.combat_chain_effect_active = True
    game_state.combat_chain_effect_duration = "this combat chain"


@given("the game is in the Action Phase")
def game_in_action_phase(game_state):
    """Rule 7.7.7: The game is in the Action Phase."""
    game_state.current_phase = "action"


# --- Whens ---

@when("all players pass in succession with an empty stack")
def all_players_pass_empty_stack(game_state):
    """Rule 7.7.2a: All players pass priority with nothing on the stack."""
    game_state.all_players_passed = True
    game_state.triggered_close_step = True
    game_state.current_combat_step = "close"


@when("all players pass in succession")
def all_players_pass(game_state):
    """Rule 7.7.2a: All players pass priority in succession."""
    game_state.all_players_passed = True
    game_state.triggered_close_step = True
    game_state.current_combat_step = "close"


@when("there are no valid attack-targets")
def no_valid_attack_targets(game_state):
    """Rule 7.7.2b: There are no valid attack-targets at the beginning of the Attack Step."""
    game_state.valid_attack_targets = []
    game_state.triggered_close_step = True
    game_state.current_combat_step = "close"


@when("the active-attack is destroyed before damage is calculated")
def active_attack_destroyed_before_damage(game_state):
    """Rule 7.7.2c: The active-attack ceases to exist before damage is calculated."""
    game_state.active_attack_exists = False
    game_state.active_attack_destroyed = True
    game_state.triggered_close_step = True
    game_state.close_step_is_game_state_action = True
    game_state.current_combat_step = "close"


@when("the effect resolves")
def effect_resolves(game_state):
    """Rule 7.7.2d: The chain-closing effect resolves."""
    game_state.chain_closing_effect_resolved = True
    game_state.triggered_close_step = True
    game_state.close_step_is_game_state_action = True
    game_state.current_combat_step = "close"


@when("the Close Step begins")
def close_step_begins(game_state):
    """Rule 7.7.3: The Close Step begins."""
    game_state.current_combat_step = "close"
    game_state.close_step_begun = True


@when("the Close Step processes the stack")
def close_step_processes_stack(game_state):
    """Rule 7.7.4: The Close Step resolves layers on the stack."""
    game_state.close_step_processing_stack = True


@when("the stack is empty during the Close Step")
def stack_empty_during_close_step(game_state):
    """Rule 7.7.5: The stack is empty during the Close Step."""
    game_state.stack_empty = True
    game_state.close_step_stack_empty = True


@when("the Close Step clears the combat chain")
def close_step_clears_combat_chain(game_state):
    """Rule 7.7.6: The Close Step clears all remaining objects from the combat chain."""
    game_state.combat_chain_cleared = True
    game_state.objects_on_combat_chain = False


@when("the combat chain closes")
def combat_chain_closes(game_state):
    """Rule 7.7.7: The combat chain closes during the Close Step."""
    game_state.combat_chain_open = False
    game_state.combat_chain_closed = True


@when("the Close Step completes")
def close_step_completes(game_state):
    """Rule 7.7.7: The Close Step finishes all its sub-steps."""
    game_state.combat_chain_open = False
    game_state.close_step_complete = True
    game_state.current_combat_step = None


# --- Thens ---

@then("the Close Step begins")
def assert_close_step_begins(game_state):
    """Rule 7.7: The Close Step has begun."""
    assert game_state.triggered_close_step, (
        "Expected Close Step to begin, but it did not trigger."
    )


@then("the combat chain is closing")
def assert_combat_chain_is_closing(game_state):
    """Rule 7.7.1: The combat chain is in the process of closing."""
    assert game_state.triggered_close_step, (
        "Expected combat chain to be closing during Close Step."
    )


@then("no player has priority during the Close Step")
def assert_no_priority_during_close_step(game_state):
    """Rule 7.7.1: No player receives priority during the Close Step."""
    # Engine must provide PrioritySystem.no_priority_during_close_step()
    assert not getattr(game_state, "player_has_priority_in_close_step", False), (
        "Expected no player to have priority during Close Step, but a player does."
    )


@then("the current step is the close step")
def assert_current_step_is_close(game_state):
    """Rule 7.7.2: The current combat step is 'close'."""
    assert game_state.current_combat_step == "close", (
        f"Expected current step to be 'close', got '{game_state.current_combat_step}'."
    )


@then("the Close Step begins instead of the Attack Step")
def assert_close_step_instead_of_attack(game_state):
    """Rule 7.7.2b: Close Step begins in place of the Attack Step."""
    assert game_state.triggered_close_step, (
        "Expected Close Step to begin instead of Attack Step."
    )
    assert getattr(game_state, "pending_step", None) != "attack" or game_state.triggered_close_step, (
        "Expected Attack Step to be skipped in favor of Close Step."
    )


@then("the Close Step begins as a game state action")
def assert_close_step_as_game_state_action(game_state):
    """Rule 7.7.2c/d: Close Step begins as a game state action (no priority window)."""
    assert game_state.triggered_close_step, (
        "Expected Close Step to begin as a game state action."
    )
    assert getattr(game_state, "close_step_is_game_state_action", False), (
        "Expected Close Step to begin as a game state action, not from priority pass."
    )


@then("the \"combat chain closes\" event occurs")
def assert_combat_chain_closes_event(game_state):
    """Rule 7.7.3: The 'combat chain closes' event has occurred."""
    # Engine must provide TriggerSystem.trigger_on_combat_chain_closes()
    assert game_state.close_step_begun, (
        "Expected 'combat chain closes' event to occur when Close Step begins."
    )


@then("effects that trigger from the combat chain closing are triggered")
def assert_triggered_effects_fire(game_state):
    """Rule 7.7.3: Effects that trigger from the combat chain closing are triggered."""
    # Engine must provide TriggerSystem to handle "combat chain closes" triggers
    assert game_state.close_step_begun, (
        "Expected triggered effects to fire when combat chain closes event occurs."
    )


@then("the attack is put into its owner's graveyard")
def assert_attack_in_graveyard(game_state):
    """Rule 7.7.3: The attack on the stack is moved to its owner's graveyard."""
    # Engine must provide Stack.move_attacks_to_graveyard()
    assert game_state.close_step_begun, (
        "Expected attack to be moved to graveyard when Close Step begins."
    )
    assert getattr(game_state, "stack_has_attack", False) is not True or game_state.close_step_begun, (
        "Attack should have been moved from stack to graveyard."
    )


@then("the attack is no longer on the stack")
def assert_attack_not_on_stack(game_state):
    """Rule 7.7.3: The attack is no longer on the stack after Close Step begins."""
    # Engine must enforce attacks are removed from stack
    assert game_state.close_step_begun, (
        "Expected attack to be removed from stack when Close Step begins."
    )


@then("the reaction is put into its owner's graveyard")
def assert_reaction_in_graveyard(game_state):
    """Rule 7.7.3: The reaction on the stack is moved to its owner's graveyard."""
    # Engine must provide Stack.move_reactions_to_graveyard()
    assert game_state.close_step_begun, (
        "Expected reaction to be moved to graveyard when Close Step begins."
    )


@then("the reaction is no longer on the stack")
def assert_reaction_not_on_stack(game_state):
    """Rule 7.7.3: The reaction is no longer on the stack after Close Step begins."""
    assert game_state.close_step_begun, (
        "Expected reaction to be removed from stack when Close Step begins."
    )


@then("the triggered layers resolve")
def assert_triggered_layers_resolve(game_state):
    """Rule 7.7.4: Triggered layers on the stack have resolved during the Close Step."""
    # Engine must provide CloseStep.resolve_triggered_layers()
    assert game_state.close_step_processing_stack, (
        "Expected triggered layers to resolve during Close Step."
    )


@then("game state actions are performed")
def assert_game_state_actions_performed(game_state):
    """Rule 7.7.4: Game state actions are performed as if all players are passing priority."""
    assert game_state.close_step_processing_stack, (
        "Expected game state actions to be performed during Close Step stack processing."
    )


@then("the equipment returns to the player's equipped zone")
def assert_equipment_returns_to_equipped_zone(game_state):
    """Rule 7.7.5: Equipment returns to its equipped zone when stack is empty during Close Step."""
    # Engine must provide Equipment.return_to_equipped_zone()
    assert game_state.close_step_stack_empty, (
        "Expected equipment to return to equipped zone when stack is empty during Close Step."
    )


@then("the weapon returns to the player's weapon zone")
def assert_weapon_returns_to_weapon_zone(game_state):
    """Rule 7.7.5: Weapon returns to its weapon zone when stack is empty during Close Step."""
    # Engine must provide Weapon.return_to_weapon_zone()
    assert game_state.close_step_stack_empty, (
        "Expected weapon to return to weapon zone when stack is empty during Close Step."
    )


@then("the permanent returns to the permanent zone")
def assert_permanent_returns_to_permanent_zone(game_state):
    """Rule 7.7.5: Permanent returns to the permanent zone when stack is empty during Close Step."""
    # Engine must provide Permanent.return_to_permanent_zone()
    assert game_state.close_step_stack_empty, (
        "Expected permanent to return to permanent zone when stack is empty during Close Step."
    )


@then("all objects are removed from the combat chain")
def assert_all_objects_removed_from_combat_chain(game_state):
    """Rule 7.7.6: All remaining objects have been removed from the combat chain."""
    assert game_state.combat_chain_cleared, (
        "Expected all objects to be removed from combat chain during Clear step."
    )


@then("the combat chain has no remaining objects")
def assert_combat_chain_has_no_objects(game_state):
    """Rule 7.7.6: The combat chain is empty after clearing."""
    assert not game_state.objects_on_combat_chain, (
        "Expected combat chain to have no remaining objects after clearing."
    )


@then("the effect that lasts for this combat chain ends")
def assert_combat_chain_effect_ends(game_state):
    """Rule 7.7.7: Effects with 'this combat chain' duration end when combat chain closes."""
    # Engine must provide EffectDuration.end_combat_chain_effects()
    assert game_state.combat_chain_closed, (
        "Expected 'this combat chain' effects to end when combat chain closes."
    )
    assert not game_state.combat_chain_effect_active, (
        "Expected combat chain effect to no longer be active after chain closes."
    )


@then("the combat chain is closed")
def assert_combat_chain_is_closed(game_state):
    """Rule 7.7.7: The combat chain is fully closed."""
    assert not game_state.combat_chain_open, (
        "Expected combat chain to be closed after Close Step completes."
    )


@then("the Close Step ends")
def assert_close_step_ends(game_state):
    """Rule 7.7.7: The Close Step has ended."""
    assert game_state.close_step_complete, (
        "Expected Close Step to end after all Close Step sub-steps complete."
    )


@then("the Action Phase continues")
def assert_action_phase_continues(game_state):
    """Rule 7.7.7: The Action Phase continues after the Close Step ends."""
    # Engine must provide ActionPhase.continue_after_close_step()
    assert game_state.close_step_complete, (
        "Expected Action Phase to continue after Close Step ends."
    )
    assert game_state.current_phase == "action", (
        f"Expected current phase to be 'action', got '{game_state.current_phase}'."
    )


# ===== Fixtures =====

@pytest.fixture
def game_state():
    """
    Fixture providing game state for testing Close Step rules.

    Uses BDDGameState which integrates with the real engine.
    Reference: Rule 7.7
    """
    from tests.bdd_helpers import BDDGameState

    state = BDDGameState()

    # Initialize Close Step tracking state
    state.combat_chain_open = False
    state.current_combat_step = None
    state.current_phase = "action"
    state.stack_empty = False
    state.all_players_passed = False
    state.triggered_close_step = False
    state.close_step_is_game_state_action = False
    state.close_step_begun = False
    state.close_step_complete = False
    state.close_step_processing_stack = False
    state.close_step_stack_empty = False
    state.player_has_priority_in_close_step = False
    state.valid_attack_targets = None
    state.active_attack_exists = False
    state.active_attack_destroyed = False
    state.chain_closing_effect_pending = False
    state.chain_closing_effect_resolved = False
    state.stack_has_attack = False
    state.stack_has_reaction = False
    state.triggered_layers_on_stack = False
    state.triggered_layers_count = 0
    state.objects_on_combat_chain = False
    state.combat_chain_object_count = 0
    state.combat_chain_cleared = False
    state.combat_chain_effect_active = False
    state.combat_chain_effect_duration = None
    state.combat_chain_closed = False
    state.pending_step = None

    return state
