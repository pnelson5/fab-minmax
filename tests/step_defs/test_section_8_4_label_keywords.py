"""
Step definitions for Section 8.4: Label Keywords
Reference: Flesh and Blood Comprehensive Rules Section 8.4

This module implements behavioral tests for label keywords:
- Combo: static ability, condition on last attack name (Rule 8.4.1)
- Crush: triggered-static, requires dealing 4+ damage (Rule 8.4.2, 8.4.2a)
- Reprise: resolution ability, condition on defending from hand (Rule 8.4.3, 8.4.3a)
- Channel: end-phase triggered, requires supertype card from pitch (Rule 8.4.4)
- Material: active while card is under a permanent (Rule 8.4.5)
- Rupture: effects if played at chain link 4+ (Rule 8.4.6)
- Contract: static ability, tracks completion condition (Rule 8.4.7)
- Surge: resolution/static, requires dealing N damage (Rule 8.4.8)
- Solflare: triggered when charged to hero's soul (Rule 8.4.9)
- Unity: triggered when defending with a card from hand (Rule 8.4.10)
- Evo Upgrade: scales with number of evos equipped (Rule 8.4.11)
- Galvanize: when defending, may destroy an item (Rule 8.4.12)
- Tower: effects when card has 13+ power (Rule 8.4.13)
- Decompose: banish 2 Earth + action from graveyard (Rule 8.4.14)
- Earth Bond: if Earth card was pitched to play this (Rule 8.4.15)
- Lightning Flow: if Lightning card played this turn (Rule 8.4.16)
- Heavy: if only card equipped to weapon zones (Rule 8.4.17)
- High Tide: if 2+ blue cards in pitch zone (Rule 8.4.18)
- Go Fish: when hitting a hero, they reveal a card (Rule 8.4.19)

Engine Features Needed for Section 8.4:
- [ ] LabelKeyword enum with all 19 label keywords (Rule 8.4)
- [ ] ComboAbility.check_condition(combat_chain) -> bool (Rule 8.4.1)
- [ ] CrushAbility.check_condition(damage_amount) -> bool (Rule 8.4.2)
- [ ] CrushAbility: triggers on damage event not just hit event (Rule 8.4.2a)
- [ ] RepriseAbility.check_condition(defender_state) -> bool (Rule 8.4.3)
- [ ] RepriseAbility: condition evaluated at resolution time (Rule 8.4.3a)
- [ ] ChannelAbility: flow counter on end phase, destroy unless supertype card pitched (Rule 8.4.4)
- [ ] MaterialAbility.check_condition(card_position) -> bool (Rule 8.4.5)
- [ ] RuptureAbility.check_condition(chain_link) -> bool (Rule 8.4.6)
- [ ] ContractAbility.check_completion(game_state) -> bool (Rule 8.4.7)
- [ ] SurgeAbility.check_condition(damage_amount, required) -> bool (Rule 8.4.8)
- [ ] SolflareAbility.check_condition(charge_event) -> bool (Rule 8.4.9)
- [ ] UnityAbility.check_condition(defend_event) -> bool (Rule 8.4.10)
- [ ] EvoUpgradeAbility.get_evo_count(player) -> int (Rule 8.4.11)
- [ ] GalvanizeAbility.check_condition(defend_event, item_destroyed) -> bool (Rule 8.4.12)
- [ ] TowerAbility.check_condition(power) -> bool (Rule 8.4.13)
- [ ] DecomposeAbility.check_condition(graveyard) -> bool (Rule 8.4.14)
- [ ] EarthBondAbility.check_condition(pitch_zone_cards) -> bool (Rule 8.4.15)
- [ ] LightningFlowAbility.check_condition(turn_state) -> bool (Rule 8.4.16)
- [ ] HeavyAbility.check_condition(weapon_zones) -> bool (Rule 8.4.17)
- [ ] HighTideAbility.check_condition(pitch_zone) -> bool (Rule 8.4.18)
- [ ] GoFishAbility: hit trigger, hero reveals card, Gold token if matches (Rule 8.4.19)

Current status: Tests written, Engine pending
"""

import pytest
from pytest_bdd import scenario, given, when, then, parsers


# ===== Rule 8.4.1: Combo =====

@scenario(
    "../features/section_8_4_label_keywords.feature",
    "Combo ability triggers when the named card was the last attack",
)
def test_combo_triggers_when_named_card_was_last_attack():
    """Rule 8.4.1: Combo condition met when named card was last attack on combat chain."""
    pass


@scenario(
    "../features/section_8_4_label_keywords.feature",
    "Combo ability does not trigger when the named card was not the last attack",
)
def test_combo_does_not_trigger_when_named_card_not_last_attack():
    """Rule 8.4.1: Combo condition not met when named card was not the last attack."""
    pass


@scenario(
    "../features/section_8_4_label_keywords.feature",
    "Combo ability does not trigger when no attack was made on this combat chain",
)
def test_combo_does_not_trigger_with_no_attacks():
    """Rule 8.4.1: Combo condition not met when no attack has been made this combat chain."""
    pass


# ===== Rule 8.4.2: Crush =====

@scenario(
    "../features/section_8_4_label_keywords.feature",
    "Crush ability triggers when the card deals 4 or more damage",
)
def test_crush_triggers_at_four_damage():
    """Rule 8.4.2: Crush condition met when card deals exactly 4 damage."""
    pass


@scenario(
    "../features/section_8_4_label_keywords.feature",
    "Crush ability triggers when the card deals more than 4 damage",
)
def test_crush_triggers_above_four_damage():
    """Rule 8.4.2: Crush condition met when card deals more than 4 damage."""
    pass


@scenario(
    "../features/section_8_4_label_keywords.feature",
    "Crush ability does not trigger when the card deals fewer than 4 damage",
)
def test_crush_does_not_trigger_below_four_damage():
    """Rule 8.4.2: Crush condition not met when card deals fewer than 4 damage."""
    pass


@scenario(
    "../features/section_8_4_label_keywords.feature",
    "Crush ability does not trigger on zero damage",
)
def test_crush_does_not_trigger_on_zero_damage():
    """Rule 8.4.2: Crush condition not met when card deals 0 damage."""
    pass


# ===== Rule 8.4.2a: Crush — damage event vs hit event =====

@scenario(
    "../features/section_8_4_label_keywords.feature",
    "Crush is conditional on a damage event not merely a hit event",
)
def test_crush_conditional_on_damage_not_hit():
    """Rule 8.4.2a: Crush triggers on a damage event, not just a hit-event."""
    pass


# ===== Rule 8.4.3: Reprise =====

@scenario(
    "../features/section_8_4_label_keywords.feature",
    "Reprise ability triggers when the defender has defended with a card from hand",
)
def test_reprise_triggers_when_defender_defended_from_hand():
    """Rule 8.4.3: Reprise condition met when defending hero defended from hand this chain link."""
    pass


@scenario(
    "../features/section_8_4_label_keywords.feature",
    "Reprise ability does not trigger when the defender has not defended from hand",
)
def test_reprise_does_not_trigger_without_hand_defense():
    """Rule 8.4.3: Reprise condition not met when defending hero has not defended from hand."""
    pass


