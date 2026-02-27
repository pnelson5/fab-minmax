"""
Step definitions for Section 2.4: Intellect
Reference: Flesh and Blood Comprehensive Rules Section 2.4

This module implements behavioral tests for the intellect property of hero
cards in Flesh and Blood.

Rule 2.4.1: Intellect is a numeric property of a hero card, which represents
            the number of cards the controlling player draws up to at the end
            of their turn. [4.4]

Rule 2.4.2: The printed intellect of a card is typically located at the bottom
            left corner of a card next to the {i} symbol. The printed intellect
            defines the base intellect of a card. If a card does not have a
            printed intellect, it does not have the intellect property
            (0 is a valid printed intellect).

Rule 2.4.3: The intellect of an object can be modified. The term "intellect"
            or the symbol {i} refers to the modified intellect of an object.

Engine Features Needed for Section 2.4:
- [ ] `CardInstance.has_intellect_property` property: True only if printed intellect exists (Rule 2.4.2)
- [ ] `CardInstance.base_intellect` property returning the unmodified printed intellect (Rule 2.4.2)
- [ ] `CardInstance.effective_intellect` (or `intellect`) returning the modified intellect (Rule 2.4.3)
- [ ] Intellect is exclusive to hero cards (Rule 2.4.1)
- [ ] End-of-turn draw-up-to logic using effective intellect (Rule 2.4.1)
- [ ] Intellect modification effects that increase/decrease effective intellect (Rule 2.4.3)
- [ ] Numeric intellect capped at zero (cross-ref Rule 2.0.3c)
"""

import pytest
from pytest_bdd import scenario, given, when, then, parsers
from dataclasses import dataclass, field
from typing import Optional


# ---------------------------------------------------------------------------
# Stub classes for testing Section 2.4 rules
# ---------------------------------------------------------------------------


@dataclass
class IntellectCheckResultStub:
    """
    Result of checking a card's intellect property.

    Rule 2.4.1: Intellect is a numeric property of a hero card.
    Rule 2.4.2: Printed intellect defines base intellect; no printed intellect = no property.
    """

    has_intellect_property: bool
    intellect_value: Optional[int]  # None if no intellect property
    is_numeric: bool = True


@dataclass
class IntellectCardStub:
    """
    Stub representing a hero card with an intellect property.

    Models what the engine must implement for Section 2.4.
    Engine Features Needed:
    - [ ] CardInstance.base_intellect: unmodified printed intellect (Rule 2.4.2)
    - [ ] CardInstance.has_intellect_property: True only if printed intellect exists (Rule 2.4.2)
    - [ ] CardInstance.effective_intellect: modified intellect for rule/effect references (Rule 2.4.3)
    - [ ] Intellect is a hero-card-only property (Rule 2.4.1)
    """

    name: str = "Test Hero"
    printed_intellect: Optional[int] = None  # None if card has no intellect property
    intellect_modifier: int = 0  # Applied by effects (Rule 2.4.3)
    is_hero: bool = True  # Rule 2.4.1: Intellect is only on hero cards

    @property
    def has_intellect_property(self) -> bool:
        """Rule 2.4.2: Card has intellect property only if there is a printed intellect."""
        return self.printed_intellect is not None

    @property
    def base_intellect(self) -> Optional[int]:
        """Rule 2.4.2: Base intellect is the printed intellect."""
        return self.printed_intellect

    @property
    def effective_intellect(self) -> Optional[int]:
        """
        Rule 2.4.3: The modified intellect of the object.

        The term "intellect" or the symbol {i} refers to this value.
        Capped at zero (cross-ref Rule 2.0.3c).
        """
        if self.printed_intellect is None:
            return None
        return max(0, self.printed_intellect + self.intellect_modifier)

    def check_intellect(self) -> IntellectCheckResultStub:
        """Rule 2.4.1/2.4.2: Get the intellect property of this card."""
        return IntellectCheckResultStub(
            has_intellect_property=self.has_intellect_property,
            intellect_value=self.effective_intellect,
            is_numeric=True,
        )

    def apply_intellect_boost(self, amount: int):
        """
        Rule 2.4.3: Apply a positive intellect modification from an effect.

        Engine Feature Needed: Effect system applying intellect modifications.
        """
        self.intellect_modifier += amount

    def apply_intellect_reduction(self, amount: int):
        """
        Rule 2.4.3: Apply a negative intellect modification from an effect.

        Engine Feature Needed: Effect system applying intellect reductions.
        """
        self.intellect_modifier -= amount


