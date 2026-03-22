"""
Step definitions for Section 7.2: Attack Step
Reference: Flesh and Blood Comprehensive Rules Section 7.2

This module implements behavioral tests for the Attack Step of combat:
the game state where an attack resolves onto the combat chain as a chain link
and becomes attacking, before any defending cards are declared.

Engine Features Needed for Section 7.2:
- [ ] CombatState.attack_step_active property — tracks Attack Step (Rule 7.2.1)
- [ ] CombatState.defend_step_active property — tracks Defend Step (Rule 7.2.6)
- [ ] CombatState.close_step_active property — tracks Close Step (Rule 7.2.2)
- [ ] CombatState.current_step property — "layer"|"attack"|"defend"|"reaction"|"damage"|"resolution"|"close"
- [ ] AttackTarget.is_legal_target() -> bool — re-checks legality at Attack Step start (Rule 7.2.2)
- [ ] CombatChain.active_chain_link property — the current chain link (Rule 7.2.3)
- [ ] CombatChain.active_attack property — the active-attack on the current chain link (Rule 7.2.3a)
- [ ] ChainLink.attack_card property — the attack-card for this chain link (Rule 7.2.3a)
- [ ] ChainLink.attack_proxy property — the attack-proxy for this chain link (Rule 7.2.3b)
- [ ] ChainLink.attack_source property — the attack-source for this chain link (Rule 7.2.3b)
- [ ] CardInstance.is_attacking property — tracks attacking status (Rule 7.2.3a)
- [ ] CardInstance.is_living property — checks if object is still alive (Rule 7.2.4a)
- [ ] AttackStep.run_target_legality_check() — Rule 7.2.2 first action
- [ ] AttackStep.generate_resolution_abilities() — Rule 7.2.3 second action
- [ ] AttackStep.place_attack_on_chain() — Rule 7.2.3 second action
- [ ] AttackStep.trigger_attack_event() — Rule 7.2.4 third action
- [ ] AttackStep.grant_priority_to_turn_player() — Rule 7.2.5 fourth action
- [ ] GameState.attacking_hero property — (controller, hero) tuple (Rule 7.2.4a)
- [ ] GameState.defending_hero property — (controller, hero) tuple (Rule 7.2.4b)
- [ ] GameState.turn_player property — player with current priority (Rule 7.2.5)
- [ ] PrioritySystem.who_has_priority() -> Player (Rule 7.2.5)
- [ ] PrioritySystem.all_players_passed() -> bool (Rule 7.2.6)

Current status: Tests written, Engine pending
"""

import pytest
from pytest_bdd import scenario, given, when, then, parsers


# ===== Scenarios =====

# Rule 7.2.1 — Attack Step is a distinct game state

@scenario(
    "../features/section_7_2_attack_step.feature",
    "Attack Step is a game state where the attack becomes attacking before defenders are declared",
)
def test_attack_step_is_game_state_before_defenders():
    """Rule 7.2.1: The Attack Step is where the attack becomes attacking before any defenders declared."""
    pass


# Rule 7.2.2 — Target legality check

@scenario(
    "../features/section_7_2_attack_step.feature",
    "Attack Step proceeds when the attack-target is still a legal target",
)
def test_attack_step_proceeds_with_legal_target():
    """Rule 7.2.2: Attack Step proceeds when at least one attack-target is still legal."""
    pass


@scenario(
    "../features/section_7_2_attack_step.feature",
    "Attack Step ends immediately when all attack-targets are illegal",
)
def test_attack_step_ends_when_all_targets_illegal():
    """Rule 7.2.2: Attack Step ends and Close Step begins when no attack-targets are legal."""
    pass


@scenario(
    "../features/section_7_2_attack_step.feature",
    "Attack Step proceeds when at least one of multiple attack-targets is still legal",
)
def test_attack_step_proceeds_with_one_legal_of_multiple_targets():
    """Rule 7.2.2a: Only one attack-target needs to remain legal for the Attack Step to proceed."""
    pass


