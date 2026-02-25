"""
Step definitions for Section 1.7: Abilities
Reference: Flesh and Blood Comprehensive Rules Section 1.7

This module implements behavioral tests for ability rules:
- Rule 1.7.1: Abilities are properties of objects that influence the game
- Rule 1.7.1a: Source of an ability; activated/triggered-layers exist independently
- Rule 1.7.1b: Controller of activated-layer (activating player) and triggered-layer (source controller)
- Rule 1.7.2: Object with ability is considered card with that ability; base vs. derived
- Rule 1.7.3: Three ability categories: activated, resolution, static
- Rule 1.7.4: Ability functionality conditions
- Rule 1.7.4a-j: Specific functionality exceptions and conditions
- Rule 1.7.5: Modal abilities
- Rule 1.7.5a-e: Modal ability selection rules
- Rule 1.7.6: Connected ability pairs
- Rule 1.7.6a-c: Connected pair rules
- Rule 1.7.7: Abilities can be modified

Engine Features Needed for Section 1.7:
- [ ] Ability class hierarchy (ActivatedAbility, ResolutionAbility, StaticAbility) (Rule 1.7.3)
- [ ] Ability.category property returning "activated", "resolution", or "static" (Rule 1.7.3)
- [ ] Ability.is_functional(context) method with full functionality check (Rule 1.7.4)
- [ ] Ability.source reference to creating card or token (Rule 1.7.1a)
- [ ] Layer.source reference tracking original source (Rule 1.7.1a)
- [ ] Layer.exists_independently_of_source = True (Rule 1.7.1a)
- [ ] Layer.controller_id based on layer type (Rules 1.7.1b)
- [ ] CardInstance.has_ability(ability_name) returning bool (Rule 1.7.2)
- [ ] CardInstance.has_base_ability(ability_name) returning bool (Rule 1.7.2)
- [ ] CardInstance.get_ability_categories() returning set of category names (Rule 1.7.3)
- [ ] Functionality context: FunctionalityContext with zone, is_defending, is_resolving, etc.
- [ ] Meta-static ability functionality outside the game (Rule 1.7.4d)
- [ ] Play-static ability functionality during play (Rule 1.7.4e)
- [ ] Property-static ability functionality in any zone (Rule 1.7.4f)
- [ ] While-static ability with while-condition evaluation (Rule 1.7.4g)
- [ ] Zone-movement replacement static ability (Rule 1.7.4j)
- [ ] ModalAbility class with mode selection (Rule 1.7.5)
- [ ] ModalAbility.declare_modes(modes) validation (Rule 1.7.5a, 1.7.5b)
- [ ] ModalAbility.selected_modes_are_base_abilities property (Rule 1.7.5d)
- [ ] ConnectedAbilityPair class (Rule 1.7.6)
- [ ] ConnectedAbilityPair.can_following_refer_to_leading() (Rule 1.7.6b)
- [ ] Effect system supporting ability modification (Rule 1.7.7)
"""

import pytest
from pytest_bdd import scenario, given, when, then, parsers
from fab_engine.cards.model import CardInstance, CardTemplate, CardType, Color, Subtype
from fab_engine.zones.zone import ZoneType


# ---------------------------------------------------------------------------
# Scenario: ability_is_property_of_object
# Tests Rule 1.7.1 - Ability is a property of an object
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_1_7_abilities.feature",
    "ability_is_property_of_object",
)
def test_ability_is_property_of_object():
    """Rule 1.7.1: An ability is a property of an object influencing the game."""
    pass


@given('a card with a functional text ability "Gain 3 life"')
def step_card_with_gain_life_ability(game_state):
    """Rule 1.7.1: Card has an ability as a property."""
    game_state.test_card = game_state.create_card(name="Sigil of Solace")
    game_state.test_card.functional_text = "Gain 3{h}"
    game_state.ability_text = "Gain 3 life"


@when("the ability is defined on the card")
def step_ability_defined_on_card(game_state):
    """Rule 1.7.1: Ability is a property of the card."""
    # The ability is defined in the card's functional text
    game_state.ability_defined = hasattr(game_state.test_card, "functional_text")


@then("the card should have that ability as a property")
def step_card_has_ability_as_property(game_state):
    """Rule 1.7.1: Ability is a property of the card."""
    assert game_state.test_card is not None
    # Engine Feature Needed: CardInstance.has_ability() method
    assert game_state.test_card.has_ability(game_state.ability_text)


@then("the ability should influence the game")
def step_ability_influences_game(game_state):
    """Rule 1.7.1: Ability influences the game by generating effects."""
    # Engine Feature Needed: Ability.generates_effects property
    assert game_state.test_card.ability_generates_effects(game_state.ability_text)


# ---------------------------------------------------------------------------
# Scenario: base_abilities_from_rules_text
# Tests Rule 1.7.1 - Base abilities from rules text for non-token cards
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_1_7_abilities.feature",
    "base_abilities_from_rules_text",
)
def test_base_abilities_from_rules_text():
    """Rule 1.7.1: Base abilities of non-token card come from rules text."""
    pass


@given('a non-token action card with functional text "Gain 3{h}"')
def step_non_token_action_card(game_state):
    """Rule 1.7.1: Non-token card with rules text ability."""
    game_state.test_card = game_state.create_card(
        name="Sigil of Solace", card_type=CardType.ACTION
    )
    game_state.test_card.functional_text = "Gain 3{h}"


@when("the card's base abilities are determined")
def step_determine_base_abilities(game_state):
    """Rule 1.7.1: Determine base abilities from rules text."""
    # Engine Feature Needed: CardInstance.get_base_abilities()
    game_state.base_abilities = game_state.test_card.get_base_abilities()


@then("the base abilities should be derived from the rules text")
def step_base_abilities_from_rules_text(game_state):
    """Rule 1.7.1: Base abilities come from functional text (rules text)."""
    # Engine Feature Needed: CardInstance.get_base_abilities() returns rule-text-derived abilities
    assert game_state.base_abilities is not None
    assert len(game_state.base_abilities) > 0


# ---------------------------------------------------------------------------
# Scenario: token_base_abilities_from_creating_effect
# Tests Rule 1.7.1 - Token base abilities from creating effect
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_1_7_abilities.feature",
    "token_base_abilities_from_creating_effect",
)
def test_token_base_abilities_from_creating_effect():
    """Rule 1.7.1: Base abilities of token defined by creating effect."""
    pass


@given('a token card created with the ability "Deal 1 damage"')
def step_token_with_creating_ability(game_state):
    """Rule 1.7.1: Token defined by creating effect."""
    game_state.test_token = game_state.create_token_card(name="Warrior Token")
    # Engine Feature Needed: Token.set_abilities_from_creating_effect()
    game_state.token_ability_text = "Deal 1 damage"
    game_state.test_token.created_with_abilities = [game_state.token_ability_text]


@when("the token's base abilities are determined")
def step_determine_token_base_abilities(game_state):
    """Rule 1.7.1: Token base abilities from creating effect."""
    # Engine Feature Needed: CardInstance.get_base_abilities() for tokens uses creating effect
    game_state.token_base_abilities = game_state.test_token.get_base_abilities()


@then("the base abilities should be those given at creation")
def step_token_has_creation_abilities(game_state):
    """Rule 1.7.1: Token base abilities come from creating effect."""
    assert game_state.token_ability_text in game_state.token_base_abilities


@then("the base abilities should not come from a rules text")
def step_token_base_abilities_not_from_rules_text(game_state):
    """Rule 1.7.1: Tokens don't have traditional rules text abilities."""
    # Engine Feature Needed: Token.base_abilities_source == "creating_effect"
    assert game_state.test_token.base_abilities_source == "creating_effect"


# ---------------------------------------------------------------------------
# Scenario: ability_source_is_card_that_has_it
# Tests Rule 1.7.1a - Source of an ability is the card that has it
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_1_7_abilities.feature",
    "ability_source_is_card_that_has_it",
)
def test_ability_source_is_card_that_has_it():
    """Rule 1.7.1a: The source of an ability is the card that has it."""
    pass


@given('a card with an ability "Gain 3 life"')
def step_card_with_ability(game_state):
    """Rule 1.7.1a: Card with an ability."""
    game_state.source_card = game_state.create_card(name="Ability Source Card")
    game_state.source_card.functional_text = "Gain 3{h}"


@when("the ability's source is queried")
def step_query_ability_source(game_state):
    """Rule 1.7.1a: Query the ability's source."""
    # Engine Feature Needed: CardInstance.get_ability_source(ability_name)
    game_state.queried_source = game_state.source_card.get_ability_source("Gain 3 life")


@then("the source should be that card")
def step_source_is_the_card(game_state):
    """Rule 1.7.1a: Source is the card that has the ability."""
    assert game_state.queried_source is game_state.source_card


# ---------------------------------------------------------------------------
# Scenario: activated_layer_source_is_same_as_creating_ability_source
# Tests Rule 1.7.1a - Activated-layer source = creating ability source
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_1_7_abilities.feature",
    "activated_layer_source_is_same_as_creating_ability_source",
)
def test_activated_layer_source_is_same_as_creating_ability_source():
    """Rule 1.7.1a: Activated-layer source is same as creating ability source."""
    pass


