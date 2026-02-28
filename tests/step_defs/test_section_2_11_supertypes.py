"""
Step definitions for Section 2.11: Supertypes
Reference: Flesh and Blood Comprehensive Rules Section 2.11

This module implements behavioral tests for the supertype property:
- Supertypes as supertype keywords determining card-pool inclusion (Rule 2.11.1)
- Objects having zero or more supertypes (Rule 2.11.2)
- Supertypes determined by type box (Rule 2.11.3)
- Layer supertype inheritance (Rule 2.11.4)
- Gaining/losing supertypes via effects (Rule 2.11.5)
- Supertypes as non-functional keywords; class vs talent (Rule 2.11.6, 2.11.6a, 2.11.6b)

Engine Features Needed for Section 2.11:
- [ ] `CardTemplate.supertypes` returning a set/frozenset of supertype keywords (Rule 2.11.2)
- [ ] `SupertypeRegistry.CLASS_SUPERTYPES` frozenset containing all 17 class supertypes (Rule 2.11.6a)
- [ ] `SupertypeRegistry.TALENT_SUPERTYPES` frozenset containing all 12 talent supertypes (Rule 2.11.6b)
- [ ] `SupertypeRegistry.get_category(name)` -> "class" | "talent" | None (Rule 2.11.6)
- [ ] `SupertypeRegistry.is_non_functional(name) = True` (Rule 2.11.6)
- [ ] Type box parser extracting supertypes before card type (Rule 2.11.3)
- [ ] `Layer.supertypes` inheriting from source (Rule 2.11.4)
- [ ] `CardInstance.gain_supertype(name)` method (Rule 2.11.5)
- [ ] `CardInstance.lose_supertype(name)` method (Rule 2.11.5)
- [ ] `card_pool_legality_check_supertypes(card, hero)` for supertype subset validation (Rule 2.11.1)
- [ ] "Generic" type box means no supertypes (Rule 2.14.1a cross-ref)
"""

import pytest
from pytest_bdd import scenario, given, when, then, parsers


# ---------------------------------------------------------------------------
# Scenario: Supertypes determine card-pool inclusion
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_11_supertypes.feature",
    "Supertypes determine card-pool inclusion",
)
def test_supertypes_determine_card_pool_inclusion():
    """Rule 2.11.1: Supertypes determine whether a card can be in a player's card-pool."""
    pass


# ---------------------------------------------------------------------------
# Scenario: Non-matching supertypes prevent card-pool inclusion
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_11_supertypes.feature",
    "Non-matching supertypes prevent card-pool inclusion",
)
def test_non_matching_supertypes_prevent_card_pool_inclusion():
    """Rule 2.11.1: Cards whose supertypes are not a subset of the hero's cannot be in card-pool."""
    pass


# ---------------------------------------------------------------------------
# Scenario: Card with zero supertypes has no supertypes property values
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_11_supertypes.feature",
    "Card with zero supertypes has no supertypes property values",
)
def test_card_with_zero_supertypes():
    """Rule 2.11.2: An object can have zero supertypes."""
    pass


# ---------------------------------------------------------------------------
# Scenario: Card can have exactly one supertype
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_11_supertypes.feature",
    "Card can have exactly one supertype",
)
def test_card_can_have_exactly_one_supertype():
    """Rule 2.11.2: An object can have one supertype."""
    pass


# ---------------------------------------------------------------------------
# Scenario: Card can have multiple supertypes
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_11_supertypes.feature",
    "Card can have multiple supertypes",
)
def test_card_can_have_multiple_supertypes():
    """Rule 2.11.2: An object can have multiple supertypes."""
    pass


# ---------------------------------------------------------------------------
# Scenario: Supertypes are determined from the type box
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_11_supertypes.feature",
    "Supertypes are determined from the type box",
)
def test_supertypes_determined_from_type_box():
    """Rule 2.11.3: Supertypes come from the type box."""
    pass


# ---------------------------------------------------------------------------
# Scenario: Supertypes are printed before the card type in the type box
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_11_supertypes.feature",
    "Supertypes are printed before the card type in the type box",
)
def test_supertypes_printed_before_card_type():
    """Rule 2.11.3: Supertypes printed before the card type in the type box."""
    pass


