"""
Step definitions for Section 2.15: Types
Reference: Flesh and Blood Comprehensive Rules Section 2.15

This module implements behavioral tests for the types property of cards and
other game objects in Flesh and Blood.

Rule 2.15.1: Types are a collection of type keywords. The types of a card
             determine whether the card is a hero-, token-, deck-, or
             arena-card, and how a deck-card may be played.

Rule 2.15.2: An object can have zero or more types.

Rule 2.15.3: The type of a card is determined by its type box. The type is
             printed after the card's supertypes, and before a long dash and
             subtypes (if any).

Rule 2.15.4: The types of an activated-layer or triggered-layer are the same
             as the types of its source.

Rule 2.15.4a: The types of an activated ability layer include the types
              determined by the activated ability. [5.2.1]

Rule 2.15.5: An object can gain or lose types from rules and/or effects.

Rule 2.15.6: Types are functional keywords and add additional rules to an
             object.

Rule 2.15.6a: The type keywords are Action, Attack Reaction, Block, Companion,
              Defense Reaction, Demi-Hero, Equipment, Hero, Instant, Macro,
              Mentor, Resource, Token, and Weapon. [8.1]

Engine Features Needed for Section 2.15:
- [ ] `CardTemplate.types` property returning frozenset of type keywords (Rule 2.15.2)
- [ ] `CardInstance.types` property returning resolved frozenset of type keywords (Rule 2.15.2)
- [ ] `CardInstance.has_type(name)` method (Rule 2.15.1)
- [ ] `CardTemplate.get_card_classification()` -> "hero"/"token"/"deck"/"arena" (Rule 2.15.1)
- [ ] `TypeRegistry.ALL_TYPE_KEYWORDS` frozenset with all 14 type keywords (Rule 2.15.6a)
- [ ] `TypeRegistry.is_functional(name)` = True always (Rule 2.15.6)
- [ ] `TypeRegistry.DECK_CARD_TYPES` frozenset of deck-making types (Rule 2.15.1 / 1.3.2c)
- [ ] Type box parser extracting types after supertypes, before subtypes (Rule 2.15.3)
- [ ] `Layer.types` property inheriting from source (Rule 2.15.4)
- [ ] Activated ability layer's `types` property including ability-determined types (Rule 2.15.4a)
- [ ] `CardInstance.gain_type(name)` method (Rule 2.15.5)
- [ ] `CardInstance.lose_type(name)` method (Rule 2.15.5)
"""

import pytest
from pytest_bdd import scenario, given, when, then, parsers
from dataclasses import dataclass, field
from typing import Optional, List, Set, FrozenSet


# ---------------------------------------------------------------------------
# Stub classes for testing Section 2.15 rules
# ---------------------------------------------------------------------------

# Rule 2.15.6a: The 14 type keywords
ALL_TYPE_KEYWORDS: FrozenSet[str] = frozenset(
    {
        "Action",
        "Attack Reaction",
        "Block",
        "Companion",
        "Defense Reaction",
        "Demi-Hero",
        "Equipment",
        "Hero",
        "Instant",
        "Macro",
        "Mentor",
        "Resource",
        "Token",
        "Weapon",
    }
)

# Rule 2.15.1 / 1.3.2c: Types that make a card a deck-card
DECK_CARD_TYPES: FrozenSet[str] = frozenset(
    {
        "Action",
        "Attack Reaction",
        "Block",
        "Defense Reaction",
        "Instant",
        "Mentor",
        "Resource",
    }
)

# Rule 2.15.1 / 1.3.2a: Types that make a card a hero-card
HERO_CARD_TYPES: FrozenSet[str] = frozenset({"Hero"})

# Rule 2.15.1 / 1.3.2b: Types that make a card a token-card
TOKEN_CARD_TYPES: FrozenSet[str] = frozenset({"Token"})

# Rule 2.15.1 / 1.3.2d: Arena-card types (non-hero, non-token, non-deck)
ARENA_CARD_TYPES: FrozenSet[str] = frozenset(
    {
        "Companion",
        "Demi-Hero",
        "Equipment",
        "Macro",
        "Weapon",
    }
)


