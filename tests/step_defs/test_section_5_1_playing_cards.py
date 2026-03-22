"""
Step definitions for Section 5.1: Playing Cards
Reference: Flesh and Blood Comprehensive Rules Section 5.1

This module implements behavioral tests for the card playing process in FaB.

Engine Features Needed for Section 5.1:
- [ ] CardPlayProcess: sequence of steps (Announce, Declare Costs, Declare Modes and Targets,
      Check Legal Play, Calculate Asset-Costs, Pay Asset-Costs, Calculate Effect-Costs,
      Pay Effect-Costs, Play) - Rule 5.1.1
- [ ] Zone restrictions: cards can only be played from hand or arsenal by default - Rule 5.1.1a
- [ ] Ownership check: only owner can play a card - Rule 5.1.1
- [ ] Announce step: moves card to stack as topmost layer - Rule 5.1.2
- [ ] Continuous effect application on announce for "next card played" effects - Rule 5.1.2a
- [ ] Play restriction check at announce time - Rule 5.1.2b
- [ ] Variable cost X declaration and X=0 rule for free plays - Rule 5.1.3a
- [ ] Optional additional cost declaration - Rule 5.1.3b
- [ ] Alternative cost declaration (only one permitted) - Rule 5.1.3c
- [ ] Instant vs non-instant action declaration - Rule 5.1.3d
- [ ] Effect-cost ordering declaration - Rule 5.1.3e
- [ ] Attack target declaration - Rule 5.1.4b
- [ ] Check Legal Play step: reverses game state if illegal - Rule 5.1.5
- [ ] Asset-cost calculation order: set -> increase -> reduce (floor 0) - Rule 5.1.6a
- [ ] Action asset-cost: 0 for instants, 1 for non-instant actions - Rule 5.1.6b
- [ ] Resource asset-cost: 0 when alternative cost declared - Rule 5.1.6c
- [ ] Game state reversal when asset-cost not paid in full - Rule 5.1.7a
- [ ] Game state reversal when effect-cost cannot be paid - Rule 5.1.8a
- [ ] Replacement effect on effect-cost: card can still be played - Rule 5.1.9a
- [ ] Player regains priority after Play step - Rule 5.1.10

Current status: Tests written, Engine pending
"""

import pytest
from pytest_bdd import scenario, given, when, then, parsers


# ===== Scenarios =====


@scenario(
    "../features/section_5_1_playing_cards.feature",
    "A player can play a card from their hand",
)
def test_play_from_hand():
    """Rule 5.1.1a: Cards can be played from hand."""
    pass


@scenario(
    "../features/section_5_1_playing_cards.feature",
    "A player can play a card from their arsenal",
)
def test_play_from_arsenal():
    """Rule 5.1.1a: Cards can be played from arsenal."""
    pass


@scenario(
    "../features/section_5_1_playing_cards.feature",
    "A player cannot play a card from an invalid zone without special permission",
)
def test_cannot_play_from_graveyard():
    """Rule 5.1.1a: Cards cannot be played from zones other than hand/arsenal without permission."""
    pass


@scenario(
    "../features/section_5_1_playing_cards.feature",
    "Only the owner of a card can play it",
)
def test_only_owner_can_play():
    """Rule 5.1.1: Only the owner can play a card unless otherwise specified."""
    pass


@scenario(
    "../features/section_5_1_playing_cards.feature",
    "Announcing a card moves it to the stack as topmost layer",
)
def test_announce_moves_card_to_stack():
    """Rule 5.1.2: Announcing a card moves it to the stack as topmost layer."""
    pass


@scenario(
    "../features/section_5_1_playing_cards.feature",
    "Announcing a second card makes it the new topmost layer",
)
def test_second_announce_becomes_topmost():
    """Rule 5.1.2: The most recently announced card is the topmost layer."""
    pass


@scenario(
    "../features/section_5_1_playing_cards.feature",
    "A continuous effect applying to the next card played activates on announce",
)
def test_continuous_effect_applies_on_announce():
    """Rule 5.1.2a: 'Next card played' effects apply when the matching card is announced."""
    pass


@scenario(
    "../features/section_5_1_playing_cards.feature",
    "A continuous effect does not apply if the card doesn't match the description",
)
def test_continuous_effect_does_not_apply_for_non_matching_card():
    """Rule 5.1.2a: 'Next attack action card played' effect does not apply to non-attack cards."""
    pass


@scenario(
    "../features/section_5_1_playing_cards.feature",
    "A card may not be announced if no rule or effect allows it to be played",
)
def test_card_cannot_be_announced_without_permission():
    """Rule 5.1.2b: Cards may only be announced if a rule or effect allows it."""
    pass


@scenario(
    "../features/section_5_1_playing_cards.feature",
    "A player declares the value of X for a card with variable cost",
)
def test_declare_variable_cost_x():
    """Rule 5.1.3a: Players must declare the value of X for variable-cost cards."""
    pass


@scenario(
    "../features/section_5_1_playing_cards.feature",
    "A player playing a card without paying its cost containing X must declare X as 0",
)
def test_free_play_x_equals_zero():
    """Rule 5.1.3a: When playing a card with X cost without paying, X must be declared as 0."""
    pass


@scenario(
    "../features/section_5_1_playing_cards.feature",
    "A player declares optional additional costs before paying",
)
def test_declare_optional_additional_cost():
    """Rule 5.1.3b: Optional additional costs must be declared."""
    pass


@scenario(
    "../features/section_5_1_playing_cards.feature",
    "A player may choose not to pay an optional additional cost",
)
def test_decline_optional_additional_cost():
    """Rule 5.1.3b: Optional additional costs may be declined."""
    pass


@scenario(
    "../features/section_5_1_playing_cards.feature",
    "A player declares an alternative cost if using one",
)
def test_declare_alternative_cost():
    """Rule 5.1.3c: Alternative cost must be declared; resource asset-cost starts at zero."""
    pass


@scenario(
    "../features/section_5_1_playing_cards.feature",
    "A player cannot declare two alternative costs simultaneously",
)
def test_cannot_declare_two_alternative_costs():
    """Rule 5.1.3c: Only one alternative cost may be declared at a time."""
    pass


@scenario(
    "../features/section_5_1_playing_cards.feature",
    "A player declares an action card is being played as an instant",
)
def test_declare_action_as_instant():
    """Rule 5.1.3d: When an action card is played as an instant, action cost starts at zero."""
    pass


@scenario(
    "../features/section_5_1_playing_cards.feature",
    "An action card not declared as instant incurs action cost",
)
def test_action_card_without_instant_declaration_incurs_cost():
    """Rule 5.1.3d: Action cards not declared as instant have action cost of 1."""
    pass


