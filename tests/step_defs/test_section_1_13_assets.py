"""
Step definitions for Section 1.13: Assets
Reference: Flesh and Blood Comprehensive Rules Section 1.13

This module implements behavioral tests for the asset system in Flesh and Blood.
Assets are points of a given type owned by a player, used to pay costs when
playing cards and activating abilities.

Engine Features Needed for Section 1.13:
- [ ] PlayerAssets class tracking action_points, resource_points, life_points, chi_points (Rule 1.13.1)
- [ ] AssetType enum with ACTION_POINT, RESOURCE_POINT, LIFE_POINT, CHI_POINT (Rule 1.13.1)
- [ ] Player.assets property returning PlayerAssets (Rule 1.13.1)
- [ ] Player.gain_asset(asset_type, amount) method (Rules 1.13.2a, 1.13.3a, 1.13.4a, 1.13.5a)
- [ ] Player.spend_asset(asset_type, amount) method (Rule 1.13.2)
- [ ] GameEngine.begin_action_phase(player_id) granting 1 action point (Rule 1.13.2a)
- [ ] GoAgainEffect granting 1 action point when trigger fires (Rule 1.13.2a)
- [ ] Action phase guard: Player.can_gain_action_points() = False outside action phase (Rule 1.13.2b)
- [ ] Chi points counted as resource points for resource payment (Rule 1.13.5b)
- [ ] Payment order: chi first, then resource, then life, then action (Rule 1.14.2a)
- [ ] PitchEffect generating assets based on card pitch type and value (Rule 1.13.3a, 1.13.5a)
- [ ] Pitch restriction: only pitch if card generates needed asset type (Rule 1.14.3b)
"""

import pytest
from pytest_bdd import scenario, given, when, then, parsers


# ============================================================
# Scenario: There are exactly four types of assets
# Tests Rule 1.13.1 - Four asset types
# ============================================================


@scenario(
    "../features/section_1_13_assets.feature",
    "There are exactly four types of assets",
)
def test_there_are_exactly_four_asset_types():
    """Rule 1.13.1: There are four types of assets."""
    pass


# ============================================================
# Scenario: An asset is owned by a player
# Tests Rule 1.13.1 - Assets belong to players
# ============================================================


@scenario(
    "../features/section_1_13_assets.feature",
    "An asset is owned by a player",
)
def test_asset_owned_by_player():
    """Rule 1.13.1: Assets are points owned by a player."""
    pass


# ============================================================
# Scenario: Action points are used to play action cards
# Tests Rule 1.13.2 - Action points spent on action card play
# ============================================================


@scenario(
    "../features/section_1_13_assets.feature",
    "Action points are used to play action cards",
)
def test_action_points_used_to_play_action_cards():
    """Rule 1.13.2: Action points are spent when playing action cards."""
    pass


# ============================================================
# Scenario: Player gains 1 action point at start of action phase
# Tests Rule 1.13.2a - Action point gained at phase start
# ============================================================


@scenario(
    "../features/section_1_13_assets.feature",
    "Player gains 1 action point at start of action phase",
)
def test_player_gains_action_point_at_action_phase_start():
    """Rule 1.13.2a: Player gains 1 action point at the start of their action phase."""
    pass


# ============================================================
# Scenario: Go again grants player 1 additional action point
# Tests Rule 1.13.2a - Go again ability grants action point
# ============================================================


@scenario(
    "../features/section_1_13_assets.feature",
    "Go again grants player 1 additional action point",
)
def test_go_again_grants_action_point():
    """Rule 1.13.2a: The go again ability grants the player 1 action point."""
    pass


# ============================================================
# Scenario: Effect grants action points during action phase
# Tests Rule 1.13.2a - Effects can grant action points
# ============================================================


@scenario(
    "../features/section_1_13_assets.feature",
    "Effect grants action points during action phase",
)
def test_effect_grants_action_points():
    """Rule 1.13.2a: Effects that grant action points work during the action phase."""
    pass


# ============================================================
# Scenario: Non-turn player cannot gain action points from go again
# Tests Rule 1.13.2b - Action points blocked outside action phase
# ============================================================


@scenario(
    "../features/section_1_13_assets.feature",
    "Non-turn player cannot gain action points from go again",
)
def test_non_turn_player_no_action_points_from_go_again():
    """Rule 1.13.2b: A player not in their action phase cannot gain action points from go again."""
    pass


# ============================================================
# Scenario: Non-turn player cannot gain action points from effects outside action phase
# Tests Rule 1.13.2b - Effects blocked outside action phase
# ============================================================


@scenario(
    "../features/section_1_13_assets.feature",
    "Non-turn player cannot gain action points from effects outside action phase",
)
def test_non_turn_player_no_action_points_from_effects():
    """Rule 1.13.2b: Effects that would grant action points are blocked outside action phase."""
    pass


# ============================================================
# Scenario: Lead the Charge non-turn player gets no action points
# Tests Rule 1.13.2b - Lead the Charge example from the rules
# ============================================================


