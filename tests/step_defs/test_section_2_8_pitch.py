"""
Step definitions for Section 2.8: Pitch
Reference: Flesh and Blood Comprehensive Rules Section 2.8

This module implements behavioral tests for the pitch property of cards
in Flesh and Blood.

Rule 2.8.1: Pitch is a property of a card, which represents the assets a
            player gains when they pitch the card. The pitch value of the
            card is the number of assets gained when pitched and it
            determines the object's uniqueness (along with the name
            property).

Rule 2.8.2: The printed pitch of a card is expressed visually as one, two,
            or three socketed {r} or {c} symbols, typically located in the
            top left corner of a card, where the types of symbols dictate
            what asset is generated when pitched and the number of symbols
            dictates the printed pitch value. The printed pitch value
            defines the base pitch value of a card. If a card does not have
            a printed pitch value, it does not have the pitch property.

Rule 2.8.3: The pitch of an object can be modified. The term "pitch" refers
            to the modified pitch value of an object.

Rule 2.8.4: The visual expression of {r} or {c} symbols and the numerical
            expression of pitch are functionally identical.
            Example: The text "Search your deck for a card with pitch value 1,"
            is considered to be the same as the text "Search your deck for a
            card with pitch value {r}."

Engine Features Needed for Section 2.8:
- [ ] `CardInstance.has_pitch_property` property: False when no printed pitch (Rule 2.8.2)
- [ ] `CardInstance.base_pitch` property returning the unmodified printed pitch (Rule 2.8.2)
- [ ] `CardInstance.pitch` or `CardInstance.effective_pitch` returning modified pitch (Rule 2.8.3)
- [ ] `CardInstance.pitch_asset_type` returning "resource" or "chi" based on symbol type (Rule 2.8.2)
- [ ] `CardInstance.pitch_assets_generated` method returning assets gained when pitched (Rule 2.8.1)
- [ ] Pitch modification effects that increase/decrease effective pitch (Rule 2.8.3)
- [ ] Numeric pitch capped at zero (cross-ref Rule 2.0.3c)
- [ ] `CardTemplate.is_distinct_from(other)` based on name + pitch (Rules 2.8.1, 1.3.4)
- [ ] Symbol count ({r} or {c}) and numeric pitch treated as functionally identical (Rule 2.8.4)
"""

import pytest
from pytest_bdd import scenario, given, when, then, parsers
from dataclasses import dataclass, field
from typing import Optional, List


# ---------------------------------------------------------------------------
# Stub classes for testing Section 2.8 rules
# ---------------------------------------------------------------------------


@dataclass
class PitchCheckResultStub:
    """
    Result of checking a card's pitch property.

    Rule 2.8.1: Pitch is a property representing assets gained when pitched.
    Rule 2.8.2: Printed pitch defines base pitch; no printed pitch = no property.
    """

    has_pitch_property: bool
    pitch_value: Optional[int]  # None if no pitch property
    is_numeric: bool = True


