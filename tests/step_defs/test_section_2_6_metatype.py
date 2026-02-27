"""
Step definitions for Section 2.6: Metatype
Reference: Flesh and Blood Comprehensive Rules Section 2.6

This module implements behavioral tests for metatype rules in Flesh and Blood.

Rule 2.6.1: Metatypes are a collection of metatype keywords. The metatypes of
            an object determine whether it may be added to a game.

Rule 2.6.2: An object can have zero or more metatypes.

Rule 2.6.3: The metatype of a card is determined by its type box. The metatype
            is printed before the card's supertypes.

Rule 2.6.4: The metatypes of an activated-layer or triggered-layer are the
            same as the metatypes of its source.

Rule 2.6.5: An object cannot gain or lose metatypes.

Rule 2.6.6: Metatypes are either hero-metatypes or set-metatypes.
            Hero-metatypes specify the moniker(s) of a hero, and the card can
            only be included in a player's card-pool if it matches their hero's
            moniker(s). Set-metatypes specify the name(s) of the set the object
            can be used in as defined by tournament rules.

Engine Features Needed for Section 2.6:
- [ ] CardTemplate.metatypes property: frozenset of metatype keywords (Rule 2.6.1)
- [ ] MetatypeKeyword class (or enum) with hero-metatype and set-metatype variants (Rule 2.6.6)
- [ ] CardTemplate.has_metatype(keyword) method (Rules 2.6.2, 2.6.3)
- [ ] Layer.metatypes property inheriting from source (Rule 2.6.4)
- [ ] CardTemplate.metatypes is immutable (Rule 2.6.5) - no gain/lose operations
- [ ] HeroCard.moniker property extracted from name (Rule 2.6.6, cross-ref 2.7.3)
- [ ] card_pool_legality_check(card, hero) validates metatype matching (Rule 2.6.6)
- [ ] TournamentRule.allowed_sets for set-metatype validation (Rule 2.6.6)
"""

import pytest
from pytest_bdd import scenario, given, when, then, parsers
from dataclasses import dataclass, field
from typing import Optional, List, Set, FrozenSet


# ---------------------------------------------------------------------------
# Stub classes for testing Section 2.6 rules
# ---------------------------------------------------------------------------


@dataclass
class MetatypeStub:
    """
    Stub representing a metatype keyword.

    Rule 2.6.6: Metatypes are either hero-metatypes or set-metatypes.

    Engine Features Needed:
    - [ ] MetatypeKeyword class with metatype_type ('hero' or 'set') (Rule 2.6.6)
    - [ ] MetatypeKeyword.value: the keyword string (Rule 2.6.1)
    """

    value: str  # The keyword string, e.g. "Dorinthea", "Classic Constructed"
    metatype_type: str  # "hero" or "set"

    def is_hero_metatype(self) -> bool:
        """Return True if this is a hero-metatype (Rule 2.6.6)."""
        return self.metatype_type == "hero"

    def is_set_metatype(self) -> bool:
        """Return True if this is a set-metatype (Rule 2.6.6)."""
        return self.metatype_type == "set"


@dataclass
class MetatypeCardStub:
    """
    Stub representing a card with metatype properties.

    Models what the engine must implement for Section 2.6.

    Engine Features Needed:
    - [ ] CardTemplate.metatypes: frozenset of metatype keywords (Rule 2.6.3)
    - [ ] CardTemplate.has_metatype(keyword): bool (Rule 2.6.2)
    - [ ] CardTemplate.metatypes is immutable (Rule 2.6.5)
    - [ ] CardTemplate.metatypes_are_before_supertypes: True by definition (Rule 2.6.3)
    """

    name: str
    _metatypes: List[MetatypeStub] = field(default_factory=list)
    supertypes: List[str] = field(default_factory=list)

    @property
    def metatypes(self) -> List[MetatypeStub]:
        """
        Rule 2.6.2: An object can have zero or more metatypes.
        Rule 2.6.3: Metatype determined by type box; printed before supertypes.
        """
        return list(self._metatypes)

    @property
    def metatype_count(self) -> int:
        """Return the number of metatypes on this card (Rule 2.6.2)."""
        return len(self._metatypes)

    @property
    def has_metatypes(self) -> bool:
        """Return True if the card has any metatypes (Rule 2.6.2)."""
        return len(self._metatypes) > 0

    def has_metatype(self, keyword: str) -> bool:
        """
        Check if the card has a specific metatype keyword (Rule 2.6.2).
        Returns True if any metatype matches the given keyword value.
        """
        return any(m.value == keyword for m in self._metatypes)

    def gain_metatype(self, metatype: MetatypeStub) -> bool:
        """
        Attempt to gain a metatype.

        Rule 2.6.5: An object cannot gain or lose metatypes.
        This operation always fails - metatypes are immutable.

        Returns False (always fails per Rule 2.6.5).
        """
        return False  # Cannot gain metatypes (Rule 2.6.5)

    def lose_metatype(self, keyword: str) -> bool:
        """
        Attempt to lose a metatype.

        Rule 2.6.5: An object cannot gain or lose metatypes.
        This operation always fails - metatypes are immutable.

        Returns False (always fails per Rule 2.6.5).
        """
        return False  # Cannot lose metatypes (Rule 2.6.5)

    def metatypes_precede_supertypes_in_type_box(self) -> bool:
        """
        Rule 2.6.3: Metatype is printed before the card's supertypes.
        Returns True to indicate correct type box ordering.
        """
        return True


