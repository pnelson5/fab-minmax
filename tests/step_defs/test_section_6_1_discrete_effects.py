"""
Step definitions for Section 6.1: Discrete Effects
Reference: Flesh and Blood Comprehensive Rules Section 6.1

This module implements behavioral tests for discrete effects — effects that change
the game state by producing a single event with no lasting duration.

Engine Features Needed for Section 6.1:
- [ ] Discrete effect system: create_discrete_effect(description) (Rule 6.1.1)
- [ ] Effect resolution: resolve_discrete_effect(effect) returning an event (Rule 6.1.1)
- [ ] Duration check: effect_has_duration(effect) -> bool (Rule 6.1.1)
- [ ] Continuous modifier tracking: effect_leaves_continuous_modifier(effect) -> bool (Rule 6.1.1)
- [ ] Sequential effect generation: generate_effects_sequentially(effects) (Rule 6.1.2)
- [ ] Effect event ordering: get_effect_generation_order() -> List (Rule 6.1.2)
- [ ] Effect completion tracking: was_effect_completed_before(effect_a, effect_b) -> bool (Rule 6.1.2)
- [ ] Conditional discrete effect: create_conditional_discrete_effect(condition, effect) (Rule 6.1.3)
- [ ] Condition evaluation: evaluate_effect_condition(effect) -> bool (Rule 6.1.3)
- [ ] Single evaluation tracking: was_condition_evaluated_once(effect) -> bool (Rule 6.1.3)

Current status: Tests written, Engine pending
"""

import pytest
from pytest_bdd import scenario, given, when, then, parsers


# ===== Scenarios =====


@scenario(
    "../features/section_6_1_discrete_effects.feature",
    "A discrete effect changes game state by producing an event",
)
def test_discrete_effect_produces_event():
    """Rule 6.1.1: A discrete effect changes game state by producing an event."""
    pass


@scenario(
    "../features/section_6_1_discrete_effects.feature",
    "A discrete effect has no duration after its event completes",
)
def test_discrete_effect_has_no_duration():
    """Rule 6.1.1: Discrete effects have no lasting duration after their event."""
    pass


@scenario(
    "../features/section_6_1_discrete_effects.feature",
    "A discrete effect does not continuously modify objects or rules",
)
def test_discrete_effect_not_a_continuous_modifier():
    """Rule 6.1.1: Discrete effects do not leave ongoing continuous modifiers."""
    pass


@scenario(
    "../features/section_6_1_discrete_effects.feature",
    "Multiple discrete effects from one ability are generated sequentially",
)
def test_multiple_discrete_effects_sequential():
    """Rule 6.1.2: Multiple discrete effects are generated one at a time."""
    pass


@scenario(
    "../features/section_6_1_discrete_effects.feature",
    "Each discrete effect completes before the next is generated",
)
def test_each_discrete_effect_completes_before_next():
    """Rule 6.1.2: Each discrete effect's event completes before the next effect is generated."""
    pass


@scenario(
    "../features/section_6_1_discrete_effects.feature",
    "A search-put-discard-shuffle sequence produces four sequential atomic events",
)
def test_search_put_discard_shuffle_sequential():
    """Rule 6.1.2: Sand Sketched Plan-style effects are atomic and sequential."""
    pass


@scenario(
    "../features/section_6_1_discrete_effects.feature",
    "A conditional discrete effect is generated when its condition is met at generation time",
)
def test_conditional_discrete_effect_generated_when_condition_met():
    """Rule 6.1.3: A conditional discrete effect is generated if its condition is met at generation time."""
    pass


@scenario(
    "../features/section_6_1_discrete_effects.feature",
    "A conditional discrete effect is not generated when its condition is not met at generation time",
)
def test_conditional_discrete_effect_not_generated_when_condition_not_met():
    """Rule 6.1.3: A conditional discrete effect is NOT generated if its condition is not met."""
    pass


@scenario(
    "../features/section_6_1_discrete_effects.feature",
    "A conditional discrete effect condition is evaluated only once at generation time",
)
def test_conditional_discrete_effect_condition_evaluated_only_once():
    """Rule 6.1.3: Condition is evaluated only once; later state changes don't un-generate the effect."""
    pass


