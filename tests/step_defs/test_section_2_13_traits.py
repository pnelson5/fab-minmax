"""
Step definitions for Section 2.13: Traits
Reference: Flesh and Blood Comprehensive Rules Section 2.13

This module implements behavioral tests for the traits property of objects
in Flesh and Blood.

Rule 2.13.1: Trait is a property of an object, which represents one of its
             object identities. [1.2.2]

Rule 2.13.2: The printed traits of a card are typically located at the top of
             the card, under the card name. The printed traits define the
             traits of a card.

Rule 2.13.3: Traits are non-functional keywords or phrases and do not add
             additional rules to an object.

Rule 2.13.3a: The trait keywords and phrases are Agents of Chaos.

Rule 2.13.4: If an effect refers to a group of cards by a trait, it refers to
             all cards with that trait.

             Example: Arakni, Web of Deceit has the text "At the beginning of
             your end phase, if an opponent is marked, you become a random
             Agent of Chaos." This refers to a group which includes all cards
             with the Agent of Chaos trait, and selecting one at random from
             that group.

Engine Features Needed for Section 2.13:
- [ ] `CardInstance.traits` property returning a set/frozenset of trait strings (Rule 2.13.2)
- [ ] `CardTemplate.traits` returning the printed traits (Rule 2.13.2)
- [ ] `CardInstance.has_trait(name)` method (Rule 2.13.1)
- [ ] `CardInstance.get_object_identities()` includes trait strings (Rule 2.13.1, cross-ref 1.2.2)
- [ ] `TraitRegistry.TRAIT_KEYWORDS` frozenset containing only "Agents of Chaos" (Rule 2.13.3a)
- [ ] `TraitRegistry.is_non_functional(name)` = True always (Rule 2.13.3)
- [ ] `TraitRegistry.adds_additional_rules(name)` = False always (Rule 2.13.3)
- [ ] `TraitGroupEffect.get_group(trait_name)` collecting all objects with the trait (Rule 2.13.4)
"""

import pytest
from pytest_bdd import scenario, given, when, then, parsers
from dataclasses import dataclass, field
from typing import Optional, List, Set
import random


# ---------------------------------------------------------------------------
# Stub classes for testing Section 2.13 rules
# ---------------------------------------------------------------------------


# Rule 2.13.3a: The only defined trait keyword
AGENTS_OF_CHAOS = "Agents of Chaos"
DEFINED_TRAIT_KEYWORDS = frozenset({AGENTS_OF_CHAOS})


@dataclass
class TraitCardStub:
    """
    Stub representing a card with traits.

    Models what the engine must implement for Section 2.13.

    Engine Features Needed:
    - [ ] CardTemplate.traits: frozenset[str] — printed traits (Rule 2.13.2)
    - [ ] CardInstance.traits: frozenset[str] — resolved traits (Rule 2.13.2)
    - [ ] CardInstance.has_trait(name): bool (Rule 2.13.1)
    - [ ] CardInstance.get_object_identities(): includes trait names (Rule 2.13.1)
    """

    name: str = "Test Card"
    _printed_traits: frozenset = field(default_factory=frozenset)

    @property
    def traits(self) -> frozenset:
        """Rule 2.13.2: Printed traits define the traits of a card."""
        return self._printed_traits

    @property
    def base_traits(self) -> frozenset:
        """Rule 2.13.2: Base traits as defined by printed text."""
        return self._printed_traits

    def has_trait(self, name: str) -> bool:
        """Rule 2.13.1: Check whether the card has a given trait."""
        return name in self._printed_traits

    def get_object_identities(self) -> Set[str]:
        """
        Rule 2.13.1 + Rule 1.2.2: Traits are object identities.

        Engine Feature Needed:
        - [ ] CardInstance.get_object_identities() includes trait strings (Rule 2.13.1)
        """
        identities = {"object", "card", self.name}
        # Rule 2.13.1: traits represent object identities
        identities.update(self._printed_traits)
        return identities

    @property
    def has_traits_property(self) -> bool:
        """Rule 2.13.1: Whether the card has a traits property."""
        # All cards have a traits property (possibly empty)
        return True


