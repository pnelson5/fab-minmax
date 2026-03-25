"""Stub classes for engine features not yet implemented."""

from typing import List, Optional, Any
from fab_engine.cards.model import CardInstance


# ===== Stub classes for Section 1.2 engine features not yet implemented =====


class LastKnownInformationStub:
    """
    Stub for last known information of a game object (Rule 1.2.3).

    Engine Feature Needed:
    - [ ] LastKnownInformation class with full snapshot semantics
    - [ ] Immutability enforcement (Rule 1.2.3c)
    - [ ] Not a legal target (Rule 1.2.3d)
    """

    def __init__(self, card: CardInstance):
        # Snapshot the card's state at the time of creation
        self._card = card
        self.name = card.name
        self.power = card.template.power + card.temp_power_mod
        self.temp_power_mod = card.temp_power_mod
        self.had_go_again = getattr(card, "_has_go_again", False)
        self.is_last_known_information = True

    @property
    def is_legal_target(self) -> bool:
        """Rule 1.2.3d: LKI is not a legal target."""
        return False


class ModificationResultStub:
    """
    Stub result for attempting to modify LKI (Rule 1.2.3c).

    Engine Feature Needed:
    - [ ] Modification attempt result with failed/was_noop flags
    """

    def __init__(self, failed: bool = False, was_noop: bool = False):
        self.failed = failed
        self.was_noop = was_noop


class TargetingResultStub:
    """
    Stub result for targeting an object (Rule 1.2.3d).

    Engine Feature Needed:
    - [ ] TargetingResult with success/reason attributes
    """

    def __init__(self, success: bool, reason: str = ""):
        self.success = success
        self.reason = reason


class AttackProxyStub:
    """
    Stub for an attack-proxy object (Rules 1.2.1a, 1.2.4).

    Engine Feature Needed:
    - [ ] AttackProxy class with source, owner, and object identity support
    """

    def __init__(self, source: Optional[CardInstance] = None):
        self.source = source
        self.owner_id = source.owner_id if source else None
        self.is_game_object = True


class SourceValidationResultStub:
    """
    Stub result for source validation (Rule 1.2.4).

    Engine Feature Needed:
    - [ ] SourceValidationResult with is_valid attribute
    """

    def __init__(self, is_valid: bool):
        self.is_valid = is_valid


class PreventionEffectStub:
    """
    Stub for a prevention effect (Rule 1.2.4).

    Engine Feature Needed:
    - [ ] PreventionEffect with source card/macro reference
    """

    def __init__(self, source: CardInstance):
        self.source = source


# ===== Stub classes for Section 1.7 engine features not yet implemented =====


class ActivatedLayerStub:
    """
    Stub for an activated-layer created by an activated ability (Rule 1.6.2b, 1.7.1a).

    Engine Feature Needed:
    - [ ] ActivatedLayer class (Rule 1.6.2b)
    - [ ] ActivatedLayer.source reference (Rule 1.7.1a)
    - [ ] ActivatedLayer.controller_id = activating player (Rule 1.7.1b)
    - [ ] ActivatedLayer.exists_independently_of_source = True (Rule 1.7.1a)
    - [ ] ActivatedLayer.is_resolved property (Rule 1.6.1)
    - [ ] ActivatedLayer.can_resolve property (Rule 1.7.1a)
    - [ ] ActivatedLayer.layer_category = "activated-layer" (Rule 1.6.2b)
    """

    def __init__(
        self,
        source: Optional[CardInstance],
        controller_id: int = 0,
        ability_text: str = "",
    ):
        self.source = source
        self.controller_id = controller_id
        self.ability_text = ability_text
        self.is_resolved = False
        self.can_resolve = True
        self.exists_independently_of_source = True
        self.layer_category = "activated-layer"
        self.is_layer = True


class TriggeredLayerStub:
    """
    Stub for a triggered-layer created by a triggered effect (Rule 1.6.2c, 1.7.1a).

    Engine Feature Needed:
    - [ ] TriggeredLayer class (Rule 1.6.2c)
    - [ ] TriggeredLayer.source reference (Rule 1.7.1a)
    - [ ] TriggeredLayer.controller_id = controller at trigger time or owner (Rule 1.7.1b)
    - [ ] TriggeredLayer.exists_independently_of_source = True (Rule 1.7.1a)
    - [ ] TriggeredLayer.can_resolve property (Rule 1.7.1a)
    - [ ] TriggeredLayer.layer_category = "triggered-layer" (Rule 1.6.2c)
    """

    def __init__(
        self,
        source: Optional[CardInstance],
        controller_id: int = 0,
        ability_text: str = "",
    ):
        self.source = source
        self.controller_id = controller_id
        self.ability_text = ability_text
        self.is_resolved = False
        self.can_resolve = True
        self.exists_independently_of_source = True
        self.layer_category = "triggered-layer"
        self.is_layer = True


