"""
Step definitions for Section 2.5: Life
Reference: Flesh and Blood Comprehensive Rules Section 2.5

This module implements behavioral tests for the life property of objects in
Flesh and Blood.

Rule 2.5.1: Life is a numeric property of an object, which represents the
            starting life total of that object.

Rule 2.5.1a: A permanent with the life property is a living object. [1.3.3]

Rule 2.5.2: The printed life of a card is typically located at the bottom
            right corner of a card next to the {h} symbol. The printed life
            defines the base life of a card. If a card does not have a printed
            life, it does not have the life property (0 is a valid printed
            life).

Rule 2.5.3: The life of a permanent can be modified. The term "life total" or
            the symbol {h} refers to the modified life of an object.

Rule 2.5.3a: A permanent's life total is equal to the permanent's base life,
             plus life gained and minus life lost, as recorded by the players
             of the game.

Rule 2.5.3b: Life gained and life lost are not continuous effects - they are
             discrete effects that apply once, and they permanently modify the
             life total. [8.5.7]

Rule 2.5.3c: If the base life of a permanent changes, then the life total is
             recalculated using the new base life value of the object.
             Example: Shiyana (20 base life, lost 5) copies Kano (15 base life)
             -> new life total = 10.

Rule 2.5.3d: A permanent's life total can be greater than its base life.

Rule 2.5.3e: A permanent cannot have a negative life total. If the life total
             is calculated to be less than zero, instead it is considered zero.

Rule 2.5.3f: If a permanent's life total is reduced to zero, it is cleared as
             a game state action; or if the permanent is a hero, their player
             loses or the game is a draw as a game state action. [1.10.2][4.5]

Rule 2.5.3g: If a living object ceases to exist, it is considered to have died.

Engine Features Needed for Section 2.5:
- [ ] CardInstance.has_life_property: True only if printed life exists (Rule 2.5.2)
- [ ] CardInstance.base_life: unmodified printed life (Rule 2.5.2)
- [ ] CardInstance.life_total: modified life for rule/effect references (Rule 2.5.3)
- [ ] Permanent.is_living_object: True only when in arena with life property (Rule 2.5.1a)
- [ ] Life tracking: life_gained and life_lost accumulate (Rule 2.5.3a)
- [ ] Life gain/loss are discrete effects that permanently modify life total (Rule 2.5.3b)
- [ ] Base life change triggers life_total recalculation preserving gain/loss (Rule 2.5.3c)
- [ ] life_total >= 0 enforcement (Rule 2.5.3e)
- [ ] GameStateAction.check_hero_deaths() for hero at 0 life (Rule 2.5.3f / 1.10.2a)
- [ ] GameStateAction.clear_zero_life_permanents() for non-hero at 0 life (Rule 2.5.3f / 1.10.2b)
- [ ] is_dead tracking for ceased living objects (Rule 2.5.3g)
"""

import pytest
from pytest_bdd import scenario, given, when, then, parsers
from dataclasses import dataclass, field
from typing import Optional


# ---------------------------------------------------------------------------
# Stub classes for testing Section 2.5 rules
# ---------------------------------------------------------------------------


@dataclass
class LifeCheckResultStub:
    """
    Result of checking a card's life property.

    Rule 2.5.1: Life is a numeric property.
    Rule 2.5.2: Printed life defines base life; no printed life = no property.
    """

    has_life_property: bool
    life_value: Optional[int]  # None if no life property
    is_numeric: bool = True


@dataclass
class LifeCardStub:
    """
    Stub representing a card with a life property.

    Models what the engine must implement for Section 2.5.

    Engine Features Needed:
    - [ ] CardInstance.base_life: unmodified printed life (Rule 2.5.2)
    - [ ] CardInstance.has_life_property: True only if printed life exists (Rule 2.5.2)
    - [ ] CardInstance.life_total: modified life for rule/effect references (Rule 2.5.3)
    - [ ] is_living_object: True only if permanent in arena with life property (Rule 2.5.1a)
    """

    name: str = "Test Card"
    printed_life: Optional[int] = None  # None if card has no life property
    life_gained: int = 0  # Accumulated life gained (Rule 2.5.3a)
    life_lost: int = 0  # Accumulated life lost (Rule 2.5.3a)
    is_in_arena: bool = (
        False  # Permanents must be in arena to be "living" (Rule 2.5.1a)
    )
    is_permanent_card: bool = True  # Whether this is a permanent-eligible card
    is_hero: bool = False  # Whether this is a hero card

    @property
    def has_life_property(self) -> bool:
        """Rule 2.5.2: Card has life property only if there is a printed life."""
        return self.printed_life is not None

    @property
    def base_life(self) -> Optional[int]:
        """Rule 2.5.2: Base life is the printed life."""
        return self.printed_life

    @property
    def life_total(self) -> Optional[int]:
        """
        Rule 2.5.3: The modified life of the object.
        Rule 2.5.3a: = base life + life gained - life lost.
        Rule 2.5.3e: Cannot be negative; capped at zero.

        The term "life total" or symbol {h} refers to this value.
        """
        if self.printed_life is None:
            return None
        raw_total = self.printed_life + self.life_gained - self.life_lost
        return max(0, raw_total)  # Rule 2.5.3e: no negative life total

    @property
    def is_living_object(self) -> bool:
        """Rule 2.5.1a: A permanent with the life property is a living object."""
        return self.is_permanent_card and self.is_in_arena and self.has_life_property

    def gain_life(self, amount: int):
        """
        Rule 2.5.3a/3b: Apply discrete life gain to the object.
        Life gained is a discrete effect that permanently modifies life total.
        """
        self.life_gained += amount

    def lose_life(self, amount: int):
        """
        Rule 2.5.3a/3b: Apply discrete life loss to the object.
        Life lost is a discrete effect that permanently modifies life total.
        """
        self.life_lost += amount

    def change_base_life(self, new_base_life: int):
        """
        Rule 2.5.3c: Change the base life value (e.g., via copy effect).
        Life total is recalculated from the new base life, preserving
        life_gained and life_lost.
        """
        self.printed_life = new_base_life
        # life_gained and life_lost are preserved; life_total is recalculated

    def check_life(self) -> LifeCheckResultStub:
        """Rule 2.5.1/2.5.2: Get the life property of this card."""
        return LifeCheckResultStub(
            has_life_property=self.has_life_property,
            life_value=self.life_total,
        )


