#!/usr/bin/env python3
"""
FAB Rules Search - Wrapper script for searching the Flesh and Blood ruleset.

Usage:
    python fab_search.py "<query>" [-n <num>]

Examples:
    python fab_search.py "restriction takes precedence"
    python fab_search.py "attack target" -n 10
    python fab_search.py "1.0.2" -n 3
"""

import argparse
import subprocess
import sys


def search_fab_rules(query: str, num_results: int = 5, use_query: bool = False) -> str:
    """Search the FAB ruleset using qmd."""
    cmd = ["qmd"]

    if use_query:
        cmd.extend(["query", query])
    else:
        cmd.extend(["search", query])

    cmd.extend(["-c", "fab-rules", "-n", str(num_results)])

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)

        if result.returncode == 0:
            return result.stdout
        else:
            return f"Error: {result.stderr}"
    except subprocess.TimeoutExpired:
        return "Error: Search timed out"
    except FileNotFoundError:
        return "Error: qmd not found. Please install with: npm install -g @tobilu/qmd"
    except Exception as e:
        return f"Error: {e}"


def main():
    parser = argparse.ArgumentParser(
        description="Search the Flesh and Blood comprehensive ruleset",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python fab_search.py "restriction takes precedence"
  python fab_search.py "attack target" -n 10
  python fab_search.py "how does blocking work" --query
        """,
    )

    parser.add_argument("query", help="Search query (keywords or natural language)")
    parser.add_argument(
        "-n",
        "--num-results",
        type=int,
        default=5,
        help="Number of results to return (default: 5)",
    )
    parser.add_argument(
        "--query",
        action="store_true",
        dest="use_query",
        help="Use semantic query search with reranking (slower but more accurate)",
    )

    args = parser.parse_args()

    print(f"Searching FAB rules for: '{args.query}'")
    print(f"Method: {'Semantic query' if args.use_query else 'Keyword search'}")
    print("-" * 60)

    results = search_fab_rules(args.query, args.num_results, args.use_query)
    print(results)


if __name__ == "__main__":
    main()
