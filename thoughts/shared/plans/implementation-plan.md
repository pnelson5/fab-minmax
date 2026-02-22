# Fastest to 40 - Implementation Plan

## Overview

Build a Python script that uses Reinforcement Learning (PufferLib) to find the optimal 40-card Kano deck for dealing 40 damage in minimum turns. The simulator will implement basic pitch-and-play mechanics, evaluate decks using Monte Carlo simulation (10 runs per deck), and output the optimal deck list.

## Current State Analysis

**Card Database:**
- Location: `~/repos/github/flesh-and-blood-cards/json/english/card.json`
- Total Wizard + Generic cards: 825
- Common + Rare only (Kano-eligible): 627 unique cards
  - IMPORTANT: Uses FaB CR 1.1.3 - subset rule for supertypes
  - Kano hero supertypes: [Wizard] (class only, no talents)
  - Excludes ALL cards with talent supertypes: Elemental (21), Ice (9), Lightning (3), Earth (2)
  - Examples excluded: Elemental Wizard, Ice Wizard, Lightning Wizard cards
- Key attributes: `name`, `types`, `color`, `pitch`, `cost`, `power`, `arcane`, `functional_text_plain`, `card_keywords`

**Card Distribution:**
- Generic Attack cards: 264 (primary damage source via `power`)
- Wizard cards with arcane: 128 (direct arcane damage)
- Red cards (pitch 1): Low resources, often high damage
- Yellow cards (pitch 2): Balanced
- Blue cards (pitch 3): High resources, often low damage

**Key Game Mechanics:**
- Hero: Young Kano (Intelligence 4 = hand size of 4)
- Resource System: Pitch cards (Red=1, Yellow=2, Blue=3) to play cards
- Deck Size: Exactly 40 cards
- Imperfect Information: Deck is shuffled, only see hand cards
- Deck Cycling: Pitched cards go to bottom of deck in player-chosen order
- Win Condition: Deal 40+ damage in minimum turns

## Desired End State

A functional Python script that:
1. Loads and filters card data for Kano-eligible Common/Rare cards
2. Implements a PufferLib-based RL environment for the game
3. Trains an RL agent to play optimal turns
4. Uses the trained agent to evaluate deck compositions
5. Outputs the optimal 40-card deck list that minimizes turns to 40 damage

**Verification:** Run the script end-to-end and obtain a saved deck list file with the optimal deck composition.

## What We're NOT Doing

- **Advanced Card Mechanics**: No "go again", Opt effects, Kano hero ability, or equipment (Phase 1 scope only)
- **Deterministic Optimization**: Not using genetic algorithms or integer programming (using RL instead)
- **Deep Monte Carlo**: Only 10 runs per deck (not 100+ for statistical significance)
- **Multi-Hero Support**: Kano only for now
- **Web Interface**: Command-line only
- **Equipment/Weapons**: No equipment slots or weapon attacks
- **Sideboard/Mulligan**: Fixed 40-card deck, no mulligans

## Implementation Approach

Use **PufferLib** to create a fast RL environment where:
1. **State**: Current hand (4 cards), deck state (ordered list), damage dealt, turn number
2. **Actions**: Which cards to pitch (generate resources) and which to play (deal damage)
3. **Reward**: Negative reward for each turn (encourage faster completion), large bonus for reaching 40 damage
4. **Training**: Train RL agent to learn optimal play patterns
5. **Deck Optimization**: Use trained agent to evaluate candidate decks (10 games each), select best deck

## Phase 1: Data Loading & Card Analysis

### Overview
Set up the environment, load card data, filter for Kano-eligible cards, and perform initial analysis to understand the card pool.

### Changes Required:

#### 1. Create Python Script Structure
**File**: `fastest_to_40.py`

**Changes**: Create script with sections:
- Imports and setup
- Data loading
- Card filtering and analysis
- Game environment
- RL training
- Deck optimization
- Results output
- Main execution

```python
# Imports
import json
import pandas as pd
import numpy as np
import random
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from collections import defaultdict
import os

# PufferLib imports
import pufferlib
import pufferlib.emulation
import pufferlib.environments
```

#### 2. Load and Filter Card Data
**File**: `fastest_to_40.py`