# ---------------------------------------------------------------------------
# Scenario: Activated-layer inherits supertypes from its source
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_11_supertypes.feature",
    "Activated-layer inherits supertypes from its source",
)
def test_activated_layer_inherits_supertypes():
    """Rule 2.11.4: Activated-layer supertypes equal source's supertypes."""
    pass


# ---------------------------------------------------------------------------
# Scenario: Triggered-layer inherits supertypes from its source
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_11_supertypes.feature",
    "Triggered-layer inherits supertypes from its source",
)
def test_triggered_layer_inherits_supertypes():
    """Rule 2.11.4: Triggered-layer supertypes equal source's supertypes."""
    pass


# ---------------------------------------------------------------------------
# Scenario: Layer from no-supertype source inherits no supertypes
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_11_supertypes.feature",
    "Layer from no-supertype source inherits no supertypes",
)
def test_layer_from_no_supertype_source():
    """Rule 2.11.4: Layer from no-supertype source has zero supertypes."""
    pass


# ---------------------------------------------------------------------------
# Scenario: An object can gain a supertype from an effect
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_11_supertypes.feature",
    "An object can gain a supertype from an effect",
)
def test_object_can_gain_supertype():
    """Rule 2.11.5: Objects can gain supertypes."""
    pass


# ---------------------------------------------------------------------------
# Scenario: An object can lose a supertype from an effect
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_11_supertypes.feature",
    "An object can lose a supertype from an effect",
)
def test_object_can_lose_supertype():
    """Rule 2.11.5: Objects can lose supertypes."""
    pass


# ---------------------------------------------------------------------------
# Scenario: Supertypes are non-functional keywords
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_11_supertypes.feature",
    "Supertypes are non-functional keywords",
)
def test_supertypes_are_non_functional():
    """Rule 2.11.6: Supertypes do not add additional rules to an object."""
    pass


# ---------------------------------------------------------------------------
# Scenario: Warrior is a class supertype keyword
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_11_supertypes.feature",
    "Warrior is a class supertype keyword",
)
def test_warrior_is_class_supertype():
    """Rule 2.11.6/2.11.6a: Warrior is a class supertype keyword."""
    pass


# ---------------------------------------------------------------------------
# Scenario: Draconic is a talent supertype keyword
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_11_supertypes.feature",
    "Draconic is a talent supertype keyword",
)
def test_draconic_is_talent_supertype():
    """Rule 2.11.6/2.11.6b: Draconic is a talent supertype keyword."""
    pass


# ---------------------------------------------------------------------------
# Scenario: All class supertype keywords are recognized
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_11_supertypes.feature",
    "All class supertype keywords are recognized",
)
def test_all_class_supertypes_recognized():
    """Rule 2.11.6a: All 17 class supertype keywords recognized."""
    pass


# ---------------------------------------------------------------------------
# Scenario: All talent supertype keywords are recognized
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_11_supertypes.feature",
    "All talent supertype keywords are recognized",
)
def test_all_talent_supertypes_recognized():
    """Rule 2.11.6b: All 12 talent supertype keywords recognized."""
    pass


# ---------------------------------------------------------------------------
# Scenario: Generic type box means card has no supertypes
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_11_supertypes.feature",
    "Generic type box means card has no supertypes",
)
def test_generic_type_box_means_no_supertypes():
    """Rule 2.14.1a cross-ref: 'Generic' in type box means the card has no supertypes."""
    pass


# ---------------------------------------------------------------------------
# Scenario: Card with no supertypes can be in any card-pool
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_11_supertypes.feature",
    "Card with no supertypes can be in any card-pool",
)
def test_card_with_no_supertypes_in_any_card_pool():
    """Rule 2.11.1: Empty supertype set is a subset of any hero's supertypes."""
    pass


# ---------------------------------------------------------------------------
# Scenario: Card with Warrior supertype valid for Warrior hero with Draconic talent
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_11_supertypes.feature",
    "Card with Warrior supertype valid for Warrior hero with Draconic talent",
)
def test_warrior_draconic_card_valid_for_warrior_draconic_hero():
    """Rule 2.11.1/2.11.2: Card with multiple supertypes valid when all are subset of hero's."""
    pass


