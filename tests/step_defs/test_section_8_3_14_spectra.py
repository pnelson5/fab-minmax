"""
Step definitions for Section 8.3.14: Spectra (Ability Keyword)
Reference: Flesh and Blood Comprehensive Rules Section 8.3.14

This module implements behavioral tests for the Spectra ability keyword:
- Spectra is both a static ability and a triggered-static ability (Rule 8.3.14)
- Static ability: "this can be attacked" (Rule 8.3.14)
- Triggered-static ability: "When this becomes the target of an attack, destroy this." (Rule 8.3.14)
- Rule 8.3.14a: An object with Spectra can be the target of an attack, even if it is not a
  living object.
- Rule 8.3.14b: When an object with Spectra becomes the target of an attack, a triggered-layer
  is put on the stack. When the triggered-layer resolves, the object with Spectra is destroyed.
  If there are no other legal attack-targets, the combat chain closes.

Engine Features Needed for Section 8.3.14:
- [ ] AbilityKeyword.SPECTRA on cards (Rule 8.3.14)
- [ ] SpectraAbility.is_static -> True (Rule 8.3.14 - makes object attackable)
- [ ] SpectraAbility.is_triggered_static -> True (Rule 8.3.14 - destroys object when attacked)
- [ ] SpectraAbility.makes_attackable() -> bool (Rule 8.3.14a - allows non-living object to be attacked)
- [ ] AttackTargetValidator.is_legal_target(obj) respects Spectra static ability (Rule 8.3.14a)
- [ ] SpectraAbility.create_triggered_layer() -> TriggeredLayer (Rule 8.3.14b)
- [ ] TriggeredLayer.resolve() destroys the Spectra object (Rule 8.3.14b)
- [ ] CombatChain.close() triggered when Spectra object destroyed and no other legal targets (Rule 8.3.14b)
- [ ] CombatChain.has_legal_attack_targets() -> bool (Rule 8.3.14b)

Current status: Tests written, Engine pending
"""

import pytest
from pytest_bdd import scenario, given, when, then, parsers


# ===== Rule 8.3.14: Spectra is classified as an ability keyword =====

@scenario(
    "../features/section_8_3_14_spectra.feature",
    "Spectra is classified as an ability keyword",
)
def test_spectra_is_ability_keyword():
    """Rule 8.3.14: Spectra is listed as an ability keyword in Section 8.3."""
    pass


# ===== Rule 8.3.14a: A non-living object with Spectra can be attacked =====

@scenario(
    "../features/section_8_3_14_spectra.feature",
    "A non-living object with Spectra can be the target of an attack",
)
def test_non_living_spectra_object_is_legal_attack_target():
    """Rule 8.3.14a: A non-living object with Spectra can be the target of an attack."""
    pass


# ===== Rule 8.3.14a: A non-living object without Spectra cannot be attacked =====

@scenario(
    "../features/section_8_3_14_spectra.feature",
    "A non-living object without Spectra cannot be the target of an attack",
)
def test_non_living_object_without_spectra_is_not_legal_attack_target():
    """Rule 8.3.14a: A non-living object without Spectra is not a legal attack target."""
    pass


# ===== Rule 8.3.14b: Triggered-layer placed on stack when Spectra object is attacked =====

@scenario(
    "../features/section_8_3_14_spectra.feature",
    "A triggered-layer is placed on the stack when a Spectra object becomes the target of an attack",
)
def test_triggered_layer_placed_when_spectra_attacked():
    """Rule 8.3.14b: When a Spectra object becomes the target of an attack, a triggered-layer is put on the stack."""
    pass


# ===== Rule 8.3.14b: Spectra object is destroyed when triggered-layer resolves =====

@scenario(
    "../features/section_8_3_14_spectra.feature",
    "A Spectra object is destroyed when the triggered-layer resolves",
)
def test_spectra_object_destroyed_when_triggered_layer_resolves():
    """Rule 8.3.14b: When the triggered-layer resolves, the Spectra object is destroyed."""
    pass


# ===== Rule 8.3.14b: Combat chain closes when no other legal attack targets =====

@scenario(
    "../features/section_8_3_14_spectra.feature",
    "Combat chain closes when Spectra object is destroyed and there are no other legal attack targets",
)
def test_combat_chain_closes_when_no_other_targets():
    """Rule 8.3.14b: If there are no other legal attack-targets, the combat chain closes."""
    pass


# ===== Rule 8.3.14b: Combat chain does not close when other legal attack targets exist =====

@scenario(
    "../features/section_8_3_14_spectra.feature",
    "Combat chain does not close when Spectra object is destroyed and there are other legal attack targets",
)
def test_combat_chain_does_not_close_when_other_targets_exist():
    """Rule 8.3.14b: If there are other legal attack-targets, the combat chain does not close."""
    pass


# ===== Step Definitions =====

@given("the engine's list of ability keywords")
def engine_ability_keywords_list(game_state):
    """Retrieve the engine's list of ability keywords."""
    game_state.ability_keywords = game_state.get_ability_keywords_list()


@when(parsers.parse('I check if "{keyword}" is in the list of ability keywords'))
def check_keyword_in_ability_keywords(game_state, keyword):
    """Check if the given keyword is in the ability keywords list."""
    game_state.keyword_check_name = keyword
    game_state.keyword_found = game_state.is_ability_keyword(keyword)


