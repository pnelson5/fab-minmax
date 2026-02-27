"""
Step definitions for Section 2.7: Name
Reference: Flesh and Blood Comprehensive Rules Section 2.7

This module implements behavioral tests for name property rules in Flesh and Blood.

Rule 2.7.1: Name is a property of an object, which represents one of its object
            identities and determines the object's uniqueness (along with the
            pitch property). [1.2.2][1.3.4]

Rule 2.7.2: The printed name of a card is typically located at the top of the
            card. The printed name defines the name of a card.

Rule 2.7.3: If an object has a name that is a personal name, that name
            determines the object's moniker. A personal name is typically
            written in the format "[HONORIFIC?] [MONIKER] [LAST?] [, SUFFIX?]."

Rule 2.7.3a: If an object does not have a name that is a personal name, it does
             not have a moniker.

Rule 2.7.3b: If two objects have different names, they may have the same moniker.
             An effect that refers to an object using a moniker may refer to two
             or more objects with different names but the same moniker.

Rule 2.7.3c: A moniker is not considered a name. If an effect identifies an
             object by a name, it does not identify objects with a moniker that
             is the same as that name.

Rule 2.7.4: An object's printed name is always considered to be the English
            language version of its name, regardless of the printed language.

Rule 2.7.5: A name or part of a name is equal to another name or part of a name
            only if it is an exact case-insensitive match of each whole word in
            order.

Engine Features Needed for Section 2.7:
- [ ] CardTemplate.name property: the printed name of the card (Rule 2.7.2)
- [ ] CardInstance.name property: accessible on instances (Rule 2.7.1)
- [ ] CardInstance.get_object_identities(): includes name as identity (Rule 2.7.1)
- [ ] CardTemplate.moniker property: derived from personal name, or None (Rule 2.7.3)
- [ ] PersonalNameParser.extract_moniker(name) -> str | None (Rule 2.7.3)
- [ ] CardTemplate.has_moniker: bool property (Rule 2.7.3/2.7.3a)
- [ ] NameMatcher.matches(candidate, query) -> bool with whole-word, case-insensitive (Rule 2.7.5)
- [ ] NameMatcher.matches_moniker(objects, moniker) -> List (Rule 2.7.3b)
- [ ] CardTemplate.is_distinct_from(other): based on name+pitch (Rule 2.7.1 / cross-ref 1.3.4)
- [ ] Engine name handling: English-language canonical name always used (Rule 2.7.4)
"""

import pytest
from pytest_bdd import scenario, given, when, then, parsers
from dataclasses import dataclass, field
from typing import Optional, List


# ---------------------------------------------------------------------------
# Stub classes for testing Section 2.7 rules
# ---------------------------------------------------------------------------


@dataclass
class NameCardStub:
    """
    Stub representing a card with a name property.

    Models what the engine must implement for Section 2.7.

    Engine Features Needed:
    - [ ] CardTemplate.name: the printed name (Rule 2.7.2)
    - [ ] CardInstance.name accessible from instance (Rule 2.7.1)
    - [ ] CardTemplate.moniker: derived from personal name (Rule 2.7.3)
    - [ ] CardTemplate.has_moniker: bool (Rule 2.7.3/2.7.3a)
    - [ ] CardInstance.get_object_identities(): includes name (Rule 2.7.1)
    """

    name: str
    pitch_value: Optional[int] = None
    is_personal_name: bool = False
    _moniker: Optional[str] = None
    _language_version: str = "english"

    @property
    def has_name_property(self) -> bool:
        """
        Rule 2.7.1: Name is a property of an object.
        Every card has a name property.
        """
        return True

    @property
    def moniker(self) -> Optional[str]:
        """
        Rule 2.7.3: Personal name determines the moniker.
        Rule 2.7.3a: Non-personal names have no moniker (returns None).
        """
        if not self.is_personal_name:
            return None
        return self._moniker

    @property
    def has_moniker(self) -> bool:
        """
        Rule 2.7.3/2.7.3a: Only personal names have monikers.
        """
        return self.moniker is not None

    def get_object_identities(self) -> List[str]:
        """
        Rule 2.7.1: Name is one of the card's object identities.
        Rule 1.2.2: All objects have the 'object' identity; named objects have
                    their name as an identity.

        Engine Features Needed:
        - [ ] CardInstance.get_object_identities() -> Set[str] (Rule 1.2.2)
        """
        identities = ["object", "card", self.name]
        return identities

    def matches_name(self, query: str) -> bool:
        """
        Rule 2.7.5: Exact case-insensitive whole word match required.

        Engine Features Needed:
        - [ ] NameMatcher.matches(candidate, query) with whole-word, case-insensitive (Rule 2.7.5)
        """
        card_words = self.name.lower().split()
        query_words = query.lower().split()
        # Check if query_words appear as a contiguous whole-word sub-sequence
        if len(query_words) > len(card_words):
            return False
        for i in range(len(card_words) - len(query_words) + 1):
            if card_words[i : i + len(query_words)] == query_words:
                return True
        return False

    def is_distinct_from(self, other: "NameCardStub") -> bool:
        """
        Rule 2.7.1 / cross-ref 1.3.4: Uniqueness determined by name + pitch.
        Two cards are distinct if they have different names or different pitch values.

        Engine Features Needed:
        - [ ] CardTemplate.is_distinct_from(other): name+pitch based (Rule 2.7.1, 1.3.4)
        """
        if self.name != other.name:
            return True
        if self.pitch_value != other.pitch_value:
            return True
        return False


