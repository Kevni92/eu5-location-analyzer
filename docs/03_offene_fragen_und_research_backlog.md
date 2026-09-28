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
2. Einfachen Location-Debug-Map-Mode erstellen, der Rohwerte wie Control, Wealth und Population ausgibt.
3. `Fiscal Efficiency` als erste berechnete Kennzahl implementieren.
4. Economic-Base-Beitrag pro Location so exakt wie technisch möglich ergänzen.
5. Population Value kalibrieren.
6. Ersten `Retention Value` ohne Vasallenmodell erstellen.
7. Subject-/Vassal-Mechanik vollständig verifizieren.
8. `Retention Value` gegen `Subject Value` erweitern.
9. RGO Economic Value ergänzen.
10. RGO Strategic Value und weitere strategische Faktoren ergänzen.
11. Regionale/zusammenhängende Subject-Candidate-Analyse prüfen.

## Qualitätsregel

Jeder neue Bewertungsfaktor soll vor Aufnahme in den Composite Score dokumentieren:

- Quelle der Mechanik,
- exakte Formel oder angenommene Heuristik,
- Scope und technische Verfügbarkeit,
- erwartete Einheit/Skalierung,
- Risiko von Doppelzählung,
- Kalibrierungsbedarf.

So bleibt der Location Analyzer auch bei wachsender Komplexität nachvollziehbar und moddingtechnisch wartbar.
