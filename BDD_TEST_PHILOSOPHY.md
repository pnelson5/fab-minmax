# BDD Test Philosophy: Specification First, Implementation Later

## The Core Principle

**BDD tests are SPECIFICATIONS, not implementations.**

When you run `/implement-bdd-rule`, you are writing a CONTRACT that the engine must fulfill. You are NOT implementing the engine to fulfill that contract.

## The Two-Phase Approach

### Phase 1: Write Test Specifications (This Command)
```bash
/implement-bdd-rule 1.1 Players
```

**What happens:**
1. Read comprehensive rules for section 1.1
2. Write Gherkin scenarios based on rules
3. Write step definitions using test helpers
4. Run tests - they FAIL ✅
5. Document what engine features are needed
6. Mark section complete
7. **Move on to next rule**

**Result:** Test spec is written, tests are red (expected)

### Phase 2: Implement Engine Features (Separate Task)
```bash
/implement-engine-feature 1.1
# (This command doesn't exist yet, but will be created later)
```

**What happens:**
1. Read the test specifications
2. Read documented engine requirements
3. Implement engine features in `fab_engine/`
4. Run tests - they PASS ✅
5. Refactor if needed
6. Mark engine implementation complete

**Result:** Engine features exist, tests are green

## Why This Approach?

### ✅ Benefits of Separation

1. **Speed**: Can rapidly write all test specs without getting bogged down in implementation
2. **Clarity**: Tests remain pure specifications, not influenced by implementation details
3. **Coverage**: Can ensure 100% rule coverage before any engine work
4. **Flexibility**: Can batch engine work (e.g., implement all Zone features together)
5. **Quality**: Tests won't accidentally accommodate buggy engine behavior

### ❌ Problems with Immediate Implementation

1. **Slow**: Each rule takes 10x longer (write test + implement + debug)
2. **Scope Creep**: Easy to rush engine implementation
3. **Contamination**: Tests might be written to match broken engine
4. **Distraction**: Lose focus on comprehensive rule coverage
5. **Inefficiency**: Can't optimize engine for multiple related rules

## The Test Failure Mindset

### When Writing Tests (Phase 1)

```python
# You write this test:
def test_player_has_card_pool(game_state):
    assert game_state.player.card_pool is not None
    
# Test runs and fails:
AttributeError: 'TestPlayer' has no attribute 'card_pool'

# Your response:
✅ "Perfect! Test is written correctly. The engine needs Player.card_pool."
❌ "Oh no, a failure! Let me implement Player.card_pool right now."
```

### Good Failures vs Bad Failures

| Failure Type | Example | Your Response |
|-------------|---------|---------------|
| **Good** | `AttributeError: 'Player' has no attribute 'card_pool'` | ✅ Document, move on |
| **Good** | `NotImplementedError: Zone.move_card()` | ✅ Document, move on |
| **Good** | `AssertionError: Restriction didn't block play` | ✅ Document, move on |
| **Bad** | `SyntaxError: invalid syntax` | ❌ Fix test code |
| **Bad** | `ImportError: cannot import CardType` | ❌ Fix test code |
| **Bad** | `NameError: 'game_state' is not defined` | ❌ Fix test code |

## The Golden Rules

### DO ✅
1. Write tests that match the comprehensive rules exactly
2. Use real engine components via `bdd_helpers.py`
3. Fix broken test code (syntax, imports, fixtures)
4. Add generic helper methods to `bdd_helpers.py`
5. Document what engine features are needed
6. Mark tests complete when they fail for the right reasons
7. Move on to the next rule

### DON'T ❌
1. Implement engine features in `fab_engine/` during test writing
2. Try to make tests pass by writing engine code
3. Modify engine behavior to make tests easier
4. Skip documenting required engine features
5. Feel bad about red tests (they're supposed to be red!)
6. Implement engine features "just to see if the test is right"
7. Get distracted by implementation details

## Handling Edge Cases

### "But I found a bug in the engine while writing tests!"

**If it's clearly a bug** (not missing features):
- Document it: `# BUG: PrecedenceManager.has_restriction() returns wrong type`
- Mark test as failing due to bug
- Move on - bugs will be fixed during implementation phase

**If you're not sure** it's a bug:
- Assume it's a missing feature
- Document what you expected
- Move on

### "The helper in bdd_helpers.py doesn't do what I need"

**If it's test infrastructure** (not engine logic):
- ✅ OK to add/modify: `TestPlayer.clear_restrictions()`
- ✅ OK to add/modify: `BDDGameState.create_card()`
- ❌ NOT OK to add: Full game logic in helpers

**Rule of thumb**: 
- Helpers are THIN WRAPPERS for tests, not implementations
- If you're writing complex logic, it belongs in `fab_engine/`

### "All my tests are failing and I feel unproductive"

**This is the GOAL!** 

Red tests = Progress! You're documenting what the engine MUST do.

Think of it like this:
- 0 tests written, 0 tests failing = 0% progress
- 50 tests written, 50 tests failing = 50% specification complete ✅
- 50 tests written, 0 tests failing = Either done OR tests are wrong

## The Ralph Loop in Practice

### Rapid Specification Phase (Weeks 1-2)
```bash
/implement-bdd-rule 1.1 Players      # 7 tests written, 7 red ✅
/implement-bdd-rule 1.2 Objects      # 5 tests written, 5 red ✅
/implement-bdd-rule 1.3 Cards        # 12 tests written, 12 red ✅
/implement-bdd-rule 2.1 Color        # 8 tests written, 8 red ✅
# ... continue for all 90 sections
# Result: 500+ tests written, all red (expected)
```

### Engine Implementation Phase (Weeks 3-N)
```bash
/implement-engine-feature "1.1 Players"     # 7 tests green ✅
/implement-engine-feature "1.2 Objects"     # 5 tests green ✅
/implement-engine-feature "Zones"           # 30 tests green ✅
# ... continue until all green
# Result: 500+ tests green, engine complete
```

## Success Metrics

### After `/implement-bdd-rule` Task

✅ **Success looks like:**
- Tests written for all sub-rules
- Tests collect successfully
- Tests fail with AttributeError, NotImplementedError, AssertionError
- Engine features needed are documented
- Section marked complete in checklist
- Ready to move to next rule

❌ **Failure looks like:**
- Tests have syntax errors
- Tests can't be collected
- Tests fail with ImportError, NameError
- No documentation of engine needs
- Engine code was modified
- Tests are passing (unless engine already implemented this)

## Communicating Status

### Good Summary (After Writing Tests)
```markdown
## Completed: Section 1.1 - Players

✅ Tests Written: 7 scenarios covering all sub-rules
✅ Test Status: All failing as expected (missing engine features)
✅ Documentation: Updated BDD_TESTS_README.md
✅ Ready for: Engine implementation (separate task)

Engine Features Needed:
- [ ] Player.card_pool property
- [ ] Player.hero property  
- [ ] Supertype subset validation
```

### Bad Summary (Trying to Implement)
```markdown
## Completed: Section 1.1 - Players

✅ Tests Written: 7 scenarios
❌ Implemented Player.card_pool in fab_engine/engine/game.py
❌ Implemented supertype validation
⚠️ 3 tests passing, 4 still failing
⚠️ Need to debug PrecedenceManager next
```

## Remember

**You are writing the rulebook for a game engine, not building the game engine itself.**

The comprehensive rules tell you WHAT must happen.
Your tests verify THAT it happens.
The engine (later) makes it ACTUALLY happen.

Tests = WHAT (specification)
Engine = HOW (implementation)

Keep them separate, stay focused, move fast.
