"""
Step definitions for Section 8.3.5: Go again (Ability Keyword)
Reference: Flesh and Blood Comprehensive Rules Section 8.3.5

This module implements behavioral tests for the go again ability keyword:
- Go again is a resolution ability meaning "Gain 1 action point" (Rule 8.3.5)
- For non-attack layers: fires AFTER all other resolution abilities (Rule 8.3.5a / 5.3.5)
- For attacks on the active chain link: fires at the BEGINNING of Resolution Step (Rule 8.3.5b / 7.6.2)
- An object cannot have more than one go again ability (Rule 8.3.5c)
- Last known information used when the object no longer exists (Rule 5.3.5a, 7.6.2a)
- LKI is immutable; conditional static go again cannot apply retroactively (Rule 1.2.3c)
- Go again gained is lost if the object resets (becomes new object) (Rule 3.0.9)

Engine Features Needed for Section 8.3.5:
- [ ] AbilityKeyword.GO_AGAIN resolution ability on cards (Rule 8.3.5)
- [ ] GoAgainAbility.is_resolution -> True (Rule 8.3.5)
- [ ] GoAgainAbility.meaning == "Gain 1 action point" (Rule 8.3.5)
- [ ] LayerResolver resolves go again AFTER all other resolution abilities (Rule 5.3.5)
- [ ] LayerResolver.resolve_go_again(layer, player) grants 1 AP for non-attack layers (Rule 8.3.5a)
- [ ] ResolutionStep.begin() grants 1 AP if attack had go again (Rule 8.3.5b / 7.6.2)
- [ ] GoAgainDuplicateCheck: adding go again to object with go again fails (Rule 8.3.5c)
- [ ] LastKnownInfo.had_go_again(chain_link) uses LKI when object gone (Rule 7.6.2a)
- [ ] LastKnownInfo is immutable — conditional static go again cannot alter it (Rule 1.2.3c)
- [ ] Object.reset() on zone change removes gained go again (Rule 3.0.9)
- [ ] Non-turn-player go again outside action phase: no action point granted (Rule 1.13.2a)

Current status: Tests written, Engine pending
"""

import pytest
from pytest_bdd import scenario, given, when, then, parsers
from typing import Optional, Any


# ===== Rule 8.3.5: Go again is a resolution ability =====

@scenario(
    "../features/section_8_3_5_go_again.feature",
    "Go again is a resolution ability",
)
def test_go_again_is_resolution_ability():
    """Rule 8.3.5: Go again is a special resolution ability."""
    pass


# ===== Rule 8.3.5a: Non-attack layer =====

@scenario(
    "../features/section_8_3_5_go_again.feature",
    "Non-attack layer with go again grants action point after other resolutions",
)
def test_non_attack_layer_go_again_grants_ap_after_others():
    """Rule 8.3.5a: Go again fires last (after other resolution abilities) for non-attack layers."""
    pass


@scenario(
    "../features/section_8_3_5_go_again.feature",
    "Non-turn player does not gain action point from go again outside action phase",
)
def test_go_again_outside_action_phase_no_ap():
    """Rule 1.13.2a: Go again only grants AP during action phase (non-turn player example)."""
    pass


# ===== Rule 8.3.5b: Attack on active chain link =====

@scenario(
    "../features/section_8_3_5_go_again.feature",
    "Attack with go again grants 1 action point at the Resolution Step",
)
def test_attack_with_go_again_grants_ap_at_resolution_step():
    """Rule 8.3.5b: Attack go again fires at the beginning of the Resolution Step."""
    pass


@scenario(
    "../features/section_8_3_5_go_again.feature",
    "Attack without go again does not grant action point at Resolution Step",
)
def test_attack_without_go_again_no_ap():
    """Rule 8.3.5b: No action point is granted if the attack lacks go again."""
    pass


# ===== Rule 8.3.5c: At most one go again =====

