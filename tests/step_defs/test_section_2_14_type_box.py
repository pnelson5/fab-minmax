"""
Step definitions for Section 2.14: Type Box
Reference: Flesh and Blood Comprehensive Rules Section 2.14

This module implements behavioral tests for type box parsing rules in Flesh and Blood.

Rule 2.14.1: The type box of a card determines the card's metatypes, supertypes,
             types, and subtypes, typically located at the bottom of the card.
             Type boxes are typically written in the format
             "[METATYPES] [SUPERTYPES] [TYPE] [--- SUBTYPES]," where METATYPES
             is zero or more metatypes, SUPERTYPES is zero or more supertypes,
             TYPE is zero or more types, and SUBTYPES is zero or more subtypes.

Rule 2.14.1a: If the SUPERTYPES of a type box is "Generic," the card has no
              supertypes.

Rule 2.14.1b: Hybrid cards are cards with SUPERTYPES written in the format
              "[SUPERTYPES-1] / [SUPERTYPES-2]." A hybrid card can be included
              in a player's card-pool as though it only has one of the supertypes
              sets, SUPERTYPES-1 or SUPERTYPES-2, not both. [1.1.3] Otherwise,
              hybrid cards have all of the supertypes specified by SUPERTYPES-1
              and SUPERTYPES-2.

Engine Features Needed for Section 2.14:
- [ ] `TypeBoxParser.parse(type_box_str)` returning parsed components (Rule 2.14.1)
- [ ] `TypeBoxParseResult.metatypes` frozenset (Rule 2.14.1)
- [ ] `TypeBoxParseResult.supertypes` frozenset (Rule 2.14.1)
- [ ] `TypeBoxParseResult.types` frozenset (Rule 2.14.1)
- [ ] `TypeBoxParseResult.subtypes` frozenset (Rule 2.14.1)
- [ ] `TypeBoxParseResult.is_generic` returning True when "Generic" is SUPERTYPES (Rule 2.14.1a)
- [ ] `TypeBoxParseResult.is_hybrid` returning True when "/" separates supertype sets (Rule 2.14.1b)
- [ ] `HybridCard.supertype_set_1` and `HybridCard.supertype_set_2` frozensets (Rule 2.14.1b)
- [ ] `HybridCardPoolEligibility.check(card, hero)` checking either set (Rule 2.14.1b)
- [ ] `CardTemplate.type_box` property storing the raw type box string (Rule 2.14.1)
"""

import pytest
from pytest_bdd import scenario, given, when, then, parsers
from dataclasses import dataclass, field
from typing import Optional, FrozenSet, List


# ---------------------------------------------------------------------------
# Stub classes for testing Section 2.14 rules
# ---------------------------------------------------------------------------

# Known metatypes (hero monikers and set identifiers)
KNOWN_METATYPES = frozenset(
    {
        "Dorinthea",
        "Katsu",
        "Bravo",
        "Rhinar",
        "Lexi",
        "Prism",
        "Kano",
        "Shiyana",
        "Boltyn",
        "Iyslander",
        "Dromai",
    }
)

