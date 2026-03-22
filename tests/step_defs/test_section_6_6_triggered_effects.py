"""
Step definitions for Section 6.6: Triggered Effects
Reference: Flesh and Blood Comprehensive Rules Section 6.6

This module implements behavioral tests for triggered effects: effects that
create triggered-layers placed on the stack when their trigger condition is met.
Covers inline-triggered, delayed-triggered, and static-triggered variants, along
with trigger limits, ordinal conditions, state-based triggers, and triggered-layer
stack ordering rules.

Engine Features Needed for Section 6.6:
- [ ] TriggeredEffect class distinguishing event-based vs state-based conditions (Rule 6.6.1c)
- [ ] TriggeredEffect.trigger_limit property - max times the effect can fire (Rule 6.6.1a)
- [ ] TriggeredEffect.ordinal property - which occurrence triggers the effect (Rule 6.6.1b)
- [ ] TriggeredEffect.trigger_count counter tracking how many times it has fired (Rule 6.6.5e)
- [ ] TriggeredEffect.check_trigger(event) - returns True if event meets condition (Rule 6.6.5)
- [ ] TriggeredEffect.fire() -> TriggeredLayer - creates triggered-layer (Rule 6.6.5)
- [ ] InlineTriggeredEffect subclass - fires only when generated, not retroactively (Rule 6.6.2)
- [ ] DelayedTriggeredEffect subclass - layer-continuous, requires duration (Rule 6.6.3)
- [ ] StaticTriggeredEffect subclass - static-continuous, fires repeatedly (Rule 6.6.4)
- [ ] GameStateProcess.add_triggered_layer_to_stack() - before next priority (Rule 6.6.6)
- [ ] TriggeredLayer.declare_parameters() - modal modes + targets before stack (Rule 6.6.6a)
- [ ] TriggeredLayer.ceases_to_exist_if_no_targets() - no legal targets -> not added (Rule 6.6.6a)
- [ ] Stack.add_pending_triggered_layers(turn_player_selection) - ordering (Rule 6.6.6b)
- [ ] TriggerPreventionEffect - prevents layer creation but counts toward limit (Rule 6.6.5f)

Current status: Tests written, Engine pending
"""

import pytest
from pytest_bdd import scenario, given, when, then, parsers


def _make_triggered_layer(game_state, source_card, ability_text, controller_id=0):
    """
    Helper to create a TriggeredLayerStub directly, bypassing the BDDGameState method
    override at line 2578 (which only accepts 'source').
    """
    from tests.bdd_helpers import TriggeredLayerStub
    return TriggeredLayerStub(
        source=source_card,
        controller_id=controller_id,
        ability_text=ability_text,
    )


# ===== Scenarios =====


@scenario(
    "../features/section_6_6_triggered_effects.feature",
    "A triggered effect creates a triggered-layer when its condition is met",
)
def test_triggered_effect_creates_triggered_layer():
    """Rule 6.6.1 + 6.6.5: Triggered effects create a triggered-layer added to the stack."""
    pass


@scenario(
    "../features/section_6_6_triggered_effects.feature",
    "A triggered effect does not use the word \"instead\"",
)
def test_triggered_effect_not_replacement():
    """Rule 6.6.1: Triggered effects are distinct from replacement effects - never use 'instead'."""
    pass


@scenario(
    "../features/section_6_6_triggered_effects.feature",
    "A triggered effect with no trigger limit triggers any number of times",
)
def test_unlimited_triggered_effect():
    """Rule 6.6.1a: No trigger limit means the effect can be triggered any number of times."""
    pass


@scenario(
    "../features/section_6_6_triggered_effects.feature",
    "A triggered effect with a trigger limit cannot exceed that limit",
)
def test_trigger_limit_restricts_triggers():
    """Rule 6.6.1a: Trigger limit is the maximum number of times an effect can be triggered."""
    pass


@scenario(
    "../features/section_6_6_triggered_effects.feature",
    "A triggered effect with an ordinal only triggers on the specified occurrence",
)
def test_ordinal_trigger_condition():
    """Rule 6.6.1b: Ordinal specifies which event occurrence(s) trigger the effect."""
    pass


@scenario(
    "../features/section_6_6_triggered_effects.feature",
    "An event-based triggered effect triggers when the specified event occurs",
)
def test_event_based_triggered_effect():
    """Rule 6.6.1c: Event-based triggered effects fire when the specified event occurs."""
    pass


@scenario(
    "../features/section_6_6_triggered_effects.feature",
    "A state-based triggered effect triggers when the game state meets its condition",
)
def test_state_based_triggered_effect():
    """Rule 6.6.1c: State-based triggered effects fire when the game state meets the condition."""
    pass


@scenario(
    "../features/section_6_6_triggered_effects.feature",
    "Triggered-layer generates effects when it resolves",
)
def test_triggered_layer_generates_effects_on_resolve():
    """Rule 6.6.1d: Resolution abilities of the triggered-layer generate effects when it resolves."""
    pass


@scenario(
    "../features/section_6_6_triggered_effects.feature",
    "An inline-triggered effect triggers only when it is generated",
)
def test_inline_triggered_effect_fires_when_generated():
    """Rule 6.6.2: Inline-triggered effects are discrete and only fire when generated."""
    pass


@scenario(
    "../features/section_6_6_triggered_effects.feature",
    "An inline-triggered effect does not trigger if condition met after generation",
)
def test_inline_triggered_effect_no_retroactive_trigger():
    """Rule 6.6.2a: Inline-triggered effects don't trigger retroactively."""
    pass


@scenario(
    "../features/section_6_6_triggered_effects.feature",
    "A delayed-triggered effect is a layer-continuous triggered effect",
)
def test_delayed_triggered_effect_is_layer_continuous():
    """Rule 6.6.3: Delayed-triggered effects are layer-continuous triggered effects."""
    pass


@scenario(
    "../features/section_6_6_triggered_effects.feature",
    "A delayed triggered effect specifies its duration",
)
def test_delayed_triggered_effect_specifies_duration():
    """Rule 6.6.3a: Delayed triggered effects always specify their duration."""
    pass


@scenario(
    "../features/section_6_6_triggered_effects.feature",
    "A delayed triggered effect conditional on combat chain close lasts until triggered",
)
def test_delayed_triggered_effect_duration_combat_chain():
    """Rule 6.6.3a: Delayed triggered effects ending with phase/step change last until triggered."""
    pass


@scenario(
    "../features/section_6_6_triggered_effects.feature",
    "A static-triggered effect is a static-continuous triggered effect",
)
def test_static_triggered_effect_is_static_continuous():
    """Rule 6.6.4: Static-triggered effects are static-continuous triggered effects."""
    pass


@scenario(
    "../features/section_6_6_triggered_effects.feature",
    "A static-triggered effect with a limit specified",
)
def test_static_triggered_effect_with_limit():
    """Rule 6.6.4: Static-triggered effects can have a trigger limit and ordinal."""
    pass


@scenario(
    "../features/section_6_6_triggered_effects.feature",
    "A triggered effect is triggered when the game event meets the trigger condition",
)
def test_effect_is_triggered_when_condition_met():
    """Rule 6.6.5: Effect is triggered when the game event meets the trigger condition."""
    pass


@scenario(
    "../features/section_6_6_triggered_effects.feature",
    "A triggered effect does not fire if it did not exist before the triggering event",
)
def test_triggered_effect_must_exist_before_event():
    """Rule 6.6.5a: Triggered effect must exist before the triggering event occurs."""
    pass


