# AGENTS.md — EU5 Location Analyzer

Diese Datei gilt repo-weit. Sie ist die primäre Arbeitsanweisung für Codex und andere Coding-Agenten, die dieses Repository lokal weiterentwickeln.

## 1. Projektziel

`eu5-location-analyzer` ist eine EU5-Mod und zugleich ein Forschungs-/Analyseprojekt. Langfristiges Ziel ist eine belastbare Bewertung einzelner Locations und deren Darstellung über eigene Map Modes. Die zentrale Spielerfrage lautet:

> Wie wertvoll ist diese Location für den aktuellen Besitzer, und wie schmerzhaft wäre es, sie abzugeben, auszugliedern oder einem Subject/Vasallen zu überlassen?

Die Bewertung soll schrittweise mindestens berücksichtigen:

- fiskalischen Nutzen des direkten Besitzes,
- Control und tatsächliche Abschöpfbarkeit,
- Economic Base und deren marginale laufende Kosten,
- Population als positiven eigenen Wertfaktor,
- RGO-Wert, später getrennt in wirtschaftlichen und strategischen Wert,
- Gebäude, Markt/Handel, Manpower/Sailors, Kultur/Religion, Geographie und militärische Lage, soweit sinnvoll,
- Vergleich `Direct Ownership Value` gegen `Subject/Vassal Value`.

Daneben erweitert die Mod die Economy-Seite um Planungsinformationen wie Income-/Expense-Anteile, Slider-Budgetanteile, Wealth/Tax-Base-Diagnostik und Breakdown-Charts.

## 2. Wichtigste Regel: Grounding vor Generierung

EU5 basiert auf Clausewitz/Jomini. Kenntnisse aus EU4, CK3, Victoria 3 oder älteren EU5-Patches sind nur konzeptionelle Hinweise und **kein Syntaxbeweis**.

Bei konkreter EU5-Syntax niemals raten. Vor Verwendung eines Triggers, Effects, Scope Links, Modifiers, GUI-Ausdrucks, Widgets, `blockoverride`, Datenbankfelds oder Identifiers mindestens prüfen:

1. **Existenz** — existiert der Name in der aktuellen Zielversion?
2. **Scope/Position** — ist er aus dem aktuellen Scope bzw. an dieser strukturellen Position gültig?
3. **Semantik** — welcher Wert-, Objekt- oder Blocktyp wird tatsächlich erwartet?

Wenn keine belastbare Referenz existiert, Unsicherheit dokumentieren und nicht durch plausible Erfindungen ersetzen.

## 3. Quellenhierarchie

Bei Widersprüchen gilt grundsätzlich diese Reihenfolge:

1. **Aktuelle lokale Engine-Dumps derselben EU5-Version**
   - `script_docs`
   - `dump_data_types`
   - generierte Trigger-/Effect-/Scope-/Modifier-/On-Action-/GUI-Datentyp-Dokumentation
2. **Vanilla-Dateien derselben Spielversion**
3. **Getestete Community-Mods derselben oder sehr nahen Spielversion**
4. **EU5 Paradox Wiki / Modding-Dokumentation**
5. **Steam Guides, Workshop-Beschreibungen, Reddit/Discord**

Eine Community-Mod ist ein Implementierungsbeispiel, keine Engine-Definition. Die zu prüfende eigene Mod ist niemals Beweis für die Gültigkeit ihrer eigenen Syntax.

## 4. Nachschlagewerke und wo gesucht wird

### 4.1 Lokale Spielinstallation — höchste praktische Autorität

Wenn lokal vorhanden, zuerst die tatsächlich installierte Zielversion verwenden. Der Builder erkennt übliche Steam-Libraries automatisch. Typischer Game-Root unter Windows:

```text
<SteamLibrary>\steamapps\common\Europa Universalis V\game\
```

Wichtige Vanilla-Bereiche:

```text
game/in_game/common/
game/in_game/events/
game/in_game/gui/
game/in_game/map_data/
game/in_game/setup/
game/main_menu/common/
game/main_menu/gui/
game/main_menu/localization/
game/main_menu/setup/
game/loading_screen/
game/dlc/
```

Besonders wichtig für Modifier-Audits:

```text
game/main_menu/common/modifier_type_definitions/00_modifier_types.txt
```

Bei DLC-Mechaniken immer auch `game/dlc/` nach Definitionen und Overrides durchsuchen.

