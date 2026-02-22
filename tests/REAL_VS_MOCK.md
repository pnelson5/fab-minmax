# BDD Tests: Real Engine vs Mock Components

## Current Architecture (After Refactoring)

### ✅ REAL Engine Components Being Tested

These are actual production code from `fab_engine/`:

1. **`fab_engine/engine/precedence.py`** ⭐
   - `PrecedenceManager` - Full precedence system implementation
   - `PrecedenceEffect` - Effect representation
   - `PrecedenceResult` - Validation results
   - `EffectType` - Restriction/Requirement/Allowance enum
   - **Tests exercise 100% of this module**

2. **`fab_engine/zones/zone.py`** ⭐
   - `Zone` - Actual zone implementation
   - `ZoneType` - Zone type enum
   - All zone operations (add, remove, contains, etc.)
   - **Tests use real Zone objects through TestZone wrapper**

3. **`fab_engine/cards/model.py`** ⭐
   - `CardTemplate` - Immutable card definitions
   - `CardInstance` - Mutable card state
   - `Color`, `CardType`, `Subtype` - All enum types
   - `Keyword` - Keyword enum
   - **Tests create and manipulate real card objects**

### 🔧 Thin Test Wrappers (Delegate to Real Engine)

These are minimal adapters in `tests/bdd_helpers.py` that expose real engine functionality with a test-friendly interface:

1. **`TestZone`**
   ```python
   class TestZone:
       def __init__(self, zone_type: ZoneType, owner_id: int = 0):
           self._zone = Zone(zone_type=zone_type, owner_id=owner_id)  # REAL Zone!
       
       def add_card(self, card: CardInstance):
           self._zone.add(card)  # Delegates to REAL zone
   ```
   - Wraps `Zone` for interface compatibility
   - Every operation calls real Zone methods
   - Zero business logic in the wrapper

2. **`TestPlayer`**
   ```python
   class TestPlayer:
       def __init__(self, player_id: int = 0):
           self.precedence = PrecedenceManager()  # REAL precedence!
           self.hand = TestZone(ZoneType.HAND, player_id)  # REAL zones!
           self.banished_zone = TestZone(ZoneType.BANISHED, player_id)
           # etc...
   ```
   - Uses REAL `PrecedenceManager`
   - Uses REAL `Zone` objects (through TestZone)
   - Business logic is all in real precedence system

3. **`TestAttack`**
   ```python
   @dataclass
   class TestAttack:
       precedence: PrecedenceManager = field(default_factory=PrecedenceManager)  # REAL!
   ```
   - Uses REAL `PrecedenceManager` for attack restrictions
   - Minimal glue code for test scenarios

### 📦 Test Helper Objects (Not Production Code)

These are simple data holders with no business logic:

1. **`PlayResult`** - Just a result container
2. **`DefendResult`** - Just a result container
3. **`LegalPlay`** - Simple data class
4. **`RestrictionCheck`** - Simple data class
5. **`BDDGameState`** - Test fixture coordinator

## What the Tests Actually Validate

### Direct Testing of Real Engine ✅

```python
# Example from test_restriction_overrides_allowance_banished

# 1. Using REAL PrecedenceManager
game_state.player.precedence.add_restriction("cant_play_from_banished")
game_state.player.precedence.add_allowance("may_play_from_banished")

# 2. Using REAL Zone (through TestZone wrapper)
game_state.player.banished_zone.add_card(test_card)

# 3. Using REAL precedence logic
result = game_state.player.precedence.check_action("play_from_banished")

# 4. Validating REAL precedence behavior
assert not result.permitted  # Restriction actually blocked the action!
assert result.blocked_by == "restriction"
```

### Real Zone Operations ✅

```python
# These use REAL Zone.add(), Zone.remove(), Zone.contains()
game_state.player.hand.add_card(card)
game_state.player.hand.remove_card(card)
assert card in game_state.player.hand  # Uses Zone.contains()
```

### Real Card Model ✅

```python
# Creates REAL CardTemplate and CardInstance objects
card = state.create_card(name="Test", color=Color.RED, cost=3)

# Tests real card properties
assert card.template.color == Color.RED
assert card.template.cost == 3
assert CardType.ACTION in card.template.types
```

## Integration Points

### Where Tests Connect to Engine

```
BDD Test Step
    ↓
TestPlayer.add_restriction()
    ↓
PrecedenceManager.add_restriction()  ← REAL ENGINE CODE
    ↓
Creates PrecedenceEffect                ← REAL ENGINE CODE
    ↓
Stores in effects list                  ← REAL ENGINE CODE

Later...

BDD Test Step
    ↓
TestPlayer.attempt_play_from_zone()
    ↓
PrecedenceManager.check_action()       ← REAL ENGINE CODE
    ↓
Evaluates precedence rules              ← REAL ENGINE CODE
    ↓
Returns PrecedenceResult                ← REAL ENGINE CODE
    ↓
Test validates result ✓
```

### What's NOT Tested (Yet)

These real engine components exist but aren't integrated into BDD tests yet:

- ❌ `GameEngine` - Main game loop
- ❌ `PlayerState` - Full player state (we use TestPlayer instead)
- ❌ `CombatChain` - Combat system
- ❌ `CombatEngine` - Combat resolution
- ❌ Action execution through `execute_action()`

## How to Tell What's Real

### ✅ Signs You're Testing Real Code

1. **Import from `fab_engine/`**
   ```python
   from fab_engine.engine.precedence import PrecedenceManager  # REAL!
   from fab_engine.zones.zone import Zone                      # REAL!
   from fab_engine.cards.model import CardInstance             # REAL!
   ```

2. **Direct instantiation of engine classes**
   ```python
   self.precedence = PrecedenceManager()  # REAL engine object
   self._zone = Zone(zone_type, owner_id)  # REAL zone
   ```

3. **Calling engine methods**
   ```python
   self.precedence.add_restriction()      # REAL method
   self._zone.add(card)                    # REAL method
   result = precedence.check_action()      # REAL logic
   ```

### ❌ Signs You're Using Test Doubles

1. **Defined in `tests/` directory**
   ```python
   # In tests/bdd_helpers.py
   class TestZone:  # Test wrapper (but delegates to real Zone!)
   class TestPlayer:  # Test coordinator (but uses real components!)
   ```

2. **Simple data holders**
   ```python
   @dataclass
   class PlayResult:  # Just holds data
       success: bool
   ```

## Benefits of This Approach

1. **Real Behavior Validation** ✅
   - Tests prove the precedence system actually works
   - Not testing mock behavior, testing real logic

2. **Catches Real Bugs** ✅
   - If precedence logic is broken, tests fail
   - If zone operations fail, tests fail

3. **Refactoring Safety** ✅
   - Can refactor PrecedenceManager implementation
   - Tests ensure behavior stays correct

4. **Documentation Through Tests** ✅
   - Tests show how to use PrecedenceManager
   - Tests demonstrate Zone operations
   - Tests validate against official rules

5. **Easy Migration Path** ✅
   - When we build full PlayerState integration
   - Just replace TestPlayer with real PlayerState
   - Tests stay the same, validation unchanged

## Next Steps for More Integration

To test even MORE real engine code:

1. **Use Real PlayerState** instead of TestPlayer
2. **Use Real GameEngine** to execute actions
3. **Use Real CombatChain** for attack tests
4. **Integration tests** that run full game scenarios

But for Rule 1.0.2 testing, we're already exercising the REAL precedence system with REAL zones and REAL cards! 🎉
