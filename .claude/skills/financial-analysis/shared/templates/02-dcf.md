# DCF — <TICKER> от <YYYY-MM-DD>

## Допущения (base case)

| Параметр | Значение | Источник |
| Revenue CAGR 5y | <%> | <гайденс / sector / consensus> |
| Operating margin terminal | <%> | <тренд / peer median> |
| Tax rate | <%> | <эффективная за 5y> |
| Capex / Revenue | <%> | <maintenance + growth> |
| ΔWC / ΔRevenue | <%> | <история> |
| WACC | <%> | β=<>, Rf=<>, ERP=<>, D/E=<>, kd=<> |
| Terminal growth (g) | <%> | <реальная, 1–3%> |

## Прогноз FCF

| Год | Revenue | Op margin | EBIT | Taxes | NOPAT | D&A | Capex | ΔWC | FCF |
| Y+1 | ... | ... | ... | ... | ... | ... | ... | ... | ... |
| Y+2 |  |  |  |  |  |  |  |  |  |
| Y+3 |  |  |  |  |  |  |  |  |  |
| Y+4 |  |  |  |  |  |  |  |  |  |
| Y+5 |  |  |  |  |  |  |  |  |  |

## Terminal value

TV = FCF<sub>Y+6</sub> / (WACC − g) = <…>

## Enterprise value

| Компонент | Значение |
| Σ PV(FCF) Y+1..Y+5 | ... |
| PV(TV) | ... |
| **EV** | ... |
| − Net debt | ... |
| + Non-op assets / cash above operational | ... |
| **Equity value** | ... |
| ÷ Shares outstanding (diluted) | ... |
| **Fair value / share** | **$...** |

**Доля TV в EV:** <%>. Если > 75% — модель «всё в терминале», ненадёжна.

## Sensitivity (Equity per share)

|         | g = 1% | g = 2% | g = 3% |
| WACC 8% |   |   |   |
| WACC 9% |   |   |   |
| WACC 10% |  |   |   |

## Сценарии

| Сценарий | Revenue CAGR | Op margin | WACC | g | Fair value |
| Base |  |  |  |  | $ |
| Bull |  |  |  |  | $ |
| Bear |  |  |  |  | $ |

## Cross-check

- [ ] PV(TV) / EV < 75%
- [ ] ROIC > WACC в стационарном состоянии
- [ ] Капитализированная отдача (FCF / EV) реалистична vs peer multiples