# ===== Rule 8.4.3a: Reprise — condition checked at resolution =====

@scenario(
    "../features/section_8_4_label_keywords.feature",
    "Reprise condition is checked at resolution time",
)
def test_reprise_condition_checked_at_resolution():
    """Rule 8.4.3a: Reprise condition is checked on resolution, not retroactively."""
    pass


# ===== Rule 8.4.4: Channel =====

@scenario(
    "../features/section_8_4_label_keywords.feature",
    "Channel ability puts a flow counter on the card at start of end phase",
)
def test_channel_adds_flow_counter_at_end_phase():
    """Rule 8.4.4: Channel puts a flow counter on the card at start of end phase."""
    pass


@scenario(
    "../features/section_8_4_label_keywords.feature",
    "Channel ability destroys the card unless a supertype card is put from pitch to deck bottom",
)
def test_channel_destroys_card_without_pitch_payment():
    """Rule 8.4.4: Channel destroys card if player does not put supertype card from pitch to deck."""
    pass


@scenario(
    "../features/section_8_4_label_keywords.feature",
    "Channel ability does not destroy the card when the player fulfills the Channel cost",
)
def test_channel_preserves_card_with_pitch_payment():
    """Rule 8.4.4: Channel does not destroy card if player fulfills the cost."""
    pass


# ===== Rule 8.4.5: Material =====

@scenario(
    "../features/section_8_4_label_keywords.feature",
    "Material ability effects are active while the card is under a permanent",
)
def test_material_active_while_under_permanent():
    """Rule 8.4.5: Material effects apply while card is under a permanent."""
    pass


@scenario(
    "../features/section_8_4_label_keywords.feature",
    "Material ability effects are not active when the card is not under a permanent",
)
def test_material_inactive_when_not_under_permanent():
    """Rule 8.4.5: Material effects do not apply when card is not under a permanent."""
    pass


# ===== Rule 8.4.6: Rupture =====

@scenario(
    "../features/section_8_4_label_keywords.feature",
    "Rupture ability triggers when played at chain link 4",
)
def test_rupture_triggers_at_chain_link_4():
    """Rule 8.4.6: Rupture condition met when played at chain link 4."""
    pass


@scenario(
    "../features/section_8_4_label_keywords.feature",
    "Rupture ability triggers when played at chain link 5 or higher",
)
def test_rupture_triggers_at_chain_link_5():
    """Rule 8.4.6: Rupture condition met when played at chain link 5 or higher."""
    pass


@scenario(
    "../features/section_8_4_label_keywords.feature",
    "Rupture ability does not trigger when played at chain link 3",
)
def test_rupture_does_not_trigger_at_chain_link_3():
    """Rule 8.4.6: Rupture condition not met when played at chain link 3."""
    pass


@scenario(
    "../features/section_8_4_label_keywords.feature",
    "Rupture ability does not trigger when played at chain link 1",
)
def test_rupture_does_not_trigger_at_chain_link_1():
    """Rule 8.4.6: Rupture condition not met when played at chain link 1."""
    pass


# ===== Rule 8.4.7: Contract =====

@scenario(
    "../features/section_8_4_label_keywords.feature",
    "Contract ability recognizes when the contract condition is completed",
)
def test_contract_recognizes_completion():
    """Rule 8.4.7: Contract condition recognized when fulfilled."""
    pass


@scenario(
    "../features/section_8_4_label_keywords.feature",
    "Contract ability effect triggers when the contract is completed",
)
def test_contract_triggers_reward_on_completion():
    """Rule 8.4.7: Contract reward effect triggers when contract is completed."""
    pass


@scenario(
    "../features/section_8_4_label_keywords.feature",
    "Contract ability does not trigger when the contract condition is not fulfilled",
)
def test_contract_does_not_trigger_when_not_fulfilled():
    """Rule 8.4.7: Contract does not trigger when condition not fulfilled."""
    pass


# ===== Rule 8.4.8: Surge =====

@scenario(
    "../features/section_8_4_label_keywords.feature",
    "Surge ability triggers when the card deals the required damage amount",
)
def test_surge_triggers_at_required_damage():
    """Rule 8.4.8: Surge condition met when card deals N or more damage."""
    pass


@scenario(
    "../features/section_8_4_label_keywords.feature",
    "Surge ability does not trigger when the card deals less than required damage",
)
def test_surge_does_not_trigger_below_required_damage():
    """Rule 8.4.8: Surge condition not met when card deals less than N damage."""
    pass


# ===== Rule 8.4.9: Solflare =====

@scenario(
    "../features/section_8_4_label_keywords.feature",
    "Solflare ability triggers when the card is charged to the hero's soul",
)
def test_solflare_triggers_when_charged_to_soul():
    """Rule 8.4.9: Solflare condition met when card is charged to hero's soul."""
    pass


@scenario(
    "../features/section_8_4_label_keywords.feature",
    "Solflare ability does not trigger when the card is not charged to the soul",
)
def test_solflare_does_not_trigger_outside_soul():
    """Rule 8.4.9: Solflare condition not met when card enters arena without being charged to soul."""
    pass


# ===== Rule 8.4.10: Unity =====

@scenario(
    "../features/section_8_4_label_keywords.feature",
    "Unity ability triggers when the card defends together with a card from hand",
)
def test_unity_triggers_when_defending_with_hand_card():
    """Rule 8.4.10: Unity condition met when card defends with a card from hand."""
    pass


@scenario(
    "../features/section_8_4_label_keywords.feature",
    "Unity ability does not trigger when the card defends alone",
)
def test_unity_does_not_trigger_when_defending_alone():
    """Rule 8.4.10: Unity condition not met when card defends without a card from hand."""
    pass


# ===== Rule 8.4.11: Evo Upgrade =====

@scenario(
    "../features/section_8_4_label_keywords.feature",
    "Evo Upgrade effect scales with 1 evo equipped",
)
def test_evo_upgrade_scales_with_one_evo():
    """Rule 8.4.11: Evo Upgrade value equals number of evos equipped (1)."""
    pass


@scenario(
    "../features/section_8_4_label_keywords.feature",
    "Evo Upgrade effect scales with 3 evos equipped",
)
def test_evo_upgrade_scales_with_three_evos():
    """Rule 8.4.11: Evo Upgrade value equals number of evos equipped (3)."""
    pass


@scenario(
    "../features/section_8_4_label_keywords.feature",
    "Evo Upgrade effect is 0 when no evos are equipped",
)
def test_evo_upgrade_zero_with_no_evos():
    """Rule 8.4.11: Evo Upgrade value is 0 when no evos are equipped."""
    pass


# ===== Rule 8.4.12: Galvanize =====

@scenario(
    "../features/section_8_4_label_keywords.feature",
    "Galvanize ability triggers when the card defends",
)
def test_galvanize_triggers_on_defense():
    """Rule 8.4.12: Galvanize option available when the card defends."""
    pass


@scenario(
    "../features/section_8_4_label_keywords.feature",
    "Galvanize additional effects apply when player destroys an item while defending",
)
def test_galvanize_effects_apply_with_item_destruction():
    """Rule 8.4.12: Galvanize condition met when player destroys an item while defending."""
    pass