@dataclass
class EndOfTurnDrawResultStub:
    """
    Result of resolving the end-of-turn draw for a player.

    Rule 2.4.1: Intellect represents the number of cards drawn up to at end of turn.
    The player draws cards up to their current (modified) intellect value.
    """

    cards_drawn_up_to: int  # The number the player draws up to (modified intellect)
    intellect_used: int  # The intellect value that was used


@dataclass
class IntellectModificationResultStub:
    """
    Result of resolving the modified intellect of an object.

    Rule 2.4.3: The term "intellect" or {i} refers to the modified intellect.
    """

    modified_intellect: int
    base_intellect: int
    is_modified: bool


# ---------------------------------------------------------------------------
# Scenarios
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_4_intellect.feature",
    "Intellect is a numeric property of a hero card",
)
def test_intellect_is_numeric_property():
    """Rule 2.4.1/2.4.2: Intellect is a numeric property of a hero card."""
    pass


@scenario(
    "../features/section_2_4_intellect.feature",
    "Intellect represents cards drawn at end of turn",
)
def test_intellect_represents_cards_drawn_at_end_of_turn():
    """Rule 2.4.1: Intellect represents the number of cards drawn up to at end of turn."""
    pass


@scenario(
    "../features/section_2_4_intellect.feature",
    "Intellect is a property of hero cards only",
)
def test_intellect_is_hero_card_property_only():
    """Rule 2.4.1: Intellect is a property of hero cards, not other card types."""
    pass


@scenario(
    "../features/section_2_4_intellect.feature",
    "Printed intellect defines the base intellect of a hero card",
)
def test_printed_intellect_defines_base_intellect():
    """Rule 2.4.2: Printed intellect defines the base intellect."""
    pass


@scenario(
    "../features/section_2_4_intellect.feature",
    "Zero is a valid printed intellect",
)
def test_zero_is_valid_printed_intellect():
    """Rule 2.4.2: Zero is a valid printed intellect value."""
    pass


@scenario(
    "../features/section_2_4_intellect.feature",
    "Card without a printed intellect lacks the intellect property",
)
def test_card_without_printed_intellect_lacks_property():
    """Rule 2.4.2: No printed intellect means no intellect property."""
    pass


@scenario(
    "../features/section_2_4_intellect.feature",
    "Intellect of a hero can be modified by effects",
)
def test_intellect_can_be_modified():
    """Rule 2.4.3: Intellect can be modified by effects."""
    pass


@scenario(
    "../features/section_2_4_intellect.feature",
    "The term intellect refers to the modified intellect not base intellect",
)
def test_intellect_term_refers_to_modified_intellect():
    """Rule 2.4.3: The term 'intellect' refers to the modified intellect."""
    pass


@scenario(
    "../features/section_2_4_intellect.feature",
    "The symbol i refers to the modified intellect of a hero",
)
def test_i_symbol_refers_to_modified_intellect():
    """Rule 2.4.3: The {i} symbol refers to the modified intellect."""
    pass


@scenario(
    "../features/section_2_4_intellect.feature",
    "Intellect of a hero can be decreased by effects",
)
def test_intellect_can_be_decreased():
    """Rule 2.4.3: Intellect can be decreased by effects."""
    pass


@scenario(
    "../features/section_2_4_intellect.feature",
    "Intellect cannot be reduced below zero",
)
def test_intellect_cannot_be_negative():
    """Rule 2.0.3c cross-ref: Numeric properties (including intellect) cannot be negative."""
    pass


@scenario(
    "../features/section_2_4_intellect.feature",
    "Modified intellect affects how many cards are drawn at end of turn",
)
def test_modified_intellect_affects_end_of_turn_draw():
    """Rule 2.4.1 + 2.4.3: Modified intellect determines cards drawn at end of turn."""
    pass


@scenario(
    "../features/section_2_4_intellect.feature",
    "Multiple hero cards have independent intellect values",
)
def test_multiple_hero_cards_independent_intellect():
    """Rule 2.4.2: Each hero card has its own independent intellect value."""
    pass


# ---------------------------------------------------------------------------
# Step definitions
# ---------------------------------------------------------------------------


