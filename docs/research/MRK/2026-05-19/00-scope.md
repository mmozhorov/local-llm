# Scope — MRK (Merck & Co.) от 2026-05-19

## TL;DR
- Компания: Merck & Co., Inc. (NYSE: MRK) — US pharma giant (**не** Merck KGaA Germany / EMD)
- Горизонт: 6–24 месяца
- Валюта: USD
- Бенчмарк: S&P 500
- Цель работы: принятие решения по сделке (hold / add / trim)

## Параметры

| Параметр | Значение | Комментарий |
| Горизонт | 6–24 месяца | Наследуется от JNJ/KO scope |
| Валюта учёта | USD | Натив MRK |
| Бенчмарк | S&P 500 | Широкий рынок |
| Допустимая просадка позиции | 20% | Умеренный риск-профиль |
| Макс. размер позиции (% портфеля) | 5% | Hard cap |
| Цель работы | Принятие решения по сделке | Финал — action plan |
| Известная позиция | Long, P&L положительный (точный % не указан, default +5..+15% / midpoint +10%) | Anchoring bias учесть в фазе 5 |
| Размер позиции (default) | ≈ 2% портфеля | Уточнить при необходимости |

## Подтверждение пользователя

> 2026-05-19. Пользователь подтвердил scope от JNJ/KO (горизонт 6–24м, USD, S&P 500, умеренный риск, цель — решение по сделке). Long-позиция в плюсе. P&L precision и точный size позиции взяты по default — если для action plan критично, уточним в фазе 6.

## Ограничения

- Web search: доступен.
- Последняя доступная отчётность MRK: 10-Q Q1 2026 — будет верифицировано в фазе 1.
- Cutoff модели: январь 2026. Свежие данные после — через web search.
- Существующий long с anchoring — следить за confirmation bias в фазах 4-5.

## Гипотезы для проверки (preview)

- **MRK = большая фарма с одной мега-зависимостью**: Keytruda (pembrolizumab) ~50%+ выручки. Главный thesis-driver.
- **Patent cliff 2028+** для Keytruda (biosimilar entry US) — **центральный риск horizon 24m**.
- **Pipeline replacement story**: можем ли мы видеть, что MRK успешно замещает Keytruda через subcutaneous Keytruda (новое IP), Winrevair (PAH), Capvaxive (PCV21), oncology beyond pembro, Gardasil expansion?
- **Multiple compression risk** перед LoE: даже с великой pipeline-replacement market исторически derate P/E за 1-2 года до cliff.
- **Animal Health divestiture** уже не вариант (Organon spinoff 2021 уже произошёл — MRK теперь pure-play pharma).
- **Gardasil China issue** — недавняя слабость, watch как продолжается.
- **Cardiovascular / cardio-metabolic** — растущий сегмент после Acceleron acquisition.

## План фаз

| Фаза | Файл | Статус |
| 0 | `00-scope.md` | ✅ |
| 1 | `01-context.md` — бизнес-модель, сегменты, pipeline, peers | pending |
| 2 | `02-fundamental.md` — quality/health/growth + DCF | pending |
| 3 | `03-technical.md` — trend, RS, S/R, ATR | pending |
| 4 | `04-sentiment.md` — analysts, insiders, options, news | pending |
| 5 | `05-synthesis.md` — bull/bear, risk matrix, scenarios | pending |
| 6 | `06-verdict.md` — финальный action plan | pending |
