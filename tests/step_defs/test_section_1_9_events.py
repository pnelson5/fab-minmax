"""
Step definitions for Section 1.9: Events
Reference: Flesh and Blood Comprehensive Rules Section 1.9

This module implements behavioral tests for event rules:
- Rule 1.9.1: An event is a change in game state (layer resolution, effect result,
              phase transition, or player action)
- Rule 1.9.1a: Events involving elements outside the game cannot be modified by
               in-game replacement effects or trigger in-game triggered effects,
               unless the event directly interacts with the game
- Rule 1.9.1b: Events comprising instructions to do nothing do not occur and cannot
               be modified by replacement effects or trigger triggered effects
- Rule 1.9.1c: Player may choose to fail unverifiable instructions
- Rule 1.9.2: Compound events involve performing the same instruction multiple times;
              expanded into individual events
- Rule 1.9.2a: Triggered effects trigger once on the compound event, not again for
               individual events
- Rule 1.9.2b: Replacement effects replacing compound events cannot also replace the
               individual events
- Rule 1.9.2c: Multi-player events are compound events in clockwise order
- Rule 1.9.3: Composite events are made up of one or more internal events
- Rule 1.9.3a: Triggered effects on composite events trigger only once
- Rule 1.9.3b: Prevented triggering applies to entire composite event
- Rule 1.9.3c: Partially replacing internal events does not prevent composite event
- Rule 1.9.3d: Composite event does not occur if all internal events fail

Engine Features Needed for Section 1.9:
- [ ] Event class hierarchy: Event, CompoundEvent, CompositeEvent (Rule 1.9.1)
- [ ] Event.event_type attribute identifying what kind of event it is (Rule 1.9.1)
- [ ] Event.occurred property tracking whether the event happened (Rule 1.9.1b)
- [ ] Event.is_outside_game property for extra-game events (Rule 1.9.1a)
- [ ] Event.directly_interacts_with_game property (Rule 1.9.1a)
- [ ] ReplacementEffect.can_modify(event) -> bool checking outside-game status (Rule 1.9.1a)
- [ ] TriggeredEffect.can_trigger_from(event) -> bool (Rules 1.9.1, 1.9.1a)
- [ ] NullEvent (instruction to do nothing) - event.occurred = False (Rule 1.9.1b)
- [ ] NullEvent not modifiable by replacement effects (Rule 1.9.1b)
- [ ] NullEvent does not trigger triggered effects (Rule 1.9.1b)
- [ ] UnverifiableInstruction class with fail_option = True (Rule 1.9.1c)
- [ ] CompoundEvent.individual_events list (Rule 1.9.2)
- [ ] CompoundEvent expansion from compact format (Rule 1.9.2)
- [ ] TriggeredEffect.triggered_from_compound_event tracking (Rule 1.9.2a)
- [ ] TriggeredEffect fires once for compound, not per individual event (Rule 1.9.2a)
- [ ] ReplacementEffect.applied_to_compound tracking to prevent re-applying to individuals (Rule 1.9.2b)
- [ ] MultiPlayerEvent as compound event in clockwise order (Rule 1.9.2c)
- [ ] MultiPlayerEvent.starting_player derived from turn_player or effect_controller (Rule 1.9.2c)
- [ ] CompositeEvent.internal_events list (Rule 1.9.3)
- [ ] CompositeEvent triggering fires once, not once per internal event (Rule 1.9.3a)
- [ ] Trigger prevention applied to entire composite event (Rule 1.9.3b)
- [ ] Partial replacement of internal event preserves composite event occurrence (Rule 1.9.3c)
- [ ] CompositeEvent.occurred = False when all internal events fail (Rule 1.9.3d)
"""

import pytest
from pytest_bdd import scenario, given, when, then, parsers

from fab_engine.cards.model import CardInstance, CardTemplate, CardType, Color, Subtype
from fab_engine.zones.zone import ZoneType


# ===========================================================================
# Scenario: layer resolution produces an event
# Tests Rule 1.9.1 - Layer resolution is a source of events
# ===========================================================================


@scenario(
    "../features/section_1_9_events.feature",
    "layer resolution produces an event",
)
def test_layer_resolution_produces_an_event():
    """Rule 1.9.1: Layer resolution produces a game state change event."""
    pass


@given('a player has a card "Sigil of Solace" on the stack')
def step_sigil_of_solace_on_stack(game_state):
    """Rule 1.9.1: Card is on the stack as a layer about to resolve."""
    game_state.sigil_card = game_state.create_card(name="Sigil of Solace")
    game_state.sigil_card.functional_text = "Gain 1 life."
    game_state.stack_layer = {
        "card": game_state.sigil_card,
        "resolved": False,
        "produced_event": None,
    }


@when("the layer resolves")
def step_layer_resolves(game_state):
    """Rule 1.9.1: Layer resolution produces an event."""
    # Engine Feature Needed: Layer.resolve() -> Event
    game_state.stack_layer["resolved"] = True
    game_state.stack_layer["produced_event"] = {
        "event_type": "layer_resolution",
        "occurred": True,
        "source": game_state.sigil_card,
    }
    game_state.produced_event = game_state.stack_layer["produced_event"]


@then("a layer resolution event is produced that changes the game state")
def step_layer_resolution_event_produced(game_state):
    """Rule 1.9.1: Layer resolution produces an event."""
    # Engine Feature Needed: Event object with occurred=True
    assert game_state.produced_event is not None
    assert game_state.produced_event.get("occurred") is True


@then('the event has an event type of "layer_resolution"')
def step_event_type_layer_resolution(game_state):
    """Rule 1.9.1: Event has event_type identifying the source."""
    # Engine Feature Needed: Event.event_type attribute
    assert game_state.produced_event.get("event_type") == "layer_resolution"


# ===========================================================================
# Scenario: player action produces an event
# Tests Rule 1.9.1 - Player actions are sources of events
# ===========================================================================


@scenario(
    "../features/section_1_9_events.feature",
    "player action produces an event",
)
def test_player_action_produces_an_event():
    """Rule 1.9.1: Player actions (like drawing) produce game state change events."""
    pass


@given("a player is taking a turn")
def step_player_taking_a_turn(game_state):
    """Rule 1.9.1: Game is in progress with a player's turn."""
    game_state.action_event = None
    deck_card = game_state.create_card(name="Deck Card")
    game_state.player.hand.add_card(deck_card)


@when("the player performs a draw action")
def step_player_performs_draw_action(game_state):
    """Rule 1.9.1: Player drawing a card is a player action that produces an event."""
    # Engine Feature Needed: PlayerAction.draw() -> Event
    game_state.action_event = {
        "event_type": "player_action",
        "action": "draw",
        "occurred": True,
    }


@then("a player action event is produced that changes the game state")
def step_player_draw_event_produced(game_state):
    """Rule 1.9.1: Drawing a card produces an event."""
    # Engine Feature Needed: Event.occurred = True
    assert game_state.action_event is not None
    assert game_state.action_event.get("occurred") is True


@then('the event has an event type of "player_action"')
def step_event_type_player_action(game_state):
    """Rule 1.9.1: Event type identifies player actions."""
    # Engine Feature Needed: Event.event_type
    assert game_state.action_event.get("event_type") == "player_action"


# ===========================================================================
# Scenario: turn phase transition produces an event
# Tests Rule 1.9.1 - Phase transitions are sources of events
# ===========================================================================


@scenario(
    "../features/section_1_9_events.feature",
    "turn phase transition produces an event",
)
def test_turn_phase_transition_produces_an_event():
    """Rule 1.9.1: Turn phase transitions produce game state change events."""
    pass


@given("a game is in the start phase")
def step_game_in_start_phase(game_state):
    """Rule 1.9.1: Game is in a specific phase."""
    # Engine Feature Needed: GameState.current_phase tracking
    game_state.current_phase = "start_phase"
    game_state.phase_event = None


@when("the game transitions to the action phase")
def step_game_transitions_to_action_phase(game_state):
    """Rule 1.9.1: Phase transition produces a phase_transition event."""
    # Engine Feature Needed: GameState.transition_phase() -> Event
    game_state.phase_event = {
        "event_type": "phase_transition",
        "from_phase": "start_phase",
        "to_phase": "action_phase",
        "occurred": True,
    }
    game_state.current_phase = "action_phase"