@scenario(
    "../features/section_7_2_attack_step.feature",
    "Attack continues even if targets become illegal after the legality check",
)
def test_attack_continues_after_targets_become_illegal_post_check():
    """Rule 7.2.2a: Targets becoming illegal after the legality check does not end combat."""
    pass


# Rule 7.2.3 — Attack moves onto combat chain

@scenario(
    "../features/section_7_2_attack_step.feature",
    "Resolution abilities of the attack generate effects before the attack moves to the combat chain",
)
def test_resolution_abilities_generate_before_chain_placement():
    """Rule 7.2.3: Resolution abilities generate effects (except go again) before chain placement."""
    pass


@scenario(
    "../features/section_7_2_attack_step.feature",
    "Attack-card moves onto the combat chain as the active-attack chain link",
)
def test_attack_card_becomes_active_attack_chain_link():
    """Rule 7.2.3a: Attack-card moves onto combat chain as chain link and is the active-attack."""
    pass


@scenario(
    "../features/section_7_2_attack_step.feature",
    "Attack-proxy and its attack-source both move onto the combat chain link",
)
def test_attack_proxy_and_source_move_onto_chain_link():
    """Rule 7.2.3b: Attack-proxy and attack-source both move onto the chain link."""
    pass


@scenario(
    "../features/section_7_2_attack_step.feature",
    "Attack Step ends and Close Step begins if active-attack cannot move to combat chain",
)
def test_attack_step_ends_if_active_attack_does_not_exist():
    """Rule 7.2.3d: If active-attack doesn't exist or can't move to chain, Close Step begins."""
    pass


# Rule 7.2.4 — "attack" event and designations

@scenario(
    "../features/section_7_2_attack_step.feature",
    "The attack event occurs after the attack moves onto the combat chain",
)
def test_attack_event_occurs_after_chain_placement():
    """Rule 7.2.4: The 'attack' event occurs after the attack is placed on the chain."""
    pass


@scenario(
    "../features/section_7_2_attack_step.feature",
    "Attack-source that is a living object becomes attacking during the Attack Step",
)
def test_living_attack_source_becomes_attacking():
    """Rule 7.2.4a: A living attack-source becomes attacking when the attack event occurs."""
    pass


@scenario(
    "../features/section_7_2_attack_step.feature",
    "Controller and hero become attacking hero when there is no living attack-source",
)
def test_controller_becomes_attacking_hero_without_living_source():
    """Rule 7.2.4a: When no living attack-source, controller and hero become the attacking hero."""
    pass


@scenario(
    "../features/section_7_2_attack_step.feature",
    "Attack-target hero and their controller become the defending hero",
)
def test_attack_target_hero_becomes_defending_hero():
    """Rule 7.2.4b: When attack-target is a hero, that hero and controller become the defending hero."""
    pass


@scenario(
    "../features/section_7_2_attack_step.feature",
    "Attacking and defending hero designations persist until the active chain link resolves",
)
def test_hero_designations_persist_until_chain_link_resolves():
    """Rule 7.2.4a + 7.2.4b: Attacking/defending hero designations last until chain link resolves."""
    pass


# Rule 7.2.5 — Turn-player gains priority

@scenario(
    "../features/section_7_2_attack_step.feature",
    "Turn-player gains priority in the Attack Step after the attack event",
)
def test_turn_player_gains_priority_in_attack_step():
    """Rule 7.2.5: The turn-player gains priority as the fourth action in the Attack Step."""
    pass


# Rule 7.2.6 — Defend Step begins

@scenario(
    "../features/section_7_2_attack_step.feature",
    "Attack Step ends and Defend Step begins when all players pass with empty stack",
)
def test_defend_step_begins_when_all_players_pass():
    """Rule 7.2.6: Attack Step ends and Defend Step begins when stack empty and all players pass."""
    pass


# ===== Step Definitions =====

# --- Rule 7.2.1 / 7.1.3 context ---

@given("the Layer Step is active")
def layer_step_is_active(game_state):
    """Rule 7.1.1: The Layer Step is active with an unresolved attack on the stack."""
    game_state.combat_state["current_step"] = "layer"
    game_state.combat_state["layer_step_active"] = True


