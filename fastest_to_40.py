#!/usr/bin/env python3
"""
Fastest to 40 - Flesh and Blood Card Game Simulator
A Python script to find the optimal 40-card Kano deck using RL.
"""

# Imports
import json
import pandas as pd
import numpy as np
import random
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from collections import defaultdict
import os

# Gymnasium imports
import gymnasium as gym
from gymnasium import spaces

# PyTorch imports for RL training
import torch
import torch.nn as nn
import torch.optim as optim
from torch.distributions import Categorical

# ============================================================================
# DATA LOADING & CARD FILTERING
# ============================================================================


def load_cards(
    db_path: str = "~/repos/github/flesh-and-blood-cards/json/english/card.json",
) -> pd.DataFrame:
    """Load card database and return as DataFrame"""
    db_path = os.path.expanduser(db_path)
    with open(db_path, "r") as f:
        cards = json.load(f)
    return pd.DataFrame(cards)


def is_kano_eligible(card: Dict) -> bool:
    """Check if card is eligible for Kano's deck (Common/Rare only)

    Card Pool Rules (FaB CR 2.11 - Supertypes):
    - Supertypes determine card pool eligibility
    - Classes: Wizard, Guardian, Warrior, etc.
    - Talents: Elemental, Ice, Lightning, Earth, Shadow, etc.

    Kano Hero Supertypes: [Wizard]
    - Can play: Wizard class cards + Generic cards
    - Cannot play: Cards with talent supertypes (Elemental, Ice, Lightning, etc.)

    Example:
    - "Wizard Action" → Eligible (has Wizard class)
    - "Elemental Wizard Action" → NOT eligible (has Elemental talent, Kano lacks this)
    - "Ice Wizard Action" → NOT eligible (has Ice talent, Kano lacks this)

    Note: Iyslander (Elemental Wizard + Essence of Ice) CAN play Elemental cards.
    Note: Oscilio (Elemental Wizard + Essence of Lightning) CAN play Elemental cards.
    """
    types = card.get("types", [])

    # Define talent supertypes (FaB CR 2.11.6b)
    TALENT_SUPERTYPES = {
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

    # Must have Wizard class or Generic
    is_wizard = "Wizard" in types
    is_generic = "Generic" in types

    if not (is_wizard or is_generic):
        return False

    # IMPORTANT: Kano has NO talent supertypes
    # Exclude any card with talent supertypes (Elemental, Ice, Lightning, etc.)
    has_talent = any(talent in types for talent in TALENT_SUPERTYPES)
    if has_talent:
        return False

    # Check if has Common or Rare printing
    printings = card.get("printings", [])
    has_common_or_rare = any(p.get("rarity") in ["C", "R"] for p in printings)

    return has_common_or_rare


# ============================================================================
# CARD ANALYSIS
# ============================================================================


def parse_numeric(value, default=0):
    """Safely parse numeric values from strings"""
    if pd.isna(value) or value == "":
        return default
    try:
        return int(float(value))
    except:
        return default


def analyze_cards(kano_cards: pd.DataFrame) -> pd.DataFrame:
    """Add derived columns and efficiency metrics"""
    # Add derived columns
    kano_cards = kano_cards.copy()
    kano_cards["pitch_val"] = kano_cards["pitch"].apply(lambda x: parse_numeric(x, 0))
    kano_cards["cost_val"] = kano_cards["cost"].apply(lambda x: parse_numeric(x, 0))
    kano_cards["power_val"] = kano_cards["power"].apply(lambda x: parse_numeric(x, 0))
    kano_cards["arcane_val"] = kano_cards["arcane"].apply(lambda x: parse_numeric(x, 0))
    kano_cards["total_damage"] = kano_cards["power_val"] + kano_cards["arcane_val"]

    # Calculate efficiency metrics
    kano_cards["damage_per_cost"] = kano_cards.apply(
        lambda row: row["total_damage"] / max(row["cost_val"], 1), axis=1
    )

    # Identify damage sources
    kano_cards["is_attack"] = kano_cards["types"].apply(
        lambda x: "Attack" in x if isinstance(x, list) else False
    )
    kano_cards["is_arcane"] = kano_cards["arcane_val"] > 0

    return kano_cards


# ============================================================================
# GAME STATE CLASSES
# ============================================================================


@dataclass
class Card:
    """Represents a card in the game"""

    name: str
    pitch: int
    cost: int
    damage: int  # power + arcane
    color: str

    @classmethod
    def from_series(cls, series):
        """Create Card from pandas Series"""
        return cls(
            name=series["name"],
            pitch=int(series.get("pitch_val", 0)),
            cost=int(series.get("cost_val", 0)),
            damage=int(series.get("total_damage", 0)),
            color=series.get("color", "Colorless"),
        )


@dataclass
class GameState:
    """Tracks the current state of the game"""

    deck: List[Card]  # Ordered list, index 0 = top of deck
    hand: List[Card]
    pitch_zone: List[Card]
    damage_dealt: int
    turn_number: int
    resources: int
    game_over: bool
    current_player: str  # 'player' or 'opponent'

    @classmethod
    def new_game(cls, deck_list: List[Card], hand_size: int = 4):
        """Initialize a new game with shuffled deck"""
        deck = deck_list.copy()
        random.shuffle(deck)
        hand = deck[:hand_size]
        remaining_deck = deck[hand_size:]
        return cls(
            deck=remaining_deck,
            hand=hand,
            pitch_zone=[],
            damage_dealt=0,
            turn_number=1,
            resources=0,
            game_over=False,
            current_player="player",  # Player always goes first
        )


# ============================================================================
# GAME LOGIC
# ============================================================================


class GameEngine:
    """Handles game mechanics and state transitions"""

    HAND_SIZE = 4
    TARGET_DAMAGE = 40

    def __init__(self, deck: List[Card]):
        self.initial_deck = deck
        self.reset()

    def reset(self):
        """Reset game to initial state"""
        self.state = GameState.new_game(self.initial_deck, self.HAND_SIZE)
        return self._get_observation()

    def _get_observation(self):
        """Return current observation for RL agent"""
        return {
            "hand": self.state.hand,
            "hand_size": len(self.state.hand),
            "resources": self.state.resources,
            "damage_dealt": self.state.damage_dealt,
            "turn_number": self.state.turn_number,
            "deck_size": len(self.state.deck),
        }

    def draw_cards(self, n: int):
        """Draw n cards from deck to hand"""
        for _ in range(n):
            if len(self.state.hand) >= self.HAND_SIZE:
                break
            if self.state.deck:
                card = self.state.deck.pop(0)
                self.state.hand.append(card)

    def pitch_card(self, card_idx: int) -> bool:
        """Pitch a card from hand to generate resources"""
        if card_idx < 0 or card_idx >= len(self.state.hand):
            return False

        card = self.state.hand.pop(card_idx)
        self.state.resources += card.pitch
        self.state.pitch_zone.append(card)
        return True

    def play_card(self, card_idx: int) -> bool:
        """Play a card from hand if enough resources"""
        if card_idx < 0 or card_idx >= len(self.state.hand):
            return False

        card = self.state.hand[card_idx]
        if card.cost > self.state.resources:
            return False

        self.state.resources -= card.cost
        self.state.damage_dealt += card.damage
        self.state.hand.pop(card_idx)
        return True

    def end_turn(self):
        """End current turn, cleanup, check win condition"""
        # Return pitched cards to bottom of deck
        # For simplicity, just append them (order doesn't matter in basic version)
        self.state.deck.extend(self.state.pitch_zone)
        self.state.pitch_zone = []

        # Check win condition (only check for player, not opponent)
        if (
            self.state.current_player == "player"
            and self.state.damage_dealt >= self.TARGET_DAMAGE
        ):
            self.state.game_over = True
            return True

        # Switch to other player
        if self.state.current_player == "player":
            self.state.current_player = "opponent"
            # Opponent immediately passes turn back (solitaire mode)
            # No actions taken by opponent
            self.state.current_player = "player"

            # Draw up to hand size for player's next turn
            self.draw_cards(self.HAND_SIZE - len(self.state.hand))

            # Next turn (counts as full round: player + opponent)
            self.state.turn_number += 1
            self.state.resources = 0

        # Check if deck is empty (shouldn't happen with 40 cards and cycling)
        if not self.state.deck and not self.state.hand:
            self.state.game_over = True

        return False

    def get_valid_actions(self):
        """Return valid actions for current state"""
        actions = []

        # Can pitch any card in hand
        for i in range(len(self.state.hand)):
            actions.append(("pitch", i))

        # Can play cards we can afford
        for i, card in enumerate(self.state.hand):
            if card.cost <= self.state.resources:
                actions.append(("play", i))

        # Can always end turn
        actions.append(("end_turn", None))

        return actions


# ============================================================================
# GYMNASIUM RL ENVIRONMENT
# ============================================================================


class FastestTo40Env(gym.Env):
    """Gymnasium environment for Fastest to 40"""

    def __init__(self, deck: List[Card], num_runs=10):
        super().__init__()
        self.deck = deck
        self.num_runs = num_runs
        self.game = None

        # Observation space: hand (4 cards) + resources + damage + turn
        # Each card: [pitch, cost, damage, color_encoded]
        # Total: 4*4 + 1 + 1 + 1 = 19 features
        self.observation_space = spaces.Box(
            low=0, high=100, shape=(19,), dtype=np.float32
        )

        # Action space:
        # 0-3: pitch card 0-3
        # 4-7: play card 0-3
        # 8: end turn
        self.action_space = spaces.Discrete(9)

    def reset(self, seed=None):
        """Reset environment with new game"""
        if seed is not None:
            random.seed(seed)
        self.game = GameEngine(self.deck)
        self.game.reset()
        return self._get_obs(), {}

    def _get_obs(self):
        """Convert game state to observation vector"""
        obs = np.zeros(19, dtype=np.float32)

        # Encode hand (4 cards, 4 features each)
        for i, card in enumerate(self.game.state.hand[:4]):
            base = i * 4
            obs[base] = card.pitch / 3.0  # Normalize
            obs[base + 1] = card.cost / 5.0  # Normalize
            obs[base + 2] = card.damage / 10.0  # Normalize
            obs[base + 3] = {"Red": 0, "Yellow": 1, "Blue": 2, "Colorless": 3}.get(
                card.color, 3
            ) / 3.0

        # Global state
        obs[16] = self.game.state.resources / 10.0
        obs[17] = self.game.state.damage_dealt / 40.0
        obs[18] = min(self.game.state.turn_number / 20.0, 1.0)

        return obs

    def step(self, actions):
        """Execute one action in the environment"""
        reward = -0.1  # Small penalty for each action (encourage efficiency)

        if actions < 4:
            # Pitch card
            success = self.game.pitch_card(actions)
            if not success:
                reward = -1  # Invalid action penalty
        elif actions < 8:
            # Play card
            card_idx = actions - 4
            success = self.game.play_card(card_idx)
            if success:
                # Reward for dealing damage (card_damage was dealt this turn)
                # Note: We don't have incremental tracking, so just give small reward
                reward = 0.5
            else:
                reward = -1  # Invalid action penalty
        else:
            # End turn
            won = self.game.end_turn()
            if won:
                reward = (
                    100.0 / self.game.state.turn_number
                )  # Reward inversely proportional to turns
            elif self.game.state.game_over:
                reward = -50  # Lost game

        terminated = self.game.state.game_over
        truncated = self.game.state.turn_number > 50  # Max 50 turns

        return self._get_obs(), reward, terminated, truncated, {}

    def evaluate_deck(self):
        """Run multiple games and return average turns to win"""
        turns_to_win = []

        for run in range(self.num_runs):
            obs, _ = self.reset(seed=run)
            done = False

            while not done:
                # Random policy for now (will be replaced by trained agent)
                action = self.action_space.sample()
                obs, reward, terminated, truncated, _ = self.step(action)
                done = terminated or truncated

            if self.game.state.damage_dealt >= 40:
                turns_to_win.append(self.game.state.turn_number)
            else:
                turns_to_win.append(50)  # Cap at 50 turns for failed games

        return np.mean(turns_to_win)


# ============================================================================
# RL POLICY NETWORK
# ============================================================================


class PolicyNetwork(nn.Module):
    """Simple policy network for Fastest to 40"""

    def __init__(self, obs_dim=19, action_dim=9, hidden_size=64):
        super(PolicyNetwork, self).__init__()

        # Shared network
        self.network = nn.Sequential(
            nn.Linear(obs_dim, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
        )

        # Policy head (actor)
        self.policy_head = nn.Linear(hidden_size, action_dim)

        # Value head (critic)
        self.value_head = nn.Linear(hidden_size, 1)

    def forward(self, x):
        """Forward pass"""
        if isinstance(x, np.ndarray):
            x = torch.FloatTensor(x)

        features = self.network(x)
        logits = self.policy_head(features)
        value = self.value_head(features)

        return logits, value

    def get_action(self, obs, deterministic=False):
        """Get action from observation"""
        logits, value = self.forward(obs)

        if deterministic:
            action = torch.argmax(logits, dim=-1)
        else:
            dist = Categorical(logits=logits)
            action = dist.sample()

        return action.item(), logits, value

    def save(self, path: str):
        """Save policy to file"""
        torch.save(self.state_dict(), path)

    def load(self, path: str):
        """Load policy from file"""
        self.load_state_dict(torch.load(path))
        self.eval()


# ============================================================================
# RL TRAINING
# ============================================================================


def train_agent(deck: List[Card], total_timesteps: int = 50000, verbose=True):
    """Train RL agent on given deck using simplified policy gradient"""

    # Create environment
    env = FastestTo40Env(deck, num_runs=1)

    # Create policy network
    policy = PolicyNetwork(obs_dim=19, action_dim=9, hidden_size=64)
    optimizer = optim.Adam(policy.parameters(), lr=3e-4)

    # Training tracking
    episode_rewards = []
    episode_lengths = []
    best_reward = float("-inf")

    if verbose:
        print(f"\n  Training policy network...")
        print(f"    Total timesteps: {total_timesteps}")
        print(f"    Network parameters: {sum(p.numel() for p in policy.parameters())}")

    obs, _ = env.reset(seed=42)
    episode_reward = 0
    episode_length = 0
    episode_count = 0

    # Storage for trajectory
    log_probs = []
    values = []
    rewards = []
    dones = []

    for step in range(total_timesteps):
        # Get action from policy
        action, logits, value = policy.get_action(obs, deterministic=False)

        # Calculate log probability
        dist = Categorical(logits=logits)
        log_prob = dist.log_prob(torch.tensor(action))

        # Take step in environment
        next_obs, reward, terminated, truncated, _ = env.step(action)
        done = terminated or truncated

        # Store trajectory
        log_probs.append(log_prob)
        values.append(value)
        rewards.append(reward)
        dones.append(done)

        episode_reward += reward
        episode_length += 1

        obs = next_obs

        # Episode ended
        if done:
            episode_rewards.append(episode_reward)
            episode_lengths.append(episode_length)
            episode_count += 1

            # Update policy every episode (simplified policy gradient)
            if len(log_probs) > 0:
                # Calculate returns (discounted rewards)
                returns = []
                R = 0
                gamma = 0.99
                for r in reversed(rewards):
                    R = r + gamma * R
                    returns.insert(0, R)

                returns = torch.tensor(returns, dtype=torch.float32)
                # Normalize returns
                if len(returns) > 1:
                    returns = (returns - returns.mean()) / (returns.std() + 1e-8)

                # Calculate policy loss and value loss
                log_probs_tensor = torch.stack(log_probs)
                values_tensor = torch.stack(values).squeeze()

                # Policy gradient loss
                advantages = returns - values_tensor.detach()
                policy_loss = -(log_probs_tensor * advantages).mean()

                # Value loss (MSE)
                value_loss = nn.MSELoss()(values_tensor, returns)

                # Total loss
                loss = policy_loss + 0.5 * value_loss

                # Update
                optimizer.zero_grad()
                loss.backward()
                torch.nn.utils.clip_grad_norm_(policy.parameters(), 0.5)
                optimizer.step()

            # Clear trajectory
            log_probs = []
            values = []
            rewards = []
            dones = []

            # Reset environment
            obs, _ = env.reset()
            episode_reward = 0
            episode_length = 0

            # Track best reward
            if episode_rewards[-1] > best_reward:
                best_reward = episode_rewards[-1]

            # Print progress
            if verbose and episode_count % 100 == 0:
                recent_rewards = (
                    episode_rewards[-100:]
                    if len(episode_rewards) >= 100
                    else episode_rewards
                )
                avg_reward = np.mean(recent_rewards)
                avg_length = np.mean(
                    episode_lengths[-100:]
                    if len(episode_lengths) >= 100
                    else episode_lengths
                )
                print(
                    f"    Episode {episode_count:4d} | Avg Reward: {avg_reward:7.2f} | Avg Length: {avg_length:5.1f} | Best: {best_reward:7.2f}"
                )

    if verbose:
        print(f"  Training complete!")
        print(f"    Episodes completed: {episode_count}")
        print(f"    Final avg reward (last 100): {np.mean(episode_rewards[-100:]):.2f}")

    return policy


def evaluate_deck_with_policy(
    deck: List[Card], policy: PolicyNetwork, num_runs: int = 10, verbose=False
) -> float:
    """Evaluate a deck using trained policy"""
    env = FastestTo40Env(deck, num_runs=num_runs)
    turns = []

    for run in range(num_runs):
        obs, _ = env.reset(seed=run)
        done = False
        action_count = 0
        max_actions = 500  # Safety limit

        while not done and action_count < max_actions:
            # Use policy to select action (greedy)
            action, _, _ = policy.get_action(obs, deterministic=True)
            obs, reward, terminated, truncated, _ = env.step(action)
            done = terminated or truncated
            action_count += 1

        if env.game.state.damage_dealt >= 40:
            turns.append(env.game.state.turn_number)
        else:
            turns.append(50)  # Failed to reach target

    avg_turns = np.mean(turns)

    if verbose:
        print(
            f"  Deck evaluation: {avg_turns:.2f} turns (best: {min(turns)}, worst: {max(turns)})"
        )

    return avg_turns


# ============================================================================
# DECK OPTIMIZATION
# ============================================================================


def generate_candidate_decks(
    card_pool: pd.DataFrame, num_decks: int = 100, strategy: str = "random"
) -> List[List[Card]]:
    """Generate candidate decks using different strategies"""
    decks = []
    eligible_cards = card_pool[card_pool["total_damage"] > 0].copy()

    if len(eligible_cards) == 0:
        raise ValueError("No eligible cards with damage > 0 found in card pool")

    print(f"  Generating {num_decks} candidate decks using '{strategy}' strategy...")
    print(f"  Card pool: {len(eligible_cards)} cards with damage > 0")

    for i in range(num_decks):
        if strategy == "random":
            # Fully random deck composition
            deck_indices = np.random.choice(eligible_cards.index, size=40, replace=True)
            deck = [Card.from_series(eligible_cards.loc[idx]) for idx in deck_indices]

        elif strategy == "high_efficiency":
            # Bias towards high damage efficiency cards
            weights = eligible_cards["damage_per_cost"].values
            weights = weights / weights.sum()
            deck_indices = np.random.choice(
                eligible_cards.index, size=40, replace=True, p=weights
            )
            deck = [Card.from_series(eligible_cards.loc[idx]) for idx in deck_indices]

        elif strategy == "balanced":
            # Mix of high efficiency and resource balance
            # Aim for ~30% red (pitch 1), ~40% yellow (pitch 2), ~30% blue (pitch 3)
            deck = []
            red_cards = eligible_cards[eligible_cards["pitch_val"] == 1]
            yellow_cards = eligible_cards[eligible_cards["pitch_val"] == 2]
            blue_cards = eligible_cards[eligible_cards["pitch_val"] == 3]

            # Add red cards (12 cards, 30%)
            if len(red_cards) > 0:
                for _ in range(12):
                    card = Card.from_series(red_cards.sample(1).iloc[0])
                    deck.append(card)

            # Add yellow cards (16 cards, 40%)
            if len(yellow_cards) > 0:
                for _ in range(16):
                    card = Card.from_series(yellow_cards.sample(1).iloc[0])
                    deck.append(card)

            # Add blue cards (12 cards, 30%)
            if len(blue_cards) > 0:
                for _ in range(12):
                    card = Card.from_series(blue_cards.sample(1).iloc[0])
                    deck.append(card)

            # Fill remaining with random if needed
            while len(deck) < 40:
                card = Card.from_series(eligible_cards.sample(1).iloc[0])
                deck.append(card)

        else:
            raise ValueError(f"Unknown strategy: {strategy}")

        decks.append(deck)

        if (i + 1) % 20 == 0:
            print(f"    Generated {i + 1}/{num_decks} decks...")

    return decks


def optimize_deck(
    card_pool: pd.DataFrame,
    num_candidates: int = 100,
    training_timesteps: int = 50000,
    evaluation_runs: int = 10,
    top_k: int = 5,
    verbose: bool = True,
):
    """Find optimal deck composition using RL-trained policy"""

    if verbose:
        print(f"\n{'=' * 60}")
        print("DECK OPTIMIZATION")
        print(f"{'=' * 60}")
        print(f"  Candidates: {num_candidates}")
        print(f"  Training timesteps: {training_timesteps}")
        print(f"  Evaluation runs per deck: {evaluation_runs}")
        print(f"  Top-k decks to return: {top_k}")

    # Generate candidate decks with different strategies
    print(f"\n[1/4] Generating candidate decks...")
    candidates = []

    # Generate decks with different strategies
    random_decks = generate_candidate_decks(
        card_pool, num_decks=num_candidates // 3, strategy="random"
    )
    candidates.extend(random_decks)

    efficiency_decks = generate_candidate_decks(
        card_pool, num_decks=num_candidates // 3, strategy="high_efficiency"
    )
    candidates.extend(efficiency_decks)

    balanced_decks = generate_candidate_decks(
        card_pool, num_decks=num_candidates - len(candidates), strategy="balanced"
    )
    candidates.extend(balanced_decks)

    print(f"  Total candidates generated: {len(candidates)}")

    # Train a policy on a representative deck first
    print(f"\n[2/4] Training base policy on representative deck...")
    # Use a high-efficiency deck for training
    base_deck = efficiency_decks[0]
    policy = train_agent(base_deck, total_timesteps=training_timesteps, verbose=verbose)

    # Evaluate all candidates
    print(f"\n[3/4] Evaluating all candidates...")
    results = []
    for i, deck in enumerate(candidates):
        avg_turns = evaluate_deck_with_policy(
            deck, policy, num_runs=evaluation_runs, verbose=False
        )
        results.append((avg_turns, deck, i))

        if (i + 1) % 10 == 0:
            best_so_far = min(r[0] for r in results)
            print(
                f"    Evaluated {i + 1}/{len(candidates)} decks | Best so far: {best_so_far:.2f} turns"
            )

    # Sort by average turns (lower is better)
    results.sort(key=lambda x: x[0])

    print(f"\n[4/4] Optimization complete!")
    print(f"  Best deck: {results[0][0]:.2f} turns")
    print(f"  Worst deck: {results[-1][0]:.2f} turns")
    print(f"  Average: {np.mean([r[0] for r in results]):.2f} turns")
    print(f"  Returning top {top_k} decks")

    return results[:top_k], policy


def save_deck(deck: List[Card], filename: str, avg_turns: float, rank: int = 1):
    """Save deck list to file"""
    with open(filename, "w") as f:
        f.write(f"# Fastest to 40 - Optimal Deck #{rank}\n")
        f.write(f"# Average Turns: {avg_turns:.2f}\n")
        f.write(f"# Generated: {pd.Timestamp.now()}\n\n")

        # Count card frequencies
        card_counts = defaultdict(int)
        for card in deck:
            card_counts[card.name] += 1

        f.write("## Deck List (40 cards)\n\n")
        for name, count in sorted(card_counts.items()):
            f.write(f"{count}x {name}\n")

        f.write(f"\n## Card Details\n\n")
        f.write(
            f"{'Card Name':<40} | {'Pitch':>5} | {'Cost':>4} | {'Damage':>6} | {'Color':>10}\n"
        )
        f.write("-" * 80 + "\n")

        # Show unique cards
        unique_cards = {}
        for card in deck:
            if card.name not in unique_cards:
                unique_cards[card.name] = card

        for name in sorted(unique_cards.keys()):
            card = unique_cards[name]
            count = card_counts[name]
            f.write(
                f"{name[:40]:<40} | {card.pitch:>5} | {card.cost:>4} | {card.damage:>6} | {card.color:>10}\n"
            )

    print(f"  Saved deck to: {filename}")


# ============================================================================
# DECK ANALYSIS & GAMEPLAY
# ============================================================================


def analyze_deck(deck: List[Card]) -> Dict:
    """Analyze deck composition and return statistics"""
    colors = [card.color for card in deck]
    pitches = [card.pitch for card in deck]
    damages = [card.damage for card in deck]
    costs = [card.cost for card in deck]

    stats = {
        "total_cards": len(deck),
        "color_distribution": pd.Series(colors).value_counts().to_dict(),
        "avg_pitch": np.mean(pitches),
        "avg_damage": np.mean(damages),
        "avg_cost": np.mean(costs),
        "total_damage_potential": sum(damages),
        "pitch_distribution": {
            "red": sum(1 for p in pitches if p == 1),
            "yellow": sum(1 for p in pitches if p == 2),
            "blue": sum(1 for p in pitches if p == 3),
        },
    }

    return stats


def print_deck_analysis(deck: List[Card], avg_turns: float = None):
    """Print deck analysis to console"""
    stats = analyze_deck(deck)
    print(f"\n{'=' * 60}")
    print(f"DECK ANALYSIS")
    print(f"{'=' * 60}")
    print(f"Total Cards: {stats['total_cards']}")
    if avg_turns is not None:
        print(f"Average Turns to Win: {avg_turns:.2f}")
    print(f"\nDamage Statistics:")
    print(f"  Average Damage per Card: {stats['avg_damage']:.2f}")
    print(f"  Total Damage Potential: {stats['total_damage_potential']}")
    print(f"  Average Cost: {stats['avg_cost']:.2f}")

    print(f"\nResource Statistics:")
    print(f"  Average Pitch: {stats['avg_pitch']:.2f}")
    print(f"  Red (pitch 1): {stats['pitch_distribution']['red']} cards")
    print(f"  Yellow (pitch 2): {stats['pitch_distribution']['yellow']} cards")
    print(f"  Blue (pitch 3): {stats['pitch_distribution']['blue']} cards")

    print(f"\nColor Distribution:")
    for color, count in sorted(stats["color_distribution"].items()):
        color_name = color if color else "Colorless"
        print(f"  {color_name}: {count} cards")


def simulate_game(deck: List[Card], policy: PolicyNetwork, verbose=True, seed=None):
    """Simulate a single game and show turn-by-turn breakdown"""
    env = FastestTo40Env(deck, num_runs=1)
    obs, _ = env.reset(seed=seed)

    if verbose:
        print("=" * 60)
        print("SAMPLE GAMEPLAY")
        print("=" * 60)

    turn_log = []
    done = False
    action_count = 0
    max_actions = 500

    current_turn = 1
    turn_actions = []

    while not done and action_count < max_actions:
        # Get action from policy
        action, _, _ = policy.get_action(obs, deterministic=True)

        # Record state before action
        prev_turn = env.game.state.turn_number
        prev_damage = env.game.state.damage_dealt
        prev_resources = env.game.state.resources

        # Take action
        obs, reward, terminated, truncated, _ = env.step(action)
        done = terminated or truncated
        action_count += 1

        # Decode action
        if action < 4:
            action_str = f"Pitch card {action}"
        elif action < 8:
            action_str = f"Play card {action - 4}"
        else:
            action_str = "End turn"

        turn_actions.append(action_str)

        # Check if turn ended
        if env.game.state.turn_number != prev_turn or done:
            damage_this_turn = env.game.state.damage_dealt - prev_damage
            turn_log.append(
                {
                    "turn": prev_turn,
                    "actions": turn_actions.copy(),
                    "damage": damage_this_turn,
                    "total_damage": env.game.state.damage_dealt,
                }
            )
            turn_actions = []

    if verbose:
        print(f"\nGame completed in {env.game.state.turn_number} turns!")
        print(f"Total damage dealt: {env.game.state.damage_dealt}")
        print(f"Target reached: {env.game.state.damage_dealt >= 40}")

        print(f"\nTurn-by-turn breakdown:")
        for entry in turn_log[:10]:  # Show first 10 turns
            print(
                f"  Turn {entry['turn']}: +{entry['damage']} damage (total: {entry['total_damage']})"
            )
            if verbose and len(entry["actions"]) > 0:
                print(f"    Actions: {', '.join(entry['actions'][:5])}")

    return env.game.state.turn_number, env.game.state.damage_dealt


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Fastest to 40 - Kano Deck Optimizer")
    print("=" * 60)

    # Load cards
    print("\n[1/3] Loading card database...")
    all_cards = load_cards()
    print(f"  Total cards in database: {len(all_cards)}")

    # Filter for Kano-eligible cards
    print("\n[2/3] Filtering for Kano-eligible cards...")
    eligible_mask = all_cards.apply(lambda row: is_kano_eligible(row.to_dict()), axis=1)
    kano_cards = all_cards[eligible_mask].copy()
    print(f"  Kano-eligible cards (Common/Rare Wizard+Generic): {len(kano_cards)}")

    # Analyze cards
    print("\n[3/3] Analyzing cards...")
    kano_cards = analyze_cards(kano_cards)
    print(f"  Analysis complete!")

    # Display summary statistics
    print("\n" + "=" * 60)
    print("CARD POOL SUMMARY")
    print("=" * 60)
    print(f"Total eligible cards: {len(kano_cards)}")
    print(f"Cards with damage > 0: {len(kano_cards[kano_cards['total_damage'] > 0])}")
    print(f"Attack cards: {kano_cards['is_attack'].sum()}")
    print(f"Arcane damage cards: {kano_cards['is_arcane'].sum()}")

    print("\n" + "-" * 60)
    print("Top 10 Cards by Damage Efficiency")
    print("-" * 60)
    top_damage = kano_cards[kano_cards["total_damage"] > 0].nlargest(
        10, "damage_per_cost"
    )
    for idx, row in top_damage.iterrows():
        print(
            f"  {row['name'][:40]:<40} | Cost: {row['cost_val']:2d} | Damage: {row['total_damage']:2d} | Efficiency: {row['damage_per_cost']:.2f}"
        )

    print("\n" + "-" * 60)
    print("Sample High-Damage Cards")
    print("-" * 60)
    high_damage = kano_cards[kano_cards["total_damage"] >= 5].nlargest(
        10, "total_damage"
    )
    for idx, row in high_damage.iterrows():
        card_type = (
            "Attack" if row["is_attack"] else "Arcane" if row["is_arcane"] else "Other"
        )
        print(
            f"  {row['name'][:40]:<40} | Type: {card_type:<6} | Pitch: {row['pitch_val']} | Cost: {row['cost_val']:2d} | Damage: {row['total_damage']:2d}"
        )

    print("\n" + "=" * 60)
    print("Phase 1 Complete!")
    print("=" * 60)

    # ========================================================================
    # PHASE 2 TESTING: Game Environment
    # ========================================================================
    print("\n" + "=" * 60)
    print("PHASE 2: Testing Game Engine")
    print("=" * 60)

    # Create a sample deck from top damage cards
    print("\n[1/4] Creating sample deck...")
    damage_cards = kano_cards[kano_cards["total_damage"] > 0].copy()
    sample_deck_data = damage_cards.nlargest(40, "damage_per_cost")
    sample_deck = [Card.from_series(row) for _, row in sample_deck_data.iterrows()]
    print(f"  Sample deck created: {len(sample_deck)} cards")
    print(f"  Average damage: {np.mean([c.damage for c in sample_deck]):.2f}")
    print(f"  Average pitch: {np.mean([c.pitch for c in sample_deck]):.2f}")
    print(f"  Average cost: {np.mean([c.cost for c in sample_deck]):.2f}")

    # Initialize game engine
    print("\n[2/4] Initializing GameEngine...")
    game = GameEngine(sample_deck)
    obs = game.reset()
    print(f"  Game initialized!")
    print(f"  Hand size: {obs['hand_size']}")
    print(f"  Deck size: {obs['deck_size']}")
    print(f"  Turn: {obs['turn_number']}")
    print(f"  Damage dealt: {obs['damage_dealt']}")

    # Test basic game mechanics
    print("\n[3/4] Testing game mechanics...")
    print(f"  Initial hand: {[c.name[:30] for c in game.state.hand]}")

    # Pitch a card
    print(f"\n  Testing pitch_card()...")
    initial_resources = game.state.resources
    pitch_result = game.pitch_card(0)
    print(f"    Pitch successful: {pitch_result}")
    print(f"    Resources: {initial_resources} -> {game.state.resources}")
    print(f"    Hand size: 4 -> {len(game.state.hand)}")
    print(f"    Pitch zone: {len(game.state.pitch_zone)} cards")

    # Play a card
    print(f"\n  Testing play_card()...")
    # Find a card we can afford
    affordable_idx = None
    for i, card in enumerate(game.state.hand):
        if card.cost <= game.state.resources:
            affordable_idx = i
            break

    if affordable_idx is not None:
        card_to_play = game.state.hand[affordable_idx]
        initial_damage = game.state.damage_dealt
        play_result = game.play_card(affordable_idx)
        print(f"    Played: {card_to_play.name[:30]}")
        print(f"    Play successful: {play_result}")
        print(f"    Damage: {initial_damage} -> {game.state.damage_dealt}")
        print(f"    Hand size: {len(game.state.hand) + 1} -> {len(game.state.hand)}")
    else:
        print(f"    No affordable cards to play")

    # End turn
    print(f"\n  Testing end_turn()...")
    initial_turn = game.state.turn_number
    won = game.end_turn()
    print(f"    Turn: {initial_turn} -> {game.state.turn_number}")
    print(f"    Current player: {game.state.current_player}")
    print(f"    Hand refilled to: {len(game.state.hand)} cards")
    print(
        f"    Pitch zone returned to deck: {len(game.state.pitch_zone)} cards in pitch zone"
    )
    print(f"    Resources reset: {game.state.resources}")
    print(f"    Game won: {won}")
    print(f"    Game over: {game.state.game_over}")
    print(f"    (Note: Opponent automatically passed their turn)")

    # Run a full test game
    print("\n[4/4] Running full test game (max 50 turns)...")
    game.reset()
    turn_log = []

    while not game.state.game_over and game.state.turn_number <= 50:
        turn_start_damage = game.state.damage_dealt

        # Simple greedy strategy: pitch high-pitch cards, play high-damage cards
        # Sort hand by pitch (descending) for pitching
        hand_with_idx = [(i, card) for i, card in enumerate(game.state.hand)]
        hand_with_idx.sort(key=lambda x: x[1].pitch, reverse=True)

        # Pitch cards until we have enough resources
        pitched_count = 0
        while pitched_count < 2 and game.state.hand:
            # Always pitch first card (already sorted by pitch)
            game.pitch_card(0)
            pitched_count += 1

        # Play cards in order of damage (descending)
        while game.state.hand:
            # Find highest damage card we can afford
            best_idx = None
            best_damage = 0
            for i, card in enumerate(game.state.hand):
                if card.cost <= game.state.resources and card.damage > best_damage:
                    best_idx = i
                    best_damage = card.damage

            if best_idx is not None:
                game.play_card(best_idx)
            else:
                break

        # End turn
        won = game.end_turn()
        turn_damage = game.state.damage_dealt - turn_start_damage
        turn_log.append(
            {
                "turn": game.state.turn_number - 1,
                "damage": turn_damage,
                "total_damage": game.state.damage_dealt,
            }
        )

        if won:
            break

    print(f"\n  Game completed!")
    print(f"  Total turns: {game.state.turn_number}")
    print(f"  Total damage: {game.state.damage_dealt}")
    print(f"  Target reached: {game.state.damage_dealt >= 40}")

    print(f"\n  Turn-by-turn breakdown (first 10 turns):")
    for entry in turn_log[:10]:
        print(
            f"    Turn {entry['turn']}: +{entry['damage']} damage (total: {entry['total_damage']})"
        )

    print("\n" + "=" * 60)
    print("Phase 2 Complete!")
    print("=" * 60)

    # ========================================================================
    # PHASE 3 TESTING: Gymnasium RL Environment
    # ========================================================================
    print("\n" + "=" * 60)
    print("PHASE 3: Testing Gymnasium RL Environment")
    print("=" * 60)

    # Create environment with sample deck
    print("\n[1/5] Creating FastestTo40Env...")
    env = FastestTo40Env(sample_deck, num_runs=10)
    print(f"  Environment created!")
    print(f"  Observation space: {env.observation_space}")
    print(f"  Action space: {env.action_space}")

    # Test reset
    print("\n[2/5] Testing reset()...")
    obs, info = env.reset(seed=42)
    print(f"  Reset successful!")
    print(f"  Observation shape: {obs.shape}")
    print(f"  Observation dtype: {obs.dtype}")
    print(f"  Observation range: [{obs.min():.3f}, {obs.max():.3f}]")
    print(f"  Sample observation (first 5 values): {obs[:5]}")

    # Test step
    print("\n[3/5] Testing step()...")
    print(f"  Initial damage: {env.game.state.damage_dealt}")

    # Take a few actions
    for i in range(5):
        action = env.action_space.sample()
        obs, reward, terminated, truncated, info = env.step(action)
        action_type = "pitch" if action < 4 else "play" if action < 8 else "end_turn"
        print(
            f"    Action {i + 1}: {action_type} (action={action}), reward={reward:.2f}, terminated={terminated}, truncated={truncated}"
        )

        if terminated or truncated:
            print(f"    Game ended after {i + 1} actions")
            break

    print(f"  Final damage: {env.game.state.damage_dealt}")
    print(f"  Final turn: {env.game.state.turn_number}")

    # Test full game with random policy
    print("\n[4/5] Testing full game with random policy...")
    obs, _ = env.reset(seed=123)
    done = False
    action_count = 0
    max_actions = 500  # Safety limit

    while not done and action_count < max_actions:
        action = env.action_space.sample()
        obs, reward, terminated, truncated, _ = env.step(action)
        done = terminated or truncated
        action_count += 1

    print(f"  Game completed!")
    print(f"  Total actions taken: {action_count}")
    print(f"  Final turn: {env.game.state.turn_number}")
    print(f"  Final damage: {env.game.state.damage_dealt}")
    print(f"  Target reached: {env.game.state.damage_dealt >= 40}")

    # Test evaluate_deck
    print("\n[5/5] Testing evaluate_deck()...")
    print(f"  Running 10 games with random policy...")
    avg_turns = env.evaluate_deck()
    print(f"  Average turns to win (or timeout): {avg_turns:.2f}")

    print("\n" + "=" * 60)
    print("Phase 3 Complete!")
    print("=" * 60)

    # ========================================================================
    # PHASE 4 TESTING: RL Training Setup
    # ========================================================================
    print("\n" + "=" * 60)
    print("PHASE 4: Testing RL Training")
    print("=" * 60)

    # Test policy network initialization
    print("\n[1/5] Testing PolicyNetwork initialization...")
    policy = PolicyNetwork(obs_dim=19, action_dim=9, hidden_size=64)
    print(f"  Policy network created!")
    print(f"  Total parameters: {sum(p.numel() for p in policy.parameters()):,}")
    print(f"  Architecture:")
    print(f"    Input: 19 features")
    print(f"    Hidden: 64 units (2 layers)")
    print(f"    Output: 9 actions + 1 value")

    # Test forward pass
    print("\n[2/5] Testing forward pass...")
    test_obs = env.observation_space.sample()
    logits, value = policy.forward(test_obs)
    print(f"  Forward pass successful!")
    print(f"  Input shape: {test_obs.shape}")
    print(f"  Logits shape: {logits.shape}")
    print(f"  Value shape: {value.shape}")
    print(f"  Logits range: [{logits.min().item():.3f}, {logits.max().item():.3f}]")
    print(f"  Value: {value.item():.3f}")

    # Test action selection
    print("\n[3/5] Testing action selection...")
    action_det, _, _ = policy.get_action(test_obs, deterministic=True)
    action_stoch, _, _ = policy.get_action(test_obs, deterministic=False)
    print(f"  Deterministic action: {action_det}")
    print(f"  Stochastic action: {action_stoch}")
    print(f"  Action in valid range: {0 <= action_det < 9 and 0 <= action_stoch < 9}")

    # Test training with small timesteps
    print("\n[4/5] Testing training loop (1000 timesteps)...")
    print(f"  Training on sample deck...")
    trained_policy = train_agent(sample_deck, total_timesteps=1000, verbose=True)
    print(f"  Training completed successfully!")

    # Test save/load policy
    print("\n[5/6] Testing save/load policy...")
    import tempfile

    with tempfile.NamedTemporaryFile(suffix=".pt", delete=False) as tmp:
        tmp_path = tmp.name
    print(f"  Saving policy to {tmp_path}...")
    trained_policy.save(tmp_path)
    print(f"  Policy saved successfully!")

    print(f"  Loading policy from {tmp_path}...")
    loaded_policy = PolicyNetwork(obs_dim=19, action_dim=9, hidden_size=64)
    loaded_policy.load(tmp_path)
    print(f"  Policy loaded successfully!")

    # Verify loaded policy works
    test_obs = env.observation_space.sample()
    action1, _, _ = trained_policy.get_action(test_obs, deterministic=True)
    action2, _, _ = loaded_policy.get_action(test_obs, deterministic=True)
    print(f"  Original policy action: {action1}")
    print(f"  Loaded policy action: {action2}")
    print(f"  Actions match: {action1 == action2}")

    # Clean up temp file
    os.unlink(tmp_path)

    # Test policy evaluation
    print("\n[6/6] Testing deck evaluation with trained policy...")
    print(f"  Running 10 evaluation games...")
    avg_turns_trained = evaluate_deck_with_policy(
        sample_deck, trained_policy, num_runs=10, verbose=True
    )
    print(f"  Average turns with trained policy: {avg_turns_trained:.2f}")
    print(f"  Baseline (random policy from Phase 3): {avg_turns:.2f}")
    if avg_turns_trained < avg_turns:
        print(
            f"  Improvement: {((avg_turns - avg_turns_trained) / avg_turns * 100):.1f}%"
        )
    else:
        print(f"  Note: Policy needs more training timesteps for improvement")

    print("\n" + "=" * 60)
    print("Phase 4 Complete!")
    print("=" * 60)

    # ========================================================================
    # PHASE 5 TESTING: Deck Optimization
    # ========================================================================
    print("\n" + "=" * 60)
    print("PHASE 5: Testing Deck Optimization")
    print("=" * 60)

    # Test candidate deck generation
    print("\n[1/5] Testing candidate deck generation...")
    print("  Testing 'random' strategy...")
    random_test_decks = generate_candidate_decks(
        kano_cards, num_decks=5, strategy="random"
    )
    print(f"    Generated {len(random_test_decks)} random decks")
    print(
        f"    Sample deck avg damage: {np.mean([c.damage for c in random_test_decks[0]]):.2f}"
    )

    print("  Testing 'high_efficiency' strategy...")
    efficiency_test_decks = generate_candidate_decks(
        kano_cards, num_decks=5, strategy="high_efficiency"
    )
    print(f"    Generated {len(efficiency_test_decks)} efficiency decks")
    print(
        f"    Sample deck avg damage: {np.mean([c.damage for c in efficiency_test_decks[0]]):.2f}"
    )

    print("  Testing 'balanced' strategy...")
    balanced_test_decks = generate_candidate_decks(
        kano_cards, num_decks=5, strategy="balanced"
    )
    print(f"    Generated {len(balanced_test_decks)} balanced decks")
    print(
        f"    Sample deck avg damage: {np.mean([c.damage for c in balanced_test_decks[0]]):.2f}"
    )

    # Test deck evaluation
    print("\n[2/5] Testing deck evaluation with policy...")
    test_deck = efficiency_test_decks[0]
    test_policy = PolicyNetwork(obs_dim=19, action_dim=9, hidden_size=64)
    avg_test_turns = evaluate_deck_with_policy(
        test_deck, test_policy, num_runs=5, verbose=True
    )
    print(f"  Evaluation completed: {avg_test_turns:.2f} turns")

    # Test save_deck
    print("\n[3/5] Testing save_deck()...")
    import tempfile

    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as tmp:
        tmp_deck_path = tmp.name
    save_deck(test_deck, tmp_deck_path, avg_test_turns, rank=1)
    print(f"  Deck saved to: {tmp_deck_path}")

    # Verify file was created and contains expected content
    with open(tmp_deck_path, "r") as f:
        saved_content = f.read()
    print(f"  File size: {len(saved_content)} bytes")
    print(f"  Contains 40 cards: {'40 cards' in saved_content}")
    os.unlink(tmp_deck_path)
    print(f"  Temp file cleaned up")

    # Test optimization with very small parameters
    print("\n[4/5] Testing optimize_deck() with minimal parameters...")
    print("  Running optimization with 10 candidates, 500 training timesteps...")
    top_decks, opt_policy = optimize_deck(
        kano_cards,
        num_candidates=10,
        training_timesteps=500,
        evaluation_runs=5,
        top_k=3,
        verbose=True,
    )
    print(f"\n  Optimization returned {len(top_decks)} decks")
    print(f"  Best deck: {top_decks[0][0]:.2f} turns")
    print(f"  2nd best: {top_decks[1][0]:.2f} turns")
    print(f"  3rd best: {top_decks[2][0]:.2f} turns")

    # Save the best deck
    print("\n[5/5] Saving optimal deck to file...")
    best_turns, best_deck, best_idx = top_decks[0]
    save_deck(best_deck, "optimal_deck.txt", best_turns, rank=1)
    print(f"  Optimal deck saved!")

    # Show deck statistics
    print(f"\n  Deck Statistics:")
    print(f"    Total cards: {len(best_deck)}")
    print(f"    Avg damage: {np.mean([c.damage for c in best_deck]):.2f}")
    print(f"    Avg pitch: {np.mean([c.pitch for c in best_deck]):.2f}")
    print(f"    Avg cost: {np.mean([c.cost for c in best_deck]):.2f}")

    # Color distribution
    colors = [c.color for c in best_deck]
    color_counts = pd.Series(colors).value_counts()
    print(f"    Color distribution:")
    for color, count in color_counts.items():
        print(f"      {color}: {count} cards")

    print("\n" + "=" * 60)
    print("Phase 5 Complete!")
    print("=" * 60)

    # ========================================================================
    # PHASE 6 TESTING: Results & Analysis
    # ========================================================================
    print("\n" + "=" * 60)
    print("PHASE 6: Testing Results & Analysis")
    print("=" * 60)

    # Test deck analysis
    print("\n[1/3] Testing analyze_deck()...")
    stats = analyze_deck(best_deck)
    print(f"  Analysis completed!")
    print(f"    Total cards: {stats['total_cards']}")
    print(f"    Avg damage: {stats['avg_damage']:.2f}")
    print(f"    Avg pitch: {stats['avg_pitch']:.2f}")
    print(f"    Avg cost: {stats['avg_cost']:.2f}")
    print(f"    Total damage potential: {stats['total_damage_potential']}")

    # Test print_deck_analysis
    print("\n[2/3] Testing print_deck_analysis()...")
    print_deck_analysis(best_deck, avg_turns=best_turns)

    # Test simulate_game
    print("\n[3/3] Testing simulate_game()...")
    turns, damage = simulate_game(best_deck, opt_policy, verbose=True, seed=42)
    print(f"\n  Simulation complete!")
    print(f"    Turns: {turns}")
    print(f"    Damage: {damage}")
    print(f"    Success: {damage >= 40}")

    print("\n" + "=" * 60)
    print("Phase 6 Complete!")
    print("=" * 60)

    # ========================================================================
    # FINAL SUMMARY
    # ========================================================================
    print("\n" + "=" * 60)
    print("ALL PHASES COMPLETE!")
    print("=" * 60)
    print(f"\n✓ Phase 1: Data Loading & Card Analysis")
    print(f"✓ Phase 2: Game Environment")
    print(f"✓ Phase 3: Gymnasium RL Environment")
    print(f"✓ Phase 4: RL Training Setup")
    print(f"✓ Phase 5: Deck Optimization")
    print(f"✓ Phase 6: Results & Analysis")
    print(f"\nOptimal deck saved to: optimal_deck.txt")
    print(f"Average turns to win: {best_turns:.2f}")
    print(f"\n{'=' * 60}")
    print("Run complete! Check optimal_deck.txt for results.")
    print("=" * 60)