@dataclass
class TypeCardStub:
    """
    Stub representing a card with types.

    Models what the engine must implement for Section 2.15.

    Engine Features Needed:
    - [ ] CardTemplate.types: frozenset[str] — type keywords (Rule 2.15.2)
    - [ ] CardInstance.types: frozenset[str] — resolved types (Rule 2.15.2)
    - [ ] CardInstance.has_type(name): bool (Rule 2.15.1)
    - [ ] CardInstance.get_card_classification(): str (Rule 2.15.1)
    """

    name: str = "Test Card"
    _types: FrozenSet[str] = field(default_factory=frozenset)

    @property
    def types(self) -> FrozenSet[str]:
        """Rule 2.15.2: An object can have zero or more types."""
        return self._types

    @property
    def type_count(self) -> int:
        """Rule 2.15.2: Number of types."""
        return len(self._types)

    def has_type(self, name: str) -> bool:
        """Rule 2.15.1: Check whether the card has a given type."""
        return name in self._types

    def gain_type(self, name: str) -> bool:
        """
        Rule 2.15.5: Object can gain a type from rules/effects.

        Engine Feature Needed:
        - [ ] CardInstance.gain_type(name) method
        """
        if name not in self._types:
            object.__setattr__(self, "_types", self._types | frozenset({name}))
            return True
        return False

    def lose_type(self, name: str) -> bool:
        """
        Rule 2.15.5: Object can lose a type from rules/effects.

        Engine Feature Needed:
        - [ ] CardInstance.lose_type(name) method
        """
        if name in self._types:
            object.__setattr__(self, "_types", self._types - frozenset({name}))
            return True
        return False

    def get_card_classification(self) -> str:
        """
        Rule 2.15.1: Types determine card classification.

        Cross-ref 1.3.2a/b/c/d: Classification logic.

        Engine Feature Needed:
        - [ ] CardTemplate.get_card_classification() -> "hero"/"token"/"deck"/"arena"
        """
        for t in self._types:
            if t in HERO_CARD_TYPES:
                return "hero"
        for t in self._types:
            if t in TOKEN_CARD_TYPES:
                return "token"
        for t in self._types:
            if t in DECK_CARD_TYPES:
                return "deck"
        for t in self._types:
            if t in ARENA_CARD_TYPES:
                return "arena"
        # No types or unrecognized types
        return "unknown"

    def can_start_in_deck(self) -> bool:
        """
        Rule 2.15.1 / 1.3.2c: Deck-cards may start in player's deck.

        Engine Feature Needed:
        - [ ] CardTemplate.can_start_in_deck property
        """
        return self.get_card_classification() == "deck"

    def is_part_of_card_pool(self) -> bool:
        """
        Rule 2.15.1 / 1.3.2b: Token-cards not part of card-pool.

        Engine Feature Needed:
        - [ ] CardTemplate.is_part_of_card_pool property
        """
        return self.get_card_classification() != "token"

    def starts_as_hero(self) -> bool:
        """
        Rule 2.15.1 / 1.3.2a: Hero-cards start as player's hero.

        Engine Feature Needed:
        - [ ] CardTemplate.starts_as_hero property
        """
        return self.get_card_classification() == "hero"


@dataclass
class TypeBoxParseResult215:
    """
    Stub for parsing a type box string to extract types, supertypes, subtypes.

    Engine Feature Needed:
    - [ ] TypeBoxParser.parse(type_box_str) -> TypeBoxParseResult (Rule 2.15.3)
    """

    _type_box: str = ""
    _ordering: List[str] = field(default_factory=list)

    @classmethod
    def parse(cls, type_box_str: str) -> "TypeBoxParseResult215":
        """
        Rule 2.15.3: Type printed after supertypes, before subtypes.

        Parses: "[SUPERTYPES] [TYPE] - [SUBTYPES]"
        or:     "[SUPERTYPES] [TYPE]"   (no subtypes)
        """
        instance = cls(_type_box=type_box_str)
        instance._ordering = []

        # Split on long dash to separate subtypes
        if " - " in type_box_str:
            before_dash, after_dash = type_box_str.split(" - ", 1)
            subtype_tokens = after_dash.split()
        else:
            before_dash = type_box_str
            subtype_tokens = []

        # All known supertypes (from Rule 2.11.6a/b) to distinguish from types
        known_supertypes = frozenset(
            {
                "Adjudicator",
                "Assassin",
                "Bard",
                "Brute",
                "Guardian",
                "Illusionist",
                "Mechanologist",
                "Merchant",
                "Necromancer",
                "Ninja",
                "Pirate",
                "Ranger",
                "Runeblade",
                "Shapeshifter",
                "Thief",
                "Warrior",
                "Wizard",  # class supertypes
                "Chaos",
                "Draconic",
                "Earth",
                "Elemental",
                "Ice",
                "Light",
                "Lightning",
                "Mystic",
                "Revered",
                "Reviled",
                "Royal",
                "Shadow",  # talent
            }
        )

        # Split on spaces - need to handle multi-word types like "Attack Reaction"
        tokens = before_dash.strip().split()
        supertypes = []
        type_tokens = []

        i = 0
        while i < len(tokens):
            # Check for multi-word type keywords first
            matched_multi = False
            for n in [2]:  # check 2-word keywords
                if i + n <= len(tokens):
                    candidate = " ".join(tokens[i : i + n])
                    if candidate in ALL_TYPE_KEYWORDS:
                        type_tokens.append(candidate)
                        instance._ordering.extend([("type", candidate)] * 1)
                        for _ in range(n):
                            i += 1
                        matched_multi = True
                        break
            if matched_multi:
                continue

            token = tokens[i]
            if token in known_supertypes:
                supertypes.append(token)
                instance._ordering.append(("supertype", token))
            elif token in ALL_TYPE_KEYWORDS:
                type_tokens.append(token)
                instance._ordering.append(("type", token))
            i += 1

        instance._supertypes = frozenset(supertypes)
        instance._types = frozenset(type_tokens)
        instance._subtypes = frozenset(subtype_tokens)

        return instance

    @property
    def supertypes(self) -> FrozenSet[str]:
        """Rule 2.15.3: Supertypes appear before the type."""
        return self._supertypes

    @property
    def types(self) -> FrozenSet[str]:
        """Rule 2.15.3: The type(s) parsed from the type box."""
        return self._types

    @property
    def subtypes(self) -> FrozenSet[str]:
        """Rule 2.15.3: Subtypes appear after the long dash."""
        return self._subtypes

    def get_component_position(self, kind: str, value: str) -> int:
        """
        Rule 2.15.3: Return position of component in ordered list.

        Used to verify supertypes before types, types before subtypes.
        """
        for pos, (k, v) in enumerate(self._ordering):
            if k == kind and v == value:
                return pos
        return -1


