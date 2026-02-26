"""
Step definitions for Section 1.14: Costs
Reference: Flesh and Blood Comprehensive Rules Section 1.14

This module implements behavioral tests for the cost system in Flesh and Blood.
Costs are the requirements of payment incurred by playing a card, activating an
ability, or resolving/applying an effect. Costs consist of asset-costs (paying
assets) and/or effect-costs (generating effects).

Engine Features Needed for Section 1.14:
- [ ] Cost class hierarchy: AssetCost, EffectCost (Rule 1.14.1)
- [ ] Cost.cost_type attribute ("asset_cost" or "effect_cost") (Rule 1.14.1)
- [ ] AssetCost.pay(player) method subtracting assets and returning success (Rule 1.14.2)
- [ ] AssetCost.can_be_paid(player) check (Rule 1.14.2b)
- [ ] Multi-asset payment order: chi -> resource -> life -> action (Rule 1.14.2a)
- [ ] GameEngine.reverse_illegal_action() when cost cannot be paid (Rule 1.14.2b, 1.10.3)
- [ ] AssetCost.pay_chi_cost(player, amount) (Rule 1.14.2c)
- [ ] AssetCost.pay_resource_cost(player, amount) - chi before resource (Rule 1.14.2d)
- [ ] AssetCost.pay_life_cost(player, amount) (Rule 1.14.2e)
- [ ] AssetCost.pay_action_cost(player, amount) (Rule 1.14.2f)
- [ ] PitchAction.execute(player, card) moving hand -> pitch zone (Rule 1.14.3)
- [ ] CardTemplate.has_pitch property (Rule 1.14.3a)
- [ ] PitchAction.validate(player, card, needed_asset_type) (Rule 1.14.3b)
- [ ] PitchEvent that can trigger and be replaced (Rule 1.14.3c)
- [ ] EffectCost.pay(player) generating and resolving the specified effects (Rule 1.14.4)
- [ ] EffectCost.can_be_paid(player) before payment (Rule 1.14.4b)
- [ ] EffectCost with multiple effects: player declares order (Rule 1.14.4a)
- [ ] EffectCost.replaced_event_still_counts_as_paid = True (Rule 1.14.4c)
- [ ] ZeroCost acknowledgment (Rule 1.14.5)
"""

import pytest
from pytest_bdd import scenario, given, when, then, parsers


# ============================================================
# Scenario: A cost is incurred by playing a card
# Tests Rule 1.14.1 - Playing a card incurs a cost
# ============================================================


@scenario(
    "../features/section_1_14_costs.feature",
    "A cost is incurred by playing a card",
)
def test_cost_incurred_by_playing_card():
    """Rule 1.14.1: Playing a card incurs a cost requiring payment."""
    pass


# ============================================================
# Scenario: A cost is incurred by activating an ability
# Tests Rule 1.14.1 - Activating an ability incurs a cost
# ============================================================


@scenario(
    "../features/section_1_14_costs.feature",
    "A cost is incurred by activating an ability",
)
def test_cost_incurred_by_activating_ability():
    """Rule 1.14.1: Activating an ability incurs a cost requiring payment."""
    pass


# ============================================================
# Scenario: A cost can require both asset-costs and effect-costs
# Tests Rule 1.14.1 - Costs can have both asset and effect components
# ============================================================


@scenario(
    "../features/section_1_14_costs.feature",
    "A cost can require both asset-costs and effect-costs",
)
def test_cost_can_require_both_asset_and_effect_components():
    """Rule 1.14.1: A cost can require asset-costs and/or effect-costs."""
    pass


# ============================================================
# Scenario: Player pays asset-cost with exact assets
# Tests Rule 1.14.2 - Asset-cost paid with exact assets
# ============================================================


@scenario(
    "../features/section_1_14_costs.feature",
    "Player pays asset-cost with exact assets",
)
def test_player_pays_asset_cost_with_exact_assets():
    """Rule 1.14.2: Player can pay asset-cost with the exact amount."""
    pass


# ============================================================
# Scenario: Player pays asset-cost with more than enough assets
# Tests Rule 1.14.2 - Asset-cost paid with excess assets; excess retained
# ============================================================


@scenario(
    "../features/section_1_14_costs.feature",
    "Player pays asset-cost with more than enough assets",
)
def test_player_pays_asset_cost_with_surplus_assets():
    """Rule 1.14.2: Player retains excess assets after paying asset-cost."""
    pass


# ============================================================
# Scenario: Player cannot pay asset-cost with insufficient assets
# Tests Rule 1.14.2b - Insufficient assets blocks cost payment
# ============================================================


@scenario(
    "../features/section_1_14_costs.feature",
    "Player cannot pay asset-cost with insufficient assets",
)
def test_player_cannot_pay_asset_cost_with_insufficient_assets():
    """Rule 1.14.2b: If player lacks enough assets, cost cannot be paid and game state reverses."""
    pass


# ============================================================
# Scenario: Multi-asset cost paid in correct order chi then resource then life then action
# Tests Rule 1.14.2a - Multi-asset payment order
# ============================================================


@scenario(
    "../features/section_1_14_costs.feature",
    "Multi-asset cost paid in correct order chi then resource then life then action",
)
def test_multi_asset_cost_paid_in_correct_order():
    """Rule 1.14.2a: Multi-asset costs paid in order: chi, resource, life, action."""
    pass


# ============================================================
# Scenario: Each asset type must be paid in full before the next
# Tests Rule 1.14.2a - Full payment before next asset type
# ============================================================


@scenario(
    "../features/section_1_14_costs.feature",
    "Each asset type must be paid in full before the next",
)
def test_each_asset_type_paid_in_full_before_next():
    """Rule 1.14.2a: Each asset type must be fully paid before starting the next."""
    pass


# ============================================================
# Scenario: Mandatory asset-cost failure reverses entire action
# Tests Rule 1.14.2b - Mandatory cost failure reverses action
# ============================================================


@scenario(
    "../features/section_1_14_costs.feature",
    "Mandatory asset-cost failure reverses entire action",
)
def test_mandatory_asset_cost_failure_reverses_entire_action():
    """Rule 1.14.2b: Mandatory cost failure reverses the entire action."""
    pass


# ============================================================
# Scenario: Pitching during payment can provide needed assets
# Tests Rule 1.14.2d - Pitching during payment provides resources
# ============================================================


@scenario(
    "../features/section_1_14_costs.feature",
    "Pitching during payment can provide needed assets",
)
def test_pitching_during_payment_provides_needed_assets():
    """Rule 1.14.2d: Player can pitch cards during cost payment to gain resources."""
    pass


# ============================================================
# Scenario: Paying chi cost uses chi points
# Tests Rule 1.14.2c - Chi cost paid using chi points
# ============================================================


@scenario(
    "../features/section_1_14_costs.feature",
    "Paying chi cost uses chi points",
)
def test_paying_chi_cost_uses_chi_points():
    """Rule 1.14.2c: Chi point cost must be paid using chi points."""
    pass


# ============================================================
# Scenario: Player pitches chi card to gain chi for chi cost
# Tests Rule 1.14.2c - Pitching chi card for chi cost
# ============================================================


@scenario(
    "../features/section_1_14_costs.feature",
    "Player pitches chi card to gain chi for chi cost",
)
def test_player_pitches_chi_card_to_gain_chi_for_chi_cost():
    """Rule 1.14.2c: Player can pitch chi cards to gain chi points for chi cost."""
    pass


# ============================================================
# Scenario: Paying resource cost uses chi points first then resource points
# Tests Rule 1.14.2d - Chi before resource in resource payment
# ============================================================


@scenario(
    "../features/section_1_14_costs.feature",
    "Paying resource cost uses chi points first then resource points",
)
def test_paying_resource_cost_uses_chi_first_then_resource():
    """Rule 1.14.2d: Chi points are spent before resource points when paying resource cost."""
    pass


# ============================================================
# Scenario: Player pitches resource card to gain resources for resource cost
# Tests Rule 1.14.2d - Pitching during resource cost payment
# ============================================================


@scenario(
    "../features/section_1_14_costs.feature",
    "Player pitches resource card to gain resources for resource cost",
)
def test_player_pitches_resource_card_during_resource_cost_payment():
    """Rule 1.14.2d: Player can pitch cards during resource cost payment."""
    pass


# ============================================================
# Scenario: Pitching stops when resource cost is fully paid
# Tests Rule 1.14.2d - Pitching stops when cost paid (example from CR)
# ============================================================


@scenario(
    "../features/section_1_14_costs.feature",
    "Pitching stops when resource cost is fully paid",
)
def test_pitching_stops_when_resource_cost_paid():
    """Rule 1.14.2d: Player can no longer pitch when cost is fully paid; excess retained."""
    pass


# ============================================================
# Scenario: Paying life cost uses life points
# Tests Rule 1.14.2e - Life cost paid using life points
# ============================================================


@scenario(
    "../features/section_1_14_costs.feature",
    "Paying life cost uses life points",
)
def test_paying_life_cost_uses_life_points():
    """Rule 1.14.2e: Life point cost must be paid using life points."""
    pass


# ============================================================
# Scenario: Life cost cannot be paid with chi points
# Tests Rule 1.14.2e - Chi cannot substitute for life costs
# ============================================================


@scenario(
    "../features/section_1_14_costs.feature",
    "Life cost cannot be paid with chi points",
)
def test_life_cost_cannot_be_paid_with_chi_points():
    """Rule 1.14.2e: Chi points cannot pay life point costs."""
    pass