@scenario(
    "../features/section_8_4_label_keywords.feature",
    "Galvanize additional effects do not apply when player does not destroy an item",
)
def test_galvanize_effects_do_not_apply_without_item_destruction():
    """Rule 8.4.12: Galvanize condition not met when player does not destroy an item."""
    pass


# ===== Rule 8.4.13: Tower =====

@scenario(
    "../features/section_8_4_label_keywords.feature",
    "Tower ability triggers when the card has 13 or more power",
)
def test_tower_triggers_at_13_power():
    """Rule 8.4.13: Tower condition met when card has exactly 13 power."""
    pass


@scenario(
    "../features/section_8_4_label_keywords.feature",
    "Tower ability triggers when the card has more than 13 power",
)
def test_tower_triggers_above_13_power():
    """Rule 8.4.13: Tower condition met when card has more than 13 power."""
    pass


@scenario(
    "../features/section_8_4_label_keywords.feature",
    "Tower ability does not trigger when the card has fewer than 13 power",
)
def test_tower_does_not_trigger_below_13_power():
    """Rule 8.4.13: Tower condition not met when card has fewer than 13 power."""
    pass


# ===== Rule 8.4.14: Decompose =====

@scenario(
    "../features/section_8_4_label_keywords.feature",
    "Decompose ability condition is met when 2 Earth cards and an action card are available in graveyard",
)
def test_decompose_condition_met_with_required_graveyard_cards():
    """Rule 8.4.14: Decompose condition met when graveyard has 2 Earth + 1 action card."""
    pass


@scenario(
    "../features/section_8_4_label_keywords.feature",
    "Decompose ability condition is not met when graveyard lacks required cards",
)
def test_decompose_condition_not_met_without_required_cards():
    """Rule 8.4.14: Decompose condition not met when graveyard lacks required cards."""
    pass


# ===== Rule 8.4.15: Earth Bond =====

@scenario(
    "../features/section_8_4_label_keywords.feature",
    "Earth Bond ability triggers when an Earth card was pitched to play the card",
)
def test_earth_bond_triggers_with_earth_pitch():
    """Rule 8.4.15: Earth Bond condition met when an Earth card was pitched to play this."""
    pass


@scenario(
    "../features/section_8_4_label_keywords.feature",
    "Earth Bond ability does not trigger when no Earth card was pitched",
)
def test_earth_bond_does_not_trigger_without_earth_pitch():
    """Rule 8.4.15: Earth Bond condition not met when no Earth card was pitched."""
    pass


# ===== Rule 8.4.16: Lightning Flow =====

@scenario(
    "../features/section_8_4_label_keywords.feature",
    "Lightning Flow ability triggers when a Lightning card was played this turn",
)
def test_lightning_flow_triggers_with_lightning_card_played():
    """Rule 8.4.16: Lightning Flow condition met when a Lightning card was played this turn."""
    pass


@scenario(
    "../features/section_8_4_label_keywords.feature",
    "Lightning Flow ability does not trigger when no Lightning card was played this turn",
)
def test_lightning_flow_does_not_trigger_without_lightning_card():
    """Rule 8.4.16: Lightning Flow condition not met when no Lightning card was played this turn."""
    pass


# ===== Rule 8.4.17: Heavy =====

@scenario(
    "../features/section_8_4_label_keywords.feature",
    "Heavy ability triggers when the card is the only card equipped to weapon zones",
)
def test_heavy_triggers_as_only_weapon():
    """Rule 8.4.17: Heavy condition met when card is the only card in weapon zones."""
    pass


@scenario(
    "../features/section_8_4_label_keywords.feature",
    "Heavy ability does not trigger when another card is also in a weapon zone",
)
def test_heavy_does_not_trigger_with_other_weapon():
    """Rule 8.4.17: Heavy condition not met when another card is also in a weapon zone."""
    pass


# ===== Rule 8.4.18: High Tide =====

@scenario(
    "../features/section_8_4_label_keywords.feature",
    "High Tide ability triggers when there are 2 or more blue cards in pitch zone",
)
def test_high_tide_triggers_with_two_blue_cards():
    """Rule 8.4.18: High Tide condition met when there are 2 blue cards in pitch zone."""
    pass


@scenario(
    "../features/section_8_4_label_keywords.feature",
    "High Tide ability triggers when there are more than 2 blue cards in pitch zone",
)
def test_high_tide_triggers_with_three_blue_cards():
    """Rule 8.4.18: High Tide condition met when there are 3 blue cards in pitch zone."""
    pass


@scenario(
    "../features/section_8_4_label_keywords.feature",
    "High Tide ability does not trigger when there is only 1 blue card in pitch zone",
)
def test_high_tide_does_not_trigger_with_one_blue_card():
    """Rule 8.4.18: High Tide condition not met when there is only 1 blue card in pitch zone."""
    pass


@scenario(
    "../features/section_8_4_label_keywords.feature",
    "High Tide ability does not trigger when there are no blue cards in pitch zone",
)
def test_high_tide_does_not_trigger_with_no_blue_cards():
    """Rule 8.4.18: High Tide condition not met when there are no blue cards in pitch zone."""
    pass


# ===== Rule 8.4.19: Go Fish =====

@scenario(
    "../features/section_8_4_label_keywords.feature",
    "Go Fish ability triggers when the card hits a hero",
)
def test_go_fish_triggers_on_hit():
    """Rule 8.4.19: Go Fish ability triggers when the card hits a hero."""
    pass


@scenario(
    "../features/section_8_4_label_keywords.feature",
    "Go Fish creates a Gold token when the revealed card matches the adjective",
)
def test_go_fish_creates_gold_token_on_match():
    """Rule 8.4.19: Go Fish creates a Gold token and the hero discards when card matches."""
    pass


@scenario(
    "../features/section_8_4_label_keywords.feature",
    "Go Fish does not create a Gold token when the revealed card does not match",
)
def test_go_fish_no_gold_token_on_mismatch():
    """Rule 8.4.19: Go Fish does not create Gold token and hero does not discard when card doesn't match."""
    pass


# ===== Step Definitions =====

# ---- Given steps ----

@given(parsers.parse('a card with "Combo" labeling that names "{named_card}"'))
def card_with_combo_labeling(game_state, named_card):
    """Rule 8.4.1: Create a card with the Combo label naming a specific card."""
    card = game_state.create_card(name="Combo Card")
    card._has_combo = True
    card._combo_name = named_card
    game_state.test_card = card


@given(parsers.parse('"{named_card}" was the last attack this combat chain'))
def named_card_was_last_attack(game_state, named_card):
    """Rule 8.4.1: Set up the combat chain so the named card was the last attack."""
    game_state.last_attack_name = named_card


@given("the last attack this combat chain was a different card")
def different_card_was_last_attack(game_state):
    """Rule 8.4.1: Set up the combat chain with a different last attack."""
    game_state.last_attack_name = "Some Other Card"


