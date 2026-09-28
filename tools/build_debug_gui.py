#!/usr/bin/env python3
"""Build the EU5 Location Analyzer Economy analysis GUI from installed vanilla."""

from __future__ import annotations

import argparse
import hashlib
import os
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = REPO_ROOT / "in_game" / "gui" / "economy_lateralview.gui"

PATCHES = (
    (
        "wealth_reconstruction_probe",
        'text = "[Player.GetTotalWealth|2L]"',
        'text = "[Player.GetTotalWealth|2L] | R[Player.MakeScope.ScriptValue(\'ela_total_wealth_reconstructed\')|2]"',
    ),
    (
        "taxable_wealth_share_probe",
        'text = "[Player.GetTotalTaxBase]"',
        'text = "[Player.GetTotalTaxBase|2] | R[Player.MakeScope.ScriptValue(\'ela_taxable_wealth_share\')|%1]"',
    ),
    (
        "maintenance_slider_percent_and_budget_share",
        'text = "[MaintenanceSetting.GetExpenseBenefit]"',
        'raw_text = "[MaintenanceSetting.GetSliderValue|0%V] | [Divide_CFixedPoint(Abs_CFixedPoint(MaintenanceSetting.GetExpense), Max_CFixedPoint(Abs_CFixedPoint(EconomyView.GetAllExpense), \'(CFixedPoint)0.01\'))|%1]B"',
    ),
    (
        "non_slider_maintenance_budget_share",
        'raw_text = "[MaintenanceSetting.GetExpenseWithCurrency]"',
        'raw_text = "[MaintenanceSetting.GetExpenseWithCurrency] ([Divide_CFixedPoint(Abs_CFixedPoint(MaintenanceSetting.GetExpense), Max_CFixedPoint(Abs_CFixedPoint(EconomyView.GetAllExpense), \'(CFixedPoint)0.01\'))|%1])"',
    ),
    (
        "stability_slider_percent_and_budget_share",
        'raw_text = "[EconomyView.GetStabilityChange|2+=]@stability!"',
        'raw_text = "[EconomyView.GetDefaultStabilityInvestment|0%V] | [Divide_CFixedPoint(Abs_CFixedPoint(EconomyView.GetStabilityInvestmentExpense), Max_CFixedPoint(Abs_CFixedPoint(EconomyView.GetAllExpense), \'(CFixedPoint)0.01\'))|%1]B"',
    ),
)

INCOME_SHARE_DENOMINATOR = (
    "Max_CFixedPoint(Abs_CFixedPoint(EconomyView.GetAllIncome), '(CFixedPoint)0.01')"
)
EXPENSE_SHARE_DENOMINATOR = (
    "Max_CFixedPoint(Abs_CFixedPoint(EconomyView.GetAllExpense), '(CFixedPoint)0.01')"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate the Workshop-ready EU5 Location Analyzer Economy analysis GUI."
    )
    parser.add_argument("--source", type=Path)
    parser.add_argument("--game-dir", type=Path)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def steam_library_paths() -> list[Path]:
    roots: list[Path] = []
    env_steam = os.environ.get("STEAM_DIR")
    if env_steam:
        roots.append(Path(env_steam))

    if sys.platform == "win32":
        roots.extend([Path(r"C:\Program Files (x86)\Steam"), Path(r"C:\Program Files\Steam")])
    else:
        roots.extend([Path.home() / ".steam" / "steam", Path.home() / ".local" / "share" / "Steam"])

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

    for library in steam_library_paths():
        for game_name in ("Europa Universalis V", "Europa Universalis 5"):
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


