"""
Step definitions for Section 8.3.4: Dominate (Ability Keyword)
Reference: Flesh and Blood Comprehensive Rules Section 8.3.4

This module implements behavioral tests for the Dominate ability keyword:
- Dominate is a static ability (Rule 8.3.4)
- Dominate means "This can't be defended by more than one card from hand" (Rule 8.3.4)
- Second hand card cannot be added as defender (Rule 8.3.4a)
- Defense reactions from hand are blocked when hand defender exists (Rule 8.3.4b)
- Gaining Dominate does not retroactively remove existing hand defenders (Rule 8.3.4c)

Engine Features Needed for Section 8.3.4:
- [ ] AbilityKeyword.DOMINATE static ability on cards (Rule 8.3.4)
- [ ] DominateAbility.is_static -> True (Rule 8.3.4)
- [ ] DominateAbility.meaning — "This can't be defended by more than one card from hand" (Rule 8.3.4)
- [ ] AttackChainLink.add_defender(card, from_hand) — tracks hand-origin of defenders (Rule 8.3.4a)
- [ ] AttackChainLink.hand_defender_count — count of defending cards that came from hand (Rule 8.3.4a)
- [ ] DominateAbility prevents adding 2nd+ hand card as defender (Rule 8.3.4a)
- [ ] DominateAbility prevents playing defense reactions from hand when hand defender exists (Rule 8.3.4b)
- [ ] AttackChainLink.gain_keyword(keyword) — applies keyword mid-combat (Rule 8.3.4c)
- [ ] Gaining Dominate does NOT retroactively remove existing hand defenders (Rule 8.3.4c)

Current status: Tests written, Engine pending
"""

import pytest
from pytest_bdd import scenario, given, when, then, parsers
from typing import Optional, Any


# ===== Rule 8.3.4: Dominate is a static ability =====

@scenario(
    "../features/section_8_3_4_dominate.feature",
    "Dominate is a static ability",
)
def test_dominate_is_static_ability():
    """Rule 8.3.4: The Dominate ability is a static ability."""
    pass


@scenario(
    "../features/section_8_3_4_dominate.feature",
    "Dominate ability has the correct meaning",
)
def test_dominate_ability_meaning():
    """Rule 8.3.4: Dominate means 'This can't be defended by more than one card from hand'."""
    pass


# ===== Rule 8.3.4a: Second hand card cannot be added =====

@scenario(
    "../features/section_8_3_4_dominate.feature",
    "A second hand card cannot be added to defend a Dominate attack",
)
def test_second_hand_card_rejected_by_dominate():
    """Rule 8.3.4a: Once a hand card defends a Dominate attack, no more hand cards can be added."""
    pass


@scenario(
    "../features/section_8_3_4_dominate.feature",
    "A first hand card can defend a Dominate attack normally",
)
def test_first_hand_card_can_defend_dominate_attack():
    """Rule 8.3.4a: The first hand card can still defend a Dominate attack."""
    pass


@scenario(
    "../features/section_8_3_4_dominate.feature",
    "Non-hand defender can be added even when Dominate attack has a hand defender",
)
def test_non_hand_defender_allowed_with_dominate():
    """Rule 8.3.4a: Dominate restricts hand cards only; non-hand defenders are unaffected."""
    pass


# ===== Rule 8.3.4b: Defense reactions from hand are blocked =====

@scenario(
    "../features/section_8_3_4_dominate.feature",
    "Defense reaction from hand cannot be played when Dominate attack has a hand defender",
)
def test_defense_reaction_from_hand_blocked_by_dominate():
    """Rule 8.3.4b: Defense reactions from hand are blocked when a hand card already defends."""
    pass


@scenario(
    "../features/section_8_3_4_dominate.feature",
    "Defense reaction can be played when Dominate attack has no hand defender yet",
)
def test_defense_reaction_allowed_when_no_hand_defender():
    """Rule 8.3.4b: Defense reactions from hand are allowed when no hand card defends yet."""
    pass


# ===== Rule 8.3.4c: Gaining Dominate does not retroactively remove defenders =====

@scenario(
    "../features/section_8_3_4_dominate.feature",
    "Gaining Dominate does not remove existing hand defenders",
)
def test_gaining_dominate_does_not_remove_existing_defenders():
    """Rule 8.3.4c: Dominate gained mid-combat does not retroactively remove hand defenders."""
    pass


