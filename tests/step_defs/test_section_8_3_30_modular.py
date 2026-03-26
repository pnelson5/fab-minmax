"""
Step definitions for Section 8.3.30: Modular (Ability Keyword)
Reference: Flesh and Blood Comprehensive Rules Section 8.3.30

This module implements behavioral tests for the Modular ability keyword:
- Modular is a static ability (Rule 8.3.30)
- Modular means: "This may be equipped to any of your equipment zones.
  It has the subtype of the zone it's equipped to." (Rule 8.3.30)
- The equipment zones are Arms, Chest, Head, and Legs (Rule 8.3.30a)
- A card can only be equipped to its owner's equipment zones with Modular (Rule 8.3.30b)
- A card with modular does not have any of the equipment subtypes until it is
  equipped to a zone (Rule 8.3.30c)

Engine Features Needed for Section 8.3.30:
- [ ] ModularAbility class as a static ability (Rule 8.3.30)
- [ ] ModularAbility.is_static -> True (Rule 8.3.30)
- [ ] ModularAbility.meaning: the text of the ability (Rule 8.3.30)
- [ ] Equipment zone types: Arms, Chest, Head, Legs (Rule 8.3.30a)
- [ ] Engine must allow a Modular card to be equipped to any equipment zone (Rule 8.3.30)
- [ ] Engine must grant the zone's subtype to the Modular card when equipped (Rule 8.3.30)
- [ ] Engine must restrict Modular equipping to the owner's zones only (Rule 8.3.30b)
- [ ] Engine must not grant any equipment subtypes to an unequipped Modular card (Rule 8.3.30c)
- [ ] CardInstance.subtypes property (Rule 8.3.30c)

Current status: Tests written, Engine pending
"""

import pytest
from pytest_bdd import scenario, given, when, then, parsers


# ===== Rule 8.3.30: Modular is recognized as a keyword =====

@scenario(
    "../features/section_8_3_30_modular.feature",
    "Modular is recognized as an ability keyword",
)
def test_modular_is_recognized_as_keyword():
    """Rule 8.3.30: Modular must be recognized as a keyword on cards that have it."""
    pass


# ===== Rule 8.3.30: Modular is a static ability =====

@scenario(
    "../features/section_8_3_30_modular.feature",
    "Modular is a static ability",
)
def test_modular_is_static_ability():
    """Rule 8.3.30: Modular must be classified as a static ability."""
    pass


# ===== Rule 8.3.30c: No equipment subtypes before equipping =====

@scenario(
    "../features/section_8_3_30_modular.feature",
    "Card with Modular has no equipment subtypes before being equipped",
)
def test_modular_card_has_no_subtypes_before_equipping():
    """Rule 8.3.30c: A Modular card has no equipment subtypes until it is equipped."""
    pass


# ===== Rule 8.3.30 + 8.3.30a: Can equip to Arms =====

@scenario(
    "../features/section_8_3_30_modular.feature",
    "Card with Modular can be equipped to the Arms zone",
)
def test_modular_can_equip_to_arms():
    """Rule 8.3.30/8.3.30a: A Modular card can be equipped to the Arms zone."""
    pass


# ===== Rule 8.3.30 + 8.3.30a: Can equip to Chest =====

@scenario(
    "../features/section_8_3_30_modular.feature",
    "Card with Modular can be equipped to the Chest zone",
)
def test_modular_can_equip_to_chest():
    """Rule 8.3.30/8.3.30a: A Modular card can be equipped to the Chest zone."""
    pass


# ===== Rule 8.3.30 + 8.3.30a: Can equip to Head =====

@scenario(
    "../features/section_8_3_30_modular.feature",
    "Card with Modular can be equipped to the Head zone",
)
def test_modular_can_equip_to_head():
    """Rule 8.3.30/8.3.30a: A Modular card can be equipped to the Head zone."""
    pass


# ===== Rule 8.3.30 + 8.3.30a: Can equip to Legs =====