@scenario(
    "../features/section_5_1_playing_cards.feature",
    "A player declares the order of multiple effect-costs",
)
def test_declare_effect_cost_order():
    """Rule 5.1.3e: When two or more effect-costs exist, their payment order must be declared."""
    pass


@scenario(
    "../features/section_5_1_playing_cards.feature",
    "An attack card requires a target declaration",
)
def test_attack_requires_target_declaration():
    """Rule 5.1.4b: Attack cards require declaring their target."""
    pass


@scenario(
    "../features/section_5_1_playing_cards.feature",
    "The game state is reversed if a card is determined to be illegal after announce",
)
def test_illegal_card_reverses_game_state():
    """Rule 5.1.5: If a card is illegal to play, the game state is reversed to before announce."""
    pass


@scenario(
    "../features/section_5_1_playing_cards.feature",
    "An illegal play due to illegal target parameters reverses game state",
)
def test_illegal_target_reverses_game_state():
    """Rule 5.1.5: Illegal target parameters cause game state reversal."""
    pass


@scenario(
    "../features/section_5_1_playing_cards.feature",
    "Asset-costs are calculated with set effects applied before increase effects",
)
def test_asset_cost_set_before_increase():
    """Rule 5.1.6a: Set effects apply before increase effects in asset-cost calculation."""
    pass


@scenario(
    "../features/section_5_1_playing_cards.feature",
    "Asset-cost reduction cannot reduce below zero",
)
def test_asset_cost_floor_zero():
    """Rule 5.1.6a: Asset-cost reductions cannot reduce the cost below zero."""
    pass


@scenario(
    "../features/section_5_1_playing_cards.feature",
    "Action asset-cost is zero when playing as instant",
)
def test_action_cost_zero_for_instant():
    """Rule 5.1.6b: Action asset-cost is zero for cards played as instant."""
    pass


@scenario(
    "../features/section_5_1_playing_cards.feature",
    "Action asset-cost is one when playing as a non-instant action",
)
def test_action_cost_one_for_non_instant():
    """Rule 5.1.6b: Action asset-cost is one for action cards not played as instant."""
    pass


@scenario(
    "../features/section_5_1_playing_cards.feature",
    "Declaring an alternative cost sets the resource asset-cost to zero",
)
def test_alternative_cost_sets_resource_cost_to_zero():
    """Rule 5.1.6c: Declaring an alternative cost sets the resource asset-cost to zero."""
    pass


@scenario(
    "../features/section_5_1_playing_cards.feature",
    "If an asset-cost is not paid in full the card cannot be played",
)
def test_unpaid_asset_cost_reverses_game_state():
    """Rule 5.1.7a: Unpaid asset-costs cause game state reversal."""
    pass


@scenario(
    "../features/section_5_1_playing_cards.feature",
    "If an effect-cost cannot be paid in declared order the play is reversed",
)
def test_unpayable_effect_cost_reverses_game_state():
    """Rule 5.1.8a: If an effect-cost cannot be paid, the game state is reversed."""
    pass


@scenario(
    "../features/section_5_1_playing_cards.feature",
    "If a replacement effect modifies an effect-cost and it cannot be paid the card can still be played",
)
def test_replacement_effect_cost_failure_still_allows_play():
    """Rule 5.1.9a: A replacement-modified effect-cost failure does not prevent playing."""
    pass


@scenario(
    "../features/section_5_1_playing_cards.feature",
    "After successfully playing a card the player regains priority",
)
def test_player_regains_priority_after_play():
    """Rule 5.1.10: After the Play step, the card is considered played and priority is regained."""
    pass


# ===== Step Definitions =====


@given("a player has a card in their hand")
def player_has_card_in_hand(game_state):
    """Rule 5.1.1a: Set up a card in the player's hand zone."""
    card = game_state.create_card(name="Hand Card")
    try:
        game_state.player.hand.add_card(card)
        game_state.test_card = card
        game_state.test_card_source_zone = "hand"
    except AttributeError:
        game_state.test_card = card
        game_state.test_card_source_zone = "hand"


@given("a player has a card in their arsenal")
def player_has_card_in_arsenal(game_state):
    """Rule 5.1.1a: Set up a card in the player's arsenal zone."""
    card = game_state.create_card(name="Arsenal Card")
    try:
        game_state.player.arsenal.add_card(card)
        game_state.test_card = card
        game_state.test_card_source_zone = "arsenal"
    except AttributeError:
        game_state.test_card = card
        game_state.test_card_source_zone = "arsenal"


@given("a player has a card in their graveyard")
def player_has_card_in_graveyard(game_state):
    """Rule 5.1.1a: Set up a card in the player's graveyard (invalid play zone)."""
    card = game_state.create_card(name="Graveyard Card")
    try:
        game_state.player.graveyard.add_card(card)
        game_state.test_card = card
        game_state.test_card_source_zone = "graveyard"
    except AttributeError:
        game_state.test_card = card
        game_state.test_card_source_zone = "graveyard"


@when("the player announces the card from their hand")
def player_announces_from_hand(game_state):
    """Rule 5.1.2: Attempt to announce the card from the hand."""
    try:
        result = game_state.player.attempt_play_from_zone(
            game_state.test_card, "hand"
        )
        game_state.announce_result = result
    except AttributeError:
        game_state.announce_result = None


@when("the player announces the card from their arsenal")
def player_announces_from_arsenal(game_state):
    """Rule 5.1.2: Attempt to announce the card from the arsenal."""
    try:
        result = game_state.player.attempt_play_from_zone(
            game_state.test_card, "arsenal"
        )
        game_state.announce_result = result
    except AttributeError:
        game_state.announce_result = None


@when("the player announces the card from their graveyard")
def player_announces_from_graveyard(game_state):
    """Rule 5.1.1a: Attempt to announce the card from the graveyard (should be rejected)."""
    try:
        result = game_state.player.attempt_play_from_zone(
            game_state.test_card, "graveyard"
        )
        game_state.announce_result = result
    except AttributeError:
        game_state.announce_result = None


@then("the card should be accepted as a legal announce location")
def card_accepted_as_legal_location(game_state):
    """Rule 5.1.1a: Hand and arsenal are legal announce locations."""
    try:
        result = game_state.announce_result
        if result is not None:
            assert result.success, (
                "Engine needs: allow announce from hand/arsenal (Rule 5.1.1a)"
            )
        else:
            pytest.fail(
                "Engine needs: attempt_play_from_zone returning a result (Rule 5.1.1a)"
            )
    except AttributeError:
        pytest.fail(
            "Engine needs: PlayResult with success attribute (Rule 5.1.1a)"
        )