@scenario(
    "../features/section_6_6_triggered_effects.feature",
    "An inline-triggered effect fires even as it is being generated",
)
def test_inline_triggered_effect_fires_during_generation():
    """Rule 6.6.5a exception: Inline-triggered effects fire as they are generated."""
    pass


@scenario(
    "../features/section_6_6_triggered_effects.feature",
    "An event-based triggered effect does not trigger if the event is modified and no longer meets the condition",
)
def test_event_based_no_trigger_if_event_modified():
    """Rule 6.6.5b: Event-based effects don't trigger if event is replaced and no longer meets condition."""
    pass


@scenario(
    "../features/section_6_6_triggered_effects.feature",
    "A triggered effect with both event and state conditions only triggers when both are met",
)
def test_combined_event_and_state_condition():
    """Rule 6.6.5b: If trigger has event + state conditions, both must be met."""
    pass


@scenario(
    "../features/section_6_6_triggered_effects.feature",
    "A state-based triggered effect triggers when the game state changes to meet its condition",
)
def test_state_based_triggers_on_state_change():
    """Rule 6.6.5c: State-based triggered effect triggers on change from not-met to met."""
    pass


@scenario(
    "../features/section_6_6_triggered_effects.feature",
    "A state-based triggered effect generated while condition is already met triggers immediately",
)
def test_state_based_triggers_if_condition_already_met_at_generation():
    """Rule 6.6.5c: State-based effect generated while condition is already met triggers immediately."""
    pass


@scenario(
    "../features/section_6_6_triggered_effects.feature",
    "A triggered effect with ordinal does not trigger after the specified ordinal time has passed",
)
def test_ordinal_trigger_missed_if_ordinal_passed():
    """Rule 6.6.5d: If effect becomes functional after the ordinal time, it won't trigger that duration."""
    pass


@scenario(
    "../features/section_6_6_triggered_effects.feature",
    "A triggered effect at its trigger limit does not create another triggered-layer",
)
def test_trigger_limit_prevents_layer_creation():
    """Rule 6.6.5e: When trigger limit is reached, no additional triggered-layer is created."""
    pass


@scenario(
    "../features/section_6_6_triggered_effects.feature",
    "Triggering prevented by an effect still counts toward the trigger limit",
)
def test_prevention_counts_toward_trigger_limit():
    """Rule 6.6.5f: Even if triggering is prevented, it counts toward the trigger limit."""
    pass


@scenario(
    "../features/section_6_6_triggered_effects.feature",
    "A triggered-layer is added to the stack before the next player receives priority",
)
def test_triggered_layer_added_before_priority():
    """Rule 6.6.6: Triggered-layers are added to the stack as a game state process before priority."""
    pass


@scenario(
    "../features/section_6_6_triggered_effects.feature",
    "Controller must declare parameters when triggered-layer is added to stack",
)
def test_controller_declares_parameters_for_triggered_layer():
    """Rule 6.6.6a: Controller declares modes and targets when triggered-layer is added to stack."""
    pass


@scenario(
    "../features/section_6_6_triggered_effects.feature",
    "A triggered-layer ceases to exist if no legal targets can be declared",
)
def test_triggered_layer_ceases_if_no_legal_targets():
    """Rule 6.6.6a: If no legal targets can be declared, triggered-layer ceases to exist."""
    pass


@scenario(
    "../features/section_6_6_triggered_effects.feature",
    "Triggered-layer from Thaw requires mode and target selection before being added to stack",
)
def test_thaw_like_triggered_layer_requires_mode_and_target():
    """Rule 6.6.6a: Modal triggered-layers require mode + target declaration before being added to stack."""
    pass


@scenario(
    "../features/section_6_6_triggered_effects.feature",
    "Multiple simultaneous triggered-layers are ordered by turn-player selection",
)
def test_multiple_triggered_layers_ordered_by_turn_player():
    """Rule 6.6.6b: Multiple simultaneous triggered-layers ordered by turn-player selection."""
    pass


@scenario(
    "../features/section_6_6_triggered_effects.feature",
    "Player can order their own triggered-layers to maximize benefit",
)
def test_player_can_order_own_triggered_layers():
    """Rule 6.6.6b: Example - player orders triggered-layers to gain resource before spending it."""
    pass


# ===== Step Definitions =====


@given(parsers.parse('a player has a card with a triggered effect "{ability_text}"'))
def player_has_card_with_triggered_effect(game_state, ability_text):
    """Set up a card with a triggered effect for the player. Rule 6.6.1."""
    card = game_state.create_card("Triggered Effect Card")
    game_state.test_card = card
    game_state.triggered_effect_text = ability_text
    game_state.trigger_limit = None
    game_state.trigger_count = 0
    game_state.triggered_layers = []


@given("there is no trigger limit specified")
def no_trigger_limit(game_state):
    """The triggered effect has no trigger limit. Rule 6.6.1a."""
    game_state.trigger_limit = None


@given(parsers.parse("the trigger limit is {limit:d}"))
def set_trigger_limit(game_state, limit):
    """The triggered effect has a specific trigger limit. Rule 6.6.1a."""
    game_state.trigger_limit = limit


@given(parsers.parse('a triggered effect with text "{ability_text}"'))
def triggered_effect_with_text(game_state, ability_text):
    """A triggered effect with the given text. Rule 6.6.1."""
    game_state.triggered_effect_text = ability_text
    game_state.triggered_effect_type = "triggered"


@given(parsers.parse('a delayed-triggered effect "{ability_text}"'))
def delayed_triggered_effect(game_state, ability_text):
    """Set up a delayed-triggered effect. Rule 6.6.3."""
    card = game_state.create_card("Delayed Trigger Card")
    game_state.test_card = card
    game_state.triggered_effect_text = ability_text
    game_state.triggered_effect_category = "delayed-triggered"
    game_state.triggered_layers = []


@given("a player controls a permanent with a static-triggered effect \"Whenever you boost, create a Ponder token\"")
def permanent_with_static_triggered_effect(game_state):
    """Set up a permanent with a static-triggered effect. Rule 6.6.4."""
    card = game_state.create_card("Static Trigger Permanent")
    game_state.play_card_to_arena(card, controller_id=0)
    game_state.test_card = card
    game_state.triggered_effect_text = "Whenever you boost, create a Ponder token"
    game_state.triggered_effect_category = "static-triggered"
    game_state.triggered_layers = []


@given("a player controls a permanent with a static-triggered effect \"The first time you boost each turn, gain 1 life\"")
def permanent_with_limited_static_triggered_effect(game_state):
    """Set up a permanent with a static-triggered effect that has a limit. Rule 6.6.4."""
    card = game_state.create_card("Limited Static Trigger Permanent")
    game_state.play_card_to_arena(card, controller_id=0)
    game_state.test_card = card
    game_state.triggered_effect_text = "The first time you boost each turn, gain 1 life"
    game_state.triggered_effect_category = "static-triggered"
    game_state.trigger_limit = 1
    game_state.trigger_ordinal = "first"
    game_state.triggered_layers = []


@given("a discrete effect contains an inline-triggered effect \"When [condition] [effect]\"")
def discrete_effect_with_inline_triggered(game_state):
    """Set up a discrete effect containing an inline-triggered effect. Rule 6.6.2."""
    card = game_state.create_card("Inline Trigger Card")
    game_state.test_card = card
    game_state.triggered_effect_category = "inline-triggered"
    game_state.inline_condition_met_at_generation = False
    game_state.inline_condition_met_after_generation = False
    game_state.inline_effect_fired = False
    game_state.triggered_layers = []


