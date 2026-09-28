# EU5 Location Analyzer

Analyse-/Prototyping-Mod für Europa Universalis V.

## Aktueller Stand: Economy Analysis UI (0.2.0-alpha)

Die erste aus der Debugphase abgeleitete Version erweitert die Economy-Seite um direkt nutzbare Planungswerte.

Sie ergänzt:

- `Tax Base` um den Anteil der Tax Base am gesamten Wealth,
- bei generischen Maintenance-/Spending-Slidern die exakte Sliderstellung und den Anteil an den gesamten Monatsausgaben,
- beim Stability-Investment ebenfalls Sliderstellung und Ausgabenanteil,
- die von Vanilla bereits angezeigten absoluten monatlichen Kosten bleiben sichtbar.

Anzeige bei Slidern:

```text
25% | 4.2%B
```

bedeutet:

```text
Sliderstellung:                       25.0 %
Anteil an gesamten Monatsausgaben:     4.2 %
```

`B` steht in dieser Alpha-Version für Budgetanteil = Anteil an `EconomyView.GetAllExpense`.

Oben soll Tax Base beispielsweise so erscheinen:

```text
287.80 (80.1%)
```

Der Prozentwert ist:

```text
Tax Base / Wealth
```

und damit bewusst etwas anderes als die daneben stehende `Tax Efficiency`.

## Laufzeitvalidierung vom 28.09.2026

Der erste Ingame-Test hat bestätigt, dass die generischen Sliderwerte und deren Budgetanteile funktionieren. Sichtbar waren unter anderem Court, Army, Navy, Fort, Diplomatic Spending und Food. Stability funktioniert als separater EconomyView-Block.

Der erste Tax-Base-Prototyp zeigte dagegen das Wort `default`. Ursache war die Verwendung von `raw_text` in einem Vanilla-Block, dessen Basistemplate bereits eine `text`-Property definiert. Version 0.2.0-alpha überschreibt nun gezielt `text` und verwendet für die Division das in EU5-GUIs etablierte `Select_CFixedPoint(... Divide_CFixedPoint(...))`-Muster mit Nullschutz.

Die Budgetquote wird nun mit einer Nachkommastelle ausgegeben. Das vermeidet die in der ersten Debugversion sichtbare Abschneidung, z. B. bei Fortkosten knapp unter 14 %.

## Warum wird die GUI generiert?

`in_game/gui/economy_lateralview.gui` ist ein Whole-file-Override. Eine fest eingecheckte Kopie würde bei jedem EU5-Patch schnell veralten. Der Builder nimmt deshalb **deine aktuell installierte Vanilla-Datei** und wendet nur kleine, validierte Analyse-Patches an.

Nach dem Build liegt die fertige Workshop-Datei unter:

```text
in_game/gui/economy_lateralview.gui
```

Die `.metadata/metadata.json` liegt bereits im Repository. Danach ist der Repository-Root als EU5-Mod-Payload bzw. Workshop-Inhalt verwendbar.

## Build

Am einfachsten unter Windows:

```bat
tools\build_debug_gui.bat
```

Oder direkt mit Python:

```bash
python tools/build_debug_gui.py
```

Wenn EU5 in einer benutzerdefinierten Steam-Library liegt:

```bash
python tools/build_debug_gui.py --game-dir "D:\\SteamLibrary\\steamapps\\common\\Europa Universalis V"
```

Alternativ kann die Vanilla-Datei direkt angegeben werden:

```bash
python tools/build_debug_gui.py --source "...\\game\\in_game\\gui\\economy_lateralview.gui"
```

Der Builder bricht absichtlich ab, wenn die erwarteten Vanilla-Anker nicht exakt gefunden werden. Damit wird nach einem Patch keine veraltete GUI stillschweigend erzeugt.

## Nächster Test

Nach einem `git pull` den Builder erneut ausführen und Economy öffnen. Prüfen:

1. `Tax Base` zeigt jetzt einen Zahlenwert plus Prozent in Klammern statt `default`.
2. Court/Diplomacy/Army/Navy/Fort usw. zeigen `Slider% | Budget%B` mit einer Nachkommastelle.
3. Stability zeigt dasselbe Format; ein Test mit Stability > 0 % ist besonders nützlich.

Falls etwas leer oder falsch ist, bitte Screenshot und passende `error.log`-Zeilen senden.

## Kompatibilität

Die Alpha-Version überschreibt `in_game/gui/economy_lateralview.gui` vollständig und kollidiert daher mit anderen Mods, die dieselbe Datei überschreiben. Für Tests sollte der Location Analyzer nach solchen UI-Mods geladen werden oder diese sollten vorübergehend deaktiviert sein.

Die Mod ändert keine Spielmechanik und ist in `.metadata/metadata.json` als nicht multiplayer-synchronisiert markiert.

## Dokumentation

Die fachliche Analyse und Roadmap liegen unter [`docs/`](docs/README.md).
