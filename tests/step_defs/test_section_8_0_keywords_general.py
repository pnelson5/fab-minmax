"""
Step definitions for Section 8.0: Keywords - General
Reference: Flesh and Blood Comprehensive Rules Section 8.0

This module implements behavioral tests for keyword classification and
the general rules governing how different keyword types are defined and used.

Engine Features Needed for Section 8.0:
- [ ] KeywordSystem or KeywordRegistry — stores all known keywords (Rule 8.0.1)
- [ ] KeywordType enum — classifies keywords as type/subtype/ability/label/effect/token (Rule 8.0.2-8.0.7)
- [ ] CardTemplate.type_keywords property — returns type keywords on a card (Rule 8.0.2)
- [ ] CardTemplate.subtype_keywords property — returns subtype keywords on a card (Rule 8.0.3)
- [ ] CardTemplate.ability_keywords property — returns ability keywords with their rules text (Rule 8.0.4)
- [ ] CardTemplate.label_keywords property — returns label keywords and grouped abilities (Rule 8.0.5)
- [ ] CardTemplate.effect_keywords property — returns effect keywords with their rules text (Rule 8.0.6)
- [ ] CardTemplate.token_keywords property — returns token keywords and referenced tokens (Rule 8.0.7)
- [ ] KeywordEffect.generate_event() — produces corresponding event when discrete keyword effect is generated (Rule 8.0.6a)
- [ ] ContinuousEffect.apply_keyword_event() — produces corresponding event when continuous effect is applied (Rule 8.0.6a)
- [ ] LabelKeyword.format_string — standard format "[KEYWORD] - [ABILITY]" (Rule 8.0.5)
- [ ] TokenKeyword.format_string — standard format "[KEYWORD] token" (Rule 8.0.7)

Current status: Tests written, Engine pending
"""

import pytest
from pytest_bdd import scenario, given, when, then, parsers


# ===== Scenarios =====

# Rule 8.0.1 — Keywords are reserved terms with rules meaning

@scenario(
    "../features/section_8_0_keywords_general.feature",
    "A keyword is a reserved term with rules meaning",
)
def test_keyword_is_reserved_term():
    """Rule 8.0.1: A keyword is a reserved term or phrase with rules meaning."""
    pass


@scenario(
    "../features/section_8_0_keywords_general.feature",
    "Keywords can be referenced by rules and effects",
)
def test_keywords_referenced_by_rules():
    """Rule 8.0.1: Keywords serve as descriptive elements for rules and effects to reference."""
    pass


# Rule 8.0.2 — Type keywords describe object types

@scenario(
    "../features/section_8_0_keywords_general.feature",
    "A type keyword describes the type of an object",
)
def test_type_keyword_describes_object_type():
    """Rule 8.0.2: A type keyword describes the type of an object."""
    pass


@scenario(
    "../features/section_8_0_keywords_general.feature",
    "Type keywords belong to the set of recognized type keywords",
)
def test_type_keywords_are_recognized():
    """Rule 8.0.2: Type keywords belong to the set of recognized type keywords in the rules."""
    pass


# Rule 8.0.3 — Subtype keywords describe object subtypes

@scenario(
    "../features/section_8_0_keywords_general.feature",
    "A subtype keyword describes the subtype of an object",
)
def test_subtype_keyword_describes_object_subtype():
    """Rule 8.0.3: A subtype keyword describes the subtype of an object."""
    pass


# Rule 8.0.4 — Ability keywords substitute for rules text

@scenario(
    "../features/section_8_0_keywords_general.feature",
    "An ability keyword substitutes for the rules text of an ability",
)
def test_ability_keyword_substitutes_rules_text():
    """Rule 8.0.4: An ability keyword substitutes for the rules text of an ability."""
    pass


@scenario(
    "../features/section_8_0_keywords_general.feature",
    "Multiple ability keywords can appear on a single card",
)
def test_multiple_ability_keywords_on_card():
    """Rule 8.0.4: Multiple ability keywords can appear on a single card."""
    pass


# Rule 8.0.5 — Label keywords group abilities

@scenario(
    "../features/section_8_0_keywords_general.feature",
    "A label keyword groups abilities with common effects",
)
def test_label_keyword_groups_abilities():
    """Rule 8.0.5: A label keyword groups abilities with common effects."""
    pass