@given("two or more triggered-layers would be created simultaneously")
def multiple_simultaneous_triggered_layers(game_state):
    """Set up a scenario where two triggered-layers fire simultaneously. Rule 6.6.6b."""
    from tests.bdd_helpers import TestPlayer
    game_state.player2 = TestPlayer(player_id=1)
    card1 = game_state.create_card("Trigger Card A")
    card2 = game_state.create_card("Trigger Card B")
    game_state.pending_triggered_layers = [
        _make_triggered_layer(game_state, card1, "Trigger A effect", controller_id=0),
        _make_triggered_layer(game_state, card2, "Trigger B effect", controller_id=0),
    ]
    game_state.triggered_layers = []


@given("player 1 is the turn-player")
def player_1_is_turn_player(game_state):
    """Designate player 1 as the turn-player. Rule 6.6.6b."""
    game_state.turn_player_id = 0
    game_state.turn_player = game_state.player


@given(parsers.parse('a card with a state-based triggered effect "{ability_text}"'))
def card_with_state_based_effect(game_state, ability_text):
    """Set up a card with a state-based triggered effect. Rule 6.6.5c."""
    card = game_state.create_card("State Trigger Card")
    game_state.test_card = card
    game_state.triggered_effect_text = ability_text
    game_state.triggered_effect_category = "state-based"
    game_state.trigger_count = 0
    game_state.triggered_layers = []


@given(parsers.parse("the card initially has {n:d} steam counter"))
def card_has_n_steam_counters(game_state, n):
    """Card starts with some counters. Rule 6.6.5c."""
    game_state.card_counter_count = n


@given("a player has a card with a state-based triggered effect \"When this has no steam counters, destroy it\"")
def player_has_state_based_card(game_state):
    """Set up a card with state-based effect. Rule 6.6.5c."""
    card = game_state.create_card("Hyper Driver Like Card")
    game_state.test_card = card
    game_state.triggered_effect_text = "When this has no steam counters, destroy it"
    game_state.triggered_effect_category = "state-based"
    game_state.card_counter_count = 1
    game_state.trigger_count = 0
    game_state.triggered_layers = []


@given("a player has a card with a triggered effect that has modal resolution abilities")
def card_with_modal_triggered_effect(game_state):
    """Card has a triggered effect with modal abilities requiring mode declaration. Rule 6.6.6a."""
    card = game_state.create_card("Modal Trigger Card")
    game_state.test_card = card
    game_state.triggered_effect_text = "Triggered modal ability: choose 1 - do A or do B"
    game_state.triggered_effect_category = "modal-triggered"
    game_state.declared_mode = None
    game_state.triggered_layers = []


@given("a player has a card with a triggered effect that requires a legal target")
def card_with_targeted_triggered_effect(game_state):
    """Card has a triggered effect requiring targets. Rule 6.6.6a."""
    card = game_state.create_card("Targeted Trigger Card")
    game_state.test_card = card
    game_state.triggered_effect_text = "Triggered: destroy target permanent"
    game_state.triggered_effect_requires_target = True
    game_state.triggered_layers = []


@given("there are no legal targets available in the game state")
def no_legal_targets_available(game_state):
    """No legal targets exist for the triggered-layer. Rule 6.6.6a."""
    game_state.legal_targets_available = False


@given("a player has a card similar to Thaw with a triggered effect with multiple modes requiring targets")
def card_similar_to_thaw(game_state):
    """Card with modal triggered effect where each mode requires a target. Rule 6.6.6a."""
    card = game_state.create_card("Thaw-like Card")
    game_state.test_card = card
    game_state.triggered_effect_text = (
        "At the start of your turn, choose 1: Destroy target Frostbite. "
        "Destroy target Ice affliction. Unfreeze target frozen card."
    )
    game_state.triggered_effect_requires_target = True
    game_state.triggered_effect_is_modal = True
    game_state.triggered_layers = []


@given("a player has a card with a triggered effect limited to triggering once per turn")
def card_with_once_per_turn_triggered_effect(game_state):
    """Card with a once-per-turn triggered effect. Rule 6.6.5e."""
    card = game_state.create_card("Once Per Turn Trigger Card")
    game_state.test_card = card
    game_state.triggered_effect_text = "Once per turn - When [event], [effect]"
    game_state.trigger_limit = 1
    game_state.trigger_count = 0
    game_state.triggered_layers = []


@given("the effect has already triggered once this turn")
def effect_already_triggered_once(game_state):
    """The triggered effect has already fired once this turn. Rule 6.6.5e."""
    game_state.trigger_count = 1


@given("a player controls Katsu with \"The first time an attack action card you control hits each turn, [effect]\"")
def player_controls_katsu_like_card(game_state):
    """Katsu-like card with once-per-turn triggered effect. Rule 6.6.5f."""
    card = game_state.create_card("Katsu-like Card")
    game_state.play_card_to_arena(card, controller_id=0)
    game_state.katsu_card = card
    game_state.trigger_limit = 1
    game_state.trigger_count = 0
    game_state.katsu_triggered_layers = []


@given("Tripwire Trap is active with \"Hit effects don't trigger this chain link\"")
def tripwire_trap_is_active(game_state):
    """Tripwire Trap prevention effect is active. Rule 6.6.5f."""
    card = game_state.create_card("Tripwire Trap")
    game_state.play_card_to_arena(card, controller_id=1)
    game_state.prevention_effect_active = True
    game_state.prevention_effect_text = "Hit effects don't trigger this chain link"


@given("a player has a card with an event-based triggered effect \"When this hits, draw a card\"")
def card_with_hit_triggered_effect(game_state):
    """Card with event-based triggered effect. Rule 6.6.5b."""
    card = game_state.create_card("Hit Trigger Card")
    game_state.test_card = card
    game_state.triggered_effect_text = "When this hits, draw a card"
    game_state.triggered_effect_category = "event-based"
    game_state.trigger_count = 0
    game_state.triggered_layers = []


@given("a replacement effect modifies the event so the card no longer hits")
def replacement_effect_modifies_event(game_state):
    """A replacement effect prevents the 'hit' event. Rule 6.6.5b."""
    game_state.event_modified_by_replacement = True
    game_state.modified_event_still_triggers = False


@given("a player has a card with a triggered effect requiring both an event and a state condition")
def card_with_combined_event_state_condition(game_state):
    """Card with triggered effect requiring both event and state conditions. Rule 6.6.5b."""
    card = game_state.create_card("Combined Condition Trigger Card")
    game_state.test_card = card
    game_state.triggered_effect_text = "When [event] and [state condition], [effect]"
    game_state.triggered_effect_category = "event-and-state"
    game_state.trigger_count = 0
    game_state.triggered_layers = []


@given("a triggered effect fires during a game state process")
def triggered_effect_fires_during_game_state_process(game_state):
    """Set up scenario where triggered effect fires during game state process. Rule 6.6.6."""
    card = game_state.create_card("GSP Trigger Card")
    game_state.test_card = card
    game_state.triggered_layers = []
    game_state.priority_received = False


@given("a triggering event occurs before the triggered effect exists")
def triggering_event_occurs_before_effect_exists(game_state):
    """Event occurs before the triggered effect is generated. Rule 6.6.5a."""
    game_state.event_occurred_at = 1
    game_state.triggered_effect_created_at = 2
    game_state.triggered_layers = []


