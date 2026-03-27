"""
Step definitions for Section 8.3.42: Suspense (Ability Keyword)
Reference: Flesh and Blood Comprehensive Rules Section 8.3.42

This module implements behavioral tests for the Suspense ability keyword:
- Suspense consists of one static ability + two triggered-static abilities (Rule 8.3.42)
- Static ability: the permanent enters the arena with 2 suspense counters (Rule 8.3.42)
- Triggered-static ability 1: at the start of your turn, remove a suspense counter (Rule 8.3.42)
- Triggered-static ability 2: when no suspense counters remain, destroy it (Rule 8.3.42)
- After 2 start-of-turn triggers the card is destroyed (Rule 8.3.42)

Engine Features Needed for Section 8.3.42:
- [ ] AbilityKeyword.SUSPENSE static ability on cards (Rule 8.3.42)
- [ ] SuspenseAbility.static_part.is_static -> True (enters with 2 counters) (Rule 8.3.42)
- [ ] SuspenseAbility.triggered_parts: two triggered-static abilities (Rule 8.3.42)
- [ ] CardInstance.suspense_counters property (counter tracking) (Rule 8.3.42)
- [ ] ArenaEntryHandler: place 2 suspense counters when Suspense card enters arena (Rule 8.3.42)
- [ ] StartOfTurnHandler: remove one suspense counter from each Suspense card (Rule 8.3.42)
- [ ] CounterCheckHandler: destroy Suspense card when suspense_counters == 0 (Rule 8.3.42)

Current status: Tests written, Engine pending
"""

import pytest
from pytest_bdd import scenario, given, when, then, parsers


# ===== Rule 8.3.42: Suspense comprises one static + two triggered-static abilities =====

@scenario(
    "../features/section_8_3_42_suspense.feature",
    "Suspense is a static ability and two triggered-static abilities",
)
def test_suspense_ability_types():
    """Rule 8.3.42: Suspense includes one static and two triggered-static abilities."""
    pass


# ===== Rule 8.3.42: Card enters arena with 2 suspense counters =====

@scenario(
    "../features/section_8_3_42_suspense.feature",
    "A card with Suspense enters the arena with 2 suspense counters",
)
def test_suspense_card_enters_with_two_counters():
    """Rule 8.3.42: A Suspense card enters the arena with exactly 2 suspense counters."""
    pass


@scenario(
    "../features/section_8_3_42_suspense.feature",
    "A card with Suspense does not enter with fewer than 2 suspense counters",
)
def test_suspense_card_does_not_enter_with_one_counter():
    """Rule 8.3.42: A Suspense card must enter with exactly 2 counters, not fewer."""
    pass


@scenario(
    "../features/section_8_3_42_suspense.feature",
    "A card with Suspense does not enter with more than 2 suspense counters",
)
def test_suspense_card_does_not_enter_with_three_counters():
    """Rule 8.3.42: A Suspense card must enter with exactly 2 counters, not more."""
    pass


# ===== Rule 8.3.42: Remove a suspense counter at start of turn =====

@scenario(
    "../features/section_8_3_42_suspense.feature",
    "A suspense counter is removed at the start of the controlling player's turn",
)
def test_suspense_counter_removed_at_start_of_turn():
    """Rule 8.3.42: One suspense counter is removed at the start of each turn."""
    pass


@scenario(
    "../features/section_8_3_42_suspense.feature",
    "A second start-of-turn removes the last suspense counter",
)
def test_suspense_last_counter_removed():
    """Rule 8.3.42: The final suspense counter is removed at the second start-of-turn."""
    pass


# ===== Rule 8.3.42: Destroy card when no suspense counters remain =====

@scenario(
    "../features/section_8_3_42_suspense.feature",
    "A card with Suspense is destroyed when it has no suspense counters",
)
def test_suspense_card_destroyed_at_zero_counters():
    """Rule 8.3.42: A Suspense card is destroyed when it has 0 suspense counters."""
    pass


@scenario(
    "../features/section_8_3_42_suspense.feature",
    "After two start-of-turn triggers a Suspense card is destroyed",
)
def test_suspense_card_destroyed_after_two_turns():
    """Rule 8.3.42: After 2 start-of-turn events a Suspense card is destroyed."""
    pass


# ===== Rule 8.3.42: Card with remaining counters is not destroyed =====

@scenario(
    "../features/section_8_3_42_suspense.feature",
    "A card with Suspense is not destroyed while it still has suspense counters",
)
def test_suspense_card_not_destroyed_with_counters():
    """Rule 8.3.42: A Suspense card is not destroyed as long as it has counters remaining."""
    pass


# ===== Rule 8.3.42: Cards without Suspense are unaffected =====

@scenario(
    "../features/section_8_3_42_suspense.feature",
    "A card without Suspense does not enter with suspense counters",
)
def test_non_suspense_card_no_counters():
    """Rule 8.3.42: Cards without Suspense do not receive suspense counters on arena entry."""
    pass