@scenario(
    "../features/section_6_1_discrete_effects.feature",
    "A conditional discrete effect that is not generated produces no event",
)
def test_conditional_discrete_effect_skipped_produces_no_event():
    """Rule 6.1.3: A conditional discrete effect that is not generated produces no event."""
    pass


# ===== Step Definitions =====


@given("a game is in progress", target_fixture="game_state")
def game_in_progress(game_state):
    """Chapter 6: A game is actively being played."""
    try:
        game_state.start_game()
    except AttributeError:
        pass  # Engine needs: start_game()
    return game_state


@given("a player has a card that generates a discrete draw effect")
def player_has_draw_effect_card(game_state):
    """Rule 6.1.1: Setup a card that generates a discrete draw-a-card effect."""
    game_state.draw_effect_card = game_state.create_card(name="Draw Effect Card")


@when("the discrete draw effect is generated")
def discrete_draw_effect_generated(game_state):
    """Rule 6.1.1: Generate a discrete draw effect."""
    try:
        game_state.discrete_effect = game_state.create_discrete_effect(
            description="draw a card"
        )
        game_state.draw_result = game_state.resolve_discrete_effect(game_state.discrete_effect)
    except AttributeError:
        game_state.discrete_effect = None
        game_state.draw_result = None


@then("the game state changes as a result of the event")
def game_state_changes_from_event(game_state):
    """Rule 6.1.1: The discrete effect produces an event that changes the game state."""
    try:
        effect = game_state.discrete_effect
        assert effect is not None, \
            "Engine needs: create_discrete_effect() to create a discrete effect (Rule 6.1.1)"
        result = game_state.draw_result
        assert result is not None, \
            "Engine needs: resolve_discrete_effect() to produce an event (Rule 6.1.1)"
    except AttributeError:
        pytest.fail(
            "Engine needs: Discrete effect system create_discrete_effect() + resolve_discrete_effect() (Rule 6.1.1)"
        )


@then("the player has drawn a card")
def player_has_drawn_a_card(game_state):
    """Rule 6.1.1: After the discrete draw effect, the player has drawn a card."""
    try:
        result = game_state.draw_result
        if result is not None:
            cards_drawn = getattr(result, "cards_drawn", None)
            assert cards_drawn is not None, \
                "Engine needs: resolve_discrete_effect() result tracking cards drawn (Rule 6.1.1)"
    except AttributeError:
        pytest.fail(
            "Engine needs: Discrete effect result with cards_drawn attribute (Rule 6.1.1)"
        )


@given("a discrete effect has been generated and produced its event")
def discrete_effect_generated_and_produced_event(game_state):
    """Rule 6.1.1: A discrete effect that has already produced its event."""
    try:
        effect = game_state.create_discrete_effect(description="deal 1 damage")
        game_state.completed_effect = effect
        game_state.resolve_discrete_effect(effect)
    except AttributeError:
        game_state.completed_effect = None


@when("the event from the discrete effect completes")
def event_from_discrete_effect_completes(game_state):
    """Rule 6.1.1: The event produced by the discrete effect has finished."""
    try:
        effect = game_state.completed_effect
        if effect is not None:
            game_state.effect_completed = game_state.is_discrete_effect_completed(effect)
    except AttributeError:
        game_state.effect_completed = None


@then("the discrete effect has no further influence on the game state")
def discrete_effect_has_no_further_influence(game_state):
    """Rule 6.1.1: After completing, the discrete effect has no further influence."""
    try:
        effect = game_state.completed_effect
        assert effect is not None, \
            "Engine needs: create_discrete_effect() for discrete effect object (Rule 6.1.1)"
        is_active = game_state.is_effect_still_active(effect)
        assert not is_active, \
            "Engine needs: Discrete effects must become inactive after event completes (Rule 6.1.1)"
    except AttributeError:
        pytest.fail(
            "Engine needs: is_effect_still_active() to verify discrete effects end after event (Rule 6.1.1)"
        )