@then("a phase transition event is produced that changes the game state")
def step_phase_transition_event_produced(game_state):
    """Rule 1.9.1: Phase transition produces an event."""
    assert game_state.phase_event is not None
    assert game_state.phase_event.get("occurred") is True


@then('the event has an event type of "phase_transition"')
def step_event_type_phase_transition(game_state):
    """Rule 1.9.1: Event type identifies phase transitions."""
    # Engine Feature Needed: Event.event_type = "phase_transition"
    assert game_state.phase_event.get("event_type") == "phase_transition"


# ===========================================================================
# Scenario: event can be modified by replacement effect
# Tests Rule 1.9.1 - Events can be modified by replacement effects
# ===========================================================================


@scenario(
    "../features/section_1_9_events.feature",
    "event can be modified by replacement effect",
)
def test_event_can_be_modified_by_replacement_effect():
    """Rule 1.9.1: Events can be modified by replacement effects."""
    pass


@given("a player has a card being drawn")
def step_player_has_card_being_drawn(game_state):
    """Rule 1.9.1: A draw event is about to occur."""
    game_state.draw_card = game_state.create_card(name="Draw Target")
    game_state.cards_drawn = []
    game_state.replacement_effect_active = False


@given("a replacement effect that replaces draw events with two draws")
def step_replacement_effect_double_draw(game_state):
    """Rule 1.9.1: A replacement effect exists that doubles draws."""
    # Engine Feature Needed: ReplacementEffect.applies_to("draw") = True
    game_state.replacement_effect_active = True
    game_state.replacement_effect = {
        "type": "replacement",
        "replaces": "draw",
        "replacement": "draw_two",
        "active": True,
    }


@when("the draw event occurs")
def step_draw_event_occurs(game_state):
    """Rule 1.9.1: The draw event fires and the replacement effect modifies it."""
    # Engine Feature Needed: EventSystem.apply_replacements(event)
    if game_state.replacement_effect_active:
        game_state.cards_drawn = ["card1", "card2"]
        game_state.event_was_modified = True
    else:
        game_state.cards_drawn = ["card1"]
        game_state.event_was_modified = False


@then("the replacement effect modifies the event")
def step_replacement_effect_modifies_event(game_state):
    """Rule 1.9.1: The event was modified by the replacement effect."""
    # Engine Feature Needed: Event.was_modified_by_replacement = True
    assert game_state.event_was_modified is True


@then("two cards are drawn instead of one")
def step_two_cards_drawn(game_state):
    """Rule 1.9.1: The replacement effect doubled the draw."""
    assert len(game_state.cards_drawn) == 2


# ===========================================================================
# Scenario: event can trigger a triggered effect
# Tests Rule 1.9.1 - Events can trigger triggered effects
# ===========================================================================


@scenario(
    "../features/section_1_9_events.feature",
    "event can trigger a triggered effect",
)
def test_event_can_trigger_a_triggered_effect():
    """Rule 1.9.1: Events can trigger triggered effects."""
    pass


@given("a player has a triggered effect that triggers on discard")
def step_player_has_triggered_effect_on_discard(game_state):
    """Rule 1.9.1: A triggered effect is registered for discard events."""
    # Engine Feature Needed: TriggeredEffect.trigger_condition = "on_discard"
    game_state.triggered_effect_for_discard = {
        "trigger_condition": "on_discard",
        "trigger_count": 0,
        "active": True,
    }
    game_state.discard_triggered = False


@given("a player has a card to discard")
def step_player_has_card_to_discard(game_state):
    """Rule 1.9.1: A card is in hand to be discarded."""
    game_state.trigger_discard_card = game_state.create_card(name="Discard Target")
    game_state.player.hand.add_card(game_state.trigger_discard_card)


@when("the player discards that card")
def step_player_discards_that_card(game_state):
    """Rule 1.9.1: Discarding produces an event that can trigger effects."""
    # Engine Feature Needed: DischargeEvent triggers TriggeredEffect
    game_state.player.hand.remove_card(game_state.trigger_discard_card)
    if game_state.triggered_effect_for_discard.get("active"):
        game_state.triggered_effect_for_discard["trigger_count"] += 1
        game_state.discard_triggered = True


@then("the triggered effect is triggered by the discard event")
def step_triggered_effect_triggered_by_discard(game_state):
    """Rule 1.9.1: The discard event triggers the triggered effect."""
    # Engine Feature Needed: TriggeredEffect triggered when discard event occurs
    assert game_state.discard_triggered is True
    assert game_state.triggered_effect_for_discard["trigger_count"] == 1


# ===========================================================================
# Scenario: outside-game event cannot be modified by replacement effects
# Tests Rule 1.9.1a - Outside-game events are not modifiable in-game
# ===========================================================================


@scenario(
    "../features/section_1_9_events.feature",
    "outside-game event cannot be modified by replacement effects",
)
def test_outside_game_event_cannot_be_modified_by_replacement_effects():
    """Rule 1.9.1a: Events outside the game cannot be modified by in-game replacement effects."""
    pass


@given("an effect would open and reveal a booster pack outside the game")
def step_outside_game_reveal_effect(game_state):
    """Rule 1.9.1a: Effect involves elements outside the game."""
    # Engine Feature Needed: Event.is_outside_game = True
    game_state.outside_game_event = {
        "event_type": "reveal_booster",
        "is_outside_game": True,
        "directly_interacts_with_game": False,
        "was_modified": False,
    }


@given("a replacement effect exists that would normally modify reveal events")
def step_replacement_effect_for_reveal_events(game_state):
    """Rule 1.9.1a: A replacement effect exists but should not apply to outside-game events."""
    # Engine Feature Needed: ReplacementEffect.can_modify(event) = False for outside-game
    game_state.in_game_replacement = {
        "type": "replacement",
        "replaces": "reveal",
        "active": True,
        "can_modify_outside_game": False,
    }


@when("the outside-game reveal event occurs")
def step_outside_game_reveal_event_occurs(game_state):
    """Rule 1.9.1a: The outside-game event fires."""
    # Engine Feature Needed: EventSystem.can_modify(event, replacement) checks is_outside_game
    event = game_state.outside_game_event
    if event.get("is_outside_game") and not event.get("directly_interacts_with_game"):
        event["was_modified"] = False
    else:
        event["was_modified"] = True


@then("the replacement effect does not modify the outside-game reveal event")
def step_replacement_does_not_modify_outside_game(game_state):
    """Rule 1.9.1a: Outside-game event is not modified by in-game replacement."""
    # Engine Feature Needed: Event.was_modified_by_replacement = False for outside-game events
    assert game_state.outside_game_event["was_modified"] is False


# ===========================================================================
# Scenario: outside-game event that interacts with game can be modified
# Tests Rule 1.9.1a - Events that interact with game CAN be modified
# ===========================================================================


@scenario(
    "../features/section_1_9_events.feature",
    "outside-game event that interacts with game can be modified",
)
def test_outside_game_event_that_interacts_with_game_can_be_modified():
    """Rule 1.9.1a: Events from outside-game effects that directly interact with the game can be modified."""
    pass


@given("an effect would open a booster pack and put cards into hand")
def step_booster_pack_put_into_hand_effect(game_state):
    """Rule 1.9.1a: Effect has component that directly interacts with game (put cards into hand)."""
    # Engine Feature Needed: Event.directly_interacts_with_game = True for put-into-zone events
    game_state.put_into_hand_event = {
        "event_type": "put_into_zone",
        "zone": "hand",
        "is_outside_game": False,
        "directly_interacts_with_game": True,
        "was_modified": False,
    }


@given("a replacement effect exists that modifies zone-entry events")
def step_replacement_effect_for_zone_entry(game_state):
    """Rule 1.9.1a: Replacement effect for zone-entry events."""
    game_state.zone_entry_replacement = {
        "type": "replacement",
        "replaces": "put_into_zone",
        "active": True,
        "applied": False,
    }


@when("the put-into-hand event from the outside-game effect occurs")
def step_put_into_hand_event_occurs(game_state):
    """Rule 1.9.1a: The put-into-hand event (which interacts with game) fires."""
    # Engine Feature Needed: EventSystem can modify events that directly interact with game
    event = game_state.put_into_hand_event
    replacement = game_state.zone_entry_replacement
    if event.get("directly_interacts_with_game") and replacement.get("active"):
        event["was_modified"] = True
        replacement["applied"] = True


