# 04 – Economy-Page UI-Erweiterungen

Stand: 2026-09-28

Dieses Dokument beschreibt zusätzliche Economy-UI-Funktionen für den EU5 Location Analyzer. Ziel ist nicht nur die Bewertung einzelner Locations über Map Modes, sondern auch eine bessere Lesbarkeit der landesweiten wirtschaftlichen Zusammenhänge, auf denen diese Bewertung basiert.

## 1. Vanilla-Ausgangspunkt

In der aktuellen Vanilla-`economy_lateralview.gui` stehen oberhalb des Balance-Diagramms vier Kennzahlen:

1. **Economic Base** – `Player.GetEconomicalBase`
2. **Wealth** – `Player.GetTotalWealth`
3. **Tax Base** – `Player.GetTotalTaxBase`
4. **Tax Efficiency** – `Player.GetModifierValueNoFormat('tax_income_efficiency')`

Quelle:

`reference_game_files/game/in_game/gui/economy_lateralview.gui`

Verifizierter Referenzstand beim Entwurf dieses Dokuments:

`HLJSXK/eu5-towards-victory`, Commit `879fb81040a873a5eeb9a9a034621fc6572571e5`.

Direkt unter diesen Kennzahlen wird die jüngste Balance-Historie über `EconomyView.GetRecentBalance` dargestellt.

Wichtig für das Design: **Tax Base und Tax Efficiency sind zwei verschiedene Konzepte.** Der geplante Wealth/Tax-Base-Quotient darf deshalb nicht als Tax Efficiency bezeichnet werden.

---

## 2. Neue Kennzahl: Taxable Wealth Share

### Spielerfrage

> Wie viel meines gesamten Wealth kann der Staat überhaupt als Tax Base erfassen?

Die bestehende Economy-Seite zeigt Wealth und Tax Base als absolute Werte, aber nicht deren Verhältnis.

### Vorgeschlagene Kennzahl

```text
Taxable Wealth Share = Total Tax Base / Total Wealth
```

Als Prozentwert:

```text
Taxable Wealth Share % = (Total Tax Base / Total Wealth) × 100
```

Sonderfall:

```text
wenn Total Wealth <= 0 → kein Prozentwert / N/A
```

### Beispiel

```text
Wealth:                 10,000
Tax Base:                4,200
Taxable Wealth Share:    42.0 %
```

Interpretation:

Nur 42 % des vorhandenen Wealth liegen aktuell in der Tax Base des Staates.

Dieser Wert ist **nicht** dasselbe wie ein einfacher durchschnittlicher Control-Wert. Er ist vielmehr ein landesweiter, wealth-gewichteter Indikator dafür, welcher Anteil der wirtschaftlichen Basis überhaupt in der Tax Base landet. Falls weitere Mechaniken außer Control die Tax Base beeinflussen, werden sie automatisch im realen Verhältnis sichtbar.

### UI-Platzierung

Bevorzugt direkt im vorhandenen Wealth-/Tax-Base-Bereich.

Mögliche Darstellungen:

```text
Wealth        10,000
Tax Base       4,200   (42.0 % of Wealth)
```

oder kompakter:

```text
Tax Base       4,200 | 42.0 %
```

Der Tooltip sollte mindestens enthalten:

```text
Taxable Wealth Share
42.0 % of your country's total Wealth currently contributes to Tax Base.

Tax Base: 4,200
Total Wealth: 10,000
Untaxed / non-tax-base Wealth: 5,800
```

### Sekundäre Kennzahl

Optional kann auch der Gegenwert angezeigt werden:

```text
Non-Tax-Base Wealth Share = 1 - Taxable Wealth Share
```

Im Beispiel wären das 58 %.

Diese Kennzahl ist insbesondere für den Location Analyzer relevant, weil sie auf Landesebene sofort sichtbar macht, wie viel wirtschaftliches Potential aufgrund von Control und anderen Tax-Base-Effekten nicht direkt steuerbar ist.

---

## 3. Verhältnis zu Tax Efficiency