class ResolutionResultStub:
    """
    Stub for the result of resolving a layer from the stack (Rule 5.3).

    Engine Feature Needed:
    - [ ] ResolutionResult class with effects_generated list
    - [ ] Stack.resolve_top() returning ResolutionResult
    """

    def __init__(self, effects_generated: Optional[List[str]] = None):
        self.effects_generated = effects_generated or []
        self.success = True


class ModalModeResultStub:
    """
    Stub result for modal mode declaration (Rules 1.7.5a, 1.7.5b).

    Engine Feature Needed:
    - [ ] ModalAbility.declare_modes() return value
    - [ ] ModalAbilityResult with success, reason, requires_distinct_modes
    """

    def __init__(
        self,
        success: bool,
        reason: str = "",
        requires_distinct_modes: bool = False,
    ):
        self.success = success
        self.reason = reason
        self.requires_distinct_modes = requires_distinct_modes


class ConnectedAbilityPairResultStub:
    """
    Stub result for adding a connected ability pair to a card (Rule 1.7.6c).

    Engine Feature Needed:
    - [ ] ConnectedAbilityPair class tracking leading/following connection
    - [ ] Effect.add_connected_ability_pair() return value
    """

    def __init__(
        self,
        leading_ability: str,
        following_ability: str,
        is_connected: bool = True,
        follows_only_added_leading: bool = True,
    ):
        self.leading_ability = leading_ability
        self.following_ability = following_ability
        self.is_connected = is_connected
        self.follows_only_added_leading = follows_only_added_leading


class AbilityModificationResultStub:
    """
    Stub result for modifying a card's ability (Rule 1.7.7).

    Engine Feature Needed:
    - [ ] Effect.modify_ability() return value
    - [ ] CardInstance.abilities mutable list
    """

    def __init__(self, success: bool, original_ability_replaced: bool = False):
        self.success = success
        self.original_ability_replaced = original_ability_replaced


# ===== Stub classes for Section 1.8 engine features not yet implemented =====


class DamageEffectStub:
    """
    Stub for a damage effect (Rule 1.8.1).

    Engine Feature Needed:
    - [ ] Effect class with source, controller_id, effect_type (Rule 1.8.1)
    - [ ] Effect.source tracking per generating ability source (Rule 1.8.1a)
    - [ ] Effect.controller_id tracking per generating ability controller (Rule 1.8.1b)
    """

    def __init__(
        self,
        source: Optional["CardInstance"] = None,
        damage_amount: int = 0,
        damage_type: str = "normal",
        controller_id: int = 0,
        target: Optional["CardInstance"] = None,
        requires_arena_target: bool = False,
    ):
        self.source = source
        self.damage_amount = damage_amount
        self.damage_type = damage_type
        self.controller_id = controller_id
        self.target = target
        self.requires_arena_target = requires_arena_target
        self.effect_type = "deal_damage"
        self.failed = False


class OptionalEffectStub:
    """
    Stub for an optional effect (Rule 1.8.3).

    Engine Feature Needed:
    - [ ] OptionalEffect class with requires_player_choice (Rule 1.8.3)
    - [ ] OptionalEffect.can_be_generated() checking game state (Rule 1.8.3b)
    - [ ] OptionalEffect.is_may_choose_to phrasing distinction (Rule 1.8.3b)
    """

    def __init__(
        self,
        source: Optional["CardInstance"] = None,
        effect_text: str = "",
        can_be_generated: bool = True,
        is_may_choose_to: bool = False,
    ):
        self.source = source
        self.effect_text = effect_text
        self._can_be_generated = can_be_generated
        self.is_may_choose_to = is_may_choose_to
        self.requires_player_choice = True  # All optional effects require choice

    def can_be_generated(self) -> bool:
        """Check if this optional effect can currently be generated."""
        return self._can_be_generated


class OptionalEffectResultStub:
    """
    Stub result for resolving an optional effect (Rule 1.8.3a).

    Engine Feature Needed:
    - [ ] OptionalEffectResult with was_generated attribute
    - [ ] OptionalEffect.generate(player_chose=True/False)
    """

    def __init__(self, was_generated: bool = False):
        self.was_generated = was_generated


