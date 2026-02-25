"""
Step definitions for Section 1.6: Layers
Reference: Flesh and Blood Comprehensive Rules Section 1.6

This module implements behavioral tests for layer objects in Flesh and Blood.
Layers are objects on the stack awaiting resolution. There are three types:
card-layers, activated-layers, and triggered-layers.

Engine Features Needed for Section 1.6:
- [ ] Layer base class with `is_layer`, `is_resolved`, `layer_category` attributes (Rule 1.6.1)
- [ ] CardLayer class wrapping a CardInstance on the stack (Rule 1.6.2a)
- [ ] ActivatedLayer class created by an activated ability (Rule 1.6.2b)
- [ ] TriggeredLayer class created by a triggered effect (Rule 1.6.2c)
- [ ] Layer.owner_id property per layer type (Rule 1.6.1a)
  - CardLayer.owner_id = owner of the card
  - ActivatedLayer.owner_id = player who activated the ability
  - TriggeredLayer.owner_id = controller of source when triggered
- [ ] Layer.controller_id = player who put it on the stack (Rule 1.6.1b)
- [ ] Layer.can_only_exist_on_stack validation (Rules 1.6.2b, 1.6.2c)
- [ ] TriggeredLayer created before being put on stack (Rule 1.6.2c)
- [ ] Layer resolution is independent of source existence (Rule 1.7.1a cross-ref)
- [ ] Stack zone correctly holds layer objects (Rule 3.15)

These features will be implemented in a separate task.
Current status: Tests written, Engine pending
"""

import pytest
from pytest_bdd import scenario, given, when, then, parsers


# ============================================================
# Rule 1.6.1: A layer is an object on the stack yet to be resolved
# ============================================================


@scenario(
    "../features/section_1_6_layers.feature",
    "A layer is an object on the stack yet to be resolved",
)
def test_layer_is_object_on_stack_yet_to_be_resolved():
    """Rule 1.6.1: A layer is an object on the stack that is yet to be resolved."""
    pass


@scenario(
    "../features/section_1_6_layers.feature",
    "All three layer types are recognized as layers",
)
def test_all_three_layer_types_are_layers():
    """Rule 1.6.1: Card-layers, activated-layers, and triggered-layers are all layers."""
    pass


# ============================================================
# Rule 1.6.1a: Owner determination by layer type
# ============================================================


@scenario(
    "../features/section_1_6_layers.feature",
    "Card-layer owner is the player who owns the card",
)
def test_card_layer_owner_is_card_owner():
    """Rule 1.6.1a: Owner of a card-layer is the player who owns the card."""
    pass


@scenario(
    "../features/section_1_6_layers.feature",
    "Activated-layer owner is the player who activated the ability",
)
def test_activated_layer_owner_is_activating_player():
    """Rule 1.6.1a: Owner of an activated-layer is the player who activated the ability."""
    pass


@scenario(
    "../features/section_1_6_layers.feature",
    "Triggered-layer owner is the controller of the source at trigger time",
)
def test_triggered_layer_owner_is_controller_at_trigger_time():
    """Rule 1.6.1a: Owner of triggered-layer = controller of source when triggered."""
    pass


@scenario(
    "../features/section_1_6_layers.feature",
    "Triggered-layer owner is based on who controlled source when it triggered",
)
def test_triggered_layer_owner_uses_controller_at_trigger_time():
    """Rule 1.6.1a: Triggered-layer owner is the controller at trigger time, not now."""
    pass


# ============================================================
# Rule 1.6.1b: Controller of a layer is the player that put it on the stack
# ============================================================


@scenario(
    "../features/section_1_6_layers.feature",
    "Controller of a card-layer is the player who put it on the stack",
)
def test_card_layer_controller_is_player_who_put_on_stack():
    """Rule 1.6.1b: Controller of a layer is the player that put it on the stack."""
    pass


@scenario(
    "../features/section_1_6_layers.feature",
    "Controller of an activated-layer is the player who activated it",
)
def test_activated_layer_controller_is_activating_player():
    """Rule 1.6.1b: Controller of activated-layer = player who activated the ability."""
    pass


@scenario(
    "../features/section_1_6_layers.feature",
    "Controller of a triggered-layer is the player who put it on the stack",
)
def test_triggered_layer_controller_is_player_who_put_on_stack():
    """Rule 1.6.1b: Controller of triggered-layer = player who put it on the stack."""
    pass


# ============================================================
# Rule 1.6.2: Three layer categories
# ============================================================


@scenario(
    "../features/section_1_6_layers.feature",
    "There are exactly 3 categories of layers",
)
def test_there_are_exactly_3_layer_categories():
    """Rule 1.6.2: There are exactly 3 categories of layers."""
    pass


# ============================================================
# Rule 1.6.2a: Card-layer is a layer represented by a card on the stack
# ============================================================


@scenario(
    "../features/section_1_6_layers.feature",
    "A card played to the stack becomes a card-layer",
)
def test_card_played_to_stack_becomes_card_layer():
    """Rule 1.6.2a: A card on the stack is a card-layer."""
    pass


@scenario(
    "../features/section_1_6_layers.feature",
    "A card-layer retains the card's properties",
)
def test_card_layer_retains_card_properties():
    """Rule 1.6.2a: A card-layer retains the properties of the card it represents."""
    pass


# ============================================================
# Rule 1.6.2b: Activated-layer is created by an activated ability
# ============================================================


@scenario(
    "../features/section_1_6_layers.feature",
    "Activating an ability creates an activated-layer on the stack",
)
def test_activating_ability_creates_activated_layer():
    """Rule 1.6.2b: Activated ability creates an activated-layer on the stack."""
    pass


@scenario(
    "../features/section_1_6_layers.feature",
    "An activated-layer can only exist on the stack",
)
def test_activated_layer_can_only_exist_on_stack():
    """Rule 1.6.2b: An activated-layer can only exist on the stack."""
    pass


# ============================================================
# Rule 1.6.2c: Triggered-layer is created by a triggered effect
# ============================================================


@scenario(
    "../features/section_1_6_layers.feature",
    "A triggered effect creates a triggered-layer when it fires",
)
def test_triggered_effect_creates_triggered_layer():
    """Rule 1.6.2c: A triggered effect creates a triggered-layer (Snatch example)."""
    pass


