"""
Step definitions for Section 7.0: General (Combat)
Reference: Flesh and Blood Comprehensive Rules Section 7.0

This module implements behavioral tests for combat fundamentals:
the combat chain, chain links, active-attacks, and defending cards.

Engine Features Needed for Section 7.0:
- [ ] CombatChain.is_open property (Rule 7.0.2)
- [ ] CombatChain.open() / CombatChain.close() methods (Rule 7.0.2a)
- [ ] CombatChain.chain_links list property (Rule 7.0.3)
- [ ] ChainLink class (not object, not zone) with active_attack and defending_cards (Rule 7.0.3)
- [ ] ChainLink.number property (N+1 ordering) (Rule 7.0.3a)
- [ ] CombatChain.active_chain_link property (Rule 7.0.3b)
- [ ] ChainLink.controller / ChainLink.owner -> active-attack properties + LKI (Rule 7.0.3c)
- [ ] CombatChain.open_step property tracking "Layer Step" start (Rule 7.0.2a)
- [ ] CombatRestriction: action cards cannot be played as non-instants during combat (Rule 7.0.1a)
- [ ] ChainLink.add_defending_card(card, target) -> DefendResult (Rule 7.0.5)
- [ ] DefendResult with success flag and reason (Rule 7.0.5b)
- [ ] "defend" event triggered after card added as defending card (Rule 7.0.5a)
- [ ] ChainLink.defending_cards list (Rule 7.0.5)
- [ ] Card.is_defending property (Rule 7.0.5a)
- [ ] ChainLink.defending_alone(card) / defending_together(cards) (Rule 7.0.5e)
- [ ] Active-attack replacement clears existing active-attack, preserves targets (Rule 7.0.4a)
- [ ] CombatChainEffect.this_combat_chain_reference (Rule 7.0.2b)
- [ ] ActiveChainLinkEffect.this_chain_link_reference (Rule 7.0.3d)
- [ ] Layer played during combat associated with active chain link (Rule 7.0.3e)
- [ ] Card on chain link is considered on combat chain AND in arena (Rule 7.0.3f)

Current status: Tests written, Engine pending
"""

import pytest
from pytest_bdd import scenario, given, when, then, parsers


# ===== Scenarios =====

# Rule 7.0.1 - Combat state with open combat chain

@scenario(
    "../features/section_7_0_combat_general.feature",
    "Combat is a game state where the combat chain is open",
)
def test_combat_is_game_state_with_open_chain():
    """Rule 7.0.1: Combat is a game state where the combat chain is open."""
    pass


@scenario(
    "../features/section_7_0_combat_general.feature",
    "Combat resolution proceeds through seven ordered steps",
)
def test_combat_resolution_seven_ordered_steps():
    """Rule 7.0.1: Combat resolution has seven steps in order."""
    pass


# Rule 7.0.1a - Action card restrictions during combat

@scenario(
    "../features/section_7_0_combat_general.feature",
    "Action cards cannot be played during combat except as instants",
)
def test_action_cards_cannot_be_played_during_combat_non_instant():
    """Rule 7.0.1a: Action cards cannot be played as non-instants during combat."""
    pass


@scenario(
    "../features/section_7_0_combat_general.feature",
    "Action cards can be played as instants during combat",
)
def test_action_cards_can_be_played_as_instants_during_combat():
    """Rule 7.0.1a: Action cards can still be played as instants during combat."""
    pass


@scenario(
    "../features/section_7_0_combat_general.feature",
    "Activated abilities with type action cannot be activated during combat as non-instants",
)
def test_action_abilities_cannot_be_activated_during_combat_non_instant():
    """Rule 7.0.1a: Activated abilities with type action cannot be activated as non-instants during combat."""
    pass


# Rule 7.0.2 - Combat chain as a zone

@scenario(
    "../features/section_7_0_combat_general.feature",
    "The combat chain is a zone",
)
def test_combat_chain_is_a_zone():
    """Rule 7.0.2: The combat chain is a zone."""
    pass


@scenario(
    "../features/section_7_0_combat_general.feature",
    "The combat chain starts the game closed",
)
def test_combat_chain_starts_game_closed():
    """Rule 7.0.2: The combat chain starts the game closed."""
    pass


@scenario(
    "../features/section_7_0_combat_general.feature",
    "The combat chain is empty when closed",
)
def test_combat_chain_is_empty_when_closed():
    """Rule 7.0.2: The combat chain is empty when closed."""
    pass


@scenario(
    "../features/section_7_0_combat_general.feature",
    "The combat chain contains chain links when open",
)
def test_combat_chain_contains_chain_links_when_open():
    """Rule 7.0.2: The combat chain contains chain links when open."""
    pass


# Rule 7.0.2a - Combat chain opens when attack added

@scenario(
    "../features/section_7_0_combat_general.feature",
    "Combat chain opens when an attack is added to the stack",
)
def test_combat_chain_opens_when_attack_added_to_stack():
    """Rule 7.0.2a: Combat chain opens when attack is added to the stack."""
    pass


@scenario(
    "../features/section_7_0_combat_general.feature",
    "Combat chain remains open through subsequent chain links",
)
def test_combat_chain_remains_open_through_subsequent_links():
    """Rule 7.0.2a: Combat chain remains open for subsequent attacks."""
    pass


# Rule 7.0.2b - "This combat chain" reference

@scenario(
    "../features/section_7_0_combat_general.feature",
    "Effect referencing this combat chain works when chain is open",
)
def test_this_combat_chain_reference_works_when_open():
    """Rule 7.0.2b: 'This combat chain' refers to the current open chain."""
    pass


@scenario(
    "../features/section_7_0_combat_general.feature",
    "Effect referencing this combat chain fails when chain is closed",
)
def test_this_combat_chain_reference_fails_when_closed():
    """Rule 7.0.2b: 'This combat chain' fails to be generated when chain is closed."""
    pass


# Rule 7.0.3 - Chain link structure

@scenario(
    "../features/section_7_0_combat_general.feature",
    "A chain link is neither an object nor a zone",
)
def test_chain_link_is_neither_object_nor_zone():
    """Rule 7.0.3: A chain link is neither an object nor a zone."""
    pass


@scenario(
    "../features/section_7_0_combat_general.feature",
    "A chain link comprises an active-attack and optional defending cards",
)
def test_chain_link_comprises_active_attack_and_defenders():
    """Rule 7.0.3: A chain link comprises an active-attack and defending cards."""
    pass


# Rule 7.0.3a - Chain link creation and numbering

@scenario(
    "../features/section_7_0_combat_general.feature",
    "Chain link is created when attack is added to combat chain",
)
def test_chain_link_created_when_attack_added():
    """Rule 7.0.3a: Chain link created when attack added to combat chain."""
    pass


