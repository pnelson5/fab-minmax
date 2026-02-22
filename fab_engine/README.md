# Flesh and Blood Game Engine Tutorial

This document explains how to use the FAB engine to build, train, and evaluate RL agents for the Flesh and Blood card game.

## Table of Contents
1. [Installation](#installation)
2. [Quick Start](#quick-start)
3. [Understanding the Game Engine](#understanding-the-game-engine)
4. [The Gymnasium Environment](#the-gymnasium-environment)
5. [Training an Agent](#training-an-agent)
6. [Evaluating a Deck](#evaluating-a-deck)
7. [Customizing the Game](#customizing-the-game)

## Installation

Install the package in development mode:

```bash
cd /Users/pxn/repos/github/fab-minmax
uv pip install -e .
```

You also need the Flesh and Blood card database:

```bash
# The card database should be at:
# ~/repos/github/flesh-and-blood-cards/json/english/card.json
```

## Quick Start

Run a simple game with random actions:

```python
from fab_engine.gym_env.env import FaBEnv

# Create the environment
env = FaBEnv()

# Reset to start a new game
obs, info = env.reset(seed=42)

# Play until the game ends
done = False
step = 0
while not done:
    # Get the number of available actions
    active = env.game_engine.state.active_player_id
    actions = env.game_engine.get_legal_actions(active)
    
    # Take a random action (in real code, your agent would choose here)
    action_idx = 0
    
    obs, reward, terminated, truncated, info = env.step(action_idx)
    done = terminated or truncated
    step += 1

# Check who won
print(f"Game ended after {step} steps")
print(f"Winner: Player {env.game_engine.state.winner}")
```

## Understanding the Game Engine

### Core Concepts

The engine models a two-player Flesh and Blood game:
- **Player 0**: You (the RL agent) - plays as Kano (Young), a Wizard hero with 15 life
- **Player 1**: The opponent - plays as a Generic hero with 20 life

### Game Phases

Each turn has phases:
1. **Start Phase**: Draw cards up to intellect (Kano draws to 4)
2. **Action Phase**: Main gameplay - play action cards, attack. Costs are paid by auto-pitching from hand.
3. **End Phase**: Arsenal a card, pitch zone returns to deck, turn passes

### Pitching (Rule 1.14.3b)

Per official Flesh and Blood rules, a player may only pitch a card if it gains them resources to pay for something. The engine implements this as **automatic pitch** - when you attempt to play a card with a cost you can't afford, the game automatically pitches cards from your hand until you can pay. You cannot pitch cards arbitrarily.

### Combat Chain

When you play an attack card, the combat chain opens:
1. **Layer Step**: Attack is placed on the stack
2. **Attack Step**: Attack becomes attacking
3. **Defend Step**: Opponent declares defenders (blocking cards)
4. **Reaction Step**: Reactions can be played
5. **Damage Step**: Damage is calculated (attack power - defense)
6. **Resolution Step**: Go again grants additional action points
7. **Close Step**: Combat chain closes, cards go to graveyard

### Key Classes

```python
from fab_engine.cards.model import CardTemplate, CardInstance, HeroState
from fab_engine.engine.game import GameEngine, GameState, GamePhase
from fab_engine.engine.combat import CombatChain, CombatStep
from fab_engine.engine.actions import Action, ActionType, ActionResult
from fab_engine.zones.player_zones import PlayerZones
```

## The Gymnasium Environment

The `FaBEnv` class implements the Gymnasium interface for RL training.

### Observation Space

The observation is a dictionary with these keys:

```python
{
    "player_life": float,          # Your current life (0-40)
    "player_resources": float,     # Your resource points (0-20)
    "player_action_points": float, # Your action points (0-3)
    "player_hand_size": int,       # Cards in your hand
    "player_deck_size": int,       # Cards in your deck
    "player_pitch_size": int,      # Cards in your pitch zone
    "opponent_life": float,        # Opponent's life
    "opponent_hand_size": int,     # Opponent's hand size (hidden but tracked)
    "opponent_deck_size": int,     # Opponent's deck size
    "phase": float,                # Current game phase
    "turn_number": int,            # Current turn
    "combat_open": float,          # Is combat chain open? (0 or 1)
    "hand_cards": np.array,        # Your hand (11 cards x 8 features)
    "top_of_deck": np.array,       # Top card of your deck (8 features)
}
```

### Card Features

Each card is encoded with 8 features:
- Cost (or 0 if no cost)
- Power (or 0 if no power)
- Defense (or 0 if no defense)
- Arcane damage (or 0)
- Pitch value (or 0)
- Is attack action? (0/1)
- Is instant? (0/1)
- Has go again? (0/1)

### Action Space

The environment has 100 discrete actions. The actual available actions depend on game state:

```python
# What actions can the active player take?
active = env.game_engine.state.active_player_id
actions = env.game_engine.get_legal_actions(active)

# Action types include:
# - PLAY_CARD_FROM_HAND: Play an action card (auto-pitches to cover cost if needed)
# - DECLARE_DEFENDERS: Declare blocking cards during combat
# - END_PHASE: End your turn
# - ACTIVATE_HERO_ABILITY: Use hero ability (Kano's ability costs 3 resources)
```

### Reward Signal

- **+100**: You win the game
- **-100**: You lose the game
- **+0.1**: Successful action
- **-1.0**: Invalid action

## Training an Agent

### Basic Training Loop

```python
import torch
from fab_engine.gym_env.env import FaBEnv
from fab_engine.agents.policy import FABPolicy, FABValue

# Create environment
env = FaBEnv()

# Create policy and value networks
policy = FABPolicy(obs_dim=108, action_dim=100)
value_network = FABValue(obs_dim=108)

optimizer = torch.optim.Adam(list(policy.parameters()) + list(value_network.parameters()), lr=3e-4)

# Training loop
num_episodes = 1000
gamma = 0.99

for episode in range(num_episodes):
    obs, info = env.reset()
    done = False
    episode_reward = 0
    
    while not done:
        # Get action from policy
        obs_tensor = {k: torch.tensor(v) for k, v in obs.items()}
        with torch.no_grad():
            logits = policy(obs_tensor)
            probs = torch.softmax(logits, dim=-1)
            action = torch.multinomial(probs, 1).item()
        
        # Take step
        obs, reward, terminated, truncated, info = env.step(action)
        done = terminated or truncated
        episode_reward += reward
    
    if episode % 100 == 0:
        print(f"Episode {episode}: reward = {episode_reward:.2f}")

# Save trained policy
torch.save(policy.state_dict(), "trained_policy.pt")
```

### Using a Trained Policy

```python
import torch
from fab_engine.agents.policy import FABPolicy
from fab_engine.gym_env.env import FaBEnv

# Load trained policy
policy = FABPolicy()
policy.load_state_dict(torch.load("trained_policy.pt"))
policy.eval()

# Run evaluation
env = FaBEnv()
wins = 0
num_games = 100

for _ in range(num_games):
    obs, info = env.reset()
    done = False
    
    while not done:
        obs_tensor = {k: torch.tensor(v) for k, v in obs.items()}
        with torch.no_grad():
            logits = policy(obs_tensor)
            action = torch.argmax(torch.softmax(logits, dim=-1)).item()
        
        obs, reward, terminated, truncated, info = env.step(action)
        done = terminated or truncated
    
    if env.game_engine.state.winner == 0:
        wins += 1

print(f"Win rate: {wins/num_games:.1%}")
```

## Evaluating a Deck

### Manual Game Play

```python
from fab_engine.gym_env.env import FaBEnv

env = FaBEnv()
obs, info = env.reset()

# Inspect game state
state = env.game_engine.state
print(f"Your life: {state.players[0].hero.life_total}")
print(f"Opponent life: {state.players[1].hero.life_total}")
print(f"Your resources: {state.players[0].hero.resource_points}")
print(f"Your hand: {[c.name for c in state.players[0].zones.hand.cards]}")

# Get available actions
actions = env.game_engine.get_legal_actions(0)
for i, action in enumerate(actions):
    if action.card_instance_id > 0:
        card = state.players[0].zones.hand.get_by_id(action.card_instance_id)
        print(f"{i}: {action.action_type.name} - {card.name}")
    else:
        print(f"{i}: {action.action_type.name}")
```

### Watching a Game

```python
from fab_engine.gym_env.env import FaBEnv
import random

def play_game_with_strategy(env):
    """Simple greedy strategy for demonstration."""
    obs, info = env.reset()
    done = False
    
    while not done:
        active = env.game_engine.state.active_player_id
        state = env.game_engine.state
        player = state.players[active]
        
        # Get legal actions
        actions = env.game_engine.get_legal_actions(active)
        if not actions:
            break
        
        # Greedy strategy:
        # 1. If defending, declare defenders
        # 2. If no resources, pitch
        # 3. Otherwise, play attack if possible
        # 4. End phase as last resort
        
        action_idx = 0
        
        if state.combat_step.name == 'DEFEND':
            # Must defend
            action_idx = 0
        elif player.hero.resource_points == 0:
            # Pitch for resources
            for i, a in enumerate(actions):
                if a.action_type.name == 'PITCH_CARD':
                    action_idx = i
                    break
        else:
            # Play attack
            for i, a in enumerate(actions):
                if a.action_type.name == 'PLAY_CARD_FROM_HAND':
                    card = player.zones.hand.get_by_id(a.card_instance_id)
                    if card and card.template.is_attack_action:
                        action_idx = i
                        break
            else:
                # Pitch or end phase
                for i, a in enumerate(actions):
                    if a.action_type.name == 'PITCH_CARD':
                        action_idx = i
                        break
                else:
                    action_idx = len(actions) - 1
        
        obs, reward, terminated, truncated, info = env.step(action_idx)
        done = terminated or truncated
    
    return state.winner

# Run a game
env = FaBEnv()
winner = play_game_with_strategy(env)
print(f"Winner: Player {winner}")
```

## Customizing the Game

### Loading Specific Cards

```python
from fab_engine.cards.loader import CardLoader

loader = CardLoader()

# Get specific heroes
kano_young = loader.get_kano_young()
kano_adult = loader.get_kano_adult()
generic_hero = loader.get_generic_hero()

# Get card pools
kano_cards = loader.kano_cards  # All Kano-eligible cards
generic_cards = loader.generic_cards  # All Generic cards

# Filter cards
arcane_spells = [c for c in kano_cards if c.has_arcane and c.arcane > 0]
attack_cards = [c for c in kano_cards if c.is_attack_action]
```

### Creating Custom Decks

```python
from fab_engine.cards.model import CardInstance

# Create a deck from specific cards
deck = []
for template in my_card_list:
    deck.append(CardInstance(template=template))

# Shuffle
import random
random.shuffle(deck)

# Create game with custom decks
from fab_engine.engine.game import create_game

engine = create_game(
    player_0_hero=kano_young,
    player_0_deck=deck,
    player_1_hero=generic_hero,
    player_1_deck=opponent_deck,
)
```

### Understanding Card Properties

```python
from fab_engine.cards.model import CardTemplate, CardType, Subtype, Keyword

# Check card properties
card = kano_cards[0]

# Basic properties
card.name           # Card name
card.cost           # Resource cost to play
card.power          # Attack power
card.defense        # Defense value
card.arcane         # Arcane damage
card.pitch          # Pitch value (resources you get)

# Types
card.is_attack_action    # Is an attack action?
card.is_non_attack_action  # Is a non-attack action (arcane spell)?
card.is_instant          # Is an instant?

# Keywords
card.has_keyword(Keyword.GO_AGAIN)
card.has_keyword(Keyword.DOMINATE)
card.has_keyword(Keyword.OVERPOWER)
arcane_barrier = card.get_keyword_param(Keyword.ARCANE_BARRIER)
```

## Common Patterns

### Implementing a Custom Agent

```python
class MyAgent:
    def __init__(self):
        pass
    
    def get_action(self, obs, legal_actions, game_state):
        """Choose an action based on observation."""
        
        # Example: Simple rule-based agent
        player = game_state.players[0]
        
        # Always pitch if no resources
        if player.hero.resource_points == 0:
            for i, action in enumerate(legal_actions):
                if action.action_type.name == 'PITCH_CARD':
                    return i
        
        # Play highest power attack if we can afford it
        best_power = -1
        best_idx = len(legal_actions) - 1  # Default to last action (usually END_PHASE)
        
        for i, action in enumerate(legal_actions):
            if action.action_type.name == 'PLAY_CARD_FROM_HAND':
                card = player.zones.hand.get_by_id(action.card_instance_id)
                if card and card.template.power > best_power:
                    best_power = card.template.power
                    best_idx = i
        
        return best_idx

# Use the agent
agent = MyAgent()
obs, info = env.reset()
done = False

while not done:
    active = env.game_engine.state.active_player_id
    actions = env.game_engine.get_legal_actions(active)
    
    if active == 0:  # Your turn
        action_idx = agent.get_action(obs, actions, env.game_engine.state)
    else:
        # Let opponent play
        action_idx = 0
    
    obs, reward, terminated, truncated, info = env.step(action_idx)
    done = terminated or truncated
```

## Troubleshooting

### "No actions available"

This can happen if:
- It's not your turn (check `active_player_id`)
- You're in a combat step that requires specific actions
- The game is over

### "Invalid action" penalty

This means your action index was out of bounds or the action wasn't in the legal actions list. Always validate against `get_legal_actions()`.

### Games never ending

Check that:
1. The deck has cards (deck size > 0)
2. You're properly handling the DEFEND combat step
3. Turn switching is working (check `turn_player_id`)

## Next Steps

- Implement more sophisticated RL algorithms (PPO, A2C)
- Add more card abilities (equipment effects, on-hit triggers)
- Build deck optimization using the evaluation framework
- Add proper action masking for invalid actions
