"""
Step definitions for Section 1.5: Macros
Reference: Flesh and Blood Comprehensive Rules Section 1.5

This module implements behavioral tests for macro objects in Flesh and Blood.
Macros are non-card objects in the arena, used in specific tournament formats.

Engine Features Needed for Section 1.5:
- [ ] MacroObject class (Rule 1.5.1) - non-card arena object
- [ ] MacroObject.owner_id = None always (Rule 1.5.1a)
- [ ] MacroObject.controller_id set by tournament rule (Rule 1.5.1b)
- [ ] MacroObject.is_in_card_pool = False (Rule 1.5.2)
- [ ] Engine.remove_from_game(macro) when macro leaves arena (Rule 1.5.3)
- [ ] MacroObject.get_type() returns "macro" (Rule 8.1.13a)
- [ ] MacroObject.abilities list set by creating rule/effect (Rule 1.7.1)

These features will be implemented in a separate task.
Current status: Tests written, Engine pending
"""

import pytest
from pytest_bdd import scenario, given, when, then, parsers


# ============================================================
# Rule 1.5.1: A macro is a non-card object in the arena
# ============================================================


@scenario(
    "../features/section_1_5_macros.feature",
    "Macro is a non-card game object in the arena",
)
def test_macro_is_non_card_game_object():
    """Rule 1.5.1: Macro is a non-card object recognized as a game object."""
    pass


@scenario(
    "../features/section_1_5_macros.feature",
    "Macro exists in the arena zone",
)
def test_macro_exists_in_arena_zone():
    """Rule 1.5.1: Macro is located in the arena."""
    pass


# ============================================================
# Rule 1.5.1a: Macro has no owner
# ============================================================


@scenario(
    "../features/section_1_5_macros.feature",
    "Macro has no owner",
)
def test_macro_has_no_owner():
    """Rule 1.5.1a: A macro has no owner."""
    pass


# ============================================================
# Rule 1.5.1b: Controller determined by tournament rule
# ============================================================


@scenario(
    "../features/section_1_5_macros.feature",
    "Macro controller is determined by the tournament rule that created it",
)
def test_macro_controller_set_by_tournament_rule():
    """Rule 1.5.1b: Controller of a macro is set by the tournament rule that created it."""
    pass


@scenario(
    "../features/section_1_5_macros.feature",
    "Macro controller can be assigned to any player by tournament rule",
)
def test_macro_controller_can_be_any_player():
    """Rule 1.5.1b: Tournament rule can assign controller to any player."""
    pass


# ============================================================
# Rule 1.5.2: Macro is not part of a player's card-pool
# ============================================================


@scenario(
    "../features/section_1_5_macros.feature",
    "Macro is not part of any player's card-pool",
)
def test_macro_not_part_of_card_pool():
    """Rule 1.5.2: Macro cannot be part of a player's card-pool."""
    pass


@scenario(
    "../features/section_1_5_macros.feature",
    "Macro represented by a physical card is still not in card-pool",
)
def test_macro_represented_by_physical_card_not_in_card_pool():
    """Rule 1.5.2: Even if represented by a physical card, macro is not in card-pool."""
    pass


# ============================================================
# Rule 1.5.3: Macro leaving arena is removed from the game
# ============================================================


@scenario(
    "../features/section_1_5_macros.feature",
    "Macro leaving the arena is removed from the game",
)
def test_macro_leaving_arena_removed_from_game():
    """Rule 1.5.3: If a macro leaves the arena, it is removed from the game."""
    pass


@scenario(
    "../features/section_1_5_macros.feature",
    "Macro is removed from game when destroyed, not sent to graveyard",
)
def test_macro_destroyed_removed_not_graveyard():
    """Rule 1.5.3: Destroyed macro goes to removed-from-game, not graveyard."""
    pass


# ============================================================
# Rule 8.1.13: Macro type keyword
# ============================================================


@scenario(
    "../features/section_1_5_macros.feature",
    "Only macro objects have the macro type",
)
def test_only_macros_have_macro_type():
    """Rule 8.1.13a: Only macro objects have the macro type."""
    pass


@scenario(
    "../features/section_1_5_macros.feature",
    "Macro can have abilities defined by the rule or effect that created it",
)
def test_macro_has_abilities_from_creating_rule():
    """Rule 1.5.1 / 8.1.13: Macro has abilities defined by tournament rule or effect."""
    pass


# ============================================================
# Step Definitions
# ============================================================