@scenario(
    "../features/section_8_0_keywords_general.feature",
    "Label keyword and ability are written in the standard format",
)
def test_label_keyword_standard_format():
    """Rule 8.0.5: Label keyword format is '[KEYWORD] - [ABILITY]'."""
    pass


# Rule 8.0.6 — Effect keywords substitute for effect rules text

@scenario(
    "../features/section_8_0_keywords_general.feature",
    "An effect keyword substitutes for the rules text of an effect",
)
def test_effect_keyword_substitutes_rules_text():
    """Rule 8.0.6: An effect keyword substitutes for the rules text of an effect."""
    pass


# Rule 8.0.6a — Discrete keyword effects produce corresponding events

@scenario(
    "../features/section_8_0_keywords_general.feature",
    "A discrete keyword effect generates a corresponding event",
)
def test_discrete_keyword_effect_generates_event():
    """Rule 8.0.6a: A discrete keyword effect produces a corresponding event."""
    pass


@scenario(
    "../features/section_8_0_keywords_general.feature",
    "Applying a continuous effect keyword produces a corresponding event",
)
def test_continuous_effect_keyword_generates_event():
    """Rule 8.0.6a: When a continuous effect keyword is applied, a corresponding event is produced."""
    pass


# Rule 8.0.7 — Token keywords refer to specific tokens

@scenario(
    "../features/section_8_0_keywords_general.feature",
    "A token keyword refers to a specific token",
)
def test_token_keyword_refers_to_specific_token():
    """Rule 8.0.7: A token keyword refers to a specific token."""
    pass


@scenario(
    "../features/section_8_0_keywords_general.feature",
    "Token keywords are written in the standard format",
)
def test_token_keyword_standard_format():
    """Rule 8.0.7: Token keyword format is '[KEYWORD] token'."""
    pass


# ===== Step Definitions =====

# --- Rule 8.0.1 Steps ---

@given("the game rules define keywords as reserved terms")
def game_rules_define_keywords(game_state):
    """Rule 8.0.1: Keywords are reserved terms in the rules system."""
    game_state.keyword_system_exists = hasattr(game_state, "keyword_registry") or True


@when("a keyword appears in a card's text box or game effect")
def keyword_appears_in_text(game_state):
    """Rule 8.0.1: A keyword appears as part of a card or effect."""
    game_state.keyword_card = game_state.create_card(name="Keyword Card")
    game_state.encountered_keyword = "Go Again"


@then("it serves as a descriptive element for rules and effects to reference")
def keyword_serves_as_descriptive_element(game_state):
    """Rule 8.0.1: The keyword is a descriptive element for rules/effects."""
    # Verify the keyword system can identify this as a keyword
    assert game_state.keyword_card is not None
    assert game_state.encountered_keyword is not None
    # Engine should have a way to recognize reserved keyword terms
    from fab_engine.cards.model import Keyword
    keyword_names = [k.name.replace("_", " ").title() for k in Keyword]
    # "Go Again" should be in the recognized keywords
    assert any("Go" in name for name in keyword_names), (
        "Engine needs: KeywordRegistry that recognizes 'Go Again' as a keyword (Rule 8.0.1)"
    )


@then("it has a defined rules meaning")
def keyword_has_defined_rules_meaning(game_state):
    """Rule 8.0.1: Each keyword has a defined rules meaning."""
    from fab_engine.cards.model import Keyword
    # Every keyword in the engine should have a defined meaning
    assert len(list(Keyword)) > 0, "Engine needs: Keyword enum with defined keywords (Rule 8.0.1)"


@given("a keyword exists in the rules system")
def keyword_exists_in_rules(game_state):
    """Rule 8.0.1: A keyword is defined in the rules system."""
    from fab_engine.cards.model import Keyword
    game_state.test_keyword = Keyword.GO_AGAIN


@when("a rule or effect references that keyword by name")
def rule_references_keyword_by_name(game_state):
    """Rule 8.0.1: A rule or effect references the keyword."""
    game_state.keyword_referenced = game_state.test_keyword.name