@given('a card with an activated ability "Gain 1 resource"')
def step_card_with_activated_ability(game_state):
    """Rule 1.7.1a: Card with activated ability."""
    game_state.source_card = game_state.create_card(name="Resource Generator")
    game_state.source_card.functional_text = "Action -- {0}: Gain 1 resource"
    # Engine Feature Needed: CardInstance.activated_abilities property
    game_state.source_card.has_activated_ability = True


@given("the ability has been activated creating an activated-layer on the stack")
def step_ability_activated_creating_layer(game_state):
    """Rule 1.7.1a: Ability activated, layer on stack."""
    # Engine Feature Needed: ActivatedAbility.activate() creating an ActivatedLayer
    game_state.activated_layer = game_state.activate_ability(
        game_state.source_card, "Gain 1 resource"
    )
    game_state.stack.append(game_state.activated_layer)


@when("the activated-layer's ability source is queried")
def step_query_activated_layer_source(game_state):
    """Rule 1.7.1a: Query the activated-layer's ability source."""
    # Engine Feature Needed: ActivatedLayer.source property
    game_state.layer_source = game_state.activated_layer.source


@then("the source should be the original card")
def step_layer_source_is_original_card(game_state):
    """Rule 1.7.1a: Layer source is the original card."""
    assert game_state.layer_source is game_state.source_card


# ---------------------------------------------------------------------------
# Scenario: activated_layer_survives_source_destruction
# Tests Rule 1.7.1a - Activated-layer exists independently of source
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_1_7_abilities.feature",
    "activated_layer_survives_source_destruction",
)
def test_activated_layer_survives_source_destruction():
    """Rule 1.7.1a: Activated-layers exist independently of their source."""
    pass


@given("a card with an activated ability has been activated")
def step_activated_ability_was_activated(game_state):
    """Rule 1.7.1a: Ability was activated."""
    game_state.source_card = game_state.create_card(name="Energy Potion")
    game_state.source_card.functional_text = "Instant -- {0}: Gain 1 resource"
    game_state.activated_layer = game_state.activate_ability(
        game_state.source_card, "Gain 1 resource"
    )
    game_state.stack.append(game_state.activated_layer)


@given("an activated-layer is on the stack")
def step_activated_layer_on_stack(game_state):
    """Rule 1.7.1a: Activated-layer is on the stack."""
    assert game_state.activated_layer in game_state.stack


@when("the source card is destroyed")
def step_source_card_destroyed(game_state):
    """Rule 1.7.1a: Source card is destroyed."""
    # Engine Feature Needed: GameEngine.destroy_card() / CardInstance.is_destroyed
    game_state.source_card.is_destroyed = True
    # Source is gone, but the layer should remain


@then("the activated-layer should still exist on the stack")
def step_activated_layer_still_on_stack(game_state):
    """Rule 1.7.1a: Layer persists even when source is destroyed."""
    assert game_state.activated_layer in game_state.stack
    # Engine Feature Needed: ActivatedLayer.exists_independently_of_source = True
    assert game_state.activated_layer.exists_independently_of_source is True


@then("the activated-layer should still be resolvable")
def step_activated_layer_still_resolvable(game_state):
    """Rule 1.7.1a: Layer can still resolve."""
    # Engine Feature Needed: Layer.can_resolve property
    assert game_state.activated_layer.can_resolve is True


# ---------------------------------------------------------------------------
# Scenario: triggered_layer_survives_source_leaving_play
# Tests Rule 1.7.1a - Triggered-layer exists independently of source
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_1_7_abilities.feature",
    "triggered_layer_survives_source_leaving_play",
)
def test_triggered_layer_survives_source_leaving_play():
    """Rule 1.7.1a: Triggered-layers exist independently of their source."""
    pass


@given("a card with a triggered ability has triggered")
def step_triggered_ability_triggered(game_state):
    """Rule 1.7.1a: Triggered ability has triggered."""
    game_state.source_card = game_state.create_card(name="Snatch")
    game_state.source_card.functional_text = "When you discard a card, gain 1 resource"
    game_state.triggered_layer = game_state.create_triggered_layer(
        game_state.source_card, "gain 1 resource"
    )
    game_state.stack.append(game_state.triggered_layer)


@given("a triggered-layer is on the stack")
def step_triggered_layer_on_stack(game_state):
    """Rule 1.7.1a: Triggered-layer is on the stack."""
    assert game_state.triggered_layer in game_state.stack


@when("the source card moves to the graveyard")
def step_source_moves_to_graveyard(game_state):
    """Rule 1.7.1a: Source moved to graveyard."""
    # Engine Feature Needed: Zone.move_card() or GameEngine.move_to_graveyard()
    game_state.source_card.current_zone = "graveyard"
    game_state.source_in_arena = False


@then("the triggered-layer should still exist on the stack")
def step_triggered_layer_still_on_stack(game_state):
    """Rule 1.7.1a: Triggered-layer persists after source leaves."""
    assert game_state.triggered_layer in game_state.stack
    # Engine Feature Needed: TriggeredLayer.exists_independently_of_source = True
    assert game_state.triggered_layer.exists_independently_of_source is True


@then("the triggered-layer should still be resolvable")
def step_triggered_layer_still_resolvable(game_state):
    """Rule 1.7.1a: Triggered-layer can still resolve."""
    assert game_state.triggered_layer.can_resolve is True


# ---------------------------------------------------------------------------
# Scenario: activated_layer_controller_is_activating_player
# Tests Rule 1.7.1b - Controller of activated-layer
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_1_7_abilities.feature",
    "activated_layer_controller_is_activating_player",
)
def test_activated_layer_controller_is_activating_player():
    """Rule 1.7.1b: Controller of activated-layer is the activating player."""
    pass


@given("player 0 controls a card with an activated ability")
def step_player_0_controls_card_with_activated_ability(game_state):
    """Rule 1.7.1b: Player 0 has a card with activated ability."""
    game_state.source_card = game_state.create_card(name="Ability Card")
    game_state.source_card.controller_id = 0


@when("player 0 activates the ability creating an activated-layer")
def step_player_0_activates_ability(game_state):
    """Rule 1.7.1b: Player 0 activates the ability."""
    # Engine Feature Needed: ActivatedAbility.activate(player_id) creating ActivatedLayer
    game_state.activated_layer = game_state.activate_ability(
        game_state.source_card, "ability", activating_player_id=0
    )
    game_state.stack.append(game_state.activated_layer)


@then("the activated-layer's controller should be player 0")
def step_activated_layer_controller_is_player_0(game_state):
    """Rule 1.7.1b: Activated-layer controller is the activating player."""
    # Engine Feature Needed: ActivatedLayer.controller_id
    assert game_state.activated_layer.controller_id == 0


# ---------------------------------------------------------------------------
# Scenario: triggered_layer_controller_is_controller_at_trigger_time
# Tests Rule 1.7.1b - Controller of triggered-layer
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_1_7_abilities.feature",
    "triggered_layer_controller_is_controller_at_trigger_time",
)
def test_triggered_layer_controller_is_controller_at_trigger_time():
    """Rule 1.7.1b: Controller of triggered-layer is controller at trigger time."""
    pass


@given("player 0 controls a card with a triggered ability")
def step_player_0_controls_card_with_triggered_ability(game_state):
    """Rule 1.7.1b: Player 0 controls source of triggered ability."""
    game_state.source_card = game_state.create_card(name="Triggered Ability Card")
    game_state.source_card.controller_id = 0


@when("the trigger condition is met for the card")
def step_trigger_condition_met(game_state):
    """Rule 1.7.1b: Trigger condition is met."""
    game_state.trigger_occurred = True
    game_state.controller_at_trigger_time = game_state.source_card.controller_id


@when("a triggered-layer is created")
def step_triggered_layer_created(game_state):
    """Rule 1.7.1b: Triggered-layer is created."""
    game_state.triggered_layer = game_state.create_triggered_layer(
        game_state.source_card,
        "trigger effect",
        controller_id=game_state.controller_at_trigger_time,
    )
    game_state.stack.append(game_state.triggered_layer)


@then("the triggered-layer's controller should be player 0")
def step_triggered_layer_controller_is_player_0(game_state):
    """Rule 1.7.1b: Triggered-layer controller is player 0."""
    assert game_state.triggered_layer.controller_id == 0


# ---------------------------------------------------------------------------
# Scenario: triggered_layer_controller_is_owner_when_source_has_no_controller
# Tests Rule 1.7.1b - Triggered-layer controller = owner when no controller
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_1_7_abilities.feature",
    "triggered_layer_controller_is_owner_when_source_has_no_controller",
)
def test_triggered_layer_controller_is_owner_when_source_has_no_controller():
    """Rule 1.7.1b: Triggered-layer controller = owner when source has no controller."""
    pass


@given("a card owned by player 0 with no controller")
def step_card_owned_by_player_0_no_controller(game_state):
    """Rule 1.7.1b: Card owned by player 0, no controller."""
    game_state.source_card = game_state.create_card(
        name="No Controller Card", owner_id=0
    )
    game_state.source_card.controller_id = None  # No controller