@then("the announce should be rejected as an illegal zone")
def announce_rejected_as_illegal_zone(game_state):
    """Rule 5.1.1a: Cards cannot be announced from zones other than hand/arsenal."""
    try:
        result = game_state.announce_result
        if result is not None:
            assert not result.success, (
                "Engine needs: reject announce from graveyard (Rule 5.1.1a)"
            )
        else:
            pytest.fail(
                "Engine needs: attempt_play_from_zone with zone validation (Rule 5.1.1a)"
            )
    except AttributeError:
        pytest.fail(
            "Engine needs: PlayResult zone validation (Rule 5.1.1a)"
        )


@given("a card is controlled by one player but owned by another")
def card_controlled_not_owned(game_state):
    """Rule 5.1.1: Set up a card where controller differs from owner."""
    card = game_state.create_card(name="Borrowed Card")
    game_state.test_card = card
    game_state.card_owner_id = 0
    game_state.card_controller_id = 1


@when("the non-owner attempts to announce the card")
def non_owner_announces_card(game_state):
    """Rule 5.1.1: Non-owner attempts to play a card they don't own."""
    try:
        result = game_state.attempt_play_by_non_owner(
            game_state.test_card,
            owner_id=game_state.card_owner_id,
            controller_id=game_state.card_controller_id,
        )
        game_state.announce_result = result
    except AttributeError:
        game_state.announce_result = None


@then("the announce should be rejected as played by non-owner")
def announce_rejected_non_owner(game_state):
    """Rule 5.1.1: Only the owner can play a card."""
    try:
        result = game_state.announce_result
        if result is not None:
            assert not result.success, (
                "Engine needs: ownership check - only owner can play (Rule 5.1.1)"
            )
        else:
            pytest.fail(
                "Engine needs: attempt_play_by_non_owner with ownership validation (Rule 5.1.1)"
            )
    except AttributeError:
        pytest.fail(
            "Engine needs: ownership validation when playing cards (Rule 5.1.1)"
        )


@given("the stack has no layers")
def stack_has_no_layers(game_state):
    """Rule 5.1.2: Ensure the stack starts empty."""
    try:
        if hasattr(game_state, "stack_zone"):
            game_state.stack_was_empty = len(game_state.stack_zone.cards) == 0
        else:
            game_state.stack_was_empty = True
    except AttributeError:
        game_state.stack_was_empty = True


@when("the player announces the card")
def player_announces_card(game_state):
    """Rule 5.1.2: Announce the card to move it to the stack."""
    try:
        game_state.play_card_to_stack(game_state.test_card, controller_id=0)
        game_state.announce_result = type("Result", (), {"success": True})()
    except Exception as e:
        game_state.announce_result = type("Result", (), {"success": False})()
        game_state.announce_error = str(e)


@then("the card should be on the stack")
def card_should_be_on_stack(game_state):
    """Rule 5.1.2: Card moves to the stack when announced."""
    try:
        stack_zone = game_state.stack_zone
        assert stack_zone is not None, "Engine needs: stack zone (Rule 5.1.2)"
        card_on_stack = game_state.test_card in stack_zone.cards
        assert card_on_stack, (
            "Engine needs: card moves to stack when announced (Rule 5.1.2)"
        )
    except AttributeError:
        pytest.fail(
            "Engine needs: GameState.stack_zone with card tracking (Rule 5.1.2)"
        )


@then("the card should be the topmost layer of the stack")
def card_is_topmost_layer(game_state):
    """Rule 5.1.2: Announced card becomes topmost layer."""
    try:
        stack_zone = game_state.stack_zone
        assert len(stack_zone.cards) >= 1, (
            "Engine needs: stack zone with layers (Rule 5.1.2)"
        )
        top_layer = stack_zone.cards[-1]
        assert top_layer is game_state.test_card, (
            "Engine needs: announced card becomes topmost layer (Rule 5.1.2)"
        )
    except AttributeError:
        pytest.fail(
            "Engine needs: Stack topmost layer tracking (Rule 5.1.2)"
        )


@given("a player has two cards in their hand")
def player_has_two_cards_in_hand(game_state):
    """Rule 5.1.2: Two cards are available for the player to play."""
    card1 = game_state.create_card(name="First Hand Card")
    card2 = game_state.create_card(name="Second Hand Card")
    try:
        game_state.player.hand.add_card(card1)
        game_state.player.hand.add_card(card2)
    except AttributeError:
        pass
    game_state.first_card = card1
    game_state.second_card = card2


@given("the first card has been announced and is on the stack")
def first_card_on_stack(game_state):
    """Rule 5.1.2: The first card is already on the stack."""
    try:
        game_state.play_card_to_stack(game_state.first_card, controller_id=0)
    except Exception:
        pass


@when("the player announces the second card")
def player_announces_second_card(game_state):
    """Rule 5.1.2: The second card is announced."""
    try:
        game_state.play_card_to_stack(game_state.second_card, controller_id=0)
    except Exception:
        pass


@then("the second card should be the topmost layer of the stack")
def second_card_is_topmost(game_state):
    """Rule 5.1.2: The most recently announced card is on top."""
    try:
        stack_zone = game_state.stack_zone
        assert len(stack_zone.cards) >= 2, (
            "Engine needs: multiple layers on stack (Rule 5.1.2)"
        )
        top_layer = stack_zone.cards[-1]
        assert top_layer is game_state.second_card, (
            "Engine needs: most recently announced card is topmost (Rule 5.1.2)"
        )
    except AttributeError:
        pytest.fail(
            "Engine needs: Stack with LIFO ordering (Rule 5.1.2)"
        )


@given("a continuous effect is active that applies to the next attack action card played")
def continuous_effect_active_for_next_attack(game_state):
    """Rule 5.1.2a: A 'next attack action card played' effect is in play."""
    try:
        effect = game_state.create_next_card_played_effect(
            card_type="attack action",
            modifier="power_boost",
            amount=3,
        )
        game_state.next_card_effect = effect
    except AttributeError:
        game_state.next_card_effect = {"type": "next_attack_played", "modifier": "power_boost", "amount": 3}


@when("a player announces an attack action card")
def player_announces_attack_action_card(game_state):
    """Rule 5.1.2a: An attack action card is announced."""
    from fab_engine.cards.model import CardType
    card = game_state.create_card(name="Test Attack", card_type=CardType.ACTION)
    try:
        game_state.play_card_to_stack(card, controller_id=0)
        game_state.test_card = card
        game_state.announced_card_is_attack = True
    except Exception:
        game_state.test_card = card
        game_state.announced_card_is_attack = True