@dataclass
class HeroCardStub:
    """
    Stub representing a hero card with a moniker.

    Rule 2.6.6: Hero-metatypes match against a hero's moniker(s).
    Rule 2.7.3: Monikers are derived from a personal name.

    Engine Features Needed:
    - [ ] HeroCard.moniker property derived from name (Rule 2.7.3)
    - [ ] HeroCard.name: full name of the hero (Rule 2.6.6)
    """

    name: str
    moniker: str  # The most significant identifier of the hero's name (Rule 2.7.3)


@dataclass
class LayerWithMetatypeStub:
    """
    Stub representing a layer (activated or triggered) with inherited metatypes.

    Rule 2.6.4: The metatypes of an activated-layer or triggered-layer are the
                same as the metatypes of its source.

    Engine Features Needed:
    - [ ] Layer.metatypes property inheriting from source (Rule 2.6.4)
    - [ ] Layer.source reference to the creating card (Rule 1.6.1a / 1.7.1a)
    """

    layer_type: str  # "activated" or "triggered"
    source: Optional[MetatypeCardStub] = None

    @property
    def metatypes(self) -> List[MetatypeStub]:
        """
        Rule 2.6.4: Layer metatypes are the same as the source's metatypes.
        """
        if self.source is None:
            return []
        return self.source.metatypes

    @property
    def metatype_count(self) -> int:
        """Return the number of metatypes (inherited from source, Rule 2.6.4)."""
        return len(self.metatypes)

    def has_metatype(self, keyword: str) -> bool:
        """Check if this layer has a specific metatype (Rule 2.6.4)."""
        return any(m.value == keyword for m in self.metatypes)


@dataclass
class CardPoolLegalityResultStub:
    """
    Result of checking if a card may be added to a card-pool.

    Rule 2.6.1: Metatypes determine whether an object may be added to a game.
    Rule 2.6.6: Hero-metatypes checked against hero's moniker.

    Engine Features Needed:
    - [ ] card_pool_legality_check(card, hero) with metatype validation (Rule 2.6.6)
    - [ ] LegalityResult.is_legal, .rejection_reason attributes
    """

    is_legal: bool
    rejection_reason: Optional[str] = None  # e.g. "metatype_mismatch"


@dataclass
class MetatypeGainLossResultStub:
    """
    Result of attempting to gain or lose a metatype.

    Rule 2.6.5: An object cannot gain or lose metatypes.

    Engine Features Needed:
    - [ ] Enforcement of metatype immutability in the engine (Rule 2.6.5)
    """

    success: bool = False  # Always False per Rule 2.6.5
    reason: str = "metatypes_are_immutable"


@dataclass
class TournamentRuleStub:
    """
    Stub representing a tournament rule for set-metatype validation.

    Rule 2.6.6: Set-metatypes specify the name(s) of the set the object can
                be used in as defined by tournament rules.

    Engine Features Needed:
    - [ ] TournamentRule.allowed_sets: set of allowed set names (Rule 2.6.6)
    - [ ] TournamentRule.allows_set(set_name): bool (Rule 2.6.6)
    """

    allowed_sets: List[str] = field(default_factory=list)

    def allows_set(self, set_name: str) -> bool:
        """Return True if the tournament rule allows a given set (Rule 2.6.6)."""
        return set_name in self.allowed_sets


# ---------------------------------------------------------------------------
# Helper function for card-pool legality check
# ---------------------------------------------------------------------------


def check_card_pool_legality(
    card: MetatypeCardStub,
    hero: HeroCardStub,
    tournament_rule: Optional[TournamentRuleStub] = None,
) -> CardPoolLegalityResultStub:
    """
    Check whether a card may be included in a hero's card-pool.

    Rule 2.6.1: Metatypes determine game-entry eligibility.
    Rule 2.6.6: Hero-metatypes checked against hero's moniker.
               Set-metatypes checked against tournament rule's allowed sets.

    Engine Features Needed:
    - [ ] GameEngine.check_card_pool_legality(card, hero, tournament_rule) (Rule 2.6.6)
    """
    for metatype in card.metatypes:
        if metatype.is_hero_metatype():
            # Hero-metatype: card must match hero's moniker (Rule 2.6.6)
            if metatype.value != hero.moniker:
                return CardPoolLegalityResultStub(
                    is_legal=False, rejection_reason="metatype_mismatch_hero_moniker"
                )
        elif metatype.is_set_metatype():
            # Set-metatype: must be permitted by tournament rules (Rule 2.6.6)
            if tournament_rule is None or not tournament_rule.allows_set(
                metatype.value
            ):
                return CardPoolLegalityResultStub(
                    is_legal=False, rejection_reason="metatype_mismatch_tournament_set"
                )
    # No metatype violations found
    return CardPoolLegalityResultStub(is_legal=True)


# ===========================================================================
# SCENARIOS
# ===========================================================================


# ---------------------------------------------------------------------------
# Scenario: Metatypes determine whether an object may be added to a game
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_6_metatype.feature",
    "Metatypes determine whether an object may be added to a game",
)
def test_metatypes_determine_game_entry_eligibility():
    """Rule 2.6.1: Metatypes of an object determine whether it may be added to a game."""
    pass


