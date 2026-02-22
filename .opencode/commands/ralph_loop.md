---
description: Ralph loop - Rapidly implement BDD test specifications for the next unchecked rule
---

# Ralph Loop: Rapid BDD Test Implementation

**This command implements ONE rule section's tests, then exits for you to verify and continue.**

## What This Does

1. ✅ Reads `tests/BDD_TESTS_README.md` to find the next unchecked rule
2. ✅ Calls `/implement-bdd-rule <section> <name>` to write the tests
3. ✅ Verifies tests were written correctly
4. ✅ Updates the checklist to mark section complete
5. ✅ Exits so you can review and start next iteration

## Usage

```bash
/ralph-loop
```

That's it! No arguments needed. The command:
- Finds the next `[ ]` (unchecked) rule in the checklist
- Implements that rule's tests
- Marks it `[x]` (complete)
- Exits

## The Loop

```bash
# Iteration 1
/ralph-loop
# → Implements 1.0: General
# → Exits

# You review the tests, verify they look good

# Iteration 2  
/ralph-loop
# → Implements 1.1: Players
# → Exits

# You review the tests, verify they look good

# Iteration 3
/ralph-loop
# → Implements 1.2: Objects
# → Exits

# ... and so on for all 90 sections
```

## Implementation Steps

### Step 1: Find Next Rule

1. Read `tests/BDD_TESTS_README.md`
2. Parse the "Rule Coverage Goals" section
3. Find the FIRST unchecked `[ ]` item
4. Extract section number and name

**Example:**
```markdown
### Section 1: Game Concepts
- [ ] 1.0: General           ← FIRST unchecked, select this
  - [x] 1.0.2: Precedence
- [ ] 1.1: Players
- [ ] 1.2: Objects
```

**Result:** Next rule is `1.0 General`

### Step 2: Invoke /implement-bdd-rule

Call the implementation command:
```bash
/implement-bdd-rule 1.0 General
```

**Important:** Let `/implement-bdd-rule` run completely through all its steps:
1. Research the rule section
2. Plan test scenarios  
3. Write feature file
4. Write step definitions
5. Update helpers (if needed)
6. Run and verify tests
7. Update documentation
8. Complete the task

Do NOT interrupt or skip steps. Let it finish completely.

### Step 3: Verify Implementation

After `/implement-bdd-rule` completes, verify:

**✅ Required Files Exist:**
```bash
# Check feature file exists
ls tests/features/section_1_0_general.feature

# Check step definitions exist  
ls tests/step_defs/test_section_1_0_general.py
```

**✅ Tests Collect Successfully:**
```bash
uv run pytest tests/step_defs/test_section_1_0_general.py --collect-only
```
Should show scenarios, no collection errors.

**✅ Tests Fail for Right Reasons:**
```bash
uv run pytest tests/step_defs/test_section_1_0_general.py -v
```

