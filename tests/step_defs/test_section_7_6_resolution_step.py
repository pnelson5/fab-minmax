"""
Step definitions for Section 7.6: Resolution Step
Reference: Flesh and Blood Comprehensive Rules Section 7.6

This module implements behavioral tests for the Resolution Step of combat:
the game state where the active chain link resolves and the attacker may gain
an action point from go again and continue the combat chain by attacking.

Engine Features Needed for Section 7.6:
- [ ] CombatState.resolution_step_active property — tracks Resolution Step (Rule 7.6.1)
- [ ] CombatState.current_step property — "layer"|"attack"|"defend"|"reaction"|"damage"|"resolution"|"close"
- [ ] ResolutionStep.begin() — starts Resolution Step after Damage Step ends (Rule 7.6.1)
- [ ] ResolutionStep.end() — ends Resolution Step and begins Close Step (Rule 7.6.4)
- [ ] CloseStep.begin() — begins Close Step after Resolution Step ends (Rule 7.6.4)
- [ ] ChainLink.resolve() — makes active chain link a resolved chain link (Rule 7.6.2)
- [ ] ChainLink.is_resolved property — whether chain link is resolved (Rule 7.6.2)
- [ ] TriggerSystem.trigger_on_chain_link_resolved(chain_link) — triggers resolution effects (Rule 7.6.2)
- [ ] GoAgain.check(attack) -> bool — checks if attack has go again (Rule 7.6.2)
- [ ] GoAgain.grant_action_point(controller) — grants 1 action point if go again (Rule 7.6.2)
- [ ] LastKnownInformation.had_go_again(attack_lki) -> bool — LKI for go again (Rule 7.6.2a)
- [ ] PrioritySystem.grant_priority_to_turn_player() — turn-player gains priority (Rule 7.6.3)
- [ ] ResolutionStep.handle_new_attack(attack) — new attack ends Resolution Step, begins Layer Step (Rule 7.6.3)
- [ ] LayerStep.begin() — begins Layer Step when new attack added (Rule 7.6.3)
- [ ] ActionRestriction.can_play_attack_during_resolution(player) -> bool — (Rule 7.6.3a)
- [ ] ActionRestriction.can_play_non_attack_action_during_resolution(player) -> bool — (Rule 7.0.1a)
- [ ] PrioritySystem.all_players_passed() -> bool — check if all players passed (Rule 7.6.4)
- [ ] Stack.is_empty property — whether stack currently has items (Rule 7.6.4)

Current status: Tests written, Engine pending
"""

import pytest
from pytest_bdd import scenario, given, when, then, parsers


# ===== Scenarios =====

# Rule 7.6.1 — Resolution Step is a distinct game state

@scenario(
    "../features/section_7_6_resolution_step.feature",
    "Resolution Step is the game state where the active chain link resolves",
)
def test_resolution_step_is_game_state():
    """Rule 7.6.1: The Resolution Step is a distinct game state for chain link resolution."""
    pass


@scenario(
    "../features/section_7_6_resolution_step.feature",
    "Resolution Step begins after the Damage Step ends",
)
def test_resolution_step_begins_after_damage_step():
    """Rule 7.5.4 → 7.6.1: Resolution Step begins after the Damage Step ends."""
    pass


# Rule 7.6.2 — Chain link becomes resolved; go again grants action point

@scenario(
    "../features/section_7_6_resolution_step.feature",
    "Active chain link becomes a resolved chain link at the start of Resolution Step",
)
def test_chain_link_becomes_resolved():
    """Rule 7.6.2: Active chain link becomes a resolved chain link at resolution start."""
    pass


@scenario(
    "../features/section_7_6_resolution_step.feature",
    "Attack with go again grants the controller 1 action point",
)
def test_go_again_grants_action_point():
    """Rule 7.6.2: If the attack has go again, its controller gains 1 action point."""
    pass


@scenario(
    "../features/section_7_6_resolution_step.feature",
    "Attack without go again does not grant an action point",
)
def test_no_go_again_no_action_point():
    """Rule 7.6.2: Attack without go again does not grant an action point."""
    pass


# Rule 7.6.2a — Last known information for go again

@scenario(
    "../features/section_7_6_resolution_step.feature",
    "Last known information determines go again if attack leaves combat chain before Resolution Step",
)
def test_lki_go_again_attack_left_chain():
    """Rule 7.6.2a: LKI used to determine go again when attack is no longer on combat chain."""
    pass