@dataclass
class PersonalNameParserStub:
    """
    Stub for parsing personal names to extract monikers.

    Models the name parsing logic that the engine must implement.

    Engine Features Needed:
    - [ ] PersonalNameParser.extract_moniker(name) -> str | None (Rule 2.7.3)
    - [ ] PersonalNameParser.is_personal_name(name) -> bool (Rule 2.7.3)
    """

    # Known personal name patterns from the rulebook examples
    KNOWN_PERSONAL_NAMES = {
        "Bravo": "Bravo",
        "Dorinthea Ironsong": "Dorinthea",
        "Data Doll MKII": "Data Doll",
        "Ser Boltyn, Breaker of Dawn": "Boltyn",
        "Blasmophet, the Soul Harvester": "Blasmophet",
        "The Librarian": "The Librarian",
        "Dawnblade": "Dawnblade",
        "Stalagmite, Bastion of Isenloft": "Stalagmite",
        "Bravo, Showstopper": "Bravo",
        "Bravo, Star of the Show": "Bravo",
        "Dawnblade, Resplendent": "Dawnblade",
    }

    def is_personal_name(self, name: str) -> bool:
        """
        Rule 2.7.3: Determine if a name is a personal name.

        Engine Features Needed:
        - [ ] PersonalNameParser.is_personal_name(name) -> bool (Rule 2.7.3)
        """
        return name in self.KNOWN_PERSONAL_NAMES

    def extract_moniker(self, name: str) -> Optional[str]:
        """
        Rule 2.7.3: Extract the moniker from a personal name.
        Rule 2.7.3a: Non-personal names return None.

        Engine Features Needed:
        - [ ] PersonalNameParser.extract_moniker(name) -> str | None (Rule 2.7.3)
        """
        return self.KNOWN_PERSONAL_NAMES.get(name, None)


def search_cards_by_name(cards: List[NameCardStub], query: str) -> List[NameCardStub]:
    """
    Rule 2.7.5: Search cards by name using whole-word, case-insensitive match.

    Engine Features Needed:
    - [ ] NameMatcher: a full name search system using whole-word match (Rule 2.7.5)
    """
    return [card for card in cards if card.matches_name(query)]


def find_by_moniker(cards: List[NameCardStub], moniker: str) -> List[NameCardStub]:
    """
    Rule 2.7.3b: Effect using a moniker may refer to multiple cards with that moniker.

    Engine Features Needed:
    - [ ] NameMatcher.matches_by_moniker(cards, moniker) -> List (Rule 2.7.3b)
    """
    return [card for card in cards if card.moniker == moniker]


# ---------------------------------------------------------------------------
# Scenario: Name is a property of a card object
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_7_name.feature",
    "Name is a property of a card object",
)
def test_name_is_property_of_card():
    """Rule 2.7.1: Name is a property of an object."""
    pass


@given('a card named "Pummel" is created', target_fixture="pummel_card")
def given_pummel_card_created():
    """Rule 2.7.2: Printed name defines the name of a card."""
    return NameCardStub(name="Pummel")


@when(
    "the engine checks the name property of the Pummel card",
    target_fixture="pummel_name_check",
)
def when_engine_checks_name_property_of_pummel(pummel_card):
    """Rule 2.7.1: Check that name is a property."""
    return {
        "has_name_property": pummel_card.has_name_property,
        "name": pummel_card.name,
        "identities": pummel_card.get_object_identities(),
    }


@then("the Pummel card should have the name property")
def then_pummel_has_name_property(pummel_name_check):
    """Rule 2.7.1: Name is a property of an object."""
    assert pummel_name_check["has_name_property"] is True


@then('the name of the Pummel card should be "Pummel"')
def then_pummel_name_is_pummel(pummel_name_check):
    """Rule 2.7.2: Printed name defines the name."""
    assert pummel_name_check["name"] == "Pummel"


@then("the name should be one of the card's object identities")
def then_name_is_object_identity(pummel_name_check):
    """Rule 2.7.1: Name represents one of its object identities."""
    assert "Pummel" in pummel_name_check["identities"]


# ---------------------------------------------------------------------------
# Scenario: Name determines card uniqueness along with pitch value
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_7_name.feature",
    "Name determines card uniqueness along with pitch value",
)
def test_name_determines_uniqueness_with_pitch():
    """Rule 2.7.1: Name + pitch determine uniqueness."""
    pass