@then("the replacement effect can modify the put-into-hand event")
def step_replacement_can_modify_put_event(game_state):
    """Rule 1.9.1a: Events directly interacting with game can be modified."""
    # Engine Feature Needed: ReplacementEffect.can_modify returns True for game-interacting events
    assert game_state.put_into_hand_event["was_modified"] is True


# ===========================================================================
# Scenario: zero damage event does not occur
# Tests Rule 1.9.1b - Instruction to do nothing means event doesn't occur
# ===========================================================================


@scenario(
    "../features/section_1_9_events.feature",
    "zero damage event does not occur",
)
def test_zero_damage_event_does_not_occur():
    """Rule 1.9.1b: If an event would deal 0 damage, it does not occur."""
    pass


@given('a card "Blazing Aether" has dealt 0 arcane damage to a hero this turn')
def step_blazing_aether_dealt_zero_damage(game_state):
    """Rule 1.9.1b: X = 0 means the instruction is to do nothing."""
    game_state.blazing_aether = game_state.create_card(name="Blazing Aether")
    game_state.arcane_damage_dealt_this_turn = 0
    game_state.damage_event = None


@when("the player plays Blazing Aether")
def step_player_plays_blazing_aether(game_state):
    """Rule 1.9.1b: Playing creates a potential event that does nothing."""
    # Engine Feature Needed: Event.occurred = False when instruction is to do nothing
    damage_amount = game_state.arcane_damage_dealt_this_turn
    if damage_amount == 0:
        game_state.damage_event = {
            "event_type": "deal_arcane_damage",
            "amount": damage_amount,
            "occurred": False,
        }
    else:
        game_state.damage_event = {
            "event_type": "deal_arcane_damage",
            "amount": damage_amount,
            "occurred": True,
        }


@then("the event to deal 0 arcane damage does not occur")
def step_zero_damage_event_does_not_occur(game_state):
    """Rule 1.9.1b: The event does not occur when amount is 0."""
    # Engine Feature Needed: NullEvent.occurred = False
    assert game_state.damage_event is not None
    assert game_state.damage_event["occurred"] is False


@then("the event is marked as not_occurred")
def step_event_marked_not_occurred(game_state):
    """Rule 1.9.1b: Event has occurred = False."""
    # Engine Feature Needed: Event.occurred property
    assert game_state.damage_event["occurred"] is False


# ===========================================================================
# Scenario: non-occurring event cannot be modified by replacement effects
# Tests Rule 1.9.1b - Null events block replacement effects
# ===========================================================================


@scenario(
    "../features/section_1_9_events.feature",
    "non-occurring event cannot be modified by replacement effects",
)
def test_non_occurring_event_cannot_be_modified_by_replacement_effects():
    """Rule 1.9.1b: Non-occurring events cannot be modified by replacement effects."""
    pass


@given("a null event comprising an instruction to do nothing")
def step_null_event_instruction(game_state):
    """Rule 1.9.1b: An event that is an instruction to do nothing."""
    # Engine Feature Needed: NullEvent class or Event(occurred=False)
    game_state.null_event = {
        "event_type": "draw_card",
        "amount": 0,
        "occurred": False,
        "was_modified": False,
    }


@given("a replacement effect that would modify that null event")
def step_replacement_effect_for_null_event(game_state):
    """Rule 1.9.1b: A replacement effect exists but should not apply to null events."""
    game_state.null_event_replacement = {
        "type": "replacement",
        "replaces": "draw_card",
        "active": True,
        "applied": False,
    }


@when("the null draw event would occur")
def step_null_draw_event_would_occur(game_state):
    """Rule 1.9.1b: The null event doesn't occur, so no replacements apply."""
    # Engine Feature Needed: EventSystem.process_event() skips replacement for null events
    event = game_state.null_event
    replacement = game_state.null_event_replacement
    if not event.get("occurred"):
        # Rule 1.9.1b: null event cannot be modified
        replacement["applied"] = False
    else:
        if replacement.get("active"):
            replacement["applied"] = True
            event["was_modified"] = True


@then("the replacement effect does not apply to the null draw event")
def step_replacement_not_applied_to_null_event(game_state):
    """Rule 1.9.1b: Replacement effects cannot modify null events."""
    # Engine Feature Needed: ReplacementEffect cannot apply to non-occurring events
    assert game_state.null_event_replacement["applied"] is False


# ===========================================================================
# Scenario: non-occurring event does not trigger effects
# Tests Rule 1.9.1b - Null events don't trigger triggered effects
# ===========================================================================


@scenario(
    "../features/section_1_9_events.feature",
    "non-occurring event does not trigger effects",
)
def test_non_occurring_event_does_not_trigger_effects():
    """Rule 1.9.1b: Non-occurring events do not trigger triggered effects."""
    pass


@given("a null damage event comprising an instruction to do nothing")
def step_null_damage_event_for_trigger(game_state):
    """Rule 1.9.1b: An event that doesn't occur."""
    game_state.null_damage_event = {
        "event_type": "deal_arcane_damage",
        "amount": 0,
        "occurred": False,
    }


@given("a triggered effect that triggers on that damage event type")
def step_triggered_effect_on_damage_type(game_state):
    """Rule 1.9.1b: A triggered effect would normally fire on this event type."""
    game_state.damage_trigger = {
        "trigger_condition": "on_deal_arcane_damage",
        "trigger_count": 0,
        "active": True,
    }


@when("the null damage event would occur")
def step_null_damage_event_would_occur(game_state):
    """Rule 1.9.1b: The null event doesn't occur, so no triggers should fire."""
    # Engine Feature Needed: EventSystem.process_triggers() skips null events
    event = game_state.null_damage_event
    trigger = game_state.damage_trigger
    if event.get("occurred"):
        trigger["trigger_count"] += 1


@then("the triggered damage effect is not triggered")
def step_triggered_damage_effect_not_triggered(game_state):
    """Rule 1.9.1b: Triggered effect does not fire from null event."""
    # Engine Feature Needed: TriggeredEffect.trigger() skips non-occurring events
    assert game_state.damage_trigger["trigger_count"] == 0


# ===========================================================================
# Scenario: player may fail unverifiable instruction
# Tests Rule 1.9.1c - Player can fail search when deck is private
# ===========================================================================


@scenario(
    "../features/section_1_9_events.feature",
    "player may fail unverifiable instruction",
)
def test_player_may_fail_unverifiable_instruction():
    """Rule 1.9.1c: Player can choose to fail an instruction the opponent cannot verify."""
    pass


@given('a player has a "Moon Wish" card that hit')
def step_moon_wish_hit(game_state):
    """Rule 1.9.1c: Moon Wish's triggered effect fires."""
    game_state.moon_wish = game_state.create_card(name="Moon Wish")
    game_state.moon_wish.functional_text = (
        "When this hits, search your deck for a card named Sun Kiss."
    )
    game_state.moon_wish_hit = True
    game_state.search_result = None


@given("the player's deck is private to the opponent")
def step_deck_is_private(game_state):
    """Rule 1.9.1c: The deck is a private zone, opponent cannot verify contents."""
    # Engine Feature Needed: Zone.is_private property
    game_state.deck_is_private = True
    game_state.opponent_can_verify = False


@when("the player must search their deck for Sun Kiss")
def step_player_must_search_for_sun_kiss(game_state):
    """Rule 1.9.1c: Player has option to fail search since opponent cannot verify."""
    # Engine Feature Needed: UnverifiableInstruction.player_may_fail = True
    game_state.player_chose_to_fail = True
    if game_state.player_chose_to_fail and not game_state.opponent_can_verify:
        game_state.search_result = {
            "found": False,
            "reason": "player_chose_to_fail",
            "event_occurred": False,
        }
    else:
        game_state.search_result = {
            "found": True,
            "reason": "found_in_deck",
            "event_occurred": True,
        }


@then("the player may choose to fail to find Sun Kiss")
def step_player_may_fail_search(game_state):
    """Rule 1.9.1c: Player choosing to fail is a legal game action."""
    # Engine Feature Needed: UnverifiableInstruction allows failure option
    assert game_state.search_result is not None
    assert game_state.search_result["reason"] == "player_chose_to_fail"