# ============================================================
# Scenario: Paying action cost uses action points
# Tests Rule 1.14.2f - Action cost paid using action points
# ============================================================


@scenario(
    "../features/section_1_14_costs.feature",
    "Paying action cost uses action points",
)
def test_paying_action_cost_uses_action_points():
    """Rule 1.14.2f: Action point cost must be paid using action points."""
    pass


# ============================================================
# Scenario: Pitching a card moves it from hand to pitch zone and grants assets
# Tests Rule 1.14.3 - Pitching moves card and grants assets
# ============================================================


@scenario(
    "../features/section_1_14_costs.feature",
    "Pitching a card moves it from hand to pitch zone and grants assets",
)
def test_pitching_card_moves_to_pitch_zone_and_grants_assets():
    """Rule 1.14.3: Pitching moves card from hand to pitch zone and grants assets."""
    pass


# ============================================================
# Scenario: Pitch property determines type and amount of assets gained
# Tests Rule 1.14.3 - Pitch property type and value
# ============================================================


@scenario(
    "../features/section_1_14_costs.feature",
    "Pitch property determines type and amount of assets gained",
)
def test_pitch_property_determines_type_and_amount_of_assets():
    """Rule 1.14.3: Pitch property determines what type and how many assets are gained."""
    pass


# ============================================================
# Scenario: Card without pitch property cannot be pitched
# Tests Rule 1.14.3a - Cards without pitch cannot be pitched
# ============================================================


@scenario(
    "../features/section_1_14_costs.feature",
    "Card without pitch property cannot be pitched",
)
def test_card_without_pitch_property_cannot_be_pitched():
    """Rule 1.14.3a: A card cannot be pitched if it does not have the pitch property."""
    pass


# ============================================================
# Scenario: Card with pitch property can be pitched
# Tests Rule 1.14.3a - Cards with pitch property can be pitched
# ============================================================


@scenario(
    "../features/section_1_14_costs.feature",
    "Card with pitch property can be pitched",
)
def test_card_with_pitch_property_can_be_pitched():
    """Rule 1.14.3a: A card with pitch property can be pitched."""
    pass


# ============================================================
# Scenario: Player can only pitch card if it gains needed asset type
# Tests Rule 1.14.3b - Pitch only for needed asset type
# ============================================================


@scenario(
    "../features/section_1_14_costs.feature",
    "Player can only pitch card if it gains needed asset type",
)
def test_player_can_only_pitch_card_if_gains_needed_asset_type():
    """Rule 1.14.3b: A player may only pitch a card that gains the needed asset type."""
    pass


# ============================================================
# Scenario: Player can pitch card if it gains the needed asset type
# Tests Rule 1.14.3b - Pitch accepted when it gains needed type
# ============================================================


@scenario(
    "../features/section_1_14_costs.feature",
    "Player can pitch card if it gains the needed asset type",
)
def test_player_can_pitch_card_if_gains_needed_asset_type():
    """Rule 1.14.3b: Pitch is accepted when the card gains the needed asset type."""
    pass


# ============================================================
# Scenario: Player can pitch card if instructed by an effect
# Tests Rule 1.14.3b - Effect instruction allows pitching
# ============================================================


@scenario(
    "../features/section_1_14_costs.feature",
    "Player can pitch card if instructed by an effect",
)
def test_player_can_pitch_card_if_instructed_by_effect():
    """Rule 1.14.3b: Player can pitch a card if instructed by an effect."""
    pass


# ============================================================
# Scenario: Pitching a card triggers effects that watch for pitching
# Tests Rule 1.14.3c - Pitching is an event that triggers effects
# ============================================================


@scenario(
    "../features/section_1_14_costs.feature",
    "Pitching a card triggers effects that watch for pitching",
)
def test_pitching_card_triggers_pitch_watchers():
    """Rule 1.14.3c: Pitching a card is an event that can trigger triggered effects."""
    pass


# ============================================================
# Scenario: Pitching a card can be replaced by replacement effects
# Tests Rule 1.14.3c - Pitching event can be replaced
# ============================================================


@scenario(
    "../features/section_1_14_costs.feature",
    "Pitching a card can be replaced by replacement effects",
)
def test_pitching_card_can_be_replaced_by_replacement_effects():
    """Rule 1.14.3c: Pitching a card is an event that can be replaced by effects."""
    pass


# ============================================================
# Scenario: Effect-cost requires successfully generating and resolving an effect
# Tests Rule 1.14.4 - Effect-cost requires generating and resolving effects
# ============================================================


@scenario(
    "../features/section_1_14_costs.feature",
    "Effect-cost requires successfully generating and resolving an effect",
)
def test_effect_cost_requires_generating_and_resolving_effect():
    """Rule 1.14.4: Effect-cost requires payment in the form of generating effects."""
    pass


# ============================================================
# Scenario: Hope Merchants Hood effect-cost example
# Tests Rule 1.14.4 - Hope Merchant's Hood destroy cost example
# ============================================================


@scenario(
    "../features/section_1_14_costs.feature",
    "Hope Merchants Hood effect-cost example",
)
def test_hope_merchants_hood_effect_cost_example():
    """Rule 1.14.4: Hope Merchant's Hood has destroy-self as an effect-cost."""
    pass


# ============================================================
# Scenario: Player declares order for multi-effect-cost
# Tests Rule 1.14.4a - Multi-effect-cost player declares order
# ============================================================


@scenario(
    "../features/section_1_14_costs.feature",
    "Player declares order for multi-effect-cost",
)
def test_player_declares_order_for_multi_effect_cost():
    """Rule 1.14.4a: Player declares order in which multiple effect-costs are generated."""
    pass


# ============================================================
# Scenario: Effect-cost that cannot be generated reverses game state
# Tests Rule 1.14.4b - Unpayable effect-cost reverses game state
# ============================================================


@scenario(
    "../features/section_1_14_costs.feature",
    "Effect-cost that cannot be generated reverses game state",
)
def test_effect_cost_that_cannot_be_generated_reverses_game_state():
    """Rule 1.14.4b: If effect-cost cannot be generated, game state is reversed."""
    pass


# ============================================================
# Scenario: Mandatory effect-cost failure reverses entire action
# Tests Rule 1.14.4b - Mandatory effect-cost failure reverses action
# ============================================================


@scenario(
    "../features/section_1_14_costs.feature",
    "Mandatory effect-cost failure reverses entire action",
)
def test_mandatory_effect_cost_failure_reverses_entire_action():
    """Rule 1.14.4b: Mandatory effect-cost failure reverses the entire action."""
    pass


# ============================================================
# Scenario: Effect-cost replaced but considered paid
# Tests Rule 1.14.4c - Replaced effect-costs still count as paid
# ============================================================


@scenario(
    "../features/section_1_14_costs.feature",
    "Effect-cost replaced but considered paid",
)
def test_effect_cost_replaced_but_considered_paid():
    """Rule 1.14.4c: Effect-cost is still paid if its events are replaced."""
    pass


# ============================================================
# Scenario: Card with cost zero still has a cost to pay
# Tests Rule 1.14.5 - Zero cost is still a cost
# ============================================================


@scenario(
    "../features/section_1_14_costs.feature",
    "Card with cost zero still has a cost to pay",
)
def test_card_with_cost_zero_still_has_cost_to_pay():
    """Rule 1.14.5: A cost of 0 is still a cost paid by acknowledging it."""
    pass


# ============================================================
# Scenario: Asset-costs reduced to zero still require acknowledgment
# Tests Rule 1.14.5 - Reduced-to-zero cost still requires acknowledgment
# ============================================================


@scenario(
    "../features/section_1_14_costs.feature",
    "Asset-costs reduced to zero still require acknowledgment",
)
def test_asset_costs_reduced_to_zero_still_require_acknowledgment():
    """Rule 1.14.5: Cost reduced to zero still requires acknowledgment as paid."""
    pass


# ============================================================
# Scenario: Zero cost with no effect-costs is still a cost
# Tests Rule 1.14.5 - Zero-cost card has a cost (the zero cost)
# ============================================================


@scenario(
    "../features/section_1_14_costs.feature",
    "Zero cost with no effect-costs is still a cost",
)
def test_zero_cost_with_no_effect_costs_is_still_a_cost():
    """Rule 1.14.5: Zero cost with no effect-costs is acknowledged and paid."""
    pass


# ============================================================
# Step Definitions
# ============================================================


# ----- Given steps -----


@given("a player has a card with cost 2")
def player_has_card_with_cost_2(game_state):
    """Rule 1.14.1: Set up a card with an asset-cost of 2 resource points."""
    game_state.test_card = game_state.create_card_with_resource_cost(
        name="Action Card", cost=2
    )
    game_state.player.hand.add_card(game_state.test_card)


@given("the player has 2 resource points")
def player_has_2_resource_points(game_state):
    """Rule 1.14.2: Player has 2 resource points available."""
    game_state.set_player_resource_points(game_state.player, 2)


@given("a player has a card with an activated ability costing 1 resource point")
def player_has_card_with_ability_costing_1_resource(game_state):
    """Rule 1.14.1: Set up a card with an activated ability costing 1 resource."""
    game_state.test_card = game_state.create_card_with_resource_cost(
        name="Ability Card", cost=1
    )
    game_state.ability_card = game_state.test_card
    game_state.player.arena.add_card(game_state.test_card)


@given("the player has 1 resource point")
def player_has_1_resource_point(game_state):
    """Rule 1.14.2: Player has 1 resource point available."""
    game_state.set_player_resource_points(game_state.player, 1)