@given(parsers.parse('a card named {card_name} with hero-metatype "{metatype_value}"'))
def card_with_hero_metatype(card_name, metatype_value, game_state_2_6):
    """Rule 2.6.1: Card with a hero-metatype keyword."""
    card = MetatypeCardStub(
        name=card_name,
        _metatypes=[MetatypeStub(value=metatype_value, metatype_type="hero")],
    )
    game_state_2_6.cards[card_name] = card


@given(parsers.parse('a hero named {hero_name} with moniker "{moniker}"'))
def hero_with_moniker(hero_name, moniker, game_state_2_6):
    """Rule 2.6.6: Hero has a moniker used for metatype matching."""
    hero = HeroCardStub(name=hero_name, moniker=moniker)
    game_state_2_6.heroes[hero_name] = hero


@when(parsers.parse("the engine checks if the {card_name} may be added to a game"))
def check_if_card_may_be_added(card_name, game_state_2_6):
    """Rule 2.6.1: Check if the card is eligible to be added to a game."""
    card = game_state_2_6.cards[card_name]
    hero = list(game_state_2_6.heroes.values())[0]
    game_state_2_6.last_legality_result = check_card_pool_legality(card, hero)


@then(
    parsers.parse(
        "the {card_name} should be eligible to be added for the {hero_name} hero"
    )
)
def card_should_be_eligible_for_hero(card_name, hero_name, game_state_2_6):
    """Rule 2.6.1: Card should be eligible to be added for the matching hero."""
    assert game_state_2_6.last_legality_result.is_legal is True, (
        f"Expected {card_name} to be eligible for {hero_name}, "
        f"but was rejected: {game_state_2_6.last_legality_result.rejection_reason}"
    )


# ---------------------------------------------------------------------------
# Scenario: Card with non-matching hero-metatype cannot be added
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_6_metatype.feature",
    "Card with non-matching hero-metatype cannot be added to a game",
)
def test_non_matching_hero_metatype_cannot_be_added():
    """Rule 2.6.1/2.6.6: Card with non-matching metatype rejected from game."""
    pass


@given(
    parsers.parse(
        'a card named {card_name} with hero-metatype "{metatype_value}" and a hero named {hero_name} with moniker "{moniker}"'
    )
)
def card_with_metatype_and_non_matching_hero(
    card_name, metatype_value, hero_name, moniker, game_state_2_6
):
    """Rule 2.6.6: Setup card and non-matching hero."""
    card = MetatypeCardStub(
        name=card_name,
        _metatypes=[MetatypeStub(value=metatype_value, metatype_type="hero")],
    )
    hero = HeroCardStub(name=hero_name, moniker=moniker)
    game_state_2_6.cards[card_name] = card
    game_state_2_6.heroes[hero_name] = hero


@when(
    parsers.parse(
        "the engine checks if the {card_name} may be added to a game for {hero_name}"
    )
)
def check_if_card_may_be_added_for_hero(card_name, hero_name, game_state_2_6):
    """Rule 2.6.1: Check if the card is eligible for a specific hero."""
    card = game_state_2_6.cards[card_name]
    hero = game_state_2_6.heroes[hero_name]
    game_state_2_6.last_legality_result = check_card_pool_legality(card, hero)


@then(parsers.parse("the {card_name} should not be eligible for the {hero_name} hero"))
def card_should_not_be_eligible_for_hero(card_name, hero_name, game_state_2_6):
    """Rule 2.6.1/2.6.6: Card should NOT be eligible for non-matching hero."""
    assert game_state_2_6.last_legality_result.is_legal is False, (
        f"Expected {card_name} to be rejected for {hero_name}, but was allowed"
    )


# ---------------------------------------------------------------------------
# Scenario: A card with no metatypes has zero metatypes
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_6_metatype.feature",
    "A card with no metatypes has zero metatypes",
)
def test_card_with_no_metatypes_has_zero_metatypes():
    """Rule 2.6.2: An object can have zero metatypes."""
    pass


@given(parsers.parse("a card named {card_name} with no metatypes"))
def card_with_no_metatypes(card_name, game_state_2_6):
    """Rule 2.6.2: Card with no metatypes (empty metatype list)."""
    card = MetatypeCardStub(name=card_name, _metatypes=[])
    game_state_2_6.cards[card_name] = card


@when(parsers.parse("the engine checks the metatypes of the {card_name}"))
def check_metatypes_of_card(card_name, game_state_2_6):
    """Rule 2.6.2: Check the metatypes of the card."""
    card = game_state_2_6.cards[card_name]
    game_state_2_6.last_metatypes = card.metatypes
    game_state_2_6.last_metatype_count = card.metatype_count


@then(parsers.parse("the {card_name} should have zero metatypes"))
def card_should_have_zero_metatypes(card_name, game_state_2_6):
    """Rule 2.6.2: Card should have zero metatypes."""
    assert game_state_2_6.last_metatype_count == 0, (
        f"Expected {card_name} to have zero metatypes, "
        f"but has {game_state_2_6.last_metatype_count}"
    )