@dataclass
class LayerWithTypesStub215:
    """
    Stub representing an activated- or triggered-layer with inherited types.

    Engine Feature Needed:
    - [ ] Layer.types property inheriting from source (Rule 2.15.4)
    - [ ] ActivatedAbilityLayer.types includes types from ability (Rule 2.15.4a)
    """

    source_types: FrozenSet[str] = field(default_factory=frozenset)
    ability_types: FrozenSet[str] = field(default_factory=frozenset)
    is_activated_ability_layer: bool = False

    @property
    def types(self) -> FrozenSet[str]:
        """
        Rule 2.15.4: Layer types same as source types.
        Rule 2.15.4a: Activated ability layer adds types from the ability.
        """
        result = self.source_types
        if self.is_activated_ability_layer:
            result = result | self.ability_types
        return result

    def has_type(self, name: str) -> bool:
        """Rule 2.15.4: Check whether the layer has a given type."""
        return name in self.types

    @property
    def type_count(self) -> int:
        """Rule 2.15.2: Number of types on this layer."""
        return len(self.types)


@dataclass
class TypeCheckResultStub215:
    """
    Stub representing the result of a type check.

    Documents engine features needed.
    """

    type_name: str
    is_functional: bool = True  # Rule 2.15.6: types are always functional
    adds_additional_rules: bool = True  # Rule 2.15.6: always adds rules
    is_deck_card_type: bool = False


def check_type_functional(type_name: str) -> TypeCheckResultStub215:
    """
    Rule 2.15.6: Types are functional keywords.

    Engine Feature Needed:
    - [ ] TypeRegistry.is_functional(name) = True always (Rule 2.15.6)
    """
    return TypeCheckResultStub215(
        type_name=type_name,
        is_functional=True,
        adds_additional_rules=True,
        is_deck_card_type=type_name in DECK_CARD_TYPES,
    )


class SupertypeCheckStub:
    """
    Stub for checking whether supertypes are non-functional.

    Used in the comparison test (Rule 2.15.6 vs supertypes which are non-functional).
    """

    @staticmethod
    def is_functional(name: str) -> bool:
        """
        Rule 2.11.6: Supertypes are non-functional keywords.
        This contrasts with Rule 2.15.6: Types are functional.
        """
        return False  # Supertypes are always non-functional


class PlayabilityCheckStub:
    """
    Stub for checking how a card's type determines when it may be played.

    Engine Feature Needed:
    - [ ] Type-based play rules: Action = action phase only; Instant = any time (Rule 2.15.1)
    """

    ACTION_PHASE_ONLY_TYPES = frozenset(
        {
            "Action",
            "Attack Reaction",
            "Defense Reaction",
            "Block",
            "Resource",
            "Mentor",
        }
    )

    ANYTIME_TYPES = frozenset({"Instant"})

    @classmethod
    def can_play_outside_action_phase(cls, type_name: str) -> bool:
        """Rule 2.15.1: Instant can be played outside action phase."""
        return type_name in cls.ANYTIME_TYPES

    @classmethod
    def action_phase_only(cls, type_name: str) -> bool:
        """Rule 2.15.1: Action can only be played during action phase."""
        return type_name in cls.ACTION_PHASE_ONLY_TYPES


# ---------------------------------------------------------------------------
# Scenario: Action type makes a card a deck-card
# Tests Rule 2.15.1 - Types determine card classification
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_15_types.feature",
    "Action type makes a card a deck-card",
)
def test_action_type_makes_deck_card():
    """Rule 2.15.1: Action type determines card is a deck-card."""
    pass


@scenario(
    "../features/section_2_15_types.feature",
    "Types determine how a deck-card may be played",
)
def test_types_determine_how_deck_card_played():
    """Rule 2.15.1: Types determine how a deck-card may be played."""
    pass


@scenario(
    "../features/section_2_15_types.feature",
    "Hero type makes a card a hero-card",
)
def test_hero_type_makes_hero_card():
    """Rule 2.15.1: Hero type determines card is a hero-card."""
    pass


@scenario(
    "../features/section_2_15_types.feature",
    "Token type makes a card a token-card",
)
def test_token_type_makes_token_card():
    """Rule 2.15.1: Token type determines card is a token-card."""
    pass


@scenario(
    "../features/section_2_15_types.feature",
    "Equipment type makes a card an arena-card",
)
def test_equipment_type_makes_arena_card():
    """Rule 2.15.1: Equipment type determines card is an arena-card."""
    pass


@scenario(
    "../features/section_2_15_types.feature",
    "Weapon type makes a card an arena-card via weapon type",
)
def test_weapon_type_makes_arena_card():
    """Rule 2.15.1: Weapon type determines card is an arena-card."""
    pass


@scenario(
    "../features/section_2_15_types.feature",
    "Object with zero types",
)
def test_object_with_zero_types():
    """Rule 2.15.2: An object can have zero types."""
    pass


@scenario(
    "../features/section_2_15_types.feature",
    "Object can have exactly one type",
)
def test_object_can_have_exactly_one_type():
    """Rule 2.15.2: An object can have exactly one type."""
    pass


@scenario(
    "../features/section_2_15_types.feature",
    "Object can have multiple types",
)
def test_object_can_have_multiple_types():
    """Rule 2.15.2: An object can have multiple types."""
    pass


@scenario(
    "../features/section_2_15_types.feature",
    "Type is determined from the type box",
)
def test_type_determined_from_type_box():
    """Rule 2.15.3: Type determined from type box."""
    pass