@scenario(
    "../features/section_7_6_resolution_step.feature",
    "Last known information used when attack without go again leaves combat chain",
)
def test_lki_no_go_again_attack_left_chain():
    """Rule 7.6.2a: LKI shows no go again when attack without go again left the chain."""
    pass


# Rule 7.6.3 — Turn-player gains priority; new attack starts Layer Step

@scenario(
    "../features/section_7_6_resolution_step.feature",
    "Turn-player gains priority during the Resolution Step",
)
def test_turn_player_gains_priority():
    """Rule 7.6.3: Turn-player gains priority during the Resolution Step."""
    pass


@scenario(
    "../features/section_7_6_resolution_step.feature",
    "Adding an attack to the stack during Resolution Step ends it and begins Layer Step",
)
def test_new_attack_ends_resolution_step_starts_layer_step():
    """Rule 7.6.3: If an attack is added to the stack, Resolution Step ends and Layer Step begins."""
    pass


# Rule 7.6.3a — Turn-player may play/activate attacks during Resolution Step

@scenario(
    "../features/section_7_6_resolution_step.feature",
    "Turn-player may play attack action cards during the Resolution Step",
)
def test_attack_action_card_allowed_during_resolution():
    """Rule 7.6.3a: Turn-player may play attack action cards during the Resolution Step."""
    pass


@scenario(
    "../features/section_7_6_resolution_step.feature",
    "Turn-player may activate attack abilities during the Resolution Step",
)
def test_attack_ability_allowed_during_resolution():
    """Rule 7.6.3a: Turn-player may activate attack abilities during the Resolution Step."""
    pass


@scenario(
    "../features/section_7_6_resolution_step.feature",
    "Non-attack action cards cannot be played during the Resolution Step",
)
def test_non_attack_action_not_allowed_during_resolution():
    """Rule 7.0.1a: Non-attack action cards cannot be played during combat."""
    pass


# Rule 7.6.4 — Resolution Step ends when stack empty and all players pass

@scenario(
    "../features/section_7_6_resolution_step.feature",
    "Resolution Step ends and Close Step begins when all players pass with empty stack",
)
def test_resolution_step_ends_close_step_begins():
    """Rule 7.6.4: Resolution Step ends and Close Step begins when all pass with empty stack."""
    pass


@scenario(
    "../features/section_7_6_resolution_step.feature",
    "Resolution Step does not end while the stack has items",
)
def test_resolution_step_does_not_end_with_items_on_stack():
    """Rule 7.6.4: Resolution Step does not end while there are items on the stack."""
    pass


# Integration scenarios

@scenario(
    "../features/section_7_6_resolution_step.feature",
    "Attack with go again allows attacker to continue combat chain",
)
def test_go_again_allows_continued_combat():
    """Integration: Go again grants action point allowing the combat chain to continue."""
    pass


@scenario(
    "../features/section_7_6_resolution_step.feature",
    "Attack without go again leads to Close Step if no new attack is played",
)
def test_no_go_again_leads_to_close_step():
    """Integration: No go again and no new attack played leads to Close Step."""
    pass


# ===== Step Definitions =====

# --- Given steps ---

@given("the combat chain is open with an active chain link")
def combat_chain_open_with_active_chain_link(resolution_step_state):
    """Setup: There is an active chain link on the open combat chain."""
    resolution_step_state.combat_chain_open = True
    resolution_step_state.has_active_chain_link = True


@given("the combat chain is open with a resolved chain link")
def combat_chain_open_with_resolved_chain_link(resolution_step_state):
    """Setup: There is a resolved chain link on the open combat chain."""
    resolution_step_state.combat_chain_open = True
    resolution_step_state.has_active_chain_link = True
    resolution_step_state.chain_link_resolved = True


@given("the Damage Step has just ended")
def damage_step_just_ended(resolution_step_state):
    """Rule 7.5.4: The Damage Step has completed and Resolution Step is next."""
    resolution_step_state.damage_step_completed = True


@given("the Damage Step is active")
def damage_step_is_active(resolution_step_state):
    """Setup: The game is currently in the Damage Step."""
    resolution_step_state.current_step = "damage"


@given("the Resolution Step is active")
def resolution_step_is_active(resolution_step_state):
    """Setup: The game is currently in the Resolution Step."""
    resolution_step_state.begin_resolution_step()


@given("the active attack has go again")
def active_attack_has_go_again(resolution_step_state):
    """Rule 7.6.2: The active attack has the go again keyword."""
    resolution_step_state.attack_has_go_again = True