@then(parsers.parse("the {card_name} metatypes list should be empty"))
def card_metatypes_list_should_be_empty(card_name, game_state_2_6):
    """Rule 2.6.2: The metatypes list should be empty."""
    assert len(game_state_2_6.last_metatypes) == 0, (
        f"Expected {card_name} metatypes list to be empty, "
        f"but found: {game_state_2_6.last_metatypes}"
    )


# ---------------------------------------------------------------------------
# Scenario: A card can have exactly one metatype
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_6_metatype.feature",
    "A card can have exactly one metatype",
)
def test_card_can_have_exactly_one_metatype():
    """Rule 2.6.2: An object can have one metatype."""
    pass


@then(parsers.parse("the {card_name} should have exactly one metatype"))
def card_should_have_exactly_one_metatype(card_name, game_state_2_6):
    """Rule 2.6.2: Card should have exactly one metatype."""
    assert game_state_2_6.last_metatype_count == 1, (
        f"Expected {card_name} to have exactly 1 metatype, "
        f"but has {game_state_2_6.last_metatype_count}"
    )


@then(parsers.parse('the {card_name} metatype should be "{expected_metatype}"'))
def card_metatype_should_be(card_name, expected_metatype, game_state_2_6):
    """Rule 2.6.2: The single metatype value should match."""
    metatype_values = [m.value for m in game_state_2_6.last_metatypes]
    assert expected_metatype in metatype_values, (
        f"Expected {card_name} to have metatype '{expected_metatype}', "
        f"but metatypes are: {metatype_values}"
    )


# ---------------------------------------------------------------------------
# Scenario: A card can have multiple metatypes
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_6_metatype.feature",
    "A card can have multiple metatypes",
)
def test_card_can_have_multiple_metatypes():
    """Rule 2.6.2: An object can have more than one metatype."""
    pass


@given(
    parsers.parse(
        'a card named {card_name} with two hero-metatypes "{metatype1}" and "{metatype2}"'
    )
)
def card_with_two_hero_metatypes(card_name, metatype1, metatype2, game_state_2_6):
    """Rule 2.6.2: Card with two hero-metatypes."""
    card = MetatypeCardStub(
        name=card_name,
        _metatypes=[
            MetatypeStub(value=metatype1, metatype_type="hero"),
            MetatypeStub(value=metatype2, metatype_type="hero"),
        ],
    )
    game_state_2_6.cards[card_name] = card


@then(parsers.parse("the {card_name} should have exactly two metatypes"))
def card_should_have_exactly_two_metatypes(card_name, game_state_2_6):
    """Rule 2.6.2: Card should have exactly two metatypes."""
    assert game_state_2_6.last_metatype_count == 2, (
        f"Expected {card_name} to have exactly 2 metatypes, "
        f"but has {game_state_2_6.last_metatype_count}"
    )


@then(parsers.parse('the {card_name} metatypes should include "{expected_metatype}"'))
def card_metatypes_should_include(card_name, expected_metatype, game_state_2_6):
    """Rule 2.6.2: The metatypes list should include the given value."""
    metatype_values = [m.value for m in game_state_2_6.last_metatypes]
    assert expected_metatype in metatype_values, (
        f"Expected {card_name} metatypes to include '{expected_metatype}', "
        f"but metatypes are: {metatype_values}"
    )


# ---------------------------------------------------------------------------
# Scenario: The metatype of a card is determined by its type box
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_6_metatype.feature",
    "The metatype of a card is determined by its type box",
)
def test_metatype_determined_by_type_box():
    """Rule 2.6.3: Metatype of a card is determined by its type box."""
    pass


@given(
    parsers.parse(
        'a card named {card_name} with type box showing metatype "{metatype_value}" before supertypes'
    )
)
def card_with_type_box_metatype(card_name, metatype_value, game_state_2_6):
    """Rule 2.6.3: Card with metatype in type box."""
    card = MetatypeCardStub(
        name=card_name,
        _metatypes=[MetatypeStub(value=metatype_value, metatype_type="hero")],
        supertypes=["Warrior"],
    )
    game_state_2_6.cards[card_name] = card


@when(
    parsers.parse("the engine reads the metatype from the type box of the {card_name}")
)
def read_metatype_from_type_box(card_name, game_state_2_6):
    """Rule 2.6.3: Read metatype from the type box."""
    card = game_state_2_6.cards[card_name]
    game_state_2_6.last_metatypes = card.metatypes
    game_state_2_6.last_type_box_order = card.metatypes_precede_supertypes_in_type_box()


@then(parsers.parse('the metatype should be "{expected_value}"'))
def metatype_value_should_be(expected_value, game_state_2_6):
    """Rule 2.6.3: The metatype value should match what's in the type box."""
    metatype_values = [m.value for m in game_state_2_6.last_metatypes]
    assert expected_value in metatype_values, (
        f"Expected metatype '{expected_value}' in type box, "
        f"but found: {metatype_values}"
    )


@then("the metatype should appear before the supertypes in the type box")
def metatype_should_appear_before_supertypes_then(game_state_2_6):
    """Rule 2.6.3: Metatype is printed before the card's supertypes."""
    assert game_state_2_6.last_type_box_order is True, (
        "Expected metatype to appear before supertypes in type box"
    )


@then("the metatype position should be before the supertype position in the type box")
def metatype_position_before_supertype_then(game_state_2_6):
    """Rule 2.6.3: Metatype precedes supertypes in the type box format."""
    assert game_state_2_6.last_type_box_order is True, (
        "Expected metatype to be printed before supertypes in type box per Rule 2.6.3"
    )