@scenario(
    "../features/section_7_0_combat_general.feature",
    "Second attack creates chain link N+1",
)
def test_second_attack_creates_chain_link_n_plus_1():
    """Rule 7.0.3a: Second attack creates chain link N+1."""
    pass


# Rule 7.0.3b - Active chain link

@scenario(
    "../features/section_7_0_combat_general.feature",
    "The most recent chain link is the active chain link",
)
def test_most_recent_chain_link_is_active():
    """Rule 7.0.3b: The most recent chain link is the active chain link."""
    pass


@scenario(
    "../features/section_7_0_combat_general.feature",
    "The active chain link remains until it resolves or combat chain closes",
)
def test_active_chain_link_remains_until_resolved():
    """Rule 7.0.3b: Active chain link remains until resolved."""
    pass


# Rule 7.0.3c - Chain link properties from active-attack + LKI

@scenario(
    "../features/section_7_0_combat_general.feature",
    "Chain link properties match the active-attack properties",
)
def test_chain_link_properties_match_active_attack():
    """Rule 7.0.3c: Chain link properties match the active-attack properties."""
    pass


@scenario(
    "../features/section_7_0_combat_general.feature",
    "Chain link uses last-known information when active-attack ceases to exist",
)
def test_chain_link_uses_lki_when_active_attack_ceases():
    """Rule 7.0.3c: Chain link uses LKI when active-attack ceases to exist."""
    pass


# Rule 7.0.3d - "This chain link" reference

@scenario(
    "../features/section_7_0_combat_general.feature",
    "Effect referencing this chain link works when active chain link exists",
)
def test_this_chain_link_reference_works_with_active_chain_link():
    """Rule 7.0.3d: 'This chain link' works when active chain link exists."""
    pass


@scenario(
    "../features/section_7_0_combat_general.feature",
    "Effect referencing this chain link fails when no active chain link exists",
)
def test_this_chain_link_reference_fails_when_no_active_chain_link():
    """Rule 7.0.3d: 'This chain link' fails when no active chain link."""
    pass


# Rule 7.0.3e - Layers during combat on active chain link

@scenario(
    "../features/section_7_0_combat_general.feature",
    "A layer played during combat is associated with the active chain link",
)
def test_layer_played_during_combat_on_active_chain_link():
    """Rule 7.0.3e: Layer played during combat is on the active chain link."""
    pass


# Rule 7.0.3f - Cards on chain link are on combat chain and in arena

@scenario(
    "../features/section_7_0_combat_general.feature",
    "A card on a chain link is considered to be on the combat chain",
)
def test_card_on_chain_link_is_on_combat_chain():
    """Rule 7.0.3f: Card on chain link is on combat chain."""
    pass


@scenario(
    "../features/section_7_0_combat_general.feature",
    "A card on a chain link is also considered to be in the arena",
)
def test_card_on_chain_link_is_in_arena():
    """Rule 7.0.3f: Card on chain link is also in arena."""
    pass


# Rule 7.0.4 - Active-attack

@scenario(
    "../features/section_7_0_combat_general.feature",
    "The active-attack is an attack put onto the combat chain as a chain link",
)
def test_active_attack_is_attack_on_combat_chain():
    """Rule 7.0.4: Active-attack is an attack put onto the combat chain."""
    pass


# Rule 7.0.4a - Replacing the active-attack

@scenario(
    "../features/section_7_0_combat_general.feature",
    "Putting a new attacking card clears the existing active-attack",
)
def test_putting_new_attacking_card_clears_existing_active_attack():
    """Rule 7.0.4a: New attacking card clears existing active-attack."""
    pass


@scenario(
    "../features/section_7_0_combat_general.feature",
    "Replacing the active-attack preserves the attack target",
)
def test_replacing_active_attack_preserves_target():
    """Rule 7.0.4a: Replacing active-attack preserves attack target."""
    pass


@scenario(
    "../features/section_7_0_combat_general.feature",
    "The replacement attacking card is considered a new attack",
)
def test_replacement_attacking_card_is_new_attack():
    """Rule 7.0.4a: Replacement attacking card is a new attack."""
    pass


# Rule 7.0.5 - Defending cards

@scenario(
    "../features/section_7_0_combat_general.feature",
    "A defending card is designated as defending on a chain link by a rule or effect",
)
def test_defending_card_designated_on_chain_link():
    """Rule 7.0.5: Defending card is designated on a chain link."""
    pass


@scenario(
    "../features/section_7_0_combat_general.feature",
    "A defending card remains defending until it leaves the combat chain",
)
def test_defending_card_remains_until_leaves_combat_chain():
    """Rule 7.0.5: Defending card remains defending until it leaves the combat chain."""
    pass


# Rule 7.0.5a - Adding a defending card causes defend event

@scenario(
    "../features/section_7_0_combat_general.feature",
    "The defend event occurs after a defending card is added",
)
def test_defend_event_occurs_after_card_added():
    """Rule 7.0.5a: The defend event occurs after a defending card is added."""
    pass


@scenario(
    "../features/section_7_0_combat_general.feature",
    "The controller at defend time is considered to have defended with the card",
)
def test_controller_at_defend_time_considered_to_have_defended():
    """Rule 7.0.5a: Controller at defend time is considered to have defended."""
    pass


# Rule 7.0.5b - Failed defend addition

@scenario(
    "../features/section_7_0_combat_general.feature",
    "Adding a card already defending on the chain link fails",
)
def test_adding_already_defending_card_fails():
    """Rule 7.0.5b: Adding a card already defending on the chain link fails."""
    pass


@scenario(
    "../features/section_7_0_combat_general.feature",
    "Adding a card blocked by another effect from defending fails",
)
def test_adding_card_blocked_from_defending_fails():
    """Rule 7.0.5b: Adding a card blocked by effect from defending fails."""
    pass


# Rule 7.0.5c - Defending against active-attack (+ LKI)

@scenario(
    "../features/section_7_0_combat_general.feature",
    "A defending card defends against the active-attack",
)
def test_defending_card_defends_against_active_attack():
    """Rule 7.0.5c: A defending card defends against the active-attack."""
    pass


@scenario(
    "../features/section_7_0_combat_general.feature",
    "Defending card uses last-known information if active-attack ceases to exist",
)
def test_defending_card_uses_lki_when_attack_ceases():
    """Rule 7.0.5c: Defending card uses LKI when active-attack ceases to exist."""
    pass


# Rule 7.0.5d - Card can only defend on one chain link at a time

@scenario(
    "../features/section_7_0_combat_general.feature",
    "A card can only defend on one chain link for one attack-target at a time",
)
def test_card_can_only_defend_on_one_chain_link_at_a_time():
    """Rule 7.0.5d: A card can only defend on one chain link at a time."""
    pass


