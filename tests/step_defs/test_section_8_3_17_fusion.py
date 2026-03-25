"""
Step definitions for Section 8.3.17: Fusion (Ability Keyword)
Reference: Flesh and Blood Comprehensive Rules Section 8.3.17

This module implements behavioral tests for the Fusion ability keyword:
- Fusion is an optional additional-cost play-static ability (Rule 8.3.17)
- Written "[SUPERTYPES] Fusion" meaning "As an additional cost to play this,
  you may reveal (a/an) [SUPERTYPES] card(s) from your hand" (Rule 8.3.17)
- If a player pays the additional cost, the player is considered to have fused
  those supertypes and the played card is considered to have been fused (Rule 8.3.17a)
- A player cannot fuse if they cannot pay the additional cost of revealing the
  card(s) with the specified supertypes from their hand (Rule 8.3.17b)
- A player may only reveal up to one card for each of the supertypes listed;
  a single card may be revealed for one or more different supertypes (Rule 8.3.17c)
- "and" requires all supertypes; "and/or" requires at least one (Rule 8.3.17d)

Engine Features Needed for Section 8.3.17:
- [ ] FusionAbility class as a play-static ability (Rule 8.3.17)
- [ ] FusionAbility.is_play_static -> True (Rule 8.3.17)
- [ ] FusionAbility.is_optional -> True (Rule 8.3.17)
- [ ] FusionAbility.supertypes: list of required supertypes (Rule 8.3.17)
- [ ] FusionAbility.conjunction: "and" | "and/or" | None for single-supertype (Rule 8.3.17d)
- [ ] FusionAbility.meaning: formatted ability text (Rule 8.3.17)
- [ ] PlayAction.pay_fusion_cost(revealed_cards) to pay the optional cost (Rule 8.3.17)
- [ ] PlayAction.card_is_fused -> bool: True if fusion cost was paid (Rule 8.3.17a)
- [ ] GameState.player_fused_supertypes: records which supertypes were fused (Rule 8.3.17a)
- [ ] FusionValidator.can_fuse(hand, fusion_ability) -> bool (Rule 8.3.17b)
- [ ] FusionValidator: enforce max one card per listed supertype (Rule 8.3.17c)
- [ ] FusionValidator: allow single card to satisfy multiple supertypes (Rule 8.3.17c)
- [ ] FusionValidator.validate_and_conjunction: requires all supertypes (Rule 8.3.17d)
- [ ] FusionValidator.validate_and_or_conjunction: requires at least one supertype (Rule 8.3.17d)

Current status: Tests written, Engine pending
"""

import pytest
from pytest_bdd import scenario, given, when, then, parsers


# ===== Rule 8.3.17: Fusion is a play-static ability =====

@scenario(
    "../features/section_8_3_17_fusion.feature",
    "Fusion is a play-static ability",
)
def test_fusion_is_play_static_ability():
    """Rule 8.3.17: Fusion is a play-static ability."""
    pass


# ===== Rule 8.3.17: Fusion ability meaning format =====

@scenario(
    "../features/section_8_3_17_fusion.feature",
    "Fusion ability meaning is correctly formatted with the specified supertypes",
)
def test_fusion_ability_meaning_format():
    """Rule 8.3.17: Fusion meaning is correctly formatted."""
    pass


# ===== Rule 8.3.17a: Paying fusion cost makes card and player fused =====

@scenario(
    "../features/section_8_3_17_fusion.feature",
    "Paying the fusion cost makes the played card considered fused",
)
def test_paying_fusion_cost_makes_card_fused():
    """Rule 8.3.17a: Paying fusion cost marks the card and player as fused."""
    pass


@scenario(
    "../features/section_8_3_17_fusion.feature",
    "Playing a fusion card without paying the fusion cost does not make it fused",
)
def test_not_paying_fusion_cost_card_not_fused():
    """Rule 8.3.17a: Not paying fusion cost means card is not fused."""
    pass


# ===== Rule 8.3.17b: Cannot fuse without required supertype cards in hand =====

@scenario(
    "../features/section_8_3_17_fusion.feature",
    "Player cannot fuse if they have no cards with the required supertype in hand",
)
def test_cannot_fuse_without_required_supertype_in_hand():
    """Rule 8.3.17b: Player cannot fuse if they cannot pay the additional cost."""
    pass


# ===== Rule 8.3.17c: At most one card per listed supertype =====

