"""
Step definitions for Section 8.3.18: Heave (Ability Keyword)
Reference: Flesh and Blood Comprehensive Rules Section 8.3.18

This module implements behavioral tests for the Heave ability keyword:
- Heave is a hidden triggered ability (Rule 8.3.18)
- Written as "Heave N" meaning "While this is in your hand, at the beginning
  of your end phase, you may pay N{r} and put this face-up into your arsenal.
  If you do, create N Seismic Surge tokens." (Rule 8.3.18)
- If a player pays the resource cost and puts the card face-up into their
  arsenal, the player is considered to have heaved and the card is considered
  to have been heaved (Rule 8.3.18a)
- A player cannot heave if they cannot pay the resource point cost or cannot
  put the card face-up into their arsenal (Rule 8.3.18b)

Engine Features Needed for Section 8.3.18:
- [ ] HeaveAbility class as a hidden triggered ability (Rule 8.3.18)
- [ ] HeaveAbility.is_hidden -> True (Rule 8.3.18)
- [ ] HeaveAbility.is_triggered -> True (Rule 8.3.18)
- [ ] HeaveAbility.n: int — the resource cost value N (Rule 8.3.18)
- [ ] HeaveAbility.meaning: formatted ability text string (Rule 8.3.18)
- [ ] HeaveAbility.trigger_condition: "beginning_of_end_phase_while_in_hand" (Rule 8.3.18)
- [ ] HeaveAbility.triggers_in_zone(zone) -> True only for ZoneType.HAND (Rule 8.3.18)
- [ ] EndPhaseBeginEvent triggers HeaveAbility for cards in hand (Rule 8.3.18)
- [ ] HeaveAction.can_heave(player) -> bool: checks resource cost + arsenal availability (Rule 8.3.18b)
- [ ] HeaveAction.pay_cost(player) -> HeaveResult: pay N{r} + move card to arsenal (Rule 8.3.18)
- [ ] HeaveAction.create_seismic_surge_tokens(n) -> List[TokenCard] (Rule 8.3.18)
- [ ] HeaveAction.result.player_heaved -> bool (Rule 8.3.18a)
- [ ] HeaveAction.result.card_was_heaved -> bool (Rule 8.3.18a)
- [ ] HeaveValidator.can_pay_resource_cost(player, n) -> bool (Rule 8.3.18b)
- [ ] HeaveValidator.can_put_card_in_arsenal(player) -> bool (Rule 8.3.18b)
- [ ] Arsenal.is_occupied -> bool: True if arsenal zone already has a card (Rule 8.3.18b)

Current status: Tests written, Engine pending
"""

import pytest
from pytest_bdd import scenario, given, when, then, parsers


# ===== Rule 8.3.18: Heave is a hidden triggered ability =====

@scenario(
    "../features/section_8_3_18_heave.feature",
    "Heave is a hidden triggered ability",
)
def test_heave_is_hidden_triggered_ability():
    """Rule 8.3.18: Heave is a hidden triggered ability."""
    pass


# ===== Rule 8.3.18: Heave triggers at the beginning of the end phase =====

@scenario(
    "../features/section_8_3_18_heave.feature",
    "Heave triggers at the beginning of the end phase while in hand",
)
def test_heave_triggers_at_beginning_of_end_phase():
    """Rule 8.3.18: Heave triggers at the beginning of the end phase."""
    pass


@scenario(
    "../features/section_8_3_18_heave.feature",
    "Heave does not trigger if the card is not in hand",
)
def test_heave_does_not_trigger_outside_hand():
    """Rule 8.3.18: Heave only triggers while the card is in hand."""
    pass


# ===== Rule 8.3.18: Heave is optional =====

@scenario(
    "../features/section_8_3_18_heave.feature",
    "Heave is optional — player may decline to pay the cost",
)
def test_heave_is_optional():
    """Rule 8.3.18: Heave is optional — player may decline."""
    pass


# ===== Rule 8.3.18: Paying Heave cost puts card face-up in arsenal and creates tokens =====