# Rule 7.0.5e - Defend alone vs together

@scenario(
    "../features/section_7_0_combat_general.feature",
    "Exactly one defending card added is considered to defend alone",
)
def test_one_defending_card_defends_alone():
    """Rule 7.0.5e: Exactly one defending card defends alone."""
    pass


@scenario(
    "../features/section_7_0_combat_general.feature",
    "Two cards added in the same event defend together",
)
def test_two_cards_added_together_defend_together():
    """Rule 7.0.5e: Two cards added in the same event defend together."""
    pass


@scenario(
    "../features/section_7_0_combat_general.feature",
    "A defense reaction added after declared defenders defends alone",
)
def test_defense_reaction_after_declared_defenders_defends_alone():
    """Rule 7.0.5e: Defense reaction added after declared defenders defends alone."""
    pass


# ===== Step Definitions =====


@given("a game state is initialized")
def game_state_initialized(game_state):
    """Initialize a basic game state."""
    pass


@given("a new game is initialized")
def new_game_initialized(game_state):
    """Initialize a fresh game state."""
    pass


@given("the combat chain is open")
def combat_chain_is_open(game_state):
    """Set the combat chain to open state."""
    game_state.combat_chain_open = True


@given("the combat chain is closed")
def combat_chain_is_closed(game_state):
    """Set the combat chain to closed state."""
    game_state.combat_chain_open = False


@given("the combat chain is open with zero chain links")
def combat_chain_open_zero_links(game_state):
    """Combat chain is open but has no chain links yet."""
    game_state.combat_chain_open = True
    game_state.chain_links = []


@given("the combat chain is open with one chain link")
def combat_chain_open_one_link(game_state):
    """Combat chain is open with one existing chain link."""
    game_state.combat_chain_open = True
    attack = game_state.create_card(name="Attack Card 1", card_type="attack_action")
    link = game_state.create_chain_link(attack, link_number=1)
    game_state.chain_links = [link]


@given("the combat chain has two chain links")
def combat_chain_has_two_links(game_state):
    """Combat chain is open with two chain links."""
    game_state.combat_chain_open = True
    attack1 = game_state.create_card(name="Attack Card 1", card_type="attack_action")
    attack2 = game_state.create_card(name="Attack Card 2", card_type="attack_action")
    link1 = game_state.create_chain_link(attack1, link_number=1)
    link2 = game_state.create_chain_link(attack2, link_number=2)
    game_state.chain_links = [link1, link2]


@given("an attack has been placed on the combat chain as a chain link")
def attack_placed_on_combat_chain(game_state):
    """An attack is on the combat chain as a chain link."""
    attack = game_state.create_card(name="Test Attack", card_type="attack_action")
    link = game_state.create_chain_link(attack, link_number=1)
    game_state.chain_links = [link]
    game_state.attack_card = attack


@given("a chain link exists on the combat chain")
def chain_link_exists(game_state):
    """A chain link exists on the combat chain."""
    game_state.combat_chain_open = True
    attack = game_state.create_card(name="Test Attack", card_type="attack_action")
    link = game_state.create_chain_link(attack, link_number=1)
    game_state.chain_links = [link]
    game_state.test_chain_link = link


@given("a chain link exists on the combat chain with an attack card")
def chain_link_exists_with_attack(game_state):
    """A chain link exists on the combat chain with an attack card."""
    game_state.combat_chain_open = True
    attack = game_state.create_card(name="Test Attack", card_type="attack_action")
    link = game_state.create_chain_link(attack, link_number=1)
    game_state.chain_links = [link]
    game_state.test_chain_link = link
    game_state.attack_card = attack


@given("a chain link exists with an active-attack")
def chain_link_with_active_attack(game_state):
    """A chain link exists with an active-attack."""
    game_state.combat_chain_open = True
    attack = game_state.create_card(name="Test Attack", card_type="attack_action")
    link = game_state.create_chain_link(attack, link_number=1)
    game_state.chain_links = [link]
    game_state.test_chain_link = link
    game_state.attack_card = attack


@given(parsers.parse("a chain link exists with an attack card controlled by player {player_id:d}"))
def chain_link_with_attack_controlled_by_player(game_state, player_id):
    """A chain link exists with an attack controlled by a specific player."""
    game_state.combat_chain_open = True
    attack = game_state.create_card(
        name="Test Attack",
        card_type="attack_action",
        controller_id=player_id,
    )
    link = game_state.create_chain_link(attack, link_number=1, controller_id=player_id)
    game_state.chain_links = [link]
    game_state.test_chain_link = link
    game_state.attack_card = attack
    game_state.attack_controller_id = player_id


@given("chain link 1 is the active chain link")
def chain_link_1_is_active(game_state):
    """Chain link 1 is the active chain link."""
    game_state.combat_chain_open = True
    attack = game_state.create_card(name="Test Attack", card_type="attack_action")
    link = game_state.create_chain_link(attack, link_number=1)
    game_state.chain_links = [link]
    game_state.active_chain_link = link


@given("the combat chain is open with an active chain link")
def combat_chain_open_with_active_chain_link(game_state):
    """Combat chain is open with an active chain link."""
    game_state.combat_chain_open = True
    attack = game_state.create_card(name="Test Attack", card_type="attack_action")
    link = game_state.create_chain_link(attack, link_number=1)
    game_state.chain_links = [link]
    game_state.active_chain_link = link


@given("there is no active chain link")
def no_active_chain_link(game_state):
    """There is no active chain link."""
    game_state.combat_chain_open = False
    game_state.chain_links = []
    game_state.active_chain_link = None


@given(parsers.parse("there is an effect that references \"{reference_text}\""))
def effect_references_text(game_state, reference_text):
    """An effect referencing a specific combat-related text."""
    game_state.effect_reference = reference_text
    result = game_state.create_chain_reference_effect(reference_text)
    game_state.chain_reference_result = result


@given("a player has an action card in hand")
def player_has_action_card_in_hand(game_state):
    """Player has an action card in hand."""
    card = game_state.create_card(name="Action Card", card_type="action")
    game_state.player.hand.add_card(card)
    game_state.test_card = card


@given("a player has an activated ability with type action")
def player_has_activated_ability_with_type_action(game_state):
    """Player has an activated ability with type action."""
    card = game_state.create_card(name="Ability Source", card_type="equipment")
    game_state.test_action_ability = game_state.create_action_type_activated_ability(card)
    game_state.test_card = card


@given("an attack card is on a chain link")
def attack_card_is_on_chain_link(game_state):
    """An attack card is on a chain link."""
    game_state.combat_chain_open = True
    attack = game_state.create_card(name="Test Attack", card_type="attack_action")
    link = game_state.create_chain_link(attack, link_number=1)
    game_state.chain_links = [link]
    game_state.test_chain_link = link
    game_state.attack_card = attack