@dataclass
class TraitCheckResultStub:
    """
    Result of checking trait-related properties.

    Engine Features Needed:
    - [ ] TraitRegistry.is_non_functional(name): bool (Rule 2.13.3)
    - [ ] TraitRegistry.adds_additional_rules(name): bool (Rule 2.13.3)
    - [ ] TraitRegistry.TRAIT_KEYWORDS: frozenset (Rule 2.13.3a)
    """

    trait_name: str = ""

    def is_non_functional(self) -> bool:
        """
        Rule 2.13.3: Traits are non-functional keywords.

        Engine Feature Needed:
        - [ ] TraitRegistry.is_non_functional(name) -> True always (Rule 2.13.3)
        """
        return True

    def adds_additional_rules(self) -> bool:
        """
        Rule 2.13.3: Traits do not add additional rules.

        Engine Feature Needed:
        - [ ] TraitRegistry.adds_additional_rules(name) -> False always (Rule 2.13.3)
        """
        return False


def get_all_trait_keywords() -> frozenset:
    """
    Rule 2.13.3a: Return all defined trait keywords.

    Engine Feature Needed:
    - [ ] TraitRegistry.TRAIT_KEYWORDS frozenset containing only "Agents of Chaos"
    """
    return DEFINED_TRAIT_KEYWORDS


@dataclass
class TraitGroupEffectStub:
    """
    Stub representing an effect that targets a group of cards by trait.

    Engine Features Needed:
    - [ ] TraitGroupEffect.get_group(trait_name, objects) -> List[object] (Rule 2.13.4)
    """

    target_trait: str = ""
    _candidates: List[TraitCardStub] = field(default_factory=list)

    def get_group(self) -> List[TraitCardStub]:
        """
        Rule 2.13.4: Return all cards in the arena that have the target trait.

        Engine Feature Needed:
        - [ ] TraitGroupEffect.get_group(trait_name) collecting all objects with the trait
        """
        return [c for c in self._candidates if c.has_trait(self.target_trait)]

    def select_random(self) -> Optional[TraitCardStub]:
        """
        Rule 2.13.4 (Arakni example): Select a random card from the trait group.

        Engine Feature Needed:
        - [ ] TraitGroupEffect.select_random() -> optional card from the group
        """
        group = self.get_group()
        if not group:
            return None
        return random.choice(group)


# ---------------------------------------------------------------------------
# Scenario: Trait is a property of an object representing its identity
# Tests Rule 2.13.1
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_13_traits.feature",
    "Trait is a property of an object representing its identity",
)
def test_trait_is_property_representing_object_identity():
    """Rule 2.13.1: Trait is a property representing an object identity."""
    pass


@given('a card with the trait "Agents of Chaos"')
def card_with_agents_of_chaos_trait(game_state):
    """Rule 2.13.2: Printed traits define the traits of a card."""
    game_state.trait_card = TraitCardStub(
        name="Arakni, Web of Deceit",
        _printed_traits=frozenset({AGENTS_OF_CHAOS}),
    )


@when("the engine reads the card's traits")
def engine_reads_card_traits(game_state):
    """Rule 2.13.2: Engine reads the traits from the card."""
    game_state.read_traits = game_state.trait_card.traits


@then('the card has the trait "Agents of Chaos"')
def card_has_agents_of_chaos(game_state):
    """Rule 2.13.1: Verify card has the Agents of Chaos trait."""
    assert game_state.trait_card.has_trait(AGENTS_OF_CHAOS), (
        f"Expected card to have trait '{AGENTS_OF_CHAOS}', "
        f"but traits were: {game_state.trait_card.traits}"
    )


@then('"Agents of Chaos" is an object identity of the card')
def agents_of_chaos_is_object_identity(game_state):
    """Rule 2.13.1 + Rule 1.2.2: Trait is an object identity."""
    identities = game_state.trait_card.get_object_identities()
    assert AGENTS_OF_CHAOS in identities, (
        f"Expected '{AGENTS_OF_CHAOS}' in object identities, "
        f"but identities were: {identities}"
    )