@given("the active attack does not have go again")
def active_attack_does_not_have_go_again(resolution_step_state):
    """Rule 7.6.2: The active attack does not have go again."""
    resolution_step_state.attack_has_go_again = False


@given("the active attack has left the combat chain before the Resolution Step")
def active_attack_left_combat_chain(resolution_step_state):
    """Rule 7.6.2a: The attack is no longer on the combat chain (LKI applies)."""
    resolution_step_state.attack_on_combat_chain = False
    resolution_step_state.attack_left_chain = True


@given("the chain link has resolved")
def chain_link_has_resolved(resolution_step_state):
    """Setup: The active chain link has become a resolved chain link."""
    resolution_step_state.chain_link_resolved = True


@given("the turn-player has priority")
def turn_player_has_priority(resolution_step_state):
    """Setup: The turn-player currently has priority."""
    resolution_step_state.turn_player_has_priority = True


@given("the turn-player has an attack action card in hand")
def turn_player_has_attack_action_card(resolution_step_state):
    """Setup: The turn-player has an attack action card in hand."""
    resolution_step_state.turn_player_has_attack_action = True


@given("the turn-player has an action point")
def turn_player_has_action_point(resolution_step_state):
    """Setup: The turn-player has at least 1 action point."""
    resolution_step_state.turn_player_action_points = 1


@given("the turn-player has a weapon with an attack ability")
def turn_player_has_weapon_with_attack_ability(resolution_step_state):
    """Setup: The turn-player has a weapon that has an attack activated ability."""
    resolution_step_state.turn_player_has_attack_weapon = True


@given("the turn-player has a non-attack action card in hand")
def turn_player_has_non_attack_action_card(resolution_step_state):
    """Setup: The turn-player has a non-attack action card (e.g. a regular action)."""
    resolution_step_state.turn_player_has_non_attack_action = True


@given("the stack is empty")
def stack_is_empty(resolution_step_state):
    """Setup: The stack has no items."""
    resolution_step_state.stack_empty = True


@given("there is an item on the stack")
def there_is_item_on_stack(resolution_step_state):
    """Setup: There is at least one item on the stack."""
    resolution_step_state.stack_empty = False
    resolution_step_state.stack_has_items = True


# --- When steps ---

@when("the Resolution Step begins")
def resolution_step_begins(resolution_step_state):
    """Rule 7.6.1: The Resolution Step has started."""
    resolution_step_state.begin_resolution_step()


@when("the stack is empty and all players pass in succession during the Damage Step")
def all_pass_during_damage_step(resolution_step_state):
    """Rule 7.5.4: All players pass during the Damage Step with empty stack."""
    resolution_step_state.stack_empty = True
    resolution_step_state.all_players_passed_damage = True
    resolution_step_state.end_damage_step()


@when("the chain link resolution begins")
def chain_link_resolution_begins(resolution_step_state):
    """Rule 7.6.2: The chain link begins resolving."""
    resolution_step_state.resolve_chain_link()


@when("priority is granted")
def priority_is_granted(resolution_step_state):
    """Rule 7.6.3: Priority is granted to the turn-player."""
    resolution_step_state.grant_priority_to_turn_player()


@when("the turn-player plays an attack action card during the Resolution Step")
def turn_player_plays_attack_action(resolution_step_state):
    """Rule 7.6.3: The turn-player plays an attack action card."""
    resolution_step_state.play_attack_during_resolution()


@when("the turn-player attempts to play an attack action card during the Resolution Step")
def turn_player_attempts_attack_action(resolution_step_state):
    """Rule 7.6.3a: The turn-player attempts to play an attack action card."""
    resolution_step_state.attempt_play_attack_action = True
    resolution_step_state.attempt_play_result = resolution_step_state.check_can_play_attack_action()


@when("the turn-player attempts to activate the attack ability during the Resolution Step")
def turn_player_attempts_attack_ability(resolution_step_state):
    """Rule 7.6.3a: The turn-player attempts to activate a weapon's attack ability."""
    resolution_step_state.attempt_activate_attack_ability = True
    resolution_step_state.attempt_play_result = resolution_step_state.check_can_activate_attack_ability()


@when("the turn-player attempts to play the non-attack action card during the Resolution Step")
def turn_player_attempts_non_attack_action(resolution_step_state):
    """Rule 7.0.1a: The turn-player attempts to play a non-attack action card."""
    resolution_step_state.attempt_play_non_attack = True
    resolution_step_state.attempt_play_result = resolution_step_state.check_can_play_non_attack_action()