# ---------------------------------------------------------------------------
# Scenario: Card with Wizard supertype is invalid for Warrior hero
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_11_supertypes.feature",
    "Card with Wizard supertype is invalid for Warrior hero",
)
def test_wizard_card_invalid_for_warrior_hero():
    """Rule 2.11.1: Non-matching supertype card cannot be included in card-pool."""
    pass


# ---------------------------------------------------------------------------
# Scenario: Card with multiple supertypes needs all to be subset of hero supertypes
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_2_11_supertypes.feature",
    "Card with multiple supertypes needs all to be subset of hero supertypes",
)
def test_multi_supertype_card_needs_all_match():
    """Rule 2.11.1: All card supertypes must be a subset of hero's supertypes."""
    pass


# ---------------------------------------------------------------------------
# Step Definitions
# ---------------------------------------------------------------------------

# --- GIVEN steps ---


@given(parsers.re(r'^a card with supertypes "(?P<supertype>[^"]+)"$'))
def card_with_one_supertype(game_state, supertype):
    """Rule 2.11.2: Create card with a single supertype.

    Sets game_state.test_card with the given supertype.
    """
    game_state.test_card = game_state.create_card(name="Test Card")
    game_state.test_card._supertypes = {supertype}


@given(
    parsers.re(
        r'a card with supertypes "(?P<supertype1>[^"]+)" and "(?P<supertype2>[^"]+)"'
    )
)
def card_with_two_supertypes(game_state, supertype1, supertype2):
    """Rule 2.11.2: Create card with two supertypes.

    Sets game_state.test_card with both supertypes.
    """
    game_state.test_card = game_state.create_card(name="Test Card")
    game_state.test_card._supertypes = {supertype1, supertype2}


@given("a card with no supertypes")
def card_with_no_supertypes(game_state):
    """Rule 2.11.2: Create card with zero supertypes.

    Sets game_state.test_card with empty supertypes.
    """
    game_state.test_card = game_state.create_card(name="Test Card")
    game_state.test_card._supertypes = set()


@given(parsers.parse('a hero with supertype "{supertype}"'))
def hero_with_one_supertype(game_state, supertype):
    """Rule 2.11.1: Set the hero's supertypes to a single supertype for card-pool validation."""
    game_state.hero_supertypes = {supertype}


@given(
    parsers.re(
        r'a hero with supertypes "(?P<supertype1>[^"]+)" and "(?P<supertype2>[^"]+)"'
    )
)
def hero_with_two_supertypes(game_state, supertype1, supertype2):
    """Rule 2.11.1: Set the hero's supertypes to two supertypes for card-pool validation."""
    game_state.hero_supertypes = {supertype1, supertype2}


@given(parsers.parse('a card with type box "{type_box}"'))
def card_with_type_box(game_state, type_box):
    """Rule 2.11.3: Create card with the given type box string for parsing."""
    game_state.test_card = game_state.create_card(name="Test Card")
    game_state.test_type_box = type_box
    # Engine will need to parse this type box
    # Expected: TypeBoxParser.parse(type_box) -> ParseResult with supertypes, type, subtypes
    game_state.type_box_parse_result = game_state.parse_type_box(type_box)


@given(parsers.parse('a type box parse result for "{type_box}"'))
def type_box_parse_result_for(game_state, type_box):
    """Rule 2.11.3: Parse the type box string to verify ordering."""
    game_state.test_type_box = type_box
    game_state.type_box_parse_result = game_state.parse_type_box(type_box)


@given(parsers.parse("an activated-layer is created from that card"))
def activated_layer_from_card(game_state):
    """Rule 2.11.4: Create an activated-layer from the test card source."""
    # Engine will need ActivatedLayer class
    # Expected: ActivatedLayer.source = test_card; inherits supertypes
    game_state.test_layer = game_state.create_activated_layer(
        source=game_state.test_card
    )


@given(parsers.parse("a triggered-layer is created from that card"))
def triggered_layer_from_card(game_state):
    """Rule 2.11.4: Create a triggered-layer from the test card source."""
    # Engine will need TriggeredLayer class
    # Expected: TriggeredLayer.source = test_card; inherits supertypes
    game_state.test_layer = game_state.create_triggered_layer(
        source=game_state.test_card
    )


