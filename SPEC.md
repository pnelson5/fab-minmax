# Fastest to 40 - Flesh and Blood Card Game Simulator

## Project Overview
A Python Jupyter notebook that simulates a "Fastest to 40" game mode using the Flesh and Blood TCG card pool. The goal is to determine the optimal deck composition to deal 40 damage in the minimum number of turns.

**Quick Stats**:
- **Card Pool**: 1,362 Common & Rare Wizard + Generic cards available to Kano
  - 912 Common cards
  - 450 Rare cards
  - ❌ Excluded: Super Rare, Majestic, Fabled, Legendary, Promo, Token
- **Objective**: Deal 40 damage in minimum turns
- **Deck Size**: Exactly 40 cards
- **Hero**: Young Kano (15 health, Intelligence 4, special hero ability)
- **Mode**: Solo optimization (no opponent, no blocking)

## Table of Contents
1. [Game Rules](#game-rules)
2. ["Fastest to 40" Game Mode Assumptions](#fastest-to-40-game-mode-assumptions)
3. [Data Sources](#data-sources)
4. [Game Mechanics to Simulate](#game-mechanics-to-simulate)
5. [Technical Requirements](#technical-requirements)
6. [Design Decisions](#design-decisions-needed)
7. [Success Metrics](#success-metrics)
8. [Deliverables](#deliverables)
9. [Open Questions](#open-questions)
10. [Next Steps](#next-steps)
11. [References](#references)

## Game Rules

### Core Objective
- Deal exactly 40 damage (or more) in as few turns as possible
- Construct a deck of exactly 40 cards
- No opponent (solitaire optimization)
- Unlimited resources (pitch/mana generation from hand)

### Hero Selection
- **Primary Hero**: Kano (Wizard class)
- **Card Pool**: Wizard class cards + Generic cards only
- Future expansion: Support other heroes with their respective card pools

### Deck Construction Rules
- **Deck Size**: Exactly 40 cards
- **Card Eligibility**: 
  - All **Common** Wizard class cards
  - All **Rare** Wizard class cards
  - All **Common** Generic class cards
  - All **Rare** Generic class cards
  - ❌ **Excluded rarities**: Super Rare, Majestic, Fabled, Legendary, Promo, Token
- **No duplicate restrictions** (can run multiple copies of same card)
- **Equipment/Weapons**: TBD - decide if hero can use equipment/weapons
- **Hero Card**: The hero card itself is not part of the 40-card deck

## "Fastest to 40" Game Mode Assumptions

This is a **solo optimization mode** distinct from standard FaB gameplay:

### Key Differences from Standard FaB
1. **No Opponent**: The goal is racing against turn count, not another player
2. **No Defense**: Cards with `defense` values have no blocking utility (no opponent to block)
3. **Simplified State**: No need to track life totals, equipment breaking, or blocking decisions
4. **Optimization Focus**: Find the deck that deals 40 damage in minimum turns with optimal play

### Assumed Mechanics

#### Turn Structure
- **Start of Game**: 
  - Hero: Young Kano (Intelligence 4 = hand size of 4)
  - Deck: 40 cards of your choice
  - Starting Hand: Draw 4 cards
  - Arsenal: Empty (TBD if we allow arsenal in this mode)

- **Each Turn**:
  1. **Draw Phase**: Draw up to hand size (4 cards)
  2. **Action Phase**: 
     - Play action cards for their effects
     - Generate resources by pitching cards
     - Use Kano's hero ability (3 resources for extra action)
     - Continue until out of resources/actions or choose to end
  3. **End Phase**: 
     - Cleanup, discard down to hand size if needed
     - Track total damage dealt this game
     - If damage >= 40, game ends

#### Resource System
- **Pitching**: Any card can be pitched from hand to generate resources equal to its pitch value
- **Resource Pool**: Resources do not carry over between turns (use them or lose them)
- **Pitch Value**:
  - Red cards: 1 resource
  - Yellow cards: 2 resources
  - Blue cards: 3 resources
  - Colorless/Equipment: 0 resources (cannot be pitched)
- **Pitch Zone Mechanics**:
  1. **During Turn**: Pitched cards go to the pitch zone (temporary holding area)
  2. **End Phase**: All cards in pitch zone are returned to the **bottom of the deck**
  3. **Ordering**: Player chooses the **order** when returning multiple pitched cards
  4. **Cycling**: Cards will eventually be drawn again after cycling through the deck

#### Damage Calculation
- **Attack Damage**: `power` value of Attack cards
- **Arcane Damage**: `arcane` value of spells
- **Bonus Damage**: From card abilities (e.g., "deal +X damage", "your next attack deals +Y")
- **Total**: Sum of all damage dealt across all turns

#### Information Mechanics
- **Opt X**: Look at top X cards, put one in hand, rest on bottom in chosen order
  - Only way to see upcoming cards before drawing
  - Examples: Opt 1, Opt 2, Opt 3 effects
- **Deck Cycling**: As cards are pitched to bottom, deck gradually cycles
  - First cycle: Random order (shuffled)
  - Subsequent cycles: Semi-ordered based on pitch decisions
- **Kano Hero Ability**: Reveals top card but doesn't show full deck state

#### Card Availability
- **Shuffled Deck**: Deck is shuffled before play starts
- **No Perfect Information**: Cannot see deck order on first cycle through
- **Card Knowledge**: Only know cards currently in hand (Intelligence 4 = hand size)
- **No Mulligan**: Start with first 4 cards drawn
- **No Sideboard**: 40 cards only
- **Pitch Pile Management**: Pitched cards go to bottom of deck, player chooses order

### Simplified Rules
- Ignore defense values on cards
- Ignore ward, dominate, and defensive keywords
- Ignore equipment durability/destroy mechanics
- Ignore banish pile mechanics unless specifically relevant (e.g., Kano's ability)
- All "target hero" effects target the imaginary opponent (damage is dealt)
- "Target ally" effects may have no valid target or TBD behavior

### Game State Tracking
To simulate accurately, we must track:

#### Deck State
- **Deck**: Ordered list of remaining cards (top = next draw)
- **Position**: Index of next card to draw
- **Cycling**: When deck empties, reshuffle or continue with bottom cards?
  - **Clarification needed**: In real FaB, when deck runs out, you reshuffle discard into deck
  - **But**: Our pitched cards go to bottom, so we need to clarify cycling behavior

#### Hand State
- **Cards in Hand**: Current hand (max 4 cards for Kano)
- **Resources Available**: Sum of pitch values of cards that could be pitched
- **Cards Played This Turn**: Track for "once per turn" effects

#### Card Location Tracking
Each card has one of these locations:
- **Deck**: Not yet drawn (top = next draw)
- **Hand**: Currently held
- **Pitch Zone**: Cards pitched this turn (temporary, returned to deck at end phase)
- **In Play**: Cards currently resolving/active
- **Banished**: Cards removed by Kano's ability or other effects (removed from game)
- **Discard**: Cards played/resolved (TBD if we need this)

#### Turn Flow & Card Movement
1. **Start of Turn**: Draw cards to fill hand size
2. **Action Phase**: 
   - Play cards (move Hand → In Play → Discard/Banished)
   - Pitch cards (move Hand → Pitch Zone)
3. **End Phase**: 
   - Return Pitch Zone cards to bottom of deck in chosen order
   - Discard down to hand size if needed
   - Clear "once per turn" effects

#### Information State
- **Known Cards**: Cards in hand + cards seen via Opt effects
- **Unknown Cards**: Rest of deck (random order on first cycle)
- **Partial Knowledge**: Cards seen previously but not current location

**Note**: This is significantly more complex than perfect-information simulation. We'll need to decide how to handle the stochastic nature.

## Data Sources

### Card Pool Composition
**Total Kano-Eligible Cards**: 1,362 cards (Common & Rare only, Wizard + Generic, excluding hero cards)

**Top Card Categories** (Common & Rare only):
1. **Generic Attack Actions**: 621 cards - Primary damage source via `power`
2. **Generic Actions**: 140 cards - Utility, draw, resource generation
3. **Wizard Actions**: 98 cards - Arcane damage, spell synergies
4. **Generic Items**: ~90 cards - Equipment-like effects, TBD usefulness
5. **Generic Instants**: ~60 cards - Kano hero ability synergy

**Excluded Cards** (not available):
- 207 Majestic cards (often strongest effects)
- 227 Promo cards
- 21 Super Rare cards
- 17 Legendary cards
- 16 Fabled cards
- 30 Token cards

**Card Distribution by Type**:
- **Attack Cards** (Generic): High damage potential via `power` value
- **Wizard Spells** (with `arcane`): Direct arcane damage, no blocking
- **Action Cards**: Mix of damage and utility
- **Defense Reactions**: May have limited value in solo mode
- **Equipment**: ~220 equipment cards across all slots (chest, head, arms, legs)

### Damage Sources Analysis
- **Physical Attacks**: `power` value on Attack cards
- **Arcane Damage**: `arcane` value on Wizard spells
- **Effect Damage**: From card text (e.g., "deal X damage")
- **Buffed Damage**: Multiplier effects (e.g., Aether Flare buffing next spell)

### Resource Generation
- **Pitch Values**: 
  - Blue cards: 3 resources (most efficient)
  - Yellow cards: 2 resources
  - Red cards: 1 resource (least efficient but often highest damage)

**Strategic Insight**: Optimal deck likely mixes high-pitch Blue cards (to generate resources) with high-damage Red cards (to spend resources on).

### Impact of Common/Rare Restriction

**What We're Losing**:
- **Majestic cards** (207): Often the most powerful spells and combos
- **Legendary cards** (17): Unique, game-defining effects
- **Fabled cards** (16): Extremely rare and powerful
- **Super Rare** (21): Strong synergistic pieces
- **Total**: 261 high-power cards removed from pool

**What Remains** (1,362 cards):
- Solid foundation of Common cards (912)
- Useful Rare cards (450) with decent effects
- Still plenty of "go again" and arcane damage options
- Resource generation (pitch) cards intact

**Strategic Adjustment**:
- Focus shifts to efficiency and consistency over raw power
- Common arcane spells like Aether Dart and Aether Hail remain viable
- Generic attack cards still provide physical damage options
- Deck must rely more on quantity of plays rather than powerful single cards

**Expected Impact on "Fastest to 40"**:
- More turns likely required (fewer explosive combos)
- Deck building emphasizes resource efficiency and card draw
- "Go again" chains become even more critical
- Kano's hero ability (3 resources for extra action) is now relatively more valuable

### Impact of Imperfect Information & Deck Cycling

**What This Changes**:
1. **No longer perfect play**: Cannot pre-calculate optimal sequence because we don't know draw order
2. **Strategic decisions matter**: Choosing which cards to pitch and in what order affects future turns
3. **Opt cards gain value**: Information about upcoming draws is now scarce and valuable
4. **Multiple deck cycles**: Cards return to deck, so we might see the same cards multiple times
5. **Variance increases**: Random shuffle means some games are better/worse than others for same deck

**Simulation Complexity**:
- Need to run **multiple iterations** per deck to account for shuffle variance
- Optimize for **expected value** (average turns across many shuffles)
- Consider **worst-case scenarios** (bad starting hands, poor draws)
- Track **deck state** across cycles (which cards are where)

**Optimization Challenges**:
- Can't use deterministic optimization (depends on random shuffle)
- Need Monte Carlo simulation or similar approach
- Balance between greedy play (maximize this turn) and setup (optimize future turns)
- Deck composition must be robust across different draw orders

### Card Pool Location
- **Path**: `~/repos/github/flesh-and-blood-cards/`
- **Primary Data**: `/json/english/card.json`
- **Schema Documentation**: Available in `/documentation/json-schemas.md`

### Key Card Attributes
From the JSON schema, each card contains:
- `name`: Card name
- `types`: Array of types (e.g., ["Wizard", "Action", "Attack"])
- `color`: Red/Yellow/Blue (pitch value indicator)
- `pitch`: Resource value (1/2/3)
- `cost`: Resource cost to play the card
- `power`: Attack damage value
- `defense`: Defense value (for blocking)
- `functional_text_plain`: Card abilities and effects
- `card_keywords`: Special keywords (e.g., "Go again", "Dominate")
- `arcane`: Arcane damage value (for Wizard spells)

### Card Categories
1. **Hero Cards**: `types` contains "Hero"
2. **Attack Cards**: `types` contains "Attack" (have `power` value)
3. **Action Cards**: `types` contains "Action" (may or may not attack)
4. **Instant Cards**: `types` contains "Instant"
5. **Equipment**: `types` contains "Equipment"
6. **Auras**: `types` contains "Aura"

## Game Mechanics to Simulate

### Turn Structure
1. **Start of Turn**: Draw up to hand size (unclear - needs decision)
2. **Resource Phase**: Pitch cards to generate resources
3. **Action Phase**: Play cards that cost resources
4. **Combat Phase**: Resolve attacks and deal damage
5. **End of Turn**: Cleanup effects

### Key Mechanics

#### Pitch System
- Red cards: Pitch 1 resource
- Yellow cards: Pitch 2 resources  
- Blue cards: Pitch 3 resources
- Cards can be pitched for resources OR played for their effect (not both)

#### Combat
- Attack cards have a `power` value = base damage
- Some cards have "go again" allowing multiple attacks per turn
- Damage accumulates toward the 40 damage goal
- No blocking/defense in this solo mode

#### Arcane Damage
- Wizard-specific mechanic
- Cards may have `arcane` damage value
- Arcane damage bypasses normal combat rules
- Special Kano hero ability may interact with arcane

#### Special Keywords to Consider
- **Go again**: Allows you to play another action after this one
- **Opt X**: Look at top X cards, put one in hand, rest on bottom
- **Dominate**: Cannot be defended by certain cards (not relevant in solo)
- **Ward X**: Protection mechanic (not relevant for offense)
- **Instant**: Can be played at different timing windows

### Kano-Specific Mechanics

#### Kano Variants
**Young Kano** (`Kano`)
- **Health**: 15
- **Intelligence**: 4 (hand size)
- **Legal Formats**: Blitz, Commoner, Silver Age
- **Hero Ability**: Instant - Pay {r}{r}{r}: Look at top card of deck. If it's a 'non-attack' action card, you may banish it. If you do, you may play it this turn as though it were an instant.

**Kano, Dracai of Aether**
- **Health**: 30
- **Intelligence**: 4 (hand size)
- **Legal Formats**: Classic Constructed
- **Hero Ability**: Same as Young Kano

#### Hero Ability Analysis
**Cost**: 3 resources ({r}{r}{r})
**Effect**: 
1. Look at top card of deck
2. If non-attack action card, may banish it
3. If banished, may play it this turn as an instant

**Strategic Implications**:
- Can generate additional cards/actions per turn beyond hand limit
- Synergizes with arcane damage cards played at instant speed
- 3 resource cost is significant - must balance with other actions
- Works best with high-impact non-attack actions

#### Arcane Damage
- **Source**: Wizard spells with `arcane` value
- **Examples**: 
  - Aether Dart: 0 cost, 1-3 arcane damage depending on pitch
  - Aether Hail: 1 cost, 3-4 arcane damage
  - Aether Flare: 1 cost, 1-3 arcane + bonus to next arcane spell
- **Mechanics**: Direct damage that bypasses combat
- **Kano Synergy**: Can use hero ability to cast additional arcane spells at instant speed

#### Resource/Pitch Strategy
- **Blue Cards** (pitch 3): Best for pitching to generate resources
- **Red Cards** (pitch 1): High arcane damage but poor for pitching
- **Yellow Cards** (pitch 2): Balanced option
- **Optimal Strategy**: Mix of high-pitch cards to fuel casting high-damage low-pitch cards

## Technical Requirements

### Jupyter Notebook Structure
1. **Data Loading Section**
   - Load and parse card.json
   - Filter for Wizard + Generic cards
   - **Filter for Common (C) and Rare (R) rarities only**
   - Create card database/dataframe
   - Verify card count: ~1,362 eligible cards

2. **Card Analysis Section**
   - Damage-per-resource efficiency calculations
   - "Go again" chain analysis
   - Combo identification

3. **Deck Building Section**
   - Constraint: exactly 40 cards
   - Optimization objective: minimize turns to 40 damage
   - Generate candidate decks

4. **Simulation Engine**
   - Turn-by-turn game state
   - Resource management
   - Action sequencing
   - Damage tracking

5. **Optimization Module**
   - Algorithm TBD (genetic algorithm, integer programming, exhaustive search, etc.)
   - Objective function: minimize expected turns to 40 damage
   - Constraints: deck composition rules

6. **Results & Visualization**
   - Optimal deck list
   - Turn-by-turn breakdown
   - Damage curves
   - Statistical analysis (if probabilistic)

### Python Libraries
- **pandas**: Data manipulation
- **numpy**: Numerical operations
- **matplotlib/seaborn**: Visualization
- **json**: Parse card data
- **Optional**: 
  - `scipy.optimize`: For optimization algorithms
  - `pulp` or `cvxpy`: For integer/linear programming
  - `networkx`: For game state graphs
  - **[PufferLib](https://github.com/PufferAI/PufferLib)**: For reinforcement learning environment and training
    - Provides fast parallel environment vectorization
    - Optimized for RL training loops
    - Could be used to train an RL agent to play optimal turns

## Design Decisions Needed

### 1. Hand Size & Drawing
- [ ] What is the starting hand size?
- [ ] Do we draw cards each turn? How many?
- [ ] Is there a maximum hand size?
- **Proposal**: Start with infinite hand (draw entire deck turn 1) for simplest case

### 2. Arsenal & Hero Ability
- [ ] Can cards be placed in "Arsenal" (delayed play)?
- [x] What is Kano's hero ability exactly? **RESOLVED**: Instant - 3 resources to look at/banish/play top card if non-attack action
- [ ] Does the hero ability cost resources or have uses per turn? **ANSWERED**: Costs 3 resources, no usage limit
- [ ] Should we allow arsenal in solo mode? **Proposal**: Start without arsenal for simplicity
- **Proposal**: Start with Young Kano (15 health, Blitz format) - health is irrelevant for damage race anyway

### 3. Equipment & Weapons
- [ ] Can Kano use weapons/equipment?
- [ ] Do weapons add damage to attacks?
- [ ] Equipment effects on resource generation?
- **Proposal**: Start without equipment, add later if needed

### 4. Card Restrictions
- [ ] Allow duplicate cards (unlimited copies)?
- [ ] Any legendary restrictions (max 1 copy)?
- **Proposal**: Allow unlimited duplicates for first iteration

### 5. Deterministic vs. Stochastic ⭐ **DECIDED**
- [x] Is card draw order random or optimized? **DECIDED**: Deck is shuffled (random) at game start
- [x] Do we simulate variance or find perfect-information optimal? **DECIDED**: Imperfect information on first cycle through deck
- **Card Flow**: 
  - Cards pitched go to bottom of deck (player chooses order)
  - Only Opt effects reveal upcoming cards
  - After first full cycle, deck state is influenced by pitch decisions
- **Simulation Approach**: Need to handle:
  1. Random initial shuffle
  2. Partial information (only know hand, not deck)
  3. Strategic ordering of pitched cards on bottom
  4. Multiple deck cycles possible over the game

### 6. Turn Limits
- [ ] Is there a maximum number of turns to consider?
- [ ] What happens if 40 damage is impossible?
- **Proposal**: No limit, but flag decks that can't reach 40

### 7. Card Rarity Restriction ⭐ **DECIDED**
- [x] Which card rarities are allowed? **DECIDED**: Common (C) and Rare (R) only
- [x] Which rarities are excluded? **DECIDED**: Super Rare (S), Majestic (M), Fabled (F), Legendary (L), Promo (P), Token (T), Basic (B), Marvel (V)
- **Rationale**: Creates a more constrained optimization problem, focuses on efficiency over raw power
- **Impact**: Reduces card pool from 1,876 to 1,362 cards (27.4% reduction)
- **Expected Outcome**: More turns required, emphasizes resource efficiency and card draw over powerful single cards

## Success Metrics

### Primary Metric
- **Minimum turns to 40 damage** with optimal play

### Secondary Metrics
- **Average damage per turn**
- **Resource efficiency** (damage per resource spent)
- **Consistency** (variance in turns required across different draw orders)
- **Deck diversity** (number of unique cards vs. duplicates)

## Deliverables

### Phase 1: Foundation
- [ ] Load card data into pandas DataFrame
- [ ] Filter Kano-eligible cards (Wizard + Generic)
- [ ] Basic card statistics and exploration
- [x] Document Kano's hero ability and starting conditions

### Phase 2: Simulation Engine
- [ ] Implement turn structure
- [ ] Resource/pitch system
- [ ] Action sequencing (with "go again" chains)
- [ ] Damage tracking

### Phase 3: Deck Building
- [ ] Brute force small deck search (e.g., 10 cards)
- [ ] Greedy heuristic deck builder
- [ ] Full 40-card optimization

### Phase 4: Analysis & Visualization
- [ ] Optimal deck report
- [ ] Turn-by-turn gameplay breakdown
- [ ] Comparison of different deck strategies
- [ ] Visualizations of damage curves

### Phase 5: Extensions
- [ ] Support for other heroes
- [ ] Equipment/weapon integration
- [ ] Probabilistic simulation with variance
- [ ] Combo detection and highlighting

## Open Questions

### Resolved ✓
1. ~~**Kano's Hero Ability**: What exactly does Kano's hero card do?~~ **RESOLVED**: Instant ability costing 3 resources to potentially play an extra non-attack action card per turn.
2. ~~**Card Rarity Restriction**: Which rarities are allowed?~~ **RESOLVED**: Common and Rare only. Super Rare, Majestic, Fabled, Legendary, Promo, and Token cards are excluded.
3. ~~**Legendary Cards**: Are there legendary cards with special restrictions?~~ **RESOLVED**: Not relevant - Legendary cards are excluded from the pool.
4. ~~**Card Availability & Information**: Do we have perfect information?~~ **RESOLVED**: Deck is shuffled (no perfect info). Only Opt effects reveal cards. Pitched cards go to bottom in player-chosen order.

### Still Open
5. **"Go Again" Chains**: How many actions can chain in one turn? Is there a limit? **Answer**: In real FaB, no limit if you keep playing "go again" cards.

6. **Instant Speed**: Do instants provide value in a solo damage race? **Analysis**: Only if they deal damage AND we have Kano's hero ability to play them at instant speed, OR if they synergize with other cards.

7. **Banished/Exiled**: Do any cards get removed from game? Does this affect strategy? **Analysis**: Kano's ability banishes cards - these may or may not return to the game. Need to clarify if banished cards count as "removed from game" or can be recycled.

8. **Multi-card Combos**: Are there cards that explicitly combo with each other for bonus damage? **Needs research**: Look for cards like "Aether Flare" which buffs the next arcane spell.

9. **Optimization Approach**: How do we handle imperfect information?
   - Simulate multiple games with different shuffles?
   - Calculate expected value across random draws?
   - Find best strategy given information constraints?

## Strategic Hypotheses

### Hypothesis 1: Arcane-Heavy Deck
**Theory**: Wizard arcane spells are the most efficient damage source because:
- No blocking (opponent doesn't exist in solo mode anyway)
- Kano's hero ability provides extra arcane spells per turn
- High arcane-to-cost ratios on cards like Aether Hail (4 arcane for 1 cost)

### Hypothesis 2: Pitch/Damage Efficiency
**Theory**: Optimal ratio is 1 Blue (3 pitch) : 1 Red (1 pitch, high damage):
- Pitch 1 Blue = 3 resources
- Play 1 Red attack (1 cost) = 4-6+ damage
- Kano ability adds another action for 3 resources

### Hypothesis 3: "Go Again" Chains
**Theory**: Cards with "go again" are extremely valuable:
- Can play multiple attacks per turn
- Extends the damage ceiling of a single turn
- Worth lower base damage if they enable chains

### Hypothesis 4: Kano Ability Synergy
**Theory**: Deck should maximize non-attack actions for Kano's hero ability:
- Instant-speed arcane spells at instant speed = extra damage
- Draw/filtering effects to improve hand quality
- 3-resource cost must be balanced with main phase actions

### Hypothesis 5: Deck Cycling & Pitch Ordering
**Theory**: Order of pitched cards matters for future turns:
- Place high-value cards at bottom when you need them next cycle
- Keep "bad" draws at top of deck to pitch immediately when drawn
- Opt effects become valuable for deck manipulation and information
- Second cycle through deck has more predictable order than first

### Hypothesis 6: Opt Card Value
**Theory**: Cards with "Opt X" are more valuable than raw stats suggest:
- Opt provides information about upcoming draws
- Can put good cards in hand, bad cards on bottom
- Deck manipulation improves consistency over multiple turns
- Example: Opt 2 effectively draws 1 card + 1 card knowledge

## Next Steps

### Immediate Actions
1. **Create Jupyter Notebook**
   - Set up environment with pandas, numpy, matplotlib
   - Load card.json and filter for Kano-eligible cards
   - Create initial data exploration

2. **Card Analysis**
   - Identify top damage-to-cost ratio cards
   - Find all "go again" cards
   - Catalog arcane damage cards
   - Calculate pitch efficiency metrics

3. **Simple Simulation**
   - Single-turn damage calculation
   - Test with top 10-20 cards
   - Validate resource math

### Medium-Term
4. **Multi-Turn Simulation**
   - Track deck state across turns
   - Implement drawing and hand management
   - Calculate cumulative damage

5. **Deck Optimization**
   - Integer programming formulation
   - Greedy heuristic approach
   - Compare strategies

6. **Results Analysis**
   - Optimal deck list
   - Turn-by-turn breakdown
   - Damage curve visualization
   - Sensitivity analysis

### Long-Term Extensions
- [ ] Probabilistic simulation (random draw order)
- [ ] Equipment/weapon integration
- [ ] Support other heroes (Dromai, Fai, etc.)
- [ ] Combo detection engine
- [ ] Web interface for deck building

## References

- **Card Database**: `~/repos/github/flesh-and-blood-cards/json/english/card.json`
- **FaB Official Site**: https://fabtcg.com/
- **Documentation**: `~/repos/github/flesh-and-blood-cards/documentation/`
- **Schema**: JSON schema files in `/json-schema/` directory
- **Comprehensive Rules**: `en-fab-cr.txt`