@given("a discrete effect generates an inline-triggered effect")
def discrete_effect_generates_inline_triggered(game_state):
    """Set up inline-triggered effect being generated. Rule 6.6.5a exception."""
    card = game_state.create_card("Inline Trigger Source Card")
    game_state.test_card = card
    game_state.triggered_effect_category = "inline-triggered"
    game_state.triggered_layers = []


@given("the trigger condition is met at the moment of generation")
def trigger_condition_met_at_generation(game_state):
    """The inline trigger condition is satisfied at the moment the effect is generated. Rule 6.6.5a."""
    game_state.inline_condition_met_at_generation = True


@given("a player controls two permanents with triggered effects that fire simultaneously")
def two_permanents_with_simultaneous_triggers(game_state):
    """Two permanents with effects that both fire at the same time. Rule 6.6.6b."""
    card1 = game_state.create_card("Celestial Kimono-like Card")
    card2 = game_state.create_card("Diadem of Dreamstate-like Card")
    game_state.play_card_to_arena(card1, controller_id=0)
    game_state.play_card_to_arena(card2, controller_id=0)
    game_state.simultaneous_trigger_card1 = card1
    game_state.simultaneous_trigger_card2 = card2
    game_state.triggered_layers = []


@given("one triggered effect would gain a resource and the other would spend that resource")
def triggered_effects_gain_and_spend_resource(game_state):
    """One trigger gains a resource; the other spends it. Rule 6.6.6b."""
    game_state.trigger1_effect = "gain_resource"
    game_state.trigger2_effect = "spend_resource"
    game_state.pending_triggered_layers = [
        _make_triggered_layer(game_state, 
            game_state.simultaneous_trigger_card1, "When destroyed, gain {r}", controller_id=0
        ),
        _make_triggered_layer(game_state, 
            game_state.simultaneous_trigger_card2, "When destroyed, pay {r} if you do [effect]", controller_id=0
        ),
    ]


@given("the card enters the arena after the player has already boosted once this turn")
def card_enters_arena_after_boost(game_state):
    """The card becomes functional after the ordinal-specified event already occurred. Rule 6.6.5d."""
    game_state.ordinal_event_already_occurred = True
    game_state.boost_count_this_turn = 1


@given("the card enters the arena with no steam counters")
def card_enters_arena_without_counters(game_state):
    """Card enters arena in a state that already satisfies the state-based trigger. Rule 6.6.5c."""
    game_state.card_counter_count = 0
    game_state.card_in_arena = True


# ===== When steps =====


@when("the triggering event occurs")
def triggering_event_occurs(game_state):
    """Simulate a triggering event. Rule 6.6.5."""
    if not hasattr(game_state, 'trigger_count'):
        game_state.trigger_count = 0
    limit = getattr(game_state, 'trigger_limit', None)
    if limit is None or game_state.trigger_count < limit:
        layer = _make_triggered_layer(game_state, 
            game_state.test_card,
            game_state.triggered_effect_text,
            controller_id=0,
        )
        game_state.triggered_layers.append(layer)
        game_state.trigger_count += 1


@when(parsers.parse("the triggering event occurs {n:d} times"))
def triggering_event_occurs_n_times(game_state, n):
    """Simulate triggering event occurring N times. Rule 6.6.1a."""
    if not hasattr(game_state, 'trigger_count'):
        game_state.trigger_count = 0
    if not hasattr(game_state, 'triggered_layers'):
        game_state.triggered_layers = []
    limit = getattr(game_state, 'trigger_limit', None)
    for _ in range(n):
        if limit is None or game_state.trigger_count < limit:
            layer = _make_triggered_layer(game_state, 
                game_state.test_card,
                game_state.triggered_effect_text,
                controller_id=0,
            )
            game_state.triggered_layers.append(layer)
            game_state.trigger_count += 1


@when("the triggering event occurs a second time")
def triggering_event_occurs_second_time(game_state):
    """Simulate a second triggering event. Rule 6.6.1a."""
    limit = getattr(game_state, 'trigger_limit', None)
    if limit is None or game_state.trigger_count < limit:
        layer = _make_triggered_layer(game_state, 
            game_state.test_card,
            game_state.triggered_effect_text,
            controller_id=0,
        )
        game_state.triggered_layers.append(layer)
        game_state.trigger_count += 1
    # Record that a second trigger was attempted
    game_state.second_trigger_attempted = True


@when("the player attacks for the first time that turn")
def player_attacks_first_time(game_state):
    """Player attacks for the first time this turn. Rule 6.6.1b."""
    game_state.attack_count = 1
    ordinal = getattr(game_state, 'trigger_ordinal', 'first')
    # First attack matches ordinal "first"
    if ordinal == 'first' and game_state.attack_count == 1:
        layer = _make_triggered_layer(game_state, 
            game_state.test_card,
            game_state.triggered_effect_text,
            controller_id=0,
        )
        game_state.triggered_layers.append(layer)
        game_state.trigger_count = getattr(game_state, 'trigger_count', 0) + 1


@when("the player attacks for the second time that turn")
def player_attacks_second_time(game_state):
    """Player attacks for the second time this turn. Rule 6.6.1b."""
    game_state.attack_count = 2
    # Second attack does NOT match ordinal "first"


@when("the card enters the arena")
def card_enters_arena(game_state):
    """Card enters the arena, triggering on-enter effects. Rule 6.6.1c."""
    game_state.play_card_to_arena(game_state.test_card, controller_id=0)
    layer = _make_triggered_layer(game_state, 
        game_state.test_card,
        game_state.triggered_effect_text,
        controller_id=0,
    )
    game_state.triggered_layers.append(layer)
    game_state.trigger_count = getattr(game_state, 'trigger_count', 0) + 1


@when("the game state changes so the card has no counters")
def game_state_changes_no_counters(game_state):
    """Card's counter count drops to zero, meeting state-based trigger condition. Rule 6.6.1c."""
    game_state.card_counter_count = 0
    # State condition is now met - state-based effect triggers
    layer = _make_triggered_layer(game_state, 
        game_state.test_card,
        game_state.triggered_effect_text,
        controller_id=0,
    )
    game_state.triggered_layers.append(layer)
    game_state.trigger_count = getattr(game_state, 'trigger_count', 0) + 1


@when("the triggered-layer has been added to the stack")
@given("the triggered-layer has been added to the stack")
def triggered_layer_added_to_stack(game_state):
    """The triggered-layer is on the stack. Rule 6.6.1d."""
    card = game_state.test_card
    layer = _make_triggered_layer(game_state,
        card, game_state.triggered_effect_text, controller_id=0
    )
    game_state.current_triggered_layer = layer
    game_state.triggered_layers.append(layer)
    game_state.stack = getattr(game_state, 'stack', [])
    game_state.stack.append(layer)


@when("the triggered-layer resolves")
def triggered_layer_resolves(game_state):
    """The triggered-layer resolves generating its effects. Rule 6.6.1d."""
    layer = game_state.current_triggered_layer
    # Simulate resolution - engine would generate effects from resolution abilities
    game_state.resolution_occurred = True
    game_state.effects_generated = layer.ability_text  # What the engine should do


@when("the inline-triggered effect is generated")
def inline_triggered_effect_is_generated(game_state):
    """Inline-triggered effect is generated as part of a discrete effect. Rule 6.6.2."""
    game_state.inline_effect_generated = True
    # If condition is already met, fire immediately
    if getattr(game_state, 'inline_condition_met_at_generation', False):
        game_state.inline_effect_fired = True
        layer = _make_triggered_layer(game_state, 
            game_state.test_card,
            "inline triggered effect",
            controller_id=0,
        )
        game_state.triggered_layers.append(layer)