@given("a player has a card with cost 1 and a discard effect-cost")
def player_has_card_with_cost_1_and_discard_effect_cost(game_state):
    """Rule 1.14.1: Card with both an asset-cost (1 resource) and effect-cost (discard)."""
    game_state.test_card = game_state.create_card_with_resource_cost(
        name="Combo Card", cost=1
    )
    game_state.test_card._has_discard_effect_cost = True  # type: ignore[attr-defined]
    game_state.player.hand.add_card(game_state.test_card)


@given("the player has 1 resource point and 1 card in hand")
def player_has_1_resource_and_1_card(game_state):
    """Setup for combo cost test."""
    game_state.set_player_resource_points(game_state.player, 1)
    discard_card = game_state.create_card(name="Discard Fodder")
    game_state.player.hand.add_card(discard_card)
    game_state.discard_fodder = discard_card


@given("a player has an action card with cost 3")
def player_has_card_with_cost_3(game_state):
    """Rule 1.14.2: Card with asset-cost of 3 resource points."""
    game_state.test_card = game_state.create_card_with_resource_cost(
        name="Costly Card", cost=3
    )
    game_state.player.hand.add_card(game_state.test_card)


@given("the player has 3 resource points")
def player_has_3_resource_points(game_state):
    """Rule 1.14.2: Player has 3 resource points available."""
    game_state.set_player_resource_points(game_state.player, 3)


@given("a player has an action card with cost 2")
def player_has_card_with_cost_2_action(game_state):
    """Rule 1.14.2: Card with asset-cost of 2 resource points."""
    game_state.test_card = game_state.create_card_with_resource_cost(
        name="Action Card", cost=2
    )
    game_state.player.hand.add_card(game_state.test_card)


@given("the player has 4 resource points")
def player_has_4_resource_points(game_state):
    """Rule 1.14.2: Player has 4 resource points (surplus over cost 2)."""
    game_state.set_player_resource_points(game_state.player, 4)


@given("a player has an ability with cost 1 chi and 1 resource and 1 life and 1 action")
def player_has_multi_asset_ability(game_state):
    """Rule 1.14.2a: Ability with all four asset types in its cost."""
    game_state.multi_asset_ability = game_state.create_multi_asset_ability(
        chi=1, resource=1, life=1, action=1
    )


@given(
    "the player has 1 chi point, 1 resource point, 3 life points, and 1 action point"
)
def player_has_all_asset_types(game_state):
    """Rule 1.14.2a: Player has all four asset types needed for multi-asset cost."""
    game_state.set_player_chi_points(game_state.player, 1)
    game_state.set_player_resource_points(game_state.player, 1)
    game_state.set_hero_life_total(game_state.player, 3)
    game_state.set_player_action_points(game_state.player, 1)


@given("a player has an ability with cost 2 chi and 2 resource points")
def player_has_ability_with_chi_and_resource_cost(game_state):
    """Rule 1.14.2a: Ability requiring 2 chi and 2 resource points."""
    game_state.chi_resource_ability = game_state.create_multi_asset_ability(
        chi=2, resource=2
    )


@given("the player has 1 chi point and 3 resource points")
def player_has_1_chi_3_resource(game_state):
    """Setup: insufficient chi to pay the 2 chi cost (only 1 chi)."""
    game_state.set_player_chi_points(game_state.player, 1)
    game_state.set_player_resource_points(game_state.player, 3)


@given("a player has an action card with mandatory cost 3")
def player_has_action_card_mandatory_cost_3(game_state):
    """Rule 1.14.2b: Card with mandatory resource cost of 3."""
    game_state.test_card = game_state.create_card_with_resource_cost(
        name="Big Card", cost=3
    )
    game_state.test_card._is_mandatory_cost = True  # type: ignore[attr-defined]
    game_state.player.hand.add_card(game_state.test_card)
    game_state.card_starting_zone = "hand"


@given("the player has only 1 resource point")
def player_has_only_1_resource_point(game_state):
    """Rule 1.14.2b: Player only has 1 resource point (insufficient for cost 3)."""
    game_state.set_player_resource_points(game_state.player, 1)


@given("the player has a 2-pitch card in hand")
@given("a player has a 2-pitch card in hand")
def player_has_2_pitch_card_in_hand(game_state):
    """Rule 1.14.3: A card with pitch value 2 in hand."""
    game_state.pitch_card = game_state.create_card_with_pitch(
        name="Pitch Card", pitch_value=2
    )
    game_state.player.hand.add_card(game_state.pitch_card)


@given("a player has an ability with a cost of 2 chi points")
def player_has_ability_with_chi_cost_2(game_state):
    """Rule 1.14.2c: Ability with chi cost of 2."""
    game_state.chi_ability = game_state.create_ability_with_chi_cost(chi_cost=2)


@given("the player has 3 chi points")
def player_has_3_chi_points(game_state):
    """Rule 1.14.2c: Player has 3 chi points available."""
    game_state.set_player_chi_points(game_state.player, 3)


@given("the player has 0 chi points")
def player_has_0_chi_points(game_state):
    """Rule 1.14.2c: Player has no chi points, must pitch for chi."""
    game_state.set_player_chi_points(game_state.player, 0)


@given("the player has a chi-pitch card in hand with chi pitch value 2")
def player_has_chi_pitch_card_in_hand(game_state):
    """Rule 1.14.2c: Chi-pitch card that provides chi points when pitched."""
    game_state.chi_pitch_card = game_state.create_chi_pitch_card(
        name="Chi Card", chi_value=2
    )
    game_state.player.hand.add_card(game_state.chi_pitch_card)


@given("the player has 1 chi point and 2 resource points")
def player_has_1_chi_2_resource(game_state):
    """Rule 1.14.2d: Player has 1 chi + 2 resource (chi spent before resource)."""
    game_state.set_player_chi_points(game_state.player, 1)
    game_state.set_player_resource_points(game_state.player, 2)


@given("a player has an ability with a cost of 2 life points")
def player_has_ability_with_life_cost_2(game_state):
    """Rule 1.14.2e: Ability with life cost of 2."""
    game_state.life_ability = game_state.create_ability_with_life_cost(
        cost=2, ability_text="Pay 2 life: test ability"
    )


@given("the player hero has 20 life points")
def player_hero_has_20_life(game_state):
    """Rule 1.14.2e: Hero has 20 life points."""
    game_state.set_hero_life_total(game_state.player, 20)


@given("a player has an ability with a cost of 1 life point")
def player_has_ability_with_1_life_cost(game_state):
    """Rule 1.14.2e: Ability with 1 life point cost."""
    game_state.life_ability_1 = game_state.create_ability_with_life_cost(
        cost=1, ability_text="Pay 1 life: test ability"
    )


@given("the player has 3 chi points and 1 life point")
def player_has_3_chi_1_life(game_state):
    """Rule 1.14.2e: Player has chi but life is needed for life cost."""
    game_state.set_player_chi_points(game_state.player, 3)
    game_state.set_hero_life_total(game_state.player, 1)


@given("a player has an ability with a cost of 1 action point")
def player_has_ability_with_action_cost(game_state):
    """Rule 1.14.2f: Ability with action point cost of 1."""
    game_state.action_ability = game_state.create_ability_with_action_cost(
        action_cost=1
    )


@given("the player has 1 action point")
def player_has_1_action_point(game_state):
    """Rule 1.14.2f: Player has 1 action point available."""
    game_state.set_player_action_points(game_state.player, 1)


@given("the player has a 3-pitch resource card in hand")
def player_has_3_pitch_resource_card_in_hand(game_state):
    """Rule 1.14.2d/3: A card with pitch value 3 that provides resource points."""
    game_state.large_pitch_card = game_state.create_card_with_pitch(
        name="Large Pitch Card", pitch_value=3
    )
    game_state.large_pitch_card._pitch_generates = "resource"  # type: ignore[attr-defined]
    game_state.player.hand.add_card(game_state.large_pitch_card)


@given("a player has a 3-chi-pitch card in hand")
def player_has_3_chi_pitch_card_in_hand(game_state):
    """Rule 1.14.3: Card with chi pitch value of 3."""
    game_state.chi_3_pitch_card = game_state.create_chi_pitch_card(
        name="Chi Pitch 3", chi_value=3
    )
    game_state.player.hand.add_card(game_state.chi_3_pitch_card)


@given("a player has a card with no pitch property in hand")
@given("a player has a card in hand with no pitch property")
def player_has_card_without_pitch_in_hand(game_state):
    """Rule 1.14.3a: Card without pitch property (cannot be pitched)."""
    game_state.no_pitch_card = game_state.create_card(name="No Pitch Card")
    game_state.no_pitch_card._has_pitch_property = False  # type: ignore[attr-defined]
    game_state.player.hand.add_card(game_state.no_pitch_card)


@given("a player has a card with pitch value 1 in hand")
def player_has_card_with_pitch_1_in_hand(game_state):
    """Rule 1.14.3a: Card with pitch value 1."""
    game_state.pitch_1_card = game_state.create_card_with_pitch(
        name="Pitch One", pitch_value=1
    )
    game_state.player.hand.add_card(game_state.pitch_1_card)


@given("a player is paying a chi point cost of 2")
def player_is_paying_chi_cost_2(game_state):
    """Rule 1.14.3b: Player is in the middle of paying a chi cost of 2."""
    game_state.current_cost_type = "chi_point"
    game_state.current_cost_amount = 2