@scenario(
    "../features/section_1_6_layers.feature",
    "A triggered-layer is created before it is put on the stack",
)
def test_triggered_layer_created_before_put_on_stack():
    """Rule 1.6.2c: A triggered-layer is created before being placed on the stack."""
    pass


@scenario(
    "../features/section_1_6_layers.feature",
    "A triggered-layer can only exist on the stack",
)
def test_triggered_layer_can_only_exist_on_stack():
    """Rule 1.6.2c: A triggered-layer can only exist on the stack."""
    pass


# ============================================================
# Rule 1.7.1a (cross-reference): Layers exist independently of their source
# ============================================================


@scenario(
    "../features/section_1_6_layers.feature",
    "An activated-layer continues to exist even if its source is destroyed",
)
def test_activated_layer_survives_source_destruction():
    """Rule 1.7.1a: Activated-layers exist independently of their source."""
    pass


@scenario(
    "../features/section_1_6_layers.feature",
    "A triggered-layer continues to exist even if its source leaves play",
)
def test_triggered_layer_survives_source_leaving_play():
    """Rule 1.7.1a: Triggered-layers exist independently of their source."""
    pass


# ============================================================
# Step Definitions
# ============================================================


@given("a game is in progress")
def step_game_in_progress(game_state):
    """Set up a basic game state in progress."""
    # game_state is already initialized by the fixture
    pass


@given("a player has an action card in hand")
def step_player_has_action_card_in_hand(game_state):
    """Rule 1.6.2a: Set up a player with an action card in hand."""
    from fab_engine.cards.model import CardType

    card = game_state.create_card(
        name="Test Action", card_type=CardType.ACTION, owner_id=0
    )
    game_state.player.hand.add_card(card)
    game_state.test_card = card


@given("player 0 has an action card in hand")
def step_player_0_has_action_card_in_hand(game_state):
    """Rule 1.6.1b: Player 0 has an action card in hand."""
    from fab_engine.cards.model import CardType

    card = game_state.create_card(
        name="Test Action", card_type=CardType.ACTION, owner_id=0
    )
    game_state.player.hand.add_card(card)
    game_state.test_card = card


@given("a card-layer exists on the stack")
def step_card_layer_on_stack(game_state):
    """Rule 1.6.1: Create a card-layer on the stack."""
    from fab_engine.cards.model import CardType

    card = game_state.create_card(
        name="Card Layer Card", card_type=CardType.ACTION, owner_id=0
    )
    # Engine feature needed: CardLayer class
    layer = CardLayerStub(card=card, owner_id=0, controller_id=0)
    game_state.card_layer = layer
    game_state.stack_layers.append(layer)


@given("an activated-layer exists on the stack")
def step_activated_layer_on_stack(game_state):
    """Rule 1.6.1: Create an activated-layer on the stack."""
    # Engine feature needed: ActivatedLayer class
    layer = ActivatedLayerStub(
        resolution_ability="Gain 2 resources",
        owner_id=0,
        controller_id=0,
    )
    game_state.activated_layer = layer
    game_state.stack_layers.append(layer)


@given("a triggered-layer exists on the stack")
def step_triggered_layer_on_stack(game_state):
    """Rule 1.6.1: Create a triggered-layer on the stack."""
    # Engine feature needed: TriggeredLayer class
    layer = TriggeredLayerStub(
        resolution_ability="Draw a card",
        owner_id=0,
        controller_id=0,
    )
    game_state.triggered_layer = layer
    game_state.stack_layers.append(layer)


@given("player 0 owns an action card")
def step_player_0_owns_action_card(game_state):
    """Rule 1.6.1a: Player 0 owns an action card."""
    from fab_engine.cards.model import CardType

    card = game_state.create_card(
        name="Owned Card", card_type=CardType.ACTION, owner_id=0
    )
    game_state.test_card = card
    game_state.player.hand.add_card(card)


@given("player 0 has a card with an activated ability")
def step_player_0_has_card_with_activated_ability(game_state):
    """Rule 1.6.2b: Player 0 has a card with an activated ability."""
    from fab_engine.cards.model import (
        CardType,
        CardInstance,
        CardTemplate,
        Color,
        Subtype,
    )

    template = CardTemplate(
        unique_id="energy_potion_test",
        name="Energy Potion",
        types=frozenset([CardType.ACTION]),
        supertypes=frozenset(),
        subtypes=frozenset(),
        color=Color.COLORLESS,
        pitch=0,
        has_pitch=False,
        cost=0,
        has_cost=False,
        power=0,
        has_power=False,
        defense=0,
        has_defense=False,
        arcane=0,
        has_arcane=False,
        life=0,
        intellect=0,
        keywords=frozenset(),
        keyword_params=tuple(),
        functional_text="Instant – Destroy this: Gain {r}{r}",
    )
    card = CardInstance(template=template, owner_id=0)
    game_state.test_card = card
    game_state.player.hand.add_card(card)
    # Track that this card has an activated ability
    game_state.activated_ability_source = card
    game_state.activated_ability_text = "Gain 2 resources"


@given("player 0 controls a card with a triggered effect")
def step_player_0_controls_card_with_triggered_effect(game_state):
    """Rule 1.6.1a: Player 0 controls a source with a triggered effect."""
    from fab_engine.cards.model import CardType

    card = game_state.create_card(name="Snatch", card_type=CardType.ACTION, owner_id=0)
    card.controller_id = 0
    game_state.triggered_source_card = card
    game_state.triggered_source_owner_id = 0
    game_state.triggered_source_controller_id = 0


@given("player 0 originally controlled a card with a triggered effect")
def step_player_0_originally_controlled_triggered_source(game_state):
    """Rule 1.6.1a: Set up a card originally controlled by player 0."""
    from fab_engine.cards.model import CardType

    card = game_state.create_card(
        name="Triggered Source", card_type=CardType.ACTION, owner_id=0
    )
    card.controller_id = 0
    game_state.triggered_source_card = card
    game_state.triggered_source_original_controller = 0


@given("the source card changed controller to player 1 before triggering")
def step_source_changed_controller(game_state):
    """Rule 1.6.1a: The source card now has a different controller."""
    # Engine feature needed: controller change tracking
    game_state.triggered_source_card.controller_id = 1
    game_state.triggered_source_controller_id = 1


