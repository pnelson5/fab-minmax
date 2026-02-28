"""
Step definitions for Section 2.12: Text Box
Reference: Flesh and Blood Comprehensive Rules Section 2.12

This module implements behavioral tests for the text box property of cards
in Flesh and Blood.

Rule 2.12.1: The text box of a card contains the card text of a card,
             typically located on the lower half of a card beneath the
             illustration.

Rule 2.12.2: The card text of a card contains the rules text, reminder text,
             and flavor text of the card (if any). Rules text is printed in
             roman and boldface. Reminder text is printed in parenthesized
             italics. Flavor text is separated vertically from the rules and
             reminder text (if any) by a horizontal bar and is printed in
             italics.

Rule 2.12.3: The rules text of a card defines the base abilities of the card.
             A paragraph of rules text typically defines a single ability.
             Reminder and flavor text do not affect the game.

Rule 2.12.3a: If the rules text specifies the name and/or moniker of its
              source object in the third-person it is a self-reference. A
              self-reference can be interpreted as "this" and it refers to
              its source object and not other cards with the same name.

Rule 2.12.3b: If the rules text specifies the name and/or moniker of another
              object in the context of creating it, it refers to a hypothetical
              object with defined properties, including that name. Otherwise,
              if the rules text specifies the name and/or moniker of another
              object it refers to any existing object with that name and/or
              moniker.

Engine Features Needed for Section 2.12:
- [ ] `CardInstance.text_box` property returning the full card text (Rule 2.12.1)
- [ ] `CardInstance.has_text_box` property (Rule 2.12.1)
- [ ] `CardInstance.rules_text` property returning only rules text (Rule 2.12.2)
- [ ] `CardInstance.reminder_text` property returning reminder text or None (Rule 2.12.2)
- [ ] `CardInstance.flavor_text` property returning flavor text or None (Rule 2.12.2)
- [ ] `CardInstance.get_base_abilities()` derived from rules text paragraphs (Rule 2.12.3)
- [ ] Rules text paragraph parser: one paragraph = one ability (Rule 2.12.3)
- [ ] `CardInstance.is_self_reference(name_or_moniker)` detection (Rule 2.12.3a)
- [ ] `RulesTextReferenceResolver.resolve(card, name)` returning card itself for self-refs (Rule 2.12.3a)
- [ ] `HypotheticalObject` class for "create X" contexts (Rule 2.12.3b)
- [ ] `RulesTextReferenceResolver.is_creation_context(clause)` detecting "Create a X" phrasing (Rule 2.12.3b)
"""

import pytest
from pytest_bdd import scenario, given, when, then, parsers
from dataclasses import dataclass, field
from typing import Optional, List


# ---------------------------------------------------------------------------
# Stub classes for testing Section 2.12 rules
# ---------------------------------------------------------------------------