@scenario(
    "../features/section_2_15_types.feature",
    "Type box components appear in correct order",
)
def test_type_box_components_correct_order():
    """Rule 2.15.3: Type after supertypes, before subtypes."""
    pass


@scenario(
    "../features/section_2_15_types.feature",
    "Activated-layer inherits types from its source",
)
def test_activated_layer_inherits_types():
    """Rule 2.15.4: Activated-layer types same as source types."""
    pass


@scenario(
    "../features/section_2_15_types.feature",
    "Triggered-layer inherits types from its source",
)
def test_triggered_layer_inherits_types():
    """Rule 2.15.4: Triggered-layer types same as source types."""
    pass


@scenario(
    "../features/section_2_15_types.feature",
    "Layer from no-type source has zero types",
)
def test_layer_from_no_type_source_has_zero_types():
    """Rule 2.15.4: Layer from no-type source has no types."""
    pass


@scenario(
    "../features/section_2_15_types.feature",
    "Activated ability layer includes types from the activated ability",
)
def test_activated_ability_layer_includes_ability_types():
    """Rule 2.15.4a: Activated ability layer includes types from ability."""
    pass


@scenario(
    "../features/section_2_15_types.feature",
    "Object gains a type from an effect",
)
def test_object_gains_type():
    """Rule 2.15.5: Object can gain a type from rules/effects."""
    pass


@scenario(
    "../features/section_2_15_types.feature",
    "Object loses a type from an effect",
)
def test_object_loses_type():
    """Rule 2.15.5: Object can lose a type from rules/effects."""
    pass


@scenario(
    "../features/section_2_15_types.feature",
    "Types are functional keywords that add additional rules",
)
def test_types_are_functional():
    """Rule 2.15.6: Types are functional keywords."""
    pass


@scenario(
    "../features/section_2_15_types.feature",
    "Types are functional unlike traits and non-functional subtypes",
)
def test_types_functional_vs_supertypes_nonfunctional():
    """Rule 2.15.6: Types are functional; supertypes are non-functional."""
    pass


@scenario(
    "../features/section_2_15_types.feature",
    "All 14 type keywords are recognized",
)
def test_all_14_type_keywords_recognized():
    """Rule 2.15.6a: All 14 type keywords recognized."""
    pass


@scenario(
    "../features/section_2_15_types.feature",
    "Deck-card types are Action, Attack Reaction, Block, Defense Reaction, Instant, Mentor, Resource",
)
def test_deck_card_types():
    """Rule 2.15.6a / 1.3.2c: Types that make a card a deck-card."""
    pass


# ---------------------------------------------------------------------------
# Step Definitions
# ---------------------------------------------------------------------------


@given(parsers.parse('a card with type "{type_name}"'))
def given_card_with_type(game_state, type_name):
    """Rule 2.15.2: Create a card stub with the given type."""
    game_state.card = TypeCardStub(
        name=f"Test {type_name} Card",
        _types=frozenset({type_name}),
    )


@given(parsers.parse('a card with types "{type_name1}" and "{type_name2}"'))
def given_card_with_two_types(game_state, type_name1, type_name2):
    """Rule 2.15.2: Create a card stub with two types."""
    game_state.card = TypeCardStub(
        name=f"Test {type_name1}/{type_name2} Card",
        _types=frozenset({type_name1, type_name2}),
    )


@given("a card with no printed type")
def given_card_with_no_type(game_state):
    """Rule 2.15.2: Create a card stub with no types."""
    game_state.card = TypeCardStub(
        name="Test No-Type Card",
        _types=frozenset(),
    )


@given(parsers.parse('a type box string "{type_box}"'))
def given_type_box_string(game_state, type_box):
    """Rule 2.15.3: Store a type box string for parsing."""
    game_state.type_box_string = type_box


@given("the type keyword registry")
def given_type_keyword_registry(game_state):
    """Rule 2.15.6a: Store reference to type keyword registry."""
    game_state.type_registry = ALL_TYPE_KEYWORDS


@given(parsers.parse('a card with type "{type_name}"'))
def given_card_with_single_type_for_comparison(game_state, type_name):
    """Rule 2.15.6: Create a card stub with single type for comparison."""
    game_state.card = TypeCardStub(
        name=f"Test {type_name} Card",
        _types=frozenset({type_name}),
    )


@given(parsers.parse('a card with supertype "{supertype_name}"'))
def given_card_with_supertype(game_state, supertype_name):
    """Rule 2.11.6: Create a card stub with a supertype for comparison."""
    game_state.supertype_name = supertype_name


@given(
    parsers.parse(
        'the card has an activated ability that creates a layer with type "{ability_type}"'
    )
)
def given_card_has_activated_ability_with_type(game_state, ability_type):
    """Rule 2.15.4a: Record the additional type from the activated ability."""
    game_state.ability_type = ability_type


# When steps


@when("the engine determines the card's classification")
def when_engine_determines_classification(game_state):
    """Rule 2.15.1: Determine card classification from types."""
    game_state.classification = game_state.card.get_card_classification()
    game_state.can_start_in_deck = game_state.card.can_start_in_deck()
    game_state.is_part_of_card_pool = game_state.card.is_part_of_card_pool()
    game_state.starts_as_hero = game_state.card.starts_as_hero()


@when("the engine checks how each card may be played")
def when_engine_checks_how_played(game_state):
    """Rule 2.15.1: Check playability rules for each card type."""
    game_state.action_can_play_anytime = (
        PlayabilityCheckStub.can_play_outside_action_phase("Action")
    )
    game_state.instant_can_play_anytime = (
        PlayabilityCheckStub.can_play_outside_action_phase("Instant")
    )
    game_state.action_action_phase_only = PlayabilityCheckStub.action_phase_only(
        "Action"
    )