@scenario(
    "../features/section_8_3_5_go_again.feature",
    "An object cannot be given go again if it already has go again",
)
def test_duplicate_go_again_fails():
    """Rule 8.3.5c: Granting go again to an object that already has it fails."""
    pass


@scenario(
    "../features/section_8_3_5_go_again.feature",
    "Giving go again to a card without it succeeds",
)
def test_granting_go_again_to_card_without_it_succeeds():
    """Rule 8.3.5c: Granting go again to an object without it succeeds normally."""
    pass


# ===== Rule 5.3.5a / 7.6.2a: LKI for go again =====

@scenario(
    "../features/section_8_3_5_go_again.feature",
    "Attack moved off combat chain uses last known info for go again",
)
def test_attack_off_chain_uses_lki_for_go_again():
    """Rule 7.6.2a: When attack leaves combat chain, LKI determines whether it had go again."""
    pass


@scenario(
    "../features/section_8_3_5_go_again.feature",
    "Non-attack layer moved off stack uses last known info for go again",
)
def test_non_attack_off_stack_uses_lki_for_go_again():
    """Rule 5.3.5a: When non-attack layer no longer exists, LKI determines go again."""
    pass


# ===== Rule 1.2.3c: LKI is immutable =====

@scenario(
    "../features/section_8_3_5_go_again.feature",
    "Conditional go again cannot apply retroactively via last known information",
)
def test_conditional_go_again_cannot_alter_lki():
    """Rule 1.2.3c: LKI is immutable; conditional static go again cannot update it after the fact."""
    pass


# ===== Rule 3.0.9: Object reset =====

@scenario(
    "../features/section_8_3_5_go_again.feature",
    "Go again gained then lost when object moves to non-arena non-stack zone",
)
def test_go_again_lost_when_object_resets():
    """Rule 3.0.9: When a card becomes a new object (resets), gained go again is not retained."""
    pass


# ===== Step Definitions =====

# ---- Given steps ----

@given('a card with the "go again" keyword ability')
def card_with_go_again(game_state):
    """Rule 8.3.5: Create a card that has the go again ability."""
    card = game_state.create_card(name="Test Go Again Card")
    card._has_go_again = True
    game_state.go_again_card = card


@given("a player is in their action phase with 0 action points")
def player_in_action_phase_zero_ap(game_state):
    """Rule 1.13.2a: Player in action phase starts with 0 AP for this test."""
    game_state.player._in_action_phase = True
    game_state.set_player_action_points(game_state.player, 0)


@given("a player is in their action phase with 1 action point")
def player_in_action_phase_one_ap(game_state):
    """Rule 1.13.2a: Player in action phase with 1 AP."""
    game_state.player._in_action_phase = True
    game_state.set_player_action_points(game_state.player, 1)


@given("a player is not in their action phase")
def player_not_in_action_phase(game_state):
    """Rule 1.13.2b: Go again only grants AP during action phase."""
    game_state.player._in_action_phase = False
    game_state.set_player_action_points(game_state.player, 0)


@given("the player controls a non-attack action card with go again on the stack")
def player_has_non_attack_go_again_on_stack(game_state):
    """Rule 8.3.5a: Non-attack card with go again is on the stack."""
    card = game_state.create_card(name="Non-Attack Go Again")
    card._has_go_again = True
    game_state.non_attack_go_again_card = card
    game_state.play_card_to_stack(card, controller_id=0)


@given("the card has resolution abilities that generate other effects")
def card_has_other_resolution_abilities(game_state):
    """Rule 5.3.5: Other resolution abilities resolve before go again."""
    # Track that other abilities should have resolved first
    game_state.other_abilities_resolved_before_go_again = None  # Will be set during resolution


@given("the player's attack has the go again ability on the active chain link")
def attack_with_go_again_on_chain_link(game_state):
    """Rule 8.3.5b: Attack with go again is the active chain link."""
    card = game_state.create_card(name="Test Attack With Go Again")
    game_state.attacking_card = card
    chain_link = game_state.put_on_combat_chain(card, has_go_again=True)
    game_state.active_chain_link = chain_link