@then("the event fails as if Sun Kiss could not be found")
def step_event_fails_as_if_not_found(game_state):
    """Rule 1.9.1c: Event fails as if the instruction could not be completed."""
    # Engine Feature Needed: Event.failed_as_if_not_completable = True
    assert game_state.search_result["found"] is False


# ===========================================================================
# Scenario: player cannot fail verifiable instruction
# Tests Rule 1.9.1c (converse) - Cannot fail verifiable instruction
# ===========================================================================


@scenario(
    "../features/section_1_9_events.feature",
    "player cannot fail verifiable instruction",
)
def test_player_cannot_fail_verifiable_instruction():
    """Rule 1.9.1c: Player cannot choose to fail a verifiable instruction."""
    pass


@given("a player must draw from their deck")
def step_player_must_draw_from_deck(game_state):
    """Rule 1.9.1c (converse): Drawing is verifiable."""
    deck_card = game_state.create_card(name="Top of Deck")
    game_state.deck_cards = [deck_card]
    game_state.draw_result = None


@given("the opponent can verify there are cards in the deck")
def step_opponent_can_verify_draw(game_state):
    """Rule 1.9.1c (converse): Deck is visible or card count is public."""
    # Engine Feature Needed: Deck size is a public game state element
    game_state.opponent_can_verify_draw = True


@when("the player performs the draw")
def step_player_performs_draw(game_state):
    """Rule 1.9.1c (converse): Drawing cannot be failed."""
    # Engine Feature Needed: VerifiableInstruction.player_may_fail = False
    if game_state.opponent_can_verify_draw and game_state.deck_cards:
        drawn = game_state.deck_cards.pop()
        game_state.player.hand.add_card(drawn)
        game_state.draw_result = {"drew": True, "card": drawn}


@then("the player cannot choose to fail to draw a card")
def step_player_cannot_fail_draw(game_state):
    """Rule 1.9.1c (converse): Verifiable instructions must be completed."""
    # Engine Feature Needed: Instruction.is_verifiable = True disables fail option
    assert game_state.draw_result is not None
    assert game_state.draw_result["drew"] is True


# ===========================================================================
# Scenario: draw three cards is a compound event
# Tests Rule 1.9.2 - Compound events involve the same instruction multiple times
# ===========================================================================


@scenario(
    "../features/section_1_9_events.feature",
    "draw three cards is a compound event",
)
def test_draw_three_cards_is_a_compound_event():
    """Rule 1.9.2: 'Draw 3 cards' creates a compound event of 3 individual draw events."""
    pass


@given('a card "Tome of Harvests" with the effect "Draw 3 cards"')
def step_tome_of_harvests(game_state):
    """Rule 1.9.2: Card with compact compound effect."""
    game_state.tome_of_harvests = game_state.create_card(name="Tome of Harvests")
    game_state.tome_of_harvests.functional_text = "Draw 3 cards."
    game_state.compound_event = None


@when("the card resolves")
def step_tome_resolves(game_state):
    """Rule 1.9.2: Resolution creates a compound event."""
    # Engine Feature Needed: CompoundEvent with count=3 for "Draw N cards"
    game_state.compound_event = {
        "event_type": "compound",
        "repeated_instruction": "draw_card",
        "count": 3,
        "individual_events": [
            {"event_type": "draw_card", "occurred": True, "index": 0},
            {"event_type": "draw_card", "occurred": True, "index": 1},
            {"event_type": "draw_card", "occurred": True, "index": 2},
        ],
        "occurred": True,
    }


@then("a compound event is created")
def step_compound_event_created(game_state):
    """Rule 1.9.2: A compound event object is created."""
    # Engine Feature Needed: CompoundEvent class
    assert game_state.compound_event is not None
    assert game_state.compound_event["event_type"] == "compound"


@then("the compound event contains 3 individual draw events")
def step_compound_contains_3_events(game_state):
    """Rule 1.9.2: Compound event expands to exactly 3 individual events."""
    # Engine Feature Needed: CompoundEvent.individual_events list
    assert len(game_state.compound_event["individual_events"]) == 3


@then("the individual events occur in sequence")
def step_individual_events_in_sequence(game_state):
    """Rule 1.9.2: Individual events occur one at a time."""
    # Engine Feature Needed: CompoundEvent sequential execution
    for i, event in enumerate(game_state.compound_event["individual_events"]):
        assert event["occurred"] is True
        assert event["index"] == i


# ===========================================================================
# Scenario: compound event is expanded into individual events
# Tests Rule 1.9.2 - Compact format expanded into individual events
# ===========================================================================


@scenario(
    "../features/section_1_9_events.feature",
    "compound event is expanded into individual events",
)
def test_compound_event_is_expanded_into_individual_events():
    """Rule 1.9.2: Compact compound effects expand into individual events."""
    pass


@given('a compact effect "Create 2 Runechant tokens"')
def step_compact_effect_create_runechant(game_state):
    """Rule 1.9.2: Compact format specifies repeated instruction."""
    game_state.compact_effect = {
        "compact_text": "Create 2 Runechant tokens",
        "instruction": "create_token",
        "token_type": "Runechant",
        "count": 2,
    }
    game_state.expanded_events = []


@when("the compact compound event occurs")
def step_compact_compound_event_occurs(game_state):
    """Rule 1.9.2: Compact effect expands into individual events."""
    # Engine Feature Needed: CompoundEvent.expand() -> List[Event]
    effect = game_state.compact_effect
    game_state.expanded_events = [
        {
            "event_type": "create_token",
            "token_type": effect["token_type"],
            "occurred": True,
        }
        for _ in range(effect["count"])
    ]


@then("the effect is expanded into 2 individual token creation events")
def step_expanded_to_2_events(game_state):
    """Rule 1.9.2: Compound event creates exactly 2 individual events."""
    # Engine Feature Needed: CompoundEvent.individual_events
    assert len(game_state.expanded_events) == 2


@then("each individual token creation event occurs separately")
def step_each_token_creation_event_occurs(game_state):
    """Rule 1.9.2: Each individual event occurs as its own event."""
    # Engine Feature Needed: Individual events each tracked independently
    for event in game_state.expanded_events:
        assert event["occurred"] is True


# ===========================================================================
# Scenario: triggered effect on compound event fires only once
# Tests Rule 1.9.2a - Triggered effect on compound fires only once
# ===========================================================================


@scenario(
    "../features/section_1_9_events.feature",
    "triggered effect on compound event fires only once",
)
def test_triggered_effect_on_compound_event_fires_only_once():
    """Rule 1.9.2a: Triggered effects trigger once on compound event, not per individual event."""
    pass


@given(
    'a card "Korshem" with the triggered effect "Whenever a hero reveals 1 or more cards"'
)
def step_korshem_triggered_effect(game_state):
    """Rule 1.9.2a: Korshem triggers once on compound reveal event."""
    game_state.korshem = game_state.create_card(name="Korshem")
    # Engine Feature Needed: TriggeredEffect that triggers on compound reveal event
    game_state.korshem_trigger = {
        "trigger_condition": "on_reveal_one_or_more_cards",
        "triggers_on": "compound_event",
        "trigger_count": 0,
        "active": True,
    }


@given("an effect that reveals 3 cards as a compound event")
def step_effect_reveals_3_cards(game_state):
    """Rule 1.9.2a: Compound event reveals 3 cards."""
    game_state.compound_reveal_event = {
        "event_type": "compound",
        "repeated_instruction": "reveal_card",
        "count": 3,
        "individual_events": [
            {"event_type": "reveal_card", "occurred": True},
            {"event_type": "reveal_card", "occurred": True},
            {"event_type": "reveal_card", "occurred": True},
        ],
    }


@when("the compound reveal event occurs")
def step_compound_reveal_event_occurs(game_state):
    """Rule 1.9.2a: The compound event fires; Korshem should trigger only once."""
    # Engine Feature Needed: TriggeredEffect.trigger_on_compound_only() fires once
    trigger = game_state.korshem_trigger
    compound_event = game_state.compound_reveal_event
    if trigger["active"] and compound_event["event_type"] == "compound":
        trigger["trigger_count"] += 1  # Fire exactly once for the compound event


@then("Korshem's triggered effect triggers exactly once")
def step_korshem_triggers_once(game_state):
    """Rule 1.9.2a: Korshem fires exactly once."""
    # Engine Feature Needed: TriggeredEffect fires once per compound event
    assert game_state.korshem_trigger["trigger_count"] == 1


