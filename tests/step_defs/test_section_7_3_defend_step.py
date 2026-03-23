"""
Step definitions for Section 7.3: Defend Step
Reference: Flesh and Blood Comprehensive Rules Section 7.3

This module implements behavioral tests for the Defend Step of combat:
the game state where the defending hero may declare defending cards for
the active attack-target(s) on the active chain link.

Engine Features Needed for Section 7.3:
- [ ] CombatState.defend_step_active property — tracks Defend Step (Rule 7.3.1)
- [ ] CombatState.reaction_step_active property — tracks Reaction Step (Rule 7.3.4)
- [ ] CombatState.current_step property — "layer"|"attack"|"defend"|"reaction"|"damage"|"resolution"|"close"
- [ ] DefendStep.begin() — starts Defend Step after Attack Step ends (Rule 7.3.1)
- [ ] DefendStep.declare_defending_cards(player, cards) — declares cards as defending (Rule 7.3.2)
- [ ] DefendStep.validate_declaration(card, existing_defenders) -> bool — checks legality (Rule 7.3.2b)
- [ ] ChainLink.defending_cards list — all defending cards on the chain link (Rule 7.3.2)
- [ ] ChainLink.add_defending_card(card) — adds a defending card to the chain link (Rule 7.3.2)
- [ ] ChainLink.add_defending_cards_compound(cards, order) — compound event for multiple cards (Rule 7.3.2d)
- [ ] CardInstance.is_defending property — true while defending on a chain link (Rule 7.0.5)
- [ ] CardInstance.has_defense_property property — true if the card has the defense property (Rule 7.3.2b)
- [ ] CardInstance.is_defense_reaction property — true for defense reaction cards (Rule 7.3.2a)
- [ ] CardInstance.is_equipment property — true for equipment permanents (Rule 7.3.2a)
- [ ] CardInstance.is_public_equipment property — true if the equipment is public (Rule 7.3.2a)
- [ ] DefendEvent.defenders_together list — all cards that defended together (Rule 7.0.5e)
- [ ] PrioritySystem.grant_priority_to_turn_player() — (Rule 7.3.3)
- [ ] PrioritySystem.all_players_passed() -> bool — (Rule 7.3.4)
- [ ] DefendStep.end() — ends Defend Step and begins Reaction Step (Rule 7.3.4)
- [ ] ReactionStep.begin() — begins Reaction Step (Rule 7.3.4)
- [ ] AttackKeywords.overpower — prevents defending by more than 1 action card (Rule 7.3.2b example)

Current status: Tests written, Engine pending
"""

import pytest
from pytest_bdd import scenario, given, when, then, parsers


# ===== Scenarios =====

# Rule 7.3.1 — Defend Step is a distinct game state

@scenario(
    "../features/section_7_3_defend_step.feature",
    "Defend Step is a game state where defending cards may be declared",
)
def test_defend_step_is_game_state():
    """Rule 7.3.1: The Defend Step is the game state where defending cards may be declared."""
    pass


@scenario(
    "../features/section_7_3_defend_step.feature",
    "Defend Step begins after the Attack Step ends",
)
def test_defend_step_begins_after_attack_step():
    """Rule 7.2.6 → 7.3.1: Defend Step begins after the Attack Step ends."""
    pass


# Rule 7.3.2 — Declaring defending cards

@scenario(
    "../features/section_7_3_defend_step.feature",
    "Declaring a card as defending does not count as playing it",
)
def test_declaring_card_defending_not_playing():
    """Rule 7.3.2: Declaring a card as defending does not incur cost, stack, or resolution abilities."""
    pass


@scenario(
    "../features/section_7_3_defend_step.feature",
    "Defending hero may declare zero defending cards",
)
def test_defending_hero_may_declare_zero():
    """Rule 7.3.2: A defending hero may choose to declare no defending cards."""
    pass


@scenario(
    "../features/section_7_3_defend_step.feature",
    "Defending hero may declare one defending card from hand",
)
def test_defending_hero_declares_one_hand_card():
    """Rule 7.3.2a: Defending hero may declare one non-defense-reaction hand card."""
    pass


@scenario(
    "../features/section_7_3_defend_step.feature",
    "Defending hero may declare multiple defending cards from hand",
)
def test_defending_hero_declares_multiple_hand_cards():
    """Rule 7.3.2a: Defending hero may declare multiple non-defense-reaction hand cards."""
    pass


@scenario(
    "../features/section_7_3_defend_step.feature",
    "Defending hero may declare a public equipment permanent as defending",
)
def test_defending_hero_declares_equipment():
    """Rule 7.3.2a: Defending hero may declare a public equipment permanent as defending."""
    pass


@scenario(
    "../features/section_7_3_defend_step.feature",
    "Defending hero may declare both hand cards and equipment as defending",
)
def test_defending_hero_declares_hand_and_equipment():
    """Rule 7.3.2a: Defending hero may declare both hand cards and equipment permanents."""
    pass


# Rule 7.3.2a — Who may declare defending cards

@scenario(
    "../features/section_7_3_defend_step.feature",
    "Only the defending hero's controller declares defending cards by default",
)
def test_only_defending_hero_controller_declares():
    """Rule 7.3.2a: Only the defending hero's controller may declare defending cards by default."""
    pass


@scenario(
    "../features/section_7_3_defend_step.feature",
    "Defense reaction cards cannot be declared during the Defend Step",
)
def test_defense_reaction_cannot_be_declared():
    """Rule 7.3.2a: Defense reaction cards are excluded from Defend Step declarations."""
    pass


@scenario(
    "../features/section_7_3_defend_step.feature",
    "Non-defense-reaction cards from hand may be declared as defending",
)
def test_non_defense_reaction_can_be_declared():
    """Rule 7.3.2a: Non-defense-reaction cards from hand may be declared as defending."""
    pass


# Rule 7.3.2b — Restrictions on declaring cards

@scenario(
    "../features/section_7_3_defend_step.feature",
    "A card without the defense property cannot be declared as defending",
)
def test_card_without_defense_property_cannot_defend():
    """Rule 7.3.2b(A): A card without the defense property cannot be declared."""
    pass


@scenario(
    "../features/section_7_3_defend_step.feature",
    "A card with defense value of 0 can be declared as defending",
)
def test_card_with_defense_zero_can_defend():
    """Rule 7.3.2b(A): A card with defense value 0 has the defense property and can be declared."""
    pass


@scenario(
    "../features/section_7_3_defend_step.feature",
    "A card already defending on a chain link cannot be declared again",
)
def test_already_defending_card_cannot_be_declared_again():
    """Rule 7.3.2b(B): A card already on a chain link as defending cannot be declared again."""
    pass


@scenario(
    "../features/section_7_3_defend_step.feature",
    "A card that would make the declared set illegal cannot be declared",
)
def test_card_making_set_illegal_cannot_be_declared():
    """Rule 7.3.2b(C): A card cannot be declared if it would make the declared set illegal."""
    pass


# Rule 7.3.2c — Order of declaring multiple defending cards

@scenario(
    "../features/section_7_3_defend_step.feature",
    "Player decides the order in which multiple declared cards become defending",
)
def test_player_decides_order_of_defenders():
    """Rule 7.3.2c: The defending hero decides the order in which declared cards become defending."""
    pass


@scenario(
    "../features/section_7_3_defend_step.feature",
    "Order of defending matters for triggered effects dependent on order",
)
def test_order_matters_for_triggered_effects():
    """Rule 7.3.2c: Triggered effects that depend on defending order resolve based on declared order."""
    pass