### 4.2 Kanonisches Gamefile-Referenzrepository

Projekt-Referenz:

```text
https://github.com/Kevni92/eu5-references
```

Wenn lokal als Sibling-Repo geklont, bevorzugt dort suchen, z. B.:

```text
../eu5-references/game/
```

Die initiale Referenz basiert auf der Vanilla-Spiegelung aus `HLJSXK/eu5-towards-victory`. Eine lokale Installation derselben oder neueren Patchversion gewinnt bei Abweichungen immer.

Empfohlene Suchreihenfolge im Referenzrepo:

1. konkreten Identifier/Dateinamen im gesamten `game/`-Baum suchen,
2. passende Definition unter `game/in_game/common/` finden,
3. reale Verwendung in `events/`, `on_action/`, GUI und Setup suchen,
4. globale Definitionen unter `game/main_menu/common/` prüfen,
5. DLC-Verzeichnisse nach Ergänzungen/Overrides prüfen,
6. erst danach Community-/Webquellen hinzunehmen.

### 4.3 Dieses Repository

Fachliche Projekt-Dokumentation liegt unter:

```text
docs/
```

Startpunkt:

```text
docs/README.md
```

Besonders relevant:

- `docs/01_problem_und_gesicherter_iststand.md` — belegte Mechaniken und Problemdefinition
- `docs/02_bewertungsmodell_und_map_modes.md` — Retention-/Fiscal-/Population-/RGO-Konzept
- `docs/03_offene_fragen_und_research_backlog.md` — noch nicht bewiesene Mechaniken
- `docs/04_economy_page_ui_erweiterungen.md` — Economy-UI-Zielbild
- `docs/05_economy_debug_gui_mvp.md` — Runtime-Erkenntnisse und GUI-Getter
- `docs/06_runtime_validation_0_2_1.md` — verifizierte Slider-/Expense-Pfade
- `docs/06_taxable_wealth_ratio_runtime_fix.md` — wichtige Grenze von GUI-Display-Gettern
- `docs/07_income_expense_share_ui.md` — Income-/Expense-Anteile
- `docs/08_economy_pie_charts.md` — Pie-/Donut-Konzept und bisherige Runtime-Ergebnisse

Fakten in diesen Dokumenten sind nach Möglichkeit mit einer von drei Kategorien zu behandeln:

- **Vanilla-verifiziert**
- **Rekonstruiert**
- **Designannahme**

Diese Kategorien nicht vermischen.

### 4.4 Weitere nützliche externe Referenzen

Nur nach höherwertigen Quellen verwenden:

- `HLJSXK/eu5-modding-project` — Agenten-/Verifikationsworkflow und Anti-Patterns
- `Vendra35/Mongol-Resurgence` — `verify-eu5-syntax`, `verify-tags`, `audit-mod`
- `emmahyde/eu5_economic_tooltips` — Knowledge-Agent und GUI-Recherche
- `jacklenzotti/clausewitz-mcp` — Engine-/Vanilla-Indexierung als Agententool
- `Europa-Universalis-5-Modding-Co-op/modding-digests` — Patchänderungen
- `Europa-Universalis-5-Modding-Co-op/community-mod-toolkit` — Mod-/Release-/Workshop-Struktur
- `Europa-Universalis-5-Modding-Co-op/community-mod-framework` — geteilte Mod-Infrastruktur
- `cwtools/cwtools-vscode` — allgemeine Clausewitz/Jomini-Validierung; EU5-Abdeckung verifizieren
- EU5 Wiki: `https://eu5.paradoxwikis.com/`

## 5. Repo-Struktur und Source of Truth

Wichtige Pfade:

```text
.metadata/metadata.json
in_game/common/script_values/
tools/
docs/
```

### Generierte GUI niemals als Quellcode behandeln

`in_game/gui/economy_lateralview.gui` wird aus der lokal installierten Vanilla-Datei generiert und ist absichtlich in `.gitignore` eingetragen.

**Nicht von Hand dauerhaft editieren.** Änderungen gehören in die Builder-/Injector-Skripte unter `tools/`.

Aktuelle Build-Pipeline:

```text
tools/build_debug_gui.bat
  -> tools/build_debug_gui.py
  -> tools/run_economy_pies.py
       -> tools/add_economy_pies.py
  -> tools/fix_economy_pie_layout.py
```