# ---------------------------------------------------------------------------
# Scenario: Trait is recognized as an object property
# Tests Rule 2.13.1
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_13_traits.feature",
    "Trait is recognized as an object property",
)
def test_trait_is_recognized_as_object_property():
    """Rule 2.13.1: Trait is a recognized property of objects."""
    pass


@when("the engine reads the card's properties")
def engine_reads_card_properties(game_state):
    """Rule 2.13.1: Engine reads the card's properties."""
    game_state.card_has_traits_property = game_state.trait_card.has_traits_property


@then("the card has a traits property")
def card_has_traits_property(game_state):
    """Rule 2.13.1: Card has a traits property (may be empty set)."""
    assert game_state.card_has_traits_property, (
        "Expected card to have a traits property"
    )


@then('the traits property contains "Agents of Chaos"')
def traits_property_contains_agents_of_chaos(game_state):
    """Rule 2.13.2: The traits property contains the Agents of Chaos trait."""
    assert AGENTS_OF_CHAOS in game_state.trait_card.traits, (
        f"Expected traits property to contain '{AGENTS_OF_CHAOS}'"
    )


# ---------------------------------------------------------------------------
# Scenario: Card without a trait has no trait object identity
# Tests Rule 2.13.1 (no traits = no trait identities)
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_13_traits.feature",
    "Card without a trait has no trait object identity",
)
def test_card_without_trait_has_no_trait_identity():
    """Rule 2.13.1: Cards with no traits have no trait-based object identities."""
    pass


@given("a card with no printed traits")
def card_with_no_printed_traits(game_state):
    """Rule 2.13.2: Card with no printed traits."""
    game_state.trait_card = TraitCardStub(
        name="Pummel",
        _printed_traits=frozenset(),
    )


@then("the card has zero traits")
def card_has_zero_traits(game_state):
    """Rule 2.13.2: Card with no printed traits has zero traits."""
    assert len(game_state.trait_card.traits) == 0, (
        f"Expected 0 traits, but found: {game_state.trait_card.traits}"
    )


@then("no trait appears in the card's object identities")
def no_trait_in_object_identities(game_state):
    """Rule 2.13.1: No traits means no trait object identities."""
    identities = game_state.trait_card.get_object_identities()
    # Verify none of the defined trait keywords appear in identities
    for keyword in DEFINED_TRAIT_KEYWORDS:
        assert keyword not in identities, (
            f"Expected no trait keywords in identities, but found '{keyword}': {identities}"
        )


# ---------------------------------------------------------------------------
# Scenario: Printed traits define the card traits
# Tests Rule 2.13.2
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_13_traits.feature",
    "Printed traits define the card traits",
)
def test_printed_traits_define_card_traits():
    """Rule 2.13.2: Printed traits define the traits of a card."""
    pass


@given('a card whose printed traits include "Agents of Chaos"')
def card_with_printed_agents_of_chaos(game_state):
    """Rule 2.13.2: Card with Agents of Chaos as a printed trait."""
    game_state.trait_card = TraitCardStub(
        name="Arakni",
        _printed_traits=frozenset({AGENTS_OF_CHAOS}),
    )


@when("the engine reads the printed traits")
def engine_reads_printed_traits(game_state):
    """Rule 2.13.2: Engine reads the printed trait definitions."""
    game_state.base_traits = game_state.trait_card.base_traits


@then('the base traits of the card include "Agents of Chaos"')
def base_traits_include_agents_of_chaos(game_state):
    """Rule 2.13.2: Base traits determined by printed traits."""
    assert AGENTS_OF_CHAOS in game_state.base_traits, (
        f"Expected base traits to include '{AGENTS_OF_CHAOS}', "
        f"but base traits were: {game_state.base_traits}"
    )


# ---------------------------------------------------------------------------
# Scenario: Card can have exactly one printed trait
# Tests Rule 2.13.2
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_13_traits.feature",
    "Card can have exactly one printed trait",
)
def test_card_can_have_exactly_one_trait():
    """Rule 2.13.2: Card can have exactly one printed trait."""
    pass