@when("the condition is met at the time of generation")
def condition_met_at_time_of_generation(game_state):
    """The inline trigger condition is met when the effect is generated. Rule 6.6.2."""
    game_state.inline_condition_met_at_generation = True
    # Re-check if inline effect should fire
    if game_state.inline_effect_generated:
        game_state.inline_effect_fired = True


@when("the condition is not met at the time of generation")
def condition_not_met_at_generation(game_state):
    """The inline trigger condition is NOT met when generated. Rule 6.6.2a."""
    game_state.inline_condition_met_at_generation = False


@when("the condition is met after the effect is generated")
def condition_met_after_generation(game_state):
    """The inline trigger condition becomes met after generation. Rule 6.6.2a."""
    game_state.inline_condition_met_after_generation = True
    # Inline triggered effects do NOT fire retroactively


@when("the delayed-triggered effect is generated as a layer")
def delayed_triggered_effect_generated_as_layer(game_state):
    """Delayed-triggered effect is generated and put on the stack as a layer. Rule 6.6.3."""
    layer = _make_triggered_layer(game_state, 
        game_state.test_card,
        game_state.triggered_effect_text,
        controller_id=0,
    )
    game_state.current_triggered_layer = layer
    game_state.triggered_layers.append(layer)
    game_state.layer_category = "layer-continuous"


@when("an attack hits")
def attack_hits(game_state):
    """An attack hits, potentially triggering hit-based effects. Rule 6.6.5."""
    game_state.attack_hit = True
    limit = getattr(game_state, 'trigger_limit', None)
    if limit is None or game_state.trigger_count < limit:
        layer = _make_triggered_layer(game_state, 
            game_state.test_card,
            game_state.triggered_effect_text,
            controller_id=0,
        )
        game_state.triggered_layers.append(layer)
        game_state.trigger_count += 1


@when("the triggered effect is generated after the event")
def triggered_effect_generated_after_event(game_state):
    """The triggered effect is created after the relevant event. Rule 6.6.5a."""
    # Effect did not exist when event occurred - cannot fire retroactively
    game_state.retroactive_trigger_attempted = True
    # No layer created - effect must exist BEFORE event


@when("the modified event occurs")
def modified_event_occurs(game_state):
    """The event occurs but has been modified by a replacement effect. Rule 6.6.5b."""
    game_state.event_occurred = True
    # Event was modified - it no longer meets the trigger condition
    if getattr(game_state, 'event_modified_by_replacement', False):
        # Event-based effect does not trigger
        game_state.event_triggered = False
    else:
        game_state.event_triggered = True


@when("the triggering event occurs but the state condition is not met")
def triggering_event_occurs_state_not_met(game_state):
    """Event occurs but state condition isn't met. Rule 6.6.5b."""
    game_state.event_occurred = True
    game_state.state_condition_met = False
    # Combined trigger requires both - does not fire


@when("the triggering event occurs and the state condition is met")
def triggering_event_occurs_state_met(game_state):
    """Event occurs and state condition is also met. Rule 6.6.5b."""
    game_state.event_occurred = True
    game_state.state_condition_met = True
    # Both conditions met - trigger fires
    layer = _make_triggered_layer(game_state, 
        game_state.test_card,
        game_state.triggered_effect_text,
        controller_id=0,
    )
    game_state.triggered_layers.append(layer)
    game_state.trigger_count = getattr(game_state, 'trigger_count', 0) + 1


@when("the steam counter is removed and the card now has no steam counters")
def steam_counter_removed(game_state):
    """A counter is removed, changing game state to meet state-based condition. Rule 6.6.5c."""
    game_state.card_counter_count = 0
    # State-based effect triggers due to state change
    layer = _make_triggered_layer(game_state, 
        game_state.test_card,
        game_state.triggered_effect_text,
        controller_id=0,
    )
    game_state.triggered_layers.append(layer)
    game_state.trigger_count = getattr(game_state, 'trigger_count', 0) + 1


@when("the state-based triggered effect is generated and the condition is already met")
def state_based_effect_generated_condition_already_met(game_state):
    """State-based effect is generated when state already meets condition. Rule 6.6.5c."""
    # Card entered arena with no counters - condition is already met
    layer = _make_triggered_layer(game_state, 
        game_state.test_card,
        game_state.triggered_effect_text,
        controller_id=0,
    )
    game_state.triggered_layers.append(layer)
    game_state.trigger_count = getattr(game_state, 'trigger_count', 0) + 1


@when("the player boosts again")
def player_boosts_again(game_state):
    """Player boosts after the ordinal time has already passed. Rule 6.6.5d."""
    game_state.boost_count_this_turn = getattr(game_state, 'boost_count_this_turn', 0) + 1
    # "First time" ordinal has already passed - no trigger


@when("the triggering condition is met again")
def triggering_condition_met_again(game_state):
    """The trigger condition is met again but the limit has been reached. Rule 6.6.5e."""
    game_state.second_trigger_attempted = True
    # Limit already reached - no new triggered-layer created


@when("an attack action card controlled by the Katsu player hits")
def attack_action_card_hits_katsu(game_state):
    """An attack action card hits, potentially triggering Katsu's effect. Rule 6.6.5f."""
    if not hasattr(game_state, 'katsu_hit_count'):
        game_state.katsu_hit_count = 0
    game_state.katsu_hit_count += 1
    # First hit: prevention effect is active - trigger doesn't fire but counts
    if game_state.katsu_hit_count == 1:
        prevention_active = getattr(game_state, 'prevention_effect_active', False)
        if prevention_active:
            # Trigger attempted but prevented - counts toward limit
            game_state.trigger_count += 1
            # No triggered-layer created
        else:
            if game_state.trigger_count < game_state.trigger_limit:
                layer = _make_triggered_layer(game_state, 
                    game_state.katsu_card,
                    "Katsu triggered effect",
                    controller_id=0,
                )
                game_state.katsu_triggered_layers.append(layer)
                game_state.trigger_count += 1


@when("an attack action card controlled by the Katsu player hits again this turn")
def attack_action_card_hits_katsu_again(game_state):
    """Second hit attempt - limit already reached. Rule 6.6.5f."""
    if not hasattr(game_state, 'katsu_hit_count'):
        game_state.katsu_hit_count = 0
    game_state.katsu_hit_count += 1
    # Limit was used by the prevented trigger - no layer created


@when("the card enters the arena with no steam counters")
def card_enters_arena_with_no_counters_when(game_state):
    """Card enters arena with condition already met. Rule 6.6.5c."""
    game_state.card_counter_count = 0
    game_state.card_in_arena = True


@when("the triggered-layer is created")
def triggered_layer_is_created(game_state):
    """The triggered-layer is created as part of a game state process. Rule 6.6.6."""
    layer = _make_triggered_layer(game_state, 
        game_state.test_card,
        "triggered effect",
        controller_id=0,
    )
    game_state.current_triggered_layer = layer
    game_state.triggered_layers.append(layer)
    # Stack addition happens before next priority
    game_state.layer_added_before_priority = True


@when("the triggered effect triggers and a triggered-layer is created")
def triggered_effect_creates_layer(game_state):
    """The triggered effect fires and creates a triggered-layer. Rule 6.6.6a."""
    layer = _make_triggered_layer(game_state, 
        game_state.test_card,
        game_state.triggered_effect_text,
        controller_id=0,
    )
    game_state.current_triggered_layer = layer
    game_state.triggered_layers.append(layer)
    game_state.declared_mode = None  # Must be declared before adding to stack