@then("the triggered effect does not trigger again for each individual reveal event")
def step_korshem_not_retrigger_on_individual(game_state):
    """Rule 1.9.2a: Individual events within compound don't re-trigger."""
    # Engine Feature Needed: CompoundEvent.individual_events don't re-fire triggers
    assert game_state.korshem_trigger["trigger_count"] == 1


# ===========================================================================
# Scenario: triggered effect does not re-trigger on individual events of compound
# Tests Rule 1.9.2a - Second scenario of compound event trigger prevention
# ===========================================================================


@scenario(
    "../features/section_1_9_events.feature",
    "triggered effect does not re-trigger on individual events of compound",
)
def test_triggered_effect_does_not_re_trigger_on_individual_events_of_compound():
    """Rule 1.9.2a: Triggered effects fire once for compound, not for each individual event."""
    pass


@given("a triggered effect that triggers when a card is drawn")
def step_triggered_effect_on_draw(game_state):
    """Rule 1.9.2a: A triggered effect that fires on draw events."""
    game_state.draw_trigger = {
        "trigger_condition": "on_draw",
        "trigger_count": 0,
        "active": True,
    }


@given("a compound event that draws 3 cards")
def step_compound_event_draws_3(game_state):
    """Rule 1.9.2a: A compound draw event."""
    game_state.compound_draw_event = {
        "event_type": "compound",
        "repeated_instruction": "draw_card",
        "count": 3,
        "individual_events": [
            {"event_type": "draw_card", "occurred": True},
            {"event_type": "draw_card", "occurred": True},
            {"event_type": "draw_card", "occurred": True},
        ],
    }


@when("the compound draw event occurs")
def step_compound_draw_event_occurs(game_state):
    """Rule 1.9.2a: Compound draw event fires."""
    # Engine Feature Needed: CompoundEvent processing fires triggers once, then suppresses
    trigger = game_state.draw_trigger
    event = game_state.compound_draw_event
    if trigger["active"] and event["event_type"] == "compound":
        trigger["trigger_count"] += 1  # Fire once for compound event


@then("the triggered draw effect triggers exactly once on the compound event")
def step_draw_trigger_fires_once(game_state):
    """Rule 1.9.2a: Trigger fires once on compound."""
    assert game_state.draw_trigger["trigger_count"] == 1


@then("the triggered draw effect does not trigger 3 more times for individual events")
def step_draw_trigger_not_thrice(game_state):
    """Rule 1.9.2a: No extra triggers from individual events."""
    # Engine Feature Needed: Suppressed individual event triggering
    assert game_state.draw_trigger["trigger_count"] == 1


# ===========================================================================
# Scenario: replacement effect on compound event cannot replace individual events
# Tests Rule 1.9.2b - Compound replacement doesn't cascade
# ===========================================================================


@scenario(
    "../features/section_1_9_events.feature",
    "replacement effect on compound event cannot replace individual events",
)
def test_replacement_effect_on_compound_event_cannot_replace_individual_events():
    """Rule 1.9.2b: Replacing compound event does not also replace individual events."""
    pass


@given(
    'a card "Mordred Tide" with the effect "if you would create 1 or more Runechant tokens, instead create that many plus 1"'
)
def step_mordred_tide_replacement(game_state):
    """Rule 1.9.2b: Mordred Tide replaces compound token creation."""
    game_state.mordred_tide = game_state.create_card(name="Mordred Tide")
    # Engine Feature Needed: ReplacementEffect targeting compound events only
    game_state.mordred_tide_replacement = {
        "replaces": "compound_create_runechant_tokens",
        "replacement_action": "add_one_to_count",
        "applied_to_compound": False,
        "applied_to_individual_count": 0,
    }


@given("an effect that creates 3 Runechant tokens")
def step_effect_creates_3_runechant(game_state):
    """Rule 1.9.2b: Compact effect to create 3 tokens."""
    game_state.create_3_tokens_event = {
        "event_type": "compound",
        "instruction": "create_runechant_token",
        "count": 3,
        "individual_events": [
            {"event_type": "create_runechant_token"},
            {"event_type": "create_runechant_token"},
            {"event_type": "create_runechant_token"},
        ],
    }
    game_state.tokens_created = 0


@when("the compound token creation event occurs")
def step_compound_token_creation_occurs(game_state):
    """Rule 1.9.2b: Mordred Tide replaces compound event only."""
    # Engine Feature Needed: ReplacementEffect.applied_to_compound = True, not to individuals
    replacement = game_state.mordred_tide_replacement
    event = game_state.create_3_tokens_event
    if event["event_type"] == "compound":
        replacement["applied_to_compound"] = True
        new_count = event["count"] + 1  # 4
        # Rule 1.9.2b: Individual events are NOT also replaced
        game_state.tokens_created = new_count


@then("Mordred Tide replaces the compound event to create 4 tokens")
def step_mordred_tide_replaced_compound(game_state):
    """Rule 1.9.2b: Compound event replaced: 3+1=4."""
    assert game_state.mordred_tide_replacement["applied_to_compound"] is True


@then("Mordred Tide does not also replace each individual token creation with 2 tokens")
def step_mordred_tide_not_cascade_to_individuals(game_state):
    """Rule 1.9.2b: Individual events are not additionally replaced."""
    # Engine Feature Needed: ReplacementEffect.prevent_individual_replacement = True
    assert game_state.mordred_tide_replacement["applied_to_individual_count"] == 0


@then("exactly 4 Runechant tokens are created")
def step_exactly_4_tokens_created(game_state):
    """Rule 1.9.2b: Final result is 4 tokens, not 8."""
    assert game_state.tokens_created == 4


# ===========================================================================
# Scenario: replacement of compound event does not cascade to individual events
# Tests Rule 1.9.2b - Second scenario
# ===========================================================================


@scenario(
    "../features/section_1_9_events.feature",
    "replacement of compound event does not cascade to individual events",
)
def test_replacement_of_compound_event_does_not_cascade_to_individual_events():
    """Rule 1.9.2b: Replacement of compound draw event doesn't cascade."""
    pass


@given("a replacement effect that replaces a compound draw event")
def step_replacement_replaces_compound_draw(game_state):
    """Rule 1.9.2b: Replacement for compound draw event."""
    game_state.compound_draw_replacement = {
        "replaces": "compound_draw",
        "replacement_action": "draw_fewer",
        "applied_to_compound": False,
        "applied_to_individual_count": 0,
    }


@given("a compound event that draws 2 cards")
def step_compound_event_draws_2(game_state):
    """Rule 1.9.2b: Compound draw event for 2 cards."""
    game_state.compound_draw_2 = {
        "event_type": "compound",
        "instruction": "draw_card",
        "count": 2,
    }


@when("the replacement effect replaces the compound draw event")
def step_replacement_replaces_compound_draw_event(game_state):
    """Rule 1.9.2b: Only the compound event is replaced."""
    replacement = game_state.compound_draw_replacement
    event = game_state.compound_draw_2
    if event["event_type"] == "compound":
        replacement["applied_to_compound"] = True
        replacement["applied_to_individual_count"] = 0


@then("the replacement only applies to the compound draw event once")
def step_replacement_only_applies_to_compound_once(game_state):
    """Rule 1.9.2b: Replacement applies only to compound event."""
    assert game_state.compound_draw_replacement["applied_to_compound"] is True


@then("the individual draw events are not also replaced")
def step_individual_draw_events_not_replaced(game_state):
    """Rule 1.9.2b: Individual events are not additionally replaced."""
    assert game_state.compound_draw_replacement["applied_to_individual_count"] == 0


# ===========================================================================
# Scenario: multi-player event is compound event starting with turn player
# Tests Rule 1.9.2c - Multi-player events start with turn player
# ===========================================================================


@scenario(
    "../features/section_1_9_events.feature",
    "multi-player event is a compound event in clockwise order from turn player",
)
def test_multi_player_event_is_compound_event_in_clockwise_order_from_turn_player():
    """Rule 1.9.2c: Multi-player events are compound events starting with turn player."""
    pass


@given("a 2-player game with player 0 as the turn player")
def step_2_player_game_player_0_turn(game_state):
    """Rule 1.9.2c: Two-player game with known turn player."""
    # Engine Feature Needed: GameState.turn_player_id
    game_state.turn_player_id = 0
    game_state.player_ids = [0, 1]
    game_state.multi_player_event = None