@scenario(
    "../features/section_8_3_4_dominate.feature",
    "Gaining Dominate prevents additional hand defenders after being gained",
)
def test_gaining_dominate_prevents_further_hand_defenders():
    """Rule 8.3.4c: After gaining Dominate, no additional hand cards can be added as defenders."""
    pass


# ===== Step Definitions =====

@given('a card with the "Dominate" keyword ability')
def dominate_card(game_state):
    """Set up a card with the Dominate keyword ability."""
    card = game_state.create_card(
        name="Dominate Test Attack",
        card_type="Action",
    )
    game_state.dominate_card = card


@given('an attack with the "Dominate" keyword')
def attack_with_dominate(game_state):
    """Set up an attack that has the Dominate keyword."""
    attack_card = game_state.create_card(
        name="Dominate Test Attack",
        card_type="Action",
    )
    attack = game_state.create_attack_proxy(source=attack_card)
    attack.add_keyword("Dominate")
    game_state.dominate_attack = attack
    game_state.dominate_attack_hand_defenders = 0


@given('an attack with the "Dominate" keyword on the activate chain link')
def attack_with_dominate_on_activate_chain_link(game_state):
    """Set up a Dominate attack on the activate chain link (during defend/reaction step)."""
    attack_card = game_state.create_card(
        name="Dominate Test Attack",
        card_type="Action",
    )
    attack = game_state.create_attack_proxy(source=attack_card)
    attack.add_keyword("Dominate")
    game_state.dominate_attack = attack
    game_state.dominate_attack_hand_defenders = 0
    game_state.attack_on_activate_chain_link = True


@given('an attack that does not have the "Dominate" keyword')
def attack_without_dominate(game_state):
    """Set up an attack without the Dominate keyword (will gain it later)."""
    attack_card = game_state.create_card(
        name="Non-Dominate Test Attack",
        card_type="Action",
    )
    attack = game_state.create_attack_proxy(source=attack_card)
    game_state.dominate_attack = attack
    game_state.dominate_attack_hand_defenders = 0


@given('the attack is already defended by one card from the defending player\'s hand')
def attack_defended_by_one_hand_card(game_state):
    """Record that one hand card is already defending the attack."""
    defender = game_state.create_card(name="Defender Card 1", card_type="Action")
    game_state.first_hand_defender = defender
    try:
        game_state.dominate_attack.add_defender(defender)
        game_state.dominate_attack_hand_defenders = 1
    except (AttributeError, NotImplementedError):
        game_state.dominate_attack_hand_defenders = 1
        game_state.missing_engine_feature = (
            "TestAttack.add_defender() with hand-origin tracking not implemented"
        )


@given('the attack has no defending cards yet')
def attack_has_no_defenders(game_state):
    """Set up the attack with no defending cards."""
    game_state.dominate_attack_hand_defenders = 0


@given('the attack is already defended by two cards from the defending player\'s hand')
def attack_defended_by_two_hand_cards(game_state):
    """Record that two hand cards are already defending the attack."""
    defender1 = game_state.create_card(name="Defender Card 1", card_type="Action")
    defender2 = game_state.create_card(name="Defender Card 2", card_type="Action")
    game_state.first_hand_defender = defender1
    game_state.second_hand_defender = defender2
    try:
        game_state.dominate_attack.add_defender(defender1)
        game_state.dominate_attack.add_defender(defender2)
        game_state.dominate_attack_hand_defenders = 2
    except (AttributeError, NotImplementedError):
        game_state.dominate_attack_hand_defenders = 2
        game_state.missing_engine_feature = (
            "TestAttack.add_defender() not implemented"
        )


@when('I inspect the Dominate ability on the card')
def inspect_dominate_ability(game_state):
    """Attempt to retrieve the Dominate ability from the card."""
    card = game_state.dominate_card
    try:
        ability = card.get_keyword_ability("Dominate")
        game_state.dominate_ability = ability
    except (AttributeError, NotImplementedError):
        game_state.dominate_ability = None
        game_state.missing_engine_feature = (
            "CardInstance.get_keyword_ability('Dominate') not implemented"
        )