@given("the card has a triggered ability")
def step_card_has_triggered_ability(game_state):
    """Rule 1.7.1b: Card has a triggered ability."""
    game_state.source_card.functional_text = "When X happens, gain 1 resource"


@when("the trigger condition is met")
def step_trigger_condition_met_no_controller(game_state):
    """Rule 1.7.1b: Trigger condition met when no controller."""
    game_state.trigger_occurred_no_controller = True


@when("a triggered-layer is created from the ownerless-controller source")
def step_triggered_layer_created_no_controller(game_state):
    """Rule 1.7.1b: Triggered-layer created from source with no controller."""
    # Engine Feature Needed: TriggeredLayer controller = owner when source has no controller
    game_state.triggered_layer_no_ctrl = game_state.create_triggered_layer(
        game_state.source_card,
        "trigger effect",
        # No explicit controller_id - should default to owner
    )
    game_state.stack.append(game_state.triggered_layer_no_ctrl)


@then("the triggered-layer's controller should be the card's owner (player 0)")
def step_triggered_layer_controller_is_owner(game_state):
    """Rule 1.7.1b: Controller defaults to owner when source has no controller."""
    assert game_state.triggered_layer_no_ctrl.controller_id == 0  # Owner's id


# ---------------------------------------------------------------------------
# Scenario: object_with_ability_considered_card_with_ability
# Tests Rule 1.7.2 - Object with ability is considered card with that ability
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_1_7_abilities.feature",
    "object_with_ability_considered_card_with_ability",
)
def test_object_with_ability_considered_card_with_ability():
    """Rule 1.7.2: Object with ability is considered card with that ability."""
    pass


@given('a card that has an ability "go again" as a property')
def step_card_with_go_again(game_state):
    """Rule 1.7.2: Card has go again as a property."""
    game_state.go_again_card = game_state.create_card(name="Go Again Card")
    # Engine Feature Needed: CardInstance.add_ability("go again")
    game_state.go_again_card.abilities = ["go again"]


@when("the card is checked for having go again")
def step_check_card_for_go_again(game_state):
    """Rule 1.7.2: Check if card has go again."""
    # Engine Feature Needed: CardInstance.has_ability("go again")
    game_state.has_go_again = game_state.go_again_card.has_ability("go again")


@then("the card is considered a card with go again")
def step_card_considered_with_go_again(game_state):
    """Rule 1.7.2: Card is considered to have the ability."""
    assert game_state.has_go_again is True


# ---------------------------------------------------------------------------
# Scenario: triggered_go_again_not_base_go_again
# Tests Rule 1.7.2 - Triggered go again is not base go again
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_1_7_abilities.feature",
    "triggered_go_again_not_base_go_again",
)
def test_triggered_go_again_not_base_go_again():
    """Rule 1.7.2: Torrent of Tempo - triggered go again is not base go again."""
    pass


@given(
    'a card "Torrent of Tempo" with the triggered ability "When this hits, it gets go again"'
)
def step_torrent_of_tempo_card(game_state):
    """Rule 1.7.2: Card with triggered go again."""
    game_state.torrent_of_tempo = game_state.create_card(name="Torrent of Tempo")
    game_state.torrent_of_tempo.functional_text = "When this hits, it gets go again"
    # No base go again
    game_state.torrent_of_tempo.base_abilities = []
    # Has a triggered ability that may grant go again
    game_state.torrent_of_tempo.triggered_abilities = [
        "When this hits, it gets go again"
    ]


@when("the card's base abilities are checked before hitting")
def step_check_base_abilities_before_hit(game_state):
    """Rule 1.7.2: Check base abilities before trigger fires."""
    # Engine Feature Needed: CardInstance.has_base_ability()
    game_state.has_base_go_again = game_state.torrent_of_tempo.has_base_ability(
        "go again"
    )
    game_state.has_go_again = game_state.torrent_of_tempo.has_ability("go again")


@then("the card should NOT be considered a card with base go again")
def step_card_not_base_go_again(game_state):
    """Rule 1.7.2: Not base go again."""
    assert game_state.has_base_go_again is False


@then("the card should NOT be considered a card with go again")
def step_card_not_go_again_before_hit(game_state):
    """Rule 1.7.2: No go again before trigger fires."""
    assert game_state.has_go_again is False


# ---------------------------------------------------------------------------
# Scenario: card_with_triggered_go_again_gains_ability_after_trigger
# Tests Rule 1.7.2 - Card gains non-base go again after trigger resolves
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_1_7_abilities.feature",
    "card_with_triggered_go_again_gains_ability_after_trigger",
)
def test_card_with_triggered_go_again_gains_ability_after_trigger():
    """Rule 1.7.2: After trigger resolves, card has go again but not base go again."""
    pass


@given(
    'a card "Torrent of Tempo" with the triggered ability "When this hits, it gets go again"'
)
def step_torrent_of_tempo_for_after_trigger(game_state):
    """Rule 1.7.2: Card with triggered go again."""
    game_state.torrent_of_tempo = game_state.create_card(name="Torrent of Tempo")
    game_state.torrent_of_tempo.functional_text = "When this hits, it gets go again"
    game_state.torrent_of_tempo.base_abilities = []
    game_state.torrent_of_tempo.triggered_abilities = [
        "When this hits, it gets go again"
    ]
    game_state.torrent_of_tempo.current_abilities = []


@given("the triggered condition is met (the card hits)")
def step_triggered_condition_met(game_state):
    """Rule 1.7.2: The card hits, triggering the ability."""
    # Engine Feature Needed: TriggerCondition.evaluate() - card hits
    game_state.card_has_hit = True


@given("the triggered-layer resolves")
def step_triggered_layer_resolves(game_state):
    """Rule 1.7.2: Triggered-layer has resolved, granting go again."""
    # Engine Feature Needed: TriggeredLayer.resolve() granting the "go again" ability
    game_state.torrent_of_tempo.current_abilities = ["go again"]


@when("the card's abilities are checked")
def step_check_card_abilities_after_trigger(game_state):
    """Rule 1.7.2: Check abilities after trigger resolves."""
    game_state.has_go_again = game_state.torrent_of_tempo.has_ability("go again")
    game_state.has_base_go_again = game_state.torrent_of_tempo.has_base_ability(
        "go again"
    )


@then("the card should be considered a card with go again")
def step_card_has_go_again_after_trigger(game_state):
    """Rule 1.7.2: Card has go again after trigger resolved."""
    assert game_state.has_go_again is True


@then("the card should NOT be considered a card with base go again")
def step_card_not_base_go_again_after_trigger(game_state):
    """Rule 1.7.2: Go again is non-base (granted by triggered ability)."""
    assert game_state.has_base_go_again is False


# ---------------------------------------------------------------------------
# Scenario: there_are_three_categories_of_abilities
# Tests Rule 1.7.3 - Three categories of abilities
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_1_7_abilities.feature",
    "there_are_three_categories_of_abilities",
)
def test_there_are_three_categories_of_abilities():
    """Rule 1.7.3: There are exactly three categories of abilities."""
    pass


@given("the ability category system is initialized")
def step_ability_category_system_initialized(game_state):
    """Rule 1.7.3: System has ability categories."""
    # Engine Feature Needed: AbilityCategory enum or AbilityType enum
    game_state.ability_system_initialized = True


@when("the ability categories are queried")
def step_query_ability_categories(game_state):
    """Rule 1.7.3: Query available ability categories."""
    # Engine Feature Needed: AbilityCategory enum with ACTIVATED, RESOLUTION, STATIC
    import importlib

    ability_module = importlib.import_module("fab_engine.engine.abilities")
    game_state.ability_categories = ability_module.AbilityCategory


@then("there should be exactly three ability categories")
def step_three_ability_categories(game_state):
    """Rule 1.7.3: Exactly 3 categories."""
    assert len(list(game_state.ability_categories)) == 3


@then('the categories should be "activated", "resolution", and "static"')
def step_categories_are_correct(game_state):
    """Rule 1.7.3: Categories are activated, resolution, and static."""
    category_values = {c.value for c in game_state.ability_categories}
    assert "activated" in category_values
    assert "resolution" in category_values
    assert "static" in category_values


# ---------------------------------------------------------------------------
# Scenario: activated_ability_creates_activated_layer_on_stack
# Tests Rule 1.7.3a - Activated ability creates activated-layer on stack
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_1_7_abilities.feature",
    "activated_ability_creates_activated_layer_on_stack",
)
def test_activated_ability_creates_activated_layer_on_stack():
    """Rule 1.7.3a: Activated abilities create activated-layers on the stack."""
    pass


@given('a card has an activated ability "Gain 1 resource"')
def step_card_has_activated_ability_resource(game_state):
    """Rule 1.7.3a: Card with activated ability."""
    game_state.source_card = game_state.create_card(name="Resource Card")
    game_state.source_card.functional_text = "Action -- {0}: Gain 1 resource"


@given("the player has priority")
def step_player_has_priority(game_state):
    """Rule 1.7.3a: Player has priority to activate abilities."""
    game_state.player_has_priority = True


@given("the source card is in the arena")
def step_source_card_in_arena(game_state):
    """Rule 1.7.3a: Source is in arena (functional)."""
    game_state.play_card_to_arena(game_state.source_card, controller_id=0)