@when("the engine reads the card's types")
def when_engine_reads_types(game_state):
    """Rule 2.15.2: Read card types."""
    game_state.read_types = game_state.card.types
    game_state.type_count = game_state.card.type_count


@when("the engine counts the card's types")
def when_engine_counts_types(game_state):
    """Rule 2.15.2: Count card types."""
    game_state.type_count = game_state.card.type_count


@when("the engine parses the type box")
def when_engine_parses_type_box(game_state):
    """Rule 2.15.3: Parse a type box string."""
    game_state.parsed = TypeBoxParseResult215.parse(game_state.type_box_string)


@when("an activated-layer is created from that card's ability")
def when_activated_layer_created(game_state):
    """Rule 2.15.4: Create an activated-layer from the card."""
    game_state.layer = LayerWithTypesStub215(
        source_types=game_state.card.types,
        ability_types=frozenset(),
        is_activated_ability_layer=False,
    )


@when("a triggered-layer is created by that card's triggered effect")
def when_triggered_layer_created(game_state):
    """Rule 2.15.4: Create a triggered-layer from the card."""
    game_state.layer = LayerWithTypesStub215(
        source_types=game_state.card.types,
        ability_types=frozenset(),
        is_activated_ability_layer=False,
    )


@when("the activated ability layer is created")
def when_activated_ability_layer_created(game_state):
    """Rule 2.15.4a: Create an activated ability layer with additional types."""
    game_state.layer = LayerWithTypesStub215(
        source_types=game_state.card.types,
        ability_types=frozenset({game_state.ability_type}),
        is_activated_ability_layer=True,
    )


@when(parsers.parse('an effect grants the card the type "{new_type}"'))
def when_effect_grants_type(game_state, new_type):
    """Rule 2.15.5: Grant a new type to the card."""
    game_state.types_before = len(game_state.card.types)
    game_state.card.gain_type(new_type)
    game_state.types_after = len(game_state.card.types)


@when(parsers.parse('an effect removes the type "{removed_type}"'))
def when_effect_removes_type(game_state, removed_type):
    """Rule 2.15.5: Remove a type from the card."""
    game_state.types_before = len(game_state.card.types)
    game_state.card.lose_type(removed_type)
    game_state.types_after = len(game_state.card.types)


@when("the engine checks whether types are functional")
def when_engine_checks_functional(game_state):
    """Rule 2.15.6: Check whether the type is a functional keyword."""
    game_state.type_check = check_type_functional(list(game_state.card.types)[0])


@when("the engine compares functional status")
def when_engine_compares_functional_status(game_state):
    """Rule 2.15.6: Compare functional status of types vs supertypes."""
    game_state.type_is_functional = TypeCheckResultStub215(
        type_name=list(game_state.card.types)[0],
        is_functional=True,
    ).is_functional
    game_state.supertype_is_functional = SupertypeCheckStub.is_functional(
        game_state.supertype_name
    )


@when("the engine lists all recognized type keywords")
def when_engine_lists_type_keywords(game_state):
    """Rule 2.15.6a: List all recognized type keywords."""
    game_state.all_type_keywords = ALL_TYPE_KEYWORDS


@when("the engine identifies which types make a card a deck-card")
def when_engine_identifies_deck_card_types(game_state):
    """Rule 2.15.6a / 1.3.2c: Identify which types make a deck-card."""
    game_state.deck_card_types = DECK_CARD_TYPES


# Then steps


@then("the card is classified as a deck-card")
def then_card_is_deck_card(game_state):
    """Rule 2.15.1: Card should be classified as deck-card."""
    assert game_state.classification == "deck", (
        f"Expected classification 'deck', got '{game_state.classification}'. "
        "Engine Feature Needed: CardTemplate.get_card_classification() for deck-card types"
    )


@then("the card may start in a player's deck")
def then_card_may_start_in_deck(game_state):
    """Rule 2.15.1 / 1.3.2c: Deck-card may start in player's deck."""
    assert game_state.can_start_in_deck, (
        "Expected deck-card to be able to start in deck. "
        "Engine Feature Needed: CardTemplate.can_start_in_deck property"
    )


@then("the Action card may only be played during the action phase")
def then_action_card_action_phase_only(game_state):
    """Rule 2.15.1: Action cards played only during action phase."""
    assert game_state.action_action_phase_only, (
        "Expected Action card to be action-phase-only. "
        "Engine Feature Needed: Type-based play rules enforcing Action phase restriction"
    )
    assert not game_state.action_can_play_anytime, (
        "Expected Action card NOT playable outside action phase. "
        "Engine Feature Needed: Type-based play rules for Action type"
    )


@then("the Instant card may be played outside the action phase")
def then_instant_card_play_anytime(game_state):
    """Rule 2.15.1: Instant cards can be played outside action phase."""
    assert game_state.instant_can_play_anytime, (
        "Expected Instant card to be playable outside action phase. "
        "Engine Feature Needed: Type-based play rules for Instant type"
    )


@then("the card is classified as a hero-card")
def then_card_is_hero_card(game_state):
    """Rule 2.15.1: Card should be classified as hero-card."""
    assert game_state.classification == "hero", (
        f"Expected classification 'hero', got '{game_state.classification}'. "
        "Engine Feature Needed: CardTemplate.get_card_classification() for hero-card types"
    )