@given('a card with exactly one printed trait "Agents of Chaos"')
def card_with_exactly_one_trait(game_state):
    """Rule 2.13.2: Card with exactly one printed trait."""
    game_state.trait_card = TraitCardStub(
        name="Arakni, Huntsman",
        _printed_traits=frozenset({AGENTS_OF_CHAOS}),
    )


@when("the engine counts the card's traits")
def engine_counts_card_traits(game_state):
    """Rule 2.13.2: Engine counts the number of traits."""
    game_state.trait_count = len(game_state.trait_card.traits)


@then("the card has exactly 1 trait")
def card_has_exactly_one_trait(game_state):
    """Rule 2.13.2: Exactly one trait."""
    assert game_state.trait_count == 1, (
        f"Expected exactly 1 trait, but found {game_state.trait_count}"
    )


# ---------------------------------------------------------------------------
# Scenario: Card can have zero traits
# Tests Rule 2.13.2
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_13_traits.feature",
    "Card can have zero traits",
)
def test_card_can_have_zero_traits():
    """Rule 2.13.2: Card can have zero printed traits."""
    pass


@then("the card has exactly 0 traits")
def card_has_exactly_zero_traits(game_state):
    """Rule 2.13.2: Zero traits."""
    assert game_state.trait_count == 0, (
        f"Expected exactly 0 traits, but found {game_state.trait_count}"
    )


# ---------------------------------------------------------------------------
# Scenario: Traits are non-functional and do not add additional rules
# Tests Rule 2.13.3
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_13_traits.feature",
    "Traits are non-functional and do not add additional rules",
)
def test_traits_are_non_functional():
    """Rule 2.13.3: Traits are non-functional and add no additional rules."""
    pass


@when("the engine evaluates whether traits add additional rules")
def engine_evaluates_trait_functionality(game_state):
    """Rule 2.13.3: Engine checks if traits add additional rules."""
    game_state.trait_check = TraitCheckResultStub(trait_name=AGENTS_OF_CHAOS)


@then('the trait "Agents of Chaos" is non-functional')
def agents_of_chaos_is_non_functional(game_state):
    """Rule 2.13.3: Agents of Chaos is non-functional."""
    assert game_state.trait_check.is_non_functional(), (
        f"Expected trait '{AGENTS_OF_CHAOS}' to be non-functional"
    )


@then("the trait does not add additional rules to the card")
def trait_does_not_add_rules(game_state):
    """Rule 2.13.3: Non-functional trait adds no rules."""
    assert not game_state.trait_check.adds_additional_rules(), (
        f"Expected trait '{AGENTS_OF_CHAOS}' to add no additional rules"
    )


# ---------------------------------------------------------------------------
# Scenario: Non-functional trait has no gameplay effect on its own
# Tests Rule 2.13.3
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_13_traits.feature",
    "Non-functional trait has no gameplay effect on its own",
)
def test_non_functional_trait_no_gameplay_effect():
    """Rule 2.13.3: Non-functional traits don't change gameplay rules."""
    pass


@given("a card with no traits")
def card_with_no_traits(game_state):
    """Rule 2.13.2: Card with no traits."""
    game_state.no_trait_card = TraitCardStub(
        name="Pummel",
        _printed_traits=frozenset(),
    )


@when("both cards are evaluated for additional rules added by traits")
def evaluate_both_cards_for_trait_rules(game_state):
    """Rule 2.13.3: Evaluate whether traits add rules to either card."""
    no_trait_check = TraitCheckResultStub(trait_name="none")
    with_trait_check = TraitCheckResultStub(trait_name=AGENTS_OF_CHAOS)
    game_state.no_trait_adds_rules = no_trait_check.adds_additional_rules()
    game_state.with_trait_adds_rules = with_trait_check.adds_additional_rules()