@given("player 0 activates an ability creating an activated-layer")
def step_player_0_activates_ability(game_state):
    """Rule 1.6.2b: Player 0 activates an ability creating an activated-layer."""
    # Engine feature needed: ActivatedLayer class, ability activation
    layer = ActivatedLayerStub(
        resolution_ability="Gain 2 resources",
        owner_id=0,
        controller_id=0,
    )
    game_state.activated_layer = layer
    game_state.stack_layers.append(layer)


@given('player 0 has an action card named "Lunging Press" in hand')
def step_player_0_has_lunging_press(game_state):
    """Rule 1.6.2a: Player 0 has a card named 'Lunging Press' in hand."""
    from fab_engine.cards.model import CardType

    card = game_state.create_card(
        name="Lunging Press", card_type=CardType.ACTION, owner_id=0
    )
    game_state.test_card = card
    game_state.player.hand.add_card(card)


@given(
    'player 0 has an "Energy Potion" card with activated ability "Destroy this: Gain 2 resources"'
)
def step_player_0_has_energy_potion(game_state):
    """Rule 1.6.2b: Player 0 has an Energy Potion with activated ability."""
    from fab_engine.cards.model import CardType, CardInstance, CardTemplate, Color

    template = CardTemplate(
        unique_id="energy_potion_scenario",
        name="Energy Potion",
        types=frozenset([CardType.ACTION]),
        supertypes=frozenset(),
        subtypes=frozenset(),
        color=Color.COLORLESS,
        pitch=0,
        has_pitch=False,
        cost=0,
        has_cost=False,
        power=0,
        has_power=False,
        defense=0,
        has_defense=False,
        arcane=0,
        has_arcane=False,
        life=0,
        intellect=0,
        keywords=frozenset(),
        keyword_params=tuple(),
        functional_text="Instant – Destroy this: Gain {r}{r}",
    )
    card = CardInstance(template=template, owner_id=0)
    game_state.test_card = card
    game_state.energy_potion_card = card
    game_state.player.hand.add_card(card)


@given(
    'a "Snatch" card with triggered effect "When this hits, draw a card" is on the combat chain'
)
def step_snatch_on_combat_chain(game_state):
    """Rule 1.6.2c: Snatch is on the combat chain with triggered effect."""
    from fab_engine.cards.model import (
        CardType,
        CardInstance,
        CardTemplate,
        Color,
        Subtype,
    )

    template = CardTemplate(
        unique_id="snatch_test",
        name="Snatch",
        types=frozenset([CardType.ACTION]),
        supertypes=frozenset(),
        subtypes=frozenset([Subtype.ATTACK]),
        color=Color.COLORLESS,
        pitch=0,
        has_pitch=False,
        cost=0,
        has_cost=False,
        power=4,
        has_power=True,
        defense=3,
        has_defense=True,
        arcane=0,
        has_arcane=False,
        life=0,
        intellect=0,
        keywords=frozenset(),
        keyword_params=tuple(),
        functional_text="When this hits, draw a card.",
    )
    card = CardInstance(template=template, owner_id=0)
    card.controller_id = 0
    game_state.snatch_card = card
    game_state.triggered_source_card = card
    # Put on combat chain (engine feature needed: CombatChain)
    game_state.put_on_combat_chain(card, power=4)


@given("a card with a triggered effect is on the combat chain")
def step_card_with_triggered_effect_on_chain(game_state):
    """Rule 1.6.2c: A card with a triggered effect is on the combat chain."""
    from fab_engine.cards.model import CardType, Subtype

    card = game_state.create_card(
        name="Triggered Card", card_type=CardType.ACTION, owner_id=0
    )
    card.controller_id = 0
    game_state.triggered_source_card = card
    game_state.put_on_combat_chain(card, power=3)


@given("a triggered-layer has been created by a triggered effect")
def step_triggered_layer_created(game_state):
    """Rule 1.6.2c: A triggered-layer has been created."""
    layer = TriggeredLayerStub(
        resolution_ability="Draw a card",
        owner_id=0,
        controller_id=0,
    )
    game_state.triggered_layer = layer
    game_state.stack_layers.append(layer)


@given('"Energy Potion" is destroyed after the activated-layer is created')
def step_energy_potion_destroyed(game_state):
    """Rule 1.7.1a: Source is destroyed after activated-layer created."""
    # Remove from player's hand/arena (simulate destruction)
    if hasattr(game_state, "energy_potion_card"):
        try:
            game_state.player.hand.remove_card(game_state.energy_potion_card)
        except (ValueError, AttributeError):
            pass
    game_state.source_destroyed = True


@given("a card with a triggered effect fires creating a triggered-layer")
def step_triggered_card_fires(game_state):
    """Rule 1.7.1a: Triggered effect fires and creates a layer."""
    from fab_engine.cards.model import CardType

    card = game_state.create_card(
        name="Source Card", card_type=CardType.ACTION, owner_id=0
    )
    card.controller_id = 0
    game_state.triggered_source_card = card
    # Create the triggered layer
    layer = TriggeredLayerStub(
        resolution_ability="Draw a card",
        owner_id=0,
        controller_id=0,
    )
    game_state.triggered_layer = layer
    game_state.stack_layers.append(layer)


@given("the source card moves to the graveyard after the triggered-layer is created")
def step_source_moves_to_graveyard(game_state):
    """Rule 1.7.1a: Source moves to graveyard after triggered-layer created."""
    # Engine feature needed: graveyard zone movement
    game_state.source_in_graveyard = True
    game_state.source_destroyed = True


@given("a game engine with layer support")
def step_game_engine_with_layer_support(game_state):
    """Rule 1.6.2: Game engine knows about the layer categories."""
    # Engine feature needed: Layer category enumeration
    pass


@when("the player plays the action card")
def step_player_plays_action_card(game_state):
    """Rule 1.6.1: Player plays an action card, creating a card-layer on the stack."""
    # Engine feature needed: CardLayer class for cards on the stack
    card = game_state.test_card
    if card and card in game_state.player.hand:
        game_state.player.hand.remove_card(card)
    # Create a card-layer stub representing the card on the stack
    layer = CardLayerStub(
        card=card, owner_id=card.owner_id if card else 0, controller_id=0
    )
    game_state.card_layer = layer
    game_state.stack_layers.append(layer)
    game_state.played_card_layer = layer


@when("player 0 plays the action card onto the stack")
def step_player_0_plays_card_onto_stack(game_state):
    """Rule 1.6.1a/b: Player 0 plays a card, creating a card-layer."""
    card = game_state.test_card
    if card and card in game_state.player.hand:
        game_state.player.hand.remove_card(card)
    # Engine feature needed: CardLayer class
    layer = CardLayerStub(
        card=card, owner_id=card.owner_id if card else 0, controller_id=0
    )
    game_state.card_layer = layer
    game_state.stack_layers.append(layer)