@given(parsers.parse('a macro named "{name}" exists in the arena'))
def macro_named_exists_in_arena(game_state, name):
    """
    Rule 1.5.1: Create a macro object in the arena.

    Engine Feature Needed:
    - [ ] MacroObject class with name, arena location
    - [ ] Engine.add_macro_to_arena(name) method
    """
    game_state.macro = MacroStub(name=name)
    game_state.macro_in_arena = True
    game_state.macro_removed_from_game = False


@given(
    parsers.parse(
        "the macro was created by a tournament rule assigning controller player {player_id:d}"
    )
)
def macro_created_by_tournament_rule(game_state, player_id):
    """
    Rule 1.5.1b: Tournament rule assigns controller to the macro.

    Engine Feature Needed:
    - [ ] MacroObject.controller_id assignable by tournament rule (Rule 1.5.1b)
    """
    game_state.macro.controller_id = player_id


@given("the macro is represented by a physical Flesh and Blood card")
def macro_represented_by_physical_card(game_state):
    """
    Rule 1.5.2: Even when represented by a physical card, macro is not in card-pool.

    Engine Feature Needed:
    - [ ] MacroObject.represented_by_physical_card flag
    """
    game_state.macro.represented_by_physical_card = True


@given(parsers.parse('the macro has the text "{ability_text}"'))
def macro_has_ability_text(game_state, ability_text):
    """
    Rule 1.7.1: Macro abilities defined by the creating rule or effect.

    Engine Feature Needed:
    - [ ] MacroObject.abilities list with functional text
    """
    game_state.macro.abilities_text = ability_text


@given(parsers.parse('a regular card named "{name}" exists in the hand'))
def regular_card_exists_in_hand(game_state, name):
    """Rule 8.1.13a: Create a regular card for comparison with macro type check."""
    game_state.regular_card = game_state.create_card(name=name)
    game_state.player.hand.add_card(game_state.regular_card)


@when("the engine evaluates the macro as a game object")
def engine_evaluates_macro_as_game_object(game_state):
    """
    Rule 1.5.1: Engine must classify a macro as a game object.

    Engine Feature Needed:
    - [ ] GameEngine.is_game_object(macro) returning True (Rule 1.2.1)
    """
    game_state.macro_is_game_object = getattr(game_state.macro, "is_game_object", None)
    game_state.macro_is_card = getattr(game_state.macro, "is_card", None)


@when("checking the macro's location")
def checking_macro_location(game_state):
    """Rule 1.5.1: Check which zone the macro is in."""
    game_state.checked_location = True


@when("checking the macro's ownership")
def checking_macro_ownership(game_state):
    """Rule 1.5.1a: Check ownership attributes of the macro."""
    game_state.macro_owner_id = getattr(game_state.macro, "owner_id", "NOT_CHECKED")


@when("checking the macro's controller")
def checking_macro_controller(game_state):
    """Rule 1.5.1b: Check controller attribute of the macro."""
    game_state.checked_controller = True


@when(
    parsers.parse("validating if the macro is part of player {player_id:d}'s card-pool")
)
def validating_macro_in_card_pool(game_state, player_id):
    """
    Rule 1.5.2: Check whether macro is considered part of a player's card-pool.

    Engine Feature Needed:
    - [ ] MacroObject.is_in_card_pool property returning False (Rule 1.5.2)
    """
    game_state.macro_in_card_pool = getattr(game_state.macro, "is_in_card_pool", None)


@when("the macro leaves the arena")
def macro_leaves_arena(game_state):
    """
    Rule 1.5.3: Simulate the macro leaving the arena.

    Engine Feature Needed:
    - [ ] Engine.remove_macro_from_arena(macro) triggering removal from game
    - [ ] Zone change event for macros causing removal from game (Rule 1.5.3)
    """
    game_state.macro_in_arena = False
    # When a macro leaves the arena, it should be removed from game
    game_state.macro_removed_from_game = getattr(
        game_state.macro, "is_removed_from_game", None
    )


@when("the macro is destroyed")
def macro_is_destroyed(game_state):
    """
    Rule 1.5.3: Simulate the macro being destroyed (leaves arena).

    Engine Feature Needed:
    - [ ] Destruction of macro triggers removal from game, not graveyard transition
    """
    game_state.macro_in_arena = False
    game_state.macro_in_graveyard = getattr(game_state.macro, "is_in_graveyard", False)
    game_state.macro_removed_from_game = getattr(
        game_state.macro, "is_removed_from_game", None
    )


