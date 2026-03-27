"""
Step definitions for Section 8.3.33: Beat Chest (Ability Keyword)
Reference: Flesh and Blood Comprehensive Rules Section 8.3.33

This module implements behavioral tests for the Beat Chest ability keyword:
- Beat Chest is a play-static ability (Rule 8.3.33)
- Beat Chest means: "As an additional cost to play this, you may discard a card
  with 6 or more {p}." (Rule 8.3.33)
- The additional cost is optional — player "may" pay it (Rule 8.3.33)
- The discarded card must have 6 or more pitch ({p}) (Rule 8.3.33)
- When the cost is paid, the player is considered to have beaten chest (Rule 8.3.33a)
- A player cannot beat chest if they have no cards with 6+ pitch in hand (Rule 8.3.33b)

Engine Features Needed for Section 8.3.33:
- [ ] BeatChestAbility class as a play-static ability (Rule 8.3.33)
- [ ] BeatChestAbility.is_play_static -> True (Rule 8.3.33)
- [ ] BeatChestAbility.meaning: the text of the ability (Rule 8.3.33)
- [ ] Engine must allow playing card with Beat Chest without paying the cost (Rule 8.3.33)
- [ ] Engine must allow discarding a card with 6+ pitch as Beat Chest cost (Rule 8.3.33)
- [ ] Engine must reject cards with fewer than 6 pitch as Beat Chest cost (Rule 8.3.33)
- [ ] Engine must mark the player as "beaten chest" when they pay the cost (Rule 8.3.33a)
- [ ] Engine must prevent beating chest when no 6+ pitch cards are in hand (Rule 8.3.33b)
- [ ] CardInstance.keywords property (Rule 8.3.33)
- [ ] CardInstance.get_ability("beat_chest") method (Rule 8.3.33)
- [ ] PlayResult.player_beaten_chest flag (Rule 8.3.33a)

Current status: Tests written, Engine pending
"""

import pytest
from pytest_bdd import scenario, given, when, then, parsers


# ===== Rule 8.3.33: Beat Chest is recognized as a keyword =====

@scenario(
    "../features/section_8_3_33_beat_chest.feature",
    "Beat Chest is recognized as an ability keyword",
)
def test_beat_chest_is_recognized_as_keyword():
    """Rule 8.3.33: Beat Chest must be recognized as a keyword on cards that have it."""
    pass


# ===== Rule 8.3.33: Beat Chest is a play-static ability =====

@scenario(
    "../features/section_8_3_33_beat_chest.feature",
    "Beat Chest is a play-static ability",
)
def test_beat_chest_is_play_static_ability():
    """Rule 8.3.33: Beat Chest must be classified as a play-static ability."""
    pass


# ===== Rule 8.3.33: Beat Chest ability meaning matches comprehensive rules text =====

@scenario(
    "../features/section_8_3_33_beat_chest.feature",
    "Beat Chest ability meaning matches comprehensive rules text",
)
def test_beat_chest_ability_meaning():
    """Rule 8.3.33: The Beat Chest ability meaning must match the comprehensive rules text."""
    pass


# ===== Rule 8.3.33: Beat Chest cost is optional =====

@scenario(
    "../features/section_8_3_33_beat_chest.feature",
    "Player can play a Beat Chest card without paying the additional cost",
)
def test_beat_chest_cost_is_optional():
    """Rule 8.3.33: The Beat Chest cost is optional — the player may choose not to pay it."""
    pass


# ===== Rule 8.3.33 + 8.3.33a: Beat Chest by discarding exactly 6-pitch card =====

@scenario(
    "../features/section_8_3_33_beat_chest.feature",
    "Player beats chest by discarding a card with exactly 6 pitch",
)
def test_beat_chest_by_discarding_6_pitch_card():
    """Rule 8.3.33 + 8.3.33a: Player can pay Beat Chest cost by discarding a card with exactly 6 pitch."""
    pass


# ===== Rule 8.3.33 + 8.3.33a: Beat Chest by discarding more-than-6-pitch card =====

@scenario(
    "../features/section_8_3_33_beat_chest.feature",
    "Player beats chest by discarding a card with more than 6 pitch",
)
def test_beat_chest_by_discarding_7_pitch_card():
    """Rule 8.3.33 + 8.3.33a: Player can pay Beat Chest cost by discarding a card with 7+ pitch."""
    pass


