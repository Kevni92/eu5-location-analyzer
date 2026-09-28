# 03 – Offene Fragen und Research-Backlog

Stand: 2026-09-28

Dieses Dokument trennt bereits belastbare Erkenntnisse von Punkten, die vor einer exakten Implementierung noch verifiziert werden müssen.

## Priorität A – für einen belastbaren MVP zwingend

### Exakte Tax-Base-/Steuerformel pro Location

Zu klären:

- Wie genau wird Wealth in Tax Base überführt?
- Ist die Beziehung zu Control vollständig linear oder greifen weitere Schritte dazwischen?
- Welche Estate-/Pop-spezifischen Steuersätze wirken?
- Wie greifen Tax Efficiency, Privilegien, Modifikatoren und Sonderregeln ineinander?
- Welche Werte sind in Jomini-Script bzw. Map-Mode-Kontext direkt auslesbar?

Ziel:

Ein belastbarer `Direct Fiscal Value`, der nicht auf einer pauschalen angenommenen Steuerquote beruht.

### Exakter marginaler Economic-Base-Beitrag einer Location

Zu klären:

- Welche Location-Werte speisen den landesweiten `country_economical_base` tatsächlich?
- Wie ist `ECONOMICAL_BASE_FROM_TAX_BASE = 0.5` engine-intern zu interpretieren?
- Wie genau wird Population mit `ECONOMICAL_BASE_FROM_POP = 0.015` skaliert?
- Welche Teile aus Trade Value / Trade Profit lassen sich einer einzelnen Location sinnvoll zurechnen?
- Wie verändern Institutionen den bereits berechneten Wert?

Ziel:

Nicht nur die Economic Base des Landes kennen, sondern den **marginalen Beitrag einer einzelnen Location** approximieren können.

### Verfügbarkeit der Werte im Map-Mode-Scope

Zu prüfen:

- Welche Scopes stehen in einem eigenen EU5 Map Mode zur Verfügung?
- Welche Script Values können pro Location ausgewertet werden?
- Können Owner-Werte wie aktuelle Slider, Economy-Modifier und Subject-Informationen aus dem Location-Scope zuverlässig abgefragt werden?
- Wie teuer sind komplexe Berechnungen für alle Locations aus Performance-Sicht?

Ziel:

Früh feststellen, welche theoretisch sinnvollen Formeln technisch im Map Mode realisierbar sind.

### Economy-Page UI und Budgetmetriken

Vanilla-verifiziert ist, dass die Economy-Seite oben bereits folgende Werte direkt anzeigt:

- `Player.GetEconomicalBase`
- `Player.GetTotalWealth`
- `Player.GetTotalTaxBase`
- `Player.GetModifierValueNoFormat('tax_income_efficiency')`

Für die geplante UI-Erweiterung zu klären:

- Kann `Total Tax Base / Total Wealth` direkt im GUI-Kontext berechnet werden?
- Falls nicht: welcher Script-Value-/Scripted-GUI-Weg ist am stabilsten?
- Welche API liefert `Total Monthly Expenses`?
- Welche API liefert `Total Monthly Income`?
- Lassen sich die aktuellen Monatskosten von Stability-, Diplomacy- und Court-/Government-Power-Slider direkt aus `EconomyView` auslesen?
- Lassen sich daraus live `% of total expenses` und `% of monthly income` berechnen?
- Kann während Slider-Dragging eine marginale Kostenanzeige aktualisiert werden?
- Wie lässt sich die Vanilla-Economy-GUI minimal erweitern, ohne einen unnötig großen Override zu erzeugen?

Ziel:

`Taxable Wealth Share` sowie echte Budget-Anteile der Slider auf der bestehenden Economy-Seite darstellen.

Siehe auch: `04_economy_page_ui_erweiterungen.md`.

---

## Priorität B – Hold vs. Vassal exakt modellieren

### Bedeutung von `subject_pays_vassal` / `scaled_gold = 0.2`

Bisher ist verifiziert, dass normale Vassals `subject_pays_vassal` verwenden und dieser Preis `scaled_gold = 0.2` enthält.

Nicht geklärt ist die exakte Bemessungsgrundlage von `scaled_gold`.

Zu klären:

- 20 % wovon?
- Welche Modifikatoren greifen?
- Erfolgt die Zahlung monatlich?
- Gibt es Minima/Maxima oder Sonderfälle?
- Wird die tatsächliche Subject-Economy, Economic Base oder eine andere Scaling-Funktion verwendet?

Ohne diese Information darf kein scheinbar exakter Vassal-Ertrag berechnet werden.

### Subject Upkeep und Diplomatic Capacity

Zu untersuchen:

- genaue Formel hinter `SUBJECT_UPKEEP_BASE`, `SUBJECT_UPKEEP_ECONOMY_RATIO_SCALE` und `SUBJECT_UPKEEP_ECONOMY_MIN`,
- tatsächliche Auswirkungen von `diplomatic_capacity_cost_scale = 1.0`,
- indirekte Kosten bei Überschreiten der Diplomatic Capacity,
- ob diese Kosten sinnvoll auf einzelne Subjects bzw. Locations verteilt werden können.

### Economic Base des Overlords nach Ausgliederung

Zu klären:

- welcher Economic-Base-Anteil beim Overlord durch abgegebenes Land entfällt,
- wie `ECONOMICAL_BASE_FROM_SUBJECT = 0.05` genau wirkt,
- ob sich damit ein Teil des verlorenen Economic-Base-Beitrags indirekt wieder beim Overlord niederschlägt,
- welche Institution-/Trade-/Interest-Komponenten sich beim Wechsel ändern.

Ziel:

Ein echter Vorher-/Nachher-Vergleich statt einer statischen Pauschale.

---

## Priorität C – Population als Nutzenfaktor

Population soll nicht nur über ihre Economic-Base-Kosten einfließen.

Zu recherchieren:

- Zusammenhang Population → Wealth/Produktion,
- Zusammenhang Population → RGO-Beschäftigung,
- Zusammenhang Population → Building Workforce,
- Zusammenhang Population → Manpower/Sailors bzw. militärische Ressourcen,
- Wachstumsmechaniken und langfristige Skalierung,
- Unterschiede nach Pop Type / Estate / Religion / Kultur, sofern für die Bewertung relevant.

Ziel:

Eine Population-Komponente entwickeln, die reale zukünftige und strategische Vorteile abbildet, ohne Effekte doppelt zu zählen.

---

## Priorität D – RGO-Bewertung

Zu untersuchen:

- verfügbare Script-Zugriffe auf RGO-Typ und Output,
- aktuelle Produktion und Profitabilität,
- Güterpreis und Marktpreis,
- Marktknappheit / Nachfrage / Importabhängigkeit,
- strategische Bedeutung einzelner Güter,
- Ausbaupotential der RGO-Produktion.

Mögliche spätere Trennung:

- `RGO Economic Value`
- `RGO Strategic Value`

Damit kann ein Rohstoff wirtschaftlich mittelmäßig, strategisch aber sehr wichtig sein.

---

## Priorität E – strategischer Location Value

Spätere optionale Faktoren:

- Küste / Hafen,
- Meerzugang,
- Fluss- oder Handelslage,
- Fort-/Chokepoint-Wert,
- Hauptstadt-/Nähe-zur-Hauptstadt-Effekte,
- Kultur und Religion,
- Kernland-/Homeland-Status,
- bestehende Gebäude,
- Urbanisierung,
- Marktzentrum / Handelsposition,
- besondere Ressourcen oder Monumente,
- geographische Verbindung zu anderen Landesteilen.

Diese Faktoren sollten zunächst separat sichtbar sein und erst später in einen Composite Score eingehen.

---

## Geplante Implementierungsreihenfolge

1. Vanilla-Mechaniken und verfügbare Script-Scopes für Map Modes verifizieren.
2. Economy-GUI-Zugriffe für Wealth, Tax Base, Income, Expenses und Sliderkosten verifizieren.
3. `Taxable Wealth Share` als kleinen Economy-UI-MVP implementieren.
4. Einfachen Location-Debug-Map-Mode erstellen, der Rohwerte wie Control, Wealth und Population ausgibt.
5. `Fiscal Efficiency` als erste berechnete Kennzahl implementieren.
6. Economic-Base-Beitrag pro Location so exakt wie technisch möglich ergänzen.
7. Budget-Anteile der Economy-Slider ergänzen.
8. Population Value kalibrieren.
9. Ersten `Retention Value` ohne Vasallenmodell erstellen.
10. Subject-/Vassal-Mechanik vollständig verifizieren.
11. `Retention Value` gegen `Subject Value` erweitern.
12. RGO Economic Value ergänzen.
13. RGO Strategic Value und weitere strategische Faktoren ergänzen.
14. Regionale/zusammenhängende Subject-Candidate-Analyse prüfen.

## Qualitätsregel

Jeder neue Bewertungsfaktor soll vor Aufnahme in den Composite Score dokumentieren:

- Quelle der Mechanik,
- exakte Formel oder angenommene Heuristik,
- Scope und technische Verfügbarkeit,
- erwartete Einheit/Skalierung,
- Risiko von Doppelzählung,
- Kalibrierungsbedarf.

So bleibt der Location Analyzer auch bei wachsender Komplexität nachvollziehbar und moddingtechnisch wartbar.