@scenario(
    "../features/section_1_13_assets.feature",
    "Lead the Charge non-turn player gets no action points",
)
def test_lead_the_charge_no_action_points_outside_phase():
    """Rule 1.13.2b: Lead the Charge example - non-turn player gets no action point."""
    pass


# ============================================================
# Scenario: Resource points are used to pay card costs
# Tests Rule 1.13.3 - Resource points spent on card costs
# ============================================================


@scenario(
    "../features/section_1_13_assets.feature",
    "Resource points are used to pay card costs",
)
def test_resource_points_used_to_pay_card_costs():
    """Rule 1.13.3: Resource points are spent to pay for card costs."""
    pass


# ============================================================
# Scenario: Player gains resource points by pitching a card
# Tests Rule 1.13.3a - Pitching generates resource points
# ============================================================


@scenario(
    "../features/section_1_13_assets.feature",
    "Player gains resource points by pitching a card",
)
def test_player_gains_resource_points_from_pitch():
    """Rule 1.13.3a: Pitching a card generates resource points when paying costs."""
    pass


# ============================================================
# Scenario: Effect grants resource points directly
# Tests Rule 1.13.3a - Effects can grant resource points
# ============================================================


@scenario(
    "../features/section_1_13_assets.feature",
    "Effect grants resource points directly",
)
def test_effect_grants_resource_points():
    """Rule 1.13.3a: Effects can directly grant resource points to a player."""
    pass


# ============================================================
# Scenario: Life points come from the hero life total
# Tests Rule 1.13.4 - Life points are tied to the hero
# ============================================================


@scenario(
    "../features/section_1_13_assets.feature",
    "Life points come from the hero life total",
)
def test_life_points_come_from_hero_life_total():
    """Rule 1.13.4: Life points are paid from a player's hero's life total."""
    pass


# ============================================================
# Scenario: Life points can be used to activate abilities
# Tests Rule 1.13.4 - Life points spent to activate abilities
# ============================================================


@scenario(
    "../features/section_1_13_assets.feature",
    "Life points can be used to activate abilities",
)
def test_life_points_activate_abilities():
    """Rule 1.13.4: Life points are paid from the hero's life total to activate abilities."""
    pass


# ============================================================
# Scenario: Player gains life points when hero life total increases
# Tests Rule 1.13.4a - Gaining life points via effects
# ============================================================


@scenario(
    "../features/section_1_13_assets.feature",
    "Player gains life points when hero life total increases",
)
def test_player_gains_life_points_from_effect():
    """Rule 1.13.4a: Life points are gained when effects increase the hero's life total."""
    pass


# ============================================================
# Scenario: Chi points are used to play cards and activate abilities
# Tests Rule 1.13.5 - Chi point usage
# ============================================================


@scenario(
    "../features/section_1_13_assets.feature",
    "Chi points are used to play cards and activate abilities",
)
def test_chi_points_used_to_play_cards():
    """Rule 1.13.5: Chi points are spent when playing cards and activating abilities."""
    pass


# ============================================================
# Scenario: Player gains chi points by pitching a chi card
# Tests Rule 1.13.5a - Chi pitch generates chi points
# ============================================================


@scenario(
    "../features/section_1_13_assets.feature",
    "Player gains chi points by pitching a chi card",
)
def test_player_gains_chi_points_from_chi_pitch():
    """Rule 1.13.5a: Pitching a chi card generates chi points."""
    pass


# ============================================================
# Scenario: Chi point substitutes for resource point in cost payment
# Tests Rule 1.13.5b - Chi substitutes for resource
# ============================================================


@scenario(
    "../features/section_1_13_assets.feature",
    "Chi point substitutes for resource point in cost payment",
)
def test_chi_point_substitutes_for_resource_point():
    """Rule 1.13.5b: Chi points can be used in place of resource points."""
    pass


# ============================================================
# Scenario: Chi points are used before resource points in payment
# Tests Rule 1.13.5b + 1.14.2a - Chi used before resource in payment order
# ============================================================


@scenario(
    "../features/section_1_13_assets.feature",
    "Chi points are used before resource points in payment",
)
def test_chi_points_used_before_resource_points():
    """Rule 1.13.5b + 1.14.2a: Player must use all chi points before any resource points."""
    pass


# ============================================================
# Scenario: Chi points cannot substitute for non-resource costs
# Tests Rule 1.13.5b (limitation) - Chi only replaces resource costs
# ============================================================


@scenario(
    "../features/section_1_13_assets.feature",
    "Chi points cannot substitute for non-resource costs",
)
def test_chi_points_cannot_substitute_for_life_costs():
    """Rule 1.13.5b: Chi points can only substitute for resource point costs, not life costs."""
    pass


# ============================================================
# Scenario: Pitching a resource card gains resource points
# Tests Rule 1.13.3a - Resource card pitch generates resource points
# ============================================================