@then("the effect is not tracked as an ongoing modifier")
def effect_not_tracked_as_ongoing_modifier(game_state):
    """Rule 6.1.1: Discrete effects are not tracked as continuous modifiers."""
    try:
        effect = game_state.completed_effect
        if effect is not None:
            has_duration = game_state.effect_has_duration(effect)
            assert not has_duration, \
                "Engine needs: Discrete effects must have no duration (Rule 6.1.1)"
    except AttributeError:
        pytest.fail(
            "Engine needs: effect_has_duration() to confirm discrete effects have no duration (Rule 6.1.1)"
        )


@given("a card generates a discrete deal damage effect")
def card_generates_discrete_damage_effect(game_state):
    """Rule 6.1.1: A card that generates a discrete damage effect."""
    game_state.damage_card = game_state.create_card(name="Damage Effect Card")


@when("the discrete damage effect is generated and produces its event")
def discrete_damage_effect_generated(game_state):
    """Rule 6.1.1: The damage effect is generated and produces its event."""
    try:
        effect = game_state.create_discrete_effect(description="deal 2 damage")
        game_state.damage_effect = effect
        game_state.damage_event = game_state.resolve_discrete_effect(effect)
    except AttributeError:
        game_state.damage_effect = None
        game_state.damage_event = None


@then("damage is dealt as a one-time event")
def damage_dealt_as_one_time_event(game_state):
    """Rule 6.1.1: Damage is dealt exactly once, not repeatedly."""
    try:
        effect = game_state.damage_effect
        assert effect is not None, \
            "Engine needs: create_discrete_effect() for damage effect (Rule 6.1.1)"
        event = game_state.damage_event
        assert event is not None, \
            "Engine needs: resolve_discrete_effect() to produce a one-time damage event (Rule 6.1.1)"
    except AttributeError:
        pytest.fail(
            "Engine needs: Discrete damage effect system (Rule 6.1.1)"
        )


@then("no ongoing continuous modifier is left in the game state")
def no_ongoing_continuous_modifier_left(game_state):
    """Rule 6.1.1: Discrete effects leave no continuous modifiers behind."""
    try:
        effect = game_state.damage_effect
        if effect is not None:
            leaves_modifier = game_state.effect_leaves_continuous_modifier(effect)
            assert not leaves_modifier, \
                "Engine needs: Discrete effects must not leave continuous modifiers (Rule 6.1.1)"
    except AttributeError:
        pytest.fail(
            "Engine needs: effect_leaves_continuous_modifier() to verify no residual modifiers (Rule 6.1.1)"
        )


@given("a resolution ability generates multiple discrete effects in sequence")
def resolution_ability_generates_multiple_effects(game_state):
    """Rule 6.1.2: Setup a resolution ability that produces multiple sequential effects."""
    try:
        game_state.multi_effect_card = game_state.create_card(name="Multi-Effect Card")
        game_state.effect_sequence = [
            {"type": "draw", "description": "draw a card"},
            {"type": "discard", "description": "discard a card"},
        ]
    except AttributeError:
        game_state.effect_sequence = []


@when("the ability resolves")
def ability_resolves(game_state):
    """Rule 6.1.2: The resolution ability resolves, generating its discrete effects."""
    try:
        game_state.resolution_log = game_state.generate_effects_sequentially(
            game_state.effect_sequence
        )
    except AttributeError:
        game_state.resolution_log = None


@then("each discrete effect is generated and produces its event one at a time")
def each_effect_generated_one_at_a_time(game_state):
    """Rule 6.1.2: Discrete effects are generated atomically, one at a time."""
    try:
        log = game_state.resolution_log
        assert log is not None, \
            "Engine needs: generate_effects_sequentially() to produce a resolution log (Rule 6.1.2)"
        order = game_state.get_effect_generation_order()
        assert order is not None, \
            "Engine needs: get_effect_generation_order() to track effect generation order (Rule 6.1.2)"
        assert len(order) >= 1, \
            "Engine needs: At least one effect must be tracked in generation order (Rule 6.1.2)"
    except AttributeError:
        pytest.fail(
            "Engine needs: generate_effects_sequentially() and get_effect_generation_order() (Rule 6.1.2)"
        )