@then("the continuous effect should be applied to the announced card")
def continuous_effect_applied_to_card(game_state):
    """Rule 5.1.2a: Continuous effect applies to matching announced card."""
    try:
        effect_applied = game_state.check_effect_applied_to_card(
            game_state.test_card,
            game_state.next_card_effect,
        )
        assert effect_applied, (
            "Engine needs: apply 'next card played' effects on announce (Rule 5.1.2a)"
        )
    except AttributeError:
        pytest.fail(
            "Engine needs: check_effect_applied_to_card and create_next_card_played_effect (Rule 5.1.2a)"
        )


@when("a player announces a non-attack card")
def player_announces_non_attack_card(game_state):
    """Rule 5.1.2a: A non-attack card is announced."""
    card = game_state.create_card(name="Test Non-Attack")
    try:
        game_state.play_card_to_stack(card, controller_id=0)
        game_state.test_card = card
        game_state.announced_card_is_attack = False
    except Exception:
        game_state.test_card = card
        game_state.announced_card_is_attack = False


@then("the continuous effect should not be applied to the announced card")
def continuous_effect_not_applied_to_card(game_state):
    """Rule 5.1.2a: Continuous effect does not apply to non-matching card type."""
    try:
        effect_applied = game_state.check_effect_applied_to_card(
            game_state.test_card,
            game_state.next_card_effect,
        )
        assert not effect_applied, (
            "Engine needs: do not apply 'next attack card' effect to non-attack cards (Rule 5.1.2a)"
        )
    except AttributeError:
        pytest.fail(
            "Engine needs: check_effect_applied_to_card for type-filtered effects (Rule 5.1.2a)"
        )


@given("a card has a play restriction that prevents it from being played")
def card_with_play_restriction(game_state):
    """Rule 5.1.2b: A card that cannot be announced due to restriction."""
    card = game_state.create_card(name="Restricted Card")
    try:
        game_state.player.hand.add_card(card)
        game_state.player.add_restriction("cannot_play_restricted_card")
    except AttributeError:
        pass
    game_state.test_card = card
    game_state.test_card_has_play_restriction = True


@when("the player attempts to announce that card")
def player_attempts_announce_restricted_card(game_state):
    """Rule 5.1.2b: Attempt to announce a card with a play restriction."""
    try:
        result = game_state.player.attempt_play_from_zone(
            game_state.test_card, "hand"
        )
        game_state.announce_result = result
    except AttributeError:
        game_state.announce_result = None


@then("the announce should be rejected")
def announce_rejected(game_state):
    """Rule 5.1.2b: Cards with play restrictions cannot be announced."""
    try:
        result = game_state.announce_result
        if result is not None:
            assert not result.success, (
                "Engine needs: reject announce when play restriction exists (Rule 5.1.2b)"
            )
        else:
            pytest.fail(
                "Engine needs: play restriction checking during announce (Rule 5.1.2b)"
            )
    except AttributeError:
        pytest.fail(
            "Engine needs: PlayResult with rejection for restricted cards (Rule 5.1.2b)"
        )


@given("a player has a card with a variable cost including X")
def player_has_variable_cost_card(game_state):
    """Rule 5.1.3a: A card with variable cost X is in the player's hand."""
    card = game_state.create_card(name="Variable Cost Card")
    game_state.test_card = card
    game_state.test_card_has_variable_x = True


@when("the player announces the card and declares X as 3")
def player_declares_x_as_3(game_state):
    """Rule 5.1.3a: Player declares X=3 when announcing the variable cost card."""
    try:
        result = game_state.announce_card_with_variable_x(
            game_state.test_card,
            x_value=3,
        )
        game_state.announce_result = result
        game_state.declared_x_value = 3
    except AttributeError:
        game_state.declared_x_value = 3
        game_state.announce_result = None


@then("X should be recorded as 3 for the card's cost calculation")
def x_recorded_as_3(game_state):
    """Rule 5.1.3a: The declared X value is used in cost calculation."""
    try:
        recorded_x = game_state.get_declared_x_value(game_state.test_card)
        assert recorded_x == 3, (
            f"Engine needs: record declared X value for variable cost cards (Rule 5.1.3a), got {recorded_x}"
        )
    except AttributeError:
        pytest.fail(
            "Engine needs: variable cost X declaration and tracking (Rule 5.1.3a)"
        )


@given("an effect allows the player to play the card without paying its cost")
def effect_allows_free_play(game_state):
    """Rule 5.1.3a: An effect that allows playing a card without paying its cost."""
    try:
        effect = game_state.create_free_play_effect(game_state.test_card)
        game_state.free_play_effect = effect
    except AttributeError:
        game_state.free_play_effect = {"type": "free_play"}


@when("the player announces the card using the effect")
def player_announces_using_free_play_effect(game_state):
    """Rule 5.1.3a: Player announces a card using a free play effect."""
    try:
        result = game_state.announce_card_with_free_play_effect(
            game_state.test_card,
            game_state.free_play_effect,
        )
        game_state.announce_result = result
    except AttributeError:
        game_state.announce_result = None


@then("X must be declared as 0")
def x_must_be_zero_for_free_play(game_state):
    """Rule 5.1.3a: When playing without paying cost, X must be 0."""
    try:
        recorded_x = game_state.get_declared_x_value(game_state.test_card)
        assert recorded_x == 0, (
            f"Engine needs: force X=0 when playing without paying cost (Rule 5.1.3a), got {recorded_x}"
        )
    except AttributeError:
        pytest.fail(
            "Engine needs: X=0 rule when playing without paying variable cost (Rule 5.1.3a)"
        )


@given("a player has a card with an optional additional cost")
def player_has_card_with_optional_additional_cost(game_state):
    """Rule 5.1.3b: A card with an optional additional cost is set up."""
    card = game_state.create_card(name="Optional Cost Card")
    game_state.test_card = card
    game_state.test_card_has_optional_cost = True
    try:
        game_state.test_card_optional_cost = game_state.get_optional_additional_cost(card)
    except AttributeError:
        game_state.test_card_optional_cost = "discard_a_card"


@when("the player announces the card and declares the optional cost will be paid")
def player_declares_optional_cost_paid(game_state):
    """Rule 5.1.3b: Player declares they will pay the optional additional cost."""
    try:
        result = game_state.announce_card_with_optional_cost_declared(
            game_state.test_card,
            pay_optional_cost=True,
        )
        game_state.announce_result = result
        game_state.optional_cost_declared = True
    except AttributeError:
        game_state.optional_cost_declared = True
        game_state.announce_result = None


@then("the optional additional cost should be recorded as declared")
def optional_cost_recorded(game_state):
    """Rule 5.1.3b: The optional cost is tracked as declared."""
    try:
        cost_recorded = game_state.is_optional_cost_declared(game_state.test_card)
        assert cost_recorded, (
            "Engine needs: track optional additional cost declarations (Rule 5.1.3b)"
        )
    except AttributeError:
        pytest.fail(
            "Engine needs: optional additional cost declaration tracking (Rule 5.1.3b)"
        )