@given("the player has a resource-pitch card in hand")
def player_has_resource_pitch_card_in_hand(game_state):
    """Rule 1.14.3b: Resource-pitch card (grants resource points, not chi)."""
    game_state.resource_pitch_card = game_state.create_card_with_pitch(
        name="Resource Pitch Card", pitch_value=2
    )
    game_state.resource_pitch_card._pitch_generates = "resource"  # type: ignore[attr-defined]
    game_state.player.hand.add_card(game_state.resource_pitch_card)


@given("there is an effect instructing the player to pitch a card")
def there_is_pitch_instruction_effect(game_state):
    """Rule 1.14.3b: An effect instructs the player to pitch a card."""
    game_state.has_pitch_instruction_effect = True
    game_state.pitch_instruction_effect = game_state.create_pitch_instruction_effect()


@given("there is an effect that triggers when a card is pitched")
def there_is_pitch_trigger_effect(game_state):
    """Rule 1.14.3c: A triggered effect that fires when any card is pitched."""
    game_state.pitch_trigger = game_state.create_pitch_trigger_effect()
    game_state.pitch_trigger_count = 0


@given("there is a replacement effect that modifies the pitch event")
def there_is_pitch_replacement_effect(game_state):
    """Rule 1.14.3c: A replacement effect that modifies the pitch event."""
    game_state.pitch_replacement = game_state.create_pitch_replacement_effect()
    game_state.pitch_was_replaced = False


@given("a player has an ability with the effect-cost of destroying a card")
def player_has_ability_with_destroy_effect_cost(game_state):
    """Rule 1.14.4: Ability with an effect-cost of destroying a target."""
    game_state.destroy_cost_ability = game_state.create_ability_with_effect_cost(
        effect="destroy_target"
    )


@given("the player has a card that can be destroyed")
def player_has_destroyable_card(game_state):
    """Rule 1.14.4: The player has a target for the destroy effect-cost."""
    game_state.destroyable_card = game_state.create_card(name="Destroyable Card")
    game_state.player.arena.add_card(game_state.destroyable_card)


@given("a player controls Hope Merchants Hood")
def player_controls_hope_merchants_hood(game_state):
    """Rule 1.14.4: Hope Merchant's Hood is a famous example of an effect-cost."""
    game_state.hope_merchants_hood = game_state.create_card(name="Hope Merchant's Hood")
    game_state.hope_merchants_hood._has_destroy_self_effect_cost = True  # type: ignore[attr-defined]
    game_state.hope_merchants_hood._has_shuffle_draw_ability = True  # type: ignore[attr-defined]
    game_state.player.arena.add_card(game_state.hope_merchants_hood)


@given("the player has 3 cards in hand")
def player_has_3_cards_in_hand(game_state):
    """Setup: 3 cards in hand to shuffle back into deck."""
    for i in range(3):
        card = game_state.create_card(name=f"Hand Card {i}")
        game_state.player.hand.add_card(card)


@given("a player has an ability with two effect-costs discard and deal damage")
def player_has_ability_with_two_effect_costs(game_state):
    """Rule 1.14.4a: Ability with two effect-costs (discard + deal damage)."""
    game_state.two_cost_ability = game_state.create_ability_with_two_effect_costs(
        cost1="discard_a_card",
        cost2="deal_1_damage_to_self",
    )


@given("the player has a card in hand and a valid target")
def player_has_card_and_target(game_state):
    """Setup: Player has a card to discard and a target to deal damage to."""
    discard_card = game_state.create_card(name="Discard Card")
    game_state.player.hand.add_card(discard_card)
    game_state.discard_card_ref = discard_card
    target = game_state.create_card(name="Target Card")
    game_state.player.arena.add_card(target)
    game_state.damage_target = target


@given("a player has an ability with an effect-cost of destroying their weapon")
def player_has_ability_with_destroy_weapon_effect_cost(game_state):
    """Rule 1.14.4b: Ability with destroy-weapon effect-cost."""
    game_state.weapon_destroy_ability = game_state.create_ability_with_effect_cost(
        effect="destroy_weapon"
    )


@given("the player has no weapon in play")
def player_has_no_weapon_in_play(game_state):
    """Rule 1.14.4b: Player has no weapon, so destroy-weapon cannot be generated."""
    game_state.player_weapon = None


@given("a player has a card with a mandatory effect-cost of discarding a card")
def player_has_card_with_mandatory_discard_effect_cost(game_state):
    """Rule 1.14.4b: Card with mandatory effect-cost of discarding."""
    game_state.test_card = game_state.create_card(name="Discard Cost Card")
    game_state.test_card._has_mandatory_discard_effect_cost = True  # type: ignore[attr-defined]
    game_state.player.hand.add_card(game_state.test_card)
    game_state.card_starting_zone = "hand"


@given("the player has no cards in hand to discard")
def player_has_no_cards_to_discard(game_state):
    """Rule 1.14.4b: Empty hand means discard effect-cost cannot be paid."""
    # Clear all hand cards except the test_card already added
    for card in list(game_state.player.hand.cards):
        if card is not game_state.test_card:
            game_state.player.hand.remove_card(card)


@given("a player has an ability with an effect-cost of discarding a card")
def player_has_ability_with_discard_effect_cost(game_state):
    """Rule 1.14.4c: Ability with discard effect-cost."""
    game_state.discard_cost_ability = game_state.create_ability_with_effect_cost(
        effect="discard_a_card"
    )


@given("there is a replacement effect that replaces the discard with banishment")
def there_is_discard_to_banish_replacement(game_state):
    """Rule 1.14.4c: Replacement effect changes discard to banishment."""
    game_state.discard_to_banish_replacement = game_state.create_replacement_effect(
        replaces="discard",
        with_effect="banish",
    )


@given("a player has a card with cost 0")
def player_has_card_with_cost_0(game_state):
    """Rule 1.14.5: Card with cost 0."""
    game_state.test_card = game_state.create_card_with_resource_cost(
        name="Zero Cost Card", cost=0
    )
    game_state.player.hand.add_card(game_state.test_card)


@given("a player has a card with cost 3")
def player_has_card_with_cost_3_for_reduction(game_state):
    """Rule 1.14.5: Card with cost 3 that will be reduced."""
    game_state.test_card = game_state.create_card_with_resource_cost(
        name="Three Cost Card", cost=3
    )
    game_state.player.hand.add_card(game_state.test_card)


@given("an effect reduces the cost by 3")
def effect_reduces_cost_by_3(game_state):
    """Rule 1.14.5: Effect that reduces card cost by 3."""
    game_state.cost_reduction_effect = game_state.create_cost_reduction_effect(
        reduction=3
    )


@given("a player has a card with cost 0 and no effect-costs")
def player_has_card_with_cost_0_and_no_effect_costs(game_state):
    """Rule 1.14.5: Card with cost 0 and no effect-costs - pure zero cost."""
    game_state.test_card = game_state.create_card_with_resource_cost(
        name="Pure Zero Card", cost=0
    )
    game_state.test_card._has_effect_costs = False  # type: ignore[attr-defined]
    game_state.player.hand.add_card(game_state.test_card)


# ----- When steps -----


@when("the player plays the card")
def player_plays_the_card(game_state):
    """Rule 1.14.1: Player plays a card, incurring the card's cost."""
    game_state.play_result = game_state.attempt_card_play_1_14(game_state.test_card)


@when("the player activates the ability")
def player_activates_the_ability(game_state):
    """Rule 1.14.1: Player activates an ability, incurring its cost."""
    game_state.activation_result = game_state.attempt_ability_activation_1_14(
        game_state.test_card
    )


@when("checking the full cost of the card")
def checking_full_cost_of_card(game_state):
    """Rule 1.14.1: Query all cost components of the card."""
    game_state.full_cost = game_state.get_full_cost_1_14(game_state.test_card)


@when("the player pays the asset-cost")
def player_pays_the_asset_cost(game_state):
    """Rule 1.14.2: Player pays the asset-cost of the card."""
    game_state.pay_result = game_state.pay_asset_cost_1_14(
        player=game_state.player, card=game_state.test_card
    )


@when("the player attempts to pay the asset-cost")
def player_attempts_to_pay_asset_cost(game_state):
    """Rule 1.14.2b: Player attempts to pay an asset-cost (may fail)."""
    game_state.pay_result = game_state.attempt_pay_asset_cost_1_14(
        player=game_state.player, card=game_state.test_card
    )


@when("the player pays the multi-asset cost")
def player_pays_multi_asset_cost(game_state):
    """Rule 1.14.2a: Player pays a cost with multiple asset types."""
    game_state.multi_pay_result = game_state.pay_multi_asset_cost_1_14(
        player=game_state.player, ability=game_state.multi_asset_ability
    )


@when("the player attempts to pay 2 chi then 2 resource")
def player_attempts_chi_then_resource(game_state):
    """Rule 1.14.2a: Player tries to pay 2 chi first then 2 resource."""
    game_state.multi_pay_result = game_state.attempt_pay_multi_asset_cost_1_14(
        player=game_state.player, ability=game_state.chi_resource_ability
    )


@when("the player attempts to play the card")
def player_attempts_to_play_card(game_state):
    """Rule 1.14.2b: Player attempts to play a card (may fail due to cost)."""
    game_state.play_result = game_state.attempt_card_play_1_14(game_state.test_card)


@when("the player pitches the 2-pitch card during cost payment")
def player_pitches_2_pitch_card_during_payment(game_state):
    """Rule 1.14.2d: Player pitches a 2-pitch card during cost payment."""
    game_state.pitch_result = game_state.pitch_card_during_payment_1_14(
        player=game_state.player, card=game_state.pitch_card
    )
    game_state.pay_result = game_state.pay_asset_cost_1_14(
        player=game_state.player, card=game_state.test_card
    )