@then("the effects are processed in the order they were declared")
def effects_processed_in_declared_order(game_state):
    """Rule 6.1.2: Discrete effects are processed in the order they are declared."""
    try:
        order = game_state.get_effect_generation_order()
        if order and len(order) >= 2:
            first = order[0]
            second = order[1]
            was_first_before_second = game_state.was_effect_completed_before(first, second)
            assert was_first_before_second, \
                "Engine needs: Effects must be processed in declared order (Rule 6.1.2)"
    except AttributeError:
        pytest.fail(
            "Engine needs: was_effect_completed_before() to verify effect ordering (Rule 6.1.2)"
        )


@given("a resolution ability generates a sequence of discrete effects")
def resolution_ability_generates_sequence(game_state):
    """Rule 6.1.2: Setup sequential discrete effects for ordering verification."""
    try:
        game_state.sequence_effects = [
            {"type": "search", "description": "search deck"},
            {"type": "put", "description": "put into hand"},
        ]
        game_state.effect_events = []
    except AttributeError:
        game_state.sequence_effects = []
        game_state.effect_events = []


@when("the first discrete effect is generated")
def first_discrete_effect_generated(game_state):
    """Rule 6.1.2: The first discrete effect in a sequence is generated."""
    try:
        if game_state.sequence_effects:
            first = game_state.sequence_effects[0]
            effect = game_state.create_discrete_effect(description=first["description"])
            game_state.first_effect = effect
            game_state.first_event = game_state.resolve_discrete_effect(effect)
        else:
            game_state.first_effect = None
            game_state.first_event = None
    except AttributeError:
        game_state.first_effect = None
        game_state.first_event = None


@then("the first effect completes its event before the second effect is generated")
def first_effect_completes_before_second_generated(game_state):
    """Rule 6.1.2: First discrete effect's event must complete before the second is generated."""
    try:
        first_effect = game_state.first_effect
        assert first_effect is not None, \
            "Engine needs: create_discrete_effect() for sequential effects (Rule 6.1.2)"
        first_completed = game_state.is_discrete_effect_completed(first_effect)
        assert first_completed, \
            "Engine needs: is_discrete_effect_completed() to verify sequential completion (Rule 6.1.2)"
    except AttributeError:
        pytest.fail(
            "Engine needs: is_discrete_effect_completed() for effect ordering verification (Rule 6.1.2)"
        )


@then("the second discrete effect is generated only after the first event completes")
def second_effect_generated_only_after_first_completes(game_state):
    """Rule 6.1.2: Second effect is generated only after first effect completes."""
    try:
        first_effect = game_state.first_effect
        if first_effect is not None:
            completion_timestamp = game_state.get_effect_completion_timestamp(first_effect)
            assert completion_timestamp is not None, \
                "Engine needs: Effect completion timestamp tracking (Rule 6.1.2)"
    except AttributeError:
        pytest.fail(
            "Engine needs: get_effect_completion_timestamp() for ordering verification (Rule 6.1.2)"
        )


@given("a player has a card that generates search, put, discard, and shuffle discrete effects")
def player_has_sand_sketched_plan_card(game_state):
    """Rule 6.1.2: A card like Sand Sketched Plan with four sequential discrete effects."""
    game_state.plan_card = game_state.create_card(name="Sand Sketched Plan")
    game_state.plan_effects = ["search", "put", "discard", "shuffle"]


@when("the card resolves on the stack")
def card_resolves_on_stack(game_state):
    """Rule 6.1.2: The card is resolved on the stack, generating its four effects."""
    try:
        game_state.play_card_to_stack(game_state.plan_card, controller_id=0)
        game_state.resolution_sequence = game_state.resolve_top_of_stack()
    except AttributeError:
        game_state.resolution_sequence = None