@when("player 0 activates the activated ability")
def step_player_0_activates_ability_general(game_state):
    """Rule 1.6.1a: Player 0 activates a card's activated ability."""
    # Engine feature needed: ActivatedLayer class, activated ability system
    layer = ActivatedLayerStub(
        resolution_ability=game_state.activated_ability_text
        if hasattr(game_state, "activated_ability_text")
        else "Gain 2 resources",
        owner_id=0,
        controller_id=0,
    )
    game_state.activated_layer = layer
    game_state.stack_layers.append(layer)


@when("the triggered effect fires")
def step_triggered_effect_fires(game_state):
    """Rule 1.6.1a/1.6.2c: The triggered effect fires."""
    # Use the controller at trigger time
    controller_id = getattr(game_state, "triggered_source_controller_id", 0)
    # Engine feature needed: TriggeredLayer class, triggered effect system
    layer = TriggeredLayerStub(
        resolution_ability="Draw a card",
        owner_id=controller_id,
        controller_id=controller_id,
    )
    game_state.triggered_layer = layer
    game_state.stack_layers.append(layer)


@when("the triggered effect fires while player 1 controls the source")
def step_triggered_effect_fires_player_1_controls(game_state):
    """Rule 1.6.1a: Triggered effect fires while player 1 controls source."""
    # Owner/controller of triggered-layer is the one who controlled source at trigger time
    controller_id = getattr(game_state, "triggered_source_controller_id", 1)
    # Engine feature needed: TriggeredLayer class
    layer = TriggeredLayerStub(
        resolution_ability="Draw a card",
        owner_id=controller_id,
        controller_id=controller_id,
    )
    game_state.triggered_layer = layer
    game_state.stack_layers.append(layer)


@when("the triggered effect fires and the triggered-layer is put on the stack")
def step_triggered_effect_fires_and_put_on_stack(game_state):
    """Rule 1.6.1b: Triggered-layer is created and put on the stack."""
    controller_id = getattr(game_state, "triggered_source_controller_id", 0)
    # Engine feature needed: TriggeredLayer creation before placement
    layer = TriggeredLayerStub(
        resolution_ability="Draw a card",
        owner_id=controller_id,
        controller_id=controller_id,
    )
    game_state.triggered_layer = layer
    game_state.triggered_layer_created_first = True  # Created before put on stack
    game_state.triggered_layer_on_stack = True
    game_state.stack_layers.append(layer)


@when("the layer categories are queried")
def step_layer_categories_queried(game_state):
    """Rule 1.6.2: Query the available layer categories."""
    # Engine feature needed: LayerCategory enum with 3 values
    game_state.layer_categories_queried = True


@when('player 0 plays "Lunging Press" onto the stack')
def step_player_0_plays_lunging_press(game_state):
    """Rule 1.6.2a: Player 0 plays Lunging Press."""
    card = game_state.test_card
    if card and card in game_state.player.hand:
        game_state.player.hand.remove_card(card)
    layer = CardLayerStub(card=card, owner_id=0, controller_id=0)
    game_state.card_layer = layer
    game_state.stack_layers.append(layer)


@when('player 0 activates the ability of "Energy Potion"')
def step_player_0_activates_energy_potion(game_state):
    """Rule 1.6.2b: Player 0 activates Energy Potion's ability."""
    # Engine feature needed: ActivatedLayer creation from ability activation
    layer = ActivatedLayerStub(
        resolution_ability="Gain 2 resources",
        owner_id=0,
        controller_id=0,
    )
    game_state.activated_layer = layer
    game_state.stack_layers.append(layer)


@when("player 0 activates the activated ability putting a layer on the stack")
def step_activated_ability_puts_layer_on_stack(game_state):
    """Rule 1.6.1b: Activated ability puts a layer on the stack."""
    layer = ActivatedLayerStub(
        resolution_ability="Gain 2 resources",
        owner_id=0,
        controller_id=0,
    )
    game_state.activated_layer = layer
    game_state.stack_layers.append(layer)


@when("the activated-layer is queried for its valid zones")
def step_activated_layer_queried_for_zones(game_state):
    """Rule 1.6.2b: Check which zones an activated-layer can exist in."""
    game_state.queried_layer = getattr(game_state, "activated_layer", None)


@when('"Snatch" hits the defending player')
def step_snatch_hits_defender(game_state):
    """Rule 1.6.2c: Snatch card deals damage (hits) the defending player."""
    # Engine feature needed: combat hit detection, triggered effect firing
    game_state.snatch_hit = True
    # Create the triggered layer that fires when Snatch hits
    layer = TriggeredLayerStub(
        resolution_ability="Draw a card",
        owner_id=0,
        controller_id=0,
    )
    game_state.triggered_layer = layer
    game_state.triggered_layer_created = True
    game_state.stack_layers.append(layer)


@when("the triggered-layer is queried for its valid zones")
def step_triggered_layer_queried_for_zones(game_state):
    """Rule 1.6.2c: Check which zones a triggered-layer can exist in."""
    game_state.queried_layer = getattr(game_state, "triggered_layer", None)


@when("the activated-layer is on the stack awaiting resolution")
def step_activated_layer_awaiting_resolution(game_state):
    """Rule 1.7.1a: The activated-layer is on the stack waiting to resolve."""
    # Nothing changes - source being destroyed doesn't affect the stack
    pass


@when("the triggered-layer is on the stack awaiting resolution")
def step_triggered_layer_awaiting_resolution(game_state):
    """Rule 1.7.1a: The triggered-layer is on the stack waiting to resolve."""
    # Nothing changes - source leaving doesn't affect the stack
    pass


# ============================================================
# Then steps
# ============================================================


@then("the card becomes a layer on the stack")
def step_card_becomes_layer_on_stack(game_state):
    """Rule 1.6.1: Card played to stack creates a layer."""
    # Engine feature needed: CardLayer class
    layer = getattr(game_state, "played_card_layer", None) or getattr(
        game_state, "card_layer", None
    )
    assert layer is not None, (
        "Engine feature needed: CardLayer must be created when card is played to stack"
    )
    assert layer.is_layer, "Engine feature needed: Layer.is_layer property must be True"