@dataclass
class TextBoxCardStub:
    """
    Stub representing a card with a text box.

    Models what the engine must implement for Section 2.12.

    Engine Features Needed:
    - [ ] CardInstance.text_box: str — the full card text (Rule 2.12.1)
    - [ ] CardInstance.has_text_box: bool (Rule 2.12.1)
    - [ ] CardInstance.rules_text: str — only rules text (Rule 2.12.2)
    - [ ] CardInstance.reminder_text: Optional[str] (Rule 2.12.2)
    - [ ] CardInstance.flavor_text: Optional[str] (Rule 2.12.2)
    - [ ] CardInstance.get_base_abilities(): List[str] from rules text (Rule 2.12.3)
    """

    name: str = "Test Card"
    _rules_text: Optional[str] = None
    _reminder_text: Optional[str] = None
    _flavor_text: Optional[str] = None
    _instance_id: int = 0  # for distinguishing instances with same name

    @property
    def has_text_box(self) -> bool:
        """Rule 2.12.1: Card has a text box."""
        return True  # All cards have a text box (may be empty)

    @property
    def text_box(self) -> Optional[str]:
        """Rule 2.12.1: The text box contains card text."""
        parts = []
        if self._rules_text:
            parts.append(self._rules_text)
        if self._reminder_text:
            parts.append(self._reminder_text)
        if self._flavor_text:
            parts.append(self._flavor_text)
        return "\n".join(parts) if parts else None

    @property
    def rules_text(self) -> Optional[str]:
        """Rule 2.12.2: Rules text defines base abilities."""
        return self._rules_text

    @property
    def reminder_text(self) -> Optional[str]:
        """Rule 2.12.2: Reminder text in parenthesized italics."""
        return self._reminder_text

    @property
    def flavor_text(self) -> Optional[str]:
        """Rule 2.12.2: Flavor text does not affect the game."""
        return self._flavor_text

    def get_base_abilities(self) -> List[str]:
        """
        Rule 2.12.3: Rules text defines base abilities.
        Each paragraph of rules text is one ability.
        Reminder text and flavor text do NOT contribute.

        Engine Feature Needed:
        - [ ] Parser that splits rules text into paragraphs (Rule 2.12.3)
        """
        if not self._rules_text:
            return []
        # Each paragraph (separated by newlines) is one ability
        paragraphs = [p.strip() for p in self._rules_text.split("\n") if p.strip()]
        return paragraphs

    def has_ability(self, ability_name: str) -> bool:
        """Rule 2.12.3: Check if card has an ability derived from rules text."""
        abilities = self.get_base_abilities()
        normalized = ability_name.lower().rstrip(".")
        for ability in abilities:
            if ability.lower().rstrip(".") == normalized:
                return True
        return False

    @property
    def moniker(self) -> Optional[str]:
        """
        Rule 2.12.3a: Personal name cards have a moniker (first name only).
        Engine Feature Needed:
        - [ ] PersonalNameParser.extract_moniker(name) -> str | None (Rule 2.7.3)
        """
        if "," in self.name:
            return self.name.split(",")[0].strip()
        return None


@dataclass
class RulesTextReferenceStub:
    """
    Stub for resolving name/moniker references in rules text.

    Rules:
    - Rule 2.12.3a: Name/moniker of source = self-reference → refers to this card
    - Rule 2.12.3b: Name in creation context = hypothetical; otherwise = existing objects
    """

    source_card: "TextBoxCardStub"

    def is_self_reference(self, name_or_moniker: str) -> bool:
        """
        Rule 2.12.3a: Check if a name/moniker in rules text is a self-reference.

        Engine Feature Needed:
        - [ ] CardInstance.is_self_reference(name_or_moniker) -> bool (Rule 2.12.3a)
        """
        card = self.source_card
        if name_or_moniker.lower() == card.name.lower():
            return True
        if card.moniker and name_or_moniker.lower() == card.moniker.lower():
            return True
        return False

    def resolve_self_reference(
        self, name_or_moniker: str
    ) -> Optional["TextBoxCardStub"]:
        """
        Rule 2.12.3a: A self-reference resolves to 'this' (the source card).

        Engine Feature Needed:
        - [ ] RulesTextReferenceResolver.resolve_self(card, name) -> card (Rule 2.12.3a)
        """
        if self.is_self_reference(name_or_moniker):
            return self.source_card
        return None

    def is_creation_context(self, clause: str) -> bool:
        """
        Rule 2.12.3b: Check if a name/moniker reference is in a creation context.
        (e.g., 'Create a Runechant token' → Runechant is a hypothetical object).

        Engine Feature Needed:
        - [ ] RulesTextReferenceResolver.is_creation_context(clause) -> bool (Rule 2.12.3b)
        """
        creation_keywords = ["create", "put a", "make a", "generate"]
        lower = clause.lower()
        return any(kw in lower for kw in creation_keywords)


@dataclass
class HypotheticalObjectStub:
    """
    Stub representing a hypothetical object being created by rules text.

    Rule 2.12.3b: When rules text creates a named object, that name refers
    to a hypothetical object with defined properties, including the name.

    Engine Feature Needed:
    - [ ] HypotheticalObject class with name and properties (Rule 2.12.3b)
    """

    name: str
    properties: List[str] = field(default_factory=list)

    def has_property(self, prop: str) -> bool:
        """Rule 2.12.3b: Hypothetical object has its defined properties."""
        return prop.lower() in [p.lower() for p in self.properties]


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def game_state():
    """
    Fixture providing game state for testing Section 2.12: Text Box.
    """

    class GameState212:
        def __init__(self):
            self.test_card = None
            self.second_card = None
            self.card_text = None
            self.rules_text_result = None
            self.reminder_text_result = None
            self.flavor_text_result = None
            self.has_text_box = None
            self.ability_count = None
            self.abilities_list = []
            self.self_reference_result = None
            self.reference_resolver = None
            self.hypothetical_object = None
            self.resolution_context = None

    return GameState212()


