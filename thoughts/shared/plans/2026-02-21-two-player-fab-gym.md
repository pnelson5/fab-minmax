# Two-Player Flesh and Blood Gymnasium Environment - Implementation Plan

## Overview

Build a high-fidelity two-player Flesh and Blood Gymnasium environment as a Python package (`fab_engine`), modeling Kano (Young, 15 life) vs a Generic attacker opponent. The environment implements the full combat chain, zone system, keyword abilities, and Kano's hero ability from the FaB Comprehensive Rules. The primary goal is **deck optimization** for Kano through RL training against a simple greedy heuristic opponent. Cards are loaded from the real FaB card database (Common/Rare only).

## Current State Analysis

**What exists (`fastest_to_40.py`):**
- Solitaire Kano deck optimizer - no opponent, no defending, no combat
- Simplified Card model: just name, pitch, cost, damage (power+arcane merged), color
- No zones (deck, hand, pitch zone only), no arsenal, no graveyard, no equipment
- No combat chain, no action points, no go again
- Gymnasium env with flat 19-feature observation, Discrete(9) action space
- PPO-style policy gradient RL training + deck candidate generation/evaluation
- Loads cards from `~/repos/github/flesh-and-blood-cards/json/english/card.json`

**What the real game requires (from `en-fab-cr.txt`):**
- Two players with heroes, life totals, equipment, weapons (CR 1.1, 2.5)
- Turn structure: Start Phase → Action Phase → End Phase (CR 4.0-4.4)
- Priority system: turn-player gets priority, pass back and forth (CR 1.11)
- Combat chain with steps: Layer → Attack → Defend → Reaction → Damage → Resolution → Close (CR 7.0-7.7)
- Physical damage: power vs sum of defense values (CR 7.5.2)
- Arcane damage: effect-based, bypasses combat, uses Arcane Barrier to block (CR 8.5.3b, 8.3.8)
- Resources from pitching cards (CR 1.14.3), action points (CR 1.13.2), go again (CR 8.3.5)
- Zones: deck, hand, pitch, graveyard, arsenal, banished, equipment (head/chest/arms/legs), weapons, combat chain, stack, permanent (CR 3.0-3.15)
- Equipment defending with battleworn/blade break (CR 8.1.4b, 8.3.2, 8.3.3)
- Kano hero ability: Instant - {r}{r}{r}: Look at top card, if non-attack action, may banish and play as instant

### Key Discoveries:
- Kano (Young) has 15 life, intellect 4 (CR data: `health=15`, `intelligence=4`)
- Kano, Dracai of Aether (Adult) has 30 life, intellect 4
- Kano's weapons are staves that deal arcane damage through effects, not power (e.g., Aether Conduit: "Deal 2 arcane damage")
- Wizard equipment: Robe of Rapture (Arcane Barrier 1, destroy for 3 resources), Hold Focus (Amp 1), Storm Striders, Metacarpus Node, etc.
- Generic equipment with Arcane Barrier: Nullrune set (Hood/Robe/Gloves/Boots, each AB1)
- Opponent can use Generic attack action cards loaded from the real card DB
- Cards have: `name`, `types[]`, `color`, `pitch`, `cost`, `power`, `defense`, `arcane`, `health`, `intelligence`, `functional_text_plain`, `card_keywords[]`, `ability_and_effect_keywords[]`, `abilities_and_effects[]`

## Desired End State

A Python package (`fab_engine/`) with:
1. A high-fidelity FaB game engine implementing CR rules for a Kano vs Generic 2-player game
2. A Gymnasium environment with Dict observation space and micro-action space
3. A simple greedy heuristic opponent
4. RL training infrastructure for deck optimization
5. Ability to load real cards, generate/evaluate deck candidates, and output optimal deck lists

### Verification:
- Run the game engine standalone and play a full game to completion
- Run the Gymnasium env with random actions and verify it terminates correctly
- Train an RL agent and observe improving win rates
- Generate and evaluate deck candidates, producing an optimal deck file

## What We're NOT Doing

- **Multi-hero support**: Only Kano (agent) vs Generic hero (opponent). No framework for arbitrary hero abilities.
- **Niche CR rules**: Sub-cards (CR 3.0.14), multi-target attacks, party mechanics, macros, companions, hybrid cards, metatypes
- **Token creation**: No Runechant tokens, Ponder tokens, or other token mechanics (would require tracking token permanents)
- **Aura/Item permanents**: Cards that enter the arena as permanents (too complex for V1)
- **Combo label abilities**: No Combo, Reprise, Crush, Channel, Rupture, etc. These are complex conditional triggered effects
- **Stack interactions**: Simplified stack - no counter-spells, no layered triggers. Effects resolve immediately.
- **Self-play RL**: Opponent is heuristic-only in this version
- **Card text parsing/NLP**: Card abilities will be manually mapped to engine effects for relevant cards, not parsed from `functional_text_plain`
- **Full replacement effect system**: No replacement effects (CR 6.4). Damage prevention (Arcane Barrier, equipment) handled as special cases.
- **Pitch zone ordering strategy**: Cards go to bottom of deck in a simple order (not optimized by agent)

## Implementation Approach

Reorganize the project into a Python package with separate modules for cards, zones, game engine, combat, abilities, gym environment, and RL training. The game engine follows the CR structure closely: turns have phases, combat has steps, the combat chain tracks chain links with attacking/defending cards. Card abilities are implemented as a registry of effect functions keyed by card name or keyword, not parsed from text.

The Gymnasium environment uses a Dict observation space (hand cards, opponent visible state, game phase, resources, life totals, etc.) and a micro-action space where the agent takes one action per step (pitch, play, defend, activate ability, end phase). Actions are validated against game state - invalid actions receive a penalty.

---

## Phase 1: Package Structure & Card Model

### Overview
Reorganize the project into a proper Python package and build a rich card model that captures all FaB card properties needed for a 2-player game.

### Changes Required:

#### 1. Package Directory Structure
**Create directories:**
```
fab_engine/
  __init__.py
  cards/
    __init__.py
    model.py          # Card, Hero, Equipment dataclasses
    loader.py         # Load from JSON DB, filter by hero eligibility
    abilities.py      # Ability registry: keyword → effect function
  zones/
    __init__.py
    zone.py           # Zone base class and all zone types
    player_zones.py   # PlayerZones container (all zones for one player)
  engine/
    __init__.py
    game.py           # GameEngine: turn structure, priority, win conditions
    combat.py         # CombatChain: all combat steps (Layer→Close)
    actions.py        # Action validation and execution
    effects.py        # Effect system: damage, draw, gain resources, etc.
  gym_env/
    __init__.py
    env.py            # FaBEnv: Gymnasium environment
    observation.py    # Observation encoding
    action_space.py   # Action space definition and decoding
  agents/
    __init__.py
    heuristic.py      # Greedy heuristic opponent
    policy.py         # RL policy network
    training.py       # Training loop and deck optimization
```

#### 2. Card Model (`fab_engine/cards/model.py`)

```python
from dataclasses import dataclass, field
from typing import List, Optional, Set
from enum import Enum, auto

class CardType(Enum):
    ACTION = auto()
    ATTACK_REACTION = auto()
    DEFENSE_REACTION = auto()
    INSTANT = auto()
    EQUIPMENT = auto()
    WEAPON = auto()
    HERO = auto()
    # ... others as needed

class Supertype(Enum):
    WIZARD = auto()
    GENERIC = auto()
    GUARDIAN = auto()
    WARRIOR = auto()
    NINJA = auto()
    BRUTE = auto()
    # ... others for opponent cards

class Subtype(Enum):
    ATTACK = auto()
    ARMS = auto()
    CHEST = auto()
    HEAD = auto()
    LEGS = auto()
    SWORD = auto()
    STAFF = auto()
    ORB = auto()
    ONE_HAND = auto()
    TWO_HAND = auto()
    OFF_HAND = auto()
    AURA = auto()
    ITEM = auto()
    # ... others

class Color(Enum):
    RED = auto()
    YELLOW = auto()
    BLUE = auto()
    COLORLESS = auto()

class Keyword(Enum):
    GO_AGAIN = auto()
    DOMINATE = auto()
    ARCANE_BARRIER = auto()  # parameterized: AB N
    BATTLEWORN = auto()
    BLADE_BREAK = auto()
    TEMPER = auto()
    PHANTASM = auto()
    OVERPOWER = auto()
    PIERCING = auto()  # parameterized: Piercing N
    SPELLVOID = auto()  # parameterized: Spellvoid N
    QUELL = auto()  # parameterized: Quell N
    WARD = auto()  # parameterized: Ward N
    GUARDWELL = auto()
    # ... others relevant to Kano matchup

@dataclass(frozen=True)
class CardTemplate:
    """Immutable card definition loaded from the database.
    
    A CardTemplate represents a unique card by (name, pitch) pair.
    CardInstance objects reference a template and track mutable state.
    """
    unique_id: str           # From DB
    name: str
    types: frozenset         # Set of CardType
    supertypes: frozenset    # Set of Supertype
    subtypes: frozenset      # Set of Subtype
    color: Color
    pitch: int               # 0-3 (0 = no pitch property)
    has_pitch: bool          # Whether card has the pitch property at all
    cost: int                # Resource cost to play (-1 = no cost property)
    has_cost: bool
    power: int               # Physical power (-1 = no power property)
    has_power: bool
    defense: int             # Defense value (-1 = no defense property)
    has_defense: bool
    arcane: int              # Arcane damage value (0 = none)
    has_arcane: bool
    life: int                # For heroes
    intellect: int           # For heroes
    keywords: dict           # Keyword -> parameter (e.g., {ARCANE_BARRIER: 1})
    functional_text: str     # Raw text for reference
    is_attack_action: bool   # Convenience: has Action + Attack subtypes
    is_non_attack_action: bool  # Has Action but not Attack
    is_instant: bool
    is_defense_reaction: bool
    is_attack_reaction: bool
    is_equipment: bool
    is_weapon: bool
    is_hero: bool


@dataclass
class CardInstance:
    """A mutable instance of a card in the game.
    
    Tracks zone, position, counters, and temporary modifications.
    References an immutable CardTemplate for base properties.
    """
    template: CardTemplate
    instance_id: int          # Unique per-game ID
    
    # Mutable state
    defense_counters: int = 0  # -1{d} counters from battleworn/temper
    power_counters: int = 0
    is_face_up: bool = True
    is_tapped: bool = False
    
    # Temporary modifications (cleared on zone change)
    temp_power_mod: int = 0
    temp_defense_mod: int = 0
    temp_keywords: dict = field(default_factory=dict)
    
    @property
    def name(self) -> str:
        return self.template.name
    
    @property
    def effective_defense(self) -> int:
        """Current defense value including counters and temp mods."""
        base = self.template.defense
        if base < 0:
            return -1  # No defense property
        return max(0, base + self.defense_counters + self.temp_defense_mod)
    
    @property 
    def effective_power(self) -> int:
        """Current power value including counters and temp mods."""
        base = self.template.power
        if base < 0:
            return -1
        return max(0, base + self.power_counters + self.temp_power_mod)
    
    def has_keyword(self, kw: Keyword) -> bool:
        """Check if card currently has a keyword."""
        return kw in self.template.keywords or kw in self.temp_keywords
    
    def get_keyword_param(self, kw: Keyword) -> int:
        """Get parameter value for a parameterized keyword."""
        if kw in self.temp_keywords:
            return self.temp_keywords[kw]
        return self.template.keywords.get(kw, 0)
    
    def reset_temp_mods(self):
        """Clear temporary modifications (on zone change)."""
        self.temp_power_mod = 0
        self.temp_defense_mod = 0
        self.temp_keywords.clear()
```

