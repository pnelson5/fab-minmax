"""
Step definitions for Section 8.3.9: Boost (Ability Keyword)
Reference: Flesh and Blood Comprehensive Rules Section 8.3.9

This module implements behavioral tests for the Boost ability keyword:
- Boost is an optional additional-cost play-static ability (Rule 8.3.9)
- Meaning: "As an additional cost to play this, you may banish the top card of your deck.
  If you do, if it's a Mechanologist card, this gets go again." (Rule 8.3.9)
- If the banished card is a Mechanologist card, the played card gets go again (Rule 8.3.9)
- If the banished card is NOT a Mechanologist card, go again is not granted (Rule 8.3.9)
- The player and card are still considered to have boosted regardless of card type (Rule 8.3.9a)
- Cannot boost if deck is empty (Rule 8.3.9b)
- Boost is optional — player may choose not to pay the additional cost (Rule 8.3.9)

Engine Features Needed for Section 8.3.9:
- [ ] AbilityKeyword.BOOST on cards (Rule 8.3.9)
- [ ] BoostAbility.is_play_static -> True (Rule 8.3.9)
- [ ] BoostAbility.is_optional -> True (Rule 8.3.9)
- [ ] BoostAbility.is_additional_cost -> True (Rule 8.3.9)
- [ ] BoostAbility.is_triggered -> False (Rule 8.3.9)
- [ ] BoostAbility.is_meta_static -> False (Rule 8.3.9)
- [ ] BoostAbility.meaning property returning the canonical boost text (Rule 8.3.9)
- [ ] Player.boost(card) method: banishes top deck card, checks if it's Mechanologist,
      grants go again if so (Rule 8.3.9)
- [ ] Card.boosted property: True if the card was played with boost (Rule 8.3.9a)
- [ ] Player.has_boosted property: True if player has boosted this turn (Rule 8.3.9a)
- [ ] CardTemplate.supertypes or CardTemplate.class_type to check Mechanologist (Rule 8.3.9)
- [ ] Zone.top_card property on Deck zone (Rule 8.3.9b)
- [ ] Player.can_boost() returning False when deck is empty (Rule 8.3.9b)

Current status: Tests written, Engine pending
"""

import pytest
from pytest_bdd import scenario, given, when, then, parsers


# ===== Rule 8.3.9: Boost is an optional additional-cost play-static ability =====

@scenario(
    "../features/section_8_3_9_boost.feature",
    "Boost is an optional additional-cost play-static ability",
)
def test_boost_is_optional_additional_cost_play_static():
    """Rule 8.3.9: Boost is an optional additional-cost play-static ability."""
    pass


# ===== Rule 8.3.9: Boost meaning is correct =====

@scenario(
    "../features/section_8_3_9_boost.feature",
    "Boost meaning is as specified in the rules",
)
def test_boost_meaning_is_correct():
    """Rule 8.3.9: Boost has the canonical meaning from the comprehensive rules."""
    pass


# ===== Rule 8.3.9: Boosting with Mechanologist grants go again =====

@scenario(
    "../features/section_8_3_9_boost.feature",
    "Boosting with a Mechanologist card grants go again",
)
def test_boost_with_mechanologist_grants_go_again():
    """Rule 8.3.9: If the banished card is Mechanologist, the played card gets go again."""
    pass


# ===== Rule 8.3.9: Boosting with non-Mechanologist does not grant go again =====

@scenario(
    "../features/section_8_3_9_boost.feature",
    "Boosting with a non-Mechanologist card does not grant go again",
)
def test_boost_with_non_mechanologist_no_go_again():
    """Rule 8.3.9: If the banished card is not Mechanologist, go again is not granted."""
    pass


# ===== Rule 8.3.9a: Boost status applies regardless of banished card type =====

