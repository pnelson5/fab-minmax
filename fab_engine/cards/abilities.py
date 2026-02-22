"""
Ability registry for FAB Engine.
"""

from typing import Callable, Dict, Optional, Any
from dataclasses import dataclass


EffectFn = Callable[[Any, Any, Any], None]


@dataclass
class AbilityRegistry:
    _play_effects: Dict[str, EffectFn]
    _on_hit_effects: Dict[str, EffectFn]
    _defend_effects: Dict[str, EffectFn]
    _hero_abilities: Dict[str, EffectFn]
    _activated_abilities: Dict[str, EffectFn]

    def __init__(self):
        self._play_effects = {}
        self._on_hit_effects = {}
        self._defend_effects = {}
        self._hero_abilities = {}
        self._activated_abilities = {}

    def register_play_effect(self, card_name: str, fn: EffectFn):
        self._play_effects[card_name] = fn

    def register_on_hit(self, card_name: str, fn: EffectFn):
        self._on_hit_effects[card_name] = fn

    def register_defend_effect(self, card_name: str, fn: EffectFn):
        self._defend_effects[card_name] = fn

    def register_hero_ability(self, hero_name: str, fn: EffectFn):
        self._hero_abilities[hero_name] = fn

    def register_activated_ability(self, card_name: str, fn: EffectFn):
        self._activated_abilities[card_name] = fn

    def get_play_effect(self, card_name: str) -> Optional[EffectFn]:
        return self._play_effects.get(card_name)

    def get_on_hit_effect(self, card_name: str) -> Optional[EffectFn]:
        return self._on_hit_effects.get(card_name)

    def get_defend_effect(self, card_name: str) -> Optional[EffectFn]:
        return self._defend_effects.get(card_name)

    def get_hero_ability(self, hero_name: str) -> Optional[EffectFn]:
        return self._hero_abilities.get(hero_name)

    def get_activated_ability(self, card_name: str) -> Optional[EffectFn]:
        return self._activated_abilities.get(card_name)


ABILITY_REGISTRY = AbilityRegistry()