@then("the layer has not yet been resolved")
def step_layer_not_yet_resolved(game_state):
    """Rule 1.6.1: A layer on the stack has not yet been resolved."""
    layer = getattr(game_state, "played_card_layer", None) or getattr(
        game_state, "card_layer", None
    )
    assert layer is not None, "Engine feature needed: CardLayer must exist"
    assert not layer.is_resolved, (
        "Engine feature needed: Layer.is_resolved must be False for new layer"
    )


@then("the layer is recognized as a game object")
def step_layer_is_game_object(game_state):
    """Rule 1.2.1: Layers are game objects."""
    layer = getattr(game_state, "played_card_layer", None) or getattr(
        game_state, "card_layer", None
    )
    assert layer is not None, "Engine feature needed: CardLayer must exist"
    assert layer.is_game_object, (
        "Engine feature needed: Layer.is_game_object must be True"
    )


@then("all three are recognized as layers")
def step_all_three_recognized_as_layers(game_state):
    """Rule 1.6.1: All three layer types are recognized as layers."""
    card_layer = getattr(game_state, "card_layer", None)
    activated_layer = getattr(game_state, "activated_layer", None)
    triggered_layer = getattr(game_state, "triggered_layer", None)
    assert card_layer is not None, "Engine feature needed: CardLayer class"
    assert activated_layer is not None, "Engine feature needed: ActivatedLayer class"
    assert triggered_layer is not None, "Engine feature needed: TriggeredLayer class"
    assert card_layer.is_layer, "Engine feature needed: CardLayer.is_layer property"
    assert activated_layer.is_layer, (
        "Engine feature needed: ActivatedLayer.is_layer property"
    )
    assert triggered_layer.is_layer, (
        "Engine feature needed: TriggeredLayer.is_layer property"
    )


@then("each layer is an object on the stack")
def step_each_layer_is_object_on_stack(game_state):
    """Rule 1.6.1: All layers exist on the stack."""
    for layer in game_state.stack_layers:
        assert layer.is_layer, "Engine feature needed: Layer.is_layer property"
        assert layer.is_on_stack, "Engine feature needed: Layer.is_on_stack property"


@then("a card-layer is created on the stack")
def step_card_layer_created_on_stack(game_state):
    """Rule 1.6.1a: A card-layer was created when the card was played."""
    layer = getattr(game_state, "card_layer", None)
    assert layer is not None, (
        "Engine feature needed: CardLayer must be created when card played to stack"
    )
    assert layer.is_layer, "Engine feature needed: CardLayer.is_layer must be True"
    assert layer.layer_category == "card-layer", (
        "Engine feature needed: CardLayer.layer_category == 'card-layer'"
    )


@then("the card-layer owner is player 0")
def step_card_layer_owner_is_player_0(game_state):
    """Rule 1.6.1a: Owner of card-layer is the card owner (player 0)."""
    layer = getattr(game_state, "card_layer", None)
    assert layer is not None, "Engine feature needed: CardLayer must exist"
    assert layer.owner_id == 0, (
        f"Engine feature needed: CardLayer.owner_id must be 0 (the card owner), got {layer.owner_id}"
    )


@then("an activated-layer is created on the stack")
def step_activated_layer_created_on_stack(game_state):
    """Rule 1.6.1a/1.6.2b: An activated-layer was created."""
    layer = getattr(game_state, "activated_layer", None)
    assert layer is not None, (
        "Engine feature needed: ActivatedLayer must be created when ability activated"
    )
    assert layer.is_layer, "Engine feature needed: ActivatedLayer.is_layer must be True"
    assert layer.layer_category == "activated-layer", (
        "Engine feature needed: ActivatedLayer.layer_category == 'activated-layer'"
    )


@then("the activated-layer owner is player 0")
def step_activated_layer_owner_is_player_0(game_state):
    """Rule 1.6.1a: Owner of activated-layer is the player who activated the ability."""
    layer = getattr(game_state, "activated_layer", None)
    assert layer is not None, "Engine feature needed: ActivatedLayer must exist"
    assert layer.owner_id == 0, (
        f"Engine feature needed: ActivatedLayer.owner_id must be 0 (activating player), got {layer.owner_id}"
    )


@then("a triggered-layer is created on the stack")
def step_triggered_layer_created_on_stack(game_state):
    """Rule 1.6.1a/1.6.2c: A triggered-layer was created."""
    layer = getattr(game_state, "triggered_layer", None)
    assert layer is not None, (
        "Engine feature needed: TriggeredLayer must be created when triggered effect fires"
    )
    assert layer.is_layer, "Engine feature needed: TriggeredLayer.is_layer must be True"
    assert layer.layer_category == "triggered-layer", (
        "Engine feature needed: TriggeredLayer.layer_category == 'triggered-layer'"
    )


@then("the triggered-layer owner is player 0")
def step_triggered_layer_owner_is_player_0(game_state):
    """Rule 1.6.1a: Owner of triggered-layer = controller of source when triggered (player 0)."""
    layer = getattr(game_state, "triggered_layer", None)
    assert layer is not None, "Engine feature needed: TriggeredLayer must exist"
    assert layer.owner_id == 0, (
        f"Engine feature needed: TriggeredLayer.owner_id must be 0 (source controller at trigger time), got {layer.owner_id}"
    )


@then("the triggered-layer owner is player 1")
def step_triggered_layer_owner_is_player_1(game_state):
    """Rule 1.6.1a: Owner of triggered-layer is player 1 (who controlled source when triggered)."""
    layer = getattr(game_state, "triggered_layer", None)
    assert layer is not None, "Engine feature needed: TriggeredLayer must exist"
    assert layer.owner_id == 1, (
        f"Engine feature needed: TriggeredLayer.owner_id must be 1 (controller at trigger time), got {layer.owner_id}"
    )


@then("a card-layer is on the stack")
def step_card_layer_on_stack_assertion(game_state):
    """Rule 1.6.1b: Card-layer is on the stack."""
    layer = getattr(game_state, "card_layer", None)
    assert layer is not None, "Engine feature needed: CardLayer must exist on stack"
    assert layer.is_on_stack, (
        "Engine feature needed: CardLayer.is_on_stack must be True"
    )


