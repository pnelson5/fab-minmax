"""
Zone system for FAB Engine.
"""

from enum import Enum, auto
from typing import List, Optional
from dataclasses import dataclass, field


class ZoneType(Enum):
    DECK = auto()
    HAND = auto()
    ARSENAL = auto()
    PITCH = auto()
    GRAVEYARD = auto()
    BANISHED = auto()
    HEAD = auto()
    CHEST = auto()
    ARMS = auto()
    LEGS = auto()
    WEAPON_1 = auto()
    WEAPON_2 = auto()
    COMBAT_CHAIN = auto()
    STACK = auto()
    HERO = auto()


@dataclass
class Zone:
    zone_type: ZoneType
    owner_id: int
    max_size: int = -1
    _cards: List = field(default_factory=list)

    @property
    def cards(self) -> List:
        return self._cards

    @property
    def is_empty(self) -> bool:
        return len(self._cards) == 0

    @property
    def size(self) -> int:
        return len(self._cards)

    def add(self, card, position: str = "top") -> bool:
        if self.max_size > 0 and len(self._cards) >= self.max_size:
            return False
        if position == "top":
            self._cards.insert(0, card)
        elif position == "bottom":
            self._cards.append(card)
        elif isinstance(position, int):
            self._cards.insert(position, card)
        else:
            self._cards.append(card)
        return True

    def remove(self, card) -> bool:
        if card in self._cards:
            self._cards.remove(card)
            return True
        return False

    def remove_at(self, index: int):
        if 0 <= index < len(self._cards):
            return self._cards.pop(index)
        return None

    def peek_top(self):
        return self._cards[0] if self._cards else None

    def draw_top(self):
        return self._cards.pop(0) if self._cards else None

    def shuffle(self):
        import random

        random.shuffle(self._cards)

    def contains(self, card) -> bool:
        return card in self._cards

    def get_by_id(self, instance_id: int):
        for c in self._cards:
            if c.instance_id == instance_id:
                return c
        return None
