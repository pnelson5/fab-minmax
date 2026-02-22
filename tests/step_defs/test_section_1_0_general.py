"""
Step definitions for Section 1.0: General (Rule Hierarchy)
Reference: Flesh and Blood Comprehensive Rules Section 1.0

This module implements behavioral tests for the rule hierarchy in Flesh and Blood:
- Rule 1.0.1: Comprehensive rules apply to all games
- Rule 1.0.1a: Card effects supersede comprehensive rules when they contradict
- Rule 1.0.1b: Tournament rules supersede both comprehensive rules and card effects

NOTE: Section 1.0.2 (Restrictions/Requirements/Allowances precedence) is covered
separately in test_section_1_0_2_precedence.py

Engine Features Needed for Section 1.0:
- [ ] RuleHierarchy (or GameEngine.rule_hierarchy) to represent three-tier hierarchy:
      1. Comprehensive rules (base)
      2. Card effects (supersede rules per 1.0.1a)
      3. Tournament rules (supersede all per 1.0.1b)
- [ ] GameEngine.has_rule_hierarchy() -> bool
- [ ] GameEngine.evaluate_action(action, player_id) -> ActionEvaluationResult
      where ActionEvaluationResult has: permitted (bool), governed_by (str),
      superseded_by (Optional[str])
- [ ] GameEngine.apply_card_effect(action, effect_type, source) to register effects
- [ ] GameEngine.apply_tournament_rule(action, effect_type, source) to register
      tournament-level overrides
- [ ] GameEngine.check_base_rule(action) -> bool (default comprehensive rule)
- [ ] GameEngine.evaluate_default_action(action) -> ActionEvaluationResult
- [ ] GameEngine.get_rule_hierarchy() -> RuleHierarchy
- [ ] RuleHierarchy.highest_priority, second_priority, base_priority properties
- [ ] GameEngine.register_card_effect(card, action, effect_type) for card-based effects

These features will be implemented in a separate task.
Current status: Tests written, Engine pending
"""

import pytest
from pytest_bdd import scenario, given, when, then, parsers


# ============================================================
# Scenario: Comprehensive rules apply to all games of Flesh and Blood
# Tests Rule 1.0.1: The rules in this document apply to any game of FaB
# ============================================================


@scenario(
    "../features/section_1_0_general.feature",
    "Comprehensive rules apply to all games of Flesh and Blood",
)
def test_comprehensive_rules_apply_to_all_games():
    """Rule 1.0.1: Comprehensive rules are the foundation of any FaB game."""
    pass


@given("a game of Flesh and Blood is in progress")
def game_in_progress(game_state):
    """Rule 1.0.1: Establish that a game is being played."""
    # The existence of game_state implies a game is in progress
    assert game_state is not None


@when("the comprehensive rules are consulted")
def comprehensive_rules_consulted(game_state):
    """Rule 1.0.1: Query the rule system."""
    game_state.rule_consulted = True


@then("the rules should govern the game")
def rules_govern_game(game_state):
    """Rule 1.0.1: Verify that the engine has a rule system in place.

    Engine Feature Needed: GameEngine.has_rule_hierarchy() method
    """
    # The game engine must have a rule hierarchy / rule evaluation mechanism
    assert game_state.rule_engine.has_rule_hierarchy()


# ============================================================
# Scenario: Comprehensive rules define default game behavior
# Tests Rule 1.0.1: Rules determine legality of actions by default
# ============================================================


@scenario(
    "../features/section_1_0_general.feature",
    "Comprehensive rules define default game behavior",
)
def test_comprehensive_rules_define_default_behavior():
    """Rule 1.0.1: Comprehensive rules define default behavior when no effects active."""
    pass


@given("no card effects are active")
def no_card_effects_active(game_state):
    """Rule 1.0.1: Clear all effects from game state."""
    game_state.player.clear_restrictions()
    game_state.player.clear_requirements()
    game_state.active_effects = []


@when("a game action is evaluated")
def game_action_evaluated(game_state):
    """Rule 1.0.1: Evaluate legality of an action under base rules.

    Engine Feature Needed: GameEngine.evaluate_default_action(action)
    """
    game_state.action_evaluation = game_state.rule_engine.evaluate_default_action(
        "play_from_hand"
    )


@then("the comprehensive rules determine whether the action is legal")
def comprehensive_rules_determine_legality(game_state):
    """Rule 1.0.1: Base rules apply when no effects are present.

    Engine Feature Needed: ActionEvaluationResult.governed_by attribute
    """
    assert game_state.action_evaluation is not None
    assert game_state.action_evaluation.governed_by == "comprehensive_rules"


