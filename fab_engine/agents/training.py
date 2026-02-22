"""
Training loop for FAB RL agent.
"""

import torch
import torch.optim as optim
from typing import Dict, Any, List
import numpy as np

from fab_engine.agents.policy import FABPolicy, FABValue


def train_fab_agent(
    env,
    num_episodes: int = 1000,
    learning_rate: float = 3e-4,
    gamma: float = 0.99,
    save_path: str = "fab_policy.pt",
) -> Dict[str, List[float]]:
    """Train the FAB agent."""

    policy = FABPolicy()
    value_network = FABValue()

    policy_optimizer = optim.Adam(policy.parameters(), lr=learning_rate)
    value_optimizer = optim.Adam(value_network.parameters(), lr=learning_rate)

    episode_rewards = []
    episode_losses = []

    for episode in range(num_episodes):
        obs, info = env.reset()
        done = False
        episode_reward = 0.0

        log_probs = []
        values = []
        rewards = []

        while not done:
            action = policy.get_action({k: torch.tensor(v) for k, v in obs.items()})

            obs, reward, terminated, truncated, info = env.step(action)
            done = terminated or truncated

            episode_reward += reward
            rewards.append(reward)

        episode_rewards.append(episode_reward)

        if episode % 100 == 0:
            print(f"Episode {episode}: Reward = {episode_reward:.2f}")

    torch.save(policy.state_dict(), save_path)

    return {
        "episode_rewards": episode_rewards,
        "episode_losses": episode_losses,
    }


def evaluate_agent(env, policy: FABPolicy, num_episodes: int = 100) -> float:
    """Evaluate the agent."""

    total_wins = 0.0

    for _ in range(num_episodes):
        obs, info = env.reset()
        done = False

        while not done:
            action = policy.get_action({k: torch.tensor(v) for k, v in obs.items()})
            obs, reward, terminated, truncated, info = env.step(action)
            done = terminated or truncated

        if info.get("winner") == 0:
            total_wins += 1

    return total_wins / num_episodes