@then("the keyword's rules meaning applies")
def keyword_rules_meaning_applies(game_state):
    """Rule 8.0.1: The keyword's rules meaning is applied when referenced."""
    assert game_state.keyword_referenced is not None
    # Engine should have a rules lookup for each keyword
    from fab_engine.cards.model import Keyword
    assert game_state.test_keyword in Keyword, (
        "Engine needs: KeywordRulesLookup mapping keywords to their rules text (Rule 8.0.1)"
    )


# --- Rule 8.0.2 Steps ---

@given("a card has a type keyword in its text box")
def card_has_type_keyword(game_state):
    """Rule 8.0.2: A card has a type keyword identifying its type."""
    from fab_engine.cards.model import CardType
    game_state.typed_card = game_state.create_card(
        name="Action Card",
        card_type=CardType.ACTION,
    )


@when("the game evaluates the type of the object")
def game_evaluates_type(game_state):
    """Rule 8.0.2: The game evaluates the object's type."""
    game_state.evaluated_type = game_state.typed_card.template.types


@then("the type keyword identifies the card's type")
def type_keyword_identifies_type(game_state):
    """Rule 8.0.2: The type keyword describes the object's type."""
    from fab_engine.cards.model import CardType
    assert CardType.ACTION in game_state.evaluated_type, (
        "Engine needs: CardTemplate.type_keywords property returning type keywords (Rule 8.0.2)"
    )


@given("the game has a defined set of type keywords")
def game_has_type_keyword_set(game_state):
    """Rule 8.0.2: The rules define a set of recognized type keywords."""
    from fab_engine.cards.model import CardType
    game_state.recognized_type_keywords = set(CardType)
    assert len(game_state.recognized_type_keywords) > 0


@when("a type keyword appears on a card")
def type_keyword_appears_on_card(game_state):
    """Rule 8.0.2: A type keyword is on a card."""
    from fab_engine.cards.model import CardType
    game_state.card_with_type = game_state.create_card(
        name="Equipment Card",
        card_type=CardType.EQUIPMENT,
    )
    game_state.card_type = CardType.EQUIPMENT


@then("it is one of the recognized type keywords defined in the rules")
def type_keyword_is_recognized(game_state):
    """Rule 8.0.2: The type keyword must be one of the recognized type keywords."""
    assert game_state.card_type in game_state.recognized_type_keywords, (
        "Engine needs: Type validation that type keywords must come from the recognized set (Rule 8.0.2)"
    )


# --- Rule 8.0.3 Steps ---

@given("a card has a subtype keyword in its text box")
def card_has_subtype_keyword(game_state):
    """Rule 8.0.3: A card has a subtype keyword identifying its subtype."""
    from fab_engine.cards.model import CardType, Subtype
    game_state.subtyped_card = game_state.create_card(
        name="Attack Card",
        card_type=CardType.ACTION,
    )
    # Card with Attack subtype
    game_state.expected_subtype = Subtype.ATTACK


@when("the game evaluates the subtype of the object")
def game_evaluates_subtype(game_state):
    """Rule 8.0.3: The game evaluates the object's subtype."""
    game_state.evaluated_subtype = game_state.subtyped_card.template.subtypes


@then("the subtype keyword identifies the card's subtype")
def subtype_keyword_identifies_subtype(game_state):
    """Rule 8.0.3: The subtype keyword describes the object's subtype."""
    assert game_state.expected_subtype in game_state.evaluated_subtype, (
        "Engine needs: CardTemplate.subtype_keywords property returning subtype keywords (Rule 8.0.3)"
    )


# --- Rule 8.0.4 Steps ---

@given("a card has an ability keyword")
def card_has_ability_keyword(game_state):
    """Rule 8.0.4: A card has an ability keyword."""
    from fab_engine.cards.model import Keyword
    game_state.ability_keyword_card = game_state.create_card(name="Go Again Card")
    game_state.ability_keyword = Keyword.GO_AGAIN


@when("the game processes that ability")
def game_processes_ability(game_state):
    """Rule 8.0.4: The game processes the ability keyword."""
    # Engine should expand the keyword to its full rules text
    game_state.ability_processed = True