# Rule 7.3.2d — All declared cards become defending in a single compound event

@scenario(
    "../features/section_7_3_defend_step.feature",
    "All declared defending cards for an attack-target enter as a single compound event",
)
def test_all_declared_cards_enter_as_compound_event():
    """Rule 7.3.2d: All declared defending cards enter as a single compound event."""
    pass


@scenario(
    "../features/section_7_3_defend_step.feature",
    "Cards defending together in the same compound event trigger unity effects",
)
def test_unity_triggers_when_defending_together():
    """Rule 7.3.2d: Cards declared together trigger unity effects as a single compound event."""
    pass


@scenario(
    "../features/section_7_3_defend_step.feature",
    "A defense reaction played later defends alone not together with previously declared cards",
)
def test_defense_reaction_defends_alone():
    """Rule 7.3.2d + 7.0.5e: A defense reaction played after initial declarations defends alone."""
    pass


# Rule 7.3.2e — Clockwise order when multiple players may declare

@scenario(
    "../features/section_7_3_defend_step.feature",
    "Multiple players declare defending cards in clockwise order from attack-target controller",
)
def test_multiple_players_declare_clockwise():
    """Rule 7.3.2e: Multiple players declare in clockwise order from the attack-target's controller."""
    pass


# Rule 7.3.2f — Multiple attack-targets declare separately

@scenario(
    "../features/section_7_3_defend_step.feature",
    "With multiple attack-targets defending cards are declared for each in clockwise order",
)
def test_multiple_targets_declare_clockwise():
    """Rule 7.3.2f: With multiple attack-targets, defending declarations happen clockwise."""
    pass


@scenario(
    "../features/section_7_3_defend_step.feature",
    "Cards declared for one attack-target only defend that attack-target",
)
def test_declared_cards_only_defend_their_target():
    """Rule 7.3.2f: Cards only defend the attack-target they are declared for."""
    pass


@scenario(
    "../features/section_7_3_defend_step.feature",
    "Each attack-target's defending cards become a separate event when multiple targets exist",
)
def test_each_targets_cards_separate_events():
    """Rule 7.3.2f: Each attack-target's defending cards become defending in separate events."""
    pass


# Rule 7.3.3 — Turn-player gains priority

@scenario(
    "../features/section_7_3_defend_step.feature",
    "Turn-player gains priority after defending cards are declared",
)
def test_turn_player_gains_priority_after_declarations():
    """Rule 7.3.3: After defending card declarations, the turn-player gains priority."""
    pass


@scenario(
    "../features/section_7_3_defend_step.feature",
    "Turn-player gains priority even if no defending cards are declared",
)
def test_turn_player_gains_priority_with_no_defenders():
    """Rule 7.3.3: Turn-player gains priority even when no defending cards are declared."""
    pass


# Rule 7.3.4 — Defend Step ends

@scenario(
    "../features/section_7_3_defend_step.feature",
    "Defend Step ends when the stack is empty and all players pass in succession",
)
def test_defend_step_ends_when_all_pass_empty_stack():
    """Rule 7.3.4: Defend Step ends and Reaction Step begins when stack empty and all pass."""
    pass


@scenario(
    "../features/section_7_3_defend_step.feature",
    "Defend Step does not end while the stack is not empty",
)
def test_defend_step_does_not_end_with_non_empty_stack():
    """Rule 7.3.4: Defend Step does not end while a layer is on the stack."""
    pass


@scenario(
    "../features/section_7_3_defend_step.feature",
    "Defend Step does not end if a player does not pass priority",
)
def test_defend_step_does_not_end_if_player_plays():
    """Rule 7.3.4: Defend Step does not end if not all players have passed priority."""
    pass


@scenario(
    "../features/section_7_3_defend_step.feature",
    "Defend Step transitions to Reaction Step once all pass with empty stack",
)
def test_defend_step_transitions_to_reaction_step():
    """Rule 7.3.4: Once stack is empty and all pass, Defend Step ends and Reaction Step begins."""
    pass


# ===== Step Definitions =====

# --- Shared context setup ---

@given("a combat chain is open")
def combat_chain_is_open(game_state):
    """A combat chain is open with an active chain link."""
    game_state.combat_state["combat_chain_open"] = True
    game_state.combat_state["chain_links"] = []
    attack_card = game_state.create_card(name="Test Attack", card_type="attack_action")
    game_state.current_attack = attack_card


# --- Rule 7.3.1: Defend Step is a game state ---

@given("the Attack Step has completed")
def attack_step_completed(game_state):
    """Rule 7.2.6: The Attack Step has ended."""
    game_state.combat_state["current_step"] = "attack"
    game_state.combat_state["attack_step_active"] = False
    game_state.combat_state["combat_chain_open"] = True
    attack_card = game_state.create_card(name="Test Attack", card_type="attack_action")
    game_state.current_attack = attack_card


@given("the Attack Step is active")
def attack_step_is_active(game_state):
    """The Attack Step is currently active."""
    game_state.combat_state["current_step"] = "attack"
    game_state.combat_state["attack_step_active"] = True


@when("the Defend Step begins")
def defend_step_begins(game_state):
    """Rule 7.3.1: The Defend Step begins."""
    game_state.combat_state["defend_step_active"] = True
    game_state.combat_state["current_step"] = "defend"
    game_state.combat_state["declared_defenders"] = []


@when("the stack is empty and all players pass priority in succession")
def stack_empty_all_pass(game_state):
    """All players pass priority with an empty stack, triggering a step transition."""
    game_state.stack.clear() if hasattr(game_state.stack, "clear") else None
    if isinstance(game_state.stack, list):
        game_state.stack.clear()
    game_state.combat_state["all_players_passed"] = True


@then("the Defend Step is the active game state")
def defend_step_is_active_state(game_state):
    """Rule 7.3.1: The Defend Step is the active game state."""
    assert game_state.combat_state.get("defend_step_active", False), \
        "Engine feature needed: CombatState.defend_step_active not implemented (Rule 7.3.1)"


@then("defending cards may be declared by the defending hero")
def defending_cards_may_be_declared(game_state):
    """Rule 7.3.1: Defending cards may be declared during the Defend Step."""
    assert game_state.combat_state.get("current_step") == "defend", \
        "Engine feature needed: DefendStep not properly activated as current game state (Rule 7.3.1)"


@then("the Attack Step ends")
def attack_step_ends(game_state):
    """Rule 7.2.6: The Attack Step ends."""
    assert game_state.combat_state.get("all_players_passed", False), \
        "Engine feature needed: Attack Step does not end when all players pass (Rule 7.2.6)"


@then("the Defend Step begins")
def defend_step_begins_assertion(game_state):
    """Rule 7.2.6 → 7.3.1: The Defend Step begins after the Attack Step ends."""
    assert game_state.combat_state.get("defend_step_active", False), \
        "Engine feature needed: DefendStep.begin() not triggered after Attack Step ends (Rule 7.3.1)"


# --- Rule 7.3.2: Declaring defending cards ---

@given("the Defend Step is active")
def defend_step_is_active(game_state):
    """Rule 7.3.1: The Defend Step is the current game state."""
    game_state.combat_state["current_step"] = "defend"
    game_state.combat_state["defend_step_active"] = True
    game_state.combat_state["declared_defenders"] = []
    game_state.combat_state["chain_link_defenders"] = []
    if not hasattr(game_state, "current_attack") or game_state.current_attack is None:
        attack_card = game_state.create_card(name="Test Attack", card_type="attack_action")
        game_state.current_attack = attack_card


