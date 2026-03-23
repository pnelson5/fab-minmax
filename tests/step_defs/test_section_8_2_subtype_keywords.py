"""
Step definitions for Section 8.2: Subtype Keywords
Reference: Flesh and Blood Comprehensive Rules Section 8.2

This module implements behavioral tests for each functional subtype keyword,
covering (1H), (2H), Attack, Aura, Item, Arrow, Trap, Ally, Landmark,
Off-Hand, Affliction, Ash, Invocation, Construct, Quiver, and Figment.

Engine Features Needed for Section 8.2:
- [ ] Subtype.ONE_HANDER / "1H" subtype identification (Rule 8.2.1a)
- [ ] Subtype.TWO_HANDER / "2H" subtype identification (Rule 8.2.2a)
- [ ] WeaponZone.is_empty() — check if a weapon zone is unoccupied (Rule 8.2.1b, 8.2.2b)
- [ ] WeaponZone.is_occupied_by_two_hander() — check two-hander occupancy (Rule 8.2.2c)
- [ ] Equipment.can_equip(player) — validates weapon zone availability (Rule 8.2.1b, 8.2.2b)
- [ ] TwoHander.occupied_zones() — returns which zone it occupies (Rule 8.2.2c)
- [ ] Subtype.ATTACK subtype on attack cards (Rule 8.2.3a)
- [ ] CardInstance.is_attack() — True when on stack or on combat chain as attacking card (Rule 8.2.3a)
- [ ] CombatChain.open() — opens combat chain when attack is played (Rule 8.2.3b)
- [ ] Subtype.AURA — aura subtype (Rule 8.2.4)
- [ ] Aura.enters_arena_on_resolution() — True for auras (Rule 8.2.4a)
- [ ] Aura.becomes_permanent_in_arena() — True unless added as defending card (Rule 8.2.4b)
- [ ] Subtype.ITEM — item subtype (Rule 8.2.5)
- [ ] Item.enters_arena_on_resolution() — True for items (Rule 8.2.5a)
- [ ] Item.becomes_permanent_in_arena() — True unless added as defending card (Rule 8.2.5b)
- [ ] Subtype.ARROW — arrow subtype (Rule 8.2.6)
- [ ] Arrow.can_play(player) — validates arsenal source AND bow control (Rule 8.2.6a)
- [ ] Player.controls_bow() — checks for bow weapon (Rule 8.2.6a)
- [ ] Subtype.TRAP — trap subtype is non-functional as of 2023 (Rule 8.2.7)
- [ ] Subtype.ALLY — ally subtype (Rule 8.2.8)
- [ ] Ally.is_considered_dead_on_ceasing_to_exist() — True for allies (Rule 8.2.8a)
- [ ] Ally.life_resets_to_base_in_end_phase() — True for allies (Rule 8.2.8b)
- [ ] GameState.attacking_hero_for_chain_link() — returns hero, excludes ally's controller (Rule 8.2.8c)
- [ ] GameState.defending_hero_for_chain_link() — returns hero, excludes ally's controller (Rule 8.2.8d)
- [ ] GameState.can_declare_defenders(player, chain_link) — False when ally is attack target (Rule 8.2.8d)
- [ ] GameState.can_play_defense_reaction(player, chain_link) — False when ally is attack target (Rule 8.2.8d)
- [ ] GameState.player_dealt_damage(player) — excludes ally-dealt damage (Rule 8.2.8e)
- [ ] GameState.player_was_dealt_damage(player) — excludes ally-received damage (Rule 8.2.8f)
- [ ] Subtype.LANDMARK — landmark subtype (Rule 8.2.9)
- [ ] Landmark.enters_arena_on_resolution() — True for landmarks (Rule 8.2.9a)
- [ ] Landmark.clears_other_landmarks_on_enter() — True unless added as defending card (Rule 8.2.9b)
- [ ] Subtype.OFF_HAND — off-hand subtype (Rule 8.2.10)
- [ ] OffHand.can_equip(player) — validates weapon zone AND uniqueness (Rule 8.2.10a, 8.2.10b)
- [ ] Player.has_off_hand_equipped() — checks uniqueness constraint (Rule 8.2.10b)
- [ ] Subtype.AFFLICTION — affliction subtype (Rule 8.2.11)
- [ ] Affliction.enters_arena_on_resolution() — True for afflictions (Rule 8.2.11a)
- [ ] Affliction.enters_under_opponent_control() — controller declares target opponent (Rule 8.2.11c)
- [ ] Affliction.cleared_if_cannot_enter_under_opponent() — True (Rule 8.2.11c)
- [ ] Subtype.ASH — ash subtype (Rule 8.2.12)
- [ ] Ash.enters_arena_on_resolution() — True (Rule 8.2.12a)
- [ ] Subtype.INVOCATION — invocation subtype (Rule 8.2.13)
- [ ] Invocation.enters_with_back_face_active() — True (Rule 8.2.13a)
- [ ] Subtype.CONSTRUCT — construct subtype (Rule 8.2.14)
- [ ] Construct.enters_with_back_face_active() — True (Rule 8.2.14a)
- [ ] Subtype.QUIVER — quiver subtype (Rule 8.2.15)
- [ ] Quiver.can_equip(player) — validates weapon zone or two-hander bow sharing (Rule 8.2.15a)
- [ ] Quiver.can_share_zone_with_two_hander_bow() — True (Rule 8.2.15a)
- [ ] Player.has_quiver_equipped() — checks uniqueness constraint (Rule 8.2.15b)
- [ ] Subtype.FIGMENT — figment subtype (Rule 8.2.16)
- [ ] Figment.enters_arena_on_resolution() — True (Rule 8.2.16a)

Current status: Tests written, Engine pending
"""

import pytest
from pytest_bdd import scenario, given, when, then, parsers
from typing import Optional, Any


# ===== 8.2.1 (1H) One-Hander Scenarios =====

@scenario(
    "../features/section_8_2_subtype_keywords.feature",
    "1H object is considered a one-hander",
)
def test_1h_is_one_hander():
    """Rule 8.2.1a: A (1H) object is considered a one-hander."""
    pass


@scenario(
    "../features/section_8_2_subtype_keywords.feature",
    "One-hander requires an empty weapon zone to equip",
)
def test_one_hander_requires_empty_weapon_zone():
    """Rule 8.2.1b: A one-hander must be equipped to an empty weapon zone."""
    pass


@scenario(
    "../features/section_8_2_subtype_keywords.feature",
    "One-hander cannot be equipped without an empty weapon zone",
)
def test_one_hander_blocked_without_empty_zone():
    """Rule 8.2.1b: A one-hander cannot be equipped if no empty weapon zone."""
    pass


# ===== 8.2.2 (2H) Two-Hander Scenarios =====

@scenario(
    "../features/section_8_2_subtype_keywords.feature",
    "2H object is considered a two-hander",
)
def test_2h_is_two_hander():
    """Rule 8.2.2a: A (2H) object is considered a two-hander."""
    pass