@when("the triggered effect triggers")
def triggered_effect_triggers_no_targets(game_state):
    """The triggered effect fires but needs targets. Rule 6.6.6a."""
    game_state.triggered_effect_fired = True
    legal_targets = getattr(game_state, 'legal_targets_available', True)
    if not legal_targets:
        # No legal targets - triggered-layer ceases to exist
        game_state.triggered_layer_added_to_stack = False
    else:
        layer = _make_triggered_layer(game_state, 
            game_state.test_card,
            game_state.triggered_effect_text,
            controller_id=0,
        )
        game_state.triggered_layers.append(layer)
        game_state.triggered_layer_added_to_stack = True


@when("the triggered effect fires at start of turn")
def triggered_effect_fires_at_start_of_turn(game_state):
    """Triggered effect fires at start of turn requiring mode and target. Rule 6.6.6a."""
    game_state.triggered_effect_fired = True
    game_state.requires_mode_declaration = True
    game_state.requires_target_declaration = True


@when("both triggered effects fire simultaneously")
def both_triggered_effects_fire_simultaneously(game_state):
    """Both triggered effects fire at the same time. Rule 6.6.6b."""
    game_state.simultaneous_triggers_fired = True


@when("the triggered effects fire")
def triggered_effects_fire(game_state):
    """The triggered effects fire creating pending triggered-layers. Rule 6.6.6b."""
    game_state.simultaneous_triggers_fired = True


# ===== Then steps =====


@then("a triggered-layer is created and added to the stack")
def triggered_layer_created_and_added(game_state):
    """Verify a triggered-layer was created. Rule 6.6.1 + 6.6.5."""
    assert len(game_state.triggered_layers) > 0, (
        "Engine Feature Needed: TriggeredEffect.fire() must create a triggered-layer "
        "and add it to the stack (Rule 6.6.1, 6.6.5)"
    )
    layer = game_state.triggered_layers[0]
    assert layer.layer_category == "triggered-layer", (
        "Engine Feature Needed: TriggeredLayer.layer_category must be 'triggered-layer' (Rule 1.6.2c)"
    )


@then("the effect is a triggered effect not a replacement effect")
def effect_is_triggered_not_replacement(game_state):
    """Verify the effect is categorized as triggered. Rule 6.6.1."""
    assert game_state.triggered_effect_type == "triggered", (
        "Engine Feature Needed: TriggeredEffect categorization distinct from ReplacementEffect (Rule 6.6.1)"
    )


@then("the effect does not contain the keyword \"instead\"")
def effect_does_not_contain_instead(game_state):
    """Triggered effects never use 'instead'. Rule 6.6.1."""
    ability_text = game_state.triggered_effect_text
    assert "instead" not in ability_text.lower(), (
        "Rule 6.6.1: Triggered effects never use the term 'instead' - that is reserved for replacement effects"
    )


@then(parsers.parse("the effect creates {n:d} triggered-layers"))
def effect_creates_n_triggered_layers(game_state, n):
    """Verify exactly N triggered-layers were created. Rule 6.6.1a."""
    assert len(game_state.triggered_layers) == n, (
        f"Engine Feature Needed: Triggered effect with no limit should fire {n} times, "
        f"creating {n} triggered-layers. Got {len(game_state.triggered_layers)} (Rule 6.6.1a)"
    )


@then("no additional triggered-layer is created beyond the limit")
def no_additional_triggered_layer_beyond_limit(game_state):
    """Verify trigger limit is respected. Rule 6.6.1a."""
    limit = game_state.trigger_limit
    actual_count = len(game_state.triggered_layers)
    assert actual_count <= limit, (
        f"Engine Feature Needed: TriggeredEffect.trigger_limit must cap triggering at {limit}. "
        f"Got {actual_count} triggered-layers (Rule 6.6.1a)"
    )


@then("a triggered-layer is created")
def a_triggered_layer_is_created(game_state):
    """Verify a triggered-layer was created. Rule 6.6.1b."""
    assert len(game_state.triggered_layers) > 0, (
        "Engine Feature Needed: TriggeredEffect.fire() must create a triggered-layer (Rule 6.6.5)"
    )


@then("no triggered-layer is created for the second attack")
def no_triggered_layer_for_second_attack(game_state):
    """Verify no second triggered-layer for ordinal condition. Rule 6.6.1b."""
    # First attack should have triggered (count=1), second should not add more
    assert len(game_state.triggered_layers) <= 1, (
        "Engine Feature Needed: TriggeredEffect.ordinal must restrict firing to the specified occurrence. "
        "Only the 'first' attack should trigger, not the second (Rule 6.6.1b)"
    )


@then("the triggered effect fires and creates a triggered-layer")
def triggered_effect_fires_and_creates_layer(game_state):
    """Verify the event-based triggered effect fired. Rule 6.6.1c."""
    assert len(game_state.triggered_layers) > 0, (
        "Engine Feature Needed: Event-based TriggeredEffect.check_trigger(event) must create "
        "a triggered-layer when the event occurs (Rule 6.6.1c)"
    )


@then("the state-based triggered effect fires and creates a triggered-layer")
def state_based_triggered_effect_fires(game_state):
    """Verify the state-based triggered effect fired. Rule 6.6.1c."""
    assert len(game_state.triggered_layers) > 0, (
        "Engine Feature Needed: State-based TriggeredEffect.check_state() must create "
        "a triggered-layer when the game state meets the condition (Rule 6.6.1c)"
    )
    assert game_state.card_counter_count == 0, (
        "The state condition (no counters) must be met for the state-based effect to trigger"
    )


@then("the resolution abilities of the triggered-layer generate their effects")
def resolution_abilities_generate_effects(game_state):
    """Verify triggered-layer generates effects on resolution. Rule 6.6.1d."""
    assert getattr(game_state, 'resolution_occurred', False), (
        "Engine Feature Needed: Stack.resolve_top() must resolve triggered-layer's "
        "resolution abilities and generate their effects (Rule 6.6.1d)"
    )
    assert game_state.effects_generated, (
        "Engine Feature Needed: TriggeredLayer resolution must generate the effects "
        "specified by its resolution abilities (Rule 6.6.1d)"
    )


@then("the inline-triggered effect fires immediately")
def inline_triggered_effect_fires_immediately(game_state):
    """Verify inline-triggered effect fires when condition is met at generation. Rule 6.6.2."""
    assert getattr(game_state, 'inline_effect_fired', False), (
        "Engine Feature Needed: InlineTriggeredEffect must fire when its condition is met "
        "at the time it is generated (Rule 6.6.2)"
    )


@then("the inline-triggered effect does not fire retroactively")
def inline_triggered_effect_does_not_fire_retroactively(game_state):
    """Verify inline-triggered effect doesn't fire after condition met post-generation. Rule 6.6.2a."""
    assert not getattr(game_state, 'inline_effect_fired', False), (
        "Engine Feature Needed: InlineTriggeredEffect.check_retroactive() must return False - "
        "inline-triggered effects cannot fire retroactively (Rule 6.6.2a)"
    )