# ---------------------------------------------------------------------------
# Scenario: Metatype is printed before supertypes in the type box
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_6_metatype.feature",
    "Metatype is printed before supertypes in the type box",
)
def test_metatype_printed_before_supertypes():
    """Rule 2.6.3: Metatype printed before supertypes in the type box."""
    pass


@given(
    parsers.parse(
        'a card named {card_name} with metatype "{metatype_value}" and supertype "{supertype_value}"'
    )
)
def card_with_metatype_and_supertype(
    card_name, metatype_value, supertype_value, game_state_2_6
):
    """Rule 2.6.3: Card with both a metatype and a supertype."""
    card = MetatypeCardStub(
        name=card_name,
        _metatypes=[MetatypeStub(value=metatype_value, metatype_type="hero")],
        supertypes=[supertype_value],
    )
    game_state_2_6.cards[card_name] = card


@when(parsers.parse("the engine reads the type box of the {card_name}"))
def read_type_box(card_name, game_state_2_6):
    """Rule 2.6.3: Read the type box information."""
    card = game_state_2_6.cards[card_name]
    game_state_2_6.last_type_box_order = card.metatypes_precede_supertypes_in_type_box()


# ---------------------------------------------------------------------------
# Scenario: Activated-layer has the same metatypes as its source
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_6_metatype.feature",
    "Activated-layer has the same metatypes as its source",
)
def test_activated_layer_inherits_source_metatypes():
    """Rule 2.6.4: Activated-layer metatypes same as source."""
    pass


@given(
    parsers.parse(
        'a card named {card_name} with hero-metatype "{metatype_value}" and the card creates an activated-layer'
    )
)
def card_creates_activated_layer(card_name, metatype_value, game_state_2_6):
    """Rule 2.6.4: Card with metatype creates an activated-layer."""
    source = MetatypeCardStub(
        name=card_name,
        _metatypes=[MetatypeStub(value=metatype_value, metatype_type="hero")],
    )
    layer = LayerWithMetatypeStub(layer_type="activated", source=source)
    game_state_2_6.cards[card_name] = source
    game_state_2_6.layers["activated_layer"] = layer


@when("the engine checks the layer metatypes of the activated-layer")
def check_activated_layer_metatypes(game_state_2_6):
    """Rule 2.6.4: Check the metatypes of the activated-layer."""
    layer = game_state_2_6.layers["activated_layer"]
    game_state_2_6.last_metatypes = layer.metatypes
    game_state_2_6.last_metatype_count = layer.metatype_count


@then("the activated-layer metatypes should match the source metatypes")
def activated_layer_metatypes_match_source(game_state_2_6):
    """Rule 2.6.4: Layer metatypes should be identical to source metatypes."""
    layer = game_state_2_6.layers["activated_layer"]
    source_metatypes = {m.value for m in layer.source.metatypes}
    layer_metatypes = {m.value for m in layer.metatypes}
    assert layer_metatypes == source_metatypes, (
        f"Expected layer metatypes {layer_metatypes} to match "
        f"source metatypes {source_metatypes}"
    )


@then(parsers.parse('the activated-layer should have metatype "{expected_metatype}"'))
def activated_layer_should_have_metatype(expected_metatype, game_state_2_6):
    """Rule 2.6.4: The activated-layer should have the specified metatype."""
    metatype_values = [m.value for m in game_state_2_6.last_metatypes]
    assert expected_metatype in metatype_values, (
        f"Expected activated-layer to have metatype '{expected_metatype}', "
        f"but found: {metatype_values}"
    )


# ---------------------------------------------------------------------------
# Scenario: Triggered-layer has the same metatypes as its source
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_6_metatype.feature",
    "Triggered-layer has the same metatypes as its source",
)
def test_triggered_layer_inherits_source_metatypes():
    """Rule 2.6.4: Triggered-layer metatypes same as source."""
    pass


@given(
    parsers.parse(
        'a card named {card_name} with hero-metatype "{metatype_value}" and the card creates a triggered-layer'
    )
)
def card_creates_triggered_layer(card_name, metatype_value, game_state_2_6):
    """Rule 2.6.4: Card with metatype creates a triggered-layer."""
    source = MetatypeCardStub(
        name=card_name,
        _metatypes=[MetatypeStub(value=metatype_value, metatype_type="hero")],
    )
    layer = LayerWithMetatypeStub(layer_type="triggered", source=source)
    game_state_2_6.cards[card_name] = source
    game_state_2_6.layers["triggered_layer"] = layer


@when("the engine checks the layer metatypes of the triggered-layer")
def check_triggered_layer_metatypes(game_state_2_6):
    """Rule 2.6.4: Check the metatypes of the triggered-layer."""
    layer = game_state_2_6.layers["triggered_layer"]
    game_state_2_6.last_metatypes = layer.metatypes
    game_state_2_6.last_metatype_count = layer.metatype_count


@then("the triggered-layer metatypes should match the source metatypes")
def triggered_layer_metatypes_match_source(game_state_2_6):
    """Rule 2.6.4: Triggered-layer metatypes should be identical to source metatypes."""
    layer = game_state_2_6.layers["triggered_layer"]
    source_metatypes = {m.value for m in layer.source.metatypes}
    layer_metatypes = {m.value for m in layer.metatypes}
    assert layer_metatypes == source_metatypes, (
        f"Expected triggered-layer metatypes {layer_metatypes} to match "
        f"source metatypes {source_metatypes}"
    )


