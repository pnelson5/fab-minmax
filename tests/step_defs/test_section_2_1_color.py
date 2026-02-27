"""
Step definitions for Section 2.1: Color
Reference: Flesh and Blood Comprehensive Rules Section 2.1

This module implements behavioral tests for the color property of cards in
Flesh and Blood.

Rule 2.1.1: Color is a visual representation of the color of a card.
Rule 2.1.2: The printed color of a card is typically expressed at the top of a
            card as a color strip.
            A card with a red color strip is considered red.
            A card with a yellow color strip is considered yellow.
            A card with a blue color strip is considered blue.
            A card with no color strip has no color.
Rule 2.1.2a: The printed pitch of a card is typically associated with the printed
             color of a card, but they are independent. Cards with a printed pitch
             of 1, 2, and 3, typically have a color strip of red, yellow, and blue
             respectively. A card with no printed pitch typically does not have a
             color strip.

Engine Features Needed for Section 2.1:
- [ ] `CardInstance.color` property returning Color enum (Rule 2.1.1/2.1.2)
- [ ] `CardInstance.has_color` property (Rule 2.1.2 - no color strip = no color)
- [ ] `CardInstance.color_name` property returning "red"/"yellow"/"blue"/None (Rule 2.1.2)
- [ ] `CardInstance.has_pitch` property (Rule 2.1.2a - no pitch = typically no color)
- [ ] Color.COLORLESS treated as "no color" not a color (Rule 2.1.2)
- [ ] Color and pitch treated as independent properties (Rule 2.1.2a)
"""

import pytest
from pytest_bdd import scenario, given, when, then, parsers
from dataclasses import dataclass, field
from typing import Optional


# ---------------------------------------------------------------------------
# Stub classes for testing Section 2.1 rules
# ---------------------------------------------------------------------------


@dataclass
class ColorCheckResultStub:
    """
    Result of checking a card's color property.

    Rule 2.1.1/2.1.2: Color is a visual representation expressed as a color strip.
    """

    color_name: Optional[str]  # "red", "yellow", "blue", or None
    has_color: bool
    is_visual_property: bool = True


@dataclass
class ColorAndPitchCheckResultStub:
    """
    Result of checking both color and pitch of a card.

    Rule 2.1.2a: Color and pitch are independent properties.
    """

    color_name: Optional[str]  # "red", "yellow", "blue", or None
    pitch_value: Optional[int]  # 1, 2, 3, or None
    has_color: bool
    has_pitch: bool
    are_independent: bool = True  # Rule 2.1.2a: always independent


@dataclass
class ColorCardStub:
    """
    Stub for a card with color and pitch properties.

    This models what the engine must implement for Section 2.1.
    Engine Feature Needed:
    - [ ] CardInstance.color property (Rule 2.1.2)
    - [ ] CardInstance.has_color property (Rule 2.1.2)
    - [ ] CardInstance.pitch property (Rule 2.1.2a)
    - [ ] CardInstance.has_pitch property (Rule 2.1.2a)
    """

    name: str = "Test Card"
    color_name: Optional[str] = None  # "red", "yellow", "blue", or None
    pitch_value: Optional[int] = None  # 1, 2, 3, or None

    @property
    def has_color(self) -> bool:
        """Rule 2.1.2: No color strip = no color."""
        return self.color_name is not None

    @property
    def has_pitch(self) -> bool:
        """Rule 2.1.2a: No pitch property = has_pitch is False."""
        return self.pitch_value is not None

    def check_color(self) -> ColorCheckResultStub:
        """Rule 2.1.1/2.1.2: Get the color of this card."""
        return ColorCheckResultStub(
            color_name=self.color_name,
            has_color=self.has_color,
            is_visual_property=True,
        )

    def check_color_and_pitch(self) -> ColorAndPitchCheckResultStub:
        """Rule 2.1.2a: Get both color and pitch, showing independence."""
        return ColorAndPitchCheckResultStub(
            color_name=self.color_name,
            pitch_value=self.pitch_value,
            has_color=self.has_color,
            has_pitch=self.has_pitch,
            are_independent=True,
        )


# ---------------------------------------------------------------------------
# Scenario: Color is a visual property of a card
# Tests Rule 2.1.1 - Color is a visual representation
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_1_color.feature",
    "Color is a visual property of a card",
)
def test_color_is_visual_property():
    """Rule 2.1.1: Color is a visual representation of the color of a card."""
    pass


