"""
Step definitions for Section 8.3.1: Attack (Ability Keyword)
Reference: Flesh and Blood Comprehensive Rules Section 8.3.1

This module implements behavioral tests for the Attack ability keyword, covering:
- The attack static ability that turns a layer into an attack-proxy (Rule 8.3.1)
- Attack-proxy resolution onto the combat chain (Rule 8.3.1a)
- Combat chain opening and Layer Step initiation on proxy creation (Rule 8.3.1b)
- Legal attackable target requirement (Rule 8.3.1c)
- Attack-proxy property inheritance from source (Rule 1.4.3a)
- Attack-proxy lifetime tied to its source on the same chain link (Rule 1.4.3c)
- Effect isolation between attack-proxy and its attack-source (Rules 1.4.3d, 1.4.3e)

Engine Features Needed for Section 8.3.1:
- [ ] AbilityKeyword.ATTACK static ability on weapon/card layers (Rule 8.3.1)
- [ ] Layer.is_attack_proxy() — True when layer has the Attack static ability (Rule 8.3.1)
- [ ] AttackProxy.is_card -> False — attack-proxy is a non-card object (Rule 1.4.3)
- [ ] AttackProxy.source — reference to the attack-source (Rule 1.4.3)
- [ ] CombatChain.open() — opens chain when attack-proxy is added to stack (Rule 8.3.1b)
- [ ] CombatChain.is_open() — query whether the combat chain is open (Rule 8.3.1b)
- [ ] CombatChain.layer_step_begun() — True after proxy is added to stack (Rule 8.3.1b)
- [ ] CombatChain.active_attack — the attack-proxy that is the current active-attack (Rule 8.3.1a)
- [ ] CombatChain.chain_link_source(link) — the attack-source for a given chain link (Rule 8.3.1a)
- [ ] AttackProxy.resolve() — moves proxy + source onto combat chain as chain link (Rule 8.3.1a)
- [ ] AttackProxy.inherits_properties_from_source() — name, type, power, etc. (Rule 1.4.3a)
- [ ] AttackProxy.has_activated_abilities -> False inherited from source (Rule 1.4.3a)
- [ ] AttackProxy.has_resolution_abilities -> False inherited from source (Rule 1.4.3a)
- [ ] AttackProxy.ceases_to_exist_when_source_leaves() — on stack and on chain (Rule 1.4.3c)
- [ ] AttackProxy.target — declared legal attackable target (Rule 8.3.1c)
- [ ] LegalAttackableTarget.is_valid(obj) — True for living objects or effect-made (Rule 1.4.5a)
- [ ] GameState.add_attack_proxy_to_stack(source, target) — requires target declaration (Rule 8.3.1c)

Current status: Tests written, Engine pending
"""

import pytest
from pytest_bdd import scenario, given, when, then, parsers
from typing import Optional, Any


# ===== 8.3.1: Attack is a static ability; layer with attack = attack-proxy =====

@scenario(
    "../features/section_8_3_1_attack_keyword.feature",
    "Attack keyword is a static ability on a layer",
)
def test_attack_keyword_is_static_ability():
    """Rule 8.3.1: The attack ability is a static ability."""
    pass


@scenario(
    "../features/section_8_3_1_attack_keyword.feature",
    "A layer with the attack ability is an attack-proxy",
)
def test_layer_with_attack_ability_is_attack_proxy():
    """Rule 8.3.1: A layer with the attack ability is an attack-proxy."""
    pass


@scenario(
    "../features/section_8_3_1_attack_keyword.feature",
    "An attack-proxy is a non-card object",
)
def test_attack_proxy_is_non_card_object():
    """Rule 1.4.3: An attack-proxy is a non-card object representing its attack-source."""
    pass


# ===== 8.3.1a: Proxy and source move to combat chain on resolution =====

@scenario(
    "../features/section_8_3_1_attack_keyword.feature",
    "Attack-proxy and source move to combat chain when proxy resolves",
)
def test_attack_proxy_and_source_move_to_chain_on_resolution():
    """Rule 8.3.1a: Proxy and its source move onto the combat chain as a chain link."""
    pass