@given("the player's attack does not have the go again ability")
def attack_without_go_again(game_state):
    """Rule 8.3.5b: Attack without go again creates no AP at Resolution Step."""
    card = game_state.create_card(name="Test Attack No Go Again")
    game_state.attacking_card = card
    chain_link = game_state.put_on_combat_chain(card)
    game_state.active_chain_link = chain_link


@given('a card already has the "go again" ability')
def card_already_has_go_again(game_state):
    """Rule 8.3.5c: Card already has go again."""
    card = game_state.create_card(name="Card With Go Again")
    card._has_go_again = True
    game_state.go_again_card = card


@given('a card does not have the "go again" ability')
def card_without_go_again(game_state):
    """Rule 8.3.5c: Card does not have go again."""
    card = game_state.create_card(name="Card Without Go Again")
    card._has_go_again = False
    game_state.no_go_again_card = card


@given("the attack is moved off the combat chain before the Resolution Step")
def attack_moved_off_chain(game_state):
    """Rule 7.6.2a: Attack removed from combat chain before Resolution Step."""
    lki = game_state.remove_from_combat_chain(game_state.attacking_card)
    game_state.removed_chain_link_lki = lki
    # Replace the active chain link with the LKI so Resolution Step uses LKI
    game_state.active_chain_link = lki


@given("the player controls a non-attack card with go again that was placed on the stack")
def non_attack_card_placed_on_stack(game_state):
    """Rule 5.3.5a: Non-attack card with go again placed on stack."""
    game_state.player._in_action_phase = True
    game_state.set_player_action_points(game_state.player, 0)
    card = game_state.create_card(name="Stack Go Again Card")
    card._has_go_again = True
    game_state.stack_go_again_card = card
    game_state.play_card_to_stack(card, controller_id=0)


@given("the card is removed from the stack before resolution completes")
def card_removed_from_stack(game_state):
    """Rule 5.3.5a: Card removed from stack; LKI holds go again state."""
    lki = game_state.move_card_to_hand_during_resolution(game_state.stack_go_again_card)
    game_state.removed_card_lki = lki


@given("a player controls an Illusionist attack as a chain link")
def player_controls_illusionist_attack_chain_link(game_state):
    """Rule 1.2.3c / Luminaris example: Illusionist attack as chain link."""
    card = game_state.create_card(name="Illusionist Attack")
    # No go again yet — condition not met
    card._has_go_again = False
    game_state.illusionist_attack = card
    chain_link = game_state.put_on_combat_chain(card)
    game_state.illusionist_chain_link = chain_link


@given("an effect gives Illusionist attacks go again when a yellow card is in the pitch zone")
def conditional_go_again_effect_setup(game_state):
    """Rule 1.2.3c: Conditional static ability (like Luminaris) granting go again."""
    # Track that a conditional effect exists that would give go again
    # only when a yellow card is in pitch zone
    game_state.conditional_go_again_condition = "yellow_card_in_pitch"
    game_state.conditional_go_again_met = False


@given("the attack is removed from the combat chain before the condition is met")
def attack_removed_before_condition_met(game_state):
    """Rule 1.2.3c: Attack removed; its LKI does NOT have go again yet."""
    lki = game_state.remove_from_combat_chain(game_state.illusionist_attack)
    game_state.illusionist_lki = lki
    # At time of removal, LKI does NOT have go again (condition not met yet)


@given('an attack card has the "go again" ability added to it during the reaction step')
def attack_card_gains_go_again_during_reaction(game_state):
    """Rule 3.0.9 / Snapdragon Scalers example: go again added mid-combat."""
    card = game_state.create_card(name="Endless Arrow Attack")
    game_state.resetting_attack_card = card
    # Simulate gaining go again (e.g., via Snapdragon Scalers)
    card._has_go_again = True  # gained via effect during reaction step