# ===== Step Definitions =====

# ---- Given steps ----

@given('a card has the "Suspense" keyword')
def card_has_suspense(game_state):
    """Rule 8.3.42: Create a card that has the Suspense keyword."""
    card = game_state.create_card(name="Suspense Test Card")
    card._has_suspense = True
    game_state.test_card = card


@given('a card with the "Suspense" keyword')
def card_with_suspense(game_state):
    """Rule 8.3.42: Create a Suspense card (not yet in arena)."""
    card = game_state.create_card(name="Suspense Card")
    card._has_suspense = True
    card._suspense_counters = 0
    game_state.test_card = card


@given('a card with the "Suspense" keyword is in the arena with 2 suspense counters')
def suspense_card_in_arena_with_two_counters(game_state):
    """Rule 8.3.42: Place a Suspense card in the arena with 2 counters."""
    card = game_state.create_card(name="Suspense Card")
    card._has_suspense = True
    card._suspense_counters = 2
    card._is_destroyed = False
    game_state.play_card_to_arena(card)
    game_state.test_card = card


@given('a card with the "Suspense" keyword is in the arena with 1 suspense counter')
def suspense_card_in_arena_with_one_counter(game_state):
    """Rule 8.3.42: Place a Suspense card in the arena with 1 counter."""
    card = game_state.create_card(name="Suspense Card")
    card._has_suspense = True
    card._suspense_counters = 1
    card._is_destroyed = False
    game_state.play_card_to_arena(card)
    game_state.test_card = card


@given('a card with the "Suspense" keyword is in the arena with 0 suspense counters')
def suspense_card_in_arena_with_zero_counters(game_state):
    """Rule 8.3.42: Place a Suspense card in the arena with 0 counters."""
    card = game_state.create_card(name="Suspense Card")
    card._has_suspense = True
    card._suspense_counters = 0
    card._is_destroyed = False
    game_state.play_card_to_arena(card)
    game_state.test_card = card


@given('a card without the "Suspense" keyword')
def card_without_suspense(game_state):
    """Rule 8.3.42: Create a card that does not have the Suspense keyword."""
    card = game_state.create_card(name="Normal Card")
    card._has_suspense = False
    game_state.test_card = card


# ---- When steps ----

@when("I inspect the Suspense abilities on the card")
def inspect_suspense_abilities(game_state):
    """Rule 8.3.42: Inspect the Suspense abilities on the card."""
    game_state.inspected_abilities = game_state.get_suspense_abilities(
        game_state.test_card
    )


@when("the card enters the arena")
def card_enters_arena(game_state):
    """Rule 8.3.42: Place the card into the arena, triggering entry effects."""
    game_state.arena_entry_result = game_state.enter_arena_with_suspense(
        game_state.test_card
    )


@when("the start of the controlling player's turn is processed")
def start_of_turn_processed(game_state):
    """Rule 8.3.42: Process the start-of-turn triggered-static ability."""
    game_state.start_of_turn_result = game_state.process_suspense_start_of_turn(
        game_state.test_card
    )


@when("the start of the controlling player's turn is processed twice")
def start_of_turn_processed_twice(game_state):
    """Rule 8.3.42: Process start-of-turn twice (simulating 2 turns)."""
    game_state.process_suspense_start_of_turn(game_state.test_card)
    game_state.start_of_turn_result = game_state.process_suspense_start_of_turn(
        game_state.test_card
    )


@when("the no-counters destruction trigger is processed")
def no_counters_destruction_trigger(game_state):
    """Rule 8.3.42: Process the 'when no counters remain, destroy it' trigger."""
    game_state.destruction_result = game_state.process_suspense_destruction_trigger(
        game_state.test_card
    )


# ---- Then steps ----

@then("the Suspense keyword includes one static ability")
def suspense_has_one_static_ability(game_state):
    """Rule 8.3.42: Suspense must include exactly one static ability."""
    abilities = game_state.inspected_abilities
    assert abilities is not None, "Card should have Suspense abilities"
    static_abilities = [
        a for a in abilities
        if getattr(a, "is_static", False) and not getattr(a, "is_triggered_static", False)
    ]
    assert len(static_abilities) == 1, (
        f"Suspense should include exactly 1 static ability (Rule 8.3.42), "
        f"found: {len(static_abilities)}"
    )


@then("the Suspense keyword includes two triggered-static abilities")
def suspense_has_two_triggered_static_abilities(game_state):
    """Rule 8.3.42: Suspense must include exactly two triggered-static abilities."""
    abilities = game_state.inspected_abilities
    assert abilities is not None, "Card should have Suspense abilities"
    triggered_static = [
        a for a in abilities
        if getattr(a, "is_triggered_static", False)
    ]
    assert len(triggered_static) == 2, (
        f"Suspense should include exactly 2 triggered-static abilities (Rule 8.3.42), "
        f"found: {len(triggered_static)}"
    )


