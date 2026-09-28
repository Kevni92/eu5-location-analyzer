# 06 – Income-/Expense-Share UI

Stand: 2026-09-28

## Ziel

Die Economy-Seite soll nicht nur absolute Goldwerte zeigen, sondern für jede sichtbare Einnahmen- und Ausgabenposition auch deren relativen Anteil am jeweiligen Monatstotal.

Damit beantwortet die Ansicht direkt zwei Planungsfragen:

- Wie wichtig ist eine Einnahmequelle für die gesamten Monatseinnahmen?
- Wie stark belastet eine Ausgabenposition die gesamten Monatsausgaben?

## Anzeigeformat

### Einnahmen

Feste Einnahmezeilen sowie die Kopfwerte der einstellbaren Einnahmen zeigen:

```text
+43.91 (39.3%)
```

Die Prozentzahl ist:

```text
abs(Einnahmeposten) / abs(EconomyView.GetAllIncome)
```

Erfasst werden insbesondere:

- Minting über `EconomyView.GetCoinMintingIncome`
- Estate Taxes über `TaxRateSetting.GetIncome`
- Trade Income und Selling Food sowie weitere feste Einnahmen über `EconomyView.GetIncome('<category>')`

Die bestehenden Steuer-/Minting-Sliderinformationen bleiben separat erhalten.

### Ausgaben ohne Slider

Feste Ausgabenzeilen zeigen:

```text
-14.47 (14.6%)
```

Die Prozentzahl ist:

```text
abs(Ausgabenposten) / abs(EconomyView.GetAllExpense)
```

Der Builder patcht generisch alle Zeilen, die dem Vanilla-Muster

```text
EconomyView.GetExpense('<category>')
```

folgen. Damit werden z. B. Building Maintenance, Trade Expense, Interest und weitere entsprechende Vanilla-Posten automatisch erfasst.

### Ausgaben mit Slider

Die bereits validierte kompakte Anzeige bleibt zunächst bestehen:

```text
32% | 28.5%B
```

Dabei ist der erste Wert die Sliderstellung und der zweite Wert der Anteil der tatsächlichen aktuellen Kosten an den gesamten Monatsausgaben.

## Technischer Ansatz

Die Budgetanteile werden ausschließlich aus Engine-Gettern berechnet, die im Vanilla-GUI bereits als numerische `CFixedPoint`-Werte verwendet werden.

Das unterscheidet diesen Teil bewusst von der Wealth-/Tax-Base-Probe: `Player.GetTotalWealth` und `Player.GetTotalTaxBase` haben sich im GUI-Math-Kontext als reine Display-/Localization-Getter erwiesen und lassen sich dort nicht direkt mit `Divide_CFixedPoint` verrechnen.

## Erkenntnis aus Runtime-Test 0.2.2-alpha

Der Screenshot vom 2026-09-28 zeigte:

```text
Vanilla Wealth: 611.24
rekonstruierter Wealth: 703.09
Tax Base: 192.41
rekonstruierte Quote: 27.3%
```

Damit ist bewiesen, dass die bisherige Rekonstruktion

```text
location_tax_base / local_control
```

Vanillas Wealth nicht exakt reproduziert.

Folge:

- Der Wealth-Debugwert bleibt mit Präfix `R` sichtbar.
- Auch die daraus berechnete Taxable-Wealth-Quote wird mit `R` markiert.
- Sie darf nicht als endgültiger Wert interpretiert werden.
- Für die finale Tax-Base/Wealth-Anzeige muss noch ein exakter numerischer Wealth-Pfad gefunden werden.

Aus den im Screenshot sichtbaren Vanilla-Werten ergäbe sich rechnerisch für diesen Spielstand ungefähr:

```text
192.41 / 611.24 = 31.5%
```

Diese 31.5% werden derzeit aber nicht automatisch durch die Mod berechnet, weil der numerische Vanilla-Wealth-Wert noch nicht im Script-/GUI-Math-Kontext verfügbar gemacht wurde.

## Version

Die Erweiterung ist Bestandteil von `0.2.3-alpha`.