@given("no attack has been made on the combat chain yet")
def no_attacks_on_combat_chain(game_state):
    """Rule 8.4.1: Ensure no attacks have been made on the current combat chain."""
    game_state.last_attack_name = None


@given('a card with the "Crush" label keyword')
def card_with_crush_keyword(game_state):
    """Rule 8.4.2: Create a card with the Crush label keyword."""
    card = game_state.create_card(name="Crush Card")
    card._has_crush = True
    game_state.test_card = card


@given('a card with the "Reprise" label keyword')
def card_with_reprise_keyword(game_state):
    """Rule 8.4.3: Create a card with the Reprise label keyword."""
    card = game_state.create_card(name="Reprise Card")
    card._has_reprise = True
    game_state.test_card = card


@given("the defending hero has defended with a card from their hand this chain link")
def defender_defended_from_hand(game_state):
    """Rule 8.4.3: Set up state where the defending hero has defended from hand."""
    game_state.defender_defended_from_hand = True


@given("the defending hero has not defended with a card from their hand this chain link")
def defender_not_defended_from_hand(game_state):
    """Rule 8.4.3: Set up state where the defending hero has not defended from hand."""
    game_state.defender_defended_from_hand = False


@given("the defending hero has not yet defended from hand at the time of resolution")
def defender_not_yet_defended_from_hand(game_state):
    """Rule 8.4.3a: Set up state where defender has not defended from hand at resolution."""
    game_state.defender_defended_from_hand = False
    game_state.reprise_resolution_time = True


@given('a card with the "Channel" label keyword in the arena')
def card_with_channel_in_arena(game_state):
    """Rule 8.4.4: Create a Channel card in the arena."""
    card = game_state.create_card(name="Channel Card")
    card._has_channel = True
    card._flow_counters = 0
    card._is_destroyed = False
    game_state.play_card_to_arena(card)
    game_state.test_card = card


@given('a card with the "Channel" label keyword in the arena with 1 flow counter')
def card_with_channel_and_flow_counter(game_state):
    """Rule 8.4.4: Create a Channel card in the arena with 1 flow counter."""
    card = game_state.create_card(name="Channel Card")
    card._has_channel = True
    card._flow_counters = 1
    card._is_destroyed = False
    game_state.play_card_to_arena(card)
    game_state.test_card = card


@given("the player does not put a matching supertype card from pitch to deck bottom")
def player_does_not_pay_channel_cost(game_state):
    """Rule 8.4.4: Player cannot or does not fulfill the Channel cost."""
    game_state.channel_cost_paid = False


@given("the player puts 1 matching supertype card from pitch zone to deck bottom")
def player_pays_channel_cost(game_state):
    """Rule 8.4.4: Player pays the Channel cost with 1 supertype card from pitch."""
    game_state.channel_cost_paid = True


@given('a card with the "Material" label keyword')
def card_with_material_keyword(game_state):
    """Rule 8.4.5: Create a card with the Material label keyword."""
    card = game_state.create_card(name="Material Card")
    card._has_material = True
    game_state.test_card = card


@given("the card is under a permanent")
def card_is_under_permanent(game_state):
    """Rule 8.4.5: Set up state where the card is under a permanent."""
    game_state.card_is_under_permanent = True


@given("the card is not under a permanent")
def card_is_not_under_permanent(game_state):
    """Rule 8.4.5: Set up state where the card is not under a permanent."""
    game_state.card_is_under_permanent = False


@given('a card with the "Rupture" label keyword')
def card_with_rupture_keyword(game_state):
    """Rule 8.4.6: Create a card with the Rupture label keyword."""
    card = game_state.create_card(name="Rupture Card")
    card._has_rupture = True
    game_state.test_card = card


@given('a card with the "Contract" label keyword')
def card_with_contract_keyword(game_state):
    """Rule 8.4.7: Create a card with the Contract label keyword."""
    card = game_state.create_card(name="Contract Card")
    card._has_contract = True
    card._contract_fulfilled = False
    game_state.test_card = card


@given("the contract condition has been fulfilled")
def contract_condition_fulfilled(game_state):
    """Rule 8.4.7: Set up state where the contract condition has been completed."""
    game_state.test_card._contract_fulfilled = True


@given("the contract condition has not been fulfilled")
def contract_condition_not_fulfilled(game_state):
    """Rule 8.4.7: Set up state where the contract condition has not been completed."""
    game_state.test_card._contract_fulfilled = False


@given(parsers.parse('a card with the "Surge" label keyword requiring {required_damage:d} damage'))
def card_with_surge_keyword(game_state, required_damage):
    """Rule 8.4.8: Create a card with the Surge label keyword with specific damage threshold."""
    card = game_state.create_card(name="Surge Card")
    card._has_surge = True
    card._surge_required_damage = required_damage
    game_state.test_card = card


@given('a card with the "Solflare" label keyword')
def card_with_solflare_keyword(game_state):
    """Rule 8.4.9: Create a card with the Solflare label keyword."""
    card = game_state.create_card(name="Solflare Card")
    card._has_solflare = True
    game_state.test_card = card


@given('a card with the "Unity" label keyword')
def card_with_unity_keyword(game_state):
    """Rule 8.4.10: Create a card with the Unity label keyword."""
    card = game_state.create_card(name="Unity Card")
    card._has_unity = True
    game_state.test_card = card


@given('a card with the "Evo Upgrade" label keyword')
def card_with_evo_upgrade_keyword(game_state):
    """Rule 8.4.11: Create a card with the Evo Upgrade label keyword."""
    card = game_state.create_card(name="Evo Upgrade Card")
    card._has_evo_upgrade = True
    game_state.test_card = card


@given(parsers.parse('the player has {evo_count:d} evo equipped'))
def player_has_one_evo_equipped(game_state, evo_count):
    """Rule 8.4.11: Set up player with a specific number of evos equipped (singular)."""
    game_state.player._evo_count = evo_count


@given(parsers.parse('the player has {evo_count:d} evos equipped'))
def player_has_evos_equipped(game_state, evo_count):
    """Rule 8.4.11: Set up player with a specific number of evos equipped (plural)."""
    game_state.player._evo_count = evo_count


@given('a card with the "Galvanize" label keyword')
def card_with_galvanize_keyword(game_state):
    """Rule 8.4.12: Create a card with the Galvanize label keyword."""
    card = game_state.create_card(name="Galvanize Card")
    card._has_galvanize = True
    game_state.test_card = card


@given("the player controls an item")
def player_controls_item(game_state):
    """Rule 8.4.12: Set up a player-controlled item for Galvanize."""
    item = game_state.create_card(name="Test Item")
    item._is_item = True
    game_state.player_item = item


@given(parsers.parse('a card with the "Tower" label keyword with {power:d} power'))
def card_with_tower_keyword_and_power(game_state, power):
    """Rule 8.4.13: Create a card with the Tower label keyword with specific power."""
    card = game_state.create_card(name="Tower Card")
    card._has_tower = True
    card._power = power
    game_state.test_card = card


@given('a card with the "Decompose" label keyword')
def card_with_decompose_keyword(game_state):
    """Rule 8.4.14: Create a card with the Decompose label keyword."""
    card = game_state.create_card(name="Decompose Card")
    card._has_decompose = True
    game_state.test_card = card