class MultiTargetEffectStub:
    """
    Stub for a multi-target effect (Rule 1.8.9).

    Engine Feature Needed:
    - [ ] MultiTargetEffect class with partial_success tracking (Rule 1.8.9)
    - [ ] Effect.fail() when all targets cease to exist
    - [ ] Effect.partial_success when some events succeed
    """

    def __init__(
        self,
        targets: Optional[List["CardInstance"]] = None,
        damage_amount: int = 0,
    ):
        self.targets = targets or []
        self.damage_amount = damage_amount
        self.effect_type = "deal_damage"
        self.failed = False


class EffectResolutionResultStub:
    """
    Stub result for resolving an effect with target existence check (Rule 1.8.9).

    Engine Feature Needed:
    - [ ] EffectResolutionResult with failed, partial_success attributes (Rule 1.8.9)
    - [ ] Effect.fail() returning EffectResolutionResult with failed=True
    """

    def __init__(self, failed: bool = False, partial_success: bool = False):
        self.failed = failed
        self.partial_success = partial_success
        self.succeeded = not failed


# ===== Stub classes for Section 1.13 engine features not yet implemented =====


class AssetSpendResultStub:
    """
    Stub result for spending or paying with assets (Rule 1.13).

    Engine Feature Needed:
    - [ ] AssetPaymentResult with success and reason attributes (Rule 1.13)
    - [ ] Player.spend_asset(asset_type, amount) -> AssetPaymentResult
    """

    def __init__(self, success: bool, reason: str = ""):
        self.success = success
        self.reason = reason


class ChiPaymentResultStub:
    """
    Stub result for paying a resource cost using chi points (Rule 1.13.5b).

    Engine Feature Needed:
    - [ ] ChiPaymentResult.chi_used attribute (Rule 1.13.5b)
    - [ ] ChiPaymentResult.resource_used attribute (Rule 1.13.5b)
    - [ ] ChiPaymentResult.success attribute
    - [ ] AssetPayment.pay_resource_with_chi(player_id, cost) (Rule 1.13.5b)
    """

    def __init__(
        self,
        success: bool,
        chi_used: int = 0,
        resource_used: int = 0,
        reason: str = "",
    ):
        self.success = success
        self.chi_used = chi_used
        self.resource_used = resource_used
        self.reason = reason


class LifeGainResultStub:
    """
    Stub result for gaining life points from an effect (Rule 1.13.4a).

    Engine Feature Needed:
    - [ ] LifeGainResult.amount_gained attribute (Rule 1.13.4a)
    - [ ] GainLifeEffect.apply(player_id, amount) -> LifeGainResult
    """

    def __init__(self, amount_gained: int = 0):
        self.amount_gained = amount_gained
        self.success = True


class LifeCostAbilityStub:
    """
    Stub for an ability with a life point cost (Rule 1.13.4).

    Engine Feature Needed:
    - [ ] ActivatedAbility with life_cost property (Rule 1.13.4)
    - [ ] AssetPayment.pay_life_cost(player_id, amount) (Rule 1.14.2e)
    """

    def __init__(self, life_cost: int = 0, ability_text: str = ""):
        self.life_cost = life_cost
        self.ability_text = ability_text
        self.cost_type = "life_point"


# ===== Stub classes for Section 1.14 engine features not yet implemented =====


class MultiAssetAbilityStub:
    """
    Stub for an ability with multiple asset types in its cost (Rule 1.14.2a).

    Engine Feature Needed:
    - [ ] MultiAssetCost class tracking chi, resource, life, action amounts (Rule 1.14.2a)
    - [ ] MultiAssetCost.pay(player) enforcing chi -> resource -> life -> action order
    """

    def __init__(
        self,
        chi_cost: int = 0,
        resource_cost: int = 0,
        life_cost: int = 0,
        action_cost: int = 0,
    ):
        self._chi_cost = chi_cost
        self._resource_cost = resource_cost
        self._life_cost = life_cost
        self._action_cost = action_cost


class EffectCostAbilityStub:
    """
    Stub for an ability with an effect-cost (Rule 1.14.4).

    Engine Feature Needed:
    - [ ] EffectCost class representing effects as costs (Rule 1.14.4)
    - [ ] EffectCost.can_be_generated(player) pre-payment check (Rule 1.14.4b)
    """

    def __init__(self, effect_cost: str = ""):
        self._effect_cost = effect_cost


class TwoEffectCostAbilityStub:
    """
    Stub for an ability with two effect-costs (Rule 1.14.4a).

    Engine Feature Needed:
    - [ ] MultiEffectCost with ordered effects (Rule 1.14.4a)
    - [ ] Player declares generation order for two or more effect-costs (Rule 1.14.4a)
    """

    def __init__(self, cost1: str = "", cost2: str = ""):
        self._cost1 = cost1
        self._cost2 = cost2