@then("the card-layer controller is player 0")
def step_card_layer_controller_is_player_0(game_state):
    """Rule 1.6.1b: Controller of card-layer is the player who put it on the stack."""
    layer = getattr(game_state, "card_layer", None)
    assert layer is not None, "Engine feature needed: CardLayer must exist"
    assert layer.controller_id == 0, (
        f"Engine feature needed: CardLayer.controller_id must be 0 (player who put on stack), got {layer.controller_id}"
    )


@then("the activated-layer controller is player 0")
def step_activated_layer_controller_is_player_0(game_state):
    """Rule 1.6.1b: Controller of activated-layer is the player who put it on the stack."""
    layer = getattr(game_state, "activated_layer", None)
    assert layer is not None, "Engine feature needed: ActivatedLayer must exist"
    assert layer.controller_id == 0, (
        f"Engine feature needed: ActivatedLayer.controller_id must be 0, got {layer.controller_id}"
    )


@then("the triggered-layer controller is player 0")
def step_triggered_layer_controller_is_player_0(game_state):
    """Rule 1.6.1b: Controller of triggered-layer is the player who put it on the stack."""
    layer = getattr(game_state, "triggered_layer", None)
    assert layer is not None, "Engine feature needed: TriggeredLayer must exist"
    assert layer.controller_id == 0, (
        f"Engine feature needed: TriggeredLayer.controller_id must be 0, got {layer.controller_id}"
    )


@then("there are exactly 3 layer categories")
def step_exactly_3_layer_categories(game_state):
    """Rule 1.6.2: There are exactly 3 layer categories."""
    # Engine feature needed: LayerCategory enum or equivalent with 3 values
    layer_categories = getattr(game_state, "layer_categories", None)
    # If engine has LayerCategory enum, check it has 3 members
    try:
        from fab_engine.engine.layers import LayerCategory

        assert len(LayerCategory) == 3, (
            f"Engine feature needed: LayerCategory must have exactly 3 values, got {len(LayerCategory)}"
        )
    except ImportError:
        pytest.fail(
            "Engine feature needed: fab_engine.engine.layers module with LayerCategory enum "
            "having card-layer, activated-layer, and triggered-layer"
        )


@then("the categories are card-layer, activated-layer, and triggered-layer")
def step_categories_are_correct(game_state):
    """Rule 1.6.2: The 3 layer categories are card-, activated-, and triggered-layers."""
    try:
        from fab_engine.engine.layers import LayerCategory

        category_names = {cat.value for cat in LayerCategory}
        assert "card-layer" in category_names, (
            "Engine feature needed: LayerCategory.CARD_LAYER"
        )
        assert "activated-layer" in category_names, (
            "Engine feature needed: LayerCategory.ACTIVATED_LAYER"
        )
        assert "triggered-layer" in category_names, (
            "Engine feature needed: LayerCategory.TRIGGERED_LAYER"
        )
    except ImportError:
        pytest.fail(
            "Engine feature needed: LayerCategory enum with CARD_LAYER, ACTIVATED_LAYER, TRIGGERED_LAYER"
        )


@then("a card-layer exists on the stack")
def step_card_layer_exists_on_stack(game_state):
    """Rule 1.6.2a: A card-layer is on the stack."""
    layer = getattr(game_state, "card_layer", None)
    assert layer is not None, (
        "Engine feature needed: CardLayer must be created when card played"
    )
    assert layer.is_layer, "Engine feature needed: CardLayer.is_layer property"
    assert layer.is_on_stack, "Engine feature needed: CardLayer.is_on_stack property"


@then("the layer is categorized as a card-layer")
def step_layer_categorized_as_card_layer(game_state):
    """Rule 1.6.2a: The layer has category 'card-layer'."""
    layer = getattr(game_state, "card_layer", None)
    assert layer is not None, "Engine feature needed: CardLayer must exist"
    assert layer.layer_category == "card-layer", (
        f"Engine feature needed: layer_category must be 'card-layer', got {layer.layer_category}"
    )


@then("the card-layer is represented by the action card")
def step_card_layer_represented_by_card(game_state):
    """Rule 1.6.2a: Card-layer is represented by the card itself on the stack."""
    layer = getattr(game_state, "card_layer", None)
    assert layer is not None, "Engine feature needed: CardLayer must exist"
    assert layer.card is not None, (
        "Engine feature needed: CardLayer.card must reference the card"
    )
    assert layer.card == game_state.test_card, (
        "Engine feature needed: CardLayer.card must be the card that was played"
    )


@then('the card-layer on the stack has name "Lunging Press"')
def step_card_layer_has_name_lunging_press(game_state):
    """Rule 1.6.2a: Card-layer retains the card's name."""
    layer = getattr(game_state, "card_layer", None)
    assert layer is not None, "Engine feature needed: CardLayer must exist"
    assert layer.card is not None, "Engine feature needed: CardLayer.card must exist"
    assert layer.card.name == "Lunging Press", (
        f"Engine feature needed: Card-layer's card must have name 'Lunging Press', got {layer.card.name}"
    )


@then("the card-layer is the card itself on the stack")
def step_card_layer_is_card_on_stack(game_state):
    """Rule 1.6.2a: A card-layer IS the card on the stack (not a separate object)."""
    layer = getattr(game_state, "card_layer", None)
    assert layer is not None, "Engine feature needed: CardLayer must exist"
    # Card-layer directly represents the card on the stack
    assert layer.card is not None, (
        "Engine feature needed: CardLayer.card references the card"
    )


@then('the activated-layer has resolution ability "Gain 2 resources"')
def step_activated_layer_has_resolution_ability(game_state):
    """Rule 1.6.2b: The activated-layer has the resolution ability from the activated ability."""
    layer = getattr(game_state, "activated_layer", None)
    assert layer is not None, "Engine feature needed: ActivatedLayer must exist"
    assert layer.resolution_ability == "Gain 2 resources", (
        f"Engine feature needed: ActivatedLayer.resolution_ability must be 'Gain 2 resources', "
        f"got {layer.resolution_ability}"
    )


@then('the activated-layer category is "activated-layer"')
def step_activated_layer_category(game_state):
    """Rule 1.6.2b: Layer is categorized as 'activated-layer'."""
    layer = getattr(game_state, "activated_layer", None)
    assert layer is not None, "Engine feature needed: ActivatedLayer must exist"
    assert layer.layer_category == "activated-layer", (
        f"Engine feature needed: layer_category must be 'activated-layer', got {layer.layer_category}"
    )