@then(parsers.parse('"{keyword}" is recognized as an ability keyword'))
def keyword_is_recognized_as_ability_keyword(game_state, keyword):
    """Rule 8.3.14: Spectra must appear in the engine's ability keyword list."""
    assert game_state.keyword_found, (
        f'"{keyword}" must be recognized as an ability keyword (Rule 8.3.14)'
    )


@given("a non-living object with the Spectra keyword")
def non_living_object_with_spectra(game_state):
    """Set up a non-living object with the Spectra keyword."""
    game_state.spectra_object = game_state.create_card(
        name="Spectra Object",
        card_type="Aura",
    )
    game_state.spectra_object_has_spectra = True
    game_state.attack.add_keyword("Spectra")


@given("a non-living object without the Spectra keyword")
def non_living_object_without_spectra(game_state):
    """Set up a non-living object without the Spectra keyword."""
    game_state.spectra_object = game_state.create_card(
        name="Non-Spectra Object",
        card_type="Aura",
    )
    game_state.spectra_object_has_spectra = False


@when("a player attempts to declare it as the target of an attack")
def player_declares_object_as_attack_target(game_state):
    """Simulate declaring the object as the target of an attack."""
    game_state.attack_target_result = game_state.check_spectra_attack_target(
        target=game_state.spectra_object,
        has_spectra=game_state.spectra_object_has_spectra,
    )


@then("the non-living Spectra object is a legal attack target")
def non_living_spectra_object_is_legal_target(game_state):
    """Rule 8.3.14a: Non-living object with Spectra must be a legal attack target."""
    assert game_state.attack_target_result.is_legal_target, (
        "A non-living object with Spectra must be a legal attack target (Rule 8.3.14a)"
    )


@then("the non-living object is not a legal attack target")
def non_living_object_is_not_legal_target(game_state):
    """Rule 8.3.14a: Non-living object without Spectra must NOT be a legal attack target."""
    assert not game_state.attack_target_result.is_legal_target, (
        "A non-living object without Spectra must not be a legal attack target (Rule 8.3.14a)"
    )


@when("the object becomes the target of an attack")
def object_becomes_attack_target(game_state):
    """Simulate the Spectra object becoming the target of an attack."""
    game_state.spectra_triggered_result = game_state.apply_spectra_trigger(
        target=game_state.spectra_object,
    )


@then("a triggered-layer is placed on the stack to destroy the Spectra object")
def triggered_layer_placed_on_stack_for_spectra(game_state):
    """Rule 8.3.14b: A triggered-layer must be placed on the stack to destroy the Spectra object."""
    assert game_state.spectra_triggered_result.triggered_layer_created, (
        "A triggered-layer must be placed on the stack when a Spectra object becomes "
        "the target of an attack (Rule 8.3.14b)"
    )


@given("the object has become the target of an attack")
def object_has_become_attack_target(game_state):
    """Set up that the Spectra object has already become the target of an attack."""
    game_state.spectra_was_attacked = True


@when("the triggered-layer resolves")
def triggered_layer_resolves(game_state):
    """Simulate the triggered-layer resolving to destroy the Spectra object."""
    game_state.spectra_destruction_result = game_state.resolve_spectra_triggered_layer(
        target=game_state.spectra_object,
    )


@then("the Spectra object is destroyed")
def spectra_object_is_destroyed(game_state):
    """Rule 8.3.14b: The Spectra object must be destroyed when the triggered-layer resolves."""
    assert game_state.spectra_destruction_result.object_destroyed, (
        "The Spectra object must be destroyed when the triggered-layer resolves (Rule 8.3.14b)"
    )


@given("there are no other legal attack targets")
def no_other_legal_attack_targets(game_state):
    """Rule 8.3.14b: Set up state where there are no other legal attack targets."""
    game_state.other_legal_targets = []


@given("there are other legal attack targets")
def other_legal_attack_targets_exist(game_state):
    """Rule 8.3.14b: Set up state where there are other legal attack targets."""
    game_state.other_legal_targets = [game_state.create_card(name="Other Target")]


@when("the Spectra object is destroyed by Spectra")
def spectra_object_destroyed_by_spectra(game_state):
    """Simulate the Spectra object being destroyed."""
    game_state.combat_chain_close_result = game_state.apply_spectra_destruction(
        target=game_state.spectra_object,
        other_legal_targets=game_state.other_legal_targets,
    )


@then("the combat chain closes")
def combat_chain_closes(game_state):
    """Rule 8.3.14b: Combat chain must close when no other legal attack targets exist."""
    assert game_state.combat_chain_close_result.combat_chain_closed, (
        "Combat chain must close when Spectra object is destroyed and there are no "
        "other legal attack targets (Rule 8.3.14b)"
    )


@then("the combat chain does not close")
def combat_chain_does_not_close(game_state):
    """Rule 8.3.14b: Combat chain must NOT close when other legal attack targets exist."""
    assert not game_state.combat_chain_close_result.combat_chain_closed, (
        "Combat chain must not close when Spectra object is destroyed and there are "
        "other legal attack targets (Rule 8.3.14b)"
    )


# ===== Fixtures =====

@pytest.fixture
def game_state():
    """
    Fixture providing game state for testing Spectra ability keyword.

    Uses BDDGameState which integrates with the real engine.
    Reference: Rule 8.3.14
    """
    from tests.bdd_helpers import BDDGameState

    state = BDDGameState()
    state.other_legal_targets = []
    state.spectra_was_attacked = False
    return state