@scenario(
    "../features/section_8_2_subtype_keywords.feature",
    "Two-hander requires two empty weapon zones to equip",
)
def test_two_hander_requires_two_empty_zones():
    """Rule 8.2.2b: A two-hander must be equipped to two empty weapon zones."""
    pass


@scenario(
    "../features/section_8_2_subtype_keywords.feature",
    "Two-hander cannot be equipped with only one empty weapon zone",
)
def test_two_hander_blocked_with_one_zone():
    """Rule 8.2.2b: A two-hander cannot equip if only one weapon zone is empty."""
    pass


@scenario(
    "../features/section_8_2_subtype_keywords.feature",
    "Two-hander occupies either weapon zone but not both",
)
def test_two_hander_occupies_one_zone():
    """Rule 8.2.2c: A two-hander occupies either zone, but not both."""
    pass


# ===== 8.2.3 Attack (subtype) Scenarios =====

@scenario(
    "../features/section_8_2_subtype_keywords.feature",
    "Attack card is considered an attack when on the stack",
)
def test_attack_subtype_is_attack_on_stack():
    """Rule 8.2.3a: An attack card is considered an attack when on the stack."""
    pass


@scenario(
    "../features/section_8_2_subtype_keywords.feature",
    "Attack card is considered an attack when on the combat chain",
)
def test_attack_subtype_is_attack_on_combat_chain():
    """Rule 8.2.3a: An attack card is considered an attack when on the combat chain."""
    pass


@scenario(
    "../features/section_8_2_subtype_keywords.feature",
    "Playing an attack card opens the combat chain",
)
def test_attack_card_opens_combat_chain():
    """Rule 8.2.3b: Playing an attack card opens the combat chain and starts layer step."""
    pass


# ===== 8.2.4 Aura Scenarios =====

@scenario(
    "../features/section_8_2_subtype_keywords.feature",
    "Aura enters the arena when it resolves as a layer",
)
def test_aura_enters_arena_on_resolution():
    """Rule 8.2.4a: When an aura resolves as a layer, it enters the arena."""
    pass


@scenario(
    "../features/section_8_2_subtype_keywords.feature",
    "Aura becomes a permanent when it enters the arena",
)
def test_aura_becomes_permanent():
    """Rule 8.2.4b: An aura entering the arena becomes a permanent."""
    pass


@scenario(
    "../features/section_8_2_subtype_keywords.feature",
    "Aura added as defending card does not become a permanent",
)
def test_aura_defending_card_not_permanent():
    """Rule 8.2.4b: An aura added as defending card does not become a permanent."""
    pass


# ===== 8.2.5 Item Scenarios =====

@scenario(
    "../features/section_8_2_subtype_keywords.feature",
    "Item enters the arena when it resolves as a layer",
)
def test_item_enters_arena_on_resolution():
    """Rule 8.2.5a: When an item resolves as a layer, it enters the arena."""
    pass


@scenario(
    "../features/section_8_2_subtype_keywords.feature",
    "Item becomes a permanent when it enters the arena",
)
def test_item_becomes_permanent():
    """Rule 8.2.5b: An item entering the arena becomes a permanent."""
    pass


@scenario(
    "../features/section_8_2_subtype_keywords.feature",
    "Item added as defending card does not become a permanent",
)
def test_item_defending_card_not_permanent():
    """Rule 8.2.5b: An item added as defending card does not become a permanent."""
    pass


# ===== 8.2.6 Arrow Scenarios =====

@scenario(
    "../features/section_8_2_subtype_keywords.feature",
    "Arrow can be played from arsenal when player controls a bow",
)
def test_arrow_playable_from_arsenal_with_bow():
    """Rule 8.2.6a: Arrow can be played from arsenal when player controls a bow."""
    pass


@scenario(
    "../features/section_8_2_subtype_keywords.feature",
    "Arrow cannot be played from hand even with a bow",
)
def test_arrow_not_playable_from_hand():
    """Rule 8.2.6a: Arrow can only be played from arsenal, not from hand."""
    pass


@scenario(
    "../features/section_8_2_subtype_keywords.feature",
    "Arrow cannot be played without controlling a bow",
)
def test_arrow_not_playable_without_bow():
    """Rule 8.2.6a: Arrow cannot be played without controlling a bow."""
    pass


# ===== 8.2.7 Trap Scenarios =====

@scenario(
    "../features/section_8_2_subtype_keywords.feature",
    "Trap is no longer a functional subtype keyword",
)
def test_trap_not_functional():
    """Rule 8.2.7: Trap is no longer a functional subtype keyword as of 2023."""
    pass


# ===== 8.2.8 Ally Scenarios =====

@scenario(
    "../features/section_8_2_subtype_keywords.feature",
    "Ally permanent ceasing to exist is considered to have died",
)
def test_ally_ceasing_to_exist_is_death():
    """Rule 8.2.8a: If an ally permanent ceases to exist, it is considered to have died."""
    pass


@scenario(
    "../features/section_8_2_subtype_keywords.feature",
    "Ally life total resets to base life during End Phase",
)
def test_ally_life_resets_end_phase():
    """Rule 8.2.8b: During End Phase, ally's life total resets to base life."""
    pass


@scenario(
    "../features/section_8_2_subtype_keywords.feature",
    "Ally attacking does not make controlling player an attacking hero",
)
def test_ally_attacking_not_attacking_hero():
    """Rule 8.2.8c: Ally attacking does not make controlling player/hero the attacking hero."""
    pass


@scenario(
    "../features/section_8_2_subtype_keywords.feature",
    "Ally as attack target does not make controlling player a defending hero",
)
def test_ally_attacked_not_defending_hero():
    """Rule 8.2.8d: Ally as attack target does not make controlling player/hero the defending hero."""
    pass


@scenario(
    "../features/section_8_2_subtype_keywords.feature",
    "Controlling player cannot declare defenders when ally is attack target",
)
def test_no_defenders_when_ally_attacked():
    """Rule 8.2.8d: Controlling player cannot declare defending cards when ally is attack target."""
    pass


@scenario(
    "../features/section_8_2_subtype_keywords.feature",
    "Controlling player cannot play defense reactions when ally is attack target",
)
def test_no_defense_reaction_when_ally_attacked():
    """Rule 8.2.8d: Controlling player cannot play defense reactions when ally is attack target."""
    pass


@scenario(
    "../features/section_8_2_subtype_keywords.feature",
    "Ally dealing damage does not count as controlling player dealing damage",
)
def test_ally_damage_not_attributed_to_player():
    """Rule 8.2.8e: Ally dealing damage does not count as controlling player dealing damage."""
    pass


@scenario(
    "../features/section_8_2_subtype_keywords.feature",
    "Ally being dealt damage does not count as controlling player being dealt damage",
)
def test_ally_receiving_damage_not_attributed_to_player():
    """Rule 8.2.8f: Ally being dealt damage does not count as controlling player being dealt damage."""
    pass


# ===== 8.2.9 Landmark Scenarios =====

