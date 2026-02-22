"""
Precedence system for Flesh and Blood game rules.

Implements Section 1.0.2 of the Comprehensive Rules:
- Restrictions (cannot happen)
- Requirements (should happen if possible)
- Allowances (can happen)

Rule 1.0.2: A restriction takes precedence over any requirement or allowance,
and a requirement takes precedence over any allowance.
"""

from dataclasses import dataclass, field
from typing import List, Set, Optional, Callable, Any
from enum import Enum, auto


class EffectType(Enum):
    """Type of effect for precedence evaluation."""

    RESTRICTION = auto()  # Highest precedence - cannot happen
    REQUIREMENT = auto()  # Middle precedence - should happen if possible
    ALLOWANCE = auto()  # Lowest precedence - can happen


@dataclass
class PrecedenceEffect:
    """
    Represents a restriction, requirement, or allowance effect.

    Reference: Rule 1.0.2
    """

    effect_type: EffectType
    identifier: str  # Unique identifier for this effect
    condition: Optional[Callable[[Any], bool]] = None  # Optional condition check
    source: Optional[Any] = None  # Source of the effect (card, ability, etc.)

    def applies(self, context: Any = None) -> bool:
        """Check if this effect applies in the current context."""
        if self.condition is None:
            return True
        return self.condition(context)


@dataclass
class PrecedenceResult:
    """
    Result of checking precedence for an action.

    Indicates whether an action is permitted, forbidden, or required.
    """

    permitted: bool
    blocked_by: Optional[str] = None  # Identifier of blocking restriction
    blocking_restrictions: List[str] = field(default_factory=list)
    active_requirements: List[str] = field(default_factory=list)
    active_allowances: List[str] = field(default_factory=list)

    @property
    def success(self) -> bool:
        """Alias for permitted, used in tests."""
        return self.permitted


class PrecedenceManager:
    """
    Manages restrictions, requirements, and allowances for game actions.

    Reference: Rule 1.0.2
    """

    def __init__(self):
        self.effects: List[PrecedenceEffect] = []

    def add_restriction(
        self, identifier: str, condition: Optional[Callable] = None, source: Any = None
    ):
        """
        Add a restriction effect.

        Rule 1.0.2: Restrictions state something cannot happen.
        """
        effect = PrecedenceEffect(
            effect_type=EffectType.RESTRICTION,
            identifier=identifier,
            condition=condition,
            source=source,
        )
        self.effects.append(effect)

    def add_requirement(
        self, identifier: str, condition: Optional[Callable] = None, source: Any = None
    ):
        """
        Add a requirement effect.

        Rule 1.0.2: Requirements state something should happen if possible.
        """
        effect = PrecedenceEffect(
            effect_type=EffectType.REQUIREMENT,
            identifier=identifier,
            condition=condition,
            source=source,
        )
        self.effects.append(effect)

    def add_allowance(
        self, identifier: str, condition: Optional[Callable] = None, source: Any = None
    ):
        """
        Add an allowance effect.

        Rule 1.0.2: Allowances state something can happen.
        """
        effect = PrecedenceEffect(
            effect_type=EffectType.ALLOWANCE,
            identifier=identifier,
            condition=condition,
            source=source,
        )
        self.effects.append(effect)

    def remove_effect(self, identifier: str):
        """Remove an effect by identifier."""
        self.effects = [e for e in self.effects if e.identifier != identifier]

    def clear_restrictions(self):
        """Remove all restriction effects."""
        self.effects = [
            e for e in self.effects if e.effect_type != EffectType.RESTRICTION
        ]

    def clear_requirements(self):
        """Remove all requirement effects."""
        self.effects = [
            e for e in self.effects if e.effect_type != EffectType.REQUIREMENT
        ]

    def clear_allowances(self):
        """Remove all allowance effects."""
        self.effects = [
            e for e in self.effects if e.effect_type != EffectType.ALLOWANCE
        ]

    def clear_all(self):
        """Remove all effects."""
        self.effects.clear()

    def check_action(
        self, action_identifier: str, context: Any = None
    ) -> PrecedenceResult:
        """
        Check if an action is permitted based on precedence rules.

        Rule 1.0.2: Restrictions > Requirements > Allowances

        Args:
            action_identifier: Identifier for the action being checked
            context: Optional context for condition evaluation

        Returns:
            PrecedenceResult indicating if action is permitted
        """
        # Collect applicable effects for this action
        restrictions = []
        requirements = []
        allowances = []

        for effect in self.effects:
            if not effect.applies(context):
                continue

            # Check if effect applies to this action
            if self._effect_applies_to_action(effect, action_identifier, context):
                if effect.effect_type == EffectType.RESTRICTION:
                    restrictions.append(effect.identifier)
                elif effect.effect_type == EffectType.REQUIREMENT:
                    requirements.append(effect.identifier)
                elif effect.effect_type == EffectType.ALLOWANCE:
                    allowances.append(effect.identifier)

        # Rule 1.0.2: Restrictions take precedence
        if restrictions:
            return PrecedenceResult(
                permitted=False,
                blocked_by="restriction",
                blocking_restrictions=restrictions,
                active_requirements=requirements,
                active_allowances=allowances,
            )

        # If no restrictions, check if we have requirements or allowances
        if requirements or allowances:
            # Requirements take precedence over allowances, but both permit action
            return PrecedenceResult(
                permitted=True,
                active_requirements=requirements,
                active_allowances=allowances,
            )

        # No applicable effects - action is not permitted by default
        # (needs explicit allowance in game rules)
        return PrecedenceResult(permitted=False)

    def _effect_applies_to_action(
        self, effect: PrecedenceEffect, action_identifier: str, context: Any
    ) -> bool:
        """
        Determine if an effect applies to a specific action.

        This matches effect identifiers with action identifiers.
        For example, "cant_play_from_banished" applies to actions like "play_from_banished".
        """
        # Simple string matching for now
        # Effect identifier should be related to action identifier

        # Handle "cant_X" restrictions
        if effect.effect_type == EffectType.RESTRICTION:
            if effect.identifier.startswith("cant_"):
                restricted_action = effect.identifier[5:]  # Remove "cant_"
                return restricted_action in action_identifier
            elif effect.identifier.startswith("only_"):
                # Rule 1.0.2a: "only X" means can't do anything else
                allowed_action = effect.identifier[5:]  # Remove "only_"
                return allowed_action not in action_identifier

        # Handle "must_X" requirements
        elif effect.effect_type == EffectType.REQUIREMENT:
            if effect.identifier.startswith("must_"):
                required_action = effect.identifier[5:]  # Remove "must_"
                return required_action in action_identifier

        # Handle "may_X" allowances
        elif effect.effect_type == EffectType.ALLOWANCE:
            if effect.identifier.startswith("may_"):
                allowed_action = effect.identifier[4:]  # Remove "may_"
                return allowed_action in action_identifier

        # Fallback: exact match
        return effect.identifier in action_identifier

    def has_restriction(self, identifier: str) -> bool:
        """Check if a specific restriction is active."""
        return any(
            e.identifier == identifier and e.effect_type == EffectType.RESTRICTION
            for e in self.effects
        )

    def has_requirement(self, identifier: str) -> bool:
        """Check if a specific requirement is active."""
        return any(
            e.identifier == identifier and e.effect_type == EffectType.REQUIREMENT
            for e in self.effects
        )

    def has_allowance(self, identifier: str) -> bool:
        """Check if a specific allowance is active."""
        return any(
            e.identifier == identifier and e.effect_type == EffectType.ALLOWANCE
            for e in self.effects
        )