# Known type keywords
KNOWN_TYPES = frozenset(
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

# Known supertype keywords (classes and talents)
KNOWN_SUPERTYPES = frozenset(
    {
        # Classes
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
        "Wizard",
        # Talents
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
        "Shadow",
    }
)

# Known subtype keywords
KNOWN_SUBTYPES = frozenset(
    {
        "(1H)",
        "(2H)",
        "Affliction",
        "Ally",
        "Angel",
        "Arms",
        "Arrow",
        "Ash",
        "Attack",
        "Aura",
        "Axe",
        "Base",
        "Book",
        "Bow",
        "Construct",
        "Dagger",
        "Figment",
        "Head",
        "Invocation",
        "Item",
        "Landmark",
        "Off-Hand",
        "Quiver",
        "Staff",
        "Sword",
    }
)


@dataclass
class TypeBoxParseResult214:
    """
    Result of parsing a type box string.

    Models what the engine's TypeBoxParser must implement per Rule 2.14.1.

    Engine Feature Needed:
    - [ ] TypeBoxParser.parse(type_box_str) -> TypeBoxParseResult (Rule 2.14.1)
    """

    _type_box_str: str = ""
    metatypes: FrozenSet[str] = field(default_factory=frozenset)
    supertypes: FrozenSet[str] = field(default_factory=frozenset)
    types: FrozenSet[str] = field(default_factory=frozenset)
    subtypes: FrozenSet[str] = field(default_factory=frozenset)
    is_generic: bool = False
    is_hybrid: bool = False
    _supertype_set_1: FrozenSet[str] = field(default_factory=frozenset)
    _supertype_set_2: FrozenSet[str] = field(default_factory=frozenset)
    _ordering: List[str] = field(default_factory=list)

    @classmethod
    def parse(cls, type_box_str: str) -> "TypeBoxParseResult214":
        """
        Parse a type box string into components.

        Rule 2.14.1: Format is "[METATYPES] [SUPERTYPES] [TYPE] [--- SUBTYPES]"
        Rule 2.14.1a: "Generic" in SUPERTYPES position means no supertypes
        Rule 2.14.1b: "/" in SUPERTYPES position indicates hybrid card

        Engine Feature Needed:
        - [ ] TypeBoxParser.parse(type_box_str) -> TypeBoxParseResult (Rule 2.14.1)
        """
        # Split on long dash to separate type/subtype part
        if " - " in type_box_str:
            pre_dash, subtypes_str = type_box_str.split(" - ", 1)
            subtypes_parsed = frozenset(subtypes_str.split())
        else:
            pre_dash = type_box_str
            subtypes_parsed = frozenset()

        tokens = pre_dash.split()

        metatypes = []
        supertypes_tokens = []
        types_found = []
        ordering = []

        is_generic = False
        is_hybrid = False
        supertype_set_1 = frozenset()
        supertype_set_2 = frozenset()

        # Check for hybrid: contains "/" separator
        if "/" in pre_dash:
            # Hybrid format: e.g., "Warrior / Wizard Action - Attack"
            # Find the type in tokens (last known type keyword)
            type_token = None
            for t in tokens:
                if t in KNOWN_TYPES:
                    type_token = t
                    break
            # Split into supertype part and type part
            if type_token:
                type_idx = tokens.index(type_token)
                supertype_part = " ".join(tokens[:type_idx])
                types_found = [type_token]
            else:
                supertype_part = " ".join(tokens)
                types_found = []

            # Parse supertype sets from "/" separated format
            # Find metatypes before the supertype sets
            # Heuristic: metatypes are known metatype keywords
            supertype_part_tokens = supertype_part.split()
            meta_in_super = []
            st_tokens = []
            for t in supertype_part_tokens:
                if t == "/":
                    st_tokens.append(t)
                elif t in KNOWN_METATYPES:
                    meta_in_super.append(t)
                else:
                    st_tokens.append(t)
            metatypes.extend(meta_in_super)

            # Now find the "/" in st_tokens to split into two sets
            if "/" in st_tokens:
                slash_idx = st_tokens.index("/")
                set1_tokens = [t for t in st_tokens[:slash_idx] if t]
                set2_tokens = [t for t in st_tokens[slash_idx + 1 :] if t]
                supertype_set_1 = frozenset(set1_tokens)
                supertype_set_2 = frozenset(set2_tokens)
                supertypes_parsed_final = supertype_set_1 | supertype_set_2
            else:
                supertypes_parsed_final = frozenset(st_tokens)

            is_hybrid = True
            ordering = (
                list(meta_in_super)
                + ["[HYBRID_SUPERTYPES]"]
                + types_found
                + list(subtypes_parsed)
            )

        else:
            # Non-hybrid: parse tokens left to right
            # Metatypes appear before supertypes which appear before types
            # Heuristic: metatypes are known metatype keywords,
            #            supertypes are known supertype keywords,
            #            types are known type keywords

            for token in tokens:
                if token in KNOWN_TYPES:
                    types_found.append(token)
                    ordering.append(token)
                elif token in KNOWN_SUPERTYPES:
                    supertypes_tokens.append(token)
                    ordering.append(token)
                elif token in KNOWN_METATYPES:
                    metatypes.append(token)
                    ordering.append(token)
                elif token == "Generic":
                    is_generic = True
                    ordering.append(token)
                # else: unknown token, skip

            supertypes_parsed_final = (
                frozenset(supertypes_tokens) if not is_generic else frozenset()
            )

        ordering_with_subtypes = ordering + list(subtypes_parsed)

        return cls(
            _type_box_str=type_box_str,
            metatypes=frozenset(metatypes),
            supertypes=supertypes_parsed_final,
            types=frozenset(types_found),
            subtypes=subtypes_parsed,
            is_generic=is_generic,
            is_hybrid=is_hybrid,
            _supertype_set_1=supertype_set_1,
            _supertype_set_2=supertype_set_2,
            _ordering=ordering_with_subtypes,
        )

    @property
    def supertype_set_1(self) -> FrozenSet[str]:
        """Rule 2.14.1b: First hybrid supertype set."""
        return self._supertype_set_1

    @property
    def supertype_set_2(self) -> FrozenSet[str]:
        """Rule 2.14.1b: Second hybrid supertype set."""
        return self._supertype_set_2

    def index_in_ordering(self, keyword: str) -> int:
        """Helper to find the ordering position of a keyword."""
        try:
            return self._ordering.index(keyword)
        except ValueError:
            # For "[HYBRID_SUPERTYPES]" placeholder
            return -1


@dataclass
class HeroStub214:
    """
    Stub representing a hero for card-pool eligibility testing.

    Engine Feature Needed:
    - [ ] Hero.supertypes frozenset (Rules 1.1.3, 2.14.1b)
    """

    name: str
    supertypes: FrozenSet[str] = field(default_factory=frozenset)


@dataclass
class HybridCardPoolCheckResult214:
    """
    Result of checking hybrid card eligibility for a card-pool.

    Rule 2.14.1b: Hybrid card can be included if EITHER set is a subset.

    Engine Feature Needed:
    - [ ] HybridCardPoolEligibility.check(card, hero) (Rule 2.14.1b)
    """

    is_eligible: bool
    matching_set: Optional[int]  # 1 or 2 if a set matches, None if neither
    reason: str


def check_hybrid_card_pool_eligibility(
    supertype_set_1: FrozenSet[str],
    supertype_set_2: FrozenSet[str],
    hero_supertypes: FrozenSet[str],
) -> HybridCardPoolCheckResult214:
    """
    Check if a hybrid card is eligible for a hero's card-pool.

    Rule 2.14.1b: A hybrid card can be included in a player's card-pool
    as though it only has one of the supertype sets, SUPERTYPES-1 or
    SUPERTYPES-2, not both. [1.1.3]

    Engine Feature Needed:
    - [ ] HybridCardPoolEligibility.check(hybrid_card, hero) (Rule 2.14.1b)
    """
    set1_match = supertype_set_1.issubset(hero_supertypes)
    set2_match = supertype_set_2.issubset(hero_supertypes)

    if set1_match:
        return HybridCardPoolCheckResult214(
            is_eligible=True,
            matching_set=1,
            reason=f"Supertype set 1 {supertype_set_1} is a subset of hero's supertypes {hero_supertypes}",
        )
    elif set2_match:
        return HybridCardPoolCheckResult214(
            is_eligible=True,
            matching_set=2,
            reason=f"Supertype set 2 {supertype_set_2} is a subset of hero's supertypes {hero_supertypes}",
        )
    else:
        return HybridCardPoolCheckResult214(
            is_eligible=False,
            matching_set=None,
            reason=f"Neither supertype set {supertype_set_1} nor {supertype_set_2} is a subset of hero's supertypes {hero_supertypes}",
        )


# ---------------------------------------------------------------------------
# Scenario functions
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_14_type_box.feature",
    "Type box determines all card classification components",
)
def test_type_box_determines_all_card_classification_components():
    """Rule 2.14.1: Type box determines all classification components."""
    pass