@dataclass
class GameStateActionResultStub:
    """
    Stub for the result of game state actions triggered by zero life.

    Rule 2.5.3f: If a permanent's life total is reduced to zero,
    it is cleared as a game state action; or if the permanent is a hero,
    their player loses or the game is a draw as a game state action.

    Engine Features Needed:
    - [ ] GameStateAction.check_hero_deaths() handling hero at 0 life (Rule 1.10.2a)
    - [ ] GameStateAction.clear_zero_life_permanents() for non-hero (Rule 1.10.2b)
    """

    game_state_action_fired: bool = False
    hero_death_handled: bool = False
    permanent_cleared: bool = False
    result_type: str = ""


@dataclass
class DeathTrackingResultStub:
    """
    Stub tracking whether a living object that ceased to exist is considered dead.

    Rule 2.5.3g: If a living object ceases to exist, it is considered to have
    died.

    Engine Features Needed:
    - [ ] is_dead flag for living objects that have ceased (Rule 2.5.3g)
    """

    is_dead: bool = False
    ceased_to_exist: bool = False
    had_life_property: bool = False


# ---------------------------------------------------------------------------
# Scenario: Life is a numeric property of an object
# Tests Rule 2.5.1 - Life is a numeric property
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_5_life.feature",
    "Life is a numeric property of an object",
)
def test_life_is_numeric_property():
    """Rule 2.5.1: Life is a numeric property representing the starting life total."""
    pass


@given("a hero card named numeric hero with a printed life of 20")
def create_numeric_hero(life_game_state):
    """Rule 2.5.1: Create a hero card with 20 printed life."""
    life_game_state.numeric_hero = LifeCardStub(
        name="numeric hero", printed_life=20, is_hero=True
    )


@when("the engine checks the life property of the numeric hero")
def check_life_property_numeric_hero(life_game_state):
    """Rule 2.5.1/2.5.2: Check the life property of the numeric hero."""
    life_game_state.numeric_hero_check = life_game_state.numeric_hero.check_life()


@then("the numeric hero should have the life property")
def numeric_hero_has_life_property(life_game_state):
    """Rule 2.5.1: Hero with printed life should have the life property."""
    assert life_game_state.numeric_hero_check.has_life_property is True


@then("the life of the numeric hero should be 20")
def numeric_hero_life_is_20(life_game_state):
    """Rule 2.5.1: Life value should be 20."""
    assert life_game_state.numeric_hero_check.life_value == 20


@then("the life of the numeric hero should be numeric")
def numeric_hero_life_is_numeric(life_game_state):
    """Rule 2.5.1: Life property is numeric."""
    assert life_game_state.numeric_hero_check.is_numeric is True


# ---------------------------------------------------------------------------
# Scenario: Life property represents the starting life total
# Tests Rule 2.5.1 - Life represents starting life total
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_5_life.feature",
    "Life property represents the starting life total",
)
def test_life_represents_starting_life_total():
    """Rule 2.5.1: Life property represents the starting life total."""
    pass


@given("a hero card named starting total hero with a printed life of 40")
def create_starting_total_hero(life_game_state):
    """Rule 2.5.1: Create a hero with 40 printed life."""
    life_game_state.starting_total_hero = LifeCardStub(
        name="starting total hero", printed_life=40, is_hero=True
    )


@when("the engine checks the starting life total of the starting total hero")
def check_starting_life_total(life_game_state):
    """Rule 2.5.1: Check the starting life total."""
    life_game_state.starting_life_total = life_game_state.starting_total_hero.base_life


@then("the starting life total of the starting total hero should be 40")
def starting_life_total_is_40(life_game_state):
    """Rule 2.5.1: Starting life total equals the printed life."""
    assert life_game_state.starting_life_total == 40


# ---------------------------------------------------------------------------
# Scenario: Permanent with life property is a living object
# Tests Rule 2.5.1a - Living object identification
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_5_life.feature",
    "Permanent with life property is a living object",
)
def test_permanent_with_life_is_living_object():
    """Rule 2.5.1a: A permanent with the life property is a living object."""
    pass


@given("a permanent card named living ally with a printed life of 3")
def create_living_ally(life_game_state):
    """Rule 2.5.1a: Create an ally permanent with life property."""
    life_game_state.living_ally = LifeCardStub(
        name="living ally", printed_life=3, is_permanent_card=True, is_in_arena=False
    )


@given("the living ally permanent is placed in the arena")
def place_living_ally_in_arena(life_game_state):
    """Rule 2.5.1a: Place the ally in the arena."""
    life_game_state.living_ally.is_in_arena = True


@when("the engine checks if the living ally is a living object")
def check_living_ally_is_living(life_game_state):
    """Rule 2.5.1a: Check living object status."""
    life_game_state.living_ally_is_living = life_game_state.living_ally.is_living_object


@then("the living ally should be a living object")
def living_ally_is_living_object(life_game_state):
    """Rule 2.5.1a: Permanent in arena with life property is a living object."""
    assert life_game_state.living_ally_is_living is True


# ---------------------------------------------------------------------------
# Scenario: Permanent without life property is not a living object
# Tests Rule 2.5.1a - Living object requires life property
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_5_life.feature",
    "Permanent without life property is not a living object",
)
def test_permanent_without_life_not_living():
    """Rule 2.5.1a: Permanents without the life property are NOT living objects."""
    pass