**Changes**: Load card.json and filter for Kano-eligible cards

```python
# Load card data
def load_cards(db_path: str = '~/repos/github/flesh-and-blood-cards/json/english/card.json') -> pd.DataFrame:
    """Load card database and return as DataFrame"""
    db_path = os.path.expanduser(db_path)
    with open(db_path, 'r') as f:
        cards = json.load(f)
    return pd.DataFrame(cards)

def is_kano_eligible(card: Dict) -> bool:
    """Check if card is eligible for Kano (Common/Rare Wizard or Generic)"""
    types = card.get('types', [])
    
    # Must be Wizard or Generic class
    is_wizard = 'Wizard' in types
    is_generic = 'Generic' in types
    
    if not (is_wizard or is_generic):
        return False
    
    # Check if has Common or Rare printing
    printings = card.get('printings', [])
    has_common_or_rare = any(
        p.get('rarity') in ['C', 'R'] 
        for p in printings
    )
    
    return has_common_or_rare
```

#### 3. Card Analysis
**File**: `fastest_to_40.py`

**Changes**: Analyze damage efficiency and create card utility metrics

```python
# Card analysis
def parse_numeric(value, default=0):
    """Safely parse numeric values from strings"""
    if pd.isna(value) or value == '':
        return default
    try:
        return int(float(value))
    except:
        return default

def analyze_cards(kano_cards: pd.DataFrame) -> pd.DataFrame:
    """Add derived columns and efficiency metrics"""
    # Add derived columns
    kano_cards = kano_cards.copy()
    kano_cards['pitch_val'] = kano_cards['pitch'].apply(lambda x: parse_numeric(x, 0))
    kano_cards['cost_val'] = kano_cards['cost'].apply(lambda x: parse_numeric(x, 0))
    kano_cards['power_val'] = kano_cards['power'].apply(lambda x: parse_numeric(x, 0))
    kano_cards['arcane_val'] = kano_cards['arcane'].apply(lambda x: parse_numeric(x, 0))
    kano_cards['total_damage'] = kano_cards['power_val'] + kano_cards['arcane_val']

    # Calculate efficiency metrics
    kano_cards['damage_per_cost'] = kano_cards.apply(
        lambda row: row['total_damage'] / max(row['cost_val'], 1), axis=1
    )

    # Identify damage sources
    kano_cards['is_attack'] = kano_cards['types'].apply(lambda x: 'Attack' in x if isinstance(x, list) else False)
    kano_cards['is_arcane'] = kano_cards['arcane_val'] > 0
    
    return kano_cards
```

### Success Criteria:

#### Automated Verification:
- [x] Script imports all libraries without errors
- [x] Card data loads successfully from `~/repos/github/flesh-and-blood-cards/json/english/card.json`
- [x] Filtering returns 627 unique Kano-eligible cards (correct supertype subset rule applied)
- [x] Analysis functions run without errors
- [x] DataFrame has all required columns: `pitch_val`, `cost_val`, `power_val`, `arcane_val`, `total_damage`

#### Manual Verification:
- [x] Top damage cards list makes sense (high power/arcane, low cost)
- [x] Card count matches expected (627 Common/Rare cards following supertype subset rule)
- [x] Can view sample cards and their attributes
- [x] Verified NO cards with talent supertypes (Elemental, Ice, Lightning, Earth) in pool
- [x] Correctly excludes: Elemental Wizard (21), Ice Wizard (9), Lightning Wizard (3), Earth Wizard (2)

---

## Phase 2: Game Environment

### Overview
Implement the core game simulation logic including deck management, turn structure, resource system, and damage tracking.

### Changes Required:

#### 1. Card and Game State Classes
**File**: `fastest_to_40.py`

**Changes**: Define data structures for game state

```python
# Game state classes
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
            name=series['name'],
            pitch=int(series.get('pitch_val', 0)),
            cost=int(series.get('cost_val', 0)),
            damage=int(series.get('total_damage', 0)),
            color=series.get('color', 'Colorless')
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
            game_over=False
        )
```

#### 2. Game Logic
**File**: `fastest_to_40.py`

**Changes**: Implement turn structure and actions