@scenario(
    "../features/section_2_14_type_box.feature",
    "Type box with a metatype component",
)
def test_type_box_with_a_metatype_component():
    """Rule 2.14.1: Type box can include a metatype before supertypes."""
    pass


@scenario(
    "../features/section_2_14_type_box.feature",
    "Type box with no subtypes component",
)
def test_type_box_with_no_subtypes_component():
    """Rule 2.14.1: Type box can have no subtypes (no long dash)."""
    pass


@scenario(
    "../features/section_2_14_type_box.feature",
    "Type box components appear in correct order",
)
def test_type_box_components_appear_in_correct_order():
    """Rule 2.14.1: Type box format order is metatypes, supertypes, type, subtypes."""
    pass


@scenario(
    "../features/section_2_14_type_box.feature",
    "Type box with only a type",
)
def test_type_box_with_only_a_type():
    """Rule 2.14.1: Type box can consist of just a type with no other components."""
    pass


@scenario(
    "../features/section_2_14_type_box.feature",
    "Type box with multiple supertypes",
)
def test_type_box_with_multiple_supertypes():
    """Rule 2.14.1: Multiple supertypes can appear in the type box."""
    pass


@scenario(
    "../features/section_2_14_type_box.feature",
    "Type box with multiple subtypes",
)
def test_type_box_with_multiple_subtypes():
    """Rule 2.14.1: Multiple subtypes can appear after the long dash."""
    pass


@scenario(
    "../features/section_2_14_type_box.feature",
    "Generic type box means card has no supertypes",
)
def test_generic_type_box_means_card_has_no_supertypes():
    """Rule 2.14.1a: 'Generic' in type box means no supertypes."""
    pass