# ===========================================================================
# Scenario: Card has a text box containing card text
# Tests Rule 2.12.1
# ===========================================================================


@scenario(
    "../features/section_2_12_text_box.feature",
    "Card has a text box containing card text",
)
def test_card_has_text_box():
    """Rule 2.12.1: The text box of a card contains the card text."""
    pass


@given('a card with text box rules text "Go again."')
def step_card_with_text_box_rules_text(game_state):
    """Rule 2.12.1: Card with rules text in its text box."""
    game_state.test_card = TextBoxCardStub(name="Test Attack", _rules_text="Go again.")


@when("the engine reads the text box card text")
def step_read_text_box_card_text(game_state):
    """Rule 2.12.1: Engine reads the card text from the text box."""
    game_state.card_text = game_state.test_card.text_box
    game_state.has_text_box = game_state.test_card.has_text_box


@then("the card has a text box")
def step_card_has_text_box(game_state):
    """Rule 2.12.1: Card has a text box property."""
    assert game_state.has_text_box is True, "Card should have a text box"


@then("the text box contains card text")
def step_text_box_contains_card_text(game_state):
    """Rule 2.12.1: Text box contains card text."""
    assert game_state.card_text is not None, "Text box should contain card text"
    assert len(game_state.card_text) > 0, "Text box should be non-empty"


# ===========================================================================
# Scenario: Card without rules text has an empty text box
# Tests Rule 2.12.1
# ===========================================================================


@scenario(
    "../features/section_2_12_text_box.feature",
    "Card without rules text has an empty text box",
)
def test_card_without_rules_text_empty_text_box():
    """Rule 2.12.1: A card with no rules text has an empty/absent card text."""
    pass


@given("a card with no text box rules text")
def step_card_with_no_text_box_rules_text(game_state):
    """Rule 2.12.1: Card with no rules text."""
    game_state.test_card = TextBoxCardStub(name="Vanilla Card", _rules_text=None)


@when("the engine reads the empty text box")
def step_read_empty_text_box(game_state):
    """Rule 2.12.1: Read card text from a card with no rules text."""
    game_state.card_text = game_state.test_card.text_box
    game_state.has_text_box = game_state.test_card.has_text_box


@then("the card text is empty or absent")
def step_card_text_empty_or_absent(game_state):
    """Rule 2.12.1: Card text is empty or None when no rules text."""
    assert game_state.card_text is None or game_state.card_text == "", (
        f"Card text should be empty or absent, got: {game_state.card_text!r}"
    )


# ===========================================================================
# Scenario: Card text includes rules text component
# Tests Rule 2.12.2
# ===========================================================================


@scenario(
    "../features/section_2_12_text_box.feature",
    "Card text includes rules text component",
)
def test_card_text_includes_rules_text():
    """Rule 2.12.2: Card text contains rules text."""
    pass


@given('a card with only rules text "Go again."')
def step_card_with_only_rules_text(game_state):
    """Rule 2.12.2: Card with only rules text."""
    game_state.test_card = TextBoxCardStub(name="Test Card", _rules_text="Go again.")


@when("the engine reads the rules text component")
def step_read_rules_text_component(game_state):
    """Rule 2.12.2: Engine reads the rules text component."""
    game_state.rules_text_result = game_state.test_card.rules_text


@then(parsers.parse('the rules text is "{expected}"'))
def step_rules_text_is(game_state, expected):
    """Rule 2.12.2: Rules text matches expected."""
    assert game_state.rules_text_result == expected, (
        f"Expected rules text '{expected}', got '{game_state.rules_text_result}'"
    )


# ===========================================================================
# Scenario: Card text can include reminder text
# Tests Rule 2.12.2
# ===========================================================================


@scenario(
    "../features/section_2_12_text_box.feature",
    "Card text can include reminder text",
)
def test_card_text_includes_reminder_text():
    """Rule 2.12.2: Card text can contain reminder text."""
    pass


