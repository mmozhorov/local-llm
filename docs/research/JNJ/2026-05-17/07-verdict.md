# Verdict — JNJ (NYSE) от 2026-05-17

## Bottom line

**HOLD** существующую long-позицию (+2.6%, ~2% портфеля) c trailing-стоп **$198**.
**ADD** до 3% портфеля **только** при возврате цены в зону **$210–$215** + bullish reversal candle на дневном close.
**TRIM** 50% позиции по TP1 **$245** (или раньше при касании $245–$251 без breakaway-volume).
**От текущей цены $226.71 рынок не предлагает margin of safety для новой покупки** — наш E(price) = $198 при весах 25/50/25.

## Метрики решения

| Параметр | Значение |
| Текущая цена (17-May-2026) | $226.71 |
| Сводный fair value range | $200–$230, центральная $215 |
| E(price) при наших весах 25/50/25 | $198 |
| Текущая премия к E(price) | +14% |
| Текущая премия к центральной FV | +5% |
| Sell-side avg target (12m) | $253 (+12%) |
| Stop-loss | $198 (weekly close) |
| Risk от spot до stop | $28.71 / 12.7% |

## Action plan

### 1. Текущая позиция (long, +2.6%, ~2% портфеля)

| Действие | Параметр | Условие |
| **Hold** | Базово | До триггера kill switch или TP |
| **Stop-loss** | **$198** weekly close | Trim 50%, переоценка тезиса |
| **Hard stop** | **$175** weekly close | Exit полностью (SMA200 пробит) |

### 2. Add (опциональный, по limit-ордеру)

| Поле | Значение |
| Buy zone | **$210–$215** |
| Triггер | Касание зоны + bullish reversal candle (engulfing / hammer / pin bar) **на дневном close** |
| Size | **+3% портфеля** (доводим суммарную позицию до 5% — hard cap из scope) |
| Stop | $198 (общий для всей позиции) |
| Allocation | Ladder: 50% на $213, 50% на $209 |
| Risk per add tranche | $14 / 6.6% от entry |
| R:R от entry $211 | Reward avg $261 − $211 = $50; Risk = $13 → **R:R 3.85** |
| E(return) от add @ $210 | +5.0% (расчёт ниже) |
| Срок жизни ордера | до 2026-12-31 или до пробоя $198 |

### 3. Trim (опциональный, по limit-ордеру)

| Поле | Значение |
| Sell zone TP1 | **$245** (50% позиции) |
| Sell zone TP2 | **$260** (30%) |
| Sell zone TP3 | **$280** (20%) |
| Логика | Фиксация на премию к fair value; $280 = bull case / high analyst target |

### 4. Trailing stop logic (динамический)

| Если цена закрывает неделю выше | Поднять stop до |
| $240 | $208 (S1) |
| $260 | $225 (текущий уровень) |
| $280 | $245 (TP1) |

## Sizing & risk (фаза 6 sketch)

**E(return) от add @ $210 (с учётом stop $198):**
- p(bull) 25%: return +27.6% → contribution +6.9%
- p(base) 50%: return −1.0% → contribution −0.5%
- p(bear with stop) 25%: return −5.7% → contribution −1.4%
- **Сумма E(return) = +5.0%**

**Variance**: 0.0175, Sharpe-style ratio E/σ = 0.05 / 0.13 = 0.38 — приемлемо для defensive position.

**Kelly fraction (теоретический):** 2.86× — переоценка из-за stop; на практике беру **0.25-Kelly = 70% от capacity = +3% портфеля**.

**Drawdown impact:**
- При полном размере 5% портфеля и stop срабатывает ($198): max loss = 5% × 12.7% = **0.64% портфеля**.
- Bear без stop (если gap-down ниже $198 и продали ниже): 5% × 50% = 2.5% портфеля — расчётный worst-case при провале stop-execution.

**Корреляция:** JNJ β 0.55 vs S&P; β к XLV ≈ 0.9. Если в портфеле есть другие healthcare (LLY/MRK/PFE/ABT), эффективный размер healthcare-кластера = JNJ + 0.7 × прочие healthcare. **Watch:** при суммарной экспозиции в healthcare > 15% портфеля — пересмотреть JNJ sizing.

## Что мониторить

### Ежедневно (price action)
- Закрытие относительно $208 / $198 (нижние пороги).
- Закрытие выше $245 / $260 (TP-триггеры).
- Объём при пробое любого уровня (> 20-day avg для значимости).