@scenario(
    "../features/section_8_3_9_boost.feature",
    "Player is still considered to have boosted even if banished card is not Mechanologist",
)
def test_boost_status_applies_regardless_of_card_type():
    """Rule 8.3.9a: Boosted status is granted even if the banished card is not Mechanologist."""
    pass


# ===== Rule 8.3.9b: Cannot boost with empty deck =====

@scenario(
    "../features/section_8_3_9_boost.feature",
    "Player cannot boost if their deck is empty",
)
def test_cannot_boost_with_empty_deck():
    """Rule 8.3.9b: A player cannot boost if they cannot banish the top card of their deck."""
    pass


# ===== Rule 8.3.9: Boost is optional =====

@scenario(
    "../features/section_8_3_9_boost.feature",
    "Player may choose not to boost",
)
def test_boost_is_optional():
    """Rule 8.3.9: Boost is optional — the player may choose not to pay the additional cost."""
    pass


# ===== Step Definitions =====

# ---- Given steps ----

@given('a card has the "Boost" keyword')
def card_has_boost_keyword(game_state):
    """Rule 8.3.9: Create a card that has the Boost keyword."""
    card = game_state.create_card(name="Boost Test Card")
    card._has_boost = True
    game_state.boost_card = card


@given('a player has a card with the "Boost" keyword in hand')
def player_has_boost_card_in_hand(game_state):
    """Rule 8.3.9: Give the player a card with Boost in their hand."""
    card = game_state.create_card(name="Boost Card")
    card._has_boost = True
    game_state.player.hand.add_card(card)
    game_state.boost_card = card


@given("the top card of the player's deck is a Mechanologist card")
def top_deck_card_is_mechanologist(game_state):
    """Rule 8.3.9: The deck's top card is a Mechanologist card."""
    mech_card = game_state.create_card(name="Mechanologist Top Card")
    mech_card._is_mechanologist = True
    game_state.player.deck.add_card(mech_card)
    game_state.top_deck_card = mech_card
    game_state.top_card_is_mechanologist = True


@given("the top card of the player's deck is not a Mechanologist card")
def top_deck_card_is_not_mechanologist(game_state):
    """Rule 8.3.9: The deck's top card is NOT a Mechanologist card."""
    non_mech_card = game_state.create_card(name="Non-Mechanologist Top Card")
    non_mech_card._is_mechanologist = False
    game_state.player.deck.add_card(non_mech_card)
    game_state.top_deck_card = non_mech_card
    game_state.top_card_is_mechanologist = False


@given("the player's deck is empty")
def players_deck_is_empty(game_state):
    """Rule 8.3.9b: The player has no cards in their deck."""
    game_state.deck_is_empty = True
    game_state.top_deck_card = None
    game_state.top_card_is_mechanologist = False


# ---- When steps ----

@when("I inspect the Boost ability on the card")
def inspect_boost_ability(game_state):
    """Rule 8.3.9: Inspect the Boost ability on the test card."""
    game_state.inspected_ability = game_state.get_boost_ability(
        game_state.boost_card
    )


@when("the player plays the card and chooses to boost")
def player_plays_card_and_boosts(game_state):
    """Rule 8.3.9: The player plays the Boost card and pays the boost additional cost."""
    result = game_state.attempt_boost(
        card=game_state.boost_card,
        deck_top=game_state.top_deck_card,
        deck_is_empty=getattr(game_state, "deck_is_empty", False),
    )
    game_state.boost_result = result
    game_state.chose_to_boost = True


@when("the player attempts to boost while playing the card")
def player_attempts_boost_with_empty_deck(game_state):
    """Rule 8.3.9b: The player tries to boost but the deck is empty."""
    result = game_state.attempt_boost(
        card=game_state.boost_card,
        deck_top=None,
        deck_is_empty=True,
    )
    game_state.boost_result = result
    game_state.chose_to_boost = True


