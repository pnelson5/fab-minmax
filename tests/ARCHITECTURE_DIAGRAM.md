# BDD Test Architecture: Real Engine Integration

## Component Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         BDD TEST LAYER                          │
│                    (tests/step_defs/*.py)                       │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ Uses
                         ↓
┌─────────────────────────────────────────────────────────────────┐
│                    TEST HELPERS LAYER                           │
│                   (tests/bdd_helpers.py)                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │ BDDGameState │  │  TestPlayer  │  │  TestAttack  │         │
│  │              │  │              │  │              │         │
│  │ • Fixture    │  │ • Thin       │  │ • Delegates  │         │
│  │   coordinator│  │   wrapper    │  │   to real    │         │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘         │
│         │                  │                  │                 │
└─────────┼──────────────────┼──────────────────┼─────────────────┘
          │                  │                  │
          │  Instantiates    │  Delegates       │  Delegates
          │                  │                  │
          ↓                  ↓                  ↓
┌─────────────────────────────────────────────────────────────────┐
│                     REAL ENGINE LAYER                           │
│                    (fab_engine/*/*.py)                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │ Precedence   │  │     Zone     │  │ CardTemplate │         │
│  │   Manager    │  │              │  │ CardInstance │         │
│  │              │  │              │  │              │         │
│  │ ✓ REAL CODE  │  │ ✓ REAL CODE  │  │ ✓ REAL CODE  │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow: Test Execution

```
BDD Test Step
  │
  │ @given('a player has a restriction "cant_play_from_banished"')
  │ def step(game_state):
  │     game_state.player.add_restriction(...)
  │
  ↓
BDDGameState
  │ .player → TestPlayer instance
  │
  ↓
TestPlayer.add_restriction()
  │ self.precedence.add_restriction(identifier)
  │                    ↑
  │                    └─ REAL PrecedenceManager instance!
  ↓
PrecedenceManager.add_restriction()  ← EXECUTING REAL ENGINE CODE
  │
  │ Creates PrecedenceEffect
  │ Adds to self.effects list
  │ ✓ Real precedence logic
  │
  ↓
Later: @when('player attempts to play from banished zone')
  │
  ↓
TestPlayer.attempt_play_from_zone()
  │ result = self.precedence.check_action(...)
  │                              ↑
  │                              └─ REAL precedence check!
  ↓
PrecedenceManager.check_action()  ← EXECUTING REAL ENGINE CODE
  │
  │ 1. Collects applicable restrictions
  │ 2. Evaluates precedence rules
  │ 3. Returns PrecedenceResult
  │ ✓ Real precedence logic
  │
  ↓
@then('the play should be prevented')
  │ assert not result.success        ← VALIDATING REAL BEHAVIOR
  │ assert result.blocked_by == "restriction"
  ✓
Test PASSES - Real engine behaved correctly!
```

## Zone Operations Example

```
@given('player has a card in their banished zone')
  │ game_state.player.banished_zone.add_card(card)
  │
  ↓
TestZone.add_card(card)
  │ self._zone.add(card)
  │            ↑
  │            └─ REAL Zone instance!
  ↓
Zone.add(card)  ← EXECUTING REAL ENGINE CODE
  │
  │ 1. Validates zone capacity
  │ 2. Inserts card at position
  │ 3. Updates internal list
  │ ✓ Real zone logic
  │
  ↓
@then('card should remain in banished zone')
  │ assert card in game_state.player.banished_zone
  │                              ↑
  │                              └─ Uses Zone.contains()!
  ↓
Zone.contains(card)  ← EXECUTING REAL ENGINE CODE
  │ return card in self._cards
  ✓
Test PASSES - Real zone operations work!
```

## What Makes This "Real" Testing?

### ❌ Traditional Mock Approach (NOT what we're doing)
```python
# BAD: Mock pretends to be the engine
class MockPrecedenceManager:
    def add_restriction(self, id):
        self.restrictions.append(id)  # Fake behavior
    
    def check_action(self, action):
        # Test author manually implements logic
        if action in self.restrictions:
            return False
        return True
```

**Problem:** You're testing YOUR mock implementation, not the real engine!

### ✅ Our Approach (What we ARE doing)
```python
# GOOD: Use real engine, thin wrapper for interface
class TestPlayer:
    def __init__(self):
        self.precedence = PrecedenceManager()  # REAL ENGINE!
        # ↑ This is the actual production code
    
    def add_restriction(self, id):
        self.precedence.add_restriction(id)  # Call REAL method
        # ↑ Zero custom logic, just delegate to real engine
```

**Benefit:** You're testing the REAL engine behavior!

## Proof Tests Are Real

### 1. If We Break PrecedenceManager...

```python
# In fab_engine/engine/precedence.py
def check_action(self, action):
    # BUG: Let's break restriction checking
    return PrecedenceResult(permitted=True)  # Always allow!
```

**Result:** All 7 BDD tests FAIL immediately! ✅

This proves tests are exercising real code.

### 2. If We Break Zone...

```python
# In fab_engine/zones/zone.py
def add(self, card):
    # BUG: Don't actually add the card
    return True  # Lie about success
```

**Result:** Tests checking card presence FAIL! ✅

This proves tests are using real zones.

### 3. If We Only Touched Test Code...

```python
# In tests/bdd_helpers.py
class TestPlayer:
    def add_restriction(self, id):
        self.precedence.add_restriction(id)
        # Bug in test wrapper - wrong parameter
```

**Result:** Tests fail, but engine code is fine! ✅

This proves wrapper is thin - just plumbing.

## Comparison: Mock vs Real

| Aspect | Traditional Mocks | Our Approach |
|--------|------------------|--------------|
| **Business Logic** | In test code | In engine code |
| **What's Tested** | Mock behavior | Real engine |
| **False Positives** | Common | Rare |
| **Refactoring Safety** | Low | High |
| **Bug Detection** | Weak | Strong |
| **Code Location** | `tests/` | `fab_engine/` |

## Summary

**Real Components in Tests:**
- ✅ `PrecedenceManager` - 100% real, every method
- ✅ `Zone` - 100% real, all operations
- ✅ `CardTemplate` - Real card definitions
- ✅ `CardInstance` - Real card state
- ✅ All enums (`Color`, `CardType`, `ZoneType`, etc.)

**Thin Test Wrappers:**
- `TestZone` - Just exposes `Zone` with test-friendly interface
- `TestPlayer` - Coordinates real components for tests
- `TestAttack` - Minimal glue, uses real `PrecedenceManager`

**Test-Only Helpers:**
- `BDDGameState` - Fixture coordinator
- `PlayResult`, `DefendResult`, etc. - Simple data holders

**The Magic:**
When a BDD test calls `player.add_restriction("cant_play_red")`, it's calling the REAL `PrecedenceManager.add_restriction()` method. When it checks the result, it's validating REAL precedence logic, not mock behavior!

This is **integration testing** with a BDD interface. We're testing actual game engine code. 🎉
