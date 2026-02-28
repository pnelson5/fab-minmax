"""
Step definitions for Section 2.10: Subtypes
Reference: Flesh and Blood Comprehensive Rules Section 2.10

This module implements behavioral tests for the subtypes property of objects
in Flesh and Blood.

Rule 2.10.1: Subtypes are a collection of subtype keywords. The functional
             subtypes of a card determine what additional rules apply to the card.

Rule 2.10.2: An object can have zero or more subtypes.

Rule 2.10.3: The subtypes of a card are determined by its type box. Subtypes
             (if any) are printed after a long dash after the card's type.
             Example: "Action - Attack" has subtype "Attack" after the long dash.

Rule 2.10.4: The subtypes of an activated-layer or triggered-layer are the
             same as the subtypes of its source.

Rule 2.10.5: An object can gain or lose subtypes from rules and/or effects.

Rule 2.10.6: Subtypes are either functional or non-functional keywords.
             Functional subtypes add additional rules to an object.[8.2]
             Non-functional subtypes do not add additional rules to an object.

Rule 2.10.6a: The functional subtype keywords are (1H), (2H), Affliction,
              Ally, Arrow, Ash, Attack, Aura, Construct, Figment, Invocation,
              Item, Landmark, Off-Hand, and Quiver.

Rule 2.10.6b: The non-functional subtypes keywords are Angel, Arms, Axe,
              Base, Book, Bow, Brush, Cannon, Chest, Chi, Claw, Club, Cog,
              Dagger, Demon, Dragon, Evo, Fiddle, Flail, Gem, Gun, Hammer,
              Head, Legs, Lute, Mercenary, Orb, Pistol, Pit-Fighter, Polearm,
              Rock, Scepter, Scroll, Scythe, Shuriken, Song, Staff, Sword,
              Trap, Wrench, and Young.

Engine Features Needed for Section 2.10:
- [ ] `CardTemplate.subtypes` or `CardInstance.subtypes` returning a list/set of
      subtype strings (Rule 2.10.2)
- [ ] `CardTemplate.functional_subtypes` returning only functional subtypes (Rule 2.10.6)
- [ ] `SubtypeRegistry.is_functional(name)` classifying subtypes (Rule 2.10.6)
- [ ] `SubtypeRegistry.FUNCTIONAL_SUBTYPES` list containing all 15 functional
      subtypes (Rule 2.10.6a)
- [ ] Type box parser: extracts type and subtypes from "Type - Subtype" format (Rule 2.10.3)
- [ ] `Layer.subtypes` property inheriting from source (Rule 2.10.4)
- [ ] `CardInstance.gain_subtype(name)` method (Rule 2.10.5)
- [ ] `CardInstance.lose_subtype(name)` method (Rule 2.10.5)
"""

import pytest
from pytest_bdd import scenario, given, when, then, parsers
from dataclasses import dataclass, field
from typing import Optional, List, Set


# ---------------------------------------------------------------------------
# Stub classes for testing Section 2.10 rules
# ---------------------------------------------------------------------------

# Rule 2.10.6a: The complete list of functional subtype keywords
FUNCTIONAL_SUBTYPES = frozenset(
    [
        "(1H)",
        "(2H)",
        "Affliction",
        "Ally",
        "Arrow",
        "Ash",
        "Attack",
        "Aura",
        "Construct",
        "Figment",
        "Invocation",
        "Item",
        "Landmark",
        "Off-Hand",
        "Quiver",
    ]
)

# Rule 2.10.6b: A subset of non-functional subtypes keywords (for testing)
NON_FUNCTIONAL_SUBTYPES = frozenset(
    [
        "Angel",
        "Arms",
        "Axe",
        "Base",
        "Book",
        "Bow",
        "Brush",
        "Cannon",
        "Chest",
        "Chi",
        "Claw",
        "Club",
        "Cog",
        "Dagger",
        "Demon",
        "Dragon",
        "Evo",
        "Fiddle",
        "Flail",
        "Gem",
        "Gun",
        "Hammer",
        "Head",
        "Legs",
        "Lute",
        "Mercenary",
        "Orb",
        "Pistol",
        "Pit-Fighter",
        "Polearm",
        "Rock",
        "Scepter",
        "Scroll",
        "Scythe",
        "Shuriken",
        "Song",
        "Staff",
        "Sword",
        "Trap",
        "Wrench",
        "Young",
    ]
)