class PitchInstructionEffectStub:
    """
    Stub for an effect that instructs a player to pitch a card (Rule 1.14.3b).

    Engine Feature Needed:
    - [ ] PitchInstructionEffect class overriding normal pitch restrictions (Rule 1.14.3b)
    """

    def __init__(self):
        self.is_pitch_instruction = True


class PitchTriggerEffectStub:
    """
    Stub for a triggered effect that fires when a card is pitched (Rule 1.14.3c).

    Engine Feature Needed:
    - [ ] TriggeredEffect watching for pitch events (Rule 1.14.3c)
    - [ ] PitchEvent triggering the effect
    """

    def __init__(self):
        self.is_pitch_trigger = True
        self._fire_count = 0


class PitchReplacementEffectStub:
    """
    Stub for a replacement effect that modifies a pitch event (Rule 1.14.3c).

    Engine Feature Needed:
    - [ ] ReplacementEffect for pitch events (Rule 1.14.3c)
    - [ ] ReplacementEffect.was_applied tracking
    """

    def __init__(self):
        self.is_pitch_replacement = True
        self.was_applied = False


class GeneralReplacementEffectStub:
    """
    Stub for a general replacement effect (Rules 1.14.4c, 1.14.3c).

    Engine Feature Needed:
    - [ ] ReplacementEffect class with replaces/with_effect tracking (Rule 1.14.4c)
    """

    def __init__(self, replaces: str = "", with_effect: str = ""):
        self.replaces = replaces
        self.with_effect = with_effect
        self.was_applied = False


class CostReductionEffectStub:
    """
    Stub for a cost reduction effect (Rule 1.14.5).

    Engine Feature Needed:
    - [ ] CostReductionEffect reducing AssetCost amounts (Rule 1.14.5)
    - [ ] ZeroCostAcknowledgment when effective cost reaches 0
    """

    def __init__(self, reduction: int = 0):
        self._reduction = reduction


class AssetPaymentResultStub:
    """
    Stub result for paying an asset-cost (Rule 1.14.2).

    Engine Feature Needed:
    - [ ] AssetPaymentResult with _cost_paid, _game_state_reversed attributes (Rule 1.14.2)
    - [ ] AssetCost.pay(player) returning AssetPaymentResult
    """

    def __init__(
        self,
        cost_paid: bool = False,
        game_state_reversed: bool = False,
        entire_action_reversed: bool = False,
    ):
        self._cost_paid = cost_paid
        self._game_state_reversed = game_state_reversed
        self._entire_action_reversed = entire_action_reversed


class MultiAssetPaymentResultStub:
    """
    Stub result for paying a multi-asset-cost (Rule 1.14.2a).

    Engine Feature Needed:
    - [ ] MultiAssetPaymentResult tracking payment order (Rule 1.14.2a)
    - [ ] _chi_paid_order, _resource_paid_order, _life_paid_order, _action_paid_order
    """

    def __init__(
        self,
        chi_paid_order: Optional[int] = None,
        resource_paid_order: Optional[int] = None,
        life_paid_order: Optional[int] = None,
        action_paid_order: Optional[int] = None,
        chi_payment_failed: bool = False,
        resource_payment_started: bool = True,
    ):
        self._chi_paid_order = chi_paid_order
        self._resource_paid_order = resource_paid_order
        self._life_paid_order = life_paid_order
        self._action_paid_order = action_paid_order
        self._chi_payment_failed = chi_payment_failed
        self._resource_payment_started = resource_payment_started


class CardPlayResultStub:
    """
    Stub result for attempting to play a card with cost tracking (Rule 1.14.1).

    Engine Feature Needed:
    - [ ] CardPlayResult with incurred_cost, cost_amount, cost_paid attributes (Rule 1.14.1)
    - [ ] ZeroCostAcknowledgment tracking (Rule 1.14.5)
    """

    def __init__(
        self,
        play_succeeded: bool = False,
        incurred_cost: bool = True,
        cost_amount: int = 0,
        cost_paid: bool = False,
        game_state_reversed: bool = False,
        entire_action_reversed: bool = False,
        has_cost: bool = True,
        zero_cost_acknowledged: bool = False,
        effective_cost: int = 0,
        has_asset_cost: bool = False,
        has_effect_cost: bool = False,
    ):
        self._play_succeeded = play_succeeded
        self._incurred_cost = incurred_cost
        self._cost_amount = cost_amount
        self._cost_paid = cost_paid
        self._game_state_reversed = game_state_reversed
        self._entire_action_reversed = entire_action_reversed
        self._has_cost = has_cost
        self._zero_cost_acknowledged = zero_cost_acknowledged
        self._effective_cost = effective_cost
        self._has_asset_cost = has_asset_cost
        self._has_effect_cost = has_effect_cost