Die bestehende **Tax Efficiency** bleibt unverändert eine eigene Kennzahl.

Die vier Informationen beantworten unterschiedliche Fragen:

| Kennzahl | Frage |
|---|---|
| Economic Base | Wie groß ist die landesweite Bemessungsgrundlage für verschiedene skalierende Mechaniken? |
| Wealth | Wie groß ist das gesamte vorhandene wirtschaftliche Vermögen? |
| Tax Base | Wie viel davon befindet sich in der steuerlich relevanten Basis? |
| Tax Efficiency | Wie effizient arbeitet das Steuersystem auf dieser Basis? |
| Taxable Wealth Share (neu) | Wie groß ist Tax Base relativ zu Wealth? |

Langfristig kann zusätzlich untersucht werden, ob sich eine weitere Kennzahl wie **Effective Wealth Tax Capture** sinnvoll ableiten lässt, z. B. tatsächliches Steueraufkommen relativ zu Wealth. Das ist jedoch eine andere Größe und muss vor Implementierung anhand der echten Tax-Income-Formel verifiziert werden.

---

## 4. Budget-Anteil der Economy-Slider

### Spielerfrage

> Welchen Anteil meines Staatsbudgets kostet mich die aktuelle Einstellung dieses Sliders?

Der absolute Goldbetrag eines Sliders ist zwar relevant, aber schwer einzuordnen. 10 Gold pro Monat können für ein kleines Land existenzbedrohend und für ein großes Land fast bedeutungslos sein.

Daher soll jeder relevante Economy-Slider zusätzlich relative Kosten anzeigen.

### Primäre Kennzahl: Share of Expenses

```text
Slider Expense Share = Current Slider Monthly Cost / Total Monthly Expenses
```

Als Prozentwert:

```text
Slider Expense Share % =
(Current Slider Monthly Cost / Total Monthly Expenses) × 100
```

Beispiel:

```text
Court / Legitimacy spending: 12.0 gold/month
Total expenses:              120.0 gold/month
Budget share:                 10.0 %
```

Diese Kennzahl entspricht am ehesten dem gewünschten „Anteil am Staatshaushalt“.

### Sekundäre Kennzahl: Share of Income

Für Planung ist zusätzlich sinnvoll:

```text
Slider Income Burden = Current Slider Monthly Cost / Total Monthly Income
```

Beispiel:

```text
Court spending:    12.0
Monthly income:   100.0
Income burden:     12.0 %
```

Der Unterschied ist wichtig:

- **Share of Expenses** zeigt, wofür der Staat sein Geld aktuell ausgibt.
- **Share of Income** zeigt, wie viel der gesamten Einnahmen dieser Slider bindet.

Empfehlung:

- direkt am Slider: **Share of Expenses**
- im Tooltip: zusätzlich **Share of Income**

---

## 5. Gewünschte Darstellung pro Slider

Ein Slider sollte mittelfristig ungefähr folgende Informationen liefern:

```text
Diplomatic Spending
[==========----------] 50 %

24.5 gold / month
18.2 % of total expenses
14.7 % of monthly income
```

Alternativ kompakter:

```text
24.5¤ / month | 18.2 % budget
```

Tooltip:

```text
Current monthly cost:      24.5
Share of total expenses:   18.2 %
Share of monthly income:   14.7 %
```

---

## 6. Besonders nützliche Planungskennzahl: marginale Sliderkosten

Da mehrere Economy-Slider an Economic Base skalieren, ist für den Spieler nicht nur die aktuelle Ausgabe interessant, sondern auch:

> Was kostet mich eine Erhöhung dieses Sliders konkret?

Daher sollte geprüft werden, ob zusätzlich angezeigt werden kann:

```text
Cost per +10 percentage points
```

Beispiel:

```text
Current: 25 %
Current cost: 8.0¤ / month
+10 pp would cost: +3.2¤ / month
```

Optional relativ:

```text
+10 pp = +2.1 % of monthly income
```

Das wäre für die praktische Budgetplanung oft aussagekräftiger als nur der momentane Prozentanteil.