@scenario(
    "../features/section_8_2_subtype_keywords.feature",
    "Landmark enters the arena when it resolves as a layer",
)
def test_landmark_enters_arena_on_resolution():
    """Rule 8.2.9a: When a landmark resolves as a layer, it enters the arena."""
    pass


@scenario(
    "../features/section_8_2_subtype_keywords.feature",
    "Landmark becomes a permanent and clears other landmarks",
)
def test_landmark_clears_other_landmarks():
    """Rule 8.2.9b: Landmark entering arena becomes permanent and clears other landmarks."""
    pass


@scenario(
    "../features/section_8_2_subtype_keywords.feature",
    "Landmark added as defending card does not clear other landmarks",
)
def test_landmark_defending_card_does_not_clear():
    """Rule 8.2.9b: Landmark added as defending card does not clear other landmarks."""
    pass


# ===== 8.2.10 Off-Hand Scenarios =====

@scenario(
    "../features/section_8_2_subtype_keywords.feature",
    "Off-hand requires an empty weapon zone to equip",
)
def test_off_hand_requires_empty_zone():
    """Rule 8.2.10a: Off-hand must be equipped to an empty weapon zone."""
    pass


@scenario(
    "../features/section_8_2_subtype_keywords.feature",
    "Off-hand cannot be equipped without an empty weapon zone",
)
def test_off_hand_blocked_without_empty_zone():
    """Rule 8.2.10a: Off-hand cannot be equipped if no empty weapon zone."""
    pass


@scenario(
    "../features/section_8_2_subtype_keywords.feature",
    "Player cannot equip more than one off-hand",
)
def test_off_hand_unique_restriction():
    """Rule 8.2.10b: A player cannot equip more than one off-hand."""
    pass


# ===== 8.2.11 Affliction Scenarios =====

@scenario(
    "../features/section_8_2_subtype_keywords.feature",
    "Affliction enters the arena when it resolves as a layer",
)
def test_affliction_enters_arena_on_resolution():
    """Rule 8.2.11a: When an affliction resolves as a layer, it enters the arena."""
    pass


@scenario(
    "../features/section_8_2_subtype_keywords.feature",
    "Affliction becomes a permanent under an opponent's control",
)
def test_affliction_enters_under_opponent_control():
    """Rule 8.2.11c: Affliction enters arena under a declared opponent's control."""
    pass


@scenario(
    "../features/section_8_2_subtype_keywords.feature",
    "Affliction owner declares opponent when affliction has no controller",
)
def test_affliction_owner_declares_opponent():
    """Rule 8.2.11c: When affliction has no controller, its owner declares the opponent."""
    pass


@scenario(
    "../features/section_8_2_subtype_keywords.feature",
    "Affliction is cleared if it cannot enter arena under opponent's control",
)
def test_affliction_cleared_if_cannot_enter():
    """Rule 8.2.11c: Affliction is cleared if it cannot enter under any opponent's control."""
    pass


@scenario(
    "../features/section_8_2_subtype_keywords.feature",
    "Affliction added as defending card does not become a permanent",
)
def test_affliction_defending_card_not_permanent():
    """Rule 8.2.11b: Affliction added as defending card does not become a permanent."""
    pass


# ===== 8.2.12 Ash Scenarios =====

@scenario(
    "../features/section_8_2_subtype_keywords.feature",
    "Ash enters the arena when it resolves as a layer",
)
def test_ash_enters_arena_on_resolution():
    """Rule 8.2.12a: When an ash resolves as a layer, it enters the arena."""
    pass


@scenario(
    "../features/section_8_2_subtype_keywords.feature",
    "Ash becomes a permanent when it enters the arena",
)
def test_ash_becomes_permanent():
    """Rule 8.2.12b: An ash entering the arena becomes a permanent."""
    pass


@scenario(
    "../features/section_8_2_subtype_keywords.feature",
    "Ash added as defending card does not become a permanent",
)
def test_ash_defending_card_not_permanent():
    """Rule 8.2.12b: An ash added as defending card does not become a permanent."""
    pass


# ===== 8.2.13 Invocation Scenarios =====

@scenario(
    "../features/section_8_2_subtype_keywords.feature",
    "Invocation enters arena with back-face active when it resolves",
)
def test_invocation_enters_with_back_face():
    """Rule 8.2.13a: Invocation enters arena with back-face active and becomes a permanent."""
    pass


# ===== 8.2.14 Construct Scenarios =====

@scenario(
    "../features/section_8_2_subtype_keywords.feature",
    "Construct enters arena with back-face active when it resolves",
)
def test_construct_enters_with_back_face():
    """Rule 8.2.14a: Construct enters arena with back-face active and becomes a permanent."""
    pass


# ===== 8.2.15 Quiver Scenarios =====

@scenario(
    "../features/section_8_2_subtype_keywords.feature",
    "Quiver requires an empty weapon zone to equip",
)
def test_quiver_requires_empty_zone():
    """Rule 8.2.15a: Quiver must be equipped to an empty weapon zone."""
    pass


@scenario(
    "../features/section_8_2_subtype_keywords.feature",
    "Quiver can share weapon zone occupied by a two-hander bow",
)
def test_quiver_can_share_zone_with_two_hander_bow():
    """Rule 8.2.15a: Quiver can share a weapon zone with a two-hander bow that doesn't occupy it."""
    pass


@scenario(
    "../features/section_8_2_subtype_keywords.feature",
    "Quiver cannot be equipped without an empty or bow-sharing weapon zone",
)
def test_quiver_blocked_without_valid_zone():
    """Rule 8.2.15a: Quiver cannot be equipped if no empty or shareable zone."""
    pass


@scenario(
    "../features/section_8_2_subtype_keywords.feature",
    "Player cannot equip more than one quiver",
)
def test_quiver_unique_restriction():
    """Rule 8.2.15b: A player cannot equip more than one quiver."""
    pass


# ===== 8.2.16 Figment Scenarios =====

@scenario(
    "../features/section_8_2_subtype_keywords.feature",
    "Figment enters the arena when it resolves as a layer",
)
def test_figment_enters_arena_on_resolution():
    """Rule 8.2.16a: When a figment resolves as a layer, it enters the arena."""
    pass


@scenario(
    "../features/section_8_2_subtype_keywords.feature",
    "Figment becomes a permanent when it enters the arena",
)
def test_figment_becomes_permanent():
    """Rule 8.2.16b: A figment entering the arena becomes a permanent."""
    pass


@scenario(
    "../features/section_8_2_subtype_keywords.feature",
    "Figment added as defending card does not become a permanent",
)
def test_figment_defending_card_not_permanent():
    """Rule 8.2.16b: A figment added as defending card does not become a permanent."""
    pass


# ===== Step Definitions =====

# ---- Card/object setup ----