class AbilityActivationResultStub:
    """
    Stub result for activating an ability with cost tracking (Rule 1.14.1).

    Engine Feature Needed:
    - [ ] AbilityActivationResult with _incurred_cost, _cost_amount, _cost_paid (Rule 1.14.1)
    """

    def __init__(
        self,
        incurred_cost: bool = True,
        cost_amount: int = 0,
        cost_paid: bool = False,
    ):
        self._incurred_cost = incurred_cost
        self._cost_amount = cost_amount
        self._cost_paid = cost_paid


class FullCostStub:
    """
    Stub for the full cost of a card (Rule 1.14.1).

    Engine Feature Needed:
    - [ ] FullCost class with asset/effect cost components (Rule 1.14.1)
    - [ ] Card.get_full_cost() returning FullCost
    """

    def __init__(self, has_asset_cost: bool = False, has_effect_cost: bool = False):
        self._has_asset_cost = has_asset_cost
        self._has_effect_cost = has_effect_cost


class PitchPaymentResultStub:
    """
    Stub result for pitching a card during cost payment (Rule 1.14.3).

    Engine Feature Needed:
    - [ ] PitchPaymentResult with resources_gained, chi_gained, pitch_event_occurred (Rule 1.14.3)
    """

    def __init__(
        self,
        resources_gained: int = 0,
        chi_gained: int = 0,
        pitch_event_occurred: bool = False,
        was_replaced: bool = False,
        total_resources_after_pitch: Optional[int] = None,
        pitch_succeeded: bool = True,
    ):
        self._resources_gained = resources_gained
        self._chi_gained = chi_gained
        self._pitch_event_occurred = pitch_event_occurred
        self._was_replaced = was_replaced
        self._total_resources_after_pitch = total_resources_after_pitch
        self._pitch_succeeded = pitch_succeeded


class PitchAttemptResultStub:
    """
    Stub result for attempting to pitch a card (Rule 1.14.3a/b).

    Engine Feature Needed:
    - [ ] PitchAttemptResult with _pitch_succeeded, _pitch_rejected, _rejection_reason (Rule 1.14.3a)
    """

    def __init__(
        self,
        pitch_succeeded: bool = False,
        pitch_rejected: bool = False,
        rejection_reason: str = "",
        chi_gained: int = 0,
    ):
        self._pitch_succeeded = pitch_succeeded
        self._pitch_rejected = pitch_rejected
        self._rejection_reason = rejection_reason
        self._chi_gained = chi_gained


class ChiCostPaymentResultStub:
    """
    Stub result for paying a chi cost (Rule 1.14.2c).

    Engine Feature Needed:
    - [ ] ChiCostPaymentResult with _chi_spent, _cost_paid attributes (Rule 1.14.2c)
    """

    def __init__(self, chi_spent: int = 0, cost_paid: bool = False):
        self._chi_spent = chi_spent
        self._cost_paid = cost_paid


class ResourceCostPaymentResultStub:
    """
    Stub result for paying a resource cost using chi-first order (Rule 1.14.2d).

    Engine Feature Needed:
    - [ ] ResourceCostPaymentResult tracking _chi_used_before_resource (Rule 1.14.2d)
    """

    def __init__(
        self,
        success: bool = False,
        chi_used_before_resource: bool = False,
        chi_spent: int = 0,
        resource_spent: int = 0,
    ):
        self._success = success
        self._chi_used_before_resource = chi_used_before_resource
        self._chi_spent = chi_spent
        self._resource_spent = resource_spent


class LifeCostPaymentResultStub:
    """
    Stub result for paying a life point cost (Rule 1.14.2e).

    Engine Feature Needed:
    - [ ] LifeCostPaymentResult with _life_spent, _cost_paid attributes (Rule 1.14.2e)
    """

    def __init__(self, life_spent: int = 0, cost_paid: bool = False):
        self._life_spent = life_spent
        self._cost_paid = cost_paid


class ActionCostPaymentResultStub:
    """
    Stub result for paying an action point cost (Rule 1.14.2f).

    Engine Feature Needed:
    - [ ] ActionCostPaymentResult with _action_spent, _cost_paid attributes (Rule 1.14.2f)
    """

    def __init__(self, action_spent: int = 0, cost_paid: bool = False):
        self._action_spent = action_spent
        self._cost_paid = cost_paid