@given(
    "a card is created with a red color strip for visual property testing",
    target_fixture="visual_property_card",
)
def step_given_card_for_visual_property_test():
    """Rule 2.1.1: Card with a red color strip for testing visual property."""
    return ColorCardStub(name="Red Action Card", color_name="red", pitch_value=1)


@when(
    "the engine checks the visual color property of the card",
    target_fixture="visual_property_result",
)
def step_when_check_visual_color_property(visual_property_card):
    """Rule 2.1.1: Check the visual color property of the card."""
    return visual_property_card.check_color()


@then("the card should have the color property")
def step_then_card_has_color_property(visual_property_result):
    """Rule 2.1.1: Card has a color property."""
    assert visual_property_result.has_color, (
        "Card with a color strip should have the color property"
    )


@then("the color should represent the visual appearance of the card")
def step_then_color_is_visual(visual_property_result):
    """Rule 2.1.1: Color is a visual representation."""
    assert visual_property_result.is_visual_property, (
        "Color should be recognized as a visual property"
    )


# ---------------------------------------------------------------------------
# Scenario: Card with red color strip is considered red
# Tests Rule 2.1.2 - Red color strip
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_1_color.feature",
    "Card with red color strip is considered red",
)
def test_card_with_red_color_strip_is_red():
    """Rule 2.1.2: A card with a red color strip is considered red."""
    pass


@given(
    "a card is created with a red color strip",
    target_fixture="red_card",
)
def step_given_red_card():
    """Rule 2.1.2: Create a card with red color strip."""
    return ColorCardStub(name="Red Card", color_name="red", pitch_value=1)


@when(
    "the engine checks the color of the red card",
    target_fixture="red_card_color_result",
)
def step_when_check_red_card_color(red_card):
    """Rule 2.1.2: Check the red card's color."""
    return red_card.check_color()


@then(parsers.parse('the color of the red card should be "{expected_color}"'))
def step_then_red_card_color_is(red_card_color_result, expected_color):
    """Rule 2.1.2: Verify the red card's color."""
    assert red_card_color_result.color_name == expected_color, (
        f"Expected color '{expected_color}', got '{red_card_color_result.color_name}'"
    )


# ---------------------------------------------------------------------------
# Scenario: Card with yellow color strip is considered yellow
# Tests Rule 2.1.2 - Yellow color strip
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_1_color.feature",
    "Card with yellow color strip is considered yellow",
)
def test_card_with_yellow_color_strip_is_yellow():
    """Rule 2.1.2: A card with a yellow color strip is considered yellow."""
    pass


@given(
    "a card is created with a yellow color strip",
    target_fixture="yellow_card",
)
def step_given_yellow_card():
    """Rule 2.1.2: Create a card with yellow color strip."""
    return ColorCardStub(name="Yellow Card", color_name="yellow", pitch_value=2)


@when(
    "the engine checks the color of the yellow card",
    target_fixture="yellow_card_color_result",
)
def step_when_check_yellow_card_color(yellow_card):
    """Rule 2.1.2: Check the yellow card's color."""
    return yellow_card.check_color()


@then(parsers.parse('the color of the yellow card should be "{expected_color}"'))
def step_then_yellow_card_color_is(yellow_card_color_result, expected_color):
    """Rule 2.1.2: Verify the yellow card's color."""
    assert yellow_card_color_result.color_name == expected_color, (
        f"Expected color '{expected_color}', got '{yellow_card_color_result.color_name}'"
    )


# ---------------------------------------------------------------------------
# Scenario: Card with blue color strip is considered blue
# Tests Rule 2.1.2 - Blue color strip
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_1_color.feature",
    "Card with blue color strip is considered blue",
)
def test_card_with_blue_color_strip_is_blue():
    """Rule 2.1.2: A card with a blue color strip is considered blue."""
    pass


@given(
    "a card is created with a blue color strip",
    target_fixture="blue_card",
)
def step_given_blue_card():
    """Rule 2.1.2: Create a card with blue color strip."""
    return ColorCardStub(name="Blue Card", color_name="blue", pitch_value=3)


@when(
    "the engine checks the color of the blue card",
    target_fixture="blue_card_color_result",
)
def step_when_check_blue_card_color(blue_card):
    """Rule 2.1.2: Check the blue card's color."""
    return blue_card.check_color()


@then(parsers.parse('the color of the blue card should be "{expected_color}"'))
def step_then_blue_card_color_is(blue_card_color_result, expected_color):
    """Rule 2.1.2: Verify the blue card's color."""
    assert blue_card_color_result.color_name == expected_color, (
        f"Expected color '{expected_color}', got '{blue_card_color_result.color_name}'"
    )


