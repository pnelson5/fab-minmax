# Fastest to 40 - Kano Deck Optimizer

RL-based optimizer for finding the fastest Flesh and Blood Kano deck to deal 40 damage using Gymnasium environments.

## Prerequisites

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) package manager
- Card database at `~/repos/github/flesh-and-blood-cards/json/english/card.json`

## Quick Start

```bash
# Install dependencies (first time only)
uv pip install -e .

# Run a full game with the gymnasium environment (using heuristic agents)
uv run python -c "
from fab_engine.gym_env.env import FaBEnv
from fab_engine.agents.heuristic import HeuristicAgent

env = FaBEnv()
kano = HeuristicAgent(player_id=0)
opponent = HeuristicAgent(player_id=1)

obs, info = env.reset()
print('Game started - Player (Kano): 15 life, Opponent: 20 life')

steps = 0
max_steps = 200

while steps < max_steps:
    state = env.game_engine.state
    
    if state.game_over:
        print(f'Game ended in {steps} steps')
        print(f'Winner: {\"Kano\" if state.winner == 0 else \"Opponent\"}')
        p0 = state.players[0]
        p1 = state.players[1]
        print(f'Final: Kano={p0.hero.life_total} life, Opp={p1.hero.life_total} life')
        break
    
    if state.active_player_id == 0:
        action = kano.select_action(env.game_engine)
    else:
        action = opponent.select_action(env.game_engine)
    
    if action is None:
        break
    
    env.game_engine.execute_action(action)
    steps += 1
    
    if steps % 20 == 0:
        p0 = state.players[0]
        p1 = state.players[1]
        print(f'Step {steps}: Kano={p0.hero.life_total} life, {p0.hero.resource_points} res, Opp={p1.hero.life_total} life')
else:
    print('Game reached max steps (truncated)')
"
```

## Running Tests

```bash
# Run all tests
uv run pytest tests/ -v

# Run specific test file
uv run pytest tests/test_engine.py -v
```

## Project Structure

- `fab_engine/` - Two-player FaB game engine
  - `cards/` - Card model and loader
  - `zones/` - Zone system (deck, hand, pitch, etc.)
  - `engine/` - Game engine, combat, effects
  - `gym_env/` - Gymnasium environment
  - `agents/` - Heuristic opponent, RL training

- `fastest_to_40.py` - Original solitaire Kano deck optimizer

## Current Status

**Completed Phases:**
- Phase 1: Data loading & card analysis
- Phase 2: Game engine implementation  
- Phase 3: PufferLib RL environment

**Next:**
- Phase 4: RL training setup
- Phase 5: Deck optimization
- Phase 6: Results & analysis

## Output

The script currently:
1. Loads and filters 662 Kano-eligible cards
2. Tests the game engine with a sample deck
3. Validates the PufferLib environment with random policy

Expected runtime: ~10-15 seconds

## FAB Rules Search

The project includes a searchable version of the Flesh and Blood Comprehensive Ruleset using [qmd](https://github.com/tobi/qmd).

### Setup

```bash
# The rules are already converted to markdown and indexed
# qmd is required (install via npm: npm install -g @tobilu/qmd)

# To index the rules (already done):
qmd collection add fab-rules fab-rules
qmd embed fab-rules
```

### Usage

#### Using the wrapper script (recommended):

```bash
# Basic search
python fab_search.py "restriction takes precedence"

# Search with more results
python fab_search.py "attack target" -n 10

# Semantic query search (slower but more accurate for natural language)
python fab_search.py "how does blocking work" --query

# Or make it executable and run directly
chmod +x fab_search.py
./fab_search.py "instant card rules"
```

#### Using qmd directly:

```bash
# Search for specific rules
qmd search "restriction precedence" -c fab-rules
qmd search "attack target" -c fab-rules -n 5
qmd search "combat chain" -c fab-rules -n 5

# Get results with more context
qmd query "how does blocking work" -c fab-rules -n 3

# Get a specific section by rule number
qmd get fab-rules/en-fab-cr.md:15 -l 5
```

### Search Tips

- **Rule numbers**: Search by rule number like "1.0.2" or "8.1.6a" (use the wrapper script for this)
- **Keywords**: Use terms like "attack", "block", "instant", "priority", "combat chain"
- **Natural language**: Use the `--query` flag for complex questions like "how does blocking work"
- **Exact phrases**: Put quotes around phrases like "attack target"

The rules are stored in `fab-rules/en-fab-cr.md` and converted from the original `en-fab-cr.txt` using the `convert_to_md.py` script.