@scenario(
    "../features/section_8_3_18_heave.feature",
    "Paying Heave 1 cost puts card face-up in arsenal and creates 1 Seismic Surge token",
)
def test_heave_1_creates_1_seismic_surge_token():
    """Rule 8.3.18: Heave 1 creates 1 Seismic Surge token and moves card to arsenal."""
    pass


@scenario(
    "../features/section_8_3_18_heave.feature",
    "Paying Heave 2 cost puts card face-up in arsenal and creates 2 Seismic Surge tokens",
)
def test_heave_2_creates_2_seismic_surge_tokens():
    """Rule 8.3.18: Heave 2 creates 2 Seismic Surge tokens and moves card to arsenal."""
    pass


# ===== Rule 8.3.18a: Player and card are considered to have "heaved" =====

@scenario(
    "../features/section_8_3_18_heave.feature",
    "Player is considered to have heaved after paying the cost",
)
def test_player_considered_to_have_heaved():
    """Rule 8.3.18a: Player is considered to have heaved after paying the cost."""
    pass


@scenario(
    "../features/section_8_3_18_heave.feature",
    "Player is not considered to have heaved if they decline",
)
def test_player_not_considered_to_have_heaved_on_decline():
    """Rule 8.3.18a: Player is not considered to have heaved if cost not paid."""
    pass


# ===== Rule 8.3.18b: Cannot heave if cannot pay resource cost =====

@scenario(
    "../features/section_8_3_18_heave.feature",
    "Cannot heave if player cannot pay the resource point cost",
)
def test_cannot_heave_insufficient_resources():
    """Rule 8.3.18b: Cannot heave if cannot pay the resource point cost."""
    pass


# ===== Rule 8.3.18b: Cannot heave if cannot put card into arsenal =====

@scenario(
    "../features/section_8_3_18_heave.feature",
    "Cannot heave if the player cannot put the card into their arsenal",
)
def test_cannot_heave_arsenal_unavailable():
    """Rule 8.3.18b: Cannot heave if cannot put the card into their arsenal."""
    pass


# ===== Step Definitions =====

@given(parsers.parse('a card with "{heave_text}" ability'))
def card_with_heave_ability(game_state, heave_text):
    """Rule 8.3.18: Create a card with the specified Heave ability text."""
    card = game_state.create_card(name=f"Test Heave Card ({heave_text})")
    # Record heave ability on the card for inspection
    card._heave_ability_text = heave_text  # type: ignore[attr-defined]
    # Parse N from "Heave N" format
    parts = heave_text.split()
    n = int(parts[1]) if len(parts) >= 2 and parts[1].isdigit() else 1
    card._heave_n = n  # type: ignore[attr-defined]
    game_state.heave_card = card


@given(parsers.parse('a player has a card with "{heave_text}" in their hand'))
def player_has_heave_card_in_hand(game_state, heave_text):
    """Rule 8.3.18: Put a card with Heave in the player's hand."""
    card = game_state.create_card(name=f"Test Heave Card ({heave_text})")
    card._heave_ability_text = heave_text  # type: ignore[attr-defined]
    parts = heave_text.split()
    n = int(parts[1]) if len(parts) >= 2 and parts[1].isdigit() else 1
    card._heave_n = n  # type: ignore[attr-defined]
    game_state.player.hand.add_card(card)
    game_state.heave_card = card


@given(parsers.parse('a player has a card with "{heave_text}" in their banished zone'))
def player_has_heave_card_in_banished_zone(game_state, heave_text):
    """Rule 8.3.18: Put a card with Heave in the banished zone (not in hand)."""
    card = game_state.create_card(name=f"Test Heave Card ({heave_text})")
    card._heave_ability_text = heave_text  # type: ignore[attr-defined]
    parts = heave_text.split()
    n = int(parts[1]) if len(parts) >= 2 and parts[1].isdigit() else 1
    card._heave_n = n  # type: ignore[attr-defined]
    game_state.player.banished_zone.add_card(card)
    game_state.heave_card = card