#### 3. Hero Model
```python
@dataclass
class HeroState:
    """Mutable state for a hero in the game."""
    template: CardTemplate      # Hero card template
    life_total: int             # Current life (starts at template.life)
    action_points: int = 0
    resource_points: int = 0
    has_used_hero_ability: bool = False  # Per-turn tracking
    
    @property
    def intellect(self) -> int:
        return self.template.intellect
    
    @property
    def is_alive(self) -> bool:
        return self.life_total > 0
```

### Success Criteria:

#### Automated Verification:
- [x] `pip install -e .` installs the package without errors
- [x] `from fab_engine.cards.model import CardTemplate, CardInstance` imports successfully
- [x] Can create CardTemplate and CardInstance objects with all fields
- [x] `effective_defense` and `effective_power` correctly apply counters
- [x] Keyword checking works for base and temporary keywords
- [x] `python -c "import fab_engine; print('ok')"` succeeds

#### Manual Verification:
- [x] Review the data model and confirm it captures all needed card properties
- [x] Verify enum values cover all relevant types/subtypes/keywords for Kano matchup

**Implementation Note**: After completing this phase and all automated verification passes, pause here for manual confirmation before proceeding to the next phase.

---

## Phase 2: Zone System

### Overview
Implement the zone system per CR 3.0. Each player has their own zones (deck, hand, pitch, graveyard, arsenal, banished, equipment slots, weapon slots). The combat chain, stack, and permanent zones are shared.

### Changes Required:

#### 1. Zone Base Class (`fab_engine/zones/zone.py`)

```python
from enum import Enum, auto
from typing import List, Optional
from fab_engine.cards.model import CardInstance

class ZoneType(Enum):
    DECK = auto()       # Private zone (CR 3.0.4b)
    HAND = auto()       # Private zone
    ARSENAL = auto()    # Private zone
    PITCH = auto()      # Public zone
    GRAVEYARD = auto()  # Public zone
    BANISHED = auto()   # Public zone
    HEAD = auto()       # Public equipment zone
    CHEST = auto()      # Public equipment zone
    ARMS = auto()       # Public equipment zone
    LEGS = auto()       # Public equipment zone
    WEAPON_1 = auto()   # Public weapon zone
    WEAPON_2 = auto()   # Public weapon zone
    COMBAT_CHAIN = auto()  # Shared public zone
    STACK = auto()         # Shared public zone
    HERO = auto()          # Public zone

class Zone:
    """A zone that holds CardInstance objects.
    
    Per CR 3.0: zones are public or private, and objects track visibility.
    For our game engine, we simplify: zones have a type and a list of cards.
    """
    
    def __init__(self, zone_type: ZoneType, owner_id: int, max_size: int = -1):
        self.zone_type = zone_type
        self.owner_id = owner_id  # Player ID, or -1 for shared zones
        self.max_size = max_size  # -1 = unlimited
        self._cards: List[CardInstance] = []
    
    @property
    def cards(self) -> List[CardInstance]:
        return self._cards
    
    @property
    def is_empty(self) -> bool:
        return len(self._cards) == 0
    
    @property
    def size(self) -> int:
        return len(self._cards)
    
    def add(self, card: CardInstance, position: str = "top") -> bool:
        """Add a card to this zone. Position: 'top', 'bottom', or index."""
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
    
    def remove(self, card: CardInstance) -> bool:
        """Remove a specific card from this zone."""
        if card in self._cards:
            self._cards.remove(card)
            return True
        return False
    
    def remove_at(self, index: int) -> Optional[CardInstance]:
        """Remove and return card at index."""
        if 0 <= index < len(self._cards):
            return self._cards.pop(index)
        return None
    
    def peek_top(self) -> Optional[CardInstance]:
        """Look at the top card without removing it."""
        return self._cards[0] if self._cards else None
    
    def draw_top(self) -> Optional[CardInstance]:
        """Remove and return the top card."""
        return self._cards.pop(0) if self._cards else None
    
    def shuffle(self):
        """Shuffle the cards in this zone (typically deck only)."""
        import random
        random.shuffle(self._cards)
    
    def contains(self, card: CardInstance) -> bool:
        return card in self._cards
    
    def get_by_id(self, instance_id: int) -> Optional[CardInstance]:
        for c in self._cards:
            if c.instance_id == instance_id:
                return c
        return None
```

#### 2. Player Zones Container (`fab_engine/zones/player_zones.py`)

```python
class PlayerZones:
    """All zones owned by a single player.
    
    Per CR 3.0.2: each player has deck, hand, pitch, graveyard, arsenal,
    banished, head, chest, arms, legs, hero zones, and two weapon zones.
    """
    
    def __init__(self, player_id: int):
        self.player_id = player_id
        self.hero = Zone(ZoneType.HERO, player_id, max_size=1)
        self.deck = Zone(ZoneType.DECK, player_id)
        self.hand = Zone(ZoneType.HAND, player_id)
        self.pitch = Zone(ZoneType.PITCH, player_id)
        self.graveyard = Zone(ZoneType.GRAVEYARD, player_id)
        self.arsenal = Zone(ZoneType.ARSENAL, player_id, max_size=1)
        self.banished = Zone(ZoneType.BANISHED, player_id)
        self.head = Zone(ZoneType.HEAD, player_id, max_size=1)
        self.chest = Zone(ZoneType.CHEST, player_id, max_size=1)
        self.arms = Zone(ZoneType.ARMS, player_id, max_size=1)
        self.legs = Zone(ZoneType.LEGS, player_id, max_size=1)
        self.weapon_1 = Zone(ZoneType.WEAPON_1, player_id, max_size=1)
        self.weapon_2 = Zone(ZoneType.WEAPON_2, player_id, max_size=1)
    
    @property
    def equipment_zones(self) -> list:
        """All equipment zones (head, chest, arms, legs)."""
        return [self.head, self.chest, self.arms, self.legs]
    
    @property
    def weapon_zones(self) -> list:
        return [self.weapon_1, self.weapon_2]
    
    @property
    def all_equipment(self) -> list:
        """All equipped equipment cards."""
        cards = []
        for zone in self.equipment_zones:
            cards.extend(zone.cards)
        return cards
    
    @property
    def all_weapons(self) -> list:
        """All equipped weapon cards."""
        cards = []
        for zone in self.weapon_zones:
            cards.extend(zone.cards)
        return cards
    
    def get_equipment_zone_for_card(self, card: CardInstance) -> Optional[Zone]:
        """Determine which equipment zone a card should be equipped to."""
        subtypes = card.template.subtypes
        if Subtype.HEAD in subtypes:
            return self.head
        elif Subtype.CHEST in subtypes:
            return self.chest
        elif Subtype.ARMS in subtypes:
            return self.arms
        elif Subtype.LEGS in subtypes:
            return self.legs
        return None
```

### Success Criteria:

#### Automated Verification:
- [x] Zone creation works for all zone types
- [x] `add()`, `remove()`, `draw_top()`, `peek_top()` work correctly
- [x] Max size enforcement works (arsenal=1, equipment=1)
- [x] PlayerZones creates all required zones
- [x] `get_equipment_zone_for_card()` correctly routes equipment to slots

#### Manual Verification:
- [x] Verify zone types cover all zones referenced in the game engine design

**Implementation Note**: After completing this phase and all automated verification passes, pause here for manual confirmation before proceeding.

---

## Phase 3: Game Engine Core

### Overview
Implement the turn structure (Start/Action/End phases per CR 4.0-4.4), priority system, action points, resource management, pitching, card playing, and arsenal mechanics. This is the backbone that combat and abilities build on.

### Changes Required:

#### 1. Game State (`fab_engine/engine/game.py`)

```python
from enum import Enum, auto

class GamePhase(Enum):
    NOT_STARTED = auto()
    START_OF_GAME = auto()
    START_PHASE = auto()
    ACTION_PHASE = auto()     # Main phase where players take actions
    END_PHASE = auto()
    GAME_OVER = auto()

class CombatStep(Enum):
    """Steps within combat (CR 7.0-7.7)"""
    NONE = auto()           # Not in combat
    LAYER = auto()          # 7.1: Attack on stack, waiting to resolve
    ATTACK = auto()         # 7.2: Attack resolves, becomes attacking
    DEFEND = auto()         # 7.3: Defending hero declares defenders
    REACTION = auto()       # 7.4: Attack/defense reactions
    DAMAGE = auto()         # 7.5: Calculate and apply damage
    RESOLUTION = auto()     # 7.6: Chain link resolves, go again check
    CLOSE = auto()          # 7.7: Combat chain closes

class PlayerState:
    """Complete state for one player."""
    def __init__(self, player_id: int, hero: HeroState, zones: PlayerZones):
        self.player_id = player_id
        self.hero = hero
        self.zones = zones
        self.cards_played_this_turn: List[CardInstance] = []
        self.attacks_this_turn: int = 0
        self.has_defended_with_hand_card: bool = False  # For dominate tracking
        self.damage_dealt_this_turn: int = 0
        self.arcane_damage_dealt_this_turn: int = 0

class GameState:
    """Complete game state for a 2-player FaB game."""
    
    def __init__(self, player_0: PlayerState, player_1: PlayerState):
        self.players = [player_0, player_1]
        self.turn_player_id: int = 0      # Who has the current turn
        self.active_player_id: int = 0    # Who has priority
        self.phase: GamePhase = GamePhase.NOT_STARTED
        self.combat_step: CombatStep = CombatStep.NONE
        self.combat_chain: CombatChain = CombatChain()
        self.turn_number: int = 0
        self.winner: Optional[int] = None  # Player ID of winner, or None
        self.game_over: bool = False
    
    @property
    def turn_player(self) -> PlayerState:
        return self.players[self.turn_player_id]
    
    @property
    def non_turn_player(self) -> PlayerState:
        return self.players[1 - self.turn_player_id]
    
    @property
    def active_player(self) -> PlayerState:
        return self.players[self.active_player_id]
```

#### 2. Game Engine (`fab_engine/engine/game.py`)

The engine manages the game loop. Key methods:

```python
class GameEngine:
    """Main game engine implementing CR turn structure."""
    
    def __init__(self, state: GameState):
        self.state = state
        self.event_log: List[dict] = []  # For debugging/observation
    
    # ========================
    # START-OF-GAME (CR 4.1)
    # ========================
    def setup_game(self, first_turn_player: int = 0):
        """Execute start-of-game procedure per CR 4.1."""
        self.state.phase = GamePhase.START_OF_GAME
        self.state.turn_player_id = first_turn_player
        
        # CR 4.1.2: Hero cards already placed
        # CR 4.1.4: Equipment already selected and equipped
        # CR 4.1.5: Deck cards selected
        # CR 4.1.7: Decks shuffled
        for player in self.state.players:
            player.zones.deck.shuffle()
        
        # CR 4.1.8: Equipment equipped (already done during setup)
        
        # CR 4.1.9: Draw cards up to intellect
        for player in self.state.players:
            self._draw_up_to_intellect(player)
        
        # Start first turn
        self.state.turn_number = 1
        self._start_phase()
    
    # ========================
    # START PHASE (CR 4.2)
    # ========================
    def _start_phase(self):
        """CR 4.2: Start phase - no priority, triggers resolve."""
        self.state.phase = GamePhase.START_PHASE
        # CR 4.2.2: "start of turn" effects trigger
        # (Simplified: no triggered effects in V1 beyond equipment decay)
        self._handle_start_of_turn_effects()
        # CR 4.2.3: Proceed to action phase
        self._begin_action_phase()
    
    # ========================
    # ACTION PHASE (CR 4.3)
    # ========================
    def _begin_action_phase(self):
        """CR 4.3: Action phase begins."""
        self.state.phase = GamePhase.ACTION_PHASE
        self.state.combat_step = CombatStep.NONE
        
        # CR 4.3.2: Turn player gets 1 action point
        self.state.turn_player.hero.action_points = 1
        
        # CR 4.3.3: Turn player gains priority
        self.state.active_player_id = self.state.turn_player_id
    
    def get_legal_actions(self, player_id: int) -> List[Action]:
        """Get all legal actions for the active player.
        
        During action phase (no combat):
        - Play an action card from hand (costs 1 AP + resource cost) (CR 8.1.1)
        - Play an attack action card (opens combat chain) (CR 8.2.3b)
        - Play an instant from hand (CR 8.1.6a)
        - Activate hero ability (Kano: instant, costs 3 resources)
        - Activate equipment/weapon abilities
        - Play a card from arsenal
        - Pass priority (if stack empty + both pass → end action phase)
        
        During combat (depends on step):
        - Layer step: play instants, pass
        - Attack step: play instants, pass  
        - Defend step: declare defenders
        - Reaction step: play attack/defense reactions
        - Damage step: play instants, pass
        - Resolution step: play another attack (if have AP), pass
        """
        # ... (detailed validation logic per phase/step)
    
    def execute_action(self, action: Action) -> ActionResult:
        """Execute a player action and advance game state."""
        # Validate action is legal
        # Execute the action
        # Check game state actions (CR 1.10.2)
        # Return result
    
    # ========================
    # END PHASE (CR 4.4)
    # ========================
    def _end_phase(self):
        """CR 4.4: End phase."""
        self.state.phase = GamePhase.END_PHASE
        
        # CR 4.4.2: "beginning of end phase" triggers
        
        # CR 4.4.3: End-of-turn procedure
        # CR 4.4.3a: Allies life reset (skip - no allies)
        
        # CR 4.4.3b: May arsenal a card from hand
        self._offer_arsenal(self.state.turn_player)
        
        # CR 4.4.3c: Pitch zone → bottom of deck
        self._return_pitch_to_deck(self.state.players[0])
        self._return_pitch_to_deck(self.state.players[1])
        
        # CR 4.4.3d: Untap all permanents (equipment)
        self._untap_all(self.state.turn_player)
        
        # CR 4.4.3e: Lose all action points and resource points
        for player in self.state.players:
            player.hero.action_points = 0
            player.hero.resource_points = 0
        
        # CR 4.4.3f: Draw up to intellect
        self._draw_up_to_intellect(self.state.turn_player)
        # First turn: all players draw up
        if self.state.turn_number == 1:
            self._draw_up_to_intellect(self.state.non_turn_player)
        
        # CR 4.4.4: Turn ends, "until end of turn" effects end
        self._clear_turn_effects()
        
        # Switch turn player
        self.state.turn_player_id = 1 - self.state.turn_player_id
        self.state.turn_number += 1
        
        # Reset per-turn state
        for player in self.state.players:
            player.cards_played_this_turn.clear()
            player.attacks_this_turn = 0
            player.has_defended_with_hand_card = False
            player.damage_dealt_this_turn = 0
            player.arcane_damage_dealt_this_turn = 0
            player.hero.has_used_hero_ability = False
        
        # Start next turn
        self._start_phase()
    
    # ========================
    # HELPER METHODS
    # ========================
    def _draw_up_to_intellect(self, player: PlayerState):
        """Draw cards until hand size equals hero intellect."""
        while player.zones.hand.size < player.hero.intellect:
            card = player.zones.deck.draw_top()
            if card is None:
                break  # Deck empty
            player.zones.hand.add(card)
    
    def _return_pitch_to_deck(self, player: PlayerState):
        """CR 4.4.3c: Return pitch zone cards to bottom of deck."""
        while not player.zones.pitch.is_empty:
            card = player.zones.pitch.draw_top()
            player.zones.deck.add(card, position="bottom")
    
    def _untap_all(self, player: PlayerState):
        """CR 4.4.3d: Untap all permanents."""
        for card in player.zones.all_equipment + player.zones.all_weapons:
            card.is_tapped = False
    
    def _play_card_from_hand(self, player: PlayerState, card: CardInstance):
        """Handle playing a card: pay costs, put on stack/resolve."""
        # CR 5.1.6: Calculate total cost = base cost + additional - reductions
        total_cost = card.template.cost
        
        # CR 8.1.1c: Action cards cost 1 AP
        if CardType.ACTION in card.template.types:
            if player.hero.action_points < 1:
                return False  # Not enough AP
            player.hero.action_points -= 1
        
        # Pay resource cost
        if total_cost > player.hero.resource_points:
            return False  # Need to pitch first
        player.hero.resource_points -= total_cost
        
        # Remove from hand
        player.zones.hand.remove(card)
        
        # If attack: open combat chain
        if Subtype.ATTACK in card.template.subtypes:
            self._open_combat_with_attack(player, card)
        else:
            # Resolve immediately (simplified: no real stack)
            self._resolve_card(player, card)
            # Go to graveyard after resolution
            player.zones.graveyard.add(card)
        
        player.cards_played_this_turn.append(card)
        
        # Go again check
        if card.has_keyword(Keyword.GO_AGAIN):
            player.hero.action_points += 1
        
        return True
    
    def _pitch_card(self, player: PlayerState, card: CardInstance):
        """Pitch a card from hand for resources."""
        if not card.template.has_pitch:
            return False
        player.zones.hand.remove(card)
        player.zones.pitch.add(card)
        player.hero.resource_points += card.template.pitch
        return True
    
    def _check_game_over(self):
        """CR 4.5: Check if any player has lost."""
        for player in self.state.players:
            if not player.hero.is_alive:
                self.state.game_over = True
                self.state.winner = 1 - player.player_id
                return True
        return False
```

#### 3. Action Types (`fab_engine/engine/actions.py`)

```python
from enum import Enum, auto

class ActionType(Enum):
    PITCH_CARD = auto()          # Pitch a card from hand for resources
    PLAY_CARD_FROM_HAND = auto() # Play a card from hand
    PLAY_CARD_FROM_ARSENAL = auto()
    ACTIVATE_HERO_ABILITY = auto()
    ACTIVATE_EQUIPMENT = auto()
    ACTIVATE_WEAPON = auto()
    DECLARE_DEFENDERS = auto()   # During defend step
    PLAY_ATTACK_REACTION = auto()
    PLAY_DEFENSE_REACTION = auto()
    PASS_PRIORITY = auto()       # Pass to other player / end phase
    ARSENAL_CARD = auto()        # Arsenal a card during end phase

@dataclass
class Action:
    action_type: ActionType
    player_id: int
    card_instance_id: int = -1   # Which card to act on
    target_ids: List[int] = field(default_factory=list)  # For targeted effects
    defender_ids: List[int] = field(default_factory=list)  # For declare defenders

@dataclass
class ActionResult:
    success: bool
    damage_dealt: int = 0
    arcane_damage_dealt: int = 0
    cards_drawn: int = 0
    message: str = ""
```

### Success Criteria:

#### Automated Verification:
- [x] GameEngine initializes with two players
- [x] `setup_game()` shuffles decks and draws starting hands (4 cards each)
- [x] Turn structure cycles correctly: Start → Action → End → Start (next player)
- [x] Pitching correctly adds resources and moves card to pitch zone
- [x] Playing an action card deducts AP and resources
- [x] Playing an attack opens combat (tested in Phase 4)
- [x] End phase: pitch zone → deck bottom, draw up to intellect, reset AP/resources
- [x] Game ends when a hero reaches 0 life
- [x] `python -m pytest tests/test_engine.py` passes

#### Manual Verification:
- [x] Step through a manual game turn and verify state transitions
- [x] Verify action point economy: start with 1 AP, go again grants +1

**Implementation Note**: After completing this phase and all automated verification passes, pause here for manual confirmation before proceeding.

---

## Phase 4: Combat Chain

### Overview
Implement the full combat chain with all steps (CR 7.0-7.7): Layer → Attack → Defend → Reaction → Damage → Resolution → Close. This is the most complex phase - combat is where the majority of FaB gameplay happens.

### Changes Required:

#### 1. Combat Chain Data Structure (`fab_engine/engine/combat.py`)

```python
@dataclass
class ChainLink:
    """A single chain link on the combat chain (CR 7.0.3).
    
    Represents one attack and its resolution.
    """
    link_number: int
    attacking_card: CardInstance       # The active-attack (CR 7.0.4)
    attack_target_player_id: int      # Defending hero's player ID
    defending_cards: List[CardInstance] = field(default_factory=list)
    
    # Damage tracking for this link
    physical_damage_dealt: int = 0
    did_hit: bool = False
    
    @property
    def total_defense(self) -> int:
        """Sum of defense values of all defending cards."""
        return sum(
            max(0, c.effective_defense)
            for c in self.defending_cards
            if c.effective_defense >= 0  # Must have defense property
        )

class CombatChain:
    """The combat chain zone (CR 7.0.2).
    
    Tracks chain links, the current step, and whether the chain is open.
    """
    
    def __init__(self):
        self.is_open: bool = False
        self.chain_links: List[ChainLink] = []
        self.current_step: CombatStep = CombatStep.NONE
    
    @property
    def active_chain_link(self) -> Optional[ChainLink]:
        """The most recent chain link (CR 7.0.3b)."""
        return self.chain_links[-1] if self.chain_links else None
    
    def open_chain(self, attacking_card: CardInstance, target_player_id: int):
        """Open the combat chain with a new attack (CR 7.0.2a)."""
        self.is_open = True
        link = ChainLink(
            link_number=len(self.chain_links) + 1,
            attacking_card=attacking_card,
            attack_target_player_id=target_player_id,
        )
        self.chain_links.append(link)
        self.current_step = CombatStep.LAYER
    
    def add_chain_link(self, attacking_card: CardInstance, target_player_id: int):
        """Add a new chain link during resolution step (CR 7.6.3a)."""
        link = ChainLink(
            link_number=len(self.chain_links) + 1,
            attacking_card=attacking_card,
            attack_target_player_id=target_player_id,
        )
        self.chain_links.append(link)
        self.current_step = CombatStep.LAYER
    
    def close(self):
        """Close the combat chain (CR 7.7)."""
        self.is_open = False
        self.current_step = CombatStep.NONE
```