@given(
    "a Sink Below card with pitch value 1 is created", target_fixture="sink_below_red"
)
def given_sink_below_pitch_1():
    """Rule 2.7.1: Card with specific pitch value."""
    return NameCardStub(name="Sink Below", pitch_value=1)


@given(
    "a Sink Below card with pitch value 2 is created",
    target_fixture="sink_below_yellow",
)
def given_sink_below_pitch_2():
    """Rule 2.7.1: Card with different pitch value but same name."""
    return NameCardStub(name="Sink Below", pitch_value=2)


@when(
    "the engine checks the uniqueness of the two Sink Below cards",
    target_fixture="sink_below_uniqueness",
)
def when_engine_checks_sink_below_uniqueness(sink_below_red, sink_below_yellow):
    """Rule 2.7.1: Check distinctness based on name + pitch."""
    return {
        "are_distinct": sink_below_red.is_distinct_from(sink_below_yellow),
    }


@then(
    "the two Sink Below cards should be distinct because they have different pitch values"
)
def then_sink_below_cards_are_distinct(sink_below_uniqueness):
    """Rule 2.7.1: Same name but different pitch = distinct."""
    assert sink_below_uniqueness["are_distinct"] is True


# ---------------------------------------------------------------------------
# Scenario: Cards with same name and pitch are not distinct
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_7_name.feature",
    "Cards with same name and pitch are not distinct",
)
def test_same_name_and_pitch_not_distinct():
    """Rule 2.7.1: Same name and pitch = not distinct."""
    pass


@given(
    "a Pummel card with pitch value 1 is created as card A",
    target_fixture="pummel_card_a",
)
def given_pummel_card_a():
    """Rule 2.7.1: Pummel card A with pitch 1."""
    return NameCardStub(name="Pummel", pitch_value=1)


@given(
    "a Pummel card with pitch value 1 is created as card B",
    target_fixture="pummel_card_b",
)
def given_pummel_card_b():
    """Rule 2.7.1: Pummel card B with pitch 1 (identical to card A)."""
    return NameCardStub(name="Pummel", pitch_value=1)


@when(
    "the engine checks the uniqueness of the two Pummel cards",
    target_fixture="pummel_uniqueness",
)
def when_engine_checks_pummel_uniqueness(pummel_card_a, pummel_card_b):
    """Rule 2.7.1: Check that cards with same name+pitch are NOT distinct."""
    return {
        "are_distinct": pummel_card_a.is_distinct_from(pummel_card_b),
    }


@then(
    "the two Pummel cards should not be distinct because they have the same name and pitch"
)
def then_pummel_cards_not_distinct(pummel_uniqueness):
    """Rule 2.7.1: Same name and pitch = NOT distinct."""
    assert pummel_uniqueness["are_distinct"] is False


# ---------------------------------------------------------------------------
# Scenario: Printed name defines the card name
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_7_name.feature",
    "Printed name defines the card name",
)
def test_printed_name_defines_card_name():
    """Rule 2.7.2: Printed name defines the name of a card."""
    pass


@given(
    'a card with the printed name "Lunging Press" is created',
    target_fixture="lunging_press_card",
)
def given_lunging_press_card():
    """Rule 2.7.2: Printed name defines name."""
    return NameCardStub(name="Lunging Press")


@when(
    "the engine retrieves the name of the Lunging Press card",
    target_fixture="lunging_press_name",
)
def when_engine_retrieves_lunging_press_name(lunging_press_card):
    """Rule 2.7.2: Retrieve the name from the card."""
    return {
        "name": lunging_press_card.name,
        "has_name_property": lunging_press_card.has_name_property,
    }


@then('the name of the Lunging Press card should be "Lunging Press"')
def then_lunging_press_name_is_correct(lunging_press_name):
    """Rule 2.7.2: Name matches the printed name."""
    assert lunging_press_name["name"] == "Lunging Press"


@then("the name should match the printed name exactly")
def then_lunging_press_name_exact_match(lunging_press_name):
    """Rule 2.7.2: Printed name defines the card name."""
    assert lunging_press_name["has_name_property"] is True


# ---------------------------------------------------------------------------
# Scenario: A personal name determines a moniker
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_7_name.feature",
    "A personal name determines a moniker",
)
def test_personal_name_determines_moniker():
    """Rule 2.7.3: Personal name determines the moniker."""
    pass


@given("a Bravo hero card with personal name is created", target_fixture="bravo_hero")
def given_bravo_hero_card():
    """Rule 2.7.3: Bravo is a personal name with moniker Bravo."""
    parser = PersonalNameParserStub()
    moniker = parser.extract_moniker("Bravo")
    return NameCardStub(name="Bravo", is_personal_name=True, _moniker=moniker)


@when(
    "the engine checks the moniker of the Bravo hero",
    target_fixture="bravo_moniker_check",
)
def when_engine_checks_bravo_moniker(bravo_hero):
    """Rule 2.7.3: Check the moniker of the Bravo card."""
    return {
        "moniker": bravo_hero.moniker,
        "has_moniker": bravo_hero.has_moniker,
    }