@dataclass
class PitchCardStub:
    """
    Stub representing a card with a pitch property.

    Models what the engine must implement for Section 2.8.
    Engine Features Needed:
    - [ ] CardInstance.base_pitch: unmodified printed pitch (Rule 2.8.2)
    - [ ] CardInstance.has_pitch_property: False if no printed pitch (Rule 2.8.2)
    - [ ] CardInstance.effective_pitch: modified pitch (Rule 2.8.3)
    - [ ] CardInstance.pitch_asset_type: "resource" or "chi" (Rule 2.8.2)
    """

    name: str = "Test Card"
    printed_pitch: Optional[int] = None  # None if card has no pitch property
    pitch_asset_type: str = "resource"  # "resource" or "chi" (Rule 2.8.2)
    pitch_modifier: int = 0  # Applied by effects (Rule 2.8.3)

    @property
    def has_pitch_property(self) -> bool:
        """Rule 2.8.2: Card has pitch property only if there is a printed pitch."""
        return self.printed_pitch is not None

    @property
    def base_pitch(self) -> Optional[int]:
        """Rule 2.8.2: Base pitch is the printed pitch."""
        return self.printed_pitch

    @property
    def effective_pitch(self) -> Optional[int]:
        """
        Rule 2.8.3: The modified pitch of the object.

        The term "pitch" refers to this value.
        Capped at zero (cross-ref Rule 2.0.3c).
        """
        if self.printed_pitch is None:
            return None
        return max(0, self.printed_pitch + self.pitch_modifier)

    def pitch_to_gain_assets(self) -> int:
        """
        Rule 2.8.1: The number of assets gained when this card is pitched.

        Engine Feature Needed: Pitching generates assets based on the pitch value.
        """
        if self.effective_pitch is None:
            return 0
        return self.effective_pitch

    def check_pitch(self) -> PitchCheckResultStub:
        """Rule 2.8.1/2.8.2: Get the pitch property of this card."""
        return PitchCheckResultStub(
            has_pitch_property=self.has_pitch_property,
            pitch_value=self.effective_pitch,
            is_numeric=True,
        )

    def apply_pitch_boost(self, amount: int):
        """
        Rule 2.8.3: Apply a positive pitch modification from an effect.

        Engine Feature Needed: Effect system applying pitch modifications.
        """
        self.pitch_modifier += amount

    def apply_pitch_reduction(self, amount: int):
        """
        Rule 2.8.3: Apply a negative pitch modification from an effect.

        Engine Feature Needed: Effect system applying pitch reductions.
        """
        self.pitch_modifier -= amount

    def is_distinct_from(self, other: "PitchCardStub") -> bool:
        """
        Rule 2.8.1 / cross-ref Rule 1.3.4: Cards are distinct if name or pitch differ.

        Engine Feature Needed: CardTemplate.is_distinct_from(other) based on name + pitch.
        """
        return self.name != other.name or self.base_pitch != other.base_pitch


@dataclass
class PitchSearchResultStub:
    """
    Result of searching for cards by pitch value.

    Rule 2.8.4: Numeric pitch and symbol pitch are functionally identical for search.
    """

    found_cards: List[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Scenarios
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_8_pitch.feature",
    "Pitch is a property of a card",
)
def test_pitch_is_property_of_card():
    """Rule 2.8.1: Pitch is a property of a card."""
    pass


@scenario(
    "../features/section_2_8_pitch.feature",
    "Pitch value represents assets gained when pitching",
)
def test_pitch_value_represents_assets_gained():
    """Rule 2.8.1: Pitch value represents the number of assets gained when pitched."""
    pass


@scenario(
    "../features/section_2_8_pitch.feature",
    "Pitch value contributes to card uniqueness with name",
)
def test_pitch_contributes_to_card_uniqueness():
    """Rule 2.8.1: Pitch determines uniqueness along with name."""
    pass


@scenario(
    "../features/section_2_8_pitch.feature",
    "Cards with same name and same pitch value are not distinct",
)
def test_same_name_same_pitch_not_distinct():
    """Rule 2.8.1: Cards with same name and pitch are not distinct."""
    pass


@scenario(
    "../features/section_2_8_pitch.feature",
    "Card with one resource symbol has pitch value 1",
)
def test_one_resource_symbol_is_pitch_1():
    """Rule 2.8.2: One resource symbol = pitch value 1."""
    pass


@scenario(
    "../features/section_2_8_pitch.feature",
    "Card with two resource symbols has pitch value 2",
)
def test_two_resource_symbols_is_pitch_2():
    """Rule 2.8.2: Two resource symbols = pitch value 2."""
    pass


@scenario(
    "../features/section_2_8_pitch.feature",
    "Card with three resource symbols has pitch value 3",
)
def test_three_resource_symbols_is_pitch_3():
    """Rule 2.8.2: Three resource symbols = pitch value 3."""
    pass


@scenario(
    "../features/section_2_8_pitch.feature",
    "Resource symbols generate resource points when pitched",
)
def test_resource_symbols_generate_resource_points():
    """Rule 2.8.2: {r} symbols generate resource assets when pitched."""
    pass


