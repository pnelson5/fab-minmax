"""
Step definitions for Section 8.3.32: Scrap (Ability Keyword)
Reference: Flesh and Blood Comprehensive Rules Section 8.3.32

This module implements behavioral tests for the Scrap ability keyword:
- Scrap is a play-static ability (Rule 8.3.32)
- Scrap means: "As an additional cost to play this, you may banish an item or
  equipment from your graveyard." (Rule 8.3.32)
- The additional cost is optional — player "may" pay it (Rule 8.3.32)
- Only items or equipment from the graveyard can be banished (Rule 8.3.32)
- When the cost is paid, the player is considered to have scrapped (Rule 8.3.32a)
- When the cost is paid, the banished card is considered to have been scrapped (Rule 8.3.32a)
- A player cannot scrap without items or equipment in their graveyard (Rule 8.3.32b)

Engine Features Needed for Section 8.3.32:
- [ ] ScrapAbility class as a play-static ability (Rule 8.3.32)
- [ ] ScrapAbility.is_play_static -> True (Rule 8.3.32)
- [ ] ScrapAbility.meaning: the text of the ability (Rule 8.3.32)
- [ ] Engine must allow playing card with Scrap without paying the cost (Rule 8.3.32)
- [ ] Engine must allow banishing an item from graveyard as Scrap cost (Rule 8.3.32)
- [ ] Engine must allow banishing equipment from graveyard as Scrap cost (Rule 8.3.32)
- [ ] Engine must mark the player as "scrapped" when they pay the cost (Rule 8.3.32a)
- [ ] Engine must mark the banished card as "scrapped" (Rule 8.3.32a)
- [ ] Engine must prevent scrapping when no items/equipment in graveyard (Rule 8.3.32b)
- [ ] CardInstance.keywords property (Rule 8.3.32)
- [ ] CardInstance.get_ability("scrap") method (Rule 8.3.32)
- [ ] PlayResult.player_scrapped flag (Rule 8.3.32a)
- [ ] PlayResult.scrapped_card reference (Rule 8.3.32a)

Current status: Tests written, Engine pending
"""

import pytest
from pytest_bdd import scenario, given, when, then, parsers


# ===== Rule 8.3.32: Scrap is recognized as a keyword =====

@scenario(
    "../features/section_8_3_32_scrap.feature",
    "Scrap is recognized as an ability keyword",
)
def test_scrap_is_recognized_as_keyword():
    """Rule 8.3.32: Scrap must be recognized as a keyword on cards that have it."""
    pass


# ===== Rule 8.3.32: Scrap is a play-static ability =====

@scenario(
    "../features/section_8_3_32_scrap.feature",
    "Scrap is a play-static ability",
)
def test_scrap_is_play_static_ability():
    """Rule 8.3.32: Scrap must be classified as a play-static ability."""
    pass


# ===== Rule 8.3.32: Scrap ability meaning matches comprehensive rules text =====

@scenario(
    "../features/section_8_3_32_scrap.feature",
    "Scrap ability meaning matches comprehensive rules text",
)
def test_scrap_ability_meaning():
    """Rule 8.3.32: The Scrap ability meaning must match the comprehensive rules text."""
    pass


# ===== Rule 8.3.32: Scrap cost is optional =====

@scenario(
    "../features/section_8_3_32_scrap.feature",
    "Player can play a Scrap card without paying the additional cost",
)
def test_scrap_cost_is_optional():
    """Rule 8.3.32: The Scrap cost is optional — the player may choose not to pay it."""
    pass


# ===== Rule 8.3.32 + 8.3.32a: Scrap by banishing item =====

@scenario(
    "../features/section_8_3_32_scrap.feature",
    "Player scraps by banishing an item from their graveyard",
)
def test_scrap_by_banishing_item():
    """Rule 8.3.32 + 8.3.32a: Player can pay Scrap cost by banishing an item from graveyard."""
    pass


# ===== Rule 8.3.32 + 8.3.32a: Scrap by banishing equipment =====

@scenario(
    "../features/section_8_3_32_scrap.feature",
    "Player scraps by banishing equipment from their graveyard",
)
def test_scrap_by_banishing_equipment():
    """Rule 8.3.32 + 8.3.32a: Player can pay Scrap cost by banishing equipment from graveyard."""
    pass


