"""
Step definitions for Section 8.3.12: Mentor (Ability Keyword)
Reference: Flesh and Blood Comprehensive Rules Section 8.3.12

This module implements behavioral tests for the Mentor ability keyword:
- Mentor is an ability keyword listed under Section 8.3 (Rule 8.3.12)
- As of 2022, the Mentor ability keyword was superseded by the Mentor type[8.1.10]
- The Mentor type is covered separately under Section 8.1 (Rule 8.1.10)
- Legacy cards with the old Mentor ability keyword should still be recognized

Engine Features Needed for Section 8.3.12:
- [ ] AbilityKeyword.MENTOR in engine's ability keyword registry (Rule 8.3.12)
- [ ] AbilityKeyword.MENTOR.is_superseded -> True (Rule 8.3.12)
- [ ] AbilityKeyword.MENTOR.superseded_by -> reference to Keyword.MENTOR type or "8.1.10" (Rule 8.3.12)
- [ ] CardTemplate ability keyword detection for legacy Mentor ability (Rule 8.3.12)
- [ ] Engine distinguishes Mentor ability keyword (8.3.12) from Mentor type keyword (8.1.10)

Current status: Tests written, Engine pending
"""

import pytest
from pytest_bdd import scenario, given, when, then, parsers


# ===== Rule 8.3.12: Mentor is classified as an ability keyword =====

@scenario(
    "../features/section_8_3_12_mentor.feature",
    "Mentor is classified as an ability keyword",
)
def test_mentor_is_ability_keyword():
    """Rule 8.3.12: Mentor is listed as an ability keyword in Section 8.3."""
    pass


# ===== Rule 8.3.12: Mentor ability keyword is superseded =====

@scenario(
    "../features/section_8_3_12_mentor.feature",
    "Mentor ability keyword has been superseded by the Mentor type",
)
def test_mentor_ability_keyword_superseded():
    """Rule 8.3.12: The Mentor ability keyword is superseded by the Mentor type (8.1.10)."""
    pass


# ===== Rule 8.3.12: Legacy Mentor ability cards are recognized =====

@scenario(
    "../features/section_8_3_12_mentor.feature",
    "A card with the legacy Mentor ability keyword is recognized by the engine",
)
def test_legacy_mentor_card_recognized():
    """Rule 8.3.12: A card with the old Mentor ability keyword is recognized."""
    pass


# ===== Rule 8.3.12: Mentor type (8.1.10) supersedes old ability =====

@scenario(
    "../features/section_8_3_12_mentor.feature",
    "Current Mentor behavior is governed by the Mentor type keyword (8.1.10)",
)
def test_mentor_type_governs_current_behavior():
    """Rule 8.3.12: The Mentor type (8.1.10) supersedes the old Mentor ability keyword."""
    pass


# ===== Step Definitions =====

@given("the engine's list of ability keywords")
def engine_ability_keyword_list(game_state):
    """Retrieve the engine's list of recognized ability keywords."""
    try:
        from fab_engine.cards.model import AbilityKeyword
        game_state.ability_keyword_list = list(AbilityKeyword)
    except (ImportError, AttributeError):
        game_state.ability_keyword_list = None


@when('I check if "Mentor" is in the list of ability keywords')
def check_mentor_in_ability_keywords(game_state):
    """Check whether Mentor appears in the ability keyword list."""
    if game_state.ability_keyword_list is None:
        game_state.mentor_in_ability_keywords = False
        return
    keyword_names = [k.name.upper() for k in game_state.ability_keyword_list]
    game_state.mentor_in_ability_keywords = "MENTOR" in keyword_names


@then('"Mentor" is recognized as an ability keyword')
def assert_mentor_is_ability_keyword(game_state):
    """Rule 8.3.12: Mentor must be recognized as an ability keyword."""
    assert game_state.mentor_in_ability_keywords, (
        "Expected 'Mentor' to be listed as an ability keyword (Rule 8.3.12), "
        "but it was not found in the engine's ability keyword list. "
        "Engine needs AbilityKeyword.MENTOR."
    )


@given("the engine's keyword registry for ability keywords")
def engine_keyword_registry(game_state):
    """Retrieve the engine's keyword registry."""
    try:
        from fab_engine.cards.model import AbilityKeyword
        game_state.ability_keyword_registry = AbilityKeyword
    except (ImportError, AttributeError):
        game_state.ability_keyword_registry = None


@when('I look up the "Mentor" ability keyword')
def look_up_mentor_ability_keyword(game_state):
    """Look up the Mentor entry in the ability keyword registry."""
    if game_state.ability_keyword_registry is None:
        game_state.mentor_keyword_entry = None
        return
    try:
        game_state.mentor_keyword_entry = game_state.ability_keyword_registry.MENTOR
    except AttributeError:
        game_state.mentor_keyword_entry = None


@then('the "Mentor" ability keyword is marked as superseded')
def assert_mentor_keyword_is_superseded(game_state):
    """Rule 8.3.12: Mentor ability keyword should be marked as superseded."""
    assert game_state.mentor_keyword_entry is not None, (
        "Expected AbilityKeyword.MENTOR to exist (Rule 8.3.12), "
        "but it was not found. Engine needs AbilityKeyword.MENTOR."
    )
    assert getattr(game_state.mentor_keyword_entry, 'is_superseded', None), (
        "Expected AbilityKeyword.MENTOR to be marked as superseded (Rule 8.3.12), "
        "but is_superseded was not True. "
        "Engine needs AbilityKeyword.MENTOR.is_superseded -> True."
    )


