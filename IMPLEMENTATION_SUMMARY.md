# BDD Rule Implementation Summary

## What Was Done

### 1. Updated BDD_TESTS_README.md
- Expanded the Rule Coverage Goals section with an exhaustive checklist
- Added all 9 sections with their subsections from the comprehensive rules:
  - Section 1: Game Concepts (16 subsections)
  - Section 2: Object Properties (16 subsections)
  - Section 3: Zones (17 subsections)
  - Section 4: Game Structure (6 subsections)
  - Section 5: Layers, Cards, & Abilities (5 subsections)
  - Section 6: Effects (7 subsections)
  - Section 7: Combat (8 subsections)
  - Section 8: Keywords (7 subsections)
  - Section 9: Additional Rules (4 subsections)
- Total: 90+ rule sections to implement tests for

### 2. Created /implement-bdd-rule Slash Command
- Location: `.opencode/commands/implement_bdd_rule.md`
- Provides comprehensive step-by-step guidance for implementing BDD tests
- Includes DO's and DON'Ts for each step
- References the real engine integration approach
- Contains quality checklist and example workflow

### 3. Enhanced Comprehensive Rules with Internal Links
- Updated `convert_to_md.py` to automatically add internal links
- Added `linkify_rule_references()` function to convert `[1.0.1a]` to `[1.0.1a](#101a)`
- Added `create_anchor_id()` to generate consistent anchor IDs
- Added HTML anchors (`<a id="102a"></a>`) to each rule heading
- Reconverted `en-fab-cr.txt` to `fab-rules/en-fab-cr.md` with links
- Reindexed with qmd for searchability

## How It Works

### Rule Reference Links
Before:
```markdown
### 1.0.2 A restriction takes precedence over any requirement or allowance, subject to [1.0.1a].
```

After:
```markdown
<a id="102"></a>
### 1.0.2 A restriction takes precedence over any requirement or allowance, subject to [1.0.1a](#101a).
```

Now you can click on `[1.0.1a](#101a)` to jump directly to rule 1.0.1a in the markdown file.

### Using the /implement-bdd-rule Command

```bash
/implement-bdd-rule <section_number> [rule_name]
```

Examples:
```bash
/implement-bdd-rule 1.1 Players
/implement-bdd-rule 2.1 Color
/implement-bdd-rule 7.2 Attack Step
```

The command will guide you through:
1. Research the rule section (with clickable links!)
2. Plan test scenarios
3. Write the Gherkin feature file
4. Write step definitions
5. Update bdd_helpers.py if needed
6. Run and verify tests
7. Update documentation
8. Complete the task

### Ralph Loop Workflow

You can now use a ralph (rapid implementation) loop:

1. Check the checklist in `tests/BDD_TESTS_README.md`
2. Pick an unchecked rule section
3. Run `/implement-bdd-rule X.Y Rule Name`
4. Follow the guided steps
5. Mark the section complete in README
6. Repeat for the next rule

## Files Modified

1. `tests/BDD_TESTS_README.md` - Added exhaustive rule checklist
2. `.opencode/commands/implement_bdd_rule.md` - New slash command
3. `convert_to_md.py` - Enhanced with link generation
4. `fab-rules/en-fab-cr.md` - Reconverted with internal links

## Benefits

### For Navigation
- Click on rule references to jump to definitions
- Understand rule dependencies quickly
- Follow chains of cross-references easily

### For Testing
- Identify which rules depend on each other
- Ensure comprehensive test coverage
- Find examples that illustrate interactions

### For Development
- Consistent workflow for implementing each rule
- Clear DO's and DON'Ts prevent common mistakes
- Quality checklist ensures completeness

## Next Steps

1. Start implementing tests using `/implement-bdd-rule`
2. Work through the checklist systematically
3. Use ralph loop for rapid progress
4. Tests will fail initially (by design - TDD approach)
5. Later: implement engine features to make tests pass

## Example: Testing with Links

When implementing tests for Rule 1.0.2 (Precedence):
- Rule references `[1.0.1a]` (effect supersedes rule)
- Click the link to see: "If an effect directly contradicts a rule contained in this document, the effect supersedes that rule."
- This informs test design: effects can override the precedence system itself

## Testing the Setup

Search works:
```bash
uv run python fab_search.py "restriction precedence" -n 3
```

Links work:
```bash
grep "\[1\.0\.1a\](#101a)" fab-rules/en-fab-cr.md
```

Command available:
```bash
/implement-bdd-rule 1.1 Players
```

## Complete Test Coverage Goal

The ultimate goal is to have test coverage for all ~90 rule sections. The checklist in `tests/BDD_TESTS_README.md` provides the roadmap. Currently complete:
- [x] 1.0.2: Precedence (Restrictions/Requirements/Allowances)
- [ ] 89 more sections to go!
