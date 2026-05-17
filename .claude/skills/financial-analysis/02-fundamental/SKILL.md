---
name: financial-fundamental
description: "Фаза 2: фундаментальный анализ. Quality of earnings → P&L → баланс → cash flow → оценка (DCF + мультипликаторы peers). Результат: fair value range."
---

# Фаза 2 — Fundamental analysis

Цель: получить **fair value range** через минимум два независимых метода.

<HARD-GATE>
Не переходи к фазе 3, пока:
1. Есть fair value range (например, $140–$180, центральная $160).
2. Расхождение между методами оценки объяснено.
3. Сохранены оба артефакта: 02-fundamental.md и 02-dcf.md.
</HARD-GATE>

## Под-фазы (выполнять в порядке)

### 2.1 Quality of earnings

Сначала проверь, что цифрам можно верить.

- [ ] Аудитор и наличие оговорок (qualified opinion).
- [ ] GAAP/IFRS vs non-GAAP. Если adjusted EBITDA выше GAAP на > 15–20% — раскрой
      что исключили.
- [ ] Накопленный gap между Net Income и Operating Cash Flow за 5 лет.
      NI растёт, OCF — нет = красный флаг.
- [ ] Beneish M-Score / Sloan accruals — формальные индикаторы манипуляций.
- [ ] Going concern, события после отчётной даты в примечаниях.

### 2.2 P&L (5–10 лет)

| Метрика | На что смотрим |
|---|---|
| Revenue CAGR | Органический vs M&A; темп vs рынок |
| Gross margin | Устойчивость, тренд |
| Operating margin | Операционный леверидж |
| Net margin | Налоговая ставка, разовые события |
| EPS | Разводнение vs buyback |
| ROIC, ROE | ROIC > WACC обязательно для созидания стоимости |

Сравнение **в трёх измерениях**: исторически, с peers, с гайденсом менеджмента.

### 2.3 Balance sheet

- [ ] Net Debt / EBITDA — leverage; нецикличка < 3×, commodity < 1.5×.
- [ ] Interest coverage (EBIT / interest) — > 5× здорово, < 2× проблема.
- [ ] Current / Quick ratio — ликвидность.
- [ ] Working capital cycle (DSO + DIO − DPO).
- [ ] Goodwill / Total assets — риск списания, особенно после M&A.
- [ ] Off-balance: операционная аренда (IFRS 16), пенсии, гарантии.

### 2.4 Cash flow

- [ ] OCF / Net Income > 1.0 устойчиво.
- [ ] **FCF = OCF − capex**. Для equity holder — FCFE.
- [ ] Capex split: maintenance vs growth. Если не раскрыто — оцени maintenance как
      нижнюю границу = D&A.
- [ ] Payout: дивиденды + buyback в % FCF.
- [ ] Cash conversion = FCF / Net Income — целевое 80–100%+.

### 2.5 Valuation

Минимум **два независимых метода**.

**Multiples (relative).** Peer set из фазы 1.

- Для каждого peer — trailing и forward P/E, EV/EBITDA, EV/Sales,
  P/B (только для банков/страховщиков), EV/FCF.
- Сравни медиану peers и текущую компанию; разница > 25% — объясни
  (премия за качество / дисконт за риск).
- Историческая премия/дисконт к own 5y average.

**DCF (intrinsic).** Используй шаблон `shared/templates/02-dcf.md`.

- Явный прогноз 5–10 лет.
- Terminal value через Gordon growth, g обычно 1–3% в реальных.
- WACC: cost of equity по CAPM (Rf + β·ERP), cost of debt after tax,
  по рыночным весам.
- **Три сценария**: base / bull / bear, разные g, маржа, capex.
- Sensitivity table: WACC × terminal g.
- Если PV(terminal value) > 75% от EV — модель «всё в терминале», ненадёжна,
  пометь явно.

**SOTP** (sum-of-the-parts) — если конгломерат или сегменты с радикально
разной экономикой.

**Не применимо:**
- EV/EBITDA для банков, страховщиков, REIT — у них нет смысла. Используй P/B,
  P/E на TBV, P/AUM, P/FFO соответственно.

## Артефакты

- `02-fundamental.md` — quality + P&L + баланс + CF.
- `02-dcf.md` — отдельным файлом, со sensitivity table.

## Exit criteria

- [ ] Fair value range с центральной точкой.
- [ ] Сравнение DCF vs multiples, расхождение объяснено.
- [ ] Self-review пройден.

→ Следующая фаза: `03-technical/SKILL.md`.