@given("a permanent card named lifeless equipment with no life property")
def create_lifeless_equipment(life_game_state):
    """Rule 2.5.1a: Create a permanent without life property."""
    life_game_state.lifeless_equipment = LifeCardStub(
        name="lifeless equipment",
        printed_life=None,
        is_permanent_card=True,
        is_in_arena=False,
    )


@given("the lifeless equipment permanent is placed in the arena")
def place_lifeless_equipment_in_arena(life_game_state):
    """Rule 2.5.1a: Place the lifeless equipment in the arena."""
    life_game_state.lifeless_equipment.is_in_arena = True


@when("the engine checks if the lifeless equipment is a living object")
def check_lifeless_equipment_is_living(life_game_state):
    """Rule 2.5.1a: Check living object status for no-life permanent."""
    life_game_state.lifeless_equipment_is_living = (
        life_game_state.lifeless_equipment.is_living_object
    )


@then("the lifeless equipment should not be a living object")
def lifeless_equipment_not_living(life_game_state):
    """Rule 2.5.1a: Permanent without life property is not a living object."""
    assert life_game_state.lifeless_equipment_is_living is False


# ---------------------------------------------------------------------------
# Scenario: Non-permanent card is not a living object even with life
# Tests Rule 2.5.1a - Only permanents can be living objects
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_5_life.feature",
    "Non-permanent card is not a living object even if it has a life property",
)
def test_non_permanent_not_living_even_with_life():
    """Rule 2.5.1a: Only permanents in the arena are living objects."""
    pass


@given("a non-permanent card named temporary creature with a printed life of 5")
def create_temporary_creature(life_game_state):
    """Rule 2.5.1a: Create a non-permanent card with life property."""
    life_game_state.temporary_creature = LifeCardStub(
        name="temporary creature",
        printed_life=5,
        is_permanent_card=False,  # Not a permanent card type
        is_in_arena=False,
    )


@when("the engine checks if the temporary creature is a living object")
def check_temporary_creature_is_living(life_game_state):
    """Rule 2.5.1a: Non-permanents are not living objects."""
    life_game_state.temporary_creature_is_living = (
        life_game_state.temporary_creature.is_living_object
    )


@then("the temporary creature should not be a living object")
def temporary_creature_not_living(life_game_state):
    """Rule 2.5.1a: A non-permanent card is not a living object even if it has life."""
    assert life_game_state.temporary_creature_is_living is False


# ---------------------------------------------------------------------------
# Scenario: Printed life defines the base life of a card
# Tests Rule 2.5.2 - Printed life defines base life
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_5_life.feature",
    "Printed life defines the base life of a card",
)
def test_printed_life_defines_base_life():
    """Rule 2.5.2: Printed life defines the base life."""
    pass


@given("a hero card named base life hero with a printed life of 20")
def create_base_life_hero(life_game_state):
    """Rule 2.5.2: Create a hero with 20 printed life for base life test."""
    life_game_state.base_life_hero = LifeCardStub(
        name="base life hero", printed_life=20, is_hero=True
    )


@when("the engine checks the base life of the base life hero")
def check_base_life_of_hero(life_game_state):
    """Rule 2.5.2: Check the base life of the hero."""
    life_game_state.base_life_value = life_game_state.base_life_hero.base_life


@then("the base life of the base life hero should be 20")
def base_life_of_hero_is_20(life_game_state):
    """Rule 2.5.2: Base life equals printed life."""
    assert life_game_state.base_life_value == 20


# ---------------------------------------------------------------------------
# Scenario: Zero is a valid printed life
# Tests Rule 2.5.2 - Zero is valid printed life
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_5_life.feature",
    "Zero is a valid printed life",
)
def test_zero_is_valid_printed_life():
    """Rule 2.5.2: Zero is a valid printed life value."""
    pass


@given("a card named zero life card with a printed life of 0")
def create_zero_life_card(life_game_state):
    """Rule 2.5.2: Create a card with zero printed life."""
    life_game_state.zero_life_card = LifeCardStub(name="zero life card", printed_life=0)


@when("the engine checks the life property of the zero life card")
def check_zero_life_card_property(life_game_state):
    """Rule 2.5.2: Check the life property of the zero-life card."""
    life_game_state.zero_life_check = life_game_state.zero_life_card.check_life()


@then("the zero life card should have the life property")
def zero_life_card_has_property(life_game_state):
    """Rule 2.5.2: Zero is a valid printed life; card still has the property."""
    assert life_game_state.zero_life_check.has_life_property is True


@then("the life of the zero life card should be 0")
def zero_life_card_value_is_0(life_game_state):
    """Rule 2.5.2: Life value equals 0."""
    assert life_game_state.zero_life_check.life_value == 0


# ---------------------------------------------------------------------------
# Scenario: Card without a printed life lacks the life property
# Tests Rule 2.5.2 - No printed life = no life property
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_5_life.feature",
    "Card without a printed life lacks the life property",
)
def test_card_without_printed_life_lacks_property():
    """Rule 2.5.2: Cards with no printed life do not have the life property."""
    pass


@given("a card named no life card with no printed life")
def create_no_life_card(life_game_state):
    """Rule 2.5.2: Create a card with no printed life."""
    life_game_state.no_life_card = LifeCardStub(name="no life card", printed_life=None)


@when("the engine checks the life property of the no life card")
def check_no_life_card_property(life_game_state):
    """Rule 2.5.2: Check the life property of the no-life card."""
    life_game_state.no_life_check = life_game_state.no_life_card.check_life()


@then("the no life card should not have the life property")
def no_life_card_lacks_property(life_game_state):
    """Rule 2.5.2: No printed life means no life property."""
    assert life_game_state.no_life_check.has_life_property is False


# ---------------------------------------------------------------------------
# Scenario: Life of a hero can be modified by effects
# Tests Rule 2.5.3 - Life can be modified
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_5_life.feature",
    "Life of a hero can be modified by effects",
)
def test_life_can_be_modified():
    """Rule 2.5.3: The life of a permanent can be modified."""
    pass