@then("the card has 2 suspense counters")
def card_has_two_suspense_counters(game_state):
    """Rule 8.3.42: The card should have exactly 2 suspense counters after entering."""
    card = game_state.test_card
    counters = getattr(card, "suspense_counters", None)
    if counters is None:
        counters = getattr(card, "_suspense_counters", None)
    assert counters == 2, (
        f"Card with Suspense should have 2 suspense counters after entering the arena "
        f"(Rule 8.3.42), got: {counters}"
    )


@then("the card does not have 1 suspense counter")
def card_does_not_have_one_counter(game_state):
    """Rule 8.3.42: The card should NOT have only 1 suspense counter after entering."""
    card = game_state.test_card
    counters = getattr(card, "suspense_counters", None)
    if counters is None:
        counters = getattr(card, "_suspense_counters", None)
    assert counters != 1, (
        f"Card with Suspense should NOT have 1 suspense counter after entering (Rule 8.3.42), "
        f"got: {counters}"
    )


@then("the card does not have 3 suspense counters")
def card_does_not_have_three_counters(game_state):
    """Rule 8.3.42: The card should NOT have 3 suspense counters after entering."""
    card = game_state.test_card
    counters = getattr(card, "suspense_counters", None)
    if counters is None:
        counters = getattr(card, "_suspense_counters", None)
    assert counters != 3, (
        f"Card with Suspense should NOT have 3 suspense counters after entering (Rule 8.3.42), "
        f"got: {counters}"
    )


@then("the card has 1 suspense counter")
def card_has_one_suspense_counter(game_state):
    """Rule 8.3.42: The card should have 1 suspense counter after one start-of-turn removal."""
    card = game_state.test_card
    counters = getattr(card, "suspense_counters", None)
    if counters is None:
        counters = getattr(card, "_suspense_counters", None)
    assert counters == 1, (
        f"Card with Suspense should have 1 counter after one start-of-turn removal "
        f"(Rule 8.3.42), got: {counters}"
    )


@then("the card has 0 suspense counters")
def card_has_zero_suspense_counters(game_state):
    """Rule 8.3.42: The card should have 0 suspense counters after both removals."""
    card = game_state.test_card
    counters = getattr(card, "suspense_counters", None)
    if counters is None:
        counters = getattr(card, "_suspense_counters", None)
    assert counters == 0, (
        f"Card with Suspense should have 0 counters after two start-of-turn removals "
        f"(Rule 8.3.42), got: {counters}"
    )


@then("the card is destroyed")
def card_is_destroyed(game_state):
    """Rule 8.3.42: The card should be destroyed when it has no suspense counters."""
    card = game_state.test_card
    is_destroyed = getattr(card, "is_destroyed", None)
    if is_destroyed is None:
        is_destroyed = getattr(card, "_is_destroyed", None)
    assert is_destroyed is True, (
        f"Card with Suspense should be destroyed when it has no counters (Rule 8.3.42), "
        f"got is_destroyed={is_destroyed}"
    )
    # Also verify the card is no longer in the arena
    assert card not in game_state.player.arena_zone.cards, (
        "Destroyed Suspense card should not remain in the arena (Rule 8.3.42)"
    )


@then("the card is not destroyed")
def card_is_not_destroyed(game_state):
    """Rule 8.3.42: The card should NOT be destroyed while counters remain."""
    card = game_state.test_card
    is_destroyed = getattr(card, "is_destroyed", None)
    if is_destroyed is None:
        is_destroyed = getattr(card, "_is_destroyed", False)
    assert is_destroyed is False or is_destroyed is None, (
        f"Card with Suspense should NOT be destroyed while counters remain (Rule 8.3.42), "
        f"got is_destroyed={is_destroyed}"
    )


@then("the card is still in the arena")
def card_is_still_in_arena(game_state):
    """Rule 8.3.42: The card should still be in the arena while it has counters."""
    card = game_state.test_card
    assert card in game_state.player.arena_zone.cards, (
        "Card with Suspense and remaining counters should still be in the arena (Rule 8.3.42)"
    )


@then("the card has no suspense counters")
def card_has_no_suspense_counters(game_state):
    """Rule 8.3.42: A card without Suspense should have no suspense counters."""
    card = game_state.test_card
    counters = getattr(card, "suspense_counters", None)
    if counters is None:
        counters = getattr(card, "_suspense_counters", 0)
    assert counters == 0 or counters is None, (
        f"Card without Suspense should have no suspense counters (Rule 8.3.42), "
        f"got: {counters}"
    )


# ===== Fixtures =====

@pytest.fixture
def game_state():
    """
    Fixture providing game state for testing Suspense (Rule 8.3.42).

    Uses BDDGameState which integrates with the real engine.
    Reference: Rule 8.3.42
    """
    from tests.bdd_helpers import BDDGameState

    state = BDDGameState()
    return state