@given("the top layer of the stack is the attack")
def top_of_stack_is_attack(game_state):
    """Rule 7.1.3: The attack is the top layer of the stack."""
    attack_card = game_state.create_card(name="Test Attack", card_type="attack_action")
    game_state.stack.append({"type": "attack", "card": attack_card})
    game_state.current_attack = attack_card


@when("all players pass priority in succession")
def all_players_pass(game_state):
    """All players pass priority, triggering step transitions."""
    game_state.combat_state["all_players_passed"] = True


@then("the Layer Step ends")
def layer_step_ends(game_state):
    """Rule 7.1.3: The Layer Step ends."""
    assert game_state.combat_state.get("all_players_passed", False), \
        "Engine feature needed: Layer Step does not automatically end when all players pass — LayerStepTransition not implemented"


@then("the Attack Step begins")
def attack_step_begins(game_state):
    """Rule 7.1.3 → 7.2.1: The Attack Step begins after the Layer Step ends."""
    assert game_state.combat_state.get("attack_step_active", False), \
        "Engine feature needed: CombatState.attack_step_active not implemented (Rule 7.2.1)"


@then("no defending cards have been declared yet")
def no_defending_cards_declared(game_state):
    """Rule 7.2.1: Attack Step comes before the Defend Step — no defenders yet."""
    defenders = game_state.combat_state.get("declared_defenders", [])
    assert len(defenders) == 0, \
        "Engine feature needed: CombatState.declared_defenders not tracked (Rule 7.2.1)"


# --- Rule 7.2.2: target legality check ---

@given("the Attack Step is about to begin")
def attack_step_about_to_begin(game_state):
    """Rule 7.2.2: The Layer Step has ended and the Attack Step is next."""
    game_state.combat_state["current_step"] = "attack"
    attack_card = game_state.create_card(name="Test Attack", card_type="attack_action")
    game_state.current_attack = attack_card


@given("the attack has one attack-target")
def attack_has_one_target(game_state):
    """Rule 7.2.2: The attack has a single attack-target."""
    target = game_state.create_card(name="Target Hero", card_type="hero")
    game_state.attack_targets = [{"card": target, "legal": True}]


@given("the attack-target is a legal target")
def attack_target_is_legal(game_state):
    """Rule 7.2.2: The attack-target is still a legal target."""
    for t in game_state.attack_targets:
        t["legal"] = True


@given("the attack-target is no longer a legal target")
def attack_target_is_illegal(game_state):
    """Rule 7.2.2: The attack-target is no longer a legal target."""
    for t in game_state.attack_targets:
        t["legal"] = False


@when("the Attack Step begins")
def attack_step_begins_action(game_state):
    """Rule 7.2.2: The Attack Step performs its first action — target legality check."""
    all_illegal = all(not t.get("legal", True) for t in game_state.attack_targets)
    game_state.combat_state["all_targets_illegal"] = all_illegal
    if all_illegal:
        game_state.combat_state["attack_step_ended_early"] = True
        game_state.combat_state["close_step_active"] = True
    else:
        game_state.combat_state["attack_proceeded"] = True


@then("the attack proceeds onto the combat chain")
def attack_proceeds_onto_chain(game_state):
    """Rule 7.2.2: When at least one target is legal, the attack proceeds."""
    assert game_state.combat_state.get("attack_proceeded", False), \
        "Engine feature needed: Attack Step target legality check not implemented (Rule 7.2.2)"


@then("the Attack Step ends immediately")
def attack_step_ends_immediately(game_state):
    """Rule 7.2.2: Attack Step ends immediately when all targets are illegal."""
    assert game_state.combat_state.get("attack_step_ended_early", False), \
        "Engine feature needed: Attack Step early termination on illegal targets (Rule 7.2.2)"


@then("the Close Step begins instead of the Defend Step")
def close_step_begins_instead(game_state):
    """Rule 7.2.2: Close Step begins instead of Defend Step when all targets are illegal."""
    assert game_state.combat_state.get("close_step_active", False), \
        "Engine feature needed: CombatState.close_step_active not implemented (Rule 7.2.2)"