@given(parsers.parse('a card with the subtype "{subtype}"'))
def card_with_subtype(game_state, subtype):
    """Create a card with the given subtype."""
    from fab_engine.cards.model import Subtype
    card = game_state.create_card(name=f"Test {subtype} Card")
    subtype_map = {
        "(1H)": "ONE_HANDER",
        "(2H)": "TWO_HANDER",
        "Attack": "ATTACK",
        "Aura": "AURA",
        "Item": "ITEM",
        "Arrow": "ARROW",
        "Trap": "TRAP",
        "Ally": "ALLY",
        "Landmark": "LANDMARK",
        "Off-Hand": "OFF_HAND",
        "Affliction": "AFFLICTION",
        "Ash": "ASH",
        "Invocation": "INVOCATION",
        "Construct": "CONSTRUCT",
        "Quiver": "QUIVER",
        "Figment": "FIGMENT",
    }
    game_state.test_card = card
    game_state.test_subtype = subtype
    game_state.test_subtype_key = subtype_map.get(subtype, subtype.upper())


@given("the player has an empty weapon zone")
def player_has_empty_weapon_zone(game_state):
    """Rule 8.2.1b / 8.2.10a / 8.2.15a: Player has at least one empty weapon zone."""
    game_state.player_weapon_zones = {"left": None, "right": None}
    game_state.empty_weapon_zones = 2


@given("all of the player's weapon zones are occupied")
def all_weapon_zones_occupied(game_state):
    """Rule 8.2.1b: All player weapon zones are occupied."""
    game_state.player_weapon_zones = {"left": "weapon_a", "right": "weapon_b"}
    game_state.empty_weapon_zones = 0


@given("the player has two empty weapon zones")
def player_has_two_empty_weapon_zones(game_state):
    """Rule 8.2.2b: Player has two empty weapon zones."""
    game_state.player_weapon_zones = {"left": None, "right": None}
    game_state.empty_weapon_zones = 2


@given("the player has only one empty weapon zone")
def player_has_one_empty_weapon_zone(game_state):
    """Rule 8.2.2b: Player has only one empty weapon zone."""
    game_state.player_weapon_zones = {"left": "some_weapon", "right": None}
    game_state.empty_weapon_zones = 1


@given("the two-hander is equipped to two weapon zones")
def two_hander_equipped_to_two_zones(game_state):
    """Rule 8.2.2c: A two-hander is equipped to two weapon zones."""
    game_state.two_hander_equipped = True
    game_state.two_hander_zone_left = True
    game_state.two_hander_zone_right = True
    game_state.two_hander_occupies = "left"  # Only occupies one


@given("the card is on the stack")
def card_on_stack(game_state):
    """Rule 8.2.3a: Place card on the stack."""
    game_state.card_location = "stack"
    game_state.play_card_to_stack(game_state.test_card)


@given("the card is on the combat chain as an attacking card")
def card_on_combat_chain_attacking(game_state):
    """Rule 8.2.3a: Card is on the combat chain as an attacking card."""
    game_state.card_location = "combat_chain_attacking"


@given("the combat chain is closed")
def combat_chain_is_closed(game_state):
    """Rule 8.2.3b: The combat chain is currently closed."""
    game_state.combat_chain_open = False


@given(parsers.parse("the {subtype_name} is resolving as a layer on the stack"))
def subtype_resolving_as_layer(game_state, subtype_name):
    """Rule 8.2.4a/5a/9a/11a/12a/16a: The card is resolving as a layer."""
    game_state.resolving_as_layer = True
    game_state.card_location = "resolving_from_stack"


@given(parsers.parse("the {subtype_name} has entered the arena"))
def subtype_has_entered_arena(game_state, subtype_name):
    """Rule 8.2.4b/5b/12b/16b: The card has entered the arena."""
    game_state.card_location = "arena"
    game_state.card_is_permanent = True


@given(parsers.parse("the {subtype_name} is added as a defending card to a chain link"))
def subtype_added_as_defending_card(game_state, subtype_name):
    """Rule 8.2.4b/5b/9b/11b/12b/16b: The card is added as a defending card."""
    game_state.card_location = "defending_card"
    game_state.card_is_defending = True


@given("the arrow is in the player's arsenal")
def arrow_in_arsenal(game_state):
    """Rule 8.2.6a: The arrow is in the player's arsenal."""
    game_state.arrow_location = "arsenal"


@given("the arrow is in the player's hand")
def arrow_in_hand(game_state):
    """Rule 8.2.6a: The arrow is in the player's hand."""
    game_state.arrow_location = "hand"


@given('the player controls a weapon with the subtype "Bow"')
def player_controls_bow(game_state):
    """Rule 8.2.6a: Player controls a bow weapon."""
    game_state.player_controls_bow = True


@given("the player does not control a bow")
def player_no_bow(game_state):
    """Rule 8.2.6a: Player does not control a bow."""
    game_state.player_controls_bow = False


@given("an ally permanent in the arena")
def ally_permanent_in_arena(game_state):
    """Rule 8.2.8a: An ally permanent is in the arena."""
    from fab_engine.cards.model import Subtype
    ally_card = game_state.create_card(name="Test Ally")
    game_state.ally_card = ally_card
    game_state.play_card_to_arena(ally_card)
    game_state.ally_in_arena = True


@given("an ally permanent with a modified life total")
def ally_with_modified_life(game_state):
    """Rule 8.2.8b: An ally permanent with a non-base life total."""
    from fab_engine.cards.model import Subtype
    ally_card = game_state.create_card(name="Test Ally")
    game_state.ally_card = ally_card
    game_state.ally_base_life = 4
    game_state.ally_current_life = 2  # Damaged
    game_state.ally_in_arena = True


@given("an ally permanent that is attacking")
def ally_is_attacking(game_state):
    """Rule 8.2.8c: An ally permanent is the attacking card."""
    from fab_engine.cards.model import Subtype
    ally_card = game_state.create_card(name="Test Ally Attacker")
    game_state.ally_card = ally_card
    game_state.ally_is_attacking = True


@given("an ally permanent that is the target of an attack")
def ally_is_attack_target(game_state):
    """Rule 8.2.8d: An ally permanent is the target of an attack."""
    from fab_engine.cards.model import Subtype
    ally_card = game_state.create_card(name="Test Ally Defender")
    game_state.ally_card = ally_card
    game_state.ally_is_attack_target = True


@given("the game is in the Defend Step of combat")
def game_in_defend_step(game_state):
    """Rule 8.2.8d: The game is currently in the Defend Step of combat."""
    game_state.combat_step = "defend_step"


@given("the game is in the Reaction Step of combat")
def game_in_reaction_step(game_state):
    """Rule 8.2.8d: The game is currently in the Reaction Step of combat."""
    game_state.combat_step = "reaction_step"


@given("an ally permanent that deals damage to an opposing hero")
def ally_deals_damage(game_state):
    """Rule 8.2.8e: An ally permanent deals damage."""
    ally_card = game_state.create_card(name="Test Ally Damage Dealer")
    game_state.ally_card = ally_card
    game_state.ally_dealt_damage = True
    game_state.ally_damage_amount = 3