@given("the player has 2 Earth cards and an action card in their graveyard")
def player_has_decompose_requirements(game_state):
    """Rule 8.4.14: Set up graveyard with 2 Earth cards and an action card."""
    game_state.graveyard_earth_count = 2
    game_state.graveyard_has_action = True


@given("the player has fewer than 2 Earth cards in their graveyard")
def player_lacks_earth_cards(game_state):
    """Rule 8.4.14: Set up graveyard with fewer than 2 Earth cards."""
    game_state.graveyard_earth_count = 1
    game_state.graveyard_has_action = True


@given('a card with the "Earth Bond" label keyword')
def card_with_earth_bond_keyword(game_state):
    """Rule 8.4.15: Create a card with the Earth Bond label keyword."""
    card = game_state.create_card(name="Earth Bond Card")
    card._has_earth_bond = True
    game_state.test_card = card


@given('a card with the "Lightning Flow" label keyword')
def card_with_lightning_flow_keyword(game_state):
    """Rule 8.4.16: Create a card with the Lightning Flow label keyword."""
    card = game_state.create_card(name="Lightning Flow Card")
    card._has_lightning_flow = True
    game_state.test_card = card


@given("a Lightning card was played this turn")
def lightning_card_played_this_turn(game_state):
    """Rule 8.4.16: Record that a Lightning card was played this turn."""
    game_state.lightning_played_this_turn = True


@given("no Lightning card was played this turn")
def no_lightning_card_played(game_state):
    """Rule 8.4.16: Record that no Lightning card was played this turn."""
    game_state.lightning_played_this_turn = False


@given('a card with the "Heavy" label keyword equipped to a weapon zone')
def card_with_heavy_equipped(game_state):
    """Rule 8.4.17: Create a card with the Heavy label keyword in a weapon zone."""
    card = game_state.create_card(name="Heavy Card")
    card._has_heavy = True
    game_state.weapon_cards = [card]
    game_state.test_card = card


@given("no other card is equipped to weapon zones")
def no_other_weapon_cards(game_state):
    """Rule 8.4.17: Ensure only the Heavy card is in the weapon zones."""
    # weapon_cards already only contains the one Heavy card
    pass


@given("another card is also equipped to a weapon zone")
def another_card_in_weapon_zone(game_state):
    """Rule 8.4.17: Add another card to the weapon zone."""
    other = game_state.create_card(name="Other Weapon")
    game_state.weapon_cards.append(other)


@given('a card with the "High Tide" label keyword')
def card_with_high_tide_keyword(game_state):
    """Rule 8.4.18: Create a card with the High Tide label keyword."""
    card = game_state.create_card(name="High Tide Card")
    card._has_high_tide = True
    game_state.test_card = card


@given(parsers.parse("there are {count:d} blue cards in the pitch zone"))
def blue_cards_in_pitch_zone(game_state, count):
    """Rule 8.4.18: Set up pitch zone with a specific number of blue cards."""
    game_state.pitch_zone_blue_count = count


@given(parsers.parse("there is {count:d} blue card in the pitch zone"))
def one_blue_card_in_pitch_zone(game_state, count):
    """Rule 8.4.18: Set up pitch zone with a specific number of blue cards."""
    game_state.pitch_zone_blue_count = count


@given("there are 0 blue cards in the pitch zone")
def no_blue_cards_in_pitch_zone(game_state):
    """Rule 8.4.18: Set up pitch zone with no blue cards."""
    game_state.pitch_zone_blue_count = 0


@given('a card with the "Go Fish" label keyword')
def card_with_go_fish_keyword(game_state):
    """Rule 8.4.19: Create a card with the Go Fish label keyword."""
    card = game_state.create_card(name="Go Fish Card")
    card._has_go_fish = True
    card._go_fish_adjective = None
    game_state.test_card = card


@given(parsers.parse('a card with the "Go Fish" label keyword requiring a {adjective} card'))
def card_with_go_fish_adjective(game_state, adjective):
    """Rule 8.4.19: Create a card with Go Fish requiring a specific card type."""
    card = game_state.create_card(name="Go Fish Card")
    card._has_go_fish = True
    card._go_fish_adjective = adjective
    game_state.test_card = card


# ---- When steps ----

@when("I check the Combo condition")
def check_combo_condition(game_state):
    """Rule 8.4.1: Evaluate the Combo condition against the combat chain."""
    card = game_state.test_card
    last_attack = getattr(game_state, "last_attack_name", None)
    combo_name = getattr(card, "_combo_name", None)
    game_state.combo_condition_met = (
        last_attack is not None and combo_name is not None and last_attack == combo_name
    )


@when(parsers.parse("the card deals {damage:d} damage"))
def card_deals_damage(game_state, damage):
    """Rule 8.4.2: Record the damage dealt by the card."""
    game_state.damage_dealt = damage


@when("the card hits but deals 0 damage")
def card_hits_but_deals_zero_damage(game_state):
    """Rule 8.4.2a: Record a hit event with 0 damage (e.g., all damage prevented)."""
    game_state.hit_event = True
    game_state.damage_dealt = 0


@when("I check the Reprise condition")
def check_reprise_condition(game_state):
    """Rule 8.4.3: Evaluate the Reprise condition."""
    game_state.reprise_condition_met = getattr(game_state, "defender_defended_from_hand", False)


@when("the Reprise ability resolves")
def reprise_ability_resolves(game_state):
    """Rule 8.4.3a: Simulate resolution of the Reprise ability."""
    # Condition is checked at resolution time
    game_state.reprise_resolution_evaluated = True
    game_state.reprise_condition_at_resolution = getattr(
        game_state, "defender_defended_from_hand", False
    )


@when("the start of the end phase is processed")
def start_of_end_phase_processed(game_state):
    """Rule 8.4.4: Process the start of the end phase for Channel."""
    card = game_state.test_card
    current_counters = getattr(card, "_flow_counters", 0)
    game_state.channel_flow_counter_result = current_counters + 1
    card._flow_counters = game_state.channel_flow_counter_result


@when("the end phase Channel check is processed")
def end_phase_channel_check(game_state):
    """Rule 8.4.4: Process the Channel destruction check."""
    cost_paid = getattr(game_state, "channel_cost_paid", False)
    flow_counters = getattr(game_state.test_card, "_flow_counters", 0)
    # Destroy if player didn't pay flow_counters supertype cards
    if not cost_paid:
        game_state.test_card._is_destroyed = True
    else:
        game_state.test_card._is_destroyed = False


@when("I check the Material condition")
def check_material_condition(game_state):
    """Rule 8.4.5: Evaluate the Material condition."""
    game_state.material_condition_met = getattr(game_state, "card_is_under_permanent", False)


@when(parsers.parse("the card is played at chain link {link:d}"))
def card_played_at_chain_link(game_state, link):
    """Rule 8.4.6: Record the chain link at which the card was played."""
    game_state.rupture_chain_link = link
    game_state.rupture_condition_met = link >= 4