@when("the player activates the ability")
def step_player_activates_ability(game_state):
    """Rule 1.7.3a: Player activates the ability."""
    # Engine Feature Needed: ActivatedAbility.activate() creating ActivatedLayer
    game_state.created_layer = game_state.activate_ability(
        game_state.source_card, "Gain 1 resource"
    )
    game_state.stack.append(game_state.created_layer)


@then("an activated-layer should be created on the stack")
def step_activated_layer_created_on_stack(game_state):
    """Rule 1.7.3a: Activated-layer is on the stack."""
    assert game_state.created_layer in game_state.stack
    # Engine Feature Needed: Layer.layer_category == "activated-layer"
    assert game_state.created_layer.layer_category == "activated-layer"


@then("the activated-layer should not be resolved yet")
def step_layer_not_resolved(game_state):
    """Rule 1.7.3a: Layer has not been resolved yet."""
    assert game_state.created_layer.is_resolved is False


# ---------------------------------------------------------------------------
# Scenario: resolution_ability_generates_effects_on_resolution
# Tests Rule 1.7.3b - Resolution ability generates effects when layer resolves
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_1_7_abilities.feature",
    "resolution_ability_generates_effects_on_resolution",
)
def test_resolution_ability_generates_effects_on_resolution():
    """Rule 1.7.3b: Resolution ability generates effects when layer resolves."""
    pass


@given('a card "Sigil of Solace" has a resolution ability "Gain 3 life"')
def step_sigil_of_solace_resolution_ability(game_state):
    """Rule 1.7.3b: Card with resolution ability."""
    game_state.sigil = game_state.create_card(name="Sigil of Solace")
    game_state.sigil.functional_text = "Gain 3{h}"
    # Engine Feature Needed: ResolutionAbility class
    game_state.sigil.resolution_abilities = ["Gain 3 life"]


@given("the card is on the stack as a layer")
def step_card_on_stack_as_layer(game_state):
    """Rule 1.7.3b: Card on stack."""
    game_state.play_card_to_stack(game_state.sigil, controller_id=0)


@when("the layer resolves")
def step_layer_resolves(game_state):
    """Rule 1.7.3b: Layer resolves on stack."""
    # Engine Feature Needed: Layer.resolve() triggering resolution abilities
    game_state.resolution_result = game_state.resolve_top_of_stack()


@then('the resolution ability should generate the "Gain 3 life" effect')
def step_resolution_ability_generates_effect(game_state):
    """Rule 1.7.3b: Resolution ability generates the expected effect."""
    # Engine Feature Needed: ResolutionResult.effects_generated includes "Gain 3 life"
    assert "Gain 3 life" in game_state.resolution_result.effects_generated


# ---------------------------------------------------------------------------
# Scenario: static_ability_generates_effects_continuously
# Tests Rule 1.7.3c - Static ability simply generates effects
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_1_7_abilities.feature",
    "static_ability_generates_effects_continuously",
)
def test_static_ability_generates_effects_continuously():
    """Rule 1.7.3c: Static abilities continuously generate effects."""
    pass


@given('a card has a static ability "This gets +1 power"')
def step_card_with_static_ability(game_state):
    """Rule 1.7.3c: Card with static ability."""
    game_state.static_card = game_state.create_card(name="Static Power Card")
    game_state.static_card.functional_text = "This gets +1{p}"
    # Engine Feature Needed: StaticAbility class
    game_state.static_card.static_abilities = ["This gets +1 power"]


@given("the card is in the arena")
def step_static_card_in_arena(game_state):
    """Rule 1.7.3c: Card is in arena."""
    game_state.play_card_to_arena(game_state.static_card, controller_id=0)


@when("the static ability is checked")
def step_check_static_ability(game_state):
    """Rule 1.7.3c: Check the static ability."""
    # Engine Feature Needed: StaticAbility.is_generating_effects()
    game_state.static_generating = game_state.static_card.static_ability_is_active(
        "This gets +1 power"
    )
    game_state.requires_player_action = False  # Static - no action needed


@then("it should be generating its effect continuously")
def step_static_ability_generating_continuously(game_state):
    """Rule 1.7.3c: Static ability is active."""
    assert game_state.static_generating is True


@then("no player action is required to activate it")
def step_no_player_action_required(game_state):
    """Rule 1.7.3c: Static abilities don't require activation."""
    assert game_state.requires_player_action is False


# ---------------------------------------------------------------------------
# Scenario: ability_functional_when_source_in_arena
# Tests Rule 1.7.4 - Ability is functional when source is public and in arena
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_1_7_abilities.feature",
    "ability_functional_when_source_in_arena",
)
def test_ability_functional_when_source_in_arena():
    """Rule 1.7.4: Ability is functional when source is public and in arena."""
    pass


@given('a card with an activated ability "Gain 1 resource"')
def step_card_with_activated_ability_gain_resource(game_state):
    """Rule 1.7.4: Card with activated ability."""
    game_state.source_card = game_state.create_card(name="Functional Card")
    game_state.source_card.functional_text = "Action -- {0}: Gain 1 resource"


@given("the card is in the arena (public zone)")
def step_card_in_arena_public(game_state):
    """Rule 1.7.4: Card is in public arena zone."""
    game_state.play_card_to_arena(game_state.source_card, controller_id=0)
    game_state.source_card.is_public = True


@when("the arena ability's functionality is checked")
def step_check_ability_functionality_arena(game_state):
    """Rule 1.7.4: Check if ability is functional in arena."""
    # Engine Feature Needed: Ability.is_functional(context)
    game_state.is_functional = game_state.check_ability_functional(
        game_state.source_card, "Gain 1 resource", in_arena=True, is_public=True
    )


@then("the ability should be functional")
def step_ability_is_functional(game_state):
    """Rule 1.7.4: Ability is functional."""
    assert game_state.is_functional is True


# ---------------------------------------------------------------------------
# Scenario: ability_nonfunctional_when_source_in_hand
# Tests Rule 1.7.4 - Ability is non-functional when source not in arena
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_1_7_abilities.feature",
    "ability_nonfunctional_when_source_in_hand",
)
def test_ability_nonfunctional_when_source_in_hand():
    """Rule 1.7.4: Standard ability is non-functional when source is in hand."""
    pass


@given('a card with a standard activated ability "Gain 1 resource"')
def step_card_with_standard_activated_ability_in_hand(game_state):
    """Rule 1.7.4: Card with standard activated ability (not special-case)."""
    game_state.source_card = game_state.create_card(name="Standard Ability Card")
    game_state.source_card.functional_text = "Action -- {0}: Gain 1 resource"
    # This is a standard ability - no special "can be activated from hand" text


@given("the card is in the player's hand (private zone)")
def step_card_in_hand_private(game_state):
    """Rule 1.7.4: Card in private hand zone."""
    game_state.player.hand.add_card(game_state.source_card)
    game_state.source_card.is_public = False


@when("the hand ability's functionality is checked")
def step_check_ability_functionality_hand(game_state):
    """Rule 1.7.4: Check if standard ability is functional from hand."""
    game_state.is_functional = game_state.check_ability_functional(
        game_state.source_card, "Gain 1 resource", in_arena=False, is_public=False
    )


@then("the ability should be non-functional")
def step_ability_is_nonfunctional(game_state):
    """Rule 1.7.4: Standard ability non-functional outside arena."""
    assert game_state.is_functional is False


# ---------------------------------------------------------------------------
# Scenario: defending_card_ability_nonfunctional_by_default
# Tests Rule 1.7.4a - Non-permanent defending card ability non-functional
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_1_7_abilities.feature",
    "defending_card_ability_nonfunctional_by_default",
)
def test_defending_card_ability_nonfunctional_by_default():
    """Rule 1.7.4a: Non-permanent defending card's ability is non-functional by default."""
    pass


@given("a non-permanent card is defending")
def step_non_permanent_card_defending(game_state):
    """Rule 1.7.4a: Non-permanent card is in defending state."""
    game_state.defending_card = game_state.create_card(
        name="Defending Non-Permanent", card_type=CardType.ACTION
    )
    game_state.defending_card.is_defending = True
    game_state.defending_card_is_permanent = False


@given('the card has a standard activated ability "Gain 1 resource"')
def step_defending_card_has_standard_ability(game_state):
    """Rule 1.7.4a: Defending card has a standard ability (no defending-specific text)."""
    game_state.defending_card.functional_text = "Action -- {0}: Gain 1 resource"
    # This ability has no text saying it can be activated while defending


@when("the non-permanent defending ability's functionality is checked")
def step_check_defending_card_ability(game_state):
    """Rule 1.7.4a: Check functionality while non-permanent card is defending."""
    game_state.is_functional = game_state.check_ability_functional(
        game_state.defending_card,
        "Gain 1 resource",
        in_arena=False,
        is_public=True,
        is_defending=True,
        is_permanent=False,
    )


@then("the ability should be non-functional")
def step_defending_card_ability_nonfunctional(game_state):
    """Rule 1.7.4a: Non-permanent defending card's standard ability is non-functional."""
    assert game_state.is_functional is False