@scenario(
    "../features/section_2_8_pitch.feature",
    "Chi symbols generate chi points when pitched",
)
def test_chi_symbols_generate_chi_points():
    """Rule 2.8.2: {c} symbols generate chi assets when pitched."""
    pass


@scenario(
    "../features/section_2_8_pitch.feature",
    "Printed pitch defines the base pitch value of a card",
)
def test_printed_pitch_defines_base_pitch():
    """Rule 2.8.2: Printed pitch defines the base pitch value."""
    pass


@scenario(
    "../features/section_2_8_pitch.feature",
    "Card without a printed pitch lacks the pitch property",
)
def test_card_without_printed_pitch_lacks_property():
    """Rule 2.8.2: No printed pitch means no pitch property."""
    pass


@scenario(
    "../features/section_2_8_pitch.feature",
    "Pitch of an object can be modified by effects",
)
def test_pitch_can_be_modified():
    """Rule 2.8.3: Pitch can be modified by effects."""
    pass


@scenario(
    "../features/section_2_8_pitch.feature",
    "The term pitch refers to the modified pitch value not base pitch",
)
def test_pitch_term_refers_to_modified_pitch():
    """Rule 2.8.3: The term 'pitch' refers to the modified pitch."""
    pass


@scenario(
    "../features/section_2_8_pitch.feature",
    "Pitch of an object can be decreased by effects",
)
def test_pitch_can_be_decreased():
    """Rule 2.8.3: Pitch can be decreased by effects."""
    pass


@scenario(
    "../features/section_2_8_pitch.feature",
    "Pitch cannot be reduced below zero",
)
def test_pitch_cannot_be_negative():
    """Rule 2.0.3c cross-ref: Pitch is capped at zero."""
    pass


@scenario(
    "../features/section_2_8_pitch.feature",
    "One resource symbol is functionally identical to numeric pitch 1",
)
def test_resource_symbol_identical_to_numeric_pitch_1():
    """Rule 2.8.4: {r} and numeric are equivalent."""
    pass


@scenario(
    "../features/section_2_8_pitch.feature",
    "Searching by numeric pitch value finds cards with matching resource symbols",
)
def test_search_by_numeric_pitch_finds_symbol_cards():
    """Rule 2.8.4: Search by pitch value finds both numeric and symbol cards."""
    pass


@scenario(
    "../features/section_2_8_pitch.feature",
    "Multiple cards each have independent pitch values",
)
def test_multiple_cards_independent_pitch():
    """Rule 2.8.2: Each card has its own pitch property."""
    pass


# ---------------------------------------------------------------------------
# Step definitions
# ---------------------------------------------------------------------------


@given(parsers.parse("a pitch card is created with a printed pitch of {value:d}"))
def create_pitch_card(game_state, value):
    """Rule 2.8.2: Create a card with the specified printed pitch."""
    game_state.pitch_card = PitchCardStub(
        name=f"Test Pitch Card ({value})",
        printed_pitch=value,
    )


@given("a pitch card is created with no printed pitch")
def create_no_pitch_card(game_state):
    """Rule 2.8.2: Create a card with no printed pitch (no pitch property)."""
    game_state.pitch_card = PitchCardStub(
        name="No Pitch Card",
        printed_pitch=None,
    )


@given(
    parsers.parse('a pitch card named "{name}" with pitch value {value:d} is created')
)
def create_named_pitch_card(game_state, name, value):
    """Rule 2.8.1: Create a named card with specific pitch value."""
    game_state.pitch_card = PitchCardStub(
        name=name,
        printed_pitch=value,
    )


@given(
    parsers.parse(
        'another pitch card named "{name}" with pitch value {value:d} is created'
    )
)
def create_second_named_pitch_card(game_state, name, value):
    """Rule 2.8.1: Create a second named card with specific pitch value."""
    game_state.second_pitch_card = PitchCardStub(
        name=name,
        printed_pitch=value,
    )


@given(
    parsers.parse(
        'another pitch card named "{name}" with pitch value {value:d} is also created'
    )
)
def create_second_named_pitch_card_also(game_state, name, value):
    """Rule 2.8.1: Create a second card with the same name and pitch value."""
    game_state.second_pitch_card = PitchCardStub(
        name=name,
        printed_pitch=value,
    )