@scenario(
    "../features/section_1_13_assets.feature",
    "Pitching a resource card gains resource points",
)
def test_pitching_resource_card_gains_resource_points():
    """Rule 1.13.3a: Pitching a resource card generates resource points."""
    pass


# ============================================================
# Scenario: Pitching a chi card gains chi points
# Tests Rule 1.13.5a - Chi card pitch generates chi points
# ============================================================


@scenario(
    "../features/section_1_13_assets.feature",
    "Pitching a chi card gains chi points",
)
def test_pitching_chi_card_gains_chi_points():
    """Rule 1.13.5a: Pitching a chi card generates chi points."""
    pass


# ============================================================
# Scenario: Cannot pitch card during payment if it gains the wrong asset type
# Tests Rule 1.14.3b - Pitch restricted to needed asset type
# ============================================================


@scenario(
    "../features/section_1_13_assets.feature",
    "Cannot pitch card during payment if it gains the wrong asset type",
)
def test_cannot_pitch_wrong_asset_type_card():
    """Rule 1.14.3b: Cannot pitch a card that generates the wrong type of assets."""
    pass


# ============================================================
# Step Definitions
# ============================================================


@given("a player exists in the game")
def player_exists(game_state):
    """Rule 1.13.1: Set up a player in the game state."""
    # Player already exists in the game_state fixture
    assert game_state.player is not None


@when("I query the available asset types")
def query_asset_types(game_state):
    """Rule 1.13.1: Query what asset types exist in the game."""
    game_state.asset_types = game_state.get_asset_types()


@then("there are exactly 4 asset types")
def exactly_four_asset_types(game_state):
    """Rule 1.13.1: Exactly 4 asset types must exist."""
    assert len(game_state.asset_types) == 4, (
        f"Expected 4 asset types but got {len(game_state.asset_types)}"
    )


@then(parsers.parse('one of the asset types is "{asset_type}"'))
def asset_type_exists(game_state, asset_type):
    """Rule 1.13.1: Each of the four asset types must be present."""
    assert asset_type in game_state.asset_types, (
        f"Expected '{asset_type}' in asset types but got: {game_state.asset_types}"
    )


@given(parsers.parse("the player has {amount:d} action points"))
def player_has_action_points(game_state, amount):
    """Rule 1.13.1: Set the player's action point count."""
    game_state.set_player_action_points(game_state.player, amount)


@given("the player has been given 2 action points")
def player_given_two_action_points(game_state):
    """Rule 1.13.1: Set the player's action points to 2 for ownership test."""
    game_state.set_player_action_points(game_state.player, 2)


@when("the engine queries player ownership of those action points")
def engine_queries_ownership(game_state):
    """Rule 1.13.1: Query who owns the action points."""
    pass  # Ownership determined by which player's asset pool they are in


@then("the player owns those action points")
def player_owns_action_points(game_state):
    """Rule 1.13.1: Assets are owned by the player."""
    owned_action_points = game_state.get_player_action_points(game_state.player)
    assert owned_action_points == 2, (
        f"Expected player to own 2 action points but got {owned_action_points}"
    )


@then("the action points belong to that specific player")
def action_points_belong_to_player(game_state):
    """Rule 1.13.1: Assets belong to the specific player who owns them."""
    # Verify the other player (defender) does not have the same action points
    other_action_points = game_state.get_player_action_points(game_state.defender)
    assert other_action_points == 0, (
        f"Expected defender to have 0 action points but got {other_action_points}"
    )


@given(parsers.parse("a player has {amount:d} action point"))
def player_has_one_action_point(game_state, amount):
    """Rule 1.13.2: Set the player's single action point."""
    game_state.set_player_action_points(game_state.player, amount)


@when("the player spends 1 action point to play an action card")
def player_spends_action_point(game_state):
    """Rule 1.13.2: Spend action point to play an action card."""
    game_state.action_spend_result = game_state.spend_player_action_point(
        game_state.player
    )


@then(parsers.parse("the player has {amount:d} action points"))
def player_has_n_action_points(game_state, amount):
    """Rule 1.13.2: Verify action point count."""
    current = game_state.get_player_action_points(game_state.player)
    assert current == amount, (
        f"Expected player to have {amount} action points but got {current}"
    )


@then("the action card play was permitted")
def action_card_play_permitted(game_state):
    """Rule 1.13.2: Verify the action card was permitted to be played."""
    assert game_state.action_spend_result is not None
    assert game_state.action_spend_result.success, (
        f"Expected action card play to be permitted but got: {game_state.action_spend_result}"
    )


@given("a player starts their action phase")
def player_starts_action_phase(game_state):
    """Rule 1.13.2a: Set up a player starting their action phase."""
    game_state.set_player_action_points(game_state.player, 0)
    game_state.player._in_action_phase = True  # type: ignore[attr-defined]


@when("the action phase begins")
def action_phase_begins(game_state):
    """Rule 1.13.2a: Trigger the action phase start process."""
    game_state.begin_action_phase_for_player(game_state.player)