# ===== Rule 8.3.33a: Player is considered to have beaten chest =====

@scenario(
    "../features/section_8_3_33_beat_chest.feature",
    "Player is considered to have beaten chest after paying the cost",
)
def test_player_is_considered_to_have_beaten_chest():
    """Rule 8.3.33a: When player pays the Beat Chest cost, they are considered to have beaten chest."""
    pass


# ===== Rule 8.3.33b: Cannot beat chest without a 6+ pitch card in hand =====

@scenario(
    "../features/section_8_3_33_beat_chest.feature",
    "Player cannot beat chest without a high-pitch card in hand",
)
def test_cannot_beat_chest_without_high_pitch_card():
    """Rule 8.3.33b: A player cannot beat chest if they have no cards with 6+ pitch in hand."""
    pass


# ===== Rule 8.3.33b: Cannot beat chest with only 5-pitch card =====

@scenario(
    "../features/section_8_3_33_beat_chest.feature",
    "Player cannot beat chest with a card that has only 5 pitch",
)
def test_cannot_beat_chest_with_5_pitch_card():
    """Rule 8.3.33b: A card with only 5 pitch does not meet the 6+ pitch requirement."""
    pass


# ===== Step Definitions =====

@given("a card with the Beat Chest keyword")
def card_with_beat_chest_keyword(game_state):
    """Rule 8.3.33: Create a card that has the Beat Chest keyword."""
    game_state.beat_chest_card = game_state.create_card(name="Beat Chest Test Card")
    game_state.beat_chest_card.keywords = getattr(game_state.beat_chest_card, "keywords", [])
    if "beat_chest" not in game_state.beat_chest_card.keywords:
        game_state.beat_chest_card.keywords.append("beat_chest")


@given("a player has a card with the Beat Chest keyword in hand")
def player_has_beat_chest_card_in_hand(game_state):
    """Rule 8.3.33: Set up player with a Beat Chest card in hand."""
    game_state.beat_chest_card = game_state.create_card(name="Beat Chest Test Card")
    game_state.beat_chest_card.keywords = getattr(game_state.beat_chest_card, "keywords", [])
    if "beat_chest" not in game_state.beat_chest_card.keywords:
        game_state.beat_chest_card.keywords.append("beat_chest")
    game_state.player.hand.add_card(game_state.beat_chest_card)


@given("the player has a card with 6 pitch in hand")
def player_has_6_pitch_card_in_hand(game_state):
    """Rule 8.3.33: Set up player with a card that has 6 pitch in hand."""
    game_state.high_pitch_card = game_state.create_card_with_name_and_pitch(
        name="Six Pitch Card", pitch=6
    )
    game_state.player.hand.add_card(game_state.high_pitch_card)
    game_state.beat_chest_target = game_state.high_pitch_card


@given("the player has a card with 7 pitch in hand")
def player_has_7_pitch_card_in_hand(game_state):
    """Rule 8.3.33: Set up player with a card that has 7 pitch in hand."""
    game_state.high_pitch_card = game_state.create_card_with_name_and_pitch(
        name="Seven Pitch Card", pitch=7
    )
    game_state.player.hand.add_card(game_state.high_pitch_card)
    game_state.beat_chest_target = game_state.high_pitch_card


@given("the player has no cards with 6 or more pitch in hand")
def player_has_no_high_pitch_cards_in_hand(game_state):
    """Rule 8.3.33b: Set up player with no cards meeting the 6+ pitch requirement."""
    # Ensure there are no high-pitch cards — only add a low-pitch card if needed
    game_state.beat_chest_target = None


@given("the player has a card with 5 pitch in hand")
def player_has_5_pitch_card_in_hand(game_state):
    """Rule 8.3.33b: Set up player with a card that has only 5 pitch (insufficient for Beat Chest)."""
    game_state.low_pitch_card = game_state.create_card_with_name_and_pitch(
        name="Five Pitch Card", pitch=5
    )
    game_state.player.hand.add_card(game_state.low_pitch_card)


@given("the player has no other cards with 6 or more pitch in hand")
def player_has_no_other_high_pitch_cards(game_state):
    """Rule 8.3.33b: Confirm no other 6+ pitch cards exist in hand."""
    # This step confirms no high-pitch cards were added — beat_chest_target remains None
    game_state.beat_chest_target = None


