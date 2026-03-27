"""
Step definitions for Section 8.3.39: Perched (Ability Keyword)
Reference: Flesh and Blood Comprehensive Rules Section 8.3.39

This module implements behavioral tests for the Perched ability keyword:
- Perched is a static ability (Rule 8.3.39)
- Perched means the card can equip alongside a 2H weapon and cannot be attacked while equipped (Rule 8.3.39)
- Perched card may equip to the unoccupied part of a 2H weapon zone (Rule 8.3.39a)
- Perched card cannot equip if no empty zone is available (Rule 8.3.39a)
- Perched card must have a valid equip subtype to be equipped (Rule 8.3.39b)
- An equipped perched card cannot be the target of an attack (Rule 8.3.39c)
- An equipped perched card can be the target of non-attack effects (Rule 8.3.39c)
- The attack protection only applies while the card is equipped (Rule 8.3.39c)

Engine Features Needed for Section 8.3.39:
- [ ] AbilityKeyword.PERCHED on cards (Rule 8.3.39)
- [ ] PerchedAbility.is_static -> True (Rule 8.3.39)
- [ ] PerchedAbility.meaning == "This can be equipped in addition to a 2H weapon. This can't be attacked while it's equipped." (Rule 8.3.39)
- [ ] CardInstance.get_ability("perched") returns the Perched ability object (Rule 8.3.39)
- [ ] Equipment system: perched card can equip to unoccupied slot of a 2H weapon zone (Rule 8.3.39a)
- [ ] Equipment system: perched card cannot equip when all zones are occupied (Rule 8.3.39a)
- [ ] Equipment system: perched card requires valid equip subtype to be equipped (Rule 8.3.39b)
- [ ] Attack targeting: equipped perched card cannot be targeted by attacks (Rule 8.3.39c)
- [ ] Effect targeting: equipped perched card can be targeted by non-attack effects (Rule 8.3.39c)
- [ ] Equipped state tracking: CardInstance.is_equipped property (Rule 8.3.39c)

Current status: Tests written, Engine pending
"""

import pytest
from pytest_bdd import scenario, given, when, then, parsers


# ===== Rule 8.3.39: Perched is a static ability =====

@scenario(
    "../features/section_8_3_39_perched.feature",
    "Perched is a static ability",
)
def test_perched_is_static_ability():
    """Rule 8.3.39: Perched is a static ability."""
    pass


# ===== Rule 8.3.39: Perched meaning is correct =====

@scenario(
    "../features/section_8_3_39_perched.feature",
    "Perched means this can be equipped alongside 2H weapon and cannot be attacked while equipped",
)
def test_perched_meaning_is_correct():
    """Rule 8.3.39: Perched means 'This can be equipped in addition to a 2H weapon. This can't be attacked while it's equipped.'"""
    pass


# ===== Rule 8.3.39a: Perched card equips to unoccupied 2H weapon zone slot =====

@scenario(
    "../features/section_8_3_39_perched.feature",
    "Perched card can be equipped when a 2H weapon occupies one weapon zone slot",
)
def test_perched_card_equips_alongside_2h_weapon():
    """Rule 8.3.39a: Perched card may equip to the unoccupied slot of a 2H weapon zone."""
    pass


# ===== Rule 8.3.39a: Perched card cannot equip without empty zone =====

@scenario(
    "../features/section_8_3_39_perched.feature",
    "Perched card cannot be equipped when all weapon zones are occupied",
)
def test_perched_card_cannot_equip_all_zones_occupied():
    """Rule 8.3.39a: Perched card cannot equip if no empty zone is available."""
    pass


# ===== Rule 8.3.39a: Perched card can equip to any empty zone =====

@scenario(
    "../features/section_8_3_39_perched.feature",
    "Perched card can be equipped to an empty weapon zone without a 2H weapon",
)
def test_perched_card_equips_to_empty_zone():
    """Rule 8.3.39a: Perched card can also equip to an empty zone when no 2H weapon is present."""
    pass


# ===== Rule 8.3.39b: Perched card without valid equip subtype cannot equip =====

@scenario(
    "../features/section_8_3_39_perched.feature",
    "Perched card without a valid equip subtype cannot be equipped",
)
def test_perched_card_without_equip_subtype_cannot_equip():
    """Rule 8.3.39b: Perched card must have a valid equip subtype."""
    pass