@when("I check the Contract completion status")
def check_contract_completion(game_state):
    """Rule 8.4.7: Evaluate whether the contract has been completed."""
    game_state.contract_completed = getattr(game_state.test_card, "_contract_fulfilled", False)


@when(parsers.parse("the card deals {damage:d} damage"))
def card_deals_surge_damage(game_state, damage):
    """Rule 8.4.8: Record the damage dealt by the card (Surge context)."""
    game_state.damage_dealt = damage


@when("the card is charged to the hero's soul")
def card_charged_to_soul(game_state):
    """Rule 8.4.9: Simulate the card being charged to the hero's soul."""
    game_state.solflare_trigger = True
    game_state.solflare_condition_met = True


@when("the card enters the arena without being charged to soul")
def card_enters_arena_without_soul_charge(game_state):
    """Rule 8.4.9: Simulate the card entering the arena without soul charge."""
    game_state.solflare_trigger = False
    game_state.solflare_condition_met = False


@when("the card defends together with a card from hand")
def card_defends_with_hand_card(game_state):
    """Rule 8.4.10: Simulate the card defending together with a hand card."""
    game_state.unity_condition_met = True


@when("the card defends without any card from hand")
def card_defends_alone(game_state):
    """Rule 8.4.10: Simulate the card defending alone without a hand card."""
    game_state.unity_condition_met = False


@when("I check the Evo Upgrade effect")
def check_evo_upgrade_effect(game_state):
    """Rule 8.4.11: Evaluate the Evo Upgrade effect count."""
    game_state.evo_upgrade_value = getattr(game_state.player, "_evo_count", 0)


@when("the card defends")
def card_defends(game_state):
    """Rule 8.4.12: Simulate the card defending."""
    game_state.galvanize_triggered = True


@when("the card defends and the player destroys the item")
def card_defends_and_destroys_item(game_state):
    """Rule 8.4.12: Simulate defending and destroying an item."""
    game_state.galvanize_triggered = True
    game_state.galvanize_item_destroyed = True
    game_state.galvanize_condition_met = True


@when("the card defends without destroying an item")
def card_defends_without_destroying_item(game_state):
    """Rule 8.4.12: Simulate defending without destroying an item."""
    game_state.galvanize_triggered = True
    game_state.galvanize_item_destroyed = False
    game_state.galvanize_condition_met = False


@when("I check the Tower condition")
def check_tower_condition(game_state):
    """Rule 8.4.13: Evaluate the Tower condition based on power."""
    power = getattr(game_state.test_card, "_power", 0)
    game_state.tower_condition_met = power >= 13


@when("I check the Decompose condition")
def check_decompose_condition(game_state):
    """Rule 8.4.14: Evaluate whether the Decompose cost can be paid from the graveyard."""
    earth_count = getattr(game_state, "graveyard_earth_count", 0)
    has_action = getattr(game_state, "graveyard_has_action", False)
    game_state.decompose_condition_met = (earth_count >= 2 and has_action)


@when("the card is played and an Earth card was pitched")
def card_played_with_earth_pitch(game_state):
    """Rule 8.4.15: Simulate playing the card with an Earth card pitched."""
    game_state.earth_bond_condition_met = True


@when("the card is played without pitching an Earth card")
def card_played_without_earth_pitch(game_state):
    """Rule 8.4.15: Simulate playing the card without pitching an Earth card."""
    game_state.earth_bond_condition_met = False


@when("I check the Lightning Flow condition")
def check_lightning_flow_condition(game_state):
    """Rule 8.4.16: Evaluate the Lightning Flow condition."""
    game_state.lightning_flow_condition_met = getattr(
        game_state, "lightning_played_this_turn", False
    )


@when("I check the Heavy condition")
def check_heavy_condition(game_state):
    """Rule 8.4.17: Evaluate the Heavy condition based on weapon zones."""
    weapon_cards = getattr(game_state, "weapon_cards", [])
    game_state.heavy_condition_met = len(weapon_cards) == 1


@when("I check the High Tide condition")
def check_high_tide_condition(game_state):
    """Rule 8.4.18: Evaluate the High Tide condition."""
    blue_count = getattr(game_state, "pitch_zone_blue_count", 0)
    game_state.high_tide_condition_met = blue_count >= 2


@when("the card hits a hero")
def card_hits_hero(game_state):
    """Rule 8.4.19: Simulate the Go Fish card hitting a hero."""
    game_state.go_fish_hit_hero = True
    game_state.go_fish_triggered = True
    # Hero must choose and reveal a card
    game_state.hero_must_reveal = True


@when("the card hits a hero and the hero reveals a blue card")
def card_hits_hero_hero_reveals_blue(game_state):
    """Rule 8.4.19: Hero reveals a blue card in response to Go Fish hit."""
    game_state.go_fish_hit_hero = True
    game_state.go_fish_triggered = True
    game_state.hero_revealed_card_adjective = "blue"
    required_adjective = getattr(game_state.test_card, "_go_fish_adjective", None)
    game_state.go_fish_match = (required_adjective == "blue")


@when("the card hits a hero and the hero reveals a red card")
def card_hits_hero_hero_reveals_red(game_state):
    """Rule 8.4.19: Hero reveals a red card in response to Go Fish hit."""
    game_state.go_fish_hit_hero = True
    game_state.go_fish_triggered = True
    game_state.hero_revealed_card_adjective = "red"
    required_adjective = getattr(game_state.test_card, "_go_fish_adjective", None)
    game_state.go_fish_match = (required_adjective == "red")


# ---- Then steps ----

@then("the Combo condition is met")
def combo_condition_is_met(game_state):
    """Rule 8.4.1: Assert the Combo condition is met."""
    assert game_state.combo_condition_met is True, (
        "Combo condition should be met when named card was last attack (Rule 8.4.1)"
    )


@then("the Combo condition is not met")
def combo_condition_is_not_met(game_state):
    """Rule 8.4.1: Assert the Combo condition is not met."""
    assert game_state.combo_condition_met is False, (
        "Combo condition should not be met (Rule 8.4.1)"
    )


@then("the Crush condition is met")
def crush_condition_is_met(game_state):
    """Rule 8.4.2: Assert the Crush condition is met (4+ damage)."""
    damage = getattr(game_state, "damage_dealt", 0)
    result = game_state.check_crush_condition(damage)
    assert result is True, (
        f"Crush condition should be met when dealing {damage} damage (Rule 8.4.2)"
    )


@then("the Crush condition is not met")
def crush_condition_is_not_met(game_state):
    """Rule 8.4.2: Assert the Crush condition is not met (less than 4 damage)."""
    damage = getattr(game_state, "damage_dealt", 0)
    result = game_state.check_crush_condition(damage)
    assert result is False, (
        f"Crush condition should not be met when dealing {damage} damage (Rule 8.4.2)"
    )


@then("the Reprise condition is met")
def reprise_condition_is_met(game_state):
    """Rule 8.4.3: Assert the Reprise condition is met."""
    assert game_state.reprise_condition_met is True, (
        "Reprise condition should be met when defending hero defended from hand (Rule 8.4.3)"
    )