@given(parsers.parse('the supertype "{supertype}"'))
def the_given_supertype(game_state, supertype):
    """Rule 2.11.6: Record the supertype name for classification testing."""
    game_state.test_supertype_name = supertype


# --- WHEN steps ---


@when("the engine checks if the card can be included in the hero's card-pool")
def check_card_pool_eligibility(game_state):
    """Rule 2.11.1: Perform supertype subset validation for card-pool inclusion."""
    # Engine will need: validate_card_pool_supertypes(card_supertypes, hero_supertypes)
    # Returns bool indicating if card_supertypes is a subset of hero_supertypes
    game_state.card_pool_result = game_state.check_card_pool_eligibility_by_supertypes(
        card_supertypes=game_state.test_card._supertypes,
        hero_supertypes=game_state.hero_supertypes,
    )


@when("the engine reads the supertypes of the card")
def engine_reads_card_supertypes(game_state):
    """Rule 2.11.2/2.11.3: Engine reads the card's supertypes."""
    game_state.read_supertypes = game_state.get_card_supertypes(game_state.test_card)


@when("the engine parses the type box")
def engine_parses_type_box(game_state):
    """Rule 2.11.3: Engine parses the type box string."""
    # type_box_parse_result set in the 'given' step
    # Also populate read_supertypes from the parse result for scenarios that check supertypes
    if game_state.type_box_parse_result is not None:
        game_state.read_supertypes = set(game_state.type_box_parse_result.supertypes)


@when("the engine reads the supertypes of the activated-layer")
def engine_reads_activated_layer_supertypes(game_state):
    """Rule 2.11.4: Engine reads supertypes of an activated-layer."""
    game_state.read_supertypes = game_state.get_layer_supertypes(game_state.test_layer)


@when("the engine reads the supertypes of the triggered-layer")
def engine_reads_triggered_layer_supertypes(game_state):
    """Rule 2.11.4: Engine reads supertypes of a triggered-layer."""
    game_state.read_supertypes = game_state.get_layer_supertypes(game_state.test_layer)


@when(parsers.parse('an effect grants the card the supertype "{supertype}"'))
def effect_grants_supertype(game_state, supertype):
    """Rule 2.11.5: Effect grants supertype to card."""
    # Engine will need: CardInstance.gain_supertype(name)
    game_state.gain_supertype_result = game_state.grant_supertype_to_card(
        game_state.test_card, supertype
    )
    game_state.read_supertypes = game_state.get_card_supertypes(game_state.test_card)


@when(parsers.parse('an effect removes the supertype "{supertype}" from the card'))
def effect_removes_supertype(game_state, supertype):
    """Rule 2.11.5: Effect removes supertype from card."""
    # Engine will need: CardInstance.lose_supertype(name)
    game_state.lose_supertype_result = game_state.remove_supertype_from_card(
        game_state.test_card, supertype
    )
    game_state.read_supertypes = game_state.get_card_supertypes(game_state.test_card)


@when("the engine checks the supertypes for additional rules")
def engine_checks_supertypes_for_additional_rules(game_state):
    """Rule 2.11.6: Engine checks whether supertypes add additional rules."""
    game_state.supertype_rules_result = (
        game_state.check_supertypes_add_additional_rules(game_state.test_card)
    )


@when("the engine classifies the supertype")
def engine_classifies_supertype(game_state):
    """Rule 2.11.6: Engine classifies the supertype as class or talent."""
    # Engine will need: SupertypeRegistry.get_category(name) -> "class" | "talent"
    game_state.supertype_classification = game_state.get_supertype_category(
        game_state.test_supertype_name
    )


@when("the engine lists all class supertypes")
def engine_lists_all_class_supertypes(game_state):
    """Rule 2.11.6a: Engine returns the full list of class supertypes."""
    # Engine will need: SupertypeRegistry.CLASS_SUPERTYPES frozenset
    game_state.class_supertypes = game_state.get_all_class_supertypes()


@when("the engine lists all talent supertypes")
def engine_lists_all_talent_supertypes(game_state):
    """Rule 2.11.6b: Engine returns the full list of talent supertypes."""
    # Engine will need: SupertypeRegistry.TALENT_SUPERTYPES frozenset
    game_state.talent_supertypes = game_state.get_all_talent_supertypes()


# --- THEN steps ---