#### 2. Combat Step Resolution (`fab_engine/engine/combat.py`)

```python
class CombatEngine:
    """Handles combat chain step resolution."""
    
    def __init__(self, game_state: GameState, game_engine: 'GameEngine'):
        self.state = game_state
        self.engine = game_engine
    
    # ========================
    # LAYER STEP (CR 7.1)
    # ========================
    def begin_layer_step(self):
        """CR 7.1: Attack is on the stack, waiting to resolve."""
        self.state.combat_step = CombatStep.LAYER
        # CR 7.1.2: Turn player gains priority
        self.state.active_player_id = self.state.turn_player_id
        # Players can play instants here
        # When both pass, proceed to attack step
    
    def resolve_layer_step(self):
        """Transition from layer step to attack step."""
        self.begin_attack_step()
    
    # ========================
    # ATTACK STEP (CR 7.2)
    # ========================
    def begin_attack_step(self):
        """CR 7.2: Attack resolves and becomes attacking."""
        self.state.combat_step = CombatStep.ATTACK
        chain = self.state.combat_chain
        link = chain.active_chain_link
        
        # CR 7.2.2: Check attack target is still legal
        target_player = self.state.players[link.attack_target_player_id]
        if not target_player.hero.is_alive:
            self.begin_close_step()
            return
        
        # CR 7.2.3: Resolution abilities of attack generate effects
        # (Simplified: handle card-specific effects here)
        self._resolve_attack_on_hit_triggers(link)
        
        # CR 7.2.4: "attack" event occurs
        # CR 7.2.5: Turn player gains priority
        self.state.active_player_id = self.state.turn_player_id
    
    # ========================
    # DEFEND STEP (CR 7.3)
    # ========================
    def begin_defend_step(self):
        """CR 7.3: Defending hero may declare defenders."""
        self.state.combat_step = CombatStep.DEFEND
        # CR 7.3.1: Defending player declares cards
        # This is handled by the defending player's action choice
        chain = self.state.combat_chain
        link = chain.active_chain_link
        defending_player_id = link.attack_target_player_id
        self.state.active_player_id = defending_player_id
    
    def declare_defenders(self, player: PlayerState, 
                         hand_card_ids: List[int],
                         equipment_ids: List[int]):
        """CR 7.3.2: Declare defending cards.
        
        Cards from hand and public equipment can defend.
        Each must have the defense property (CR 7.3.2b).
        """
        chain = self.state.combat_chain
        link = chain.active_chain_link
        attack = link.attacking_card
        
        for card_id in hand_card_ids:
            card = player.zones.hand.get_by_id(card_id)
            if card is None:
                continue
            if not card.template.has_defense:
                continue  # CR 7.3.2b: must have defense property
            
            # Check dominate (CR 8.3.4)
            if attack.has_keyword(Keyword.DOMINATE):
                if player.has_defended_with_hand_card:
                    continue  # Can't defend with more than 1 card from hand
            
            # Check overpower (CR 8.3.22)
            if attack.has_keyword(Keyword.OVERPOWER):
                action_defenders = [c for c in link.defending_cards 
                                   if CardType.ACTION in c.template.types]
                if action_defenders:
                    if CardType.ACTION in card.template.types:
                        continue  # Can't defend with more than 1 action card
            
            # Move card from hand to combat chain as defender
            player.zones.hand.remove(card)
            link.defending_cards.append(card)
            player.has_defended_with_hand_card = True
        
        # Equipment defending (CR 8.1.4b)
        for card_id in equipment_ids:
            card = None
            for zone in player.zones.equipment_zones:
                card = zone.get_by_id(card_id)
                if card:
                    break
            if card is None:
                continue
            if not card.template.has_defense:
                continue
            if card.effective_defense <= 0:
                continue  # Broken equipment
            
            link.defending_cards.append(card)
            # Note: equipment stays in its zone but is "on the chain link"
        
        # Proceed to reaction step
        self.begin_reaction_step()
    
    # ========================
    # REACTION STEP (CR 7.4)
    # ========================
    def begin_reaction_step(self):
        """CR 7.4: Players may play reactions."""
        self.state.combat_step = CombatStep.REACTION
        # CR 7.4.2: Turn player gains priority first
        self.state.active_player_id = self.state.turn_player_id
        # Attacker can play attack reactions
        # Defender can play defense reactions
        # When both pass, proceed to damage step
    
    # ========================
    # DAMAGE STEP (CR 7.5)
    # ========================
    def resolve_damage_step(self):
        """CR 7.5: Calculate and apply physical damage."""
        self.state.combat_step = CombatStep.DAMAGE
        chain = self.state.combat_chain
        link = chain.active_chain_link
        attack = link.attacking_card
        
        # CR 7.5.2: power > total defense → deal difference as physical damage
        attack_power = attack.effective_power
        total_defense = link.total_defense
        
        if attack_power > total_defense:
            damage = attack_power - total_defense
            target = self.state.players[link.attack_target_player_id]
            target.hero.life_total -= damage
            link.physical_damage_dealt = damage
            link.did_hit = True
            
            # Track damage
            attacker = self.state.turn_player
            attacker.damage_dealt_this_turn += damage
            
            self.engine._check_game_over()
        
        # CR 7.5.3: Turn player gains priority
        self.state.active_player_id = self.state.turn_player_id
    
    # ========================
    # RESOLUTION STEP (CR 7.6)
    # ========================
    def begin_resolution_step(self):
        """CR 7.6: Chain link resolves."""
        self.state.combat_step = CombatStep.RESOLUTION
        chain = self.state.combat_chain
        link = chain.active_chain_link
        
        # CR 7.6.2: Go again check
        attack = link.attacking_card
        if attack.has_keyword(Keyword.GO_AGAIN):
            self.state.turn_player.hero.action_points += 1
        
        # CR 7.6.2: On-hit triggers
        if link.did_hit:
            self._process_on_hit_effects(link)
        
        # CR 7.6.3: Turn player gains priority
        # Can play another attack to continue the chain
        self.state.active_player_id = self.state.turn_player_id
    
    # ========================
    # CLOSE STEP (CR 7.7)
    # ========================
    def begin_close_step(self):
        """CR 7.7: Combat chain closes."""
        self.state.combat_step = CombatStep.CLOSE
        chain = self.state.combat_chain
        
        # CR 7.7.3: "combat chain closes" event
        # Process equipment effects (battleworn, blade break, temper)
        for link in chain.chain_links:
            for card in link.defending_cards:
                self._process_post_defend_effects(card)
        
        # CR 7.7.5: Equipment returns to zones
        # (Equipment cards that were defending return to their equipment zone)
        
        # CR 7.7.6: All other cards on chain → graveyard
        for link in chain.chain_links:
            # Attack card → graveyard
            attack_card = link.attacking_card
            owner = self.state.players[0]  # Determine owner
            owner.zones.graveyard.add(attack_card)
            
            # Non-equipment defending cards → graveyard
            for card in link.defending_cards:
                if not card.template.is_equipment:
                    defender = self.state.players[link.attack_target_player_id]
                    defender.zones.graveyard.add(card)
        
        # CR 7.7.7: Close the chain
        chain.close()
        
        # Return to action phase
        self.state.phase = GamePhase.ACTION_PHASE
        self.state.active_player_id = self.state.turn_player_id
    
    def _process_post_defend_effects(self, card: CardInstance):
        """Handle equipment keywords after defending."""
        if card.has_keyword(Keyword.BATTLEWORN):
            # CR 8.3.2: Put -1{d} counter
            card.defense_counters -= 1
        
        if card.has_keyword(Keyword.BLADE_BREAK):
            # CR 8.3.3: Destroy it
            self._destroy_equipment(card)
        
        if card.has_keyword(Keyword.TEMPER):
            # CR 8.3.10: Put -1{d} counter, destroy if 0{d}
            card.defense_counters -= 1
            if card.effective_defense <= 0:
                self._destroy_equipment(card)
        
        if card.has_keyword(Keyword.GUARDWELL):
            # CR 8.3.34: Put -1{d} counters equal to current {d}
            card.defense_counters -= card.effective_defense
```

### Success Criteria:

#### Automated Verification:
- [x] Playing an attack action card opens the combat chain
- [x] Combat chain transitions through all steps: Layer → Attack → Defend → Reaction → Damage → Resolution → Close
- [x] Physical damage calculation is correct: power - total defense = damage to hero
- [x] Hit detection works: damage > 0 → did_hit = True
- [x] Defending with hand cards removes them from hand and adds defense
- [x] Equipment defending: equipment defense values contribute, equipment stays in zone
- [x] Dominate: can't defend with more than 1 hand card
- [x] Overpower: can't defend with more than 1 action card
- [x] Go again: attacker gains 1 AP when chain link resolves
- [x] Battleworn: equipment gets -1{d} counter after defending
- [x] Blade break: equipment destroyed after defending
- [x] Close step: attack cards → graveyard, hand defending cards → graveyard, equipment returns to zones
- [x] Multiple chain links work (attack → go again → another attack on same chain)
- [x] `python -m pytest tests/test_combat.py` passes

#### Manual Verification:
- [x] Play through a complete combat sequence manually and verify each step
- [x] Test a multi-attack chain link combat (attack with go again, then attack again)
- [x] Verify damage is applied to the correct hero

**Implementation Note**: After completing this phase and all automated verification passes, pause here for manual confirmation before proceeding.

---

## Phase 5: Keyword & Ability System

### Overview
Implement card abilities that go beyond simple play-for-damage. This includes arcane damage effects, Kano's hero ability, defense reactions, attack reactions, and key keywords. Abilities are registered by card name or keyword, not parsed from text.

### Changes Required:

#### 1. Ability Registry (`fab_engine/cards/abilities.py`)

```python
from typing import Callable, Dict

# Type for ability effect functions
EffectFn = Callable[['GameEngine', 'PlayerState', 'CardInstance'], None]

class AbilityRegistry:
    """Registry of card-specific and keyword-based effects.
    
    Cards are mapped to their effects by name. When a card is played/resolves,
    the engine looks up its effects in this registry.
    """
    
    def __init__(self):
        # Card name → play effect
        self._play_effects: Dict[str, EffectFn] = {}
        # Card name → on-hit effect (when attack hits)
        self._on_hit_effects: Dict[str, EffectFn] = {}
        # Card name → when-defends effect
        self._defend_effects: Dict[str, EffectFn] = {}
        # Hero ability name → activation effect
        self._hero_abilities: Dict[str, EffectFn] = {}
        # Equipment/weapon name → activation effect
        self._activated_abilities: Dict[str, EffectFn] = {}
    
    def register_play_effect(self, card_name: str, fn: EffectFn):
        self._play_effects[card_name] = fn
    
    def register_on_hit(self, card_name: str, fn: EffectFn):
        self._on_hit_effects[card_name] = fn
    
    def get_play_effect(self, card_name: str) -> Optional[EffectFn]:
        return self._play_effects.get(card_name)
    
    def get_on_hit_effect(self, card_name: str) -> Optional[EffectFn]:
        return self._on_hit_effects.get(card_name)


# Singleton registry
ABILITY_REGISTRY = AbilityRegistry()
```