@scenario(
    "../features/section_8_3_17_fusion.feature",
    "Player may only reveal one card per supertype listed in fusion",
)
def test_only_one_card_per_supertype_for_fusion():
    """Rule 8.3.17c: At most one card may be revealed for each listed supertype."""
    pass


@scenario(
    "../features/section_8_3_17_fusion.feature",
    "A single card with multiple supertypes can satisfy multiple fusion requirements",
)
def test_single_card_can_satisfy_multiple_supertypes():
    """Rule 8.3.17c: A single card may be revealed for multiple different supertypes."""
    pass


# ===== Rule 8.3.17d: "and" requires ALL supertypes =====

@scenario(
    "../features/section_8_3_17_fusion.feature",
    "Draconic and Ninja fusion requires revealing cards with both supertypes",
)
def test_and_fusion_requires_all_supertypes():
    """Rule 8.3.17d: 'and' fusion requires revealing cards for all listed supertypes."""
    pass


@scenario(
    "../features/section_8_3_17_fusion.feature",
    "Draconic and Ninja fusion cannot be paid with only one supertype revealed",
)
def test_and_fusion_cannot_be_paid_with_only_one_supertype():
    """Rule 8.3.17d: 'and' fusion fails if not all supertypes can be revealed."""
    pass


# ===== Rule 8.3.17d: "and/or" requires AT LEAST ONE supertype =====

@scenario(
    "../features/section_8_3_17_fusion.feature",
    "Draconic and/or Ninja fusion can be paid with only a Draconic card",
)
def test_and_or_fusion_satisfied_by_one_supertype_draconic():
    """Rule 8.3.17d: 'and/or' fusion is satisfied by revealing any one of the listed supertypes."""
    pass


@scenario(
    "../features/section_8_3_17_fusion.feature",
    "Draconic and/or Ninja fusion can be paid with only a Ninja card",
)
def test_and_or_fusion_satisfied_by_one_supertype_ninja():
    """Rule 8.3.17d: 'and/or' fusion is satisfied by revealing any one of the listed supertypes."""
    pass


# ===== Step Definitions =====

# ---- Given steps ----

@given(parsers.parse('a card has the "{fusion_keyword}" keyword'))
def card_with_fusion_keyword(game_state, fusion_keyword):
    """Rule 8.3.17: Create a card with the specified Fusion keyword."""
    card = game_state.create_card(name=f"Fusion Test Card ({fusion_keyword})")
    # Parse "[SUPERTYPES] Fusion" to extract supertypes and conjunction
    if fusion_keyword.endswith(" Fusion"):
        supertypes_str = fusion_keyword[:-len(" Fusion")]
        if " and/or " in supertypes_str:
            parts = [s.strip() for s in supertypes_str.split(" and/or ")]
            card._fusion_supertypes = parts
            card._fusion_conjunction = "and/or"
        elif " and " in supertypes_str:
            parts = [s.strip() for s in supertypes_str.split(" and ")]
            card._fusion_supertypes = parts
            card._fusion_conjunction = "and"
        else:
            card._fusion_supertypes = supertypes_str.split()
            card._fusion_conjunction = None
    else:
        card._fusion_supertypes = []
        card._fusion_conjunction = None
    card._fusion_keyword = fusion_keyword
    game_state.fusion_card = card


@given(parsers.parse('a player has a card with "{fusion_keyword}" in their hand'))
def player_has_fusion_card_in_hand(game_state, fusion_keyword):
    """Rule 8.3.17: Place a card with Fusion in the player's hand."""
    card = game_state.create_card(name=f"Fusion Card ({fusion_keyword})")
    if fusion_keyword.endswith(" Fusion"):
        supertypes_str = fusion_keyword[:-len(" Fusion")]
        if " and/or " in supertypes_str:
            parts = [s.strip() for s in supertypes_str.split(" and/or ")]
            card._fusion_supertypes = parts
            card._fusion_conjunction = "and/or"
        elif " and " in supertypes_str:
            parts = [s.strip() for s in supertypes_str.split(" and ")]
            card._fusion_supertypes = parts
            card._fusion_conjunction = "and"
        else:
            card._fusion_supertypes = supertypes_str.split()
            card._fusion_conjunction = None
    else:
        card._fusion_supertypes = []
        card._fusion_conjunction = None
    card._fusion_keyword = fusion_keyword
    game_state.player.hand.add_card(card)
    game_state.fusion_card = card