@given(parsers.parse("a hero card is created with a printed intellect of {value:d}"))
def hero_card_with_printed_intellect(value, game_state):
    """
    Rule 2.4.1/2.4.2: Create a hero card with the specified printed intellect.

    Engine Feature Needed: CardInstance with hero type and printed_intellect attribute.
    """
    game_state.intellect_hero = IntellectCardStub(
        name=f"Test Hero",
        printed_intellect=value,
        is_hero=True,
    )


@given("a non-hero action card is created with no intellect")
def non_hero_action_card_no_intellect(game_state):
    """
    Rule 2.4.1: Non-hero cards do not have the intellect property.

    Engine Feature Needed: CardType validation restricting intellect to hero cards.
    """
    game_state.non_hero_card = IntellectCardStub(
        name="Test Action Card",
        printed_intellect=None,  # No printed intellect
        is_hero=False,  # Not a hero card
    )


@given("a non-hero card is created with no printed intellect")
def non_hero_card_no_printed_intellect(game_state):
    """
    Rule 2.4.2: Card without printed intellect does not have the intellect property.

    Engine Feature Needed: CardInstance.has_intellect_property = False when no printed intellect.
    """
    game_state.no_intellect_card = IntellectCardStub(
        name="Test Non-Intellect Card",
        printed_intellect=None,
        is_hero=False,
    )


@given(
    parsers.parse(
        "an intellect boost effect of plus {amount:d} is applied to the intellect {value:d} hero"
    )
)
def apply_intellect_boost(amount, value, game_state):
    """
    Rule 2.4.3: Apply an intellect boost effect to the hero.

    Engine Feature Needed: Effect system applying intellect modifications.
    """
    game_state.intellect_hero.apply_intellect_boost(amount)


@given(
    parsers.parse(
        "an intellect reduction effect of minus {amount:d} is applied to the intellect {value:d} hero"
    )
)
def apply_intellect_reduction(amount, value, game_state):
    """
    Rule 2.4.3: Apply an intellect reduction effect to the hero.

    Engine Feature Needed: Effect system applying intellect reductions.
    """
    game_state.intellect_hero.apply_intellect_reduction(amount)


@given("another hero card is created with a printed intellect of 3")
def another_hero_card_with_intellect_3(game_state):
    """
    Rule 2.4.2: Create a second hero card with intellect 3.

    Engine Feature Needed: Multiple heroes with independent intellect values.
    """
    game_state.second_intellect_hero = IntellectCardStub(
        name="Second Test Hero",
        printed_intellect=3,
        is_hero=True,
    )


# ---------------------------------------------------------------------------
# When steps
# ---------------------------------------------------------------------------


@when(
    parsers.parse(
        "the engine checks the intellect property of the intellect {value:d} hero"
    )
)
def check_intellect_property_of_hero(value, game_state):
    """
    Rule 2.4.1/2.4.2: Check the intellect property of the hero.

    Engine Feature Needed: CardInstance.check_intellect() or similar method.
    """
    game_state.intellect_check_result = game_state.intellect_hero.check_intellect()


@when("the engine resolves end-of-turn draw for the intellect 3 hero")
def resolve_end_of_turn_draw_for_intellect_3(game_state):
    """
    Rule 2.4.1: Resolve the end-of-turn draw for a hero with intellect 3.

    Engine Feature Needed: End-of-turn draw-up-to logic using effective intellect.
    """
    intellect_value = game_state.intellect_hero.effective_intellect
    game_state.end_of_turn_draw_result = EndOfTurnDrawResultStub(
        cards_drawn_up_to=intellect_value,
        intellect_used=intellect_value,
    )


@when("the engine checks the intellect property of both cards")
def check_intellect_property_of_both_cards(game_state):
    """
    Rule 2.4.1: Check intellect property of both hero and non-hero cards.

    Engine Feature Needed: CardInstance.has_intellect_property distinction between card types.
    """
    game_state.hero_intellect_result = game_state.intellect_hero.check_intellect()
    game_state.non_hero_intellect_result = game_state.non_hero_card.check_intellect()


@when(
    parsers.parse(
        "the engine checks the base intellect of the intellect {value:d} hero"
    )
)
def check_base_intellect_of_hero(value, game_state):
    """
    Rule 2.4.2: Check the base (unmodified printed) intellect of the hero.

    Engine Feature Needed: CardInstance.base_intellect property.
    """
    game_state.base_intellect_result = game_state.intellect_hero.base_intellect