`build_debug_gui.py` erzeugt zuerst den Whole-file-Override aus der installierten Vanilla-GUI. Die nachfolgenden Schritte injizieren bzw. post-processen die Analyse-Pies.

Der Builder soll **fail closed** arbeiten: Wenn ein erwarteter Vanilla-Anchor fehlt oder unerwartet mehrfach vorkommt, Build abbrechen statt einen möglicherweise kaputten Override zu erzeugen.

## 6. Mod-Struktur und Dateipfade

Neue Ordner oder Datenbankpfade nicht aus Plausibilität erfinden. Zuerst ein aktuelles Vanilla-Beispiel mit demselben Datentyp finden.

Typische Bereiche sind:

- `.metadata/` — Mod-/Launcher-Metadaten
- `in_game/common/` — Definitionen und wiederverwendbares Script
- `in_game/events/`
- `in_game/gui/`
- `in_game/gfx/`
- `in_game/map_data/`
- `in_game/setup/`
- `main_menu/` — u. a. Localization und globale Definitionen
- `loading_screen/` — frühe Defines/globaler Lade-Kontext

Metadatenfelder ebenfalls gegen eine funktionierende aktuelle EU5-Vorlage prüfen. Aktuell ist die Mod als UI-Mod für EU5 `1.3.*` geführt; bei relevanten Releases die Version in `.metadata/metadata.json` sinnvoll erhöhen.

## 7. Jomini-Scripting: Scopes, Trigger, Effects, Script Values

### Trigger und Effects

Für jeden Trigger/Effect prüfen:

- erlaubte Eingangsscopes,
- Parameterform,
- reale Vanilla-Verwendung im gleichen Kontext.

Viele Treffer in Vanilla beweisen nicht, dass der Aufruf aus dem eigenen Scope korrekt ist.

### Scope-Navigation

- `root`, `prev` und gespeicherte Scopes nur verwenden, wenn der reale Scope-Stack verstanden ist.
- Optische Einrückung entspricht nicht automatisch einem Scope-Hop.
- Bei komplexer Navigation gespeicherte Scopes gegenüber implizitem Zurückspringen bevorzugen.
- Scope Links anhand der Engine-Dumps auf Input-/Output-Scope prüfen.

### Script Values und Variablen

- Scopepräfixe sind echte Navigation, keine dekorativen Namensbestandteile.
- Variablen müssen zum Auswertungszeitpunkt existieren.
- Validierungs-/Ladephasen können Script Values früher evaluieren als erwartet.
- temporäre Variablen gezielt aufräumen.
- Operatorfelder und Variablensyntax nicht aus anderen Paradox-Spielen übernehmen.

### Events und On Actions

- Alte EU4-Eventmuster nicht ungeprüft übernehmen.
- Events werden typischerweise explizit über On Actions, andere Events, Entscheidungen oder Scripted Effects ausgelöst.
- On-Action-Hookname, Scope und Frequenz verifizieren.
- Performancekritische Pulshooks früh filtern; keine unnötige Arbeit über alle Countries/Locations.

### Strukturelle Felder

Wenn ein Objekttyp unklar ist:

1. mehrere Vanilla-Dateien derselben Kategorie lesen,
2. wiederkehrende Top-Level-Felder bestimmen,
3. Sonderfelder nur in ihrem bewiesenen Kontext verwenden,
4. Felder ohne Referenz als unbewiesen behandeln.

## 8. GUI-Regeln — besonders streng

GUI ist einer der Bereiche mit der höchsten Halluzinationsgefahr.

Vor jeder GUI-Änderung:

1. Ziel-Vanilladatei lesen.
2. verwendete `type`/Templates bis zur Definition verfolgen.
3. `blockoverride`-Namen aus dem echten Template ableiten.
4. `dump_data_types` für verfügbare Datentypen/Getters prüfen.
5. Expressionen gegen funktionierende Vanilla-Verwendungen verifizieren.

### Datacontext

Nicht davon ausgehen, dass ein Getter überall verfügbar ist. Ein Objekt kann in einem Panel existieren und in einem Tooltip oder Child-Widget fehlen.

### Display-Getter sind nicht automatisch numerische Getter

Runtime-Erkenntnis aus diesem Projekt:

```text
Player.GetTotalWealth
Player.GetTotalTaxBase
```

lassen sich im Economy-Header anzeigen, schlugen aber als Operanden von `Divide_CFixedPoint(...)` fehl. GUI-Anzeigbarkeit beweist also **nicht**, dass ein Getter im selben Kontext numerisch weiterverrechnet werden kann.