# ---------------------------------------------------------------------------
# Scenario: Card with no color strip has no color
# Tests Rule 2.1.2 - No color strip
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_1_color.feature",
    "Card with no color strip has no color",
)
def test_card_with_no_color_strip_has_no_color():
    """Rule 2.1.2: A card with no color strip has no color."""
    pass


@given(
    "a card is created with no color strip",
    target_fixture="colorless_card",
)
def step_given_colorless_card():
    """Rule 2.1.2: Create a card with no color strip."""
    return ColorCardStub(name="Colorless Card", color_name=None, pitch_value=None)


@when(
    "the engine checks the color of the colorless card",
    target_fixture="colorless_card_color_result",
)
def step_when_check_colorless_card_color(colorless_card):
    """Rule 2.1.2: Check the colorless card's color."""
    return colorless_card.check_color()


@then("the colorless card should have no color")
def step_then_colorless_card_has_no_color(colorless_card_color_result):
    """Rule 2.1.2: Verify the card has no color."""
    assert not colorless_card_color_result.has_color, (
        "Card with no color strip should have no color"
    )
    assert colorless_card_color_result.color_name is None, (
        "Card with no color strip should have color_name = None"
    )


# ---------------------------------------------------------------------------
# Scenario: Card with pitch 1 typically has red color
# Tests Rule 2.1.2a - Pitch 1 typically associated with red
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_1_color.feature",
    "Card with pitch 1 typically has red color",
)
def test_card_pitch_1_typically_red():
    """Rule 2.1.2a: Cards with pitch 1 typically have a red color strip."""
    pass


@given(
    "a card is created with pitch value 1 and red color strip",
    target_fixture="red_pitch_1_card",
)
def step_given_pitch_1_red_card():
    """Rule 2.1.2a: Create a card with pitch 1 and red color (typical association)."""
    return ColorCardStub(name="Pitch 1 Red Card", color_name="red", pitch_value=1)


@when(
    "the engine checks both the color and pitch of the red pitch 1 card",
    target_fixture="red_pitch_1_result",
)
def step_when_check_pitch_1_color(red_pitch_1_card):
    """Rule 2.1.2a: Check color and pitch of pitch 1 red card."""
    return red_pitch_1_card.check_color_and_pitch()


@then(parsers.parse('the color of the red pitch 1 card should be "{expected_color}"'))
def step_then_red_pitch_1_color_is(red_pitch_1_result, expected_color):
    """Rule 2.1.2a: Verify the color of pitch 1 card."""
    assert red_pitch_1_result.color_name == expected_color, (
        f"Expected color '{expected_color}', got '{red_pitch_1_result.color_name}'"
    )


@then(parsers.parse("the pitch of the red pitch 1 card should be {expected_pitch:d}"))
def step_then_red_pitch_1_value_is(red_pitch_1_result, expected_pitch):
    """Rule 2.1.2a: Verify the pitch value."""
    assert red_pitch_1_result.pitch_value == expected_pitch, (
        f"Expected pitch {expected_pitch}, got {red_pitch_1_result.pitch_value}"
    )


# ---------------------------------------------------------------------------
# Scenario: Card with pitch 2 typically has yellow color
# Tests Rule 2.1.2a - Pitch 2 typically associated with yellow
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_1_color.feature",
    "Card with pitch 2 typically has yellow color",
)
def test_card_pitch_2_typically_yellow():
    """Rule 2.1.2a: Cards with pitch 2 typically have a yellow color strip."""
    pass


@given(
    "a card is created with pitch value 2 and yellow color strip",
    target_fixture="yellow_pitch_2_card",
)
def step_given_pitch_2_yellow_card():
    """Rule 2.1.2a: Create a card with pitch 2 and yellow color (typical association)."""
    return ColorCardStub(name="Pitch 2 Yellow Card", color_name="yellow", pitch_value=2)


@when(
    "the engine checks both the color and pitch of the yellow pitch 2 card",
    target_fixture="yellow_pitch_2_result",
)
def step_when_check_pitch_2_color(yellow_pitch_2_card):
    """Rule 2.1.2a: Check color and pitch of pitch 2 yellow card."""
    return yellow_pitch_2_card.check_color_and_pitch()


