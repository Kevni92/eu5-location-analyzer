# EU5 Location Analyzer – Dokumentation

Stand: 2026-09-28

Dieses Verzeichnis sammelt die fachliche Grundlage für eine Europa-Universalis-V-Mod, die einzelne Locations bewertet und die Ergebnisse über eigene Map Modes sichtbar macht. Ergänzend soll die Economy-Seite um Kennzahlen erweitert werden, die Wealth, Tax Base und laufende Budgetbelastungen besser einordnen.

## Ziel

Die Mod soll nicht nur anzeigen, ob eine Location „reich“ ist, sondern eine für den Spieler relevante Frage beantworten:

> Wie wertvoll ist diese Location für mein Land – und wie schmerzhaft wäre es, sie abzugeben, auszugliedern oder einem Vasallen zu überlassen?

Dafür soll die Bewertung schrittweise mehrere Dimensionen berücksichtigen:

- fiskalischer Nutzen des direkten Besitzes,
- Control und daraus resultierende tatsächliche Abschöpfbarkeit,
- Economic Base und deren indirekte Kosten,
- Population als eigener Wertfaktor,
- RGO und strategische Rohstoffe,
- später ggf. Gebäude, Markt-/Handelswert, Manpower, Seestreitkräfte, Kultur/Religion, Geographie und militärische Lage,
- Vergleich „direkt halten“ gegen „als Subject/Vasall halten“.

Zusätzlich soll die Economy-Seite bessere Planungsinformationen liefern, insbesondere:

- Verhältnis von Tax Base zu Wealth (`Taxable Wealth Share`),
- Anteil einzelner Economy-Slider an den gesamten Monatsausgaben,
- Anteil jeder sichtbaren Einnahmequelle an den gesamten Monatseinnahmen,
- Anteil fester Ausgabenposten an den gesamten Monatsausgaben,
- optional Anteil der Sliderkosten am Monatseinkommen,
- später marginale Kosten einer Slidererhöhung und aggregierter Economic-Base-Spending-Druck.

## Dokumente

- [01 – Problem und gesicherter Ist-Stand](01_problem_und_gesicherter_iststand.md)
- [02 – Bewertungsmodell und Map-Mode-Ideen](02_bewertungsmodell_und_map_modes.md)
- [03 – Offene Fragen und Research-Backlog](03_offene_fragen_und_research_backlog.md)
- [04 – Economy-Page UI-Erweiterungen](04_economy_page_ui_erweiterungen.md)
- [05 – Economy Debug GUI MVP](05_economy_debug_gui_mvp.md)
- [06 – Economy Analysis UI Runtime-Validierung 0.2.1](06_runtime_validation_0_2_1.md)
- [07 – Income-/Expense-Share UI](07_income_expense_share_ui.md)

## Grundprinzip

Die spätere Implementierung soll zwischen drei Kategorien unterscheiden:

1. **Vanilla-verifiziert** – direkt aus aktuellen EU5-Gamefiles/Defines/Localization belegt.
2. **Rekonstruiert** – durch Script-Werte, UI-Verhalten oder Community-Mods nachvollzogen, aber nicht vollständig in Vanilla-Script offenliegend.
3. **Designannahme** – bewusst von uns definierter Bewertungsfaktor, etwa ein zusätzlicher strategischer Population- oder RGO-Wert.

So bleibt jederzeit erkennbar, welche Teile die reale Spielmechanik abbilden und welche Teile eine bewusst gewählte Analyse-Heuristik sind.