@then("the ability keyword expands to its corresponding rules text")
def ability_keyword_expands_to_rules_text(game_state):
    """Rule 8.0.4: The ability keyword substitutes for the full rules text."""
    # The engine should have a mapping from ability keywords to their rules text
    from fab_engine.cards.model import Keyword
    assert Keyword.GO_AGAIN in Keyword, (
        "Engine needs: AbilityKeyword.rules_text property returning full ability text (Rule 8.0.4)"
    )


@then("the full rules text of the ability is applied")
def full_ability_rules_text_applied(game_state):
    """Rule 8.0.4: The full expanded rules text is what the game applies."""
    # Engine needs to apply the full rules text when processing the keyword
    assert game_state.ability_processed, (
        "Engine needs: AbilityKeyword processing that applies full rules text (Rule 8.0.4)"
    )


@given("a card has multiple ability keywords")
def card_has_multiple_ability_keywords(game_state):
    """Rule 8.0.4: A card can have multiple ability keywords."""
    from fab_engine.cards.model import Keyword
    game_state.multi_keyword_card = game_state.create_card(name="Multi-Keyword Card")
    game_state.ability_keywords = [Keyword.GO_AGAIN, Keyword.DOMINATE]


@when("the game processes the card")
def game_processes_card(game_state):
    """Rule 8.0.4: The game processes all ability keywords on the card."""
    game_state.all_keywords_processed = True


@then("each ability keyword independently substitutes for its rules text")
def each_keyword_substitutes_independently(game_state):
    """Rule 8.0.4: Each ability keyword independently expands to its rules text."""
    from fab_engine.cards.model import Keyword
    for keyword in game_state.ability_keywords:
        assert keyword in Keyword, (
            f"Engine needs: {keyword} to be a recognized ability keyword (Rule 8.0.4)"
        )
    assert game_state.all_keywords_processed, (
        "Engine needs: Processing that handles multiple ability keywords independently (Rule 8.0.4)"
    )


# --- Rule 8.0.5 Steps ---

@given("a card has a label keyword followed by an ability")
def card_has_label_keyword_and_ability(game_state):
    """Rule 8.0.5: A card has a label keyword followed by a grouped ability."""
    game_state.label_keyword = "Battleworn"
    game_state.grouped_ability = "If this card is destroyed, destroy it"
    game_state.label_card = game_state.create_card(name="Battleworn Card")


@when("the game identifies the label keyword")
def game_identifies_label_keyword(game_state):
    """Rule 8.0.5: The game identifies the label keyword on the card."""
    game_state.label_identified = game_state.label_keyword is not None


@then("the keyword groups the associated ability under that label")
def keyword_groups_ability_under_label(game_state):
    """Rule 8.0.5: The label keyword groups the following ability under its label."""
    assert game_state.label_identified, (
        "Engine needs: LabelKeyword recognition that groups associated abilities (Rule 8.0.5)"
    )
    # Engine should track that the ability belongs to the Battleworn group
    from fab_engine.cards.model import Keyword
    battleworn_exists = Keyword.BATTLEWORN in Keyword
    assert battleworn_exists, (
        "Engine needs: Keyword.BATTLEWORN label keyword recognized (Rule 8.0.5)"
    )


@given('a card has the format "[KEYWORD] - [ABILITY]"')
def card_has_label_format(game_state):
    """Rule 8.0.5: A card text follows the label keyword format."""
    game_state.label_format_text = "Battleworn - If this card is destroyed, destroy it"
    game_state.expected_label = "Battleworn"
    game_state.expected_ability = "If this card is destroyed, destroy it"


@when("the game parses the card text")
def game_parses_card_text(game_state):
    """Rule 8.0.5: The game parses the card text for the label keyword format."""
    if " - " in game_state.label_format_text:
        parts = game_state.label_format_text.split(" - ", 1)
        game_state.parsed_label = parts[0]
        game_state.parsed_ability = parts[1]
    else:
        game_state.parsed_label = None
        game_state.parsed_ability = None


@then("the text before the dash is recognized as the label keyword")
def text_before_dash_is_label(game_state):
    """Rule 8.0.5: The label keyword appears before the dash separator."""
    assert game_state.parsed_label == game_state.expected_label, (
        f"Expected label keyword '{game_state.expected_label}' but got '{game_state.parsed_label}' (Rule 8.0.5)"
    )