@dataclass
class SubtypeCardStub:
    """
    Stub representing a card with subtypes.

    Models what the engine must implement for Section 2.10.
    Engine Features Needed:
    - [ ] CardInstance.subtypes: set of subtype strings (Rule 2.10.2)
    - [ ] CardInstance.functional_subtypes: only functional ones (Rule 2.10.6)
    - [ ] CardInstance.gain_subtype(name): gain a subtype (Rule 2.10.5)
    - [ ] CardInstance.lose_subtype(name): lose a subtype (Rule 2.10.5)
    """

    name: str = "Test Card"
    _subtypes: Set[str] = field(default_factory=set)

    @property
    def subtypes(self) -> Set[str]:
        """Rule 2.10.2: Zero or more subtypes."""
        return set(self._subtypes)

    @property
    def functional_subtypes(self) -> Set[str]:
        """Rule 2.10.6: Only functional subtypes."""
        return {st for st in self._subtypes if st in FUNCTIONAL_SUBTYPES}

    @property
    def non_functional_subtypes(self) -> Set[str]:
        """Rule 2.10.6: Only non-functional subtypes."""
        return {st for st in self._subtypes if st in NON_FUNCTIONAL_SUBTYPES}

    def has_subtype(self, name: str) -> bool:
        """Rule 2.10.2: Check if the card has a specific subtype."""
        return name in self._subtypes

    def gain_subtype(self, name: str) -> bool:
        """Rule 2.10.5: Object can gain a subtype from rules/effects."""
        self._subtypes.add(name)
        return True

    def lose_subtype(self, name: str) -> bool:
        """Rule 2.10.5: Object can lose a subtype from rules/effects."""
        if name in self._subtypes:
            self._subtypes.discard(name)
            return True
        return False


@dataclass
class TypeBoxParseResultStub:
    """
    Result of parsing a type box string.

    Rule 2.10.3: Subtypes are printed after a long dash after the card's type.
    Engine Features Needed:
    - [ ] TypeBoxParser.parse(type_box_string) -> (types, subtypes) (Rule 2.10.3)
    """

    type_string: str  # e.g., "Action"
    subtypes: List[str]  # e.g., ["Attack"]

    def parse_type_box(self, type_box: str) -> "TypeBoxParseResultStub":
        """Parse 'Type - Subtype' format."""
        if " - " in type_box:
            parts = type_box.split(" - ", 1)
            return TypeBoxParseResultStub(
                type_string=parts[0].strip(),
                subtypes=[s.strip() for s in parts[1].split(",")],
            )
        return TypeBoxParseResultStub(type_string=type_box.strip(), subtypes=[])


@dataclass
class LayerWithSubtypesStub:
    """
    Stub representing a layer that inherits subtypes from its source.

    Rule 2.10.4: Activated-layer and triggered-layer inherit source subtypes.
    Engine Features Needed:
    - [ ] ActivatedLayer.subtypes delegates to source.subtypes (Rule 2.10.4)
    - [ ] TriggeredLayer.subtypes delegates to source.subtypes (Rule 2.10.4)
    """

    layer_category: str  # "activated-layer" or "triggered-layer"
    source: SubtypeCardStub

    @property
    def subtypes(self) -> Set[str]:
        """Rule 2.10.4: Inherit subtypes from source."""
        return self.source.subtypes

    def has_subtype(self, name: str) -> bool:
        """Rule 2.10.4: Inherited subtype check."""
        return name in self.subtypes


@dataclass
class SubtypeCheckResultStub:
    """
    Result of checking subtype functionality.

    Rule 2.10.6: Subtypes are either functional or non-functional.
    """

    subtype_name: str
    is_functional: bool
    adds_additional_rules: bool

    @classmethod
    def for_subtype(cls, name: str) -> "SubtypeCheckResultStub":
        """Create a result stub checking whether a subtype is functional."""
        is_func = name in FUNCTIONAL_SUBTYPES
        return cls(
            subtype_name=name,
            is_functional=is_func,
            adds_additional_rules=is_func,
        )


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def game_state():
    """
    Fixture providing game state for Section 2.10 subtype tests.

    Uses dynamic attributes for test state sharing between steps.
    Reference: Rule 2.10
    """
    from tests.bdd_helpers import BDDGameState

    state = BDDGameState()

    # Test objects for subtype tracking
    state.subtype_card = None
    state.second_subtype_card = None
    state.layer_source_card = None
    state.layer = None
    state.type_box_parse_result = None
    state.subtype_check_result = None
    state.functional_keyword_list = list(FUNCTIONAL_SUBTYPES)
    state.non_functional_keyword_list = list(NON_FUNCTIONAL_SUBTYPES)
    state.functional_subtype_count = None
    state.subtype_adds_rules = None

    return state


# ---------------------------------------------------------------------------
# Scenario: Subtypes are subtype keywords that determine additional rules
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_10_subtypes.feature",
    "Subtypes are subtype keywords that determine additional rules",
)
def test_subtypes_are_subtype_keywords():
    """Rule 2.10.1: Subtypes are subtype keywords; functional ones add rules."""
    pass


@given('a card is created with the subtype "Attack"')
def create_card_with_attack_subtype(game_state):
    """Rule 2.10.1: Create a card with the Attack subtype."""
    game_state.subtype_card = SubtypeCardStub(
        name="Test Attack Card",
        _subtypes={"Attack"},
    )


@when("the engine checks the subtypes of the attack-subtype card")
def check_attack_subtype_card_subtypes(game_state):
    """Rule 2.10.1: Check the subtypes on the attack-subtype card."""
    game_state.subtype_check_result = SubtypeCheckResultStub.for_subtype("Attack")


@then('the attack-subtype card should have the "Attack" subtype')
def assert_has_attack_subtype(game_state):
    """Rule 2.10.1: Card should have the Attack subtype."""
    assert game_state.subtype_card.has_subtype("Attack"), (
        "Engine Feature Needed: CardInstance.has_subtype('Attack') -> True"
    )