# ============================================================
# Scenario: Card effect supersedes a comprehensive rule
# Tests Rule 1.0.1a: If an effect directly contradicts a rule, the effect supersedes
# ============================================================


@scenario(
    "../features/section_1_0_general.feature",
    "Card effect supersedes a comprehensive rule",
)
def test_effect_supersedes_rule():
    """Rule 1.0.1a: Card effect overrides comprehensive rule when they conflict."""
    pass


@given("a comprehensive rule states an action is not normally allowed")
def rule_states_action_not_allowed(game_state):
    """Rule 1.0.1a: Establish base rule that prohibits an action.

    Engine Feature Needed: GameEngine.check_base_rule(action) -> bool
    """
    game_state.tested_action = "play_from_graveyard"
    game_state.base_rule_action = "play_from_graveyard"
    # The base rule says cards cannot be played from graveyard by default
    game_state.base_rule_permits = game_state.rule_engine.check_base_rule(
        "play_from_graveyard"
    )
    assert game_state.base_rule_permits is False


@given("a card effect directly contradicts that rule by allowing the action")
def card_effect_contradicts_rule(game_state):
    """Rule 1.0.1a: Apply card effect that overrides the base rule.

    Engine Feature Needed: GameEngine.apply_card_effect(action, effect_type, source)
    """
    game_state.rule_engine.apply_card_effect(
        action="play_from_graveyard",
        effect_type="allowance",
        source="card_effect",
    )


@then("the card effect takes precedence over the comprehensive rule")
def card_effect_takes_precedence(game_state):
    """Rule 1.0.1a: Verify that the effect overrode the base rule.

    Engine Feature Needed: ActionEvaluationResult.superseded_by attribute
    """
    assert game_state.action_result.superseded_by == "card_effect"


@then("the action is permitted")
def action_is_permitted(game_state):
    """Rule 1.0.1a: Verify the action is allowed due to effect overriding rule.

    Engine Feature Needed: ActionEvaluationResult.permitted attribute
    """
    assert game_state.action_result.permitted is True


# ============================================================
# Scenario: Card effect can override a default restriction from the rules
# Tests Rule 1.0.1a: Effect override of default rule-based restriction
# ============================================================


@scenario(
    "../features/section_1_0_general.feature",
    "Card effect can override a default restriction from the rules",
)
def test_card_effect_overrides_default_rule_restriction():
    """Rule 1.0.1a: A specific card effect overrides a default rule restriction."""
    pass


@given('a player has a card with an effect "you may play this from your graveyard"')
def player_has_graveyard_play_card(game_state):
    """Rule 1.0.1a: Create a card that has a graveyard play effect.

    Engine Feature Needed: GameEngine.register_card_effect(card, action, effect_type)
    """
    from tests.bdd_helpers import TestZone
    from fab_engine.zones.zone import ZoneType

    game_state.graveyard_card = game_state.create_card("Graveyard Effect Card")
    game_state.graveyard_zone.add_card(game_state.graveyard_card)
    # Register the card's effect in the engine
    game_state.rule_engine.register_card_effect(
        card=game_state.graveyard_card,
        action="play_from_graveyard",
        effect_type="allowance",
    )


@given("the default rules state cards cannot be played from the graveyard")
def default_rules_prevent_graveyard_play(game_state):
    """Rule 1.0.1a: Establish the base rule that restricts graveyard play.

    Engine Feature Needed: GameEngine.check_base_rule(action) without registered effects
    """
    # Without any card effect registered, the base rule prohibits graveyard play
    # (Card effect was just registered in the previous step so we use a fresh query)
    base_permitted = game_state.rule_engine.check_base_rule("play_from_graveyard")
    assert base_permitted is False


@when("the player attempts to play the card from the graveyard")
def player_attempts_graveyard_play(game_state):
    """Rule 1.0.1a: Attempt to play the card with the graveyard effect.

    Engine Feature Needed: GameEngine.evaluate_card_play(card, from_zone, player_id)
    """
    game_state.graveyard_play_result = game_state.rule_engine.evaluate_card_play(
        card=game_state.graveyard_card,
        from_zone="graveyard",
        player_id=0,
    )


@then("the card effect supersedes the default rule")
def card_effect_supersedes_default_rule(game_state):
    """Rule 1.0.1a: Verify effect overrode the base rule.

    Engine Feature Needed: ActionEvaluationResult.superseded_by attribute
    """
    assert game_state.graveyard_play_result.superseded_by == "card_effect"