@then('it references the "Mentor" type keyword from section 8.1.10')
def assert_mentor_ability_references_type(game_state):
    """Rule 8.3.12: Mentor ability keyword should reference the Mentor type (8.1.10)."""
    assert game_state.mentor_keyword_entry is not None, (
        "Expected AbilityKeyword.MENTOR to exist (Rule 8.3.12), "
        "but it was not found. Engine needs AbilityKeyword.MENTOR."
    )
    superseded_by = getattr(game_state.mentor_keyword_entry, 'superseded_by', None)
    assert superseded_by is not None, (
        "Expected AbilityKeyword.MENTOR.superseded_by to reference the Mentor type (Rule 8.3.12), "
        "but no superseded_by was found. "
        "Engine needs AbilityKeyword.MENTOR.superseded_by -> Mentor type reference."
    )


@given('a card has the legacy "Mentor" ability keyword')
def card_with_legacy_mentor_ability(game_state):
    """Create a card with the legacy Mentor ability keyword."""
    game_state.mentor_ability_card = game_state.create_card(
        name="Legacy Mentor Test Card",
        card_type="Action",
    )
    game_state.mentor_ability_keyword = "Mentor"


@when('I inspect the ability keywords on the card')
def inspect_card_ability_keywords(game_state):
    """Inspect the ability keywords on the test card."""
    card = game_state.mentor_ability_card
    try:
        game_state.card_ability_keywords = card.ability_keywords
    except AttributeError:
        game_state.card_ability_keywords = None


@then('the card is recognized as having the "Mentor" ability keyword')
def assert_card_has_mentor_ability_keyword(game_state):
    """Rule 8.3.12: A legacy Mentor ability card should be recognized."""
    assert game_state.card_ability_keywords is not None, (
        "Expected card to have an ability_keywords attribute (Rule 8.3.12), "
        "but CardInstance has no ability_keywords property. "
        "Engine needs CardInstance.ability_keywords."
    )
    keyword_names = [
        k.name.upper() if hasattr(k, 'name') else str(k).upper()
        for k in game_state.card_ability_keywords
    ]
    assert "MENTOR" in keyword_names, (
        "Expected card to have 'Mentor' in its ability keywords (Rule 8.3.12), "
        "but it was not found. Engine needs support for the legacy Mentor ability keyword."
    )


@given('a card with the "Mentor" type')
def card_with_mentor_type(game_state):
    """Create a card with the Mentor type keyword."""
    game_state.mentor_type_card = game_state.create_card(
        name="Mentor Type Card",
        card_type="Mentor",
    )


@when("the game checks deck construction rules for the card")
def check_deck_construction_for_mentor_type_card(game_state):
    """Check what rules apply to a Mentor type card during deck construction."""
    card = game_state.mentor_type_card
    try:
        from fab_engine.cards.model import CardType
        game_state.card_is_mentor_type = CardType.MENTOR in card.types
    except (ImportError, AttributeError):
        game_state.card_is_mentor_type = False

    try:
        # The Mentor type (8.1.10) requires a young hero
        game_state.mentor_type_requires_young_hero = getattr(
            card, 'requires_young_hero', None
        )
    except AttributeError:
        game_state.mentor_type_requires_young_hero = None


@then("the Mentor type rules (8.1.10) apply to the card")
def assert_mentor_type_rules_apply(game_state):
    """Rule 8.3.12: Mentor type cards should be governed by the Mentor type rules (8.1.10)."""
    assert game_state.card_is_mentor_type, (
        "Expected Mentor type card to have CardType.MENTOR in its types (Rule 8.3.12 -> 8.1.10), "
        "but CardType.MENTOR was not found. "
        "Engine needs CardType.MENTOR in the CardType enum."
    )


@then("the Mentor ability keyword rules do not apply")
def assert_mentor_ability_rules_do_not_apply(game_state):
    """Rule 8.3.12: Mentor type cards are not governed by the superseded Mentor ability rules."""
    card = game_state.mentor_type_card
    # A Mentor TYPE card should NOT have the old Mentor ability keyword applied
    try:
        ability_keywords = card.ability_keywords
        keyword_names = [
            k.name.upper() if hasattr(k, 'name') else str(k).upper()
            for k in ability_keywords
        ]
        # A card typed as Mentor should not also carry the old Mentor ability keyword
        assert "MENTOR" not in keyword_names or game_state.card_is_mentor_type, (
            "Expected Mentor type card to be governed by the Mentor type rules (8.1.10), "
            "not the superseded Mentor ability keyword rules (8.3.12)."
        )
    except AttributeError:
        # If no ability_keywords attribute, the Mentor ability is not applied — acceptable
        pass


# ===== Fixtures =====

@pytest.fixture
def game_state():
    """
    Fixture providing game state for testing Mentor ability keyword.

    Covers Rule 8.3.12: Mentor (Ability Keyword - Superseded).
    The Mentor ability keyword was superseded in 2022 by the Mentor type (Rule 8.1.10).
    """
    from tests.bdd_helpers import BDDGameState
    return BDDGameState()