@given("a hero card named modify test hero with a printed life of 20")
def create_modify_test_hero(life_game_state):
    """Rule 2.5.3: Create a hero for modification test."""
    life_game_state.modify_test_hero = LifeCardStub(
        name="modify test hero", printed_life=20, is_hero=True
    )


@given("a life loss effect of 5 is applied to the modify test hero")
def apply_life_loss_5_to_modify_test_hero(life_game_state):
    """Rule 2.5.3: Apply a life loss effect of 5."""
    life_game_state.modify_test_hero.lose_life(5)


@when("the engine checks the modified life total of the modify test hero")
def check_modified_life_total(life_game_state):
    """Rule 2.5.3: Check the modified life total."""
    life_game_state.modified_life_total = life_game_state.modify_test_hero.life_total


@then("the modified life total of the modify test hero should be 15")
def modified_life_total_is_15(life_game_state):
    """Rule 2.5.3: After losing 5 life, 20 base -> 15 total."""
    assert life_game_state.modified_life_total == 15


# ---------------------------------------------------------------------------
# Scenario: The term life total refers to the modified life not base life
# Tests Rule 2.5.3 - "life total" = modified life
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_5_life.feature",
    "The term life total refers to the modified life not base life",
)
def test_life_total_refers_to_modified_life():
    """Rule 2.5.3: The term 'life total' refers to the modified life."""
    pass


@given("a hero card named life total term hero with a printed life of 20")
def create_life_total_term_hero(life_game_state):
    """Rule 2.5.3: Create a hero for life total term test."""
    life_game_state.life_total_term_hero = LifeCardStub(
        name="life total term hero", printed_life=20, is_hero=True
    )


@given("a life gain effect of 3 is applied to the life total term hero")
def apply_life_gain_3_to_term_hero(life_game_state):
    """Rule 2.5.3: Apply a life gain effect of 3."""
    life_game_state.life_total_term_hero.gain_life(3)


@when("the engine resolves the term life total for the life total term hero")
def resolve_term_life_total(life_game_state):
    """Rule 2.5.3: Resolve the term 'life total'."""
    life_game_state.resolved_term_life_total = (
        life_game_state.life_total_term_hero.life_total
    )


@then("the resolved life total of the life total term hero should be 23")
def resolved_term_life_total_is_23(life_game_state):
    """Rule 2.5.3: Life total (modified) = 20 + 3 = 23."""
    assert life_game_state.resolved_term_life_total == 23


@then("the base life of the life total term hero should remain 20")
def base_life_remains_20_after_gain(life_game_state):
    """Rule 2.5.3: Base life is unchanged when life is gained."""
    assert life_game_state.life_total_term_hero.base_life == 20


# ---------------------------------------------------------------------------
# Scenario: The symbol h refers to the modified life total of an object
# Tests Rule 2.5.3 - {h} symbol refers to modified life
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_5_life.feature",
    "The symbol h refers to the modified life total of an object",
)
def test_h_symbol_refers_to_modified_life():
    """Rule 2.5.3: The symbol {h} refers to the modified life total."""
    pass


@given("a hero card named h symbol hero with a printed life of 20")
def create_h_symbol_hero(life_game_state):
    """Rule 2.5.3: Create a hero for {h} symbol test."""
    life_game_state.h_symbol_hero = LifeCardStub(
        name="h symbol hero", printed_life=20, is_hero=True
    )


@given("a life loss effect of 5 is applied to the h symbol hero")
def apply_life_loss_5_to_h_symbol_hero(life_game_state):
    """Rule 2.5.3: Apply a life loss of 5 to the {h} symbol test hero."""
    life_game_state.h_symbol_hero.lose_life(5)


@when("the engine resolves the h symbol for the h symbol hero")
def resolve_h_symbol(life_game_state):
    """Rule 2.5.3: Resolve {h} symbol which equals the modified life total."""
    life_game_state.h_symbol_value = life_game_state.h_symbol_hero.life_total


@then("the resolved h symbol value for h symbol hero should be 15")
def h_symbol_value_is_15(life_game_state):
    """Rule 2.5.3: {h} = modified life total = 20 - 5 = 15."""
    assert life_game_state.h_symbol_value == 15


# ---------------------------------------------------------------------------
# Scenario: Life total equals base life plus life gained minus life lost
# Tests Rule 2.5.3a - Life total formula
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_5_life.feature",
    "Life total equals base life plus life gained minus life lost",
)
def test_life_total_formula():
    """Rule 2.5.3a: Life total = base life + gained - lost."""
    pass


@given("a hero card named formula hero with a printed life of 20")
def create_formula_hero(life_game_state):
    """Rule 2.5.3a: Create a hero for formula test."""
    life_game_state.formula_hero = LifeCardStub(
        name="formula hero", printed_life=20, is_hero=True
    )


@given("the formula hero gains 5 life")
def formula_hero_gains_5(life_game_state):
    """Rule 2.5.3a: Formula hero gains 5 life."""
    life_game_state.formula_hero.gain_life(5)


@given("the formula hero loses 3 life")
def formula_hero_loses_3(life_game_state):
    """Rule 2.5.3a: Formula hero loses 3 life."""
    life_game_state.formula_hero.lose_life(3)


@when("the engine calculates the life total of the formula hero")
def calculate_formula_hero_life_total(life_game_state):
    """Rule 2.5.3a: Calculate life total using the formula."""
    life_game_state.formula_result = life_game_state.formula_hero.life_total


@then("the formula hero life total should be 22")
def formula_hero_life_total_is_22(life_game_state):
    """Rule 2.5.3a: 20 + 5 - 3 = 22."""
    assert life_game_state.formula_result == 22