@when("the player announces the card and declares the optional cost will not be paid")
def player_declares_optional_cost_not_paid(game_state):
    """Rule 5.1.3b: Player declares they will NOT pay the optional additional cost."""
    try:
        result = game_state.announce_card_with_optional_cost_declared(
            game_state.test_card,
            pay_optional_cost=False,
        )
        game_state.announce_result = result
        game_state.optional_cost_declined = True
    except AttributeError:
        game_state.optional_cost_declined = True
        game_state.announce_result = None


@then("the optional additional cost should not be required")
def optional_cost_not_required(game_state):
    """Rule 5.1.3b: Declining an optional cost means it is not required."""
    try:
        cost_required = game_state.is_optional_cost_required(game_state.test_card)
        assert not cost_required, (
            "Engine needs: optional cost that can be declined is not required (Rule 5.1.3b)"
        )
    except AttributeError:
        pytest.fail(
            "Engine needs: optional additional cost required check (Rule 5.1.3b)"
        )


@given("a player has a card with an alternative cost")
def player_has_card_with_alternative_cost(game_state):
    """Rule 5.1.3c: A card with an alternative cost is available."""
    card = game_state.create_card(name="Alternative Cost Card")
    game_state.test_card = card
    game_state.test_card_has_alternative_cost = True


@when("the player announces the card and declares the alternative cost will be used")
def player_declares_alternative_cost(game_state):
    """Rule 5.1.3c: Player declares using the alternative cost."""
    try:
        result = game_state.announce_card_with_alternative_cost(
            game_state.test_card,
            use_alternative_cost=True,
        )
        game_state.announce_result = result
        game_state.alternative_cost_declared = True
    except AttributeError:
        game_state.alternative_cost_declared = True
        game_state.announce_result = None


@then("the resource asset-cost should start at zero")
def resource_cost_starts_at_zero(game_state):
    """Rule 5.1.3c / 5.1.6c: Alternative cost sets resource asset-cost to zero."""
    try:
        resource_cost = game_state.get_starting_resource_cost(game_state.test_card)
        assert resource_cost == 0, (
            f"Engine needs: resource asset-cost starts at 0 when alternative cost declared (Rule 5.1.6c), got {resource_cost}"
        )
    except AttributeError:
        pytest.fail(
            "Engine needs: resource asset-cost calculation with alternative cost (Rule 5.1.6c)"
        )


@given("a player has a card with two alternative costs")
def player_has_card_with_two_alternative_costs(game_state):
    """Rule 5.1.3c: A card with two alternative costs is available."""
    card = game_state.create_card(name="Double Alternative Card")
    game_state.test_card = card
    game_state.test_card_has_two_alternative_costs = True


@when("the player attempts to declare both alternative costs simultaneously")
def player_declares_both_alternative_costs(game_state):
    """Rule 5.1.3c: Attempting to use two alternative costs at once."""
    try:
        result = game_state.announce_card_with_multiple_alternative_costs(
            game_state.test_card,
            alternative_costs=["alt_cost_1", "alt_cost_2"],
        )
        game_state.declare_two_alts_result = result
    except AttributeError:
        game_state.declare_two_alts_result = None


@then("only one alternative cost declaration should be accepted")
def only_one_alternative_cost_accepted(game_state):
    """Rule 5.1.3c: Only one alternative cost may be declared."""
    try:
        result = game_state.declare_two_alts_result
        if result is not None:
            assert not result.success or result.only_one_used, (
                "Engine needs: reject declaring two alternative costs at once (Rule 5.1.3c)"
            )
        else:
            pytest.fail(
                "Engine needs: validation for multiple alternative cost declarations (Rule 5.1.3c)"
            )
    except AttributeError:
        pytest.fail(
            "Engine needs: alternative cost mutual exclusivity enforcement (Rule 5.1.3c)"
        )


@given("a player has an action card that may be played as an instant")
def player_has_action_card_playable_as_instant(game_state):
    """Rule 5.1.3d: An action card with 'may be played as an instant' ability is set up."""
    from fab_engine.cards.model import CardType
    card = game_state.create_card(name="Instant Action Card", card_type=CardType.ACTION)
    game_state.test_card = card
    game_state.test_card_can_be_instant = True


@when("the player announces the card and declares it is being played as an instant")
def player_declares_instant_play(game_state):
    """Rule 5.1.3d: Player declares the action card is being played as an instant."""
    try:
        result = game_state.announce_action_as_instant(
            game_state.test_card,
            as_instant=True,
        )
        game_state.announce_result = result
        game_state.card_played_as_instant = True
    except AttributeError:
        game_state.card_played_as_instant = True
        game_state.announce_result = None


@then("the action cost should start at zero")
def action_cost_starts_at_zero(game_state):
    """Rule 5.1.6b: Action asset-cost is 0 when played as instant."""
    try:
        action_cost = game_state.get_action_asset_cost(game_state.test_card)
        assert action_cost == 0, (
            f"Engine needs: action cost=0 for instant plays (Rule 5.1.6b), got {action_cost}"
        )
    except AttributeError:
        pytest.fail(
            "Engine needs: get_action_asset_cost returning 0 for instants (Rule 5.1.6b)"
        )


@when("the player announces the card without declaring instant play")
def player_announces_without_instant_declaration(game_state):
    """Rule 5.1.3d: Player announces action card without instant declaration."""
    try:
        result = game_state.announce_action_as_instant(
            game_state.test_card,
            as_instant=False,
        )
        game_state.announce_result = result
        game_state.card_played_as_instant = False
    except AttributeError:
        game_state.card_played_as_instant = False
        game_state.announce_result = None


@then("the action cost should start at one")
def action_cost_starts_at_one(game_state):
    """Rule 5.1.6b: Action asset-cost is 1 when played as non-instant action."""
    try:
        action_cost = game_state.get_action_asset_cost(game_state.test_card)
        assert action_cost == 1, (
            f"Engine needs: action cost=1 for non-instant action plays (Rule 5.1.6b), got {action_cost}"
        )
    except AttributeError:
        pytest.fail(
            "Engine needs: get_action_asset_cost returning 1 for non-instant actions (Rule 5.1.6b)"
        )


@given("a player has a card with two effect-costs")
def player_has_card_with_two_effect_costs(game_state):
    """Rule 5.1.3e: A card with two effect-costs is set up."""
    try:
        card = game_state.create_ability_with_two_effect_costs(
            cost1="discard_a_card",
            cost2="lose_1_life",
        )
        game_state.test_card = card
    except AttributeError:
        card = game_state.create_card(name="Two Effect Cost Card")
        game_state.test_card = card
    game_state.test_card_has_two_effect_costs = True