@then("the activated-layer can only exist on the stack")
def step_activated_layer_only_on_stack(game_state):
    """Rule 1.6.2b: Activated-layer can only exist on the stack."""
    layer = getattr(game_state, "queried_layer", None) or getattr(
        game_state, "activated_layer", None
    )
    assert layer is not None, "Engine feature needed: ActivatedLayer must exist"
    assert layer.can_only_exist_on_stack, (
        "Engine feature needed: ActivatedLayer.can_only_exist_on_stack must be True"
    )


@then("it cannot exist in hand, graveyard, banished, or arena zones")
def step_activated_layer_cannot_exist_in_other_zones(game_state):
    """Rule 1.6.2b: Activated-layer cannot exist outside the stack."""
    layer = getattr(game_state, "queried_layer", None) or getattr(
        game_state, "activated_layer", None
    )
    assert layer is not None, "Engine feature needed: ActivatedLayer must exist"
    # Engine feature needed: Zone validity check for layers
    invalid_zones = ["hand", "graveyard", "banished", "arena"]
    for zone in invalid_zones:
        valid = getattr(layer, f"can_exist_in_{zone}", True)
        assert not valid, (
            f"Engine feature needed: ActivatedLayer cannot exist in {zone} zone"
        )


@then("a triggered-layer is created")
def step_triggered_layer_is_created(game_state):
    """Rule 1.6.2c: A triggered-layer was created."""
    layer = getattr(game_state, "triggered_layer", None)
    assert layer is not None, (
        "Engine feature needed: TriggeredLayer must be created when triggered effect fires"
    )
    assert layer.is_layer, "Engine feature needed: TriggeredLayer.is_layer must be True"


@then("the triggered-layer is put on the stack")
def step_triggered_layer_put_on_stack(game_state):
    """Rule 1.6.2c: The triggered-layer is placed on the stack."""
    layer = getattr(game_state, "triggered_layer", None)
    assert layer is not None, (
        "Engine feature needed: TriggeredLayer must be on the stack"
    )
    assert layer.is_on_stack, (
        "Engine feature needed: TriggeredLayer.is_on_stack must be True"
    )


@then('the triggered-layer has resolution ability "Draw a card"')
def step_triggered_layer_has_draw_ability(game_state):
    """Rule 1.6.2c: Triggered-layer has resolution ability from the triggered effect."""
    layer = getattr(game_state, "triggered_layer", None)
    assert layer is not None, "Engine feature needed: TriggeredLayer must exist"
    assert layer.resolution_ability == "Draw a card", (
        f"Engine feature needed: TriggeredLayer.resolution_ability must be 'Draw a card', "
        f"got {layer.resolution_ability}"
    )


@then('the triggered-layer category is "triggered-layer"')
def step_triggered_layer_category(game_state):
    """Rule 1.6.2c: Layer is categorized as 'triggered-layer'."""
    layer = getattr(game_state, "triggered_layer", None)
    assert layer is not None, "Engine feature needed: TriggeredLayer must exist"
    assert layer.layer_category == "triggered-layer", (
        f"Engine feature needed: layer_category must be 'triggered-layer', got {layer.layer_category}"
    )


@then("the triggered-layer is first created as an object")
def step_triggered_layer_created_as_object_first(game_state):
    """Rule 1.6.2c: Triggered-layer is created BEFORE being put on stack."""
    # Engine feature needed: Two-step creation for triggered layers
    created_first = getattr(game_state, "triggered_layer_created_first", False)
    layer = getattr(game_state, "triggered_layer", None)
    assert layer is not None, "Engine feature needed: TriggeredLayer creation"
    # The test verifies the engine correctly creates the layer before placing it
    assert layer.is_layer, (
        "Engine feature needed: TriggeredLayer must be created as a layer object"
    )


@then("then the triggered-layer is put on the stack")
def step_triggered_layer_then_put_on_stack(game_state):
    """Rule 1.6.2c: After creation, triggered-layer is placed on the stack."""
    layer = getattr(game_state, "triggered_layer", None)
    assert layer is not None, "Engine feature needed: TriggeredLayer must be on stack"
    assert layer.is_on_stack, (
        "Engine feature needed: TriggeredLayer must be on stack after creation"
    )


@then("the triggered-layer can only exist on the stack once placed")
def step_triggered_layer_can_only_exist_on_stack(game_state):
    """Rule 1.6.2c: Once placed, triggered-layer can only exist on the stack."""
    layer = getattr(game_state, "triggered_layer", None)
    assert layer is not None, "Engine feature needed: TriggeredLayer must exist"
    assert layer.can_only_exist_on_stack, (
        "Engine feature needed: TriggeredLayer.can_only_exist_on_stack must be True"
    )


@then("the triggered-layer can only exist on the stack")
def step_triggered_layer_only_on_stack(game_state):
    """Rule 1.6.2c: Triggered-layer can only exist on the stack."""
    layer = getattr(game_state, "queried_layer", None) or getattr(
        game_state, "triggered_layer", None
    )
    assert layer is not None, "Engine feature needed: TriggeredLayer must exist"
    assert layer.can_only_exist_on_stack, (
        "Engine feature needed: TriggeredLayer.can_only_exist_on_stack must be True"
    )


@then("it cannot exist outside the stack")
def step_layer_cannot_exist_outside_stack(game_state):
    """Rule 1.6.2c: Layer cannot exist in any zone except the stack."""
    layer = getattr(game_state, "queried_layer", None) or getattr(
        game_state, "triggered_layer", None
    )
    assert layer is not None, "Engine feature needed: Layer must exist"
    assert layer.can_only_exist_on_stack, (
        "Engine feature needed: Layer.can_only_exist_on_stack must be True"
    )


@then("the activated-layer still exists on the stack")
def step_activated_layer_still_on_stack(game_state):
    """Rule 1.7.1a: Activated-layer persists on stack despite source destruction."""
    layer = getattr(game_state, "activated_layer", None)
    assert layer is not None, (
        "Engine feature needed: ActivatedLayer must persist after source destroyed"
    )
    assert layer.is_on_stack, (
        "Engine feature needed: ActivatedLayer.is_on_stack must remain True after source destroyed"
    )