# ---------------------------------------------------------------------------
# Scenario: Multiple life gain and loss events accumulate in the life total
# Tests Rule 2.5.3a - Accumulation
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_5_life.feature",
    "Multiple life gain and loss events accumulate in the life total",
)
def test_multiple_life_events_accumulate():
    """Rule 2.5.3a: Life events accumulate correctly."""
    pass


@given("a hero card named accumulate hero with a printed life of 20")
def create_accumulate_hero(life_game_state):
    """Rule 2.5.3a: Create a hero for accumulation test."""
    life_game_state.accumulate_hero = LifeCardStub(
        name="accumulate hero", printed_life=20, is_hero=True
    )


@given("the accumulate hero gains 2 life in a first event")
def accumulate_hero_gains_2(life_game_state):
    """Rule 2.5.3a: First life gain event."""
    life_game_state.accumulate_hero.gain_life(2)


@given("the accumulate hero gains 4 life in a second event")
def accumulate_hero_gains_4(life_game_state):
    """Rule 2.5.3a: Second life gain event."""
    life_game_state.accumulate_hero.gain_life(4)


@given("the accumulate hero loses 1 life in a third event")
def accumulate_hero_loses_1(life_game_state):
    """Rule 2.5.3a: Third life loss event."""
    life_game_state.accumulate_hero.lose_life(1)


@when("the engine calculates the accumulated life total of the accumulate hero")
def calculate_accumulate_hero_life_total(life_game_state):
    """Rule 2.5.3a: Calculate the accumulated life total."""
    life_game_state.accumulated_total = life_game_state.accumulate_hero.life_total


@then("the accumulate hero life total should be 25")
def accumulate_hero_total_is_25(life_game_state):
    """Rule 2.5.3a: 20 + 2 + 4 - 1 = 25."""
    assert life_game_state.accumulated_total == 25


# ---------------------------------------------------------------------------
# Scenario: Life gained and life lost are discrete effects not continuous
# Tests Rule 2.5.3b - Life gain/loss are discrete, not continuous
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_5_life.feature",
    "Life gained and life lost are discrete effects not continuous",
)
def test_life_gain_loss_are_discrete():
    """Rule 2.5.3b: Life gained/lost are discrete effects, not continuous."""
    pass


@given("a hero card named discrete hero with a printed life of 20")
def create_discrete_hero(life_game_state):
    """Rule 2.5.3b: Create hero for discrete effect test."""
    life_game_state.discrete_hero = LifeCardStub(
        name="discrete hero", printed_life=20, is_hero=True
    )


@given("a discrete life gain of 5 is applied to the discrete hero")
def apply_discrete_life_gain_5(life_game_state):
    """Rule 2.5.3b: Apply a discrete (one-shot) life gain of 5."""
    # Discrete effects permanently modify life total (applied once)
    life_game_state.discrete_hero.gain_life(5)
    life_game_state.discrete_effect_was_applied = True


@when("the discrete hero life gain source is removed")
def remove_discrete_hero_life_gain_source(life_game_state):
    """
    Rule 2.5.3b: Simulate removal of the 'source' of a discrete life gain.
    Since life gain is discrete (not continuous), removing the source does NOT
    undo the life gained - it permanently modified the life total.
    """
    # In a real engine, removing a continuous effect would undo it.
    # But removing the source of a discrete effect does nothing - it already fired.
    # The life_gained value remains unchanged.
    life_game_state.life_after_source_removed = life_game_state.discrete_hero.life_total


@then("the discrete hero life total should remain 25")
def discrete_hero_life_remains_25(life_game_state):
    """Rule 2.5.3b: Discrete life total remains 25 even after source removed."""
    assert life_game_state.life_after_source_removed == 25


# ---------------------------------------------------------------------------
# Scenario: Discrete life effects permanently modify life total
# Tests Rule 2.5.3b - Permanent modification
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_5_life.feature",
    "Discrete life effects permanently modify life total",
)
def test_discrete_life_permanently_modifies():
    """Rule 2.5.3b: Discrete life gain permanently modifies life total."""
    pass


@given("a hero card named permanent mod hero with a printed life of 20")
def create_permanent_mod_hero(life_game_state):
    """Rule 2.5.3b: Create hero for permanent modification test."""
    life_game_state.permanent_mod_hero = LifeCardStub(
        name="permanent mod hero", printed_life=20, is_hero=True
    )


@given("a permanent life gain of 3 is applied to the permanent mod hero")
def apply_permanent_life_gain_3(life_game_state):
    """Rule 2.5.3b: Apply a discrete (permanent) life gain of 3."""
    life_game_state.permanent_mod_hero.gain_life(3)


@when("the engine checks the permanent mod hero life total")
def check_permanent_mod_hero_life_total(life_game_state):
    """Rule 2.5.3b: Check life total after permanent modification."""
    life_game_state.permanent_mod_total = life_game_state.permanent_mod_hero.life_total


@then("the permanent mod hero life total should be 23")
def permanent_mod_total_is_23(life_game_state):
    """Rule 2.5.3b: Life total is 23 permanently (discrete effect applied once)."""
    assert life_game_state.permanent_mod_total == 23


# ---------------------------------------------------------------------------
# Scenario: Changing base life recalculates life total preserving life lost
# Tests Rule 2.5.3c - Shiyana example: base life change recalculates total
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_5_life.feature",
    "Changing base life recalculates life total preserving life lost",
)
def test_base_life_change_recalculates_preserving_lost():
    """Rule 2.5.3c: Base life change recalculates total (Shiyana example)."""
    pass


@given("a hero card named Shiyana with a printed life of 20")
def create_shiyana(life_game_state):
    """Rule 2.5.3c: Create Shiyana with 20 printed life."""
    life_game_state.shiyana = LifeCardStub(
        name="Shiyana", printed_life=20, is_hero=True
    )


@given("the Shiyana hero loses 5 life")
def shiyana_loses_5(life_game_state):
    """Rule 2.5.3c: Shiyana loses 5 life."""
    life_game_state.shiyana.lose_life(5)