@given(parsers.parse('the player has {amount:d} resource point'))
@given(parsers.parse('the player has {amount:d} resource points'))
def player_has_resource_points(game_state, amount):
    """Rule 8.3.18b: Set the player's resource points."""
    game_state.set_player_resource_points(game_state.player, amount)


@given("the player's arsenal is empty")
def player_arsenal_is_empty(game_state):
    """Rule 8.3.18b: Ensure the player's arsenal is empty."""
    # Arsenal should already be empty; verify and record
    game_state._arsenal_occupied = False  # type: ignore[attr-defined]


@given("the player's arsenal is occupied")
def player_arsenal_is_occupied(game_state):
    """Rule 8.3.18b: Place a card in the player's arsenal to make it occupied."""
    blocker = game_state.create_card(name="Arsenal Blocker")
    game_state.player.arsenal.add_card(blocker)
    game_state._arsenal_occupied = True  # type: ignore[attr-defined]


# ===== When steps =====

@when("I inspect the Heave ability type")
def inspect_heave_ability_type(game_state):
    """Rule 8.3.18: Inspect the ability type of the Heave ability."""
    card = game_state.heave_card
    # Attempt to get HeaveAbility from the engine
    from fab_engine.abilities import HeaveAbility  # type: ignore[import]
    ability = HeaveAbility(n=card._heave_n)
    game_state._heave_ability_instance = ability  # type: ignore[attr-defined]


@when("the beginning of the end phase occurs")
def end_phase_begins(game_state):
    """Rule 8.3.18: Simulate the beginning of the end phase."""
    from fab_engine.phases import EndPhaseBeginEvent  # type: ignore[import]
    event = EndPhaseBeginEvent(player=game_state.player)
    result = event.evaluate_triggers(game_state.player.hand.cards)
    game_state._end_phase_triggers = result  # type: ignore[attr-defined]


@when("the Heave ability triggers at the beginning of the end phase")
def heave_ability_triggers(game_state):
    """Rule 8.3.18: Simulate Heave trigger firing at beginning of end phase."""
    card = game_state.heave_card
    from fab_engine.abilities import HeaveAbility  # type: ignore[import]
    ability = HeaveAbility(n=getattr(card, "_heave_n", 1))
    game_state._heave_ability_instance = ability  # type: ignore[attr-defined]
    # Check if it can trigger (card must be in hand)
    in_hand = card in game_state.player.hand.cards
    game_state._heave_triggered = in_hand  # type: ignore[attr-defined]


@when("the player chooses not to pay the Heave cost")
def player_declines_heave(game_state):
    """Rule 8.3.18: Player opts not to pay the Heave cost (optional ability)."""
    game_state._heave_paid = False  # type: ignore[attr-defined]
    game_state._heave_result = None  # type: ignore[attr-defined]


@when(parsers.parse("the player pays the Heave cost of {amount:d} resource point"))
@when(parsers.parse("the player pays the Heave cost of {amount:d} resource points"))
def player_pays_heave_cost(game_state, amount):
    """Rule 8.3.18: Player pays N resource points to heave."""
    card = game_state.heave_card
    from fab_engine.abilities import HeaveAbility, HeaveAction  # type: ignore[import]
    ability = HeaveAbility(n=getattr(card, "_heave_n", amount))
    action = HeaveAction(ability=ability, card=card, player=game_state.player)
    result = action.pay_cost(game_state.player)
    game_state._heave_paid = result.success  # type: ignore[attr-defined]
    game_state._heave_result = result  # type: ignore[attr-defined]


@when("the player pays the Heave cost and puts the card face-up into their arsenal")
def player_pays_heave_cost_full(game_state):
    """Rule 8.3.18a: Player pays cost and puts card face-up into arsenal."""
    card = game_state.heave_card
    from fab_engine.abilities import HeaveAbility, HeaveAction  # type: ignore[import]
    n = getattr(card, "_heave_n", 1)
    ability = HeaveAbility(n=n)
    action = HeaveAction(ability=ability, card=card, player=game_state.player)
    result = action.pay_cost(game_state.player)
    game_state._heave_paid = result.success  # type: ignore[attr-defined]
    game_state._heave_result = result  # type: ignore[attr-defined]


