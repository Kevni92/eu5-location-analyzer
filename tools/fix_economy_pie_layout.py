#!/usr/bin/env python3
"""Post-process the generated Economy pie panel into two non-overlapping half-width cards."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = REPO_ROOT / "in_game" / "gui" / "economy_lateralview.gui"
MARKER = "# ELA economy breakdown pie panel"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--source", type=Path)
    parser.add_argument("--game-dir", type=Path)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args, _ = parser.parse_known_args()
    return args


def main() -> None:
    args = parse_args()
    output = args.output.expanduser()
    if not output.is_file():
        raise SystemExit(f"ERROR: Generated economy GUI not found: {output}")

    text = output.read_text(encoding="utf-8-sig")
    start = text.find(MARKER)
    if start < 0:
        raise SystemExit("ERROR: Economy pie panel marker not found; run the pie injector first.")

    scroll_match = re.search(r'(?m)^[ \t]*scroll_list\s*=\s*\{\s*$', text[start:])
    if scroll_match is None:
        raise SystemExit("ERROR: Could not find the Economy scroll_list after the pie panel.")

    end = start + scroll_match.start()
    panel = text[start:end]

    # The first prototype used two horizontally-expanding widgets inside an hbox.
    # In EU5/Jomini those widgets occupied the same effective coordinate space,
    # so the income and expense donuts were rendered on top of each other.
    # Give both cards explicit half-widths instead.
    card_pattern = re.compile(
        r'(?m)^(?P<indent>[ \t]*)layoutpolicy_horizontal = expanding\s*\n'
        r'(?P=indent)size = \{ -1 132 \}\s*$'
    )
    panel, card_count = card_pattern.subn(
        lambda match: f"{match.group('indent')}size = {{ 50% 132 }}",
        panel,
    )
    if card_count != 2:
        raise SystemExit(
            "ERROR: Expected exactly two pie analysis cards to resize, "
            f"found {card_count}."
        )

    # With exact 50/50 cards, remove spacing/margins from the containing hbox so
    # the two widths add up cleanly to the available panel width.
    panel, margin_count = re.subn(
        r'(?m)^(?P<indent>[ \t]*)margin = \{ 5 5 \}\s*$',
        lambda match: f"{match.group('indent')}margin = {{ 0 0 }}",
        panel,
        count=1,
    )
    panel, spacing_count = re.subn(
        r'(?m)^(?P<indent>[ \t]*)spacing = 5\s*$',
        lambda match: f"{match.group('indent')}spacing = 0",
        panel,
        count=1,
    )
    if margin_count != 1 or spacing_count != 1:
        raise SystemExit(
            "ERROR: Could not normalize the shared pie-panel hbox spacing/margins."
        )

    # Keep the center label compact. The side is already communicated by the
    # title and color palette, so the currency icon only makes the donut center
    # harder to read.
    replacements = {
        'raw_text = "[EconomyView.GetAllIncome|2]@income!"':
            'raw_text = "[EconomyView.GetAllIncome|2]"',
        'raw_text = "[EconomyView.GetAllExpense|2]@expense!"':
            'raw_text = "[EconomyView.GetAllExpense|2]"',
    }
    for old, new in replacements.items():
        count = panel.count(old)
        if count != 1:
            raise SystemExit(
                f"ERROR: Expected center-label anchor once, found {count}: {old}"
            )
        panel = panel.replace(old, new, 1)

    text = text[:start] + panel + text[end:]
    output.write_text(text, encoding="utf-8-sig", newline="\n")

    print("Economy pie layout post-process applied successfully.")
    print("  Income card : fixed 50% width")
    print("  Expense card: fixed 50% width")
    print("  Shared hbox : zero spacing / zero margin")
    print("  Donut center: numeric total only")


if __name__ == "__main__":
    main()