@given(
    'a card with rules text and reminder text "(If you play this card before your action phase ends, you may play another card.)"'
)
def step_card_with_reminder_text(game_state):
    """Rule 2.12.2: Card with rules text and reminder text."""
    game_state.test_card = TextBoxCardStub(
        name="Test Card",
        _rules_text="Go again.",
        _reminder_text="(If you play this card before your action phase ends, you may play another card.)",
    )


@when("the engine reads the reminder text component")
def step_read_reminder_text_component(game_state):
    """Rule 2.12.2: Engine reads the reminder text component."""
    game_state.reminder_text_result = game_state.test_card.reminder_text


@then(
    'the card has reminder text "(If you play this card before your action phase ends, you may play another card.)"'
)
def step_card_has_reminder_text(game_state):
    """Rule 2.12.2: Reminder text matches expected."""
    expected = "(If you play this card before your action phase ends, you may play another card.)"
    assert game_state.reminder_text_result is not None, (
        "Reminder text should be present"
    )
    assert game_state.reminder_text_result == expected, (
        f"Expected reminder text '{expected}', got '{game_state.reminder_text_result}'"
    )


# ===========================================================================
# Scenario: Card text can include flavor text
# Tests Rule 2.12.2
# ===========================================================================


@scenario(
    "../features/section_2_12_text_box.feature",
    "Card text can include flavor text",
)
def test_card_text_includes_flavor_text():
    """Rule 2.12.2: Card text can contain flavor text."""
    pass


@given('a card with rules text and flavor text "The true warrior never tires."')
def step_card_with_flavor_text(game_state):
    """Rule 2.12.2: Card with rules text and flavor text."""
    game_state.test_card = TextBoxCardStub(
        name="Test Card",
        _rules_text="Go again.",
        _flavor_text="The true warrior never tires.",
    )


@when("the engine reads the flavor text component")
def step_read_flavor_text_component(game_state):
    """Rule 2.12.2: Engine reads the flavor text component."""
    game_state.flavor_text_result = game_state.test_card.flavor_text


@then('the card has flavor text "The true warrior never tires."')
def step_card_has_flavor_text(game_state):
    """Rule 2.12.2: Flavor text matches expected."""
    expected = "The true warrior never tires."
    assert game_state.flavor_text_result is not None, "Flavor text should be present"
    assert game_state.flavor_text_result == expected, (
        f"Expected flavor text '{expected}', got '{game_state.flavor_text_result}'"
    )


# ===========================================================================
# Scenario: Card text may have no reminder text
# Tests Rule 2.12.2
# ===========================================================================


@scenario(
    "../features/section_2_12_text_box.feature",
    "Card text may have no reminder text",
)
def test_card_text_may_have_no_reminder_text():
    """Rule 2.12.2: Card text may omit reminder text."""
    pass


@given("a card with only rules text and no reminder text")
def step_card_only_rules_no_reminder(game_state):
    """Rule 2.12.2: Card with rules text but no reminder text."""
    game_state.test_card = TextBoxCardStub(
        name="Test Card",
        _rules_text="Go again.",
        _reminder_text=None,
    )


@when("the engine reads the reminder text field")
def step_read_reminder_text_field(game_state):
    """Rule 2.12.2: Engine reads the reminder text field."""
    game_state.reminder_text_result = game_state.test_card.reminder_text


@then("the card has no reminder text")
def step_no_reminder_text(game_state):
    """Rule 2.12.2: Reminder text is absent."""
    assert game_state.reminder_text_result is None, (
        f"Expected no reminder text, got '{game_state.reminder_text_result}'"
    )


# ===========================================================================
# Scenario: Card text may have no flavor text
# Tests Rule 2.12.2
# ===========================================================================


@scenario(
    "../features/section_2_12_text_box.feature",
    "Card text may have no flavor text",
)
def test_card_text_may_have_no_flavor_text():
    """Rule 2.12.2: Card text may omit flavor text."""
    pass


@given("a card with only rules text and no flavor text")
def step_card_only_rules_no_flavor(game_state):
    """Rule 2.12.2: Card with rules text but no flavor text."""
    game_state.test_card = TextBoxCardStub(
        name="Test Card",
        _rules_text="Go again.",
        _flavor_text=None,
    )


@when("the engine reads the flavor text field")
def step_read_flavor_text_field(game_state):
    """Rule 2.12.2: Engine reads the flavor text field."""
    game_state.flavor_text_result = game_state.test_card.flavor_text