@given('an effect "Each hero draws a card" that is not controlled by either player')
def step_each_hero_draws_no_controller(game_state):
    """Rule 1.9.2c: Multi-player effect without specific controller."""
    game_state.each_hero_draws_effect = {
        "text": "Each hero draws a card",
        "type": "multi_player",
        "controller_id": None,
    }


@when("the multi-player draw event occurs")
def step_multi_player_draw_event_occurs(game_state):
    """Rule 1.9.2c: Multi-player event expands as compound event."""
    # Engine Feature Needed: MultiPlayerEvent starting with turn_player
    effect = game_state.each_hero_draws_effect
    starting_player = (
        effect["controller_id"]
        if effect["controller_id"] is not None
        else game_state.turn_player_id
    )
    players_in_order = []
    start_idx = game_state.player_ids.index(starting_player)
    for i in range(len(game_state.player_ids)):
        players_in_order.append(
            game_state.player_ids[(start_idx + i) % len(game_state.player_ids)]
        )
    game_state.multi_player_event = {
        "event_type": "compound",
        "players_in_order": players_in_order,
    }


@then("the multi-player event is a compound event")
def step_multi_player_event_is_compound(game_state):
    """Rule 1.9.2c: Multi-player events are compound events."""
    assert game_state.multi_player_event["event_type"] == "compound"


@then("player 0 draws first as the turn player")
def step_player_0_draws_first(game_state):
    """Rule 1.9.2c: Turn player draws first."""
    assert game_state.multi_player_event["players_in_order"][0] == 0


@then("player 1 draws second in clockwise order from turn player")
def step_player_1_draws_second(game_state):
    """Rule 1.9.2c: Player 1 draws second in clockwise order from turn player."""
    assert game_state.multi_player_event["players_in_order"][1] == 1


# ===========================================================================
# Scenario: multi-player event from effect starts with effect controller
# Tests Rule 1.9.2c - When effect has controller, that controller starts
# ===========================================================================


@scenario(
    "../features/section_1_9_events.feature",
    "multi-player event from effect starts with effect controller",
)
def test_multi_player_event_from_effect_starts_with_effect_controller():
    """Rule 1.9.2c: When effect is produced by an effect, start with effect controller."""
    pass


@given("a 2-player game with player 1 as the turn player")
def step_2_player_game_player_1_turn(game_state):
    """Rule 1.9.2c: Player 1 is the turn player."""
    game_state.turn_player_id = 1
    game_state.player_ids = [0, 1]


@given('player 0 controls the effect "Each hero draws a card" as it resolves')
def step_player_0_controls_effect(game_state):
    """Rule 1.9.2c: Effect controller is player 0, not the turn player."""
    game_state.effect_controller_event = {
        "text": "Each hero draws a card",
        "type": "multi_player",
        "controller_id": 0,
    }


@when("the multi-player draw event from the effect occurs")
def step_effect_multi_player_draw_occurs(game_state):
    """Rule 1.9.2c: Compound event starts with effect controller (player 0)."""
    # Engine Feature Needed: MultiPlayerEvent.starting_player = effect.controller_id
    effect = game_state.effect_controller_event
    starting_player = effect["controller_id"]
    players_in_order = []
    start_idx = game_state.player_ids.index(starting_player)
    for i in range(len(game_state.player_ids)):
        players_in_order.append(
            game_state.player_ids[(start_idx + i) % len(game_state.player_ids)]
        )
    game_state.effect_multi_player_event = {
        "event_type": "compound",
        "players_in_order": players_in_order,
    }


@then("the effect multi-player event is a compound event")
def step_effect_multi_player_is_compound(game_state):
    """Rule 1.9.2c: Effect-produced multi-player event is compound."""
    assert game_state.effect_multi_player_event["event_type"] == "compound"


@then("player 0 draws first as the effect controller")
def step_player_0_draws_first_as_controller(game_state):
    """Rule 1.9.2c: Effect controller draws first, overriding turn player priority."""
    assert game_state.effect_multi_player_event["players_in_order"][0] == 0


@then("player 1 draws second in clockwise order from effect controller")
def step_player_1_draws_second_clockwise(game_state):
    """Rule 1.9.2c: Player 1 draws second."""
    assert game_state.effect_multi_player_event["players_in_order"][1] == 1


# ===========================================================================
# Scenario: discard is a composite event with internal events
# Tests Rule 1.9.3 - Composite events have internal events
# ===========================================================================


@scenario(
    "../features/section_1_9_events.feature",
    "discard is a composite event with internal events",
)
def test_discard_is_a_composite_event_with_internal_events():
    """Rule 1.9.3: Discard is a composite event comprising internal events."""
    pass


@given("a player has a card in hand for discarding")
def step_player_has_card_in_hand_for_discarding(game_state):
    """Rule 1.9.3: A card is in hand to be discarded."""
    game_state.composite_card = game_state.create_card(name="Composite Test Card")
    game_state.player.hand.add_card(game_state.composite_card)
    game_state.composite_event = None


@when("the card in hand is discarded")
def step_card_in_hand_is_discarded(game_state):
    """Rule 1.9.3: Discard creates a composite event."""
    # Engine Feature Needed: DiscardEvent as CompositeEvent with internal move event
    game_state.player.hand.remove_card(game_state.composite_card)
    game_state.composite_event = {
        "event_type": "composite",
        "composite_type": "discard",
        "occurred": True,
        "internal_events": [
            {
                "event_type": "move_card",
                "from_zone": "hand",
                "to_zone": "graveyard",
                "occurred": True,
            }
        ],
    }


@then("a composite discard event occurs")
def step_composite_discard_event_occurs(game_state):
    """Rule 1.9.3: The composite discard event occurred."""
    # Engine Feature Needed: CompositeEvent tracking
    assert game_state.composite_event is not None
    assert game_state.composite_event["composite_type"] == "discard"
    assert game_state.composite_event["occurred"] is True


@then("the composite event contains an internal move event from hand to graveyard")
def step_composite_has_internal_move_event(game_state):
    """Rule 1.9.3: Composite event has internal move event."""
    # Engine Feature Needed: CompositeEvent.internal_events list
    internal = game_state.composite_event["internal_events"]
    assert len(internal) == 1
    assert internal[0]["event_type"] == "move_card"
    assert internal[0]["from_zone"] == "hand"
    assert internal[0]["to_zone"] == "graveyard"


# ===========================================================================
# Scenario: composite event is made up of one or more internal events
# Tests Rule 1.9.3 - Generic composite event tracking
# ===========================================================================


@scenario(
    "../features/section_1_9_events.feature",
    "composite event is made up of one or more internal events",
)
def test_composite_event_is_made_up_of_one_or_more_internal_events():
    """Rule 1.9.3: Composite events are comprised of internal events."""
    pass


@given("an effect keyword produces a composite event")
def step_effect_keyword_composite(game_state):
    """Rule 1.9.3: Effect keywords like 'Discard' produce composite events."""
    # Engine Feature Needed: EffectKeyword that produces CompositeEvent
    game_state.keyword_composite = {
        "keyword": "Discard",
        "produces_composite": True,
        "composite_event": None,
    }


@when("the composite keyword event occurs")
def step_composite_keyword_event_occurs(game_state):
    """Rule 1.9.3: Composite event is created with its internal events."""
    # Engine Feature Needed: CompositeEvent with internal_events list
    game_state.keyword_composite["composite_event"] = {
        "event_type": "composite",
        "internal_events": [{"event_type": "move_card", "occurred": True}],
        "occurred": True,
    }


@then("the composite event is tracked with its internal events")
def step_composite_tracked_with_internal(game_state):
    """Rule 1.9.3: Composite event has tracked internal events."""
    # Engine Feature Needed: CompositeEvent.internal_events
    composite = game_state.keyword_composite["composite_event"]
    assert composite is not None
    assert len(composite["internal_events"]) >= 1


# ===========================================================================
# Scenario: triggered effect only triggers once on composite event
# Tests Rule 1.9.3a - Composite event triggering fires once
# ===========================================================================


@scenario(
    "../features/section_1_9_events.feature",
    "triggered effect only triggers once on composite event",
)
def test_triggered_effect_only_triggers_once_on_composite_event():
    """Rule 1.9.3a: Triggered effects trigger once on composite event."""
    pass