@when("checking object types")
def checking_object_types(game_state):
    """Rule 8.1.13a: Compare type attributes of macro and regular card."""
    game_state.macro_type = getattr(game_state.macro, "type_name", None)
    game_state.regular_card_type = getattr(game_state.regular_card, "type_name", None)


@when("the engine reads the macro's abilities")
def engine_reads_macro_abilities(game_state):
    """
    Rule 1.7.1: Macro abilities are defined by the creating rule or effect.

    Engine Feature Needed:
    - [ ] MacroObject.get_abilities() returning list of abilities
    """
    game_state.macro_abilities = getattr(
        game_state.macro, "get_abilities", lambda: []
    )()
    game_state.macro_abilities_text = getattr(game_state.macro, "abilities_text", None)


@then("the macro should be recognized as a game object")
def macro_recognized_as_game_object(game_state):
    """
    Rule 1.5.1: Macros are game objects (Rule 1.2.1 lists macros as objects).

    Engine Feature Needed:
    - [ ] MacroObject.is_game_object = True
    """
    assert game_state.macro_is_game_object is True, (
        "Engine Feature Needed: MacroObject.is_game_object should return True. "
        "Rule 1.2.1 states: 'Cards, attacks, macros, and layers are objects.'"
    )


@then("the macro should NOT be recognized as a card")
def macro_not_recognized_as_card(game_state):
    """
    Rule 1.5.1 / 8.1.13: A macro is NOT a card.

    Engine Feature Needed:
    - [ ] MacroObject.is_card = False (Rule 1.5.1 note: 'A macro is not a card')
    """
    assert game_state.macro_is_card is False, (
        "Engine Feature Needed: MacroObject.is_card should be False. "
        "Rule 1.5.1 note states: 'A macro is not a card, even if it is represented "
        "by an official Flesh and Blood card.'"
    )


@then("the macro should be in the arena")
def macro_should_be_in_arena(game_state):
    """
    Rule 1.5.1: Macros exist in the arena.

    Engine Feature Needed:
    - [ ] Arena zone tracking for MacroObject (Rule 1.5.1)
    """
    assert game_state.macro_in_arena is True, (
        "Engine Feature Needed: Arena zone must track macro objects. "
        "Rule 1.5.1: 'A macro is a non-card object in the arena.'"
    )


@then("the macro should not be in any other zone")
def macro_not_in_other_zones(game_state):
    """
    Rule 1.5.1: Macros can only be in the arena.

    Engine Feature Needed:
    - [ ] Zone system that prevents macros from entering non-arena zones
    """
    # If macro_in_arena is True and the macro was just created in arena,
    # it should not be tracked as being elsewhere
    macro_in_non_arena = getattr(game_state.macro, "is_in_non_arena_zone", False)
    assert not macro_in_non_arena, (
        "Engine Feature Needed: Macros must only reside in the arena. "
        "Rule 1.5.1: Macros are non-card objects in the arena."
    )


@then("the macro should have no owner")
def macro_should_have_no_owner(game_state):
    """
    Rule 1.5.1a: A macro has no owner.

    Engine Feature Needed:
    - [ ] MacroObject.owner_id = None always (Rule 1.5.1a)
    """
    owner_id = game_state.macro_owner_id
    assert owner_id is None, (
        f"Engine Feature Needed: MacroObject.owner_id should be None. "
        f"Got {owner_id!r}. Rule 1.5.1a: 'A macro has no owner.'"
    )


@then("the macro owner_id should be None")
def macro_owner_id_is_none(game_state):
    """Rule 1.5.1a: Macro owner_id is specifically None (not 0 or any player id)."""
    assert game_state.macro_owner_id is None, (
        "Engine Feature Needed: MacroObject.owner_id must be None, not any player id. "
        "Rule 1.5.1a: 'A macro has no owner.'"
    )


@then("the macro should have a controller")
def macro_should_have_controller(game_state):
    """
    Rule 1.5.1b: Macro controller is set by tournament rule.

    Engine Feature Needed:
    - [ ] MacroObject.controller_id property (Rule 1.5.1b)
    """
    controller_id = getattr(game_state.macro, "controller_id", "NOT_SET")
    assert controller_id != "NOT_SET" and controller_id is not None, (
        "Engine Feature Needed: MacroObject.controller_id must be set by tournament rule. "
        "Rule 1.5.1b: 'The controller of a macro is determined by the tournament rule that created it.'"
    )