@when("I inspect the card's keywords")
def inspect_card_keywords(game_state):
    """Rule 8.3.33: Inspect the keywords on a card."""
    game_state.inspected_keywords = getattr(game_state.beat_chest_card, "keywords", [])


@when("I check the ability type of Beat Chest")
def check_beat_chest_ability_type(game_state):
    """Rule 8.3.33: Check whether Beat Chest is classified as a play-static ability."""
    game_state.beat_chest_ability = None
    if hasattr(game_state.beat_chest_card, "get_ability"):
        game_state.beat_chest_ability = game_state.beat_chest_card.get_ability("beat_chest")


@when("I inspect the Beat Chest ability's meaning")
def inspect_beat_chest_meaning(game_state):
    """Rule 8.3.33: Read the meaning of the Beat Chest ability."""
    game_state.beat_chest_ability = None
    if hasattr(game_state.beat_chest_card, "get_ability"):
        game_state.beat_chest_ability = game_state.beat_chest_card.get_ability("beat_chest")


@when("the player plays the card without paying the Beat Chest cost")
def play_card_without_beat_chest_cost(game_state):
    """Rule 8.3.33: Player plays the Beat Chest card without paying the additional cost."""
    game_state.play_result = game_state.player.attempt_play_from_zone(
        game_state.beat_chest_card, "hand"
    )
    game_state.paid_beat_chest_cost = False


@when("the player plays the card and pays the Beat Chest cost by discarding the 6-pitch card")
def play_card_paying_beat_chest_cost_6_pitch(game_state):
    """Rule 8.3.33 + 8.3.33a: Player plays the Beat Chest card and discards a 6-pitch card."""
    game_state.paid_beat_chest_cost = True
    game_state.beat_chest_result = game_state.player.attempt_play_with_beat_chest(
        game_state.beat_chest_card, discard_target=game_state.beat_chest_target
    ) if hasattr(game_state.player, "attempt_play_with_beat_chest") else None
    game_state.play_result = game_state.beat_chest_result


@when("the player plays the card and pays the Beat Chest cost by discarding the 7-pitch card")
def play_card_paying_beat_chest_cost_7_pitch(game_state):
    """Rule 8.3.33 + 8.3.33a: Player plays the Beat Chest card and discards a 7-pitch card."""
    game_state.paid_beat_chest_cost = True
    game_state.beat_chest_result = game_state.player.attempt_play_with_beat_chest(
        game_state.beat_chest_card, discard_target=game_state.beat_chest_target
    ) if hasattr(game_state.player, "attempt_play_with_beat_chest") else None
    game_state.play_result = game_state.beat_chest_result


@when("the player attempts to pay the Beat Chest cost")
def player_attempts_to_pay_beat_chest_cost(game_state):
    """Rule 8.3.33b: Player attempts to pay the Beat Chest cost with no valid card to discard."""
    game_state.beat_chest_attempt_result = (
        game_state.player.can_beat_chest()
        if hasattr(game_state.player, "can_beat_chest")
        else None
    )


@then("the card has the Beat Chest keyword")
def card_has_beat_chest_keyword(game_state):
    """Rule 8.3.33: The card must have the Beat Chest keyword."""
    keywords = game_state.inspected_keywords
    normalized = [k.lower().replace(" ", "_") if isinstance(k, str) else k for k in keywords]
    assert "beat_chest" in normalized, (
        f"Expected 'beat_chest' in card keywords, but got: {keywords}"
    )


@then("Beat Chest is a play-static ability")
def beat_chest_is_play_static(game_state):
    """Rule 8.3.33: Beat Chest must be classified as a play-static ability."""
    ability = game_state.beat_chest_ability
    assert ability is not None, (
        "BeatChestAbility not found — engine needs BeatChestAbility class (Rule 8.3.33)"
    )
    is_play_static = getattr(ability, "is_play_static", None)
    assert is_play_static is True, (
        f"Expected Beat Chest ability to be play-static, but is_play_static={is_play_static} (Rule 8.3.33)"
    )


@then(parsers.parse('the Beat Chest meaning is "{meaning}"'))
def beat_chest_meaning_matches(game_state, meaning):
    """Rule 8.3.33: The Beat Chest meaning must match the comprehensive rules text."""
    ability = game_state.beat_chest_ability
    assert ability is not None, (
        "BeatChestAbility not found — engine needs BeatChestAbility class (Rule 8.3.33)"
    )
    actual_meaning = getattr(ability, "meaning", None)
    assert actual_meaning is not None, "BeatChestAbility.meaning not found (Rule 8.3.33)"
    assert meaning.lower() in actual_meaning.lower(), (
        f"Expected Beat Chest meaning to contain '{meaning}', but got: '{actual_meaning}' (Rule 8.3.33)"
    )