@then("the play attempt is permitted by the effect")
def play_permitted_by_effect(game_state):
    """Rule 1.0.1a: Verify the card effect allows the play.

    Engine Feature Needed: ActionEvaluationResult.permitted attribute
    """
    assert game_state.graveyard_play_result.permitted is True


# ============================================================
# Scenario: Effect supersedes rule but tournament rule supersedes effect
# Tests the full hierarchy: tournament > effect > rule
# ============================================================


@scenario(
    "../features/section_1_0_general.feature",
    "Effect supersedes rule but tournament rule supersedes effect",
)
def test_full_hierarchy_tournament_beats_effect_beats_rule():
    """Rule 1.0.1a/1.0.1b: Full hierarchy: tournament > effect > rule."""
    pass


@given("a card effect grants an allowance")
def card_effect_grants_allowance(game_state):
    """Rule 1.0.1a: Apply a card effect that grants an allowance.

    Engine Feature Needed: GameEngine.apply_card_effect(action, effect_type, source)
    """
    game_state.tested_action = "play_from_graveyard"
    game_state.rule_engine.apply_card_effect(
        action="play_from_graveyard",
        effect_type="allowance",
        source="card_effect",
    )


@then("the tournament rule takes precedence over both the card effect and rule")
def tournament_rule_beats_all(game_state):
    """Rule 1.0.1b: Tournament rule overrides both card effects and base rules.

    Engine Feature Needed: GameEngine.evaluate_action(), ActionEvaluationResult
    """
    result = game_state.rule_engine.evaluate_action(
        action="play_from_graveyard",
        player_id=0,
    )
    assert result.superseded_by == "tournament_rule"
    assert result.permitted is False


# ============================================================
# Scenario: Tournament rule supersedes comprehensive rule
# Tests Rule 1.0.1b: Tournament rules override comprehensive rules
# ============================================================


@scenario(
    "../features/section_1_0_general.feature",
    "Tournament rule supersedes comprehensive rule",
)
def test_tournament_rule_supersedes_comprehensive_rule():
    """Rule 1.0.1b: Tournament rule takes precedence over comprehensive rule."""
    pass


@given("a comprehensive rule permits a certain action")
def comprehensive_rule_permits_action(game_state):
    """Rule 1.0.1b: Establish a base rule that permits an action.

    Engine Feature Needed: GameEngine.check_base_rule(action) -> bool
    """
    # Base rules allow playing from hand
    base_permitted = game_state.rule_engine.check_base_rule("play_from_hand")
    assert base_permitted is True
    game_state.tested_action = "play_from_hand"


@given("a tournament rule prohibits that action")
def tournament_rule_prohibits_comprehensive_allowed_action(game_state):
    """Rule 1.0.1b: Apply tournament rule that overrides the comprehensive rule.

    Engine Feature Needed: GameEngine.apply_tournament_rule(action, effect_type, source)
    """
    game_state.rule_engine.apply_tournament_rule(
        action=game_state.tested_action,
        effect_type="prohibition",
        source="tournament_rule",
    )


@when("the action is attempted")
def action_attempted_with_tournament_rule(game_state):
    """Rule 1.0.1b: Attempt the action with tournament rule active.

    Engine Feature Needed: GameEngine.evaluate_action(action, player_id)
    """
    game_state.action_result = game_state.rule_engine.evaluate_action(
        action=game_state.tested_action,
        player_id=0,
    )


@then("the tournament rule takes precedence")
def tournament_rule_takes_precedence(game_state):
    """Rule 1.0.1b: Verify tournament rule overrides the comprehensive rule.

    Engine Feature Needed: ActionEvaluationResult.superseded_by
    """
    assert game_state.action_result.superseded_by == "tournament_rule"


@then("the action is prohibited")
def action_is_prohibited(game_state):
    """Rule 1.0.1b: Verify the action is blocked by tournament rule.

    Engine Feature Needed: ActionEvaluationResult.permitted
    """
    assert game_state.action_result.permitted is False


# ============================================================
# Scenario: Tournament rule supersedes card effect
# Tests Rule 1.0.1b: Tournament rules even override card effects
# ============================================================


@scenario(
    "../features/section_1_0_general.feature",
    "Tournament rule supersedes card effect",
)
def test_tournament_rule_supersedes_card_effect():
    """Rule 1.0.1b: Tournament rules supersede card effects."""
    pass