@scenario(
    "../features/section_2_14_type_box.feature",
    "Generic keyword is not a supertype",
)
def test_generic_keyword_is_not_a_supertype():
    """Rule 2.14.1a: 'Generic' is not itself a supertype, it means zero supertypes."""
    pass


@scenario(
    "../features/section_2_14_type_box.feature",
    "Generic type box is equivalent to having zero supertypes",
)
def test_generic_type_box_is_equivalent_to_having_zero_supertypes():
    """Rule 2.14.1a: A 'Generic' card and a card with no supertypes both have zero supertypes."""
    pass


@scenario(
    "../features/section_2_14_type_box.feature",
    "Hybrid card has slash-separated supertype sets",
)
def test_hybrid_card_has_slash_separated_supertype_sets():
    """Rule 2.14.1b: Hybrid card supertype format is '[SUPERTYPES-1] / [SUPERTYPES-2]'."""
    pass


@scenario(
    "../features/section_2_14_type_box.feature",
    "Hybrid card can be included in card-pool matching first supertype set",
)
def test_hybrid_card_can_be_included_in_card_pool_matching_first_supertype_set():
    """Rule 2.14.1b: Hybrid card eligible if first supertype set is subset of hero's supertypes."""
    pass


@scenario(
    "../features/section_2_14_type_box.feature",
    "Hybrid card can be included in card-pool matching second supertype set",
)
def test_hybrid_card_can_be_included_in_card_pool_matching_second_supertype_set():
    """Rule 2.14.1b: Hybrid card eligible if second supertype set is subset of hero's supertypes."""
    pass


@scenario(
    "../features/section_2_14_type_box.feature",
    "Hybrid card cannot be included in card-pool when neither supertype set matches",
)
def test_hybrid_card_cannot_be_included_when_neither_set_matches():
    """Rule 2.14.1b: Hybrid card not eligible if neither supertype set is subset."""
    pass


@scenario(
    "../features/section_2_14_type_box.feature",
    "Hybrid card card-pool check uses only one supertype set at a time",
)
def test_hybrid_card_card_pool_check_uses_only_one_supertype_set_at_a_time():
    """Rule 2.14.1b: Card-pool check evaluates each set independently, not combined."""
    pass


@scenario(
    "../features/section_2_14_type_box.feature",
    "Hybrid card has all supertypes outside of card-pool eligibility check",
)
def test_hybrid_card_has_all_supertypes_outside_card_pool_check():
    """Rule 2.14.1b: Outside card-pool check, hybrid card has all supertypes from both sets."""
    pass


@scenario(
    "../features/section_2_14_type_box.feature",
    "Hybrid card with multi-supertype sets matches if either set is a subset",
)
def test_hybrid_card_with_multi_supertype_sets_matches_if_either_is_subset():
    """Rule 2.14.1b: Multi-supertype sets - either set must be fully a subset."""
    pass


@scenario(
    "../features/section_2_14_type_box.feature",
    "Hybrid card with partial set match is not eligible",
)
def test_hybrid_card_with_partial_set_match_is_not_eligible():
    """Rule 2.14.1b: Partial match of a supertype set is not enough for eligibility."""
    pass


# ---------------------------------------------------------------------------
# Given steps
# ---------------------------------------------------------------------------


@given(parsers.parse('a card with type box "{type_box}"'))
def given_card_with_type_box(game_state, type_box):
    """Rule 2.14.1: Card has a type box string."""
    game_state.type_box_str = type_box
    game_state.parse_result = None


@given("a card with no printed traits")
def given_card_with_no_printed_traits(game_state):
    """Used as auxiliary step context; not the primary action here."""
    game_state.second_type_box_str = None


@given(parsers.parse('a card with type box "{type_box2}" for comparison'))
def given_second_card_with_type_box(game_state, type_box2):
    """Second card type box for comparison scenarios."""
    game_state.second_type_box_str = type_box2
    game_state.second_parse_result = None


@given(parsers.parse('a card with type box "{type_box2}"'), target_fixture="game_state")
def given_second_card_type_box_comparison(game_state, type_box2):
    """Rule 2.14.1a: Second card for generic comparison."""
    if not hasattr(game_state, "type_box_str"):
        game_state.type_box_str = type_box2
    else:
        game_state.second_type_box_str = type_box2
    return game_state


@given(parsers.parse('a hybrid card with supertype sets "{set1}" and "{set2}"'))
def given_hybrid_card_with_two_supertype_sets(game_state, set1, set2):
    """Rule 2.14.1b: Hybrid card defined by two supertype sets."""
    game_state.hybrid_supertype_set_1 = frozenset(set1.split())
    game_state.hybrid_supertype_set_2 = frozenset(set2.split())
    game_state.hybrid_card_parse_result = None


