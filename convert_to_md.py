#!/usr/bin/env python3
"""
Convert Flesh and Blood comprehensive ruleset from txt to markdown format.

This script converts the hierarchical numbered structure (1.0, 1.0.1, 1.0.1a) into
markdown headers (#, ##, ###) suitable for qmd search indexing.
"""

import re
from pathlib import Path


def parse_rule_number(line: str) -> tuple[str, int, str] | None:
    """
    Parse a rule number from the beginning of a line.

    Returns (full_number, depth, title) or None if not a rule line.

    Examples:
        "1 Game Concepts" -> ("1", 1, "Game Concepts")
        "1.0 General" -> ("1.0", 2, "General")
        "1.0.1 The rules..." -> ("1.0.1", 3, "The rules...")
        "1.0.1a If an effect..." -> ("1.0.1a", 4, "If an effect...")
    """
    # Match pattern: number(s) at the start followed by space and content
    match = re.match(r"^(\d+(?:\.\d+)?(?:\.\d+)?[a-z]?)\s+(.+)$", line)
    if match:
        number = match.group(1)
        content = match.group(2)

        # Calculate depth based on number structure
        # 1 -> 1 (top level)
        # 1.0 -> 2 (subsection)
        # 1.0.1 -> 3 (rule)
        # 1.0.1a -> 4 (sub-rule)
        depth = 1
        if "." in number:
            parts = number.split(".")
            if len(parts) == 2:
                depth = 2
            elif len(parts) == 3:
                depth = 3

        # If there's a letter suffix, add to depth
        if re.search(r"[a-z]$", number):
            depth = max(depth + 1, 4)

        return (number, depth, content)

    return None


def is_example(line: str) -> bool:
    """Check if a line starts with 'Example:'"""
    return line.strip().startswith("Example:")


def is_note(line: str) -> bool:
    """Check if a line starts with 'Note:'"""
    return line.strip().startswith("Note:")


def create_anchor_id(rule_number: str) -> str:
    """
    Create a markdown anchor ID from a rule number.

    Examples:
        "1.0.2" -> "102"
        "1.0.2a" -> "102a"
        "2.5.1a" -> "251a"
    """
    # Remove dots and keep letters
    return rule_number.replace(".", "")


def linkify_rule_references(text: str) -> str:
    """
    Convert rule references like [1.0.2] or [1.0.2a] into markdown links.

    Examples:
        "subject to [1.0.1a]" -> "subject to [1.0.1a](#101a)"
        "[1.3.2a]" -> "[1.3.2a](#132a)"
        "[2.5.1a]" -> "[2.5.1a](#251a)"
    """
    # Pattern to match rule references: [digits.digits] or [digits.digits.digits] with optional letter
    pattern = r"\[(\d+\.\d+(?:\.\d+)?[a-z]?)\]"

    def replace_reference(match):
        rule_ref = match.group(1)
        anchor = create_anchor_id(rule_ref)
        return f"[{rule_ref}](#{anchor})"

    return re.sub(pattern, replace_reference, text)


def convert_to_markdown(input_file: str, output_file: str) -> None:
    """Convert the txt ruleset to markdown format."""
    with open(input_file, "r") as f:
        lines = f.readlines()

    md_lines = []
    md_lines.append("# Flesh and Blood Comprehensive Rules")
    md_lines.append("")
    md_lines.append(
        "This document contains the complete ruleset for Flesh and Blood TCG."
    )
    md_lines.append("")

    current_section = None
    in_example = False
    example_lines = []
    in_note = False
    note_lines = []

    for i, line in enumerate(lines):
        line = line.rstrip()

        # Skip empty lines at the beginning
        if not line and not md_lines:
            continue

        # Parse rule number
        parsed = parse_rule_number(line)

        if parsed:
            # Close any open example or note blocks
            if in_example and example_lines:
                md_lines.append("> " + "\n> ".join(example_lines))
                md_lines.append("")
                example_lines = []
                in_example = False

            if in_note and note_lines:
                md_lines.append("> **Note:** " + "\n> ".join(note_lines))
                md_lines.append("")
                note_lines = []
                in_note = False

            number, depth, content = parsed

            # Map depth to markdown header level
            # Depth 1 -> # (H1)
            # Depth 2 -> ## (H2)
            # Depth 3 -> ### (H3)
            # Depth 4+ -> #### (H4)
            header_level = min(depth, 4)
            header_prefix = "#" * header_level

            # Create anchor ID for this rule
            anchor_id = create_anchor_id(number)

            # Linkify any rule references in the content
            linked_content = linkify_rule_references(content)

            # Include rule number in the visible content so it's searchable
            # Add HTML anchor for internal linking
            md_lines.append(f'<a id="{anchor_id}"></a>')
            md_lines.append(f"{header_prefix} {number} {linked_content}")
            md_lines.append("")

            current_section = number

        elif is_example(line):
            # Close any open note
            if in_note and note_lines:
                md_lines.append("> **Note:** " + "\n> ".join(note_lines))
                md_lines.append("")
                note_lines = []
                in_note = False

            # Start example block
            in_example = True
            example_content = line.replace("Example:", "").strip()
            if example_content:
                example_lines.append(example_content)

        elif is_note(line):
            # Close any open example
            if in_example and example_lines:
                md_lines.append("> " + "\n> ".join(example_lines))
                md_lines.append("")
                example_lines = []
                in_example = False

            # Start note block
            in_note = True
            note_content = line.replace("Note:", "").strip()
            if note_content:
                note_lines.append(note_content)

        else:
            # Regular content line - linkify rule references
            linked_line = linkify_rule_references(line)

            if in_example:
                example_lines.append(linked_line)
            elif in_note:
                note_lines.append(linked_line)
            elif line.strip():  # Non-empty line
                md_lines.append(linked_line)
            else:
                md_lines.append("")  # Preserve paragraph breaks

    # Close any remaining blocks
    if in_example and example_lines:
        md_lines.append("> " + "\n> ".join(example_lines))
        md_lines.append("")

    if in_note and note_lines:
        md_lines.append("> **Note:** " + "\n> ".join(note_lines))
        md_lines.append("")

    # Write output
    with open(output_file, "w") as f:
        f.write("\n".join(md_lines))

    print(f"Converted {input_file} to {output_file}")
    print(f"Total lines: {len(lines)} -> {len(md_lines)} markdown lines")


if __name__ == "__main__":
    input_path = Path("en-fab-cr.txt")
    output_path = Path("en-fab-cr.md")

    if not input_path.exists():
        print(f"Error: {input_path} not found")
        exit(1)

    convert_to_markdown(str(input_path), str(output_path))