@given(
    parsers.parse(
        "a pitch card is created with {count:d} resource symbol in the pitch area"
    )
)
def create_card_with_resource_symbols_single(game_state, count):
    """Rule 2.8.2: Create a card with a specified number of resource symbols."""
    game_state.pitch_card = PitchCardStub(
        name=f"Resource Symbol Card ({count})",
        printed_pitch=count,
        pitch_asset_type="resource",
    )


@given(
    parsers.parse(
        "a pitch card is created with {count:d} resource symbols in the pitch area"
    )
)
def create_card_with_resource_symbols_plural(game_state, count):
    """Rule 2.8.2: Create a card with a specified number of resource symbols."""
    game_state.pitch_card = PitchCardStub(
        name=f"Resource Symbol Card ({count})",
        printed_pitch=count,
        pitch_asset_type="resource",
    )


@given(
    parsers.parse(
        "a pitch card is created with {count:d} resource symbols for resource asset type"
    )
)
def create_card_with_resource_symbols_resource_type(game_state, count):
    """Rule 2.8.2: Create a resource-type pitch card."""
    game_state.pitch_card = PitchCardStub(
        name=f"Resource Pitch Card ({count})",
        printed_pitch=count,
        pitch_asset_type="resource",
    )


@given(
    parsers.parse(
        "a pitch card is created with {count:d} chi symbol for chi asset type"
    )
)
def create_card_with_chi_symbol_singular(game_state, count):
    """Rule 2.8.2: Create a chi-type pitch card."""
    game_state.pitch_card = PitchCardStub(
        name=f"Chi Pitch Card ({count})",
        printed_pitch=count,
        pitch_asset_type="chi",
    )


@given(
    parsers.parse(
        "a pitch card is created with {count:d} chi symbols for chi asset type"
    )
)
def create_card_with_chi_symbols_plural(game_state, count):
    """Rule 2.8.2: Create a chi-type pitch card."""
    game_state.pitch_card = PitchCardStub(
        name=f"Chi Pitch Card ({count})",
        printed_pitch=count,
        pitch_asset_type="chi",
    )


@given(
    parsers.parse(
        "a pitch boost effect of plus {amount:d} is applied to the pitch {base:d} card"
    )
)
def apply_pitch_boost(game_state, amount, base):
    """Rule 2.8.3: Apply a positive pitch modification to the card."""
    game_state.pitch_card.apply_pitch_boost(amount)


@given(
    parsers.parse(
        "a pitch reduction effect of minus {amount:d} is applied to the pitch {base:d} card"
    )
)
def apply_pitch_reduction(game_state, amount, base):
    """Rule 2.8.3: Apply a negative pitch modification to the card."""
    game_state.pitch_card.apply_pitch_reduction(amount)


@given(parsers.parse("another pitch card is created with a printed pitch of {value:d}"))
def create_second_pitch_card(game_state, value):
    """Rule 2.8.2: Create a second card with the specified printed pitch."""
    game_state.second_pitch_card = PitchCardStub(
        name=f"Second Test Pitch Card ({value})",
        printed_pitch=value,
    )


@given("a pitch card is created with a cost expressed as one resource symbol pitch")
def create_card_with_one_symbol_pitch(game_state):
    """Rule 2.8.4: Create a card with one resource symbol as pitch notation."""
    game_state.pitch_card = PitchCardStub(
        name="Symbol Pitch Card",
        printed_pitch=1,
        pitch_asset_type="resource",
    )
    game_state.pitch_notation_type = "symbol"


@given(
    parsers.parse(
        'a pitch card named "{name}" is created with a numeric pitch of {value:d}'
    )
)
def create_named_card_with_numeric_pitch(game_state, name, value):
    """Rule 2.8.4: Create a named card with numeric pitch notation."""
    if not hasattr(game_state, "search_cards"):
        game_state.search_cards = []
    card = PitchCardStub(name=name, printed_pitch=value, pitch_asset_type="resource")
    game_state.search_cards.append(card)


