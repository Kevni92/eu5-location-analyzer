# 05 – Economy Debug GUI MVP

Stand: 2026-09-28

## Zweck

Diese Version ist absichtlich keine finale Economy-UI. Sie ist ein diagnostischer MVP, der mit möglichst kleinen Änderungen an der Vanilla-Economy-Seite genau die Werte sichtbar macht, die für die nächste Designrunde benötigt werden.

## Technischer Ansatz

`in_game/gui/economy_lateralview.gui` wird in EU5 als Whole-file-Override behandelt. Deshalb wird keine dauerhaft eingecheckte Vanilla-Kopie gepflegt. `tools/build_debug_gui.py` nimmt die aktuell installierte Vanilla-Datei und erzeugt daraus die Mod-Datei.

Der Builder verlangt für jeden Patch genau einen erwarteten Vanilla-Anker. Ändert Paradox die Datei so, dass ein Anker fehlt oder mehrfach vorkommt, bricht der Build ab. Das ist gewollt.

## Verifizierte Budget-Getter

Die Recherche nach dem ersten Entwurf hat einen wichtigen offenen Punkt geklärt. Vanilla verwendet in `in_game/gui/shared/topbar_tooltips.gui` direkt:

```text
EconomyView.GetAllIncome
EconomyView.GetAllExpense
```

Damit stehen numerische Gesamtwerte für monatliche Einnahmen und Ausgaben zur Verfügung.

Für einzelne generische Maintenance-/Spending-Einträge ist zusätzlich `MaintenanceSetting.GetExpense` in aktuellen 1.3-UI-Implementierungen belegt. Für die Debuganzeige wird der Betrag mit `Abs_CFixedPoint` normalisiert, damit die Budgetquote unabhängig von der Vorzeichenkonvention positiv dargestellt wird.

## Debug-Patches

### 1. Tax Base / Wealth

Vanilla:

```text
Tax Base: <absolute value>
```

Debug:

```text
Tax Base: <absolute value> | <Tax Base / Wealth %> W
```

Berechnung:

```text
Taxable Wealth Share = Total Tax Base / max(Total Wealth, 0.01)
```

Die `0.01` dient nur als Schutz vor Division durch null. Für normale Länder mit Wealth > 0 entspricht der Wert exakt `Tax Base / Wealth`.

Verwendete Zugriffe:

- `Player.GetTotalTaxBase`
- `Player.GetTotalWealth`
- `Divide_CFixedPoint`
- `Max_CFixedPoint`

### 2. Generische Maintenance-/Spending-Slider

Die Vanilla-Karte zeigt bereits den tatsächlichen monatlichen Aufwand über:

```text
MaintenanceSetting.GetExpenseWithCurrency
```

Der Debug-MVP ersetzt den sekundären Benefit-Text temporär durch eine kompakte Diagnose:

```text
25%|4%B
```

Bedeutung:

```text
25 % = MaintenanceSetting.GetSliderValue
 4 % = abs(MaintenanceSetting.GetExpense) / abs(EconomyView.GetAllExpense)
 B   = Budget / total monthly expenses
```

Damit stehen im selben Screenshot pro generischem Slider zur Verfügung:

- Name,
- absolute monatliche Kosten,
- Sliderstellung in Prozent,
- Anteil an den gesamten Monatsausgaben.

Die finale UI soll den ursprünglichen Benefit-Text wieder erhalten; der Debug-MVP opfert ihn nur für Platz und maximale Robustheit.

### 3. Stability Investment

Vanilla zeigt oben bereits:

```text
EconomyView.GetStabilityInvestmentExpense
```

Der Debug-MVP ersetzt unten temporär die Stability-Change-Anzeige durch dasselbe kompakte Format:

```text
25%|4%B
```

Dabei gilt:

```text
Slider % = EconomyView.GetDefaultStabilityInvestment
Budget % = abs(EconomyView.GetStabilityInvestmentExpense) / abs(EconomyView.GetAllExpense)
```

Damit sind absolute Kosten, Sliderstellung und Budgetanteil gleichzeitig sichtbar.

## Was bewusst noch nicht in die Karte gepackt wird

Da `EconomyView.GetAllIncome` nun ebenfalls verifiziert ist, kann später auch berechnet werden:

```text
Slider Income Burden = Slider Expense / Total Monthly Income
```

Der Debug-MVP zeigt zunächst nur den Anteil an den Gesamtausgaben (`B`), damit die bestehende 60-Pixel-Zeile nicht überladen wird. Der Einkommensanteil ist für die finale Tooltip-/Detaildarstellung vorgemerkt.

## Gewünschte Screenshots nach dem Build

### Screenshot A – Kopf der Economy-Seite

Sichtbar sollen sein:

- Economic Base,
- Wealth,
- Tax Base inklusive neuem Prozentwert,
- Tax Efficiency,
- oberer Teil des Balance-Diagramms.

Ziel: Platzbedarf und Format des Wealth/Tax-Base-Verhältnisses beurteilen.

### Screenshot B – relevante Ausgaben-Slider

Sichtbar sollen möglichst gleichzeitig sein:

- Slidername,
- monatliche Kosten,
- Debugwert `Slider%|Budget%B`,
- bei Stability die Stability-Karte.

Besonders wichtig:

- Stability,
- Diplomacy,
- Court/Government-/Legitimacy-bezogene Settings,
- sonstige Settings, die über `EconomyView.GetMaintenanceSettings` erscheinen.

Ziel: feststellen, welche gewünschten Slider tatsächlich über den generischen `MaintenanceSetting`-Datamodel laufen und wie viel horizontaler Platz für zusätzliche Kennzahlen existiert.

### Screenshot C – optional mit Tooltips

Zusätzlich hilfreich:

- Income-Header-Tooltip (`GetAllIncomeInfo`),
- Expense-Header-Tooltip (`GetAllExpenseInfo`),
- Tooltip eines relevanten Spending-Sliders.

## Fehlerdiagnose

Falls die Seite nicht korrekt lädt, bitte zusätzlich relevante Zeilen aus `error.log` bereitstellen. Interessante Suchbegriffe:

```text
economy_lateralview
MaintenanceSetting
GetSliderValue
GetExpense
GetAllExpense
Divide_CFixedPoint
Abs_CFixedPoint
Max_CFixedPoint
GetDefaultStabilityInvestment
```

Ein fehlgeschlagener Probe-Getter ist in dieser Phase ein verwertbares Ergebnis und wird anschließend aus der finalen UI entfernt bzw. durch einen belegten Zugriff ersetzt.

## Kompatibilität

Der erzeugte GUI-Override kollidiert mit jeder anderen Mod, die `in_game/gui/economy_lateralview.gui` ebenfalls ersetzt. Das ist für den Debug-MVP akzeptiert und muss für eine spätere Release-Version explizit behandelt werden.