@scenario(
    "../features/section_8_3_1_attack_keyword.feature",
    "Attack-proxy becomes the active-attack on resolution",
)
def test_attack_proxy_becomes_active_attack():
    """Rule 8.3.1a: The attack-proxy is the active-attack; the source becomes attacking."""
    pass


# ===== 8.3.1b: Combat chain opens and Layer Step begins =====

@scenario(
    "../features/section_8_3_1_attack_keyword.feature",
    "Combat chain opens when attack-proxy is added to a closed stack",
)
def test_combat_chain_opens_when_proxy_added():
    """Rule 8.3.1b: Adding an attack-proxy to a closed combat chain opens it."""
    pass


@scenario(
    "../features/section_8_3_1_attack_keyword.feature",
    "Layer Step of combat begins when attack-proxy is added to stack",
)
def test_layer_step_begins_when_proxy_added():
    """Rule 8.3.1b: The Layer Step begins when an attack-proxy is added to the stack."""
    pass


@scenario(
    "../features/section_8_3_1_attack_keyword.feature",
    "Adding second attack-proxy does not close and reopen combat chain",
)
def test_second_proxy_does_not_close_chain():
    """Rule 8.3.1b: The chain opens if closed — an already-open chain stays open."""
    pass


# ===== 8.3.1c: Legal attackable target required =====

@scenario(
    "../features/section_8_3_1_attack_keyword.feature",
    "A legal attackable target must be declared to add attack-proxy to stack",
)
def test_legal_target_required_for_proxy():
    """Rule 8.3.1c: A legal attackable target must be declared."""
    pass


@scenario(
    "../features/section_8_3_1_attack_keyword.feature",
    "Cannot add attack-proxy to stack without declaring a target",
)
def test_cannot_add_proxy_without_target():
    """Rule 8.3.1c: No target declaration means the proxy cannot be added."""
    pass


@scenario(
    "../features/section_8_3_1_attack_keyword.feature",
    "Cannot add attack-proxy to stack when no legal attackable target exists",
)
def test_cannot_add_proxy_no_legal_target():
    """Rule 8.3.1c + 1.4.5a: Proxy cannot be added when no legal attackable target exists."""
    pass


# ===== 1.4.3a: Attack-proxy inherits properties from source =====

@scenario(
    "../features/section_8_3_1_attack_keyword.feature",
    "Attack-proxy inherits name and type properties from its source",
)
def test_attack_proxy_inherits_name_and_type():
    """Rule 1.4.3a: Attack-proxy inherits name, type, and other properties from source."""
    pass


@scenario(
    "../features/section_8_3_1_attack_keyword.feature",
    "Attack-proxy does not inherit activated abilities from its source",
)
def test_attack_proxy_does_not_inherit_activated_abilities():
    """Rule 1.4.3a: Attack-proxy does NOT inherit the source's activated abilities."""
    pass


@scenario(
    "../features/section_8_3_1_attack_keyword.feature",
    "Attack-proxy does not inherit resolution abilities from its source",
)
def test_attack_proxy_does_not_inherit_resolution_abilities():
    """Rule 1.4.3a: Attack-proxy does NOT inherit the source's resolution abilities."""
    pass


# ===== 1.4.3c: Attack-proxy ceases when source ceases =====

@scenario(
    "../features/section_8_3_1_attack_keyword.feature",
    "Attack-proxy ceases to exist when its source ceases to exist on the stack",
)
def test_attack_proxy_ceases_when_source_ceases():
    """Rule 1.4.3c: Attack-proxy ceases to exist if its source ceases to exist."""
    pass


# ===== 1.4.3d/e: Effect isolation =====

@scenario(
    "../features/section_8_3_1_attack_keyword.feature",
    "Effects on attack-source do not directly apply to its attack-proxy",
)
def test_source_effects_do_not_directly_apply_to_proxy():
    """Rule 1.4.3d: Effects on the source don't directly apply to the proxy."""
    pass


@scenario(
    "../features/section_8_3_1_attack_keyword.feature",
    "Effects on attack-proxy do not apply to its attack-source",
)
def test_proxy_effects_do_not_apply_to_source():
    """Rule 1.4.3e: Effects on the proxy don't apply to the attack-source."""
    pass


# ===== Step Definitions =====

# -- Given steps --