Wenn GUI-Mathematik scheitert, echte numerische Script-/Engine-Werte verwenden oder die Rechnung in einen verifizierten `script_value` verlagern.

### Current Economy Getter — runtime-validiert

Unter anderem bestätigt:

```text
EconomyView.GetAllIncome
EconomyView.GetAllExpense
MaintenanceSetting.GetSliderValue
MaintenanceSetting.GetExpense
EconomyView.GetDefaultStabilityInvestment
EconomyView.GetStabilityInvestmentExpense
TaxRateSetting.GetIncome
EconomyView.GetCoinMintingIncome
```

Nicht daraus auf andere Getter extrapolieren.

### Rekonstruktionswerte

`in_game/common/script_values/ela_economy_values.txt` enthält derzeit rekonstruierte Wealth-/Taxable-Wealth-Werte. `R`-präfixierte UI-Werte sind Diagnosewerte und dürfen **nicht** als exakt vanilla-verifiziert bezeichnet werden.

Die Rekonstruktion kann je nach Spielzustand sehr nah an Vanilla liegen, war in anderen Runtime-Tests aber deutlich abweichend. Vor finaler Verwendung muss ein exakter numerischer Wealth-Pfad gefunden oder die Abweichung sauber modelliert werden.

### Whole-file GUI Override

`economy_lateralview.gui` ist ein Whole-file-Override und daher konfliktanfällig. Bei Compatibility-Arbeit immer vom tatsächlich downstream gültigen Stand ausgehen; niemals eine alte Vanilla-Kopie als Merge-Basis verwenden und damit Features anderer UI-Mods still entfernen.

## 9. Aktueller Pie-/Donut-Status — NICHT als gelöst behandeln

Stand des letzten Runtime-Screenshots vom 2026-09-28:

- beide Pies werden gerendert,
- Income-Slices erscheinen grün, Expense-Slices rot,
- die aktuellen Totalwerte werden grundsätzlich geliefert,
- **Income- und Expense-Donut liegen trotz des 0.3.3-Post-Processors weiterhin übereinander**,
- auch die Center-Texte überlagern sich,
- daher ist die aktuelle Layout-Lösung in `fix_economy_pie_layout.py` **runtime-widerlegt**.

Die nächste Bearbeitung darf nicht davon ausgehen, dass `size = { 50% ... }` in diesem Layout zwei getrennte Koordinatenräume erzeugt. Vor dem nächsten Fix funktionierende Vanilla-HBox-/Grid-/Fixed-Width-Beispiele prüfen. Gegebenenfalls explizite Child-Container mit bewiesenen Größen-/Anchor-Regeln oder ein anderes Panel-Layout verwenden.

Tooltips und einzelne Slice-Geometrie erst endgültig bewerten, wenn die beiden Charts räumlich getrennt sind.

## 10. Localization und Assets

Localization-Keys:

- mit eindeutigem Modpräfix versehen,
- alle Script-/GUI-Referenzen auflösbar halten,
- im korrekten EU5-Localization-Baum speichern,
- Encoding und Zeilenformat anhand aktueller Vanilla-Dateien desselben Zielordners prüfen.

Keine pauschale BOM-Regel für alle `.txt`/`.gui` annehmen. Für `.yml` ist UTF-8-BOM in mehreren EU5-Quellen dokumentiert, trotzdem bei neuen Dateitypen immer aktuelle Vanilla-Konvention prüfen.

Für Icons bevorzugen:

1. existierende Inline-/Texticons,
2. existierende Vanilla-Texturen/Widgets,
3. erst danach eigene Assets.

Bei fehlender Localization/GUI außerdem auf identische relative Dateipfade und Shadowing prüfen.

## 11. Kompatibilität, Load Order und Overrides

Zwei Konfliktklassen unterscheiden:

### Gleicher relativer Dateipfad

Whole-file-Override/Shadowing. Effektive Modreihenfolge entscheidet, welche Datei gewinnt.

### Mehrere Dateien verändern dasselbe Datenbankobjekt

Hier können `INJECT`, `REPLACE` und datenbankspezifische Operationen greifen. Das ist **nicht** dasselbe wie Filename-Shadowing.

Regeln:

- `zz_` ist keine universelle Load-Order-Lösung.
- Operationstyp und Datenbankverhalten zuerst verifizieren.
- `INJECT` nicht als beliebiges rekursives Deep Merge verstehen.
- verschachtelte Singleton-Blöcke können durch Inject doppelt/ungültig werden.
- bei tiefen Änderungen kann ein verifizierter kompletter `REPLACE` sicherer sein.
- doppelte Scripted-Effect-/Trigger-Definitionen unter später sortierenden Dateinamen sind kein verlässlicher Override-Mechanismus.
- numerische Felder verhalten sich nicht über alle Datenbankklassen gleich.

Bei GUI-Compatibility-Patches:

1. alle Mods mit identischem relativen GUI-Pfad finden,
2. Dependency-/Playlist-Reihenfolge klären,
3. tatsächlich letzten/downstream Stand als Merge-Basis verwenden,
4. Änderungen minimal halten,
5. fremde Types/Widgets/Assets vollständig nachvollziehen.

## 12. Debugging, Testing und Audit

### Debug-Quellen

Für ernsthafte Syntax-/GUI-Arbeit nach Möglichkeit EU5 im Debug-Modus nutzen und aktuelle Dumps erzeugen:

```text
script_docs
dump_data_types
```

Zusätzlich `error.log` im Paradox-EU5-Benutzerverzeichnis prüfen.

### Kein Logfehler != Erfolg

Ein EU5-Script kann still scheitern. Jede relevante Änderung braucht soweit möglich drei Ebenen:

1. statische Prüfung,
2. Logprüfung,
3. Verhaltenstest im Spiel.

### Positive Kontrolltests

Scanner/Builder dürfen `0 Treffer` nicht still als Erfolg werten. Sie müssen nachweisen, dass sie tatsächlich den erwarteten Input geprüft haben.

Bevorzugt ausgeben:

- Zahl geprüfter Dateien/Objekte,
- Zahl gefundener Definitionen/Anchors,
- bekannte positive Kontrolltreffer,
- erst danach negative Ergebnisse.

Der aktuelle GUI-Builder folgt diesem Prinzip bereits: erwartete Anchors werden gezählt und bei unklarer Lage wird abgebrochen.

### Read-only Audit vor größeren Fixserien

Bei größeren Problemen:

1. erst vollständigen Audit erstellen,
2. Funde klassifizieren,
3. dann gezielt ändern,
4. nach Änderungen Audit/Tests wiederholen.

Klassifikation:

- **sicher falsch** — durch Engine/Vanilla widerlegt
- **verdächtig** — Existenz belegt, Scope/Semantik aber unbewiesen
- **offen** — Referenzlage reicht nicht

Ein Audit soll mindestens berücksichtigen:

- unbekannte/fabrizierte Script-Schlüssel,
- falsche Scopes,
- ungültige Identifiers,
- doppelte Definitionen,
- Localization,
- File Overrides/Shadowing,
- Encoding,
- Reachability von Events/Zuständen,
- Endzustände von Situationen/State Machines,
- Ownership vs. Control/Cores/Integration,
- Designkonformität.

## 13. Bekannte Anti-Patterns

Diese Muster aktiv vermeiden:

1. Syntax aus EU4/CK3/Vic3 ableiten.
2. „Der Begriff existiert, also ist er hier gültig.“
3. plausible Country Tags, Locations, Regions, Enums, Modifier oder GUI-Types erfinden.
4. historische/angezeigte Namen mit internen IDs gleichsetzen.
5. `zz_` als universelle Override-Lösung benutzen.
6. `INJECT` als rekursives Deep Merge behandeln.
7. GUI aus Erinnerungswissen schreiben.
8. Encoding pauschalisieren.
9. fehlende Logfehler als Funktionsbeweis werten.
10. leere Such-/Auditinputs als „clean“ akzeptieren.
11. ein Feature beim ersten Syntaxproblem entfernen, statt zunächst korrekt zu recherchieren.
12. fremde Mods als Engine-Autorität behandeln.
13. eigene fehlerhafte Dateien als Beweis verwenden.
14. Scope-Hops anhand optischer Einrückung zählen.
15. syntaktische Validität mit Designkorrektheit verwechseln.

## 14. Arbeitsablauf für Änderungen

Für nichttriviale Änderungen bevorzugt:

1. Ziel/Problem in `docs/` bzw. bestehendem Research-Backlog verstehen.
2. aktuellen Repo-Stand und betroffene Generatoren lesen.
3. Engine/Vanilla/Referenzrepo recherchieren.
4. Fakten als `Vanilla-verifiziert`, `rekonstruiert` oder `Designannahme` einordnen.
5. kleinstmögliche kohärente Änderung implementieren.
6. generierte Dateien nur über den vorgesehenen Builder erzeugen.
7. Build/Static Checks ausführen.
8. Runtime-Testbedarf explizit nennen.
9. bei Runtime-Fund Doku/Anti-Pattern aktualisieren.
10. `git diff` prüfen, dann logisch committen und pushen.

### Standard-Build unter Windows

```bat
tools\build_debug_gui.bat
```

Der Batch soll die komplette aktuelle GUI-Pipeline ausführen. Einzelne Python-Skripte nur gezielt zum Debuggen direkt starten.

Wenn EU5 nicht automatisch gefunden wird, `--game-dir` bzw. `--source` verwenden.

## 15. Git-/Commit-/Push-Regeln

Änderungen sollen nicht als großer unscharfer Sammelcommit enden.

- Ein Commit = eine sinnvolle, kohärente Änderung.
- Commit-Nachrichten kurz und beschreibend, bevorzugt Conventional-Commit-artig:
  - `fix(gui): separate economy pie chart containers`
  - `feat(mapmode): add fiscal efficiency prototype`
  - `docs: document vassal value research`
  - `refactor(build): make vanilla anchors patch-safe`
- Vor Commit `git status` und `git diff` prüfen.
- Keine generierte `in_game/gui/economy_lateralview.gui` committen; sie ist absichtlich ignoriert.
- Keine fremden oder unzusammenhängenden lokalen Änderungen überschreiben.
- Keine History-Rewrites/Force-Pushes ohne ausdrückliche Anweisung.
- Nach erfolgreicher bzw. bestmöglicher Validierung die sinnvollen Änderungen **committen und auf das vorgesehene Remote pushen**, sofern der Nutzer nichts anderes verlangt.
- Wenn ein Runtime-Test lokal nicht möglich ist, trotzdem nicht behaupten, er sei bestanden. Commit/Doku als `runtime unverified` kennzeichnen und die konkreten Testschritte nennen.
- Bei user-visiblem Versionsschritt `.metadata/metadata.json` und passende Doku konsistent aktualisieren.

## 16. Lernschleife

Jeder echte Engine-/Runtime-Fund soll dauerhaft nutzbar gemacht werden:

1. beobachtetes Symptom festhalten,
2. Ursache festhalten,
3. falsches Muster dokumentieren,
4. verifizierte Alternative dokumentieren,
5. Quelle/Pfad/Version notieren,
6. passende `docs/`-Datei oder Research-Backlog aktualisieren.

Das Projekt soll nicht darauf angewiesen sein, dass ein Agent frühere Chat-Sessions „erinnert“.

## 17. Definition of Done

Eine Änderung ist erst dann fertig, wenn für ihren Umfang angemessen gilt:

- die verwendete EU5-Syntax ist geerdet,
- Scope/Datacontext ist geklärt,
- relevante Vanilla-/Engine-Referenz wurde geprüft,
- Build/Scanner zeigen positive Kontrolltreffer,
- keine neuen offensichtlichen `error.log`-Fehler,
- Runtime-Verhalten wurde getestet oder ausdrücklich als offen markiert,
- Rekonstruktionen/Heuristiken werden nicht als Vanilla-Fakten dargestellt,
- Doku wurde bei neuen Erkenntnissen aktualisiert,
- Commit ist logisch geschnitten und gepusht.

## 18. Schnellcheck vor jeder EU5-Änderung

Vor dem Schreiben von Code kurz fragen:

- Ist das aktuelle EU5/Jomini oder nur Erinnerung aus einem anderen Paradox-Spiel?
- Wo ist die Engine-/Vanilla-Referenz?
- Welcher Scope/Datacontext gilt hier?
- Ist der interne Identifier wirklich verifiziert?
- Handelt es sich um Whole-file-Shadowing oder Datenbankoperationen?
- Ist eine Anzeige-API auch als numerischer Wert nutzbar?
- Kann der Fehler still scheitern?
- Wie beweise ich, dass mein Test tatsächlich etwas geprüft hat?
- Ist dieser Wert Vanilla-verifiziert, rekonstruiert oder Designannahme?
- Muss die Erkenntnis anschließend in `docs/` festgehalten werden?