@when('the defending player attempts to add a second card from hand as a defender')
def attempt_add_second_hand_defender(game_state):
    """Attempt to add a second hand card as a defender against a Dominate attack."""
    second_defender = game_state.create_card(name="Second Defender Card", card_type="Action")
    game_state.second_hand_defender = second_defender
    attack = game_state.dominate_attack
    try:
        result = attack.add_hand_defender(second_defender)
        game_state.defend_result = result
    except (AttributeError, NotImplementedError):
        # Try generic defender addition
        try:
            result = attack.add_defender(second_defender)
            game_state.defend_result = result
        except (AttributeError, NotImplementedError):
            game_state.defend_result = None
            game_state.missing_engine_feature = (
                "AttackChainLink.add_defender() / Dominate restriction not implemented (Rule 8.3.4a)"
            )


@when('the defending player attempts to defend with one card from hand')
def attempt_defend_with_one_hand_card(game_state):
    """Attempt to defend with the first hand card against a Dominate attack."""
    defender = game_state.create_card(name="First Defender Card", card_type="Action")
    game_state.first_hand_defender = defender
    attack = game_state.dominate_attack
    try:
        result = attack.add_hand_defender(defender)
        game_state.defend_result = result
    except (AttributeError, NotImplementedError):
        try:
            result = attack.add_defender(defender)
            game_state.defend_result = result
        except (AttributeError, NotImplementedError):
            game_state.defend_result = None
            game_state.missing_engine_feature = (
                "AttackChainLink.add_defender() not implemented (Rule 8.3.4a)"
            )


@when('the defending player attempts to add a card that does not come from hand as a defender')
def attempt_add_non_hand_defender(game_state):
    """Attempt to add a non-hand card (e.g., equipment) as a defender."""
    non_hand_defender = game_state.create_card(name="Equipment Defender", card_type="Equipment")
    game_state.non_hand_defender = non_hand_defender
    attack = game_state.dominate_attack
    try:
        result = attack.add_non_hand_defender(non_hand_defender)
        game_state.defend_result = result
    except (AttributeError, NotImplementedError):
        game_state.defend_result = None
        game_state.missing_engine_feature = (
            "AttackChainLink.add_non_hand_defender() / non-hand defender tracking "
            "not implemented (Rule 8.3.4a)"
        )


@when('the defending player attempts to play a defense reaction from hand')
def attempt_play_defense_reaction_from_hand(game_state):
    """Attempt to play a defense reaction card from hand against a Dominate attack."""
    defense_reaction = game_state.create_card(
        name="Defense Reaction Test Card",
        card_type="Instant",
    )
    game_state.defense_reaction_card = defense_reaction
    attack = game_state.dominate_attack

    try:
        result = attack.play_defense_reaction_from_hand(defense_reaction)
        game_state.defense_reaction_result = result
    except (AttributeError, NotImplementedError):
        game_state.defense_reaction_result = None
        game_state.missing_engine_feature = (
            "AttackChainLink.play_defense_reaction_from_hand() / "
            "Dominate defense reaction restriction not implemented (Rule 8.3.4b)"
        )


@when('the attack gains the "Dominate" keyword')
def attack_gains_dominate(game_state):
    """Apply the Dominate keyword to an attack that didn't have it initially."""
    attack = game_state.dominate_attack
    try:
        attack.add_keyword("Dominate")
        game_state.dominate_gained_mid_combat = True
    except (AttributeError, NotImplementedError):
        game_state.dominate_gained_mid_combat = False
        game_state.missing_engine_feature = (
            "TestAttack.add_keyword('Dominate') / dynamic keyword granting not implemented"
        )


@when('the defending player attempts to add another card from hand as a defender')
def attempt_add_another_hand_defender_after_dominate(game_state):
    """Attempt to add another hand card as defender after the attack gains Dominate."""
    another_defender = game_state.create_card(
        name="Additional Defender Card", card_type="Action"
    )
    game_state.additional_hand_defender = another_defender
    attack = game_state.dominate_attack
    try:
        result = attack.add_hand_defender(another_defender)
        game_state.additional_defend_result = result
    except (AttributeError, NotImplementedError):
        try:
            result = attack.add_defender(another_defender)
            game_state.additional_defend_result = result
        except (AttributeError, NotImplementedError):
            game_state.additional_defend_result = None
            game_state.missing_engine_feature = (
                "AttackChainLink.add_defender() / Dominate restriction after gaining keyword "
                "not implemented (Rule 8.3.4c)"
            )