@then('the moniker of the Bravo hero should be "Bravo"')
def then_bravo_moniker_is_bravo(bravo_moniker_check):
    """Rule 2.7.3: Bravo's moniker is Bravo."""
    assert bravo_moniker_check["moniker"] == "Bravo"


# ---------------------------------------------------------------------------
# Scenario: Dorinthea Ironsong has moniker Dorinthea
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_7_name.feature",
    "Dorinthea Ironsong has moniker Dorinthea",
)
def test_dorinthea_ironsong_moniker():
    """Rule 2.7.3: Dorinthea Ironsong has moniker Dorinthea."""
    pass


@given(
    'a hero card with the personal name "Dorinthea Ironsong" is created',
    target_fixture="dorinthea_hero",
)
def given_dorinthea_ironsong_card():
    """Rule 2.7.3: Dorinthea Ironsong personal name."""
    parser = PersonalNameParserStub()
    moniker = parser.extract_moniker("Dorinthea Ironsong")
    return NameCardStub(
        name="Dorinthea Ironsong", is_personal_name=True, _moniker=moniker
    )


@when(
    "the engine checks the moniker of the Dorinthea Ironsong hero",
    target_fixture="dorinthea_moniker_check",
)
def when_engine_checks_dorinthea_moniker(dorinthea_hero):
    """Rule 2.7.3: Extract moniker from Dorinthea Ironsong."""
    return {
        "moniker": dorinthea_hero.moniker,
        "has_moniker": dorinthea_hero.has_moniker,
    }


@then('the moniker of the Dorinthea Ironsong hero should be "Dorinthea"')
def then_dorinthea_moniker_is_dorinthea(dorinthea_moniker_check):
    """Rule 2.7.3: Dorinthea Ironsong's moniker is Dorinthea."""
    assert dorinthea_moniker_check["moniker"] == "Dorinthea"


# ---------------------------------------------------------------------------
# Scenario: Name with honorific and suffix extracts the correct moniker
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_7_name.feature",
    "Name with honorific and suffix extracts the correct moniker",
)
def test_honorific_and_suffix_moniker():
    """Rule 2.7.3: Honorific and suffix don't affect moniker extraction."""
    pass


@given(
    'a hero card with the personal name "Ser Boltyn, Breaker of Dawn" is created',
    target_fixture="ser_boltyn_hero",
)
def given_ser_boltyn_card():
    """Rule 2.7.3: Ser Boltyn, Breaker of Dawn - honorific 'Ser', suffix 'Breaker of Dawn'."""
    parser = PersonalNameParserStub()
    moniker = parser.extract_moniker("Ser Boltyn, Breaker of Dawn")
    return NameCardStub(
        name="Ser Boltyn, Breaker of Dawn", is_personal_name=True, _moniker=moniker
    )


@when(
    "the engine checks the moniker of the Ser Boltyn hero",
    target_fixture="ser_boltyn_moniker_check",
)
def when_engine_checks_ser_boltyn_moniker(ser_boltyn_hero):
    """Rule 2.7.3: Extract moniker from Ser Boltyn, Breaker of Dawn."""
    return {
        "moniker": ser_boltyn_hero.moniker,
        "has_moniker": ser_boltyn_hero.has_moniker,
    }


@then('the moniker of the Ser Boltyn hero should be "Boltyn"')
def then_ser_boltyn_moniker_is_boltyn(ser_boltyn_moniker_check):
    """Rule 2.7.3: Ser Boltyn, Breaker of Dawn's moniker is Boltyn."""
    assert ser_boltyn_moniker_check["moniker"] == "Boltyn"


# ---------------------------------------------------------------------------
# Scenario: The Librarian has moniker The Librarian
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_7_name.feature",
    "The Librarian has moniker The Librarian",
)
def test_the_librarian_moniker():
    """Rule 2.7.3: The Librarian has moniker 'The Librarian'."""
    pass


@given(
    'a hero card with the personal name "The Librarian" is created',
    target_fixture="librarian_hero",
)
def given_the_librarian_card():
    """Rule 2.7.3: The Librarian - multi-word personal name."""
    parser = PersonalNameParserStub()
    moniker = parser.extract_moniker("The Librarian")
    return NameCardStub(name="The Librarian", is_personal_name=True, _moniker=moniker)


@when(
    "the engine checks the moniker of The Librarian hero",
    target_fixture="librarian_moniker_check",
)
def when_engine_checks_librarian_moniker(librarian_hero):
    """Rule 2.7.3: Extract moniker from The Librarian."""
    return {
        "moniker": librarian_hero.moniker,
        "has_moniker": librarian_hero.has_moniker,
    }


@then('the moniker of The Librarian hero should be "The Librarian"')
def then_librarian_moniker_is_the_librarian(librarian_moniker_check):
    """Rule 2.7.3: The Librarian's moniker is The Librarian."""
    assert librarian_moniker_check["moniker"] == "The Librarian"