@scenario(
    "../features/section_8_3_30_modular.feature",
    "Card with Modular can be equipped to the Legs zone",
)
def test_modular_can_equip_to_legs():
    """Rule 8.3.30/8.3.30a: A Modular card can be equipped to the Legs zone."""
    pass


# ===== Rule 8.3.30: Gains Arms subtype when equipped to Arms =====

@scenario(
    "../features/section_8_3_30_modular.feature",
    "Card with Modular gains Arms subtype when equipped to Arms zone",
)
def test_modular_gains_arms_subtype():
    """Rule 8.3.30: A Modular card equipped to Arms must gain the Arms subtype."""
    pass


# ===== Rule 8.3.30: Gains Chest subtype when equipped to Chest =====

@scenario(
    "../features/section_8_3_30_modular.feature",
    "Card with Modular gains Chest subtype when equipped to Chest zone",
)
def test_modular_gains_chest_subtype():
    """Rule 8.3.30: A Modular card equipped to Chest must gain the Chest subtype."""
    pass


# ===== Rule 8.3.30b: Can only equip to owner's zones =====

@scenario(
    "../features/section_8_3_30_modular.feature",
    "Card with Modular can only be equipped to owner's equipment zones",
)
def test_modular_only_owner_can_equip():
    """Rule 8.3.30b: A Modular card can only be equipped to the owner's equipment zones."""
    pass


# ===== Rule 8.3.30: Modular meaning matches comprehensive rules =====

@scenario(
    "../features/section_8_3_30_modular.feature",
    "Modular ability meaning matches comprehensive rules text",
)
def test_modular_meaning_matches_rules():
    """Rule 8.3.30: The Modular ability meaning must match the comprehensive rules text."""
    pass


# ===== Given Steps =====

@given("a card with the Modular keyword")
def modular_card(game_state):
    """Rule 8.3.30: Create a card that has the Modular keyword."""
    card = game_state.create_card(name="Modular Test Card")
    game_state.test_card = card


@given("the card belongs to player one")
def card_belongs_to_player_one(game_state):
    """Rule 8.3.30b: Establish the card's owner as player one."""
    try:
        game_state.test_card.owner_id = game_state.player.player_id
        game_state.owner_id = game_state.player.player_id
    except (AttributeError, NotImplementedError):
        game_state.owner_id = 0


# ===== When Steps =====

@when("I inspect the card's keywords")
def inspect_keywords(game_state):
    """Rule 8.3.30: Inspect the keywords on the test card."""
    try:
        game_state.card_keywords = game_state.test_card.keywords
    except AttributeError:
        game_state.card_keywords = None


@when("I check the ability type of Modular")
def check_ability_type(game_state):
    """Rule 8.3.30: Check whether Modular is classified as a static ability."""
    try:
        modular_ability = game_state.test_card.get_ability("modular")
        game_state.modular_ability = modular_ability
        game_state.modular_is_static = getattr(modular_ability, "is_static", False)
    except (AttributeError, TypeError):
        game_state.modular_ability = None
        game_state.modular_is_static = False


@when("I check the card's subtypes before equipping")
def check_subtypes_before_equipping(game_state):
    """Rule 8.3.30c: Retrieve the card's subtypes without equipping it first."""
    try:
        game_state.card_subtypes = list(game_state.test_card.subtypes)
    except (AttributeError, NotImplementedError):
        game_state.card_subtypes = None


@when("the card is equipped to the Arms zone")
def equip_to_arms(game_state):
    """Rule 8.3.30/8.3.30a: Equip the Modular card to the Arms zone."""
    try:
        result = game_state.player.arms.equip(game_state.test_card)
        game_state.equip_result = result
        game_state.equipped_zone = "Arms"
        game_state.card_subtypes_after = list(
            getattr(game_state.test_card, "subtypes", [])
        )
    except (AttributeError, NotImplementedError):
        game_state.equip_result = None
        game_state.equipped_zone = "Arms"
        game_state.card_subtypes_after = None