@given("a weapon card with the \"Attack\" ability")
def weapon_with_attack_ability(game_state):
    """Rule 8.3.1: Set up a weapon with the Attack static ability."""
    from fab_engine.cards.model import CardType
    game_state.weapon = game_state.create_card(
        name="Test Weapon",
        card_type=CardType.WEAPON,
    )
    game_state.weapon_has_attack_ability = True


@given(parsers.parse('a weapon named "{name}" with {power:d} power and the "Attack" ability'))
def weapon_named_with_power(game_state, name, power):
    """Rule 1.4.3a: A named weapon with specific power and the Attack ability."""
    from fab_engine.cards.model import CardType
    game_state.weapon = game_state.create_card(
        name=name,
        card_type=CardType.WEAPON,
    )
    game_state.weapon_expected_power = power
    game_state.weapon_has_attack_ability = True


@given("a weapon with an activated ability and an attack ability")
def weapon_with_activated_and_attack_ability(game_state):
    """Rule 1.4.3a: A weapon with both an activated ability and the Attack ability."""
    from fab_engine.cards.model import CardType
    game_state.weapon = game_state.create_card(
        name="Multi-Ability Weapon",
        card_type=CardType.WEAPON,
    )
    game_state.weapon_has_activated_ability = True
    game_state.weapon_has_attack_ability = True


@given('a weapon with a resolution ability "When this hits" and an attack ability')
def weapon_with_resolution_and_attack_ability(game_state):
    """Rule 1.4.3a: A weapon with a resolution ability and the Attack ability."""
    from fab_engine.cards.model import CardType
    game_state.weapon = game_state.create_card(
        name="Weapon With On-Hit",
        card_type=CardType.WEAPON,
    )
    game_state.weapon_has_resolution_ability = True
    game_state.weapon_has_attack_ability = True


@given("an attack-proxy for the weapon is on the stack")
def attack_proxy_on_stack(game_state):
    """Rule 8.3.1: Create an attack-proxy representing the weapon on the stack."""
    game_state.attack_proxy = game_state.create_attack_proxy(
        source=game_state.weapon
    )
    game_state.stack = [game_state.attack_proxy]


@given("the combat chain is closed")
def combat_chain_is_closed(game_state):
    """Rule 8.3.1b: The combat chain starts in a closed state."""
    result = game_state.get_combat_chain_state()
    game_state.chain_was_closed = True


@given("a player controls a weapon with an attack ability")
def player_controls_weapon_with_attack(game_state):
    """Rule 8.3.1c: Set up a player with a weapon that has the Attack ability."""
    from fab_engine.cards.model import CardType
    game_state.weapon = game_state.create_card(
        name="Player Weapon",
        card_type=CardType.WEAPON,
    )
    game_state.player.weapon = game_state.weapon


@given("there is a living opponent hero that is a legal attackable target")
def living_opponent_hero_exists(game_state):
    """Rule 1.4.5a: A living opponent hero is a legal attackable target."""
    from fab_engine.cards.model import CardType
    game_state.opponent_hero = game_state.create_card(
        name="Opponent Hero",
        card_type=CardType.HERO,
    )
    game_state.opponent_hero_is_alive = True


@given("there are no legal attackable targets")
def no_legal_attackable_targets(game_state):
    """Rule 1.4.5a: No living objects or effect-made attackable objects exist."""
    game_state.no_legal_targets = True


@given("the combat chain is open with one chain link")
def combat_chain_open_with_one_link(game_state):
    """Rule 8.3.1b: Combat chain is already open with an existing chain link."""
    from fab_engine.cards.model import CardType
    source = game_state.create_card(
        name="First Attack Source",
        card_type=CardType.WEAPON,
    )
    first_proxy = game_state.create_attack_proxy(source=source)
    game_state.put_on_combat_chain(source)
    game_state.combat_chain_link_count = 1


@given("a weapon with a continuous effect that modifies the weapon's power")
def weapon_with_continuous_power_effect(game_state):
    """Rule 1.4.3d: Weapon has a continuous effect modifying its own power."""
    from fab_engine.cards.model import CardType
    game_state.weapon = game_state.create_card(
        name="Power-Modified Weapon",
        card_type=CardType.WEAPON,
    )
    game_state.weapon_base_power = 3


