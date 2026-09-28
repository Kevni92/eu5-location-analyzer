# 01 – Problem und gesicherter Ist-Stand

Stand: 2026-09-28

## Ausgangsproblem

In EU5 ist der nominelle Reichtum einer Location nicht automatisch identisch mit ihrem tatsächlichen Wert für den Staat. Besonders wichtig ist die Kombination aus **Wealth**, **Control**, **Population** und **Economic Base**.

Eine reiche Location mit niedriger Control kann relativ wenig direkt abschöpfbaren Nutzen liefern, während Teile ihrer Economic Base unabhängig von Control weiter in landesweite Kostenmechaniken eingehen. Daraus entsteht die Frage, ob eine solche Location besser direkt gehalten oder als Subject/Vasall ausgegliedert werden sollte.

Die Mod soll diese Entscheidung sichtbar und vergleichbar machen.

---

## Gesicherte Vanilla-Fakten

### Economic Base ignoriert Control direkt

Die aktuelle Vanilla-Beschreibung von `economic_base` besagt, dass sie auf der gesamten **Wealth** und **Population** eines Landes basiert, **unabhängig von Control**.

Zusätzlich steigt Economic Base durch Subjects und Institutionen sowie durch bestimmte weitere Einkommens-/Besitzquellen.

Damit gilt qualitativ:

- niedrige Control reduziert nicht automatisch die Economic Base einer Location,
- eine reiche oder bevölkerungsreiche Location kann deshalb weiterhin erhebliche Economic Base erzeugen,
- während ihr direkt abschöpfbarer fiskalischer Wert gleichzeitig durch geringe Control eingeschränkt sein kann.

### Relevante Vanilla-Defines für Economic Base

Aktuell verifiziert:

- `ECONOMICAL_BASE_FROM_TAX_BASE = 0.5`
- `ECONOMICAL_BASE_FROM_POP = 0.015`
- `ECONOMICAL_BASE_FROM_TRADE_VALUE = 0.2`
- `ECONOMICAL_BASE_FROM_TRADE_PROFIT = 0.2`
- `ECONOMICAL_BASE_INTEREST = 0.25`
- `ECONOMICAL_BASE_FROM_FOREIGN_BUILDINGS = 1.0`
- `ECONOMICAL_BASE_FROM_SUBJECT = 0.05`
- `ECONOMICAL_BASE_SCALE_FROM_EACH_INSTITUTION = 0.066`

Wichtig: Der interne Name `FROM_TAX_BASE` ist nicht automatisch gleichbedeutend mit einer vollständig controlreduzierten Steuerbasis. Die Localization beschreibt Economic Base ausdrücklich als auf totaler Wealth und Population basierend. Die genaue engine-interne Zuordnung dieses Defines muss bei Bedarf noch weiter verifiziert werden.

### Tax Base und Control

Vanilla beschreibt die Tax Base als den Teil der Wealth, der durch Steuern erfasst werden kann. Control ist dabei ein zentraler Faktor.

Für die Analyse ist deshalb die qualitative Beziehung sicher:

> Je niedriger Control, desto kleiner der tatsächlich steuerlich nutzbare Anteil der vorhandenen Wealth.

Für eine wirklich exakte Modformel müssen jedoch noch alle Faktoren der effektiven Steuerabschöpfung untersucht werden, insbesondere Estate-/Pop-bezogene Steuersätze, Tax Efficiency, Privilegien und weitere Modifikatoren.

---

## Economic-Base-abhängige Slider

Drei besonders relevante laufende Ausgaben sind:

- Stability Spending,
- Diplomatic Spending,
- Court/Government-Power-Spending, das je nach Regierungsform u. a. für Legitimitäts-/Regierungsressourcen relevant ist.

Vanilla enthält u. a.:

- `diplomatic_spending_cost = 0.1`
- `STABILIY_EXPENSE_FACTOR = 0.1`

Für Court- und Stability-Spending existieren Community-Rekonstruktionen, die die Kosten im Kern als proportional zu

`Slider × 0.1 × country_economical_base`

modellieren, anschließend angepasst durch die entsprechende Efficiency.

Diese Rekonstruktion ist sehr plausibel und passt zu den vorhandenen Vanilla-Modifikatoren, ist aber für Court/Stability bislang nicht als vollständig offenliegende Vanilla-Engine-Formel verifiziert. Deshalb wird sie im Projekt als **rekonstruiert**, nicht als endgültig vanilla-verifiziert geführt.

---

## Relevantes Spielprofil für die Bewertung

Für die bisherige Analyse wurde folgendes typisches Spielverhalten angenommen:

- Stability Spending: fast immer `0 %`,
- Diplomatic Spending: nur situativ aktiv,
- Court/Legitimacy-orientiertes Spending: langfristig im Mittel ungefähr `20–30 %`.