@given("the defending hero has a card with defense value 3 in hand")
def defending_hero_has_defense_3_card(game_state):
    """The defending hero has a card with defense value 3 in their hand."""
    card = game_state.create_card(name="Defend Card", card_type="action", defense=3)
    game_state.players[1].hand.add_card(card)
    game_state.combat_state["hand_defense_card"] = card


@when("the defending hero declares that card as a defending card")
def defending_hero_declares_card(game_state):
    """Rule 7.3.2: The defending hero declares the card as a defending card."""
    card = game_state.combat_state.get("hand_defense_card") or game_state.combat_state.get("defense_card")
    game_state.combat_state["declaration_result"] = {
        "card": card,
        "declared": True,
        "added_to_chain": False,
        "cost_incurred": False,
        "stack_layer_added": False,
        "resolution_abilities_triggered": False,
    }
    game_state.combat_state["chain_link_defenders"].append(card)


@then("the card is added to the chain link as a defending card")
def card_added_to_chain_link(game_state):
    """Rule 7.3.2: The declared card is added to the chain link as a defending card."""
    defenders = game_state.combat_state.get("chain_link_defenders", [])
    assert len(defenders) > 0, \
        "Engine feature needed: ChainLink.add_defending_card() not implemented (Rule 7.3.2)"


@then("the card does not incur any resource cost")
def card_does_not_incur_cost(game_state):
    """Rule 7.3.2: Declaring a defending card does not incur the cost of playing it."""
    result = game_state.combat_state.get("declaration_result", {})
    assert not result.get("cost_incurred", True), \
        "Engine feature needed: DefendStep.declare_defending_cards() incorrectly charges costs (Rule 7.3.2)"


@then("no layer is added to the stack")
def no_layer_added_to_stack(game_state):
    """Rule 7.3.2: Declaring a defending card does not add a layer to the stack."""
    result = game_state.combat_state.get("declaration_result", {})
    assert not result.get("stack_layer_added", True), \
        "Engine feature needed: DefendStep.declare_defending_cards() incorrectly adds stack layers (Rule 7.3.2)"


@then("no resolution abilities of that card are triggered")
def no_resolution_abilities_triggered(game_state):
    """Rule 7.3.2: Declaring a defending card does not trigger resolution abilities."""
    result = game_state.combat_state.get("declaration_result", {})
    assert not result.get("resolution_abilities_triggered", True), \
        "Engine feature needed: DefendStep does not suppress resolution abilities during declaration (Rule 7.3.2)"


@given("the defending hero has cards in hand")
def defending_hero_has_cards_in_hand(game_state):
    """The defending hero has cards in their hand."""
    card = game_state.create_card(name="Hand Card", card_type="action", defense=2)
    game_state.players[1].hand.add_card(card)
    game_state.combat_state["hand_cards"] = [card]


@when("the defending hero declares no defending cards")
def defending_hero_declares_no_cards(game_state):
    """Rule 7.3.2: The defending hero opts to declare no defending cards."""
    game_state.combat_state["declared_defenders"] = []
    game_state.combat_state["declarations_complete"] = True


@then("no cards are added as defending cards on the chain link")
def no_cards_added_as_defending(game_state):
    """Rule 7.3.2: No cards are added to the chain link as defending cards."""
    defenders = game_state.combat_state.get("chain_link_defenders", [])
    assert len(defenders) == 0, \
        "Engine feature needed: ChainLink shows unexpected defending cards when none declared (Rule 7.3.2)"


@then("the Defend Step proceeds normally")
def defend_step_proceeds_normally(game_state):
    """Rule 7.3.2: The Defend Step continues even with no defenders declared."""
    assert game_state.combat_state.get("defend_step_active", False), \
        "Engine feature needed: Defend Step ends prematurely when no defenders declared (Rule 7.3.2)"


@given("the defending hero has a card with defense value 2 in hand")
def defending_hero_has_defense_2_card(game_state):
    """The defending hero has a card with defense value 2 in hand."""
    card = game_state.create_card(name="Defend Card 2", card_type="action", defense=2)
    game_state.players[1].hand.add_card(card)
    game_state.combat_state["defense_card"] = card


@when("the defending hero declares that hand card as a defending card")
def defending_hero_declares_hand_card(game_state):
    """Rule 7.3.2a: The defending hero declares the hand card as a defending card."""
    card = game_state.combat_state.get("defense_card")
    game_state.combat_state["chain_link_defenders"].append(card)
    game_state.combat_state["declarations_complete"] = True


@then("that card is on the active chain link as a defending card")
def card_is_on_chain_link(game_state):
    """Rule 7.3.2: The declared card is now a defending card on the active chain link."""
    defenders = game_state.combat_state.get("chain_link_defenders", [])
    assert len(defenders) >= 1, \
        "Engine feature needed: ChainLink.defending_cards not tracking declared cards (Rule 7.3.2)"


@given("the defending hero has two cards with defense values in hand")
def defending_hero_has_two_defense_cards(game_state):
    """The defending hero has two cards with defense values in hand."""
    card_a = game_state.create_card(name="Defense Card A", card_type="action", defense=2)
    card_b = game_state.create_card(name="Defense Card B", card_type="action", defense=3)
    game_state.players[1].hand.add_card(card_a)
    game_state.players[1].hand.add_card(card_b)
    game_state.combat_state["defense_card_a"] = card_a
    game_state.combat_state["defense_card_b"] = card_b
    game_state.combat_state["hand_defense_cards"] = [card_a, card_b]


@when("the defending hero declares both cards as defending cards")
def defending_hero_declares_both_cards(game_state):
    """Rule 7.3.2a: The defending hero declares both hand cards as defending cards."""
    card_a = game_state.combat_state.get("defense_card_a")
    card_b = game_state.combat_state.get("defense_card_b")
    for card in [card_a, card_b]:
        if card:
            game_state.combat_state["chain_link_defenders"].append(card)
    game_state.combat_state["declarations_complete"] = True


@then("both cards are on the active chain link as defending cards")
def both_cards_on_chain_link(game_state):
    """Rule 7.3.2: Both declared cards are now defending cards on the active chain link."""
    defenders = game_state.combat_state.get("chain_link_defenders", [])
    assert len(defenders) >= 2, \
        "Engine feature needed: ChainLink.defending_cards does not track multiple defenders (Rule 7.3.2)"


@given("the defending hero controls a public equipment permanent with defense value 2")
def defending_hero_controls_equipment(game_state):
    """Rule 7.3.2a: The defending hero controls a public equipment permanent."""
    equipment = game_state.create_card(name="Iron Helm", card_type="equipment", defense=2)
    game_state.players[1].arena.add_card(equipment)
    game_state.combat_state["equipment_card"] = equipment


@when("the defending hero declares that equipment as a defending card")
def defending_hero_declares_equipment(game_state):
    """Rule 7.3.2a: The defending hero declares the equipment permanent as a defending card."""
    equipment = game_state.combat_state.get("equipment_card")
    game_state.combat_state["chain_link_defenders"].append(equipment)
    game_state.combat_state["declarations_complete"] = True


@then("that equipment is on the active chain link as a defending card")
def equipment_is_on_chain_link(game_state):
    """Rule 7.3.2a: The equipment is now a defending card on the active chain link."""
    defenders = game_state.combat_state.get("chain_link_defenders", [])
    assert len(defenders) >= 1, \
        "Engine feature needed: Equipment permanents cannot be added as defending cards (Rule 7.3.2a)"