def apply_income_expense_share_patches(text: str) -> tuple[str, dict[str, int]]:
    counts: dict[str, int] = {}

    income_pattern = re.compile(
        r"raw_text = \"\[EconomyView\.GetIncome\('([^']+)'\)\|2\+=\]@income!\""
    )

    def replace_income(match: re.Match[str]) -> str:
        category = match.group(1)
        numerator = f"Abs_CFixedPoint(EconomyView.GetIncome('{category}'))"
        return (
            'raw_text = "'
            f"[EconomyView.GetIncome('{category}')|2+=]@income! "
            f"([Divide_CFixedPoint({numerator}, {INCOME_SHARE_DENOMINATOR})|%1])"
            '"'
        )

    text, counts["generic_income_rows"] = income_pattern.subn(replace_income, text)

    expense_pattern = re.compile(
        r"raw_text = \"\[EconomyView\.GetExpense\('([^']+)'\)\|2\+=\]@expense!\""
    )

    def replace_expense(match: re.Match[str]) -> str:
        category = match.group(1)
        numerator = f"Abs_CFixedPoint(EconomyView.GetExpense('{category}'))"
        return (
            'raw_text = "'
            f"[EconomyView.GetExpense('{category}')|2+=]@expense! "
            f"([Divide_CFixedPoint({numerator}, {EXPENSE_SHARE_DENOMINATOR})|%1])"
            '"'
        )

    text, counts["generic_expense_rows"] = expense_pattern.subn(replace_expense, text)

    tax_income_old = 'raw_text = "[TaxRateSetting.GetIncome|2+=]@income!"'
    tax_income_new = (
        'raw_text = "[TaxRateSetting.GetIncome|2+=]@income! '
        f"([Divide_CFixedPoint(Abs_CFixedPoint(TaxRateSetting.GetIncome), {INCOME_SHARE_DENOMINATOR})|%1])"
        '"'
    )
    tax_count = text.count(tax_income_old)
    if tax_count != 1:
        raise SystemExit(f"ERROR: Estate-tax income share expected its vanilla anchor once, found {tax_count}.")
    text = text.replace(tax_income_old, tax_income_new, 1)
    counts["estate_tax_income"] = 1

    minting_old = 'raw_text = "[EconomyView.GetCoinMintingIncome|2+=]@income!"'
    minting_new = (
        'raw_text = "[EconomyView.GetCoinMintingIncome|2+=]@income! '
        f"([Divide_CFixedPoint(Abs_CFixedPoint(EconomyView.GetCoinMintingIncome), {INCOME_SHARE_DENOMINATOR})|%1])"
        '"'
    )
    minting_count = text.count(minting_old)
    if minting_count != 1:
        raise SystemExit(f"ERROR: Minting income share expected its vanilla anchor once, found {minting_count}.")
    text = text.replace(minting_old, minting_new, 1)
    counts["minting_income"] = 1

    if counts["generic_income_rows"] == 0:
        raise SystemExit("ERROR: No generic EconomyView.GetIncome rows were found.")
    if counts["generic_expense_rows"] == 0:
        raise SystemExit("ERROR: No generic EconomyView.GetExpense rows were found.")

    return text, counts


def build(source: Path, output: Path) -> None:
    raw = source.read_bytes()
    source_sha256 = hashlib.sha256(raw).hexdigest()
    text = raw.decode("utf-8-sig")

    if "kevni92.eu5_location_analyzer" in text or "MaintenanceSetting.GetSliderValue|0%V] | [Divide_CFixedPoint" in text:
        raise SystemExit(
            "ERROR: The selected source already appears to be patched. "
            "Point --source at the vanilla game file, not the mod output."
        )

    patched = text
    for patch_name, old, new in PATCHES:
        patched = apply_patch_once(patched, patch_name, old, new)

    patched, dynamic_counts = apply_income_expense_share_patches(patched)

    header = (
        "# EU5 Location Analyzer - generated Economy analysis override\n"
        "# Mod id: kevni92.eu5_location_analyzer\n"
        f"# Vanilla source SHA256: {source_sha256}\n"
        "# Slider format: <slider %> | <share of total expenses %>B\n"
        "# Fixed row format: <gold amount> (<share of total side %>)\n"
        "# Generated by tools/build_debug_gui.py; do not hand-edit this generated file.\n\n"
    )

    output = output.expanduser()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(header + patched, encoding="utf-8-sig", newline="\n")

    print("EU5 Location Analyzer Economy analysis GUI generated successfully.")
    print(f"Source : {source}")
    print(f"SHA256 : {source_sha256}")
    print(f"Output : {output}")
    print("Applied fixed patches:")
    for patch_name, _, _ in PATCHES:
        print(f"  - {patch_name}")
    print("Applied dynamic budget-share patches:")
    for name, count in dynamic_counts.items():
        print(f"  - {name}: {count}")
    print("\nDisplay formats:")
    print("  Slider expense: 25% | 4.2%B")
    print("  Fixed income : +43.91 (39.3%)")
    print("  Fixed expense: -14.47 (14.6%)")
    print("  R-prefixed Wealth/Tax Base values are reconstruction probes only.")


def main() -> None:
    args = parse_args()
    source = find_source(args)
    build(source, args.output)


if __name__ == "__main__":
    main()