#### 2. Core Effect Functions (`fab_engine/engine/effects.py`)

```python
def deal_arcane_damage(engine: 'GameEngine', source_player: PlayerState, 
                       target_player: PlayerState, amount: int,
                       source_card: CardInstance):
    """Deal arcane damage to a hero (CR 8.5.3b).
    
    Arcane damage is not physical damage - it bypasses combat.
    It can be prevented by Arcane Barrier (CR 8.3.8).
    """
    # Check Arcane Barrier on defending equipment
    remaining = amount
    for card in target_player.zones.all_equipment:
        if remaining <= 0:
            break
        ab_value = card.get_keyword_param(Keyword.ARCANE_BARRIER)
        if ab_value > 0:
            # Player can pay {r} per point to prevent
            can_prevent = min(ab_value, remaining, target_player.hero.resource_points)
            if can_prevent > 0:
                # For heuristic: always prevent if possible
                # For RL agent: this would be a decision point
                target_player.hero.resource_points -= can_prevent
                remaining -= can_prevent
    
    # Apply remaining arcane damage
    if remaining > 0:
        target_player.hero.life_total -= remaining
        source_player.damage_dealt_this_turn += remaining
        source_player.arcane_damage_dealt_this_turn += remaining
        engine._check_game_over()
    
    return remaining  # Actual damage dealt


def deal_generic_damage(engine: 'GameEngine', target_player: PlayerState, amount: int):
    """Deal generic (non-typed) damage to a hero (CR 8.5.3b)."""
    if amount > 0:
        target_player.hero.life_total -= amount
        engine._check_game_over()
    return amount
```

#### 3. Kano Hero Ability

```python
def kano_hero_ability(engine: 'GameEngine', player: PlayerState, hero_card: CardInstance):
    """Kano's hero ability: Instant - {r}{r}{r}
    
    Look at top card of deck. If it's a non-attack action card,
    may banish it. If banished, may play it this turn as though
    it were an instant.
    
    Per CR: This is an activated ability (Instant timing).
    Cost: 3 resource points.
    """
    # Check cost
    if player.hero.resource_points < 3:
        return False
    
    # Pay cost
    player.hero.resource_points -= 3
    
    # Look at top card
    top_card = player.zones.deck.peek_top()
    if top_card is None:
        return True  # Ability used but deck empty
    
    # Check if non-attack action card
    is_action = CardType.ACTION in top_card.template.types
    is_attack = Subtype.ATTACK in top_card.template.subtypes
    
    if is_action and not is_attack:
        # May banish it (for RL: always banish for now, could be decision)
        card = player.zones.deck.draw_top()
        card.is_face_up = True
        player.zones.banished.add(card)
        
        # Card can be played this turn as an instant
        # Mark it as playable-from-banished
        card.temp_keywords[Keyword.GO_AGAIN] = 0  # Not go again, just a marker
        # Engine needs to allow playing from banished zone for this card
        
        return True
    
    return True  # Looked but couldn't banish

ABILITY_REGISTRY.register_hero_ability("Kano", kano_hero_ability)
```

#### 4. Key Card Effects to Register

For the most common/important Wizard cards:

```python
# Aether Flare (Red/Yellow/Blue)
# "Deal 3/2/1 arcane damage to target opposing hero.
#  Next card with arcane damage effect deals +X where X = damage dealt"
def aether_flare_effect(engine, player, card):
    target = engine.state.non_turn_player if player == engine.state.turn_player else engine.state.turn_player
    arcane_val = card.template.arcane
    actual = deal_arcane_damage(engine, player, target, arcane_val, card)
    # Set up bonus for next arcane spell
    player._next_arcane_bonus = actual

# Aether Dart (Blue)
# "Deal 1 arcane damage to target opposing hero"
def aether_dart_effect(engine, player, card):
    target = engine.state.non_turn_player if player == engine.state.turn_player else engine.state.turn_player
    deal_arcane_damage(engine, player, target, card.template.arcane, card)

# Aether Conduit (Weapon - Staff)
# "Once per Turn Action - {r}{r}: Deal 2 arcane damage to target hero"
def aether_conduit_activate(engine, player, card):
    if card.is_tapped:
        return False
    if player.hero.resource_points < 2:
        return False
    player.hero.resource_points -= 2
    card.is_tapped = True  # Once per turn
    target = engine.state.non_turn_player if player == engine.state.turn_player else engine.state.turn_player
    deal_arcane_damage(engine, player, target, 2, card)
    return True

# Register all effects
ABILITY_REGISTRY.register_play_effect("Aether Flare", aether_flare_effect)
ABILITY_REGISTRY.register_play_effect("Aether Dart", aether_dart_effect)
ABILITY_REGISTRY.register_activated_ability("Aether Conduit", aether_conduit_activate)
# ... register more cards as needed
```

#### 5. Default Card Resolution

Cards without registered effects use default behavior:
- **Attack action cards**: Power contributes to combat damage (handled by combat chain)
- **Non-attack action cards with arcane**: Deal arcane damage equal to `arcane` value
- **Defense reactions**: Become a defending card with their defense value
- **Instants**: Effect depends on registration; if unregistered, no effect

### Success Criteria:

#### Automated Verification:
- [x] Arcane damage correctly reduces target hero life
- [x] Arcane Barrier prevents arcane damage at resource cost
- [x] Kano's hero ability: costs 3 resources, looks at top card, can banish/play non-attack actions
- [x] Aether Flare deals arcane damage and sets up bonus for next spell
- [x] Aether Conduit activation: costs 2 resources, deals 2 arcane, once per turn
- [x] Go again: playing a card with go again grants +1 AP
- [x] Default card resolution works for unregistered cards (attacks use power, spells use arcane)
- [x] `python -m pytest tests/test_abilities.py` passes

#### Manual Verification:
- [x] Play a turn with Kano's hero ability and verify the full sequence
- [x] Verify Arcane Barrier decision-making (prevent or take damage)
- [x] Check that the ability registry correctly dispatches effects

**Implementation Note**: After completing this phase and all automated verification passes, pause here for manual confirmation before proceeding.

---

## Phase 6: Card Loading & Filtering

### Overview
Load real cards from the FaB card database with full property parsing. Filter for Kano-eligible cards and Generic cards for the opponent. Map card database fields to our CardTemplate model.

### Changes Required:

#### 1. Card Loader (`fab_engine/cards/loader.py`)