@given("the Shiyana hero base life changes to 15 via copy")
def shiyana_base_life_changes_to_15(life_game_state):
    """Rule 2.5.3c: Shiyana copies Kano (base life 15)."""
    life_game_state.shiyana.change_base_life(15)


@when("the engine recalculates the Shiyana hero life total")
def recalculate_shiyana_life_total(life_game_state):
    """Rule 2.5.3c: Recalculate life total with new base."""
    life_game_state.shiyana_recalculated = life_game_state.shiyana.life_total


@then("the Shiyana hero life total should be 10")
def shiyana_life_total_is_10(life_game_state):
    """Rule 2.5.3c: Shiyana new total = 15 (new base) - 5 (life lost) = 10."""
    assert life_game_state.shiyana_recalculated == 10


# ---------------------------------------------------------------------------
# Scenario: Changing base life recalculates life total preserving life gained
# Tests Rule 2.5.3c - Base life change with life gained
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_5_life.feature",
    "Changing base life recalculates life total preserving life gained",
)
def test_base_life_change_preserves_life_gained():
    """Rule 2.5.3c: Base life change recalculates preserving life gained."""
    pass


@given("a hero card named Copycat with a printed life of 20")
def create_copycat(life_game_state):
    """Rule 2.5.3c: Create Copycat hero with 20 printed life."""
    life_game_state.copycat = LifeCardStub(
        name="Copycat", printed_life=20, is_hero=True
    )


@given("the Copycat hero gains 3 life")
def copycat_gains_3(life_game_state):
    """Rule 2.5.3c: Copycat gains 3 life."""
    life_game_state.copycat.gain_life(3)


@given("the Copycat hero base life changes to 10 via copy")
def copycat_base_life_changes_to_10(life_game_state):
    """Rule 2.5.3c: Copycat base life changes to 10 via copy effect."""
    life_game_state.copycat.change_base_life(10)


@when("the engine recalculates the Copycat hero life total")
def recalculate_copycat_life_total(life_game_state):
    """Rule 2.5.3c: Recalculate with new base, preserving gained."""
    life_game_state.copycat_recalculated = life_game_state.copycat.life_total


@then("the Copycat hero life total should be 13")
def copycat_life_total_is_13(life_game_state):
    """Rule 2.5.3c: Copycat new total = 10 (new base) + 3 (gained) = 13."""
    assert life_game_state.copycat_recalculated == 13


# ---------------------------------------------------------------------------
# Scenario: Life total can be greater than base life
# Tests Rule 2.5.3d - Life total can exceed base life
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_5_life.feature",
    "Life total can be greater than base life",
)
def test_life_total_can_exceed_base():
    """Rule 2.5.3d: A permanent's life total can be greater than its base life."""
    pass


@given("a hero card named exceed hero with a printed life of 20")
def create_exceed_hero(life_game_state):
    """Rule 2.5.3d: Create a hero with 20 printed life."""
    life_game_state.exceed_hero = LifeCardStub(
        name="exceed hero", printed_life=20, is_hero=True
    )


@given("a life gain effect of 5 is applied to the exceed hero")
def apply_life_gain_5_to_exceed_hero(life_game_state):
    """Rule 2.5.3d: Apply life gain of 5 (life total will exceed base)."""
    life_game_state.exceed_hero.gain_life(5)


@when("the engine checks if the exceed hero life total exceeds base life")
def check_exceed_hero_life_exceeds_base(life_game_state):
    """Rule 2.5.3d: Check if life total > base life."""
    hero = life_game_state.exceed_hero
    life_game_state.exceed_life_total = hero.life_total
    life_game_state.exceed_base_life = hero.base_life
    life_game_state.life_exceeds_base = hero.life_total > hero.base_life


@then("the exceed hero life total of 25 should exceed base life of 20")
def exceed_hero_life_total_exceeds_base(life_game_state):
    """Rule 2.5.3d: Life total (25) > base life (20)."""
    assert life_game_state.life_exceeds_base is True
    assert life_game_state.exceed_life_total == 25
    assert life_game_state.exceed_base_life == 20


# ---------------------------------------------------------------------------
# Scenario: Life total cannot be negative and is capped at zero
# Tests Rule 2.5.3e - Capped at zero
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_5_life.feature",
    "Life total cannot be negative and is capped at zero",
)
def test_life_total_capped_at_zero():
    """Rule 2.5.3e: Life total cannot be negative; capped at zero."""
    pass


@given("a hero card named low life hero with a printed life of 5")
def create_low_life_hero(life_game_state):
    """Rule 2.5.3e: Create a hero with 5 printed life."""
    life_game_state.low_life_hero = LifeCardStub(
        name="low life hero", printed_life=5, is_hero=True
    )


@given("a life loss effect of 10 is applied to the low life hero")
def apply_life_loss_10_to_low_life_hero(life_game_state):
    """Rule 2.5.3e: Apply life loss of 10 (exceeds base life of 5)."""
    life_game_state.low_life_hero.lose_life(10)


@when("the engine calculates the low life hero capped life total")
def calculate_low_life_hero_capped_total(life_game_state):
    """Rule 2.5.3e: Calculate life total (should be capped at 0)."""
    life_game_state.capped_life_total = life_game_state.low_life_hero.life_total


@then("the low life hero capped life total should be 0")
def low_life_hero_capped_total_is_0(life_game_state):
    """Rule 2.5.3e: 5 - 10 = -5, but capped at 0."""
    assert life_game_state.capped_life_total == 0


# ---------------------------------------------------------------------------
# Scenario: Life total reduced to exactly zero is zero not negative
# Tests Rule 2.5.3e - Exactly zero
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_5_life.feature",
    "Life total reduced to exactly zero is zero not negative",
)
def test_life_total_exactly_zero():
    """Rule 2.5.3e: Life total reduced to exactly zero remains zero."""
    pass