@when("the engine checks the intellect property of the intellect 0 hero")
def check_intellect_property_of_intellect_0_hero(game_state):
    """
    Rule 2.4.2: Check intellect property for a hero with 0 printed intellect.

    Engine Feature Needed: CardInstance.has_intellect_property = True even for 0 intellect.
    """
    game_state.intellect_check_result = game_state.intellect_hero.check_intellect()


@when("the engine checks the intellect property of the no-intellect card")
def check_intellect_property_of_no_intellect_card(game_state):
    """
    Rule 2.4.2: Check the intellect property of a card with no printed intellect.

    Engine Feature Needed: CardInstance.has_intellect_property = False when no printed intellect.
    """
    game_state.intellect_check_result = game_state.no_intellect_card.check_intellect()


@when(
    parsers.parse(
        "the engine checks the modified intellect of the intellect {value:d} hero"
    )
)
def check_modified_intellect_of_hero(value, game_state):
    """
    Rule 2.4.3: Check the modified (effective) intellect of the hero.

    Engine Feature Needed: CardInstance.effective_intellect returning modified value.
    """
    game_state.modified_intellect_result = game_state.intellect_hero.effective_intellect


@when(
    parsers.parse(
        "the engine resolves the term intellect for the intellect {value:d} hero"
    )
)
def resolve_term_intellect_for_hero(value, game_state):
    """
    Rule 2.4.3: Resolve the term "intellect" to get the modified intellect.

    Engine Feature Needed: The term "intellect" resolves to modified intellect.
    """
    game_state.resolved_intellect = game_state.intellect_hero.effective_intellect
    game_state.base_intellect_stored = game_state.intellect_hero.base_intellect


@when(
    parsers.parse("the engine resolves the i symbol for the intellect {value:d} hero")
)
def resolve_i_symbol_for_hero(value, game_state):
    """
    Rule 2.4.3: Resolve the {i} symbol to get the modified intellect.

    Engine Feature Needed: The {i} symbol resolves to modified intellect.
    """
    game_state.i_symbol_intellect = game_state.intellect_hero.effective_intellect


@when("the engine resolves end-of-turn draw for the boosted intellect 4 hero")
def resolve_end_of_turn_draw_for_boosted_hero(game_state):
    """
    Rule 2.4.1 + 2.4.3: Resolve end-of-turn draw using modified (boosted) intellect.

    Engine Feature Needed: End-of-turn draw uses modified intellect, not base intellect.
    """
    intellect_value = game_state.intellect_hero.effective_intellect
    game_state.end_of_turn_draw_result = EndOfTurnDrawResultStub(
        cards_drawn_up_to=intellect_value,
        intellect_used=intellect_value,
    )


@when("the engine checks both intellect hero cards")
def check_both_intellect_hero_cards(game_state):
    """
    Rule 2.4.2: Check intellect of two independent hero cards.

    Engine Feature Needed: Each hero card maintains its own intellect value.
    """
    game_state.first_hero_intellect = game_state.intellect_hero.effective_intellect
    game_state.second_hero_intellect = (
        game_state.second_intellect_hero.effective_intellect
    )


# ---------------------------------------------------------------------------
# Then steps
# ---------------------------------------------------------------------------


@then(parsers.parse("the intellect {value:d} hero should have the intellect property"))
def assert_hero_has_intellect_property(value, game_state):
    """
    Rule 2.4.2: Verify hero card has the intellect property.

    Engine Feature Needed: CardInstance.has_intellect_property = True when printed intellect exists.
    """
    assert game_state.intellect_check_result.has_intellect_property, (
        f"Expected hero with intellect {value} to have the intellect property, "
        f"but has_intellect_property was False. "
        f"Engine Feature Needed: CardInstance.has_intellect_property (Rule 2.4.2)"
    )


@then(
    parsers.parse(
        "the intellect of the intellect {value:d} hero should be {expected:d}"
    )
)
def assert_hero_intellect_value(value, expected, game_state):
    """
    Rule 2.4.1/2.4.2: Verify the intellect value of the hero card.

    Engine Feature Needed: CardInstance.effective_intellect returning correct value.
    """
    assert game_state.intellect_check_result.intellect_value == expected, (
        f"Expected hero intellect to be {expected}, "
        f"but got {game_state.intellect_check_result.intellect_value}. "
        f"Engine Feature Needed: CardInstance.effective_intellect (Rule 2.4.1)"
    )