@given(
    parsers.parse(
        'a pitch card named "{name}" is created with one resource symbol pitch'
    )
)
def create_named_card_with_symbol_pitch(game_state, name):
    """Rule 2.8.4: Create a named card with one resource symbol pitch notation."""
    if not hasattr(game_state, "search_cards"):
        game_state.search_cards = []
    card = PitchCardStub(name=name, printed_pitch=1, pitch_asset_type="resource")
    game_state.search_cards.append(card)


# When steps


@when(parsers.parse("the engine checks the pitch property of the pitch {value:d} card"))
def check_pitch_property_by_value(game_state, value):
    """Rule 2.8.1/2.8.2: Check the pitch property of the card."""
    game_state.pitch_check_result = game_state.pitch_card.check_pitch()


@when("the engine checks the pitch property of the no-pitch card")
def check_no_pitch_property(game_state):
    """Rule 2.8.2: Check the pitch property of a card with no printed pitch."""
    game_state.pitch_check_result = game_state.pitch_card.check_pitch()


@when(parsers.parse("the engine pitches the pitch {value:d} card to gain assets"))
def pitch_card_to_gain_assets(game_state, value):
    """Rule 2.8.1: Pitch the card to gain assets."""
    game_state.assets_gained = game_state.pitch_card.pitch_to_gain_assets()


@when("the engine checks if the two Sink Below cards are distinct")
def check_sink_below_distinctness(game_state):
    """Rule 2.8.1: Check uniqueness of the two Sink Below cards."""
    game_state.cards_are_distinct = game_state.pitch_card.is_distinct_from(
        game_state.second_pitch_card
    )


@when("the engine checks if the two Pummel cards are distinct")
def check_pummel_distinctness(game_state):
    """Rule 2.8.1: Check uniqueness of the two Pummel cards."""
    game_state.cards_are_distinct = game_state.pitch_card.is_distinct_from(
        game_state.second_pitch_card
    )


@when(
    parsers.parse(
        "the engine checks the printed pitch of the {count:d}-resource-symbol card"
    )
)
def check_printed_pitch_by_symbol_count(game_state, count):
    """Rule 2.8.2: Check the printed pitch of a card based on symbol count."""
    game_state.printed_pitch_result = game_state.pitch_card.base_pitch


@when(
    parsers.parse(
        "the engine determines the asset type generated by the resource-symbol pitch card"
    )
)
def check_resource_symbol_asset_type(game_state):
    """Rule 2.8.2: Determine the asset type generated when the card is pitched."""
    game_state.asset_type_result = game_state.pitch_card.pitch_asset_type


@when(
    parsers.parse(
        "the engine determines the asset type generated by the chi-symbol pitch card"
    )
)
def check_chi_symbol_asset_type(game_state):
    """Rule 2.8.2: Determine the asset type generated when the chi card is pitched."""
    game_state.asset_type_result = game_state.pitch_card.pitch_asset_type


@when(
    parsers.parse("the engine checks the base pitch of the base-pitch-{value:d} card")
)
def check_base_pitch(game_state, value):
    """Rule 2.8.2: Check the base (unmodified) pitch of the card."""
    game_state.base_pitch_result = game_state.pitch_card.base_pitch


@when(parsers.parse("the engine checks the modified pitch of the pitch {value:d} card"))
def check_modified_pitch(game_state, value):
    """Rule 2.8.3: Check the modified (effective) pitch of the card."""
    game_state.modified_pitch_result = game_state.pitch_card.effective_pitch


@when(parsers.parse("the engine resolves the term pitch for the pitch {value:d} card"))
def resolve_pitch_term(game_state, value):
    """Rule 2.8.3: Resolve the term 'pitch' for a card (gives modified pitch)."""
    game_state.resolved_pitch = game_state.pitch_card.effective_pitch
    game_state.base_pitch_stored = game_state.pitch_card.base_pitch


@when("the engine interprets the resource symbol pitch as numeric")
def interpret_symbol_pitch_as_numeric(game_state):
    """Rule 2.8.4: Interpret the resource symbol pitch as a numeric value."""
    game_state.numeric_pitch_equivalent = game_state.pitch_card.effective_pitch