@then("neither card gains additional rules from traits")
def neither_card_gains_additional_rules(game_state):
    """Rule 2.13.3: Neither card with nor without traits gains additional rules."""
    assert not game_state.no_trait_adds_rules, (
        "Expected no-trait card to gain no additional rules"
    )
    assert not game_state.with_trait_adds_rules, (
        f"Expected '{AGENTS_OF_CHAOS}' trait card to gain no additional rules"
    )


# ---------------------------------------------------------------------------
# Scenario: Agents of Chaos is a recognized trait keyword
# Tests Rule 2.13.3a
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_13_traits.feature",
    "Agents of Chaos is a recognized trait keyword",
)
def test_agents_of_chaos_is_recognized_trait_keyword():
    """Rule 2.13.3a: The trait keywords and phrases are Agents of Chaos."""
    pass


@given('the trait keyword "Agents of Chaos"')
def the_trait_keyword_agents_of_chaos(game_state):
    """Rule 2.13.3a: Reference to the Agents of Chaos trait keyword."""
    game_state.queried_trait = AGENTS_OF_CHAOS


@when("the engine checks the recognized trait keywords")
def engine_checks_recognized_trait_keywords(game_state):
    """Rule 2.13.3a: Engine retrieves the set of recognized trait keywords."""
    game_state.recognized_traits = get_all_trait_keywords()


@then('"Agents of Chaos" is a valid trait keyword')
def agents_of_chaos_is_valid_trait_keyword(game_state):
    """Rule 2.13.3a: Agents of Chaos recognized as a valid trait keyword."""
    assert AGENTS_OF_CHAOS in game_state.recognized_traits, (
        f"Expected '{AGENTS_OF_CHAOS}' to be in recognized trait keywords"
    )


@then("the total number of defined trait keywords is 1")
def total_trait_keywords_is_one(game_state):
    """Rule 2.13.3a: Only Agents of Chaos is defined as a trait keyword."""
    count = len(game_state.recognized_traits)
    assert count == 1, (
        f"Expected exactly 1 trait keyword, but found {count}: {game_state.recognized_traits}"
    )


# ---------------------------------------------------------------------------
# Scenario: Effect using a trait refers to all cards with that trait
# Tests Rule 2.13.4
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_13_traits.feature",
    "Effect using a trait refers to all cards with that trait",
)
def test_effect_refers_to_all_cards_with_trait():
    """Rule 2.13.4: Effect targeting by trait collects all matching cards."""
    pass


@given("a group of cards in the arena")
def a_group_of_cards_in_the_arena(game_state):
    """Set up a group of cards representing the arena."""
    game_state.arena_cards = []


@given('one card has the trait "Agents of Chaos"')
def one_card_has_agents_of_chaos_trait(game_state):
    """Rule 2.13.2: One card in arena has the trait."""
    game_state.agent_card = TraitCardStub(
        name="Arakni, Huntsman",
        _printed_traits=frozenset({AGENTS_OF_CHAOS}),
    )
    game_state.arena_cards.append(game_state.agent_card)


@given('another card does not have the trait "Agents of Chaos"')
def another_card_does_not_have_agents_of_chaos(game_state):
    """Rule 2.13.4: One card without the trait for contrast."""
    game_state.non_agent_card = TraitCardStub(
        name="Pummel",
        _printed_traits=frozenset(),
    )
    game_state.arena_cards.append(game_state.non_agent_card)


@when('an effect targets "all cards with the Agents of Chaos trait"')
def effect_targets_all_agents_of_chaos(game_state):
    """Rule 2.13.4: Effect collects all cards with the Agents of Chaos trait."""
    effect = TraitGroupEffectStub(
        target_trait=AGENTS_OF_CHAOS,
        _candidates=game_state.arena_cards,
    )
    game_state.trait_group = effect.get_group()


@then('only the card with the trait "Agents of Chaos" is in the target group')
def only_agent_card_in_target_group(game_state):
    """Rule 2.13.4: Only cards with the trait are in the group."""
    assert game_state.agent_card in game_state.trait_group, (
        "Expected the Agents of Chaos card to be in the target group"
    )
    assert len(game_state.trait_group) == 1, (
        f"Expected exactly 1 card in trait group, but found {len(game_state.trait_group)}"
    )