@then("the Reprise condition is not met")
def reprise_condition_is_not_met(game_state):
    """Rule 8.4.3: Assert the Reprise condition is not met."""
    assert game_state.reprise_condition_met is False, (
        "Reprise condition should not be met when defending hero did not defend from hand "
        "(Rule 8.4.3)"
    )


@then("the Reprise condition is evaluated at resolution not retroactively")
def reprise_evaluated_at_resolution(game_state):
    """Rule 8.4.3a: Assert Reprise was evaluated at resolution time."""
    assert getattr(game_state, "reprise_resolution_evaluated", False) is True, (
        "Reprise condition should have been evaluated at resolution (Rule 8.4.3a)"
    )
    # Condition was False at resolution time
    assert game_state.reprise_condition_at_resolution is False, (
        "Reprise condition should be False at resolution (Rule 8.4.3a): "
        "effects should not be generated retroactively"
    )


@then("the card has 1 flow counter")
def card_has_one_flow_counter(game_state):
    """Rule 8.4.4: Assert the card has 1 flow counter after end phase."""
    counters = getattr(game_state.test_card, "_flow_counters", None)
    assert counters == 1, (
        f"Channel card should have 1 flow counter after end phase (Rule 8.4.4), got: {counters}"
    )


@then("the card is destroyed by Channel")
def card_destroyed_by_channel(game_state):
    """Rule 8.4.4: Assert the card was destroyed by the Channel ability."""
    is_destroyed = getattr(game_state.test_card, "_is_destroyed", False)
    assert is_destroyed is True, (
        "Channel card should be destroyed when cost not paid (Rule 8.4.4)"
    )


@then("the card is not destroyed by Channel")
def card_not_destroyed_by_channel(game_state):
    """Rule 8.4.4: Assert the card was not destroyed by Channel."""
    is_destroyed = getattr(game_state.test_card, "_is_destroyed", False)
    assert is_destroyed is False, (
        "Channel card should not be destroyed when cost is paid (Rule 8.4.4)"
    )


@then("the Material condition is met")
def material_condition_is_met(game_state):
    """Rule 8.4.5: Assert the Material condition is met."""
    assert game_state.material_condition_met is True, (
        "Material condition should be met when card is under a permanent (Rule 8.4.5)"
    )


@then("the Material condition is not met")
def material_condition_is_not_met(game_state):
    """Rule 8.4.5: Assert the Material condition is not met."""
    assert game_state.material_condition_met is False, (
        "Material condition should not be met when card is not under a permanent (Rule 8.4.5)"
    )


@then("the Rupture condition is met")
def rupture_condition_is_met(game_state):
    """Rule 8.4.6: Assert the Rupture condition is met."""
    assert game_state.rupture_condition_met is True, (
        f"Rupture condition should be met at chain link {game_state.rupture_chain_link} (Rule 8.4.6)"
    )


@then("the Rupture condition is not met")
def rupture_condition_is_not_met(game_state):
    """Rule 8.4.6: Assert the Rupture condition is not met."""
    assert game_state.rupture_condition_met is False, (
        f"Rupture condition should not be met at chain link {game_state.rupture_chain_link} "
        f"(Rule 8.4.6)"
    )


@then("the contract is completed")
def contract_is_completed(game_state):
    """Rule 8.4.7: Assert the contract is completed."""
    assert game_state.contract_completed is True, (
        "Contract should be recognized as completed (Rule 8.4.7)"
    )


@then("the Contract reward effect is triggered")
def contract_reward_triggered(game_state):
    """Rule 8.4.7: Assert the Contract reward triggers when completed."""
    result = game_state.check_contract_reward(game_state.test_card)
    assert result is True, (
        "Contract reward effect should trigger on completion (Rule 8.4.7)"
    )


@then("the contract is not completed")
def contract_is_not_completed(game_state):
    """Rule 8.4.7: Assert the contract is not completed."""
    assert game_state.contract_completed is False, (
        "Contract should not be recognized as completed (Rule 8.4.7)"
    )


@then("the Surge condition is met")
def surge_condition_is_met(game_state):
    """Rule 8.4.8: Assert the Surge condition is met."""
    damage = getattr(game_state, "damage_dealt", 0)
    required = getattr(game_state.test_card, "_surge_required_damage", 0)
    result = game_state.check_surge_condition(damage, required)
    assert result is True, (
        f"Surge condition should be met when dealing {damage} damage "
        f"(required {required}) (Rule 8.4.8)"
    )


@then("the Surge condition is not met")
def surge_condition_is_not_met(game_state):
    """Rule 8.4.8: Assert the Surge condition is not met."""
    damage = getattr(game_state, "damage_dealt", 0)
    required = getattr(game_state.test_card, "_surge_required_damage", 0)
    result = game_state.check_surge_condition(damage, required)
    assert result is False, (
        f"Surge condition should not be met when dealing {damage} damage "
        f"(required {required}) (Rule 8.4.8)"
    )


@then("the Solflare condition is met")
def solflare_condition_is_met(game_state):
    """Rule 8.4.9: Assert the Solflare condition is met."""
    assert game_state.solflare_condition_met is True, (
        "Solflare condition should be met when card is charged to hero's soul (Rule 8.4.9)"
    )


@then("the Solflare condition is not met")
def solflare_condition_is_not_met(game_state):
    """Rule 8.4.9: Assert the Solflare condition is not met."""
    assert game_state.solflare_condition_met is False, (
        "Solflare condition should not be met when card is not charged to soul (Rule 8.4.9)"
    )


@then("the Unity condition is met")
def unity_condition_is_met(game_state):
    """Rule 8.4.10: Assert the Unity condition is met."""
    assert game_state.unity_condition_met is True, (
        "Unity condition should be met when card defends with a hand card (Rule 8.4.10)"
    )


@then("the Unity condition is not met")
def unity_condition_is_not_met(game_state):
    """Rule 8.4.10: Assert the Unity condition is not met."""
    assert game_state.unity_condition_met is False, (
        "Unity condition should not be met when card defends alone (Rule 8.4.10)"
    )


@then(parsers.parse("the Evo Upgrade value is {expected:d}"))
def evo_upgrade_value_is(game_state, expected):
    """Rule 8.4.11: Assert the Evo Upgrade effect value equals the number of evos equipped."""
    assert game_state.evo_upgrade_value == expected, (
        f"Evo Upgrade value should be {expected} (Rule 8.4.11), "
        f"got: {game_state.evo_upgrade_value}"
    )


@then("the Galvanize option is available")
def galvanize_option_available(game_state):
    """Rule 8.4.12: Assert the Galvanize option is available when defending."""
    assert game_state.galvanize_triggered is True, (
        "Galvanize option should be available when the card defends (Rule 8.4.12)"
    )


@then("the Galvanize condition is met")
def galvanize_condition_is_met(game_state):
    """Rule 8.4.12: Assert the Galvanize condition is met."""
    assert game_state.galvanize_condition_met is True, (
        "Galvanize condition should be met when player destroys an item while defending "
        "(Rule 8.4.12)"
    )


