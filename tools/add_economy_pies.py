#!/usr/bin/env python3
"""Add Income/Expense pie charts to the generated EU5 economy GUI override."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = REPO_ROOT / "in_game" / "gui" / "economy_lateralview.gui"
MARKER = "# ELA economy breakdown pie charts"

INCOME_COLORS = [
    (0.16, 0.55, 0.25, 1.0),
    (0.22, 0.68, 0.31, 1.0),
    (0.31, 0.78, 0.39, 1.0),
    (0.42, 0.67, 0.24, 1.0),
    (0.14, 0.62, 0.46, 1.0),
    (0.50, 0.76, 0.33, 1.0),
    (0.24, 0.72, 0.55, 1.0),
    (0.37, 0.58, 0.19, 1.0),
]

EXPENSE_COLORS = [
    (0.68, 0.16, 0.17, 1.0),
    (0.82, 0.22, 0.18, 1.0),
    (0.72, 0.29, 0.21, 1.0),
    (0.88, 0.35, 0.22, 1.0),
    (0.58, 0.15, 0.24, 1.0),
    (0.77, 0.30, 0.31, 1.0),
    (0.63, 0.36, 0.23, 1.0),
    (0.86, 0.27, 0.38, 1.0),
]

INCOME_LABELS = {
    "interest": "Interest",
    "trade": "Trade Income",
    "selling_food": "Selling Food",
    "food": "Selling Food",
    "diplomacy": "Diplomacy",
    "io_payments": "Payments",
    "payments": "Payments",
    "mercenary": "Mercenary Income",
    "privateer": "Privateer",
    "foreign_buildings": "Buildings Abroad",
    "buildings_abroad": "Buildings Abroad",
    "other": "Other Incomes",
}

EXPENSE_LABELS = {
    "interest": "Paying Interest",
    "trade": "Trade Expense",
    "diplomacy": "Diplomacy",
    "mercenary": "Hiring Mercenaries",
    "building_subsidies": "Building Subsidies",
    "privateer": "Privateer Maintenance",
    "other": "Other Expenses",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--source", type=Path)  # accepted for compatibility with build_debug_gui.py
    parser.add_argument("--game-dir", type=Path)  # accepted for compatibility
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args, _ = parser.parse_known_args()
    return args


def unique(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value not in seen:
            seen.add(value)
            result.append(value)
    return result


def pretty_key(key: str) -> str:
    return key.replace("_", " ").title()


def color_text(color: tuple[float, float, float, float]) -> str:
    return "{ " + " ".join(f"{component:.2f}" for component in color) + " }"


def static_slice(value_expr: str, tooltip: str, color: tuple[float, float, float, float], indent: str) -> str:
    return (
        f"{indent}pieslice = {{\n"
        f"{indent}\ttexture = \"gfx/interface/pie_charts/piechart_alpha.dds\"\n"
        f"{indent}\ttexture_density = 2\n"
        f"{indent}\tvalue = \"[FixedPointToFloat(Abs_CFixedPoint({value_expr}))]\"\n"
        f"{indent}\tcolor = {color_text(color)}\n"
        f"{indent}\traw_tooltip = \"{tooltip}\"\n"
        f"{indent}\talpha = 0.99\n"
        f"{indent}}}\n"
    )


def dynamic_slices(
    value_expr: str,
    tooltip_expr: str,
    colors: list[tuple[float, float, float, float]],
    indent: str,
) -> str:
    blocks: list[str] = []
    modulo = len(colors)
    for index, color in enumerate(colors):
        visible_expr = (
            "[And(Not(EqualTo_CFixedPoint(Abs_CFixedPoint(" + value_expr + "), '(CFixedPoint)0')), "
            "EqualTo_int32(Modulo_int32(PdxGuiWidget.GetIndexInDataModel, '(int32)" + str(modulo) + "'), '(int32)" + str(index) + "'))]"
        )
        blocks.append(
            f"{indent}pieslice = {{\n"
            f"{indent}\tvisible = \"{visible_expr}\"\n"
            f"{indent}\ttexture = \"gfx/interface/pie_charts/piechart_alpha.dds\"\n"
            f"{indent}\ttexture_density = 2\n"
            f"{indent}\tvalue = \"[Select_float(EqualTo_int32(Modulo_int32(PdxGuiWidget.GetIndexInDataModel, '(int32){modulo}'), '(int32){index}'), FixedPointToFloat(Abs_CFixedPoint({value_expr})), '(float)0')]\"\n"
            f"{indent}\tcolor = {color_text(color)}\n"
            f"{indent}\ttooltip = \"{tooltip_expr}\"\n"
            f"{indent}\talpha = 0.99\n"
            f"{indent}}}\n"
        )
    return "".join(blocks)


def make_chart(
    *,
    title: str,
    side: str,
    categories: list[str],
    indent: str,
) -> str:
    is_income = side == "income"
    colors = INCOME_COLORS if is_income else EXPENSE_COLORS
    labels = INCOME_LABELS if is_income else EXPENSE_LABELS
    total_expr = "EconomyView.GetAllIncome" if is_income else "EconomyView.GetAllExpense"

    pie_indent = indent + "\t\t\t"
    parts = [
        f"{indent}{MARKER}: {side}\n",
        f"{indent}widget = {{\n",
        f"{indent}\tsize = {{ -1 104 }}\n",
        f"{indent}\thbox = {{\n",
        f"{indent}\t\texpand = {{}}\n",
        f"{indent}\t\tvbox = {{\n",
        f"{indent}\t\t\tspacing = 2\n",
        f"{indent}\t\t\ttext_single = {{\n",
        f"{indent}\t\t\t\tautoresize = yes\n",
        f"{indent}\t\t\t\talign = hcenter|nobaseline\n",
        f"{indent}\t\t\t\traw_text = \"{title}\"\n",
        f"{indent}\t\t\t}}\n",
        f"{indent}\t\t\tpiechart = {{\n",
        f"{indent}\t\t\t\tsize = {{ 82 82 }}\n",
        f"{indent}\t\t\t\tparentanchor = hcenter\n",
        f"{indent}\t\t\t\tusing = piechart_angles\n",
        f"{indent}\t\t\t\ticon = {{\n",
        f"{indent}\t\t\t\t\tsize = {{ 100% 100% }}\n",
        f"{indent}\t\t\t\t\tparentanchor = center\n",
        f"{indent}\t\t\t\t\ttexture = \"gfx/interface/pie_charts/piechart_alpha.dds\"\n",
        f"{indent}\t\t\t\t\ttexture_density = 2\n",
        f"{indent}\t\t\t\t\tcolor = {{ 0.05 0.05 0.05 0.30 }}\n",
        f"{indent}\t\t\t\t}}\n",
    ]

    static_index = 0
    if is_income:
        mint_expr = "EconomyView.GetCoinMintingIncome"
        mint_share = (
            "[Divide_CFixedPoint(Abs_CFixedPoint(EconomyView.GetCoinMintingIncome), "
            "Max_CFixedPoint(Abs_CFixedPoint(EconomyView.GetAllIncome), '(CFixedPoint)0.01'))|%1]"
        )
        parts.append(
            static_slice(
                mint_expr,
                f"Minting: [EconomyView.GetCoinMintingIncome|2+=]@gold! ({mint_share})",
                colors[static_index % len(colors)],
                pie_indent + "\t",
            )
        )
        static_index += 1
    else:
        stability_expr = "EconomyView.GetStabilityInvestmentExpense"
        stability_share = (
            "[Divide_CFixedPoint(Abs_CFixedPoint(EconomyView.GetStabilityInvestmentExpense), "
            "Max_CFixedPoint(Abs_CFixedPoint(EconomyView.GetAllExpense), '(CFixedPoint)0.01'))|%1]"
        )
        parts.append(
            static_slice(
                stability_expr,
                f"Stability: [EconomyView.GetStabilityInvestmentExpense|2+=]@gold! ({stability_share})",
                colors[static_index % len(colors)],
                pie_indent + "\t",
            )
        )
        static_index += 1

    getter = "GetIncome" if is_income else "GetExpense"
    icon = "@income!" if is_income else "@expense!"
    for category in categories:
        label = labels.get(category, pretty_key(category))
        value_expr = f"EconomyView.{getter}('{category}')"
        share = (
            f"[Divide_CFixedPoint(Abs_CFixedPoint({value_expr}), "
            f"Max_CFixedPoint(Abs_CFixedPoint({total_expr}), '(CFixedPoint)0.01'))|%1]"
        )
        tooltip = f"{label}: [{value_expr}|2+=]{icon} ({share})"
        parts.append(static_slice(value_expr, tooltip, colors[static_index % len(colors)], pie_indent + "\t"))
        static_index += 1

    if is_income:
        parts.extend(
            [
                f"{indent}\t\t\t\tdatamodel = \"[EconomyView.GetTaxRateSettings]\"\n",
                f"{indent}\t\t\t\titem = {{\n",
                dynamic_slices(
                    "TaxRateSetting.GetIncome",
                    "[TaxRateSetting.GetEstate.GetName]",
                    colors,
                    pie_indent + "\t\t",
                ),
                f"{indent}\t\t\t\t}}\n",
            ]
        )
    else:
        parts.extend(
            [
                f"{indent}\t\t\t\tdatamodel = \"[EconomyView.GetMaintenanceSettings]\"\n",
                f"{indent}\t\t\t\titem = {{\n",
                dynamic_slices(
                    "MaintenanceSetting.GetExpense",
                    "[MaintenanceSetting.GetName]",
                    colors,
                    pie_indent + "\t\t",
                ),
                f"{indent}\t\t\t\t}}\n",
            ]
        )

    parts.extend(
        [
            f"{indent}\t\t\t}}\n",
            f"{indent}\t\t}}\n",
            f"{indent}\t\texpand = {{}}\n",
            f"{indent}\t}}\n",
            f"{indent}}}\n\n",
        ]
    )
    return "".join(parts)


def insert_before_anchor(text: str, anchor: str, chart: str) -> str:
    pattern = re.compile(rf"(?m)^(?P<indent>[ \t]*){re.escape(anchor)}\s*$")
    matches = list(pattern.finditer(text))
    if len(matches) != 1:
        raise SystemExit(f"ERROR: Pie-chart anchor {anchor!r} expected once, found {len(matches)}.")
    match = matches[0]
    return text[: match.start()] + chart + text[match.start() :]


def main() -> None:
    args = parse_args()
    output = args.output.expanduser()
    if not output.is_file():
        raise SystemExit(f"ERROR: Generated economy GUI not found: {output}")

    text = output.read_text(encoding="utf-8-sig")
    if MARKER in text:
        raise SystemExit("ERROR: Economy pie charts are already present in the generated GUI.")

    income_categories = unique(
        re.findall(r"raw_text = \"\[EconomyView\.GetIncome\('([^']+)'\)\|2\+=\]@income!", text)
    )
    expense_categories = unique(
        re.findall(r"raw_text = \"\[EconomyView\.GetExpense\('([^']+)'\)\|2\+=\]@expense!", text)
    )

    if not income_categories:
        raise SystemExit("ERROR: Could not discover generic income categories in generated Economy GUI.")
    if not expense_categories:
        raise SystemExit("ERROR: Could not discover generic expense categories in generated Economy GUI.")

    income_anchor = "#all the estates and their taxes"
    expense_anchor = "#anything that uses maintenance settings"

    income_match = re.search(rf"(?m)^(?P<indent>[ \t]*){re.escape(income_anchor)}\s*$", text)
    expense_match = re.search(rf"(?m)^(?P<indent>[ \t]*){re.escape(expense_anchor)}\s*$", text)
    if income_match is None or expense_match is None:
        raise SystemExit("ERROR: Could not locate Economy income/expense list anchors for pie charts.")

    income_chart = make_chart(
        title="Income Breakdown",
        side="income",
        categories=income_categories,
        indent=income_match.group("indent"),
    )
    text = insert_before_anchor(text, income_anchor, income_chart)

    # Re-find after the first insertion because byte offsets changed.
    expense_match = re.search(rf"(?m)^(?P<indent>[ \t]*){re.escape(expense_anchor)}\s*$", text)
    assert expense_match is not None
    expense_chart = make_chart(
        title="Expense Breakdown",
        side="expense",
        categories=expense_categories,
        indent=expense_match.group("indent"),
    )
    text = insert_before_anchor(text, expense_anchor, expense_chart)

    output.write_text(text, encoding="utf-8-sig", newline="\n")

    print("Economy pie charts injected successfully.")
    print(f"  Income static categories : {len(income_categories) + 1} + dynamic estate taxes")
    print(f"  Expense static categories: {len(expense_categories) + 1} + dynamic maintenance settings")
    print("  Income palette: green tones")
    print("  Expense palette: red tones")
    print("  Hover tooltips: category/setting name; static slices also show value and share")


if __name__ == "__main__":
    main()