@then(parsers.parse('the triggered-layer should have metatype "{expected_metatype}"'))
def triggered_layer_should_have_metatype(expected_metatype, game_state_2_6):
    """Rule 2.6.4: The triggered-layer should have the specified metatype."""
    metatype_values = [m.value for m in game_state_2_6.last_metatypes]
    assert expected_metatype in metatype_values, (
        f"Expected triggered-layer to have metatype '{expected_metatype}', "
        f"but found: {metatype_values}"
    )


# ---------------------------------------------------------------------------
# Scenario: Layer from a source with no metatypes has no metatypes
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_6_metatype.feature",
    "Layer from a source with no metatypes has no metatypes",
)
def test_layer_from_no_metatype_source_has_no_metatypes():
    """Rule 2.6.4: Layer inherits no metatypes when source has none."""
    pass


@given(
    parsers.parse(
        "a card named {card_name} with no metatypes and the card creates an activated-layer"
    )
)
def card_with_no_metatypes_creates_layer(card_name, game_state_2_6):
    """Rule 2.6.4: Card with no metatypes creates a layer."""
    source = MetatypeCardStub(name=card_name, _metatypes=[])
    layer = LayerWithMetatypeStub(layer_type="activated", source=source)
    game_state_2_6.cards[card_name] = source
    game_state_2_6.layers[f"layer_from_{card_name}"] = layer


@when(
    parsers.parse(
        "the engine checks the layer metatypes of the activated-layer from {source_name}"
    )
)
def check_metatypes_of_layer_from_source(source_name, game_state_2_6):
    """Rule 2.6.4: Check metatypes of layer from specified source."""
    layer = game_state_2_6.layers[f"layer_from_{source_name}"]
    game_state_2_6.last_metatype_count = layer.metatype_count


@then(
    parsers.parse("the activated-layer from {source_name} should have zero metatypes")
)
def layer_from_source_should_have_zero_metatypes(source_name, game_state_2_6):
    """Rule 2.6.4: Layer from source with no metatypes should have zero metatypes."""
    assert game_state_2_6.last_metatype_count == 0, (
        f"Expected layer from {source_name} to have zero metatypes, "
        f"but has {game_state_2_6.last_metatype_count}"
    )


# ---------------------------------------------------------------------------
# Scenario: An object cannot gain metatypes via effects
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_6_metatype.feature",
    "An object cannot gain metatypes via effects",
)
def test_object_cannot_gain_metatypes():
    """Rule 2.6.5: An object cannot gain metatypes."""
    pass


@given(parsers.parse("a card named {card_name} with no metatypes"))
def card_without_metatypes_for_gain_test(card_name, game_state_2_6):
    """Rule 2.6.5: Card with no metatypes (target for gain attempt)."""
    card = MetatypeCardStub(name=card_name, _metatypes=[])
    game_state_2_6.cards[card_name] = card


@when(
    parsers.parse(
        'an effect attempts to grant the {card_name} hero-metatype "{metatype_value}"'
    )
)
def effect_attempts_to_grant_metatype(card_name, metatype_value, game_state_2_6):
    """Rule 2.6.5: Attempt to grant a metatype via an effect."""
    card = game_state_2_6.cards[card_name]
    new_metatype = MetatypeStub(value=metatype_value, metatype_type="hero")
    success = card.gain_metatype(new_metatype)
    game_state_2_6.last_gain_result = MetatypeGainLossResultStub(success=success)


@then("the metatype gain attempt should fail")
def metatype_gain_attempt_should_fail(game_state_2_6):
    """Rule 2.6.5: Gaining a metatype should not be possible."""
    assert game_state_2_6.last_gain_result.success is False, (
        "Expected metatype gain attempt to fail per Rule 2.6.5, but it succeeded"
    )


@then(parsers.parse("the {card_name} should still have zero metatypes"))
def card_should_still_have_zero_metatypes(card_name, game_state_2_6):
    """Rule 2.6.5: Card should remain unchanged after failed gain attempt."""
    card = game_state_2_6.cards[card_name]
    assert card.metatype_count == 0, (
        f"Expected {card_name} to still have zero metatypes, "
        f"but now has {card.metatype_count}"
    )


# ---------------------------------------------------------------------------
# Scenario: An object cannot lose metatypes via effects
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_6_metatype.feature",
    "An object cannot lose metatypes via effects",
)
def test_object_cannot_lose_metatypes():
    """Rule 2.6.5: An object cannot lose metatypes."""
    pass


@given(parsers.parse('a card named {card_name} with hero-metatype "{metatype_value}"'))
def card_with_single_hero_metatype(card_name, metatype_value, game_state_2_6):
    """Rule 2.6.5: Card with a metatype (target for removal attempt)."""
    card = MetatypeCardStub(
        name=card_name,
        _metatypes=[MetatypeStub(value=metatype_value, metatype_type="hero")],
    )
    game_state_2_6.cards[card_name] = card