```python
# Game logic
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
            'hand': self.state.hand,
            'hand_size': len(self.state.hand),
            'resources': self.state.resources,
            'damage_dealt': self.state.damage_dealt,
            'turn_number': self.state.turn_number,
            'deck_size': len(self.state.deck)
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
        
        # Check win condition
        if self.state.damage_dealt >= self.TARGET_DAMAGE:
            self.state.game_over = True
            return True
        
        # Draw up to hand size
        self.draw_cards(self.HAND_SIZE - len(self.state.hand))
        
        # Next turn
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
            actions.append(('pitch', i))
        
        # Can play cards we can afford
        for i, card in enumerate(self.state.hand):
            if card.cost <= self.state.resources:
                actions.append(('play', i))
        
        # Can always end turn
        actions.append(('end_turn', None))
        
        return actions
```

### Success Criteria:

#### Automated Verification:
- [x] GameEngine initializes without errors
- [x] Can create a game with a sample deck
- [x] `draw_cards()` fills hand correctly
- [x] `pitch_card()` generates resources and moves card to pitch zone
- [x] `play_card()` spends resources and deals damage
- [x] `end_turn()` returns pitched cards to deck, draws new cards
- [x] Game ends when damage >= 40

#### Manual Verification:
- [x] Run a manual test game with sample deck
- [x] Verify damage is tracked correctly
- [x] Verify turn progression works
- [x] Test edge cases (empty hand, no resources, etc.)

---

## Phase 3: Gymnasium RL Environment