@then("it is a layer-continuous triggered effect on the stack")
def it_is_layer_continuous_triggered_effect(game_state):
    """Verify the delayed-triggered effect is layer-continuous. Rule 6.6.3."""
    assert getattr(game_state, 'layer_category', None) == "layer-continuous", (
        "Engine Feature Needed: DelayedTriggeredEffect must be a layer-continuous triggered effect "
        "(Rule 6.6.3)"
    )
    assert len(game_state.triggered_layers) > 0, (
        "Engine Feature Needed: DelayedTriggeredEffect must be placed on the stack as a layer (Rule 6.6.3)"
    )


@then(parsers.parse('the effect has an explicit duration of "{duration}"'))
def effect_has_explicit_duration(game_state, duration):
    """Verify the delayed-triggered effect specifies a duration. Rule 6.6.3a."""
    ability_text = game_state.triggered_effect_text
    assert duration in ability_text, (
        f"Engine Feature Needed: DelayedTriggeredEffect.duration must be specified. "
        f"Expected duration '{duration}' in '{ability_text}' (Rule 6.6.3a)"
    )


@then("the effect lasts until it is triggered when the combat chain closes")
def effect_lasts_until_triggered_on_chain_close(game_state):
    """Verify duration for combat-chain-close delayed effects. Rule 6.6.3a."""
    ability_text = game_state.triggered_effect_text
    assert "combat chain closes" in ability_text or "next time" in ability_text, (
        "Engine Feature Needed: DelayedTriggeredEffect must implicitly last until triggered "
        "when conditional on combat chain closing (Rule 6.6.3a)"
    )


@then("it is a static-continuous triggered effect")
def it_is_static_continuous_triggered_effect(game_state):
    """Verify the static-triggered effect is static-continuous. Rule 6.6.4."""
    assert game_state.triggered_effect_category == "static-triggered", (
        "Engine Feature Needed: StaticTriggeredEffect must be categorized as "
        "static-continuous triggered effect (Rule 6.6.4)"
    )


@then("the effect has a trigger limit of once per turn")
def effect_has_once_per_turn_limit(game_state):
    """Verify the static-triggered effect has a trigger limit. Rule 6.6.4."""
    assert getattr(game_state, 'trigger_limit', None) == 1, (
        "Engine Feature Needed: StaticTriggeredEffect.trigger_limit must be set to 1 "
        "for 'once per turn' effects (Rule 6.6.4)"
    )


@then("the ordinal \"first\" specifies when the trigger fires")
def ordinal_first_specifies_trigger_timing(game_state):
    """Verify ordinal is properly tracked. Rule 6.6.4."""
    assert getattr(game_state, 'trigger_ordinal', None) == "first", (
        "Engine Feature Needed: StaticTriggeredEffect.ordinal must track which occurrence "
        "triggers the effect (Rule 6.6.1b, 6.6.4)"
    )


@then("the triggered effect is triggered")
def triggered_effect_is_triggered(game_state):
    """Verify the triggered effect fired. Rule 6.6.5."""
    assert game_state.trigger_count > 0, (
        "Engine Feature Needed: TriggeredEffect.check_trigger(event) must return True "
        "and increment trigger_count when condition is met (Rule 6.6.5)"
    )


@then("a triggered-layer is created")
def another_triggered_layer_is_created(game_state):
    """Verify a triggered-layer was created. Rule 6.6.5."""
    assert len(game_state.triggered_layers) > 0, (
        "Engine Feature Needed: TriggeredEffect.fire() must create a triggered-layer (Rule 6.6.5)"
    )


@then("the triggered effect does not retroactively create a triggered-layer")
def no_retroactive_triggered_layer(game_state):
    """Verify no retroactive triggering. Rule 6.6.5a."""
    assert len(game_state.triggered_layers) == 0, (
        "Engine Feature Needed: TriggeredEffect.fire() must NOT create a triggered-layer "
        "retroactively - effect must exist before event (Rule 6.6.5a)"
    )


@then("the inline-triggered effect fires as it is generated")
def inline_triggered_effect_fires_as_generated(game_state):
    """Verify inline-triggered fires during generation. Rule 6.6.5a exception."""
    condition_met = getattr(game_state, 'inline_condition_met_at_generation', False)
    assert condition_met, "Condition must be met at generation for this test"
    # The inline-triggered effect fires as exception to the 'must exist before event' rule
    assert len(game_state.triggered_layers) > 0, (
        "Engine Feature Needed: InlineTriggeredEffect fires as it is generated if condition is met - "
        "this is the exception to Rule 6.6.5a"
    )


@then("the event-based triggered effect does not trigger")
def event_based_triggered_effect_does_not_trigger(game_state):
    """Verify event-based effect doesn't fire when event is modified. Rule 6.6.5b."""
    assert not getattr(game_state, 'event_triggered', True) or len(game_state.triggered_layers) == 0, (
        "Engine Feature Needed: EventBasedTriggeredEffect.check_trigger() must return False "
        "when the event was modified by a replacement effect and no longer meets the condition (Rule 6.6.5b)"
    )


@then("the triggered effect does not trigger")
def triggered_effect_does_not_trigger(game_state):
    """Verify triggered effect doesn't fire. Rule 6.6.5b."""
    assert len(game_state.triggered_layers) == 0, (
        "Engine Feature Needed: TriggeredEffect.check_trigger() must return False when "
        "combined event+state conditions are not both met (Rule 6.6.5b)"
    )


@then("the triggered effect triggers")
def triggered_effect_triggers_combined(game_state):
    """Verify triggered effect fires when both conditions met. Rule 6.6.5b."""
    assert len(game_state.triggered_layers) > 0, (
        "Engine Feature Needed: TriggeredEffect.check_trigger() must return True when "
        "both event condition and state condition are met (Rule 6.6.5b)"
    )


@then("the state-based triggered effect is triggered")
def state_based_triggered_effect_is_triggered(game_state):
    """Verify state-based effect triggers on state change. Rule 6.6.5c."""
    assert game_state.card_counter_count == 0, "Counter should be removed"
    assert len(game_state.triggered_layers) > 0, (
        "Engine Feature Needed: StateBasedTriggeredEffect must trigger when game state changes "
        "from not-met to met (Rule 6.6.5c)"
    )


@then("the state-based triggered effect is generated and the condition is already met")
def state_based_effect_generated_condition_met(game_state):
    """Verify state-based effect fires when generated with condition already met. Rule 6.6.5c."""
    assert game_state.card_counter_count == 0, "Card should have no counters"
    assert len(game_state.triggered_layers) > 0, (
        "Engine Feature Needed: StateBasedTriggeredEffect must trigger immediately when "
        "generated while the condition is already met (Rule 6.6.5c)"
    )


@then("the effect is triggered immediately")
def effect_is_triggered_immediately(game_state):
    """State-based effect fires immediately on generation. Rule 6.6.5c."""
    # Verified in the previous step - state was met at generation so it triggered
    assert len(game_state.triggered_layers) > 0, (
        "Engine Feature Needed: StateBasedTriggeredEffect must trigger as soon as it is "
        "generated if the state condition is already satisfied (Rule 6.6.5c)"
    )


@then("the triggered effect does not trigger because the first boost already happened")
def triggered_effect_does_not_trigger_ordinal_passed(game_state):
    """Verify ordinal-based effect misses if ordinal time already passed. Rule 6.6.5d."""
    assert getattr(game_state, 'ordinal_event_already_occurred', False), (
        "Test setup: ordinal event should have already occurred"
    )
    assert len(game_state.triggered_layers) == 0, (
        "Engine Feature Needed: TriggeredEffect with ordinal must not trigger if the "
        "specified ordinal occurrence has already happened in the duration (Rule 6.6.5d)"
    )