@then("the player gains 1 action point")
def player_gains_one_action_point(game_state):
    """Rule 1.13.2a: Player gets 1 action point when action phase begins."""
    current = game_state.get_player_action_points(game_state.player)
    assert current >= 1, (
        f"Expected player to have gained at least 1 action point but has {current}"
    )


@then("the player has 1 action point available")
def player_has_one_action_point_available(game_state):
    """Rule 1.13.2a: Player has exactly 1 action point at start of action phase."""
    current = game_state.get_player_action_points(game_state.player)
    assert current == 1, f"Expected player to have 1 action point but has {current}"


@given(parsers.parse("a player is in their action phase with {amount:d} action point"))
def player_in_action_phase_with_action_points(game_state, amount):
    """Rule 1.13.2a: Set up player in action phase with given action points."""
    game_state.set_player_action_points(game_state.player, amount)
    game_state.player._in_action_phase = True  # type: ignore[attr-defined]


@given("the player's attack has the go again keyword")
def attack_has_go_again(game_state):
    """Rule 1.13.2a: The attack has the go again keyword."""
    game_state.attack.add_keyword("go_again")


@when("the go again effect triggers")
def go_again_triggers(game_state):
    """Rule 1.13.2a: Trigger the go again effect to grant an action point."""
    game_state.trigger_go_again_for_player(game_state.player)


@then("the player has 2 action points total")
def player_has_two_action_points_total(game_state):
    """Rule 1.13.2a: Player should have 2 action points after go again."""
    current = game_state.get_player_action_points(game_state.player)
    assert current == 2, (
        f"Expected player to have 2 action points total but has {current}"
    )


@when("an effect grants the player 1 additional action point")
def effect_grants_action_point(game_state):
    """Rule 1.13.2a: An effect grants the player 1 action point."""
    game_state.grant_action_points_via_effect(game_state.player, amount=1)


@given("player 0 is in their action phase")
def player_0_in_action_phase(game_state):
    """Rule 1.13.2b: Player 0 is in their action phase (turn player)."""
    game_state.set_player_action_points(game_state.player, 1)
    game_state.player._in_action_phase = True  # type: ignore[attr-defined]
    game_state.turn_player_id = 0


@given("player 1 is NOT in their action phase")
def player_1_not_in_action_phase(game_state):
    """Rule 1.13.2b: Player 1 is not in their action phase."""
    game_state.set_player_action_points(game_state.defender, 0)
    game_state.defender._in_action_phase = False  # type: ignore[attr-defined]


@when("player 1 plays an instant with the go again ability")
def player_1_plays_instant_with_go_again(game_state):
    """Rule 1.13.2b: Player 1 plays an instant card with go again as a non-turn player."""
    game_state.simulate_instant_play_with_go_again(game_state.defender)


@then("player 1 does not gain any action points from go again")
def player_1_no_action_points_from_go_again(game_state):
    """Rule 1.13.2b: Go again does not grant action points outside action phase."""
    current = game_state.get_player_action_points(game_state.defender)
    assert current == 0, (
        f"Expected player 1 to have 0 action points (not their phase) but has {current}"
    )


@then("player 1 has 0 action points")
def player_1_has_zero_action_points(game_state):
    """Rule 1.13.2b: Player 1 ends up with 0 action points."""
    current = game_state.get_player_action_points(game_state.defender)
    assert current == 0, f"Expected player 1 to have 0 action points but has {current}"


@when("an effect would grant player 1 an action point")
def effect_would_grant_player_1_action_point(game_state):
    """Rule 1.13.2b: Attempt to grant action point via effect outside action phase."""
    game_state.attempt_grant_action_points_outside_phase(game_state.defender, amount=1)


@then("player 1 does not gain any action points")
def player_1_does_not_gain_action_points(game_state):
    """Rule 1.13.2b: Action points are not gained outside the action phase."""
    current = game_state.get_player_action_points(game_state.defender)
    assert current == 0, (
        f"Expected player 1 to not gain action points (blocked by rule 1.13.2b) but has {current}"
    )


@given("player 1 has played Lead the Charge as an instant with delayed trigger")
def player_1_played_lead_the_charge(game_state):
    """Rule 1.13.2b: Lead the Charge creates a delayed trigger for next cost 0 action."""
    game_state.register_lead_the_charge_trigger_for(game_state.defender)


@when("player 1 plays a cost 0 action card as an instant")
def player_1_plays_cost_zero_instant(game_state):
    """Rule 1.13.2b: Player 1 plays a cost 0 action card as an instant."""
    game_state.simulate_cost_zero_action_play(game_state.defender)


@then("player 1 does not gain an action point from the delayed trigger")
def no_action_point_from_delayed_trigger(game_state):
    """Rule 1.13.2b: Delayed trigger from Lead the Charge doesn't fire outside action phase."""
    current = game_state.get_player_action_points(game_state.defender)
    assert current == 0, (
        f"Expected no action points from delayed Lead the Charge trigger but has {current}"
    )