@given("a card effect permits a certain action")
def card_effect_permits_action(game_state):
    """Rule 1.0.1b: Apply a card effect that permits an action.

    Engine Feature Needed: GameEngine.apply_card_effect(action, effect_type, source)
    """
    game_state.rule_engine.apply_card_effect(
        action="play_from_graveyard",
        effect_type="allowance",
        source="card_effect",
    )
    game_state.tested_action = "play_from_graveyard"


@when("the action is attempted under tournament conditions")
def action_attempted_under_tournament(game_state):
    """Rule 1.0.1b: Attempt action with both card effect and tournament rule active.

    Engine Feature Needed: GameEngine.evaluate_action(action, player_id)
    """
    game_state.action_result = game_state.rule_engine.evaluate_action(
        action=game_state.tested_action,
        player_id=0,
    )


@then("the tournament rule takes precedence over the card effect")
def tournament_beats_card_effect(game_state):
    """Rule 1.0.1b: Tournament rule has higher priority than card effects.

    Engine Feature Needed: ActionEvaluationResult.superseded_by
    """
    assert game_state.action_result.superseded_by == "tournament_rule"


# ============================================================
# Scenario: Rule hierarchy has correct priority ordering
# Tests Rule 1.0.1/1.0.1a/1.0.1b: The full three-tier hierarchy
# ============================================================


@scenario(
    "../features/section_1_0_general.feature",
    "Rule hierarchy has correct priority ordering",
)
def test_rule_hierarchy_priority_ordering():
    """Rule 1.0.1/1.0.1a/1.0.1b: Verify full three-tier rule hierarchy."""
    pass


@given("the game engine has a rule hierarchy")
def engine_has_rule_hierarchy(game_state):
    """Rule 1.0.1: The engine must implement a rule hierarchy.

    Engine Feature Needed: GameEngine.has_rule_hierarchy() -> bool
    """
    assert game_state.rule_engine.has_rule_hierarchy()


@when("the hierarchy levels are examined")
def hierarchy_levels_examined(game_state):
    """Rule 1.0.1: Query the rule hierarchy structure.

    Engine Feature Needed: GameEngine.get_rule_hierarchy() -> RuleHierarchy
    """
    game_state.hierarchy = game_state.rule_engine.get_rule_hierarchy()


@then("tournament rules should have the highest priority")
def tournament_rules_highest_priority(game_state):
    """Rule 1.0.1b: Tournament rules override everything.

    Engine Feature Needed: RuleHierarchy.highest_priority property
    """
    assert game_state.hierarchy.highest_priority == "tournament_rules"


@then("card effects should have the second highest priority")
def card_effects_second_priority(game_state):
    """Rule 1.0.1a: Card effects override comprehensive rules.

    Engine Feature Needed: RuleHierarchy.second_priority property
    """
    assert game_state.hierarchy.second_priority == "card_effects"


@then("comprehensive rules should have the base priority")
def comprehensive_rules_base_priority(game_state):
    """Rule 1.0.1: Comprehensive rules are the base/default.

    Engine Feature Needed: RuleHierarchy.base_priority property
    """
    assert game_state.hierarchy.base_priority == "comprehensive_rules"


# ============================================================
# Fixtures
# ============================================================