@then('the "Attack" subtype should be recognized as a functional subtype')
def assert_attack_is_functional(game_state):
    """Rule 2.10.1/2.10.6a: Attack is a functional subtype."""
    assert game_state.subtype_check_result.is_functional, (
        "Engine Feature Needed: SubtypeRegistry.is_functional('Attack') -> True (Rule 2.10.6a)"
    )


# ---------------------------------------------------------------------------
# Scenario: Non-functional subtypes do not add additional rules to an object
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_10_subtypes.feature",
    "Non-functional subtypes do not add additional rules to an object",
)
def test_non_functional_subtypes_add_no_rules():
    """Rule 2.10.6: Non-functional subtypes don't add additional rules."""
    pass


@given('a card is created with the subtype "Sword"')
def create_card_with_sword_subtype(game_state):
    """Rule 2.10.6b: Create a card with the Sword non-functional subtype."""
    game_state.subtype_card = SubtypeCardStub(
        name="Sword Card",
        _subtypes={"Sword"},
    )


@when('the engine checks whether "Sword" is a functional subtype')
def check_sword_is_functional(game_state):
    """Rule 2.10.6b: Check whether Sword is a functional subtype."""
    game_state.subtype_check_result = SubtypeCheckResultStub.for_subtype("Sword")


@then('"Sword" should not be a functional subtype')
def assert_sword_not_functional(game_state):
    """Rule 2.10.6b: Sword is a non-functional subtype."""
    assert not game_state.subtype_check_result.is_functional, (
        "Engine Feature Needed: SubtypeRegistry.is_functional('Sword') -> False (Rule 2.10.6b)"
    )


@then('the sword-subtype card should have the "Sword" subtype')
def assert_card_has_sword(game_state):
    """Rule 2.10.2: Card still has its non-functional subtype."""
    assert game_state.subtype_card.has_subtype("Sword"), (
        "Engine Feature Needed: CardInstance.has_subtype('Sword') -> True (Rule 2.10.2)"
    )


# ---------------------------------------------------------------------------
# Scenario: Object with zero subtypes is valid
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_10_subtypes.feature",
    "Object with zero subtypes is valid",
)
def test_object_with_zero_subtypes():
    """Rule 2.10.2: An object can have zero subtypes."""
    pass


@given("a card is created with no subtypes")
def create_card_with_no_subtypes(game_state):
    """Rule 2.10.2: Create a card with no subtypes."""
    game_state.subtype_card = SubtypeCardStub(
        name="No Subtype Card",
        _subtypes=set(),
    )


@when("the engine checks the subtypes of the no-subtype card")
def check_no_subtype_card(game_state):
    """Rule 2.10.2: Check subtypes of zero-subtype card."""
    # Nothing to compute; subtypes already tracked in game_state.subtype_card
    pass


@then("the no-subtype card should have zero subtypes")
def assert_zero_subtypes(game_state):
    """Rule 2.10.2: Card has zero subtypes."""
    assert len(game_state.subtype_card.subtypes) == 0, (
        "Engine Feature Needed: CardInstance.subtypes returns empty collection "
        "when no subtypes defined (Rule 2.10.2)"
    )


@then("the no-subtype card should still be a valid game object")
def assert_no_subtype_valid_object(game_state):
    """Rule 2.10.2: Zero subtypes doesn't make an invalid object."""
    assert game_state.subtype_card is not None, (
        "Engine Feature Needed: CardInstance with zero subtypes is still valid (Rule 2.10.2)"
    )


# ---------------------------------------------------------------------------
# Scenario: Object can have exactly one subtype
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_10_subtypes.feature",
    "Object can have exactly one subtype",
)
def test_object_can_have_one_subtype():
    """Rule 2.10.2: An object can have exactly one subtype."""
    pass


@given('a card is created with exactly one subtype "Ally"')
def create_card_with_ally_subtype(game_state):
    """Rule 2.10.2: Create a card with one subtype (Ally)."""
    game_state.subtype_card = SubtypeCardStub(
        name="Ally Card",
        _subtypes={"Ally"},
    )


@when("the engine checks the subtypes of the one-subtype card")
def check_one_subtype_card(game_state):
    """Rule 2.10.2: Check subtypes of one-subtype card."""
    pass


@then("the one-subtype card should have exactly 1 subtype")
def assert_one_subtype(game_state):
    """Rule 2.10.2: Card has exactly one subtype."""
    assert len(game_state.subtype_card.subtypes) == 1, (
        "Engine Feature Needed: CardInstance.subtypes count == 1 (Rule 2.10.2)"
    )


@then('the one-subtype card should have the "Ally" subtype')
def assert_has_ally(game_state):
    """Rule 2.10.2: Card has the Ally subtype."""
    assert game_state.subtype_card.has_subtype("Ally"), (
        "Engine Feature Needed: CardInstance.has_subtype('Ally') -> True (Rule 2.10.2)"
    )