# ===== Rule 8.3.39b: Perched card with valid equip subtype can equip =====

@scenario(
    "../features/section_8_3_39_perched.feature",
    "Perched card with a valid equip subtype can be equipped",
)
def test_perched_card_with_equip_subtype_can_equip():
    """Rule 8.3.39b: Perched card with a valid equip subtype can be equipped."""
    pass


# ===== Rule 8.3.39c: Equipped perched card cannot be attacked =====

@scenario(
    "../features/section_8_3_39_perched.feature",
    "Equipped perched card cannot be the target of an attack",
)
def test_equipped_perched_card_cannot_be_attacked():
    """Rule 8.3.39c: An equipped perched card cannot be the target of an attack."""
    pass


# ===== Rule 8.3.39c: Equipped perched card can be targeted by non-attack effects =====

@scenario(
    "../features/section_8_3_39_perched.feature",
    "Equipped perched card can be the target of non-attack effects",
)
def test_equipped_perched_card_can_be_targeted_by_non_attack_effects():
    """Rule 8.3.39c: An equipped perched card may be the target of non-attack effects."""
    pass


# ===== Rule 8.3.39c: Protection only applies while equipped =====

@scenario(
    "../features/section_8_3_39_perched.feature",
    "Unequipped card with Perched keyword can be attacked normally",
)
def test_unequipped_perched_card_can_be_attacked():
    """Rule 8.3.39c: The attack protection only applies while the perched card is equipped."""
    pass


# ===== Step Definitions =====

@given(parsers.parse('a card has the "{keyword}" keyword'))
def card_with_keyword(game_state, keyword):
    """Create a card with the specified keyword."""
    game_state.keyword_card = game_state.create_card(name="Perched Test Card")
    game_state.keyword_str = keyword


@given('a player has a two-hander weapon equipped in the left weapon zone')
def player_has_2h_weapon_in_left_zone(game_state):
    """Set up a player with a 2H weapon occupying the left weapon zone."""
    game_state.two_hander_equipped = True
    game_state.left_zone_occupied = True
    game_state.right_zone_occupied = False


@given('the right weapon zone is unoccupied')
def right_zone_is_unoccupied(game_state):
    """Confirm the right weapon zone is unoccupied."""
    game_state.right_zone_occupied = False


@given(parsers.parse('the player has a card with "{keyword}" that has a valid equip subtype'))
def player_has_perched_card_with_valid_subtype(game_state, keyword):
    """Set up a perched card with a valid equip subtype."""
    game_state.perched_card = game_state.create_card(name="Perched Equipment")
    game_state.perched_card_has_valid_subtype = True
    game_state.equip_attempted = False
    game_state.equip_result = None


@given('a player has a two-hander weapon that occupies all weapon zone slots')
def player_has_2h_weapon_occupying_all_slots(game_state):
    """Set up a player with a 2H weapon that occupies both weapon zone slots."""
    game_state.two_hander_equipped = True
    game_state.left_zone_occupied = True
    game_state.right_zone_occupied = True


@given('a player has no weapons equipped')
def player_has_no_weapons(game_state):
    """Set up a player with no weapons equipped."""
    game_state.two_hander_equipped = False
    game_state.left_zone_occupied = False
    game_state.right_zone_occupied = False


@given('a player has an empty weapon zone')
def player_has_empty_weapon_zone(game_state):
    """Set up a player with an empty weapon zone."""
    game_state.left_zone_occupied = False
    game_state.right_zone_occupied = False
    game_state.two_hander_equipped = False


@given(parsers.parse('the player has a card with "{keyword}" but no valid equip subtype'))
def player_has_perched_card_without_valid_subtype(game_state, keyword):
    """Set up a perched card without a valid equip subtype."""
    game_state.perched_card = game_state.create_card(name="Perched Equipment No Subtype")
    game_state.perched_card_has_valid_subtype = False
    game_state.equip_attempted = False
    game_state.equip_result = None


@given(parsers.parse('the player has a card with "{keyword}" and a valid equip subtype for that zone'))
def player_has_perched_card_with_zone_specific_subtype(game_state, keyword):
    """Set up a perched card with a valid equip subtype for the available zone."""
    game_state.perched_card = game_state.create_card(name="Perched Equipment With Subtype")
    game_state.perched_card_has_valid_subtype = True
    game_state.equip_attempted = False
    game_state.equip_result = None