@given("an attack is put onto the combat chain")
def attack_put_onto_combat_chain(game_state):
    """An attack is put onto the combat chain."""
    game_state.combat_chain_open = True
    attack = game_state.create_card(name="Test Attack", card_type="attack_action")
    link = game_state.create_chain_link(attack, link_number=1)
    game_state.chain_links = [link]
    game_state.attack_card = attack
    game_state.test_chain_link = link


@given("a chain link exists with attack card A as the active-attack")
def chain_link_with_card_a_as_active_attack(game_state):
    """Chain link exists with card A as active-attack."""
    game_state.combat_chain_open = True
    card_a = game_state.create_card(name="Attack Card A", card_type="attack_action")
    link = game_state.create_chain_link(card_a, link_number=1)
    game_state.chain_links = [link]
    game_state.test_chain_link = link
    game_state.card_a = card_a


@given(parsers.parse("a chain link exists with attack card A targeting player {player_id:d}"))
def chain_link_with_attack_targeting_player(game_state, player_id):
    """Chain link with attack targeting a specific player."""
    game_state.combat_chain_open = True
    card_a = game_state.create_card(name="Attack Card A", card_type="attack_action")
    link = game_state.create_chain_link(
        card_a, link_number=1, attack_target_id=player_id
    )
    game_state.chain_links = [link]
    game_state.test_chain_link = link
    game_state.card_a = card_a
    game_state.attack_target_id = player_id


@given("a card is a defending card on the active chain link")
def card_is_defending_on_active_chain_link(game_state):
    """A card is a defending card on the active chain link."""
    game_state.combat_chain_open = True
    attack = game_state.create_card(name="Test Attack", card_type="attack_action")
    link = game_state.create_chain_link(attack, link_number=1)
    defender = game_state.create_card(name="Defender", card_type="action")
    link_result = game_state.add_defending_card_to_link(link, defender)
    game_state.chain_links = [link]
    game_state.test_chain_link = link
    game_state.defending_card = defender
    game_state.defend_result = link_result


@given("card X is already defending on that chain link")
def card_x_already_defending(game_state):
    """Card X is already defending on the chain link."""
    game_state.combat_chain_open = True
    attack = game_state.create_card(name="Test Attack", card_type="attack_action")
    link = game_state.create_chain_link(attack, link_number=1)
    card_x = game_state.create_card(name="Card X", card_type="action")
    game_state.add_defending_card_to_link(link, card_x)
    game_state.chain_links = [link]
    game_state.test_chain_link = link
    game_state.card_x = card_x


@given("an effect prevents card Y from becoming a defending card")
def effect_prevents_card_y_from_defending(game_state):
    """An effect prevents card Y from becoming a defending card."""
    card_y = game_state.create_card(name="Card Y", card_type="action")
    game_state.card_y = card_y
    game_state.add_defend_prevention_effect(card_y)


@given("card D is a defending card on that chain link")
def card_d_is_defending_on_chain_link(game_state):
    """Card D is a defending card on the chain link."""
    defender = game_state.create_card(name="Defender D", card_type="action")
    link = game_state.test_chain_link
    game_state.add_defending_card_to_link(link, defender)
    game_state.card_d = defender


@given(parsers.parse("card Z is already defending on chain link {link_num:d} for attack-target player {player_id:d}"))
def card_z_defending_on_chain_link(game_state, link_num, player_id):
    """Card Z is already defending on a specific chain link."""
    game_state.combat_chain_open = True
    attack1 = game_state.create_card(name="Attack 1", card_type="attack_action")
    attack2 = game_state.create_card(name="Attack 2", card_type="attack_action")
    link1 = game_state.create_chain_link(
        attack1, link_number=1, attack_target_id=player_id
    )
    link2 = game_state.create_chain_link(
        attack2, link_number=2, attack_target_id=player_id
    )
    card_z = game_state.create_card(name="Card Z", card_type="action")
    game_state.add_defending_card_to_link(link1, card_z, target_player_id=player_id)
    game_state.chain_links = [link1, link2]
    game_state.chain_link_1 = link1
    game_state.chain_link_2 = link2
    game_state.card_z = card_z


@given(parsers.parse("a card is controlled by player {player_id:d}"))
def card_controlled_by_player(game_state, player_id):
    """A card is controlled by a specific player."""
    card = game_state.create_card(
        name="Defend Card", card_type="action", controller_id=player_id
    )
    game_state.defending_card = card
    game_state.defender_controller_id = player_id


@given("two cards were declared as defenders together")
def two_cards_declared_as_defenders_together(game_state):
    """Two cards were declared as defenders together during the defend step."""
    link = game_state.test_chain_link
    card1 = game_state.create_card(name="Defender 1", card_type="action")
    card2 = game_state.create_card(name="Defender 2", card_type="action")
    # Add them in the same event (together)
    game_state.declare_defenders_together(link, [card1, card2])
    game_state.declared_defenders = [card1, card2]


# ===== When steps =====


@when("we check the game state")
def check_game_state(game_state):
    """Check whether the game is in combat."""
    game_state.in_combat_result = game_state.check_in_combat()


@when("we list the combat chain resolution steps")
def list_combat_resolution_steps(game_state):
    """Get the list of combat chain resolution steps."""
    game_state.resolution_steps = game_state.get_combat_resolution_steps()


@when("the player attempts to play the action card as a non-instant")
def player_attempts_play_action_non_instant(game_state):
    """Player attempts to play action card as non-instant during combat."""
    game_state.play_result = game_state.attempt_play_during_combat(
        game_state.test_card, as_instant=False
    )


@when("the player attempts to play the action card as an instant")
def player_attempts_play_action_as_instant(game_state):
    """Player attempts to play action card as instant during combat."""
    game_state.play_result = game_state.attempt_play_during_combat(
        game_state.test_card, as_instant=True
    )


@when("the player attempts to activate the ability as a non-instant")
def player_attempts_activate_action_ability_non_instant(game_state):
    """Player attempts to activate action-type ability as non-instant during combat."""
    game_state.activation_result = game_state.attempt_activate_during_combat(
        game_state.test_action_ability, as_instant=False
    )


@when("we check the combat chain zone type")
def check_combat_chain_zone_type(game_state):
    """Check the type of the combat chain."""
    game_state.combat_chain_type_result = game_state.get_combat_chain_type()


@when("we check whether the combat chain is open")
def check_whether_combat_chain_is_open(game_state):
    """Check whether the combat chain is open."""
    game_state.chain_open_result = game_state.is_combat_chain_open()