```python
import json
import os
from typing import List, Dict, Optional
from fab_engine.cards.model import *

DB_PATH = "~/repos/github/flesh-and-blood-cards/json/english/card.json"

def load_card_database(db_path: str = DB_PATH) -> List[Dict]:
    """Load raw card data from JSON."""
    db_path = os.path.expanduser(db_path)
    with open(db_path, "r") as f:
        return json.load(f)

def parse_card_template(raw: Dict) -> CardTemplate:
    """Convert raw JSON card data to CardTemplate."""
    types_raw = raw.get("types", [])
    
    # Parse types
    types = set()
    for t in types_raw:
        if t == "Action": types.add(CardType.ACTION)
        elif t == "Attack Reaction": types.add(CardType.ATTACK_REACTION)
        elif t == "Defense Reaction": types.add(CardType.DEFENSE_REACTION)
        elif t == "Instant": types.add(CardType.INSTANT)
        elif t == "Equipment": types.add(CardType.EQUIPMENT)
        elif t == "Weapon": types.add(CardType.WEAPON)
        elif t == "Hero": types.add(CardType.HERO)
    
    # Parse supertypes (also in types[] in the DB)
    supertypes = set()
    for t in types_raw:
        if t == "Wizard": supertypes.add(Supertype.WIZARD)
        elif t == "Generic": supertypes.add(Supertype.GENERIC)
        elif t == "Guardian": supertypes.add(Supertype.GUARDIAN)
        elif t == "Warrior": supertypes.add(Supertype.WARRIOR)
        elif t == "Ninja": supertypes.add(Supertype.NINJA)
        elif t == "Brute": supertypes.add(Supertype.BRUTE)
    
    # Parse subtypes from type_text
    type_text = raw.get("type_text", "")
    subtypes = set()
    if "Attack" in types_raw:
        subtypes.add(Subtype.ATTACK)
    if "(2H)" in type_text: subtypes.add(Subtype.TWO_HAND)
    if "(1H)" in type_text: subtypes.add(Subtype.ONE_HAND)
    if "Staff" in type_text: subtypes.add(Subtype.STAFF)
    if "Sword" in type_text: subtypes.add(Subtype.SWORD)
    if "Orb" in type_text: subtypes.add(Subtype.ORB)
    if "Head" in type_text: subtypes.add(Subtype.HEAD)
    if "Chest" in type_text: subtypes.add(Subtype.CHEST)
    if "Arms" in type_text: subtypes.add(Subtype.ARMS)
    if "Legs" in type_text: subtypes.add(Subtype.LEGS)
    if "Off-Hand" in type_text: subtypes.add(Subtype.OFF_HAND)
    
    # Parse numeric values
    def parse_int(val, default=-1):
        if val is None or val == "":
            return default
        try:
            return int(float(val))
        except:
            return default
    
    pitch_val = parse_int(raw.get("pitch"), -1)
    cost_val = parse_int(raw.get("cost"), -1)
    power_val = parse_int(raw.get("power"), -1)
    defense_val = parse_int(raw.get("defense"), -1)
    arcane_val = parse_int(raw.get("arcane"), 0)
    life_val = parse_int(raw.get("health"), 0)
    intellect_val = parse_int(raw.get("intelligence"), 0)
    
    # Parse keywords from functional text
    func_text = raw.get("functional_text_plain", "")
    keywords = parse_keywords_from_text(func_text)
    
    # Parse color
    color_str = raw.get("color", "")
    color = {
        "Red": Color.RED, "Yellow": Color.YELLOW, 
        "Blue": Color.BLUE
    }.get(color_str, Color.COLORLESS)
    
    return CardTemplate(
        unique_id=raw.get("unique_id", ""),
        name=raw.get("name", ""),
        types=frozenset(types),
        supertypes=frozenset(supertypes),
        subtypes=frozenset(subtypes),
        color=color,
        pitch=max(0, pitch_val),
        has_pitch=pitch_val >= 0,
        cost=max(0, cost_val),
        has_cost=cost_val >= 0,
        power=max(0, power_val),
        has_power=power_val >= 0,
        defense=max(0, defense_val),
        has_defense=defense_val >= 0,
        arcane=arcane_val,
        has_arcane=arcane_val > 0,
        life=life_val,
        intellect=intellect_val,
        keywords=keywords,
        functional_text=func_text,
        is_attack_action=(CardType.ACTION in types and Subtype.ATTACK in subtypes),
        is_non_attack_action=(CardType.ACTION in types and Subtype.ATTACK not in subtypes),
        is_instant=(CardType.INSTANT in types),
        is_defense_reaction=(CardType.DEFENSE_REACTION in types),
        is_attack_reaction=(CardType.ATTACK_REACTION in types),
        is_equipment=(CardType.EQUIPMENT in types),
        is_weapon=(CardType.WEAPON in types),
        is_hero=(CardType.HERO in types),
    )


def parse_keywords_from_text(text: str) -> Dict:
    """Extract keywords from functional text.
    
    This is a simple regex/string matching approach for common keywords.
    """
    keywords = {}
    text_lower = text.lower()
    
    if "go again" in text_lower:
        keywords[Keyword.GO_AGAIN] = 0
    if "dominate" in text_lower:
        keywords[Keyword.DOMINATE] = 0
    if "overpower" in text_lower:
        keywords[Keyword.OVERPOWER] = 0
    if "phantasm" in text_lower:
        keywords[Keyword.PHANTASM] = 0
    
    # Parameterized keywords
    import re
    ab_match = re.search(r"arcane barrier (\d+)", text_lower)
    if ab_match:
        keywords[Keyword.ARCANE_BARRIER] = int(ab_match.group(1))
    
    sv_match = re.search(r"spellvoid (\d+)", text_lower)
    if sv_match:
        keywords[Keyword.SPELLVOID] = int(sv_match.group(1))
    
    piercing_match = re.search(r"piercing (\d+)", text_lower)
    if piercing_match:
        keywords[Keyword.PIERCING] = int(piercing_match.group(1))
    
    if "battleworn" in text_lower:
        keywords[Keyword.BATTLEWORN] = 0
    if "blade break" in text_lower:
        keywords[Keyword.BLADE_BREAK] = 0
    if "temper" in text_lower:
        keywords[Keyword.TEMPER] = 0
    if "guardwell" in text_lower:
        keywords[Keyword.GUARDWELL] = 0
    
    return keywords


# ========================
# CARD POOL FILTERS
# ========================

TALENT_SUPERTYPES = {
    "Chaos", "Draconic", "Earth", "Elemental", "Ice", 
    "Light", "Lightning", "Mystic", "Revered", "Reviled", 
    "Royal", "Shadow"
}

def is_kano_eligible(raw: Dict) -> bool:
    """Check if card is eligible for Kano's deck (CR 1.1.3).
    
    Kano supertypes: [Wizard]
    Can play: Wizard + Generic (no talent supertypes)
    Rarity: Common or Rare only
    """
    types = raw.get("types", [])
    
    is_wizard = "Wizard" in types
    is_generic = "Generic" in types
    if not (is_wizard or is_generic):
        return False
    
    has_talent = any(t in types for t in TALENT_SUPERTYPES)
    if has_talent:
        return False
    
    # Exclude heroes, tokens
    if "Hero" in types or "Token" in types:
        return False
    
    # Common or Rare printing
    printings = raw.get("printings", [])
    return any(p.get("rarity") in ["C", "R"] for p in printings)


def is_generic_opponent_eligible(raw: Dict) -> bool:
    """Check if card is eligible for the Generic opponent's deck.
    
    Generic hero can only play Generic cards.
    """
    types = raw.get("types", [])
    
    if "Generic" not in types:
        return False
    if "Hero" in types or "Token" in types:
        return False
    
    printings = raw.get("printings", [])
    return any(p.get("rarity") in ["C", "R"] for p in printings)


def load_kano_card_pool() -> List[CardTemplate]:
    """Load all Kano-eligible card templates."""
    raw_cards = load_card_database()
    return [parse_card_template(c) for c in raw_cards if is_kano_eligible(c)]


def load_opponent_card_pool() -> List[CardTemplate]:
    """Load all Generic opponent card templates."""
    raw_cards = load_card_database()
    return [parse_card_template(c) for c in raw_cards if is_generic_opponent_eligible(c)]


def load_hero_template(name: str) -> Optional[CardTemplate]:
    """Load a specific hero card template."""
    raw_cards = load_card_database()
    for c in raw_cards:
        if c.get("name") == name and "Hero" in c.get("types", []):
            return parse_card_template(c)
    return None
```

### Success Criteria:

#### Automated Verification:
- [x] `load_card_database()` loads cards from JSON without errors
- [x] `parse_card_template()` correctly parses all fields for a sample Wizard card
- [x] `parse_keywords_from_text()` extracts go again, dominate, arcane barrier N, etc.
- [x] `is_kano_eligible()` excludes talent-supertype cards (Elemental Wizard, Ice Wizard, etc.)
- [x] `load_kano_card_pool()` returns expected number of cards (~627 unique cards)
- [x] `load_opponent_card_pool()` returns Generic cards for opponent
- [x] `load_hero_template("Kano")` returns the Young Kano hero with life=15, intellect=4
- [x] Equipment cards have correct subtype (Head, Chest, Arms, Legs)
- [x] Weapon cards have correct subtype (Staff, Sword, etc.)
- [x] `python -m pytest tests/test_loader.py` passes

#### Manual Verification:
- [x] Spot-check 5-10 parsed cards against the actual card database
- [x] Verify Kano card pool contains expected cards (Aether Flare, Aether Dart, etc.)
- [x] Verify opponent pool contains attack action cards with power values

**Implementation Note**: After completing this phase and all automated verification passes, pause here for manual confirmation before proceeding.

---

## Phase 7: Heuristic Opponent

### Overview
Implement a simple greedy heuristic opponent that plays as a Generic attacker hero. The heuristic follows straightforward rules: pitch blue cards, play highest-damage attacks, defend with lowest-value cards.

### Changes Required:

#### 1. Heuristic Agent (`fab_engine/agents/heuristic.py`)

```python
class GreedyHeuristic:
    """Simple greedy opponent strategy.
    
    Attack turn:
    1. Pitch highest-pitch cards first (blues > yellows > reds)
    2. Play highest-damage attack action cards that can be afforded
    3. Chain attacks if go again is available
    4. End turn when out of AP or playable cards
    
    Defense turn:
    1. Defend with lowest-value hand cards first (cards with lowest damage potential)
    2. Use equipment defense if available and worth it
    3. Don't over-block (don't defend if damage is small)
    4. Save high-damage cards for offense
    
    Resource management:
    - Always pitch the card with highest pitch value and lowest damage
    - Never pitch cards with go again (they're valuable for chaining)
    """
    
    def __init__(self, player_id: int):
        self.player_id = player_id
    
    def choose_action(self, game_state: GameState) -> Action:
        """Choose the best action given current game state."""
        player = game_state.players[self.player_id]
        phase = game_state.phase
        combat_step = game_state.combat_step
        
        if combat_step == CombatStep.DEFEND:
            return self._choose_defense(game_state, player)
        elif combat_step == CombatStep.REACTION:
            return self._choose_reaction(game_state, player)
        elif phase == GamePhase.ACTION_PHASE:
            return self._choose_attack_action(game_state, player)
        elif phase == GamePhase.END_PHASE:
            return self._choose_end_phase_action(game_state, player)
        else:
            return Action(ActionType.PASS_PRIORITY, self.player_id)
    
    def _choose_attack_action(self, state: GameState, player: PlayerState) -> Action:
        """Choose what to do during action phase (our turn)."""
        hand = player.zones.hand.cards
        
        if not hand:
            return Action(ActionType.PASS_PRIORITY, self.player_id)
        
        # First: if we have AP and can play an attack, do it
        if player.hero.action_points > 0:
            # Find playable attack action cards
            playable_attacks = [
                c for c in hand
                if c.template.is_attack_action and c.template.cost <= player.hero.resource_points
            ]
            
            if playable_attacks:
                # Play highest damage attack
                best = max(playable_attacks, key=lambda c: c.effective_power)
                return Action(ActionType.PLAY_CARD_FROM_HAND, self.player_id, 
                            card_instance_id=best.instance_id)
            
            # Need resources - pitch a card
            pitchable = [c for c in hand if c.template.has_pitch]
            if pitchable:
                # Pitch the card with best pitch-to-damage ratio (high pitch, low damage)
                best_pitch = max(pitchable, key=lambda c: (c.template.pitch, -c.template.power))
                return Action(ActionType.PITCH_CARD, self.player_id, 
                            card_instance_id=best_pitch.instance_id)
        
        return Action(ActionType.PASS_PRIORITY, self.player_id)
    
    def _choose_defense(self, state: GameState, player: PlayerState) -> Action:
        """Choose which cards to defend with."""
        chain = state.combat_chain
        link = chain.active_chain_link
        if link is None:
            return Action(ActionType.PASS_PRIORITY, self.player_id)
        
        attack_power = link.attacking_card.effective_power
        
        # Sort hand cards by "sacrifice value" - defend with worst offensive cards first
        hand = player.zones.hand.cards
        defendable = [c for c in hand if c.template.has_defense]
        
        # Sort by: lowest damage first (sacrifice the worst cards)
        defendable.sort(key=lambda c: (c.template.power if c.template.has_power else 0, 
                                        c.template.arcane))
        
        # Choose cards to defend with: block enough to prevent most damage
        # Don't over-block - leave cards for offense
        defender_ids = []
        total_defense = 0
        
        for card in defendable:
            if total_defense >= attack_power:
                break  # Enough defense
            # Don't sacrifice high-value attack cards unless necessary
            if (card.template.has_power and card.effective_power >= 5 and 
                total_defense > 0):
                continue  # Save this card
            defender_ids.append(card.instance_id)
            total_defense += card.effective_defense
        
        # Also consider equipment
        equipment_ids = []
        for eq in player.zones.all_equipment:
            if eq.effective_defense > 0 and total_defense < attack_power:
                equipment_ids.append(eq.instance_id)
                total_defense += eq.effective_defense
        
        return Action(ActionType.DECLARE_DEFENDERS, self.player_id,
                      defender_ids=defender_ids + equipment_ids)
    
    def _choose_reaction(self, state: GameState, player: PlayerState) -> Action:
        """Choose reaction during reaction step."""
        # Simple: no reactions for now
        return Action(ActionType.PASS_PRIORITY, self.player_id)
    
    def _choose_end_phase_action(self, state: GameState, player: PlayerState) -> Action:
        """Choose arsenal card during end phase."""
        # Arsenal the best card remaining in hand
        hand = player.zones.hand.cards
        if hand and player.zones.arsenal.is_empty:
            # Arsenal the highest-damage card
            best = max(hand, key=lambda c: (c.template.power if c.template.has_power else 0))
            return Action(ActionType.ARSENAL_CARD, self.player_id, 
                        card_instance_id=best.instance_id)
        return Action(ActionType.PASS_PRIORITY, self.player_id)
```

#### 2. Opponent Deck Builder

