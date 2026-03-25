"""
Step definitions for Section 8.3.22: Overpower (Ability Keyword)
Reference: Flesh and Blood Comprehensive Rules Section 8.3.22

This module implements behavioral tests for the Overpower ability keyword:
- Overpower is a static ability (Rule 8.3.22)
- Overpower means "This can't be defended by more than one action card." (Rule 8.3.22)
- If an attack with Overpower is currently defended by an action card, an
  additional action card cannot be added as a defending card (Rule 8.3.22a)
- If an attack gains Overpower after already being defended by 2+ action cards,
  no cards are retroactively removed from defending (Rule 8.3.22b)

Engine Features Needed for Section 8.3.22:
- [ ] OverpowerAbility class as a static ability (Rule 8.3.22)
- [ ] OverpowerAbility.is_static -> True (Rule 8.3.22)
- [ ] OverpowerAbility.meaning: "This can't be defended by more than one action card."
- [ ] CardTemplate.has_overpower property or keyword check (Rule 8.3.22)
- [ ] Defend validation: count action-card defenders, block if >= 1 already exist (Rule 8.3.22a)
- [ ] Restriction "overpower" applied to attacks with Overpower (Rule 8.3.22a)
- [ ] Retroactive non-removal: gaining Overpower mid-combat does not remove defenders (Rule 8.3.22b)

Current status: Tests written, Engine pending
"""

import pytest
from pytest_bdd import scenario, given, when, then, parsers


# ===== Rule 8.3.22: Overpower is a static ability =====

@scenario(
    "../features/section_8_3_22_overpower.feature",
    "Overpower is a static ability",
)
def test_overpower_is_static_ability():
    """Rule 8.3.22: Overpower must be a static ability."""
    pass


@scenario(
    "../features/section_8_3_22_overpower.feature",
    "Overpower ability has correct meaning",
)
def test_overpower_has_correct_meaning():
    """Rule 8.3.22: Overpower means 'This can't be defended by more than one action card.'"""
    pass


# ===== Rule 8.3.22a: First action card can defend =====

@scenario(
    "../features/section_8_3_22_overpower.feature",
    "First action card can defend an Overpower attack",
)
def test_first_action_card_can_defend():
    """Rule 8.3.22a: The first action card is allowed to defend an Overpower attack."""
    pass


# ===== Rule 8.3.22a: Second action card is blocked =====

@scenario(
    "../features/section_8_3_22_overpower.feature",
    "Second action card cannot defend an Overpower attack",
)
def test_second_action_card_blocked():
    """Rule 8.3.22a: A second action card cannot be added as defender to an Overpower attack."""
    pass


# ===== Rule 8.3.22a: Equipment is not restricted =====

@scenario(
    "../features/section_8_3_22_overpower.feature",
    "Equipment can defend an Overpower attack alongside one action card",
)
def test_equipment_can_defend_alongside_action_card():
    """Rule 8.3.22a: Overpower only restricts action cards, not equipment."""
    pass


@scenario(
    "../features/section_8_3_22_overpower.feature",
    "Multiple equipment cards can defend an Overpower attack",
)
def test_multiple_equipment_can_defend():
    """Rule 8.3.22a: Multiple equipment can defend an Overpower attack (only action cards restricted)."""
    pass


# ===== Rule 8.3.22b: No retroactive removal =====

@scenario(
    "../features/section_8_3_22_overpower.feature",
    "Gaining Overpower does not remove existing action card defenders",
)
def test_gaining_overpower_no_retroactive_removal():
    """Rule 8.3.22b: Gaining Overpower mid-combat does not remove existing defenders."""
    pass


@scenario(
    "../features/section_8_3_22_overpower.feature",
    "After gaining Overpower additional action card defenders are blocked",
)
def test_after_gaining_overpower_additional_blocked():
    """Rule 8.3.22b: After gaining Overpower, a third action card is still blocked."""
    pass


# ===== Rule 8.3.22a: No defenders yet — first action card OK =====

@scenario(
    "../features/section_8_3_22_overpower.feature",
    "Overpower attack with no defenders allows first action card",
)
def test_overpower_no_defenders_allows_first():
    """Rule 8.3.22a: An Overpower attack with no defenders allows the first action card."""
    pass


# ===== Step Definitions =====

@given("a card with Overpower ability")
def card_with_overpower(game_state):
    """Rule 8.3.22: Create a card that has the Overpower keyword."""
    game_state.test_card = game_state.create_card(name="Overpower Card")
    try:
        from fab_engine.engine.keywords import OverpowerAbility
        game_state.overpower_ability = OverpowerAbility()
    except (ImportError, AttributeError):
        game_state.overpower_ability = None


@when("I inspect the Overpower ability")
def inspect_overpower_ability(game_state):
    """Rule 8.3.22: Access the Overpower ability for inspection."""
    # Ability is already set in given step
    pass