@given(parsers.parse("a Warrior hero"))
def given_warrior_hero(game_state):
    """Rule 2.14.1b: Hero with Warrior supertype."""
    game_state.hero = HeroStub214(name="Dorinthea", supertypes=frozenset({"Warrior"}))


@given(parsers.parse("a Wizard hero"))
def given_wizard_hero(game_state):
    """Rule 2.14.1b: Hero with Wizard supertype."""
    game_state.hero = HeroStub214(name="Kano", supertypes=frozenset({"Wizard"}))


@given(parsers.parse("a Ninja hero"))
def given_ninja_hero(game_state):
    """Rule 2.14.1b: Hero with Ninja supertype."""
    game_state.hero = HeroStub214(name="Katsu", supertypes=frozenset({"Ninja"}))


@given(parsers.parse("a Warrior hero without the Wizard supertype"))
def given_warrior_hero_without_wizard(game_state):
    """Rule 2.14.1b: Hero with only Warrior supertype (not Wizard)."""
    game_state.hero = HeroStub214(name="Bravo", supertypes=frozenset({"Warrior"}))


@given(
    parsers.parse(
        'a hybrid card with supertype set 1 "{set1}" and supertype set 2 "{set2}"'
    )
)
def given_hybrid_card_with_multi_supertype_sets(game_state, set1, set2):
    """Rule 2.14.1b: Hybrid card with multi-word supertype sets."""
    game_state.hybrid_supertype_set_1 = frozenset(set1.split())
    game_state.hybrid_supertype_set_2 = frozenset(set2.split())


@given(parsers.parse('a hero with supertypes "{st1}" and "{st2}"'))
def given_hero_with_two_supertypes(game_state, st1, st2):
    """Rule 2.14.1b: Hero with two supertypes."""
    game_state.hero = HeroStub214(
        name="TestHero",
        supertypes=frozenset({st1, st2}),
    )


@given(parsers.parse('a hero with only supertype "{st1}"'))
def given_hero_with_only_one_supertype(game_state, st1):
    """Rule 2.14.1b: Hero with only one supertype."""
    game_state.hero = HeroStub214(
        name="TestHero",
        supertypes=frozenset({st1}),
    )


# ---------------------------------------------------------------------------
# When steps
# ---------------------------------------------------------------------------


@when("the engine parses the type box")
def when_engine_parses_type_box(game_state):
    """Rule 2.14.1: Engine parses the type box string into components."""
    game_state.parse_result = TypeBoxParseResult214.parse(game_state.type_box_str)


@when("the engine parses the type box as a hybrid card")
def when_engine_parses_type_box_as_hybrid(game_state):
    """Rule 2.14.1b: Engine parses type box and identifies hybrid card."""
    game_state.parse_result = TypeBoxParseResult214.parse(game_state.type_box_str)


@when("both cards' supertypes are compared")
def when_both_cards_supertypes_compared(game_state):
    """Rule 2.14.1a: Parse both type boxes and compare their supertypes."""
    game_state.parse_result = TypeBoxParseResult214.parse(game_state.type_box_str)
    second_box = getattr(game_state, "second_type_box_str", None)
    if second_box:
        game_state.second_parse_result = TypeBoxParseResult214.parse(second_box)
    else:
        # The second type box was set via the second "a card with type box..." step
        game_state.second_parse_result = None


@when("checking if the hybrid card can be included in the Warrior hero's card-pool")
def when_checking_hybrid_card_warrior_pool(game_state):
    """Rule 2.14.1b: Check hybrid card eligibility for Warrior hero."""
    game_state.pool_check_result = check_hybrid_card_pool_eligibility(
        game_state.hybrid_supertype_set_1,
        game_state.hybrid_supertype_set_2,
        game_state.hero.supertypes,
    )


@when("checking if the hybrid card can be included in the Wizard hero's card-pool")
def when_checking_hybrid_card_wizard_pool(game_state):
    """Rule 2.14.1b: Check hybrid card eligibility for Wizard hero."""
    game_state.pool_check_result = check_hybrid_card_pool_eligibility(
        game_state.hybrid_supertype_set_1,
        game_state.hybrid_supertype_set_2,
        game_state.hero.supertypes,
    )


@when("checking if the hybrid card can be included in the Ninja hero's card-pool")
def when_checking_hybrid_card_ninja_pool(game_state):
    """Rule 2.14.1b: Check hybrid card eligibility for Ninja hero."""
    game_state.pool_check_result = check_hybrid_card_pool_eligibility(
        game_state.hybrid_supertype_set_1,
        game_state.hybrid_supertype_set_2,
        game_state.hero.supertypes,
    )