Unter dieser Spielweise ist der Economic-Base-Nachteil von Low-Control-Land deutlich kleiner als in einer Modellrechnung, in der alle drei Slider dauerhaft hoch stehen.

Beispielhafte Rekonstruktion bei neutraler Efficiency:

- Court im Mittel 25 % → ca. `2.5 % × Economic Base`
- Diplomatie im langfristigen Mittel 5–10 % → ca. `0.5–1.0 % × Economic Base`
- Stabilität 0 % → `0`

Damit läge die typische Belastung aus diesen drei Sinks eher bei ungefähr `3–3.5 % × Economic Base` als bei einem theoretischen Maximalwert von rund 30 %.

Das hat eine wichtige Konsequenz:

> Niedrige Control allein ist unter diesem Spielstil kein ausreichender Grund, eine Location abzugeben.

---

## Bisheriges Break-even-Modell

Für eine erste Näherung definieren wir:

- `c` = Control als Anteil zwischen 0 und 1,
- `T100` = direkter monatlicher fiskalischer Ertrag der Location bei 100 % Control,
- `K` = zusätzliche monatliche Kosten des direkten Besitzes,
- `V` = monatlicher Netto-Nutzen derselben Region als Vasall/Subject,
- `H` = sonstige Vorteile des direkten Besitzes, monetarisiert oder separat bewertet.

Direkter Besitz ist besser, wenn:

`c × T100 + H - K > V`

Der reine fiskalische Break-even liegt damit bei:

`c* = (V + K - H) / T100`

Diese Formel ist absichtlich abstrakt. Sie ist mathematisch sauber, aber ihre Eingangsgrößen müssen noch genauer aus Vanilla-Werten abgeleitet werden.

---

## Beispiel aus der bisherigen Diskussion

Angenommen:

- Wealth = 100,
- effektive Steuerabschöpfung bei 100 % Control = 40 %, also `T100 = 40`,
- Wealth-bedingte Economic Base ≈ 50,
- durchschnittliche Economic-Base-Sliderbelastung = 3.5 %.

Dann entstehen aus dem Wealth-Anteil ungefähr:

`50 × 0.035 = 1.75` Gold/Monat indirekte Kosten.

Der direkte fiskalische Wert wäre in dieser vereinfachten Rechnung:

`40 × c - 1.75`

Ohne Subject-Gegenwert wäre die Location bereits ab ungefähr 4.4 % Control positiv.

Wenn ein Vasall beispielsweise 8 Gold/Monat Netto-Nutzen erzeugen würde, ergäbe sich:

`40 × c - 1.75 = 8`

und damit ein Break-even von ungefähr 24.4 % Control.

Diese Zahlen sind **nur Demonstrationswerte**, keine Vanilla-Konstanten. Sie zeigen, wie stark der Break-even von tatsächlichem Tax Yield, Slider-Nutzung und Subject-Wert abhängt.

---

## Subject-/Vassal-Seite: bisher gesichert

Für den normalen Vanilla-Vassal wurde verifiziert:

- Subject-Typ verwendet `subject_pays_vassal`,
- der zugehörige Preis enthält `scaled_gold = 0.2`,
- `diplomatic_capacity_cost_scale = 1.0`.

Außerdem existieren Vanilla-Defines für Subject Upkeep:

- `SUBJECT_UPKEEP_BASE = 0.1`
- `SUBJECT_UPKEEP_ECONOMY_RATIO_SCALE = 2.0`
- `SUBJECT_UPKEEP_ECONOMY_MIN = 0.1`

Noch **nicht abschließend verifiziert** ist, was `scaled_gold = 0.2` mathematisch exakt als Bemessungsgrundlage verwendet. Es darf deshalb derzeit nicht einfach als „20 % des Einkommens“ oder „20 % der Wealth“ interpretiert werden.

Genau dieser Punkt ist für einen echten Hold-vs-Vassal-Map-Mode zentral und steht im Research-Backlog.

---

## Zentrale Schlussfolgerung bisher

Die wichtigste Erkenntnis lautet nicht „Low Control = schlecht“, sondern:

> Eine Location ist dann problematisch, wenn ihr tatsächlicher direkter Nutzen im Verhältnis zu den durch Wealth, Population und weitere Faktoren verursachten landesweiten Opportunitätskosten niedrig ist.

Control ist deshalb ein wichtiger Effizienzfaktor, aber nicht der alleinige Wertmaßstab.

Eine spätere Bewertungsformel sollte mindestens Wealth, Control, Population und den alternativen Subject-Wert getrennt modellieren, bevor daraus ein Gesamturteil gebildet wird.