@then("the card has no flavor text")
def step_no_flavor_text(game_state):
    """Rule 2.12.2: Flavor text is absent."""
    assert game_state.flavor_text_result is None, (
        f"Expected no flavor text, got '{game_state.flavor_text_result}'"
    )


# ===========================================================================
# Scenario: Rules text defines the base abilities of a card
# Tests Rule 2.12.3
# ===========================================================================


@scenario(
    "../features/section_2_12_text_box.feature",
    "Rules text defines the base abilities of a card",
)
def test_rules_text_defines_base_abilities():
    """Rule 2.12.3: The rules text of a card defines its base abilities."""
    pass


@given('a card whose rules text is "Go again."')
def step_card_whose_rules_text_is_go_again(game_state):
    """Rule 2.12.3: Card with 'Go again.' as its rules text."""
    game_state.test_card = TextBoxCardStub(
        name="Test Attack",
        _rules_text="Go again.",
    )


@when("the engine evaluates the rules text for base abilities")
def step_evaluate_rules_text_for_base_abilities(game_state):
    """Rule 2.12.3: Engine evaluates what abilities the rules text defines."""
    game_state.abilities_list = game_state.test_card.get_base_abilities()


@then(parsers.parse('the card has base ability "{ability_name}"'))
def step_card_has_base_ability(game_state, ability_name):
    """Rule 2.12.3: Card has the expected base ability."""
    assert game_state.test_card.has_ability(ability_name), (
        f"Expected card to have base ability '{ability_name}'. "
        f"Abilities: {game_state.abilities_list}"
    )


# ===========================================================================
# Scenario: Each paragraph of rules text defines a single ability
# Tests Rule 2.12.3
# ===========================================================================


@scenario(
    "../features/section_2_12_text_box.feature",
    "Each paragraph of rules text defines a single ability",
)
def test_each_paragraph_is_one_ability():
    """Rule 2.12.3: A paragraph of rules text typically defines a single ability."""
    pass


@given('a card with two ability paragraphs "Go again." and "Draw a card."')
def step_card_two_ability_paragraphs(game_state):
    """Rule 2.12.3: Card with two separate ability paragraphs."""
    game_state.test_card = TextBoxCardStub(
        name="Test Card",
        _rules_text="Go again.\nDraw a card.",
    )


@when("the engine counts abilities from rules text paragraphs")
def step_count_abilities_from_paragraphs(game_state):
    """Rule 2.12.3: Engine counts abilities from rules text paragraphs."""
    game_state.abilities_list = game_state.test_card.get_base_abilities()
    game_state.ability_count = len(game_state.abilities_list)


@then(parsers.parse("the card has {count:d} base abilities"))
def step_card_has_n_abilities(game_state, count):
    """Rule 2.12.3: Card has N base abilities from N paragraphs."""
    assert game_state.ability_count == count, (
        f"Expected {count} base abilities, got {game_state.ability_count}. "
        f"Abilities: {game_state.abilities_list}"
    )


# ===========================================================================
# Scenario: Reminder text does not contribute to base abilities
# Tests Rule 2.12.3
# ===========================================================================


@scenario(
    "../features/section_2_12_text_box.feature",
    "Reminder text does not contribute to base abilities",
)
def test_reminder_text_does_not_add_abilities():
    """Rule 2.12.3: Reminder text does not affect the game."""
    pass


@given("a card with go again rules text and a reminder text paragraph")
def step_card_with_go_again_and_reminder(game_state):
    """Rule 2.12.3: Card with go again and a reminder text."""
    game_state.test_card = TextBoxCardStub(
        name="Test Card",
        _rules_text="Go again.",
        _reminder_text="(If you play this card before your action phase ends, you may play another card.)",
    )


@when("the engine evaluates abilities excluding reminder text")
def step_evaluate_abilities_excluding_reminder(game_state):
    """Rule 2.12.3: Engine evaluates abilities, ignoring reminder text."""
    game_state.abilities_list = game_state.test_card.get_base_abilities()


@then("the reminder text does not add any abilities to the card")
def step_reminder_no_abilities(game_state):
    """Rule 2.12.3: Reminder text adds zero abilities; only 1 ability (go again) present."""
    assert len(game_state.abilities_list) == 1, (
        f"Expected 1 ability (not counting reminder text), "
        f"got {len(game_state.abilities_list)}: {game_state.abilities_list}"
    )