@when(
    "checking if the hybrid card can be included in the Warrior hero's card-pool",
    target_fixture="game_state",
)
def when_checking_hybrid_card_warrior_only_pool(game_state):
    """Rule 2.14.1b: Check hybrid card eligibility for Warrior-only hero."""
    game_state.pool_check_result = check_hybrid_card_pool_eligibility(
        game_state.hybrid_supertype_set_1,
        game_state.hybrid_supertype_set_2,
        game_state.hero.supertypes,
    )
    return game_state


@when("the engine evaluates the hybrid card's supertypes normally")
def when_engine_evaluates_hybrid_supertypes_normally(game_state):
    """Rule 2.14.1b: Outside card-pool check, hybrid card has all supertypes."""
    # All supertypes = union of both sets
    game_state.all_hybrid_supertypes = (
        game_state.hybrid_supertype_set_1 | game_state.hybrid_supertype_set_2
    )


@when("checking if the hybrid card can be included in that hero's card-pool")
def when_checking_hybrid_card_multi_hero_pool(game_state):
    """Rule 2.14.1b: Check hybrid card eligibility for multi-supertype hero."""
    game_state.pool_check_result = check_hybrid_card_pool_eligibility(
        game_state.hybrid_supertype_set_1,
        game_state.hybrid_supertype_set_2,
        game_state.hero.supertypes,
    )


# ---------------------------------------------------------------------------
# Then steps
# ---------------------------------------------------------------------------


@then(parsers.parse('the card has supertype "{supertype}"'))
def then_card_has_supertype(game_state, supertype):
    """Rule 2.14.1: Card supertypes include the given value."""
    parse_result = getattr(game_state, "parse_result", None)
    if parse_result:
        assert supertype in parse_result.supertypes, (
            f"Expected supertype '{supertype}' in {parse_result.supertypes}"
        )
    else:
        # For hybrid card scenarios without type box parse
        all_supertypes = getattr(game_state, "all_hybrid_supertypes", None)
        assert all_supertypes is not None, (
            "No parse result or hybrid supertypes available"
        )
        assert supertype in all_supertypes, (
            f"Expected supertype '{supertype}' in hybrid supertypes {all_supertypes}"
        )


@then(parsers.parse('the card has type "{card_type}"'))
def then_card_has_type(game_state, card_type):
    """Rule 2.14.1: Card types include the given type keyword."""
    parse_result = game_state.parse_result
    assert card_type in parse_result.types, (
        f"Expected type '{card_type}' in {parse_result.types}"
    )


@then(parsers.parse('the card has subtype "{subtype}"'))
def then_card_has_subtype(game_state, subtype):
    """Rule 2.14.1: Card subtypes include the given subtype keyword."""
    parse_result = game_state.parse_result
    assert subtype in parse_result.subtypes, (
        f"Expected subtype '{subtype}' in {parse_result.subtypes}"
    )


@then(parsers.parse('the card has metatype "{metatype}"'))
def then_card_has_metatype(game_state, metatype):
    """Rule 2.14.1: Card metatypes include the given metatype keyword."""
    parse_result = game_state.parse_result
    assert metatype in parse_result.metatypes, (
        f"Expected metatype '{metatype}' in {parse_result.metatypes}"
    )


@then("the card has no metatypes")
def then_card_has_no_metatypes(game_state):
    """Rule 2.14.1: Card has an empty metatypes set."""
    parse_result = game_state.parse_result
    assert len(parse_result.metatypes) == 0, (
        f"Expected no metatypes but got {parse_result.metatypes}"
    )


@then("the card has no supertypes")
def then_card_has_no_supertypes(game_state):
    """Rule 2.14.1/2.14.1a: Card has an empty supertypes set."""
    parse_result = game_state.parse_result
    assert len(parse_result.supertypes) == 0, (
        f"Expected no supertypes but got {parse_result.supertypes}"
    )


@then("the card has no subtypes")
def then_card_has_no_subtypes(game_state):
    """Rule 2.14.1: Card has an empty subtypes set."""
    parse_result = game_state.parse_result
    assert len(parse_result.subtypes) == 0, (
        f"Expected no subtypes but got {parse_result.subtypes}"
    )


@then("the card has zero supertypes")
def then_card_has_zero_supertypes(game_state):
    """Rule 2.14.1a: Explicitly zero supertypes (used with Generic)."""
    parse_result = game_state.parse_result
    assert len(parse_result.supertypes) == 0, (
        f"Expected zero supertypes but got {parse_result.supertypes}"
    )


