import pytest
import numpy as np
from fab_engine.gym_env.env import FaBEnv


class TestFaBEnv:
    def test_env_creation(self):
        """Test environment can be created."""
        env = FaBEnv()
        assert env.observation_space is not None
        assert env.action_space is not None

    def test_reset(self):
        """Test environment reset."""
        env = FaBEnv()
        obs, info = env.reset()

        assert isinstance(obs, dict)
        assert "player_life" in obs
        assert "opponent_life" in obs
        assert "player_hand_size" in obs
        assert "player_deck_size" in obs

        assert obs["player_life"][0] == 15.0
        assert obs["opponent_life"][0] == 20.0

    def test_step(self):
        """Test environment step."""
        env = FaBEnv()
        obs, info = env.reset()

        action = 0
        obs, reward, terminated, truncated, info = env.step(action)

        assert isinstance(obs, dict)
        assert isinstance(reward, float)
        assert isinstance(terminated, bool)
        assert isinstance(truncated, bool)
        assert isinstance(info, dict)

    def test_game_completes(self):
        """Test that games can complete with random actions."""
        env = FaBEnv()
        obs, info = env.reset()

        steps = 0
        max_steps = 100

        while steps < max_steps:
            legal_actions = env.game_engine.get_legal_actions(0)
            if not legal_actions:
                break

            action = len(legal_actions) - 1
            obs, reward, terminated, truncated, info = env.step(action)
            steps += 1

            if terminated or truncated:
                print(f"Game completed in {steps} steps")
                print(f"Winner: {info.get('winner')}")
                break

    def test_observation_space_shape(self):
        """Test observation space has correct shapes."""
        env = FaBEnv()
        obs, info = env.reset()

        assert obs["player_life"].shape == (1,)
        assert obs["player_resources"].shape == (1,)
        assert obs["player_action_points"].shape == (1,)
        assert obs["player_hand_size"].shape == (1,)
        assert obs["hand_cards"].shape == (11, 8)
        assert obs["top_of_deck"].shape == (8,)

    def test_legal_actions(self):
        """Test that legal actions can be retrieved."""
        env = FaBEnv()
        obs, info = env.reset()

        actions = env.game_engine.get_legal_actions(0)
        assert isinstance(actions, list)