@when("the player announces the card and declares the order of effect-costs")
def player_declares_effect_cost_order(game_state):
    """Rule 5.1.3e: Player declares the order in which effect-costs will be paid."""
    try:
        result = game_state.declare_effect_cost_order(
            game_state.test_card,
            order=["discard_a_card", "lose_1_life"],
        )
        game_state.effect_cost_order_result = result
        game_state.declared_effect_cost_order = ["discard_a_card", "lose_1_life"]
    except AttributeError:
        game_state.declared_effect_cost_order = ["discard_a_card", "lose_1_life"]
        game_state.effect_cost_order_result = None


@then("the declared order should be recorded for effect-cost payment")
def effect_cost_order_recorded(game_state):
    """Rule 5.1.3e: The declared effect-cost order is tracked."""
    try:
        recorded_order = game_state.get_effect_cost_order(game_state.test_card)
        assert recorded_order is not None, (
            "Engine needs: track effect-cost payment order (Rule 5.1.3e)"
        )
        assert len(recorded_order) == 2, (
            "Engine needs: both effect-costs in order record (Rule 5.1.3e)"
        )
    except AttributeError:
        pytest.fail(
            "Engine needs: effect-cost ordering declaration and tracking (Rule 5.1.3e)"
        )


@given("a player has an attack action card")
def player_has_attack_action_card(game_state):
    """Rule 5.1.4b: An attack action card is in the player's hand."""
    from fab_engine.cards.model import CardType
    card = game_state.create_card(name="Attack Card", card_type=CardType.ACTION)
    try:
        game_state.player.hand.add_card(card)
    except AttributeError:
        pass
    game_state.test_card = card
    game_state.test_card_is_attack = True


@when("the player announces the attack card")
def player_announces_attack_card(game_state):
    """Rule 5.1.4b: Player announces an attack card."""
    try:
        result = game_state.announce_attack_card(game_state.test_card)
        game_state.announce_attack_result = result
    except AttributeError:
        game_state.announce_attack_result = None


@then("the player must declare an attack target")
def player_must_declare_attack_target(game_state):
    """Rule 5.1.4b: Attack cards require target declaration."""
    try:
        target_required = game_state.is_attack_target_required(game_state.test_card)
        assert target_required, (
            "Engine needs: require attack target declaration for attack cards (Rule 5.1.4b)"
        )
    except AttributeError:
        pytest.fail(
            "Engine needs: is_attack_target_required for attack card validation (Rule 5.1.4b)"
        )


@given("a rule prevents the card from being played")
def rule_prevents_card_play(game_state):
    """Rule 5.1.5: A rule or effect prevents the card from being played."""
    try:
        game_state.player.add_restriction("cannot_play_any_card")
        game_state.play_is_prevented = True
    except AttributeError:
        game_state.play_is_prevented = True


@when("the player attempts to announce the card")
def player_attempts_to_announce(game_state):
    """Rule 5.1.5: Player attempts to announce a card with a restriction."""
    try:
        result = game_state.player.attempt_play_from_zone(
            game_state.test_card, "hand"
        )
        game_state.announce_result = result
    except AttributeError:
        game_state.announce_result = None


@then("the card should remain in the player's hand")
def card_remains_in_hand(game_state):
    """Rule 5.1.5: If play is illegal, card remains in hand (game state reversed)."""
    try:
        hand_zone = game_state.player.hand
        card_in_hand = game_state.test_card in hand_zone.cards
        assert card_in_hand, (
            "Engine needs: reverse game state - card stays in hand if play is illegal (Rule 5.1.5)"
        )
    except AttributeError:
        pytest.fail(
            "Engine needs: game state reversal keeping card in hand (Rule 5.1.5)"
        )


@then("the stack should be empty")
def stack_should_be_empty(game_state):
    """Rule 5.1.5: Game state reversal means the stack is empty after illegal play attempt."""
    try:
        stack_zone = game_state.stack_zone
        assert len(stack_zone.cards) == 0, (
            "Engine needs: game state reversal empties stack on illegal play (Rule 5.1.5)"
        )
    except AttributeError:
        pytest.fail(
            "Engine needs: stack zone with game state reversal support (Rule 5.1.5)"
        )


@given("a player has a card that requires a valid target")
def player_has_card_requiring_target(game_state):
    """Rule 5.1.5: A card that requires a valid target."""
    card = game_state.create_card(name="Target Required Card")
    try:
        game_state.player.hand.add_card(card)
    except AttributeError:
        pass
    game_state.test_card = card
    game_state.test_card_requires_target = True


@given("there are no valid targets available")
def no_valid_targets(game_state):
    """Rule 5.1.5: No valid targets exist for the card."""
    game_state.valid_targets_exist = False
    try:
        game_state.clear_valid_targets()
    except AttributeError:
        pass


@when("the player announces the card")
def player_announces_target_required_card(game_state):
    """Rule 5.1.5: Player announces a card that requires a target."""
    try:
        result = game_state.announce_card_with_no_valid_targets(game_state.test_card)
        game_state.announce_result = result
    except AttributeError:
        game_state.announce_result = None


@then("the game state is reversed to before the announce")
def game_state_reversed(game_state):
    """Rule 5.1.5: Game state is reversed when play is determined illegal."""
    try:
        result = game_state.announce_result
        if result is not None:
            assert not result.success, (
                "Engine needs: game state reversal when no valid targets (Rule 5.1.5)"
            )
        else:
            pytest.fail(
                "Engine needs: game state reversal for illegal announce (Rule 5.1.5)"
            )
    except AttributeError:
        pytest.fail(
            "Engine needs: game state reversal mechanism (Rule 5.1.5)"
        )


@given("a card has a base resource cost of {cost:d}")
def card_has_base_resource_cost(game_state, cost):
    """Rule 5.1.6: Set up a card with a specific base resource cost."""
    try:
        card = game_state.create_card_with_resource_cost(resource_cost=cost)
        game_state.test_card = card
        game_state.base_resource_cost = cost
    except AttributeError:
        card = game_state.create_card(name=f"Cost {cost} Card")
        game_state.test_card = card
        game_state.base_resource_cost = cost


@given("an effect sets the resource cost to {cost:d}")
def effect_sets_resource_cost(game_state, cost):
    """Rule 5.1.6a: An effect that sets the resource cost to a specific value."""
    try:
        effect = game_state.create_cost_set_effect(
            game_state.test_card,
            new_cost=cost,
            timestamp=1,
        )
        game_state.cost_set_effect = effect
        game_state.cost_after_set = cost
    except AttributeError:
        game_state.cost_after_set = cost