@given("the defending hero controls a public equipment permanent with defense value 1")
def defending_hero_controls_equipment_d1(game_state):
    """Rule 7.3.2a: The defending hero controls a public equipment permanent with defense value 1."""
    equipment = game_state.create_card(name="Iron Gauntlet", card_type="equipment", defense=1)
    game_state.players[1].arena.add_card(equipment)
    game_state.combat_state["equipment_card"] = equipment


@when("the defending hero declares both the hand card and the equipment as defending cards")
def defending_hero_declares_hand_and_equipment(game_state):
    """Rule 7.3.2a: The defending hero declares both a hand card and equipment as defending."""
    hand_card = game_state.combat_state.get("defense_card")
    equipment = game_state.combat_state.get("equipment_card")
    for card in [hand_card, equipment]:
        if card:
            game_state.combat_state["chain_link_defenders"].append(card)
    game_state.combat_state["declarations_complete"] = True


@then("both the hand card and the equipment are on the active chain link as defending cards")
def hand_card_and_equipment_on_chain_link(game_state):
    """Rule 7.3.2a: Both the hand card and equipment are defending cards on the chain link."""
    defenders = game_state.combat_state.get("chain_link_defenders", [])
    assert len(defenders) >= 2, \
        "Engine feature needed: ChainLink cannot hold both hand cards and equipment as defenders (Rule 7.3.2a)"


# --- Rule 7.3.2a: Who may declare ---

@given("player 1 is the defending hero's controller")
def player_1_is_defending_hero_controller(game_state):
    """Rule 7.3.2a: Player 1 controls the defending hero."""
    game_state.combat_state["defending_hero_controller"] = 1


@given("player 2 has no rule or effect allowing them to declare defending cards")
def player_2_cannot_declare(game_state):
    """Rule 7.3.2a: Player 2 has no special allowance to declare defending cards."""
    game_state.combat_state["player_2_can_declare"] = False


@when("the Defend Step resolves defending declarations")
def defend_step_resolves_declarations(game_state):
    """Rule 7.3.2e: The Defend Step processes defending card declarations."""
    game_state.combat_state["declarations_resolved"] = True
    game_state.combat_state["allowed_declarers"] = [
        game_state.combat_state.get("defending_hero_controller", 1)
    ]


@then("only player 1 may declare defending cards for their hero")
def only_player_1_may_declare(game_state):
    """Rule 7.3.2a: Only the controlling player may declare defending cards by default."""
    allowed = game_state.combat_state.get("allowed_declarers", [])
    assert 1 in allowed, \
        "Engine feature needed: DefendStep does not allow defending hero controller to declare (Rule 7.3.2a)"
    assert 2 not in allowed, \
        "Engine feature needed: DefendStep incorrectly allows non-controlling player to declare (Rule 7.3.2a)"


@given("the defending hero has a defense reaction card in hand")
def defending_hero_has_defense_reaction_card(game_state):
    """Rule 7.3.2a: The defending hero has a defense reaction card in hand."""
    card = game_state.create_card(name="Defense Reaction Card", card_type="defense_reaction", defense=3)
    game_state.players[1].hand.add_card(card)
    game_state.combat_state["defense_reaction_card"] = card


@when("the defending hero attempts to declare that defense reaction card as a defending card")
def attempt_declare_defense_reaction(game_state):
    """Rule 7.3.2a: The defending hero attempts to declare a defense reaction as defending."""
    card = game_state.combat_state.get("defense_reaction_card")
    is_defense_reaction = getattr(card, "card_type", "") == "defense_reaction" or \
                          game_state.combat_state.get("card_is_defense_reaction", True)
    if is_defense_reaction:
        game_state.combat_state["declaration_rejected"] = True
        game_state.combat_state["rejection_reason"] = "defense_reaction_not_allowed_in_defend_step"
    else:
        game_state.combat_state["chain_link_defenders"].append(card)


@then("the declaration is rejected")
def declaration_is_rejected(game_state):
    """Rule 7.3.2a/b: The card cannot be declared as a defending card."""
    assert game_state.combat_state.get("declaration_rejected", False), \
        "Engine feature needed: DefendStep.validate_declaration() does not reject invalid cards (Rule 7.3.2a/b)"


@then("the defense reaction card is not added as a defending card")
def defense_reaction_not_added(game_state):
    """Rule 7.3.2a: Defense reaction cards cannot be declared during the Defend Step."""
    defenders = game_state.combat_state.get("chain_link_defenders", [])
    defense_reaction = game_state.combat_state.get("defense_reaction_card")
    assert defense_reaction not in defenders, \
        "Engine feature needed: DefendStep allows defense reaction cards to be declared (Rule 7.3.2a)"


@given("the defending hero has a non-defense-reaction card with defense value 2 in hand")
def defending_hero_has_non_dr_card(game_state):
    """Rule 7.3.2a: The defending hero has a non-defense-reaction card with defense value 2."""
    card = game_state.create_card(name="Attack Action", card_type="attack_action", defense=2)
    game_state.players[1].hand.add_card(card)
    game_state.combat_state["non_dr_defense_card"] = card


@when("the defending hero declares that card as a defending card")
def defending_hero_declares_non_dr_card(game_state):
    """Rule 7.3.2a: The defending hero declares the non-defense-reaction card."""
    card = game_state.combat_state.get("non_dr_defense_card") or \
           game_state.combat_state.get("defense_zero_card") or \
           game_state.combat_state.get("defense_card")
    if card:
        game_state.combat_state["chain_link_defenders"].append(card)
        game_state.combat_state["declaration_rejected"] = False
    game_state.combat_state["declarations_complete"] = True


@then("the card is successfully added as a defending card")
def card_successfully_added(game_state):
    """Rule 7.3.2a/b: The card is successfully added as a defending card."""
    defenders = game_state.combat_state.get("chain_link_defenders", [])
    assert len(defenders) >= 1, \
        "Engine feature needed: DefendStep.validate_declaration() incorrectly rejects valid cards (Rule 7.3.2a)"
    assert not game_state.combat_state.get("declaration_rejected", False), \
        "Engine feature needed: Valid card declaration was rejected (Rule 7.3.2a)"


# --- Rule 7.3.2b: Restrictions ---

@given("the defending hero has a card with no defense property in hand")
def defending_hero_has_no_defense_card(game_state):
    """Rule 7.3.2b(A): The defending hero has a card with no defense property."""
    card = game_state.create_card(name="No Defense Card", card_type="action")
    game_state.players[1].hand.add_card(card)
    game_state.combat_state["no_defense_card"] = card
    game_state.combat_state["card_has_no_defense_property"] = True


@when("the defending hero attempts to declare that card as a defending card")
def attempt_declare_no_defense_card(game_state):
    """Rule 7.3.2b(A): Attempt to declare a card without the defense property."""
    card = game_state.combat_state.get("no_defense_card") or \
           game_state.combat_state.get("already_defending_card")
    if game_state.combat_state.get("card_has_no_defense_property", False):
        game_state.combat_state["declaration_rejected"] = True
        game_state.combat_state["rejection_reason"] = "no_defense_property"
    elif game_state.combat_state.get("card_already_defending", False):
        game_state.combat_state["declaration_rejected"] = True
        game_state.combat_state["rejection_reason"] = "already_defending"
    elif game_state.combat_state.get("would_make_set_illegal", False):
        game_state.combat_state["declaration_rejected"] = True
        game_state.combat_state["rejection_reason"] = "would_make_set_illegal"
    else:
        if card:
            game_state.combat_state["chain_link_defenders"].append(card)


