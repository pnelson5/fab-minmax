---
description: Search the Flesh and Blood comprehensive ruleset using qmd
---

# Search FAB Rules

Search the Flesh and Blood TCG comprehensive ruleset using qmd's powerful search capabilities.

## Usage

```
/fab_search <query> [-n <num>] [--query]
```

## Arguments

- `<query>` - The search query (keywords or natural language)
- `-n <num>` - Number of results to return (default: 5)
- `--query` - Use semantic query search with reranking (slower but more accurate for complex questions)

## Examples

```
/fab_search "instant card rules"
/fab_search "restriction precedence" -n 10
/fab_search "how does blocking work" --query
```

## Implementation

When this command is invoked:

1. Execute `fab_search.py` with the provided query and options
2. Present the results with clear formatting
3. Highlight the rule numbers found in the results
4. If no results found, suggest alternative search terms

**Command executed:**
```bash
python fab_search.py "<query>" -n <num>            # For keyword search
python fab_search.py "<query>" -n <num> --query    # For semantic search
```

## Search Tips

- **For specific rules**: Include keywords from the rule like "restriction" or "attack target"
- **For concepts**: Use keywords like "attack", "block", "instant", "priority"
- **For natural language**: Use `--query` for better semantic understanding
- **Rule numbers**: While rule numbers (like 1.0.2) are in the content, the BM25 search works best with keywords
