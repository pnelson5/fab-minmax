"""
Policy network for FAB RL agent.
"""

import torch
import torch.nn as nn
from typing import Dict, Any


class FABPolicy(nn.Module):
    """Policy network for the FAB agent."""

    def __init__(self, obs_dim: int = 108, action_dim: int = 100):
        super().__init__()

        self.network = nn.Sequential(
            nn.Linear(obs_dim, 256),
            nn.ReLU(),
            nn.Linear(256, 256),
            nn.ReLU(),
            nn.Linear(256, action_dim),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.network(x)

    def get_action(
        self, obs: Dict[str, torch.Tensor], deterministic: bool = False
    ) -> int:
        """Get action from observation."""
        flat_obs = self._flatten_obs(obs)

        with torch.no_grad():
            logits = self.forward(flat_obs)
            probs = torch.softmax(logits, dim=-1)

            if deterministic:
                action = torch.argmax(probs, dim=-1)
            else:
                action = torch.multinomial(probs, 1)

        return action.item()

    def _flatten_obs(self, obs: Dict[str, torch.Tensor]) -> torch.Tensor:
        """Flatten observation dict into a single tensor."""
        parts = []

        parts.append(obs.get("player_life", torch.zeros(1)))
        parts.append(obs.get("player_resources", torch.zeros(1)))
        parts.append(obs.get("player_action_points", torch.zeros(1)))
        parts.append(obs.get("player_hand_size", torch.zeros(1)))
        parts.append(obs.get("player_deck_size", torch.zeros(1)))
        parts.append(obs.get("player_pitch_size", torch.zeros(1)))
        parts.append(obs.get("opponent_life", torch.zeros(1)))
        parts.append(obs.get("opponent_hand_size", torch.zeros(1)))
        parts.append(obs.get("opponent_deck_size", torch.zeros(1)))
        parts.append(obs.get("phase", torch.zeros(1)))
        parts.append(obs.get("turn_number", torch.zeros(1)))
        parts.append(obs.get("combat_open", torch.zeros(1)))

        hand = obs.get("hand_cards", torch.zeros(11, 8))
        parts.append(hand.flatten())

        top = obs.get("top_of_deck", torch.zeros(8))
        parts.append(top)

        return torch.cat(parts)


class FABValue(nn.Module):
    """Value network for the FAB agent."""

    def __init__(self, obs_dim: int = 108):
        super().__init__()

        self.network = nn.Sequential(
            nn.Linear(obs_dim, 256),
            nn.ReLU(),
            nn.Linear(256, 256),
            nn.ReLU(),
            nn.Linear(256, 1),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.network(x)