class EffectCostPaymentResultStub:
    """
    Stub result for paying an effect-cost (Rule 1.14.4).

    Engine Feature Needed:
    - [ ] EffectCostPaymentResult with _effect_generated, _target_destroyed, etc. (Rule 1.14.4)
    - [ ] _game_state_reversed when effect-cost cannot be paid (Rule 1.14.4b)
    - [ ] _replacement_was_applied for Rule 1.14.4c
    """

    def __init__(
        self,
        effect_generated: bool = False,
        target_destroyed: bool = False,
        cost_paid: bool = False,
        game_state_reversed: bool = False,
        replacement_was_applied: bool = False,
    ):
        self._effect_generated = effect_generated
        self._target_destroyed = target_destroyed
        self._cost_paid = cost_paid
        self._game_state_reversed = game_state_reversed
        self._replacement_was_applied = replacement_was_applied


class HoodActivationResultStub:
    """
    Stub result for activating Hope Merchant's Hood (Rule 1.14.4 example).

    Engine Feature Needed:
    - [ ] HoodActivationResult tracking destroy-as-effect-cost (Rule 1.14.4)
    """

    def __init__(
        self,
        destroy_was_effect_cost: bool = False,
        cards_shuffled: bool = False,
        cost_paid: bool = False,
    ):
        self._destroy_was_effect_cost = destroy_was_effect_cost
        self._cards_shuffled = cards_shuffled
        self._cost_paid = cost_paid


class MultiEffectCostResultStub:
    """
    Stub result for paying a multi-effect-cost with player-declared ordering (Rule 1.14.4a).

    Engine Feature Needed:
    - [ ] MultiEffectCostResult with _player_declared_order, _generated_in_declared_order (Rule 1.14.4a)
    """

    def __init__(
        self,
        player_declared_order: bool = False,
        generated_in_declared_order: bool = False,
        cost_paid: bool = False,
    ):
        self._player_declared_order = player_declared_order
        self._generated_in_declared_order = generated_in_declared_order
        self._cost_paid = cost_paid


# ===========================================================================
# Section 2.11 Supertypes stubs
# ===========================================================================


class TypeBoxParseResultStub211:
    """
    Stub result for parsing a type box string (Rule 2.11.3).

    Engine Feature Needed:
    - [ ] TypeBoxParser.parse(type_box_str) returning parsed result (Rule 2.11.3)
    - [ ] TypeBoxParseResult.supertypes: list of supertype strings
    - [ ] TypeBoxParseResult.card_type: the primary card type string
    - [ ] TypeBoxParseResult.subtypes: list of subtype strings
    - [ ] TypeBoxParseResult.supertypes_before_type: True (Rule 2.11.3)
    """

    def __init__(
        self,
        supertypes: list = None,
        card_type: str = "",
        subtypes: list = None,
    ):
        self.supertypes = supertypes or []
        self.card_type = card_type
        self.subtypes = subtypes or []
        self.supertypes_before_type = (
            True  # Supertypes always before type per Rule 2.11.3
        )

    @classmethod
    def parse(cls, type_box_str: str) -> "TypeBoxParseResultStub211":
        """
        Parse a type box string in the format "[SUPERTYPES] [TYPE] [--- SUBTYPES]".

        Rule 2.11.3: Supertypes are printed before the card's type.
        Rule 2.14.1a: "Generic" as supertype means no supertypes.
        """
        KNOWN_CLASS_SUPERTYPES = {
            "Adjudicator",
            "Assassin",
            "Bard",
            "Brute",
            "Guardian",
            "Illusionist",
            "Mechanologist",
            "Merchant",
            "Necromancer",
            "Ninja",
            "Pirate",
            "Ranger",
            "Runeblade",
            "Shapeshifter",
            "Thief",
            "Warrior",
            "Wizard",
        }
        KNOWN_TALENT_SUPERTYPES = {
            "Chaos",
            "Draconic",
            "Earth",
            "Elemental",
            "Ice",
            "Light",
            "Lightning",
            "Mystic",
            "Revered",
            "Reviled",
            "Royal",
            "Shadow",
        }
        ALL_SUPERTYPES = KNOWN_CLASS_SUPERTYPES | KNOWN_TALENT_SUPERTYPES
        CARD_TYPES = {
            "Action",
            "Attack Reaction",
            "Defense Reaction",
            "Instant",
            "Resource",
            "Equipment",
            "Weapon",
            "Hero",
            "Token",
            "Mentor",
        }

        # Split on " - " to separate subtypes
        if " - " in type_box_str:
            main_part, subtype_part = type_box_str.split(" - ", 1)
            subtypes = [s.strip() for s in subtype_part.split(",")]
        else:
            main_part = type_box_str
            subtypes = []

        # "Generic" means no supertypes (Rule 2.14.1a)
        if main_part.startswith("Generic "):
            return cls(
                supertypes=[],
                card_type=main_part[len("Generic ") :].strip(),
                subtypes=subtypes,
            )
        if main_part == "Generic":
            return cls(supertypes=[], card_type="", subtypes=subtypes)

        # Parse the main part by splitting on spaces and identifying supertypes vs type
        tokens = main_part.strip().split()
        supertypes = []
        card_type_tokens = []
        type_found = False

        for token in tokens:
            if not type_found and token in ALL_SUPERTYPES:
                supertypes.append(token)
            else:
                type_found = True
                card_type_tokens.append(token)

        return cls(
            supertypes=supertypes,
            card_type=" ".join(card_type_tokens),
            subtypes=subtypes,
        )


