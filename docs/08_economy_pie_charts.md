# Economy Pie Charts – 0.3.0-alpha

## Ziel

Die Balance-Seite der Economy-Ansicht erhält zwei kompakte Tortendiagramme:

- links: **Income Breakdown** in Grüntönen
- rechts: **Expense Breakdown** in Rot-/Orangetönen

Die Diagramme sollen auf einen Blick zeigen, welche Einnahme- bzw. Ausgabenblöcke das Monatsbudget dominieren. Jeder Slice ist hoverbar und liefert einen Tooltip zur zugehörigen Kategorie.

## Vanilla-Grundlage

EU5/Jomini besitzt ein natives `piechart`/`pieslice`-Widget. Vanilla nutzt dynamische Pie-Charts unter anderem für Market-Value-Contributions und Population-Auswertungen. Pie-Slices können Wert, Farbe und eigenen Tooltip erhalten.

Für die Economy-Seite liegen die Daten allerdings nicht in einem einzigen fertigen Contribution-Datamodel vor. Deshalb kombiniert der Prototyp mehrere vorhandene Economy-Datenquellen.

## Datenquellen

### Income

Statische Slices:

- `EconomyView.GetCoinMintingIncome`
- alle im Vanilla-GUI entdeckten `EconomyView.GetIncome('<category>')`-Kategorien

Dynamische Slices:

- `EconomyView.GetTaxRateSettings`
- Wert pro Estate: `TaxRateSetting.GetIncome`
- Tooltip-Bezeichnung: `TaxRateSetting.GetEstate.GetName`

### Expenses

Statische Slices:

- `EconomyView.GetStabilityInvestmentExpense`
- alle im Vanilla-GUI entdeckten `EconomyView.GetExpense('<category>')`-Kategorien

Dynamische Slices:

- `EconomyView.GetMaintenanceSettings`
- Wert pro Maintenance-Eintrag: `MaintenanceSetting.GetExpense`
- Tooltip-Bezeichnung: `MaintenanceSetting.GetName`

Damit kann insbesondere auch Building Maintenance in das Expense-Diagramm eingehen, obwohl diese Zeile keinen Slider besitzt.

## Farben

Income verwendet mehrere abgestufte Grüntöne. Expenses verwendet mehrere Rot-/Orange-/Bordeaux-Töne.

Für dynamische Datamodel-Slices wird die Farbe anhand von `PdxGuiWidget.GetIndexInDataModel` zyklisch aus einer Palette gewählt. Dadurch bleiben benachbarte Slices unterscheidbar, ohne dass für jede mögliche Estate- oder Maintenance-Art eine harte Zuordnung nötig ist.

## Tooltips

Statische Slices zeigen im Prototyp:

- Kategoriename
- monatlichen Goldwert
- Anteil am gesamten Income bzw. Expense

Dynamische Estate-/Maintenance-Slices zeigen zunächst den vom Spiel gelieferten Namen der jeweiligen Kategorie. Nach erfolgreicher Runtime-Validierung kann der Tooltip zusätzlich um Goldwert und prozentualen Anteil erweitert werden.

## Builder-Architektur

`tools/build_debug_gui.bat` führt jetzt zwei Schritte aus:

1. `build_debug_gui.py` erzeugt wie bisher den aktuellen Economy-Override auf Basis der lokal installierten Vanilla-Datei.
2. `add_economy_pies.py` entdeckt die vorhandenen Income-/Expense-Kategorien und injiziert die beiden Pie-Charts an den Vanilla-Ankern der linken und rechten Budgetspalte.

Dadurch bleibt der bestehende Ansatz erhalten, keine komplette 1.3-GUI statisch im Repository einzufrieren.

## Offener Runtime-Test

Noch nicht durch einen Screenshot validiert ist die Kombination aus:

- direkt definierten statischen `pieslice`-Elementen und
- zusätzlichen über `datamodel`/`item` erzeugten Slices

innerhalb desselben `piechart`-Widgets.

Die Einzelmechanismen sind aus Vanilla belegt; die gemischte Verwendung im selben Pie ist der zentrale Testpunkt von 0.3.0-alpha.

Falls Jomini diese Kombination nicht akzeptiert, wird die Darstellung im nächsten Schritt auf eine Variante umgestellt, die statische und dynamische Beiträge anders aggregiert bzw. in getrennten Datenpfaden rendert.

## Erwarteter Test

Nach `git pull` und `tools\\build_debug_gui.bat`:

- Economy öffnen
- links oberhalb der Income-Liste sollte ein grünes Pie erscheinen
- rechts oberhalb der Expense-Liste sollte ein rotes Pie erscheinen
- einzelne Slices mit der Maus testen
- Screenshot der gesamten Balance-Seite senden
- bei fehlenden oder fehlerhaften Diagrammen relevante `error.log`-Zeilen mitsenden