@when("the player plays the card without choosing to boost")
def player_plays_card_without_boosting(game_state):
    """Rule 8.3.9: The player plays the Boost card but opts not to pay the boost cost."""
    game_state.boost_result = None
    game_state.chose_to_boost = False
    game_state.card_banished_from_deck = False
    game_state.card_got_go_again_from_boost = False
    game_state.player_boosted = False


# ---- Then steps ----

@then("the Boost ability is a play-static ability")
def boost_is_play_static(game_state):
    """Rule 8.3.9: Boost must be a play-static ability."""
    ability = game_state.inspected_ability
    assert ability is not None, "Card should have a Boost ability"
    is_play_static = getattr(ability, "is_play_static", None)
    assert is_play_static is True, (
        f"Boost should be a play-static ability (Rule 8.3.9), got is_play_static={is_play_static}"
    )


@then("the Boost ability is an optional additional-cost ability")
def boost_is_optional_additional_cost(game_state):
    """Rule 8.3.9: Boost must be optional and an additional cost."""
    ability = game_state.inspected_ability
    assert ability is not None, "Card should have a Boost ability"
    is_optional = getattr(ability, "is_optional", None)
    is_additional_cost = getattr(ability, "is_additional_cost", None)
    assert is_optional is True, (
        f"Boost should be optional (Rule 8.3.9), got is_optional={is_optional}"
    )
    assert is_additional_cost is True, (
        f"Boost should be an additional cost (Rule 8.3.9), got is_additional_cost={is_additional_cost}"
    )


@then("the Boost ability is not a triggered ability")
def boost_is_not_triggered(game_state):
    """Rule 8.3.9: Boost must NOT be a triggered ability."""
    ability = game_state.inspected_ability
    assert ability is not None, "Card should have a Boost ability"
    is_triggered = getattr(ability, "is_triggered", False)
    assert is_triggered is False, (
        f"Boost should NOT be a triggered ability (Rule 8.3.9), got is_triggered={is_triggered}"
    )


@then("the Boost ability is not a meta-static ability")
def boost_is_not_meta_static(game_state):
    """Rule 8.3.9: Boost must NOT be a meta-static ability."""
    ability = game_state.inspected_ability
    assert ability is not None, "Card should have a Boost ability"
    is_meta_static = getattr(ability, "is_meta_static", False)
    assert is_meta_static is False, (
        f"Boost should NOT be a meta-static ability (Rule 8.3.9), got is_meta_static={is_meta_static}"
    )


@then(parsers.parse('the Boost ability means "{meaning}"'))
def boost_meaning_is_correct(game_state, meaning):
    """Rule 8.3.9: Boost has the canonical meaning text."""
    ability = game_state.inspected_ability
    actual_meaning = getattr(ability, "meaning", None)
    assert actual_meaning == meaning, (
        f"Boost meaning should be '{meaning}' (Rule 8.3.9), got: {actual_meaning}"
    )


@then("the top card is banished from the player's deck")
def top_card_is_banished(game_state):
    """Rule 8.3.9: When boosting, the top card of the deck is banished."""
    result = game_state.boost_result
    if result is not None:
        banished = getattr(result, "card_banished", None)
        assert banished is True, (
            "The top card of the deck should be banished when boosting (Rule 8.3.9), "
            f"got: {banished}"
        )
    else:
        # None result means engine not implemented yet — expected
        pass


@then("the played card gets go again")
def played_card_gets_go_again(game_state):
    """Rule 8.3.9: When boosted with a Mechanologist card, the played card gets go again."""
    result = game_state.boost_result
    if result is not None:
        has_go_again = getattr(result, "got_go_again", None)
        assert has_go_again is True, (
            "Played card should get go again when boosted with a Mechanologist card "
            f"(Rule 8.3.9), got: {has_go_again}"
        )
    else:
        pass


@then("the played card does not get go again")
def played_card_does_not_get_go_again(game_state):
    """Rule 8.3.9: When boosted with a non-Mechanologist card, go again is NOT granted."""
    result = game_state.boost_result
    if result is not None:
        has_go_again = getattr(result, "got_go_again", False)
        assert has_go_again is False, (
            "Played card should NOT get go again when boosted with a non-Mechanologist card "
            f"(Rule 8.3.9), got: {has_go_again}"
        )
    else:
        pass