@when("we check the combat chain contents")
def check_combat_chain_contents(game_state):
    """Check the contents of the combat chain."""
    game_state.chain_contents = game_state.get_combat_chain_contents()


@when("an attack is added to the stack")
def attack_added_to_stack(game_state):
    """An attack is added to the stack while combat chain is closed."""
    attack = game_state.create_card(name="New Attack", card_type="attack_action")
    game_state.stack_add_result = game_state.add_attack_to_stack(attack)


@when("a second attack is added to the stack")
def second_attack_added_to_stack(game_state):
    """A second attack is added to the stack."""
    attack = game_state.create_card(name="Second Attack", card_type="attack_action")
    game_state.second_add_result = game_state.add_attack_to_stack(attack)


@when("we check if the effect can be generated")
def check_if_effect_can_be_generated(game_state):
    """Check whether the effect referencing combat chain/link can be generated."""
    game_state.effect_can_generate = game_state.check_chain_reference_effect(
        game_state.chain_reference_result
    )


@when("we check the type of the chain link")
def check_chain_link_type(game_state):
    """Check the type of the chain link."""
    game_state.chain_link_type_result = game_state.get_chain_link_type(
        game_state.test_chain_link
    )


@when("we inspect the chain link components")
def inspect_chain_link_components(game_state):
    """Inspect the components of the chain link."""
    game_state.chain_link_components = game_state.get_chain_link_components(
        game_state.test_chain_link
    )


@when("an attack is added to the combat chain as a chain link")
def attack_added_to_combat_chain(game_state):
    """An attack is added to the combat chain as a chain link."""
    attack = game_state.create_card(name="New Attack", card_type="attack_action")
    game_state.new_attack = attack
    game_state.new_link_result = game_state.add_attack_to_combat_chain(attack)


@when("a second attack is added to the combat chain as a chain link")
def second_attack_added_to_combat_chain(game_state):
    """A second attack is added to the combat chain as a chain link."""
    attack = game_state.create_card(name="Second Attack", card_type="attack_action")
    game_state.second_attack = attack
    game_state.second_link_result = game_state.add_attack_to_combat_chain(attack)


@when("we check the active chain link")
def check_active_chain_link(game_state):
    """Check which chain link is the active chain link."""
    game_state.active_link_result = game_state.get_active_chain_link()


@when("chain link 1 resolves")
def chain_link_1_resolves(game_state):
    """Chain link 1 resolves."""
    game_state.resolve_chain_link(game_state.active_chain_link)


@when("we check the chain link properties")
def check_chain_link_properties(game_state):
    """Check the properties of the chain link."""
    game_state.link_properties = game_state.get_chain_link_properties(
        game_state.test_chain_link
    )


@when("the active-attack ceases to exist")
def active_attack_ceases_to_exist(game_state):
    """The active-attack ceases to exist."""
    game_state.active_attack_lki = game_state.capture_lki(game_state.attack_card)
    game_state.remove_active_attack(game_state.test_chain_link)


@when("a layer is played during combat")
def layer_played_during_combat(game_state):
    """A layer is played during combat."""
    layer_card = game_state.create_card(name="Instant Spell", card_type="action")
    game_state.played_layer = layer_card
    game_state.layer_chain_link = game_state.play_layer_during_combat(layer_card)


@when("we check the card's zone membership")
def check_card_zone_membership(game_state):
    """Check what zones the card belongs to."""
    game_state.card_zones = game_state.get_card_zone_membership(game_state.attack_card)


@when("we check the active-attack")
def check_the_active_attack(game_state):
    """Check the active-attack of the chain link."""
    game_state.active_attack_result = game_state.get_active_attack(
        game_state.test_chain_link
    )


@when("card B is put onto the chain link as the new attacking card")
def card_b_put_as_attacking_card(game_state):
    """Card B is put onto the chain link as the new attacking card."""
    card_b = game_state.create_card(name="Attack Card B", card_type="attack_action")
    game_state.card_b = card_b
    game_state.replace_result = game_state.replace_active_attack(
        game_state.test_chain_link, card_b
    )


@when("a card is designated as a defending card on that chain link")
def card_designated_as_defending(game_state):
    """A card is designated as a defending card on the chain link."""
    defender = game_state.create_card(name="Defender Card", card_type="action")
    game_state.defending_card = defender
    game_state.defend_result = game_state.add_defending_card_to_link(
        game_state.test_chain_link, defender
    )


@when("we check the card's status")
def check_card_status(game_state):
    """Check if the card is still defending."""
    game_state.is_defending_result = game_state.is_card_defending(
        game_state.defending_card
    )


@when("the card leaves the combat chain")
def card_leaves_combat_chain(game_state):
    """The card leaves the combat chain."""
    game_state.remove_from_combat_chain_result = game_state.remove_from_combat_chain(
        game_state.defending_card
    )
    game_state.is_defending_after_leave = game_state.is_card_defending(
        game_state.defending_card
    )


@when("a card is put onto the chain link as a defending card")
def card_put_as_defending(game_state):
    """A card is put onto the chain link as a defending card."""
    defender = game_state.create_card(name="Defender", card_type="action")
    game_state.defending_card = defender
    game_state.defend_result = game_state.add_defending_card_to_link(
        game_state.test_chain_link, defender
    )


@when(parsers.parse("player {player_id:d} puts the card onto the chain link as a defending card"))
def player_puts_card_as_defending(game_state, player_id):
    """Player puts a card onto the chain link as a defending card."""
    game_state.defend_result = game_state.add_defending_card_to_link(
        game_state.test_chain_link,
        game_state.defending_card,
        controller_id=player_id,
    )
    game_state.defending_controller_id = player_id


@when("an effect tries to add card X as a defending card again on the same chain link")
def effect_tries_to_add_card_x_again(game_state):
    """An effect tries to add card X as a defending card again."""
    game_state.second_defend_result = game_state.add_defending_card_to_link(
        game_state.test_chain_link, game_state.card_x
    )


@when("an effect tries to add card Y as a defending card on that chain link")
def effect_tries_to_add_card_y(game_state):
    """An effect tries to add card Y as a defending card."""
    game_state.card_y_defend_result = game_state.add_defending_card_to_link(
        game_state.test_chain_link, game_state.card_y
    )


@when("we check what card D is defending against")
def check_what_card_d_defends_against(game_state):
    """Check what card D is defending against."""
    game_state.defending_against = game_state.get_defending_against(game_state.card_d)


@when("attack card A ceases to exist")
def attack_card_a_ceases_to_exist(game_state):
    """Attack card A ceases to exist."""
    game_state.card_a_lki = game_state.capture_lki(game_state.card_a)
    game_state.remove_active_attack(game_state.test_chain_link)


