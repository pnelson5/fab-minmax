"""
Action types and definitions for FAB Engine.
"""

from enum import Enum, auto
from dataclasses import dataclass, field
from typing import List, Optional


class ActionType(Enum):
    PITCH_CARD = auto()
    PLAY_CARD_FROM_HAND = auto()
    PLAY_CARD_FROM_ARSENAL = auto()
    ACTIVATE_HERO_ABILITY = auto()
    ACTIVATE_EQUIPMENT = auto()
    ACTIVATE_WEAPON = auto()
    DECLARE_DEFENDERS = auto()
    PLAY_ATTACK_REACTION = auto()
    PLAY_DEFENSE_REACTION = auto()
    PASS_PRIORITY = auto()
    ARSENAL_CARD = auto()
    END_PHASE = auto()


@dataclass
class Action:
    action_type: ActionType
    player_id: int
    card_instance_id: int = -1
    target_ids: List[int] = field(default_factory=list)
    defender_ids: List[int] = field(default_factory=list)

    def __repr__(self) -> str:
        return f"Action({self.action_type.name}, player={self.player_id}, card={self.card_instance_id})"


@dataclass
class ActionResult:
    success: bool
    damage_dealt: int = 0
    arcane_damage_dealt: int = 0
    cards_drawn: int = 0
    message: str = ""
    action_points_gained: int = 0

    @property
    def is_game_over(self) -> bool:
        return self.damage_dealt >= 40 or self.arcane_damage_dealt >= 40