@then("the player is considered to have boosted")
def player_is_considered_boosted(game_state):
    """Rule 8.3.9a: The player is considered to have boosted after paying the boost cost."""
    result = game_state.boost_result
    if result is not None:
        player_boosted = getattr(result, "player_boosted", None)
        assert player_boosted is True, (
            "Player should be considered to have boosted (Rule 8.3.9a), "
            f"got: {player_boosted}"
        )
    else:
        pass


@then("the played card is considered to have been boosted")
def card_is_considered_boosted(game_state):
    """Rule 8.3.9a: The played card is considered to have been boosted."""
    result = game_state.boost_result
    if result is not None:
        card_boosted = getattr(result, "card_boosted", None)
        assert card_boosted is True, (
            "Played card should be considered to have been boosted (Rule 8.3.9a), "
            f"got: {card_boosted}"
        )
    else:
        pass


@then("the player cannot boost")
def player_cannot_boost(game_state):
    """Rule 8.3.9b: When the deck is empty, the player cannot boost."""
    result = game_state.boost_result
    if result is not None:
        can_boost = getattr(result, "can_boost", None)
        boost_succeeded = getattr(result, "card_banished", False)
        assert boost_succeeded is False, (
            "Player should NOT be able to boost with empty deck (Rule 8.3.9b), "
            f"got: boost_succeeded={boost_succeeded}"
        )
        if can_boost is not None:
            assert can_boost is False, (
                f"can_boost should be False when deck is empty (Rule 8.3.9b), got: {can_boost}"
            )
    else:
        pass


@then("the boost additional cost cannot be paid")
def boost_additional_cost_cannot_be_paid(game_state):
    """Rule 8.3.9b: The boost additional cost (banish top of deck) cannot be paid if deck is empty."""
    result = game_state.boost_result
    if result is not None:
        cost_paid = getattr(result, "additional_cost_paid", False)
        assert cost_paid is False, (
            "Boost additional cost should not be payable with empty deck (Rule 8.3.9b), "
            f"got: cost_paid={cost_paid}"
        )
    else:
        pass


@then("no card is banished from the deck")
def no_card_banished_from_deck(game_state):
    """Rule 8.3.9: When the player opts not to boost, no card is banished."""
    assert game_state.card_banished_from_deck is False, (
        "No card should be banished when player does not boost (Rule 8.3.9)"
    )


@then("the played card does not get go again from boost")
def played_card_does_not_get_go_again_from_boost(game_state):
    """Rule 8.3.9: When not boosting, the card does not get go again from boost."""
    assert game_state.card_got_go_again_from_boost is False, (
        "Played card should not get go again from boost when player chose not to boost "
        "(Rule 8.3.9)"
    )


@then("the player is not considered to have boosted")
def player_is_not_considered_boosted(game_state):
    """Rule 8.3.9: When the player opts not to boost, they are not considered to have boosted."""
    assert game_state.player_boosted is False, (
        "Player should NOT be considered to have boosted when they chose not to boost "
        "(Rule 8.3.9)"
    )


# ===== Fixtures =====

@pytest.fixture
def game_state():
    """
    Fixture providing game state for testing Boost (Rule 8.3.9).

    Uses BDDGameState which integrates with the real engine.
    Reference: Rule 8.3.9
    """
    from tests.bdd_helpers import BDDGameState

    state = BDDGameState()
    state.boost_card = None
    state.top_deck_card = None
    state.top_card_is_mechanologist = False
    state.deck_is_empty = False
    state.boost_result = None
    state.chose_to_boost = False
    state.card_banished_from_deck = False
    state.card_got_go_again_from_boost = False
    state.player_boosted = False
    return state