@given('the player has a Draconic card in their hand')
def player_has_draconic_card_in_hand(game_state):
    """Rule 8.3.17: Place a Draconic supertype card in the player's hand."""
    card = game_state.create_card(name="Test Draconic Card")
    card._card_supertypes = ["Draconic"]
    game_state.player.hand.add_card(card)
    game_state.draconic_card = card


@given('the player has a Ninja card in their hand')
def player_has_ninja_card_in_hand(game_state):
    """Rule 8.3.17: Place a Ninja supertype card in the player's hand."""
    card = game_state.create_card(name="Test Ninja Card")
    card._card_supertypes = ["Ninja"]
    game_state.player.hand.add_card(card)
    game_state.ninja_card = card


@given('the player has two Draconic cards in their hand')
def player_has_two_draconic_cards_in_hand(game_state):
    """Rule 8.3.17c: Place two Draconic supertype cards in the player's hand."""
    card1 = game_state.create_card(name="Test Draconic Card 1")
    card1._card_supertypes = ["Draconic"]
    card2 = game_state.create_card(name="Test Draconic Card 2")
    card2._card_supertypes = ["Draconic"]
    game_state.player.hand.add_card(card1)
    game_state.player.hand.add_card(card2)
    game_state.draconic_cards = [card1, card2]


@given('the player has no Draconic cards in their hand')
def player_has_no_draconic_cards_in_hand(game_state):
    """Rule 8.3.17b: Confirm the player has no Draconic cards in hand."""
    # Remove any Draconic cards from hand
    draconic_to_remove = [
        c for c in list(game_state.player.hand.cards)
        if getattr(c, "_card_supertypes", []) and "Draconic" in c._card_supertypes
    ]
    for c in draconic_to_remove:
        game_state.player.hand.remove_card(c)
    game_state.draconic_card = None


@given('the player has no Ninja cards in their hand')
def player_has_no_ninja_cards_in_hand(game_state):
    """Rule 8.3.17b: Confirm the player has no Ninja cards in hand."""
    ninja_to_remove = [
        c for c in list(game_state.player.hand.cards)
        if getattr(c, "_card_supertypes", []) and "Ninja" in c._card_supertypes
    ]
    for c in ninja_to_remove:
        game_state.player.hand.remove_card(c)
    game_state.ninja_card = None


@given('the player has a card with both Draconic and Ninja supertypes in their hand')
def player_has_draconic_ninja_card_in_hand(game_state):
    """Rule 8.3.17c: Place a card with both Draconic and Ninja supertypes in hand."""
    card = game_state.create_card(name="Test Draconic Ninja Card")
    card._card_supertypes = ["Draconic", "Ninja"]
    game_state.player.hand.add_card(card)
    game_state.draconic_ninja_card = card


# ---- When steps ----

@when('I inspect the Fusion ability on the card')
def inspect_fusion_ability(game_state):
    """Rule 8.3.17: Inspect the Fusion ability on the card."""
    game_state.inspected_ability = game_state.get_fusion_ability(
        game_state.fusion_card
    )


@when('the player plays the fusion card and reveals the Draconic card as the fusion cost')
def player_plays_fusion_card_with_draconic_revealed(game_state):
    """Rule 8.3.17a: Play the fusion card and pay the fusion cost by revealing the Draconic card."""
    game_state.play_result = game_state.play_card_with_fusion(
        game_state.fusion_card,
        revealed_cards=[game_state.draconic_card],
    )


@when('the player plays the fusion card without paying the fusion cost')
def player_plays_fusion_card_without_fusion_cost(game_state):
    """Rule 8.3.17a: Play the fusion card without paying the optional fusion cost."""
    game_state.play_result = game_state.play_card_with_fusion(
        game_state.fusion_card,
        revealed_cards=[],
    )


@when('the player attempts to pay the fusion cost')
def player_attempts_to_pay_fusion_cost(game_state):
    """Rule 8.3.17b: Attempt to pay the fusion cost."""
    game_state.fusion_attempt = game_state.attempt_fusion(
        game_state.fusion_card,
        game_state.player.hand,
    )


@when('the player attempts to reveal both Draconic cards for the fusion cost')
def player_attempts_to_reveal_two_draconic_cards(game_state):
    """Rule 8.3.17c: Attempt to reveal two Draconic cards for a single Draconic fusion."""
    game_state.fusion_attempt = game_state.attempt_fusion_with_cards(
        game_state.fusion_card,
        revealed_cards=game_state.draconic_cards,
    )