@given(parsers.parse("a player has {amount:d} resource points"))
def player_has_resource_points(game_state, amount):
    """Rule 1.13.3: Set up player with resource points."""
    game_state.set_player_resource_points(game_state.player, amount)


@when(
    parsers.parse(
        "the player spends {amount:d} resource points to pay for a card with cost {cost:d}"
    )
)
def player_spends_resource_points(game_state, amount, cost):
    """Rule 1.13.3: Player spends resource points to pay a card cost."""
    game_state.resource_spend_result = game_state.pay_resource_cost(
        game_state.player, cost
    )


@then(parsers.parse("the player has {amount:d} resource points"))
def player_has_n_resource_points(game_state, amount):
    """Rule 1.13.3: Verify resource point count."""
    current = game_state.get_player_resource_points(game_state.player)
    assert current == amount, (
        f"Expected player to have {amount} resource points but got {current}"
    )


@then("the card cost was paid successfully")
def card_cost_paid_successfully(game_state):
    """Rule 1.13.3: Verify the card cost was paid."""
    assert game_state.resource_spend_result is not None
    assert game_state.resource_spend_result.success, (
        f"Expected card cost payment to succeed but got: {game_state.resource_spend_result}"
    )


@given(
    parsers.parse(
        "a player has {resource_count:d} resource points in hand with a {pitch:d}-pitch card"
    )
)
def player_has_resource_points_and_pitch_card(game_state, resource_count, pitch):
    """Rule 1.13.3a: Set up player with resource points and a pitchable card."""
    game_state.set_player_resource_points(game_state.player, resource_count)
    pitch_card = game_state.create_card_with_pitch(
        name=f"{pitch}-pitch card",
        pitch_value=pitch,
        pitch_generates="resource",
    )
    game_state.player.hand.add_card(pitch_card)
    game_state.pitch_card = pitch_card


@when(parsers.parse("the player pitches the {pitch:d}-pitch card during cost payment"))
def player_pitches_card(game_state, pitch):
    """Rule 1.13.3a: Player pitches the card to generate resource points."""
    game_state.pitch_result = game_state.pitch_card_for_resources(
        game_state.player, game_state.pitch_card
    )


@then(parsers.parse("the player gains {amount:d} resource points"))
def player_gains_resource_points(game_state, amount):
    """Rule 1.13.3a: Player gained the expected number of resource points from pitching."""
    gained = game_state.get_player_resource_points(game_state.player)
    assert gained >= amount, (
        f"Expected player to gain at least {amount} resource points but has {gained}"
    )


@then("the pitched card moves to the pitch zone")
def pitched_card_in_pitch_zone(game_state):
    """Rule 1.13.3a / 1.14.3: Pitched card moves to the pitch zone."""
    assert game_state.pitch_card in game_state.player.pitch_zone, (
        "Expected pitched card to be in the pitch zone"
    )


@given(parsers.parse("a player has {amount:d} resource points"))
def player_has_zero_resource_points(game_state, amount):
    """Rule 1.13.3a: Set up player with resource points."""
    game_state.set_player_resource_points(game_state.player, amount)


@when(parsers.parse("an effect grants the player {amount:d} resource points"))
def effect_grants_resource_points(game_state, amount):
    """Rule 1.13.3a: Effect directly grants resource points."""
    game_state.grant_resource_points_via_effect(game_state.player, amount)


@then(parsers.parse("the player has {amount:d} resource points"))
def player_has_n_resource_points_check(game_state, amount):
    """Rule 1.13.3a: Verify the correct number of resource points after effect."""
    current = game_state.get_player_resource_points(game_state.player)
    assert current == amount, (
        f"Expected player to have {amount} resource points but has {current}"
    )


@given(parsers.parse("a player's hero has {life:d} life"))
def players_hero_has_life(game_state, life):
    """Rule 1.13.4: Set the player's hero life total."""
    game_state.set_hero_life_total(game_state.player, life)


@when("the engine checks the player's life point assets")
def check_life_point_assets(game_state):
    """Rule 1.13.4: Check how many life point assets the player has."""
    game_state.life_point_query_result = game_state.get_player_life_points(
        game_state.player
    )


@then("the player has life points equal to the hero's life total")
def life_points_equal_to_hero_total(game_state):
    """Rule 1.13.4: Life points are tied directly to the hero's life total."""
    hero_life = game_state.get_hero_life_total(game_state.player)
    life_points = game_state.life_point_query_result
    assert life_points == hero_life, (
        f"Expected life points ({life_points}) to equal hero's life total ({hero_life})"
    )


@then("the life point asset is tracked on the hero")
def life_points_tracked_on_hero(game_state):
    """Rule 1.13.4: Life points are stored on the hero card."""
    assert game_state.player_hero_has_life_tracking(game_state.player), (
        "Expected hero to have life tracking for life point assets"
    )


@given('there is an ability with cost "pay 2 life"')
def ability_with_life_cost(game_state):
    """Rule 1.13.4: Set up an ability that costs 2 life points."""
    game_state.life_cost_ability = game_state.create_ability_with_life_cost(
        cost=2, ability_text="Pay 2 life: Draw a card"
    )