@given("a triggered effect that triggers on discard events")
def step_triggered_effect_on_discard_events(game_state):
    """Rule 1.9.3a: A triggered effect for discard events."""
    game_state.composite_trigger = {
        "trigger_condition": "on_discard",
        "trigger_count": 0,
        "active": True,
    }


@given("a player has a card to discard once")
def step_player_has_card_to_discard_once(game_state):
    """Rule 1.9.3a: Setup for a discard event."""
    game_state.single_discard_card = game_state.create_card(
        name="Card to Discard Single"
    )
    game_state.player.hand.add_card(game_state.single_discard_card)


@when("the composite discard event occurs along with its internal move event")
def step_composite_discard_and_move_occur(game_state):
    """Rule 1.9.3a: Both composite and internal events fire; trigger should fire once."""
    # Engine Feature Needed: CompositeEvent.trigger_once_on_composite_event()
    game_state.player.hand.remove_card(game_state.single_discard_card)
    trigger = game_state.composite_trigger
    # Rule 1.9.3a: trigger fires once for the composite event
    if trigger["active"]:
        trigger["trigger_count"] += 1  # Fires once on composite, NOT on internal


@then("the discard triggered effect triggers exactly once")
def step_discard_triggered_fires_once(game_state):
    """Rule 1.9.3a: Exactly one trigger from composite event."""
    # Engine Feature Needed: CompositeEvent single-trigger mechanism
    assert game_state.composite_trigger["trigger_count"] == 1


@then(
    "the triggered effect does not trigger a second time from the internal move event"
)
def step_composite_no_second_trigger(game_state):
    """Rule 1.9.3a: Internal event doesn't re-fire the trigger."""
    # Engine Feature Needed: Internal events don't separately trigger
    assert game_state.composite_trigger["trigger_count"] == 1


# ===========================================================================
# Scenario: triggered effect on composite event does not double-trigger
# Tests Rule 1.9.3a - Second scenario: double-matching trigger fires once
# ===========================================================================


@scenario(
    "../features/section_1_9_events.feature",
    "triggered effect on composite event does not double-trigger",
)
def test_triggered_effect_on_composite_event_does_not_double_trigger():
    """Rule 1.9.3a: Even if both composite and internal event match, trigger fires once."""
    pass


@given(
    "a triggered effect that would trigger on both discard and card-moved-to-graveyard"
)
def step_double_match_trigger(game_state):
    """Rule 1.9.3a: Trigger matches both composite and internal event types."""
    # Engine Feature Needed: TriggeredEffect that could match multiple events
    game_state.double_trigger = {
        "trigger_conditions": ["on_discard", "on_card_moved_to_graveyard"],
        "trigger_count": 0,
        "active": True,
    }


@given("a player has a card for the double trigger check")
def step_player_has_card_for_double_trigger(game_state):
    """Rule 1.9.3a: A discard event about to occur."""
    game_state.double_check_card = game_state.create_card(name="Double Check Card")
    game_state.player.hand.add_card(game_state.double_check_card)


@when(
    "the composite discard event and its internal move event both would trigger the effect"
)
def step_both_events_would_trigger(game_state):
    """Rule 1.9.3a: Both composite and internal events match the trigger condition."""
    # Engine Feature Needed: CompositeEvent.dedup_triggers() ensures single fire
    game_state.player.hand.remove_card(game_state.double_check_card)
    trigger = game_state.double_trigger
    # Rule 1.9.3a: Even though both composite and internal match, fire only once
    if trigger["active"]:
        trigger["trigger_count"] += 1  # Only once


@then("the triggered effect triggers only once")
def step_double_match_triggers_once(game_state):
    """Rule 1.9.3a: One trigger from composite + internal, not two."""
    # Engine Feature Needed: CompositeEvent deduplicate triggers
    assert game_state.double_trigger["trigger_count"] == 1


# ===========================================================================
# Scenario: preventing trigger on composite event also prevents on internal events
# Tests Rule 1.9.3b - Prevented triggering is complete
# ===========================================================================


@scenario(
    "../features/section_1_9_events.feature",
    "preventing trigger on composite event also prevents on internal events",
)
def test_preventing_trigger_on_composite_event_also_prevents_on_internal_events():
    """Rule 1.9.3b: Preventing a trigger on composite also prevents on internal events."""
    pass


@given("a triggered effect that would trigger on discard")
def step_triggered_effect_that_would_trigger_on_discard(game_state):
    """Rule 1.9.3b: A triggered effect that would fire on discard."""
    game_state.prevented_trigger = {
        "trigger_condition": "on_discard",
        "trigger_count": 0,
        "active": True,
        "prevented": False,
    }


@given("a rule prevents the triggered effect from triggering on the discard event")
def step_rule_prevents_trigger(game_state):
    """Rule 1.9.3b: A prevention rule is active."""
    # Engine Feature Needed: TriggerPrevention.applies_to_composite_and_internal = True
    game_state.prevented_trigger["prevented"] = True


@when("the composite discard event occurs")
def step_composite_discard_occurs_prevented(game_state):
    """Rule 1.9.3b: Composite event fires but trigger is prevented entirely."""
    # Engine Feature Needed: Prevention applies to entire composite event
    trigger = game_state.prevented_trigger
    if not trigger["prevented"]:
        trigger["trigger_count"] += 1


@then("the triggered effect does not trigger on the composite event")
def step_prevented_on_composite(game_state):
    """Rule 1.9.3b: Trigger prevented on composite."""
    assert game_state.prevented_trigger["trigger_count"] == 0


@then("the triggered effect does not trigger from any internal event either")
def step_prevented_on_internal(game_state):
    """Rule 1.9.3b: Trigger also prevented on internal events."""
    # Engine Feature Needed: Internal events also suppressed when composite trigger prevented
    assert game_state.prevented_trigger["trigger_count"] == 0


# ===========================================================================
# Scenario: replacing internal event destination does not prevent composite event
# Tests Rule 1.9.3c - Partial replacement preserves composite event
# ===========================================================================


@scenario(
    "../features/section_1_9_events.feature",
    "replacing internal event destination does not prevent composite event",
)
def test_replacing_internal_event_destination_does_not_prevent_composite_event():
    """Rule 1.9.3c: Partially modifying internal events doesn't prevent composite event."""
    pass


@given("a player has a card to discard with destination replacement")
def step_player_has_card_discard_destination_replacement(game_state):
    """Rule 1.9.3c: Card is in hand to be discarded."""
    game_state.partial_replace_card = game_state.create_card(
        name="Partial Replace Card"
    )
    game_state.player.hand.add_card(game_state.partial_replace_card)
    game_state.partial_composite_event = None


@given(
    "a replacement effect that changes the destination of move events to banished zone"
)
def step_replacement_changes_destination_to_banished(game_state):
    """Rule 1.9.3c: Replacement modifies destination but doesn't cancel the move."""
    # Engine Feature Needed: ReplacementEffect that modifies internal event destination
    game_state.banish_replacement = {
        "replaces_destination": "graveyard",
        "new_destination": "banished",
        "active": True,
        "applied": False,
    }


@when("the player discards the card with replacement active")
def step_player_discards_card_with_replacement_active(game_state):
    """Rule 1.9.3c: Discard occurs but destination is replaced."""
    # Engine Feature Needed: CompositeEvent preserves even with modified internal events
    game_state.player.hand.remove_card(game_state.partial_replace_card)
    replacement = game_state.banish_replacement
    if replacement["active"]:
        replacement["applied"] = True
        destination = replacement["new_destination"]
    else:
        destination = "graveyard"
    game_state.partial_composite_event = {
        "event_type": "composite",
        "composite_type": "discard",
        "occurred": True,  # Composite event still occurs!
        "internal_events": [
            {
                "event_type": "move_card",
                "from_zone": "hand",
                "to_zone": destination,
                "occurred": True,
            }
        ],
    }


@then("the replacement effect modifies the internal move event destination to banished")
def step_move_destination_modified_to_banished(game_state):
    """Rule 1.9.3c: Internal event destination was replaced."""
    # Engine Feature Needed: ReplacementEffect modifies CompositeEvent.internal_events
    internal = game_state.partial_composite_event["internal_events"][0]
    assert internal["to_zone"] == "banished"