@given("an attack-proxy for the weapon is on the combat chain")
def attack_proxy_on_combat_chain(game_state):
    """Rule 8.3.1a: An attack-proxy for the weapon is on the combat chain."""
    game_state.attack_proxy = game_state.create_attack_proxy(
        source=game_state.weapon
    )
    game_state.put_on_combat_chain(game_state.weapon)


@given("a weapon card with an attack-proxy on the combat chain")
def weapon_with_proxy_on_chain(game_state):
    """Rule 1.4.3e: Set up weapon + attack-proxy on the combat chain."""
    from fab_engine.cards.model import CardType
    game_state.weapon = game_state.create_card(
        name="Effect Test Weapon",
        card_type=CardType.WEAPON,
    )
    game_state.weapon_base_power = 4
    game_state.attack_proxy = game_state.create_attack_proxy(
        source=game_state.weapon
    )
    game_state.put_on_combat_chain(game_state.weapon)


# -- When steps --

@when("I inspect the attack ability on the weapon")
def inspect_attack_ability(game_state):
    """Rule 8.3.1: Query the attack ability type."""
    result = game_state.check_ability_functional(
        game_state.weapon, "attack"
    )
    game_state.ability_check_result = result


@when("the weapon activates its attack ability to create a layer on the stack")
def weapon_activates_attack_ability(game_state):
    """Rule 8.3.1: Activating the Attack ability creates an attack-proxy on the stack."""
    game_state.attack_proxy = game_state.create_attack_proxy(
        source=game_state.weapon
    )
    game_state.stack = [game_state.attack_proxy]


@when("the attack-proxy resolves from the stack")
def proxy_resolves(game_state):
    """Rule 8.3.1a: The attack-proxy resolves from the top of the stack."""
    game_state.resolution_result = game_state.resolve_attack_proxy(
        game_state.attack_proxy
    )


@when("the player adds an attack-proxy to the stack")
def player_adds_proxy_to_stack(game_state):
    """Rule 8.3.1b: Player adds an attack-proxy to the stack."""
    game_state.add_result = game_state.add_attack_proxy_to_stack(
        source=game_state.weapon
    )


@when("the player declares the opponent hero as the attack target")
def player_declares_target(game_state):
    """Rule 8.3.1c: Player declares a legal attackable target."""
    game_state.declared_target = game_state.opponent_hero


@when("the player adds an attack-proxy with the declared target")
def player_adds_proxy_with_target(game_state):
    """Rule 8.3.1c: Adds attack-proxy to stack with a declared target."""
    game_state.add_result = game_state.add_attack_proxy_to_stack(
        source=game_state.weapon,
        target=game_state.declared_target,
    )


@when("the player adds an attack-proxy to the stack", target_fixture="add_proxy_result")
def player_adds_proxy_with_declared_target(game_state):
    """Rule 8.3.1c: Player adds an attack-proxy to the stack after declaring target."""
    return game_state.add_attack_proxy_to_stack(
        source=game_state.weapon,
        target=getattr(game_state, "declared_target", None),
    )


@when("the player attempts to add an attack-proxy without declaring a target")
def player_attempts_proxy_no_target(game_state):
    """Rule 8.3.1c: Attempt to add attack-proxy without declaring a target."""
    game_state.add_result = game_state.add_attack_proxy_to_stack(
        source=game_state.weapon,
        target=None,
    )


@when("the player attempts to add an attack-proxy to the stack")
def player_attempts_proxy_no_legal_target(game_state):
    """Rule 8.3.1c: Attempt to add proxy when no legal targets exist."""
    game_state.add_result = game_state.add_attack_proxy_to_stack(
        source=game_state.weapon,
        target=None,
    )


@when("the weapon (attack-source) ceases to exist")
def source_ceases_to_exist(game_state):
    """Rule 1.4.3c: The attack-source is removed from the game."""
    game_state.source_ceased = game_state.remove_card_from_game(
        game_state.weapon
    )


@when("a separate effect directly modifies the weapon's power property")
def effect_modifies_source_power(game_state):
    """Rule 1.4.3d: An effect modifies the weapon's power directly."""
    game_state.power_modification = game_state.apply_power_modification(
        target=game_state.weapon,
        delta=2,
    )


