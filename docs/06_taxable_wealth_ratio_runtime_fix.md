# 06 – Taxable-Wealth-Ratio: Runtime-Fix

Stand: 2026-09-28

## Beobachteter Fehler

Die GUI-Ausdrücke

```text
Divide_CFixedPoint(Player.GetTotalTaxBase, Player.GetTotalWealth)
```

und zuvor auch eine Variante mit `Select_CFixedPoint(...)` schlagen zur Laufzeit mit `FetchData failed` fehl.

Damit ist praktisch bestätigt: `Player.GetTotalTaxBase` und `Player.GetTotalWealth` sind in diesem UI-Kontext als direkte Anzeige-/Localization-Getter verwendbar, aber nicht als numerische `CFixedPoint`-Argumente für GUI-Mathematik.

## Neuer Ansatz ab 0.2.2-alpha

Mathematik wird aus dem GUI-String herausgenommen und in `in_game/common/script_values/ela_economy_values.txt` berechnet. Die GUI zeigt nur noch zwei getrennte Werte an:

```text
[Player.GetTotalTaxBase|2]
[Player.MakeScope.ScriptValue('ela_taxable_wealth_share')|%1]
```

Vanilla-Script-Values verwenden `country_tax_base` numerisch. Das Summieren über `every_owned_location` ist ebenfalls Vanilla-Syntax.

## Rekonstruktion von Wealth

Für die aktuelle Testversion wird Wealth pro Location rekonstruiert als:

```text
location_tax_base / max(local_control, 0.01)
```

und anschließend über alle eigenen Locations summiert. Dieses Muster ist in aktueller 1.3-Community-Praxis als `local_wealth_display` belegt, ist aber noch nicht als exakt identisch zu `Player.GetTotalWealth` validiert.

Deshalb ist der daraus gebildete Wert zunächst **rekonstruiert**, nicht `Vanilla-verifiziert`.

## Nächster Runtime-Test

Nach dem Build von 0.2.2-alpha bitte Economy öffnen und prüfen:

1. keine `PdxDataFetchLocalizedData`-/`Divide_CFixedPoint(Player.GetTotal...)`-Fehler mehr,
2. Tax Base zeigt wieder den absoluten Vanilla-Wert,
3. daneben erscheint ein Prozentwert,
4. Screenshot mit gleichzeitig sichtbarem Wealth und Tax Base senden.

Aus `Tax Base / angezeigtem Prozentwert` lässt sich dann der vom Script Value rekonstruierte Wealth zurückrechnen und direkt gegen den oben angezeigten Vanilla-Wealth vergleichen.