# ---------------------------------------------------------------------------
# Scenario: Object can have multiple subtypes
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_10_subtypes.feature",
    "Object can have multiple subtypes",
)
def test_object_can_have_multiple_subtypes():
    """Rule 2.10.2: An object can have multiple subtypes."""
    pass


@given('a card is created with subtypes "Attack" and "Arrow"')
def create_card_with_attack_and_arrow_subtypes(game_state):
    """Rule 2.10.2: Create a card with Attack and Arrow subtypes."""
    game_state.subtype_card = SubtypeCardStub(
        name="Arrow Attack Card",
        _subtypes={"Attack", "Arrow"},
    )


@when("the engine checks the subtypes of the multi-subtype card")
def check_multi_subtype_card(game_state):
    """Rule 2.10.2: Check the multi-subtype card's subtypes."""
    pass


@then("the multi-subtype card should have exactly 2 subtypes")
def assert_two_subtypes(game_state):
    """Rule 2.10.2: Card has two subtypes."""
    assert len(game_state.subtype_card.subtypes) == 2, (
        "Engine Feature Needed: CardInstance.subtypes count == 2 (Rule 2.10.2)"
    )


@then('the multi-subtype card should have the "Attack" subtype')
def assert_multi_has_attack(game_state):
    """Rule 2.10.2: Multi-subtype card has Attack."""
    assert game_state.subtype_card.has_subtype("Attack"), (
        "Engine Feature Needed: CardInstance.has_subtype('Attack') -> True (Rule 2.10.2)"
    )


@then('the multi-subtype card should have the "Arrow" subtype')
def assert_multi_has_arrow(game_state):
    """Rule 2.10.2: Multi-subtype card has Arrow."""
    assert game_state.subtype_card.has_subtype("Arrow"), (
        "Engine Feature Needed: CardInstance.has_subtype('Arrow') -> True (Rule 2.10.2)"
    )


# ---------------------------------------------------------------------------
# Scenario: Subtypes are determined by the type box of the card
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_10_subtypes.feature",
    "Subtypes are determined by the type box of the card",
)
def test_subtypes_determined_by_type_box():
    """Rule 2.10.3: Subtypes come from the type box after the long dash."""
    pass


@given('a card is defined with type box "Action - Attack"')
def create_card_with_action_attack_type_box(game_state):
    """Rule 2.10.3: Create a card with type box 'Action - Attack'."""
    parser = TypeBoxParseResultStub(type_string="", subtypes=[])
    game_state.type_box_parse_result = parser.parse_type_box("Action - Attack")


@when("the engine parses the type box of the attack-action card")
def parse_attack_action_type_box(game_state):
    """Rule 2.10.3: Parse the type box to extract type and subtypes."""
    # Result already captured in type_box_parse_result
    pass


@then('the attack-action card type should be "Action"')
def assert_type_is_action(game_state):
    """Rule 2.10.3: Type extracted correctly from type box."""
    assert game_state.type_box_parse_result.type_string == "Action", (
        "Engine Feature Needed: TypeBoxParser.parse() extracts type 'Action' "
        "from 'Action - Attack' (Rule 2.10.3)"
    )


@then('the attack-action card subtype should be "Attack"')
def assert_subtype_is_attack(game_state):
    """Rule 2.10.3: Subtype extracted after long dash."""
    assert "Attack" in game_state.type_box_parse_result.subtypes, (
        "Engine Feature Needed: TypeBoxParser.parse() extracts subtype 'Attack' "
        "from 'Action - Attack' (Rule 2.10.3)"
    )


# ---------------------------------------------------------------------------
# Scenario: Card with no dash in type box has no subtype
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_10_subtypes.feature",
    "Card with no dash in type box has no subtype",
)
def test_card_with_no_dash_has_no_subtype():
    """Rule 2.10.3: No long dash in type box = no subtype."""
    pass


@given('a card is defined with type box "Instant"')
def create_card_with_instant_type_box(game_state):
    """Rule 2.10.3: Create a card with type box 'Instant' (no long dash)."""
    parser = TypeBoxParseResultStub(type_string="", subtypes=[])
    game_state.type_box_parse_result = parser.parse_type_box("Instant")


@when("the engine parses the type box of the instant-only card")
def parse_instant_type_box(game_state):
    """Rule 2.10.3: Parse the 'Instant' type box."""
    pass


@then("the instant-only card should have no subtype from its type box")
def assert_instant_has_no_subtype(game_state):
    """Rule 2.10.3: No dash = no subtype."""
    assert len(game_state.type_box_parse_result.subtypes) == 0, (
        "Engine Feature Needed: TypeBoxParser.parse('Instant') returns empty subtypes "
        "(Rule 2.10.3)"
    )


# ---------------------------------------------------------------------------
# Scenario: Activated-layer inherits subtypes from its source
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_10_subtypes.feature",
    "Activated-layer inherits subtypes from its source",
)
def test_activated_layer_inherits_subtypes():
    """Rule 2.10.4: Activated-layer subtypes = source subtypes."""
    pass


@given('a card is created with the subtype "Ally" as a layer source')
def create_ally_layer_source(game_state):
    """Rule 2.10.4: Create a card with Ally subtype to serve as layer source."""
    game_state.layer_source_card = SubtypeCardStub(
        name="Ally Source Card",
        _subtypes={"Ally"},
    )