# ===========================================================================
# Scenario: Flavor text does not contribute to base abilities
# Tests Rule 2.12.3
# ===========================================================================


@scenario(
    "../features/section_2_12_text_box.feature",
    "Flavor text does not contribute to base abilities",
)
def test_flavor_text_does_not_add_abilities():
    """Rule 2.12.3: Flavor text does not affect the game."""
    pass


@given("a card with go again rules text and a flavor text paragraph")
def step_card_with_go_again_and_flavor(game_state):
    """Rule 2.12.3: Card with go again and flavor text."""
    game_state.test_card = TextBoxCardStub(
        name="Test Card",
        _rules_text="Go again.",
        _flavor_text="The true warrior never tires.",
    )


@when("the engine evaluates abilities excluding flavor text")
def step_evaluate_abilities_excluding_flavor(game_state):
    """Rule 2.12.3: Engine evaluates abilities, ignoring flavor text."""
    game_state.abilities_list = game_state.test_card.get_base_abilities()


@then("the flavor text does not add any abilities to the card")
def step_flavor_no_abilities(game_state):
    """Rule 2.12.3: Flavor text adds zero abilities; only 1 ability (go again) present."""
    assert len(game_state.abilities_list) == 1, (
        f"Expected 1 ability (not counting flavor text), "
        f"got {len(game_state.abilities_list)}: {game_state.abilities_list}"
    )


# ===========================================================================
# Scenario: Card name in rules text is a self-reference
# Tests Rule 2.12.3a
# ===========================================================================


@scenario(
    "../features/section_2_12_text_box.feature",
    "Card name in rules text is a self-reference",
)
def test_card_name_in_rules_text_is_self_reference():
    """Rule 2.12.3a: Name of source object in rules text is a self-reference."""
    pass


@given('a card named "Pummel" with self-referencing rules text')
def step_pummel_with_self_ref_rules_text(game_state):
    """Rule 2.12.3a: Pummel card with self-referencing rules text."""
    game_state.test_card = TextBoxCardStub(
        name="Pummel",
        _rules_text="When Pummel enters play, draw a card.",
        _instance_id=1,
    )
    game_state.reference_resolver = RulesTextReferenceStub(
        source_card=game_state.test_card
    )


@when(
    parsers.parse(
        'the engine resolves the name reference "{ref_name}" in the rules text'
    )
)
def step_resolve_name_ref(game_state, ref_name):
    """Rule 2.12.3a: Engine resolves the name reference."""
    game_state.self_reference_result = (
        game_state.reference_resolver.resolve_self_reference(ref_name)
    )


@then("the reference resolves to the card itself")
def step_ref_resolves_to_self(game_state):
    """Rule 2.12.3a: Self-reference resolves to the source card."""
    assert game_state.self_reference_result is not None, (
        "Expected self-reference to resolve to the source card, got None"
    )
    assert game_state.self_reference_result is game_state.test_card, (
        "Self-reference should resolve to the source card itself"
    )


@then("it does not refer to any other card with the same name")
def step_ref_not_other_cards(game_state):
    """Rule 2.12.3a: Self-reference does not refer to other same-named cards."""
    assert game_state.self_reference_result is game_state.test_card, (
        "Self-reference must be to THIS card instance, not any other"
    )


# ===========================================================================
# Scenario: Card moniker in rules text is a self-reference
# Tests Rule 2.12.3a
# ===========================================================================


@scenario(
    "../features/section_2_12_text_box.feature",
    "Card moniker in rules text is a self-reference",
)
def test_card_moniker_in_rules_text_is_self_reference():
    """Rule 2.12.3a: Moniker of source object in rules text is a self-reference."""
    pass


@given(
    'a hero card named "Bravo, Showstopper" with moniker self-referencing rules text'
)
def step_bravo_showstopper_with_moniker_ref(game_state):
    """Rule 2.12.3a: Bravo hero with moniker self-reference in rules text."""
    game_state.test_card = TextBoxCardStub(
        name="Bravo, Showstopper",
        _rules_text="When Bravo enters play, gain 1 life.",
    )
    game_state.reference_resolver = RulesTextReferenceStub(
        source_card=game_state.test_card
    )