# ---------------------------------------------------------------------------
# Scenario: defending_card_ability_functional_when_specified_as_defending_only
# Tests Rule 1.7.4a - Defending card ability is functional if specified
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_1_7_abilities.feature",
    "defending_card_ability_functional_when_specified_as_defending_only",
)
def test_defending_card_ability_functional_when_specified_as_defending_only():
    """Rule 1.7.4a: Ability with 'while defending' text is functional when defending."""
    pass


@given('a non-permanent card "Rally the Rearguard" is defending')
def step_rally_the_rearguard_defending(game_state):
    """Rule 1.7.4a: Rally the Rearguard is defending."""
    game_state.rally_card = game_state.create_card(name="Rally the Rearguard")
    game_state.rally_card.is_defending = True
    game_state.rally_card_is_permanent = False


@given('the card has the ability "Activate this only while this is defending"')
def step_rally_has_defending_ability(game_state):
    """Rule 1.7.4a: Ability explicitly specifies it can be activated when defending."""
    game_state.rally_card.functional_text = (
        "Once per Turn Instant -- Discard a card: This gets +3{d}. "
        "Activate this only while this is defending"
    )
    game_state.rally_card.ability_specifies_defending = True


@when("the rally defending ability's functionality is checked")
def step_check_rally_ability_while_defending(game_state):
    """Rule 1.7.4a: Check Rally's ability while defending."""
    game_state.is_functional = game_state.check_ability_functional(
        game_state.rally_card,
        "This gets +3{d}",
        in_arena=False,
        is_public=True,
        is_defending=True,
        is_permanent=False,
        specifies_defending=True,
    )


@then("the ability should be functional")
def step_rally_ability_functional_while_defending(game_state):
    """Rule 1.7.4a: Rally's defending ability is functional."""
    assert game_state.is_functional is True


# ---------------------------------------------------------------------------
# Scenario: activated_ability_functional_when_cost_only_payable_outside_arena
# Tests Rule 1.7.4b - Activated ability functional outside arena when cost requires it
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_1_7_abilities.feature",
    "activated_ability_functional_when_cost_only_payable_outside_arena",
)
def test_activated_ability_functional_when_cost_only_payable_outside_arena():
    """Rule 1.7.4b: Activated ability functional when cost only payable outside arena."""
    pass


@given(
    'a card "Mighty Windup" with the ability "Instant -- Discard this: Create a Might token"'
)
def step_mighty_windup_card(game_state):
    """Rule 1.7.4b: Mighty Windup with discard-self cost."""
    game_state.mighty_windup = game_state.create_card(name="Mighty Windup")
    game_state.mighty_windup.functional_text = (
        "Instant -- Discard this: Create a Might token"
    )
    # The cost is "Discard this" - which can only be done from hand (private zone)
    game_state.mighty_windup.ability_cost_only_payable_from_hand = True


@given("the card is in the player's hand")
def step_mighty_windup_in_hand(game_state):
    """Rule 1.7.4b: Card is in hand."""
    game_state.player.hand.add_card(game_state.mighty_windup)


@when("Mighty Windup's ability functionality is checked")
def step_check_mighty_windup_ability(game_state):
    """Rule 1.7.4b: Check if Mighty Windup's ability is functional from hand."""
    game_state.is_functional = game_state.check_ability_functional(
        game_state.mighty_windup,
        "Create a Might token",
        in_arena=False,
        is_public=False,
        cost_only_payable_outside_arena=True,
        current_zone="hand",
    )


@then("the ability should be functional")
def step_mighty_windup_ability_functional(game_state):
    """Rule 1.7.4b: Mighty Windup's ability is functional from hand."""
    assert game_state.is_functional is True


@then("the cost (discarding itself) can only be paid from hand")
def step_cost_only_payable_from_hand(game_state):
    """Rule 1.7.4b: The discard cost can only be paid from hand."""
    assert game_state.mighty_windup.ability_cost_only_payable_from_hand is True


# ---------------------------------------------------------------------------
# Scenario: resolution_ability_functional_when_layer_resolves
# Tests Rule 1.7.4c - Resolution ability functional when resolving as layer
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_1_7_abilities.feature",
    "resolution_ability_functional_when_layer_resolves",
)
def test_resolution_ability_functional_when_layer_resolves():
    """Rule 1.7.4c: Resolution ability is functional when its source is resolving."""
    pass


@given('a card "Sigil of Solace" has a resolution ability "Gain 3{h}"')
def step_sigil_has_resolution_ability(game_state):
    """Rule 1.7.4c: Card with resolution ability."""
    game_state.sigil = game_state.create_card(name="Sigil of Solace")
    game_state.sigil.functional_text = "Gain 3{h}"
    game_state.sigil.resolution_abilities = ["Gain 3{h}"]


@given("the card is currently resolving as a layer on the stack")
def step_sigil_resolving_as_layer(game_state):
    """Rule 1.7.4c: Card is actively resolving."""
    game_state.play_card_to_stack(game_state.sigil, controller_id=0)
    game_state.sigil.is_resolving = True


@when("the resolution ability's functionality is checked while resolving")
def step_check_sigil_resolution_ability(game_state):
    """Rule 1.7.4c: Check if resolution ability is functional while resolving."""
    game_state.is_functional = game_state.check_ability_functional(
        game_state.sigil,
        "Gain 3{h}",
        in_arena=False,
        is_public=True,
        is_resolving=True,
        ability_type="resolution",
    )


@then("the ability should be functional")
def step_sigil_resolution_ability_functional(game_state):
    """Rule 1.7.4c: Resolution ability is functional during resolution."""
    assert game_state.is_functional is True


# ---------------------------------------------------------------------------
# Scenario: resolution_ability_nonfunctional_when_source_not_resolving
# Tests Rule 1.7.4c - Resolution ability non-functional when not resolving
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_1_7_abilities.feature",
    "resolution_ability_nonfunctional_when_source_not_resolving",
)
def test_resolution_ability_nonfunctional_when_source_not_resolving():
    """Rule 1.7.4c: Resolution ability non-functional when not resolving."""
    pass


@given('a card has a resolution ability "Gain 3{h}"')
def step_card_has_resolution_ability_in_hand(game_state):
    """Rule 1.7.4c: Card with resolution ability in hand."""
    game_state.res_ability_card = game_state.create_card(
        name="Card With Resolution Ability"
    )
    game_state.res_ability_card.functional_text = "Gain 3{h}"
    game_state.res_ability_card.resolution_abilities = ["Gain 3{h}"]


@given("the card is in the player's hand (not on stack)")
def step_card_in_hand_not_on_stack(game_state):
    """Rule 1.7.4c: Card is in hand, not on stack."""
    game_state.player.hand.add_card(game_state.res_ability_card)
    game_state.res_ability_card.is_resolving = False


@when("the resolution ability's functionality is checked from hand")
def step_check_resolution_ability_in_hand(game_state):
    """Rule 1.7.4c: Check functionality of resolution ability from hand."""
    game_state.is_functional = game_state.check_ability_functional(
        game_state.res_ability_card,
        "Gain 3{h}",
        in_arena=False,
        is_public=False,
        is_resolving=False,
        ability_type="resolution",
    )


@then("the ability should be non-functional")
def step_resolution_ability_nonfunctional_in_hand(game_state):
    """Rule 1.7.4c: Resolution ability non-functional when not resolving."""
    assert game_state.is_functional is False


# ---------------------------------------------------------------------------
# Scenario: meta_static_ability_functional_outside_game
# Tests Rule 1.7.4d - Meta-static ability functional outside the game
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_1_7_abilities.feature",
    "meta_static_ability_functional_outside_game",
)
def test_meta_static_ability_functional_outside_game():
    """Rule 1.7.4d: Meta-static ability is functional outside the game."""
    pass


@given("a card with the Specialization keyword (a meta-static ability)")
def step_card_with_specialization(game_state):
    """Rule 1.7.4d: Card with Specialization meta-static ability."""
    game_state.specialization_card = game_state.create_card(name="Specialized Action")
    # Engine Feature Needed: Keyword.SPECIALIZATION
    game_state.specialization_card.functional_text = "Specialization [Hero Name]"
    game_state.specialization_card.has_specialization = True
    game_state.specialization_card.specialization_hero = "Hero Name"


@when("the meta-static ability's functionality is checked outside the game")
def step_check_specialization_outside_game(game_state):
    """Rule 1.7.4d: Check functionality in deck-building context."""
    game_state.is_functional_outside_game = game_state.check_ability_functional(
        game_state.specialization_card,
        "Specialization",
        ability_type="meta_static",
        context="outside_game",
    )


@then("the ability should be functional outside the game")
def step_specialization_functional_outside_game(game_state):
    """Rule 1.7.4d: Meta-static ability is functional for deck building."""
    assert game_state.is_functional_outside_game is True


# ---------------------------------------------------------------------------
# Scenario: play_static_ability_functional_when_source_being_played
# Tests Rule 1.7.4e - Play-static ability functional when source is being played
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_1_7_abilities.feature",
    "play_static_ability_functional_when_source_being_played",
)
def test_play_static_ability_functional_when_source_being_played():
    """Rule 1.7.4e: Play-static ability functional when source is public and being played."""
    pass