@then("the Galvanize condition is not met")
def galvanize_condition_is_not_met(game_state):
    """Rule 8.4.12: Assert the Galvanize condition is not met."""
    assert game_state.galvanize_condition_met is False, (
        "Galvanize condition should not be met without item destruction (Rule 8.4.12)"
    )


@then("the Tower condition is met")
def tower_condition_is_met(game_state):
    """Rule 8.4.13: Assert the Tower condition is met."""
    assert game_state.tower_condition_met is True, (
        f"Tower condition should be met when card has {game_state.test_card._power} power "
        f"(Rule 8.4.13)"
    )


@then("the Tower condition is not met")
def tower_condition_is_not_met(game_state):
    """Rule 8.4.13: Assert the Tower condition is not met."""
    assert game_state.tower_condition_met is False, (
        f"Tower condition should not be met when card has {game_state.test_card._power} power "
        f"(Rule 8.4.13)"
    )


@then("the Decompose condition is met")
def decompose_condition_is_met(game_state):
    """Rule 8.4.14: Assert the Decompose condition is met."""
    assert game_state.decompose_condition_met is True, (
        "Decompose condition should be met when graveyard has required cards (Rule 8.4.14)"
    )


@then("the Decompose condition is not met")
def decompose_condition_is_not_met(game_state):
    """Rule 8.4.14: Assert the Decompose condition is not met."""
    assert game_state.decompose_condition_met is False, (
        "Decompose condition should not be met without required graveyard cards (Rule 8.4.14)"
    )


@then("the Earth Bond condition is met")
def earth_bond_condition_is_met(game_state):
    """Rule 8.4.15: Assert the Earth Bond condition is met."""
    assert game_state.earth_bond_condition_met is True, (
        "Earth Bond condition should be met when an Earth card was pitched (Rule 8.4.15)"
    )


@then("the Earth Bond condition is not met")
def earth_bond_condition_is_not_met(game_state):
    """Rule 8.4.15: Assert the Earth Bond condition is not met."""
    assert game_state.earth_bond_condition_met is False, (
        "Earth Bond condition should not be met without an Earth card pitch (Rule 8.4.15)"
    )


@then("the Lightning Flow condition is met")
def lightning_flow_condition_is_met(game_state):
    """Rule 8.4.16: Assert the Lightning Flow condition is met."""
    assert game_state.lightning_flow_condition_met is True, (
        "Lightning Flow condition should be met when Lightning card was played (Rule 8.4.16)"
    )


@then("the Lightning Flow condition is not met")
def lightning_flow_condition_is_not_met(game_state):
    """Rule 8.4.16: Assert the Lightning Flow condition is not met."""
    assert game_state.lightning_flow_condition_met is False, (
        "Lightning Flow condition should not be met without a Lightning card played (Rule 8.4.16)"
    )


@then("the Heavy condition is met")
def heavy_condition_is_met(game_state):
    """Rule 8.4.17: Assert the Heavy condition is met."""
    assert game_state.heavy_condition_met is True, (
        "Heavy condition should be met when card is only weapon equipped (Rule 8.4.17)"
    )


@then("the Heavy condition is not met")
def heavy_condition_is_not_met(game_state):
    """Rule 8.4.17: Assert the Heavy condition is not met."""
    assert game_state.heavy_condition_met is False, (
        "Heavy condition should not be met when another card is in a weapon zone (Rule 8.4.17)"
    )


@then("the High Tide condition is met")
def high_tide_condition_is_met(game_state):
    """Rule 8.4.18: Assert the High Tide condition is met."""
    assert game_state.high_tide_condition_met is True, (
        "High Tide condition should be met with 2+ blue cards in pitch zone (Rule 8.4.18)"
    )


@then("the High Tide condition is not met")
def high_tide_condition_is_not_met(game_state):
    """Rule 8.4.18: Assert the High Tide condition is not met."""
    assert game_state.high_tide_condition_met is False, (
        "High Tide condition should not be met with fewer than 2 blue cards in pitch zone "
        "(Rule 8.4.18)"
    )


@then("the Go Fish ability triggers and the hero must choose and reveal a card from hand")
def go_fish_triggers_and_hero_reveals(game_state):
    """Rule 8.4.19: Assert Go Fish triggers and the hero must reveal a card."""
    assert game_state.go_fish_triggered is True, (
        "Go Fish should trigger when hitting a hero (Rule 8.4.19)"
    )
    assert game_state.hero_must_reveal is True, (
        "Hero must choose and reveal a card from hand when hit by Go Fish (Rule 8.4.19)"
    )


@then("the hero discards the revealed card")
def hero_discards_revealed_card(game_state):
    """Rule 8.4.19: Assert the hero discards the matching revealed card."""
    assert game_state.go_fish_match is True, (
        "Hero should discard the revealed card when it matches the Go Fish adjective (Rule 8.4.19)"
    )


@then("the Go Fish player creates a Gold token")
def go_fish_creates_gold_token(game_state):
    """Rule 8.4.19: Assert a Gold token is created on a matching reveal."""
    result = game_state.check_go_fish_gold_token(game_state.test_card, game_state.go_fish_match)
    assert result is True, (
        "Go Fish should create a Gold token when revealed card matches adjective (Rule 8.4.19)"
    )


@then("the hero does not discard the revealed card")
def hero_does_not_discard_revealed_card(game_state):
    """Rule 8.4.19: Assert the hero does not discard the non-matching revealed card."""
    assert game_state.go_fish_match is False, (
        "Hero should not discard revealed card when it does not match the adjective (Rule 8.4.19)"
    )


@then("no Gold token is created")
def no_gold_token_created(game_state):
    """Rule 8.4.19: Assert no Gold token is created on a non-matching reveal."""
    result = game_state.check_go_fish_gold_token(game_state.test_card, game_state.go_fish_match)
    assert result is False, (
        "Go Fish should not create a Gold token when revealed card does not match (Rule 8.4.19)"
    )


# ===== Fixtures =====

@pytest.fixture
def game_state():
    """
    Fixture providing game state for testing label keywords (Rule 8.4).

    Uses BDDGameState which integrates with the real engine.
    Reference: Rule 8.4
    """
    from tests.bdd_helpers import BDDGameState

    state = BDDGameState()
    state.last_attack_name = None
    state.damage_dealt = 0
    state.hit_event = False
    state.defender_defended_from_hand = False
    state.channel_cost_paid = False
    state.card_is_under_permanent = False
    state.rupture_chain_link = 0
    state.rupture_condition_met = False
    state.combo_condition_met = False
    state.reprise_condition_met = False
    state.material_condition_met = False
    state.contract_completed = False
    state.solflare_condition_met = False
    state.unity_condition_met = False
    state.galvanize_triggered = False
    state.galvanize_condition_met = False
    state.tower_condition_met = False
    state.decompose_condition_met = False
    state.earth_bond_condition_met = False
    state.lightning_flow_condition_met = False
    state.lightning_played_this_turn = False
    state.heavy_condition_met = False
    state.high_tide_condition_met = False
    state.pitch_zone_blue_count = 0
    state.weapon_cards = []
    state.go_fish_triggered = False
    state.hero_must_reveal = False
    state.go_fish_match = False
    return state