@when("the player pays the chi point cost")
def player_pays_chi_cost(game_state):
    """Rule 1.14.2c: Player pays the chi point cost of the ability."""
    game_state.chi_pay_result = game_state.pay_chi_cost_1_14(
        player=game_state.player, cost=2
    )


@when("the player pitches the chi card to pay the chi cost")
def player_pitches_chi_card(game_state):
    """Rule 1.14.2c: Player pitches a chi card to gain chi for the chi cost."""
    game_state.pitch_result = game_state.pitch_card_for_chi(
        game_state.player, game_state.chi_pitch_card
    )
    game_state.chi_pay_result = game_state.pay_chi_cost_1_14(
        player=game_state.player, cost=2
    )


@when("the player pays the resource cost")
def player_pays_resource_cost(game_state):
    """Rule 1.14.2d: Player pays the resource cost using chi first then resource."""
    game_state.resource_pay_result = game_state.pay_resource_cost_tracked_1_14(
        player=game_state.player, cost=2
    )


@when("the player pitches the 2-pitch card during resource cost payment")
def player_pitches_2_pitch_card_for_resource(game_state):
    """Rule 1.14.2d: Player pitches a card to gain resources during resource cost payment."""
    game_state.pitch_result = game_state.pitch_card_for_resources(
        game_state.player, game_state.pitch_card
    )
    game_state.pay_result = game_state.pay_asset_cost_1_14(
        player=game_state.player, card=game_state.test_card
    )


@when("the player pitches the 3-pitch card to pay the 2 resource cost")
def player_pitches_3_pitch_card_for_2_resource_cost(game_state):
    """Rule 1.14.2d: Pitching 3-pitch card for cost of 2; excess retained."""
    game_state.pitch_result = game_state.pitch_card_for_resources(
        game_state.player, game_state.large_pitch_card
    )
    game_state.pay_result = game_state.pay_asset_cost_1_14(
        player=game_state.player, card=game_state.test_card
    )
    game_state.further_pitch_result = game_state.attempt_pitch_another_card_1_14(
        player=game_state.player
    )


@when("the player pays the life point cost")
def player_pays_life_cost(game_state):
    """Rule 1.14.2e: Player pays the life point cost of the ability."""
    game_state.life_pay_result = game_state.pay_life_cost_1_14(
        player=game_state.player, amount=2
    )


@when("the player attempts to pay 1 life using chi points")
def player_attempts_chi_for_life(game_state):
    """Rule 1.14.2e: Player attempts to use chi points to pay a life cost (should fail)."""
    game_state.invalid_pay_result = game_state.attempt_chi_for_life_payment(
        game_state.player, 1
    )


@when("the player pays the action point cost")
def player_pays_action_cost(game_state):
    """Rule 1.14.2f: Player pays the action point cost of the ability."""
    game_state.action_pay_result = game_state.pay_action_cost_1_14(
        player=game_state.player, amount=1
    )


@when("the player pitches the card during cost payment")
def player_pitches_card_during_payment_generic(game_state):
    """Rule 1.14.3: Player pitches a card to gain assets during cost payment."""
    if (
        hasattr(game_state, "chi_3_pitch_card")
        and game_state.chi_3_pitch_card is not None
    ):
        card = game_state.chi_3_pitch_card
        game_state.pitch_result = game_state.pitch_card_for_chi(game_state.player, card)
    else:
        card = game_state.pitch_card
        game_state.pitch_result = game_state.pitch_card_for_resources(
            game_state.player, card
        )


@when("the player attempts to pitch that card")
def player_attempts_to_pitch_no_pitch_card(game_state):
    """Rule 1.14.3a: Attempt to pitch a card without the pitch property."""
    game_state.pitch_attempt_result = game_state.attempt_pitch_card_1_14(
        player=game_state.player, card=game_state.no_pitch_card
    )


@when("the player pitches that card during cost payment")
def player_pitches_pitch_card_1(game_state):
    """Rule 1.14.3a: Player pitches a card with pitch property."""
    game_state.pitch_attempt_result = game_state.attempt_pitch_card_1_14(
        player=game_state.player, card=game_state.pitch_1_card
    )


@when("the player attempts to pitch the resource card for chi cost")
def player_attempts_to_pitch_resource_card_for_chi(game_state):
    """Rule 1.14.3b: Attempt to pitch resource card when chi is needed."""
    game_state.invalid_pitch_result = game_state.attempt_pitch_for_wrong_type(
        player=game_state.player,
        card=game_state.resource_pitch_card,
        needed_asset="chi_point",
    )


@when("the player pitches the chi card for chi cost")
def player_pitches_chi_card_for_chi_cost(game_state):
    """Rule 1.14.3b: Player pitches chi card when chi is the needed type."""
    game_state.valid_pitch_result = game_state.pitch_card_for_chi(
        game_state.player, game_state.chi_pitch_card
    )


@when("the player pitches the card as instructed by the effect")
def player_pitches_card_as_instructed(game_state):
    """Rule 1.14.3b: Player pitches card as instructed by an effect."""
    game_state.effect_pitch_result = game_state.pitch_card_via_effect_instruction_1_14(
        player=game_state.player,
        card=game_state.no_pitch_card,
        effect=game_state.pitch_instruction_effect,
    )


@when(
    "the player pitches the card during cost payment",
    target_fixture="_pitch_trigger_result",
)
def player_pitches_card_for_trigger_check(game_state):
    """Rule 1.14.3c: Player pitches card, triggering any pitch watchers."""
    game_state.pitch_result = game_state.pitch_card_with_trigger_check_1_14(
        player=game_state.player,
        card=game_state.pitch_card,
        trigger=game_state.pitch_trigger,
    )
    game_state.pitch_trigger_count = game_state.count_pitch_triggers_fired_1_14(
        game_state.pitch_trigger
    )
    return game_state.pitch_result


@when(
    "the player pitches the card during cost payment",
    target_fixture="_pitch_replacement_result",
)
def player_pitches_card_for_replacement(game_state):
    """Rule 1.14.3c: Player pitches card; replacement effect modifies the event.
    Also handles generic 'pitch during payment' when no replacement effect is set."""
    # Determine which card to pitch (pitch_card for most scenarios, fall back to chi_3_pitch_card)
    card = (
        game_state.pitch_card
        if game_state.pitch_card is not None
        else game_state.chi_3_pitch_card
    )

    # Handle replacement effect scenario
    if game_state.pitch_replacement is not None:
        game_state.pitch_result = game_state.pitch_card_with_replacement_check_1_14(
            player=game_state.player,
            card=card,
            replacement=game_state.pitch_replacement,
        )
        game_state.pitch_was_replaced = getattr(
            game_state.pitch_replacement, "was_applied", False
        )
        return game_state.pitch_result

    # Handle trigger scenario (pitch_trigger set but no replacement)
    if game_state.pitch_trigger is not None:
        game_state.pitch_result = game_state.pitch_card_with_trigger_check_1_14(
            player=game_state.player,
            card=card,
            trigger=game_state.pitch_trigger,
        )
        game_state.pitch_trigger_count = game_state.count_pitch_triggers_fired_1_14(
            game_state.pitch_trigger
        )
        return game_state.pitch_result

    # Generic pitch: no replacement, no trigger
    if game_state.chi_3_pitch_card is not None and card is game_state.chi_3_pitch_card:
        game_state.pitch_result = game_state.pitch_card_for_chi(game_state.player, card)
    else:
        game_state.pitch_result = game_state.pitch_card_for_resources(
            game_state.player, card
        )
    game_state.pitch_was_replaced = False
    return game_state.pitch_result

    game_state.pitch_result = game_state.pitch_card_with_replacement_check_1_14(
        player=game_state.player,
        card=card,
        replacement=game_state.pitch_replacement,
    )
    game_state.pitch_was_replaced = getattr(
        game_state.pitch_replacement, "was_applied", False
    )
    return game_state.pitch_result


@when("the player pays the effect-cost")
def player_pays_effect_cost(game_state):
    """Rule 1.14.4: Player pays the effect-cost (generates the specified effect)."""
    # Use whichever ability was set in the Given steps
    ability = (
        game_state.discard_cost_ability
        if game_state.discard_cost_ability is not None
        else game_state.destroy_cost_ability
    )
    target = (
        game_state.destroyable_card if game_state.discard_cost_ability is None else None
    )
    # Check if a replacement effect is active for this payment
    replacement = game_state.discard_to_banish_replacement
    game_state.effect_cost_result = game_state.pay_effect_cost_1_14(
        player=game_state.player,
        ability=ability,
        target=target,
        replacement=replacement,
    )


@when("the player activates the ability to destroy Hope Merchants Hood")
def player_activates_hope_merchants_hood(game_state):
    """Rule 1.14.4: Player activates the Hood ability (destroy self effect-cost)."""
    game_state.hood_activation_result = (
        game_state.activate_ability_with_effect_cost_1_14(
            player=game_state.player,
            source=game_state.hope_merchants_hood,
        )
    )


@when("the player pays the multi-effect-cost")
def player_pays_multi_effect_cost(game_state):
    """Rule 1.14.4a: Player pays a cost with two effect components."""
    game_state.multi_effect_cost_result = game_state.pay_multi_effect_cost_1_14(
        player=game_state.player,
        ability=game_state.two_cost_ability,
        effect1_target=game_state.discard_card_ref,
        effect2_target=None,
    )