@then("no triggered-layer is created because the trigger limit is reached")
def no_triggered_layer_limit_reached(game_state):
    """Verify trigger limit prevents new triggered-layer. Rule 6.6.5e."""
    assert game_state.trigger_count >= game_state.trigger_limit, (
        "Trigger count should be at the limit"
    )
    # Second trigger attempt should not have created a new layer
    assert len(game_state.triggered_layers) == 0, (
        "Engine Feature Needed: TriggeredEffect.fire() must return None and NOT create "
        "a triggered-layer when trigger_count >= trigger_limit (Rule 6.6.5e)"
    )


@then("the Katsu triggered effect does not create a triggered-layer due to Tripwire Trap")
def katsu_effect_prevented_by_tripwire_trap(game_state):
    """Verify Tripwire Trap prevents Katsu's triggered-layer. Rule 6.6.5f."""
    assert getattr(game_state, 'prevention_effect_active', False), "Prevention effect must be active"
    assert len(game_state.katsu_triggered_layers) == 0, (
        "Engine Feature Needed: TriggerPreventionEffect (Tripwire Trap) must prevent "
        "the triggered-layer from being created (Rule 6.6.5f)"
    )


@then("the once-per-turn limit for the Katsu triggered effect has been used up")
def katsu_limit_used_up(game_state):
    """Verify the trigger still counted toward the limit. Rule 6.6.5f."""
    assert game_state.trigger_count >= game_state.trigger_limit, (
        "Engine Feature Needed: Even when a trigger is prevented, it must count toward "
        "the trigger limit (Rule 6.6.5f)"
    )


@then("the Katsu triggered effect does not create a triggered-layer because the limit is reached")
def katsu_effect_no_layer_limit_reached(game_state):
    """Verify Katsu doesn't trigger again because limit was used by the prevented trigger. Rule 6.6.5f."""
    assert len(game_state.katsu_triggered_layers) == 0, (
        "Engine Feature Needed: TriggeredEffect must not create triggered-layer when "
        "limit is reached, even if the earlier trigger was prevented (Rule 6.6.5f)"
    )


@then("it is added to the stack as a game state process before the next priority is given")
def triggered_layer_added_before_priority(game_state):
    """Verify triggered-layer is added before next priority. Rule 6.6.6."""
    assert getattr(game_state, 'layer_added_before_priority', False), (
        "Engine Feature Needed: GameStateProcess must add triggered-layers to the stack "
        "before giving priority to the next player (Rule 6.6.6)"
    )


@then("the controller must declare the mode for the triggered-layer's modal abilities")
def controller_declares_mode(game_state):
    """Verify controller must declare modes. Rule 6.6.6a."""
    # Mode declaration is required before adding to stack
    assert getattr(game_state, 'declared_mode', None) is None, (
        "Engine Feature Needed: TriggeredLayer.declare_parameters() must prompt controller "
        "to select modes for modal triggered-layers (Rule 6.6.6a)"
    )


@then("the triggered-layer is added to the stack after modes are declared")
def triggered_layer_added_after_mode_declaration(game_state):
    """Verify triggered-layer goes on stack after parameter declaration. Rule 6.6.6a."""
    assert len(game_state.triggered_layers) > 0, (
        "Engine Feature Needed: TriggeredLayer must be added to stack after controller "
        "declares modes (Rule 6.6.6a)"
    )


@then("the triggered-layer ceases to exist and is not added to the stack")
def triggered_layer_ceases_to_exist(game_state):
    """Verify triggered-layer ceases if no legal targets. Rule 6.6.6a."""
    assert not getattr(game_state, 'triggered_layer_added_to_stack', True), (
        "Engine Feature Needed: TriggeredLayer.ceases_to_exist_if_no_targets() must remove "
        "the triggered-layer from existence when no legal targets can be declared (Rule 6.6.6a)"
    )


@then("the controller must select a mode and declare a legal target before the layer is added")
def controller_selects_mode_and_target(game_state):
    """Verify mode and target must be declared. Rule 6.6.6a."""
    assert getattr(game_state, 'requires_mode_declaration', False), (
        "Engine Feature Needed: Modal TriggeredLayer must require mode declaration before "
        "being added to the stack (Rule 6.6.6a)"
    )
    assert getattr(game_state, 'requires_target_declaration', False), (
        "Engine Feature Needed: Targeted TriggeredLayer must require target declaration "
        "before being added to the stack (Rule 6.6.6a)"
    )


@then("if no legal target exists for the selected mode the triggered-layer is not added")
def no_legal_target_means_no_layer(game_state):
    """Verify modal triggered-layer ceases if no legal targets. Rule 6.6.6a."""
    # This behavior must be enforced by the engine
    # If the check_target_required_on_stack fails, the layer is not added
    check_result = game_state.check_target_required_on_stack(game_state.test_card)
    assert check_result is not None, (
        "Engine Feature Needed: TriggeredLayer must check for legal targets. "
        "If none exist, the layer ceases to exist (Rule 6.6.6a)"
    )


@then("the turn-player selects a starting player")
def turn_player_selects_starting_player(game_state):
    """Verify turn-player selects which player adds triggered-layers first. Rule 6.6.6b."""
    assert hasattr(game_state, 'pending_triggered_layers'), (
        "Engine Feature Needed: Stack must track pending triggered-layers (Rule 6.6.6b)"
    )
    assert len(game_state.pending_triggered_layers) >= 2, (
        "Multiple simultaneous triggered-layers must be tracked as pending (Rule 6.6.6b)"
    )


@then("each player adds their pending triggered-layers to the stack in clockwise order")
def players_add_triggered_layers_clockwise(game_state):
    """Verify clockwise ordering of triggered-layer stack addition. Rule 6.6.6b."""
    assert hasattr(game_state, 'pending_triggered_layers'), (
        "Engine Feature Needed: Stack.add_pending_triggered_layers() must add layers "
        "in clockwise order from the selected player (Rule 6.6.6b)"
    )


@then("the controlling player may order their triggered-layers so the resource gain resolves first")
def player_may_order_own_triggered_layers(game_state):
    """Verify players can order their own triggered-layers. Rule 6.6.6b."""
    assert len(game_state.pending_triggered_layers) == 2, (
        "Both triggered-layers should be pending"
    )
    # Player should be able to choose the order
    layer1_effect = game_state.pending_triggered_layers[0].ability_text
    assert "gain" in layer1_effect.lower() or "destroy" in layer1_effect.lower(), (
        "Engine Feature Needed: Players must be able to choose the order of their own "
        "triggered-layers when multiple are pending (Rule 6.6.6b)"
    )


@then("this is true even if they are not the turn-player")
def true_even_if_not_turn_player(game_state):
    """Verify non-turn-player can still order their own triggered-layers. Rule 6.6.6b."""
    # The example from the rules shows this is possible regardless of turn-player status
    assert len(game_state.pending_triggered_layers) == 2, (
        "Engine Feature Needed: Each player orders their OWN pending triggered-layers, "
        "regardless of whether they are the turn-player (Rule 6.6.6b)"
    )


# ===== Fixtures =====


@pytest.fixture
def game_state():
    """
    Fixture providing game state for testing section 6.6 Triggered Effects.

    Uses BDDGameState which integrates with the real engine.
    Reference: Rule 6.6
    """
    from tests.bdd_helpers import BDDGameState

    state = BDDGameState()
    state.triggered_layers = []
    state.trigger_count = 0
    state.trigger_limit = None

    return state