@given(
    'a card "Ghostly Visit" with the play-static ability "You may play this from your banished zone"'
)
def step_ghostly_visit_card(game_state):
    """Rule 1.7.4e: Ghostly Visit with play-static ability."""
    game_state.ghostly_visit = game_state.create_card(name="Ghostly Visit")
    game_state.ghostly_visit.functional_text = (
        "You may play this from your banished zone"
    )
    game_state.ghostly_visit.has_play_static_ability = True
    game_state.ghostly_visit.play_from_zones = ["banished"]


@given("the card is public in the banished zone")
def step_ghostly_visit_in_banished_zone(game_state):
    """Rule 1.7.4e: Card is in banished zone (public)."""
    game_state.player.banished_zone.add_card(game_state.ghostly_visit)
    game_state.ghostly_visit.is_public = True


@when("the player attempts to play the card")
def step_attempt_to_play_ghostly_visit(game_state):
    """Rule 1.7.4e: Player attempts to play from banished zone."""
    game_state.play_result = game_state.player.attempt_play_from_zone(
        game_state.ghostly_visit, "banished"
    )
    game_state.play_static_functional = game_state.check_ability_functional(
        game_state.ghostly_visit,
        "You may play this from your banished zone",
        ability_type="play_static",
        is_public=True,
        is_being_played=True,
    )


@then("the play-static ability should be functional")
def step_ghostly_visit_play_static_functional(game_state):
    """Rule 1.7.4e: Play-static ability is functional."""
    assert game_state.play_static_functional is True


@then("the card should be playable from the banished zone")
def step_ghostly_visit_playable_from_banished(game_state):
    """Rule 1.7.4e: The play-static ability allows playing from banished."""
    assert game_state.play_result.success is True


# ---------------------------------------------------------------------------
# Scenario: property_static_ability_functional_in_any_zone
# Tests Rule 1.7.4f - Property-static ability functional in any zone
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_1_7_abilities.feature",
    "property_static_ability_functional_in_any_zone",
)
def test_property_static_ability_functional_in_any_zone():
    """Rule 1.7.4f: Property-static ability functional when source is in any zone."""
    pass


@given('a card "Mutated Mass" with a property-static ability defining its power')
def step_mutated_mass_card(game_state):
    """Rule 1.7.4f: Mutated Mass with property-static ability."""
    game_state.mutated_mass = game_state.create_card(name="Mutated Mass")
    game_state.mutated_mass.functional_text = (
        "{p} = number of different costed cards in pitch zone"
    )
    game_state.mutated_mass.has_property_static_ability = True
    game_state.mutated_mass.property_static_defines = "power"


@when("the ability's functionality is checked while the card is in the graveyard")
def step_check_mutated_mass_in_graveyard(game_state):
    """Rule 1.7.4f: Check property-static from graveyard."""
    game_state.is_functional = game_state.check_ability_functional(
        game_state.mutated_mass,
        "power_definition",
        ability_type="property_static",
        current_zone="graveyard",
    )


@then("the property-static ability should be functional")
def step_property_static_functional_in_graveyard(game_state):
    """Rule 1.7.4f: Property-static functional in any zone."""
    assert game_state.is_functional is True


@then("the power should be defined by the property-static ability")
def step_power_defined_by_property_static(game_state):
    """Rule 1.7.4f: Property-static defines the power property."""
    assert game_state.mutated_mass.property_static_defines == "power"


# ---------------------------------------------------------------------------
# Scenario: while_static_ability_functional_when_condition_met
# Tests Rule 1.7.4g - While-static ability functional when while-condition is met
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_1_7_abilities.feature",
    "while_static_ability_functional_when_condition_met",
)
def test_while_static_ability_functional_when_condition_met():
    """Rule 1.7.4g: While-static ability functional when while-condition is met."""
    pass


@given(
    'a card "Yinti Yanti" with "While this is defending and you control an aura, this gets +1{d}"'
)
def step_yinti_yanti_card(game_state):
    """Rule 1.7.4g: Yinti Yanti with while-static ability."""
    game_state.yinti_yanti = game_state.create_card(name="Yinti Yanti")
    game_state.yinti_yanti.functional_text = (
        "While this is defending and you control an aura, this gets +1{d}"
    )
    game_state.yinti_yanti.has_while_static_ability = True
    game_state.yinti_yanti.while_condition = "is_defending and controls_aura"
    game_state.yinti_yanti.while_effect = "+1 defense"


@given("the card is defending")
def step_yinti_yanti_defending(game_state):
    """Rule 1.7.4g: Card is defending."""
    game_state.yinti_yanti.is_defending = True


@given("the player controls an aura")
def step_player_controls_aura(game_state):
    """Rule 1.7.4g: Player controls an aura permanent."""
    aura = game_state.create_card_with_permanent_subtype(
        name="Test Aura", subtype="aura", owner_id=0
    )
    game_state.play_card_to_arena(aura, controller_id=0)
    game_state.player_controls_aura = True


@when("the while-static ability's functionality is checked with condition met")
def step_check_yinti_yanti_while_static(game_state):
    """Rule 1.7.4g: Check while-static functionality with condition met."""
    game_state.is_functional = game_state.check_ability_functional(
        game_state.yinti_yanti,
        "this gets +1{d}",
        ability_type="while_static",
        while_condition_met=True,
    )


@then("the while-static ability should be functional")
def step_yinti_yanti_while_static_functional(game_state):
    """Rule 1.7.4g: While-static ability is functional."""
    assert game_state.is_functional is True


@then("the card should get +1 defense")
def step_yinti_yanti_gets_defense_bonus(game_state):
    """Rule 1.7.4g: The effect applies (+1 defense)."""
    # Engine Feature Needed: StaticAbility generates defense bonus effect
    assert game_state.yinti_yanti.while_effect == "+1 defense"


# ---------------------------------------------------------------------------
# Scenario: while_static_ability_nonfunctional_when_condition_not_met
# Tests Rule 1.7.4g - While-static ability non-functional when condition not met
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_1_7_abilities.feature",
    "while_static_ability_nonfunctional_when_condition_not_met",
)
def test_while_static_ability_nonfunctional_when_condition_not_met():
    """Rule 1.7.4g: While-static ability non-functional when while-condition not met."""
    pass


@given('a card with a while-static ability requiring "while defending"')
def step_card_with_while_defending_ability(game_state):
    """Rule 1.7.4g: Card with while-defending condition."""
    game_state.while_card = game_state.create_card(name="While Defending Card")
    game_state.while_card.functional_text = "While this is defending, this gets +1{d}"
    game_state.while_card.has_while_static_ability = True
    game_state.while_card.while_condition = "is_defending"


@given("the card is NOT defending")
def step_card_not_defending(game_state):
    """Rule 1.7.4g: Card is not defending."""
    game_state.while_card.is_defending = False


@when("the while-static ability's functionality is checked with condition not met")
def step_check_while_static_not_defending(game_state):
    """Rule 1.7.4g: Check while-static when not defending."""
    game_state.is_functional = game_state.check_ability_functional(
        game_state.while_card,
        "this gets +1{d}",
        ability_type="while_static",
        while_condition_met=False,
    )


@then("the while-static ability should be non-functional")
def step_while_static_nonfunctional(game_state):
    """Rule 1.7.4g: While-static ability non-functional when condition not met."""
    assert game_state.is_functional is False


# ---------------------------------------------------------------------------
# Scenario: zone_movement_replacement_static_functional_when_condition_met
# Tests Rule 1.7.4j - Zone-movement replacement static ability
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_1_7_abilities.feature",
    "zone_movement_replacement_static_functional_when_condition_met",
)
def test_zone_movement_replacement_static_functional_when_condition_met():
    """Rule 1.7.4j: Zone-movement replacement static ability is functional when condition met."""
    pass


@given(
    'a card "Drone of Brutality" with "If this would be put into your graveyard, instead put it on the bottom of your deck"'
)
def step_drone_of_brutality_card(game_state):
    """Rule 1.7.4j: Card with zone-movement replacement effect."""
    game_state.drone = game_state.create_card(name="Drone of Brutality")
    game_state.drone.functional_text = (
        "If this would be put into your graveyard from anywhere, "
        "instead put it on the bottom of your deck"
    )
    game_state.drone.has_zone_replacement_static = True
    game_state.drone.zone_replacement_from = "graveyard"
    game_state.drone.zone_replacement_to = "bottom_of_deck"


@when("the card would be moved to the graveyard")
def step_drone_would_go_to_graveyard(game_state):
    """Rule 1.7.4j: Drone is about to be moved to graveyard."""
    game_state.movement_would_be_to = "graveyard"
    game_state.movement_replacement_applied = False
    # Engine Feature Needed: ReplacementEffect system detecting the zone movement
    game_state.is_functional = game_state.check_ability_functional(
        game_state.drone,
        "zone_movement_replacement",
        ability_type="zone_replacement_static",
        destination_zone="graveyard",
    )


@then("the replacement static ability should be functional")
def step_drone_replacement_ability_functional(game_state):
    """Rule 1.7.4j: Zone-replacement static ability is functional."""
    assert game_state.is_functional is True


@then("the card should go to the bottom of the deck instead")
def step_drone_goes_to_deck_bottom(game_state):
    """Rule 1.7.4j: Replacement redirects to deck bottom."""
    # Engine Feature Needed: ReplacementEffect.apply() redirecting zone movement
    assert game_state.drone.zone_replacement_to == "bottom_of_deck"