@given("an ally permanent that is dealt damage")
def ally_receives_damage(game_state):
    """Rule 8.2.8f: An ally permanent is dealt damage."""
    ally_card = game_state.create_card(name="Test Ally Damage Receiver")
    game_state.ally_card = ally_card
    game_state.ally_received_damage = True
    game_state.ally_received_damage_amount = 2


@given("there is already a landmark permanent in the arena")
def existing_landmark_in_arena(game_state):
    """Rule 8.2.9b: There is already a landmark permanent in the arena."""
    existing = game_state.create_card(name="Existing Landmark")
    game_state.existing_landmark = existing
    game_state.play_card_to_arena(existing)
    game_state.existing_landmark_in_arena = True


@given("the player already has an off-hand equipped")
def player_has_off_hand(game_state):
    """Rule 8.2.10b: Player already has an off-hand equipped."""
    game_state.player_has_off_hand = True
    game_state.empty_weapon_zones = 1  # Has a zone free but already has one off-hand


@given("the player already has a quiver equipped")
def player_has_quiver(game_state):
    """Rule 8.2.15b: Player already has a quiver equipped."""
    game_state.player_has_quiver = True
    game_state.empty_weapon_zones = 1  # Has a zone free but already has one quiver


@given("the affliction is controlled by a player with an opponent")
def affliction_has_controller_with_opponent(game_state):
    """Rule 8.2.11c: The affliction has a controller who has an opponent."""
    game_state.affliction_has_controller = True
    game_state.affliction_controller_has_opponent = True


@given("the affliction has no controller before entering the arena")
def affliction_no_controller(game_state):
    """Rule 8.2.11c: The affliction has no controller."""
    game_state.affliction_has_controller = False


@given("the affliction cannot enter the arena under any opponent's control")
def affliction_cannot_enter(game_state):
    """Rule 8.2.11c: The affliction cannot enter the arena under any opponent's control."""
    game_state.affliction_can_enter_under_opponent = False


@given("the player has a two-hander bow equipped that does not occupy one of the weapon zones")
def two_hander_bow_with_unoccupied_zone(game_state):
    """Rule 8.2.15a: A two-hander bow is equipped but only occupies one zone."""
    game_state.has_two_hander_bow = True
    game_state.two_hander_bow_unoccupied_zone = "right"  # The zone the bow doesn't occupy
    game_state.empty_weapon_zones = 0  # Both zones are "equipped" but one is free for a quiver


@given("all of the player's weapon zones are occupied by non-bow permanents")
def all_weapon_zones_occupied_non_bow(game_state):
    """Rule 8.2.15a: All weapon zones are occupied by non-bow weapons."""
    game_state.player_weapon_zones = {"left": "sword", "right": "shield"}
    game_state.empty_weapon_zones = 0
    game_state.has_two_hander_bow = False


# ---- When steps ----

@when("the game checks the object's handedness")
def check_handedness(game_state):
    """Check whether an object is a one-hander or two-hander."""
    game_state.handedness_result = game_state.check_subtype_handedness(
        game_state.test_card, game_state.test_subtype
    )


@when("the game checks if the one-hander can be equipped")
def check_one_hander_equip(game_state):
    """Rule 8.2.1b: Check if a one-hander can be equipped."""
    game_state.equip_result = game_state.check_one_hander_equippable(
        game_state.test_card,
        empty_zones=game_state.empty_weapon_zones
    )


@when("the game checks if the two-hander can be equipped")
def check_two_hander_equip(game_state):
    """Rule 8.2.2b: Check if a two-hander can be equipped."""
    game_state.equip_result = game_state.check_two_hander_equippable(
        game_state.test_card,
        empty_zones=game_state.empty_weapon_zones
    )


@when("the game checks which weapon zones the two-hander occupies")
def check_two_hander_occupation(game_state):
    """Rule 8.2.2c: Check which weapon zone the two-hander occupies."""
    game_state.occupation_result = game_state.check_two_hander_occupation(game_state.test_card)


@when("the game checks if the card is an attack")
def check_is_attack(game_state):
    """Rule 8.2.3a: Check if the card is considered an attack."""
    game_state.is_attack_result = game_state.check_is_attack(
        game_state.test_card,
        location=game_state.card_location
    )


@when("the player plays the attack card")
def play_attack_card(game_state):
    """Rule 8.2.3b: Play an attack card."""
    game_state.play_result = game_state.attempt_play_attack(game_state.test_card)


@when("the resolution completes")
def resolution_completes(game_state):
    """Simulate a card resolving as a layer on the stack."""
    game_state.resolution_result = game_state.resolve_subtype_layer(
        game_state.test_card,
        game_state.test_subtype
    )


@when(parsers.parse("the game checks the {subtype_name}'s status"))
def check_subtype_status(game_state, subtype_name):
    """Check the status of the card (permanent or not)."""
    game_state.status_result = game_state.check_permanent_status(
        game_state.test_card,
        location=game_state.card_location
    )


@when("the game checks if the arrow can be played")
def check_arrow_playable(game_state):
    """Rule 8.2.6a: Check if the arrow can be played."""
    game_state.play_check_result = game_state.check_arrow_playable(
        game_state.test_card,
        location=game_state.arrow_location,
        controls_bow=game_state.player_controls_bow
    )


@when("the game checks if trap provides additional functional rules")
def check_trap_functional(game_state):
    """Rule 8.2.7: Check if trap subtype adds functional rules."""
    game_state.trap_functional_result = game_state.check_subtype_is_functional("Trap")


@when("the ally permanent ceases to exist")
def ally_ceases_to_exist(game_state):
    """Rule 8.2.8a: Simulate the ally ceasing to exist."""
    game_state.ally_ceased_result = game_state.process_ally_cease_to_exist(game_state.ally_card)


@when("the End Phase begins")
def end_phase_begins(game_state):
    """Rule 8.2.8b: Simulate the End Phase beginning."""
    game_state.end_phase_result = game_state.process_end_phase_ally_life_reset(
        game_state.ally_card,
        base_life=game_state.ally_base_life,
        current_life=game_state.ally_current_life
    )


@when("the game checks who is the attacking hero for the chain link")
def check_attacking_hero(game_state):
    """Rule 8.2.8c: Check who is the attacking hero."""
    game_state.attacking_hero_result = game_state.get_attacking_hero_for_chain_link(
        attacking_permanent=game_state.ally_card,
        is_ally=True
    )


@when("the game checks who is the defending hero for the chain link")
def check_defending_hero(game_state):
    """Rule 8.2.8d: Check who is the defending hero."""
    game_state.defending_hero_result = game_state.get_defending_hero_for_chain_link(
        attack_target=game_state.ally_card,
        is_ally=True
    )


@when("the controlling player attempts to declare defending cards")
def attempt_declare_defenders(game_state):
    """Rule 8.2.8d: Attempt to declare defending cards."""
    game_state.defend_declaration_result = game_state.can_declare_defenders(
        attack_target=game_state.ally_card,
        is_ally=True,
        combat_step=game_state.combat_step
    )


