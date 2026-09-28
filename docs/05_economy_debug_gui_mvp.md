# 05 – Economy Debug GUI MVP / Runtime-Validierung

Stand: 2026-09-28

## Zweck

Dieses Dokument beschreibt den diagnostischen Economy-MVP und die Ergebnisse des ersten Ingame-Tests. Aus diesem Test wurde Version `0.2.0-alpha` der Economy Analysis UI abgeleitet.

## Technischer Ansatz

`in_game/gui/economy_lateralview.gui` wird in EU5 als Whole-file-Override behandelt. Deshalb wird keine dauerhaft eingecheckte Vanilla-Kopie gepflegt. `tools/build_debug_gui.py` nimmt die aktuell installierte Vanilla-Datei und erzeugt daraus die Mod-Datei.

Der Builder verlangt für jeden Patch genau einen erwarteten Vanilla-Anker. Ändert Paradox die Datei so, dass ein Anker fehlt oder mehrfach vorkommt, bricht der Build ab. Das ist gewollt.

## Verifizierte Budget-Getter

Vanilla verwendet in `in_game/gui/shared/topbar_tooltips.gui` direkt:

```text
EconomyView.GetAllIncome
EconomyView.GetAllExpense
```

Damit stehen numerische Gesamtwerte für monatliche Einnahmen und Ausgaben zur Verfügung.

Für einzelne generische Maintenance-/Spending-Einträge ist `MaintenanceSetting.GetExpense` verwendbar. Die erste Laufzeitprobe bestätigt außerdem, dass `MaintenanceSetting.GetSliderValue` in der Economy-Seite den tatsächlichen Sliderwert liefert.

Für Stability funktionieren die separaten Zugriffe:

```text
EconomyView.GetDefaultStabilityInvestment
EconomyView.GetStabilityInvestmentExpense
```

## Erster Ingame-Test

Der vom Nutzer getestete Spielstand zeigte unter anderem:

```text
Economic Base:       287.80
Wealth:              359.26
Income:              +40.52
Expenses:            -161.36
Court:               -10.54   / Slider 32% / Debug Budget 6%
Army:                 -3.85   / Slider 100% / Debug Budget 2%
Navy:                 -7.32   / Slider 100% / Debug Budget 4%
Fort:                -22.54   / Slider 100% / Debug Budget 13%
Diplomatic Spending: -15.82   / Slider 50% / Debug Budget 9%
Food:                  0.00   / Slider 100% / Debug Budget 0%
Stability:             0.00   / Slider 0% / Debug Budget 0%
Building Maintenance:-13.43
Trade Expense:       -87.82
```

Damit ist bestätigt, dass die generischen Sliderkarten gleichzeitig ihren realen monatlichen Aufwand, ihre Sliderstellung und ihren Anteil an den gesamten Monatsausgaben darstellen können.

Die erste Debugversion formatierte den Budgetanteil ohne Nachkommastelle. Dadurch wurden Werte effektiv abgeschnitten bzw. zu grob dargestellt. Beispiel: `22.54 / 161.36 ≈ 13.97%`, während die Debuganzeige `13%B` zeigte. Version `0.2.0-alpha` nutzt deshalb eine Nachkommastelle.

## Tax Base / Wealth – gefundener UI-Fehler

Der erste Build zeigte bei Tax Base statt einer Zahl das Wort:

```text
default
```

Die Ursache liegt nicht beim Getter `Player.GetTotalTaxBase`, sondern beim Patch des benannten Vanilla-Blocks. Der Vanilla-Subheader besitzt bereits eine `text`-Property. Der MVP setzte zusätzlich `raw_text`; dadurch blieb die ursprüngliche Default-Textproperty aktiv.

Version `0.2.0-alpha` überschreibt deshalb gezielt `text` und verwendet:

```text
Tax Base (Tax Base / Wealth %)
```

mit einem Nullschutz über das in EU5-GUIs belegte Muster:

```text
Select_CFixedPoint(
    GreaterThan_CFixedPoint(Wealth, 0),
    Divide_CFixedPoint(TaxBase, Wealth),
    0
)
```

Zielanzeige beispielsweise:

```text
287.80 (80.1%)
```

Der Prozentwert ist die `Taxable Wealth Share` und darf nicht mit der daneben stehenden `Tax Efficiency` verwechselt werden.

## Aktuelle Alpha-Anzeige

### Tax Base

```text
<absolute Tax Base> (<Tax Base / Wealth %>)
```

### Maintenance-/Spending-Slider

```text
25% | 4.2%B
```

Bedeutung:

```text
25%   = aktuelle Sliderstellung
4.2%B = Anteil der tatsächlichen aktuellen Sliderkosten an EconomyView.GetAllExpense
```

Der absolute monatliche Goldbetrag bleibt in der Vanilla-Kartenüberschrift sichtbar.

### Stability

Stability verwendet dasselbe Anzeigeformat, wird technisch aber über die separaten `EconomyView`-Getter berechnet.

## Nächste Validierung

Nach Build von `0.2.0-alpha` sollen zwei Dinge geprüft werden:

1. Tax Base muss einen numerischen Wert plus Prozentzahl statt `default` anzeigen.
2. Stability soll einmal mit einem Wert größer als 0 % getestet werden, um den separaten Expense-Pfad auch mit realen Kosten zu validieren.

Diese Tests sind keine Voraussetzung mehr für die UI-Struktur, sondern reine Laufzeitvalidierung.

## Spätere Ausbaustufe

Für die endgültige UI sind zusätzlich vorgesehen:

- ausgeschriebener Tooltip für `Budget share`,
- optional `Slider Expense / Total Monthly Income`,
- marginale Kosten einer Slidererhöhung um +10 Prozentpunkte,
- aggregierter Economic-Base-Spending-Pressure,
- Verbindung dieser Landeskennzahlen mit den späteren Location-Map-Modes.

## Kompatibilität

Der erzeugte GUI-Override kollidiert mit jeder anderen Mod, die `in_game/gui/economy_lateralview.gui` ebenfalls ersetzt. Das bleibt für die Alpha akzeptiert und muss für eine spätere Release-Version explizit behandelt werden.