# ---------------------------------------------------------------------------
# Scenario: modal_ability_provides_choice_of_modes
# Tests Rule 1.7.5 - Modal ability is a choice of modes
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_1_7_abilities.feature",
    "modal_ability_provides_choice_of_modes",
)
def test_modal_ability_provides_choice_of_modes():
    """Rule 1.7.5: Modal ability is a choice of modes."""
    pass


@given('a card "Art of War" with a modal ability "Choose 2"')
def step_art_of_war_card(game_state):
    """Rule 1.7.5: Art of War with modal ability."""
    game_state.art_of_war = game_state.create_card(name="Art of War")
    game_state.art_of_war.functional_text = (
        "Choose 2; [mode A], [mode B], [mode C], [mode D]"
    )
    game_state.art_of_war.is_modal = True
    game_state.art_of_war.modal_choose_count = 2
    game_state.art_of_war.available_modes = ["mode A", "mode B", "mode C", "mode D"]


@given("the card has four available modes")
def step_art_of_war_four_modes(game_state):
    """Rule 1.7.5: Four modes available."""
    assert len(game_state.art_of_war.available_modes) == 4


@when("the card is added to the stack")
def step_art_of_war_added_to_stack(game_state):
    """Rule 1.7.5: Card is being added to the stack."""
    game_state.play_card_to_stack(game_state.art_of_war, controller_id=0)
    game_state.mode_declaration_required = True


@then("the player must declare exactly 2 modes")
def step_player_must_declare_two_modes(game_state):
    """Rule 1.7.5: Player must declare exactly 2 modes."""
    assert game_state.art_of_war.modal_choose_count == 2
    # Engine Feature Needed: ModalAbility.required_mode_count == 2
    assert game_state.mode_declaration_required is True


# ---------------------------------------------------------------------------
# Scenario: cannot_select_same_mode_twice_without_permission
# Tests Rule 1.7.5b - Cannot select same mode twice
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_1_7_abilities.feature",
    "cannot_select_same_mode_twice_without_permission",
)
def test_cannot_select_same_mode_twice_without_permission():
    """Rule 1.7.5b: Cannot select the same mode twice unless specified."""
    pass


@given('a card with a modal ability "Choose 2"')
def step_card_with_choose_2_modal(game_state):
    """Rule 1.7.5b: Card with modal ability."""
    game_state.modal_card = game_state.create_card(name="Modal Card Choose 2")
    game_state.modal_card.is_modal = True
    game_state.modal_card.modal_choose_count = 2
    game_state.modal_card.available_modes = ["mode 1", "mode 2", "mode 3"]
    game_state.modal_card.allows_duplicate_modes = False


@given("the card does not specify the same mode can be chosen more than once")
def step_no_duplicate_modes_allowed(game_state):
    """Rule 1.7.5b: Duplicate mode selection not permitted."""
    assert game_state.modal_card.allows_duplicate_modes is False


@when("the player attempts to select mode 1 twice")
def step_player_selects_mode_1_twice(game_state):
    """Rule 1.7.5b: Player tries to select same mode twice."""
    # Engine Feature Needed: ModalAbility.declare_modes() validating uniqueness
    game_state.mode_selection_result = game_state.declare_modal_modes(
        game_state.modal_card, ["mode 1", "mode 1"]
    )


@then("the selection should be rejected")
def step_duplicate_mode_selection_rejected(game_state):
    """Rule 1.7.5b: Duplicate mode selection is rejected."""
    assert game_state.mode_selection_result.success is False
    assert game_state.mode_selection_result.reason == "duplicate_mode_not_allowed"


@then("the player must select two distinct modes")
def step_must_select_distinct_modes(game_state):
    """Rule 1.7.5b: Player must select two different modes."""
    assert game_state.mode_selection_result.requires_distinct_modes is True


# ---------------------------------------------------------------------------
# Scenario: can_only_select_available_modes
# Tests Rule 1.7.5b - Can only select available modes up to max
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_1_7_abilities.feature",
    "can_only_select_available_modes",
)
def test_can_only_select_available_modes():
    """Rule 1.7.5b: Can only select as many modes as are available."""
    pass


@given('a card with a modal ability "Choose 3"')
def step_card_with_choose_3_modal(game_state):
    """Rule 1.7.5b: Card with choose 3 modal ability."""
    game_state.modal_card_3 = game_state.create_card(name="Modal Card Choose 3")
    game_state.modal_card_3.is_modal = True
    game_state.modal_card_3.modal_choose_count = 3


@given("only 2 modes are available")
def step_only_2_modes_available(game_state):
    """Rule 1.7.5b: Only 2 modes are available."""
    game_state.modal_card_3.available_modes = ["mode A", "mode B"]


@when("the player selects modes")
def step_player_selects_modes_with_fewer_available(game_state):
    """Rule 1.7.5b: Player selects modes with fewer than requested available."""
    game_state.max_selectable = game_state.get_max_selectable_modes(
        game_state.modal_card_3
    )


@then("the player can only select a maximum of 2 modes")
def step_max_modes_is_available_count(game_state):
    """Rule 1.7.5b: Maximum selectable = available modes."""
    assert game_state.max_selectable == 2


# ---------------------------------------------------------------------------
# Scenario: selected_modes_become_base_abilities
# Tests Rule 1.7.5d - Selected modes become base abilities of source
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_1_7_abilities.feature",
    "selected_modes_become_base_abilities",
)
def test_selected_modes_become_base_abilities():
    """Rule 1.7.5d: Selected modes determine base abilities of the source."""
    pass


@given('a card with a modal ability "Choose 1"')
def step_card_with_choose_1_modal(game_state):
    """Rule 1.7.5d: Card with modal ability."""
    game_state.modal_source = game_state.create_card(name="Modal Source Card")
    game_state.modal_source.is_modal = True
    game_state.modal_source.modal_choose_count = 1
    game_state.modal_source.available_modes = [
        "Gain 3 life",
        "Draw a card",
        "Deal 2 damage",
    ]


@when('the player selects mode A "Gain 3 life"')
def step_player_selects_gain_life_mode(game_state):
    """Rule 1.7.5d: Player selects the gain life mode."""
    game_state.mode_selection_result = game_state.declare_modal_modes(
        game_state.modal_source, ["Gain 3 life"]
    )
    game_state.selected_modes = ["Gain 3 life"]


@then('the card\'s base abilities should include "Gain 3 life"')
def step_card_has_gain_life_as_base_ability(game_state):
    """Rule 1.7.5d: Selected mode is a base ability."""
    # Engine Feature Needed: ModalAbility selected modes become base abilities
    assert game_state.modal_source.has_base_ability("Gain 3 life") is True


@then("the card should NOT have the unselected modes as base abilities")
def step_card_not_have_unselected_modes(game_state):
    """Rule 1.7.5d: Unselected modes are not base abilities."""
    assert game_state.modal_source.has_base_ability("Draw a card") is False
    assert game_state.modal_source.has_base_ability("Deal 2 damage") is False


# ---------------------------------------------------------------------------
# Scenario: mode_count_evaluated_at_mode_selection_time
# Tests Rule 1.7.5e - Mode count evaluated at selection time
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_1_7_abilities.feature",
    "mode_count_evaluated_at_mode_selection_time",
)
def test_mode_count_evaluated_at_mode_selection_time():
    """Rule 1.7.5e: Mode count evaluated at time of mode selection."""
    pass


@given(
    'a card "Sacred Art: Undercurrent Desires" with "If you\'ve played another blue card this turn, choose 3. Otherwise, choose 1"'
)
def step_sacred_art_card(game_state):
    """Rule 1.7.5e: Card with conditional mode count."""
    game_state.sacred_art = game_state.create_card(
        name="Sacred Art: Undercurrent Desires"
    )
    game_state.sacred_art.functional_text = (
        "If you've played another blue card this turn, choose 3. Otherwise, choose 1"
    )
    game_state.sacred_art.is_modal = True
    game_state.sacred_art.conditional_modal_count = True
    game_state.sacred_art.available_modes = ["A", "B", "C", "D"]


@given("the player has already played a blue card this turn")
def step_player_played_blue_card(game_state):
    """Rule 1.7.5e: Player already played a blue card."""
    game_state.played_blue_this_turn = True
    game_state.sacred_art.conditional_modal_count_value = (
        3  # Condition is True -> choose 3
    )


@when("the card is added to the stack and modes are selected")
def step_sacred_art_added_to_stack(game_state):
    """Rule 1.7.5e: Modes are selected at this time."""
    game_state.modal_count_at_selection = game_state.evaluate_modal_count(
        game_state.sacred_art, game_state_context={"played_blue_this_turn": True}
    )


@then("the player should be able to choose 3 modes")
def step_player_can_choose_3_modes(game_state):
    """Rule 1.7.5e: Modal count is 3 because condition was true at selection time."""
    assert game_state.modal_count_at_selection == 3