@given("an effect increases the resource cost by {amount:d}")
def effect_increases_resource_cost(game_state, amount):
    """Rule 5.1.6a: An effect that increases the resource cost by a specific amount."""
    try:
        effect = game_state.create_cost_increase_effect(
            game_state.test_card,
            increase=amount,
            timestamp=2,
        )
        game_state.cost_increase_effect = effect
        game_state.cost_increase_amount = amount
    except AttributeError:
        game_state.cost_increase_amount = amount


@when("asset-costs are calculated")
def asset_costs_calculated(game_state):
    """Rule 5.1.6: Trigger the asset-cost calculation process."""
    try:
        result = game_state.calculate_asset_costs(game_state.test_card)
        game_state.asset_cost_result = result
    except AttributeError:
        game_state.asset_cost_result = None


@then("the final resource cost should be {expected:d}")
def final_resource_cost_is(game_state, expected):
    """Rule 5.1.6a: The final resource cost matches the expected value."""
    try:
        result = game_state.asset_cost_result
        if result is not None:
            actual = result.resource_cost
            assert actual == expected, (
                f"Engine needs: correct asset-cost calculation order (Rule 5.1.6a), "
                f"expected {expected}, got {actual}"
            )
        else:
            pytest.fail(
                "Engine needs: calculate_asset_costs returning AssetCostResult (Rule 5.1.6a)"
            )
    except AttributeError:
        pytest.fail(
            "Engine needs: AssetCostResult.resource_cost property (Rule 5.1.6a)"
        )


@given("an effect reduces the resource cost by {amount:d}")
def effect_reduces_resource_cost(game_state, amount):
    """Rule 5.1.6a: An effect that reduces the resource cost."""
    try:
        effect = game_state.create_cost_reduction_effect(reduction=amount)
        game_state.cost_reduction_effect = effect
        game_state.cost_reduction_amount = amount
    except AttributeError:
        game_state.cost_reduction_amount = amount


@given("a player has an action card")
def player_has_action_card(game_state):
    """Rule 5.1.6b: An action card is in the player's hand."""
    from fab_engine.cards.model import CardType
    card = game_state.create_card(name="Action Card", card_type=CardType.ACTION)
    try:
        game_state.player.hand.add_card(card)
    except AttributeError:
        pass
    game_state.test_card = card


@given("the player declares they are playing it as an instant")
def player_declares_as_instant(game_state):
    """Rule 5.1.6b: Player has declared to play the action card as an instant."""
    try:
        game_state.set_card_play_as_instant(game_state.test_card, as_instant=True)
        game_state.card_playing_as_instant = True
    except AttributeError:
        game_state.card_playing_as_instant = True


@given("the player declares they are NOT playing it as an instant")
def player_declares_not_as_instant(game_state):
    """Rule 5.1.6b: Player has declared to NOT play the action card as an instant."""
    try:
        game_state.set_card_play_as_instant(game_state.test_card, as_instant=False)
        game_state.card_playing_as_instant = False
    except AttributeError:
        game_state.card_playing_as_instant = False


@when("the action asset-cost is calculated")
def action_asset_cost_calculated(game_state):
    """Rule 5.1.6b: Calculate the action asset-cost."""
    try:
        result = game_state.calculate_action_asset_cost(game_state.test_card)
        game_state.action_asset_cost_result = result
    except AttributeError:
        game_state.action_asset_cost_result = None


@then("the action asset-cost should be {expected:d}")
def action_asset_cost_is(game_state, expected):
    """Rule 5.1.6b: The action asset-cost matches the expected value."""
    try:
        result = game_state.action_asset_cost_result
        if result is not None:
            actual = result.action_cost
            assert actual == expected, (
                f"Engine needs: correct action asset-cost (Rule 5.1.6b), "
                f"expected {expected}, got {actual}"
            )
        else:
            pytest.fail(
                "Engine needs: calculate_action_asset_cost method (Rule 5.1.6b)"
            )
    except AttributeError:
        pytest.fail(
            "Engine needs: ActionAssetCostResult.action_cost property (Rule 5.1.6b)"
        )


@given("a player has a card with a base resource cost of {cost:d}")
def player_has_card_with_resource_cost(game_state, cost):
    """Rule 5.1.6c: Set up a card with a specific base resource cost."""
    try:
        card = game_state.create_card_with_resource_cost(resource_cost=cost)
        game_state.test_card = card
        game_state.base_resource_cost = cost
    except AttributeError:
        card = game_state.create_card(name=f"Resource Cost {cost} Card")
        game_state.test_card = card
        game_state.base_resource_cost = cost


@given("the player declares an alternative cost that replaces the resource asset-cost")
def player_declares_alternative_cost_replacing_resource(game_state):
    """Rule 5.1.6c: Player declares an alternative cost replacing the resource cost."""
    try:
        game_state.declare_alternative_cost_for_card(
            game_state.test_card,
            replaces_resource_cost=True,
        )
        game_state.alternative_cost_replaces_resource = True
    except AttributeError:
        game_state.alternative_cost_replaces_resource = True


@when("the resource asset-cost is calculated")
def resource_asset_cost_calculated(game_state):
    """Rule 5.1.6c: Calculate the resource asset-cost."""
    try:
        result = game_state.calculate_resource_asset_cost(game_state.test_card)
        game_state.resource_cost_result = result
    except AttributeError:
        game_state.resource_cost_result = None


@then("the resource asset-cost should start at zero")
def resource_asset_cost_starts_at_zero(game_state):
    """Rule 5.1.6c: Resource asset-cost is 0 when alternative cost is declared."""
    try:
        result = game_state.resource_cost_result
        if result is not None:
            actual = result.resource_cost
            assert actual == 0, (
                f"Engine needs: resource cost=0 when alternative cost declared (Rule 5.1.6c), got {actual}"
            )
        else:
            pytest.fail(
                "Engine needs: calculate_resource_asset_cost method (Rule 5.1.6c)"
            )
    except AttributeError:
        pytest.fail(
            "Engine needs: ResourceAssetCostResult.resource_cost property (Rule 5.1.6c)"
        )


@given("a player has a card with a resource cost of {cost:d}")
def player_has_card_with_specific_resource_cost(game_state, cost):
    """Rule 5.1.7a: A card with a specific resource cost is set up."""
    try:
        card = game_state.create_card_with_resource_cost(resource_cost=cost)
        game_state.test_card = card
        game_state.required_resource_cost = cost
    except AttributeError:
        card = game_state.create_card(name=f"Costs {cost} Card")
        game_state.test_card = card
        game_state.required_resource_cost = cost


