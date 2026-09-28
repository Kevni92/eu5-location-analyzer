# 02 – Bewertungsmodell und Map-Mode-Ideen

Stand: 2026-09-28

## Zielbild

Die Mod soll nicht nur Rohdaten anzeigen, sondern aus ihnen eine für Entscheidungen brauchbare Bewertung erzeugen.

Die zentrale Frage lautet:

> Wie wertvoll ist diese Location für den aktuellen Besitzer – und wie sinnvoll wäre es, sie direkt zu behalten, einem Subject zu geben oder vollständig aufzugeben?

Dafür ist ein modularer Ansatz sinnvoll. Einzelne Teilwerte sollten separat berechnet und sichtbar gemacht werden, bevor sie in einen Gesamt-Score einfließen.

---

## 1. Fiskalischer Direktwert

Dieser Wert soll approximieren, wie viel die Location dem Staat tatsächlich bringt.

Konzeptionell:

`Direct Fiscal Value = effective tax yield + other direct income - ownership-linked marginal costs`

Wichtig ist, nicht einfach Wealth zu verwenden. Eine Location mit hoher Wealth, aber sehr niedriger Control kann fiskalisch schwach sein.

Langfristig sollten hier mindestens einfließen:

- Wealth,
- Control,
- tatsächliche Tax Efficiency,
- Estate-/Pop-spezifische Steuermechaniken,
- Gebäudeerträge, soweit sie direkt dem Staat zugutekommen,
- ggf. Handels- oder Marktkomponenten, sofern sie wirklich locationbezogen sinnvoll zurechenbar sind.

---

## 2. Economic-Base-Burden

Eine zweite Kennzahl soll messen, wie viel Economic Base eine Location verursacht, verglichen mit ihrem tatsächlich nutzbaren Ertrag.

Eine einfache diagnostische Kennzahl wäre:

`Fiscal Efficiency = Direct Fiscal Value / Marginal Economic Base`

oder umgekehrt:

`Economic Base Burden = Marginal Economic Base / Direct Fiscal Value`

Eine hohe Belastungsquote würde Locations markieren, die viel Economic Base erzeugen, aber wenig direkt abschöpfbaren Nutzen liefern.

Das ist besonders interessant für Low-Control-Gebiete.

Dieser Wert ist aber nur dann wirklich relevant, wenn der Spieler Economic-Base-abhängige Ausgaben tatsächlich nutzt. Deshalb sollte eine spätere Version möglichst die aktuellen Sliderwerte bzw. den realen aktuellen marginalen Goldpreis der Economic Base verwenden statt einen pauschalen Fixwert.

---

## 3. Population Value

Population soll ausdrücklich **nicht nur als Kostenfaktor über Economic Base** betrachtet werden.

Eine hohe Population ist grundsätzlich strategisch wertvoll, selbst wenn die aktuelle fiskalische Abschöpfung schwach ist.

Mögliche Wertkomponenten:

- potenzielle Steuerbasis,
- Arbeitskräfte für RGO und Gebäude,
- Manpower-/Militärpotential,
- langfristiges Wirtschaftswachstum,
- Urbanisierungs-/Produktionspotential,
- strategischer Wert großer Bevölkerungszentren.

Deshalb sollte Population als eigener positiver Wert in die Bewertung eingehen.

Ein erster konzeptioneller Ansatz:

`Population Value = normalized population × population weight`

Der Population Weight darf nicht willkürlich dauerhaft festgeschrieben werden. Er sollte später gegen reale Vanilla-Effekte kalibriert werden.

Wichtig ist vor allem die Richtung:

> Zwei ansonsten identische Locations dürfen nicht denselben Gesamtwert erhalten, wenn eine davon ein Vielfaches der Population besitzt.

---

## 4. RGO Value

RGO soll mittelfristig ein zentraler Bestandteil des Location Value werden.

Dabei sollte nicht nur der aktuelle monetäre Output betrachtet werden. Manche Güter haben einen erheblichen strategischen Wert, der sich nicht vollständig im lokalen Einkommen widerspiegelt.

Mögliche Komponenten:

- aktuelle Produktionsmenge,
- lokaler/marktweiter Preis,
- Profitabilität,
- Knappheit des Gutes im eigenen Markt,
- militärische oder industrielle Relevanz,
- Möglichkeit, die Produktion später auszubauen,
- Abhängigkeit von Importen,
- Marktanteil bzw. strategische Versorgungssicherheit.

Langfristig könnte daraus entstehen:

`RGO Value = economic output + scarcity premium + strategic goods premium`

Der strategische Aufschlag wäre eine bewusst von der Mod definierte Heuristik und muss klar von Vanilla-Werten getrennt dokumentiert werden.

---

## 5. Retention Value / „Behalten oder abgeben?“

Der eigentliche Hauptscore sollte nicht einfach „Location Value“ heißen, sondern möglichst die konkrete Entscheidung abbilden.

Konzeptionell:

`Retention Value = Direct Ownership Value - Alternative Subject Value`

Dabei könnte gelten:

- stark positiv → direkt behalten,
- nahe null → ökonomisch weitgehend indifferent,
- negativ → Ausgliederung/Vasallisierung kann sinnvoll sein.

`Direct Ownership Value` könnte später zusammengesetzt sein aus:

`Fiscal Value + Population Value + RGO Value + Strategic Value - Marginal Costs`

`Alternative Subject Value` könnte umfassen:

`Subject Payments + Subject Strategic Utility - Diplomatic/Subject Costs + retained indirect benefits`

Die Formel soll zunächst modular bleiben, damit einzelne Teilwerte ein- und ausgeschaltet oder unterschiedlich gewichtet werden können.

---

## Vorgeschlagene Map Modes

### A. Retention Value

Der wichtigste Map Mode.

Er zeigt direkt, wie stark eine Location aus Sicht des aktuellen Spielers zum direkten Besitz tendiert.

Mögliche Farblogik:

- dunkelgrün: sehr klar behalten,
- hellgrün: eher behalten,
- gelb: ungefähr neutral,
- orange: eher abgebbar,
- rot: guter Kandidat für Subject/Vasallisierung.

Der Tooltip sollte die Komponenten des Scores offenlegen, damit der Wert nachvollziehbar bleibt.

Beispielhafte Tooltip-Struktur:

- Direct Fiscal Value
- Population Value
- RGO Value
- Economic Base Cost
- Other Strategic Value
- Estimated Subject Value
- Net Retention Value

### B. Fiscal Efficiency

Dieser Map Mode beantwortet:

> Welche Locations liefern im Verhältnis zu ihrer Economic Base tatsächlich wenig staatlichen Ertrag?

Er ist besonders für die Identifikation ineffizienter Low-Control-Locations nützlich.

### C. Population Importance

Ein separater Map Mode für Population verhindert, dass dicht bevölkerte, derzeit aber schlecht kontrollierte Gebiete im Gesamtmodell „unsichtbar“ werden.

Er kann später auch als Debug-/Kalibrierungsansicht dienen.

### D. RGO / Strategic Resource Value

Ein Map Mode, der den Rohstoffwert aus Sicht des eigenen Marktes bewertet.

Später besonders sinnvoll für Güterknappheit und strategische Versorgung.

### E. Subject Candidate Score

Optional zusätzlich zum Retention Value.

Dieser könnte stärker auf die konkrete Frage optimiert sein:

> Welche zusammenhängenden Regionen eignen sich am besten zur Ausgliederung in ein Subject?

Dafür reicht eine reine Einzel-Location-Bewertung langfristig nicht aus. Zusammenhängende Gebiete, mögliche Hauptstädte, Kultur, Zugang zum Meer und wirtschaftliche Tragfähigkeit eines neuen Subjects müssten berücksichtigt werden.

---

## Warum mehrere Map Modes statt nur eines Scores?

Ein einzelner Gesamtwert ist bequem, kann aber wichtige Gründe verdecken.

Beispiel:

- Location A ist fiskalisch schwach, aber extrem bevölkerungsreich.
- Location B ist fiskalisch schwach und zugleich fast unbewohnt.

Ein reiner Steuer-/Control-Score könnte beide ähnlich bewerten, obwohl ihre strategische Bedeutung offensichtlich unterschiedlich ist.

Deshalb sollte die Mod zwei Ebenen anbieten:

1. **Komponenten-Map-Modes** zum Verstehen der Situation.
2. **Composite Map Mode** für die eigentliche Entscheidung.

---

## Vorgeschlagene erste MVP-Stufe

Die erste wirklich umsetzbare Version sollte bewusst klein bleiben.

MVP-Komponenten:

- Control,
- Wealth,
- Population,
- approximierter marginaler Economic-Base-Beitrag,
- approximierter fiskalischer Direktwert,
- daraus abgeleitete Fiscal Efficiency,
- einfacher Retention Score ohne RGO-Strategie und ohne vollständig modellierten Vasallenwert.

Danach können RGO, Subject-Vergleich und strategische Faktoren ergänzt werden.

Das reduziert das Risiko, früh einen scheinbar präzisen Gesamtscore zu bauen, dessen Einzelkomponenten noch nicht belastbar sind.

---

## Designprinzipien für die spätere Formel

Die Bewertungsformel sollte:

- nachvollziehbar sein,
- im Tooltip zerlegbar sein,
- reale Vanilla-Werte bevorzugen,
- keine mehrfachen Doppelzählungen erzeugen,
- aktuelle Spielerparameter berücksichtigen, wo möglich,
- positive und negative Populationseffekte getrennt behandeln,
- subjektive strategische Gewichtungen klar als Mod-Heuristik kennzeichnen,
- später über Script Values zentral justierbar sein.

Besonders wichtig ist die Vermeidung von Doppelzählung. Wenn Population bereits über Wealth, RGO-Output oder Manpower indirekt Wert erzeugt, darf derselbe Effekt nicht zusätzlich vollständig als separater Population Value ein zweites Mal eingerechnet werden.