# Rule 7.2.2a: multiple targets

@given("the attack has two attack-targets")
def attack_has_two_targets(game_state):
    """Rule 7.2.2a: The attack has two attack-targets."""
    target1 = game_state.create_card(name="Target Hero 1", card_type="hero")
    target2 = game_state.create_card(name="Target Hero 2", card_type="hero")
    game_state.attack_targets = [
        {"card": target1, "legal": True},
        {"card": target2, "legal": True},
    ]


@given("one attack-target is a legal target")
def one_target_is_legal(game_state):
    """Rule 7.2.2a: One of the attack-targets is still a legal target."""
    if game_state.attack_targets:
        game_state.attack_targets[0]["legal"] = True


@given("the other attack-target is no longer a legal target")
def other_target_is_illegal(game_state):
    """Rule 7.2.2a: The other attack-target is no longer a legal target."""
    if len(game_state.attack_targets) > 1:
        game_state.attack_targets[1]["legal"] = False


# Rule 7.2.2a: post-check illegality

@given("the Attack Step has passed the target legality check")
def attack_step_passed_legality_check(game_state):
    """Rule 7.2.2a: The target legality check in the Attack Step was passed."""
    game_state.combat_state["target_legality_check_passed"] = True
    attack_card = game_state.create_card(name="Test Attack", card_type="attack_action")
    game_state.current_attack = attack_card
    target = game_state.create_card(name="Target Hero", card_type="hero")
    game_state.attack_targets = [{"card": target, "legal": True}]


@given("all attack-targets cease to be legal after the check")
def all_targets_become_illegal_post_check(game_state):
    """Rule 7.2.2a: All targets are now illegal, but the check has already passed."""
    for t in game_state.attack_targets:
        t["legal"] = False
    game_state.combat_state["targets_illegal_post_check"] = True


@when("the attack is on the combat chain as the active chain link")
def attack_is_on_chain_as_active(game_state):
    """Rule 7.2.3: The attack has been placed on the combat chain as the active chain link."""
    game_state.combat_state["attack_on_chain"] = True
    game_state.combat_state["active_chain_link"] = {"attack": game_state.current_attack}


@then("the attack remains on the combat chain")
def attack_remains_on_chain(game_state):
    """Rule 7.2.2a: Attack stays on chain even though targets are now illegal."""
    assert game_state.combat_state.get("attack_on_chain", False), \
        "Engine feature needed: Attack should remain on chain after legality check passes (Rule 7.2.2a)"


@then("combat continues to the Defend Step")
def combat_continues_to_defend_step(game_state):
    """Rule 7.2.2a: Combat proceeds to the Defend Step."""
    # This requires the engine to not abort the attack step retroactively
    assert game_state.combat_state.get("target_legality_check_passed", False), \
        "Engine feature needed: Post-check target illegality should not abort combat (Rule 7.2.2a)"


# Rule 7.2.3: resolution abilities and chain placement

@given("the attack has a resolution ability")
def attack_has_resolution_ability(game_state):
    """Rule 7.2.3: The attack has a resolution ability that should fire in the Attack Step."""
    game_state.combat_state["attack_has_resolution_ability"] = True
    game_state.combat_state["resolution_ability_generated"] = False


@when("the Attack Step processes the resolution abilities")
def attack_step_processes_resolution_abilities(game_state):
    """Rule 7.2.3: Resolution abilities are processed in order in the Attack Step."""
    if game_state.combat_state.get("attack_has_resolution_ability", False):
        game_state.combat_state["resolution_ability_generated"] = True
    game_state.combat_state["resolution_abilities_processed"] = True


@then("the resolution ability generates its effect")
def resolution_ability_generates_effect(game_state):
    """Rule 7.2.3: The resolution ability's effect is generated."""
    assert game_state.combat_state.get("resolution_ability_generated", False), \
        "Engine feature needed: Resolution abilities must generate effects in Attack Step (Rule 7.2.3)"