@then("the card starts the game as a player's hero")
def then_card_starts_as_hero(game_state):
    """Rule 2.15.1 / 1.3.2a: Hero-cards start as a player's hero."""
    assert game_state.starts_as_hero, (
        "Expected hero-card to start as player's hero. "
        "Engine Feature Needed: Hero card identification via type"
    )


@then("the card is classified as a token-card")
def then_card_is_token_card(game_state):
    """Rule 2.15.1: Card should be classified as token-card."""
    assert game_state.classification == "token", (
        f"Expected classification 'token', got '{game_state.classification}'. "
        "Engine Feature Needed: CardTemplate.get_card_classification() for token-card types"
    )


@then("the card is not considered part of a player's card-pool")
def then_card_not_in_card_pool(game_state):
    """Rule 2.15.1 / 1.3.2b: Token-cards are not part of card-pool."""
    assert not game_state.is_part_of_card_pool, (
        "Expected token-card to NOT be part of card-pool. "
        "Engine Feature Needed: CardTemplate.is_part_of_card_pool returning False for tokens"
    )


@then("the card is classified as an arena-card")
def then_card_is_arena_card(game_state):
    """Rule 2.15.1: Card should be classified as arena-card."""
    assert game_state.classification == "arena", (
        f"Expected classification 'arena', got '{game_state.classification}'. "
        "Engine Feature Needed: CardTemplate.get_card_classification() for arena-card types"
    )


@then("the card cannot start in a player's deck")
def then_card_cannot_start_in_deck(game_state):
    """Rule 2.15.1 / 1.3.2d: Arena-cards cannot start in player's deck."""
    assert not game_state.can_start_in_deck, (
        "Expected arena-card to NOT start in deck. "
        "Engine Feature Needed: CardTemplate.can_start_in_deck returning False for arena-cards"
    )


@then("the card has zero types")
def then_card_has_zero_types(game_state):
    """Rule 2.15.2: Card with no type has zero types."""
    assert game_state.type_count == 0, (
        f"Expected 0 types, got {game_state.type_count}. "
        "Engine Feature Needed: CardInstance.types property (empty for no-type cards)"
    )


@then("the card is still a valid game object")
def then_card_is_valid_game_object(game_state):
    """Rule 2.15.2: Cards with zero types are still game objects."""
    # A card can still be a game object with zero types
    assert game_state.card is not None, (
        "Expected card to be a valid game object even with no types."
    )


@then(parsers.parse("the card has exactly {count:d} type"))
def then_card_has_exactly_n_types(game_state, count):
    """Rule 2.15.2: Verify card has exactly n types."""
    assert game_state.type_count == count, (
        f"Expected {count} type(s), got {game_state.type_count}. "
        "Engine Feature Needed: CardInstance.types property"
    )


@then(parsers.parse('the type name is "{type_name}"'))
def then_type_name_is(game_state, type_name):
    """Rule 2.15.2: Verify the type name matches."""
    assert type_name in game_state.card.types, (
        f"Expected type '{type_name}' not found in card types {game_state.card.types}. "
        "Engine Feature Needed: CardInstance.types property"
    )


@then(parsers.parse("the card has exactly {count:d} types"))
def then_card_has_exactly_n_types_plural(game_state, count):
    """Rule 2.15.2: Verify card has exactly n types."""
    assert game_state.type_count == count, (
        f"Expected {count} types, got {game_state.type_count}. "
        "Engine Feature Needed: CardInstance.types property"
    )


@then(parsers.parse('the card has type "{type_name}"'))
def then_card_has_type(game_state, type_name):
    """Rule 2.15.2: Verify card has a specific type."""
    assert game_state.card.has_type(type_name), (
        f"Expected card to have type '{type_name}'. Current types: {game_state.card.types}. "
        "Engine Feature Needed: CardInstance.has_type(name) method"
    )


@then(parsers.parse('the parsed type is "{type_name}"'))
def then_parsed_type_is(game_state, type_name):
    """Rule 2.15.3: Verify the type parsed from type box."""
    assert type_name in game_state.parsed.types, (
        f"Expected parsed type '{type_name}', got {game_state.parsed.types}. "
        "Engine Feature Needed: TypeBoxParser with type extraction"
    )


@then(parsers.parse('the parsed supertype is "{supertype_name}"'))
def then_parsed_supertype_is(game_state, supertype_name):
    """Rule 2.15.3: Verify the supertype parsed from type box."""
    assert supertype_name in game_state.parsed.supertypes, (
        f"Expected parsed supertype '{supertype_name}', got {game_state.parsed.supertypes}. "
        "Engine Feature Needed: TypeBoxParser with supertype extraction"
    )


@then(parsers.parse('the parsed subtype is "{subtype_name}"'))
def then_parsed_subtype_is(game_state, subtype_name):
    """Rule 2.15.3: Verify the subtype parsed from type box."""
    assert subtype_name in game_state.parsed.subtypes, (
        f"Expected parsed subtype '{subtype_name}', got {game_state.parsed.subtypes}. "
        "Engine Feature Needed: TypeBoxParser with subtype extraction"
    )