@given("an activated-layer is created from the ally-source card")
def create_activated_layer_from_ally_source(game_state):
    """Rule 2.10.4: Create an activated-layer from the ally-source card."""
    game_state.layer = LayerWithSubtypesStub(
        layer_category="activated-layer",
        source=game_state.layer_source_card,
    )


@when("the engine checks the subtypes of the activated-ally-layer")
def check_activated_ally_layer_subtypes(game_state):
    """Rule 2.10.4: Check the activated-ally-layer's subtypes."""
    pass


@then('the activated-ally-layer should have the "Ally" subtype')
def assert_activated_layer_has_ally(game_state):
    """Rule 2.10.4: Activated-layer inherits Ally subtype from source."""
    assert game_state.layer.has_subtype("Ally"), (
        "Engine Feature Needed: ActivatedLayer.subtypes delegates to "
        "source.subtypes (Rule 2.10.4)"
    )


# ---------------------------------------------------------------------------
# Scenario: Triggered-layer inherits subtypes from its source
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_10_subtypes.feature",
    "Triggered-layer inherits subtypes from its source",
)
def test_triggered_layer_inherits_subtypes():
    """Rule 2.10.4: Triggered-layer subtypes = source subtypes."""
    pass


@given('a card is created with the subtype "Aura" as a layer source')
def create_aura_layer_source(game_state):
    """Rule 2.10.4: Create a card with Aura subtype as layer source."""
    game_state.layer_source_card = SubtypeCardStub(
        name="Aura Source Card",
        _subtypes={"Aura"},
    )


@given("a triggered-layer is created from the aura-source card")
def create_triggered_layer_from_aura_source(game_state):
    """Rule 2.10.4: Create a triggered-layer from the aura-source card."""
    game_state.layer = LayerWithSubtypesStub(
        layer_category="triggered-layer",
        source=game_state.layer_source_card,
    )


@when("the engine checks the subtypes of the triggered-aura-layer")
def check_triggered_aura_layer_subtypes(game_state):
    """Rule 2.10.4: Check the triggered-aura-layer's subtypes."""
    pass


@then('the triggered-aura-layer should have the "Aura" subtype')
def assert_triggered_layer_has_aura(game_state):
    """Rule 2.10.4: Triggered-layer inherits Aura subtype from source."""
    assert game_state.layer.has_subtype("Aura"), (
        "Engine Feature Needed: TriggeredLayer.subtypes delegates to "
        "source.subtypes (Rule 2.10.4)"
    )


# ---------------------------------------------------------------------------
# Scenario: Layer from source with no subtypes has no subtypes
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_10_subtypes.feature",
    "Layer from source with no subtypes has no subtypes",
)
def test_layer_from_no_subtype_source():
    """Rule 2.10.4: Layer with no-subtype source has zero subtypes."""
    pass


@given("a card is created with no subtypes as a no-subtype-layer-source")
def create_no_subtype_layer_source(game_state):
    """Rule 2.10.4: Create a no-subtype card as layer source."""
    game_state.layer_source_card = SubtypeCardStub(
        name="No Subtype Source",
        _subtypes=set(),
    )


@given("an activated-layer is created from the no-subtype-layer-source card")
def create_activated_layer_from_no_subtype_source(game_state):
    """Rule 2.10.4: Create an activated-layer from no-subtype source."""
    game_state.layer = LayerWithSubtypesStub(
        layer_category="activated-layer",
        source=game_state.layer_source_card,
    )


@when("the engine checks the subtypes of the no-subtype activated-layer")
def check_no_subtype_activated_layer(game_state):
    """Rule 2.10.4: Check the no-subtype activated-layer's subtypes."""
    pass


@then("the no-subtype activated-layer should have zero subtypes")
def assert_no_subtype_layer_zero(game_state):
    """Rule 2.10.4: Layer has zero subtypes when source has none."""
    assert len(game_state.layer.subtypes) == 0, (
        "Engine Feature Needed: ActivatedLayer.subtypes returns empty set "
        "when source has no subtypes (Rule 2.10.4)"
    )


# ---------------------------------------------------------------------------
# Scenario: Object can gain a subtype from an effect
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_10_subtypes.feature",
    "Object can gain a subtype from an effect",
)
def test_object_can_gain_subtype():
    """Rule 2.10.5: Objects can gain subtypes from rules/effects."""
    pass


@given("a card is created with no subtypes", target_fixture="game_state_gain_subtype")
def create_card_no_subtypes_for_gain(game_state):
    """Rule 2.10.5: Create a no-subtype card to gain a subtype."""
    game_state.subtype_card = SubtypeCardStub(
        name="Gain Subtype Card",
        _subtypes=set(),
    )
    return game_state


@given('a gain-subtype effect grants the "Aura" subtype to the no-subtype card')
def grant_aura_subtype_to_card(game_state):
    """Rule 2.10.5: Apply an effect that grants the Aura subtype."""
    # Simulate an effect granting a subtype (Rule 2.10.5)
    game_state.subtype_card.gain_subtype("Aura")