@when("the player activates the ability and pays 2 life points")
def player_activates_life_cost_ability(game_state):
    """Rule 1.13.4: Player activates the ability by paying life points."""
    game_state.life_ability_result = game_state.activate_ability_with_life_cost(
        game_state.player, game_state.life_cost_ability, life_cost=2
    )


@then("the hero's life total is reduced to 18")
def hero_life_reduced_to_18(game_state):
    """Rule 1.13.4: Paying 2 life from 20 hero life reduces it to 18."""
    hero_life = game_state.get_hero_life_total(game_state.player)
    assert hero_life == 18, (
        f"Expected hero life to be 18 after paying 2 life but got {hero_life}"
    )


@then("the ability activation was permitted")
def ability_activation_permitted(game_state):
    """Rule 1.13.4: Verify the ability activation was permitted."""
    assert game_state.life_ability_result is not None
    assert game_state.life_ability_result.success, (
        f"Expected ability activation to be permitted but got: {game_state.life_ability_result}"
    )


@given(
    parsers.parse(
        "a player's hero has {current:d} life out of a maximum of {maximum:d}"
    )
)
def hero_has_partial_life(game_state, current, maximum):
    """Rule 1.13.4a: Set up hero with below-maximum life total."""
    game_state.set_hero_life_total(game_state.player, current)
    game_state.hero_max_life = maximum


@when(parsers.parse("an effect increases the hero's life total by {amount:d}"))
def effect_increases_hero_life(game_state, amount):
    """Rule 1.13.4a: Effect increases the hero's life total."""
    game_state.life_gain_result = game_state.grant_life_points_via_effect(
        game_state.player, amount
    )


@then(parsers.parse("the player has gained {amount:d} life points"))
def player_gained_life_points(game_state, amount):
    """Rule 1.13.4a: Player gained the correct number of life points."""
    assert game_state.life_gain_result is not None
    assert game_state.life_gain_result.amount_gained == amount, (
        f"Expected to gain {amount} life points but gained "
        f"{game_state.life_gain_result.amount_gained}"
    )


@then(parsers.parse("the hero's life total is {total:d}"))
def hero_life_total_is(game_state, total):
    """Rule 1.13.4a: Verify the hero's life total after gaining life."""
    hero_life = game_state.get_hero_life_total(game_state.player)
    assert hero_life == total, (
        f"Expected hero life total to be {total} but got {hero_life}"
    )


@given(parsers.parse("a player has {amount:d} chi points"))
def player_has_chi_points(game_state, amount):
    """Rule 1.13.5: Set up player with chi points."""
    game_state.set_player_chi_points(game_state.player, amount)


@when(parsers.parse("the player spends {amount:d} chi points to pay for a chi cost"))
def player_spends_chi_points(game_state, amount):
    """Rule 1.13.5: Player spends chi points to pay a chi cost."""
    game_state.chi_spend_result = game_state.pay_chi_cost(game_state.player, amount)


@then("the chi cost was paid successfully")
def chi_cost_paid_successfully(game_state):
    """Rule 1.13.5: Verify the chi cost was paid."""
    assert game_state.chi_spend_result is not None
    assert game_state.chi_spend_result.success, (
        f"Expected chi cost payment to succeed but got: {game_state.chi_spend_result}"
    )


@then("the chi points are available to spend")
def chi_points_available(game_state):
    """Rule 1.13.5: The gained chi points can be used for future costs."""
    chi_count = game_state.get_player_chi_points(game_state.player)
    assert chi_count > 0, "Expected player to have chi points available to spend"


@then(parsers.parse("the player has {amount:d} chi points"))
def player_has_n_chi_points(game_state, amount):
    """Rule 1.13.5: Verify chi point count."""
    current = game_state.get_player_chi_points(game_state.player)
    assert current == amount, (
        f"Expected player to have {amount} chi points but got {current}"
    )


@given("a player has 0 chi points and holds a 1-chi-pitch card")
def player_has_chi_pitch_card(game_state):
    """Rule 1.13.5a: Set up player with a chi-generating pitch card."""
    game_state.set_player_chi_points(game_state.player, 0)
    chi_card = game_state.create_card_with_pitch(
        name="Chi Pitch Card",
        pitch_value=1,
        pitch_generates="chi",
    )
    game_state.player.hand.add_card(chi_card)
    game_state.chi_pitch_card = chi_card


@when("the player pitches the chi card during cost payment")
def player_pitches_chi_card(game_state):
    """Rule 1.13.5a: Player pitches the chi card to generate chi points."""
    game_state.chi_pitch_result = game_state.pitch_card_for_chi(
        game_state.player, game_state.chi_pitch_card
    )


@then("the player gains 1 chi point")
def player_gains_one_chi_point(game_state):
    """Rule 1.13.5a: Pitching a 1-chi card grants 1 chi point."""
    chi_count = game_state.get_player_chi_points(game_state.player)
    assert chi_count >= 1, (
        f"Expected player to have gained at least 1 chi point but has {chi_count}"
    )