### Еженедельно
- Weekly close < $198 → trim 50% (kill switch).
- Weekly close > $260 на breakaway-volume → re-rate fair value.
- XLV/S&P RS — JNJ как top-2 holding ETF.

### Ежеквартально (binary events)
- **Q2 2026 earnings: 15-Jul-2026.** Consensus EPS $2.84 / Rev $25.01B. Hold через отчёт со stop'ом или trim 25–50% за неделю до.
- **Sep 2026: IRA Round 3 selection list.** Если IMBRUVICA + XARELTO + новый JNJ-drug — kill switch на re-evaluation.
- Q3 2026 earnings (октябрь).
- Q4 2026 / FY 2026 earnings (январь 2027).

### Непрерывно (legal / regulatory)
- Talc bellwether docket: вердикт > $500M → score event.
- Mediator updates: settlement signals.
- FDA pipeline decisions (RYBREVANT/LAZCLUZE label expansion Q4 2026).
- FOMC дот-плот каждое заседание.

## Триггеры на полный re-research

- Любое срабатывание kill switch из фазы 5.
- Smena CEO / CFO (структурный шок).
- M&A > $20B (мега-сделка меняет тезис).
- Через 90 дней — обязательная переоценка (фаза 2 refresh).
- Через 6 месяцев — полный re-research, если позиция в портфеле.

## Anti-patterns check (финальный)

- [x] Решение опирается на **расчёты**, не narrative.
- [x] **Числа**: entry, stop, TP1/2/3, R:R, E(return), Kelly-derived sizing.
- [x] **Stop ниже** существенного support ($200) и EMA50 ($204).
- [x] **TP** дискретные, не «куда-то выше».
- [x] **Kill switches** заданы количественно.
- [x] **Sizing** в рамках hard cap из scope (5% портфеля).
- [x] **R:R** для add ≥ 2.0 (3.85).
- [x] **Bias check** выполнен в фазе 5.
- [x] **Срок** review задан (90 дней / 6 месяцев).

## Caveats

- Фаза 3 имеет flag по неверифицированному H4 и volume — **обязательная сверка с TradingView перед исполнением** ордеров.
- E(price) $198 < spot $226.71 — это сильный сигнал; решение «hold» оправдано только потому, что **позиция уже открыта и защищена stop'ом**. Открывать новую long с нуля по $226.71 **не оправдано**.
- Talc tail-risk имеет ограниченную видимость — mediator-процесс может закрыть его в одну сторону резко (positive или negative). Stop $198 защищает от негативного сценария, но gap-risk на news-driven move присутствует.
- Sizing рассчитан под умеренный риск-профиль из scope (drawdown ≤ 20%, size ≤ 5%). При другом риск-профиле — пересчёт нужен.

## Эволюция тезиса (vs предыдущие фазы)

| Фаза | Ключевой вывод |
| 0 — Scope | Long +2.6%, 2% портфеля, горизонт 6–24m, цель — решение по сделке |
| 1 — Context | Mature compounder с pipeline-driven re-acceleration; Stelara cliff + talc — два главных встречных ветра |
| 2 — Fundamental | Fair value range $200–$230, центральная $215; current price в верхней половине |
| 3 — Technical | Uptrend сильный, но cooling; R:R от текущей 1.20 (не add), R:R от $210 = 3.85 (add активен) |
| 4 — Sentiment | Mixed на 6m (Q2 earnings binary event); mildly positive на 12m |
| 5 — Synthesis | Веса 25/50/25, E(price) = $198, asymmetric downside в 2.8× absolutely |
| **7 — Verdict** | **HOLD + add на pullback к $210–$215 + trim к $245 + stop $198** |

## Источники

Полные ссылки в фазах 1, 2, 4. Ключевые:
- JNJ Q1 2026 earnings — investor.jnj.com
- DCF с WACC 7.2%, g 2.5% — построен в `02-dcf.md`
- Talc litigation status May 2026 — LawsuitInfoCenter
- IRA Medicare drug pricing — CMS
- Peer multiples — StockAnalysis / Yahoo Finance
- Technical levels — ChartMill / Barchart

---

**Полный пакет research:**
- `00-scope.md` — параметры исследования
- `01-context.md` — бизнес, peer set, регуляторика
- `02-fundamental.md` — quality of earnings, P&L, balance, CF, multiples
- `02-dcf.md` — DCF модель + sensitivity
- `03-technical.md` — уровни, индикаторы, setup
- `04-sentiment.md` — новости, sentiment, макро, триггеры
- `05-synthesis.md` — три сценария, E(price), risk register
- **`07-verdict.md`** — финальный action plan **(этот файл)**