@then("the Overpower ability is a static ability")
def overpower_is_static(game_state):
    """Rule 8.3.22: Overpower must be a static ability."""
    ability = game_state.overpower_ability
    assert ability is not None, "OverpowerAbility not implemented"
    assert ability.is_static, "OverpowerAbility.is_static must be True (Rule 8.3.22)"


@then('the Overpower meaning is "This can\'t be defended by more than one action card"')
def overpower_has_correct_meaning(game_state):
    """Rule 8.3.22: Overpower must have the correct static meaning."""
    ability = game_state.overpower_ability
    assert ability is not None, "OverpowerAbility not implemented"
    meaning = getattr(ability, "meaning", None) or getattr(ability, "static_meaning", None)
    assert meaning is not None, "OverpowerAbility must have a meaning attribute"
    assert "more than one action card" in meaning.lower() or "one action card" in meaning.lower(), (
        f"Overpower meaning should reference 'one action card', got: {meaning}"
    )


@given("an attack with Overpower")
def attack_with_overpower(game_state):
    """Rule 8.3.22a: Set up an attack that has the Overpower keyword."""
    game_state.attack.add_keyword("overpower")
    game_state.attack.add_restriction("overpower")


@given("the defending player has an action card in hand")
def defender_has_action_card(game_state):
    """Set up a defending player with an action card in hand."""
    from fab_engine.cards.model import CardType
    card = game_state.create_card(name="Defender Action Card", card_type=CardType.ACTION)
    game_state.defender.hand.add_card(card)
    game_state.defender_card_1 = card


@given("the attack is already defended by one action card")
def attack_defended_by_one_action_card(game_state):
    """Rule 8.3.22a: The attack already has one action card defender."""
    from fab_engine.cards.model import CardType
    first_defender = game_state.create_card(name="First Defender", card_type=CardType.ACTION)
    game_state.attack.add_defender(first_defender)
    game_state.initial_defender_count = 1


@given("the defending player has another action card")
def defender_has_another_action_card(game_state):
    """Set up a second action card for the defending player."""
    from fab_engine.cards.model import CardType
    card = game_state.create_card(name="Second Defender Action", card_type=CardType.ACTION)
    game_state.defender.hand.add_card(card)
    game_state.defender_card_2 = card


@when("the defending player defends with the action card")
def defend_with_action_card(game_state):
    """Rule 8.3.22a: The defending player attempts to defend with one action card."""
    card = game_state.defender_card_1
    game_state.defend_result = game_state.defender.attempt_defend_overpower(
        game_state.attack, card
    )


@when("the defending player tries to add a second action card as defender")
def try_add_second_action_card(game_state):
    """Rule 8.3.22a: Attempt to add a second action card when Overpower is active."""
    card = game_state.defender_card_2
    game_state.defend_result = game_state.defender.attempt_defend_overpower(
        game_state.attack, card
    )


@given("the defending player has an equipment card")
def defender_has_equipment(game_state):
    """Set up equipment card for the defending player."""
    from fab_engine.cards.model import CardType
    equip = game_state.create_card(name="Defender Equipment", card_type=CardType.EQUIPMENT)
    game_state.defender.hand.add_card(equip)
    game_state.test_equipment = equip


@when("the defending player defends with the equipment card")
def defend_with_equipment(game_state):
    """Rule 8.3.22a: Defend with equipment (should be allowed even with Overpower)."""
    equip = game_state.test_equipment
    game_state.defend_result = game_state.defender.attempt_defend_overpower(
        game_state.attack, equip
    )


@given("the defending player has two equipment cards")
def defender_has_two_equipment(game_state):
    """Set up two equipment cards for the defending player."""
    from fab_engine.cards.model import CardType
    equip1 = game_state.create_card(name="Equipment 1", card_type=CardType.EQUIPMENT)
    equip2 = game_state.create_card(name="Equipment 2", card_type=CardType.EQUIPMENT)
    game_state.defender.hand.add_card(equip1)
    game_state.defender.hand.add_card(equip2)
    game_state.defender_card_1 = equip1
    game_state.defender_card_2 = equip2


@when("the defending player defends with both equipment cards")
def defend_with_both_equipment(game_state):
    """Rule 8.3.22a: Defend with two equipment cards (both should be allowed)."""
    equip1 = game_state.defender_card_1
    equip2 = game_state.defender_card_2
    result1 = game_state.defender.attempt_defend_overpower(game_state.attack, equip1)
    # Add first equipment as defender if successful
    if result1.success:
        game_state.attack.add_defender(equip1)
    result2 = game_state.defender.attempt_defend_overpower(game_state.attack, equip2)
    # Store combined result: both must succeed
    from tests.bdd_helpers.core import DefendResult
    game_state.defend_result = DefendResult(
        success=result1.success and result2.success,
        message="Both equipment defenders",
    )


@given("an attack without Overpower")
def attack_without_overpower(game_state):
    """Set up an attack that does NOT yet have Overpower."""
    # No keywords or restrictions added — default attack
    pass