class SupertypeCheckResultStub211:
    """
    Stub result for checking whether supertypes add additional rules (Rule 2.11.6).

    Engine Feature Needed:
    - [ ] SupertypeRegistry.is_non_functional(name) = True always (Rule 2.11.6)
    - [ ] SupertypeCheckResult.adds_additional_rules = False (Rule 2.11.6)
    """

    def __init__(
        self, adds_additional_rules: bool = False, is_non_functional: bool = True
    ):
        self.adds_additional_rules = adds_additional_rules
        self.is_non_functional = is_non_functional


class LayerWithSupertypesStub211:
    """
    Stub for a layer that inherits supertypes from its source (Rule 2.11.4).

    Engine Feature Needed:
    - [ ] ActivatedLayer.supertypes == source.supertypes (Rule 2.11.4)
    - [ ] TriggeredLayer.supertypes == source.supertypes (Rule 2.11.4)
    """

    def __init__(self, source=None, layer_type: str = "activated"):
        self._source = source
        self.layer_type = layer_type

    @property
    def supertypes(self):
        """Inherit supertypes from source (Rule 2.11.4)."""
        if self._source is None:
            return set()
        return getattr(self._source, "_supertypes", set())


# ===== Section 8.3.5: Go again stubs =====


class GoAgainAbilityStub:
    """
    Stub for the go again ability (Rule 8.3.5).

    Engine Feature Needed:
    - [ ] GoAgainAbility class with is_resolution = True (Rule 8.3.5)
    - [ ] GoAgainAbility.meaning == "Gain 1 action point" (Rule 8.3.5)
    - [ ] AbilityKeyword.GO_AGAIN enum value (Rule 8.3.5)
    """

    is_resolution: bool = True
    is_static: bool = False
    is_activated: bool = False
    meaning: str = "Gain 1 action point"
    keyword: str = "go again"


class NonAttackGoAgainResolutionResultStub:
    """
    Stub for the result of resolving a non-attack layer with go again (Rule 8.3.5a / 5.3.5).

    Engine Feature Needed:
    - [ ] LayerResolver.resolve_go_again() for non-attack layers (Rule 8.3.5a)
    - [ ] LayerResolver fires go again AFTER all other resolution abilities (Rule 5.3.5)
    - [ ] NonAttackLayerResolutionResult.go_again_was_last attribute
    """

    def __init__(self, go_again_was_last: bool = False, action_points_granted: int = 0):
        self.go_again_was_last = go_again_was_last
        self.action_points_granted = action_points_granted


class ResolutionStepResultStub:
    """
    Stub for the result of the Resolution Step in combat (Rule 8.3.5b / 7.6.2).

    Engine Feature Needed:
    - [ ] ResolutionStep.begin() grants AP if attack had go again (Rule 7.6.2)
    - [ ] ResolutionStep uses LKI when attack no longer on chain (Rule 7.6.2a)
    - [ ] ResolutionStepResult.action_points_granted attribute
    - [ ] ResolutionStepResult.used_last_known_information attribute
    """

    def __init__(
        self,
        action_points_granted: int = 0,
        used_last_known_information: bool = False,
    ):
        self.action_points_granted = action_points_granted
        self.used_last_known_information = used_last_known_information


class GoAgainGrantResultStub:
    """
    Stub for the result of granting go again to an object (Rule 8.3.5c).

    Engine Feature Needed:
    - [ ] GoAgainEffect.grant(card) fails if card already has go again (Rule 8.3.5c)
    - [ ] GoAgainGrantResult.success == False when card already has go again
    """

    def __init__(self, success: bool = True):
        self.success = success


class GoAgainLKIEvaluationResultStub:
    """
    Stub for evaluating go again from last known information (Rule 5.3.5a).

    Engine Feature Needed:
    - [ ] GoAgainResolver.evaluate_from_lki(lki, player) (Rule 5.3.5a)
    - [ ] GoAgainLKIResult.used_last_known_information = True
    """

    def __init__(self, used_last_known_information: bool = True, action_points_granted: int = 0):
        self.used_last_known_information = used_last_known_information
        self.action_points_granted = action_points_granted


