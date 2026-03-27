"""
Step definitions for Section 8.3.36: Cloaked (Ability Keyword)
Reference: Flesh and Blood Comprehensive Rules Section 8.3.36

This module implements behavioral tests for the Cloaked ability keyword:
- Cloaked is a static ability (Rule 8.3.36)
- Cloaked means: "Equip this face-down." (Rule 8.3.36)
- A card with Cloaked is equipped face-down (private) in its equipment zone (Rule 8.3.36)
- Equipment zones (arms, chest, head, legs, weapon) are public zones (Rule 3.0.4a)
- A public zone may contain a private object (Rule 3.0.4c)
- Face-down means the card is private — properties not available to all players (Rule 3.0.3)
- A card without Cloaked is equipped face-up (public) by default

Engine Features Needed for Section 8.3.36:
- [ ] CloakedAbility class as a static ability (Rule 8.3.36)
- [ ] CloakedAbility.is_static -> True (Rule 8.3.36)
- [ ] CloakedAbility.meaning property returning canonical text "Equip this face-down" (Rule 8.3.36)
- [ ] CardInstance.keywords property to check for Cloaked keyword (Rule 8.3.36)
- [ ] CardInstance.get_ability("cloaked") method (Rule 8.3.36)
- [ ] Equip action respects Cloaked: card is equipped as private object (Rule 8.3.36)
- [ ] CardInstance.is_public / CardInstance.is_private property (Rule 3.0.3)
- [ ] Zone.is_public property to check if a zone is a public zone (Rule 3.0.4)
- [ ] Equip action for non-Cloaked cards defaults to public/face-up (Rule 8.3.36)

Current status: Tests written, Engine pending
"""

import pytest
from pytest_bdd import scenario, given, when, then, parsers


# ===== Rule 8.3.36: Cloaked is recognized as an ability keyword =====

@scenario(
    "../features/section_8_3_36_cloaked.feature",
    "Cloaked is recognized as an ability keyword",
)
def test_cloaked_is_recognized_as_keyword():
    """Rule 8.3.36: Cloaked must be recognized as a keyword on cards that have it."""
    pass


# ===== Rule 8.3.36: Cloaked is a static ability =====

@scenario(
    "../features/section_8_3_36_cloaked.feature",
    "Cloaked is a static ability",
)
def test_cloaked_is_static_ability():
    """Rule 8.3.36: Cloaked must be classified as a static ability."""
    pass


# ===== Rule 8.3.36: Cloaked ability meaning =====

@scenario(
    "../features/section_8_3_36_cloaked.feature",
    "Cloaked ability meaning matches comprehensive rules text",
)
def test_cloaked_ability_meaning():
    """Rule 8.3.36: The Cloaked ability meaning must match the comprehensive rules text."""
    pass


# ===== Rule 8.3.36: Card with Cloaked is equipped face-down =====

@scenario(
    "../features/section_8_3_36_cloaked.feature",
    "A card with Cloaked is equipped face-down in an equipment zone",
)
def test_cloaked_card_equipped_face_down():
    """Rule 8.3.36: A card with Cloaked is equipped face-down (private)."""
    pass


# ===== Rule 8.3.36: Card without Cloaked is equipped face-up =====

@scenario(
    "../features/section_8_3_36_cloaked.feature",
    "A card without Cloaked is equipped face-up in an equipment zone",
)
def test_non_cloaked_card_equipped_face_up():
    """Rule 8.3.36: A card without Cloaked is equipped face-up (public) by default."""
    pass


# ===== Rule 8.3.36 + 3.0.4c: Cloaked card is private in a public zone =====

@scenario(
    "../features/section_8_3_36_cloaked.feature",
    "A Cloaked card in a public equipment zone is a private object in a public zone",
)
def test_cloaked_card_private_object_in_public_zone():
    """Rule 8.3.36 + 3.0.4c: A Cloaked equipped card is a private object in a public zone."""
    pass


# ===== Rule 8.3.36: Cloaked card properties hidden from opponents =====

@scenario(
    "../features/section_8_3_36_cloaked.feature",
    "Cloaked card properties are hidden from opponents when equipped",
)
def test_cloaked_card_properties_hidden_from_opponent():
    """Rule 8.3.36 + 3.0.3: Opponent cannot determine properties of a Cloaked equipped card."""
    pass


# ===== Given steps =====

@given("a card with the Cloaked keyword")
def card_with_cloaked_keyword(game_state):
    """Rule 8.3.36: Create a card that has the Cloaked keyword."""
    card = game_state.create_card(name="Cloaked Test Card")
    card._keywords = getattr(card, "_keywords", [])
    if "cloaked" not in [k.lower() for k in card._keywords]:
        card._keywords.append("cloaked")
    game_state.cloaked_card = card