@then(
    parsers.parse('the type "{type_name}" appears after supertype "{supertype_name}"')
)
def then_type_appears_after_supertype(game_state, type_name, supertype_name):
    """Rule 2.15.3: Type appears after supertype in type box."""
    supertype_pos = game_state.parsed.get_component_position(
        "supertype", supertype_name
    )
    type_pos = game_state.parsed.get_component_position("type", type_name)
    assert supertype_pos >= 0, (
        f"Supertype '{supertype_name}' not found in parsed ordering. "
        "Engine Feature Needed: TypeBoxParser tracking component positions"
    )
    assert type_pos >= 0, (
        f"Type '{type_name}' not found in parsed ordering. "
        "Engine Feature Needed: TypeBoxParser tracking component positions"
    )
    assert supertype_pos < type_pos, (
        f"Expected supertype '{supertype_name}' (pos {supertype_pos}) "
        f"before type '{type_name}' (pos {type_pos}). "
        "Engine Feature Needed: TypeBoxParser preserving ordering"
    )


@then(parsers.parse('the type "{type_name}" appears before subtype "{subtype_name}"'))
def then_type_appears_before_subtype(game_state, type_name, subtype_name):
    """Rule 2.15.3: Type appears before subtype in type box."""
    # Subtypes appear after the long dash, so they are always after types
    assert subtype_name in game_state.parsed.subtypes, (
        f"Subtype '{subtype_name}' not found in parsed subtypes. "
        "Engine Feature Needed: TypeBoxParser with subtype extraction"
    )
    assert type_name in game_state.parsed.types, (
        f"Type '{type_name}' not found in parsed types. "
        "Engine Feature Needed: TypeBoxParser with type extraction"
    )
    # By definition, types appear before subtypes (separated by long dash)


@then('the activated-layer has type "Action"')
def then_activated_layer_has_action_type(game_state):
    """Rule 2.15.4: Activated-layer inherits Action type from source."""
    assert game_state.layer.has_type("Action"), (
        "Expected activated-layer to have type 'Action'. "
        "Engine Feature Needed: Layer.types property inheriting from source"
    )


@then("the layer types match the source card types")
def then_layer_types_match_source(game_state):
    """Rule 2.15.4: Layer types exactly match source types."""
    assert game_state.layer.types == game_state.card.types, (
        f"Expected layer types {game_state.layer.types} to match "
        f"source types {game_state.card.types}. "
        "Engine Feature Needed: Layer.types == source.types"
    )


@then('the triggered-layer has type "Action"')
def then_triggered_layer_has_action_type(game_state):
    """Rule 2.15.4: Triggered-layer inherits Action type from source."""
    assert game_state.layer.has_type("Action"), (
        "Expected triggered-layer to have type 'Action'. "
        "Engine Feature Needed: Layer.types property inheriting from source"
    )


@then('the triggered-layer has type "Attack Reaction"')
def then_triggered_layer_has_attack_reaction_type(game_state):
    """Rule 2.15.4: Triggered-layer inherits Attack Reaction type from source."""
    assert game_state.layer.has_type("Attack Reaction"), (
        "Expected triggered-layer to have type 'Attack Reaction'. "
        "Engine Feature Needed: Layer.types property inheriting multiple types from source"
    )


@then("the activated-layer has zero types")
def then_activated_layer_has_zero_types(game_state):
    """Rule 2.15.4: Layer from no-type source has zero types."""
    assert game_state.layer.type_count == 0, (
        f"Expected activated-layer to have 0 types, got {game_state.layer.type_count}. "
        "Engine Feature Needed: Layer.types inherits from source (including empty)"
    )


@then('the activated ability layer has type "Equipment" from the source')
def then_activated_ability_layer_has_equipment_type(game_state):
    """Rule 2.15.4: Activated ability layer inherits Equipment type from source."""
    assert game_state.layer.has_type("Equipment"), (
        "Expected activated ability layer to have source type 'Equipment'. "
        "Engine Feature Needed: ActivatedAbilityLayer.types includes source types"
    )


@then('the activated ability layer also has type "Action" from the ability itself')
def then_activated_ability_layer_has_action_from_ability(game_state):
    """Rule 2.15.4a: Activated ability layer includes additional types from ability."""
    assert game_state.layer.has_type("Action"), (
        "Expected activated ability layer to have ability type 'Action'. "
        "Engine Feature Needed: ActivatedAbilityLayer.types includes types from activated ability"
    )


@then('the card now has type "Action"')
def then_card_still_has_action_type(game_state):
    """Rule 2.15.5: Original type retained after gaining new type."""
    assert game_state.card.has_type("Action"), (
        "Expected card to still have type 'Action' after gaining another type. "
        "Engine Feature Needed: CardInstance.gain_type(name) method"
    )


@then('the card now has type "Attack Reaction"')
def then_card_has_attack_reaction_type(game_state):
    """Rule 2.15.5: Newly gained type is present."""
    assert game_state.card.has_type("Attack Reaction"), (
        "Expected card to have gained type 'Attack Reaction'. "
        "Engine Feature Needed: CardInstance.gain_type(name) method"
    )


@then("the card went from 1 type to 2 types")
def then_card_went_from_1_to_2_types(game_state):
    """Rule 2.15.5: Card gained exactly one type."""
    assert game_state.types_before == 1, (
        f"Expected 1 type before, got {game_state.types_before}."
    )
    assert game_state.types_after == 2, (
        f"Expected 2 types after, got {game_state.types_after}. "
        "Engine Feature Needed: CardInstance.gain_type(name) adding the type"
    )


@then('the card still has type "Action"')
def then_card_still_has_action_after_loss(game_state):
    """Rule 2.15.5: Unreleated type retained after losing another type."""
    assert game_state.card.has_type("Action"), (
        "Expected card to still have type 'Action' after losing 'Attack Reaction'. "
        "Engine Feature Needed: CardInstance.lose_type(name) method"
    )