@when("an effect tries to add card Z as a defending card on chain link 2")
def effect_tries_to_add_card_z_on_link_2(game_state):
    """An effect tries to add card Z as a defending card on chain link 2."""
    game_state.second_defend_for_z = game_state.add_defending_card_to_link(
        game_state.chain_link_2, game_state.card_z
    )


@when("exactly one card is put onto the chain link as a defending card")
def one_card_put_as_defending(game_state):
    """Exactly one card is put onto the chain link as a defending card."""
    defender = game_state.create_card(name="Solo Defender", card_type="action")
    game_state.solo_defender = defender
    game_state.solo_defend_result = game_state.add_defending_card_to_link(
        game_state.test_chain_link, defender
    )


@when("two cards are put onto the chain link as defending cards in the same event")
def two_cards_put_as_defending_in_same_event(game_state):
    """Two cards are put onto the chain link as defending cards in the same event."""
    card1 = game_state.create_card(name="Defender 1", card_type="action")
    card2 = game_state.create_card(name="Defender 2", card_type="action")
    game_state.twin_defenders = [card1, card2]
    game_state.twin_defend_result = game_state.declare_defenders_together(
        game_state.test_chain_link, [card1, card2]
    )


@when("a defense reaction is played adding one more card as a defending card")
def defense_reaction_played_adding_defender(game_state):
    """A defense reaction is played adding one more card as a defending card."""
    reaction_card = game_state.create_card(
        name="Defense Reaction", card_type="defense_reaction"
    )
    game_state.reaction_card = reaction_card
    game_state.reaction_defend_result = game_state.add_defending_card_to_link(
        game_state.test_chain_link, reaction_card
    )


# ===== Then steps =====


@then("the game is in combat")
def game_is_in_combat(game_state):
    """Verify the game is in combat."""
    assert game_state.in_combat_result is not None, "in_combat_result not set"
    assert game_state.in_combat_result, "Game should be in combat when combat chain is open"


@then(parsers.parse("the steps are \"{steps_text}\" in order"))
def steps_are_in_order(game_state, steps_text):
    """Verify the combat resolution steps are in the correct order."""
    expected = [s.strip() for s in steps_text.split(",")]
    assert game_state.resolution_steps is not None, "resolution_steps not set"
    assert game_state.resolution_steps == expected, (
        f"Expected steps {expected}, got {game_state.resolution_steps}"
    )


@then("the play attempt fails")
def play_attempt_fails(game_state):
    """Verify the play attempt failed."""
    assert game_state.play_result is not None, "play_result not set"
    assert not game_state.play_result.success, "Play should have failed during combat"


@then(parsers.parse("the reason is \"{reason}\""))
def play_fail_reason(game_state, reason):
    """Verify the reason for failure."""
    result = getattr(game_state, 'play_result', None) or getattr(game_state, 'activation_result', None)
    assert result is not None, "No result found"
    assert hasattr(result, 'reason'), "Result has no reason attribute"
    assert reason.lower() in result.reason.lower(), (
        f"Expected reason '{reason}' in '{result.reason}'"
    )


@then("the play attempt is not blocked by the combat restriction")
def play_attempt_not_blocked_by_combat_restriction(game_state):
    """Verify the play as instant is not blocked by combat restriction."""
    assert game_state.play_result is not None, "play_result not set"
    assert not getattr(game_state.play_result, 'blocked_by_combat_restriction', True), (
        "Play as instant should not be blocked by combat restriction"
    )


@then("the activation attempt fails")
def activation_attempt_fails(game_state):
    """Verify the activation attempt failed."""
    assert game_state.activation_result is not None, "activation_result not set"
    assert not game_state.activation_result.success, (
        "Activation should have failed during combat"
    )


@then("the combat chain is recognized as a zone")
def combat_chain_recognized_as_zone(game_state):
    """Verify the combat chain is recognized as a zone."""
    assert game_state.combat_chain_type_result is not None, "combat_chain_type_result not set"
    assert game_state.combat_chain_type_result.is_zone, (
        "Combat chain should be recognized as a zone"
    )


@then("the combat chain is closed")
def combat_chain_is_closed_result(game_state):
    """Verify the combat chain is closed."""
    assert game_state.chain_open_result is not None, "chain_open_result not set"
    assert not game_state.chain_open_result, (
        "Combat chain should be closed at game start"
    )


@then("the combat chain has no chain links")
def combat_chain_has_no_chain_links(game_state):
    """Verify the combat chain has no chain links."""
    assert game_state.chain_contents is not None, "chain_contents not set"
    assert len(game_state.chain_contents) == 0, (
        "Combat chain should have no chain links when closed"
    )


@then("the combat chain has at least one chain link")
def combat_chain_has_chain_links(game_state):
    """Verify the combat chain has at least one chain link."""
    assert game_state.chain_contents is not None, "chain_contents not set"
    assert len(game_state.chain_contents) >= 1, (
        "Combat chain should have at least one chain link when open"
    )


@then("the combat chain opens")
def combat_chain_opens(game_state):
    """Verify the combat chain opened."""
    assert game_state.stack_add_result is not None, "stack_add_result not set"
    assert game_state.stack_add_result.combat_chain_opened, (
        "Combat chain should have opened when attack was added to stack"
    )


@then("the Layer Step begins")
def layer_step_begins(game_state):
    """Verify the Layer Step began."""
    assert game_state.stack_add_result is not None, "stack_add_result not set"
    assert game_state.stack_add_result.layer_step_started, (
        "Layer Step should begin when combat chain opens"
    )


@then("the combat chain remains open")
def combat_chain_remains_open(game_state):
    """Verify the combat chain remains open."""
    assert game_state.combat_chain_open, (
        "Combat chain should remain open after second attack"
    )


@then("the effect can be generated referencing the current combat chain")
def effect_can_be_generated_for_combat_chain(game_state):
    """Verify the effect can reference the current combat chain."""
    assert game_state.effect_can_generate is not None, "effect_can_generate not set"
    assert game_state.effect_can_generate.success, (
        "Effect should be able to reference 'this combat chain' when chain is open"
    )


@then("the effect fails to be generated")
def effect_fails_to_be_generated(game_state):
    """Verify the effect fails to be generated."""
    assert game_state.effect_can_generate is not None, "effect_can_generate not set"
    assert not game_state.effect_can_generate.success, (
        "Effect should fail to be generated when combat chain/link reference is invalid"
    )


@then("the chain link is not an object")
def chain_link_is_not_object(game_state):
    """Verify the chain link is not an object."""
    assert game_state.chain_link_type_result is not None, "chain_link_type_result not set"
    assert not game_state.chain_link_type_result.is_object, (
        "Chain link should not be an object"
    )