@when(parsers.parse("the engine searches for cards with pitch value {value:d}"))
def search_cards_by_pitch_value(game_state, value):
    """Rule 2.8.4: Search for cards with a specific pitch value."""
    if not hasattr(game_state, "search_cards"):
        game_state.search_cards = []
    game_state.pitch_search_result = PitchSearchResultStub(
        found_cards=[
            card.name for card in game_state.search_cards if card.base_pitch == value
        ]
    )


@when("the engine checks both pitch cards")
def check_both_pitch_cards(game_state):
    """Rule 2.8.2: Check the pitch of both cards to verify independence."""
    game_state.first_pitch_card_pitch = game_state.pitch_card.effective_pitch
    game_state.second_pitch_card_pitch = game_state.second_pitch_card.effective_pitch


# Then steps


@then(parsers.parse("the pitch {value:d} card should have the pitch property"))
def assert_has_pitch_property(game_state, value):
    """Rule 2.8.2: Verify that the card has the pitch property."""
    assert game_state.pitch_check_result.has_pitch_property, (
        f"Card with printed pitch {value} should have pitch property"
    )


@then("the no-pitch card should not have the pitch property")
def assert_no_pitch_property(game_state):
    """Rule 2.8.2: Verify that a card without printed pitch lacks the property."""
    assert not game_state.pitch_check_result.has_pitch_property, (
        "Card without printed pitch should not have the pitch property"
    )


@then(parsers.parse("the pitch of the pitch {value:d} card should be {expected:d}"))
def assert_pitch_value(game_state, value, expected):
    """Rule 2.8.1/2.8.2: Verify the pitch value."""
    assert game_state.pitch_check_result.pitch_value == expected, (
        f"Expected pitch {expected}, got {game_state.pitch_check_result.pitch_value}"
    )


@then(
    parsers.parse(
        "the assets gained from pitching the pitch {value:d} card should be {expected:d}"
    )
)
def assert_assets_gained(game_state, value, expected):
    """Rule 2.8.1: Verify the number of assets gained when the card is pitched."""
    assert game_state.assets_gained == expected, (
        f"Expected {expected} assets gained, got {game_state.assets_gained}"
    )


@then("the two Sink Below cards should be distinct due to different pitch values")
def assert_sink_below_cards_distinct(game_state):
    """Rule 2.8.1: Verify that cards with different pitch values are distinct."""
    assert game_state.cards_are_distinct, (
        "Sink Below red (pitch 1) and Sink Below blue (pitch 3) should be distinct"
    )


@then("the two Pummel cards should not be distinct")
def assert_pummel_cards_not_distinct(game_state):
    """Rule 2.8.1: Verify that cards with same name and pitch are not distinct."""
    assert not game_state.cards_are_distinct, (
        "Two Pummel cards with the same pitch value should NOT be distinct"
    )


@then(
    parsers.parse(
        "the printed pitch of the {count:d}-resource-symbol card should be {expected:d}"
    )
)
def assert_printed_pitch_by_symbol_count(game_state, count, expected):
    """Rule 2.8.2: Verify the printed pitch value based on symbol count."""
    assert game_state.printed_pitch_result == expected, (
        f"Card with {count} resource symbols should have printed pitch {expected}, "
        f"got {game_state.printed_pitch_result}"
    )


@then("the resource-symbol pitch card should generate resource points when pitched")
def assert_resource_symbol_generates_resources(game_state):
    """Rule 2.8.2: Verify that resource symbols generate resource points."""
    assert game_state.asset_type_result == "resource", (
        f"Resource symbol card should generate 'resource' points, "
        f"got '{game_state.asset_type_result}'"
    )


@then("the chi-symbol pitch card should generate chi points when pitched")
def assert_chi_symbol_generates_chi(game_state):
    """Rule 2.8.2: Verify that chi symbols generate chi points."""
    assert game_state.asset_type_result == "chi", (
        f"Chi symbol card should generate 'chi' points, "
        f"got '{game_state.asset_type_result}'"
    )