@given("the player only has {amount:d} resource available")
def player_has_limited_resources(game_state, amount):
    """Rule 5.1.7a: Player has insufficient resources to pay the cost."""
    try:
        game_state.set_player_resources(player_id=0, resources=amount)
        game_state.player_resources_available = amount
    except AttributeError:
        game_state.player_resources_available = amount


@when("the player attempts to pay the asset-costs")
def player_attempts_to_pay_asset_costs(game_state):
    """Rule 5.1.7a: Player attempts to pay asset-costs with insufficient resources."""
    try:
        result = game_state.attempt_card_play_1_14(game_state.test_card)
        game_state.play_attempt_result = result
    except AttributeError:
        game_state.play_attempt_result = None


@then("the card play should fail")
def card_play_should_fail(game_state):
    """Rule 5.1.7a / 5.1.8a: The card play fails due to unpaid costs."""
    try:
        result = game_state.play_attempt_result
        if result is not None:
            assert not result.success, (
                "Engine needs: fail card play when costs cannot be paid (Rule 5.1.7a)"
            )
        else:
            pytest.fail(
                "Engine needs: play attempt result with success tracking (Rule 5.1.7a)"
            )
    except AttributeError:
        pytest.fail(
            "Engine needs: play attempt result tracking (Rule 5.1.7a)"
        )


@then("the game state should be reversed to before the announce")
def game_state_reversed_after_failed_asset_cost(game_state):
    """Rule 5.1.7a: Game state is reversed when asset-cost cannot be paid."""
    try:
        is_reversed = game_state.was_game_state_reversed()
        assert is_reversed, (
            "Engine needs: game state reversal when asset-costs unpaid (Rule 5.1.7a)"
        )
    except AttributeError:
        pytest.fail(
            "Engine needs: was_game_state_reversed() method (Rule 5.1.7a)"
        )


@given("a player has a card with an effect-cost that cannot be paid")
def player_has_card_with_unpayable_effect_cost(game_state):
    """Rule 5.1.8a: A card with an unpayable effect-cost."""
    card = game_state.create_card(name="Unpayable Effect Cost Card")
    game_state.test_card = card
    game_state.test_card_effect_cost_unpayable = True


@when("the player attempts to calculate effect-costs")
def player_attempts_effect_cost_calculation(game_state):
    """Rule 5.1.8a: Player tries to calculate effect-costs."""
    try:
        result = game_state.calculate_effect_costs_for_card(game_state.test_card)
        game_state.effect_cost_result = result
    except AttributeError:
        game_state.effect_cost_result = None


@given("a player has a card with an effect-cost")
def player_has_card_with_effect_cost(game_state):
    """Rule 5.1.9a: A card with an effect-cost is set up."""
    try:
        card = game_state.create_ability_with_effect_cost(effect="discard_a_card")
        game_state.test_card = card
    except AttributeError:
        card = game_state.create_card(name="Effect Cost Card")
        game_state.test_card = card


@given("a replacement effect modifies the effect-cost")
def replacement_effect_modifies_effect_cost(game_state):
    """Rule 5.1.9a: A replacement effect changes how the effect-cost is paid."""
    try:
        replacement = game_state.create_replacement_effect(
            replaces="discard_a_card",
            with_effect="lose_3_life",
        )
        game_state.replacement_effect = replacement
    except AttributeError:
        game_state.replacement_effect = {"replaces": "discard", "with": "life_cost"}


@given("the modified effect-cost cannot be paid")
def modified_effect_cost_cannot_be_paid(game_state):
    """Rule 5.1.9a: The replacement effect creates an unpayable effect-cost."""
    try:
        game_state.set_player_life(player_id=0, life=0)
        game_state.modified_cost_unpayable = True
    except AttributeError:
        game_state.modified_cost_unpayable = True


@when("the player pays effect-costs")
def player_pays_effect_costs(game_state):
    """Rule 5.1.9a: Player attempts to pay effect-costs with replacement effect active."""
    try:
        result = game_state.pay_effect_costs_with_replacement(
            game_state.test_card,
            game_state.replacement_effect,
        )
        game_state.effect_cost_pay_result = result
    except AttributeError:
        game_state.effect_cost_pay_result = None


@then("the card play should still succeed")
def card_play_should_succeed(game_state):
    """Rule 5.1.9a: Despite replaced effect-cost failure, card play succeeds."""
    try:
        result = game_state.effect_cost_pay_result
        if result is not None:
            assert result.success, (
                "Engine needs: allow card play when replacement effect-cost fails (Rule 5.1.9a)"
            )
        else:
            pytest.fail(
                "Engine needs: pay_effect_costs_with_replacement method (Rule 5.1.9a)"
            )
    except AttributeError:
        pytest.fail(
            "Engine needs: replacement effect on effect-cost failure handling (Rule 5.1.9a)"
        )


@when("the player successfully completes all steps to play the card")
def player_completes_all_play_steps(game_state):
    """Rule 5.1.10: All play steps are completed successfully."""
    card = game_state.create_card(name="Successfully Played Card")
    try:
        game_state.player.hand.add_card(card)
    except AttributeError:
        pass
    game_state.test_card = card
    try:
        result = game_state.complete_card_play(card, player_id=0)
        game_state.play_completion_result = result
    except AttributeError:
        game_state.play_completion_result = None


@then("the card should be considered played")
def card_considered_played(game_state):
    """Rule 5.1.10: After the Play step, the card is considered played."""
    try:
        is_played = game_state.is_card_considered_played(game_state.test_card)
        assert is_played, (
            "Engine needs: track cards as 'considered played' after Play step (Rule 5.1.10)"
        )
    except AttributeError:
        pytest.fail(
            "Engine needs: is_card_considered_played tracking (Rule 5.1.10)"
        )


@then("the player should regain priority")
def player_regains_priority(game_state):
    """Rule 5.1.10: After the Play step, the player regains priority."""
    try:
        has_priority = game_state.does_player_have_priority(player_id=0)
        assert has_priority, (
            "Engine needs: player regains priority after Play step (Rule 5.1.10)"
        )
    except AttributeError:
        pytest.fail(
            "Engine needs: does_player_have_priority tracking (Rule 5.1.10)"
        )


# ===== Fixtures =====


@pytest.fixture
def game_state():
    """
    Fixture providing game state for testing Section 5.1: Playing Cards.

    Uses BDDGameState which integrates with the real engine.
    Reference: Rule 5.1 - Playing Cards
    """
    from tests.bdd_helpers import BDDGameState

    state = BDDGameState()

    # Track announce results and play outcomes
    state.announce_result = None
    state.play_attempt_result = None
    state.test_card = None
    state.test_card_source_zone = None

    return state