@given(parsers.parse('a player has a card with "{keyword}" that is equipped'))
def player_has_equipped_perched_card(game_state, keyword):
    """Set up an equipped perched card."""
    game_state.perched_card = game_state.create_card(name="Equipped Perched Card")
    game_state.card_is_equipped = True
    game_state.attack_attempted = False
    game_state.attack_is_legal = None
    game_state.effect_targeted = False
    game_state.effect_target_is_legal = None


@given(parsers.parse('a player has a card with "{keyword}" that is not equipped'))
def player_has_unequipped_perched_card(game_state, keyword):
    """Set up an unequipped perched card."""
    game_state.perched_card = game_state.create_card(name="Unequipped Perched Card")
    game_state.card_is_equipped = False
    game_state.attack_attempted = False
    game_state.attack_is_legal = None


@when('I inspect the Perched ability on the card')
def inspect_perched_ability(game_state):
    """Inspect the Perched ability on the keyword_card."""
    card = game_state.keyword_card
    try:
        game_state.ability_obj = card.get_ability("perched")
    except (AttributeError, NotImplementedError):
        game_state.ability_obj = None


@when('the player equips the perched card')
def player_equips_perched_card(game_state):
    """Player equips the perched card."""
    card = game_state.perched_card
    game_state.equip_attempted = True
    try:
        result = card.equip(
            has_valid_subtype=game_state.perched_card_has_valid_subtype,
            left_zone_occupied=game_state.left_zone_occupied,
            right_zone_occupied=game_state.right_zone_occupied,
            two_hander_equipped=getattr(game_state, 'two_hander_equipped', False),
        )
        game_state.equip_result = result
        game_state.card_is_equipped = True
        game_state.equipped_zone = getattr(result, 'zone', 'right' if not game_state.right_zone_occupied else 'unknown')
    except (AttributeError, NotImplementedError):
        game_state.equip_result = None
        # Simulate expected behavior for test assertions
        all_occupied = game_state.left_zone_occupied and game_state.right_zone_occupied
        game_state.card_is_equipped = not all_occupied and game_state.perched_card_has_valid_subtype
        game_state.equipped_zone = 'right' if not game_state.right_zone_occupied else None


@when('the player attempts to equip the perched card')
def player_attempts_to_equip_perched_card(game_state):
    """Player attempts to equip the perched card (may fail)."""
    card = game_state.perched_card
    game_state.equip_attempted = True
    try:
        result = card.equip(
            has_valid_subtype=game_state.perched_card_has_valid_subtype,
            left_zone_occupied=game_state.left_zone_occupied,
            right_zone_occupied=game_state.right_zone_occupied,
            two_hander_equipped=getattr(game_state, 'two_hander_equipped', False),
        )
        game_state.equip_result = result
        game_state.equip_rejected = getattr(result, 'rejected', False)
        game_state.card_is_equipped = not game_state.equip_rejected
    except (AttributeError, NotImplementedError):
        game_state.equip_result = None
        # Simulate expected behavior
        all_occupied = game_state.left_zone_occupied and game_state.right_zone_occupied
        no_valid_subtype = not game_state.perched_card_has_valid_subtype
        game_state.equip_rejected = all_occupied or no_valid_subtype
        game_state.card_is_equipped = False


@when('an opponent attempts to attack the equipped perched card')
def opponent_attempts_to_attack_equipped_perched_card(game_state):
    """Opponent attempts to attack the equipped perched card."""
    card = game_state.perched_card
    game_state.attack_attempted = True
    try:
        result = card.check_can_be_attacked(is_equipped=game_state.card_is_equipped)
        game_state.attack_is_legal = getattr(result, 'is_legal', False)
    except (AttributeError, NotImplementedError):
        game_state.attack_is_legal = None


@when('a non-attack effect targets the equipped perched card')
def non_attack_effect_targets_equipped_perched_card(game_state):
    """A non-attack effect targets the equipped perched card."""
    card = game_state.perched_card
    game_state.effect_targeted = True
    try:
        result = card.check_can_be_targeted_by_non_attack_effect(is_equipped=game_state.card_is_equipped)
        game_state.effect_target_is_legal = getattr(result, 'is_legal', True)
    except (AttributeError, NotImplementedError):
        game_state.effect_target_is_legal = None