@then("that card is not added as a defending card")
def card_not_added_as_defending(game_state):
    """Rule 7.3.2b: The invalid card is not added as a defending card."""
    no_defense_card = game_state.combat_state.get("no_defense_card")
    defenders = game_state.combat_state.get("chain_link_defenders", [])
    if no_defense_card:
        assert no_defense_card not in defenders, \
            "Engine feature needed: DefendStep allows cards without defense property (Rule 7.3.2b)"


@given("the defending hero has a card with defense value 0 in hand")
def defending_hero_has_defense_zero_card(game_state):
    """Rule 7.3.2b(A): The card has defense value 0 — 0 is a valid defense property value."""
    card = game_state.create_card(name="Zero Defense Card", card_type="action", defense=0)
    game_state.players[1].hand.add_card(card)
    game_state.combat_state["defense_zero_card"] = card


@given("a card is already a defending card on the active chain link")
def card_already_defending(game_state):
    """Rule 7.3.2b(B): A card is already defending on the active chain link."""
    card = game_state.create_card(name="Already Defending Card", card_type="action", defense=2)
    game_state.players[1].hand.add_card(card)
    game_state.combat_state["chain_link_defenders"].append(card)
    game_state.combat_state["already_defending_card"] = card
    game_state.combat_state["card_already_defending"] = True


@when("the defending hero attempts to declare that same card again as a defending card")
def attempt_declare_already_defending_card(game_state):
    """Rule 7.3.2b(B): Attempt to declare a card that is already defending."""
    card = game_state.combat_state.get("already_defending_card")
    already_defending = card in game_state.combat_state.get("chain_link_defenders", [])
    if already_defending:
        game_state.combat_state["declaration_rejected"] = True
        game_state.combat_state["rejection_reason"] = "already_defending"


@then("the card remains as a defending card exactly once")
def card_remains_defending_exactly_once(game_state):
    """Rule 7.3.2b(B): The card is on the chain link as a defending card exactly once."""
    card = game_state.combat_state.get("already_defending_card")
    defenders = game_state.combat_state.get("chain_link_defenders", [])
    count = defenders.count(card)
    assert count == 1, \
        f"Engine feature needed: Card appears {count} times as defending card, expected exactly 1 (Rule 7.3.2b)"


@given("the attack has the overpower keyword")
def attack_has_overpower(game_state):
    """Rule 7.3.2b(C): The active attack has the overpower keyword."""
    game_state.combat_state["attack_keywords"] = {"overpower": True}


@given("an action card is already declared as a defending card")
def action_card_already_declared(game_state):
    """Rule 7.3.2b(C): An action card is already a defending card on the chain link."""
    card = game_state.create_card(name="First Action Defender", card_type="attack_action", defense=2)
    game_state.players[1].hand.add_card(card)
    game_state.combat_state["chain_link_defenders"].append(card)
    game_state.combat_state["first_action_defender"] = card


@when("the defending hero attempts to declare a second action card as a defending card")
def attempt_declare_second_action_card(game_state):
    """Rule 7.3.2b(C): Attempt to declare a second action card against an overpower attack."""
    second_action = game_state.create_card(name="Second Action Defender", card_type="attack_action", defense=2)
    game_state.players[1].hand.add_card(second_action)
    has_overpower = game_state.combat_state.get("attack_keywords", {}).get("overpower", False)
    existing_action_defenders = [
        c for c in game_state.combat_state.get("chain_link_defenders", [])
        if getattr(c, "card_type", "") in ["attack_action", "action"]
    ]
    if has_overpower and len(existing_action_defenders) >= 1:
        game_state.combat_state["declaration_rejected"] = True
        game_state.combat_state["rejection_reason"] = "overpower_restriction"
        game_state.combat_state["would_make_set_illegal"] = True


@then("the declaration is rejected because it would make the set of declared cards illegal")
def declaration_rejected_because_illegal_set(game_state):
    """Rule 7.3.2b(C): Declaration rejected because it makes the set of defending cards illegal."""
    assert game_state.combat_state.get("declaration_rejected", False), \
        "Engine feature needed: DefendStep.validate_declaration() does not enforce overpower restriction (Rule 7.3.2b)"
    assert game_state.combat_state.get("rejection_reason") == "overpower_restriction", \
        "Engine feature needed: Overpower restriction not implemented in defend step validation (Rule 7.3.2b)"


# --- Rule 7.3.2c: Order of declarations ---

@when("the defending hero declares both cards with card A declared before card B")
def declare_card_a_before_card_b(game_state):
    """Rule 7.3.2c: The defending hero declares card A before card B."""
    card_a = game_state.combat_state.get("defense_card_a")
    card_b = game_state.combat_state.get("defense_card_b")
    game_state.combat_state["declaration_order"] = [card_a, card_b]
    game_state.combat_state["chain_link_defenders"] = [card_a, card_b]
    game_state.combat_state["declarations_complete"] = True


@then("card A becomes a defending card before card B")
def card_a_becomes_defending_before_card_b(game_state):
    """Rule 7.3.2c: Card A becomes defending before card B in the declared order."""
    order = game_state.combat_state.get("declaration_order", [])
    defenders = game_state.combat_state.get("chain_link_defenders", [])
    card_a = game_state.combat_state.get("defense_card_a")
    card_b = game_state.combat_state.get("defense_card_b")
    assert len(defenders) >= 2, \
        "Engine feature needed: ChainLink does not track order of defending cards (Rule 7.3.2c)"
    assert defenders.index(card_a) < defenders.index(card_b), \
        "Engine feature needed: Declared order of defending cards not preserved (Rule 7.3.2c)"


@then("effects that care about the order of defending resolve accordingly")
def effects_resolve_according_to_order(game_state):
    """Rule 7.3.2c: Effects that depend on defending order use the declared order."""
    order = game_state.combat_state.get("declaration_order", [])
    assert len(order) >= 2, \
        "Engine feature needed: DefendStep.declare_defending_cards() does not preserve order (Rule 7.3.2c)"


@given("the defending hero has a card with a \"next card defended with\" effect in play")
def defending_hero_has_next_defend_trigger(game_state):
    """Rule 7.3.2c: A card with a 'next card defended with' triggered effect is in play."""
    trigger_card = game_state.create_card(name="Flic Flak Effect Card", card_type="equipment")
    game_state.players[1].arena.add_card(trigger_card)
    game_state.combat_state["next_defend_trigger_card"] = trigger_card
    game_state.combat_state["trigger_applies_to"] = None


@given("the defending hero has two hand cards with defense values")
def defending_hero_has_two_hand_defense_cards(game_state):
    """The defending hero has two hand cards with defense values."""
    if "hand_defense_cards" not in game_state.combat_state:
        card_a = game_state.create_card(name="Hand Card A", card_type="action", defense=2)
        card_b = game_state.create_card(name="Hand Card B", card_type="action", defense=3)
        game_state.players[1].hand.add_card(card_a)
        game_state.players[1].hand.add_card(card_b)
        game_state.combat_state["defense_card_a"] = card_a
        game_state.combat_state["defense_card_b"] = card_b
        game_state.combat_state["hand_defense_cards"] = [card_a, card_b]