@when('the player pays the fusion cost by revealing that card for both supertypes')
def player_pays_fusion_with_single_dual_supertype_card(game_state):
    """Rule 8.3.17c: Pay fusion cost by revealing one card that satisfies multiple supertypes."""
    game_state.play_result = game_state.play_card_with_fusion(
        game_state.fusion_card,
        revealed_cards=[game_state.draconic_ninja_card],
    )


@when('the player pays the fusion cost by revealing one Draconic and one Ninja card')
def player_pays_fusion_with_draconic_and_ninja(game_state):
    """Rule 8.3.17d: Pay 'and' fusion cost with one Draconic and one Ninja card."""
    game_state.play_result = game_state.play_card_with_fusion(
        game_state.fusion_card,
        revealed_cards=[game_state.draconic_card, game_state.ninja_card],
    )


@when('the player pays the fusion cost by revealing the Draconic card')
def player_pays_fusion_with_only_draconic(game_state):
    """Rule 8.3.17d: Pay 'and/or' fusion cost with only the Draconic card."""
    game_state.play_result = game_state.play_card_with_fusion(
        game_state.fusion_card,
        revealed_cards=[game_state.draconic_card],
    )


@when('the player pays the fusion cost by revealing the Ninja card')
def player_pays_fusion_with_only_ninja(game_state):
    """Rule 8.3.17d: Pay 'and/or' fusion cost with only the Ninja card."""
    game_state.play_result = game_state.play_card_with_fusion(
        game_state.fusion_card,
        revealed_cards=[game_state.ninja_card],
    )


# ---- Then steps ----

@then('the Fusion ability is a play-static ability')
def fusion_is_play_static(game_state):
    """Rule 8.3.17: Fusion must be a play-static ability."""
    ability = game_state.inspected_ability
    assert ability is not None, "Card should have a Fusion ability"
    is_play_static = getattr(ability, "is_play_static", None)
    assert is_play_static is True, (
        f"Fusion should be a play-static ability (Rule 8.3.17), got: {is_play_static}"
    )


@then('the Fusion ability is optional')
def fusion_is_optional(game_state):
    """Rule 8.3.17: Fusion is an optional additional cost."""
    ability = game_state.inspected_ability
    assert ability is not None, "Card should have a Fusion ability"
    is_optional = getattr(ability, "is_optional", None)
    assert is_optional is True, (
        f"Fusion should be optional (Rule 8.3.17), got: {is_optional}"
    )


@then(parsers.parse('the Fusion ability means "{expected_meaning}"'))
def fusion_meaning_is_correct(game_state, expected_meaning):
    """Rule 8.3.17: Fusion meaning format matches the rule."""
    ability = game_state.inspected_ability
    meaning = getattr(ability, "meaning", None)
    assert meaning == expected_meaning, (
        f"Fusion meaning should be '{expected_meaning}' (Rule 8.3.17), got: {meaning}"
    )


@then('the played card is considered to have been fused')
def played_card_is_fused(game_state):
    """Rule 8.3.17a: The played card is considered to have been fused."""
    result = game_state.play_result
    assert result is not None, "play_card_with_fusion should return a result"
    card_is_fused = getattr(result, "card_is_fused", None)
    assert card_is_fused is True, (
        f"Played card should be considered fused (Rule 8.3.17a), got: {card_is_fused}"
    )


@then('the player is considered to have fused Draconic')
def player_fused_draconic(game_state):
    """Rule 8.3.17a: The player is considered to have fused the Draconic supertype."""
    result = game_state.play_result
    fused_supertypes = getattr(result, "fused_supertypes", None)
    assert fused_supertypes is not None, "Result should track which supertypes were fused"
    assert "Draconic" in fused_supertypes, (
        f"Player should have fused Draconic (Rule 8.3.17a), got fused_supertypes={fused_supertypes}"
    )


@then('the player is considered to have fused Ninja')
def player_fused_ninja(game_state):
    """Rule 8.3.17a: The player is considered to have fused the Ninja supertype."""
    result = game_state.play_result
    fused_supertypes = getattr(result, "fused_supertypes", None)
    assert fused_supertypes is not None, "Result should track which supertypes were fused"
    assert "Ninja" in fused_supertypes, (
        f"Player should have fused Ninja (Rule 8.3.17a), got fused_supertypes={fused_supertypes}"
    )