@given("a player has 0 resource points and 2 chi points")
def player_has_only_chi_points(game_state):
    """Rule 1.13.5b: Set up player with chi points but no resource points."""
    game_state.set_player_resource_points(game_state.player, 0)
    game_state.set_player_chi_points(game_state.player, 2)


@when("the player pays a resource cost of 2 using chi points")
def player_pays_resource_cost_using_chi(game_state):
    """Rule 1.13.5b: Player pays a resource cost of 2 using chi points."""
    game_state.chi_resource_payment_result = game_state.pay_resource_cost_with_chi(
        game_state.player, 2
    )


@then("the payment succeeds with chi points replacing resource points")
def payment_succeeded_with_chi(game_state):
    """Rule 1.13.5b: Verify the payment succeeded using chi points."""
    assert game_state.chi_resource_payment_result is not None
    assert game_state.chi_resource_payment_result.success, (
        "Expected chi-substituted resource payment to succeed"
    )


@then("the player used 2 chi points to pay the resource cost")
def player_used_chi_for_resource(game_state):
    """Rule 1.13.5b: Verify chi points were used instead of resource points."""
    result = game_state.chi_resource_payment_result
    assert result is not None
    assert result.chi_used == 2, (
        f"Expected 2 chi points to be used but used {result.chi_used}"
    )


@given("a player has 1 resource point and 2 chi points")
def player_has_resource_and_chi_points(game_state):
    """Rule 1.13.5b + 1.14.2a: Set up player with both resource and chi points."""
    game_state.set_player_resource_points(game_state.player, 1)
    game_state.set_player_chi_points(game_state.player, 2)


@when("the player pays a cost of 2 resource points")
def player_pays_two_resource_cost(game_state):
    """Rule 1.13.5b + 1.14.2a: Player pays a cost that requires 2 resource points."""
    game_state.mixed_payment_result = (
        game_state.pay_resource_cost_with_available_assets(game_state.player, cost=2)
    )


@then("the player uses the 2 chi points first")
def player_uses_chi_before_resource(game_state):
    """Rule 1.13.5b + 1.14.2a: Chi must be spent before resource points."""
    result = game_state.mixed_payment_result
    assert result is not None
    assert result.chi_used == 2, (
        f"Expected 2 chi points used first but used {result.chi_used}"
    )


@then("the player still has 1 resource point remaining")
def player_still_has_resource_point(game_state):
    """Rule 1.13.5b + 1.14.2a: Resource point is preserved when chi covers the cost."""
    remaining_resource = game_state.get_player_resource_points(game_state.player)
    assert remaining_resource == 1, (
        f"Expected 1 resource point remaining but has {remaining_resource}"
    )


@given("a player has 2 chi points")
def player_has_two_chi_points(game_state):
    """Rule 1.13.5b: Set up player with chi points."""
    game_state.set_player_chi_points(game_state.player, 2)


@when("the player needs to pay a life point cost of 2")
def player_needs_to_pay_life_cost(game_state):
    """Rule 1.13.5b: Set up a life point cost payment requirement."""
    game_state.life_payment_cost = 2


@then("the player cannot use chi points to pay the life cost")
def chi_cannot_pay_life_cost(game_state):
    """Rule 1.13.5b: Chi points cannot substitute for life point costs."""
    result = game_state.attempt_chi_for_life_payment(
        game_state.player, game_state.life_payment_cost
    )
    assert not result.success, (
        "Expected chi payment for life cost to be rejected but it succeeded"
    )
    assert result.reason == "chi_cannot_substitute_for_life", (
        f"Expected rejection reason 'chi_cannot_substitute_for_life' but got: {result.reason}"
    )


@then("the payment fails unless the player has 2 life points")
def payment_fails_without_life_points(game_state):
    """Rule 1.13.5b: Life point payment requires actual life points."""
    # The player has 0 life points set up for this test, so payment should fail
    result = game_state.attempt_chi_for_life_payment(
        game_state.player, game_state.life_payment_cost
    )
    assert not result.success, (
        "Expected life point cost payment to fail when player has only chi points"
    )


@given(
    parsers.parse("a player holds a card with pitch value {pitch:d} of type resource")
)
def player_holds_resource_pitch_card(game_state, pitch):
    """Rule 1.13.3a: Player holds a card that generates resource points when pitched."""
    resource_card = game_state.create_card_with_pitch(
        name=f"Resource Pitch Card",
        pitch_value=pitch,
        pitch_generates="resource",
    )
    game_state.player.hand.add_card(resource_card)
    game_state.resource_pitch_card = resource_card


@when("the player pitches the card to pay a resource cost")
def player_pitches_card_for_resource(game_state):
    """Rule 1.13.3a: Player pitches the card to generate resource points."""
    game_state.resource_pitch_result = game_state.pitch_card_for_resources(
        game_state.player, game_state.resource_pitch_card
    )


