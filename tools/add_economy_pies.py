#!/usr/bin/env python3
"""Inject a shared Income/Expense pie analysis panel into the generated EU5 Economy GUI."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = REPO_ROOT / "in_game" / "gui" / "economy_lateralview.gui"
MARKER = "# ELA economy breakdown pie panel"

INCOME_COLORS = [
    (0.05, 0.28, 0.08, 1.0),
    (0.08, 0.45, 0.13, 1.0),
    (0.18, 0.62, 0.18, 1.0),
    (0.42, 0.72, 0.16, 1.0),
    (0.08, 0.50, 0.36, 1.0),
    (0.18, 0.70, 0.50, 1.0),
    (0.38, 0.55, 0.10, 1.0),
    (0.58, 0.68, 0.20, 1.0),
]

EXPENSE_COLORS = [
    (0.30, 0.03, 0.05, 1.0),
    (0.47, 0.05, 0.07, 1.0),
    (0.66, 0.07, 0.10, 1.0),
    (0.86, 0.12, 0.11, 1.0),
    (0.60, 0.10, 0.27, 1.0),
    (0.82, 0.27, 0.14, 1.0),
    (0.52, 0.20, 0.10, 1.0),
    (0.78, 0.40, 0.18, 1.0),
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
    parser.add_argument("--source", type=Path)
    parser.add_argument("--game-dir", type=Path)
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


def static_slice(
    value_expr: str,
    tooltip: str,
    color: tuple[float, float, float, float],
    indent: str,
) -> str:
    return (
        f'{indent}pieslice = {{\n'
        f'{indent}\ttexture = "gfx/interface/pie_charts/piechart_alpha.dds"\n'
        f'{indent}\ttexture_density = 2\n'
        f'{indent}\tvalue = "[FixedPointToFloat(Abs_CFixedPoint({value_expr}))]"\n'
        f'{indent}\tcolor = {color_text(color)}\n'
        f'{indent}\ttagtooltip_enabled = yes\n'
        f'{indent}\traw_tooltip = "{tooltip}"\n'
        f'{indent}\talpha = 0.99\n'
        f'{indent}}}\n'
    )


def dynamic_slices(
    *,
    value_expr: str,
    tooltip_expr: str,
    colors: list[tuple[float, float, float, float]],
    indent: str,
) -> str:
    blocks: list[str] = []
    modulo = len(colors)
    for index, color in enumerate(colors):
        current_index = "PdxGuiWidget.GetIndexInDataModel"
        visible_expr = (
            f"[And(Not(EqualTo_CFixedPoint(Abs_CFixedPoint({value_expr}), '(CFixedPoint)0')), "
            f"EqualTo_int32(Modulo_int32({current_index}, '(int32){modulo}'), '(int32){index}'))]"
        )
        blocks.append(
            f'{indent}pieslice = {{\n'
            f'{indent}\tvisible = "{visible_expr}"\n'
            f'{indent}\ttexture = "gfx/interface/pie_charts/piechart_alpha.dds"\n'
            f'{indent}\ttexture_density = 2\n'
            f'{indent}\tvalue = "[FixedPointToFloat(Abs_CFixedPoint({value_expr}))]"\n'
            f'{indent}\tcolor = {color_text(color)}\n'
            f'{indent}\ttagtooltip_enabled = yes\n'
            f'{indent}\traw_tooltip = "{tooltip_expr}"\n'
            f'{indent}\talpha = 0.99\n'
            f'{indent}}}\n'
        )
    return "".join(blocks)


def make_pie(
    *,
    side: str,
    categories: list[str],
    indent: str,
) -> str:
    is_income = side == "income"
    colors = INCOME_COLORS if is_income else EXPENSE_COLORS
    labels = INCOME_LABELS if is_income else EXPENSE_LABELS
    total_expr = "EconomyView.GetAllIncome" if is_income else "EconomyView.GetAllExpense"
    getter = "GetIncome" if is_income else "GetExpense"
    icon = "@income!" if is_income else "@expense!"

    parts: list[str] = [
        f'{indent}piechart = {{\n',
        f'{indent}\tparentanchor = center\n',
        f'{indent}\tsize = {{ 104 104 }}\n',
        f'{indent}\tusing = piechart_angles\n',
        f'{indent}\ticon = {{\n',
        f'{indent}\t\tsize = {{ 100% 100% }}\n',
        f'{indent}\t\tparentanchor = center\n',
        f'{indent}\t\ttexture = "gfx/interface/pie_charts/piechart_alpha.dds"\n',
        f'{indent}\t\ttexture_density = 2\n',
        f'{indent}\t\tcolor = {{ 0.02 0.02 0.02 0.35 }}\n',
        f'{indent}\t}}\n',
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
                f"Minting: [EconomyView.GetCoinMintingIncome|2+=]@income! ({mint_share})",
                colors[static_index % len(colors)],
                indent + "\t",
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
                f"Stability: [EconomyView.GetStabilityInvestmentExpense|2+=]@expense! ({stability_share})",
                colors[static_index % len(colors)],
                indent + "\t",
            )
        )
        static_index += 1

    for category in categories:
        label = labels.get(category, pretty_key(category))
        value_expr = f"EconomyView.{getter}('{category}')"
        share = (
            f"[Divide_CFixedPoint(Abs_CFixedPoint({value_expr}), "
            f"Max_CFixedPoint(Abs_CFixedPoint({total_expr}), '(CFixedPoint)0.01'))|%1]"
        )
        tooltip = f"{label}: [{value_expr}|2+=]{icon} ({share})"
        parts.append(
            static_slice(
                value_expr,
                tooltip,
                colors[static_index % len(colors)],
                indent + "\t",
            )
        )
        static_index += 1

    if is_income:
        parts.extend(
            [
                f'{indent}\tdatamodel = "[EconomyView.GetTaxRateSettings]"\n',
                f'{indent}\titem = {{\n',
                dynamic_slices(
                    value_expr="TaxRateSetting.GetIncome",
                    tooltip_expr=(
                        "[TaxRateSetting.GetEstate.GetName]: "
                        "[TaxRateSetting.GetIncome|2+=]@income! "
                        "([Divide_CFixedPoint(Abs_CFixedPoint(TaxRateSetting.GetIncome), "
                        "Max_CFixedPoint(Abs_CFixedPoint(EconomyView.GetAllIncome), '(CFixedPoint)0.01'))|%1])"
                    ),
                    colors=colors,
                    indent=indent + "\t\t",
                ),
                f'{indent}\t}}\n',
            ]
        )
    else:
        parts.extend(
            [
                f'{indent}\tdatamodel = "[EconomyView.GetMaintenanceSettings]"\n',
                f'{indent}\titem = {{\n',
                dynamic_slices(
                    value_expr="MaintenanceSetting.GetExpense",
                    tooltip_expr=(
                        "[MaintenanceSetting.GetName]: "
                        "[MaintenanceSetting.GetExpense|2+=]@expense! "
                        "([Divide_CFixedPoint(Abs_CFixedPoint(MaintenanceSetting.GetExpense), "
                        "Max_CFixedPoint(Abs_CFixedPoint(EconomyView.GetAllExpense), '(CFixedPoint)0.01'))|%1])"
                    ),
                    colors=colors,
                    indent=indent + "\t\t",
                ),
                f'{indent}\t}}\n',
            ]
        )

    parts.append(f'{indent}}}\n')
    return "".join(parts)


def make_card(
    *,
    side: str,
    categories: list[str],
    indent: str,
) -> str:
    is_income = side == "income"
    title = "Income Breakdown" if is_income else "Expense Breakdown"
    total_expr = "EconomyView.GetAllIncome" if is_income else "EconomyView.GetAllExpense"
    total_icon = "@income!" if is_income else "@expense!"

    inner = indent + "\t"
    chart_widget = inner + "\t\t"

    return (
        f'{indent}widget = {{\n'
        f'{inner}layoutpolicy_horizontal = expanding\n'
        f'{inner}size = {{ -1 132 }}\n'
        f'{inner}using = bg_paper_card\n'
        f'{inner}using = bg_cabinet_card_frame\n'
        f'{inner}vbox = {{\n'
        f'{inner}\tmargin = {{ 6 5 }}\n'
        f'{inner}\tspacing = 2\n'
        f'{inner}\ttext_single = {{\n'
        f'{inner}\t\tsize = {{ 100% 20 }}\n'
        f'{inner}\t\tautoresize = no\n'
        f'{inner}\t\talign = hcenter|nobaseline\n'
        f'{inner}\t\traw_text = "{title}"\n'
        f'{inner}\t\tusing = Font_Type_Headers\n'
        f'{inner}\t}}\n'
        f'{inner}\twidget = {{\n'
        f'{inner}\t\tlayoutpolicy_horizontal = expanding\n'
        f'{inner}\t\tsize = {{ -1 106 }}\n'
        + make_pie(side=side, categories=categories, indent=chart_widget)
        + f'{inner}\t\ttext_single = {{\n'
        f'{inner}\t\t\tignore_layout = yes\n'
        f'{inner}\t\t\tparentanchor = center\n'
        f'{inner}\t\t\twidgetanchor = center\n'
        f'{inner}\t\t\tautoresize = yes\n'
        f'{inner}\t\t\talign = hcenter|nobaseline\n'
        f'{inner}\t\t\traw_text = "[{total_expr}|2]{total_icon}"\n'
        f'{inner}\t\t\tusing = Font_Size_Medium\n'
        f'{inner}\t\t}}\n'
        f'{inner}\t}}\n'
        f'{inner}}}\n'
        f'{indent}}}\n'
    )


def make_panel(
    *,
    income_categories: list[str],
    expense_categories: list[str],
    indent: str,
) -> str:
    card_indent = indent + "\t"
    return (
        f'{indent}{MARKER}\n'
        f'{indent}widget = {{\n'
        f'{indent}\tsize = {{ -1 140 }}\n'
        f'{indent}\tusing = bg_secondary_inner_image_alt\n'
        f'{indent}\thbox = {{\n'
        f'{indent}\t\tmargin = {{ 5 5 }}\n'
        f'{indent}\t\tspacing = 5\n'
        + make_card(side="income", categories=income_categories, indent=card_indent + "\t")
        + make_card(side="expense", categories=expense_categories, indent=card_indent + "\t")
        + f'{indent}\t}}\n'
        f'{indent}}}\n\n'
    )


def find_scroll_list_anchor(text: str) -> re.Match[str]:
    marker = 'name = "income_and_expenses"'
    marker_count = text.count(marker)
    if marker_count != 1:
        raise SystemExit(
            f"ERROR: Expected the Economy income/expense header marker once, found {marker_count}."
        )

    start = text.index(marker)
    pattern = re.compile(r'(?m)^(?P<indent>[ \t]*)scroll_list = \{\s*$')
    match = pattern.search(text, start)
    if match is None:
        raise SystemExit(
            "ERROR: Could not find the Economy scroll_list immediately after the income/expense header."
        )
    return match


def main() -> None:
    args = parse_args()
    output = args.output.expanduser()
    if not output.is_file():
        raise SystemExit(f"ERROR: Generated economy GUI not found: {output}")

    text = output.read_text(encoding="utf-8-sig")
    if MARKER in text:
        raise SystemExit("ERROR: Economy pie panel is already present in the generated GUI.")

    income_categories = unique(
        re.findall(
            r'raw_text = "\[EconomyView\.GetIncome\(\'([^\']+)\'\)\|2\+=\]@income!',
            text,
        )
    )
    expense_categories = unique(
        re.findall(
            r'raw_text = "\[EconomyView\.GetExpense\(\'([^\']+)\'\)\|2\+=\]@expense!',
            text,
        )
    )

    if not income_categories:
        raise SystemExit("ERROR: Could not discover generic income categories in generated Economy GUI.")
    if not expense_categories:
        raise SystemExit("ERROR: Could not discover generic expense categories in generated Economy GUI.")

    anchor = find_scroll_list_anchor(text)
    panel = make_panel(
        income_categories=income_categories,
        expense_categories=expense_categories,
        indent=anchor.group("indent"),
    )
    text = text[: anchor.start()] + panel + text[anchor.start() :]

    output.write_text(text, encoding="utf-8-sig", newline="\n")

    print("Economy pie analysis panel injected successfully.")
    print("  Placement: one shared block directly below the Income / Expenses header")
    print(f"  Income static categories : {len(income_categories) + 1} + dynamic estate taxes")
    print(f"  Expense static categories: {len(expense_categories) + 1} + dynamic maintenance settings")
    print("  Income palette: high-contrast green tones")
    print("  Expense palette: high-contrast red/orange tones")
    print("  Slice hover: raw tooltip with name, monthly value and total-side share")
    print("  Donut center: current total Income / Expense")


if __name__ == "__main__":
    main()