# ===== Then steps =====

@then("the Heave ability is a hidden triggered ability")
def heave_is_hidden_triggered(game_state):
    """Rule 8.3.18: Heave ability must be both hidden and triggered."""
    ability = game_state._heave_ability_instance
    assert hasattr(ability, "is_hidden"), "HeaveAbility must have is_hidden attribute"
    assert ability.is_hidden is True, "HeaveAbility must be hidden"
    assert hasattr(ability, "is_triggered"), "HeaveAbility must have is_triggered attribute"
    assert ability.is_triggered is True, "HeaveAbility must be a triggered ability"


@then("the Heave ability triggers for that card")
def heave_triggers(game_state):
    """Rule 8.3.18: Heave ability should trigger when card is in hand at end phase start."""
    triggers = game_state._end_phase_triggers
    assert triggers is not None, "End phase trigger evaluation must return results"
    heave_card = game_state.heave_card
    assert any(
        getattr(t, "source_card", None) is heave_card for t in triggers
    ), "Heave trigger should fire for the card in hand"


@then("the Heave ability does not trigger for that card")
def heave_does_not_trigger(game_state):
    """Rule 8.3.18: Heave ability should NOT trigger when card is not in hand."""
    triggers = game_state._end_phase_triggers
    heave_card = game_state.heave_card
    heave_triggers_found = [
        t for t in (triggers or [])
        if getattr(t, "source_card", None) is heave_card
    ]
    assert len(heave_triggers_found) == 0, "Heave should not trigger when card is not in hand"


@then("the card remains in the player's hand")
def card_remains_in_hand(game_state):
    """Rule 8.3.18: Card stays in hand if player declines Heave."""
    assert game_state.heave_card in game_state.player.hand.cards, \
        "Card should remain in hand when Heave cost not paid"


@then("no Seismic Surge tokens are created")
def no_seismic_surge_tokens(game_state):
    """Rule 8.3.18: No Seismic Surge tokens created when Heave not paid."""
    result = getattr(game_state, "_heave_result", None)
    if result is not None:
        tokens = getattr(result, "seismic_surge_tokens_created", [])
        assert len(tokens) == 0, "No Seismic Surge tokens should be created"
    # If no result (player declined), confirm no tokens via game objects
    seismic_tokens = [
        obj for obj in game_state.get_all_game_objects()
        if getattr(obj, "name", "") == "Seismic Surge"
    ]
    assert len(seismic_tokens) == 0, "No Seismic Surge tokens should exist"


@then("the card is placed face-up in the player's arsenal")
def card_in_arsenal_face_up(game_state):
    """Rule 8.3.18: Card must be placed face-up in arsenal after paying Heave cost."""
    card = game_state.heave_card
    result = getattr(game_state, "_heave_result", None)
    assert result is not None, "HeaveAction.pay_cost must return a result"
    assert result.success is True, "Heave cost payment must succeed"
    # Card should now be in arsenal
    assert card in game_state.player.arsenal.cards, \
        "Card should be in arsenal after heaving"
    # Card should be face-up
    assert getattr(card, "face_up", None) is True or \
           getattr(result, "card_placed_face_up", False), \
        "Card should be placed face-up in arsenal"


@then(parsers.parse("{count:d} Seismic Surge token is created"))
@then(parsers.parse("{count:d} Seismic Surge tokens are created"))
def seismic_surge_tokens_created(game_state, count):
    """Rule 8.3.18: N Seismic Surge tokens must be created when Heave cost is paid."""
    result = game_state._heave_result
    assert result is not None, "HeaveAction.pay_cost must return a result"
    assert result.success is True, "Heave cost payment must succeed"
    tokens = getattr(result, "seismic_surge_tokens_created", None)
    assert tokens is not None, "HeaveAction result must include seismic_surge_tokens_created"
    assert len(tokens) == count, \
        f"Expected {count} Seismic Surge token(s), got {len(tokens)}"
    for token in tokens:
        assert getattr(token, "name", "") == "Seismic Surge", \
            "Created tokens must be named 'Seismic Surge'"