Check that failures are:
- ✅ AttributeError (missing engine features)
- ✅ NotImplementedError (missing engine features)
- ✅ AssertionError (engine behavior doesn't match spec)
- ❌ NOT SyntaxError, ImportError, NameError (broken test code)

**✅ Documentation Updated:**
- Check that `tests/BDD_TESTS_README.md` has new section documented
- Should include scenario names and what they test

**If ANY verification fails:**
1. Fix the issue (broken test code, missing files, etc.)
2. Re-run verification
3. Do NOT proceed to Step 4 until all verifications pass

### Step 4: Mark Section Complete

Update `tests/BDD_TESTS_README.md`:

**Find the section:**
```markdown
- [ ] 1.0: General
```

**Change to:**
```markdown
- [x] 1.0: General
```

Use the Edit tool to make this change.

**Critical:** Only mark the TOP-LEVEL section, not subsections.

**Example:**
```markdown
### Section 1: Game Concepts
- [x] 1.0: General           ← Mark this complete
  - [x] 1.0.2: Precedence    ← This was already done
- [ ] 1.1: Players           ← Leave unchecked
```

### Step 5: Report and Exit

Provide a clear summary, then EXIT:

```markdown
## Ralph Loop Iteration Complete ✅

### Rule Implemented
- **Section:** 1.0 General
- **Tests Written:** 5 scenarios
- **Status:** All tests failing as expected (missing engine features)

### Files Created
- tests/features/section_1_0_general.feature
- tests/step_defs/test_section_1_0_general.py

### Verification Results
- ✅ Tests collect successfully
- ✅ Tests fail for correct reasons (missing engine features)
- ✅ Documentation updated
- ✅ Checklist marked complete

### Engine Features Needed
- [ ] Rule hierarchy system (1.0.1a, 1.0.1b)
- [ ] Effect supersedes rule logic
- [ ] Tournament rule precedence

### Progress
- **Completed:** 2 / 90 sections (1.0.2 + 1.0)
- **Remaining:** 88 sections

### Next Steps
1. Review the tests: `tests/step_defs/test_section_1_0_general.py`
2. Verify they match comprehensive rules
3. Run `/ralph-loop` again to implement next rule (1.1 Players)

---

**Ralph loop iteration complete. Ready for next iteration.**
```

**Then EXIT.** Do not continue to the next rule.

## Important Notes

### One Rule Per Iteration

**DO:**
- ✅ Implement ONE rule section
- ✅ Verify it completely
- ✅ Mark it complete
- ✅ Exit

**DON'T:**
- ❌ Implement multiple rules in one iteration
- ❌ Skip verification steps
- ❌ Continue to next rule automatically
- ❌ Mark sections complete without verification

### When to Stop

The ralph loop stops automatically when:
```markdown
### Section 9: Additional Rules
- [x] 9.0: General
- [x] 9.1: Double-Faced Cards
- [x] 9.2: Split-Cards
- [x] 9.3: Marked
```

When all sections are `[x]`, announce:
```
🎉 ALL RULE SECTIONS COMPLETE! 🎉

All 90 rule sections have BDD test specifications written.
Total tests: ~500+ scenarios
All tests failing as expected (ready for engine implementation)

Next phase: Implement engine features to make tests pass.
```

### Subsection Handling

Some sections have subsections:

```markdown
- [ ] 1.0: General
  - [x] 1.0.2: Precedence (Restrictions/Requirements/Allowances)
```

**Rules:**
1. If parent section is unchecked `[ ] 1.0: General`, implement the PARENT, not subsections
2. The subsection `1.0.2` is already done, so skip it when implementing `1.0`
3. Focus on rules NOT covered by existing subsections
4. Mark only the PARENT complete when done

### If No Rules Left in a Section

Sometimes all subsections are complete but parent isn't marked:

```markdown
- [ ] 1.0: General
  - [x] 1.0.1: Rule Hierarchy
  - [x] 1.0.2: Precedence
  # (all subsections done)
```

In this case:
1. Check if there are rules in section 1.0 NOT covered by subsections
2. If yes, implement tests for those rules
3. If no, just mark `[x] 1.0: General` complete and move on

### Error Handling

**If test collection fails:**
```bash
ERROR: SyntaxError in test_section_1_0_general.py
```
1. Fix the syntax error in the test file
2. Re-run collection
3. Do NOT mark complete until collection succeeds

**If tests fail with wrong error types:**
```bash
ImportError: cannot import name 'CardTyp'
```
1. This is broken test code (typo)
2. Fix the import
3. Re-run tests
4. Do NOT mark complete until failures are correct type

**If verification step fails:**
1. Report what failed
2. Fix the issue
3. Re-run verification
4. Do NOT proceed until verification passes

### Skip Already-Complete Sections

When finding next rule to implement:

```markdown
- [x] 1.0: General           ← Skip (already done)
- [x] 1.1: Players           ← Skip (already done)
- [ ] 1.2: Objects           ← IMPLEMENT THIS
```

Always find the FIRST unchecked `[ ]` section at the top level.

## Verification Checklist

Before marking complete and exiting, verify:

- [ ] Feature file exists and has scenarios
- [ ] Step definitions exist and have test functions
- [ ] `pytest --collect-only` succeeds
- [ ] Tests fail with AttributeError, NotImplementedError, or AssertionError
- [ ] Tests do NOT fail with SyntaxError, ImportError, NameError
- [ ] `tests/BDD_TESTS_README.md` is updated with test documentation
- [ ] Section is marked `[x]` in checklist
- [ ] Summary report is provided
- [ ] You are about to EXIT (not continue to next rule)

## Example Full Iteration

```
User: /ralph-loop