@then(
    parsers.parse('the color of the yellow pitch 2 card should be "{expected_color}"')
)
def step_then_yellow_pitch_2_color_is(yellow_pitch_2_result, expected_color):
    """Rule 2.1.2a: Verify the color of pitch 2 card."""
    assert yellow_pitch_2_result.color_name == expected_color, (
        f"Expected color '{expected_color}', got '{yellow_pitch_2_result.color_name}'"
    )


@then(
    parsers.parse("the pitch of the yellow pitch 2 card should be {expected_pitch:d}")
)
def step_then_yellow_pitch_2_value_is(yellow_pitch_2_result, expected_pitch):
    """Rule 2.1.2a: Verify the pitch value."""
    assert yellow_pitch_2_result.pitch_value == expected_pitch, (
        f"Expected pitch {expected_pitch}, got {yellow_pitch_2_result.pitch_value}"
    )


# ---------------------------------------------------------------------------
# Scenario: Card with pitch 3 typically has blue color
# Tests Rule 2.1.2a - Pitch 3 typically associated with blue
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_1_color.feature",
    "Card with pitch 3 typically has blue color",
)
def test_card_pitch_3_typically_blue():
    """Rule 2.1.2a: Cards with pitch 3 typically have a blue color strip."""
    pass


@given(
    "a card is created with pitch value 3 and blue color strip",
    target_fixture="blue_pitch_3_card",
)
def step_given_pitch_3_blue_card():
    """Rule 2.1.2a: Create a card with pitch 3 and blue color (typical association)."""
    return ColorCardStub(name="Pitch 3 Blue Card", color_name="blue", pitch_value=3)


@when(
    "the engine checks both the color and pitch of the blue pitch 3 card",
    target_fixture="blue_pitch_3_result",
)
def step_when_check_pitch_3_color(blue_pitch_3_card):
    """Rule 2.1.2a: Check color and pitch of pitch 3 blue card."""
    return blue_pitch_3_card.check_color_and_pitch()


@then(parsers.parse('the color of the blue pitch 3 card should be "{expected_color}"'))
def step_then_blue_pitch_3_color_is(blue_pitch_3_result, expected_color):
    """Rule 2.1.2a: Verify the color of pitch 3 card."""
    assert blue_pitch_3_result.color_name == expected_color, (
        f"Expected color '{expected_color}', got '{blue_pitch_3_result.color_name}'"
    )


@then(parsers.parse("the pitch of the blue pitch 3 card should be {expected_pitch:d}"))
def step_then_blue_pitch_3_value_is(blue_pitch_3_result, expected_pitch):
    """Rule 2.1.2a: Verify the pitch value."""
    assert blue_pitch_3_result.pitch_value == expected_pitch, (
        f"Expected pitch {expected_pitch}, got {blue_pitch_3_result.pitch_value}"
    )


# ---------------------------------------------------------------------------
# Scenario: Color and pitch are independent - red card can have pitch 3
# Tests Rule 2.1.2a - Independence of color and pitch
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_1_color.feature",
    "Color and pitch are independent - red card can have pitch 3",
)
def test_color_and_pitch_are_independent():
    """Rule 2.1.2a: Color and pitch are independent - red with pitch 3 is valid."""
    pass


@given(
    "a card is created with a red color strip and pitch value 3",
    target_fixture="red_pitch_3_card",
)
def step_given_red_card_with_pitch_3():
    """Rule 2.1.2a: Create a red card with pitch 3 (unusual but valid combination)."""
    return ColorCardStub(name="Red Pitch 3 Card", color_name="red", pitch_value=3)


@when(
    "the engine checks the color and pitch of the red pitch 3 card independently",
    target_fixture="red_pitch_3_result",
)
def step_when_check_red_pitch_3_independently(red_pitch_3_card):
    """Rule 2.1.2a: Check color and pitch as independent properties."""
    return red_pitch_3_card.check_color_and_pitch()


@then(parsers.parse('the color of the red pitch 3 card should be "{expected_color}"'))
def step_then_red_pitch_3_color_is(red_pitch_3_result, expected_color):
    """Rule 2.1.2a: Verify color is still red despite having pitch 3."""
    assert red_pitch_3_result.color_name == expected_color, (
        f"Expected color '{expected_color}', got '{red_pitch_3_result.color_name}'"
    )


@then(parsers.parse("the pitch of the red pitch 3 card should be {expected_pitch:d}"))
def step_then_red_pitch_3_value_is(red_pitch_3_result, expected_pitch):
    """Rule 2.1.2a: Verify pitch is 3 despite being a red card."""
    assert red_pitch_3_result.pitch_value == expected_pitch, (
        f"Expected pitch {expected_pitch}, got {red_pitch_3_result.pitch_value}"
    )


