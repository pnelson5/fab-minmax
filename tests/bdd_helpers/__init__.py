"""
BDD test helpers package.

Re-exports all classes for backward compatibility with:
    from tests.bdd_helpers import BDDGameState
"""

from tests.bdd_helpers.core import (
    TestZone,
    TestAttack,
    PlayResult,
    DefendResult,
    LegalPlay,
    RestrictionCheck,
    TestPlayer,
)

from tests.bdd_helpers.game_state import BDDGameState

from tests.bdd_helpers.stubs import (
    LastKnownInformationStub,
    ModificationResultStub,
    TargetingResultStub,
    AttackProxyStub,
    SourceValidationResultStub,
    PreventionEffectStub,
    ActivatedLayerStub,
    TriggeredLayerStub,
    ResolutionResultStub,
    ModalModeResultStub,
    ConnectedAbilityPairResultStub,
    AbilityModificationResultStub,
    DamageEffectStub,
    OptionalEffectStub,
    OptionalEffectResultStub,
    MultiTargetEffectStub,
    EffectResolutionResultStub,
    AssetSpendResultStub,
    ChiPaymentResultStub,
    LifeGainResultStub,
    LifeCostAbilityStub,
    MultiAssetAbilityStub,
    EffectCostAbilityStub,
    TwoEffectCostAbilityStub,
    PitchInstructionEffectStub,
    PitchTriggerEffectStub,
    PitchReplacementEffectStub,
    GeneralReplacementEffectStub,
    CostReductionEffectStub,
    AssetPaymentResultStub,
    MultiAssetPaymentResultStub,
    CardPlayResultStub,
    AbilityActivationResultStub,
    FullCostStub,
    PitchPaymentResultStub,
    PitchAttemptResultStub,
    ChiCostPaymentResultStub,
    ResourceCostPaymentResultStub,
    LifeCostPaymentResultStub,
    ActionCostPaymentResultStub,
    EffectCostPaymentResultStub,
    HoodActivationResultStub,
    MultiEffectCostResultStub,
    TypeBoxParseResultStub211,
    SupertypeCheckResultStub211,
    LayerWithSupertypesStub211,
)