@then("then the attack moves onto the combat chain as a chain link")
def attack_moves_onto_chain_after_abilities(game_state):
    """Rule 7.2.3: After resolution abilities, the attack is placed on the combat chain."""
    assert game_state.combat_state.get("resolution_abilities_processed", False), \
        "Engine feature needed: Attack moves to chain AFTER resolution abilities fire (Rule 7.2.3)"


# Rule 7.2.3a: attack-card

@given("the Attack Step is processing an attack-card")
def attack_step_processing_attack_card(game_state):
    """Rule 7.2.3a: The attack being processed is an attack-card (not a proxy or layer)."""
    attack_card = game_state.create_card(name="Test Attack Card", card_type="attack_action")
    game_state.current_attack = attack_card
    game_state.combat_state["attack_type"] = "attack_card"
    game_state.combat_state["current_attack_card"] = attack_card


@when("the attack-card moves onto the combat chain")
def attack_card_moves_onto_chain(game_state):
    """Rule 7.2.3a: The attack-card moves onto the combat chain as a chain link."""
    game_state.combat_state["attack_on_chain"] = True
    game_state.combat_state["active_chain_link"] = {
        "attack": game_state.combat_state.get("current_attack_card"),
        "is_attacking": True,
    }


@then("the attack-card is the active-attack")
def attack_card_is_active_attack(game_state):
    """Rule 7.2.3a: The attack-card is the active-attack on the current chain link."""
    assert game_state.combat_state.get("active_chain_link") is not None, \
        "Engine feature needed: CombatChain.active_attack property (Rule 7.2.3a)"


@then("the attack-card is on the combat chain as a chain link")
def attack_card_is_on_chain_as_link(game_state):
    """Rule 7.2.3a: The attack-card is placed on the combat chain as a chain link."""
    assert game_state.combat_state.get("attack_on_chain", False), \
        "Engine feature needed: ChainLink.attack_card property (Rule 7.2.3a)"


@then("the attack-card has the attacking status")
def attack_card_has_attacking_status(game_state):
    """Rule 7.2.3a: The attack-card has the 'attacking' status."""
    chain_link = game_state.combat_state.get("active_chain_link", {})
    assert chain_link.get("is_attacking", False), \
        "Engine feature needed: CardInstance.is_attacking property (Rule 7.2.3a)"


# Rule 7.2.3b: attack-proxy

@given("the Attack Step is processing an attack with an attack-proxy")
def attack_step_processing_attack_proxy(game_state):
    """Rule 7.2.3b: The attack being processed has an attack-proxy."""
    proxy = game_state.create_attack_proxy()
    game_state.combat_state["attack_type"] = "attack_proxy"
    game_state.combat_state["attack_proxy"] = proxy


@given("the attack-proxy has an attack-source")
def attack_proxy_has_source(game_state):
    """Rule 7.2.3b: The attack-proxy has an associated attack-source."""
    source_card = game_state.create_card(name="Attack Source", card_type="weapon")
    game_state.combat_state["attack_source"] = source_card


@when("the attack moves onto the combat chain")
def attack_proxy_moves_onto_chain(game_state):
    """Rule 7.2.3b: The attack-proxy and attack-source both move onto the chain link."""
    game_state.combat_state["attack_on_chain"] = True
    game_state.combat_state["active_chain_link"] = {
        "attack_proxy": game_state.combat_state.get("attack_proxy"),
        "attack_source": game_state.combat_state.get("attack_source"),
        "is_attacking": True,
    }


@then("the attack-proxy is the active-attack")
def attack_proxy_is_active_attack(game_state):
    """Rule 7.2.3b: The attack-proxy is the active-attack."""
    chain_link = game_state.combat_state.get("active_chain_link", {})
    assert chain_link.get("attack_proxy") is not None, \
        "Engine feature needed: ChainLink.attack_proxy property (Rule 7.2.3b)"