@when("the controlling player attempts to play a defense reaction card")
def attempt_play_defense_reaction(game_state):
    """Rule 8.2.8d: Attempt to play a defense reaction card."""
    defense_card = game_state.create_card(name="Test Defense Reaction")
    game_state.defense_reaction_result = game_state.can_play_defense_reaction(
        attack_target=game_state.ally_card,
        is_ally=True,
        combat_step=game_state.combat_step
    )


@when("the game checks who dealt damage")
def check_who_dealt_damage(game_state):
    """Rule 8.2.8e: Check who dealt damage."""
    game_state.damage_dealer_result = game_state.check_damage_attribution(
        damage_source=game_state.ally_card,
        is_ally=True,
        amount=game_state.ally_damage_amount
    )


@when("the game checks who was dealt damage")
def check_who_received_damage(game_state):
    """Rule 8.2.8f: Check who was dealt damage."""
    game_state.damage_receiver_result = game_state.check_damage_received_attribution(
        damage_target=game_state.ally_card,
        is_ally=True,
        amount=game_state.ally_received_damage_amount
    )


@when("the new landmark enters the arena")
def new_landmark_enters_arena(game_state):
    """Rule 8.2.9b: Process the new landmark entering the arena."""
    game_state.landmark_entry_result = game_state.process_landmark_entry(
        game_state.test_card,
        existing_landmark=game_state.existing_landmark
    )


@when("the game processes the landmark as a defending card")
def process_landmark_as_defending_card(game_state):
    """Rule 8.2.9b: Process a landmark that is a defending card."""
    game_state.defending_landmark_result = game_state.process_defending_card_landmark(
        game_state.test_card
    )


@when("the game checks if the off-hand can be equipped")
def check_off_hand_equip(game_state):
    """Rule 8.2.10a: Check if an off-hand can be equipped."""
    game_state.equip_result = game_state.check_off_hand_equippable(
        game_state.test_card,
        empty_zones=game_state.empty_weapon_zones,
        has_off_hand=getattr(game_state, 'player_has_off_hand', False)
    )


@when("the game checks if the second off-hand can be equipped")
def check_second_off_hand_equip(game_state):
    """Rule 8.2.10b: Check if a second off-hand can be equipped."""
    game_state.equip_result = game_state.check_off_hand_equippable(
        game_state.test_card,
        empty_zones=game_state.empty_weapon_zones,
        has_off_hand=True  # Already has one
    )


@when("the affliction enters the arena")
def affliction_enters_arena(game_state):
    """Rule 8.2.11c: Process the affliction entering the arena."""
    game_state.affliction_entry_result = game_state.process_affliction_entry(
        game_state.test_card,
        has_controller=getattr(game_state, 'affliction_has_controller', True),
        can_enter_under_opponent=getattr(game_state, 'affliction_can_enter_under_opponent', True)
    )


@when("the affliction attempts to enter the arena")
def affliction_attempts_entry(game_state):
    """Rule 8.2.11c: Attempt to process the affliction entering the arena."""
    game_state.affliction_entry_result = game_state.process_affliction_entry(
        game_state.test_card,
        has_controller=True,
        can_enter_under_opponent=False  # Cannot enter
    )


@when("the game checks if the quiver can be equipped")
def check_quiver_equip(game_state):
    """Rule 8.2.15a: Check if a quiver can be equipped."""
    game_state.equip_result = game_state.check_quiver_equippable(
        game_state.test_card,
        empty_zones=game_state.empty_weapon_zones,
        has_two_hander_bow=getattr(game_state, 'has_two_hander_bow', False),
        has_quiver=getattr(game_state, 'player_has_quiver', False)
    )


@when("the game checks if the quiver can be equipped to the unoccupied zone")
def check_quiver_equip_bow_zone(game_state):
    """Rule 8.2.15a: Check if quiver can share zone with two-hander bow."""
    game_state.equip_result = game_state.check_quiver_equippable(
        game_state.test_card,
        empty_zones=0,  # No empty zones, but there's a bow
        has_two_hander_bow=True,
        has_quiver=False
    )


@when("the game checks if the second quiver can be equipped")
def check_second_quiver_equip(game_state):
    """Rule 8.2.15b: Check if a second quiver can be equipped."""
    game_state.equip_result = game_state.check_quiver_equippable(
        game_state.test_card,
        empty_zones=game_state.empty_weapon_zones,
        has_two_hander_bow=False,
        has_quiver=True  # Already has one
    )


# ---- Then steps ----

@then("the object is considered a one-hander")
def assert_is_one_hander(game_state):
    """Rule 8.2.1a: The object is a one-hander."""
    assert game_state.handedness_result.is_one_hander is True, \
        "Expected object with (1H) subtype to be considered a one-hander"


@then("the one-hander can be equipped to the weapon zone")
def assert_one_hander_can_equip(game_state):
    """Rule 8.2.1b: One-hander can equip to available weapon zone."""
    assert game_state.equip_result.can_equip is True, \
        "Expected one-hander to be equippable to available weapon zone"


@then("the one-hander cannot be equipped")
def assert_one_hander_cannot_equip(game_state):
    """Rule 8.2.1b: One-hander cannot equip without empty weapon zone."""
    assert game_state.equip_result.can_equip is False, \
        "Expected one-hander to be blocked when no empty weapon zone"


@then("the object is considered a two-hander")
def assert_is_two_hander(game_state):
    """Rule 8.2.2a: The object is a two-hander."""
    assert game_state.handedness_result.is_two_hander is True, \
        "Expected object with (2H) subtype to be considered a two-hander"


@then("the two-hander can be equipped to two weapon zones")
def assert_two_hander_can_equip(game_state):
    """Rule 8.2.2b: Two-hander can equip to two available weapon zones."""
    assert game_state.equip_result.can_equip is True, \
        "Expected two-hander to be equippable to two available weapon zones"


@then("the two-hander cannot be equipped")
def assert_two_hander_cannot_equip(game_state):
    """Rule 8.2.2b: Two-hander cannot equip without two empty weapon zones."""
    assert game_state.equip_result.can_equip is False, \
        "Expected two-hander to be blocked when fewer than two empty weapon zones"


@then("the two-hander occupies one of the two weapon zones")
def assert_two_hander_occupies_one_zone(game_state):
    """Rule 8.2.2c: Two-hander occupies exactly one zone."""
    assert game_state.occupation_result.occupied_zone_count == 1, \
        "Expected two-hander to occupy exactly one weapon zone"


@then("the two-hander does not occupy both weapon zones simultaneously")
def assert_two_hander_not_both_zones(game_state):
    """Rule 8.2.2c: Two-hander does not occupy both zones simultaneously."""
    assert game_state.occupation_result.occupies_both is False, \
        "Expected two-hander to not occupy both zones simultaneously"