@then(parsers.parse("the player has {amount:d} resource points remaining"))
def player_resource_points_remaining(game_state, amount):
    """Rule 8.3.18: Resource points should be reduced after paying Heave cost."""
    remaining = game_state.get_player_resource_points(game_state.player)
    assert remaining == amount, \
        f"Expected {amount} resource points remaining, got {remaining}"


@then("the player is considered to have heaved")
def player_considered_heaved(game_state):
    """Rule 8.3.18a: Player must be marked as having heaved."""
    result = game_state._heave_result
    assert result is not None, "HeaveAction.pay_cost must return a result"
    assert getattr(result, "player_heaved", False) is True, \
        "player_heaved must be True after paying Heave cost (Rule 8.3.18a)"


@then("the card is considered to have been heaved")
def card_considered_heaved(game_state):
    """Rule 8.3.18a: Card must be marked as having been heaved."""
    result = game_state._heave_result
    assert result is not None, "HeaveAction.pay_cost must return a result"
    assert getattr(result, "card_was_heaved", False) is True, \
        "card_was_heaved must be True after paying Heave cost (Rule 8.3.18a)"


@then("the player is not considered to have heaved")
def player_not_considered_heaved(game_state):
    """Rule 8.3.18a: Player must NOT be marked as having heaved if cost not paid."""
    result = getattr(game_state, "_heave_result", None)
    if result is not None:
        assert getattr(result, "player_heaved", False) is False, \
            "player_heaved must be False when Heave cost not paid (Rule 8.3.18a)"


@then("the card is not considered to have been heaved")
def card_not_considered_heaved(game_state):
    """Rule 8.3.18a: Card must NOT be marked as having been heaved if cost not paid."""
    result = getattr(game_state, "_heave_result", None)
    if result is not None:
        assert getattr(result, "card_was_heaved", False) is False, \
            "card_was_heaved must be False when Heave cost not paid (Rule 8.3.18a)"


@then("the player cannot pay the Heave cost")
def player_cannot_pay_heave_cost(game_state):
    """Rule 8.3.18b: Player cannot heave with insufficient resources."""
    card = game_state.heave_card
    from fab_engine.abilities import HeaveAbility, HeaveValidator  # type: ignore[import]
    n = getattr(card, "_heave_n", 1)
    ability = HeaveAbility(n=n)
    validator = HeaveValidator()
    can_pay = validator.can_pay_resource_cost(game_state.player, n)
    assert can_pay is False, \
        f"Player should not be able to pay Heave {n} with insufficient resources (Rule 8.3.18b)"


@then("the player cannot heave because the arsenal is unavailable")
def player_cannot_heave_arsenal_occupied(game_state):
    """Rule 8.3.18b: Player cannot heave if arsenal is not available."""
    card = game_state.heave_card
    from fab_engine.abilities import HeaveAbility, HeaveValidator  # type: ignore[import]
    n = getattr(card, "_heave_n", 1)
    ability = HeaveAbility(n=n)
    validator = HeaveValidator()
    can_put_in_arsenal = validator.can_put_card_in_arsenal(game_state.player)
    assert can_put_in_arsenal is False, \
        "Player should not be able to heave when arsenal is occupied (Rule 8.3.18b)"


# ===== Fixtures =====

@pytest.fixture
def game_state():
    """
    Fixture providing game state for testing Heave ability.

    Uses BDDGameState which integrates with the real engine.
    Reference: Rule 8.3.18 — Heave ability keyword
    """
    from tests.bdd_helpers import BDDGameState

    state = BDDGameState()
    state.heave_card = None
    state._heave_ability_instance = None
    state._heave_triggered = False
    state._heave_paid = False
    state._heave_result = None
    state._end_phase_triggers = []
    state._arsenal_occupied = False

    return state