@then(parsers.parse("the intellect of the intellect {value:d} hero should be numeric"))
def assert_hero_intellect_is_numeric(value, game_state):
    """
    Rule 2.4.1: Verify intellect is a numeric property.

    Engine Feature Needed: Intellect property is a numeric type.
    """
    assert game_state.intellect_check_result.is_numeric, (
        f"Expected intellect to be a numeric property, "
        f"but is_numeric was False. "
        f"Engine Feature Needed: Intellect as numeric property (Rule 2.4.1)"
    )


@then(parsers.parse("the player draws up to {expected:d} cards at end of turn"))
def assert_draws_up_to_n_cards(expected, game_state):
    """
    Rule 2.4.1: Verify player draws up to the intellect value at end of turn.

    Engine Feature Needed: End-of-turn draw-up-to logic using effective intellect.
    """
    assert game_state.end_of_turn_draw_result.cards_drawn_up_to == expected, (
        f"Expected player to draw up to {expected} cards at end of turn, "
        f"but got {game_state.end_of_turn_draw_result.cards_drawn_up_to}. "
        f"Engine Feature Needed: End-of-turn draw using intellect (Rule 2.4.1)"
    )


@then("the hero card should have the intellect property")
def assert_hero_card_has_intellect_property(game_state):
    """
    Rule 2.4.1: Verify hero card has intellect property.

    Engine Feature Needed: CardInstance.has_intellect_property = True for heroes.
    """
    assert game_state.hero_intellect_result.has_intellect_property, (
        "Expected hero card to have the intellect property. "
        "Engine Feature Needed: CardInstance.has_intellect_property (Rule 2.4.1)"
    )


@then("the non-hero action card should not have the intellect property")
def assert_non_hero_card_lacks_intellect_property(game_state):
    """
    Rule 2.4.1: Verify non-hero cards do not have the intellect property.

    Engine Feature Needed: CardInstance.has_intellect_property = False for non-hero cards.
    """
    assert not game_state.non_hero_intellect_result.has_intellect_property, (
        "Expected non-hero action card to NOT have the intellect property. "
        "Engine Feature Needed: Intellect restricted to hero cards (Rule 2.4.1)"
    )


@then(
    parsers.parse(
        "the base intellect of the intellect {value:d} hero should be {expected:d}"
    )
)
def assert_base_intellect_value(value, expected, game_state):
    """
    Rule 2.4.2: Verify the base (unmodified) intellect of the hero.

    Engine Feature Needed: CardInstance.base_intellect property returning printed intellect.
    """
    assert game_state.base_intellect_result == expected, (
        f"Expected base intellect to be {expected}, "
        f"but got {game_state.base_intellect_result}. "
        f"Engine Feature Needed: CardInstance.base_intellect (Rule 2.4.2)"
    )


@then("the intellect 0 hero should have the intellect property")
def assert_intellect_0_hero_has_property(game_state):
    """
    Rule 2.4.2: A hero with 0 printed intellect still has the intellect property.

    Engine Feature Needed: CardInstance.has_intellect_property = True for 0 intellect.
    """
    assert game_state.intellect_check_result.has_intellect_property, (
        "Expected hero with 0 printed intellect to have the intellect property. "
        "Engine Feature Needed: CardInstance.has_intellect_property (Rule 2.4.2)"
    )


@then("the intellect of the intellect 0 hero should be 0")
def assert_intellect_0_hero_value_is_0(game_state):
    """
    Rule 2.4.2: A hero with 0 printed intellect has intellect value of 0.

    Engine Feature Needed: CardInstance.effective_intellect returning 0 for 0-intellect hero.
    """
    assert game_state.intellect_check_result.intellect_value == 0, (
        f"Expected hero intellect to be 0, "
        f"but got {game_state.intellect_check_result.intellect_value}. "
        f"Engine Feature Needed: CardInstance.effective_intellect (Rule 2.4.2)"
    )