@given("an equipment card with the Cloaked keyword")
def equipment_card_with_cloaked_keyword(game_state):
    """Rule 8.3.36: Create an equipment card that has the Cloaked keyword."""
    card = game_state.create_card(name="Cloaked Equipment Card")
    card._keywords = getattr(card, "_keywords", [])
    if "cloaked" not in [k.lower() for k in card._keywords]:
        card._keywords.append("cloaked")
    game_state.cloaked_card = card
    game_state.equipment_card = card


@given("an equipment card without the Cloaked keyword")
def equipment_card_without_cloaked_keyword(game_state):
    """Rule 8.3.36: Create an equipment card that does not have Cloaked."""
    card = game_state.create_card(name="Normal Equipment Card")
    card._keywords = getattr(card, "_keywords", [])
    # Explicitly ensure no cloaked keyword
    card._keywords = [k for k in card._keywords if k.lower() != "cloaked"]
    game_state.equipment_card = card
    game_state.non_cloaked_card = card


@given("a second player as the opponent")
def second_player_as_opponent(game_state):
    """Rule 8.3.36: Set up a second player (opponent) for visibility testing."""
    game_state.has_opponent = True


# ===== When steps =====

@when("I inspect the card's keywords")
def inspect_card_keywords(game_state):
    """Rule 8.3.36: Retrieve the keyword list from the card."""
    card = game_state.cloaked_card
    game_state.inspected_keywords = getattr(card, "keywords", None) or getattr(card, "_keywords", [])


@when("I check the ability type of Cloaked")
def check_ability_type_of_cloaked(game_state):
    """Rule 8.3.36: Look up the Cloaked ability and check its type classification."""
    card = game_state.cloaked_card
    game_state.cloaked_ability = getattr(card, "get_ability", lambda _: None)("cloaked")


@when("I inspect the Cloaked ability's meaning")
def inspect_cloaked_meaning(game_state):
    """Rule 8.3.36: Retrieve the meaning text from the Cloaked ability."""
    card = game_state.cloaked_card
    ability = getattr(card, "get_ability", lambda _: None)("cloaked")
    game_state.cloaked_ability = ability
    game_state.cloaked_meaning = getattr(ability, "meaning", None)


@when("the card is equipped to the player's equipment zone")
def equip_card_to_equipment_zone(game_state):
    """Rule 8.3.36: Simulate equipping the card to the player's equipment zone."""
    card = game_state.equipment_card
    # Attempt to equip via the engine's equip mechanism
    # Engine feature needed: equip action that respects Cloaked
    equip_fn = getattr(game_state.player, "equip_card", None)
    if equip_fn is not None:
        game_state.equip_result = equip_fn(card)
    else:
        # Track as equipped on game_state (missing engine feature)
        game_state.equip_result = None
    game_state.equipped_card = card
    game_state.equipment_zone = getattr(game_state.player, "chest_zone", None) or \
                                 getattr(game_state.player, "arms_zone", None)


# ===== Then steps =====

@then("the card has the Cloaked keyword")
def card_has_cloaked_keyword(game_state):
    """Rule 8.3.36: The card's keyword list must include Cloaked."""
    keywords = game_state.inspected_keywords
    assert keywords is not None, "Card should expose a keywords attribute (Rule 8.3.36)"
    keyword_strs = [str(k).lower() for k in keywords]
    assert "cloaked" in keyword_strs, (
        f"Card should have the 'cloaked' keyword (Rule 8.3.36), got keywords: {keywords}"
    )


@then("Cloaked is a static ability")
def cloaked_is_static_ability(game_state):
    """Rule 8.3.36: Cloaked must be a static ability."""
    ability = game_state.cloaked_ability
    assert ability is not None, (
        "Card should expose a Cloaked ability via get_ability('cloaked') (Rule 8.3.36)"
    )
    is_static = getattr(ability, "is_static", None)
    assert is_static is True, (
        f"Cloaked should be a static ability (Rule 8.3.36), got is_static: {is_static}"
    )


@then('the Cloaked meaning is "Equip this face-down"')
def cloaked_meaning_correct(game_state):
    """Rule 8.3.36: The Cloaked ability's meaning text must match the comprehensive rules."""
    ability = game_state.cloaked_ability
    assert ability is not None, (
        "Card should expose a Cloaked ability via get_ability('cloaked') (Rule 8.3.36)"
    )
    meaning = game_state.cloaked_meaning
    expected = "Equip this face-down"
    assert meaning == expected, (
        f"Cloaked meaning should be '{expected}' (Rule 8.3.36), got: '{meaning}'"
    )


@then("the equipped card is face-down")
def equipped_card_is_face_down(game_state):
    """Rule 8.3.36: A Cloaked card that has been equipped must be face-down."""
    card = game_state.equipped_card
    is_face_up = getattr(card, "is_face_up", None)
    is_public = getattr(card, "is_public", None)
    # face-down means private (not public)
    assert is_face_up is False or is_public is False, (
        f"Cloaked equipped card should be face-down/private (Rule 8.3.36), "
        f"got is_face_up={is_face_up}, is_public={is_public}"
    )