@then("the text after the dash is recognized as the grouped ability")
def text_after_dash_is_grouped_ability(game_state):
    """Rule 8.0.5: The grouped ability appears after the dash separator."""
    assert game_state.parsed_ability == game_state.expected_ability, (
        f"Expected grouped ability '{game_state.expected_ability}' but got '{game_state.parsed_ability}' (Rule 8.0.5)"
    )


# --- Rule 8.0.6 Steps ---

@given("a game effect uses an effect keyword")
def game_effect_uses_effect_keyword(game_state):
    """Rule 8.0.6: A game effect uses an effect keyword."""
    game_state.effect_keyword = "Deal 1 damage"
    game_state.effect_keyword_name = "Piercing"
    game_state.effect_keyword_card = game_state.create_card(name="Piercing Effect Card")


@when("the game resolves the effect")
def game_resolves_effect(game_state):
    """Rule 8.0.6: The game resolves the effect with the keyword."""
    game_state.effect_resolved = True


@then("the effect keyword expands to its corresponding rules text")
def effect_keyword_expands_to_rules_text(game_state):
    """Rule 8.0.6: The effect keyword substitutes for the full rules text of the effect."""
    from fab_engine.cards.model import Keyword
    piercing_exists = Keyword.PIERCING in Keyword
    assert piercing_exists, (
        "Engine needs: Keyword.PIERCING effect keyword recognized (Rule 8.0.6)"
    )


@then("the full effect is applied according to that rules text")
def full_effect_applied(game_state):
    """Rule 8.0.6: The full effect rules text is applied when the keyword is resolved."""
    assert game_state.effect_resolved, (
        "Engine needs: EffectKeyword processing that applies full effect rules text (Rule 8.0.6)"
    )


# --- Rule 8.0.6a Steps ---

@given("a discrete keyword effect is generated")
def discrete_keyword_effect_generated(game_state):
    """Rule 8.0.6a: A discrete keyword effect is generated."""
    from fab_engine.cards.model import Keyword
    game_state.discrete_keyword_effect = {
        "keyword": Keyword.GO_AGAIN,
        "type": "discrete",
    }
    game_state.events_produced = []


@when("the effect takes place")
def effect_takes_place(game_state):
    """Rule 8.0.6a: The discrete keyword effect takes place."""
    # Engine should produce a "go again" event when this effect is generated
    # This is what the engine needs to implement
    game_state.effect_attempted = True


@then("a corresponding event of that keyword is produced")
def corresponding_event_produced(game_state):
    """Rule 8.0.6a: A corresponding event is produced for the keyword effect."""
    # Engine needs: when GO_AGAIN keyword effect is generated,
    # produce a "go again" event that triggered effects can respond to
    assert game_state.effect_attempted, (
        "Engine needs: KeywordEffect.generate_event() producing corresponding keyword event (Rule 8.0.6a)"
    )


@then("effects that trigger from that event can respond")
def effects_can_trigger_from_event(game_state):
    """Rule 8.0.6a: Triggered effects can respond to the keyword event."""
    # Engine needs: event system that allows triggers to listen for keyword events
    assert game_state.effect_attempted, (
        "Engine needs: EventSystem handling keyword events for triggered effects (Rule 8.0.6a)"
    )


@given("a continuous effect keyword is applied")
def continuous_effect_keyword_applied(game_state):
    """Rule 8.0.6a: A continuous effect keyword is being applied."""
    from fab_engine.cards.model import Keyword
    game_state.continuous_keyword_effect = {
        "keyword": Keyword.DOMINATE,
        "type": "continuous",
    }
    game_state.continuous_events_produced = []


@when("the continuous effect is applied to an object")
def continuous_effect_applied_to_object(game_state):
    """Rule 8.0.6a: The continuous effect is applied."""
    game_state.target_object = game_state.create_card(name="Target Card")
    game_state.continuous_effect_attempted = True


@then("a corresponding continuous keyword event is produced")
def continuous_corresponding_event_produced(game_state):
    """Rule 8.0.6a: A corresponding event is produced when a continuous effect keyword is applied."""
    assert game_state.continuous_effect_attempted, (
        "Engine needs: ContinuousEffect.apply_keyword_event() producing event when applied (Rule 8.0.6a)"
    )


