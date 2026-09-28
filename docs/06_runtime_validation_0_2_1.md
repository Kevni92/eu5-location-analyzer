# 06 – Economy Analysis UI Runtime-Validierung 0.2.1

Stand: 2026-09-28

## Zweiter Ingame-Test

Der zweite Test bestätigt die zentralen Expense-/Slider-Getter auch bei realen Nicht-Null-Werten.

Beobachtet wurden unter anderem:

```text
Economic Base:        287.80
Wealth:               359.26
Income:               +98.80
Expenses:             -114.94
Court:                -31.97 / Slider 100% / Budget 27.8%
Army:                  -3.85 / Slider 100% / Budget 3.3%
Navy:                  -7.32 / Slider 100% / Budget 6.3%
Fort:                 -22.09 / Slider 98%  / Budget 19.2%
Diplomatic Spending: -15.82 / Slider 50%  / Budget 13.7%
Food:                   0.00 / Slider 100% / Budget 0.0%
Stability:            -20.42 / Slider 100% / Budget 17.7%
Building Maintenance: -13.43
```

Damit ist insbesondere der separate Stability-Pfad zur Laufzeit bestätigt:

```text
EconomyView.GetDefaultStabilityInvestment
EconomyView.GetStabilityInvestmentExpense
EconomyView.GetAllExpense
```

Die generischen Maintenance-/Spending-Karten sind ebenfalls bestätigt:

```text
MaintenanceSetting.GetSliderValue
MaintenanceSetting.GetExpense
EconomyView.GetAllExpense
```

## Tax Base / Wealth

Der zweite Test zeigte, dass die verschachtelte Guard-Expression

```text
Select_CFixedPoint(GreaterThan_CFixedPoint(...), Divide_CFixedPoint(...), 0)
```

im `text`-Pfad des Tax-Base-Subheaders nicht lokalisiert/aufgelöst wird. Das Log meldete `FetchData failed` bzw. `PdxDataFetchLocalizedData failed` für genau diese Expression.

Version `0.2.1-alpha` entfernt deshalb die verschachtelte `Select_CFixedPoint`-Expression und verwendet direkt:

```text
Divide_CFixedPoint(Player.GetTotalTaxBase, Player.GetTotalWealth)
```

Für normale spielbare Länder ist `Wealth > 0`; ein theoretischer Zero-Wealth-Sonderfall wird bewusst nicht durch eine erneut verschachtelte Localization-Expression abgesichert.

Für die im Test sichtbaren Werte wäre die erwartete Anzeige:

```text
Tax Base: 287.80 (80.1%)
```

weil `287.80 / 359.26 ≈ 0.8011`.

## Status

Nach diesem Test gelten als runtime-validiert:

- Sliderstellung generischer Maintenance-/Spending-Settings,
- tatsächlicher monatlicher Aufwand dieser Settings,
- Budgetanteil an den gesamten Monatsausgaben,
- Stability-Sliderstellung,
- Stability-Ausgabe,
- Gesamt-Einnahmen und Gesamt-Ausgaben als numerische EconomyView-Getter.

Offen ist nur noch die erneute Ingame-Bestätigung der vereinfachten Tax-Base/Wealth-Anzeige aus `0.2.1-alpha`.