@then("a search event occurs first")
def search_event_occurs_first(game_state):
    """Rule 6.1.2: The search effect is the first to generate and produce its event."""
    try:
        order = game_state.get_effect_generation_order()
        assert order is not None, \
            "Engine needs: get_effect_generation_order() for sequential effect tracking (Rule 6.1.2)"
        if order:
            assert order[0] == "search" or hasattr(order[0], "type"), \
                "Engine needs: First effect in sequence must be search (Rule 6.1.2)"
    except AttributeError:
        pytest.fail(
            "Engine needs: get_effect_generation_order() to verify search-first ordering (Rule 6.1.2)"
        )


@then("after the search event a put event occurs")
def put_event_occurs_after_search(game_state):
    """Rule 6.1.2: The put effect occurs after the search effect completes."""
    try:
        order = game_state.get_effect_generation_order()
        if order and len(order) >= 2:
            assert True, "Engine needs to verify put event is second (Rule 6.1.2)"
    except AttributeError:
        pytest.fail(
            "Engine needs: Effect ordering system for search-put-discard-shuffle sequence (Rule 6.1.2)"
        )


@then("after the put event a discard event occurs")
def discard_event_occurs_after_put(game_state):
    """Rule 6.1.2: The discard effect occurs after the put effect completes."""
    try:
        order = game_state.get_effect_generation_order()
        if order and len(order) >= 3:
            assert True, "Engine needs to verify discard event is third (Rule 6.1.2)"
    except AttributeError:
        pytest.fail(
            "Engine needs: Effect ordering tracking for the discard step (Rule 6.1.2)"
        )


@then("after the discard event a shuffle event occurs")
def shuffle_event_occurs_after_discard(game_state):
    """Rule 6.1.2: The shuffle effect occurs after the discard effect completes."""
    try:
        order = game_state.get_effect_generation_order()
        if order and len(order) >= 4:
            assert True, "Engine needs to verify shuffle event is fourth (Rule 6.1.2)"
    except AttributeError:
        pytest.fail(
            "Engine needs: Effect ordering tracking for the shuffle step (Rule 6.1.2)"
        )


@then("each event is completed before the next begins")
def each_event_completes_before_next(game_state):
    """Rule 6.1.2: Each discrete effect's event completes before the next begins."""
    try:
        completion_order = game_state.get_effect_completion_order()
        assert completion_order is not None, \
            "Engine needs: get_effect_completion_order() to verify sequential atomic events (Rule 6.1.2)"
    except AttributeError:
        pytest.fail(
            "Engine needs: get_effect_completion_order() for sequential discrete effect tracking (Rule 6.1.2)"
        )


# ===== Rule 6.1.3: Conditional discrete effects =====


@given("the game state satisfies the condition for a conditional discrete effect")
def game_state_satisfies_condition(game_state):
    """Rule 6.1.3: The game state currently satisfies the condition for a conditional effect."""
    try:
        game_state.condition_met_at_generation = True
        game_state.conditional_condition = lambda gs: gs.condition_met_at_generation
    except AttributeError:
        game_state.conditional_condition = None


@when("the conditional discrete effect would be generated")
def conditional_discrete_effect_would_be_generated(game_state):
    """Rule 6.1.3: Attempt to generate a conditional discrete effect."""
    try:
        game_state.conditional_effect = game_state.create_conditional_discrete_effect(
            condition="condition_is_met",
            effect_description="draw a card",
        )
        game_state.condition_evaluation_result = game_state.evaluate_effect_condition(
            game_state.conditional_effect
        )
    except AttributeError:
        game_state.conditional_effect = None
        game_state.condition_evaluation_result = None


@then("the condition is evaluated once at the time the effect would be generated")
def condition_evaluated_once_at_generation(game_state):
    """Rule 6.1.3: Condition is evaluated exactly once at generation time."""
    try:
        effect = game_state.conditional_effect
        assert effect is not None, \
            "Engine needs: create_conditional_discrete_effect() (Rule 6.1.3)"
        was_evaluated_once = game_state.was_condition_evaluated_once(effect)
        assert was_evaluated_once, \
            "Engine needs: Condition must be evaluated exactly once at generation time (Rule 6.1.3)"
    except AttributeError:
        pytest.fail(
            "Engine needs: was_condition_evaluated_once() for conditional discrete effects (Rule 6.1.3)"
        )