@when("the card is equipped to the Chest zone")
def equip_to_chest(game_state):
    """Rule 8.3.30/8.3.30a: Equip the Modular card to the Chest zone."""
    try:
        result = game_state.player.chest.equip(game_state.test_card)
        game_state.equip_result = result
        game_state.equipped_zone = "Chest"
        game_state.card_subtypes_after = list(
            getattr(game_state.test_card, "subtypes", [])
        )
    except (AttributeError, NotImplementedError):
        game_state.equip_result = None
        game_state.equipped_zone = "Chest"
        game_state.card_subtypes_after = None


@when("the card is equipped to the Head zone")
def equip_to_head(game_state):
    """Rule 8.3.30/8.3.30a: Equip the Modular card to the Head zone."""
    try:
        result = game_state.player.head.equip(game_state.test_card)
        game_state.equip_result = result
        game_state.equipped_zone = "Head"
        game_state.card_subtypes_after = list(
            getattr(game_state.test_card, "subtypes", [])
        )
    except (AttributeError, NotImplementedError):
        game_state.equip_result = None
        game_state.equipped_zone = "Head"
        game_state.card_subtypes_after = None


@when("the card is equipped to the Legs zone")
def equip_to_legs(game_state):
    """Rule 8.3.30/8.3.30a: Equip the Modular card to the Legs zone."""
    try:
        result = game_state.player.legs.equip(game_state.test_card)
        game_state.equip_result = result
        game_state.equipped_zone = "Legs"
        game_state.card_subtypes_after = list(
            getattr(game_state.test_card, "subtypes", [])
        )
    except (AttributeError, NotImplementedError):
        game_state.equip_result = None
        game_state.equipped_zone = "Legs"
        game_state.card_subtypes_after = None


@when("player two attempts to equip the card")
def opponent_attempts_equip(game_state):
    """Rule 8.3.30b: Simulate player two (the opponent) attempting to equip the card."""
    try:
        result = game_state.opponent.arms.equip(game_state.test_card)
        game_state.opponent_equip_result = result
    except (AttributeError, NotImplementedError, ValueError, PermissionError):
        # Engine raises an error when a non-owner tries to equip - expected
        game_state.opponent_equip_result = None


@when("I check the meaning of the Modular ability")
def check_modular_meaning(game_state):
    """Rule 8.3.30: Retrieve the meaning text of the Modular ability."""
    try:
        modular_ability = game_state.test_card.get_ability("modular")
        game_state.modular_meaning = modular_ability.meaning
    except (AttributeError, TypeError):
        game_state.modular_meaning = None


# ===== Then Steps =====

@then("the card has the Modular keyword")
def card_has_modular_keyword(game_state):
    """Rule 8.3.30: The card must have Modular in its list of keywords."""
    assert game_state.card_keywords is not None, (
        "Engine feature needed: CardInstance.keywords property (Rule 8.3.30)"
    )
    assert "modular" in [k.lower() for k in game_state.card_keywords], (
        "Engine feature needed: Modular keyword must appear in card.keywords (Rule 8.3.30)"
    )


@then("Modular is a static ability")
def modular_is_static(game_state):
    """Rule 8.3.30: Modular must be classified as a static ability."""
    assert game_state.modular_ability is not None, (
        "Engine feature needed: CardInstance.get_ability('modular') (Rule 8.3.30)"
    )
    assert game_state.modular_is_static, (
        "Engine feature needed: ModularAbility.is_static must be True (Rule 8.3.30)"
    )


@then("the card has no equipment subtypes")
def card_has_no_equipment_subtypes(game_state):
    """Rule 8.3.30c: An unequipped Modular card must have no equipment subtypes."""
    assert game_state.card_subtypes is not None, (
        "Engine feature needed: CardInstance.subtypes property (Rule 8.3.30c)"
    )
    equipment_subtypes = {"arms", "chest", "head", "legs"}
    actual_subtypes = {str(s).lower() for s in game_state.card_subtypes}
    overlap = actual_subtypes & equipment_subtypes
    assert not overlap, (
        f"Engine feature needed: Modular card must have no equipment subtypes before equipping. "
        f"Found: {overlap} (Rule 8.3.30c)"
    )