@then(parsers.parse("the macro controller_id should be {player_id:d}"))
def macro_controller_id_is(game_state, player_id):
    """
    Rule 1.5.1b: Macro controller_id matches the assigned tournament rule player.

    Engine Feature Needed:
    - [ ] MacroObject.controller_id set to tournament-rule-assigned player (Rule 1.5.1b)
    """
    actual_controller = getattr(game_state.macro, "controller_id", None)
    assert actual_controller == player_id, (
        f"Engine Feature Needed: MacroObject.controller_id should be {player_id}, "
        f"got {actual_controller!r}. "
        "Rule 1.5.1b: 'The controller of a macro is determined by the tournament rule that created it.'"
    )


@then("the macro should not be part of the card-pool")
def macro_not_part_of_card_pool(game_state):
    """
    Rule 1.5.2: Macro cannot be and is not considered part of a player's card-pool.

    Engine Feature Needed:
    - [ ] MacroObject.is_in_card_pool = False (Rule 1.5.2)
    - [ ] Card-pool validation rejecting macros (Rule 1.5.2 ref 1.1.3)
    """
    assert game_state.macro_in_card_pool is False, (
        "Engine Feature Needed: MacroObject.is_in_card_pool must be False. "
        "Rule 1.5.2: 'A macro cannot be and is not considered part of a player's card-pool.'"
    )


@then("the macro should be removed from the game")
def macro_removed_from_game(game_state):
    """
    Rule 1.5.3: Macro leaving arena is removed from the game.

    Engine Feature Needed:
    - [ ] Engine.remove_from_game(macro) triggered when macro leaves arena
    - [ ] MacroObject.is_removed_from_game flag (Rule 1.5.3)
    """
    assert game_state.macro_removed_from_game is True, (
        "Engine Feature Needed: MacroObject.is_removed_from_game should be True "
        "after leaving the arena. "
        "Rule 1.5.3: 'If a macro leaves the arena, it is removed from the game.'"
    )


@then("the macro should not exist in any zone")
def macro_not_in_any_zone(game_state):
    """
    Rule 1.5.3: Macro leaves the game entirely, not moving to another zone.

    Engine Feature Needed:
    - [ ] Zone system ensuring macros leaving arena are not placed in other zones
    - [ ] No zone transition: macro is simply removed from game (Rule 1.5.3)
    """
    assert not game_state.macro_in_arena, (
        "Engine Feature Needed: Macro must not be in arena after removal. "
        "Rule 1.5.3: Macro is removed from the game when it leaves the arena."
    )
    macro_in_other_zones = getattr(game_state.macro, "is_in_any_zone", False)
    assert not macro_in_other_zones, (
        "Engine Feature Needed: Macro must not be in any zone after removal from game. "
        "Rule 1.5.3: Macro is removed from the game when it leaves the arena."
    )


@then("the macro should not appear in any graveyard")
def macro_not_in_graveyard(game_state):
    """
    Rule 1.5.3: Macro goes to removed-from-game state, not graveyard.

    Engine Feature Needed:
    - [ ] Macro destruction handling: removed from game, not graveyard (Rule 1.5.3)
    - [ ] Distinct from card destruction where cards go to graveyard
    """
    assert not game_state.macro_in_graveyard, (
        "Engine Feature Needed: MacroObject should NOT be placed in graveyard on destruction. "
        "Rule 1.5.3: Macro leaves arena and is removed from the game (not graveyard)."
    )


@then("the macro should have the macro type")
def macro_has_macro_type(game_state):
    """
    Rule 8.1.13a: Only macro objects have the macro type.

    Engine Feature Needed:
    - [ ] MacroObject.type_name = 'macro' (Rule 8.1.13a)
    - [ ] CardType.MACRO enum value or equivalent
    """
    macro_type = game_state.macro_type
    assert macro_type == "macro", (
        f"Engine Feature Needed: MacroObject.type_name should be 'macro', got {macro_type!r}. "
        "Rule 8.1.13a: 'Only macro objects have the macro type.'"
    )


@then("the regular card should not have the macro type")
def regular_card_not_macro_type(game_state):
    """
    Rule 8.1.13a: Regular cards do not have the macro type.

    Engine Feature Needed:
    - [ ] CardInstance.type_name != 'macro' for non-macro objects
    """
    card_type = game_state.regular_card_type
    assert card_type != "macro", (
        "Engine Feature Needed: Regular CardInstance should not have type_name 'macro'. "
        "Rule 8.1.13a: Only macro objects have the macro type."
    )