@when("all players pass in succession during the Resolution Step")
def all_players_pass_during_resolution(resolution_step_state):
    """Rule 7.6.4: All players pass priority in succession during the Resolution Step."""
    resolution_step_state.all_players_passed_resolution = True
    resolution_step_state.check_resolution_step_end()


@when("all players attempt to pass in succession during the Resolution Step")
def all_players_attempt_to_pass(resolution_step_state):
    """Rule 7.6.4: All players attempt to pass (stack not empty)."""
    resolution_step_state.all_players_passed_resolution = True
    resolution_step_state.check_resolution_step_end()


@when("the chain link resolves and the controller gains 1 action point")
def chain_link_resolves_and_gains_action_point(resolution_step_state):
    """Rule 7.6.2: Chain link resolves and go again grants action point."""
    resolution_step_state.resolve_chain_link()


@when("the turn-player plays another attack action card")
def turn_player_plays_another_attack(resolution_step_state):
    """Rule 7.6.3: Turn-player plays another attack during the Resolution Step."""
    resolution_step_state.play_attack_during_resolution()


# --- Then steps ---

@then('the current combat step is "resolution"')
def current_step_is_resolution(resolution_step_state):
    """Verify: The current combat step is the Resolution Step."""
    assert resolution_step_state.current_step == "resolution", (
        f"Expected 'resolution' step but got '{resolution_step_state.current_step}'"
    )


@then("the active chain link begins resolving")
def active_chain_link_begins_resolving(resolution_step_state):
    """Verify: The active chain link is in the process of resolving."""
    assert resolution_step_state.chain_link_resolving, (
        "Expected chain link to be resolving but it is not"
    )


@then("the Damage Step ends")
def damage_step_ends(resolution_step_state):
    """Verify: The Damage Step has ended."""
    assert resolution_step_state.damage_step_completed, (
        "Expected Damage Step to have ended"
    )


@then("the Resolution Step begins")
def resolution_step_begins_assertion(resolution_step_state):
    """Verify: The Resolution Step has begun."""
    assert resolution_step_state.current_step == "resolution", (
        f"Expected Resolution Step to begin but current step is '{resolution_step_state.current_step}'"
    )


@then("the active chain link becomes a resolved chain link")
def chain_link_becomes_resolved(resolution_step_state):
    """Rule 7.6.2: The active chain link is now a resolved chain link."""
    assert resolution_step_state.chain_link_resolved, (
        "Expected chain link to become a resolved chain link"
    )


@then("effects that trigger when the chain link resolves are triggered")
def resolve_triggers_fire(resolution_step_state):
    """Rule 7.6.2: Effects triggered by chain link resolution have been triggered."""
    assert resolution_step_state.resolution_triggers_fired, (
        "Expected resolution triggers to fire when chain link resolves"
    )


@then("the controller of the attack gains 1 action point")
def controller_gains_action_point(resolution_step_state):
    """Rule 7.6.2: The attack's controller gains 1 action point from go again."""
    assert resolution_step_state.action_point_granted, (
        "Expected controller to gain 1 action point from go again"
    )
    assert resolution_step_state.action_points_granted == 1, (
        f"Expected exactly 1 action point granted but got {resolution_step_state.action_points_granted}"
    )


@then("the controller of the attack does not gain an action point from resolution")
def controller_does_not_gain_action_point(resolution_step_state):
    """Rule 7.6.2: The attack's controller does not gain an action point (no go again)."""
    assert not resolution_step_state.action_point_granted, (
        "Expected no action point to be granted (no go again)"
    )


@then("last known information indicates the attack had go again")
def lki_shows_go_again(resolution_step_state):
    """Rule 7.6.2a: LKI confirms the attack had go again."""
    assert resolution_step_state.lki_had_go_again is True, (
        "Expected LKI to show the attack had go again"
    )


@then("last known information indicates the attack did not have go again")
def lki_shows_no_go_again(resolution_step_state):
    """Rule 7.6.2a: LKI confirms the attack did not have go again."""
    assert resolution_step_state.lki_had_go_again is False, (
        "Expected LKI to show the attack did not have go again"
    )


@then("the turn-player has priority during the Resolution Step")
def turn_player_has_priority_during_resolution(resolution_step_state):
    """Rule 7.6.3: The turn-player has priority during the Resolution Step."""
    assert resolution_step_state.turn_player_has_priority, (
        "Expected turn-player to have priority during the Resolution Step"
    )