# ---------------------------------------------------------------------------
# Scenario: A non-personal name has no moniker
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_7_name.feature",
    "A non-personal name has no moniker",
)
def test_non_personal_name_has_no_moniker():
    """Rule 2.7.3a: Non-personal names have no moniker."""
    pass


@given(
    'a card named "Pummel" that is not a personal name is created',
    target_fixture="pummel_non_personal",
)
def given_pummel_non_personal_name():
    """Rule 2.7.3a: Pummel is not a personal name."""
    return NameCardStub(name="Pummel", is_personal_name=False, _moniker=None)


@when(
    "the engine checks the moniker of the Pummel card",
    target_fixture="pummel_moniker_check",
)
def when_engine_checks_pummel_moniker(pummel_non_personal):
    """Rule 2.7.3a: Check that non-personal name has no moniker."""
    return {
        "moniker": pummel_non_personal.moniker,
        "has_moniker": pummel_non_personal.has_moniker,
    }


@then("the Pummel card should have no moniker")
def then_pummel_has_no_moniker(pummel_moniker_check):
    """Rule 2.7.3a: Non-personal names have no moniker."""
    assert pummel_moniker_check["moniker"] is None
    assert pummel_moniker_check["has_moniker"] is False


# ---------------------------------------------------------------------------
# Scenario: A non-hero action card has no moniker
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_7_name.feature",
    "A non-hero action card has no moniker",
)
def test_action_card_has_no_moniker():
    """Rule 2.7.3a: Action cards are not personal names."""
    pass


@given(
    'a card named "Lunging Press" is created as an action card',
    target_fixture="lunging_press_action",
)
def given_lunging_press_action_card():
    """Rule 2.7.3a: Lunging Press is an action card, not a personal name."""
    return NameCardStub(name="Lunging Press", is_personal_name=False, _moniker=None)


@when(
    "the engine checks the moniker of the Lunging Press action card",
    target_fixture="lunging_press_moniker_check",
)
def when_engine_checks_lunging_press_moniker(lunging_press_action):
    """Rule 2.7.3a: Check that action card has no moniker."""
    return {
        "moniker": lunging_press_action.moniker,
        "has_moniker": lunging_press_action.has_moniker,
    }


@then("the Lunging Press action card should have no moniker")
def then_lunging_press_has_no_moniker(lunging_press_moniker_check):
    """Rule 2.7.3a: Action cards have no moniker."""
    assert lunging_press_moniker_check["moniker"] is None
    assert lunging_press_moniker_check["has_moniker"] is False


# ---------------------------------------------------------------------------
# Scenario: Bravo Showstopper has the same moniker as Bravo
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_7_name.feature",
    "Bravo Showstopper has the same moniker as Bravo",
)
def test_bravo_showstopper_same_moniker():
    """Rule 2.7.3b: Different names may have the same moniker."""
    pass


@given(
    "a Bravo hero card is created for moniker comparison",
    target_fixture="bravo_original",
)
def given_bravo_original_hero():
    """Rule 2.7.3b: Original Bravo card."""
    parser = PersonalNameParserStub()
    moniker = parser.extract_moniker("Bravo")
    return NameCardStub(name="Bravo", is_personal_name=True, _moniker=moniker)


@given(
    "a Bravo Showstopper hero card is created for moniker comparison",
    target_fixture="bravo_showstopper",
)
def given_bravo_showstopper_hero():
    """Rule 2.7.3b: Bravo, Showstopper - different name, same moniker."""
    parser = PersonalNameParserStub()
    moniker = parser.extract_moniker("Bravo, Showstopper")
    return NameCardStub(
        name="Bravo, Showstopper", is_personal_name=True, _moniker=moniker
    )


@when(
    "the engine checks the monikers of both Bravo cards",
    target_fixture="bravo_moniker_comparison",
)
def when_engine_checks_both_bravo_monikers(bravo_original, bravo_showstopper):
    """Rule 2.7.3b: Compare monikers of two different Bravo cards."""
    return {
        "bravo_moniker": bravo_original.moniker,
        "showstopper_moniker": bravo_showstopper.moniker,
        "same_moniker": bravo_original.moniker == bravo_showstopper.moniker,
        "different_names": bravo_original.name != bravo_showstopper.name,
    }


@then('both Bravo cards should have the moniker "Bravo"')
def then_both_bravo_have_same_moniker(bravo_moniker_comparison):
    """Rule 2.7.3b: Different names but same moniker."""
    assert bravo_moniker_comparison["bravo_moniker"] == "Bravo"
    assert bravo_moniker_comparison["showstopper_moniker"] == "Bravo"
    assert bravo_moniker_comparison["same_moniker"] is True


@then("the two Bravo cards should have different names")
def then_bravo_cards_have_different_names(bravo_moniker_comparison):
    """Rule 2.7.3b: Despite same moniker, they have different names."""
    assert bravo_moniker_comparison["different_names"] is True


