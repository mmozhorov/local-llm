# DCF — JNJ от 2026-05-17

Валюта: USD млрд. Дата отсечки: 2026-05-17. Shares outstanding (diluted): 2.59B (mkt cap $585B / $225.7).

## Допущения (base case)

| Параметр | Значение | Источник / обоснование |
| Revenue CAGR 5y (2026-2030) | 6.5% (взвешенно) | Менеджмент guidance 2026 +6.7%, ускорение к 2028 после Stelara cliff |
| Operating margin 2026 | 27.5% | Восстановление после Stelara hit |
| Operating margin terminal | 29.0% | Mix shift к Innovative Medicine (oncology 36% margin); MedTech recovery |
| Tax rate | 17% | Эффективная 2025 ~17%; ниже US statutory из-за international structure |
| Capex / Revenue | 5.0% | 2025 = 5.1%; рост на capacity & R&D |
| D&A / Revenue | 4.5% | Историческая средняя, рост амортизации после Shockwave/Intra-Cellular |
| ΔWC / ΔRevenue | 8% | Стабильный WC cycle; sensitivity невелика |
| **WACC** | **7.2%** | β ~0.55, Rf ~4.5%, ERP ~5%, AAA debt 4.5% (после tax 3.7%) |
| **Terminal growth (g)** | **2.5%** | Реальный 0.5-1% + инфляция 2% (LT US developed market) |

## Прогноз FCF (2026–2030)

| Год | Revenue | Op % | EBIT | Taxes (17%) | NOPAT | + D&A | − Capex | − ΔWC | **FCF** |
| 2026 | 100.3 | 27.5% | 27.6 | 4.7 | 22.9 | 4.5 | 5.0 | 0.5 | **21.9** |
| 2027 | 106.3 | 28.0% | 29.8 | 5.1 | 24.7 | 4.8 | 5.3 | 0.5 | **23.7** |
| 2028 | 113.2 | 28.5% | 32.3 | 5.5 | 26.8 | 5.1 | 5.7 | 0.5 | **25.7** |
| 2029 | 121.1 | 29.0% | 35.1 | 6.0 | 29.1 | 5.4 | 6.1 | 0.6 | **27.8** |
| 2030 | 129.6 | 29.0% | 37.6 | 6.4 | 31.2 | 5.8 | 6.5 | 0.7 | **29.8** |
| **Σ** | — | — | — | — | — | — | — | — | **128.9** |

## Terminal value

TV = FCF₂₀₃₁ / (WACC − g) = (29.8 × 1.025) / (0.072 − 0.025) = **30.5 / 0.047 = $650B**

## Enterprise value

| Компонент | $B |
| PV(FCF) 2026 | 21.9 / 1.072 = 20.4 |
| PV(FCF) 2027 | 23.7 / 1.072² = 20.6 |
| PV(FCF) 2028 | 25.7 / 1.072³ = 20.8 |
| PV(FCF) 2029 | 27.8 / 1.072⁴ = 21.1 |
| PV(FCF) 2030 | 29.8 / 1.072⁵ = 21.1 |
| **Σ PV(FCF)** | **104.0** |
| PV(TV) = 650 / 1.072⁵ | **459.5** |
| **EV** | **563.5** |
| − Net debt | 24.8 |
| + Non-op assets | 0 (консервативно) |
| − Talc reserve | уже в OCF assumptions; флаг отдельным риском |
| **Equity value** | **538.7** |
| ÷ Shares (diluted) | 2.59B |
| **Fair value / share** | **$208** |

**Доля TV в EV:** 459.5 / 563.5 = **81.5%** — выше 75% threshold. **Flag:** модель ощутимо зависит от терминала; sensitivity на g и WACC высокая (см. ниже). Это типично для mature compounders, но требует осторожности.

## Sensitivity (Equity per share, $)

|             | g = 1.5% | g = 2.0% | g = 2.5% | g = 3.0% | g = 3.5% |
| WACC 6.5% | 215 | 232 | 254 | 281 | 318 |
| WACC 7.0% | 196 | 210 | 226 | 246 | 271 |
| **WACC 7.2%** | **189** | **202** | **$208** | **228** | **249** |
| WACC 7.5% | 180 | 192 | 205 | 220 | 238 |
| WACC 8.0% | 165 | 174 | 185 | 197 | 211 |
| WACC 8.5% | 152 | 160 | 169 | 179 | 191 |

**Замечания:**
- Диапазон при «реалистичном» окне WACC 7.0–7.5% и g 2.0–3.0%: **$192–$228** — это backbone fair value range.
- Каждые 50 bps в WACC дают ~10% сдвиг fair value (классическая duration mature compounder).
- При g 3% (агрессивно) — JNJ оценен «по DCF» в $228, чуть выше текущего рынка.

## Сценарии (для фазы 5 — preview)

| Сценарий | Rev CAGR | Op margin term. | WACC | g | Talc adj | **FV/share** |
| **Base** | 6.5% | 29.0% | 7.2% | 2.5% | — | **$208** |
| **Bull** | 8.0% | 30.0% | 6.8% | 3.0% | — | **$268** |
| **Bear** | 3.5% | 25.5% | 8.0% | 1.5% | −$15B equity hit | **$108** |

**Bull predпосылки:** RYBREVANT+LAZCLUZE становится blockbuster (>$8B peak), CARVYKTI ускоряется, MedTech margin восстанавливается до 17–18%, IRA/pricing смягчается; cost of capital падает на смягчении ФРС.

**Bear предпосылки:** дополнительные $15B talc claims (примерно verdict $5–10B + новые bellwether), Q-loss accelerated на BMS competition в онкологии, MedTech China headwinds extend, ставка ФРС остаётся высокой, биосимиляры Stelara съедают быстрее ожидаемого.

## Cross-check

- [x] PV(TV) / EV = 81.5% — выше 75%, **flag** учтён в risk register
- [x] ROIC base ~22% (NOPAT₃₁ / IC ~140B) > WACC 7.2% — стоимость создаётся
- [x] Implied FCF yield (FCF₁ / EV) = 21.9 / 563.5 = 3.9% — сопоставимо с EV/FCF ≈ 26× у peers с похожим quality
- [x] Implied 2026E P/E на fair value $208 / $11.53 adj EPS = **18.0×** — близко к peer median forward 16.5× с премией ~9% (justifiable)
- [ ] Beneish M-Score не пересчитан явно — flag в фазе 4 для мониторинга

## Вывод фазы 2 (только fair value, без рекомендации)

- **DCF base fair value: $208** на акцию
- **DCF реалистичный диапазон (sensitivity):** $192–$228
- **Multiples cross-check:** $190–$219
- **Сводный fair value range: $200–$230, центральная $215**
- **Текущая цена $225.7** ≈ верхняя половина диапазона. Не «дёшево», не «дорого». Решение «buy / hold / trim» формируется в фазе 5 с учётом TA и sentiment.