@then(parsers.parse("the player gains {amount:d} resource points from the pitch"))
def player_gains_resource_from_pitch(game_state, amount):
    """Rule 1.13.3a: Verify resource points gained from pitching."""
    gained = game_state.get_player_resource_points(game_state.player)
    assert gained == amount, (
        f"Expected {amount} resource points from pitch but gained {gained}"
    )


@given(parsers.parse("a player holds a card with pitch value {pitch:d} of type chi"))
def player_holds_chi_pitch_card(game_state, pitch):
    """Rule 1.13.5a: Player holds a card that generates chi points when pitched."""
    chi_card = game_state.create_card_with_pitch(
        name=f"Chi Pitch Card",
        pitch_value=pitch,
        pitch_generates="chi",
    )
    game_state.player.hand.add_card(chi_card)
    game_state.chi_type_pitch_card = chi_card


@when("the player pitches the card to pay a chi or resource cost")
def player_pitches_card_for_chi(game_state):
    """Rule 1.13.5a: Player pitches the chi card to generate chi points."""
    game_state.chi_type_pitch_result = game_state.pitch_card_for_chi(
        game_state.player, game_state.chi_type_pitch_card
    )


@then(parsers.parse("the player gains {amount:d} chi points from the pitch"))
def player_gains_chi_from_pitch(game_state, amount):
    """Rule 1.13.5a: Verify chi points gained from pitching a chi card."""
    gained = game_state.get_player_chi_points(game_state.player)
    assert gained == amount, (
        f"Expected {amount} chi points from pitch but gained {gained}"
    )


@given("a player has 0 chi points and needs to pay 2 chi points")
def player_has_no_chi_needs_chi(game_state):
    """Rule 1.14.3b: Player needs chi points but has none."""
    game_state.set_player_chi_points(game_state.player, 0)
    game_state.required_chi_cost = 2


@given("the player holds a card that only generates resource points when pitched")
def player_holds_resource_only_card(game_state):
    """Rule 1.14.3b: Player holds a resource-generating card."""
    resource_card = game_state.create_card_with_pitch(
        name="Resource Only Pitch Card",
        pitch_value=2,
        pitch_generates="resource",
    )
    game_state.player.hand.add_card(resource_card)
    game_state.resource_only_card = resource_card


@when("the player tries to pitch the resource-generating card to pay the chi cost")
def player_tries_wrong_pitch(game_state):
    """Rule 1.14.3b: Player attempts to pitch a card that generates the wrong asset type."""
    game_state.wrong_pitch_result = game_state.attempt_pitch_for_wrong_type(
        game_state.player,
        card=game_state.resource_only_card,
        needed_asset="chi",
    )


@then("the pitch is rejected")
def pitch_is_rejected(game_state):
    """Rule 1.14.3b: The pitch attempt was rejected because wrong asset type."""
    assert not game_state.wrong_pitch_result.success, (
        "Expected pitch to be rejected (wrong asset type) but it succeeded"
    )
    assert game_state.wrong_pitch_result.reason == "wrong_asset_type", (
        f"Expected rejection reason 'wrong_asset_type' but got: "
        f"{game_state.wrong_pitch_result.reason}"
    )


@then("the player gains no assets from the failed pitch attempt")
def player_gains_no_assets_from_failed_pitch(game_state):
    """Rule 1.14.3b: No assets are gained from a rejected pitch attempt."""
    chi_count = game_state.get_player_chi_points(game_state.player)
    resource_count = game_state.get_player_resource_points(game_state.player)
    assert chi_count == 0, (
        f"Expected 0 chi points after failed pitch but has {chi_count}"
    )
    assert resource_count == 0, (
        f"Expected 0 resource points after failed pitch but has {resource_count}"
    )


# ============================================================
# Fixtures
# ============================================================


@pytest.fixture
def game_state():
    """
    Fixture providing game state for Section 1.13 asset tests.

    Uses BDDGameState which integrates with the real engine.
    Reference: Rules 1.13.1 - 1.13.5b
    """
    from tests.bdd_helpers import BDDGameState

    state = BDDGameState()

    # Add asset tracking helpers
    state.asset_types = []
    state.pitch_card = None
    state.chi_pitch_card = None
    state.chi_type_pitch_card = None
    state.resource_only_card = None
    state.resource_pitch_card = None
    state.action_spend_result = None
    state.resource_spend_result = None
    state.chi_spend_result = None
    state.life_ability_result = None
    state.life_gain_result = None
    state.pitch_result = None
    state.chi_pitch_result = None
    state.chi_type_pitch_result = None
    state.resource_pitch_result = None
    state.wrong_pitch_result = None
    state.mixed_payment_result = None
    state.life_point_query_result = None
    state.life_cost_ability = None
    state.resource_payment_cost = 0
    state.life_payment_cost = 0
    state.required_chi_cost = 0
    state.hero_max_life = 20
    state.turn_player_id = 0
    state.chi_resource_payment_result = None

    return state