# ---------------------------------------------------------------------------
# Scenario: Effect using a moniker matches all cards with that moniker
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_7_name.feature",
    "Effect using a moniker matches all cards with that moniker",
)
def test_effect_moniker_matches_multiple_cards():
    """Rule 2.7.3b: Effect using moniker matches all cards with that moniker."""
    pass


@given(
    'Bravo card 1 with personal name "Bravo" is created for moniker effect test',
    target_fixture="bravo_card_1",
)
def given_bravo_card_1():
    """Rule 2.7.3b: First Bravo card."""
    parser = PersonalNameParserStub()
    return NameCardStub(
        name="Bravo", is_personal_name=True, _moniker=parser.extract_moniker("Bravo")
    )


@given(
    'Bravo card 2 with personal name "Bravo, Showstopper" is created for moniker effect test',
    target_fixture="bravo_card_2",
)
def given_bravo_card_2():
    """Rule 2.7.3b: Second Bravo card (Showstopper)."""
    parser = PersonalNameParserStub()
    return NameCardStub(
        name="Bravo, Showstopper",
        is_personal_name=True,
        _moniker=parser.extract_moniker("Bravo, Showstopper"),
    )


@given(
    'Bravo card 3 with personal name "Bravo, Star of the Show" is created for moniker effect test',
    target_fixture="bravo_card_3",
)
def given_bravo_card_3():
    """Rule 2.7.3b: Third Bravo card (Star of the Show)."""
    parser = PersonalNameParserStub()
    return NameCardStub(
        name="Bravo, Star of the Show",
        is_personal_name=True,
        _moniker=parser.extract_moniker("Bravo, Star of the Show"),
    )


@when(
    'an effect refers to objects by the moniker "Bravo"',
    target_fixture="bravo_moniker_effect_result",
)
def when_effect_refers_by_bravo_moniker(bravo_card_1, bravo_card_2, bravo_card_3):
    """Rule 2.7.3b: Effect uses moniker to match objects."""
    all_cards = [bravo_card_1, bravo_card_2, bravo_card_3]
    matched = find_by_moniker(all_cards, "Bravo")
    return {
        "matched_cards": matched,
        "match_count": len(matched),
    }


@then("all three Bravo-moniker cards should be matched by the effect")
def then_all_three_bravo_cards_matched(bravo_moniker_effect_result):
    """Rule 2.7.3b: All three cards have moniker 'Bravo' and should be matched."""
    assert bravo_moniker_effect_result["match_count"] == 3


@then("the effect should match 3 objects")
def then_effect_matches_3_objects(bravo_moniker_effect_result):
    """Rule 2.7.3b: Three objects with moniker Bravo are matched."""
    assert bravo_moniker_effect_result["match_count"] == 3


# ---------------------------------------------------------------------------
# Scenario: Effect naming Dawnblade does not match Dawnblade Resplendent
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_7_name.feature",
    "Effect naming Dawnblade does not match Dawnblade Resplendent",
)
def test_dawnblade_name_vs_moniker():
    """Rule 2.7.3c: Moniker is not a name; name-based effect doesn't use moniker."""
    pass


@given(
    'a card named "Dawnblade" with moniker "Dawnblade" is created',
    target_fixture="dawnblade_card",
)
def given_dawnblade_card():
    """Rule 2.7.3c: Dawnblade card with its moniker."""
    return NameCardStub(name="Dawnblade", is_personal_name=True, _moniker="Dawnblade")


@given(
    'a card named "Dawnblade, Resplendent" with moniker "Dawnblade" is created',
    target_fixture="dawnblade_resplendent_card",
)
def given_dawnblade_resplendent_card():
    """Rule 2.7.3c: Dawnblade, Resplendent has same moniker but different name."""
    return NameCardStub(
        name="Dawnblade, Resplendent", is_personal_name=True, _moniker="Dawnblade"
    )


@when(
    'an effect identifies an object by the name "Dawnblade"',
    target_fixture="dawnblade_name_effect_result",
)
def when_effect_identifies_by_name_dawnblade(
    dawnblade_card, dawnblade_resplendent_card
):
    """Rule 2.7.3c: Name-based identification does NOT use monikers."""
    all_cards = [dawnblade_card, dawnblade_resplendent_card]
    # Name match: exact case-insensitive full name
    name_matched = [c for c in all_cards if c.name.lower() == "dawnblade"]
    return {
        "name_matched_names": [c.name for c in name_matched],
    }


@then('the effect should match the card named "Dawnblade"')
def then_dawnblade_name_matches_dawnblade(dawnblade_name_effect_result):
    """Rule 2.7.3c: Effect identifies the card named 'Dawnblade'."""
    assert "Dawnblade" in dawnblade_name_effect_result["name_matched_names"]


@then('the effect should not match the card named "Dawnblade, Resplendent"')
def then_dawnblade_name_does_not_match_resplendent(dawnblade_name_effect_result):
    """Rule 2.7.3c: Moniker match doesn't count as name match."""
    assert (
        "Dawnblade, Resplendent"
        not in dawnblade_name_effect_result["name_matched_names"]
    )