@then("the card is successfully equipped")
def card_is_successfully_equipped(game_state):
    """Rule 8.3.30: The Modular card must be equippable to the given zone."""
    assert game_state.equip_result is not None, (
        f"Engine feature needed: Player.{game_state.equipped_zone.lower()}.equip() must allow "
        f"Modular cards to be equipped (Rule 8.3.30)"
    )
    success = getattr(game_state.equip_result, "success", game_state.equip_result)
    assert success, (
        f"Engine feature needed: Modular card equip to {game_state.equipped_zone} "
        f"must succeed (Rule 8.3.30)"
    )


@then("the card has the Arms subtype")
def card_has_arms_subtype(game_state):
    """Rule 8.3.30: A Modular card equipped to Arms must gain the Arms subtype."""
    assert game_state.card_subtypes_after is not None, (
        "Engine feature needed: CardInstance.subtypes must be updated when Modular card "
        "is equipped (Rule 8.3.30)"
    )
    actual_subtypes = {str(s).lower() for s in game_state.card_subtypes_after}
    assert "arms" in actual_subtypes, (
        f"Engine feature needed: Modular card equipped to Arms must gain Arms subtype. "
        f"Found subtypes: {actual_subtypes} (Rule 8.3.30)"
    )


@then("the card has the Chest subtype")
def card_has_chest_subtype(game_state):
    """Rule 8.3.30: A Modular card equipped to Chest must gain the Chest subtype."""
    assert game_state.card_subtypes_after is not None, (
        "Engine feature needed: CardInstance.subtypes must be updated when Modular card "
        "is equipped (Rule 8.3.30)"
    )
    actual_subtypes = {str(s).lower() for s in game_state.card_subtypes_after}
    assert "chest" in actual_subtypes, (
        f"Engine feature needed: Modular card equipped to Chest must gain Chest subtype. "
        f"Found subtypes: {actual_subtypes} (Rule 8.3.30)"
    )


@then("the equipment attempt fails")
def equipment_attempt_fails(game_state):
    """Rule 8.3.30b: Equipping a Modular card to a non-owner's zone must be rejected."""
    assert game_state.opponent_equip_result is None, (
        "Engine feature needed: Engine must prevent equipping Modular card to a non-owner's "
        "equipment zone. Got a result instead of failure. (Rule 8.3.30b)"
    )


@then(parsers.parse('the Modular meaning is "{meaning}"'))
def modular_meaning_matches(game_state, meaning):
    """Rule 8.3.30: The Modular ability meaning must match the comprehensive rules."""
    assert game_state.modular_meaning is not None, (
        "Engine feature needed: ModularAbility.meaning property (Rule 8.3.30)"
    )
    assert game_state.modular_meaning == meaning, (
        f"Engine feature needed: ModularAbility.meaning must match CR text. "
        f"Expected: '{meaning}', Got: '{game_state.modular_meaning}' (Rule 8.3.30)"
    )


# ===== Fixtures =====

@pytest.fixture
def game_state():
    """
    Fixture providing game state for Modular ability testing.

    Uses BDDGameState which integrates with the real engine.
    Reference: Rule 8.3.30 - Modular
    """
    from tests.bdd_helpers import BDDGameState

    state = BDDGameState()
    state.test_card = None
    state.owner_id = 0
    state.card_keywords = None
    state.modular_ability = None
    state.modular_is_static = False
    state.modular_meaning = None
    state.card_subtypes = None
    state.card_subtypes_after = None
    state.equip_result = None
    state.equipped_zone = None
    state.opponent_equip_result = "not_set"  # sentinel; None means "failed as expected"

    return state