# ---- When steps ----

@when("I inspect the go again ability on the card")
def inspect_go_again_ability(game_state):
    """Rule 8.3.5: Inspect the go again ability on the card."""
    game_state.inspected_ability = game_state.get_go_again_ability(
        game_state.go_again_card
    )


@when("the non-attack layer resolves")
def non_attack_layer_resolves(game_state):
    """Rule 8.3.5a / 5.3.5: Non-attack layer resolves, go again fires last."""
    result = game_state.resolve_non_attack_layer_with_go_again(
        game_state.non_attack_go_again_card,
        game_state.player,
    )
    game_state.resolution_result = result


@when("the Resolution Step begins")
def resolution_step_begins(game_state):
    """Rule 8.3.5b / 7.6.2: Resolution Step begins — go again checked for active chain link."""
    chain_link = getattr(game_state, "active_chain_link", None)
    result = game_state.begin_resolution_step(
        chain_link,
        game_state.player,
    )
    game_state.resolution_step_result = result


@when('an effect attempts to give the "go again" ability to the card again')
def effect_attempts_duplicate_go_again(game_state):
    """Rule 8.3.5c: Attempt to grant go again to card that already has it."""
    game_state.duplicate_go_again_result = game_state.grant_go_again(
        game_state.go_again_card
    )


@when('an effect gives the "go again" ability to the card')
def effect_grants_go_again(game_state):
    """Rule 8.3.5c: Grant go again to card that doesn't have it."""
    game_state.grant_go_again_result = game_state.grant_go_again(
        game_state.no_go_again_card
    )


@when("go again is evaluated after resolution")
def go_again_evaluated_after_resolution(game_state):
    """Rule 5.3.5a: Go again evaluated using LKI since card no longer on stack."""
    lki = game_state.removed_card_lki
    result = game_state.evaluate_go_again_from_lki(lki, game_state.player)
    game_state.lki_go_again_result = result


@when("a yellow card is placed into the pitch zone")
def yellow_card_placed_in_pitch(game_state):
    """Rule 1.2.3c: Condition is now met, but LKI of the attack is already fixed."""
    game_state.conditional_go_again_met = True
    # Attempt to apply conditional go again via LKI (should fail — LKI is immutable)
    lki = game_state.illusionist_lki
    game_state.conditional_apply_result = game_state.try_modify_lki(
        lki, "add_go_again"
    )


@when("the attack card moves to a zone that resets the object")
def attack_moves_to_resetting_zone(game_state):
    """Rule 3.0.9: Card moves to hand (non-arena, non-stack) and resets."""
    # Move to hand simulates the object reset (e.g., Endless Arrow "when this hits, put into hand")
    result = game_state.move_card_to_zone_causing_reset(
        game_state.resetting_attack_card
    )
    game_state.reset_card = result  # The new object (reset)


# ---- Then steps ----

@then("the go again ability is a resolution ability")
def go_again_is_resolution_ability(game_state):
    """Rule 8.3.5: Go again ability must be categorized as a resolution ability."""
    ability = game_state.inspected_ability
    assert ability is not None, "Card should have a go again ability"
    is_resolution = getattr(ability, "is_resolution", None)
    assert is_resolution is True, (
        f"Go again should be a resolution ability (Rule 8.3.5), got: {is_resolution}"
    )


@then('the go again ability means "Gain 1 action point"')
def go_again_meaning_is_correct(game_state):
    """Rule 8.3.5: Go again means 'Gain 1 action point'."""
    ability = game_state.inspected_ability
    meaning = getattr(ability, "meaning", None)
    assert meaning == "Gain 1 action point", (
        f"Go again meaning should be 'Gain 1 action point' (Rule 8.3.5), got: {meaning}"
    )