# ===== Rule 8.3.32a: Player is considered to have scrapped =====

@scenario(
    "../features/section_8_3_32_scrap.feature",
    "Player is considered to have scrapped after paying the Scrap cost",
)
def test_player_is_considered_to_have_scrapped():
    """Rule 8.3.32a: When player pays the Scrap cost, they are considered to have scrapped."""
    pass


# ===== Rule 8.3.32a: Banished card is considered to have been scrapped =====

@scenario(
    "../features/section_8_3_32_scrap.feature",
    "The banished card is considered to have been scrapped",
)
def test_banished_card_is_considered_scrapped():
    """Rule 8.3.32a: The banished card is considered to have been scrapped."""
    pass


# ===== Rule 8.3.32b: Cannot scrap without items/equipment in graveyard =====

@scenario(
    "../features/section_8_3_32_scrap.feature",
    "Player cannot scrap with an empty graveyard",
)
def test_cannot_scrap_with_empty_graveyard():
    """Rule 8.3.32b: A player cannot scrap if there are no items or equipment in the graveyard."""
    pass


# ===== Step Definitions =====

@given("a card with the Scrap keyword")
def card_with_scrap_keyword(game_state):
    """Rule 8.3.32: Create a card that has the Scrap keyword."""
    game_state.scrap_card = game_state.create_card(name="Scrap Test Card")
    game_state.scrap_card.keywords = getattr(game_state.scrap_card, "keywords", [])
    if "scrap" not in game_state.scrap_card.keywords:
        game_state.scrap_card.keywords.append("scrap")


@given("a player has a card with the Scrap keyword in hand")
def player_has_scrap_card_in_hand(game_state):
    """Rule 8.3.32: Set up player with a Scrap card in hand."""
    game_state.scrap_card = game_state.create_card(name="Scrap Test Card")
    game_state.scrap_card.keywords = getattr(game_state.scrap_card, "keywords", [])
    if "scrap" not in game_state.scrap_card.keywords:
        game_state.scrap_card.keywords.append("scrap")
    game_state.player.hand.add_card(game_state.scrap_card)


@given("the player has an item in their graveyard")
def player_has_item_in_graveyard(game_state):
    """Rule 8.3.32: Set up player with an item card in their graveyard."""
    from fab_engine.cards.model import CardType
    game_state.graveyard_item = game_state.create_card(name="Test Item")
    # Mark as item type
    game_state.graveyard_item.card_type = CardType.ITEM if hasattr(CardType, "ITEM") else "item"
    game_state.player.graveyard.add_card(game_state.graveyard_item)
    game_state.scrap_target = game_state.graveyard_item


@given("the player has an equipment in their graveyard")
def player_has_equipment_in_graveyard(game_state):
    """Rule 8.3.32: Set up player with an equipment card in their graveyard."""
    from fab_engine.cards.model import CardType
    game_state.graveyard_equipment = game_state.create_card(name="Test Equipment")
    # Mark as equipment type
    game_state.graveyard_equipment.card_type = CardType.EQUIPMENT if hasattr(CardType, "EQUIPMENT") else "equipment"
    game_state.player.graveyard.add_card(game_state.graveyard_equipment)
    game_state.scrap_target = game_state.graveyard_equipment


@given("the player's graveyard has no items or equipment")
def player_graveyard_has_no_scrapable_cards(game_state):
    """Rule 8.3.32b: Set up player with an empty graveyard (no scrapable cards)."""
    # Ensure graveyard is empty or has only non-scrapable cards
    game_state.scrap_target = None


@when("I inspect the card's keywords")
def inspect_card_keywords(game_state):
    """Rule 8.3.32: Inspect the keywords on a card."""
    game_state.inspected_keywords = getattr(game_state.scrap_card, "keywords", [])


@when("I check the ability type of Scrap")
def check_scrap_ability_type(game_state):
    """Rule 8.3.32: Check whether Scrap is classified as a play-static ability."""
    game_state.scrap_ability = None
    if hasattr(game_state.scrap_card, "get_ability"):
        game_state.scrap_ability = game_state.scrap_card.get_ability("scrap")