@when("the engine checks the subtypes of the card after gaining the subtype")
def check_card_after_gaining_subtype(game_state):
    """Rule 2.10.5: Check the card's subtypes post-gain."""
    pass


@then('the card should now have the "Aura" subtype')
def assert_card_has_aura(game_state):
    """Rule 2.10.5: Card has gained the Aura subtype."""
    assert game_state.subtype_card.has_subtype("Aura"), (
        "Engine Feature Needed: CardInstance.gain_subtype('Aura') applies "
        "and CardInstance.has_subtype('Aura') -> True (Rule 2.10.5)"
    )


@then("the card should have exactly 1 subtype after gaining")
def assert_card_has_one_subtype_after_gain(game_state):
    """Rule 2.10.5: Card went from 0 to 1 subtype."""
    assert len(game_state.subtype_card.subtypes) == 1, (
        "Engine Feature Needed: CardInstance.gain_subtype() adds exactly one "
        "subtype to the card (Rule 2.10.5)"
    )


# ---------------------------------------------------------------------------
# Scenario: Object can lose a subtype from an effect
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_10_subtypes.feature",
    "Object can lose a subtype from an effect",
)
def test_object_can_lose_subtype():
    """Rule 2.10.5: Objects can lose subtypes from rules/effects."""
    pass


@given('a card is created with the subtype "Attack" and subtype "Arrow"')
def create_card_with_attack_and_arrow_for_lose(game_state):
    """Rule 2.10.5: Create a card with Attack and Arrow subtypes."""
    game_state.subtype_card = SubtypeCardStub(
        name="Arrow Attack To Lose",
        _subtypes={"Attack", "Arrow"},
    )


@given('a lose-subtype effect removes the "Arrow" subtype from the two-subtype card')
def remove_arrow_subtype_from_card(game_state):
    """Rule 2.10.5: Apply an effect that removes the Arrow subtype."""
    game_state.subtype_card.lose_subtype("Arrow")


@when("the engine checks the subtypes of the card after losing the subtype")
def check_card_after_losing_subtype(game_state):
    """Rule 2.10.5: Check the card's subtypes post-loss."""
    pass


@then('the card should no longer have the "Arrow" subtype')
def assert_card_lost_arrow(game_state):
    """Rule 2.10.5: Card no longer has Arrow after losing it."""
    assert not game_state.subtype_card.has_subtype("Arrow"), (
        "Engine Feature Needed: CardInstance.lose_subtype('Arrow') removes "
        "the subtype (Rule 2.10.5)"
    )


@then('the card should still have the "Attack" subtype')
def assert_card_kept_attack(game_state):
    """Rule 2.10.5: Card retains Attack subtype after losing Arrow."""
    assert game_state.subtype_card.has_subtype("Attack"), (
        "Engine Feature Needed: CardInstance.lose_subtype() removes only "
        "the specified subtype (Rule 2.10.5)"
    )


# ---------------------------------------------------------------------------
# Scenario: Functional subtype keywords include Attack
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_10_subtypes.feature",
    "Functional subtype keywords include Attack",
)
def test_functional_subtypes_include_attack():
    """Rule 2.10.6: Functional subtypes add additional rules."""
    pass


@given("the engine has a list of functional subtype keywords")
def engine_has_functional_keyword_list(game_state):
    """Rule 2.10.6a: The engine has the functional subtype keyword list."""
    game_state.functional_keyword_list = list(FUNCTIONAL_SUBTYPES)


@when('the engine is queried for whether "Attack" is a functional subtype keyword')
def query_if_attack_is_functional(game_state):
    """Rule 2.10.6: Query the functional subtype list."""
    game_state.subtype_check_result = SubtypeCheckResultStub.for_subtype("Attack")


@then('"Attack" should be in the functional subtype keyword list')
def assert_attack_in_functional_list(game_state):
    """Rule 2.10.6a: Attack is in the functional subtype list."""
    assert "Attack" in game_state.functional_keyword_list, (
        "Engine Feature Needed: SubtypeRegistry.FUNCTIONAL_SUBTYPES includes 'Attack' "
        "(Rule 2.10.6a)"
    )


# ---------------------------------------------------------------------------
# Scenario: All functional subtype keywords are recognized
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_10_subtypes.feature",
    "All functional subtype keywords are recognized",
)
def test_all_functional_subtypes_recognized():
    """Rule 2.10.6a: All 15 functional subtype keywords recognized."""
    pass


@given("the engine has the complete list of functional subtype keywords")
def engine_has_complete_functional_list(game_state):
    """Rule 2.10.6a: The engine has all functional subtype keywords."""
    game_state.functional_keyword_list = list(FUNCTIONAL_SUBTYPES)


@when("the engine checks each known functional subtype keyword")
def check_each_functional_keyword(game_state):
    """Rule 2.10.6a: Check all known functional subtype keywords."""
    pass