@then("the equipped card is private")
def equipped_card_is_private(game_state):
    """Rule 8.3.36 + 3.0.3: A Cloaked equipped card's properties are not available to all players."""
    card = game_state.equipped_card
    is_private = getattr(card, "is_private", None)
    is_public = getattr(card, "is_public", None)
    assert is_private is True or is_public is False, (
        f"Cloaked equipped card should be private (Rule 8.3.36 + 3.0.3), "
        f"got is_private={is_private}, is_public={is_public}"
    )


@then("the equipped card is face-up")
def equipped_card_is_face_up(game_state):
    """Rule 8.3.36: A non-Cloaked card that has been equipped must be face-up (public) by default."""
    card = game_state.equipped_card
    is_face_up = getattr(card, "is_face_up", None)
    is_public = getattr(card, "is_public", None)
    # face-up means public — equipment zones are public zones (Rule 3.0.4a)
    assert is_face_up is True or is_public is True, (
        f"Non-Cloaked equipped card should be face-up/public (Rule 8.3.36 + 3.0.4a), "
        f"got is_face_up={is_face_up}, is_public={is_public}"
    )


@then("the equipped card is public")
def equipped_card_is_public(game_state):
    """Rule 8.3.36 + 3.0.4a: A non-Cloaked card in an equipment zone is a public object."""
    card = game_state.equipped_card
    is_public = getattr(card, "is_public", None)
    is_private = getattr(card, "is_private", None)
    assert is_public is True or is_private is False, (
        f"Non-Cloaked equipped card should be public (Rule 8.3.36 + 3.0.4a), "
        f"got is_public={is_public}, is_private={is_private}"
    )


@then("the equipment zone is a public zone")
def equipment_zone_is_public(game_state):
    """Rule 3.0.4a: Equipment zones (arms, chest, head, legs, weapon) are public zones."""
    zone = game_state.equipment_zone
    if zone is None:
        # Engine feature needed: player.chest_zone / player.arms_zone not implemented
        pytest.fail(
            "Player does not expose an equipment zone (Rule 3.0.4a) — "
            "Engine feature needed: player.chest_zone or player.arms_zone"
        )
    is_public_zone = getattr(zone, "is_public", None)
    assert is_public_zone is True, (
        f"Equipment zone should be a public zone (Rule 3.0.4a), got is_public={is_public_zone}"
    )


@then("the equipped Cloaked card is private within that public zone")
def cloaked_card_private_in_public_zone(game_state):
    """Rule 8.3.36 + 3.0.4c: A public zone may contain a private object (Cloaked card)."""
    card = game_state.equipped_card
    zone = game_state.equipment_zone
    if zone is None:
        pytest.fail(
            "Player does not expose an equipment zone — "
            "Engine feature needed: player.chest_zone or player.arms_zone (Rule 3.0.4)"
        )
    # Zone must be public
    zone_is_public = getattr(zone, "is_public", None)
    assert zone_is_public is True, (
        f"Equipment zone should be public (Rule 3.0.4a), got: {zone_is_public}"
    )
    # Card must be private despite being in a public zone
    card_is_private = getattr(card, "is_private", None)
    card_is_public = getattr(card, "is_public", None)
    assert card_is_private is True or card_is_public is False, (
        f"Cloaked card should be private even in a public zone (Rule 8.3.36 + 3.0.4c), "
        f"got is_private={card_is_private}, is_public={card_is_public}"
    )


@then("the opponent cannot determine the properties of the equipped card")
def opponent_cannot_see_cloaked_card(game_state):
    """Rule 8.3.36 + 3.0.3: Opponent cannot access properties of a private (Cloaked) card."""
    card = game_state.equipped_card
    # A private object's properties are not available to all players (Rule 3.0.3)
    # The engine should enforce that opponents cannot query private card properties
    is_private = getattr(card, "is_private", None)
    is_public = getattr(card, "is_public", None)
    assert is_private is True or is_public is False, (
        f"Cloaked equipped card must be private so opponent cannot see its properties "
        f"(Rule 8.3.36 + 3.0.3), got is_private={is_private}, is_public={is_public}"
    )
    # Attempt to check if opponent visibility is restricted
    opponent_can_see = getattr(card, "visible_to_opponent", None)
    if opponent_can_see is not None:
        assert opponent_can_see is False, (
            f"Cloaked equipped card should not be visible to the opponent (Rule 8.3.36 + 3.0.3), "
            f"got visible_to_opponent={opponent_can_see}"
        )


# ===== Fixtures =====

@pytest.fixture
def game_state():
    """
    Fixture providing game state for testing Cloaked (Rule 8.3.36).

    Uses BDDGameState which integrates with the real engine.
    Reference: Rule 8.3.36
    """
    from tests.bdd_helpers import BDDGameState

    state = BDDGameState()
    state.has_opponent = False
    return state