@then("the card is eligible for the card-pool")
def card_is_eligible_for_card_pool(game_state):
    """Rule 2.11.1: Card's supertypes are a subset of hero's supertypes."""
    assert game_state.card_pool_result is not None, (
        "Engine feature needed: check_card_pool_eligibility_by_supertypes()"
    )
    assert game_state.card_pool_result is True or (
        hasattr(game_state.card_pool_result, "is_eligible")
        and game_state.card_pool_result.is_eligible
    ), f"Card should be eligible for card-pool but got: {game_state.card_pool_result}"


@then("the card is not eligible for the card-pool")
def card_is_not_eligible_for_card_pool(game_state):
    """Rule 2.11.1: Card's supertypes are NOT a subset of hero's supertypes."""
    assert game_state.card_pool_result is not None, (
        "Engine feature needed: check_card_pool_eligibility_by_supertypes()"
    )
    assert game_state.card_pool_result is False or (
        hasattr(game_state.card_pool_result, "is_eligible")
        and not game_state.card_pool_result.is_eligible
    ), (
        f"Card should NOT be eligible for card-pool but got: {game_state.card_pool_result}"
    )


@then("the card has zero supertypes")
def card_has_zero_supertypes(game_state):
    """Rule 2.11.2: Card has no supertypes."""
    assert game_state.read_supertypes is not None, (
        "Engine feature needed: get_card_supertypes() returning supertypes collection"
    )
    assert len(game_state.read_supertypes) == 0, (
        f"Card should have zero supertypes but has: {game_state.read_supertypes}"
    )


@then("the card is still a valid game object")
def card_is_still_valid_game_object(game_state):
    """Rule 2.11.2: Zero supertypes does not invalidate an object."""
    assert game_state.test_card is not None, (
        "Card should still exist as a valid game object"
    )


@then(parsers.parse("the card has exactly {count:d} supertype"))
def card_has_exactly_n_supertypes(game_state, count):
    """Rule 2.11.2: Card has exactly N supertypes."""
    assert game_state.read_supertypes is not None, (
        "Engine feature needed: get_card_supertypes() returning supertypes collection"
    )
    assert len(game_state.read_supertypes) == count, (
        f"Card should have exactly {count} supertype(s) but has: {len(game_state.read_supertypes)}"
    )


@then(parsers.parse("the card has exactly {count:d} supertypes"))
def card_has_exactly_n_supertypes_plural(game_state, count):
    """Rule 2.11.2: Card has exactly N supertypes (plural form)."""
    assert game_state.read_supertypes is not None, (
        "Engine feature needed: get_card_supertypes() returning supertypes collection"
    )
    assert len(game_state.read_supertypes) == count, (
        f"Card should have exactly {count} supertypes but has: {len(game_state.read_supertypes)}"
    )


@then(parsers.parse('the card has supertype "{supertype}"'))
def card_has_supertype(game_state, supertype):
    """Rule 2.11.2: Card has the specified supertype."""
    assert game_state.read_supertypes is not None, (
        "Engine feature needed: get_card_supertypes() returning supertypes collection"
    )
    supertype_names = {
        s if isinstance(s, str) else s.name.title() for s in game_state.read_supertypes
    }
    assert supertype in supertype_names or supertype.upper() in {
        s.upper() if isinstance(s, str) else s.name.upper()
        for s in game_state.read_supertypes
    }, f"Card should have supertype '{supertype}' but has: {game_state.read_supertypes}"


@then(parsers.parse('the card type is "{card_type}"'))
def card_type_is(game_state, card_type):
    """Rule 2.11.3: Type box parse result has the correct card type."""
    assert game_state.type_box_parse_result is not None, (
        "Engine feature needed: parse_type_box() returning ParseResult"
    )
    assert hasattr(game_state.type_box_parse_result, "card_type"), (
        "Engine feature needed: TypeBoxParseResult.card_type attribute"
    )
    assert game_state.type_box_parse_result.card_type == card_type, (
        f"Card type should be '{card_type}' but is: {game_state.type_box_parse_result.card_type}"
    )


