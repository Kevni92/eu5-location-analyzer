#!/usr/bin/env python3
"""Build the EU5 Location Analyzer Economy analysis GUI from installed vanilla.

The Economy view is a whole-file GUI override. To avoid committing a stale copy of
Paradox' file, this builder reads the user's current vanilla
`game/in_game/gui/economy_lateralview.gui`, applies deliberately small analysis
patches, and writes the Workshop-ready override to
`in_game/gui/economy_lateralview.gui` in this repository.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = REPO_ROOT / "in_game" / "gui" / "economy_lateralview.gui"

# Compact analysis format inside slider cards:
#   25% | 4.2%B
# means slider at 25%, consuming 4.2% of total monthly expenses.
#
# Abs_CFixedPoint is intentional because expense getters may be exposed with a
# negative sign while the ratio we want is a positive budget share.
#
# Tax Base uses `text`, not `raw_text`, because the named block in the vanilla
# subheader template already defines a `text` property. The first debug build used
# raw_text here and the untouched base `text = "default"` won, producing the
# literal word "default" in-game.
#
# Runtime testing also proved that Player.GetTotalTaxBase / Player.GetTotalWealth
# are display/localization getters, not CFixedPoint arguments accepted by GUI math
# helpers. Therefore the percentage is calculated as a numeric ScriptValue in
# in_game/common/script_values/ela_economy_values.txt and merely displayed here.
PATCHES = (
    (
        "taxable_wealth_share",
        'text = "[Player.GetTotalTaxBase]"',
        'text = "[Player.GetTotalTaxBase|2] ([Player.MakeScope.ScriptValue(\'ela_taxable_wealth_share\')|%1])"',
    ),
    (
        "maintenance_slider_percent_and_budget_share",
        'text = "[MaintenanceSetting.GetExpenseBenefit]"',
        'raw_text = "[MaintenanceSetting.GetSliderValue|0%V] | [Divide_CFixedPoint(Abs_CFixedPoint(MaintenanceSetting.GetExpense), Max_CFixedPoint(Abs_CFixedPoint(EconomyView.GetAllExpense), \'(CFixedPoint)0.01\'))|%1]B"',
    ),
    (
        "stability_slider_percent_and_budget_share",
        'raw_text = "[EconomyView.GetStabilityChange|2+=]@stability!"',
        'raw_text = "[EconomyView.GetDefaultStabilityInvestment|0%V] | [Divide_CFixedPoint(Abs_CFixedPoint(EconomyView.GetStabilityInvestmentExpense), Max_CFixedPoint(Abs_CFixedPoint(EconomyView.GetAllExpense), \'(CFixedPoint)0.01\'))|%1]B"',
    ),
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate the Workshop-ready EU5 Location Analyzer Economy analysis GUI."
    )
    parser.add_argument(
        "--source",
        type=Path,
        help="Direct path to vanilla game/in_game/gui/economy_lateralview.gui.",
    )
    parser.add_argument(
        "--game-dir",
        type=Path,
        help="EU5 install directory (the directory containing game/).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=f"Generated GUI path (default: {DEFAULT_OUTPUT}).",
    )
    return parser.parse_args()


def steam_library_paths() -> list[Path]:
    roots: list[Path] = []

    env_steam = os.environ.get("STEAM_DIR")
    if env_steam:
        roots.append(Path(env_steam))

    if sys.platform == "win32":
        roots.extend(
            [
                Path(r"C:\Program Files (x86)\Steam"),
                Path(r"C:\Program Files\Steam"),
            ]
        )
    else:
        roots.extend(
            [
                Path.home() / ".steam" / "steam",
                Path.home() / ".local" / "share" / "Steam",
            ]
        )

    libraries: list[Path] = []
    seen: set[Path] = set()

    def add_library(path: Path) -> None:
        try:
            normalized = path.expanduser().resolve()
        except OSError:
            normalized = path.expanduser()
        if normalized not in seen:
            seen.add(normalized)
            libraries.append(normalized)

    for steam_root in roots:
        if not steam_root.exists():
            continue
        add_library(steam_root)
        vdf = steam_root / "steamapps" / "libraryfolders.vdf"
        if not vdf.exists():
            continue
        try:
            content = vdf.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for match in re.finditer(r'"path"\s+"([^"]+)"', content):
            raw = match.group(1).replace(r"\\", "\\")
            add_library(Path(raw))

    return libraries


def find_source(args: argparse.Namespace) -> Path:
    if args.source:
        source = args.source.expanduser()
        if source.is_file():
            return source
        raise SystemExit(f"ERROR: --source does not exist: {source}")

    if args.game_dir:
        candidate = args.game_dir.expanduser() / "game" / "in_game" / "gui" / "economy_lateralview.gui"
        if candidate.is_file():
            return candidate
        raise SystemExit(f"ERROR: Could not find vanilla Economy GUI below --game-dir: {candidate}")

    env_game = os.environ.get("EU5_GAME_DIR")
    if env_game:
        candidate = Path(env_game).expanduser() / "game" / "in_game" / "gui" / "economy_lateralview.gui"
        if candidate.is_file():
            return candidate

    game_folder_names = (
        "Europa Universalis V",
        "Europa Universalis 5",
    )
    for library in steam_library_paths():
        for game_name in game_folder_names:
            candidate = library / "steamapps" / "common" / game_name / "game" / "in_game" / "gui" / "economy_lateralview.gui"
            if candidate.is_file():
                return candidate

    raise SystemExit(
        "ERROR: Could not auto-detect EU5. Use --game-dir <EU5 install directory> "
        "or --source <economy_lateralview.gui>."
    )


def apply_patch_once(text: str, patch_name: str, old: str, new: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(
            f"ERROR: Patch '{patch_name}' expected its vanilla anchor exactly once, found {count}.\n"
            "The installed EU5 GUI probably changed. Do not force the patch; update the builder against the new vanilla file."
        )
    return text.replace(old, new, 1)


def build(source: Path, output: Path) -> None:
    raw = source.read_bytes()
    source_sha256 = hashlib.sha256(raw).hexdigest()
    text = raw.decode("utf-8-sig")

    if "kevni92.eu5_location_analyzer" in text or "MaintenanceSetting.GetSliderValue|0%V] | [Divide_CFixedPoint" in text:
        raise SystemExit(
            "ERROR: The selected source already appears to be patched. Point --source at the vanilla game file, not the mod output."
        )

    patched = text
    for patch_name, old, new in PATCHES:
        patched = apply_patch_once(patched, patch_name, old, new)

    header = (
        "# EU5 Location Analyzer - generated Economy analysis override\n"
        "# Mod id: kevni92.eu5_location_analyzer\n"
        f"# Vanilla source SHA256: {source_sha256}\n"
        "# Slider format: <slider %> | <share of total expenses %>B\n"
        "# Generated by tools/build_debug_gui.py; do not hand-edit this generated file.\n\n"
    )

    output = output.expanduser()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(header + patched, encoding="utf-8-sig", newline="\n")

    print("EU5 Location Analyzer Economy analysis GUI generated successfully.")
    print(f"Source : {source}")
    print(f"SHA256 : {source_sha256}")
    print(f"Output : {output}")
    print("Applied patches:")
    for patch_name, _, _ in PATCHES:
        print(f"  - {patch_name}")
    print("\nSlider format: <slider %> | <share of total monthly expenses %>B")
    print("Example: 25% | 4.2%B means slider=25% and budget share=4.2%.")
    print("Enable the mod and open Economy. The generated file is a whole-file GUI override.")


def main() -> None:
    args = parse_args()
    source = find_source(args)
    build(source, args.output)


if __name__ == "__main__":
    main()