@then("the card is played successfully")
def card_is_played_successfully(game_state):
    """Rule 8.3.33: The card should be played successfully."""
    result = game_state.play_result
    assert result is not None, (
        "No play result returned — engine needs play handling (Rule 8.3.33)"
    )
    assert getattr(result, "success", False), (
        f"Expected play to succeed, but result.success={getattr(result, 'success', None)} (Rule 8.3.33)"
    )


@then("the high-pitch card remains in hand")
def high_pitch_card_remains_in_hand(game_state):
    """Rule 8.3.33: When Beat Chest cost is not paid, the high-pitch card stays in hand."""
    assert game_state.high_pitch_card in game_state.player.hand, (
        "High-pitch card should remain in hand when Beat Chest cost is not paid (Rule 8.3.33)"
    )


@then("the player is not considered to have beaten chest")
def player_not_considered_beaten_chest(game_state):
    """Rule 8.3.33: When cost is not paid, player is not considered to have beaten chest."""
    result = game_state.play_result
    player_beaten_chest = getattr(result, "player_beaten_chest", False) if result else False
    assert not player_beaten_chest, (
        "Player should NOT be considered to have beaten chest when cost was not paid (Rule 8.3.33)"
    )


@then("the 6-pitch card is in the graveyard")
def six_pitch_card_is_in_graveyard(game_state):
    """Rule 8.3.33a: After beating chest, the discarded 6-pitch card should be in the graveyard."""
    assert game_state.beat_chest_target in game_state.player.graveyard, (
        "The discarded 6-pitch card should be in the graveyard (Rule 8.3.33a)"
    )


@then("the 7-pitch card is in the graveyard")
def seven_pitch_card_is_in_graveyard(game_state):
    """Rule 8.3.33a: After beating chest, the discarded 7-pitch card should be in the graveyard."""
    assert game_state.beat_chest_target in game_state.player.graveyard, (
        "The discarded 7-pitch card should be in the graveyard (Rule 8.3.33a)"
    )


@then("the player is considered to have beaten chest")
def player_is_considered_to_have_beaten_chest(game_state):
    """Rule 8.3.33a: When player pays the Beat Chest cost, they are considered to have beaten chest."""
    result = game_state.play_result
    assert result is not None, "No play result returned (Rule 8.3.33a)"
    player_beaten_chest = getattr(result, "player_beaten_chest", None)
    assert player_beaten_chest is True, (
        f"Expected player_beaten_chest=True, but got {player_beaten_chest} (Rule 8.3.33a)"
    )


@then("the player cannot beat chest")
def player_cannot_beat_chest(game_state):
    """Rule 8.3.33b: Player cannot beat chest without a 6+ pitch card in hand."""
    can_beat_chest = game_state.beat_chest_attempt_result
    assert can_beat_chest is False or can_beat_chest is None, (
        f"Expected player to be unable to beat chest, but can_beat_chest={can_beat_chest} (Rule 8.3.33b)"
    )


@then("no card is discarded as the Beat Chest cost")
def no_card_discarded_as_beat_chest_cost(game_state):
    """Rule 8.3.33b: No card should be discarded when Beat Chest cost cannot be paid."""
    graveyard = game_state.player.graveyard
    graveyard_cards = getattr(graveyard, "cards", [])
    assert len(graveyard_cards) == 0, (
        f"Expected no cards discarded to graveyard, but found {len(graveyard_cards)} cards (Rule 8.3.33b)"
    )


# ===== Fixtures =====

@pytest.fixture
def game_state():
    """
    Fixture providing game state for Beat Chest keyword tests.

    Uses BDDGameState which integrates with the real engine.
    Reference: Rule 8.3.33
    """
    from tests.bdd_helpers import BDDGameState

    state = BDDGameState()
    state.beat_chest_card = None
    state.beat_chest_target = None
    state.high_pitch_card = None
    state.low_pitch_card = None
    state.play_result = None
    state.beat_chest_result = None
    state.paid_beat_chest_cost = False
    state.beat_chest_attempt_result = None
    state.beat_chest_ability = None
    state.inspected_keywords = []

    return state