@when("an effect specifically targets the attack-proxy and modifies its power")
def effect_targets_proxy_power(game_state):
    """Rule 1.4.3e: An effect directly targets and modifies the attack-proxy's power."""
    game_state.proxy_power_modification = game_state.apply_power_modification(
        target=game_state.attack_proxy,
        delta=3,
    )


@when("the player adds a second attack-proxy to the stack")
def player_adds_second_proxy(game_state):
    """Rule 8.3.1b: Player adds a second attack-proxy (chain already open)."""
    game_state.second_add_result = game_state.add_attack_proxy_to_stack(
        source=game_state.weapon
    )


# -- Then steps --

@then("the attack ability is a static ability")
def assert_attack_is_static(game_state):
    """Rule 8.3.1: The attack ability must be a static ability type."""
    result = game_state.get_attack_ability_type(game_state.weapon)
    assert result.ability_type == "static", (
        f"Expected attack to be a static ability, got: {result.ability_type}"
    )


@then("the layer on the stack is an attack-proxy")
def assert_layer_is_attack_proxy(game_state):
    """Rule 8.3.1: A layer with the attack ability is an attack-proxy."""
    assert game_state.attack_proxy is not None, "No attack-proxy was created"
    result = game_state.check_is_attack_proxy(game_state.attack_proxy)
    assert result.is_attack_proxy, (
        "Expected the layer to be identified as an attack-proxy"
    )


@then("the attack-proxy on the stack is not a card object")
def assert_proxy_is_not_card(game_state):
    """Rule 1.4.3: An attack-proxy is a non-card object."""
    from fab_engine.cards.model import CardInstance
    assert not isinstance(game_state.attack_proxy, CardInstance), (
        "Attack-proxy should not be a CardInstance"
    )


@then("the attack-proxy represents the weapon as its attack-source")
def assert_proxy_has_correct_source(game_state):
    """Rule 1.4.3: The attack-proxy's source is the weapon that created it."""
    assert game_state.attack_proxy.source is game_state.weapon, (
        f"Expected source to be {game_state.weapon}, "
        f"got {game_state.attack_proxy.source}"
    )


@then("the attack-proxy is on the combat chain as the active-attack")
def assert_proxy_on_combat_chain(game_state):
    """Rule 8.3.1a: The attack-proxy is on the combat chain after resolution."""
    result = game_state.get_combat_chain_state()
    assert result.active_attack is game_state.attack_proxy, (
        "Expected the attack-proxy to be the active-attack on the combat chain"
    )


@then("the weapon is on the same chain link as the attack-proxy")
def assert_source_on_same_chain_link(game_state):
    """Rule 8.3.1a: The attack-source is on the same chain link as the proxy."""
    result = game_state.get_combat_chain_state()
    assert result.current_chain_link_source is game_state.weapon, (
        "Expected the weapon to be on the same chain link as the attack-proxy"
    )


@then("the attack-proxy is the active-attack for that chain link")
def assert_proxy_is_active_attack(game_state):
    """Rule 8.3.1a: The attack-proxy is the active-attack."""
    result = game_state.get_combat_chain_state()
    assert result.active_attack is game_state.attack_proxy, (
        "Expected attack-proxy to be the active-attack"
    )


@then("the weapon is in the attacking state")
def assert_weapon_is_attacking(game_state):
    """Rule 8.3.1a (ref 7.2.3b): The weapon is in the attacking state."""
    result = game_state.get_attack_source_state(game_state.weapon)
    assert result.is_attacking, (
        "Expected the weapon to be in the attacking state"
    )


@then("the combat chain is open")
def assert_combat_chain_open(game_state):
    """Rule 8.3.1b: The combat chain is open."""
    result = game_state.get_combat_chain_state()
    assert result.is_open, "Expected the combat chain to be open"


@then("the Layer Step of combat has begun")
def assert_layer_step_begun(game_state):
    """Rule 8.3.1b: The Layer Step of combat has begun."""
    result = game_state.get_combat_phase_state()
    assert result.layer_step_active, (
        "Expected the Layer Step of combat to be active"
    )


@then("the combat chain remains open")
def assert_combat_chain_remains_open(game_state):
    """Rule 8.3.1b: The combat chain remains open (was already open)."""
    result = game_state.get_combat_chain_state()
    assert result.is_open, "Expected the combat chain to remain open"