@then(parsers.parse('"{keyword}" should be a functional subtype'))
def assert_specific_functional_subtype(keyword, game_state):
    """Rule 2.10.6a: Each keyword is a functional subtype."""
    result = SubtypeCheckResultStub.for_subtype(keyword)
    assert result.is_functional, (
        f"Engine Feature Needed: SubtypeRegistry.is_functional('{keyword}') -> True "
        f"(Rule 2.10.6a)"
    )


# ---------------------------------------------------------------------------
# Scenario: Non-functional subtype keywords include common weapon subtypes
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_10_subtypes.feature",
    "Non-functional subtype keywords include common weapon subtypes",
)
def test_non_functional_subtypes_recognized():
    """Rule 2.10.6b: Non-functional subtype keywords recognized."""
    pass


@given("the engine has the complete list of non-functional subtype keywords")
def engine_has_non_functional_list(game_state):
    """Rule 2.10.6b: The engine has non-functional subtype keywords."""
    game_state.non_functional_keyword_list = list(NON_FUNCTIONAL_SUBTYPES)


@when("the engine checks each known non-functional subtype keyword")
def check_each_non_functional_keyword(game_state):
    """Rule 2.10.6b: Check known non-functional subtype keywords."""
    pass


@then(parsers.parse('"{keyword}" should be a non-functional subtype'))
def assert_specific_non_functional_subtype(keyword, game_state):
    """Rule 2.10.6b: Each keyword is a non-functional subtype."""
    result = SubtypeCheckResultStub.for_subtype(keyword)
    assert not result.is_functional, (
        f"Engine Feature Needed: SubtypeRegistry.is_functional('{keyword}') -> False "
        f"(Rule 2.10.6b)"
    )


# ---------------------------------------------------------------------------
# Scenario: There are exactly 15 functional subtype keywords
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_10_subtypes.feature",
    "There are exactly 15 functional subtype keywords",
)
def test_exactly_15_functional_subtypes():
    """Rule 2.10.6a: The functional subtype list has exactly 15 keywords."""
    pass


@given(
    "the engine has the complete list of functional subtype keywords",
    target_fixture="functional_list_context",
)
def engine_has_functional_list_for_count(game_state):
    """Rule 2.10.6a: The engine has the functional subtype list for counting."""
    game_state.functional_keyword_list = list(FUNCTIONAL_SUBTYPES)
    return game_state


@when("the engine counts all functional subtype keywords")
def count_functional_keywords(game_state):
    """Rule 2.10.6a: Count the functional subtype keywords."""
    game_state.functional_subtype_count = len(game_state.functional_keyword_list)


@then("there should be exactly 15 functional subtype keywords")
def assert_exactly_15_functional(game_state):
    """Rule 2.10.6a: Exactly 15 functional subtypes (1H, 2H, Affliction, Ally,
    Arrow, Ash, Attack, Aura, Construct, Figment, Invocation, Item, Landmark,
    Off-Hand, Quiver)."""
    assert game_state.functional_subtype_count == 15, (
        f"Engine Feature Needed: SubtypeRegistry.FUNCTIONAL_SUBTYPES has exactly 15 "
        f"entries (Rule 2.10.6a). Got {game_state.functional_subtype_count}"
    )


# ---------------------------------------------------------------------------
# Scenario: Attack subtype adds functional rules to a card
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_10_subtypes.feature",
    "Attack subtype adds functional rules to a card",
)
def test_attack_subtype_is_functional():
    """Rule 2.10.6a: Attack is a functional subtype."""
    pass


@given('a card is created with the subtype "Attack" as the functional-attack card')
def create_functional_attack_card(game_state):
    """Rule 2.10.6a: Create a card with Attack as functional subtype."""
    game_state.subtype_card = SubtypeCardStub(
        name="Functional Attack Card",
        _subtypes={"Attack"},
    )


@when("the engine checks whether the functional-attack card's subtype adds rules")
def check_if_attack_adds_rules(game_state):
    """Rule 2.10.6: Check whether the Attack subtype adds additional rules."""
    game_state.subtype_adds_rules = SubtypeCheckResultStub.for_subtype("Attack")


@then("the functional-attack-subtype should add additional rules")
def assert_attack_adds_rules(game_state):
    """Rule 2.10.6: Attack subtype adds additional rules to the card."""
    assert game_state.subtype_adds_rules.adds_additional_rules, (
        "Engine Feature Needed: SubtypeRegistry.is_functional('Attack') -> True, "
        "which means it adds additional rules (Rule 2.10.6)"
    )


@then('the "Attack" subtype should be functional')
def assert_attack_is_functional_in_context(game_state):
    """Rule 2.10.6a: Attack is confirmed as a functional subtype."""
    assert game_state.subtype_adds_rules.is_functional, (
        "Engine Feature Needed: SubtypeRegistry.is_functional('Attack') -> True "
        "(Rule 2.10.6a)"
    )


# ---------------------------------------------------------------------------
# Scenario: Sword subtype does not add functional rules to a card
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_10_subtypes.feature",
    "Sword subtype does not add functional rules to a card",
)
def test_sword_subtype_is_non_functional():
    """Rule 2.10.6b: Sword is a non-functional subtype."""
    pass