@then("the card is considered an attack")
def assert_card_is_attack(game_state):
    """Rule 8.2.3a: The card is considered an attack."""
    assert game_state.is_attack_result.is_attack is True, \
        f"Expected card with Attack subtype at '{game_state.card_location}' to be considered an attack"


@then("the combat chain opens")
def assert_combat_chain_opens(game_state):
    """Rule 8.2.3b: Playing an attack card opens the combat chain."""
    assert game_state.play_result.combat_chain_opened is True, \
        "Expected combat chain to open when attack card is played"


@then("the layer step of combat begins")
def assert_layer_step_begins(game_state):
    """Rule 8.2.3b: The layer step of combat begins."""
    assert game_state.play_result.layer_step_started is True, \
        "Expected layer step of combat to begin when attack card is played"


@then(parsers.parse("the {subtype_name} enters the arena"))
def assert_enters_arena(game_state, subtype_name):
    """Rule 8.2.4a/5a/9a/11a/12a/16a: The card enters the arena."""
    assert game_state.resolution_result.entered_arena is True, \
        f"Expected {subtype_name} to enter the arena on resolution"


@then(parsers.parse("the {subtype_name} is a permanent in the arena"))
def assert_is_permanent(game_state, subtype_name):
    """Rule 8.2.4b/5b/12b/16b: The card is a permanent."""
    assert game_state.status_result.is_permanent is True, \
        f"Expected {subtype_name} in the arena to be a permanent"


@then(parsers.parse("the {subtype_name} is not considered a permanent"))
def assert_not_permanent(game_state, subtype_name):
    """Rule 8.2.4b/5b/9b/11b/12b/16b: The card is not a permanent."""
    assert game_state.status_result.is_permanent is False, \
        f"Expected {subtype_name} added as defending card to not be a permanent"


@then("the arrow can be played")
def assert_arrow_can_play(game_state):
    """Rule 8.2.6a: Arrow can be played."""
    assert game_state.play_check_result.can_play is True, \
        "Expected arrow to be playable from arsenal when player controls a bow"


@then("the arrow cannot be played because it is not in the arsenal")
def assert_arrow_blocked_not_arsenal(game_state):
    """Rule 8.2.6a: Arrow cannot be played from non-arsenal location."""
    assert game_state.play_check_result.can_play is False, \
        "Expected arrow to be blocked when not played from arsenal"
    assert "arsenal" in game_state.play_check_result.reason.lower(), \
        "Expected reason to mention arsenal requirement"


@then("the arrow cannot be played because the player does not control a bow")
def assert_arrow_blocked_no_bow(game_state):
    """Rule 8.2.6a: Arrow cannot be played without controlling a bow."""
    assert game_state.play_check_result.can_play is False, \
        "Expected arrow to be blocked when player has no bow"
    assert "bow" in game_state.play_check_result.reason.lower(), \
        "Expected reason to mention bow requirement"


@then("trap does not add additional rules to the object")
def assert_trap_not_functional(game_state):
    """Rule 8.2.7: Trap subtype is not functional."""
    assert game_state.trap_functional_result.is_functional is False, \
        "Expected trap subtype to not add additional rules (non-functional as of 2023)"


@then("the ally is considered to have died")
def assert_ally_considered_dead(game_state):
    """Rule 8.2.8a: Ally ceasing to exist is death."""
    assert game_state.ally_ceased_result.is_considered_dead is True, \
        "Expected ally to be considered dead when it ceases to exist"


@then("the ally's life total is reset to its base life")
def assert_ally_life_reset(game_state):
    """Rule 8.2.8b: Ally's life total is reset to base life."""
    assert game_state.end_phase_result.life_reset is True, \
        "Expected ally's life total to reset to base life during End Phase"
    assert game_state.end_phase_result.new_life == game_state.ally_base_life, \
        f"Expected ally life to be {game_state.ally_base_life}, got {game_state.end_phase_result.new_life}"


@then("the controlling player is not considered the attacking hero")
def assert_player_not_attacking_hero(game_state):
    """Rule 8.2.8c: Controlling player is not the attacking hero."""
    assert game_state.attacking_hero_result.controller_is_attacking_hero is False, \
        "Expected controlling player to not be the attacking hero when ally is attacking"


@then("the controlling player's hero is not considered the attacking hero")
def assert_players_hero_not_attacking_hero(game_state):
    """Rule 8.2.8c: Controlling player's hero is not the attacking hero."""
    assert game_state.attacking_hero_result.controller_hero_is_attacking_hero is False, \
        "Expected controlling player's hero to not be the attacking hero when ally is attacking"


@then("the controlling player is not considered the defending hero")
def assert_player_not_defending_hero(game_state):
    """Rule 8.2.8d: Controlling player is not the defending hero."""
    assert game_state.defending_hero_result.controller_is_defending_hero is False, \
        "Expected controlling player to not be the defending hero when ally is attack target"


@then("the controlling player's hero is not considered the defending hero")
def assert_players_hero_not_defending_hero(game_state):
    """Rule 8.2.8d: Controlling player's hero is not the defending hero."""
    assert game_state.defending_hero_result.controller_hero_is_defending_hero is False, \
        "Expected controlling player's hero to not be the defending hero when ally is attack target"


@then("the controlling player cannot declare defending cards")
def assert_cannot_declare_defenders(game_state):
    """Rule 8.2.8d: Controlling player cannot declare defending cards."""
    assert game_state.defend_declaration_result.can_declare is False, \
        "Expected controlling player to be unable to declare defenders when ally is attack target"


@then("the defense reaction cannot be played because the ally is the attack target")
def assert_defense_reaction_blocked(game_state):
    """Rule 8.2.8d: Defense reaction cannot be played when ally is attack target."""
    assert game_state.defense_reaction_result.can_play is False, \
        "Expected defense reaction to be blocked when ally is the attack target"


@then("the controlling player is not considered to have dealt damage")
def assert_player_not_damage_dealer(game_state):
    """Rule 8.2.8e: Controlling player is not considered to have dealt damage."""
    assert game_state.damage_dealer_result.controller_dealt_damage is False, \
        "Expected controlling player to not be considered to have dealt damage when ally dealt it"


@then("the controlling player's hero is not considered to have dealt damage")
def assert_players_hero_not_damage_dealer(game_state):
    """Rule 8.2.8e: Controlling player's hero is not considered to have dealt damage."""
    assert game_state.damage_dealer_result.controller_hero_dealt_damage is False, \
        "Expected controlling player's hero to not be considered to have dealt damage"


@then("the controlling player is not considered to have been dealt damage")
def assert_player_not_damage_receiver(game_state):
    """Rule 8.2.8f: Controlling player is not considered to have been dealt damage."""
    assert game_state.damage_receiver_result.controller_received_damage is False, \
        "Expected controlling player to not be considered to have been dealt damage when ally received it"


@then("the controlling player's hero is not considered to have been dealt damage")
def assert_players_hero_not_damage_receiver(game_state):
    """Rule 8.2.8f: Controlling player's hero is not considered to have been dealt damage."""
    assert game_state.damage_receiver_result.controller_hero_received_damage is False, \
        "Expected controlling player's hero to not be considered to have been dealt damage"