@when("the player attempts to pay the effect-cost")
def player_attempts_to_pay_effect_cost(game_state):
    """Rule 1.14.4b: Player attempts to pay effect-cost (may fail)."""
    game_state.effect_cost_result = game_state.attempt_pay_effect_cost_1_14(
        player=game_state.player,
        ability=game_state.weapon_destroy_ability,
        target=None,
    )


@when("the player plays the card with reduced cost")
def player_plays_card_with_reduced_cost(game_state):
    """Rule 1.14.5: Player plays card after its cost has been reduced to 0."""
    game_state.play_result = game_state.play_card_with_cost_reduction_1_14(
        player=game_state.player,
        card=game_state.test_card,
        reduction_effect=game_state.cost_reduction_effect,
    )


# ----- Then steps -----


@then("the card play incurs a cost")
def card_play_incurs_cost(game_state):
    """Rule 1.14.1: Card play should incur a cost requiring payment."""
    assert getattr(game_state.play_result, "_incurred_cost", False) is True, (
        "Expected card play to incur a cost (Rule 1.14.1: playing a card incurs a cost)"
    )


@then("the cost requires payment of 2 resource points")
def cost_requires_2_resource_points(game_state):
    """Rule 1.14.1/1.14.2: The incurred cost requires 2 resource points."""
    assert getattr(game_state.play_result, "_cost_amount", None) == 2, (
        f"Expected cost of 2 resource points (Rule 1.14.1)"
    )


@then("activating the ability incurs a cost")
def activating_ability_incurs_cost(game_state):
    """Rule 1.14.1: Activating an ability incurs a cost."""
    assert getattr(game_state.activation_result, "_incurred_cost", False) is True, (
        "Expected ability activation to incur a cost (Rule 1.14.1)"
    )


@then("the cost requires payment of 1 resource point")
def cost_requires_1_resource_point(game_state):
    """Rule 1.14.1/1.14.2: The incurred cost requires 1 resource point."""
    assert getattr(game_state.activation_result, "_cost_amount", None) == 1, (
        "Expected cost of 1 resource point (Rule 1.14.1)"
    )


@then("the cost has an asset-cost component")
def cost_has_asset_cost_component(game_state):
    """Rule 1.14.1: Card has an asset-cost component."""
    assert getattr(game_state.full_cost, "_has_asset_cost", False) is True, (
        "Expected cost to have an asset-cost component (Rule 1.14.1)"
    )


@then("the cost has an effect-cost component")
def cost_has_effect_cost_component(game_state):
    """Rule 1.14.1: Card has an effect-cost component."""
    assert getattr(game_state.full_cost, "_has_effect_cost", False) is True, (
        "Expected cost to have an effect-cost component (Rule 1.14.1)"
    )


@then("the cost is paid successfully")
def cost_is_paid_successfully(game_state):
    """Rule 1.14.2: The asset-cost was paid successfully."""
    assert getattr(game_state.pay_result, "_cost_paid", False) is True, (
        "Expected cost to be paid successfully (Rule 1.14.2)"
    )


@then("the player has 0 resource points remaining")
def player_has_0_resource_remaining(game_state):
    """Rule 1.14.2: All resource points were spent paying the cost."""
    remaining = game_state.get_player_resource_points(game_state.player)
    assert remaining == 0, (
        f"Expected 0 resource points remaining, got {remaining} (Rule 1.14.2)"
    )


@then("the player has 2 resource points remaining")
def player_has_2_resource_remaining(game_state):
    """Rule 1.14.2: 2 resource points remain after paying cost of 2 from 4."""
    remaining = game_state.get_player_resource_points(game_state.player)
    assert remaining == 2, (
        f"Expected 2 resource points remaining, got {remaining} (Rule 1.14.2)"
    )


@then("the cost cannot be paid")
def cost_cannot_be_paid(game_state):
    """Rule 1.14.2b: The cost payment failed."""
    # Prefer pay_result if set, otherwise fall back to play_result
    result = (
        game_state.pay_result
        if game_state.pay_result is not None
        else game_state.play_result
    )
    assert getattr(result, "_cost_paid", True) is False, (
        "Expected cost to fail because assets are insufficient (Rule 1.14.2b)"
    )


@then("the game state is reversed to before payment")
def game_state_reversed_to_before_payment(game_state):
    """Rule 1.14.2b: Game state is reversed when cost cannot be paid."""
    assert getattr(game_state.pay_result, "_game_state_reversed", False) is True, (
        "Expected game state to be reversed when cost cannot be paid (Rule 1.14.2b)"
    )


@then("chi points are paid first")
def chi_points_paid_first(game_state):
    """Rule 1.14.2a: Chi points are the first asset type paid."""
    assert getattr(game_state.multi_pay_result, "_chi_paid_order", None) == 1, (
        "Expected chi points to be paid first (Rule 1.14.2a)"
    )


@then("resource points are paid second")
def resource_points_paid_second(game_state):
    """Rule 1.14.2a: Resource points are the second asset type paid."""
    assert getattr(game_state.multi_pay_result, "_resource_paid_order", None) == 2, (
        "Expected resource points to be paid second (Rule 1.14.2a)"
    )


@then("life points are paid third")
def life_points_paid_third(game_state):
    """Rule 1.14.2a: Life points are the third asset type paid."""
    assert getattr(game_state.multi_pay_result, "_life_paid_order", None) == 3, (
        "Expected life points to be paid third (Rule 1.14.2a)"
    )


@then("action points are paid last")
def action_points_paid_last(game_state):
    """Rule 1.14.2a: Action points are the last asset type paid."""
    assert getattr(game_state.multi_pay_result, "_action_paid_order", None) == 4, (
        "Expected action points to be paid last (Rule 1.14.2a)"
    )


@then("the chi cost payment fails because chi points are insufficient")
def chi_cost_payment_fails_insufficient(game_state):
    """Rule 1.14.2a: Chi cost cannot be paid if insufficient chi points."""
    assert getattr(game_state.multi_pay_result, "_chi_payment_failed", False) is True, (
        "Expected chi payment to fail when insufficient chi (Rule 1.14.2a)"
    )


@then("payment of resource points does not begin")
def resource_payment_does_not_begin(game_state):
    """Rule 1.14.2a: Resources not paid until chi is fully paid."""
    assert (
        getattr(game_state.multi_pay_result, "_resource_payment_started", True) is False
    ), "Expected resource payment not to start when chi payment failed (Rule 1.14.2a)"


@then("the entire card play action is reversed")
def entire_card_play_action_reversed(game_state):
    """Rule 1.14.2b: The entire action (not just cost) is reversed."""
    assert getattr(game_state.play_result, "_entire_action_reversed", False) is True, (
        "Expected entire action to be reversed when mandatory cost fails (Rule 1.14.2b)"
    )


@then("the card is returned to its starting zone")
def card_returned_to_starting_zone(game_state):
    """Rule 1.14.2b: Card is back in the zone it started in."""
    assert game_state.test_card in game_state.player.hand, (
        "Expected card to be returned to hand after reversal (Rule 1.14.2b)"
    )


@then("the player gains 2 resource points from pitching")
def player_gains_2_resource_from_pitching(game_state):
    """Rule 1.14.3: Pitching grants resource points equal to pitch value."""
    assert getattr(game_state.pitch_result, "_resources_gained", None) == 2, (
        "Expected 2 resource points from pitching (Rule 1.14.3)"
    )


@then("the player now has 3 resource points total")
def player_now_has_3_resource_total(game_state):
    """Rule 1.14.2d: Player has 1 + 2 = 3 resource points after pitching (before cost payment)."""
    # Check resources stored on the pitch result (captured before cost payment)
    total = getattr(game_state.pitch_result, "_total_resources_after_pitch", None)
    if total is None:
        # Fall back to current resource points if not stored on result
        total = game_state.get_player_resource_points(game_state.player)
    assert total == 3, f"Expected 3 total resource points after pitching, got {total}"


@then("the chi points are spent")
def chi_points_are_spent(game_state):
    """Rule 1.14.2c: Chi points were used to pay the chi cost."""
    assert getattr(game_state.chi_pay_result, "_chi_spent", None) == 2, (
        "Expected 2 chi points spent (Rule 1.14.2c)"
    )


@then("the player has 1 chi point remaining")
def player_has_1_chi_remaining(game_state):
    """Rule 1.14.2c: 1 chi point remains after paying 2 from 3."""
    remaining = game_state.get_player_chi_points(game_state.player)
    assert remaining == 1, (
        f"Expected 1 chi point remaining, got {remaining} (Rule 1.14.2c)"
    )


@then("the player gains 2 chi points from pitching")
def player_gains_2_chi_from_pitching(game_state):
    """Rule 1.14.2c: Pitching a chi card grants chi points."""
    assert getattr(game_state.pitch_result, "_chi_gained", None) == 2, (
        "Expected 2 chi points gained from pitching (Rule 1.14.2c)"
    )


@then("the chi cost is paid successfully")
def chi_cost_paid_successfully(game_state):
    """Rule 1.14.2c: Chi cost paid successfully after pitching chi card."""
    assert getattr(game_state.chi_pay_result, "_cost_paid", False) is True, (
        "Expected chi cost to be paid successfully after pitching (Rule 1.14.2c)"
    )


@then("chi points are used before resource points")
def chi_used_before_resource(game_state):
    """Rule 1.14.2d: Chi points spent first when paying resource cost."""
    assert (
        getattr(game_state.resource_pay_result, "_chi_used_before_resource", False)
        is True
    ), "Expected chi to be used before resource points (Rule 1.14.2d)"