@when(
    parsers.parse(
        'an effect attempts to remove the "{metatype_value}" metatype from the {card_name}'
    )
)
def effect_attempts_to_remove_metatype(metatype_value, card_name, game_state_2_6):
    """Rule 2.6.5: Attempt to remove a metatype via an effect."""
    card = game_state_2_6.cards[card_name]
    success = card.lose_metatype(metatype_value)
    game_state_2_6.last_loss_result = MetatypeGainLossResultStub(success=success)


@then("the metatype removal attempt should fail")
def metatype_removal_attempt_should_fail(game_state_2_6):
    """Rule 2.6.5: Removing a metatype should not be possible."""
    assert game_state_2_6.last_loss_result.success is False, (
        "Expected metatype removal attempt to fail per Rule 2.6.5, but it succeeded"
    )


@then(parsers.parse('the {card_name} should still have metatype "{expected_metatype}"'))
def card_should_still_have_metatype(card_name, expected_metatype, game_state_2_6):
    """Rule 2.6.5: Card should retain its original metatypes."""
    card = game_state_2_6.cards[card_name]
    assert card.has_metatype(expected_metatype), (
        f"Expected {card_name} to still have metatype '{expected_metatype}' "
        "after failed removal attempt"
    )


# ---------------------------------------------------------------------------
# Scenario: Hero-metatype card legal only for matching hero moniker
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_6_metatype.feature",
    "Hero-metatype card legal only for matching hero moniker",
)
def test_hero_metatype_legal_for_matching_moniker():
    """Rule 2.6.6: Hero-metatype card legal for matching hero moniker."""
    pass


@given(
    parsers.parse(
        'a card named {card_name} with hero-metatype "{metatype_value}" and a hero named {hero_name} with moniker "{moniker}"'
    )
)
def card_with_metatype_and_matching_hero(
    card_name, metatype_value, hero_name, moniker, game_state_2_6
):
    """Rule 2.6.6: Setup card and hero where moniker matches metatype."""
    card = MetatypeCardStub(
        name=card_name,
        _metatypes=[MetatypeStub(value=metatype_value, metatype_type="hero")],
    )
    hero = HeroCardStub(name=hero_name, moniker=moniker)
    game_state_2_6.cards[card_name] = card
    game_state_2_6.heroes[hero_name] = hero


@when(parsers.parse("checking if {card_name} is legal for card-pool"))
def check_card_pool_legality_step(card_name, game_state_2_6):
    """Rule 2.6.6: Check card-pool legality for the first available hero."""
    card = game_state_2_6.cards[card_name]
    hero = list(game_state_2_6.heroes.values())[0]
    game_state_2_6.last_legality_result = check_card_pool_legality(card, hero)


@then(parsers.parse("the {card_name} should be legal for the {hero_name} hero"))
def card_should_be_legal_for_hero(card_name, hero_name, game_state_2_6):
    """Rule 2.6.6: Card with matching metatype should be legal."""
    assert game_state_2_6.last_legality_result.is_legal is True, (
        f"Expected {card_name} to be legal for {hero_name}, "
        f"but was rejected: {game_state_2_6.last_legality_result.rejection_reason}"
    )


# ---------------------------------------------------------------------------
# Scenario: Hero-metatype card illegal for non-matching hero moniker
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_6_metatype.feature",
    "Hero-metatype card illegal for non-matching hero moniker",
)
def test_hero_metatype_illegal_for_non_matching_moniker():
    """Rule 2.6.6: Hero-metatype card illegal for non-matching hero moniker."""
    pass


@when(parsers.parse("checking if {card_name} is legal for the {hero_name} card-pool"))
def check_card_pool_legality_for_hero(card_name, hero_name, game_state_2_6):
    """Rule 2.6.6: Check card-pool legality for a specific hero."""
    card = game_state_2_6.cards[card_name]
    hero = game_state_2_6.heroes[hero_name]
    game_state_2_6.last_legality_result = check_card_pool_legality(card, hero)


@then(parsers.parse("the {card_name} should not be legal for the {hero_name} hero"))
def card_should_not_be_legal_for_hero(card_name, hero_name, game_state_2_6):
    """Rule 2.6.6: Card with non-matching metatype should be illegal."""
    assert game_state_2_6.last_legality_result.is_legal is False, (
        f"Expected {card_name} to be illegal for {hero_name}, but was allowed"
    )


# ---------------------------------------------------------------------------
# Scenario: Set-metatype card requires matching tournament set rule
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_6_metatype.feature",
    "Set-metatype card requires matching tournament set rule",
)
def test_set_metatype_requires_matching_tournament_rule():
    """Rule 2.6.6: Set-metatype card must match tournament rule."""
    pass


@given(parsers.parse('a card named {card_name} with set-metatype "{set_name}"'))
def card_with_set_metatype(card_name, set_name, game_state_2_6):
    """Rule 2.6.6: Card with a set-metatype."""
    card = MetatypeCardStub(
        name=card_name,
        _metatypes=[MetatypeStub(value=set_name, metatype_type="set")],
    )
    game_state_2_6.cards[card_name] = card


@given(parsers.parse('a tournament rule allowing the set "{set_name}"'))
def tournament_rule_allowing_set(set_name, game_state_2_6):
    """Rule 2.6.6: Tournament rule that allows a specific set."""
    game_state_2_6.tournament_rule = TournamentRuleStub(allowed_sets=[set_name])