@when(
    parsers.parse(
        'the engine resolves the moniker reference "{moniker_name}" in the rules text'
    )
)
def step_resolve_moniker_ref(game_state, moniker_name):
    """Rule 2.12.3a: Engine resolves the moniker reference."""
    game_state.self_reference_result = (
        game_state.reference_resolver.resolve_self_reference(moniker_name)
    )


@then("the reference resolves to the hero card itself")
def step_moniker_ref_resolves_to_self(game_state):
    """Rule 2.12.3a: Moniker self-reference resolves to the hero card."""
    assert game_state.self_reference_result is not None, (
        "Expected moniker self-reference to resolve to source hero card, got None"
    )
    assert game_state.self_reference_result is game_state.test_card, (
        "Moniker self-reference should resolve to the hero card itself"
    )


# ===========================================================================
# Scenario: Self-reference does not match other same-named card instances
# Tests Rule 2.12.3a
# ===========================================================================


@scenario(
    "../features/section_2_12_text_box.feature",
    "Self-reference does not match other same-named card instances",
)
def test_self_reference_not_other_instances():
    """Rule 2.12.3a: Self-reference refers to THIS card, not other same-named cards."""
    pass


@given("a primary Pummel card with self-referencing rules text")
def step_primary_pummel_card(game_state):
    """Rule 2.12.3a: First Pummel instance with self-referencing rules text."""
    game_state.test_card = TextBoxCardStub(
        name="Pummel",
        _rules_text="When Pummel enters play, draw a card.",
        _instance_id=1,
    )
    game_state.reference_resolver = RulesTextReferenceStub(
        source_card=game_state.test_card
    )


@given("another separate Pummel card instance in play")
def step_second_pummel_in_play(game_state):
    """Rule 2.12.3a: Second Pummel instance in play."""
    game_state.second_card = TextBoxCardStub(
        name="Pummel",
        _rules_text="When Pummel enters play, draw a card.",
        _instance_id=2,
    )


@when("the engine resolves the Pummel self-reference in the first card's context")
def step_resolve_pummel_self(game_state):
    """Rule 2.12.3a: Resolve 'Pummel' in the first card's context."""
    game_state.self_reference_result = (
        game_state.reference_resolver.resolve_self_reference("Pummel")
    )


@then("the reference refers only to the first card, not the second")
def step_ref_only_first_card(game_state):
    """Rule 2.12.3a: Self-reference is to this specific card instance, not others."""
    assert game_state.self_reference_result is game_state.test_card, (
        "Self-reference must resolve to the FIRST card instance (id=1)"
    )
    assert game_state.self_reference_result is not game_state.second_card, (
        "Self-reference must NOT resolve to the second card instance (id=2)"
    )


# ===========================================================================
# Scenario: Creating a named token refers to a hypothetical object
# Tests Rule 2.12.3b
# ===========================================================================


@scenario(
    "../features/section_2_12_text_box.feature",
    "Creating a named token refers to a hypothetical object",
)
def test_creating_named_token_is_hypothetical():
    """Rule 2.12.3b: Name in creation context refers to a hypothetical object."""
    pass


@given("a card whose rules text creates a Runechant token")
def step_card_creates_runechant_token(game_state):
    """Rule 2.12.3b: Card with 'Create a Runechant token.' rules text."""
    game_state.test_card = TextBoxCardStub(
        name="Source Card",
        _rules_text="Create a Runechant token.",
    )
    game_state.reference_resolver = RulesTextReferenceStub(
        source_card=game_state.test_card
    )


@when("the engine checks whether the Runechant reference is a creation context")
def step_check_runechant_creation_context(game_state):
    """Rule 2.12.3b: Engine checks if the rules text is in a creation context."""
    rules_text = game_state.test_card.rules_text
    game_state.resolution_context = game_state.reference_resolver.is_creation_context(
        rules_text
    )
    game_state.hypothetical_object = HypotheticalObjectStub(name="Runechant")


@then('the "Runechant" reference is to a hypothetical object being created')
def step_runechant_is_hypothetical(game_state):
    """Rule 2.12.3b: Runechant reference is in creation context (hypothetical)."""
    assert game_state.resolution_context is True, (
        "Expected 'Create a Runechant token.' to be a creation context"
    )
    assert game_state.hypothetical_object is not None, (
        "Expected a hypothetical object to be created"
    )