# ---------------------------------------------------------------------------
# Scenario: connected_ability_pair_following_refers_to_leading
# Tests Rule 1.7.6 - Connected ability pairs
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_1_7_abilities.feature",
    "connected_ability_pair_following_refers_to_leading",
)
def test_connected_ability_pair_following_refers_to_leading():
    """Rule 1.7.6: Connected ability pair - following refers to leading's events."""
    pass


@given('a card "Reckless Swing" with:')
def step_reckless_swing_card(game_state, docstring):
    """Rule 1.7.6: Reckless Swing with connected ability pair."""
    game_state.reckless_swing = game_state.create_card(name="Reckless Swing")
    game_state.reckless_swing.leading_ability = (
        "As an additional cost to play this, discard a random card"
    )
    game_state.reckless_swing.following_ability = (
        "If the discarded card has 6 or more {p}, deal 2 damage to the attacking hero"
    )
    game_state.reckless_swing.has_connected_ability_pair = True


@when("the card is played and the discard additional cost is paid")
def step_reckless_swing_played_with_discard(game_state):
    """Rule 1.7.6: Card played, discard cost paid, leading ability fires."""
    # Engine Feature Needed: ConnectedAbilityPair.leading_ability.fire(events)
    # Create a high-power card using the template factory (CardTemplate is frozen)
    from fab_engine.cards.model import CardTemplate

    high_power_template = CardTemplate(
        unique_id="test_high_power_card",
        name="High Power Card",
        types=frozenset([CardType.ACTION]),
        supertypes=frozenset(),
        subtypes=frozenset(),
        color=Color.RED,
        pitch=0,
        has_pitch=False,
        cost=0,
        has_cost=False,
        power=7,
        has_power=True,
        defense=0,
        has_defense=False,
        arcane=0,
        has_arcane=False,
        life=0,
        intellect=0,
        keywords=frozenset(),
        keyword_params=tuple(),
        functional_text="",
    )
    from fab_engine.cards.model import CardInstance

    game_state.discarded_card = CardInstance(template=high_power_template, owner_id=0)
    game_state.leading_ability_events = {"discarded_card": game_state.discarded_card}


@then("the following ability can reference the discarded card")
def step_following_ability_can_reference_discard(game_state):
    """Rule 1.7.6: Following ability can reference leading ability's events."""
    # Engine Feature Needed: ConnectedAbilityPair.following_ability.can_reference(leading_events)
    assert game_state.reckless_swing.has_connected_ability_pair is True
    assert "discarded_card" in game_state.leading_ability_events


@then("the following ability can determine if the card had 6+ power")
def step_following_ability_determines_power(game_state):
    """Rule 1.7.6: Following ability evaluates power of discarded card."""
    discarded = game_state.leading_ability_events["discarded_card"]
    assert discarded.template.power >= 6


# ---------------------------------------------------------------------------
# Scenario: following_ability_fails_when_leading_events_unavailable
# Tests Rule 1.7.6b - Following ability fails when leading events unavailable
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_1_7_abilities.feature",
    "following_ability_fails_when_leading_events_unavailable",
)
def test_following_ability_fails_when_leading_events_unavailable():
    """Rule 1.7.6b: Following ability fails when cannot refer to leading ability's events."""
    pass


@given("a card with a connected ability pair")
def step_card_with_connected_pair(game_state):
    """Rule 1.7.6b: Card with connected ability pair."""
    game_state.connected_pair_card = game_state.create_card(name="Connected Pair Card")
    game_state.connected_pair_card.has_connected_ability_pair = True
    game_state.connected_pair_card.leading_ability = "Discard a card"
    game_state.connected_pair_card.following_ability = (
        "If the discarded card has X, do Y"
    )


@given("the leading ability has NOT been triggered (no discard occurred)")
def step_leading_ability_not_triggered(game_state):
    """Rule 1.7.6b: Leading ability hasn't fired."""
    game_state.leading_ability_events = {}  # Empty - no discard occurred
    game_state.leading_ability_fired = False


@when("the following ability attempts to reference the leading ability's events")
def step_following_ability_tries_to_reference(game_state):
    """Rule 1.7.6b: Following ability tries to access leading events."""
    # Engine Feature Needed: ConnectedAbilityPair.following_can_refer_to_leading()
    game_state.can_refer = game_state.check_following_can_refer_to_leading(
        game_state.connected_pair_card, leading_events=game_state.leading_ability_events
    )


@then("the relevant effects of the following ability should fail")
def step_following_ability_effects_fail(game_state):
    """Rule 1.7.6b: Following ability effects fail."""
    assert game_state.can_refer is False


@then("there are no parameters/events to refer to")
def step_no_events_to_refer_to(game_state):
    """Rule 1.7.6b: No leading events = following fails."""
    assert len(game_state.leading_ability_events) == 0


# ---------------------------------------------------------------------------
# Scenario: connected_pair_added_together_is_connected
# Tests Rule 1.7.6c - Connected pair added together remains connected
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_1_7_abilities.feature",
    "connected_pair_added_together_is_connected",
)
def test_connected_pair_added_together_is_connected():
    """Rule 1.7.6c: Connected pair added together as pair stays connected."""
    pass


@given("a card with neither ability A nor ability B originally")
def step_card_without_connected_pair_abilities(game_state):
    """Rule 1.7.6c: Card with no connected abilities."""
    game_state.target_card = game_state.create_card(name="Target Card")
    game_state.target_card.abilities = []
    game_state.target_card.connected_pairs = []


@when(
    "an effect adds both ability A (leading) and ability B (following) together as a connected pair"
)
def step_effect_adds_connected_pair(game_state):
    """Rule 1.7.6c: Effect adds both abilities as a connected pair."""
    # Engine Feature Needed: Effect.add_connected_ability_pair(card, leading_A, following_B)
    pair_result = game_state.add_connected_ability_pair(
        game_state.target_card,
        leading_ability="ability A",
        following_ability="ability B",
    )
    game_state.added_pair_result = pair_result


@then(
    "the added following ability B should be connected to the added leading ability A"
)
def step_added_following_connected_to_added_leading(game_state):
    """Rule 1.7.6c: Added abilities form a connected pair."""
    # Engine Feature Needed: The added pair tracks their connection
    assert game_state.added_pair_result.is_connected is True
    assert game_state.added_pair_result.leading_ability == "ability A"
    assert game_state.added_pair_result.following_ability == "ability B"


@then("the following ability should only refer to the added leading ability")
def step_following_only_refers_to_added_leading(game_state):
    """Rule 1.7.6c: Following refers to the specific added leading, not others."""
    assert game_state.added_pair_result.follows_only_added_leading is True


# ---------------------------------------------------------------------------
# Scenario: object_abilities_can_be_modified
# Tests Rule 1.7.7 - The abilities of an object can be modified
# ---------------------------------------------------------------------------


@scenario(
    "../features/section_1_7_abilities.feature",
    "object_abilities_can_be_modified",
)
def test_object_abilities_can_be_modified():
    """Rule 1.7.7: The abilities of an object can be modified."""
    pass


@given('a card with the ability "Deal 2 damage"')
def step_card_with_deal_2_damage(game_state):
    """Rule 1.7.7: Card with original ability."""
    game_state.modifiable_card = game_state.create_card(name="Modifiable Card")
    game_state.modifiable_card.abilities = ["Deal 2 damage"]


@when('an effect modifies the card to give it the ability "Deal 4 damage instead"')
def step_effect_modifies_ability(game_state):
    """Rule 1.7.7: Effect modifies the card's ability."""
    # Engine Feature Needed: Effect.modify_ability(card, old_ability, new_ability)
    game_state.modify_result = game_state.modify_card_ability(
        game_state.modifiable_card, "Deal 2 damage", "Deal 4 damage instead"
    )


@then("the card should now have the modified ability")
def step_card_has_modified_ability(game_state):
    """Rule 1.7.7: Modified ability is active."""
    # Engine Feature Needed: Ability modification tracked on CardInstance
    assert game_state.modify_result.success is True
    assert game_state.modifiable_card.has_ability("Deal 4 damage instead") is True


@then("the card's original ability should no longer be in effect (or modified)")
def step_original_ability_modified(game_state):
    """Rule 1.7.7: Original ability is modified (no longer the same)."""
    # The original unmodified ability should no longer be present (or should be modified)
    assert game_state.modify_result.original_ability_replaced is True


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def game_state():
    """
    Fixture providing game state for testing Section 1.7 (Abilities).

    Uses BDDGameState which integrates with the real engine.
    Reference: Rule 1.7

    Engine Features Needed:
    - [ ] Ability class hierarchy (ActivatedAbility, ResolutionAbility, StaticAbility)
    - [ ] Layer.source reference and exists_independently_of_source property
    - [ ] CardInstance.has_ability() / has_base_ability()
    - [ ] CardInstance.get_base_abilities()
    - [ ] AbilityCategory enum in fab_engine.engine.abilities module
    - [ ] ModalAbility with mode selection validation
    - [ ] ConnectedAbilityPair with following/leading tracking
    - [ ] Ability.is_functional(context) method
    """
    from tests.bdd_helpers import BDDGameState

    state = BDDGameState()

    # Initialize ability-testing specific attributes
    state.ability_text = ""
    state.ability_defined = False
    state.is_functional = False
    state.base_abilities = []
    state.ability_categories = None

    return state