@when(parsers.parse("checking if {card_name} may be added to the game"))
def check_if_set_card_may_be_added(card_name, game_state_2_6):
    """Rule 2.6.6: Check if the set-metatype card is permitted."""
    card = game_state_2_6.cards[card_name]
    # For set-metatypes we need a placeholder hero and the tournament rule
    placeholder_hero = HeroCardStub(name="Any Hero", moniker="Any")
    result = check_card_pool_legality(
        card, placeholder_hero, game_state_2_6.tournament_rule
    )
    game_state_2_6.last_legality_result = result


@then(parsers.parse("the {card_name} should be allowed in the game"))
def card_should_be_allowed_in_game(card_name, game_state_2_6):
    """Rule 2.6.6: Card should be allowed under matching tournament rule."""
    assert game_state_2_6.last_legality_result.is_legal is True, (
        f"Expected {card_name} to be allowed in game, "
        f"but rejected: {game_state_2_6.last_legality_result.rejection_reason}"
    )


# ---------------------------------------------------------------------------
# Scenario: Set-metatype card rejected without matching tournament rule
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_6_metatype.feature",
    "Set-metatype card rejected when tournament rule does not allow that set",
)
def test_set_metatype_rejected_without_matching_tournament_rule():
    """Rule 2.6.6: Set-metatype card rejected when tournament rule doesn't allow."""
    pass


@given(parsers.parse('a tournament rule that does not allow "{set_name}"'))
def tournament_rule_not_allowing_set(set_name, game_state_2_6):
    """Rule 2.6.6: Tournament rule that does not allow the given set."""
    game_state_2_6.tournament_rule = TournamentRuleStub(
        allowed_sets=[]
    )  # allows nothing


@when(
    parsers.parse(
        "checking if {card_name} may be added under the non-matching tournament rule"
    )
)
def check_if_card_allowed_under_non_matching_rule(card_name, game_state_2_6):
    """Rule 2.6.6: Check if the set-metatype card is permitted under non-matching rule."""
    card = game_state_2_6.cards[card_name]
    placeholder_hero = HeroCardStub(name="Any Hero", moniker="Any")
    result = check_card_pool_legality(
        card, placeholder_hero, game_state_2_6.tournament_rule
    )
    game_state_2_6.last_legality_result = result


@then(parsers.parse("the {card_name} should not be allowed for the non-matching rule"))
def card_should_not_be_allowed_for_non_matching_rule(card_name, game_state_2_6):
    """Rule 2.6.6: Card should be rejected under non-matching tournament rule."""
    assert game_state_2_6.last_legality_result.is_legal is False, (
        f"Expected {card_name} to be rejected under non-matching tournament rule, "
        "but was allowed"
    )


# ---------------------------------------------------------------------------
# Scenario: Card with no metatypes is always eligible regardless of hero
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_6_metatype.feature",
    "Card with no metatypes is always eligible regardless of hero",
)
def test_card_with_no_metatypes_always_eligible():
    """Rule 2.6.1/2.6.2: Card with no metatypes not excluded by metatype checks."""
    pass


@when(parsers.parse("checking if {card_name} can be added to game for {hero_name}"))
def check_if_no_metatype_card_can_be_added(card_name, hero_name, game_state_2_6):
    """Rule 2.6.1/2.6.2: Check legality for card with no metatypes."""
    card = game_state_2_6.cards[card_name]
    hero = game_state_2_6.heroes[hero_name]
    game_state_2_6.last_legality_result = check_card_pool_legality(card, hero)


@then(parsers.parse("the {card_name} should not be excluded by metatype restrictions"))
def card_should_not_be_excluded_by_metatype_restrictions(card_name, game_state_2_6):
    """Rule 2.6.2: Card with no metatypes not excluded by metatype restrictions."""
    assert game_state_2_6.last_legality_result.is_legal is True, (
        f"Expected {card_name} (no metatypes) to pass metatype check, "
        f"but was excluded: {game_state_2_6.last_legality_result.rejection_reason}"
    )


# ===========================================================================
# FIXTURES
# ===========================================================================


@pytest.fixture
def game_state_2_6():
    """
    Fixture providing game state for Section 2.6 metatype tests.

    Provides a simple state object holding test cards, heroes, and layers.

    Engine Features Needed for Section 2.6:
    - [ ] CardTemplate.metatypes: frozenset of metatype keywords (Rule 2.6.1)
    - [ ] MetatypeKeyword class variants: hero-metatype, set-metatype (Rule 2.6.6)
    - [ ] Layer.metatypes inherited from source (Rule 2.6.4)
    - [ ] Metatype immutability enforcement (Rule 2.6.5)
    - [ ] HeroCard.moniker property (Rule 2.6.6, cross-ref 2.7.3)
    - [ ] card_pool_legality_check with metatype validation (Rule 2.6.6)
    - [ ] TournamentRule.allowed_sets for set-metatype (Rule 2.6.6)
    """

    class GameState2_6:
        def __init__(self):
            self.cards = {}
            self.heroes = {}
            self.layers = {}
            self.tournament_rule = None
            self.last_legality_result = None
            self.last_metatypes = []
            self.last_metatype_count = 0
            self.last_type_box_order = None
            self.last_gain_result = None
            self.last_loss_result = None

    return GameState2_6()