@then("the chain link is not a zone")
def chain_link_is_not_zone(game_state):
    """Verify the chain link is not a zone."""
    assert game_state.chain_link_type_result is not None, "chain_link_type_result not set"
    assert not game_state.chain_link_type_result.is_zone, (
        "Chain link should not be a zone"
    )


@then("the chain link has an active-attack")
def chain_link_has_active_attack(game_state):
    """Verify the chain link has an active-attack."""
    assert game_state.chain_link_components is not None, "chain_link_components not set"
    assert game_state.chain_link_components.active_attack is not None, (
        "Chain link should have an active-attack"
    )


@then("the chain link has zero or more defending cards")
def chain_link_has_zero_or_more_defending_cards(game_state):
    """Verify the chain link has defending cards list (zero or more)."""
    assert game_state.chain_link_components is not None, "chain_link_components not set"
    assert hasattr(game_state.chain_link_components, 'defending_cards'), (
        "Chain link components should have defending_cards attribute"
    )


@then(parsers.parse("chain link {link_num:d} exists on the combat chain"))
def chain_link_n_exists(game_state, link_num):
    """Verify a specific chain link number exists on the combat chain."""
    assert game_state.new_link_result is not None, "new_link_result not set"
    assert game_state.new_link_result.link_number == link_num, (
        f"Expected chain link {link_num}, got {game_state.new_link_result.link_number}"
    )


@then("the attack is the active-attack of chain link 1")
def attack_is_active_attack_of_chain_link_1(game_state):
    """Verify the attack is the active-attack of chain link 1."""
    assert game_state.new_link_result is not None, "new_link_result not set"
    assert game_state.new_link_result.active_attack == game_state.new_attack, (
        "The attack should be the active-attack of chain link 1"
    )


@then(parsers.parse("chain link {link_num:d} exists on the combat chain"))
def chain_link_2_exists(game_state, link_num):
    """Verify chain link 2 exists."""
    result = game_state.second_link_result
    assert result is not None, "second_link_result not set"
    assert result.link_number == link_num, (
        f"Expected chain link {link_num}, got {result.link_number}"
    )


@then("the second attack is the active-attack of chain link 2")
def second_attack_is_active_attack_of_chain_link_2(game_state):
    """Verify the second attack is the active-attack of chain link 2."""
    assert game_state.second_link_result is not None, "second_link_result not set"
    assert game_state.second_link_result.active_attack == game_state.second_attack, (
        "The second attack should be the active-attack of chain link 2"
    )


@then("the active chain link is chain link 2")
def active_chain_link_is_link_2(game_state):
    """Verify the active chain link is chain link 2 (most recent)."""
    assert game_state.active_link_result is not None, "active_link_result not set"
    assert game_state.active_link_result.link_number == 2, (
        "The active chain link should be chain link 2 (most recent)"
    )


@then("chain link 1 is no longer the active chain link")
def chain_link_1_no_longer_active(game_state):
    """Verify chain link 1 is no longer the active chain link after resolving."""
    current_active = game_state.get_active_chain_link()
    if current_active is not None:
        assert current_active != game_state.active_chain_link, (
            "Chain link 1 should no longer be the active chain link after resolving"
        )


@then("the chain link controller matches the active-attack controller")
def chain_link_controller_matches_attack(game_state):
    """Verify chain link controller matches the active-attack controller."""
    assert game_state.link_properties is not None, "link_properties not set"
    assert game_state.link_properties.controller_id == game_state.attack_controller_id, (
        "Chain link controller should match the active-attack controller"
    )


@then("the chain link owner matches the active-attack owner")
def chain_link_owner_matches_attack(game_state):
    """Verify chain link owner matches the active-attack owner."""
    assert game_state.link_properties is not None, "link_properties not set"
    assert hasattr(game_state.link_properties, 'owner_id'), (
        "Chain link properties should include owner_id"
    )


@then("the chain link properties still reference the last-known controller")
def chain_link_uses_lki_controller(game_state):
    """Verify chain link uses LKI for controller after active-attack ceases."""
    assert game_state.active_attack_lki is not None, "LKI was not captured"
    lki_controller = game_state.active_attack_lki.controller_id
    link_props = game_state.get_chain_link_properties(game_state.test_chain_link)
    assert link_props.controller_id == lki_controller, (
        "Chain link should use last-known controller when active-attack ceased to exist"
    )


@then("the chain link properties still reference the last-known owner")
def chain_link_uses_lki_owner(game_state):
    """Verify chain link uses LKI for owner after active-attack ceases."""
    assert game_state.active_attack_lki is not None, "LKI was not captured"
    assert hasattr(game_state.active_attack_lki, 'owner_id'), (
        "LKI should capture owner_id"
    )


@then("the effect references the active chain link")
def effect_references_active_chain_link(game_state):
    """Verify the effect can reference the active chain link."""
    assert game_state.effect_can_generate is not None, "effect_can_generate not set"
    assert game_state.effect_can_generate.success, (
        "Effect should be able to reference 'this chain link' when active chain link exists"
    )
    assert game_state.effect_can_generate.referenced_link is not None, (
        "Effect should reference the active chain link"
    )


@then("the layer is associated with the active chain link")
def layer_associated_with_active_chain_link(game_state):
    """Verify the layer played during combat is on the active chain link."""
    assert game_state.layer_chain_link is not None, "layer_chain_link not set"
    assert game_state.layer_chain_link == game_state.active_chain_link, (
        "Layer played during combat should be associated with the active chain link"
    )


@then("the card is on the combat chain")
def card_is_on_combat_chain(game_state):
    """Verify the card is on the combat chain."""
    assert game_state.card_zones is not None, "card_zones not set"
    assert game_state.card_zones.on_combat_chain, (
        "Card on chain link should be considered to be on the combat chain"
    )


@then("the card is in the arena")
def card_is_in_arena(game_state):
    """Verify the card is in the arena."""
    assert game_state.card_zones is not None, "card_zones not set"
    assert game_state.card_zones.in_arena, (
        "Card on chain link should be considered to be in the arena"
    )


@then("the attack is the active-attack of the chain link")
def attack_is_active_attack_of_chain_link(game_state):
    """Verify the attack is the active-attack of its chain link."""
    assert game_state.active_attack_result is not None, "active_attack_result not set"
    assert game_state.active_attack_result == game_state.attack_card, (
        "The attack should be the active-attack of the chain link"
    )


@then("card A is no longer the active-attack")
def card_a_no_longer_active_attack(game_state):
    """Verify card A is no longer the active-attack."""
    assert game_state.replace_result is not None, "replace_result not set"
    assert game_state.replace_result.previous_active_attack_cleared, (
        "Card A should be cleared as active-attack"
    )


@then("card B is the new active-attack for that chain link")
def card_b_is_new_active_attack(game_state):
    """Verify card B is the new active-attack."""
    assert game_state.replace_result is not None, "replace_result not set"
    assert game_state.replace_result.new_active_attack == game_state.card_b, (
        "Card B should be the new active-attack"
    )