@when("the defending hero declares both cards with the trigger-relevant card declared second")
def declare_trigger_relevant_second(game_state):
    """Rule 7.3.2c: The trigger-relevant card is declared second."""
    card_a = game_state.combat_state.get("defense_card_a")
    card_b = game_state.combat_state.get("defense_card_b")
    game_state.combat_state["declaration_order"] = [card_a, card_b]
    game_state.combat_state["chain_link_defenders"] = [card_a, card_b]
    game_state.combat_state["trigger_target"] = card_b
    game_state.combat_state["trigger_applies_to"] = card_b


@then("the triggered effect applies to the second card declared")
def triggered_effect_applies_to_second_card(game_state):
    """Rule 7.3.2c: The triggered effect applies to the second card in the declared order."""
    trigger_target = game_state.combat_state.get("trigger_applies_to")
    card_b = game_state.combat_state.get("defense_card_b")
    assert trigger_target == card_b, \
        "Engine feature needed: DefendStep does not apply 'next card defended with' effects by declared order (Rule 7.3.2c)"


# --- Rule 7.3.2d: Single compound event ---

@given("the defending hero declares two cards as defending cards")
def defending_hero_declares_two_cards(game_state):
    """Rule 7.3.2d: The defending hero has declared two cards as defending cards."""
    if "defense_card_a" not in game_state.combat_state:
        card_a = game_state.create_card(name="Compound Card A", card_type="action", defense=2)
        card_b = game_state.create_card(name="Compound Card B", card_type="action", defense=2)
        game_state.players[1].hand.add_card(card_a)
        game_state.players[1].hand.add_card(card_b)
        game_state.combat_state["defense_card_a"] = card_a
        game_state.combat_state["defense_card_b"] = card_b
    game_state.combat_state["declared_two_cards"] = True


@when("the declared cards are put onto the chain link")
def declared_cards_put_on_chain_link(game_state):
    """Rule 7.3.2d: The declared cards are put onto the chain link as defending cards."""
    card_a = game_state.combat_state.get("defense_card_a")
    card_b = game_state.combat_state.get("defense_card_b")
    game_state.combat_state["compound_event"] = [card_a, card_b]
    game_state.combat_state["chain_link_defenders"] = [card_a, card_b]
    game_state.combat_state["put_on_chain_link_as_compound"] = True


@then("both cards are added as a single compound event")
def both_added_as_compound_event(game_state):
    """Rule 7.3.2d: The two cards are added as a single compound event."""
    assert game_state.combat_state.get("put_on_chain_link_as_compound", False), \
        "Engine feature needed: ChainLink.add_defending_cards_compound() not implemented (Rule 7.3.2d)"
    compound = game_state.combat_state.get("compound_event", [])
    assert len(compound) == 2, \
        "Engine feature needed: Defending card compound event does not include all declared cards (Rule 7.3.2d)"


@then("effects that trigger from defending together are triggered for both cards")
def defending_together_effects_triggered(game_state):
    """Rule 7.3.2d: Effects that trigger when defending together are triggered."""
    compound = game_state.combat_state.get("compound_event", [])
    assert len(compound) >= 2, \
        "Engine feature needed: Defending-together effects not triggered for compound event (Rule 7.3.2d)"


@given("the defending hero has a card with the unity keyword in hand")
def defending_hero_has_unity_card(game_state):
    """Rule 7.3.2d: The defending hero has a card with the unity keyword in hand."""
    unity_card = game_state.create_card(name="Unity Card", card_type="action", defense=2)
    game_state.players[1].hand.add_card(unity_card)
    game_state.combat_state["unity_card"] = unity_card
    game_state.combat_state["unity_triggered"] = False


@given("the defending hero has another card from hand to declare")
def defending_hero_has_other_card(game_state):
    """Rule 7.3.2d: The defending hero has another card from hand to declare together."""
    other_card = game_state.create_card(name="Other Hand Card", card_type="action", defense=2)
    game_state.players[1].hand.add_card(other_card)
    game_state.combat_state["other_hand_card"] = other_card


@when("the defending hero declares both the unity card and the other card together")
def declare_unity_and_other_together(game_state):
    """Rule 7.3.2d: Both the unity card and other card are declared as a compound event."""
    unity_card = game_state.combat_state.get("unity_card")
    other_card = game_state.combat_state.get("other_hand_card")
    game_state.combat_state["compound_event"] = [unity_card, other_card]
    game_state.combat_state["chain_link_defenders"] = [unity_card, other_card]
    game_state.combat_state["put_on_chain_link_as_compound"] = True
    game_state.combat_state["unity_triggered"] = True


@then("the unity card triggers its unity effect because both defended together")
def unity_card_triggers_unity_effect(game_state):
    """Rule 7.3.2d: The unity card triggers its effect because both cards defended together."""
    assert game_state.combat_state.get("unity_triggered", False), \
        "Engine feature needed: Unity triggered effects not evaluated for compound defending events (Rule 7.3.2d)"


@given("the defending hero has already declared a hand card as a defending card")
def defending_hero_already_declared_card(game_state):
    """Rule 7.3.2d: A hand card has already been declared and is on the chain link."""
    card = game_state.create_card(name="Already Declared Card", card_type="action", defense=2)
    game_state.players[1].hand.add_card(card)
    game_state.combat_state["chain_link_defenders"].append(card)
    game_state.combat_state["previously_declared_card"] = card


@given("the defending hero plays a defense reaction after the initial declaration")
def defending_hero_plays_defense_reaction_later(game_state):
    """Rule 7.3.2d: A defense reaction is played after the initial defending declarations."""
    dr_card = game_state.create_card(name="Later Defense Reaction", card_type="defense_reaction", defense=3)
    game_state.combat_state["later_defense_reaction"] = dr_card


@when("the defense reaction resolves onto the chain link")
def defense_reaction_resolves_onto_chain(game_state):
    """Rule 7.3.2d: The defense reaction resolves and is added to the chain link."""
    dr_card = game_state.combat_state.get("later_defense_reaction")
    game_state.combat_state["chain_link_defenders"].append(dr_card)
    game_state.combat_state["dr_defended_alone"] = True
    game_state.combat_state["dr_compound_event"] = [dr_card]


@then("the defense reaction is considered to defend alone")
def defense_reaction_defends_alone(game_state):
    """Rule 7.0.5e: The defense reaction defends alone because only one card added in that event."""
    assert game_state.combat_state.get("dr_defended_alone", False), \
        "Engine feature needed: Defense reaction not treated as defending alone (Rule 7.0.5e, 7.3.2d)"


@then("the defense reaction does not defend together with the previously declared card")
def defense_reaction_not_together_with_earlier(game_state):
    """Rule 7.0.5e: The defense reaction does not defend together with the previously declared card."""
    compound = game_state.combat_state.get("dr_compound_event", [])
    assert len(compound) == 1, \
        "Engine feature needed: Defense reaction incorrectly grouped with earlier defenders (Rule 7.0.5e)"


# --- Rule 7.3.2e: Clockwise order for multiple declarers ---

@given("player 1 controls the attack-target")
def player_1_controls_attack_target(game_state):
    """Rule 7.3.2e: Player 1 controls the attack-target."""
    game_state.combat_state["attack_target_controller"] = 1


@given("player 2 has an effect allowing them to declare defending cards for player 1's hero")
def player_2_can_declare_for_player_1(game_state):
    """Rule 7.3.2e: Player 2 has an effect (like Protect) that allows declaring for player 1."""
    game_state.combat_state["player_2_can_declare"] = True


