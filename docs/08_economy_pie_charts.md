# Economy Pie Charts – 0.3.1-alpha

## Ziel

Die Balance-Seite der Economy-Ansicht erhält einen **gemeinsamen Analyseblock direkt unterhalb der Vanilla-Zeile `Income / Expenses` und oberhalb der eigentlichen Listen**.

Der Block enthält:

- links: **Income Breakdown** in klar unterscheidbaren Grüntönen
- rechts: **Expense Breakdown** in klar unterscheidbaren Rot-/Orange-/Bordeaux-Tönen
- in der Mitte jedes Donuts: die aktuelle Gesamtsumme von Income bzw. Expenses
- pro Slice: eigener Hover-Tooltip mit Name, Monatswert und Anteil an der jeweiligen Gesamtsumme

## Runtime-Erkenntnisse aus 0.3.0-alpha

Der erste Prototyp hat technisch gerendert, aber drei UX-/Runtime-Probleme gezeigt:

1. Die Charts wurden an zwei verschiedenen Stellen innerhalb der linken und rechten Listen eingefügt. Dadurch lagen sie vertikal versetzt zwischen normalen Budgetzeilen.
2. Die Farbpalette war zu ähnlich, sodass einzelne Slices visuell kaum voneinander zu unterscheiden waren.
3. Die Slice-Tooltips reagierten nicht, weil die Slices zwar `raw_tooltip`/`tooltip` erhielten, aber nicht konsequent mit dem von Vanilla verwendeten `tagtooltip_enabled = yes` konfiguriert waren.

0.3.1-alpha korrigiert genau diese drei Punkte.

## Vanilla-Grundlage

EU5/Jomini besitzt native `piechart`- und `pieslice`-Widgets. Vanilla nutzt für interaktive Slices das Muster:

- `value` für die Segmentgröße
- `color` für die Segmentfarbe
- `tagtooltip_enabled = yes`
- eigenen Tooltip pro Slice
- `piechart_angles` für die Kreisgeometrie

Die Mod bleibt bei diesen nativen Widgets und benötigt dafür keine Scripted GUI.

## Platzierung

Der Builder sucht in der aktuellen Vanilla-Datei zunächst den eindeutigen Header:

```text
name = "income_and_expenses"
```

Danach wird der nächste `scroll_list = {`-Block gesucht. Der gemeinsame Pie-Analyseblock wird unmittelbar **vor** diesem Scroll-Listenblock eingefügt.

Damit stehen beide Charts:

- auf derselben Höhe
- in einem gemeinsamen sichtbaren Panel
- direkt zwischen `Income / Expenses` und den Budgetlisten

und sind nicht mehr Bestandteil der beiden unterschiedlichen Listenflüsse.

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

Dadurch geht auch Building Maintenance in das Expense-Diagramm ein, obwohl diese Zeile keinen Slider besitzt.

## Center-Werte

In der Mitte des Income-Donuts wird angezeigt:

```text
EconomyView.GetAllIncome
```

In der Mitte des Expense-Donuts:

```text
EconomyView.GetAllExpense
```

Die Summe ist als separates, zentriertes Text-Widget über dem Donut gerendert und nicht Bestandteil des Piecharts selbst.

## Farben

Die 0.3.0-Palette war visuell zu homogen. 0.3.1 verwendet deutlich stärkere Helligkeits- und Sättigungsabstände innerhalb derselben Farbfamilie.

Income reicht von dunklem Waldgrün über kräftiges Grün und Türkisgrün bis zu hellem Olivgrün.

Expenses reicht von dunklem Bordeaux über kräftiges Rot und Magentarot bis zu Orange-/Rosttönen.

Dynamische Datamodel-Slices wechseln zyklisch durch diese Paletten.

## Tooltips

Alle Slices erhalten jetzt explizit:

```text
tagtooltip_enabled = yes
```

Statische Slices zeigen:

- Kategoriename
- monatlichen Goldwert
- Anteil am gesamten Income bzw. Expense

Dynamische Estate- und Maintenance-Slices zeigen ebenfalls:

- vom Spiel gelieferten Namen
- realen Monatswert
- Anteil an der jeweiligen Gesamtsumme

Beispiel:

```text
Fort Maintenance: -22.54 (13.9%)
```

## Builder-Architektur

`tools/build_debug_gui.bat` führt weiterhin zwei Schritte aus:

1. `build_debug_gui.py` erzeugt den Economy-Override aus der lokal installierten Vanilla-Datei.
2. `add_economy_pies.py` entdeckt die vorhandenen Income-/Expense-Kategorien und injiziert den gemeinsamen Analyseblock.

Damit bleibt die Mod gegen kleinere Vanilla-Änderungen deutlich robuster als ein statischer kompletter GUI-Snapshot.

## Nächster Runtime-Test

Nach `git pull` und `tools\\build_debug_gui.bat` prüfen:

- beide Donuts stehen direkt nebeneinander im selben Panel
- sie stehen vollständig oberhalb der Budgetlisten
- Income- und Expense-Summe stehen lesbar in der Donut-Mitte
- die Slices sind durch deutlich unterschiedliche Farbtöne erkennbar
- Hover auf jedem Slice zeigt einen Tooltip
- dynamische Estate-/Maintenance-Slices sind weiterhin Bestandteil desselben Charts

Falls die Slices trotz der stärkeren Palette weiterhin nicht sauber getrennt sichtbar sind, ist der nächste Schritt nicht weiteres Farb-Tuning, sondern eine Umstellung des Datenmodells auf einen einzigen vereinheitlichten Pie-Datamodel-Pfad.