@given('a card is created with the subtype "Sword" as the non-functional-sword card')
def create_non_functional_sword_card(game_state):
    """Rule 2.10.6b: Create a card with Sword as non-functional subtype."""
    game_state.subtype_card = SubtypeCardStub(
        name="Sword Card Non-Functional",
        _subtypes={"Sword"},
    )


@when("the engine checks whether the non-functional-sword card's subtype adds rules")
def check_if_sword_adds_rules(game_state):
    """Rule 2.10.6: Check whether the Sword subtype adds rules."""
    game_state.subtype_adds_rules = SubtypeCheckResultStub.for_subtype("Sword")


@then("the non-functional-sword-subtype should not add additional rules")
def assert_sword_no_additional_rules(game_state):
    """Rule 2.10.6b: Sword subtype does not add additional rules."""
    assert not game_state.subtype_adds_rules.adds_additional_rules, (
        "Engine Feature Needed: SubtypeRegistry.is_functional('Sword') -> False "
        "(Rule 2.10.6b)"
    )


# ---------------------------------------------------------------------------
# Scenario: A card can have both functional and non-functional subtypes
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_10_subtypes.feature",
    "A card can have both functional and non-functional subtypes",
)
def test_card_can_have_both_functional_and_non_functional_subtypes():
    """Rule 2.10.6: Cards can have both functional and non-functional subtypes."""
    pass


@given('a card is created with subtypes "Attack" and "Sword"')
def create_card_with_attack_and_sword(game_state):
    """Rule 2.10.6: Create a card with both Attack (functional) and Sword (non-functional)."""
    game_state.subtype_card = SubtypeCardStub(
        name="Attack Sword Card",
        _subtypes={"Attack", "Sword"},
    )


@when("the engine checks the subtypes of the attack-and-sword card")
def check_attack_and_sword_card(game_state):
    """Rule 2.10.6: Check the mixed-subtype card's subtypes."""
    pass


@then('the attack-and-sword card should have the "Attack" subtype')
def assert_attack_and_sword_has_attack(game_state):
    """Rule 2.10.6: Card has Attack subtype."""
    assert game_state.subtype_card.has_subtype("Attack"), (
        "Engine Feature Needed: CardInstance.has_subtype('Attack') -> True (Rule 2.10.6)"
    )


@then('the attack-and-sword card should have the "Sword" subtype')
def assert_attack_and_sword_has_sword(game_state):
    """Rule 2.10.6: Card has Sword subtype."""
    assert game_state.subtype_card.has_subtype("Sword"), (
        "Engine Feature Needed: CardInstance.has_subtype('Sword') -> True (Rule 2.10.6)"
    )


@then(
    'the functional subtypes of the attack-and-sword card should include only "Attack"'
)
def assert_only_attack_is_functional(game_state):
    """Rule 2.10.6: Only Attack is functional; Sword is not."""
    functional = game_state.subtype_card.functional_subtypes
    assert functional == {"Attack"}, (
        f"Engine Feature Needed: CardInstance.functional_subtypes returns only "
        f"functional ones. Expected {{'Attack'}}, got {functional} (Rule 2.10.6)"
    )


# ---------------------------------------------------------------------------
# Scenario: Layer inherits multiple subtypes from source card
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_10_subtypes.feature",
    "Layer inherits multiple subtypes from source card",
)
def test_layer_inherits_multiple_subtypes():
    """Rule 2.10.4: Layer inherits all subtypes from multi-subtype source."""
    pass


@given('a card is created with subtypes "Attack" and "Arrow" as an arrow-attack-source')
def create_arrow_attack_source(game_state):
    """Rule 2.10.4: Create a card with Attack and Arrow as layer source."""
    game_state.layer_source_card = SubtypeCardStub(
        name="Arrow Attack Source",
        _subtypes={"Attack", "Arrow"},
    )


@given("an activated-layer is created from the arrow-attack-source card")
def create_activated_layer_from_arrow_attack_source(game_state):
    """Rule 2.10.4: Create an activated-layer from the arrow-attack source."""
    game_state.layer = LayerWithSubtypesStub(
        layer_category="activated-layer",
        source=game_state.layer_source_card,
    )


@when("the engine checks the subtypes of the arrow-attack activated-layer")
def check_arrow_attack_activated_layer(game_state):
    """Rule 2.10.4: Check the multi-subtype layer's subtypes."""
    pass


@then('the arrow-attack activated-layer should have the "Attack" subtype')
def assert_arrow_attack_layer_has_attack(game_state):
    """Rule 2.10.4: Layer inherits Attack subtype from source."""
    assert game_state.layer.has_subtype("Attack"), (
        "Engine Feature Needed: ActivatedLayer.subtypes delegates to source.subtypes; "
        "includes 'Attack' (Rule 2.10.4)"
    )


@then('the arrow-attack activated-layer should have the "Arrow" subtype')
def assert_arrow_attack_layer_has_arrow(game_state):
    """Rule 2.10.4: Layer inherits Arrow subtype from source."""
    assert game_state.layer.has_subtype("Arrow"), (
        "Engine Feature Needed: ActivatedLayer.subtypes delegates to source.subtypes; "
        "includes 'Arrow' (Rule 2.10.4)"
    )