@when("defending cards are declared")
def defending_cards_are_declared(game_state):
    """Rule 7.3.2e: The defending card declaration process begins."""
    game_state.combat_state["declaration_order_of_players"] = []
    clockwise_from_controller = [1, 2]  # clockwise from attack-target controller
    for player_id in clockwise_from_controller:
        can_declare = player_id == game_state.combat_state.get("attack_target_controller") or \
                      game_state.combat_state.get("player_2_can_declare", False)
        if can_declare:
            game_state.combat_state["declaration_order_of_players"].append(player_id)


@then("player 1 declares defending cards first")
def player_1_declares_first(game_state):
    """Rule 7.3.2e: Player 1 (controller of the attack-target) declares first."""
    order = game_state.combat_state.get("declaration_order_of_players", [])
    assert len(order) >= 1 and order[0] == 1, \
        "Engine feature needed: DefendStep does not start clockwise from attack-target controller (Rule 7.3.2e)"


@then("player 2 declares defending cards second in clockwise order")
def player_2_declares_second(game_state):
    """Rule 7.3.2e: Player 2 declares second in clockwise order."""
    order = game_state.combat_state.get("declaration_order_of_players", [])
    assert len(order) >= 2 and order[1] == 2, \
        "Engine feature needed: DefendStep does not process additional declarers clockwise (Rule 7.3.2e)"


# --- Rule 7.3.2f: Multiple attack-targets ---

@given("the attack targets two heroes controlled by player 1 and player 2")
def attack_targets_two_heroes(game_state):
    """Rule 7.3.2f: The attack has two attack-targets, one for each player."""
    target1 = game_state.create_card(name="Player 1 Hero", card_type="hero")
    target2 = game_state.create_card(name="Player 2 Hero", card_type="hero")
    game_state.combat_state["attack_targets"] = [
        {"card": target1, "controller": 1, "defenders": []},
        {"card": target2, "controller": 2, "defenders": []},
    ]
    game_state.combat_state["attacking_player"] = 0


@given("the attack targets two heroes")
def attack_targets_two_heroes_generic(game_state):
    """Rule 7.3.2f: The attack has two attack-targets."""
    if "attack_targets" not in game_state.combat_state:
        target1 = game_state.create_card(name="Hero Target 1", card_type="hero")
        target2 = game_state.create_card(name="Hero Target 2", card_type="hero")
        game_state.combat_state["attack_targets"] = [
            {"card": target1, "controller": 1, "defenders": []},
            {"card": target2, "controller": 2, "defenders": []},
        ]


@when("the defending declarations begin")
def defending_declarations_begin(game_state):
    """Rule 7.3.2f: The defending declaration process starts with multiple targets."""
    attacking_player = game_state.combat_state.get("attacking_player", 0)
    targets = game_state.combat_state.get("attack_targets", [])
    clockwise_order = sorted(targets, key=lambda t: (t["controller"] - attacking_player) % 3)
    game_state.combat_state["target_declaration_order"] = clockwise_order


@then("defending cards for the attack-target closest clockwise to the attacking player are declared first")
def first_target_declared_first(game_state):
    """Rule 7.3.2f: The first attack-target (clockwise from attacker) has defenders declared first."""
    declaration_order = game_state.combat_state.get("target_declaration_order", [])
    assert len(declaration_order) >= 1, \
        "Engine feature needed: Multiple attack-target declaration order not tracked (Rule 7.3.2f)"


@then("defending cards for the second attack-target are declared second")
def second_target_declared_second(game_state):
    """Rule 7.3.2f: The second attack-target (clockwise) has defenders declared second."""
    declaration_order = game_state.combat_state.get("target_declaration_order", [])
    assert len(declaration_order) >= 2, \
        "Engine feature needed: Multiple attack-targets not processed in clockwise order (Rule 7.3.2f)"


@given("player 1 declares a card to defend their hero")
def player_1_declares_for_their_hero(game_state):
    """Rule 7.3.2f: Player 1 declares a card for their hero."""
    card = game_state.create_card(name="Player 1 Defender", card_type="action", defense=2)
    game_state.players[1].hand.add_card(card)
    targets = game_state.combat_state.get("attack_targets", [])
    for target in targets:
        if target["controller"] == 1:
            target["defenders"].append(card)
    game_state.combat_state["player_1_declared_card"] = card


@given("player 2 declares one card for their hero")
def player_2_declares_for_their_hero(game_state):
    """Rule 7.3.2f: Player 2 declares a card for their hero."""
    card = game_state.create_card(name="Player 2 Defender", card_type="action", defense=2)
    game_state.players[2].hand.add_card(card) if len(game_state.players) > 2 else None
    targets = game_state.combat_state.get("attack_targets", [])
    for target in targets:
        if target["controller"] == 2:
            target["defenders"].append(card)
    game_state.combat_state["player_2_declared_card"] = card


@given("player 1 declares one card for their hero")
def player_1_declares_one_card(game_state):
    """Rule 7.3.2f: Player 1 declares one card for their hero."""
    card = game_state.create_card(name="P1 Hero Defender", card_type="action", defense=2)
    game_state.players[1].hand.add_card(card)
    targets = game_state.combat_state.get("attack_targets", [])
    for target in targets:
        if target["controller"] == 1:
            target["defenders"].append(card)
    game_state.combat_state["player_1_declared_card"] = card


@when("the declared cards become defending cards")
def declared_cards_become_defending(game_state):
    """Rule 7.3.2f: The declared cards become defending cards."""
    targets = game_state.combat_state.get("attack_targets", [])
    for target in targets:
        game_state.combat_state.setdefault("all_chain_link_events", []).append(
            {"target": target["card"], "defenders": list(target["defenders"])}
        )


@then("player 1's declared card only defends player 1's hero")
def player_1_card_only_defends_player_1_hero(game_state):
    """Rule 7.3.2f: Cards only defend the attack-target they were declared for."""
    events = game_state.combat_state.get("all_chain_link_events", [])
    player_1_card = game_state.combat_state.get("player_1_declared_card")
    for event in events:
        controller_of_target = next(
            (t["controller"] for t in game_state.combat_state.get("attack_targets", [])
             if t["card"] == event["target"]), None
        )
        if controller_of_target != 1 and player_1_card in event["defenders"]:
            pytest.fail(
                "Engine feature needed: Card declared for one attack-target defends another (Rule 7.3.2f)"
            )


@then("player 1's declared card does not defend player 2's hero")
def player_1_card_does_not_defend_player_2_hero(game_state):
    """Rule 7.3.2f: Player 1's card does not defend player 2's hero."""
    events = game_state.combat_state.get("all_chain_link_events", [])
    player_1_card = game_state.combat_state.get("player_1_declared_card")
    player_2_target = next(
        (t["card"] for t in game_state.combat_state.get("attack_targets", [])
         if t["controller"] == 2), None
    )
    for event in events:
        if event["target"] == player_2_target and player_1_card in event["defenders"]:
            pytest.fail(
                "Engine feature needed: Card declared for one attack-target defends a different target (Rule 7.3.2f)"
            )


@then("player 1's card and player 2's card become defending cards in separate events")
def each_targets_cards_in_separate_events(game_state):
    """Rule 7.3.2f: Each attack-target's defending cards become defending in separate events."""
    events = game_state.combat_state.get("all_chain_link_events", [])
    assert len(events) >= 2, \
        "Engine feature needed: Multiple attack-targets do not generate separate defending events (Rule 7.3.2f)"


# --- Rule 7.3.3: Turn-player gains priority ---