@then('the player is considered to have fused Draconic and Ninja')
def player_fused_draconic_and_ninja(game_state):
    """Rule 8.3.17a+d: The player is considered to have fused both Draconic and Ninja supertypes."""
    result = game_state.play_result
    fused_supertypes = getattr(result, "fused_supertypes", None)
    assert fused_supertypes is not None, "Result should track which supertypes were fused"
    assert "Draconic" in fused_supertypes and "Ninja" in fused_supertypes, (
        f"Player should have fused Draconic and Ninja (Rule 8.3.17a), got: {fused_supertypes}"
    )


@then('the played card is not considered to have been fused')
def played_card_is_not_fused(game_state):
    """Rule 8.3.17a: Without paying fusion cost, the card is not fused."""
    result = game_state.play_result
    assert result is not None, "play_card_with_fusion should return a result"
    card_is_fused = getattr(result, "card_is_fused", None)
    assert card_is_fused is False, (
        f"Played card should NOT be considered fused when fusion cost not paid "
        f"(Rule 8.3.17a), got: {card_is_fused}"
    )


@then('the player is not considered to have fused Draconic')
def player_not_fused_draconic(game_state):
    """Rule 8.3.17a: Without paying fusion cost, the player has not fused any supertypes."""
    result = game_state.play_result
    fused_supertypes = getattr(result, "fused_supertypes", None)
    has_draconic = fused_supertypes is not None and "Draconic" in fused_supertypes
    assert not has_draconic, (
        f"Player should NOT have fused Draconic when fusion cost not paid "
        f"(Rule 8.3.17a), got fused_supertypes={fused_supertypes}"
    )


@then('the player cannot fuse because no Draconic card is available in hand')
def player_cannot_fuse_no_draconic_in_hand(game_state):
    """Rule 8.3.17b: Cannot fuse if no card with the required supertype is in hand."""
    attempt = game_state.fusion_attempt
    assert attempt is not None, "attempt_fusion should return a result"
    can_fuse = getattr(attempt, "can_fuse", None)
    assert can_fuse is False, (
        f"Player should NOT be able to fuse without a Draconic card in hand "
        f"(Rule 8.3.17b), got can_fuse={can_fuse}"
    )


@then('the player may only reveal one card for the Draconic fusion cost')
def only_one_card_allowed_per_supertype(game_state):
    """Rule 8.3.17c: At most one card may be revealed per listed supertype."""
    attempt = game_state.fusion_attempt
    assert attempt is not None, "attempt_fusion_with_cards should return a result"
    is_valid = getattr(attempt, "is_valid", None)
    assert is_valid is False, (
        f"Revealing two cards for a single Draconic supertype should be invalid "
        f"(Rule 8.3.17c), got is_valid={is_valid}"
    )


@then('the player only needed to reveal one card to satisfy both fusion requirements')
def one_card_satisfies_multiple_supertypes(game_state):
    """Rule 8.3.17c: One card with multiple supertypes can satisfy multiple fusion requirements."""
    result = game_state.play_result
    assert result is not None, "play_card_with_fusion should return a result"
    revealed_count = getattr(result, "revealed_card_count", None)
    assert revealed_count == 1, (
        f"One dual-supertype card should satisfy both fusion requirements "
        f"(Rule 8.3.17c), got revealed_card_count={revealed_count}"
    )


@then('the player cannot fuse because not all required supertypes are available in hand')
def player_cannot_fuse_missing_supertypes(game_state):
    """Rule 8.3.17d: 'and' fusion fails if not all supertypes can be revealed."""
    attempt = game_state.fusion_attempt
    assert attempt is not None, "attempt_fusion should return a result"
    can_fuse = getattr(attempt, "can_fuse", None)
    assert can_fuse is False, (
        f"Player should NOT be able to pay 'and' fusion cost without all required "
        f"supertypes in hand (Rule 8.3.17d), got can_fuse={can_fuse}"
    )


# ===== Fixtures =====

@pytest.fixture
def game_state():
    """
    Fixture providing game state for testing Fusion (Rule 8.3.17).

    Uses BDDGameState which integrates with the real engine.
    Reference: Rule 8.3.17
    """
    from tests.bdd_helpers import BDDGameState

    state = BDDGameState()
    state.fusion_card = None
    state.draconic_card = None
    state.ninja_card = None
    state.draconic_ninja_card = None
    state.draconic_cards = []
    state.play_result = None
    state.fusion_attempt = None
    state.inspected_ability = None
    return state