```python
def build_generic_opponent_deck(card_pool: List[CardTemplate], 
                                 deck_size: int = 40) -> List[CardTemplate]:
    """Build a reasonable Generic attack deck for the opponent.
    
    Strategy: Mix of attack action cards with good damage/cost ratio,
    balanced pitch distribution (30% red, 30% yellow, 40% blue).
    """
    # Filter to attack action cards and useful non-attacks
    attacks = [c for c in card_pool if c.is_attack_action and c.has_power]
    
    # Sort by damage efficiency
    attacks.sort(key=lambda c: c.power / max(c.cost, 1), reverse=True)
    
    deck = []
    # 12 red attacks (high damage)
    red_attacks = [c for c in attacks if c.color == Color.RED][:12]
    # 12 yellow attacks (balanced)
    yellow_attacks = [c for c in attacks if c.color == Color.YELLOW][:12]
    # 16 blue cards (resource generation)
    blue_attacks = [c for c in attacks if c.color == Color.BLUE][:16]
    
    deck.extend(red_attacks)
    deck.extend(yellow_attacks)
    deck.extend(blue_attacks)
    
    # Fill remaining slots
    while len(deck) < deck_size:
        remaining = [c for c in attacks if c not in deck]
        if remaining:
            deck.append(remaining[0])
        else:
            deck.append(attacks[0])  # Duplicate best card
    
    return deck[:deck_size]
```

### Success Criteria:

#### Automated Verification:
- [x] Heuristic opponent can play a complete game without errors
- [x] Attack selection picks highest damage affordable card
- [x] Pitching prioritizes high-pitch, low-damage cards
- [x] Defense selection doesn't over-block
- [x] Equipment defense is used when beneficial
- [x] Opponent deck builder creates a 40-card deck with balanced pitch distribution
- [x] `python -m pytest tests/test_heuristic.py` passes

#### Manual Verification:
- [x] Watch a full game between random Kano deck and heuristic opponent
- [x] Verify opponent makes reasonable decisions (attacks, defends, pitches)
- [x] Confirm games typically complete within 10-20 turns

**Implementation Note**: After completing this phase and all automated verification passes, pause here for manual confirmation before proceeding.

---

## Phase 8: Gymnasium Environment

### Overview
Create the Gymnasium environment wrapper with Dict observation space and micro-action space. The agent (Kano) takes one action per step, and the heuristic opponent responds automatically.

### Changes Required:

#### 1. Observation Encoding (`fab_engine/gym_env/observation.py`)

```python
import numpy as np
from gymnasium import spaces

def build_observation_space() -> spaces.Dict:
    """Define the Dict observation space.
    
    Observations include:
    - hand: 4 cards x features (pitch, cost, power, defense, arcane, color, type flags)
    - opponent_life: scalar
    - my_life: scalar  
    - resources: scalar
    - action_points: scalar
    - turn_number: scalar
    - game_phase: one-hot (action, combat steps)
    - opponent_equipment_defense: 4 values (head, chest, arms, legs)
    - opponent_hand_size: scalar
    - deck_size: scalar
    - arsenal: 1 card x features (or zeros if empty)
    - combat_state: attack power, total defense, chain link count
    """
    CARD_FEATURES = 10  # pitch, cost, power, defense, arcane, color(3), is_attack, is_instant
    MAX_HAND = 4
    
    return spaces.Dict({
        "hand": spaces.Box(0, 1, shape=(MAX_HAND, CARD_FEATURES), dtype=np.float32),
        "hand_mask": spaces.MultiBinary(MAX_HAND),  # Which hand slots are occupied
        "arsenal": spaces.Box(0, 1, shape=(1, CARD_FEATURES), dtype=np.float32),
        "arsenal_mask": spaces.MultiBinary(1),
        "my_life": spaces.Box(0, 1, shape=(1,), dtype=np.float32),
        "opponent_life": spaces.Box(0, 1, shape=(1,), dtype=np.float32),
        "resources": spaces.Box(0, 1, shape=(1,), dtype=np.float32),
        "action_points": spaces.Box(0, 1, shape=(1,), dtype=np.float32),
        "turn_number": spaces.Box(0, 1, shape=(1,), dtype=np.float32),
        "phase": spaces.MultiBinary(8),  # One-hot for game phase + combat steps
        "opponent_equipment_defense": spaces.Box(0, 1, shape=(4,), dtype=np.float32),
        "opponent_hand_size": spaces.Box(0, 1, shape=(1,), dtype=np.float32),
        "deck_size": spaces.Box(0, 1, shape=(1,), dtype=np.float32),
        "combat_attack_power": spaces.Box(0, 1, shape=(1,), dtype=np.float32),
        "combat_total_defense": spaces.Box(0, 1, shape=(1,), dtype=np.float32),
    })


def encode_observation(game_state: GameState, player_id: int) -> dict:
    """Encode game state into observation dict for the RL agent."""
    player = game_state.players[player_id]
    opponent = game_state.players[1 - player_id]
    
    # Normalize values to [0, 1] range
    obs = {}
    
    # Hand encoding
    hand_obs = np.zeros((4, 10), dtype=np.float32)
    hand_mask = np.zeros(4, dtype=np.int8)
    for i, card in enumerate(player.zones.hand.cards[:4]):
        hand_obs[i] = encode_card(card)
        hand_mask[i] = 1
    obs["hand"] = hand_obs
    obs["hand_mask"] = hand_mask
    
    # Arsenal
    arsenal_obs = np.zeros((1, 10), dtype=np.float32)
    arsenal_mask = np.zeros(1, dtype=np.int8)
    if not player.zones.arsenal.is_empty:
        arsenal_obs[0] = encode_card(player.zones.arsenal.cards[0])
        arsenal_mask[0] = 1
    obs["arsenal"] = arsenal_obs
    obs["arsenal_mask"] = arsenal_mask
    
    # Scalars
    obs["my_life"] = np.array([player.hero.life_total / 40.0], dtype=np.float32)
    obs["opponent_life"] = np.array([opponent.hero.life_total / 40.0], dtype=np.float32)
    obs["resources"] = np.array([min(player.hero.resource_points / 10.0, 1.0)], dtype=np.float32)
    obs["action_points"] = np.array([min(player.hero.action_points / 3.0, 1.0)], dtype=np.float32)
    obs["turn_number"] = np.array([min(game_state.turn_number / 30.0, 1.0)], dtype=np.float32)
    
    # Phase encoding (one-hot)
    phase = np.zeros(8, dtype=np.int8)
    phase_map = {
        GamePhase.ACTION_PHASE: 0,
        CombatStep.LAYER: 1, CombatStep.ATTACK: 2,
        CombatStep.DEFEND: 3, CombatStep.REACTION: 4,
        CombatStep.DAMAGE: 5, CombatStep.RESOLUTION: 6,
    }
    if game_state.combat_step != CombatStep.NONE:
        idx = phase_map.get(game_state.combat_step, 0)
    else:
        idx = phase_map.get(game_state.phase, 0)
    phase[idx] = 1
    obs["phase"] = phase
    
    # Opponent equipment defense
    eq_defense = np.zeros(4, dtype=np.float32)
    for i, zone in enumerate(opponent.zones.equipment_zones):
        if not zone.is_empty:
            eq_defense[i] = zone.cards[0].effective_defense / 3.0
    obs["opponent_equipment_defense"] = eq_defense
    
    obs["opponent_hand_size"] = np.array([opponent.zones.hand.size / 4.0], dtype=np.float32)
    obs["deck_size"] = np.array([player.zones.deck.size / 40.0], dtype=np.float32)
    
    # Combat state
    chain = game_state.combat_chain
    if chain.is_open and chain.active_chain_link:
        link = chain.active_chain_link
        obs["combat_attack_power"] = np.array([link.attacking_card.effective_power / 10.0], dtype=np.float32)
        obs["combat_total_defense"] = np.array([link.total_defense / 10.0], dtype=np.float32)
    else:
        obs["combat_attack_power"] = np.zeros(1, dtype=np.float32)
        obs["combat_total_defense"] = np.zeros(1, dtype=np.float32)
    
    return obs


def encode_card(card: CardInstance) -> np.ndarray:
    """Encode a single card as a feature vector."""
    features = np.zeros(10, dtype=np.float32)
    features[0] = card.template.pitch / 3.0
    features[1] = card.template.cost / 5.0
    features[2] = card.effective_power / 10.0 if card.template.has_power else 0.0
    features[3] = card.effective_defense / 5.0 if card.template.has_defense else 0.0
    features[4] = card.template.arcane / 5.0
    # Color one-hot (3 values)
    features[5] = 1.0 if card.template.color == Color.RED else 0.0
    features[6] = 1.0 if card.template.color == Color.YELLOW else 0.0
    features[7] = 1.0 if card.template.color == Color.BLUE else 0.0
    features[8] = 1.0 if card.template.is_attack_action else 0.0
    features[9] = 1.0 if card.template.is_instant or card.template.is_non_attack_action else 0.0
    return features
```

#### 2. Action Space (`fab_engine/gym_env/action_space.py`)

```python
from gymnasium import spaces

# Micro-action space:
# 0-3:   Pitch hand card 0-3
# 4-7:   Play hand card 0-3
# 8:     Play from arsenal
# 9:     Activate hero ability (Kano)
# 10:    Activate weapon
# 11-14: Defend with hand card 0-3 (during defend step)
# 15-18: Defend with equipment (head/chest/arms/legs)
# 19:    Pass priority / end turn / confirm defenders
ACTION_SPACE = spaces.Discrete(20)

def decode_action(action_id: int, game_state: GameState, player_id: int) -> Action:
    """Convert action space integer to engine Action."""
    # ... mapping logic
```

#### 3. FaB Gymnasium Environment (`fab_engine/gym_env/env.py`)