@then(
    "color and pitch of the red pitch 3 card should be recognized as independent properties"
)
def step_then_red_pitch_3_independent(red_pitch_3_result):
    """Rule 2.1.2a: Verify that color and pitch are flagged as independent."""
    assert red_pitch_3_result.are_independent, (
        "Color and pitch should be independent properties (Rule 2.1.2a)"
    )


# ---------------------------------------------------------------------------
# Scenario: Card with no printed pitch typically has no color strip
# Tests Rule 2.1.2a - No pitch typically means no color
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_1_color.feature",
    "Card with no printed pitch typically has no color strip",
)
def test_card_no_pitch_typically_no_color():
    """Rule 2.1.2a: Cards with no printed pitch typically do not have a color strip."""
    pass


@given(
    "a card is created with no pitch and no color strip",
    target_fixture="no_pitch_no_color_card",
)
def step_given_no_pitch_no_color_card():
    """Rule 2.1.2a: Create a card with neither pitch nor color (typical case)."""
    return ColorCardStub(
        name="No Pitch No Color Card", color_name=None, pitch_value=None
    )


@when(
    "the engine checks color and pitch of the no-pitch no-color card",
    target_fixture="no_pitch_no_color_result",
)
def step_when_check_no_pitch_no_color(no_pitch_no_color_card):
    """Rule 2.1.2a: Check color and pitch of no-pitch no-color card."""
    return no_pitch_no_color_card.check_color_and_pitch()


@then("the no-pitch no-color card should have no color")
def step_then_no_pitch_card_has_no_color(no_pitch_no_color_result):
    """Rule 2.1.2a: Verify the card has no color."""
    assert not no_pitch_no_color_result.has_color, (
        "Card with no color strip should have no color"
    )


@then("the no-pitch no-color card should have no pitch property")
def step_then_no_pitch_card_has_no_pitch(no_pitch_no_color_result):
    """Rule 2.1.2a: Verify the card has no pitch property."""
    assert not no_pitch_no_color_result.has_pitch, (
        "Card with no pitch should have has_pitch = False"
    )


# ---------------------------------------------------------------------------
# Scenario: Card without pitch can have a color via independent color property
# Tests Rule 2.1.2a - A card can have a color without a pitch (they are independent)
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_1_color.feature",
    "Card without pitch can have a color via independent color property",
)
def test_card_no_pitch_can_have_color():
    """Rule 2.1.2a: Color and pitch are independent; card can have color without pitch."""
    pass


@given(
    "a card is created with a blue color strip but no pitch property",
    target_fixture="blue_no_pitch_card",
)
def step_given_blue_card_without_pitch():
    """Rule 2.1.2a: Create a blue card without a pitch property."""
    return ColorCardStub(name="Blue No Pitch Card", color_name="blue", pitch_value=None)


@when(
    "the engine checks the color and pitch of the blue no-pitch card independently",
    target_fixture="blue_no_pitch_result",
)
def step_when_check_blue_no_pitch_independently(blue_no_pitch_card):
    """Rule 2.1.2a: Check color and pitch as independent properties."""
    return blue_no_pitch_card.check_color_and_pitch()


@then(parsers.parse('the color of the blue no-pitch card should be "{expected_color}"'))
def step_then_blue_no_pitch_color_is(blue_no_pitch_result, expected_color):
    """Rule 2.1.2a: Verify the card is still blue despite having no pitch."""
    assert blue_no_pitch_result.color_name == expected_color, (
        f"Expected color '{expected_color}', got '{blue_no_pitch_result.color_name}'"
    )


@then("the blue no-pitch card should have no pitch property")
def step_then_blue_no_pitch_has_no_pitch(blue_no_pitch_result):
    """Rule 2.1.2a: Verify the card has no pitch property."""
    assert not blue_no_pitch_result.has_pitch, (
        "Card without pitch should have has_pitch = False"
    )


@then(
    "color and pitch of the blue no-pitch card should be recognized as independent properties"
)
def step_then_blue_no_pitch_independence(blue_no_pitch_result):
    """Rule 2.1.2a: Verify that color and pitch are recognized as independent."""
    assert blue_no_pitch_result.are_independent, (
        "Color and pitch should be independent properties (Rule 2.1.2a)"
    )