@then("the attack is added to the stack")
def attack_added_to_stack(resolution_step_state):
    """Rule 7.6.3: The new attack was added to the stack."""
    assert resolution_step_state.new_attack_on_stack, (
        "Expected the new attack to be on the stack"
    )


@then("the Resolution Step ends")
def resolution_step_ends(resolution_step_state):
    """Verify: The Resolution Step has ended."""
    assert resolution_step_state.resolution_step_ended, (
        "Expected Resolution Step to have ended"
    )


@then("the Layer Step begins")
def layer_step_begins(resolution_step_state):
    """Rule 7.6.3: The Layer Step has begun after the new attack was added."""
    assert resolution_step_state.current_step == "layer", (
        f"Expected Layer Step to begin but current step is '{resolution_step_state.current_step}'"
    )


@then("the play is allowed")
def play_is_allowed(resolution_step_state):
    """Verify: The play or activation was allowed."""
    assert resolution_step_state.attempt_play_result is True, (
        "Expected the play to be allowed during the Resolution Step"
    )


@then("the activation is allowed")
def activation_is_allowed(resolution_step_state):
    """Verify: The ability activation was allowed."""
    assert resolution_step_state.attempt_play_result is True, (
        "Expected the activation to be allowed during the Resolution Step"
    )


@then("the play is not allowed during the Resolution Step")
def play_not_allowed(resolution_step_state):
    """Rule 7.0.1a: Non-attack action cards cannot be played during combat."""
    assert resolution_step_state.attempt_play_result is False, (
        "Expected the non-attack action play to be blocked during the Resolution Step"
    )


@then("the Close Step begins")
def close_step_begins(resolution_step_state):
    """Rule 7.6.4: The Close Step has begun after the Resolution Step ended."""
    assert resolution_step_state.current_step == "close", (
        f"Expected Close Step to begin but current step is '{resolution_step_state.current_step}'"
    )


@then("the Resolution Step has not ended")
def resolution_step_has_not_ended(resolution_step_state):
    """Rule 7.6.4: The Resolution Step continues while the stack has items."""
    assert not resolution_step_state.resolution_step_ended, (
        "Expected Resolution Step to NOT have ended (stack has items)"
    )


@then("the combat chain continues with a new chain link")
def combat_chain_continues(resolution_step_state):
    """Integration: The combat chain has a new chain link continuing combat."""
    assert resolution_step_state.new_chain_link_created, (
        "Expected a new chain link to be created, continuing the combat chain"
    )


# ===== Fixture =====

@pytest.fixture
def resolution_step_state():
    """
    Fixture providing game state for Resolution Step testing.

    Tracks the state of the Resolution Step, including chain link resolution,
    go again action point grants, priority, and step transitions.
    Reference: Rule 7.6
    """
    return ResolutionStepState()