@then("the no-intellect card should not have the intellect property")
def assert_no_intellect_card_lacks_property(game_state):
    """
    Rule 2.4.2: Card without printed intellect does not have the intellect property.

    Engine Feature Needed: CardInstance.has_intellect_property = False when no printed intellect.
    """
    assert not game_state.intellect_check_result.has_intellect_property, (
        "Expected card without printed intellect to NOT have the intellect property. "
        "Engine Feature Needed: CardInstance.has_intellect_property (Rule 2.4.2)"
    )


@then(
    parsers.parse(
        "the modified intellect of the intellect {value:d} hero should be {expected:d}"
    )
)
def assert_modified_intellect_value(value, expected, game_state):
    """
    Rule 2.4.3: Verify the modified intellect of the hero.

    Engine Feature Needed: CardInstance.effective_intellect returning modified value.
    """
    assert game_state.modified_intellect_result == expected, (
        f"Expected modified intellect to be {expected}, "
        f"but got {game_state.modified_intellect_result}. "
        f"Engine Feature Needed: CardInstance.effective_intellect (Rule 2.4.3)"
    )


@then(
    parsers.parse(
        "the resolved intellect of the intellect {value:d} hero should be {expected:d}"
    )
)
def assert_resolved_intellect_is_modified(value, expected, game_state):
    """
    Rule 2.4.3: Verify the term "intellect" resolves to the modified intellect.

    Engine Feature Needed: Intellect references resolve to modified value, not base.
    """
    assert game_state.resolved_intellect == expected, (
        f"Expected resolved intellect to be {expected}, "
        f"but got {game_state.resolved_intellect}. "
        f"Engine Feature Needed: Intellect term resolves to modified value (Rule 2.4.3)"
    )


@then(
    parsers.parse(
        "the base intellect of the intellect {value:d} hero should remain {expected:d}"
    )
)
def assert_base_intellect_unchanged(value, expected, game_state):
    """
    Rule 2.4.3: Verify the base intellect is unchanged after modification.

    Engine Feature Needed: CardInstance.base_intellect unchanged by effects.
    """
    assert game_state.base_intellect_stored == expected, (
        f"Expected base intellect to remain {expected}, "
        f"but got {game_state.base_intellect_stored}. "
        f"Engine Feature Needed: CardInstance.base_intellect distinct from effective_intellect (Rule 2.4.3)"
    )


@then(
    parsers.parse(
        "the i symbol intellect of the intellect {value:d} hero should be {expected:d}"
    )
)
def assert_i_symbol_intellect_is_modified(value, expected, game_state):
    """
    Rule 2.4.3: Verify the {i} symbol resolves to the modified intellect.

    Engine Feature Needed: {i} symbol resolves to modified intellect value.
    """
    assert game_state.i_symbol_intellect == expected, (
        f"Expected {{i}} symbol intellect to be {expected}, "
        f"but got {game_state.i_symbol_intellect}. "
        f"Engine Feature Needed: {{i}} symbol resolves to modified intellect (Rule 2.4.3)"
    )


@then(parsers.parse("the first hero intellect should be {expected:d}"))
def assert_first_hero_intellect(expected, game_state):
    """
    Rule 2.4.2: Verify the first hero card has its own independent intellect.

    Engine Feature Needed: Each hero card maintains independent intellect.
    """
    assert game_state.first_hero_intellect == expected, (
        f"Expected first hero intellect to be {expected}, "
        f"but got {game_state.first_hero_intellect}. "
        f"Engine Feature Needed: Independent intellect per hero (Rule 2.4.2)"
    )


@then(parsers.parse("the second hero intellect should be {expected:d}"))
def assert_second_hero_intellect(expected, game_state):
    """
    Rule 2.4.2: Verify the second hero card has its own independent intellect.

    Engine Feature Needed: Each hero card maintains independent intellect.
    """
    assert game_state.second_hero_intellect == expected, (
        f"Expected second hero intellect to be {expected}, "
        f"but got {game_state.second_hero_intellect}. "
        f"Engine Feature Needed: Independent intellect per hero (Rule 2.4.2)"
    )


# ---------------------------------------------------------------------------
# Fixture
# ---------------------------------------------------------------------------


@pytest.fixture
def game_state():
    """
    Fixture providing game state for testing Section 2.4: Intellect.

    Uses a simple namespace object to store test state between steps.
    This allows stub-based testing while documenting what engine features are needed.

    Reference: Rule 2.4 - Intellect
    """

    class GameStateNamespace:
        """Namespace for storing test state between BDD steps."""

        pass

    return GameStateNamespace()