@then("the new landmark becomes a permanent")
def assert_new_landmark_is_permanent(game_state):
    """Rule 8.2.9b: New landmark becomes a permanent."""
    assert game_state.landmark_entry_result.new_landmark_is_permanent is True, \
        "Expected new landmark to become a permanent in the arena"


@then("the previous landmark permanent is cleared from the arena")
def assert_old_landmark_cleared(game_state):
    """Rule 8.2.9b: Previous landmark is cleared from arena."""
    assert game_state.landmark_entry_result.previous_landmark_cleared is True, \
        "Expected previous landmark to be cleared when new landmark enters the arena"


@then("the existing landmark permanent is not cleared")
def assert_existing_landmark_not_cleared(game_state):
    """Rule 8.2.9b: Existing landmark is not cleared when added as defending card."""
    assert game_state.defending_landmark_result.existing_landmark_cleared is False, \
        "Expected existing landmark to not be cleared when landmark is added as defending card"


@then("the off-hand can be equipped to the weapon zone")
def assert_off_hand_can_equip(game_state):
    """Rule 8.2.10a: Off-hand can be equipped."""
    assert game_state.equip_result.can_equip is True, \
        "Expected off-hand to be equippable to available weapon zone"


@then("the off-hand cannot be equipped")
def assert_off_hand_cannot_equip(game_state):
    """Rule 8.2.10a: Off-hand cannot be equipped without empty zone."""
    assert game_state.equip_result.can_equip is False, \
        "Expected off-hand to be blocked when no empty weapon zone"


@then("the second off-hand cannot be equipped because the player already has one")
def assert_second_off_hand_blocked(game_state):
    """Rule 8.2.10b: Second off-hand cannot be equipped."""
    assert game_state.equip_result.can_equip is False, \
        "Expected second off-hand to be blocked (player can only have one)"
    assert game_state.equip_result.reason == "already_has_off_hand", \
        "Expected reason to indicate player already has an off-hand"


@then("the controller declares an opponent")
def assert_controller_declares_opponent(game_state):
    """Rule 8.2.11c: Affliction controller declares an opponent."""
    assert game_state.affliction_entry_result.opponent_declared is True, \
        "Expected affliction controller to declare an opponent"


@then("the affliction enters the arena under that opponent's control")
def assert_affliction_under_opponent_control(game_state):
    """Rule 8.2.11c: Affliction enters under opponent's control."""
    assert game_state.affliction_entry_result.entered_under_opponent is True, \
        "Expected affliction to enter the arena under the declared opponent's control"


@then("the affliction's owner declares an opponent")
def assert_owner_declares_opponent(game_state):
    """Rule 8.2.11c: When no controller, owner declares opponent."""
    assert game_state.affliction_entry_result.owner_declared_opponent is True, \
        "Expected affliction owner to declare opponent when affliction has no controller"


@then("the affliction is cleared")
def assert_affliction_cleared(game_state):
    """Rule 8.2.11c: Affliction is cleared when it cannot enter."""
    assert game_state.affliction_entry_result.was_cleared is True, \
        "Expected affliction to be cleared when it cannot enter under any opponent's control"


@then("the affliction is not considered to have entered the arena")
def assert_affliction_not_entered(game_state):
    """Rule 8.2.11c: Cleared affliction did not enter the arena."""
    assert game_state.affliction_entry_result.entered_arena is False, \
        "Expected cleared affliction to not be considered to have entered the arena"


@then("the invocation enters the arena with its back-face active")
def assert_invocation_back_face(game_state):
    """Rule 8.2.13a: Invocation enters with back-face active."""
    assert game_state.resolution_result.back_face_active is True, \
        "Expected invocation to enter the arena with its back-face active"


@then("the invocation becomes a permanent")
def assert_invocation_permanent(game_state):
    """Rule 8.2.13a: Invocation becomes a permanent."""
    assert game_state.resolution_result.is_permanent is True, \
        "Expected invocation to become a permanent when it enters the arena"


@then("the construct enters the arena with its back-face active")
def assert_construct_back_face(game_state):
    """Rule 8.2.14a: Construct enters with back-face active."""
    assert game_state.resolution_result.back_face_active is True, \
        "Expected construct to enter the arena with its back-face active"


@then("the construct becomes a permanent")
def assert_construct_permanent(game_state):
    """Rule 8.2.14a: Construct becomes a permanent."""
    assert game_state.resolution_result.is_permanent is True, \
        "Expected construct to become a permanent when it enters the arena"


@then("the quiver can be equipped to the weapon zone")
def assert_quiver_can_equip(game_state):
    """Rule 8.2.15a: Quiver can be equipped."""
    assert game_state.equip_result.can_equip is True, \
        "Expected quiver to be equippable to available weapon zone"


@then("the quiver can be equipped to the weapon zone alongside the two-hander bow")
def assert_quiver_can_share_bow_zone(game_state):
    """Rule 8.2.15a: Quiver can share zone with two-hander bow."""
    assert game_state.equip_result.can_equip is True, \
        "Expected quiver to be equippable to zone shared with two-hander bow"
    assert game_state.equip_result.sharing_with_two_hander_bow is True, \
        "Expected quiver to be sharing a zone with the two-hander bow"


@then("the quiver cannot be equipped")
def assert_quiver_cannot_equip(game_state):
    """Rule 8.2.15a: Quiver cannot be equipped without valid zone."""
    assert game_state.equip_result.can_equip is False, \
        "Expected quiver to be blocked when no valid weapon zone"


@then("the second quiver cannot be equipped because the player already has one")
def assert_second_quiver_blocked(game_state):
    """Rule 8.2.15b: Second quiver cannot be equipped."""
    assert game_state.equip_result.can_equip is False, \
        "Expected second quiver to be blocked (player can only have one)"
    assert game_state.equip_result.reason == "already_has_quiver", \
        "Expected reason to indicate player already has a quiver"


# ===== Fixtures =====

@pytest.fixture
def game_state():
    """
    Fixture providing game state for testing Section 8.2: Subtype Keywords.

    Uses BDDGameState which integrates with the real engine.
    Reference: Rules 8.2.1–8.2.16
    """
    from tests.bdd_helpers import BDDGameState

    state = BDDGameState()

    # Initialize default state
    state.test_card = None
    state.test_subtype = None
    state.test_subtype_key = None
    state.card_location = None
    state.combat_chain_open = False
    state.resolving_as_layer = False
    state.card_is_permanent = False
    state.card_is_defending = False
    state.empty_weapon_zones = 0
    state.player_controls_bow = False
    state.ally_in_arena = False
    state.ally_is_attacking = False
    state.ally_is_attack_target = False
    state.existing_landmark_in_arena = False
    state.player_has_off_hand = False
    state.player_has_quiver = False
    state.has_two_hander_bow = False
    state.affliction_has_controller = True
    state.affliction_can_enter_under_opponent = True

    return state