@then(parsers.parse("the card has {count:d} supertypes"))
def then_card_has_n_supertypes(game_state, count):
    """Rule 2.14.1: Card has exactly N supertypes."""
    parse_result = getattr(game_state, "parse_result", None)
    if parse_result:
        assert len(parse_result.supertypes) == count, (
            f"Expected {count} supertypes but got {len(parse_result.supertypes)}: {parse_result.supertypes}"
        )
    else:
        # For hybrid card scenarios
        all_supertypes = getattr(game_state, "all_hybrid_supertypes", None)
        assert all_supertypes is not None, (
            "No parse result or hybrid supertypes available"
        )
        assert len(all_supertypes) == count, (
            f"Expected {count} supertypes but got {len(all_supertypes)}: {all_supertypes}"
        )


@then(parsers.parse("the card has {count:d} subtypes"))
def then_card_has_n_subtypes(game_state, count):
    """Rule 2.14.1: Card has exactly N subtypes."""
    parse_result = game_state.parse_result
    assert len(parse_result.subtypes) == count, (
        f"Expected {count} subtypes but got {len(parse_result.subtypes)}: {parse_result.subtypes}"
    )


@then(
    parsers.parse(
        'the type box ordering has metatype "{metatype}" before supertype "{supertype}"'
    )
)
def then_ordering_has_metatype_before_supertype(game_state, metatype, supertype):
    """Rule 2.14.1: Metatypes appear before supertypes in the type box."""
    parse_result = game_state.parse_result
    ordering = parse_result._ordering
    assert metatype in ordering, f"Metatype '{metatype}' not in ordering {ordering}"
    assert supertype in ordering, f"Supertype '{supertype}' not in ordering {ordering}"
    assert ordering.index(metatype) < ordering.index(supertype), (
        f"Expected '{metatype}' (idx {ordering.index(metatype)}) before '{supertype}' "
        f"(idx {ordering.index(supertype)}) in {ordering}"
    )


@then(
    parsers.parse(
        'the type box ordering has supertype "{supertype}" before type "{card_type}"'
    )
)
def then_ordering_has_supertype_before_type(game_state, supertype, card_type):
    """Rule 2.14.1: Supertypes appear before types in the type box."""
    parse_result = game_state.parse_result
    ordering = parse_result._ordering
    assert supertype in ordering, f"Supertype '{supertype}' not in ordering {ordering}"
    assert card_type in ordering, f"Type '{card_type}' not in ordering {ordering}"
    assert ordering.index(supertype) < ordering.index(card_type), (
        f"Expected '{supertype}' (idx {ordering.index(supertype)}) before '{card_type}' "
        f"(idx {ordering.index(card_type)}) in {ordering}"
    )


@then(
    parsers.parse(
        'the type box ordering has type "{card_type}" before subtype "{subtype}"'
    )
)
def then_ordering_has_type_before_subtype(game_state, card_type, subtype):
    """Rule 2.14.1: Types appear before subtypes in the type box."""
    parse_result = game_state.parse_result
    ordering = parse_result._ordering
    assert card_type in ordering, f"Type '{card_type}' not in ordering {ordering}"
    assert subtype in ordering, f"Subtype '{subtype}' not in ordering {ordering}"
    assert ordering.index(card_type) < ordering.index(subtype), (
        f"Expected '{card_type}' (idx {ordering.index(card_type)}) before '{subtype}' "
        f"(idx {ordering.index(subtype)}) in {ordering}"
    )


@then("the card is identified as a hybrid card")
def then_card_is_identified_as_hybrid(game_state):
    """Rule 2.14.1b: Type box with '/' is identified as a hybrid card."""
    parse_result = game_state.parse_result
    assert parse_result.is_hybrid, (
        "Expected card to be identified as a hybrid card (has '/' in type box)"
    )


@then(parsers.parse('supertype set 1 is "{set1}"'))
def then_supertype_set_1_is(game_state, set1):
    """Rule 2.14.1b: First hybrid supertype set matches the expected value."""
    parse_result = game_state.parse_result
    expected_set = frozenset(set1.split())
    assert parse_result.supertype_set_1 == expected_set, (
        f"Expected supertype set 1 to be {expected_set} but got {parse_result.supertype_set_1}"
    )


@then(parsers.parse('supertype set 2 is "{set2}"'))
def then_supertype_set_2_is(game_state, set2):
    """Rule 2.14.1b: Second hybrid supertype set matches the expected value."""
    parse_result = game_state.parse_result
    expected_set = frozenset(set2.split())
    assert parse_result.supertype_set_2 == expected_set, (
        f"Expected supertype set 2 to be {expected_set} but got {parse_result.supertype_set_2}"
    )