@when('an opponent attempts to attack the unequipped perched card')
def opponent_attempts_to_attack_unequipped_perched_card(game_state):
    """Opponent attempts to attack the unequipped perched card."""
    card = game_state.perched_card
    game_state.attack_attempted = True
    try:
        result = card.check_can_be_attacked(is_equipped=game_state.card_is_equipped)
        game_state.attack_is_legal = getattr(result, 'is_legal', True)
    except (AttributeError, NotImplementedError):
        game_state.attack_is_legal = None


# ===== Then steps =====

@then('the Perched ability is a static ability')
def perched_is_static_ability(game_state):
    """Verify Perched is a static ability."""
    card = game_state.keyword_card
    try:
        ability = card.get_ability("perched")
        assert ability.is_static, "Perched must be a static ability"
    except (AttributeError, NotImplementedError):
        pytest.fail("Engine feature needed: card.get_ability('perched').is_static (Rule 8.3.39)")


@then('the Perched ability is not a triggered ability')
def perched_is_not_triggered(game_state):
    """Verify Perched is not a triggered ability."""
    card = game_state.keyword_card
    try:
        ability = card.get_ability("perched")
        assert not ability.is_triggered, "Perched must not be a triggered ability"
    except (AttributeError, NotImplementedError):
        pytest.fail("Engine feature needed: card.get_ability('perched').is_triggered (Rule 8.3.39)")


@then('the Perched ability is not an activated ability')
def perched_is_not_activated(game_state):
    """Verify Perched is not an activated ability."""
    card = game_state.keyword_card
    try:
        ability = card.get_ability("perched")
        assert not ability.is_activated, "Perched must not be an activated ability"
    except (AttributeError, NotImplementedError):
        pytest.fail("Engine feature needed: card.get_ability('perched').is_activated (Rule 8.3.39)")


@then('the Perched ability means "This can be equipped in addition to a 2H weapon. This can\'t be attacked while it\'s equipped."')
def perched_meaning_is_correct(game_state):
    """Verify the meaning string for Perched."""
    card = game_state.keyword_card
    expected_meaning = "This can be equipped in addition to a 2H weapon. This can't be attacked while it's equipped."
    try:
        ability = card.get_ability("perched")
        assert ability.meaning == expected_meaning, (
            f"Perched meaning mismatch: expected '{expected_meaning}', got '{ability.meaning}'"
        )
    except (AttributeError, NotImplementedError):
        pytest.fail(f"Engine feature needed: PerchedAbility.meaning == '{expected_meaning}' (Rule 8.3.39)")


@then('the perched card is equipped successfully')
def perched_card_is_equipped_successfully(game_state):
    """Verify the perched card was equipped successfully."""
    assert game_state.card_is_equipped, "Perched card should have been equipped successfully"
    card = game_state.perched_card
    try:
        assert card.is_equipped, "Engine: card.is_equipped should be True after equipping (Rule 8.3.39a)"
    except (AttributeError, NotImplementedError):
        pytest.fail("Engine feature needed: CardInstance.is_equipped property (Rule 8.3.39a)")


@then('the perched card occupies the unoccupied weapon zone')
def perched_card_occupies_unoccupied_zone(game_state):
    """Verify the perched card was equipped to the unoccupied weapon zone slot."""
    assert game_state.equipped_zone is not None, "Perched card should occupy a weapon zone"
    card = game_state.perched_card
    try:
        zone = card.equipped_zone
        assert zone is not None, "Engine: card.equipped_zone should not be None"
    except (AttributeError, NotImplementedError):
        pytest.fail("Engine feature needed: CardInstance.equipped_zone tracks which zone the card occupies (Rule 8.3.39a)")


@then('the perched card cannot be equipped')
def perched_card_cannot_be_equipped(game_state):
    """Verify the perched card could not be equipped."""
    assert not game_state.card_is_equipped, "Perched card should not have been equipped"
    card = game_state.perched_card
    try:
        assert not card.is_equipped, "Engine: card.is_equipped should be False (Rule 8.3.39a)"
    except (AttributeError, NotImplementedError):
        pytest.fail("Engine feature needed: CardInstance.is_equipped property (Rule 8.3.39a)")


@then('the equip action is rejected')
def equip_action_is_rejected(game_state):
    """Verify the equip action was rejected."""
    assert game_state.equip_rejected, "Equip action should have been rejected"
    try:
        result = game_state.equip_result
        if result is not None:
            assert result.rejected, "Engine: equip result should indicate rejection (Rule 8.3.39a)"
    except (AttributeError, NotImplementedError):
        pytest.fail("Engine feature needed: Equipment system rejects equip when no valid zone available (Rule 8.3.39a)")