class RuleEngineProxy:
    """
    Proxy object representing the rule hierarchy engine.

    This proxy is expected to FAIL with AttributeError or similar errors
    because the actual engine does not yet implement rule hierarchy APIs.

    This is intentional: the test failures document what the engine needs.

    Engine Features Needed:
    - has_rule_hierarchy() -> bool
    - evaluate_action(action, player_id) -> ActionEvaluationResult
    - evaluate_default_action(action) -> ActionEvaluationResult
    - apply_card_effect(action, effect_type, source) -> None
    - apply_tournament_rule(action, effect_type, source) -> None
    - check_base_rule(action) -> bool
    - evaluate_card_play(card, from_zone, player_id) -> ActionEvaluationResult
    - register_card_effect(card, action, effect_type) -> None
    - get_rule_hierarchy() -> RuleHierarchy
    """

    def has_rule_hierarchy(self) -> bool:
        """Rule 1.0.1: Engine must have a rule hierarchy."""
        from fab_engine.engine.game import GameEngine

        # GameEngine does not yet have has_rule_hierarchy() method
        # This will raise AttributeError - expected missing engine feature
        engine = GameEngine.__new__(GameEngine)
        return engine.has_rule_hierarchy()

    def evaluate_default_action(self, action: str):
        """Rule 1.0.1: Evaluate an action against base rules only."""
        from fab_engine.engine.game import GameEngine

        engine = GameEngine.__new__(GameEngine)
        return engine.evaluate_default_action(action)

    def evaluate_action(self, action: str, player_id: int):
        """Rule 1.0.1a/b: Evaluate an action considering full hierarchy."""
        from fab_engine.engine.game import GameEngine

        engine = GameEngine.__new__(GameEngine)
        return engine.evaluate_action(action=action, player_id=player_id)

    def apply_card_effect(self, action: str, effect_type: str, source: str):
        """Rule 1.0.1a: Register a card effect that overrides a rule."""
        from fab_engine.engine.game import GameEngine

        engine = GameEngine.__new__(GameEngine)
        return engine.apply_card_effect(
            action=action, effect_type=effect_type, source=source
        )

    def apply_tournament_rule(self, action: str, effect_type: str, source: str):
        """Rule 1.0.1b: Register a tournament rule override."""
        from fab_engine.engine.game import GameEngine

        engine = GameEngine.__new__(GameEngine)
        return engine.apply_tournament_rule(
            action=action, effect_type=effect_type, source=source
        )

    def check_base_rule(self, action: str) -> bool:
        """Rule 1.0.1: Query the comprehensive rule for an action."""
        from fab_engine.engine.game import GameEngine

        engine = GameEngine.__new__(GameEngine)
        return engine.check_base_rule(action)

    def evaluate_card_play(self, card, from_zone: str, player_id: int):
        """Rule 1.0.1a: Evaluate playing a specific card from a specific zone."""
        from fab_engine.engine.game import GameEngine

        engine = GameEngine.__new__(GameEngine)
        return engine.evaluate_card_play(
            card=card, from_zone=from_zone, player_id=player_id
        )

    def register_card_effect(self, card, action: str, effect_type: str):
        """Rule 1.0.1a: Register a card-specific effect."""
        from fab_engine.engine.game import GameEngine

        engine = GameEngine.__new__(GameEngine)
        return engine.register_card_effect(
            card=card, action=action, effect_type=effect_type
        )

    def get_rule_hierarchy(self):
        """Rule 1.0.1/1.0.1a/1.0.1b: Get the rule hierarchy structure."""
        from fab_engine.engine.game import GameEngine

        engine = GameEngine.__new__(GameEngine)
        return engine.get_rule_hierarchy()


@pytest.fixture
def game_state():
    """
    Fixture providing game state for Section 1.0 General tests.

    Uses BDDGameState extended with a RuleEngineProxy for rule hierarchy testing.
    The RuleEngineProxy attempts to call methods on GameEngine that do not yet exist.
    Tests will fail with AttributeError on GameEngine methods - this is EXPECTED.

    Reference: Rule 1.0.1, 1.0.1a, 1.0.1b

    Engine Features Needed (cause test failures):
    - GameEngine.has_rule_hierarchy() -> bool
    - GameEngine.evaluate_action(action, player_id) -> ActionEvaluationResult
    - GameEngine.apply_card_effect(action, effect_type, source)
    - GameEngine.apply_tournament_rule(action, effect_type, source)
    - GameEngine.check_base_rule(action) -> bool
    - GameEngine.evaluate_default_action(action) -> ActionEvaluationResult
    - GameEngine.evaluate_card_play(card, from_zone, player_id)
    - GameEngine.register_card_effect(card, action, effect_type)
    - GameEngine.get_rule_hierarchy() -> RuleHierarchy
    - RuleHierarchy class with highest_priority, second_priority, base_priority
    - ActionEvaluationResult with permitted, governed_by, superseded_by attributes
    """
    from tests.bdd_helpers import BDDGameState
    from fab_engine.zones.zone import ZoneType
    from tests.bdd_helpers import TestZone

    state = BDDGameState()

    # Graveyard zone for testing graveyard-play effects (Rule 1.0.1a)
    state.graveyard_zone = TestZone(ZoneType.GRAVEYARD, 0)

    # Rule engine proxy - calls methods that don't yet exist on GameEngine
    state.rule_engine = RuleEngineProxy()

    # Additional state storage for test results
    state.rule_consulted = False
    state.active_effects = []
    state.action_evaluation = None
    state.action_result = None
    state.graveyard_card = None
    state.graveyard_play_result = None
    state.tested_action = None
    state.hierarchy = None
    state.base_rule_action = None
    state.base_rule_permits = None

    return state