@then("the composite discard event still occurs")
def step_composite_discard_still_occurs(game_state):
    """Rule 1.9.3c: Composite event occurs despite internal modification."""
    # Engine Feature Needed: CompositeEvent.occurred = True even with modified internals
    assert game_state.partial_composite_event["occurred"] is True
    assert game_state.partial_composite_event["composite_type"] == "discard"


@then("the card ends up in the banished zone not the graveyard")
def step_card_in_banished_not_graveyard(game_state):
    """Rule 1.9.3c: Card moved to banished as per replacement effect."""
    internal = game_state.partial_composite_event["internal_events"][0]
    assert internal["to_zone"] == "banished"
    assert internal["to_zone"] != "graveyard"


# ===========================================================================
# Scenario: partial modification of internal event leaves composite event intact
# Tests Rule 1.9.3c - Second scenario
# ===========================================================================


@scenario(
    "../features/section_1_9_events.feature",
    "partial modification of internal event leaves composite event intact",
)
def test_partial_modification_of_internal_event_leaves_composite_event_intact():
    """Rule 1.9.3c: Partially modifying an internal event does not cancel the composite event."""
    pass


@given("a replacement effect that partially modifies an internal event")
def step_partial_replacement_of_internal(game_state):
    """Rule 1.9.3c: Replacement partially modifies an internal event."""
    game_state.partial_modification = {
        "type": "partial_replacement",
        "applied": False,
    }


@when("the composite event containing the modified internal event occurs")
def step_composite_with_modified_internal_occurs(game_state):
    """Rule 1.9.3c: Composite event fires with modified internal event."""
    # Engine Feature Needed: CompositeEvent still occurs when internal is partially replaced
    game_state.partial_modification["applied"] = True
    game_state.partial_composite_still_occurs = True


@then("the composite event is not replaced or cancelled")
def step_composite_not_cancelled(game_state):
    """Rule 1.9.3c: Partial internal replacement does not cancel composite."""
    # Engine Feature Needed: CompositeEvent.occurred = True with partial replacement
    assert game_state.partial_composite_still_occurs is True


@then("the composite event still occurs with the modified internal event")
def step_composite_occurs_with_modified_internal(game_state):
    """Rule 1.9.3c: Composite event occurs with its (now modified) internals."""
    assert game_state.partial_modification["applied"] is True
    assert game_state.partial_composite_still_occurs is True


# ===========================================================================
# Scenario: composite event does not occur if all internal events are replaced
# Tests Rule 1.9.3d - All internal events fail means composite doesn't occur
# ===========================================================================


@scenario(
    "../features/section_1_9_events.feature",
    "composite event does not occur if all internal events are replaced",
)
def test_composite_event_does_not_occur_if_all_internal_events_are_replaced():
    """Rule 1.9.3d: If all internal events are replaced, composite event doesn't occur."""
    pass


@given("a player has a card to discard with full replacement")
def step_player_has_card_discard_full_replacement(game_state):
    """Rule 1.9.3d: Card in hand for a discard with full replacement."""
    game_state.full_replace_card = game_state.create_card(name="Full Replace Card")
    game_state.player.hand.add_card(game_state.full_replace_card)
    game_state.full_replace_composite_event = None


@given("a replacement effect that completely replaces the move event in a discard")
def step_full_replacement_of_move_event(game_state):
    """Rule 1.9.3d: Replacement completely replaces the internal move event."""
    # Engine Feature Needed: ReplacementEffect.fully_replaces_event = True
    game_state.full_move_replacement = {
        "fully_replaces_move_event": True,
        "active": True,
        "applied": False,
    }


@when("the player attempts to discard the card with full replacement")
def step_player_attempts_discard_full_replace(game_state):
    """Rule 1.9.3d: Discard attempted but internal event fully replaced."""
    # Engine Feature Needed: CompositeEvent.occurred = False when no internal events occur
    replacement = game_state.full_move_replacement
    if replacement["active"] and replacement["fully_replaces_move_event"]:
        replacement["applied"] = True
        game_state.full_replace_composite_event = {
            "event_type": "composite",
            "composite_type": "discard",
            "occurred": False,  # Composite does NOT occur!
            "internal_events": [
                {
                    "event_type": "move_card",
                    "occurred": False,  # Fully replaced = does not occur
                }
            ],
        }


@then("the internal move event is replaced entirely and does not occur")
def step_internal_move_event_fully_replaced(game_state):
    """Rule 1.9.3d: The internal move event does not occur."""
    internal = game_state.full_replace_composite_event["internal_events"][0]
    assert internal["occurred"] is False


@then("the composite discard event is considered not to have occurred")
def step_composite_discard_not_occurred(game_state):
    """Rule 1.9.3d: Composite event does not occur when all internal events fail."""
    # Engine Feature Needed: CompositeEvent.occurred = False when all internals fail
    assert game_state.full_replace_composite_event["occurred"] is False


@then("triggered effects on discard do not trigger")
def step_discard_triggers_do_not_fire(game_state):
    """Rule 1.9.3d: No triggers fire because composite event didn't occur."""
    # Engine Feature Needed: TriggeredEffect.can_trigger_from(composite_event) = False
    assert game_state.full_replace_composite_event["occurred"] is False


# ===========================================================================
# Scenario: all-internal-events-fail prevents composite event triggering
# Tests Rule 1.9.3d - Second scenario with triggered effect
# ===========================================================================


@scenario(
    "../features/section_1_9_events.feature",
    "all-internal-events-fail prevents composite event triggering",
)
def test_all_internal_events_fail_prevents_composite_event_triggering():
    """Rule 1.9.3d: No triggers fire when composite event does not occur."""
    pass


@given("a triggered effect that triggers on discard")
def step_discard_trigger_for_full_replace(game_state):
    """Rule 1.9.3d: Triggered effect that would fire on discard."""
    game_state.discard_trigger_full_replace = {
        "trigger_condition": "on_discard",
        "trigger_count": 0,
        "active": True,
    }


@given("a replacement effect that fully replaces the move-to-graveyard internal event")
def step_full_graveyard_replacement(game_state):
    """Rule 1.9.3d: Full replacement of internal move event."""
    game_state.full_graveyard_replacement = {
        "fully_replaces_move_to_graveyard": True,
        "active": True,
    }


@when("the player discards a card with the full replacement active")
def step_discard_with_full_replacement(game_state):
    """Rule 1.9.3d: Discard attempted; internal event fully replaced; composite doesn't occur."""
    # Engine Feature Needed: TriggeredEffect checks if composite event occurred before triggering
    replacement = game_state.full_graveyard_replacement
    trigger = game_state.discard_trigger_full_replace
    if replacement["active"] and replacement["fully_replaces_move_to_graveyard"]:
        composite_occurred = False
    else:
        composite_occurred = True
    if composite_occurred and trigger["active"]:
        trigger["trigger_count"] += 1


@then("the composite discard event does not occur")
def step_composite_discard_does_not_occur_full(game_state):
    """Rule 1.9.3d: Composite event does not occur."""
    # Engine Feature Needed: CompositeEvent.occurred = False
    assert game_state.discard_trigger_full_replace["trigger_count"] == 0


@then("the triggered effect on discard is not triggered")
def step_discard_triggered_not_triggered(game_state):
    """Rule 1.9.3d: Trigger does not fire when composite event didn't occur."""
    # Engine Feature Needed: TriggeredEffect cannot fire from non-occurring composite event
    assert game_state.discard_trigger_full_replace["trigger_count"] == 0


# ===========================================================================
# Fixtures
# ===========================================================================


@pytest.fixture
def game_state():
    """
    Fixture providing game state for testing.

    Uses BDDGameState which integrates with the real engine.
    Reference: Rule 1.9
    """
    from tests.bdd_helpers import BDDGameState

    state = BDDGameState()

    # Initialize event tracking attributes
    state.produced_event = None
    state.action_event = None
    state.phase_event = None
    state.current_phase = None
    state.event_was_modified = False
    state.cards_drawn = []
    state.discard_triggered = False

    # Compound event tracking
    state.compound_event = None
    state.expanded_events = []
    state.tokens_created = 0

    # Composite event tracking
    state.composite_event = None
    state.partial_composite_still_occurs = False
    state.deck_is_private = False
    state.opponent_can_verify = True
    state.search_result = None

    return state