@then("the attack-proxy is on the stack with the declared target")
def assert_proxy_on_stack_with_target(game_state):
    """Rule 8.3.1c: The attack-proxy is on the stack with the target."""
    result = game_state.add_result
    assert result.success, "Expected attack-proxy to be successfully added to stack"
    assert result.declared_target is game_state.declared_target, (
        "Expected the attack-proxy's target to be the declared target"
    )


@then("the attack-proxy cannot be added to the stack")
def assert_proxy_cannot_be_added(game_state):
    """Rule 8.3.1c: The attack-proxy cannot be added without a valid target."""
    result = game_state.add_result
    assert not result.success, (
        "Expected the attack-proxy to be rejected (no legal target)"
    )


@then(parsers.parse('the attack-proxy inherits the name "{name}" from its source'))
def assert_proxy_inherits_name(game_state, name):
    """Rule 1.4.3a: Attack-proxy inherits name from source."""
    result = game_state.get_proxy_inherited_property(
        game_state.attack_proxy, "name"
    )
    assert result.value == name, (
        f"Expected proxy to inherit name '{name}', got '{result.value}'"
    )


@then(parsers.parse("the attack-proxy inherits the power value {power:d} from its source"))
def assert_proxy_inherits_power(game_state, power):
    """Rule 1.4.3a: Attack-proxy inherits power from source."""
    result = game_state.get_proxy_inherited_property(
        game_state.attack_proxy, "power"
    )
    assert result.value == power, (
        f"Expected proxy to inherit power {power}, got {result.value}"
    )


@then("the attack-proxy does not have the source's activated abilities")
def assert_proxy_lacks_activated_abilities(game_state):
    """Rule 1.4.3a: Attack-proxy does NOT inherit activated abilities from source."""
    result = game_state.check_proxy_has_ability_type(
        game_state.attack_proxy, "activated"
    )
    assert not result.has_inherited_abilities, (
        "Attack-proxy should NOT have the source's activated abilities"
    )


@then("the attack-proxy does not inherit the resolution abilities from its source")
def assert_proxy_lacks_resolution_abilities(game_state):
    """Rule 1.4.3a: Attack-proxy does NOT inherit resolution abilities from source."""
    result = game_state.check_proxy_has_ability_type(
        game_state.attack_proxy, "resolution"
    )
    assert not result.has_inherited_abilities, (
        "Attack-proxy should NOT inherit the source's resolution abilities"
    )


@then("the attack-proxy also ceases to exist")
def assert_proxy_ceased(game_state):
    """Rule 1.4.3c: The attack-proxy ceases to exist when its source does."""
    result = game_state.check_object_exists(game_state.attack_proxy)
    assert not result.exists, (
        "Expected the attack-proxy to have ceased to exist when its source did"
    )


@then("the power modification does not directly apply to the attack-proxy")
def assert_source_effect_not_on_proxy(game_state):
    """Rule 1.4.3d: Effects on source don't directly apply to proxy."""
    result = game_state.get_proxy_power_after_source_modification(
        game_state.attack_proxy,
        game_state.power_modification,
    )
    assert not result.directly_applied_to_proxy, (
        "Source power modification should NOT directly apply to the attack-proxy"
    )


@then("that power modification does not apply to the weapon (attack-source)")
def assert_proxy_effect_not_on_source(game_state):
    """Rule 1.4.3e: Effects on proxy don't apply to the attack-source."""
    result = game_state.get_source_power_after_proxy_modification(
        game_state.weapon,
        game_state.proxy_power_modification,
    )
    assert not result.applied_to_source, (
        "Proxy power modification should NOT apply to the attack-source (weapon)"
    )


# ===== Fixtures =====

@pytest.fixture
def game_state():
    """
    Fixture providing game state for testing Section 8.3.1: Attack keyword.

    Uses BDDGameState which integrates with the real engine.
    Reference: Rules 8.3.1, 1.4.3
    """
    from tests.bdd_helpers import BDDGameState

    state = BDDGameState()

    # Provide stub methods for engine features not yet implemented
    state.weapon = None
    state.attack_proxy = None
    state.stack = []
    state.declared_target = None
    state.chain_was_closed = False

    return state