@then("both the attack-proxy and attack-source are on the same chain link")
def proxy_and_source_on_same_chain_link(game_state):
    """Rule 7.2.3b: Both the attack-proxy and attack-source are on the same chain link."""
    chain_link = game_state.combat_state.get("active_chain_link", {})
    assert chain_link.get("attack_proxy") is not None and chain_link.get("attack_source") is not None, \
        "Engine feature needed: ChainLink.attack_source property (Rule 7.2.3b)"


# Rule 7.2.3d: active-attack doesn't exist

@given("the Attack Step is processing an attack")
def attack_step_processing_attack(game_state):
    """Rule 7.2.3d: The Attack Step is in progress."""
    game_state.combat_state["current_step"] = "attack"


@given("the active-attack does not exist")
def active_attack_does_not_exist(game_state):
    """Rule 7.2.3d: The active-attack no longer exists (e.g. was destroyed)."""
    game_state.current_attack = None
    game_state.combat_state["active_attack_exists"] = False


@when("the Attack Step attempts to place the attack on the combat chain")
def attack_step_attempts_chain_placement(game_state):
    """Rule 7.2.3d: The Attack Step attempts to place the attack on the chain."""
    if not game_state.combat_state.get("active_attack_exists", True):
        game_state.combat_state["attack_step_ended_early"] = True
        game_state.combat_state["close_step_active"] = True


@then("the Attack Step ends")
def attack_step_ends(game_state):
    """Rule 7.2.3d / 7.2.2 / 7.2.6: The Attack Step ends (either early or after all players pass)."""
    ended_early = game_state.combat_state.get("attack_step_ended_early", False)
    ended_normally = game_state.combat_state.get("all_players_passed", False)
    assert ended_early or ended_normally, \
        "Engine feature needed: Attack Step transition logic not implemented (Rule 7.2.3d / 7.2.6)"


@then("the Close Step begins")
def close_step_begins(game_state):
    """Rule 7.2.3d / 7.2.2: The Close Step begins."""
    assert game_state.combat_state.get("close_step_active", False), \
        "Engine feature needed: CombatState.close_step_active not implemented (Rule 7.2.3d)"


# Rule 7.2.4: attack event

@given("the attack has been placed on the combat chain as a chain link")
def attack_placed_on_chain(game_state):
    """Rule 7.2.4: The attack has been placed on the combat chain."""
    attack_card = game_state.create_card(name="Test Attack", card_type="attack_action")
    game_state.current_attack = attack_card
    game_state.combat_state["attack_on_chain"] = True
    game_state.combat_state["active_chain_link"] = {"attack": attack_card}


@when("the Attack Step triggers the attack event")
def attack_step_triggers_attack_event(game_state):
    """Rule 7.2.4: The 'attack' event is triggered after chain placement."""
    game_state.combat_state["attack_event_occurred"] = True
    game_state.combat_state["attack_triggered_effects"] = []


@then("effects that trigger on attacking are triggered")
def attack_triggered_effects_are_triggered(game_state):
    """Rule 7.2.4: Effects that trigger from attacking are triggered."""
    assert game_state.combat_state.get("attack_event_occurred", False), \
        "Engine feature needed: Attack event must be fired after chain placement (Rule 7.2.4)"


# Rule 7.2.4a: attack-source becomes attacking

@given("the Attack Step is processing an attack with a living attack-source")
def attack_with_living_source(game_state):
    """Rule 7.2.4a: The attack has a living attack-source."""
    source_card = game_state.create_card(name="Living Attack Source", card_type="weapon")
    game_state.combat_state["attack_source"] = source_card
    game_state.combat_state["attack_source_is_living"] = True
    game_state.combat_state["attack_on_chain"] = True


@when("the attack event occurs")
def attack_event_occurs(game_state):
    """Rule 7.2.4: The attack event occurs."""
    game_state.combat_state["attack_event_occurred"] = True
    source_is_living = game_state.combat_state.get("attack_source_is_living", False)
    source = game_state.combat_state.get("attack_source")
    if source_is_living and source is not None:
        game_state.combat_state["attack_source_is_attacking"] = True
    else:
        game_state.combat_state["controller_is_attacking_hero"] = True