@then(parsers.parse('the card subtype is "{subtype}"'))
def card_subtype_is(game_state, subtype):
    """Rule 2.11.3: Type box parse result has the correct subtype."""
    assert game_state.type_box_parse_result is not None, (
        "Engine feature needed: parse_type_box() returning ParseResult"
    )
    assert hasattr(game_state.type_box_parse_result, "subtypes"), (
        "Engine feature needed: TypeBoxParseResult.subtypes attribute"
    )
    assert subtype in game_state.type_box_parse_result.subtypes, (
        f"Card should have subtype '{subtype}' but has: {game_state.type_box_parse_result.subtypes}"
    )


@then("the type box order shows supertypes before the type")
def type_box_order_shows_supertypes_before_type(game_state):
    """Rule 2.11.3: Supertypes are printed before the card type in the type box."""
    assert game_state.type_box_parse_result is not None, (
        "Engine feature needed: parse_type_box() returning ParseResult"
    )
    assert hasattr(game_state.type_box_parse_result, "supertypes_before_type"), (
        "Engine feature needed: TypeBoxParseResult.supertypes_before_type flag"
    )
    assert game_state.type_box_parse_result.supertypes_before_type is True, (
        "Type box should have supertypes ordered before the card type"
    )


@then(parsers.parse('the activated-layer has supertype "{supertype}"'))
def activated_layer_has_supertype(game_state, supertype):
    """Rule 2.11.4: Activated-layer has the supertype inherited from its source."""
    assert game_state.read_supertypes is not None, (
        "Engine feature needed: get_layer_supertypes() for activated-layer"
    )
    supertype_names = {
        s if isinstance(s, str) else s.name.title() for s in game_state.read_supertypes
    }
    assert supertype in supertype_names or supertype.upper() in {
        s.upper() if isinstance(s, str) else s.name.upper()
        for s in game_state.read_supertypes
    }, (
        f"Activated-layer should have supertype '{supertype}' but has: {game_state.read_supertypes}"
    )


@then("the activated-layer has zero supertypes")
def activated_layer_has_zero_supertypes(game_state):
    """Rule 2.11.4: Activated-layer has no supertypes when source has none."""
    assert game_state.read_supertypes is not None, (
        "Engine feature needed: get_layer_supertypes() for activated-layer"
    )
    assert len(game_state.read_supertypes) == 0, (
        f"Activated-layer should have zero supertypes but has: {game_state.read_supertypes}"
    )


@then(parsers.parse('the triggered-layer has supertype "{supertype}"'))
def triggered_layer_has_supertype(game_state, supertype):
    """Rule 2.11.4: Triggered-layer has the supertype inherited from its source."""
    assert game_state.read_supertypes is not None, (
        "Engine feature needed: get_layer_supertypes() for triggered-layer"
    )
    supertype_names = {
        s if isinstance(s, str) else s.name.title() for s in game_state.read_supertypes
    }
    assert supertype in supertype_names or supertype.upper() in {
        s.upper() if isinstance(s, str) else s.name.upper()
        for s in game_state.read_supertypes
    }, (
        f"Triggered-layer should have supertype '{supertype}' but has: {game_state.read_supertypes}"
    )


@then(parsers.parse('the card no longer has supertype "{supertype}"'))
def card_no_longer_has_supertype(game_state, supertype):
    """Rule 2.11.5: Supertype was removed from the card."""
    assert game_state.read_supertypes is not None, (
        "Engine feature needed: get_card_supertypes()"
    )
    supertype_upper = {
        s.upper() if isinstance(s, str) else s.name.upper()
        for s in game_state.read_supertypes
    }
    assert supertype.upper() not in supertype_upper, (
        f"Card should NOT have supertype '{supertype}' but has: {game_state.read_supertypes}"
    )


@then(parsers.parse('the card still has supertype "{supertype}"'))
def card_still_has_supertype(game_state, supertype):
    """Rule 2.11.5: Other supertypes are not affected by removal."""
    assert game_state.read_supertypes is not None, (
        "Engine feature needed: get_card_supertypes()"
    )
    supertype_upper = {
        s.upper() if isinstance(s, str) else s.name.upper()
        for s in game_state.read_supertypes
    }
    assert supertype.upper() in supertype_upper, (
        f"Card should still have supertype '{supertype}' but has: {game_state.read_supertypes}"
    )