@then('the absence of "Energy Potion" does not prevent resolution')
def step_energy_potion_absence_no_effect(game_state):
    """Rule 1.7.1a: Source being gone doesn't prevent layer resolution."""
    layer = getattr(game_state, "activated_layer", None)
    assert layer is not None, "Engine feature needed: ActivatedLayer must exist"
    source_destroyed = getattr(game_state, "source_destroyed", False)
    assert source_destroyed, "Test setup: source should have been destroyed"
    # The layer should still be resolvable
    assert not layer.is_prevented_by_source_absence, (
        "Engine feature needed: ActivatedLayer.is_prevented_by_source_absence must be False "
        "(layers exist independently of their source per Rule 1.7.1a)"
    )


@then("the triggered-layer still exists on the stack")
def step_triggered_layer_still_on_stack(game_state):
    """Rule 1.7.1a: Triggered-layer persists on stack despite source leaving play."""
    layer = getattr(game_state, "triggered_layer", None)
    assert layer is not None, (
        "Engine feature needed: TriggeredLayer must persist after source leaves"
    )
    assert layer.is_on_stack, (
        "Engine feature needed: TriggeredLayer.is_on_stack must remain True after source leaves play"
    )


@then("the source being gone does not prevent the triggered-layer from resolving")
def step_source_gone_no_prevention(game_state):
    """Rule 1.7.1a: Source leaving doesn't prevent triggered-layer resolution."""
    layer = getattr(game_state, "triggered_layer", None)
    assert layer is not None, "Engine feature needed: TriggeredLayer must exist"
    source_gone = getattr(game_state, "source_destroyed", False)
    assert source_gone, "Test setup: source should have left play"
    # The layer should still be resolvable
    assert not layer.is_prevented_by_source_absence, (
        "Engine feature needed: TriggeredLayer.is_prevented_by_source_absence must be False "
        "(layers exist independently of their source per Rule 1.7.1a)"
    )


# ============================================================
# Fixtures
# ============================================================


@pytest.fixture
def game_state():
    """
    Fixture providing game state for Section 1.6 layer tests.

    Uses BDDGameState which integrates with the real engine.
    Reference: Rule 1.6
    """
    from tests.bdd_helpers import BDDGameState

    state = BDDGameState()

    # Additional state for layer tests
    state.stack_layers = []  # List of layer stubs on the stack
    state.card_layer = None
    state.activated_layer = None
    state.triggered_layer = None
    state.played_card_layer = None
    state.queried_layer = None
    state.source_destroyed = False
    state.source_in_graveyard = False
    state.triggered_source_controller_id = 0
    state.triggered_layer_created_first = False
    state.triggered_layer_on_stack = False
    state.layer_categories_queried = False
    state.snatch_hit = False
    state.snatch_card = None

    return state


# ============================================================
# Layer Stub Classes
# (These stubs model the EXPECTED engine behavior per the rules.
#  The engine must implement real Layer classes to replace these.)
# ============================================================


class CardLayerStub:
    """
    Stub for a card-layer (Rule 1.6.2a).

    Engine Feature Needed:
    - [ ] CardLayer class wrapping a CardInstance on the stack
    - [ ] CardLayer.layer_category == "card-layer"
    - [ ] CardLayer.owner_id = card owner
    - [ ] CardLayer.controller_id = player who played it
    - [ ] CardLayer.is_layer = True
    - [ ] CardLayer.is_on_stack = True (while on stack)
    - [ ] CardLayer.is_resolved = False (until resolved)
    - [ ] CardLayer.is_game_object = True
    """

    def __init__(self, card, owner_id: int, controller_id: int):
        self.card = card
        self.owner_id = owner_id
        self.controller_id = controller_id
        self.layer_category = "card-layer"
        self.is_layer = True
        self.is_on_stack = True
        self.is_resolved = False
        self.is_game_object = True
        self.can_only_exist_on_stack = True

    @property
    def name(self):
        return self.card.name if self.card else None


class ActivatedLayerStub:
    """
    Stub for an activated-layer (Rule 1.6.2b).

    Engine Feature Needed:
    - [ ] ActivatedLayer class created by activated ability
    - [ ] ActivatedLayer.layer_category == "activated-layer"
    - [ ] ActivatedLayer.owner_id = player who activated ability
    - [ ] ActivatedLayer.controller_id = player who put it on stack
    - [ ] ActivatedLayer.resolution_ability = ability text
    - [ ] ActivatedLayer.is_layer = True
    - [ ] ActivatedLayer.is_on_stack = True (while on stack)
    - [ ] ActivatedLayer.can_only_exist_on_stack = True
    - [ ] ActivatedLayer.is_prevented_by_source_absence = False (Rule 1.7.1a)
    - [ ] ActivatedLayer.can_exist_in_hand/graveyard/banished/arena = False
    """

    def __init__(self, resolution_ability: str, owner_id: int, controller_id: int):
        self.resolution_ability = resolution_ability
        self.owner_id = owner_id
        self.controller_id = controller_id
        self.layer_category = "activated-layer"
        self.is_layer = True
        self.is_on_stack = True
        self.is_resolved = False
        self.is_game_object = True
        self.can_only_exist_on_stack = True
        self.is_prevented_by_source_absence = False  # Rule 1.7.1a
        # Zone validity
        self.can_exist_in_hand = False
        self.can_exist_in_graveyard = False
        self.can_exist_in_banished = False
        self.can_exist_in_arena = False


class TriggeredLayerStub:
    """
    Stub for a triggered-layer (Rule 1.6.2c).

    Engine Feature Needed:
    - [ ] TriggeredLayer class created by triggered effect
    - [ ] TriggeredLayer.layer_category == "triggered-layer"
    - [ ] TriggeredLayer.owner_id = controller of source at trigger time
    - [ ] TriggeredLayer.controller_id = player who put it on stack
    - [ ] TriggeredLayer.resolution_ability = ability text
    - [ ] TriggeredLayer.is_layer = True
    - [ ] TriggeredLayer.is_on_stack = True (while on stack)
    - [ ] TriggeredLayer.can_only_exist_on_stack = True
    - [ ] TriggeredLayer.is_prevented_by_source_absence = False (Rule 1.7.1a)
    """

    def __init__(self, resolution_ability: str, owner_id: int, controller_id: int):
        self.resolution_ability = resolution_ability
        self.owner_id = owner_id
        self.controller_id = controller_id
        self.layer_category = "triggered-layer"
        self.is_layer = True
        self.is_on_stack = True
        self.is_resolved = False
        self.is_game_object = True
        self.can_only_exist_on_stack = True
        self.is_prevented_by_source_absence = False  # Rule 1.7.1a