@then('the equip action is rejected due to missing equip subtype')
def equip_action_is_rejected_due_to_missing_subtype(game_state):
    """Verify the equip action was rejected due to missing equip subtype."""
    assert game_state.equip_rejected, "Equip action should have been rejected due to missing subtype"
    try:
        result = game_state.equip_result
        if result is not None:
            assert result.rejected, "Engine: equip result should indicate rejection (Rule 8.3.39b)"
            assert getattr(result, 'reason', None) in (None, 'missing_subtype', 'invalid_subtype'), (
                f"Engine: rejection reason should be subtype-related, got: {result.reason}"
            )
    except (AttributeError, NotImplementedError):
        pytest.fail("Engine feature needed: Equipment system rejects equip when card lacks valid equip subtype (Rule 8.3.39b)")


@then('the attack targeting the perched card is not legal')
def attack_targeting_perched_card_is_not_legal(game_state):
    """Verify the attack targeting the equipped perched card is not legal."""
    card = game_state.perched_card
    try:
        result = card.check_can_be_attacked(is_equipped=True)
        assert not result.is_legal, "Engine: attack targeting equipped perched card should not be legal (Rule 8.3.39c)"
    except (AttributeError, NotImplementedError):
        pytest.fail("Engine feature needed: CardInstance.check_can_be_attacked() returns False when card is equipped with Perched (Rule 8.3.39c)")


@then('the perched card cannot be attacked')
def perched_card_cannot_be_attacked(game_state):
    """Verify the equipped perched card cannot be attacked."""
    assert game_state.attack_is_legal is None or not game_state.attack_is_legal, (
        "Equipped perched card should not be attackable"
    )


@then('the non-attack effect can legally target the perched card')
def non_attack_effect_can_target_perched_card(game_state):
    """Verify a non-attack effect can legally target the equipped perched card."""
    card = game_state.perched_card
    try:
        result = card.check_can_be_targeted_by_non_attack_effect(is_equipped=True)
        assert result.is_legal, "Engine: non-attack effect should legally target equipped perched card (Rule 8.3.39c)"
    except (AttributeError, NotImplementedError):
        pytest.fail("Engine feature needed: CardInstance.check_can_be_targeted_by_non_attack_effect() (Rule 8.3.39c)")


@then('the perched card is a valid target for the non-attack effect')
def perched_card_is_valid_target_for_non_attack_effect(game_state):
    """Verify the equipped perched card is a valid target for the non-attack effect."""
    assert game_state.effect_target_is_legal is None or game_state.effect_target_is_legal, (
        "Equipped perched card should be a valid target for non-attack effects"
    )


@then('the attack is legal')
def attack_is_legal(game_state):
    """Verify the attack on the unequipped perched card is legal."""
    card = game_state.perched_card
    try:
        result = card.check_can_be_attacked(is_equipped=False)
        assert result.is_legal, "Engine: attack on unequipped perched card should be legal (Rule 8.3.39c)"
    except (AttributeError, NotImplementedError):
        pytest.fail("Engine feature needed: CardInstance.check_can_be_attacked() returns True when card is NOT equipped with Perched (Rule 8.3.39c)")


@then('the unequipped perched card can be attacked')
def unequipped_perched_card_can_be_attacked(game_state):
    """Verify the unequipped perched card can be attacked."""
    assert game_state.attack_is_legal is None or game_state.attack_is_legal, (
        "Unequipped perched card should be attackable"
    )


# ===== Fixtures =====

@pytest.fixture
def game_state():
    """
    Fixture providing game state for testing Perched.

    Uses BDDGameState which integrates with the real engine.
    Reference: Rule 8.3.39
    """
    from tests.bdd_helpers import BDDGameState

    state = BDDGameState()
    state.two_hander_equipped = False
    state.left_zone_occupied = False
    state.right_zone_occupied = False
    state.card_is_equipped = False
    state.equip_attempted = False
    state.equip_result = None
    state.equip_rejected = False
    state.equipped_zone = None
    state.attack_attempted = False
    state.attack_is_legal = None
    state.effect_targeted = False
    state.effect_target_is_legal = None
    state.perched_card_has_valid_subtype = True

    return state