@then(
    parsers.parse(
        "the base pitch of the base-pitch-{value:d} card should be {expected:d}"
    )
)
def assert_base_pitch(game_state, value, expected):
    """Rule 2.8.2: Verify the base (unmodified) pitch."""
    assert game_state.base_pitch_result == expected, (
        f"Expected base pitch {expected}, got {game_state.base_pitch_result}"
    )


@then(
    parsers.parse(
        "the modified pitch of the pitch {value:d} card should be {expected:d}"
    )
)
def assert_modified_pitch(game_state, value, expected):
    """Rule 2.8.3: Verify the modified (effective) pitch."""
    assert game_state.modified_pitch_result == expected, (
        f"Expected modified pitch {expected}, got {game_state.modified_pitch_result}"
    )


@then(
    parsers.parse(
        "the resolved pitch of the pitch {value:d} card should be {expected:d}"
    )
)
def assert_resolved_pitch_term(game_state, value, expected):
    """Rule 2.8.3: Verify the resolved 'pitch' term equals the modified pitch."""
    assert game_state.resolved_pitch == expected, (
        f"Expected resolved pitch {expected}, got {game_state.resolved_pitch}"
    )


@then(
    parsers.parse(
        "the base pitch of the pitch {value:d} card should remain {expected:d}"
    )
)
def assert_base_pitch_unchanged(game_state, value, expected):
    """Rule 2.8.3: Verify base pitch is unchanged after modification."""
    assert game_state.base_pitch_stored == expected, (
        f"Expected base pitch to remain {expected}, got {game_state.base_pitch_stored}"
    )


@then("the numeric pitch equivalent should be 1")
def assert_numeric_pitch_equivalent_1(game_state):
    """Rule 2.8.4: Verify one resource symbol equals numeric pitch 1."""
    assert game_state.numeric_pitch_equivalent == 1, (
        f"Expected numeric pitch equivalent 1, got {game_state.numeric_pitch_equivalent}"
    )


@then(parsers.parse('both "{name1}" and "{name2}" should be found'))
def assert_both_cards_found(game_state, name1, name2):
    """Rule 2.8.4: Verify search finds both numeric and symbol pitch cards."""
    found = game_state.pitch_search_result.found_cards
    assert name1 in found, f"Expected to find '{name1}' in search results, got {found}"
    assert name2 in found, f"Expected to find '{name2}' in search results, got {found}"


@then(parsers.parse("the first pitch card pitch should be {expected:d}"))
def assert_first_pitch_card_pitch(game_state, expected):
    """Rule 2.8.2: Verify the first card's pitch."""
    assert game_state.first_pitch_card_pitch == expected, (
        f"Expected first card pitch {expected}, got {game_state.first_pitch_card_pitch}"
    )


@then(parsers.parse("the second pitch card pitch should be {expected:d}"))
def assert_second_pitch_card_pitch(game_state, expected):
    """Rule 2.8.2: Verify the second card's pitch."""
    assert game_state.second_pitch_card_pitch == expected, (
        f"Expected second card pitch {expected}, got {game_state.second_pitch_card_pitch}"
    )


# ---------------------------------------------------------------------------
# Fixture
# ---------------------------------------------------------------------------


@pytest.fixture
def game_state():
    """
    Fixture providing game state for testing.

    Uses BDDGameState which integrates with the real engine.
    Reference: Rule 2.8 - Pitch property of cards.
    """
    from tests.bdd_helpers import BDDGameState

    state = BDDGameState()

    # Placeholders for test objects
    state.pitch_card = None
    state.second_pitch_card = None
    state.pitch_check_result = None
    state.assets_gained = None
    state.cards_are_distinct = None
    state.printed_pitch_result = None
    state.asset_type_result = None
    state.base_pitch_result = None
    state.modified_pitch_result = None
    state.resolved_pitch = None
    state.base_pitch_stored = None
    state.numeric_pitch_equivalent = None
    state.pitch_search_result = None
    state.search_cards = []
    state.first_pitch_card_pitch = None
    state.second_pitch_card_pitch = None
    state.pitch_notation_type = None

    return state