@then("no additional rules are added by the supertypes")
def no_additional_rules_added_by_supertypes(game_state):
    """Rule 2.11.6: Supertypes are non-functional and don't add rules."""
    assert game_state.supertype_rules_result is not None, (
        "Engine feature needed: check_supertypes_add_additional_rules()"
    )
    assert not game_state.supertype_rules_result.adds_additional_rules, (
        "Supertypes should NOT add additional rules (they are non-functional)"
    )


@then("the supertype is classified as non-functional")
def supertype_is_classified_non_functional(game_state):
    """Rule 2.11.6: Supertypes are non-functional keywords."""
    assert game_state.supertype_rules_result is not None, (
        "Engine feature needed: check_supertypes_add_additional_rules()"
    )
    assert game_state.supertype_rules_result.is_non_functional is True, (
        "Supertype should be classified as non-functional"
    )


@then(parsers.parse('the supertype category is "{category}"'))
def supertype_category_is(game_state, category):
    """Rule 2.11.6: Supertype is classified as 'class' or 'talent'."""
    assert game_state.supertype_classification is not None, (
        "Engine feature needed: get_supertype_category()"
    )
    assert game_state.supertype_classification == category, (
        f"Supertype should be classified as '{category}' but is: {game_state.supertype_classification}"
    )


@then(parsers.parse('the class supertypes include "{supertype}"'))
def class_supertypes_include(game_state, supertype):
    """Rule 2.11.6a: Class supertypes list includes the given supertype."""
    assert game_state.class_supertypes is not None, (
        "Engine feature needed: get_all_class_supertypes()"
    )
    class_names_upper = {
        s.upper() if isinstance(s, str) else s.upper()
        for s in game_state.class_supertypes
    }
    assert supertype.upper() in class_names_upper, (
        f"Class supertypes should include '{supertype}' but has: {game_state.class_supertypes}"
    )


@then(parsers.parse("there are exactly {count:d} class supertypes"))
def there_are_exactly_n_class_supertypes(game_state, count):
    """Rule 2.11.6a: Exactly N class supertype keywords are defined."""
    assert game_state.class_supertypes is not None, (
        "Engine feature needed: get_all_class_supertypes()"
    )
    assert len(game_state.class_supertypes) == count, (
        f"Should have exactly {count} class supertypes but has {len(game_state.class_supertypes)}: "
        f"{game_state.class_supertypes}"
    )


@then(parsers.parse('the talent supertypes include "{supertype}"'))
def talent_supertypes_include(game_state, supertype):
    """Rule 2.11.6b: Talent supertypes list includes the given supertype."""
    assert game_state.talent_supertypes is not None, (
        "Engine feature needed: get_all_talent_supertypes()"
    )
    talent_names_upper = {
        s.upper() if isinstance(s, str) else s.upper()
        for s in game_state.talent_supertypes
    }
    assert supertype.upper() in talent_names_upper, (
        f"Talent supertypes should include '{supertype}' but has: {game_state.talent_supertypes}"
    )


@then(parsers.parse("there are exactly {count:d} talent supertypes"))
def there_are_exactly_n_talent_supertypes(game_state, count):
    """Rule 2.11.6b: Exactly N talent supertype keywords are defined."""
    assert game_state.talent_supertypes is not None, (
        "Engine feature needed: get_all_talent_supertypes()"
    )
    assert len(game_state.talent_supertypes) == count, (
        f"Should have exactly {count} talent supertypes but has {len(game_state.talent_supertypes)}: "
        f"{game_state.talent_supertypes}"
    )


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def game_state():
    """
    Fixture providing game state for Section 2.11 Supertype tests.

    Uses BDDGameState which integrates with the real engine.
    Reference: Rule 2.11 - Supertypes
    """
    from tests.bdd_helpers import BDDGameState

    state = BDDGameState()

    # Initialize attributes used by steps
    state.test_card = None
    state.hero_supertypes = set()
    state.card_pool_result = None
    state.read_supertypes = None
    state.test_layer = None
    state.test_type_box = None
    state.type_box_parse_result = None
    state.gain_supertype_result = None
    state.lose_supertype_result = None
    state.supertype_rules_result = None
    state.supertype_classification = None
    state.class_supertypes = None
    state.talent_supertypes = None
    state.test_supertype_name = None

    return state