class ArcaneBarrierAbilityStub:
    """
    Stub for the Arcane Barrier ability (Rule 8.3.8).

    Engine Feature Needed:
    - [ ] ArcaneBarrierAbility class with is_static = True (Rule 8.3.8)
    - [ ] ArcaneBarrierAbility.value == N in "Arcane Barrier N" (Rule 8.3.8)
    - [ ] ArcaneBarrierAbility.meaning == "If you would be dealt arcane damage, you may pay N{r} to prevent N of that damage" (Rule 8.3.8)
    - [ ] AbilityKeyword.ARCANE_BARRIER enum value (Rule 8.3.8)
    """

    def __init__(self, value: int = 1):
        self.is_static: bool = True
        self.is_triggered: bool = False
        self.is_meta_static: bool = False
        self.is_resolution: bool = False
        self.is_activated: bool = False
        self.value: int = value
        self.keyword: str = f"Arcane Barrier {value}"
        self.meaning: str = (
            f"If you would be dealt arcane damage, you may pay {value}{{r}} to prevent {value} of that damage"
        )


class ArcaneBarrierActivationResultStub:
    """
    Stub for the result of attempting to activate Arcane Barrier (Rule 8.3.8).

    Engine Feature Needed:
    - [ ] ArcaneBarrierAbility.can_activate(player, damage_type) checks resources and damage type (Rule 8.3.8)
    - [ ] ArcaneBarrierAbility.activate(player) spends N resources and prevents N arcane damage (Rule 8.3.8)
    - [ ] ArcaneBarrierActivationResult.activated == True if cost was paid and damage prevented (Rule 8.3.8)
    - [ ] ArcaneBarrierActivationResult.can_activate == False if wrong damage type or insufficient resources (Rule 8.3.8)
    """

    def __init__(self, activated: bool = False, can_activate: bool = False, prevented: int = 0):
        self.activated: bool = activated
        self.can_activate: bool = can_activate
        self.prevented: int = prevented


class SpellvoidAbilityStub:
    """
    Stub for the Spellvoid ability (Rule 8.3.15).

    Engine Feature Needed:
    - [ ] SpellvoidAbility class with is_static = True (Rule 8.3.15)
    - [ ] SpellvoidAbility.value == N in "Spellvoid N" (Rule 8.3.15)
    - [ ] SpellvoidAbility.meaning == "If you would be dealt arcane damage, you may destroy this to prevent N of that damage" (Rule 8.3.15)
    - [ ] AbilityKeyword.SPELLVOID enum value (Rule 8.3.15)
    """

    def __init__(self, value: int = 1):
        self.is_static: bool = True
        self.is_triggered: bool = False
        self.is_meta_static: bool = False
        self.is_resolution: bool = False
        self.is_activated: bool = False
        self.value: int = value
        self.keyword: str = f"Spellvoid {value}"
        self.meaning: str = (
            f"If you would be dealt arcane damage, you may destroy this to prevent {value} of that damage"
        )


class SpellvoidActivationResultStub:
    """
    Stub for the result of attempting to activate Spellvoid (Rule 8.3.15).

    Engine Feature Needed:
    - [ ] SpellvoidAbility.can_activate(obj, damage_type) checks if obj can be destroyed and damage is arcane (Rule 8.3.15a)
    - [ ] SpellvoidAbility.activate(obj) destroys the object and prevents N arcane damage (Rule 8.3.15)
    - [ ] SpellvoidActivationResult.activated == True if obj was destroyed and damage prevented (Rule 8.3.15)
    - [ ] SpellvoidActivationResult.can_activate == False if wrong damage type or obj cannot be destroyed (Rule 8.3.15a)
    """

    def __init__(self, activated: bool = False, can_activate: bool = False, prevented: int = 0):
        self.activated: bool = activated
        self.can_activate: bool = can_activate
        self.prevented: int = prevented


class ResetCardStub:
    """
    Stub representing a card that has become a new object after zone transition (Rule 3.0.9).

    Engine Feature Needed:
    - [ ] Zone.move_card() triggers object reset for non-arena/non-stack destination (Rule 3.0.9)
    - [ ] New object has no relation to previous existence (Rule 3.0.9)
    - [ ] Gained abilities (e.g., go again) are NOT retained on reset
    """

    def __init__(self, original_card=None):
        self.is_new_object = True
        self._has_go_again = False  # Reset card has no gained abilities
        self.name = getattr(original_card, "name", "Reset Card") if original_card else "Reset Card"