@then("the hybrid card is eligible for the card-pool")
def then_hybrid_card_is_eligible(game_state):
    """Rule 2.14.1b: Hybrid card can be included in the hero's card-pool."""
    result = game_state.pool_check_result
    assert result.is_eligible, (
        f"Expected hybrid card to be eligible but was not. Reason: {result.reason}"
    )


@then("the hybrid card is not eligible for the card-pool")
def then_hybrid_card_is_not_eligible(game_state):
    """Rule 2.14.1b: Hybrid card cannot be included in the hero's card-pool."""
    result = game_state.pool_check_result
    assert not result.is_eligible, (
        f"Expected hybrid card to NOT be eligible but it was. Reason: {result.reason}"
    )


@then(parsers.parse('the first supertype set "{set1}" is the matching set'))
def then_first_set_is_matching_set(game_state, set1):
    """Rule 2.14.1b: First supertype set was the matching one."""
    result = game_state.pool_check_result
    assert result.matching_set == 1, (
        f"Expected matching_set to be 1 (first set '{set1}') but got {result.matching_set}"
    )


@then(parsers.parse('the second supertype set "{set2}" is the matching set'))
def then_second_set_is_matching_set(game_state, set2):
    """Rule 2.14.1b: Second supertype set was the matching one."""
    result = game_state.pool_check_result
    assert result.matching_set == 2, (
        f"Expected matching_set to be 2 (second set '{set2}') but got {result.matching_set}"
    )


@then("only one supertype set needs to match not both combined")
def then_only_one_set_needed(game_state):
    """Rule 2.14.1b: Only one supertype set needs to be a subset, not both combined."""
    result = game_state.pool_check_result
    assert result.is_eligible, (
        "Expected hybrid card to be eligible (one set matches) but was not"
    )
    # Verify the hero doesn't have both supertypes (to confirm the test is meaningful)
    hero_supertypes = game_state.hero.supertypes
    set1 = game_state.hybrid_supertype_set_1
    set2 = game_state.hybrid_supertype_set_2
    combined = set1 | set2
    # At least one set should NOT fully match (otherwise the test is trivial)
    # For Warrior-only hero + Warrior/Wizard hybrid: Wizard doesn't match but Warrior does
    assert not combined.issubset(hero_supertypes), (
        "Both sets combined are subsets - test not distinguishing single-set check"
    )


@then(parsers.parse('the card does not have supertype "{supertype}"'))
def then_card_does_not_have_supertype(game_state, supertype):
    """Rule 2.14.1a: Card does NOT have the given supertype."""
    parse_result = game_state.parse_result
    assert supertype not in parse_result.supertypes, (
        f"Expected '{supertype}' NOT in supertypes, but got {parse_result.supertypes}"
    )


@then("both cards have zero supertypes")
def then_both_cards_have_zero_supertypes(game_state):
    """Rule 2.14.1a: Both 'Generic Action' and 'Action' have zero supertypes."""
    parse_result = game_state.parse_result
    assert len(parse_result.supertypes) == 0, (
        f"First card: expected zero supertypes but got {parse_result.supertypes}"
    )
    second_result = getattr(game_state, "second_parse_result", None)
    if second_result:
        assert len(second_result.supertypes) == 0, (
            f"Second card: expected zero supertypes but got {second_result.supertypes}"
        )


@then(parsers.parse('supertype set 1 "{set1}" was the matching set'))
def then_set1_multi_was_matching_set(game_state, set1):
    """Rule 2.14.1b: Multi-word supertype set 1 was the matching one."""
    result = game_state.pool_check_result
    assert result.matching_set == 1, (
        f"Expected matching set to be 1 ('{set1}') but got {result.matching_set}"
    )


@then("neither full supertype set matches the hero's supertypes")
def then_neither_full_set_matches(game_state):
    """Rule 2.14.1b: Neither complete supertype set matched."""
    result = game_state.pool_check_result
    assert not result.is_eligible, (
        f"Expected card to NOT be eligible but was. Reason: {result.reason}"
    )
    assert result.matching_set is None, (
        f"Expected no matching set but got {result.matching_set}"
    )


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def game_state():
    """
    Fixture providing a game state container for testing.

    Uses a simple namespace object since Section 2.14 tests use stubs
    for the type box parser and hybrid card logic.

    Reference: Rule 2.14 — Type Box
    """
    from types import SimpleNamespace

    state = SimpleNamespace()
    state.type_box_str = ""
    state.second_type_box_str = None
    state.parse_result = None
    state.second_parse_result = None
    state.hybrid_supertype_set_1 = frozenset()
    state.hybrid_supertype_set_2 = frozenset()
    state.hero = None
    state.pool_check_result = None
    state.all_hybrid_supertypes = None
    return state