class ResolutionStepState:
    """
    Stub state for Resolution Step tests.

    Tracks state transitions and engine interactions needed for
    the Resolution Step (Rule 7.6) without requiring full engine implementation.

    Engine Features Needed:
    - CombatState.current_step (Rule 7.6.1)
    - ChainLink.resolve() (Rule 7.6.2)
    - GoAgain.grant_action_point() (Rule 7.6.2)
    - LastKnownInformation for go again (Rule 7.6.2a)
    - PrioritySystem.grant_priority_to_turn_player() (Rule 7.6.3)
    - ResolutionStep.handle_new_attack() (Rule 7.6.3)
    - ActionRestriction for attacks during Resolution Step (Rule 7.6.3a)
    - PrioritySystem.all_players_passed() (Rule 7.6.4)
    """

    def __init__(self):
        # Step tracking
        self.current_step: str = "damage"
        self.combat_chain_open: bool = False
        self.has_active_chain_link: bool = False
        self.damage_step_completed: bool = False

        # Chain link state
        self.chain_link_resolved: bool = False
        self.chain_link_resolving: bool = False
        self.resolution_triggers_fired: bool = False

        # Go again
        self.attack_has_go_again: bool = False
        self.attack_on_combat_chain: bool = True
        self.attack_left_chain: bool = False
        self.lki_had_go_again: bool | None = None
        self.action_point_granted: bool = False
        self.action_points_granted: int = 0

        # Priority
        self.turn_player_has_priority: bool = False
        self.turn_player_action_points: int = 0

        # Playing during Resolution Step
        self.turn_player_has_attack_action: bool = False
        self.turn_player_has_attack_weapon: bool = False
        self.turn_player_has_non_attack_action: bool = False
        self.attempt_play_result: bool | None = None
        self.new_attack_on_stack: bool = False

        # Step end conditions
        self.stack_empty: bool = True
        self.stack_has_items: bool = False
        self.all_players_passed_damage: bool = False
        self.all_players_passed_resolution: bool = False
        self.resolution_step_ended: bool = False

        # Integration
        self.new_chain_link_created: bool = False

    def begin_resolution_step(self):
        """
        Simulates beginning the Resolution Step.

        Engine Feature Needed:
        - [ ] ResolutionStep.begin() (Rule 7.6.1)
        - [ ] CombatState.current_step = "resolution" (Rule 7.6.1)
        """
        self.current_step = "resolution"
        self.chain_link_resolving = True

    def end_damage_step(self):
        """
        Simulates ending the Damage Step.

        Engine Feature Needed:
        - [ ] DamageStep.end() transitions to ResolutionStep.begin() (Rule 7.5.4)
        """
        if self.all_players_passed_damage and self.stack_empty:
            self.damage_step_completed = True
            self.begin_resolution_step()

    def resolve_chain_link(self):
        """
        Simulates chain link resolution.

        Engine Feature Needed:
        - [ ] ChainLink.resolve() — makes chain link resolved (Rule 7.6.2)
        - [ ] TriggerSystem.trigger_on_chain_link_resolved() (Rule 7.6.2)
        - [ ] GoAgain.grant_action_point() (Rule 7.6.2)
        - [ ] LastKnownInformation.had_go_again() (Rule 7.6.2a)
        """
        self.chain_link_resolved = True
        self.resolution_triggers_fired = True

        # Determine go again via LKI if attack left the chain
        if self.attack_left_chain:
            # Use last known information
            self.lki_had_go_again = self.attack_has_go_again
            had_go_again = self.lki_had_go_again
        else:
            had_go_again = self.attack_has_go_again

        if had_go_again:
            self.action_point_granted = True
            self.action_points_granted = 1

    def grant_priority_to_turn_player(self):
        """
        Simulates granting priority to the turn-player.

        Engine Feature Needed:
        - [ ] PrioritySystem.grant_priority_to_turn_player() (Rule 7.6.3)
        """
        self.turn_player_has_priority = True

    def check_can_play_attack_action(self) -> bool:
        """
        Checks if an attack action card can be played during the Resolution Step.

        Engine Feature Needed:
        - [ ] ActionRestriction.can_play_attack_during_resolution() (Rule 7.6.3a)
        """
        # During Resolution Step, attack action cards are allowed (Rule 7.6.3a)
        if self.current_step == "resolution" and self.turn_player_has_attack_action:
            return True
        return False

    def check_can_activate_attack_ability(self) -> bool:
        """
        Checks if a weapon's attack ability can be activated during the Resolution Step.

        Engine Feature Needed:
        - [ ] ActionRestriction.can_play_attack_during_resolution() (Rule 7.6.3a)
        """
        # During Resolution Step, attack abilities are allowed (Rule 7.6.3a)
        if self.current_step == "resolution" and self.turn_player_has_attack_weapon:
            return True
        return False

    def check_can_play_non_attack_action(self) -> bool:
        """
        Checks if a non-attack action card can be played during the Resolution Step.

        Engine Feature Needed:
        - [ ] ActionRestriction.can_play_non_attack_action_during_resolution() (Rule 7.0.1a)
        """
        # During Resolution Step (combat), non-attack action cards are NOT allowed (Rule 7.0.1a)
        if self.current_step == "resolution" and self.turn_player_has_non_attack_action:
            return False
        return True

    def play_attack_during_resolution(self):
        """
        Simulates playing an attack action card during the Resolution Step.

        Engine Feature Needed:
        - [ ] ResolutionStep.handle_new_attack() — ends Resolution Step, begins Layer Step (Rule 7.6.3)
        """
        self.new_attack_on_stack = True
        self.resolution_step_ended = True
        self.current_step = "layer"
        self.new_chain_link_created = True

    def check_resolution_step_end(self):
        """
        Checks if the Resolution Step should end.

        Engine Feature Needed:
        - [ ] PrioritySystem.all_players_passed() (Rule 7.6.4)
        - [ ] Stack.is_empty property (Rule 7.6.4)
        - [ ] ResolutionStep.end() → CloseStep.begin() (Rule 7.6.4)
        """
        if self.all_players_passed_resolution and self.stack_empty:
            self.resolution_step_ended = True
            self.current_step = "close"