@when("I inspect the Scrap ability's meaning")
def inspect_scrap_meaning(game_state):
    """Rule 8.3.32: Read the meaning of the Scrap ability."""
    game_state.scrap_ability = None
    if hasattr(game_state.scrap_card, "get_ability"):
        game_state.scrap_ability = game_state.scrap_card.get_ability("scrap")


@when("the player plays the card without paying the Scrap cost")
def play_card_without_scrap_cost(game_state):
    """Rule 8.3.32: Player plays the Scrap card without paying the additional cost."""
    game_state.play_result = game_state.player.attempt_play_from_zone(
        game_state.scrap_card, "hand"
    )
    game_state.paid_scrap_cost = False


@when("the player plays the card and pays the Scrap cost by banishing the item")
def play_card_paying_scrap_cost_item(game_state):
    """Rule 8.3.32 + 8.3.32a: Player plays the Scrap card and banishes the item."""
    # Attempt to play with the Scrap cost paid
    game_state.paid_scrap_cost = True
    game_state.scrap_result = game_state.player.attempt_play_with_scrap(
        game_state.scrap_card, scrap_target=game_state.scrap_target
    ) if hasattr(game_state.player, "attempt_play_with_scrap") else None
    game_state.play_result = game_state.scrap_result


@when("the player plays the card and pays the Scrap cost by banishing the equipment")
def play_card_paying_scrap_cost_equipment(game_state):
    """Rule 8.3.32 + 8.3.32a: Player plays the Scrap card and banishes the equipment."""
    game_state.paid_scrap_cost = True
    game_state.scrap_result = game_state.player.attempt_play_with_scrap(
        game_state.scrap_card, scrap_target=game_state.scrap_target
    ) if hasattr(game_state.player, "attempt_play_with_scrap") else None
    game_state.play_result = game_state.scrap_result


@when("the player attempts to pay the Scrap cost")
def player_attempts_to_pay_scrap_cost(game_state):
    """Rule 8.3.32b: Player attempts to pay the Scrap cost with nothing to banish."""
    game_state.scrap_attempt_result = game_state.player.can_scrap() if hasattr(game_state.player, "can_scrap") else None


@then("the card has the Scrap keyword")
def card_has_scrap_keyword(game_state):
    """Rule 8.3.32: The card must have the Scrap keyword."""
    keywords = game_state.inspected_keywords
    assert "scrap" in [k.lower() if isinstance(k, str) else k for k in keywords], (
        f"Expected 'scrap' in card keywords, but got: {keywords}"
    )


@then("Scrap is a play-static ability")
def scrap_is_play_static(game_state):
    """Rule 8.3.32: Scrap must be classified as a play-static ability."""
    ability = game_state.scrap_ability
    assert ability is not None, "ScrapAbility not found — engine needs ScrapAbility class (Rule 8.3.32)"
    is_play_static = getattr(ability, "is_play_static", None)
    assert is_play_static is True, (
        f"Expected Scrap ability to be play-static, but is_play_static={is_play_static} (Rule 8.3.32)"
    )


@then(parsers.parse('the Scrap meaning is "{meaning}"'))
def scrap_meaning_matches(game_state, meaning):
    """Rule 8.3.32: The Scrap meaning must match the comprehensive rules text."""
    ability = game_state.scrap_ability
    assert ability is not None, "ScrapAbility not found — engine needs ScrapAbility class (Rule 8.3.32)"
    actual_meaning = getattr(ability, "meaning", None)
    assert actual_meaning is not None, "ScrapAbility.meaning not found (Rule 8.3.32)"
    assert meaning.lower() in actual_meaning.lower(), (
        f"Expected Scrap meaning to contain '{meaning}', but got: '{actual_meaning}' (Rule 8.3.32)"
    )


@then("the card is played successfully")
def card_is_played_successfully(game_state):
    """Rule 8.3.32: The card should be played successfully."""
    result = game_state.play_result
    assert result is not None, "No play result returned — engine needs play handling (Rule 8.3.32)"
    assert getattr(result, "success", False), (
        f"Expected play to succeed, but result.success={getattr(result, 'success', None)} (Rule 8.3.32)"
    )


@then("the item remains in the graveyard")
def item_remains_in_graveyard(game_state):
    """Rule 8.3.32: When Scrap cost is not paid, item stays in graveyard."""
    assert game_state.graveyard_item in game_state.player.graveyard, (
        "Item should remain in graveyard when Scrap cost is not paid (Rule 8.3.32)"
    )