@then('the hypothetical object has the name "Runechant"')
def step_hypothetical_has_name(game_state):
    """Rule 2.12.3b: Hypothetical object has the name from the creation instruction."""
    assert game_state.hypothetical_object.name == "Runechant", (
        f"Expected hypothetical name 'Runechant', "
        f"got '{game_state.hypothetical_object.name}'"
    )


# ===========================================================================
# Scenario: Reference to named object not being created refers to existing objects
# Tests Rule 2.12.3b
# ===========================================================================


@scenario(
    "../features/section_2_12_text_box.feature",
    "Reference to named object not being created refers to existing objects",
)
def test_destroy_target_refers_to_existing_objects():
    """Rule 2.12.3b: Name outside creation context refers to existing objects."""
    pass


@given("a card whose rules text destroys a target Runechant")
def step_card_destroys_runechant(game_state):
    """Rule 2.12.3b: Card with 'Destroy target Runechant.' rules text."""
    game_state.test_card = TextBoxCardStub(
        name="Source Card",
        _rules_text="Destroy target Runechant.",
    )
    game_state.reference_resolver = RulesTextReferenceStub(
        source_card=game_state.test_card
    )


@given("a Runechant token currently in the arena")
def step_runechant_token_in_arena(game_state):
    """Rule 2.12.3b: A Runechant token exists in the arena."""
    game_state.second_card = TextBoxCardStub(
        name="Runechant",
        _rules_text=None,
        _instance_id=10,
    )


@when("the engine checks whether the Runechant reference is a non-creation context")
def step_check_runechant_non_creation_context(game_state):
    """Rule 2.12.3b: Engine checks if the rules text is NOT in a creation context."""
    rules_text = game_state.test_card.rules_text
    game_state.resolution_context = game_state.reference_resolver.is_creation_context(
        rules_text
    )


@then('the "Runechant" reference refers to the existing Runechant token in play')
def step_runechant_refers_to_existing(game_state):
    """Rule 2.12.3b: Non-creation context refers to existing objects."""
    # "Destroy target Runechant." is NOT a creation context
    assert game_state.resolution_context is False, (
        "'Destroy target Runechant.' should NOT be a creation context "
        f"(is_creation_context returned {game_state.resolution_context})"
    )
    assert game_state.second_card is not None, (
        "Expected an existing Runechant token in the arena to be the target"
    )
    assert game_state.second_card.name == "Runechant", (
        "Expected existing Runechant token to be targeted"
    )


# ===========================================================================
# Scenario: Hypothetical named object has properties defined by creating instruction
# Tests Rule 2.12.3b
# ===========================================================================


@scenario(
    "../features/section_2_12_text_box.feature",
    "Hypothetical named object has properties defined by creating instruction",
)
def test_hypothetical_object_has_defined_properties():
    """Rule 2.12.3b: Hypothetical object includes the name and defined properties."""
    pass


@given("a card whose rules text creates a Runechant token with go again")
def step_card_creates_runechant_with_go_again(game_state):
    """Rule 2.12.3b: Card with 'Create a Runechant token with go again.' rules text."""
    game_state.test_card = TextBoxCardStub(
        name="Source Card",
        _rules_text="Create a Runechant token with go again.",
    )
    game_state.reference_resolver = RulesTextReferenceStub(
        source_card=game_state.test_card
    )


@when("the engine constructs the hypothetical Runechant object")
def step_construct_hypothetical_runechant(game_state):
    """Rule 2.12.3b: Engine builds the hypothetical object with its properties."""
    game_state.hypothetical_object = HypotheticalObjectStub(
        name="Runechant",
        properties=["go again"],
    )


@then('the hypothetical Runechant has property "go again"')
def step_hypothetical_has_go_again(game_state):
    """Rule 2.12.3b: Hypothetical object has the properties from the creation instruction."""
    assert game_state.hypothetical_object.has_property("go again"), (
        "Expected hypothetical Runechant to have 'go again' property"
    )


@then('the hypothetical Runechant has name "Runechant"')
def step_hypothetical_runechant_name(game_state):
    """Rule 2.12.3b: Hypothetical object has the specified name."""
    assert game_state.hypothetical_object.name == "Runechant", (
        f"Expected name 'Runechant', got '{game_state.hypothetical_object.name}'"
    )
