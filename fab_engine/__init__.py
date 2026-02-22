"""
FAB Engine - Flesh and Blood Two-Player Gymnasium Environment

A high-fidelity game engine implementing CR rules for Kano vs Generic 2-player games.
"""

__version__ = "0.1.0"

from fab_engine.cards.model import CardTemplate, CardInstance, HeroState
from fab_engine.cards.loader import CardLoader
from fab_engine.engine.game import GameEngine, GameState, GamePhase, CombatStep
from fab_engine.gym_env.env import FaBEnv

__all__ = [
    "CardTemplate",
    "CardInstance",
    "HeroState",
    "CardLoader",
    "GameEngine",
    "GameState",
    "GamePhase",
    "CombatStep",
    "FaBEnv",
]