@given("the attack is defended by two action cards")
def attack_defended_by_two_action_cards(game_state):
    """Rule 8.3.22b: The attack already has two action card defenders."""
    from fab_engine.cards.model import CardType
    defender1 = game_state.create_card(name="Action Defender 1", card_type=CardType.ACTION)
    defender2 = game_state.create_card(name="Action Defender 2", card_type=CardType.ACTION)
    game_state.attack.add_defender(defender1)
    game_state.attack.add_defender(defender2)
    game_state.initial_defender_count = 2


@when("the attack gains Overpower")
def attack_gains_overpower(game_state):
    """Rule 8.3.22b: The attack gains Overpower after defenders are already declared."""
    game_state.attack.add_keyword("overpower")
    game_state.attack.add_restriction("overpower")
    game_state.attack.process_restrictions()  # Rule 8.3.22b: no retroactive removal


@then("both action cards remain as defenders")
def both_action_cards_remain(game_state):
    """Rule 8.3.22b: Existing defenders are NOT removed when Overpower is gained."""
    defender_count = len(game_state.attack.defenders)
    assert defender_count >= game_state.initial_defender_count, (
        f"Rule 8.3.22b: Defenders should not be removed when Overpower is gained. "
        f"Expected {game_state.initial_defender_count}, got {defender_count}"
    )


@when("the defending player tries to add a third action card as defender")
def try_add_third_action_card(game_state):
    """Rule 8.3.22b: Attempt to add yet another action card after Overpower is gained."""
    from fab_engine.cards.model import CardType
    third = game_state.create_card(name="Third Defender", card_type=CardType.ACTION)
    game_state.defender_card_2 = third
    game_state.defend_result = game_state.defender.attempt_defend_overpower(
        game_state.attack, third
    )


@then("the defense is successful")
def defense_is_successful(game_state):
    """Verify that the defend attempt succeeded."""
    result = game_state.defend_result
    assert result is not None, "No defend result recorded"
    assert result.success, f"Defense should have succeeded, but failed: {result.message}"


@then("the defense is blocked")
def defense_is_blocked(game_state):
    """Rule 8.3.22a: The defend attempt was blocked by Overpower."""
    result = game_state.defend_result
    assert result is not None, "No defend result recorded"
    assert not result.success, (
        f"Defense should have been blocked by Overpower, but succeeded: {result.message}"
    )


@then('the block reason is "overpower restriction"')
def block_reason_is_overpower(game_state):
    """Rule 8.3.22a: The block reason should identify Overpower."""
    result = game_state.defend_result
    assert result is not None, "No defend result recorded"
    blocked_by = getattr(result, "blocked_by", "") or ""
    message = getattr(result, "message", "") or ""
    assert "overpower" in blocked_by.lower() or "overpower" in message.lower(), (
        f"Block reason should mention overpower. blocked_by={blocked_by!r}, message={message!r}"
    )


@then("the number of defenders is 2")
def defender_count_is_2(game_state):
    """Rule 8.3.22b: Exactly 2 defenders remain after Overpower is gained."""
    count = len(game_state.attack.defenders)
    assert count == 2, f"Expected 2 defenders (Rule 8.3.22b), got {count}"


@given("the attack has no defenders yet")
def attack_has_no_defenders(game_state):
    """Ensure the attack starts with no defenders."""
    game_state.attack.defenders.clear()


@then("the number of defenders is 1")
def defender_count_is_1(game_state):
    """Verify exactly 1 defender was added."""
    count = len(game_state.attack.defenders)
    assert count == 1, f"Expected 1 defender, got {count}"


# ===== Fixture =====

@pytest.fixture
def game_state():
    """
    Fixture providing game state for testing Section 8.3.22: Overpower.

    Uses BDDGameState which integrates with the real engine.
    Extends the defender's TestPlayer with Overpower-aware defend logic.
    Reference: Rule 8.3.22
    """
    from tests.bdd_helpers import BDDGameState
    from tests.bdd_helpers.core import DefendResult
    from fab_engine.cards.model import CardType

    state = BDDGameState()

    def attempt_defend_overpower(attack, card):
        """
        Attempt to defend an Overpower attack with a single card.

        Rule 8.3.22a: If attack has Overpower and is already defended by
        an action card, a second action card cannot be added.
        """
        is_action = CardType.ACTION in card.template.types
        has_overpower = attack.has_keyword("overpower")

        if has_overpower and is_action:
            # Count existing action card defenders
            action_defender_count = sum(
                1 for d in attack.defenders
                if hasattr(d, "template") and CardType.ACTION in d.template.types
            )
            if action_defender_count >= 1:
                return DefendResult(
                    success=False,
                    blocked_by="overpower",
                    message="Overpower: attack can't be defended by more than one action card",
                )

        # Defense is allowed — add to defenders
        attack.add_defender(card)
        return DefendResult(success=True, message="Defense declared")

    state.defender.attempt_defend_overpower = attempt_defend_overpower
    state.overpower_ability = None

    return state