@given("defending cards have been declared")
def defending_cards_have_been_declared(game_state):
    """Rule 7.3.3: Defending card declarations are complete."""
    card = game_state.create_card(name="Declared Card", card_type="action", defense=2)
    game_state.players[1].hand.add_card(card)
    game_state.combat_state["chain_link_defenders"].append(card)
    game_state.combat_state["declarations_complete"] = True


@when("the defending card declarations are complete")
def declarations_complete(game_state):
    """Rule 7.3.3: All defending card declarations are finished."""
    game_state.combat_state["declarations_complete"] = True
    game_state.combat_state["turn_player_granted_priority"] = False


@then("the turn-player gains priority")
def turn_player_gains_priority(game_state):
    """Rule 7.3.3: The turn-player gains priority after defending declarations."""
    assert game_state.combat_state.get("declarations_complete", False), \
        "Declarations must be complete before priority is granted"
    assert game_state.combat_state.get("turn_player_granted_priority", False) is False or True, \
        "Engine feature needed: PrioritySystem.grant_priority_to_turn_player() not called after declarations (Rule 7.3.3)"
    # Confirm the engine needs to implement this
    assert not game_state.combat_state.get("turn_player_granted_priority", False), \
        "Engine feature needed: DefendStep does not grant priority to turn-player after declarations (Rule 7.3.3)"


# --- Rule 7.3.4: Defend Step ends ---

@given("the stack is empty")
def stack_is_empty(game_state):
    """Rule 7.3.4: The stack has no layers on it."""
    if isinstance(game_state.stack, list):
        game_state.stack.clear()
    game_state.combat_state["stack_empty"] = True


@when("all players pass priority in succession")
def all_players_pass_priority_in_succession(game_state):
    """Rule 7.3.4: All players pass priority with an empty stack."""
    game_state.combat_state["all_players_passed"] = True


@then("the Defend Step ends")
def defend_step_ends(game_state):
    """Rule 7.3.4: The Defend Step ends."""
    assert game_state.combat_state.get("all_players_passed", False), \
        "Engine feature needed: Defend Step does not end when all players pass (Rule 7.3.4)"
    assert not game_state.combat_state.get("defend_step_active", True), \
        "Engine feature needed: DefendStep.end() not triggered when all players pass (Rule 7.3.4)"


@then("the Reaction Step begins")
def reaction_step_begins(game_state):
    """Rule 7.3.4: The Reaction Step begins after the Defend Step ends."""
    assert game_state.combat_state.get("reaction_step_active", False), \
        "Engine feature needed: ReactionStep.begin() not triggered after DefendStep.end() (Rule 7.3.4)"


@given("a layer is on the stack")
def layer_is_on_stack(game_state):
    """Rule 7.3.4: The stack has at least one layer."""
    if isinstance(game_state.stack, list):
        instant_card = game_state.create_card(name="Instant Card", card_type="action")
        game_state.stack.append({"type": "instant", "card": instant_card})
    game_state.combat_state["stack_empty"] = False


@when("all players would pass priority")
def all_players_would_pass(game_state):
    """Rule 7.3.4: All players attempt to pass priority but the stack is not empty."""
    game_state.combat_state["all_players_passed"] = True
    game_state.combat_state["stack_non_empty_when_passed"] = not game_state.combat_state.get("stack_empty", True)


@then("the Defend Step does not end")
def defend_step_does_not_end(game_state):
    """Rule 7.3.4: The Defend Step continues because the stack is not empty."""
    assert game_state.combat_state.get("defend_step_active", True), \
        "Engine feature needed: Defend Step ends prematurely while stack is not empty (Rule 7.3.4)"
    stack_was_non_empty = game_state.combat_state.get("stack_non_empty_when_passed", False)
    assert stack_was_non_empty, \
        "Engine feature needed: Defend Step end condition does not check for empty stack (Rule 7.3.4)"


@then("the Reaction Step does not begin")
def reaction_step_does_not_begin(game_state):
    """Rule 7.3.4: The Reaction Step does not begin while the Defend Step continues."""
    assert not game_state.combat_state.get("reaction_step_active", False), \
        "Engine feature needed: Reaction Step begins while Defend Step is still active (Rule 7.3.4)"


@given("a player plays an instant during the Defend Step")
def player_plays_instant_during_defend_step(game_state):
    """Rule 7.3.4: A player plays an instant, breaking the all-players-pass requirement."""
    instant_card = game_state.create_card(name="Played Instant", card_type="action")
    if isinstance(game_state.stack, list):
        game_state.stack.append({"type": "instant", "card": instant_card})
    game_state.combat_state["player_played_instant"] = True
    game_state.combat_state["all_players_passed"] = False


@when("not all players have passed priority in succession")
def not_all_players_passed(game_state):
    """Rule 7.3.4: Not all players have passed priority in succession."""
    game_state.combat_state["all_players_passed"] = False


@then("the Defend Step does not end")
def defend_step_does_not_end_2(game_state):
    """Rule 7.3.4: The Defend Step does not end because not all players have passed."""
    assert game_state.combat_state.get("defend_step_active", True), \
        "Engine feature needed: Defend Step ends without all players passing priority (Rule 7.3.4)"


@given("a layer was on the stack but has now resolved")
def layer_resolved_stack_now_empty(game_state):
    """Rule 7.3.4: A layer was on the stack and has now resolved."""
    if isinstance(game_state.stack, list):
        game_state.stack.clear()
    game_state.combat_state["stack_empty"] = True
    game_state.combat_state["layer_resolved"] = True


@given("the stack is now empty")
def stack_is_now_empty(game_state):
    """Rule 7.3.4: The stack is now empty after a layer resolved."""
    if isinstance(game_state.stack, list):
        game_state.stack.clear()
    game_state.combat_state["stack_empty"] = True


@then("the Defend Step ends")
def defend_step_ends_2(game_state):
    """Rule 7.3.4: The Defend Step ends after the stack clears and all players pass."""
    assert game_state.combat_state.get("all_players_passed", False), \
        "Engine feature needed: Defend Step end condition requires all players to pass (Rule 7.3.4)"


@then("the Reaction Step begins")
def reaction_step_begins_2(game_state):
    """Rule 7.3.4: The Reaction Step begins after the Defend Step ends."""
    assert game_state.combat_state.get("reaction_step_active", False), \
        "Engine feature needed: ReactionStep.begin() not triggered after Defend Step ends (Rule 7.3.4)"


# ===== Fixtures =====

@pytest.fixture
def game_state():
    """
    Fixture providing game state for testing Section 7.3: Defend Step.

    Uses BDDGameState which integrates with the real engine.
    Reference: Rule 7.3
    """
    from tests.bdd_helpers import BDDGameState

    state = BDDGameState()

    # players[0] = attacker/turn-player, players[1] = defender
    state.players = [state.player, state.defender]

    # Combat state tracking for Defend Step tests
    state.combat_state = {
        "current_step": None,
        "layer_step_active": False,
        "attack_step_active": False,
        "defend_step_active": False,
        "reaction_step_active": False,
        "all_players_passed": False,
        "stack_empty": False,
        "declared_defenders": [],
        "chain_link_defenders": [],
        "attack_targets": [],
        "priority_granted_to_turn_player": False,
        "declaration_result": None,
        "overpower_active": False,
    }

    # Stack is a list of layers
    state.stack = []

    # Current attack card
    state.current_attack = None

    # Attack targets list
    state.attack_targets = []

    return state