@then("the card without the trait is not in the target group")
def non_agent_card_not_in_target_group(game_state):
    """Rule 2.13.4: Cards without the trait are excluded from the group."""
    assert game_state.non_agent_card not in game_state.trait_group, (
        "Expected the non-Agents of Chaos card to NOT be in the target group"
    )


# ---------------------------------------------------------------------------
# Scenario: Effect selects a random card from the Agents of Chaos group
# Tests Rule 2.13.4 (Arakni, Web of Deceit example)
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_13_traits.feature",
    "Effect selects a random card from the Agents of Chaos group",
)
def test_effect_selects_random_card_from_agents_group():
    """Rule 2.13.4: Random selection from the Agents of Chaos group (Arakni example)."""
    pass


@given('multiple cards each with the trait "Agents of Chaos"')
def multiple_cards_with_agents_of_chaos(game_state):
    """Rule 2.13.4: Multiple Agents of Chaos cards for random selection."""
    game_state.agent_cards = [
        TraitCardStub(
            name="Arakni, Huntsman", _printed_traits=frozenset({AGENTS_OF_CHAOS})
        ),
        TraitCardStub(
            name="Arakni, Web of Deceit", _printed_traits=frozenset({AGENTS_OF_CHAOS})
        ),
        TraitCardStub(name="Arakni", _printed_traits=frozenset({AGENTS_OF_CHAOS})),
    ]


@when('an effect selects a random "Agent of Chaos" card from the group')
def effect_selects_random_agent_of_chaos(game_state):
    """Rule 2.13.4: Effect randomly selects one card from the trait group."""
    effect = TraitGroupEffectStub(
        target_trait=AGENTS_OF_CHAOS,
        _candidates=game_state.agent_cards,
    )
    game_state.selected_card = effect.select_random()


@then('the selected card has the trait "Agents of Chaos"')
def selected_card_has_agents_of_chaos(game_state):
    """Rule 2.13.4: The randomly selected card must have the trait."""
    assert game_state.selected_card is not None, (
        "Expected a card to be selected, but got None"
    )
    assert game_state.selected_card.has_trait(AGENTS_OF_CHAOS), (
        f"Expected selected card to have trait '{AGENTS_OF_CHAOS}'"
    )


@then("the selected card is one of the cards in the Agents of Chaos group")
def selected_card_is_in_agents_group(game_state):
    """Rule 2.13.4: Selected card comes from the correct group."""
    assert game_state.selected_card in game_state.agent_cards, (
        "Expected selected card to be one of the Agents of Chaos candidates"
    )


# ---------------------------------------------------------------------------
# Scenario: Effect targets empty group when no cards have the trait
# Tests Rule 2.13.4 (edge case: empty group)
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_13_traits.feature",
    "Effect targets empty group when no cards have the trait",
)
def test_effect_targets_empty_group_when_no_cards_have_trait():
    """Rule 2.13.4: Empty group when no arena cards have the trait."""
    pass


@given("a group of cards in the arena with no Agents of Chaos trait")
def arena_cards_with_no_agents_of_chaos(game_state):
    """Rule 2.13.4: Arena cards that have no Agents of Chaos trait."""
    game_state.arena_cards = [
        TraitCardStub(name="Pummel", _printed_traits=frozenset()),
        TraitCardStub(name="Lunging Press", _printed_traits=frozenset()),
    ]


@then("the target group is empty")
def target_group_is_empty(game_state):
    """Rule 2.13.4: No cards in group when none have the trait."""
    assert len(game_state.trait_group) == 0, (
        f"Expected empty target group, but found {len(game_state.trait_group)} cards"
    )


# ---------------------------------------------------------------------------
# Scenario: Trait contributes to object identity alongside name
# Tests Rule 2.13.1 cross-ref Rule 1.2.2b
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_13_traits.feature",
    "Trait contributes to object identity alongside name",
)
def test_trait_contributes_to_object_identity_alongside_name():
    """Rule 2.13.1 + Rule 1.2.2b: Trait is an object identity alongside name."""
    pass