# ===== Then Steps =====

@then('the Dominate ability is a static ability')
def dominate_ability_is_static(game_state):
    """Rule 8.3.4: Dominate is a static ability."""
    if game_state.dominate_ability is None:
        pytest.fail(
            "Engine Feature Needed: CardInstance.get_keyword_ability('Dominate') / "
            "AbilityKeyword.DOMINATE not implemented (Rule 8.3.4)"
        )
    ability = game_state.dominate_ability
    try:
        assert ability.is_static, (
            "Dominate should be a static ability"
        )
    except (AttributeError, NotImplementedError):
        pytest.fail(
            "Engine Feature Needed: Ability.is_static not implemented (Rule 8.3.4)"
        )


@then('the Dominate ability means "This can\'t be defended by more than one card from hand"')
def dominate_ability_has_correct_meaning(game_state):
    """Rule 8.3.4: Dominate's meaning is a specific static ability text."""
    if game_state.dominate_ability is None:
        pytest.fail(
            "Engine Feature Needed: CardInstance.get_keyword_ability('Dominate') / "
            "AbilityKeyword.DOMINATE not implemented (Rule 8.3.4)"
        )
    ability = game_state.dominate_ability
    try:
        meaning = ability.meaning
        assert "defended" in meaning.lower(), (
            f"Dominate meaning should reference 'defended', got: {meaning}"
        )
        assert "one" in meaning.lower() or "more than one" in meaning.lower(), (
            f"Dominate meaning should reference limiting to one defender, got: {meaning}"
        )
        assert "hand" in meaning.lower(), (
            f"Dominate meaning should reference 'hand', got: {meaning}"
        )
    except (AttributeError, NotImplementedError):
        pytest.fail(
            "Engine Feature Needed: DominateAbility.meaning not implemented (Rule 8.3.4)"
        )


@then('the defend attempt is rejected')
def defend_attempt_is_rejected(game_state):
    """Rule 8.3.4a: The attempt to add a second hand defender is rejected."""
    result = game_state.defend_result
    if result is None:
        pytest.fail(
            "Engine Feature Needed: AttackChainLink.add_defender() / "
            "Dominate restriction logic not implemented (Rule 8.3.4a)"
        )
    try:
        assert not result.success, (
            "Dominate should reject adding a second hand card as defender"
        )
    except (AttributeError, NotImplementedError):
        pytest.fail(
            "Engine Feature Needed: DefendResult.success attribute not implemented (Rule 8.3.4a)"
        )


@then('the attack still has exactly one defending card from hand')
def attack_has_exactly_one_hand_defender(game_state):
    """Rule 8.3.4a: Only one hand card defends the Dominate attack."""
    attack = game_state.dominate_attack
    try:
        count = attack.hand_defender_count
        assert count == 1, (
            f"Dominate attack should have exactly 1 hand defender, got: {count}"
        )
    except (AttributeError, NotImplementedError):
        pytest.fail(
            "Engine Feature Needed: AttackChainLink.hand_defender_count "
            "not implemented (Rule 8.3.4a)"
        )


@then('the defend attempt succeeds')
def defend_attempt_succeeds(game_state):
    """The defend attempt was accepted."""
    result = game_state.defend_result
    if result is None:
        pytest.fail(
            "Engine Feature Needed: AttackChainLink.add_defender() not implemented (Rule 8.3.4a)"
        )
    try:
        assert result.success, (
            "First hand card should be able to defend a Dominate attack"
        )
    except (AttributeError, NotImplementedError):
        pytest.fail(
            "Engine Feature Needed: DefendResult.success attribute not implemented (Rule 8.3.4a)"
        )


@then('the attack has one defending card from hand')
def attack_has_one_hand_defender(game_state):
    """Rule 8.3.4a: The first hand card is registered as a defender."""
    attack = game_state.dominate_attack
    try:
        count = attack.hand_defender_count
        assert count == 1, (
            f"Dominate attack should have exactly 1 hand defender, got: {count}"
        )
    except (AttributeError, NotImplementedError):
        pytest.fail(
            "Engine Feature Needed: AttackChainLink.hand_defender_count "
            "not implemented (Rule 8.3.4a)"
        )