@then("1 chi point is spent")
def one_chi_point_is_spent(game_state):
    """Rule 1.14.2d: 1 chi point was used toward the resource cost."""
    assert getattr(game_state.resource_pay_result, "_chi_spent", None) == 1, (
        "Expected 1 chi point spent (Rule 1.14.2d)"
    )


@then("1 resource point is spent")
def one_resource_point_is_spent(game_state):
    """Rule 1.14.2d: 1 resource point was used after chi toward the resource cost."""
    assert getattr(game_state.resource_pay_result, "_resource_spent", None) == 1, (
        "Expected 1 resource point spent (Rule 1.14.2d)"
    )


@then("the player gains 2 resource points from the pitch")
def player_gains_2_resource_from_pitch(game_state):
    """Rule 1.14.2d: Pitching grants 2 resource points during payment."""
    assert getattr(game_state.pitch_result, "_resources_gained", None) == 2, (
        "Expected 2 resource points from pitching (Rule 1.14.2d)"
    )


@then("the resource cost is paid with available resources")
def resource_cost_paid_with_available(game_state):
    """Rule 1.14.2d: Resource cost paid after pitching gave enough resources."""
    assert getattr(game_state.pay_result, "_cost_paid", False) is True, (
        "Expected resource cost to be paid after pitching (Rule 1.14.2d)"
    )


@then("the cost is paid")
def cost_is_paid(game_state):
    """Rule 1.14.2: Cost has been paid."""
    assert getattr(game_state.pay_result, "_cost_paid", False) is True, (
        "Expected cost to be paid (Rule 1.14.2)"
    )


@then("the player has 1 resource point left over from pitching")
def player_has_1_resource_leftover(game_state):
    """Rule 1.14.2d: 1 resource point from the 3-pitch card is left over after cost of 2."""
    remaining = game_state.get_player_resource_points(game_state.player)
    assert remaining >= 1, (
        f"Expected at least 1 resource point left over after pitching, got {remaining}"
    )


@then("the player cannot pitch more cards to pay this cost")
def player_cannot_pitch_more_cards(game_state):
    """Rule 1.14.2d/1.14.3b: Cannot pitch more cards when cost is already fully paid."""
    assert getattr(game_state.further_pitch_result, "_pitch_rejected", False) is True, (
        "Expected further pitch to be rejected when cost is already paid (Rule 1.14.3b)"
    )


@then("the life points are spent")
def life_points_are_spent(game_state):
    """Rule 1.14.2e: Life points were used to pay the life cost."""
    assert getattr(game_state.life_pay_result, "_life_spent", None) == 2, (
        "Expected 2 life points spent (Rule 1.14.2e)"
    )


@then("the player hero has 18 life points remaining")
def player_hero_has_18_life(game_state):
    """Rule 1.14.2e: Hero has 18 life after paying 2 life from 20."""
    remaining = game_state.get_hero_life_total(game_state.player)
    assert remaining == 18, (
        f"Expected hero to have 18 life remaining, got {remaining} (Rule 1.14.2e)"
    )


@then("the payment fails because chi cannot pay life costs")
def payment_fails_chi_cannot_pay_life(game_state):
    """Rule 1.14.2e: Chi points cannot be used to pay life costs."""
    assert game_state.invalid_pay_result.success is False, (
        "Expected chi-for-life payment to fail (Rule 1.14.2e)"
    )
    assert game_state.invalid_pay_result.reason == "chi_cannot_substitute_for_life", (
        f"Expected reason 'chi_cannot_substitute_for_life', got {game_state.invalid_pay_result.reason}"
    )


@then("the game state is not changed")
def game_state_not_changed(game_state):
    """Rule 1.14.2e: No state was changed when payment failed."""
    life_remaining = game_state.get_hero_life_total(game_state.player)
    assert life_remaining == 1, (
        f"Expected hero life to remain 1 (unchanged), got {life_remaining}"
    )


@then("the action point is spent")
def action_point_is_spent(game_state):
    """Rule 1.14.2f: Action point was used to pay the action cost."""
    assert getattr(game_state.action_pay_result, "_action_spent", None) == 1, (
        "Expected 1 action point spent (Rule 1.14.2f)"
    )


@then("the player has 0 action points remaining")
def player_has_0_action_remaining(game_state):
    """Rule 1.14.2f: Player has 0 action points after paying the 1 action cost."""
    remaining = game_state.get_player_action_points(game_state.player)
    assert remaining == 0, (
        f"Expected 0 action points remaining, got {remaining} (Rule 1.14.2f)"
    )


@then("the card moves from hand to the pitch zone")
def card_moves_from_hand_to_pitch_zone(game_state):
    """Rule 1.14.3: Pitched card is moved from hand to pitch zone."""
    if (
        hasattr(game_state, "chi_3_pitch_card")
        and game_state.chi_3_pitch_card is not None
    ):
        card = game_state.chi_3_pitch_card
    else:
        card = game_state.pitch_card
    assert card not in game_state.player.hand, (
        "Expected pitched card to be removed from hand (Rule 1.14.3)"
    )
    assert card in game_state.player.pitch_zone, (
        "Expected pitched card to be in pitch zone (Rule 1.14.3)"
    )


@then("the player gains 3 chi points from pitching")
def player_gains_3_chi_from_pitching(game_state):
    """Rule 1.14.3: Pitching 3-chi-pitch card grants 3 chi points."""
    assert getattr(game_state.pitch_result, "_chi_gained", None) == 3, (
        "Expected 3 chi points from pitching (Rule 1.14.3)"
    )


@then("the pitch zone contains the card")
def pitch_zone_contains_the_card(game_state):
    """Rule 1.14.3: Pitched card is in pitch zone."""
    if (
        hasattr(game_state, "chi_3_pitch_card")
        and game_state.chi_3_pitch_card is not None
    ):
        card = game_state.chi_3_pitch_card
    else:
        card = game_state.pitch_card
    assert card in game_state.player.pitch_zone, (
        "Expected card to be in pitch zone after pitching (Rule 1.14.3)"
    )


@then("the pitch attempt fails")
def pitch_attempt_fails(game_state):
    """Rule 1.14.3a: Cannot pitch a card without the pitch property."""
    assert (
        getattr(game_state.pitch_attempt_result, "_pitch_succeeded", True) is False
    ), "Expected pitch to fail for card without pitch property (Rule 1.14.3a)"


@then("the card remains in hand")
def card_remains_in_hand(game_state):
    """Rule 1.14.3a: Card stays in hand when pitch fails."""
    assert game_state.no_pitch_card in game_state.player.hand, (
        "Expected card to remain in hand after failed pitch (Rule 1.14.3a)"
    )


@then("the pitch succeeds")
def pitch_succeeds(game_state):
    """Rule 1.14.3a: Card with pitch property can be pitched."""
    assert (
        getattr(game_state.pitch_attempt_result, "_pitch_succeeded", False) is True
    ), "Expected pitch to succeed for card with pitch property (Rule 1.14.3a)"


@then("the card moves to the pitch zone")
def card_moves_to_pitch_zone(game_state):
    """Rule 1.14.3a: Pitched card is in pitch zone."""
    if hasattr(game_state, "pitch_1_card") and game_state.pitch_1_card is not None:
        assert game_state.pitch_1_card in game_state.player.pitch_zone, (
            "Expected card to be in pitch zone after pitching (Rule 1.14.3a)"
        )
    elif hasattr(game_state, "no_pitch_card") and game_state.no_pitch_card is not None:
        assert game_state.no_pitch_card in game_state.player.pitch_zone, (
            "Expected card to be in pitch zone after effect-instructed pitch (Rule 1.14.3b)"
        )


@then("the pitch attempt is rejected")
def pitch_attempt_rejected(game_state):
    """Rule 1.14.3b: Pitch rejected because card doesn't gain needed asset type."""
    assert getattr(game_state.invalid_pitch_result, "_pitch_rejected", False) is True, (
        "Expected pitch to be rejected when card gains wrong asset type (Rule 1.14.3b)"
    )


@then("the reason is that the card only gains resource points not chi points")
def reason_wrong_asset_type(game_state):
    """Rule 1.14.3b: Reason for pitch rejection is wrong asset type."""
    assert (
        getattr(game_state.invalid_pitch_result, "_rejection_reason", None)
        == "wrong_asset_type"
    ), "Expected rejection reason 'wrong_asset_type' (Rule 1.14.3b)"


@then("the pitch is accepted")
def pitch_is_accepted(game_state):
    """Rule 1.14.3b: Pitch accepted because card gains the needed asset type."""
    assert getattr(game_state.valid_pitch_result, "_pitch_succeeded", False) is True, (
        "Expected pitch to be accepted when card gains needed asset type (Rule 1.14.3b)"
    )


@then("the player gains chi points for the chi cost")
def player_gains_chi_for_chi_cost(game_state):
    """Rule 1.14.3b: Chi points gained from pitching chi card toward chi cost."""
    assert getattr(game_state.valid_pitch_result, "_chi_gained", 0) > 0, (
        "Expected chi points to be gained from pitching chi card (Rule 1.14.3b)"
    )


@then("the pitch is accepted despite no normal pitch property")
def pitch_accepted_via_effect(game_state):
    """Rule 1.14.3b: Effect instruction allows pitching even without pitch property."""
    assert getattr(game_state.effect_pitch_result, "_pitch_succeeded", False) is True, (
        "Expected pitch to succeed when instructed by effect (Rule 1.14.3b)"
    )