Wichtig: Diese Berechnung darf erst als exakt bezeichnet werden, wenn die jeweilige Slider-Kostenformel und alle Efficiency-Modifikatoren vollständig verifiziert sind.

---

## 7. Aggregate Economic-Base Spending Pressure

Da Stability-, Diplomatic- und Court-/Government-Power-Ausgaben zumindest teilweise an Economic Base skalieren, ist später eine aggregierte Kennzahl denkbar:

```text
Economic-Base Spending Pressure =
Summe aller aktuell aktiven Economic-Base-abhängigen Sliderkosten
/ Total Monthly Income
```

Beispiel:

```text
Stability:      0.0
Diplomacy:      4.0
Court:         10.0
-------------------
Total:         14.0
Monthly income: 100.0

EB Spending Pressure: 14.0 %
```

Diese Kennzahl wäre eine gute Brücke zwischen der Economy-Seite und dem Location Analyzer: Sie zeigt landesweit, wie teuer zusätzliche Economic Base unter der aktuellen Spielweise tatsächlich ist.

Bei einer Spielweise mit Stability meistens 0, Diplomacy nur situativ und Court nur moderat kann dieser Wert deutlich niedriger sein als bei dauerhaft hohen Slidern. Genau das soll später in der Location-Bewertung berücksichtigt werden.

---

## 8. Verbindung zum Location Analyzer

Die Economy-Page-Erweiterung soll dieselben Begriffe verwenden wie die Map Modes.

Geplante Verbindung:

```text
Country level:
Wealth
→ Tax Base
→ Taxable Wealth Share
→ actual tax income / slider burden

Location level:
Location Wealth
→ Location Tax Base / Control contribution
→ Direct Fiscal Value
→ Economic-Base Cost
→ Retention Value
```

Dadurch kann der Spieler zuerst auf Landesebene erkennen:

> Mein Land hat viel Wealth, aber nur 38 % davon liegen in der Tax Base.

und anschließend über den Map Mode herausfinden:

> Welche Locations verursachen diesen schlechten Quotienten bzw. welche Locations liefern besonders viel steuerbaren Wert?

---

## 9. Technische Research-Aufgaben vor Implementierung

Vor dem UI-Code müssen folgende Punkte verifiziert werden:

1. Kann in GUI-Script direkt mit `Player.GetTotalTaxBase` und `Player.GetTotalWealth` gerechnet werden, oder ist dafür ein Script Value / Scripted GUI notwendig?
2. Welche API liefert **Total Monthly Expenses** zuverlässig?
3. Welche API liefert **Total Monthly Income** zuverlässig?
4. Lassen sich die aktuellen Monatskosten jedes einzelnen Sliders direkt aus `EconomyView` auslesen?
5. Falls nicht: müssen die Kosten über dieselben Formeln wie das Spiel rekonstruiert werden?
6. Aktualisieren sich eigene GUI-Werte während des Slider-Draggings live genug für eine Vorschau?
7. Können Vanilla-Widgets minimal erweitert werden, ohne den kompletten Economy-Lateralview unnötig zu überschreiben?
8. Welche Override-/Load-Order-Konflikte entstehen mit anderen Economy-UI-Mods?

Bis diese Punkte geprüft sind, ist dies ein **UI-Design und Berechnungskonzept**, noch keine Aussage über die technische Implementierbarkeit jeder Anzeige.

---

## 10. MVP für die Economy-Seite

Der erste sinnvolle Economy-UI-MVP sollte bewusst klein bleiben:

1. **Taxable Wealth Share** neben Tax Base anzeigen.
2. Bei den drei relevanten Economic-Base-Slidern den aktuellen Goldbetrag beibehalten bzw. auslesen.
3. **% of Total Expenses** ergänzen.
4. Im Tooltip zusätzlich **% of Monthly Income** anzeigen.
5. Erst danach marginale `+10 pp`-Kosten und den aggregierten `EB Spending Pressure` ergänzen.

Damit entstehen bereits sehr nützliche Planungsinformationen, ohne sofort das gesamte Economy-UI neu bauen zu müssen.