@then("the other resolution abilities resolve before go again")
def other_abilities_resolve_before_go_again(game_state):
    """Rule 5.3.5: Go again fires after all other resolution abilities."""
    result = game_state.resolution_result
    ordering = getattr(result, "go_again_was_last", None)
    assert ordering is True, (
        "Go again should resolve AFTER all other resolution abilities (Rule 5.3.5)"
    )


@then("the player gains 1 action point from go again")
def player_gains_one_ap_from_go_again(game_state):
    """Rule 8.3.5a/b: Player gains 1 action point due to go again."""
    ap = game_state.get_player_action_points(game_state.player)
    assert ap >= 1, (
        f"Player should have gained 1 action point from go again (Rule 8.3.5), got {ap}"
    )


@then("the player does not gain an action point from go again")
def player_does_not_gain_ap_from_go_again(game_state):
    """Rule 1.13.2a/b: Go again outside action phase does not grant AP."""
    ap = game_state.get_player_action_points(game_state.player)
    assert ap == 0, (
        f"Player should NOT gain action point from go again outside action phase (Rule 1.13.2b), got {ap}"
    )


@then("the player now has 2 action points")
def player_now_has_two_ap(game_state):
    """Rule 8.3.5b: Attack go again adds 1 AP to existing 1 AP = 2 total."""
    ap = game_state.get_player_action_points(game_state.player)
    assert ap == 2, (
        f"Player should have 2 action points after go again (Rule 8.3.5b), got {ap}"
    )


@then("the player does not gain an action point from the attack")
def player_does_not_gain_ap_from_attack(game_state):
    """Rule 8.3.5b: No go again on attack = no AP granted at Resolution Step."""
    result = game_state.resolution_step_result
    ap_gained = getattr(result, "action_points_granted", 0)
    assert ap_gained == 0, (
        f"Attack without go again should not grant AP (Rule 8.3.5b), got {ap_gained}"
    )


@then("the player still has 1 action point")
def player_still_has_one_ap(game_state):
    """Rule 8.3.5b: No AP gained at Resolution Step without go again."""
    ap = game_state.get_player_action_points(game_state.player)
    assert ap == 1, (
        f"Player AP should remain 1 (no go again, Rule 8.3.5b), got {ap}"
    )


@then("that part of the effect fails")
def duplicate_go_again_effect_part_fails(game_state):
    """Rule 8.3.5c: Granting go again to an object that already has it fails."""
    result = game_state.duplicate_go_again_result
    assert result is not None, "grant_go_again should return a result"
    succeeded = getattr(result, "success", None)
    assert succeeded is False, (
        f"Granting go again to object that already has it should fail (Rule 8.3.5c), got success={succeeded}"
    )


@then("the card still has exactly one go again ability")
def card_has_exactly_one_go_again_after_fail(game_state):
    """Rule 8.3.5c: Card should still have exactly one go again after failed duplicate grant."""
    card = game_state.go_again_card
    count = game_state.count_go_again_abilities(card)
    assert count == 1, (
        f"Card should have exactly 1 go again ability (Rule 8.3.5c), got {count}"
    )


@then("the card gains the go again ability")
def card_gains_go_again(game_state):
    """Rule 8.3.5c: Granting go again to a card without it succeeds."""
    result = game_state.grant_go_again_result
    succeeded = getattr(result, "success", None)
    assert succeeded is True, (
        f"Granting go again to card without it should succeed (Rule 8.3.5c), got success={succeeded}"
    )


@then("the card has exactly one go again ability")
def card_has_exactly_one_go_again(game_state):
    """Rule 8.3.5c: Card should have exactly one go again ability."""
    card = game_state.no_go_again_card
    count = game_state.count_go_again_abilities(card)
    assert count == 1, (
        f"Card should have exactly 1 go again ability after granting (Rule 8.3.5c), got {count}"
    )