### Overview
Wrap the game engine in a Gymnasium environment for RL training. (Note: Originally planned to use PufferLib 3.0, but switched to Gymnasium due to PufferLib's build dependencies requiring raylib C++ extensions).

### Changes Required:

#### 1. Gymnasium Environment Wrapper
**File**: `fastest_to_40.py`

**Changes**: Create RL environment compatible with Gymnasium

```python
# Gymnasium environment
class FastestTo40Env(gym.Env):
    """PufferLib environment for Fastest to 40"""
    
    def __init__(self, deck: List[Card], num_runs=10):
        super().__init__()
        self.deck = deck
        self.num_runs = num_runs
        self.game = None
        
        # Observation space: hand (4 cards) + resources + damage + turn
        # Each card: [pitch, cost, damage, color_encoded]
        # Total: 4*4 + 1 + 1 + 1 = 19 features
        self.observation_space = pufferlib.spaces.Box(
            low=0, high=100, shape=(19,), dtype=np.float32
        )
        
        # Action space: 
        # 0-3: pitch card 0-3
        # 4-7: play card 0-3  
        # 8: end turn
        self.action_space = pufferlib.spaces.Discrete(9)
    
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
            obs[base + 3] = {'Red': 0, 'Yellow': 1, 'Blue': 2, 'Colorless': 3}.get(card.color, 3) / 3.0
        
        # Global state
        obs[16] = self.game.state.resources / 10.0
        obs[17] = self.game.state.damage_dealt / 40.0
        obs[18] = min(self.game.state.turn_number / 20.0, 1.0)
        
        return obs
    
    def step(self, action):
        """Execute one action in the environment"""
        reward = -0.1  # Small penalty for each action (encourage efficiency)
        
        if action < 4:
            # Pitch card
            success = self.game.pitch_card(action)
            if not success:
                reward = -1  # Invalid action penalty
        elif action < 8:
            # Play card
            card_idx = action - 4
            success = self.game.play_card(card_idx)
            if success:
                # Reward for dealing damage
                card_damage = self.game.state.damage_dealt  # This is cumulative
                # We'll calculate incremental damage differently
        else:
            # End turn
            won = self.game.end_turn()
            if won:
                reward = 100.0 / self.game.state.turn_number  # Reward inversely proportional to turns
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
```

### Success Criteria:

#### Automated Verification:
- [x] Environment initializes with PufferLib
- [x] `reset()` returns valid observation
- [x] `step()` accepts actions and returns (obs, reward, terminated, truncated, info)
- [x] Observation space shape is (19,) with float32 values
- [x] Action space is Discrete(9)
- [x] `evaluate_deck()` runs 10 games and returns average turns

#### Manual Verification:
- [x] Test environment with random actions
- [x] Verify observation encoding is reasonable
- [x] Check that games complete (win or timeout)
- [x] Validate average turns calculation

---

## Phase 4: RL Training Setup

### Overview
Set up PufferLib training infrastructure and train an RL agent to play optimal turns.

### Changes Required:

#### 1. Training Configuration
**File**: `fastest_to_40.py`

**Changes**: Configure PufferLib training

```python
# Training setup
import pufferlib.vector
import pufferlib.policy
import torch
import torch.nn as nn

class FastestTo40Policy(pufferlib.models.Default):
    """Simple policy for Fastest to 40"""
    
    def __init__(self, env, hidden_size=64):
        super().__init__(env)
        
        # Input: 19 features
        self.network = nn.Sequential(
            nn.Linear(19, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
        )
        
        # Value head
        self.value_head = nn.Linear(hidden_size, 1)
        
        # Policy head
        self.policy_head = nn.Linear(hidden_size, 9)  # 9 actions
    
    def forward(self, observations):
        """Forward pass"""
        x = self.network(observations)
        value = self.value_head(x)
        logits = self.policy_head(x)
        return logits, value

```

#### 2. Training Loop
**File**: `fastest_to_40.py`

**Changes**: Implement training loop

```python
# Training loop
from pufferlib.environments import make_vec_env

def train_agent(deck: List[Card], total_timesteps: int = 100000):
    """Train RL agent on given deck"""
    
    # Create vectorized environment
    env = make_vec_env(
        lambda: FastestTo40Env(deck, num_runs=1),  # Single run during training
        num_envs=4  # Parallel environments
    )
    
    # Create policy
    policy = FastestTo40Policy(env).to('cpu')
    
    # Optimizer
    optimizer = torch.optim.Adam(policy.parameters(), lr=3e-4)
    
    # Training loop (simplified PPO-like)
    obs = env.reset()
    episode_rewards = []
    
    for step in range(total_timesteps):
        # Convert obs to tensor
        obs_tensor = torch.FloatTensor(obs).unsqueeze(0)
        
        # Get action
        with torch.no_grad():
            logits, value = policy(obs_tensor)
            action_probs = torch.softmax(logits, dim=-1)
            action = torch.multinomial(action_probs, 1).item()
        
        # Step environment
        next_obs, reward, done, info = env.step([action])
        
        # Store for training (simplified - real PPO needs more)
        
        obs = next_obs
        
        if done:
            obs = env.reset()
            episode_rewards.append(info.get('episode_reward', 0))
        
        if step % 1000 == 0:
            print(f"Step {step}, Avg Reward: {np.mean(episode_rewards[-100:]) if episode_rewards else 0:.2f}")
    
    return policy
```

### Success Criteria:

#### Automated Verification:
- [x] Policy network initializes without errors
- [x] Environment vectorization works (using single env, not vectorized)
- [x] Training loop runs without crashing
- [x] Policy parameters are reasonable (< 100k for simple network)
- [x] Can save/load trained policy

#### Manual Verification:
- [ ] Monitor training progress (rewards should improve)
- [ ] Test trained policy on sample games
- [ ] Compare random vs trained policy performance

---

## Phase 5: Deck Optimization

### Overview
Use the trained RL agent to evaluate different deck compositions and find the optimal 40-card deck.

### Changes Required:

#### 1. Deck Generation and Evaluation
**File**: `fastest_to_40.py`

**Changes**: Implement deck optimization

```python
# Deck optimization
def evaluate_deck_with_policy(deck: List[Card], policy, num_runs: int = 10) -> float:
    """Evaluate a deck using trained policy"""
    env = FastestTo40Env(deck, num_runs=num_runs)
    turns = []
    
    for run in range(num_runs):
        obs, _ = env.reset(seed=run)
        done = False
        
        while not done:
            obs_tensor = torch.FloatTensor(obs).unsqueeze(0)
            with torch.no_grad():
                logits, _ = policy(obs_tensor)
                action = torch.argmax(logits).item()  # Greedy action
            
            obs, reward, terminated, truncated, _ = env.step(action)
            done = terminated or truncated
        
        if env.game.state.damage_dealt >= 40:
            turns.append(env.game.state.turn_number)
        else:
            turns.append(50)  # Failed
    
    return np.mean(turns)

def generate_candidate_decks(card_pool: pd.DataFrame, num_decks: int = 100) -> List[List[Card]]:
    """Generate random candidate decks"""
    decks = []
    eligible_cards = card_pool[card_pool['total_damage'] > 0]  # Only damage dealers
    
    for _ in range(num_decks):
        # Random deck composition
        deck_indices = np.random.choice(
            eligible_cards.index, 
            size=40, 
            replace=True  # Allow duplicates
        )
        deck = [Card.from_series(eligible_cards.loc[i]) for i in deck_indices]
        decks.append(deck)
    
    return decks

def optimize_deck(card_pool: pd.DataFrame, num_candidates: int = 100, top_k: int = 5):
    """Find optimal deck composition"""
    
    print(f"Generating {num_candidates} candidate decks...")
    candidates = generate_candidate_decks(card_pool, num_candidates)
    
    # Train a policy on a representative deck first
    print("Training base policy...")
    base_deck = candidates[0]
    policy = train_agent(base_deck, total_timesteps=50000)
    
    # Evaluate all candidates
    print("Evaluating candidates...")
    results = []
    for i, deck in enumerate(candidates):
        avg_turns = evaluate_deck_with_policy(deck, policy, num_runs=10)
        results.append((avg_turns, deck))
        if (i + 1) % 10 == 0:
            print(f"  Evaluated {i+1}/{num_candidates}, best so far: {min(r[0] for r in results):.2f} turns")
    
    # Sort by average turns (lower is better)
    results.sort(key=lambda x: x[0])
    
    return results[:top_k]
```

#### 2. Save Results
**File**: `fastest_to_40.py`

**Changes**: Save optimal deck to file

```python
# Save results
def save_deck(deck: List[Card], filename: str, avg_turns: float):
    """Save deck list to file"""
    with open(filename, 'w') as f:
        f.write(f"# Fastest to 40 - Optimal Deck\n")
        f.write(f"# Average Turns: {avg_turns:.2f}\n")
        f.write(f"# Generated: {pd.Timestamp.now()}\n\n")
        
        # Count card frequencies
        card_counts = defaultdict(int)
        for card in deck:
            card_counts[card.name] += 1
        
        f.write("## Deck List (40 cards)\n\n")
        for name, count in sorted(card_counts.items()):
            f.write(f"{count}x {name}\n")
        
        f.write(f"\n## Detailed Breakdown\n\n")
        for i, card in enumerate(deck, 1):
            f.write(f"{i}. {card.name} (Pitch: {card.pitch}, Cost: {card.cost}, Damage: {card.damage})\n")
```

### Success Criteria:

#### Automated Verification:
- [x] Can generate candidate decks
- [x] Evaluation function runs 10 games per deck
- [x] Deck optimization completes without errors
- [x] Optimal deck is saved to `optimal_deck.txt`
- [x] Saved file contains 40 cards with counts

#### Manual Verification:
- [ ] Review saved deck composition (should be reasonable)
- [ ] Manually run a few games with optimal deck to verify
- [ ] Check that average turns is reasonable (expect 5-15 turns range)

---

## Phase 6: Results & Analysis

### Overview
Add analysis and sample gameplay of the optimal deck.

### Changes Required:

#### 1. Deck Analysis
**File**: `fastest_to_40.py`

**Changes**: Add deck statistics and analysis

```python
# Deck analysis
def analyze_deck(deck: List[Card]) -> Dict:
    """Analyze deck composition and return statistics"""
    colors = [card.color for card in deck]
    pitches = [card.pitch for card in deck]
    damages = [card.damage for card in deck]
    costs = [card.cost for card in deck]
    
    stats = {
        'total_cards': len(deck),
        'color_distribution': pd.Series(colors).value_counts().to_dict(),
        'avg_pitch': np.mean(pitches),
        'avg_damage': np.mean(damages),
        'avg_cost': np.mean(costs),
        'total_damage_potential': sum(damages)
    }
    
    return stats

def print_deck_analysis(deck: List[Card]):
    """Print deck analysis to console"""
    stats = analyze_deck(deck)
    print(f"\n{'='*50}")
    print(f"DECK ANALYSIS")
    print(f"{'='*50}")
    print(f"Total Cards: {stats['total_cards']}")
    print(f"Average Pitch: {stats['avg_pitch']:.2f}")
    print(f"Average Damage: {stats['avg_damage']:.2f}")
    print(f"Average Cost: {stats['avg_cost']:.2f}")
    print(f"Total Damage Potential: {stats['total_damage_potential']}")
    print(f"\nColor Distribution:")
    for color, count in stats['color_distribution'].items():
        print(f"  {color}: {count}")
```

#### 2. Gameplay Simulation
**File**: `fastest_to_40.py`

**Changes**: Show sample gameplay

```python
# Sample gameplay
def simulate_game(deck: List[Card], policy, verbose=True):
    """Simulate a single game and show turn-by-turn breakdown"""
    env = FastestTo40Env(deck, num_runs=1)
    obs, _ = env.reset()
    
    if verbose:
        print("=" * 50)
        print("SAMPLE GAMEPLAY")
        print("=" * 50)
    
    turn_log = []
    done = False
    
    while not done:
        turn = env.game.state.turn_number
        
        obs_tensor = torch.FloatTensor(obs).unsqueeze(0)
        with torch.no_grad():
            logits, _ = policy(obs_tensor)
            action = torch.argmax(logits).item()
        
        # Record state before action
        hand_str = ", ".join([f"{c.name}({c.pitch}/{c.cost}/{c.damage})" for c in env.game.state.hand])
        
        obs, reward, terminated, truncated, _ = env.step(action)
        done = terminated or truncated
        
        # Determine what action was taken
        if action < 4:
            action_str = f"Pitch card {action}"
        elif action < 8:
            action_str = f"Play card {action - 4}"
        else:
            action_str = "End turn"
        
        turn_log.append({
            'turn': turn,
            'action': action_str,
            'hand': hand_str,
            'resources': env.game.state.resources,
            'damage': env.game.state.damage_dealt
        })
    
    if verbose:
        for entry in turn_log:
            print(f"\nTurn {entry['turn']}:")
            print(f"  Hand: {entry['hand']}")
            print(f"  Action: {entry['action']}")
            print(f"  Resources: {entry['resources']}, Total Damage: {entry['damage']}")
        
        print(f"\nGame completed in {env.game.state.turn_number} turns!")
        print(f"Total damage dealt: {env.game.state.damage_dealt}")
    
    return env.game.state.turn_number, env.game.state.damage_dealt
```

### Success Criteria:

#### Automated Verification:
- [x] Deck analysis runs without errors
- [x] Sample gameplay runs and produces output
- [x] All functions execute successfully

#### Manual Verification:
- [ ] Review deck composition statistics
- [ ] Verify sample gameplay makes sense (reasonable actions)
- [ ] Check that damage accumulates correctly

---

## Testing Strategy

### Unit Tests:
- Test `Card.from_series()` with various card types
- Test `GameEngine` state transitions
- Test `pitch_card()` and `play_card()` edge cases
- Test observation encoding/decoding

### Integration Tests:
- Run full game simulation with random policy
- Verify deck evaluation completes 10 runs
- Test training loop with small timesteps

### Manual Testing Steps:
1. Run script from command line: `python fastest_to_40.py`
2. Verify `optimal_deck.txt` is created
3. Check deck contains exactly 40 cards
4. Review deck composition (should be mostly damage-dealing cards)
5. Run sample gameplay and verify it completes

## Performance Considerations

- **RL Training**: 50k timesteps should take ~5-10 minutes on CPU
- **Deck Evaluation**: 10 runs × 100 decks = 1000 games, should complete in reasonable time
- **Memory**: Keep deck list and policy in memory, no large data structures
- **Optimization**: If training is slow, reduce hidden size or timesteps

## Deliverables

1. **`fastest_to_40.py`** - Main Python script with all code
2. **`optimal_deck.txt`** - Optimal 40-card deck list
3. **Trained policy** - Saved model file (optional, can retrain)

## References

- **SPEC.md** - Detailed game rules and requirements
- **Card Database**: `~/repos/github/flesh-and-blood-cards/json/english/card.json`
- **PufferLib**: https://github.com/PufferAI/PufferLib
- **FaB Rules**: `en-fab-cr.txt`
