# EU5 Location Analyzer

Debug-/Prototyping-Mod für Europa Universalis V.

## Aktueller Stand: Economy Debug UI (0.1.0-debug)

Die erste lauffähige Version verändert ausschließlich die Economy-Seite und soll Daten für die spätere finale UI liefern.

Sie zeigt bzw. ergänzt:

- `Tax Base` zusammen mit `Tax Base / Wealth` in Prozent,
- bei generischen Maintenance-/Spending-Slidern die exakte Sliderstellung in Prozent,
- beim Stability-Investment die exakte Sliderstellung,
- die bereits von Vanilla angezeigten absoluten monatlichen Kosten bleiben sichtbar.

Damit kann ein Screenshot gleichzeitig Wealth, Tax Base, Economic Base, Tax Efficiency, Sliderstellung und Sliderkosten zeigen.

## Warum wird die GUI generiert?

`in_game/gui/economy_lateralview.gui` ist ein Whole-file-Override. Eine fest eingecheckte Kopie würde bei jedem EU5-Patch schnell veralten. Der Builder nimmt deshalb **deine aktuell installierte Vanilla-Datei** und wendet nur drei kleine, validierte Debug-Patches an.

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

## Test/Screenshot

1. Mod aktivieren und Economy-Seite öffnen.
2. Einen Screenshot des oberen Bereichs mit Economic Base / Wealth / Tax Base / Tax Efficiency machen.
3. Einen Screenshot machen, auf dem die relevanten Ausgaben-Slider samt Kosten und Prozentwerten sichtbar sind.
4. Besonders interessant sind Stability, Diplomacy und Court/Government-/Legitimacy-bezogene Spending-Slider.
5. Falls die Economy-Seite nicht öffnet oder ein Debugwert leer/falsch ist, zusätzlich `error.log` nach `economy_lateralview`, `MaintenanceSetting`, `Divide_CFixedPoint` oder `GetSliderValue` durchsuchen.

## Kompatibilität

Die Debug-Version überschreibt `in_game/gui/economy_lateralview.gui` vollständig und kollidiert daher mit anderen Mods, die dieselbe Datei überschreiben. Für den Test sollte der Location Analyzer nach solchen UI-Mods geladen werden oder diese sollten vorübergehend deaktiviert sein.

Die Mod ändert keine Spielmechanik und ist in `.metadata/metadata.json` als nicht multiplayer-synchronisiert markiert.

## Dokumentation

Die fachliche Analyse und Roadmap liegen unter [`docs/`](docs/README.md).
