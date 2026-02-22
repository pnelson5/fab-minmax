# Model Selection for Ralph Loop

## Quick Reference

```bash
# Use default model (whatever OpenCode is configured for)
./ralph.sh
./ralph-auto.sh 5

# Use specific model
./ralph.sh anthropic/claude-sonnet-4-5
./ralph-auto.sh 5 anthropic/claude-opus-4-5

# In OpenCode TUI, set model preference in settings
# Then just run: /ralph-loop
```

## Available Models

### List All Models
```bash
# List Anthropic models
opencode models anthropic

# List OpenAI models  
opencode models openai

# List all providers
opencode models
```

### Recommended Models for BDD Test Writing

| Model | Speed | Quality | Cost | Best For |
|-------|-------|---------|------|----------|
| **claude-sonnet-4-5** | Fast | Excellent | Medium | **Recommended default** |
| **claude-opus-4-5** | Slower | Best | High | Complex rules, careful review |
| **claude-3-5-sonnet** | Fast | Good | Low | Batch processing, simple rules |
| **claude-haiku-4-5** | Fastest | Decent | Lowest | Quick iterations, testing |

### Model Selection Strategy

#### For First 10 Rules (Learning Phase)
```bash
# Use the best model to set high quality baseline
./ralph.sh anthropic/claude-opus-4-5
```

**Why:** You want high-quality examples to learn from. Opus will write more thorough tests with better documentation.

#### For Rules 11-50 (Standard Phase)
```bash
# Use Sonnet for good balance of speed and quality
./ralph-auto.sh 10 anthropic/claude-sonnet-4-5
```

**Why:** You understand the pattern. Sonnet is fast enough for batch processing and maintains quality.

#### For Rules 51-90 (Speed Phase)
```bash
# Use Sonnet or even Haiku for rapid completion
./ralph-auto.sh 20 anthropic/claude-sonnet-4-5
# or
./ralph-auto.sh 20 anthropic/claude-haiku-4-5
```

**Why:** The pattern is established. You can review quickly and fix minor issues.

## Usage Examples

### Manual Mode with Model
```bash
# Use Opus for careful implementation
./ralph.sh anthropic/claude-opus-4-5

# Use Sonnet for standard implementation  
./ralph.sh anthropic/claude-sonnet-4-5

# Use Haiku for fast iteration
./ralph.sh anthropic/claude-haiku-4-5
```

### Batch Mode with Model
```bash
# 5 rules with Opus (careful)
./ralph-auto.sh 5 anthropic/claude-opus-4-5

# 10 rules with Sonnet (balanced)
./ralph-auto.sh 10 anthropic/claude-sonnet-4-5

# 20 rules with Haiku (fast)
./ralph-auto.sh 20 anthropic/claude-haiku-4-5
```

### Mixed Strategy
```bash
# Complex sections (Combat, Effects) with Opus
./ralph.sh anthropic/claude-opus-4-5  # Section 6: Effects
./ralph.sh anthropic/claude-opus-4-5  # Section 7: Combat

# Simple sections (Properties) with Sonnet
./ralph-auto.sh 10 anthropic/claude-sonnet-4-5  # Section 2: Properties

# Straightforward sections with Haiku
./ralph-auto.sh 5 anthropic/claude-haiku-4-5  # Section 8: Keywords
```

## Cost Optimization

### Estimated Costs (Approximate)

**Per rule section:**
- Opus 4.5: ~$0.10-0.30 per rule
- Sonnet 4.5: ~$0.03-0.10 per rule
- Haiku 4.5: ~$0.01-0.03 per rule

**For all 90 rules:**
- All Opus: ~$9-27 total
- All Sonnet: ~$3-9 total
- All Haiku: ~$1-3 total
- Mixed (10 Opus + 40 Sonnet + 40 Haiku): ~$4-12 total

### Cost-Effective Strategy
```bash
# Use Opus for 10 most complex sections (~$1-3)
# Use Sonnet for 50 standard sections (~$2-5)
# Use Haiku for 30 simple sections (~$0.30-1)
# Total: ~$3-9
```

## Quality vs Speed Trade-offs

### Opus 4.5
**Pros:**
- ✅ Most thorough test scenarios
- ✅ Best documentation
- ✅ Catches edge cases
- ✅ Better rule interpretation

**Cons:**
- ❌ Slower (2-3x longer)
- ❌ More expensive
- ❌ Overkill for simple rules

### Sonnet 4.5  
**Pros:**
- ✅ Excellent quality
- ✅ Fast enough for batches
- ✅ Good cost/quality ratio
- ✅ Reliable for standard rules

**Cons:**
- ❌ May miss some edge cases
- ❌ Less detailed documentation

### Haiku 4.5
**Pros:**
- ✅ Very fast
- ✅ Cheap
- ✅ Good for simple rules
- ✅ Great for iteration

**Cons:**
- ❌ May need more review/fixes
- ❌ Less thorough scenarios
- ❌ Simpler documentation

## Setting Default Model

### In OpenCode Config
```bash
# Edit OpenCode settings to set default model
opencode
# Then in settings: Model > Select provider/model
```

### Using Environment Variable
```bash
# Set in your shell profile (~/.bashrc, ~/.zshrc)
export OPENCODE_MODEL="anthropic/claude-sonnet-4-5"

# Then scripts will use this by default
./ralph.sh  # Uses sonnet-4-5
```

### Per-Session Override
```bash
# Override for just this run
./ralph.sh anthropic/claude-opus-4-5
```

## Checking Model Performance

### After Running Tests
```bash
# Check quality of generated tests
cat tests/features/section_X_Y_Z.feature
cat tests/step_defs/test_section_X_Y_Z.py

# Run tests to check correctness
uv run pytest tests/step_defs/test_section_X_Y_Z.py -v

# Compare different models' outputs
diff tests/features/section_opus_*.feature tests/features/section_haiku_*.feature
```

### Model Performance Metrics

Track these for each model you try:

| Metric | Opus | Sonnet | Haiku |
|--------|------|--------|-------|
| Time per rule | 5-10 min | 3-5 min | 2-3 min |
| Scenarios per rule | 5-10 | 3-7 | 2-5 |
| Manual fixes needed | 0-1 | 1-2 | 2-4 |
| Edge cases caught | High | Medium | Low |
| Documentation quality | Excellent | Good | Basic |

## Recommendations by Section

### Use Opus For (Complex Rules):
- Section 1.8: Effects
- Section 6: Effects (detailed)
- Section 7: Combat
- Section 5.4: Static Abilities
- Section 6.4: Replacement Effects

### Use Sonnet For (Standard Rules):
- Section 1.1: Players
- Section 1.2: Objects
- Section 1.3: Cards
- Section 2: Object Properties
- Section 3: Zones
- Section 4: Game Structure

### Use Haiku For (Simple Rules):
- Section 2.1: Color
- Section 2.7: Name
- Section 8: Keywords (many are straightforward)
- Section 9: Additional Rules

## Summary

**Start with Opus** for first 5-10 rules to establish quality baseline.

**Switch to Sonnet** for bulk of rules (good quality, good speed).

**Use Haiku** for simple sections or when doing large batches.

**Default recommendation:** `anthropic/claude-sonnet-4-5` for best balance.

```bash
# Most common usage
./ralph-auto.sh 10 anthropic/claude-sonnet-4-5
```