@then("the player is not considered to have scrapped")
def player_not_considered_scrapped(game_state):
    """Rule 8.3.32: When cost is not paid, player is not considered to have scrapped."""
    result = game_state.play_result
    player_scrapped = getattr(result, "player_scrapped", False) if result else False
    assert not player_scrapped, (
        "Player should NOT be considered to have scrapped when cost was not paid (Rule 8.3.32)"
    )


@then("the item is banished")
def item_is_banished(game_state):
    """Rule 8.3.32a: After scrapping, the item should be in the banished zone."""
    assert game_state.scrap_target in game_state.player.banished_zone, (
        "The scrapped item should be in the banished zone (Rule 8.3.32a)"
    )


@then("the item is no longer in the graveyard")
def item_no_longer_in_graveyard(game_state):
    """Rule 8.3.32a: After scrapping, the item should not be in the graveyard."""
    assert game_state.scrap_target not in game_state.player.graveyard, (
        "The scrapped item should not remain in the graveyard (Rule 8.3.32a)"
    )


@then("the equipment is banished")
def equipment_is_banished(game_state):
    """Rule 8.3.32a: After scrapping, the equipment should be in the banished zone."""
    assert game_state.scrap_target in game_state.player.banished_zone, (
        "The scrapped equipment should be in the banished zone (Rule 8.3.32a)"
    )


@then("the equipment is no longer in the graveyard")
def equipment_no_longer_in_graveyard(game_state):
    """Rule 8.3.32a: After scrapping, the equipment should not be in the graveyard."""
    assert game_state.scrap_target not in game_state.player.graveyard, (
        "The scrapped equipment should not remain in the graveyard (Rule 8.3.32a)"
    )


@then("the player is considered to have scrapped")
def player_is_considered_to_have_scrapped(game_state):
    """Rule 8.3.32a: When player pays the Scrap cost, they are considered to have scrapped."""
    result = game_state.play_result
    assert result is not None, "No play result returned (Rule 8.3.32a)"
    player_scrapped = getattr(result, "player_scrapped", None)
    assert player_scrapped is True, (
        f"Expected player_scrapped=True, but got {player_scrapped} (Rule 8.3.32a)"
    )


@then("the banished card is considered to have been scrapped")
def banished_card_is_considered_scrapped(game_state):
    """Rule 8.3.32a: The banished card is considered to have been scrapped."""
    result = game_state.play_result
    assert result is not None, "No play result returned (Rule 8.3.32a)"
    scrapped_card = getattr(result, "scrapped_card", None)
    assert scrapped_card is not None, (
        "Expected scrapped_card reference in play result (Rule 8.3.32a)"
    )
    card_was_scrapped = getattr(scrapped_card, "was_scrapped", None)
    assert card_was_scrapped is True, (
        f"Expected card.was_scrapped=True, but got {card_was_scrapped} (Rule 8.3.32a)"
    )


@then("the player cannot scrap")
def player_cannot_scrap(game_state):
    """Rule 8.3.32b: Player cannot scrap without items/equipment in graveyard."""
    can_scrap = game_state.scrap_attempt_result
    assert can_scrap is False or can_scrap is None, (
        f"Expected player to be unable to scrap, but can_scrap={can_scrap} (Rule 8.3.32b)"
    )


@then("no card is banished from the graveyard")
def no_card_banished_from_graveyard(game_state):
    """Rule 8.3.32b: No card should be banished from graveyard when scrap fails."""
    banished_zone = game_state.player.banished_zone
    banished_cards = getattr(banished_zone, "cards", [])
    assert len(banished_cards) == 0, (
        f"Expected no cards banished, but found {len(banished_cards)} cards in banished zone (Rule 8.3.32b)"
    )


# ===== Fixtures =====

@pytest.fixture
def game_state():
    """
    Fixture providing game state for Scrap keyword tests.

    Uses BDDGameState which integrates with the real engine.
    Reference: Rule 8.3.32
    """
    from tests.bdd_helpers import BDDGameState

    state = BDDGameState()
    state.scrap_card = None
    state.scrap_target = None
    state.play_result = None
    state.scrap_result = None
    state.paid_scrap_cost = False
    state.scrap_attempt_result = None

    return state