@given("a hero card named exact zero hero with a printed life of 5")
def create_exact_zero_hero(life_game_state):
    """Rule 2.5.3e: Create hero with 5 printed life for exact zero test."""
    life_game_state.exact_zero_hero = LifeCardStub(
        name="exact zero hero", printed_life=5, is_hero=True
    )


@given("a life loss effect of 5 is applied to the exact zero hero")
def apply_life_loss_5_to_exact_zero_hero(life_game_state):
    """Rule 2.5.3e: Apply life loss of 5 (equals base life)."""
    life_game_state.exact_zero_hero.lose_life(5)


@when("the engine checks the exact zero hero life total")
def check_exact_zero_hero_life_total(life_game_state):
    """Rule 2.5.3e: Check life total is exactly 0."""
    life_game_state.exact_zero_total = life_game_state.exact_zero_hero.life_total


@then("the exact zero hero life total should be exactly 0")
def exact_zero_hero_total_is_0(life_game_state):
    """Rule 2.5.3e: 5 - 5 = 0."""
    assert life_game_state.exact_zero_total == 0


# ---------------------------------------------------------------------------
# Scenario: Hero reaching zero life is handled as a game state action
# Tests Rule 2.5.3f - Hero at zero life causes game state action
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_5_life.feature",
    "Hero reaching zero life is handled as a game state action",
)
def test_hero_zero_life_triggers_game_state_action():
    """Rule 2.5.3f: Hero at 0 life triggers a game state action (player loss/draw)."""
    pass


@given("a hero card named dying hero with a printed life of 20")
def create_dying_hero(life_game_state):
    """Rule 2.5.3f: Create hero for game state action test."""
    life_game_state.dying_hero = LifeCardStub(
        name="dying hero", printed_life=20, is_hero=True
    )


@given("a life loss effect of 20 is applied to the dying hero")
def apply_life_loss_20_to_dying_hero(life_game_state):
    """Rule 2.5.3f: Apply full life loss - hero reaches 0."""
    life_game_state.dying_hero.lose_life(20)


@when("the engine transitions to priority state with dying hero at zero life")
def transition_to_priority_state_dying_hero(life_game_state):
    """
    Rule 2.5.3f: Simulate game state transition when hero has 0 life.

    Engine Feature Needed:
    - [ ] GameStateAction.check_hero_deaths() detecting 0-life heroes (Rule 1.10.2a)
    - [ ] Game state action fires for hero death (not player action)
    """
    hero = life_game_state.dying_hero
    result = GameStateActionResultStub()
    if hero.life_total == 0 and hero.is_hero:
        result.game_state_action_fired = True
        result.hero_death_handled = True
        result.result_type = "player_loss"
    life_game_state.dying_hero_action_result = result


@then("a game state action should fire for the dying hero at zero life")
def game_state_action_fires_for_dying_hero(life_game_state):
    """Rule 2.5.3f: Game state action fires for hero at 0 life."""
    assert life_game_state.dying_hero_action_result.game_state_action_fired is True
    assert life_game_state.dying_hero_action_result.hero_death_handled is True


# ---------------------------------------------------------------------------
# Scenario: Non-hero permanent with zero life total is cleared from arena
# Tests Rule 2.5.3f - Non-hero permanent at zero life is cleared
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_5_life.feature",
    "Non-hero permanent with zero life total is cleared from arena",
)
def test_non_hero_permanent_zero_life_cleared():
    """Rule 2.5.3f: Non-hero permanent at 0 life is cleared as game state action."""
    pass


@given("an ally permanent named zero ally with a printed life of 3")
def create_zero_ally(life_game_state):
    """Rule 2.5.3f: Create an ally permanent with 3 printed life."""
    life_game_state.zero_ally = LifeCardStub(
        name="zero ally", printed_life=3, is_permanent_card=True, is_hero=False
    )


@given("the zero ally is placed in the arena")
def place_zero_ally_in_arena(life_game_state):
    """Rule 2.5.3f: Place the ally in the arena."""
    life_game_state.zero_ally.is_in_arena = True


@given("a life loss effect of 3 is applied to the zero ally")
def apply_life_loss_3_to_zero_ally(life_game_state):
    """Rule 2.5.3f: Apply life loss equal to ally's life."""
    life_game_state.zero_ally.lose_life(3)


@when("the engine transitions to priority state with zero ally at zero life")
def transition_to_priority_state_zero_ally(life_game_state):
    """
    Rule 2.5.3f: Simulate game state transition when non-hero permanent has 0 life.

    Engine Feature Needed:
    - [ ] GameStateAction.clear_zero_life_permanents() removing 0-life permanents (Rule 1.10.2b)
    """
    ally = life_game_state.zero_ally
    result = GameStateActionResultStub()
    if ally.life_total == 0 and ally.is_living_object and not ally.is_hero:
        result.game_state_action_fired = True
        result.permanent_cleared = True
        result.result_type = "permanent_cleared"
        # Simulate clearing: remove from arena
        ally.is_in_arena = False
    life_game_state.zero_ally_action_result = result


@then("a game state action should fire to clear the zero ally")
def game_state_action_clears_zero_ally(life_game_state):
    """Rule 2.5.3f: Game state action fires to clear the 0-life ally."""
    assert life_game_state.zero_ally_action_result.game_state_action_fired is True
    assert life_game_state.zero_ally_action_result.permanent_cleared is True


# ---------------------------------------------------------------------------
# Scenario: Living object ceasing to exist is considered dead
# Tests Rule 2.5.3g - Death when ceasing to exist
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_5_life.feature",
    "Living object ceasing to exist is considered dead",
)
def test_living_object_ceasing_is_dead():
    """Rule 2.5.3g: If a living object ceases to exist, it is considered to have died."""
    pass


@given("a permanent card named ceasing permanent with a printed life of 5")
def create_ceasing_permanent(life_game_state):
    """Rule 2.5.3g: Create a permanent that will cease to exist."""
    life_game_state.ceasing_permanent = LifeCardStub(
        name="ceasing permanent", printed_life=5, is_permanent_card=True
    )