@given('a card named "Test Agent" with the trait "Agents of Chaos"')
def card_named_test_agent_with_trait(game_state):
    """Rule 2.13.1: Named card with trait."""
    game_state.trait_card = TraitCardStub(
        name="Test Agent",
        _printed_traits=frozenset({AGENTS_OF_CHAOS}),
    )


@when("the engine retrieves all object identities of the card")
def engine_retrieves_all_object_identities(game_state):
    """Rule 2.13.1 + Rule 1.2.2: Engine collects all object identities."""
    game_state.object_identities = game_state.trait_card.get_object_identities()


@then('the object identities include "Agents of Chaos"')
def object_identities_include_agents_of_chaos(game_state):
    """Rule 2.13.1: Trait is in the object identities."""
    assert AGENTS_OF_CHAOS in game_state.object_identities, (
        f"Expected object identities to include '{AGENTS_OF_CHAOS}', "
        f"but identities were: {game_state.object_identities}"
    )


@then('the object identities also include "Test Agent"')
def object_identities_also_include_name(game_state):
    """Rule 1.2.2b: Card name is also an object identity."""
    assert "Test Agent" in game_state.object_identities, (
        f"Expected object identities to include 'Test Agent', "
        f"but identities were: {game_state.object_identities}"
    )


# ---------------------------------------------------------------------------
# Scenario: Multiple card instances with same trait all belong to the trait group
# Tests Rule 2.13.4 (all matching cards included)
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_13_traits.feature",
    "Multiple card instances with same trait all belong to the trait group",
)
def test_multiple_card_instances_with_same_trait_in_group():
    """Rule 2.13.4: All cards with the same trait appear in the trait group."""
    pass


@given('three cards each with the trait "Agents of Chaos"')
def three_cards_each_with_agents_of_chaos(game_state):
    """Rule 2.13.4: Three cards each having the Agents of Chaos trait."""
    game_state.arena_cards = [
        TraitCardStub(name="Arakni A", _printed_traits=frozenset({AGENTS_OF_CHAOS})),
        TraitCardStub(name="Arakni B", _printed_traits=frozenset({AGENTS_OF_CHAOS})),
        TraitCardStub(name="Arakni C", _printed_traits=frozenset({AGENTS_OF_CHAOS})),
    ]


@when('an effect targets all cards with the trait "Agents of Chaos"')
def effect_targets_all_cards_with_agents_of_chaos(game_state):
    """Rule 2.13.4: Effect targets all cards with the Agents of Chaos trait."""
    effect = TraitGroupEffectStub(
        target_trait=AGENTS_OF_CHAOS,
        _candidates=game_state.arena_cards,
    )
    game_state.trait_group = effect.get_group()


@then("all three cards are in the target group")
def all_three_cards_in_target_group(game_state):
    """Rule 2.13.4: All cards with the trait are in the group."""
    assert len(game_state.trait_group) == 3, (
        f"Expected all 3 cards in trait group, but found {len(game_state.trait_group)}"
    )
    for card in game_state.arena_cards:
        assert card in game_state.trait_group, (
            f"Expected card '{card.name}' to be in the target group"
        )


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def game_state():
    """
    Fixture providing game state for testing Section 2.13 rules.

    Uses a simple namespace object to hold test state.
    Reference: Rule 2.13
    """
    from tests.bdd_helpers import BDDGameState

    state = BDDGameState()

    # Initialize trait-related state
    state.trait_card = None
    state.no_trait_card = None
    state.agent_card = None
    state.non_agent_card = None
    state.agent_cards = []
    state.arena_cards = []
    state.trait_group = []
    state.selected_card = None
    state.object_identities = set()
    state.read_traits = frozenset()
    state.base_traits = frozenset()
    state.trait_count = 0
    state.recognized_traits = frozenset()
    state.queried_trait = ""
    state.card_has_traits_property = False
    state.no_trait_adds_rules = False
    state.with_trait_adds_rules = False
    state.trait_check = None

    return state