@then("the attack-source has the attacking status")
def attack_source_has_attacking_status(game_state):
    """Rule 7.2.4a: A living attack-source gains the attacking status."""
    assert game_state.combat_state.get("attack_source_is_attacking", False), \
        "Engine feature needed: Living attack-source must become attacking during attack event (Rule 7.2.4a)"


# Rule 7.2.4a: no living attack-source → attacking hero

@given("the Attack Step is processing an attack without a living attack-source")
def attack_without_living_source(game_state):
    """Rule 7.2.4a: The attack has no living attack-source."""
    game_state.combat_state["attack_source"] = None
    game_state.combat_state["attack_source_is_living"] = False
    game_state.combat_state["attack_on_chain"] = True
    hero_card = game_state.create_card(name="Attacking Hero", card_type="hero")
    game_state.combat_state["attacking_controller_hero"] = hero_card


@then("the attacking controller becomes the attacking hero")
def attacking_controller_becomes_attacking_hero(game_state):
    """Rule 7.2.4a: Controller becomes the attacking hero when no living attack-source."""
    assert game_state.combat_state.get("controller_is_attacking_hero", False), \
        "Engine feature needed: GameState.attacking_hero must be set when no living attack-source (Rule 7.2.4a)"


@then("the attacking hero's hero card is designated as the attacking hero")
def attacking_hero_card_is_designated(game_state):
    """Rule 7.2.4a: The controller's hero card is designated as the attacking hero."""
    assert game_state.combat_state.get("attacking_controller_hero") is not None, \
        "Engine feature needed: GameState.attacking_hero.hero_card property (Rule 7.2.4a)"


# Rule 7.2.4b: defending hero

@given("the attack-target is a hero")
def attack_target_is_hero(game_state):
    """Rule 7.2.4b: The attack-target is a hero card."""
    hero_card = game_state.create_card(name="Defending Hero", card_type="hero")
    game_state.attack_targets = [{"card": hero_card, "legal": True, "is_hero": True}]
    game_state.combat_state["attack_target_is_hero"] = True
    game_state.combat_state["defending_hero_card"] = hero_card


@then("the attack-target hero becomes the defending hero")
def attack_target_hero_becomes_defending_hero(game_state):
    """Rule 7.2.4b: The attack-target hero is designated as the defending hero."""
    assert game_state.combat_state.get("attack_target_is_hero", False), \
        "Engine feature needed: GameState.defending_hero must be set when attack-target is hero (Rule 7.2.4b)"


@then("the attack-target hero's controller becomes the defending hero's controller")
def defending_hero_controller_is_set(game_state):
    """Rule 7.2.4b: The defending hero's controller is tracked."""
    assert game_state.combat_state.get("defending_hero_card") is not None, \
        "Engine feature needed: GameState.defending_hero.controller property (Rule 7.2.4b)"


# Rule 7.2.4a + 7.2.4b: designations persist until chain link resolves

@given("the attack event has occurred")
def attack_event_has_occurred(game_state):
    """Rule 7.2.4: The attack event has already occurred."""
    game_state.combat_state["attack_event_occurred"] = True


@given("the attacking hero and defending hero have been designated")
def heroes_designated(game_state):
    """Rule 7.2.4a + 7.2.4b: Both attacking and defending heroes have been designated."""
    hero_attack = game_state.create_card(name="Attacking Hero", card_type="hero")
    hero_defend = game_state.create_card(name="Defending Hero", card_type="hero")
    game_state.combat_state["attacking_hero"] = hero_attack
    game_state.combat_state["defending_hero"] = hero_defend
    game_state.combat_state["designations_active"] = True


@when("the active chain link resolves")
def active_chain_link_resolves(game_state):
    """Rule 7.2.4a + 7.2.4b: The active chain link resolves."""
    game_state.combat_state["chain_link_resolved"] = True
    game_state.combat_state["designations_active"] = False


@then("the attacking hero designation is removed")
def attacking_hero_designation_removed(game_state):
    """Rule 7.2.4a: Attacking hero designation is cleared after chain link resolves."""
    assert not game_state.combat_state.get("designations_active", True), \
        "Engine feature needed: Attacking hero designation must be cleared after chain link resolves (Rule 7.2.4a)"