# ---------------------------------------------------------------------------
# Scenario: A moniker is not considered a name for identification purposes
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_7_name.feature",
    "A moniker is not considered a name for identification purposes",
)
def test_moniker_not_considered_name():
    """Rule 2.7.3c: Moniker is not considered a name."""
    pass


@given(
    'a card named "Bravo" with moniker "Bravo" is created',
    target_fixture="bravo_name_card",
)
def given_bravo_name_card():
    """Rule 2.7.3c: Bravo card with matching name and moniker."""
    return NameCardStub(name="Bravo", is_personal_name=True, _moniker="Bravo")


@given(
    'a card named "Bravo, Showstopper" with moniker "Bravo" is created',
    target_fixture="bravo_showstopper_name_card",
)
def given_bravo_showstopper_name_card():
    """Rule 2.7.3c: Bravo, Showstopper has moniker Bravo but different name."""
    return NameCardStub(
        name="Bravo, Showstopper", is_personal_name=True, _moniker="Bravo"
    )


@when(
    'an effect identifies an object by the name "Bravo"',
    target_fixture="bravo_name_effect_result",
)
def when_effect_identifies_by_name_bravo(bravo_name_card, bravo_showstopper_name_card):
    """Rule 2.7.3c: Name-based identification is exact name match."""
    all_cards = [bravo_name_card, bravo_showstopper_name_card]
    name_matched = [c for c in all_cards if c.name.lower() == "bravo"]
    return {
        "name_matched_names": [c.name for c in name_matched],
    }


@then('the name-based identification should match only the card named "Bravo"')
def then_name_matches_only_bravo(bravo_name_effect_result):
    """Rule 2.7.3c: Name match is exact, finds only 'Bravo'."""
    assert "Bravo" in bravo_name_effect_result["name_matched_names"]
    assert len(bravo_name_effect_result["name_matched_names"]) == 1


@then('the name-based identification should not match "Bravo, Showstopper"')
def then_name_does_not_match_showstopper(bravo_name_effect_result):
    """Rule 2.7.3c: Moniker match is not a name match."""
    assert "Bravo, Showstopper" not in bravo_name_effect_result["name_matched_names"]


# ---------------------------------------------------------------------------
# Scenario: Printed name always considered English version
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_7_name.feature",
    "Printed name always considered English version",
)
def test_printed_name_always_english():
    """Rule 2.7.4: Printed name is always English regardless of card language."""
    pass


@given(
    'a card with the English name "Pummel" has a Japanese printed card',
    target_fixture="japanese_pummel_card",
)
def given_japanese_pummel_card():
    """Rule 2.7.4: The physical card is Japanese but canonical name is English."""
    return NameCardStub(name="Pummel", _language_version="japanese")


@when(
    "the engine determines the name of the Japanese Pummel card",
    target_fixture="japanese_pummel_name_check",
)
def when_engine_determines_japanese_pummel_name(japanese_pummel_card):
    """Rule 2.7.4: The engine uses the English canonical name."""
    return {
        "name": japanese_pummel_card.name,
        "language_version": japanese_pummel_card._language_version,
    }


@then('the name of the Japanese Pummel card should be "Pummel"')
def then_japanese_pummel_name_is_pummel(japanese_pummel_name_check):
    """Rule 2.7.4: English name regardless of physical card language."""
    assert japanese_pummel_name_check["name"] == "Pummel"


@then("the name should be the English version regardless of the printed language")
def then_name_is_english_version(japanese_pummel_name_check):
    """Rule 2.7.4: Name is English even for non-English printed cards."""
    assert japanese_pummel_name_check["name"] == "Pummel"


# ---------------------------------------------------------------------------
# Scenario: Name matching is case-insensitive but requires whole word match
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_7_name.feature",
    "Name matching is case-insensitive but requires whole word match",
)
def test_name_matching_whole_word_case_insensitive():
    """Rule 2.7.5: Case-insensitive, whole-word name matching."""
    pass


@given(
    '"Blazing Aether" and "Trailblazing Aether" cards are in the game for whole word test',
    target_fixture="cards_for_whole_word_test",
)
def given_blazing_and_trailblazing_for_whole_word_test():
    """Rule 2.7.5: Blazing Aether and Trailblazing Aether in the game."""
    return {
        "blazing": NameCardStub(name="Blazing Aether"),
        "trailblazing": NameCardStub(name="Trailblazing Aether"),
    }


@when(
    'an effect searches for cards matching the name "Blazing Aether"',
    target_fixture="blazing_search_result",
)
def when_effect_searches_blazing_aether(cards_for_whole_word_test):
    """Rule 2.7.5: Name search with whole-word matching."""
    all_cards = list(cards_for_whole_word_test.values())
    matched = search_cards_by_name(all_cards, "Blazing Aether")
    return {
        "matched_names": [c.name for c in matched],
    }