@then('the defense reaction play is rejected')
def defense_reaction_play_rejected(game_state):
    """Rule 8.3.4b: Playing a defense reaction from hand is rejected by Dominate."""
    result = game_state.defense_reaction_result
    if result is None:
        pytest.fail(
            "Engine Feature Needed: AttackChainLink.play_defense_reaction_from_hand() / "
            "Dominate defense reaction restriction not implemented (Rule 8.3.4b)"
        )
    try:
        assert not result.success, (
            "Dominate should reject playing defense reactions from hand when hand card already defends"
        )
    except (AttributeError, NotImplementedError):
        pytest.fail(
            "Engine Feature Needed: PlayResult.success attribute not implemented (Rule 8.3.4b)"
        )


@then('the defense reaction play succeeds')
def defense_reaction_play_succeeds(game_state):
    """Rule 8.3.4b: Playing a defense reaction from hand is allowed when no hand card defends yet."""
    result = game_state.defense_reaction_result
    if result is None:
        pytest.fail(
            "Engine Feature Needed: AttackChainLink.play_defense_reaction_from_hand() "
            "not implemented (Rule 8.3.4b)"
        )
    try:
        assert result.success, (
            "Defense reaction from hand should be allowed when no hand card defends a Dominate attack"
        )
    except (AttributeError, NotImplementedError):
        pytest.fail(
            "Engine Feature Needed: PlayResult.success attribute not implemented (Rule 8.3.4b)"
        )


@then('both defending cards remain as defenders')
def both_defending_cards_remain(game_state):
    """Rule 8.3.4c: Gaining Dominate does not remove existing hand defenders."""
    attack = game_state.dominate_attack
    try:
        count = attack.defender_count
        assert count >= 2, (
            f"Both hand defenders should still be defending after attack gains Dominate, "
            f"got {count} defenders"
        )
    except (AttributeError, NotImplementedError):
        pytest.fail(
            "Engine Feature Needed: AttackChainLink.defender_count not implemented (Rule 8.3.4c)"
        )


@then('no cards are retroactively removed from defending')
def no_cards_retroactively_removed(game_state):
    """Rule 8.3.4c: Dominate does not retroactively alter the defending state."""
    attack = game_state.dominate_attack
    try:
        count = attack.defender_count
        assert count == 2, (
            f"Retroactive removal should not occur — expected 2 defenders, got {count}"
        )
    except (AttributeError, NotImplementedError):
        pytest.fail(
            "Engine Feature Needed: AttackChainLink.defender_count not implemented (Rule 8.3.4c)"
        )


@then('the additional defend attempt is rejected')
def additional_defend_attempt_rejected(game_state):
    """Rule 8.3.4c: After gaining Dominate, no additional hand cards can defend."""
    result = game_state.additional_defend_result
    if result is None:
        pytest.fail(
            "Engine Feature Needed: AttackChainLink.add_defender() / "
            "Dominate restriction after gaining keyword not implemented (Rule 8.3.4c)"
        )
    try:
        assert not result.success, (
            "Dominate should prevent adding further hand defenders after gaining the keyword"
        )
    except (AttributeError, NotImplementedError):
        pytest.fail(
            "Engine Feature Needed: DefendResult.success attribute not implemented (Rule 8.3.4c)"
        )


# ===== Fixtures =====

@pytest.fixture
def game_state():
    """
    Fixture providing game state for testing Dominate.

    Uses BDDGameState which integrates with the real engine.
    Reference: Rule 8.3.4 - Dominate keyword ability.
    """
    from tests.bdd_helpers import BDDGameState

    state = BDDGameState()
    state.dominate_card = None
    state.dominate_ability = None
    state.dominate_attack = None
    state.dominate_attack_hand_defenders = 0
    state.first_hand_defender = None
    state.second_hand_defender = None
    state.non_hand_defender = None
    state.defense_reaction_card = None
    state.defend_result = None
    state.defense_reaction_result = None
    state.additional_defend_result = None
    state.additional_hand_defender = None
    state.dominate_gained_mid_combat = False
    state.attack_on_activate_chain_link = False
    state.missing_engine_feature = None

    return state