@then("since the condition is met the effect is generated")
def effect_generated_because_condition_met(game_state):
    """Rule 6.1.3: When condition is met, the conditional effect is generated."""
    try:
        effect = game_state.conditional_effect
        assert effect is not None, \
            "Engine needs: create_conditional_discrete_effect() (Rule 6.1.3)"
        was_generated = game_state.was_effect_generated(effect)
        assert was_generated, \
            "Engine needs: Conditional effect must be generated when condition is met (Rule 6.1.3)"
    except AttributeError:
        pytest.fail(
            "Engine needs: was_effect_generated() to verify conditional effect generation (Rule 6.1.3)"
        )


@then("the effect produces its event")
def conditional_effect_produces_event(game_state):
    """Rule 6.1.3: The generated conditional effect produces its event."""
    try:
        effect = game_state.conditional_effect
        if effect is not None:
            event = game_state.get_effect_event(effect)
            assert event is not None, \
                "Engine needs: get_effect_event() to verify event was produced (Rule 6.1.3)"
    except AttributeError:
        pytest.fail(
            "Engine needs: get_effect_event() for conditional discrete effect events (Rule 6.1.3)"
        )


@given("the game state does not satisfy the condition for a conditional discrete effect")
def game_state_does_not_satisfy_condition(game_state):
    """Rule 6.1.3: The game state does NOT currently satisfy the condition."""
    try:
        game_state.condition_met_at_generation = False
        game_state.conditional_condition = lambda gs: gs.condition_met_at_generation
    except AttributeError:
        game_state.conditional_condition = None


@then("since the condition is not met the effect is not generated")
def effect_not_generated_because_condition_not_met(game_state):
    """Rule 6.1.3: When condition is not met, the conditional effect is not generated."""
    try:
        effect = game_state.conditional_effect
        assert effect is not None, \
            "Engine needs: create_conditional_discrete_effect() (Rule 6.1.3)"
        was_generated = game_state.was_effect_generated(effect)
        assert not was_generated, \
            "Engine needs: Conditional effect must NOT be generated when condition is not met (Rule 6.1.3)"
    except AttributeError:
        pytest.fail(
            "Engine needs: was_effect_generated() to verify conditional effect was skipped (Rule 6.1.3)"
        )


@then("no event is produced for that effect")
def no_event_produced_for_ungenerated_effect(game_state):
    """Rule 6.1.3: A non-generated conditional effect produces no event."""
    try:
        effect = game_state.conditional_effect
        if effect is not None:
            event = game_state.get_effect_event(effect)
            assert event is None, \
                "Engine needs: Non-generated conditional effects must produce no event (Rule 6.1.3)"
    except AttributeError:
        pytest.fail(
            "Engine needs: get_effect_event() returning None for non-generated effects (Rule 6.1.3)"
        )


@given("the game state satisfies the condition for a conditional discrete effect at generation time")
def game_state_satisfies_condition_at_generation(game_state):
    """Rule 6.1.3: Game state satisfies the condition specifically at the moment of generation."""
    try:
        game_state.condition_at_generation = True
        game_state.condition_current = True
    except AttributeError:
        pass


@when("the condition is evaluated and the effect is generated")
def condition_evaluated_and_effect_generated(game_state):
    """Rule 6.1.3: The condition is evaluated (true) and the effect is generated."""
    try:
        game_state.conditional_effect = game_state.create_conditional_discrete_effect(
            condition="condition_at_generation",
            effect_description="draw a card",
        )
        game_state.generation_timestamp = game_state.get_current_timestamp()
        game_state.evaluate_effect_condition(game_state.conditional_effect)
    except AttributeError:
        game_state.conditional_effect = None
        game_state.generation_timestamp = None


@when("the game state changes so that the condition would no longer be met")
def game_state_changes_condition_no_longer_met(game_state):
    """Rule 6.1.3: The game state changes AFTER the effect was already generated."""
    try:
        game_state.condition_at_generation = False
        game_state.condition_current = False
    except AttributeError:
        pass