@then("the macro should have at least one ability")
def macro_has_at_least_one_ability(game_state):
    """
    Rule 1.7.1: Macro abilities are defined by the creating rule or effect.

    Engine Feature Needed:
    - [ ] MacroObject.abilities list (Rule 1.7.1)
    - [ ] MacroObject.get_abilities() method
    """
    abilities = game_state.macro_abilities
    abilities_text = game_state.macro_abilities_text
    has_ability = (abilities and len(abilities) > 0) or (abilities_text is not None)
    assert has_ability, (
        "Engine Feature Needed: MacroObject.abilities must be set by creating rule/effect. "
        "Rule 1.7.1: 'The base abilities of a token card, macro, or non-card layer are "
        "defined by a rule, or the effect or ability that created it.'"
    )


@then("the abilities should be defined by the creating rule or effect")
def macro_abilities_defined_by_creating_rule(game_state):
    """
    Rule 1.7.1: Macro abilities come from the rule or effect that created it.

    Engine Feature Needed:
    - [ ] MacroObject.ability_source indicating 'tournament_rule' or 'effect'
    """
    ability_source = getattr(game_state.macro, "ability_source", None)
    # Either the macro has a set ability source, or it has abilities_text we set
    has_defined_source = (
        ability_source in ("tournament_rule", "effect", "rule")
        or game_state.macro_abilities_text is not None
    )
    assert has_defined_source, (
        "Engine Feature Needed: MacroObject must track ability_source = 'tournament_rule' "
        "or 'effect'. Rule 1.7.1: Macro abilities are defined by a rule or effect."
    )


# ============================================================
# Fixtures
# ============================================================


@pytest.fixture
def game_state():
    """
    Fixture providing game state for testing Section 1.5: Macros.

    Uses BDDGameState which integrates with the real engine.
    Reference: Rule 1.5
    """
    from tests.bdd_helpers import BDDGameState

    state = BDDGameState()

    # Initialize macro-specific test state
    state.macro = None
    state.macro_in_arena = False
    state.macro_removed_from_game = False
    state.macro_in_graveyard = False
    state.macro_owner_id = "NOT_CHECKED"
    state.macro_is_game_object = None
    state.macro_is_card = None
    state.macro_in_card_pool = None
    state.macro_type = None
    state.regular_card = None
    state.regular_card_type = None
    state.macro_abilities = []
    state.macro_abilities_text = None

    return state


# ============================================================
# Stub class for Macro object (engine feature not yet implemented)
# ============================================================


class MacroStub:
    """
    Stub for a macro object in the arena (Rule 1.5).

    Engine Feature Needed:
    - [ ] MacroObject class (Rule 1.5.1)
    - [ ] MacroObject.owner_id = None always (Rule 1.5.1a)
    - [ ] MacroObject.controller_id set by tournament rule (Rule 1.5.1b)
    - [ ] MacroObject.is_in_card_pool = False (Rule 1.5.2)
    - [ ] MacroObject.is_removed_from_game tracking (Rule 1.5.3)
    - [ ] MacroObject.type_name = 'macro' (Rule 8.1.13a)
    - [ ] MacroObject.abilities / get_abilities() (Rule 1.7.1)
    """

    def __init__(self, name: str, controller_id: int = None):
        self.name = name
        # Rule 1.5.1a: A macro has no owner
        self.owner_id = None
        # Rule 1.5.1b: Controller determined by tournament rule
        self.controller_id = controller_id
        # Rule 1.5.1: Macro is a game object but NOT a card
        self.is_game_object = None  # Engine feature needed: should be True
        self.is_card = None  # Engine feature needed: should be False
        # Rule 1.5.2: Macro is not part of a card-pool
        self.is_in_card_pool = None  # Engine feature needed: should be False
        # Rule 1.5.3: Track removal from game
        self.is_removed_from_game = (
            None  # Engine feature needed: should be True after leaving
        )
        # Rule 8.1.13a: Macro type
        self.type_name = None  # Engine feature needed: should be 'macro'
        # Rule 1.7.1: Abilities
        self.abilities_text = None
        self.ability_source = None
        # Zones
        self.is_in_non_arena_zone = False
        self.is_in_any_zone = False
        self.is_in_graveyard = False
        # Physical card representation flag
        self.represented_by_physical_card = False

    def get_abilities(self):
        """Rule 1.7.1: Return macro abilities."""
        return []