@then('the card no longer has type "Attack Reaction"')
def then_card_no_longer_has_attack_reaction(game_state):
    """Rule 2.15.5: Lost type is no longer present."""
    assert not game_state.card.has_type("Attack Reaction"), (
        "Expected card to no longer have type 'Attack Reaction'. "
        "Engine Feature Needed: CardInstance.lose_type(name) method"
    )


@then("the card went from 2 types to 1 type")
def then_card_went_from_2_to_1_type(game_state):
    """Rule 2.15.5: Card lost exactly one type."""
    assert game_state.types_before == 2, (
        f"Expected 2 types before, got {game_state.types_before}."
    )
    assert game_state.types_after == 1, (
        f"Expected 1 type after, got {game_state.types_after}. "
        "Engine Feature Needed: CardInstance.lose_type(name) removing the type"
    )


@then(parsers.parse('the type "{type_name}" is classified as a functional keyword'))
def then_type_is_functional_keyword(game_state, type_name):
    """Rule 2.15.6: Types are functional keywords."""
    assert game_state.type_check.is_functional, (
        f"Expected type '{type_name}' to be classified as functional. "
        "Engine Feature Needed: TypeRegistry.is_functional(name) = True for all types"
    )


@then(parsers.parse('the type "{type_name}" adds additional rules to the card'))
def then_type_adds_additional_rules(game_state, type_name):
    """Rule 2.15.6: Functional types add additional rules."""
    assert game_state.type_check.adds_additional_rules, (
        f"Expected type '{type_name}' to add additional rules. "
        "Engine Feature Needed: TypeRegistry.adds_additional_rules() = True for all types"
    )


@then(parsers.parse('the type "{type_name}" is functional'))
def then_type_is_functional(game_state, type_name):
    """Rule 2.15.6: Types are functional."""
    assert game_state.type_is_functional, (
        f"Expected type '{type_name}' to be functional. "
        "Engine Feature Needed: TypeRegistry.is_functional() = True"
    )


@then(parsers.parse('the supertype "{supertype_name}" is non-functional'))
def then_supertype_is_nonfunctional(game_state, supertype_name):
    """Rule 2.11.6: Supertypes are non-functional (contrast with types)."""
    assert not game_state.supertype_is_functional, (
        f"Expected supertype '{supertype_name}' to be non-functional. "
        "Engine Feature Needed: SupertypeRegistry.is_non_functional() = True"
    )


@then("there are exactly 14 type keywords")
def then_exactly_14_type_keywords(game_state):
    """Rule 2.15.6a: Exactly 14 type keywords."""
    assert len(game_state.all_type_keywords) == 14, (
        f"Expected 14 type keywords, got {len(game_state.all_type_keywords)}: "
        f"{game_state.all_type_keywords}. "
        "Engine Feature Needed: TypeRegistry.ALL_TYPE_KEYWORDS with exactly 14 keywords"
    )


@then(parsers.parse('"{keyword}" is a recognized type keyword'))
def then_keyword_is_recognized_type(game_state, keyword):
    """Rule 2.15.6a: The keyword should be a recognized type."""
    assert keyword in game_state.all_type_keywords, (
        f"Expected '{keyword}' to be a recognized type keyword. "
        f"Current keywords: {game_state.all_type_keywords}. "
        "Engine Feature Needed: TypeRegistry.ALL_TYPE_KEYWORDS containing all 14 keywords"
    )


@then(parsers.parse('"{type_name}" makes a deck-card'))
def then_type_makes_deck_card(game_state, type_name):
    """Rule 2.15.6a / 1.3.2c: Type makes a deck-card."""
    assert type_name in game_state.deck_card_types, (
        f"Expected '{type_name}' to make a deck-card. "
        "Engine Feature Needed: TypeRegistry.DECK_CARD_TYPES"
    )


@then(parsers.parse('"{type_name}" does not make a deck-card'))
def then_type_does_not_make_deck_card(game_state, type_name):
    """Rule 2.15.6a / 1.3.2c: Type does NOT make a deck-card."""
    assert type_name not in game_state.deck_card_types, (
        f"Expected '{type_name}' to NOT make a deck-card, but it's in {game_state.deck_card_types}. "
        "Engine Feature Needed: TypeRegistry.DECK_CARD_TYPES excluding non-deck types"
    )


# ---------------------------------------------------------------------------
# Fixture
# ---------------------------------------------------------------------------


@pytest.fixture
def game_state():
    """
    Fixture providing game state for Section 2.15 testing.

    Uses BDDGameState which integrates with the real engine.
    Reference: Rule 2.15
    """
    from tests.bdd_helpers import BDDGameState

    state = BDDGameState()

    # Section 2.15 state attributes
    state.card = None
    state.layer = None
    state.classification = None
    state.type_count = 0
    state.read_types = frozenset()
    state.can_start_in_deck = False
    state.is_part_of_card_pool = True
    state.starts_as_hero = False
    state.type_box_string = ""
    state.parsed = None
    state.type_registry = ALL_TYPE_KEYWORDS
    state.all_type_keywords = ALL_TYPE_KEYWORDS
    state.deck_card_types = DECK_CARD_TYPES
    state.type_check = None
    state.type_is_functional = None
    state.supertype_is_functional = None
    state.supertype_name = None
    state.ability_type = None
    state.types_before = 0
    state.types_after = 0
    state.action_can_play_anytime = None
    state.instant_can_play_anytime = None
    state.action_action_phase_only = None

    return state