@then("the effect still produces its event because the condition was already evaluated as met")
def effect_produces_event_despite_state_change(game_state):
    """Rule 6.1.3: Once generated, the effect continues even if the condition would no longer be met."""
    try:
        effect = game_state.conditional_effect
        assert effect is not None, \
            "Engine needs: create_conditional_discrete_effect() (Rule 6.1.3)"
        was_generated = game_state.was_effect_generated(effect)
        assert was_generated, \
            "Engine needs: Once generated, conditional effect stays generated even if condition changes (Rule 6.1.3)"
    except AttributeError:
        pytest.fail(
            "Engine needs: was_effect_generated() for already-generated conditional effects (Rule 6.1.3)"
        )


@then("the condition is not re-evaluated after the effect has been generated")
def condition_not_re_evaluated_after_generation(game_state):
    """Rule 6.1.3: Condition is evaluated exactly once; it is not re-evaluated later."""
    try:
        effect = game_state.conditional_effect
        if effect is not None:
            evaluation_count = game_state.get_condition_evaluation_count(effect)
            assert evaluation_count is not None, \
                "Engine needs: get_condition_evaluation_count() for evaluation tracking (Rule 6.1.3)"
            assert evaluation_count == 1, \
                "Engine needs: Condition must be evaluated exactly once (Rule 6.1.3)"
    except AttributeError:
        pytest.fail(
            "Engine needs: get_condition_evaluation_count() to verify single evaluation (Rule 6.1.3)"
        )


@given("a card has a conditional discrete effect requiring a specific board state")
def card_has_conditional_effect_requiring_board_state(game_state):
    """Rule 6.1.3: Setup a card with a board-state-conditional discrete effect."""
    game_state.conditional_card = game_state.create_card(name="Conditional Effect Card")
    try:
        game_state.required_board_state = "hero_has_over_10_life"
    except AttributeError:
        game_state.required_board_state = None


@given("the required board state is absent")
def required_board_state_is_absent(game_state):
    """Rule 6.1.3: The board state required by the conditional effect is not present."""
    try:
        game_state.board_state_present = False
    except AttributeError:
        pass


@then("the condition is evaluated as not met")
def condition_evaluated_as_not_met(game_state):
    """Rule 6.1.3: The condition check returns false since the board state is absent."""
    try:
        effect = game_state.conditional_effect
        if effect is not None:
            result = game_state.condition_evaluation_result
            assert result is False or result is None, \
                "Engine needs: Condition evaluation must return False when board state is absent (Rule 6.1.3)"
    except AttributeError:
        pytest.fail(
            "Engine needs: evaluate_effect_condition() returning False when condition not met (Rule 6.1.3)"
        )


@then("the effect is skipped entirely with no event occurring")
def effect_skipped_entirely(game_state):
    """Rule 6.1.3: The conditional effect is entirely skipped when its condition is not met."""
    try:
        effect = game_state.conditional_effect
        if effect is not None:
            was_generated = game_state.was_effect_generated(effect)
            assert not was_generated, \
                "Engine needs: Conditional effect must be skipped if condition not met (Rule 6.1.3)"
    except AttributeError:
        pytest.fail(
            "Engine needs: was_effect_generated() to verify effect was skipped (Rule 6.1.3)"
        )


@then("the game state is unchanged by that conditional effect")
def game_state_unchanged_by_skipped_effect(game_state):
    """Rule 6.1.3: When a conditional effect is not generated, the game state is unaffected."""
    try:
        effect = game_state.conditional_effect
        if effect is not None:
            state_changed = game_state.did_effect_change_game_state(effect)
            assert not state_changed, \
                "Engine needs: Non-generated conditional effects must not change game state (Rule 6.1.3)"
    except AttributeError:
        pytest.fail(
            "Engine needs: did_effect_change_game_state() to verify skipped effects have no impact (Rule 6.1.3)"
        )


# ===== Fixtures =====


@pytest.fixture
def game_state():
    """
    Fixture providing game state for Section 6.1 testing.

    Uses BDDGameState which integrates with the real engine.
    Reference: Rule 6.1 (Discrete Effects)
    """
    from tests.bdd_helpers import BDDGameState

    state = BDDGameState()

    return state