@then("last known information is used to determine whether the attack had go again")
def lki_used_to_determine_go_again_for_attack(game_state):
    """Rule 7.6.2a: LKI is used when attack is off the combat chain."""
    result = game_state.resolution_step_result
    used_lki = getattr(result, "used_last_known_information", None)
    assert used_lki is True, (
        "Engine should use last known information for go again when attack is off chain (Rule 7.6.2a)"
    )


@then("the player gains 1 action point because the attack had go again")
def player_gains_ap_because_attack_had_go_again_via_lki(game_state):
    """Rule 7.6.2a: Even with attack off chain, go again still grants AP if LKI has it."""
    ap = game_state.get_player_action_points(game_state.player)
    assert ap >= 1, (
        f"Player should gain 1 AP from go again via LKI (Rule 7.6.2a), got {ap}"
    )


@then("the player gains 1 action point because the card had go again")
def player_gains_ap_because_card_had_go_again_via_lki(game_state):
    """Rule 5.3.5a: Even with non-attack layer off stack, go again grants AP if LKI has it."""
    ap = game_state.get_player_action_points(game_state.player)
    assert ap >= 1, (
        f"Player should gain 1 AP from go again via LKI (Rule 5.3.5a), got {ap}"
    )


@then("last known information is used to determine whether the card had go again")
def lki_used_to_determine_go_again_for_non_attack(game_state):
    """Rule 5.3.5a: LKI is used when non-attack layer no longer exists."""
    result = game_state.lki_go_again_result
    used_lki = getattr(result, "used_last_known_information", None)
    assert used_lki is True, (
        "Engine should use last known information for go again when layer is gone (Rule 5.3.5a)"
    )


@then("the chain link does not gain go again via the conditional effect")
def chain_link_does_not_gain_go_again_via_conditional(game_state):
    """Rule 1.2.3c: LKI is immutable; conditional effect cannot add go again retroactively."""
    result = game_state.conditional_apply_result
    # ModificationResultStub uses .failed=True to signal the modification did not apply
    failed = getattr(result, "failed", None)
    was_noop = getattr(result, "was_noop", None)
    assert (failed is True) or (was_noop is True), (
        "Conditional go again should NOT apply to LKI after the fact (Rule 1.2.3c); "
        f"expected failed=True or was_noop=True, got failed={failed}, was_noop={was_noop}"
    )


@then("the player does not gain an action point from the conditional effect")
def player_does_not_gain_ap_from_conditional_go_again(game_state):
    """Rule 1.2.3c: Since LKI can't be modified, no AP is granted."""
    # The LKI did not have go again at the time the attack was removed
    lki = game_state.illusionist_lki
    had_go_again = getattr(lki, "had_go_again", False)
    assert had_go_again is False, (
        "LKI of removed attack should not have go again (Rule 1.2.3c)"
    )


@then("the reset card is a new object with no relation to its previous existence")
def reset_card_is_new_object(game_state):
    """Rule 3.0.9: Card that moved to hand is a new object."""
    reset_card = game_state.reset_card
    is_new_object = getattr(reset_card, "is_new_object", None)
    assert is_new_object is True, (
        "Card should be a new object after moving to hand (Rule 3.0.9)"
    )


@then('the reset card does not have the "go again" ability')
def reset_card_has_no_go_again(game_state):
    """Rule 3.0.9: New object has no relation to previous existence; gained go again is gone."""
    reset_card = game_state.reset_card
    has_go_again = getattr(reset_card, "_has_go_again", False)
    assert has_go_again is False, (
        "Reset card (new object) should NOT have go again (Rule 3.0.9)"
    )


# ===== Fixtures =====

@pytest.fixture
def game_state():
    """
    Fixture providing game state for testing go again (Rule 8.3.5).

    Uses BDDGameState which integrates with the real engine.
    Reference: Rules 8.3.5, 8.3.5a, 8.3.5b, 8.3.5c, 5.3.5, 7.6.2, 1.2.3c, 3.0.9
    """
    from tests.bdd_helpers import BDDGameState

    state = BDDGameState()
    return state