@then("the pitch event occurs")
def pitch_event_occurs(game_state):
    """Rule 1.14.3c: Pitching is an event."""
    assert getattr(game_state.pitch_result, "_pitch_event_occurred", False) is True, (
        "Expected pitch event to occur (Rule 1.14.3c)"
    )


@then("the triggered effect fires in response to the pitch")
def triggered_effect_fires_from_pitch(game_state):
    """Rule 1.14.3c: Triggered effects fire in response to pitch events."""
    assert game_state.pitch_trigger_count == 1, (
        f"Expected pitch trigger to fire once, count={game_state.pitch_trigger_count} (Rule 1.14.3c)"
    )


@then("the replacement effect modifies the pitch event")
def replacement_effect_modifies_pitch(game_state):
    """Rule 1.14.3c: Replacement effect was applied to the pitch event."""
    assert game_state.pitch_was_replaced is True, (
        "Expected replacement effect to be applied to pitch event (Rule 1.14.3c)"
    )


@then("the modified pitch occurs instead of the normal pitch")
def modified_pitch_occurs(game_state):
    """Rule 1.14.3c: The replaced pitch event occurs (not the original)."""
    assert getattr(game_state.pitch_result, "_was_replaced", False) is True, (
        "Expected pitch to occur with replacement modification (Rule 1.14.3c)"
    )


@then("the destroy effect is generated")
def destroy_effect_is_generated(game_state):
    """Rule 1.14.4: Destroy effect is generated as part of effect-cost payment."""
    assert getattr(game_state.effect_cost_result, "_effect_generated", False) is True, (
        "Expected destroy effect to be generated as effect-cost (Rule 1.14.4)"
    )


@then("the target card is destroyed as the cost")
def target_card_destroyed_as_cost(game_state):
    """Rule 1.14.4: The target card is destroyed during effect-cost payment."""
    assert getattr(game_state.effect_cost_result, "_target_destroyed", False) is True, (
        "Expected target card to be destroyed as part of effect-cost (Rule 1.14.4)"
    )


@then("destroying Hope Merchants Hood is an effect-cost")
def destroying_hope_merchants_hood_is_effect_cost(game_state):
    """Rule 1.14.4: Destroying Hope Merchant's Hood is part of the effect-cost."""
    assert (
        getattr(game_state.hood_activation_result, "_destroy_was_effect_cost", False)
        is True
    ), "Expected Hood destruction to be an effect-cost (Rule 1.14.4)"


@then("the cards are shuffled back into the deck")
def cards_shuffled_back_into_deck(game_state):
    """Rule 1.14.4: After paying effect-cost, the effect of the ability resolves."""
    assert (
        getattr(game_state.hood_activation_result, "_cards_shuffled", False) is True
    ), "Expected cards to be shuffled back into deck (Rule 1.14.4)"


@then("the player declares the order of the effects")
def player_declares_effect_order(game_state):
    """Rule 1.14.4a: Player can declare the order of multiple effect-costs."""
    assert (
        getattr(game_state.multi_effect_cost_result, "_player_declared_order", False)
        is True
    ), "Expected player to declare the order of effect-costs (Rule 1.14.4a)"


@then("the effects are generated in the declared order")
def effects_generated_in_declared_order(game_state):
    """Rule 1.14.4a: Effects are generated in the order declared by the player."""
    assert (
        getattr(
            game_state.multi_effect_cost_result, "_generated_in_declared_order", False
        )
        is True
    ), "Expected effects to be generated in declared order (Rule 1.14.4a)"


@then("the effect-cost cannot be paid")
def effect_cost_cannot_be_paid(game_state):
    """Rule 1.14.4b: Effect-cost cannot be paid when generation fails."""
    assert getattr(game_state.effect_cost_result, "_cost_paid", True) is False, (
        "Expected effect-cost to fail when effect cannot be generated (Rule 1.14.4b)"
    )


@then("the game state is reversed to before activation")
def game_state_reversed_to_before_activation(game_state):
    """Rule 1.14.4b: Game state reversed when effect-cost fails."""
    assert (
        getattr(game_state.effect_cost_result, "_game_state_reversed", False) is True
    ), "Expected game state to be reversed when effect-cost fails (Rule 1.14.4b)"


@then("the effect-cost cannot be resolved")
def effect_cost_cannot_be_resolved(game_state):
    """Rule 1.14.4b: Effect-cost cannot be resolved when there is nothing to discard."""
    assert getattr(game_state.play_result, "_cost_paid", True) is False, (
        "Expected effect-cost to fail when no discard target (Rule 1.14.4b)"
    )


@then("the replacement effect replaces the discard event")
def replacement_replaces_discard_event(game_state):
    """Rule 1.14.4c: The replacement effect modifies the discard into a banishment."""
    assert (
        getattr(game_state.effect_cost_result, "_replacement_was_applied", False)
        is True
    ), "Expected replacement effect to be applied to discard event (Rule 1.14.4c)"


@then("the cost is still considered paid despite the replacement")
def cost_still_considered_paid_after_replacement(game_state):
    """Rule 1.14.4c: Effect-cost is paid even when its events are replaced."""
    assert getattr(game_state.effect_cost_result, "_cost_paid", False) is True, (
        "Expected effect-cost to be considered paid after replacement (Rule 1.14.4c)"
    )


@then("the cost of 0 is acknowledged as paid")
def cost_of_zero_acknowledged_as_paid(game_state):
    """Rule 1.14.5: Zero cost is acknowledged and considered paid."""
    assert getattr(game_state.play_result, "_zero_cost_acknowledged", False) is True, (
        "Expected zero cost to be acknowledged as paid (Rule 1.14.5)"
    )


@then("the card play proceeds normally")
def card_play_proceeds_normally(game_state):
    """Rule 1.14.5: Card play proceeds normally after zero-cost acknowledgment."""
    assert getattr(game_state.play_result, "_play_succeeded", False) is True, (
        "Expected card play to succeed after zero cost (Rule 1.14.5)"
    )


@then("the cost has been reduced to 0")
def cost_has_been_reduced_to_zero(game_state):
    """Rule 1.14.5: Cost reduction effect brought cost to 0."""
    assert getattr(game_state.play_result, "_effective_cost", -1) == 0, (
        "Expected effective cost of 0 (Rule 1.14.5)"
    )


@then("the zero cost is acknowledged as paid")
def zero_cost_acknowledged_as_paid(game_state):
    """Rule 1.14.5: Zero cost (after reduction) is acknowledged as paid."""
    assert getattr(game_state.play_result, "_zero_cost_acknowledged", False) is True, (
        "Expected zero cost (after reduction) to be acknowledged (Rule 1.14.5)"
    )


@then("the zero cost is a valid cost")
def zero_cost_is_valid_cost(game_state):
    """Rule 1.14.5: Zero cost is a valid cost that must be acknowledged."""
    assert getattr(game_state.play_result, "_has_cost", False) is True, (
        "Expected zero-cost card to still have a cost (Rule 1.14.5)"
    )


@then("the cost is paid by acknowledging it")
def cost_paid_by_acknowledging(game_state):
    """Rule 1.14.5: Zero cost is paid by acknowledging it."""
    assert getattr(game_state.play_result, "_zero_cost_acknowledged", False) is True, (
        "Expected zero cost to be paid via acknowledgment (Rule 1.14.5)"
    )


# ============================================================
# Fixtures
# ============================================================


@pytest.fixture
def game_state():
    """
    Fixture providing game state for Section 1.14 (Costs) testing.

    Uses BDDGameState which integrates with the real engine.
    Reference: Rule 1.14
    """
    from tests.bdd_helpers import BDDGameState

    state = BDDGameState()

    # Initialize test state containers (section 1.14 specific)
    state.test_card = None
    state.ability_card = None
    state.pitch_card = None
    state.chi_pitch_card = None
    state.no_pitch_card = None
    state.pitch_1_card = None
    state.resource_pitch_card = None
    state.large_pitch_card = None
    state.chi_3_pitch_card = None
    state.multi_asset_ability = None
    state.chi_resource_ability = None
    state.chi_ability = None
    state.life_ability = None
    state.life_ability_1 = None
    state.action_ability = None
    state.destroy_cost_ability = None
    state.weapon_destroy_ability = None
    state.discard_cost_ability = None
    state.two_cost_ability = None
    state.hope_merchants_hood = None
    state.cost_reduction_effect = None
    state.pitch_trigger = None
    state.pitch_trigger_count = 0
    state.pitch_replacement = None
    state.pitch_was_replaced = False
    state.discard_to_banish_replacement = None
    state.play_result = None
    state.activation_result = None
    state.pay_result = None
    state.multi_pay_result = None
    state.chi_pay_result = None
    state.resource_pay_result = None
    state.life_pay_result = None
    state.action_pay_result = None
    state.pitch_result = None
    state.pitch_attempt_result = None
    state.invalid_pitch_result = None
    state.valid_pitch_result = None
    state.effect_pitch_result = None
    state.effect_cost_result = None
    state.multi_effect_cost_result = None
    state.hood_activation_result = None
    state.further_pitch_result = None
    state.invalid_pay_result = None
    state.full_cost = None
    state.current_cost_type = None
    state.current_cost_amount = 0
    state.card_starting_zone = "hand"
    state.player_weapon = None
    state.has_pitch_instruction_effect = False
    state.pitch_instruction_effect = None
    state.discard_card_ref = None
    state.damage_target = None

    return state