@given("the ceasing permanent is in the arena as a living object")
def ceasing_permanent_in_arena(life_game_state):
    """Rule 2.5.3g: Ceasing permanent is in arena (is a living object)."""
    life_game_state.ceasing_permanent.is_in_arena = True
    assert life_game_state.ceasing_permanent.is_living_object is True
    life_game_state.ceasing_death_tracking = DeathTrackingResultStub(
        had_life_property=True
    )


@when("the ceasing permanent ceases to exist")
def ceasing_permanent_ceases(life_game_state):
    """
    Rule 2.5.3g: The permanent ceases to exist.

    Engine Feature Needed:
    - [ ] is_dead flag set when living object ceases to exist (Rule 2.5.3g)
    """
    # Simulate the permanent ceasing to exist (removed from arena)
    life_game_state.ceasing_permanent.is_in_arena = False
    life_game_state.ceasing_death_tracking.ceased_to_exist = True
    life_game_state.ceasing_death_tracking.is_dead = True


@then("the ceasing permanent should be considered to have died")
def ceasing_permanent_is_dead(life_game_state):
    """Rule 2.5.3g: Permanent that ceased to exist is considered dead."""
    assert life_game_state.ceasing_death_tracking.ceased_to_exist is True
    assert life_game_state.ceasing_death_tracking.is_dead is True


# ---------------------------------------------------------------------------
# Scenario: Card dying is distinct from card merely losing life
# Tests Rule 2.5.3g - Death vs life loss distinction
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_5_life.feature",
    "Card dying is distinct from card merely losing life",
)
def test_death_distinct_from_life_loss():
    """Rule 2.5.3g: A living object that lost life but still exists has NOT died."""
    pass


@given("a permanent card named surviving permanent with a printed life of 5")
def create_surviving_permanent(life_game_state):
    """Rule 2.5.3g: Create a permanent that will lose life but survive."""
    life_game_state.surviving_permanent = LifeCardStub(
        name="surviving permanent", printed_life=5, is_permanent_card=True
    )
    life_game_state.surviving_permanent.is_in_arena = True


@given("the surviving permanent loses 2 life but remains in the arena")
def surviving_permanent_loses_2_life(life_game_state):
    """Rule 2.5.3g: Permanent loses life but stays in arena (still exists)."""
    life_game_state.surviving_permanent.lose_life(2)
    # Still in arena - not ceased
    assert life_game_state.surviving_permanent.is_in_arena is True


@when("the engine checks the surviving permanent death status")
def check_surviving_permanent_death(life_game_state):
    """Rule 2.5.3g: Check if living object that lost life is considered dead."""
    life_game_state.surviving_death_tracking = DeathTrackingResultStub(
        had_life_property=True,
        ceased_to_exist=False,
        is_dead=False,
    )


@then("the surviving permanent should not be considered dead")
def surviving_permanent_not_dead(life_game_state):
    """Rule 2.5.3g: Losing life does not make an object dead; ceasing does."""
    assert life_game_state.surviving_death_tracking.is_dead is False
    # Verify the permanent is still a living object
    assert life_game_state.surviving_permanent.is_living_object is True


# ---------------------------------------------------------------------------
# Scenario: Multiple cards maintain independent life totals
# Tests independence of multiple life totals
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_5_life.feature",
    "Multiple cards maintain independent life totals",
)
def test_multiple_independent_life_totals():
    """Rule 2.5.2: Each card has its own independent life total."""
    pass


@given("a hero card named independent hero A with a printed life of 20")
def create_independent_hero_a(life_game_state):
    """Create first hero with 20 printed life."""
    life_game_state.independent_hero_a = LifeCardStub(
        name="independent hero A", printed_life=20, is_hero=True
    )


@given("a hero card named independent hero B with a printed life of 40")
def create_independent_hero_b(life_game_state):
    """Create second hero with 40 printed life."""
    life_game_state.independent_hero_b = LifeCardStub(
        name="independent hero B", printed_life=40, is_hero=True
    )


@when("a life loss of 5 is applied to independent hero A only")
def apply_life_loss_to_hero_a_only(life_game_state):
    """Apply life loss to hero A only; hero B unaffected."""
    life_game_state.independent_hero_a.lose_life(5)


@then("independent hero A life total should be 15")
def hero_a_life_is_15(life_game_state):
    """Hero A: 20 - 5 = 15."""
    assert life_game_state.independent_hero_a.life_total == 15


@then("independent hero B life total should be 40")
def hero_b_life_is_40(life_game_state):
    """Hero B is unaffected: still 40."""
    assert life_game_state.independent_hero_b.life_total == 40


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def life_game_state():
    """
    Fixture providing game state for Section 2.5 Life testing.

    Uses stub classes to document required engine features.
    All tests verify behavioral specifications from the comprehensive rules.

    Engine Features Needed:
    - [ ] CardInstance.has_life_property (Rule 2.5.2)
    - [ ] CardInstance.base_life (Rule 2.5.2)
    - [ ] CardInstance.life_total (Rule 2.5.3)
    - [ ] Permanent.is_living_object (Rule 2.5.1a)
    - [ ] Life tracking: life_gained + life_lost accumulation (Rule 2.5.3a)
    - [ ] Discrete life effects (Rule 2.5.3b)
    - [ ] Base life change recalculation (Rule 2.5.3c)
    - [ ] life_total >= 0 enforcement (Rule 2.5.3e)
    - [ ] GameStateAction.check_hero_deaths() (Rule 2.5.3f / 1.10.2a)
    - [ ] GameStateAction.clear_zero_life_permanents() (Rule 2.5.3f / 1.10.2b)
    - [ ] is_dead tracking for ceased living objects (Rule 2.5.3g)
    """
    from tests.bdd_helpers import BDDGameState

    state = BDDGameState()
    return state