```python
import gymnasium as gym

class FaBEnv(gym.Env):
    """Two-player FaB Gymnasium environment.
    
    The RL agent plays as Kano (player 0).
    The opponent (player 1) is controlled by a heuristic.
    """
    
    metadata = {"render_modes": ["human"]}
    
    def __init__(self, kano_deck: List[CardTemplate], 
                 opponent_deck: List[CardTemplate],
                 kano_equipment: List[CardTemplate] = None,
                 opponent_equipment: List[CardTemplate] = None,
                 kano_weapon: CardTemplate = None,
                 opponent_weapon: CardTemplate = None,
                 max_turns: int = 50):
        super().__init__()
        
        self.kano_deck_templates = kano_deck
        self.opponent_deck_templates = opponent_deck
        self.kano_equipment_templates = kano_equipment or []
        self.opponent_equipment_templates = opponent_equipment or []
        self.kano_weapon_template = kano_weapon
        self.opponent_weapon_template = opponent_weapon
        self.max_turns = max_turns
        
        self.observation_space = build_observation_space()
        self.action_space = ACTION_SPACE
        
        self.engine: Optional[GameEngine] = None
        self.opponent_agent = GreedyHeuristic(player_id=1)
    
    def reset(self, seed=None, options=None):
        """Reset environment with a new game."""
        super().reset(seed=seed)
        
        # Create game state
        # ... instantiate CardInstances from templates, set up zones, etc.
        
        self.engine = GameEngine(state)
        self.engine.setup_game(first_turn_player=0)  # Kano goes first
        
        obs = encode_observation(self.engine.state, player_id=0)
        return obs, {}
    
    def step(self, action_id: int):
        """Execute one micro-action for the Kano agent.
        
        The opponent's turn is handled automatically by the heuristic.
        """
        state = self.engine.state
        
        # If it's the opponent's turn or opponent needs to act, let heuristic handle
        while state.active_player_id == 1 and not state.game_over:
            opp_action = self.opponent_agent.choose_action(state)
            self.engine.execute_action(opp_action)
        
        if state.game_over:
            return self._terminal_obs(), self._terminal_reward(), True, False, {}
        
        # Decode and execute Kano's action
        action = decode_action(action_id, state, player_id=0)
        result = self.engine.execute_action(action)
        
        # Let opponent respond if needed
        while state.active_player_id == 1 and not state.game_over:
            opp_action = self.opponent_agent.choose_action(state)
            self.engine.execute_action(opp_action)
        
        # Calculate reward
        reward = self._calculate_reward(result)
        
        # Check termination
        terminated = state.game_over
        truncated = state.turn_number > self.max_turns
        
        obs = encode_observation(state, player_id=0)
        return obs, reward, terminated, truncated, {}
    
    def _calculate_reward(self, result: ActionResult) -> float:
        """Reward shaping for deck optimization.
        
        Primary reward: +1 for winning, -1 for losing
        Shaping: small bonus for dealing damage, penalty per turn
        """
        state = self.engine.state
        
        if state.game_over:
            if state.winner == 0:
                # Won! Bonus inversely proportional to turn count
                return 10.0 / max(state.turn_number, 1)
            else:
                return -1.0
        
        reward = -0.01  # Small per-step penalty (encourage fast games)
        
        if result.damage_dealt > 0:
            reward += result.damage_dealt * 0.1
        if result.arcane_damage_dealt > 0:
            reward += result.arcane_damage_dealt * 0.1
        
        if not result.success:
            reward -= 0.5  # Penalty for invalid actions
        
        return reward
```

### Success Criteria:

#### Automated Verification:
- [x] `FaBEnv()` initializes with valid observation and action spaces
- [x] `reset()` returns a valid observation dict with correct shapes
- [x] `step()` accepts actions and returns (obs, reward, terminated, truncated, info)
- [x] Invalid actions result in negative reward but don't crash the env
- [x] Opponent heuristic runs automatically during opponent's turn
- [x] Games terminate correctly (hero dies or max turns exceeded)
- [x] Observation encoding produces values in [0, 1] range
- [x] `python -m pytest tests/test_env.py` passes

#### Manual Verification:
- [x] Run env with random Kano actions and verify games complete
- [x] Check that observations change meaningfully as the game progresses
- [x] Verify reward signal: positive for damage, negative for invalid actions, big reward for winning
- [x] Play several full games and check the game log makes sense

**Implementation Note**: After completing this phase and all automated verification passes, pause here for manual confirmation before proceeding.

---

## Phase 9: RL Training & Deck Optimization

### Overview
Implement the policy network, training loop, and deck optimization pipeline. The goal is to train an agent that plays Kano well, then use it to evaluate different deck compositions and find the optimal one.

### Changes Required:

#### 1. Policy Network (`fab_engine/agents/policy.py`)

```python
import torch
import torch.nn as nn
from gymnasium import spaces

class FaBPolicyNetwork(nn.Module):
    """Policy network for FaB environment with Dict observations."""
    
    def __init__(self, obs_space: spaces.Dict, action_dim: int = 20, 
                 hidden_size: int = 128):
        super().__init__()
        
        # Card encoder (shared for hand and arsenal cards)
        self.card_encoder = nn.Sequential(
            nn.Linear(10, 32),
            nn.ReLU(),
        )
        
        # Hand aggregator (processes all 4 hand cards)
        self.hand_aggregator = nn.Sequential(
            nn.Linear(32 * 4, 64),
            nn.ReLU(),
        )
        
        # Scalar features encoder
        # my_life, opp_life, resources, AP, turn, opp_hand, deck_size,
        # combat_power, combat_defense = 9 scalars
        # + phase (8) + opp_eq (4) = 21 scalar-like features
        self.scalar_encoder = nn.Sequential(
            nn.Linear(21, 32),
            nn.ReLU(),
        )
        
        # Combined network
        combined_dim = 64 + 32 + 32  # hand + arsenal + scalars
        self.combined = nn.Sequential(
            nn.Linear(combined_dim, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
        )
        
        # Policy head (actor)
        self.policy_head = nn.Linear(hidden_size, action_dim)
        
        # Value head (critic)
        self.value_head = nn.Linear(hidden_size, 1)
    
    def forward(self, obs: dict):
        """Forward pass with dict observation."""
        # Encode hand cards
        hand = obs["hand"]  # (batch, 4, 10)
        hand_encoded = self.card_encoder(hand)  # (batch, 4, 32)
        hand_flat = hand_encoded.reshape(-1, 4 * 32)  # (batch, 128)
        hand_features = self.hand_aggregator(hand_flat)  # (batch, 64)
        
        # Encode arsenal
        arsenal = obs["arsenal"]  # (batch, 1, 10)
        arsenal_encoded = self.card_encoder(arsenal.squeeze(1))  # (batch, 32)
        
        # Scalar features
        scalars = torch.cat([
            obs["my_life"], obs["opponent_life"], obs["resources"],
            obs["action_points"], obs["turn_number"], obs["phase"].float(),
            obs["opponent_equipment_defense"], obs["opponent_hand_size"],
            obs["deck_size"], obs["combat_attack_power"], obs["combat_total_defense"],
        ], dim=-1)
        scalar_features = self.scalar_encoder(scalars)  # (batch, 32)
        
        # Combine
        combined = torch.cat([hand_features, arsenal_encoded, scalar_features], dim=-1)
        features = self.combined(combined)
        
        logits = self.policy_head(features)
        value = self.value_head(features)
        
        return logits, value
```

#### 2. Training Loop (`fab_engine/agents/training.py`)

```python
def train_agent(kano_deck: List[CardTemplate],
                opponent_deck: List[CardTemplate],
                total_timesteps: int = 100000,
                verbose: bool = True) -> FaBPolicyNetwork:
    """Train RL agent using PPO on the FaB environment."""
    
    env = FaBEnv(kano_deck, opponent_deck)
    
    policy = FaBPolicyNetwork(env.observation_space, action_dim=20)
    optimizer = torch.optim.Adam(policy.parameters(), lr=3e-4)
    
    # ... PPO training loop (similar to existing code in fastest_to_40.py)
    # But adapted for Dict observation space
    
    return policy


def evaluate_deck(kano_deck: List[CardTemplate],
                  opponent_deck: List[CardTemplate],
                  policy: FaBPolicyNetwork,
                  num_games: int = 50) -> dict:
    """Evaluate a Kano deck against the opponent.
    
    Returns:
        dict with: win_rate, avg_turns_to_win, avg_damage_dealt, etc.
    """
    env = FaBEnv(kano_deck, opponent_deck)
    
    results = {"wins": 0, "losses": 0, "draws": 0, 
               "turns": [], "damage_dealt": []}
    
    for game in range(num_games):
        obs, _ = env.reset(seed=game)
        done = False
        
        while not done:
            action, _, _ = policy.get_action(obs, deterministic=True)
            obs, reward, terminated, truncated, _ = env.step(action)
            done = terminated or truncated
        
        state = env.engine.state
        if state.winner == 0:
            results["wins"] += 1
        elif state.winner == 1:
            results["losses"] += 1
        else:
            results["draws"] += 1
        
        results["turns"].append(state.turn_number)
        results["damage_dealt"].append(
            state.players[1].hero.life_total  # Remaining opponent life
        )
    
    results["win_rate"] = results["wins"] / num_games
    results["avg_turns"] = np.mean(results["turns"])
    
    return results


def optimize_deck(card_pool: List[CardTemplate],
                  opponent_deck: List[CardTemplate],
                  num_candidates: int = 100,
                  training_timesteps: int = 50000,
                  evaluation_games: int = 50,
                  top_k: int = 5) -> List[Tuple[dict, List[CardTemplate]]]:
    """Find optimal Kano deck composition.
    
    1. Generate candidate decks
    2. Train a base policy
    3. Evaluate all candidates with the policy
    4. Return top-k decks
    """
    # ... similar to existing optimize_deck() but for 2-player game
```

### Success Criteria:

#### Automated Verification:
- [x] Policy network forward pass works with Dict observations
- [x] Training loop runs for 1000 timesteps without errors
- [x] `evaluate_deck()` runs 10 games and returns valid results
- [x] `optimize_deck()` generates candidates, trains, evaluates, and returns top decks
- [x] Results include win_rate, avg_turns, and other metrics
- [ ] `python -m pytest tests/test_training.py` passes

#### Manual Verification:
- [ ] Monitor training progress: win rate should improve over time
- [ ] Compare trained agent vs random actions
- [ ] Review optimal deck composition: should be reasonable (mix of arcane damage + resource cards)
- [x] Win rate against heuristic opponent should be > 50% with a good deck and trained policy

**Implementation Note**: After completing this phase and all automated verification passes, pause here for manual confirmation before proceeding.

---

## Testing Strategy

### Unit Tests:
- **Card model**: CardTemplate creation, CardInstance mutations, keyword checking
- **Zone system**: Add/remove/draw operations, max size enforcement
- **Game engine**: Turn structure, pitching, playing cards, action points
- **Combat**: Damage calculation, defending, equipment effects
- **Abilities**: Arcane damage, Kano ability, go again, Arcane Barrier
- **Card loader**: Parsing, filtering, keyword extraction

### Integration Tests:
- Full game simulation with two heuristic players
- Full game with RL agent vs heuristic
- Deck evaluation pipeline

### Manual Testing Steps:
1. Run a full game with verbose logging and review each turn
2. Play several games with different deck compositions
3. Verify Kano's hero ability works correctly in various situations
4. Test edge cases: empty deck, 0 life exactly, equipment all destroyed

## Performance Considerations

- **Card loading**: Load and parse once at startup, cache CardTemplate objects
- **Game simulation speed**: Target ~100 games/second for deck evaluation
- **Memory**: CardTemplate objects are shared (immutable); only CardInstance carries mutable state
- **RL training**: Use batched environments if training is slow
- **Observation encoding**: Pre-allocate numpy arrays, avoid repeated allocation

## Migration Notes

- The existing `fastest_to_40.py` is preserved as-is (solitaire mode)
- The new `fab_engine/` package is independent
- `pyproject.toml` updated to include the new package
- No breaking changes to existing code

## References

- Original solitaire implementation: `fastest_to_40.py`
- Original spec: `SPEC.md`
- Previous plan: `thoughts/shared/plans/implementation-plan.md`
- FaB Comprehensive Rules: `en-fab-cr.txt`
- Card database: `~/repos/github/flesh-and-blood-cards/json/english/card.json`
- Kano (Young): 15 life, intellect 4, Wizard Hero
- Kano, Dracai of Aether (Adult): 30 life, intellect 4, Wizard Hero