@then('the search should find the card named "Blazing Aether"')
def then_search_finds_blazing_aether(blazing_search_result):
    """Rule 2.7.5: Exact whole-word match found."""
    assert "Blazing Aether" in blazing_search_result["matched_names"]


@then('the search should not find the card named "Trailblazing Aether"')
def then_search_does_not_find_trailblazing(blazing_search_result):
    """Rule 2.7.5: 'Blazing' in 'Trailblazing' is not a whole-word match."""
    assert "Trailblazing Aether" not in blazing_search_result["matched_names"]


# ---------------------------------------------------------------------------
# Scenario: Name matching is case-insensitive
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_7_name.feature",
    "Name matching is case-insensitive",
)
def test_name_matching_case_insensitive():
    """Rule 2.7.5: Case-insensitive matching."""
    pass


@given(
    'a "Blazing Aether" card is in the game for case test',
    target_fixture="blazing_aether_for_case_test",
)
def given_blazing_aether_for_case_test():
    """Rule 2.7.5: Blazing Aether for case-insensitivity test."""
    return NameCardStub(name="Blazing Aether")


@when(
    'an effect searches for cards matching the name "blazing aether"',
    target_fixture="lowercase_search_result",
)
def when_effect_searches_lowercase_blazing(blazing_aether_for_case_test):
    """Rule 2.7.5: Lowercase query should match mixed-case card name."""
    all_cards = [blazing_aether_for_case_test]
    matched = search_cards_by_name(all_cards, "blazing aether")
    return {
        "matched_names": [c.name for c in matched],
    }


@then(
    'the search should find the card named "Blazing Aether" using case-insensitive match'
)
def then_lowercase_search_finds_blazing_aether(lowercase_search_result):
    """Rule 2.7.5: Case-insensitive match finds 'Blazing Aether'."""
    assert "Blazing Aether" in lowercase_search_result["matched_names"]


# ---------------------------------------------------------------------------
# Scenario: Proto does not match Protos in name matching
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_7_name.feature",
    "Proto does not match Protos in name matching",
)
def test_proto_does_not_match_protos():
    """Rule 2.7.5: 'Proto' does not match 'Protos' - whole word match required."""
    pass


@given(
    'a "Breaker Helm Protos" card is in the game for proto test',
    target_fixture="breaker_helm_protos_card",
)
def given_breaker_helm_protos_in_game():
    """Rule 2.7.5: Breaker Helm Protos - 'Protos' is not a match for 'Proto'."""
    return NameCardStub(name="Breaker Helm Protos")


@when(
    'an effect searches for cards with "Proto" in their name',
    target_fixture="proto_search_result",
)
def when_effect_searches_proto(breaker_helm_protos_card):
    """Rule 2.7.5: Search for 'Proto' requires whole word match."""
    all_cards = [breaker_helm_protos_card]
    matched = search_cards_by_name(all_cards, "Proto")
    return {
        "matched_names": [c.name for c in matched],
    }


@then('the search should not find the card named "Breaker Helm Protos"')
def then_proto_search_does_not_find_protos(proto_search_result):
    """Rule 2.7.5: 'Protos' is not a whole-word match for 'Proto'."""
    assert "Breaker Helm Protos" not in proto_search_result["matched_names"]


@then(
    'the non-match reason should be that "Protos" is not a whole word match for "Proto"'
)
def then_protos_not_whole_word_match_for_proto(proto_search_result):
    """Rule 2.7.5: 'Protos' != 'Proto' (not the same word)."""
    assert len(proto_search_result["matched_names"]) == 0


# ---------------------------------------------------------------------------
# Scenario: Full word match finds the correct cards
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_7_name.feature",
    "Full word match finds the correct cards",
)
def test_full_word_match_finds_correct_cards():
    """Rule 2.7.5: Exact word 'Proto' matches 'Proto Helm'."""
    pass


@given(
    'a "Proto Helm" card is in the game for exact match test',
    target_fixture="proto_helm_card",
)
def given_proto_helm_in_game():
    """Rule 2.7.5: Proto Helm - 'Proto' is an exact whole word match."""
    return NameCardStub(name="Proto Helm")


@when(
    'an effect searches for cards with "Proto" in their name for exact test',
    target_fixture="proto_helm_search_result",
)
def when_effect_searches_proto_in_proto_helm(proto_helm_card):
    """Rule 2.7.5: 'Proto' is a whole word in 'Proto Helm'."""
    all_cards = [proto_helm_card]
    matched = search_cards_by_name(all_cards, "Proto")
    return {
        "matched_names": [c.name for c in matched],
    }


@then('the search should find the card named "Proto Helm"')
def then_proto_search_finds_proto_helm(proto_helm_search_result):
    """Rule 2.7.5: 'Proto' is a whole word in 'Proto Helm'."""
    assert "Proto Helm" in proto_helm_search_result["matched_names"]


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def game_state():
    """
    Fixture providing game state for testing.

    Uses BDDGameState which integrates with the real engine.
    Reference: Rule 2.7
    """
    from tests.bdd_helpers import BDDGameState

    return BDDGameState()