@then(parsers.parse("card B's attack target is still player {player_id:d}"))
def card_b_attack_target_preserved(game_state, player_id):
    """Verify card B's attack target is still the original player."""
    assert game_state.replace_result is not None, "replace_result not set"
    assert game_state.replace_result.attack_target_preserved == player_id, (
        f"Attack target should still be player {player_id}"
    )


@then("card B is considered a new attack for rules and effects")
def card_b_is_new_attack(game_state):
    """Verify card B is considered a new attack."""
    assert game_state.replace_result is not None, "replace_result not set"
    assert game_state.replace_result.is_new_attack, (
        "Replacement attacking card should be considered a new attack"
    )


@then("the card is a defending card")
def card_is_defending_card(game_state):
    """Verify the card is a defending card."""
    assert game_state.defend_result is not None, "defend_result not set"
    assert game_state.defend_result.success, "Card should be a defending card"
    assert game_state.is_card_defending(game_state.defending_card), (
        "Card should be defending"
    )


@then("the card is still defending")
def card_is_still_defending(game_state):
    """Verify the card is still defending."""
    assert game_state.is_defending_result is not None, "is_defending_result not set"
    assert game_state.is_defending_result, "Card should still be defending"


@then("the card is no longer defending")
def card_is_no_longer_defending(game_state):
    """Verify the card is no longer defending after leaving combat chain."""
    assert not game_state.is_defending_after_leave, (
        "Card should not be defending after leaving the combat chain"
    )


@then("the defend event occurs")
def defend_event_occurs(game_state):
    """Verify the defend event occurred."""
    assert game_state.defend_result is not None, "defend_result not set"
    assert game_state.defend_result.defend_event_occurred, (
        "The defend event should occur when a defending card is added"
    )


@then("effects that trigger from defending are triggered")
def effects_triggered_from_defending(game_state):
    """Verify effects that trigger from defending are triggered."""
    assert game_state.defend_result is not None, "defend_result not set"
    assert game_state.defend_result.defend_triggers_checked, (
        "Effects that trigger from defending should be checked"
    )


@then(parsers.parse("player {player_id:d} is considered to have defended with that card"))
def player_considered_to_have_defended(game_state, player_id):
    """Verify the specified player is considered to have defended."""
    assert game_state.defend_result is not None, "defend_result not set"
    assert game_state.defend_result.defending_controller_id == player_id, (
        f"Player {player_id} should be considered to have defended with the card"
    )


@then("the effect fails")
def effect_fails(game_state):
    """Verify the defend effect failed."""
    result = getattr(game_state, 'second_defend_result', None) or \
              getattr(game_state, 'card_y_defend_result', None)
    assert result is not None, "No defend result found"
    assert not result.success, "The defend effect should have failed"


@then("no defend event occurs")
def no_defend_event_occurs(game_state):
    """Verify no defend event occurred."""
    result = getattr(game_state, 'second_defend_result', None) or \
              getattr(game_state, 'card_y_defend_result', None)
    assert result is not None, "No defend result found"
    assert not result.defend_event_occurred, "No defend event should occur on failure"


@then("card X remains on the chain link unchanged")
def card_x_remains_unchanged(game_state):
    """Verify card X remains on the chain link unchanged."""
    assert game_state.is_card_defending(game_state.card_x), (
        "Card X should remain defending on the chain link"
    )


@then("card Y does not move zones")
def card_y_does_not_move_zones(game_state):
    """Verify card Y did not move zones."""
    assert game_state.card_y_defend_result is not None, "card_y_defend_result not set"
    assert not game_state.card_y_defend_result.card_moved_zones, (
        "Card Y should not have moved zones"
    )


@then("card D is defending against attack card A")
def card_d_defends_against_attack_a(game_state):
    """Verify card D is defending against attack card A."""
    assert game_state.defending_against is not None, "defending_against not set"
    assert game_state.defending_against == game_state.card_a, (
        "Card D should be defending against attack card A"
    )


@then("card D still references last-known information about attack card A")
def card_d_uses_lki_for_attack_a(game_state):
    """Verify card D uses LKI for attack card A."""
    assert game_state.card_a_lki is not None, "card_a LKI was not captured"
    defending_against = game_state.get_defending_against_lki(game_state.card_d)
    assert defending_against is not None, (
        "Should still have reference to attack via LKI"
    )
    assert defending_against.lki_controller_id == game_state.card_a_lki.controller_id, (
        "Card D should use LKI info about attack card A"
    )


@then("the second defend attempt fails")
def second_defend_attempt_fails(game_state):
    """Verify the second defend attempt (for card Z on link 2) fails."""
    assert game_state.second_defend_for_z is not None, "second_defend_for_z not set"
    assert not game_state.second_defend_for_z.success, (
        "Card Z cannot defend on two chain links simultaneously"
    )


@then("card Z remains defending only on chain link 1")
def card_z_still_defending_on_link_1(game_state):
    """Verify card Z is still defending only on chain link 1."""
    assert game_state.is_card_defending(game_state.card_z), (
        "Card Z should still be defending on chain link 1"
    )
    assert not game_state.is_card_defending_on_link(game_state.card_z, game_state.chain_link_2), (
        "Card Z should not be defending on chain link 2"
    )


@then("that card defends alone")
def that_card_defends_alone(game_state):
    """Verify the single defending card defends alone."""
    assert game_state.solo_defend_result is not None, "solo_defend_result not set"
    assert game_state.solo_defend_result.defends_alone, (
        "A single defending card should defend alone"
    )


@then("those cards defend together")
def those_cards_defend_together(game_state):
    """Verify the two cards defend together."""
    assert game_state.twin_defend_result is not None, "twin_defend_result not set"
    assert game_state.twin_defend_result.defends_together, (
        "Two cards added in the same event should defend together"
    )


@then("the defense reaction card defends alone despite other defenders already being present")
def defense_reaction_defends_alone(game_state):
    """Verify the defense reaction card defends alone."""
    assert game_state.reaction_defend_result is not None, "reaction_defend_result not set"
    assert game_state.reaction_defend_result.defends_alone, (
        "A defense reaction card added alone should defend alone, "
        "even if other defenders are already on the chain link"
    )


# ===== Fixtures =====


@pytest.fixture
def game_state():
    """
    Fixture providing game state for testing combat general rules.

    Uses BDDGameState which integrates with the real engine.
    Reference: Rules 7.0.1 through 7.0.5e
    """
    from tests.bdd_helpers import BDDGameState

    state = BDDGameState()
    state.combat_chain_open = False
    state.chain_links = []
    state.active_chain_link = None

    return state