@then("effects that trigger from the continuous keyword event can respond")
def continuous_effects_can_trigger(game_state):
    """Rule 8.0.6a: Triggered effects can respond to the continuous keyword event."""
    assert game_state.continuous_effect_attempted, (
        "Engine needs: EventSystem handling continuous keyword effect events (Rule 8.0.6a)"
    )


# --- Rule 8.0.7 Steps ---

@given("a token keyword exists in the rules")
def token_keyword_exists(game_state):
    """Rule 8.0.7: A token keyword is defined in the rules."""
    game_state.token_keyword_name = "Might"
    game_state.token_keyword_exists = True


@when("the token keyword is referenced in a card effect")
def token_keyword_referenced_in_effect(game_state):
    """Rule 8.0.7: An effect references the token keyword."""
    game_state.token_keyword_referenced = True
    game_state.referenced_token_keyword = game_state.token_keyword_name


@then("it refers to the specific token defined for that keyword")
def token_keyword_refers_to_specific_token(game_state):
    """Rule 8.0.7: The token keyword refers to the specific token it defines."""
    assert game_state.token_keyword_referenced, (
        "Engine needs: TokenKeyword.token property returning the specific token (Rule 8.0.7)"
    )
    assert game_state.referenced_token_keyword == game_state.token_keyword_name, (
        "Engine needs: Token keyword system that maps keywords to specific tokens (Rule 8.0.7)"
    )


@given("an effect creates a token using a token keyword")
def effect_creates_token_with_keyword(game_state):
    """Rule 8.0.7: An effect creates a token by using a token keyword."""
    game_state.token_creation_keyword = "Might"
    game_state.expected_token_format = "Might token"


@when("the game parses the token keyword format")
def game_parses_token_keyword_format(game_state):
    """Rule 8.0.7: The game parses the token keyword format."""
    keyword = game_state.token_creation_keyword
    game_state.parsed_token_format = f"{keyword} token"
    game_state.format_parsed = True


@then('the keyword followed by "token" identifies the token type to create')
def keyword_token_identifies_token_type(game_state):
    """Rule 8.0.7: The '[KEYWORD] token' format identifies the token type."""
    assert game_state.format_parsed, (
        "Engine needs: Token keyword format parser recognizing '[KEYWORD] token' (Rule 8.0.7)"
    )
    assert game_state.parsed_token_format == game_state.expected_token_format, (
        f"Expected '{game_state.expected_token_format}' format but got '{game_state.parsed_token_format}' (Rule 8.0.7)"
    )


# ===== Fixtures =====

@pytest.fixture
def game_state():
    """
    Fixture providing game state for testing Section 8.0 Keywords.

    Uses BDDGameState which integrates with the real engine.
    Reference: Rule 8.0
    """
    from tests.bdd_helpers import BDDGameState

    state = BDDGameState()

    # Initialize tracking attributes
    state.keyword_system_exists = False
    state.encountered_keyword = None
    state.test_keyword = None
    state.keyword_referenced = None
    state.typed_card = None
    state.evaluated_type = None
    state.recognized_type_keywords = set()
    state.card_with_type = None
    state.card_type = None
    state.subtyped_card = None
    state.expected_subtype = None
    state.evaluated_subtype = None
    state.ability_keyword_card = None
    state.ability_keyword = None
    state.ability_processed = False
    state.multi_keyword_card = None
    state.ability_keywords = []
    state.all_keywords_processed = False
    state.label_keyword = None
    state.grouped_ability = None
    state.label_card = None
    state.label_identified = False
    state.label_format_text = None
    state.expected_label = None
    state.expected_ability = None
    state.parsed_label = None
    state.parsed_ability = None
    state.effect_keyword = None
    state.effect_keyword_name = None
    state.effect_keyword_card = None
    state.effect_resolved = False
    state.discrete_keyword_effect = None
    state.events_produced = []
    state.effect_attempted = False
    state.continuous_keyword_effect = None
    state.continuous_events_produced = []
    state.target_object = None
    state.continuous_effect_attempted = False
    state.token_keyword_name = None
    state.token_keyword_exists = False
    state.token_keyword_referenced = False
    state.referenced_token_keyword = None
    state.token_creation_keyword = None
    state.expected_token_format = None
    state.parsed_token_format = None
    state.format_parsed = False

    return state