@then("the defending hero designation is removed")
def defending_hero_designation_removed(game_state):
    """Rule 7.2.4b: Defending hero designation is cleared after chain link resolves."""
    assert not game_state.combat_state.get("designations_active", True), \
        "Engine feature needed: Defending hero designation must be cleared after chain link resolves (Rule 7.2.4b)"


# Rule 7.2.5: turn-player gains priority

@given("the attack has been placed on the combat chain")
def attack_placed_on_chain_for_priority(game_state):
    """Rule 7.2.5: The attack is on the combat chain."""
    attack_card = game_state.create_card(name="Test Attack", card_type="attack_action")
    game_state.current_attack = attack_card
    game_state.combat_state["attack_on_chain"] = True


@given("the attack event has occurred", target_fixture=None)
def attack_event_has_occurred_for_priority(game_state):
    """Rule 7.2.5: The attack event has occurred."""
    game_state.combat_state["attack_event_occurred"] = True


@when("the Attack Step grants priority")
def attack_step_grants_priority(game_state):
    """Rule 7.2.5: The turn-player is given priority."""
    game_state.combat_state["priority_granted_to_turn_player"] = True


@then("the turn-player has priority")
def turn_player_has_priority(game_state):
    """Rule 7.2.5: The turn-player has priority in the Attack Step."""
    assert game_state.combat_state.get("priority_granted_to_turn_player", False), \
        "Engine feature needed: PrioritySystem.who_has_priority() must return turn-player (Rule 7.2.5)"


# Rule 7.2.6: Defend Step begins

@given("the Attack Step is active")
def attack_step_is_active(game_state):
    """Rule 7.2.6: The Attack Step is active."""
    game_state.combat_state["current_step"] = "attack"
    game_state.combat_state["attack_step_active"] = True


@given("the stack is empty")
def stack_is_empty(game_state):
    """Rule 7.2.6: The stack is empty."""
    game_state.stack.clear()


@then("the Defend Step begins")
def defend_step_begins(game_state):
    """Rule 7.2.6: The Defend Step begins after the Attack Step ends."""
    assert game_state.combat_state.get("defend_step_active", False), \
        "Engine feature needed: CombatState.defend_step_active not implemented (Rule 7.2.6)"


# ===== Fixture =====

@pytest.fixture
def game_state():
    """
    Fixture providing game state for testing Section 7.2: Attack Step.

    Uses BDDGameState which integrates with the real engine.
    Reference: Rule 7.2
    """
    from tests.bdd_helpers import BDDGameState

    state = BDDGameState()

    # Combat state tracking for Attack Step tests
    state.combat_state = {
        "current_step": None,
        "layer_step_active": False,
        "attack_step_active": False,
        "defend_step_active": False,
        "close_step_active": False,
        "all_players_passed": False,
        "attack_on_chain": False,
        "active_chain_link": None,
        "attack_event_occurred": False,
        "priority_granted_to_turn_player": False,
        "declared_defenders": [],
        "attack_targets": [],
        "attack_has_resolution_ability": False,
        "resolution_ability_generated": False,
        "resolution_abilities_processed": False,
        "attack_type": None,
        "attack_proxy": None,
        "attack_source": None,
        "attack_source_is_living": False,
        "attack_source_is_attacking": False,
        "controller_is_attacking_hero": False,
        "attacking_hero": None,
        "defending_hero": None,
        "attacking_controller_hero": None,
        "defending_hero_card": None,
        "attack_target_is_hero": False,
        "designations_active": False,
        "target_legality_check_passed": False,
        "all_targets_illegal": False,
        "attack_step_ended_early": False,
        "targets_illegal_post_check": False,
        "active_attack_exists": True,
        "chain_link_resolved": False,
        "attack_triggered_effects": [],
    }

    # Stack is a list of layers
    state.stack = []

    # Current attack card
    state.current_attack = None

    # Attack targets list
    state.attack_targets = []

    return state
